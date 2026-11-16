# From photographs to 3D: cameras, radiance fields, and point clouds

Source: https://ml-biomat.com/tutorials/machine-learning/m14/en/
Language: en

Calculate depth, accumulate color along rays, and learn unordered point sets with a PointNet-style network.

## 1. A photograph loses distance along the viewing direction

Hold up a finger and alternate closing your left and right eyes. The finger appears to jump relative to the distant background. Nearby objects shift more than distant ones, providing an everyday example of the information used in stereo depth estimation. A photograph projects a three-dimensional world onto a plane. Many positions along one viewing ray can produce the same image location. Measuring distance, reconstructing a part, or viewing a room from another position requires recovering relationships among cameras, space, and images. Understanding what projection removes is a useful starting point before operating a large reconstruction package.

Three distinct goals appear in this chapter. Geometric reconstruction estimates where surfaces are and how they connect. Novel-view synthesis predicts what another camera would see. Point-cloud learning assigns categories or part labels to spatial samples. A scene can look convincing from familiar directions while revealing incorrect geometry from a less-observed viewpoint. A sparse cloud can contain enough information to recognize a chair while remaining insufficient to manufacture it precisely. Defining the intended output helps choose among coordinates, surfaces, volume densities, and Gaussian primitives, as well as the measurements needed to assess the result.

We first calculate pinhole projection and stereo distance by hand, then examine how multiple images jointly constrain cameras and spatial points. A known three-dimensional density field provides a controlled rendering experiment in which sampling and occlusion determine pixel colors. Finally, a shared point network learns to distinguish sphere-surface and cube-surface samples, with a direct test that changing point order preserves its output. NeRF, 3D Gaussian Splatting, and PointNet become concrete computational ideas within these stages rather than isolated architecture names.

## 2. A camera converts coordinate systems

A spatial coordinate needs a reference frame. A world frame may be fixed to a table, while a camera frame moves with the lens. Moving the camera changes an object's camera coordinates without changing its world coordinates. Extrinsic rotation and translation perform this frame conversion. Intrinsic focal lengths and principal-point coordinates determine the projection into image pixels. We use positive depth in front of the camera and a virtual image plane in front of its center, avoiding an additional image-inversion sign. Software packages differ in axis conventions and in whether a stored pose maps world to camera or camera to world, so these conventions belong with the data.

