# 数字、单位与计算机里的近似

Source: https://ml-biomat.com/tutorials/python-scientific/p02/
Language: zh-CN

从一条薄膜的应力计算，分清单位换算、测量变化与浮点舍入。

## 为什么同一个样品，会被算出相差一百万倍的结果？

一条薄膜受到 5 N 的拉力，宽度为 2 mm，厚度为 0.10 mm。把拉力除以横截面积，就能得到用于比较拉伸状态的名义应力。计算只涉及一次乘法和一次除法，却很容易在单位上出错：毫米直接相乘得到平方毫米，米直接相乘得到平方米，两者相差一百万倍。如果程序只保存数字、不保存我们对单位的理解，错误的结果也会被迅速算出，并带着许多小数位出现在图上。本章从这条薄膜出发，讨论怎样让数字、单位和计算精度始终对应同一件事。

N 是牛顿，用来表示力；mm 是毫米，用来表示长度。想象几个人拉着两条材料相同、粗细不同的带子，拉力一样时，较细的带子把同样的力分摊在较小的截面上，所以每单位面积承受的力更大。名义应力正是把拉力按原始截面积归一化的量。本章采用宽度乘厚度得到的矩形初始截面，不考虑局部缺口和截面内部的应力变化。这里的数值是定义明确的教学输入，重点是计算方法与尺度关系，而不是预测某种薄膜会在什么载荷下断裂。

另一个看起来完全不同的问题，也会出现在这次计算里：`0.1 + 0.2` 为什么可能显示为 `0.30000000000000004`？前者是单位错配，后者是有限数值表示造成的微小偏差，它们需要不同的处理方法。给结果多保留几位小数，解决不了单位错误；把图上的尾数隐藏起来，也没有改变计算机内部保存的数。我们将用实际 Python 代码把这几种问题分开，再通过厚度变化实验，比较输入测量变化和计算舍入究竟怎样影响结果。

本章需要上一章中的变量、相乘和相除概念。新的工具只有几个：表示整数与浮点数的类型、科学计数法、Python 自带的 `math`、`decimal` 和 `fractions` 模块。完整示例会给出同一应力的两套单位计算、三种数字表示的对照，以及厚度输入变化的曲线。所有图都由这些确定的算式产生，因而你可以选一个点先用纸笔计算，再到图和数值摘要中找到它。

![相同初始矩形截面在两套单位下给出25 MPa。下方解析曲线固定力与宽度，展示厚度在分母中的作用及正负偏移的不对称。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8cee4fbdcd750fbc163a0c29.svg?v=8cee4fbdcd75)

图 1相同初始矩形截面在两套单位下给出25 MPa。下方解析曲线固定力与宽度，展示厚度在分母中的作用及正负偏移的不对称。

## 把单位带进计算，面积换算就不会少乘一次

1 m 等于 1000 mm，因此 1 mm 是 0.001 m。把宽度与厚度都换成米，得到 0.002 m 和 0.0001 m；两者相乘为 0.0000002 m²。如果保留毫米，面积为 2×0.10=0.20 mm²。这两个写法描述完全相同的截面。面积包含两次长度相乘，每个长度中的千分之一都要保留，所以从平方毫米换到平方米时，换算因子是百万分之一。可以想象把一条边上的毫米刻度放进正方形网格：横向和纵向都缩放，面积的缩放就会同时积累两个因子。

