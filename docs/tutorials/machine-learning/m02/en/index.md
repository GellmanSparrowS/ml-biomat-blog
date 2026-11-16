# Mathematics that makes a model inspectable

Source: https://ml-biomat.com/tutorials/machine-learning/m02/en/
Language: en

Connect shapes, units, transformations, gradient steps and probability costs through four small experiments.

## Mathematics as a way to inspect predictions

Suppose you want to predict daily electricity consumption from temperature, visitor count and opening hours. A table contains several columns, but the program must turn them into one predicted number. After discovering that predictions are too high, you need to decide which parameter to adjust and by how much. Even a useful average prediction leaves a further question about day-to-day variation. These problems lead to linear algebra, calculus and probability. They are tools introduced as a problem demands them. This chapter follows one computational chain: organize inputs, produce predictions, measure error, adjust parameters and check whether the numerical result deserves its interpretation.

Three questions make formulas easier to read: what does a quantity describe, what is its shape, and what are its units? Temperature is a scalar measured on a defined scale; a month of temperatures is a sequence; one hundred days with three features form a table with one hundred rows and three columns. Multiplying that table by three weights should produce one hundred predictions. Shape and unit checks catch many errors before a long calculation begins. Each experiment therefore includes concrete dimensions and small examples that can be checked by hand before inspecting the complete Python results.

The figures come from explicit geometric constructions and small numerical experiments. They show a circle transformed by a matrix, a two-dimensional field reconstructed from a few components, gradient updates that either approach or escape a minimum, and probability reports that incur different costs. These are working parts of later models. Linear regression uses matrix products, principal components use projections and decompositions, neural networks use the chain rule, and probabilistic classifiers use logarithmic losses. Seeing the connections prepares you to read implementations without memorizing a list of mathematical terms detached from their purposes.

## From a column of numbers to a batch calculation

A single number is a scalar; an ordered collection is a vector; a rectangular table is a matrix. In programming, a tensor commonly means an array with an arbitrary number of axes. A batch of color images might have axes for image number, height, width and color channel. Each axis carries meaning, so exchanging axes changes more than the appearance of the array. Treating height as the batch axis may still permit an operation to run while changing the underlying question. Define the axes before deciding how to broadcast, transpose or reduce them.

