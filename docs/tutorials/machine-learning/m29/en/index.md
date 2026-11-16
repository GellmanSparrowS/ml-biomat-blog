# From a cup of coffee to scientific machine learning: PINNs, FNOs, and equation discovery

Source: https://ml-biomat.com/tutorials/machine-learning/m29/en/
Language: en

Connect scientific laws, observations, and numerical methods through solving, identification, operator learning, and equation discovery.

## 1. What can a cup of coffee teach us about scientific machine learning?

Leave a hot cup of coffee on a desk and record its temperature once a minute. A declining curve appears quickly, but several different questions can follow. How hot will the coffee be after ten minutes? How would a different cup change its cooling rate? Can measurements from the first minute identify both the cup's insulation and the room temperature? These questions all involve data, yet require different computations. With a known law and known parameters, we calculate temperatures forward in time. With a known law and unknown parameters, we infer parameters from observations. When even the law is uncertain, we compare candidate equations that could explain the measurements.

Scientific machine learning brings this structure into the learning process. Prior information can take the form of a conservation relation, a differential equation, a geometric symmetry, or a differentiable simulation program. A network might represent an unknown function, supply a missing mechanism, or accelerate many repeated solutions. Think of completing a map whose roads and rivers are already partly known. Identifying the reliable information and the parts that observations must determine gives a more concrete basis for selecting a model and loss than simply increasing network size. It also determines what counts as an informative new measurement.

Three connected problems organize this chapter. Cooling introduces numerical integration, physics-informed neural networks, and parameter identification. A conducting ring explains why a Fourier neural operator learns a function-to-function mapping. Noisy growth curves let sparse identification select an equation from a candidate library. Finally, oscillator energy separates the roles of a continuous equation, a learned representation, and a discrete solver. The diagram compares their inputs and outputs. Return to it while reading the program to identify exactly what is being learned in each experiment.

![From Fourier decomposition to SINDy, PINNs, and FNOs: each method has different inputs and learned objects. Curves illustrate mechanisms; subsequent figures report actual calculations.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c80d8f2a1a9c4a2529766533.svg?v=c80d8f2a1a9c)

Figure 1From Fourier decomposition to SINDy, PINNs, and FNOs: each method has different inputs and learned objects. Curves illustrate mechanisms; subsequent figures report actual calculations.

## 2. A differential equation describes how a state changes now

A thermometer reports the temperature at a particular instant; a differential equation describes its instantaneous rate of change. Coffee generally loses heat faster when it is much hotter than its surroundings. A simple lumped-temperature model makes that rate proportional to the temperature excess. Representing the whole cup by one number ignores internal spatial differences. Ambient temperature and the cooling coefficient are also held constant during this experiment. These choices suit an overall cooling curve. Studying temperature inside a thick object instead requires spatial coordinates and a heat-conduction equation, because different locations can have different temperatures simultaneously.

