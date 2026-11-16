# Indexing and Broadcasting along the Right Axis

Source: https://ml-biomat.com/tutorials/python-scientific/p08/en/
Language: en

Select observations, pair baselines, correct offsets, and trace shared array storage.

## Pair every observation with the right reference

Three specimens gradually become thicker in a liquid. Which one changes most? Comparing their final thicknesses also includes differences already present before the experiment. A more useful question is how much each specimen changes relative to its own initial thickness. If the measuring instrument also develops a zero offset during the experiment, a time-specific correction comes first. This chapter uses one three-by-five array to connect slicing, conditional selection, and broadcasting. By the end, you should be able to identify the selected observations, explain their numerical pairings, and predict whether editing a selection changes the original data.

We continue with the constructed thickness records from the preceding chapter. Rows represent specimens A, B, and C; columns represent 0, 10, 20, 40, and 60 min; thickness is measured in millimeters. A changes from 1.00 to 1.20, B from 1.02 to 1.24, and C from 0.98 to 1.18. The values support transparent hand calculations rather than reporting a laboratory experiment. Although the table is rectangular, the time intervals are unequal. An array index describes a storage position; the associated time array supplies its physical coordinate.

Imagine a measurement cabinet whose rows identify specimens and whose columns identify observation times. Selecting compartments retrieves observations. Giving each row its own initial compartment establishes the reference. Applying the same rule throughout the cabinet performs an array calculation. None of these operations automatically understands that A is a specimen or that 10 means minutes. We translate measurement meaning into shapes and indices, then check the translation against numerical relationships we already understand. An expression that runs successfully still needs to pair the intended quantities.

## Slices select positions; coordinates supply the time

The expression `h[1, 2]` selects position 1 on axis 0, specimen B, and position 2 on axis 1, the 20 min column. Its result is 1.16 mm. Indexing starts at zero, and the order follows the shape (3,5). Selecting an axis with a single integer removes that axis from the result: `h[1]` is a one-dimensional array of five values, whereas `h[1:2]` remains a two-dimensional array with one row and five columns. They contain the same thicknesses but retain different structural information for subsequent operations.

In `h[:, 1:4]`, the first colon keeps every specimen. The slice `1:4` selects positions 1, 2, and 3, excluding stop position 4. It therefore retrieves 10, 20, and 40 min and returns shape (3,3). An excluded stop makes adjoining intervals convenient: `0:2` and `2:5` neither overlap nor leave a gap. A second colon introduces a step. For example, `h[:, ::2]` selects columns 0, 2, and 4. Their times are 0, 20, and 60 min, so selecting every second column does not create evenly spaced physical observations.

For a physical time interval, express the condition on the time coordinates. The expression `(time >= 10) & (time <= 40)` produces five Boolean values, each stating whether its time lies within the interval. Placing this Boolean array in the column position, as `h[:, selected]`, retrieves those time columns for every specimen. Parentheses keep each comparison together; `&` combines them position by position. Python’s `and` operates on whole conditions and is not a replacement for this elementwise combination of arrays.

Use the same selection on the time coordinates when selecting thicknesses. A plot of three thickness columns needs the corresponding three times. Keeping five old coordinates, or treating new positions 0, 1, and 2 as minutes, changes the meaning of the plot. Reordering specimen rows similarly requires reordering their names. NumPy preserves positional relationships, while names and units need to remain synchronized alongside them. Later chapters introduce labeled tables and multidimensional data structures that help express these connections directly.

