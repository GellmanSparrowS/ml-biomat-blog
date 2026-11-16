# Putting Repeated Measurements into an Array

Source: https://ml-biomat.com/tutorials/python-scientific/p07/en/
Language: en

Start with three specimens observed at five times, and see how shape, indexing, and axes give a calculation its meaning.

## Three specimens, five times: deciding what the numbers mean

Imagine placing a water-absorbing film in water and measuring its thickness at several times. One specimen gives a time curve. With three specimens, more useful questions become possible: do they change at similar rates, what is a typical thickness at a given time, and how different are the specimens? These questions use the same observations, but combine them in different ways. This chapter starts with a small table and develops the NumPy representation needed to answer each question while preserving the meaning of the measurements.

We use explicitly constructed teaching data for specimens A, B, and C, observed at 0, 10, 20, 40, and 60 min. Thickness is recorded in mm. The decimal values are chosen so that several calculations can be checked by hand. They describe a teaching scenario of gradually increasing thickness, rather than measurements of a particular real material. Initial thickness and subsequent change differ slightly among specimens. A useful analysis retains those differences while also describing their common trend; reducing the whole table to one number too early would remove much of the information we want to examine.

Give every value an address before calculating with it. The first row belongs to A, the second to B, and the third to C. Columns identify the observation times. The value 1.16 mm is specimen B at 20 min: it has both a specimen identity and a time identity. Much as a room can require a floor number and a room number, this observation needs two indices. NumPy calls a regularly indexed numerical object an array. A two-dimensional array can be drawn as a table, while the same idea extends to images, volumes, and experiments with several varying conditions.

Writing down what one row and one column represent is often more important than remembering a function name. Swapping specimen and time axes can produce perfectly valid arithmetic and plausible-looking numbers while changing the scientific question. The computer knows that the array has three rows and five columns. It does not know that one dimension represents independently prepared specimens and the other represents repeated observations of those same specimens. We preserve those meanings through names, coordinate arrays, figure captions, and result metadata.

![A three-by-five thickness matrix linked to three time curves, with one observation highlighted.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ab2fa6932bc6e79c8baa793a.svg?v=ab2fa6932bc6)

Figure 1Two representations of the same constructed teaching data. Each matrix row is a specimen and each column is a time. The curves preserve the same specimen identities. The gold cell and ring identify one observation: specimen B is 1.16 mm thick at 20 min.

## Shape describes the indices; dtype describes each element

A Python list can contain several kinds of object, including other lists. A numerical NumPy array adds useful structure: its elements share a data type, and its dimensions form a regular shape. Passing three lists of length five to `np.array` creates an array with shape `(3, 5)`. The parentheses contain a tuple whose entries give dimension lengths in indexing order. These numbers are not the physical width and height of the film, and they are not the minimum and maximum values in the data.

`h.shape` is `(3, 5)`, `h.ndim` is 2, and `h.size` is 15. They answer three different questions: how long is each dimension, how many dimensions are there, and how many elements are stored? Flattening the same values into a one-dimensional array of length 15 preserves the element count but removes the visible grouping by specimen and time. Array dimension also differs from physical dimension. A collection of three-dimensional atomic coordinates is often stored in a two-dimensional array with shape `(number_of_atoms, 3)`: two indices locate an element, while three coordinate components describe space.

Here `dtype=np.float64` explicitly requests 64-bit floating-point numbers. Floating-point storage supports the decimal values used for thickness. The 64 bits describe a numerical representation, not the accuracy of the measuring instrument. Entering 1.20 mm does not tell NumPy that the measurement resolution was 0.01 mm; resolution, detection limits, and other experimental information need their own records. Integer arrays deserve particular care because assigning a fractional value to an integer element can truncate it. Choosing a type is therefore part of deciding how the observations will be represented.

A shared element type also makes the numerical storage requirement easy to estimate. Each float64 occupies 8 bytes, so fifteen elements occupy a 120-byte numerical buffer. Python also manages information about the array object, and a rendered figure stores colors, labels, and layout. Consequently, `h.nbytes` measures neither the entire program's memory nor the size of every output file. This distinction becomes useful when a small table grows into thousands of volumetric images: shape and bytes per element help determine an appropriate reading and processing strategy.

