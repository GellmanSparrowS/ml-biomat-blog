# 随机数怎样帮助理解测量

Source: https://ml-biomat.com/tutorials/python-scientific/p09/
Language: zh-CN

重复完整的测量过程，分别观察平均值的波动、固定偏差与共有条件。

## 多测几次，究竟改善了什么？

用同一把测厚仪连续测量一块薄片，显示值可能在1.18、1.23、1.20 mm附近变化。把十六次读数平均，通常比随手选一次更稳定；但如果仪器始终多读0.03 mm，多测几次也会保留这份偏差。本章用NumPy生成明确规则下的随机读数，让这两个现象同时可见。我们会比较一次、四次、十六次和六十四次读数的平均结果，观察分布怎样变窄，再加入固定偏差与同次测量共有的偏移，判断增加重复次数能够改善哪部分误差。

整个例子设定薄片真实厚度为1.20 mm，单次独立读数的波动标准差为0.04 mm。程序开展4000次模拟实验，每次最多生成64个读数。这些是根据给定数学模型计算的模拟数据；设定的真值与波动大小使我们能够同时检查随机结果和解析关系。实际测量的波动范围则需要来自仪器、校准记录和实验条件的估计。模拟的作用，是先把不同误差机制拆开，再观察它们在平均值中怎样组合。

这里有两个不能混淆的数目：每次实验读多少次，以及把整次实验重复模拟多少遍。前者决定一个平均值用了多少观测，后者决定我们能多清楚地看见平均值可能形成的分布。把一份十六次测量的记录复制4000份，不会产生4000次独立实验。本章每一行都重新生成读数，因此行与行对应重新开展的测量过程；这种数组结构延续了上一章“先说明每条轴代表什么”的习惯。

## 随机变量描述可能的读数，分布描述它们出现的规律

随机变量并不是一个永远无法说明的数字，而是把一次尚未观察到的结果写成数值的规则。例如，下次测厚仪的读数可以记作X；测量完成后，X才落实为某个具体数。为了模拟读数，我们还需要一个分布，描述哪些结果较常见、哪些较少见。本章选用正态分布作为明确的教学模型：中心附近读数较多，偏离中心越远，通常越少。正态只是本例选择的形状，不能因为数据来自测量，就默认所有误差都具有这种分布。

先生成中心为0、标准差为1的标准正态数Z，再乘0.04 mm并加1.20 mm，就得到有物理单位的读数。乘法设置波动尺度，加法设置中心。例如某次Z恰好为−0.5，读数就是1.20−0.5×0.04=1.18 mm；Z为1.5时，读数为1.26 mm。Z没有长度单位，标准差带有mm，因此乘积与最后的读数都有长度单位。这种拆法把随机形状和测量尺度分开，改变仪器波动大小时，计算含义仍然清楚。

$$
X=\mu+\sigma Z,\qquad Z\sim\mathcal{N}(0,1)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46833dd7644e5c60bb4525fe.svg) | 一次厚度读数，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 设定分布中心，本例1.20 mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 独立读数波动的标准差，本例0.04 mm |
| ![Formula](https://ml-biomat.com/static/agent-math/2ff8585a9cda3f4625f17d79.svg) | 标准正态随机数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/be802d478d02bfa3ac2b08b1.svg) | 服从均值0、方差1的正态分布，两个参数无量纲 |

标准随机数乘以长度尺度再加中心，就得到有单位的读数。Z=−0.5时，X=1.20+0.04×(−0.5)=1.18 mm。

标准差描述分布的宽窄，和最大允许误差不是同一概念。这里0.04 mm说明一条读数分布的波动尺度，并不表示读数必然位于1.16到1.24 mm之间。对本例理想正态模型，这个区间约占68%的概率；更远的读数仍可能出现。标准差平方叫方差，单位变成mm²。后面推导平均值的波动时，方差便于相加；最后再开平方，结果回到容易解释的mm。

直方图把厚度轴切成许多小区间，再统计每个区间落入多少读数。若纵轴是计数，柱子相加等于总读数；若纵轴是概率密度，柱子的面积相加等于1。本章采用概率密度，以便让不同组的分布和理论曲线在同一坐标上比较。横轴单位为mm，纵轴便是mm⁻¹，两者相乘得到无量纲概率。密度超过1完全可能，例如读数集中在很窄的厚度范围里；只有面积才表示概率，而不是某个点的曲线高度。

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 可能的厚度值，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/93f888a1ee0b7da5e29f442f.svg) | 概率密度，mm⁻¹；区间下的面积表示概率 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 正态分布中心，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 正态分布标准差，mm，公式要求大于0 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约3.14159，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/38c5da563ad696bdc123bf67.svg) | 以自然常数e为底的指数函数；u是括号内无量纲表达式 |

