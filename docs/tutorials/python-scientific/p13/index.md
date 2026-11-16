# 把多张表准确地拼在一起

Source: https://ml-biomat.com/tutorials/python-scientific/p13/
Language: zh-CN

从样品身份追踪到统计权重，理解concat、merge和每一次匹配如何改变结果。

## 一次测量的完整信息，常常分散在几张表里

一台仪器保存应力数值，样品登记表保存配方，另一份记录保存制备批次。研究“哪一种配方的应力更高”时，需要把这些信息接起来。手工把几列复制到一起，看起来很快，实际却要求所有表的行顺序始终相同；一旦某个样品测了两次、某张表少了一行，后面的数值就可能配错身份。pandas提供按字段匹配的连接操作，使每次测量可以找到对应的样品信息。本篇将用两张小表追踪每一次配对，再观察一次重复匹配怎样悄悄改变平均值。

教学测量表有六条记录。R01与R02来自样品S01，应力为12和14 kPa；R03来自S02，为18 kPa；R04与R05来自S03，为21和23 kPa；R06来自S04，为16 kPa。R开头的是测量记录编号，S开头的是样品编号，两者回答不同问题。一个样品可以有多次测量，所以样品编号允许在测量表中重复；每次测量仍有自己的记录编号，便于把计算结果追溯到原来的一行。

样品信息表使用另一种粒度：每行描述一个样品，记录它所属的配方。S01与S03属于A，S02与S05属于B。这里故意保留两个不完全对应的情况：S04有测量却缺少配方登记，S05有登记却尚无测量。这些差异会帮助我们理解不同连接规则。表格中的“粒度”就是一行究竟代表什么；先讲清它，才能判断连接以后多出来的行是合理的一对多关系，还是同一条观测被重复使用。

可以把两张表想成实验记录本和样品名册。记录本中的每次测量通过样品编号找到名册中的描述，名册重新排序不会改变对应关系。这种做法同样适用于患者与检验、设备与传感器读数、分子编号与性质、模拟任务与输出文件。接下来不仅要把表拼好，还要保留未匹配对象、检查键是否唯一，并弄清结果中的每一行会怎样进入统计计算。

## 从关系数据思想理解“按键连接”

1970年，E. F. Codd提出关系数据模型，把数据的逻辑组织与底层存储安排分开。IBM对这段历史的回顾强调，使用者应能按信息之间的关系访问数据，而不必依赖它们在机器里的具体存放位置。今天在两张表之间按样品编号建立对应，就是这种思想的一种直观应用。我们关心的是“这条记录属于哪个样品”，而不是“它现在碰巧排在第几行”。图中右表故意采用S03、S01、S05、S02的顺序，连接仍能把相同身份配在一起。

