# 一张科学图是怎样组成的

Source: https://ml-biomat.com/tutorials/python-scientific/p15/
Language: zh-CN

从六条标定记录出发，看清数据、绘图区和屏幕位置怎样对应，学会有目的地修改一张图。

## 从六条记录开始，决定这张图要回答什么

把一组实验记录画成图，最直接的用途是看见表格中不容易同时看清的关系。例如，浓度升高时仪器读数是否也升高？某一条记录是否偏离其余数据？两个样品的变化是否发生在相同区间？这些问题决定横轴、纵轴和标记各自承担什么任务。打开绘图库以后，先把问题写成一句具体的话，往往比先选颜色更能帮助我们把图画清楚。本章用六条浓度与吸光度记录，学习怎样从数据建立一张图，以及怎样有目的地改变它的坐标、文字和输出方式。

这里使用明确给定的教学数据。浓度依次为0、0.1、0.2、0.3、0.4、0.5 mmol/L，相应吸光度为0.032、0.111、0.205、0.296、0.389、0.481。每一对数值是一条记录；两个数组中位置相同的元素必须配在一起。mmol/L表示每升溶液含多少毫摩尔相应物质，是浓度单位。吸光度描述样品对光的衰减，通常作为无量纲数报告。这组教学数据模拟了随浓度增加而升高的仪器读数，便于逐一追踪六个点在图中的位置。

假如把这张表打印在纸上，我们能逐个读出数值，但要估计整体趋势，需要在多个单元格之间来回移动视线。散点图把每条记录变成一个位置：横向位置表示浓度，竖直位置表示吸光度。六个位置共享同一对坐标轴，大小关系因此可以被直接比较。这个过程也包含选择：点的颜色是否表示样品类别，点的面积是否表示另一个变量，两个点之间是否应该有连线，都需要有明确含义。

Matplotlib提供了组织这些选择的对象。你可以把一张图想成一张有明确分工的实验记录页：整页负责尺寸与导出，其中某个区域负责一套坐标，区域里再放置点、线、文字和图例。这种类比的作用是帮助我们理解“修改哪个对象”，实际程序中的对象关系比纸张更灵活。同一个Figure里可以放很多绘图区，每个绘图区可以展示不同变量，也可以共享同一条时间轴。

读完本章，你应当能找到一张图中的Figure、Axes、Axis和Artist，写出一个可保存的散点图，并解释一个看似矛盾的现象：数值没有变化，点在屏幕上的位置却改变了。理解这件事以后，缩放坐标、多面板比较、固定角落的标注和科学图的尺寸设置，都有了共同的出发点。