取μ=1.20 mm、σ=0.04 mm。中心x=1.20 mm处指数为0，密度为1/(0.04√(2π))≈9.974 mm⁻¹。高度超过1并不矛盾，概率由密度乘厚度区间后累积得到；σ=0时分布集中于一个点，不使用此密度公式。

公式中的指数项先用标准差把偏离中心的长度变成无量纲数，再将远离中心的数值压低。前面的系数调整整体高度，使全部曲线下面积等于1。标准差越小，曲线越窄，也就必须越高，才能保留相同总面积。图中随着平均次数增加而升高的峰，正是在呈现这种变化。直方图区间的宽度也会改变柱子外观；比较分布时应采用共同分箱或明确标注，避免把不同画法造成的差异误认为测量机制改变。

例如，200个均值中有40个位于宽0.01 mm的区间内，这个区间的经验概率为40/200=0.20；采用密度纵轴时，柱高为0.20/0.01=20 mm⁻¹。柱子虽然高达20，面积仍是0.20。再把区间宽度减半，读数会重新分配到较细的柱子中，单根柱子的高度可能变化，但完整直方图的总面积仍为1。这个手算把计数、比例和密度三个常见纵轴连在一起。

## 让随机计算能够重复，也能够改变

`rng = np.random.default_rng(2026)`创建一个随机数生成器对象。它内部维护自己的状态，每次抽样后推进到下一状态。种子2026用于确定初始状态；它只是一个约定的整数，不表示年份具有任何统计作用。随后`rng.normal(0, 1, size=(4000,64))`生成一张4000行64列的标准正态数组。前两个参数分别控制中心与标准差，`size`控制输出形状。把生成器传给需要随机数的函数，能够让随机性的来源保持明确。

计算机生成的这些数叫伪随机数：它们由确定的算法产生，却被设计成具有适合抽样的统计性质。重复相同的初始化与调用流程，可以重新得到同一轮模拟，便于检查修改的影响。种子固定并不意味着分布假设正确，也不意味着有限样本刚好具有理论均值。它解决的是重复执行的起点；模型是否符合研究问题，还要用测量定义、解析关系和实际数据判断。

重新创建相同种子的生成器会重新开始相同序列。如果在每次实验循环里都创建`default_rng(2026)`，每一行可能得到相同读数，造成重复了很多次实验的假象。正确做法是创建一次生成器，再连续取得需要的数组，或者有明确设计地建立多条随机序列。本例采用前一种方式。另一个容易忽略的细节是调用顺序：在前面多抽一次随机数，后面的状态就可能改变，因此记录种子时，还要保留代码与抽样形状。

程序同时记录NumPy版本、实际位生成器名称、种子以及数组大小。它还保存本次生成的标准随机数，使之后能够针对完全相同的抽样结果比较参数。版本和算法可能演进，所以长期复现需要这些信息共同描述运行条件，而不是只传递一个种子整数。浏览器实验直接使用完整程序生成并保存的两组标准随机数，切换种子时选择另一组，改变波动或偏差参数时则保持同一组抽样，这样更容易看出参数本身的作用。

## 蒙特卡洛把许多可能的实验变成可计算的对象

