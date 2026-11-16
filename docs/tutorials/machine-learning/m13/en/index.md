# Beyond recognition: location, shape, and motion

Source: https://ml-biomat.com/tutorials/machine-learning/m13/en/
Language: en

Understand detection, segmentation, tracking, pose, and OCR through the structure of their outputs.

## 1. After recognizing a car, what else must a system know?

Knowing that a traffic video contains cars is only a first step. Counting vehicles requires locating individual objects. Measuring how much road they occupy requires their outlines. Detecting a vehicle traveling in the wrong direction requires connecting the same vehicle across successive frames. Reading its license plate adds another challenge: recovering an ordered character sequence from pixels. Image classification compresses an image into a category. These tasks retain location, shape, identity, and time in their outputs, so their annotation rules, model designs, and evaluation procedures must retain the corresponding structure too.

Think of an image as a city map. A detection box marks an approximate building footprint, a segmentation mask traces its occupied area, keypoints mark important landmarks, and a trajectory records movement over time. A box does not contain a complete outline, and a mask does not automatically establish correspondence with a previous frame. The intended use determines how much structure is needed. Counting parked cars may not require precise boundaries around their tires, while a rectangle is insufficient for measuring the width of a thin crack. Choosing the output is therefore part of defining the problem, before choosing an architecture.

This chapter connects the tasks through a sequence of concrete calculations. We first measure overlap between boxes and handle duplicate predictions. We then train a small U-shaped network to produce a foreground probability at every pixel. Finally, we associate observations through time and inspect when crossing paths cause identities to switch. Synthetic circles and rectangles provide images with fully specified ground truth, making pixel-level checking straightforward. Larger detectors, promptable segmentation, pose systems, and OCR are explained through their inputs and outputs so that the runnable experiment can become a starting point for a more complete visual pipeline.

## 2. A box needs the right extent, not just the right center

An axis-aligned bounding box can be written as four coordinates identifying its upper-left and lower-right corners. We use horizontal coordinates increasing to the right and vertical coordinates increasing downward. Coordinates describe pixel boundaries, so width is the right boundary minus the left boundary, without an extra one. This convention affects areas and overlap. Halving an image's dimensions halves its box coordinates. Padding followed by resizing requires recording both translation and scale before predictions can be mapped back to the original image. A persistent small displacement in displayed predictions often originates in coordinate restoration rather than the recognition model.

