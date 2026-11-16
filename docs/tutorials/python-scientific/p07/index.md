# 把多次实验放进同一个数组

Source: https://ml-biomat.com/tutorials/python-scientific/p07/
Language: zh-CN

从三个样品、五个时刻出发，看清数组的形状、索引和轴怎样决定计算的含义。

## 三个样品、五个时刻，应该怎样放进计算机

把一片吸水后会膨胀的薄膜放进水里，隔一段时间测量厚度，就能得到一条随时间变化的曲线。若同时准备三个样品，问题很快变得更具体：三个样品是否以相近的速度变化？同一个时刻的典型厚度是多少？样品之间相差多少？这些问题会用到同一批数字，但需要以不同方式组合它们。本章从这样一张很小的表开始，学习NumPy怎样存放数值，以及怎样让每一步计算保留原来的实验含义。

这里使用一组明确构造的教学数据：三个样品记作A、B、C，在0、10、20、40和60 min分别记录厚度，单位为mm。数据被选成可以直接手算的小数，便于检查程序。它描述的是一个逐渐增厚的教学情境，不是某种真实材料的性能测量。三个样品的初始厚度略有差别，最后的变化幅度也不同。读图时既要看共同趋势，也要保留这些差别；如果过早把整张表压成一个平均值，许多原本能够回答的问题就消失了。

先给每个数字一个明确地址。第一行属于A，第二行属于B，第三行属于C；第一列是0 min，最后一列是60 min。样品B在20 min的厚度为1.16 mm，因此这个数既有“谁”的身份，又有“什么时候”的身份。就像一栋楼的房间要同时用楼层和门牌定位，表格中的一个观测也需要两个索引。NumPy把这种由规则索引定位的数值对象称为数组。二维数组可以画成表格，但数组这个概念还可以延伸到图像、三维体数据和多批实验。

把数据放入数组之前，先写清一行、一列分别代表什么，通常比记住某个函数更重要。若把样品与时间颠倒，数字本身不会报错，平均值也可能看起来很合理，但它回答的科学问题已经改变。计算机知道一个数组有三行五列，却不会自动知道第一维是三个独立制备的样品，第二维是同一批样品的五次重复观察。我们需要把这些含义保存在变量名、时间数组、图注和结果文件中。

![三行五列厚度热图与三个样品的时间曲线，标出同一观测。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8b8e526ae99f0aa9a89c8f53.svg?v=8b8e526ae99f)

图 1同一组教学数据的两种表示。左侧每一行对应一个样品，每一列对应一个时刻；右侧按样品分别绘制时间曲线，把每行连接成时间曲线。金色边框与圆圈指向同一个观测：样品B在20 min的厚度1.16 mm。

## 形状说明有几条索引，类型说明每格存什么

Python列表可以保存一组对象，也可以把列表放进列表。NumPy的数值数组进一步约定：这批元素采用共同的数据类型，并且各维长度形成规整的形状。把三个长度都是五的列表交给`np.array`，就得到一个形状为`(3, 5)`的数组。这里的圆括号表示一个元组；两个数字按索引次序给出各维长度。它们并不是物理空间中的长和宽，也不是数组里最小值与最大值。

`h.shape`给出`(3, 5)`，`h.ndim`给出2，`h.size`给出15。三个属性分别回答“每一维多长”“有几维”“总共有几个元素”。如果把同样十五个数放成一个长度为15的一维数组，总元素数没有改变，但样品与时间的分组方式需要由别的信息恢复。数组的维数也与物理向量的维数分属不同层次：一批三维坐标常用形状`(原子数, 3)`的二维数组保存；二维说的是需要两条索引，3才对应坐标分量。

本例用`dtype=np.float64`明确选择64位浮点数。浮点数允许小数参与计算，适合保存这里的厚度；64位描述的是存储格式，不是测量仪器准确到64位。输入1.20 mm也不会让程序知道测量分辨率是0.01 mm。若实验记录有精度或检出限，这些信息应另外保存。还要留意整数数组：向整数类型的格子写入小数时可能发生截断，保存后的数字含义随之改变。选择类型，是选择怎样表达数据，而不只是选择一个省内存的选项。

数组的共同类型让许多数值操作可以按统一规则执行，也使存储量容易估计。一个`float64`元素占8 byte，十五个元素的数值缓冲区占120 byte。Python还需要管理对象本身的额外信息，图像导出也需要保存布局和文字，因此`h.nbytes`不是整个脚本、整个文件夹或全部内存使用量。这个小例子中的差异很小，到了数千帧三维图像，先估算数组形状与元素大小，就能判断读取方式是否合适。