$$
\frac{dT}{dt}=-k(T-T_a),\qquad T(t)=T_a+(T_0-T_a)e^{-kt}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bfb18198bbe0d00a4b99f5f6.svg) | Current, ambient, and initial temperatures in°C; temperature differences can equivalently use kelvin. |
| ![Formula](https://ml-biomat.com/static/agent-math/46e85659ae7cce8ad65d8b6c.svg) | Time in minutes and positive cooling rate in inverse minutes; kt is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f970573b6ea0d9dd47cb0090.svg) | Temperature rate in°C/min; e is the base of the natural exponential. |

For constant ambient, excess θ=T−T_a obeys θ′=−kθ. An exponential differentiates into itself times its rate, so θ=(T_0−T_a)e^(−kt) satisfies both equation and initial value. With T_0=80, T_a=20, k=.35, initial rate is−21°C/min and analytic temperature after one minute is approximately 62.28°C.

A derivative becomes less mysterious when interpreted as a local rate. If temperature is currently falling at approximately 21 degrees per minute, a first estimate over 0.1 minute is a decrease of 2.1 degrees. Use the new temperature to estimate the next short interval, and repeat. This is explicit Euler integration: approximate a continuous curve with short straight steps. A larger step assumes an almost constant rate over a longer interval, even though cooling slows as temperature falls. Reducing the step and checking whether predictions settle provides evidence about the numerical approximation; the number of printed decimal places does not provide that evidence by itself.

$$
T_{n+1}=T_n-hk(T_n-T_a),\qquad T_{n+1}-T_a=(1-hk)(T_n-T_a)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8d3557db3b53e7263582572.svg) | Step index and temperature at that step; dimensionless index and°C state. |
| ![Formula](https://ml-biomat.com/static/agent-math/a70852daaf5fec5d910599d1.svg) | Time step in minutes, cooling rate in inverse minutes, and fixed ambient temperature in°C. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e042d48fdfe39efc4daf9ad.svg) | Dimensionless one-step multiplier for the temperature excess. |

Current slope times step size gives a temperature increment. k=.5, h=2 gives multiplier 0 and sends 80°C to 20°C in one step. k=.5, h=4 gives−1, alternating 80 and−40°C. Asymptotic decay requires|1−hk|<1, or 0<hk<2; monotone cooling without crossing ambient requires 0<hk≤1.

For this equation, stability follows from a simple multiplier. Each step multiplies the temperature excess by the same factor. A factor between zero and one produces monotone cooling; between minus one and zero, the numerical temperature crosses ambient repeatedly while its oscillation shrinks. A magnitude greater than one makes the oscillation grow. The coffee has not acquired a heater: the growing excess comes from the discrete rule. The interactive experiment changes cooling rate and step size while comparing the analytic curve, Euler integration, and fourth-order Runge–Kutta. Understanding this numerical error helps identify what a learned surrogate is actually approximating.

## Can a numerical solver make coffee hotter?

Change cooling rate and step size against the exact exponential curve. Every point is computed by the selected integration rule. Axis limits expand to retain overshoot and divergence.

[Figure: Temperature versus time and one-step multiplier](https://ml-biomat.com/tutorials/machine-learning/m29/en/#M29-board)

RK4 evaluates four slopes within each step and averages them with weights 1,2,2,1 divided by 6. The displayed multiplier applies to a full step; a shorter final step ends exactly at 12min.

An ordinary differential equation has one independent variable, commonly time. A partial differential equation also describes variation with variables such as spatial position. Adaptive numerical solvers estimate local error and adjust their steps; SciPy's solve_ivp supplies this kind of interface. Absolute tolerance specifies the allowed absolute error near zero, while relative tolerance scales with state magnitude. Solver tolerance and observation noise concern different parts of the problem: the former controls a computational approximation, and the latter describes measurement variation. Keeping them separate helps determine whether additional numerical refinement has practical value for the available observations.

## 3. A PINN checks a learned curve against an equation

Time-stepping methods advance from an initial state toward the future. A physics-informed neural network first represents the entire unknown curve with a network: supply a time coordinate and receive a state value. Automatic differentiation computes the curve's slope, which is substituted with its state into the governing equation. An imbalance becomes a residual. Training adjusts the curve using residuals at many coordinates together with initial or boundary conditions. The public PINN work by Raissi and colleagues develops this approach for solving equations and discovering their parameters. The central connection is between a differentiable representation and an available scientific relation.

Putting degrees Celsius and minutes directly into a multi-term loss can create scale imbalances. We divide temperature excess by its initial 60 degrees and time by ten minutes. The resulting state u and time tau are dimensionless, and the cooling coefficient becomes 3.5. Nondimensionalization changes coordinates while preserving the process. As with converting currencies to a common accounting unit, comparable scales make error weights easier to interpret. If data, boundary, and residual errors are combined later, their scales and weights must also be defined. A large numerical residual can otherwise reflect the chosen units as much as a poorly represented solution.

$$
u_\theta(\tau)=1+\tau N_\theta(\tau),\qquad r_\theta=\frac{du_\theta}{d\tau}+\kappa u_\theta,\qquad L_r=\frac1{N_c}\sum_{i=1}^{N_c}r_\theta(\tau_i)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/72cc594dfb76298686ce40b5.svg) | Dimensionless τ=t/(10min) and u=(T−20°C)/(60°C); θ denotes network parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/c60c8d085d6caee0e9ac014b.svg) | Scalar network output and dimensionless rate κ=(10min)k=3.5. |
| ![Formula](https://ml-biomat.com/static/agent-math/4e82384609c5e54e34522cc1.svg) | Dimensionless equation residual, its mean square, 64 collocation positions, and their index. |

At τ=0, u is exactly 1. At a point with u=.5 and derivative−1.6, residual is−1.6+3.5×.5=.15 and its square is.0225. Training averages these imbalances. Autodifferentiation retains the derivative graph so the residual loss can subsequently differentiate with respect to θ.

Our representation is one plus tau times a learnable function. At tau equal to zero, the second term vanishes for every set of weights, enforcing the initial condition exactly. This places the condition directly in the representation instead of relying on a large penalty weight. Minimizing only the differential-equation residual would also permit the identically zero curve, which satisfies the cooling equation but starts from a different temperature. The equation and its initial or boundary conditions jointly define the problem. Leaving out one component can produce a decreasing loss for a solution to a different physical question.

The experiment uses 64 collocation positions, two hidden layers of 24 units, and 1,600 updates. Residuals are then checked at 200 separate positions. Maximum normalized-state error within the training interval is approximately 0.00259, or 0.156 degrees after restoring temperature units. Extending the same network to twice the time gives maximum error approximately 0.335; its curve visibly turns upward beyond the constrained interval. This suggests concrete follow-up experiments: extend the residual domain, retain longer-time observations, or use a time-advancing representation, then compare errors over the same interval. A network's ability to return a number at any coordinate does not establish equal accuracy across all coordinates.

![Left: analytic and Euler cooling at k=.35 per minute. Middle: PINN training covers τ≤1, with extrapolation checked to 2. Right: actual residual-loss history.](https://ml-biomat.com/static/tutorials/machine-learning/figures/57f4109ddbaa8782b5d2d354.svg?v=57f4109ddbaa)

Figure 2Left: analytic and Euler cooling at k=.35 per minute. Middle: PINN training covers τ≤1, with extrapolation checked to 2. Right: actual residual-loss history.

## 4. An inverse problem lets observations determine parameters

Keep the cooling law but treat its rate as unknown. Every proposed rate lets the simulator produce predicted temperatures; squared differences from observations measure agreement. If each simulation step is differentiable, the final observation loss can be propagated backward through the steps to determine how a small parameter change affects it. We apply softplus to an unconstrained scalar so that the cooling rate remains positive, then optimize it through an Euler simulator with a 0.05-minute step. The learned object is just one scalar. Identifying a dynamical system from observations does not require a large neural network.

$$
k=\log(1+e^a),\qquad L_{\rm obs}(a)=\frac1m\sum_{j=1}^m\left[T_h(t_j;k(a))-y_j\right]^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ecdfbca3a5b513951afdb7.svg) | Unconstrained scalar a and positive cooling rate k; the code parameterizes its numerical value in inverse minutes. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa1443ee8179ae13c02ba6cb.svg) | Nine observations, observation index, time in minutes, and measured temperature in°C. |
| ![Formula](https://ml-biomat.com/static/agent-math/4fae8c260301ef518f4a8217.svg) | Simulator temperature with step h=.05min; observation MSE has units°C². |

Errors of+1°C and−2°C give MSE(1²+2²)/2=2.5°C². The chain rule propagates through time steps and then k(a); softplus has derivative sigmoid(a). The exponential argument a is dimensionless, while the parameterization attaches the chosen physical unit to k.

Constructed data use a true rate of 0.35 per minute and observations at each integer minute from zero through eight. Independent noise has standard deviation 0.4 degrees, except for the initial state, which is known exactly. Optimization estimates approximately 0.35115 per minute. At a fixed probe parameter, automatic differentiation and centered finite differences agree to a relative difference of about 3.23×10⁻⁹. This checks differentiation of the discrete simulator. Automatic differentiation accurately differentiates the implemented program; its time-discretization error remains governed by the step size. Repeating identification with a smaller step reveals whether that approximation materially affects the estimated parameter.

Whether observations can distinguish parameters is more fundamental than whether an optimizer can continue lowering its loss. If ambient temperature is also unknown, a colder room and a smaller cooling rate can produce similar first-minute curves. Error contours consequently form an elongated valley. Extending the observation window to eight minutes separates these effects more clearly and concentrates the low-error region. This is identifiability. Repeating measurements at one instant mainly helps reduce noise; observing longer or changing the initial temperature can supply a different kind of information. Experimental design should target the information that is missing, rather than automatically collecting more of the same measurements.

![Left: nine observations and continuous curve using the estimated rate; 0.4°C error bars except the exact initial condition. Right: parameter RMSE contours from noiseless targets over two observation windows; stars mark true parameters.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f01f11808e222e75118f862f.svg?v=f01f11808e22)

Figure 3Left: nine observations and continuous curve using the estimated rate; 0.4°C error bars except the exact initial condition. Right: parameter RMSE contours from noiseless targets over two observation windows; stars mark true parameters.

When a trusted law describes only part of a process, a hybrid model can retain that part and learn a correction. For example, a known cooling term could be combined with an unknown time-varying heat input. The 2020 Universal Differential Equations work develops ways of inserting learnable components into differential equations. Inputs, units, and allowed variation of the correction need an explicit definition. A very flexible correction can absorb sensor bias, incorrect physical parameters, and missing mechanisms simultaneously. Comparing it across distinct experimental conditions helps determine which explanation is consistent with what the model has learned.

## 5. FNO maps an entire initial field to an entire final field

A single temperature can approximate the coffee, while a conducting ring requires a value at every location. Initially hot regions spread heat toward cooler surroundings, progressively smoothing sharp variations. In his 1822 Analytical Theory of Heat, Fourier connected heat conduction with trigonometric expansions: a complex shape can be decomposed into waves whose decay can be calculated separately. This represents a complicated curve through amplitudes with a clear interpretation. The attenuation plot shows that finer spatial oscillations decay faster. Constant temperature, corresponding to the zero-frequency mode, remains unchanged in the source-free periodic problem.

$$
\partial_t u=\nu\partial_{xx}u,\quad u(x+1,t)=u(x,t),\qquad \widehat u_k(t)=\widehat u_k(0)e^{-\nu(2\pi k)^2t}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fbbaf8b0fdd040f786401509.svg) | Position, time, relative field, and diffusivity are nondimensionalized in this ring experiment; ν=.01. |
| ![Formula](https://ml-biomat.com/static/agent-math/3fbb79a4d0c9ef0232fdb904.svg) | First partial derivative in time and second partial derivative in position. |
| ![Formula](https://ml-biomat.com/static/agent-math/e785b1453f8f37fb139bdad4.svg) | Integer spatial mode, complex Fourier amplitude, and pi; this k is not the cooling coefficient. |

Twice differentiating a sine or cosine multiplies it by−(2πk)², so each amplitude obeys exponential decay. At t=1, mode 1 multiplies by approximately.673825 and mode 2 by.206153. Mode 0 multiplies by 1, preserving the mean. Periodicity joins the ring endpoints, which are not duplicated in the sampled grid.

For one solution, established numerical methods may already be appropriate. Repeatedly solving related inputs, as in design optimization, creates a different opportunity: learn the mapping from an initial function to its later function. The Fourier Neural Operator, first submitted in 2020 and subsequently published, places part of a learnable transformation in frequency space. Our PINN accepts a coordinate and returns a value of one solution. The FNO accepts an entire initial field and returns its corresponding final field. Consequently, splitting data by independent functions is essential: different grid points on the same curve are parts of one sample.

$$
v_{\ell+1}(x)=\sigma\!\left(W_\ell v_\ell(x)+\mathcal F^{-1}\!\left[R_\ell(k)\mathcal F[v_\ell](k)\right](x)+b_\ell\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f3f6b3ec1592328a300359e.svg) | Twelve-channel field at layerℓ, layer index, and dimensionless position; batch shape B×12×N. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4d9fbc783e21ae17b2cff8a.svg) | Pointwise real 12×12 matrix, 12-vector bias, and GELU, shared across positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/edcf1fc5bb0656f0573915de.svg) | Real-input FFT, its inverse, and a complex 12×12 channel matrix at each retained mode; k=0…5 retained and remaining spectral-branch coefficients set to 0. |

