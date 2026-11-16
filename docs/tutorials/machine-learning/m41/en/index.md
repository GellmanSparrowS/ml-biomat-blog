# Moving noise toward data: flow matching and rectified flow

Source: https://ml-biomat.com/tutorials/machine-learning/m41/en/
Language: en

Distinguish training segments from actual trajectories, then compare coupling, reflow, and numerical solvers.

## Giving a cloud of points directions until it forms a pattern

Imagine a drone display. Many lights begin scattered across the sky, then gradually form three curved pinwheel arms. If every drone were assigned a destination and flew straight there, the task might seem solved. A generative model starts with different information: we have samples of desired positions and can produce random starting positions, but there is no natural one-to-one correspondence between them. The model must learn where to move at a given position and time so that the distribution of the entire population becomes the desired distribution. Following one particle is useful, but the population is the object being modeled.

Flow matching turns this problem into velocity prediction. Construct paths that are easy to sample, choose a random position and time along them, and use the known velocity there as a training target. After training, begin at fresh random positions, repeatedly query the velocity, and integrate forward to create new samples. This approach works with continuous representations of images, sounds, and motion, and can transport between two observed distributions as well as from Gaussian noise to data. It provides a regression problem with explicit inputs and numerical labels for learning a generator.

Keep two pictures in view: the paths constructed for training and the paths actually obtained by integrating the model. Straight training segments can lead to curved generated trajectories. A small velocity loss can coexist with missing regions of the final distribution. Our three-arm pinwheel makes these distinctions visible. We train independent-pairing, minibatch optimal-transport, reflow, and arm-conditioned models, then evaluate their trajectories from the same new starting points. The open tutorial illustration below also separates distributions, velocity fields, and particle paths, three views that will remain useful throughout the chapter.

![CFM and OT-CFM densities, fields, and particles while transporting eight Gaussians toward two moons.](https://ml-biomat.com/static/tutorials/machine-learning/figures/7c604f4a70ace0ff466d7153.png?v=7c604f4a70ac)

Figure 1Three times from the original TorchCFM animation, selecting CFM and OT-CFM columns. Rows within each time show density, velocity field, and particle trajectories from eight Gaussians toward two moons. Alexander Tong and TorchCFM contributors, MIT; cropped and rearranged frames 0,55,110 with copyright and license retained. These are the source tutorial’s experiments.

## How a path supplies positions, times, and velocity labels

The easiest path to calculate is a straight line between two endpoints. Define generation time from zero to one, with noise at zero and data at one. An intermediate position is a weighted average of the endpoints. This time is a scale controlling generation progress, rather than the physical seconds of a drone flight. If the whole segment is traversed in one unit of generation time, its velocity is simply the destination minus the starting point. That vector gives both the direction and the distance traveled per unit of generation time.

$$
x_t=(1-t)x_0+tx_1,\qquad u_t(x_0,x_1)=\frac{d x_t}{dt}=x_1-x_0,\qquad t\sim\mathcal U(0,1)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2337d07ffc05a0636ede060.svg) | Noise endpoint, data endpoint, and intermediate location, all d-vectors; here d=2 with dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/6cf8706468163f4cc00255a7.svg) | Normalized generation time, uniform distribution on zero to one, conditional path velocity, and time derivative; velocity units are coordinate/generation-time. |

Hold endpoints fixed when differentiating the linear interpolation, obtaining −x₀+x₁. For x₀=(0,0),x₁=(2,1),t=0.25, position is (0.5,0.25) and velocity (2,1). Traversing the same displacement over five physical seconds would give (0.4,0.2) per second; normalized time is not automatically a second.

For a start at (0,0) and destination (2,1), the quarter-time position is (0.5,0.25), and velocity remains (2,1). Manufacturing a training example is straightforward: draw endpoints, draw a time between zero and one, and calculate the intermediate position and its velocity directly. There is no need to simulate the earlier quarter of the path or solve a complete ordinary differential equation during this training step. This is the concrete meaning of simulation-free training here. Generating a new sample still requires solving the motion defined by the trained network.

A collection of such moving segments produces a population at every time. Its changing probability distribution is called a probability path. Gaussian starts and observed data endpoints determine the two endpoint distributions; the pairing rule and interpolation determine the distributions in between. Linear interpolation is one convenient construction. Time-dependent signal and noise coefficients can define other paths with curved conditional trajectories. Specifying the endpoints, path, and time convention first is essential for identifying what the network is actually asked to predict and how its output should be interpreted.

Even identical endpoint distributions can have changing intermediate distributions. Suppose both one-dimensional endpoints are independent standard Gaussians. Half the start plus half the end has variance 0.25+0.25=0.5, narrower than either endpoint’s unit variance. If every destination is instead set equal to its own start, the paths remain stationary and variance stays one. These constructions share endpoint distributions but have different intermediate contraction. Coupling changes more than the lines in a diagram: it changes the population distributions that the network must transport along the way.

## One velocity at an intersection can still transport a population

Independent starts and destinations create many crossing segments. If two paths pass through the same position at the same time while demanding different velocities, a network receiving only position and time cannot return both answers. Squared-error regression instead returns the conditional average: it weights the velocities of paths that could pass through that location at that time by their relative likelihood. This is a local calculation conditioned on the current state, rather than one global direction averaged over the entire dataset. The distinction explains how a single vector field can represent a diverse population of training paths.