$$
\widehat{\mathbf y}=X\mathbf w+b\mathbf1_n,\qquad\widehat y_i=\sum_{j=1}^{p}X_{ij}w_j+b
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46833dd7644e5c60bb4525fe.svg) | An n×p input matrix; rows are observations, columns are features with their own units. |
| ![Formula](https://ml-biomat.com/static/agent-math/dbf1dc27226e2761db070ccb.svg) | Sample count, feature count, row index and column index, all unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/96db857c645773bf5928888e.svg) | A p-vector of weights and its jth entry, in output units divided by feature-j units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Scalar intercept in output units. |
| ![Formula](https://ml-biomat.com/static/agent-math/78cd82e74e7c5af5aa1274cd.svg) | An n-vector of ones, broadcasting the intercept to observations; unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/63a5ce02962df2a4e8d07d43.svg) | An n-vector of predictions and prediction i, in target units. |

With rows (1,2) and (3,4), weights (2,−1) and intercept 5, predictions are 5 and 7. Shapes (2,2) times (2,) produce (2,).

Matrix multiplication sums over the feature axis. For one observation, multiply each of its three features by the corresponding weight and add the contributions. Applying the same rule to one hundred observations yields one hundred predictions. In NumPy, the @ operator expresses matrix multiplication, while * normally expresses elementwise multiplication. Both can execute without an error. If X has shape (100,3) and w has shape (3,), X@w produces one hundred numbers; X*w retains a (100,3) table of separate contributions. Checking the first row by hand is often more informative than examining the entire printed array.

Units propagate through the computation. If consumption is measured in kilowatt-hours and temperature in degrees Celsius, the corresponding coefficient has units of kilowatt-hours per degree Celsius. If opening time is measured in hours, its coefficient has units of kilowatts. Different feature units are compatible because each weighted contribution has the same output unit. The intercept must have that output unit too. Standardization changes the interpretation of coefficients and the numerical geometry, but it does not create information. Retain the training means and standard deviations so that future observations enter the same coordinate system.

Broadcasting makes batch operations convenient but can conceal an alignment mistake. A three-element feature-mean vector can be subtracted from a (100,3) matrix because the last axis aligns with the three features. A prediction array accidentally stored as (100,1), however, can interact with a target array of shape (100,) to create a (100,100) difference table rather than one hundred residuals. Inspect shapes at important transitions and verify alignment on a two-row example. The same habit later applies to batch, time and channel dimensions in neural networks.

## Matrices transform space; projections retain directions

Draw a two-dimensional vector as an arrow from the origin. A matrix then becomes a rule transforming every arrow. Some matrices rotate; others stretch one direction or mix coordinates. Watching a circle become an ellipse reveals the effect on all directions at once. The orange marker follows the same point through each stage, preventing the symmetry of a circle from concealing a rotation or reflection. Coordinates use dimensionless teaching scales. Direction and relative length, rather than a particular physical interpretation of the axes, are the quantities under investigation.

![A unit circle passes through the orientation, stretch and orientation stages of SVD. The orange point tracks one input; the final panel equals direct multiplication by the matrix.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e3638f1bfbd840096e756836.svg?v=e3638f1bfbd8)

Figure 1A unit circle passes through the orientation, stretch and orientation stages of SVD. The orange point tracks one input; the final panel equals direct multiplication by the matrix.

An inner product measures directional alignment together with magnitude. Orthogonal arrows have zero inner product; similarly directed arrows generally have a positive inner product whose size also depends on their lengths. Projection asks a more specific question: what part of a vector is visible along a chosen direction? A shadow is a useful analogy because it retains some directions while discarding others. Dimensionality reduction necessarily makes such a choice. The discarded part may be noise, but it may also contain a weak signal that a prediction task needs. A projection is therefore best understood together with the objective it is intended to serve.

$$
\operatorname{proj}_{\mathbf u}(\mathbf x)=\frac{\mathbf u^\top\mathbf x}{\mathbf u^\top\mathbf u}\mathbf u,\qquad A\mathbf v=\lambda\mathbf v
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/99aba7f28d3cd80a9ab78b53.svg) | Equal-dimensional vectors; u is a nonzero projection direction on a consistent coordinate scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/9221822a6402f4d6cb9d08be.svg) | Transpose; uᵀx is an inner product. |
| ![Formula](https://ml-biomat.com/static/agent-math/586e312e13336db7e2ba5c78.svg) | Projection along the specified direction, in the same units as x. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Square linear transformation, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/67f20bb68a72f1c8979c3402.svg) | Nonzero eigenvector and its eigenvalue; lambda is the signed stretch factor. |

For x=(3,2) and u=(1,0), the projection is (3,0), discarding (0,2). With A=diag(2,1), v=(1,0) satisfies Av=2v, so lambda=2.

An eigenvector identifies a stable direction of a square transformation: after multiplication, it remains on the same line, although its length or sign may change. The factor is the eigenvalue. A real matrix need not possess a complete real eigenvector basis. Covariance matrices, however, are symmetric and positive semidefinite, so they admit orthogonal eigenvectors with nonnegative eigenvalues. This makes them especially convenient for data analysis. Their eigenvectors identify directions of variation, and their eigenvalues quantify the variance in those directions. Principal component analysis retains selected directions and records how much variation is discarded.

Large variance is not automatically useful predictive information. A large background drift can dominate a sensor dataset while a smaller component distinguishes the classes. Evaluate a projection according to whether the objective is reconstruction, denoising, compression or prediction. Centering makes directions describe variation around the mean. Dividing by feature standard deviations additionally changes whether large numerical scales receive more influence. That decision depends on the meaning of the original units. The geometric view makes the choice visible instead of treating dimensionality reduction as a preprocessing button with one universally correct setting.

## Decomposing a transformation into ordered components

Singular value decomposition expresses a matrix as three transformations: change input directions, stretch along orthogonal directions, then change output directions. It applies to rectangular matrices and therefore fits data tables more broadly than an eigenvector discussion restricted to square matrices. Figure 1 follows these stages. The unit circle undergoes an orientation change, unequal stretching and a final orientation change, reaching the same ellipse as direct multiplication by the original matrix. Singular values state the stretching magnitude for each independent direction and are ordered from largest to smallest.

$$
A=U\Sigma V^\top,\qquad A_r=\sum_{k=1}^{r}\sigma_k\mathbf u_k\mathbf v_k^\top
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | An m×n real matrix with the units of the data. |
| ![Formula](https://ml-biomat.com/static/agent-math/b5ab03b659ab43ca500f4c01.svg) | Row count, column count, retained rank and component index; 1≤r≤min(m,n). |
| ![Formula](https://ml-biomat.com/static/agent-math/181c6fbfc16569597629ec4d.svg) | Reduced orthonormal-column matrices of shapes m×s and n×s, where s=min(m,n); directions are unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1fbad29a1619c9468255aa67.svg) | An s×s diagonal matrix and its nonnegative descending entries; singular values inherit A units. |
| ![Formula](https://ml-biomat.com/static/agent-math/45b9cfc916d4ca94324ea100.svg) | Column k of U and V, and the r-term approximation in the units of A. |

For A=diag(3,1), U and V may be identity matrices, with singular values 3 and 1. Keeping the first term gives diag(3,0), with Frobenius error 1 and relative error 1/√10≈0.3162.

Keeping only a few large singular values and their associated directions gives a low-rank approximation. For a grayscale image viewed as a matrix, one rank-one component is the outer product of a vertical pattern and a horizontal pattern. Several such separable patterns can combine into a more complicated field. Our example is an analytically generated scalar field containing two smooth peaks and diagonal oscillations. It is not a photograph. Knowing its construction lets us compare lost and retained structures directly rather than equating visual smoothness with successful compression.

![A dimensionless 96×96 field formed from two Gaussian peaks and diagonal oscillations. Panels share a color scale; lower plots show singular-value decay and relative Frobenius reconstruction errors.](https://ml-biomat.com/static/tutorials/machine-learning/figures/79e242bbe6a70452bc3d97ea.svg?v=79e242bbe6a7)

Figure 2A dimensionless 96×96 field formed from two Gaussian peaks and diagonal oscillations. Panels share a color scale; lower plots show singular-value decay and relative Frobenius reconstruction errors.

The upper panels share a color scale for the original field and its approximations. The lower panels show singular-value decay and relative reconstruction error. The relative error takes the square root of the sum of squared pixel discrepancies and divides it by the corresponding length of the original field. This dimensionless quantity supports comparisons across amplitude scales. Retaining more components reduces reconstruction error. Once the remaining singular values approach floating-point precision, retaining them adds almost no visible structure. Truncated SVD is optimal for a fixed rank under this squared reconstruction criterion; that statement concerns reconstruction, not classification accuracy.

The decomposition also reveals numerical sensitivity. A very small singular value means that changes along one input direction have little effect on the output. Reversing the mapping then requires division by a small number, amplifying measurement errors. This explains why regression implementations normally use stable least-squares solvers or regularization rather than explicitly forming a matrix inverse. A condition number based on the largest and smallest nonzero singular values describes one aspect of this amplification. It is a diagnostic for the specified linear problem, not a universal quality score for every machine-learning model.

## What does a small adjustment change?

When adjusting a tap, we care how much the flow changes if the handle turns a little farther. A derivative measures this local rate of change. A steep response curve means a small input adjustment causes a large output change; a flat region means the same adjustment has little effect. If input and output carry physical units, the derivative carries output units divided by input units. Machine learning replaces the handle with a model parameter and the flow with a loss. The derivative then tells us how a small parameter adjustment changes the objective near the current setting.

$$
\frac{df}{dx}=\lim_{h\to0}\frac{f(x+h)-f(x)}h,\qquad\frac{dL}{dw}=\frac{dL}{d\widehat y}\frac{d\widehat y}{dw}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a580622b14a1c16add55735.svg) | Input, input perturbation and output function; h has x units and the derivative has f units divided by x units. |
| ![Formula](https://ml-biomat.com/static/agent-math/af71e757095127e67ae46646.svg) | The limit of the difference quotient as the perturbation approaches zero, when the derivative exists. |
| ![Formula](https://ml-biomat.com/static/agent-math/0af214a4fb74136f9c2fe407.svg) | Loss, scalar parameter and intermediate prediction; the chain rule multiplies derivatives along differentiable dependencies. |

Let x=3, y=5, prediction wx and loss (wx−y)². At w=2, prediction is 6; dL/dprediction=2 and dprediction/dw=3, giving dL/dw=6. Expanding the square and differentiating gives the same result.

Models usually have several parameters. A partial derivative changes one parameter while holding the others fixed. Arranging all partial derivatives in parameter order gives the gradient vector. Under the usual Euclidean geometry, the gradient points in the direction of greatest local increase, while its negative points toward greatest local decrease. “Greatest” compares infinitesimal moves of the same size. It does not imply that an arbitrarily long step in that direction decreases the objective. When the landscape curves, a local slope is guidance for a nearby move rather than a map of the whole terrain.

Predictions often involve several successive calculations, so derivatives need the chain rule. Parameters first determine a prediction, and that prediction determines a loss. Their overall influence is obtained by multiplying the local rates along the computational chain. In the worked example, prediction is weight times input and loss is the squared difference from an observation. One factor comes from differentiating the square; the other comes from the dependence of prediction on the weight. Backpropagation applies this principle systematically through many layers and adds contributions where paths branch. Automatic differentiation saves arithmetic while retaining the need for the correct objective and computational graph.

Finite differences provide an independent check. Slightly increase and decrease a parameter, recompute the loss, and divide the difference between the losses by the distance between those perturbations. The script compares this central-difference approximation against the analytic gradient of a quadratic. The perturbation should not simply be as small as possible. If too small, subtracting nearly equal floating-point values loses significant digits; if too large, it stops measuring the local slope. Checking agreement across several sensible perturbation sizes is more informative than relying on a single extremely small number.

## Descending a slope, one controlled step at a time

Gradient descent repeatedly moves opposite the gradient, with a learning rate controlling the step length. Our objective is a bowl whose second direction has eight times the curvature of the first. A small step is stable but requires more updates. A larger stable step can oscillate across the steep direction while the oscillations gradually shrink. An excessive step overshoots by more on every iteration and diverges. The figure uses the same initial parameters with three learning rates, allowing the parameter-space trajectories and objective curves to tell the same numerical story.

$$
L(\mathbf w)=\tfrac12(w_1^2+kw_2^2),\quad\nabla L=(w_1,kw_2)^\top,\quad\mathbf w_{t+1}=\mathbf w_t-\eta\nabla L(\mathbf w_t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cb4681a1a45ee2509bf3d35c.svg) | Two-dimensional parameter vector and its coordinates, dimensionless in this example. |
| ![Formula](https://ml-biomat.com/static/agent-math/7677415a903353266414162c.svg) | Quadratic objective and positive curvature; k>0 gives strict convexity, with k=8 in the example. |
| ![Formula](https://ml-biomat.com/static/agent-math/8c12ab9487a4458e174c3e1d.svg) | Gradient containing the two partial derivatives, with the parameter shape. |
| ![Formula](https://ml-biomat.com/static/agent-math/a75429b238a0ac5516db3841.svg) | Update index and positive learning rate, dimensionless here. |

At (2,2) with k=8 the gradient is (2,16). A step of 0.1 gives (1.8,0.4) and loss 0.5(3.24+1.28)=2.26. Stability for this quadratic requires 0<eta<2/max(1,k), hence an upper bound of 0.25 when k=8.

![Twenty-five gradient updates from (2,2) on 0.5(w₁²+8w₂²). The left panel fixes the viewing region, so a diverging path leaves it; the logarithmic objective plot retains the full numerical growth.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1b84cc19f05ebbf7be706e0d.svg?v=1b84cc19f05e)

Figure 3Twenty-five gradient updates from (2,2) on 0.5(w₁²+8w₂²). The left panel fixes the viewing region, so a diverging path leaves it; the logarithmic objective plot retains the full numerical growth.

Convexity gives an important geometric guarantee: along the line between two inputs, function values do not rise above the straight interpolation of the endpoint values. For a differentiable convex function, a point with zero gradient is a global minimizer. The quadratic bowl is a standard example. Nonconvex objectives can contain several basins, saddle points and flat regions, so local gradient information does not identify the best global location by itself. This distinction explains different guarantees without imagining every practical objective as an arbitrary mountain landscape. Even a convex problem can converge slowly when coordinate scales and learning rates are poorly matched.

Some parameters must satisfy constraints: probabilities are nonnegative, and mixture proportions must sum to one. Constrained optimization reduces an objective while maintaining these conditions. Projected gradient descent first takes an ordinary gradient step and then returns to the feasible set. For a single nonnegative coordinate, projection clips a negative value to zero; more complicated sets require their corresponding projections. Regularization instead places a preference inside the objective, such as penalizing large weights. These approaches are related, but arbitrary clipping does not automatically solve the same optimization problem as a chosen regularization penalty.

## Walk toward the minimum, one step at a time

Start at (2,2); all quantities are dimensionless. Trajectory and objective share the same calculation. Changing parameters resets the start.

[Figure: Walk toward the minimum, one step at a time](https://ml-biomat.com/tutorials/machine-learning/m02/en/#M02-plot)

The interactive experiment changes the learning rate and the curvature of the second direction, then advances one update at a time. Starting from (2,2), curvature eight and learning rate 0.1 produce (1.8,0.4) after one update; the objective decreases from eighteen to 2.26. This checks the gradient, learning rate, coordinate order and objective definition together. Reset and use a learning rate of 0.3 to observe amplification in the steep direction. Every point is calculated by the recurrence rather than replayed from a decorative animation, so different settings produce genuinely different trajectories.

## An observed outcome and a distribution of possibilities

Tomorrow either rains or does not, yet today's forecast can represent the proportion of possible situations that involve rain. Probabilities lie between zero and one, and probabilities of a complete set of mutually exclusive outcomes sum to one. A random variable assigns a number to each outcome, such as one for rain and zero otherwise. An expectation is a probability-weighted average and need not equal any possible single observation. A coin may have expected heads count 0.7 per trial even though each trial produces zero or one. Variance describes how outcomes spread around that expectation.

$$
\mathbb E[X]=\sum_i p_i x_i=\mu,\quad\operatorname{Var}(X)=\sum_i p_i(x_i-\mu)^2,\quad P(A\mid B)=\frac{P(A\cap B)}{P(B)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0021244cb2867b2bc1498b5a.svg) | Discrete random variable, possible value and value index; values use measurement units. |
| ![Formula](https://ml-biomat.com/static/agent-math/29d8041678f9875c2bfdd4ae.svg) | Outcome probabilities and expectation; probabilities are nonnegative and sum to one, and expectation has X units. |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | Variance, in squared X units. |
| ![Formula](https://ml-biomat.com/static/agent-math/69e39a892cb662e81faeb8af.svg) | Events, probability, intersection and conditioning; P(B)>0 is required and probabilities are unitless. |

For values 0,1,2 with probabilities 0.2,0.5,0.3, the mean is 1.1 and variance is 0.49. If rain has probability 0.5 and rain with congestion has probability 0.3, congestion given rain has probability 0.6.

A conditional probability changes the population within which a proportion is calculated. If congestion occurs on twenty of one hundred dry days and sixty of one hundred rainy days, knowing that a day is rainy directs attention to the rainy-day group. It does not use the combined rate indiscriminately. Conditioning changes the comparison group and is not automatically a causal intervention. Rain and congestion can share relationships with travel choices, visibility and road management. Independence means learning one event does not change the probability of the other. This is stronger than zero correlation, because nonlinear dependence can exist even when a linear correlation vanishes.

Likelihood uses a probability model to compare parameter settings after observations have been collected. After seven heads in ten trials, the data are fixed and candidate head probabilities are compared. Assuming independent trials with a common probability, multiply the probabilities of the observed outcomes. Maximum likelihood selects 0.7. This is a parameter estimate, not a probability that the parameter equals 0.7. Assigning probabilities to the parameter itself requires an additional construction, such as a prior distribution and Bayesian updating. Keeping observations and candidate parameters conceptually separate makes both approaches easier to understand.

![Left: relative log likelihood for seven successes in ten independent trials. Center: binary entropy. Right: cross entropy for different reports when the true success probability is 0.7. Natural logs give nats.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1505123d621a2b7abdc4175c.svg?v=1505123d621a)

Figure 4Left: relative log likelihood for seven successes in ten independent trials. Center: binary entropy. Right: cross entropy for different reports when the true success probability is 0.7. Natural logs give nats.

Logarithms turn the product of independent observation probabilities into a sum. They simplify derivatives and avoid multiplying many small values until the computer rounds them to zero. The first panel shifts log likelihood so that its maximum is zero, preserving the maximizing parameter while making curve shape easier to compare. Independence and a common distribution are part of the model assumptions. Consecutive time points or repeated records from one participant may not satisfy them. Before assigning a likelihood, examine how observations are related rather than treating every array row as a new independent piece of evidence.

## From communication to the cost of probability forecasts

In his 1948 communication study, Claude Shannon centered a practical question: when several messages are possible, how much information is needed on average to identify the message actually sent? An almost inevitable outcome conveys little surprise; equally likely alternatives require more information to distinguish. This leads to entropy. The second panel in Figure 4 displays binary entropy: uncertainty is small near probabilities zero and one and greatest when the two outcomes are equally likely. Statistical uncertainty here is different from whether a message's semantic content is interesting or useful to its recipient.

$$
H(p)=-\sum_i p_i\ln p_i,\quad H(p,q)=-\sum_i p_i\ln q_i,\quad D_{\rm KL}(p\|q)=H(p,q)-H(p)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/89e5019371c0d604f379329e.svg) | True and reported distributions on the same discrete outcomes, each normalized; q_i>0 is needed wherever p_i>0 for finite values. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Outcome index, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d3dd181217f9d250008c256f.svg) | Entropy, cross entropy and KL divergence, in nats for natural logs; 0ln0 is defined as zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | Natural logarithm of dimensionless probabilities. |

For p=(0.5,0.5), entropy is ln2≈0.6931nats. Reporting q=(0.9,0.1) gives cross entropy≈1.2040nats and KL≈0.5108nats. Reporting p itself gives zero extra cost.

Cross entropy prices outcomes drawn from a true distribution using another reported probability distribution. If the true head rate is 0.7 but a forecaster repeatedly reports 0.99, the occasional tail incurs a large logarithmic penalty. The curve is minimized when reported and true probabilities agree. Its excess over the true entropy is the Kullback–Leibler divergence. This measures additional logarithmic cost in a specified direction: exchanging the two distributions generally changes the result, so it is not an ordinary Euclidean distance. Assigning zero probability to an outcome that truly can occur produces an unbounded penalty.

Natural logarithms measure information in nats; base-two logarithms measure it in bits. Changing the base rescales entropy and cross entropy without changing which report is optimal. In classification, an observed label is often encoded as a vector with a one at its class and zeros elsewhere. The cross-entropy expression then reduces to the negative logarithm of the probability assigned to that class. Raising its probability from 0.1 to 0.9 greatly reduces loss, and a confident mistake costs more than a hesitant one. Accuracy examines the largest-probability class; cross entropy also evaluates the quality of the probability report.

$$
\log\sum_{j=1}^{K}e^{z_j}=a+\log\sum_{j=1}^{K}e^{z_j-a},\quad a=\max_jz_j,\quad q_i=e^{z_i-\operatorname{logsumexp}(\mathbf z)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5bf4e2ea8de2808c57b6a731.svg) | Number of classes and class indices, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6f1f5acc2895e75bc4d32d09.svg) | Score, K-vector of scores and largest score, all dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | Normalized probability of class i, nonnegative with total one. |
| ![Formula](https://ml-biomat.com/static/agent-math/6bdb4529d9344276682d4249.svg) | Stable natural log of the exponential sum, on a dimensionless log scale. |

Subtracting the maximum from (1000,1001,999) gives (−1,0,−2), whose exponentials are approximately (0.3679,1,0.1353). Dividing by their sum 1.5032 yields (0.2447,0.6652,0.0900).

Correct algebra still needs a stable numerical implementation. Scores of 1000, 1001 and 999 overflow if exponentiated directly. Subtracting the same maximum from all scores leaves values −1, zero and −2, whose exponentials can be normalized safely. The resulting probabilities are unchanged. The code uses logsumexp for logarithmic normalization and obtains approximately 0.2447, 0.6652 and 0.0900, summing to one. This neither changes the model nor discards a class; it removes a common large scale using an identity. Numerical stability often comes from reorganizing a formula rather than choosing a larger data type.

### Complete experiment: decomposition, differences, optimization and probability

Requires NumPy, SciPy and Matplotlib. Run python main.py --output results --language en to generate four figures, input arrays and summary.json. All data are generated by the explicit rules in the code.

```
"""Small, reproducible experiments in geometry, approximation and optimization."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import logsumexp, xlogy

def main(output, language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
    def t(a,b):return a if zh else b
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    # A complete two-dimensional SVD: rotation/reflection, stretch, rotation.
    A=np.array([[2.,1.],[0.,1.]])
    U,s,Vt=np.linalg.svd(A);theta=np.linspace(0,2*np.pi,401);circle=np.array([np.cos(theta),np.sin(theta)])
    fig,axes=plt.subplots(1,4,figsize=(12,3.2),layout='constrained')
    arrays=[circle,Vt@circle,np.diag(s)@Vt@circle,A@circle]
    titles=[t('单位圆','Unit circle'),'Vᵀ x','Σ Vᵀ x','U Σ Vᵀ x = A x']
    for ax,points,title in zip(axes,arrays,titles):
        ax.plot(*points,color='#167d87',lw=2);ax.scatter(*points[:,0],color='#d48745',s=30,zorder=3)
        ax.axhline(0,color='#b8c7ce',lw=.7);ax.axvline(0,color='#b8c7ce',lw=.7)
        ax.set(xlim=(-2.8,2.8),ylim=(-2.8,2.8),aspect='equal',title=title,xlabel='x₁',ylabel='x₂')
    save(fig,'geometry')
    # Original analytic image, with structure known exactly; no downloaded image.
    x=np.linspace(-1,1,96);xx,yy=np.meshgrid(x,x)
    img=np.exp(-((xx+.35)**2+(yy-.2)**2)/.11)+.6*np.exp(-((xx-.35)**2+(yy+.3)**2)/.09)+.22*np.cos(11*(xx+yy))*np.exp(-xx**2-yy**2)
    u,sv,vt=np.linalg.svd(img,full_matrices=False);ranks=[1,2,4,12];errs=[]
    fig=plt.figure(figsize=(13,6.0),layout='constrained');gs=fig.add_gridspec(2,5,height_ratios=[1,1.1]);field_axes=[]
    for j,(rank,title) in enumerate([(96,t('原始场','Original field'))]+[(r,f'r={r}') for r in ranks]):
        approx=img if rank==96 else (u[:,:rank]*sv[:rank])@vt[:rank]
        ax=fig.add_subplot(gs[0,j]);field_axes.append(ax);field_image=ax.imshow(approx,cmap='magma',vmin=img.min(),vmax=img.max(),origin='lower',extent=[-1,1,-1,1]);ax.set(title=title);ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1])
        if rank!=96:errs.append(float(np.linalg.norm(img-approx)/np.linalg.norm(img)))
    fig.colorbar(field_image,ax=field_axes,location='right',shrink=.85,pad=.025,label=t('场幅值（无量纲）','Field amplitude (dimensionless)'))
    ax=fig.add_subplot(gs[1,:3]);ax.semilogy(np.arange(1,21),sv[:20],'o-',color='#167d87');ax.set(xlabel=t('奇异值序号','Singular-value index'),ylabel=t('奇异值（场幅值单位）','Singular value (field units)'));ax.grid(alpha=.2)
    ax=fig.add_subplot(gs[1,3:]);ax.bar([str(r) for r in ranks],errs,color='#d48745');ax.set(xlabel=t('保留秩 r','Retained rank r'),ylabel=t('相对重建误差','Relative reconstruction error'));save(fig,'svd')
    H=np.diag([1.,8.]);start=np.array([2.,2.]);trajectories={}
    fig,(ax,lossax)=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');g=np.linspace(-2.4,2.4,200);gx,gy=np.meshgrid(g,g);ax.contour(gx,gy,.5*(gx**2+8*gy**2),levels=[.1,.5,1,2,4,8,16],colors='#cad8de')
    for eta,col in [(.05,'#167d87'),(.22,'#d48745'),(.3,'#8b557c')]:
        w=start.copy();path=[w.copy()]
        for _ in range(25):w=w-eta*(H@w);path.append(w.copy())
        path=np.array(path);loss=.5*np.sum(path*(path@H),axis=1);trajectories[str(eta)]={'path':path.tolist(),'loss':loss.tolist()}
        ax.plot(*path.T,'o-',ms=2,color=col,label=f'η={eta}');lossax.semilogy(loss,color=col,label=f'η={eta}')
    ax.set(xlim=(-2.4,2.4),ylim=(-2.4,2.4),xlabel='w₁',ylabel='w₂',title=t('同一碗形目标，三种步长','One quadratic objective, three step sizes'));ax.legend()
    lossax.set(xlabel=t('更新次数','Update'),ylabel=t('目标函数（无量纲）','Objective (dimensionless)'));lossax.grid(alpha=.2);lossax.legend();save(fig,'gradients')
    q=np.linspace(.001,.999,500);p=.7;entropy=-(xlogy(q,q)+xlogy(1-q,1-q));ce=-(p*np.log(q)+(1-p)*np.log1p(-q));loglike=7*np.log(q)+3*np.log1p(-q)
    fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
    axes[0].plot(q,loglike-loglike.max(),color='#167d87');axes[0].axvline(.7,color='#d48745',ls='--');axes[0].set(xlabel=t('候选正面概率 q','Candidate success probability q'),ylabel=t('相对对数似然','Relative log likelihood'),title=t('10次中7次正面','Seven successes in ten trials'))
    axes[1].plot(q,entropy,color='#167d87');axes[1].set(xlabel='q',ylabel=t('熵（nat）','Entropy (nats)'),title=t('不确定性在中间最大','Uncertainty peaks in the middle'))
    axes[2].plot(q,ce,label=t('交叉熵','Cross entropy'),color='#167d87');hp=-(p*np.log(p)+(1-p)*np.log1p(-p));axes[2].axhline(hp,color='#d48745',label='H(p)');axes[2].set(xlabel=t('报告概率 q','Reported probability q'),ylabel='nat',title=t('真实比例 p=0.7','True proportion p=0.7'));axes[2].legend();save(fig,'probability')
    f=lambda v:.5*v@H@v;eps=1e-6;fd=np.array([(f(start+eps*np.eye(2)[i])-f(start-eps*np.eye(2)[i]))/(2*eps) for i in range(2)])
    logits=np.array([1000.,1001.,999.]);probs=np.exp(logits-logsumexp(logits))
    summary={'matrix_reconstruction_error':float(np.linalg.norm(A-U@np.diag(s)@Vt)),'singular_values':s.tolist(),'image_rank_errors':dict(zip(map(str,ranks),errs)),'analytic_gradient':(H@start).tolist(),'finite_difference_gradient':fd.tolist(),'gradient_max_error':float(np.max(np.abs(fd-H@start))),'one_step_eta_0_1':(start-.1*H@start).tolist(),'one_step_loss':f(start-.1*H@start),'stable_probabilities':probs.tolist(),'stable_probability_sum':float(probs.sum()),'entropy_p_0_7_nats':hp,'trajectories':trajectories}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(output/'experiment_data.npz',A=A,image=img,singular_values=sv,q=q,cross_entropy=ce)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

After running the experiment, trace one plotted quantity back to its calculation: a transformed point to its matrix product, an objective value to its coordinates, or a probability to its normalization. Replace an input with an easy hand-checkable number and confirm the expected change. Later chapters combine these components into larger models, but the inspection procedure remains the same. Identify the object, shape and units; verify one calculable relationship; then decide whether the complete experiment answers the question that motivated it.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning — Linear Algebra](https://d2l.ai/chapter_preliminaries/linear-algebra.html)

   Matrices, shapes and norms.

   CC BY-SA 4.0
2. [Dive into Deep Learning — Calculus](https://d2l.ai/chapter_preliminaries/calculus.html)

   Partial derivatives, gradients and chain rule.

   CC BY-SA 4.0
3. [NumPy — Singular Value Decomposition](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)

   Reduced decomposition shapes and reconstruction.

   NumPy documentation
4. [SciPy — logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html)

   Stable logarithmic normalization.

   SciPy documentation
5. [Shannon (1948), A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

   Communication context and original argument for entropy.
