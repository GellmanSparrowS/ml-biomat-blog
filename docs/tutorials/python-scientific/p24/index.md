# 让数学推导连接数值计算

Source: https://ml-biomat.com/tutorials/python-scientific/p24/
Language: zh-CN

从弹性储能出发，用SymPy推导力与刚度，再看精确公式怎样解释数值误差。

## 从拉长一根弹性元件开始

拉开夹子、压缩弹簧或拉伸一小段柔性连接件时，手会感觉到阻力逐渐变化。如果已经写出了元件储存能量的公式，能否直接算出需要施加多大的力，以及再拉长一点会增加多少阻力？这三个问题分别对应储能、力和刚度。它们常常出现在材料模型和实验分析中，也很适合用来学习符号计算：保留字母推导关系，再把参数和位移交给数值程序，便能得到相互对应的曲线。

本节用一个有意简化的弹性储能模型贯穿整个过程。位移从零开始，元件缓慢加载，外力做的功储存在元件里；卸载时沿同一关系返回。这样的模型适合描述可逆弹性响应。若实验出现明显滞回、速度依赖或永久变形，就需要增加描述耗散或内部状态的变量。先把这一模型讲清楚，可以具体看见物理假设怎样决定公式的用途。

SymPy负责保存和变换数学表达式，NumPy负责成批计算位移点，Matplotlib把三种物理量画出来。最后还会用一个看起来很合理的数值办法估计力：取附近两个能量值相减，再除以位移间隔。把这个估计与符号导数比较，便能解释为什么步长缩得太小，计算结果反而会变差。

## 先把能量、位移和单位放在一起

把能量想成逐步存进元件的一笔机械功。位移越大，通常存入越多；但每增加同样的一小段位移，付出的功可以不同。我们用二次项描述最简单的弹性储能，再加一个四次项，让大位移时的阻力上升得更快。两个系数分别控制这两部分的大小。它们是教学模型的输入参数，图中的点由公式计算得到。

$$
U(x)=\frac{kx^2}{2}+\frac{\alpha x^4}{4},\qquad k>0,\quad \alpha\geq0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9469b6261e047457191334c2.svg) | 位移为x时储存的弹性能，mJ；U(0)=0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 相对未变形位置的位移，mm；正负表示方向。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 二次储能项系数，也是原点的切线刚度，N/mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 四次储能项系数，N/mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96d66c13fb959b10fd625f8f.svg) | 分母中的无量纲常数；上标2和4分别表示平方与四次方。 |

取k=2 N/mm、α=0.5 N/mm³、x=1 mm，U=2×1²/2+0.5×1⁴/4=1.125 N·mm=1.125 mJ。两个加法项都有能量单位。α为零时保留二次储能模型；α为正时加入随大位移更快增长的项。

指数只说明位移出现了几次，单位也必须跟着相乘。二次项里的位移平方带有平方毫米，乘上牛顿每毫米，就得到牛顿毫米。四次项的系数则需要牛顿每立方毫米，才能得到相同的能量单位。只有同类量才能相加，因此这一步也能发现漏写指数或系数单位的问题。本节始终以毫米输入位移，最终能量用毫焦表示，因为一牛顿毫米就是一毫焦。

取刚度系数2 N/mm、四次项系数0.5 N/mm³，位移为1 mm时，二次项贡献1 mJ，四次项贡献0.125 mJ，总共1.125 mJ。位移变为2 mm后，两部分分别是4 mJ和2 mJ，总共6 mJ。位移加倍时，二次项扩大到原来的四倍，四次项扩大到十六倍；较高次项为什么在大位移时显得更突出，在这两个数字中已经能看出来。

模型把零位移的能量设为零，方便直接计算加载过程存入的功。若给整个能量函数加同一个常数，任意两点间的能量差保持不变，维持位移所需的力也保持不变。这是选择能量参考点的自由。改变位移单位则是另一回事：把毫米改成米时，两个系数必须同步换算，不能只修改横轴文字。

