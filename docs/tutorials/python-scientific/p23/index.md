# 回归系数、实验批次与模型诊断

Source: https://ml-biomat.com/tutorials/python-scientific/p23/
Language: zh-CN

在18个可追踪读数中，分开组内趋势、批次高度和单点影响。

## 每个批次都在上升，合在一起怎么反而下降

调整配方浓度时，我们常想知道：浓度每增加一点，材料响应平均会改变多少。把所有实验点画在一起，再拟合一条直线，看上去就能得到答案。然而，实验往往分批完成，不同批次可能有不同原料状态、制备条件或仪器基线。如果高浓度恰好都在整体读数较低的批次中，合并直线就同时承受浓度变化与批次差异的影响。

本节使用18个明确生成的教学读数。批次A在1、2、3 mmol/L各有三个独立试样，批次B在4、5、6 mmol/L各有三个。每个批次内，浓度增加1 mmol/L，响应中心都增加2 kPa；批次B整体下移10 kPa。每个浓度的三个读数再分别加上−0.4、0、0.4 kPa，使同一条件下的点也有可见分散。这些规则让每个结果都可以回到数据生成方式检查。

我们将用statsmodels建立合并模型和包含批次的模型，理解系数对应什么比较，再通过残差和单点扰动检查模型如何受数据影响。本节不需要先掌握统计建模术语：先读散点的空间关系，再把这些关系写成几列数字，最后看软件怎样为每一列求出系数。

## 科学史中的汇总问题，在散点图里也会出现

1951年，E. H. Simpson讨论了列联表中的交互与条件关系，说明分组信息的处理会改变统计关系的解释。列联表统计的是不同类别中的数量，本节画的是连续浓度与响应，但共同的问题很直观：把不同背景的样本混在一起时，组间位置可能盖过组内变化。历史上的讨论促使我们在解释一个总体趋势之前，先看样本是怎样组成的。

![同一18点数据在合并模型与批次模型下的结果。颜色标记批次，组内实线只绘在该批次实际浓度范围内；两幅图共享响应尺度。](https://ml-biomat.com/static/tutorials/python-scientific/figures/3ae735cbd37d4e7b06858b91.svg?v=3ae735cbd37d)

图 1同一18点数据在合并模型与批次模型下的结果。颜色标记批次，组内实线只绘在该批次实际浓度范围内；两幅图共享响应尺度。

左图把18个点合并，最小二乘直线的斜率约为−0.5714 kPa·L/mmol。右图保留批次，两个组内的斜率都是+2。两个结果并不是软件算错了，而是在回答不同的比较：合并模型描述当前这张混合样本表里的整体关系，批次模型估计在批次保持相同时，浓度变化对应怎样的响应变化。研究问题关心哪一种比较，就决定应保留哪些背景信息。

可以用两条高度不同的楼梯来想象。每条楼梯向右走都在上升，但第二条楼梯整体位于更低的位置。如果只看第一条左端和第二条右端，连线可能向下。把批次看作楼梯的基准高度，浓度看作沿楼梯前进的位置，就能理解为何需要同时记录位置和楼梯编号。类比帮助看清结构，实际判断仍然依据图中的每个试样与明确模型。

这组数据的两个浓度范围并不重叠，因此共同斜率主要由各批次内部的三个浓度水平估计，批次差值还依赖共同直线形状。若要在真实实验中更直接地比较批次，可以让各批次覆盖部分共同浓度，并安排相同条件的对照。实验设计中的重叠范围能够减少解释对外推形式的依赖，也更容易看出不同批次是否有不同斜率。

观察批次中心还能把反向趋势拆开理解。A的平均浓度为2 mmol/L、平均响应14 kPa；B的平均浓度为5 mmol/L、平均响应10 kPa。两个中心的连线是向下的，而每个中心附近的点云是向上的。合并直线同时吸收了这两部分变化。本节两个批次试样数相同，组间高度差又较大，因此组间方向足以把总体斜率拉成负值。

## 为浓度和批次各留一列，让系数有明确单位

最简单的合并模型给每个点一个共同截距和一项浓度贡献。包含批次时，再增加一个只在批次B取1、批次A取0的指示变量。它就像一只开关：属于A时不增加这项，属于B时加上一个固定偏移。用0和1表达类别，是为了在数字计算中保留分类身份；它没有把A、B解释成某种连续刻度。

$$
y_i=\beta_0+\beta_1c_i+\gamma z_i+\varepsilon_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i个试样的响应，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 试样编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29928b2adca455a1420619c0.svg) | 该试样的浓度，mmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | 批次指示变量：A为0，B为1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a5318f0ad2a783837b048ae3.svg) | 批次A的截距，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d05dff35bcc6d68d1a8ec42a.svg) | 保持批次相同的共同浓度斜率，kPa·L/mmol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 批次B相对A的基线偏移，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/df6c5ac19bbf29886eee1c95.svg) | 该观测偏离模型中心的部分，kPa。 |

