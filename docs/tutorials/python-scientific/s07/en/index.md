# Seeing Inside Three-Dimensional Scientific Data

Source: https://ml-biomat.com/tutorials/python-scientific/s07/en/
Language: en

Connect spatial samples, isosurfaces, internal slices, and measurable geometry with PyVista.

## Once the outside is visible, how do we inspect the inside?

Microscopy tomography often arrives as a stack of grayscale slices. A simulation may instead store temperature, concentration, or displacement at many positions in space. Turning those values into a three-dimensional shape helps us understand orientation, connectivity, and internal location. Measuring a volume also requires understanding how that shape was constructed. In this chapter, PyVista connects the steps: build volume data with millimeter coordinates, extract an isosurface, inspect slices, and compare measured volumes and areas with known answers.

We begin with a constructed ellipsoidal model. Its mathematical expression and reference dimensions are known, so we can perform real three-dimensional operations while checking the resulting errors. The example helps explain workflows for particles, pores, or tissue outlines. Its values are calculated from an analytical field, and the threshold defines a chosen boundary. For experimental images, selecting a threshold also involves the meaning of the signal, background, and calibration.

The three-dimensional view establishes spatial relationships, the two-dimensional slice supports precise reading, and the error plot tests the discretized result. Rotating the camera can reveal a hidden side, but it does not improve the resolution of the input. A smoother-looking surface also need not have a more accurate volume. Keeping these views together makes it possible to identify what each operation actually changes.

## Assign a number to every position

A scalar field associates a position with one numerical value. Temperature in a room is an intuitive example; describing wind requires direction as well as magnitude and leads to a vector field. Here we assign a dimensionless value q to a position by dividing each coordinate by a reference length, squaring, and adding. This compresses the position's relationship to the origin into one number while retaining different characteristic sizes along the three directions.

$$
q(x,y,z)=\left(\frac{x}{a}\right)^2+\left(\frac{y}{b}\right)^2+\left(\frac{z}{c}\right)^2,\qquad q\leq\lambda
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eeaf78722a7e7f8494b85137.svg) | Three spatial coordinates relative to the center, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | Positive reference semiaxes of 3, 2, and 1 mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Dimensionless scalar value; positions sharing a value form an isosurface. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Positive dimensionless threshold; the interior has q no greater than this value. |

Each length divided by its reference length gives a dimensionless ratio. Squaring makes opposite directions contribute equally, and summing combines the three contributions. At (1.5, 1, 0.5) mm, q=(1.5/3)²+(1/2)²+(0.5/1)²=0.75, placing the point inside the λ=1 boundary. The isosurface semiaxes are a√λ, b√λ, and c√λ. At λ=0.5, the longest semiaxis is 3√0.5≈2.121320 mm. The threshold selects the region; it does not specify the distance between sampled points.

The reference lengths are 3, 2, and 1 mm. At (3, 0, 0) mm, only the first squared term is nonzero and q equals one. The same value occurs at (0, 2, 0) and (0, 0, 1) mm. All positions with q equal to one form an ellipsoid. These reference lengths are semiaxes, measured from the center to an endpoint; the complete axis lengths are 6, 4, and 2 mm. Think of a sphere stretched differently in three directions. Reaching the same scalar value requires moving farther along its longest direction.

An isosurface selects q equal to a threshold λ. We define the interior by q no greater than λ. Reducing λ from one to 0.5 multiplies every semiaxis by the square root of 0.5; increasing it to 1.5 enlarges all three. Lower q values lie closer to the center in this field, so the chosen interior is below the threshold. With another field, establish which side corresponds to the material or region being studied. Color brightness alone does not define inside and outside.

Threshold and grid resolution are different choices. The threshold changes the boundary being requested. Resolution changes how many samples describe the same field. Keeping them separate prevents an increase caused by selecting a larger region from being mistaken for improved numerical accuracy. We will refine samples at each fixed threshold, then compare results across three thresholds.

## Do array values and spatial cells have the same count?

PyVista's ImageData organizes regularly spaced sample positions and the connections between them. Three settings establish its geometry: dimensions gives the number of points along each direction, origin locates the first point, and spacing gives physical distances between neighboring points. A numerical table alone can store values; these spatial definitions tell the program how far apart the values are and which points form a small volume cell.

$$
h=\frac{x_{\max}-x_{\min}}{N-1},\qquad x_i=x_{\min}+ih,\quad i=0,\ldots,N-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Distance between neighboring sample points, in mm; equal along all three directions here. |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd27db42b5426d22e4e9954.svg) | First and last coordinates along the direction, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of sample points along each direction, a dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Point index beginning at zero, a dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | Coordinate of sample point i, in mm. |

There are N−1 intervals between N points, so the total length is divided by the interval count. With endpoints −4 and 4 mm and N=33, h=8/32=0.25 mm. Point 16 lies at −4+16×0.25=0 mm. Three directions with 33 points each produce 33³=35,937 points and 32³=32,768 volume cells. In an anisotropic dataset, calculate and store a separate spacing for each direction.