还可以在代入数字前检查模型的对称性。由于两项都是位移的偶次方，向相反方向移动相同距离会储存相同能量。于是正负方向的力大小相同、方向相反，而两侧的切线刚度相同。这是当前公式包含的一条具体物理假设；若元件拉伸和压缩表现不同，就要调整模型结构，再重新计算这些量。

## 曲线的斜率为什么就是力

先从很短的一段加载过程理解导数。若这一小段里的外力近似不变，做功就是力乘位移增量；反过来，用能量增加量除以位移增加量，就得到这段过程的平均力。在储能曲线上，这个比值是连接两个点的割线斜率。让两点逐渐靠近，平均力趋向该位置的力，割线趋向切线，导数就是这个局部变化率。

$$
F(x)=\frac{\mathrm dU}{\mathrm dx}=kx+\alpha x^3,\qquad K(x)=\frac{\mathrm dF}{\mathrm dx}=k+3\alpha x^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f42ff2aa801298d0b0e10a.svg) | 缓慢加载时维持位移的外力，N；元件恢复力为−F。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c18cc14db4443d05e8ca8d27.svg) | 当前位置的切线刚度，N/mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d2936881a9db32d00d3ef560.svg) | U为储能，mJ；x为位移，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c716d1023aa9003462dc1854.svg) | k为二次项系数，N/mm；α为四次项系数，N/mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d7307287aa169cbb98be8758.svg) | 对位移求导，表示每单位微小位移所引起的变化。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6cb44f25e489afb06ec62d2e.svg) | 对x³求导得到3x²时出现的无量纲系数。 |

幂函数求导时，指数移到前面，再把指数减1：x²变为2x，x⁴变为4x³，因此能量里的分母恰好消去。用k=2、α=0.5、x=1并保持前述单位，F=2+0.5=2.5 N，K=2+3×0.5=3.5 N/mm。导数连接能量的局部斜率与力，再连接力的局部斜率与刚度。

这里的正力是为维持正位移而施加的外力。元件自身的恢复力方向相反，会把它拉回能量较低的位置，大小相同而符号为负。把作用对象说清楚，可以避免同一个导数在不同教材中看起来差了一个负号。继续求一次导数，得到外力对位移的变化率，即切线刚度；它回答的是从当前位置再移动一点会增加多少力。

在1 mm处，外力为2.5 N，切线刚度为3.5 N/mm。因此再增加0.01 mm位移时，力的增量大约是0.035 N。这个估计使用当前位置的斜率，适合很小的增量；完整模型给出的增量为0.0351505 N，两者相差约0.0001505 N。若一步拉得较远，沿途刚度也会改变，就应计算两个位置的完整力值再相减。

![同一储能模型的能量、外力与切线刚度。三种颜色比较α=0、0.5、2 N/mm³，均取k=2 N/mm。蓝点追踪x=1 mm的三个对应值；所有曲线为模型计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/59ab7615066e276e09fe0f5d.svg?v=59ab7615066e)

图 1同一储能模型的能量、外力与切线刚度。三种颜色比较α=0、0.5、2 N/mm³，均取k=2 N/mm。蓝点追踪x=1 mm的三个对应值；所有曲线为模型计算。

三幅图用同一组参数展示能量、外力和刚度。灰线对应四次项为零，外力随位移线性增加，刚度是一条水平线；蓝线和橙线保留四次项，刚度随位移上升。能量曲线越弯，并不等于纵轴上的能量值本身就是力。先看纵轴单位，再看求导连接的是哪两个量，三幅图便能互相解释。

## 让字母保留含义，让分数保留精确值

写下`x = sp.Symbol('x', real=True)`，得到的是代表实数的符号对象。此时还没有选定某个位移。系数`k`设为正，`alpha`设为非负，正好对应本节的弹性模型；零值也属于非负，因此能够自然比较有无四次项的情况。符号的取值条件参与化简，例如实数的平方再开平方得到绝对值。位移为−2 mm时，这个结果是2 mm，保留绝对值才符合开平方的含义。

程序用`sp.Rational(1, 2)`和`sp.Rational(1, 4)`建立精确分数。这两个分数在二进制浮点中恰好也能精确表示，但使用分数对象能让整条推导继续保留精确系数；换成三分之一时，这一点尤其明显。Python先计算普通整数之间的除法，再把结果放入表达式，而Rational直接保存分子和分母。推导完成后，才根据输出需要转换成小数。