$$
A=bt,\qquad 1\,\mathrm{mm}^2=(10^{-3}\,\mathrm{m})^2=10^{-6}\,\mathrm{m}^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 矩形截面积；可用mm²或m²，须与两条边的单位一致 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 初始宽度，mm或m |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 初始厚度，与宽度使用同一长度单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/caa594000bc5cab4891fd227.svg) | 千分之一，无量纲单位换算因子 |
| ![Formula](https://ml-biomat.com/static/agent-math/9d3c6e8b3220d80e71bb33eb.svg) | 平方，表示两个相同因子相乘；面积单位包含两次长度 |

2 mm×0.10 mm=0.20 mm²。分别换成米后为0.002 m×0.0001 m=2×10⁻⁷ m²。面积换算同时包含两个长度换算因子。

用牛顿除以平方米得到帕斯卡，符号 Pa；一百万帕斯卡为 1 MPa，M 是表示百万的单位前缀。于是 5 N 除以 0.0000002 m² 得到 25000000 Pa，也就是 25 MPa。另一条路线更短：5 N 除以 0.20 mm² 得到 25 N/mm²，而 1 N/mm² 恰好等于 1 MPa。两条路线都正确，条件是每次相乘、相除与最后的单位名称保持一致。把数值 25 写成 Pa，就会把一个正确的算式解释成错误的物理量。

$$
\sigma=\frac{F}{A}=\frac{F}{bt},\qquad 1\,\mathrm{N/mm^2}=10^6\,\mathrm{Pa}=1\,\mathrm{MPa}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 以初始截面归一化的名义应力；使用N与mm时为MPa，使用N与m时为Pa |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 沿样品轴向的拉力，N |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 正的初始截面积，mm²或m² |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 初始宽度，mm或m |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 初始厚度，与宽度单位一致 |
| ![Formula](https://ml-biomat.com/static/agent-math/80f0e0ae45cf90c79ea06edc.svg) | 帕斯卡，1 Pa=1 N/m² |
| ![Formula](https://ml-biomat.com/static/agent-math/dfc02cd70c8bfefa2abfca40.svg) | 兆帕，1 MPa=10⁶ Pa |

名义应力把拉力按原始矩形截面分摊：5/0.20=25 N/mm²=25 MPa。用平方米计算为5/(2×10⁻⁷)=2.5×10⁷ Pa，再除以10⁶得到25 MPa。

Python 中的 `1e-3` 表示一乘十的负三次方，也就是 0.001；`2e-7` 表示 0.0000002。这里的 `e` 是科学计数法的写法，不是一个变量，也不是自然常数。负指数表示反复除以十，正指数表示反复乘以十。科学计数法把很多零压缩成数量级，适合检查一个数处于什么尺度。它与单位前缀有相似的阅读作用，但表达层次不同：`1e6` 是一个数，MPa 则是带有百万因子的单位。

### 两条单位路线

两项均为25.0，分别经N/mm²与N/m²得到MPa。

```
force_N = 5.0
width_mm = 2.0
thickness_mm = 0.1
area_mm2 = width_mm * thickness_mm
stress_MPa = force_N / area_mm2
width_m = width_mm * 1e-3
thickness_m = thickness_mm * 1e-3
area_m2 = width_m * thickness_m
stress_Pa = force_N / area_m2
print(stress_MPa, stress_Pa / 1e6)
```

在代码中把变量命名为 `width_mm`、`width_m` 和 `area_m2`，可以让换算过程直接可见。把所有输入先转成一套内部单位，再集中计算，通常比在多个算式之间反复换算更容易检查；输出时按读者熟悉的单位转换即可。也可以全程采用 N 与 mm，只要公式和结果标签都配套。本章同时保留两种路线，是为了建立独立的数值核对。单位换算得到一致结果，比只重复运行同一行代码更能暴露尺度错误。

## 共同的米，来自怎样的测量历史？

单位并不是给数字补上的装饰。两间实验室都写下“长度为 1”，如果没有共同的参照，仍然无法比较它们测量的是多长。米的历史很好地展示了共同参照如何发展。1889 年的定义联系到铂铱米原器上的长度；1960 年，定义转向氪86辐射的波长；1983 年，又转向光在真空中一定时间内传播的距离。国际计量局对这段历史的说明强调，改变定义与改进单位的实际复现能力有关，而不只是替换一个文字约定。

下图画出了三种方法各自在比较什么。原器方法需要把长度与共同保存的实物联系起来；光学方法把长度连接到可重复观测的辐射与干涉；光速定义则把长度与时间标准联系起来。今天，真空光速的数值被固定为每秒 299792458 米，米因此可以通过秒与光速建立定义。图中的c表示真空光速，单位m/s；Δt表示时间间隔，单位s，相乘得到以米表示的长度。取Δt为1/299792458秒，就得到1米。图中的光路概括了定义中的长度与时间关系，实际复现米则需要精密光学与时间计量技术。

![长度计量方法的原创图解：实物刻线比较、光学波长联系，以及真空光速与时间的定义关系。图形表示方法，没有按比例重建历史仪器。](https://ml-biomat.com/static/tutorials/python-scientific/figures/e9fb5cd6da29b21533eb6d01.svg?v=e9fb5cd6da29)

图 2长度计量方法的原创图解：实物刻线比较、光学波长联系，以及真空光速与时间的定义关系。图形表示方法，没有按比例重建历史仪器。

这种历史变化帮助我们区分两个容易混在一起的问题：单位定义是否共同、一次具体测量能做到多精细。单位定义明确，不意味着手里的尺子能读出任意多位；天平使用克，也不意味着每个显示数字都具有相同的测量可信度。程序中的换算关系可以是精确的，例如毫米与米之间的十进制关系，而输入厚度仍然受测量方法、位置和样品表面影响。计算把这些输入传播到结果里，却不会凭空补出仪器没有提供的信息。

科研软件中的共同单位约定，与历史上的共同计量参照解决着相近的协作问题。一个文件写毫米，另一个文件写米，只要转换规则明确，就能放进同一计算；若只看数值大小猜单位，错误可能隐藏到很晚才被发现。保存数据时，把单位放在清楚的字段名或元数据中；绘图时，把它写在坐标轴旁；函数接收输入时，把预期单位写进说明。这样，单位就成为计算过程的一部分，而不必依靠某个使用者一直记得。

## 计算机里的数，是有限刻度上的位置

Python 的整数类型 `int` 适合计数，例如样品个数和循环次数。普通 Python 整数可以随着数值增长使用更多存储空间，因此不局限于某个固定的十位数范围；计算仍然受到可用内存和时间限制。带小数点的常见类型是 `float`，它适合用有限空间表示很大或很小的数，并支持高效数值运算。它的表示方式类似科学计数法：一部分记录有效数字，一部分记录尺度。有效数字的数量有限，意味着许多实数需要用邻近的可表示数来近似。

先从十进制熟悉的例子理解这种近似。三分之一写成 0.3、0.33、0.333，会越来越接近精确分数，但只要小数位有限，就没有写完。同样，二进制小数的各位分别表示二分之一、四分之一、八分之一，依次继续。例如 0.625 可以由二分之一加八分之一精确组成，而十进制 0.1 在二进制中需要不断延续的位。计算机必须在某处停止，于是保存最近的某个有限表示。错误的来源是表示规则与有限长度，而不是机器不会做小学加法。

$$
0.625=1\times2^{-1}+0\times2^{-2}+1\times2^{-3}=\frac12+0+\frac18
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7303dcd9121400b1daa141ec.svg) | 待表示的无量纲数 |
| ![Formula](https://ml-biomat.com/static/agent-math/3ecfcbd49f702b154e843aff.svg) | 二进制小数点后的第一、第二、第三位权重，分别为1/2、1/4、1/8，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/dc8c18188ba2a40751b5057e.svg) | 各二进制小数位是否取用对应权重，只能为0或1 |
| ![Formula](https://ml-biomat.com/static/agent-math/a28115dcd3646ef2947dff18.svg) | 分别表示权重相乘与各项相加 |

二进制小数0.101的三位依次取一半、不取四分之一、取八分之一，相加为0.625。十进制0.1在同样的二进制规则下需要无限延续的位，因此有限存储时会近似。

图上先使用一个刻意简化的固定小数位网格，让每个可选位置都能看清。小数位增加时，格点更密，0.1 附近的近似也更细。这是帮助理解舍入的玩具模型；实际浮点数还包含尺度部分，不同数量级附近的格点间距会改变。Python 常见的双精度浮点数在 1 附近，相邻可表示数间距约为 2.22×10⁻¹⁶。用 `math.ulp(1.0)` 可以读取这个尺度；它描述计算机表示的间距，与某台实验仪器的分辨率是两件事。

![固定二进制小数位的玩具网格把舍入位置画出来；下方显示实际Python执行得到的浮点、十进制和分数结果。玩具网格与实际浮点格式分开标明。](https://ml-biomat.com/static/tutorials/python-scientific/figures/82fe9cb7c19fe4b656e93781.svg?v=82fe9cb7c19f)

图 3固定二进制小数位的玩具网格把舍入位置画出来；下方显示实际Python执行得到的浮点、十进制和分数结果。玩具网格与实际浮点格式分开标明。

`0.1 + 0.2` 中的两个输入已经经过二进制近似，相加后还要把结果放回可表示数中，因此直接显示时可能看到长尾数。Python 通常尽量用简短的十进制文字表示一个浮点值，所以单独打印 `0.1` 往往仍只看到三个字符。这种简洁显示没有把内部值变成精确的十分之一。用格式化字符串减少小数位，或调用 `round`，都需要理解它们改变的是哪一层：面向读者的显示、另一个舍入结果，还是确实不同的数字表示方式。

## 什么时候需要整数、十进制数或分数？

从文件或输入框读到的内容，常常先是文字。例如`"0.10"`包含四个字符，调用`float("0.10")`后才得到可用于相乘的数。`int("3")`把表示整数的文字转成整数，但`int(3.9)`会向零截去小数部分，得到3，而不是按四舍五入得到4。数值转换需要符合对象含义，不能把一个小数长度随手转成整数来“去掉尾数”。Python中的`/`执行普通除法，`//`执行向下取整的除法；例如7/2得到3.5，7//2得到3。后者适合计算能够组成多少个完整分组，却会丢掉面积归一化中需要保留的小数。同一个符号看起来只多了一条斜线，回答的问题已经改变了。

选择数值类型，应从数据和运算的含义出发。样品数量通常使用整数，因为半个记录行没有这里需要的含义；连续长度、力和数值求解通常使用浮点数，因为计算速度、库兼容性和数量级范围都很合适。当十进制输入必须保留特定规则，例如逐项核对按十进制记录的金额或配比时，可以使用 `Decimal`。它按十进制处理数值，`Decimal("0.1")` 加 `Decimal("0.2")` 能精确得到十进制 0.3。选择这种类型，改变的是数的表示与算术规则。

引号在这里尤其重要。`Decimal("0.1")` 从文本读取十进制数，`Decimal(0.1)` 则接收已经建立好的浮点数，并把那个浮点值精确转换成十进制表示。后者会把此前的二进制近似一并保留下来。可以把它理解为复印不同的原稿：从十进制文字起步，得到文字表达的数；从浮点数起步，得到机器此前实际保存的数。若上游数据已经被近似处理，换一种容器不会自动恢复丢失的信息。

`Fraction` 则使用整数分子与整数分母表示有理数，例如 `Fraction(1, 3)` 精确保存三分之一。它适合讲解比例、检查有理算式或处理需要精确分数的离散关系。不断做复杂运算时，分子分母可能变得很大，计算成本也会增加；平方根、圆周率等数也不能普遍写成两个整数的比。`Decimal` 同样不是所有运算都无须近似：在设置十二位精度后计算三分之一，仍然只能保存有限位小数。这里的选择是使表示方法与问题匹配，而不是把某一种类型当作所有科学计算的统一替代品。

### 数字表示与求和方法

依次输出0.30000000000000004、0.3、3/10、0.0、1.0。

```
from decimal import Decimal
from fractions import Fraction
import math
print(repr(0.1 + 0.2))
print(Decimal("0.1") + Decimal("0.2"))
print(Fraction(1, 10) + Fraction(2, 10))
print((1e16 + 1.0) - 1e16)
print(math.fsum([1e16, 1.0, -1e16]))
```

即使所有输入都能精确表示，运算顺序也可能使小贡献丢失。先算 `1e16 + 1.0`，此时大数附近的浮点格点已经容不下这一个单位的增加；再减去 `1e16`，结果成为 0。数学上这三个数相加应为 1。`math.fsum` 专门改进浮点求和中的精度处理，本例会得到 1.0。这里的重点是先理解大数与小数混合时发生了什么，再选用合适算法。给最终的零增加更多显示位数，并不能把已经丢掉的贡献重新找回来。

## “足够接近”必须带有尺度

用 `==` 比较两个浮点数，询问的是它们是否完全相等。对于编号、整数计数和某些明确的离散状态，这样的比较很自然；对于经过不同浮点运算路线得到的量，常常需要问它们的差是否小于一个明确尺度。`math.isclose` 把这个问题写成了带参数的比较。相对容差按数值大小缩放，绝对容差使用与被比较数相同的单位。两者的目的不同：前者控制比例上的接近程度，后者给零附近提供一个有实际意义的比较尺度。

$$
|x-y|\leq\max\!\left(r\max(|x|,|y|),a\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | 待比较的两个数，必须表示相同物理量并使用相同单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 非负相对容差，无量纲；math.isclose中对应rel_tol |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 非负绝对容差，与x、y同单位；对应abs_tol |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | 绝对值，只取大小，不保留正负号 |
| ![Formula](https://ml-biomat.com/static/agent-math/8228983b74c5db73c259fc11.svg) | 取括号中较大的量 |
| ![Formula](https://ml-biomat.com/static/agent-math/97a7392d70b366cf7bc75310.svg) | 小于或等于，满足时返回True |

比较0与10⁻⁹，若r=10⁻⁶、a=0，阈值为10⁻¹⁵，差10⁻⁹超出阈值；改为a=2×10⁻⁹后满足条件。相对尺度与零附近的绝对尺度各自承担明确作用。

例如比较 25.000000000 MPa 与 25.000000001 MPa，差约为十亿分之一 MPa。若相对容差设为 10⁻⁹，允许差值约为 25×10⁻⁹ MPa，这两个数会被认为接近。但比较 0 与 10⁻⁹ 时，相对容差 10⁻⁶ 只给出 10⁻¹⁵ 的阈值，二者仍不接近；设绝对容差为 2×10⁻⁹，才明确允许这种零附近的差。容差不是隐藏错误的按钮，应来自当前检查要分辨的尺度。数值算法复核可以使用很小的计算容差，实验测量比较则要依据测量定义和数据精度另行选择。

Python 在 2015 年提出并随后引入 `math.isclose` 的设计讨论中，专门处理了零附近的比较问题。它把各程序原先可能自行编写、容易不一致的规则，变成含义明确的公共接口。这样的计算史与米的历史可以放在一起理解：前者建立数值比较的共同规则，后者建立物理测量的共同参照。规则明确后，使用者仍需选择符合任务的尺度。默认参数是一个起点，不能代替对实验问题的判断。

在同一量的不同单位之间使用绝对容差时，也要跟着换算。2×10⁻⁹ MPa 与 2×10⁻³ Pa 表示同一个物理差值；如果数值换成 Pa、绝对容差却原样保留，比较规则已经变了。相对容差没有单位，在一致的比例换算下更容易保持含义。阅读别人给出的“通过误差检查”时，应查看比较的量、单位、阈值以及计算路线，这些信息共同说明检查回答了什么问题。

## 完整运行：把三种误差放到各自的位置

完整脚本先用两条单位路线计算薄膜的名义应力，然后演示浮点数、十进制数和分数的表示，最后生成厚度敏感性、有限数轴和长度计量史三幅图。输入宽度与厚度是初始截面尺寸，因此图上的应力始终是名义应力；后续若使用拉伸中的实时面积，得到的就是另一种定义，需要同步更改变量、图轴和解释。计算模型的含义由这些约定确定，不能仅凭公式外观判断。

### 完整计算与三幅图

数值部分使用Python标准库；图形依赖Matplotlib。

```
"""Units, floating-point representation and thickness sensitivity."""
from pathlib import Path
import argparse
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=="zh"
    def tr(a,b): return a if zh else b

    # Defined teaching model; width and thickness are initial dimensions.
    force_N=5.0; width_mm=2.0; thickness_mm=0.1
    width_m=width_mm*1e-3; thickness_m=thickness_mm*1e-3
    area_mm2=width_mm*thickness_mm
    area_m2=width_m*thickness_m
    stress_Pa=force_N/area_m2
    stress_MPa=stress_Pa/1e6
    stress_from_mm=force_N/area_mm2
    assert math.isclose(stress_MPa,stress_from_mm,rel_tol=1e-12)

    decimal_sum=Decimal("0.1")+Decimal("0.2")
    rational_sum=Fraction(1,10)+Fraction(2,10)
    float_sum=0.1+0.2
    cancellation=(1e16+1.0)-1e16
    stable_sum=math.fsum([1e16,1.0,-1e16])
    with localcontext() as ctx:
        ctx.prec=12
        decimal_third=str(Decimal(1)/Decimal(3))
    print(f"Area: {area_mm2:.3f} mm^2 = {area_m2:.3e} m^2")
    print(f"Nominal stress: {stress_MPa:.3f} MPa")
    print("Float addition:",repr(float_sum),"Decimal:",decimal_sum,"Fraction:",rational_sum)
    print("Cancellation:",cancellation,"math.fsum:",stable_sum)
    print("Near zero, relative-only:",math.isclose(0,1e-9,rel_tol=1e-6))
    print("Near zero, absolute tolerance:",math.isclose(0,1e-9,abs_tol=2e-9))

    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ["Noto Sans CJK SC","Microsoft YaHei","DejaVu Sans"] if f in fonts),"DejaVu Sans")
    plt.rcParams.update({"font.family":[family,"DejaVu Sans"] if zh else ["DejaVu Sans"],"font.size":12,"axes.titlesize":15,"axes.titleweight":"bold","svg.fonttype":"none","figure.facecolor":"#fbfaf6","axes.facecolor":"#fbfaf6","text.color":"#172b36","axes.labelcolor":"#172b36","axes.spines.top":False,"axes.spines.right":False})
    blue,red,ink,green="#28648a","#b85336","#172b36","#467a62"
    def save(fig,name):
        fig.savefig(args.output/f"{name}-{args.language}.svg",bbox_inches="tight")
        fig.savefig(args.output/f"{name}-{args.language}.png",dpi=180,bbox_inches="tight")
        plt.close(fig)

    fig=plt.figure(figsize=(12,7),layout="constrained")
    gs=fig.add_gridspec(2,2,height_ratios=[.9,1.3])
    ax=fig.add_subplot(gs[0,:]);ax.axis("off")
    ax.text(.01,.87,tr("a  同一截面，两套一致的单位", "a  One cross-section, two consistent unit choices"),fontsize=16,weight="bold",transform=ax.transAxes)
    ax.text(.03,.55,"2.00 mm × 0.10 mm = 0.20 mm²",fontsize=19,color=red,transform=ax.transAxes)
    ax.text(.03,.18,"0.002 m × 0.0001 m = 0.0000002 m²",fontsize=19,color=blue,transform=ax.transAxes)
    ax.text(.64,.55,"5 N / 0.20 mm² = 25 MPa",fontsize=17,color=red,transform=ax.transAxes)
    ax.text(.64,.18,"5 N / (2 × 10⁻⁷ m²) = 25 × 10⁶ Pa",fontsize=15,color=blue,transform=ax.transAxes)
    ts=[.04+i*.001 for i in range(201)]
    ax=fig.add_subplot(gs[1,0]);ax.plot(ts,[force_N/(width_mm*t) for t in ts],lw=2.8,color=blue)
    for t in [.08,.1,.12]:
        y=force_N/(width_mm*t);ax.scatter([t],[y],s=55,color=red);ax.annotate(f"{t:.2f} mm → {y:.2f} MPa",(t,y),xytext=(.13,y+5) if t!=.12 else (.145,6),fontsize=11,arrowprops={"arrowstyle":"-","color":ink})
    ax.set(xlabel=tr("初始厚度 / mm","Initial thickness / mm"),ylabel=tr("名义应力 / MPa","Nominal stress / MPa"),title=tr("b  分母越薄，应力越大","b  A thinner denominator gives higher stress"),xlim=(.04,.24),ylim=(0,66));ax.grid(alpha=.15)
    ax=fig.add_subplot(gs[1,1]);errors=[-.4+i*.004 for i in range(201)]
    ax.plot([100*e for e in errors],[100*(1/(1+e)-1) for e in errors],color=red,lw=2.8)
    ax.axhline(0,color=ink,lw=.8);ax.axvline(0,color=ink,lw=.8)
    ax.scatter([-20,20],[25,-100/6],s=60,color=ink)
    ax.set(xlabel=tr("厚度输入相对偏差 / %","Relative thickness-input shift / %"),ylabel=tr("应力结果相对变化 / %","Relative stress change / %"),title=tr("c  相同正负偏差，影响并不对称","c  Equal signed shifts have unequal effects"));ax.grid(alpha=.15)
    save(fig,"units-sensitivity")

    fig=plt.figure(figsize=(12,7),layout="constrained")
    gs=fig.add_gridspec(2,2,height_ratios=[1.2,1])
    ax=fig.add_subplot(gs[0,:]);ax.set_xlim(-.025,.38);ax.set_ylim(-.35,1.7);ax.axis("off")
    ax.set_title(tr("a  玩具数轴：固定小数位，展示有限刻度", "a  A toy fixed-fraction grid makes finite spacing visible"),loc="left")
    for row,bits in enumerate([3,5,8]):
        y=1.3-row*.55;step=2**(-bits);ax.hlines(y,0,.35,color="#bcc7c7",lw=1)
        for k in range(int(.35/step)+1):ax.vlines(k*step,y-.05,y+.05,color=blue,lw=1)
        rounded=round(.1/step)*step;ax.scatter([rounded],[y],s=65,color=red,zorder=3)
        ax.annotate(f"{bits} bits: {rounded:.7f}",(rounded,y),xytext=(.19,y+.07),fontsize=12,arrowprops={"arrowstyle":"-","color":red})
    ax.axvline(.1,ymin=.13,ymax=.9,color=ink,ls="--",lw=1.4);ax.text(.1,-.2,"0.1",ha="center",fontsize=14)
    ax.text(.005,1.57,tr("红点：离0.1最近的格点；这不是实际float格式。","Red: nearest grid point to 0.1; this is not the actual float format."),fontsize=12)
    ax=fig.add_subplot(gs[1,0]); ax.axis("off")
    ax.set_title(tr("b  实际Python浮点加法", "b  Actual Python floating-point addition"),loc="left")
    ax.text(.02,.75,"0.1 + 0.2",fontsize=21,transform=ax.transAxes)
    ax.text(.02,.48,repr(float_sum),fontsize=21,color=blue,transform=ax.transAxes)
    ax.text(.02,.18,tr("显示位数改变文字，不改变已存储的值。","Formatting changes the text, not the stored value."),fontsize=12,transform=ax.transAxes)
    ax=fig.add_subplot(gs[1,1]);ax.axis("off")
    ax.set_title(tr("c  精确记录小数或有理数", "c  Exact decimal input or a rational value"),loc="left")
    ax.text(.02,.76,'Decimal("0.1") + Decimal("0.2")',fontsize=14,transform=ax.transAxes)
    ax.text(.02,.56,str(decimal_sum),fontsize=23,color=red,transform=ax.transAxes)
    ax.text(.02,.30,'Fraction(1, 10) + Fraction(2, 10)',fontsize=14,transform=ax.transAxes)
    ax.text(.02,.10,str(rational_sum),fontsize=23,color=green,transform=ax.transAxes)
    save(fig,"finite-number-lines")

    fig=plt.figure(figsize=(12,6.3),layout="constrained");ax=fig.add_subplot();ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,6.3)
    ax.text(.1,5.9,tr("长度标准怎样变得可以重现？", "How can a length standard become reproducible?"),fontsize=19,weight="bold")
    ax.text(.1,5.35,tr("原创方法示意：原器比较 → 光学计数 → 由光速与时间定义", "Original method schematic: artifact comparison → optical counting → light and time"),fontsize=12)
    ax.add_patch(Rectangle((.3,3.6),3.1,.35,facecolor="#bfc6c5",edgecolor=ink))
    for x in [.55,3.15]:ax.plot([x,x],[3.5,4.08],color=ink,lw=2)
    ax.annotate('',(.55,4.35),(3.15,4.35),arrowprops={"arrowstyle":"<->","color":ink})
    ax.text(1.85,4.55,tr("刻线间的距离","Distance between marks"),ha="center",fontsize=13)
    ax.text(.3,2.9,tr("铂铱原器（1889）", "Platinum–iridium (1889)"),fontsize=13,weight="bold")
    ax.text(.3,2.35,tr("与共同保存的实物比较", "Compare against a\nshared physical reference"),fontsize=13)
    xs=[4.4+i*.006 for i in range(451)];ys=[3.8+.27*math.sin((x-4.4)*2*math.pi/.45) for x in xs]
    ax.plot(xs,ys,color=blue,lw=2);ax.hlines(3.8,4.4,7.1,color="#bac4c6",lw=.7)
    ax.annotate('',(4.4,4.4),(4.85,4.4),arrowprops={"arrowstyle":"<->","color":ink});ax.text(4.625,4.58,tr("波长","Wavelength"),ha="center",fontsize=12)
    ax.text(4.4,2.9,tr("氪86辐射（1960）", "Krypton-86 radiation (1960)"),fontsize=13,weight="bold")
    ax.text(4.4,2.35,tr("通过光学干涉连接长度与波长", "Relate length to wavelength\nusing optical interference"),fontsize=12)
    ax.add_patch(FancyArrowPatch((8.4,3.8),(11.5,3.8),arrowstyle='->',mutation_scale=22,color=red,lw=2))
    ax.plot([8.5,8.5],[3.4,4.2],color=ink);ax.plot([11.35,11.35],[3.4,4.2],color=ink)
    ax.text(9.9,4.4,"c × Δt",ha="center",fontsize=21,color=red)
    ax.text(8.4,2.9,tr("真空中的光与时间（1983）", "Light in vacuum and time (1983)"),fontsize=12,weight="bold")
    ax.text(8.4,2.35,tr("固定光速，使用秒定义长度", "Fix light speed; use the\nsecond to define length"),fontsize=13)
    ax.text(.3,1.25,tr("今天的米：光在真空中经过1/299792458秒所走的距离。", "Today’s metre: the distance light travels in vacuum in 1/299792458 second."),fontsize=14)
    ax.text(.3,.55,tr("共同单位定义与实际测量精度，是两个相连但不同的问题。", "A shared unit definition and practical measurement precision are distinct, connected questions."),fontsize=13)
    save(fig,"length-history")
    summary={"model":"Nominal stress from initial rectangular section; defined teaching inputs","force_N":force_N,"width_mm":width_mm,"thickness_mm":thickness_mm,"area_mm2":area_mm2,"area_m2":area_m2,"stress_MPa":stress_MPa,"float_sum_repr":repr(float_sum),"decimal_sum":str(decimal_sum),"rational_sum":str(rational_sum),"decimal_third_12_digits":decimal_third,"direct_cancellation":cancellation,"fsum_result":stable_sum,"float_spacing_at_one":math.ulp(1.0),"near_zero_relative_only":math.isclose(0,1e-9,rel_tol=1e-6),"near_zero_absolute":math.isclose(0,1e-9,abs_tol=2e-9),"stress_at_thickness_mm":{str(t):force_N/(width_mm*t) for t in [.08,.1,.12]}}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')


if __name__=="__main__": main()
```

运行后，数值摘要应包含面积 0.20 mm²、面积 2×10⁻⁷ m² 和应力 25 MPa。浮点加法的文字表示为 `0.30000000000000004`，十进制加法保存为 `0.3`，有理数结果保存为 `3/10`。JSON 中将后两类值写成字符串，是为了保留它们的明确表示；如果直接转成普通浮点数再保存，就又回到了前面讨论的表示方式。图中的两条单位路线与数值摘要应一致，这是检查数据流是否连贯的起点。

### 运行并保存结果

输出包括summary.json与SVG、PNG科学图。

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

厚度敏感性图则展示一个远大于浮点尾数的变化。保持 5 N 和 2 mm 不变，把厚度从 0.10 mm 改为 0.08 mm，应力从 25 MPa 增至 31.25 MPa；厚度改为 0.12 mm，应力降至约 20.83 MPa。厚度减少 20% 带来应力增加 25%，厚度增加 20% 则带来应力减少约 16.67%。正负变化不对称，是因为厚度在分母中。输入测量的变化通过公式传播，形成了结果差别；这与存储 0.1 时微小的二进制近似不是一个量级的问题。

$$
t=t_0(1+\varepsilon),\qquad\frac{\sigma}{\sigma_0}=\frac{1}{1+\varepsilon},\qquad\frac{\sigma-\sigma_0}{\sigma_0}=\frac{1}{1+\varepsilon}-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 改变后的正厚度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a15f4e949d9181049b209fc5.svg) | 参考厚度，本例0.10 mm |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 厚度相对变化(t−t₀)/t₀，无量纲，须大于−1 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 改变厚度后的名义应力，MPa |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 相同力与宽度、参考厚度下的名义应力，MPa |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | 无量纲单位比值 |

固定力与宽度时，应力与厚度成反比。ε=−0.20时，应力比为1/0.8=1.25，增加25%；ε=+0.20时，应力比为1/1.2≈0.8333，减少约16.67%。

由此可以建立一个检查顺序。先核对对象和公式定义，再核对单位和数量级，随后查看输入测量如何影响输出，最后检查数值算法与表示误差。这个顺序直接对应问题的来源：面积错用了一百万倍时，先修单位；厚度取样位置差别较大时，先理解测量与几何；大数相消丢失了小贡献时，再改进算法。把所有差别统称为“精度问题”，会使真正需要采取的操作变得模糊。

## 改变厚度与单位，让几何、曲线和检查同步变化

下面的实验允许改变力、初始宽度和厚度，并选择以毫米或米显示长度。两个视图分别追踪几何截面与应力随厚度的变化，计算面板同时显示两条单位路线。先切换显示单位，观察截面的物理尺寸和最终 MPa 结果应保持不变；再增加厚度，截面面积增大，当前点沿应力曲线向下移动。为了能看清薄截面，几何图对两个方向使用分别标出的绘图尺度，长度标签给出真实数值。图形的形状承担定位作用，定量比较以坐标和计算结果为准。

### 一个截面，两条单位路线

尺寸输入以毫米记录，单位选择改变图内的显示。比较基准采用当前的力与宽度、0.10 mm厚度。

[Figure: 矩形截面与尺寸](https://ml-biomat.com/tutorials/python-scientific/p02/#P02-geometry)

[Figure: 厚度与应力的解析曲线](https://ml-biomat.com/tutorials/python-scientific/p02/#P02-curve)

把厚度记录的偏移设为正值或负值，可以同时看到名义应力和相对变化。程序保留 0.10 mm 作为厚度比较基准，但力与宽度仍采用当前输入，因此基准点与当前点回答的是同一组加载条件下的厚度问题。再改变相对容差与绝对容差，检查当前结果与基准是否被规则判为接近。这个判断由你输入的阈值决定，图上的点和两者差值始终保留，使“接近”不会遮住发生了多少变化。

最后可以独立验证一个新组合：力 8 N，宽 4 mm，厚 0.20 mm，截面积为 0.80 mm²，应力为 10 MPa。把毫米转换成米后，应得到相同结果。若把所有长度同时放大两倍、力保持不变，面积变为四倍，应力变为原来的四分之一。能解释这两个检验，就说明单位、乘法中的维度和比例关系已经连在一起。下一章把这种清楚的量与单位组织进列表和字典，为处理多个实验样品作准备。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Python — Floating-point arithmetic](https://docs.python.org/3.14/tutorial/floatingpoint.html)

   数值表示、二进制小数与显示的技术基础。

   PSF documentation license
2. [Python — Decimal](https://docs.python.org/3.14/library/decimal.html)

   构造输入与精度上下文。

   PSF documentation license
3. [Python — Fractions](https://docs.python.org/3.14/library/fractions.html)

   整数分子分母与浮点转换的区别。

   PSF documentation license
4. [Python — math](https://docs.python.org/3.14/library/math.html)

   fsum、ulp与isclose的操作定义。

   PSF documentation license
5. [PEP 485 — Approximate equality](https://peps.python.org/pep-0485/)

   近似相等规则与零附近比较的设计背景。

   Public-domain dedication in PEP
6. [BIPM — History of the metre](https://www.bipm.org/en/history-si/metre)

   长度标准从原器到光学方法的历史。
7. [BIPM — SI unit metre](https://www.bipm.org/en/si-base-units/metre)

   真空光速与米定义的精确关系。