$$
B=N\,T\,b
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Number of bytes in the numerical array buffer, excluding Python object overhead. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Length of the first dimension, the specimen count, 3 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Length of the second dimension, the observation count, 5 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Bytes per element; float64 uses 8 bytes. |

Here 3×5×8=120 bytes, matching h.nbytes. A float64 uses 64 bits, and 8 bits make one byte. Rendering a heat map does not alter the numerical buffer; the image file additionally stores colors, text, and layout.

A regular rectangular shape should also reflect the observation design. If A was measured at 10 min but B's second observation was taken at 15 min, placing both in the same column would conceal a time difference. Keep the actual time associated with each record before deciding whether alignment or interpolation is justified. NumPy supplies the numerical container; the experiment determines whether the observations belong in this particular rectangular arrangement.

## Why scientific computing developed a common array object

Scientific work repeatedly applies the same rule to many values. Subtracting a reference temperature, calibrating every pixel, or translating all atomic coordinates are examples. In a hand calculation, we state the rule and then apply it to each value. A program can do the same with a loop. When a common operation on a structured collection occurs throughout an analysis, making the collection itself a well-defined object helps both expression and cooperation between tools.

The development of NumPy reflects this need. In their 2020 review, Harris and colleagues describe Numeric, which brought numerical arrays and array-aware functions to Python in the 1990s. Numarray subsequently developed capabilities including flexible indexing and memory handling for demands such as large astronomical images. Work on NumPy began in 2005 to bring earlier array developments into a common foundation. Although film measurements, telescope images, and molecular coordinates concern different subjects, each needs a clear account of where numerical values are stored, what type they have, and how an operation acts on them.

Seen this way, `h.mean(axis=0)` expresses more than a convenient abbreviation. It identifies an object, an operation, and a direction: compute the mean of `h` along axis 0. The array retains shape and type, and numerical functions can use that information consistently. A plotting library can interpret the values as point coordinates, an optimization library can use them to calculate residuals, and an image library can treat them as pixels. A shared representation reduces the need to reorganize the same data every time another scientific tool is introduced.

The storage strip in the figure lays out our values row by row. It separates the two-dimensional interpretation from the order of values in a numerical buffer. This is a schematic of the contiguous array created here; NumPy can also use strides to describe how indexing moves between elements, so a sliced view need not occupy one contiguous region. The next chapter examines shared data and views in detail. For now, the important point is that structural information participates in the calculation alongside the numbers themselves.

![Array storage, a scalar-to-array calculation correspondence, and the historical relationship among three array projects.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9ae4b94171f5aafc1261b9b8.svg?v=9ae4b94171f5)

Figure 2Array programming separates the numerical object from the operation. The top schematic shows row-major contiguous storage of this table; the middle links a hand calculation to its NumPy expression; the bottom outlines the relationship among Numeric, Numarray, and NumPy. NumPy can also describe noncontiguous views through strides. Historical context follows the NumPy review by Harris and colleagues.

## Locate a value, a row, or a column precisely

Python and NumPy indexing starts at zero. Specimens A, B, and C therefore have row indices 0, 1, and 2, while the five time positions have column indices 0 through 4. `h[1, 2]` selects the intersection of row index 1 and column index 2: the second row and third column in everyday counting. It returns 1.16. An index is an address, not a physical time. Writing `h[1, 20]` requests column index 20; it does not search for the observation taken at 20 min.

The separate `time_min` array records the physical coordinate associated with each column. Indices 0, 1, 2, 3, and 4 correspond to 0, 10, 20, 40, and 60 min. The later time gaps are larger, so a plot should position points at their actual times rather than spacing every observation equally. Keeping indices and coordinates distinct also helps determine whether two arrays of the same length genuinely refer to matching times.

`h[1, :]` selects all of specimen B's observations. The colon means retain every element along that dimension, and the output has shape `(5,)`. In contrast, `h[:, 2]` selects the column at 20 min and returns shape `(3,)`. Both outputs are one-dimensional, but one is a time history for a single specimen and the other is a distribution across specimens at one time. Drawing the first as a time curve and the second as a set of specimen points makes their distinct roles more visible.