![The same measurements as a full table, baseline column, and selected window. Equal-width heatmap columns are labeled with actual minutes.](https://ml-biomat.com/static/tutorials/python-scientific/figures/5d56c8ffd1e12d031f3ac107.svg?v=5d56c8ffd1e1)

Figure 1The same measurements as a full table, baseline column, and selected window. Equal-width heatmap columns are labeled with actual minutes.

Negative indices count from the end, so `h[:,-1]` selects each specimen’s final stored observation and returns shape (3,). “Final” describes the array’s ordering and means latest in time only when the time coordinates are sorted. Check those coordinates after reordering records. A slice may also legally return an empty array, for example when its starting position lies beyond the available values. An empty selection means that no observations were selected; it does not mean zero thickness. Check the number of selected elements before calculating a summary that requires observations.

## Selecting specimens differs from selecting individual values

The shape of a condition determines what is being selected. Calculate each specimen’s final relative change and compare it with 21%. This produces a Boolean array of length three, one decision per specimen. Used in the row position, it selects complete specimen records. Here only B reaches approximately 21.57% at 60 min, so the selection retains B’s entire row. The selection criterion concerns the final observation, while the retained object is the whole trajectory. This is useful when asking which specimens meet a response criterion and then examining how they reached it.

By contrast, `h > 1.15` produces a three-by-five Boolean array that tests every one of the fifteen observations. The expression `h[h > 1.15]` returns a one-dimensional collection of matching values; their former rectangular arrangement is no longer retained. Such a collection can help inspect value ranges but is not directly a time trajectory. To trace the observations back, obtain row and column positions with `np.nonzero`, then look up their specimen names and times. If a rectangular structure is needed, mark unwanted positions while retaining the grid instead of immediately compressing them into a vector.

An integer index array can select positions in a specified order. For example, `h[[2,0]]` returns the C and A rows. The nested brackets have separate jobs: the inner list describes the positions, and the outer brackets apply that selection to the array. Unlike a continuous basic slice, this advanced indexing can reorder or repeat elements and returns independently stored values. A later editing example makes the storage consequence visible. First establish which scientific identities should be selected, then check whether the resulting shape still represents those identities.

A selection rule is itself part of the analysis definition. The 21% threshold distinguishes array-selection behavior in this teaching example; a material performance requirement would instead come from the research task or measurement convention. Display rounding can also hide small differences near a threshold. Apply an explicit comparison to the underlying numbers and round only for presentation. A value displayed as 20.00% may be represented by a floating-point number slightly above or below its ideal decimal value, so the numerical comparison rule should be understood independently of its printed appearance.

Selection order can change the scientific reference. One workflow identifies specimens from their final response and then selects a time window. Computing relative changes on the full time record before selecting the display window preserves the initial reference. If the initial column is removed first and the remaining window’s first column becomes the new baseline, the result instead describes change relative to the window’s start. Both questions can be useful, but they use different reference states. Indexing order therefore affects more than array shape; it can change what comparison is being made.

## How one baseline column serves an entire table

Relative thickness change is current thickness divided by initial thickness, minus one. Dividing lengths with the same unit produces a dimensionless ratio. Subtracting one moves the unchanged initial state to zero. For B at 20 min, the calculation is 1.16 mm divided by 1.02 mm, minus one: approximately 0.137255, or 13.73%. It describes the proportional increase in thickness. Interpreting this as a volume change would require information about the other dimensions or a specified deformation relationship, so the quantity here remains explicitly a thickness change.

$$
\varepsilon_{ij}=\frac{h_{ij}}{h_{i0}}-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e1dffe683e6706f37bf2ad55.svg) | Relative thickness change of specimen i at time j, dimensionless; multiply by 100 to express percent |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Specimen and time position indices, dimensionless; i=0,1,2 and j=0,…,4 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dbf6e5f545cd01f55d42bc3.svg) | Corresponding thickness, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3abf426a48c1d4f6a951f9ce.svg) | The same specimen’s initial thickness, mm, required positive |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | The ratio of the initial thickness to itself, dimensionless |

Length units cancel. For B at 20 min, 1.16/1.02−1=0.1372549, or 13.73%; initial thickness divided by itself minus one gives zero.

The expression `baseline = h[:, 0:1]` retains a column of three initial thicknesses with shape (3,1). In `h / baseline - 1`, NumPy pairs each baseline with every time observation in its own row. All A values are divided by 1.00, all B values by 1.02, and all C values by 0.98. This is broadcasting. Think of each specimen’s reference ruler being attached beside its row: moving along that row keeps using the same ruler. The numerical expression is short because the shape describes how the ruler should be reused.

Broadcasting checks shapes from the rightmost dimension. Equal dimensions can pair position by position. A dimension of size one can supply its single position repeatedly along the corresponding dimension of the other array. For (3,5) and (3,1), compare 5 with 1 first, then 3 with 3. Both pairs are compatible, giving a result of shape (3,5). This structural rule checks neither physical units nor which axis represents a specimen. Writing the meaning of each dimension beside its size is more informative than memorizing that a column can divide a table.

The expression `h[:,0]` instead returns shape (3,), with no explicit time dimension. Aligning it from the right with (3,5) compares 3 against 5 and raises a shape error. Inserting an axis using `h[:,0,None]` or `h[:,0][:,None]` also produces (3,1). In this indexing context, `None` inserts a dimension; its role differs from using None as a missing value in a record. Retaining the first column with `0:1` is often the clearest starting point because it visibly preserves the original measurement structure.

