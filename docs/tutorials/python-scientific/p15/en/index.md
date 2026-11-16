# How a Scientific Figure Is Built

Source: https://ml-biomat.com/tutorials/python-scientific/p15/en/
Language: en

Start with six calibration records and connect data, plotting objects, and screen positions to make deliberate changes to a figure.

## Start with six records and a question for the figure

A scientific figure helps us see relationships that are difficult to inspect one table cell at a time. Does an instrument reading increase with concentration? Does one record depart from the pattern formed by the others? Do two samples change over the same interval? These questions determine what the horizontal axis, vertical axis, and visual marks need to represent. Before choosing colors, write the question as a concrete sentence. In this chapter, six concentration–absorbance records provide a small enough example to inspect completely while we learn how data become a figure and how to change its coordinates, text, and output deliberately.

The data are explicitly defined for teaching. Concentrations are 0, 0.1, 0.2, 0.3, 0.4, and 0.5 mmol/L; the corresponding absorbances are 0.032, 0.111, 0.205, 0.296, 0.389, and 0.481. Each pair is one record. Elements at the same position in the two arrays must stay paired. The concentration unit mmol/L expresses millimoles of the relevant substance per liter of solution. Absorbance describes attenuation of light by a sample and is normally reported as a dimensionless quantity. These teaching values model an instrument reading that rises with concentration, letting us trace the position of each of the six points in a figure.

On paper, the table allows us to read every value precisely. To judge the overall pattern, however, we have to move between cells and remember their relationships. A scatter plot maps each record to a location: horizontal position represents concentration, and vertical position represents absorbance. All six points share the same axes, which makes their relative positions directly comparable. The mapping also involves choices. Color might identify a sample group, area might encode another quantity, and a connecting line might imply a sequence. Each choice should carry a meaning that we can explain.

Matplotlib provides objects for organizing those choices. A useful analogy is an experimental record sheet with clearly assigned responsibilities. The complete sheet has a size and an output format; one region holds a coordinate system; points, lines, text, and legends occupy that region. The analogy helps us decide which object to modify, although the software is more flexible than a physical sheet. A single Figure can contain several plotting regions, each showing different variables or sharing the same time axis with its neighbors.

By the end of the chapter, you should be able to identify Figure, Axes, Axis, and Artist objects, write a scatter-plot program that saves its output, and explain an initially surprising observation: a point can move on the screen while its numerical values remain unchanged. This distinction becomes the common foundation for zooming, comparing panels, keeping annotations in fixed corners, and preparing figures at appropriate output sizes.