An integer index usually removes its dimension. This is why `h[1, :]` and `h[1:2, :]` have different shapes despite containing the same five values. The integer selection leaves a one-dimensional array, whereas the slice retains a row interval starting at 1 and stopping before 2, producing shape `(1, 5)`. When an operation later raises a shape-related error, printing the shapes of its inputs is often more informative than trying different function names.

Translate a question into an index in two steps. Say, “I want the thicknesses of all three specimens at 20 min.” Identify time index 2, then write `h[:, 2]`. Check that the result contains three values and that their unit remains mm. This practice connects the question, the address, and the output size. As expressions become longer, assigning a descriptive name to the selected array also makes the intended meaning easier to follow.

### Build the array and average along both axes

time_min stores physical times separately, while h contains one kind of quantity: thickness. Axis 0 represents specimens and axis 1 represents time. The array does not automatically know these scientific meanings.

```
import numpy as np

time_min = np.array([0, 10, 20, 40, 60], dtype=float)
h = np.array([
    [1.00, 1.08, 1.14, 1.18, 1.20],
    [1.02, 1.09, 1.16, 1.21, 1.24],
    [0.98, 1.05, 1.11, 1.15, 1.18],
], dtype=np.float64)

print(h.shape, h.ndim, h.size)
print(h[1, 2])
print(h.mean(axis=0))
print(h.mean(axis=1))
print(h.std(axis=0, ddof=1))
```

## The reduced axis determines what remains

The phrase “average along axis 0” is easy to misread as a direction on a drawn chart. A more reliable interpretation is that the operation combines the elements of dimension 0 and preserves the other dimensions. In shape `(3, 5)`, dimension 0 has length three and represents specimens. Hold one time column fixed and combine its three specimen values into one average. Repeat for all five times, and five values remain, with shape `(5,)`.

The 20 min column provides a transparent hand calculation. Its thicknesses are 1.14, 1.16, and 1.11 mm. Their sum is 3.41 mm; dividing equally among three specimens gives 1.136666… mm. The added quantities share a unit, and the divisor is a dimensionless count, so the result remains a thickness. Index notation simply expresses “hold time fixed and vary the specimen” more explicitly.

$$
\bar{h}_{j}=\frac{1}{N}\sum_{i=0}^{N-1}h_{i,j}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | Thickness of specimen i at observation time j, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Specimen index, from 0 to N−1, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Observation-time index, dimensionless; the physical time is time_min[j]. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of specimens included in this average, 3 here, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Summation operator, adding thicknesses over the stated index range. |
| ![Formula](https://ml-biomat.com/static/agent-math/3356748dfad5e7f77344ed1d.svg) | Mean specimen thickness at time index j, in mm; the bar denotes an average. |

Hold j fixed, add thicknesses across specimen index i, and divide by the number of specimens. At 20 min, j=2, so (1.14+1.16+1.11)/3=1.136666… mm. The divisor is three specimens, not five times. h.mean(axis=0) performs this calculation for all five columns.

With `axis=1`, the dimension of length five is combined instead. Hold specimen A fixed, add its five observations, and divide by five to obtain 1.120 mm. The corresponding values for B and C are 1.144 and 1.094 mm. Specimen identity remains, so the output has length three. A useful check is to write the input shape and cross out the reduced dimension: `(3, 5) → (5,)` or `(3, 5) → (3,)`. A reduction combines several elements into fewer elements; sums, maxima, and means are all reductions.

$$
\bar{h}^{\mathrm{obs}}_{i}=\frac{1}{T}\sum_{j=0}^{T-1}h_{i,j}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | Thickness of specimen i at observation j, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | The fixed specimen index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Observation-time index varied in this expression, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Number of observations of this specimen, 5 here; T is a count, not temperature or duration. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum over the T listed observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/e88fa37eedbb9f408846d989.svg) | Mean observed thickness of specimen i, in mm; obs indicates equal weight per observation. |

For specimen A, (1.00+1.08+1.14+1.18+1.20)/5=1.120 mm. This summarizes the five observations with equal weights. The interval from 10 to 20 min differs from the interval from 40 to 60 min; an average over the full duration requires time weights or integration.

