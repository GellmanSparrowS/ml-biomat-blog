# Putting a model to work: deployment, compression and monitoring

Source: https://ml-biomat.com/tutorials/machine-learning/m27/en/
Language: en

Follow a digit recognizer through export, real interface calls, compression and canary replay, connecting data, versions, latency and feedback.

## 1 What needs to travel with a trained model?

Imagine building a small application that recognizes handwritten digits. It reads most images correctly in your training program. A colleague connects the model to a web page, and an image suddenly receives a different answer. The weights may be responsible, but the cause may be less conspicuous: one program divides pixel intensities by sixteen and the other divides them again; one flattens the image row by row while the other uses columns; or the request contains strings where numerical values are expected. Deployment concerns this entire route from a real input to a returned answer. For each prediction, we want to identify the version, the transformation applied to the input, the time consumed and the route back to a working version.

A trained network resembles a recipe that has worked in one kitchen. Reproducing the dish elsewhere also requires ingredient specifications, measurement units, equipment and an order of operations. The model supplies computational instructions, the input contract supplies ingredient specifications, and the inference environment supplies equipment. Monitoring helps reveal changes in the ingredients or process. The analogy also separates two objectives: food quality and time to serve. A highly accurate recognizer can still process requests too slowly, while a fast program can consistently return the wrong answer. A useful release therefore connects task quality to the conditions under which people will actually use it.

In 2015, Sculley and colleagues discussed data dependencies, configuration and feedback loops in Hidden Technical Debt in Machine Learning Systems. The 2017 ML Test Score organized questions about data, models, infrastructure and monitoring into a testing framework. The focus extends from an isolated offline score to a system that keeps operating. This chapter makes that development concrete through one experiment: train a digit recognizer, create a reloadable release, export ONNX graphs, call a local HTTP endpoint, and compare compression, response time and changed inputs. Keeping the same images throughout allows differences to be traced to particular operations rather than to unrelated demonstrations.

![Original workflow and historical diagram: fixed data, an ONNX graph containing preprocessing, and operational feedback. Three public studies provide historical context. Routing dots are conceptual.](https://ml-biomat.com/static/tutorials/machine-learning/figures/336b210c341b0bc52f560576.svg?v=336b210c341b)

Figure 1Original workflow and historical diagram: fixed data, an ONNX graph containing preprocessing, and operational feedback. Three public studies provide historical context. Routing dots are conceptual.

MLOps can initially be understood as coordinating data, training, delivery and observation. A personal project already benefits from saving split indices, keeping preprocessing with the model, providing explicit interface examples and retaining a previous release. As collaboration grows, a registry, pipeline and serving platform can take over parts of that work. Their scale can increase gradually. Input definitions, version identity and evaluation criteria are useful from the first working model, because they determine what it means for a later version to reproduce or improve an earlier result.

## 2 Giving every prediction a traceable identity

The experiment uses scikit-learn's bundled digits dataset: 1,797 grayscale images of eight by eight pixels, with intensities from zero to sixteen and ten digit labels. Fixed stratified splits produce 1,077 training images, 270 validation images and 450 test images. Training observations update weights, validation observations select the saved epoch, and test observations compare the resulting configurations. The teacher has sixty-four hidden units; two student networks have sixteen. Each divides raw pixels by sixteen and then applies a linear layer, ReLU and another linear layer. These small dimensions allow the entire release workflow to run on an ordinary CPU.

A manifest accompanies the model files. It records a digest of the data arrays, a digest of the script, all split indices, input shape and units, dependency versions, model-file digests and evaluation results. A digest is a compact identifier computed from the complete bytes of an object. Changing those bytes will ordinarily change the identifier. This answers whether today's file is the file checked yesterday. It does not assess the model's task quality; that requires data definitions and evaluation. File identity, computational behavior and predictive quality are related checks, but each answers its own question.

A model registry manages these relationships across contributors. A fixed version can be associated with training inputs, parameters and evaluation, while an alias such as production or champion points to the version currently intended for a particular use. Updating an alias resembles moving a sign to another room while keeping room numbers fixed. MLflow implements this organization through versions and aliases; ordinary files expose the underlying relationships in our experiment. A prediction returns the identifier digits-v1, and the manifest records the actual model bytes. If behavior changes later, investigation can begin with a concrete release rather than an ambiguous filename such as latest_model.

Reproduction also requires a definition of agreement. Reloading the student's ONNX file produces a maximum output difference of zero across the 450 images. Moving from PyTorch to ONNX Runtime produces a maximum absolute logit difference of approximately 7.63×10⁻⁶. Floating-point operation order and backend implementations can affect rounding, so a numerical comparison commonly combines predetermined absolute and relative tolerances with a comparison of predicted classes. A random seed alone cannot replace this check. Splits, preprocessing, library versions and the saved weights all participate in determining the computation, including details that are easy to overlook when only the training command is recorded.

$$
|a_i-b_i|\le\epsilon_{\rm abs}+\epsilon_{\rm rel}|b_i|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64807847039db96a4a8ce3ac.svg) | Logits for the same image/class from two backends, dimensionless. A batch is B×10; i traverses every element. |
| ![Formula](https://ml-biomat.com/static/agent-math/c5fcad9d6f8a9a1d4ee3d0ec.svg) | Nonnegative absolute and relative tolerances; dimensionless here, with b as reference. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | Absolute value measures magnitude independently of the sign. |

Absolute tolerance handles values near zero; relative tolerance follows the reference scale. For b=2 and both tolerances 10⁻⁵, the allowed difference is 3×10⁻⁵; a=2.00002 passes. Check every array element and then compare classes.

A practical release also includes a repeatable entry point and representative input-output pairs. The complete program starts from the bundled digits, saves all splits and models, and checks class decisions, numerical behavior and file identity. Once the files exist, inference can load ONNX directly without repeating training. The training and inference environments can consequently be maintained separately. The latter needs the graph execution and request-handling components; it does not need to reproduce every tool used to optimize the network.

## 3 An interface is a shared agreement about the data

An interface establishes expectations on both sides of a call. Our endpoint accepts a JSON object containing one field, pixels. Its value is a two-dimensional array with one to 256 rows and exactly sixty-four numerical entries per row. Those entries follow the row-major order of an eight-by-eight image and represent raw, unnormalized intensities. Values must be finite and within zero to sixteen. The response contains a version, one predicted class per image and ten logits per image. Logits are scores before normalization; their interpretation as probabilities additionally involves softmax and, when needed, calibration.

$$
X=P/16,\qquad H=\operatorname{ReLU}(XW_1+\mathbf b_1),\qquad Z=HW_2+\mathbf b_2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e034ee6fc2f7c49c91499907.svg) | Raw intensity and normalized input, shape B×64. P uses the 0–16 intensity scale; X is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/2a43927f8ea27ee9dedf59dd.svg) | B is batch size; H is B×h hidden activation and Z is B×10 logits, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a57aa09f24b92830de67d596.svg) | Weights and biases of shapes 64×h, h, h×10,10. Teacher h=64 and student h=16; entries are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dfc64c58afee6ca11adda4a.svg) | ReLU applies max(0, x) elementwise; 16 is the raw-intensity full scale. Biases broadcast across the batch. |