$$
B=N\,T\,b
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 数组数值缓冲区的字节数，单位byte；不包含Python对象管理开销。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 第一维长度，即样品数，本例3，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 第二维长度，即观测次数，本例5，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 每个元素占用的字节数；float64占8 byte。 |

本例3×5×8=120 byte，与h.nbytes一致。64表示每个浮点数64 bit，8 bit组成1 byte。把一个数组显示成热图不会改变这120 byte数值本身；图像文件还需要存颜色、文字和布局。

规整的形状还有一个实用含义：每一行应当对应相同的一组时间。如果A在10 min测量，而B的第二次测量实际发生在15 min，把两者直接放进同一列就会隐藏时间差。遇到这种数据，先保留每条记录自己的时间标签，再决定是否按时间对齐或插值。NumPy提供数值容器，数据是否可以直接排列成这张矩形表，需要由实验设计来决定。

## 科学家为什么需要一种共同的数组对象

科学计算经常需要对一整组数施加相同的规则。把每个温度减去一个参考值、对每个像素做标定、把每个原子的坐标平移相同距离，都是这样的任务。手工计算时，我们会先说明规则，再依次处理每个数。程序也可以逐个循环，但当“同一种规则作用于有结构的一组数”反复出现时，把这组数本身变成一个明确的对象，会让表达和不同程序之间的协作都更清楚。

NumPy的发展回应了这种需求。Harris等人在2020年的综述中回顾，1990年代的Numeric为Python提供了数值数组与了解数组的计算函数；之后的Numarray面向包括大型天文图像在内的需求，发展了更灵活的索引和内存处理能力。2005年开始的NumPy工作把这些既有方向整合到共同的数组基础上。这个历史过程与今天读取材料图像、整理坐标或分析测量曲线直接相关：应用领域不同，却都需要清楚描述数值在哪里、是什么类型以及怎样参与运算。

从这个角度看，`h.mean(axis=0)`不仅是一种简短写法。它同时交代了数据对象、操作和方向：在`h`中沿第0轴求平均。数组保留了形状与类型，计算函数可以利用这些信息解释操作。许多科学Python库也因此能够交换同一种数组，绘图库读取它来确定点的位置，优化库读取它来计算残差，图像库把它解释为像素。共同的表示减少了每换一个工具就重新组织数据的负担。

图中的存储条带把本例数值按行依次排开，说明二维形状与底层数值次序可以分开理解。它画的是本例创建的连续数组；实际NumPy还可以通过“步幅”描述怎样从一个元素走到下一个元素，所以切片形成的视图未必占据连续的一段位置。下一章会具体看这些视图怎样与原数组共享数据。现在先保留一个判断：数组的结构信息本身就是计算的一部分，不能只盯着打印出来的数字。

