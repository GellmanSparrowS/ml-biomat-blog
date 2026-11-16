# Teaching a generator a distribution: GAN, DCGAN, and WGAN

Source: https://ml-biomat.com/tutorials/machine-learning/m18/en/
Language: en

Follow adversarial training across eight clusters, then examine convolutional images, conditioning, and complementary evaluation measures.

## How can a model learn to draw without one exact answer?

Ask a model to sharpen a blurred photograph and the task quickly exceeds pixelwise comparison. Hair can contain many plausible arrangements of fine strands, and a patch of grass can have many reasonable textures. Averaging all possible answers often produces a smooth image with little realistic detail. A generative model learns to produce a collection of plausible outcomes, rather than only an average answer for a given input. A GAN supplies a particular learning signal: another network repeatedly compares real and generated samples, then sends the differences it detects back to the generator.

Imagine two people practicing pottery. One makes cups, while the other studies finished examples and points out structures that look unusual. The maker need not receive a unique correct coordinate for every point on every cup, but needs useful feedback about proportions and local detail. A GAN passes this feedback through differentiable computation, and its discriminator changes as the generated samples change. Training becomes an interaction between two adapting networks. Texture synthesis, image translation, and distribution modeling can use this mechanism, with each application specifying which details may vary freely and which content must be preserved.

Goodfellow and colleagues introduced adversarial training of a generator and discriminator in 2014. DCGAN brought convolutional structure into image generation in 2015, while WGAN and gradient-penalty methods revisited distribution distances and training signals in 2017. We first inspect these ideas in a two-dimensional plane, then generate actual handwriting images. The GAN Lab storyboard below preserves six moments from the original project animation. Green target samples form a ring; purple generated samples change during training. Movement and coverage reveal aspects of learning that a single loss curve cannot show.