For a time-axis average, ask whether each observation should receive equal weight. Our early measurements are closer together than our later ones. An equal-weight mean answers, “What is the mean of these five observed thicknesses?” A mean over the complete 60 min duration instead requires the lengths of the time intervals and a choice about how thickness changes between observations. Integration will provide a way to connect that question to the area under a curve. A function can perform correct arithmetic while the research question determines which arithmetic is appropriate.

Without an axis argument, `h.mean()` combines all fifteen entries into approximately 1.119333 mm. This can describe the numerical center of the whole table, but it removes both time and specimen grouping. `keepdims=True` offers a separate choice about output shape: `h.mean(axis=0, keepdims=True)` returns shape `(1, 5)`. Keeping a length-one dimension makes later operations, such as subtracting each time's mean from every specimen, easier to align with the original shape.

![Time-resolved means and standard deviations beside mean observed thickness for each specimen.](https://ml-biomat.com/static/tutorials/python-scientific/figures/d6e6aede4231cfee1c74e6f5.svg?v=d6e6aede4231)

Figure 3The reduced axis determines the question. On the left, axis=0 combines three specimens and retains five times; error bars are the sample standard deviation among specimens at each time. On the right, axis=1 combines five observations within each specimen. Because times are unevenly spaced, these are equal-weight observation means, not continuous-time averages.

## Preserve specimen differences alongside the mean

At 60 min, the three thicknesses are 1.20, 1.24, and 1.18 mm, giving a mean of 1.206667 mm. A mean curve alone does not reveal whether it summarizes almost identical values or widely separated values. Retaining the specimen curves as thin colored lines and adding a stronger mean curve shows both common change and individual differences. A sample standard deviation at each time then summarizes the spread in the same unit as thickness.

Its calculation can be understood step by step. Subtract the mean at the chosen time from each specimen value. Positive deviations identify specimens thicker than the mean; negative deviations identify thinner specimens. Simply adding deviations would allow them to cancel, so square them before combining them. After calculating a variance, take a square root to recover the original unit. When estimating population spread from a sample, sample variance conventionally uses the divisor `N−1` because one mean was estimated from the same observations. NumPy expresses this choice with `ddof=1`; its default `ddof=0` uses N.

$$
s_j=\sqrt{\frac{1}{N-1}\sum_{i=0}^{N-1}(h_{i,j}-\bar{h}_j)^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9141db84cefd44582dab98f5.svg) | Sample standard deviation among specimens at time index j, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | Individual specimen thickness, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/2a421271888a0b4d29592461.svg) | Mean specimen thickness at the same time, in mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Specimen and time indices, respectively, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of included specimens at this time, 3 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/3c66a41ccc40e7bbec2752d5.svg) | Divisor used for sample variance after estimating one mean from the same observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/cee6a0fff7f10651952de6b6.svg) | Squaring makes deviations nonnegative; the square root returns the result to mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum of squared deviations across the N specimens. |

At 0 min the values are 1.00, 1.02, and 0.98 mm, with mean 1.00 mm. Squared deviations sum to 0.0008 mm²; division by 2 gives 0.0004 mm², and the square root is 0.020 mm. Use h.std(axis=0, ddof=1). This measures specimen-to-specimen spread; uncertainty in the estimated mean is a separate statistical quantity.

The error bars here are sample standard deviations among three specimens. They describe the spread of the observations. Instrument error, uncertainty in an estimated mean, and variation among specimens concern different questions and require different information. A specimen can differ from another specimen even if both are measured precisely; an average based on few specimens can also vary between repeated experiments. The figure caption should identify which quantity is displayed. Later statistics chapters develop standard errors and confidence intervals; here we first align specimen identities, units, and denominators.

Observing one specimen at five times does not create five independently prepared specimens. Specimen A's preparation, initial thickness, and many unmeasured characteristics can influence all of its later observations. In the array, that relationship is represented by an entire row belonging to one object. Retaining the row identity supports questions about within-specimen change. Treating all fifteen entries as independent specimens would describe a different experimental structure. Shape cannot replace experimental design, but it can help preserve that design in the analysis.