![数组值、形状和类型的存储示意，逐数计算与数组表达式的对应，以及三个数组项目的历史联系。](https://ml-biomat.com/static/tutorials/python-scientific/figures/9a168efa727313fe2580e5f2.svg?v=9a168efa7273)

图 2数组编程把数据对象与计算规则分开。上方用同一组厚度数值示意连续存储与行优先顺序，中间对应手算和NumPy表达式，下方概括Numeric、Numarray与NumPy的历史联系。存储条带是本例连续数组的示意；NumPy也能通过步幅描述非连续视图。历史依据Harris等人的NumPy综述。

## 用索引准确找到一个数、一行或一列

在Python和NumPy中，索引从0开始。本例样品A、B、C的行索引依次是0、1、2，五个时间的列索引依次是0到4。因此`h[1, 2]`表示第1号行与第2号列交会的元素，也就是日常计数中的第二行、第三列。它返回1.16。索引是地址，不是物理时间；`h[1, 20]`会要求读取第二十一列，并不会自动寻找20 min。

为什么经常把时间单独存为`time_min`？因为一列所对应的物理时间是数据解释的一部分，而不是厚度数值的一部分。本例的索引0、1、2、3、4对应0、10、20、40、60 min。后两个时间间隔更大，作图时应该把点放在真实时间位置，而不是简单等距排开。将索引与坐标分开，也有助于发现两个看似同样长度的数据集是否真正对应相同的时刻。

`h[1, :]`取出样品B的整行，冒号表示沿这一维保留全部元素，结果形状为`(5,)`。`h[:, 2]`则取出20 min的整列，形状为`(3,)`。它们都成为一维数组，却有完全不同的含义：前者是一个样品的时间变化，后者是一个时刻的样品分布。将两种结果分别画成曲线和并列散点，会比把它们都称作“一组数据”更容易避免误解。

单个整数索引通常会去掉相应维度，所以`h[1, :]`和`h[1:2, :]`的形状不同。前者选中一行后留下长度为5的一维数组，后者保留“从第1行开始、到第2行之前”的行区间，结果仍是形状`(1, 5)`的二维数组。两个结果包含相同的五个厚度值，但保留维度的方式不同。遇到后续运算的形状错误，先打印`shape`往往比反复修改函数名更有效。

写代码时可以把问题读出来，再翻译成索引：“我要20 min时三个样品的厚度”，对应先确定时间索引2，再写`h[:, 2]`。随后检查结果有三个数，单位仍为mm。这个小习惯同时检查了科学问题、地址和输出大小。数据变得更复杂后，也可以用明确的变量名保存选出的结果，而不在一长串表达式中反复猜测每一个数字索引的含义。

### 建立数组并沿两个方向求平均

time_min单独保存时间，h只保存同一种厚度数值。第一轴对应样品，第二轴对应时间；数组并不会自动记住这两种科学含义。

```
import numpy as np

time_min = np.array([0, 10, 20, 40, 60], dtype=float)
h = np.array([
    [1.00, 1.08, 1.14, 1.18, 1.20],
    [1.02, 1.09, 1.16, 1.21, 1.24],
    [0.98, 1.05, 1.11, 1.15, 1.18],
], dtype=np.float64)

print(h.shape, h.ndim, h.size)
print(h[1, 2])
print(h.mean(axis=0))
print(h.mean(axis=1))
print(h.std(axis=0, ddof=1))
```

## 沿哪条轴求平均，决定最后留下什么

“沿axis=0求平均”最容易让人困惑的地方，是把轴误读成图上的水平或竖直方向。更稳妥的理解方式是：这个操作将第0维的一组元素合并成一个结果，并保留其余维度。在形状`(3, 5)`中，第0维长度为3，代表样品。固定某个时间列，三个样品合成一个平均厚度；五个时间各做一次，最终留下五个数，形状为`(5,)`。

用20 min这一列手算一次最直观。三个厚度为1.14、1.16、1.11 mm，总和为3.41 mm，平均分给三个样品得到1.136666… mm。相加时单位相同，分母只是无量纲的样品计数，因此结果仍是厚度。写成带索引的公式，只是把“固定时间、遍历样品”这个过程表达得更明确，并没有增加新的物理假设。

$$
\bar{h}_{j}=\frac{1}{N}\sum_{i=0}^{N-1}h_{i,j}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | 第i个样品在第j个观测时刻的厚度，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样品索引，从0到N−1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 观测时刻的索引，无量纲；实际时间由time_min[j]给出。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 参与这一次平均的样品数，本例为3，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 求和运算，把指定索引范围内的厚度相加。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3356748dfad5e7f77344ed1d.svg) | 第j个时刻的样品平均厚度，单位mm；横线表示平均。 |

固定j，遍历样品索引i，先把同一时刻的厚度相加，再平均分给N个样品。20 min对应j=2，因此(1.14+1.16+1.11)/3=1.136666… mm。分母是三个样品，不是五个时刻。NumPy中的h.mean(axis=0)一次完成五个这样的计算。

改成`axis=1`，被合并的是长度为5的时间维。固定样品A，将它五个观测值相加并除以5，得到1.120 mm。对B、C同样计算，结果分别为1.144和1.094 mm。现在剩下的是三个样品，所以输出长度为3。一个简单的记忆办法是先把输入形状写出来，再划掉被归约的那一维：`(3, 5) → (5,)`或`(3, 5) → (3,)`。这里“归约”指把多个元素合并为较少元素的运算，求和、最大值和平均值都属于这一类。

$$
\bar{h}^{\mathrm{obs}}_{i}=\frac{1}{T}\sum_{j=0}^{T-1}h_{i,j}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | 样品i在观测j的厚度，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 固定的样品索引，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 在本式中变化的观测时刻索引，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 该样品的观测次数，本例为5；这里T是计数，不是温度，也不是持续时间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对列出的T次观测求和。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e88fa37eedbb9f408846d989.svg) | 样品i的观测平均厚度，单位mm；obs提示每个观测等权。 |