For a single channel and mode, amplitude 2 times weight.5 gives 1; the inverse transform recombines modes in space. Actual blocks also mix channels and include the local branch and nonlinearity. The same spectral weights can be used at N=32 or 64; accuracy for changed input functions is assessed separately.

We actually train a small two-block FNO. Input values are lifted to 12 feature channels. Each block applies a Fourier transform, learns channel mixing at the first six frequency positions, and transforms back to space. A parallel pointwise linear transformation supplies a local contribution; their sum passes through GELU. Spectral weights are complex because waves carry phase as well as amplitude, while the resulting field remains real. Keeping relatively few frequency modes makes the global transformation compact. The local branch and nonlinear activations also contribute spatial detail, so the complete network is more than a single low-pass filter.

There are 96 training functions, 24 validation functions for selecting weights, and 24 independent test functions. Each initial field combines a constant with sine and cosine modes one through four. Exact heat-equation attenuation generates the targets. Training uses 32 grid points and selects update 580 by validation error. Mean per-function relative L2 error is approximately 0.00612. For each curve, take the square root of summed squared pointwise errors and divide by the square root of summed squared target values, then average these ratios over the 24 functions. Evaluating the same held-out functions on 64 grid points gives approximately 0.00612 again. This tests a change of resolution within one parameter setting and one input family. Investigating higher-frequency inputs, different diffusivities, or new boundaries requires adding those conditions to the training and independent evaluation design.

![One FNO predicts the same 24 held-out functions on 32/64 grids; error maps share a symmetric scale. Upper right: training/validation MSE. Lower right: exact heat attenuation, with input modes 1–4 shaded.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d177ee90aa8a2a7be56d89a6.svg?v=d177ee90aa8a)

Figure 4One FNO predicts the same 24 held-out functions on 32/64 grids; error maps share a symmetric scale. Upper right: training/validation MSE. Lower right: exact heat attenuation, with input modes 1–4 shaded.

## 6. A known conservation relation can shape the output directly

A source-free periodic conducting ring exchanges no heat with its surroundings, so its mean temperature stays constant. A generic FNO does not enforce this exactly: our raw output has mean absolute conservation error approximately 9.54×10⁻⁴. Subtracting the prediction's mean and adding the input's mean restores the discrete conservation relation. Geometrically, this translates the whole predicted curve vertically while retaining its spatial variation. Because the exact target has the same required mean, this operation removes the constant-direction error component under the uniform-grid mean-squared-error metric. The physical information is used in a concrete operation whose effect can be measured.

