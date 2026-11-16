# 读懂一张真实的数据表

Source: https://ml-biomat.com/tutorials/python-scientific/p11/
Language: zh-CN

从南极企鹅记录出发，理解行与列、单位、缺失值和保留观测身份的筛选。

## 先问每一行是什么，再问怎样算

打开一张实验表，最先看到的通常是密密麻麻的数字。可同样一个“4.2”，可能表示质量、长度、溶液酸碱度，也可能只是一个类别编号。计算之前需要把这些数放回观测过程：测了什么对象，每次记录包含哪些信息，单位是什么，空白又表示什么。pandas适合处理这种既有数字又有名称、日期和分类的表格。本章用真实的企鹅测量数据练习读取、检查、选择和保存，让后续分析中的每一个点都能找到对应记录。

这份数据包含344条成年企鹅观测记录，涉及Adelie、Chinstrap和Gentoo三个物种，记录了岛屿、喙的两个尺寸、鳍状肢长度、身体质量、性别和研究年份。Adelie指阿德利企鹅，Chinstrap指帽带企鹅，Gentoo指巴布亚企鹅，常见中文名称也有白眉企鹅。程序保留文件中的英文类别值，避免同一个类别在不同译名之间变成两个组。学习表格操作无需先掌握鸟类分类，只需记住这些名字用来区分三类观测对象。

一个很适合入门的问题是：来自Dream岛、属于Adelie物种、身体质量至少4000 g的记录有哪些？问题包含两个类别条件和一个数值条件，还要求质量已经测得。我们将把这句话逐项变成程序中的条件，得到14条记录，并在鳍状肢长度与身体质量的散点图中标出来。这里关注的是这份数据中的记录集合，物种和岛屿的组合由实际采样安排决定；读者会在图中直接看到哪些组合有记录。

数据文件与完整例子放在一起，运行时直接读取随包提供的CSV。它采用公开的CC0数据许可，收集工作来自Kristen Gorman及Palmer站长期生态研究项目，整理版由palmerpenguins项目提供。正文中的图与筛选结果都由这份表实际计算得到。我们先保持输入文件原样，给记录建立稳定的本章编号，再生成需要的新列与结果表，这样可以随时从一个图形标记回到原始读数。

## 野外测量留下的结构，藏在列名里

这批观测对应南极的三个野外研究季节，数据中的年份标签为2007、2008和2009。原研究在2014年发表，研究人员在岛屿上的繁殖巢位测量成年企鹅，用卡尺记录喙的尺寸、用尺记录鳍状肢长度，并称量身体质量。对生物学家来说，这些量分别描述身体的不同部分；对程序来说，它们后来成了不同的列。一次完整的观测过程把身体结构、地点和时间联系起来，表格保存的正是这些联系。

喙就是鸟的嘴部，喙长和喙深描述不同方向的尺寸。长度较大并不必然意味着上下方向也厚，因而两个字段需要分别保存。鳍状肢由企鹅的前肢形成，本表记录的是其长度；身体质量则是整只动物的称量结果。一个字段测量局部长度，另一个字段测量整体质量，它们可以放在同一行，但不能因为都是数字就直接相加。列名中的`_mm`与`_g`把单位带在变量旁边，读程序时能够持续提醒我们这些差别。

图中的年份与物种计数说明，真实数据很少是每个组都一样大的整齐方格：Adelie三年的记录数为50、50、52，Chinstrap为26、18、24，Gentoo为34、46、44。每个数字都是表中实际存在的行数。计数不均衡会影响之后的汇总方式，也使保留物种和年份变得重要。研究年份表示采样所属季节，多个年份的记录放在同一张表里，并不自动构成同一个体的连续跟踪；要研究个体变化，还需要可以跨时间对应的原始个体标识。

pandas的历史同样与观测表的结构有关。Wes McKinney在2010年的论文中介绍它时，讨论的就是带有字段名称、不同数据类型和观测标签的表格。NumPy已经能高效计算数值数组，真实记录还需要回答“这一列是什么”“两份结果中哪两行对应”这样的问题。DataFrame把数值和标签一起组织起来，使程序能够按列名取出身体质量、按记录标签找到同一次观测。下面的图把野外采样的分组结构与表中的具体行放在一起，展示这种联系。

