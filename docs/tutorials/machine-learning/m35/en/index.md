# How clouds deform and densities change: normalizing flows

Source: https://ml-biomat.com/tutorials/machine-learning/m35/en/
Language: en

Use probability-mass conservation to understand volume changes and Jacobians, then connect affine coupling, splines, and continuous flows through an actual trained density model.

## 1 Where does probability go when a cloud is bent?

Suppose a device records two sensor readings that usually lie along a curved band. As the first reading increases, the second initially falls and then rises. An ellipse based on a mean and covariance can assign substantial density to the empty middle of that curve. We want a distribution that follows the band, generates plausible new readings, and evaluates density at a particular observation. A normalizing flow turns this into a geometric problem: can a sequence of invertible deformations turn the complicated data cloud back into a Gaussian cloud whose density is easy to calculate?

Imagine an elastic sheet printed with a grid of dots. Stretching a small square leaves its number of dots unchanged but lowers the number per unit area. Compressing it raises that density. Probability obeys the same conservation idea: moving a collection of possible outcomes preserves its probability mass while changing the length, area, or higher-dimensional volume it occupies. A flow therefore moves points and records local expansion. This expansion factor is the geometric meaning of the Jacobian determinant introduced below. The picture also provides a reliable way to check the direction of a density correction.

$$
x=f(z),\qquad p_X(x)=p_Z(z)\left|\frac{dz}{dx}\right|=\frac{p_Z(z)}{|f'(z)|},\qquad z=f^{-1}(x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/62ff9d7345c45d49c87a5d02.svg) | Base variable, transformed variable, differentiable invertible map, and inverse; examples use dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/bd0b4ae4b916ebfc8fbea14f.svg) | Input and output probability densities, with units inverse to their respective coordinate units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ad3f3fdb5413303f68fbd0.svg) | Local slope, inverse slope, and absolute value, retaining a positive length ratio. |

Corresponding small intervals carry the same probability: p_X(x)dx≈p_Z(z)dz. For x=2z+3, slope is two; x=3 corresponds to z=0 and density 1/(2√(2π))≈0.199471. A reversed coordinate can have negative slope, but density uses its absolute value.

The complete argument is already visible in one dimension. Multiply a standard-normal variable by two and shift it right by three. The new distribution is centered at three and has twice the original width. Its center density drops from about 0.398942 to 0.199471 because the same probability mass now occupies twice the length. Translation changes location; scaling changes density. Density is not the probability of being exactly equal to three: a continuous variable assigns zero probability to an individual point. Probability in a small interval is approximately density times interval width.

## 2 From length to area: why a determinant appears

A two-dimensional transformation can rotate, shear, and stretch simultaneously, so one edge length no longer describes its effect. The Jacobian matrix records how each output coordinate responds to a small change in each input coordinate. Applied to a sufficiently small square, it approximately produces a parallelogram. The absolute determinant gives the area ratio. Scaling horizontally by two and vertically by three multiplies area by six and divides density by six. A shear can visibly tilt the square while preserving its area, requiring no corresponding local density change.

$$
\log p_X(x)=\log p_Z(g(x))+\log|\det J_g(x)|,\qquad J_{g,ij}=\frac{\partial g_i}{\partial x_j},\qquad g=f^{-1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1948951fb2582b68d628dbcb.svg) | D-dimensional data and latent vectors, generative mapping, and inverse normalization map; D=2 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/bdd32a98db8b6d68e884c880.svg) | D×D Jacobian matrix, output-coordinate index, and input-coordinate index. |
| ![Formula](https://ml-biomat.com/static/agent-math/4628700cca9689c491f4e5e5.svg) | Determinant, absolute value, natural logarithm, and the two densities; log densities are measured in nats using fixed coordinate units. |

Generative scaling by two horizontally and three vertically gives detJ_f=6 and detJ_g=1/6, decreasing output log density by ln6. Composition multiplies Jacobians and determinants, so log determinants add across layers. Absolute value handles orientation; it does not make a singular mapping invertible.

We use f for the generative mapping from a simple latent variable z to data x, and g for its inverse. To evaluate an observation, apply g to find the corresponding Gaussian coordinate, then add the inverse mapping’s log-volume correction. Logarithms turn products of determinants across many layers into sums, reducing numerical problems with very large or small products. Writing the same calculation in the generative direction changes the correction’s sign. The geometric rule remains unchanged: expanding the occupied region lowers its density.

This construction preserves information. Projecting a two-dimensional point onto one number generally merges distinct inputs, preventing recovery through a single inverse function. A conventional autoencoder may compress into fewer dimensions; basic invertible flow layers preserve dimensionality. Image rearrangements, checkerboard splits, and channel permutations may alter tensor shape while retaining every element. Invertibility also constrains topology: a continuous invertible mapping cannot tear a connected space into genuinely disconnected pieces. It can make the connecting region extremely low-density, approximating clusters that appear visually separate.

## 3 Keep one half as a reference and recover the other

A general deep network is not necessarily easy to invert, even with matching input and output dimensions. Computing a large Jacobian determinant may also be expensive. Real NVP, released in 2016, uses affine coupling layers: divide the coordinates into two groups, leave one unchanged, and use that group to compute a scale and shift for the other. During inversion, the unchanged reference group remains available, so the same scale and shift can be recomputed before subtraction and division. The coefficient network can be complex without itself being invertible.

$$
y_a=x_a,\quad y_b=x_b\odot e^{s(x_a)}+t(x_a),\qquad x_b=(y_b-t(y_a))\odot e^{-s(y_a)},\qquad \log|\det J|=\sum_j s_j(x_a)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64a9e92858a356da3c167f14.svg) | Two coordinate groups before and after a coupling transform; group a is unchanged and group b transformed. Each group is scalar in our example. |
| ![Formula](https://ml-biomat.com/static/agent-math/9d0ae721d9a4bed70799a71d.svg) | Log-scale, shift, and positive scale computed from the reference group, matching group b’s shape. s is dimensionless; t has the transformed coordinate’s units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a2f763450e66e0be3c61a7cf.svg) | Elementwise multiplication, layer Jacobian, and component index within the transformed group. |

With s=ln2 and t(x_a)=3x_a, input (0.5,1) becomes (0.5,3.5). Jacobian [[1,0],[3,2]] has determinant two and log determinant ln2≈0.693147. The unchanged y_a reconstructs coefficients without inverting their network. Code defaults to the normalization direction and samples by invoking inverse=True in reverse layer order.

For a numerical example, retain the first coordinate and replace the second with twice its old value plus three times the first coordinate. Input (0.5,1) becomes (0.5,3.5). Inverting uses the preserved 0.5 and calculates (3.5−1.5)/2 to recover one. The Jacobian is triangular with diagonal entries one and two, giving determinant two. The second output also depends on the first input, but that off-diagonal dependence does not alter the determinant of a triangular matrix. A flexible coefficient network can therefore bend coordinates while keeping the volume calculation tractable.

![Original UvA checkerboard-mask figure partitions variables into preserved and transformed groups. Phillip Lippe, UvA Deep Learning Tutorials; unchanged, with MIT license and copyright retained.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4514065dd34a5a8681e125e0.svg?v=4514065dd34a)

Figure 1Original UvA checkerboard-mask figure partitions variables into preserved and transformed groups. Phillip Lippe, UvA Deep Learning Tutorials; unchanged, with MIT license and copyright retained.

A single coupling layer changes only one group, so subsequent layers exchange the roles. Our two-dimensional example alternately preserves the first and second coordinates. Image models can use the checkerboard pattern shown in the original tutorial figure: one set of squares supplies context while the other is transformed, followed by the opposite split. This mask partitions transformed variables; it serves a different purpose from PixelCNN’s causal mask. After stacking layers, variables can influence one another more extensively. Inversion must undo the layers in reverse order, a requirement directly checked by reconstruction error.

## 4 Train an actual invertible model of a curved density

Our experiment starts with two independent standard-normal variables. It scales the first by 1.2 and combines 0.35 times the second with a quadratic bend determined by the first. This produces a thick banana-shaped cloud. Because the generating transformation is known, its true density can be calculated and displayed alongside the learned density using the same color scale. Independent seeds create 4,096 training points, 1,024 validation points, and 2,048 test points. Parameter learning and selection use the first two sets; the last set provides the final evaluation.

$$
x_1=1.2z_1,\quad x_2=0.35z_2+0.55(z_1^2-1),\quad z\sim\mathcal N(0,I_2),\qquad L(\theta)=-\frac1N\sum_{n=1}^N\log p_\theta(x^{(n)})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/de213b795d23890187cb5527.svg) | Two independent standard-normal coordinates and two transformed coordinates, all dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/03df122ca86d7ab9c1db3258.svg) | Zero-mean two-dimensional Gaussian with identity covariance, and the example’s horizontal scale, vertical thickness, and bend coefficient. |
| ![Formula](https://ml-biomat.com/static/agent-math/1172e770bf980becbada7547.svg) | Network parameters, training-point count, sample index, sample n, and average negative log-density objective in nats per point. |

The generating Jacobian is [[1.2,0],[1.1z₁,0.35]], with constant determinant 0.42. True density is the corresponding standard-Gaussian density divided by 0.42. z=(0,0) maps to x=(0,−0.55), with density about 0.378940. The network trains on point likelihoods without using analytic density labels; the known density provides an independent comparison.

The model contains eight affine coupling layers. Each coefficient network has two 32-unit tanh hidden layers, giving 9,488 parameters overall. The implementation evaluates density in the data-to-Gaussian direction and minimizes mean negative log density. Each layer bounds its log-scale between −0.8 and 0.8 using 0.8 times tanh, keeping individual exponential scales moderate. Zero initialization of the final linear layer makes the initial coupling transformation close to identity. After two hundred epochs, validation loss selects epoch 121. The network begins in a stable coordinate system and gradually learns compression and curvature.

Each update accounts for two effects together. Moving data toward the Gaussian center increases its base-distribution density. Compressing many distinct observations into a small latent region also changes the Jacobian correction. Both terms are necessary to obtain density in the original data coordinates. Rewarding only proximity to the origin would encourage the network to squeeze everything together without accounting for how much probability different original regions contain. The invertible structure and volume correction connect coordinate movement to probability density, making the training objective correspond to the distribution being fitted.

![Left: 700 independent target points in orange and 700 generated points in blue. Middle: density from the known generating rule. Right: learned flow density. Density panels share coordinate limits and color scale; coordinates are dimensionless.](https://ml-biomat.com/static/tutorials/machine-learning/figures/43aabdb70861d97fd56bcc12.svg?v=43aabdb70861)

Figure 2Left: 700 independent target points in orange and 700 generated points in blue. Middle: density from the known generating rule. Right: learned flow density. Density panels share coordinate limits and color scale; coordinates are dimensionless.

On the same independent test set, a fitted single Gaussian gives mean negative log density 2.883696 nats, the flow gives 1.964784, and the known generating density gives 1.961473. The last quantity is the actual target distribution’s average score on these particular samples, placing the learned score in context. Finite-sample values vary with the evaluation points. The scatter panel shows generated samples, while the density panels use the change-of-variables equation. These are separate computations: samples alone can conceal mass discrepancies, and density evaluation alone can miss an error in the inverse sampling path.

![The same latent-coordinate grid after zero,two,four,eight actual inverse coupling layers; orange points track the same 160 latent draws. Grid lines bend while intersections retain one-to-one correspondence.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5437df57ad9b048b7b33cecc.svg?v=5437df57ad9b)

Figure 3The same latent-coordinate grid after zero,two,four,eight actual inverse coupling layers; orange points track the same 160 latent draws. Grid lines bend while intersections retain one-to-one correspondence.

Mapping all 2,048 test points to latent coordinates and back gives maximum coordinate error approximately 1.91×10⁻⁶. Forward and inverse log determinants cancel with maximum error about 4.17×10⁻⁷. At one selected point, automatic differentiation constructs the complete two-dimensional Jacobian, whose log determinant differs from the accumulated layer formula by roughly 3.3×10⁻¹⁶. These checks address different questions: whether positions are recovered, whether volume corrections cancel, and whether the efficient formula agrees with full derivatives. Together they connect mathematical invertibility to the numerical implementation.

## Move a grid through actual invertible layers

The grid and samples come from the trained eight-layer flow. Choose a Gaussian starting point, advance through generation layers, and inspect area ratio, density, and inverse-recovery error. Every selected point uses actual trained weights; both directions support single stepping.

[Figure: Corresponding latent and transformed grids with area and density](https://ml-biomat.com/tutorials/machine-learning/m35/en/#M35-board)

Blue lines show the same grid, orange points are 160 fixed latent samples, and red marks the selected input and output; dashed red segments connect successive layer outputs. Coordinates are dimensionless; both panels use the same length scale. Area ratio comes from the Jacobian, and density is initial Gaussian density divided by that ratio.

## 5 Autoregressive flows: which direction is parallel?

Coupling layers obtain a simple inverse by preserving one variable group. Autoregressive flows instead make the transformation of coordinate i depend on preceding coordinates. Their Jacobian remains triangular, but execution speed depends on which variables provide that context. Masked Autoregressive Flow, introduced in 2017 and abbreviated MAF, is suited to density estimation. Given the complete observed vector, every required prefix is known, so a masked network can compute all coordinate means and scales in one pass. Generating the data requires successive coordinates because later parameters depend on earlier generated values.

$$
z_i=\frac{x_i-\mu_i(x_{<i})}{\sigma_i(x_{<i})},\qquad \sigma_i>0,\qquad \log|\det J_{x\to z}|=-\sum_{i=1}^{D}\log\sigma_i(x_{<i})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/49176a361325b6b62d8f3501.svg) | Data coordinate i, latent coordinate i, preceding data coordinates, and total dimensionality. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc1454c20c7160593f31559a.svg) | Shift and positive scale predicted from the data prefix; μ has x’s units and σ converts between data and latent units. |
| ![Formula](https://ml-biomat.com/static/agent-math/67575451a8129bb2d625dc8b.svg) | Triangular data-to-latent Jacobian, natural logarithm, and determinant. |

MAF computes all parameter sets in parallel when complete x is given. In two dimensions, scales (2,3) give inverse volume ratio 1/6 and correction −ln6. Sampling x_i=μ_i(x_<i)+σ_i(x_<i)z_i requires earlier x values. IAF instead conditions generative coefficients on z_<i, enabling parallel sampling from known z.

Inverse Autoregressive Flow, or IAF, puts the readily parallelized direction on the sampling side. Its coefficient network reads preceding latent coordinates. All latent variables are already available after drawing the initial noise vector, so generation can calculate the transformed coordinates together. Recovering latent variables from an observed data point generally requires sequential inversion. The word “inverse” draws attention to which side supplies the coefficient network’s inputs. When comparing implementations, ask separately how many network evaluations are needed for density evaluation and for sampling.

Three numbers make the dependency visible. Consider x₁=z₁, x₂=z₂+0.5z₁, and x₃=z₃+z₁z₂. Given the complete z vector, every right-hand side is known. Given x, recover z₁ first, then z₂, then z₃. The ordering resembles character generation, but the steps here transform continuous coordinates invertibly and track their density. Coupling layers, MAF, and IAF choose different balances among expressiveness, network-call count, and the direction most frequently needed. Spline transforms provide another design choice by changing the shape of each individual coordinate transformation.

## 6 Replace straight scaling with a flexible monotone curve

For fixed conditioning variables, an affine transformation only scales and shifts a coordinate along a straight line. A nonlinear monotone curve can compress one part of that coordinate and expand another. Neural Spline Flows, introduced in 2019, use monotonic rational-quadratic splines. Ordered input and output knots specify where the curve passes, positive derivatives specify its slopes at the knots, and smooth segments connect adjacent knots. As the input moves right, the output continues moving right, avoiding folds that would merge different input positions.

$$
\xi=\frac{x-x_0}{w},\quad s=\frac hw,\qquad f(x)=y_0+\frac{h\left[s\xi^2+d_0\xi(1-\xi)\right]}{s+(d_0+d_1-2s)\xi(1-\xi)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b578ba9b754822a716ede6.svg) | Input/output left endpoints, input-bin width, and output-bin height; widths and heights are strictly positive. |
| ![Formula](https://ml-biomat.com/static/agent-math/17bae4178ce5e4537b485569.svg) | Input within the segment, local coordinate in [0,1], and secant slope h/w. |
| ![Formula](https://ml-biomat.com/static/agent-math/fe5457fb4e7b4cb7078ce6c0.svg) | Positive derivatives at the left/right endpoints and output value; derivative units are output units per input unit, dimensionless here. |

In the example bin x∈[−1,0], y∈[−2,0.5], w=1,h=2.5,d₀=0.5,d₁=2. At x=−0.5, ξ=0.5; numerator and denominator both equal 1.875, giving f(x)=−1. The quotient rule gives derivative 10/3. Forward and inverse routines share knots and derivatives; inversion solves a quadratic within the corresponding output bin.

The expression is longer than scale-and-shift because it meets several conditions simultaneously: passing through both endpoints, matching both specified endpoint slopes, and remaining monotone between them. Its numerator and denominator are quadratic polynomials in a local coordinate. Given an output, rearranging the equation therefore produces an analytically solvable quadratic. The code uses a root expression that avoids subtracting nearly equal quantities and separately handles the case that reduces to a linear equation. Positive bin widths, heights, and endpoint derivatives maintain invertibility while allowing flexible deformation.

Knots determine the local computation as well. Forward evaluation first locates the input between two input knots, then uses that segment’s width, height, and derivatives. Inversion locates the output between output knots. The two searches use different coordinate axes but identify the same segment correspondence. Identity lines extend the mapping beyond its finite knot range, ensuring that distant points also have a defined transformation. Endpoint slopes equal to one join these tails smoothly to the spline. These boundary choices affect tail densities and inverse results and therefore belong to the complete transform definition.

![A predetermined five-knot rational-quadratic spline: map, positive derivative, and 5,000 transformed samples compared with change-of-variables density. Identity tails use endpoint derivatives one. This construction isolates the spline mechanism.](https://ml-biomat.com/static/tutorials/machine-learning/figures/a7009ed83517d2eadfdba9a2.svg?v=a7009ed83517)

Figure 4A predetermined five-knot rational-quadratic spline: map, positive derivative, and 5,000 transformed samples compared with change-of-variables density. Identity tails use endpoint derivatives one. This construction isolates the spline mechanism.

The figure uses five predetermined knots to isolate the spline mechanism; it is a numerical construction rather than an additional trained model. The left panel shows the curve and knots, the middle verifies positive slope, and the right overlays five thousand transformed Gaussian samples with the change-of-variables density. A steep region spreads probability mass over a broader output range; a flatter region concentrates it. Across 1,401 test positions, the maximum inverse error is about 1.1×10⁻¹⁵. Finite-difference and analytic derivatives differ by at most about 4.5×10⁻¹⁰ away from knots.

A neural spline flow lets a conditioning network predict widths, heights, and derivatives, then uses transformations such as softmax or softplus to enforce positivity. Splines can be placed inside either coupling or autoregressive structures: the spline describes how an individual coordinate changes, while the outer structure specifies how its parameters depend on other coordinates. Image pixels introduce an additional discrete-to-continuous issue. A common approach adds uniform noise within integer bins and trains a continuous density. The original discrete pixel probability corresponds to an integral over its bin, rather than density evaluated at one point.

## 7 From many small transformations to a continuous flow

A discrete flow comprises identifiable invertible layers. A continuous normalizing flow supplies a time-dependent velocity field and moves points according to an ordinary differential equation. Under suitable existence and uniqueness conditions, a final point and the complete dynamics determine an initial point through backward integration. Probability mass remains conserved. Density changes according to whether a small surrounding volume expands or contracts, and this local expansion rate is the trace of the velocity Jacobian, also called its divergence.

$$
\frac{dx_t}{dt}=v_\theta(x_t,t),\qquad \frac{d\log p_t(x_t)}{dt}=-\operatorname{tr}\!\left(\frac{\partial v_\theta}{\partial x_t}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9afa3cb39c93766ce5e0d003.svg) | D-dimensional coordinate at time t, continuous time, D-dimensional velocity field, and its parameters; time and coordinates are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea03d1e0f61a4a14eff275ea.svg) | Density along the moving trajectory and total derivative following that trajectory. |
| ![Formula](https://ml-biomat.com/static/agent-math/d1bdb262be05fb4f5450d327.svg) | D×D velocity Jacobian and its diagonal sum; divergence has inverse-time units. |

For v=(0.4x₁,−0.2x₂), the Jacobian trace is 0.2, so log density falls by 0.2 over unit time. Coordinates scale by e^0.4 and e^(−0.2), giving area ratio e^0.2, canceled by density factor e^(−0.2). General neural fields require numerical integration together with accumulated density change.

Over a short time interval, the transformation is approximately the current coordinate plus velocity times the interval. Its Jacobian is correspondingly close to the identity plus the velocity Jacobian times that interval. The first-order volume change depends on the sum of diagonal entries. This connects the determinant used by discrete flows with the trace in the continuous density equation. FFJORD, released in 2018, uses stochastic trace estimation to reduce high-dimensional costs. Our two-dimensional example computes the complete trace directly, keeping coordinate and log-density changes easy to inspect.

![Left: analytic trajectory from (1,1) to time one under a linear velocity field. Right: actual maximum endpoint errors for RK4 with 1,2,4,8,16 steps, on logarithmic axes, compared against the analytic endpoint.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5f5b453a621f0a9ba54372d2.svg?v=5f5b453a621f)

Figure 5Left: analytic trajectory from (1,1) to time one under a linear velocity field. Right: actual maximum endpoint errors for RK4 with 1,2,4,8,16 steps, on logarithmic axes, compared against the analytic endpoint.

The example’s horizontal velocity is 0.4 times the horizontal coordinate, and its vertical velocity is −0.2 times the vertical coordinate. Starting from (1,1), the analytic endpoint at time one is approximately (1.491825,0.818731). Area grows by exp(0.2), so log density along the trajectory decreases by 0.2. One RK4 step gives maximum endpoint error about 9.14×10⁻⁵; sixteen steps reduce it to about 1.90×10⁻⁹. Mathematical invertibility and numerical integration accuracy are distinct quantities to inspect when choosing solver steps, tolerances, and computational budgets.

## 8 Use density to detect change and understand where mass lies

After learning the normal-data distribution, low-density locations can flag observations for investigation. We set a threshold at the lower five-percent quantile of validation log density, then freeze it. About 4.98% of independent normal test points are flagged. Shifting a separate independent sample upward by 1.5 leads to detection of about 97.66%. This experiment defines a specific change: the entire curved band moves vertically relative to its training location. The threshold is not selected using test anomalies, allowing normal flagging and detection of this particular shift to be interpreted together.

![Left: training/validation negative log density; dotted line is the true distribution scored on validation points. Middle: normal and vertically shifted score histograms with a validation-set threshold. Right: 64D Gaussian radius density, blue left axis, and point density relative to origin, orange right axis.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f696fde607b4869cbc913590.svg?v=f696fde607b4)

Figure 6Left: training/validation negative log density; dotted line is the true distribution scored on validation points. Middle: normal and vertically shifted score histograms with a validation-set threshold. Right: 64D Gaussian radius density, blue left axis, and point density relative to origin, orange right axis.

Density and probability mass remain different. A 64-dimensional standard Gaussian has its highest point density at the origin, yet most samples have radius near eight because vastly more locations are available farther from the origin. The blue curve plots density of the radius itself, while the dashed orange curve shows point density relative to the origin. They answer different questions. If an application concerns semantic classes, failure risk, or prohibited combinations, evaluation data must represent those outcomes. A low-density score first measures rarity under the learned coordinate distribution; the research task determines how that rarity contributes to a decision.

### Complete Python: train Real NVP, transform splines, and integrate a continuous flow

Run python main.py --output results --language en with NumPy, Matplotlib, and PyTorch. Explicit rules generate all data. The flow is trained; the spline and linear ODE are separate mechanism calculations. Outputs include weights, points, densities, grids, and five SVGs.

```
"""Eight affine coupling layers learn a known curved density.
Also compute rational-quadratic splines and a continuous linear flow.
"""
from pathlib import Path
import argparse,json,math,copy,platform
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
def banana(n,seed):
 z=np.random.default_rng(seed).normal(size=(n,2));return np.c_[1.2*z[:,0],.35*z[:,1]+.55*(z[:,0]**2-1)].astype('float32')
def true_logp(x):
 z=np.c_[x[:,0]/1.2,(x[:,1]-.55*((x[:,0]/1.2)**2-1))/.35];return -.5*(z*z).sum(1)-math.log(2*math.pi)-math.log(.42)
train,valid,test=banana(4096,350),banana(1024,351),banana(2048,352);xt=torch.tensor(train);xv=torch.tensor(valid);xe=torch.tensor(test)
class Coupling(nn.Module):
 def __init__(self,keep):
  super().__init__();self.keep=keep;self.change=1-keep;self.net=nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2));nn.init.zeros_(self.net[-1].weight);nn.init.zeros_(self.net[-1].bias)
 def forward(self,x,inverse=False):
  coeff=self.net(x[:,self.keep:self.keep+1]);s=.8*torch.tanh(coeff[:,0]);t=coeff[:,1];y=x.clone()
  if inverse:y[:,self.change]=x[:,self.change]*torch.exp(s)+t;ld=s
  else:y[:,self.change]=(x[:,self.change]-t)*torch.exp(-s);ld=-s
  return y,ld
class Flow(nn.Module):
 def __init__(self):super().__init__();self.layers=nn.ModuleList([Coupling(i%2) for i in range(8)])
 def forward(self,x,inverse=False):
  ld=x.new_zeros(len(x));layers=reversed(self.layers) if inverse else self.layers
  for layer in layers:x,delta=layer(x,inverse);ld=ld+delta
  return x,ld
 def logp(self,x):
  z,ld=self(x);return -.5*(z*z).sum(1)-math.log(2*math.pi)+ld
torch.manual_seed(355);model=Flow();optimizer=torch.optim.Adam(model.parameters(),lr=.001);rng=torch.Generator().manual_seed(356);history=[];best=float('inf');best_state=None;best_epoch=0
for epoch in range(1,201):
 order=torch.randperm(len(xt),generator=rng);total=0.
 for idx in order.split(256):
  loss=-model.logp(xt[idx]).mean();optimizer.zero_grad();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),5);optimizer.step();total+=loss.item()*len(idx)
 with torch.no_grad():val=-model.logp(xv).mean().item()
 history.append([epoch,total/len(xt),val])
 if val<best:best=val;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch
model.load_state_dict(best_state);model.eval();torch.save(dict(model=model.state_dict(),best_epoch=best_epoch),out/'realnvp.pt')
with torch.no_grad():
 test_lp=model.logp(xe).numpy();val_lp=model.logp(xv).numpy();latents=np.random.default_rng(357).normal(size=(2048,2)).astype('float32');generated=model(torch.tensor(latents),True)[0].numpy();encoded,forward_ld=model(xe);restored,inverse_ld=model(encoded,True);roundtrip=float((restored-xe).abs().max());logdet_cancel=float((forward_ld+inverse_ld).abs().max())
mean=train.mean(0);cov=np.cov(train.T);inv_cov=np.linalg.inv(cov)
def gaussian_logp(x):return -.5*np.einsum('ni,ij,nj->n',x-mean,inv_cov,x-mean)-math.log(2*math.pi)-.5*np.linalg.slogdet(cov)[1]
anomalies=banana(2048,353);anomalies[:,1]+=1.5;threshold=float(np.quantile(val_lp,.05))
with torch.no_grad():anomaly_lp=model.logp(torch.tensor(anomalies)).numpy()
# Verify the learned triangular Jacobian against a full autograd Jacobian.
double_model=copy.deepcopy(model).double();point=torch.tensor([.4,-.2],dtype=torch.float64,requires_grad=True)
jac=torch.autograd.functional.jacobian(lambda x:double_model(x[None])[0][0],point);jac_logdet=torch.linalg.slogdet(jac)[1].item();analytic_ld=double_model(point[None])[1].item()
# One-dimensional rational-quadratic spline, identity tails and endpoint derivatives one.
xknots=np.array([-3.,-1.,0.,1.,3.]);yknots=np.array([-3.,-2.,.5,2.,3.]);derivatives=np.array([1.,.5,2.,.5,1.])
def spline(values,inverse=False):
 values=np.asarray(values,dtype=float);bins=np.clip(np.searchsorted(yknots if inverse else xknots,values,side='right')-1,0,len(xknots)-2);x0=xknots[bins];y0=yknots[bins];w=np.diff(xknots)[bins];h=np.diff(yknots)[bins];delta=h/w;d0=derivatives[bins];d1=derivatives[bins+1]
 if inverse:
  rel=values-y0;a=rel*(d0+d1-2*delta)+h*(delta-d0);b=h*d0-rel*(d0+d1-2*delta);c=-delta*rel;disc=np.maximum(b*b-4*a*c,0);linear=np.abs(a)<1e-12;xi=np.zeros_like(values);np.divide(2*c,-b-np.sqrt(disc),out=xi,where=~linear);np.divide(-c,b,out=xi,where=linear);result=x0+w*xi
 else:xi=(values-x0)/w;den=delta+(d0+d1-2*delta)*xi*(1-xi);result=y0+h*(delta*xi*xi+d0*xi*(1-xi))/den
 den=delta+(d0+d1-2*delta)*xi*(1-xi);deriv=delta**2*(d1*xi**2+2*delta*xi*(1-xi)+d0*(1-xi)**2)/den**2;outside=(values<=-3)|(values>=3);result=np.where(outside,values,result);deriv=np.where(outside,1,deriv)
 return result,(-np.log(deriv) if inverse else np.log(deriv))
sx=np.linspace(-3.5,3.5,1401);sy,sld=spline(sx);sback,_=spline(sy,True);finite=(spline(sx+1e-5)[0]-spline(sx-1e-5)[0])/2e-5
interior=np.min(np.abs(sx[:,None]-xknots[None]),axis=1)>.001;spline_derivative_error=float(np.max(np.abs(finite[interior]-np.exp(sld[interior]))));spline_inverse_error=float(np.max(np.abs(sx-sback)))
sz=np.random.default_rng(358).normal(size=5000);sgen=spline(sz)[0];grid1=np.linspace(-4,4,1000);latent1,invld=spline(grid1,True);spline_pdf=np.exp(-.5*latent1**2)/math.sqrt(2*math.pi)*np.exp(invld)
# A continuous flow with analytic solution and a separately implemented RK4 solver.
A=np.diag([.4,-.2]);z0=np.array([1.,1.]);exact=z0*np.exp(np.diag(A));ode=[]
def rhs(state):return A@state
for n in [1,2,4,8,16]:
 x=z0.copy();dt=1/n
 for _ in range(n):
  k1=rhs(x);k2=rhs(x+.5*dt*k1);k3=rhs(x+.5*dt*k2);k4=rhs(x+dt*k3);x+=dt*(k1+2*k2+2*k3+k4)/6
 ode.append(dict(steps=n,x=x.tolist(),max_error=float(np.max(np.abs(x-exact))),logdensity_change=-float(np.trace(A))))
# Layer-by-layer grids and samples are computed by the actual learned inverse.
lines=[]
for fixed in np.linspace(-2,2,9):
 t=np.linspace(-2,2,41);lines.extend([np.c_[np.full(len(t),fixed),t],np.c_[t,np.full(len(t),fixed)]])
gridlines=np.array(lines).astype('float32');frames=[];cur=torch.tensor(gridlines.reshape(-1,2));points=torch.tensor(latents[:160]);probe=torch.tensor([[.5,-.5]],dtype=torch.float32);ld_probe=0.
with torch.no_grad():
 for layer_index,layer in enumerate([None]+list(reversed(model.layers))):
  if layer is not None:cur,_=layer(cur,True);points,_=layer(points,True);probe,dl=layer(probe,True);ld_probe+=dl.item()
  frames.append(dict(layer=layer_index,grid=cur.reshape(gridlines.shape).numpy().tolist(),points=points.numpy().tolist(),probe=probe[0].tolist(),probe_logdet=ld_probe))
hand_spline_y,hand_spline_ld=spline(np.array([-.5]));weights=[]
for layer in model.layers:
 weights.append(dict(keep=layer.keep,layers=[dict(weight=m.weight.detach().numpy().tolist(),bias=m.bias.detach().numpy().tolist()) for m in layer.net if isinstance(m,nn.Linear)]))
(out/'flow-lab.json').write_text(json.dumps(dict(frames=frames,weights=weights),separators=(',',':')),encoding='utf-8')
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=2048,seed=[350,351,352],true_logdet=math.log(.42)),training=dict(epochs=200,best_epoch=best_epoch,parameters=sum(p.numel() for p in model.parameters()),layers=8,batch=256,lr=.001,scale_bound=.8),density=dict(flow_test_nll=float(-test_lp.mean()),gaussian_test_nll=float(-gaussian_logp(test).mean()),true_test_nll=float(-true_logp(test).mean()),roundtrip_max_error=roundtrip,logdet_cancel_error=logdet_cancel,jacobian_logdet=jac_logdet,analytic_logdet=analytic_ld,jacobian_error=abs(jac_logdet-analytic_ld)),anomaly=dict(logdensity_threshold=threshold,false_positive=float((test_lp<threshold).mean()),shifted_detection=float((anomaly_lp<threshold).mean()),vertical_shift=1.5),spline=dict(inverse_max_error=spline_inverse_error,derivative_max_error=spline_derivative_error,min_derivative=float(np.exp(sld).min())),ode=ode,hand=dict(affine_scale=2,affine_point_density=1/(2*math.sqrt(2*math.pi)),coupling_logdet=math.log(2),spline_midpoint=float(hand_spline_y[0]),spline_midpoint_derivative=float(np.exp(hand_spline_ld[0])),ode_logdensity_change=-.2,ode_final_x1=float(exact[0]),ode_final_x2=float(exact[1])))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,validation=valid,test=test,latents=latents,generated=generated,encoded=encoded.numpy(),test_logdensity=test_lp,anomalies=anomalies,anomaly_logdensity=anomaly_lp,history=history,spline_x=sx,spline_y=sy,spline_logderivative=sld,spline_generated=sgen,ode=np.array([[r['steps'],r['max_error']] for r in ode]))
# Density is shown on one common coordinate grid and color scale.
gx,gy=np.meshgrid(np.linspace(-4,4,180),np.linspace(-2,5,160));mesh=np.c_[gx.ravel(),gy.ravel()].astype('float32')
with torch.no_grad():density=np.exp(model.logp(torch.tensor(mesh)).numpy()).reshape(gx.shape)
true_density=np.exp(true_logp(mesh)).reshape(gx.shape);fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
axs[0].scatter(test[:700,0],test[:700,1],s=5,alpha=.5,color='#b97d43');axs[0].scatter(generated[:700,0],generated[:700,1],s=4,alpha=.4,color='#125f82');axs[0].set_title(tr('A  目标与生成：各700点','A  Target and generated: 700 each'))
for ax,img,title in zip(axs[1:],[true_density,density],[tr('B  已知目标密度','B  Known target density'),tr('C  可逆网络密度','C  Learned flow density')]):
 im=ax.pcolormesh(gx,gy,img,vmin=0,vmax=max(true_density.max(),density.max()),cmap='YlGnBu',shading='auto',rasterized=True);ax.set_title(title);fig.colorbar(im,ax=ax,label=tr('每单位面积概率密度','Density per unit area'))
for ax in axs:ax.set(xlim=(-4,4),ylim=(-2,5),xlabel='x1',ylabel='x2');ax.set_aspect('equal')
save(fig,'density')
fig,axs=plt.subplots(1,4,figsize=(14,4),layout='constrained')
for ax,i in zip(axs,[0,2,4,8]):
 frame=frames[i]
 for line in frame['grid']:line=np.array(line);ax.plot(line[:,0],line[:,1],color='#125f82',lw=.7,alpha=.8)
 pt=np.array(frame['points']);ax.scatter(pt[:,0],pt[:,1],s=3,color='#c17a3a',alpha=.5);ax.set(xlim=(-5,5),ylim=(-3,7),xlabel=tr('坐标1','Coordinate 1'),ylabel=tr('坐标2','Coordinate 2'),title=tr('逆向层数 ','Inverse layers ')+str(i));ax.set_aspect('equal')
save(fig,'grids')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');axs[0].plot(sx,sy,color='#125f82');axs[0].scatter(xknots,yknots,color='#bf7139',s=30);axs[0].plot(sx,sx,ls=':',color='#8c9698');axs[0].set(xlabel='z',ylabel='x = f(z)',title=tr('A  单调有理二次样条','A  Monotone rational-quadratic spline'))
axs[1].plot(sx,np.exp(sld),color='#bf7139');axs[1].axhline(0,color='#777',lw=.7);axs[1].set(xlabel='z',ylabel="f'(z)",title=tr('B  每处斜率保持为正','B  Positive slope throughout'))
axs[2].hist(sgen,bins=70,density=True,color='#8fb9c1',alpha=.7,label=tr('5000个样本','5,000 samples'));axs[2].plot(grid1,spline_pdf,color='#125f82',label=tr('变量变换密度','Change-of-variables density'));axs[2].set(xlabel='x',ylabel=tr('概率密度','Density'),title=tr('C  拉伸改变密度','C  Stretching changes density'));axs[2].legend(fontsize=9);save(fig,'spline')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,1],label=tr('训练','Train'));axs[0].plot(h[:,0],h[:,2],label=tr('验证','Validation'));axs[0].axhline(-true_logp(valid).mean(),ls=':',color='#555',label=tr('目标本身','True density'));axs[0].set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('负对数密度 / nats','Negative log density / nats'),title=tr('A  最大似然训练','A  Maximum-likelihood training'));axs[0].legend(fontsize=9)
axs[1].hist(-test_lp,bins=np.histogram_bin_edges(np.r_[-test_lp,-anomaly_lp],bins=45),density=True,alpha=.55,label=tr('目标测试集','Target test'),color='#125f82');axs[1].hist(-anomaly_lp,bins=np.histogram_bin_edges(np.r_[-test_lp,-anomaly_lp],bins=45),density=True,alpha=.45,label=tr('向上移1.5','Shifted upward 1.5'),color='#bf7139');axs[1].axvline(-threshold,ls='--',color='#222');axs[1].set(xlabel=tr('负对数密度分数','Negative log-density score'),ylabel=tr('直方图密度','Histogram density'),title=tr('B  用验证集确定阈值','B  Threshold set on validation'));axs[1].legend(fontsize=9)
r=np.linspace(.001,13,600);log_shell=(64-1)*np.log(r)-.5*r*r-(64/2-1)*math.log(2)-math.lgamma(64/2);axs[2].plot(r,np.exp(log_shell),color='#125f82',label=tr('半径概率密度','Radius density'));axs[2].set(xlabel=tr('64维标准高斯半径','Radius in a 64D standard normal'),ylabel=tr('半径概率密度','Radial density'),title=tr('C  概率质量聚集在一圈','C  Probability mass occupies a shell'));ax2=axs[2].twinx();ax2.plot(r,np.exp(-.5*r*r),ls='--',color='#bf7139');ax2.set_ylabel(tr('相对原点的点密度','Point density relative to origin'),color='#bf7139');save(fig,'diagnostics')
fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');times=np.linspace(0,1,101);path=z0[None]*np.exp(times[:,None]*np.diag(A));axs[0].plot(path[:,0],path[:,1],color='#125f82',lw=3);axs[0].scatter([1,exact[0]],[1,exact[1]],c=['#bf7139','#125f82'],s=60);axs[0].set(xlabel='x1',ylabel='x2',title=tr('A  dx/dt = diag(0.4, −0.2)x','A  dx/dt = diag(0.4, -0.2)x'));axs[0].set_aspect('equal');axs[1].loglog([x['steps'] for x in ode],[x['max_error'] for x in ode],'o-',color='#125f82');axs[1].set(xlabel=tr('RK4步数','RK4 steps'),ylabel=tr('相对解析终点的最大绝对误差','Maximum absolute endpoint error'),title=tr('B  连续可逆性与数值误差','B  Continuous invertibility and numerical error'));save(fig,'ode')
print(json.dumps(summary,indent=2))
```

The complete program preserves training, validation, and test points; 2,048 generated points; layer-by-layer grids; model weights; and spline and ODE results. In the explorer, choose a Gaussian starting point and inspect its movement through successive inverse layers, comparing density with the local area ratio. Changing sensor units also changes numerical densities because coordinate volume carries units, so a threshold must remain consistent with preprocessing. A flow places sampling, density correction, and inverse recovery in one computable framework, allowing each relationship to be followed through the actual transformation.

This perspective also clarifies the relationship to other generative approaches. A VAE uses an inference distribution and a lower bound when its marginal density is difficult to compute. A GAN learns a sampler through an adversarial objective. A basic flow chooses an invertible equal-dimensional map so its density follows from volume accounting. These design decisions create different advantages for evaluation and generation. The most useful comparison starts with which quantities a particular application needs to sample, score, condition on, or recover.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M35.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Density Estimation Using Real NVP](https://arxiv.org/html/1605.08803v3)

   Change of variables, affine coupling, and invertible composition.

   Primary paper; no copied figures
2. [UvA Tutorial 11: Normalizing Flows for Image Modeling](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial11/NF_image_modeling.html)

   Original checkerboard figure, dequantization, and image-flow structure.

   MIT; original notebook cell33 execution14 mask output only
3. [Masked Autoregressive Flow for Density Estimation](https://arxiv.org/html/1705.07057v4)

   Dependency directions and computation in MAF versus IAF.

   Primary paper; no copied figures
4. [Improved Variational Inference with Inverse Autoregressive Flow](https://arxiv.org/abs/1606.04934)

   IAF parallel generation from known latent coordinates.

   Primary paper; no copied figures
5. [Neural Spline Flows](https://arxiv.org/html/1906.04032v2)

   Rational-quadratic splines, derivatives, and quadratic inversion.

   Primary paper; independent numerical construction
6. [FFJORD](https://arxiv.org/abs/1810.01367)

   Continuous flow, divergence, and trace estimation.

   Primary paper; no copied figures
7. [Do Deep Generative Models Know What They Don’t Know?](https://arxiv.org/abs/1810.09136)

   Distinguishing density estimation from out-of-distribution detection.

   Primary paper; own analytic Gaussian-shell illustration