Each direction extends from −4 to 4 mm. Thirty-three points create thirty-two intervals, so spacing is 0.25 mm. The volume contains 35,937 points and 32,768 small cubic cells. The distinction resembles five marks on a ruler enclosing four intervals. Confusing point count with interval count shifts the physical endpoint and affects every subsequent geometric measurement. Coordinates and array shape must be interpreted together.

We store q in `point_data`, identifying values at sample points. In contrast, `cell_data` attaches one value to each cell, as is useful for cell averages or region labels. Those associations express different physical definitions. The example obtains coordinates directly from `grid.points` and calculates one q value for each, preserving their correspondence. Importing an existing three-dimensional NumPy array also requires checking axis order and flattening order. Matching the number of entries alone does not establish correct orientation.

Check positions with simple expected values: q is zero at the center and one at each reference semiaxis endpoint. At (1.5, 1, 0.5) mm, all three terms are 0.25, giving 0.75. Such checks connect coordinates, units, and array association. With experimental stacks, also establish whether the separation between slices equals the in-plane pixel spacing. Different spacings are allowed; the displayed geometry should respect their physical proportions.

## Where does the surface cross between eight samples?

Lorensen and Cline introduced Marching Cubes in 1987 to construct surfaces from three-dimensional medical imaging samples. The algorithm examines eight neighboring corner values, locates threshold crossings along cell edges, and connects crossings with triangles. The 2019 PyVista paper presents a Python interface to VTK's three-dimensional plotting and mesh analysis. Here, specifying `method='marching_cubes'` applies the actual algorithm to our sampled field.