![三物种三年份记录数矩阵、四项测量字段说明，以及含NA的前六行表格。](https://ml-biomat.com/static/tutorials/python-scientific/figures/45f497adfa74f35dd4f19c2d.svg?v=45f497adfa74)

图 12007、2008、2009是数据中的研究年份标签。计数矩阵呈现各物种的实际记录数，右侧把测量量与列名连接；下方保留首六条记录及本章生成的PG编号。

## DataFrame与Series：整张表和一列记录

`pd.read_csv`把CSV读成DataFrame，可以先把它理解为一张具有行标签和列标签的表。原表的`shape`是(344,8)，表示344行、8列；`head(6)`显示前六行，便于检查列名是否读对、分隔是否正确、数字是否落在预期位置。这里的`shape`是现成属性，不需要括号；`head`需要执行一次取前几行的操作，因此写成函数调用。屏幕只显示一部分行时，省略号表示显示被缩短，数据仍保存在表里。

写`table['body_mass_g']`会得到一个Series，即带有行标签的一列数据。写`table[['body_mass_g']]`则仍得到DataFrame，只是它只有一列：里面的一对方括号构成列名列表，外面的一对方括号执行选择。这个区别在后续函数要求一维或二维输入时很有用。选择多个字段时，把列名放进同一个列表，例如同时取物种、岛屿和身体质量，得到一张更窄的表，原来的记录配对关系保持不变。

本章给文件中的第一条记录命名为PG001，第二条为PG002，依此到PG344。这是我们根据当前CSV行顺序生成的记录标签，便于教学中的查找与追踪；它没有替代生物研究中的个体身份。程序用`set_index`把这些标签设成索引，同时保留`record_id`列，保存CSV时就能把编号一起写出去。索引像图书目录里的定位标签，负责帮助程序找到一行，并不强制规定这一行排在屏幕第几个位置。

`table.loc['PG001']`按标签找到第一条原始记录，而`table.iloc[0]`按当前位置找到当前表的第一行。在刚读入、尚未排序时，两者恰好指向同一条记录；按身体质量从大到小排序后，`iloc[0]`变成PG170，质量为6300 g，`loc['PG001']`仍然找到3750 g的那条记录。理解这个差别，能避免把“排序后的第一行”误当成“最初的第一条观测”。筛选保留原标签也有同样的好处，编号中出现间隔只是说明中间记录未被选中。

索引选择还能取出一段记录，但两种切片的边界约定不同。`iloc[0:3]`按位置取第0、1、2行，不包括位置3，沿用Python切片的习惯；在本章有序且唯一的标签索引中，`loc['PG001':'PG003']`包括起止两个标签，也取到前三条。写条件之前先想清楚自己是在说“前三个位置”还是“这两个标签之间”，就能给边界一个具体解释。排序改变的是位置与顺序，标签指向的记录内容仍应保持一致。

## 让数字、类别和单位各就各位

CSV本身是文本，读入后需要确定每一列在程序中的类型。物种、岛屿和性别按字符串读取；带小数的喙长与喙深使用可缺失的`Float64`；鳍状肢长度、身体质量和年份使用可缺失的`Int64`。这里大写的I与F是pandas可缺失类型名称的一部分，允许一列既保存数值又保存`<NA>`。它让“以整数记录的质量中有两条未提供数值”保持为一个自然的数据结构，无需把缺失伪装成一个特别大的负数。

类型与科学含义有关，却不是一回事。年份虽然以整数保存，我们通常会按年份选择或分组，而不是把它与喙长加在一起；物种名称虽然是字符串，也不能通过字母顺序推断物种之间的生物距离。`dtypes`告诉我们程序采用什么存储与运算方式，列的含义仍要从测量定义中理解。读入时指定类型还有一个实际作用：原本应该是数字的位置若混入不符合约定的文字，转换会暴露这条输入问题，方便回到记录核查。

身体质量原列使用g，作图时可以另外增加kg列。程序直接把整列除以1000，pandas会对每个已测得的数完成换算，同时让缺失位置继续缺失。PG001的3750 g变成3.75 kg，但观测对象和测得的质量没有改变。我们保留原来的g列，把换算结果命名为`body_mass_kg`，这样筛选条件可以继续使用4000 g，图中也能清楚采用kg，两处都能根据列名查回单位。

$$
m_{\mathrm{kg}}=\frac{m_{\mathrm g}}{1000}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dc51519473042eca7790d43a.svg) | 同一身体质量以g表示的数值 |
| ![Formula](https://ml-biomat.com/static/agent-math/d795b0597896cbce0a258e78.svg) | 同一身体质量以kg表示的数值 |
| ![Formula](https://ml-biomat.com/static/agent-math/11e3e740ee2e42f3954f5b75.svg) | 1 kg包含1000 g所对应的数值换算因子 |

本式转换同一个物理量的数值表示。PG001的3750 g除以1000后为3.75 kg；原g列保留，新建kg列。缺失值在换算后仍然缺失。

把新列加到表中时，pandas会依据索引标签对齐Series。比如把某一列排序后再赋回另一张表，它会优先根据标签寻找对应记录，而不是仅按当前显示顺序逐格填入。这种行为在带标签的计算中很有价值，也要求我们保留有意义且适当唯一的索引。若显式转成NumPy数组，标签信息就被去掉，之后通常按位置处理。先明确自己需要按记录配对还是按位置配对，再决定是否转换成数组。

还可以检查类别值的拼写与空格。比如`Adelie`和末尾多一个空格的`Adelie`在字符串比较中属于不同值；若一份表确实有这类录入差异，应先查清哪些写法代表同一个类别，再统一。原始记录中两只企鹅也可能恰好有相同的质量与长度，这不能单凭数值相等就判成重复录入。删除重复记录需要能说明观测身份的字段或记录依据，而不是只比较某几列是否一样。

## 一个空格，为什么会改变可回答的问题

原表中的`NA`表示该字段没有可用值。程序读入后用`isna()`检查，质量缺失2条、每种长度测量也各缺失2条，性别缺失11条。PG004和PG272的四项身体测量与性别都缺失，但物种、岛屿和年份仍然存在；另外九条记录有身体测量，却缺少性别。把缺失位置画成矩阵，可以看出几个字段的空格是否落在同一行，这比只看各列缺了几个数更接近观测本身。

![各字段缺失条数与逐条记录的缺失位置矩阵。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f60e35430661738a88abe4c2.svg?v=f60e35430661)

图 2四项身体测量各缺2条，性别缺11条。右侧逐条显示11条不完整记录：PG004和PG272同时缺少五个字段，其余九条只缺性别。

缺失质量与质量为0含义不同。前者表示这条记录没有可用称量值，后者会宣称动物的质量为0 g。把两个空格填成0后，程序依然能计算平均值，却已经回答了被改写的问题：本表有效质量的平均值约为4201.754 g，错误填零后变成约4177.326 g。差异来自总质量不变，而计入平均值的条数由342增加到344，而不是企鹅忽然变轻了。这个例子也说明，只要程序成功运行，并不足以判断表中的科学含义是否保持正确。

$$
f_{\mathrm{observed}}=\frac{N-M}{N},\qquad P_{\mathrm{observed}}=100f_{\mathrm{observed}}\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 当前记录集合的总行数，本例为344，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 所检查字段的缺失记录数；质量列为2，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/11f64c3bfb2e86718a2ef65d.svg) | 该字段已观测比例，无量纲，0到1 |
| ![Formula](https://ml-biomat.com/static/agent-math/a763e1e215ae6ae5172f959a.svg) | 将同一比例写成百分数；%表示每一百份 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c0d9d65f3495da5c81dd0e3.svg) | 把比例数值换算为百分数的因子 |

先从总数中减去缺失数，再除以总数。质量已观测比例为342/344≈0.994186，即99.4186%；性别则为333/344≈96.8023%。先指定字段与记录范围，比例才有明确含义。空集合N=0时显示“无记录”，不计算这个比值。

保留哪些行，应由当前问题所需的字段决定。画鳍状肢长度与质量的散点图，需要这两列都有数；在本数据中可以使用342条记录。研究性别分组时，还要有性别，若要求原来八列全部完整，则留下333条。一个性别缺失但质量已测得的记录，仍能帮助展示质量分布。程序分别生成所需字段完整的选择，不在一开始就把所有含空格的行一并删除。这样，不同分析的实际记录数也能明确报告。

检测缺失使用`isna()`或`notna()`，不要通过是否等于某个缺失符号来猜测。可缺失类型中的未知值参与大小比较时，结果也可能未知；本章在质量筛选条件后使用`fillna(False)`，明确规定“质量未知的记录不能满足至少4000 g这个条件”。这一步只把用于筛选的真假结果补成False，没有给质量填入任何数字。交互中若不设置质量门槛，可以保留含缺失的记录，并分别显示其中有多少条能够进入散点图。

## 把一个问题拆成三个条件

现在把“Dream岛、Adelie、至少4000 g”拆开。`table['species'].eq('Adelie')`给每条记录判断物种，`table['island'].eq('Dream')`判断岛屿，`table['body_mass_g'].ge(4000)`判断质量门槛。每个判断都得到与原表索引对应的一列真假值。用`&`把三列条件连接起来，表示三件事同时满足；用`|`则表示满足其中之一。在直接写比较表达式时，每个条件都加括号，可以清楚控制组合顺序。

Python的`and`通常连接两个单独的真假判断，不能直接替代整列条件之间的`&`。一张表里有的记录满足条件，有的不满足，不能用一个真假值代表全列。筛选掩码恰好保留了这种逐行差别。随后写`table.loc[mask]`，只取掩码为True的行；若还想限定输出字段，可以在逗号后给出列名列表。筛选过程选的是整条记录，物种、岛屿和身体测量仍然来自同一行。

本例得到14条记录，其中前四条是PG036、PG040、PG044和PG046，质量分别为4150、4650、4400和4600 g。图中的圆环标记这些记录在完整散点中的位置。它们都位于4 kg水平线或其上方，但线之上的其他点不一定被选中，因为还要同时满足物种和岛屿条件。把筛选结果放回全部观测的背景，读者就能看见每个条件究竟在排除哪部分记录。

![物种着色的长度—质量散点图、选中记录圆环、质量直方图与记录编号。](https://ml-biomat.com/static/tutorials/python-scientific/figures/397ca50346cf7c43437e4173.svg?v=397ca50346cf)

图 3全部342条具有鳍状肢长度与质量的记录作为背景，圆环标出满足Adelie、Dream和至少4000 g的14条记录。直方图与编号列表展示同一选择。

筛选以后，若要在结果上增加或修改列，程序先取`.copy()`形成一个明确的结果表；对原表中的目标区域赋值时，使用一次完整的`.loc[行条件, 列名]`。这种写法让修改对象清楚可读，也符合pandas 3中的复制与赋值语义。保存结果时使用`index=False`，因为`record_id`已经作为普通列保留，再保存一次索引会增加重复信息。把缺失输出为`NA`，下次读取仍能恢复本章约定的缺失含义。

图中的散点和直方图分别提供不同的观察角度。散点把同一记录的长度与质量配成位置；若两条记录的两项测量完全相同，它们可能重叠，所以肉眼看到的圆点数会少于实际记录数。直方图把质量划分成每250 g一个区间，柱高统计落入区间的记录数。两种图都来自已保留身份的同一张表：前者保留变量配对，后者汇总一个变量的分布。读取图时同时看坐标单位、区间宽度与记录数，就能避免把柱高误当成质量值。

## 完整例子：从原表到可追踪的筛选结果

下载包中包含`main.py`、原样保留的`penguins.csv`及数据许可说明。运行时不需要联网，程序从自己的文件旁找到CSV，避免依赖终端当前打开在哪个目录。`load_table`负责指定类型、建立记录编号和换算kg列；`select_records`负责按给定条件选择；主函数保存结果表、数值摘要和三组图。完整函数都列在下面，可以边看正文边检查每项操作如何落实。

### 运行真实表格例子

中文图使用--language zh；main.py旁应保留下载包内的penguins.csv。

```
python main.py --output output --language en
```

### 读取、检查、筛选与绘图的完整程序

保留原表，以明确类型读取；逐行建立标签，生成kg列，并将同一筛选结果同时写成CSV和图。

```
"""Read, inspect, select, and plot real CC0 Palmer penguin measurements."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap

SPECIES = ['Adelie', 'Chinstrap', 'Gentoo']
COLORS = {'Adelie': '#2e6e91', 'Chinstrap': '#b7553d', 'Gentoo': '#37806a'}
MEASUREMENTS = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
DTYPES = {'species':'string','island':'string','bill_length_mm':'Float64',
          'bill_depth_mm':'Float64','flipper_length_mm':'Int64',
          'body_mass_g':'Int64','sex':'string','year':'Int64'}


def load_table(path):
    raw = pd.read_csv(path, dtype=DTYPES, na_values=['NA'])
    table = raw.copy()
    table.insert(0, 'record_id', [f'PG{i+1:03d}' for i in range(len(table))])
    table = table.set_index('record_id', drop=False)
    table.index.name = 'record_key'
    table['body_mass_kg'] = table['body_mass_g'] / 1000
    return raw, table


def select_records(table, species='all', island='all', minimum_g=0, complete=False):
    mask = pd.Series(True, index=table.index)
    if species != 'all':
        mask &= table['species'].eq(species)
    if island != 'all':
        mask &= table['island'].eq(island)
    if minimum_g > 0:
        mask &= table['body_mass_g'].ge(minimum_g).fillna(False)
    if complete:
        mask &= table[list(DTYPES)].notna().all(axis=1)
    return table.loc[mask].copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('output'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    input_path = Path(__file__).with_name('penguins.csv')
    raw, table = load_table(input_path)
    missing = raw.isna().sum()
    complete_measurements = table.dropna(subset=MEASUREMENTS)
    complete_all = table.dropna(subset=list(DTYPES))
    selected = select_records(table, 'Adelie', 'Dream', 4000)
    mass_mean = float(table['body_mass_g'].mean())
    wrong_zero_mean = float(table['body_mass_g'].fillna(0).mean())
    ordered = table.sort_values('body_mass_g', ascending=False, kind='stable', na_position='last')
    with input_path.open(encoding='utf8', newline='') as file:
        independent = list(csv.DictReader(file))
    valid_mass = [int(r['body_mass_g']) for r in independent if r['body_mass_g'] != 'NA']
    selected_ids = [f'PG{i+1:03d}' for i,r in enumerate(independent)
                    if r['species']=='Adelie' and r['island']=='Dream'
                    and r['body_mass_g']!='NA' and int(r['body_mass_g'])>=4000]
    assert selected.index.tolist() == selected_ids
    assert len(raw)==344 and len(complete_measurements)==342 and len(complete_all)==333
    assert missing['body_mass_g']==2 and missing['sex']==11 and len(selected)==14
    assert math.isclose(mass_mean, math.fsum(valid_mass)/len(valid_mass))
    assert float(table.loc['PG001','body_mass_kg']) == 3.75
    assert pd.isna(table.loc['PG004','body_mass_g'])
    table.to_csv(args.output/'penguins_with_ids.csv', index=False, na_rep='NA')
    selected.to_csv(args.output/'selected_records.csv', index=False, na_rep='NA')
    records = json.loads(table.to_json(orient='records'))
    (args.output/'lab-records.json').write_text(json.dumps(records,ensure_ascii=False),encoding='utf8')
    zh=args.language=='zh'; tr=lambda z,e:z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family':family if zh else ['DejaVu Sans','Arial'],
                         'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold',
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none',
                         'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=170,bbox_inches='tight')
        plt.close(fig)

    fig=plt.figure(figsize=(12.6,8.3),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,.95])
    counts=pd.crosstab(raw['species'],raw['year']).reindex(SPECIES)
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(counts.to_numpy(),cmap='Blues',vmin=0,vmax=60,aspect='auto')
    for i in range(3):
        for j in range(3):ax.text(j,i,str(counts.iloc[i,j]),ha='center',va='center',fontsize=19,color='white' if counts.iloc[i,j]>35 else '#172b36')
    ax.set(xticks=[0,1,2],xticklabels=counts.columns,yticks=[0,1,2],yticklabels=SPECIES,
           xlabel=tr('研究年份标签','Study-year label'),title=tr('a  三次野外季节留下的记录数','a  Records from three field seasons'))
    fig.colorbar(im,ax=ax,pad=.02).set_label(tr('记录数','Records'))
    ax=fig.add_subplot(gs[0,1]);ax.axis('off')
    ax.text(0,.98,tr('测量对象 → 量与单位 → 数据列','Observation → quantity and unit → column'),fontsize=15,weight='bold',va='top')
    descriptions=[('bill_length_mm',tr('喙长：沿喙的长度 / mm','Bill length / mm')),('bill_depth_mm',tr('喙深：喙的上下尺寸 / mm','Bill depth / mm')),('flipper_length_mm',tr('鳍状肢长度 / mm','Flipper length / mm')),('body_mass_g',tr('身体质量 / g','Body mass / g'))]
    for k,(field,label) in enumerate(descriptions):
        y=.77-k*.20;ax.text(0,y,label,fontsize=13);ax.text(0,y-.08,field,fontsize=12,color='#2e6e91')
    ax=fig.add_subplot(gs[1,:]);ax.axis('off')
    rows=[]
    for _,r in table.iloc[:6].iterrows():
        rows.append([r['record_id'],r['species'],r['island'],str(r['year']), 'NA' if pd.isna(r['body_mass_g']) else str(r['body_mass_g']), 'NA' if pd.isna(r['sex']) else r['sex']])
    tab=ax.table(cellText=rows,colLabels=['record_id','species','island','year','body_mass_g','sex'],cellLoc='center',bbox=[0,.08,1,.78]);tab.auto_set_font_size(False);tab.set_fontsize(12)
    for (i,j),cell in tab.get_celld().items():cell.set_edgecolor('#d1dddd');cell.set_facecolor('#e4eeec' if i==0 else '#fbfaf6');cell.set_text_props(color='#b7553d' if i==4 and j in [4,5] else '#172b36')
    ax.text(0,.98,tr('b  每行是一条观测；PG编号保留CSV中的记录位置','b  One observation per row; generated PG labels preserve CSV record positions'),fontsize=14,weight='bold')
    save(fig,'field-records-history')

    fig=plt.figure(figsize=(12.6,7.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);fields=MEASUREMENTS+['sex'];labels=[tr('喙长','Bill length'),tr('喙深','Bill depth'),tr('鳍状肢长','Flipper length'),tr('质量','Body mass'),tr('性别','Sex')];values=[int(missing[c]) for c in fields]
    ax.barh(labels,values,color=['#2e6e91']*4+['#b7553d']);ax.invert_yaxis();ax.set(xlim=(0,13),xticks=range(0,13,2),xlabel=tr('缺失记录数（总数344）','Missing records (344 total)'),title=tr('a  每一列缺了多少','a  Missingness by column'));ax.grid(axis='x',alpha=.15)
    for i,v in enumerate(values):ax.text(v+.2,i,f'{v} / 344',va='center')
    ax=fig.add_subplot(gs[0,1]);incomplete=table.loc[table[fields].isna().any(axis=1),fields];matrix=incomplete.isna().to_numpy(dtype=int)
    ax.imshow(matrix,cmap=ListedColormap(['#e3ecea','#b7553d']),vmin=0,vmax=1,aspect='auto')
    for i in range(len(incomplete)):
        for j in range(5):ax.text(j,i,'NA' if matrix[i,j] else '✓',ha='center',va='center',color='white' if matrix[i,j] else '#286b5a',fontsize=12)
    ax.set(xticks=range(5),xticklabels=labels,yticks=range(len(incomplete)),yticklabels=incomplete.index,title=tr('b  缺失是否落在同一条记录','b  Which fields are missing together'))
    ax.tick_params(axis='x',labelsize=10);fig.suptitle(tr('保留观测身份，才能理解一个空格','A missing entry makes sense within its observation'),fontsize=17,weight='bold')
    save(fig,'missing-records')

    fig=plt.figure(figsize=(12.6,7.7),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.45,1],height_ratios=[1,1])
    ax=fig.add_subplot(gs[:,0])
    for species in SPECIES:
        sub=table.loc[table['species'].eq(species)].dropna(subset=['flipper_length_mm','body_mass_kg'])
        ax.scatter(sub['flipper_length_mm'].to_numpy(dtype=float),sub['body_mass_kg'].to_numpy(dtype=float),s=30,alpha=.65,color=COLORS[species],label=species)
    ax.scatter(selected['flipper_length_mm'].to_numpy(dtype=float),selected['body_mass_kg'].to_numpy(dtype=float),s=100,facecolors='none',edgecolors='#172b36',lw=1.5,label=tr('筛出的14条记录','14 selected records'))
    ax.axhline(4,color='#172b36',ls=':',lw=1);ax.set(xlabel=tr('鳍状肢长度 / mm','Flipper length / mm'),ylabel=tr('身体质量 / kg','Body mass / kg'),xlim=(170,235),ylim=(2.5,6.6),title=tr('a  同一行的两次测量组成一个点','a  Two measurements from one row form a point'));ax.legend(loc='upper left',fontsize=11);ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[0,1]);bins=np.arange(2500,6501,250)
    ax.hist(table['body_mass_g'].dropna().to_numpy(dtype=float),bins=bins,histtype='step',lw=2,color='#9aa9ac',label=tr('全部有效质量','All observed masses'))
    ax.hist(selected['body_mass_g'].to_numpy(dtype=float),bins=bins,color='#2e6e91',alpha=.75,label=tr('筛选结果','Selected'))
    ax.set(xlabel=tr('身体质量 / g','Body mass / g'),ylabel=tr('记录数','Records'),title=tr('b  阈值之外，还限定物种和岛屿','b  Species and island also determine selection'));ax.legend(fontsize=10);ax.grid(axis='y',alpha=.12)
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.text(0,.95,'Adelie  ∩  Dream  ∩  mass ≥ 4000 g',fontsize=13,weight='bold');ax.text(0,.74,tr('344条记录 → 14条满足全部条件','344 records → 14 meet every condition'),fontsize=13)
    ax.text(0,.54,tr('原始位置编号保留，例如：','Original-position labels remain, for example:'),fontsize=12)
    for i,(_,r) in enumerate(selected.head(4).iterrows()):ax.text(0,.37-i*.1,f"{r['record_id']}    {r['flipper_length_mm']} mm    {r['body_mass_g']} g",fontsize=12)
    save(fig,'linked-selection')
    summary={'dataset':'Palmer penguins, CC0','input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
             'raw_shape':list(raw.shape),'dtypes':{k:str(v) for k,v in raw.dtypes.items()},'missing_counts':{k:int(v) for k,v in missing.items()},
             'measurement_complete_rows':len(complete_measurements),'all_complete_rows':len(complete_all),
             'selected_count':len(selected),'selected_ids':selected_ids,'mass_observed_count':len(valid_mass),
             'mean_mass_g':mass_mean,'zero_filled_mean_mass_g':wrong_zero_mean,
             'first_record_mass_kg':float(table.loc['PG001','body_mass_kg']),
             'heaviest_record':ordered.iloc[0]['record_id'],'heaviest_mass_g':int(ordered.iloc[0]['body_mass_g']),
             'missing_record_ids':incomplete.index.tolist(),'year_counts':json.loads(counts.to_json(orient='index'))}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
```

运行后，`penguins_with_ids.csv`保存344条记录、生成的编号和kg列，`selected_records.csv`保存14条筛选结果。`summary.json`记录原表形状、各列类型、缺失数、实际可用记录数以及筛选编号。程序还用Python标准库的CSV读取器独立数了一遍满足条件的记录，并用逐个数字的求和核对有效质量均值。两种实现围绕同一个原始文件得到一致结果，有助于检查条件与索引是否写对。

代码中的`dropna(subset=...)`明确列出当前需要的字段，`notna().all(axis=1)`则问“这一行列出的所有字段是否都有值”。这里沿轴1把一行中的多个真假结果合成一个判断，最后每条记录得到一个True或False。图中缺失矩阵采用另一种信息汇总：`isna().any(axis=1)`找出至少有一个字段缺失的行，以便逐条检查。`all`和`any`对应日常语言里的“全部”和“至少一个”，把它们放回具体行就很容易理解。

再留意散点图的生成方式：程序从同一张已筛选的表中同时取鳍状肢长度和质量，然后把这两列交给绘图函数。如果先分别删除两列中的缺失值，再按剩余位置配对，在一般数据里可能把不同记录拼成一个点。当前表的两列恰好在同两条记录上缺失，也仍然采用按整行选择的写法，让配对规则在数据更新后继续成立。每个点保持它所代表的那一次观测，才有资格用于解释变量之间的关系。

历史图中的计数矩阵由`pd.crosstab`生成：一个分类字段决定行，另一个分类字段决定列，每个格子统计同时具有这两个类别的记录数。选Adelie与2007时，它数的是对应的50行，而不是对年份或身体尺寸做平均。这个小例子把分类信息转成了可检查的表格结构，也为下一章按实验组汇总做好准备。数据类型允许求平均，并不意味着每一列都适合用平均值回答问题。

## 在图、筛选条件和原记录之间往返

下面的交互读入与Python相同的344条记录。物种和岛屿可以独立选择，质量门槛从“不限制”逐渐提高，还可以要求八个原始字段全部完整。页面同时显示选中的记录数、可绘制散点的记录数和所选记录中的缺失情况。选择一条记录时，详情和图中的高亮点一起更新；如果该记录缺少绘图所需测量，详情保留NA并说明它为何没有对应散点。

### 从344条记录中选择，仍然保留每一行的身份

灰点保留全部有坐标的记录；彩色点为当前选择；橙色环标出正在查看的记录。

[Figure: 与记录选择联动的散点和缺失统计](https://ml-biomat.com/tutorials/python-scientific/p11/#P11-chart)

先保持全部记录，选择PG004，观察它的物种与年份仍然可读，但长度和质量为空。随后勾选完整记录条件，PG004会离开结果表，总数变成333。取消完整条件，再选择Adelie、Dream和4000 g，结果应为14条，与Python一致。最后把物种改成Gentoo、岛屿改成Torgersen，结果为空；这是当前文件没有符合该组合的记录，图中仍保留坐标轴与背景，方便区分空集合与显示故障。

一张表读懂之后，数据清理就不再等同于把空格填满或把所有列变成数字。需要的是让列的类型与测量相符，让每个筛选条件对应清楚的问题，让缺失保持它的观测含义，并让图中的点能回到一条具体记录。下一章将从按类别汇总进入材料配方与重复测量，讨论同一试样多读几次数值后，组平均值应该怎样计算，以及这个平均值到底在描述谁。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P11.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pandas: Read and write tabular data](https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html)

   读入、检查类型与导出

   BSD-3-Clause; original teaching code
2. [pandas: Select a subset of a DataFrame](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html)

   列选择、布尔条件与标签选择

   BSD-3-Clause
3. [pandas: Working with missing data](https://pandas.pydata.org/pandas-docs/version/3.0/user_guide/missing_data.html)

   缺失值、可缺失类型与比较

   BSD-3-Clause
4. [Palmer penguins data](https://allisonhorst.github.io/palmerpenguins/)

   公开测量数据、字段定义和数据许可

   CC0 data; no artwork reproduced
5. [Gorman, Williams & Fraser (2014)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081)

   野外观测与测量方法

   CC BY article; factual context
6. [McKinney (2010): Data Structures for Statistical Computing in Python](https://doi.org/10.25080/Majora-92bf1922-00a)

   带标签表格的设计背景

   CC BY4.0 proceedings article
