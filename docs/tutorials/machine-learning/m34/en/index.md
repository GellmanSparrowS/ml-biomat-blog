# From static to images: diffusion, scores, and conditioning

Source: https://ml-biomat.com/tutorials/machine-learning/m34/en/
Language: en

Follow actual denoising trajectories, compare DDPM, DDIM, and guidance, then enter latent space.

## Drawing a ring from television static

Mix random static into a drawing of a ring. First its boundary becomes unclear; eventually even the presence of a ring is uncertain. Now reverse the challenge: give a machine a screen of static and ask it to draw a ring. Can a sequence of corrections organize the pixels into a plausible shape? This is the basic task of diffusion generation. It is useful when one condition admits many candidates, such as illustration sketches, speech segments, or possible robot motions. The condition determines the kind of answer, while starting noise and the sampling procedure supply variation.

Restoring a known photograph after adding noise and generating a new image from independent noise are different tasks. During generation, there is no unique original photograph hidden behind the static. The model has learned from many examples and proposes a new one. Keeping this distinction in view explains why training can use known noise labels, why generation must estimate its corrections, and why repeated generation can produce different answers to the same request. It also prevents a misleading interpretation of a reverse trajectory as the recovery of a particular training image.

In 2015, Sohl-Dickstein and colleagues described a generative approach that gradually destroys data and learns the reverse process, drawing on a process perspective from nonequilibrium thermodynamics. DDPM in 2020 made the connection between gradual denoising and noise-prediction training especially effective. The practical difficulty behind this development is easy to appreciate: mapping a whole random image directly into a coherent picture is complex. Dividing the job into small corrections, and specifying the noise level of each correction, gives the network a more definite task. We will first inspect directions on a two-dimensional plane, then train a model that actually generates 8×8 rings and crosses.