固定样品A，(1.00+1.08+1.14+1.18+1.20)/5=1.120 mm。这个平均回答五次观测的中心位置。10到20 min与40到60 min的间隔不同，如果问题是整个60 min过程中平均保持多厚，需要引入时间权重或积分。

时间轴上的平均还需要多问一句：每个观测应该有同样权重吗？本例在早期采得较密，后期采得较疏。把五个数等权平均，回答的是“这五次观测的平均厚度”；若想知道材料在整个60 min里平均保持多厚，就需要考虑每一段持续时间，并决定两次测量之间怎样近似变化。以后学习积分时，会用曲线下面积来处理这个问题。一个函数可以正确执行算术，但研究问题决定这种算术是否对应我们想求的量。

若不写`axis`，`h.mean()`把全部十五个数合为一个平均值，得到约1.119333 mm。这在描述整张表的数值中心时有用，却同时丢掉了时间与样品两种分组。还可以使用`keepdims=True`保留被合并维度的位置：`h.mean(axis=0, keepdims=True)`的形状是`(1, 5)`。保留那个长度为1的维度，会让后续“把每个样品减去对应时间的平均值”更容易与数组形状对应。

![按时间的均值与标准差曲线，以及按样品的观测平均条形图。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8857422f08421e825c301896.svg?v=8857422f0842)

图 3归约的方向决定结果回答的问题。左图沿axis=0汇总三个样品，保留五个时刻；误差条是每个时刻三个样品之间的样本标准差。右图沿axis=1汇总五个观测，保留样品身份。五个时刻间隔不等，因此右侧是观测值的等权平均，不是连续时间平均。

## 平均曲线之外，还要保留样品之间的差别

在60 min，三个样品的厚度为1.20、1.24和1.18 mm，平均为1.206667 mm。只画平均线时，看不出这个平均来自三个几乎相同的数，还是来自差异很大的数。把每个样品的曲线保留为较细的有色线，再叠加平均曲线，就能同时看见共同变化与个体差别。进一步可以在每个时刻计算样本标准差，用一个与厚度相同单位的数概括样品间的分散程度。

标准差的计算分成几个可理解的步骤。先将每个样品减去同一时刻的平均值，得到偏差；正偏差表示厚于平均，负偏差表示薄于平均。直接把偏差相加会互相抵消，因此先平方，再相加和平均，最后开平方恢复原单位。在用样本估计总体离散程度时，样本方差通常用`N−1`作分母，因为同一批数已经用于估计了一个平均值。NumPy用`ddof=1`表达这个分母选择，默认`ddof=0`则除以N。

$$
s_j=\sqrt{\frac{1}{N-1}\sum_{i=0}^{N-1}(h_{i,j}-\bar{h}_j)^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9141db84cefd44582dab98f5.svg) | 第j个时刻样品间的样本标准差，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/027ef905f53019bca46b31b7.svg) | 单个样品的厚度，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2a421271888a0b4d29592461.svg) | 同一时刻的样品平均厚度，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 分别为样品和时刻的索引，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 同一时刻参与统计的样品数，本例为3。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c66a41ccc40e7bbec2752d5.svg) | 估计样本方差时使用的分母；已用同一组数据估计一个平均值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cee6a0fff7f10651952de6b6.svg) | 平方使正负偏差都贡献非负量；最后开平方恢复mm单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 把N个样品的平方偏差相加。 |

在0 min，三值为1.00、1.02、0.98 mm，平均为1.00 mm。平方偏差之和为0+0.0004+0.0004=0.0008 mm²，除以2得到0.0004 mm²，开平方为0.020 mm。使用h.std(axis=0, ddof=1)。这个量描述三个样品的离散程度；它和均值估计的不确定性是两个统计问题。

这条误差条画的是三个样品之间的样本标准差。它描述数据的散布，不直接等于平均值的置信区间，也不等于仪器的测量误差。三者涉及不同问题：样品可能彼此不同，仪器可能读数不精确，而用少量样品估计总体平均又会带来抽样不确定性。图注应说清楚画的是哪一种量。后续统计章节会进一步解释标准误和置信区间；在这里，先把样品身份和每一个统计量的分母对准。