`U.subs({k: 2, alpha: sp.Rational(1, 2)})`返回代入参数后的新表达式，原来的通式仍然保留。这个安排很像同时保存一张空白计算表和一张填好参数的计算表：前者还能用于比较其他元件，后者用于当前实例。若只代入两个系数，位移仍是自由符号；再代入位移，才会得到一个确定的能量值。查看`free_symbols`能帮助发现漏填的参数。

本节的符号对象保存代数关系，单位通过变量定义和一致的数值约定管理。把`x`命名成位移，并不会自动赋予它毫米单位。实际改写模型时，可以先列出输入量和输出量的单位，再检查每一个加法项和导数的单位。这样既能读懂程序，也能知道一个看似成功执行的计算究竟对应哪种物理量。

## 公式怎样成为计算机可以改写的对象

如果只把公式保存成一张图片，计算机能显示它，却难以直接对它求导。符号计算需要更具体的内部表示。2017年，Meurer等人在介绍SymPy的论文中解释了表达式树：加法、乘法和乘方是节点，符号与常数是末端，数学运算通过读取和重建这些结构完成。把这样的系统做成Python库，便能在同一个程序中连接代数推导与数组计算。论文及其作者公开的源码给出了这一设计的实际说明。

![原创建模图：从实际SymPy表达式递归读取13个节点，显示加法、乘法、乘方和精确分数如何组成能量。下方列出该表达式与其导数。2017年论文讨论了这种表达式树架构；图中模型为本节构造。](https://ml-biomat.com/static/tutorials/python-scientific/figures/41805bc6fe15c1f990fcf405.svg?v=41805bc6fe15)

图 2原创建模图：从实际SymPy表达式递归读取13个节点，显示加法、乘法、乘方和精确分数如何组成能量。下方列出该表达式与其导数。2017年论文讨论了这种表达式树架构；图中模型为本节构造。

图中最上面的Add表示把两项相加。沿着其中一条分支往下看，Mul把精确分数、系数和位移的幂相乘；Pow再把位移与指数连接起来。这张图由当前能量表达式的真实结构生成，因此可以逐层对应程序中的`func`和`args`。顶层的加法有两个孩子，乘方也有两个孩子；符号和分数已经不能再拆成这些代数操作，便成为叶子。

这种表示还解释了为什么“看起来相等”与“结构相同”是两个问题。例如同一个多项式可以写成乘积，也可以展开成各项之和，两个表达式树可能不同。Python的赋值号用于给对象起名字，`sp.Eq`用于建立方程，`==`比较SymPy表达式的结构。检查本节两个多项式是否恒等时，可以展开或化简它们的差，观察结果是否为零；代入几个数值则适合寻找错误线索。

回到储能模型，程序从同一个U求出F和K，再把F积分回来。这让三个量始终共享同一组系数和幂次。改变能量模型时，相关导数随之重新生成；比起在多个函数里分别手写相似公式，这种组织方式更容易维持数学上的一致性。沿着树图逐层读取，就能追踪每个导数项从哪里来。

## 从推导结果走到一整条数值曲线

保留字母适合推导，绘图则需要很多具体数值。程序用`lambdify((x, k, alpha), U, modules='numpy')`创建可调用的数值函数。括号里的顺序定义输入顺序，之后传入位移数组、刚度系数和四次项系数，就得到每个位移的能量。F和K也以同样方式转换。这里可以把lambdify理解为一次明确的接口转换：推导结果已经确定，接下来让NumPy对整组输入进行计算。

数组共有401个位移，从0到2 mm均匀排列；相邻点间隔0.005 mm。模型表同时保存位移、能量、外力和切线刚度，每一行对应同一个位置。这样的列关系比单独保存几条曲线更方便追踪：读到位移为1 mm的那一行，就能同时核对1.125 mJ、2.5 N和3.5 N/mm。绘图加密只让曲线显示得更细，物理参数仍是同一组。

同一个模型还能反过来回答问题：外力为3 N时，需要多大位移？程序把力表达式减去3，交给`nsolve`寻找零点，从1 mm开始迭代，得到约1.134728 mm。求解之后再把该位移代回力表达式，检查是否返回3 N。由于本节刚度始终为正，外力随位移严格增加，因而每一个给定外力只有一个实数平衡位移；这种唯一性来自模型的斜率性质。

$$
W_{0\to b}=\int_0^b F(s)\,\mathrm ds=U(b)-U(0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa1aa9ce37fea73c98f0d1b.svg) | 从位移0缓慢加载到b时外力做的功，mJ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 加载的终点位移，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 积分中的位移变量，mm；它沿加载路径从0变化到b。 |
| ![Formula](https://ml-biomat.com/static/agent-math/553badbaf2c0b915d0d4369a.svg) | 位移s处的外力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eafdac3dd6a477b3670861c5.svg) | 积分符号表示累计沿途微小位移段的功；ds带有mm单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fdd3a5a8d8d6ca2f49a8ba46.svg) | 终点与起点储能，mJ。 |

取b=2 mm、k=2 N/mm、α=0.5 N/mm³，积分得到k b²/2+α b⁴/4=4+2=6 mJ。起点储能为零，所以功等于终点储能。积分用s表示沿途位置，避免把可变化的积分变量与固定上限b混在一起。

积分把沿途每一小段的功累加起来。从0到2 mm，计算得到6 mJ，正好等于终点与起点的能量差。对于这根越拉越硬的元件，不能用终点力8 N乘整个2 mm位移来代替积分：那样相当于假定全程都施加8 N，会算出16 mJ。图像中应累计的是整条力曲线下面的面积，这也给符号积分的结果提供了具体的力学解释。

求根初值与模型参数也有不同角色。初值告诉数值算法从哪里开始寻找，改变它通常不应改变这里唯一的平衡解；改变刚度系数则改变元件本身，会移动平衡位置。若对更复杂的能量函数求根，可能出现多个平衡点，需要结合取值范围以及附近能量的升降判断对应的状态。先读懂力曲线，再解释求解器返回的位置，能够让数值结果与物理图像保持联系。

## 为什么差分步长不能一味缩小

假如手边只有一个可以返回能量值的函数，仍然可以取目标位置左右各一个点，用两点能量差除以它们的距离估计外力。这种中心差分对称地利用了两侧信息。半间距记作h，因此两点之间的完整距离是2h；少写这个2，会把估计力放大一倍。对本节的四次多项式，SymPy能把估计与真实导数的差完整展开，留下一个很简单的表达式。

$$
D_hU(x)=\frac{U(x+h)-U(x-h)}{2h},\qquad D_hU(x)-F(x)=\alpha xh^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/732aa542b12ff5c3ed36159d.svg) | 半间距为h的中心差分力估计，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a83c7a267ed0d7a6190ac2db.svg) | 中心位置两侧的储能，mJ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c42b0b36a7b3ec0bebfa150.svg) | x为中心位移，h为正的半间距，单位均为mm；两点距离为2h。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f42ff2aa801298d0b0e10a.svg) | 符号导数给出的外力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 四次储能项系数，N/mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f5f3224583db57b9cfe323c8.svg) | 分母中的2表示完整间距；上标2表示平方。 |

