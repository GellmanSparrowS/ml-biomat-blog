# 用列表和字典组织一组实验

Source: https://ml-biomat.com/tutorials/python-scientific/p03/
Language: zh-CN

让样品身份、条件和数值一起移动，理解排序、缺失与复制。

## 样品多起来以后，怎样让每个数字都找得到主人？

第一章只处理一块凝胶，干质量和湿质量放在两个变量里就能说清。现在准备比较水浴和盐水浴中的六个样品，每个样品还带有编号、处理条件和温度。如果继续写`dry_1`、`dry_2`、`wet_1`、`wet_2`，程序很快就会变成一长串需要人工配对的名字。更麻烦的是，某个样品少了一次称量，或者我们想按质量重新排列它们，原先靠位置记住的关系就可能错开。本章学习列表和字典，用结构把样品身份、条件和数值一起保存。

我们采用六条构造的教学记录。A01、A02、A03属于水浴，B01、B02、B03属于盐水浴；所有记录的温度字段均为25.0 °C。干质量分别为1.20、1.00、0.80、1.20、1.00、0.80 g，湿质量为4.80、3.40、2.80、3.60、缺失、2.32 g。这里的质量已经扣除容器。本例把干质量作为固定参照，增加的质量按所吸收液体计；盐水浴中吸收的液体包含水与溶解组分。编号前缀只是本例安排好的标签，实际分析仍读取明确的处理条件字段。这样，后续即使编号规则改变，也不会靠猜测字母来决定样品属于哪一组。

每条记录可以想成贴在样品袋上的一张完整标签：编号告诉我们是哪一件，条件告诉我们经历了什么，质量给出可计算的量。列表像一个有顺序的样品架，负责把多条记录收在一起；字典像标签上的“字段名—字段值”对应表，负责表达一条记录内部的含义。两者配合后，可以按位置取出第二条记录，也可以根据稳定的编号找到A02，取出的湿质量应是同一个3.40 g。

本章会从一个简单数字列表开始，逐步建立字典、记录列表和按编号查找的索引，再处理缺失值、排序与复制。最后的图和交互会展示一个容易被忽视的错误：同样的数字，只要干湿质量的对应关系改变，就会得到完全不同的吸液量。保持总数相同、数据没有报错，还不足以保证计算表达了原来的实验。

![六条教学记录的结构。位置索引与字段键分开表达：records\[1\]选记录，wet_g选字段；按编号索引能在重新排序后继续找到相同样品。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f0f7eacb76610ed404012f20.svg?v=f0f7eacb7661)

图 1六条教学记录的结构。位置索引与字段键分开表达：records[1]选记录，wet_g选字段；按编号索引能在重新排序后继续找到相同样品。

## 列表把一串值放在有顺序的位置上

列表用方括号包住多个值，值之间用逗号分隔，例如`dry_masses = [1.2, 1.0, 0.8]`。这里三个值依次对应三条记录。`len(dry_masses)`给出列表长度3，`dry_masses[0]`取出第一个值1.2。Python的位置索引从0开始，所以索引0、1、2分别对应人们口头说的第一、第二、第三项。可以把索引理解为从起点向后走了几步：第一项不需要移动，因而位置为0。

负索引从末尾开始找，`dry_masses[-1]`取最后一项0.8；切片`dry_masses[0:2]`则取得从位置0开始、到位置2之前的两项。右端不包含在结果中，这样`[0:2]`与`[2:3]`可以拼成原来的连续范围，而不会重复边界元素。切片得到的是一段序列，单个索引得到的是其中一个对象，两者在后续操作中扮演不同角色。刚开始使用时，把位置写在纸上，再预测取到哪些值，会比凭直觉记住冒号更牢靠。

### 位置、切片与添加

依次得到3；1.2与0.8；[1.2,1.0]；最后列表为[1.2,1.0,0.8,1.1]。

```
dry_masses = [1.2, 1.0, 0.8]
print(len(dry_masses))
print(dry_masses[0], dry_masses[-1])
print(dry_masses[0:2])
dry_masses.append(1.1)
print(dry_masses)
```

