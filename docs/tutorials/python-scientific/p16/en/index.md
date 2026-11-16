# From Clear Curves to a Scientific Figure

Source: https://ml-biomat.com/tutorials/python-scientific/p16/en/
Language: en

Connect an overview with linear and logarithmic details, preserving quantitative meaning across panels.

## How a composite figure makes a whole process readable

Imagine four containers that each initially hold 4 mg of a soluble substance. Material is removed at different rates, and you record how much remains over time. You can already draw four curves with Matplotlib. Preparing a report introduces a different set of questions. Should the curves share one coordinate system or occupy separate panels? How can you compare late stages when very little material remains? If you add a color image, how will readers recognize that its colors describe the same values as the curves? These decisions influence the scientific comparisons that a figure makes possible.

This chapter uses a fully specified teaching process to organize overview, detail, and quantitative interpretation into a composite scientific figure. An overview shows the range of behavior, a detailed view follows an individual trajectory, and a supporting panel explains the effect of a scale transformation. Think of a regional map accompanied by street maps and scale bars. Each element answers a different question, and their connections make the entire display useful. Increasing the number of panels helps only when the additional view carries a distinct part of the explanation.

We will use arrays, functions, and the Figure and Axes objects introduced in the previous chapter. Exponentials and logarithms will be explained through concrete values. By the end, you will be able to arrange shared coordinates, assign a common color scale to comparable images, and export vector graphics for a document. The organizing decision comes first: identify the quantities that readers need to compare, then choose the positions, scales, colors, and labels that make those comparisons accessible.

## What changes when numbers acquire common coordinates?

William Playfair’s 1786 *Commercial and Political Atlas* used charts to present trade and public accounts. Placing quantities along a time axis now feels familiar, but it gave columns of numbers a different mode of reading. A table makes an individual value easy to retrieve; common coordinates reveal increases, decreases, crossings, and gaps together. The Wellcome Collection’s original-edition catalogue records the work and its date. The diagram below recreates this change in representation using our teaching data, connecting a historical graphical idea to the Python work in this chapter.

![From retrieving tabular entries to comparing trajectories on common coordinates: an original diagram of the comparison principle associated with Playfair’s chart tradition. Points correspond to table entries and lines join those sampled positions. Values come from this chapter’s teaching model.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8341c4cf896af0483376bfed.svg?v=8341c4cf896a)

Figure 1From retrieving tabular entries to comparing trajectories on common coordinates: an original diagram of the comparison principle associated with Playfair’s chart tradition. Points correspond to table entries and lines join those sampled positions. Values come from this chapter’s teaching model.

The table lets you retrieve the mass at a particular time precisely. Comparing two processes requires holding several entries in mind and subtracting them. In the adjacent plot, values from the same row occupy a common vertical scale, so their difference becomes a visible height difference. The coordinate system performs part of the mental arithmetic. Separately autoscaled small panels would make similarly shaped trajectories look equally tall, sending the reader back to the tick labels. A shared scale therefore supports a specific comparison rather than merely giving panels a consistent appearance.

Graphs also change the order in which questions arise. You may first notice that two processes separate early, then inspect a particular numerical value. Generating the figure with code lets this reading structure follow updated data. A changed model rule or an additional condition can propagate to the lines, colors, and legends together. Keeping a clear relationship between data and drawing instructions gives the figure a durable role in an evolving analysis.

## Build curves whose values can be checked directly

We define a simple removal process: equal time intervals remove equal proportions of the material currently present. When more remains, the amount removed per unit time is larger; as the container empties, the absolute removal rate falls. Repeatedly withdrawing a small fraction from a well-mixed liquid offers a useful physical analogy. The continuous version of this rule produces exponential decay. It supplies smooth positive teaching curves with several points that can be checked by hand.

