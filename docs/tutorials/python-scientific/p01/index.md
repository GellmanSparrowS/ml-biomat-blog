# 让一段程序回答一个具体问题

Source: https://ml-biomat.com/tutorials/python-scientific/p01/
Language: zh-CN

从三次称量开始，看清变量、执行顺序和两个比例的区别。

## 一块吸水后的凝胶，究竟吸进了多少水？

把一小块干燥的凝胶放进水里，过一段时间取出，吸去表面容易流动的水，再放到天平上，它通常会比原来重。这个日常可理解的变化，也出现在吸水树脂、敷料、软接触材料和许多实验样品中。如果想比较两种材料，单看“增加了几克”还不够：原来较大的一块，往往也能留住更多水。我们需要把称量记录变成一个说得清楚的结果，例如每克干材料留住了多少克水。本章就用这件事写出第一段 Python 程序，并把原始读数、计算过程和图中的比例一一对应起来。

这里使用一组专门构造的教学读数：空容器为 0.40 g，容器与干样合计为 1.60 g，容器与湿样合计为 5.20 g。g 是克的符号，三个读数使用同一个单位。读数简单，便于先用纸笔检查程序；它们没有对应某一种商品的性能。称量时使用同一个容器，是因为我们要把容器的贡献从两次总读数中扣除。若中途换了容器，就应分别记录各自质量，计算规则也要随记录调整。程序的任务从来不只是做减法，还要让每个参与减法的数有明确对象。

可以先把问题想成两次拆包裹。天平看到的是“容器加内容物”，我们想知道的却是内容物。第一次拆掉容器得到干材料质量，第二次拆掉容器得到湿样质量；再比较这两份内容物，得到增加的质量。在本章设定的吸水过程中，把这部分增量记作留存水质量。实际设计这样的称量实验时，需要统一浸泡时间、表面水处理和干燥状态；如果同时发生材料溶出，质量变化还包含材料损失。把对象和过程先说清楚，后面的变量名、公式和图表才有共同含义。

完成这一章后，你将能保存并运行一个短程序，知道赋值语句怎样一步步产生结果，分清计算值与显示文字，并用两种分母比较同一份水的比例。页面中的完整示例还会生成三幅图和一份数值摘要。第一次阅读时，可以先掌握其中最前面的称量计算，再逐渐看懂绘图和保存结果的部分；计算主线始终是这三次称量，而不是一串需要背下来的命令。