还要留意列表运算与数字运算的区别。两个列表相加会首尾连接，例如`[1.2, 1.0] + [0.8]`得到三个元素；列表乘以2会重复其中的序列，例如`[1.2, 1.0] * 2`得到四个元素，而不是把每个质量加倍。如果想改变每个数，需要逐项施加计算规则，后面的循环与NumPy数组会提供合适方式。遇到一个新对象时，先问运算符对这个对象代表什么，能够避免把熟悉的数学符号直接套进另一种数据结构。

列表可以改变。`dry_masses.append(1.1)`把一个新值添加到末尾；点号左边是要操作的对象，右边是它提供的操作名，括号里是这次操作需要的输入。这里的`append`会直接改变原列表，返回值为`None`，因此不要把它的返回值重新赋给列表名。`dry_masses[1] = 1.05`替换第二项，列表长度不变；删除一项则会让后面的项向前移动。位置描述的是当前排列，不能天然充当永远稳定的样品编号。

列表允许存放不同类型的值，但“可以存”与“这样组织容易理解”是两回事。把编号、质量和温度交错放进一个长列表，会迫使每次使用都记住哪个位置是什么。对于同一类连续观测，例如按时间记录的一组温度，列表非常自然；对于一个样品的多个不同字段，使用有名字的对应关系会更清楚。下一步引入字典，就是为了让字段含义直接出现在取值语句中，而不再依赖隐藏的位置约定。

## 字典让字段名称与值一起移动

字典用花括号表示，其中每一项由键、冒号和值组成。键是用来查找的名称，例如`"dry_g"`；值是对应内容，例如1.2。写成`sample["dry_g"]`，就取得这条样品记录的干质量。引号表明字段名是字符串，方括号中的键指定要找哪一项。一个字典可以同时容纳字符串、数字和缺失标记，因为它们分别描述不同字段。字段名中的单位后缀把上一章的单位约定保留在数据结构里。

### 按字段名读取和修改

先读取A01与4.8，未提供的note返回None；修改后wet_g为4.9。

```
sample = {"id": "A01", "bath": "water", "dry_g": 1.2, "wet_g": 4.8}
print(sample["id"], sample["wet_g"])
print(sample.get("note"))
sample["wet_g"] = 4.9
print(sample["wet_g"])
```

字典中的键是唯一的。给已经存在的键赋值，会更新对应值，而不是增加第二个同名字段。这带来方便，也要求我们认真处理编号：如果两条记录都用A01作为外层字典的键，后写入的值会覆盖先前的关联。因此在建立按编号查找的字典之前，先检查编号是否重复。`set(ids)`建立只保留不同编号的集合，把集合长度与原编号列表长度比较，就能发现是否有重复。集合在这里用于检查唯一性，不承担原始记录顺序的保存。

Python字典保留插入顺序，所以打印时通常能看到字段按建立时的顺序出现。不过按键查找依赖的是键的含义，不是它显示在第几行。`sample["wet_g"]`在字段排列改变后仍然读取湿质量。列表索引与字典键都写在方括号里，但查找规则不同：前者问“当前位置上是什么”，后者问“这个键对应什么”。把这两个问题分清，便能判断某个数据操作应该保持顺序，还是应该保持名称关联。

如果字段本来就应存在，直接使用方括号查找可以及时暴露拼写或结构问题；键不存在时会出现`KeyError`。`sample.get("note")`则适合读取确实可选的备注，缺少时返回默认值`None`。如果把必需的湿质量字段也随手设置默认0，程序可能继续运行，却把没有记录的称量解释成真实零质量。数据结构的选择与缺失处理是一件连贯的事：先决定哪些字段必须有，再决定缺失内容如何表达，最后决定哪些记录能够进入某个计算。

## 一条记录作为一个整体，排序才不会拆散实验