同一个样品在五个时刻出现，并不会因此变成五个独立制备的样品。样品A的初始厚度、制备条件和许多未观测特征，会同时影响它后续的观测。这个关系在数组中表现为一整行属于同一个对象。比较时间变化时保留每行身份，才能讨论样品内变化；把十五个数字当成十五个独立样品，会把实验结构改写成另一个问题。数组形状不能替代实验设计，但可以帮助我们把设计保留下来。

缺失值也会改变参与统计的数量。若B在20 min没有记录，`np.nan`可以标记那个位置；普通`mean`遇到它会把相应结果传播为缺失，`nanmean`则跳过缺失位置。选择后一种操作时，20 min的平均来自两个样品，而其他时刻仍来自三个，结果应同时附带计数。更换函数并不能恢复缺失观测，也不能解释为什么它缺失。交互实验会让这一差别同时出现在矩阵、曲线和统计结果中。

## 把计算、保存和图形连接成一次完整分析

下面的完整脚本把同一组数据经过几条互相对应的路径处理。数值部分计算两个方向的平均值和按时间的样本标准差；保存部分同时输出NumPy原生文件与简单CSV；绘图部分把这些数值组织成前面的图。每一张图都从同一数组生成，所以金色标记、热图格子、样品曲线和平均点对应同一个观测。改变原始表后重新运行，相关结果会一起更新。

`.npy`文件保存数组值以及形状、类型等信息，使用`np.load`读取后可以直接恢复本例数组。CSV是可以用文本编辑器查看的数字表，更方便与其他软件交换；本例用两位小数写出，并在读取时明确分隔符。原数据本来就只有两位小数，因此这次文本往返保留了所需数值。对于有更多有效位数的数据，需要选择合适的输出精度。文件格式也不自动保存样品名称、时间单位和实验含义，所以脚本另写`summary.json`说明这些信息。

程序中的两类检查各有用途。一个检查用Python逐列的`sum`与除法重新计算平均值，核对NumPy沿轴归约的结果；另一个检查保存后再读出的数组是否与输入一致。前者检查运算方向与数值，后者检查文件往返。它们都容易理解，而且失败时能指出具体环节。研究数据更大以后，这类小而明确的检查可以放在分析入口，帮助及时发现列顺序、单位转换或数据筛选中的变化。

完整脚本也包含Matplotlib绘图函数。此时可以先读`main`中的数据路径：创建数组、计算、检查、保存、生成图。再沿着`figures`函数观察每个数组怎样成为一组图形坐标。字体和配色由`style`控制，它们改变表达方式，不参与均值计算。把数值计算与显示设置分开，有利于以后修改图形时保持科学结果稳定，也方便分别检查数值与画面。

### 完整示例：计算、保存、读取并生成三组科学图

依赖NumPy与Matplotlib。main函数完成数值计算和数据往返检查，figures函数把同一批数值组织成数组结构图、轴归约对照和历史概念图；style只控制显示。