$$
p_c=Rp_w+t,\qquad u=f_x\frac{X_c}{Z_c}+c_x,\quad v=f_y\frac{Y_c}{Z_c}+c_y
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/544857d035238c222088f2be.svg) | 3-component point column vectors in world and camera frames, in meters; pc=(Xc,Yc,Zc)ᵀ with Zc>0. |
| ![Formula](https://ml-biomat.com/static/agent-math/3cafeb78b5a3fe4ab1afd21f.svg) | 3-by-3 world-to-camera rotation, dimensionless; 3-component translation in meters. |
| ![Formula](https://ml-biomat.com/static/agent-math/d14b71953101044988436e00.svg) | Horizontal/vertical focal lengths and principal-point coordinates, all in pixels. |
| ![Formula](https://ml-biomat.com/static/agent-math/487fcc1666d8aaba8b444887.svg) | Image coordinates in pixels and camera-coordinate components in meters; lens distortion is excluded here. |

Transform to the camera frame, then apply the coordinate-to-depth ratios from similar triangles. With identity R, zero t, point (0.3,0.15,3) meters, focal lengths 800 pixels, and principal point (320,240), u=800×0.3/3+320=400 and v=280 pixels. Point (0.6,0.3,6) meters on the same ray projects identically, exposing the missing depth information.

Division by depth follows from similar triangles. A more distant object occupies a smaller angle and consequently a smaller image region. When focal length is expressed in pixels, the length units cancel in the ratios of camera coordinates and the result has pixel units. For camera coordinates (0.3, 0.15, 3) meters, focal lengths of 800 pixels, and principal point (320,240), the projection is (400,280). Converting all three spatial coordinates to millimeters preserves the answer. Substituting a focal length measured in millimeters directly into a pixel formula would instead mix optical and sampling scales.

Real lenses introduce distortion. Radial distortion bends straight lines near image edges, while tangential terms account for certain lens and sensor misalignments. Calibration observes known geometry, such as a checkerboard under several poses, and estimates intrinsic and distortion parameters that explain its measured corners. Varied tilts provide constraints that repeated front-facing photographs lack. Changing focal length, image resolution, or cropping requires corresponding parameter updates. Reprojection error compares projected and observed points in image coordinates. It assesses how well the model explains those observations, alongside practical checks of image coverage and the distances at which the camera will be used.

The inverse construction turns a pixel into a ray step by step. Subtract the principal point, divide by the two focal lengths, and append a forward component of one. This defines a direction through the virtual image plane; normalization converts it to a unit vector. Camera pose rotates the direction into the world frame, where sampling starts at the camera center. Distinguish camera-axis depth from distance along this ray. They coincide on the central axis, but an oblique ray travels farther to reach the same forward depth. The script reports a weighted distance along the ray, rather than labeling that quantity as the camera-coordinate Z value.

## 3. Two viewing rays constrain distance

Two cameras observing the same point provide two rays whose intersection constrains its position. In a rectified stereo configuration with parallel optical axes, corresponding points are mapped onto the same image row. Their horizontal difference is disparity, and the separation between camera centers is the baseline. A larger baseline or longer focal length generally produces a larger disparity at a fixed depth. More distant objects produce smaller disparity. The following relation is obtained by subtracting the two projection equations. With measurement noise, rays may not intersect exactly, so triangulation seeks a position consistent with the observations.

$$
d=u_L-u_R=\frac{fB}{Z},\qquad Z=\frac{fB}{d}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d3a304cfd8c87c33bffa627c.svg) | Horizontal coordinates of a corresponding point in rectified left/right images and their disparity, in pixels; d>0 under this configuration. |
| ![Formula](https://ml-biomat.com/static/agent-math/978f149e4d511c2397b7abd1.svg) | Common horizontal focal length in pixels, horizontal camera baseline in meters, and forward depth in meters. |

The left projection contains fX/Z, while the right camera sees horizontal coordinate X−B. Subtraction removes X and leaves fB/Z. With f=800 pixels, B=0.12 meters, and Z=3 meters, disparity is 32 pixels. Inversion gives 800×0.12/32=3 meters. Measuring 31 pixels gives about 3.097 meters; 33 pixels gives about 2.909 meters. A one-pixel error thus corresponds to roughly nine or ten centimeters here. The relation assumes the stated rectified geometry and known baseline.

Without rectification, corresponding image points obey an epipolar constraint. A pixel in the first image defines a spatial ray. Projecting that ray into the second image traces an epipolar line, reducing a two-dimensional correspondence search to locations near a line. Geometry identifies possible matches; texture and feature evidence select among them. Repeated windows, smooth walls, and reflections can make correspondence ambiguous. Camera motion consisting almost entirely of rotation supplies little translational parallax, leaving depth weakly constrained even when the images appear quite different.

Structure from motion, or SfM, jointly estimates camera poses and sparse scene points from multiple images. A typical incremental pipeline extracts and matches features, rejects geometrically inconsistent correspondences, chooses an initial pair, adds cameras, triangulates new points, and jointly refines cameras and points through bundle adjustment. Schönberger and Frahm's 2016 work examines the robustness and scalability of this process and provides the open-source COLMAP implementation. Its task is to establish consistent structure from unordered image collections, including reliable matching and initialization, rather than estimating an unrelated depth map for each photograph.

Multi-view stereo uses the recovered cameras to estimate denser depth and fuse it into a cloud or surface. A poorly observed back side has fewer image constraints, while transparent and reflective regions can violate simple appearance consistency. Monocular SfM usually recovers relative scale: scaling the scene and camera translations together can preserve every projection. Metric distances require a known baseline, reference object, reliable external poses, or another scale measurement. The depth–disparity curve below also shows why distant measurements become sensitive: disparity changes more slowly with depth, so a fixed pixel error produces a larger distance error.

![Left: depth–disparity relation for focal length 800 pixels and baseline 0.12 meters; 3 meters corresponds to 32 pixels. Right: actual sphere and cube test clouds with 64 points, colored by normalized z. Coordinates are centered and scaled by maximum point distance.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c1b68c6a6b5016bc7e873eaa.svg?v=c1b68c6a6b50)

Figure 1Left: depth–disparity relation for focal length 800 pixels and baseline 0.12 meters; 3 meters corresponds to 32 pixels. Right: actual sphere and cube test clouds with 64 points, colored by normalized z. Coordinates are centered and scaled by maximum point distance.

## 4. What points, surfaces, and fields preserve

A point cloud records sampled spatial positions, often with color, normals, or return intensity. It is a direct representation for laser scanning and multi-view reconstruction, but it has no default connectivity and may have highly uneven density. A mesh additionally states how vertices form triangles, supporting surface normals, areas, and rendering. Incorrect connectivity changes the represented surface. A voxel grid partitions space into regular cells and supports three-dimensional convolution. Doubling resolution along every axis multiplies the cell count by eight. Representation choice therefore determines both preserved detail and computational cost.

An implicit representation supplies a queryable function instead of listing every surface point. An occupancy function describes whether a position belongs inside an object. A signed-distance function gives distance from the surface with a sign distinguishing the two sides; the surface is its zero set. Arbitrary continuous locations can be queried, but extracting a mesh still requires spatial sampling and locating the zero isosurface. A radiance field asks different questions: what volume density is present at a location, and what color is emitted toward a viewing direction? It is organized around generating images rather than requiring a clean triangle mesh at the outset.

The word density has different meanings in these representations. Density in NeRF-style volume rendering controls opacity accumulated over length and has inverse-length units. It is neither material mass density nor the number of sampled points per cubic meter. Multiplying volume density by a ray interval's length gives dimensionless optical thickness. That unit relationship determines how density becomes opacity and explains why scene scale, distances, and density must be transformed consistently. Keeping these meanings separate makes the rendering equation easier to interpret and prevents a visual field from being mistaken for a physical material measurement.

Whether to preserve absolute size also depends on the task. Centering and scaling a point cloud encourages a classifier to focus on shape, while removing position and scale. A miniature building and a full-size building may consequently have similar normalized inputs. Predicting mass, length, or spatial placement requires retaining the removed transformation, restoring it in the output, or supplying it as additional information. Normalization is a deliberate choice about which differences the model should ignore. Recording that choice together with the desired invariance and final measurement units prevents a shape-classification preprocessing rule from silently changing a measurement problem.

## 5. NeRF: accumulating color along a ray

Imagine looking at a white background through several colored veils. The first veil contributes some color, leaving only part of the incoming visibility for the second, then the third. A more opaque front layer reduces the influence of everything behind it. Volume rendering divides a camera ray into intervals, queries density and color in each, and composites their contributions from front to back. Position, occlusion order, and local appearance all enter the result. Averaging every color encountered along the ray would discard which colors are actually visible.

$$
r(t)=o+t\,d,\quad \alpha_i=1-e^{-\sigma_i\Delta_i},\quad T_i=\prod_{j<i}(1-\alpha_j),\qquad C=\sum_{i=1}^{N}T_i\alpha_i c_i+T_{N+1}c_{\rm bg}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c183f0b2cce72055896ed3cf.svg) | Ray position and camera origin in length units, unit direction vector dimensionless, and ray distance t in length units; d here is a direction, not disparity. |
| ![Formula](https://ml-biomat.com/static/agent-math/aff3de4d1287f50ac8efc600.svg) | Front-to-back interval index, preceding interval index, count, and interval length; Δi uses the same units as t. |
| ![Formula](https://ml-biomat.com/static/agent-math/29c3a8316806774aaf842d39.svg) | Approximately constant interval density in inverse length, opacity, and incoming transmittance, with the latter two dimensionless; T1=1. |
| ![Formula](https://ml-biomat.com/static/agent-math/e6e788e985849507bdb7d611.svg) | Local, background, and final 3-component RGB colors, normalized from zero to one here. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d72c41288befef4e73ce70f.svg) | Transmittance remaining after all intervals; it sums with the weights Tiαi to one. |

Transmittance through a uniform interval decays exponentially. Density times length is dimensionless, and one minus the surviving fraction gives opacity. With interval length one and density ln2 per length unit, opacity is one half. Two such layers have weights 0.5 and 0.25, leaving background weight 0.25. Red before blue on white produces (0.75,0.25,0.5). Changing the sample count changes interval lengths; retaining the old opacity for each new sample would change the represented optical thickness.

Take a red front layer and a blue rear layer, both with opacity one half, against white. Red contributes weight 0.5. Only half the visibility reaches blue, which contributes weight 0.25. The remaining background weight is 0.25, producing RGB (0.75,0.25,0.50). Reversing the layers gives (0.50,0.25,0.75). Their colors and individual opacities are unchanged, yet their order changes the pixel. The interaction exposes each accumulation step, showing incoming transmittance, layer weight, and cumulative color so that the conservation of total weight can be checked directly.

### Ray lab: composite one pixel layer by layer

The ray crosses red, blue, and green layers from left to right against white. Each step processes one layer; the unprocessed remainder is temporarily white. Opacity and order changes recompute the current step.

[Figure: Incoming transmittance, contribution weights, and pixel color for three layers](https://ml-biomat.com/tutorials/machine-learning/m14/en/#M14-svg)

In the 2020 NeRF work by Mildenhall and colleagues, a neural network represents a continuous radiance field. Spatial position and viewing direction determine density and direction-dependent color. Each image pixel defines a ray; the network is queried along that ray, and differentiable volume rendering produces a pixel prediction. Error against observed photographs flows backward through this computation to update network parameters. Positional encoding expands coordinates into multiple frequencies to support finer detail. Concentrating samples in influential regions spends queries where they affect the image. Direction-dependent color represents appearance that changes with viewpoint, including some specular behavior.

Our experiment separates defining a field from learning one. The script specifies two Gaussian-shaped density regions and their colors analytically, then renders them from three camera positions. It does not fit a NeRF. The known field makes the resulting image and ray-distance map inspectable, while different sample counts reveal numerical integration error. Learning a NeRF would replace this function with a trainable field, use training-camera pixels as supervision, and reserve other cameras for evaluation. Fit to seen views, quality of unseen views, and metric geometric accuracy remain separate quantities to examine.

![Three camera views of a known analytic 3D density field, with 96 midpoint samples per ray](https://ml-biomat.com/static/tutorials/machine-learning/figures/9f2e98acc21b94349a354744.svg?v=9f2e98acc21b)

Figure 2Three camera views of a known analytic 3D density field, with 96 midpoint samples per ray. Above: normalized RGB. Below: ray distance weighted by Tiαi and divided by total opacity; rays with opacity below 0.05 are masked. Two colored Gaussian density regions define the field. These are numerical renders, not reconstructions from a fitted NeRF.

The soft boundaries in our renders are properties of the specified field. Gaussian density decreases smoothly away from each center, so edge opacity decreases and more white background remains visible. This differs from blur caused by unsuccessful training. Increasing the ray sample count integrates the same soft field more accurately; it does not turn that field into a hard sphere surface. Testing reconstruction of a sharp boundary requires a corresponding sharp-surface or signed-distance reference and an examination of whether sampling and learning recover it. Separating the target field from approximation error helps explain what the rendered image actually shows.

## 6. Gaussian splatting: projectable ellipsoids describe a scene

Ray marching can query many positions, including empty space. Kerbl and colleagues' 2023 3D Gaussian Splatting method instead represents a scene with explicit three-dimensional Gaussian primitives. Each has a center, orientation and scale, opacity, and parameters for view-dependent appearance. Its covariance determines the axes along which the ellipsoid extends. Equal scales give a spherical shape; anisotropic shapes can represent thin surface-like regions more compactly. Under a camera transformation, a primitive projects to an elliptical footprint, whose color is composited with other primitives according to visibility and depth.

$$
g(x)=\exp\!\left[-\tfrac12(x-\mu)^{\mathsf T}\Sigma^{-1}(x-\mu)\right],\qquad \Sigma_{\rm image}\approx J R\Sigma R^{\mathsf T}J^{\mathsf T}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/313be2bc3b1ea3e88ce189b7.svg) | 3D query position and center in length units, and a symmetric positive-definite 3-by-3 covariance in squared length; the hand example uses the analogous 2D form. |
| ![Formula](https://ml-biomat.com/static/agent-math/a9e111e418e432fd154a819b.svg) | Dimensionless Gaussian footprint weight before opacity, without a probability-density normalization constant. |
| ![Formula](https://ml-biomat.com/static/agent-math/1921007cc69f5e372ba69af9.svg) | 3-by-3 world-to-camera rotation, dimensionless; 2-by-3 local projection Jacobian in pixels/length; approximate 2-by-2 image covariance in squared pixels. |
| ![Formula](https://ml-biomat.com/static/agent-math/b5661152420d3e399df6a285.svg) | Transpose and matrix inverse; the quadratic form measures displacement in covariance-scaled units, producing a dimensionless exponent. |

In 2D with zero center and covariance diag(1,1), position (2,0) gives exp(−2)≈0.1353. With covariance diag(4,1), the horizontal standard deviation becomes two and the value is exp(−0.5)≈0.6065. Projection first rotates the covariance, then uses the local linear map J to convert length variation into pixel variation. The result has squared-pixel units. This approximation explains an ellipsoid's image footprint; opacity, depth ordering, and pixel coverage complete the rendering process.

A small numerical example clarifies shape. Increase a two-dimensional Gaussian's horizontal standard deviation from one to two while retaining vertical standard deviation one. At displacement (2,0), its unscaled Gaussian weight rises from exp(−2)≈0.135 to exp(−0.5)≈0.607, reflecting a wider footprint. Projecting a three-dimensional covariance also depends on camera rotation and the local derivative of perspective projection near the primitive's center. Simply deleting the third row and column does not perform that transformation. Identical primitives closer to a camera typically cover more pixels, while viewpoint changes alter their projected orientation and extent.

Training differentiates image error through rendering to optimize centers, shapes, opacities, and appearance. Density control adjusts the number and distribution of primitives, splitting or adding detail where needed and removing low-contribution elements. A common NeRF description is to query a learned field at positions; a common 3DGS description is to project and blend explicit primitives. Both depend on cameras and multi-view observations. A convincing appearance is a different product from a closed surface mesh suitable for a mechanical solver. Dimensions, normals, and topology can be extracted and evaluated when those are the quantities the application needs.

## 7. PointNet: learning from an unordered bag of coordinates

A cloud can list its highest point first or its leftmost point first without changing the object. Concatenating every coordinate in that arbitrary order would allow a network to confuse ordering with shape. In PointNet, published in 2017, Qi and colleagues apply the same network to every point and aggregate with a symmetric maximum operation. Imagine asking all points the same questions and keeping the strongest answer to each question. The arrival order does not change those strongest answers. The resulting fixed-length global feature then supports object classification.

$$
h_i=\phi(p_i),\quad z_k=\max_{1\le i\le N}h_{ik},\qquad \widehat y=\psi(z)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64ce1240f88a388826694962.svg) | 3-component point, point index, and count; N=64 in the code, with centered and scaled dimensionless coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/3ee18f897c9f94e3975aff0c.svg) | Shared point network, F-component point feature, and its kth component; F=64 and hidden quantities are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3da56523af656a4dda677791.svg) | Channel index, maximum over points for that channel, and F-component global representation; different points may supply different channel maxima. |
| ![Formula](https://ml-biomat.com/static/agent-math/ae4dec2f081c6c8cbdad8485.svg) | Classification head and class-score vector; the code outputs two dimensionless logits and chooses the larger one. |

For three point features (1,4), (3,2), and (2,5), channelwise maxima give z=(3,5). Reordering the three points preserves z, while shared φ preserves each point's processing rule. Whole-object classification is therefore permutation invariant. Point segmentation can concatenate z with each hi and produce correspondingly reordered outputs. Maximum pooling alone does not prescribe the effect of rotating coordinates, which requires separate design.

Pointwise part segmentation additionally preserves local point features, broadcasts the global feature back to each point, concatenates both, and predicts a label at each position. Knowledge of the whole object can help distinguish a chair leg from its back. The original PointNet also contains input and feature alignment modules. Our small model retains the shared point transformation and maximum readout, with random rotations in its training data to provide varied orientations. Permutation invariance follows from the computation itself. Rotation invariance is a separate requirement and does not follow automatically from maximum pooling.

The experiment samples sphere and cube surfaces, with sixty-four points per cloud. Each cloud receives a random rotation, is centered by subtracting its point mean, and is scaled by its largest point distance, giving comparable input scale. Training, validation, and test sets contain 160, forty, and sixty clouds. A point's three coordinates become thirty-two and then sixty-four features. Channelwise maxima feed a small classifier producing two class scores. Training lasts eighty epochs, with validation loss selecting epoch sixty-four. Test accuracy is 58/60, or 0.9667. Reordering every test cloud's points gives a maximum absolute output difference of zero.

### Complete Python: geometry, volume rendering, and point classification

Run main.py --output output --language en, or select zh. NumPy, PyTorch, and Matplotlib train a small shared point network on CPU and independently render a known 3D field. Clouds, predictions, ray images, and summary.json are saved; no pretrained weights are downloaded.

```
"""Camera geometry, volume compositing, and a PointNet-style classifier."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


def clouds(count, seed):
    rng=np.random.default_rng(seed);points=[];labels=np.arange(count)%2
    for label in labels:
        if label==0:
            p=rng.normal(size=(64,3));p/=np.linalg.norm(p,axis=1,keepdims=True)
        else:
            p=rng.uniform(-1,1,(64,3));axes=rng.integers(0,3,64)
            p[np.arange(64),axes]=rng.choice([-1,1],64)
        rotation,_=np.linalg.qr(rng.normal(size=(3,3)))
        p=p@rotation;p-=p.mean(0);p/=np.linalg.norm(p,axis=1).max()
        points.append(p)
    return np.array(points,dtype=np.float32),labels


class PointModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.point=nn.Sequential(nn.Linear(3,32),nn.ReLU(),nn.Linear(32,64),nn.ReLU())
        self.readout=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,2))
    def forward(self,x):
        return self.readout(self.point(x).amax(dim=1))


def scene(points):
    centers=np.array([[-.35,0,0],[.35,.12,.08]])
    sizes=np.array([.23,.19]);colors=np.array([[.82,.25,.18],[.12,.42,.75]])
    components=16*np.exp(-.5*np.square((points[...,None,:]-centers)/sizes[:,None]).sum(-1))
    sigma=components.sum(-1)
    color=(components[...,None]*colors).sum(-2)/(sigma[...,None]+1e-15)
    return sigma,color


def render(angle, samples, resolution=48):
    origin=np.array([2.8*np.cos(angle),1.,2.8*np.sin(angle)])
    forward=-origin/np.linalg.norm(origin)
    right=np.cross(forward,[0,1,0]);right/=np.linalg.norm(right)
    up=np.cross(right,forward)
    q=(np.arange(resolution)+.5-resolution/2)/(resolution/2)
    xx,yy=np.meshgrid(q,-q)
    direction=1.8*forward+xx[...,None]*right+yy[...,None]*up
    direction/=np.linalg.norm(direction,axis=-1,keepdims=True)
    edges=np.linspace(1,5,samples+1);t=(edges[:-1]+edges[1:])/2;delta=np.diff(edges)
    points=origin+direction[:,:,None,:]*t[None,None,:,None]
    sigma,color=scene(points);alpha=-np.expm1(-sigma*delta)
    trans=np.concatenate([np.ones((*alpha.shape[:2],1)),np.cumprod(1-alpha,axis=-1)[...,:-1]],axis=-1)
    weights=trans*alpha;remaining=np.prod(1-alpha,axis=-1)
    rgb=(weights[...,None]*color).sum(-2)+remaining[...,None]
    opacity=weights.sum(-1)
    depth=(weights*t).sum(-1)/(opacity+1e-12)
    conservation=float(np.max(np.abs(opacity+remaining-1)))
    return rgb,depth,opacity,conservation


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def txt(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    torch.manual_seed(14)
    tx,ty=clouds(160,10);vx,vy=clouds(40,20);ex,ey=clouds(60,30)
    tx,ty,vx,vy=map(torch.tensor,[tx,ty,vx,vy]);model=PointModel()
    optimizer=torch.optim.Adam(model.parameters(),lr=.003);history=[];best=float('inf')
    for epoch in range(80):
        model.train();losses=[]
        for ids in torch.randperm(160).split(20):
            optimizer.zero_grad();loss=nn.functional.cross_entropy(model(tx[ids]),ty[ids])
            loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad():val=nn.functional.cross_entropy(model(vx),vy).item()
        history.append([np.mean(losses),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    with torch.no_grad():
        test=torch.tensor(ex);logits=model(test);prediction=logits.argmax(1).numpy()
        permutation=torch.tensor(np.random.default_rng(17).permutation(64))
        permutation_error=float((model(test[:,permutation])-logits).abs().max())
    angles=[0,.8,1.6];renders=[render(a,96) for a in angles]
    reference=render(.8,256)[0];sample_counts=[8,16,32,64,96]
    errors=[float(np.sqrt(np.mean((render(.8,n)[0]-reference)**2))) for n in sample_counts]
    conservation=max(r[3] for r in renders)
    focal,baseline,depth=800.,.12,3.
    disparity=focal*baseline/depth
    recovered=focal*baseline/disparity
    # Front-to-back red and blue layers, both with opacity one half.
    red=np.array([1.,0,0]);blue=np.array([0.,0,1]);white=np.ones(3)
    red_first=.5*red+.5*.5*blue+.25*white
    blue_first=.5*blue+.5*.5*red+.25*white
    summary={'test_pointclouds':60,'test_accuracy':float(np.mean(prediction==ey)),
             'permutation_max_error':permutation_error,'selected_epoch':int(np.argmin(np.array(history)[:,1])+1),
             'compositing_conservation_error':conservation,'stereo_disparity_px':disparity,
             'recovered_depth_m':recovered,'sample_counts':sample_counts,'rgb_rmse_to_256_samples':errors,
             'red_front_rgb':red_first.tolist(),'blue_front_rgb':blue_first.tolist()}
    assert permutation_error<1e-6 and conservation<1e-12
    assert abs(recovered-3)<1e-12
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',test_clouds=ex,test_labels=ey,prediction=prediction,history=history,
             view_rgb=np.array([r[0] for r in renders]),view_depth=np.array([r[1] for r in renders]),
             view_opacity=np.array([r[2] for r in renders]),samples=sample_counts,rmse=errors)
    fig=plt.figure(figsize=(12,4.3));gs=fig.add_gridspec(1,3,width_ratios=[1.1,1,1])
    ax=fig.add_subplot(gs[0]);zs=np.linspace(.8,8,150);ds=focal*baseline/zs
    ax.plot(zs,ds,color='#176b91');ax.scatter([3],[32],color='#bb554d',zorder=3)
    ax.annotate('3 m → 32 px',(3,32),xytext=(3.4,65),arrowprops={'arrowstyle':'->'})
    ax.set(xlabel=txt('深度 / m','Depth / m'),ylabel=txt('视差 / px','Disparity / px'),title=txt('固定焦距800 px，基线0.12 m','Focal length 800 px; baseline 0.12 m'))
    for k in range(2):
        ax=fig.add_subplot(gs[k+1],projection='3d');p=ex[k]
        ax.scatter(*p.T,c=p[:,2],cmap='viridis',s=15,vmin=-1,vmax=1)
        ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1),xlabel='x',ylabel='y',zlabel='z',title=txt(['球面点集','立方体表面点集'][k],['Sphere points','Cube-surface points'][k]))
        ax.set_box_aspect((1,1,1));ax.view_init(22,35)
        ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_zticks([-1,0,1])
    fig.tight_layout();save(fig,'geometry')
    fig,axs=plt.subplots(2,3,figsize=(12,7))
    for j,angle in enumerate(angles):
        rgb,dep,opacity,_=renders[j]
        axs[0,j].imshow(rgb);axs[0,j].set_title(txt(f'相机方位 {angle:.1f} rad',f'Camera azimuth {angle:.1f} rad'))
        masked=np.ma.masked_where(opacity<.05,dep)
        im=axs[1,j].imshow(masked,cmap='viridis',vmin=2,vmax=4)
        axs[1,j].set_title(txt('条件加权射线距离 / 单位长度','Conditional ray distance / length units'))
        for i in range(2):axs[i,j].set_xticks([]);axs[i,j].set_yticks([])
    fig.colorbar(im,ax=axs[1,:],shrink=.65,label=txt('射线距离','Ray distance'))
    save(fig,'views')
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,3,width_ratios=[1.3,1,1])
    ax=fig.add_subplot(gs[:,0]);hist=np.array(history)
    ax.plot(np.arange(1,81),hist[:,0],label=txt('训练','Training'),color='#176b91')
    ax.plot(np.arange(1,81),hist[:,1],label=txt('验证','Validation'),color='#bb554d')
    ax.set(xlabel=txt('轮数','Epoch'),ylabel=txt('交叉熵','Cross-entropy'),title=txt('共享逐点网络与最大值读出','Shared point network and max readout'));ax.legend()
    ax=fig.add_subplot(gs[0,1]);conf=np.zeros((2,2),int)
    for y,p in zip(ey,prediction):conf[y,p]+=1
    ax.imshow(conf,cmap='Blues',vmin=0,vmax=30)
    for i in range(2):
        for j in range(2):ax.text(j,i,str(conf[i,j]),ha='center',va='center',color='white' if conf[i,j]>15 else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xlabel=txt('预测类别','Predicted class'),ylabel=txt('真实类别','True class'))
    ax=fig.add_subplot(gs[1,1]);ax.semilogy(sample_counts,errors,'o-',color='#176b91')
    ax.set(xlabel=txt('每射线采样数','Samples per ray'),ylabel='RGB RMSE',title=txt('对照256采样','Reference: 256 samples'))
    ax=fig.add_subplot(gs[0,2]);ax.imshow(np.tile(red_first,(30,30,1)));ax.set_title(txt('红在前，蓝在后','Red in front of blue'));ax.axis('off')
    ax=fig.add_subplot(gs[1,2]);ax.imshow(np.tile(blue_first,(30,30,1)));ax.set_title(txt('蓝在前，红在后','Blue in front of red'));ax.axis('off')
    fig.tight_layout();save(fig,'results')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

The script saves both rendering and classification data. Rendering with eight, sixteen, thirty-two, sixty-four, and ninety-six midpoint samples per ray is compared with a 256-sample reference. RGB root-mean-square difference decreases from about 0.00558 to 0.0000175. Across the rendered rays, accumulated weights plus remaining background transmittance differ from one by at most about 1.55×10⁻¹⁵. The point-cloud figure displays actual model inputs, the confusion matrix reports all sixty test clouds, and the colored patches display the two-layer compositing calculation. Together they examine learned classification, numerical integration, and occlusion logic.

![Left: training and validation cross-entropy for the shared point network](https://ml-biomat.com/static/tutorials/machine-learning/figures/af9c6cc58a4365a5cfbf4668.svg?v=af9c6cc58a43)

Figure 3Left: training and validation cross-entropy for the shared point network. Upper center: confusion matrix for sixty test clouds, class 0 sphere and class 1 cube. Lower center: RGB RMSE against 256 ray samples. Right: RGB patches for reversed red/blue layer order, both opacity 0.5, on white.

Maximum readout also has an instructive consequence: duplicating an already present point cannot change any channel maximum. This suits a representation of sampled shape, but does not make point multiplicity a measure of object mass. If counts themselves carry information, a sum or an explicit count feature may be appropriate. Different channels can receive their maxima from different, sometimes relatively few, points. Recording those contributing points in space reveals which sampled regions support the global representation. Such a visualization answers a more specific question than displaying only a class probability: which observations supplied the features used by the classifier?

## 8. Evaluate geometry together with observation coverage

Evaluation should respect camera and object grouping. Novel-view synthesis holds out camera positions, examining both interpolation between familiar views and positions with weaker coverage. Similar scans of one object should not be casually split between point-cloud training and testing. Reconstruction can be assessed through point-to-surface distance, normal agreement, and known dimensions. Image synthesis can be assessed through pixel error, structural similarity, or perceptual measures. Scale alignment, background inclusion, and treatment of occluded or unobserved regions directly affect the meaning of those numbers.

Sampling changes the shape evidence available to a point network. Sparse clouds can miss a thin leg or hole; occlusion can remove an entire side; a distant outlier may dominate some maximum channels. Beyond accuracy, reduce point count, add a small number of outliers, or remove points from one viewing direction and inspect the resulting errors. Local-neighborhood models and graph networks add relationships among points. Equivariant networks encode prescribed coordinate-transformation behavior. Each extension addresses a particular problem in the observations or output, so the task and sampling conditions should motivate the choice.

A complete small project could photograph a static object beside a known scale, check calibration and view coverage, estimate sparse points and poses, and train a scene representation from part of the views. Remaining views assess image synthesis while known lengths assess geometry. Displaying camera distribution, image error, and length error together reveals where evidence is strong and where results rely on interpolation. The practical value of three-dimensional learning lies in spatial relationships that can be computed, checked, and used for the next measurement or interaction.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M14.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

   Pinhole projection, intrinsic/extrinsic parameters, and calibration.
2. [Structure-from-Motion Revisited](https://demuc.de/papers/schoenberger2016sfm.pdf)

   Original incremental-SfM and COLMAP paper.
3. [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934)

   Continuous radiance fields, differentiable rendering, and learning.
4. [Nerfstudio — Nerfacto](https://docs.nerf.studio/nerfology/methods/nerfacto.html)

   Ray sampling, pose refinement, and implementation pipeline; original pipeline illustration available on the source page.
5. [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)

   Gaussian primitives, anisotropic covariance, and visibility-aware rendering.
6. [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://arxiv.org/abs/1612.00593)

   Shared point maps, symmetric aggregation, and local/global features.