建立记录之前，还应定义“一条”究竟代表什么。本章一条记录对应一个样品的一次干湿称量配对，所以样品ID在表中唯一。如果同一个样品在10、20、30分钟分别称量，就会出现多次观测；可以给每次观测独立编号，并把样品ID与时间作为字段保存，也可以在样品记录中组织时间序列。此时样品ID重复并不一定是录入错误，是否允许重复取决于记录的单位。先确定这一层含义，唯一性检查才会检查正确的对象。

把六个样品字典放进一个列表，就得到记录列表`records`。`records[1]`是第二个字典，继续写`["wet_g"]`便取得它的湿质量；这个连续取值过程是先选样品，再选字段。也可以建立`by_id`字典，把每个样品编号映射到整条记录，随后用`by_id["A02"]["wet_g"]`直接查找。前者适合按当前顺序逐条处理，后者适合回答“某个样品现在在哪里”。两种结构可以引用同一批记录，并不一定复制一份新的实验数据。

排序时，应该让记录作为整体移动。按照干质量排列六条记录后，A01可能离开原来的列表位置，但它的编号、水浴条件、干质量和湿质量仍在同一个字典里。完整示例使用`sorted`产生排序后的新列表，原列表的顺序保留。排序键指定按哪个字段比较，这里是干质量；相同干质量的记录仍按原来的先后顺序出现。排序改变展示和遍历的次序，不应改变一条记录内部的科学含义。

看看只排序湿质量一列会怎样。三条水浴记录原先配对为1.20与4.80、1.00与3.40、0.80与2.80 g，吸液量分别为3.00、2.40、2.50 g/g。如果把湿质量单独升序排列，第一项变成2.80 g并与A01的1.20 g误配，最后一项4.80 g则与A03的0.80 g误配，结果变成约1.33、2.40、5.00 g/g。湿质量总和完全没变，每个数也仍像一个合理读数，但样品之间的关联已经被破坏。

![前三条水浴记录在不同排列下的关联。正确关联保留相同ID；单独排序湿质量改变配对，产生不同吸液量。Codd的历史问题与本例的稳定身份做法相连接。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8bd8ab1c3f89d0a6ddccf666.svg?v=8bd8ab1c3f89)

图 2前三条水浴记录在不同排列下的关联。正确关联保留相同ID；单独排序湿质量改变配对，产生不同吸液量。Codd的历史问题与本例的稳定身份做法相连接。

这一问题与数据管理史中的一个重要方向相通。E. F. Codd在1970年提出关系数据模型时，讨论了怎样让使用者对数据的操作不必紧紧依附机器内部的存储安排。我们在小例子中采取的做法是把编号与测量关系明确保存，使重新排列不会改变“哪个值属于哪个样品”。普通Python字典提供按键查找，记录列表提供组织和遍历；当需要更大的数据表、关联查询和长期维护时，还会用到专门的表格与数据库工具。当前最值得掌握的原则，是把稳定身份与临时位置区分开。

## 没有称量，与称得零克，进入计算的方式不同

B02的湿质量写成`None`，表示这次称量没有提供数值。它与数字0有完全不同的含义：0 g是一条具有数值内容的记录，可能提示称量对象或过程需要检查；`None`表示这里尚无可代入公式的量。若用0替代缺失湿质量，按本章公式会得到−1 g/g，相当于声称整个干样质量都消失了。一个数据整理上的随手替换，就会变成一个强烈但没有测量支持的物理结论。

本章的规则是保留B02整条记录，把它的吸液量结果也记作`None`，仅在计算需要湿质量的统计量时跳过这一项。这样，记录总数仍为6，有效吸液量数为5；水浴组有3个有效结果，盐水浴组有2个。图中明确保留B02的位置并标注未称量，读者可以看见缺失发生在哪个样品。缺失记录仍包含有用的编号、干质量和处理条件，不能因为某个计算用不上它，就把这些信息一起抹去。

