# Make predictions useful: uncertainty, reliability and privacy

Source: https://ml-biomat.com/tutorials/machine-learning/m39/en/
Language: en

Move from confidence to operating conditions through probabilities, prediction sets, perturbations and distribution changes.

## 1. From counting correct answers to using a prediction

A parcel-sorting system reads a handwritten digit. “This is an 8 with probability 0.51” can lead to a different action from “This is an 8 with probability 0.99”: send the first image to a person, accept the second automatically. Those actions become useful only when the probabilities have a meaningful relationship with actual performance. A new camera, tilted paper or unfamiliar handwriting introduces another question: does the same relationship still hold? Reliability therefore concerns an entire chain of use—how a prediction expresses uncertainty, what happens to ambiguous records, which changes cause errors, and how data are protected during training and release.

Probability forecasts were evaluated long before deep learning. A weather service can collect many occasions on which it predicted an 80% chance of rain, then examine whether rain occurred on roughly 80% of those occasions. Classification adds a selection step because an interface often displays only the most probable class. Guo and colleagues’2017 study of neural-network calibration highlighted a distinction that accuracy can hide: better classification does not automatically produce probabilities that better match observed frequencies. The useful historical lesson is to measure two things separately—how well scores rank the correct answer, and how accurately their numerical probabilities describe uncertainty.

Our running experiment uses public 8×8 handwritten digits. A random partition assigns the 1797 images to 900 training records,150 temperature-tuning records,150 conformal-calibration records and 597 test records, without overlap. Each partition has a different job. Additional synthetic experiments give us known noise in a regression curve, two explicitly constructed federated clients, and a bounded statistic for privacy calculations. This combination lets us follow actual model outputs while retaining small examples in which the underlying calculation can be checked by hand.

## 2. Noisy observations and an incompletely learned model

Repeated readings from the same thermometer can vary even under apparently identical conditions. More training observations may help estimate that variation without removing the instrument’s noise. A different difficulty arises when a model trained only between 0 and 30 degrees is asked about a freezing environment: its knowledge does not cover the requested conditions. These are commonly called aleatoric, or data, uncertainty and epistemic, or model, uncertainty. The distinction depends on available information. Recording a previously missing environmental variable can make some apparently random variation predictable, so a statement about irreducible noise always belongs to a particular conditioning set and task.

Kendall and Gal’s 2017 work brought these two forms of uncertainty into a common treatment for deep vision. We inspect them with a smaller regression example. One hundred inputs lie between −3 and 3; the mean response follows a sine curve, while noise standard deviation is 0.1 plus 0.12 times the absolute input. The center is therefore quieter than the edges. Five independently initialized neural networks use bootstrap samples of the observations. Each predicts a mean and a positive variance, learned through Gaussian negative log likelihood. This allows different input locations to have different predicted noise levels rather than imposing one constant variance.

