# How much probability lies in a valley? Energy models, score matching, and sampling

Source: https://ml-biomat.com/tutorials/machine-learning/m40/en/
Language: en

Turn energy differences into probabilities, then separate model shape, probability mass, and sampling coverage through real training and chains.

## Drawing a landscape that tells samples where to spend time

Choosing a chair involves load capacity, comfort, dimensions, and appearance. These requirements rarely specify one unique answer, but they can help compare candidate designs. An energy-based model takes a similar approach: it assigns a scalar energy to each complete candidate, with plausible samples in lower regions and less likely samples in higher regions. An image candidate contains all its pixels; a motion candidate may contain an entire joint trajectory. The network first learns to evaluate the candidate as a whole, after which search or stochastic sampling proposes new candidates.

The landscape analogy helps explain motion: the slope supplies a downhill direction, and valleys correspond to regions of higher density. Sampling also has a frequency requirement, however. Candidates should appear in the proportions assigned by the distribution. A ball that only rolls downhill will settle near a valley bottom and repeatedly produce almost the same answer. Random perturbations keep a particle moving around a valley and sometimes let it cross a ridge into another region. The learned landscape and the exploration process jointly determine what generated samples we actually observe.

Statistical physics uses energy and temperature to describe the relative occurrence of microscopic states. Machine learning inherits the idea of expressing global constraints through a scalar function. We will first distinguish energy from probability, then train a neural energy model on four point clusters with unequal weights. A correct model must find four valleys and allocate the right probability mass among them. This small setting makes partition functions, negative samples, mixing, and scores visible without hiding the central calculations behind a large image model.

![Iteration sequence in which neural-energy sampling develops digits from random pixels.](https://ml-biomat.com/static/tutorials/machine-learning/figures/236ace608adb1351f3b4456f.svg?v=236ace608adb)

Figure 1Original neural-energy sampling output from UvA Deep Learning Tutorials: random-pixel initialization gradually develops digit structure across the indicated iterations. Phillip Lippe and tutorial contributors, MIT, unmodified original notebook output. This is the source tutorial’s MNIST experiment; the chapter separately trains two-dimensional models to examine probability mass.

## Turning energy into probability requires a global total

Energy can be positive or negative and cannot be used directly as probability. Negating and exponentiating it gives a positive weight, larger for lower energies. Add the weights of all possible states, then divide each weight by that total. The total is the partition function. Discrete states use a sum; continuous coordinates use an integral. Normalization makes total probability one. A continuous density at a point can exceed one because probability is obtained by integrating over a region, not by interpreting the pointwise density as a standalone event probability.

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},\qquad Z_\theta=\int e^{-E_\theta(u)}\,du
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/450ec5d073fe8ccb5c2ec2a1.svg) | Sample coordinates, dummy integration coordinates, and parameters; x and u are dimensionless two-vectors here. |
| ![Formula](https://ml-biomat.com/static/agent-math/c7a2d1fed05fbe504fca30c8.svg) | Scalar dimensionless energy, natural-exponential base, partition function, and density; for dimensional coordinates, density has inverse-coordinate-volume units. |

Integration sums all positive weights, making the normalized density integrate to one; discrete states use a sum. Energies zero and ln2 yield weights one and one-half, total three-halves, and probabilities two-thirds and one-third. Physical energy U in joules becomes dimensionless E after division by k_B T, where k_B is Boltzmann’s constant and T absolute temperature. Our network energy is not measured in joules.

For two discrete states with energies zero and ln2, the weights are one and one-half, giving probabilities two-thirds and one-third. Adding seven to both energies multiplies both weights and their total by the same factor e^{−7}, leaving probabilities unchanged. The absolute energy zero is therefore adjustable; differences determine relative probabilities. Subtracting the minimum energy from each model’s landscape is useful for comparing its shape, but the resulting heights do not replace the model’s normalized probabilities. A visually deep valley may still occupy little probability mass if its volume is very small.

The difficulty in continuous spaces is the number of states. A small two-dimensional grid lets us add contributions from individual cells. Thousands of pixels, each with many possible values, make enumeration infeasible. A flexible energy network provides an easy way to score one candidate without automatically providing the total over the whole space. Training and sampling methods must therefore connect local evaluations with this global normalization requirement. Keeping both parts visible helps explain why a simple network output can lead to a demanding inference problem.

Valley depth and width must be considered together. Imagine two disjoint regions with approximately constant energy. The first has energy zero and area one; the second has energy ln2 and area four. Their integrated weights are approximately one and two, respectively. Despite its higher energy, the second region carries two-thirds of the normalized probability because it contains more available area. The deepest point alone cannot identify the region visited most often. In high-dimensional spaces, available volume has the same role. Attractive-looking minima therefore lead naturally to the next question: how much integrated probability does each surrounding region receive? Quadrature and regional sampling frequencies answer that question directly.

Temperature provides another connection to the physical picture. Holding a physical energy difference fixed, increasing temperature reduces the corresponding dimensionless difference and brings relative state weights closer together. Lowering temperature favors low-energy states more strongly. Machine learning commonly absorbs this scale into the network output; that is our fixed convention, so the numerical network energy is not in joules. Dividing a trained energy by an extra sampling temperature selects a new target distribution. A change in step size, by comparison, changes the discretized sampling process. Keeping these controls separate helps explain whether an observed change in the cloud comes from a deliberately different target or from numerical sampling behavior.

## Why training needs data and samples the model currently favors

Maximum likelihood seeks high probability for observed data. Substituting the energy distribution into negative log likelihood gives the data energy plus the logarithm of the partition function. Lowering data energy alone is insufficient: the network might also lower many other regions, increasing the total weight. Differentiating the complete objective yields an average parameter gradient over data minus an average parameter gradient over the model distribution. These contributions are commonly called the positive and negative phases. Their difference determines which relative energies should change, rather than merely shifting the entire landscape.

$$
L(\theta)=\mathbb E_{p_{\rm data}}[E_\theta(x)]+\log Z_\theta,\qquad \nabla_\theta L=\mathbb E_{p_{\rm data}}[\nabla_\theta E_\theta(x)]-\mathbb E_{p_\theta}[\nabla_\theta E_\theta(x)]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a07fca8b0d4692ec528a5732.svg) | Mean negative log density, natural logarithm, and expectation under its subscript distribution; L is in nats under fixed coordinate units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a8443011abc65f8fca430718.svg) | Data distribution, current model distribution, sample, and parameter vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/cd215d0ce220d9e9827a8a4f.svg) | Scalar energy, partition function, and parameter gradient, whose shape matches the parameters. |