Broadcasting avoids materializing repeated copies of a small input, but the full calculation result usually still needs storage. Fifteen values are inexpensive here. Accidentally combining large axes into every possible pairing, however, can produce an output much larger than either input. Estimate the result shape before execution. Multiplying its element count by eight gives the basic numerical-buffer size for float64 values, after which other arrays retained by the program also need consideration. Shape reasoning therefore connects scientific pairing with practical memory use.

Transposing a one-dimensional array does not automatically create a column. An array of shape (3,) has only one axis, so its `.T` still has shape (3,). A two-dimensional row of shape (1,3) transposes to (3,1). Numbers written horizontally on paper have a visual arrangement; array dimensions are an actual structure. For one reference per specimen, explicitly retain the specimen axis and a singleton time axis. For one correction per time, retain a singleton specimen axis and the time axis. Printed orientation alone does not establish those dimensions.

## Corrections follow time; baselines follow specimens

Introduce a defined calibration condition: an independent calibration record says the instrument reads too high by 0, 0.01, 0.02, 0.03, and 0.04 mm at the five observation times, with the same effect on all specimens at a given time. These are supplied teaching calibration offsets, not a trend inferred from the specimen response. Correct thickness by subtracting the corresponding offset from each column. In `h - drift[None,:]`, the correction has shape (1,5): time positions match individually, while the specimen direction reuses the same correction.

