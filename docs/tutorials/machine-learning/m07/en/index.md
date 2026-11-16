# Let evidence update belief: Bayesian models, hidden states and Gaussian processes

Source: https://ml-biomat.com/tutorials/machine-learning/m07/en/
Language: en

From a hand-computed posterior after seven successes to partial pooling, message passing and inspectable approximations.

## How much do seven successes tell us?

A new shop welcomes ten customers, seven of whom make a purchase. Reporting a purchase rate of seventy percent is easy, but will seven of the next ten customers also buy something? If another shop serves a thousand customers and records seven hundred purchases, are its seventy percent and the new shop's seventy percent equally informative? These questions require an estimate to reflect how much evidence supports it. Bayesian inference treats the unknown success rate as an uncertain quantity, describes its possible values, and lets observations change the support assigned to those values.

A prior expresses knowledge before seeing the current data. A likelihood describes how readily those data would arise under a particular parameter value. The posterior combines them into a distribution after observing the data. Bayes's posthumous essay, communicated by Price in 1763, considered inference about an unknown chance from observed events. Modern models extend far beyond that setting, but reasoning backward from outcomes to their probabilistic generating mechanism remains a useful entry point. Updating makes the relation between assumptions and new evidence explicit rather than creating certainty without a basis.

$$
p(\theta\mid D)=\frac{p(D\mid\theta)p(\theta)}{p(D)},\qquad p(D)=\int p(D\mid\theta)p(\theta)\,d\theta
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f0f92154fe22663cdf94a902.svg) | Observed data and unknown parameter; theta here is a unitless success probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/e28cb8f34e18057679d10fca.svg) | Prior density, likelihood and posterior density; density units follow parameter/observation units, and likelihood as a function of theta need not integrate to one over theta. |
| ![Formula](https://ml-biomat.com/static/agent-math/10ef1a90ef491e62d41ffc76.svg) | Evidence, integration over parameter values and integration variable; discrete parameters use a sum. |

Two candidates theta=0.5 and 0.8 each have prior weight 0.5. One success gives weighted likelihoods 0.25 and 0.4, evidence 0.65 and posterior weights 5/13 and 8/13. The denominator normalizes the candidate weights.

Suppose there are two candidate coins, with head probabilities 0.5 and 0.8, equally likely before a toss. Observing one head favors the second coin, giving it posterior probability 8/13. Evidence has changed their relative support without identifying the coin with certainty. Allowing the success rate to vary continuously between zero and one replaces two weights with a density curve. High-density regions receive more support, while the spread retains uncertainty from finite observations. An exact value has probability zero under a continuous distribution; probability belongs to an interval's area under the curve.

Seven successes in ten trials connect the analytic calculations, interactive experiment and sampling example throughout this chapter. Trials are modeled as independent conditional on a shared success rate, which remains constant during the observations. Different customer channels or a price change during the experiment would motivate additional structure. Expressing such conditions inside the model determines which observations can update a common parameter and which differences require their own variables. The resulting probability calculation can then be traced back to a specific account of how the records were generated.

## A hand-computable posterior can predict future results

The Beta distribution lives between zero and one, making it suitable for an unknown success probability. Its two positive parameters control shape: equal parameters give symmetry around one half, while a relatively larger first parameter favors higher probabilities. Under binomial observations, multiplying a Beta prior by the likelihood produces another Beta distribution. Add successes to the first parameter and failures to the second. This conjugacy preserves a convenient distributional family after updating, letting us understand the probability operations before introducing more demanding computational methods.

$$
\theta\sim\operatorname{Beta}(a,b),\quad s\mid\theta\sim\operatorname{Binomial}(n,\theta),\quad\theta\mid s\sim\operatorname{Beta}(a+s,b+n-s),\quad\mathbb E[\theta\mid s]=\frac{a+s}{a+b+n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | Positive dimensionless Beta shape parameters; they act as prior pseudocounts without requiring literal historical observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/c1d92ccdad2a809dfc0820ba.svg) | Trial count, success count and common success probability; 0≤s≤n and trials are conditionally independent. |
| ![Formula](https://ml-biomat.com/static/agent-math/479c4b5409f673fd67c54b6e.svg) | Beta distribution, binomial distribution, expectation and distribution notation; success counts are counts and probabilities unitless. |

The Beta density has powers a−1 and b−1 on theta and one minus theta; the likelihood adds powers s and n−s. With a=b=2, s=7 and n=10, the posterior is Beta(9,5) with mean 9/14. When both posterior shapes exceed one, MAP is (9−1)/(9+5−2)=2/3.

Updating Beta(2,2) with seven successes and three failures gives Beta(9,5). The posterior mean is 9/14, approximately 0.6429, and its maximum-density location, the MAP estimate, is 8/12, approximately 0.6667. The observed fraction is 0.7. These quantities answer different questions: the mean averages the posterior, MAP selects its highest-density location, and the observed fraction summarizes counts. The equal-tailed 95% posterior interval is approximately 0.386 to 0.861. Under the specified model and prior, posterior probability for the parameter to fall inside that interval is 95%.

## Add evidence one observation at a time

Blue is the updated success-rate density and gray the prior. Bars show probabilities for success counts in ten future trials. The initial seven successes and three failures can be extended or undone one at a time.

[Figure: Beta posterior and future success-count distribution](https://ml-biomat.com/tutorials/machine-learning/m07/en/#M07-plot)

The next ten trials introduce another source of variation. Even with a fixed success probability, individual outcomes fluctuate. Posterior prediction calculates future-outcome probabilities at each possible parameter value and averages them using posterior weights. The code gives a future success-count mean of about 6.429 and variance 3.673. Fixing the parameter at its posterior mean instead gives a binomial variance of only about 2.296. The extra spread comes from remaining parameter uncertainty. The two sets of probability bars share a mean while allocating different mass toward the tails.

$$
P(K=k\mid D)=\int_0^1P(K=k\mid\theta)p(\theta\mid D)\,d\theta={m\choose k}\frac{B(a_*+k,b_*+m-k)}{B(a_*,b_*)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4c44806b2cfd835465c6e2b3.svg) | Random future success count, a possible count and future trial count, with k from zero to m. |
| ![Formula](https://ml-biomat.com/static/agent-math/621c406e4bb4bb0dbf1ed09f.svg) | Observed data, success probability and updated Beta shape parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/77b70a684b1e323b868811a4.svg) | Beta function, number of ways to place k successes among m trials and probability; the result is a unitless discrete probability. |

The Beta function normalizes the Beta density. Future binomial likelihood adds powers, and integration gives a ratio of Beta functions. For posterior Beta(9,5), ten future trials have mean 10×9/14≈6.429 and variance 10×9×5×24/(14²×15)≈3.673. Fixing theta at 9/14 gives variance 10×9/14×5/14≈2.296.

![Left: prior and posterior, with equal-tailed 95% posterior interval. Middle: full posterior prediction versus a binomial model fixed at the posterior mean. Right: equal success fractions with different sample counts.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6de637a11307be6ea381ac0e.svg?v=6de637a11307)

Figure 1Left: prior and posterior, with equal-tailed 95% posterior interval. Middle: full posterior prediction versus a binomial model fixed at the posterior mean. Right: equal success fractions with different sample counts.

Conjugacy extends beyond coins. Normal observations with suitable normal priors, and Poisson counts with Gamma priors, also lead to tractable updates. Before selecting a prior, simulate the observations it permits. If it predicts a small shop regularly receiving more customers than its physical capacity allows, reconsider the model and its units. Prior prediction translates parameter assumptions into recognizable outcomes; posterior prediction checks whether the updated model reproduces phenomena that matter. These operations connect probability curves to the actual research or decision problem rather than treating the curves as an end product.

## What can a small shop learn from other shops?

Four shops observe 5, 20, 50 and 200 customers, with 4, 10, 30 and 110 purchases. The first has the highest observed rate but only five records. Pooling all shops into one purchase rate erases real differences, while estimating each completely separately makes small-sample estimates unstable. A hierarchical model connects the two extremes. Every shop has its own success rate, these rates share a population distribution, and the population mean and concentration are themselves updated from observations. Shared information becomes part of an explicit probabilistic structure.

$$
\mu\sim\operatorname{Uniform}(0,1),\quad\kappa\sim\operatorname{Exponential}(\text{rate}=0.1),\quad\theta_g\mid\mu,\kappa\sim\operatorname{Beta}(\kappa\mu,\kappa(1-\mu)),\quad Y_g\mid\theta_g\sim\operatorname{Binomial}(n_g,\theta_g)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d2455474f43efb98735a21bd.svg) | Group index, trial count, success count and success probability; group observations are independent conditional on their rates. |
| ![Formula](https://ml-biomat.com/static/agent-math/e1b9bd30207e04217b3c892c.svg) | Population mean success rate and positive concentration, unitless; larger concentration draws group probabilities closer to the mean. |
| ![Formula](https://ml-biomat.com/static/agent-math/698aabd843434d4c0d576e20.svg) | Uniform and exponential distributions and rate parameter; rate 0.1 implies mean ten. |

With mu=0.6 and kappa=10 fixed, four successes in five trials give posterior mean (4+6)/(5+10)=2/3; 110 in 200 give 116/210≈0.5524. The actual hierarchical experiment additionally integrates over their posterior, so its values differ from this conditional calculation.

Conditional on the population mean and concentration, a shop's posterior mean is a weighted average of its observed fraction and the population mean. Population information carries more weight for a small sample; the shop's own observations carry more weight for a large one. This is partial pooling. It does not mechanically pull every estimate toward one half: the common population and individual shop records inform each other. Shops serving distinctly different populations may need region or channel predictors, or separate population distributions, so the sharing assumptions reflect the actual organization of the problem.

![Left: observed fractions, separate Beta(1,1) posterior means and integrated hierarchical means for four shops; dotted line is posterior population-mean average. Right: joint hyperparameter grid mass, with logarithmic concentration axis.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ba9eac91acde7cc8bc12de29.svg?v=ba9eac91acde)

Figure 2Left: observed fractions, separate Beta(1,1) posterior means and integrated hierarchical means for four shops; dotted line is posterior population-mean average. Right: joint hyperparameter grid mass, with logarithmic concentration axis.

The code integrates over a two-dimensional grid of population mean and concentration, retaining hyperparameter uncertainty before computing shop posterior means. Results are approximately 0.635, 0.531, 0.593 and 0.552. The first shop moves substantially from its observed 0.8 toward shared information; the fourth changes little because it has 200 records. The posterior population-mean average is about 0.572. The right panel displays probability mass on the hyperparameter grid. Concentration uses a logarithmic grid, and the corresponding integration weights are included; treating those grid points as equally spaced in concentration would change the declared prior.

The population mean has a uniform prior between zero and one, and concentration has an exponential prior with mean ten. Numerical integration uses explicit finite bounds. Small mass near the grid edges provides a diagnostic for subsequent refinement and expansion. Empirical Bayes offers another strategy: estimate a hyperparameter value first and condition on it. This can simplify computation, while leaving that hyperparameter's uncertainty outside subsequent shop estimates. The present example deliberately integrates over it, allowing readers to distinguish the hierarchical model structure from the approximation used to compute its consequences.

## Evidence can travel through states we cannot see

A device's internal alarm-prone condition may be hidden while its alarm output is observable. A hidden Markov model, or HMM, represents the internal condition with a hidden state, observations with emission probabilities, and persistence or change with transition probabilities. A graphical model draws these relationships as nodes and arrows: hidden states connect through time, and each state connects to its observation. The arrows first specify a probability factorization. Conditional on the current state, its observation needs no direct dependence on other hidden states. This conditional-independence structure makes sequential computation possible.

![Hidden-state chain alongside a hierarchical group model](https://ml-biomat.com/static/tutorials/machine-learning/figures/56b4fda59ec5799a52020473.svg?v=56b4fda59ec5)

Figure 3Original probability-structure diagrams: HMMs share information through neighboring states, hierarchies through population parameters. Arrows specify conditional distributions and shaded nodes are observed; each group count also conditions on its known trial count.

Conditional independence does not mean that observed signals have no relationship. A persistent hidden operating condition makes neighboring alarms correlated, while knowing the current state allows its emission mechanism to be evaluated separately. The shop hierarchy has a related distinction: conditional on population parameters, shop rates are generated independently under the model; integrating out those unknown population parameters lets observations inform one another through the shared population. When reading the diagram, cover a hidden node and ask what common information remains, then reveal it. Connections specify a probability factorization. Interpreting them as effects of physical interventions requires an additional causal model, which is a different modeling commitment.

$$
p(z_{1:T},y_{1:T})=\pi_{z_1}b_{z_1}(y_1)\prod_{t=2}^TA_{z_{t-1},z_t}b_{z_t}(y_t),\quad\alpha_t(j)=b_j(y_t)\sum_i\alpha_{t-1}(i)A_{ij}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b4ca40e89600686579ed8a15.svg) | Sequence length, time, hidden state, observation and previous/current state indices; states and alarms are binary here. |
| ![Formula](https://ml-biomat.com/static/agent-math/ba3ba85084bcd9e08182feb4.svg) | Initial state probability, transition probability from i to j and emission probability for y in state j; each appropriate discrete distribution normalizes. |
| ![Formula](https://ml-biomat.com/static/agent-math/41f2ee49482a5b9573a1dae6.svg) | Joint probability of observations through t and state j, and sequential product; all unitless. This alpha is unnormalized; code rescales each step to avoid underflow. |

Initial probabilities (0.6,0.4) and no-alarm emissions (0.85,0.2) give first joint weights (0.51,0.08). Their sum 0.59 is the first observation probability; normalization gives state-one probability 0.135593. Subsequent sums reuse path prefixes instead of enumerating them repeatedly.

The example has states zero and one. State one produces an alarm with probability 0.8, while state zero produces it with probability 0.15. Persistence probabilities are 0.9 for state zero and 0.8 for state one. Initial probability for state one is 0.4. The first observation has no alarm, giving state contributions 0.6 times 0.85 and 0.4 times 0.2. Normalizing gives state-one probability about 0.1356. Each new observation repeats a pattern: predict through the transition matrix, multiply by state-dependent observation probabilities, then normalize.

This forward message uses a short vector to summarize all earlier observations relevant to the current state. Filtering uses observations available so far and supports real-time inference. Smoothing also sends later evidence backward and supports retrospective reconstruction. The eight alarm observations are 0,0,1,1,1,0,1,0. At the third time, filtered state-one probability is about 0.460; after later consecutive alarms are incorporated, the smoothed probability becomes about 0.797. The difference follows from available information. A real-time system must use the filtering information set at that moment rather than future observations.

The most probable complete state path also differs from selecting the highest-posterior state at each time independently. The former maximizes a path's joint probability, usually with Viterbi dynamic programming; the latter maximizes separate marginal probabilities and can produce another path. For eight times and two states, the code enumerates all 256 paths as an independent check of the forward observation likelihood. Their difference is about 4.3×10⁻¹⁹. Longer sequences benefit from reusing intermediate messages instead of enumerating every path, demonstrating the computational value of the graph's structure.

## EM alternates soft assignments and parameter updates

The preceding HMM uses given transition and emission probabilities. If those parameters are also unknown and records have no observed internal states, inference must address both hidden variables and model parameters. Gaussian-mixture membership creates a related problem. Assigning a fixed guessed label to every observation and then treating it as truth locks uncertain membership too early. Expectation maximization instead computes soft assignments under the current model and uses their probabilities as weights in parameter updates. Several possible assignments can therefore influence the next fitted model.

$$
q_i(k)=p(z_i=k\mid x_i,\vartheta^{\rm old}),\quad N_k=\sum_iq_i(k),\quad\mu_k^{\rm new}=\frac{\sum_iq_i(k)x_i}{N_k}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c3662d65405121157c505c41.svg) | Observation index, component index, observed value and hidden membership. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0fc2bc6be6dda63561ac5f5.svg) | Responsibility under current parameters, old parameter collection and effective component count; q is unitless and sums to one over components. |
| ![Formula](https://ml-biomat.com/static/agent-math/64800a1b919238f0694d679d.svg) | Updated component mean, in observation units, requiring positive effective count. |

For observations zero and two with component responsibilities 0.75 and 0.25, effective count is one and weighted mean is 0.5. The E step updates soft membership and the M step parameters; covariance and proportions use the same weights.

The E step computes the conditional hidden-variable distribution. The M step maximizes expected complete-data log likelihood under that distribution. For a Gaussian mixture, updates become weighted means, weighted variances and mixture proportions. For an HMM, forward-backward messages estimate state probabilities and adjacent-state-pair probabilities; expected counts then update transition and emission distributions. This classical HMM training procedure is commonly called Baum–Welch. The two model families share an optimization principle, while dependence among their hidden variables changes the computation required in the E step.

![Left and middle: Gaussian-mixture EM on 300 observations and per-round log likelihood. Right: HMM filtering and smoothing for eight observations, with alarm values below each time index.](https://ml-biomat.com/static/tutorials/machine-learning/figures/65debd1714203a0c25c164e6.svg?v=65debd171420)

Figure 4Left and middle: Gaussian-mixture EM on 300 observations and per-round log likelihood. Right: HMM filtering and smoothing for eight observations, with alarm values below each time index.

The actual code runs twenty Gaussian-mixture EM updates on 300 generated one-dimensional observations. Training log likelihood rises from approximately −685.0 to −550.7, with component means about −2.054 and 1.805. Its curve checks objective improvement and shows increasingly small changes late in optimization. EM supplies a parameter optimum for one initialization, rather than retaining complete parameter uncertainty; multiple local optima motivate comparing initializations. Bayesian inference, EM and HMM describe different parts of the analysis: an inference framework, an optimization method and a probabilistic model structure, respectively.

## Many accepted moves can still explore very little

High-dimensional posteriors often resist direct integration. The 1953 work of Metropolis, the Rosenbluths and the Tellers applied probability-weighted state visits to statistical-physics computation, helping establish Markov chain Monte Carlo methods. A random walk proposes a state and accepts it or keeps the previous state according to relative target density. With appropriate execution and diagnostics, recorded visits approximate posterior means, intervals and predictions. Successive records remain correlated, so a stored sample count alone does not describe the amount of independent information available for those estimates.

$$
a(\theta,\theta^{\prime})=\min\!\left(1,\frac{\widetilde p(\theta^{\prime})q(\theta\mid\theta^{\prime})}{\widetilde p(\theta)q(\theta^{\prime}\mid\theta)}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/12d2ba147169a3af41c53b5f.svg) | Current and proposed parameter states; this example proposes in dimensionless logit coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/96d59c36164b7f8b52db2b2b.svg) | Unnormalized target density, conditional proposal density and acceptance probability; shared normalization constants cancel, leaving a unitless acceptance probability. |

Symmetric proposals cancel the q terms. A candidate/current density ratio 0.4 gives acceptance probability 0.4; ratios above one are accepted. Transforming theta to u=log(theta/(1−theta)) contributes Jacobian theta(1−theta), making the logit-space Beta(9,5) density proportional to theta⁹(1−theta)⁵.

The example intentionally targets Beta(9,5), whose analytic answer is available for checking. Random walks occur in logit coordinates, and the target includes the transformation Jacobian so changing coordinates preserves the intended probability distribution. Four chains start at dispersed positions, discard the first 500 iterations and retain 4,000 each. At proposal step 0.7, their combined posterior mean is about 0.6420, close to the analytic 0.6429. Acceptance rates are approximately 64–65%. Autocorrelation remains, so each chain's effective sample size is smaller than its 4,000 retained records.

![Each row contains four chains with 4,000 retained draws each; proposal steps are 0.7 above and 0.03 below. Traces display every fifth draw while ESS uses every retained draw. Middle: lag autocorrelation. Right: histograms with the analytic Beta posterior.](https://ml-biomat.com/static/tutorials/machine-learning/figures/db71a61f6e7f64f4a2feb54f.svg?v=db71a61f6e7f)

Figure 5Each row contains four chains with 4,000 retained draws each; proposal steps are 0.7 above and 0.03 below. Traces display every fifth draw while ESS uses every retained draw. Middle: lag autocorrelation. Right: histograms with the analytic Beta posterior.

Reducing proposal step to 0.03 raises acceptance to roughly 97–99%, yet the traces move slowly. Minimum single-chain effective sample size falls from about 573 to 4.6, while classical split R-hat rises from about 1.001 to 1.224. A high acceptance rate means proposed changes are easy to accept; tiny changes can take a long time to cross the posterior region. Traces, autocorrelations and histograms display the effect together. A plausible-looking histogram cannot replace checks of agreement between chains and the rate at which they explore the distribution.

$$
N_{\rm eff}\approx\frac{N}{1+2\sum_{\ell\ge1}\rho_\ell},\qquad\widehat R=\sqrt{\frac{\frac{n-1}{n}W+\frac Bn}{W}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/baccfdf2f10c579a84f14ad8.svg) | Retained single-chain draw count, effective count for an estimand, lag autocorrelation and lag, all unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c061b232f898f9c6c2805a73.svg) | Draw count per split chain, mean within-chain sample variance, n times sample variance of chain means, and classical split R-hat; W and B have squared-parameter units and R-hat is unitless. |

For one thousand draws with autocorrelations given by successive powers of 0.8, their sum is four and ESS is about 1000/9=111. Monte Carlo error for the mean follows effective information rather than treating all correlated draws as independent. Code splits each chain in half before comparing W and B; modern rank diagnostics are discussed separately.

The script transparently implements classical split R-hat and a single-chain ESS estimate using positive autocorrelation pairs. Complex applications generally use rank-normalized and folded R-hat, bulk and tail ESS, and sampler-specific diagnostics such as Hamiltonian Monte Carlo divergences. R-hat near one indicates that this comparison has found little between-chain discrepancy; chains may still jointly miss another mode. Before extending a problematic run, investigate parameterization, scales and posterior geometry. Routine thinning often discards information useful for averaging rather than fixing the underlying exploration problem.

## Approximate a posterior with an easier distribution

Variational inference turns integration into optimization. Choose a tractable family of distributions, then adjust its parameters to approach the target posterior. A common mean-field approximation factorizes latent variables into independent components, simplifying computation and storage. Its cost is concrete: when a posterior stretches along a tilted direction, independent factors can approximate it only with an axis-aligned shape. Even an optimizer that solves the specified objective accurately cannot create a correlation structure absent from the chosen family. Model, approximation family and numerical optimizer therefore deserve separate attention.

$$
\operatorname{ELBO}(q)=\mathbb E_q[\log p(D,\theta)-\log q(\theta)],\quad\log p(D)=\operatorname{ELBO}(q)+D_{\rm KL}(q\|p(\theta\mid D))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3afa9187688d4f19a6e3b0a9.svg) | Observations, latent variables/parameters, approximating distribution and model probability or density. |
| ![Formula](https://ml-biomat.com/static/agent-math/a33fdd5fe38628007d233099.svg) | Expectation under q, natural logarithm, KL divergence and evidence lower bound; log ratios and KL are in nats under a consistent base measure. |

Evidence is fixed with respect to q and KL is nonnegative, so maximizing ELBO minimizes this KL. For unit marginal variances and correlation 0.9, target precision diagonals are 1/(1−0.9²), giving optimal independent reverse-KL variances 0.19 while target marginals remain one. Actual optimized KL is about 0.83037 nats.

The code targets a two-dimensional Gaussian with mean (1,−1), marginal variances one and correlation 0.9, then actually optimizes an independent Gaussian under reverse KL divergence. It recovers the mean near (1,−1), but both approximating variances become about 0.19. Taking reciprocals of the target precision matrix's diagonal entries independently verifies that result. The tilted target contours and tighter axis-aligned approximation show how the approximation avoids low-density target regions. Marginal curves reveal the narrower uncertainty directly. This behavior belongs to the stated target and approximation family rather than every variational method.

![Left: correlated Gaussian target contours and an independent reverse-KL Gaussian approximation. Right: first-coordinate marginal densities. Target variance one versus approximate variance 0.19 displays the correlation structure lost by this family.](https://ml-biomat.com/static/tutorials/machine-learning/figures/79302bd3f0075ff1455958f5.svg?v=79302bd3f007)

Figure 6Left: correlated Gaussian target contours and an independent reverse-KL Gaussian approximation. Right: first-coordinate marginal densities. Target variance one versus approximate variance 0.19 displays the correlation structure lost by this family.

The evidence lower bound, ELBO, relates model fit to entropy of the approximating distribution. Increasing it reduces the corresponding KL divergence for a fixed model. A stable optimization curve says the numerical objective is no longer improving substantially; approximation quality still benefits from comparison with analytic answers or small MCMC runs, richer distribution families, and checks of relevant posterior predictions. Variational inference offers efficient approximations for larger models, while MCMC can explore more complicated shapes through samples. Both can contribute to one workflow, with their roles determined by the quantities the analysis needs.

## A Gaussian process places uncertainty over a function

In regression, the unknown object can be an entire function rather than one success probability. A Gaussian process specifies that function values at any finite collection of inputs follow a multivariate Gaussian distribution. Its mean function describes a central trend, while its kernel describes how values at different positions co-vary. The RBF kernel strongly relates nearby inputs, and its length scale controls the distance over which that relation persists. An observation therefore informs nearby positions through covariance. Far from the observations, predictions gradually return toward the behavior specified by the prior.

$$
k(x,x^{\prime})=\sigma_f^2\exp\!\left[-\frac{(x-x^{\prime})^2}{2\ell^2}\right],\quad m_*=k_*^\mathsf T(K+\sigma_n^2I)^{-1}y,\quad s_*^2=k_{**}-k_*^\mathsf T(K+\sigma_n^2I)^{-1}k_*
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/91cb5b808cf3e88540c9e610.svg) | One-dimensional input locations, positive length scale and prior function variance; length shares input units and variance has squared-response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/78bbd28daaaf026101b6a87f.svg) | Observation count, n-by-n training kernel covariance, n-by-n identity and n-vector of responses, with zero prior mean. |
| ![Formula](https://ml-biomat.com/static/agent-math/24a4d93ed15072671e37c951.svg) | n-vector of training/test function covariances, test prior variance and independent homoscedastic Gaussian observation-noise variance. |
| ![Formula](https://ml-biomat.com/static/agent-math/ac644bcc73563be6034d1268.svg) | Conditional latent-function mean and variance, transpose and matrix inverse; response and squared-response units respectively. The library uses stable linear algebra. |

For one observation y=1 at the test position, K=k*=k**=1 and noise variance 0.25 give mean 1/1.25=0.8 and latent variance 1−1/1.25=0.2. Future observation variance adds independent noise to give 0.45. The multi-observation formula conditions a joint Gaussian distribution.

Six observations here come from a sine function plus Gaussian noise with standard deviation 0.15. Length scales 0.4, 1.2 and 3.0 are compared with kernel amplitude fixed at one and without optimizing hyperparameters on the six points. A short length scale permits rapid changes and can leave substantial uncertainty between observations; a longer scale favors smoother changes and transmits information farther. At length scale 1.2, latent-function standard deviation is about 0.113 at input zero and 0.970 at input four. The specified kernel and observation positions jointly produce these values.

![The same six noisy observations with RBF length scales 0.4, 1.2 and 3. Blue bands are latent-function and pale orange bands future-observation pointwise 95% intervals; the dotted curve is generating sin(x). Kernel amplitude one, noise standard deviation 0.15, fixed hyperparameters.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4b835400aa0cd7631f7be4ba.svg?v=4b835400aa0c)

Figure 7The same six noisy observations with RBF length scales 0.4, 1.2 and 3. Blue bands are latent-function and pale orange bands future-observation pointwise 95% intervals; the dotted curve is generating sin(x). Kernel amplitude one, noise standard deviation 0.15, fixed hyperparameters.

Blue bands show pointwise 95% posterior intervals for the latent function. Pale orange bands add future measurement-noise variance and are wider. A hand-computable example makes the distinction clear. With prior function variance one, observation value one at the same input, and noise variance 0.25, posterior mean is 0.8 and latent variance 0.2. Future-observation variance adds another 0.25 to give 0.45. Separate what has been learned about the function from how much another measurement will fluctuate. Pointwise 95% coverage also differs from a 95% probability that an entire function lies inside a simultaneous band.

![Public GP example: observations, prediction and pointwise posterior interval](https://ml-biomat.com/static/tutorials/machine-learning/figures/f259c98ddd7e8398023b3604.png?v=f259c98ddd7e)

Figure 8Original noisy Gaussian-process figure by the scikit-learn developers, BSD-3-Clause, unmodified. Its function x sin(x) differs from this chapter experiment; the original code gives pointwise latent-function intervals conditional on the fitted model.

The official example figure uses another function and noise setting to compare behavior near and away from observations. Its legend says confidence interval. Given that example's RBF-based kernel, training-noise alpha and standard deviation returned by predict, the band is interpreted here as a pointwise latent-function posterior interval conditional on the fitted model. Code determines the meaning of the shaded region. Including WhiteKernel in predictive covariance or integrating over kernel hyperparameters changes the interpretation, so color and a printed percentage alone do not identify which uncertainty is displayed.

### Complete experiment: analytic posterior, hierarchy, HMM, EM, sampling, VI and GP

Requires NumPy, SciPy, Matplotlib and scikit-learn. Run python main.py --output results --language en. No dataset download is needed; outputs are six original figure groups, arrays and summary.json. Analytic probabilities, full-path enumeration and a one-observation GP provide independent numerical checks.

```
"""Bayesian updates, hierarchy, exact messages, sampling, variational inference and GP."""
from pathlib import Path
import argparse,json,itertools
import numpy as np
from scipy.stats import beta,betabinom,binom,norm,multivariate_normal
from scipy.special import betaln,logsumexp,expit
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def hmm(observations,A,B,pi):
 n=len(observations);forward=np.zeros((n,2));scale=np.zeros(n);forward[0]=pi*B[:,observations[0]];scale[0]=forward[0].sum();forward[0]/=scale[0]
 for t in range(1,n):forward[t]=(forward[t-1]@A)*B[:,observations[t]];scale[t]=forward[t].sum();forward[t]/=scale[t]
 backward=np.ones((n,2))
 for t in range(n-2,-1,-1):backward[t]=A@(B[:,observations[t+1]]*backward[t+1])/scale[t+1]
 smooth=forward*backward;smooth/=smooth.sum(1,keepdims=True)
 return forward,smooth,float(np.prod(scale))

def ess_one(x):
 x=x-x.mean();n=len(x);f=np.fft.rfft(x,n=2*n);ac=np.fft.irfft(f*f.conj())[:n];ac/=ac[0];positive=0.;last=np.inf
 for lag in range(1,n-1,2):
  pair=ac[lag]+ac[lag+1]
  if pair<=0:break
  pair=min(pair,last);positive+=pair;last=pair
 return float(n/(1+2*positive)),ac

def sample_beta(step,seed,draws=4000,burn=500):
 rng=np.random.default_rng(seed);chains=[];rates=[]
 def logtarget(u):return 9*(-np.logaddexp(0,-u))+5*(-np.logaddexp(0,u)) # Beta(9,5) plus logit Jacobian
 for start in [-2,-.7,.7,2]:
  u=start;lp=logtarget(u);vals=[];accepted=0
  for t in range(draws+burn):
   v=u+rng.normal(scale=step);lv=logtarget(v)
   if np.log(rng.random())<lv-lp:u=v;lp=lv;accepted+=1
   if t>=burn:vals.append(expit(u))
  chains.append(vals);rates.append(accepted/(draws+burn))
 chains=np.array(chains);split=np.concatenate([chains[:,:draws//2],chains[:,draws//2:]]);n=split.shape[1];W=np.var(split,axis=1,ddof=1).mean();B=n*np.var(split.mean(1),ddof=1);rhat=np.sqrt(((n-1)/n*W+B/n)/W);esses=[ess_one(c)[0] for c in chains]
 return chains,{'step':step,'mean':float(chains.mean()),'acceptance':rates,'classical_split_rhat':float(rhat),'per_chain_ess':esses,'minimum_chain_ess':min(esses)}

def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';T=lambda z,e:z if zh else e;rng=np.random.default_rng(7)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
 def save(fig,n):fig.savefig(out/f'{n}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 a,b=9,5;grid=np.linspace(.001,.999,1000);k=np.arange(11);pred=betabinom.pmf(k,10,a,b);plug=binom.pmf(k,10,a/(a+b));ci=beta.ppf([.025,.975],a,b)
 fig,axs=plt.subplots(1,3,figsize=(14,4.3),layout='constrained');axs[0].plot(grid,beta.pdf(grid,2,2),label=T('先验 Beta(2,2)','Prior Beta(2,2)'),color='#83949e');axs[0].plot(grid,beta.pdf(grid,a,b),label=T('后验 Beta(9,5)','Posterior Beta(9,5)'),color='#237b94');axs[0].fill_between(grid,0,beta.pdf(grid,a,b),where=(grid>=ci[0])&(grid<=ci[1]),alpha=.17,color='#237b94');axs[0].set(xlabel=T('成功概率','Success probability'),ylabel=T('概率密度','Density'));axs[0].legend(fontsize=9)
 axs[1].bar(k-.18,pred,width=.36,color='#237b94',label=T('后验预测','Posterior predictive'));axs[1].bar(k+.18,plug,width=.36,color='#d87430',label=T('固定均值概率','Fixed mean probability'));axs[1].set(xlabel=T('未来10次的成功数','Successes in ten future trials'),ylabel=T('概率','Probability'));axs[1].legend(fontsize=9)
 for n in [10,40,200]:axs[2].plot(grid,beta.pdf(grid,2+.7*n,2+.3*n),label=f'n={n}')
 axs[2].set(xlabel=T('成功概率','Success probability'),ylabel=T('后验密度','Posterior density'),title=T('成功比例均为70%','Same observed success fraction: 70%'));axs[2].legend();save(fig,'update_predictive')
 # Integrate uncertain population mean and concentration on a quadrature grid.
 ns=np.array([5,20,50,200]);success=np.array([4,10,30,110]);mu=np.linspace(.002,.998,240);kappa=np.geomspace(.05,150,220);M,K=np.meshgrid(mu,kappa);aa=M*K;bb=(1-M)*K;logw=-K/10+np.log(K) # Exp(mean=10) prior and log-kappa Jacobian; mu uniform
 for n,s in zip(ns,success):logw+=betaln(s+aa,n-s+bb)-betaln(aa,bb)
 weights=np.exp(logw-logsumexp(logw));hiermean=np.array([np.sum(weights*(s+aa)/(n+K)) for n,s in zip(ns,success)]);independent=(success+1)/(ns+2);population_mu=float(np.sum(weights*M));edge_mass=float(weights[:3].sum()+weights[-3:].sum()+weights[:,:3].sum()+weights[:,-3:].sum())
 fig,axs=plt.subplots(1,2,figsize=(12,4.7),layout='constrained');xs=np.arange(4);axs[0].plot(xs,success/ns,'o--',label=T('观测比例','Observed fraction'),color='#d87430');axs[0].plot(xs,independent,'s--',label=T('各自Beta(1,1)','Separate Beta(1,1)'),color='#83949e');axs[0].plot(xs,hiermean,'o-',label=T('层次后验均值','Hierarchical posterior mean'),color='#237b94');axs[0].axhline(population_mu,ls=':',color='#237b94');axs[0].set(xticks=xs,xticklabels=[f'{i+1} (n={n})' for i,n in enumerate(ns)],xlabel=T('群组与样本量','Group and sample count'),ylabel=T('成功概率估计','Estimated success probability'),ylim=(.35,.9));axs[0].legend(fontsize=9)
 im=axs[1].pcolormesh(mu,kappa,weights,shading='auto',cmap='Blues',rasterized=True);axs[1].set(yscale='log',xlabel=T('总体均值','Population mean'),ylabel=T('集中程度 kappa','Concentration kappa'),title=T('超参数联合后验网格质量','Hyperparameter joint posterior grid mass'));fig.colorbar(im,ax=axs[1],label=T('网格概率质量','Grid probability mass'));save(fig,'hierarchy')
 # Transparent EM for a one-dimensional Gaussian mixture.
 latent=rng.random(300)>.4;data=rng.normal(np.where(latent,2.,-2.),np.where(latent,1.,.7));means=np.array([-1.,1.]);variances=np.ones(2);mix=np.ones(2)/2;history=[]
 for iteration in range(21):
  logjoint=np.array([np.log(mix[j])+norm.logpdf(data,means[j],np.sqrt(variances[j])) for j in range(2)]).T;den=logsumexp(logjoint,axis=1);history.append(float(den.sum()));resp=np.exp(logjoint-den[:,None]);mass=resp.sum(0)
  if iteration<20:mix=mass/len(data);means=(resp*data[:,None]).sum(0)/mass;variances=np.maximum((resp*(data[:,None]-means)**2).sum(0)/mass,1e-6)
 obs=np.array([0,0,1,1,1,0,1,0]);A=np.array([[.9,.1],[.2,.8]]);B=np.array([[.85,.15],[.2,.8]]);pi=np.array([.6,.4]);filtered,smoothed,likelihood=hmm(obs,A,B,pi);brute=0.;pathbest=None;maxprob=-1
 for path in itertools.product(range(2),repeat=len(obs)):
  prob=pi[path[0]]*B[path[0],obs[0]]
  for t in range(1,len(obs)):prob*=A[path[t-1],path[t]]*B[path[t],obs[t]]
  brute+=prob
  if prob>maxprob:maxprob=prob;pathbest=path
 fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained');u=np.linspace(-5,5,500);axs[0].hist(data,bins=30,density=True,color='#d8e3e8');axs[0].plot(u,sum(mix[j]*norm.pdf(u,means[j],np.sqrt(variances[j])) for j in range(2)),color='#237b94');axs[0].set(xlabel=T('观测值','Observation'),ylabel=T('密度','Density'),title=T('EM拟合混合密度','EM mixture fit'));axs[1].plot(range(21),history,'o-',ms=3,color='#237b94');axs[1].set(xlabel=T('EM更新次数','EM updates'),ylabel=T('训练对数似然','Training log likelihood'));axs[2].plot(range(1,9),filtered[:,1],'o-',label=T('过滤：截至当前','Filtering: observations so far'));axs[2].plot(range(1,9),smoothed[:,1],'s--',label=T('平滑：完整序列','Smoothing: full sequence'));axs[2].set(xticks=range(1,9),xticklabels=[f'{i+1}\n{o}' for i,o in enumerate(obs)],xlabel=T('时刻 / 报警观测','Time / observed alarm'),ylabel=T('状态1的后验概率','Posterior probability of state 1'),ylim=(0,1));axs[2].legend(fontsize=8);save(fig,'latent_messages')
 good,gd=sample_beta(.7,7);slow,sd=sample_beta(.03,17);fig,axs=plt.subplots(2,3,figsize=(14,8),layout='constrained')
 for row,(chains,dg) in enumerate([(good,gd),(slow,sd)]):
  for i,c in enumerate(chains):axs[row,0].plot(c[::5],lw=.6,alpha=.7,label=str(i+1))
  axs[row,0].set(xlabel=T('每5步显示一次','Displayed every fifth draw'),ylabel=T('成功概率','Success probability'),title=f'step={dg["step"]}, split R-hat={dg["classical_split_rhat"]:.3f}')
  for c in chains:axs[row,1].plot(ess_one(c)[1][:100],alpha=.8)
  axs[row,1].set(xlabel=T('滞后步数','Lag'),ylabel=T('自相关','Autocorrelation'),title=f'min ESS={dg["minimum_chain_ess"]:.0f}')
  axs[row,2].hist(chains.ravel(),bins=45,density=True,alpha=.6,color='#237b94');axs[row,2].plot(grid,beta.pdf(grid,a,b),color='#d87430');axs[row,2].set(xlabel=T('成功概率','Success probability'),ylabel=T('密度','Density'),title=T('采样与解析后验','Samples and analytic posterior'))
 save(fig,'sampling')
 # Actual optimization of reverse KL for an independent Gaussian approximation.
 target_mean=np.array([1.,-1.]);cov=np.array([[1,.9],[.9,1.]]);precision=np.linalg.inv(cov)
 def kl(p):
  delta=p[:2]-target_mean;v=np.exp(2*p[2:]);return .5*(np.dot(np.diag(precision),v)+delta@precision@delta-2+np.linalg.slogdet(cov)[1]-np.log(v).sum())
 fit=minimize(kl,[0,0,0,0],method='BFGS');qm=fit.x[:2];qv=np.exp(2*fit.x[2:]);gx,gy=np.meshgrid(np.linspace(-2,4,160),np.linspace(-4,2,160));pts=np.dstack([gx,gy]);fig,axs=plt.subplots(1,2,figsize=(11,4.6),layout='constrained');axs[0].contour(gx,gy,multivariate_normal.pdf(pts,target_mean,cov),levels=[.02,.08,.2],colors=['#d87430']);axs[0].contour(gx,gy,multivariate_normal.pdf(pts,qm,np.diag(qv)),levels=[.02,.08,.2],colors=['#237b94'],linestyles='--');axs[0].set(xlabel='theta 1',ylabel='theta 2',title=T('橙：目标；蓝虚线：独立近似','Orange: target; blue dashed: independent approximation'));axs[0].set_aspect('equal');u=np.linspace(-2,4,500);axs[1].plot(u,norm.pdf(u,1,1),label=T('目标边缘','Target marginal'),color='#d87430');axs[1].plot(u,norm.pdf(u,qm[0],np.sqrt(qv[0])),label=T('变分边缘','Variational marginal'),color='#237b94');axs[1].set(xlabel='theta 1',ylabel=T('概率密度','Density'));axs[1].legend();save(fig,'variational')
 xx=np.array([-2,-1.6,-.5,.2,.7,1.8])[:,None];yy=np.sin(xx[:,0])+rng.normal(0,.15,len(xx));query=np.linspace(-4,4,400)[:,None];gps={};fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained')
 for ax,length in zip(axs,[.4,1.2,3.]):
  gp=GaussianProcessRegressor(kernel=RBF(length,length_scale_bounds='fixed'),alpha=.15**2,optimizer=None).fit(xx,yy);mean,std=gp.predict(query,return_std=True);obs_std=np.sqrt(std**2+.15**2);ax.fill_between(query[:,0],mean-1.96*obs_std,mean+1.96*obs_std,color='#d87430',alpha=.15,label=T('未来观测95%区间','Future-observation 95% interval'));ax.fill_between(query[:,0],mean-1.96*std,mean+1.96*std,color='#237b94',alpha=.25,label=T('潜在函数95%区间','Latent-function 95% interval'));ax.plot(query,mean,color='#237b94');ax.scatter(xx,yy,c='#263744',s=24);ax.plot(query,np.sin(query),':',color='#83949e');ax.set(title=f'RBF length={length}',xlabel=T('输入x（无量纲）','Input x (unitless)'),ylabel=T('响应（无量纲）','Response (unitless)'),ylim=(-2.8,2.8));gps[str(length)]={'latent_std_at_zero':float(gp.predict([[0]],return_std=True)[1][0]),'latent_std_at_four':float(gp.predict([[4]],return_std=True)[1][0])}
 axs[1].legend(fontsize=8,loc='upper center');save(fig,'gaussian_process')
 one=GaussianProcessRegressor(kernel=RBF(1,length_scale_bounds='fixed'),alpha=.25,optimizer=None).fit([[0]],[1]);one_m,one_s=one.predict([[0]],return_std=True)
 summary={'prior_alpha':2,'prior_beta':2,'successes':7,'failures':3,'posterior_alpha':a,'posterior_beta':b,'posterior_mean':a/(a+b),'posterior_map':(a-1)/(a+b-2),'posterior_ci95':ci.tolist(),'predictive_mean':float(betabinom.mean(10,a,b)),'predictive_variance':float(betabinom.var(10,a,b)),'predictive_mass_sum':float(pred.sum()),'hierarchical_group_means':hiermean.tolist(),'hierarchical_population_mean':population_mu,'hyper_grid_edge_mass':edge_mass,'em_final_means':means.tolist(),'em_log_likelihood':history,'em_min_improvement':float(np.diff(history).min()),'hmm_likelihood':likelihood,'hmm_brute_likelihood':brute,'hmm_likelihood_error':abs(likelihood-brute),'hmm_filtered':filtered[:,1].tolist(),'hmm_smoothed':smoothed[:,1].tolist(),'hmm_most_probable_path':list(pathbest),'mcmc_good':gd,'mcmc_slow':sd,'variational_mean':qm.tolist(),'variational_variances':qv.tolist(),'variational_kl':float(fit.fun),'variational_optimizer_success':bool(fit.success),'gp':gps,'gp_one_observation_mean':float(one_m[0]),'gp_one_observation_latent_variance':float(one_s[0]**2)}
 np.savez_compressed(out/'experiment_data.npz',beta_grid=grid,predictive=pred,hierarchy_mu=mu,hierarchy_kappa=kappa,hierarchy_weights=weights,em_data=data,hmm_observations=obs,hmm_transitions=A,hmm_emissions=B,good_chains=good,slow_chains=slow,gp_x=xx,gp_y=yy);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

The experiments form a checkable progression: obtain an analytic Beta update, share information through hierarchical integration, handle temporal dependence with HMM messages, estimate latent-variable parameters through EM, examine sampling and variational approximations, then propagate uncertainty to function predictions. A new problem can follow the same logic. Describe observation generation, specify unknown quantities and shared relationships, choose a computational method, and bring posterior predictions back to recognizable objects for assessment. Each step then has a clear location for uncertainty and a concrete calculation that determines how it moves forward.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Bayes (1763), An Essay towards Solving a Problem in the Doctrine of Chances](https://www.jstor.org/stable/105741)

   Historical inference about unknown chances from observations.

   Historical reference
2. [PyMC — General API quickstart](https://www.pymc.io/projects/examples/en/latest/introductory/api_quickstart.html)

   Modern workflow for specification, priors, sampling and prediction.

   MIT example project; reference
3. [Gelman et al., Bayesian Workflow](https://arxiv.org/abs/2011.01808)

   Model and computational checks within inference.
4. [Stan — Latent Discrete Parameters](https://mc-stan.org/docs/stan-users-guide/latent-discrete.html)

   HMMs and forward marginalization.
5. [hmmlearn — Tutorial](https://hmmlearn.readthedocs.io/en/latest/tutorial.html)

   Hidden states, emissions, decoding and EM.

   BSD-3-Clause project
6. [Metropolis et al. (1953), Equation of State Calculations by Fast Computing Machines](https://www.osti.gov/biblio/4390578)

   Historical context for probability-weighted state visits.

   Primary bibliographic reference
7. [Stan — Posterior Analysis](https://mc-stan.org/docs/reference-manual/analysis.html)

   Split R-hat, rank normalization, ESS and Monte Carlo error.
8. [Blei, Kucukelbir & McAuliffe (2017), Variational Inference: A Review for Statisticians](https://www.cs.columbia.edu/~blei/papers/BleiKucukelbirMcAuliffe2017.pdf)

   ELBO, mean field and approximation families.
9. [scikit-learn — Gaussian Processes regression: basic introductory example](https://scikit-learn.org/stable/auto_examples/gaussian_process/plot_gpr_noisy_targets.html)

   Original public GP figure, kernels and training noise.

   BSD-3-Clause
