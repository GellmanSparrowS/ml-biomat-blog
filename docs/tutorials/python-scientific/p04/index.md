# 把重复操作写成可靠的函数

Source: https://ml-biomat.com/tutorials/python-scientific/p04/
Language: zh-CN

从一条质量记录追踪到整批结果，看清参数、分支、循环与返回值。

## 让同一套计算走过每个样品

整理好六条实验记录以后，我们希望对每个样品计算吸液量，同时保留缺少称量的记录。最直接的办法，是把同一行减法和除法复制六遍，再逐个改变量名。但当样品增加到六十个，或者需要调整一次质量检查规则时，每一份复制出来的代码都要重新核对。本章把一个样品的计算写成函数，再用循环把记录逐条送进去。学完以后，你会得到一份包含每条记录状态、计算结果和累计统计量的处理程序，也能沿着执行过程解释某个结果为什么出现。

这里继续使用上一章的六条构造记录。A01的干、湿质量为1.20和4.80 g，A02为1.00和3.40 g，A03为0.80和2.80 g，B01为1.20和3.60 g，B02的干质量为1.00 g而湿质量缺失，B03为0.80和2.32 g。质量均已扣除容器；本例把干物质质量视为固定参照，湿减干的增加量按所吸收液体计。液体可以含有溶解组分，因此统一称为吸液量。本章研究程序怎样处理这些记录，处理顺序并不是实验时间，也不把先后记录解释为同一样品逐渐吸液的过程。

函数可以想成一张有明确输入栏和输出栏的计算单。输入栏写“干质量，g”和“湿质量，g”，内部规定如何检查、如何相减和相除，输出栏给出“每克干物质对应的液体质量，g/g”。每换一个样品，只换输入栏，计算规则保持一致。这个类比也提醒我们：写好一张计算单，并不等于已经拿它算过某个样品。Python中的函数定义和函数调用，正对应制定规则和使用规则这两个动作。

## 定义、调用与返回值，分别发生了什么？

下面先写一个只包含算式的短函数。`def`告诉Python要定义函数，后面的`uptake_simple`是我们取的名字。括号里的`dry_g`和`wet_g`是参数，表示函数每次工作时需要接收两个对象。冒号引出函数体，缩进的下一行属于这个函数。通常每级使用四个空格；缩进在Python中表达代码的归属，直接决定哪些语句在一次调用中执行，不能只把它当排版。

### 先定义，再传入两个质量

依次打印3.0与2.4，单位均为g/g。

```
def uptake_simple(dry_g, wet_g):
    return (wet_g - dry_g) / dry_g

q = uptake_simple(1.2, 4.8)
print(q)
print(uptake_simple(wet_g=3.4, dry_g=1.0))
```

执行定义时，Python把函数对象与名字关联起来，先不代入质量。执行`uptake_simple(1.2, 4.8)`时，数值1.2交给第一个参数，4.8交给第二个参数；这两个传入的具体对象叫实参。函数内部计算后，`return`把结果交回调用位置，因此赋值语句把3.0保存在`q`里。若写成`uptake_simple(wet_g=4.8, dry_g=1.2)`，参数名已经写明，传入顺序可以改变。质量相近时，两个位置写反未必一眼就能看出来，使用关键字实参能让调用处直接展示量的含义。

`return`与`print`承担不同工作。返回值可以继续参与求平均、绘图或保存；打印只负责把一段文字显示给人看。若把函数最后一行改成`print(...)`而没有返回语句，屏幕上仍可能出现3.0，但赋给`q`的将是`None`。这时再拿`q`参与除法就会出错。完整程序把计算与显示分开：函数返回可继续使用的结果，外层程序决定何时打印、画图和写文件。

函数中的参数属于这次调用的局部名字。第一次调用里的`dry_g`是1.2，第二次可以是1.0，不需要先把第一次的名字手动清空。外面即使存在同名变量，也不等于函数会自动使用它。通过参数传入所需信息，能从一行调用看清计算依赖。对于列表和字典还要注意，传入的对象可以被多个名字共享；在函数中修改字典内容会影响共享它的外部记录。本例为每条结果先创建浅复制，因为字段值都是数字、字符串或`None`，这样添加结果字段不会改写原始记录。