Missing values change the number of observations contributing to a result. If B has no record at 20 min, `np.nan` can mark the corresponding position. Ordinary `mean` propagates that missing value into the affected result, while `nanmean` skips it. With the latter operation, the mean at 20 min uses two specimens while other times use three, so counts belong beside the averages. Changing a function cannot recover the unobserved value or explain why it is missing. The interactive experiment makes the changed membership visible in the matrix, curves, and summary.

## Connect the calculation, saved data, and figures

The complete script processes this one dataset through several connected paths. Its numerical section computes means along both axes and sample standard deviations across specimens. Its saving section writes both NumPy's native array format and a simple CSV. Its plotting section organizes the same values into the figures above. The highlighted cell, curve point, and mean therefore refer to the same observations. Changing the input and rerunning the script updates all of those representations together.

A `.npy` file stores values together with information such as shape and dtype, so `np.load` restores the array directly. CSV is a text representation that is convenient for exchange with other software. Here values are written to two decimal places and read using an explicit comma delimiter. Because our input values already have two decimal places, this preserves the required numbers. Data with more meaningful digits needs a corresponding output precision. Specimen names, time units, and experimental interpretation are additionally recorded in `summary.json`.

The script includes two understandable checks. One recomputes every column average using Python addition and division, then compares it with the NumPy reduction. The other reloads saved data and compares it with the original input. The first checks arithmetic and reduction direction; the second checks file round-tripping. Both identify a specific link in the analysis. As datasets grow, similarly focused checks help detect changes in column order, unit conversion, or selection before those changes propagate into a figure.

The complete script also includes Matplotlib code. First follow the data path inside `main`: establish the array, calculate, check, save, and draw. Then inspect `figures` to see how numerical values become positions and colors. `style` changes visual presentation but does not contribute to the means. Separating numerical operations from presentation makes it easier to revise a figure while preserving its scientific result, and allows numerical and visual checks to be performed independently.

### Complete example: calculate, save, reload, and generate the figures

Requires NumPy and Matplotlib. main performs the calculations and round-trip checks; figures turns the same observations into an array diagram, axis comparison, and historical concept figure. style controls presentation only.

