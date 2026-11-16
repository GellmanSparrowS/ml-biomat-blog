# 分组以后，平均值回答什么问题

Source: https://ml-biomat.com/tutorials/python-scientific/p12/
Language: zh-CN

沿着读数、试样和配方三层身份，理解分组、权重、缺失与表格变形。

## 同一块材料多称几次，平均值为什么变了

比较两种吸水材料时，我们常常想知道哪一种配方平均能吸收更多水。把所有读数放进表格，按配方求平均，似乎已经回答了问题。但如果某块试样称了三次，另一块只称了一次，直接平均就让前者贡献了三份数字。这里有两个不同层次：制备了多少块独立试样，以及每块试样留下多少次技术读数。它们都值得记录，却不能只用一个含糊的“样本数”代替。本节学习 pandas 的分组计算，并沿着每一条读数追踪平均值的对象和权重。

我们用一组明确构造的教学记录：A、B 两种配方各有三块独立制备的试样，编号分别为 A01–A03 和 B01–B03。A01 的读数是 2.0、2.2，A02 是 2.8，A03 是 3.0、3.2、3.4；B01 是 2.0、2.2，B02 是 2.5、2.7，B03 是 2.9。每个数字都是同一规定浸泡条件下的吸水量 q，表示每克干材料所吸收的水的克数，记作 g/g。总共六块试样留下十一条读数，其中同一编号内的数值来自对同一试样状态的重复读取。真实实验还需保持称量过程中的含水状态稳定，并记录浸泡时间、温度和擦除表面液体的方法。

例如，一块干质量为 0.50 g 的材料，在规定的测量状态下湿质量为 1.55 g，吸水量就是湿、干质量之差除以干质量。这个定义把不同大小试样换算到相同的干材料基准，也让“2.1”有了明确含义。它不是湿材料里水的百分比；换成湿质量作分母，回答的会是另一个问题。进入表格计算之前，先确定每一列怎样测得、每一行代表谁，后续的分组才有稳定的科学含义。