An intensity 8 becomes 0.5. With a single weight 2 and bias −0.2, the hidden activation is max(0,0.5×2−0.2)=0.8. Dividing before the call and again inside the graph instead maps 8 to 0.03125.

These details determine where every number in the model's mathematical expression comes from. Correct shape does not ensure correct units. An image already scaled to zero through one still lies inside the allowed zero-through-sixteen interval, so a range check accepts it. If the inference graph divides by sixteen again, its inputs have now been scaled by a total factor of 256. In this experiment, double normalization reduces accuracy from 96.22% to 34.22%. An input contract therefore combines executable shape and range checks with examples that state units and processing order, plus comparisons of the complete outputs for fixed representative inputs.

The program starts a temporary HTTP server bound to the local machine, sends seven requests and closes the server. A legitimate two-image request receives status 200. Incorrect column count, out-of-range values, text, a nonfinite value, an empty batch and an incorrect field name each receive status 400. A successful status indicates that the request completed the agreed computation. Whether the predicted digit is correct is assessed separately against its label. Interface error rates reveal transport and contract problems, classification errors describe the task, and response times describe how long the caller waits. Combining all three into a single success number would obscure where a problem originates.

Batch, online and edge inference can use the same graph under different operating conditions. An overnight job can accumulate many images and amortize loading and invocation costs. An interactive application must respond to individual requests, and time spent waiting for a full batch contributes to user-visible latency. A phone or sensor additionally has memory, energy, network and supported-operator constraints. Begin by specifying how often inputs arrive, when answers are needed and which data should remain on the device. Batch size and serving architecture can then be selected to match those requirements.

## 4 Exporting a graph whose steps can be inspected

ONNX represents computation through tensors, operators and their connections. Think of it as the worked steps of a calculation: pixels enter a Div node for scaling, pass through matrix multiplication and bias addition, then through ReLU and another linear transformation to produce ten scores. The example constructs these nodes explicitly with the ONNX helper API, allowing every shape to be checked. The batch dimension is symbolic, so the same file accepts one or 128 images. The feature dimension remains fixed at sixty-four because it describes a particular input representation rather than an arbitrary quantity that can change between calls.

Placing preprocessing inside the graph ensures that each backend receives raw pixels and applies the same division. If scaling remained only in the training script while the release contained linear-layer weights, part of the computation would be missing from the artifact. A graph checker inspects connections, types and operator conventions; an execution provider then implements the supported operations. Here CPU execution is selected explicitly and inference thread counts are fixed to one. More complicated models may have dynamic branches, custom operators or several supported shape ranges. Representative export checks should exercise those routes instead of relying on a single convenient input.

Graph validity, successful execution and agreement with the original model are successive questions. We first run the ONNX checker, compare ONNX and PyTorch logits on all 450 images, and finally reload from disk and compare again. This resembles checking a circuit diagram, powering up a prototype and checking the assembled device. Identical predicted classes are useful evidence, but scores deserve attention as well: an input near a decision boundary may change class after a small numerical perturbation. Predetermined tolerances and representative inputs give that comparison an explicit meaning.

The experiment retains another useful result: omitting normalization happens to produce the same aggregate accuracy of 96.22%, yet the maximum logit difference is about 483.77. In a largely ReLU-based network, a global change in scale can preserve many class orderings while greatly changing score magnitudes. This explains why a release check includes numerical behavior alongside task metrics. One unchanged accuracy value does not describe the entire computation. Quantization follows the same sequence in the next section: measure output differences, inspect class changes, and then examine resource use.

## 5 Several ways to make the same task smaller

Compression acts on different parts of a model. Distillation transfers output relationships from a larger network to a smaller one. Pruning removes the influence of some connections. Quantization stores parameters on a coarser numerical grid. They can be combined, but their mechanisms should remain distinguishable. Hinton, Vinyals and Dean's 2015 distillation paper emphasized information in a teacher's complete output distribution. A blurred three might also resemble an eight. That relationship can guide the student, whereas a single hard label supplies only the answer three. Temperature controls how clearly such secondary relationships appear in the target distribution.