```
"""Represent repeated thickness measurements as an array and inspect both axes."""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches, font_manager

TIME = np.array([0, 10, 20, 40, 60], dtype=float)
SPECIMENS = ["A", "B", "C"]
THICKNESS = np.array([
    [1.00, 1.08, 1.14, 1.18, 1.20],
    [1.02, 1.09, 1.16, 1.21, 1.24],
    [0.98, 1.05, 1.11, 1.15, 1.18],
], dtype=np.float64)
COLORS = ["#28648a", "#b85336", "#467a62"]
INK = "#172b36"

def style():
    available = {font.name for font in font_manager.fontManager.ttflist}
    family = next((name for name in ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"] if name in available), "DejaVu Sans")
    plt.rcParams.update({"font.family": family, "font.size": 12, "axes.labelsize": 13,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "axes.edgecolor": INK, "axes.labelcolor": INK,
        "text.color": INK, "xtick.color": INK, "ytick.color": INK,
        "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6", "savefig.facecolor": "#fbfaf6",
        "svg.fonttype": "none", "pdf.fonttype": 42, "axes.unicode_minus": False})

def label(zh, en, language):
    return zh if language == "zh" else en

def save(fig, output, name, language):
    fig.savefig(output / f"{name}-{language}.svg", bbox_inches="tight", pad_inches=0.22)
    fig.savefig(output / f"{name}-{language}.png", dpi=170, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)

def figures(output, language, mean_time, mean_specimen, spread):
    t = lambda zh, en: label(zh, en, language)
    fig = plt.figure(figsize=(12.5, 6.8), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=[1.4, 1], height_ratios=[1, 0.27])
    ax = fig.add_subplot(grid[0, 0])
    im = ax.imshow(THICKNESS, cmap="cividis", vmin=0.95, vmax=1.25, aspect="auto")
    for i in range(3):
        for j in range(5):
            ax.text(j, i, f"{THICKNESS[i,j]:.2f}", ha="center", va="center", fontsize=16,
                    color="white" if THICKNESS[i,j] < 1.09 else INK)
    ax.add_patch(patches.Rectangle((1.5, .5), 1, 1, fill=False, lw=3.5, ec="#e4a321"))
    ax.set_xticks(range(5), [f"{int(v)}" for v in TIME]); ax.set_yticks(range(3), SPECIMENS)
    ax.set_xlabel(t("时间 / min（第1轴）", "Time / min (axis 1)")); ax.set_ylabel(t("样品（第0轴）", "Specimen (axis 0)"))
    ax.set_title(t("a  同一张表，两个索引", "a  One table, two indices"), loc="left", pad=16)
    cbar = fig.colorbar(im, ax=ax, shrink=.8, pad=.04)
    cbar.set_label(t("厚度 / mm", "Thickness / mm"))
    ax = fig.add_subplot(grid[0, 1])
    for i, color in enumerate(COLORS):
        ax.plot(TIME, THICKNESS[i], "o-", color=color, lw=2.2, ms=6, label=SPECIMENS[i])
    ax.scatter([20], [1.16], s=180, facecolor="none", edgecolor="#e4a321", lw=2.5, zorder=5)
    ax.annotate("h[1, 2] = 1.16 mm", xy=(20, 1.16), xytext=(25, 1.045),
                arrowprops={"arrowstyle":"->", "color": INK}, fontsize=12)
    ax.set(xlabel=t("时间 / min", "Time / min"), ylabel=t("厚度 / mm", "Thickness / mm"), ylim=(.95,1.27))
    ax.legend(title=t("样品", "Specimen"), frameon=False, ncol=3, loc="upper left")
    ax.set_title(t("b  行身份成为曲线身份", "b  Rows become individual curves"), loc="left", pad=16)
    ax = fig.add_subplot(grid[1, :]); ax.axis("off")
    lines = [t("shape = (3, 5)：3个样品 × 5个时刻", "shape = (3, 5): 3 specimens × 5 times"),
             t("ndim = 2：两个索引；size = 15：十五个数", "ndim = 2: two indices; size = 15: fifteen values"),
             t("教学构造数据；颜色与数字表示同一厚度。", "Constructed teaching data; color and number encode the same thickness.")]
    for y, text in zip([.82,.44,.06], lines): ax.text(.01,y,text,fontsize=13,transform=ax.transAxes)
    save(fig,output,"array-anatomy",language)

    fig = plt.figure(figsize=(12.5, 7.8), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=[1.45,1], height_ratios=[1,.8])
    ax = fig.add_subplot(grid[:, 0])
    for i, color in enumerate(COLORS): ax.plot(TIME, THICKNESS[i], "o-", color=color, lw=1.5, alpha=.75, label=SPECIMENS[i])
    ax.errorbar(TIME, mean_time, yerr=spread, fmt="D-", color=INK, lw=2.7, ms=6, capsize=5,
                label=t("均值 ± 样本标准差", "Mean ± sample SD"))
    ax.set(xlabel=t("时间 / min", "Time / min"), ylabel=t("厚度 / mm", "Thickness / mm"), ylim=(.94,1.28))
    ax.set_title(t("a  axis=0：每个时刻，汇总三个样品", "a  axis=0: combine specimens at each time"),loc="left",pad=16)
    ax.legend(frameon=False,loc="upper left",fontsize=11)
    ax.text(.04,.03,t("结果形状 (5,)；保留时间顺序", "Output shape (5,); time order is retained"),transform=ax.transAxes,fontsize=12)
    ax = fig.add_subplot(grid[0,1])
    ax.barh(SPECIMENS, mean_specimen, color=COLORS, height=.5)
    for i, value in enumerate(mean_specimen): ax.text(value+.015,i,f"{value:.3f}",va="center",fontsize=13)
    ax.set(xlabel=t("五个观测时刻的等权平均 / mm", "Equally weighted mean of five observations / mm"), xlim=(0,1.35))
    ax.invert_yaxis(); ax.set_title(t("b  axis=1：每个样品，汇总五个时刻", "b  axis=1: combine times within each specimen"),loc="left",pad=16)
    ax = fig.add_subplot(grid[1,1]); ax.axis("off")
    values=[t("留下什么？", "What remains?"),t("axis=0  →  时间，5个数", "axis=0  →  time, five values"),t("axis=1  →  样品，3个数", "axis=1  →  specimen, three values"),t("axis=None  →  全表，1个数", "axis=None  →  the whole table, one value"),t("时间间隔不等：行平均是观测平均。", "Unequal time gaps: row means average observations."),t("它与按持续时间加权的平均不同。", "A duration-weighted average answers another question.")]
    for y, text in zip([.92,.72,.54,.36,.14,.0], values): ax.text(.02,y,text,fontsize=12.5 if y<.9 else 14,weight="bold" if y>.9 else "normal")
    save(fig,output,"axis-reductions",language)

    fig, axes=plt.subplots(3,1,figsize=(12.5,7.8),gridspec_kw={"height_ratios":[1,.8,1]},layout="constrained")
    for ax in axes: ax.axis("off");ax.set_xlim(0,15);ax.set_ylim(0,1)
    ax=axes[0]
    ax.text(0,.97,t("a  一致的数据对象：数值 + 形状 + 类型", "a  One array object: values + shape + type"),weight="bold",fontsize=15)
    flat=THICKNESS.ravel()
    for k, value in enumerate(flat):
        ax.add_patch(patches.Rectangle((k+.03,.18),.92,.42,facecolor=COLORS[k//5],alpha=.17,edgecolor=COLORS[k//5]))
        ax.text(k+.49,.39,f"{value:.2f}",ha="center",va="center",fontsize=11)
    ax.text(.1,.03,t("连续存储示意；行优先排列", "Contiguous-storage schematic; row-major order"),fontsize=12)
    ax=axes[1]
    ax.text(0,.92,t("b  同一个计算规则，可以作用于整组数", "b  The same numerical rule acts on a group of values"),weight="bold",fontsize=15)
    ax.text(.25,.4,"(1.14 + 1.16 + 1.11) / 3",fontsize=20,color=INK)
    ax.annotate("",xy=(8.4,.45),xytext=(6.4,.45),arrowprops={"arrowstyle":"->","lw":2,"color":INK})
    ax.text(8.6,.4,"h.mean(axis=0)[2]",fontsize=20,color=COLORS[0])
    ax=axes[2]
    ax.text(0,.97,t("c  科学需求推动共同的数组接口", "c  Scientific needs motivate a common array interface"),weight="bold",fontsize=15)
    boxes=[(0,4.2,"Numeric",t("1990年代：Python中的数值数组", "1990s: numerical arrays in Python")),(5.1,4.2,"Numarray",t("大幅天文图像与灵活索引", "Large astronomical images and flexible indexing")),(10.2,4.6,"NumPy",t("2005：整合既有数组工作的方向", "2005: a shared direction for earlier array work"))]
    for x,w,name,description in boxes:
        ax.add_patch(patches.Rectangle((x,.15),w,.52,facecolor="#e8e6dc",edgecolor="none"))
        ax.text(x+.18,.48,name,fontsize=17,weight="bold")
        ax.text(x+.18,.27,description,fontsize=10.4)
    save(fig,output,"array-history",language)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="zh")
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True);style()
    mean_time=THICKNESS.mean(axis=0)
    mean_specimen=THICKNESS.mean(axis=1)
    spread=THICKNESS.std(axis=0,ddof=1)
    manual_columns=np.array([sum(THICKNESS[i,j] for i in range(3))/3 for j in range(5)])
    np.testing.assert_allclose(mean_time,manual_columns,rtol=0,atol=1e-14)
    np.save(args.output/"thickness.npy",THICKNESS)
    np.savetxt(args.output/"thickness.csv",THICKNESS,delimiter=",",fmt="%.2f")
    recovered=np.load(args.output/"thickness.npy")
    np.testing.assert_array_equal(recovered,THICKNESS)
    np.testing.assert_allclose(np.loadtxt(args.output/"thickness.csv",delimiter=","),THICKNESS,rtol=0,atol=1e-14)
    summary={"data_kind":"constructed teaching data","specimens":SPECIMENS,"time_min":TIME.tolist(),
             "thickness_mm":THICKNESS.tolist(),"shape":list(THICKNESS.shape),"ndim":THICKNESS.ndim,
             "size":THICKNESS.size,"dtype":str(THICKNESS.dtype),"nbytes":THICKNESS.nbytes,
             "mean_over_specimens_mm":mean_time.tolist(),"mean_over_observed_times_mm":mean_specimen.tolist(),
             "sample_sd_over_specimens_mm":spread.tolist(),"overall_mean_mm":float(THICKNESS.mean()),
             "npy_roundtrip_exact":bool(np.array_equal(recovered,THICKNESS))}
    (args.output/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    figures(args.output,args.language,mean_time,mean_specimen,spread)
    print(json.dumps({"shape":summary["shape"],"mean_over_specimens_mm":summary["mean_over_specimens_mm"]}))

if __name__=="__main__":main()
```

