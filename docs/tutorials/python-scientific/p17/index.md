# 分布、重复测量与误差线：让每个样品都说话

Source: https://ml-biomat.com/tutorials/python-scientific/p17/
Language: zh-CN

用Seaborn连接样品点、分布与统计区间，读懂标准差、标准误和独立样本数。

## 平均值相同的两批材料，使用感受也会相同吗

假设你要为一款软垫比较两批材料。每批取12个独立制作的样品，分别测量表示软硬程度的弹性模量。两批的平均模量恰好都是10 kPa，但第一批样品集中在8至12 kPa，第二批却从6到14 kPa都有。对使用者而言，后一批更可能出现明显偏软或偏硬的个体；对生产过程而言，它提示的是一致性问题。只画两根同样高的平均值柱子，这个差异就很难被看见。本节将用Seaborn把每个样品、整体分布与均值附近的误差线放到同一条解释路径中。

弹性模量可以先理解为材料抵抗变形的程度，本节用kPa作为单位，只研究这些数值怎样被统计和展示。我们会创建一组明确列出的教学数据，学习散点、直方图、累积分布和箱线图分别保留了哪些信息，再比较标准差、标准误与均值置信区间。完整程序还会保存每个样品的三次仪器读数，让你能追踪从72行原始记录到24个样品平均值，再到两个组均值的每一步。

Seaborn建立在Matplotlib之上，擅长把表格中的变量映射为坐标、颜色与分组，并完成相应的统计汇总。它的便利之处也意味着我们要先说清楚表格中每一行代表什么。样品、重复读数、批次和条件可能占据不同层级；图形函数接收到哪一层数据，图上的一个点、一个计数以及误差线中的样本数就会随之改变。

## 为什么统计学家坚持先看数据的样子

1973年，F. J. Anscombe在《Graphs in Statistical Analysis》中构造了几组数值摘要十分接近、散点结构却明显不同的数据。这个例子后来广为人知，因为它把一个容易忽略的问题变成了直观图像：平均值、方差或拟合直线可以浓缩信息，却不会保留数据的全部结构。图形分析让研究者看见弯曲关系、聚集区域与特殊观测，再决定使用什么统计方法。这里沿用这条思路，用自己的两组教学样品展示“平均值相同”与“分布相同”之间的距离。