$$
m(t)=m_0\exp(-t/\tau)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | Remaining mass at time t, mg |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Initial mass, 4 mg here |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, min |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Time constant, 1, 2, 4, or 8 min |
| ![Formula](https://ml-biomat.com/static/agent-math/d7bdddb2b2f38a1d246c4b23.svg) | Natural exponential function; its input and output are dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Generic argument of the exponential, here −t/τ; dimensionless |

Equal durations correspond to equal remaining fractions; continuous multiplication produces an exponential. Dividing t by τ cancels minutes. At t=0, exp(0)=1 and the mass is 4 mg. At t=τ=4 min, exp(−1)≈0.367879, giving 4×0.367879≈1.47152 mg.

The time constant τ controls how far the curve spreads horizontally. With τ = 1 min, about 36.8% of the initial mass remains after one minute. With τ = 8 min, reaching that same fraction takes eight minutes. All four curves begin at 4 mg because the initial mass is held constant. Each row of our array stores a complete trajectory for one time constant; each column contains the values at one common time. Establishing these directions makes it straightforward to place time horizontally and conditions in separate heatmap rows.

The program divides the interval from 0 to 12 min into 241 time points and uses broadcasting to calculate an array of shape 4 × 241. This dense grid comes from an explicit mathematical function, so every entry is a model value. For experimental data, retain the actual sampling times and use markers to identify observations. Both kinds of data can be joined with lines, but the line has a different meaning: here it represents a known continuous function, whereas experimental connecting segments usually help readers follow adjacent observations.

A useful comparison point is the time at which the remaining mass reaches 2 mg, half its initial value. Substituting that value into the model shows that the half-time is proportional to τ. Marking these positions on the linear panel connects the algebraic relationship to horizontal distance. When τ = 4 min, the half-time is approximately 2.773 min. The half-time and the 4 min time constant identify two different fractions of the starting mass.

$$
t_{1/2}=\tau\ln 2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | Time required to reach half the initial mass, min |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Exponential time constant, min |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | Natural logarithm, the inverse of exp; its argument is dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/f5f3224583db57b9cfe323c8.svg) | Ratio of initial mass to half-mass; dimensionless |

Set m(t)/m₀=1/2 and take natural logarithms to obtain −t/τ=−ln2. Multiplication by −τ gives the half-time. For τ=4 min, t₁/₂=4×0.693147≈2.77259 min, and substitution into the model returns 2 mg.

## Use an overview for range and details for reading values

The composite figure gives its upper region to an overview and its lower region to two views of the trajectories. Time runs horizontally in the overview, four rows represent four time constants, and color represents remaining mass. Scanning the heatmap reveals which conditions retain material and when their behavior diverges. The lower-left panel uses an ordinary linear mass scale, making differences in milligrams directly readable. The lower-right panel uses a logarithmic vertical scale, allocating visible space to small late-stage quantities that differ by large factors.

![Four teaching exponential models share a 4 mg initial value and one 0–4 mg color range. The top rows are discrete conditions. Lower left marks half-times; lower right uses logarithmic spacing while retaining mass units.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e00cd461da5f09b0aae2d2bc.svg?v=e00cd461da5f)

Figure 2Four teaching exponential models share a 4 mg initial value and one 0–4 mg color range. The top rows are discrete conditions. Lower left marks half-times; lower right uses logarithmic spacing while retaining mass units.

Matplotlib’s `subplot_mosaic` expresses this arrangement with named panels. The first layout row contains two adjacent occurrences of `'map'`, producing one panel that spans both columns. The second row contains `'linear'` and `'log'`, producing separate panels. The resulting dictionary lets drawing statements address `ax['linear']` directly. Names become particularly useful when the layout changes: a line still belongs to the linear view even after that view moves to another position in the figure.

`layout='constrained'` allocates room for tick labels, axis titles, and colorbars. It adjusts panel placement using the space occupied by these decorations, which makes repeated generation easier than repeatedly changing margins by hand. The overall figure dimensions still depend on the intended reading size. A label that looks spacious on a monitor can become difficult to read in a narrow document column. Inspect the saved figure at its final placement size, paying particular attention to units, legends, and colorbar ticks.