### Run the complete example

Run from the directory containing main.py. Outputs include summary.json, thickness.npy, thickness.csv, and SVG/PNG figures in the selected language. Both languages use identical numerical values.

```
python main.py --output output --language zh
python main.py --output output-en --language en
```

After running the example, inspect `summary.json` and compare its input shape `[3, 5]` with the lengths of the two mean arrays. Next inspect the fifteen CSV values. Finally, locate the highlighted 1.16 mm observation in the figure and check that it is still specimen B at 20 min. This sequence follows the meaning of the data from representation to output. A saved file shows that bytes were written; reading the numbers and matching a specific observation to the figure checks what those bytes represent.

## Change one observation and follow its consequences

The experiment below links an array, individual time curves, and a reduction output. Select specimen B at 20 min and increase that observation by 0.06 mm. One matrix cell changes and one point on B's curve moves. With `axis=0`, the mean at 20 min increases by 0.02 mm because three specimens share the change. With `axis=1`, B's observation mean increases by 0.012 mm because the divisor is five times. One controlled edit makes the difference between the reductions directly visible.

Now mark the selected observation as missing. The matrix shows an empty entry and the curve has a gap; each summary also displays its valid count. Along axis 0, A and C remain at 20 min, giving 1.125 mm. Along axis 1, B retains four observations, giving 1.140 mm. Skipping a missing value changes both the participating values and the divisor. Before comparing groups, check which records actually contribute to each result.