![Concentration versus absorbance scatter plot alongside Figure, Axes, Axis, and Artist responsibilities](https://ml-biomat.com/static/tutorials/python-scientific/figures/0714706a459ec6104fda5f15.svg?v=0714706a459e)

Figure 1Six explicitly defined teaching calibration records and the responsibilities of plotting objects. The red ring marks record 4. Figure, Axes, and Axis also belong to the Artist hierarchy; the list describes responsibilities rather than four nested containers.

## Why plotting must support exploration and publication

Matplotlib grew from a specific scientific workflow. In his own account, its creator John D. Hunter described developing an interactive application for electroencephalography data. As the work expanded to databases, network communication, and more complicated data structures, he moved toward Python and wanted a two-dimensional plotting library that was easy to use, could be embedded in a graphical interface, and could produce high-quality scientific graphics. The connection is familiar in many fields: the numbers inspected on a screen are often the same numbers later presented in a publication.

During exploration, we may change a time window, examine a local fluctuation, or select a signal segment. During presentation, we choose fixed limits, readable units, and an export that can be placed in a document. One collection of plotting objects can support both tasks. Objects describe the lines, locations, text, and properties; an output backend then renders those descriptions into an interactive window, a PNG image, or an SVG file.

The method diagram below uses two teaching waveforms generated from explicitly defined sine functions. Their amplitudes are in arbitrary units. They illustrate how multichannel data pass through a common plotting structure to different output media. The key relationship runs from data to objects to rendered output. A different medium can change resolution or interaction, while the identity and numerical values of the records should remain consistent.

![Multichannel illustrative signals connect through plotting objects to an interactive window and vector output](https://ml-biomat.com/static/tutorials/python-scientific/figures/918390314e12702f1115a5ef.svg?v=918390314e12)

Figure 2A historical need addressed by Matplotlib: the same data must support interactive exploration and saved scientific graphics. The two signals on the left are teaching waveforms generated from sine functions, with arbitrary amplitude, to explain a multichannel workflow.

This background also explains why Matplotlib offers both a convenient command-oriented interface and explicit object operations. A few short commands work well for quickly inspecting a curve. When a figure contains several regions, lines, and annotations, keeping references to the relevant objects makes modifications easier to locate. We will retain the names `fig` and `ax` so that each command has an identifiable target.

## The responsibilities of Figure, Axes, and Artist

A `Figure` represents the complete graphical output. It knows the overall size, contains plotting regions, and provides methods for saving the result. An `Axes` is a plotting region in which data coordinates are defined. Although the word ends in “s,” one Axes object can represent a single region; the name does not necessarily mean a collection. The call `plt.subplots()` creates a Figure and an Axes, and we store the two returned objects in `fig` and `ax`.

An `Axis` manages the ticks, tick labels, axis label, and related coordinate-reading machinery for one direction. A typical two-dimensional Axes has a horizontal and a vertical Axis. Decisions such as whether a tick reads 0.10 or 0.1 and how ticks are spaced involve these objects. The names Axes and Axis look similar, but their roles differ: the former provides a plotting space for data, whereas the latter organizes the numbers used to read a coordinate. Distinguishing them helps you find the relevant interface in the documentation.

`Artist` is the common base class for drawable objects. Figure, Axes, and Axis participate in this hierarchy, as do the objects used for points, lines, and text. The four terms are therefore not four boxes nested in a simple sequence. For example, the markers in a scatter plot are normally managed by a `PathCollection` within the Axes; a plotted line is commonly a `Line2D`; and a text item is a `Text`. You do not need to memorize every class immediately. What matters is that a plotting operation creates an object whose properties can be inspected or changed later.

The small program below retains three useful references. `fig` identifies the complete figure for saving; `ax` identifies the region whose limits and labels we set; and `points` identifies the collection of scatter markers. These names do not create three copies of the image. They allow the program to find the appropriate object again. A method call such as `ax.scatter(...)` asks that Axes to perform an operation, while the arguments specify the data, color, and marker size used by the operation.

### Create a figure through explicit objects

Elements at matching positions in concentration and absorbance form one record. fig refers to the whole figure, ax to its plotting region, and points to the collection of markers. Each setting targets a specific object.

```
import matplotlib.pyplot as plt

concentration = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
absorbance = [0.032, 0.111, 0.205, 0.296, 0.389, 0.481]
fig, ax = plt.subplots(figsize=(6.2, 4.2), layout="constrained")
points = ax.scatter(concentration, absorbance, color="#28658c", s=45)
ax.set(xlabel="Concentration / mmol L⁻¹", ylabel="Absorbance / dimensionless",
       xlim=(0, 0.6), ylim=(0, 0.55))
fig.savefig("calibration.svg")
plt.show()
```

The assignment `fig, ax = plt.subplots(...)` uses sequence unpacking: the function returns two objects, and the two names receive them in order. The argument `figsize=(6.2, 4.2)` sets the width and height to 6.2 and 4.2 inches. These dimensions matter when the figure is placed in a document. `layout="constrained"` asks the layout engine to allocate space around plots and labels, reducing the chance that an axis label extends beyond the canvas. The saved output still needs inspection, especially when long labels or wide text have been added.

In a script, `fig.savefig(...)` writes a file and `plt.show()` requests a display window. A notebook may also display the Figure automatically as part of its cell output. Displaying and saving are distinct actions. An analysis script should save its result explicitly and make the destination clear, so its output remains available even in an environment that does not open a graphical window. This separation is especially useful when processing several datasets in a batch.

## Give each visual mark an explainable meaning

Concentration and absorbance are two fields from the same record, so a scatter plot is a natural first representation. Position carries the numerical relationship. Equal marker sizes and a single color keep attention on the coordinates. If different experimental batches are introduced, color or shape can identify the batch, with an explicit legend. When one record is emphasized with a larger marker, an outline or annotation should explain the emphasis; otherwise, a reader may reasonably infer that marker area encodes mass, concentration, or sample count.

A line connecting two points also makes a statement. When successive times track the same sample, a line helps follow the sequence. Six independently prepared calibration concentrations are first six discrete observation locations. A fitted relationship can be added after specifying a model and an estimation method. Simply connecting points in array order describes that ordering; it does not establish a physical law. The fitting chapter will return to the question of how a model is constructed from observations and how its residuals are assessed.

An axis label should identify both the quantity and its unit. “Concentration / mmol L⁻¹” and “Absorbance / dimensionless” make it clear why a value of 0.3 on one axis has a different meaning from 0.3 on the other. The notation L⁻¹ means per liter and is equivalent to writing mmol/L. Tick labels are normally rounded for readability, while the arrays retain their actual values. Showing two decimal places on an axis does not increase the precision of the underlying measurement.

Grid lines, colors, and spacing help comparison when they support the data. A light horizontal grid helps the eye connect a marker's height with a tick value. A dark, dense grid competes with the markers. Across several views, reuse a color for the same scientific identity: blue might refer to the complete dataset, and red to the currently selected record. If the red ring, red guide lines, and numerical readout all identify the same record, the reader can trace that record from one view to another without repeatedly decoding a new legend.

Axis limits are also a scientific communication choice. Including zero helps readers judge absolute magnitudes and proportions. A restricted range can reveal a small variation that is important to a different question. Make the limits and ticks explicit, and consider showing both a global and a local view when each carries useful information. Shared limits in adjacent panels allow direct comparison of amplitudes. Separately auto-scaled panels require readers to check the tick values before deciding whether visually similar curves also have similar numerical ranges.

## How data coordinates become positions in a plot

A record has data coordinates before it has a screen position. On a linear concentration axis spanning 0 to 0.6 mmol/L, a concentration of 0.3 mmol/L is halfway across. If the same axis instead spans 0 to 1.2 mmol/L, that value lies one quarter of the way across. Imagine a ruler whose displayed numerical interval can change. A fixed value occupies a different fraction of the ruler when the total interval changes.

$$
u=\frac{x-x_{\min}}{x_{\max}-x_{\min}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4620fefc72ebf96810ce9f34.svg) | Horizontal position as a fraction of the Axes width, dimensionless; 0 is left and 1 is right |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Horizontal data value; concentration in mmol/L here |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd27db42b5426d22e4e9954.svg) | Left and right limits of a linear horizontal axis, in the same units as x; right must exceed left |

Subtract the left limit to measure distance from the origin of the displayed interval, then divide by its width. A concentration of 0.30 mmol/L has u=0.50 on a 0–0.60 mmol/L axis and u=0.25 on a 0–1.20 mmol/L axis. Its concentration remains 0.30 mmol/L. This expression describes an increasing linear axis; a logarithmic axis requires applying the same logarithm to the value and limits first.

The horizontal fraction is not a new experimental quantity. It describes placement inside the plotting region. The numerator measures how far the value lies from the left limit; the denominator is the width of the displayed interval. Their units cancel. The resulting fraction directly locates the point on an increasing linear axis. On a logarithmic axis, equal visual distances represent equal ratios, so the data and limits undergo a logarithmic transformation before placement. Zero and negative values then require specific treatment.

$$
v=\frac{y-y_{\min}}{y_{\max}-y_{\min}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Vertical position as a fraction of Axes height, dimensionless; 0 is bottom and 1 is top |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Vertical data value; dimensionless absorbance in this example |
| ![Formula](https://ml-biomat.com/static/agent-math/547e3985a94f06060d90cef2.svg) | Lower and upper limits of an increasing linear vertical axis, in the same units as y |

The vertical calculation follows the same logic. Absorbance 0.296 on a 0–0.55 axis lies at 0.296/0.55≈0.5382, or about 53.82% of the height measured upward from the bottom. Browser pixel coordinates normally increase downward, so the SVG implementation converts this upward fraction into a downward screen position; it does not change the sign of the measured quantity.

The selected record in this example is record 4, which is element 3 under Python's zero-based indexing. Its concentration is 0.300 mmol/L and its absorbance is 0.296. With the original limits, the horizontal fraction is 0.50 and the vertical fraction is approximately 0.5382. Changing the horizontal maximum to 1.20 changes the horizontal fraction to 0.25 while leaving the vertical fraction unchanged. The figure below draws the same arrays in two separate Axes; the red ring and guide lines keep the correspondence visible.

![The same scatter data compared on concentration axes spanning 0–0.6 and 0–1.2](https://ml-biomat.com/static/tutorials/python-scientific/figures/99eaea6ed233c0b47cc187ef.svg?v=99eaea6ed233)

Figure 3Identical data displayed with two horizontal ranges. Record 4 remains at 0.300 mmol/L and absorbance 0.296. Doubling the horizontal range moves it from 50% to 25% of the plot width by changing the display mapping.

Matplotlib packages these transformations into objects. An annotation placed in data coordinates moves with the data when limits change. An annotation using `ax.transAxes` is positioned by a fraction of the Axes width and height; a note near the upper-right corner can therefore remain in that corner during zooming. Figure coordinates are relative to the complete figure. The final rendering converts these descriptions into pixels or the coordinates required by another output format. Knowing which coordinate system you selected explains why some labels follow a curve and others stay in a fixed corner.

This distinction also separates enlarging a figure from expanding its horizontal data range. Enlarging the output gives the same data interval more pixels. Expanding the data interval makes a fixed value occupy a smaller fraction of the plotting region. The first operation concerns physical size and output resolution; the second concerns the mapping of data to the figure. Recording both settings makes multi-panel comparisons easier to interpret and prevents display differences from being mistaken for differences between samples.

## Test your prediction in two linked views

The interactive experiment separates selection of a record from selection of axis limits. The left panel keeps its original range. The right panel uses your settings, while both red rings refer to the same record. Predict a point's movement before changing a control. For record 4, expanding only the horizontal maximum from 0.60 to 1.20 should move the point left to one quarter of the plot width. Raising the vertical maximum to 1.10 should then move it down to approximately 26.91% of the plot height.

### Where does a point go when the axis limits change?

Both panels display the same six teaching records. Select a record and expand the right panel's horizontal or vertical limits. Watch the red marker, guide lines, and relative coordinates move together. The left panel retains its original limits as a reference.

[Figure: Data in the original coordinate range](https://ml-biomat.com/tutorials/python-scientific/p15/en/#P15-reference)

[Figure: Data in the current coordinate range](https://ml-biomat.com/tutorials/python-scientific/p15/en/#P15-current)

Concentration / mmol L⁻¹**0.300**

Absorbance / dimensionless**0.296**

Horizontal fraction u**0.5000**

Vertical fraction v**0.5382**

```
ax.set(xlim=(0, 0.60), ylim=(0, 0.55))
```

Connect three layers while observing the result. The displayed concentration and absorbance are the record's data values. The horizontal and vertical fractions describe the coordinate mapping. The location of the red ring is the visible result of that mapping. Coordinated changes in the numbers, guides, and marker location make the calculation inspectable. If the fraction changes but the point remains stationary, investigate the plotting update. If a change in display limits also changes the reported experimental value, investigate whether the code has accidentally modified the data array.

Selecting the first record provides a useful boundary check. Its concentration is zero, so it should stay at the left limit regardless of the horizontal maximum. Its absorbance is 0.032, however, so it does not lie at the origin. This example separates a zero horizontal coordinate from a record whose two coordinates are both zero. Similarly, record 6 retains a concentration of 0.5, greater than record 4's 0.3, even when different axis ranges place their markers at visually similar locations.

The command readout corresponds to `ax.set(xlim=..., ylim=...)`. Writing the same limits into the Python program should reproduce the same normalized positions. The interactive view can therefore inform a reproducible script: use interaction to explore and check a choice, then retain the selected parameters, data, and plotting code so that the final figure can be generated again.

## Run the complete program and preserve the mapping

The complete program defines the six teaching records once and shares them across all three figures. This reduces the chance of introducing inconsistent values through manual copying. The function `plot_data` handles the scatter marks and common labels; `save` exports a Figure as SVG and PNG. The historical method diagram separately generates its illustrative signals from specified sine functions. Repeated plotting work is placed in functions so that changes to a common label or style do not require editing several copies.

### Generate the chapter data, figures, and numerical summary

Save as main.py and run python main.py --output output --language en; use zh for Chinese. The script writes three SVG/PNG figures, calibration.csv, and summary.json. Every calibration plot uses the same arrays. Dependencies are NumPy and Matplotlib.

```
"""Build three scientific figures from one explicitly defined teaching dataset."""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch

BLUE, RED, INK, GRAY = "#28658c", "#b64a35", "#202e39", "#71808b"


def make_figures(output, language):
    output.mkdir(parents=True, exist_ok=True)
    zh = language == "zh"
    def tr(chinese, english):
        return chinese if zh else english
    plt.rcParams.update({"font.family": [name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],
                         "font.size": 12, "axes.labelsize": 12,
                         "axes.titlesize": 14, "axes.titleweight": "bold",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": INK, "text.color": INK,
                         "xtick.color": INK, "ytick.color": INK,
                         "svg.fonttype": "none", "svg.hashsalt": "P15",
                         "savefig.facecolor": "white"})
    concentration = np.array([0, .1, .2, .3, .4, .5], dtype=float)
    absorbance = np.array([.032, .111, .205, .296, .389, .481])
    selected = 3
    def save(fig, name):
        fig.savefig(output / f"{name}-{language}.svg", metadata={"Date": None})
        fig.savefig(output / f"{name}-{language}.png", dpi=180)
        plt.close(fig)
    def plot_data(ax, xmax=.6, ymax=.55):
        points = ax.scatter(concentration, absorbance, s=65, color=BLUE,
                            edgecolors="white", linewidths=.8, zorder=3, clip_on=False)
        ax.set(xlim=(0, xmax), ylim=(0, ymax),
               xlabel=tr("浓度 / mmol L⁻¹", "Concentration / mmol L⁻¹"),
               ylabel=tr("吸光度 / 无量纲", "Absorbance / dimensionless"))
        ax.grid(axis="y", color="#dce3e8", linewidth=.7, zorder=0)
        return points

    fig = plt.figure(figsize=(12.4, 6.4))
    fig.patch.set_edgecolor("#bccbd5"); fig.patch.set_linewidth(2)
    ax = fig.add_axes([.09, .18, .54, .67])
    points = plot_data(ax)
    ax.annotate(tr("第4行记录", "Record 4"),
                xy=(concentration[selected], absorbance[selected]),
                xytext=(.1, .43), textcoords="data", color=RED,
                arrowprops={"arrowstyle": "->", "color": RED})
    ax.scatter([concentration[selected]], [absorbance[selected]],
               s=140, facecolors="none", edgecolors=RED, linewidths=1.7, zorder=4)
    fig.text(.09, .94, tr("Figure：组织整张输出", "Figure: the complete output"),
             fontsize=17, weight="bold")
    fig.text(.09, .075, tr("Axes：这块绘图区有自己的数据范围", "Axes: a plotting region with its own data limits"), color=BLUE)
    hierarchy = [("Figure", tr("整张图、尺寸与保存", "Canvas, size, and export")),
                 ("Axes", tr("绘图区与数据坐标", "Plot region and data coordinates")),
                 ("Axis", tr("Axes中的刻度与轴标签对象", "Ticks and axis labels within Axes")),
                 ("Artist", tr("所有可绘制对象的共同基类", "The common base for drawable objects"))]
    for i, (name, detail) in enumerate(hierarchy):
        y = .79 - i * .16
        fig.text(.70, y, name, fontsize=16, weight="bold", color=BLUE if i == 1 else INK)
        fig.text(.70, y - .055, detail, fontsize=11)
        if i == 0:
            fig.add_artist(FancyArrowPatch((.72, y - .075), (.72, y - .113),
                           transform=fig.transFigure, arrowstyle="->", color=GRAY,
                           mutation_scale=12))
    save(fig, "anatomy")

    fig = plt.figure(figsize=(12.4, 5.7))
    signal_ax = fig.add_axes([.07, .25, .35, .57])
    t = np.linspace(0, 2, 400)
    first = .65 * np.sin(2 * np.pi * 3 * t)
    second = .3 * np.sin(2 * np.pi * 5 * t) + .15 * np.cos(2 * np.pi * t)
    signal_ax.plot(t, first + 1.1, color=BLUE, lw=1.7)
    signal_ax.plot(t, second - .65, color=RED, lw=1.7)
    signal_ax.set(xlabel=tr("时间 / s", "Time / s"), yticks=[], xlim=(0, 2), ylim=(-1.2, 2.2))
    signal_ax.set_title(tr("多通道数据提出交互需求", "Multichannel data call for interaction"), loc="left", fontsize=13)
    signal_ax.text(.02, .94, tr("教学信号；振幅为任意单位", "Illustrative signals; arbitrary amplitude"), transform=signal_ax.transAxes, color=GRAY, fontsize=9, va="top")
    fig.text(.48, .65, tr("同一组绘图对象", "One set of plotting objects"), fontsize=14, weight="bold")
    fig.text(.48, .52, "Figure → Axes → Artists", fontsize=12, color=BLUE)
    for y, title, detail in [(.76, tr("交互窗口", "Interactive window"), tr("选择、放大与回看", "Select, zoom, and inspect")),
                              (.31, tr("矢量输出", "Vector output"), tr("坐标、文字和图形\n一起保存", "Save coordinates, text,\nand marks"))]:
        fig.text(.79, y, title, weight="bold", fontsize=14)
        fig.text(.79, y - .09, detail, fontsize=10)
        fig.add_artist(FancyArrowPatch((.67, .57), (.77, y - .025), transform=fig.transFigure,
                        arrowstyle="->", color=GRAY, mutation_scale=16))
    fig.add_artist(FancyArrowPatch((.42, .54), (.47, .54), transform=fig.transFigure,
                    arrowstyle="->", color=GRAY, mutation_scale=16))
    fig.text(.07, .95, tr("从数据探索到可出版图形", "From data exploration to publishable figures"), fontsize=17, weight="bold")
    fig.text(.07, .065, tr("方法关系图；曲线由明确的正弦函数生成。", "Method diagram; signals are generated from defined sine functions."), color=GRAY, fontsize=10)
    save(fig, "history")

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.4), layout="constrained")
    for ax, xmax, name in zip(axes, [.6, 1.2], [tr("原坐标范围", "Original limits"), tr("横轴范围扩大一倍", "Twice the horizontal range")]):
        plot_data(ax, xmax=xmax)
        ax.scatter([concentration[selected]], [absorbance[selected]], s=140,
                   facecolors="none", edgecolors=RED, linewidths=1.7, zorder=4)
        ax.vlines(concentration[selected], 0, absorbance[selected], color=RED, linestyle="--", lw=1)
        ax.hlines(absorbance[selected], 0, concentration[selected], color=RED, linestyle="--", lw=1)
        u = concentration[selected] / xmax
        ax.text(.04, .95, f"c = 0.300 mmol L⁻¹\nA = 0.296\nu = {u:.2f}",
                transform=ax.transAxes, ha="left", va="top", fontsize=12)
        ax.set_title(name, loc="left")
    save(fig, "coordinates")
    np.savetxt(output / "calibration.csv", np.c_[concentration, absorbance], delimiter=",",
               header="concentration_mmol_L,absorbance", comments="", fmt="%.6f")
    summary = {"data_kind": "explicitly defined teaching data", "n_records": len(concentration),
               "selected_record_zero_based": selected,
               "concentration_mmol_L": concentration.tolist(), "absorbance": absorbance.tolist(),
               "selected": {"c_mmol_L": float(concentration[selected]), "absorbance": float(absorbance[selected]),
                            "u_original": float(concentration[selected] / .6),
                            "u_expanded": float(concentration[selected] / 1.2),
                            "v": float(absorbance[selected] / .55)},
               "versions": {"numpy": np.__version__, "matplotlib": matplotlib.__version__}}
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    options = parser.parse_args()
    make_figures(options.output, options.language)
```

After the program finishes, `calibration.csv` contains the two numerical columns actually plotted. `summary.json` records the selected row and its coordinate fractions. The three SVG/PNG pairs explain object responsibilities, the connection between exploration and output, and the effect of changing axis limits. Together, these outputs let you move from a figure back to its numbers and from the numbers back to its program. A screenshot alone does not reveal which records were selected or how the coordinates were mapped.

The actual calculations give six records, selected concentration 0.3, absorbance 0.296, original horizontal fraction 0.5, expanded horizontal fraction 0.25, and vertical fraction approximately 0.5381818. The divisions introduced above provide a simple independent check. The program also writes the NumPy and Matplotlib versions used at runtime, which helps reproduce the result in another environment. Version information complements inspection of the values and their meaning rather than replacing it.

If Chinese labels appear as empty squares, check whether the system has a font containing the required characters and select an installed font in the font-family list. Font selection affects text rendering, not the numerical calculation. The example checks installed Noto Sans CJK SC, Noto Sans SC, Microsoft YaHei, and SimHei in that order, retaining DejaVu Sans for Latin text. Different systems can use whichever of these Chinese fonts is available. Inspect the output again after changing fonts because the same label can occupy a different width and may need additional space.

## Save a result that remains readable

PNG stores an image as pixels and is useful for browser previews and many document workflows. SVG describes much of a plot through vector elements such as paths and text, making it useful for scaling and subsequent layout. An SVG containing photographs or raster heat maps can also embed pixel images, so its extension does not guarantee that every layer is vector. Choose the format for the final task: curves and text should remain clear when scaled, while microscopy data should retain their underlying pixels and calibration.

Output dimensions must be considered together with the intended reading size. If a figure is designed with very small labels and later reduced to half-column width, its labels become difficult to read. Raising a PNG's dpi increases the number of pixels but does not resolve a crowded legend. First arrange an appropriate figure size, font size, panel count, and spacing; then select sufficient output resolution. This order preserves information hierarchy at the size a reader will actually encounter.

After saving, check that all six records can be found, the labels and units are complete, the red ring selects record 4, and the two comparison panels contain identical data. Then reduce the figure to its intended reading size and inspect the smallest ticks, labels, and caption. Numerical checks verify that data and transformations agree. Visual inspection verifies that a reader can actually recover that agreement from the figure.

Once these relationships are clear, plotting becomes a set of purposeful operations. You know which object saves the complete figure, which object sets a data range, why a marker appears at a particular location, and which coordinate system anchors an annotation. The next chapter uses these relationships to organize multiple views into a scientific figure that answers a more substantial question.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P15.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Matplotlib Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html)

   Figure, Axes, and the object-oriented plotting interface

   Matplotlib documentation license
2. [Matplotlib Transformations Tutorial](https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html)

   Data, Axes, Figure, and display coordinate systems

   Matplotlib documentation license
3. [John D. Hunter: Matplotlib History](https://matplotlib.org/stable/project/history.html)

   The creator's account of EEG analysis and the requirements for a plotting library

   Matplotlib documentation license
4. [Matplotlib Introduction to Artists](https://matplotlib.org/stable/users/explain/artists/artist_intro.html)

   Containers, primitive drawing objects, and the Artist hierarchy

   Matplotlib documentation license
5. [Matplotlib Figure.savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)

   Export formats, dimensions, and save options

   Matplotlib documentation license