$$
w_\cap=\max(0,\min(x_2,x_2')-\max(x_1,x_1')),\quad h_\cap=\max(0,\min(y_2,y_2')-\max(y_1,y_1')),\qquad \operatorname{IoU}=\frac{w_\cap h_\cap}{(x_2-x_1)(y_2-y_1)+(x_2'-x_1')(y_2'-y_1')-w_\cap h_\cap}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d552cb9f1aa1fec81772895c.svg) | Left, top, right, and bottom boundaries of the first box in pixels, with positive width and height. |
| ![Formula](https://ml-biomat.com/static/agent-math/41d1fa18a670d3fb43df055a.svg) | Corresponding boundaries of the second box in pixels; primes identify another box, not derivatives. |
| ![Formula](https://ml-biomat.com/static/agent-math/67de279b9227ab3828a2ac64.svg) | Intersection width and height in pixels, clipped to zero if disjoint. |
| ![Formula](https://ml-biomat.com/static/agent-math/edf6d089f5f2b0f0b5fc3470.svg) | Intersection over union, dimensionless from zero to one; square-pixel units cancel. |

The intersection takes the inward boundaries. Adding both box areas counts their overlap twice, so subtracting it once gives the union. Boxes (0,0,10,10) and (5,0,15,10) intersect over width 5 and height 10, giving area 50 and union 100+100−50=150. IoU is 1/3. Identical boxes give one; disjoint boxes give zero. These continuous pixel-boundary coordinates require no extra one in width or height.

Intersection over union, or IoU, divides overlapping area by the total area covered by either box. It penalizes displacement, excessive size, and insufficient coverage. Two 10-by-10 boxes displaced horizontally by five pixels overlap over fifty square pixels, while their union covers 150, giving IoU one third. Small objects are especially sensitive to pixel-scale errors: a two-pixel displacement has a different effect on an eight-pixel-wide object and an eighty-pixel-wide object. Inspecting errors by object size helps explain an overall score and prevents successful localization of large objects from obscuring missed small ones.

A detector often produces several nearby boxes for one object. Non-maximum suppression, or NMS, retains the highest-scoring box, removes same-class candidates whose overlap with it exceeds a threshold, and repeats. A lower overlap threshold suppresses more strongly; a higher threshold retains more overlapping predictions. In crowds, two real people may overlap substantially, so aggressive suppression can remove a real instance. The NMS overlap threshold, the output confidence threshold, and the IoU threshold used for evaluation perform three different jobs. Naming and adjusting them separately avoids a common source of confusion.

### Box lab: displacement, duplicates, and thresholds

Gray regions are two ground-truth objects; colored boxes are three candidates of one class. Dashed candidates are filtered. The right panel evaluates retained predictions at IoU≥0.5 after NMS.

[Figure: Ground-truth objects, candidate boxes, retained results, overlap and matching statistics](https://ml-biomat.com/tutorials/machine-learning/m13/en/#M13-svg)

Evaluation sorts predictions by confidence and matches them one-to-one to ground-truth objects under a specified IoU condition. Each ground-truth instance can be claimed correctly only once; additional duplicate predictions count as false positives. Precision asks how many reported objects are correct. Recall asks how many actual objects were found. Moving the confidence threshold traces a precision–recall curve; AP summarizes it, while mAP averages over prescribed classes or overlap conditions. AP50, AP75, and an average over thresholds from 0.50 to 0.95 impose different localization requirements. A meaningful comparison states which convention produced the number.

$$
\operatorname{Precision}=\frac{TP}{TP+FP},\qquad \operatorname{Recall}=\frac{TP}{TP+FN}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fedfc0b572b83a7991e52748.svg) | Count of predictions matched one-to-one to ground truth with the correct class and required IoU. |
| ![Formula](https://ml-biomat.com/static/agent-math/479b502526ba6c1154af06a5.svg) | Unmatched prediction count, including duplicates, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f6b50c71aba1b713f18bdba.svg) | Ground-truth object count without a correct matched prediction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3d052e2baf25a3b565522340.svg) | Precision and recall, dimensionless proportions from zero to one; zero denominators require an explicit evaluation convention. |

With five actual objects and six predicted boxes, four successful unique matches give TP=4, FP=2, and FN=1. Precision is 4/6≈0.667 and recall is 4/5=0.8. Raising confidence can remove both false and true positives, motivating inspection across thresholds. AP requires the ranked precision–recall behavior and a specified interpolation convention; precision at one threshold is not AP.

## 3. Propose regions, predict directly, or predict a set

Two-stage detection separates the question of where to look from what the proposed region contains. A Faster R-CNN-style pipeline computes a shared feature map, proposes potentially relevant regions, extracts aligned regional features, and performs classification with box refinement. It resembles marking promising places on a map before examining each one closely. Shared features avoid running the entire image computation independently for every candidate. Regional features let subsequent heads focus on individual objects. Adding a mask prediction to each proposed instance provides a route from detection to instance segmentation.

Single-stage detection places category and localization predictions directly on one or more feature maps. Redmon and colleagues' YOLO work, initially released in 2015, framed detection as joint whole-image prediction of boxes and associated categories. SSD explicitly uses multiple feature-map scales to address objects of different sizes. Fine-resolution maps retain detail for small objects; coarser positions observe larger input regions. Anchor-based methods refine predefined boxes with selected scales and aspect ratios. Anchor-free approaches can express boundaries through centers or distances instead. Both need a strategy for assigning training targets and handling the imbalance between abundant background locations and relatively few objects.

![Original D2L SSD multiscale architecture](https://ml-biomat.com/static/tutorials/machine-learning/figures/6026bfbb90dbc0cbcaa779b0.svg?v=6026bfbb90db)

Figure 1Original D2L SSD multiscale architecture. Follow progressively smaller feature maps and their category/localization predictions for different object sizes. Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, Dive into Deep Learning, Fig. 14.7.1, https://d2l.ai/chapter_computer-vision/ssd.html, CC BY-SA 4.0; unmodified.

Inspect the output tensor before memorizing detector names. A 20-by-20 feature map with three anchors at each position and two object classes plus background requires 20×20×3×3 classification scores and 20×20×3×4 localization parameters. These candidates must be decoded into image coordinates and processed for duplicates. Convolutional prediction heads are useful because locations differ while the rule for predicting local information is shared. Other implementations define background, target assignment, and regression targets differently, so the dimensions should be checked against the actual head rather than assumed from a generic diagram.

Carion and colleagues' 2020 DETR work instead formulates detection as set prediction. A fixed collection of learned object queries produces candidate slots; slots without a corresponding object learn a no-object category. During training, bipartite matching assigns predictions to ground-truth instances one-to-one before category and localization losses are calculated. With two actual objects and three slots, the best assignment makes two slots responsible for the objects and trains the third as empty. Encouraging unique predictions through the set objective is central to removing conventional anchor generation and NMS from that formulation. Training behavior, small-object accuracy, and runtime still depend on the implementation, image scales, and optimization setup.

## 4. Expanding a category prediction to every pixel

Semantic segmentation assigns a category to each pixel, such as road, vehicle, or sky. Pixels belonging to two touching vehicles still share the vehicle category. Instance segmentation additionally distinguishes the first vehicle from the second. Panoptic segmentation combines countable object instances with continuous background regions into a unified scene description. Consider two touching circles: their binary foreground mask may contain one connected region even though two objects exist. Counting connected components is therefore not equivalent to counting instances. The distinction determines whether the required annotation is a class map, an instance map, or a combination.

Segmentation needs context and precise localization together. Reducing feature resolution expands the observable area but loses boundary detail; examining only a tiny neighborhood can confuse an object with similar texture. In the 2015 U-Net paper, Ronneberger, Fischer, and Brox combine a contracting context pathway with an expanding pathway that restores spatial resolution. High-resolution features are passed to corresponding decoding stages. These skip connections resemble returning a detailed sketch to an artist who has just established the large composition. The decoder learns to combine spatial detail with contextual information rather than merely enlarging a small prediction image.

$$
p_i=\frac{1}{1+e^{-z_i}},\qquad \mathcal L=-\frac1N\sum_{i=1}^{N}\big[y_i\log p_i+(1-y_i)\log(1-p_i)\big]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | Number of pixels in the batch and a pixel index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/29337fa51cf400a673c72b86.svg) | Foreground logit and sigmoid probability at pixel i, dimensionless; network output shape is B×1×H×W. |
| ![Formula](https://ml-biomat.com/static/agent-math/6efa4604c774374baf410795.svg) | Batch image count and pixel height and width; the code uses B×1×48×48. |
| ![Formula](https://ml-biomat.com/static/agent-math/d904ffb3258f0e94299beb6e.svg) | Binary foreground label, mean binary cross-entropy, and natural logarithm; loss is measured in nats per pixel. |

For a foreground pixel, only −log p remains; for background, only −log(1−p) remains. Assigning higher probability to the correct outcome reduces loss. A foreground pixel with p=0.8 contributes −ln0.8≈0.2231, while a background pixel with the same foreground probability contributes −ln0.2≈1.6094. The code computes binary_cross_entropy_with_logits directly from z for stability and converts to probabilities for display.

Our binary model produces a foreground logit at each pixel. Training uses a numerically stable binary cross-entropy implementation; display converts logits to probabilities with a sigmoid and applies a threshold of 0.5. When background dominates, pixel accuracy can obscure complete failure to find objects. An image containing 95% background permits 95% accuracy from an all-background prediction. Foreground IoU and Dice compare the predicted and true regions directly. Boundary measurements and object-level analysis add information about thin structures or merged instances. Averaging a metric over images and computing it after pooling all pixels apply different weights to image size and foreground amount.

$$
\operatorname{IoU}_{\rm mask}=\frac{|P\cap G|}{|P|+|G|-|P\cap G|},\qquad \operatorname{Dice}=\frac{2|P\cap G|}{|P|+|G|}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/939924d4ef9cfd6c8974e1c1.svg) | Predicted and ground-truth foreground pixel sets; a probability threshold defines P. |
| ![Formula](https://ml-biomat.com/static/agent-math/614e03b6a4b537e0c9c4b390.svg) | Pixel counts of the two regions and their intersection. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa08102b6650df285e8ee2b7.svg) | Region IoU and Dice overlap coefficient, dimensionless from zero to one; every experimental image contains foreground. |

With eight predicted pixels, ten true pixels, and six shared pixels, the union contains twelve. IoU is 6/12=0.5 and Dice is 12/18≈0.667. They assess overlap on different scales, so their numerical sizes are not directly interchangeable. This chapter computes each metric per image and averages over forty images, weighting images equally. Empty-foreground cases require a separately stated convention.

Promptable segmentation also takes the user's intended object as input. The 2023 Segment Anything Model combines an image encoder, prompt encoding for inputs such as points and boxes, and a mask decoder. An image representation can be cached while different prompts generate candidate masks. A positive point indicates a desired region, a negative point excludes an area, and a box supplies approximate extent. A point on a wheel is ambiguous: the requested object might be the wheel or the entire car. Multiple candidates and further interaction help express that intent. Prompts guide object selection; class definitions and annotation conventions remain part of the task.

SAM 2, introduced in 2024, extends promptable segmentation to video using streaming memory for information across frames. Additional guidance can correct an object region and influence later propagation. A practical annotation project still defines whether masks cover visible pixels or inferred full objects, how identity persists through occlusion, and how touching objects are separated. General segmentation models provide learned object priors. Thin lines, transparent regions, low-contrast boundaries, and specialized imaging conditions warrant targeted examples and corresponding evaluation. The mask is ultimately an input to a measurement or decision, so its quality should be assessed against that use.

## 5. From an image to a video: displacement, identity, and action

Optical flow describes apparent pixel displacement between images. Both object movement and camera movement can produce it, so an arrow in the image does not directly give an object's three-dimensional physical velocity. A classical derivation assumes that a visible surface point approximately preserves brightness over a short interval. A first-order expansion relates spatial intensity gradients, the temporal gradient, and two motion components. A straight edge mainly constrains motion perpendicular to itself; movement along the edge can leave the local image almost unchanged. Consequently, the information at one pixel does not uniquely determine both motion components.

$$
I_x u+I_y v+I_t=0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/338ef8468bcc4575db37ec2d.svg) | Normalized dimensionless image intensity at position (x,y) and time t. |
| ![Formula](https://ml-biomat.com/static/agent-math/5e6b967262bd6322703a3df2.svg) | Spatial and temporal intensity derivatives, with units intensity/pixel, intensity/pixel, and intensity/frame. |
| ![Formula](https://ml-biomat.com/static/agent-math/8d978f4f1831d626cb3d5ca1.svg) | Horizontal and vertical image velocities in pixels/frame; using seconds changes the units consistently to pixels/second. |

Begin with approximate brightness constancy, I(x,y,t)≈I(x+uΔt,y+vΔt,t+Δt), expand to first order, and divide by Δt. If Ix=2, Iy=0, and It=−6 in consistent units, the equation gives u=3 pixels/frame while leaving v unspecified. Additional independent neighborhood constraints are needed to determine both components. Large motion and changing brightness affect the approximation and its assumptions.

Lucas–Kanade-style estimation assumes similar motion within a small neighborhood and combines gradient equations from several pixels. An image pyramid helps handle larger displacement at a coarser scale first. Weak texture, changing reflections, and occlusion weaken the underlying evidence. Learning-based flow methods can learn matching features and update rules, but still distinguish observed correspondences from regions hidden in another frame. Flow studies motion at pixel level. Multi-object tracking instead associates detected objects into identity-bearing trajectories, commonly combining motion predictions, appearance similarity, and a one-to-one matching procedure.

Connecting every new detection to the nearest previous location can exchange identities when two objects cross. A simple constant-velocity predictor estimates direction from recent observations and matches detections against predicted positions. In our controlled example, two objects cross between frames nine and ten, and both detections exist in every frame. Position-only association produces two identity switches, while velocity-based association produces zero. Keeping observations available isolates association errors from detection errors. Abrupt turns or extended occlusion would require additional modeling, appearance information, track persistence, or re-identification to continue the same identity reliably.

The ByteTrack preprint from 2021 focuses on another recurring situation: a partially occluded true object often receives a low detection score, and discarding it can fragment the trajectory. Its association strategy first processes higher-confidence detections, then uses remaining tracks to recover compatible lower-confidence detections. A weak observation consistent with an existing track can thus continue that identity. Detection precision, identity preservation, and trajectory completeness describe different aspects of the system. Identity-aware metrics such as IDF1 and association-aware measures such as HOTA complement box overlap, while frame-by-frame inspection reveals exactly when a correspondence breaks.

Video understanding adds event-level structure. Opening a door and closing it may contain similar individual frames, with order determining the action. Three-dimensional convolution extracts patterns over spatial and temporal neighborhoods. A recurrent model can accumulate history from frame features, while a space-time Transformer relates positions across frames through attention. Clip classification assigns a label to a segment; temporal action localization predicts beginning and end times; framewise action segmentation partitions a longer sequence into meaningful stages. Frame rate, boundary conventions, and whether future frames are available must match the intended use. An online alert and an offline video annotation system have different temporal information.

## 6. Structured objects: joints form poses and characters form text

Pose estimation represents an object through landmarks such as shoulder, elbow, and wrist. A top-down pipeline first detects each person, then predicts keypoints within the individual region. A bottom-up pipeline finds joints across the image and groups joints that belong to the same person. The first separates person localization from landmark localization, with a missed person box losing the entire pose. The second must solve ownership in crowded scenes. A model can regress coordinates directly or predict a heatmap indicating plausible positions for each landmark. Heatmaps retain spatial ambiguity before peaks are converted into original-image coordinates.

Coordinate restoration matters here too. A 200-by-400-pixel person region resized to 100 by 200 requires predicted wrist coordinates to be rescaled and shifted by the original box origin. If the output heatmap is four times smaller again, that additional factor must also be restored. Keypoint errors need object-scale context: a five-pixel wrist error means different things for a distant small person and a close large one. Measures such as PCK and OKS use scale-related tolerances. Visibility annotations distinguish an unannotated joint, an occluded joint with an inferred position, and a visible joint, preventing unlike information states from being treated as identical supervision.

Optical character recognition recovers an ordered sequence of characters from an image. A complete pipeline typically detects text regions, corrects orientation or perspective, recognizes their contents, and recovers reading order. The 2020 PP-OCR work presents a lightweight combination of text detection, direction classification, and recognition. Text regions can be rotated quadrilaterals, and curved text requires more detailed boundary handling. Cropping away the top of a character can remove information that no downstream recognizer receives. Separating text localization quality from transcription quality helps identify which stage causes an end-to-end error.

The character count is generally unknown, and character-level boundaries may be unavailable. A recognizer using connectionist temporal classification, or CTC, predicts character-or-blank distributions along the image width, then collapses repeated consecutive labels and removes blanks. A simplified path A, A, blank, B, B becomes AB; A, blank, A remains AA. Training sums probabilities over alignment paths that yield the target sequence, avoiding a requirement to manually cut out every character. An attention-based decoder instead generates characters sequentially while selecting relevant visual features. Language regularities can aid recognition, but may also favor a familiar word over an unusual identifier.

$$
\operatorname{CER}=\frac{S+D+I}{N}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/13068cfa28766b99858d616e.svg) | Substitution, deletion, and insertion counts in a minimum reference-to-prediction edit alignment, measured in characters; I here is unrelated to image intensity. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of characters in the nonempty reference text, after a fixed normalization convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/d3283f595665abbe12efce0d.svg) | Dimensionless character error rate, which can exceed one when insertions are numerous. |

Using edits from reference to recognition output, turning 2074 into 204 deletes 7, so D=1 and CER=1/4. Turning 2074 into 2074A inserts A, again giving 1/4. Total edit distance is symmetric, but insertion/deletion names exchange when direction reverses, so the implementation fixes a direction. Complete-string accuracy separately counts only exact whole-sequence matches.

Character error rate, CER, counts substitutions, deletions, and insertions relative to the number of ground-truth characters. Reading “2074” as “204” requires one deletion and gives CER one quarter. Reading it as “2074A” requires one insertion and gives the same CER. Complete-string accuracy can better reflect parcel numbers or laboratory sample identifiers, because a single wrong character may refer to a different object. Documents additionally require correct column order, table cells, and punctuation. Define case, whitespace, and character-normalization conventions before evaluation. The output eventually serves a concrete workflow, and that workflow determines which errors matter most.

## 7. A complete experiment: masks, errors, and trajectories together

The script generates 160 training images, forty validation images, and forty test images with separate random seeds. Every 48-by-48 grayscale image contains one to three circles or rectangles. A mild background brightness gradient and Gaussian noise with standard deviation 0.14 make individual pixel thresholds imperfect. Ground truth is the union of all generated shapes, so overlapping shapes belong to the same semantic foreground. The network has one downsampling and one upsampling stage, with a skip connection between high-resolution and low-resolution processing. Its size keeps the entire U-shaped computation visible in the source.

### Complete Python: pixel segmentation and identity association

Requires NumPy, SciPy, PyTorch, and Matplotlib. Run main.py --output output --language en, or choose zh for Chinese plots. The script trains a small U-shaped network, saves test probabilities and overlap metrics, and separately computes NMS and two association trajectories. All outputs go to the specified directory.

```
"""Pixel segmentation, component boxes, NMS, and temporal association."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

torch.set_num_threads(2)


def make_images(n, seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[:48, :48]
    images, masks = [], []
    for _ in range(n):
        mask = np.zeros((48,48), bool)
        for obj in range(rng.integers(1,4)):
            x,y=rng.integers(9,39,2); size=rng.integers(4,9)
            if obj%2: shape=(abs(xx-x)<size)&(abs(yy-y)<size)
            else: shape=(xx-x)**2+(yy-y)**2<size**2
            mask |= shape
        background=.15+.08*xx/48
        image=np.clip(background+mask*rng.uniform(.35,.65)+rng.normal(0,.14,(48,48)),0,1)
        images.append(image);masks.append(mask)
    return np.array(images,dtype=np.float32)[:,None], np.array(masks,dtype=np.float32)[:,None]


class SmallUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.high=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.Conv2d(8,8,3,padding=1),nn.ReLU())
        self.low=nn.Sequential(nn.MaxPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),nn.Conv2d(16,16,3,padding=1),nn.ReLU())
        self.output=nn.Sequential(nn.Conv2d(24,8,3,padding=1),nn.ReLU(),nn.Conv2d(8,1,1))

    def forward(self,x):
        high=self.high(x);low=self.low(high)
        up=nn.functional.interpolate(low,size=high.shape[-2:],mode='bilinear',align_corners=False)
        return self.output(torch.cat([high,up],dim=1))


def iou(box1,box2):
    x1,y1=np.maximum(box1[:2],box2[:2]);x2,y2=np.minimum(box1[2:],box2[2:])
    intersection=max(0,x2-x1)*max(0,y2-y1)
    area1=np.prod(np.array(box1[2:])-box1[:2]);area2=np.prod(np.array(box2[2:])-box2[:2])
    return intersection/(area1+area2-intersection)


def nms(boxes,scores,threshold):
    order=np.argsort(-np.asarray(scores));keep=[]
    while len(order):
        selected=int(order[0]);keep.append(selected)
        order=np.array([i for i in order[1:] if iou(boxes[selected],boxes[i])<=threshold],dtype=int)
    return keep


def box_components(mask):
    labels,n=ndimage.label(mask)
    boxes=[]
    for i in range(1,n+1):
        y,x=np.where(labels==i)
        if len(x)>=12:boxes.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
    return boxes


def track(use_velocity):
    frames=np.arange(21)
    truth=np.stack([np.column_stack([8+2*frames,24+0*frames]),np.column_stack([46-2*frames,25+0*frames])],axis=1)
    rng=np.random.default_rng(9);observed=truth+rng.normal(0,.12,truth.shape)
    previous=observed[0].copy();velocity=np.zeros((2,2));history=[previous.copy()];identities=[np.array([0,1])]
    for obs in observed[1:]:
        predicted=previous+velocity if use_velocity else previous
        cost=np.square(predicted[:,None,:]-obs[None,:,:]).sum(2)
        _,col=linear_sum_assignment(cost)
        current=obs[col];velocity=current-previous;previous=current
        history.append(current.copy());identities.append(col)
    identities=np.array(identities)
    switches=int(np.sum(identities[1:]!=identities[:-1]))
    return truth,np.array(history),switches


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def text(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    torch.manual_seed(12)
    xt,yt=map(torch.tensor,make_images(160,100));xv,yv=map(torch.tensor,make_images(40,200))
    test_x,test_y=make_images(40,300);model=SmallUNet();optimizer=torch.optim.Adam(model.parameters(),lr=.003)
    best=float('inf');history=[]
    for epoch in range(25):
        model.train();losses=[]
        for indices in torch.randperm(160).split(20):
            optimizer.zero_grad();loss=nn.functional.binary_cross_entropy_with_logits(model(xt[indices]),yt[indices])
            loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad(): val=nn.functional.binary_cross_entropy_with_logits(model(xv),yv).item()
        history.append([float(np.mean(losses)),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    with torch.no_grad():probability=torch.sigmoid(model(torch.tensor(test_x))).numpy()[:,0]
    truth=test_y[:,0].astype(bool);predicted=probability>=.5;baseline=test_x[:,0]>=.45
    def overlap(pred):
        inter=(pred&truth).sum((1,2));union=(pred|truth).sum((1,2))
        return inter/union,2*inter/(pred.sum((1,2))+truth.sum((1,2)))
    score,dice=overlap(predicted);base_score,_=overlap(baseline)
    boxes=[[5,5,25,25],[7,6,27,26],[30,10,44,25]];scores=[.9,.8,.7]
    assert abs(iou([0,0,10,10],[5,0,15,10])-1/3)<1e-12
    assert nms(boxes,scores,.5)==[0,2]
    trajectories={}
    for method in ['position','velocity']:
        true_track,estimated,switches=track(method=='velocity')
        trajectories[method]=(estimated,switches)
    summary={'test_images':40,'mean_foreground_iou':float(score.mean()),'mean_dice':float(dice.mean()),
             'intensity_baseline_iou':float(base_score.mean()),'selected_epoch':int(np.argmin(np.array(history)[:,1])+1),
             'nms_kept':nms(boxes,scores,.5),'position_identity_switches':trajectories['position'][1],
             'velocity_identity_switches':trajectories['velocity'][1]}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',test_images=test_x,test_masks=test_y,probability=probability,
             history=history,iou=score,dice=dice,baseline_iou=base_score,true_track=true_track,
             position_track=trajectories['position'][0],velocity_track=trajectories['velocity'][0])
    selected=[0,1,int(np.argmin(score))];fig,axs=plt.subplots(3,4,figsize=(12,8))
    titles=[text('带噪输入','Noisy input'),text('真实前景','Ground-truth foreground'),text('预测概率','Predicted probability'),text('错误与连通域框','Errors and component boxes')]
    for row,index in enumerate(selected):
        axs[row,0].imshow(test_x[index,0],cmap='gray',vmin=0,vmax=1)
        axs[row,1].imshow(truth[index],cmap='gray',vmin=0,vmax=1)
        im=axs[row,2].imshow(probability[index],cmap='viridis',vmin=0,vmax=1)
        rgb=np.stack([truth[index]*.2]*3,axis=-1);rgb[predicted[index]&~truth[index]]=[.8,.3,.2];rgb[~predicted[index]&truth[index]]=[.1,.6,.8]
        axs[row,3].imshow(rgb)
        for x1,y1,x2,y2 in box_components(predicted[index]):axs[row,3].add_patch(Rectangle((x1-.5,y1-.5),x2-x1,y2-y1,fill=False,edgecolor='#e8bd52',lw=1))
        axs[row,0].set_ylabel(f'#{index} | IoU={score[index]:.3f}')
        for col in range(4):
            axs[row,col].set_xticks([]);axs[row,col].set_yticks([])
            if row==0:axs[row,col].set_title(titles[col])
    fig.tight_layout(rect=(0,.075,1,1))
    color_axis=fig.add_axes([.535,.035,.17,.012])
    fig.colorbar(im,cax=color_axis,orientation='horizontal',ticks=[0,.5,1],label=text('前景概率','Foreground probability'))
    save(fig,'segmentation')
    fig,axs=plt.subplots(1,3,figsize=(12,3.7),gridspec_kw={'width_ratios':[1.1,1,.9]})
    history=np.array(history)
    axs[0].plot(np.arange(1,26),history[:,0],label=text('训练','Training'),color='#176b91')
    axs[0].plot(np.arange(1,26),history[:,1],label=text('验证','Validation'),color='#bb554d')
    axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('像素二元交叉熵','Pixel binary cross-entropy'));axs[0].legend()
    axs[1].scatter(base_score,score,c='#176b91',s=24);axs[1].plot([0,1],[0,1],'--',c='#999')
    axs[1].set(xlim=(0,1),ylim=(0,1),xlabel=text('强度阈值基线IoU','Intensity-threshold IoU'),ylabel=text('小型U形网络IoU','Small U-shaped network IoU'),aspect='equal')
    for i,b in enumerate(boxes):
        axs[2].add_patch(Rectangle((b[0],b[1]),b[2]-b[0],b[3]-b[1],fill=False,lw=2,ls='--' if i==1 else '-',edgecolor=['#176b91','#bb554d','#8f711b'][i]))
        axs[2].text(b[0],b[3]+3 if i==1 else b[1]-1,f'{i}: {scores[i]}',fontsize=9)
    axs[2].set(xlim=(0,48),ylim=(35,0),aspect='equal',xlabel=text('横坐标 / px','Horizontal / px'),ylabel=text('纵坐标 / px','Vertical / px'),title=text('NMS保留0、2','NMS retains 0 and 2'))
    fig.tight_layout();save(fig,'metrics')
    fig,axs=plt.subplots(2,2,figsize=(12,4.2),gridspec_kw={'height_ratios':[1,.35]})
    for j,method in enumerate(['position','velocity']):
        estimated,switches=trajectories[method]
        for k,c in enumerate(['#176b91','#bb554d']):
            axs[0,j].plot(np.arange(21),true_track[:,k,0],'--',color='#adb6bc',lw=3)
            axs[0,j].plot(np.arange(21),estimated[:,k,0],color=c,label=f'ID {k+1}')
        method_name={'position':'位置关联','velocity':'速度预测关联'}[method]
        axs[0,j].set(xlabel=text('帧编号','Frame'),ylabel=text('横坐标 / px','Horizontal / px'),xticks=np.arange(0,21,5),title=text(f'{method_name}：身份切换{switches}次',f'{method}: {switches} identity switches'));axs[0,j].legend()
        axs[1,j].axis('off')
        for a,t in enumerate([0,7,10,13,20]):
            inset=axs[1,j].inset_axes([a*.2,0,.18,.9]);inset.set(xlim=(0,58),ylim=(34,16),aspect='equal')
            for k,c in enumerate(['#176b91','#bb554d']):
                px,py=estimated[t,k];inset.add_patch(Rectangle((px-3,py-3),6,6,fill=False,edgecolor=c,lw=2));inset.text(px,py-5,str(k+1),color=c,ha='center')
            inset.set_title(f't={t}',fontsize=9);inset.set_xticks([]);inset.set_yticks([])
    fig.tight_layout();save(fig,'tracking')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

Training runs for twenty-five epochs in batches of twenty. Validation binary cross-entropy selects the checkpoint, which is epoch twenty-five in the executed run. Across forty test images, mean per-image foreground IoU is 0.9082 and mean Dice is 0.9499. A direct intensity-threshold baseline at 0.45 obtains mean IoU 0.6363. This comparison shows how spatial context helps separate shapes from pixel noise. The contact sheet displays test images zero and one together with the test image having the lowest IoU. In the final column, red identifies false positives, blue identifies missed foreground, and yellow boxes enclose predicted connected regions.

![Executed outputs for test images 0, 1, and the lowest-IoU example](https://ml-biomat.com/static/tutorials/machine-learning/figures/b7b747c218e5b95935ce5085.svg?v=b7b747c218e5)

Figure 2Executed outputs for test images 0, 1, and the lowest-IoU example. Inputs and probabilities range from zero to one; masks are binary. Red shows false positives, blue missed foreground, and yellow boxes enclose predicted components of at least twelve pixels. All images are 48×48 pixels; row labels give sample index and IoU.

These component boxes are geometry extracted from the segmentation output, retaining connected regions with at least twelve pixels. The script does not train a separate detection head or learn confidence scores for those boxes. This step demonstrates conversion from masks to coarse localization and shows why touching objects may produce one region. The metrics figure retains a separate network-versus-baseline comparison for every test image, with a diagonal representing equal scores. Its NMS panel uses three explicitly defined boxes and scores, independently of segmentation training, making the duplicate-removal calculation easy to inspect.

![Left: training and validation binary cross-entropy](https://ml-biomat.com/static/tutorials/machine-learning/figures/2526b88671f5b02040bfa82c.svg?v=2526b88671f5)

Figure 3Left: training and validation binary cross-entropy. Center: per-image IoU for forty test images, with the diagonal indicating equality with the intensity baseline. Right: NMS on separately defined candidates at threshold 0.5; dashed box 1 is suppressed by box 0, retaining boxes 0 and 2.

The final figure follows all twenty-one frames of the synthetic trajectories. Dashed lines show true horizontal positions, while colored lines connect observations according to estimated identity. Five selected frames below show identity-labeled boxes. Position association connects the wrong paths after crossing, whereas velocity association maintains the correspondence. Detection centers in this experiment are generated directly from true centers plus small observation noise, isolating association from image-detector omissions. To study occlusion next, remove selected observations and add track prediction and re-association. The same replay can then reveal which particular failure each extension resolves.

![Two association rules process the same twenty-one-frame observations](https://ml-biomat.com/static/tutorials/machine-learning/figures/f30c85f519c4a6df567a5776.svg?v=f30c85f519c4)

Figure 4Two association rules process the same twenty-one-frame observations. Above: horizontal position versus frame, with gray dashed truth and colored estimated identities. Below: identity boxes at five selected frames. Position-only association makes two identity switches; velocity prediction makes zero. Observed centers are true centers plus noise with standard deviation 0.12 pixels.

## 8. Turning a convincing picture into a useful visual measurement

A usable visual project starts with annotation conventions. Does a box cover visible extent or the inferred whole object? Are transparent areas included in a mask? How are hidden joints labeled? Does an action start when a hand moves or when it contacts an object? These choices define the training target. Independently labeling a small representative sample and resolving disagreements often improves consistency before scaling annotation. Objects, scenes, and video clips should also guide the split. Randomly distributing adjacent frames between training and testing places similar backgrounds and almost duplicate poses on both sides.

Resolution, speed, and accuracy need direct measurement. Reducing input size saves computation but can leave small text only a few pixels wide. Tiled processing preserves detail while introducing overlap merging and objects that cross tile boundaries. Runtime reports should specify image decoding, preprocessing, inference, NMS, and result transfer, and should distinguish batch throughput from single-frame latency. An interactive video application responds to the delay from an input becoming available to a usable result. A large offline analysis may instead prioritize sustained throughput and stable handling of unusual inputs.

Make errors inspectable at the level of the output structure. Detection needs examples of small-object misses and duplicate boxes; segmentation needs thin structures and touching boundaries; tracking needs identities after occlusion; pose estimation needs hidden landmarks; OCR needs confusing characters and reading order. Include ordinary conditions as well as darkness, blur, and dense overlap, placing images beside the corresponding metrics. A number describes aggregate change, while an example identifies where it occurred. Richer visual outputs become useful when each part can be checked against the real task it is meant to support.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M13.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Single Shot Multibox Detection](https://d2l.ai/chapter_computer-vision/ssd.html)

   Multiscale detection tutorial, implementation, and licensed original diagram.

   Original diagram CC BY-SA 4.0.
2. [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

   Combining context with localization through a U-shaped architecture.
3. [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640)

   Joint whole-image category and localization prediction.
4. [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)

   Object queries, one-to-one set matching, and detection.
5. [Segment Anything](https://arxiv.org/abs/2304.02643)

   Prompts, image representations, and mask decoding.
6. [SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714)

   Promptable video segmentation and streaming memory.
7. [ByteTrack: Multi-Object Tracking by Associating Every Detection Box](https://arxiv.org/abs/2110.06864)

   Using lower-confidence observations in association.
8. [PP-OCR: A Practical Ultra Lightweight OCR System](https://arxiv.org/abs/2009.09941)

   Text detection, direction handling, and sequence recognition.
9. [OpenCV Optical Flow Tutorial](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)

   Optical-flow assumptions, gradient constraints, and Lucas–Kanade.
10. [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)

    Two-stage detection with shared features and region proposals.
11. [Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)

    Path collapsing and learning from unsegmented sequences.
12. [MMPose Overview](https://mmpose.readthedocs.io/en/latest/overview.html)

    Keypoints, heatmaps, encoding and decoding, and pose tooling.