$$
p^{(T)}_j=\frac{e^{z^{\rm teacher}_j/T}}{\sum_k e^{z^{\rm teacher}_k/T}},\quad q^{(T)}_j=\frac{e^{z^{\rm student}_j/T}}{\sum_k e^{z^{\rm student}_k/T}},\quad \mathcal L=\alpha(-\log q_y^{(1)})+(1-\alpha)T^2\sum_j p_j^{(T)}\log\frac{p_j^{(T)}}{q_j^{(T)}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c671ba92b071f80f71d8772.svg) | j and k range over ten classes; y is the true-class index, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3f7a856793a46b4d4b0ff2ab.svg) | Teacher/student ten-dimensional logits and temperature-softened probabilities; teacher outputs are fixed during student training. |
| ![Formula](https://ml-biomat.com/static/agent-math/11b913c202121dc8431c2214.svg) | Positive temperature and hard-label loss weight; T=3 and alpha=0.4 here, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/10b2710f583efc874c9bdc82.svg) | Per-example objective, averaged across the batch; natural logarithms give nats. T² compensates for temperature-related gradient scaling. |

Teacher logits (2,0) give probabilities about (0.881,0.119) at T=1 and (0.731,0.269) at T=2. The secondary class becomes more visible. Matching teacher probabilities makes the KL term zero; the hard-label term still rewards the true answer.

The teacher here has 4,810 parameters, and each student has 1,210. One student learns only the true labels. The other uses temperature three and combines hard-label cross entropy and the teacher's soft target with weights 0.4 and 0.6. Both students begin with the same initialization and receive 300 training epochs, selecting their own saved epoch by validation cross entropy. The teacher reaches 97.11% test accuracy; both students reach 96.22%. The example demonstrates actual distillation while retaining a run in which it does not improve the final accuracy. Teacher quality, student capacity, objective weighting and optimization time all affect what the student can learn.

Pruning starts from the distilled student and zeros the half of its matrix weights with the smallest absolute values. This removes 592 weights while leaving biases unchanged, and it is followed by no extra fine-tuning. Accuracy becomes 95.11%. A weight image shows the removed connections directly. The ONNX file remains 5,146 bytes because the graph still contains dense matrices of the original dimensions, including stored floating-point zeros. Reducing arithmetic or memory traffic requires an execution path that exploits the sparse representation, or structured removal of entire channels together with corresponding changes in the following layer.

$$
s_j=\max_i|W_{ij}|/127,\quad Q_{ij}=\operatorname{clip}(\operatorname{round}(W_{ij}/s_j),-127,127),\quad \widehat W_{ij}=s_j(Q_{ij}-0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a897ff986da9ea876108627a.svg) | Original and reconstructed weight; i indexes inputs and j output channels. Weights are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/fa530fa6ab8c96f5457e2164.svg) | Positive per-output-channel scale and signed 8-bit integer; an all-zero channel uses a tiny positive scale to avoid division by zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/23d65448edb24bc1c870044f.svg) | Round to integer with NumPy ties-to-even; clamp to the given interval; symmetric quantization uses zero point 0. |

If a channel maximum is 1.27, its scale is 0.01. Weight 0.026 maps to integer 3 and reconstructs as 0.03, an error of 0.004. Separate channel scales allow small-amplitude channels to use the available integer levels.

The quantized variant uses symmetric eight-bit weight storage separately for each output channel. The largest absolute weight determines the channel's scale, and values are rounded to integer levels from minus 127 through 127. DequantizeLinear nodes carry the integer tensors, scales and zero points back to floating-point weights. Activations remain float 32, so this is W8A32 storage. The file falls from 5,146 to 1,922 bytes, a reduction of approximately 62.65%. All 450 predicted classes remain unchanged, although the maximum logit difference is 0.365. Numerical error and discrete decisions offer complementary views of the same approximation.

![Left: cross entropy on the same validation set. Middle: actual ONNX bytes and 450-image accuracy; hard and student overlap. Right: original/pruned first-layer weights with a shared scale. The 50% pruning fraction applies across both matrices together.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e244137d4be86c21594e8025.svg?v=e244137d4be8)

Figure 2Left: cross entropy on the same validation set. Middle: actual ONNX bytes and 450-image accuracy; hard and student overlap. Right: original/pruned first-layer weights with a shared scale. The 50% pruning fraction applies across both matrices together.

Static activation quantization additionally needs representative calibration inputs to determine ranges. Dynamic quantization estimates some ranges during execution, while quantization-aware training includes the effect of rounding in learning. The execution provider determines how those representations become operations. Our graph explicitly dequantizes weights and retains floating-point activations; a runtime may fold constant dequantization back into floating-point matrices. The experiment therefore demonstrates compressed weight storage. Runtime memory, integer-kernel use and speed are separate measurements. Keeping these quantities distinct makes it possible to connect a smaller file, fewer operations and faster responses to their actual mechanisms.

## 6 Measuring the wait rather than counting parameters

A café receiving ten orders may prepare them together and reduce average work per drink, while making the first customer wait longer. Inference has a similar batching trade-off. Throughput counts samples completed per unit time; latency measures the duration of an invocation. Queueing, request parsing, transfer and model computation together determine the delay experienced by a caller. For a very small network, invocation and scheduling overhead can be substantial relative to matrix multiplication. A fourfold reduction in parameter count consequently does not imply a fourfold reduction in single-request latency.