蒙特卡洛方法的核心，是按给定概率规则模拟许多可能过程，再汇总它们的结果。Metropolis在1987年的亲历回顾中描述了统计抽样与早期电子计算机结合的过程；他与Ulam在1949年发表的《The Monte Carlo Method》，使这种计算思路成为明确的方法文献。电子计算机让大量重复路径或实验的计算变得可行，研究者能够用样本集合研究直接求解困难的问题。本章沿用的正是“重复完整过程，再研究结果分布”的思路。

![原创蒙特卡洛过程图：前八次实验的十六个读数与对应均值，下方汇总4000个均值。所有数值由给定正态模型生成。](https://ml-biomat.com/static/tutorials/python-scientific/figures/6d0be7a19fecd5ed0d68b81a.svg?v=6d0be7a19fec)

图 1原创蒙特卡洛过程图：前八次实验的十六个读数与对应均值，下方汇总4000个均值。所有数值由给定正态模型生成。

图上方把前八次模拟实验展开：每一行有十六个读数，颜色表示它们偏离设定真值多少微米，右边再画出这一行的平均偏离。1 mm等于1000 μm，所以0.04 mm的波动尺度在这里对应40 μm。把同一行的正负偏离相加再除以十六，常能获得较小的平均偏离。下方则收集全部4000行的平均值，形成另一条分布。它描述的是“若完整重做十六次读数的实验，平均值会怎样变化”。

这一步并没有把同一批数偷偷当成更多独立试样。模型设定的是同一真实厚度下反复开展测量，行内的读数波动首先按独立条件生成，行之间也是重新抽样。若想研究不同薄片之间的制造差异，需要另外加入每块薄片的真实厚度变化，并说明哪条轴代表薄片。把随机数组生成得更大，不能替代对实验单位的定义；数组大小只有放回生成过程，才有明确的统计含义。

使用共同随机数比较参数，是一个很实用的观察办法。把全部读数同时加0.03 mm，我们知道每次平均值都应增加0.03 mm；继续使用原来的随机波动，就能逐个配对验证这个变化。若每次调整参数都重新抽样，看到的差异还会夹杂新一轮随机起伏。本章先保持抽样固定来观察机制，再通过另一种子检查现象是否仍然存在。两种操作分别帮助比较参数作用与抽样变化。

## 平均值为什么更稳定，又为什么不会每次都更准

平均值先把一次实验中的n个读数相加，再除以n。对同一中心、相同方差且相互独立的读数，和的方差等于各项方差之和；除以n后，方差还要除以n²，因此平均值方差是单次方差的1/n。开平方得到平均值的标准差，也常称标准误：单次标准差除以√n。这个推导说明平方根从哪里来，也说明独立性为什么重要。若读数一起向上或向下偏，它们之间的联系会改变方差相加的结果。

$$
\bar X_r=\frac{1}{n}\sum_{j=1}^{n}X_{rj},\qquad \operatorname{SD}(\bar X)=\frac{\sigma}{\sqrt n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a934d6a2da636a96d533bf97.svg) | 第r次完整实验的第j个厚度读数，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/945c1a122d82e7eb08609a35.svg) | 第r次实验的平均厚度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/c9b8c7a8cde7033169f76cde.svg) | 实验与读数编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 每次实验的读数数量，正整数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/67b782d816a5bbd0406cf935.svg) | 把同一次实验中的n个读数相加 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 独立、同分布读数的有限标准差，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f0c1878f989135224d5a4c.svg) | 完整重复实验之间，平均厚度的标准差，mm |

独立读数相加的方差为nσ²，平均后除以n²，因此均值方差为σ²/n；开平方得到标准误。σ=0.04 mm、n=16时，0.04/4=0.01 mm。

本例单次标准差0.04 mm。四次读数的平均值标准差为0.02 mm，十六次为0.01 mm，六十四次为0.005 mm。想让这个波动尺度减半，需要把独立读数数量增加到原来的四倍，而不是两倍。图右的对数坐标让相同倍数变化占相同距离，便于比较这条规律；坐标标签仍然写实际读数数量与mm。左侧则把四种均值分布放在相同厚度范围内，让尺度变化直接表现为曲线宽窄。

