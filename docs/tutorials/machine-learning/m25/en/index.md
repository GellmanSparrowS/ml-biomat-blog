# Understand how a model decides: explanations, attribution and internal mechanisms

Source: https://ml-biomat.com/tutorials/machine-learning/m25/en/
Language: en

Start with readable models, then inspect replacement, backgrounds, gradients and internal interventions—each tied to a specific question.

## What do we want to know after a correct prediction?

A camera recognizes a handwritten digit as three. We may still want to know whether it used the right-hand curves or an accidental bright patch in the background. A demand model predicts a high value; perhaps one input raised its prediction, or perhaps two nearly identical features share the same predictive information. Interpretability starts with questions like these. It can help researchers understand a fitted model, uncover processing errors, examine application requirements and identify useful follow-up measurements. Its value comes from the particular question an explanation helps answer.

Different questions need different explanations. Global explanations summarize behavior across a population; local explanations describe a particular prediction relative to a reference. Input attribution allocates output differences, while internal analysis examines neurons, representations and computational paths. An importance ranking does not identify the reason for every individual prediction, and one local heatmap does not summarize an entire system. We first specify the model, output scale, reference and intended use, then choose an appropriate calculation. This keeps an attractive graphic attached to a clear scientific object.

Two actual models support the chapter: one reads three correlated tabular features, and another recognizes eight-by-eight-pixel handwritten digits. The tabular experiment exposes replacement, averaging and contribution allocation. The image experiment exposes gradients, path integrals, channel responses and changes after occlusion. Every visualization follows a defined operation. Predictive relationships inside a model and interventions in the world require different evidence; a question about changing a real condition connects these analyses to causal design and suitable observations.

## Begin with a structure that can be read directly

A linear model multiplies each feature by a coefficient and adds the results. Holding other inputs fixed, its coefficient gives the prediction change associated with a one-unit change in that feature. Interpretation therefore carries the feature's units, transformation and relationships with other inputs. After standardization, one unit means one standard deviation. A log-transformed feature needs interpretation on its transformed scale. Two almost identical inputs may divide the same predictive information between their coefficients. A simple mathematical structure remains informative when the representation is included in the explanation.

A shallow decision tree can be followed as a small sequence of threshold decisions. As the tree grows, a single path may remain readable even though the complete rule system becomes difficult to inspect. A generalized additive model, GAM, assigns each feature a potentially curved response and adds these responses, retaining a component-wise structure while representing nonlinearity. When two features produce an additional joint effect, that interaction must be included explicitly. Otherwise the additive restriction leaves part of the relationship unmodeled, even when each individual curve is flexible.

$$
\widehat y=\beta_0+\sum_{j=1}^p f_j(x_j)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/84b54b809e5e61516ae65a79.svg) | Predicted outcome and intercept; outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/b6f63c98dba7f777ad1c41c8.svg) | Feature index, count, feature value and univariate response; feature-specific input units and outcome-unit function values. |

Linear models use fj=βjxj; additive splines allow curved responses. Intercept 1, f1(2)=4 and f2(3)=9 give 14. A sum alone has no cross-feature products; interactions require additional terms.

The synthetic response contains a linear effect of the first feature, a squared effect of the second, and their product. The third feature nearly copies the first, with correlation approximately 0.996. Using 600 training and 200 test records, RMSE is about 0.947 for a linear model, 0.731 for a shallow tree, 0.678 for additive splines, and 0.271 for a random forest. A boosting model constrained to increase with the first feature reaches 0.211. The generating mechanism is indeed increasing in that feature while others are held fixed, so this constraint matches the constructed problem.