参数名中的`_g`还把输入约定留在了最容易看到的地方。Python不会因为名字里写了g就自动把毫克换算成克：若干质量传入1200而湿质量传入4.8，函数看到的只是两个数，必须由入口检查或数据读取步骤发现单位不一致。把两者都换成毫克虽然比值不变，但记录中的单位字段和函数说明也要随之改变。函数开头三引号中的文字叫文档字符串，可以通过`help(uptake)`查看；它适合写清物理量、单位、返回值以及缺失如何处理，让计算约定随函数一起保存。

## 子程序曾经解决的，是科学计算中的重复劳动

函数背后的复用思想，早于Python很多年。剑桥计算机实验室的历史记载，1948—1949年的EDSAC程序研究已经包括Wheeler的闭合子程序和子程序库；到1950年，库程序中有Gill的Runge–Kutta计算程序和Wheeler的浮点运算程序。1951年，Wilkes、Wheeler和Gill出版了程序编制著作。这里与今天最直接的联系，是把一段经常使用的计算组织成可调用的单元，让主程序带着数据进入，完成后回到原来的计算流程。

想象一个数值计算中先后需要多次求相同类型的数学结果。每处重新写一遍指令，修改时就会产生多处工作；跳到一份公共程序执行，则需要知道“输入放在哪里”和“完成后回到哪里”。输入约定与返回约定共同决定这份计算能否被稳定复用。现代Python替我们处理了大量底层细节，括号中的参数和`return`仍然保留着这两个清晰的接口。图中的箭头按本章吸液量函数绘制，用来解释调用关系，不是对EDSAC机器指令的复刻。