The heatmap’s four rows represent discrete models and have equal visual heights. Vertical distance does not encode the numerical spacing between time constants. Explicit labels of 1, 2, 4, and 8 preserve that interpretation. A study that requires interpolation along a continuous parameter axis needs the actual parameter grid and appropriate cell boundaries. Before drawing an image, identify separately what position, area, and color represent; each can carry a different part of the quantitative meaning.

## What changes when you change coordinates or colors?

On a linear vertical axis, the interval from 1 mg to 2 mg occupies the same distance as the interval from 2 mg to 3 mg: both add 1 mg. On a logarithmic axis, equal distances correspond to equal ratios. The intervals 0.01 to 0.1, 0.1 to 1, and 1 to 10 each represent a factor of ten. Exponential decay becomes a straight line on a semilogarithmic plot, with a steeper decline corresponding to a shorter time constant. The transformation redistributes display space while tick labels and the stored data retain the original mass units.

A logarithmic scale requires positive values. An exact zero calls for a representation chosen from the meaning of the data: a linear scale, an explicitly marked detection threshold, or a transformation suitable for signed values may be appropriate. Adding a small arbitrary constant changes ratios among small values. In this chapter the exponential function remains positive at every finite time, allowing us to examine the effect of the logarithmic scale directly.

$$
u_{\rm linear}=\frac{m-m_{\min}}{m_{\max}-m_{\min}},\qquad u_{\rm log}=\frac{\ln(m/m_{\min})}{\ln(m_{\max}/m_{\min})}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1e48cd157a8c7e656e0ed609.svg) | Position in a linear color map; dimensionless, from 0 to 1 within the limits |
| ![Formula](https://ml-biomat.com/static/agent-math/de2636f600afbad84bba9c98.svg) | Position in a logarithmic color map; dimensionless, from 0 to 1 within the limits |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Mass to map, mg; positive for the logarithmic expression |
| ![Formula](https://ml-biomat.com/static/agent-math/c48390dbe4819072144e626a.svg) | Lower color limit, mg; strictly positive for log mapping |
| ![Formula](https://ml-biomat.com/static/agent-math/f4112cac5b9e25ee587461ea.svg) | Upper color limit, mg; greater than the lower limit |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | Natural logarithm, applied to dimensionless mass ratios |

For linear limits of 0 and 4 mg, 1 mg maps to (1−0)/(4−0)=0.25. For logarithmic limits of 0.01 and 4 mg, it maps to ln100/ln400≈0.76862. The same 1 mg value receives different color positions, which the respective colorbars explain. Values beyond the limits receive endpoint colors or explicitly assigned out-of-range colors.

Color introduces another mapping step. First, a mass value is placed within a standard interval from zero to one; the resulting position then selects a color. `Normalize(0,4)` maps 0 mg to the beginning and 4 mg to the end of the colormap, placing 1 mg at 0.25. Reusing one Normalize object gives the same mass the same color across panels. `LogNorm` instead allocates space according to ratios between positive values, which can reveal structure across several orders of magnitude. In either case, a colorbar labeled with physical units provides a route back to the underlying quantity.

![The upper panels compare linear and logarithmic color mapping for identical positive masses. Below, raw masses differ by a factor of four, while division by each initial value makes the remaining-fraction curves coincide.](https://ml-biomat.com/static/tutorials/python-scientific/figures/590242f059b92496f191f9e7.svg?v=590242f059b9)

Figure 3The upper panels compare linear and logarithmic color mapping for identical positive masses. Below, raw masses differ by a factor of four, while division by each initial value makes the remaining-fraction curves coincide.

The lower panels show a third operation. Dividing sample A by its own initial mass of 4 mg and sample B by its own initial mass of 1 mg makes their curves overlap. This calculation creates a new quantity, the remaining fraction, which answers whether the progress of the two processes is similar. The original mass plot answers how much material remains, and its two trajectories stay a factor of four apart. Coordinate scaling, color scaling, and normalization of a physical quantity serve different questions; their axis labels and captions should identify the corresponding quantity.

## Preserve meaning in geometry, markers, and text

A curve places each time value directly at a point’s horizontal coordinate. A heatmap must instead give each value a small rectangular area. That difference introduces a detail worth examining: an image boundary and a pixel center occupy different positions. Adjacent calculation times in this chapter are 0.05 min apart. The image boundaries extend outward by 0.025 min on each side, while the visible horizontal range remains 0 to 12 min. The first and last pixel centers consequently sit at 0 and 12, and every intermediate column aligns with its calculation time. Cropping at the axis boundaries displays half of each endpoint pixel.

`imshow` suits a regularly arranged matrix. It spreads equal-width and equal-height pixels across a specified extent, so directly applying it to irregular experimental times changes the meaning of horizontal position. For observations at 0, 1, 3, and 8 min, first establish the time interval represented by each value, then use a function such as `pcolormesh` with explicit cell boundaries when a colored-cell display is appropriate. A point plot is often more direct for a few isolated observations. Understanding what region each cell represents helps determine whether a plotting function matches the structure of the data.

Lines, points, and filled regions also need distinct responsibilities. Sequential color in the overview represents increasing mass. Colors in the line panels identify conditions, and the legend explains those identities. Every color change therefore has a specific job. Circular markers at half-mass emphasize calculated times and come from the same function as the dense curves. Adding experimental observations would call for a visually distinct marker style so readers can distinguish measurements from calculations. Grayscale printing and differences in color perception also affect readability; a few curves can combine color with line style, while important positions can use labels or shapes.

Axis ranges should follow the intended comparison. Enlarging a narrow vertical interval helps expose small differences, and readers also need to locate that interval within the full variation. One solution retains the complete process as the main panel and adds a detail panel with its range marked explicitly. This chapter provides complementary linear and logarithmic views of the complete time interval, with both horizontal axes fixed at 0 to 12 min. If later work focuses on a late-stage window, give the detail panels the same time limits so readers can compare positions without repeated coordinate conversion.

Export choices affect quantitative communication too. SVG works well for figures built from curves, text, and rectangles because their boundaries remain clear when enlarged. A microscopy image containing millions of pixels can retain its raster image while scale bars and labels remain vector elements. Setting `svg.fonttype='none'` stores labels as editable text; the device opening the file needs a suitable font, particularly for Chinese characters. PNG instead fixes the final display as pixels and can be exported at a resolution matched to the intended document dimensions. Both formats benefit from inspection at the actual reading size.

It is useful to distinguish the size of a data marker from the quantity being measured. In this chapter, equal-sized points mark selected positions and carry no additional variable. If a future scatter plot uses marker area to represent mass, its legend must show how area maps to that quantity; doubling the radius would quadruple the area. Similar reasoning applies to line thickness and opacity. A graphical element can make information easier to find without encoding a new measurement, provided its role remains clear in the surrounding explanation.

## A complete program, from arrays to reusable figures

The program calculates four trajectories and saves them as CSV before generating three figures from the same values. `mass[2]` selects the full trajectory for τ = 4 min. `mass[:, 80]` selects the four values at the eighty-first time point. The first operation reads along time, while the second compares conditions. Transposing with `mass.T` puts time points into rows for export, so each spreadsheet row corresponds to one time. A transpose rearranges entries without recalculating their mass values.

The colorbar is constructed from the heatmap object, `image`, and therefore shares its normalization range and colormap. The legend comes from the labels assigned to curves. These objects have different jobs: a legend identifies which condition a line belongs to, while a colorbar translates a continuous color into a mass. Changing `taus` offers a useful extension exercise. Follow the change through the row labels, curve labels, and half-times. In a general-purpose version, generate these labels from the parameter array so that annotations follow the calculation automatically.

### Complete Python: shared arrays, figure composition, and color mapping

Calculate the model with NumPy and generate all figures using Matplotlib named panels, normalization objects, and vector export.

```
"""Compose scientific figures from explicitly defined teaching depletion curves."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import Normalize, LogNorm

BLUE, RED, INK = '#28658c', '#b64a35', '#20313e'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    def tr(a, b): return a if zh else b
    def save(fig, name):
        fig.savefig(args.output/f'{name}-{args.language}.svg')
        fig.savefig(args.output/f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}], 'font.size':12,
                         'svg.fonttype':'none', 'axes.spines.top':False,
                         'axes.spines.right':False, 'axes.labelcolor':INK,
                         'axes.titleweight':'bold', 'savefig.facecolor':'white'})
    t = np.linspace(0, 12, 241)
    taus = np.array([1., 2., 4., 8.])
    mass = 4 * np.exp(-t[None, :] / taus[:, None])
    np.savetxt(args.output/'curves.csv', np.column_stack([t, mass.T]), delimiter=',',
               header='time_min,mass_tau1_mg,mass_tau2_mg,mass_tau4_mg,mass_tau8_mg', comments='')
    norm = Normalize(0, 4)
    fig, ax = plt.subplot_mosaic([['map','map'],['linear','log']], figsize=(12,9),
                                 layout='constrained', gridspec_kw={'height_ratios':[1.05,1]})
    # Rows represent four discrete models; row labels retain physical relaxation times.
    image = ax['map'].imshow(mass, extent=[-.025,12.025,3.5,-.5], aspect='auto',
                             interpolation='nearest', cmap='viridis', norm=norm)
    ax['map'].set(xlim=(0,12), yticks=range(4), yticklabels=['1','2','4','8'], xlabel=tr('时间 / min','Time / min'),
                  ylabel=tr('时间常数 / min','Time constant / min'), title=tr('A  总览：相同质量色标','A  Overview: one mass scale'))
    fig.colorbar(image, ax=ax['map'], label=tr('剩余质量 / mg','Remaining mass / mg'), shrink=.9)
    colors=plt.colormaps['viridis'](np.linspace(.15,.8,4))
    for tau, row, color in zip(taus, mass, colors):
        for key in ['linear','log']:
            ax[key].plot(t,row,color=color,lw=2,label=f'τ = {tau:g} min')
        ax['linear'].scatter([tau*np.log(2)],[2],color=color,s=28,zorder=5)
    ax['linear'].axhline(2,color='#71808b',ls=':',lw=1)
    ax['linear'].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('剩余质量 / mg','Remaining mass / mg'),
                     ylim=(0,4.2),title=tr('B  线性轴：比较绝对差值','B  Linear axis: absolute differences'))
    ax['log'].set_yscale('log'); ax['log'].set(xlabel=tr('时间 / min','Time / min'),
        ylabel=tr('剩余质量 / mg（对数刻度）','Remaining mass / mg (log scale)'),
        title=tr('C  对数轴：比较倍数与速率','C  Log axis: ratios and rates'))
    for key in ['linear','log']:
        ax[key].set_xlim(0,12); ax[key].grid(alpha=.15); ax[key].legend(fontsize=10,frameon=False)
    save(fig, 'composition')

    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    z=np.array([[.01,.1,1.,4.]])
    for ax, n, title in [(axes[0,0],Normalize(0,4),tr('A  线性颜色：差值相等','A  Linear color: equal differences')),
                          (axes[0,1],LogNorm(.01,4),tr('B  对数颜色：倍数相等','B  Log color: equal ratios'))]:
        im=ax.imshow(z,aspect='auto',norm=n,cmap='viridis'); ax.set(yticks=[],xticks=range(4),
            xticklabels=['0.01','0.1','1','4'],xlabel=tr('选取的质量值 / mg','Selected mass values / mg'),title=title)
        fig.colorbar(im,ax=ax,label=tr('质量 / mg','Mass / mg'),orientation='horizontal',pad=.18)
    a=4*np.exp(-t/4); b=np.exp(-t/4)
    for ax, normalized in [(axes[1,0],False),(axes[1,1],True)]:
        ax.plot(t,a/4 if normalized else a,color=BLUE,lw=2,label=tr('样品 A，初始 4 mg','Sample A, initially 4 mg'))
        ax.plot(t,b if normalized else b,color=RED,lw=2,ls='--',label=tr('样品 B，初始 1 mg','Sample B, initially 1 mg'))
        ax.set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('剩余比例','Remaining fraction') if normalized else tr('质量 / mg','Mass / mg'),
               title=tr('D  除以各自初值：曲线重合','D  Divide by each initial value: overlap') if normalized else tr('C  原始量：A 是 B 的 4 倍','C  Raw quantity: a factor of four'))
        ax.legend(frameon=False,fontsize=10); ax.grid(alpha=.15)
    save(fig, 'mapping')

    fig=plt.figure(figsize=(12,5.2),layout='constrained');axes=fig.subplots(1,2,gridspec_kw={'width_ratios':[.8,1.2]})
    axes[0].axis('off')
    values=np.column_stack([np.arange(0,13,3),4*np.exp(-np.arange(0,13,3)/2),4*np.exp(-np.arange(0,13,3)/8)])
    table=axes[0].table(cellText=[[f'{r[0]:.0f}',f'{r[1]:.2f}',f'{r[2]:.2f}'] for r in values],
        colLabels=[tr('时间/min','Time/min'),'τ=2 min','τ=8 min'],cellLoc='center',loc='center')
    table.auto_set_font_size(False);table.set_fontsize(12);table.scale(1,2.2)
    axes[0].set_title(tr('数字：逐项读取','Numbers: read item by item'),loc='left')
    axes[1].plot(values[:,0],values[:,1],'o-',color=BLUE,label='τ=2 min')
    axes[1].plot(values[:,0],values[:,2],'s-',color=RED,label='τ=8 min')
    axes[1].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('剩余质量 / mg','Remaining mass / mg'),
                title=tr('共同坐标：同时比较过程','Common coordinates: compare processes'))
    axes[1].legend(frameon=False);axes[1].grid(alpha=.15)
    fig.suptitle(tr('从 Playfair 1786 年图表传统到可复现科学图','From Playfair’s 1786 chart tradition to reproducible figures'),fontsize=15)
    save(fig, 'history')
    summary={'versions':{'numpy':np.__version__,'matplotlib':matplotlib.__version__},
             'initial_mg':float(mass[2,0]),'tau4_t4_mg':float(4/np.e),
             'half_times_min':(taus*np.log(2)).tolist(),'half_mass_mg':2.,
             'linear_color_1mg':float(norm(1)), 'log_color_1mg':float(LogNorm(.01,4)(1)),
             'raw_mass_ratio':4.,'normalized_difference_max':float(np.max(np.abs(a/4-b)))}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__': main()
```

The resulting `summary.json` reports several checkable values: an initial mass of 4 mg, approximately 1.47152 mg after 4 min when τ = 4 min, and half-times of approximately 0.693, 1.386, 2.773, and 5.545 min. The raw mass ratio is four, and the maximum difference between the two remaining-fraction curves is zero. `curves.csv` contains all 241 time points. The three SVG files provide the composite scientific figure, the mapping comparison, and the historical concept diagram shown in the chapter. SVG retains geometric information for lines and text, making it convenient for enlargement and document layout.

## Link colors, curves, and numerical readings

The experiment samples the heatmap every 0.5 min, giving 25 displayed times. Its curves use the same formula as the 241-point Python grid. Three views remain linked. Selecting a time constant and time moves the highlighted heatmap location and the markers in both curve panels together. Start with τ = 4 min and time 4 min: both curve panels identify approximately 1.472 mg. Change the time constant to 8 min while retaining time 4 min, and the remaining mass becomes approximately 2.426 mg. The selected value changes while the mass color scale remains fixed, giving its color change a quantitative interpretation.

### One dataset, three views

Select time and condition to track one mass through all views. Lower the color limit to compare saturated colors with the unchanged numerical values.

[Figure: Mass overview and selected location](https://ml-biomat.com/tutorials/python-scientific/p16/en/#P16-map)

[Figure: Linear mass curve](https://ml-biomat.com/tutorials/python-scientific/p16/en/#P16-linear)

[Figure: Logarithmic mass curve](https://ml-biomat.com/tutorials/python-scientific/p16/en/#P16-log)

Now lower the upper color limit from 4 mg to 2 mg. Cells above the limit accumulate at the end of the colormap, emphasizing distinctions among smaller masses. The trajectory panels and exact numerical readout retain their original values because this control changes the display mapping. A count of grid points above the color limit makes the saturated region inspectable. In a saved figure, this upper limit belongs on the colorbar; when several figures will be compared, decide explicitly whether they should share the same range.

Finally, choose a short time constant and a late time. The selected point approaches the baseline in the linear panel but remains separated from other small values in the logarithmic panel. These two views expose different aspects of the same result: a small absolute quantity and a potentially large ratio. Which view deserves the main position depends on whether the question concerns remaining mass, proportional differences, or removal rate.

## Apply the arrangement to your own data

Your data may come from release experiments, sensors, temperature sweeps, or mechanical measurements. Begin with one sentence describing the comparison the figure should support, such as identifying conditions that look similar early and diverge later. Then identify the quantities that must be inspected together. With many conditions, an overview heatmap can help locate regions of interest. With only a few, superimposed curves may be easier to read. The number of panels follows the work the reader needs to perform.

For several comparable heatmaps, combine their value ranges first and construct one normalization object for all plotting objects. Panels that show different units need separate colorbars with explicit quantity names. Repeated measurements introduce another requirement: retain sample points and identify the meanings of means, intervals, and sample counts. The following chapter develops those statistical distinctions. The smooth teaching trajectories here have no measurement noise, so their displays show the calculated functions and their transformations directly.

After assembling a figure, read it in the order a new reader is likely to follow. Identify the first panel encountered, the location of units, the color assigned to each condition, and the place to check the key numerical value. Write the central observation of each panel in a brief caption and see whether it can be read from the image. If doing so requires repeated searches across unrelated legends, revise the labels or layout. A well-organized figure lets relationships between quantities occupy the foreground while coordinates and markings handle routine lookup and conversion.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P16.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Matplotlib: constrained layout](https://matplotlib.org/3.10.9/users/explain/axes/constrainedlayout_guide.html)

   Allocate layout space for axis labels, legends, and colorbars

   Matplotlib license; original teaching code and figures
2. [Matplotlib: subplot mosaic](https://matplotlib.org/3.10.9/users/explain/axes/mosaic.html)

   Compose named panels with different spans

   Matplotlib license; original teaching code and figures
3. [Matplotlib: colormap normalization](https://matplotlib.org/3.10.9/users/explain/colors/colormapnorms.html)

   Understand normalization followed by color lookup

   Matplotlib license; original teaching code and figures
4. [Matplotlib: choosing colormaps](https://matplotlib.org/3.10.9/users/explain/colors/colormaps.html)

   Choose sequential or diverging maps from the meaning of quantities

   Matplotlib license; original teaching code and figures
5. [Playfair, The Commercial and Political Atlas (1786), Wellcome Collection](https://wellcomecollection.org/works/kau5c9ny)

   Original-edition record and historical context of graphical comparison

   Historical bibliographic reference; no image or text reproduction