$$
\text{throughput}=\frac{B}{\operatorname{median}(t_1,\ldots,t_R)},\qquad t_{95}=\operatorname{quantile}_{0.95}(t_1,\ldots,t_R)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5230febb20293ad37084280.svg) | Images in a call and repeat count; B is 1/32/128 and R=120. |
| ![Formula](https://ml-biomat.com/static/agent-math/c17639b1b0d2032abf884074.svg) | Duration of repeat r and 95th-percentile duration; seconds in this formula, milliseconds in the figure. |
| ![Formula](https://ml-biomat.com/static/agent-math/99e21cc7739fc3403e487912.svg) | Median and NumPy default linearly interpolated quantile; throughput is images per second. |

A batch of 32 taking a median 0.002 seconds gives 16000 images/second. For sorted times(1,1,2,2,4)ms, the interpolated p95 lies 80% from the fourth to fifth value, giving 3.6 ms. Record the quantile convention.

Each ONNX variant is measured at batch sizes one,32 and 128. A configuration receives twenty warm-up calls followed by 120 timed calls, with its inputs already in memory and one inference thread. The left panel displays the entire empirical distribution of single-image call times. The right panel divides batch size by median call duration to obtain throughput. The measurement boundary surrounds the ONNX Runtime call, excluding HTTP parsing and queueing. Readers can move that boundary outward to include a full request and compare pure inference with end-to-end waiting time under the same workload.

![Bilingual plots from one run: 20 warmups and 120 measurements/configuration, CPU, single-thread. Left: empirical single-image call times. Right: batch size divided by median duration. ONNX invocation overhead is included; input loading, HTTP and queueing are outside the boundary.](https://ml-biomat.com/static/tutorials/machine-learning/figures/67b1be677d0ffed7e2b41b80.svg?v=67b1be677d0f)

Figure 3Bilingual plots from one run: 20 warmups and 120 measurements/configuration, CPU, single-thread. Left: empirical single-image call times. Right: batch size divided by median duration. ONNX invocation overhead is included; input loading, HTTP and queueing are outside the boundary.

The 95th percentile is a time at or below which 95% of observed calls finish. It describes the slower end of experience rather than only the center. A service with a small average can still occasionally make users wait. For our short CPU calls, background activity, caches and timer resolution affect the distribution, so repeated measurements are retained. The quantized artifact also does not automatically gain lower latency from its smaller size. Dequantization, operator fusion and invocation costs contribute to execution. Moving to another device or provider calls for another measurement with the same inputs and batch definitions.

Cost can be evaluated using an equally explicit boundary. Device time, utilization, storage and transfer contribute to the cost of a completed request. Peak throughput is not average daily utilization, and an idle provisioned device can still incur costs. An edge application also needs model loading time, sustained device temperature and battery use. A useful comparison places task quality beside file size, working memory, throughput and tail latency. Application requirements then decide which of these quantities matters most, rather than asking parameter count to represent every resource consideration.

## 7 A stable statistic can conceal a changed task

Monitoring begins with the contract: are fields missing, values out of range or image dimensions changing? It can then track feature distributions, such as the mean intensity of each image. We use training images as the reference and divide mean intensity into fixed intervals. The population stability index, PSI, combines changes in interval frequencies into one number. Each bin receives a smoothing count of 0.5 before the two histograms are normalized separately, avoiding an undefined logarithm for an empty bin. Bin boundaries and smoothing belong in the recorded definition because they affect the value being compared.

$$
p_k=\frac{n_k+a}{N+Ka},\quad q_k=\frac{m_k+a}{M+Ka},\qquad \operatorname{PSI}=\sum_{k=1}^{K}(q_k-p_k)\log(q_k/p_k)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e5f01e3334ca6eea7725b3d8.svg) | Bin index and number of bins; sixteen width-one bins cover 0–16 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/96c0c6e9a14b9316d52b1df6.svg) | Reference/current bin counts and group totals; N=1077 and M=450 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d3f9077282c047751278416.svg) | Pseudocount a=0.5 per bin and normalized reference/current proportions; proportions and PSI are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e8695a3f226258d2bce68824.svg) | Natural logarithm and summation of binwise contributions. |

Identical normalized proportions make every term zero. For p=(0.5,0.5) and q=(0.75,0.25), PSI=0.25log(1.5)−0.25log(0.5)≈0.27465. It describes only the chosen feature histogram.

Three groups contain 450 images each: original test images, images with half their intensity, and images rotated through 90 degrees. Dimming moves the brightness distribution substantially, giving PSI about 12.11, while accuracy changes from 96.22% to 95.56%. Rotation preserves every pixel value and changes only its position, so each image's mean intensity and the resulting PSI are exactly the same as for the originals. Accuracy nevertheless drops to 9.33%. One transformation is conspicuous in the selected statistic and has a modest task effect; the other is invisible to that statistic and alters the spatial structure on which the model relies.