![关系数据的核心思想用本例两张表表示：左边一行是一次测量，右边一行是一个样品；箭头只连接相同样品键。右表顺序故意打乱，S04只有测量，S05只有样品信息。](https://ml-biomat.com/static/tutorials/python-scientific/figures/76a04a2bfecdace70cd90c63.svg?v=76a04a2bfecd)

图 1关系数据的核心思想用本例两张表表示：左边一行是一次测量，右边一行是一个样品；箭头只连接相同样品键。右表顺序故意打乱，S04只有测量，S05只有样品信息。

用于匹配的字段叫作键。本例的键是`sample`列，其中的S01、S02等值是标识符。它们看上去含有数字，却不是适合求平均的测量量：S01加S02没有样品科学含义。把编号保存为字符串，能够保留前导零，也能避免软件自动把它改写成另一种表示。键的作用是区分身份，所以空格、大小写和字符编码都会影响是否相等。清理键时应根据登记规则统一写法，并保留足以检查原始记录的字段。

键的范围也必须明确。若每一批实验都从S01重新编号，单独的样品号就无法在全部数据中唯一确定样品。可以同时使用`batch`和`sample`两列作为复合键，相当于用“批次名加样品名”寻找对象。类似地，一个文件里的第10行与另一个文件里的第10行不一定是同一条记录；行号通常描述当前排列位置，而记录编号描述身份。排序、筛选或重建索引以后，身份字段仍应保留。

在pandas里，`DataFrame`是一张带行标签和列名的表。连接可以使用显式列，也可以使用索引；初学时把身份保存在看得见的列中，再用`on="sample"`指定匹配，通常更便于核对。如果两边的键列名称不同，可以分别写`left_on`与`right_on`，但两个字段必须表示同一种身份。名称相同并不自动证明含义相同，含义相同也不要求名称完全一致。

## 同名样品来自不同批次时，把范围写进键

考虑一个独立的小例子：B01批次的S01测得10 kPa，B02批次的S01测得30 kPa。登记表说明B01的S01属于配方A，B02的S01属于配方B。如果只按S01连接，每条测量都会找到两条同名登记，于是出现四个组合，其中包含“B01的测量配上B02的配方”。两个文件各自都可能整理得很清楚，问题出在合并时把编号的使用范围丢掉了。把批次与样品号一起作为键，两个原本不同的实验对象才会保持分开。

`on=["batch", "sample"]`表示两个字段必须同时相等。程序会把B01/S01的10 kPa配到A，把B02/S01的30 kPa配到B，结果回到两行。完整脚本包含这个小例子，并把正确结果写入`composite-key.csv`。可以交换登记表的行顺序再检查结果；由于配对使用字段值，样品身份保持不变。复合键也可以包含测试阶段、位置或测量轮次，但每增加一列，都应能解释它为什么是区分对象所必需的信息。

键的组成与研究粒度相互决定。若同一样品在处理前后各测一次，样品号适合关联其固定属性，而“样品号加阶段”适合把处理前后的两种记录分别找到。若两台仪器对同一样品同时测量，仪器编号可能是观测身份的一部分，却不是样品身份的一部分。先确定要连接的是样品、一次测量还是某个处理阶段，再选择键，可以避免把所有字段一股脑加入匹配条件。过少的键会把不同对象混在一起，过多而含义不一致的键则会把本来属于同一对象的记录拆开。

实际检查时可以直接查看复合键上的重复情况：`duplicated(["batch", "sample"], keep=False)`标出所有重复组合，便于把相关行一起取出核对。`keep=False`让第一次出现也被标出，避免只看后续重复而漏掉比较对象。这个检查是否应当发现重复，仍取决于表的粒度：样品登记表通常要求组合唯一，测量表则可能允许同一样品有多次记录。身份规则写清以后，重复检查才能成为有意义的实验整理工具。

## 增加观测记录，与补充样品属性，是两种操作

`concat`适合把结构相同的观测表沿行方向接起来。比如第二批测量又得到R07、R08，它们仍然包含记录号、样品号和应力三列。把两张表放进一个列表交给`pd.concat`，就能得到八条记录。`ignore_index=True`会重新生成从0开始的行标签，避免两个输入表都从0编号造成标签重复；原有的`record`列仍保存真正的测量身份。重新编号行标签与给实验记录重新命名，是两件不同的事情。

纵向拼接会按列名对齐字段，而不是只看第几列。假如后一张表把应力列写成`stress_MPa`，前一张使用`stress_kPa`，直接拼接会出现两列，并在各自缺失的位置留下空值。这个结果提示需要先统一单位与字段定义。如果两列都叫`stress`，但实际一列为MPa、一列为kPa，软件会把数值放入同一列，单位差异反而更难发现。因此，同名列应在拼接之前具有相同含义和单位。

`merge`处理另一种任务：给已有观测补充对应对象的属性。本篇希望为每一次测量找到样品配方，这时需要按样品编号连接。样品S01的两次测量都应拿到配方A，原本的两次观测仍各占一行。把两张表简单沿列方向`concat`，则主要按照行标签对齐，不会自动理解样品编号。因此，“增加新的测量”与“为测量补充属性”虽然都能让表变大，使用的对应关系不同。

当需要连续读取许多小文件时，可以先把各文件读成表，加入有意义的批次字段，再收集到列表中一次拼接。这样既保存每条记录的实验归属，也减少反复创建中间表。拼接完成后检查记录号是否唯一，检查列名与数据类型是否符合预期，再进入连接步骤。文件数增加并没有改变最基本的问题：每一行代表什么，怎样识别它，与另一张表中的哪一行有关。

## 决定未匹配对象应该留在哪里

把测量表写在左边、样品表写在右边以后，`how`决定哪些键进入结果。`inner`只保留两边都有对应的记录；本例留下S01、S02、S03，共五次测量。`left`保留左表全部测量，并尽可能补上右表属性，因此得到六行，S04的配方为空。`outer`进一步保留两边出现过的全部键，因此还会出现S05这一行，它有配方B，但没有测量编号和应力，共七行。

选择规则需要联系问题。若任务是整理全部已经发生的测量，左连接可以保留缺少登记信息的S04，使后续补登记有明确对象。若问题限定为“已知配方的测量如何比较”，可以在完成匹配检查后明确筛选这些记录。外连接则适合核对样品名册与测量记录是否齐全，同时发现“测了但没登记”和“登记了但没测”两类情况。规则本身没有统一优先级，它描述的是本次分析准备保留哪些对象。

### 把连接关系和检查要求一起写出

这里的measurements与specimens由下面完整脚本中的make_tables建立。m:1允许左边多个观测对应右边一个样品；indicator保留匹配状态。

```
joined = measurements.merge(
    specimens, on="sample", how="left",
    validate="m:1", indicator=True,
)
missing = joined.loc[joined["_merge"].eq("left_only")]
print(joined)
print(missing[["record", "sample"]])
```

`indicator=True`把匹配状态写进`_merge`列。`both`表示两边都找到了相应键，`left_only`表示只有左表记录，`right_only`表示只有右表信息。可以据此生成待补字段表，并把它与统计结果分开保存。缺失配方与配方值为零不是同一种情况；缺失应力与应力为0 kPa也不相同。将空值填成零会把“没有观测”变成一次具体的零值测量，直接影响平均值和图形。

![同一数据的三种连接规则。键唯一时，inner、left、outer分别得到5、6、7行；S03元数据复制后分别得到7、8、9行。颜色说明这些行来自两侧都匹配、仅左侧或仅右侧。](https://ml-biomat.com/static/tutorials/python-scientific/figures/fcd1fea488752fac713f4afd.svg?v=fcd1fea48875)

图 2同一数据的三种连接规则。键唯一时，inner、left、outer分别得到5、6、7行；S03元数据复制后分别得到7、8、9行。颜色说明这些行来自两侧都匹配、仅左侧或仅右侧。

合并时还应主动指定键。若省略`on`，pandas可能把两表同名列共同用作匹配条件，后续多出一个同名字段就可能改变结果。对于两边都含有的非键列，例如都叫`temperature`，可用后缀保留各自角色，再核对它们是否一致。复制一份温度信息并不能说明哪个值优先；如果一边是制备温度、另一边是测试温度，给它们明确的列名才是正确的整理方式。

## 重复键怎样把两条测量变成四条结果

本例允许测量表中的样品键重复，因为同一样品可以测量多次；右边的样品表则要求每个样品只有一条配方信息。这种关系称为多对一，用`validate="m:1"`表达。m表示可以有多条，1表示该侧键必须唯一。验证会在发现不符合关系的键时给出错误，让程序停在出现身份歧义的位置。它把“右表应该是一份唯一名册”这项理解直接写进可执行的连接操作。

如果右表中的S03被意外复制一次，连接会发生什么？R04能与第一条S03匹配，也能与第二条S03匹配；R05同样有两种匹配。因此，两次测量会生成四条结果行。软件执行的是相同键下所有左右组合的配对。每一条结果都符合相等规则，但它们并不代表四次独立测量。看见结果行数增加时，应沿记录编号回查配对过程，而不是把新增行直接当成新增数据。

$$
N_k=m_k n_k
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 一个具体键值，例如样品S03；标识符，无单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/db7985d73352cce0c498191f.svg) | 左表中键为k的行数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | 右表中键为k的行数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/ad7b34e7b5b399c686f1e5e8.svg) | 该键产生的成功匹配行数，无量纲整数 |