Differentiating Z produces −∇E times exp(−E); dividing by Z turns the result into a model expectation. For E(0)=0,E(1)=θ, suppose data state one occurs with probability 0.8. At θ=0 the model probability is 0.5, so the gradient is 0.8−0.5=0.3. Gradient descent lowers θ and increases state one’s probability.

The positive phase pulls energy down near observed samples. The negative phase samples the model’s current beliefs and pushes against regions receiving excessive probability. Negative samples are therefore not manually labeled wrong answers, and they need not look absurd. They are candidates to which the model currently assigns probability. If those samples come from only one valley, training receives little information about probability allocated elsewhere. Sampling coverage enters the parameter update itself, rather than affecting only the final gallery of generated pictures.

In low dimensions, we can expose this calculation directly. One training method in this chapter sums weights on a 48×48 grid to approximate the partition function inside a window, allowing automatic differentiation through the full approximate likelihood. Another method approximates the negative phase with persistent stochastic chains. Both use the same network family and training data, then share a denser-grid validation measure. This arrangement compares their consequences on a common scale, instead of treating two differently defined training losses as if they measured the same quantity.

## Downhill motion plus noise: Langevin and acceptance correction

Each Langevin step moves against the energy gradient and adds a Gaussian perturbation. The gradient points toward increasing density; noise maintains exploration. Their scales must match. In our convention, deterministic motion is multiplied by step size, while noise standard deviation is the square root of twice that size. Changing noise amplitude arbitrarily changes the long-run distribution. Removing noise produces an optimization procedure for finding low-energy locations. Sampling instead retains fluctuations so that broad regions and distinct valleys can receive their appropriate share of visits.

$$
x_{k+1}=x_k-h\nabla_xE_\theta(x_k)+\sqrt{2h}\,\xi_k,\qquad \xi_k\sim\mathcal N(0,I_d)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9338ef5dbb88926a09481bfd.svg) | d-dimensional position at step k, discrete-step index, and dimension; d=2 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/9767612e4b8e0ed0506d92bf.svg) | Positive step size, position gradient, independent standard Gaussian d-vector per step, and d×d identity; coordinates and algorithmic time are dimensionless here. |

Drift and noise variance 2h are matched. For E=x²/2, the update is (1−h)x+√(2h)ξ. Stationary variance obeys V=(1−h)²V+2h, giving V=1/(1−h/2) for 0<h<2. At h=0.1 this is 1.05263 instead of the target one. Starting at x=1 with ξ=0 gives x_next=0.9; random noise can also move uphill.

The continuous-time Langevin process is connected to the target density, while a finite-step discretization introduces bias. The version without an acceptance correction is called ULA. For a standard Gaussian target, the energy gradient is position itself, so the discrete update becomes a linear random recurrence. Its stationary variance departs from the target as step size grows. Larger steps can move particles through space more quickly while broadening the clouds around valleys or eventually making the recursion unstable. A step-size choice therefore changes numerical behavior as well as apparent speed.

MALA adds a Metropolis–Hastings decision after the same Langevin proposal. It accounts for both the energy change and proposal probabilities in the two directions, making the target invariant under ideal exact computation. A rejected proposal leaves the chain at its previous location; this repeated position remains a valid state and must be included in sample statistics. High acceptance may simply reflect small moves. Acceptance correction addresses the stationary-distribution error of discretization, while the time needed to travel among valleys remains a separate mixing question.