![Top: a test cross corrupted along a genuine Markov path. Bottom: a ring generated from independent noise. These rows are separate processes. Arrays retain raw values; displayed grayscale saturates outside \[−1,1\].](https://ml-biomat.com/static/tutorials/machine-learning/figures/42eafd77ffa1e5c1fc40f8f1.svg?v=42eafd77ffa1)

Figure 1Top: a test cross corrupted along a genuine Markov path. Bottom: a ring generated from independent noise. These rows are separate processes. Arrays retain raw values; displayed grayscale saturates outside [−1,1].

## Adding noise while keeping track of each distribution

An image can be flattened into a list of numbers. Our images contain 64 pixels, with −1 for background and 1 for solid ink; averaged boundaries take intermediate values. One corruption step shrinks the existing values slightly and adds independent standard Gaussian noise. Standard means zero mean and unit variance, so the perturbation has no preferred sign. Square roots appear in the signal and noise coefficients because independent variances add, while multiplying a random variable by a coefficient multiplies its variance by the square of that coefficient.

$$
x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t,\quad \alpha_t=1-\beta_t,\quad \bar\alpha_t=\prod_{j=1}^{t}\alpha_j,\qquad x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/afd3e05d1c68845d6dd89d64.svg) | Clean sample, previous state, and current state, all d-dimensional vectors; d=64 for images and d=2 for points. Coordinates are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c290ee14e71a69efaf1d339d.svg) | Noise index from 1 to T, total step count 64, and product index; these are not physical seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/590d661f97b5749e1a61c517.svg) | Single-step noise variance proportion, single-step signal variance retention, and cumulative retention, all dimensionless; initially ᾱ₀=1. |
| ![Formula](https://ml-biomat.com/static/agent-math/d1c9e542a3bf09d0034a4de3.svg) | Independent standard-normal d-vectors; the first is a step innovation and the second equivalent accumulated noise. The expressions describe the same marginal distribution. |

Expanding the recursion gives accumulated noise variance 1−ᾱ_t, permitting direct construction at a selected time. For x₀=1, ᾱ_t=0.64, ε=−0.5, the result is 0.8−0.3=0.5. With that particular noise known, inversion gives x₀=(0.5+0.3)/0.8=1. Generation instead requires an estimated noise.

Single-step retention and cumulative retention describe different quantities. Losing a small amount of signal at each step can remove almost all of it over many steps. Cumulative retention is the product of the individual retention factors. Expanding the recursion shows that old noise is repeatedly attenuated while fresh independent noise is added. Their sum remains Gaussian, so a sample at any chosen noise level can be constructed directly from the clean image and a new Gaussian draw. Training can use this shortcut instead of simulating all preceding steps for every example.

The code uses a 64-step cosine schedule, retaining substantial signal initially and reducing it toward the end. The final single-step noise proportion is capped at 0.999. Actual cumulative signal retention at step 64 is about 5.93×10^{−7}, making a standard Gaussian a useful starting approximation for generation. A schedule specifies the noise levels; a sampler specifies how to move between them. In the figure, the forward row is an actual Markov corruption path of a test cross. The reverse row starts from independent noise and requests a ring. The rows illustrate two processes, rather than reconstruction of the same image.

## Learning a target we can check: the noise that was added

Training noise is generated by us, so its value is known. We draw a training image and a time index, construct the noisy image using the cumulative formula, and ask the network for 64 noise estimates. Pixelwise squared differences between predicted and actual noise form the learning objective. Random time indices expose the same network to nearly clean images, ambiguous outlines, and almost pure noise. Time information matters because an identical gray pixel carries different evidence at low and high noise levels. The model learns how its correction should depend on that context.

$$
L(\theta)=\mathbb E_{x_0,c,t,\epsilon}\!\left[\frac1d\left\|\epsilon-\epsilon_\theta\!\left(\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,t,c\right)\right\|_2^2\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ebaa51d428d62bfd4786339f.svg) | Trainable parameters, network predicting d noise components, and mean noise-squared-error objective. |
| ![Formula](https://ml-biomat.com/static/agent-math/d1eb7bc324e541f723ab8009.svg) | Training sample, class condition including null, uniformly sampled time 1…64, and independent standard-normal noise. |
| ![Formula](https://ml-biomat.com/static/agent-math/d04bd1bd8af9b2288f302d50.svg) | Average over these random quantities, coordinate count, sum of squared components, and cumulative signal retention; the error is dimensionless. |

For true noise (1,−1) and prediction (0.5,−0.5), average squared error is (0.25+0.25)/2=0.25, then averaged across the batch. The squared-error optimum is the conditional mean of noise given noisy input, time, and condition, accommodating multiple possible clean-image/noise combinations.

Our network represents time with 16 sine–cosine pairs and concatenates these with the pixels and a three-dimensional class code. Two hidden layers of width 128 produce the noise estimate. The three codes mean ring, cross, and absent condition, giving 37,568 trainable parameters overall. Flattening is manageable for a small image. Higher-resolution denoisers often exchange information across spatial scales. A U-Net reduces resolution to gather broad structural information, then restores resolution while skip connections supply finer features. Coarse representations help decide where an object belongs; finer representations recover boundaries and texture. Time information modulates what each stage should correct.

Once noise has been estimated, subtracting its contribution gives an estimate of the clean image. DDPM combines that estimate with the current noisy state to obtain the next-step mean, then adds a random perturbation with a specified variance. The final variance is zero, bringing the output to the image endpoint. At high noise, the clean-image estimate can be inaccurate because division by a very small cumulative-signal square root amplifies prediction errors. The implementation clips the estimate to the training pixel range, −1 to 1. This operation is part of the actual sampler and should be considered alongside the network prediction when interpreting results.

$$
\hat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\,\hat\epsilon}{\sqrt{\bar\alpha_t}},\quad \tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,\qquad \mu_t=\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}\hat x_0+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t,\qquad x_{t-1}=\mu_t+\sqrt{\tilde\beta_t}\,\xi
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a1eec75ae8541f9a02f11387.svg) | Predicted noise, inferred clean-image estimate, and current d-dimensional state. The implementation clips x̂₀ to [−1,1] before the mean calculation. |
| ![Formula](https://ml-biomat.com/static/agent-math/4be26bade2781b22846fb0c8.svg) | Reverse Gaussian mean d-vector, per-coordinate posterior variance, and independent standard-normal d-vector; the last step has no random term. |
| ![Formula](https://ml-biomat.com/static/agent-math/b36d1cab37b8c12e9f8817e7.svg) | Previously defined single-step and cumulative proportions and current index; all coordinates and variances here are dimensionless. |

For known true x₀, completing the square in the forward Gaussian joint distribution yields these posterior coefficients. Sampling substitutes the network estimate for unknown x₀. At t=1, ᾱ₀=1: posterior variance and the second coefficient vanish, while the first coefficient equals one, giving x̂₀ directly. With ᾱ_t=0.64, x_t=0.5, and estimated noise −0.5, x̂₀=1.

## Why denoising arrows point toward the data

Set images aside and imagine two clusters of points on a plane. Noise broadens the clusters until they overlap. At any location, we can ask which direction increases the probability density at that noise level. The gradient of log density answers this question and is called the score. A two-dimensional score has two components: it is a direction vector, rather than a scalar image-quality rating or a class probability. Viewing it as a field of arrows makes the relation between noise prediction and motion toward plausible data much easier to inspect.

$$
s_t(x)=\nabla_x\log p_t(x)\approx-\frac{\epsilon_\theta(x,t)}{\sqrt{1-\bar\alpha_t}},\qquad \nabla_x\log\mathcal N(x;\mu,vI)=\frac{\mu-x}{v}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/265f560b7424dae7e9bb959e.svg) | Marginal density at time t, its d-dimensional score, and gradient with respect to every position component. |
| ![Formula](https://ml-biomat.com/static/agent-math/f5a4dcd34fbea73d591b6a1f.svg) | Unconditional noise predictor and cumulative retention; a conditional network corresponds to a conditional-density score. |
| ![Formula](https://ml-biomat.com/static/agent-math/317b5d2f052f838279d9fe18.svg) | Gaussian mean d-vector, per-coordinate variance, d×d identity, and location. Score has inverse-coordinate units, dimensionless here. |

Differentiating the Gaussian log-density term −||x−μ||²/(2v) gives (μ−x)/v. Given x₀=1 and ᾱ=0.64, corruption has mean 0.8 and variance 0.36; at x=0.5 its conditional score is 0.3/0.36=0.833333. This is conditional on that clean point. The data-marginal score averages conditional scores over possible clean points, which is supplied by the noise conditional mean learned under squared loss.

For a Gaussian with known mean, the arrows point toward that mean. Their magnitude grows with distance and decreases with variance. In a two-Gaussian mixture, a location can lie in the tails of both components. The correct arrow therefore averages their directions using their relative likelihood at that location, rather than always selecting the closest center. Orange arrows in the figure are calculated from the known mixture; blue arrows come from a separate learned network with 6,530 parameters. Grid root-mean-square errors are 1.643, 0.154, and 0.057 at the three displayed times. Low-noise fields are steeper, and the uniform grid includes low-density tails, so the arrow scale and density background matter when reading these errors.

![Two-dimensional score fields at three noise levels: orange analytic Gaussian-mixture directions, blue learned directions, and gray true noisy density. Displayed arrows use a 9×9 subset; RMSE uses the full 17×17 grid. Panels share arrow scale and density color scale.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d3412f274401b3a163466c61.svg?v=d3412f274401)

Figure 2Two-dimensional score fields at three noise levels: orange analytic Gaussian-mixture directions, blue learned directions, and gray true noisy density. Displayed arrows use a 9×9 subset; RMSE uses the full 17×17 grid. Panels share arrow scale and density color scale.

Multi-noise score learning in 2019 made a useful strategy explicit: first find directions in a broad, smooth distribution, then gradually move toward sharper distributions. The later stochastic-differential-equation formulation connected these ideas to continuous time. A stochastic differential equation combines deterministic drift with random motion. Its probability-flow ordinary differential equation has a deterministic velocity and, with an exact score, shares the same sequence of marginal distributions. Matching distributions does not require matching individual particle trajectories. That distinction prepares us to understand why several sampling routes can use the same learned information.

$$
dx=f(x,t)\,dt+g(t)\,dW_t,\qquad dx=[f(x,t)-g(t)^2s_t(x)]\,dt+g(t)\,d\bar W_t\quad(dt<0),\qquad \frac{dx}{dt}=f(x,t)-\tfrac12g(t)^2s_t(x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d3e56d32773c66fd5e2759a0.svg) | Continuous state, continuous noise time, d-dimensional drift, and scalar diffusion amplitude; f has coordinate/time units and g coordinate/√time units. |
| ![Formula](https://ml-biomat.com/static/agent-math/12a030d7b0da4d1bbf359805.svg) | Forward and reverse Brownian increments, with per-coordinate variances dt and \|dt\| respectively; the reverse equation is integrated from larger to smaller t. |
| ![Formula](https://ml-biomat.com/static/agent-math/bb9ea1db401c1b448204586d.svg) | Exact marginal score, squared diffusion amplitude, and probability-flow ODE velocity; matching marginals requires the correct score and corresponding initial distribution. |

The first equation is the forward SDE, the second its reverse, and the third the deterministic probability-flow ODE. For a stationary standard normal with f=−x/2, g=1, and s=−x, reverse drift is +x/2 but dt is negative. Probability-flow velocity is zero. Stationary particles can maintain the same Gaussian population distribution, illustrating why equal marginals need not imply equal trajectories.

A small numerical step makes the discrete-to-continuous connection concrete. Let the time interval be 0.01 and the single-step noise variance also be 0.01. Signal is multiplied by the square root of 0.99, approximately 0.994987, so its mean displacement is about −0.005013 times its current position. Noise standard deviation is 0.1. Dividing mean displacement by the time interval approaches a drift of −0.5 times position per unit time, while noise standard deviation scales with the square root of the interval, as a Brownian increment does. A continuous limit arises by shrinking intervals while matching these coefficients. Our 64-level schedule remains a discrete construction, and a DDIM jump across several levels must use its own update. Smooth-looking trajectories alone do not make two samplers numerically equivalent.

## Using one model with 64 steps or 16 steps

Training does not force generation to use a single step count. DDIM constructs a different family of processes with the training marginals preserved. When its additional stochastic term is set to zero, a fixed starting noise and condition determine the subsequent path. Each step estimates the clean endpoint and recombines that estimate with residual noise at a chosen lower noise level. Reducing the timetable from 64 levels to 16 reduces network evaluations, while changing how prediction errors and larger steps influence the result. A deterministic path is reproducible, but its accuracy still depends on the model and its numerical treatment.

$$
\hat\epsilon_{\rm consistent}=\frac{x_t-\sqrt{\bar\alpha_t}\,\hat x_0}{\sqrt{1-\bar\alpha_t}},\qquad x_s=\sqrt{\bar\alpha_s}\,\hat x_0+\sqrt{1-\bar\alpha_s}\,\hat\epsilon_{\rm consistent},\qquad 0\le s<t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cae1ce632ae35c9c5529a926.svg) | Current and next selected time indices and their d-dimensional states; the next time may skip multiple training levels. |
| ![Formula](https://ml-biomat.com/static/agent-math/9fa7e35ea97ef40ec2c7748a.svg) | Clipped clean-image estimate and residual recomputed from the current state and that estimate. |
| ![Formula](https://ml-biomat.com/static/agent-math/3728c71b94ab6bc4fd00b2e9.svg) | Cumulative signal retention at the two times; this is DDIM with additional stochastic term η=0. All quantities are dimensionless. |

For ᾱ_t=0.64, x_t=0.5, and x̂₀=1, the consistent residual is −0.5. Selecting ᾱ_s=0.81 gives x_s=0.9−0.5√0.19≈0.682055. At endpoint s=0, ᾱ₀=1 and the update returns x̂₀. Fewer steps reduce evaluations, while model errors and the skipped intervals can change the output.

We compare DDIM with 64, 16, and 8 steps using the same trained weights and the same 64 initial noise vectors. Because clean-image estimates are clipped, the code recomputes residual noise to remain consistent with those clipped estimates before moving to the next time. Otherwise the estimated image plus residual would no longer reconstruct the current state. This detail ties the formula to the displayed output. A sampler comparison is most informative when the initial noise, conditions, weights, and clipping rules are kept explicit rather than allowing several factors to change at once.

![The first twelve generated samples in fixed order, alternating ring and cross requests. Columns share initial noise. Rows are DDPM64, DDIM64, DDIM16, and DDIM8, all with ordinary conditioning w=1.](https://ml-biomat.com/static/tutorials/machine-learning/figures/dcf1b1bbab8f4d9b501e6101.svg?v=dcf1b1bbab8f)

Figure 3The first twelve generated samples in fixed order, alternating ring and cross requests. Columns share initial noise. Rows are DDPM64, DDIM64, DDIM16, and DDIM8, all with ordinary conditioning w=1.

Each column in the figure starts from the same noise, and every row displays the first 12 outputs in their original order. DDPM with 64 steps gives more continuous outlines in this experiment. DDIM outputs from this small network contain gaps, extra marks, and shape distortions. An independent shape classifier agrees with the requested class for 63/64, 57/64, 57/64, and 56/64 outputs respectively. The equal DDIM64 and DDIM16 class counts do not imply pixelwise agreement. To choose a sampling budget, specify the properties that matter, then measure which ones change as the number of steps decreases.

## Inspect actual generated pixels step by step

Every frame is recorded from actual sampling. Methods share initial noise. Select a sample and pixel to compare the current state, its current endpoint estimate, and the final output.

[Figure: Pixel states, trajectories, and a fixed sample group](https://ml-biomat.com/tutorials/machine-learning/m34/en/#M34-board)

Red outlines mark the selected pixel. The trace retains raw values; grayscale maps [−1,1] to white–black and saturates outside that interval. The bottom strip shows all eight retained samples at the current step, with alternating ring and cross requests. Playback starts paused; native controls support keyboard changes.

## Turning “draw a ring” into an adjustable direction

Conditional generation passes a request to the model. We use a class code; a text-conditioned model can use vectors representing a sentence. Classifier-free guidance occasionally removes conditions during training, allowing one network to predict both a general denoising correction and a correction informed by the request. Here each training example has a 15% chance of receiving the absent-condition code. At sampling time, both predictions are evaluated. Their difference measures the change supplied by the condition, and a coefficient controls how strongly that change contributes to the update.

$$
\hat\epsilon_w=\epsilon_\theta(x_t,t,\varnothing)+w\,[\epsilon_\theta(x_t,t,c)-\epsilon_\theta(x_t,t,\varnothing)]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/79c9cb0224e7f17ab5f2c8e1.svg) | Noisy state, time, requested class or other condition, and null-condition code. |
| ![Formula](https://ml-biomat.com/static/agent-math/2475ae267775357fa1147f48.svg) | Noise prediction by the same network, combined d-dimensional prediction, and dimensionless guidance weight; w=0 is unconditional and w=1 ordinary conditional. |

For unconditional prediction 0.2 and conditional prediction −0.1, w=3 gives 0.2+3(−0.1−0.2)=−0.7. Linear extrapolation strengthens the conditional difference. The output is still predicted noise, which a sampler must convert to an image update. Our code uses two network calls for w>0 and one for w=0.

Our convention assigns zero to the unconditional prediction, one to the ordinary conditional prediction, and three to three times the conditional difference added to the unconditional prediction. Some publications or software use a shifted convention in which ordinary conditioning is called zero guidance. Reading the formula together with the parameter avoids confusion. Stronger guidance can improve agreement with a request, narrow variation within a class, or amplify modeling errors in some regions. These effects can be observed directly in a fixed-noise comparison instead of assuming that a larger number always means a better image.

![Sixteen-step DDIM with identical initial noise and guidance weights zero, one, and three. Even indices request rings and odd indices crosses; the unconditional first row does not use those requests.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6225c0fc8a983cb65eb4641e.svg?v=6225c0fc8a98)

Figure 4Sixteen-step DDIM with identical initial noise and guidance weights zero, one, and three. Even indices request rings and odd indices crosses; the unconditional first row does not use those requests.

With the same 16-step DDIM sampler and the same noise, weights zero, one, and three give class agreement of 36/64, 57/64, and 64/64. Mean within-request pixel variances are approximately 0.1063, 0.0985, and 0.0777. Lower variance means less pixel variation; random artifacts can also increase variance, so the contact sheet remains part of the evidence. The logistic-regression classifier is used after generation for measurement only. It does not train the denoiser or provide sampling gradients. Guidance here comes from two predictions by the same denoiser, which explains the term classifier-free.

Condition dropout changes the information supplied to the network; it does not remove the training image or replace the noise target by zero. In a batch of 128 images, about 19.2 receive the null code on average, with the realized count varying randomly. Those examples retain their ring or cross structure, so the unconditional branch learns denoising for the mixture of both classes. Ordinary conditioning narrows the plausible answers using the label. When the two predictions differ little, guidance changes the update little; a large difference can make linear extrapolation move toward regions less represented during training. A convention that starts from the conditional prediction would call our weight three an additional guidance coefficient two. Converting that convention before comparing experiments keeps the actual update consistent.

## Compress first, then denoise repeatedly in latent space

A 512×512 color image contains 786,432 numbers. Running a large network at that resolution repeatedly can be expensive. Latent diffusion first uses an encoder to represent structure and appearance in a smaller tensor, learns denoising in that representation, and finally uses a decoder to reconstruct an image. For an illustrative encoder output of 64×64×4, the tensor contains 16,384 elements, one forty-eighth of the input count. This ratio describes selected tensor shapes rather than a file-compression ratio. Encoder computation and information loss also belong in the system-level assessment.

$$
z_0=E(x),\qquad z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon,\qquad \hat x=D(\hat z_0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0c30339c653b4a1e34212ca7.svg) | Input image, encoder, and clean latent tensor; illustrative shapes are 512×512×3 to 64×64×4. |
| ![Formula](https://ml-biomat.com/static/agent-math/86b07ee12f031d15e41b128c.svg) | Noisy latent state and standard-normal noise with the latent tensor’s shape, plus cumulative retention. |
| ![Formula](https://ml-biomat.com/static/agent-math/faf0419082fed59255822f01.svg) | Generated latent representation, decoder, and output image; latents use the training scaling convention and have no physical unit. |

The illustrative image has 786432 components, versus 16384 latent values, a 48-fold element-count reduction. Encoding and decoding still require computation and determine which visual information is retained. The latent representation and its scaling must be established before denoiser training. Generation starts from latent noise and decodes after repeated updates.

Latent diffusion, introduced in a 2021 preprint and published in 2022, connected perceptual compression with diffusion generation. It shares the encoder–decoder idea developed in the VAE chapter, while learning a more flexible generative distribution over latent representations. Text conditioning can enter through cross-attention: spatial features supply queries and text features supply keys and values, allowing locations to retrieve relevant word information. Time conditioning answers how noisy the current representation is; text conditioning answers what should appear. These inputs have complementary roles in the same denoising computation.

![Text conditions a latent denoiser; repeated latent updates are followed by image decoding.](https://ml-biomat.com/static/tutorials/machine-learning/figures/3ceac8991126bd1810910422.svg?v=3ceac8991126)

Figure 5Conditioning, iterative latent updates, and decoding. Adapted from the Diffusion Explainer architecture by Polo Club of Data Science under MIT, with original copyright text retained. Labels and illustrative tensor dimensions are redrawn; the chapter experiment operates in pixel space.

The important loop in the diagram is the repeated update of the latent tensor. Image decoding is usually performed at the endpoint. Our actual experiment operates directly on small pixel arrays, making every coordinate available for inspection; latent diffusion places the corresponding process inside a compressed representation. Fine lettering or exact geometric relationships may already be affected by the encoder. When studying a high-resolution system, evaluate compression reconstruction, latent generation, and text agreement separately so that errors can be connected to the stage where they arise.

Compression quality can first be measured independently. Take a held-out image, pass it through the encoder and decoder without diffusion, and compare input with reconstruction. Blurred lettering at this stage belongs to representation and decoding. Next generate latent variables with diffusion and examine whether shape or texture errors increase. The two stages need not contribute errors additively, because the decoder is nonlinear: a small change in one latent direction may move an edge, while another mainly changes a smooth color region. Latent scaling also sets the meaning of a noise level. Doubling latent values while adding the same unit-variance noise increases relative signal strength and changes the task presented to the denoiser. Reusing a model therefore means preserving its encoder, scaling factor, and decoder together, as well as its denoising weights.

## Keeping pictures, measurements, and the full program together

Explicit geometric rules generate all data. Rings vary in radius and position; crosses vary in angle, length, and stroke width. Shapes are drawn on a 32×32 grid and averaged over 4×4 blocks to produce 8×8 grayscale images with antialiased boundaries. Independent seeds create 3,072 training images, 512 validation images, and 512 test images, balanced across both classes. Training uses 5,000 updates of 128 images. Fixed validation noise is evaluated every 250 updates, selecting the final checkpoint at update 5,000. Validation and test noise mean-squared errors are approximately 0.1746 and 0.1798.

The program retains all 64 outputs for every sampling setting, requested labels, configuration details, and complete trajectories for the first eight images. The shape classifier has 100% accuracy on the independent clean test set; agreement on generated images measures the shape that this classifier recognizes. Nearest-training-image pixel distance measures similarity, within-request variance describes variation, and denoiser-call counts quantify the main sampling work. A correctly classified image can still have broken edges. Similarity to training images can also follow from a narrowly defined geometric family. Keeping these measurements beside the actual samples reveals the particular question each one answers.

![Left: checkpoint errors on fixed validation noise. Middle: class agreement across 64 outputs per method. Right: within-request pixel variance, annotated with actual denoiser-call counts; each call processes 64 images together.](https://ml-biomat.com/static/tutorials/machine-learning/figures/91ffc6030665b9fd8cb8d1d5.svg?v=91ffc6030665)

Figure 6Left: checkpoint errors on fixed validation noise. Middle: class agreement across 64 outputs per method. Right: within-request pixel variance, annotated with actual denoiser-call counts; each call processes 64 images together.

The complete program trains the image denoiser, generates six comparison groups, then trains the two-dimensional score network. Outputs include weights, numerical arrays, replay data, and five scientific figures. During training, a single noise level is sampled for each example. During generation, the network is called repeatedly along a timetable. Follow those two routes in the code: first locate the construction of the noisy input and its known noise label, then inspect how the sampler converts a prediction into the next state. Keeping initial noise fixed makes later experiments with step counts, guidance weights, or shape rules easier to compare.

### Complete Python: noise prediction, six sampling settings, and 2D scores

Run python main.py --output results --language en using NumPy, PyTorch, scikit-learn, and Matplotlib. No data or model downloads are needed. Both networks are actually trained; geometry, weights, seeds, outputs, and trajectories are retained.

```
"""Learn diffusion scores on points, then train a conditional image denoiser.
Images are original antialiased ring/cross shapes generated by explicit geometry.
"""
from pathlib import Path
import argparse,json,math,copy,platform,time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.linear_model import LogisticRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
T=64;times=torch.arange(T+1,dtype=torch.float64);schedule=torch.cos((times/T+.008)/1.008*math.pi/2).square();schedule/=schedule[0].clone();beta=(1-schedule[1:]/schedule[:-1]).clamp(max=.999).float();alpha=1-beta;abar=torch.cat([torch.ones(1),torch.cumprod(alpha,0)])
class Denoiser(nn.Module):
 def __init__(self,dim,hidden,conditional):
  super().__init__();self.conditional=conditional;self.register_buffer('frequencies',torch.exp(-math.log(10000)*torch.arange(16)/16));self.net=nn.Sequential(nn.Linear(dim+32+(3 if conditional else 0),hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,dim))
 def forward(self,x,t,c=None):
  phase=t[:,None]*self.frequencies[None];parts=[x,phase.sin(),phase.cos()]
  if self.conditional:parts.append(F.one_hot(c,3).float())
  return self.net(torch.cat(parts,1))
def noised(x,t,eps):return abar[t,None].sqrt()*x+(1-abar[t,None]).sqrt()*eps
def glyphs(n,seed):
 rng=np.random.default_rng(seed);labels=np.arange(n)%2;rng.shuffle(labels);grid=(np.arange(32)+.5)/4-.5;xx,yy=np.meshgrid(grid,grid);result=[]
 for c in labels:
  dx=xx-(3.5+rng.uniform(-.45,.45));dy=yy-(3.5+rng.uniform(-.45,.45));width=rng.uniform(.45,.7)
  if c==0:ink=np.abs(np.sqrt(dx*dx+dy*dy)-rng.uniform(1.8,2.5))<width/2
  else:
   angle=rng.uniform(-.35,.35);u=dx*np.cos(angle)+dy*np.sin(angle);v=-dx*np.sin(angle)+dy*np.cos(angle);length=rng.uniform(2.2,2.8);ink=((np.abs(u)<width/2)&(np.abs(v)<length))|((np.abs(v)<width/2)&(np.abs(u)<length))
  result.append(ink.reshape(8,4,8,4).mean((1,3)).reshape(-1)*2-1)
 return np.array(result,dtype='float32'),labels
train,train_y=glyphs(3072,340);valid,valid_y=glyphs(512,341);test,test_y=glyphs(512,342);xt=torch.tensor(train);yt=torch.tensor(train_y)
torch.manual_seed(343);image_model=Denoiser(64,128,True);opt=torch.optim.Adam(image_model.parameters(),lr=.001);rng=torch.Generator().manual_seed(344);vrng=torch.Generator().manual_seed(345);vt=torch.randint(1,T+1,(len(valid),),generator=vrng);ve=torch.randn((len(valid),64),generator=vrng);vx=noised(torch.tensor(valid),vt,ve);history=[];best=float('inf');best_state=None;best_step=0;start=time.perf_counter()
for step in range(1,5001):
 idx=torch.randint(len(xt),(128,),generator=rng);t=torch.randint(1,T+1,(128,),generator=rng);eps=torch.randn((128,64),generator=rng);x=noised(xt[idx],t,eps);c=yt[idx].clone();c[torch.rand(128,generator=rng)<.15]=2;prediction=image_model(x,t,c);loss=F.mse_loss(prediction,eps);opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(image_model.parameters(),1);opt.step()
 if step%250==0:
  with torch.no_grad():vl=F.mse_loss(image_model(vx,vt,torch.tensor(valid_y)),ve).item()
  history.append([step,loss.item(),vl])
  if vl<best:best=vl;best_step=step;best_state=copy.deepcopy(image_model.state_dict())
image_model.load_state_dict(best_state);image_model.eval();training_seconds=time.perf_counter()-start;torch.save(dict(model=image_model.state_dict(),beta=beta,best_step=best_step),out/'image-denoiser.pt')
te=torch.randn((len(test),64),generator=vrng);tt=torch.randint(1,T+1,(len(test),),generator=vrng)
with torch.no_grad():test_mse=F.mse_loss(image_model(noised(torch.tensor(test),tt,te),tt,torch.tensor(test_y)),te).item()
# A classifier measures one aspect of shape fidelity, separately from denoiser training.
classifier=LogisticRegression(C=1,max_iter=1000).fit(train,train_y);classifier_test=float((classifier.predict(test)==test_y).mean())
sample_rng=torch.Generator().manual_seed(346);initial=torch.randn((64,64),generator=sample_rng);requests=torch.arange(64)%2
@torch.no_grad()
def guided(x,t,c,weight):
 null=torch.full_like(c,2);unconditional=image_model(x,t,null)
 if weight==0:return unconditional
 conditional=image_model(x,t,c);return unconditional+weight*(conditional-unconditional)
@torch.no_grad()
def generate(method='ddpm',steps=64,weight=1.,seed=347):
 x=initial.clone();rng=torch.Generator().manual_seed(seed);path=[dict(t=T,x=x[:8].numpy().tolist())];predicted=[]
 levels=list(range(T,0,-1)) if method=='ddpm' else np.linspace(T,1,steps,dtype=int).tolist()
 for i,level in enumerate(levels):
  t=torch.full((len(x),),level,dtype=torch.long);noise=guided(x,t,requests,weight);x0=((x-(1-abar[level]).sqrt()*noise)/abar[level].sqrt()).clamp(-1,1)
  predicted.append(dict(t=level,x0=x0[:8].numpy().tolist()))
  if method=='ddpm':
   prev=level-1;variance=beta[level-1]*(1-abar[prev])/(1-abar[level]);mean=abar[prev].sqrt()*beta[level-1]/(1-abar[level])*x0+alpha[level-1].sqrt()*(1-abar[prev])/(1-abar[level])*x;x=mean+(variance.sqrt()*torch.randn(x.shape,generator=rng) if prev>0 else 0)
  else:
   prev=levels[i+1] if i+1<len(levels) else 0
   # Recompute residual noise after clipping x0, keeping the decomposition consistent.
   noise=(x-abar[level].sqrt()*x0)/(1-abar[level]).sqrt();x=abar[prev].sqrt()*x0+(1-abar[prev]).sqrt()*noise
  path.append(dict(t=int(prev),x=x[:8].numpy().tolist()))
 return x.numpy(),path,predicted
settings=[('DDPM64',dict(method='ddpm',steps=64,weight=1)),('DDIM64',dict(method='ddim',steps=64,weight=1)),('DDIM16',dict(method='ddim',steps=16,weight=1)),('DDIM8',dict(method='ddim',steps=8,weight=1)),('CFG0',dict(method='ddim',steps=16,weight=0)),('CFG3',dict(method='ddim',steps=16,weight=3))]
outputs={};metrics={};replays={};requests_np=requests.numpy()
for name,setting in settings:
 started=time.perf_counter();generated,path,predicted=generate(**setting);seconds=time.perf_counter()-started;outputs[name]=generated;replays[name]=dict(settings=setting,path=path,predicted=predicted)
 prediction=classifier.predict(generated);distance=((generated[:,None]-train[None])**2).mean(2).min(1)
 metrics[name]=dict(condition_match=float((prediction==requests_np).mean()),predicted_ring_fraction=float((prediction==0).mean()),nearest_training_mse=float(distance.mean()),mean_pixel_variance=float(np.mean([np.var(generated[requests_np==c],axis=0).mean() for c in [0,1]])),denoiser_calls=setting['steps']*(1 if setting['weight']==0 else 2),seconds=seconds)
# A genuine forward Markov path, distinct from the direct marginal sampling used in training.
forward_rng=torch.Generator().manual_seed(348);forward=[torch.tensor(test[0])];current=forward[0]
for t in range(1,T+1):current=alpha[t-1].sqrt()*current+beta[t-1].sqrt()*torch.randn(64,generator=forward_rng);forward.append(current)
forward=torch.stack(forward).numpy()
# Learn the same epsilon objective for a two-Gaussian point mixture.
r=np.random.default_rng(349);point_labels=r.integers(0,2,4096);point_centers=np.array([[-1.,0.],[1.,0.]],dtype='float32');point_data=(point_centers[point_labels]+r.normal(0,.25,(4096,2))).astype('float32');point_tensor=torch.tensor(point_data)
torch.manual_seed(350);point_model=Denoiser(2,64,False);po=torch.optim.Adam(point_model.parameters(),lr=.002);prng=torch.Generator().manual_seed(351)
for step in range(2000):
 idx=torch.randint(4096,(256,),generator=prng);t=torch.randint(1,T+1,(256,),generator=prng);eps=torch.randn((256,2),generator=prng);loss=F.mse_loss(point_model(noised(point_tensor[idx],t,eps),t),eps);po.zero_grad();loss.backward();po.step()
torch.save(dict(model=point_model.state_dict(),beta=beta),out/'point-denoiser.pt')
axis=np.linspace(-2.5,2.5,17);gx,gy=np.meshgrid(axis,axis);grid=np.c_[gx.ravel(),gy.ravel()].astype('float32');fields=[]
for t in [8,32,56]:
 b=abar[t].item();means=point_centers*math.sqrt(b);variance=b*.25**2+(1-b);diff=means[None]-grid[:,None];lp=-np.sum(diff**2,axis=2)/(2*variance);prob=np.exp(lp-lp.max(1,keepdims=True));prob/=prob.sum(1,keepdims=True);truth=(prob[:,:,None]*diff).sum(1)/variance
 with torch.no_grad():learned=(-point_model(torch.tensor(grid),torch.full((len(grid),),t))/(1-abar[t]).sqrt()).numpy()
 fields.append(dict(t=t,score=learned.tolist(),truth=truth.tolist(),density=(np.exp(lp).mean(1)/(2*math.pi*variance)).tolist(),rmse=float(np.sqrt(np.mean((learned-truth)**2))),variance=variance))
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=3072,validation=512,test=512,image_shape=[8,8],classes=['ring','cross'],seeds=[340,341,342]),training=dict(steps=5000,best_step=best_step,parameters=sum(p.numel() for p in image_model.parameters()),batch=128,lr=.001,condition_dropout=.15,validation_noise_mse=best,test_noise_mse=test_mse,seconds=training_seconds),schedule=dict(T=T,alpha_bar_T=abar[-1].item(),beta_first=beta[0].item(),beta_last=beta[-1].item()),classifier=dict(test_accuracy=classifier_test,role='post-hoc shape-class evaluation; never used to guide generation'),generation=metrics,point_score=dict(parameters=sum(p.numel() for p in point_model.parameters()),steps=2000,grid_rmse={str(f['t']):f['rmse'] for f in fields}),hand=dict(noised_scalar=math.sqrt(.64)*1+math.sqrt(.36)*(-.5),recovered_scalar=(.5-math.sqrt(.36)*(-.5))/math.sqrt(.64),conditional_gaussian_score=-(-.5)/math.sqrt(.36),guidance_unconditional=.2,guidance_conditional=-.1,guidance_weight3=.2+3*(-.1-.2)))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'replay.json').write_text(json.dumps(dict(forward=forward.tolist(),forward_class=int(test_y[0]),alpha_bar=abar.tolist(),models=replays,requested_classes=requests_np[:8].tolist()),separators=(',',':')),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train=train,train_labels=train_y,validation=valid,validation_labels=valid_y,test=test,test_labels=test_y,initial_noise=initial.numpy(),requested_classes=requests_np,beta=beta.numpy(),alpha_bar=abar.numpy(),history=history,forward_path=forward,point_train=point_data,point_grid=grid,point_scores=np.array([f['score'] for f in fields]),point_truth=np.array([f['truth'] for f in fields]),**{name:values for name,values in outputs.items()})
def image_axis(ax,img):ax.imshow((np.array(img).reshape(8,8)+1)/2,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
fig,axs=plt.subplots(2,7,figsize=(13,4.8),layout='constrained');levels=[0,8,16,32,48,56,64]
for j,t in enumerate(levels):image_axis(axs[0,j],forward[t]);axs[0,j].set_title(f't={t}')
path=replays['DDPM64']['path'];levels_reverse=[64,56,48,32,16,8,0]
for j,t in enumerate(levels_reverse):image_axis(axs[1,j],next(f for f in path if f['t']==t)['x'][0]);axs[1,j].set_title(f't={t}')
axs[0,0].set_ylabel(tr('十字：前向加噪','Corruption (cross)'),fontsize=11);axs[1,0].set_ylabel(tr('圆环：独立生成','Generation (ring)'),fontsize=11);save(fig,'noise-path')
fig,axs=plt.subplots(4,12,figsize=(13,5.8),layout='constrained')
for row,name in enumerate(['DDPM64','DDIM64','DDIM16','DDIM8']):
 for col in range(12):
  image_axis(axs[row,col],outputs[name][col])
  if row==0:axs[row,col].set_title(tr('环','Ring') if col%2==0 else tr('十字','Cross'),fontsize=9)
 axs[row,0].set_ylabel(name,fontsize=11)
save(fig,'samplers')
fig,axs=plt.subplots(3,12,figsize=(13,4.8),layout='constrained')
for row,name in enumerate(['CFG0','DDIM16','CFG3']):
 for col in range(12):image_axis(axs[row,col],outputs[name][col])
 axs[row,0].set_ylabel(['w=0','w=1','w=3'][row],fontsize=12)
save(fig,'guidance')
fig,axs=plt.subplots(1,3,figsize=(13,4.2),layout='constrained');arrow_ids=np.arange(len(grid)).reshape(17,17)[::2,::2].ravel();maximum=max(max(f['density']) for f in fields)
for ax,f in zip(axs,fields):
 truth=np.array(f['truth']);score=np.array(f['score']);im=ax.contourf(gx,gy,np.array(f['density']).reshape(17,17),levels=np.linspace(0,maximum,15),cmap='Greys',alpha=.25);ax.quiver(grid[arrow_ids,0],grid[arrow_ids,1],truth[arrow_ids,0],truth[arrow_ids,1],color='#c18a57',angles='xy',scale_units='xy',scale=15,width=.004);ax.quiver(grid[arrow_ids,0],grid[arrow_ids,1],score[arrow_ids,0],score[arrow_ids,1],color='#125f82',angles='xy',scale_units='xy',scale=15,width=.003);ax.set(xlabel='x1',ylabel='x2',title=f"t={f['t']}; RMSE={f['rmse']:.3f}",xlim=(-2.7,2.7),ylim=(-2.7,2.7));ax.set_aspect('equal')
fig.colorbar(im,ax=axs,label=tr('加噪后的目标密度','Noisy target density'),fraction=.022,pad=.02)
save(fig,'score')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,2],color='#125f82');axs[0].set(xlabel=tr('参数更新数','Parameter updates'),ylabel=tr('固定验证噪声MSE','Fixed validation noise MSE'),title=tr('A  噪声预测学习','A  Learning noise prediction'))
names=list(metrics);pos=np.arange(len(names));axs[1].bar(pos,[metrics[n]['condition_match'] for n in names],color='#125f82');axs[1].set_xticks(pos,names,rotation=35,ha='right');axs[1].set(ylim=(0,1.06),ylabel=tr('后验分类器与请求一致率','Post-hoc classifier / request agreement'),title=tr('B  每设置64张图','B  64 images per setting'))
axs[2].scatter([metrics[n]['denoiser_calls'] for n in names],[metrics[n]['mean_pixel_variance'] for n in names],c=['#125f82']*4+['#bf7139','#648454'],s=45)
for n in names:axs[2].annotate(n,(metrics[n]['denoiser_calls'],metrics[n]['mean_pixel_variance']),xytext=(3,4),textcoords='offset points',fontsize=8)
axs[2].set(xlabel=tr('每批采样去噪器调用次数','Denoiser calls per sampling batch'),ylabel=tr('按请求分组的平均像素方差','Mean pixel variance within request groups'),title=tr('C  计算量与输出变化','C  Computation and output variation'));save(fig,'metrics')
print(json.dumps(summary,indent=2))
```

## Sounds and actions require their own measures of success

Diffusion can also operate on audio waveforms, spectrograms, or compressed sound representations. Temporal and phase relationships affect whether a sound is coherent. Evaluation therefore combines listening with checks of duration, noise, linguistic content, or agreement with a requested sound. A robot trajectory might contain several joint angles or spatial coordinates at every time position. A denoising network can propose corrections to the entire sequence, representing alternative routes around an obstacle. Joint limits, velocity, collision, and endpoint error become central measurements; visual smoothness answers only one part of the motion problem.

These applications share a computational structure: define the representation, choose a noise process, learn time-dependent predictions, and use a sampler to create candidates. They have different scales. Pixels here are normalized dimensionless values, audio may use normalized amplitudes, and motion combines positions, angles, and time under explicit unit conventions. Putting numerically dissimilar quantities into one unweighted squared error can make the largest-valued coordinates dominate. Representation and loss choices should make the deviations that matter to the task visible to learning and evaluation.

Three practical questions help organize a model choice. Does the training target describe the quantity that needs correction? Does the sampling budget produce suitable candidates? Does evaluation cover both requested properties and meaningful variation? Our rings and crosses let every prediction be expanded into 64 numbers, while the point experiment turns the same idea into a visible direction field. These views give concrete meanings to time conditioning, schedules, guidance, and sampling when reading work on image, speech, or motion generation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M34.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585)

   The 2015 forward corruption and learned reversal construction.

   Primary paper; no copied figures
2. [Denoising Diffusion Probabilistic Models](https://arxiv.org/html/2006.11239v2)

   Forward marginals, noise objective, and reverse Gaussian sampling.

   Primary paper; independent experiment
3. [Denoising Diffusion Implicit Models](https://arxiv.org/html/2010.02502v4)

   Processes preserving marginals, deterministic sampling, and reduced step counts.

   Primary paper; independent experiment
4. [Generative Modeling by Estimating Gradients of the Data Distribution](https://arxiv.org/abs/1907.05600)

   Multi-noise score learning in 2019.

   Primary paper; own analytic mixture figure
5. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/html/2011.13456v2)

   Reverse SDEs, probability-flow ODEs, and time direction.

   Primary paper; no copied figures
6. [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)

   Joint conditional/unconditional training and guidance conventions.

   Primary paper; independent experiment
7. [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752)

   Latent encoding, perceptual compression, and cross-attention.

   Primary paper; no copied figures
8. [Diffusion Explainer](https://poloclub.github.io/diffusion-explainer/)

   Architecture components for conditioning, latent denoising, and image decoding.

   MIT, Copyright 2022 Polo Club of Data Science; adapted diagram; license retained