![阶梯线为模拟均值的密度直方图，平滑线为解析正态密度；右侧点给出实际4000次模拟的标准差。](https://ml-biomat.com/static/tutorials/python-scientific/figures/2300b0f61074dc8acdf6402b.svg?v=2300b0f61074)

图 2阶梯线为模拟均值的密度直方图，平滑线为解析正态密度；右侧点给出实际4000次模拟的标准差。

程序实际得到的四个均值标准差依次约为0.040070、0.020117、0.010034、0.004980 mm，与解析值接近，却不必完全相等。4000个模拟均值本身也是有限样本，估计出的分布宽度仍有波动。增加模拟实验次数，能够使我们更稳定地估计这条分布；增加每次实验的读数数量，则改变所研究的均值分布本身。这是两种不同的“多做一些”，看清它们可以避免把计算量增加误认为测量精度自动改善。

在本例正态且独立的模型下，平均值本身也具有正态分布，不需要等到很大的n才近似成立。更一般的独立、同分布且方差有限的读数，在满足相应条件时，均值分布随着n增加会接近正态，这与中心极限定理有关。不过，标准误按平方根下降的关系与“原始数据必须正态”并不是同一条件。这里把正态模型、独立性和有限方差分别说清，后续面对偏斜数据或相关读数时，才能知道该调整哪一部分。

标准误变小是一种对重复实验分布的判断，并不保证每增加一次读数，眼前这一条累计平均就必然更接近真值。新读数可能把当前平均拉近，也可能暂时拉远。类似于多人掷硬币时正反面比例总体趋于平衡，单次增加的结果仍会有方向上的波动。可靠的表述是平均值可能出现的范围逐渐收窄；观察某一次恰好靠近中心的结果，不能代替对整个分布的检查。

读数的标准差与平均值的标准误，回答的是不同问题：前者描述单个读数彼此有多分散，后者描述完整实验重新开展时，平均结果会怎样变化。若把标准误画成单个读数的分散范围，就会让观测看起来比实际更集中。因此，画误差条之前要说明重复的单位究竟是读数、一次会话的均值，还是独立试样。即使它们最后都用mm表示，也不能只因单位相同就互相替代。

## 固定偏差与共有偏移，为什么留在平均值里

先给每个读数都加固定的0.03 mm。无论平均多少次，这一项都会原样加到平均值上：十六次的均值分布从1.20附近移动到1.23附近，宽度仍然约为0.01 mm。多次结果彼此很接近，说明重复性好；分布中心与设定真值的距离，则反映这里加入的固定偏差。这个例子将“变化小”和“中心对”画成两个可以分别观察的属性，避免只凭一组很整齐的读数就判断校准已经准确。

再考虑另一种情形：每次开始测量时，装夹或仪器零点给这一整组读数带来同一个偏移，但重新开展实验时这个偏移会改变。用标准差0.03 mm的随机量描述这种会话共有部分，同次实验里的十六个读数便一起平移。它们仍各自有0.04 mm的独立波动，可共有偏移不会因为同次多读几遍就互相抵消。这里“会话”指一次共同装夹或共同零点条件下的一组测量。

$$
X_{rj}=\mu+b+\sigma Z_{rj}+\tau U_r,\qquad \operatorname{SD}(\bar X)=\sqrt{\frac{\sigma^2}{n}+\tau^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a934d6a2da636a96d533bf97.svg) | 第r个会话的第j个读数，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 设定真实厚度，1.20 mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 所有读数共有的固定偏差，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 独立读数波动的标准差，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/9eaf25a888dbfdc9822c18d9.svg) | 每个读数独立的标准正态变量，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 会话间共有偏移的标准差，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/efc46a95815086e114611e76.svg) | 第r个会话共有的标准正态变量，无量纲；与全部Z独立，不同会话也独立 |
| ![Formula](https://ml-biomat.com/static/agent-math/fafca02cde4303b92d177576.svg) | 会话编号、读数编号和每会话读数数量，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f0c1878f989135224d5a4c.svg) | 重新开展会话时平均值的标准差，mm |

同一会话的共有项平均后仍保留τU_r；固定偏差b只改变中心，不改变标准差。σ=0.04 mm、τ=0.03 mm、n=16时，√(0.0016/16+0.0009)=0.0316228 mm。

十六次读数时，独立部分给均值贡献0.01 mm的标准差，共有部分贡献0.03 mm。因为两部分在模型中独立，应当先把方差相加，再开平方，得到约0.031623 mm，而不是把0.01与0.03直接相加成0.04 mm。程序从4000次模拟得到约0.031028 mm，差异来自有限抽样。图右继续增加同一会话的读数数量，独立部分逐渐减小，共有部分却保持着0.03 mm的尺度。

![固定偏差平移均值分布；会话共有偏移增加分布宽度，并保留在同一会话反复读数的平均值中。](https://ml-biomat.com/static/tutorials/python-scientific/figures/a5707aa644094a3638935e39.svg?v=a5707aa64409)

图 3固定偏差平移均值分布；会话共有偏移增加分布宽度，并保留在同一会话反复读数的平均值中。

这给实验设计一个具体提示：若主要波动来自共同装夹，增加同一装夹下的读数，与重新装夹后再测量，提供的信息不同。独立重复多个会话，可以帮助估计会话间的变化；校准记录帮助识别固定偏差；单次会话内重复读数则帮助观察短时间读数波动。它们并非互相替代。分析时保留会话编号、试样编号与读数编号，后面才能把这些不同层次的数据分别汇总。

本章模型把独立波动与共有偏移都设为正态，而且共有项对同一会话里的每个读数影响相同。实际过程还可能出现随时间增长的漂移、相邻读数的逐渐衰减关联，或个别异常值。面对这些现象，应根据残差随时间的图、校准实验与测量步骤选择对应模型。这里先把一项完全共有的偏移讲清，是为了看见独立假设失效时平均值会发生什么，而不是把所有相关过程都归成相同的一种。

## 完整模拟与实际输出

完整程序把标准随机数与物理参数分开保存。首先用固定种子生成4000×64的独立标准正态数组，再生成4000×1的会话标准正态数组。后者只有一列，正好沿每次实验的读数方向广播。不同n使用同一行最前面的n个读数，因此四种设计之间是配对比较；每一种设计内部仍包含4000次重新生成的实验。程序用普通Python求和与平方偏差独立核对NumPy的均值和标准差计算。

### 完整程序：读数、均值分布与误差机制

保存实际生成数组、两组交互抽样、数值摘要和三幅图。

```
"""Simulate repeated thickness readings and distinguish noise, bias, and shared offsets."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

MU=1.2
SIGMA=.04
TRIALS=4000
MAX_READINGS=64

def draws(seed):
    rng=np.random.default_rng(seed)
    individual=rng.normal(0,1,size=(TRIALS,MAX_READINGS))
    common=rng.normal(0,1,size=(TRIALS,1))
    return individual,common,type(rng.bit_generator).__name__

def scalar_sd(values):
    average=math.fsum(float(v) for v in values)/len(values)
    return math.sqrt(math.fsum((float(v)-average)**2 for v in values)/(len(values)-1))

def density(x,center,sd):
    return np.exp(-.5*((x-center)/sd)**2)/(sd*np.sqrt(2*np.pi))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    z,c,bitgen=draws(2026);readings=MU+SIGMA*z
    sizes=[1,4,16,64];means={n:readings[:,:n].mean(axis=1) for n in sizes}
    empirical={n:float(means[n].std(ddof=1)) for n in sizes};theory={n:SIGMA/math.sqrt(n) for n in sizes}
    shared_means=(MU+SIGMA*z[:,:16]+.03*c).mean(axis=1)
    biased_means=means[16]+.03
    assert np.allclose(means[16],[math.fsum(float(x) for x in row)/16 for row in readings[:,:16]])
    for n in sizes:assert math.isclose(empirical[n],scalar_sd(means[n]),rel_tol=1e-12)
    assert math.isclose(float(biased_means.std(ddof=1)),empirical[16],rel_tol=1e-12)
    assert math.isclose(float(biased_means.mean()-means[16].mean()),.03,abs_tol=1e-12)
    zh=args.language=='zh';tr=lambda a,b:a if zh else b;colors=['#28648a','#467a62','#b85336','#7b5c90']
    fonts={f.name for f in font_manager.fontManager.ttflist};family=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,n):
        fig.savefig(args.output/f'{n}-{args.language}.svg',bbox_inches='tight');fig.savefig(args.output/f'{n}-{args.language}.png',dpi=170,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12.5,7.8),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[3,1],height_ratios=[1,.85]);ax=fig.add_subplot(gs[0,0]);dev=1000*(readings[:8,:16]-MU);im=ax.imshow(dev,cmap='RdBu_r',vmin=-100,vmax=100,aspect='auto');ax.set(xticks=np.arange(0,16,3),xticklabels=np.arange(1,17,3),yticks=range(8),yticklabels=np.arange(1,9),xlabel=tr('同一次实验里的读数编号','Reading number within an experiment'),ylabel=tr('重新开展的实验编号','Repeated experiment'),title=tr('a  蒙特卡洛：按同一规则生成许多完整实验','a  Monte Carlo: generate complete repeated experiments'));fig.colorbar(im,ax=ax,pad=.02).set_label(tr('读数减去真值 / μm','Reading minus truth / μm'))
    im.set_clim(-20*math.ceil(float(np.abs(dev).max())/20),20*math.ceil(float(np.abs(dev).max())/20))
    ax=fig.add_subplot(gs[0,1]);ax.barh(np.arange(8),1000*(means[16][:8]-MU),color=colors[0]);ax.set_ylim(7.5,-.5);ax.axvline(0,color='#607078',lw=1);ax.set(yticks=np.arange(8),yticklabels=np.arange(1,9),xlabel=tr('均值偏离 / μm','Mean offset / μm'),title=tr('b  每行得到一个均值','b  One mean per row'))
    ax=fig.add_subplot(gs[1,:]);ax.hist(means[16],bins=np.arange(1.15,1.251,.004),density=True,color=colors[0],alpha=.4,edgecolor='#fbfaf6');xx=np.linspace(1.15,1.25,500);ax.plot(xx,density(xx,MU,.01),color=colors[0],lw=2.2,label=tr('模型：均值标准差0.01 mm','Model: mean SD 0.01 mm'));ax.axvline(MU,color='#172b36',ls='--',label=tr('设定真值1.20 mm','Specified truth 1.20 mm'));ax.set(xlabel=tr('每次16个读数的平均厚度 / mm','Mean thickness of 16 readings / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),title=tr('c  4000个模拟均值形成分布；上图只展示前8次','c  Distribution of 4000 simulated means; above shows the first 8'));ax.legend(fontsize=11);ax.grid(alpha=.1)
    save(fig,'monte-carlo-history')

    fig=plt.figure(figsize=(12.5,6.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.4,1]);ax=fig.add_subplot(gs[0]);bins=np.arange(.99,1.411,.005);xx=np.linspace(1,1.4,700)
    for n,col in zip(sizes,colors):ax.hist(means[n],bins=bins,density=True,histtype='step',lw=1.5,color=col,alpha=.6);ax.plot(xx,density(xx,MU,theory[n]),color=col,lw=2,label=f'n = {n}')
    ax.set(xlabel=tr('一次实验的平均厚度 / mm','Mean thickness in one experiment / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),xlim=(1.04,1.36),title=tr('a  读数越多，均值分布越窄','a  More readings narrow the mean distribution'));ax.legend();ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[1]);nn=np.arange(1,65);ax.plot(nn,SIGMA/np.sqrt(nn),color=colors[0],lw=2,label=tr('解析关系 σ/√n','Analytical σ/√n'));ax.scatter(sizes,[empirical[n] for n in sizes],s=65,color=colors[2],zorder=3,label=tr('4000次模拟的标准差','SD across 4000 simulations'));ax.set_xscale('log',base=2);ax.set_yscale('log',base=2);ax.set_xticks([1,4,16,64],[1,4,16,64]);ax.set_yticks([.005,.01,.02,.04],['0.005','0.010','0.020','0.040']);ax.set(xlabel=tr('每次实验的读数数目 n','Readings per experiment n'),ylabel=tr('均值标准差 / mm','Standard deviation of the mean / mm'),title=tr('b  四倍读数，使标准差减半','b  Four times as many halves the SD'));ax.legend(loc='lower left',fontsize=10);ax.grid(alpha=.15)
    save(fig,'averaging-distributions')

    fig=plt.figure(figsize=(12.5,7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.35,1]);ax=fig.add_subplot(gs[0]);xx=np.linspace(1.05,1.4,600)
    scenarios=[(means[16],MU,.01,colors[0],tr('独立噪声','Independent noise')),(biased_means,MU+.03,.01,colors[2],tr('再加固定偏差0.03 mm','Add fixed bias 0.03 mm')),(shared_means,MU,math.sqrt(.001),colors[1],tr('会话偏移标准差0.03 mm','Session offset SD 0.03 mm'))]
    for values,center,sd,col,label in scenarios:ax.hist(values,bins=np.arange(1.04,1.411,.005),density=True,histtype='step',color=col,alpha=.5);ax.plot(xx,density(xx,center,sd),color=col,lw=2,label=label)
    ax.axvline(MU,color='#172b36',ls='--',lw=1.5);ax.set(xlabel=tr('16个读数的平均厚度 / mm','Mean thickness of 16 readings / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),xlim=(1.08,1.35),title=tr('a  分布变窄，与中心正确是两件事','a  A narrow distribution can have a shifted center'));ax.legend(fontsize=10);ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[1]);nn=np.arange(1,257);ax.plot(nn,SIGMA/np.sqrt(nn),color=colors[0],lw=2,label=tr('只有独立噪声','Independent noise only'));ax.plot(nn,np.sqrt(SIGMA**2/nn+.03**2),color=colors[1],lw=2,label=tr('加会话共有偏移','With shared session offset'));ax.axhline(.03,color=colors[1],ls=':',label=tr('共有部分：0.03 mm','Shared component: 0.03 mm'));ax.set_xscale('log',base=2);ax.set_xticks([1,4,16,64,256],[1,4,16,64,256]);ax.set(xlabel=tr('同一会话的读数数目 n','Readings within one session n'),ylabel=tr('均值标准差 / mm','Standard deviation of the mean / mm'),ylim=(0,.055),title=tr('b  重复读数无法消除共有偏移','b  Repeated readings retain a shared offset'));ax.legend(fontsize=10);ax.grid(alpha=.12);save(fig,'bias-and-shared-offset')
    lab={}
    for seed in [2026,2027]:
        zi,ci,_=draws(seed);lab[str(seed)]={'individual':zi[:200].tolist(),'common':ci[:200,0].tolist()}
    (args.output/'lab-draws.json').write_text(json.dumps(lab,separators=(',',':')),encoding='utf8')
    np.savez_compressed(args.output/'simulation.npz',individual_standard=z,session_standard=c,readings_mm=readings)
    summary={'model':{'true_thickness_mm':MU,'individual_sd_mm':SIGMA,'trials':TRIALS,'maximum_readings':MAX_READINGS,'seed':2026,'bit_generator':bitgen,'numpy_version':np.__version__},'mean_sd':{str(n):{'empirical_mm':empirical[n],'analytic_mm':theory[n],'mean_mm':float(means[n].mean())} for n in sizes},'n16_scenarios':{'unbiased':{'mean_mm':float(means[16].mean()),'sd_mm':empirical[16]},'fixed_bias':{'mean_mm':float(biased_means.mean()),'sd_mm':float(biased_means.std(ddof=1))},'shared_offset':{'mean_mm':float(shared_means.mean()),'sd_mm':float(shared_means.std(ddof=1)),'analytic_sd_mm':math.sqrt(.001)}},'first_trial_n16_mean_mm':float(means[16][0]),'first_trial_readings_mm':readings[0,:16].tolist()}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary['mean_sd'],indent=2));print(json.dumps(summary['n16_scenarios'],indent=2))

if __name__=='__main__':main()
```

数值摘要记录模型参数、版本、位生成器、四种均值标准差和三种误差情形。默认十六次读数的4000个均值平均约为1.200244 mm；加入固定偏差后为1.230244 mm，两者的分布标准差相同，约0.010034 mm。共有偏移情形的整体平均约为1.200503 mm，分布宽度却明显增加。这些具体输出把分布中心与分布宽度分开呈现，读者可以从保存的数组重新计算，而不只依赖图中的外观。

`simulation.npz`保存标准随机数组和完整读数，`summary.json`保存便于阅读的数值摘要；三幅图分别解释重复实验、平均次数与误差机制。文件保存的随机数属于这一轮模拟，实现了“同一组抽样，再比较计算”的用法。代码中的`ddof=1`用于计算4000个模拟均值的样本标准差；它描述这组均值的分散程度，与模型参数中直接给定的单次读数标准差0.04 mm需要区分。

这里沿第1轴求均值，是因为第1轴存放一次实验中的读数。`readings[:,:16].mean(axis=1)`把每行十六个数合成一个，输出长度4000，恰好对应4000次完整实验。若改成axis=0，就得到十六个结果，每个表示所有模拟实验在相同读数位置上的平均。那是另一个问题，也不会得到本章需要的均值分布。计算标准差时，我们再沿4000个均值组成的一维数组汇总，两个阶段的统计对象因此清楚分开。

## 把重复次数、随机波动与共同偏移分开调整

实验使用程序生成的200次模拟实验，每次最多64个标准读数。选择一次实验，可以在散点图里看到这组读数与它们的平均值；右侧直方图同时展示全部200个均值。改变每次读数数量，观察理论标准误和实际分布宽度怎样变化；再加入固定偏差，查看中心平移；最后增加共有偏移的标准差，观察均值分布为什么仍然宽。所有参数都有单位，曲线和表格从同一组数重新计算。

### 实验：哪些波动能被平均？

200次完整模拟实验。保留同一组标准随机数，改变参数观察因果关系；换种子可观察另一组抽样。

[Figure: 一次实验的读数和均值](https://ml-biomat.com/tutorials/python-scientific/p09/#P09-readings)

[Figure: 200个均值与解析分布](https://ml-biomat.com/tutorials/python-scientific/p09/#P09-distribution)

可以先把独立波动标准差设为0.04 mm、其余偏差设为零，从4次切换到16次，核对理论标准误由0.02降到0.01 mm。然后保留16次并加入0.03 mm的固定偏差，验证每个均值都平移而宽度不变。最后把固定偏差恢复为零，加入0.03 mm的会话偏移，比较增加到64次以后仍保留的波动。三个操作对应不同的实验改进方向：增加独立读数、校准中心，以及控制或独立重复共有条件。

浏览器为了便于逐次查看，保留的是前200次模拟；正文图使用全部4000次。因此，界面显示的经验标准差与正文中的数值可能略有差别，解析标准误则只由参数与读数数量决定。可以用两个种子分别观察这个差别，再核对解析值是否保持不变。增加模拟次数主要改善分布估计的稳定程度，而换种子展示了这种估计本来就存在的随机变化。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P09.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NumPy — Random Generator](https://numpy.org/doc/2.4/reference/random/generator.html)

   生成器、种子与输出形状

   BSD-3-Clause
2. [NumPy — Generator.normal](https://numpy.org/doc/2.4/reference/random/generated/numpy.random.Generator.normal.html)

   正态抽样参数与实现入口

   BSD-3-Clause
3. [NumPy — Random compatibility policy](https://numpy.org/doc/2.4/reference/random/compatibility.html)

   版本、调用顺序与抽样流复现条件

   BSD-3-Clause
4. [NIST/SEMATECH — Normal Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm)

   密度、中心与标准差的统计定义

   US government handbook; factual reference
5. [N. Metropolis — The Beginning of the Monte Carlo Method (1987)](https://mcnp-green.lanl.gov/pdf_files/Article_1987_LAS_Metropolis_125--130.pdf)

   统计抽样与早期电子计算的亲历回顾

   Public LANL archival article; factual paraphrase and original figures