![浓度与吸光度散点图，旁列Figure、Axes、Axis、Artist的职责](https://ml-biomat.com/static/tutorials/python-scientific/figures/f7da92a9fb2daeaa00e2dc43.svg?v=f7da92a9fb2d)

图 1六条明确给定的教学标定记录，以及绘图对象各自负责的部分。红圈标出第4条记录。Figure、Axes和Axis本身也属于Artist体系；右侧列出职责，不表示四个对象逐层包含。

## 绘图库为何需要同时照顾探索和出版

Matplotlib的诞生与一类很具体的科研工作有关。原作者John D. Hunter在自己的回顾中写到，他处理脑电数据时，需要把数据分析做成可以交互的应用。随着任务涉及数据库、网络通信和更复杂的数据结构，他转向Python，同时希望拥有便于使用、能够嵌入图形界面、并能输出高质量科学图的二维绘图库。这段经历把一个常见需求说得很清楚：研究者在屏幕上查看数据和在文章中展示结果，往往使用的是同一批数字。

探索数据时，我们可能拖动时间范围、查看局部波动，或点击某段信号。整理结果时，我们希望固定坐标、标清单位，得到可以重新排版的图。把这两件事建立在同一组绘图对象上，就能保持数据与显示之间的联系。图中线条是什么、放在哪里、怎样表示颜色，先由对象描述；随后由输出后端把这些描述画到窗口、PNG像素图或SVG矢量图中。

下图用两条由正弦函数生成的教学信号，画出这种方法关系。波形用于解释多通道数据如何进入同一套绘图流程；它们的振幅使用任意单位。重要的是从左向右的对应关系：数据进入绘图对象，再进入不同输出媒介。改变输出媒介可以改变清晰度、交互能力或文件格式，数据记录仍然需要保持一致。

![多通道教学信号通过同一绘图对象连接交互窗口与矢量输出](https://ml-biomat.com/static/tutorials/python-scientific/figures/07cafdb17e9fe80e7efa8442.svg?v=07cafdb17e9f)

图 2Matplotlib所回应的一类历史需求：同一数据既需要交互探索，也需要形成可保存的科学图。左侧为本章用正弦函数生成的两条教学信号，振幅为任意单位；它们用于解释多通道数据工作流。

这种历史背景也解释了Matplotlib为什么同时保留方便的命令式入口和明确的对象操作。临时查看一条曲线时，几条简单命令很有效；图中有多个区域、多条曲线或很多标注时，保留对象名称能帮助我们准确定位。我们接下来采用显式的`fig`和`ax`，让每次设置都能回答“这条命令作用在什么地方”。

## Figure、Axes和Artist各自做什么

`Figure`表示完整的图形输出。它知道整张图的尺寸，包含一个或多个绘图区，并提供保存图形的方法。`Axes`表示其中一块承载数据坐标的绘图区。这个名称虽然以字母s结尾，一个`Axes`对象仍然可以指一块绘图区；不要把它误认为必然是一组对象。我们用`plt.subplots()`创建Figure和Axes，再把返回的两个对象分别放进变量`fig`与`ax`。

`Axis`则负责某一条坐标轴的刻度、刻度文字以及轴标签等内容。二维绘图区通常有横向和纵向两个Axis。一个数字该显示成0.10还是0.1，刻度间隔应该多大，轴上用什么单位表达，都与它们有关。`Axes`和`Axis`拼写相近，但职责不同：前者是一套数据的绘制空间，后者是组织坐标读数的对象。把两者分清，查阅文档时就容易知道自己正在寻找哪个接口。

`Artist`是可绘制对象的共同基类。Figure、Axes、Axis也属于这一体系，点、线和文字同样由相应Artist对象表示。它们并不是“Figure包含Axes、Axes包含Axis、Axis再包含全部点线”的四级直线关系。例如，散点通常由Axes中的一个`PathCollection`管理，折线通常对应`Line2D`，文字对应`Text`。初学时无须记住所有类名，但要知道一次绘图操作会创建一个可以继续修改的对象。

下面的最小程序保留了三个有用的名称。`fig`用于保存整张图；`ax`用于设置坐标、标签和范围；`points`表示刚创建的散点集合。变量并没有把图“复制”三次，它们只是让我们能够再次找到相应对象。点号后面的方法，例如`ax.scatter(...)`，可以理解为请这个绘图区执行一次具体操作；括号中的参数说明使用哪些数据、颜色和尺寸。

### 从对象开始创建一张图

concentration与absorbance相同位置的元素组成一条记录。fig保存整张图，ax保存绘图区，points保存散点集合。每一次设置都指向具体对象。

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

`fig, ax = plt.subplots(...)`使用的是序列解包：函数返回两个对象，左边两个名称依次接收它们。`figsize=(6.2, 4.2)`把图的宽、高设为6.2和4.2英寸；这决定最终页面中的物理尺寸关系。`layout="constrained"`要求布局引擎为标签和绘图区安排空间，减少轴标签挤出画布的情况。它仍然需要我们在输出后检查，尤其是长标题、多行单位和中文字体较宽时。

把样例放进脚本后，`fig.savefig(...)`会写出文件，`plt.show()`负责显示图形窗口；在Notebook里，单元格输出机制还可能自动显示Figure。看见图与保存文件是两个动作。为了在不同环境中得到明确输出，完整分析脚本应保留显式保存，并清楚说明文件放在哪里。这样即使运行环境没有弹出窗口，结果仍然能够被查看和复用。

## 每个视觉标记都应有可以说清的含义

浓度与吸光度分别来自一条记录的两个字段，因此首先用散点表示它们。散点的位置携带数值关系，标记大小保持一致，颜色也保持一致，这让读者把注意力放在坐标上。若再引入不同批次，可以用颜色或形状区分批次，并在图例中说明。若把点变大只是为了强调某条记录，最好再用轮廓或文字标注指出理由，避免读者误以为面积编码了质量、浓度或样本数。

连接两点的线也包含一个判断。按时间先后记录同一个样品的状态时，连线能帮助追踪变化顺序；六个独立配制浓度的标定点，则首先是六个离散观测位置。若要画出拟合关系，应当另行说明采用的模型和参数估计方法。直接把散点按数组中的顺序连起来，只说明连接顺序，不会自动成为经过验证的物理规律。后面的拟合章节会专门讨论怎样从散点建立模型。

标签应告诉读者“测量了什么”和“用什么单位”。本例写成“浓度 / mmol L⁻¹”和“吸光度 / 无量纲”，使横轴0.3与纵轴0.3的不同含义立即可见。单位中L⁻¹表示每升，与mmol/L是同一种写法。轴上的刻度通常会适当舍入以便阅读，而原始数组仍保留实际数值；把刻度写成两位小数，并不会把数据的计算精度提高到两位小数所暗示的测量精度。

网格线、颜色和留白可以帮助比较，但它们应当服从数据。淡网格让读者把一个点的高度对到数值刻度；过密、过黑的网格会与数据标记竞争。多组数据需要重复使用同一套颜色含义，例如一张图中蓝色一直表示同一批样本，红色一直表示当前选中的记录。红圈、红辅助线与下方数值说明指向同一条记录，就形成了跨视图的稳定联系。

显示范围同样是一项科学表达选择。保留零点可以帮助理解绝对量的比例；研究某个很窄的波动区间时，局部范围又能显露细节。选择范围时应把端点和刻度清楚标出，并根据问题决定是否同时提供全局与局部视图。将两个样本并排比较时，共用范围有利于直接比较幅值；若分别自动缩放，读者需要先读刻度，才能判断两条曲线看起来相似是否也意味着数值相近。

## 数据坐标怎样变成图中的位置

一条记录先有数据坐标，然后才有屏幕位置。对于线性横轴，浓度0.3 mmol/L在0到0.6 mmol/L的范围内正好位于中间；如果把范围改成0到1.2 mmol/L，这个数值就位于从左边数起四分之一处。可以把坐标轴想成一把可伸缩的尺：尺上覆盖的数值范围改变了，相同数值落在尺身上的比例也随之改变。

$$
u=\frac{x-x_{\min}}{x_{\max}-x_{\min}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4620fefc72ebf96810ce9f34.svg) | 点在绘图区中的水平相对位置，无量纲；0为左边，1为右边 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 点的横坐标；本例是浓度，单位mmol/L |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd27db42b5426d22e4e9954.svg) | 线性横轴的左右端点，与x同单位；要求右端点大于左端点 |

先减去左端点，把左边界移到零；再除以整个范围，得到占全宽的比例。浓度0.30 mmol/L在0–0.60 mmol/L的轴上给出u=0.50；范围扩大到0–1.20 mmol/L后u=0.25。浓度仍是0.30 mmol/L。此式描述线性轴且方向未反转；对数轴要先对数据与端点做相同的对数变换。

横向比例并不是新的实验变量。它只是描述点如何放进绘图区。公式分子是点距离左端点多远，分母是整个横轴跨度，两者单位相同，相除后单位消去。只要横轴保持线性、方向向右增加，这个比例就能直接用于定位。若把轴改成对数尺度，相等的视觉间距对应相等的倍数变化，定位前就要先做对数变换；零和负值也需要另行处理。

$$
v=\frac{y-y_{\min}}{y_{\max}-y_{\min}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 点在绘图区中的竖直相对位置，无量纲；0为底部，1为顶部 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 点的纵坐标；本例为无量纲吸光度 |
| ![Formula](https://ml-biomat.com/static/agent-math/547e3985a94f06060d90cef2.svg) | 线性纵轴的下、上端点，与y同单位；要求上端点大于下端点 |

纵向比例的计算与横向相同。吸光度0.296在0–0.55的纵轴上位于0.296/0.55≈0.5382处，即从底部向上约53.82%的高度。浏览器像素坐标通常从顶部向下增大，因此实现SVG时需要把这个向上的比例转换成向下的屏幕坐标；物理量本身没有反号。

本例选中第4条记录，即Python索引为3的元素。它的浓度是0.300 mmol/L，吸光度是0.296。原范围下，横向比例为0.50，竖直比例约为0.5382。把横轴上限改成1.20以后，横向比例变成0.25，竖直比例保持不变。下图由同一组数组分别绘制两个Axes；红圈和辅助线让对应关系可以直接比较。

![同一组散点在0到0.6与0到1.2浓度范围下并排比较](https://ml-biomat.com/static/tutorials/python-scientific/figures/ecb23ec11221b25a4e85581a.svg?v=ecb23ec11221)

图 3同一组数据在两个不同横轴范围中的位置。第4条记录始终是0.300 mmol/L、吸光度0.296；横轴范围扩大一倍后，它从全宽的50%处移到25%处。改变的是显示映射。

Matplotlib把这些转换封装在对象中。用数据坐标放置标注时，标注会随着数据范围一起移动；使用`ax.transAxes`时，位置由绘图区中的相对比例决定，例如靠近右上角的说明可以在缩放后仍然留在右上角。使用Figure坐标时，位置相对整张图；保存到屏幕或文件时，还会转换成实际像素或其他输出坐标。知道自己选择了哪一层坐标，就能解释为什么某些文字会跟着曲线走，而另外一些文字停留在角落。

这也说明“把图放大”和“扩大横轴范围”是不同操作。放大整张输出会让同样的坐标范围占更多像素；扩大数据范围则让同一个点占绘图区的比例缩小。前者涉及图的尺寸和输出分辨率，后者涉及数据显示映射。做组图时同时记录这两类设置，能够避免把不同尺寸或不同比例尺造成的视觉差异解释成样品差异。

## 在两个联动视图中检查自己的判断

下面的交互实验把数据选择与坐标范围分开。左图保持原始范围，右图接受你的设置，两个红圈始终对应同一条记录。你可以先预测点将朝哪个方向移动，再调整参数验证。例如，选中第4条记录，只把横轴上限从0.60改成1.20，点应向左移动到全宽的四分之一处；接着把纵轴上限改成1.10，点应向下移动到全高约26.91%的位置。

### 坐标范围改变以后，点去了哪里？

两幅图显示同样六条教学记录。先选中一条记录，再扩大右图的横轴或纵轴范围；观察红圈、辅助线和相对坐标一起怎样变化。左图保持原范围，作为对照。

[Figure: 原坐标范围中的数据](https://ml-biomat.com/tutorials/python-scientific/p15/#P15-reference)

[Figure: 当前坐标范围中的数据](https://ml-biomat.com/tutorials/python-scientific/p15/#P15-current)

浓度 / mmol L⁻¹**0.300**

吸光度 / 无量纲**0.296**

水平比例 u**0.5000**

竖直比例 v**0.5382**

```
ax.set(xlim=(0, 0.60), ylim=(0, 0.55))
```

观察时把三个层次联系起来：下方浓度与吸光度是数据本身；横向比例和竖直比例描述坐标映射；红圈所在的位置是这个映射的可视化结果。变化能够同时在数值、辅助线与点的位置上体现，才容易检查计算是否正确。如果数值变化了而点没有移动，就要检查绘图更新；如果点移动了而实验数值也被改掉，就要检查程序是否误把显示操作写进了数据数组。

选中浓度为零的第一条记录还可以检查边界。无论横轴上限如何改变，它都应留在左端点；但它的吸光度是0.032，因此不会落在原点。这个例子有助于区分“横坐标为零”和“两项数值都为零”。同理，把第6条记录选中后，它的浓度0.5始终大于第4条记录的0.3，即使两者在不同坐标范围下看起来可能落在相似位置。

交互中的命令提示对应`ax.set(xlim=..., ylim=...)`。把同样的端点写回Python程序，应得到相同的归一化位置。这样，网页里的探索可以连接到正式分析脚本：交互用于观察和检查，最后保留确定的参数、数据和绘图代码，使图能够再次生成。

## 运行完整程序，保留数据和图的对应关系

完整程序把六条教学记录定义在一个位置，再让三张图共同使用它们。这能避免手工复制数字时产生不一致。`plot_data`函数负责散点与共同轴标签，`save`函数负责把一张Figure写成SVG和PNG；历史方法图另用明确给定的正弦函数生成教学信号。把重复的绘图步骤放进函数后，改变字体或轴标签时不必在多个地方寻找同样的代码。

### 生成本章全部数据、图形与数值摘要

保存为main.py。运行python main.py --output output --language zh；英文使用--language en。脚本输出三组SVG/PNG、calibration.csv及summary.json；所有图都由同一组数组产生，依赖NumPy和Matplotlib。

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

运行完成后，`calibration.csv`保留实际用于绘图的两列数值，`summary.json`保留选中记录及其坐标比例，三组SVG/PNG则展示对象职责、方法关系和坐标变化。这样的输出组合使我们能够从图回到数值，再从数值回到程序。只有一张截图时，读者很难判断图中的点是否经过筛选、坐标是否被改动，或者哪条记录对应哪个标记。

本例实际计算得到：记录数为6，选中记录的浓度为0.3，吸光度为0.296，原横向比例为0.5，扩大范围后的横向比例为0.25，竖直比例约为0.5381818。你可以用前面的除法独立核对这些数值。程序还写入NumPy和Matplotlib的实际版本，方便以后在另一个环境中复现；版本信息属于运行结果说明，不应代替对数值与图形含义的检查。

若中文显示为方框，首先检查系统是否有可用的中文字形，并在字体列表中指定已有字体。字体设置影响文本呈现，不改变数据计算。脚本依次检查已安装的Noto Sans CJK SC、Noto Sans SC、Microsoft YaHei和SimHei，并保留DejaVu Sans处理拉丁文字；不同系统可使用其中已有的中文字体。修改字体后应再看一次实际输出，因为同一句文字在不同字体下占用的宽度可能不同，原来恰好合适的图例也可能需要重新安排。

## 把可读的结果保存下来

PNG用像素保存图像，适合浏览器预览和常见文档插图；SVG主要用路径、文字等矢量元素描述图形，适合缩放和进一步排版。图中若包含照片或栅格热图，SVG也可能嵌入像素图，因此“文件扩展名是SVG”并不意味着其中每一层都是矢量。选择格式时看最终用途：精确曲线和文字希望放大后保持清晰，真实显微图像则要保持原始像素与标定信息。

输出尺寸需要与阅读位置一起考虑。一张准备放在正文半栏中的图，若在制作时把文字设得很小，之后缩小就会难以阅读。提高PNG的dpi可以增加像素数量，却不会让过密的图例自动变得清楚。先安排合理的图幅、字体、面板数量和留白，再选择足够的输出分辨率，才能让图在实际页面中保持信息层次。

保存后，先检查六个点是否都能找到，再看轴标签和单位是否完整，红圈是否确实选中了第4条记录，左右两幅图的数据是否一致。随后把页面缩到实际阅读尺寸，查看最小刻度、中文标签和图注是否仍清楚。数值核对与视觉检查解决不同问题：前者保证坐标映射与数据对应，后者保证读者能从图中读出这种对应。

当这些关系清楚以后，绘图就不再是一串需要背诵的设置命令。你知道整张图由谁保存，绘图区在哪里规定数据范围，标记为何落在某个位置，说明文字又属于哪种坐标系统。下一章会在这套对象关系上组织多面板科学图，让不同视图共同支持一个更完整的问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P15.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Matplotlib Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html)

   Figure、Axes与面向对象绘图入口

   Matplotlib documentation license
2. [Matplotlib Transformations Tutorial](https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html)

   数据、Axes、Figure与显示坐标的关系

   Matplotlib documentation license
3. [John D. Hunter: Matplotlib History](https://matplotlib.org/stable/project/history.html)

   原作者关于脑电数据分析与绘图库需求的回顾

   Matplotlib documentation license
4. [Matplotlib Introduction to Artists](https://matplotlib.org/stable/users/explain/artists/artist_intro.html)

   容器、基础图形对象与共同Artist体系

   Matplotlib documentation license
5. [Matplotlib Figure.savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)

   输出格式、尺寸和保存选项

   Matplotlib documentation license