![沿用Anscombe强调图形检查的思路，用本节两组各12个样品的教学数据比较均值柱与完整样品点。每个点是一个样品的三次读数平均值；蜂群的横向位移只用于避免点重叠。](https://ml-biomat.com/static/tutorials/python-scientific/figures/58c274020dd0e2fef89ebc09.svg?v=58c274020dd0)

图 1沿用Anscombe强调图形检查的思路，用本节两组各12个样品的教学数据比较均值柱与完整样品点。每个点是一个样品的三次读数平均值；蜂群的横向位移只用于避免点重叠。

左图只保留两个均值，右图给每个独立样品一个点。A组在中心附近堆得更密，B组占据更宽的范围，两个组的中心仍然对齐。蜂群图会横向挪开重叠的点，使相同或相近的模量也能分别看见；横向小位移表示排布空间，纵坐标才是模量。因而数一数点，就能核对每组有12个样品。这种图适合较小样本，能让读者同时查看数值范围与样本数量。

计算工具逐渐把这类统计阅读习惯变成了直接可执行的操作。Michael Waskom在2021年介绍Seaborn的论文中强调了表格数据与统计图形之间的联系：用户指定哪个变量放到哪个位置，库负责把分组与图形元素组织起来。对于本例，把`group`映射到组别、把`modulus_kPa`映射到纵轴，就能让同一份样品表在不同统计视图中反复使用。每次换图形时，数据的身份仍然可以保留。

## 先确定一个点究竟代表什么

A组的12个样品平均值依次为8、8、9、9、10、10、10、10、11、11、12、12 kPa，B组为6、6、7、8、9、10、10、11、12、13、14、14 kPa。每个样品再配三次读数，分别比其平均值少0.2、相同、多0.2 kPa。这些重复偏移是预先规定的教学规则，便于核对聚合过程。每一行原始记录包含组别、样品编号、重复编号和模量，四个字段一起说明读数来自哪里。

例如A01的三次读数为7.8、8.0、8.2 kPa，平均后得到该样品的8.0 kPa。对全部样品重复这个操作，72条仪器记录会变成24条样品记录。假设独立制作过程发生在样品层面，那么用于比较组间材料差异的独立单位就是样品。同一样品上的读数共享材料结构，重复测量能帮助稳定这个样品的读数，却不会把它变成三个不同的材料个体。把这些层级写在表格里，比计算之后再回忆实验设计可靠得多。

代码使用`groupby(['group','specimen'])`，先在组别与样品编号的组合内求平均。两列一起作为分组键，可以保留完整身份。随后，Seaborn接收这张每行一个样品的表，`x='group'`选择组别列，`y='modulus_kPa'`选择模量列。这里传入的是列名，不是把字符串当成一个物理数值。`hue='group'`再让颜色跟随组别；明确指定颜色字典，可以让A、B在整篇图中始终保持同一种颜色。

如果以后一个样品的重复次数不同，直接把所有原始读数混在一起求平均，会让重复次数多的样品获得更大权重。先求每个样品的平均值，再对样品平均，可以让每个独立样品贡献相同权重。本例每个样品恰好都测三次，所以两种组均值数值相同；它们在标准误计算中仍会产生不同结果，因为用于表示独立信息量的样本数不同。

## 从逐个样品走向分布：分箱、累计和排序

当样品更多时，可以把模量轴分成相邻区间，数每个区间中有多少样品，得到直方图。它像把不同长度的螺丝放进标有尺寸范围的盒子，盒子里的数量形成柱高。箱宽较小时，细节更多，也更容易出现由有限样本造成的起伏；箱宽较大时，整体趋势更平滑，但不同区域可能被合在一起。因此比较A、B时，应让两组使用相同的箱边界。否则某个数值落在哪一箱会随组别变化，柱高就难以直接对照。

![同一份24样品表的四种视图：两种箱宽、经验累积分布与箱线摘要叠加全部样品。直方图计数使用共同边界；箱线图采用1.5倍四分位间距须线。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f94e46c7488ec4137b186ab0.svg?v=f94e46c7488e)

图 2同一份24样品表的四种视图：两种箱宽、经验累积分布与箱线摘要叠加全部样品。直方图计数使用共同边界；箱线图采用1.5倍四分位间距须线。

图中上排只改变箱宽，原始样品没有增减。每个区间采用左闭右开的计数约定，最后一个区间包含右端点；本例把边界放在半整数上，使整数样品值不落在边界。你可以先找到A组的10 kPa，它有四个样品，窄箱视图因此出现一个较高的中心计数。宽箱把相邻数值合在一起，突出的是较大范围的集中程度。柱高表示样品数，只有改为密度表示时，才需要额外除以总样本数与箱宽，并以柱子的面积表示比例。

经验累积分布函数不需要选择箱宽。沿横轴从小到大走，每遇到一个样品，就把累计比例增加1/12；遇到相同值时，一次增加多个样品所占的比例。A组在10 kPa处已经累计到8/12，也就是约66.7%，B组在该位置累计到7/12，即约58.3%。这个视图适合回答“有多少样品不超过某个阈值”，也能直接比较某个比例对应的数值位置。阶梯来自有限个样品，是数据结构的自然结果。

箱线图进一步压缩排序后的数据，用中位数标出中间位置，用第一、第三四分位数围住中间一半数值。常用须线延伸到四分位间距1.5倍规则内最远的实际观测，超出者单独标记。这个标记表示相对分布较远的位置，需要结合记录检查其原因。少量样品时，把原始点叠加上去尤其有用：读者可以看到箱子由哪些值形成，也能发现同一个箱线摘要背后可能存在的不同形状。分位数在有限样本间需要插值，本例采用NumPy默认的线性分位数约定。

## 标准差、标准误与置信区间在回答不同问题

平均值描述数据的中心。为了表示样品围绕中心分散多远，可以计算每个值与均值的差，平方后求和，再除以自由度并开平方，得到样本标准差SD。平方使正负偏差不会相互抵消，开平方把单位从kPa²恢复成kPa。分母中的n−1与使用样本均值有关：偏差相加必须为零，最后一个偏差由其余偏差确定，因此只有n−1个可以自由变化。

$$
\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar x)^2}{n-1}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | 第i个独立样品的三次读数平均模量，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样品序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 独立样品数，本节每组12，无量纲且大于1 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | 所选组的样品均值，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 样本标准差SD，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 把指定范围内各样品的量相加 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bcc38017e1856dc949d86bd.svg) | 平方根，把平方单位恢复为原单位 |