![Three groups of 450: original, half-intensity and 90-degree rotation. Top: the same example with grayscale 0–16. Original solid and rotated dashed brightness histograms overlap below, while their accuracies differ markedly.](https://ml-biomat.com/static/tutorials/machine-learning/figures/bffeb336eb3d7330a7188c10.svg?v=bffeb336eb3d)

Figure 4Three groups of 450: original, half-intensity and 90-degree rotation. Top: the same example with grayscale 0–16. Original solid and rotated dashed brightness histograms overlap below, while their accuracies differ markedly.

This comparison distinguishes changes in data, changes in conditional relationships and degradation of the task. Input drift concerns the distribution of observed features. If the relationship between an input and its answer changes, the problem also involves the conditional target distribution. Input-only observations can reveal many formatting, equipment and acquisition changes quickly. Accuracy, group-specific errors and realized decision costs become measurable when labels arrive. For equipment lifetime or repayment outcomes, that delay may be long. A monitoring view should report how many labels have returned and which period they cover, so an absence of observed mistakes is not confused with evidence about unobserved outcomes.

An alert threshold depends on ordinary variation, sample size and the consequences of investigation. PSI has no universal threshold shared by every task: binning, features and reference samples affect its magnitude. After a signal appears, continue through input groups and release identity. Did image orientation change? Did one digit become more frequent? Is a candidate worse on a particular group? Collecting representative labels and reevaluating affected groups can lead to a targeted change in preprocessing, calibration or training. This connects a monitoring signal to a concrete next experiment.

## 8 Replacing a version gradually and learning from feedback

After offline evaluation, a shadow deployment can process the same requests with a candidate while the existing version continues to supply answers. A canary release then assigns some requests to the candidate and expands that share progressively. Rollback routes subsequent requests back to a retained version. These operations address different stages: shadowing compares computations, a canary observes behavior after the candidate enters the actual workflow, and rollback shortens further exposure to a problematic release. Previously issued answers and any downstream actions still require their own records and handling; changing the route does not erase that history.

The interactive replay treats 450 fixed test images as sequential requests arriving in batches of 50. The teacher is the existing version. Candidates include the student, its eight-bit-weight variant, the pruned version and a double-normalization variant. A fixed request-number rule determines routing, while the traffic fraction controls which subsequent requests enter the candidate. Label delay determines when recent answers become observable. Advance traffic, wait for labels and compare candidate and existing-model errors on the same labeled candidate requests. Every prediction comes from the real run above; the browser replays these outputs without retraining a network.

### Replay a canary release with actual predictions

Each batch contains 50 images; the teacher is the existing version. Traffic-share changes affect future requests. Changing candidate or label delay starts a new experiment. Process batches, then roll back and observe how history and future routing differ.

[Figure: Actual request routing and delayed-label replay](https://ml-biomat.com/tutorials/machine-learning/m27/en/#M27-plot)

The replay makes evaluation definitions visible. A single error can move the rate sharply when few candidate requests have labels. Before labels return, request and execution status are the available observations. After rollback, future requests use the existing version while earlier results remain displayed. A production experiment must also match allocation to users, repeated visits and feedback: persistent user-level assignment may be more appropriate than request-level routing. An evaluation window and stopping rule help separate an actionable comparison from repeated reactions to random fluctuations as results accumulate.

Continuous training returns newly collected observations to a training workflow. Continual learning additionally concerns how a model absorbs new information while retaining earlier capabilities. Both need evaluation designed around the update: check new labels, separate training from evaluation by time or relevant groups, and assess new conditions alongside important old ones. Recommendation systems make the feedback connection especially visible because model choices determine exposure, and exposure influences the clicks available for later learning. Appropriate exploration, exposure records and independent evaluation help the next experiment understand how its training observations came into existence.

### Complete program from training to local inference

Install numpy, torch, onnx, onnxruntime, scikit-learn and matplotlib. Run python main.py --output results --language en. Then python main.py --serve results --port 8765 starts the local /predict endpoint; send a two-dimensional pixels array and stop with Ctrl+C. The experiment closes its temporary contract-check server itself.

```
"""A complete local model release: training, compression, ONNX, HTTP and monitoring.
Run: python main.py --output results --language en
Serve a previously generated bundle: python main.py --serve results --port 8765
"""
from pathlib import Path
import argparse, copy, hashlib, importlib.metadata, json, platform, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen, build_opener, ProxyHandler
from urllib.error import HTTPError
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import onnx
from onnx import helper, numpy_helper, TensorProto
import onnxruntime as ort
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Network(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.fc1 = nn.Linear(64, width)
        self.fc2 = nn.Linear(width, 10)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


def fit(width, x, y, xv, yv, teacher=None):
    torch.manual_seed(270 + width)
    model = Network(width)
    optimizer = torch.optim.Adam(model.parameters(), lr=.01)
    history, best, chosen = [], float('inf'), 0
    teacher_logits = None if teacher is None else teacher(x).detach()
    for epoch in range(300):
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        if teacher is not None:
            temperature = 3.
            soft = F.kl_div(F.log_softmax(logits / temperature, dim=1),
                            F.softmax(teacher_logits / temperature, dim=1), reduction='batchmean')
            loss = .4 * loss + .6 * temperature ** 2 * soft
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        with torch.no_grad():
            validation = F.cross_entropy(model(xv), yv).item()
        history.append([float(loss.detach()), validation])
        if validation < best:
            best, chosen, state = validation, epoch + 1, copy.deepcopy(model.state_dict())
    model.load_state_dict(state); model.eval()
    return model, np.array(history), chosen


def export_graph(model, path):
    # The raw-pixel /16 transform travels inside the inference graph.
    arrays = {'scale': np.array(16, dtype=np.float32),
              'w1': model.fc1.weight.detach().numpy().T.copy(),
              'b1': model.fc1.bias.detach().numpy(),
              'w2': model.fc2.weight.detach().numpy().T.copy(),
              'b2': model.fc2.bias.detach().numpy()}
    nodes = [helper.make_node('Div', ['pixels', 'scale'], ['scaled']),
             helper.make_node('MatMul', ['scaled', 'w1'], ['m1']),
             helper.make_node('Add', ['m1', 'b1'], ['a1']),
             helper.make_node('Relu', ['a1'], ['hidden']),
             helper.make_node('MatMul', ['hidden', 'w2'], ['m2']),
             helper.make_node('Add', ['m2', 'b2'], ['logits'])]
    graph = helper.make_graph(nodes, 'digits-release',
        [helper.make_tensor_value_info('pixels', TensorProto.FLOAT, ['batch', 64])],
        [helper.make_tensor_value_info('logits', TensorProto.FLOAT, ['batch', 10])],
        [numpy_helper.from_array(v, name=k) for k, v in arrays.items()])
    model_proto = helper.make_model(graph, opset_imports=[helper.make_opsetid('', 18)])
    model_proto.ir_version = 10
    onnx.checker.check_model(model_proto)
    onnx.save(model_proto, path)


def session(path):
    settings = ort.SessionOptions()
    settings.intra_op_num_threads = 1; settings.inter_op_num_threads = 1
    return ort.InferenceSession(str(path), settings, providers=['CPUExecutionProvider'])


def quantize_weights(source, destination):
    """Store signed8-bit weights per output channel, with explicit dequantization.

    Activations remain float32; this graph demonstrates W8A32 storage.
    Execution providers may fold constant dequantization back into float matrices.
    """
    graph_model = onnx.load(source)
    additions, replacements = [], []
    for tensor in list(graph_model.graph.initializer):
        if tensor.name not in ['w1', 'w2']:
            continue
        weight = numpy_helper.to_array(tensor)
        scale = np.maximum(np.abs(weight).max(axis=0) / 127, 1e-12).astype(np.float32)
        quantized = np.clip(np.rint(weight / scale), -127, 127).astype(np.int8)
        name = tensor.name
        replacements.extend([numpy_helper.from_array(quantized, name + '_q'),
                             numpy_helper.from_array(scale, name + '_scale'),
                             numpy_helper.from_array(np.zeros(scale.shape, np.int8), name + '_zero')])
        additions.append(helper.make_node('DequantizeLinear',
                         [name + '_q', name + '_scale', name + '_zero'], [name], axis=1))
        graph_model.graph.initializer.remove(tensor)
    graph_model.graph.initializer.extend(replacements)
    original_nodes = list(graph_model.graph.node)
    del graph_model.graph.node[:]
    graph_model.graph.node.extend(additions + original_nodes)
    onnx.checker.check_model(graph_model)
    onnx.save(graph_model, destination)


def predict(sess, payload):
    if not isinstance(payload, dict) or set(payload) != {'pixels'}:
        raise ValueError('Expected one field: pixels')
    raw = np.asarray(payload['pixels'])
    if raw.ndim != 2 or raw.shape[1] != 64 or not 1 <= raw.shape[0] <= 256:
        raise ValueError('pixels must have shape [1..256,64]')
    if raw.dtype.kind not in 'fiu' or not np.isfinite(raw).all():
        raise ValueError('pixels must contain finite numbers')
    if raw.min() < 0 or raw.max() > 16:
        raise ValueError('Raw pixel range is 0..16')
    logits = sess.run(None, {'pixels': raw.astype(np.float32)})[0]
    return {'version': 'digits-v1', 'classes': logits.argmax(1).tolist(),
            'logits': logits.tolist()}


def handler(sess):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # No request features are written to a log.

        def do_POST(self):
            try:
                if self.path != '/predict':
                    self.send_error(404); return
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 1000000:
                    raise ValueError('Invalid request size')
                result = predict(sess, json.loads(self.rfile.read(length)))
                code = 200
            except (ValueError, TypeError, OverflowError):
                result, code = {'error': 'Request does not match the pixel contract'}, 400
            data = json.dumps(result, allow_nan=False).encode()
            self.send_response(code); self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
    return Handler


def http_checks(sess, sample):
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler(sess))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    client = build_opener(ProxyHandler({})); records = []
    payloads = [{'pixels': sample.tolist()}, {'pixels': [[0] * 63]},
                {'pixels': [[17] * 64]}, {'pixels': [['zero'] * 64]},
                {'pixels': [[float('nan')] * 64]}, {'pixels': []}, {'image': sample.tolist()}]
    try:
        for payload in payloads:
            request = Request(f'http://127.0.0.1:{server.server_port}/predict',
                              json.dumps(payload).encode(), {'Content-Type': 'application/json'})
            try:
                with client.open(request, timeout=10) as response:
                    code, body = response.status, json.loads(response.read())
            except HTTPError as error:
                code, body = error.code, json.loads(error.read())
            records.append({'status': code, 'body': body})
    finally:
        server.shutdown(); server.server_close(); thread.join()
    assert [r['status'] for r in records] == [200, 400, 400, 400, 400, 400, 400]
    assert records[0]['body']['classes'] == predict(sess, payloads[0])['classes']
    return records


def psi(reference, current, edges):
    p = np.histogram(reference, edges)[0].astype(float) + .5
    q = np.histogram(current, edges)[0].astype(float) + .5
    p /= p.sum(); q /= q.sum()
    return float(np.sum((q - p) * np.log(q / p)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results')
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    parser.add_argument('--serve', type=Path); parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if args.serve:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler(session(args.serve / 'student.onnx')))
        print(f'Local prediction endpoint: http://127.0.0.1:{args.port}/predict', flush=True)
        try: server.serve_forever()
        except KeyboardInterrupt: pass
        finally: server.server_close()
        return
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'; tr = lambda z, e: z if zh else e
    torch.set_num_threads(1); torch.manual_seed(271); np.random.seed(271)
    data = load_digits(); pixels = data.data.astype(np.float32); labels = data.target
    development, test = train_test_split(np.arange(len(labels)), test_size=450, stratify=labels, random_state=271)
    train, validation = train_test_split(development, test_size=270, stratify=labels[development], random_state=272)
    tensor = lambda ids: torch.from_numpy(pixels[ids] / 16)
    target = lambda ids: torch.from_numpy(labels[ids])
    teacher, ht, et = fit(64, tensor(train), target(train), tensor(validation), target(validation))
    hard, hh, eh = fit(16, tensor(train), target(train), tensor(validation), target(validation))
    student, hs, es = fit(16, tensor(train), target(train), tensor(validation), target(validation), teacher)
    pruned = copy.deepcopy(student)
    weights = torch.cat([pruned.fc1.weight.flatten(), pruned.fc2.weight.flatten()])
    threshold = torch.quantile(weights.abs(), .5)
    with torch.no_grad():
        for layer in [pruned.fc1, pruned.fc2]: layer.weight.mul_(layer.weight.abs() > threshold)
    models = {'teacher': teacher, 'hard': hard, 'student': student, 'pruned': pruned}
    for name, model in models.items():
        export_graph(model, out / f'{name}.onnx')
        torch.save(model.state_dict(), out / f'{name}.pt')
    quantize_weights(out / 'student.onnx', out / 'int8.onnx')
    sessions = {name: session(out / f'{name}.onnx') for name in [*models, 'int8']}
    raw = pixels[test]; truth = labels[test]
    logits = {name: sess.run(None, {'pixels': raw})[0] for name, sess in sessions.items()}
    with torch.no_grad():
        export_error = float(np.abs(logits['student'] - student(tensor(test)).numpy()).max())
        logits['wrong_scale'] = student(torch.from_numpy(raw)).numpy()
    logits['double_scale'] = sessions['student'].run(None, {'pixels': raw / 16})[0]
    predictions = {name: value.argmax(1) for name, value in logits.items()}
    accuracy = {name: float((prediction == truth).mean()) for name, prediction in predictions.items()}
    timings = {}
    for name, sess in sessions.items():
        timings[name] = {}
        for batch in [1, 32, 128]:
            feed = {'pixels': raw[:batch]}
            for _ in range(20): sess.run(None, feed)
            elapsed = []
            for _ in range(120):
                start = time.perf_counter_ns(); sess.run(None, feed)
                elapsed.append((time.perf_counter_ns() - start) / 1e6)
            timings[name][str(batch)] = elapsed
    contracts = http_checks(sessions['student'], raw[:2])
    # Rotation preserves each image's mean brightness exactly but changes its geometry.
    streams = {'clean': raw, 'dimmed': raw * .5,
               'rotated': np.rot90(raw.reshape(-1, 8, 8), k=1, axes=(1, 2)).reshape(-1, 64).copy()}
    edges = np.linspace(0, 16, 17); baseline = pixels[train].mean(1)
    drift = {}
    for name, value in streams.items():
        pred = sessions['student'].run(None, {'pixels': value})[0].argmax(1)
        drift[name] = {'psi_mean_brightness': psi(baseline, value.mean(1), edges),
                       'accuracy': float((pred == truth).mean())}
    model_files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.onnx')}
    manifest = {'version': 'digits-v1', 'data_sha256': hashlib.sha256(pixels.tobytes() + labels.tobytes()).hexdigest(),
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'split': {'train': train.tolist(), 'validation': validation.tolist(), 'test': test.tolist()},
                'schema': {'field': 'pixels', 'shape': ['batch<=256', 64], 'range': [0, 16],
                           'order': '8x8 row-major', 'transform': 'divide by16 inside ONNX'},
                'versions': {n: importlib.metadata.version(n) for n in ['numpy', 'torch', 'onnx', 'onnxruntime', 'scikit-learn']},
                'python': platform.python_version(), 'models': model_files, 'evaluation': accuracy}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
    # Reload from the written file and verify both identity and prediction parity.
    restored = json.loads((out / 'manifest.json').read_text(encoding='utf8'))
    for name, expected in restored['models'].items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == expected
    replay = session(out / 'student.onnx').run(None, {'pixels': raw})[0]
    reload_error = float(np.abs(replay - logits['student']).max())
    summary = {'samples': len(labels), 'train': len(train), 'validation': len(validation), 'test': len(test),
        'selected_epochs': {'teacher': et, 'hard': eh, 'student': es}, 'accuracy': accuracy,
        'onnx_max_logit_error': export_error, 'reload_error': reload_error,
        'int8_max_logit_error': float(np.abs(logits['int8'] - logits['student']).max()),
        'wrong_scale_max_logit_error': float(np.abs(logits['wrong_scale'] - logits['student']).max()),
        'int8_changed_predictions': int(np.count_nonzero(predictions['int8'] != predictions['student'])),
        'parameters': {name: sum(p.numel() for p in model.parameters()) for name, model in models.items()},
        'pruned_weight_zeros': sum(int((layer.weight == 0).sum()) for layer in [pruned.fc1, pruned.fc2]),
        'total_weights': len(weights), 'onnx_bytes': {name: (out / f'{name}.onnx').stat().st_size for name in sessions},
        'contract_statuses': [r['status'] for r in contracts], 'monitoring': drift,
        'timing_ms': {name: {batch: {'median': float(np.median(t)), 'p95': float(np.quantile(t, .95)),
                       'throughput': int(batch) * 1000 / float(np.median(t))} for batch, t in values.items()} for name, values in timings.items()}}
    np.savez_compressed(out / 'experiment.npz', train=train, validation=validation, test=test, labels=truth,
                        pixels=raw, teacher_history=ht, hard_history=hh, student_history=hs,
                        **{'logits_' + k: v for k, v in logits.items()},
                        **{'timing_' + k + '_' + b: np.array(t) for k, a in timings.items() for b, t in a.items()})
    (out / 'replay.json').write_text(json.dumps({'labels': truth.tolist(), 'predictions': {k: v.tolist() for k, v in predictions.items()}}), encoding='utf8')
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    for language in ['zh', 'en']:
        zh = language == 'zh'
        plt.rcParams.update({'font.family': ['Microsoft YaHei', 'DejaVu Sans'], 'font.size': 11,
                             'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False,
                             'figure.facecolor': '#faf8f3', 'axes.facecolor': '#faf8f3'})
        colors = ['#1b4660', '#897d68', '#1c8282', '#bd7049', '#77649b']
        def save(fig, name):
            fig.savefig(out / f'{name}-{language}.svg', bbox_inches='tight')
            fig.savefig(out / f'{name}-{language}.png', dpi=150, bbox_inches='tight'); plt.close(fig)
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), layout='constrained')
        for h, name, color in zip([ht, hh, hs], ['teacher', 'hard', 'student'], colors):
            axes[0].plot(np.arange(1, 301), h[:, 1], label=name, color=color)
        axes[0].set(xlabel=tr('训练轮数', 'Training epoch'), ylabel=tr('验证交叉熵 / nats', 'Validation cross entropy / nats')); axes[0].legend(frameon=False)
        for i, name in enumerate(sessions):
            axes[1].scatter(summary['onnx_bytes'][name] / 1024, accuracy[name], s=70, color=colors[i])
            if name != 'student':
                offsets = {'teacher': (-35, 14), 'hard': (-35, 22), 'pruned': (-20, -24), 'int8': (0, 14)}
                axes[1].annotate('hard / student' if name == 'hard' else name, (summary['onnx_bytes'][name] / 1024, accuracy[name]), xytext=offsets[name], textcoords='offset points', arrowprops={'arrowstyle': '-', 'color': '#7c898e'})
        axes[1].set(xscale='log', xlabel=tr('ONNX文件 / KiB', 'ONNX file / KiB'), ylabel=tr('450张测试准确率', 'Accuracy on 450 test images'), ylim=(.93, 1.005))
        original = student.fc1.weight.detach().numpy(); sparse = pruned.fc1.weight.detach().numpy()
        im = axes[2].imshow(np.concatenate([original, sparse], axis=0), cmap='RdBu_r', vmin=-abs(original).max(), vmax=abs(original).max(), aspect='auto')
        fig.colorbar(im, ax=axes[2], label=tr('权重 / 无量纲', 'Weight / dimensionless'))
        axes[2].axhline(15.5, color='#253d4a'); axes[2].set(xlabel=tr('输入像素编号', 'Input pixel index'), yticks=[7.5, 23.5], yticklabels=['student', '50% zeros'], title=tr('同一矩阵：上原始、下剪枝', 'Same matrix: original / pruned'))
        save(fig, 'compression')
        fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
        for i, name in enumerate(sessions):
            t = np.sort(timings[name]['1']); axes[0].plot(t, np.arange(1, 121) / 120, label=name, color=colors[i])
            medians = [np.median(timings[name][str(b)]) for b in [1, 32, 128]]
            axes[1].plot([1, 32, 128], np.array([1, 32, 128]) * 1000 / medians, 'o-', label=name, color=colors[i])
        axes[0].set(xlabel=tr('单次推理 / ms', 'Inference call / ms'), ylabel=tr('实测累计比例', 'Empirical cumulative fraction'), xscale='log'); axes[0].legend(frameon=False)
        axes[1].set(xlabel=tr('批量大小', 'Batch size'), ylabel=tr('吞吐 / 图像每秒', 'Throughput / images per second'), xscale='log', yscale='log'); axes[1].legend(frameon=False)
        save(fig, 'latency')
        fig = plt.figure(figsize=(12, 6.5), layout='constrained'); gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.6])
        for i, (name, value) in enumerate(streams.items()):
            ax = fig.add_subplot(gs[0, i]); ax.imshow(value[0].reshape(8, 8), cmap='gray_r', vmin=0, vmax=16); ax.set_title(name); ax.axis('off')
        ax = fig.add_subplot(gs[1, :2])
        for i, (name, value) in enumerate(streams.items()): ax.hist(value.mean(1), bins=edges, histtype='step', linewidth=4 if name == 'clean' else 2, linestyle='--' if name == 'rotated' else '-', label=name, color=colors[i])
        ax.set(xlabel=tr('每张图片的平均灰度', 'Mean intensity per image'), ylabel=tr('样本数', 'Image count')); ax.legend(frameon=False)
        ax = fig.add_subplot(gs[1, 2]); names = list(streams)
        ax.bar(names, [drift[n]['accuracy'] for n in names], color=colors[:3]); ax.set(ylim=(0, 1.08), ylabel=tr('标签到达后：准确率', 'After labels arrive: accuracy'))
        for i, n in enumerate(names): ax.text(i, drift[n]['accuracy'] + .025, f"{drift[n]['accuracy']:.3f}", ha='center')
        save(fig, 'monitoring')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
```

The complete run writes five ONNX variants, training weights, a manifest, actual prediction and timing arrays, replay data and all figures. The serve option restarts the local prediction endpoint using the same JSON agreement. Extending this example to a real application can add authentication, resource limits, concurrency and queue measurements, recovery and links to business outcomes. Each addition should have a stated purpose and an observable example. Deployment then becomes a sequence of understandable, repeatable experiments connecting model behavior to use, rather than a final operation that merely copies a weight file.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M27.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Sculley et al. (2015), Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/)

   System dependencies beyond an isolated model score.

   Primary paper reference; no reproduced figure.
2. [Breck et al. (2017), The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

   Testing data,models,infrastructure and monitoring.

   Primary paper reference; original teaching diagram.
3. [Hinton, Vinyals & Dean (2015), Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)

   Temperature-softened targets and student networks.

   Paper referenced; all experiments newly computed.
4. [ONNX — Python introduction](https://onnx.ai/onnx/intro/python.html)

   Constructing inference graphs from nodes,tensors and a dynamic batch axis.

   Apache-2.0 project; conceptual reference.
5. [ONNX — DequantizeLinear](https://onnx.ai/onnx/operators/onnx__DequantizeLinear.html)

   Per-channel scales,axis and dequantization semantics.

   Apache-2.0 project; original implementation.
6. [ONNX Runtime — Quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)

   Quantized weights,activation precision,calibration and execution providers.

   MIT project; technical reference.
7. [PyTorch — Pruning tutorial](https://docs.pytorch.org/tutorials/intermediate/pruning_tutorial.html)

   Weight masks and structured/unstructured pruning.

   BSD-3-Clause documentation/code; no figure copied.
8. [MLflow — Model Registry](https://mlflow.org/docs/latest/registry/)

   Immutable versions and mutable deployment aliases.

   Apache-2.0 project; no MLflow server needed for the example.
9. [TensorFlow Data Validation](https://www.tensorflow.org/tfx/guide/tfdv)

   Input schemas,training-serving skew and distribution drift.

   CC BY4.0 documentation; original figures.
10. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

    1797 eight-by-eight digit images,intensities0–16,and dataset provenance.

    UCI Optical Recognition of Handwritten Digits; see dataset terms.
