# From compressing an image to generating one: AE and VAE

Source: https://ml-biomat.com/tutorials/machine-learning/m33/en/
Language: en

Inspect bottlenecks, denoising, reparameterization, and the ELBO, then navigate a trained latent space.

## Put a picture on a small note, then draw it again

Suppose you can send a friend only a tiny note, but want them to redraw a picture. Copying every pixel takes too much space, so you might write “a narrow ring with a small gap at the top.” Your friend needs to understand that description to reconstruct the image. An autoencoder turns this collaboration into two jointly trained networks. The encoder writes a short vector, and the decoder reconstructs an image from it. Nobody specifies in advance whether the note should describe rings, gaps, or something else. Reconstruction error teaches the networks their own communication scheme. We want to know which structures the short description preserves and which details it leaves behind.

This connects representation learning with compression, denoising, and similarity search. An old photograph with isolated noise spots may benefit from reconstructing familiar contours while discarding accidental speckles. A large image collection may be easier to search through compact representations. However, successfully encoding an existing picture and drawing it again leaves another question open: if we invent a note at random, will the decoder draw a plausible new image? A variational autoencoder, or VAE, models how those notes should be distributed, connecting representations to probabilistic inference and generation.

Autoencoders build on learning internal representations through reconstruction error. Kingma and Welling’s 2013 Auto-Encoding Variational Bayes work used neural networks as approximate inference models and combined them with differentiable random sampling. The important change was more than adding noise: the encoder produced a distribution that participated in a probabilistic objective. The original tutorial figure below first illustrates a simpler capacity question: how does reconstruction error change with latent dimensionality? We then use the same handwriting examples to examine capacity, denoising, distributions, and sampling separately.