取β₀=10 kPa、β₁=2 kPa·L/mmol、γ=−10 kPa，B中浓度5 mmol/L的模型中心为10+2×5−10=10 kPa。三个重复读数为9.6、10、10.4 kPa，对应偏差−0.4、0、0.4 kPa。

在本例中，A的截距为10 kPa，浓度系数为2 kPa·L/mmol，B的偏移为−10 kPa。对A中浓度2 mmol/L的试样，中心预测是10+2×2=14 kPa；对B中浓度5 mmol/L的试样，中心预测是10+2×5−10=10 kPa。把各项单位相乘后相加，每一项都回到kPa，这也是检查模型表达是否合理的一种办法。

截距对应浓度为零时的模型值，而数据从1 mmol/L开始，因此10 kPa在这里首先是确定直线位置的参数。将浓度改写为“浓度减去某个参考浓度”，可以让截距对应更接近测量范围的条件，但不会改变预测曲线。重新选择批次参考组也只会改变系数的表达方式：以B为基准时，A相对B的偏移变成+10 kPa，两个批次的预测保持一致。

共同浓度系数还包含一个形状假设：两个批次的直线平行。若科学问题允许不同批次对浓度有不同响应，可以增加“浓度×批次指示变量”的交互项，让B在基准斜率上再增加一个差值。增加这一项意味着增加一个需要数据支持的自由参数；先用图和实验机制判断问题，再决定是否需要这种更灵活的模型。

这里所谓“线性模型”，首先是指对待估系数呈线性相加。若浓度变化产生弯曲趋势，也可以增加浓度平方这一列，给它另一个系数，仍然属于线性回归的计算框架。此时单个浓度系数的解释会随模型项改变，响应对浓度的局部变化率也不再由一个常数概括。先把目前的直线模型讲清，再逐项增加确有作用的项，能让系数含义保持可读。

## 公式接口把问题变成矩阵，拟合让残差平方和最小

statsmodels的公式写法`response ~ concentration + C(batch)`把响应放在左边，把解释变量放在右边。波浪号表示“用右边的项描述左边”，加号表示增加模型项。`C(batch)`明确声明批次是类别。公式接口默认包含截距，并选一个批次作为参考，避免把所有类别列和截距重复放进同一组线性关系里。

$$
\mathrm{SSE}=\sum_{i=1}^{N}(y_i-\hat y_i)^2=\sum_{i=1}^{N}r_i^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/54f0a043833cd180cb4470f2.svg) | 残差平方和，kPa²；最小二乘选择让它最小的模型系数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | N为试样总数18，i为1到N的试样编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e1db53f60a4ee89f7d43e0d6.svg) | 观测响应和模型预测，单位均为kPa；帽号表示拟合值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 观测减预测的残差，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 累加所有试样的平方残差。 |

一个浓度条件的三个残差为−0.4、0、0.4 kPa，平方后相加为0.32 kPa²。六个浓度条件合计1.92 kPa²，正是完整批次模型的结果。保留符号的原残差仍用于看偏离方向。

