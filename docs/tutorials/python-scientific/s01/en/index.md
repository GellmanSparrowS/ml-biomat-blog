# Measuring Structure in Microscopy Images

Source: https://ml-biomat.com/tutorials/python-scientific/s01/en/
Language: en

Turn a real cell phase image into an area measurement with physical units, an explicit boundary, and inspectable parameter effects.

## How does a microscopic size become a comparable number?

When examining cells in a hydrogel, pores in a polymer film, or grains in a metal, it is easy to say that one object looks larger or has a rougher boundary. Comparing treatment conditions requires measurements. Image analysis connects observation to measurement by defining an object, locating it in the image, and converting pixels into physical lengths or areas through calibration. This chapter follows a real quantitative-phase image of a cell. We use scikit-image to select its largest bright connected region, calculate projected area and equivalent-circle diameter, and inspect how those values change with the boundary rule. Figures, code, and interaction use the same original image so that each step can be checked against the input.

The public image is provided as `skimage.data.cell`. It shows a cell in saline, with a spatial sampling interval of 0.107 μm per pixel. The array contains 660 rows and 550 columns, with the cell on the right. Under the workflow defined here, the Otsu threshold is 122. Selecting the largest bright component and filling its internal holes gives 11746 pixels, a projected area of approximately 134.48 μm², and an equivalent-circle diameter of approximately 13.09 μm. These rounded values are convenient for reading; the program saves full values and processing conditions. Seeing the destination first makes the subsequent array operations and unit conversions easier to follow.

The measurement object needs a precise description. We measure the two-dimensional region selected by a grayscale rule and express its area as the diameter of an equal-area circle. Cell volume, the detailed shape of a membrane surface, and molecular concentrations require additional observations or models. A leaf provides a useful analogy: its outline on a table can define a projected area, while a curled leaf has a different total surface area. Once the object is defined, thresholding, hole filling, and calibration become choices with understandable consequences.