![An actual Marching Cubes cell and edge interpolation. Two triangles on the left are extracted by the native algorithm from eight sampled values. The right panel compares linear interpolation with the analytical field on one edge, explaining crossing positions of 0.6667 and 0.7071 mm. Corner colors identify threshold sides; axes retain physical length.](https://ml-biomat.com/static/tutorials/python-scientific/figures/c5c902f03b90899972303aff.svg?v=c5c902f03b90)

Figure 1An actual Marching Cubes cell and edge interpolation. Two triangles on the left are extracted by the native algorithm from eight sampled values. The right panel compares linear interpolation with the analytical field on one edge, explaining crossing positions of 0.6667 and 0.7071 mm. Corner colors identify threshold sides; axes retain physical length.

The left panel shows one actual cell from the example. Blue corners have q below one and orange corners have q above one. Edges connecting the two states contain boundary crossings. The local triangular patch is generated by the native algorithm. Numbers beside the corners are scalar values, while the coordinate axes separately report millimeters. Because surface vertices can lie between cell corners, the representation locates a boundary more finely than stacking entire cubic blocks.

$$
\eta=\frac{\lambda-q_0}{q_1-q_0},\qquad \mathbf r_* =\mathbf r_0+\eta(\mathbf r_1-\mathbf r_0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ff4c8bab0ec6e039de68ecf.svg) | Distinct dimensionless scalar values at the two edge endpoints. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Dimensionless threshold between the endpoint values. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Dimensionless fraction of the edge traveled from its first endpoint. |
| ![Formula](https://ml-biomat.com/static/agent-math/f27dee343dec5fb058859f85.svg) | Endpoint position vectors, each component in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/a0037efc1d28fcdd3514849d.svg) | Interpolated crossing position vector, in mm. |

Linear variation means that traveling a fraction of the edge produces the same fraction of its scalar change. On the vertical edge shown, q₀=0.75, q₁=1.5, and λ=1, so η=0.25/0.75=1/3. Starting at z=0.5 mm and adding one third of 0.5 mm gives z=2/3 mm. The analytical field on that edge is q=0.5+(z/mm)², giving a crossing at √0.5 mm≈0.707107 mm. Their difference is approximately 0.040440 mm. This calculation assumes different endpoint values and a threshold crossing within the edge.

The right panel isolates one edge. Its x coordinate is fixed at 1.5 mm and y at 1 mm. As z rises from 0.5 to 1 mm, q rises from 0.75 to 1.5. Assuming linear variation, reaching q equal to one requires one third of the total change, placing the crossing near 0.6667 mm. The known analytical field places it near 0.7071 mm. Their separation directly displays the approximation introduced by using endpoint values and linear interpolation.

Refinement shortens the distance between endpoints, making a curved relationship closer to a line over each local interval. Complex fields may contain thin features or multiple changes within one cell; representing them requires appropriate sampling or a richer data model. The current smooth, single, convex ellipsoid makes the interpolation effect easy to trace. The local cell diagram shows the same construction used in the complete surface.

## A slice of the field differs from a slice of its surface

`grid.contour([1.0], scalars='q', method='marching_cubes')` extracts the surface at q equal to one. Its PolyData output stores vertices and the triangular faces connecting them. The brackets have a specific purpose: a one-item list requests that scalar value, whereas an integer argument of one requests one automatically chosen contour. Extracting the surface leaves the original volume data available. The surface is one geometric representation of that field.

Now place a horizontal plane at z equal to 0.5 mm. Slicing the original volume produces a two-dimensional mesh carrying q values, which can be displayed using color. Slicing the ellipsoid surface produces intersection lines. Those lines enclose a cross-section but do not themselves fill it. The left panel fills the enclosed polygon in orange to locate the section; the right panel compares its boundary with the analytical ellipse on equally scaled physical axes.

![Two views of the same analytical teaching field. The native VTK rendering locates the orange section at z₀=0.5 mm inside a transparent ellipsoid. The right panel slices the original volume and overlays the mesh intersection and analytical boundary in physical coordinates. The color scale encodes dimensionless q; transparency affects visibility, while geometry determines lengths and areas.](https://ml-biomat.com/static/tutorials/python-scientific/figures/2efe4b740671331580625386.svg?v=2efe4b740671)

Figure 2Two views of the same analytical teaching field. The native VTK rendering locates the orange section at z₀=0.5 mm inside a transparent ellipsoid. The right panel slices the original volume and overlays the mesh intersection and analytical boundary in physical coordinates. The color scale encodes dimensionless q; transparency affects visibility, while geometry determines lengths and areas.

A plane needs both location and orientation. Here, origin specifies a point at (0, 0, 0.5) mm, and normal=(0, 0, 1) specifies the perpendicular direction, making the plane parallel to the xy plane. Imagine a short arrow standing upright on a sheet of paper: it defines the sheet's orientation. Moving the sheet along the arrow explores successive heights. Oblique cuts follow the same principle with a different normal and a chosen point.

The three-dimensional view shows where the section lies inside the object. Use the two-dimensional view for reading widths. Its horizontal and vertical directions both use millimeters at equal scale, preserving the ellipse's aspect ratio. Colors come from q on the sliced field, the orange boundary from the surface intersection, and the white dashed ellipse from the analytical model. Changing a color map alters the display; changing the threshold moves the selected boundary.

## Give volume and area an answer to check against

At threshold λ, each ellipsoid semiaxis equals its reference value multiplied by the square root of λ. Stretching a unit sphere along three directions multiplies its volume by the three length factors, explaining the product of semiaxes. Fixing a slice height and moving its squared-coordinate contribution to the other side leaves a two-dimensional ellipse. These relationships provide analytical volume and area values against which discrete measurements can be compared.

$$
V_\lambda=\frac{4\pi abc}{3}\lambda^{3/2},\qquad A_\lambda(z_0)=\pi ab\max\!\left[\lambda-\left(\frac{z_0}{c}\right)^2,0\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2a5cff4651c7a5c7f4a2bf9b.svg) | Analytical ellipsoid volume at threshold λ, in mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/f957e27f053a9767e0816a17.svg) | Analytical cross-sectional area at height z₀, in mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | Reference semiaxes of 3, 2, and 1 mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Positive dimensionless threshold. |
| ![Formula](https://ml-biomat.com/static/agent-math/b72465f81bed2e150afe1243.svg) | Horizontal slice height relative to the center, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant, approximately 3.141593, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/61b9dc3596ef4f553078d1bb.svg) | Choose the larger of u and zero; a plane outside the object has zero area. |

Stretching a sphere multiplies volume by the three length factors, producing abc and λ to the power 3/2. At a fixed height, the remaining squared-coordinate sum is λ−(z₀/c)². Each section semiaxis contains the square root of this remainder, so their product contains the remainder itself. At λ=1, V=4π×3×2×1/3=8π≈25.132741 mm³. At z₀=0.5 mm, A=π×3×2×(1−0.25)=4.5π≈14.137167 mm². For |z₀|≥c√λ, the section has zero area.

For λ equal to one, volume is 8π mm³, approximately 25.132741 mm³. At z equal to 0.5 mm, the remaining scalar contribution is 0.75. The section has semiaxes approximately 2.598076 and 1.732051 mm, with area 4.5π mm², approximately 14.137167 mm². At z equal to 1 mm, the section contracts to a point with zero area. Above it, the plane no longer intersects the ellipsoid. Both the program and interactive display retain this empty-section case.

A closed triangular surface defines the enclosed mesh volume. The code checks for open edges before reading `surface.volume`, then independently sums the signed tetrahedra formed by each face and the origin. Closedness matters: cutting away half a surface without capping the opening leaves an incomplete boundary. Before measuring other meshes, inspect self-intersections, duplicate faces, and inconsistent orientation as well. Each can affect the definition of the enclosed region.

$$
V_h=\frac{1}{6}\left|\sum_{j=1}^{M}\mathbf p_j\cdot(\mathbf q_j\times\mathbf r_j)\right|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eea286090480eac2f8dfd8fa.svg) | Volume enclosed by a closed, consistently oriented triangle mesh, in mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Number of triangular faces, a dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Face index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9c8b8a36b95f4c9f91eaff7d.svg) | Position vectors of the three vertices of face j, in mm; bold q here is a position vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/fc15a27a41ba825be39eec62.svg) | Cross and dot products; the scalar triple product gives a signed parallelepiped volume. |

