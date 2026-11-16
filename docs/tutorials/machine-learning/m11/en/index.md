# Learning with fewer labels: representations, questions, and memory

Source: https://ml-biomat.com/tutorials/machine-learning/m11/en/
Language: en

Start with two views of one image, then connect unlabeled training, annotation, adaptation, and replay.

## Many photographs, few answers: where learning begins

When organizing ten thousand photographs, saving the files is often easier than describing every image. Assigning a category to an email may take seconds; marking all cells in a microscopy image may take much longer. Machine learning therefore draws on two different resources: how many inputs we can collect, and how many reliable answers we can attach to them. Calling both resources “data quantity” hides an opportunity. Even without a category label, an image contains edges, shapes, and relationships that a model can study. This chapter asks how to learn from that structure and where to spend a limited supply of human judgments.

Several learning strategies fit into this setting. A model that constructs a prediction problem from the input itself uses self-supervision. A classifier trained with a small labeled set and a larger unlabeled set uses semi-supervised learning. A model that selects the next images for a person to label participates in active learning. These can form successive stages of one system: learn a representation, request useful answers, then update a predictor. Weak supervision concerns a different property: the answers may come from approximate rules, historical records, or coarse annotations. To keep the names meaningful, ask who supplies the supervision in each update and what the model is being asked to predict.

SimCLR, published in 2020, organized image augmentation, a representation network, and a contrastive objective into a particularly clear experimental framework. BYOL, also from 2020, explored representation learning without explicit negative examples, while the 2021 MAE work used visible patches to reconstruct missing image content. These developments turned learning structure before learning a specific task into concrete, comparable training procedures. The original tutorial figure below addresses a practical question: what classification performance does a representation support as the label budget increases? Read the images-per-class axis first, then follow accuracy along the curve. Our smaller handwriting experiment will make the training, querying, and forgetting processes directly inspectable.

![Original tutorial experiment on STL10 label budgets: training examples per class on the horizontal axis, showing test accuracy of a classifier on SimCLR features. The measurements and models belong to that tutorial. Phillip Lippe, UvA Deep Learning Tutorials, Tutorial 17, output cell \[18\], MIT, unchanged. Our digit results appear in the later figures.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ebe81c9a959ff485fffd26d6.svg?v=ebe81c9a959f)

Figure 1Original tutorial experiment on STL10 label budgets: training examples per class on the horizontal axis, showing test accuracy of a classifier on SimCLR features. The measurements and models belong to that tutorial. Phillip Lippe, UvA Deep Learning Tutorials, Tutorial 17, output cell [18], MIT, unchanged. Our digit results appear in the later figures.

## Representation space: making similarity computable

An eight-by-eight grayscale image can be written as 64 numbers, but nearby arrays do not necessarily depict similar digits. Moving a stroke one pixel changes many coordinates, while two different digits may share large areas of background. A representation network reorganizes the information into a shorter vector so that later tasks can read useful structure more easily. Think of reorganizing a library: raw pixels resemble shelving books by the color of their pages, whereas a useful representation begins to place related content nearby. A classifier can then divide that organized space into categories. The representation does not need to know the final category names in advance.

Our encoder maps 64 input coordinates to 32 representation coordinates. To compare directions, we divide each vector by its length and take their inner product. Multiplying an entire vector by two then leaves similarity unchanged. This choice removes magnitude from the comparison, which suits our interest in stroke structure. When magnitude carries confidence, intensity, or a physical measurement, normalization changes the question and should be chosen accordingly. A zero vector has no direction; the implementation uses the library’s stable treatment of very small lengths. Representation coordinates also generally lack individual semantic names. Information is distributed across coordinates, so coordinate seven cannot automatically be interpreted as “how circular the image is.”