相同键下，每一条左记录会与每一条右记录组成一对。S03左边有2次测量，右边有1条样品信息，得到2×1=2行；右边误复制成2行后，得到2×2=4行。此式计算成功匹配；left或outer额外保留的未匹配行需另计。

多对多关系也有合理用途。例如，一张表列出每个样品的多种成分，另一张表列出它的多次测量，按样品连接后可以把每次测量分别关联到每种成分。此时结果一行表示“某次测量与某种成分的组合”，已经不再是一行一次测量。后续统计要尊重新的粒度。如果想要测量层面的平均值，应回到唯一记录层面；如果想要分析成分关联，就需要明确每次测量在不同成分组中的角色。

发现重复以后，也不宜立即对整张表调用去重来消除报错。两条样品信息可能完全相同，可能存在拼写差异，也可能描述不同制备批次或不同版本。先检查重复键对应的全部字段，判断应该合并同义记录、补充复合键，还是按明确的版本规则选择。只有关系已经解释清楚，删掉某一行才有依据。验证的意义是把需要澄清的身份关系显现出来，而不仅是让程序顺利运行到底。

## 行数变化会进入平均值的计算

配方A原本包含R01、R02、R04、R05四条测量，应力为12、14、21、23 kPa，平均值是17.5 kPa。右表S03重复以后，21和23这两个值分别出现两次，按合并结果的每一行求平均，便得到19 kPa。所有原始应力数值都没有被改写，平均值却发生了变化。原因是连接改变了各条观测进入计算的次数，相当于给S03的测量增加了权重。