![从早期子程序的复用问题理解现代函数。两次调用携带各自的质量进入同一份定义，并把结果返回各自调用处；图为原创原理示意。](https://ml-biomat.com/static/tutorials/python-scientific/figures/7d551905bf9a110be8a34bae.svg?v=7d551905bf9a)

图 1从早期子程序的复用问题理解现代函数。两次调用携带各自的质量进入同一份定义，并把结果返回各自调用处；图为原创原理示意。

在科研程序里，复用的收益还体现在解释上。读到`uptake(dry_g=1.2, wet_g=4.8)`，我们可以立即知道当前在求什么，再进入函数查看质量定义和处理规则。若把所有读取、换算、筛选、统计和绘图都塞在一个很长的函数里，这种帮助会减弱。一个实用的分法是让单样品函数负责量的定义，让批处理函数负责记录和状态，让绘图部分负责显示结果。它们之间传递有明确含义的值，阅读者就能逐层追踪。

## 把计算成立的条件写在入口处

吸液量的分母是干质量。一个完整函数需要先保证它是有限的正数，再检查湿质量是否提供。这里“有限”指既不是正负无穷，也不是表示未定义数值的`NaN`；`math.isfinite`负责这项检查。`None`则表示尚未提供湿质量，是一种明确的缺失标记。两者虽然都不能直接当作有效质量参与本例计算，却有不同含义：一个是数值状态，一个是记录中的缺项。

$$
q=\frac{m_w-m_d}{m_d},\qquad m_d>0,\quad m_w\ge m_d
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 按干质量归一化的吸液量，g/g，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | 净湿质量，g；缺失时保留None |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | 净干质量，g；有限且大于零 |
| ![Formula](https://ml-biomat.com/static/agent-math/16df88788b1d832b83b1bd9b.svg) | 先相减得到留存液体质量，再除以干质量 |
| ![Formula](https://ml-biomat.com/static/agent-math/604114aa9f8783cbc02b7d55.svg) | 大于，以及大于或等于；限定本例质量账本的有效输入 |

干物质质量固定时，A01留存液体为4.80−1.20=3.60 g；3.60/1.20=3.00 g/g。干、湿质量同时加倍后，(9.60−2.40)/2.40仍为3.00 g/g。

在函数里，`if`后面放一个能够判断真假的条件。条件成立，就执行其下缩进的语句；否则继续向下。`dry_g <= 0`检查干质量是否小于或等于零，`not`把真假取反，`or`表示两个条件有一个成立就进入分支。先检查干质量再检查湿质量缺失，意味着即使湿质量尚未提供，零干质量也会被指出。这是我们为当前记录约定的检查顺序，写出来以后，每个样品都遵守相同规则。

湿质量为`None`时，函数直接`return None`，本次调用在这里结束，后面的减法不会执行。湿质量存在但小于干质量时，函数发出`ValueError`并附上具体信息。因为本例采用干物质质量保持不变的吸液账本，负增量需要检查样品对应、称量和物质损失；若研究对象本来就在溶解或降解，就应建立同时描述固体损失与液体进入的质量模型。条件来自测量定义，不能用一个“总取绝对值”的操作把不符合定义的数据改成看似合适的正数。

完整例子用`try`包住单样品计算，用`except ValueError`接收已知的数值检查问题，然后在结果记录里保存编号、状态和原因。这样，一条待核对的记录不会使其他独立样品的计算全部丢失。缺失与无效仍分别写成`missing`和`invalid`，不混为一种情况。字段名拼错产生的`KeyError`没有被这段处理吞掉，会继续指出程序或数据结构问题；我们处理的是明确预期的记录状态，而不是把所有报错都当成空值。

## 循环一次，只处理当前的一条记录

`for record in records:`可以读作“依次从记录列表中取出一条，暂时叫它record”。第一轮它指向A01，第二轮指向A02，直到列表耗尽。每轮先复制当前记录，再调用函数，把结果和状态添加到副本中，最后用`append`加入结果列表。循环开始前，`results = []`只创建一次空列表；如果把这句缩进到循环内部，就会在每轮重新建立列表，前面的结果无法累计。查看缩进位置，常常比盯着最后一个数值更快发现这类问题。

程序使用`enumerate(records, start=1)`同时得到步骤号与记录。步骤号从1开始，方便人阅读；列表本身的位置索引仍从0开始，两者没有冲突。只需要处理每条记录时，直接遍历记录比先生成索引再反复查找更清楚。`range(6)`生成的是0到5六个整数，适合确实需要一组整数步骤的场合；它的终点不包含在内。选择循环写法时，先问这一轮需要的是记录本身，还是记录的位置，就能避免绕远路。

![六条构造记录的逐步执行。缺少湿质量的第五条保留在结果表中，却不增加有效数；下图横轴是计算步骤，数值由完整程序计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0054ece765349decf8950d46.svg?v=0054ece76534)

图 2六条构造记录的逐步执行。缺少湿质量的第五条保留在结果表中，却不增加有效数；下图横轴是计算步骤，数值由完整程序计算。

图中第五条B02缺少湿质量，函数返回`None`。结果表仍保留这一条，因此已处理记录数从4增加到5；参与统计的有效数却仍为4，累计均值也保持2.475 g/g。处理B03后，有效数变为5，五个吸液量相加为11.8 g/g，均值为2.36 g/g。曲线横轴是程序已处理的记录数，表示统计结果随记录加入怎样变化。这里把两个处理组放在一起，是为了跟踪程序状态；若研究问题是比较处理条件，就应像上一章那样分别汇总各组。

$$
\bar q_k=\frac{1}{n_k}\sum_{i\in V_k}q_i\quad(n_k>0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 已经处理的记录数，非实验时间，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec1501006f8037f1c7ffd945.svg) | 前k条记录中已得到有效数值的样品索引集合 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 集合内的样品索引，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | 集合V_k包含的有效值数量，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | 第i个样品的吸液量，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/f5666e2316365712884fc0f6.svg) | 当前所有有效样品等权的累计均值，g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/99c8b956831093e4e1e9a7c9.svg) | 依次相加；只选属于有效集合的索引 |

第四步：(3.0+2.4+2.5+2.0)/4=2.475 g/g。第五步B02缺失，集合与计数不变；第六步加1.9，得到11.8/5=2.36 g/g。若n_k为0，均值返回None。

每完成一轮，都可以用一句话核对程序状态：“结果列表的长度等于已经处理的记录数，有效值列表只收录已经得到数值的样品。”这样的关系称为循环不变量：输入虽在变化，关系每一轮都应成立。它比只检查最终均值更容易定位问题。若第五轮突然出现五个有效值，就应回到缺失值分支；若第六轮结果表只有一条，就应检查列表是否在循环里被重新创建。理解循环，是学会同时看当前记录和累积状态。

特别要留意`return`写在哪一层。若把`return results`放在循环体内，函数处理第一条记录后就会结束，剩下的五条不会进入下一轮；放在循环之后，才表示“所有记录处理完后交回结果”。`continue`则只跳过当前这一轮剩余部分，继续下一条记录；`break`结束当前循环，却不一定结束整个函数。本例没有用后两者，因为每条记录都需要添加状态并进入轨迹，按顺序完成这些步骤更容易检查。选择控制语句时，要先想清楚想结束的是哪一层工作。

## 一个函数，既要检查答案，也要检查关系

第一个检查可以是手算过的小例子：干质量1.20 g、湿质量4.80 g，应得到3.00 g/g。第二个检查是边界情况：干、湿质量相等时，增量为零，函数应返回数值0.0；湿质量缺失时则返回`None`。这两种结果在统计中处理不同，前者要计入有效数，后者不计入。第三个检查关注无效输入：干质量为零或者湿质量小于干质量时，应走到明确的质量检查分支，而不是继续生成结果。

还可以不指定某个最终数，而检查一组输入之间必然成立的关系。若把干、湿质量同时乘以2，增量与分母也同时乘以2，比值不变；所以1.20、4.80 g与2.40、9.60 g都对应3.00 g/g。左图把一组干、湿质量组合逐点代入同一个函数，颜色代表返回的吸液量，白色线表示相同输出。右图沿着共同缩放两种质量的方向取点，得到水平线。图形既展示函数作用，也让错误的归一化分母更容易被发现。

读这个颜色图时，可以先找一个容易手算的位置：干质量1.00 g、湿质量4.00 g，差值3.00 g，因此落在标为3的等值线上。同一条线上的0.80、3.20 g也返回3，而固定干质量1.00 g、把湿质量改为3.00 g，输出就降到2。颜色表示的是函数结果，没有表示测量概率或实验出现次数。每一个颜色格来自一组明确输入，空白区则保留了当前模型不接收的组合；有了坐标和定义，图才成为可读的计算地图。

![同一吸液量函数作用于不同干、湿质量组合。等值线连接输出相同的组合；空白区对应湿质量低于干质量。共同缩放两种质量时，比值不变。](https://ml-biomat.com/static/tutorials/python-scientific/figures/558a473bf37863c1631bd1f0.svg?v=558a473bf378)

图 3同一吸液量函数作用于不同干、湿质量组合。等值线连接输出相同的组合；空白区对应湿质量低于干质量。共同缩放两种质量时，比值不变。

完整程序用`assert`写下若干可以立即检验的预期。条件不成立时，程序会给出断言错误，提醒我们返回检查实现。浮点比值使用`math.isclose`比较，避免把最后几位舍入差异误当成公式错误；零值、`None`和字典结构则可以按它们的含义直接比较。入口处的数据检查仍写成明确的`if`与`raise`：Python优化运行时可以移除断言，因此断言适合表达开发时的自检，正式输入规则由函数本身承担。

空集合也值得单独想清楚。`summarize([])`收到空列表时，有效数为0，均值返回`None`。它没有足够对象去定义平均数；返回0会错误地表达“已经测得平均吸液量为零”。我们为汇总函数返回一个字典，同时保存计数和均值，这样后续显示时能区分没有结果与结果恰好为零。好的函数接口不仅给出一个数，还保留解释这个数所需的最小信息。

## 从单样品函数接到完整分析

下面的程序先定义`uptake`、`summarize`和`analyze`，再在`main`里组织输入、验证、绘图和保存。`analyze`返回两个对象，调用处用`results, trace = analyze(records)`把它们分别接住。前一个是逐样品结果，后一个是执行轨迹。把这两种输出分开后，同一份结果可以用于报告，轨迹可以用于理解和排查处理过程，不必从打印文字中重新猜测计算状态。

### 完整函数、批处理与科学图

计算使用Python标准库，科学图由Matplotlib生成。

```
"""Trace reusable calculations over a small set of teaching specimens."""
from pathlib import Path
import argparse
import json
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def uptake(dry_g, wet_g):
    """Return retained-liquid mass per dry mass, or None if wet mass is absent.

    Masses are net specimen masses in grams. This example assumes no loss
    of dry material. Invalid mass accounting raises ValueError.
    """
    if not math.isfinite(dry_g) or dry_g <= 0:
        raise ValueError("dry_g must be finite and positive")
    if wet_g is None:
        return None
    if not math.isfinite(wet_g) or wet_g < dry_g:
        raise ValueError("wet_g must be finite and at least dry_g")
    return (wet_g - dry_g) / dry_g


def summarize(values):
    """Return the count and equally weighted mean of available values."""
    valid = [value for value in values if value is not None]
    return {"valid_count": len(valid),
            "mean": math.fsum(valid) / len(valid) if valid else None}


def analyze(records):
    """Return new result records and an execution trace, preserving inputs."""
    results, trace, available = [], [], []
    for step, record in enumerate(records, start=1):
        item = record.copy()
        try:
            value = uptake(record["dry_g"], record["wet_g"])
            status = "missing" if value is None else "valid"
            reason = "wet mass absent" if value is None else "calculated"
        except ValueError as error:
            value, status, reason = None, "invalid", str(error)
        item.update(uptake_g_per_g=value, status=status, reason=reason)
        results.append(item)
        if value is not None:
            available.append(value)
        trace.append({"step": step, "id": record["id"], "status": status,
                      "returned": value, "valid_count": len(available),
                      "sum": math.fsum(available),
                      "mean": summarize(available)["mean"]})
    return results, trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(a, b): return a if zh else b
    records = [
        {"id":"A01", "dry_g":1.2, "wet_g":4.8},
        {"id":"A02", "dry_g":1.0, "wet_g":3.4},
        {"id":"A03", "dry_g":0.8, "wet_g":2.8},
        {"id":"B01", "dry_g":1.2, "wet_g":3.6},
        {"id":"B02", "dry_g":1.0, "wet_g":None},
        {"id":"B03", "dry_g":0.8, "wet_g":2.32},
    ]
    results, trace = analyze(records)
    assert math.isclose(uptake(1.2, 4.8), 3.0)
    assert math.isclose(uptake(2.4, 9.6), uptake(1.2, 4.8))
    assert uptake(1.0, 1.0) == 0.0
    assert uptake(1.0, None) is None
    assert summarize([]) == {"valid_count": 0, "mean": None}
    invalid_examples = []
    for dry, wet in [(0.0, 1.0), (1.0, 0.5), (float("nan"), 2.0)]:
        try:
            uptake(dry, wet)
        except ValueError as error:
            invalid_examples.append({"reason": str(error)})
        else:
            raise AssertionError("An invalid input was accepted")
    assert "status" not in records[0]
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ["Noto Sans CJK SC", "Microsoft YaHei", "DejaVu Sans"] if f in fonts), "DejaVu Sans")
    plt.rcParams.update({"font.family":[family,"DejaVu Sans"] if zh else ["DejaVu Sans","Arial"],"font.size":12,"axes.titlesize":15,"axes.titleweight":"bold","svg.fonttype":"none","figure.facecolor":"#fbfaf6","axes.facecolor":"#fbfaf6","text.color":"#172b36","axes.labelcolor":"#172b36","axes.spines.top":False,"axes.spines.right":False})
    ink, blue, red, green = "#172b36", "#28648a", "#b85336", "#467a62"
    def save(fig, name):
        fig.savefig(args.output/f"{name}-{args.language}.svg", bbox_inches="tight")
        fig.savefig(args.output/f"{name}-{args.language}.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig = plt.figure(figsize=(12,8), layout="constrained")
    gs = fig.add_gridspec(2,1,height_ratios=[1.4,1])
    ax = fig.add_subplot(gs[0]);ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.15,6.6,tr("a  每次循环保留输入、分支与返回值","a  Each iteration retains inputs, branch, and return"),fontsize=17,weight="bold")
    headers=[tr("步骤","Step"),"ID",tr("干 / 湿质量 (g)","Dry / wet mass (g)"),tr("分支","Branch"),tr("返回 (g/g)","Return (g/g)"),tr("有效计数","Valid count")]
    xs=[.2,1.2,2.5,6.2,8.4,10.5]
    for x,h in zip(xs,headers):ax.text(x,5.8,h,fontsize=12,weight="bold")
    for i,(r,t) in enumerate(zip(records,trace)):
        y=5.1-i*.75;color=red if t["status"]=="missing" else blue
        ax.add_patch(Rectangle((.1,y-.2),11.7,.65,color=color,alpha=.065))
        wet="None" if r['wet_g'] is None else f"{r['wet_g']:.2f}"
        vals=[str(i+1),r['id'],f"{r['dry_g']:.2f} / {wet}",tr("缺失","Missing") if t['status']=='missing' else tr("计算","Calculate"),'None' if t['returned'] is None else f"{t['returned']:.2f}",str(t['valid_count'])]
        for x,v in zip(xs,vals):ax.text(x,y,v,color=color,fontsize=13)
    ax = fig.add_subplot(gs[1]);steps=[t['step'] for t in trace]
    ax.plot(steps,[t['mean'] for t in trace],color=blue,marker='o',lw=2,label=tr('累计样品均值','Running specimen mean'))
    ax.axvspan(4.7,5.3,color=red,alpha=.1)
    ax.annotate(tr('第5条缺失：计数与均值保持','Record 5 missing: count and mean unchanged'),(5,trace[4]['mean']),xytext=(3.0,3.15),arrowprops={'arrowstyle':'->','color':red},fontsize=12,color=red)
    ax.set(xticks=steps,xlabel=tr('已处理记录数','Records processed'),ylabel=tr('累计均值 / g·g⁻¹','Running mean / g·g⁻¹'),ylim=(2.2,3.35),title=tr('b  跟踪计算顺序；不是随时间的吸液曲线','b  A computational trace, not an uptake time curve'));ax.grid(alpha=.15)
    save(fig,'execution-trace')

    fig=plt.figure(figsize=(12,6.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.2,1])
    ax=fig.add_subplot(gs[0]);dry_values=[.5+i*.025 for i in range(61)];wet_values=[.5+i*.05 for i in range(111)]
    field=[[uptake(d,w) if w>=d else math.nan for d in dry_values] for w in wet_values]
    mesh=ax.pcolormesh(dry_values,wet_values,field,shading='auto',cmap='cividis',vmin=0,vmax=11)
    contours=ax.contour(dry_values,wet_values,field,levels=[0.5,1,2,3,5,8],colors='white',linewidths=.8)
    ax.clabel(contours,fmt='%g',fontsize=11);ax.plot([.5,2],[.5,2],color=red,lw=2)
    ax.text(1.1,.75,tr('检查质量账本','Check mass accounting'),color=red,fontsize=11,rotation=25)
    ax.scatter([1.2, .8],[4.8,3.2],s=80,facecolors='none',edgecolors='white',linewidths=2)
    ax.set(xlabel=tr('干质量 / g','Dry mass / g'),ylabel=tr('湿质量 / g','Wet mass / g'),title=tr('a  函数的输入平面与输出','a  An input plane and its output'))
    fig.colorbar(mesh,ax=ax,label=tr('吸液量 / g·g⁻¹','Uptake / g·g⁻¹'),shrink=.8)
    ax=fig.add_subplot(gs[1]);scales=[.5+i*.05 for i in range(31)]
    ax.plot(scales,[uptake(1.2*k,4.8*k) for k in scales],color=blue,lw=2)
    ax.scatter([.5,1,2],[3,3,3],s=65,color=blue)
    ax.set(xlabel=tr('同时缩放两种质量的倍数','Factor applied to both masses'),ylabel=tr('吸液量 / g·g⁻¹','Uptake / g·g⁻¹'),ylim=(0,4),title=tr('b  比一个答案更强的关系检查','b  Check a relationship, not one answer'))
    ax.text(.55,.65,tr('干、湿质量同时加倍\n相减结果与分母都加倍\n比值保持 3 g/g','Double both masses:\nthe difference and denominator\nboth double; the ratio stays 3 g/g'),fontsize=13)
    ax.grid(alpha=.15);save(fig,'function-domain')

    fig=plt.figure(figsize=(12,7),layout='constrained');ax=fig.add_subplot();ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.2,6.65,tr('复用的关键：带着输入进入，带着结果返回','Reuse: enter with inputs, return with a result'),fontsize=19,weight='bold')
    ax.text(.2,6.05,tr('EDSAC：1948–49年的子程序研究 → 今天的函数调用示意','EDSAC subroutine work, 1948–49 → a modern function-call illustration'),fontsize=13)
    for i,(label,inputs,result) in enumerate([('A01','1.20 g, 4.80 g','3.00 g/g'),('A02','1.00 g, 3.40 g','2.40 g/g')]):
        y=4.9-i*2.5
        ax.add_patch(Rectangle((.3,y-.6),3.1,1.2,facecolor=blue,alpha=.1));ax.text(.5,y+.15,f'{label} → uptake(...)',fontsize=16);ax.text(.5,y-.3,inputs,fontsize=14)
        ax.add_patch(FancyArrowPatch((3.6,y+.25),(7.2,3.55),arrowstyle='->',connectionstyle=f'arc3,rad={-.2 if i==0 else .2}',mutation_scale=18,color=blue,lw=2))
        ax.add_patch(FancyArrowPatch((7.2,3.15),(3.6,y-.25),arrowstyle='->',connectionstyle=f'arc3,rad={.25 if i==0 else -.25}',mutation_scale=18,color=red,lw=2))
        ax.text(4.0,y+.3,tr('传入参数','Pass arguments'),fontsize=12,color=blue,bbox={'facecolor':'#fbfaf6','edgecolor':'none','pad':1.5})
        ax.text(4.0,y-.5,tr('返回','Return')+' '+result,fontsize=13,color=red,bbox={'facecolor':'#fbfaf6','edgecolor':'none','pad':1.5})
    ax.add_patch(Rectangle((7.4,2.35),4.2,2.3,facecolor=green,alpha=.1,edgecolor=green))
    ax.text(7.7,4.18,'def uptake(dry_g, wet_g):',fontsize=14,weight='bold')
    ax.text(7.7,3.6,tr('检查输入与缺失','Check inputs and missing data'),fontsize=14)
    ax.text(7.7,3.05,'return (wet_g - dry_g) / dry_g',fontsize=13)
    ax.text(.3,.45,tr('同一份定义；两次调用具有各自的局部参数。图为原理示意，并非EDSAC指令。','One definition; two calls with separate local parameters. Conceptual diagram, not EDSAC instructions.'),fontsize=12)
    save(fig,'subroutine-history')
    summary={'dataset':'Constructed six-specimen uptake records','record_count':len(records),**summarize([r['uptake_g_per_g'] for r in results]),'sum':math.fsum(r['uptake_g_per_g'] for r in results if r['uptake_g_per_g'] is not None),'missing_ids':[r['id'] for r in results if r['status']=='missing'],'invalid_examples':invalid_examples,'empty_summary':summarize([]),'scaling_check':uptake(2.4,9.6),'trace':trace}
    for name,data in [('summary',summary),('results',results),('records',records)]:
        (args.output/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    print(json.dumps({k:summary[k] for k in ['record_count','valid_count','sum','mean','missing_ids']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
```

读完整程序时，可以先沿数据流走一遍：记录进入`analyze`，质量进入`uptake`，有效值进入`summarize`，结果与轨迹进入绘图。绘图样式、颜色和保存设置集中在后面，它们使用已经算好的量。末尾的`if __name__ == '__main__':`让文件直接运行时调用`main()`；以后从别的程序导入其中的函数时，就不会同时触发整套绘图。下一章读取文件时，这种组织会继续发挥作用。

汇总函数中的`[value for value in values if value is not None]`叫列表推导式，可以展开成“先创建空列表，再逐项检查，不是None就添加”。它把一个简单的筛选循环写在一行里，并没有改变缺失规则。阅读时从`for`开始，再看条件，最后看最前面放入新列表的表达式，通常更容易理解。较长的计算分支仍用普通循环写清楚；代码行数少并不是目的，能把每个输出追溯到输入才是这里需要的能力。

### 保存两种语言的输出

输出目录包含三幅图、输入记录、结果和摘要。

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

运行后的摘要给出6条记录、5个有效值、总和约11.8和均值2.36，缺失编号为B02。JSON文件中的长小数反映浮点表示，图中按阅读需要保留两到四位。三个图文件分别展示逐条执行、输入平面和调用关系；`records.json`保留输入，`results.json`保留各条状态，`summary.json`保留汇总与轨迹。把显示精度和实际保存的数据分开，既便于阅读，也保留了重新检查的空间。

函数默认参数是一个常见便利，例如`enumerate(..., start=1)`中的`start`有默认值，我们在这里显式改成1。自己设计函数时，可以给常用且含义稳定的选项设置默认值，却仍应让质量、单位和处理规则在接口处清楚可见。列表这类可变对象不宜直接写成用来不断追加的默认值，因为默认对象会在多次调用之间共享；需要新列表时，可以默认传入`None`，再在函数内部创建。理解“名字与对象”的关系，能够把上一章的复制问题和本章的函数调用连起来。

函数大小可以用“是否能说清它负责的一个问题”来判断。吸液量函数回答单个样品的量怎样定义，汇总函数回答有几个有效值以及等权均值是多少，批处理函数把记录与这些操作接起来。每一层都能先用少量输入单独理解，再连接成完整流程。以后实验需要改变质量模型时，可以集中修改单样品计算，同时重新核对记录状态和统计含义，而不用从所有绘图语句里寻找散落的减法与除法。

练习时可以先只运行函数定义和一次调用，确认结果后再加入循环；如果改动后出现问题，也沿相反方向缩小范围，从整批结果回到出错样品，再回到它的两个质量。保留这两个具体输入，就能反复复现同一个问题。这样的调试与实验中保留原始样品条件相似：问题被缩小到可重复的一次计算以后，修改是否起作用就容易判断。

## 自己走一遍：下一条记录会改变什么？

下方实验先停在零条记录的状态。按“下一条”时，表格、当前分支和累计曲线一起前进一步；按“全部处理”可以查看最终结果。先保持默认输入，在处理B02以前预测有效计数与均值是否会变化，再用第五步检验预测。接着给B02补上2.80 g湿质量，重新执行，观察它从缺失记录变成有效记录，并比较新的总均值。每次修改输入都会从头开始，保证已显示的轨迹始终来自当前这一批数据。

### 执行台：一条记录怎样进入累计结果？

先逐条运行默认记录，再修改一个样品。输入变化会重启轨迹；“重新执行”保留修改，“恢复数据”恢复原始六条记录。

[Figure: 当前函数分支和累计均值曲线](https://ml-biomat.com/tutorials/python-scientific/p04/#P04-plot)

左侧高亮当前调用结束的位置；绿色表示已通过的判断。右侧蓝点来自有效返回，红点对应没有新增数值的步骤；灰色位置尚未处理。均值中每个有效样品等权。

| 步 | ID | 干质量 | 湿质量 | 状态 | 返回 | 有效数 | 均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |

还可以把A01的湿质量改成与干质量相同，观察0.00如何计入有效数；再把它改为小于干质量，观察无效状态怎样保留编号和原因。图中的灰色位置表示尚未处理，红色分支区分缺失与需核对记录，蓝色点给出已产生的累计均值。记录处理完毕后，回到最开始的函数定义，试着逐行说明这一次执行在哪个`return`结束，或者在哪个检查处发出异常。能用具体输入讲清执行路径，函数和循环就从语法变成了可以掌握的计算工具。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Software Carpentry — Writing Functions](https://swcarpentry.github.io/python-novice-gapminder/16-writing-functions.html)

   沿用先定义、调用，再连接返回值的教学顺序；改为原创样品计算。Copyright The Carpentries。

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; original case, prose, code and figures.
2. [Python 3.14 — More Control Flow Tools](https://docs.python.org/3.14/tutorial/controlflow.html)

   条件、循环、函数参数、局部名字与默认值的语言参考。

   PSF documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Errors and Exceptions](https://docs.python.org/3.14/tutorial/errors.html)

   明确发出与接收预期异常。

   PSF documentation license
4. [University of Cambridge — A Brief Informal History of the Computer Laboratory](https://www.cl.cam.ac.uk/events/EDSAC99/history.html)

   EDSAC子程序研究、科学计算库与1951年程序编制著作的历史事实。

   Historical factual reference; copyright University of Cambridge. Original diagram; no reproduced source illustration.