$$
q=\frac{m_{\mathrm{wet}}-m_{\mathrm{dry}}}{m_{\mathrm{dry}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 按干质量归一的吸水量，g/g；质量比无量纲，g/g保留计算基准 |
| ![Formula](https://ml-biomat.com/static/agent-math/2bf977fe0b88c7538b19851d.svg) | 规定测量状态下的湿质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/22b087ed9f064a584dfccac0.svg) | 干材料质量，g，取正值 |

湿、干质量之差对应定义中的吸收水质量，使用相同质量单位后相除。m_wet=1.55 g、m_dry=0.50 g，得到q=(1.55−0.50)/0.50=2.1 g/g；即每克干材料对应2.1克吸收水。测量状态及表面液体处理在各试样间保持一致。

本节完成后，你可以把一张读数表变成带有效计数的试样表，再整理成配方比较表；也能把组内均值放回原始记录，定位一条读数与同试样其他读数的差异。示例会保存这些中间表，而不是只留下最后两个平均数。这样，看到某个结果发生变化时，可以沿着编号逐层找到原因。

## 把大表拆成小问题，再把结果放回一起

如果拿纸笔处理这十一条记录，一种自然的做法是先把同编号的纸条放在一起，对每堆计算均值，再将六个试样结果排成新表。随后按配方重新分成两堆，又可以得到配方层面的结果。这个过程包含分组、计算和合并三步。分组只决定谁与谁一起运算，并没有规定下一步一定求平均；同一堆记录也可以用于计数、取最大值，或计算与组内基准的偏离。

Hadley Wickham 在 2011 年的论文中系统讨论了 split–apply–combine，也就是“拆分—计算—合并”的数据分析策略，并用棒球记录和时空臭氧数据说明它怎样被组织成可重复使用的程序。这篇工作对应 R 的 plyr 包，讨论的是计算组织方式。今天在 pandas 中，`groupby` 让我们把同样的结构写得清楚：先说明分组键，再选择需要计算的列与操作。下面用本节数据画出这条路线，每个中间数字都能与原始记录对应。

![以A的六条构造读数说明分组计算的三步。中间表保留三个试样的身份，最后平均的分母是三个试样。](https://ml-biomat.com/static/tutorials/python-scientific/figures/19ff17dff4666d5bc7a7799b.svg?v=19ff17dff466)

图 1以A的六条构造读数说明分组计算的三步。中间表保留三个试样的身份，最后平均的分母是三个试样。

这张图还有一个容易忽略的细节：每一步之后，“一行是什么”都变了。第一张表的一行是一条读数；中间表的一行是一块试样；最后一张表的一行是一种配方。表格变短并不意味着信息自动变得更可靠，而是我们选择把一些细节压缩成了摘要。试样编号、有效读数数以及配方标签应与摘要一起保留，读者才能知道哪些信息仍在表内，哪些需要返回上一层查看。

这种思路可以迁移到显微图像、拉伸曲线和生物测量：一幅图像可能含多个颗粒，一块试样可能拍了多幅图，一个制备批次又可能包含多块试样。具体研究中，应先画出这样的层次关系，再选分组键。把颗粒、图像、试样或批次选作比较单位，会改变平均值的解释。程序可以可靠地执行每一种分组，但需要我们先说明想让哪个层次在比较中等权。

## 分组键是身份，聚合列才是需要计算的量

原始表中，`formulation` 是配方，`specimen` 是试样编号，`reading` 是该试样内的读取序号，`q` 是吸水量。配方标签和试样编号用于建立身份；读取序号帮助追踪记录；吸水量才是本例需要计算平均的物理量。即使某个编号只由数字组成，也不应因为它是数值类型就一起求平均。以“第 1、2、3 次读取”为例，序号平均得到 2，并没有给出试样吸水能力。

`table.groupby(['formulation', 'specimen'], as_index=False)` 按配方与试样编号的组合分组。方括号中的两个名字表示两个分组字段，不是先得到两套互不相干的分组。只有两列标签都相同的行才会进入同一组。在我们的编号中，A01 本身已经全局唯一；仍把配方写入键，是为了让输出表直接保留实验层次。如果不同批次各自使用“01”作为试样号，就还应加入批次字段，避免把不同实体混在一起。

后接的 `agg` 使用带名字的聚合：`q_mean=('q', 'mean')` 表示从 q 列计算均值，并把输出列命名为 q_mean；`rows=('q', 'size')` 统计该组有多少行；`valid=('q', 'count')` 统计其中有多少个非缺失的 q。三项一起计算，输出表就能同时回答结果是多少、依据几条有效读数，以及是否有记录缺失。`as_index=False` 让分组标签继续作为普通列出现，便于打印、存 CSV 和继续分组。

这一步把 A01 的两条读数压缩为 2.1，A02 保持 2.8，A03 得到 3.2；B 的三个试样均值为 2.1、2.6、2.9。新的表有六行。再次按 formulation 分组，就可以让每块试样各贡献一个均值。`groupby` 不要求同组记录在输入中相邻，换一个行顺序也不会改变这些结果。若只是想保留分组首次出现的顺序，可以显式使用 `sort=False`；排序控制展示次序，身份仍由标签决定。

## 平均数背后，每一份权重都指向一个对象

A 配方的六条读数相加为 16.6 g/g，除以 6，得到约 2.7667 g/g。若先得到三个试样均值，再把 2.1、2.8 和 3.2 相加除以 3，则得到 2.7000 g/g。两条计算路径都执行了明确的算术；区别在于前者让每条读数等权，后者让每块试样等权。A03 留下三条读数，所以在直接平均中占一半；A02 只有一条，占六分之一。在试样等权结果中，它们各占三分之一。

$$
\begin{aligned}\bar q_j&=\frac{1}{n_j}\sum_{i=1}^{n_j}q_{ij},\qquad \bar q_{\mathrm{equal}}=\frac{1}{J}\sum_{j=1}^{J}\bar q_j\\ \bar q_{\mathrm{rows}}&=\frac{\sum_{j=1}^{J}n_j\bar q_j}{\sum_{j=1}^{J}n_j}\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b3f5a274db5824837fd8be6c.svg) | 试样j的第i个有效吸水量读数，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 组内读数与试样的索引，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a84ce73458078ab383399f3.svg) | 试样j的有效读数数，无量纲正整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | 同一配方中具有有效均值的试样数，无量纲正整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/5756278ec076431a907dc307.svg) | 试样j的有效读数均值，g/g；横线表示平均 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e66413b5e17439d8aa63259.svg) | 每个有效试样等权得到的配方均值，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/30e030e3c27645d3136ff08b.svg) | 每条有效读数等权得到的配方均值，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对所标索引范围内的项依次相加 |