$$
q(y\mid x)=\mathcal N\!\left(y;x-h\nabla E(x),2hI_d\right),\qquad A(x,y)=\min\!\left(1,\frac{e^{-E(y)}q(x\mid y)}{e^{-E(x)}q(y\mid x)}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/13679622cab1185145edc120.svg) | Current state, proposal, step size, dimensionality, and identity; x and y are d-vectors. |
| ![Formula](https://ml-biomat.com/static/agent-math/73a565bd58b87235bebdcfa6.svg) | Forward and reverse proposal densities, and Gaussian density evaluated at y with mean m and covariance C. |
| ![Formula](https://ml-biomat.com/static/agent-math/b32948f4104447a4407a7661.svg) | Energy, position gradient, acceptance probability between zero and one, and minimum; the partition function cancels in the ratio. |

Accept when an independent uniform draw is below A; otherwise repeat the current state. For E=x²/2,x=0,y=1,h=0.1, the energy increase is 0.5 and forward/reverse Gaussian exponent costs are 2.5 and 2.025. The log ratio is −0.5+2.5−2.025=−0.025, giving acceptance 0.97531. Gradient proposals are asymmetric, making the reverse density necessary.

Why compare the reverse proposal as well? On a slope, the proposal mean moves toward the valley. Proposing one location from another is therefore generally different from proposing the reverse move. An acceptance rule based on energy differences alone would count that proposal preference again. The reverse density compensates for this asymmetry so that equilibrium probability flows balance between the locations. Implementation can subtract log densities instead of dividing extremely small probabilities. Only energies and gradients at the two locations are needed, because the global normalization cancels. The worked Gaussian example above makes both proposal costs visible, showing exactly which terms the acceptance decision uses.

## Short chains and persistent chains change the learning problem

Contrastive-divergence work around 2000 offered a short-chain approach for models whose samplers were expensive to equilibrate. CD-k starts from observed data, takes k sampling steps under the current model, and uses the resulting states as negative-phase approximations. Starting near data can make a few steps informative about local changes. The finite-chain distribution still depends on those data initializations and generally differs from the model’s equilibrium distribution. Standard CD updates also stop differentiation through the sampling trajectory, treating the resulting negative states as fixed inputs for that gradient estimate.

$$
E_a(x)=\tfrac12ax^2,\qquad V_{\rm after}=(1-ha)^2V_{\rm data}+2h,\qquad a_{\rm CD1}=\frac{1-\sqrt{1-2h/V_{\rm data}}}{h}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dedaa4c24fe65cc4d1ba6815.svg) | Positive precision parameter, scalar energy, and one-dimensional position; model variance is 1/a. |
| ![Formula](https://ml-biomat.com/static/agent-math/b2c3ec66990d565b9912ff10.svg) | ULA step size, variance of zero-mean data, and variance after one update; all are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/eba6a38c1ebd54119c5fb882.svg) | Lower-precision root equating data and one-step negative-sample variances; requires 1−2h/V_data nonnegative. |

Since ∂E/∂a=x²/2, the CD gradient is half the difference between before/after variances. Setting it to zero and solving the quadratic gives the displayed root. V_data=1,h=0.1 yields a≈1.055728 and model variance≈0.947214. This fixed point belongs to data-initialized one-step ULA, differing from the exact maximum-likelihood precision one.

A Gaussian calculation makes the difference concrete. Let data variance be one, and model energy be an adjustable precision times half the squared position. If a single ULA step with size 0.1 supplies CD negatives, matching variances before and after the step gives precision about 1.05573. The model density then has variance about 0.94721. Applying this update to 200,000 actual Gaussian samples gives output variance approximately 1.00075. The one-step sample variance resembles the data even though the density defined by the learned parameter is shifted. Sampling dynamics and training fixed points are coupled.

Persistent contrastive divergence keeps chain states between parameter updates. Our PCD20 implementation stores 1,024 states, selects 128 at each update, advances twenty steps of size 0.02, and returns them to the buffer. Five percent are restarted from fresh Gaussian states. Restarts support exploration while defining a particular finite-chain approximation. Neural energy-model work in 2019 combined sample replay and gradient-based sampling for more complex images and trajectories. Its central computational problem is already present in our four valleys: the negative phase must represent what the model believes across the relevant space.

Cached states also age during training, because each parameter update changes their surrounding landscape. A persistent chain reuses these locations to track the changing model. Its effectiveness depends on how quickly parameters move relative to the sampler’s exploration. The code first generates negatives under the current fixed network, detaches their coordinates from the sampling computation graph, and then differentiates their energies with respect to model parameters. This implements the displayed expectation of an energy gradient under the current model. Backpropagating through the finite sampling path would add derivatives of the sampled coordinates with respect to parameters and produce a different update. Detaching preserves the specific maximum-likelihood negative-phase estimator being approximated here.

## Learning local directions without first evaluating the total

Differentiating log density with respect to position removes the partition function because that function depends on parameters, not the current sample location. This position gradient is the score, equal to negative energy gradient for an energy model. Two-dimensional inputs give two directional components; images give a component for every pixel. Keep two derivatives separate: parameter differentiation in likelihood training must retain the partition contribution, while position differentiation for a movement direction can eliminate it. Confusing these operations would remove an essential part of learning.

$$
s_\theta(x)=\nabla_x\log p_\theta(x)=-\nabla_xE_\theta(x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/323707e7bd0b4d5427a86d8d.svg) | Score vector, d-dimensional sample, and parameters; score has d components. |
| ![Formula](https://ml-biomat.com/static/agent-math/e3a619cc3dfeb4f60937fd04.svg) | Density, dimensionless energy, position gradient, and natural logarithm; for dimensional coordinates, score has inverse-coordinate units. |

Differentiate log p=−E−logZ with respect to x; logZ is constant in x. A standard Gaussian has score −2 at x=2, pointing toward zero. A variance-four Gaussian has score −0.5 there because relative density changes more gradually. A score is not a probability, and its magnitude does not directly report density.

Score matching in 2005 asked whether a model’s direction field could be fitted directly to the data direction field. The true score is unknown, but integration by parts rewrites the objective in terms of observed samples, the model score, and its divergence, under conditions such as vanishing boundary terms. This avoids explicit partition-function evaluation. When score is defined as the gradient of a scalar energy, it automatically has the corresponding gradient-field structure. An arbitrary vector-predicting network needs the probability interpretation appropriate to its chosen model; not every unconstrained field is the gradient of one scalar log density.

$$
J(\theta)=\mathbb E_{p_{\rm data}}\!\left[\tfrac12\|s_\theta(x)\|^2+\nabla_x\cdot s_\theta(x)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7c451a648435d5ef8afa031d.svg) | Score-matching objective after dropping a parameter-independent constant, and data expectation; J may be negative. |
| ![Formula](https://ml-biomat.com/static/agent-math/7342c62a4d51a2e06ca208e9.svg) | d-dimensional score, parameters, d-dimensional position, and sum of squared components. |
| ![Formula](https://ml-biomat.com/static/agent-math/f356b92922d2e360cc410073.svg) | Divergence, the sum of each component’s derivative with respect to its matching coordinate; it has inverse-squared-coordinate units like the squared score. |

Expand squared distance between model and true scores, then integrate the cross term by parts. Smoothness, integrability, and vanishing boundary terms are required. For s=−ax and data variance V, J=a²V/2−a and its derivative is aV−1. The optimum is a=1/V; V=4 gives a=0.25 without first computing Z.

Denoising score matching makes labels easier to construct. Add known Gaussian noise to a clean sample, calculate the corruption distribution’s conditional score, and regress a network against it. The optimal conditional average is the score of the smoothed noisy-data distribution. Work connecting denoising and score matching in 2011 clarified this relationship; later multi-noise generation methods used related directions at several smoothing levels. The label is available because the corruption is chosen by us, while averaging over possible clean samples supplies the marginal direction needed for a distribution.

$$
\tilde x=x+\sigma\epsilon,\quad\epsilon\sim\mathcal N(0,I_d),\qquad L_{\rm DSM}=\mathbb E\!\left[\frac1d\left\|s_\theta(\tilde x)+\frac{\epsilon}{\sigma}\right\|^2\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/04e62bfffa527fbd0014154a.svg) | Clean sample, noisy sample, independent standard Gaussian noise, and dimension; the first three are d-vectors. |
| ![Formula](https://ml-biomat.com/static/agent-math/6166be0d8610833c0bef4930.svg) | Positive noise standard deviation, predicted score at the noisy input, and parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/451a5c7f5f37caedca8b44d7.svg) | Denoising-score squared loss, expectation over data and noise, and per-coordinate averaging; units are squared-score units. |

The Gaussian conditional score is −(x̃−x)/σ²=−ε/σ, a known target. The squared-loss conditional mean equals the smoothed marginal score. Clean N(0,1) with σ=0.5 gives noisy N(0,1.25) and score −0.8x̃. A single x=1,ε=2 produces x̃=2 and target −4; averaging possible clean origins recovers the marginal direction.

The program corrupts 200,000 standard Gaussian samples with noise of standard deviation 0.5. Noisy variance is 1.25, so the true score slope is −0.8. Fitting a single linear coefficient gives approximately −0.80221. It is shallower than the clean distribution’s slope −1 because corruption broadens the distribution. The example shows how denoising labels learn a meaningful marginal direction, while identifying exactly which distribution is learned. A fixed noise level yields a smoothed density; recovering finer structure requires information appropriate to smaller noise levels or another model component.

## The complete experiment: landscapes and probability mass

The target contains four Gaussian components centered at combinations of ±1.2 in the two coordinates. Each coordinate has standard deviation 0.32, and component weights are 0.55, 0.25, 0.15, and 0.05. Independent seeds create 4,096 training points and 1,024 each for validation and testing. Two hidden tanh layers of width 32 map position to a scalar, to which half the squared coordinate norm is added. The model has 1,185 parameters. The quadratic term raises energy far away, while the bounded hidden-network output provides local landscape variation.

![Left: known target relative-energy surface after subtracting its window minimum. Middle/right: window-normalized densities of two actually trained models, using a separate density color scale. Orange marks 150 fixed held-out samples; coordinates are dimensionless.](https://ml-biomat.com/static/tutorials/machine-learning/figures/7b4c1edade59c060e211da30.svg?v=7b4c1edade59)

Figure 2Left: known target relative-energy surface after subtracting its window minimum. Middle/right: window-normalized densities of two actually trained models, using a separate density color scale. Orange marks 150 fixed held-out samples; coordinates are dimensionless.

GridMLE and PCD20 each run for 2,000 parameter updates, selecting validation-best checkpoints at updates 2,000 and 600 respectively. Grid likelihood uses the square [−4,4]². Evaluation uses a 160×160 midpoint grid and is repeated on a 240×240 grid. Expanding the square to [−6,6]² changes log partition estimates by approximately 1.72×10^{−5} and 6.29×10^{−5}. These checks assess the window and resolution for this particular low-dimensional experiment and define the scope of the reported negative log-density values.

$$
\widehat Z_W=\Delta A\sum_{j=1}^{G^2}e^{-E_\theta(u_j)},\quad\log\widehat Z_W=\log\Delta A+\operatorname{logsumexp}_j[-E_\theta(u_j)],\quad\Delta A=(8/G)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/40325612353eae0022304974.svg) | Integration window [−4,4]², grid count per axis, grid index, and two-dimensional midpoint. |
| ![Formula](https://ml-biomat.com/static/agent-math/eb70ebc658c338a54a648e45.svg) | Midpoint approximation of the window partition function, cell area, and network energy; Z has area units. |
| ![Formula](https://ml-biomat.com/static/agent-math/61ac3ada8b31d719b9cbd211.svg) | Stable log-of-summed-exponentials operation and natural logarithm. |

Approximate each cell’s integral by its midpoint weight times area. G=48 yields 2,304 cells of area 1/36. If energy is zero throughout the window, Z=2304/36=64, the window area, and density is 1/64. Stable logsumexp subtracts the maximum input before exponentiation. Window integration differs from integration over the entire space.

Test-window negative log densities are approximately 1.7951 and 1.9903. GridMLE assigns quadrant masses approximately 0.5471, 0.2518, 0.1542, and 0.0469; PCD20 gives 0.6831, 0.2004, 0.0943, and 0.0222. Both networks form four valleys, but the latter overallocates probability to the first one. Gaussian tails cross coordinate axes slightly, so the code calculates exact target quadrant probabilities using Gaussian distribution functions before comparison. Component weights and quadrant masses are very close here, but they are not mathematically identical.

![Left: fixed validation-window negative log density versus updates. Middle: known quadrant masses and model quadrature masses. Right: final states of 512 MALA chains after 1,000 steps on GridMLE energy with h=0.03. The finite sample cloud and model-integrated masses are separate quantities.](https://ml-biomat.com/static/tutorials/machine-learning/figures/da0db72301233eeab457a589.svg?v=da0db7230123)

Figure 3Left: fixed validation-window negative log density versus updates. Middle: known quadrant masses and model quadrature masses. Right: final states of 512 MALA chains after 1,000 steps on GridMLE energy with h=0.03. The finite sample cloud and model-integrated masses are separate quantities.

Grid integration is a low-dimensional checking tool. Forty-eight points per coordinate require 2,304 locations in two dimensions but 48 to the tenth power in ten dimensions. High-dimensional methods instead use sampling, structural assumptions, or alternative learning objectives. We retain the grid to examine the model separately from its sampler. The full program saves original samples, weights, chain trajectories, probability masses, and a finite-difference check of the known target gradient. These outputs allow the landscape, normalization, and observed sampling frequencies to be inspected independently.

### Complete Python: energy training, quadrature, and chain diagnostics

Requires NumPy, PyTorch, and Matplotlib. Run python main.py --output results --language en to train both energy networks and save original data, all chain trajectories, weights, numerical summaries, and four scientific figure groups.

```
"""Neural energies, positive/negative phases, and honest sampling diagnostics."""
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
centers=np.array([[-1.2,-1.2],[1.2,-1.2],[1.2,1.2],[-1.2,1.2]]);weights=np.array([.55,.25,.15,.05]);sigma=.32;variance=sigma*sigma
signs=np.array([[-1,-1],[1,-1],[1,1],[-1,1]]);quadrant_weights=np.array([sum(w*math.prod(.5*(1+math.erf(float(sign[j]*mu[j])/(sigma*math.sqrt(2)))) for j in range(2)) for w,mu in zip(weights,centers)) for sign in signs])
def sample_data(n,seed):
 r=np.random.default_rng(seed);labels=r.choice(4,n,p=weights);return (centers[labels]+r.normal(0,sigma,(n,2))).astype('float32'),labels
def true_energy_gradient(x):
 delta=x[:,None]-centers[None];logterms=np.log(weights)[None]-np.sum(delta*delta,2)/(2*variance)-math.log(2*math.pi*variance);maximum=logterms.max(1,keepdims=True);responsibility=np.exp(logterms-maximum);total=responsibility.sum(1,keepdims=True);e=-maximum[:,0]-np.log(total[:,0]);responsibility/=total;gradient=(responsibility[:,:,None]*delta).sum(1)/variance;return e,gradient
train,train_labels=sample_data(4096,400);valid,valid_labels=sample_data(1024,401);test,test_labels=sample_data(1024,402);xt=torch.tensor(train)
class Energy(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(2,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))
 def forward(self,x):return self.net(x).flatten()+.5*x.square().sum(1)
def midpoint_grid(limit,n):
 a=-limit+(np.arange(n)+.5)*(2*limit/n);xx,yy=np.meshgrid(a,a);return np.c_[xx.ravel(),yy.ravel()].astype('float32'),(2*limit/n)**2
grid_train,cell_train=midpoint_grid(4,48);grid_eval,cell_eval=midpoint_grid(4,160);gt=torch.tensor(grid_train);ge=torch.tensor(grid_eval)
def logZ(m,g,cell):return torch.logsumexp(-m(g),0)+math.log(cell)
def langevin_torch(m,x,steps,h,rng):
 for _ in range(steps):
  x=x.detach().requires_grad_(True);gradient=torch.autograd.grad(m(x).sum(),x)[0];x=(x-h*gradient+math.sqrt(2*h)*torch.randn(x.shape,generator=rng)).detach()
 return x
models={};histories={};training={}
for name,seed in [('GridMLE',403),('PCD20',404)]:
 torch.manual_seed(seed);m=Energy();opt=torch.optim.Adam(m.parameters(),lr=.001);rng=torch.Generator().manual_seed(seed+100);buffer=1.5*torch.randn((1024,2),generator=rng);history=[];best=float('inf');best_state=None
 for step in range(1,2001):
  idx=torch.randint(len(xt),(128,),generator=rng);positive=m(xt[idx]);negative_mean=0.
  if name=='GridMLE':loss=positive.mean()+logZ(m,gt,cell_train)
  else:
   ids=torch.randperm(len(buffer),generator=rng)[:128];negative=buffer[ids].clone();restart=torch.rand((128,),generator=rng)<.05;negative[restart]=1.5*torch.randn((int(restart.sum()),2),generator=rng);negative=langevin_torch(m,negative,20,.02,rng);buffer[ids]=negative;negative_energy=m(negative.detach());negative_mean=negative_energy.mean().item();loss=positive.mean()-negative_energy.mean()
  opt.zero_grad();loss.backward();opt.step()
  if step%100==0:
   with torch.no_grad():z=logZ(m,ge,cell_eval);validation_nll=(m(torch.tensor(valid)).mean()+z).item()
   history.append([step,loss.item(),validation_nll,positive.mean().item(),negative_mean])
   if validation_nll<best:best=validation_nll;best_step=step;best_state=copy.deepcopy(m.state_dict())
 m.load_state_dict(best_state);m.eval();models[name]=m;histories[name]=history;training[name]=dict(updates=2000,best_step=best_step,validation_window_nll=best,parameters=sum(p.numel() for p in m.parameters()),seed=seed);torch.save(dict(model=m.state_dict(),best_step=best_step),out/f'{name.lower()}.pt')
def model_eg(m,x):
 a=torch.tensor(x,dtype=torch.float32,requires_grad=True);e=m(a);g=torch.autograd.grad(e.sum(),a)[0];return e.detach().numpy().astype('float64'),g.detach().numpy().astype('float64')
def quadrants(x):return np.where(x[:,1]<0,np.where(x[:,0]<0,0,1),np.where(x[:,0]>0,2,3))
def chain(eg,h,steps,initial,seed,method='ULA',record_every=10):
 rng=np.random.default_rng(seed);x=np.array(initial,dtype='float64');path=[x.copy()];accepted=0;switches=np.zeros(len(x),dtype=int);counts=np.zeros(4,dtype='int64');occupancies=[];e,g=eg(x)
 for step in range(1,steps+1):
  proposal=x-h*g+math.sqrt(2*h)*rng.normal(size=x.shape);pe,pg=eg(proposal)
  if method=='MALA':
   forward=np.sum((proposal-x+h*g)**2,1)/(4*h);backward=np.sum((x-proposal+h*pg)**2,1)/(4*h);logratio=-pe+e+forward-backward;accept=np.log(rng.uniform(size=len(x)))<np.minimum(0,logratio)
  else:accept=np.ones(len(x),dtype=bool)
  previous=quadrants(x);x[accept]=proposal[accept];e[accept]=pe[accept];g[accept]=pg[accept];accepted+=int(accept.sum());switches+=(previous!=quadrants(x))
  if step>steps//2:counts+=np.bincount(quadrants(x),minlength=4)
  if step%record_every==0:path.append(x.copy());occupancies.append(np.bincount(quadrants(x),minlength=4)/len(x))
 return x,np.array(path),dict(acceptance=accepted/(steps*len(x)),final_weights=(np.bincount(quadrants(x),minlength=4)/len(x)).tolist(),second_half_weights=(counts/counts.sum()).tolist(),total_variation=float(.5*np.abs(counts/counts.sum()-quadrant_weights).sum()),chains_ever_switched=float((switches>0).mean()),mean_switches=float(switches.mean()),steps=steps,h=h,method=method),np.array(occupancies)
initials=dict(one=np.repeat(centers[:1],128,axis=0),spread=centers[np.arange(128)%4].copy());runs={};paths={};occupancies={}
for name,h,initial,method in [('small_one',.005,'one','ULA'),('small_spread',.005,'spread','ULA'),('medium_spread',.04,'spread','ULA'),('large_spread',.16,'spread','ULA'),('mala_spread',.16,'spread','MALA')]:
 x,path,stat,occ=chain(true_energy_gradient,h,2000,initials[initial],405,method);runs[name]=stat;paths[name]=path;occupancies[name]=occ
model_stats={};densities={};neural_paths={};neural_samples={};initial_rng=np.random.default_rng(406);neural_initial=initial_rng.normal(0,1.5,(512,2))
for name,m in models.items():
 with torch.no_grad():eg=m(ge).numpy().astype('float64');z=logZ(m,ge,cell_eval).item();density=np.exp(-eg-z);test_nll=float(m(torch.tensor(test)).mean()+z)
 density_weights=np.array([density[quadrants(grid_eval)==c].sum()*cell_eval for c in range(4)]);densities[name]=dict(energy=eg,density=density)
 x,path,stat,_=chain(lambda a:model_eg(m,a),.03,1000,neural_initial,407,'MALA',20);neural_paths[name]=path;neural_samples[name]=x
 extended,extended_cell=midpoint_grid(6,240)
 with torch.no_grad():extended_logz=logZ(m,torch.tensor(extended),extended_cell).item();fine,fc=midpoint_grid(4,240);fine_logz=logZ(m,torch.tensor(fine),fc).item()
 stat['TV_from_model_quadrature']=float(.5*np.abs(np.array(stat['second_half_weights'])-density_weights).sum())
 model_stats[name]=dict(window_test_nll=test_nll,logZ_window=z,normalization_sum=float(density.sum()*cell_eval),quadrant_mass=density_weights.tolist(),quadrant_mass_TV=float(.5*np.abs(density_weights-quadrant_weights).sum()),window_logZ_refinement=abs(fine_logz-z),extended_logZ_difference=extended_logz-z,sampling=stat)
# Analytic CD1 fixed point for a Gaussian energy, and sampled denoising-score regression.
r=np.random.default_rng(408);clean=r.normal(size=200000);eps=r.normal(size=len(clean));noise_sigma=.5;noisy=clean+noise_sigma*eps;dsm_a=float(np.dot(noisy,eps/noise_sigma)/np.dot(noisy,noisy));h=.1;cd_precision=(1-math.sqrt(1-2*h))/h;cd_step=(1-h*cd_precision)*clean+math.sqrt(2*h)*r.normal(size=len(clean));gpoints=np.array([[.3,.7],[-.2,-1.1],[1.3,.9]]);analytic=true_energy_gradient(gpoints)[1];finite=np.empty_like(analytic)
for j in range(2):
 offset=np.zeros_like(gpoints);offset[:,j]=1e-5;finite[:,j]=(true_energy_gradient(gpoints+offset)[0]-true_energy_gradient(gpoints-offset)[0])/(2e-5)
single=np.array([[.5,-.25]]);neural_energy,neural_grad=model_eg(models['GridMLE'],single)
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=1024,weights=weights.tolist(),quadrant_weights=quadrant_weights.tolist(),sigma=sigma,seeds=[400,401,402]),training=training,models=model_stats,known_target_chains=runs,score_matching=dict(noise_sigma=noise_sigma,fit_precision=dsm_a,true_smoothed_precision=.8,samples=len(clean)),hand=dict(two_state_probability=[2/3,1/3],probability_ratio=2.,constant_shift=7.,cd1_precision=cd_precision,cd1_model_variance=1/cd_precision,cd1_actual_step_variance=float(cd_step.var()),true_gradient_max_error=float(np.max(np.abs(analytic-finite))),neural_probe_energy=float(neural_energy[0]),neural_probe_gradient=neural_grad[0].tolist()),domain=dict(training_window=[-4,4],training_grid=48,evaluation_grid=160,refinement_grid=240,extended_window=[-6,6]))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,train_labels=train_labels,validation=valid,test=test,grid=grid_eval,true_density=np.exp(-true_energy_gradient(grid_eval)[0]),clean_score_samples=clean,noisy_score_samples=noisy,score_noise=eps,cd1_samples=cd_step,neural_initial=neural_initial,**{n+'_history':np.array(v) for n,v in histories.items()},**{n+'_energy':d['energy'] for n,d in densities.items()},**{n+'_density':d['density'] for n,d in densities.items()},**{n+'_samples':v for n,v in neural_samples.items()},**{n+'_chain':v for n,v in paths.items()},**{n+'_occupancy':v for n,v in occupancies.items()},**{n+'_neural_chain':v for n,v in neural_paths.items()})
lab_grid,lab_cell=midpoint_grid(4,60);known_e=true_energy_gradient(lab_grid)[0];learned_e=model_eg(models['GridMLE'],lab_grid)[0];lab=dict(centers=centers.tolist(),weights=weights.tolist(),variance=variance,grid=lab_grid.tolist(),cell=lab_cell,quadrant_weights=quadrant_weights.tolist(),learned_quadrant_weights=model_stats['GridMLE']['quadrant_mass'],energies={'True':known_e.tolist(),'Learned':learned_e.tolist()},logZ={'True':0.,'Learned':model_stats['GridMLE']['logZ_window']},network={k:v.detach().numpy().tolist() for k,v in models['GridMLE'].state_dict().items()});(out/'lab-data.json').write_text(json.dumps(lab,separators=(',',':')),encoding='utf-8')
fig=plt.figure(figsize=(13,4.8),layout='constrained');ax=fig.add_subplot(131,projection='3d');small,_=midpoint_grid(3,70);truee=true_energy_gradient(small)[0];xx=small[:,0].reshape(70,70);yy=small[:,1].reshape(70,70);ax.plot_surface(xx,yy,(truee-truee.min()).reshape(70,70),cmap='viridis',linewidth=0,rasterized=True);ax.set(xlabel='x1',ylabel='x2',zlabel='',title=tr('A  已知目标：相对能量','A  Target: relative energy'));ax.view_init(35,-55)
for j,name in enumerate(['GridMLE','PCD20']):
 ax=fig.add_subplot(1,3,j+2);im=ax.imshow(densities[name]['density'].reshape(160,160),origin='lower',extent=(-4,4,-4,4),cmap='YlGnBu',vmin=0,vmax=1);ax.scatter(test[:150,0],test[:150,1],s=3,color='#b96f3b',alpha=.35);ax.set(xlabel='x1',ylabel='x2',title=name+tr('：窗口归一化密度',': window-normalized density'));fig.colorbar(im,ax=ax,label=tr('每单位面积密度','Density per unit area'),shrink=.65)
save(fig,'landscape')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
for name,color in [('GridMLE','#125f82'),('PCD20','#bf7139')]:
 hh=np.array(histories[name]);axs[0].plot(hh[:,0],hh[:,2],label=name,color=color)
axs[0].set(xlabel=tr('参数更新次数','Parameter updates'),ylabel=tr('验证窗口负对数密度','Validation window NLL'),title=tr('A  统一验证尺度','A  Shared validation measure'));axs[0].legend(fontsize=9)
ind=np.arange(4);axs[1].bar(ind-.25,quadrant_weights,.25,label=tr('目标','Target'),color='#526b59');axs[1].bar(ind,model_stats['GridMLE']['quadrant_mass'],.25,label='GridMLE',color='#125f82');axs[1].bar(ind+.25,model_stats['PCD20']['quadrant_mass'],.25,label='PCD20',color='#bf7139');axs[1].set(xticks=ind,xlabel=tr('象限类别','Quadrant class'),ylabel=tr('概率质量','Probability mass'),title=tr('B  网格积分得到的质量','B  Mass from quadrature'));axs[1].legend(fontsize=8)
axs[2].scatter(*neural_samples['GridMLE'].T,s=5,alpha=.45,color='#125f82');axs[2].set(xlim=(-4,4),ylim=(-4,4),xlabel='x1',ylabel='x2',title=tr('C  GridMLE的512条MALA终点','C  512 MALA endpoints for GridMLE'));axs[2].set_aspect('equal');save(fig,'learning')
labels={'small_one':tr('ULA h=0.005，单谷起点','ULA h=0.005, one valley'),'small_spread':tr('ULA h=0.005，四谷均分','ULA h=0.005, spread'),'medium_spread':tr('ULA h=0.04，四谷均分','ULA h=0.04, spread'),'large_spread':tr('ULA h=0.16，四谷均分','ULA h=0.16, spread'),'mala_spread':tr('MALA h=0.16，四谷均分','MALA h=0.16, spread')}
fig,axs=plt.subplots(2,3,figsize=(13,7.4),layout='constrained');names=list(runs)
for ax,name in zip(axs.flat,names):
 pp=paths[name];ax.plot(pp[:,0,0],pp[:,0,1],lw=.8,color='#bf7139',alpha=.8);ax.scatter(*pp[-1].T,s=6,color='#125f82',alpha=.6);ax.scatter(*centers.T,marker='+',color='#111',s=55);ax.set(xlim=(-4,4),ylim=(-4,4),xlabel='x1',ylabel='x2',title=f"{labels[name]}\nTV={runs[name]['total_variation']:.3f}");ax.set_aspect('equal')
axs[1,2].axis('off');axs[1,2].bar(np.arange(4),quadrant_weights,color=['#125f82','#bf7139','#63864b','#755c8b']);axs[1,2].axis('on');axs[1,2].set(xticks=range(4),xlabel=tr('象限类别','Quadrant class'),ylabel=tr('真实概率质量','True mass'),title=tr('已知目标：0.55 / 0.25 / 0.15 / 0.05','Known target: 0.55 / 0.25 / 0.15 / 0.05'));save(fig,'mixing')
fig,axs=plt.subplots(1,3,figsize=(13,4.2),layout='constrained')
for name,color in [('small_one','#125f82'),('small_spread','#bf7139'),('mala_spread','#63864b')]:
 occ=occupancies[name];axs[0].plot(np.arange(1,len(occ)+1)*10,occ[:,0],label=labels[name],color=color)
axs[0].axhline(quadrant_weights[0],color='#333',ls='--');axs[0].set(xlabel=tr('采样步数','Sampling steps'),ylabel=tr('最重象限的链比例','Fraction of chains in heaviest quadrant'),title=tr('A  初始化影响多久','A  Persistence of initialization'));axs[0].legend(fontsize=8)
for name,color in [('small_spread','#bf7139'),('mala_spread','#63864b')]:
 values=paths[name][:,0,0].copy();values-=values.mean();denom=np.dot(values,values);corr=[np.dot(values[:len(values)-lag],values[lag:])/denom if denom else float('nan') for lag in range(41)];axs[1].plot(np.arange(41)*10,corr,color=color,label=labels[name])
axs[1].set(xlabel=tr('间隔 / 采样步','Lag / sampling steps'),ylabel=tr('首链x1自相关','First-chain x1 autocorrelation'),title=tr('B  相邻样本的依赖','B  Dependence of successive samples'));axs[1].legend(fontsize=8)
q=np.linspace(-3,3,200);axs[2].plot(q,-q,label=tr('干净N(0,1) score','Clean N(0,1) score'),color='#bf7139');axs[2].plot(q,-.8*q,label=tr('加噪真实score','True noisy score'),color='#333');axs[2].plot(q,-dsm_a*q,'--',label=tr('DSM回归','DSM regression'),color='#125f82');axs[2].set(xlabel='x',ylabel='score',title=tr('C  去噪学习的是平滑密度','C  Denoising learns a smoothed density'));axs[2].legend(fontsize=8);save(fig,'diagnostics');print(json.dumps(summary,indent=2))
```

## Moving inside a valley differs from visiting all valleys

Sampling a completely known target energy first removes fitting error from the experiment. With all 128 chains initialized in the heaviest valley, ULA at step size 0.005 still spends about 95.5% of second-half states in that quadrant after 2,000 steps, compared with a target near 55.0%. Starting equal numbers in all four valleys instead gives about 27.9% there. Different initializations lead to different finite-run results, showing persistent memory of starting locations. Clouds can look plausible inside each valley while carrying incorrect population weights across valleys.

![Five initializations, step sizes, and methods on the fully known target energy. Each shows 128 final states after 2,000 steps and the first chain trajectory. Title TV uses all second-half states. Final panel shows exact target quadrant masses in lower-left, lower-right, upper-right, upper-left order.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5b66174f367cf01f0ccacf84.svg?v=5b66174f367c)

Figure 4Five initializations, step sizes, and methods on the fully known target energy. Each shows 128 final states after 2,000 steps and the first chain trajectory. Title TV uses all second-half states. Final panel shows exact target quadrant masses in lower-left, lower-right, upper-right, upper-left order.

Increasing step size to 0.16 makes ULA switch quadrants frequently, averaging about 168 switches per chain, yet quadrant total-variation distance remains about 0.229. MALA at the same size accepts about 43.2% of proposals and corrects the proposal’s equilibrium bias, but its 2,000-step quadrant distance is about 0.256 because cross-valley exploration remains slow. Frequent motion, high acceptance, and a picture containing four clusters answer different questions. Total variation here is half the sum of absolute differences among four quadrant probabilities, measuring mass allocation at that particular regional resolution.

For the learned GridMLE energy, quadrature masses differ from the target by only about 0.006 in total variation. Yet 512 fresh Gaussian starts followed by 1,000 MALA steps produce second-half masses about 0.099 away from that model’s quadrature masses. The landscape assigns reasonable weights, while finite sampling has not realized them fully. Trajectories, regional occupancies, and autocorrelation should therefore be examined together. Coordinates may decorrelate within a valley while the chain rarely visits other valleys. Multiple initializations, cross-region round trips, and longer-run distribution comparisons provide concrete follow-up checks.

![Left: instantaneous occupancy of the heaviest quadrant among 128 chains and target probability. Middle: first-chain x₁ autocorrelation, recorded every ten steps with lag converted to actual steps and full centered sum of squares as denominator. Right: denoising-score regression on 200,000 points against clean and noisy analytic Gaussian scores.](https://ml-biomat.com/static/tutorials/machine-learning/figures/85ccebf5131f579c9eff3d61.svg?v=85ccebf5131f)

Figure 5Left: instantaneous occupancy of the heaviest quadrant among 128 chains and target probability. Middle: first-chain x₁ autocorrelation, recorded every ten steps with lag converted to actual steps and full centered sum of squares as denominator. Right: denoising-score regression on 200,000 points against clean and noisy analytic Gaussian scores.

## Let the chains move: one energy, different exploration

Sixteen chains use fixed seed 4001, with complete ULA or MALA steps computed in your browser. Switch between the known target and actually trained GridMLE energy. Energy and density backgrounds have distinct meanings. Changing model, step size, or initialization starts a fresh run.

[Figure: Energy or density background, sixteen chains, and quadrant masses](https://ml-biomat.com/tutorials/machine-learning/m40/en/#M40-board)

Blue points show sixteen current states; red traces the first chain. Gray bars represent the chosen energy’s quadrant masses; blue bars accumulate sixteen states at every step, including repeated states after rejection and the initial transient. Axes expand when needed beyond the background window, and all locations remain in probability counts.

## Connecting classification scores, energy, and diffusion

A classifier’s logits can be interpreted as negative joint energies for input–class pairs. Given an input, normalizing over the finite class set reproduces softmax. Summing over classes also defines an unnormalized input score. The Joint Energy-based Model work introduced in 2019 used this connection to combine discriminative and generative learning. Classification accuracy alone does not determine the input density, however. The conditional probabilities constrain relative class scores at each input while leaving certain input-dependent changes unconstrained. This freedom matters when trying to generate inputs from a classifier.

$$
E(x,y)=-f_y(x),\qquad p(y\mid x)=\frac{e^{f_y(x)}}{\sum_c e^{f_c(x)}},\qquad E_{\rm input}(x)=-\log\sum_c e^{f_c(x)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fefe874b2667ea8d6da93133.svg) | Input vector, class label, and summation index across all classes. |
| ![Formula](https://ml-biomat.com/static/agent-math/091ca0487396554a405569c6.svg) | Dimensionless logits for corresponding classes and joint input–class energy; a C-class classifier emits C logits. |
| ![Formula](https://ml-biomat.com/static/agent-math/3092e09750f999904d9eddf5.svg) | Conditional class probability, input energy after marginalizing classes, and natural logarithm. |

Joint weight is exp(f_y); summing over classes at fixed x yields softmax and also an unnormalized input weight. Logits (2,0) give probabilities 0.880797 and 0.119203, with input energy −2.126928. Adding ten to both leaves class probabilities unchanged while shifting input energy to −12.126928. Classification training alone therefore does not identify input density.

Two numbers illustrate the issue. Logits (2,0) give first-class probability about 0.881. Adding ten to both logits for that input gives (12,10) with exactly the same class probabilities, but lowers its marginal input energy by ten. If this shared shift varies with the input, classification loss cannot identify it, while relative density across inputs changes. Turning a classifier into a useful generative energy model therefore requires an appropriate input-distribution learning signal. Reinterpreting logits supplies a mathematical structure, and joint training determines how that structure allocates probability.

Diffusion connects through scores as well. A fixed energy defines directions for one distribution, whereas diffusion usually learns directions at several noise levels and changes them over generation time. Adding energies corresponds to multiplying unnormalized weights, which can express a preference for satisfying several conditions together, such as approaching a goal while avoiding obstacles. In practical use, examine whether the energy represents the target, whether training covers relevant regions, and whether sampling explores them adequately. Every check made among these four valleys transfers to higher-dimensional candidate-design problems.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M40.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [UvA Deep Learning Tutorials: Deep Energy-Based Models](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial8/Deep_Energy_Models.html)

   Energy, negative phase, persistent sampling, and original generation-iteration figure.

   MIT, Copyright 2020 Phillip Lippe; original notebook output; external attributed figures excluded
2. [Estimation of Non-Normalized Statistical Models by Score Matching](https://jmlr.org/papers/v6/hyvarinen05a.html)

   The 2005 score-matching objective and integration-by-parts conditions.

   Primary paper reference; no copied figures
3. [A Connection Between Score Matching and Denoising Autoencoders](https://www-labs.iro.umontreal.ca/~vincentp/Publications/DenoisingScoreMatching_NeuralComp2011.pdf)

   The 2011 connection between Gaussian denoising and smoothed-density scores.

   Author-hosted primary paper; no copied figures
4. [Training Products of Experts by Minimizing Contrastive Divergence](https://www.cs.toronto.edu/~hinton/absps/tr00-004.pdf)

   Short-chain contrastive-divergence learning.

   Author-hosted technical report; no copied figures
5. [Implicit Generation and Generalization in Energy-Based Models](https://arxiv.org/html/1903.08689v2)

   Neural energies, Langevin negatives, and replay buffers.

   Primary paper reference; independent experiment
6. [Exponential Convergence of Langevin Distributions and Their Discrete Approximations](https://stat.duke.edu/~scs/Courses/Stat376/Papers/ConvergeRates/GeneralState/RobertsTweedie1996.pdf)

   Continuous Langevin dynamics, discrete approximations, and Metropolis correction.

   Primary paper reference; no copied figures
7. [Your Classifier is Secretly an Energy Based Model and You Should Treat it Like One](https://arxiv.org/abs/1912.03263)

   Classifier-logit and joint-energy connections.

   Primary paper reference; no copied figures