A triangular face and the origin define a tetrahedron with one sixth of the corresponding parallelepiped volume. With consistent face orientation, signed contributions cancel internally and leave the volume enclosed by the closed boundary. Vertices at (1,0,0), (0,1,0), and (0,0,1) mm give a scalar triple product of 1 mm³ and a tetrahedron volume of 1/6 mm³. The example compares this separate sum with VTK volume; both give 24.597686 mm³ for the default mesh. The order of each face’s vertices controls its sign.

Cross-sectional area is calculated from ordered boundary points. For this single convex ellipse, sorting intersections by angle around their center gives their boundary order, after which a polygon area calculation applies. Multiple separate regions, holes, or concave outlines require preserving the original connections and handling outer boundaries and holes appropriately. The sorting function in this example is tied to the convex-section geometry, making that assumption visible in the measurement method.

$$
A_h=\frac12\left|\sum_{i=1}^{K}(x_i y_{i+1}-y_i x_{i+1})\right|,\qquad (x_{K+1},y_{K+1})=(x_1,y_1)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/31940250be2dad706c01f020.svg) | Area enclosed by the section polygon, in mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Number of vertices ordered along the boundary, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Boundary vertex index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0628201b1fcd40d880b250aa.svg) | Planar coordinates of vertex i, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/bb35f800746b473b95c8a4f8.svg) | First vertex repeated to close the final edge, in mm. |

Two neighboring vertices and the origin define a small triangle; each term is twice its signed area. Summing around the boundary gives the polygon area. For rectangle vertices (0,0), (3,0), (3,2), and (0,2) mm, the two nonzero contributions are each 6 mm², giving (6+6)/2=6 mm². This chapter has a single convex polygon, whose boundary order can be obtained by sorting angles. Sections with holes or separate components require explicit handling of their boundary connections and orientations.

## Refine samples and inspect geometric convergence

Fix λ at one and use 17, 33, then 65 points in each direction. The corresponding spacings are 0.5, 0.25, and 0.125 mm. Domain, analytical field, and extraction method stay the same. Computed volumes are approximately 22.987597, 24.597686, and 24.999078 mm³, approaching the analytical value of 25.132741 mm³. These numbers reveal the effect of resolution more directly than comparing rendered surfaces alone.