程序实际生成三列设计矩阵：全为1的截距列、批次B的0/1列和浓度列。每一行对应一个试样，把该行三项分别乘以对应系数再相加，就得到预测。拟合要找的是整组系数，使18个“观测减预测”的平方加起来最小。平方让正负残差不会相互抵消，也使较大偏离对目标值产生更强影响。

程序使用`smf.ols(...).fit()`完成普通最小二乘，同时把公式生成的矩阵交给NumPy的`lstsq`独立核对。两条计算路径得到相同系数。检查矩阵列名很重要，因为公式中的书写顺序不一定就是底层矩阵顺序；本例矩阵依次为截距、B指示列、浓度，读取参数时使用名称可以避免把偏移和斜率弄反。

合并模型的残差平方和约104.7771 kPa²，批次模型为1.92 kPa²。后者对应18个明确设置的−0.4、0、0.4 kPa偏差，计算上可以直接核对：六个条件各贡献0.16+0+0.16=0.32 kPa²，合计1.92。增加参数通常会降低训练数据上的平方和，因此选择模型还要结合参数的科学含义、样本结构及对新数据的表现。

公式中的截距列为什么全是1，可以从一行预测直接看出来。A中2 mmol/L试样的一行是[1,0,2]，分别与截距10、B偏移−10和斜率2相乘后得到14。B中5 mmol/L试样的一行是[1,1,5]，同样运算得到10。这几列数就是分类与连续变量共同进入模型的方式。它也解释了为什么给每个批次都加一个指示列以后，通常要相应调整截距列，避免重复表达同一基线。

## 减去批次均值，亲眼看见“保持批次相同”的比较

批次模型里的浓度系数可以通过一种直观变换重新计算。先分别求出A、B的平均浓度和平均响应，再把每个点减去它所属批次的两个均值。A的中心是(2 mmol/L,14 kPa)，B的中心是(5 mmol/L,10 kPa)。减去中心之后，两批数据都围绕原点排列，整体高度差和浓度位置差被移开，保留下来的是各批次内部的变化。

![用本节数据具体展示汇总与分组的区别：左图菱形为批次均值，右图将每点减去所属批次均值。两组在中心化后重合，使用圆点和叉号区分；共同斜率由保留下来的组内变化决定。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0a700e0ebc841e79dd55e5ce.svg?v=0a700e0ebc84)

图 2用本节数据具体展示汇总与分组的区别：左图菱形为批次均值，右图将每点减去所属批次均值。两组在中心化后重合，使用圆点和叉号区分；共同斜率由保留下来的组内变化决定。

$$
\tilde c_i=c_i-\bar c_{g(i)},\quad\tilde y_i=y_i-\bar y_{g(i)},\quad\hat\beta_1=\frac{\sum_i\tilde c_i\tilde y_i}{\sum_i\tilde c_i^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca87a2688e1a8b679e738314.svg) | i为试样编号，g(i)为该试样所属批次A或B。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ee6cc894911be326cbd4ad7.svg) | 原浓度、所属批次平均浓度和批次中心化浓度，单位mmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0dac0e62b851aa1eaef0194.svg) | 原响应、所属批次平均响应和中心化响应，单位kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c61858a79b95932ea457c4e.svg) | 共同组内斜率的估计，kPa·L/mmol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5ca220bf09b42c86c851749f.svg) | 对全部18个试样求和。 |

两个批次各有三次−1、0、1 mmol/L的浓度偏差，因此分母为12 (mmol/L)²。对应浓度偏差与响应偏差的乘积和为24 kPa·mmol/L，平衡的±0.4 kPa项互相抵消。相除得到2 kPa·L/mmol，与包含批次截距的拟合相同。

对本节共同斜率、批次各有截距的模型，中心化后的浓度与响应可以直接给出相同斜率2。每个批次内的浓度偏差为−1、0、1 mmol/L，各重复三次；响应中心偏差相应为−2、0、2 kPa，加上平衡的小偏差。横纵偏差的乘积相加，再除以横偏差平方和，得到共同的组内关系。这提供了独立于软件公式解析的理解路径。