A组总和120 kPa，除以12得到10 kPa。两个8和两个12贡献的偏差平方和为16 kPa²，两个9和两个11再贡献4 kPa²，其余为0。因此s=√(20/11)≈1.34840 kPa。用样本均值代替未知总体均值会消耗一个自由度，故估计总体方差时使用n−1。

A组的偏差平方和为20 kPa²，B组为92 kPa²。两组都包含12个独立样品，所以标准差分别约为1.348和2.892 kPa。这与散点图中B组较宽的分布相一致。若研究问题是生产出的个体有多大差异，应当重点查看原始分布与SD。增加样品数会让我们更稳定地认识这种分布，但不会因为除数变大就把实际材料个体变得更一致。

标准误SEM关注另一个对象：如果按相同方法重复抽取一批独立样品，每次算一个均值，这些均值会有多大波动。独立且来自同一分布的样品越多，均值通常越稳定，于是标准差还要除以样本数的平方根。对于A组，SEM约为0.389 kPa，比SD小。这条误差线描述均值估计的精度，不能把它解释成大多数个体的分布范围。

$$
\mathrm{SEM}=s/\sqrt n
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd3305e34ff527725a7a82ea.svg) | 独立样品均值的估计标准误，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 独立样品值的样本标准差，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 独立、同分布样品数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0639947db355311e236c3a6.svg) | 样品数的平方根，无量纲 |

独立同分布数值的方差相加，平均时又除以n²，因此均值的方差是个体方差的1/n，标准差是其1/√n。A组SEM=√(20/11)/√12≈0.389249 kPa。把同一样品的重复读数当成独立样品，会改变这里的独立性条件。

95%均值置信区间在SEM的基础上再乘以一个系数。下面采用Student t区间，系数取决于独立样本数；12个样品对应11个自由度，系数约为2.201。这个计算在独立、同分布的正态样本假设下具有精确的覆盖率解释，在样本足够多且均值近似正态时也常用于近似分析。本节使用明确的教学数值演示区间如何形成。对于偏斜、小样本或分层实验，需要先检查分布与设计，再选择相应的区间方法。

$$
\mathrm{CI}_{95\%}=\left[\bar x-t_{0.975,n-1}\frac{s}{\sqrt n},\;\bar x+t_{0.975,n-1}\frac{s}{\sqrt n}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/65f4735a16f924a7e46e8319.svg) | 总体均值的95% Student t置信区间，端点单位kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | 样品均值，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 样本标准差，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 独立样品数，本节12，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/22ba3759c09a7ea30a432312.svg) | 自由度n−1的标准t分布累计概率0.975处的分位数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/6cfef8857b6fd57926324bb0.svg) | 双侧95%区间上尾留下0.025，累计概率为0.975，无量纲 |

每尾各留2.5%，中间合计95%，所以使用0.975分位数。独立正态样本下该构造具有精确覆盖率。n=12时系数约2.200985，A组半宽为2.200985×0.389249≈0.856732 kPa；用均值10减去和加上半宽，得到[9.143268,10.856732] kPa。

“95%”描述的是重复采样时按照同一规则构造的区间覆盖总体均值的长期比例。已经算出的这个区间是固定的，而未知总体均值也是固定的；区间的宽度表示当前方法下均值估计的不确定程度。图注写出“均值±SD”“均值±SEM”或“95% t区间”，读者才能知道误差线围绕哪个对象展开。只写“误差线”会把几个不同问题留给读者猜测。

## 把读数当成样品，为什么误差线会变窄

现在回到每个样品的三次读数。A组有12个独立样品、36条仪器记录。如果把36条记录直接交给标准误函数，它会按36个独立输入进行计算，得到约0.220 kPa；先按样品求平均再计算，结果是约0.389 kPa。均值仍然都是10 kPa，误差线却缩短了。程序没有自动识别记录之间共享一个样品，只是忠实执行了所给数组对应的计算。