$$
L_{\rm CFM}(\theta)=\mathbb E\!\left[\frac1d\|v_\theta(x_t,t)-u_t\|^2\right],\qquad v^*(x,t)=\mathbb E[u_t\mid x_t=x,t]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0438b4b9edaa3075aad08d79.svg) | Predicted d-dimensional velocity, parameters, and optimal conditional-mean velocity under squared loss. |
| ![Formula](https://ml-biomat.com/static/agent-math/d45451db65f0237ead2f8e9f.svg) | Average over endpoint coupling and time, conditional velocity, intermediate position, time, dimensionality, and componentwise squared sum. |
| ![Formula](https://ml-biomat.com/static/agent-math/32a003be033473682af6ff34.svg) | Per-coordinate conditional flow-matching loss and conditioning bar; loss has squared-velocity units. |

Write target velocity as its conditional mean plus a zero-mean residual. Expanding the square makes the average cross term vanish, separating prediction error from conditional target variance. Equally likely labels (2,0) and (0,2) have optimal prediction (1,1) and per-coordinate minimum loss one. Different couplings can have different irreducible target variance.

Suppose two equally likely velocities at one location are (2,0) and (0,2). Their optimal squared-error prediction is (1,1). A particle following that average will query the velocity again at later positions and times, so it generally leaves the original training segment. The training label knows the endpoint assigned to its particular example; the network knows only the current state. Consequently, training on straight segments does not establish that generation can be completed accurately in one large step. The independent-pairing panel shows many crossing segments, whereas the integrated trajectories change direction as their states evolve.

This also explains why our independent model’s one-step output crowds toward the center. At time zero, an independently sampled destination is unrelated to the given starting point. The ideal velocity is therefore the target mean minus that starting point. A single Euler step of length one cancels the starting coordinate and sends every point toward the target mean. Multistep integration continually uses information supplied by intermediate positions to distribute particles among different arms. OT and reflow make destinations depend on starts, so their initial conditional average need not use the same destination mean everywhere.

![The same 24 endpoint sets under independent and minimum-squared-cost assignments. Right: actual ODE trajectories of another fixed starting set under the independent-pairing network. Hollow points mark starts and orange points training destinations; coordinates are dimensionless.](https://ml-biomat.com/static/tutorials/machine-learning/figures/90811349fe26ea7f4375149d.svg?v=90811349fe26)

Figure 2The same 24 endpoint sets under independent and minimum-squared-cost assignments. Right: actual ODE trajectories of another fixed starting set under the independent-pairing network. Hollow points mark starts and orange points training destinations; coordinates are dimensionless.

Why does this averaging still produce the desired probability path? Consider a tiny region. Its changing population depends on the average flow crossing its boundary, rather than the identity of each particle. Conditional averaging preserves that flow, and therefore preserves the constructed time marginals when the field is learned exactly and the required solution conditions hold. A smooth field with unique solutions cannot send two trajectories through the same point at the same time and then branch them into different futures. Passing through the same spatial point at different times is entirely possible, especially when viewing trajectories projected onto a plane.

$$
\frac{\partial p_t(x)}{\partial t}+\nabla_x\!\cdot\!\big[p_t(x)v(x,t)\big]=0,\qquad \frac{dz_t}{dt}=v(z_t,t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/58d7f37513126ee9d3605676.svg) | Probability density at x, d-dimensional coordinates, and generation time; density has inverse-coordinate-volume units. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d210ccd5a1479c85e1b122f.svg) | Velocity field, probability flux, and divergence, the sum of coordinate flux derivatives. |
| ![Formula](https://ml-biomat.com/static/agent-math/cd7dd1123c2b03722096ac5a.svg) | Actual ODE trajectory, time derivative at fixed location, and derivative following a trajectory. |

Probability lost by a small region equals net outward flow. A conditional-mean field preserves flux and hence time marginals. Uniform density translated by a constant field has zero flux divergence in the region and remains unchanged. A spatially expanding velocity creates net outflow and lowers density. ODE uniqueness rules out branching at the same position and time, while allowing visits at different times.

![Actual particles and learned fields for independent and minibatch-OT models at t=0,0.5,1. Blue marks 500 fixed generated particles and pale orange 300 fixed held-out targets. Arrows share a common scale.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9fa657276cd2ade8f76a9c77.svg?v=9fa657276cd2)

Figure 3Actual particles and learned fields for independent and minibatch-OT models at t=0,0.5,1. Blue marks 500 fixed generated particles and pale orange 300 fixed held-out targets. Arrows share a common scale.

## Choosing more useful pairs before learning the field

A pairing rule is called a coupling. Two couplings can use exactly the same starting and ending samples while creating very different routes. Consider starts (−1,0) and (1,0), with destinations listed as (1,1) and (−1,1). Connecting samples in that order creates crossing routes with mean squared distance five. Swapping destinations gives two upward vertical routes with mean squared distance one. Neither endpoint distribution changes. What changes is the correspondence and the complexity of the velocity targets along the way. This small calculation exposes a modeling choice that can otherwise be hidden inside a data loader.

$$
\pi^*=\arg\min_{\pi\in S_B}\frac1B\sum_{i=1}^{B}\|a_i-b_{\pi(i)}\|^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8416f2a80d4385b5f4add97f.svg) | Batch size, index, d-dimensional noise starts, and data endpoints; B=128 during training. |
| ![Formula](https://ml-biomat.com/static/agent-math/9f98c39eb3bed43f5aeaf29a.svg) | All permutations of B items, a one-to-one assignment, a minimum-cost assignment, and the operation selecting an optimizer. |
| ![Formula](https://ml-biomat.com/static/agent-math/40ce8c99eb6c6b3590d8d679.svg) | Squared Euclidean distance and batch average; cost has squared-coordinate units. |

Starts [(−1,0),(1,0)] and destinations [(1,1),(−1,1)] yield cost matrix [[5,1],[1,5]]. Identity assignment costs five on average; swapping costs one. Linear assignment uses every endpoint exactly once and minimizes this batch cost. Batch assignment and globally optimal transport between full distributions operate at different scales.

Our OT variant calculates every squared distance between 128 Gaussian starts and 128 data points in a minibatch, then finds a one-to-one assignment minimizing the total cost. Each destination is used exactly once, preserving that batch’s empirical distribution. In the displayed 24-point illustration, mean squared cost falls from 2.846 to 0.627. This optimization concerns a finite batch. Another batch produces another assignment, so the result should be interpreted as minibatch transport rather than an already established globally optimal map between the full continuous distributions. Batch size controls both the information available to matching and its computational cost.

The 2022 flow-matching work connected probability paths with velocity regression. Later minibatch optimal-transport work studied how pairings can make that learning problem easier. These developments address related questions: first obtain a computable training target, then improve the routes contained in it. Their velocity labels have different distributions, so independent and OT validation losses are not directly comparable measures of final generative quality. We will evaluate integrated samples against the same held-out distribution and measure trajectory bending separately. This keeps a simpler regression target from being mistaken for a complete assessment of a generator.

## Rectified flow: learning to straighten routes that already work

Rectified flow also starts from straight interpolation and velocity regression, emphasizing the deterministic coupling produced by the learned ODE and how to make generated routes straighter. The 2022 work introduced reflow: integrate a trained velocity field from fresh starting points, save the actual start–end pairs, and train a second field on straight segments joining those pairs. The initial fit may begin with arbitrary pairings. The second fit inherits correspondences already created by the first model. The training target becomes more consistent with the routes that a deterministic generator can actually follow.

$$
z_1=\Phi_{v^{(k)}}(z_0),\qquad \tilde x_t=(1-t)z_0+tz_1,\qquad \tilde u=z_1-z_0,\qquad v^{(k+1)}\leftarrow\operatorname{Fit}(\tilde x_t,t,\tilde u)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5c9c71a539128c2c36e4ac1.svg) | Reflow round, teacher field, and next-round student field; the round differs from ODE time. |
| ![Formula](https://ml-biomat.com/static/agent-math/fc15703225552a6ecf429650.svg) | Map integrating the teacher ODE from zero to one, random start, and teacher-generated endpoint. |
| ![Formula](https://ml-biomat.com/static/agent-math/515cff3ac5beb1aca8f634b1.svg) | New straight-path training location, velocity label, generation time, and fitting by the preceding squared objective; locations and velocities are d-vectors. |

If a teacher sends (−1,0) to (0,2), the new midpoint is (−0.5,1) and target velocity (1,2). The student learns straight connections between teacher endpoints rather than every curved intermediate teacher velocity. Numerical teacher endpoints and fitting error affect the next distribution; all teacher pairs are saved.

A commuting analogy is useful. First help a population find routes that reach destinations. Then record actual departures and arrivals, and redesign those routes to reduce detours while retaining the correspondence. Reflow continues to learn a time-dependent velocity field, so it remains compatible with multistep integration. Directly regressing the final destination from the starting point would instead train a one-step map; such a distillation stage can follow reflow, but it is a separate computation. Straightness, time dependence, and the number of sampling steps should therefore be described explicitly rather than inferred from the method’s name.

Our experiment starts with the independent-pairing model. A 64-step Heun solver produces 2,048 training pairs and 512 validation pairs, which supervise a fresh network. Mean integrated path length minus endpoint chord length falls from approximately 0.3965 to 0.00133. One-step Euler sliced distribution distance improves from 0.5739 to 0.0852. However, the fine-step reflow distribution has distance 0.0791 from held-out data, compared with 0.0729 for its teacher. Reflow learns from teacher-generated endpoints. Straighter routes and a distribution closer to the original data are separate objectives that the measurements help distinguish.

![First 500 fixed outputs for three unconditional models using Euler1,Euler4,Heun8,and RK4-128 reference. Initial points and coordinate limits are shared. Each reference approximates its own model ODE.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1ab18f600b6a4b9076c3bb9a.svg?v=1ab18f600b6a)

Figure 4First 500 fixed outputs for three unconditional models using Euler1,Euler4,Heun8,and RK4-128 reference. Initial points and coordinate limits are shared. Each reference approximates its own model ODE.

## Trading velocity queries for integration accuracy

The network supplies an instantaneous velocity; a solver accumulates velocities into positions. Euler queries the current velocity and advances by a chosen step size. When velocity changes along that step, the update departs from the exact solution. Heun first makes an Euler prediction, queries velocity at the predicted endpoint, then corrects using the average of the two velocities. Classical RK4 evaluates two intermediate stages and an endpoint stage, combining four queries for each step. Accuracy per step and computation per step therefore change together. Comparing only the number of steps would hide this difference.

$$
x_{n+1}^{\rm Euler}=x_n+h\,v(x_n,t_n),\qquad \tilde x=x_n+h\,v(x_n,t_n),\qquad x_{n+1}^{\rm Heun}=x_n+\frac h2\big[v(x_n,t_n)+v(\tilde x,t_n+h)\big]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/880884186ce6b52872048e8b.svg) | Solver-step index, step size, current generation time, and d-state; for uniform N steps,h=1/N and t_n=nh. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca42b4fdc1565280331cdddb.svg) | Temporary Euler prediction, velocity network, and updated state; h times velocity gives a coordinate increment. |

For dx/dt=x,x₀=1,h=1, Euler gives two. Heun predicts two, then averages velocities one and two to give 2.5. The exact value is e≈2.71828. RK4 evaluates two additional half-step states and combines four velocities with weights 1:2:2:1; the complete code implements these stages. Sixteen queries buy Euler16, Heun8, or four RK4 steps.

A hand-checkable example has velocity equal to position and initial position one. From time zero to one, the exact endpoint is e≈2.71828. Euler gives two with one step, 2.44141 with four, 2.63793 with sixteen, and 2.69734 with sixty-four. The velocity field is exactly correct in this example, so the entire discrepancy comes from finite step size. A generative experiment contains both possibilities: a learned field may define the wrong motion, and a numerical solver may approximate that motion inaccurately. Separate checks are needed to identify which issue affects a particular result.

We use each model’s 128-step RK4 output as a numerical reference and repeat with 256 steps to check refinement stability. The same budget of sixteen network queries can purchase sixteen Euler steps, eight Heun steps, or four RK4 steps. For the independent-pairing model, their endpoint root-mean-square errors relative to the reference are approximately 0.06495, 0.00473, and 0.000624. Since the network is fixed, these differences come from integration. Each model must have its own reference trajectory; changing the velocity field changes the motion being approximated.

![Left: endpoint RMSE against each model’s own reference. Middle: 32-direction sliced W1 against the same held-out set. Circles,squares,triangles indicate Euler,Heun,RK4; x measures network evaluations. Right: mean path length minus chord across 1,024 reference trajectories.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ab17c79b76557b95c95802f1.svg?v=ab17c79b7655)

Figure 5Left: endpoint RMSE against each model’s own reference. Middle: 32-direction sliced W1 against the same held-out set. Circles,squares,triangles indicate Euler,Heun,RK4; x measures network evaluations. Right: mean path length minus chord across 1,024 reference trajectories.

The distribution comparison answers a different question and need not improve monotonically with integration accuracy. For example, OT with four Euler steps gives sliced distance about 0.0590, while its fine-step reference gives 0.0623. In this run, coarse numerical error happens to reduce that finite-sample metric. Choosing a sampler therefore involves numerical accuracy, the generated distribution, and regional coverage together. Denoiser or velocity-network calls are a useful common budget, while matching and training overhead belong to separate accounting when comparing how the models are built.

## Follow one particle while observing the population

Replay actual RK4-128 trajectories, showing every eighth step for seventeen frames. Arrows are predictions from the same model at that time; the right-hand panels compare models using the same coordinate limits.

[Figure: Particles,velocity field,and actual integrated trajectories](https://ml-biomat.com/tutorials/machine-learning/m41/en/#M41-board)

Blue points are current states from 128 fixed starts; red marks the selected particle and its traveled path. The gray dashed chord connects its actual endpoints to reveal detours; it is not an original training pair. Pale orange curves mark known target centerlines, with arrows shown at a fixed scale.

## Locating flow matching alongside continuous flows and diffusion

A continuous normalizing flow describes an invertible continuous transformation defined by a velocity field and an ODE. Flow matching describes a way to train that field. Both names can apply to the same model: learn velocity with flow matching, sample by integrating the ODE, and accumulate the velocity divergence along the path if a density value is also required. Velocity-regression training can omit this divergence calculation. Evaluating a particular sample’s log density requires adding it back. Separating the model structure from the learning objective resolves much of the apparent overlap between the terms.

Neural ODEs in 2018 expressed changes between network layers as continuous dynamics and supplied trainable computational machinery for continuous flows. Direct maximum-likelihood training of such models generally integrates both state and density changes inside the training loop. Flow matching later moved supervision to conditional paths that can be sampled directly. The network still defines continuous motion; the source of its training signal changes. Avoiding a solver during training and using a solver during sampling are therefore compatible statements, and their combination helps explain the appeal of this approach.

$$
\frac{d\log p_t(z_t)}{dt}=-\nabla_z\cdot v_\theta(z_t,t)=-\sum_{i=1}^{d}\frac{\partial v_{\theta,i}}{\partial z_i}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f254dc7dba41b1b4a8f26790.svg) | Actual ODE trajectory, density there, natural logarithm, and derivative following the trajectory; log density is in nats under fixed coordinate units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a6396b974572ca759bf6ac3d.svg) | Velocity component i, position coordinate i, index, dimension, and divergence; divergence has inverse-generation-time units. |

For v=(0.5z₁,0.5z₂), divergence is one. Over unit time both coordinates expand by e^0.5, area by e, and density falls by e^(−1), preserving probability mass. Flow-matching training omits this divergence, while CNF density evaluation integrates it along the path. Sample-distribution diagnostics and density evaluation answer different questions.

A diffusion probability-flow ODE also defines a velocity field, usually derived from a noise process and its score. If a corresponding sampleable conditional path directly supervises velocity, the construction can be viewed through flow matching. The approaches share many continuous probability paths and numerical tools. Differences often concern path selection, the quantity predicted by the network, and the weighting of training errors. For a fixed path, noise, clean-data, and velocity predictions may be related through known coefficients. Their loss weightings and numerical conditioning can still differ, so an algebraic conversion does not make all training implementations identical.

Time direction deserves particular attention. Here time zero is noise and time one is data. In the diffusion chapter, discrete time zero is clean data and larger indices mean more corruption. Align the time axes before comparing velocity or score signs. Otherwise a difference in convention can look like a disagreement between methods. Generation time is also distinct from physical time inside a sample. If the generated object is a robot motion sequence, the velocity field changes the entire proposed sequence as generation progresses; it does not directly denote the physical velocity of a joint within that sequence.

## The complete pinwheel experiment

The pinwheel has three arms. Radius ranges uniformly from 0.4 to 2, and angle equals an arm-specific base angle plus 0.8 times radius. Independent Gaussian noise with standard deviation 0.07 is then added to both coordinates. Independent seeds generate 4,096 training points and 1,024 points each for validation and testing. Coordinates are dimensionless. Each unconditional network has two hidden layers of width 96 and 9,890 parameters. The conditioned network additionally receives a three-dimensional arm code and has 10,178 parameters. Independent, OT, and conditional models use 4,000 updates; reflow uses 3,000.

Generation uses the same 1,024 fresh Gaussian starts across comparisons. To measure sliced Wasserstein-1 distance, project generated and held-out points onto 32 equally spaced directions, sort both projections separately, calculate their mean absolute difference, then average across directions. This turns comparison into a collection of one-dimensional transport problems. Smaller values mean closer projected distributions. Another diagnostic projects points to known arm centerlines, checks the fraction within distance 0.21, and divides each of three arms into six regions. A region is covered when it contains at least five points meeting the distance criterion.

$$
\widehat{SW}_1=\frac1K\sum_{k=1}^{K}\frac1N\sum_{i=1}^{N}\left|\operatorname{sort}(Xq_k)_i-\operatorname{sort}(Yq_k)_i\right|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fea5eb7b1530bbb810b9d5d2.svg) | N×d matrices of generated and held-out points, common count N=1024, and dimensionality d=2. |
| ![Formula](https://ml-biomat.com/static/agent-math/8e00274d63d818bbde8ebcc7.svg) | Unit projection direction k, direction count K=32, and direction index; planar angles are uniformly spaced in [0,π). |
| ![Formula](https://ml-biomat.com/static/agent-math/7d9c626d72a72106966cdb1f.svg) | Independent sorting within each projection, sorted index, absolute value, and finite-direction sliced-W1 estimate, with coordinate units. |

Equal-weight one-dimensional samples [0,2] and [1,3] have sorted differences one and one, giving W1=1. In two dimensions, project first and average across directions. Different local defects can share a metric value, so we also inspect centerline distances, eighteen-region coverage, and scatter plots.

These diagnostics describe different aspects of the same outputs. Fine-step sliced distances for independent, OT, and reflow are approximately 0.0729, 0.0623, and 0.0791. Fractions close to the centerlines are approximately 68.7%, 76.9%, and 65.1%. All three cover the eighteen defined regions, although their thickness and local placement differ. Full region coverage therefore leaves room for substantial quality differences within regions. The code saves all endpoints, complete reference trajectories, teacher pairings, training records, and weights, allowing thresholds and summaries to be changed without relying on a selected scatter plot.

The fixed validation sets are also tied to each training objective. OT validation uses the same minibatch size and matching rule as OT training, while reflow validation uses independent teacher-generated pairs. Checkpoint selection occurs within each objective. The shared held-out distribution is reserved for comparing final samples. This arrangement keeps route construction, model selection, and final distribution assessment distinct, while allowing every reported result to be reconstructed from the complete program below.

### Complete Python: velocity training, reflow, and solver comparisons

Run python main.py --output results --language en with NumPy,SciPy,PyTorch,and Matplotlib. Explicit rules generate all data. Four networks are trained; all outputs,teacher pairs,reference trajectories,weights,and scientific figures are saved.

```
"""Train flow-matching velocity fields and compare actual ODE trajectories.
All data follow the explicit pinwheel rule below. No downloads are required.
"""
from pathlib import Path
import argparse,json,math,copy,platform,time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
def pinwheel(n,seed):
 r=np.random.default_rng(seed);labels=np.arange(n)%3;r.shuffle(labels);radius=r.uniform(.4,2,n);angle=labels*2*np.pi/3+.8*radius;points=np.c_[radius*np.cos(angle),radius*np.sin(angle)]+r.normal(0,.07,(n,2));return points.astype('float32'),labels
train,labels=pinwheel(4096,410);valid,valid_labels=pinwheel(1024,411);test,test_labels=pinwheel(1024,412);xt=torch.tensor(train);yt=torch.tensor(labels)
class Velocity(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(3+(3 if conditional else 0),96),nn.SiLU(),nn.Linear(96,96),nn.SiLU(),nn.Linear(96,2))
 def forward(self,x,t,c=None):
  if isinstance(t,(float,int)):t=torch.full((len(x),1),float(t))
  else:t=t.reshape(-1,1)
  parts=[x,t]
  if self.conditional:parts.append(F.one_hot(c,3).float())
  return self.net(torch.cat(parts,1))
def couple(a,b,kind):
 if kind!='OT':return b
 cost=torch.cdist(a,b).square().numpy();_,j=linear_sum_assignment(cost);return b[j]
@torch.no_grad()
def integrate(model,initial,steps,method='heun',condition=None,record=False):
 x=initial.clone();h=1/steps;path=[x.numpy().copy()] if record else []
 for i in range(steps):
  t=i*h;k1=model(x,t,condition)
  if method=='euler':x=x+h*k1
  elif method=='heun':x=x+h*(k1+model(x+h*k1,t+h,condition))/2
  else:
   k2=model(x+h*k1/2,t+h/2,condition);k3=model(x+h*k2/2,t+h/2,condition);k4=model(x+h*k3,t+h,condition);x=x+h*(k1+2*k2+2*k3+k4)/6
  if record:path.append(x.numpy().copy())
 return x.numpy(),np.array(path)
histories={};training={};models={}
def fit(name,seed,steps=4000,paired=None):
 conditional=name=='Conditional';torch.manual_seed(seed);m=Velocity(conditional);opt=torch.optim.Adam(m.parameters(),lr=.001);rng=torch.Generator().manual_seed(seed+100);vrng=torch.Generator().manual_seed(seed+200)
 if paired is None:
  va=torch.randn((1024,2),generator=vrng);vb=torch.tensor(valid);vc=torch.tensor(valid_labels)
  if name=='OT':vb=torch.cat([couple(va[i:i+128],vb[i:i+128],name) for i in range(0,1024,128)])
 else:va,vb=paired[2:];vc=None
 vt=torch.rand((len(va),1),generator=vrng);vx=(1-vt)*va+vt*vb;vu=vb-va;best=float('inf');best_state=None;history=[];started=time.perf_counter()
 for step in range(1,steps+1):
  if paired is None:
   idx=torch.randint(len(xt),(128,),generator=rng);a=torch.randn((128,2),generator=rng);b=couple(a,xt[idx],name);c=yt[idx] if conditional else None
  else:
   idx=torch.randint(len(paired[0]),(128,),generator=rng);a,b=paired[0][idx],paired[1][idx];c=None
  t=torch.rand((128,1),generator=rng);x=(1-t)*a+t*b;u=b-a;loss=F.mse_loss(m(x,t,c),u);opt.zero_grad();loss.backward();opt.step()
  if step%200==0:
   with torch.no_grad():vl=F.mse_loss(m(vx,vt,vc),vu).item()
   history.append([step,loss.item(),vl])
   if vl<best:best=vl;best_step=step;best_state=copy.deepcopy(m.state_dict())
 m.load_state_dict(best_state);m.eval();models[name]=m;histories[name]=history;training[name]=dict(parameters=sum(p.numel() for p in m.parameters()),updates=steps,best_step=best_step,validation_velocity_mse=best,seconds=time.perf_counter()-started,seed=seed);torch.save(dict(model=m.state_dict(),conditional=conditional,best_step=best_step),out/f'{name.lower()}.pt');return m
fit('Independent',414);fit('OT',415)
teacher_rng=torch.Generator().manual_seed(416);teacher_train=torch.randn((2048,2),generator=teacher_rng);teacher_valid=torch.randn((512,2),generator=teacher_rng);teacher_b,_=integrate(models['Independent'],teacher_train,64,'heun');teacher_vb,_=integrate(models['Independent'],teacher_valid,64,'heun');fit('Reflow',417,3000,(teacher_train,torch.tensor(teacher_b),teacher_valid,torch.tensor(teacher_vb)));fit('Conditional',418)
evalrng=torch.Generator().manual_seed(413);initial=torch.randn((1024,2),generator=evalrng);requests=torch.arange(1024)%3
rr=np.linspace(.4,2,240);curve=np.concatenate([np.c_[rr*np.cos(c*2*np.pi/3+.8*rr),rr*np.sin(c*2*np.pi/3+.8*rr)] for c in range(3)]);curve_labels=np.repeat(np.arange(3),len(rr));curve_bins=np.tile(np.minimum((np.arange(len(rr))*6/len(rr)).astype(int),5),3)
angles=np.arange(32)*np.pi/32;directions=np.c_[np.cos(angles),np.sin(angles)]
def assess(x):
 distance=((x[:,None]-curve[None])**2).sum(2);nearest=distance.argmin(1);d=np.sqrt(distance[np.arange(len(x)),nearest]);cl=curve_labels[nearest];inside=d<.21;counts=np.bincount((cl*6+curve_bins[nearest])[inside],minlength=18);sw=float(np.abs(np.sort(x@directions.T,axis=0)-np.sort(test@directions.T,axis=0)).mean());return dict(sliced_w1=sw,mean_curve_distance=float(d.mean()),near_curve_fraction=float(inside.mean()),covered_bins=int((counts>=5).sum()),bin_counts=counts.tolist(),arm_counts=np.bincount(cl,minlength=3).tolist())
settings=[('Euler1','euler',1),('Euler4','euler',4),('Euler16','euler',16),('Heun8','heun',8),('RK4x4','rk4',4),('Heun32','heun',32)]
metrics={};outputs={};paths={};replay={};axis=np.linspace(-2.5,2.5,11);gx,gy=np.meshgrid(axis,axis);grid=np.c_[gx.ravel(),gy.ravel()].astype('float32')
for name,m in models.items():
 c=requests if name=='Conditional' else None;reference,reference_path=integrate(m,initial,128,'rk4',c,True);paths[name]=reference_path;outputs[name+'_reference']=reference;metrics[name]={}
 for label,method,n in settings:
  value,_=integrate(m,initial,n,method,c);stat=assess(value);stat.update(endpoint_rmse=float(np.sqrt(np.mean((value-reference)**2))),calls=n*dict(euler=1,heun=2,rk4=4)[method]);metrics[name][label]=stat;outputs[name+'_'+label]=value
 stat=assess(reference);refined,_=integrate(m,initial,256,'rk4',c);stat['refinement_rmse']=float(np.sqrt(np.mean((refined-reference)**2)));stat['calls']=512;chords=np.linalg.norm(reference_path[-1]-reference_path[0],axis=1);lengths=np.linalg.norm(np.diff(reference_path,axis=0),axis=2).sum(0);stat['mean_path_excess']=float(np.mean(lengths-chords));stat['mean_path_length']=float(lengths.mean());stat['mean_chord_length']=float(chords.mean())
 if c is not None:stat['condition_agreement']=float((curve_labels[((reference[:,None]-curve[None])**2).sum(2).argmin(1)]==requests.numpy()).mean())
 metrics[name]['Reference']=stat
 if name!='Conditional':
  time_indices=np.arange(0,129,8);fields=[]
  with torch.no_grad():
   for k in time_indices:fields.append(m(torch.tensor(grid),k/128).numpy().tolist())
  replay[name]=dict(times=(time_indices/128).tolist(),points=reference_path[time_indices,:128].tolist(),velocity=fields,solver='RK4, 128 steps')
# Exact two-by-two assignment, one hand interpolation, and a known ODE isolate calculation.
hand_a=np.array([[-1.,0.],[1.,0.]]);hand_b=np.array([[1.,1.],[-1.,1.]]);cost=((hand_a[:,None]-hand_b[None])**2).sum(2);row,col=linear_sum_assignment(cost);ode=[]
for n in [1,4,16,64]:
 x=1.;h=1/n
 for _ in range(n):x+=h*x
 ode.append(dict(steps=n,value=x,error=abs(x-math.e)))
pairrng=np.random.default_rng(419);pair_a=pairrng.normal(size=(24,2));pair_b=train[:24];_,pair_j=linear_sum_assignment(((pair_a[:,None]-pair_b[None])**2).sum(2));pair_ot=pair_b[pair_j]
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=1024,seeds=[410,411,412],noise=.07),training=training,metrics=metrics,reflow=dict(train_pairs=2048,validation_pairs=512,teacher='Independent',teacher_solver='Heun64',teacher_calls_per_pair=128),hand=dict(interpolated=[.5,.25],velocity=[2.,1.],independent_cost=float(cost.diagonal().mean()),optimal_cost=float(cost[row,col].mean()),optimal_permutation=col.tolist(),euler_exp=ode),display_pairs=dict(independent_mean_cost=float(np.mean(np.sum((pair_b-pair_a)**2,1))),ot_mean_cost=float(np.mean(np.sum((pair_ot-pair_a)**2,1)))))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'replay.json').write_text(json.dumps(dict(models=replay,grid=grid.tolist(),target=test[:400].tolist(),curves=[curve[i*240:(i+1)*240:8].tolist() for i in range(3)]),separators=(',',':')),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,train_labels=labels,validation=valid,validation_labels=valid_labels,test=test,test_labels=test_labels,initial_noise=initial.numpy(),requested_classes=requests.numpy(),teacher_train_start=teacher_train.numpy(),teacher_train_end=teacher_b,teacher_validation_start=teacher_valid.numpy(),teacher_validation_end=teacher_vb,grid=grid,pair_a=pair_a,pair_b=pair_b,pair_ot=pair_ot,**outputs,**{name+'_trajectory':v for name,v in paths.items()},**{name+'_history':np.array(v) for name,v in histories.items()})
colors=['#176b8a','#bd6d3a','#63864b']
fig,axs=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
for ax,b,title in zip(axs[:2],[pair_b,pair_ot],[tr('A  独立配对','A  Independent pairs'),tr('B  小批次最短平方距离配对','B  Minibatch squared-cost assignment')]):
 for a,z in zip(pair_a,b):ax.plot([a[0],z[0]],[a[1],z[1]],color='#647e87',alpha=.4,lw=.8)
 ax.scatter(*pair_a.T,s=26,facecolors='none',edgecolors='#125f82',label=tr('噪声起点','Noise start'));ax.scatter(*b.T,s=24,c='#bf7139',label=tr('数据终点','Data end'));ax.set_title(title);ax.legend(fontsize=8)
for i in range(24):axs[2].plot(paths['Independent'][:,i,0],paths['Independent'][:,i,1],color=colors[i%3],alpha=.7,lw=1)
axs[2].scatter(*initial[:24].numpy().T,s=20,facecolors='none',edgecolors='#125f82');axs[2].set_title(tr('C  学到的ODE轨迹','C  Learned ODE trajectories'))
for ax in axs:ax.set(xlabel='x1',ylabel='x2',xlim=(-4,4),ylim=(-4,4));ax.set_aspect('equal')
save(fig,'couplings')
fig,axs=plt.subplots(2,3,figsize=(13,8),layout='constrained')
for row,name in enumerate(['Independent','OT']):
 for col,k in enumerate([0,64,128]):
  ax=axs[row,col];pts=paths[name][k];ax.scatter(pts[:500,0],pts[:500,1],s=5,color='#176b8a',alpha=.5);ax.scatter(test[:300,0],test[:300,1],s=3,color='#bf7139',alpha=.15)
  with torch.no_grad():v=models[name](torch.tensor(grid),k/128).numpy()
  ax.quiver(grid[:,0],grid[:,1],v[:,0],v[:,1],angles='xy',scale_units='xy',scale=8,width=.003,color='#314c59');ax.set(xlim=(-3,3),ylim=(-3,3),xlabel='x1',ylabel='x2',title=f'{name}, t={k/128:.1f}');ax.set_aspect('equal')
save(fig,'velocity')
fig,axs=plt.subplots(3,4,figsize=(13,10),layout='constrained')
for row,name in enumerate(['Independent','OT','Reflow']):
 for col,key in enumerate(['Euler1','Euler4','Heun8','reference']):
  v=outputs[name+'_'+key];ax=axs[row,col];ax.scatter(*v[:500].T,s=5,alpha=.55,color='#176b8a');ax.set(xlabel='x1',ylabel='x2',xlim=(-3,3),ylim=(-3,3),title=f'{name} / {key}');ax.set_aspect('equal')
save(fig,'samples')
fig,axs=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
for j,name in enumerate(['Independent','OT','Reflow']):
 for label,method,n in settings:
  z=metrics[name][label];axs[0].scatter(z['calls'],z['endpoint_rmse'],color=colors[j],marker=dict(euler='o',heun='s',rk4='^')[method]);axs[1].scatter(z['calls'],z['sliced_w1'],color=colors[j],marker=dict(euler='o',heun='s',rk4='^')[method])
 axs[0].plot([],[],color=colors[j],label=name);axs[2].bar(j,metrics[name]['Reference']['mean_path_excess'],color=colors[j])
axs[0].set(xscale='log',yscale='log',xlabel=tr('速度网络调用次数','Velocity-network calls'),ylabel=tr('终点对参考解RMSE','Endpoint RMSE vs reference'),title=tr('A  同一模型的数值误差','A  Numerical error within each model'));axs[0].legend(fontsize=8);axs[1].set(xscale='log',xlabel=tr('速度网络调用次数','Velocity-network calls'),ylabel=tr('32方向投影W1','32-direction sliced W1'),title=tr('B  与独立测试分布比较','B  Difference from held-out distribution'));axs[2].set(xticks=range(3),xticklabels=['Independent','OT','Reflow'],ylabel=tr('平均路径长减弦长','Mean path length minus chord'),title=tr('C  积分路径弯曲程度','C  Curvature of integrated paths'));save(fig,'diagnostics')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained');conditional=outputs['Conditional_reference'];req=requests.numpy()
for c,ax in enumerate(axs):
 ax.scatter(*test[test_labels==c].T,s=7,color='#bf7139',alpha=.4,label=tr('测试目标','Test target'));ax.scatter(*conditional[req==c].T,s=7,color='#176b8a',alpha=.6,label=tr('按类别生成','Conditional samples'));ax.set(xlim=(-2.5,2.5),ylim=(-2.5,2.5),xlabel='x1',ylabel='x2',title=tr('请求叶片 ','Requested arm ')+str(c));ax.set_aspect('equal');ax.legend(fontsize=9)
save(fig,'conditions');print(json.dumps(summary,indent=2))
```

## A condition chooses the region; evaluation checks the arrival

In the conditional experiment, the network also receives the requested arm index. During training, the target point’s arm is supplied as the condition and the Gaussian start remains independent. During generation, changing the code can send the same noise toward another arm. Fine-step conditional samples agree with requested arms for approximately 99.8% of cases, with about 90.0% close to the centerline. These numbers describe this three-class geometric task. Text, sound prompts, or initial body poses require their own condition encoders and task-specific definitions of agreement.

![Actual arm-conditioned samples, blue, and corresponding held-out targets, orange. Each request uses its assigned subset of the shared evaluation noise, approximately 341 points, with RK4-128.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c4d811f7ced36fcbd0acc0af.svg?v=c4d811f7ced3)

Figure 6Actual arm-conditioned samples, blue, and corresponding held-out targets, orange. Each request uses its assigned subset of the shared evaluation noise, approximately 341 points, with RK4-128.

When a sample represents a whole motion sequence, its coordinates may concatenate joint angles across all physical time steps. The flow network then predicts how the entire candidate sequence should change during generation. That rate differs from a joint’s physical angular velocity: one follows generation time through alternative proposals, while the other follows physical time within a proposal. The model can generate several candidates, after which collision, joint range, contact conditions, and endpoint error determine whether each candidate is executable. Distinguishing these two time axes makes the representation and its evaluation easier to design.

Returning to the light display, the model learns to organize a population rather than assign permanent identities to its members. Endpoint coupling establishes the training paths, conditional averaging produces a queryable velocity field, integration creates actual trajectories, and evaluation examines the resulting distribution. These four parts explain why straight training paths can yield curved generation, why reflow can reduce the required step count, and why speed, straightness, and agreement with the target deserve separate measurements. The same reasoning applies when each point represents thousands of image or audio coordinates.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M41.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Flow Matching for Generative Modeling](https://arxiv.org/html/2210.02747v2)

   Probability paths,conditional velocities,and marginal velocity regression.

   Primary paper; independent experiment
2. [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/html/2209.03003v1)

   Straight interpolation,ODE couplings,reflow,and trajectory properties.

   Primary paper; independent experiment
3. [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482)

   Minibatch couplings and OT-CFM.

   Primary paper; independent experiment
4. [TorchCFM](https://github.com/atong01/conditional-flow-matching)

   Original density,field,and trajectory animation,identified as generated by repository tutorials.

   MIT Copyright2023AlexanderTong; cropped original frames and license retained
5. [Flow Matching Guide and Code](https://github.com/facebookresearch/flow_matching)

   Further study of continuous and discrete flow matching.

   CC BY-NC repository; linked reference only, no code/figure reuse
6. [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366)

   Continuous-dynamics networks and density evolution.

   Primary paper; no copied figures
7. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/html/2011.13456v2)

   Probability-flow ODE connections to diffusion.

   Primary paper; no copied figures