```
"""Represent repeated thickness measurements as an array and inspect both axes."""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches, font_manager

TIME = np.array([0, 10, 20, 40, 60], dtype=float)
SPECIMENS = ["A", "B", "C"]
THICKNESS = np.array([
    [1.00, 1.08, 1.14, 1.18, 1.20],
    [1.02, 1.09, 1.16, 1.21, 1.24],
    [0.98, 1.05, 1.11, 1.15, 1.18],
], dtype=np.float64)
COLORS = ["#28648a", "#b85336", "#467a62"]
INK = "#172b36"

def style():
    available = {font.name for font in font_manager.fontManager.ttflist}
    family = next((name for name in ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"] if name in available), "DejaVu Sans")
    plt.rcParams.update({"font.family": family, "font.size": 12, "axes.labelsize": 13,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "axes.edgecolor": INK, "axes.labelcolor": INK,
        "text.color": INK, "xtick.color": INK, "ytick.color": INK,
        "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6", "savefig.facecolor": "#fbfaf6",
        "svg.fonttype": "none", "pdf.fonttype": 42, "axes.unicode_minus": False})

def label(zh, en, language):
    return zh if language == "zh" else en

def save(fig, output, name, language):
    fig.savefig(output / f"{name}-{language}.svg", bbox_inches="tight", pad_inches=0.22)
    fig.savefig(output / f"{name}-{language}.png", dpi=170, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)

def figures(output, language, mean_time, mean_specimen, spread):
    t = lambda zh, en: label(zh, en, language)
    fig = plt.figure(figsize=(12.5, 6.8), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=[1.4, 1], height_ratios=[1, 0.27])
    ax = fig.add_subplot(grid[0, 0])
    im = ax.imshow(THICKNESS, cmap="cividis", vmin=0.95, vmax=1.25, aspect="auto")
    for i in range(3):
        for j in range(5):
            ax.text(j, i, f"{THICKNESS[i,j]:.2f}", ha="center", va="center", fontsize=16,
                    color="white" if THICKNESS[i,j] < 1.09 else INK)
    ax.add_patch(patches.Rectangle((1.5, .5), 1, 1, fill=False, lw=3.5, ec="#e4a321"))
    ax.set_xticks(range(5), [f"{int(v)}" for v in TIME]); ax.set_yticks(range(3), SPECIMENS)
    ax.set_xlabel(t("时间 / min（第1轴）", "Time / min (axis 1)")); ax.set_ylabel(t("样品（第0轴）", "Specimen (axis 0)"))
    ax.set_title(t("a  同一张表，两个索引", "a  One table, two indices"), loc="left", pad=16)
    cbar = fig.colorbar(im, ax=ax, shrink=.8, pad=.04)
    cbar.set_label(t("厚度 / mm", "Thickness / mm"))
    ax = fig.add_subplot(grid[0, 1])
    for i, color in enumerate(COLORS):
        ax.plot(TIME, THICKNESS[i], "o-", color=color, lw=2.2, ms=6, label=SPECIMENS[i])
    ax.scatter([20], [1.16], s=180, facecolor="none", edgecolor="#e4a321", lw=2.5, zorder=5)
    ax.annotate("h[1, 2] = 1.16 mm", xy=(20, 1.16), xytext=(25, 1.045),
                arrowprops={"arrowstyle":"->", "color": INK}, fontsize=12)
    ax.set(xlabel=t("时间 / min", "Time / min"), ylabel=t("厚度 / mm", "Thickness / mm"), ylim=(.95,1.27))
    ax.legend(title=t("样品", "Specimen"), frameon=False, ncol=3, loc="upper left")
    ax.set_title(t("b  行身份成为曲线身份", "b  Rows become individual curves"), loc="left", pad=16)
    ax = fig.add_subplot(grid[1, :]); ax.axis("off")
    lines = [t("shape = (3, 5)：3个样品 × 5个时刻", "shape = (3, 5): 3 specimens × 5 times"),
             t("ndim = 2：两个索引；size = 15：十五个数", "ndim = 2: two indices; size = 15: fifteen values"),
             t("教学构造数据；颜色与数字表示同一厚度。", "Constructed teaching data; color and number encode the same thickness.")]
    for y, text in zip([.82,.44,.06], lines): ax.text(.01,y,text,fontsize=13,transform=ax.transAxes)
    save(fig,output,"array-anatomy",language)

    fig = plt.figure(figsize=(12.5, 7.8), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=[1.45,1], height_ratios=[1,.8])
    ax = fig.add_subplot(grid[:, 0])
    for i, color in enumerate(COLORS): ax.plot(TIME, THICKNESS[i], "o-", color=color, lw=1.5, alpha=.75, label=SPECIMENS[i])
    ax.errorbar(TIME, mean_time, yerr=spread, fmt="D-", color=INK, lw=2.7, ms=6, capsize=5,
                label=t("均值 ± 样本标准差", "Mean ± sample SD"))
    ax.set(xlabel=t("时间 / min", "Time / min"), ylabel=t("厚度 / mm", "Thickness / mm"), ylim=(.94,1.28))
    ax.set_title(t("a  axis=0：每个时刻，汇总三个样品", "a  axis=0: combine specimens at each time"),loc="left",pad=16)
    ax.legend(frameon=False,loc="upper left",fontsize=11)
    ax.text(.04,.03,t("结果形状 (5,)；保留时间顺序", "Output shape (5,); time order is retained"),transform=ax.transAxes,fontsize=12)
    ax = fig.add_subplot(grid[0,1])
    ax.barh(SPECIMENS, mean_specimen, color=COLORS, height=.5)
    for i, value in enumerate(mean_specimen): ax.text(value+.015,i,f"{value:.3f}",va="center",fontsize=13)
    ax.set(xlabel=t("五个观测时刻的等权平均 / mm", "Equally weighted mean of five observations / mm"), xlim=(0,1.35))
    ax.invert_yaxis(); ax.set_title(t("b  axis=1：每个样品，汇总五个时刻", "b  axis=1: combine times within each specimen"),loc="left",pad=16)
    ax = fig.add_subplot(grid[1,1]); ax.axis("off")
    values=[t("留下什么？", "What remains?"),t("axis=0  →  时间，5个数", "axis=0  →  time, five values"),t("axis=1  →  样品，3个数", "axis=1  →  specimen, three values"),t("axis=None  →  全表，1个数", "axis=None  →  the whole table, one value"),t("时间间隔不等：行平均是观测平均。", "Unequal time gaps: row means average observations."),t("它与按持续时间加权的平均不同。", "A duration-weighted average answers another question.")]
    for y, text in zip([.92,.72,.54,.36,.14,.0], values): ax.text(.02,y,text,fontsize=12.5 if y<.9 else 14,weight="bold" if y>.9 else "normal")
    save(fig,output,"axis-reductions",language)

    fig, axes=plt.subplots(3,1,figsize=(12.5,7.8),gridspec_kw={"height_ratios":[1,.8,1]},layout="constrained")
    for ax in axes: ax.axis("off");ax.set_xlim(0,15);ax.set_ylim(0,1)
    ax=axes[0]
    ax.text(0,.97,t("a  一致的数据对象：数值 + 形状 + 类型", "a  One array object: values + shape + type"),weight="bold",fontsize=15)
    flat=THICKNESS.ravel()
    for k, value in enumerate(flat):
        ax.add_patch(patches.Rectangle((k+.03,.18),.92,.42,facecolor=COLORS[k//5],alpha=.17,edgecolor=COLORS[k//5]))
        ax.text(k+.49,.39,f"{value:.2f}",ha="center",va="center",fontsize=11)
    ax.text(.1,.03,t("连续存储示意；行优先排列", "Contiguous-storage schematic; row-major order"),fontsize=12)
    ax=axes[1]
    ax.text(0,.92,t("b  同一个计算规则，可以作用于整组数", "b  The same numerical rule acts on a group of values"),weight="bold",fontsize=15)
    ax.text(.25,.4,"(1.14 + 1.16 + 1.11) / 3",fontsize=20,color=INK)
    ax.annotate("",xy=(8.4,.45),xytext=(6.4,.45),arrowprops={"arrowstyle":"->","lw":2,"color":INK})
    ax.text(8.6,.4,"h.mean(axis=0)[2]",fontsize=20,color=COLORS[0])
    ax=axes[2]
    ax.text(0,.97,t("c  科学需求推动共同的数组接口", "c  Scientific needs motivate a common array interface"),weight="bold",fontsize=15)
    boxes=[(0,4.2,"Numeric",t("1990年代：Python中的数值数组", "1990s: numerical arrays in Python")),(5.1,4.2,"Numarray",t("大幅天文图像与灵活索引", "Large astronomical images and flexible indexing")),(10.2,4.6,"NumPy",t("2005：整合既有数组工作的方向", "2005: a shared direction for earlier array work"))]
    for x,w,name,description in boxes:
        ax.add_patch(patches.Rectangle((x,.15),w,.52,facecolor="#e8e6dc",edgecolor="none"))
        ax.text(x+.18,.48,name,fontsize=17,weight="bold")
        ax.text(x+.18,.27,description,fontsize=10.4)
    save(fig,output,"array-history",language)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="zh")
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True);style()
    mean_time=THICKNESS.mean(axis=0)
    mean_specimen=THICKNESS.mean(axis=1)
    spread=THICKNESS.std(axis=0,ddof=1)
    manual_columns=np.array([sum(THICKNESS[i,j] for i in range(3))/3 for j in range(5)])
    np.testing.assert_allclose(mean_time,manual_columns,rtol=0,atol=1e-14)
    np.save(args.output/"thickness.npy",THICKNESS)
    np.savetxt(args.output/"thickness.csv",THICKNESS,delimiter=",",fmt="%.2f")
    recovered=np.load(args.output/"thickness.npy")
    np.testing.assert_array_equal(recovered,THICKNESS)
    np.testing.assert_allclose(np.loadtxt(args.output/"thickness.csv",delimiter=","),THICKNESS,rtol=0,atol=1e-14)
    summary={"data_kind":"constructed teaching data","specimens":SPECIMENS,"time_min":TIME.tolist(),
             "thickness_mm":THICKNESS.tolist(),"shape":list(THICKNESS.shape),"ndim":THICKNESS.ndim,
             "size":THICKNESS.size,"dtype":str(THICKNESS.dtype),"nbytes":THICKNESS.nbytes,
             "mean_over_specimens_mm":mean_time.tolist(),"mean_over_observed_times_mm":mean_specimen.tolist(),
             "sample_sd_over_specimens_mm":spread.tolist(),"overall_mean_mm":float(THICKNESS.mean()),
             "npy_roundtrip_exact":bool(np.array_equal(recovered,THICKNESS))}
    (args.output/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    figures(args.output,args.language,mean_time,mean_specimen,spread)
    print(json.dumps({"shape":summary["shape"],"mean_over_specimens_mm":summary["mean_over_specimens_mm"]}))

if __name__=="__main__":main()
```

