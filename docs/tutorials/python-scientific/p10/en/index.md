# Coordinates, Matrices, and Image Calibration

Source: https://ml-biomat.com/tutorials/python-scientific/p10/en/
Language: en

Calibrate a pixel scale, understand least squares through residuals, and rotate an entire coordinate array.

## How long is a hundred pixels?

After photographing a thin fibre, we can count how many pixels it spans. A pixel identifies a sampling position in the image; it does not yet tell us the fibre's physical length. The same fibre can span very different numbers of pixels at different magnifications. A small camera rotation also turns a nearly horizontal fibre into a sloping line. To obtain comparable measurements, we need to connect pixels to a known physical scale and describe directions consistently. This chapter joins those tasks in a small calibration experiment, using matrix multiplication, vector lengths, and least squares.

Imagine placing a ruler in the field of view and reading its image coordinate at six known positions. Our constructed teaching records use positions of 0, 2, 4, 6, 8, and 10 mm, with corresponding readings of 1, 42, 80, 120, 162, and 201 px. The values lie near a straight line, with small differences that make the calculations easy to inspect. The ruler's 0 mm position appears at an image reading of 1 px. These zeros belong to different coordinate systems, so they need not coincide. Small departures from a straight line could arise during rounding or localization; here they are simply specified deviations in the constructed records.

We then consider a rectangular image region spanning 200 px horizontally and 80 px vertically. Its lower-left corner is the origin for our geometry. Pixels are square, both directions use the same scale, and the vertical coordinate has been converted to the upward direction used in mathematics. Calibration determines the rectangle's width in millimetres; rotation determines its vertex coordinates after turning. An image with substantial distortion or different horizontal and vertical scales calls for a calibration relationship that describes those features. Our calculation represents a planar image with a uniform scale over the region being measured.

The same workflow supports particle outlines, markers in tensile-test photographs, and dimensions measured from scans. Rotating a shape on screen should preserve its distances. Converting its pixel coordinates to millimetres requires a dimensioned scale factor. These operations serve different purposes, even though both change the numbers in a coordinate array. Once their rules are explicit, hundreds of outline points can follow the same procedure as the four vertices used here.

## A vector begins with two directions

Start at an origin, move 2 mm to the right, and then 1 mm upward. The destination has coordinates (2, 1) mm. We can represent this pair by a vector: an arrow from the origin to the point. Its components record horizontal and vertical displacement, while its length measures the direct distance between the endpoints. The two components form the legs of a right triangle, so the Pythagorean theorem supplies the distance. A component's sign records direction; squaring the components before adding produces a length that does not depend on which side of the origin the point occupies.

$$
r=\|\mathbf v\|_2=\sqrt{x^2+y^2},\qquad \mathbf v=\begin{bmatrix}x\\y\end{bmatrix}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Vector length, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/771507e21f2935d77160257f.svg) | Planar displacement vector; both components in mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Horizontal and vertical displacements, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ab7d58f94422b5ef65d1d1a3.svg) | Euclidean norm; subscript 2 identifies the square-sum-root rule |

Apply the Pythagorean theorem to perpendicular axes using the same length unit. With x=2 mm and y=1 mm, r=√5 mm≈2.236 mm. The rotated coordinates (-1,2) mm give the same length. Squaring produces mm²; the square root restores mm.

A 90° counterclockwise turn takes this arrow to (-1, 2) mm. The negative horizontal coordinate places the point to the left of the origin; the length remains positive. Before and after rotation, the distance is the square root of 5 mm, approximately 2.236 mm. This small calculation provides a useful program check. The answer (1, -2) would indicate the opposite rotation direction. An answer of (0, 0) would suggest an incorrect operation. Coordinates become testable physical quantities once we connect their numerical values to this geometry.

For several points, we arrange a NumPy array with one point per row and one coordinate component per column. Four rectangle vertices form an array with shape (4, 2): four points, each with two components. The array may resemble an earlier table with one experimental run per row, but its axes now mean something different. Calling `np.linalg.norm(points, axis=1)` combines the two components within each row and returns four distances. Omitting the axis combines the entire array into one number, which answers a different question.