$$
\bar y_w=\frac{\sum_{i=1}^{n}w_i y_i}{\sum_{i=1}^{n}w_i}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 原始测量记录序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 原始测量记录数，无量纲；本算例4 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i条应力记录，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | 第i条原始记录在合并结果中出现的次数，无量纲非负整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/a1a67b1c7514ecc0a21130b6.svg) | 按结果行计算的应力平均值，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对所有原始记录把各项相加 |

配方A的观测为12、14、21、23 kPa。每条出现一次时，均值为70/4=17.5 kPa。重复匹配使次数变为1、1、2、2，均值变为(12+14+42+46)/6=19 kPa。合并本身没有创造新测量，却改变了各记录进入平均值的次数。至少有一条记录被保留时分母为正。

![配方A有四条原始应力记录。重复S03元数据使R04与R05各出现两次，按结果行计算的均值从17.5变成19 kPa。左图横线是均值，右图使用从零开始的同单位柱高；原始测量值始终没有改变。](https://ml-biomat.com/static/tutorials/python-scientific/figures/2fcef99551a4823ec2e3b08e.svg?v=2fcef99551a4)

图 3配方A有四条原始应力记录。重复S03元数据使R04与R05各出现两次，按结果行计算的均值从17.5变成19 kPa。左图横线是均值，右图使用从零开始的同单位柱高；原始测量值始终没有改变。

这里的17.5 kPa也是一个具有明确身份的统计量：它是A组四次测量的平均值。若两个样品的测量次数不同，逐行平均会让测量次数较多的样品贡献更大；先求每个样品的平均，再在样品之间平均，则让每个样品各贡献一次。两者可以用于不同问题。意外重复连接所带来的额外次数既不是新的测量次数，也不是预先设计的样品权重，所以需要在统计之前识别。

检查连接结果时，行数和唯一记录数应一起看。唯一记录数告诉我们保留了多少条不同测量，行数告诉我们连接展开了多少组合。左连接从六行变成八行，唯一记录数却仍为六，就提示部分记录出现了多次。对关键字段执行`value_counts`可以进一步定位重复发生在哪些键；按记录号计数则能检查究竟是哪几次观测获得了多重匹配。把这两层计数保存下来，能让后续统计更容易追溯。

未匹配记录同样影响分析对象。内连接排除S04以后，得到的是身份已匹配的五次测量，而不是原来的全部六次测量。如果缺登记恰好与某类实验失败或某个批次有关，保留下来的数据构成也会改变。记录匹配率、列出遗漏身份、补齐可追溯的登记信息，是研究问题的一部分。完成这些工作后，平均值才对应一组清楚定义的观测。

## 用交互追踪每条配对线的去向

下面的实验同时展示输入对应关系、完整连接结果和统计变化。连接图中的每条线代表一个成功配对；选中的测量以加粗连线和表格底色标出。切换`inner`、`left`、`outer`时，相同键的成功配对规则保持不变，变化的是两边未匹配对象是否进入结果。图里的原始输入始终保留，便于看清某条记录是被规则排除，还是输入中本来没有它。

## 沿着一条测量追踪合并结果

选择连接规则，或复制S03的样品信息。连接图、完整结果表和统计图一起更新。选中R04或R05，可以看到同一条测量在重复键条件下产生两条结果行。

[Figure: 测量记录与样品信息之间的对应线](https://ml-biomat.com/tutorials/python-scientific/p13/#P13-links)

| 记录 | 样品 | 应力 / kPa | 配方 | 匹配状态 |
| --- | --- | --- | --- | --- |

[Figure: 连接结果行数和配方A平均值](https://ml-biomat.com/tutorials/python-scientific/p13/#P13-summary-plot)

先选择R04，保持左连接，然后勾选复制S03信息。R04会出现两条加粗线，表中也有两条对应结果；R05发生相同变化。此时上方原始测量仍然只有六次，下方结果行数变成八，配方A均值从17.5升到19 kPa。再切换到外连接，会增加一条S05信息，但没有新的应力观测，所以A组均值保持19 kPa。不同视图一起变化，能够区分“增加未测样品信息”和“重复已有测量”这两种完全不同的增行原因。

实验也显示`m:1`关系检查的结果。重复开关开启时，右表S03有两个相同键，原生pandas会对这一约定报告错误；页面仍展开配对，是为了让重复的来源可见。实际分析中应先解决该身份关系，再生成进入统计的正式连接表。重置会返回唯一右键、左连接和R04追踪状态，便于重新核对六条测量对应的信息。

## 完整脚本如何保存可检查的结果

完整例子直接构造两张教学表，用`concat`追加两次测量，也用它构造一条刻意重复的S03样品信息。随后，程序对键唯一与键重复两种输入分别执行三种连接，保存六份CSV，并记录成功匹配数、两侧单独出现的行数、唯一测量数和A组平均值。正式的多对一连接启用`validate`；另一次调用专门确认重复键会产生`MergeError`。这两部分分工明确：一部分计算结果，一部分检查数据关系的约定。

### 完整例子：合并、检查、计数与统计权重

真实调用pandas的concat、merge、groupby，生成每种连接结果CSV和三幅图。特意构造的重复键由MergeError检查捕获。

```
"""Join defined teaching tables and inspect record identity and statistical weight."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch,Rectangle

BLUE,RED,INK,GRAY='#28658c','#b64a35','#202e39','#71808b'


def make_tables():
    measurements=pd.DataFrame({'record':['R01','R02','R03','R04','R05','R06'],
        'sample':['S01','S01','S02','S03','S03','S04'],
        'stress_kPa':[12.,14.,18.,21.,23.,16.]})
    specimens=pd.DataFrame({'sample':['S03','S01','S05','S02'],
                            'formulation':['A','A','B','B']})
    return measurements,specimens


def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    def tr(a,b):return a if language=='zh' else b
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'font.size':11,
        'axes.labelsize':12,'axes.titlesize':13,'axes.titleweight':'bold','axes.spines.top':False,
        'axes.spines.right':False,'text.color':INK,'svg.fonttype':'none','svg.hashsalt':'P13'})
    measurements,specimens=make_tables()
    duplicated=pd.concat([specimens,specimens.loc[specimens['sample'].eq('S03')]],ignore_index=True)
    measurements.to_csv(output/'measurements.csv',index=False)
    specimens.to_csv(output/'specimens.csv',index=False)
    duplicated.to_csv(output/'specimens-duplicate.csv',index=False)
    summary={'data_kind':'explicitly defined teaching tables','cases':{}}
    results={}
    for duplicate,metadata in [(False,specimens),(True,duplicated)]:
        for how in ['inner','left','outer']:
            name=f'{how}-'+('duplicate' if duplicate else 'unique')
            result=measurements.merge(metadata,on='sample',how=how,indicator=True,sort=True)
            result.to_csv(output/f'{name}.csv',index=False)
            counts=result['_merge'].value_counts().to_dict()
            group=result.groupby('formulation')['stress_kPa'].agg(['count','mean'])
            summary['cases'][name]={'rows':len(result),'unique_observations':int(result['record'].nunique()),
                'matched':int(counts.get('both',0)),'left_only':int(counts.get('left_only',0)),
                'right_only':int(counts.get('right_only',0)),
                'A_count':int(group.loc['A','count']),'A_mean_kPa':float(group.loc['A','mean'])}
            results[name]=result
    validated=measurements.merge(specimens,on='sample',how='left',validate='m:1',indicator=True)
    try:
        measurements.merge(duplicated,on='sample',how='left',validate='m:1')
    except pd.errors.MergeError:
        summary['duplicate_contract_rejected']=True
    else:
        raise AssertionError('A duplicated right key must fail m:1 validation')
    extra=pd.DataFrame({'record':['R07','R08'],'sample':['S02','S03'],'stress_kPa':[20.,22.]})
    appended=pd.concat([measurements,extra],ignore_index=True)
    assert appended['record'].is_unique
    appended.to_csv(output/'appended-measurements.csv',index=False)
    summary['appended_rows']=len(appended)
    batch_measurements=pd.DataFrame({'batch':['B01','B02'],'sample':['S01','S01'],
                                      'stress_kPa':[10.,30.]})
    batch_metadata=pd.DataFrame({'batch':['B02','B01'],'sample':['S01','S01'],
                                'formulation':['B','A']})
    composite=batch_measurements.merge(batch_metadata,on=['batch','sample'],validate='m:1')
    ambiguous=batch_measurements.merge(batch_metadata,on='sample')
    composite.to_csv(output/'composite-key.csv',index=False)
    summary['composite_key_rows']=len(composite)
    summary['sample_only_rows']=len(ambiguous)
    assert composite['formulation'].tolist()==['A','B']
    assert len(validated)==6
    assert summary['cases']['left-duplicate']['rows']==8
    assert summary['cases']['left-unique']['A_mean_kPa']==17.5
    assert summary['cases']['left-duplicate']['A_mean_kPa']==19.
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',metadata={'Date':None})
        fig.savefig(output/f'{name}-{language}.png',dpi=180)
        plt.close(fig)
    fig=plt.figure(figsize=(12,6.5));ax=fig.add_axes([.03,.1,.94,.75]);ax.set_axis_off();ax.set(xlim=(0,1),ylim=(0,1))
    fig.text(.06,.94,tr('记录靠身份对应，不依赖当前行号','Records match by identity, independently of row order'),fontsize=16,weight='bold')
    ax.text(.04,1,tr('测量表：一行一次测量','Measurements: one row per observation'),fontsize=12,weight='bold')
    ax.text(.65,1,tr('样品表：一行一个样品','Metadata: one row per sample'),fontsize=12,weight='bold')
    colors={'S01':BLUE,'S02':'#886a29','S03':RED,'S04':GRAY,'S05':GRAY}
    for i,row in measurements.iterrows():
        y=.86-i*.135
        ax.add_patch(Rectangle((.035,y-.045),.39,.09,fc='#f2f6f8',ec='none'))
        ax.text(.055,y,f"{row['record']}   {row['sample']}   {row['stress_kPa']:.0f} kPa",va='center',fontsize=12,color=colors[row['sample']])
        for j,target in specimens.iterrows():
            if row['sample']==target['sample']:
                ax.add_patch(FancyArrowPatch((.44,y),(.64,.82-j*.20),arrowstyle='->',mutation_scale=11,color=colors[row['sample']],alpha=.65))
    for j,row in specimens.iterrows():
        y=.82-j*.2
        ax.add_patch(Rectangle((.65,y-.055),.30,.11,fc='#f2f6f8',ec='none'))
        ax.text(.67,y,f"{row['sample']}   →   {row['formulation']}",va='center',fontsize=12,color=colors[row['sample']])
    fig.text(.06,.035,tr('关系数据思想：用字段值表达对应关系；物理存放次序可以改变。','Relational idea: field values specify correspondence while storage order can change.'),fontsize=11,color=GRAY)
    save(fig,'identity')
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),layout='constrained',sharey=True)
    for ax,suffix,title in zip(axes,['unique','duplicate'],[tr('样品键唯一','Unique sample keys'),tr('S03在样品表出现两次','S03 appears twice in metadata')]):
        bottom=np.zeros(3)
        for field,color,label in [('matched',BLUE,tr('成功对应','Matched')),('left_only',RED,tr('只有测量','Measurement only')),('right_only',GRAY,tr('只有样品信息','Metadata only'))]:
            values=np.array([summary['cases'][f'{how}-{suffix}'][field] for how in ['inner','left','outer']])
            ax.bar(np.arange(3),values,bottom=bottom,color=color,width=.55,label=label)
            for x,y,b in zip(np.arange(3),values,bottom):
                if y:ax.text(x,b+y/2,str(y),ha='center',va='center',color='white',weight='bold')
            bottom+=values
        ax.set(xticks=np.arange(3),xticklabels=['inner','left','outer'],ylim=(0,11),title=title)
        ax.legend(frameon=False,loc='upper left',fontsize=10)
    axes[0].set_ylabel(tr('合并结果行数','Rows in the merged result'))
    save(fig,'join-counts')
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.3,1]},layout='constrained')
    left=results['left-unique'];dup=results['left-duplicate'];labels=['R01','R02','R04','R05']
    values=np.array([12,14,21,23])
    counts=[int(dup['record'].eq(label).sum()) for label in labels]
    for i,(record,value,count) in enumerate(zip(labels,values,counts)):
        axes[0].scatter([0],[value],s=55,color=BLUE)
        axes[0].scatter([.9+ .14*j for j in range(count)],[value]*count,s=55,color=RED)
        axes[0].annotate(record,(0,value),xytext=(-28,3),textcoords='offset points',ha='right',fontsize=10)
    axes[0].hlines([17.5,19],[-.15,.75],[.15,1.2],colors=[BLUE,RED],lw=3)
    axes[0].set(xticks=[0,1],xticklabels=[tr('键唯一','Unique keys'),tr('S03重复','Duplicate S03')],
                xlim=(-.45,1.35),ylim=(9,25),ylabel=tr('配方A的应力记录 / kPa','Stress records in formulation A / kPa'),
                title=tr('同一条记录被重复计入','The same observation enters twice'))
    axes[1].bar([0,1],[17.5,19],color=[BLUE,RED],width=.55)
    axes[1].set(xticks=[0,1],xticklabels=[tr('4条结果行','4 result rows'),tr('6条结果行','6 result rows')],
                ylim=(0,24),ylabel=tr('按结果行计算的均值 / kPa','Mean across result rows / kPa'),
                title=tr('重复匹配改变了统计权重','Repeated matches change statistical weight'))
    for i,v in enumerate([17.5,19]):axes[1].text(i,v+.6,f'{v:g}',ha='center',fontsize=13)
    save(fig,'weights')
    summary['versions']={'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

运行输出中，键唯一的`inner`、`left`、`outer`行数依次为5、6、7；复制S03以后依次为7、8、9。左右两张表的未匹配对象仍分别是S04和S05，增加的两行来自S03的两次测量各多一次匹配。A组的结果行数从4变成6，均值从17.5变成19 kPa。`summary.json`把这些量写成有名字的字段，便于与图和CSV逐项对应。

读取自己的文件时，可以保留相同的检查顺序：先确定一行的含义和键字段，再统一编号类型与必要的单位，检查关键身份是否缺失，明确连接关系，执行带验证的连接，最后查看匹配状态和记录数。pandas对空键的匹配行为与一些数据库系统不同：两侧的空键可能互相匹配。样品身份未知时，将它们当成同一个样品会制造额外组合，因此应在连接前把缺键记录单独整理，而不是让一组空值承担身份识别的工作。

完成连接以后，表格的每个字段都应能回答“它描述谁、来自哪个对象、采用什么单位”。当观测逐渐增多，批次与时间也会进入身份定义。下一篇会沿时间整理多批记录，区分日历时间与实验经过时间，并观察不同时间分箱如何改变统计曲线。这里建立的原则继续适用：先确定对象和对应关系，再让表格操作为科学问题服务。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P13.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pandas: How to combine data from multiple tables](https://pandas.pydata.org/docs/getting_started/intro_tutorials/08_combine_dataframes.html)

   纵向拼接与按键连接的官方入门路径。

   pandas BSD-3; original case and figures
2. [pandas: Merge, join, concatenate and compare](https://pandas.pydata.org/docs/user_guide/merging.html)

   匹配数量、validate、indicator与同名列规则。

   pandas BSD-3 documentation
3. [IBM: The relational database](https://www.ibm.com/history/relational-database)

   Codd 1970年关系数据模型的计算史背景。

   Historical facts paraphrased; no source image or text reproduced