![Original CIFAR10 autoencoder capacity curve from the tutorial. Error follows that tutorial’s definition and is not directly compared with our per-pixel MSE. Phillip Lippe, UvA Deep Learning Tutorials, Tutorial 9, output cell \[11\], MIT, unchanged. This figure concerns AE training.](https://ml-biomat.com/static/tutorials/machine-learning/figures/7dcdf7e65e074c7bb7184673.svg?v=7dcdf7e65e07)

Figure 1Original CIFAR10 autoencoder capacity curve from the tutorial. Error follows that tutorial’s definition and is not directly compared with our per-pixel MSE. Phillip Lippe, UvA Deep Learning Tutorials, Tutorial 9, output cell [11], MIT, unchanged. This figure concerns AE training.

## Why a bottleneck can capture structure

Each image contains eight by eight pixels, giving 64 input coordinates after flattening. Our encoder passes through 64 hidden units and compresses the image into either two or eight latent coordinates. The decoder expands that vector through another 64 hidden units into 64 reconstructed intensities. Both sides learn from data, while the short intermediate vector creates a bottleneck. If all pixels varied independently, compression would discard substantial information. Handwritten digits instead contain repeated backgrounds, connected strokes, and recurring combinations. A smaller set of coordinates can describe some of these regularities. The bottleneck encourages shared structure to replace independent channels for every pixel.

$$
z=f_\phi(x),\quad \widehat x=g_\theta(z),\qquad L_{\mathrm{AE}}=\frac1{ND}\sum_{i=1}^N\sum_{j=1}^D(\widehat x_{ij}-x_{ij})^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/388c1172af1c00ded90619da.svg) | One input and reconstruction, D=64 normalized pixels; dimensionless intensities. |
| ![Formula](https://ml-biomat.com/static/agent-math/0fd0aa86c9a7c3e4aeec2bd1.svg) | d-dimensional latent, encoder with parameters φ, and decoder with parameters θ; d=2 or 8. |
| ![Formula](https://ml-biomat.com/static/agent-math/b2819cff441cb2ca0dd46db7.svg) | Number of averaged images, pixels per image, image index, and pixel index. |
| ![Formula](https://ml-biomat.com/static/agent-math/630f78f925061226dc19efb8.svg) | Mean squared error per image and pixel, in squared normalized-intensity units. |

Input (0.2,0.8) reconstructed as (0.3,0.6) has squared errors 0.01 and 0.04, averaging to 0.025. Here each image contributes 64 terms before averaging across images. Both networks receive the loss gradient. Denoising replaces the encoder input with a corrupted image while keeping the clean x as the target.

Reconstruction loss turns visual agreement into an optimizable number. Pixelwise squared error penalizes large intensity discrepancies more strongly and provides a direct gradient. Our two-dimensional autoencoder has test mean squared error of 0.03650 per pixel, falling to 0.01451 with eight latent dimensions. The contact sheet shows how additional capacity often preserves more definite strokes. Pixel error and visual judgment nevertheless differ. A sharp stroke shifted slightly from its target may receive a larger penalty than a blurred stroke in the correct location. Choosing a loss function specifies which differences the network should spend effort correcting.

Replacing 64 coordinates with two compresses representation dimension. Actual file compression also requires decisions about bit depth, quantization, transmission of the decoder, and coding any residual. A 32-bit floating-point coordinate costs more than a small integer, and the decoder itself occupies storage. We therefore distinguish fewer coordinates from fewer file bytes. Linear methods offer another reference: under linear encoding and decoding with squared loss and suitable conditions, autoencoders recover a principal subspace closely related to PCA. Nonlinear networks can unfold curved data structure, but their latent axes no longer come with unique orientations or automatic semantic names.

![Each column follows one test image: original, 2D AE, 8D AE, β=1 VAE mean-code reconstruction, noisy input, and 8D denoising AE. One intensity scale, 0–1, is used throughout. Data: E. Alpaydin, C. Kaynak, UCI handwritten digits, CC BY 4.0. Reconstructions are measured model outputs.](https://ml-biomat.com/static/tutorials/machine-learning/figures/22f3fd78345d72afc9ef69ee.svg?v=22f3fd78345d)

Figure 2Each column follows one test image: original, 2D AE, 8D AE, β=1 VAE mean-code reconstruction, noisy input, and 8D denoising AE. One intensity scale, 0–1, is used throughout. Data: E. Alpaydin, C. Kaynak, UCI handwritten digits, CC BY 4.0. Reconstructions are measured model outputs.

## Why a denoiser receives one image and targets another

An ordinary autoencoder reconstructs the input it receives. A denoising autoencoder receives a corrupted image and targets the original clean image. Because the corruption is introduced during training, we know the desired answer without manually relabeling every pixel. The model must infer missing structure from what remains. A missing bright point along a continuous stroke can be supported by neighboring pixels; an isolated speckle may have little structural support. The objective therefore changes from compressing and redrawing an observation to recovering regularities from a damaged observation. The type of training corruption should reflect the restoration problem we want to solve.

We add Gaussian pixel noise with standard deviation 0.25, then clip the corrupted input to the interval zero to one. On these noisy test images, the ordinary eight-dimensional autoencoder has reconstruction MSE of 0.03672 against the clean targets. A denoising model with the same bottleneck reduces that error to 0.02164. For clean inputs, the ordinary model obtains 0.01451 and the denoising model obtains 0.01632. Each adapts to a different input condition. Denoising training encourages unusual details to move toward familiar structures, helping with noise while sometimes removing a genuine small variation.

This also clarifies an anomaly-detection application. A model trained on normal examples may reconstruct some unusual inputs poorly. Yet a sufficiently flexible model may reconstruct anomalies well, and rare normal handwriting styles may receive large errors. A useful evaluation first defines the changes that count as anomalies and then includes examples of those changes alongside normal cases. Reconstruction error measures how well a learned structure fits an input; the largest error does not automatically identify a bad data record. Denoising, compression, and anomaly detection reuse similar components while differing in inputs, training targets, and decision rules.

## A VAE encodes a cloud of possibilities

An ordinary autoencoder assigns an image one deterministic latent coordinate. A VAE encoder outputs a mean and variance describing possible latent coordinates for that image. The note now circles a small region instead of specifying one exact location, and the decoder should produce compatible content across that region. Means place its center; standard deviations control its width. With two latent coordinates and a diagonal Gaussian, each image receives two means and two log variances. The diagonal assumption makes coordinates conditionally independent within that encoded distribution. Across different inputs, their means can still trace a complex and correlated overall arrangement.

$$
q_\phi(z\mid x)=\mathcal N(\mu_\phi(x),\operatorname{diag}(e^{\ell_\phi(x)})),\quad p(z)=\mathcal N(0,I),\quad p_\theta(x\mid z)=\mathcal N(g_\theta(z),\sigma_x^2 I)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6b767d33fc65203af063da4c.svg) | Approximate posterior, latent prior, and observation distribution; density values depend on variable units. |
| ![Formula](https://ml-biomat.com/static/agent-math/3045d5c77821c1da3694cbe4.svg) | Mean and log-variance vectors per image; d=2 with dimensionless latent coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0363af670b35ceb835b1520.svg) | Multivariate Gaussian, diagonal-matrix construction, and identity matrix: d×d in latent space and D×D in observation space. |
| ![Formula](https://ml-biomat.com/static/agent-math/f7d87e6f03dbedd326be8ece.svg) | D=64 conditional means from the decoder and observation-noise standard deviation, σ_x=0.25 here. |

For latent mean 0.5 and log variance ln0.25, variance is 0.25 and standard deviation 0.5. The pixel observation variance is instead 0.25²=0.0625. These variances belong to different spaces: encoded variance depends on the input, while observation variance is fixed here. The prior starts generation; q uses an observed image to approximate inference in the reverse direction.

The generative model also specifies a prior: before observing an image, sample the latent coordinates from a standard normal distribution. The decoder then supplies a conditional image distribution. Our observation model is Gaussian with fixed standard deviation 0.25, and the network outputs 64 conditional pixel means. The encoder approximates the question “which latent coordinates are plausible after seeing this image?” The decoder answers “how are images distributed given these coordinates?” These are the inference and generation directions. We call the encoded distribution q because it approximates the true posterior p. Evaluating q is fast; exactly computing the posterior usually requires an intractable integral.

The figures display decoder means. A full draw from the observation model would additionally place independent Gaussian pixel noise of standard deviation 0.25 around those means. That Gaussian permits intensities outside zero to one, and clipping such draws for display would change the displayed distribution. We use mean images to inspect learned stroke structure while retaining the stated Gaussian in probability calculations. Binary images can use Bernoulli observations, and continuous color data can use other suitable distribution families. A network output that resembles an image may represent a sample, a mean, or a distribution parameter. Those interpretations lead to different calculations.

## How a random sample carries a gradient

Training draws a latent vector from the encoded distribution and sends it through the decoder. Simply instructing a random-number generator to sample from changing means and variances does not yet describe a differentiable path from the sample back to those parameters. Reparameterization places randomness in a fixed standard distribution. Draw standard normal noise, then shift and scale it using the encoder’s mean and standard deviation. For that particular noise realization, the remaining operations are ordinary differentiable arithmetic. The sample has the desired distribution, and its dependence on the network parameters is explicit.

$$
\epsilon\sim\mathcal N(0,I),\quad z=\mu+e^{\ell/2}\odot\epsilon,\qquad \frac{\partial z_j}{\partial\mu_j}=1,\quad \frac{\partial z_j}{\partial\ell_j}=\frac12e^{\ell_j/2}\epsilon_j
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bc4dcdd816066dd3105937e5.svg) | Standard normal noise, encoded mean, log variance, and sampled latent, with matching shapes and dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/a13c037afb4db6c1b0350d96.svg) | Elementwise multiplication and latent-coordinate index. |
| ![Formula](https://ml-biomat.com/static/agent-math/006e9cdbaf8f19396a4bac5d.svg) | Local partial derivative holding this noise realization fixed; other coordinates have no direct effect. |

With μ=0.5, ℓ=ln0.25, and ε=−0.4, z=0.5+0.5(−0.4)=0.3. Its derivatives are one with respect to μ and −0.1 with respect to ℓ. The code checks these in float64. Noise enters through ε, while differentiable shifting and scaling carry dependence back to the encoder.

For mean 0.5, standard deviation 0.5, and sampled noise −0.4, the latent coordinate is 0.3. Holding this noise fixed, increasing the mean by 0.01 increases the coordinate by 0.01. Increasing the standard deviation by 0.01 decreases it by 0.004. The network actually outputs log variance. Exponentiation keeps the variance positive while allowing the unconstrained network output to take any real value. With that parameterization, the derivative of this coordinate with respect to log variance is −0.1. We derive the number by hand and confirm it with autograd, making the gradient through a stochastic construction tangible.

Different random draws produce different gradient estimates, and training averages their information across examples and updates. Each training image uses one latent sample per update. Validation uses eight fixed noise realizations per image to reduce additional sampling variation during model selection. Test statistics use 32 independent realizations to estimate sampled reconstruction error. Sending the encoded mean directly through the decoder provides a stable reconstruction picture, but differs from averaging decoded samples across the encoded distribution. A nonlinear decoder generally makes “decode the average” and “average the decodings” different operations.

## Reconstruction and KL: why keep two accounts?

A reconstruction-only objective can place different images in distant, extremely narrow latent regions, allowing the decoder to specialize to each region. Random prior draws may then land in poorly trained gaps. VAE training addresses two requirements together: latent samples inferred from an input should explain it, and their encoded distribution should remain connected to the specified prior. KL divergence measures the second requirement. It compares distributions rather than means alone. Two Gaussians with matching centers but different widths still have positive KL divergence.

$$
D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))=\frac12\sum_{j=1}^d\left(\mu_j^2+e^{\ell_j}-1-\ell_j\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d030412d4e039867037a4f93.svg) | KL divergence from q to p, nonnegative and measured in nats with natural logarithms; direction matters. |
| ![Formula](https://ml-biomat.com/static/agent-math/f45e9410864d7d0b4efbf507.svg) | Encoded mean, log variance, and variance in coordinate j; dimensionless latent coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/002d92ae8202f23d5abc8977.svg) | Latent dimension, summation index, and standard normal prior; the formula assumes this prior and a diagonal Gaussian q. |

For one-dimensional μ=0.5 and variance 0.25, KL=0.5(0.25+0.25−1−ln0.25)≈0.443147. Mean zero and variance one contribute zero. Taking the expectation under q of the Gaussian log-density ratio yields this analytic form. Expected squared coordinates contain both squared means and variances, explaining why penalizing means alone would be incomplete.

Combining these terms follows a probabilistic derivation. Factor the joint distribution into a prior and a conditional image distribution, then introduce the encoder distribution. The log evidence separates into a computable lower bound and a nonnegative gap involving the true posterior. This lower bound is the ELBO. Increasing it balances how well latent samples explain the image with the distributional cost of the inference model. As the encoded distribution approaches the posterior, the gap between the ELBO and log evidence shrinks. “Variational” refers to approximating a difficult posterior with a tractable family of distributions.

$$
\log p_\theta(x)=\mathcal L(x)+D_{\mathrm{KL}}(q_\phi(z\mid x)\|p_\theta(z\mid x)),\quad \mathcal L(x)=\mathbb E_q[\log p_\theta(x\mid z)]-D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e74e6aa040ce200228f3796.svg) | Marginal image density and true latent posterior; the former integrates out the latent. |
| ![Formula](https://ml-biomat.com/static/agent-math/7ab77ec4103bb054ed229d53.svg) | Single-image evidence lower bound and expectation over latent draws from q. |
| ![Formula](https://ml-biomat.com/static/agent-math/78b2e3cdb94abade6dd35efa.svg) | KL divergence, natural logarithm, generative parameters, and encoder parameters; logarithmic terms measured in nats. |

Take the q expectation of log p(x,z) minus log q(z|x). Factoring the joint as p(z|x)p(x) gives the identity; factoring it as p(x|z)p(z) gives the ELBO expression. Nonnegative posterior KL makes the ELBO a lower bound. If log p(x)=−10 and posterior KL=0.4, the ELBO is −10.4. This posterior gap differs from the tractable q-to-prior KL used in training.

For a Gaussian observation model with fixed variance, negative log likelihood is a scaled squared error plus a constant. This gives the reconstruction term a specific origin. The code sums squared errors across 64 pixels, divides by twice the observation variance, and adds the per-image KL. The Gaussian constant can be omitted during optimization because it does not depend on trainable parameters; it is restored when reporting negative ELBO. Continuous probability densities can exceed one, so negative log densities can be negative. The β=1 test negative ELBO of about −5.780 nats per image is therefore consistent with this model. Changing intensity units or the observation distribution changes the quantity being compared.

$$
-\log p_\theta(x\mid z)=\frac{\|x-g_\theta(z)\|^2}{2\sigma_x^2}+\frac D2\log(2\pi\sigma_x^2)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e0f43653f7f49b1558e89534.svg) | Observed image and decoder mean, D=64 dimensionless pixels. |
| ![Formula](https://ml-biomat.com/static/agent-math/2900fc90c210213243c6ecbf.svg) | Fixed observation standard deviation and pixel count; this is not latent standard deviation. |
| ![Formula](https://ml-biomat.com/static/agent-math/35d95492a0d8700f5a67bf76.svg) | Sum of squared residuals over pixels, pi, and natural logarithm. |

For per-pixel MSE 0.04, total squared error is 64×0.04=2.56. Dividing by 2×0.25² gives 20.48. The Gaussian constant is about −29.91077 nats, giving conditional negative log density about −9.43077 nats. Average over encoded samples and add KL to obtain negative ELBO; mean-code reconstruction MSE does not replace that expectation.

## Control information capacity and add a condition

A β-VAE multiplies the KL term by a weight, allowing us to study an information–reconstruction tradeoff. As β increases from 0.2 to one to four in our experiment, mean KL falls from 6.433 to 3.763 to 1.857 nats per image. Sampled reconstruction MSE rises from 0.03727 to 0.03978 to 0.04818. The plot places departure from the prior on one axis and lost pixel precision on the other, using measurements from actual training. β=1 gives the standard ELBO derived above. Other values define weighted objectives, so their training-loss values are not interchangeable measurements of the same evidence bound.

![Left: mean KL and sampled reconstruction MSE for three β values, using 32 latent draws for each of 360 test images. Right: ordinary and denoising AEs with the same 8D bottleneck, reading clean or fixed noisy inputs and targeting clean images. All measurements use the same split.](https://ml-biomat.com/static/tutorials/machine-learning/figures/49de82f12d81215c9d2425bf.svg?v=49de82f12d81)

Figure 3Left: mean KL and sampled reconstruction MSE for three β values, using 32 latent draws for each of 360 test images. Right: ordinary and denoising AEs with the same 8D bottleneck, reading clean or fixed noisy inputs and targeting clean images. All measurements use the same split.

Very small KL can accompany posterior collapse: many inputs receive distributions close to the prior, and the decoder draws little useful information from the latent variable. A strong alternative conditioning pathway can make bypassing the latent especially easy. Diagnostics include per-coordinate KL, variation of means across inputs, changes in output when the latent changes, and the effect of shuffling latents between inputs. Our β=4 model retains about 1.857 nats of mean KL and mean-coordinate variances near 0.82 and 0.83. Blur alone therefore does not establish complete collapse. Increasing the KL weight gradually, adjusting decoder capacity, or targeting information capacity can change the optimization path.

A conditional VAE provides a known requirement to both networks. We represent the digit category with a ten-dimensional one-hot vector. The encoder reads the image together with the category, and the decoder reads the latent together with the category. The condition can specify the digit, leaving latent variables to describe stroke style and other within-class variation. Each figure column fixes a category; each row uses the same latent coordinates. Horizontal comparisons reveal condition effects, while vertical comparisons reveal latent effects. The 2015 work on deep conditional generative models developed this approach for structured outputs. Text, attributes, or known observations can also act as conditions when their availability is specified during both training and generation.

$$
J_\beta(x,c)=\mathbb E_{q_\phi(z\mid x,c)}[-\log p_\theta(x\mid z,c)]+\beta D_{\mathrm{KL}}(q_\phi(z\mid x,c)\|p(z))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43372e0cb627109b8d74aa73.svg) | Image, known condition, and latent variable; c is a ten-dimensional one-hot category and z is two-dimensional. |
| ![Formula](https://ml-biomat.com/static/agent-math/d98f95086ed3b254f57f2ade.svg) | Conditional encoder, conditional decoder, and standard normal prior; the prior is independent of c here. |
| ![Formula](https://ml-biomat.com/static/agent-math/c56eaa2a890eaf09a14e9f38.svg) | KL weight, weighted per-image objective, and latent expectation; β is dimensionless and the objective uses nats. |

Removing c gives the unconditional β-VAE objective. Expected reconstruction negative log density −9.4 and KL 3.8 give objective −5.6 at β=1 and 5.8 at β=4. Changing β changes the tradeoff. For a condition specifying digit three, the encoder receives 64+10 coordinates and the decoder receives 2+10. Training and sampling both provide a category, with z controlling within-category variation.

![Top: conditional VAE with a fixed category in each column and z=(−1,0),(0,0),(1,0) across rows. Bottom: all 60 standard-normal prior draws for the unconditional β=1 VAE, seed 339, in generated order. Images show decoder means without observation noise.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ca683cb8fabfc02c2532446a.svg?v=ca683cb8fabf)

Figure 4Top: conditional VAE with a fixed category in each column and z=(−1,0),(0,0),(1,0) across rows. Bottom: all 60 standard-normal prior draws for the unconditional β=1 VAE, seed 339, in generated order. Images show decoder means without observation noise.

Additional conditioning changes the task. Our conditional model has mean-code reconstruction MSE of 0.02575 compared with 0.03809 for the unconditional VAE. The conditional model already knows the true category, so two latent coordinates need not communicate all image information. Generation must also supply that category, whereas unconditional generation begins with a prior draw alone. Listing these inputs explains the source of the difference more clearly than comparing one error number. A one-hot condition is a computational control; it does not automatically turn each latent coordinate into an independently interpretable style factor. Such interpretation requires further definitions, data, or evaluation.

## Walk through latent space and inspect what was learned

A deterministic AE may organize its two-dimensional codes into curved or dispersed regions. A VAE connects encoded distributions to a standard normal prior through its KL term. The scatterplot shows encoded means; dashed circles indicate prior coordinate scales. A radius-one disk in a two-dimensional standard normal does not contain the same probability as the familiar one-standard-deviation interval in one dimension, because two coordinates vary together. The atlas decodes a regular grid, revealing how outputs change continuously with coordinates. Some neighboring positions trace smooth stroke changes, while others show ambiguous average shapes. Both are features of the model’s actual learned space.

![Left: AE codes and VAE means for 360 test images; colors are true digits used only for visualization. Dashed VAE circles have radii one and two. Right: 121 decoder means on a grid from −2.5 to 2.5 in both coordinates, spacing 0.5. The scatterplots use their own coordinate ranges; AE and VAE values are not identified with one another.](https://ml-biomat.com/static/tutorials/machine-learning/figures/aa005c84cc85ad73f762d950.svg?v=aa005c84cc85)

Figure 5Left: AE codes and VAE means for 360 test images; colors are true digits used only for visualization. Dashed VAE circles have radii one and two. Right: 121 decoder means on a grid from −2.5 to 2.5 in both coordinates, spacing 0.5. The scatterplots use their own coordinate ranges; AE and VAE values are not identified with one another.

## Move a coordinate and run the trained decoder

Pale points show encoder means for a subset of training images; circles mark radii one and two. Drag the black point or move coordinate sliders to compute 64 pixel means from the β=1 model. Click a pixel to inspect its value. Prior sampling uses a fixed random sequence for reproducibility. The plane and slider ranges expand together when a draw falls outside the current coordinates.

[Figure: Trained VAE latent space and decoded pixels](https://ml-biomat.com/tutorials/machine-learning/m33/en/#M33-board)

The image displays conditional means without added observation noise. A two-dimensional standard normal places about 39.3% and 86.5% of its mass inside radii one and two. Latent coordinates and pixel intensities are dimensionless.

Linear interpolation between two codes inspects local continuity. Sampling from the prior examines a generative distribution. These procedures choose points differently. In high-dimensional standard normal spaces, much of the probability mass lies near a characteristic radius, while the midpoint of a straight interpolation may sit closer to the center. Evaluation therefore benefits from several measurements: appearance, repetition, category or structural coverage, similarity to training examples, and the probabilistic objective. The contact sheet shows all 60 fixed-seed prior-draw means rather than selecting attractive examples. It exposes variation and blur, while numerical coverage would require a separately defined annotation or classifier-based assessment.

The interaction loads the decoder parameters trained here with β=1. Moving a point executes its 2→64→64 network in the browser and updates an eight-by-eight image; it does not switch among stored pictures. At coordinates (0,0), the sum of the 64 output intensities is approximately 20.30716, matching the Python decoder. Selecting a pixel displays its predicted mean. The interaction operates on the mean function of a trained probabilistic model, connecting the latent-variable equations, executable code, and visible image in one calculation.

## The complete experiment: separate reconstruction from generation

The program uses 1,797 public handwriting images. Seeds 330 and 331 produce a stratified split of 1,077 training, 360 validation, and 360 test images. Seven models train for 100 epochs each: two- and eight-dimensional AEs, an eight-dimensional denoising AE, three two-dimensional β-VAEs, and a conditional two-dimensional VAE. Each retains the checkpoint with its best validation objective. Denoising validation uses fixed corrupted images, while VAE validation uses eight fixed latent-noise draws and test evaluation uses another 32. Every comparison is traceable to the same data partition while retaining the objective each method actually optimizes.

### Complete Python: seven models and a trained latent space

Run python main.py --output results --language en with NumPy, Matplotlib, scikit-learn, and PyTorch. The bundled sklearn data require no separate download. All seven models train and produce four SVG figures, summary.json, experiment.npz, decoder JSON, and weights. Observation standard deviation is 0.25; mean-code MSE, sampled MSE, KL, and negative ELBO are recorded separately.

```
"""Actual AE, denoising AE, beta-VAE, and conditional VAE on bundled digits."""
from pathlib import Path
import argparse,copy,json,platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
d=load_digits();x=(d.data/16).astype('float32');y=d.target
train,other=train_test_split(np.arange(len(y)),test_size=720,random_state=330,stratify=y)
val,test=train_test_split(other,test_size=360,random_state=331,stratify=y[other])
xt,xv,xe=[torch.tensor(x[i]) for i in [train,val,test]];yt,yv,ye=[torch.tensor(y[i]) for i in [train,val,test]]
class AE(nn.Module):
 def __init__(self,latent):
  super().__init__();self.encoder=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,latent));self.decoder=nn.Sequential(nn.Linear(latent,64),nn.ReLU(),nn.Linear(64,64),nn.Sigmoid())
 def forward(self,x):return self.decoder(self.encoder(x))
class VAE(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;c=10 if conditional else 0
  self.encoder=nn.Sequential(nn.Linear(64+c,64),nn.ReLU());self.mu=nn.Linear(64,2);self.logvar=nn.Linear(64,2)
  self.decoder=nn.Sequential(nn.Linear(2+c,64),nn.ReLU(),nn.Linear(64,64),nn.Sigmoid())
 def condition(self,v,y):return torch.cat([v,F.one_hot(y,10).float()],1) if self.conditional else v
 def encode(self,x,y):
  h=self.encoder(self.condition(x,y));return self.mu(h),self.logvar(h)
 def decode(self,z,y):return self.decoder(self.condition(z,y))
 def forward(self,x,y,eps):
  mu,lv=self.encode(x,y);z=mu+torch.exp(.5*lv)*eps;return self.decode(z,y),mu,lv
def kl(mu,lv):return .5*(mu.square()+lv.exp()-1-lv).sum(1)
sigma=.25;models={};histories={};metrics={}
noisegen=torch.Generator().manual_seed(332)
noisy_test=(xe+.25*torch.randn(xe.shape,generator=noisegen)).clamp(0,1)
fixed_val_noise=(xv+.25*torch.randn(xv.shape,generator=noisegen)).clamp(0,1)
for name,latent,denoise in [('ae2',2,False),('ae8',8,False),('denoise8',8,True)]:
 torch.manual_seed(333);model=AE(latent);opt=torch.optim.Adam(model.parameters(),lr=.003);gen=torch.Generator().manual_seed(334);best=1e9;history=[]
 for epoch in range(100):
  model.train()
  for ids in torch.randperm(len(xt),generator=gen).split(64):
   inp=xt[ids]
   if denoise:inp=(inp+.25*torch.randn(inp.shape,generator=gen)).clamp(0,1)
   loss=F.mse_loss(model(inp),xt[ids]);opt.zero_grad();loss.backward();opt.step()
  model.eval()
  with torch.no_grad():vl=F.mse_loss(model(fixed_val_noise if denoise else xv),xv).item()
  history.append(vl)
  if vl<best:best=vl;beststate=copy.deepcopy(model.state_dict());bestepoch=epoch+1
 model.load_state_dict(beststate);models[name]=model;histories[name]=history
 with torch.no_grad():metrics[name]=dict(clean_mse=F.mse_loss(model(xe),xe).item(),noisy_mse=F.mse_loss(model(noisy_test),xe).item(),best_epoch=bestepoch,parameters=sum(p.numel() for p in model.parameters()))
for name,beta,condition in [('vae02',.2,False),('vae1',1.,False),('vae4',4.,False),('conditional',1.,True)]:
 torch.manual_seed(335);model=VAE(condition);opt=torch.optim.Adam(model.parameters(),lr=.003);gen=torch.Generator().manual_seed(336);history=[];best=1e9
 vg=torch.Generator().manual_seed(337);valeps=torch.randn((8,len(xv),2),generator=vg)
 for epoch in range(100):
  model.train()
  for ids in torch.randperm(len(xt),generator=gen).split(64):
   recon,mu,lv=model(xt[ids],yt[ids],torch.randn((len(ids),2),generator=gen))
   distortion=(recon-xt[ids]).square().sum(1)/(2*sigma*sigma)
   loss=(distortion+beta*kl(mu,lv)).mean();opt.zero_grad();loss.backward();opt.step()
  model.eval()
  with torch.no_grad():
   mu,lv=model.encode(xv,yv);pred=torch.stack([model.decode(mu+(.5*lv).exp()*eps,yv) for eps in valeps]);dist=(pred-xv).square().sum(2).mean(0)/(2*sigma*sigma);vl=(dist+beta*kl(mu,lv)).mean().item()
  history.append(vl)
  if vl<best:best=vl;beststate=copy.deepcopy(model.state_dict());bestepoch=epoch+1
 model.load_state_dict(beststate);models[name]=model;histories[name]=history
 with torch.no_grad():
  mu,lv=model.encode(xe,ye);meanrec=model.decode(mu,ye)
  eg=torch.Generator().manual_seed(338);eps=torch.randn((32,len(xe),2),generator=eg)
  pred=torch.stack([model.decode(mu+(.5*lv).exp()*e,ye) for e in eps]);expectedmse=(pred-xe).square().mean().item();k=kl(mu,lv).mean().item()
  constant=64*.5*np.log(2*np.pi*sigma*sigma)
  metrics[name]=dict(beta=beta,mean_reconstruction_mse=F.mse_loss(meanrec,xe).item(),sampled_reconstruction_mse=expectedmse,kl_nats=k,negative_elbo_nats=expectedmse*64/(2*sigma*sigma)+constant+k,mu_variance=mu.var(0,unbiased=False).tolist(),best_epoch=bestepoch,parameters=sum(p.numel() for p in model.parameters()))
for name,model in models.items():torch.save(model.state_dict(),out/f'{name}.pt')
chosen=np.array([np.flatnonzero(y[test]==k)[0] for k in range(10)])
with torch.no_grad():
 mu,lv=models['vae1'].encode(xe,ye);vae_rec=models['vae1'].decode(mu,ye)
 rows=[xe[chosen],models['ae2'](xe[chosen]),models['ae8'](xe[chosen]),vae_rec[chosen],noisy_test[chosen],models['denoise8'](noisy_test[chosen])]
fig,axs=plt.subplots(6,10,figsize=(13,8.6),gridspec_kw={'wspace':.04,'hspace':.2})
labels=tr(['原图','AE：2维','AE：8维','VAE：均值重建','含噪输入','去噪AE：8维'],['Original','AE: 2D','AE: 8D','VAE: mean code','Noisy input','Denoising AE: 8D'])
for r,row in enumerate(rows):
 for c,img in enumerate(row):
  axs[r,c].imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);axs[r,c].set_xticks([]);axs[r,c].set_yticks([])
  if r==0:axs[r,c].set_title(str(c))
 axs[r,0].set_ylabel(labels[r],fontsize=10)
fig.suptitle(tr('同一测试图：容量、随机潜变量与去噪目标','The same test images: capacity, stochastic codes, and denoising'),y=.97);save(fig,'reconstruction')
with torch.no_grad():
 az=models['ae2'].encoder(xe).numpy();vz=mu.numpy();vg=np.linspace(-2.5,2.5,11)
 grid=np.array([[a,b] for b in vg[::-1] for a in vg],dtype='float32');decoded=models['vae1'].decode(torch.tensor(grid),torch.zeros(len(grid),dtype=torch.long)).numpy()
mosaic=np.zeros((88,88))
for i,img in enumerate(decoded):mosaic[(i//11)*8:(i//11+1)*8,(i%11)*8:(i%11+1)*8]=img.reshape(8,8)
fig=plt.figure(figsize=(13,7));gs=fig.add_gridspec(2,2,width_ratios=[1,1.2],hspace=.5,wspace=.32)
for i,(arr,title) in enumerate([(az,tr('A  AE 的确定性坐标','A  Deterministic AE coordinates')),(vz,tr('B  VAE 的编码均值','B  VAE encoder means'))]):
 ax=fig.add_subplot(gs[i,0]);sc=ax.scatter(arr[:,0],arr[:,1],c=y[test],cmap='tab10',s=9,alpha=.7);ax.set(xlabel=r'$z_1$' if i==0 else r'$\mu_1$',ylabel=r'$z_2$' if i==0 else r'$\mu_2$',title=title)
 fig.colorbar(sc,ax=ax,ticks=range(10),fraction=.04,pad=.03,label=tr('数字','Digit'))
 if i==1:
  ax.set_aspect('equal',adjustable='box')
  for radius in [1,2]:ax.add_patch(plt.Circle((0,0),radius,fill=False,color='#6c767c',ls='--',lw=.8))
ax=fig.add_subplot(gs[:,1]);ax.imshow(mosaic,cmap='gray_r',vmin=0,vmax=1,extent=[-2.75,2.75,-2.75,2.75]);ax.set(xlabel=r'$z_1$',ylabel=r'$z_2$',title=tr('C  β=1：解码均值图册，网格间距 0.5','C  β=1 decoder-mean atlas; grid spacing 0.5'));save(fig,'latent')
fig,(ax,bar)=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
colors=['#125f82','#b85d30','#658248']
for name,color in zip(['vae02','vae1','vae4'],colors):
 m=metrics[name];ax.scatter(m['kl_nats'],m['sampled_reconstruction_mse'],s=110,color=color);ax.annotate('β='+str(m['beta']),(m['kl_nats'],m['sampled_reconstruction_mse']),xytext=(8,7),textcoords='offset points',fontsize=11)
ax.set(xlabel=tr('平均 KL / nats 每图','Mean KL / nats per image'),ylabel=tr('采样重建均方误差 / 像素','Sampled reconstruction MSE / pixel'),title=tr('A  信息约束与重建的实际取舍','A  Measured information–distortion tradeoff'));ax.margins(.25)
names=['ae8','denoise8'];xx=np.arange(2);bar.bar(xx-.17,[metrics[n]['clean_mse'] for n in names],.34,color='#125f82',label=tr('干净输入','Clean input'));bar.bar(xx+.17,[metrics[n]['noisy_mse'] for n in names],.34,color='#b85d30',label=tr('含噪输入','Noisy input'));bar.set_xticks(xx,[tr('普通 AE','Ordinary AE'),tr('去噪 AE','Denoising AE')]);bar.set(ylabel=tr('对干净图的均方误差 / 像素','MSE against clean images / pixel'),title=tr('B  相同8维瓶颈，不同训练目标','B  Same 8D bottleneck, different objectives'));bar.legend();save(fig,'tradeoff')
gen=torch.Generator().manual_seed(339);prior=torch.randn((60,2),generator=gen)
with torch.no_grad():
 samples=models['vae1'].decode(prior,torch.zeros(60,dtype=torch.long)).numpy()
 positions=torch.tensor([[-1.,0.],[0.,0.],[1.,0.]])
 cond=np.stack([models['conditional'].decode(positions,torch.full((3,),k)).numpy() for k in range(10)])
fig=plt.figure(figsize=(13,8));gs=fig.add_gridspec(2,1,height_ratios=[1,1.2],hspace=.32)
top=gs[0].subgridspec(3,10,wspace=.03,hspace=.06)
for k in range(10):
 for j in range(3):
  ax=fig.add_subplot(top[j,k]);ax.imshow(cond[k,j].reshape(8,8),cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
  if j==0:ax.set_title('c='+str(k))
  if k==0:ax.set_ylabel(f'z1={j-1}, z2=0',fontsize=9)
bottom=gs[1].subgridspec(5,12,wspace=.03,hspace=.06)
for i,img in enumerate(samples):
 ax=fig.add_subplot(bottom[i//12,i%12]);ax.imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('无条件先验抽样','Unconditional prior draws'),loc='left',fontsize=11)
fig.suptitle(tr('条件控制与随机变化：显示解码分布均值','Conditional control and random variation: decoder means'),y=.98);save(fig,'generation')
with torch.no_grad():
 means=models['vae1'].encode(xt,yt)[0].numpy()
 probes={str(pair):models['vae1'].decode(torch.tensor([pair],dtype=torch.float32),torch.tensor([0]))[0].tolist() for pair in [[0,0],[1,-1],[-2,2]]}
weights={k:v.detach().numpy().tolist() for k,v in models['vae1'].decoder.state_dict().items()}
(out/'decoder.json').write_text(json.dumps(dict(weights=weights,means=means[::7].tolist(),labels=y[train][::7].tolist(),probes=probes)),encoding='utf-8')
mu_hand=torch.tensor([.5],dtype=torch.float64,requires_grad=True);lv_hand=torch.tensor([np.log(.25)],dtype=torch.float64,requires_grad=True);eps_hand=torch.tensor([-.4],dtype=torch.float64);z_hand=mu_hand+(.5*lv_hand).exp()*eps_hand
grad_mu,grad_lv=torch.autograd.grad(z_hand.sum(),[mu_hand,lv_hand]);kl_hand=kl(mu_hand.reshape(1,1),lv_hand.reshape(1,1)).item()
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),splits=dict(train=len(train),validation=len(val),test=len(test)),seed=330,epochs=100,sigma=sigma,metrics=metrics,
 hand=dict(z=z_hand.item(),dz_dmu=grad_mu.item(),dz_dlogvar=grad_lv.item(),kl=kl_hand,normal_constant_per_image=float(64*.5*np.log(2*np.pi*sigma*sigma))),
 decoder_checks={str(k):dict(sum=float(np.sum(v)),pixel0=v[0]) for k,v in probes.items()})
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train_indices=train,val_indices=val,test_indices=test,chosen_test_indices=chosen,reconstruction=np.stack([r.numpy() for r in rows]),ae_latents=az,vae_means=vz,grid=grid,decoded=decoded,prior=prior.numpy(),samples=samples,conditional=cond,**{n+'_history':h for n,h in histories.items()})
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

Outputs include contact sheets, latent coordinates, prior draws, conditional outputs, learning histories, and model weights. Start by calculating one Gaussian KL, check one reparameterization derivative, then inspect how these mechanisms shape the images. Further experiments can change one factor at a time: latent dimension, observation noise, β, or condition information. Record reconstruction, sampling, and representation changes separately. A more accurate reconstruction, a more regular latent distribution, and a more varied sample collection are connected goals with different definitions. Keeping those definitions explicit makes the uses of autoencoders and VAEs concrete.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M33.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Auto-Encoding Variational Bayes](https://arxiv.org/html/1312.6114v11)

   Sections 2.2–2.4 on ELBO/reparameterization; Appendix B Gaussian KL and Appendix C Gaussian decoding.

   Primary paper; no figure copied
2. [UvA Tutorial 9: Deep Autoencoders](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial9/AE_CIFAR10.html)

   Bottlenecks and original latent-dimensionality figure.

   MIT; copyright 2020 Phillip Lippe; license included
3. [PyTorch examples: VAE](https://github.com/pytorch/examples/tree/main/vae)

   Official mean/log-variance, sampling, and KL implementation; our example uses Gaussian observations.

   BSD-3-Clause code; independent teaching implementation
4. [Understanding disentangling in beta-VAE](https://arxiv.org/abs/1804.03599)

   Information capacity and reconstruction tradeoffs.

   Primary paper; no figure copied
5. [Learning Structured Output Representation using Deep Conditional Generative Models](https://proceedings.neurips.cc/paper/2015/hash/8d55a249e6baa5c06772297520da2051-Abstract.html)

   Conditional latent-variable models and structured output.

   Primary paper; no figure copied
6. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   Image-data definition.

   CC BY 4.0; E. Alpaydin and C. Kaynak