把(x+h)和(x−h)代入能量后展开，相减会消去所有关于h的偶次项；再除以2h，留下kx+αx³+αxh²。前两项就是F，剩下一项是精确算术中的截断误差。取α=0.5 N/mm³、x=1 mm、h=0.1 mm，该项为0.005 N，差分力为2.505 N。浮点计算还会叠加舍入误差。

在1 mm处取h为0.1 mm，精确差分给出2.505 N，比导数大0.005 N。把h减半到0.05 mm，误差变为0.00125 N，正好缩小到四分之一。这是公式中平方项带来的结果，常说的“二阶精度”在这里有了可手算的含义。四次项系数为零时，能量是二次函数，中心差分在精确算术下就能直接给出正确斜率。

![左图在x=1 mm处比较切线与半间距0.2 mm的割线；右图固定同一模型，扫描170个步长。橙线是精确算术误差αxh²，蓝线是实际NumPy计算的绝对误差。两图横轴含义不同，分别是位置与步长。](https://ml-biomat.com/static/tutorials/python-scientific/figures/fcd5a04c0bbc229aea72605e.svg?v=fcd5a04c0bbc)

图 3左图在x=1 mm处比较切线与半间距0.2 mm的割线；右图固定同一模型，扫描170个步长。橙线是精确算术误差αxh²，蓝线是实际NumPy计算的绝对误差。两图横轴含义不同，分别是位置与步长。

浮点计算还要处理另一件事：当两点非常接近，两个能量值也非常接近。相减后留下的数很小，原来数值中的舍入误差便可能占据较大比例；随后除以更小的间距，又会放大这种影响。误差图中，较大步长区域沿着理论平方规律下降，进一步缩小时出现起伏并最终上升。具体起伏与运算次序和浮点实现有关，读图时应关注两种误差竞争的形状。

符号导数在这个例子中提供了清楚的比较基准，差分则展示只调用能量函数时的计算路径。遇到复杂模型，可以先在可求导的小问题上理解误差，再把同样的比较思路用于实际函数。若能直接从模型生成导数，就优先利用这层数学结构；若使用差分，就通过一组步长检查结果是否进入稳定区间。

误差纵轴采用牛顿，展示估计力与精确导数之间的绝对差。若把模型的力尺度整体放大，绝对误差也可能变大，因此跨模型比较时还可以考虑用一个明确的参考力归一化。当前位置的力接近零时，直接除以它会造成很大的相对误差；选择参考尺度也属于计算问题的定义。本节保留绝对误差，便于逐点对应前面的0.005 N算例。

## 完整程序：推导、求解、导出和作图

程序首先创建带条件的符号，用精确分数构造能量，然后求出力、刚度和中心差分误差。随后代入同一组参数，把几个关键值保存在数值摘要里，再生成模型表与差分误差表。三个图文件分别展示物理量之间的关系、表达式树和误差竞争。图中的模型数据、节点结构与误差曲线均由这次计算产生。

### 完整示例：从能量表达式到数值误差

生成模型与误差CSV、数值摘要，以及物理量、表达式树、差分误差三幅图。使用SymPy推导与求解，再用NumPy计算数组。

```
"""Derive a spring model symbolically, then evaluate it with NumPy."""
from pathlib import Path
import argparse
import json
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def expression_tree(ax, expression):
    """Draw the actual func/args structure; each leaf receives one position."""
    nodes, edges = [], []
    next_leaf = [0]

    def visit(expr, depth=0):
        index = len(nodes)
        nodes.append(None)
        children = [visit(child, depth + 1) for child in expr.args]
        if children:
            horizontal = np.mean([nodes[child][0] for child in children])
        else:
            horizontal = next_leaf[0]
            next_leaf[0] += 1
        label = expr.func.__name__ if children else str(expr)
        nodes[index] = (horizontal, -depth, label, bool(children))
        edges.extend((index, child) for child in children)
        return index

    visit(expression)
    for parent, child in edges:
        a, b = nodes[parent], nodes[child]
        ax.plot([a[0], b[0]], [a[1], b[1]], color='#b7c6cd', lw=1.7, zorder=0)
    for x, y, label, branch in nodes:
        ax.text(x, y, label, ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round,pad=.48', facecolor='#eaf2f5' if branch else '#fbf1e9',
                          edgecolor='#28658c' if branch else '#b36837', lw=1.3))
    ax.set(xlim=(-.65, next_leaf[0] - .35), ylim=(-3.65, .65))
    ax.axis('off')
    return len(nodes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ['Noto Sans CJK SC', 'Noto Sans SC',
        'Microsoft YaHei', 'SimHei', 'DejaVu Sans'] if f in available],
        'font.size': 12, 'svg.fonttype': 'none', 'axes.spines.top': False,
        'axes.spines.right': False, 'grid.alpha': .16})

    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)

    # Numerical values use mm, N, and N*mm (= mJ) consistently.
    x = sp.Symbol('x', real=True)
    k = sp.Symbol('k', positive=True)
    alpha = sp.Symbol('alpha', nonnegative=True)
    h = sp.Symbol('h', positive=True)
    U = sp.Rational(1, 2) * k * x**2 + sp.Rational(1, 4) * alpha * x**4
    F = sp.diff(U, x)
    K = sp.diff(F, x)
    reconstructed = sp.integrate(F, x)
    assert sp.simplify(reconstructed - U) == 0
    centered = (U.subs(x, x + h) - U.subs(x, x - h)) / (2 * h)
    truncation = sp.expand(centered - F)
    assert sp.simplify(truncation - alpha * x * h**2) == 0
    values = {k: sp.Integer(2), alpha: sp.Rational(1, 2)}
    exact_one = [expr.subs(values).subs(x, 1) for expr in (U, F, K)]
    work = sp.integrate(F.subs(values), (x, 0, 2))
    equilibrium = sp.nsolve(F.subs(values) - 3, x, 1, prec=40)
    equilibrium_residual = abs((F.subs(values) - 3).subs(x, equilibrium))
    u_num = sp.lambdify((x, k, alpha), U, modules='numpy')
    f_num = sp.lambdify((x, k, alpha), F, modules='numpy')
    stiffness_num = sp.lambdify((x, k, alpha), K, modules='numpy')
    grid = np.linspace(0, 2, 401)
    energy = u_num(grid, 2., .5)
    force = f_num(grid, 2., .5)
    stiffness = stiffness_num(grid, 2., .5)
    np.savetxt(args.output / 'model.csv', np.column_stack([grid, energy, force, stiffness]),
               delimiter=',', header='displacement_mm,energy_mJ,force_N,stiffness_N_per_mm', comments='')

    fig, axes = plt.subplots(1, 3, figsize=(13.4, 5.2), layout='constrained')
    for a, color in zip([0., .5, 2.], ['#82939b', '#28658c', '#c26835']):
        for ax, fn in zip(axes, [u_num, f_num, stiffness_num]):
            output = np.broadcast_to(fn(grid, 2., a), grid.shape)
            ax.plot(grid, output, color=color, lw=2.3, label=f'α = {a:g} N/mm³')
    for ax, value, title, ylabel in zip(axes, [1.125, 2.5, 3.5],
        [tr('A  储存了多少能量', 'A  Stored energy'), tr('B  维持位移的外力', 'B  Holding force'),
         tr('C  当前有多难再拉长', 'C  Tangent stiffness')],
        [tr('储能 U / mJ', 'Energy U / mJ'), tr('外力 F / N', 'Applied force F / N'),
         tr('切线刚度 K / (N/mm)', 'Tangent stiffness K / (N/mm)')]):
        ax.scatter([1], [value], s=58, color='#28658c', edgecolor='white', zorder=5)
        ax.annotate(f'{value:g}', (1, value), xytext=(6, 10), textcoords='offset points', color='#28658c',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=.85, pad=.5))
        ax.set(title=title, xlabel=tr('位移 x / mm', 'Displacement x / mm'), ylabel=ylabel, xlim=(0, 2))
        ax.set_xticks([0, .5, 1, 1.5, 2]); ax.grid(True)
    axes[0].legend(loc='upper left', fontsize=11)
    fig.suptitle(tr('同一个储能函数的三个读法；k = 2 N/mm',
                       'Three readings of one energy function; k = 2 N/mm'), fontsize=16)
    save(fig, 'mechanics')

    fig = plt.figure(figsize=(12, 6.8), layout='constrained')
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])
    ax = fig.add_subplot(gs[0]); node_count = expression_tree(ax, U)
    ax.set_title(tr('SymPy的2017年论文：表达式树架构',
                       'Expression-tree architecture in the 2017 SymPy paper'), fontsize=16, pad=14)
    ax = fig.add_subplot(gs[1]); ax.axis('off')
    ax.text(.02, .73, '$U=' + sp.latex(U) + '$', fontsize=19, transform=ax.transAxes)
    ax.text(.55, .73, '$F=' + sp.latex(F) + '$', fontsize=19, transform=ax.transAxes)
    ax.text(.02, .05, tr('Add：相加     Mul：相乘     Pow：乘方；叶子保留符号和精确分数。',
        'Add: sum     Mul: product     Pow: power; leaves retain symbols and exact fractions.'),
        fontsize=12, transform=ax.transAxes)
    save(fig, 'history')

    steps = np.logspace(-14, -1, 170)
    differences = (u_num(1 + steps, 2., .5) - u_num(1 - steps, 2., .5)) / (2 * steps)
    errors = abs(differences - 2.5)
    exact_error = .5 * steps**2
    np.savetxt(args.output / 'difference-error.csv', np.column_stack([steps, differences, errors, exact_error]),
        delimiter=',', header='step_mm,centered_force_N,absolute_error_N,exact_arithmetic_error_N', comments='')
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6), layout='constrained', gridspec_kw={'width_ratios': [1, 1.22]})
    local = np.linspace(.65, 1.35, 200); hh = .2
    secant = float((u_num(1 + hh, 2., .5) - u_num(1 - hh, 2., .5)) / (2 * hh))
    intercept = float((u_num(1 + hh, 2., .5) + u_num(1 - hh, 2., .5)) / 2)
    axes[0].plot(local, u_num(local, 2., .5), color='#28658c', lw=2.5, label=tr('能量曲线', 'Energy'))
    axes[0].plot(local, 1.125 + 2.5 * (local - 1), color='#2b8a74', ls='--', label=tr('中心切线', 'Center tangent'))
    axes[0].plot(local, intercept + secant * (local - 1), color='#c26835', ls=':', lw=2.4, label=tr('两点割线', 'Two-point secant'))
    axes[0].scatter([.8, 1.2], u_num(np.array([.8, 1.2]), 2., .5), color='#c26835', zorder=5)
    axes[0].set(title=tr('A  先看斜率的几何意义', 'A  Read slope geometrically'),
        xlabel=tr('位移 / mm', 'Displacement / mm'), ylabel=tr('储能 / mJ', 'Stored energy / mJ'))
    axes[0].legend(loc='upper left', fontsize=11); axes[0].grid(True)
    positive = errors > 0
    axes[1].loglog(steps[positive], errors[positive], color='#28658c', lw=1.2, marker='.', ms=3,
                  label=tr('NumPy浮点计算', 'NumPy floating-point calculation'))
    axes[1].loglog(steps, exact_error, color='#c26835', lw=2.2, ls='--',
                  label=tr('精确算术：αxh²', 'Exact arithmetic: αxh²'))
    axes[1].set(title=tr('B  步长与力的绝对误差', 'B  Step size and absolute force error'),
        xlabel=tr('半间距 h / mm', 'Half-spacing h / mm'), ylabel=tr('绝对误差 / N', 'Absolute error / N'),
        ylim=(1e-17, .1))
    axes[1].legend(loc='upper center', fontsize=11); axes[1].grid(True, which='major')
    fig.suptitle(tr('x = 1 mm，k = 2 N/mm，α = 0.5 N/mm³；左图 h = 0.2 mm',
                       'x = 1 mm, k = 2 N/mm, α = 0.5 N/mm³; left panel h = 0.2 mm'), fontsize=14)
    save(fig, 'difference')
    summary = {'sympy_version': sp.__version__, 'energy_expression': str(U), 'force_expression': str(F),
        'stiffness_expression': str(K), 'truncation_expression': str(truncation),
        'energy_at_1_mJ': float(exact_one[0]), 'force_at_1_N': float(exact_one[1]),
        'stiffness_at_1_N_per_mm': float(exact_one[2]), 'work_0_to_2_mJ': float(work),
        'equilibrium_3N_mm': float(equilibrium), 'equilibrium_residual_N': float(equilibrium_residual),
        'centered_h01_N': float(centered.subs(values).subs({x: 1, h: sp.Rational(1, 10)})),
        'exact_h01_error_N': .005, 'expression_tree_nodes': node_count,
        'sqrt_real_x_squared': str(sp.sqrt(x**2)), 'zero_float_errors': int((errors == 0).sum()),
        'minimum_positive_float_error_N': float(errors[positive].min()),
        'maximum_float_error_N': float(errors.max())}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

运行后可先看摘要中的三个1 mm结果，再看0到2 mm的功。`equilibrium_3N_mm`对应反求的位移，`truncation_expression`对应差分误差恒等式。误差表保留每一个步长的估计力、实际绝对误差和精确算术误差，方便把图上的某一点追溯到数值。对数纵轴只能放正数，程序把恰好得到零误差的点计数后从该曲线中排除；本次运行中这个计数为零。

修改程序时，可以先把四次项系数改为零，检查力是否成为直线、刚度是否成为常数，再恢复到原值。随后增加一个新的储能项，观察导数和单位需要怎样调整。这种次序每次只改变一件事，容易把图形变化与公式变化连起来。新增项是否适合某种材料，则需要结合材料的实验响应来决定。

## 联动观察：能量曲线、力和计算误差

先保持默认位置1 mm和四次项系数0.5 N/mm³，读取1.125 mJ与2.5 N。上图同时画出能量曲线、当前位置的切线和两侧取值点；左下图追踪同一位置的外力，右下图显示不同步长下的误差，并标出当前选择。改变一个参数后，三幅图共同更新，便能看出物理模型变化与计算步长变化分别影响了什么。

### 从储能看局部斜率与数值误差

[Figure: 储能曲线、切线与取值点](https://ml-biomat.com/tutorials/python-scientific/p24/#P24-energy-view)

[Figure: 同一位置的力](https://ml-biomat.com/tutorials/python-scientific/p24/#P24-force-view)

[Figure: 差分的理论与浮点误差](https://ml-biomat.com/tutorials/python-scientific/p24/#P24-error-view)

固定k=2 N/mm。蓝色为模型或实际差分误差，绿色虚线为能量切线，橙色为两侧取值点或精确算术误差。对数误差图仅绘正误差；零值在读数中保留。

把四次项系数调到零，能量曲线仍然弯曲，但力曲线已经成为直线。此时精确差分误差为零，右下图显示的是浮点运算留下的误差；读数会明确报告这个零值。再恢复四次项，把步长从0.1 mm逐级缩小，观察实际误差何时不再跟随理论线下降。很小的两点间距在上图中难以直接分辨，误差图则把这一变化放在适合比较的对数尺度上。

最后把当前位置向较大位移移动。相同四次项系数下，切线更陡，维持位移所需的力更大，差分截断误差的系数也随位置改变。到这里，能量、导数、数组与误差已经连接在同一个问题里：先说明物理量和假设，再推导关系，最后让数值计算与图形共同检查这些关系。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P24.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SymPy: Basic Operations](https://docs.sympy.org/latest/tutorials/intro-tutorial/basic_operations.html)

   参数代入与表达式不可变性。

   BSD-3-Clause; technical reference
2. [SymPy: Calculus](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html)

   求导与积分接口。

   BSD-3-Clause; technical reference
3. [SymPy: Lambdify](https://docs.sympy.org/latest/modules/utilities/lambdify.html)

   按明确输入顺序连接NumPy。

   BSD-3-Clause; technical reference
4. [SymPy: Gotchas and assumptions](https://docs.sympy.org/latest/tutorials/intro-tutorial/gotchas.html)

   精确分数、符号与等号。

   BSD-3-Clause; technical reference
5. [SymPy: Assumptions](https://docs.sympy.org/latest/guides/assumptions.html)

   实数、正数和绝对值的适用条件。

   BSD-3-Clause; technical reference
6. [SymPy: Expression Manipulation](https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html)

   表达式树、func与args。

   BSD-3-Clause; technical reference
7. [SymPy: Numerical solving](https://docs.sympy.org/latest/guides/solving/solve-numerically.html)

   nsolve与求根初值。

   BSD-3-Clause; technical reference
8. [Meurer et al. (2017): SymPy, symbolic computing in Python](https://github.com/sympy/sympy-paper)

   原作者公开的论文与架构说明，DOI:10.7717/peerj-cs.103。

   Published article CC-BY-4.0; historical reference; figures here original