![Six-frame storyboard from the GAN Lab animation, original frame indices 0,46,92,138,184,231. Green points are real ring samples and purple points generated samples. Authors: Minsuk Kahng, Nikhil Thorat, Duen Horng Chau, Fernanda B. Viégas, Martin Wattenberg; Apache 2.0. Adaptation only extracts and arranges frames; these are not our eight-cluster measurements.](https://ml-biomat.com/static/tutorials/machine-learning/figures/52acca42d21e06223efc6fe8.png?v=52acca42d21e)

Figure 1Six-frame storyboard from the GAN Lab animation, original frame indices 0,46,92,138,184,231. Green points are real ring samples and purple points generated samples. Authors: Minsuk Kahng, Nikhil Thorat, Duen Horng Chau, Fernanda B. Viégas, Martin Wattenberg; Apache 2.0. Adaptation only extracts and arranges frames; these are not our eight-cluster measurements.

## The generator supplies samples; the discriminator supplies feedback

A generator reads simple random numbers, such as two standard-normal coordinates, and outputs a point. An image generator instead maps a short random vector to a full image. These random inputs are latent variables, providing a source of output variation. The discriminator reads a sample and predicts the probability that it came from real data. During discriminator training, real examples have target one and current generated examples have target zero. During generator training, generated examples should receive higher realness probabilities. There is no prescribed target location paired with each random input; the collection of generated samples is constrained through distributional feedback.

$$
\min_\theta\max_\psi V=\mathbb E_{x\sim p_{\mathrm{data}}}[\log D_\psi(x)]+\mathbb E_{z\sim p_z}[\log(1-D_\psi(G_\theta(z)))]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eb1908cc8450efe542f213a3.svg) | Real sample, latent random vector, and generated sample; x and z are both two-dimensional in the point task, with dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f979d55af01ef145a0c149e.svg) | Generator parameterized by θ and discriminator parameterized by ψ; D returns a realness probability between zero and one. |
| ![Formula](https://ml-biomat.com/static/agent-math/39104b8057611a12e33da53c.svg) | Target data distribution, standard-normal latent distribution, and expectation under the indicated distribution. |
| ![Formula](https://ml-biomat.com/static/agent-math/7786a72523421eab514da2ff.svg) | Adversarial value, natural logarithm, generator minimization and discriminator maximization; logarithmic terms use nats. |

The discriminator maximizes logD for real examples and log(1−D) for generated examples, equivalently minimizing their negative logs. D(real)=0.8 and D(fake)=0.2 give discriminator loss −2ln0.8≈0.446287. Generator minimization pushes D(fake) upward. Our code retains this discriminator objective and uses the non-saturating generator objective below.

If the discriminator assigns probability 0.8 to a real point and 0.2 to a generated point, its loss for the pair is approximately 0.4463. Returning 0.5 for both gives approximately 1.3863. Interpretation depends on training progress. A probability of one half can reflect similar distributions, or a discriminator that has not learned a useful distinction. In the idealized matched-distribution setting, the optimal discriminator cannot distinguish the two sources. In an experiment, generated samples, coverage, and independent distances help establish what a fifty-percent discriminator actually means.

Our target distribution contains eight small clusters centered uniformly around a circle of radius two. Independent Gaussian noise with standard deviation 0.08 is added to each coordinate. Compared with a continuous ring, this creates a distinct mass-allocation problem: generated points must reach appropriate locations and distribute themselves across all eight modes. The two-dimensional generator uses two hidden layers of 64 units and a smooth final transformation bounding its output between −3 and three. Every displayed generated coordinate comes from a trained network. Training and test target points use different seeds, with the test points reserved for observing results.

## Alternating updates create two gradient paths

During a discriminator update, generated examples temporarily act as fixed inputs. The code detaches them from the generator’s computation graph, preventing that update from changing generator parameters. It then improves the discriminator’s real-versus-generated classification. During a generator update, discriminator parameters remain fixed, but derivatives of its score with respect to its input must remain available. The generator receives a direction for changing samples and propagates that direction back to its parameters. Putting the entire discriminator computation inside a no-gradient context at this stage would also remove the needed learning signal. Freezing parameters and cutting input gradients are different operations.

The original minimax objective can give the generator a small gradient when the discriminator is very confident. For a generated sample with realness probability 0.01, the saturating objective has gradient magnitude approximately 0.01 with respect to the discriminator logit. The commonly used non-saturating objective gives magnitude approximately 0.99. Both encourage a higher realness score, but their early optimization signals differ greatly. We use the non-saturating loss. The discriminator returns logits, and stable softplus operations calculate losses without separately forming an extremely small probability and then taking its logarithm.

$$
L_G^{\mathrm{sat}}=\log(1-\sigma(a)),\quad L_G^{\mathrm{NS}}=-\log\sigma(a),\qquad \frac{\partial L_G^{\mathrm{sat}}}{\partial a}=-\sigma(a),\quad\frac{\partial L_G^{\mathrm{NS}}}{\partial a}=\sigma(a)-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bc1be4a7792db09d517828f5.svg) | Discriminator logit for one generated sample and its sigmoid probability, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d90457f08ec556210aaeda7c.svg) | Saturating and non-saturating per-sample generator losses; the former is nonpositive, the latter nonnegative, in nats. |
| ![Formula](https://ml-biomat.com/static/agent-math/96b9ee67af2db0b7893154ee.svg) | Derivative with respect to the logit; full parameter gradients also include the discriminator input derivative and generator derivative. |

Set a=ln(0.01/0.99), giving sigmoid(a)=0.01. The two derivatives are −0.01 and −0.99. Gradient descent increases a in both cases, with stronger local pressure from the latter. Non-saturating loss is computed stably as softplus(−a). Full-network gradients also depend on the remaining chain-rule factors.

Alternation also explains why one loss curve is an incomplete description. When the discriminator discovers a useful new clue, generator loss may rise. When the generator removes that clue, the discriminator must find another. Learning rates, the number of updates allocated to each network, and model capacity determine how the two participants follow one another. The figure holds latent inputs fixed while showing their outputs at several training stages. This distinguishes a randomly refreshed picture from an actual change in what the updated network produces for the same inputs.

![Outputs for the same 128 latent inputs after 0,300,750,and 1,500 generator updates. Orange shows a fixed subset of independent target points and blue shows generated points. Rows compare GAN and WGAN-GP with matching coordinate ranges.](https://ml-biomat.com/static/tutorials/machine-learning/figures/fc575aa0c6006346b83f2c3a.svg?v=fc575aa0c600)

Figure 2Outputs for the same 128 latent inputs after 0,300,750,and 1,500 generator updates. Orange shows a fixed subset of independent target points and blue shows generated points. Rows compare GAN and WGAN-GP with matching coordinate ranges.

## Follow the same noise through training

Replay actual training snapshots separated by 50 generator updates. Blue points correspond to the same 128 latent inputs; orange points are independent target samples. Select a point index to trace its output from initialization to the current frame. Statistics use all 2,048 generated points.

[Figure: Actual GAN replay, selected trajectory, and mode counts](https://ml-biomat.com/tutorials/machine-learning/m18/en/#M18-board)

GAN background shows realness probability. WGAN shows critic score after subtracting the current grid mean, with the frame’s color scale labeled; subtracting a constant leaves input gradients unchanged. Coordinates are dimensionless and share one range across frames.

## Replace realness probability with the cost of moving sand

Suppose two piles of sand have different shapes. How much work is required to rearrange one into the other? If moving each small amount costs its mass times the distance traveled, the comparison naturally accounts for spatial separation. Wasserstein distance formalizes this transport idea. In the simplest example, one unit of mass is concentrated at zero and another at two, giving transport distance two. Move the second mass to one half and the distance becomes one half. Even without overlap, the distance changes continuously as the distributions approach. This offers the generator feedback different from how easily two sources can be classified.

$$
W_1(P,Q)=\sup_{\|f\|_{\mathrm{Lip}}\le1}\left(\mathbb E_{x\sim P}f(x)-\mathbb E_{y\sim Q}f(y)\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/775185e771e23c7dab6c1e19.svg) | Target and generated distributions and their samples; the input space uses Euclidean distance. |
| ![Formula](https://ml-biomat.com/static/agent-math/299c0db7dbc479dcd70cb003.svg) | Real-valued critic satisfying \|f(x)−f(y)\|≤\|\|x−y\|\| for every pair; its output is not a probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/acf251e3efd8841b6a4a4236.svg) | Supremum over constrained functions, first Wasserstein distance, and expectation; distance inherits input-coordinate units. |

If P is concentrated at zero and Q at two, f(x)=−x gives a score difference of two. The Lipschitz constraint bounds any feasible difference by two, establishing the distance. A neural critic approximates this optimization within a finite function family and training budget. Our critic minimizes E_fake f−E_real f plus penalty; the generator minimizes −E_fake f.

WGAN approximates this distance with a real-valued scoring function, usually called a critic. Its output does not pass through a sigmoid and is not a probability. For a score difference to represent distance, the critic’s rate of change must be constrained: moving an input by one unit should change its score by at most one unit. This is a one-Lipschitz condition. Without it, multiplying every score by a thousand could increase the objective without improving the comparison. Original WGAN used weight clipping as an indirect constraint. WGAN-GP instead samples positions between real and generated points and penalizes the norm of the input gradient there.

$$
\widetilde x=t x+(1-t)G_\theta(z),\quad t\sim U[0,1],\qquad L_{\mathrm{GP}}=\lambda\mathbb E\left[(\|\nabla_{\widetilde x}f(\widetilde x)\|_2-1)^2\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a9c35f5ab162afce2c2cd0f4.svg) | Real, generated, and interpolated points, all matching-dimensional vectors. |
| ![Formula](https://ml-biomat.com/static/agent-math/12d756cc228f0bd6288c2eee.svg) | Uniformly sampled interpolation coefficient in [0,1], dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/188c73183abb00d191faa5b9.svg) | Gradient of critic score with respect to input coordinates and its Euclidean norm. |
| ![Formula](https://ml-biomat.com/static/agent-math/629afdc2e987ccdb6c292fcd.svg) | Penalty weight, ten here, and the penalty added to the critic objective. |

Gradient (3,4) has norm five and unweighted penalty (5−1)²=16, contributing 160 at λ=10. Gradient (0.6,0.8) has norm one and zero penalty. Input-gradient computation retains its graph because the subsequent parameter update differentiates this gradient-norm penalty. The constraint is evaluated at sampled interpolation locations.

Our WGAN-GP performs five critic updates per generator update with gradient-penalty weight ten. The penalty is evaluated at the sampled interpolation positions, constraining local score variation. It does not directly require a generated point to enter a target cluster. After 1,500 generator updates, this run places about 5.62% of points inside the specified neighborhoods and reaches the coverage threshold for two modes. Ordinary GAN reaches about 46.39% and covers eight modes. WGAN-GP uses 7,500 critic updates compared with 1,500 for ordinary GAN. The comparison therefore records objective, optimization progress, and computational allocation together, rather than assigning a winner from a method name.

Read the WGAN trajectory by asking whether the point cloud is still moving and whether mass concentrates in a few directions. A decreasing gradient penalty means gradients at sampled positions move closer to the requested norm; it measures something different from distribution matching. Smaller steps, more updates, a different critic capacity, or another constraint are specific subsequent experiments, evaluated with the same coverage and distance definitions. We retain the fixed endpoint and complete sequence of saved states so that oscillation and displacement remain inspectable, rather than selecting only an attractive intermediate picture.

## How DCGAN expands a small grid into an image

A point generator needs only two outputs. Images contain spatial relationships between many neighboring pixels. DCGAN uses local connectivity and shared parameters in an adversarial pair: the generator expands spatial dimensions, while the discriminator compresses images through strided convolutions. Our small convolutional generator projects eight noise coordinates into a 32-channel two-by-two grid, expands it to 16 channels at four by four, then produces a one-channel eight-by-eight image. Hidden layers use batch normalization and ReLU, with tanh at the output. Real images are also scaled to −1 through one so that the discriminator receives matching intensity conventions.

$$
n_{\mathrm{out}}=(n_{\mathrm{in}}-1)s-2p+k+o
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/08d7b5c10397ef3b8b7b5c3b.svg) | Input and output grid lengths along one spatial direction, counted in pixel positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/afe7915b50d7cb6d0c9a6acf.svg) | Stride, padding per side, kernel size, and output_padding; dilation is one, and o resolves output-size choices. |

For n_in=2,s=2,p=1,k=4,o=0, output length is four, then eight on the next layer. The no-padding overlap experiment maps length four to nine with kernel three or ten with kernel four, both at stride two. This formula determines size; pixel values arise from summed kernel contributions.

A transposed convolution lets each value on the small grid contribute a weighted patch to the larger grid. Contributions add where patches overlap. It is not a general inverse of an earlier convolution: different inputs may produce the same convolutional output, and transposing a matrix does not recover information that was lost. With kernel width three and stride two, some positions receive one contribution and others receive two. In two dimensions, overlap counts multiply into an alternating pattern of one, two, and four. Setting the input and kernel to ones exposes this geometry directly in the figure. Kernel width four and stride two produce more uniform interior overlap, while boundaries and learned weights still affect the output.

![Actual transposed-convolution output for a 4×4 all-one input, all-one kernels, stride two, and no padding. Values count overlaps. Kernel three produces 9×9 and kernel four 10×10; interior and boundary differences are retained.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1237ea149057f20a15289358.svg?v=1237ea149057)

Figure 3Actual transposed-convolution output for a 4×4 all-one input, all-one kernels, stride two, and no padding. Values count overlaps. Kernel three produces 9×9 and kernel four 10×10; interior and boundary differences are retained.

The 2016 Distill analysis of checkerboard artifacts emphasized this structural mechanism. Separating resizing from ordinary convolution changes the overlap pattern: first enlarge the grid using a specified rule, then learn a convolution. Asking how spatial sizes and contribution counts change makes visible grid artifacts traceable to actual computation. Our example trains a separate transposed-convolution image network, rather than relabeling the point generator as a DCGAN. It uses 1,437 training images and 1,200 updates of each adversarial participant, with 360 images retained to show independent handwriting examples.

![Top: 20 held-out handwriting images. Bottom: all 60 outputs for fixed eight-dimensional noise inputs after 1,200 tiny-DCGAN updates, using one 0–1 grayscale. Data: E. Alpaydin and C. Kaynak, UCI, CC BY 4.0. Generated images come from the trained model.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6753dfc80d7187bb642e6da6.svg?v=6753dfc80d71)

Figure 4Top: 20 held-out handwriting images. Bottom: all 60 outputs for fixed eight-dimensional noise inputs after 1,200 tiny-DCGAN updates, using one 0–1 grayscale. Data: E. Alpaydin and C. Kaynak, UCI, CC BY 4.0. Generated images come from the trained model.

The generated contact sheet shows all 60 latent inputs fixed before training, in their original order. Inspect stroke continuity, repetition across samples, and shapes that are difficult to categorize. This eight-by-eight task makes convolutional generation fully runnable on a CPU. Larger image tasks require additional spatial hierarchy, data, and an appropriate discriminator field of view. Sampling ordinarily runs only the generator, while the discriminator supplies feedback during training. Training cost and the cost of generating one new sample therefore describe different computations and should be recorded separately.

## Specify what is wanted: conditional GANs and image translation

An unconditional generator chooses which mode to produce. A conditional GAN also receives a category, text description, or another image. The 2014 conditional-GAN work supplied the condition to both generator and discriminator. The generator must satisfy a request, and the discriminator must evaluate compatibility with that request. A discriminator that sees only an image might approve a plausible cat even when the condition asks for a dog. Conditions add information, so a conditioned model and a model without category information do not solve identical input tasks.

We specify cluster identity with an eight-dimensional one-hot vector read by both networks. To connect this mechanism to paired image translation, the experiment also adds an L1 term with weight ten, bringing generated coordinates toward actual training points with the same category. The figure explicitly labels this model “cGAN + L1.” Each category describes a small Gaussian cluster, but random inputs are not paired with particular noisy target points, so the L1 component favors the cluster center. Evaluation cycles through category requests, 256 per class, making requested categories uniform by construction. Coverage then checks whether outputs actually reach those requested regions. Condition matching reaches 100%, about 99.95% of samples enter the required neighborhoods, and all eight modes meet the coverage threshold. Within-cluster variation remains another measurement: specifying a class, locating its center, and recovering its full conditional distribution are distinct goals.

$$
L_{G,c}=\mathbb E_{z,c}[-\log D(G(z,c),c)]+\lambda_1\mathbb E_{(c,y),z}\left[\frac1{d_y}\sum_{j=1}^{d_y}|G(z,c)_j-y_j|\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1fc699f40396eab4db38187a.svg) | Known condition, independent latent noise, and a target paired with the condition; c is an eight-dimensional one-hot cluster identity. |
| ![Formula](https://ml-biomat.com/static/agent-math/efc2ea22e3846678963a6b11.svg) | Conditional generator output and discriminator that also reads the condition. |
| ![Formula](https://ml-biomat.com/static/agent-math/e10654059f4b3a972139ef46.svg) | Output coordinate count, coordinate index, and L1 weight; d_y=2 and λ₁=10 in the point example. |

For target (2,0) and generated point (1.8,0.1), mean absolute error is (0.2+0.1)/2=0.15, contributing 1.5 at weight ten. The adversarial term additionally scores compatibility with the conditional data distribution. When z is independent of fine variation in y, L1 favors conditional medians and can reduce within-class variation, motivating a separate variance measurement.

pix2pix applies this idea to paired images. An edge map can serve as input, with its corresponding photograph as target. An encoder–decoder generator with skip connections passes spatial information toward the output. A PatchGAN discriminator scores multiple local image regions, supporting texture learning, while an L1 term encourages larger-scale agreement with the paired target. These terms enforce different requirements. When a grayscale scene admits several plausible colorings but each training input has one target, a strong reconstruction term can encourage an average or common color. Adding a random latent does not ensure that the model uses it; vary noise while holding the condition fixed and inspect the resulting output changes.

## Inspect plausibility, coverage, and variation separately

Mode collapse is easy to recognize when different random inputs repeatedly produce only a few types of output. A model may draw convincing eights while rarely drawing another digit. Selecting a handful of attractive images hides that failure, and a global average may also miss it. Our point task permits explicit definitions: a generated point is valid when it lies within 0.24 of its nearest center. A mode reaches the coverage threshold when it contains at least one percent of all 2,048 generated points. Distant transitional points are therefore not assigned to a nearest class and silently counted as high-quality coverage.

![Top: final point distributions and score fields, showing 128 generated points. GAN colors are probabilities; WGAN colors are real-valued critic scores. The conditional model uses category labels and an L1 term. Bottom: mode counts among all 2,048 samples within radius 0.24; the dashed line marks uniform allocation of 256 points.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ae9a842901f5f676db9d6b61.svg?v=ae9a842901f5)

Figure 5Top: final point distributions and score fields, showing 128 generated points. GAN colors are probabilities; WGAN colors are real-valued critic scores. The conditional model uses category labels and an L1 term. Bottom: mode counts among all 2,048 samples within radius 0.24; the dashed line marks uniform allocation of 256 points.

Mode counts do not determine whether within-cluster variance is correct. Mapping every latent in a category to exactly its center could earn excellent condition and validity scores while losing the target’s small random variations. The program separately records within-class variation and retains generated coordinates. Taking the square root of variance averaged over classes and coordinates gives 0.02458, below the target 0.08. Strong L1 guidance concentrates outputs near cluster centers while narrowing variation within them. Ordinary GAN covers all eight modes but has only 46.39% validity, leaving many points between or around the small clusters. Reading mode count, validity, and internal variation together prevents one favorable number from replacing the full generation task.

Another measurement projects real and generated points onto several directions, sorts each projected set, and averages distances between corresponding positions. For equal-weight empirical samples in one dimension, sorted matching gives Wasserstein distance. Averaging over 32 directions gives our projected distance. It responds to both position and mass allocation without using the discriminator currently being trained. A finite direction set can miss some structure, so we read it alongside mode coverage. The figure also keeps generator loss visible, while distinguishing ordinary GAN’s negative log probability from WGAN’s negative critic score. Their vertical values are not directly comparable rankings.

$$
\widehat W_{\mathrm{proj}}=\frac1{Kn}\sum_{k=1}^K\sum_{i=1}^n|a^{(k)}_{(i)}-b^{(k)}_{(i)}|,\qquad a^{(k)}_i=u_k^{\mathsf T}x_i,\quad b^{(k)}_i=u_k^{\mathsf T}\widehat x_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e57eec8d96fb9b979a8d1b6.svg) | Target and generated point i, and unit projection direction k; two-dimensional here. |
| ![Formula](https://ml-biomat.com/static/agent-math/3d0b0bef87f72567316ddce8.svg) | Projected coordinates and the ith sorted value; each sample set is sorted independently. |
| ![Formula](https://ml-biomat.com/static/agent-math/f1d1453c5268cc78383f2e6a.svg) | 32 projection directions, 2,048 samples per set, and finite-direction mean empirical distance; units match the coordinates. |

For one-dimensional targets (0,2) and generated values (1,3), sorted mean distance is one. In two dimensions, project onto each direction before applying the same calculation, then average across directions uniformly spanning zero to pi. Real and generated sets have equal size. This independent measurement differs from a trained critic’s score difference.

![Validity, 32-direction projected distance, and generator losses recorded every 50 generator updates. The test target set and evaluation noise are fixed. WGAN uses five critic updates per generator step and the other settings use one. Generator loss definitions differ.](https://ml-biomat.com/static/tutorials/machine-learning/figures/8c05db777e1282b2d5255895.svg?v=8c05db777e12)

Figure 6Validity, 32-direction projected distance, and generator losses recorded every 50 generator updates. The test target set and evaluation noise are fixed. WGAN uses five critic updates per generator step and the other settings use one. Generator loss definitions differ.

Image-generation studies often use FID, comparing means and covariances in a fixed feature space. It approximates the feature distributions as Gaussians before computing a distance; the feature extractor, preprocessing, and sample count are part of the evaluation conditions. A small example illustrates the information retained by such summaries. Eight equally weighted centers on a radius-two circle and a distribution containing only the four axis-aligned centers both have zero mean and covariance twice the identity. Their Gaussian approximations match even though the latter distribution misses four modes. The code checks that covariance equality numerically. Sample appearance, coverage, repetition, and distributional summaries thus answer complementary questions.

## The complete experiment retains samples, gradients, and budgets

The point experiments use 4,096 fixed training examples, 2,048 independently generated test examples, and 1,500 generator updates for each model. Ordinary and conditional GANs use one discriminator update per generator update; WGAN-GP uses five. All point networks have two 64-unit hidden layers and the same smooth output bound. The conditional model additionally receives cluster identities and a paired L1 training signal. Learning rates and objectives are specified separately in the code. The convolutional image experiment records its own latent dimension, image split, and fixed contact-sheet inputs. Each result can therefore be traced to the information and computation it used.

### Complete Python: four actual adversarial-training experiments

Run python main.py --output results --language en with NumPy, Matplotlib, scikit-learn, and PyTorch. No model weights are downloaded. It trains GAN, WGAN-GP, cGAN+L1, and a tiny DCGAN, producing five SVGs, summary.json, data, weights, and replay states every 50 updates.

```
"""Train ordinary GAN, WGAN-GP, a conditional GAN, and a tiny image DCGAN.
Synthetic mixture samples are generated here; images are sklearn's UCI digits.
"""
from pathlib import Path
import argparse,json,platform,copy,time
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
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):fig.savefig(out/f'{name}-{a.language}.svg',bbox_inches='tight');plt.close(fig)
angles=np.arange(8)*np.pi/4;centers=np.c_[2*np.cos(angles),2*np.sin(angles)].astype('float32')
def mixture(n,seed):
 r=np.random.default_rng(seed);labels=r.integers(0,8,n);return (centers[labels]+r.normal(0,.08,(n,2))).astype('float32'),labels
train,labels=mixture(4096,180);test,testlabels=mixture(2048,181);xt=torch.tensor(train);lab=torch.tensor(labels)
zg=torch.Generator().manual_seed(182);fixed=torch.randn((2048,2),generator=zg);tracez=fixed[:128]
class Generator(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(10 if conditional else 2,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU(),nn.Linear(64,2))
 def forward(self,z,c=None):return 3*torch.tanh(self.net(torch.cat([z,F.one_hot(c,8).float()],1) if self.conditional else z)/3)
class Critic(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(10 if conditional else 2,64),nn.LeakyReLU(.2),nn.Linear(64,64),nn.LeakyReLU(.2),nn.Linear(64,1))
 def forward(self,x,c=None):return self.net(torch.cat([x,F.one_hot(c,8).float()],1) if self.conditional else x).squeeze(1)
def measures(fake):
 dist=np.linalg.norm(fake[:,None]-centers[None],axis=2);nearest=dist.argmin(1);valid=dist.min(1)<.24;counts=np.bincount(nearest[valid],minlength=8);prob=counts/max(1,counts.sum())
 directions=np.c_[np.cos(np.linspace(0,np.pi,32,endpoint=False)),np.sin(np.linspace(0,np.pi,32,endpoint=False))]
 sliced=float(np.mean(np.abs(np.sort(fake@directions.T,axis=0)-np.sort(test@directions.T,axis=0))))
 return dict(valid_fraction=float(valid.mean()),covered_modes=int((counts>=.01*len(fake)).sum()),mode_counts=counts.tolist(),mode_entropy=float(-(prob[prob>0]*np.log(prob[prob>0])).sum()),sliced_w1=sliced)
gridx=np.linspace(-3,3,31);gx,gy=np.meshgrid(gridx,gridx);grid=torch.tensor(np.c_[gx.ravel(),gy.ravel()],dtype=torch.float32)
models={};metrics={};histories={};snapshots={};times={};final_samples={}
for name in ['gan','wgan','conditional']:
 start=time.perf_counter();cond=name=='conditional';torch.manual_seed(183);g=Generator(cond);d=Critic(cond)
 lr=.0002 if name in ['wgan','conditional'] else .0005;betas=(0.,.9) if name=='wgan' else (.5,.9)
 go=torch.optim.Adam(g.parameters(),lr=lr,betas=betas);do=torch.optim.Adam(d.parameters(),lr=lr,betas=betas);rng=torch.Generator().manual_seed(184);history=[];frames=[]
 def snapshot(step):
  with torch.no_grad():
   c=torch.arange(len(fixed))%8 if cond else None;fake=g(fixed,c).numpy();m=measures(fake)
   values=d(grid,torch.zeros(len(grid),dtype=torch.long) if cond else None)
   if name!='wgan':values=values.sigmoid()
   frames.append(dict(step=step,samples=fake[:128].tolist(),field=values.numpy().reshape(31,31).tolist(),metrics=m));return m
 snapshot(0)
 for step in range(1,1501):
  ncritic=5 if name=='wgan' else 1
  for _ in range(ncritic):
   ids=torch.randint(len(xt),(128,),generator=rng);real=xt[ids];c=lab[ids] if cond else None
   fake=g(torch.randn((128,2),generator=rng),c).detach()
   if name=='wgan':
    t=torch.rand((128,1),generator=rng);mix=(t*real+(1-t)*fake).requires_grad_();s=d(mix);grad=torch.autograd.grad(s.sum(),mix,create_graph=True)[0];penalty=(grad.norm(dim=1)-1).square().mean();dl=d(fake).mean()-d(real).mean()+10*penalty
   else:dl=F.softplus(-d(real,c)).mean()+F.softplus(d(fake,c)).mean();penalty=torch.tensor(0.)
   do.zero_grad();dl.backward();do.step()
  for par in d.parameters():par.requires_grad_(False)
  pair_ids=torch.randint(len(xt),(128,),generator=rng) if cond else None
  c=lab[pair_ids] if cond else None;fake=g(torch.randn((128,2),generator=rng),c)
  gl=-d(fake).mean() if name=='wgan' else F.softplus(-d(fake,c)).mean()
  if cond:gl=gl+10*F.l1_loss(fake,xt[pair_ids])
  go.zero_grad();gl.backward();go.step()
  for par in d.parameters():par.requires_grad_(True)
  if step%50==0:
   m=snapshot(step);history.append([step,dl.item(),gl.item(),penalty.item(),m['valid_fraction'],m['sliced_w1']])
 with torch.no_grad():
  c=torch.arange(len(fixed))%8 if cond else None;fake=g(fixed,c).numpy();metrics[name]=measures(fake);final_samples[name]=fake.copy()
  if cond:
   metrics[name]['condition_match']=float((np.linalg.norm(fake[:,None]-centers[None],axis=2).argmin(1)==c.numpy()).mean())
   metrics[name]['within_class_std']=float(np.sqrt(np.mean([np.var(fake[c.numpy()==k],axis=0).mean() for k in range(8)])))
   metrics[name]['paired_l1_weight']=10
 metrics[name].update(generator_updates=1500,critic_updates=1500*(5 if name=='wgan' else 1),generator_parameters=sum(p.numel() for p in g.parameters()),critic_parameters=sum(p.numel() for p in d.parameters()),final_gradient_penalty=history[-1][3])
 models[name]=(g,d);histories[name]=np.array(history);snapshots[name]=frames;times[name]=time.perf_counter()-start
 torch.save(dict(generator=g.state_dict(),critic=d.state_dict()),out/f'{name}.pt')

# Tiny DCGAN: latent8 -> (32,2,2) -> (16,4,4) -> (1,8,8).
digits=load_digits();images=torch.tensor((digits.images/8-1).astype('float32'))[:,None]
image_train,image_test=train_test_split(np.arange(len(images)),test_size=360,stratify=digits.target,random_state=185)
class ImageGenerator(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(8,128),nn.Unflatten(1,(32,2,2)),nn.BatchNorm2d(32),nn.ReLU(),nn.ConvTranspose2d(32,16,4,2,1,bias=False),nn.BatchNorm2d(16),nn.ReLU(),nn.ConvTranspose2d(16,1,4,2,1),nn.Tanh())
 def forward(self,z):return self.net(z)
class ImageDiscriminator(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Conv2d(1,16,4,2,1),nn.LeakyReLU(.2),nn.Conv2d(16,32,4,2,1),nn.LeakyReLU(.2),nn.Flatten(),nn.Linear(128,1))
 def forward(self,x):return self.net(x).squeeze(1)
torch.manual_seed(186);ig=ImageGenerator();idd=ImageDiscriminator();igo=torch.optim.Adam(ig.parameters(),lr=.0002,betas=(.5,.999));ido=torch.optim.Adam(idd.parameters(),lr=.0002,betas=(.5,.999));rng=torch.Generator().manual_seed(187);igfixed=torch.randn((60,8),generator=rng);image_history=[]
for step in range(1,1201):
 ids=torch.randint(len(image_train),(64,),generator=rng);real=images[image_train[ids]];fake=ig(torch.randn((64,8),generator=rng)).detach();dl=F.softplus(-idd(real)).mean()+F.softplus(idd(fake)).mean();ido.zero_grad();dl.backward();ido.step()
 for par in idd.parameters():par.requires_grad_(False)
 fake=ig(torch.randn((64,8),generator=rng));gl=F.softplus(-idd(fake)).mean();igo.zero_grad();gl.backward();igo.step()
 for par in idd.parameters():par.requires_grad_(True)
 if step%50==0:image_history.append([step,dl.item(),gl.item()])
ig.eval()
with torch.no_grad(): generated=((ig(igfixed)+1)/2).numpy()[:,0]
torch.save(dict(generator=ig.state_dict(),discriminator=idd.state_dict()),out/'dcgan.pt')
# A transposed convolution with all-one input/kernel makes overlap counts explicit.
overlap3=F.conv_transpose2d(torch.ones(1,1,4,4),torch.ones(1,1,3,3),stride=2).numpy()[0,0]
overlap4=F.conv_transpose2d(torch.ones(1,1,4,4),torch.ones(1,1,4,4),stride=2).numpy()[0,0]
fig,axs=plt.subplots(2,3,figsize=(12,7.6),layout='constrained')
for col,name in enumerate(['gan','wgan','conditional']):
 fake=np.array(snapshots[name][-1]['samples']);field=np.array(snapshots[name][-1]['field']);ax=axs[0,col]
 if name!='conditional':im=ax.contourf(gx,gy,field,levels=15,cmap='PuBuGn',alpha=.5);fig.colorbar(im,ax=ax,fraction=.045,label=tr('评分','Score') if name=='wgan' else 'P(real)')
 ax.scatter(test[:300,0],test[:300,1],s=6,c='#ba783f',alpha=.45,label=tr('目标','Target'));ax.scatter(fake[:,0],fake[:,1],s=8,c='#125f82',label=tr('生成','Generated'));ax.set(xlim=(-3,3),ylim=(-3,3),xlabel='x1',ylabel='x2',title='cGAN + L1' if name=='conditional' else name.upper());ax.set_aspect('equal');ax.legend(fontsize=8)
 axs[1,col].bar(np.arange(8),metrics[name]['mode_counts'],color='#125f82');axs[1,col].axhline(2048/8,color='#b85d30',ls='--',label=tr('均匀期望','Uniform expectation'));axs[1,col].set(xlabel=tr('模式编号','Mode index'),ylabel=tr('有效生成点数','Valid generated count'),title=tr('覆盖 ','Coverage ')+f"{metrics[name]['covered_modes']}/8; "+tr('有效 ','valid ')+f"{metrics[name]['valid_fraction']:.1%}");axs[1,col].set_xticks(range(8))
save(fig,'distribution')
fig,axs=plt.subplots(2,4,figsize=(13,6.8),layout='constrained')
for row,name in enumerate(['gan','wgan']):
 for col,step in enumerate([0,300,750,1500]):
  frame=snapshots[name][step//50];fake=np.array(frame['samples']);ax=axs[row,col];ax.scatter(test[:300,0],test[:300,1],s=4,c='#b87941',alpha=.4);ax.scatter(fake[:,0],fake[:,1],s=7,c='#125f82');ax.set(xlim=(-3,3),ylim=(-3,3),title=f'{name.upper()} / {step}',xlabel='x1',ylabel='x2');ax.set_aspect('equal')
save(fig,'training')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for name,color in [('gan','#125f82'),('wgan','#b85d30'),('conditional','#658248')]:
 h=histories[name];label='cGAN + L1' if name=='conditional' else name;axs[0].plot(h[:,0],h[:,4],color=color,label=label);axs[1].plot(h[:,0],h[:,5],color=color,label=label)
axs[0].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('有效样本比例','Valid fraction'),ylim=(0,1),title=tr('A  落在目标邻域内','A  Within target neighborhoods'));axs[0].legend(fontsize=9)
axs[1].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('32方向平均投影W1','Mean projected W1, 32 directions'),title=tr('B  同时观察位置与质量分配','B  Position and mass distribution'))
for name,color in [('gan','#125f82'),('wgan','#b85d30')]:
 h=histories[name];axs[2].plot(h[:,0],h[:,2],color=color,label=name)
axs[2].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('各自定义的G损失','G loss under its own objective'),title=tr('C  两种损失具有不同含义','C  Losses have different meanings'));axs[2].legend(fontsize=9);save(fig,'metrics')
fig=plt.figure(figsize=(13,8));gs=fig.add_gridspec(2,1,height_ratios=[1,1.25],hspace=.27)
top=gs[0].subgridspec(2,10,wspace=.05,hspace=.1)
for i in range(20):
 ax=fig.add_subplot(top[i//10,i%10]);ax.imshow((images[image_test[i],0]+1)/2,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('独立保留图像','Held-out images'),loc='left',fontsize=12)
bottom=gs[1].subgridspec(5,12,wspace=.04,hspace=.08)
for i,img in enumerate(generated):
 ax=fig.add_subplot(bottom[i//12,i%12]);ax.imshow(img,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('DCGAN：固定60个噪声，1200次更新','DCGAN: 60 fixed inputs after 1,200 updates'),loc='left',fontsize=12)
save(fig,'dcgan')
fig,axs=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
for ax,img,k in zip(axs,[overlap3,overlap4],[3,4]):
 im=ax.imshow(img,vmin=0,vmax=4,cmap='YlGnBu');ax.set_title(f'kernel={k}, stride=2');ax.set(xlabel=tr('输出列','Output column'),ylabel=tr('输出行','Output row'));fig.colorbar(im,ax=ax,ticks=range(5),label=tr('覆盖次数','Overlap count'))
 for r in range(len(img)):
  for c in range(len(img)):ax.text(c,r,int(img[r,c]),ha='center',va='center',fontsize=9,color='white' if img[r,c]>2 else '#152d3a')
save(fig,'overlap')
logit=torch.tensor(np.log(.01/.99),dtype=torch.float64,requires_grad=True);saturating=F.logsigmoid(-logit);nonsaturating=F.softplus(-logit)
gsat=torch.autograd.grad(saturating,logit,retain_graph=True)[0].item();gnon=torch.autograd.grad(nonsaturating,logit)[0].item()
moment_error=float(np.max(np.abs(np.cov(centers.T,bias=True)-np.cov(centers[::2].T,bias=True))))
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,test=2048,modes=8,radius=2,std=.08,valid_radius=.24,generator_bound=3),metrics=metrics,
 dcgan=dict(train=len(image_train),test=len(image_test),updates=1200,generated=60,generator_parameters=sum(p.numel() for p in ig.parameters()),discriminator_parameters=sum(p.numel() for p in idd.parameters())),
 hand=dict(discriminator_loss=float(-2*np.log(.8)),saturating_gradient=gsat,nonsaturating_gradient=gnon,gradient_norm=float(np.linalg.norm([3,4])),gradient_penalty=float((np.linalg.norm([3,4])-1)**2),transpose_size_k3=int(overlap3.shape[0]),transpose_size_k4=int(overlap4.shape[0]),eight_vs_four_covariance_error=moment_error),runtime_seconds=times)
(out/'replay.json').write_text(json.dumps(dict(centers=centers.tolist(),real=test[:160].tolist(),grid=gridx.tolist(),models={n:snapshots[n] for n in ['gan','wgan']}),separators=(',',':')),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train=train,test=test,labels=labels,fixed_latents=fixed.numpy(),conditional_requests=np.arange(len(fixed))%8,image_train_indices=image_train,image_test_indices=image_test,generated_images=generated,image_history=image_history,overlap3=overlap3,overlap4=overlap4,**{n+'_final':v for n,v in final_samples.items()},**{n+'_history':h for n,h in histories.items()})
with np.load(out/'experiment.npz') as saved:
 summary['saved_data']={}
 for name in ['gan','wgan','conditional']:
  restored=saved[name+'_final'];recomputed=measures(restored)
  summary['saved_data'][name]=dict(rows=len(restored),coordinate_max_error=float(np.max(np.abs(restored-final_samples[name]))),valid_error=abs(recomputed['valid_fraction']-metrics[name]['valid_fraction']),mode_counts_match=recomputed['mode_counts']==metrics[name]['mode_counts'],sliced_w1_error=abs(recomputed['sliced_w1']-metrics[name]['sliced_w1']))
 requests=saved['conditional_requests'];restored=saved['conditional_final'];std=float(np.sqrt(np.mean([np.var(restored[requests==k],axis=0).mean() for k in range(8)])))
 summary['saved_data']['conditional'].update(request_counts=np.bincount(requests,minlength=8).tolist(),within_class_std_error=abs(std-metrics['conditional']['within_class_std']))
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

Read one discriminator update through its detach operation, then follow a generator update through a fixed discriminator’s input derivative. Calculate the two generator gradients at probability 0.01 by hand, and connect the overlap-count figure to transposed convolution. The program saves model weights, actual snapshots every 50 updates, evaluation curves, and source data. When changing update ratios or loss weights, retaining the same latent inputs and test points makes the resulting changes easier to interpret. Learning signals, image structure, and evaluation definitions are connected throughout this experiment; each design change should have a corresponding observable effect.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M18.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661)

   Original adversarial objective, optimal discriminator, and generator learning.

   Primary paper; no figure copied
2. [GAN Lab](https://poloclub.github.io/ganlab/)

   Original animation and open implementation of two-dimensional training dynamics.

   Apache 2.0; license retained; repository root has no NOTICE file
3. [DCGAN](https://arxiv.org/abs/1511.06434)

   Convolutional generator and discriminator design.

   Primary paper; no figure copied
4. [Wasserstein GAN](https://arxiv.org/abs/1701.07875)

   Distribution distances and Lipschitz critics.

   Primary paper; no figure copied
5. [Improved Training of Wasserstein GANs](https://arxiv.org/abs/1704.00028)

   Input-gradient penalty.

   Primary paper; no figure copied
6. [Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784)

   Conditioning both networks.

   Primary paper; no figure copied
7. [Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)

   pix2pix, PatchGAN, and paired L1 supervision.

   Primary paper; no figure copied
8. [Deconvolution and Checkerboard Artifacts](https://distill.pub/2016/deconv-checkerboard/)

   Uneven overlap mechanism; our figure is independently computed.

   CC BY 4.0 reference; original images not copied
9. [GANs Trained by a Two Time-Scale Update Rule](https://arxiv.org/abs/1706.08500)

   Update timescales and FID definition.

   Primary paper; no figure copied
10. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    Image data and license.

    CC BY 4.0; E. Alpaydin and C. Kaynak