![左图比较均值±SD、均值±SEM与95% Student t均值区间，均按每组12个独立样品计算。右图显示直接把36条重复读数视为独立输入时，计算出的SEM如何改变。](https://ml-biomat.com/static/tutorials/python-scientific/figures/cf171d8f4a58446357a3a195.svg?v=cf171d8f4a58)

图 3左图比较均值±SD、均值±SEM与95% Student t均值区间，均按每组12个独立样品计算。右图显示直接把36条重复读数视为独立输入时，计算出的SEM如何改变。

可以把同一样品的重复读数想成对同一件物品拍三张照片。三张照片有助于看清这件物品，却没有增加物品的种类与个数。统计上的独立单位来自制作、抽样或随机分配过程。对于细胞、动物、培养皿、批次与技术重复，这个单位需要根据实验设计确定；同一容器里的多个测量点也可能共享环境。把这些层级保存为列，后续才能按合适单位聚合，或使用保留层级关系的模型。

本例用样品平均值进入组间比较，使“每个独立样品贡献一次”清楚可见。若研究目标还包括仪器自身的重复性，可以另画同一样品内部的偏差，并报告重复测量的分散程度。组间材料差异与仪器重复性都值得研究，只是它们使用不同层级的变异。图中把两个SEM结果并排展示，是为了让这种分母选择对结果的影响直接呈现。

## 完整程序：让分组、统计量和图形共享同一份表

程序先从固定的24个样品值生成72条读数，然后保存原始表与样品表。Seaborn的`barplot`按组计算均值，`swarmplot`排布每个样品，`histplot`统计箱内数量，`ecdfplot`绘制累计比例，`boxplot`形成排序摘要。每个函数都显式接收同一个样品表与列名。它们返回或使用Matplotlib的Axes对象，因此仍能通过`set`修改单位、标题和刻度，把统计图纳入上一节的组图方式。

代码为均值柱设置`errorbar=None`，使第一幅历史概念图专注于“均值隐藏分布”这一问题。第三幅图的SD、SEM和t区间由NumPy、SciPy明确算出，再用Matplotlib画横向误差线。Seaborn也提供`errorbar='sd'`、`'se'`和置信区间等选项；默认的置信区间可能通过bootstrap获得，与这里的t区间是不同计算。选项名方便使用，图注仍需要交代对应的统计方法与独立单位。

### 完整Python：独立样品、分布与三种区间

生成明确规定的教学读数，以pandas按样品聚合、Seaborn绘制分布、NumPy和SciPy计算带单位的统计摘要。

```
"""Show distributions and distinguish specimens from repeated instrument readings."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
import seaborn as sns

VALUES={'A':[8,8,9,9,10,10,10,10,11,11,12,12],
        'B':[6,6,7,8,9,10,10,11,12,13,14,14]}
COLORS={'A':'#28658c','B':'#b64a35'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    sns.set_theme(style='whitegrid',font='DejaVu Sans',font_scale=1.1)
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'svg.fonttype':'none',
                        'axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.18})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    readings=pd.DataFrame([{'group':group,'specimen':f'{group}{i+1:02}',
        'repeat':j+1,'modulus_kPa':value+offset} for group,values in VALUES.items()
        for i,value in enumerate(values) for j,offset in enumerate([-.2,0,.2])])
    specimens=readings.groupby(['group','specimen'],as_index=False)['modulus_kPa'].mean()
    readings.to_csv(args.output/'readings.csv',index=False);specimens.to_csv(args.output/'specimens.csv',index=False)
    summary={'versions':{'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,
                         'seaborn':sns.__version__,'matplotlib':matplotlib.__version__},'groups':{}}
    for group in VALUES:
        v=specimens.loc[specimens.group==group,'modulus_kPa'].to_numpy();raw=readings.loc[readings.group==group,'modulus_kPa'].to_numpy()
        n=len(v);mean=float(v.mean());sd=float(v.std(ddof=1));se=float(stats.sem(v));critical=float(stats.t.ppf(.975,n-1))
        summary['groups'][group]={'n_specimens':n,'n_readings':len(raw),'mean_kPa':mean,'sd_kPa':sd,
             'sem_kPa':se,'t_critical':critical,'ci95_kPa':[mean-critical*se,mean+critical*se],
             'naive_reading_sem_kPa':float(stats.sem(raw)),'sum_squared_deviations_kPa2':float(np.sum((v-mean)**2)),
             'quantiles_kPa':np.quantile(v,[.25,.5,.75]).tolist(),
             'count_at_or_below_10':int(np.count_nonzero(v<=10))}
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    sns.barplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,errorbar=None,legend=False,ax=axes[0])
    axes[0].set(title=tr('A  均值相同：两根柱子都是10','A  Same mean: both bars equal 10'),xlabel=tr('组别','Group'),ylabel=tr('平均模量 / kPa','Mean modulus / kPa'),ylim=(0,15))
    sns.swarmplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,legend=False,size=6,ax=axes[1])
    axes[1].axhline(10,color='#71808b',ls='--',lw=1)
    axes[1].set(title=tr('B  保留样品：分布范围不同','B  Keep specimens: different distributions'),xlabel=tr('组别，每组12个样品','Group, 12 specimens each'),ylabel=tr('样品平均模量 / kPa','Specimen-mean modulus / kPa'),ylim=(0,15))
    fig.suptitle(tr('Anscombe 1973：看图能发现数值摘要隐藏的结构','Anscombe 1973: graphs reveal structure beyond summaries'),fontsize=15)
    save(fig,'history')
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for ax,width in zip(axes[0],[1,4]):
        sns.histplot(data=specimens,x='modulus_kPa',hue='group',palette=COLORS,
            bins=np.arange(5.5,17.5+width,width),element='step',fill=False,common_bins=True,stat='count',ax=ax)
        ax.set(title=tr(f'箱宽 {width} kPa',f'Bin width {width} kPa'),xlabel=tr('模量 / kPa','Modulus / kPa'),ylabel=tr('样品数','Specimen count'),xlim=(5,18))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.get_legend().set_title(tr('组别','Group'))
    sns.ecdfplot(data=specimens,x='modulus_kPa',hue='group',palette=COLORS,ax=axes[1,0])
    axes[1,0].get_legend().set_title(tr('组别','Group'))
    axes[1,0].set(title=tr('经验累积分布：逐个累计样品','Empirical CDF: accumulate specimens'),xlabel=tr('模量 / kPa','Modulus / kPa'),ylabel=tr('不超过横轴值的比例','Fraction at or below x'),xlim=(5,16))
    sns.boxplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,legend=False,width=.45,showfliers=False,ax=axes[1,1])
    sns.swarmplot(data=specimens,x='group',y='modulus_kPa',color='#20313e',size=4,ax=axes[1,1])
    axes[1,1].set(title=tr('箱线图与全部样品','Box summaries with every specimen'),xlabel=tr('组别','Group'),ylabel=tr('模量 / kPa','Modulus / kPa'))
    save(fig,'distributions')
    fig,axes=plt.subplots(1,2,figsize=(12,6),layout='constrained')
    for j,group in enumerate(VALUES):
        d=summary['groups'][group]
        for i,(label,half) in enumerate([('SD',d['sd_kPa']),('SEM',d['sem_kPa']),('95% t CI',d['ci95_kPa'][1]-10)]):
            axes[0].errorbar(10,i+j*.18,xerr=half,fmt='o',capsize=5,color=COLORS[group],label=group if i==0 else None)
        axes[1].plot([0,1],[d['sem_kPa'],d['naive_reading_sem_kPa']],'o-',color=COLORS[group],lw=2,label=group)
    axes[0].set(yticks=[.09,1.09,2.09],yticklabels=[tr('均值 ± SD','mean ± SD'),tr('均值 ± SEM','mean ± SEM'),'95% t CI'],
        xlabel=tr('模量 / kPa','Modulus / kPa'),title=tr('同一均值，三种区间含义','One mean, three interval meanings'),xlim=(6,14));axes[0].legend(frameon=False)
    axes[1].set(xticks=[0,1],xticklabels=[tr('12个独立样品','12 independent\nspecimens'),tr('36条读数\n直接计算','Treat 36 readings\nas independent')],
        ylabel=tr('计算得到的SEM / kPa','Calculated SEM / kPa'),title=tr('独立单位决定SEM的分母','Independent units determine the SEM denominator'),ylim=(0,1))
    axes[1].tick_params(axis='x',labelsize=11);axes[1].legend(frameon=False)
    save(fig,'intervals')
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

运行结果中，A、B两组均值都为10.0 kPa，标准差约为1.3484与2.8920 kPa，SEM约为0.38925与0.83485 kPa。95% t区间分别约为[9.1433,10.8567]与[8.1625,11.8375] kPa。原始读数表有72行，样品表有24行，每组各12个样品。把这些数量与图中的点数、计数柱和区间端点对应起来，就能从数值和图形两条路径核对计算。

改用自己的数据时，先检查哪些列标识独立单位，再核对唯一的样品数，随后选择绘图选项。缺少一次读数，会让某个样品的平均值依赖更少重复；缺少一个样品，则改变独立样本数。把这两种情况分开，后续统计更容易解释。原始CSV与样品CSV保留了转换前后的记录，而JSON摘要把关键数值单独列出，方便用绘图库之外的方法核对。

## 联动实验：改变展示，保留样品身份

下面可以选择组别、直方图箱宽，以及均值附近显示SD、SEM还是95% t区间。原始样品点、直方图和累计分布会一起更新；区间始终由所选组的12个独立样品计算。先比较A、B，注意均值不动而分布宽度发生变化。再固定A组，把SD切换为SEM：样品点仍在原处，变短的是均值附近的区间。

### 样品、分布与区间联动

全部统计基于每组12个独立样品的平均读数。深色点位于阈值及其以下；直方图箱宽与区间类型分别控制分布展示和均值摘要。

[Figure: 全部样品及均值区间](https://ml-biomat.com/tutorials/python-scientific/p17/#P17-points)

[Figure: 共同边界的直方图](https://ml-biomat.com/tutorials/python-scientific/p17/#P17-hist)

[Figure: 经验累积分布及阈值比例](https://ml-biomat.com/tutorials/python-scientific/p17/#P17-cdf)

把箱宽从1改为4 kPa后，直方图柱子会重新组合，而累计分布保持不变。这样可以把“数据发生改变”与“展示方式改变”分开观察。移动阈值时，累计分布上的标记与阈值以下的计数同步变化；例如A组在10 kPa处包含8个样品，B组包含7个。这个数值既能从样品点中逐个数出，也能从累计比例乘以12得到。

实验在切换视图时保留全部样品，统计量始终对应同一组观测。若在实际分析中筛选数据，可以同时显示筛选规则、剩余样本数与被排除数据的位置。图的交互功能越丰富，越需要让读者追踪当前显示的是哪一组观测，以及统计量由哪些观测计算而来。

## 让图形选择跟随研究问题

比较个体一致性时，先看原始点、分布与SD；比较均值估计的精度时，再看SEM或合适的置信区间；判断有多少样品满足阈值时，累计分布尤其直接。这几种视图可以互相补充。少量观测的细节值得保留，大样本则需要通过分箱、密度或分位数压缩展示。平滑密度曲线会加入带宽选择，窄带宽产生更多起伏，宽带宽合并细节，解释时应把这种估计步骤考虑进去。

两组均值区间是否重叠，也不能直接替代一个设计明确的组间比较。检验均值差异需要计算“差”的不确定性，并考虑两组独立、配对或分层的关系。对同一个样品前后测量的实验，逐对差值通常比把两列各自画成一根均值柱保留更多信息。后续统计章节会继续讨论采样、区间和比较规则；在进入这些计算之前，本节的样品身份与分布检查已经为选择方法提供了基础。

准备交付一幅统计图时，可以从读者需要知道的三个问题组织图注：一个点代表什么，每组包含多少独立单位，误差线使用什么定义。再加上量名、单位和必要的分组条件，图中的数字就有了完整语境。代码会帮助你反复执行同样的统计与绘图，而对实验单位和研究问题的明确理解，决定了这些操作最终表达的是什么。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P17.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Seaborn: visualizing distributions](https://seaborn.pydata.org/tutorial/distributions.html)

   分箱、平滑密度与经验累积分布的选择

   BSD-3-Clause; seaborn LICENSE.md
2. [Seaborn: statistical estimation and error bars](https://seaborn.pydata.org/tutorial/error_bars.html)

   区别样本分散程度与估计的不确定性

   BSD-3-Clause
3. [Waskom (2021), seaborn: statistical data visualization](https://joss.theoj.org/papers/10.21105/joss.03021)

   数据表与统计图形接口的原作者介绍

   CC BY4.0 paper, BSD3 software
4. [Anscombe (1973), Graphs in Statistical Analysis](https://www.tandfonline.com/doi/abs/10.1080/00031305.1973.10478966)

   数值摘要与图形结构之间关系的原始论文

   Historical attribution; no reproduced figures or passages
5. [SciPy: standard error of the mean](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sem.html)

   标准误的自由度与输入轴

   SciPy BSD3
6. [SciPy: Student t distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)

   通过分位数构造Student t均值区间

   SciPy BSD3