n_j×试样均值还原该试样的读数总和，因此第二行等于把所有有效读数相加后除以总条数。A的n_j为2、1、3，均值为2.1、2.8、3.2：逐读数均值=(2×2.1+1×2.8+3×3.2)/6≈2.7667；试样等权=(2.1+2.8+3.2)/3=2.7。两式单位均为g/g。无有效读数的试样保留在登记表，但不进入这里的J项求和。

![左：每条读数与黑色短线标记的试样均值。中：每个配方内的权重分别归一到1。右：读数等权与试样等权的配方均值，共用吸水量尺度。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0b0e168e0b8aa5de7c3aaea4.svg?v=0b0e168e0b8a)

图 2左：每条读数与黑色短线标记的试样均值。中：每个配方内的权重分别归一到1。右：读数等权与试样等权的配方均值，共用吸水量尺度。

可以把这个区别想成给每块试样分配发言时间。直接平均让每条记录获得相同的一小段时间，记录多的试样总共说得更久；先汇总试样则让每块材料先形成一个代表值，再各说一次。这个类比解释权重怎样分配，却不替实验决定哪种问题更有意义。如果研究目标是这六块独立制备材料的平均表现，通常希望保留试样这一层；如果目标确实是某个定义清楚的读取过程中的全部读数，则应同时交代该过程怎样分配读取次数。

把 A01 的两条已有记录复制成六份，是一个纯粹的计算实验：没有增加材料，也没有做新的称量。A01 的均值仍是 2.1，A 配方的试样等权均值仍是 2.7，但逐读数平均降到 2.35。原因可以完全写在纸上：A01 贡献 12 条读数、合计 25.2；其余两块试样贡献 4 条、合计 12.4；最后 37.6 除以 16 得到 2.35。改变记录数量就改变了权重，因此合并文件时重复导入同一组记录，也可能改变统计结果。

两种平均在各试样有效读数数相同时必然一致，在某些特别的数据组合下也可能恰好相同。结果相同并不能让观测单位变得无关紧要。真正的技术重复有助于了解读取波动或提高同一试样均值的精度，但没有增加独立制备试样的数量。若希望根据不同精度进一步加权，应明确建立测量方差及相关性的模型；简单按行数加权所包含的假设，需要与实际实验过程相配。

## 缺失值让分母改变，也可能让一个试样暂时失去结果

现在设 A02 的唯一吸水量没有记录下来，用缺失值表示，试样编号和那一行仍然存在。它的 size 为 1，count 为 0，试样均值为缺失。A 配方仍登记了三块试样，但只有两块具有可计算的 q；试样等权平均变为 (2.1+3.2)/2=2.65 g/g。这时若报告“3 个试样的均值 2.65”，就把登记数量与实际参与平均的数量混在了一起。程序因此同时保存 specimens 和 valid_specimens，分别表示登记试样数与有有效均值的试样数。