$$
e_V=100\frac{|V_h-V_\lambda|}{V_\lambda}\%,\qquad e_A=100\frac{|A_h-A_\lambda|}{A_\lambda}\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/02db18e605a00a9e29f6ccd1.svg) | Relative errors in volume and section area, expressed as percentages. |
| ![Formula](https://ml-biomat.com/static/agent-math/2ad35a603be4d743d1325439.svg) | Volume and section area measured on a grid of spacing h, in mm³ and mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/161ce06a736c5e1390bbed5e.svg) | Analytical volume and section area at the same threshold and slice, in mm³ and mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Sample spacing, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | Absolute value, retaining the magnitude of the discrepancy. |

Subtract the reference, take the magnitude, and divide by the reference to compare objects of different sizes. The default volume error is 100×|24.597686−25.132741|/25.132741≈2.129%, while its section-area error is approximately 0.500%. A zero-area section has no nonzero denominator for relative area error. The page reports zero area and an empty-section label in that case. The static area-error comparison uses z₀=0.5 mm, where all three selected thresholds have positive reference areas.

Volume errors are approximately 8.535%, 2.129%, and 0.532%. For this smooth model and these grids, halving the spacing reduces the error by roughly a factor of four. Cross-sectional area also approaches its reference, but it measures a different geometric quantity and need not have the same error. Separate panels show that a section can already have a small area error while the complete boundary still accumulates a larger volume error.

![Volume and section-area errors from nine actual mesh extractions. Both plots use logarithmic axes, with section areas evaluated at z₀=0.5 mm. The table records triangle count, volume, and error for every resolution and threshold. Halving spacing reduces default-threshold volume error by approximately a factor of four.](https://ml-biomat.com/static/tutorials/python-scientific/figures/4a1d5a2c586420bf37af297c.svg?v=4a1d5a2c5864)

Figure 3Volume and section-area errors from nine actual mesh extractions. Both plots use logarithmic axes, with section areas evaluated at z₀=0.5 mm. The table records triangle count, volume, and error for every resolution and threshold. Halving spacing reduces default-threshold volume error by approximately a factor of four.

The plots also compare three thresholds. A smaller threshold selects a smaller ellipsoid, making the same 0.5 mm spacing coarser relative to its dimensions and producing a larger relative error. The extraction rule has stayed fixed; the ratio of sample spacing to object size has changed. Reporting both spacing and the size of the feature being examined is therefore more informative than reporting the point count alone.

Refinement increases data size. Doubling interval count in each of three directions multiplies the number of volume cells by eight. The number of surface triangles depends on how the boundary crosses those cells; the table records actual counts. This puts accuracy and computational cost side by side. With an experimental field lacking a closed-form reference, keep processing conditions consistent, examine target quantities under refinement, and relate the required precision to imaging resolution and measurement uncertainty.

## Save the geometry and the basis of its measurements

The complete program creates nine real PyVista triangle meshes: three thresholds at three resolutions. Each receives an enclosed-volume calculation and native intersection cuts at six heights. VTK renders the default three-dimensional view off screen, while Matplotlib produces the two-dimensional and convergence figures. Off-screen rendering writes an image directly to a file, helping reproduce a specified view; desktop exploratory work can also open an interactive Plotter window.

### Complete example: volume data, meshes, sections, measurements, and figures

Run python main.py --output outputs --language en for English figures and all numerical outputs; use zh for Chinese. Dependencies are NumPy, PyVista, and Matplotlib, with VTK installed through PyVista. The program saves vertices, faces, and six native slices for each of nine meshes. The default uses N=33, λ=1, and z₀=0.5 mm. Outputs include a native VTK rendering, three scientific figures, reusable VTI/VTP geometry files, and a numerical summary.

```
"""Extract, slice, measure, and render an analytical ellipsoid field with PyVista."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import pyvista as pv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib import font_manager
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

AXES = np.array([3., 2., 1.])  # mm: reference semiaxes at q = 1
RESOLUTIONS = [17, 33, 65]
LEVELS = [.5, 1., 1.5]
SLICE_Z = [0., .25, .5, .75, 1., 1.25]  # mm


def scalar_field(points):
    return np.sum((points / AXES)**2, axis=1)


def create_grid(n):
    spacing = 8. / (n - 1)
    grid = pv.ImageData(dimensions=(n, n, n), spacing=(spacing,)*3, origin=(-4.,)*3)
    grid.point_data['q'] = scalar_field(grid.points)
    return grid


def polygon_slice(surface, z):
    """Use VTK to cut the surface, then order this convex ellipse's boundary."""
    cut = surface.slice(normal=(0, 0, 1), origin=(0, 0, z))
    if cut.n_points < 3:
        return np.empty((0, 2)), 0.
    points = np.unique(cut.points[:, :2], axis=0).astype(float)
    center = points.mean(axis=0)
    order = np.argsort(np.arctan2(points[:, 1]-center[1], points[:, 0]-center[0]))
    points = points[order]
    area = abs(np.dot(points[:, 0], np.roll(points[:, 1], -1))
               - np.dot(points[:, 1], np.roll(points[:, 0], -1))) / 2
    return points, float(area)


def analytic_volume(level):
    return 4 * math.pi * np.prod(AXES) * level**1.5 / 3


def analytic_area(level, z):
    return math.pi * AXES[0] * AXES[1] * max(level-(z/AXES[2])**2, 0.)


def triangle_volume(surface):
    """Independent signed tetrahedron sum for a consistently oriented closed mesh."""
    faces = surface.faces.reshape(-1, 4)[:, 1:]
    a, b, c = (surface.points[faces[:, i]].astype(float) for i in range(3))
    return abs(float(np.sum(np.einsum('ij,ij->i', a, np.cross(b, c))) / 6))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    tr = lambda z, e: z if args.language == 'zh' else e
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ['Noto Sans CJK SC','Noto Sans SC',
        'Microsoft YaHei','SimHei','DejaVu Sans'] if f in fonts], 'font.size': 12,
        'svg.fonttype':'none', 'axes.spines.top':False, 'axes.spines.right':False, 'grid.alpha':.16})
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)

    records, mesh_bank, surfaces = [], {}, {}
    for n in RESOLUTIONS:
        grid = create_grid(n)
        for level in LEVELS:
            # A one-item list requests this value; integer 1 would request one automatic contour.
            surface = grid.contour([level], scalars='q', method='marching_cubes').triangulate()
            assert surface.n_open_edges == 0
            assert surface.is_all_triangles
            volume = float(surface.volume)
            independent = triangle_volume(surface)
            assert math.isclose(volume, independent, rel_tol=2e-7, abs_tol=2e-7)
            slices = []
            for z in SLICE_Z:
                poly, area = polygon_slice(surface, z)
                slices.append({'z':z, 'points':poly.tolist(), 'area':area,
                               'exact_area':float(analytic_area(level, z))})
            mid = slices[2]
            key = f'{n}-{level:g}'
            mesh_bank[key] = {'n':n, 'level':level, 'spacing':8/(n-1),
                'points':surface.points.tolist(), 'faces':surface.faces.reshape(-1,4)[:,1:].tolist(),
                'volume':volume, 'exact_volume':float(analytic_volume(level)), 'slices':slices}
            surfaces[key] = surface
            records.append({'n':n,'level':level,'spacing_mm':8/(n-1),'points':surface.n_points,
                'triangles':surface.n_cells,'open_edges':surface.n_open_edges,'volume_mm3':volume,
                'independent_volume_mm3':independent,'exact_volume_mm3':float(analytic_volume(level)),
                'volume_error_percent':100*abs(volume/analytic_volume(level)-1),
                'slice_area_mm2':mid['area'],'exact_slice_area_mm2':mid['exact_area'],
                'slice_error_percent':100*abs(mid['area']/mid['exact_area']-1)})
    (args.output/'mesh-bank.json').write_text(json.dumps(mesh_bank,separators=(',',':')),encoding='utf-8')
    columns=list(records[0]);np.savetxt(args.output/'convergence.csv',
        [[row[k] for k in columns] for row in records],delimiter=',',header=','.join(columns),comments='')
    default=surfaces['33-1']; default_grid=create_grid(33)
    default.save(args.output/'ellipsoid.vtp');default_grid.save(args.output/'scalar-grid.vti')
    field_plane=default_grid.slice(normal='z',origin=(0,0,.5)).triangulate()
    field_plane.save(args.output/'field-slice.vtp')
    cut_points, cut_area=polygon_slice(default,.5)

    # Render the actual VTK geometry; physical coordinates are in millimeters.
    plotter=pv.Plotter(off_screen=True,window_size=(1100,850))
    plotter.set_background('white')
    plotter.add_mesh(default,color='#477f9b',opacity=.25,smooth_shading=False)
    loop=np.column_stack([cut_points,np.full(len(cut_points),.5)])
    disk=pv.PolyData(loop,np.r_[len(loop),np.arange(len(loop))]).triangulate()
    plotter.add_mesh(disk,color='#c8753c',opacity=.85)
    plotter.add_mesh(pv.lines_from_points(loop,close=True),color='#8f451d',line_width=4)
    # Coordinate rulers sit outside the object; each tick keeps its physical position.
    ruler_origin=np.array([-3.6,-2.6,-1.4])
    label_points=[];label_text=[]
    for axis,end,ticks in [(0,3.6,[-3,0,3]),(1,2.6,[-2,0,2]),(2,1.4,[-1,0,1])]:
        endpoint=ruler_origin.copy();endpoint[axis]=end
        plotter.add_mesh(pv.Line(ruler_origin,endpoint),color='#617780',line_width=1.4)
        for tick in ticks:
            location=ruler_origin.copy();location[axis]=tick
            label_points.append(location);label_text.append(str(tick))
        middle=ruler_origin.copy();middle[axis]=(ruler_origin[axis]+end)/2
        middle[(axis+1)%3]+= .35 if axis==2 else (-1.0 if axis==0 else -.55)
        label_points.append(middle);label_text.append(['x / mm','y / mm','z / mm'][axis])
    plotter.add_point_labels(np.array(label_points),label_text,font_size=23,text_color='#263b46',
        show_points=False,shape=None,always_visible=True)
    plotter.camera_position=[(7,-10,6),(0,0,0),(0,0,1)]
    plotter.enable_parallel_projection()
    plotter.camera.zoom(.85)
    plotter.show(screenshot=args.output/'native-surface.png')

    fig,axes=plt.subplots(1,2,figsize=(13,6.2),layout='constrained',gridspec_kw={'width_ratios':[1.05,1]})
    axes[0].imshow(plt.imread(args.output/'native-surface.png'));axes[0].axis('off')
    axes[0].set_title(tr('A  等值面与内部切片的位置','A  Surface and internal slice position'))
    xy=field_plane.points[:,:2];tri=field_plane.faces.reshape(-1,4)[:,1:]
    colored=axes[1].tripcolor(mtri.Triangulation(xy[:,0],xy[:,1],tri),field_plane['q'],
        shading='gouraud',cmap='cividis',vmin=0,vmax=7)
    close=np.vstack([cut_points,cut_points[0]])
    axes[1].plot(close[:,0],close[:,1],color='#e98a43',lw=2.4,label=tr('网格切片边界','Mesh intersection'))
    theta=np.linspace(0,2*np.pi,501);radius=np.sqrt(.75)
    axes[1].plot(3*radius*np.cos(theta),2*radius*np.sin(theta),'--',color='white',lw=1.6,label=tr('解析边界','Analytical boundary'))
    axes[1].set(xlim=(-4,4),ylim=(-4,4),aspect='equal',xlabel='x / mm',ylabel='y / mm',
        title=tr('B  在z = 0.5 mm处读内部数值','B  Read values at z = 0.5 mm'))
    axes[1].legend(loc='upper right',fontsize=10)
    fig.colorbar(colored,ax=axes[1],shrink=.8,label=tr('标量q / 无量纲','Scalar q / dimensionless'))
    fig.suptitle(tr('同一体数据：N = 33，等值面q = 1','One volume dataset: N = 33, isosurface q = 1'),fontsize=16)
    save(fig,'surface-and-slice')

    # A real marching-cubes cell, plus one edge where interpolation is hand-checkable.
    cell=pv.ImageData(dimensions=(2,2,2),spacing=(.5,.5,.5),origin=(1.5,1.,.5))
    cell['q']=scalar_field(cell.points)
    patch=cell.contour([1.],scalars='q',method='marching_cubes').triangulate()
    fig=plt.figure(figsize=(12.6,6.8),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.1,1])
    ax=fig.add_subplot(gs[0],projection='3d')
    pts=cell.points
    for i in range(8):
        for j in range(i):
            if np.count_nonzero(np.abs(pts[i]-pts[j])>1e-10)==1:
                ax.plot(*np.array([pts[i],pts[j]]).T,color='#899ba6',lw=1.2)
    faces=patch.faces.reshape(-1,4)[:,1:]
    ax.add_collection3d(Poly3DCollection(patch.points[faces],facecolors='#72a7bc',edgecolors='#28658c',alpha=.65,lw=1.5))
    ax.scatter(*pts.T,c=np.where(cell['q']<1,'#28658c','#c26835'),s=48,depthshade=False)
    for point,q in zip(pts,cell['q']):ax.text(*(point+np.array([.015,.015,.025])),f'{q:.3f}',fontsize=10)
    ax.set(xlabel='x / mm',ylabel='y / mm',zlabel='z / mm',xticks=[1.5,2],yticks=[1,1.5],zticks=[.5,1],
        title=tr('A  八个采样值决定局部三角面','A  Eight samples define a local patch'))
    ax.set_box_aspect((1,1,1));ax.view_init(elev=23,azim=-63)
    ax=fig.add_subplot(gs[1]);zz=np.linspace(.5,1,200)
    ax.plot(zz,.5+zz**2,color='#28658c',lw=2.5,label=tr('解析场：q = 0.5 + (z/mm)²','Known field: q = 0.5 + (z/mm)²'))
    ax.plot([.5,1],[.75,1.5],'o--',color='#c26835',lw=2,label=tr('边上的线性插值','Linear interpolation on edge'))
    ax.axhline(1,color='#677b86',lw=1.2)
    ax.scatter([2/3,np.sqrt(.5)],[1,1],s=65,c=['#c26835','#28658c'],zorder=4)
    ax.annotate('0.6667 mm',(2/3,1),xytext=(.51,1.15),arrowprops={'arrowstyle':'->','color':'#c26835'},color='#a65329')
    ax.annotate('0.7071 mm',(np.sqrt(.5),1),xytext=(.74,.85),arrowprops={'arrowstyle':'->','color':'#28658c'},color='#28658c')
    ax.set(xlabel='z / mm',ylabel=tr('标量q / 无量纲','Scalar q / dimensionless'),
        title=tr('B  同一条边：交点怎样确定','B  One edge: locating the crossing'))
    ax.legend(loc='upper left',fontsize=10);ax.grid(True)
    fig.suptitle(tr('1987年Marching Cubes：从相邻采样值构造边界','Marching Cubes, 1987: constructing a boundary from neighboring samples'),fontsize=15)
    save(fig,'history-interpolation')

    fig=plt.figure(figsize=(12.8,8.5),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.25,1])
    axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1])]
    for level,color in zip(LEVELS,['#28658c','#2b8a74','#c26835']):
        group=[r for r in records if r['level']==level]
        for ax,key in zip(axs,['volume_error_percent','slice_error_percent']):
            ax.loglog([r['spacing_mm'] for r in group],[r[key] for r in group],'o-',color=color,lw=2,label=f'λ = {level:g}')
    for ax,title in zip(axs,[tr('A  封闭网格体积误差','A  Enclosed mesh volume error'),tr('B  z = 0.5 mm处的面积误差','B  Area error at z = 0.5 mm')]):
        ax.set(title=title,xlabel=tr('网格间距 / mm','Grid spacing / mm'),ylabel=tr('相对误差 / %','Relative error / %'))
        ax.set_xticks([.125,.25,.5],labels=['0.125','0.25','0.5']);ax.minorticks_off();ax.legend();ax.grid(True)
    ax=fig.add_subplot(gs[1,:]);ax.axis('off')
    labels=['N','h / mm','λ',tr('三角面数','Triangles'),'V / mm³',tr('体积误差 / %','Volume error / %')]
    rows=[[r['n'],f"{r['spacing_mm']:.3f}",f"{r['level']:g}",r['triangles'],f"{r['volume_mm3']:.5f}",f"{r['volume_error_percent']:.3f}"] for r in records]
    table=ax.table(cellText=rows,colLabels=labels,loc='center',cellLoc='center',bbox=[0,.0,1,.96])
    table.auto_set_font_size(False);table.set_fontsize(11)
    for (i,j),cell in table.get_celld().items():cell.set_facecolor('#eaf1f4' if i==0 else 'white');cell.set_edgecolor('#d2dfe5')
    fig.suptitle(tr('固定解析场，仅改变采样间距；参考答案由椭球公式给出',
        'One analytical field, different sample spacings; ellipsoid formulas provide the reference'),fontsize=15)
    save(fig,'convergence')

    baseline=next(row for row in records if row['n']==33 and row['level']==1)
    summary={'pyvista_version':pv.__version__,'vtk_version':pv.vtk_version_info._asdict(),
        'reference_semiaxes_mm':AXES.tolist(),'reference_volume_mm3':float(analytic_volume(1)),
        'reference_area_z05_mm2':float(analytic_area(1,.5)),'default':baseline,'records':records,
        'single_cell_triangles':patch.n_cells,'edge_linear_crossing_mm':2/3,
        'edge_exact_crossing_mm':float(np.sqrt(.5)),
        'field_slice_points':field_plane.n_points,'field_slice_triangles':field_plane.n_cells}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
```

The output `scalar-grid.vti` preserves the regular grid and q values. `ellipsoid.vtp` stores the default surface, and `field-slice.vtp` stores the two-dimensional mesh carrying field values. PyVista can read these geometries again. `convergence.csv` contains nine measurement records, `summary.json` keeps key numerical results, and `mesh-bank.json` stores vertices, faces, and sections for the page. Images communicate a result, while geometries and tables support further calculations.

Start reading the program through create_grid, contour, and slice, then inspect the volume and area checks. The default N=33, λ=1 surface contains 1,054 vertices and 2,104 triangles. Its volume is approximately 24.597686 mm³ and its area at z=0.5 mm is approximately 14.066500 mm². The analytical references remain 25.132741 mm³ and 14.137167 mm². Preserving the numerical table connects every visual change to a specific setting.

The displayed surface retains its actual triangular geometry, without moving vertices through a geometric smoothing operation. Lighting and transparency help locate objects, while measurements use the same underlying mesh. If a later workflow adds simplification, smoothing, or repair, save quantities before and after the operation. This shows whether it changes the volume, pore size, or connectivity that matters to the investigation.

## Vary threshold, height, and resolution separately

Keep the default threshold and resolution, then move the slice upward. The orange section moves through the three-dimensional object, its two-dimensional boundary shrinks, and its area decreases. The full ellipsoid volume stays fixed. This page reads the actual meshes and sections generated beforehand by the complete Python program; Plotly displays the three-dimensional geometry. Camera rotation explores those objects, while the two-dimensional comparison keeps its physical scale.

## Experiment: three linked views of one volume dataset

Move the slice to compare position and area, then hold its height fixed while varying resolution or threshold. Meshes and intersections at six heights are actual PyVista outputs from the complete Python program. The dashed blue ellipse is analytical; the continuous area curve is analytical, and circles mark six native cuts.

### Spatial position: blue surface and orange section

Drag the 3D view to rotate, or use the keyboard-accessible view menu. The faint orange plane marks slice height even outside the object. Three-dimensional axes preserve physical proportions; the planar view below uses equal millimeter scaling.

### Section geometry: mesh and analytical boundary

[Figure: Equal-scale XY section and analytical boundary](https://ml-biomat.com/tutorials/python-scientific/s07/en/#S07-section-svg)

### How section area changes with height

[Figure: Analytical area curve and areas of six actual mesh cuts](https://ml-biomat.com/tutorials/python-scientific/s07/en/#S07-area-svg)

Next, hold the slice at 0.5 mm and change only the resolution. Analytical volume and ellipse remain fixed, while the mesh boundary, face count, and errors update. Finally, change the threshold: the analytical answers now change too, because a different region has been selected. At a slice height of 1.25 mm, all three selectable ellipsoids lie below the plane. The page retains the complete surface and volume, with an empty section and zero area.

Increase opacity to experience occlusion: the outside becomes clearer and the interior section becomes harder to see. Lower opacity or switch to a top view to locate it again. The two-dimensional view provides a stable reading instead of requiring lengths to be guessed from a three-dimensional projection. These comparisons establish a practical sequence for real volume data: confirm correspondence between values and coordinates, define the desired region, and use sections and geometric quantities to examine its three-dimensional display.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [PyVista: Creating a Uniform Grid](https://docs.pyvista.org/examples/00-load/create_uniform_grid.html)

   Definitions of point/cell association, dimensions, origin, and spacing.

   PyVista documentation and software: MIT; original example and figures here.
2. [PyVista: Contouring](https://docs.pyvista.org/examples/01-filter/contouring.html)

   Extracting an isosurface from a three-dimensional scalar field.

   MIT
3. [PyVista: DataSetFilters.contour](https://docs.pyvista.org/api/core/_autosummary/pyvista.datasetfilters.contour)

   Contour-value lists, contour counts, and the marching_cubes method argument.

   MIT
4. [PyVista: Slicing](https://docs.pyvista.org/examples/01-filter/slice.html)

   Defining slices through a normal direction and plane location.

   MIT
5. [PyVista: PolyData.volume](https://docs.pyvista.org/api/core/_autosummary/pyvista.polydata.volume)

   Measuring volume from a closed triangle mesh.

   MIT
6. [Lorensen & Cline (1987), Marching Cubes: A High Resolution 3D Surface Construction Algorithm](https://graphics.stanford.edu/courses/cs348a-20-winter/Papers/Marching_Cubes.pdf)

   The isosurface problem in medical volume data and linear interpolation along cell edges.

   Original paper consulted for historical and technical facts; no paper figures reproduced.
7. [Sullivan & Kaszynski (2019), PyVista: 3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK)](https://joss.theoj.org/papers/10.21105/joss.01450)

   The PyVista–VTK interface and publication history.

   JOSS article CC BY 4.0; software MIT.