### 运行完整示例

在main.py所在目录运行。输出包括summary.json、thickness.npy、thickness.csv和对应语言的SVG/PNG图。两种语言使用相同数值。

```
python main.py --output output --language zh
python main.py --output output-en --language en
```

运行后可以先打开`summary.json`，对照输入形状`[3, 5]`和两个平均数组的长度；再查看CSV中的十五个数；最后看图中标记的1.16 mm是否仍位于样品B、20 min的位置。这样检查的顺序沿着数据含义逐步推进。文件存在只说明有内容写出，读回数值并把它对应到图上的具体位置，才能确认从数据到图形的链条正确。

## 改变一个观测，看它怎样影响整张图

下面的实验把数组、样品曲线与归约结果放在同一个界面中。先选择样品B和20 min，把这个观测增加0.06 mm。矩阵中只有一个格子的值改变，B曲线上只有一个点移动；沿`axis=0`求平均时，20 min的平均增加0.02 mm，因为改变量被三个样品分摊。切换到`axis=1`后，B的观测平均增加0.012 mm，因为这次分母是五个时刻。沿不同轴归约的含义，可以通过同一个改动直接比较。

再将这个观测设为缺失。图中会留下一个空格和曲线缺口，统计结果同时显示每组有效观测数。沿第0轴时，20 min这一列只剩A和C，平均为1.125 mm；沿第1轴时，B只剩四个观测，观测平均为1.140 mm。这个变化提醒我们，跳过缺失值既改变参与计算的数，也改变分母。比较不同时间或不同样品时，先看清各组实际用了哪些记录。