![Left: correlated features and a replacement path outside common combinations. Middle: mean±SD MSE increases over 12 permutations. Right: five model RMSEs with the same 600/200 split.](https://ml-biomat.com/static/tutorials/machine-learning/figures/eea43ce93267fef5762468a3.svg?v=eea43ce93267)

Figure 1Left: correlated features and a replacement path outside common combinations. Middle: mean±SD MSE increases over 12 permutations. Right: five model RMSEs with the same 600/200 split.

Monotonic constraints specify a direction, sparsity reduces the number of used variables, and shape constraints can encode requirements such as convexity or saturation. They place domain knowledge directly into the set of functions a model can represent. Readability and predictive quality still need joint examination. An omitted interaction can yield a clear explanation and systematic prediction error at the same time. Comparing models on the task makes the trade-off concrete: choose enough expressive capacity to represent the required relationships while retaining as much inspectable structure as the application permits.

## Shuffle a column, or move along its values

Permutation importance measures the original test error, shuffles a feature column to disrupt its alignment with outcomes and other features, and measures the increase. The fitted model stays unchanged. Our experiment repeats each permutation twelve times and reports the mean and standard deviation. Shuffling the first feature alone increases MSE by about 3.760; shuffling its correlated copy increases it by 0.492. Shuffling both together using the same row permutation increases MSE by 6.693. Separate and joint disruption remove different information, so their measured effects need not add.

$$
I_j=\frac1n\sum_{i=1}^n\left[\ell(y_i,f(x_{i,-j},x_{\pi(i),j}))-\ell(y_i,f(x_i))\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3dc5dc5364d523cf7d193d6a.svg) | Record index, feature index, test count and random row permutation. |
| ![Formula](https://ml-biomat.com/static/agent-math/b17901c71506b5271de88ca7.svg) | Original input, other features, permuted feature value, observed outcome and fixed fitted predictor. |
| ![Formula](https://ml-biomat.com/static/agent-math/f5298f54aa4c0df5bf3005a6.svg) | Loss and mean loss increase; squared outcome units for MSE. |

Original MSE 0.2 and permuted MSE 0.7 give importance 0.5. The model is not refitted. Joint permutation preserves within-group relationships using the same row order. The plot reports 12 repetitions.

Partial dependence, PDP, replaces a selected feature with each value on a grid for every evaluation record and averages the predictions. Individual conditional expectation, ICE, keeps each record's curve instead of averaging. The mean summarizes a population-level pattern, while the separate curves reveal whether different backgrounds have similar responses. Here the second feature changes the effect of the first through an interaction, so ICE curves vary. Their differences motivate a closer look at interactions rather than assigning the same average response to every object.

$$
\operatorname{ICE}_i(z)=f(z,x_{i,-j}),\qquad\operatorname{PDP}_j(z)=\frac1n\sum_{i=1}^n\operatorname{ICE}_i(z)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/800926673aeb9732053f2892.svg) | Record index, selected feature, sample count, replacement value and remaining fixed features. |
| ![Formula](https://ml-biomat.com/static/agent-math/c6cd6629068802ef2c19ba9d.svg) | Model, individual curve and average curve; predicted-outcome units. |

Replace then predict. Three predictions 2,4,9 at a grid value give PDP 5, while ICE retains the differences. Replacement can depart from common combinations when inputs are correlated.

![Left:30 ICE curves and PDP over 200 test records. Right: PDP and ten-bin ALE with their stated centering. Vertical values summarize model predictions and centered changes.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5f103ec0770af436bdc6d9a4.svg?v=5f103ec0770a)

Figure 2Left:30 ICE curves and PDP over 200 test records. Right: PDP and ten-bin ALE with their stated centering. Vertical values summarize model predictions and centered changes.

Strong correlation creates a concrete replacement problem. Training records have nearly equal first and third features, while PDP can set the first very high and leave the third low, producing unusual combinations. Accumulated local effects, ALE, instead forms intervals, computes endpoint prediction differences only for records originally in each interval, then accumulates and centers the differences. The code uses ten quantile bins. This reduces distant replacements in the joint distribution. Sparse intervals, coarse bins and complex interactions still affect the resulting summary, so the curve should be read together with the observed feature distribution.

## Explain one prediction with a nearby simple model

The 2016 LIME work organized local explanation into an accessible procedure: generate examples near a target, query the original model, and fit a simple model that emphasizes nearby behavior. A small flat board on curved terrain offers an analogy. Close to its center, the board describes a local slope; over a larger area, distant rises and depressions influence its placement. Neighborhood generation, feasible perturbations, distance weights and surrogate complexity all determine the resulting explanation. These choices define which aspect of the fitted model the local approximation represents.

$$
\widehat g=\arg\min_{g(z)=\beta_0+\beta^\mathsf Tz}\sum_{i=1}^m w_i[f(z_i)-g(z_i)]^2+\lambda\|\beta\|_2^2,\quad w_i=\exp\!\left(-\frac{\|z_i-x\|_2^2}{2h^2}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0755ee100528064ed2d0b6e8.svg) | Target three-vector, perturbed input, perturbation count and neighborhood width; dimensionless inputs here. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b26922014466083f7794284.svg) | Original predictor, local linear surrogate, intercept and three slopes; outputs in outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/c34d4f71d9fb2cd0d844aa97.svg) | Distance weight, nonnegative penalty coefficient, Euclidean norm and minimizer. |

Distance zero receives weight 1; distance h receives e^-1/2≈0.607. The code uses 600 perturbations, h=0.2 or h=0.8 and λ=0.01, comparing fit and coefficients across five seeds.

For one forest prediction, the code fits weighted linear surrogates to 600 independent Gaussian perturbations, comparing neighborhood widths 0.2 and 0.8 over five seeds each. The forest predicts approximately −1.664 at the target. Narrow-neighborhood surrogates predict about −1.54 to −1.55 there, while wider-neighborhood fits predict −0.97 to −1.00. Weighted fit scores range from approximately 0.836 to 0.863 for the narrower neighborhoods and 0.798 to 0.807 for the wider ones. Reporting these values beside the coefficients makes the quality of the approximation inspectable.

Independent perturbations also break the strong relationship between the first and third features. The resulting surrogate consequently describes that particular perturbation neighborhood. Data with strict feasible combinations may call for constrained sampling, conditional generative models or explanation of meaningful feature groups. A local slope measures a rate of change. Converting it into a contribution additionally requires a starting point and a specified change. Keeping these objects distinct avoids treating a fitted coefficient as an already-defined allocation of the entire prediction.

## Allocate a prediction difference after choosing its reference

Shapley values originate in cooperative allocation: several participants produce a joint payoff, and a rule distributes their contributions. For model explanation, features become participants. Each feature's marginal change in prediction is averaged over all orders in which features could enter. Interactions can therefore be shared among their participants. Before calculating, define how absent features are filled and what prediction corresponds to the empty set. Different definitions create different allocation problems, even when the model and the explained input remain fixed.

$$
\phi_j=\sum_{S\subseteq F\setminus\{j\}}\frac{|S|!(p-|S|-1)!}{p!}[v(S\cup\{j\})-v(S)],\qquad v(\varnothing)+\sum_{j=1}^{p}\phi_j=f(x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c2050a20f8e050868e23ea7a.svg) | Full feature set, feature count, target feature, preceding subset, subset size and factorial. |
| ![Formula](https://ml-biomat.com/static/agent-math/81e802bf30a81f3d8c26bb91.svg) | Mean output with S fixed and other features filled from the selected background, empty-set reference and target prediction; outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b14779b70d4b2a8a3695f4f.svg) | Allocated contribution, union, set removal and subset relation; contribution has output units. |

Weights count the proportion of feature orders with a given preceding subset. For f=x1+2x2+x1x2, from(0,0) to (2,3), x1 contributes 2 or 8, averaging 5; x2 contributes 6 or 12, averaging 9; total 14.

## Two feature orders allocate the same interaction

Disclosed model f(x)=x₁+2x₂+x₁x₂. x is the target and b the reference. Paths add x₁ or x₂ first; Shapley values average the resulting increments.

[Figure: Two feature orders and their contributions](https://ml-biomat.com/tutorials/machine-learning/m25/en/#M25-plot)

The interaction uses a fully disclosed two-feature function. At input (2,3) relative to baseline (0,0), its prediction is fourteen and the two Shapley contributions are five and nine. The product term of six is shared through averaging the two possible feature orders. Changing the baseline to (1,1) gives reference prediction four. The same output fourteen now differs from its reference by ten, allocated as three and seven. Neither the model nor the target has changed; the comparison has. A larger contribution in one comparison therefore does not define universal importance across populations.

![Left: exact three-feature Shapley accumulation with 80 background records. Middle:30 test-record contributions colored by feature values. Right: local-slope mean±SD over five seeds at two widths.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6babf5da38c423c0e91233ae.svg?v=6babf5da38c4)

Figure 3Left: exact three-feature Shapley accumulation with 80 background records. Middle:30 test-record contributions colored by feature values. Right: local-slope mean±SD over five seeds at two widths.

The forest experiment enumerates all eight subsets of three features and fills missing features with 80 training background records. For one test record, the background prediction is approximately 0.380 and the contributions are −1.368, −0.287 and −0.389, summing to the predicted −1.664. Restricting the background to training records with a positive first feature raises the reference to 2.118 and changes the allocations. Exactness refers to this fitted model, finite background and coalition definition. Unreplaced background features retain their relationships with each other, while replacement breaks dependence between fixed and remaining features.

![SHAP beeswarm with feature rows, horizontal contributions and feature-value colors.](https://ml-biomat.com/static/tutorials/machine-learning/figures/0fcd149c9226bcf9c4a73868.png?v=0fcd149c9226)

Figure 4Original SHAP Adult/XGBoost beeswarm; horizontal contributions use default raw log-odds, color encodes feature value. Scott Lundberg and SHAP contributors, MIT, unmodified.

The original SHAP beeswarm shows an efficient reading convention: one feature per row, one object per dot, horizontal position for contribution, color for feature value, and piling for density. The selected Adult/XGBoost example explains raw binary-classification margins, or log-odds, under the default output choice. Its horizontal values are not probability-point changes. Our three-feature regression experiment instead uses outcome units. Conditional-background allocations can also distribute information differently among correlated features, including information carried by a column the model does not directly use. Background and output scale belong in the explanation itself.

## Does a bright pixel indicate sensitivity or contribution?

Image attribution begins by choosing a scalar output. Here it is the classifier's digit-three logit. Saliency differentiates that output with respect to each pixel, describing the effect of an infinitesimal change at the current image. Taking absolute values retains sensitivity magnitude and discards direction. A small gradient can also occur in a saturated region of a nonlinear model. The local slope at the endpoint and the accumulated change from a reference image are therefore different questions, motivating methods that inspect more than one position along an input path.

$$
S_j(x)=\frac{\partial f_c(x)}{\partial x_j}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/116d3ff8ca8fc9844612c124.svg) | 64-dimensional normalized pixel input, pixel index and target class. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff7ec1afdc831fd8806819cc.svg) | Target logit, local gradient and partial derivative; logit per normalized-intensity unit. |

Gradient 2 means a sufficiently small pixel increase 0.01 gives approximately 0.02 logit change, holding other pixels fixed. Displaying |S| removes sign, so the plot labels this choice.

Integrated Gradients follows a path between a reference image and the observed image, integrates gradients along that path, and multiplies by each pixel's total change. The 2017 work incorporated properties including sensitivity and implementation invariance into attribution design. Completeness supplies a useful numerical check: summed pixel attributions should match the difference between the two endpoint outputs. A black image, a mean image or a task-specific reference defines a different comparison. Examining the intermediate images also reveals what kind of path the integral is traversing.

$$
\operatorname{IG}_j(x;b)=(x_j-b_j)\int_0^1\frac{\partial f_c(b+\alpha(x-b))}{\partial x_j}\,d\alpha,\qquad\sum_j\operatorname{IG}_j=f_c(x)-f_c(b)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/228d8035641ba5e338c3a919.svg) | 64-dimensional target and baseline images, pixel index and target class; intensity normalized to 0–1. |
| ![Formula](https://ml-biomat.com/static/agent-math/d8e619ffa58db67bebadc631.svg) | Path position 0–1, target logit, pixel attribution, partial derivative and path integral; attribution in logit units. |

The chain rule integrated along the path gives the endpoint difference. For f=2x1+3x2 from zero to (1,2), contributions 2 and 6 sum to 8. The CNN uses 128 midpoint evaluations and reports the numerical discrepancy.

![Same observed digit 3: input, absolute gradient, black-baseline IG, mean-baseline IG and second-layer Grad-CAM before/after its positive-part step. Target: class 3 logit. IG panels share a range; Grad-CAM is scaled to 0–1.](https://ml-biomat.com/static/tutorials/machine-learning/figures/08bc8348de90183d78e64f7c.svg?v=08bc8348de90)

Figure 5Same observed digit 3: input, absolute gradient, black-baseline IG, mean-baseline IG and second-layer Grad-CAM before/after its positive-part step. Target: class 3 logit. IG panels share a range; Grad-CAM is scaled to 0–1.

The small convolutional model trains on 1,257 digit images and achieves approximately 0.963 accuracy on 540 held-out images. For the chosen three, the target logit is about 7.050 and the black-reference logit is −2.817, a difference near 9.868. A 128-point midpoint integral gives attribution sum 9.870, with numerical discrepancy approximately 0.0023. Replacing the reference with the mean training image changes the attribution distribution. The two IG panels share a color range and retain positive and negative contributions. Saliency and Grad-CAM have separately labeled scales, so equal brightness across those panels does not imply equal numerical meaning.

Grad-CAM averages target-output gradients over spatial positions to obtain channel weights, combines the chosen convolutional feature maps using those weights, and keeps the positive part. It provides localization at that layer's resolution. Interpolating a small map to input size changes display resolution, rather than adding new localization information. Our second convolutional layer remains eight by eight, allowing direct display. Input gradients, integrated contributions and feature-map localization operate at different scales; target class, layer, normalization and color meaning identify the quantity each picture represents.

$$
a_k^c=\frac1{HW}\sum_{u=1}^H\sum_{v=1}^W\frac{\partial f_c}{\partial A_{uv}^{k}},\qquad L^c=\operatorname{ReLU}\left(\sum_k a_k^c A^k\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bbf4a4beafe43aaa65bd08ff.svg) | Channel and spatial indices, map height and width; 12 channels and H=W=8 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/796902c1169abecbf44f6ae3.svg) | Channel-k feature map, its location value and target logit. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a2e2166451f4791f36f639a.svg) | Mean-gradient channel weight, localization map, positive part and derivative. The weighted map has logit scale before maximum normalization for display. |

Map values 3 and 2 with mean gradients 0.5 and −0.2 give max(0,1.5−0.4)=1.1. Spatial averaging defines channel weights; this is not a pixel-attribution completeness decomposition.

Standard Grad-CAM happens to be entirely zero for this image, so the figure also shows the signed result before taking the positive part. This network flattens convolutional positions and classifies with different fully connected weights at different locations. Grad-CAM averages those spatial weights into channel weights. Their weighted map is negative everywhere for the selected input, and taking its positive part removes the entire map, while the full model still gives class three a high logit. The paired panels identify the exact computational step where information disappears and clarify the distinction between a localization summary and the complete classifier calculation.

## Move from pixels to concepts and internal representations

People often ask whether a vertical stroke matters, rather than which individual pixel has the largest derivative. The 2018 TCAV work uses concept and comparison examples to fit a separating direction in an internal representation, then differentiates the output along that direction. A concept is defined by the examples supplied, rather than by its name alone. Layer choice, comparison examples and correlated attributes affect what the direction represents. Repeated background sampling and statistical comparisons form part of a broader concept-testing study.

$$
D_{C,c}(x)=\nabla_a f_c(a(x))^\mathsf T v_C,\qquad T_{C,c}=\frac1{|X_c|}\sum_{x\in X_c}\mathbf1\{D_{C,c}(x)>0\}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1a03a158faf24bccc3e775cf.svg) | Flattened chosen-layer activation, 512-dimensional unit concept direction here, and activation gradient. |
| ![Formula](https://ml-biomat.com/static/agent-math/b1800e2eb9f630f21ac87ec4.svg) | Concept contrast, target class, class evaluation set and its size. |
| ![Formula](https://ml-biomat.com/static/agent-math/7cf069fe502feb6e16e478e5.svg) | Directional derivative, positive-derivative fraction and indicator; fraction dimensionless, derivative depends on activation coordinates. |

Derivatives 0.2,−0.1,0.4,0.3 give fraction 3/4. The direction is trained from concept and comparison examples. One direction’s fraction is not a significance test; broader TCAV studies repeat control fitting.

![Top: generated concept-probe inputs, three vertical and three horizontal strokes. Bottom: six training digits with the largest first-layer channel 2 mean activations, labeled with class and activation.](https://ml-biomat.com/static/tutorials/machine-learning/figures/76288f8cab1d4495777ce787.svg?v=76288f8cab1d)

Figure 6Top: generated concept-probe inputs, three vertical and three horizontal strokes. Bottom: six training digits with the largest first-layer channel 2 mean activations, labeled with class and activation.

Our controlled experiment creates 60 noisy vertical-stroke images and 60 noisy horizontal-stroke images. A linear probe on first-convolutional-layer activations separates them, achieving accuracy one on 30 held-out concept examples. On real digit test images, the fraction with a positive target derivative along the vertical-versus-horizontal direction is one for classes one and three, and zero for seven. These numbers describe a direction defined by this controlled contrast. Extending the study to natural handwriting concepts would add varied writing styles, alternative controls, repeated probe fitting and evaluation across examples.

![Four diverse optimized ball-like stimulus images.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6bfaf9eb5121d82f51f687e7.png?v=6bfaf9eb5121)

Figure 7Original Distill image: diversity optimization reveals multiple ball-like appearances for GoogLeNet mixed 5a unit 9. Chris Olah, Alexander Mordvintsev and Ludwig Schubert, Feature Visualization,2017, CC BY 4.0, unmodified.

An optimized feature stimulus can also look surprisingly simple. Channel two's stimulus is almost entirely bright, while its high-activation training examples contain dense strokes. This suggests a concrete investigation of brightness, edges and position before assigning a complex semantic name to the channel. The optimization objective, allowed pixel range and regularization jointly determine what stimulus is found. Stronger smoothness penalties discourage fine texture; diversity terms can seek different inputs with similarly strong responses. Each changed objective can generate another hypothesis to check against actual examples and controlled perturbations, keeping the visualization connected to the network's observed behavior. In the actual training images, mean brightness and channel-two mean activation have correlation approximately 0.986. This numerical comparison strengthens the brightness hypothesis and suggests the next experiment: alter brightness while preserving stroke geometry, then measure the channel response again.

Feature visualization reverses the question: hold the network fixed and modify an input to activate a chosen unit strongly. Distill's 2017 examples show how one channel can respond to several appearances and how a diversity objective reveals facets hidden by one optimized image. We also optimize a genuine eight-by-eight input to maximize the mean activation of first-layer channel two, with pixel bounds, magnitude regularization and neighboring-pixel penalties. The result is a synthesized model stimulus. Actual high-activation training examples alongside it offer a complementary view of the same channel's behavior.

## Make an explanation face an actual change

Mechanistic interpretability asks how information moves through internal computation. Correlation between a neuron and a concept suggests a hypothesis. Zeroing that neuron, replacing an activation with one from another input, or patching a representation can test its role in the model's subsequent calculation. One unit may respond to several structures, while one concept may be spread across many units. Channels, directions, feature groups and small connected circuits can therefore be useful analysis units. Choosing among them requires evidence from both responses and interventions.

![Left: target logit after attribution-ordered or random black replacement in one image. Middle: optimized channel 2 stimulus. Right: positive-derivative fractions for one vertical-versus-horizontal concept direction.](https://ml-biomat.com/static/tutorials/machine-learning/figures/8ac5d6bcf465bb589b863f0c.svg?v=8ac5d6bcf465)

Figure 8Left: target logit after attribution-ordered or random black replacement in one image. Middle: optimized channel 2 stimulus. Right: positive-derivative fractions for one vertical-versus-horizontal concept direction.

Zeroing trained first-layer channel two changes test accuracy from approximately 0.963 to 0.954. Across all test images, the digit-three logit actually rises by an average of about 0.902, showing that the channel has different directional roles for different outputs. A separate check removes pixels from the chosen image in descending absolute IG order, comparing with a fixed random ordering. Removing the first four attributed pixels lowers the target logit from 7.050 to 0.408; the first four random removals leave it unchanged here. As pixels are replaced with black, the images move away from natural digits, defining the particular perturbation this experiment evaluates.

A counterfactual explanation searches for a feasible input change that reaches a desired model output. Consider a score equal to the first feature plus twice the second. Input (1,1) scores three. If the first feature is immutable, reaching threshold five requires raising the second to at least two. The code preserves that immutable coordinate and checks the new score. Applied counterfactuals also need category validity, costs, timing and feature relationships, followed by an assessment of whether the proposed change is actionable. Crossing a model threshold and observing the real-world effect of an action rely on different evidence.

$$
x^*=\arg\min_{x^\prime\in\mathcal F}d(x^\prime,x)\quad\text{subject to}\quad f(x^\prime)\ge t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/05020bbd252fb20e2fd1e79c.svg) | Original input, candidate change and selected change; feature-specific units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f70e518ff66c4f1b7d5b06.svg) | Feasible set including immutable and validity constraints, change cost, fixed predictor, threshold and minimizer. |

For f=x1+2x2, start (1,1), fix x1=1 and permit only increasing x2. Threshold 5 and minimum change in the second coordinate give (1,2), score 5.

Explanation evaluation returns to the intended use. Faithfulness checks whether emphasized components affect the model. Stability compares explanations across nearby inputs, backgrounds and random seeds. Completeness checks attribution sums. Comprehensibility requires evaluation with the people using the explanation. The 2018 saliency sanity-check work highlighted that visually similar edge-like maps can arise from different mechanisms; randomizing model parameters or training labels can test sensitivity to what the model learned. Our repeated neighborhoods, changed backgrounds, integration check and occlusion experiment each address a specific part of that evaluation.

Comparisons between explanation methods should also fix the model version and output coordinate. Probability contributions and logit contributions live on different scales. An explanation using the whole training background and one comparing only high-demand objects use different references. A useful comparison record therefore includes target class, reference samples, perturbation method, random seed and measured approximation error before assessing whether the explanation helps complete its intended task. The person reading the explanation can then trace a disagreement to a specific choice and repeat the calculation. Visual concentration alone supplies much less information about whether the method answered the original question.

### Complete experiment: tabular explanations, CNN attribution, concepts and channel intervention

Run python main.py --output results --language en. Tabular and concept data follow explicit generators; handwriting uses scikit-learn’s bundled UCI Optical Digits data. Outputs include six figure groups, CNN weights, arrays and metrics, with core explanation calculations shown directly.

```
"""Explain actual fitted models through complementary, inspectable calculations."""
from pathlib import Path
import argparse,json,itertools,math
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression,Ridge,LogisticRegression
from sklearn.preprocessing import SplineTransformer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def exact_shap(model,x,background):
 p=len(x);values={}
 for mask in range(1<<p):
  X=background.copy()
  for j in range(p):
   if mask&(1<<j):X[:,j]=x[j]
  values[mask]=float(model.predict(X).mean())
 phi=np.zeros(p)
 for j in range(p):
  for mask in range(1<<p):
   if mask&(1<<j):continue
   k=mask.bit_count();weight=math.factorial(k)*math.factorial(p-k-1)/math.factorial(p);phi[j]+=weight*(values[mask|(1<<j)]-values[mask])
 return phi,values[0],values[(1<<p)-1]
class CNN(nn.Module):
 def __init__(self):super().__init__();self.c1=nn.Conv2d(1,8,3,padding=1);self.c2=nn.Conv2d(8,12,3,padding=1);self.fc=nn.Linear(12*64,10)
 def from_first(self,a):b=F.relu(self.c2(a));return self.fc(b.flatten(1)),b
 def forward(self,x):a=F.relu(self.c1(x));o,b=self.from_first(a);return o,a,b
def ig(model,x,base,target,steps=128):
 # Midpoint quadrature, explicitly retaining the chosen baseline and target logit.
 alphas=(torch.arange(steps,dtype=x.dtype)+.5)/steps;path=(base+alphas[:,None,None,None]*(x-base)).requires_grad_(True);logit=model(path)[0][:,target];g=torch.autograd.grad(logit.sum(),path)[0];return (x-base)*g.mean(0,keepdim=True)
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);z=language=='zh';L=lambda a,b:a if z else b;rng=np.random.default_rng(25);torch.manual_seed(25);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if z else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 X=rng.uniform(-1.5,1.5,(800,3));X[:,2]=X[:,0]+rng.normal(0,.08,800);y=2*X[:,0]+X[:,1]**2+.8*X[:,0]*X[:,1]+rng.normal(0,.15,800);tr,te=train_test_split(np.arange(800),test_size=.25,random_state=25);xt,yt=X[tr],y[tr];xe,ye=X[te],y[te]
 models={'Linear':LinearRegression(),'Tree':DecisionTreeRegressor(max_depth=3,random_state=25),'GAM':make_pipeline(SplineTransformer(n_knots=6,degree=3),Ridge(alpha=1)),'Monotonic':HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=9,monotonic_cst=[1,0,0],random_state=25),'Forest':RandomForestRegressor(n_estimators=120,max_depth=7,min_samples_leaf=4,n_jobs=1,random_state=25)}
 rmse={}
 for k,m in models.items():m.fit(xt,yt);rmse[k]=float(np.sqrt(np.mean((m.predict(xe)-ye)**2)))
 rf=models['Forest'];base_mse=np.mean((rf.predict(xe)-ye)**2);perm=[]
 for cols in [[0],[1],[2],[0,2]]:
  reps=[]
  for _ in range(12):xx=xe.copy();order=rng.permutation(len(xx));xx[:,cols]=xx[order][:,cols];reps.append(float(np.mean((rf.predict(xx)-ye)**2)-base_mse))
  perm.append({'features':cols,'mean':float(np.mean(reps)),'std':float(np.std(reps,ddof=1))})
 grid=np.linspace(-1.4,1.4,60);ice=[]
 for row in xe[:30]:xx=np.tile(row,(60,1));xx[:,0]=grid;ice.append(rf.predict(xx))
 pdp=np.array([rf.predict(np.c_[np.full(len(xe),v),xe[:,1:]]).mean() for v in grid]);edges=np.quantile(xt[:,0],np.linspace(0,1,11));delta=[];counts=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  sel=(xt[:,0]>=lo)&(xt[:,0]<(hi if hi<edges[-1] else hi+1e-9));low=xt[sel].copy();high=low.copy();low[:,0]=lo;high[:,0]=hi;delta.append(float(np.mean(rf.predict(high)-rf.predict(low))));counts.append(int(sel.sum()))
 ale=np.cumsum(delta)-np.array(delta)/2;ale-=np.average(ale,weights=counts)
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].scatter(xt[:,0],xt[:,2],s=7,alpha=.25,color='#247b94');axs[0].plot([-1.3,1.3],[1,1],'o--',color='#d97b36');axs[0].set(xlabel='x0',ylabel='x2',title=L('相关特征与人工替换','Correlated features and replacement'));axs[1].barh(['x0','x1','x2','x0+x2'],[v['mean'] for v in perm],xerr=[v['std'] for v in perm],color='#247b94');axs[1].set(xlabel=L('置换后的MSE增加','MSE increase after permutation'),title=L('12次置换的均值与标准差','Mean and SD over 12 permutations'));axs[2].barh(list(rmse),list(rmse.values()),color='#d97b36');axs[2].set(xlabel='RMSE',title=L('同一200点测试集','Same 200-record test set'));save(fig,'global_models')
 fig,axs=plt.subplots(1,2,figsize=(11,4.7),layout='constrained');axs[0].plot(grid,np.array(ice).T,color='#9abac5',alpha=.45,linewidth=.7);axs[0].plot(grid,pdp,color='#d97b36',lw=3,label='PDP');axs[0].set(xlabel='x0',ylabel=L('预测结果','Predicted outcome'),title=L('30条ICE与200点PDP','30 ICE curves and 200-record PDP'));axs[0].legend();axs[1].plot(grid,pdp-pdp.mean(),label=L('PDP减去网格均值','PDP minus grid mean'));axs[1].plot((edges[1:]+edges[:-1])/2,ale,'o-',label=L('ALE按样本数居中','ALE centered by bin counts'));axs[1].set(xlabel='x0',ylabel=L('居中后的模型效应','Centered model effect'),title=L('替换全体，或只做局部差分','Global replacement or local differences'));axs[1].legend(fontsize=8);save(fig,'dependence')
 bg=xt[:80];shaps=np.array([exact_shap(rf,row,bg)[0] for row in xe[:30]]);x=xe[0];phi,base,pred=exact_shap(rf,x,bg);altphi,altbase,_=exact_shap(rf,x,xt[xt[:,0]>0][:80]);lime=[]
 for width in [.2,.8]:
  for seed in range(5):
   rg=np.random.default_rng(seed);near=x+rg.normal(size=(600,3))*width;dist=np.sum(((near-x)/width)**2,axis=1);weights=np.exp(-dist/2);lm=Ridge(alpha=.01).fit(near,rf.predict(near),sample_weight=weights);approx=lm.predict(near);target=rf.predict(near);r2=1-np.sum(weights*(target-approx)**2)/np.sum(weights*(target-np.average(target,weights=weights))**2);lime.append({'width':width,'seed':seed,'coefficients':lm.coef_.tolist(),'point_prediction':float(lm.predict(x[None])[0]),'weighted_r2':float(r2)})
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');vals=[base,*phi];bottom=0
 for i,v in enumerate(vals):axs[0].bar(i,v,bottom=bottom,color='#247b94' if v>=0 else '#d97b36');bottom+=v
 axs[0].axhline(pred,color='#20394a',ls='--');axs[0].set(xticks=range(4),xticklabels=['Base','x0','x1','x2'],ylabel=L('模型结果单位','Model outcome units'),title=L('精确三特征Shapley求和','Exact three-feature Shapley sum'))
 for j in range(3):axs[1].scatter(shaps[:,j],j+rng.uniform(-.14,.14,30),c=xe[:30,j],cmap='coolwarm',vmin=-1.5,vmax=1.5,s=24)
 axs[1].axvline(0,color='#b6c5cc');axs[1].set(yticks=range(3),yticklabels=['x0','x1','x2'],xlabel=L('Shapley贡献','Shapley contribution'),title=L('30个测试对象；颜色为特征值','30 test records; color is feature value'));fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-1.5,1.5),cmap='coolwarm'),ax=axs[1],label=L('特征值','Feature value'),shrink=.65)
 for w,c in [(.2,'#247b94'),(.8,'#d97b36')]:cs=np.array([a['coefficients'] for a in lime if a['width']==w]);axs[2].errorbar(range(3),cs.mean(0),yerr=cs.std(0,ddof=1),fmt='o-',color=c,label=f'width={w}')
 axs[2].set(xticks=range(3),xticklabels=['x0','x1','x2'],ylabel=L('局部线性斜率','Local linear slope'),title=L('5个邻域种子的均值与标准差','Mean and SD over 5 neighborhood seeds'));axs[2].legend();save(fig,'local_attribution')
 digits=load_digits();images=digits.images[:,None]/16;labels=digits.target;it,ie=train_test_split(np.arange(len(labels)),test_size=.3,stratify=labels,random_state=25);trainx=torch.tensor(images[it],dtype=torch.float32);trainy=torch.tensor(labels[it]);testx=torch.tensor(images[ie],dtype=torch.float32);model=CNN();optimizer=torch.optim.Adam(model.parameters(),lr=.003);trace=[]
 for epoch in range(35):
  order=torch.randperm(len(it));total=0
  for idx in order.split(128):logits=model(trainx[idx])[0];loss=F.cross_entropy(logits,trainy[idx]);optimizer.zero_grad();loss.backward();optimizer.step();total+=float(loss.detach())*len(idx)
  trace.append(total/len(it))
 model.eval();predicted=model(testx)[0].argmax(1).detach().numpy();acc=float(np.mean(predicted==labels[ie]));selected=int(np.flatnonzero((labels[ie]==3)&(predicted==3))[0]);image=testx[selected:selected+1].clone();target=3;xin=image.clone().requires_grad_(True);logits,a,b=model(xin);grad=torch.autograd.grad(logits[0,target],xin,retain_graph=True)[0];bggrad=torch.autograd.grad(logits[0,target],b)[0];cam_signed=(bggrad.mean((2,3),keepdim=True)*b).sum(1).detach().numpy()[0];cam=np.maximum(cam_signed,0);cam/=max(cam.max(),1e-12);zero=torch.zeros_like(image);meanbase=trainx.mean(0,keepdim=True);attr=ig(model,image,zero,target);attrmean=ig(model,image,meanbase,target);logit=float(model(image)[0][0,target].detach());base_logit=float(model(zero)[0][0,target].detach());igerr=float(attr.sum().detach())-(logit-base_logit)
 # Compare attribution-ranked deletion with a fixed random deletion schedule.
 order_ig=np.argsort(-np.abs(attr.detach().numpy().ravel()));order_random=np.random.default_rng(250).permutation(64);delete={}
 for name,order in [('IG',order_ig),('Random',order_random)]:
  vals=[]
  for n in range(0,65,4):xx=image.clone();xx.view(-1)[torch.tensor(order[:n].copy())]=0;vals.append(float(model(xx)[0][0,target].detach()))
  delete[name]=vals
 fig,axs=plt.subplots(2,3,figsize=(11,7.4),layout='constrained');maps=[image.numpy()[0,0],abs(grad.detach().numpy()[0,0]),attr.detach().numpy()[0,0],attrmean.detach().numpy()[0,0],cam_signed,cam];titles=[L('真实输入：3','Observed input: 3'),'|Saliency|',L('IG：黑色基线','IG: black baseline'),L('IG：均值基线','IG: mean baseline'),L('Grad-CAM：取正部之前','Grad-CAM: before positive-part step'),L('Grad-CAM：取正部之后','Grad-CAM: after positive-part step')]
 for j,(ax,arr,title) in enumerate(zip(axs.flat,maps,titles)):
  vmax=1 if j==5 else max(max(abs(maps[2]).max(),abs(maps[3]).max()) if j in [2,3] else abs(arr).max(),1e-8);im=ax.imshow(arr,cmap='coolwarm' if j in [2,3,4] else 'gray' if j==0 else 'magma',vmin=-vmax if j in [2,3,4] else 0,vmax=vmax);ax.set_title(title,fontsize=11);ax.set_xticks([]);ax.set_yticks([]);fig.colorbar(im,ax=ax,shrink=.6)
 save(fig,'image_attribution')
 # A controlled concept direction: synthetic central vertical versus horizontal strokes.
 concept=[];cl=[]
 for c in [0,1]:
  for _ in range(60):
   xx=rng.uniform(0,.1,(8,8));pos=int(rng.integers(2,6));xx[:,pos]=.9 if c else xx[:,pos]
   if c==0:xx[pos,:]=.9
   concept.append(xx);cl.append(c)
 concept=torch.tensor(np.array(concept)[:,None],dtype=torch.float32);activation=model(concept)[1].detach().flatten(1).numpy();ct,ce=train_test_split(np.arange(120),test_size=.25,stratify=cl,random_state=25);probe=LogisticRegression(C=1,max_iter=2000).fit(activation[ct],np.array(cl)[ct]);cav=probe.coef_[0];cav/=np.linalg.norm(cav);probeacc=float(probe.score(activation[ce],np.array(cl)[ce]));tcav={}
 for k in [1,3,7]:
  sub=testx[labels[ie]==k];first=model(sub)[1].detach().requires_grad_(True);score=model.from_first(first)[0][:,k];direction=(torch.autograd.grad(score.sum(),first)[0].flatten(1).detach().numpy()*cav).sum(1);tcav[str(k)]={'n':len(sub),'positive_fraction':float(np.mean(direction>0)),'mean_directional_derivative':float(direction.mean())}
 # Input optimization maximizes one learned channel with L2 and total-variation regularization.
 vis=torch.tensor(rng.uniform(.2,.8,(1,1,8,8)),dtype=torch.float32,requires_grad=True);vo=torch.optim.Adam([vis],lr=.04);channel=2
 for _ in range(100):
  acts=model(vis)[1];tv=(vis[:,:,:,1:]-vis[:,:,:,:-1]).square().mean()+(vis[:,:,1:]-vis[:,:,:-1]).square().mean();loss=-acts[:,channel].mean()+.03*vis.square().mean()+.1*tv;vo.zero_grad();loss.backward();vo.step()
  with torch.no_grad():vis.clamp_(0,1)
 # Intervention on a trained internal channel: zero channel2 in conv1 before the rest of the network.
 first=model(testx)[1].detach();ablated=first.clone();ablated[:,channel]=0;ablacc=float(np.mean(model.from_first(ablated)[0].argmax(1).detach().numpy()==labels[ie]));activation_drop=float((model.from_first(first)[0][:,3]-model.from_first(ablated)[0][:,3]).mean().detach())
 fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
 for name,vals in delete.items():axs[0].plot(range(0,65,4),vals,'o-',label=name)
 axs[0].set(xlabel=L('归零像素数','Pixels set to zero'),ylabel=L('数字3的logit','Digit-3 logit'),title=L('同一图像、同一黑色替换','Same image and black replacement'));axs[0].legend();vim=axs[1].imshow(vis.detach().numpy()[0,0],cmap='gray',vmin=0,vmax=1);axs[1].set_title(L('通道2偏好的亮度模式','Channel-2 brightness preference'));axs[1].set_xticks([]);axs[1].set_yticks([])
 for spine in axs[1].spines.values():spine.set_visible(True);spine.set_color('#8fa5b1')
 fig.colorbar(vim,ax=axs[1],shrink=.6,label=L('归一化强度','Normalized intensity'));axs[2].bar(list(tcav),[v['positive_fraction'] for v in tcav.values()],color='#247b94');axs[2].set(ylim=(0,1.05),xlabel=L('测试真实类别','True test class'),ylabel=L('概念方向导数为正的比例','Fraction with positive concept derivative'),title=L('竖线相对横线的方向','Vertical-versus-horizontal direction'));save(fig,'interventions_concepts')
 train_acts=model(trainx)[1][:,channel].mean((1,2)).detach().numpy();top6=np.argsort(-train_acts)[:6];fig,axs=plt.subplots(2,6,figsize=(12,4.8),layout='constrained')
 for j,k in enumerate([60,61,62,0,1,2]):axs[0,j].imshow(concept[k,0],cmap='gray',vmin=0,vmax=1);axs[0,j].set_title(L('竖线','Vertical') if k>=60 else L('横线','Horizontal'))
 for j,k in enumerate(top6):axs[1,j].imshow(trainx[k,0],cmap='gray',vmin=0,vmax=1);axs[1,j].set_title(f'label={int(trainy[k])}, a={train_acts[k]:.2f}',fontsize=9)
 for ax in axs.flat:ax.set_xticks([]);ax.set_yticks([])
 fig.suptitle(L('上：合成概念样本；下：通道2平均激活最高的训练图','Top: synthetic concept examples; bottom: training images with highest channel-2 mean activation'));save(fig,'concept_examples')
 # Transparent feasible counterfactual for a two-feature score, with x1 immutable.
 original=np.array([1.,1.]);threshold=5.;changed=original.copy();changed[1]=(threshold-original[0])/2;cf_score=float(changed[0]+2*changed[1])
 summary={'tabular_train_n':len(tr),'tabular_test_n':len(te),'feature_correlation':float(np.corrcoef(X[:,0],X[:,2])[0,1]),'rmse':rmse,'permutation':perm,'shap_point':x.tolist(),'shap_values':phi.tolist(),'shap_base':base,'shap_prediction':pred,'shap_additivity_error':float(base+phi.sum()-pred),'shap_alternative_values':altphi.tolist(),'shap_alternative_base':altbase,'lime':lime,'digits_train_n':len(it),'digits_test_n':len(ie),'digits_accuracy':acc,'selected_test_index':selected,'selected_original_index':int(ie[selected]),'target_logit':logit,'black_baseline_logit':base_logit,'ig_sum':float(attr.sum().detach()),'ig_completeness_error':igerr,'concept_probe_accuracy':probeacc,'concept_direction':tcav,'ablated_channel':channel,'ablated_accuracy':ablacc,'class3_mean_logit_drop_after_ablation':activation_drop,'counterfactual_original_score':3.,'counterfactual_new_score':cf_score,'counterfactual_immutable_error':float(changed[0]-original[0]),'deletion':delete}
 constrained_x=np.tile(x,(60,1));constrained_x[:,0]=grid;summary['monotonic_violation']=float(max(0,-np.min(np.diff(models['Monotonic'].predict(constrained_x)))));summary['ale_weighted_mean']=float(np.average(ale,weights=counts));summary['gradcam_signed_range']=[float(cam_signed.min()),float(cam_signed.max())];summary['gradcam_positive_max']=float(cam.max());summary['channel2_brightness_correlation']=float(np.corrcoef(trainx.mean((1,2,3)).numpy(),train_acts)[0,1])
 torch.save(model.state_dict(),out/'digits-cnn.pt');np.savez_compressed(out/'experiment_data.npz',X=X,y=y,train_indices=tr,test_indices=te,pdp_grid=grid,pdp=pdp,ale_edges=edges,ale=ale,shap=shaps,digits_train_indices=it,digits_test_indices=ie,image=image.numpy(),gradient=grad.detach().numpy(),ig=attr.detach().numpy(),ig_mean=attrmean.detach().numpy(),gradcam=cam,concept_images=concept.numpy(),concept_labels=np.array(cl),cav=cav,optimized_stimulus=vis.detach().numpy(),loss_trace=trace);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

For a new interpretation task, state one clear question: which output of which model is being explained, for which object, relative to what reference, and for what decision? Choose a method that matches it, then examine its account with another calculation or intervention. The explanation becomes a research tool for locating errors, proposing hypotheses and designing the next experiment, with its meaning carried by the calculation rather than by the visual appeal of a heatmap.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M25.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Christoph Molnar — Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/)

   Explanation goals and method organization.

   CC BY-NC-SA book; linked, no figure copied
2. [Ribeiro et al. (2016), Why Should I Trust You?](https://arxiv.org/abs/1602.04938)

   Original local-surrogate problem.

   Primary reference
3. [SHAP — Beeswarm example and TreeExplainer](https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/plots/beeswarm.html)

   Original plot, background records and contribution distributions.

   MIT, unmodified figure
4. [SHAP — TreeExplainer output scale](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html)

   Default raw XGBoost output is log-odds.

   MIT documentation
5. [Sundararajan et al. (2017), Axiomatic Attribution for Deep Networks](https://proceedings.mlr.press/v70/sundararajan17a.html)

   IG, references and attribution properties.

   Primary reference
6. [Captum — Integrated Gradients](https://captum.ai/docs/extension/integrated_gradients)

   Targets, baselines and completeness discrepancy.

   Official technical reference
7. [Selvaraju et al., Grad-CAM](https://arxiv.org/abs/1610.02391)

   Convolutional-gradient localization, ICCV 2017 and later version.

   Primary reference
8. [Kim et al. (2018), TCAV](https://proceedings.mlr.press/v80/kim18d.html)

   Concept directions and sensitivity.

   Primary reference
9. [Olah, Mordvintsev & Schubert (2017), Feature Visualization](https://distill.pub/2017/feature-visualization/)

   Optimized stimuli, diversity and original image.

   CC BY4.0, unmodified figure
10. [Adebayo et al., Sanity Checks for Saliency Maps](https://arxiv.org/abs/1810.03292)

    Parameter/label randomization and explanation evaluation.

    Primary reference
11. [UCI — Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    8×8 digits, using a new split of the original test subset bundled with scikit-learn.

    CC BY4.0