![三次构造称量的质量拆分。灰色容器在每次称量中占0.40 g；湿样的组成图先扣掉容器，再比较干材料与留存水。](https://ml-biomat.com/static/tutorials/python-scientific/figures/5bc7cc447ee905af6e1e6878.svg?v=5bc7cc447ee9)

图 1三次构造称量的质量拆分。灰色容器在每次称量中占0.40 g；湿样的组成图先扣掉容器，再比较干材料与留存水。

## 程序是可以重新执行的计算过程

在计算器里按下 `1.60 − 0.40`，可以立即得到干材料质量。可是第二天收到另一组读数时，谁负责记住先减容器、再求增量、最后除以干质量？如果操作只留在人的记忆里，计算器会给出每一次运算的答案，却不会留下完整的分析方法。程序把这些顺序写成可保存的文字。Python 是一种编程语言，规定这些文字怎样表达数、计算和操作；Python 解释器则是读取并执行这些语句的软件。语言与解释器的关系，类似乐谱中的记号规则与读谱演奏的工具，但程序执行的每一步都有确定的语法含义。

代码可以有两种常见用法。交互式解释器允许输入一条语句、立刻观察结果，适合试算或确认一个写法；脚本是保存为文件的一组语句，可以从头连续执行。以 `.py` 结尾的文件通常是 Python 脚本，例如 `main.py`。文件名相当于一张计算方案的标签，文件内容才是方案本身。编辑器负责修改内容，终端负责接收运行命令，解释器负责执行 Python；初学时把这三个角色分开，比急着安装很多工具更有帮助。[第六章](https://ml-biomat.com/tutorials/python-scientific/p06/)会完整讲解环境选择和安装检查，这里先沿着一个已经可运行的例子理解过程。

下面的短代码就是计算核心。以 `#` 开头的部分是注释，帮助阅读者理解“这些数是什么”，不会参与数值运算。语句中的 `-` 表示相减，`/` 表示相除，`print(...)` 把括号里的内容显示出来。不要把书中的解释器提示符当成程序内容；本页代码框给出的都是可直接保存的代码。Python 需要英文半角标点，例如括号 `()` 和小数点 `.`；中文说明放在注释或引号内，便能与程序表达式清楚地共存。

### 三个输入，两个比例

顺序执行得到1.200 g、3.600 g、3.000 g/g、75.0%。

```
# Constructed balance readings, all in grams.
tare_g = 0.4
dry_total_g = 1.6
wet_total_g = 5.2
dry_g = dry_total_g - tare_g
wet_g = wet_total_g - tare_g
water_g = wet_g - dry_g
uptake_g_per_g = water_g / dry_g
water_fraction = water_g / wet_g
print(f"Dry mass: {dry_g:.3f} g")
print(f"Retained water: {water_g:.3f} g")
print(f"Dry-basis uptake: {uptake_g_per_g:.3f} g/g")
print(f"Water fraction: {water_fraction:.1%}")
```

阅读代码时，可以从上到下用手指跟踪：先记住三个读数，再算干样和湿样，接着算水，最后求比例。代码顺序是一种依赖关系的展开：水质量依赖干样和湿样，而干样与湿样又依赖天平读数。如果直接从比例那一行开始执行，前面的名字还没有对应数值，解释器就无法知道分子和分母是什么。保存脚本后从头运行，可以让这条依赖链每次都由同样的入口开始。程序给出的结果因此既能重复得到，也能逐行检查。

## 给数值起名字，才能看清它们怎样变化

`tare_g = 0.4` 可以读成“把名字 `tare_g` 与数值 0.4 关联起来”。tare 表示容器的皮重，后缀 `_g` 提醒我们使用克。变量是程序中用于指向值的名字；它不是一张会自动持续更新的电子表格单元格，也不是数学中永远成立的等式。赋值符号 `=` 先计算右侧，再把结果交给左侧的名字。例如执行 `dry_g = dry_total_g - tare_g` 时，Python 读取此刻两个输入名字所指的数，完成相减，并把得到的数交给 `dry_g`。

这种区别可以用一次改动看得很清楚。先运行干质量计算，之后单独把 `dry_total_g` 改为 1.8，旧的 `dry_g` 仍保留先前算出的值；再次运行相减那一行，它才变成约 1.4 g。赋值记录的是执行当时的结果，而不是建立“以后自动重算”的永久连接。交互笔记本把代码分成多个单元格后，随意改变执行顺序容易让新输入和旧结果同时出现。遇到读数已经修改、图却看起来没变的情况，应沿依赖关系重新计算，而不能只凭代码在页面上的排列判断它是否已经执行。

变量名影响阅读质量。把干质量写成 `a`、湿质量写成 `b`，计算仍能运行，却需要阅读者另查一份字母表。`dry_g`、`wet_g` 和 `water_g` 则把对象与单位留在语句中。Python 区分大小写，`dry_g` 和 `Dry_g` 是两个名字；词之间使用下划线，可以避免空格被当作语法分隔。单位后缀只是给人看的约定，解释器不会因此自动换算克与毫克。要让单位真的一致，仍需在输入和运算处明确处理，下一章会详细展开。

数字与文字也要分开。`0.4` 是可参与加减的数，`"0.4 g"` 则是由字符组成的字符串，适合用来展示。字符串可以容纳中文、单位和空格，但不能直接充当相减中的质量。因此先用数值计算，再把单位添加到输出文字，是一种清楚的安排。下图把测量值、表达式和输出分开画出；它还解释了 Python 为何把容易阅读的表达方式与连接其他工具的能力放在一起，这两点会贯穿后面的科研计算。

![上半图追踪一次赋值的输入、表达式和输出；下半图用Python的早期设计背景解释可读语句怎样连接已有工具。历史关系为原创方法示意。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f625f3d905a748e46a225a92.svg?v=f625f3d905a7)

图 2上半图追踪一次赋值的输入、表达式和输出；下半图用Python的早期设计背景解释可读语句怎样连接已有工具。历史关系为原创方法示意。

## 先守住质量账，再决定怎样报告比例

从总读数得到样品质量，只需减掉容器，但这一步值得写完整，因为它确定了后面所有比例的起点。容器 0.40 g 加干材料 1.20 g，恰好等于第一次总读数 1.60 g；容器 0.40 g 加干材料 1.20 g，再加留存水 3.60 g，恰好等于第二次总读数 5.20 g。图中三种颜色分别对应这三部分。颜色不是装饰：同一部分在不同称量中保持同色，帮助我们检查到底减掉了什么、保留了什么。

$$
m_d=M_d-m_c,\qquad m_w=M_w-m_c,\qquad m_a=m_w-m_d
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | 干材料净质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/9161e0473b88657dd837c6df.svg) | 容器与干样的总读数，g |
| ![Formula](https://ml-biomat.com/static/agent-math/da91b33ee64dd3e861a37f01.svg) | 空容器质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | 湿样净质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | 容器与湿样的总读数，g |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | 本章吸水设定中的留存水质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/1526ecedf7893f4ee28503c0.svg) | 从总量中减掉已知组成部分 |

同一容器贡献可分别从两次总读数中扣除：1.60−0.40=1.20 g；5.20−0.40=4.80 g；4.80−1.20=3.60 g。最后一步把净增量归为水，对应材料自身质量保持不变的设定。

得到水质量后，需要决定比较对象。如果想比较干材料利用自身质量留水的能力，就把水质量除以干质量。想象把每份材料都换算成“原来只有 1 g 干材料”的大小，留存水也按照相同比例缩放；商便告诉我们这个统一大小的样品会对应多少水。这里的 3 g/g 表示每克干材料对应 3 克留存水。它可以大于 1，因为水来自外部，干材料并不是水质量的上限。把这一比值写成百分数时是 300%，读者必须同时看到它的分母是干材料。

$$
q=\frac{m_a}{m_d}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 按干质量归一化的吸水量；g/g，质量相除后无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | 留存水质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | 正的干材料质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/88a00dfa266c2fd007f2ab5e.svg) | 把分子量按分母量归一化；要求分母非零 |

3.60 g÷1.20 g=3.00 g/g，即每1 g干材料对应3 g水。写成百分数为300%，分母仍是干材料。

如果想问湿样拿在手里时，有多少质量是水，就应改用湿样总质量作分母。相同的 3.60 g 水，占 4.80 g 湿样的四分之三，因此水质量分数为 75%。这两个结果说的是同一个样品：300% 与 75% 并不矛盾，变化的是参照物。生活中“增长了百分之多少”和“现在占总量的百分之多少”也经常被混用。程序把分子分母明确写出来，可以让这种差别一直保留到最终报告，而不被一个孤零零的百分号掩盖。

$$
w=\frac{m_a}{m_w}=\frac{q}{1+q}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 湿样中的水质量分数，无量纲；百分数显示为100w% |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | 留存水质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | 干材料与水的总净质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 水质量与干材料质量之比，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | 把干材料质量除以自身得到的单位比值，无量纲 |

湿样由干材料和水组成，故分子分母同除以干质量后得到q/(1+q)。本例3.60/4.80=3/(1+3)=0.75，显示为75%。

图中的两条曲线把分母的作用展示得更完整。固定干质量为 1.20 g，不断增加水质量，水与干质量的比值沿直线上升；水在湿样中的分数则逐渐接近 100%，因为新增的水同时增大了分子和分母。前者适合按原始材料量比较吸水程度，后者适合描述当前湿样的组成。写结果时选择哪一个，取决于想回答的问题。程序可以同时给出两个结果，文字和坐标轴则负责让读者知道自己正在看哪一种。

![固定干质量1.20 g，逐渐增加留存水。相同水质量对应的两种比例，因分母不同而呈现直线与弯曲关系。](https://ml-biomat.com/static/tutorials/python-scientific/figures/c6ae7228828963c2d66b34be.svg?v=c6ae72288289)

图 3固定干质量1.20 g，逐渐增加留存水。相同水质量对应的两种比例，因分母不同而呈现直线与弯曲关系。

## 从读得懂的表达式，到能连接工具的语言

Python 的出现与一个很实际的问题有关：怎样让人用较清楚的语句，调用计算机里已有的功能？Guido van Rossum 在 Python 官方问答中回顾，他曾参与 ABC 语言的实现，也在 Amoeba 分布式操作系统项目中工作。ABC 的一些语言设计有助于表达清晰，而系统工作又要求容易访问已有接口、处理运行中的错误。Python 的早期设计把这些需求放在一起；开发从 1989 年末开始，1991 年公开发布。这个历史背景解释了为什么一段语言可以既写简单算式，又逐渐连接文件、数值计算和图形工具。

对本章的学习而言，历史的关键并不是记住发布日期，而是理解“表达方法”和“执行工具”之间的分工。把干质量写成总读数减皮重，是一个人能读懂的科学关系；把这个关系写进 Python，便能让解释器重复执行。需要画图时，再引入专门的绘图库，不必自己安排屏幕上的每一个像素。类似于实验室里同一份样品可以依次进入天平、显微镜和分析软件，一份数值结果也可以进入不同工具，只要各工具之间对数据的含义有共同约定。

这里的“库”是已经写好、可以在程序中调用的一组功能。完整示例使用 Matplotlib 生成图形，它提供坐标轴、线条、文字和文件导出等能力；Python 自带的 `json` 模块把结果保存成一种结构清楚的文本格式。`import` 语句让程序能够使用这些功能。计算本身仍然是普通 Python 的相减与相除，绘图库接收结果后负责把它们画出来。把两者分开，有助于定位问题：比例错了应先查数据和算式，比例正确但文字被裁掉则应查图的布局。

这种工具协作也让第一段程序能自然长大。先处理一个样品，随后用列表保存多个样品，再用函数规定统一的计算方法，最后用数组和表格处理成批记录。每一步都增加一种能够解决新问题的表达手段，而前面的质量账仍然成立。学会一个库的意义也在这里：知道它把数据组织成什么对象、能够施加哪些操作，以及这些操作怎样对应自己的科学问题。只记函数名字，往往难以判断结果；先抓住对象和关系，陌生工具就有了可以理解的位置。

## 读懂输出，也学会检查一个看似正确的数

短程序的输出会给出干质量约 1.20 g、留存水约 3.60 g、按干质量归一化的吸水量约 3.00 g/g。若直接显示某些中间值，可能看见 `1.2000000000000002`。这是计算机用有限二进制位表示小数时留下的尾数，并不是天平突然测出了这么多位。下一章会解释它怎样产生；现在可以把“内部计算保留的值”与“为阅读而安排的显示位数”区分开。完整例子用三位小数显示克数，用一位小数显示百分数；输出格式改变了文字外观，没有重新测量样品。

`f"{dry_g:.3f} g"` 是一个格式化字符串。开头的 `f` 告诉 Python，在字符串中的花括号处填入表达式的值；`dry_g` 指定要放入哪个数，冒号后的 `.3f` 指定小数点后保留三位，最后的 `g` 是普通单位文字。百分数格式 `.1%` 会在显示时把无量纲比例乘以 100，并附加百分号，因此内部的 0.75 显示为 75.0%。先确认内部值是哪一种形式，便能避免把已经是 75 的数再次按百分数格式显示成 7500%。

检查程序时，可以从几条能用纸笔解释的关系开始。干样与容器相加应回到干态总读数；湿样与容器相加应回到湿态总读数；干材料与留存水相加应回到湿样质量。把湿态读数改为与干态相同，留存水应变为零，两种吸水比例也都应为零。再把全部称量值同时放大两倍，绝对质量变成两倍，而两个比例保持不变。这些检查对应质量拆分、零增量和尺度变化，比只看某一次结果是否“像是对的”更有说服力。

还应检查物理对象的取值范围。干样总读数必须大于容器质量，才能得到正的干质量作为分母；湿质量在本章纯吸水设定下应不小于干质量。如果输入不符合这些关系，优先回到称量记录、单位和实验过程查找原因。直接把负值改成零会改变记录，掩盖需要理解的变化。程序中的错误提示应指出哪个关系不成立，帮助下一步检查。页面实验把这些条件直接写在输入附近，使错误成为可解释的反馈，而不是一张看似平滑却没有物理意义的图。

## 运行完整例子：计算、画图与保存结果

下面的完整脚本同时包含计算和三幅图的生成代码，可以在本页连续阅读。最前面的三次称量及其运算，与前面短例子完全一致。随后设置字体和颜色，建立图形，最后把数值保存为 `summary.json`。JSON 文件中的键是字段名称，例如 `water_g`，对应值是可再次读取的数；这种结构比从一张图片里辨认数字更适合继续分析。SVG 图保留矢量线条和文字，适合放大阅读；PNG 图则以像素保存，方便在许多日常软件中查看。

### 完整计算与绘图脚本

依赖Matplotlib；计算使用Python内置数值。所有输出写入指定结果文件夹。

```
"""Mass accounting for a gel: a complete, deterministic teaching example."""
from pathlib import Path
import argparse
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en

    # Readings are constructed teaching data, all in grams.
    tare_g = 0.4
    dry_total_g = 1.6
    wet_total_g = 5.2
    dry_g = dry_total_g - tare_g
    wet_g = wet_total_g - tare_g
    water_g = wet_g - dry_g
    uptake_g_per_g = water_g / dry_g
    water_fraction = water_g / wet_g
    print(f"Dry material: {dry_g:.3f} g")
    print(f"Retained water: {water_g:.3f} g")
    print(f"Water per dry material: {uptake_g_per_g:.3f} g/g")
    print(f"Water fraction of wet specimen: {water_fraction:.1%}")

    available = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ["Noto Sans CJK SC", "Microsoft YaHei", "DejaVu Sans"] if f in available), "DejaVu Sans")
    plt.rcParams.update({"font.family": family, "font.size": 12, "axes.titlesize": 15,
                         "axes.titleweight": "bold", "svg.fonttype": "none",
                         "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6",
                         "text.color": "#172b36", "axes.labelcolor": "#172b36",
                         "axes.spines.top": False, "axes.spines.right": False})
    ink, dry_color, water_color, tare_color = "#172b36", "#b85336", "#28648a", "#bfc6c5"
    def save(fig, name):
        fig.savefig(args.output / f"{name}-{args.language}.svg", bbox_inches="tight")
        fig.savefig(args.output / f"{name}-{args.language}.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig = plt.figure(figsize=(12, 6.5), layout="constrained")
    grids = fig.add_gridspec(1, 2, width_ratios=[1.3, 1])
    ax = fig.add_subplot(grids[0])
    labels = [tr("空容器", "Container"), tr("干样 + 容器", "Dry + container"), tr("湿样 + 容器", "Wet + container")]
    ax.barh(labels, [tare_g]*3, color=tare_color, label=tr("容器", "Container"), height=.52)
    ax.barh(labels, [0,dry_g,dry_g], left=[tare_g]*3, color=dry_color, label=tr("干材料", "Dry material"), height=.52)
    ax.barh(labels, [0,0,water_g], left=[tare_g,tare_g,dry_total_g], color=water_color, label=tr("留存水", "Retained water"), height=.52)
    for i, value in enumerate([tare_g,dry_total_g,wet_total_g]):
        ax.text(value+.07, i, f"{value:.2f} g", va="center")
    ax.set(xlim=(0,6.3), xlabel=tr("天平总读数 / g", "Total balance reading / g"), title=tr("a  把每次称量拆开", "a  Account for each weighing"))
    ax.invert_yaxis(); ax.legend(loc="upper right", frameon=False)
    ax.grid(axis="x", alpha=.16); ax.set_axisbelow(True)
    ax = fig.add_subplot(grids[1]); ax.axis("off")
    ax.set_title(tr("b  同一份湿样中的质量", "b  Mass inside the wet specimen"), loc="left")
    ax.add_patch(Rectangle((.08,.28),.84,.42,facecolor=water_color,transform=ax.transAxes))
    ax.add_patch(Rectangle((.08,.28),.84*(1-water_fraction),.42,facecolor=dry_color,transform=ax.transAxes))
    ax.text(.08+.42*(1-water_fraction),.49,f"{dry_g:.2f} g",color="white",ha="center",va="center",transform=ax.transAxes,fontsize=15)
    ax.text(.08+.84*(1-water_fraction)+.42*water_fraction,.49,f"{water_g:.2f} g",color="white",ha="center",va="center",transform=ax.transAxes,fontsize=18)
    ax.text(.08,.80,tr(f"总湿质量 {wet_g:.2f} g，不含容器", f"Wet mass {wet_g:.2f} g, container removed"),transform=ax.transAxes)
    ax.text(.08,.15,tr(f"干材料 {1-water_fraction:.0%}  |  水 {water_fraction:.0%}", f"Dry material {1-water_fraction:.0%}  |  water {water_fraction:.0%}"),transform=ax.transAxes,fontsize=14)
    fig.suptitle(tr("构造称量数据：相减保留了什么？", "Constructed weighings: what remains after subtraction?"),fontsize=17)
    save(fig,"mass-accounting")

    fig, axes = plt.subplots(1,2,figsize=(12,5),layout="constrained")
    water_values = [i*.03 for i in range(201)]
    axes[0].plot(water_values,[v/dry_g for v in water_values],color=dry_color,lw=2.8)
    axes[0].scatter([water_g],[uptake_g_per_g],s=85,color=ink,zorder=3)
    axes[0].annotate(f"{water_g:.2f} / {dry_g:.2f} = {uptake_g_per_g:.2f}",(water_g,uptake_g_per_g),xytext=(1,4),arrowprops={"arrowstyle":"-","color":ink})
    axes[0].set(ylabel=tr("水 / 干材料（g/g）", "Water / dry material (g/g)"),title=tr("a  干质量作分母：直线", "a  Dry mass denominator: a line"))
    axes[1].plot(water_values,[100*v/(dry_g+v) for v in water_values],color=water_color,lw=2.8)
    axes[1].scatter([water_g],[100*water_fraction],s=85,color=ink,zorder=3)
    axes[1].axhline(100,color="#899496",ls="--",lw=1)
    axes[1].annotate(f"{water_g:.2f} / {wet_g:.2f} = {water_fraction:.0%}",(water_g,100*water_fraction),xytext=(1,30),arrowprops={"arrowstyle":"-","color":ink})
    axes[1].set(ylabel=tr("水 / 湿样（%）", "Water / wet specimen (%)"),ylim=(0,108),title=tr("b  湿质量作分母：逐渐接近100%", "b  Wet mass denominator: approaches 100%"))
    for ax in axes:
        ax.set(xlabel=tr("留存水质量 / g", "Retained water mass / g"),xlim=(0,6)); ax.grid(alpha=.16)
    fig.suptitle(tr(f"固定干质量 {dry_g:.2f} g：两种比例回答两个问题", f"Dry mass fixed at {dry_g:.2f} g: two ratios answer two questions"),fontsize=16)
    save(fig,"denominators")

    fig = plt.figure(figsize=(12,7),layout="constrained")
    ax = fig.add_subplot(); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7)
    ax.text(0,6.65,tr("a  一段表达式如何连接测量与报告", "a  Expressions connect measurements to reports"),fontsize=17,weight="bold")
    boxes=[(.1,4.3,3.2,1.35,f"dry_total_g = {dry_total_g}\ntare_g = {tare_g}",tare_color),
           (4.2,4.3,3.2,1.35,"dry_g = (\n dry_total_g - tare_g\n)",dry_color),
           (8.3,4.3,3.4,1.35,f"print(dry_g)\n{dry_g!r}",water_color)]
    for x,y,w,h,label,color in boxes:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=color,alpha=.13,edgecolor=color,lw=1.2))
        ax.text(x+.15,y+h/2,label,va="center",fontsize=13)
    for x in [3.35,7.45]: ax.add_patch(FancyArrowPatch((x,4.98),(x+.75,4.98),arrowstyle="->",mutation_scale=17,color=ink))
    ax.text(.1,3.72,tr("每次赋值读取当时的数值；修改输入后，需要重新执行后续计算。", "Each assignment reads current values. Changed inputs require recalculating dependent values."),fontsize=12)
    ax.text(0,2.95,tr("b  Python的起点：可读的语言，能连接已有工具", "b  Python's origins: readable language, access to existing tools"),fontsize=17,weight="bold")
    ax.text(.1,2.15,"ABC",fontsize=21,color=dry_color,weight="bold")
    ax.text(.1,1.55,tr("表达与组织容易阅读", "Readable expressions\nand program structure"),fontsize=13)
    ax.text(4.6,2.15,"Python",fontsize=25,color=ink,weight="bold")
    ax.text(4.6,1.55,tr("1989年开始开发\n1991年公开发布", "Development began in 1989\nPublic release in 1991"),fontsize=13)
    ax.text(8.5,2.15,"Amoeba",fontsize=21,color=water_color,weight="bold")
    ax.text(8.5,1.55,tr("访问操作系统的实际需求", "Practical access to\noperating-system services"),fontsize=13)
    ax.add_patch(FancyArrowPatch((2.6,2.2),(4.3,2.2),arrowstyle="->",mutation_scale=17,color=dry_color))
    ax.add_patch(FancyArrowPatch((8.2,2.2),(6.9,2.2),arrowstyle="->",mutation_scale=17,color=water_color))
    ax.text(.1,.45,tr("今天：少量清楚的Python语句，连接数据文件、数值库与绘图工具。", "Today: a few readable Python statements connect files, numerical libraries and plotting tools."),fontsize=13)
    save(fig,"program-history")
    summary={"dataset":"Constructed mass measurements in grams", "tare_g":tare_g,"dry_total_g":dry_total_g,"wet_total_g":wet_total_g,
             "dry_g":dry_g,"wet_g":wet_g,"water_g":water_g,"uptake_g_per_g":uptake_g_per_g,"water_fraction":water_fraction}
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")


if __name__ == "__main__":
    main()
```

把脚本保存为 `main.py` 后，在它所在的文件夹运行下面的命令。命令中的 `python` 选择解释器，`main.py` 是要执行的脚本，`--output output` 指定结果写入名为 `output` 的文件夹，`--language zh` 选择中文图内文字。文件夹可以理解为用于组织文件的容器；相对路径 `output` 从当前工作位置开始寻找，与某台电脑的固定目录无关。使用英文时，把末尾的 `zh` 改为 `en`。所需绘图库的安装与环境检查在第六章集中说明。

### 运行脚本

在脚本所在文件夹运行；两行分别生成英文和中文图。

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

代码中的 `def main():` 把完整流程放在一个函数中，缩进表示哪些语句属于这个函数；文件末尾的入口判断负责在直接运行脚本时调用它。此刻可以先把这个结构看作计算过程的外框，[第四章](https://ml-biomat.com/tutorials/python-scientific/p04/)会逐步解释如何自己写函数。阅读大一点的程序时，先找输入、主要计算和输出，再理解支撑它们的布局细节，会比按每个符号平均分配注意力更清楚。本例的科学计算只有几个变量，其余代码负责把同一结果以可靠、可读的方式展示出来。

运行结束后，先打开数值摘要核对三次读数和两个比例，再查看三幅图。第一幅应让你把总读数拆回各组成部分，第二幅解释分母变化如何改变曲线，第三幅把代码依赖和语言的设计背景连接起来。若修改输入，重新运行后这些输出应来自同一组新值。保留脚本和数值文件，便能够说明一幅图是怎样产生的；仅保存图片，则会丢掉使计算可以继续修改和检查的关系。

## 亲手改变读数，观察整个计算怎样响应

下面的实验把天平读数、质量拆分、两种归一化曲线和逐步计算放在一起。先保持容器与干态读数不变，只增加湿态读数：蓝色水质量部分会增长，按干质量归一化的点沿直线移动，水质量分数沿弯曲曲线移动。接着试着把三个读数同时加上 0.20 g，这相当于给各次称量增加同样的容器质量；净干质量、净湿质量和两个比例应全部保持原值。这个操作可以帮助你理解，正确扣除皮重为什么能够消除容器对结果的影响。

### 称量、组成与分母：联动实验

输入三次称量，查看质量拆分与两种比例。虚线保留原始干质量，方便判断变化来自水还是干材料。

[Figure: 称量质量组成](https://ml-biomat.com/tutorials/python-scientific/p01/#P01-mass)

[Figure: 干基与湿基比例曲线](https://ml-biomat.com/tutorials/python-scientific/p01/#P01-curves)

再做一次更有区分度的比较：把三个读数都乘以二，看看质量条与比例是否以同样方式变化。条形图以克为单位，显示绝对大小；两个比例以材料量作参照，显示组成或相对吸水程度。相同的比例并不意味着相同大小的样品，相同的水质量也不意味着相同的归一化吸水量。图、单位和变量名共同保留这些区别。完成这些尝试后，你已经不只是让程序“算出一个数”，而是在检查输入改变时，结果是否按照问题本身的结构发生变化。

可以给自己的第一段程序留下一个小任务：将干态总读数改为 2.40 g，湿态总读数改为 6.40 g，容器仍为 0.40 g，先手算，再运行。净干质量应为 2.00 g，水质量为 4.00 g，按干质量归一化为 2.00 g/g，湿样中的水占约 66.7%。用一句完整的话说明每个比例的分母，比只抄下答案更能检验理解。下一章将在这条主线上继续，讨论数字、单位和有限精度怎样影响计算，让程序里的数始终对应可以解释的量。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Software Carpentry — Variables and Assignment](https://swcarpentry.github.io/python-novice-gapminder/02-variables.html)

   沿用变量与执行顺序的教学方法，改写为原创称量案例与联动图。Copyright The Carpentries；CC BY 4.0。

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; adapted instructional structure, original prose/code/figures.
2. [Python 3.14 Tutorial — An Informal Introduction](https://docs.python.org/3.14/tutorial/introduction.html)

   算术、赋值、字符串与print的语言参考。

   Python Software Foundation documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Using the Interpreter](https://docs.python.org/3.14/tutorial/interpreter.html)

   交互执行与脚本执行的区别。

   PSF documentation license.
4. [Python FAQ — Why was Python created?](https://docs.python.org/3/faq/general.html#why-was-python-created-in-the-first-place)

   Guido van Rossum关于ABC、Amoeba与Python起源的公开回顾。

   PSF documentation license; original historical diagram.