“控制批次”在这里有具体含义：用每个批次自己的基线解释数据，再比较同一批次里的浓度差异。它并不自动解决所有实验设计问题。若每个批次只有一个浓度，浓度与批次就无法从这些数据中独立区分；若某个未记录因素随浓度变化，仍需通过设计、测量或进一步模型处理。明确哪些变化被数据实际支持，能够把回归系数讲得更准确。

中心化方法还说明不同试样在斜率估计中扮演的角色。位于各批次平均浓度处的试样，中心化浓度为0，对斜率分子的直接贡献为0；它们仍然帮助确定批次中心和估计散布。远离批次中心的浓度水平提供更长的横向跨度，对识别斜率尤其有用。因此，合理覆盖浓度范围与简单增加同一浓度的重复次数，改善的是不同方面的信息。

## 残差找结构，影响度找值得追查的读数

残差图把每个点在纵向偏离模型的程度单独画出来。合并模型中，两个批次各自保留明显的变化结构；加入批次以后，残差回到设定的−0.4、0、0.4 kPa。真实数据里，弯曲趋势可能提示线性形状不合适，随预测值扩大的散布可能提示误差尺度变化，连续时间里的成串同号残差可能提示相关性。诊断图的用处是把下一步需要理解的结构指出来。

![上排比较原数据的合并与批次残差；下排给18号响应增加6 kPa后计算真实Cook距离，并重新拟合检查斜率变化。去掉18号仅作为诊断对照。](https://ml-biomat.com/static/tutorials/python-scientific/figures/2eafbe61810e3d9295228abe.svg?v=2eafbe61810e)

图 3上排比较原数据的合并与批次残差；下排给18号响应增加6 kPa后计算真实Cook距离，并重新拟合检查斜率变化。去掉18号仅作为诊断对照。

程序还做一次可追踪的扰动：给18号试样的响应增加6 kPa，其余17个读数保持原样。批次模型的浓度系数从2变为2.5，说明一个位于浓度范围边缘的读数能对斜率产生明显影响。下排Cook距离概括单个观测对整组拟合值的影响，18号约为1.1487。这个数可以帮助定位需要复核的记录，接着应查看原始测量、样品条件和独立复测。

杠杆值描述一个点在解释变量空间中的位置有多特殊；残差描述它在响应方向上偏离多少。一个点可能浓度很特殊却紧贴模型，也可能浓度普通却响应偏离很大，两者对拟合的影响不同。Cook距离将位置和残差共同纳入，因此与单纯按最高响应值排序不同。本例同时保存杠杆、残差和Cook距离，便于把每个诊断数追到试样编号。

为检查影响度的实际含义，程序额外去掉18号后重新拟合，斜率约为1.95862。它略低于原来的2，是因为被去掉的原始18号本来就带有+0.4 kPa偏差。这次重算是一项敏感性分析，用来展示结果对该记录的依赖。是否修改数据，应依据记录核查和预先规定的数据处理规则；完整数据结果与敏感性结果可以同时保存。

对异常点的处理可以形成一条可检查的流程：先确认试样编号与原始文件一致，再检查单位、录入、仪器状态与试样制备记录，必要时安排复测。若确认是录入错误，就保存更正依据；若读数确实反映样品差异，就把它作为需要解释的数据结构。敏感性分析在这条流程中说明结论受该点影响多大，而实验记录决定这种影响应该怎样理解。

## 完整程序：读出有名字的系数，而不是搬运整张摘要

完整示例将数据生成、两种拟合、中心化检查和单点扰动放在同一文件中。`params`提供有名字的系数，`fittedvalues`给出每个已有试样的预测，`resid`给出对应残差，`get_influence`连接诊断量。预测新条件时，用包含浓度与批次两列的DataFrame传给`predict`，让软件按照原先的类别编码处理。

### 完整示例：公式回归、批次中心化和单点影响

运行生成两份试样表、诊断表、数值摘要和三幅组图。所有教学数据在程序中明确生成。

```
"""Fit concentration trends while preserving experimental batch identity."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
COLORS={'A':'#28658c','B':'#c26835'}


def data(offset=-10.,perturbation=0.):
    rows=[]
    for batch,levels in [('A',[1.,2.,3.]),('B',[4.,5.,6.])]:
        for concentration in levels:
            for residual in [-.4,0.,.4]:
                rows.append({'specimen':len(rows)+1,'batch':batch,'concentration':concentration,
                    'response':10+2*concentration+(offset if batch=='B' else 0)+residual})
    frame=pd.DataFrame(rows);frame.loc[17,'response']+=perturbation
    return frame


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';tr=lambda z,e:z if zh else e;available={f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family':[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in available],'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    frame=data();pooled=smf.ols('response ~ concentration',data=frame).fit();adjusted=smf.ols('response ~ concentration + C(batch)',data=frame).fit()
    design=adjusted.model.exog;independent=np.linalg.lstsq(design,frame.response.to_numpy(),rcond=None)[0]
    assert np.allclose(independent,adjusted.params.to_numpy())
    centered=frame[['concentration','response']]-frame.groupby('batch')[['concentration','response']].transform('mean')
    centered_slope=float(np.dot(centered.concentration,centered.response)/np.dot(centered.concentration,centered.concentration))
    changed=data(perturbation=6.);changed_fit=smf.ols('response ~ concentration + C(batch)',data=changed).fit();influence=changed_fit.get_influence();without=smf.ols('response ~ concentration + C(batch)',data=changed.iloc[:-1]).fit()
    frame.to_csv(args.output/'specimens.csv',index=False);changed.to_csv(args.output/'perturbed-specimens.csv',index=False)
    diagnostics=pd.DataFrame({'specimen':changed.specimen,'fitted':changed_fit.fittedvalues,'residual':changed_fit.resid,'leverage':influence.hat_matrix_diag,'cooks_distance':influence.cooks_distance[0]});diagnostics.to_csv(args.output/'diagnostics.csv',index=False)
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for batch,group in frame.groupby('batch'):
        for a in ax:a.scatter(group.concentration,group.response,color=COLORS[batch],label=tr(f'批次{batch}',f'Batch {batch}'),s=45)
        x=np.linspace(group.concentration.min(),group.concentration.max(),100);prediction=adjusted.predict(pd.DataFrame({'concentration':x,'batch':batch}));ax[1].plot(x,prediction,color=COLORS[batch],lw=2)
    x=np.linspace(1,6,200);ax[0].plot(x,pooled.predict(pd.DataFrame({'concentration':x})),color='#20313e',lw=2,label=tr('合并直线','Pooled line'))
    for a in ax:a.set(xlabel=tr('浓度 / mmol·L⁻¹','Concentration / mmol·L⁻¹'),ylabel=tr('响应 / kPa','Response / kPa'),ylim=(6.5,17));a.legend(frameon=False,fontsize=10);a.grid()
    ax[0].set_title(tr('合并所有点：斜率 −0.5714','All points pooled: slope −0.5714'));ax[1].set_title(tr('保留批次：共同斜率 +2','Retain batch: common slope +2'));save(fig,'regression')
    fig,ax=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for j,model in enumerate([pooled,adjusted]):
        for batch,group in frame.groupby('batch'):ax[0,j].scatter(group.concentration,model.resid.loc[group.index],color=COLORS[batch],s=42,label=batch)
        ax[0,j].axhline(0,color='#20313e',lw=1);ax[0,j].set(xlabel=tr('浓度 / mmol·L⁻¹','Concentration / mmol·L⁻¹'),ylabel=tr('残差 / kPa','Residual / kPa'),title=tr('合并模型的残差','Pooled-model residuals') if j==0 else tr('批次模型的残差','Batch-model residuals'));ax[0,j].legend(frameon=False)
    ax[1,0].bar(changed.specimen,influence.cooks_distance[0],color=[COLORS[b] for b in changed.batch]);ax[1,0].set(xticks=[1,3,6,9,12,15,18],xlabel=tr('试样编号','Specimen index'),ylabel=tr('Cook距离，无量纲','Cook distance, dimensionless'),title=tr('给18号读数增加6 kPa后','After adding 6 kPa to specimen 18'))
    slopes=[adjusted.params['concentration'],changed_fit.params['concentration'],without.params['concentration']]
    ax[1,1].scatter([0,1,2],slopes,s=65,color=['#20313e','#b64a35',COLORS['A']]);ax[1,1].plot([0,1,2],slopes,color='#8f9ca5',lw=1);ax[1,1].set(xlim=(-.5,2.5),xticks=[0,1,2],xticklabels=[tr('原数据','Original'),tr('18号+6','18 + 6'),tr('逐一检查：\n去掉18号','Diagnostic refit:\nleave out 18')],ylabel=tr('浓度系数 / kPa·L·mmol⁻¹','Concentration coefficient / kPa·L·mmol⁻¹'),title=tr('读数影响通过重新拟合核对','Check influence by refitting'))
    for a in ax.flat:a.grid(axis='y')
    save(fig,'diagnostics')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for batch,group in frame.groupby('batch'):
        ax[0].scatter(group.concentration,group.response,color=COLORS[batch],label=batch,s=40)
        ax[0].scatter(group.concentration.mean(),group.response.mean(),marker='D',s=100,edgecolor='#20313e',color=COLORS[batch])
        c=centered.loc[group.index];ax[1].scatter(c.concentration,c.response,color=COLORS[batch],s=55 if batch=='A' else 25,marker='o' if batch=='A' else 'x',label=batch)
    ax[0].plot([2,5],[14,10],color='#71808b',ls='--',label=tr('批次均值之间的方向','Direction between batch means'))
    ax[0].set(xlabel=tr('原浓度 / mmol·L⁻¹','Original concentration / mmol·L⁻¹'),ylabel=tr('原响应 / kPa','Original response / kPa'),title=tr('组间位置改变合并趋势','Between-group positions change the pooled trend'))
    ax[1].plot([-1.1,1.1],[-2.2,2.2],color='#20313e',label=tr('批次中心化斜率2','Within-batch centered slope 2'))
    ax[1].set(xlabel=tr('浓度 − 批次均值 / mmol·L⁻¹','Concentration − batch mean / mmol·L⁻¹'),ylabel=tr('响应 − 批次均值 / kPa','Response − batch mean / kPa'),title=tr('减去各批次均值，显出组内变化','Subtract each batch mean to expose within-group change'))
    for a in ax:a.legend(frameon=False,fontsize=9);a.grid()
    save(fig,'history')
    summary={'versions':{'numpy':np.__version__,'pandas':pd.__version__,'statsmodels':statsmodels.__version__,'matplotlib':matplotlib.__version__},'n':len(frame),
        'pooled_slope':float(pooled.params['concentration']),'pooled_intercept':float(pooled.params['Intercept']),'adjusted_slope':float(adjusted.params['concentration']),'adjusted_intercept_A':float(adjusted.params['Intercept']),'batch_B_shift':float(adjusted.params['C(batch)[T.B]']),
        'pooled_sse':float(pooled.ssr),'adjusted_sse':float(adjusted.ssr),'centered_slope':centered_slope,'design_columns':adjusted.model.exog_names,
        'perturbed_slope':float(changed_fit.params['concentration']),'leave18out_slope':float(without.params['concentration']),'specimen18_cook':float(influence.cooks_distance[0][-1]),'specimen18_leverage':float(influence.hat_matrix_diag[-1])}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

输出中的两张试样表分别保存原数据和18号加6 kPa后的数据，诊断表则逐行保存试样编号、预测、残差、杠杆与Cook距离。数值摘要保留本节需要解释的系数与平方和。statsmodels还能够给出标准误、置信区间和检验，但这些推断需要与误差结构匹配。本节的平衡偏差是为解释计算而明确设置的，因此主要关注系数、拟合几何与敏感性。

若使用真实实验，拟合前要检查缺失值、类别拼写和单位是否一致，并确认最终模型用了哪些行。类别“A”与“A ”可能成为不同组，浓度单位混用会改变系数尺度。把清理后的输入表与拟合结果一起保存，能够让统计解释回到实际试样，而不是只留下模型摘要中的几行数字。

## 联动实验：改变批次高度，再追踪一个点的影响

实验允许改变B的整体偏移、18号读数的额外变化，以及采用合并还是批次模型。主图显示全部18个点与当前拟合线，残差图显示同一批点对模型的偏离，系数图同时比较合并斜率、批次斜率与去掉18号后的批次斜率。每次操作都重新计算同一套数据关系，不会把图线与读数分开更新。

### 批次、浓度与一个可追踪的试样

[Figure: 原始点与拟合线](https://ml-biomat.com/tutorials/python-scientific/p23/#P23-data)

[Figure: 同一试样的残差](https://ml-biomat.com/tutorials/python-scientific/p23/#P23-residual)

[Figure: 三种拟合的斜率比较](https://ml-biomat.com/tutorials/python-scientific/p23/#P23-coefficients)

蓝色A、橙色B；黑色外圈标记追踪试样。批次线只覆盖各自实测浓度范围；右下图始终保留去掉18号的诊断对照。

先将B偏移从−10 kPa调到0。两个批次逐渐落到同一条趋势线上，合并斜率会从负值回到2，批次模型的组内斜率保持2。再恢复−10，并给18号增加6 kPa，观察两个模型怎样调整以及18号残差怎样变化。选择某个试样后，两幅散点图会同时强调该点，并显示它的浓度、观测与预测，方便追踪一条记录的完整路径。

这里的“去掉18号”始终作为固定的诊断对照显示，不会改变主图中的数据集。这样可以同时看到完整拟合与敏感性重算。对研究中的异常读数，先通过图定位，再用记录和实验过程解释原因，能够比直接删点得到更清楚的科学判断。

还可以把主图中选中的18号与原始公式逐项对照。未增加额外读数时，它属于B、浓度6 mmol/L、响应12.4 kPa，批次模型预测12 kPa，因此残差为0.4 kPa。加上6 kPa后，模型本身也会重新调整，新的残差不能简单沿用原残差再加6，因为新的预测值已经改变。这个细节帮助区分“修改观测多少”和“拟合后还剩多少偏离”。

## 一条回归结论，应当说明比较发生在什么条件下

解释本节结果时，可以写：在所设平行直线模型中，同一批次内浓度每增加1 mmol/L，平均响应增加2 kPa；B相对于A的基线偏移为−10 kPa。这个说法明确了条件、单位和比较对象。若只说“浓度系数为2”，读者就需要猜测它属于哪种模型、是否控制批次，以及浓度究竟用什么单位。

真实研究中，回归可以帮助描述关联、预测指定条件下的响应、调整已记录的背景差异，并检查结果对某些观测的敏感性。若目标是确定改变浓度带来的因果效果，还需要随机化、对照或其他能区分共同变化因素的研究设计。把这些任务放在各自合适的位置，模型系数就能成为连接数据、实验条件与研究解释的清楚语言。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P23.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [statsmodels 0.14.6: Fitting models using formulas](https://www.statsmodels.org/v0.14.6/example_formulas.html)

   类别变量、默认截距与交互项的公式语义。

   BSD-3-Clause; technical reference
2. [statsmodels: OLS](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html)

   普通最小二乘与设计矩阵接口。

   BSD-3-Clause; technical reference
3. [statsmodels: OLSInfluence](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html)

   杠杆、Cook距离与逐点敏感性。

   BSD-3-Clause; technical reference
4. [Simpson (1951): The Interpretation of Interaction in Contingency Tables](https://doi.org/10.1111/j.2517-6161.1951.tb00088.x)

   分组、汇总与条件关系的原始讨论；本节连续数据与图为原创。

   Copyrighted article; historical reference only