### Array experiment: one observation, three linked views

Select a cell, change it or mark it missing. The matrix, specimen curves, and reduction all use the same values. These are constructed teaching data; thickness is in mm.

Numerical array

[Figure: Numerical array](https://ml-biomat.com/tutorials/python-scientific/p07/en/#P07-matrix)

Specimen and mean curves

[Figure: Specimen and mean curves](https://ml-biomat.com/tutorials/python-scientific/p07/en/#P07-curves)

Reduction and valid counts

[Figure: Reduction and valid counts](https://ml-biomat.com/tutorials/python-scientific/p07/en/#P07-result)

The outlined cell, circled curve point, and highlighted result identify one observation. Missing values are skipped and each group's valid count is shown.

You can also move the edit to the initial time and inspect how it changes your impression of thickening. This experiment holds all other observations fixed to isolate the effect of one value. An actual measurement error may instead affect an entire batch or drift over time. Those cases require additional records describing the shared batch or instrument. Later chapters introduce labeled tables so that such scientific information can accompany numerical values explicitly.

You should now be able to describe what each axis represents, what an index selects, what a reduction retains, and how many specimens contribute to a statistic. When you next meet an image, coordinate set, or multi-condition experiment, sketch those dimensions before choosing an array shape. A clear representation gives indexing, broadcasting, fitting, and visualization a common basis.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

   Open introduction to arrays, shape, types, indexing, and saving.

   NumPy code and documentation: BSD-3-Clause; teaching narrative and figures here are independently written.
2. [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)

   Definitions of axis and keepdims.

   BSD-3-Clause documentation.
3. [numpy.std](https://numpy.org/doc/stable/reference/generated/numpy.std.html)

   Standard deviation and the ddof parameter.

   BSD-3-Clause documentation.
4. [Harris et al. — Array programming with NumPy (2020)](https://doi.org/10.1038/s41586-020-2649-2)

   Array programming and the history of Numeric, Numarray, and NumPy.

   Scientific attribution; original concept figures, no publisher artwork reproduced.