$$
q_i=\frac{m_{w,i}-m_{d,i}}{m_{d,i}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样品标识对应的索引，无量纲；始终在同一样品内配对 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | 第i个样品按干质量归一化的吸液量，g/g，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/58390e8adf97ce97c3d618a2.svg) | 第i个样品的净湿质量，g；缺失时不计算q |
| ![Formula](https://ml-biomat.com/static/agent-math/5bb3742873949f3a3604d91d.svg) | 第i个样品的正净干质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/1526ecedf7893f4ee28503c0.svg) | 湿质量减干质量，得到本例中的留存液体质量 |

A02：(3.40−1.00)/1.00=2.40 g/g；B03：(2.32−0.80)/0.80=1.90 g/g。编号保持干湿质量属于同一样品；B02缺少湿质量，结果保留为None。

公式中的差值先取出每个样品留存的水，再除以该样品自己的干质量。A02的结果是(3.40−1.00)/1.00=2.40 g/g，B03的结果是(2.32−0.80)/0.80=1.90 g/g。代码使用`is None`检查缺失标记，而不是使用`if not value`这类把零、空字符串等情况一并当成假的判断。明确检查缺少的是什么，有助于让处理规则与记录含义一致。更复杂的表格缺失值会在pandas章节展开，这里先把最基本的区别建立稳固。

在进入计算前，程序还检查干质量是否为正，以及本例干物质质量保持不变的吸液设定下湿质量是否小于干质量。这些条件直接来自质量对象和公式分母。处理缺失与验证有效范围是两种不同操作：前者说明没有提供某个值，后者说明已提供的值是否满足当前计算条件。保持原始字段、另建结果字段，可以让这两个过程都看得清楚，并为以后更换分析规则留下可重新计算的原始记录。

## 汇总时保留样品点与有效计数

六条记录整理好后，最容易想做的是比较两组平均吸液量。但在计算之前，先把每个样品画出来，能看见组内差异和缺失位置。水浴组的三个值为3.00、2.40、2.50 g/g；盐水浴组的两个有效值为2.00、1.90 g/g。图中的每个点仍带着样品身份，组别用颜色区分；右侧的平均线则把这几个点汇总成一个代表值，同时显示进入平均的有效数量。一个均值不能替代构成它的记录。

$$
\bar q_G=\frac{1}{n_G}\sum_{i\in G_{\mathrm{valid}}}q_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 所选处理组，如water或saline；组名，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a91f85a3669211aaa75489f7.svg) | 该组中具有有效吸液量的样品集合 |
| ![Formula](https://ml-biomat.com/static/agent-math/cf52d0d51f7a704e935d0e7c.svg) | 有效样品数，为正整数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | 样品i的吸液量，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/af6a93670140117cb6d2d5f5.svg) | 每个有效样品等权的组平均吸液量，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/99c8b956831093e4e1e9a7c9.svg) | Σ表示逐个相加；∈表示索引属于有效样品集合 |

水浴组(3.00+2.40+2.50)/3=2.6333… g/g；盐水浴组(2.00+1.90)/2=1.95 g/g。没有有效结果时，均值应保留缺失，不能把空集合除以零。

这里采用每个有效样品等权的算术平均，水浴组为(3.00+2.40+2.50)/3≈2.6333 g/g，盐水浴组为(2.00+1.90)/2=1.95 g/g。分母使用有效结果数，而不是预先计划的样品数。若把盐水浴组的两个结果之和仍除以3，就等价于偷偷添加一个零结果，平均值会降低为1.30 g/g。公开分母和有效计数，使读者能够直接复算，而不必猜测缺失记录究竟怎样进入了汇总。

![左侧保留每个样品与缺失位置，右侧给出各组的有效数和等权样品均值。数据为构造例子，点位由脚本实际计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/32fd5d73f3e5197c450eec39.svg?v=32fd5d73f3e5)

图 3左侧保留每个样品与缺失位置，右侧给出各组的有效数和等权样品均值。数据为构造例子，点位由脚本实际计算。

当记录增加时，字段的一致性也需要维护。`"water"`、`"Water"`和`"water "`是三个不同字符串，最后一个还带有空格；按文字分组时，它们会被当成不同条件。可以在读取阶段统一约定的大小写和空格处理，并保留真正不同的实验条件。温度为25与温度字段缺失也应分别表达。把清理规则集中应用在输入边界，比在每次求平均时临时修补更容易看清数据经历了什么变化。

每个样品的比值平均，还不同于先把各样品质量相加再计算一个总体比值。后一种操作会让干质量较大的样品贡献更多权重，回答的是整批干材料合计对应多少水。本章选择等权样品平均，是为了练习逐条记录计算后再分组汇总；更详细的权重问题将在[第十二章](https://ml-biomat.com/tutorials/python-scientific/p12/)讨论。把汇总的对象说清楚，可以防止一个熟悉的“平均”符号掩盖了实际比较单位。

这组教学记录的用途是演示结构与计算规则。图上两组结果不同，说明在这些给定输入下怎样得到不同汇总；如果要在真实研究中比较处理条件，还需要相应的实验设计、足够的独立样品和测量说明。数据结构应为这些信息保留位置，例如批次、时间和处理浓度。先让每个数有明确身份，再逐步增加所需字段，能够使后来的统计分析建立在可以追踪的实验对象上。

## 完整代码：从原始记录到可检查的结果

下面的脚本把六条构造记录直接写在开头，不需要联网获取数据。它先检查编号唯一性，建立按编号查找的字典，然后逐条计算吸液量，并分别保存原始记录和带结果的记录。`for record in records`表示依次取出列表中的每条记录，缩进语句对当前记录执行；`if`根据条件选择处理分支。下一章会详细讲循环与函数，本章先把它们读作“对每条记录应用同一规则”，注意输入和结果怎样保持联系。

### 完整记录分析与绘图

记录与计算使用Python内置结构，绘图使用Matplotlib。

```
"""Keep specimen identity attached to values while organizing records."""
from pathlib import Path
import argparse
import json
import math
import copy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    # Net specimen masses in grams; constructed teaching records.
    records=[
        {"id":"A01","bath":"water","dry_g":1.2,"wet_g":4.8,"temperature_C":25.0},
        {"id":"A02","bath":"water","dry_g":1.0,"wet_g":3.4,"temperature_C":25.0},
        {"id":"A03","bath":"water","dry_g":0.8,"wet_g":2.8,"temperature_C":25.0},
        {"id":"B01","bath":"saline","dry_g":1.2,"wet_g":3.6,"temperature_C":25.0},
        {"id":"B02","bath":"saline","dry_g":1.0,"wet_g":None,"temperature_C":25.0},
        {"id":"B03","bath":"saline","dry_g":0.8,"wet_g":2.32,"temperature_C":25.0},
    ]
    ids=[record['id'] for record in records]
    if len(set(ids))!=len(ids):raise ValueError("Specimen identifiers must be unique.")
    by_id={record['id']:record for record in records}
    processed=[]
    for record in records:
        if record['dry_g']<=0:raise ValueError("Dry mass must be positive.")
        item=record.copy()
        if record['wet_g'] is None:
            item['uptake_g_per_g']=None
        else:
            if record['wet_g']<record['dry_g']:raise ValueError("Check uptake mass accounting.")
            item['uptake_g_per_g']=(record['wet_g']-record['dry_g'])/record['dry_g']
        processed.append(item)
    groups={}
    for bath in ['water','saline']:
        all_rows=[r for r in processed if r['bath']==bath]
        values=[r['uptake_g_per_g'] for r in all_rows if r['uptake_g_per_g'] is not None]
        groups[bath]={'record_count':len(all_rows),'valid_count':len(values),'mean_uptake':math.fsum(values)/len(values) if values else None}
    ordered=sorted(records,key=lambda row:row['dry_g'])
    ordered_lookup={record['id']:record for record in ordered}
    assert ordered_lookup['A01']==by_id['A01']
    # Assignment shares an object; deepcopy provides independent nested records.
    alias=records
    independent=copy.deepcopy(records)
    independent[0]['dry_g']=9.0
    assert records[0]['dry_g']==1.2 and alias is records

    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ['Noto Sans CJK SC','Microsoft YaHei','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans'],'font.size':12,'axes.titlesize':15,'axes.titleweight':'bold','svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36','axes.labelcolor':'#172b36','axes.spines.top':False,'axes.spines.right':False})
    ink,blue,red,green='#172b36','#28648a','#b85336','#467a62'
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12,7),layout='constrained');ax=fig.add_subplot();ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.1,6.6,tr('a  列表保留记录顺序，字典保留字段名称','a  A list orders records; dictionaries name their fields'),fontsize=17,weight='bold')
    cols=[.2,1.4,3.3,5.1,7.1,9.3]; widths=[1,1.7,1.6,1.7,1.9,2.4]
    headers=[tr('位置','Position'),'id','bath','dry_g','wet_g','temperature_C']
    for x,label in zip(cols,headers):ax.text(x,5.95,label,fontsize=13,weight='bold')
    for i,r in enumerate(records):
        y=5.05-i*.62
        vals=[str(i),r['id'],r['bath'],f"{r['dry_g']:.2f}",'None' if r['wet_g'] is None else f"{r['wet_g']:.2f}",f"{r['temperature_C']:.1f}"]
        for j,(x,w,val) in enumerate(zip(cols,widths,vals)):
            ax.add_patch(Rectangle((x-.05,y-.13),w,.5,facecolor=red if i==1 else blue,alpha=.13 if i==1 else .045,edgecolor='#cad2d0',lw=.6))
            ax.text(x+.05,y+.03,val,fontsize=13,color=red if val=='None' else ink)
    ax.text(.2,.85,'records[1]["wet_g"] → 3.40 g',fontsize=19,color=red)
    ax.text(6.0,.85,'by_id["A02"]["wet_g"] → 3.40 g',fontsize=17,color=blue)
    ax.text(.2,.2,tr('None表示缺少该次称量；0.00表示称量值为零。两者参与计算的规则不同。','None marks an absent weighing; 0.00 is a numerical reading. They require different calculations.'),fontsize=12)
    save(fig,'record-anatomy')

    fig=plt.figure(figsize=(12,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.1,1.2])
    for panel,wrong in enumerate([False,True]):
        ax=fig.add_subplot(gs[0,panel]);ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
        ax.set_title(tr('a  排序整条记录：身份保持','a  Sort whole records: preserve identity') if not wrong else tr('b  单独排序一列：配对改变','b  Sort one column alone: change pairing'),loc='left')
        order=[2,1,0] if not wrong else [0,1,2]
        left=['A01 | 1.20 g','A02 | 1.00 g','A03 | 0.80 g']; right=['A03 | 2.80 g','A02 | 3.40 g','A01 | 4.80 g']
        for i in range(3):
            y=.78-i*.28;ax.text(.02,y,left[i],fontsize=13);ax.text(.67,y,right[i],fontsize=13)
            dest=2-i if not wrong else i
            ax.add_patch(FancyArrowPatch((.36,y+.02),(.65,.78-dest*.28+.02),arrowstyle='->',mutation_scale=16,color=[blue,green,red][i],lw=1.7))
        ax.text(.02,.96,tr('干质量及身份','Dry mass + identity'),fontsize=11);ax.text(.67,.96,tr('湿质量及身份','Wet mass + identity'),fontsize=11)
    ax=fig.add_subplot(gs[1,0]);correct=[3,2.4,2.5];wrong=[(2.8-1.2)/1.2,(3.4-1)/1,(4.8-.8)/.8]
    for i,(c,w) in enumerate(zip(correct,wrong)):
        ax.plot([c,w],[i,i],color='#acb8b8',lw=2);ax.scatter([c],[i],color=blue,s=80,zorder=3);ax.scatter([w],[i],color=red,s=70,marker='x',zorder=3)
    ax.set(yticks=[0,1,2],yticklabels=['A01','A02','A03'],xlabel=tr('按干质量归一化的吸液量 / g·g⁻¹','Dry-basis liquid uptake / g·g⁻¹'),title=tr('c  相同数字，错误关联改变结果','c  The same numbers give different results'))
    ax.grid(axis='x',alpha=.15);ax.scatter([],[],color=blue,s=60,label=tr('正确配对','Correct pairing'));ax.scatter([],[],color=red,s=60,marker='x',label=tr('错配','Mismatched'));ax.legend(frameon=False)
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.set_title(tr('d  从存储位置转向数据含义','d  Separate position from meaning'),loc='left')
    ax.text(.02,.78,'E. F. Codd · 1970',fontsize=20,color=ink,transform=ax.transAxes)
    ax.text(.02,.54,tr('关系数据模型关注：\n改变存储安排时，数据关系保持清楚。','Relational data modeling asks how\nmeaning can survive changes\nin storage arrangement.'),fontsize=15,transform=ax.transAxes)
    ax.text(.02,.15,tr('本例中的做法：\n把样品ID、条件与测量值放在同一记录中。','In this example:\nkeep specimen ID, conditions,\nand measurements in one record.'),fontsize=14,transform=ax.transAxes)
    save(fig,'identity-history')

    fig=plt.figure(figsize=(12,6),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.4,1])
    ax=fig.add_subplot(gs[0]);
    for i,r in enumerate(processed):
        color=blue if r['bath']=='water' else red;q=r['uptake_g_per_g']
        if q is None:ax.text(.08,i,tr('未称量','Not weighed'),va='center',color='#6b7779',fontsize=12)
        else:ax.hlines(i,0,q,color=color,alpha=.4,lw=2);ax.scatter([q],[i],s=80,color=color);ax.text(q+.08,i,f'{q:.2f}',va='center',fontsize=12)
    ax.set(yticks=range(6),yticklabels=ids,xlim=(0,3.7),xlabel=tr('吸液量 / g·g⁻¹','Liquid uptake / g·g⁻¹'),title=tr('a  每个点保留样品身份','a  Keep each specimen visible'));ax.set_ylim(-.5,len(processed)-.5);ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
    ax=fig.add_subplot(gs[1]);
    for i,bath in enumerate(['water','saline']):
        vals=[r['uptake_g_per_g'] for r in processed if r['bath']==bath and r['uptake_g_per_g'] is not None];col=blue if i==0 else red
        ax.scatter([i+(.1*(j-(len(vals)-1)/2)) for j in range(len(vals))],vals,color=col,s=70,alpha=.8)
        avg=groups[bath]['mean_uptake'];ax.text(i,3.3,tr(f"有效 {len(vals)} / 3",f"{len(vals)} of 3 valid"),ha='center',fontsize=14)
        if avg is not None:
            ax.hlines(avg,i-.25,i+.25,color=ink,lw=3)
            label=tr(f'均值 {avg:.4f}',f'Mean {avg:.4f}')
        else:
            label=tr('无有效称量','No valid weighing')
        ax.text(i,.4,label,ha='center',fontsize=13,color=col)
    ax.set(xticks=[0,1],xticklabels=[tr('水浴','Water'),tr('盐水浴','Saline')],ylabel=tr('吸液量 / g·g⁻¹','Liquid uptake / g·g⁻¹'),ylim=(0,3.6),xlim=(-.55,1.55),title=tr('b  汇总同时说明有效计数','b  Summaries retain valid counts'));ax.grid(axis='y',alpha=.15)
    save(fig,'specimen-results')
    summary={'dataset':'Constructed six-record liquid-uptake example','record_count':len(records),'valid_count':sum(r['uptake_g_per_g'] is not None for r in processed),'missing_ids':[r['id'] for r in processed if r['uptake_g_per_g'] is None],'groups':groups,'uptake_by_id':{r['id']:r['uptake_g_per_g'] for r in processed},'lookup_A01_after_sort':ordered_lookup['A01'],'independent_copy_original_dry_g':records[0]['dry_g'],'wrong_pairing_A_uptake':wrong}
    for name,data in [('records.json',records),('processed.json',processed),('summary.json',summary)]:
        (args.output/name).write_text(json.dumps(data,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

代码还展示了复制中的一个细节。`alias = records`让两个名字指向同一个列表，修改其中的字典会通过另一个名字看见；仅复制最外层列表，也仍可能让内部字典被共享。`copy.deepcopy(records)`则为本例建立独立的嵌套记录，修改副本不会改变原始值。完整脚本用一次明确改动检验这种差别，随后确认原始A01干质量仍为1.20 g。理解名字、容器与内部对象的关系，可以避免在“试着修改一下”时无意改变正在分析的数据。

本例计算结果时使用`record.copy()`复制一条字典，再增加`uptake_g_per_g`字段。由于这些原始字段只包含字符串、数字和`None`，浅复制足以让新增字段与原字典分开。若字段里还嵌着可修改的列表，例如一个样品的全部时间序列，就需要重新考虑共享关系。这不是要求每次都做最深的复制，而是要求清楚哪一层对象会被改动，哪些对象应继续作为共同的原始记录。

### 运行并保留三层结果

生成原始记录、逐样品结果、摘要及三幅科学图。

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

运行后先检查`summary.json`中的记录数6、有效数5和缺失编号B02，再核对每个编号的吸液量。`records.json`保存原始字段，`processed.json`保存新增的计算结果；其中JSON的`null`对应Python中的`None`。这三个文件各有清楚用途，前者帮助检查输入，中间结果帮助追踪单个样品，摘要帮助快速比较。保留这些层次，比只留下两条均值更方便定位一次录入或配对错误。

## 重排记录、修改一条称量，再追踪它的去向

下面的实验允许选择样品、修改它的干湿质量或把湿质量标为缺失，并按编号、干质量或湿质量排列记录。表格与结果图同步更新，高亮始终追踪所选编号。先选择A01，再改变排序方式：它在列表中的位置可能移动，湿质量和吸液量仍应跟随A01。对照模式会故意把前三条水浴记录的湿质量单独排序，让你看到数字没有变化时，错误关联怎样改变结果。

### 记录移动，身份保持

先选择一个样品，再排序或修改记录。表格位置和图中高亮共同追踪同一个编号，紫色错配对照保留原始输入数字。

| 位置 | ID | 处理 | dry_g | wet_g | 吸液量 / g·g⁻¹ |
| --- | --- | --- | --- | --- | --- |

[Figure: 干湿质量关系及按样品计算的吸液量](https://ml-biomat.com/tutorials/python-scientific/p03/#P03-plot)

接着选择B02，取消缺失标记，并输入湿质量2.80 g。它的干质量为1.00 g，因此新吸液量为1.80 g/g，盐水浴组有效数从2变为3，均值从1.95变为1.90 g/g。这个变化不是重新排列造成的，而是确实增加了一条可计算的观测。再次勾选缺失，样品记录仍在，图中的结果点消失，汇总分母回到2。把位置变化、数值修改和观测是否存在分开观察，数据整理就会变成一组可以理解和验证的操作。

最后试着用一句话描述每个结构的职责：列表保存一批记录的顺序，字典保存字段之间的对应，编号索引帮助查找稳定身份，缺失标记保留“这里没有数”的事实。它们让一个小程序可以扩展到更多样品，而不必成倍增加人工配对的工作。下一章将在这些记录上把重复计算写成函数，使同一条科学规则能够被清楚地调用、检查和复用。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Software Carpentry — Lists](https://swcarpentry.github.io/python-novice-gapminder/11-lists.html)

   沿用先追踪单项再修改集合的教学顺序，改为原创样品记录案例。Copyright The Carpentries。

   CC BY4.0, https://creativecommons.org/licenses/by/4.0/; original prose, code and figures.
2. [Python 3.14 — Data Structures](https://docs.python.org/3.14/tutorial/datastructures.html)

   列表、字典、排序与浅复制的语言参考。

   PSF documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Built-in Types](https://docs.python.org/3.14/library/stdtypes.html#dict)

   映射查找、插入顺序与缺失标记相关操作。

   PSF documentation license
4. [E. F. Codd — A Relational Model of Data for Large Shared Data Banks (1970)](https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks)

   数据含义与内部存储安排分离的历史背景。

   Historical factual reference to IBM publication record; no reproduced article text or figure.
