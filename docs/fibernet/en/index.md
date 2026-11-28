# FiberNet

Source: https://ml-biomat.com/fibernet/en/
Language: en

4.40.0 · Python 3.9+ · MIT

Fiber-network generation, analysis, and mechanical modeling

Connect network generation, structural analysis, and mechanical modeling in Python. Use FiberScope to inspect, configure, and export networks on the desktop.

## Python library

FiberNet represents structures through nodes and edges, connecting generation, analysis, simulation, and export in reusable Python workflows.

- Generate 2D and 3D structures and manage nodes, edges, and fiber radii.
- Analyze planar snapshots, pore distributions, and tensile recruitment on supplied trajectories.
- Use beam-frame FEM and additional computational backends installed as needed.
- Save native graphs and results for analysis with the provided examples.

## FiberScope desktop interface

FiberScope 3.1.0 supports geometry configuration, structural inspection, trajectory playback, and export. The Windows download includes its runtime.

## Fiber network in motion

![Structural deformation](https://ml-biomat.com/static/images/fibernet/homepage/network-morph.webp)

Structural deformation

![Tensile fracture of a woven network](https://ml-biomat.com/static/images/fibernet/homepage/woven-fracture.webp)

Tensile fracture of a woven network

![From an orientation field to a 3D fiber bundle](https://ml-biomat.com/static/images/fibernet/homepage/orientation-to-bundle.webp)

From an orientation field to a 3D fiber bundle

![From leaf veins to a graph neural network](https://ml-biomat.com/static/images/fibernet/homepage/leaf-venation-gnn.webp)

From leaf veins to a graph neural network · Original photograph [Brocken Inaglory](https://commons.wikimedia.org/wiki/File:Vein_skeleton_of_a_leaf.JPG) · cropped, recolored and skeletonized · [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

![Flow through a 3D fiber network](https://ml-biomat.com/static/images/fibernet/homepage/porous-fiber-flow.webp)

Flow through a 3D fiber network

[Animation sources and methods](https://github.com/GellmanSparrowS/fibernet/blob/d50dcd08606917c9b693573bcfb8bd6dc81aebd0/docs/MEDIA_GALLERY.md)

## Install FiberNet

Run this command in a terminal. The base installation includes NumPy, SciPy, NetworkX, and Matplotlib, and is sufficient for the honeycomb example below.

```bash
python -m pip install "fibernet==4.40.0"
```

Optional dependencies

```bash
python -m pip install "fibernet[ml]==4.40.0"  # Machine learning
python -m pip install "fibernet[viz]==4.40.0"  # 3D display
python -m pip install "fibernet[manufacturing]==4.40.0"  # Geometry and solid export
```

The 3D viewer uses PyVista. For the Taichi backend, install the `accel` extra.

## Example: stretching a honeycomb network

This Python script displays a 2D honeycomb network, computes its maximum displacement in meters, and saves the network and simulation result as separate JSON files.

```python
import fibernet as fn

# Build a 2D honeycomb network (lengths in meters)
graph = fn.pattern_2d(
    unit="honeycomb", box=(0.01, 0.01), grid=(2, 2),
    radius=0.00005, seed=23,
)
fn.show(graph)

# Solve for 1% extension with linear beams (elastic modulus in Pa)
result = fn.simulate(
    graph, backend="fem", mode="stretch", stretch_ratio=1.01,
    nonlinear=False, E=1e9, nu=0.3,
)
print(result.max_displacement)

graph.save_json("network.json")
result.save("fem_result.json")
```

## More workflows

### Structural analysis and learning

Extract features from planar snapshots or use edge-strain histories to study when fibers begin carrying load. The examples also cover physical labels, regression, and target-curve search.

[Snapshot example](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/snapshot_features_workflow.py)[Physical-learning example](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/physical_learning_workflow.py)[Target-curve search](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/curve_inverse_workflow.py)

### Geometric routes and export

Build continuous paths on a plane or curved surface with custom cells, then export the paths or solid geometry.

[Route-generation example](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/manufacturing_workflow.py)[Solid-export example](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/solid_export_workflow.py)

## Documentation and tutorials

[PyPI 4.40.0](https://pypi.org/project/fibernet/4.40.0/)[4.40.0 release notes](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/RELEASE_4_40_0.md)[Quick start](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/quickstart.rst)[Beam-FEM model and units](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/METHODS_BEAM_FEM_CONTRACT.md)[Examples](https://github.com/GellmanSparrowS/fibernet/tree/main/examples)[Complete notebook tutorial](https://github.com/GellmanSparrowS/fibernet/blob/main/tutorials/complete_tutorial_v4.ipynb)

Structure and simulation gallery (6 figures)

![Twelve 2D structures from the v3 gallery.](https://ml-biomat.com/static/images/fibernet/01_2d_gallery.webp?v=fce8466dc2ec)

Twelve 2D structures from the v3 gallery. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/01_2d_gallery.png)

![Eight saved honeycomb frames, colored by edge stretch ratio.](https://ml-biomat.com/static/images/fibernet/05_trajectory_dark.webp?v=49bfe332bfbb)

Eight saved honeycomb frames, colored by edge stretch ratio. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/05_trajectory_dark.png)

![Beam-frame FEM example, colored by sigma_total: absolute axial stress plus bending stress.](https://ml-biomat.com/static/images/fibernet/fem_showcase_dark.webp?v=9528bb432d96)

Beam-frame FEM example, colored by sigma_total: absolute axial stress plus bending stress. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/fem_showcase_dark.png)

![Voronoi-network example at a target stretch ratio of 1.5.](https://ml-biomat.com/static/images/fibernet/voronoi_1.5x_auto.webp?v=e8a06dbbbab0)

Voronoi-network example at a target stretch ratio of 1.5. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/voronoi_1.5x_auto.png)

![Classification example: confusion matrix, ROC, feature importance, and learning curve.](https://ml-biomat.com/static/images/fibernet/09_ml_analysis_dark.webp?v=1d577a2906f4)

Classification example: confusion matrix, ROC, feature importance, and learning curve. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/09_ml_analysis_dark.png)

![CEM search example: per-iteration objective values and the best value found so far.](https://ml-biomat.com/static/images/fibernet/11_rl_reward_dark.webp?v=6f458966f86e)

CEM search example: per-iteration objective values and the best value found so far. [Source figure](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/11_rl_reward_dark.png)