$$
\widehat{\operatorname{Var}}(Y\mid x)=\frac1M\sum_{m=1}^M\sigma_m^2(x)+\frac1M\sum_{m=1}^M[\mu_m(x)-\bar\mu(x)]^2,\quad\bar\mu=\frac1M\sum_m\mu_m
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5eab15f1c4638adc5f25a660.svg) | Input and random outcome; feature-specific input units and y outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/b0f36d3188e052b14d52a5a7.svg) | Model index, count, predicted mean and variance; y units and squared y units. |
| ![Formula](https://ml-biomat.com/static/agent-math/53ee4b0d1216901fe0bb79f8.svg) | Ensemble mean and mixture variance; y units and their square. |

Treat models as M equally weighted conditional distributions and apply total variance. Means 1 and 3 with noise variance 0.25 each give mean 2, mean variance 1 and total variance 1.25. Division by M defines the mixture; it is not an unbiased sample-variance estimator.

Imagine five observers, each providing a distribution rather than a single number. Even if their central predictions agree, their individual distributions may be broad. If their centers differ as well, the mixture becomes broader still. The first term averages the component noise variances; the second measures disagreement among their means. Division by five follows from an equally weighted mixture. These trained networks define a computable approximation, rather than a complete Bayesian posterior obtained simply by training five times. Architecture, prior restrictions and the training observations all influence how much their predictions disagree.

![Five heteroscedastic networks each predict a mean and noise variance from 100 training records. Left: mean±1.96 total standard deviations. Right: mean disagreement, predicted noise and known generating noise. Vertical lines mark the training-input range.](https://ml-biomat.com/static/tutorials/machine-learning/figures/3e5f760c77ab360173bdca07.svg?v=3e5f760c77ab)

Figure 1Five heteroscedastic networks each predict a mean and noise variance from 100 training records. Left: mean±1.96 total standard deviations. Right: mean disagreement, predicted noise and known generating noise. Vertical lines mark the training-input range.

Start reading the figure at the vertical lines marking −3 and 3. Inside that range there are observations; outside it the networks extend their learned functions. Near input 4, average predicted noise variance is about 1.70 and variance among model means about 0.057, whereas the known generating noise variance is approximately 0.34. Some unfamiliar-region mismatch has entered the predicted noise term. The estimated decomposition and the generating decomposition therefore deserve separate inspection. The left-hand band uses mean plus or minus 1.96 total standard deviations as a moment summary. Its actual coverage depends on distribution shape and extrapolation error; conformal calibration will address coverage directly using separate observations.

## 3. Making ninety-percent confidence mean something

A classifier typically produces unnormalized class scores, or logits, before applying softmax. Multiplying every score by the same positive factor preserves the winning class but pushes probabilities toward zero and one. We deliberately multiply the fitted model’s logits by 2.5 to create a controlled overconfidence example, then fit one positive temperature using only the 150 tuning images. This separates a change in probability expression from a change in classification ability. A larger temperature compresses score differences and usually makes probabilities flatter. It acts on the scale of the same class scores, leaving their ordering unchanged.

$$
p_j(x;T)=\frac{\exp(z_j(x)/T)}{\sum_{k=1}^{K}\exp(z_k(x)/T)},\qquad T>0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39a8252b6cee9c681e60c71c.svg) | Input, class-j logit, class count and class indices; logits are dimensionless scores. |
| ![Formula](https://ml-biomat.com/static/agent-math/a94cd21cc54c4257a0be4fe2.svg) | Positive temperature and class probability, dimensionless. |

Dividing every score by a positive constant preserves order. Logits(2,0) give first-class probability 0.881 at T=1 and 0.731 at T=2. Fit T by minimizing negative log likelihood on an independent tuning set.

The fitted temperature is approximately 2.2075. Test accuracy remains 92.13%, with zero changes in the most probable class, while negative log likelihood falls from about 0.258 to 0.195. Negative log likelihood rewards probability assigned to the observed class and strongly penalizes confident errors, so it detects a change that accuracy misses. The temperature comes from a separate tuning sample; test records supply the final measurements. Repeatedly choosing a calibration procedure after inspecting the test results would give those records a different role, turning a final evaluation set into another source of fitting decisions.

$$
\operatorname{ECE}=\sum_{b=1}^B\frac{n_b}{N}\left|a_b-c_b\right|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/437425f90c982ec6174f0461.svg) | Confidence-bin index, bin count, bin sample count and total test count. |
| ![Formula](https://ml-biomat.com/static/agent-math/f7a162fbcad799200a452030.svg) | Bin accuracy, average maximum probability and weighted absolute gap, dimensionless. |

Two equal bins with confidence 0.6/0.9 and accuracy 0.5/0.8 give ECE 0.1. The estimate depends on binning and sample size; empty bins carry no weight.

A reliability diagram groups records with similar maximum predicted probabilities. Its horizontal coordinate is average confidence within a bin; its vertical coordinate is the fraction classified correctly. Points below the diagonal indicate greater confidence than observed accuracy, while points above it indicate the reverse. With ten equal-width bins, expected calibration error decreases from approximately 0.0513 to 0.0193. Read this scalar alongside bin counts: a large bin with a small gap and a tiny bin with a large gap can contribute similarly. Changing the binning changes the estimate. The code retains counts, confidence and accuracy for every occupied bin so that the average remains interpretable.

![Top-class reliability, confidence distribution and selective prediction for 597 test digits. Temperature is fitted on a separate 150 records; labels beside the right-hand points give acceptance thresholds.](https://ml-biomat.com/static/tutorials/machine-learning/figures/3465fce7c540be16aa0cc090.svg?v=3465fce7c540)

Figure 2Top-class reliability, confidence distribution and selective prediction for 597 test digits. Temperature is fitted on a separate 150 records; labels beside the right-hand points give acceptance thresholds.

Confidence also connects to workload. Accepting only predictions with maximum probability at least 0.9 retains 471 images, or 78.89% of the test set, with an error rate of about 0.64% among retained records. The other 126 require another route. Raising the threshold to 0.99 retains 308 images, with no observed errors in this particular subset. A deployed system would continue accumulating error counts on new accepted records. A practical threshold should be selected using separate validation data and the costs of mistakes, missed cases and human review. Maximizing confidence alone says nothing about how the rejected workload is handled.

![Reliability curves and probability histograms for logistic regression, SVC, isotonic calibration and sigmoid calibration.](https://ml-biomat.com/static/tutorials/machine-learning/figures/26cd6d1fa2a0abb04db43ef7.png?v=26cd6d1fa2a0)

Figure 3Original scikit-learn calibration example: positive-class probabilities versus observed positive fractions, with probability histograms below. This binary plot concerns positive-class probabilities; our digit experiment concerns top-class confidence and accuracy. scikit-learn contributors, BSD-3-Clause, unmodified.

The reproduced official figure provides a complementary view. Its vertical axis is the observed positive fraction in a binary task; our digit diagram instead uses correctness of the most probable class in a ten-class task. Establish which event is being calibrated before comparing curves. Sigmoid calibration learns a smooth mapping, isotonic regression learns a monotonic stepwise mapping, and temperature scaling learns a single scale while preserving multiclass score order. Simpler mappings can be more stable with limited calibration data; flexible mappings can capture more complex distortions when enough relevant data are available. All require calibration observations representative of the intended operating conditions.

## 4. Retaining a set of plausible answers

Sometimes a set is more useful than a single answer. An unclear address digit might be handed to an operator as “3 or 8”; a continuous prediction might be accompanied by an interval. Conformal prediction connects such outputs to a finite-sample ordering calculation. First fix the fitted predictor. Then use separate calibration observations to measure how incompatible their true outcomes look to that predictor. A new outcome is assessed against those scores. The conformal tradition developed from the late twentieth century onward around exchangeability and ranks; the tutorial by Angelopoulos and Bates shows how this structure can be attached to many modern predictors.

$$
s_i=1-p_{y_i}(x_i),\quad k=\lceil(n+1)(1-\alpha)\rceil,\quad q=s_{(k)},\quad C(x)=\{j:1-p_j(x)\le q\}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d00d1d454d62db2557ded6e9.svg) | Conformal-calibration index, count, input, true label and fixed model class-j probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/82d95afabbbe1d8f61b7227b.svg) | True-class nonconformity, kth ascending score and one-based rank; scores are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c82e35d09cd7e769da2ba9d9.svg) | Target miscoverage, threshold, prediction-label set and class index; probabilities are dimensionless and size counts labels. |

For n=150 and alpha 0.1, k=136. Here q≈0.4324 admits classes with probability at least 0.5676. If k=n+1, use infinity. Conditional on a fixed fitted model, exchangeable calibration and new scores yield at least 1−alpha marginal coverage by the rank among n+1 positions; using≤ handles ties conservatively.

Our score is one minus the probability assigned to the true class, so a poorly supported true class has a larger score. Sorting 150 calibration scores and choosing target miscoverage 0.1 selects position 136, using a one-based rank. This is a specific finite-sample order statistic, rather than an unspecified software interpolation at the 90th percentile. The extra position accounts for the new observation. If its score and the calibration scores are exchangeable, the new rank can be viewed as uniformly placed among 151 positions. Choosing a sufficiently high order statistic controls marginal miscoverage over the randomness of calibration and the new record. It does not assign identical coverage to every image, class or image-quality group.

The fitted threshold is approximately 0.4324, so a class enters the set when its probability is at least 0.5676. Since that requirement exceeds one half, this run produces at most one class per set. Among 597 test images,27 sets are empty and the remainder are singletons; average set size is about 0.955 and true-label coverage 90.45%. An empty set here means that no class meets the common probability requirement. If an application needs several candidates for ambiguous images, a score based on cumulative sorted class probabilities offers another construction, followed by fresh calibration. The score determines efficiency and set shape; the rank argument supplies the coverage connection.

## Turn a calibration rank into visible intervals

Nine fixed absolute calibration residuals appear on the left; ten teaching records show prediction intervals and observed outcomes on the right. Lowering target miscoverage widens intervals; increasing the new-data shift moves only right-hand outcomes. Displayed coverage is a finite-sample count; theoretical marginal coverage relies on exchangeability over repeated sampling.

[Figure: Ordered calibration scores and new prediction intervals](https://ml-biomat.com/tutorials/machine-learning/m39/en/#M39-plot)

The interaction applies the same rank idea to absolute regression residuals. Nine ordered calibration residuals and target miscoverage 0.2 select the eighth value,0.6, giving interval width 1.2. Moving the outcomes of the new records increases the number outside their intervals while leaving the old calibration residuals untouched. Two ideas become visible at once: empirical coverage is a direct count, and a guarantee derived from old scores depends on the relevant exchangeability conditions holding for new observations. Adapting to a different noise level calls for matching calibration records or an extension whose weighting or grouping assumptions are explicitly justified.

## 5. A new camera can change the operating problem

Distribution changes can affect input appearance, class proportions or the relationship between an input and its outcome. These possibilities call for different checks. Describing all of them simply as “OOD” can hide the relevant mechanism. A hospital changing scanners may alter pixel statistics and also change which patients enter its database; a previously rare condition becoming common alters label prevalence. Define the training environment, intended operating environment and proposed change before selecting recalibration, reweighting, additional sampling or retraining. When the meaning of the label has changed, the task definition itself also needs attention.

We rotate each of the 597 test images by 30 degrees, retain the 8×8 canvas, use linear interpolation and fill the boundary with zeros. This is a specified transformation involving orientation, local intensities and cropped boundaries. Applying the original predictor, temperature and conformal threshold reduces classification accuracy to 49.08% and prediction-set coverage to 41.54%. The old calibration scores came from unrotated images, while the new observations systematically differ. Plotting set size beside coverage helps reveal whether the model is becoming uncertain or remains confident in an incorrect class. The transformation is an image-shift experiment, not an assumption that the full conditional label relationship is unchanged.

![Prediction-set coverage and size before and after 30° rotation; image-quality groups use a training-derived ink threshold. All use the same conformal threshold. The dashed line is the nominal 90% marginal target.](https://ml-biomat.com/static/tutorials/machine-learning/figures/b62d714c155fd686748fa61a.svg?v=b62d714c155f)

Figure 4Prediction-set coverage and size before and after 30° rotation; image-quality groups use a training-derived ink threshold. All use the same conformal threshold. The dashed line is the nominal 90% marginal target.

One minus the maximum class probability can also serve as an anomaly score distinguishing original from rotated images. Its AUROC is approximately 0.844 here, indicating useful separation with remaining overlap. Choosing an operational alert threshold still requires an allowed false-positive rate and an examination of the transformations that escape detection. Sensitivity to rotation does not automatically imply sensitivity to incorrect labels, novel classes or blur; these belong in separate evaluation groups. Keeping original and transformed records paired also makes it possible to follow how an individual case moves between correctness, uncertainty and confident error.

## 6. Noise chosen to move toward an error

Random noise has no particular objective, while an adversarial perturbation is chosen to increase a model’s loss. Goodfellow and colleagues’ fast gradient sign method gives a particularly transparent first-order calculation. Treat the 64 pixels as differentiable coordinates, calculate the loss gradient with respect to them, and move each coordinate in the direction of increasing loss. Small changes in many coordinates can collectively produce a substantial score change. This history explains why judging two images as visually similar is only part of a robustness study: the allowed changes and the procedure used to search for them must also be specified.

$$
x_{\rm adv}=\operatorname{clip}_{[0,1]}\!\left(x+\epsilon\operatorname{sign}\nabla_x\ell(f_\theta(x),y)\right),\quad\|x_{\rm adv}-x\|_\infty\le\epsilon
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a1941f9cd259ed6c94c9c2b7.svg) | Original and perturbed inputs, fixed model parameters, predictor and true label; inputs are 64-dimensional 0–1 pixels. |
| ![Formula](https://ml-biomat.com/static/agent-math/51e7596ee37a2ca79a5c442d.svg) | Cross entropy, input gradient and elementwise sign; dimensionless loss. |
| ![Formula](https://ml-biomat.com/static/agent-math/d2e0462cdaf8f016404392f2.svg) | Pixel budget, clipping to the valid range and maximum absolute component norm; epsilon uses normalized pixel units. |

Pixels(0.2,0.95), gradient signs(+1,+1) and epsilon 0.1 become(0.3,1.0), changing by(0.1,0.05). For a first-order loss approximation, each signed endpoint maximizes loss increase inside the coordinate box.

A budget of 0.1 means a maximum change of 0.1 per pixel after normalization to the interval from zero to one. Clipping retains valid intensities. The difference image uses an explicit −0.1 to 0.1 color scale, so its strong red and blue colors are a visualization of small changes rather than original image intensities. The standard model scores about 92.13% on clean images and 51.42% under FGSM with this budget. A second model trains on equally weighted clean and budget 0.1 FGSM cross entropies. It scores 91.12% on clean images and 70.35% under a fresh budget 0.1 attack against its own parameters.

![One 8×8 digit, its FGSM version and actual pixel difference, on 0–1 and −0.1 to 0.1 scales. Each model is attacked using its own gradient; the right panel compares white-box FGSM accuracy at identical budgets.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5d6c6c5b3fb1583d96be75c8.svg?v=5d6c6c5b3fb1)

Figure 5One 8×8 digit, its FGSM version and actual pixel difference, on 0–1 and −0.1 to 0.1 scales. Each model is attacked using its own gradient; the right panel compares white-box FGSM accuracy at identical budgets.

Recomputing the attack matters. An input optimized against the standard model may no longer represent an equally effective direction for the defended model. Comparing defenses requires the same allowed perturbation set and comparable attack computation, followed by stronger searches such as multiple steps and different initializations. The present curves measure a one-step FGSM procedure, rather than an exhaustive worst case throughout the perturbation box. A certified robustness radius answers a different computational question, using a provable bound or, for example, a randomized-smoothing argument under its stated conditions. Its distance metric and probability statement belong with the reported radius.

Contaminated training data provide another failure route. The code randomly selects 90 of 900 training labels, shifts each class number cyclically by one, and fits a third network with the same initialization and training procedure. Its clean-test accuracy is 92.80%, compared with 92.13% for the original fit. In this finite run the label corruption does not lower aggregate test accuracy; the result makes repeated seeds, targeted cases and data-level checks useful extensions of the experiment. Real poisoning may target particular records or insert triggers. Evaluation should then record clean performance, targeted changes and contamination fraction together. Data versions, label review, duplicate checks and update inspection address these entry points more directly than adding noise to test images.

## 7. Following average performance into individual groups

A strong overall score can coexist with persistent errors in one group. We divide test images using the median training-set mean pixel intensity, fixing the rule before examining test outcomes. The lower-ink and higher-ink groups contain 280 and 317 images, with coverage of approximately 91.79% and 89.27%. This is an image-quality stratification showing how the aggregate 90.45% is composed. A group definition, its sample size and its task meaning belong together: brightness strata in digit images answer a different question from demographic fairness in hiring, lending or service allocation.

$$
\operatorname{TPR}_g=\frac{TP_g}{TP_g+FN_g},\qquad\operatorname{FPR}_g=\frac{FP_g}{FP_g+TN_g}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/983459c66fab7d802fbf231f.svg) | Group index and counts of true positives, false negatives, false positives and true negatives. |
| ![Formula](https://ml-biomat.com/static/agent-math/852109845d67c334953178b1.svg) | Detection rate among actual positives and false-alarm rate among actual negatives, dimensionless; denominators must be positive. |

Detecting 16 of 20 actual positives and falsely flagging 8 of 80 negatives gives TPR 0.8 and FPR 0.1. Each group uses its own positive and negative denominators, not total group size.

For a binary decision with a defined positive class, demographic parity compares selection rates across groups. Equal opportunity compares detection rates among actual positives; equalized odds compares both detection and false-positive rates. Their denominators and objectives differ. When groups have different prevalences, identical true- and false-positive rates can still produce different overall selection rates. Choosing a criterion therefore starts with consequences: who bears the cost of a missed case, who bears the cost of a false alarm, how the label was generated, and which institutional requirements apply. Reporting several measures can expose tradeoffs while leaving those substantive choices visible.

Small groups add sampling variability. One additional error among ten people changes the measured rate by ten percentage points; fine intersections of attributes can create many such groups. Counts, uncertainty intervals and measurements across time help interpret the observed differences. Label availability may itself depend on past decisions and deserves inspection. Data governance enters the same workflow through permitted uses, label and version histories, access and retention rules, and a process for withdrawal or correction. These practices preserve the meaning of a comparison across model revisions and define the record-level unit that a privacy mechanism is meant to protect.

## 8. Reducing one record’s influence on a release

Even an average can reveal an individual value. Knowing 99 records and the exact sum of 100 allows the final value to be recovered. Differential privacy therefore compares two data worlds differing in one record, rather than asking only whether an output contains names. The probabilities of released events should remain close across those worlds. Dwork and Roth’s monograph develops a mathematical definition that can be analyzed for randomized mechanisms and multiple releases. We adopt a fixed sample count and replacement of one record as the neighboring-dataset relation, making the protected change explicit before calculating any noise.

$$
\Pr[\mathcal M(D)\in S]\le e^\epsilon\Pr[\mathcal M(D^\prime)\in S]+\delta
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a5e0799435269c7929f194f6.svg) | Adjacent datasets: fixed count and replacement of one record in this chapter. |
| ![Formula](https://ml-biomat.com/static/agent-math/be63aeac331eaa36afb23131.svg) | Randomized release mechanism, arbitrary measurable output event and probability over mechanism randomness. |
| ![Formula](https://ml-biomat.com/static/agent-math/24a3eb098ec2e963fece6ef7.svg) | Nonnegative dimensionless privacy parameters: exponential probability-ratio bound and additive slack. |

The inequality holds for every neighboring pair and output event. With epsilon=ln 2 and delta 0, an event with probability 0.1 on one side has at most 0.2 on the other; exchanging the datasets also satisfies the bound. Delta is additive slack, not a direct personal-disclosure probability.

For 100 values restricted in advance to the interval from zero to one, changing one record can alter the sum by at most one and the mean by at most 0.01. This maximum change is sensitivity. A Laplace mechanism chooses noise according to sensitivity divided by the privacy parameter. Its scale follows from the bounds, sample count, adjacency relation and desired parameter, rather than an informal judgment that an output looks sufficiently noisy. Expanding the bounds to zero through 100 multiplies sensitivity by 100. Selecting the bounds by an unprotected examination of private data would add another information-bearing step to analyze.

$$
\widetilde\mu=\frac1n\sum_{i=1}^{n}\operatorname{clip}_{[a,b]}(x_i)+Z,\quad\Delta=\frac{b-a}{n},\quad Z\sim\operatorname{Laplace}(0,\Delta/\epsilon)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/50f030f03bd74cf6533e1194.svg) | Fixed record count, index, value and predeclared public clipping bounds; values and bounds share units. |
| ![Formula](https://ml-biomat.com/static/agent-math/574b08031328fb735714c7c3.svg) | Released mean, maximum mean change under one-record replacement and random noise; original value units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d75420bd21d22fb2849de561.svg) | Dimensionless privacy parameter and zero-location Laplace distribution with scale sensitivity/epsilon; scale has value units. |

For n=100 and bounds[0,1], sensitivity 0.01. Epsilon 0.5 gives scale 0.02 and SD sqrt 2×0.02≈0.02828. One replacement changes a bounded record by at most b−a; averaging divides that change by n.

The public synthetic experiment draws 10,000 noises at each setting. Epsilon 0.5 gives theoretical root mean squared error 0.02828 and simulated error about 0.02874. At epsilon 0.1, the theoretical value rises to approximately 0.1414. A smaller parameter tightens the relationship between neighboring output distributions while making the release noisier. The code uses a public fixed seed to reproduce a distribution plot. A mechanism releasing a statistic from private records instead needs appropriate nonpublic secure randomness, correct sensitivity and cumulative accounting. Publishing the noise seed alongside a private noisy statistic changes the information available to an observer.

![Left and middle: Laplace noise and 10,000-draw RMSE for public synthetic data. Right: FedAvg with two heterogeneous clients; the horizontal axis counts communication rounds, with different local work per round.](https://ml-biomat.com/static/tutorials/machine-learning/figures/b5242662d2267c6044985882.svg?v=b5242662d226)

Figure 6Left and middle: Laplace noise and 10,000-draw RMSE for public synthetic data. Right: FedAvg with two heterogeneous clients; the horizontal axis counts communication rounds, with different local work per round.

Repeated releases accumulate information. Two pure differential-privacy mechanisms with epsilon 0.5 each on the same records have a basic composed upper bound of epsilon 1 and delta zero. More refined accountants can use sampling and mechanism structure to analyze training. DP-SGD applies this reasoning to optimization by computing per-example gradients, clipping each to a declared norm bound, adding Gaussian noise to their aggregate, and accounting for sampling rate, noise multiplier and update count. Ordinary gradient clipping controls optimization updates; the private-training mechanism additionally requires the per-record sensitivity calculation, randomness and accounting.

The protected unit matters as much as the algorithm name. Protecting one visit and protecting all visits by one person imply different neighboring datasets; more training steps also change accumulated information. Differential privacy constrains a release distribution, while governance manages access to raw records, retention and authorization changes. These act at different positions in a workflow and can support each other. Naming their actual protected objects makes implementation more concrete than treating anonymization, encryption and private training as interchangeable labels.

## 9. Learning together while records remain distributed

Typing histories on phones, hospital images and factory sensor records naturally reside in different places. FedAvg, described by McMahan and colleagues in 2017, organizes learning into communication rounds. A server distributes the current parameters, clients update on their local records for several steps, and returned parameters are averaged with sample-count weights. More local work can reduce communication for a given amount of progress. When clients have different data, however, it can also carry them farther toward different local objectives before the next aggregation.

$$
\theta^{(r+1)}=\sum_{k=1}^K\frac{n_k}{\sum_{j=1}^K n_j}\,\theta_k^{(r,E)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/397338c685aa99b36ec9a948.svg) | Communication round, client count and client summation indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/c5b6a59ed4dd1d73983aa22d.svg) | Client-k sample count and local gradient-step count per round. |
| ![Formula](https://ml-biomat.com/static/agent-math/c5f24bbc7db331cc86546496.svg) | Aggregated parameter vector and client vector after E steps from a common start; parameters retain their model-specific units. |

Equal-size clients returning(1,0) and(3,2) aggregate to (2,1). With one full-batch step, a shared learning rate and sample-size weights, local gradients average to the pooled gradient. Multiple steps evaluate later gradients at different client positions.

Our two clients each have 100 records. The first has inputs centered near −2 and an additional outcome offset of −1; the second has inputs centered near 2 and offset+1. Both fit straight lines, but their preferred parameters differ. The experiment compares one, five and twenty local steps per round over forty communication rounds. The horizontal axis deliberately counts communication: twenty-step rounds perform more gradient work than one-step rounds. Pooled least squares supplies a common optimization target against which the different trajectories can be understood.

With one local full-batch step, sample-weighted gradients equal the pooled gradient. The measured maximum parameter difference is about 4.4×10⁻¹⁶, at floating-point rounding scale. After forty rounds, pooled-data MSE is approximately 0.19923, close to the pooled optimum; twenty local steps give about 0.21753 in this heterogeneous example. The optimal pooled slope, approximately 2.452, also merits interpretation. The generating coefficient of input is 2, but the group offset is correlated with input location. A pooled line without a group indicator absorbs some between-group difference into its slope. The fitted optimization parameter and the generating conditional coefficient therefore refer to different models.

Keeping raw records local changes how data are collected, while transmitted updates can still carry information about those records. Secure aggregation hides individual updates within a protocol so the server observes an aggregate; differential privacy constrains output sensitivity to neighboring data. They can be combined, with their protected objects and participant assumptions stated separately. This chapter simulates two clients in one process to expose the update calculation and client drift. A distributed deployment additionally needs to handle dropout, compression, participation rates and model-version synchronization, which determine what data actually contribute to each round.

The complete script produces all five original experiment figure groups, fixed partitions, model weights and numerical summaries. Follow the information flow when reading it: fitting uses training records, temperature uses tuning records, and the set threshold uses conformal records. Shift evaluation reuses fixed fitted components. Each defense receives attacks generated against its own parameters. Privacy and federation use separate public synthetic inputs. Making these relationships executable preserves both the practical role of a prediction and the actual meaning of each reported measurement.

### Complete CPU experiments from calibration to federated optimization

Generates every original experiment figure, fixed data splits, model weights and numerical summaries. Public digits and synthetic data are separate; privacy plots simulate noise using a public seed.

```
"""Reliability experiments with separate fit, temperature, conformal and test sets."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.ndimage import rotate
from scipy.special import softmax
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss,roc_auc_score
import torch
from torch import nn
from torch.nn import functional as F
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def bins(prob,y):
 conf=prob.max(1);correct=prob.argmax(1)==y;edges=np.linspace(0,1,11);rows=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  mask=(conf>=lo)&(conf<(hi if hi<1 else hi+1e-9));n=int(mask.sum())
  if n:rows.append({'n':n,'confidence':float(conf[mask].mean()),'accuracy':float(correct[mask].mean())})
 return rows,float(sum(r['n']*abs(r['confidence']-r['accuracy']) for r in rows)/len(y))
class Classifier(nn.Module):
 def __init__(self):super().__init__();self.net=nn.Sequential(nn.Linear(64,48),nn.ReLU(),nn.Linear(48,10))
 def forward(self,x):return self.net(x)
def fgsm(model,x,y,epsilon):
 xx=x.clone().detach().requires_grad_(True);loss=F.cross_entropy(model(xx),y);g=torch.autograd.grad(loss,xx)[0];return (xx+epsilon*g.sign()).clamp(0,1).detach()
def train_classifier(x,y,adversarial=False):
 torch.manual_seed(39);m=Classifier();opt=torch.optim.Adam(m.parameters(),lr=.005)
 for epoch in range(30):
  order=torch.randperm(len(x))
  for ids in order.split(128):
   xx=x[ids];yy=y[ids];loss=F.cross_entropy(m(xx),yy)
   if adversarial:adv=fgsm(m,xx,yy,.1);loss=.5*(loss+F.cross_entropy(m(adv),yy))
   opt.zero_grad();loss.backward();opt.step()
 m.eval();return m
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);z=language=='zh';L=lambda a,b:a if z else b;rng=np.random.default_rng(39);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if z else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 # Five independently initialized/bootstrap heteroscedastic Gaussian regressors.
 rx=rng.uniform(-3,3,100);true_sd=.1+.12*abs(rx);ry=np.sin(1.5*rx)+rng.normal(size=100)*true_sd;grid=np.linspace(-5,5,240);means=[];vars=[]
 for seed in range(5):
  torch.manual_seed(390+seed);model=nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2));opt=torch.optim.Adam(model.parameters(),lr=.01);ii=np.random.default_rng(seed).choice(100,100,replace=True);xx=torch.tensor(rx[ii,None],dtype=torch.float32);yy=torch.tensor(ry[ii],dtype=torch.float32)
  for _ in range(350):mu,lv=model(xx).unbind(1);lv=lv.clamp(-6,2);loss=.5*((yy-mu).square()*torch.exp(-lv)+lv).mean();opt.zero_grad();loss.backward();opt.step()
  with torch.no_grad():a=model(torch.tensor(grid[:,None],dtype=torch.float32));means.append(a[:,0].numpy());vars.append(torch.exp(a[:,1].clamp(-6,2)).numpy())
  torch.save(model.state_dict(),out/f'uncertainty-model-{seed}.pt')
 means=np.array(means);vars=np.array(vars);mean=means.mean(0);alea=vars.mean(0);epis=means.var(0);total=alea+epis
 fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained');axs[0].fill_between(grid,mean-1.96*np.sqrt(total),mean+1.96*np.sqrt(total),color='#d2e6ec',label=L('均值±1.96总标准差','Mean ±1.96 total SD'));axs[0].plot(grid,mean,color='#247b94',label=L('集成均值','Ensemble mean'));axs[0].plot(grid,np.sin(1.5*grid),'--',color='#d97b36',label=L('生成均值','Generating mean'));axs[0].scatter(rx,ry,s=14,color='#293f4c',alpha=.6);axs[0].set(xlabel='x',ylabel='y',title=L('100训练点；训练范围[-3,3]','100 training points; training range[-3,3]'));axs[0].legend(fontsize=8)
 axs[1].plot(grid,alea,label=L('平均预测噪声方差','Mean predicted noise variance'));axs[1].plot(grid,epis,label=L('模型均值方差','Variance of model means'));axs[1].plot(grid,(.1+.12*abs(grid))**2,':',label=L('已知生成噪声方差','Known generating noise variance'));axs[1].set(xlabel='x',ylabel=L('y单位平方','Squared y units'));axs[1].legend(fontsize=8)
 for ax in axs:
  for edge in [-3,3]:ax.axvline(edge,color='#8399a5',ls=':')
 save(fig,'uncertainty')
 data=load_digits();X=data.data/16;y=data.target;ids=np.arange(len(y));train,rest=train_test_split(ids,train_size=900,random_state=39);cal,test=train_test_split(rest,train_size=300,random_state=39);tune,conf=train_test_split(cal,train_size=150,random_state=39);tx=torch.tensor(X[train],dtype=torch.float32);ty=torch.tensor(y[train]);testx=torch.tensor(X[test],dtype=torch.float32);testy=torch.tensor(y[test]);model=train_classifier(tx,ty)
 # Explicitly sharpen by2.5 to create a controlled overconfidence example.
 all_logits=model(torch.tensor(X,dtype=torch.float32)).detach()*2.5;logT=torch.tensor(0.,requires_grad=True);opt=torch.optim.LBFGS([logT],lr=.2,max_iter=80,line_search_fn='strong_wolfe');tune_y=torch.tensor(y[tune])
 def closure():opt.zero_grad();loss=F.cross_entropy(all_logits[tune]/logT.exp(),tune_y);loss.backward();return loss
 opt.step(closure);temperature=float(logT.exp().detach());raw=softmax(all_logits[test].numpy(),axis=1);prob=softmax(all_logits[test].numpy()/temperature,axis=1);cp=softmax(all_logits[conf].numpy()/temperature,axis=1);alpha=.1;k=int(np.ceil((len(conf)+1)*(1-alpha)));scores=1-cp[np.arange(len(conf)),y[conf]];q=float(np.sort(scores)[k-1]);sets=prob>=1-q;coverage=float(sets[np.arange(len(test)),y[test]].mean());setsize=float(sets.sum(1).mean());rawbins,rawece=bins(raw,y[test]);calbins,calece=bins(prob,y[test]);selection=[]
 for threshold in [.5,.7,.9,.95,.99]:
  accept=prob.max(1)>=threshold;selection.append({'threshold':threshold,'retained':int(accept.sum()),'fraction':float(accept.mean()),'error':float(np.mean(prob[accept].argmax(1)!=y[test][accept])) if accept.any() else None})
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained');axs[0].plot([0,1],[0,1],':',color='#8d9da6')
 for name,rows,c in [(L('原始分数×2.5','Raw logits×2.5'),rawbins,'#d97b36'),(L('温度校准','Temperature'),calbins,'#247b94')]:axs[0].plot([r['confidence'] for r in rows],[r['accuracy'] for r in rows],'o-',label=name,color=c)
 axs[0].set(xlabel=L('分箱平均最大概率','Mean maximum probability in bin'),ylabel=L('该箱分类正确率','Classification accuracy in bin'),title=L('10个等宽置信箱','10 equal-width confidence bins'));axs[0].legend(fontsize=8);axs[1].hist(raw.max(1),bins=np.linspace(0,1,11),alpha=.5,color='#d97b36',label=L('原始分数×2.5','Raw logits×2.5'));axs[1].hist(prob.max(1),bins=np.linspace(0,1,11),alpha=.5,color='#247b94',label=L('温度校准','Temperature'));axs[1].set(xlabel=L('最大预测概率','Maximum predicted probability'),ylabel=L('测试对象数','Test records'));axs[1].legend(fontsize=8);axs[2].plot([a['fraction'] for a in selection],[a['error'] for a in selection],'o-',color='#247b94')
 for a in selection:axs[2].annotate(str(a['threshold']),(a['fraction'],a['error']),xytext=(3,3),textcoords='offset points')
 axs[2].set(xlabel=L('保留预测比例','Fraction retained'),ylabel=L('保留对象中的错误率','Error among retained records'),title=L('阈值改变工作量与错误','Threshold changes workload and errors'));save(fig,'calibration')
 shifted=np.array([rotate(im,30,reshape=False,order=1,mode='constant',cval=0) for im in data.images[test]/16]);shiftx=torch.tensor(shifted.reshape(-1,64),dtype=torch.float32);sp=softmax(model(shiftx).detach().numpy()*2.5/temperature,axis=1);ssets=sp>=1-q;shiftcover=float(ssets[np.arange(len(test)),y[test]].mean());shiftacc=float(np.mean(sp.argmax(1)==y[test]));oodauc=float(roc_auc_score(np.r_[np.zeros(len(test)),np.ones(len(test))],np.r_[1-prob.max(1),1-sp.max(1)]));groups={};ink_cut=float(np.median(X[train].mean(1)))
 for g,mask in [('Lower ink',X[test].mean(1)<ink_cut),('Higher ink',X[test].mean(1)>=ink_cut)]:groups[g]={'n':int(mask.sum()),'accuracy':float(np.mean(prob[mask].argmax(1)==y[test][mask])),'coverage':float(sets[mask][np.arange(mask.sum()),y[test][mask]].mean()),'mean_set_size':float(sets[mask].sum(1).mean())}
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].bar([L('原图','Original'),L('旋转30°','Rotated30°')],[coverage,shiftcover],color=['#247b94','#d97b36']);axs[0].axhline(.9,ls='--',color='#263c49');axs[0].set(ylim=(0,1),ylabel=L('真实标签落入集合的比例','Fraction of true labels in prediction set'),title=L('同一共形阈值','Same conformal threshold'));axs[1].hist(sets.sum(1),bins=np.arange(-.5,2.5),alpha=.6,color='#247b94',label=L('原图','Original'));axs[1].hist(ssets.sum(1),bins=np.arange(-.5,2.5),alpha=.6,color='#d97b36',label=L('旋转30°','Rotated30°'));axs[1].set(xlabel=L('集合类别数','Prediction-set size'),ylabel=L('测试对象数','Test records'),xticks=[0,1],xlim=(-.5,1.5));axs[1].legend(fontsize=8);ix=np.arange(2);axs[2].bar(ix-.16,[g['accuracy'] for g in groups.values()],width=.3,label=L('准确率','Accuracy'));axs[2].bar(ix+.16,[g['coverage'] for g in groups.values()],width=.3,label=L('覆盖率','Coverage'));axs[2].set(xticks=ix,xticklabels=[f'{L("较少墨迹" if k=="Lower ink" else "较多墨迹",k)}\nn={v["n"]}' for k,v in groups.items()],ylim=(0,1),title=L('按训练亮度阈值分组','Groups from a training-set ink threshold'));axs[2].legend(fontsize=8);save(fig,'coverage_shift')
 # Separate trained models and fresh white-box attacks for each defense.
 robust=train_classifier(tx,ty,adversarial=True);poison_labels=ty.clone();pi=rng.choice(900,90,replace=False);poison_labels[pi]=(poison_labels[pi]+1)%10;poison=train_classifier(tx,poison_labels);attacks={};adversarial_examples={}
 for name,net in [('Standard',model),('Adversarial training',robust)]:
  vals=[]
  for eps in [0,.05,.1,.2]:
   adv=fgsm(net,testx,testy,eps);vals.append(float((net(adv).argmax(1)==testy).float().mean()));
   if eps==.1:adversarial_examples[name]=adv
  attacks[name]=vals
 changed=np.flatnonzero((model(testx).argmax(1)==testy).detach().numpy()&(model(adversarial_examples['Standard']).argmax(1)!=testy).detach().numpy());pick=int(changed[0]);original=testx[pick].reshape(8,8).numpy();adv=adversarial_examples['Standard'][pick].reshape(8,8).numpy();fig=plt.figure(figsize=(13,5),layout='constrained');gs=fig.add_gridspec(2,4,width_ratios=[1,1,1,2]);axs=[fig.add_subplot(gs[:,i]) for i in range(4)];titles=[L(f'原图：真实{int(testy[pick])}，预测{int(model(testx[pick:pick+1]).argmax(1)[0])}',f'Original: true {int(testy[pick])}, predicted {int(model(testx[pick:pick+1]).argmax(1)[0])}'),L(f'FGSM ε=0.1：预测{int(model(adversarial_examples["Standard"][pick:pick+1]).argmax(1)[0])}',f'FGSM ε=0.1: predicted {int(model(adversarial_examples["Standard"][pick:pick+1]).argmax(1)[0])}'),L('像素变化（真实尺度）','Pixel change (actual scale)')]
 for ax,arr,title,cmap in zip(axs[:3],[original,adv,adv-original],titles,['gray','gray','coolwarm']):im=ax.imshow(arr,cmap=cmap,vmin=-.1 if cmap=='coolwarm' else 0,vmax=.1 if cmap=='coolwarm' else 1);ax.set_title(title,fontsize=10);ax.set_xticks([]);ax.set_yticks([]);fig.colorbar(im,ax=ax,shrink=.55)
 for name,vals in attacks.items():axs[3].plot([0,.05,.1,.2],vals,'o-',label=L('标准训练' if name=='Standard' else '对抗训练',name))
 axs[3].set(xlabel=L('L∞扰动上限','L∞ perturbation budget'),ylabel=L('相应模型的FGSM准确率','FGSM accuracy for the attacked model'),ylim=(0,1));axs[3].legend(fontsize=8);save(fig,'robustness')
 # Public synthetic-data simulation of Laplace accuracy; fixed seed is for the teaching plot.
 bounded=rng.uniform(0,1,100);sensitivity=.01;epsilons=np.array([.1,.2,.5,1.]);dp=[];noises=[]
 for eps in epsilons:
  noise=rng.laplace(0,sensitivity/eps,10000);noises.append(noise);dp.append({'epsilon':float(eps),'scale':float(sensitivity/eps),'theoretical_rmse':float(np.sqrt(2)*sensitivity/eps),'empirical_rmse':float(np.sqrt(np.mean(noise**2)))})
 # Federated full-batch linear regression, two equally sized heterogeneous clients.
 clients=[]
 for center,offset in [(-2.,-1.),(2.,1.)]:
  cx=rng.normal(center,.8,100);cy=2*cx+offset+rng.normal(0,.2,100);clients.append((np.c_[cx,np.ones(100)],cy))
 FX=np.vstack([a for a,b in clients]);FY=np.concatenate([b for a,b in clients]);optimal=np.linalg.lstsq(FX,FY,rcond=None)[0];fed={};fweights={};lr=.03
 for steps in [1,5,20]:
  w=np.zeros(2);trace=[]
  for _ in range(40):
   local=[]
   for cx,cy in clients:
    v=w.copy()
    for _ in range(steps):v-=lr*2*cx.T@(cx@v-cy)/len(cy)
    local.append(v)
   w=np.mean(local,axis=0);trace.append(float(np.mean((FX@w-FY)**2)))
  fed[str(steps)]=trace;fweights[str(steps)]=w.tolist()
 central=np.zeros(2)
 for _ in range(40):central-=lr*2*FX.T@(FX@central-FY)/len(FY)
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');axs[0].hist(noises[0],bins=70,density=True,alpha=.5,label='ε=0.1');axs[0].hist(noises[2],bins=70,density=True,alpha=.6,label='ε=0.5');axs[0].set(xlabel=L('发布均值减去原均值','Released mean minus original mean'),ylabel=L('密度','Density'),title=L('公开模拟；每条件10000次噪声','Public simulation;10,000 noise draws each'));axs[0].legend();axs[1].plot(epsilons,[d['theoretical_rmse'] for d in dp],'o-',label=L('理论RMSE','Theoretical RMSE'));axs[1].plot(epsilons,[d['empirical_rmse'] for d in dp],'x',label=L('模拟RMSE','Simulated RMSE'));axs[1].set(xlabel='ε',ylabel=L('均值单位的RMSE','RMSE in mean units'));axs[1].legend(fontsize=8)
 for steps,trace in fed.items():axs[2].plot(range(1,41),trace,label=f'{L("本地步数","Local steps")}={steps}')
 axs[2].axhline(np.mean((FX@optimal-FY)**2),color='#8299a5',ls=':',label=L('合并数据最小二乘','Pooled least-squares optimum'));axs[2].set(xlabel=L('通信轮数','Communication round'),ylabel=L('全体数据MSE','Pooled-data MSE'),yscale='log');axs[2].legend(fontsize=7);save(fig,'privacy_federation')
 acc=float(np.mean(prob.argmax(1)==y[test]));summary={'n_total':len(y),'n_train':len(train),'n_temperature':len(tune),'n_conformal':len(conf),'n_test':len(test),'split_intersection':sum(len(set(a)&set(b)) for i,a in enumerate([train,tune,conf,test]) for b in [train,tune,conf,test][i+1:]),'temperature':temperature,'sharpening_factor':2.5,'accuracy':acc,'raw_nll':float(log_loss(y[test],raw)),'temperature_nll':float(log_loss(y[test],prob)),'raw_ece':rawece,'temperature_ece':calece,'argmax_change_count':int(np.sum(raw.argmax(1)!=prob.argmax(1))),'conformal_rank':k,'conformal_threshold':q,'coverage':coverage,'mean_set_size':setsize,'empty_set_count':int(np.sum(sets.sum(1)==0)),'shift_accuracy':shiftacc,'shift_coverage':shiftcover,'shift_mean_set_size':float(ssets.sum(1).mean()),'ood_uncertainty_auroc':oodauc,'groups':groups,'selection':selection,'attacks':attacks,'poison_count':len(pi),'poison_clean_accuracy':float((poison(testx).argmax(1)==testy).float().mean()),'attack_max_linf':float(torch.max(abs(adversarial_examples['Standard']-testx))),'laplace_sensitivity':sensitivity,'privacy_accuracy':dp,'basic_two_release_epsilon':1.,'basic_two_release_delta':0.,'fedavg_E1_centralized_max_error':float(np.max(abs(np.array(fweights['1'])-central))),'fed_weights':fweights,'pooled_optimal_weights':optimal.tolist(),'pooled_optimal_mse':float(np.mean((FX@optimal-FY)**2)),'fed_final_mse':{k:v[-1] for k,v in fed.items()},'uncertainty_at_zero':{'aleatoric':float(alea[np.argmin(abs(grid))]),'epistemic':float(epis[np.argmin(abs(grid))])},'uncertainty_at_four':{'aleatoric':float(alea[np.argmin(abs(grid-4))]),'epistemic':float(epis[np.argmin(abs(grid-4))])}}
 for name,net in [('standard',model),('adversarial',robust),('poisoned',poison)]:torch.save(net.state_dict(),out/f'{name}-classifier.pt')
 np.savez_compressed(out/'experiment_data.npz',train_indices=train,temperature_indices=tune,conformal_indices=conf,test_indices=test,raw_probabilities=raw,calibrated_probabilities=prob,conformal_scores=scores,prediction_sets=sets,shifted_images=shifted,shifted_probabilities=sp,test_labels=y[test],regression_x=rx,regression_y=ry,regression_grid=grid,ensemble_means=means,ensemble_variances=vars,adversarial_example=adv,original_example=original,poison_indices=pi,client_X=FX,client_y=FY);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M39.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Guo et al. (2017), On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)

   Temperature scaling and calibration.

   Primary technical reference; linked, not reproduced
2. [Angelopoulos & Bates, A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511)

   Finite-sample sets, ranks and coverage conditions.

   Primary technical reference; linked, not reproduced
3. [Kendall & Gal (2017), What Uncertainties Do We Need in Bayesian Deep Learning?](https://arxiv.org/abs/1703.04977)

   Aleatoric and epistemic uncertainty.

   Primary technical reference; linked, not reproduced
4. [Goodfellow et al., Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572)

   FGSM linearization and adversarial training.

   Primary technical reference; linked, not reproduced
5. [Fairlearn: common fairness metrics](https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html)

   Denominators in demographic parity, equal opportunity and equalized odds.

   Primary technical reference; linked, not reproduced
6. [Dwork & Roth (2014), The Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)

   Laplace mechanisms, sensitivity and composition.

   Primary technical reference; linked, not reproduced
7. [Opacus FAQ](https://opacus.ai/docs/faq)

   Per-example clipping, noise, accounting and secure randomness.

   Primary technical reference; linked, not reproduced
8. [McMahan et al. (2017), Communication-Efficient Learning of Deep Networks from Decentralized Data](https://proceedings.mlr.press/v54/mcmahan17a.html)

   FedAvg local updates and communication.

   Primary technical reference; linked, not reproduced
9. [scikit-learn: Probability calibration curves](https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html)

   SVC and two calibration methods in the reproduced figure.

   BSD-3-Clause; original figure reused
10. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    Digit data and original task.

    CC BY 4.0; digit data
