# 从清楚的曲线到完整的科学组图

Source: https://ml-biomat.com/tutorials/python-scientific/p16/
Language: zh-CN

用相同数据组织总览、线性尺度与对数尺度，让面板之间的比较有准确的数量依据。

## 一张组图怎样让读者看清整个过程

假设有四个装着可溶性物质的小容器，起初都含有4 mg物质，随后以不同快慢被带走。你每隔一段时间记录剩余质量，已经能用Matplotlib画出四条曲线。接下来的问题更接近实际写报告时的困难：四条曲线应当放在同一坐标系里，还是分开画？末期只剩很少的物质，怎样看清它们仍在以不同速度减少？如果同时给出一幅颜色图，读者怎样知道颜色与曲线讲的是同一组数值？这些决定直接影响读者从图中得到什么结论。

本节用一个计算规则明确的教学过程，练习把总览、细节和数量关系组织成一张科学组图。这里的“组图”是由几个互相配合的面板组成的完整图形：总览回答整个参数范围发生了什么，细节回答某一条曲线如何变化，辅助面板说明尺度转换产生的效果。它很像一张旅行地图与几张街区放大图的组合。地图负责方向，放大图负责细节，比例尺负责把图上的距离与真实距离联系起来；这三部分各有工作，放在一起才容易读懂。

本节会用到数组、函数和上一节介绍的Figure、Axes对象。指数与对数会从实际数字开始解释。完成之后，你可以为多组时间曲线安排共享坐标，为一组热图指定共同颜色尺度，并导出能够放入文档的矢量图。组图的设计从科学问题开始：先确定哪些量需要直接比较，再决定面板位置、刻度、颜色和文字，而不是先填满几个空白格子。

## 从一列数字到共同坐标，比较方式发生了什么变化

William Playfair在1786年的《商业与政治图集》中，用图表展示贸易与公共账目。今天看来，把数量沿着时间轴排列是很自然的做法，当时这种表达却让大量数字获得了新的阅读方式。表格适合查出某一年某一项的确切数值；共同坐标则让增长、下降、交叉与差距直接出现在眼前。Wellcome Collection保存的原版目录记录了这部图集及其年代。下图用本节的教学数据重画这种从表格到共同坐标的变化，便于把历史中的表达方法与正在学习的Python联系起来。