$$
\widetilde u_j=\widehat u_j-\overline{\widehat u}+\overline{u_0},\qquad \overline u=\frac1N\sum_{j=1}^N u_j
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2bba91d3946a6152c4300f05.svg) | Raw prediction, projected prediction at grid point j, and initial field; dimensionless field values. |
| ![Formula](https://ml-biomat.com/static/agent-math/f4e94f360946e2a19f19f355.svg) | Arithmetic mean on a uniform grid, number of positions, and index; N=32 or 64. |

Prediction (1,3) has mean 2. If the initial mean is 1.5, projection gives (.5,2.5), with the required mean 1.5. Hats here denote predictions rather than Fourier coefficients. Nonuniform grids require cell-weighted integral means.

On the 32-point test grid, projection reduces MSE from approximately 5.38×10⁻⁶ to 3.87×10⁻⁶, with mean-conservation error at floating-point rounding scale. The relevant conditions are periodic boundaries, a source-free heat equation, and uniformly weighted grid positions. A heat source, an exchanging boundary, or unequal cell sizes requires a source balance, boundary-flux balance, or weighted spatial integral instead. Calling something a physical constraint becomes useful only after specifying the conserved quantity, the circumstances in which it is conserved, and the discrete calculation that measures it in the available data.

Energy provides another useful structure for a frictionless oscillator. Hamiltonian methods generate motion from an energy function; the 2019 Hamiltonian Neural Networks work makes that function learnable. In continuous time, opposing cross-derivative contributions cancel in the energy derivative. Actual simulation still advances through discrete steps. A continuous conservation structure and the properties of a chosen time integrator therefore need separate examination. Our next example holds the oscillator equation fixed and changes only the integration rule, isolating this numerical layer rather than training another network. The phase portrait and energy trace make the consequences visible together.

$$
H(q,p)=\tfrac12(q^2+p^2),\quad \dot q=p,\quad\dot p=-q,\qquad p_{n+1}=p_n-hq_n,\quad q_{n+1}=q_n+hp_{n+1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a28ff85d15b897481636239.svg) | Dimensionless position, momentum, and energy; mass and stiffness scaled to 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/5034fd939bf7fc7f74b7be0b.svg) | Derivatives with respect to dimensionless time, step index, and step h=.1. |

Continuous energy derivative is q·p+p·(−q)=0. Symplectic Euler starts at (1,0), updates momentum to −0.1, then position to 0.99, giving energy 0.49505. Explicit Euler uses old momentum for position, giving (1, −.1) and energy 0.505. The discrete energy behavior differs from the first step.

![Same dimensionless oscillator, h=.1, 400 steps: explicit versus symplectic Euler. The inset resolves symplectic energy oscillation; the dashed line marks initial energy 0.5.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c17af9dec495572d5a3c5d70.svg?v=c17af9dec495)

Figure 5Same dimensionless oscillator, h=.1, 400 steps: explicit versus symplectic Euler. The inset resolves symplectic energy oscillation; the dashed line marks initial energy 0.5.

Explicit Euler spirals outward. Its initial energy of 0.5 reaches approximately 26.76 after 400 steps. Symplectic Euler first updates momentum and then uses that new momentum to update position. Its trajectory remains near the initial orbit, with energy oscillating between approximately 0.476 and 0.526. The inset reveals this bounded variation rather than hiding it behind the much larger explicit-Euler scale. Symplectic integration preserves phase-space geometry; it does not generally conserve the original energy exactly at every step. For learned dynamics, checking the continuous vector field, one-step predictions, and long-time trajectories separately helps locate where an error originates and accumulates.

## 7. Discovering an equation begins with a library of possible terms

When the governing rule is unknown, start with candidate expressions such as a constant, the state, its square, and its cube. Seek a small subset that explains observed derivatives. SINDy, introduced by Brunton, Proctor, and Kutz in 2016, organizes this task as sparse regression. Its output is an equation that can be read, analyzed, and integrated again. A linear term describes change proportional to the state, while a negative quadratic term can express a limiting effect that strengthens as the state grows. Discovery remains tied to the candidate library: an absent mechanism does not appear merely because the regression coefficients are estimated precisely.