![左：只复制A01的已有记录，试样数不变；右：A02的q缺失以后，记录行数与有效数值数分别保留。](https://ml-biomat.com/static/tutorials/python-scientific/figures/5e56ca17ac5874aa2403bfee.svg?v=5e56ca17ac58)

图 3左：只复制A01的已有记录，试样数不变；右：A02的q缺失以后，记录行数与有效数值数分别保留。

pandas 的 `mean` 默认跳过数值缺失，分母使用有效数值的数量。这个行为能让部分完整的组继续产生摘要，但缺失的科学原因还需要结合记录理解：仪器未保存、试样破损和数值低于检测范围，可能对应不同的数据处理问题。本例保留缺失状态，并把有效计数与结果放在一起。如果把缺失填为 0，A02 就变成了一个“确实测得不吸水”的试样，组均值随之变为约 1.7667；这已经改变了输入信息的含义。

分组标签缺失是另一件事。若某行的配方没有填写，默认分组会将它排除在按配方的结果之外。示例在主要分组中写出 `dropna=False`，让缺失标签也能作为一个待识别的组保留下来；这与 q 的均值是否跳过缺失数值是两个不同开关。实际整理时，可以先检查标签的空白、拼写和多余空格，再统计每个分组含多少条记录。一个“B ”和一个“B”在原始字符串上不同，不会自动因为看起来相近而合成同一组。

配方比较表还保存试样均值的标准差。它描述独立试样代表值的离散程度，而不是同一试样重复读取的波动。对于 A 的 2.1、2.8、3.2，平均为 2.7，三个偏差平方合计 0.62，除以 2 再开方，得到约 0.5568 g/g。如果组内只有一个有效试样，样本标准差没有足够的自由度，结果保持缺失；写成 0 会暗示已经观察到完全没有试样间差异。均值、离散程度和有效计数一起阅读，才看得清这张摘要表描写了什么。

$$
s_q=\sqrt{\frac{\sum_{j=1}^{J}(\bar q_j-\bar q_{\mathrm{equal}})^2}{J-1}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d6959d02159dd0ada26992e7.svg) | 有效试样均值之间的样本标准差，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/5756278ec076431a907dc307.svg) | 第j个有效试样的读数均值，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e66413b5e17439d8aa63259.svg) | 这J个试样均值的等权平均，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 有效试样索引，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | 有效试样数，无量纲；本式要求至少2个 |
| ![Formula](https://ml-biomat.com/static/agent-math/a532e06315851dc3910227b7.svg) | 均值由这组数据估计后剩下的离散偏差自由度 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ca563c8033303e110f807c.svg) | 将平方偏差相加，再开平方恢复原量的单位 |

先测量各试样均值离共同中心多远；三个偏差受总和为零的约束，样本方差按J−1归一。A的偏差为−0.6、0.1、0.5 g/g，平方和0.62，s_q=√(0.62/2)≈0.556776 g/g。这描述试样代表值的离散；将其用于总体方差估计时，还需独立且具有可比抽样分布的试样。

## 摘要放在新表里，组内基准也能回到每一条记录

聚合后的六行表适合比较试样，但有时我们想保留十一行原始读数，并为每一行添上所属试样的均值。`transform('mean')` 正好完成这个任务：它在组内计算一个均值，再把这个均值按原来的行身份放回去。A01 的两行都得到 2.1，A03 的三行都得到 3.2。输出长度仍为十一，因而可以直接作为新列加入原表，不必凭记忆复制粘贴，也不必假设分组结果的第几行恰好对应原表的第几行。

用每条 q 减去这一列试样均值，得到组内偏离。A01 的两项为 −0.1 和 +0.1，A03 的三项为 −0.2、0、+0.2。这些量帮助我们观察某次读取相对于同一试样的其他读取处在什么位置。每组偏离之和接近零，是均值定义带来的代数性质；它可以检查行对齐和计算过程，却没有说明仪器已校准，也没有证明读数不存在系统偏移。若所有读数一起偏高，减去它们自己的均值会把共同偏移一并消去。

从输出形状看，`agg` 把每组压成一行，`transform` 为原表每行返回一个组内计算结果。记住这个区别，比单独背两个函数名更有用。还可以用筛选保留满足某种条件的完整分组，例如要求至少两条有效技术读数；这种筛选应对应预先确定的质量规则，同时保存哪些试样因此未进入后续结果。按一个规则删除整组，与按某个数值阈值删除单条读数，也会留下不同的研究对象。

`pivot` 则处理另一种需求：把试样排在行上、读取序号排在列上，让 A03 的三次读取并排出现。它重新安排已有数值，不替我们决定如何合并重复单元格。初始表中，每个“试样—读取序号”组合只出现一次，因此可以直接透视；复制 A01 之后，这个组合不再唯一，必须把 copy 也纳入身份，或者先按明确规则汇总。没有第三次读取的 A01 在宽表第三列为空，这表示没有对应记录，不能把它与真正测得零吸水量的格子混淆。

## 完整程序保留从读数到配方的每一层

程序从 `READINGS` 字典构造原始表。字典的键是试样编号，值是该试样的技术读数列表；`make_table` 将这些嵌套内容展开成整齐的行，并保留配方、读取序号和复制编号。默认 copies=1、missing=False 对应原始十一条教学记录。两个可选参数只用于比较权重和缺失处理，不会修改字典中的原始列表。这样的安排使每次计算都从同一份明确输入重新开始，便于追踪交互实验中的单一变化。

`summarize` 返回三个对象：试样表、配方表和添有组内基准的读数表。函数中的第一次聚合负责试样，第二次负责配方；逐读数均值单独计算，再按配方标签映射到同一张比较表。这里使用标签对应，而没有直接把一列结果按当前位置塞进去，是为了让表格即使经过排序，A 的结果仍回到 A。下一节连接多张表时，会继续用身份键来维护这种对应关系。

### 运行完整示例

使用已安装pandas、NumPy和Matplotlib的环境；中文图将en换成zh。

```
python main.py --output results --language en
```

### 从读数到试样，再到配方

所有构造输入保存在READINGS中；make_table建立记录，summarize保留三层计算关系，plot_all生成结果图。

```
"""Follow technical readings through specimen and formulation summaries.

The values are constructed teaching data. Copying A01 readings below is a
weighting experiment; the copies are not additional physical measurements.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

READINGS = {'A01': [2.0, 2.2], 'A02': [2.8], 'A03': [3.0, 3.2, 3.4],
            'B01': [2.0, 2.2], 'B02': [2.5, 2.7], 'B03': [2.9]}
BLUE, ORANGE, INK = '#235f83', '#bd5838', '#1e303c'


def make_table(copies=1, missing=False):
    records = []
    for specimen, values in READINGS.items():
        for copy in range(copies if specimen == 'A01' else 1):
            for reading, value in enumerate(values, 1):
                records.append({'formulation': specimen[0], 'specimen': specimen,
                                'reading': reading, 'copy': copy + 1,
                                'q': np.nan if missing and specimen == 'A02' else value})
    return pd.DataFrame(records)


def summarize(table):
    specimens = (table.groupby(['formulation', 'specimen'], as_index=False, dropna=False)
                 .agg(q_mean=('q', 'mean'), rows=('q', 'size'), valid=('q', 'count')))
    formulations = (specimens.groupby('formulation', as_index=False, dropna=False)
                    .agg(q_equal=('q_mean', 'mean'), specimens=('specimen', 'size'),
                         valid_specimens=('q_mean', 'count'), sd_specimens=('q_mean', 'std')))
    row_means = table.groupby('formulation', dropna=False)['q'].mean()
    # Map by category label. Position alone is not a group identifier.
    formulations['q_rows'] = formulations['formulation'].map(row_means)
    traced = table.copy()
    traced['specimen_mean'] = traced.groupby('specimen')['q'].transform('mean')
    traced['within_specimen'] = traced['q'] - traced['specimen_mean']
    return specimens, formulations, traced


def plot_all(table, specimens, groups, output, language):
    zh = language == 'zh'
    tr = lambda z, e: z if zh else e
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','DejaVu Sans'] if f in available]
    plt.rcParams.update({'font.family': fonts if zh else ['DejaVu Sans'], 'font.size': 12,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none', 'axes.unicode_minus': False})
    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(output / f'{name}-{language}.{ext}', dpi=165, bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 5.3), gridspec_kw={'width_ratios':[1.2, .9, 1]}, layout='constrained')
    for i, row in specimens.iterrows():
        values = table.loc[table.specimen == row.specimen, 'q'].to_numpy()
        offsets = np.linspace(-.14,.14,len(values)) if len(values)>1 else [0]
        axes[0].scatter(values, i+np.array(offsets), color=BLUE if row.formulation=='A' else ORANGE, s=45)
        axes[0].plot([row.q_mean-.03, row.q_mean+.03], [i,i], color=INK, lw=3)
    axes[0].set(yticks=range(6), yticklabels=specimens.specimen, xlabel='q / g g⁻¹',
                title=tr('a  11条读数，6个独立试样','a  11 readings, 6 independent specimens'))
    axes[0].invert_yaxis();axes[0].grid(axis='x',alpha=.15)
    axes[1].barh(np.arange(6)-.15, specimens.valid/np.repeat([6,5],3), height=.28,color=BLUE,label=tr('逐读数权重','Reading weights'))
    axes[1].barh(np.arange(6)+.15, np.ones(6)/3, height=.28,color=ORANGE,label=tr('试样等权','Equal specimens'))
    axes[1].set(yticks=range(6),yticklabels=specimens.specimen,xlim=(0,.62),xlabel=tr('配方内权重，无量纲','Weight within formulation'),title=tr('b  谁在平均值中占得更多','b  Who receives more weight'))
    axes[1].invert_yaxis();axes[1].legend(loc='lower right',fontsize=9)
    for i,row in groups.iterrows():
        axes[2].plot([i-.13,i+.13],[row.q_rows,row.q_equal],color='#9aa6ad',lw=1.5)
        axes[2].scatter(i-.13,row.q_rows,color=BLUE,s=65,label=tr('逐读数','Readings') if i==0 else None)
        axes[2].scatter(i+.13,row.q_equal,color=ORANGE,s=65,label=tr('试样等权','Equal specimens') if i==0 else None)
        axes[2].annotate(f'{row.q_rows:.4f}',(i-.13,row.q_rows),xytext=(-2,12),textcoords='offset points',ha='right',fontsize=10)
        axes[2].annotate(f'{row.q_equal:.4f}',(i+.13,row.q_equal),xytext=(2,-20),textcoords='offset points',ha='left',fontsize=10)
    axes[2].set(xticks=[0,1],xticklabels=['A','B'],xlim=(-.6,1.6),ylim=(2.25,2.95),ylabel='q / g g⁻¹',xlabel=tr('配方','Formulation'),title=tr('c  两个明确的平均问题','c  Two explicit averaging questions'))
    axes[2].legend(loc='upper right',fontsize=9);axes[2].grid(axis='y',alpha=.15)
    save(fig,'units-and-weights')

    fig,ax=plt.subplots(figsize=(13.5,6.4));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.02,.94,tr('2011：把分组计算组织成可复用的步骤','2011: organize grouped computation into reusable steps'),fontsize=19,weight='bold')
    ax.text(.02,.86,tr('Wickham的 split–apply–combine 思路；下方用本节构造读数演示。','Wickham’s split–apply–combine strategy, illustrated with this chapter’s constructed readings.'),fontsize=12)
    boxes=[(.02,.08,.25,.66),(.36,.08,.27,.66),(.73,.08,.25,.66)]
    for x,y,w,h in boxes:ax.add_patch(plt.Rectangle((x,y),w,h,facecolor='#edf3f4',edgecolor='#c5d2d9'))
    for x1,x2 in [(.28,.35),(.64,.72)]:ax.annotate('',xy=(x2,.43),xytext=(x1,.43),arrowprops={'arrowstyle':'->','lw':2,'color':INK})
    ax.text(.04,.68,tr('分开：按试样身份','Split: by specimen'),fontsize=14,weight='bold')
    ax.text(.04,.56,'A01   2.0, 2.2\nA02   2.8\nA03   3.0, 3.2, 3.4',fontsize=15,linespacing=2,va='top')
    ax.text(.04,.15,tr('6条A配方读数','6 readings for A'),fontsize=13)
    ax.text(.38,.68,tr('计算：每个试样一个均值','Apply: specimen mean'),fontsize=13,weight='bold')
    ax.text(.38,.56,'A01   (2.0+2.2)/2 = 2.1\nA02   2.8/1 = 2.8\nA03   (3.0+3.2+3.4)/3 = 3.2',fontsize=12.5,linespacing=2.3,va='top')
    ax.text(.38,.18,tr('保留编号\n与有效读数数','Retain identifiers\nand valid reading counts'),fontsize=12,va='top')
    ax.text(.75,.68,tr('合并：试样汇总表','Combine: summaries'),fontsize=13,weight='bold')
    ax.text(.75,.56,'A01   2.1\nA02   2.8\nA03   3.2',fontsize=14,linespacing=1.6,va='top')
    ax.plot([.75,.96],[.30,.30],color='#9baeb7',lw=1)
    ax.text(.75,.25,tr('下一轮：按配方再分组','Next grouping: formulation'),fontsize=12)
    ax.text(.75,.16,'A: (2.1+2.8+3.2)/3 = 2.7',fontsize=12)
    save(fig,'split-apply-combine')

    fig,axes=plt.subplots(1,2,figsize=(12.5,5.5),layout='constrained')
    copies=range(1,7);curve=[]
    for k in copies:
        _,g,_=summarize(make_table(k));curve.append(g.loc[g.formulation=='A','q_rows'].iloc[0])
    axes[0].plot(list(copies),curve,'o-',lw=2.5,color=BLUE,label=tr('逐读数平均','Mean over rows'))
    axes[0].axhline(2.7,color=ORANGE,lw=2.2,label=tr('3个试样等权','3 equally weighted specimens'))
    axes[0].set(xticks=list(copies),xlabel=tr('A01两条记录的保留份数 k','Copies k of the two A01 records'),ylabel='A: q / g g⁻¹',ylim=(2.1,2.9),title=tr('a  复制记录改变权重','a  Copied records change weights'))
    axes[0].legend(frameon=False);axes[0].grid(alpha=.15)
    absent=make_table(missing=True);s,g,t=summarize(absent)
    counts=pd.DataFrame({'rows':s.rows.to_numpy(),'valid':s.valid.to_numpy()},index=s.specimen)
    im=axes[1].imshow(counts,cmap='Blues',vmin=0,vmax=3,aspect='auto')
    axes[1].set(xticks=[0,1],xticklabels=[tr('行数 size','Rows: size'),tr('有效数 count','Valid: count')],yticks=range(6),yticklabels=counts.index,title=tr('b  A02缺失时，行仍然存在','b  An A02 row remains when q is missing'))
    for i in range(6):
        for j in range(2):axes[1].text(j,i,int(counts.iloc[i,j]),ha='center',va='center',fontsize=19,color='white' if counts.iloc[i,j]>=2 else INK)
    cb=fig.colorbar(im,ax=axes[1],ticks=[0,1,2,3],shrink=.75);cb.set_label(tr('条数','Count'))
    save(fig,'copies-and-missing')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('results'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    table=make_table();specimens,groups,traced=summarize(table)
    # A pivot rearranges unique cells. It does not select or average duplicates.
    wide=table.pivot(index='specimen',columns='reading',values='q')
    assert abs(groups.loc[0,'q_rows']-83/30)<1e-12
    assert abs(groups.loc[0,'q_equal']-27/10)<1e-12
    assert abs(groups.loc[1,'q_rows']-123/50)<1e-12
    assert abs(groups.loc[1,'q_equal']-38/15)<1e-12
    assert np.allclose(traced.groupby('specimen').within_specimen.sum(),0)
    _,missing_groups,_=summarize(make_table(missing=True))
    _,copied_groups,_=summarize(make_table(copies=6))
    for name,data in [('readings',table),('specimens',specimens),('formulations',groups),('trace',traced)]:data.to_csv(args.output/f'{name}.csv',index=False)
    wide.to_csv(args.output/'wide.csv')
    summary={'versions':{'pandas':pd.__version__,'numpy':np.__version__},'rows':len(table),'specimens':len(specimens),'A_row_mean':float(groups.q_rows.iloc[0]),'A_equal_mean':float(groups.q_equal.iloc[0]),'B_row_mean':float(groups.q_rows.iloc[1]),'B_equal_mean':float(groups.q_equal.iloc[1]),'A_missing_equal':float(missing_groups.q_equal.iloc[0]),'A_missing_valid_specimens':int(missing_groups.valid_specimens.iloc[0]),'A_six_copies_row_mean':float(copied_groups.q_rows.iloc[0]),'A_six_copies_equal_mean':float(copied_groups.q_equal.iloc[0]),'A_specimen_sd':float(groups.sd_specimens.iloc[0])}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    plot_all(table,specimens,groups,args.output,args.language)
    print(json.dumps(summary))


if __name__=='__main__':main()
```

运行后，readings.csv 保存十一行输入，specimens.csv 保存六行试样摘要，formulations.csv 保存两行配方结果，trace.csv 保留每条读数及其组内偏离，wide.csv 展示试样与读取序号构成的宽表。数值摘要中，A 的两种均值分别约为 2.7667 和 2.7000，B 则为 2.4600 和 2.5333。程序还核对组内偏离之和接近零，并用明确的分数检验主要平均值。先打开这几张表观察行数和列名怎样变化，再返回函数阅读，每一步操作就都有具体对象。

如果把例子改成自己的数据，应先整理列名和单位，并确认试样编号在全表中的唯一范围。读取序号可以重复出现，因为不同试样都有“第 1 次”；试样编号若在不同日期或批次重复使用，就要与相应批次共同构成键。保存中间表还有一个实际好处：合作方可以在不重新运行全部绘图的情况下，核对某个试样均值用了哪些读数。图注中的 n 也可以从明确的 valid_specimens 列获得，而不需要在画图时猜测。

## 改动记录结构，观察谁改变、谁保持不变

下面的实验台保留相同的六块试样。先选择一块试样，观察它的读数、均值以及在配方内的两种权重；然后增加 A01 两条已有记录的保留份数。每一份都包含 2.0 和 2.2，因此 A01 的试样均值保持不变，左图的点会按记录顺序展开，权重条和 A 的逐读数均值同时改变。右侧曲线画出从一份到六份的全部计算，并标记当前选择，方便把一次操作放回完整趋势中理解。

### 从读数追踪平均值

增加的是A01已有记录的副本，每份含2.0与2.2；选中试样后对照两种权重。

[Figure: 试样读数与均值](https://ml-biomat.com/tutorials/python-scientific/p12/#P12-readings)

[Figure: 两种配方内权重](https://ml-biomat.com/tutorials/python-scientific/p12/#P12-weights)

[Figure: 记录份数与两种平均](https://ml-biomat.com/tutorials/python-scientific/p12/#P12-curve)

蓝色按有效读数等权；橙色按有有效均值的试样等权。空值保持缺失，副本不会增加独立试样数。

将份数调到六，你会看到 A01 在 A 的十六条有效读数中占十二条，权重变成 0.75；在试样等权路径中，它仍占三分之一。再勾选 A02 缺失，A 只有两块试样具有有效均值，等权路径中 A01 与 A03 各占一半，配方均值成为 2.65。表格同时保留 A02 的一行记录和零条有效数值，帮助你区分“试样还在登记表中”与“试样为当前均值提供了有效信息”。重置后可以从原始十一条记录重新开始比较。

把这个练习带回实际研究时，可以在结果句里明确写出比较层次，例如“先对每块试样的技术读数取均值，再对每种配方的三个独立试样等权平均”。这句话同时说明计算对象、运算顺序和试样数量。pandas 让这种规则落实为可重复执行的程序；原始记录、中间表与图中的点共同保留它的含义。下一步把配方、批次与其他测量表连接起来时，我们继续使用这些身份键，确保新增信息进入了正确的试样。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P12.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pandas: Group by — split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html)

   分组键、缺失标签、聚合与转换的官方指南。

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
2. [pandas: Summary statistics](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html)

   按明确数值列汇总，并区分size与count。

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
3. [pandas: GroupBy.aggregate](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.aggregate.html)

   带名字的输出聚合接口。

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
4. [pandas: GroupBy.transform](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.transform.html)

   为原始各行返回对齐的组内计算结果。

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
5. [pandas: DataFrame.pivot](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html)

   唯一单元格与不隐式聚合的透视规则。

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
6. [Wickham (2011): The Split-Apply-Combine Strategy for Data Analysis](https://www.jstatsoft.org/article/view/v040i01)

   计算组织方式的原作者论文；本节图与数据为原创。

   JSS original article; historical reference, no reproduced figure or text.