### 数组实验：一个观测，三种联动视图

选择一个格子，修改它或设为缺失；矩阵、样品曲线和归约结果使用同一组数。底图是构造的教学数据，厚度单位为 mm。

数值矩阵

[Figure: 数值矩阵](https://ml-biomat.com/tutorials/python-scientific/p07/#P07-matrix)

样品与平均曲线

[Figure: 样品与平均曲线](https://ml-biomat.com/tutorials/python-scientific/p07/#P07-curves)

归约结果与有效计数

[Figure: 归约结果与有效计数](https://ml-biomat.com/tutorials/python-scientific/p07/#P07-result)

矩阵边框、曲线圆圈和结果中的高亮来自同一格子。缺失观测按跳过缺失值计算；图中同时报告每组有效观测数。

还可以把误差加在初始时刻，而不是最后时刻，观察“总体变厚”这一印象是否受影响。这里的交互保持其他数字固定，专门隔离一个观测对结果的影响。正式实验中，误差可能同时影响一整批样品，也可能随时间漂移；那时需要为共同误差保存额外的批次或仪器标识。这正是为什么后续章节会引入带列名的表格，而不是要求所有科学信息都塞进一个没有标签的数组。

完成本章后，应当能够从一张小表出发，说明每条轴对应什么、一个索引找到什么、某个归约留下什么，以及统计量用了多少个样品。下一次遇到图像、坐标或多批测量，可以先画出这些维度，再决定数组的形状。先把表示想清楚，后面的切片、广播、拟合和可视化就会成为同一条分析路线上的自然步骤。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

   数组、形状、类型、索引与保存的开放入门教程。

   NumPy code and documentation: BSD-3-Clause; teaching narrative and figures here are independently written.
2. [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)

   axis与keepdims参数的定义。

   BSD-3-Clause documentation.
3. [numpy.std](https://numpy.org/doc/stable/reference/generated/numpy.std.html)

   标准差与ddof参数。

   BSD-3-Clause documentation.
4. [Harris et al. — Array programming with NumPy (2020)](https://doi.org/10.1038/s41586-020-2649-2)

   数组编程及Numeric、Numarray与NumPy的发展背景。

   Scientific attribution; original concept figures, no publisher artwork reproduced.