The origin must remain consistent throughout a calculation. Measured from the rectangle's lower-left corner, the four vertex distances are 0, 10, approximately 10.770, and 4 mm. Moving the origin to the centre changes all four of these distances, while leaving the distances between pairs of vertices unchanged. To measure the separation between two points, subtract the starting coordinate from the ending coordinate and take the length of the resulting displacement vector. Their common origin disappears in the subtraction. This is why image measurements often begin with a difference between two coordinates.

![Original and rotated rectangles, unit-direction arrows, and four preserved distances.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a7a1d1f3a485e0564a3e03c3.svg?v=a7a1d1f3a485)

Figure 1A calibrated rectangle rotates counterclockwise by 30°. Rotated unit directions explain the matrix columns; paired bars verify each vertex’s distance. Geometry axes have equal scale.

## Matrix columns show where the basic directions go

Every planar displacement can be assembled from two basic arrows: one unit to the right and one unit upward. The point (2, 1) combines two copies of the horizontal arrow with one copy of the vertical arrow. To rotate that combination, we can first rotate the two basic arrows and then combine their new directions using the original weights. The first column of a rotation matrix records the new horizontal unit direction, and the second column records the new vertical unit direction. Matrix multiplication weights those columns and adds their contributions.

$$
\theta=\frac{\pi\phi}{180},\qquad \begin{bmatrix}x^\prime\\y^\prime\end{bmatrix}=\underbrace{\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}}_{R}\begin{bmatrix}x\\y\end{bmatrix}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | Counterclockwise angle expressed numerically in degrees, such as 30 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Same angle in radians, a dimensionless angular unit |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/09ddc635f7b6cb67ae9fd772.svg) | Number of degrees in a half-turn, for degree-to-radian conversion |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 2×2 rotation matrix, with dimensionless entries |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Coordinates before rotation, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/2a3d1fd52a68a190a931ec53.svg) | Coordinates after rotation about the origin, mm; primes mark transformed values |
| ![Formula](https://ml-biomat.com/static/agent-math/5bc8e1a5d4bcca693b9f9dcf.svg) | Sine and cosine give unit-direction projections; their values are dimensionless |

The columns are the rotated horizontal and vertical unit directions. Weight them by the original x and y and add. For 30°, θ=π/6; (2,1) mm becomes (2×0.866025−0.5,2×0.5+0.866025) mm≈(1.232051,1.866025) mm.

At 30°, the horizontal unit arrow becomes approximately (0.866, 0.500), while the vertical unit arrow becomes approximately (-0.500, 0.866). Consequently, (2, 1) mm becomes approximately (1.232, 1.866) mm. Its new horizontal component is twice 0.866 minus 0.500; its new vertical component is twice 0.500 plus 0.866. Each multiplication and addition has a geometric meaning. NumPy's trigonometric functions take angles in radians. `np.deg2rad(30)` converts 30° to one sixth of pi radians; passing 30 directly to `np.sin` describes an entirely different angle.

Written mathematical formulas usually place one vector in a column. Our data table stores each point in a row, so the batch calculation is `points @ R.T`. Transposing `R` exchanges its rows and columns, making each data row receive the two component calculations in the formula. The shape rule is (4, 2) multiplied by (2, 2): the inner dimensions match, and the output shape is (4, 2). For a single one-dimensional array `[2., 1.]`, `R @ point` directly returns a one-dimensional array with two entries. A one-dimensional NumPy array does not itself have a fixed row or column orientation.

Python 3.5 introduced the dedicated `@` operator, following PEP 465, proposed in 2014. The design addressed a persistent difficulty in scientific programs: elementwise multiplication and matrix multiplication needed distinct notation. For NumPy arrays, `*` multiplies corresponding entries, while `@` sums products along the matching dimensions. A rotation needs the contributions from both original components to be added, which is the matrix-product operation. The program also checks that `R.T @ R` is close to the identity matrix: turning back should recover the starting coordinates. `np.allclose` accommodates the small rounding differences introduced by floating-point trigonometry.

This calculation keeps the axes fixed while actively rotating the shape. Keeping the shape fixed and rotating the axes counterclockwise instead produces the opposite coordinate transformation. Image row numbers also commonly increase downward, unlike the upward mathematical axis. Establish a consistent axis direction before interpreting the sign of an angle. Marking the origin, showing positive directions, and checking a 90° example separates these conventions before arbitrary rotations are attempted.

## A calibration line carries units

Return to the six ruler readings. An extra 2 mm corresponds to roughly 40 additional pixels, suggesting a model that multiplies length by a scale factor and adds a zero-position offset. The scale factor is the slope, measured in px/mm; the offset is the intercept, measured in px. These parameters have different jobs. The slope describes image magnification, while the intercept locates the ruler's zero mark in the image coordinate system. Translating the whole image changes the intercept without changing how many pixels span one millimetre.

$$
\widehat p_i=a s_i+b,\qquad r_i=p_i-\widehat p_i,\qquad s=\frac{p-b}{a},\qquad \Delta s=\frac{\Delta p}{a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Calibration record index, 1 through 6, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/98809785fc57c54ab2c96fe5.svg) | Known calibration position or recovered position, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e473ccb167494c193bb13372.svg) | Corresponding image reading, px |
| ![Formula](https://ml-biomat.com/static/agent-math/68e840913b12a81fc785459a.svg) | Fitted pixel reading, px; the hat marks a prediction |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Pixel scale, the line slope, px/mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Image coordinate of the ruler zero, px |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | Observed-minus-fitted residual, px |
| ![Formula](https://ml-biomat.com/static/agent-math/d865353994b14d656a35dc2f.svg) | Displacement between positions in px and mm respectively; Δ means a difference |

For a uniform linear calibration with a=20 px/mm and b=1 px, the prediction at 4 mm is 81 px; an observed 80 px gives a −1 px residual. Inverting 81 px gives (81−1)/20=4 mm. The common intercept cancels in a difference, so a 200 px displacement is 10 mm.

The first and last records give a slope of 20 px/mm and an intercept of 1 px. In this constructed example, their line happens to equal the least-squares solution using all six records. Other pairs give different answers: the readings at 0 and 2 mm produce a slope of 20.5 px/mm. Dependence on the selected pair motivates a common rule using every record. The fitted readings for all six positions are 1, 41, 81, 121, 161, and 201 px. Subtracting these from the observations gives 0, 1, -1, -1, 1, and 0 px.

These differences are residuals. A positive residual places an observation above the fitted line; a negative residual places it below. Residuals use the selected model's fitted values as their reference and can therefore be computed from the available records. They differ from measurement errors relative to an unknown true value. A separate residual plot is useful because its vertical range covers a few pixels rather than the hundreds shown in the calibration plot. Curvature in the residual pattern would motivate an examination of the linear relationship, lens distortion, or reading procedure. Such structure can be difficult to notice in an apparently straight calibration curve.

With a scale of 20 px/mm, a displacement of 200 px corresponds to 10 mm, and 80 px corresponds to 4 mm. These are differences relative to a chosen image point, so the common 1 px intercept has already cancelled. Recovering an absolute ruler position from an image reading requires subtracting the intercept before dividing by the slope: a reading of 81 px corresponds to 4 mm. Distinguishing position from displacement explains why the calibration model includes an intercept while the rectangle's side-length conversion uses only the slope.

![Dimensioned calibration line, six signed residuals, and design-matrix records.](https://ml-biomat.com/static/tutorials/python-scientific/figures/73d2c5d6522b2ce6f0d3e0e4.svg?v=73d2c5d6522b)

Figure 2Six constructed calibration records yield 20 px/mm and 1 px. The residual panel magnifies departures and matches the design-matrix rows; squared residuals sum to 4 px².

## Least squares grew out of imperfect observations

Early nineteenth-century astronomy and geodesy faced a recurring problem: many observations were available, but they could not all agree exactly with a small set of unknown parameters. In his 1805 work on comet orbits, Legendre discussed this mismatch and introduced least squares in an appendix, also applying the method to French meridian measurements. The central choice was to make the sum of squared residuals as small as possible. Microscope calibration concerns a different object, yet it retains the same structure: several observations jointly determine a smaller set of parameters.

$$
S(a,b)=\sum_{i=1}^{N}\left[p_i-(a s_i+b)\right]^2=\sum_{i=1}^{N}r_i^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Sum of squared residuals for the chosen coefficients, px² |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | Slope and intercept to fit, in px/mm and px |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of calibration records, here 6, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Record index from 1 to N, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/494b59eedd3f44cca8cf919a.svg) | Observed pixel reading in record i, px |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | Known ruler position in record i, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | Observed-minus-fitted residual in record i, px |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum all N terms |

With equal weights, the least-squares solution minimizes S. Residuals 0,1,−1,−1,1,0 px give S=0+1+1+1+1+0=4 px². Squaring measures departures without signed cancellation; ruler positions are treated as sufficiently accurate inputs.

Simply adding signed residuals allows cancellation. Our six residuals sum to 0 px even though four readings depart from the fitted line. Squaring makes each contribution nonnegative: both 1 px and -1 px contribute 1 px², giving a total of 4 px². Larger departures receive more emphasis, since a residual of 3 px contributes 9 px². A sum of absolute residuals is another possible objective and defines a different optimization problem. The name least squares identifies the particular measure of disagreement chosen here.

The contour plot below uses slope and intercept as its two coordinates. Every parameter pair defines a calibration line and therefore a residual sum of squares. Points on one contour have the same total squared departure; moving toward the centre reduces it. The elongated, tilted contours show that the two parameters can partly compensate for each other. A slightly larger slope combined with a smaller intercept may change predictions near the middle of the calibration range only a little. A wider range of known positions helps separate scale from offset.

Forcing the intercept to zero restricts the parameter search to the horizontal line where the intercept is zero. The resulting slope is approximately 20.136364 px/mm, and the squared residual sum is approximately 5.909091 px², compared with 4 px² for the free-intercept fit. The difference comes from the imposed constraint. Fixing a zero intercept is appropriate when the experimental definition independently establishes coincident zeros. Here, the six pixel readings receive equal weight and the ruler positions are treated as sufficiently accurate inputs. Unequal reading precision can be represented through weighted fitting; substantial uncertainty in the horizontal coordinates requires a model that accounts for both directions.

![Squared-residual contours over slope and intercept, with residuals for two model choices.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8b3ece9d72298ade6799d1ac.svg?v=8b3ece9d7229)

Figure 3This chapter’s data illustrate Legendre’s 1805 squared-error objective. Computed contours show how fixing a zero intercept restricts the parameter choice, increasing the sum from 4 to about 5.909 px².

## Arrange the six relationships for NumPy

A line has two unknown coefficients, slope and intercept, whereas our table contains six records. Place each known length beside a constant 1 to form a design matrix with shape (6, 2). Multiplying the first column by the slope and the second by the intercept, then adding within each row, produces the six predicted pixel readings. The constant column includes the same offset term in every record; it is not an additional measurement. The two columns also carry different units. Length is in millimetres, while the constant is dimensionless, and their respective coefficient products both have units of pixels.

`np.column_stack([LENGTH, np.ones_like(LENGTH)])` constructs this table. `np.linalg.lstsq(design, PIXEL, rcond=None)` returns the coefficients, a residual-sum array, the matrix rank, and singular values. The column order determines coefficient order. Because length precedes the constant here, the first coefficient is the slope and the second is the intercept. `design @ coefficients` then produces fitted readings, and `PIXEL - predicted` produces individual residuals. Naming these quantities separately makes it possible to connect each variable to an element in the plots.

Initially, think of rank as the number of independent kinds of information in the design matrix. Our lengths differ, so the length column cannot be produced by multiplying the constant column by one fixed number. The rank is two, allowing both coefficients to be identified. If every reading were taken at the same ruler position, repetitions could reveal variability at that position but could not distinguish slope from intercept. `lstsq` can still return a coefficient vector when information is insufficient; its rank output helps identify the need to revise the calibration design. Singular values describe numerical directions and scales. The program preserves them for inspection without interpreting them as two measurements having one shared physical unit.

The residual-sum return value follows a specific interface rule: it is empty when the matrix is rank deficient or when the number of records does not exceed the number of unknowns. An empty array means that this field is not reporting a sum; it does not establish that every residual is zero. The complete program therefore always computes `residual @ residual` directly. A separate scalar function uses centred sums to check the slope and intercept independently. Readers can first verify the two-point calculation and six residuals by hand, then examine that checking function while NumPy remains responsible for the main solution.

The centred sums in the checking function have a geometric interpretation. The mean ruler position is 5 mm and the mean pixel reading is 101 px. Subtracting those means shifts the numerical origin to the centre of the records. Products of centred lengths and centred readings sum to 1400 mm·px; squared centred lengths sum to 70 mm². Their ratio gives 20 px/mm. Subtracting the slope times the mean length from the mean reading then gives the 1 px intercept. This explains both the arithmetic and why the denominator vanishes if every calibration position is identical.

## The complete calibration and rotation

The program below contains all constructed input values at its beginning and can be run directly. It first estimates the calibration coefficients, divides four pixel displacements by the scale to obtain millimetre coordinates, and rotates them by 30°. It saves three scientific figures and a `summary.json` containing the calibration values, residuals, rotation matrix, vertex coordinates, and distances. NumPy handles the array calculations and Matplotlib draws the figures. Both packages belong in the same Python environment introduced in [P06](https://ml-biomat.com/tutorials/python-scientific/p06/en/).

### Run the complete example

Use zh for Chinese figures. Run in an environment containing NumPy and Matplotlib.

```
python main.py --output output --language en
```

### Complete calibration and coordinate transformation

LENGTH and PIXEL contain six constructed records; OUTLINE stores pixel displacements from an image origin. scalar_fit independently checks coefficients, rotation builds the transformation, and main saves results and figures.

```
"""Calibrate a constructed microscope scale and rotate planar coordinates."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon

LENGTH = np.array([0, 2, 4, 6, 8, 10], dtype=float)  # mm
PIXEL = np.array([1, 42, 80, 120, 162, 201], dtype=float)  # px
OUTLINE = np.array([[0, 0], [200, 0], [200, 80], [0, 80]], dtype=float)
BLUE, RED, GREEN = '#246989', '#b95235', '#42816b'


def rotation(degrees):
    theta = np.deg2rad(degrees)
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


def scalar_fit(x, y):
    """Independent centered-sum line fit, used as an arithmetic check."""
    xbar = math.fsum(map(float, x)) / len(x)
    ybar = math.fsum(map(float, y)) / len(y)
    numerator = math.fsum((float(u)-xbar)*(float(v)-ybar) for u, v in zip(x, y))
    denominator = math.fsum((float(u)-xbar)**2 for u in x)
    slope = numerator / denominator
    return slope, ybar - slope*xbar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('output'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    design = np.column_stack([LENGTH, np.ones_like(LENGTH)])
    coefficients, returned_sse, rank, singular = np.linalg.lstsq(design, PIXEL, rcond=None)
    slope, intercept = coefficients
    predicted = design @ coefficients
    residual = PIXEL - predicted
    sse = float(residual @ residual)
    R = rotation(30)
    physical = OUTLINE / slope  # displacement from a chosen image origin, in mm
    rotated = physical @ R.T
    radii = np.linalg.norm(physical, axis=1)
    rotated_radii = np.linalg.norm(rotated, axis=1)
    point90 = rotation(90) @ np.array([2., 1.])
    constrained_slope = float(LENGTH @ PIXEL / (LENGTH @ LENGTH))
    constrained_residual = PIXEL - constrained_slope * LENGTH
    assert np.allclose(coefficients, [20, 1])
    assert np.allclose(coefficients, scalar_fit(LENGTH, PIXEL))
    assert np.allclose(residual, [0, 1, -1, -1, 1, 0]) and np.isclose(sse, 4)
    assert np.allclose(point90, [-1, 2])
    assert np.allclose(R.T @ R, np.eye(2))
    assert np.allclose(radii, rotated_radii)
    assert np.allclose(rotated, [[u*math.cos(math.pi/6)-v*math.sin(math.pi/6),
                                 u*math.sin(math.pi/6)+v*math.cos(math.pi/6)] for u, v in physical])
    zh = args.language == 'zh'
    tr = lambda z, e: z if zh else e
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    family = [f for f in ['Noto Sans CJK SC', 'Noto Sans SC', 'Microsoft YaHei', 'DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family': family if zh else ['DejaVu Sans', 'Arial'],
                         'font.size': 12, 'axes.titlesize': 14, 'axes.titleweight': 'bold',
                         'axes.spines.top': False, 'axes.spines.right': False, 'svg.fonttype': 'none',
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6', 'text.color': '#172b36'})
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=170, bbox_inches='tight')
        plt.close(fig)

    fig = plt.figure(figsize=(12.4, 7.7), layout='constrained')
    gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 1])
    ax = fig.add_subplot(gs[:, 0])
    for points, color, label in [(physical, BLUE, tr('标定后','Calibrated')), (rotated, RED, tr('逆时针30°','30° counterclockwise'))]:
        ax.add_patch(Polygon(points, facecolor=color, edgecolor=color, alpha=.15, lw=2))
        closed = np.vstack([points, points[0]])
        ax.plot(closed[:, 0], closed[:, 1], 'o-', color=color, lw=2, label=label)
    for i, (x, y) in enumerate(rotated):
        ax.annotate(str(i), (x, y), xytext=(6, 7), textcoords='offset points', color=RED, weight='bold')
    ax.axhline(0, color='#83949a', lw=.8); ax.axvline(0, color='#83949a', lw=.8)
    ax.set(xlim=(-4, 12), ylim=(-3, 11), aspect='equal', xlabel='x / mm', ylabel='y / mm', title=tr('a  长度不变，坐标改变','a  Coordinates change; lengths do not'))
    ax.legend(loc='upper left', fontsize=11); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[0, 1])
    basis = rotation(30)
    for v, color, label in [(np.array([1, 0]), BLUE, '(1, 0)'), (np.array([0, 1]), BLUE, '(0, 1)'), (basis[:, 0], RED, '(0.866, 0.500)'), (basis[:, 1], GREEN, '(-0.500, 0.866)')]:
        ax.annotate('', xy=v, xytext=(0, 0), arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': 2})
        ax.text(v[0]*1.08, v[1]*1.08, label, color=color, fontsize=10, ha='center')
    ax.set(xlim=(-.8, 1.45), ylim=(-.2, 1.35), aspect='equal', title=tr('b  矩阵的两列：单位方向转到哪里','b  Matrix columns: rotated unit directions'))
    ax.set_xlabel(tr('无量纲方向分量','Dimensionless direction components')); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[1, 1])
    pos = np.arange(4)
    ax.bar(pos-.17, radii, .34, color=BLUE, label=tr('旋转前','Before'))
    ax.bar(pos+.17, rotated_radii, .34, color=RED, alpha=.75, label=tr('旋转后','After'))
    ax.set(xticks=pos, xlabel=tr('顶点编号','Vertex index'), ylabel=tr('到原点距离 / mm','Distance to origin / mm'), title=tr('c  按行计算向量长度','c  Vector norms computed row by row'))
    ax.legend(); ax.grid(axis='y', alpha=.15)
    save(fig, 'coordinate-rotation')

    fig = plt.figure(figsize=(12.4, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1], width_ratios=[1.5, 1])
    ax = fig.add_subplot(gs[0, 0])
    xx = np.linspace(0, 10, 101)
    ax.plot(xx, slope*xx+intercept, color=BLUE, lw=2, label='p = 20s + 1')
    ax.scatter(LENGTH, PIXEL, color=RED, s=65, zorder=3, label=tr('构造的标定记录','Constructed calibration records'))
    ax.set(xlabel=tr('已知长度 s / mm','Known length s / mm'), ylabel='p / px', title=tr('a  像素读数：六条记录确定比例与零点','a  Six records determine scale and offset'))
    ax.legend(); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[1, 0])
    ax.axhline(0, color='#83949a', lw=1)
    ax.vlines(LENGTH, 0, residual, color=BLUE, lw=3); ax.scatter(LENGTH, residual, color=BLUE, s=55)
    ax.set(xlabel=tr('已知长度 / mm','Known length / mm'), ylabel=tr('观测 − 拟合 / px','Observed − fitted / px'), ylim=(-1.7, 1.7), yticks=[-1,0,1], title=tr('b  残差放大后，1 px清楚可见','b  Residual view reveals 1 px differences'))
    ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[:, 1]); ax.axis('off')
    table = ax.table(cellText=[[f'{s:.0f}', '1', f'{p:.0f}', str(round(float(r)))] for s,p,r in zip(LENGTH,PIXEL,residual)],
                     colLabels=['s / mm', '1', 'p / px', 'r / px'], loc='center', cellLoc='center', bbox=[.02,.22,.96,.60])
    table.auto_set_font_size(False); table.set_fontsize(13)
    for (i,j), cell in table.get_celld().items():
        cell.set_edgecolor('#d3dcdb'); cell.set_facecolor('#e6efee' if i==0 else '#fbfaf6')
    ax.text(.02,.94,tr('c  设计矩阵的每一行都对应一条记录','c  One design-matrix row per record'),fontsize=14,weight='bold')
    ax.text(.02,.10,tr('a = 20 px/mm；b = 1 px\n残差平方和 = 4 px²；rank = 2','a = 20 px/mm; b = 1 px\nSquared residual sum = 4 px²; rank = 2'),fontsize=14,linespacing=1.7)
    save(fig, 'calibration-residuals')

    fig = plt.figure(figsize=(12.4, 7.5), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[.2, 1], width_ratios=[1.2, 1])
    ax = fig.add_subplot(gs[0, :]); ax.axis('off')
    ax.text(0,.75,tr('1805：把互不完全吻合的观测，变成一个共同的求解问题','1805: reconciling observations through one shared objective'),fontsize=18,weight='bold')
    ax.text(0,.05,tr('勒让德的最小二乘思想，用本章构造的显微标定记录展示。','Legendre’s least-squares principle, illustrated with this chapter’s constructed calibration records.'),fontsize=12)
    ax = fig.add_subplot(gs[1, 0])
    aa, bb = np.meshgrid(np.linspace(19,21,301), np.linspace(-4,6,301))
    costs = np.sum((PIXEL[:,None,None] - aa[None]*LENGTH[:,None,None]-bb[None])**2, axis=0)
    contours = ax.contour(aa, bb, costs, levels=[5,10,20,40,80,160,320], cmap='viridis', linewidths=1.5)
    ax.clabel(contours, inline=True, fontsize=10, fmt='%g')
    ax.axhline(0, color=RED, linestyle=':', linewidth=1.2, alpha=.6)
    ax.scatter([slope,constrained_slope],[intercept,0],color=[BLUE,RED],s=[80,65],zorder=4)
    ax.annotate(tr('自由零点：(20, 1)','Free offset: (20, 1)'),(20,1),xytext=(19.05,4.5),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE)
    ax.annotate(tr('强制 b = 0','Force b = 0'),(constrained_slope,0),xytext=(20.25,-3),arrowprops={'arrowstyle':'->','color':RED},color=RED)
    ax.set(xlabel=tr('斜率 a / (px/mm)','Slope a / (px/mm)'), ylabel=tr('截距 b / px','Intercept b / px'), title=tr('a  等高线数字：残差平方和 / px²','a  Contour labels: squared residual sum / px²'))
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(LENGTH,residual,'o-',color=BLUE,label=tr('自由零点','Free offset'))
    ax.plot(LENGTH,constrained_residual,'s--',color=RED,label=tr('强制零点','Forced zero'))
    ax.axhline(0,color='#83949a',lw=1)
    ax.set(xlabel=tr('已知长度 / mm','Known length / mm'),ylabel=tr('残差 / px','Residual / px'),ylim=(-1.8,1.8),title=tr('b  改变模型，残差也随之改变','b  Changing the model changes the residuals'))
    ax.legend();ax.grid(alpha=.15)
    save(fig,'least-squares-history')
    summary = {'dataset':'Constructed microscope calibration', 'length_mm':LENGTH.tolist(),'pixel_px':PIXEL.tolist(),
               'slope_px_per_mm':float(slope),'intercept_px':float(intercept),'residual_px':residual.tolist(),'sse_px2':sse,
               'rank':int(rank),'singular_values':singular.tolist(),'returned_sse_px2':returned_sse.tolist(),
               'rotation_30':R.tolist(),'physical_vertices_mm':physical.tolist(),'rotated_vertices_mm':rotated.tolist(),
               'radii_before_mm':radii.tolist(),'radii_after_mm':rotated_radii.tolist(),'point_90_mm':point90.tolist(),
               'constrained_slope_px_per_mm':constrained_slope,'constrained_sse_px2':float(constrained_residual@constrained_residual)}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
```

The fitted slope is approximately 20.000000 px/mm and the intercept approximately 1.000000 px. Rotated vertices are approximately (0, 0), (8.660254, 5.000000), (6.660254, 8.464102), and (-2.000000, 3.464102) mm. The second vertex starts at (10, 0) mm, so its new components are 10 times the cosine and sine of 30°. The third vertex also includes the original 4 mm vertical edge, reducing its horizontal coordinate by 2 mm and increasing its vertical coordinate by approximately 3.464102 mm. Checking individual points exposes a misplaced transpose or reversed angle more clearly than viewing the outline alone.

The program checks three complementary properties: each vertex's distance is preserved, the rotation followed by its inverse gives the identity transformation, and scalar trigonometric calculations reproduce the complete coordinate array. The geometry panel uses equal horizontal and vertical scales, preserving the appearance of lengths and angles. Stretching one display direction would distort the rectangle visually even if the coordinate values were correct. The residual plot deliberately magnifies vertical differences because it compares two quantities rather than representing a planar physical shape.

Try replacing the rotation angle with 90° and check that the rectangle moves into the region above and to the left of the origin. Next, examine what happens when length units change. Expressing the same ruler positions in centimetres divides their numerical values by ten and multiplies the slope, now in px/cm, by ten. The physical rectangle retains its size when units and values are changed together. Changing numbers without changing their stated meaning instead describes a different calibration experiment.

The solver may print 19.99999999999999 rather than exactly 20 because its arithmetic uses finite precision. Figure annotations round values for reading, while the numerical file preserves the computed results for subsequent calculations. A long decimal tail is not additional measurement precision. Our input readings are integer pixels; extra displayed digits mainly help compare intermediate calculations. Relate meaningful differences back to the resolution and uncertainty of the calibration records.

## Follow one altered reading through the calculation

The interactive experiment uses the same six records. Select one record and adjust its pixel reading: the fitted line, six residuals, squared residual sum, and rectangle dimensions update together. The rectangle still spans 200 by 80 px, so its size in physical coordinates depends on the current fitted slope. Rotation changes its orientation. Showing both the unrotated and rotated outlines makes changes of scale and direction easier to separate. The intercept can be fitted freely or constrained to zero to compare the two models.

### How calibration changes the image scale

Adjust one ruler reading or rotate the rectangle. Geometry uses millimetres; the pixel outline stays fixed at 200 by 80 px.

[Figure: Calibration, residuals, and linked rotating rectangle](https://ml-biomat.com/tutorials/python-scientific/p10/en/#P10-chart)

Blue: fit under the current model. Orange: altered record and rotated outline. Grey: unrotated outline. Residuals are observed minus fitted.

Keep the angle at 30° and add 10 px to the reading at 10 mm. Because this position lies far from the mean length, the change noticeably affects the fitted slope and reduces the converted rectangle width. Restore the reading, then alter the record at 0 mm and observe how slope and intercept adjust together. Changing one record at a time keeps the cause traceable. Finally, switch between 0° and 90°: with the calibration unchanged, dimensions and residuals stay fixed while the vertex coordinates turn.

Image measurements return repeatedly to the same practical choices: the coordinate origin, axis directions, calibration range, independently established zero positions, and validity of a common pixel scale. NumPy applies these choices consistently to complete coordinate collections, while matrices express the rules compactly. Understanding each column and each weighted sum makes it possible to extend the workflow to longer outlines, multiple images, and repeated calibrations. The next chapter moves to real records containing names, categories, and missing values, where preserving the meaning of each observation remains just as important.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P10.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NumPy: numpy.linalg.lstsq](https://numpy.org/doc/2.4/reference/generated/numpy.linalg.lstsq.html)

   Design matrices, rank, and return-value rules

   BSD-3-Clause documentation; original example here
2. [NumPy: numpy.matmul](https://numpy.org/doc/2.4/reference/generated/numpy.matmul.html)

   Matrix products and compatible shapes

   BSD-3-Clause documentation
3. [NumPy: numpy.linalg.norm](https://numpy.org/doc/2.4/reference/generated/numpy.linalg.norm.html)

   Vector norms along a specified axis

   BSD-3-Clause documentation
4. [PEP 465: matrix multiplication operator](https://peps.python.org/pep-0465/)

   Design history of the @ operator

   Public domain PEP; factual reference
5. [Legendre, Nouvelles méthodes, 1805](https://doi.org/10.3931/e-rara-35115)

   Original observational problem and historical context of least squares

   Public Domain Mark, ETH Library; no scans reproduced