$$
h^{\mathrm{corr}}_{ij}=h_{ij}-d_j,\qquad \varepsilon^{\mathrm{corr}}_{ij}=\frac{h^{\mathrm{corr}}_{ij}}{h^{\mathrm{corr}}_{i0}}-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcb192a1662d80f082b86f72.svg) | Corrected thickness, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/8dbf6e5f545cd01f55d42bc3.svg) | Instrument thickness reading, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa5d90d675f75ab6ffeebf3.svg) | Known excess reading at time j, mm; shared by all specimens here |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Specimen and time position, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d13ee63029543cfd8b898aca.svg) | Corrected initial thickness, mm, required positive |
| ![Formula](https://ml-biomat.com/static/agent-math/c9e06ef0b2ebc976afe19222.svg) | Corrected relative thickness change, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | Normalized initial ratio, dimensionless |

For B at 20 min, 1.16−0.02=1.14 mm. The initial offset is zero, giving 1.14/1.02−1=0.1176471, or 11.76%.

Normalize the corrected thicknesses by each specimen’s corrected initial thickness so that numerator and denominator use a consistent definition. The initial offset happens to be zero here, leaving the baseline unchanged. If it were nonzero, the denominator would need correction too. At 60 min, A is corrected from 1.20 to 1.16 mm and changes by 16%; B from 1.24 to 1.20 mm and changes by approximately 17.65%; C from 1.18 to 1.14 mm and changes by approximately 16.33%. The separation of solid and dashed curves follows the supplied calibration, not a preference for whichever curve looks smoother.

![Top: changes before and after the supplied drift correction. Bottom: a wrong broadcast passes shape checks when both axes happen to have length three.](https://ml-biomat.com/static/tutorials/python-scientific/figures/b2789f3d5a6d383a78488480.svg?v=b2789f3d5a6d)

Figure 2Top: changes before and after the supplied drift correction. Bottom: a wrong broadcast passes shape checks when both axes happen to have length three.

A subtler shape problem appears when retaining only the first three columns, giving a (3,3) table. Dividing this by the initial-thickness array of shape (3,) now runs successfully because the rightmost dimensions both have size three. But it pairs 1.00, 1.02, and 0.98 with the three time columns. A at 20 min is consequently divided by C’s initial thickness. The lower panels show correct and incorrect pairings side by side. Correct normalization makes every initial relative change zero, whereas the incorrect result gives initial values of 2% for B and −2% for C. A physical relationship reveals the error that the shape check cannot detect.

A useful check therefore examines shapes, units, and a few interpretable entries together. Verify B’s 13.73% at 20 min and the zero initial change in each row. Then reduce the table to three columns and confirm that normalization still follows specimens. Deliberately changing an array dimension helps expose mistakes hidden by equal axis lengths. Images, spectra, and three-dimensional trajectories introduce additional dimensions, making an explicit description of every axis even more valuable. A successful operation establishes structural compatibility; an identified numerator and denominator establish the intended calculation.

Calibration requires a sign convention. An instrument that reads 0.02 mm too high calls for subtracting 0.02 mm. A field defined as an additive correction could encode the same situation as −0.02 mm and be applied by addition. Field names, units, and the calculation should express the convention together. Sharing one offset across specimens also follows the stated calibration conditions. Separate measuring channels with different offsets require channel-specific values; a convenient broadcastable row does not establish that their physical corrections are identical.

## Array design explains views and copies

A longstanding need in numerical computing is to change how large data are accessed without moving every value on each operation. In their 2020 retrospective, NumPy’s authors describe multidimensional arrays and their operations as a foundation of scientific Python. One particularly useful design separates the numerical buffer from metadata describing shape, type, and access strides. Different selections or arrangements can then refer to the same stored values. The historical idea becomes concrete here: our measurement table can expose a smaller observation window while retaining the original numerical storage.

This design has a concrete research history. Numeric provided an early Python array object. Numarray later developed flexible indexing, memory mapping, and other capabilities for large astronomical images from the Hubble Space Telescope. NumPy emerged in 2005 by combining strengths of both projects. A researcher selecting a small image region needs to locate existing pixels efficiently and, when appropriate, create an independently processed result. The fifteen-value example reduces the same access and storage relationships to a scale where every selected value can be inspected.

![Original buffer diagram: selected cells share the same data; a slice keeps the original 40-byte row stride while the independent copy uses 24 bytes.](https://ml-biomat.com/static/tutorials/python-scientific/figures/91abb734c61b8323ee072b67.svg?v=91abb734c61b)

Figure 3Original buffer diagram: selected cells share the same data; a slice keeps the original 40-byte row stride while the independent copy uses 24 bytes.

The example stores fifteen contiguous float64 values, each occupying eight bytes. A row of five values occupies forty bytes. Moving one column to the right advances eight bytes; moving to the corresponding column of the next row advances forty. The slice `h[:,1:4]` starts eight bytes after the original buffer’s beginning and has shape (3,3), but its row stride remains forty bytes because the original row still contains two unselected columns. These storage distances are called strides. Their byte units distinguish them from the time intervals measured in minutes.

$$
o_{ij}=i\,s_0+j\,s_1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8180a7e0eb6f9b4d3cc44dc.svg) | Byte offset from this array’s starting point, bytes |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Zero-based row and column positions, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/c2e6885af79283f639bc340b.svg) | Byte strides for one step along axes 0 and 1, bytes |

The contiguous float64 array has strides (40,8) bytes. B at 20 min, position (1,2), lies 1×40+2×8=56 bytes from its start. The slice starts 8 bytes later but retains strides (40,8).

A basic slice shares numerical storage with its original array and is called a view. Picture a viewing frame placed over an existing worksheet: the cells visible through it still belong to that worksheet, so changing them changes the worksheet itself. The program takes a view of a separate demonstration array and changes the first selected value to 9.0. The original demonstration array’s A value at 10 min also becomes 9.0. This deliberately conspicuous value reveals the storage connection; the scientific calculations continue to use the unchanged thickness table.

Calling `.copy()` creates independent numerical storage, so editing the copy does not alter the original. Reading through advanced indexing also returns independent values. However, `h[:, selected] = values` assigns directly into selected positions of the original array and does alter it. “Advanced indexing returns a copy when reading” does not mean it can never be used to update original values. The function `np.shares_memory` checks whether two arrays share storage, which is more informative than observing that their variable names differ. Choose a view or copy according to whether changes should be shared or isolated.

The distinction becomes especially useful during exploratory analysis. A small selected window can be a convenient view when it is only being inspected. If a trial correction should leave the source measurements intact, make an explicit copy before editing. Naming that copy to describe its role makes the decision visible to a later reader. Conversely, intentionally updating a calibrated working array can use direct indexed assignment. The important choice concerns the ownership of changed values, rather than a general rule that every selection must be copied or that every copy is wasteful.

## A complete program makes each pairing inspectable

The complete program starts from the fixed thickness table and performs time selection, specimen-specific normalization, time-offset correction, a 21% specimen threshold, and a view-versus-copy editing demonstration. It deliberately attempts the incompatible (3,5) and (3,) operation and records its actual error message. It also constructs the executable but incorrectly paired (3,3) calculation. Placing both errors in one example makes it possible to distinguish what the interpreter can discover from what requires the measurement definition and a known numerical relationship.

### Complete program: selection, correction, broadcasting, and shared memory

Produces three figures and summary.json, captures an actual shape error, and independently checks elementwise results.

```
"""Select, calibrate, and normalize a constructed specimen-by-time array."""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch

TIME=np.array([0,10,20,40,60],dtype=float)
H=np.array([[1,1.08,1.14,1.18,1.2],[1.02,1.09,1.16,1.21,1.24],[.98,1.05,1.11,1.15,1.18]],dtype=np.float64)
DRIFT=np.array([0,.01,.02,.03,.04])
NAMES=['A','B','C'];COLORS=['#28648a','#b85336','#467a62']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('output'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    baseline=H[:,0:1]
    strain=H/baseline-1
    corrected=H-DRIFT[None,:]
    corrected_strain=corrected/corrected[:,0:1]-1
    selected=(TIME>=10)&(TIME<=40)
    selected_values=H[:,selected]
    qualifying=strain[:,-1]>=.21
    square=H[:,:3];wrong_square=square/H[:,0]-1;correct_square=square/baseline-1
    shared=H.copy();view=shared[:,1:4];isolated=shared[:,1:4].copy();advanced=shared[:,[1,2,3]]
    view[0,0]=9.0
    assert shared[0,1]==9 and isolated[0,0]==1.08 and advanced[0,0]==1.08
    independent=np.array([[float(H[i,j])/float(H[i,0])-1 for j in range(5)] for i in range(3)])
    assert np.allclose(strain,independent)
    assert np.allclose(corrected,[[float(H[i,j])-float(DRIFT[j]) for j in range(5)] for i in range(3)])
    assert qualifying.tolist()==[False,True,False]
    assert np.shares_memory(view,shared) and not np.shares_memory(isolated,shared) and not np.shares_memory(advanced,shared)
    try:H/H[:,0]
    except ValueError as error:incompatible=str(error)
    else:raise AssertionError('Shapes (3,5) and (3,) should be incompatible')
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={x.name for x in font_manager.fontManager.ttflist};family=next((x for x in ['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'] if x in available),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=170,bbox_inches='tight');plt.close(fig)
    def grid(ax,data,title,cols,unit):
        im=ax.imshow(data,cmap='cividis',vmin=H.min(),vmax=H.max(),aspect='auto')
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):ax.text(j,i,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=15,color='white' if data[i,j]<1.1 else '#172b36')
        ax.set(xticks=range(data.shape[1]),xticklabels=cols,yticks=range(3),yticklabels=NAMES,xlabel=unit,title=title)
        return im
    fig=plt.figure(figsize=(12.5,7.7),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,.9],width_ratios=[1.5,1]);ax=fig.add_subplot(gs[0,0]);im=grid(ax,H,tr('a  原数组 h：(3,5)','a  Original h: (3,5)'),TIME.astype(int),tr('时间 / min','Time / min'))
    ax.add_patch(Rectangle((.5,-.5),3,3,fill=False,edgecolor='#c6623b',lw=3));fig.colorbar(im,ax=ax,pad=.02).set_label(tr('厚度 / mm','Thickness / mm'))
    ax=fig.add_subplot(gs[0,1]);grid(ax,baseline,tr('b  每个样品的基准：(3,1)','b  Baseline per specimen: (3,1)'),[0],tr('时间 / min','Time / min'))
    ax=fig.add_subplot(gs[1,0]);grid(ax,selected_values,tr('c  h[:, 1:4] 对应10、20、40 min','c  h[:, 1:4] selects 10, 20, 40 min'),TIME[selected].astype(int),tr('时间 / min','Time / min'))
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.text(0,.9,'(3, 5) / (3, 1) → (3, 5)',fontsize=19,weight='bold');ax.text(0,.65,tr('末轴：5 与 1，可广播','Last axis: 5 and 1 are compatible'),fontsize=14);ax.text(0,.43,tr('前轴：3 与 3，一一配对','First axis: 3 and 3 match'),fontsize=14);ax.text(0,.15,tr('B，20 min：1.16 / 1.02 − 1 = 0.137255','B, 20 min: 1.16 / 1.02 − 1 = 0.137255'),fontsize=13)
    save(fig,'selection-broadcast')

    fig=plt.figure(figsize=(12.5,8.1),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.4,1]);ax=fig.add_subplot(gs[0,:])
    for i,c in enumerate(COLORS):
        ax.plot(TIME,strain[i]*100,'o-',color=c,lw=2,label=f'{NAMES[i]} '+tr('原始','raw'))
        ax.plot(TIME,corrected_strain[i]*100,'s--',color=c,lw=1.8,ms=5,label=f'{NAMES[i]} '+tr('校正后','corrected'))
    ax.set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('相对厚度变化 / %','Relative thickness change / %'),title=tr('a  各样品用自己的初始厚度归一化','a  Normalize each specimen by its own initial thickness'));ax.legend(ncol=3,fontsize=11);ax.grid(alpha=.15)
    for k,(data,title) in enumerate([(correct_square,tr('b  (3,3) / (3,1)：按样品','b  (3,3) / (3,1): by specimen')),(wrong_square,tr('c  (3,3) / (3,)：误按时间列','c  (3,3) / (3,): wrong time columns'))]):
        ax=fig.add_subplot(gs[1,k]);im=ax.imshow(data*100,cmap='RdBu_r',vmin=-3,vmax=18,aspect='auto')
        for i in range(3):
            for j in range(3):ax.text(j,i,f'{100*data[i,j]:.2f}%',ha='center',va='center',fontsize=14,color='white' if data[i,j]>.13 else '#172b36')
        ax.set(xticks=range(3),xticklabels=[0,10,20],yticks=range(3),yticklabels=NAMES,xlabel=tr('时间 / min','Time / min'),title=title)
    fig.colorbar(im,ax=fig.axes[1:3],shrink=.8,pad=.02).set_label(tr('相对变化 / %','Relative change / %'));save(fig,'normalized-response')

    fig=plt.figure(figsize=(12.5,8.3),layout='constrained');gs=fig.add_gridspec(3,1,height_ratios=[.3,.8,1.3]);ax=fig.add_subplot(gs[0]);ax.axis('off');ax.text(0,.7,tr('数组思想：一个数值缓冲区，多种访问方式','Array programming: one numerical buffer, multiple access patterns'),fontsize=18,weight='bold');ax.text(0,.05,tr('NumPy作者2020年回顾的核心结构：数值数据与形状、类型、步长分开组织。','Core structure in the authors’ 2020 retrospective: values plus shape, dtype, and strides.'),fontsize=12)
    ax=fig.add_subplot(gs[1]);ax.axis('off');ax.set_xlim(-.7,15.3);ax.set_ylim(-.4,2.8)
    for k,v in enumerate(H.ravel()):
        selected_cell=k%5 in [1,2,3];ax.add_patch(Rectangle((k,1),.94,.9,facecolor=COLORS[k//5],alpha=.25 if selected_cell else .08,edgecolor=COLORS[k//5]));ax.text(k+.47,1.45,f'{v:.2f}',ha='center',va='center',fontsize=11);ax.text(k+.47,.5,str(k*8),ha='center',fontsize=10)
    ax.text(0,2.35,tr('写入前的连续float64缓冲区：3 × 5 × 8 = 120字节','Before editing — contiguous float64 buffer: 3 × 5 × 8 = 120 bytes'),fontsize=14);ax.text(0,-.1,tr('数字下方：相对起点的字节偏移；每个数占8字节','Below: byte offsets from the buffer start; each value uses 8 bytes'),fontsize=12)
    ax=fig.add_subplot(gs[2]);ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,5.5)
    for x,title,data,stride,c in [(0,tr('视图写入9.0：原表同格一起改变','Write 9.0 through view: source changes'),view,40,COLORS[0]),(6.2,tr('提前复制的数据：仍然保留1.08','Earlier copy: still retains 1.08'),isolated,24,COLORS[2])]:
        ax.text(x+.05,5.05,title,fontsize=14,weight='bold');ax.text(x+.05,4.45,f'shape = (3,3); strides = ({stride},8) bytes',fontsize=12)
        for i in range(3):
            for j in range(3):
                px=x+.2+j*1.7;py=3.1-i*.85;changed=x==0 and i==0 and j==0;ax.add_patch(Rectangle((px,py),1.55,.7,facecolor=COLORS[1] if changed else c,alpha=.22 if changed else .08));ax.text(px+.775,py+.35,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=15,color=COLORS[1] if changed else '#172b36')
        ax.text(x+.05,.35,tr('共享存储；从原缓冲区偏移8字节','Shared storage; start offset 8 bytes') if x==0 else tr('独立存储：3 × 3 × 8 = 72字节','Independent storage: 3 × 3 × 8 = 72 bytes'),fontsize=12)
    save(fig,'memory-history')
    summary={'dataset':'Constructed specimen thickness table','shape':list(H.shape),'selected_times_min':TIME[selected].tolist(),'selected_values_mm':selected_values.tolist(),'baseline_shape':list(baseline.shape),'strain':strain.tolist(),'corrected_strain':corrected_strain.tolist(),'qualifying_at_21_percent':[NAMES[i] for i in np.flatnonzero(qualifying)],'wrong_square_strain':wrong_square.tolist(),'correct_square_strain':correct_square.tolist(),'incompatible_shape_error':incompatible,'view_copy':{'view_shares_memory':bool(np.shares_memory(view,shared)),'copy_shares_memory':bool(np.shares_memory(isolated,shared)),'advanced_shares_memory':bool(np.shares_memory(advanced,shared)),'edited_original_value':float(shared[0,1]),'isolated_value':float(isolated[0,0]),'original_strides_bytes':list(H.strides),'view_strides_bytes':list(view.strides),'copy_strides_bytes':list(isolated.strides)}}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'selected_times_min':summary['selected_times_min'],'last_raw_percent':(strain[:,-1]*100).tolist(),'last_corrected_percent':(corrected_strain[:,-1]*100).tolist(),'view_copy':summary['view_copy']},indent=2))

if __name__=='__main__':main()
```

The numerical summary retains selected times 10, 20, and 40 min, the full relative-change arrays, and memory-sharing checks. Original final changes are approximately 20.00%, 21.57%, and 20.41%; corrected values are approximately 16.00%, 17.65%, and 16.33%. A plain Python nested loop independently evaluates each specified operation and compares it with the array result. The loop is deliberately explicit: the outer loop selects a specimen, the inner loop selects a time, and the denominator can be traced to a particular row on every iteration.

When reading the plotting code, notice that heatmap columns and time-curve coordinates use different layouts. The heatmap gives each column equal display width and labels it with its actual time, helping the reader inspect indexing and pairing. The curves place observations at the numerical coordinates 0, 10, 20, 40, and 60, helping the reader inspect change over time. Both represent the same observations, but equal-width heatmap cells do not imply equally spaced sampling. The visual coordinate system should be interpreted through its labels and the question the panel addresses.

## Trace a cell through selection, correction, and editing

The interactive experiment connects the source table, selected window, and relative-change curves. Choosing start and stop columns displays both index positions and minutes. Changing calibration strength changes all specimens at a given time together. Switching between a view and a copy before editing one selected value shows whether the source table changes with it. Each adjustment reconstructs its state from the fixed teaching table, so reset returns the complete initial record. The baseline used for normalization is the source array’s initial column; editing that column through a view changes the baseline too.

### Experiment: trace an edit through a selection

Both endpoint positions are included. The increment changes the selected specimen’s first window value. A view changes the source; a copy preserves it. Blue, orange, and green identify A, B, and C.

[Figure: Source table and selected window](https://ml-biomat.com/tutorials/python-scientific/p08/en/#P08-grid)

[Figure: Relative changes over time](https://ml-biomat.com/tutorials/python-scientific/p08/en/#P08-plot)

First select 10 through 40 min and confirm that three columns are retained. Apply the supplied drift correction and observe B at 20 min change from approximately 13.73% to 11.76%. Then increase the first selected value by 0.10 mm and compare the source table under view and copy modes. These operations respectively test positional selection, directional pairing, and shared storage. Their relationships give compact array expressions an explanation that can be followed cell by cell. The next chapter uses repeated random sampling to explore how measurement results vary.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NumPy — Indexing on ndarrays](https://numpy.org/doc/2.4/user/basics.indexing.html)

   Indexing, selection shapes, and assignment

   BSD-3-Clause
2. [NumPy — Broadcasting](https://numpy.org/doc/2.4/user/basics.broadcasting.html)

   Trailing-axis compatibility and result size

   BSD-3-Clause
3. [NumPy — Copies and views](https://numpy.org/doc/2.4/user/basics.copies.html)

   Shared storage and independent copies

   BSD-3-Clause
4. [Harris et al. — Array Programming with NumPy (2020)](https://arxiv.org/html/2006.10256v1)

   Array-programming history and buffer/metadata design; original teaching figure

   CC BY 4.0 article; no original artwork reproduced