![从表格读取数值，到用共同坐标比较走势：以本节模型数据重画Playfair图表传统中的比较思路。点与表格条目一一对应，连线用于连接这些采样位置；图中数值为本节教学模型。](https://ml-biomat.com/static/tutorials/python-scientific/figures/038631407d46c5469f299bf6.svg?v=038631407d46)

图 1从表格读取数值，到用共同坐标比较走势：以本节模型数据重画Playfair图表传统中的比较思路。点与表格条目一一对应，连线用于连接这些采样位置；图中数值为本节教学模型。

观察左侧表格，你可以准确读到某个时间的质量，但要比较两种过程的快慢，需要在心中记住几行数字并做减法。右侧把同一行的两个值放到同一个纵向尺度上，差距就表现为两个点的高度差。共同尺度承担了部分心算工作。如果两幅小图分别自动缩放纵轴，两条走势相似的曲线可能看起来同样高，读者又必须回头核对刻度。设计科学图时，共享尺度并不是一种统一外观的习惯，而是在帮助读者完成具体的比较。

图表也改变了我们提问的顺序。先看整体，可以发现两个过程是否在早期就分开，随后再查某个时刻的数值。用代码生成图，让这种阅读方式可以跟随数据更新：修改一条计算规则或加入一组条件，图上的线、颜色和图例都能同步改变。保留数据与绘图指令之间的关系，是科学图能够反复使用的基础。

## 建立一组能够逐项核对的曲线

为了把注意力放在绘图上，我们规定一个简单的减少过程：在相同时间长度内，总是带走当前剩余物质的相同比例。一个容器最初剩得多，单位时间带走的量也较多；后来剩得少，带走的绝对量跟着减少。可以把它想成反复取走充分混匀液体的一小部分。把这样的过程连续化，会得到指数衰减曲线。它为本节提供平滑、始终为正且能手算关键点的数据。

$$
m(t)=m_0\exp(-t/\tau)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | 时刻t的剩余质量，mg |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 初始质量，本节为4 mg |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过时间，min |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 时间常数，本节取1、2、4、8 min |
| ![Formula](https://ml-biomat.com/static/agent-math/d7bdddb2b2f38a1d246c4b23.svg) | 自然指数函数，输入与输出均为无量纲数 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 指数函数的通用自变量，此处为−t/τ，无量纲 |

同一时长对应相同剩余比例，因此连续相乘形成指数。t与τ都用min，二者相除使指数无单位。t=0时exp(0)=1，质量为4 mg；t=τ=4 min时exp(−1)≈0.367879，质量为4×0.367879≈1.47152 mg。

时间常数τ控制曲线横向展开的程度。τ=1 min时，经过1 min剩下初始值的大约36.8%；τ=8 min时，需要8 min才走到同一比例。这里没有为四条曲线分别改变初始质量，因此它们在时间零点都从4 mg出发。数组中的每一行保存一个时间常数下的完整过程，每一列对应同一个时刻。明确这两个方向，后面才能正确地把“时间”放在横轴，把“不同条件”放在热图的各行。

代码把0到12 min分成241个时刻，用广播一次算出形状为4×241的数组。密集网格来自公式计算；它的每个值都是模型值。若换成真实实验，应保留实际采样时刻，并用点标出观测位置。两种数据都可以画成线，但线的含义不同：这里表示已知函数在时刻之间的连续变化，实验连线通常只是帮助追踪相邻记录。

还可以找一个很容易比较的共同位置：剩余质量降到2 mg，也就是初始量的一半。把2代入模型后，可以得到半衰时间随τ成正比。在线性曲线面板上标出这几个点，读者能把公式里的比例关系与实际横向距离对应起来。对τ=4 min，半衰时间约为2.773 min；它与时间常数4 min表示的是两个不同的比例位置。

$$
t_{1/2}=\tau\ln 2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | 质量降至初值一半所需时间，min |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 指数衰减的时间常数，min |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | 自然对数函数，是exp的反函数；其自变量为无量纲数 |
| ![Formula](https://ml-biomat.com/static/agent-math/f5f3224583db57b9cfe323c8.svg) | 初始质量与半质量之比，无量纲 |

令m(t)/m₀=1/2，取自然对数后得到−t/τ=−ln2。乘以−τ可得本式。τ=4 min时，t₁/₂=4×0.693147≈2.77259 min，代回模型得到2 mg。

## 总览给范围，细节给读数

下面的组图把上方留给总览，下方留给两种曲线视图。总览中的横轴是时间，四行分别对应四个时间常数，颜色表示剩余质量。扫过整幅热图，可以快速看出哪一行保留较多物质，以及差异在什么时候出现。下方左图保留质量的普通线性刻度，能够直接读出某一时刻相差多少mg。右图使用对数纵轴，让末期相差很多倍的小量也能占据可辨认的距离。

![四个指数衰减教学模型共用4 mg初值与0至4 mg颜色尺度。上方面板四行是离散条件；左下标出半衰时间，右下保留同一质量单位并采用对数刻度。](https://ml-biomat.com/static/tutorials/python-scientific/figures/1a504f40608d5721c7a2325d.svg?v=1a504f40608d)

图 2四个指数衰减教学模型共用4 mg初值与0至4 mg颜色尺度。上方面板四行是离散条件；左下标出半衰时间，右下保留同一质量单位并采用对数刻度。

在Matplotlib中，`subplot_mosaic`可以把这种安排写成有名字的布局。代码中的第一行是两个连续的`'map'`，它们组成跨越两列的一个面板；第二行的`'linear'`与`'log'`形成两个独立面板。返回的字典让绘图语句可以写成`ax['linear'].plot(...)`。名字在这里很有价值：当你改变面板排列时，曲线仍然发往“线性视图”，不必重新记忆它原来处于第几个格子。

`layout='constrained'`负责为刻度、轴标题和颜色条预留空间。它根据文字占据的范围调整面板位置，因此比反复手动挪动边距更适合可重复生成的图。图的整体尺寸仍需要根据阅读场景选择：在屏幕中宽度足够的标题，缩进论文的一栏之后可能很难读。保存完成后，应按最终插入文档的尺寸检查，尤其查看单位、图例和颜色条刻度。

热图中的四行是四种离散模型，各行高度相同，纵向距离不表示时间常数之间的数值间隔。代码明确写出1、2、4、8这些行标签，而没有把整幅图误标成连续参数场。如果研究对象要求在参数方向做定量插值，就需要使用真实参数网格和相应的网格边界。一个面板中的位置、面积与颜色分别代表什么，应该在绘制之前先说清楚。

## 改变坐标或颜色，究竟改变了什么

在线性纵轴上，从1 mg到2 mg与从2 mg到3 mg的垂直距离相同，因为两段都增加1 mg。在对数纵轴上，相等距离对应相同倍数：0.01到0.1、0.1到1以及1到10都相差10倍。指数衰减在半对数图中成为直线，较陡的下降表示较短的时间常数。这个变换重新分配了显示空间，曲线中的质量值仍以mg标注，数据文件里的数字也保持原值。

对数刻度需要正值。质量恰好为零时，应根据数据含义选择普通刻度、专门标记检测下限，或使用适合正负两侧的其他变换。给零偷偷加一个很小的常数，会同时改变小数值之间的倍数关系。本节的指数函数在有限时间内始终为正，所以可以直接展示对数轴；它也使我们能单独观察坐标变换本身的效果。

$$
u_{\rm linear}=\frac{m-m_{\min}}{m_{\max}-m_{\min}},\qquad u_{\rm log}=\frac{\ln(m/m_{\min})}{\ln(m_{\max}/m_{\min})}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1e48cd157a8c7e656e0ed609.svg) | 线性颜色映射位置，无量纲，范围内值对应0至1 |
| ![Formula](https://ml-biomat.com/static/agent-math/de2636f600afbad84bba9c98.svg) | 对数颜色映射位置，无量纲，范围内值对应0至1 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 待映射质量，mg；对数式中为正 |
| ![Formula](https://ml-biomat.com/static/agent-math/c48390dbe4819072144e626a.svg) | 颜色范围下限，mg；对数式要求其大于0 |
| ![Formula](https://ml-biomat.com/static/agent-math/f4112cac5b9e25ee587461ea.svg) | 颜色范围上限，mg，且大于下限 |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | 自然对数，质量比使其自变量无量纲 |

线性范围0至4 mg中，1 mg的位置是(1−0)/(4−0)=0.25。对数范围0.01至4 mg中，1 mg的位置为ln100/ln400≈0.76862。两种映射把同一个1 mg放在不同颜色位置，颜色条说明各自的换算规则。范围外的值使用端点色或另外指定的超范围颜色。

颜色还多了一层映射：先把质量放入0到1的标准区间，再到颜色表中查找对应颜色。`Normalize(0,4)`规定0 mg对应颜色表起点、4 mg对应终点，1 mg的位置为0.25。多幅图使用同一个`Normalize`对象，就能保证相同质量得到相同颜色。`LogNorm`则先比较正值之间的倍数，适合横跨多个数量级的数据。两种颜色方式都应把真实单位写在颜色条上，让读者能回到原始数值。

![上排用同一组正质量值比较线性与对数颜色映射。下排比较原始质量与除以各自初值后的剩余比例：A的原始质量是B的4倍，比例曲线重合。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8d19228b3e3c877090902c30.svg?v=8d19228b3e3c)

图 3上排用同一组正质量值比较线性与对数颜色映射。下排比较原始质量与除以各自初值后的剩余比例：A的原始质量是B的4倍，比例曲线重合。

下排展示了另一种容易混淆的操作。若把样品A的质量除以自己的初值4 mg，把样品B除以自己的初值1 mg，两条曲线会重合。这是对数据计算出的“剩余比例”，回答的是进程是否相似；它改变了纵轴所代表的量。原始质量图回答的是实际剩下多少物质，A组质量始终是B组的4倍。坐标尺度、颜色尺度和物理量归一化服务于不同问题，图注需要用对应的量名区分它们。

## 让几何位置、标记和文字都保留准确含义

画曲线时，数组中的时刻直接成为点的横坐标；画热图时，每个值却需要占据一个小矩形。这个差别会带来一个细节：图像的外边界在哪里，像素中心就不一定在哪里。本节相邻计算时刻相差0.05 min，因此把图像左右边界各向外延伸0.025 min，再把可见横轴限定到0至12 min。这样第一个像素的中心位于0，最后一个位于12，中间各列的中心也与计算时刻一致。端点像素只显示一半宽度，是边界裁切的结果。

`imshow`适合规则排列的矩阵。它把等宽、等高的像素铺到指定范围中，所以在间隔不均匀的实验时间上直接使用，会改变横向位置的含义。遇到0、1、3、8 min这样的不规则采样，可以先明确每个值代表的时间区间，再用`pcolormesh`传入真实单元格边界。若只是少量离散时刻，点图往往更直接。先理解一个色块覆盖哪个范围，才能判断某种绘图函数是否适合自己的数据结构。

连线、点和填色也需要分工。在总览里，顺序颜色适合从少到多的质量；在线图里，颜色识别的是条件，图例负责解释对应关系。这里没有把所有颜色都变成新的变量。标出半质量位置的小圆点强调的是计算得到的关键时刻，它们与密集曲线使用同一个函数；如果图中加入观测点，就应给观测和计算安排容易区分的标记。黑白打印或色觉差异也会影响识别，因此少量曲线可以同时使用线型，重要位置可以加文字或形状。

尺度范围同样需要围绕比较目标决定。只放大一小段纵轴，确实有助于查看微小差异，但读者同时需要知道该区间在整个变化中占多大比例。可以把完整过程保留为主图，把局部细节放到有范围标记的附图中。本节通过线性与对数两幅完整时间视图提供这种互补关系，两个横轴都保持0至12 min。若后续只查看末期，可以让两幅细节图共享同一时间范围，避免读者在来回比较时不断换算位置。

导出也是数量表达的一部分。SVG通常适合这些由曲线、文字和矩形构成的图，它在放大时保持边界清楚；包含数百万像素的显微图则可以把图像保留为栅格，同时让标尺与文字保持矢量。设置`svg.fonttype='none'`让文字继续以文本保存，便于后续编辑；打开文件的设备需要相应字体，中文字体尤其值得检查。PNG则通过像素固定最终显示，可以用足够分辨率满足文档尺寸。两种格式都应检查最终成图的实际大小，而不是把导出成功当成排版完成。

还可以把标记的大小与被测量的数值区分开来。本节各点大小相同，它们标出所选位置，没有增加新的变量。若今后的散点图用圆点面积表示质量，图例就需要说明面积与质量之间的关系；把半径加倍会使面积变成4倍。线宽、透明度也有类似问题。图形元素可以帮助读者找到重点，而不必每一种视觉变化都代表一项新的测量。

## 完整程序：从数组到可复用的组图

程序先计算四条曲线并保存CSV，再由同一个数组生成三组图。`mass[2]`取得τ=4 min的完整曲线，`mass[:, 80]`取得第81个时刻的四个质量值；前者沿时间阅读，后者沿条件比较。`mass.T`在导出时把时间点放到各行，让表格软件中的每一行都对应一个时刻。这里的转置只改变排列方向，不重新计算质量。

颜色条从热图对象`image`生成，因此直接使用该图像的归一化范围与颜色表。图例则来自绘制曲线时设置的`label`，与颜色条承担不同工作：图例识别哪条线属于哪个条件，颜色条把连续颜色换算为质量。你可以通过修改`taus`探索新的时间常数，同时检查行标签、图例和半衰时间是否一起更新。实际扩展程序时，可以由数组自动生成这些标签，让数值与注释保持同步。

### 完整Python：共用数组、组图和颜色映射

用NumPy计算模型，以Matplotlib的具名面板、归一化对象与矢量导出生成正文全部图。

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

运行后，`summary.json`给出几个便于核对的结果：初始质量4 mg，τ=4 min时经过4 min剩余约1.47152 mg，四个半衰时间约为0.693、1.386、2.773和5.545 min。原始质量比为4，两条剩余比例曲线的最大差为0。`curves.csv`包含全部241个时刻的数值，三个SVG文件分别对应正文中的组图、映射比较和历史概念图。SVG保存线条与文字的几何信息，适合放大查看或嵌入排版文档。

## 联动观察：让颜色、曲线和读数指向同一个位置

下面的实验用0.5 min的显示步长绘制热图，共25个时刻；曲线与Python中的241点网格使用同一公式。三个视图互相联系。选择时间常数和时刻后，热图中的位置、下方两条曲线上的标记以及数值读数会一起移动。先选τ=4 min、时间4 min，观察两个曲线面板都指向约1.472 mg。再把时间常数改成8 min，保持时间4 min，剩余质量增加到约2.426 mg。数据点的位置发生了变化，而质量色标保持一致，因此热图中的颜色变化有明确的数量含义。

### 共同数据，三种视角

选择时刻与条件，核对三图中的同一质量。降低颜色上限，观察饱和色区域和精确读数之间的关系。

[Figure: 质量总览与所选位置](https://ml-biomat.com/tutorials/python-scientific/p16/#P16-map)

[Figure: 线性质量曲线](https://ml-biomat.com/tutorials/python-scientific/p16/#P16-linear)

[Figure: 对数质量曲线](https://ml-biomat.com/tutorials/python-scientific/p16/#P16-log)

再把颜色上限从4 mg改成2 mg。超过上限的格子会汇集到颜色表终点，热图会强调较小质量范围的差别。下方曲线和精确读数保持原来的质量，提示你这次修改的是显示映射。实验同时报告超出颜色上限的网格点数，使饱和区域有可核对的范围。查看整幅图时，需要把这个上限写进颜色条；比较多个图时，则应决定是否让它们使用同一范围。

最后选择较短时间常数和较晚时刻。在线性坐标中，点接近横轴；在对数坐标中，它仍能与其他小值分开。两幅图对“绝对量已经很小”和“仍相差若干倍”分别提供清楚的视角。选择哪一幅作为主图，取决于研究问题究竟关注剩余总量、比例差异还是减少速率。

## 把这种组织方法带到自己的数据中

实际研究中的数据可能来自释放实验、传感器响应、温度扫描或机械测试。可以先写一句图要回答的问题，例如“哪些条件在早期表现相近，随后出现差异”，再把它拆成需要同时观察的量。若条件很多，总览热图有助于找到区域；若条件很少，直接叠加曲线往往更容易读。选择图形的依据是读者要完成的比较，面板数量随问题变化。

遇到多幅热图时，可以先把所有待比较数据的范围合并，生成一个共同归一化对象，再把它交给各个绘图对象。若不同面板的单位不同，就分别给出颜色条和清楚的量名。遇到重复测量时，应保留样本点并说明均值、误差线与样本数；下一节将进一步讨论这些统计对象。这里的平滑模型曲线没有观测噪声，因此也没有给它们附加测量误差条。

完成组图后，沿着读者的视线再读一次：先看到哪个面板，从哪里找到单位，哪种颜色表示同一个条件，在哪里能核对关键数值。把每个面板最重要的判断写成一句简短图注，再检查它能否从图中直接读出。如果一句话需要读者反复查找多个没有关联的图例，就调整标记、布局或注释。清楚的组图让数据之间的关系占据主要位置，而把查找和换算的负担交给经过设计的坐标与标记。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P16.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Matplotlib: constrained layout](https://matplotlib.org/3.10.9/users/explain/axes/constrainedlayout_guide.html)

   让轴标题、图例与颜色条参与布局

   Matplotlib license; original teaching code and figures
2. [Matplotlib: subplot mosaic](https://matplotlib.org/3.10.9/users/explain/axes/mosaic.html)

   用名字组织跨度不同的面板

   Matplotlib license; original teaching code and figures
3. [Matplotlib: colormap normalization](https://matplotlib.org/3.10.9/users/explain/colors/colormapnorms.html)

   理解数值到颜色的两阶段映射

   Matplotlib license; original teaching code and figures
4. [Matplotlib: choosing colormaps](https://matplotlib.org/3.10.9/users/explain/colors/colormaps.html)

   按量的含义选择连续或发散色图

   Matplotlib license; original teaching code and figures
5. [Playfair, The Commercial and Political Atlas (1786), Wellcome Collection](https://wellcomecollection.org/works/kau5c9ny)

   原版书目与图表表达的历史背景

   Historical bibliographic reference; no image or text reproduction