$$
\dot{\boldsymbol u}\approx\Theta(\boldsymbol u)\boldsymbol\xi,\qquad \Theta(u_i)=(1,u_i,u_i^2,u_i^3)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/100f8a1637ae5388f5005717.svg) | Dimensionless states pooled across three trajectories, estimated derivatives in inverse minutes, and sample index. |
| ![Formula](https://ml-biomat.com/static/agent-math/82770301c5be3fcb36b932c8.svg) | Design matrix with 4 candidate terms per row and 4 sparse coefficients; all coefficients have inverse-minute units because u is dimensionless. |

At u=.5, the library row is (1, .5, .25, .125). Multiplying by (0,1.2, −.8,0) gives derivative 0.4 per minute. Thresholded regression alternates least squares, removal of small coefficients, and refitting retained columns. The threshold 0.08 applies to these variable and column scales; training derivatives are estimated from noisy observations.

Three growth trajectories with different initial states supply the training data. The true equation contains 1.2u and−0.8u², with dimensionless state and time in minutes. Sampling every 0.02 minute is followed by state noise with standard deviation 0.002. Dividing differences between neighboring observations by the time interval is simple, but amplifies noise. Errors from both measurements enter the numerator, while a small denominator can create large derivative fluctuations. We instead fit local cubic polynomials over 21-point windows and differentiate those polynomials. Removing ten points at each edge reduces the effect of asymmetric boundary windows on the regression.

Regression first fits all terms, removes coefficients whose absolute values are below 0.08, and refits the retained terms repeatedly. It identifies approximately 1.19949u−0.79938u², setting constant and cubic coefficients to zero. Raw finite-difference derivative RMSE is approximately 0.0725, compared with 0.00958 after local-polynomial differentiation. The threshold depends on units and column scaling. Changing state units changes the meaning of a fixed numerical threshold, and larger libraries may contain strongly correlated columns. In a broader study, compare several thresholds and inspect whether independent trajectories consistently support the same retained terms.

![Estimate derivatives from noisy states, select library terms, and evaluate a new u₀=.8 trajectory over 0–8 min. Training trajectories cover 0–4 min; the vertical line marks that boundary.](https://ml-biomat.com/static/tutorials/machine-learning/figures/537add67d3b60141aa566baf.svg?v=537add67d3b6)

Figure 6Estimate derivatives from noisy states, select library terms, and evaluate a new u₀=.8 trajectory over 0–8 min. Training trajectories cover 0–4 min; the vertical line marks that boundary.

Training trajectories cover zero through four minutes. We then integrate the identified equation from a new initial state of 0.8 through eight minutes, obtaining maximum state error approximately 0.000520. This changes both initial condition and time horizon, complementing the derivative fit. Other symbolic-regression approaches search expression trees assembled from operators such as addition, multiplication, and exponentiation. A larger search space makes complexity control, dimensional consistency, and independent data increasingly useful. A concise formula supports interpretation; its behavior under relevant changes in experimental conditions helps determine which aspects of the underlying mechanism it captures.

## 8. The complete experiment connects numerical baselines and learned models

The program below includes all five groups of calculations through one entry point. It saves PINN and FNO weights, constructed data, training traces, independent predictions, and scientific figures. Cooling begins with an analytic baseline before checking the network and simulator. Operator learning splits by functions and compares two resolutions on the same test functions. Equation discovery retains raw noisy states, estimated derivatives, and final coefficients, allowing a questionable term to be traced through the calculation. Fixed seeds reproduce the particular numerical examples, while explicit data-generating rules make the experimental conditions inspectable.

### Complete Python: five reproducible experiments

NumPy, SciPy, and PyTorch perform the computations.summary.json records metrics; experiment.npz retains data and predictions; pinn.pt and fno.pt contain weights.

```
"""Cooling, a small Fourier neural operator, and sparse equation discovery.

All data are constructed from the equations stated in the chapter.
The program writes only to the selected output directory.
"""
from pathlib import Path
import argparse
import copy
import json

import numpy as np
import torch
from torch import nn
from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
torch.manual_seed(2901)
rng = np.random.default_rng(2901)
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=Path('results'))
parser.add_argument('--language', choices=['zh', 'en'], default='en')
args = parser.parse_args()
out = args.output
out.mkdir(parents=True, exist_ok=True)
zh = args.language == 'zh'


def tr(chinese, english):
    return chinese if zh else english


plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
    'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
    'svg.fonttype': 'none', 'figure.facecolor': '#faf9f5',
    'axes.facecolor': '#faf9f5',
})


def save(fig, name):
    fig.savefig(out / f'{name}-{args.language}.svg', bbox_inches='tight')
    fig.savefig(out / f'{name}-{args.language}.png', dpi=130, bbox_inches='tight')
    plt.close(fig)


def euler_cooling(k, step, stop=12.0):
    time, temperature = [0.0], [80.0]
    while time[-1] < stop - 1e-12:
        dt = min(step, stop - time[-1])
        temperature.append(temperature[-1] - dt * k * (temperature[-1] - 20))
        time.append(time[-1] + dt)
    return np.array(time), np.array(temperature)


# A forward PINN: tau=t/10, u=(T-20)/60, du/dtau + 3.5*u=0.
net = nn.Sequential(nn.Linear(1, 24), nn.Tanh(), nn.Linear(24, 24),
                    nn.Tanh(), nn.Linear(24, 1)).double()
optimizer = torch.optim.Adam(net.parameters(), lr=.003)
collocation = torch.linspace(0, 1, 64, dtype=torch.float64)[:, None]
trace = []
for iteration in range(1600):
    tau = collocation.clone().requires_grad_(True)
    u = 1 + tau * net(tau)  # The initial condition is exact for any parameters.
    derivative = torch.autograd.grad(u.sum(), tau, create_graph=True)[0]
    residual = derivative + 3.5 * u
    loss = residual.square().mean()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if iteration % 40 == 0:
        trace.append([iteration, loss.item()])
grid = torch.linspace(0, 2, 401, dtype=torch.float64)[:, None]
with torch.no_grad():
    pinn = (1 + grid * net(grid)).numpy().ravel()
tau = grid.numpy().ravel()
exact = np.exp(-3.5 * tau)
test_tau = torch.tensor(np.linspace(.0025, .9975, 200)[:, None], requires_grad=True)
test_u = 1 + test_tau * net(test_tau)
test_derivative = torch.autograd.grad(test_u.sum(), test_tau)[0]
pinn_residual = (test_derivative + 3.5 * test_u).detach().numpy().ravel()
torch.save(net.state_dict(), out / 'pinn.pt')

# A differentiable numerical simulator estimates k from noisy observations.
obs_time = np.arange(0, 8.01, 1.0)
obs = 20 + 60 * np.exp(-.35 * obs_time) + rng.normal(0, .4, len(obs_time))
obs[0] = 80  # Initial condition is measured exactly in this constructed example.
dt = .05
obs_indices = torch.tensor(np.rint(obs_time / dt).astype(int))


def simulator(k):
    temperatures = [torch.tensor(80., dtype=torch.float64)]
    for _ in range(int(8 / dt)):
        temperatures.append(temperatures[-1] - dt * k * (temperatures[-1] - 20))
    return torch.stack(temperatures)[obs_indices]


probe_k = torch.tensor(.25, dtype=torch.float64, requires_grad=True)
probe_loss = (simulator(probe_k) - torch.tensor(obs)).square().mean()
automatic_gradient = torch.autograd.grad(probe_loss, probe_k)[0].item()
eps = 1e-5
with torch.no_grad():
    finite_gradient = (((simulator(torch.tensor(.25 + eps, dtype=torch.float64)) - torch.tensor(obs)).square().mean()
                       - (simulator(torch.tensor(.25 - eps, dtype=torch.float64)) - torch.tensor(obs)).square().mean()) / (2 * eps)).item()
raw_k = torch.tensor(-1.5, dtype=torch.float64, requires_grad=True)
inverse_optimizer = torch.optim.Adam([raw_k], lr=.04)
inverse_trace = []
for iteration in range(350):
    k = nn.functional.softplus(raw_k)
    inverse_loss = (simulator(k) - torch.tensor(obs)).square().mean()
    inverse_optimizer.zero_grad()
    inverse_loss.backward()
    inverse_optimizer.step()
    if iteration % 10 == 0:
        inverse_trace.append([iteration, k.item(), inverse_loss.item()])
estimated_k = nn.functional.softplus(raw_k).item()

# A genuine two-block FNO maps an initial periodic field to its field at time1.
nu = .01


def fields(coefficients, resolution, final=False):
    x = np.arange(resolution) / resolution
    result = np.repeat(coefficients[:, :1], resolution, axis=1)
    for mode in range(1, 5):
        amplitude = np.exp(-nu * (2 * np.pi * mode) ** 2) if final else 1.
        result += amplitude * (
            coefficients[:, 2 * mode - 1:2 * mode] * np.cos(2 * np.pi * mode * x)
            + coefficients[:, 2 * mode:2 * mode + 1] * np.sin(2 * np.pi * mode * x))
    return result.astype('float32')


coefficients = rng.normal(0, .45, (144, 9))
coefficients[:, 0] = rng.uniform(-.5, .5, 144)
train_x = torch.tensor(fields(coefficients[:96], 32))[:, None]
train_y = torch.tensor(fields(coefficients[:96], 32, True))[:, None]
valid_x = torch.tensor(fields(coefficients[96:120], 32))[:, None]
valid_y = torch.tensor(fields(coefficients[96:120], 32, True))[:, None]


class SpectralLayer(nn.Module):
    def __init__(self, width, modes):
        super().__init__()
        self.modes = modes
        self.weights = nn.Parameter(torch.randn(width, width, modes, dtype=torch.cfloat) / width)

    def forward(self, values):
        transformed = torch.fft.rfft(values, dim=-1)
        result = torch.zeros(values.shape[0], values.shape[1], transformed.shape[-1],
                             dtype=torch.cfloat, device=values.device)
        result[:, :, :self.modes] = torch.einsum(
            'bik,iok->bok', transformed[:, :, :self.modes], self.weights)
        return torch.fft.irfft(result, n=values.shape[-1], dim=-1)


class SmallFNO(nn.Module):
    def __init__(self):
        super().__init__()
        self.lift = nn.Conv1d(1, 12, 1)
        self.spectral = nn.ModuleList([SpectralLayer(12, 6) for _ in range(2)])
        self.local = nn.ModuleList([nn.Conv1d(12, 12, 1) for _ in range(2)])
        self.readout = nn.Conv1d(12, 1, 1)

    def forward(self, values):
        hidden = self.lift(values)
        for spectral, local in zip(self.spectral, self.local):
            hidden = nn.functional.gelu(spectral(hidden) + local(hidden))
        return self.readout(hidden)


torch.manual_seed(2902)
fno = SmallFNO()
fno_optimizer = torch.optim.Adam(fno.parameters(), lr=.003)
fno_rng = torch.Generator().manual_seed(2903)
best_validation, best_state, best_step = float('inf'), None, None
fno_trace = []
for iteration in range(601):
    indices = torch.randint(96, (32,), generator=fno_rng)
    loss = (fno(train_x[indices]) - train_y[indices]).square().mean()
    fno_optimizer.zero_grad()
    loss.backward()
    fno_optimizer.step()
    if iteration % 20 == 0:
        with torch.no_grad():
            validation = (fno(valid_x) - valid_y).square().mean().item()
        fno_trace.append([iteration, loss.item(), validation])
        if validation < best_validation:
            best_validation = validation
            best_state = copy.deepcopy(fno.state_dict())
            best_step = iteration
fno.load_state_dict(best_state)
torch.save(fno.state_dict(), out / 'fno.pt')
operator_results = {}
operator_arrays = {}
for resolution in [32, 64]:
    inputs = fields(coefficients[120:], resolution)
    targets = fields(coefficients[120:], resolution, True)
    with torch.no_grad():
        prediction = fno(torch.tensor(inputs)[:, None]).numpy()[:, 0]
    conserved = prediction - prediction.mean(1, keepdims=True) + inputs.mean(1, keepdims=True)
    relative = np.linalg.norm(prediction - targets, axis=1) / np.linalg.norm(targets, axis=1)
    operator_results[str(resolution)] = {
        'mean_relative_l2': float(relative.mean()),
        'mse': float(np.mean((prediction - targets) ** 2)),
        'projected_mse': float(np.mean((conserved - targets) ** 2)),
        'mean_conservation_error': float(np.mean(np.abs(prediction.mean(1) - inputs.mean(1)))),
        'projected_conservation_max_error': float(np.max(np.abs(conserved.mean(1) - inputs.mean(1)))),
        'identity_mse': float(np.mean((inputs - targets) ** 2)),
    }
    operator_arrays.update({f'input_{resolution}': inputs, f'target_{resolution}': targets,
                            f'prediction_{resolution}': prediction, f'projected_{resolution}': conserved})

# Sparse identification uses smoothed numerical derivatives, not known derivatives.
time = np.arange(0, 4.001, .02)


def logistic(t, initial):
    capacity = 1.2 / .8
    return capacity / (1 + (capacity / initial - 1) * np.exp(-1.2 * t))


clean = np.array([logistic(time, initial) for initial in [.2, .5, 1.]])
noisy = clean + rng.normal(0, .002, clean.shape)
smooth = savgol_filter(noisy, 21, 3, axis=1)
estimated_derivatives = savgol_filter(noisy, 21, 3, deriv=1, delta=.02, axis=1)
raw_derivatives = np.gradient(noisy, .02, axis=1)
states = smooth[:, 10:-10].ravel()
derivatives = estimated_derivatives[:, 10:-10].ravel()
library = np.stack([np.ones_like(states), states, states**2, states**3], axis=1)
coefficients_sindy = np.linalg.lstsq(library, derivatives, rcond=None)[0]
for _ in range(8):
    active = np.abs(coefficients_sindy) >= .08
    coefficients_sindy[~active] = 0
    coefficients_sindy[active] = np.linalg.lstsq(library[:, active], derivatives, rcond=None)[0]
rollout_time = np.linspace(0, 8, 401)
identified = solve_ivp(lambda t, x: sum(c * x**i for i, c in enumerate(coefficients_sindy)),
                       [0, 8], [.8], t_eval=rollout_time, rtol=1e-9, atol=1e-11).y[0]
true_derivative = 1.2 * clean - .8 * clean**2

# Same oscillator, different integrators: geometry changes long-time energy.
position = {'euler': [1.], 'symplectic': [1.]}
momentum = {'euler': [0.], 'symplectic': [0.]}
for _ in range(400):
    x, v = position['euler'][-1], momentum['euler'][-1]
    position['euler'].append(x + .1 * v)
    momentum['euler'].append(v - .1 * x)
    x, v = position['symplectic'][-1], momentum['symplectic'][-1]
    new_v = v - .1 * x
    momentum['symplectic'].append(new_v)
    position['symplectic'].append(x + .1 * new_v)
energy = {key: .5 * (np.array(position[key])**2 + np.array(momentum[key])**2) for key in position}

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
t = np.linspace(0, 12, 401)
axes[0].plot(t, 20 + 60 * np.exp(-.35 * t), color='#183a4c', label=tr('解析解', 'Analytic'))
for step, color in [(1, '#267b7d'), (6, '#bd653f')]:
    et, ey = euler_cooling(.35, step)
    axes[0].plot(et, ey, 'o--', color=color, label=f'Euler h={step}')
axes[0].axhline(20, color='#aaa', lw=.8)
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('温度 / °C', 'Temperature / °C'), title=tr('A  步长改变数值行为', 'A  Step size changes dynamics'))
axes[0].legend(fontsize=8)
axes[1].plot(tau, exact, color='#183a4c', label=tr('解析解', 'Analytic'))
axes[1].plot(tau, pinn, color='#267b7d', label='PINN')
axes[1].axvline(1, color='#bd653f', ls='--')
axes[1].set(xlabel=tr('无量纲时间 τ', 'Dimensionless time τ'), ylabel=tr('无量纲温差 u', 'Dimensionless excess u'), title=tr('B  训练区间与外推', 'B  Training interval and extrapolation'))
axes[1].legend(fontsize=8)
axes[2].semilogy(np.array(trace)[:, 0], np.array(trace)[:, 1], color='#267b7d')
axes[2].set(xlabel=tr('更新次数', 'Updates'), ylabel=tr('残差均方', 'Mean squared residual'), title=tr('C  自动微分形成约束', 'C  Autodifferentiated constraint'))
save(fig, 'cooling')

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
axes[0].errorbar(obs_time, obs, yerr=np.r_[0, np.repeat(.4, len(obs_time)-1)], fmt='o', color='#bd653f', label=tr('观测 ±1σ', 'Observations ±1σ'))
axes[0].plot(t, 20 + 60 * np.exp(-estimated_k * t), color='#267b7d', label=tr('估计参数的连续解', 'Continuous curve at fitted k'))
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('温度 / °C', 'Temperature / °C'), title=tr('A  可微求解器识别参数', 'A  Identify a simulator parameter'))
axes[0].legend(fontsize=8)
kk, ambient = np.meshgrid(np.linspace(.15, .6, 101), np.linspace(5, 35, 101))
for ax, stop in zip(axes[1:], [1, 8]):
    sample_t = np.linspace(0, stop, 9)
    target = 20 + 60 * np.exp(-.35 * sample_t)
    predicted = ambient[..., None] + (80 - ambient[..., None]) * np.exp(-kk[..., None] * sample_t)
    rmse = np.sqrt(np.mean((predicted - target)**2, axis=-1))
    contours = ax.contour(kk, ambient, rmse, levels=[.2, .5, 1, 2, 4, 8], cmap='viridis')
    ax.clabel(contours, fontsize=8)
    ax.plot(.35, 20, '*', color='#bd653f', ms=11)
    ax.set(xlabel=tr('冷却率 k / min$^{-1}$', 'Rate k / min$^{-1}$'), ylabel=tr('环境温度 / °C', 'Ambient / °C'), title=tr(f'0–{stop} min：温度RMSE等值线', f'0–{stop} min: temperature-RMSE contours'))
save(fig, 'inverse')

fig, axes = plt.subplots(2, 3, figsize=(13.5, 7), layout='constrained')
error_limit = max(float(np.max(np.abs(operator_arrays[f'prediction_{n}'] - operator_arrays[f'target_{n}']))) for n in [32, 64])
for column, resolution in enumerate([32, 64]):
    x = np.arange(resolution) / resolution
    for values, label, color in [(operator_arrays[f'input_{resolution}'][0], tr('初始', 'Initial'), '#aaa'),
                                 (operator_arrays[f'target_{resolution}'][0], tr('真实终态', 'Exact final'), '#183a4c'),
                                 (operator_arrays[f'prediction_{resolution}'][0], 'FNO', '#bd653f')]:
        axes[0, column].plot(x, values, label=label, color=color)
    axes[0, column].set(xlabel='x / L', ylabel=tr('场值', 'Field value'), title=f'N={resolution}')
    axes[0, column].legend(fontsize=8)
    error = operator_arrays[f'prediction_{resolution}'] - operator_arrays[f'target_{resolution}']
    im = axes[1, column].imshow(error, aspect='auto', extent=[0, 1, 24, 0], cmap='RdBu_r', vmin=-error_limit, vmax=error_limit)
    axes[1, column].set(xlabel='x / L', ylabel=tr('独立函数编号', 'Held-out function'), title=tr('全部24个函数的误差', 'Errors for all 24 held-out functions'))
    fig.colorbar(im, ax=axes[1, column], label=tr('预测−真实', 'Predicted−exact'))
ft = np.array(fno_trace)
axes[0, 2].semilogy(ft[:, 0], ft[:, 1], label=tr('训练批次', 'Training batch'), color='#267b7d')
axes[0, 2].semilogy(ft[:, 0], ft[:, 2], label=tr('验证函数', 'Validation functions'), color='#bd653f')
axes[0, 2].set(xlabel=tr('更新次数', 'Updates'), ylabel='MSE', title=tr('按验证函数选择权重', 'Select by validation functions'))
axes[0, 2].legend(fontsize=8)
modes = np.arange(0, 9)
axes[1, 2].semilogy(modes, np.exp(-nu * (2 * np.pi * modes)**2), 'o-', color='#267b7d')
axes[1, 2].axvspan(.5, 4.5, color='#267b7d', alpha=.1)
axes[1, 2].set(xlabel=tr('Fourier模式 k', 'Fourier mode k'), ylabel=tr('精确衰减因子', 'Exact attenuation'), title=tr('高频更快消退', 'High frequencies decay faster'))
save(fig, 'operator')

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
axes[0].plot(time, true_derivative[0], color='#183a4c', label=tr('真实导数', 'Exact derivative'))
axes[0].plot(time, raw_derivatives[0], color='#bbb', alpha=.6, label=tr('直接差分', 'Finite difference'))
axes[0].plot(time, estimated_derivatives[0], color='#bd653f', label=tr('局部多项式导数', 'Local-polynomial derivative'))
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel='du/dt / min$^{-1}$', title=tr('A  求导会放大噪声', 'A  Differentiation amplifies noise'))
axes[0].legend(fontsize=8)
axes[1].bar(np.arange(4) - .18, [0, 1.2, -.8, 0], .36, label=tr('真实', 'True'), color='#183a4c')
axes[1].bar(np.arange(4) + .18, coefficients_sindy, .36, label=tr('识别', 'Identified'), color='#bd653f')
axes[1].set(xticks=np.arange(4), xticklabels=['1', 'u', 'u²', 'u³'], ylabel=tr('系数 / min$^{-1}$', 'Coefficient / min$^{-1}$'), title=tr('B  从候选库选择表达式', 'B  Select terms from a library'))
axes[1].legend(fontsize=8)
axes[2].plot(rollout_time, logistic(rollout_time, .8), color='#183a4c', label=tr('真实', 'True'))
axes[2].plot(rollout_time, identified, '--', color='#bd653f', label='SINDy')
axes[2].axvline(4, color='#aaa', ls=':')
axes[2].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('无量纲状态 u', 'Dimensionless state u'), title=tr('C  新初值与更长时间', 'C  New initial state and longer time'))
axes[2].legend(fontsize=8)
save(fig, 'discovery')

fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
for key, color in [('euler', '#bd653f'), ('symplectic', '#267b7d')]:
    label = tr('显式Euler', 'Explicit Euler') if key == 'euler' else tr('辛Euler', 'Symplectic Euler')
    axes[0].plot(position[key], momentum[key], color=color, label=label)
    axes[1].plot(np.arange(401)*.1, energy[key], color=color, label=label)
axes[0].set(xlabel='q', ylabel='p', title=tr('相平面轨迹', 'Phase-space trajectory'))
axes[0].set_aspect('equal')
axes[0].legend(fontsize=8)
axes[1].axhline(.5, color='#aaa', ls='--')
axes[1].set(xlabel=tr('无量纲时间', 'Dimensionless time'), ylabel=tr('能量 H', 'Energy H'), title=tr('离散更新改变长期能量', 'Discrete updates change long-time energy'))
axes[1].legend(fontsize=8)
inset = axes[1].inset_axes([.13, .42, .48, .43])
inset.plot(np.arange(401)*.1, energy['symplectic'], color='#267b7d', lw=.8)
inset.axhline(.5, color='#aaa', ls='--', lw=.7)
inset.set(ylim=(.47, .53), title=tr('辛Euler：能量放大', 'Symplectic energy: zoom'))
inset.tick_params(labelsize=7)
inset.title.set_fontsize(8)
save(fig, 'structure')

summary = {
    'pinn': {'inside_max_abs_error': float(np.max(np.abs(pinn[tau <= 1] - exact[tau <= 1]))),
             'outside_max_abs_error': float(np.max(np.abs(pinn[tau > 1] - exact[tau > 1]))),
             'independent_residual_rmse': float(np.sqrt(np.mean(pinn_residual**2))),
             'initial_condition_error': abs(float(pinn[0])-1), 'updates':1600},
    'inverse': {'true_k':.35, 'estimated_k':estimated_k, 'step':dt,
                'automatic_gradient':automatic_gradient, 'finite_gradient':finite_gradient,
                'gradient_relative_error':abs(automatic_gradient-finite_gradient)/abs(automatic_gradient)},
    'operator': {'train_functions':96, 'validation_functions':24, 'test_functions':24,
                 'selected_step':best_step, 'resolutions':operator_results},
    'sindy': {'coefficients':coefficients_sindy.tolist(), 'active_terms':int(np.count_nonzero(coefficients_sindy)),
              'derivative_rmse_raw':float(np.sqrt(np.mean((raw_derivatives[:,10:-10]-true_derivative[:,10:-10])**2))),
              'derivative_rmse_smooth':float(np.sqrt(np.mean((estimated_derivatives[:,10:-10]-true_derivative[:,10:-10])**2))),
              'heldout_rollout_max_error':float(np.max(np.abs(identified-logistic(rollout_time,.8))))},
    'structure':{'euler_final_energy':float(energy['euler'][-1]),
                 'symplectic_energy_min':float(energy['symplectic'].min()),
                 'symplectic_energy_max':float(energy['symplectic'].max())},
    'hand':{'euler_k05_h2_final':float(euler_cooling(.5,2)[1][-1]),
            'euler_k05_h4_final':float(euler_cooling(.5,4)[1][-1]),
            'heat_mode1_factor':float(np.exp(-.01*(2*np.pi)**2))}
}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
np.savez_compressed(out/'experiment.npz',tau=tau,pinn=pinn,exact=exact,
                    collocation=collocation.numpy(),pinn_trace=trace,pinn_test_residual=pinn_residual,
                    obs_time=obs_time,observations=obs,inverse_trace=inverse_trace,
                    operator_coefficients=coefficients,fno_trace=fno_trace,
                    sindy_time=time,sindy_clean=clean,sindy_noisy=noisy,
                    sindy_derivatives=estimated_derivatives,sindy_coefficients=coefficients_sindy,
                    rollout_time=rollout_time,identified_rollout=identified,
                    euler_energy=energy['euler'],symplectic_energy=energy['symplectic'],**operator_arrays)
print(json.dumps(summary,indent=2))
```

On a first reading, follow the temperature list inside simulator. Each new state depends on the previous state and cooling rate, and observation loss differentiates through that chain. Then inspect SpectralLayer: grid length comes from the current input, while the learned frequency-channel weights are reused. This explains how a model trained with 32 positions can compute an output with 64. Finally, read the library construction and thresholded-regression loop. Change a candidate term or noise level and observe the resulting equation, derivative error, and long-time trajectory together. Each part of the program corresponds to a concrete figure discussed above.

Choosing a scientific-learning method becomes clearer after listing what is already known and what must be inferred. For a small number of solves with known equations, start with established numerical methods. For many repeated conditions, assess an operator surrogate's training cost against subsequent evaluation benefits. For a few unknown parameters, connect observations to a differentiable simulator. For a missing mechanism that should become a readable expression, begin with a scientifically meaningful candidate library. Keep units, boundaries, data splits, and error definitions beside the model so that another researcher can understand and extend the resulting calculation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M29.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Physics Informed Deep Learning](https://maziarraissi.github.io/PINNs/)

   Continuous-time residuals, conditions, and parameter discovery.
2. [Fourier Neural Operator for Parametric PDEs](https://arxiv.org/abs/2010.08895)

   Original operator-learning paper and history.
3. [NeuralOperator: Fourier Neural Operators](https://neuraloperator.github.io/dev/theory_guide/fno.html)

   Spectral layers, local terms, and resolution changes.
4. [Discovering governing equations by sparse identification](https://arxiv.org/abs/1509.03580)

   Sparse libraries and equation discovery.
5. [PySINDy documentation](https://pysindy.readthedocs.io/en/stable/)

   System identification and extensible implementation.
6. [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)

   Independent trajectory integration and tolerances.
7. [Hamiltonian Neural Networks](https://arxiv.org/abs/1906.01563)

   Learned Hamiltonians and continuous conservation.
8. [Fourier, Théorie analytique de la chaleur (1822)](https://www.e-rara.ch/zut/content/titleinfo/6187666)

   Original monograph connecting heat conduction and Fourier representation.

   Historical work linked; no scanned image reproduced
9. [Universal Differential Equations for Scientific Machine Learning](https://arxiv.org/abs/2001.04385)

   Embedding learnable structures within known dynamics.

   Primary paper
10. [PySINDy STLSQ](https://pysindy.readthedocs.io/en/latest/generated/pysindy.optimizers.STLSQ.html)

    Thresholded regression, column scaling, and refitting.

    Official documentation