$$
\widehat h=\frac{h}{\|h\|_2},\qquad s(h,g)=\widehat h^{\mathsf T}\widehat g
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6d2cac1d7937c055c2fc3fad.svg) | Two d-dimensional representation vectors, d=32 here; dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/86a6ff610030486a41b7d0b1.svg) | Euclidean length; j indexes coordinates. Direct division requires a nonzero vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0cf8e03c42a61e2ae1cdb0d.svg) | Unit-length normalized vectors with the original shape. |
| ![Formula](https://ml-biomat.com/static/agent-math/04ad2f8aaa01d02353cfeba2.svg) | Cosine similarity and transpose notation; s is dimensionless and ranges from −1 to 1. |

For h=(0.6,0.8) and g=(0,1), both lengths are one and the inner product is 0.8. Scaling h to (1.2,1.6) gives length two and the same normalized result. Summing coordinate products measures directional alignment: opposite directions yield −1, orthogonal vectors zero, and matching directions one.

Once a representation exists, we can read it in several ways. Freezing the encoder and fitting a linear classification head tests how the existing coordinates support class separation. Updating the encoder as well is fine-tuning. Comparing an input with a few reference examples enables retrieval or prototype classification. Transfer learning occurs when representations or parameters move from one learning stage into another task; the stages can use different forms of supervision. We will give exactly the same 50 labels to linear classifiers on pixels, randomly initialized representations, and contrastively trained representations. Holding the label budget fixed separates exposure to additional unlabeled inputs from access to additional human answers.

## Contrastive learning: why inspect the same image twice?

Contrastive learning first constructs two observations. Independently add mild noise and hide a small fraction of the pixels in one digit image, producing views A and B. Their common origin makes them a positive pair. Views of other images in the batch become candidate negatives. Given A, the network should recover its corresponding B among those candidates. The supervision says “these observations came from the same input,” without saying “the image depicts eight.” Augmentation specifies which changes the model should ignore. Mild noise may be irrelevant, but rotating a six into a nine and enforcing consistency would teach the wrong invariance. Looking at augmented images is therefore a useful part of designing the learning problem.

![The same ten training images before and after two independent augmentations. Intensity range 0–1; noise standard deviation 0.08; pixel masking probability 0.15. Digit headings are for interpretation and are not supplied to contrastive training. Data: E. Alpaydin, C. Kaynak, UCI, CC BY 4.0.](https://ml-biomat.com/static/tutorials/machine-learning/figures/866cbb29d811c22a74f0c3d0.svg?v=866cbb29d811)

Figure 2The same ten training images before and after two independent augmentations. Intensity range 0–1; noise standard deviation 0.08; pixel masking probability 0.15. Digit headings are for interpretation and are not supplied to contrastive training. Data: E. Alpaydin, C. Kaynak, UCI, CC BY 4.0.

A projection head follows the encoder, mapping the 32-dimensional representation to a normalized 16-dimensional vector. The projection is specialized for the contrastive objective; subsequent classification reads the encoder output. This gives the two stages some freedom to organize information differently. A batch of 128 original images creates 256 views. Excluding an anchor itself leaves 255 candidates, including exactly one paired positive. The final, smaller batch has fewer candidates, and the code constructs its targets using the actual batch size. The loss decreases as the correct partner receives a larger share of the candidate probability. The expression below turns that matching task into a differentiable calculation.

$$
\ell_i=-\log\frac{\exp(s_{i,p(i)}/\tau)}{\sum_{k\ne i}^{2B}\exp(s_{ik}/\tau)},\qquad L=\frac1{2B}\sum_{i=1}^{2B}\ell_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4b3e0810d86961c413c0d22d.svg) | Original-image batch size and total views from two augmentations; the last batch uses its actual B. |
| ![Formula](https://ml-biomat.com/static/agent-math/eee47ba016d4b0ec84f4b688.svg) | Anchor index, candidate index, and index of the anchor’s paired view. |
| ![Formula](https://ml-biomat.com/static/agent-math/96e5c22b3bf6f2ac2a0feadc.svg) | Cosine similarity between normalized 16-dimensional projections i and k; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa8e2e336dcfa0bdaadf756.svg) | Positive temperature, 0.2 here, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc3c3e662e2bd7210059aba7.svg) | Per-anchor loss, mean over views, natural exponential, and natural logarithm; losses in nats. |

Excluding the anchor avoids the trivial task of retrieving itself. With B=2, there are three candidates. Equal similarities give positive probability 1/3 and loss ln3≈1.09861. A positive similarity of one and two negative similarities of zero, at temperature one, give probability e/(e+2) and loss about 0.55144. Averaging over every view makes both augmentations participate symmetrically.

Temperature controls how strongly similarity differences affect the candidate probabilities. With a small temperature, a slightly more similar candidate can dominate the distribution, increasing the influence of difficult or incorrect neighbors. Negatives introduce another tension: two independently collected eights are negatives for the current objective, even though a later classifier should group them together. Distinguishing individual instances and recognizing categories are different tasks. We therefore inspect both the contrastive loss and the later labeled task. The similarity matrix arranges ten paired views along its axes, with positives on the diagonal. The two-dimensional projection shows only part of the 32-dimensional structure. Test labels supply the plot colors and never enter representation training.

![A: measured mean contrastive loss over 80 epochs. B: cosine similarities for ten view pairs; matching indices share an original image. C: 32-dimensional encoder outputs for 360 test images projected onto two principal components fitted to training representations. Colors use test labels for visualization only.](https://ml-biomat.com/static/tutorials/machine-learning/figures/cbafca59986a64838fd98a72.svg?v=cbafca59986a)

Figure 3A: measured mean contrastive loss over 80 epochs. B: cosine similarities for ten view pairs; matching indices share an original image. C: 32-dimensional encoder outputs for 360 test images projected onto two principal components fitted to training representations. Colors use test labels for visualization only.

## Fill a gap, follow a teacher, or use an incomplete answer

Contrastive learning organizes representations by matching partners; masked modeling organizes them by filling gaps. Divide an image into patches, hide some patches, let the encoder process the visible subset, and ask a decoder to recover missing content using the representation and position information. MAE allocates the expensive encoder to visible patches and uses a lighter decoder for reconstruction. Masked language modeling follows a related idea, with discrete tokens as the prediction targets. The important design question is whether the missing content requires context. When a target can be copied directly from an input, the task does little to encourage the dependencies we hoped the model would learn.

$$
L_{\mathrm{mask}}=\frac1{|M|}\sum_{j\in M}(\widehat x_j-x_j)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3338e5ecd5025495beebe602.svg) | True and predicted intensity at hidden position j; normalized dimensionless values here. |
| ![Formula](https://ml-biomat.com/static/agent-math/e7fd209208b840d9771c9d72.svg) | Set of masked positions and its size; at least one position is masked. |
| ![Formula](https://ml-biomat.com/static/agent-math/2dd22608cd95890d21973e89.svg) | Mean squared error on masked positions only, in squared normalized-intensity units. |

For hidden targets (0.2,0.8) and predictions (0.3,0.6), squared errors are 0.01 and 0.04, averaging to 0.025. Visible positions are excluded so that easy copies do not dominate this objective. MAE reconstructs patch pixels; pixel indices express the same calculation here. A mask indicator distinguishes missing content from a genuinely zero intensity.

Self-distillation provides a different target: another version of the model acts as a teacher. In BYOL, an online network reads one view and uses a prediction head to approach the representation produced by a target network on another view. The target branch receives no gradient from this loss. Instead, its parameters follow a slow moving average of the online parameters, making the teacher change more smoothly. Every image could, in principle, produce the same vector and still agree with its paired view; this is representation collapse. The prediction head, asymmetric updates, and normalization affect the training dynamics together. Stopping a gradient is not a general guarantee against collapse for every architecture. Variation across inputs and downstream performance remain useful measurements.

$$
\xi\leftarrow m\xi+(1-m)\theta_{\mathrm{ep}},\qquad L_{\mathrm{distill}}=\|\widehat q_\theta(v_1)-\operatorname{sg}(\widehat z_\xi(v_2))\|_2^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/82b55e8ce69542eb61b08c56.svg) | θ contains all online trainable parameters; ξ contains target encoder and projection parameters. The target branch has no prediction head. |
| ![Formula](https://ml-biomat.com/static/agent-math/0030058cb275aaad3114e821.svg) | The online encoder and projection subset corresponding to the target; only this subset enters the moving average. The prediction head is trained by gradients on the online branch only. |
| ![Formula](https://ml-biomat.com/static/agent-math/8673ecb2a5bdfceacd858b53.svg) | Target-update momentum; values closer to one change more slowly per update. |
| ![Formula](https://ml-biomat.com/static/agent-math/0315e8b8aea066fef3c4e73d.svg) | Two augmented views of the same original input. |
| ![Formula](https://ml-biomat.com/static/agent-math/2465c23fdfd871da565282f3.svg) | Online predictor output and target representation, normalized to unit vectors of matching dimension. |
| ![Formula](https://ml-biomat.com/static/agent-math/92e7a9bd6c7eaacb185459e8.svg) | Stop-gradient operation and one-direction squared-distance objective, dimensionless. |

A target parameter of 0.2 and online parameter of 0.6 with m=0.9 produce an updated target of 0.24. Unit outputs (1,0) and (0.8,0.6) have squared distance 0.2²+0.6²=0.4. Stop-gradient retains the target value in the comparison without backpropagating this loss through it. Full BYOL also swaps the views for the opposite direction.

With a few human labels available, semi-supervised learning can incorporate the classification task directly. FixMatch predicts an unlabeled input under a weak augmentation, keeps a high-confidence prediction as a pseudo-label, and asks a strongly augmented version to predict the same category. For probabilities (0.92, 0.08), a threshold of 0.9 accepts the first category; for (0.58, 0.42), that example contributes no pseudo-label update on this step. The threshold changes which examples participate, while the meaning of confidence depends on the model and validation evidence. Our 50-label classifier selects 123 remaining training images at a threshold of 0.8. All selected predictions happen to be correct in this run. Their hidden labels are revealed only for this diagnostic; they are not used to train the classifier. Evaluating a subsequent pseudo-label update would require actually performing that additional training stage.

Weak supervision obtains answers from another source. A rule containing “refund” might label an email as a refund request, while a transaction record might suggest an after-sales category. Such rules can disagree or share the same blind spot. Systems such as Snorkel model coverage, conflicts, and dependencies among labeling functions before training a final predictor. Coarse boxes, noisy text labels, and historical business fields can also provide weak supervision. They extend human knowledge across more examples, but their systematic error patterns belong in the data design. This makes the distinction concrete: an unlabeled input, a model’s pseudo-label, and a noisy rule-derived answer carry different information.

## Which image deserves the next question?

Active learning delegates a decision within the training process to the model: where should the next annotation budget go? Fit a predictor on existing labels, score the unlabeled pool, ask a person for selected answers, and refit. Uncertainty is an intuitive score. A binary predictor returning (0.5, 0.5) finds two answers equally plausible, whereas (0.99, 0.01) expresses a strong preference. Entropy compresses this spread into one number. Because it measures the model’s own uncertainty, it can find examples near a decision boundary. It can also repeatedly select blurred, corrupted, or irrelevant inputs whose ambiguity is difficult to resolve.

$$
H(p)=-\sum_{k=1}^{C}p_k\log p_k
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0547280d94d95a6b3705ca72.svg) | Class count and class index, C=10 in the digit experiment. |
| ![Formula](https://ml-biomat.com/static/agent-math/e02cdc3c22c69f868e141570.svg) | Classifier probabilities for one unlabeled input, dimensionless and summing to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/295b5229388ab789074fb769.svg) | Predictive entropy and natural logarithm; entropy in nats, with 0log0 defined as zero. |

Binary probabilities (0.5,0.5) have entropy ln2≈0.69315; (0.9,0.1) gives about 0.32508. A uniform ten-class prediction has entropy ln10≈2.30259. The score describes the current predictor’s uncertainty. Confident errors can receive low scores, motivating complementary coverage and diversity criteria.

Useful query strategies often include representativeness and diversity. Twenty nearly identical blurred images may answer essentially one question. Covering different regions of representation space lets a limited label budget address more variation. A practical strategy can first shortlist uncertain examples, then choose a diverse subset, or enforce coverage across rare classes, devices, and time periods. Querying must operate within the training pool, while the test set remains a fixed examination. Using test labels to decide what to annotate and then evaluating on the same test set changes the meaning of the budget comparison.

Our experiment begins with five labels per class, 50 total, and adds 20 labels in each of five rounds. Entropy and random selection share the initial labels, frozen representation, and linear classifier. At 150 labels, entropy selection reaches 86.11% test accuracy and random selection reaches 88.06%; the curves cross at intermediate budgets. Additional labels improve overall recognition, but entropy selection does not dominate throughout this run. The selected samples may concentrate on difficult cases, and the representation may organize those cases imperfectly. The interaction lets you choose a point to query and see how its answer moves class prototypes and the resulting prediction regions.

![Left: measured test accuracy from the same 50 initial labels through five rounds of 20 additional labels; both policies query the training pool. Right: four prediction methods using exactly the same 50 labels. Each curve is one fixed-seed run; no repeated-run error bars are plotted.](https://ml-biomat.com/static/tutorials/machine-learning/figures/a1866720e730c9d6a61dc0e9.svg?v=a1866720e730)

Figure 4Left: measured test accuracy from the same 50 initial labels through five rounds of 20 additional labels; both policies query the training pool. Right: four prediction methods using exactly the same 50 labels. Each curve is one fixed-seed run; no repeated-run error bars are plotted.

## Choose the next label yourself

These teaching points use the fixed rule x+0.55y>0.05. Only two labels are initially revealed. Click a gray point, or use Tab and Enter, to request one answer; prototypes and nearest-prototype regions update. “Most uncertain” applies an entropy query. A point’s true class is shown after querying. Random queries use a fixed-seed 114 pseudorandom sequence and uniform selection from the remaining pool; resetting reproduces it.

[Figure: Two-dimensional label queries and prototypes](https://ml-biomat.com/tutorials/machine-learning/m11/en/#M11-board)

Pale blue and orange regions follow the current two prototypes; crosses mark averages of revealed examples. Numbers identify samples. Both axes are dimensionless features, not physical image coordinates.

## A few examples, rapid adaptation, and a different environment

After seeing a few photographs of an unfamiliar bird, a person can often identify shared features without relearning vision. Prototype methods use a related procedure: embed the support examples of a class, average them into a class center, then classify a query according to its distance from the centers. The support set defines the categories available in the current task; the query set checks recognition on additional examples. Prototypical Networks, introduced in 2017, trained this structure through collections of small tasks. Here we calculate prototypes on an already trained representation, obtaining 78.33% test accuracy. The example demonstrates distance-based classification; it does not add an episodic prototype-network training stage.

$$
c_k=\frac1{|S_k|}\sum_{i\in S_k}h_i,\qquad p(y=k\mid h)=\frac{\exp(-\|h-c_k\|^2/T)}{\sum_j\exp(-\|h-c_j\|^2/T)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4609563f79194104c68e45e5.svg) | Support indices for class k, their count, and an index in the set; each class has at least one support. |
| ![Formula](https://ml-biomat.com/static/agent-math/eb9d55748d8bb4c809677e9d.svg) | Support embedding, query embedding, and class prototype; dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea1243653251291ec000c74d.svg) | Predicted class, selected class index, and summation index over classes. |
| ![Formula](https://ml-biomat.com/static/agent-math/85a38e0eee398d3b92ce3dea.svg) | Temperature for converting distances to probabilities, and class probability; T has squared-distance units. |

Support points (0,1) and (2,1) average to (1,1). Query (1,0) has squared distance one from this prototype and four from prototype (3,0). At T=1, its first-class probability is 1/(1+exp(−3))≈0.95257. Maximizing probability selects the nearest prototype. The interaction uses two-dimensional teaching points and T=1; the digit experiment selects prototypes in 32 dimensions.

Meta-learning also puts the adaptation process inside the training objective. MAML takes a small parameter update on the support data of each training task, then evaluates the adapted parameters on that task’s query data. The outer update learns an initialization from which those small adjustments work well. Consider three linear tasks with slopes −1, 1, and 3, and a model with one trainable slope. Each support example has input one; each query has input two. Starting from slope zero, one inner update produces slopes −0.5, 0.5, and 1.5. Query errors then push the shared initialization toward one. The code retains the inner update’s computation graph and obtains an outer gradient of −1. An outer learning rate of 0.1 moves the initialization to 0.1.

$$
w^{\prime}_a=w-\alpha\nabla_w\tfrac12(w-a)^2,\qquad J(w)=\frac13\sum_{a\in\{-1,1,3\}}\tfrac12(2w^{\prime}_a-2a)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a286aa7eca10e8b965a0853b.svg) | Shared initial slope, adapted slope for task a, and true task slope; all coordinates and slopes dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/4c587223ad233e42e6a867df.svg) | Inner learning rate and derivative with respect to the initial slope. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d412557ea41f341470c49c0.svg) | Support and query input coordinates; predictions are w and 2w′. |
| ![Formula](https://ml-biomat.com/static/agent-math/246a35cd24461118c16c775e.svg) | Mean query loss across three tasks and its averaging factor. |

The inner derivative is w−a, giving w′=(w+a)/2. Substitution yields query residual 2w′−2a=w−a and loss (w−a)²/2. The mean slope is one, so J′(0)=−1. An outer rate of 0.1 moves w from zero to 0.1. The code uses create_graph=True to preserve dependence through the inner derivative; converting adapted values into ordinary numbers would break this meta-gradient path.

Domain adaptation addresses a different change: category meanings remain related while the input distribution shifts. Components photographed in daylight may look different under dim factory lighting. Measured exposure changes can first be handled by calibration and normalization; more complicated shifts may require learned features. A domain-adversarial model trains a category head and a domain head together. One predicts component category; the other predicts which environment produced the image. Reversing the domain gradient received by the representation network encourages it to discard clues that identify the environment. DANN, introduced in 2015, implemented this opposing pressure through a gradient-reversal layer that fits into ordinary backpropagation.

The choice of what to align matters. If one environment contains only class A and another contains only class B, environment and category are entangled. Removing every domain difference can then erase useful category information. Before adapting, identify source labels, target unlabeled inputs, category correspondences, and validation data available for model selection. Few-shot learning concerns a shortage of answers for a new task; meta-learning concerns how adaptation rules or initializations are learned; domain adaptation concerns changing input distributions. They can occur together, but they imply different task definitions and evaluation splits.

## Why learning something new can erase something old

Deployed systems often receive data over time. Updating parameters as batches arrive is online learning. When categories, environments, or objectives change and earlier abilities must survive, the problem also involves continual learning. Shared parameters support transfer, but new gradients can alter features needed by old tasks. Imagine repeatedly rewriting the same page of notes: a more complete new explanation can make the previous one harder to recover. Forgetting has a direct measurement here. Evaluate an old task, learn a new task, then return to the same old test questions and measure the change.

Our experiment reveals labels for digits zero through four first, then labels for five through nine. Each stage uses 200 updates, and the classification head always has ten outputs. The encoder has already seen every training image without labels, so this experiment focuses on the order in which class labels become available. After stage A, accuracy is 100% on old classes and zero on new classes. Training only on new classes raises new-class accuracy to 95.56%, while old-class accuracy falls to zero. Cross entropy in the new stage raises new-class scores and, through its normalization, pushes against old outputs. Forgetting therefore involves competition at the classifier and changes in shared representations, rather than just the disappearance of a few stroke detectors.

![Old classes 0–4 and new classes 5–9 each have 180 test images. Stage A exposes old-class labels. Both stage-B runs start from the same stage-A model and use 200 updates of 64 images. Replay batches mix 32 new and 32 old images drawn from an 80-image buffer. The matrix reports measured accuracies.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6ab2e03fdd01c246a3f0b851.svg?v=6ab2e03fdd01)

Figure 5Old classes 0–4 and new classes 5–9 each have 180 test images. Stage A exposes old-class labels. Both stage-B runs start from the same stage-A model and use 200 updates of 64 images. Replay batches mix 32 new and 32 old images drawn from an 80-image buffer. The matrix reports measured accuracies.

Replay keeps a small set of earlier experiences in the update stream. We retain 16 images from each old class, 80 images total. During stage B, each batch contains 32 new images and 32 replay images, keeping the total batch size and update count fixed. Old-class accuracy then remains at 90.00%, while new-class accuracy reaches 93.89%. Replay restores old-task contributions to the gradient and allocates some batch positions away from new examples. This is an observable stability–plasticity tradeoff. Larger or more diverse buffers, distillation of an earlier model’s outputs, and constraints on important parameters all change how past knowledge is preserved. A transparent replay baseline makes those more elaborate mechanisms easier to evaluate.

## Turn one dataset into several learning questions

The complete program uses the 1,797 handwriting images bundled with scikit-learn and divides pixel values by 16. Seeds 110 and 111 produce a stratified split of 1,077 training images, 360 validation images, and 360 test images. Representation training runs for a fixed 80 epochs without category labels. Budgets and settings are specified in advance; the validation subset is retained without a hyperparameter search. Five training labels per class are then exposed. Linear probes, prototypes, the pseudo-label diagnostic, and active learning all start from this shared labeled subset. The split randomly partitions existing images rather than grouping them by writer. A study of new-writer generalization would use a writer-level split.

At 50 labels, a linear model on raw pixels reaches 86.67%, the contrastive representation reaches 82.78%, and the random representation reaches 77.50%. Contrastive training improves on these random features without surpassing the simple pixel baseline. The small digit images are already aligned, leaving substantial structure directly readable in their pixels. Our noise and masking objectives also ask the representation to ignore some information. Connecting those results to the augmentation rules and downstream task is more useful than treating pretraining as an automatic improvement. The program saves split indices, query decisions, representations, augmented views, and model parameters so that a changed decision can be traced through the experiment.

### Complete Python: unlabeled representations, annotation budgets, and replay

Requires NumPy, Matplotlib, scikit-learn, and PyTorch. Run python main.py --output results --language en to generate four experimental SVGs, summary.json, model weights, and experiment.npz. The projection head and encoder train for 80 epochs. The meta-gradient is independently derived as −1 and checked by autograd.

```
"""Representation, label budgets, and forgetting: an entirely local CPU experiment.

Data: sklearn digits (E. Alpaydin / C. Kaynak, UCI, CC BY 4.0).
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse, copy, json, platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path('results'))
parser.add_argument('--language',choices=['zh','en'],default='en')
args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
zh=args.language=='zh'
def tr(a,b): return a if zh else b
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5',
 'axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):
 fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)

data=load_digits();X=(data.data/16).astype('float32');y=data.target
train,other=train_test_split(np.arange(len(y)),test_size=720,stratify=y,random_state=110)
val,test=train_test_split(other,test_size=360,stratify=y[other],random_state=111)
xt=torch.tensor(X[train]);yt=torch.tensor(y[train]);xte=torch.tensor(X[test]);yte=y[test]
class Encoder(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,32))
 def forward(self,x): return self.net(x)
class Contrastive(nn.Module):
 def __init__(self):
  super().__init__();self.encoder=Encoder();self.projector=nn.Sequential(nn.Linear(32,32),nn.ReLU(),nn.Linear(32,16))
 def forward(self,x): return F.normalize(self.projector(self.encoder(x)),dim=1)
def augment(x,g):
 noise=.08*torch.randn(x.shape,generator=g)
 visible=torch.rand(x.shape,generator=g)>.15
 return (x+noise).clamp(0,1)*visible
def ntxent(a,b,tau=.2):
 z=torch.cat([a,b]);n=len(a);scores=z@z.T/tau
 scores=scores.masked_fill(torch.eye(2*n,dtype=torch.bool),-1e9)
 target=(torch.arange(2*n)+n)%(2*n)
 return F.cross_entropy(scores,target)
torch.manual_seed(112);model=Contrastive();untrained=copy.deepcopy(model.encoder)
optimizer=torch.optim.Adam(model.parameters(),lr=.001)
g=torch.Generator().manual_seed(113);losses=[]
for epoch in range(80):
 total=0.;order=torch.randperm(len(xt),generator=g)
 for ids in order.split(128):
  a,b=augment(xt[ids],g),augment(xt[ids],g)
  loss=ntxent(model(a),model(b));optimizer.zero_grad();loss.backward();optimizer.step()
  total+=loss.item()*len(ids)
 losses.append(total/len(xt))
model.eval()
with torch.no_grad():
 feat=F.normalize(model.encoder(xt),dim=1).numpy()
 testfeat=F.normalize(model.encoder(xte),dim=1).numpy()
 rawfeat=F.normalize(untrained(xt),dim=1).numpy()
 rawtestfeat=F.normalize(untrained(xte),dim=1).numpy()
rng=np.random.default_rng(114)
initial=np.concatenate([rng.choice(np.where(y[train]==k)[0],5,replace=False) for k in range(10)])
def probe(features,testing,ids):
 clf=LogisticRegression(C=10,max_iter=1500).fit(features[ids],y[train][ids])
 return clf,float(clf.score(testing,yte))
cl,accuracy=probe(feat,testfeat,initial)
_,random_accuracy=probe(rawfeat,rawtestfeat,initial)
_,pixel_accuracy=probe(X[train],X[test],initial)
prototypes=np.stack([feat[initial[y[train][initial]==k]].mean(0) for k in range(10)])
prototype_pred=((testfeat[:,None]-prototypes[None])**2).sum(2).argmin(1)
prototype_accuracy=float((prototype_pred==yte).mean())
pool=np.setdiff1d(np.arange(len(train)),initial)
confidence=cl.predict_proba(feat[pool]);accepted=confidence.max(1)>=.8
pseudo=dict(threshold=.8,count=int(accepted.sum()),correct_fraction=float((cl.predict(feat[pool][accepted])==y[train][pool][accepted]).mean()) if accepted.any() else None)
active={};acquired={}
for policy in ['entropy','random']:
 ids=initial.copy();curve=[];round_ids=[];rg=np.random.default_rng(115)
 for round_index in range(6):
  classifier,score=probe(feat,testfeat,ids);curve.append([len(ids),score])
  if round_index==5:break
  remaining=np.setdiff1d(np.arange(len(train)),ids)
  probabilities=classifier.predict_proba(feat[remaining])
  entropy=-(probabilities*np.log(np.maximum(probabilities,1e-15))).sum(1)
  selected=remaining[np.argsort(-entropy,kind='stable')[:20]] if policy=='entropy' else rg.choice(remaining,20,replace=False)
  round_ids.append(selected);ids=np.r_[ids,selected]
 active[policy]=curve;acquired[policy]=np.array(round_ids)

# Exact differentiable inner update: three tasks y = a*x, each with one support point.
w=torch.tensor(0.,requires_grad=True);outer=[]
for slope in [-1.,1.,3.]:
 support_loss=.5*(w-slope)**2
 inner_grad=torch.autograd.grad(support_loss,w,create_graph=True)[0]
 adapted=w-.5*inner_grad
 outer.append(.5*(2*adapted-2*slope)**2)
meta_loss=torch.stack(outer).mean();meta_gradient=torch.autograd.grad(meta_loss,w)[0].item()

# Class-incremental labels: the encoder has seen every training image without labels.
class Classifier(nn.Module):
 def __init__(self,encoder):
  super().__init__();self.encoder=copy.deepcopy(encoder);self.head=nn.Linear(32,10)
 def forward(self,x): return self.head(self.encoder(x))
torch.manual_seed(116);stage_a=Classifier(model.encoder)
old=np.where(y[train]<5)[0];new=np.where(y[train]>=5)[0]
def fit_steps(net,primary,replay=None,seed=117):
 opt=torch.optim.Adam(net.parameters(),lr=.003);gen=np.random.default_rng(seed)
 net.train()
 for step in range(200):
  ids=gen.choice(primary,64 if replay is None else 32)
  if replay is not None:ids=np.r_[ids,gen.choice(replay,32)]
  loss=F.cross_entropy(net(xt[ids]),yt[ids]);opt.zero_grad();loss.backward();opt.step()
 net.eval()
def task_scores(net):
 with torch.no_grad(): pred=net(xte).argmax(1).numpy()
 return [float((pred[yte<5]==yte[yte<5]).mean()),float((pred[yte>=5]==yte[yte>=5]).mean())]
fit_steps(stage_a,old);continual={'after_A':task_scores(stage_a)}
replay_rng=np.random.default_rng(118)
buffer=np.concatenate([replay_rng.choice(np.where(y[train]==k)[0],16,replace=False) for k in range(5)])
for name,replay in [('new_only',None),('replay',buffer)]:
 net=copy.deepcopy(stage_a);fit_steps(net,new,replay,119);continual[name]=task_scores(net)
 torch.save(net.state_dict(),out/f'continual-{name}.pt')
torch.save(model.state_dict(),out/'contrastive.pt')

gv=torch.Generator().manual_seed(120)
chosen=np.array([np.flatnonzero(y[train]==k)[0] for k in range(10)])
images=xt[chosen];view1=augment(images,gv);view2=augment(images,gv)
fig,axs=plt.subplots(3,10,figsize=(13,4.8),gridspec_kw={'wspace':.03,'hspace':.15})
for row,items in enumerate([images,view1,view2]):
 for col,img in enumerate(items):
  axs[row,col].imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);axs[row,col].set_xticks([]);axs[row,col].set_yticks([])
  if row==0:axs[row,col].set_title(str(col))
 axs[row,0].set_ylabel(tr(['原图','视图 A','视图 B'][row],['Original','View A','View B'][row]))
fig.suptitle(tr('同一张图，两次独立变化：噪声 σ=0.08，遮挡概率 0.15','One image, two independent views: noise σ=0.08; masking probability 0.15'))
save(fig,'views')
with torch.no_grad():
 za,zb=model(view1),model(view2);similarity=(za@zb.T).numpy()
pca=PCA(n_components=2).fit(feat);coords=pca.transform(testfeat)
fig=plt.figure(figsize=(13,7.8));grid=fig.add_gridspec(2,2,width_ratios=[1,1.3],hspace=.4,wspace=.32)
ax=fig.add_subplot(grid[0,0]);ax.plot(np.arange(1,81),losses,color='#125f82',lw=2)
ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('平均 NT-Xent / nats','Mean NT-Xent / nats'),title=tr('A  标签未进入表示训练','A  Representation training sees no labels'))
ax=fig.add_subplot(grid[1,0]);im=ax.imshow(similarity,cmap='viridis',vmin=-1,vmax=1);ax.set(xlabel=tr('视图 B：样本编号','View B: sample index'),ylabel=tr('视图 A：样本编号','View A: sample index'),title=tr('B  对角线是同一原图的配对','B  Diagonal entries are positive pairs'))
fig.colorbar(im,ax=ax,fraction=.045,label=tr('余弦相似度','Cosine similarity'))
ax=fig.add_subplot(grid[:,1]);sc=ax.scatter(coords[:,0],coords[:,1],c=yte,cmap='tab10',s=23,alpha=.8,edgecolors='none')
ax.set(xlabel=tr('主成分 1','Principal component 1'),ylabel=tr('主成分 2','Principal component 2'),title=tr('C  测试表示的二维投影；颜色只用于读图','C  Test representations; labels color the plot only'))
fig.colorbar(sc,ax=ax,ticks=range(10),fraction=.045,label=tr('真实数字','True digit'));save(fig,'representation')
fig,(ax,bar)=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[1.5,1]},layout='constrained')
for policy,color,label in [('entropy','#b85d30',tr('熵选样','Entropy queries')),('random','#125f82',tr('随机选样','Random queries'))]:
 c=np.array(active[policy]);ax.plot(c[:,0],c[:,1],'-o',color=color,lw=2,label=label)
ax.set(xlabel=tr('累计人工标签数','Cumulative human labels'),ylabel=tr('测试准确率','Test accuracy'),ylim=(.5,1),title=tr('A  每轮新增 20 个标签','A  Twenty additional labels per round'));ax.legend()
names=[tr('像素 + 线性','Pixels + linear'),tr('随机表示 + 线性','Random + linear'),tr('对比表示 + 线性','Contrastive + linear'),tr('对比表示 + 原型','Contrastive + prototypes')]
vals=[pixel_accuracy,random_accuracy,accuracy,prototype_accuracy]
bar.barh(names,vals,color=['#a9b2b8','#a9b2b8','#125f82','#b85d30']);bar.set(xlim=(0,1.05),title=tr('B  相同的 50 个标签','B  The same 50 labels'),xlabel=tr('测试准确率','Test accuracy'))
for i,v in enumerate(vals):bar.text(v+.01,i,f'{v:.1%}',va='center',fontsize=10)
save(fig,'labels')
fig,(ax,table)=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.4,1]},layout='constrained')
names=['after_A','new_only','replay'];xx=np.arange(3)
ax.bar(xx-.18,[continual[n][0] for n in names],.36,label=tr('旧类 0–4','Old classes 0–4'),color='#125f82')
ax.bar(xx+.18,[continual[n][1] for n in names],.36,label=tr('新类 5–9','New classes 5–9'),color='#b85d30')
ax.set_xticks(xx,[tr('学完 A','After A'),tr('B：仅新样本','B: new only'),tr('B：加入回放','B: with replay')]);ax.set(ylim=(0,1.12),ylabel=tr('测试准确率','Test accuracy'),title=tr('A  学到新类后，旧知识还在吗？','A  Learning new classes: what survives?'));ax.legend(loc='upper left',fontsize=9)
matrix=np.array([continual[n] for n in names]);im=table.imshow(matrix,vmin=0,vmax=1,cmap='Blues',aspect='auto')
table.set_xticks([0,1],[tr('旧类','Old'),tr('新类','New')]);table.set_yticks(xx,[tr('A 后','After A'),tr('新样本','New only'),tr('80 张回放','80 replay images')]);table.set_title(tr('B  每种方式的实际结果','B  Measured task accuracies'))
for i in range(3):
 for j in range(2):table.text(j,i,f'{matrix[i,j]:.1%}',ha='center',va='center',color='white' if matrix[i,j]>.6 else '#152d3a',fontsize=14)
save(fig,'forgetting')
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__,sklearn=sklearn.__version__),
 splits=dict(train=len(train),validation=len(val),test=len(test)),seed=110,
 contrastive=dict(epochs=80,temperature=.2,batch_size=128,final_loss=losses[-1],encoder_parameters=sum(p.numel() for p in model.encoder.parameters()),projector_parameters=sum(p.numel() for p in model.projector.parameters())),
 probes=dict(contrastive=accuracy,random=random_accuracy,pixels=pixel_accuracy,prototype=prototype_accuracy),
 active=active,pseudo=pseudo,continual=continual,replay_count=len(buffer),
 meta=dict(gradient=meta_gradient,initial=0,inner_rate=.5,outer_rate=.1,updated=-.1*meta_gradient),
 hand=dict(cosine=float(np.dot([.6,.8],[0.,1.])),uniform_three_candidate_loss=float(np.log(3)),masked_mse=float(np.mean((np.array([.3,.6])-np.array([.2,.8]))**2)),prototype=np.mean([[0.,1.],[2.,1.]],axis=0).tolist()))
(out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train_indices=train,val_indices=val,test_indices=test,initial_labels=initial,
 features=feat,test_features=testfeat,pca_coordinates=coords,loss=losses,similarity=similarity,view1=view1.numpy(),view2=view2.numpy(),
 entropy_queries=acquired['entropy'],random_queries=acquired['random'],replay_indices=buffer)
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

After running it, begin with the image contact sheet and check whether augmentation preserves the content you want to recognize. Then inspect paired similarities, compare classifiers at equal label budgets, and examine old and new task scores. Change one design decision at a time: reduce masking, acquire more labels, add diversity to queries, or expand the replay buffer. Each change follows a specific question developed in this chapter: what information should the representation preserve, which questions should a person answer, and how should new knowledge coexist with old knowledge?

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M11.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SimCLR](https://arxiv.org/abs/2002.05709)

   Positive pairs, projection heads, and augmentation.

   Primary paper; figures not copied
2. [UvA Tutorial 17: SimCLR](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial17/SimCLR.html)

   Representation evaluation and the licensed original figure.

   MIT; copyright 2020 Phillip Lippe; original tutorial output figure only
3. [Bootstrap Your Own Latent](https://arxiv.org/abs/2006.07733)

   Online/target networks, moving averages, and stop-gradient.

   Primary paper; figures not copied
4. [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)

   Visible-patch encoding and missing-pixel reconstruction.

   Primary paper; figures not copied
5. [FixMatch](https://arxiv.org/abs/2001.07685)

   Weak/strong augmentations and confidence-filtered pseudo-labels.

   Primary paper; figures not copied
6. [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160)

   Labeling-function coverage, conflicts, and label modeling.

   Primary paper; figures not copied
7. [Prototypical Networks for Few-shot Learning](https://arxiv.org/abs/1703.05175)

   Support prototypes and query distances.

   Primary paper; figures not copied
8. [Model-Agnostic Meta-Learning](https://arxiv.org/abs/1703.03400)

   Inner support updates and outer query objectives.

   Primary paper; figures not copied
9. [Domain-Adversarial Training of Neural Networks](https://arxiv.org/abs/1505.07818)

   Domain adaptation and gradient reversal.

   Primary paper; figures not copied
10. [Experience Replay for Continual Learning](https://arxiv.org/abs/1811.11682)

    Replay mechanisms; the original experiments concern reinforcement learning.

    Primary paper; our digit experiment is independently designed
11. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    Data description and image license.

    CC BY 4.0; E. Alpaydin and C. Kaynak