![Original cell phase image, boundary detail, and horizontal intensity profile. Spatial coordinates use 0.107 μm per pixel; yellow contours mark the largest region at threshold 122.](https://ml-biomat.com/static/tutorials/python-scientific/figures/6d1063ee6fcbe28777e99675.svg?v=6d1063ee6fcb)

Figure 1Original cell phase image, boundary detail, and horizontal intensity profile. Spatial coordinates use 0.107 μm per pixel; yellow contours mark the largest region at threshold 122.

## Read the image as a table of values with positions

A digital grayscale image resembles a map covered by small squares. Each square is a pixel, and its stored number determines its displayed brightness. After `io.imread`, our image is a two-dimensional NumPy array whose `shape` is `(660, 550)`: rows first, columns second. The expression `image[370, 400]` locates row 370 vertically and column 400 horizontally, with indexing beginning at zero. Plotting usually assigns columns to the horizontal coordinate and rows to the vertical coordinate. This change of order matters when drawing contours returned as row-column pairs.

The array has the type `uint8`, an unsigned eight-bit integer with possible values from 0 to 255. We use the stored grayscale range directly, so threshold 122 belongs to that same range. Converting an image to floating point and rescaling its values to the interval from zero to one are different operations. A type conversion may simply turn 122 into 122.0, whereas rescaling changes the numerical threshold scale. Checking shape, type, minimum, and maximum before choosing parameters connects the processing code to the actual data representation.

This image originates from quantitative-phase imaging, which measures information about the phase changes of light passing through a sample. The grayscale values in the provided image encode that information. Here we read an eight-bit public image, rather than treating its values as raw phase measurements in radians or directly converting them into a molecular concentration. Our task uses the grayscale difference between the cell region and background. The horizontal profile plots the successive pixels in row 370, connecting visible background, a dark edge, and the bright interior to a sequence of numbers at known positions.

Image coordinates should also agree with the sampling convention. The example places the outer pixel boundaries from zero onwards, so pixel centers lie halfway across their squares. Profiles and contour coordinates consequently include a half-pixel offset when expressed in physical units. The vertical coordinate increases downward, as image row numbers do. This convention aligns the original image, enlarged boundary view, and profile. When adopting another microscope's exported images, check calibration, axis direction, and any resizing before using the same representation.

## From drawing a boundary to Otsu's threshold

A simple way to separate a bright region from its background is to choose a threshold. Pixels strictly brighter than that threshold become true; the others become false. The expression `image > threshold` compares the complete array and returns a Boolean array of the same shape. This true-false map is a mask: it records which pixels the present rule includes in the object. Lowering the threshold admits more pixels, while raising it progressively removes edge pixels and darker interior regions. Threshold segmentation is useful when object and background can be distinguished by intensity; choosing the threshold requires inspecting the intensity distribution.

A histogram groups pixels by intensity. Its horizontal axis is the grayscale value, and its vertical axis counts pixels in each group. Spatial positions disappear, while the distribution of dark and bright values remains. The present image has many darker background pixels and fewer bright cell pixels. Because their counts differ substantially, the histogram uses a logarithmic count axis to show both distributions clearly. The calculation still uses the original counts. A logarithmic display changes how a graph is viewed, whereas transforming image values would change the input to the algorithm.

In 1979, Nobuyuki Otsu published a method for choosing an intensity threshold from a histogram. The method turns a visual choice into a repeatable calculation: try candidate thresholds, divide pixels into dark and bright classes, calculate each class's fraction and mean intensity, and assess their separation. The figure below plots that assessment for the original image used throughout this chapter. Writing the selection rule as a mathematical objective makes the threshold reproducible for the same input.

$$
B(T)=w_0(T)w_1(T)\big[\mu_0(T)-\mu_1(T)\big]^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | candidate threshold in the image intensity scale, 0–255 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2227ed627c5314ec2dc3cc.svg) | between-class variance at T, squared intensity units |
| ![Formula](https://ml-biomat.com/static/agent-math/abf19469b88ec6828af62099.svg) | fractions of all pixels in the dark (≤T) and bright (>T) classes, dimensionless, summing to one |
| ![Formula](https://ml-biomat.com/static/agent-math/f937e16c6768b39074edb1b7.svg) | mean intensity within each class, intensity units |

Subtract the class means and square the difference to obtain a nonnegative separation measure. Multiplying by both class fractions accounts for the pixels assigned to each class. Otsu selects the candidate with the largest B; empty classes are excluded. In a teaching calculation, fractions 0.9 and 0.1 with mean intensities 60 and 180 give B=0.9×0.1×(60−180)²=1296 intensity². These illustrative values explain the formula; the plotted curve is calculated from the real image histogram.

![The real image illustrates Otsu’s 1979 selection rule through the histogram, between-class variance, and class fractions. Counts are displayed logarithmically, while the algorithm uses original counts.](https://ml-biomat.com/static/tutorials/python-scientific/figures/926ef48af6e8e7785d55a2c0.svg?v=926ef48af6e8)

Figure 2The real image illustrates Otsu’s 1979 selection rule through the histogram, between-class variance, and class fractions. Counts are displayed logarithmically, while the algorithm uses original counts.

The objective reaches its maximum at threshold 122, matching `filters.threshold_otsu(image)`. The example also calculates the complete objective curve independently from cumulative histogram counts and intensity sums, checking the library result against the formula. Greater separation of class means increases the score; the product of class fractions reduces the score for a split that isolates a tiny number of exceptionally bright pixels. The objective describes grayscale statistics rather than biological identity. Overlaying the resulting boundary on the image connects that statistical choice to the object we intend to measure.

## Decide which pixels belong together and how to treat holes

A threshold mask can contain a cell, small bright spots, and isolated noise. Measuring one object requires a definition of connectivity. Four-connectivity joins pixels through their top, bottom, left, and right neighbors; eight-connectivity also permits diagonal contact. In a two-dimensional image, `measure.label(..., connectivity=2)` selects eight-connectivity and assigns each connected region an integer label. Zero denotes the background. `np.bincount` counts occurrences of each label, and the program selects the largest non-background region. This choice matches the present image and its single dominant bright cell. An image containing many cells calls for retaining multiple labels and constructing an object-by-object table.

Hole filling makes another substantive choice. A selected region can contain internal islands whose intensity is below the threshold. Keeping these islands empty measures the selected threshold area. Filling islands enclosed by the outer boundary measures the area enclosed by that boundary. The example uses `ndimage.binary_fill_holes` for the latter definition. It fills internal background regions disconnected from the outside, rather than smoothing every indentation. At threshold 122, retaining or filling holes gives the same pixel count. At threshold 140, filling adds eight pixels. The interactive switch connects this processing definition to a visible boundary and an area value.

Operation order belongs to the measurement definition too. The program thresholds the image, labels connected components, selects the largest component, and optionally fills its holes. Smoothing extensively beforehand or connecting separated components first could change the result because the Boolean map entering the labeling operation would be different. A short, explicit sequence helps a beginner see each step's contribution. Uneven illumination or touching objects can later motivate background correction, local thresholds, or watershed segmentation, with each addition tied to a particular image problem.

## Convert pixel counts into area and equivalent diameter

Once a mask exists, area calculation resembles counting floor tiles. Each image pixel corresponds to a small square in the sample plane, with a side length determined by spatial calibration. Count selected squares and multiply by one square's area. The value 0.107 μm is a pixel's side length in the specimen, rather than its area. Multiplying length by length produces μm² and explains why the scale factor must be squared. Multiplying a pixel count by the scale only once gives both the wrong units and the wrong value, even though a program can execute the operation without an error.

$$
A=N s^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | area of the selected projected region, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | number of true pixels in the mask, dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | physical side length of one square pixel, μm per pixel |

Each square pixel has area s², and summing N selected squares gives A. Squaring means multiplying a value by itself. With s=0.107 μm and N=11746, A=11746×0.107×0.107=134.479954 μm². Equal spacing in both directions is assumed; unequal spacings are multiplied separately.

The selected region is not perfectly circular, but we can ask for the diameter of a circle with the same area. That question defines equivalent-circle diameter. It expresses area as a familiar length while preserving a precise equal-area meaning. A narrow elongated object and a circular object can have the same equivalent diameter, so a study of shape would add measures such as major and minor axes, perimeter, or orientation. Establishing area and equivalent diameter first gives those later properties a clear place in an object measurement table.

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | diameter of an equal-area circle, μm; eq denotes equivalent |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | selected region area, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | circle constant, approximately 3.14159, dimensionless |

Circle area is π times radius squared. Divide area by π, take the nonnegative square root to obtain radius, then multiply by two. For A=134.479954 μm², A/π≈42.8063 μm², radius≈6.54265 μm, and diameter≈13.0853 μm. The quantity describes an area scale without requiring a circular object.

Calibration errors affect these values systematically. Increasing the recorded pixel side length by about one percent increases the area by about two percent and the equivalent diameter by about one percent. Collecting more images does not automatically remove a shared scale error, which is why calibration belongs with the input data. The program additionally creates an analytic disk of radius 8 μm as a teaching check. Sampling it at the same pixel spacing gives an area of about 200.976 μm², compared with the geometric value of about 201.062 μm², a relative difference of approximately −0.043%. This generated calibration object is identified separately from the real cell image. It checks units and discrete sampling rather than contributing another biological observation.

## The complete Python program and inspectable outputs

The program starts from the original image included with the example and requires no network connection for its default run. Reading, Otsu thresholding, connected-region selection, unit conversion, threshold scanning, and plotting are all visible in one file. `region_mask` returns the selected Boolean region, `metrics` turns a region into a count and physical quantities, and `otsu_curve` transforms the histogram into an inspectable objective curve. Passing images, masks, and measurements separately helps identify whether a change arises in image processing or unit conversion.

### Calculate image regions, sensitivity curves, and an analytic disk check

Read the bundled original image and produce a measurement summary, threshold table, and three scientific figures. Numerical measurements use the full grid; simplified contours support interactive display.

```
"""Measure the largest bright region in a public quantitative-phase cell image.

Data: skimage.data.cell, CC0, Mueller et al. (2018),
https://doi.org/10.1364/OE.26.010729 . Pixel spacing: 0.107 micrometres.
The calibrated disk is an analytic teaching object, separate from the image.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import math

import numpy as np
from scipy import ndimage
from skimage import io, filters, measure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
SPACING = 0.107
THRESHOLDS = np.arange(80, 201, 2)



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def region_mask(image, threshold, fill):
    """Select the largest 8-connected region strictly brighter than threshold."""
    labels = measure.label(image > threshold, connectivity=2)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    mask = labels == int(sizes.argmax()) if sizes.max() else np.zeros_like(image, bool)
    return ndimage.binary_fill_holes(mask) if fill else mask


def metrics(mask):
    pixels = int(np.count_nonzero(mask))
    area = pixels * SPACING ** 2
    return {"pixels": pixels, "area_um2": area,
            "equivalent_diameter_um": 2 * math.sqrt(area / math.pi)}


def otsu_curve(image):
    """Between-class variance for every integer uint8 threshold."""
    counts = np.bincount(image.ravel(), minlength=256)
    p = counts / counts.sum()
    weights = np.cumsum(p)
    first_moment = np.cumsum(p * np.arange(256))
    total_mean = first_moment[-1]
    score = np.zeros(256)
    valid = (weights > 0) & (weights < 1)
    score[valid] = (total_mean * weights[valid] - first_moment[valid]) ** 2 / (
        weights[valid] * (1 - weights[valid]))
    return counts, weights, score


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    out = args.output; out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    text = lambda a, b: a if zh else b
    path = HERE / "data/cell.png"
    image = io.imread(path)
    assert image.shape == (660, 550) and image.dtype == np.uint8
    threshold = int(filters.threshold_otsu(image))
    mask = region_mask(image, threshold, True)
    base = metrics(mask)
    counts, weights, score = otsu_curve(image)
    assert int(score.argmax()) == threshold
    states = []
    for t in THRESHOLDS:
        for fill in (False, True):
            current = region_mask(image, int(t), fill)
            contours = measure.find_contours(current.astype(float), .5)
            # Simplification affects display geometry, never the measured area.
            outlines = [np.round(measure.approximate_polygon(c, tolerance=1.0)[:, ::-1], 1).tolist()
                        for c in contours if len(c) > 8]
            states.append({"threshold": int(t), "fill": fill, **metrics(current), "contours": outlines})
    # An independent analytic area check at known spatial sampling.
    yy, xx = np.mgrid[-15:15:SPACING, -15:15:SPACING]
    radius = 8.0
    disk = xx ** 2 + yy ** 2 <= radius ** 2
    disk_area = float(disk.sum() * SPACING ** 2)
    analytic_area = math.pi * radius ** 2
    assert abs(disk_area / analytic_area - 1) < .01
    summary = {"dataset": "skimage.data.cell", "data_license": "CC0", "shape": list(image.shape),
               "spacing_um": SPACING, "threshold_otsu": threshold, "fill_holes": True,
               "connectivity": 8, "comparison": "image > threshold", **base,
               "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "disk_check": {"radius_um": radius, "pixel_area_um2": disk_area,
                              "analytic_area_um2": analytic_area,
                              "relative_error": disk_area / analytic_area - 1}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "lab-data.json").write_text(json.dumps({"width": 550, "height": 660, "spacing": SPACING,
        "otsu": threshold, "states": states, "histogram": counts.tolist(),
        "image": "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()}, separators=(",", ":")), encoding="utf-8")
    np.savetxt(out / "threshold-sensitivity.csv", np.array([[s['threshold'],int(s['fill']),s['pixels'],s['area_um2'],s['equivalent_diameter_um']] for s in states]), delimiter=",", header="threshold,fill_holes,pixels,area_um2,equivalent_diameter_um", comments="")
    plt.rcParams.update({"font.family": available_plot_fonts(), "font.size": 12,
                         "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none",
                         "axes.labelcolor": "#172534", "text.color": "#172534", "axes.edgecolor": "#81939d",
                         "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    blue, orange = "#205b8c", "#ba5231"
    def save(fig, name):
        fig.savefig(out / f"{name}-{args.language}.svg", metadata={"Date": None})
        fig.savefig(out / f"{name}-{args.language}.png", dpi=150)
        plt.close(fig)
    # Spatial views share physical coordinates, including the zoomed boundary.
    fig = plt.figure(figsize=(12.4, 7.2), layout="constrained")
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, .7])
    ax = fig.add_subplot(gs[:, 0]); zoom = fig.add_subplot(gs[0, 1]); profile = fig.add_subplot(gs[1, 1])
    for a in (ax, zoom):
        a.imshow(image, cmap="gray", vmin=0, vmax=255, extent=(0, 550*SPACING,660*SPACING,0))
        for c in measure.find_contours(mask.astype(float), .5):
            a.plot((c[:,1]+.5)*SPACING,(c[:,0]+.5)*SPACING,color="#ffcb66",lw=1.5)
        a.set(xlabel=text("水平位置 / μm", "Horizontal position / μm"),ylabel=text("垂直位置 / μm", "Vertical position / μm"))
    ax.set_title(text("A  原始相位图与测量边界", "A  Phase image and measured boundary"),loc="left")
    zoom.set(xlim=(34,55),ylim=(49,29));zoom.set_title(text("B  边界附近的真实灰度", "B  Original intensities near the boundary"),loc="left")
    row=370; ax.axhline((row+.5)*SPACING,color="#74d9db",ls="--",lw=1)
    profile.plot((np.arange(550)+.5)*SPACING,image[row],color=blue,lw=1.3)
    profile.axhline(threshold,color=orange,ls="--",label=f"T = {threshold}")
    profile.set(xlabel=text("水平位置 / μm", "Horizontal position / μm"),ylabel=text("灰度值", "Intensity"),ylim=(0,270))
    profile.set_title(text("C  水平剖面（第 370 行）", "C  Horizontal profile (row 370)"),loc="left");profile.legend(frameon=False)
    save(fig,"measured-cell")
    fig, axs=plt.subplots(1,2,figsize=(12.4,4.8),layout="constrained")
    for fill,color,ls in [(False,blue,"-"),(True,orange,"--")]:
        ss=[s for s in states if s['fill']==fill]
        for a,key in zip(axs,['area_um2','equivalent_diameter_um']):
            a.plot([s['threshold'] for s in ss],[s[key] for s in ss],color=color,ls=ls,lw=2,label=text("填充孔洞" if fill else "保留孔洞","Holes filled" if fill else "Holes retained"))
    for a,key in zip(axs,['area_um2','equivalent_diameter_um']):
        a.axvline(threshold,color="#7a8a94",ls=":");a.scatter([threshold],[base[key]],color=orange,zorder=3)
        a.set_xlabel(text("灰度阈值 T", "Intensity threshold T"));a.grid(axis='y',alpha=.18)
    axs[0].set_ylabel(text("投影区域面积 / μm²", "Projected region area / μm²"));axs[1].set_ylabel(text("等效圆直径 / μm", "Equivalent-circle diameter / μm"))
    axs[0].set_title(text("A  边界选择改变测量面积", "A  Boundary choice changes measured area"),loc="left")
    axs[1].set_title(text("B  相同面积换算成直径", "B  The same area expressed as a diameter"),loc="left");axs[0].legend(frameon=False)
    save(fig,"threshold-sensitivity")
    fig=plt.figure(figsize=(12.4,6.2),layout="constrained");gs=fig.add_gridspec(2,2,width_ratios=[1.25,1])
    hist=fig.add_subplot(gs[:,0]);criterion=fig.add_subplot(gs[0,1]);weight=fig.add_subplot(gs[1,1])
    hist.bar(np.arange(256),counts,width=1,color=np.where(np.arange(256)>threshold,orange,blue),rasterized=True)
    hist.axvline(threshold,color="#172534",ls="--");hist.set_yscale('log')
    hist.set(xlabel=text("灰度值", "Intensity"),ylabel=text("像素数（对数坐标）", "Pixel count (log scale)"),xlim=(0,255),ylim=(1,counts.max()*2))
    hist.set_title(text("A  按灰度把像素分成两类", "A  Split pixels into two intensity classes"),loc="left")
    criterion.plot(np.arange(256),score,color=blue);criterion.axvline(threshold,color=orange,ls="--")
    criterion.set(xlabel=text("候选阈值", "Candidate threshold"),ylabel=text("类间方差 / 灰度²", "Between-class variance / intensity²"));criterion.set_title(text("B  Otsu（1979）：比较所有分割", "B  Otsu (1979): compare all splits"),loc="left")
    weight.plot(np.arange(256),weights,color=blue,label=text("暗侧比例", "Dark-class fraction"));weight.plot(np.arange(256),1-weights,color=orange,label=text("亮侧比例", "Bright-class fraction"))
    weight.set(xlabel=text("候选阈值", "Candidate threshold"),ylabel=text("像素比例", "Pixel fraction"),ylim=(0,1));weight.legend(frameon=False,fontsize=10)
    save(fig,"otsu-separation")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
```

The output `summary.json` records image shape, pixel spacing, threshold, connectivity, hole-filling state, and the final measurement. `threshold-sensitivity.csv` records both hole treatments for thresholds from 80 to 200 in increments of two. The three principal figures answer where the boundary lies, how sensitive the result is to the threshold, and why Otsu chooses its threshold. To check the outputs, begin with the pixel count, calculate the area by hand, and then convert the area to a diameter. Each step corresponds to a particular function, making discrepancies easier to locate.

Contours exported for interaction are simplified as polylines using an approximately one-pixel tolerance, reducing the number of coordinates that the page needs to display. Area and diameter always come from the complete 660-by-550 mask. They are calculated from neither a thumbnail nor the geometry of a simplified outline. This separates a representation prepared for display from the grid used for measurement. Scientific visualization often needs this distinction: display geometry can be simplified while the calculation retains its stated resolution and definition.

## Plot parameter effects to assess a measurement

A single boundary and area provide little information about sensitivity to processing choices. A threshold scan makes that relationship visible: hold the image fixed, vary the threshold, and repeat the full selection and measurement procedure. With holes filled, threshold 100 gives approximately 140.96 μm²; threshold 122 gives 134.48 μm²; and threshold 160 gives 100.20 μm². The higher setting excludes part of the darker interior, so the change in area should be read alongside the change in contour. Every point follows the same operations, giving the comparison a consistent definition.

![Threshold sensitivity for the same original image, with holes retained or filled. Area and equivalent diameter have physical units; the vertical line marks the Otsu threshold of 122.](https://ml-biomat.com/static/tutorials/python-scientific/figures/6e9cb9eb41961e9af581f409.svg?v=6e9cb9eb4196)

Figure 3Threshold sensitivity for the same original image, with holes retained or filled. Area and equivalent diameter have physical units; the vertical line marks the Otsu threshold of 122.

Changing the threshold in the interactive workspace updates the image contour, histogram divider, position on the area-sensitivity curve, and numerical measurements together. The hole switch changes treatment of enclosed background at the same threshold. The page displays 122 states calculated in advance by the example Python program at full image resolution, allowing complete offline use. Threshold, hole treatment, pixel count, and physical quantities remain visible together, so that the current area can be reproduced from its recorded threshold and hole treatment.

### Boundary and measurement workbench

Change the threshold and hole treatment to inspect the boundary, intensity distribution, and measured area together.

[Figure: Original image, physical coordinates, and selected region boundary](https://ml-biomat.com/tutorials/python-scientific/s01/en/#S01-image)

[Figure: Intensity histogram and current threshold](https://ml-biomat.com/tutorials/python-scientific/s01/en/#S01-hist)

[Figure: Area sensitivity curve and current state](https://ml-biomat.com/tutorials/python-scientific/s01/en/#S01-curve)

Inspect three connected questions. Does the outline still refer to the same main object? Does a small threshold change produce a gradual area change? What image feature corresponds to a rapidly changing part of the curve? Here, sensitivity describes processing choices for one image. It has a different meaning from variation among cells or repeated experiments. Comparing treatment groups requires the same predefined workflow for each image and an explicit distinction between cells, fields of view, and independent experimental batches, so that pixels in one view are not counted as independent biological samples.

## Extend one-region measurement to your own images

Begin with a measurable description of the object, such as the projected area of each separated pore or the major-axis length of each nucleus. Check image dimensions and calibration next. A color image adds a channel dimension, a volumetric stack adds a slice dimension, and slice spacing can differ from in-plane spacing. Applying a two-dimensional procedure directly to a color array or treating unequal voxel dimensions as equal cubes changes the measurement's meaning. Once the input structure is understood, overlay masks and boundaries on representative original images and establish selection rules that match the research object.

For multiple objects, `measure.regionprops_table` can assemble area, centroid, and shape properties for each label. Retain object identifiers, image identifiers, and experimental conditions so that a table row can be located in the original image. Objects touching the image edge may be partially captured and need a consistent rule appropriate to the question. Small regions, touching objects, and uneven background should likewise be handled through inspectable examples. Apply the resulting rules across the image collection, then visualize the distribution of measurements to prepare meaningful group comparisons.

The workflow transfers to many materials problems: an image array supplies positions and signals, a segmentation rule defines objects, calibration turns a grid into physical quantities, and a parameter scan reveals how processing choices affect those quantities. scikit-image provides general operations, while the scientific question determines their connection. The useful result includes the original image, boundary, measurement definition, and executable program alongside the area value. Together, they turn a visual observation into quantitative evidence that can support further investigation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [scikit-image tutorials: Images are arrays](https://scikit-image.org/skimage-tutorials/lectures/00_images_are_arrays.html)

   Open tutorial foundation for arrays, image types, indexing, and value ranges.

   Tutorial materials CC0, per repository README.
2. [scikit-image tutorials: Image segmentation](https://scikit-image.org/skimage-tutorials/lectures/4_segmentation.html)

   Histogram, threshold, and region workflow; this chapter adds calibration, unit derivations, and parameter sensitivity.

   Tutorial materials CC0, per repository README.
3. [scikit-image: cell image](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)

   Real image, 0.107 μm pixel spacing, and original research identity.

   Image: CC0, as documented by scikit-image.
4. [Mueller et al. (2018), Optics Express 26, 10729](https://doi.org/10.1364/OE.26.010729)

   Original scientific study associated with the public cell phase image.

   Scientific citation; supplied image separately released under CC0.
5. [Otsu (1979), A Threshold Selection Method from Gray-Level Histograms](https://doi.org/10.1109/TSMC.1979.4310076)

   Original between-class-variance threshold method.
6. [scikit-image: Measure region properties](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html)

   Official example for extending to object properties and tables.
