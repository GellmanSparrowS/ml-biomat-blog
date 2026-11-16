# 切片与广播：沿正确的方向计算

Source: https://ml-biomat.com/tutorials/python-scientific/p08/
Language: zh-CN

选中观测、配对基准、校正漂移，并追踪视图与原始数据的联系。

## 让每一个数都和正确的参照量配对

三块试样在液体中逐渐变厚，怎样判断哪一块变化更大？直接比较最后的厚度，会把初始尺寸差异也算进去。更合适的问题是：每块试样相对于自己的初始厚度增加了多少。如果仪器在测量过程中还发生了零点漂移，就要先按时间扣除对应偏差。本章用同一张三行五列的数组完成这些操作，把切片、条件筛选和广播放进一个连续的测量问题中。读完后，你应当能够说明程序拿了哪些数、这些数怎样配对，以及改动一个切片会不会影响原始数据。

沿用上一章的构造厚度记录：三行分别代表A、B、C，五列对应0、10、20、40和60 min，厚度单位为mm。A从1.00变为1.20，B从1.02变为1.24，C从0.98变为1.18。这些数字用于手算与数组操作教学。虽然表格外观整齐，时间间隔却不是等长的；数组下标只表示存放位置，真正的时间需要从配套的时间数组读取。把这两种坐标区分开，是后面正确筛选与绘图的起点。

可以把数组想成带行列坐标的实验记录柜：行告诉我们是哪块试样，列告诉我们何时测量。拿出某些格子叫选择，让每行找到自己的初始格子叫配对，把同一规则应用到全部格子叫数组运算。这些操作不会自动理解A是试样、10是分钟。我们要把测量含义翻译成形状与索引，再用已知的数值关系检查翻译是否正确。一个没有报错的表达式，仍然需要回答这个配对问题。

## 切片选择的是位置，时间仍由坐标给出

`h[1, 2]`的第一个索引1指向第0轴上编号为1的B试样，第二个索引2指向第1轴上编号为2的时间列，得到20 min的1.16 mm。这里下标从0开始，书写顺序与`shape=(3,5)`一致。用一个整数选定某条轴时，这条轴不再出现在结果形状里：`h[1]`是一维的五个数，而`h[1:2]`仍是一行五列的二维数组。两者包含相同厚度，却保留了不同的结构信息。

`h[:, 1:4]`中的冒号表示保留全部试样，`1:4`表示选择位置1、2、3，停止位置4不包括在内。因此结果对应10、20、40 min，共三列，形状是(3,3)。这种右端不包含的规则，使相邻区间可以自然接起来：`0:2`与`2:5`既没有重复位置，也没有漏掉位置。步长写在第二个冒号之后，例如`h[:, ::2]`取第0、2、4列；它得到0、20、60 min，而不是等时间间隔的采样。

按物理时间选区间时，先在时间数组上表达条件更清楚。`(time >= 10) & (time <= 40)`生成五个真假值，分别回答每个时间是否位于区间内。把这个布尔数组放在列的位置，`h[:, selected]`便保留同一组时间列。括号把两个比较各自组成一个整体，`&`再逐位置组合结果。Python的`and`用于判断整体条件，不适合直接代替这里逐元素的布尔运算。

筛选厚度后，也要用同一选择处理时间坐标。若图里画的是三列厚度，横坐标就应当是三个对应时间；把五个旧时间或重新编号的0、1、2当作分钟，都会改变图的含义。类似地，重新排列样品行时，样品名称也要一起排列。NumPy保存的是位置关系，名称与单位需要我们同步维护。等到带标签的表格和多维数据章节，这种同步关系会由更专门的数据结构帮助表达。

![同一组厚度记录的完整表、基准列和时间窗口；热图列宽相同，标签给出实际分钟。](https://ml-biomat.com/static/tutorials/python-scientific/figures/d0730e8aa613e86d926d47f1.svg?v=d0730e8aa613)

图 1同一组厚度记录的完整表、基准列和时间窗口；热图列宽相同，标签给出实际分钟。

负下标从末端定位，`h[:,-1]`因此表示三块试样各自最后一次测量，结果形状为(3,)。这里“最后”指数组排列的末端，只有时间已经按顺序排列时才等于最晚时刻。若记录经过重排，先核对时间数组再使用末列。切片也可能合法地得到空数组，例如起点已经超过有效范围；空选择表示没有观测满足这次选择，并不意味着厚度为零。后续求均值前，应先查看选择后的元素数，判断是否还有可以计算的对象。

## 选择几块试样，与选择若干个观测值

条件的形状决定了筛选的对象。先计算各试样在最后时刻的相对变化，再与21%比较，会得到长度为3的布尔数组，表示三块试样是否满足条件。把它放在行索引位置，就选中完整试样记录。本例只有B在60 min达到约21.57%，因此结果保留B的一整行。选择依据是最后时刻，保留下来的却是该试样的全部时间轨迹，这个区别在研究“哪些样品符合某种响应”时很有用。

若直接写`h > 1.15`，得到的条件与h一样是三行五列，分别检查十五个观测值。再写`h[h > 1.15]`，结果是一维的符合条件数值集合，原来的行列排列不再保留。这样的集合适合检查数值范围，却不能直接当作某一条时间曲线。要继续追踪它们来自哪里，可以用`np.nonzero`取得行、列位置，再查对应试样名称与时间；需要保留完整矩形结构时，则可以把不合条件的位置标记出来，而不立即压成一维。

整数索引数组还允许按指定顺序挑选，例如`h[[2,0]]`得到C、A两行。这里的双层方括号有明确分工：内层列表描述要取的位置，外层方括号把这个选择交给数组。与连续切片相比，这种高级索引能够重排或重复元素，因此其结果拥有独立的数据存储。后面会用实际修改说明这一点。眼下先记住选择所需的科学身份，再检查输出形状是否仍表达那种身份。

筛选条件本身也属于分析定义。21%是本例用来辨别数组选择行为的阈值，不能自动变成所有材料的性能要求。实际实验中的阈值应当来自任务目标或测量约定。显示到小数点后两位的数字，也可能掩盖阈值附近的微小差异；计算时采用明确的原始数值比较规则，展示时再决定保留位数，能避免把四舍五入后的外观当成真实比较结果。

还可以把两种选择按顺序组合：先根据终点响应挑选样品，再从这些样品中取某个时间区间。为了保持初始参照，通常先在完整时间表上计算相对变化，再筛选需要显示的时间窗口。若先把起点那一列切掉，再把剩余窗口的第一列当作初始厚度，研究问题就变成相对于窗口起点的变化。两种计算都可以有用途，但必须明确起点。这个例子说明，索引操作的先后顺序不仅影响程序形状，也可能改变科学比较的参照。

## 一列基准怎样服务于整张表

相对厚度变化先用当前厚度除以初始厚度，再减去1。除法把同单位的长度化成无量纲比例，减1把“初始值为一倍”移到零变化的位置。B在20 min的厚度为1.16 mm，初始为1.02 mm，所以相对变化是1.16÷1.02−1，约0.137255，写成百分数为13.73%。它回答厚度相对于起点增加的比例；这里没有把厚度变化进一步解释成体积变化，因为那还需要其他方向的尺寸或形变关系。

$$
\varepsilon_{ij}=\frac{h_{ij}}{h_{i0}}-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e1dffe683e6706f37bf2ad55.svg) | 样品i在时刻j的相对厚度变化，无量纲；乘100后表示为百分数 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 样品与时间位置索引，无量纲；i=0,1,2，j=0,…,4 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dbf6e5f545cd01f55d42bc3.svg) | 对应厚度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3abf426a48c1d4f6a951f9ce.svg) | 同一样品初始厚度，mm，必须为正 |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | 初始厚度与自身之比，无量纲 |

分子与分母同为长度，单位相消。B在20 min为1.16/1.02−1=0.1372549，约13.73%；初始时刻厚度除以自身再减1得到0。

把初始厚度写成`baseline = h[:, 0:1]`，结果是一列三个数，形状(3,1)。计算`h / baseline - 1`时，NumPy把这列基准沿时间方向配给同一行的各个观测：A一行都除以1.00，B一行都除以1.02，C一行都除以0.98。这叫广播。可以把它想成每行旁边固定放着一把自己的标尺，沿着这一行测量时始终使用那把标尺。

广播判断从形状的最右端开始。两个维度大小相等，可以一一配对；其中一个大小为1，可以让这个位置提供同一值给另一边。对(3,5)与(3,1)，先比较5与1，满足后一种情况；再比较3与3，满足前一种情况，结果仍是(3,5)。这种规则只检查数组结构，不检查单位，也不猜测哪一条轴表示样品。与其记住“列向量除表格”，不如把每个维度代表什么写在形状旁边。

`h[:,0]`则得到形状(3,)，其中没有显式的时间维度。把它与(3,5)从右端对齐时，3会遇到5，因而报形状不匹配。用`h[:,0,None]`或`h[:,0][:,None]`插入长度为1的新轴，也能得到(3,1)；`None`在这种索引位置是插入轴的写法，与数据记录中用None表示缺失的语境不同。初学时采用`0:1`保留基准列，通常最容易看清原来的测量结构。

广播可以避免把小数组事先复制成许多份，但完整计算结果通常仍需要存储。本例结果只有十五个数，成本很小；若不小心把两个大型轴组合成所有可能的配对，结果可能比任一输入都大得多。执行前估算结果形状，比只观察输入文件大小更有帮助。每个float64数占8字节，结果元素总数乘8可以给出数值缓冲区的基本大小，再考虑程序同时保留的其他数组。

把一维数组转置也不会自动变成列数组：形状(3,)的对象只有一条轴，`baseline.T`仍然是(3,)。二维(1,3)转置后才会得到(3,1)。这个细节经常出现在把纸上的“横着写的三个数”翻译成代码时；纸面方向是排版，数组维度是实际结构。需要给每个样品一个基准，就明确保留样品轴与长度为1的时间轴。需要给每个时间一个校正值，就明确保留长度为1的样品轴与时间轴，不依赖文本打印出来的朝向判断。

## 校正量沿时间走，基准量沿样品走

现在给测量增加一个明确的教学条件：独立校准记录表明，仪器在五个时刻分别多读了0、0.01、0.02、0.03、0.04 mm，同一时刻对三块试样的影响相同。这是一组给定的校准偏差，不是从厚度增长曲线里猜出来的趋势。要恢复校正后的厚度，就按列减去对应偏差。写成`h - drift[None,:]`，偏差形状是(1,5)，时间位置一一对应，样品方向允许复用。

$$
h^{\mathrm{corr}}_{ij}=h_{ij}-d_j,\qquad \varepsilon^{\mathrm{corr}}_{ij}=\frac{h^{\mathrm{corr}}_{ij}}{h^{\mathrm{corr}}_{i0}}-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcb192a1662d80f082b86f72.svg) | 校正后的厚度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/8dbf6e5f545cd01f55d42bc3.svg) | 仪器厚度读数，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa5d90d675f75ab6ffeebf3.svg) | 时刻j的已知多读偏差，mm；本例对所有样品相同 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 样品与时间位置，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/d13ee63029543cfd8b898aca.svg) | 校正后的初始厚度，mm，必须为正 |
| ![Formula](https://ml-biomat.com/static/agent-math/c9e06ef0b2ebc976afe19222.svg) | 校正后的相对厚度变化，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | 归一化起点，无量纲 |

B在20 min的读数1.16 mm减去0.02 mm得到1.14 mm；起点偏差为零，故1.14/1.02−1=0.1176471，约11.76%。

校正后再用每块试样校正后的起点归一化，能够保持计算定义一致。这里起点偏差恰好为零，所以初始厚度不变；若起点也有偏差，分母同样要使用校正值。60 min时，A由1.20校正到1.16 mm，相对变化16%；B由1.24校正到1.20 mm，相对变化约17.65%；C由1.18校正到1.14 mm，相对变化约16.33%。图中虚线与实线的间距由已知偏差产生，不能通过“曲线看起来更顺”来决定是否校正。

![上方比较给定漂移校正前后的变化；下方展示三个样品与三个时间恰好同长度时，错误广播如何通过形状检查。](https://ml-biomat.com/static/tutorials/python-scientific/figures/395ffe089128323e7b7aaec5.svg?v=395ffe089128)

图 2上方比较给定漂移校正前后的变化；下方展示三个样品与三个时间恰好同长度时，错误广播如何通过形状检查。

形状检查还可能遇到更隐蔽的情况：只保留前三列后，厚度表变成(3,3)。这时把形状(3,)的初始厚度直接拿来除，程序能够执行，因为最右端的三个位置恰好相等。但它会把1.00、1.02、0.98分别配给三个时间列，A在20 min就会错误地除以C的初始厚度。图下方把正确与错误结果并排显示：正确结果在第一列全部为0，错误结果却让B、C的起点变成2%和−2%，这条物理关系立即暴露了配对错误。

因此，好的检查应当同时查看形状、单位和少量可以解释的单元格。本例至少核对B在20 min的13.73%，以及每行起点的零变化。再把全表改成只有三列，确认代码仍然按样品归一化。这种主动改变数组尺寸的检查，能够发现被相同轴长度掩盖的问题。后续处理图像、光谱或三维轨迹时，轴数更多，逐轴写出含义会更加有用。

校准偏差还涉及符号约定。本例说仪器“多读”0.02 mm，所以从读数中减去0.02 mm；如果给出的字段直接叫“应加的校正量”，相同物理情况可能记录为−0.02 mm，并通过加法使用。输入名称、单位和公式要共同表达约定。偏差是否对所有样品相同，也需要校准条件支持；若每个测量通道有不同偏差，就应使用相应通道的数据结构，不能只因为一行数组方便广播，就让所有通道采用同一数值。

## 从数组的历史设计理解视图与副本

数组计算的一个长期需求，是在大量数据上改变观察方式，而不必每次重新搬动全部数值。NumPy作者在2020年的回顾中把多维数组及其操作作为科学Python的重要基础来说明。对本章尤其有用的设计，是把实际存放数值的缓冲区，与描述形状、类型和访问步长的信息分开。这样，同一批数据可以有不同的切片或排列入口，操作仍能通过这些信息找到需要的数。

这种设计有具体的研究背景。NumPy之前，Numeric已经为Python提供数组；后来，为了处理哈勃空间望远镜的大型天文图像，Numarray发展了更灵活的索引、内存映射等能力。2005年出现的NumPy汇合了两者的长处。面对图像中的一小块区域，研究者希望直接定位已有像素，同时又能在需要时建立独立处理结果。本章十五个数的例子，把大图像里同样重要的访问与存储关系缩小到可以逐格查看的尺度。

![原创缓冲区图解：彩色位置属于同一数据，切片保留原40字节行步长，副本采用独立的24字节行步长。](https://ml-biomat.com/static/tutorials/python-scientific/figures/d657803b37262a259f707a4c.svg?v=d657803b3726)

图 3原创缓冲区图解：彩色位置属于同一数据，切片保留原40字节行步长，副本采用独立的24字节行步长。

本例连续存放十五个float64数，每个占8字节，一行五个数占40字节。在同一行走到下一列，存储位置前进8字节；走到下一行的对应列，前进40字节。切片`h[:,1:4]`从第1列开始，起点相对原缓冲区偏移8字节，形状变为(3,3)，但跨行仍要前进40字节，因为原表每行还有未被选中的两列。这组跨轴距离叫步长，单位是字节，与时间数组里的分钟间隔是两个概念。

$$
o_{ij}=i\,s_0+j\,s_1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8180a7e0eb6f9b4d3cc44dc.svg) | 相对本数组起点的字节偏移，字节 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 从0开始的行、列位置，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/c2e6885af79283f639bc340b.svg) | 沿第0与第1轴前进一步的字节步长，字节 |

本例连续float64数组的步长为(40,8)字节，B在20 min的位置(1,2)偏移1×40+2×8=56字节。切片起点另向后偏移8字节，但其内部步长仍为(40,8)。

基本切片得到的数组共享原来的数值存储，叫视图。可以把视图理解成放在同一张底稿上的取景框：取景框里的格子仍属于那张底稿，修改它就会改到底稿。程序在一份用于演示的数组上取出视图，再把视图第一个值改为9.0，原数组A在10 min的位置也变成9.0。这个夸张的数专门用于让存储关系明显可见，后面的科学计算仍然使用未改动的厚度表。

显式调用`.copy()`会创建独立数值存储，修改副本不影响原数组。高级索引提取出的结果同样独立；但`h[:, selected] = values`是直接给原数组选定位置赋值，仍会改变原数组，不能把“高级索引读出副本”误解成“高级索引永远不能修改原值”。用`np.shares_memory`检查两个数组是否共享存储，比仅仅看变量名是否不同更可靠。选择视图还是副本，应当对应你希望共享修改还是独立处理的实际目的。

这个区别在探索性分析中很实用：只观察一小段数据时，视图能直接呈现原表；尝试某种校正且希望保留源记录时，先显式复制，再给副本起一个表明用途的名字。反过来，如果目标就是更新一份工作数组，直接按索引赋值能够清楚地表达修改位置。决定的核心是哪些数值应当共同变化、哪些需要各自保存，而不是要求每次选择都复制。复制还会使这块独立数据连续排列，所以本例三列副本跨行只需24字节，原切片视图仍跨40字节。

## 完整程序把配对规则变成可检查的输出

下面的程序从固定厚度表出发，依次完成时间筛选、每个样品的起点归一化、时间漂移校正、21%阈值选样，以及视图和副本的修改演示。它还故意执行一次(3,5)与(3,)的不兼容运算并保存实际错误消息，再构造(3,3)的可执行错误配对。两种错误放在同一个程序中，便于比较解释器能发现的问题与必须依靠测量定义才能发现的问题。

### 完整程序：时间选择、校正、广播与共享内存

输出三幅图和summary.json，实际捕获形状错误并独立核对逐元素结果。

```
"""Select, calibrate, and normalize a constructed specimen-by-time array."""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch

TIME=np.array([0,10,20,40,60],dtype=float)
H=np.array([[1,1.08,1.14,1.18,1.2],[1.02,1.09,1.16,1.21,1.24],[.98,1.05,1.11,1.15,1.18]],dtype=np.float64)
DRIFT=np.array([0,.01,.02,.03,.04])
NAMES=['A','B','C'];COLORS=['#28648a','#b85336','#467a62']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('output'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    baseline=H[:,0:1]
    strain=H/baseline-1
    corrected=H-DRIFT[None,:]
    corrected_strain=corrected/corrected[:,0:1]-1
    selected=(TIME>=10)&(TIME<=40)
    selected_values=H[:,selected]
    qualifying=strain[:,-1]>=.21
    square=H[:,:3];wrong_square=square/H[:,0]-1;correct_square=square/baseline-1
    shared=H.copy();view=shared[:,1:4];isolated=shared[:,1:4].copy();advanced=shared[:,[1,2,3]]
    view[0,0]=9.0
    assert shared[0,1]==9 and isolated[0,0]==1.08 and advanced[0,0]==1.08
    independent=np.array([[float(H[i,j])/float(H[i,0])-1 for j in range(5)] for i in range(3)])
    assert np.allclose(strain,independent)
    assert np.allclose(corrected,[[float(H[i,j])-float(DRIFT[j]) for j in range(5)] for i in range(3)])
    assert qualifying.tolist()==[False,True,False]
    assert np.shares_memory(view,shared) and not np.shares_memory(isolated,shared) and not np.shares_memory(advanced,shared)
    try:H/H[:,0]
    except ValueError as error:incompatible=str(error)
    else:raise AssertionError('Shapes (3,5) and (3,) should be incompatible')
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={x.name for x in font_manager.fontManager.ttflist};family=next((x for x in ['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'] if x in available),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=170,bbox_inches='tight');plt.close(fig)
    def grid(ax,data,title,cols,unit):
        im=ax.imshow(data,cmap='cividis',vmin=H.min(),vmax=H.max(),aspect='auto')
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):ax.text(j,i,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=15,color='white' if data[i,j]<1.1 else '#172b36')
        ax.set(xticks=range(data.shape[1]),xticklabels=cols,yticks=range(3),yticklabels=NAMES,xlabel=unit,title=title)
        return im
    fig=plt.figure(figsize=(12.5,7.7),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,.9],width_ratios=[1.5,1]);ax=fig.add_subplot(gs[0,0]);im=grid(ax,H,tr('a  原数组 h：(3,5)','a  Original h: (3,5)'),TIME.astype(int),tr('时间 / min','Time / min'))
    ax.add_patch(Rectangle((.5,-.5),3,3,fill=False,edgecolor='#c6623b',lw=3));fig.colorbar(im,ax=ax,pad=.02).set_label(tr('厚度 / mm','Thickness / mm'))
    ax=fig.add_subplot(gs[0,1]);grid(ax,baseline,tr('b  每个样品的基准：(3,1)','b  Baseline per specimen: (3,1)'),[0],tr('时间 / min','Time / min'))
    ax=fig.add_subplot(gs[1,0]);grid(ax,selected_values,tr('c  h[:, 1:4] 对应10、20、40 min','c  h[:, 1:4] selects 10, 20, 40 min'),TIME[selected].astype(int),tr('时间 / min','Time / min'))
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.text(0,.9,'(3, 5) / (3, 1) → (3, 5)',fontsize=19,weight='bold');ax.text(0,.65,tr('末轴：5 与 1，可广播','Last axis: 5 and 1 are compatible'),fontsize=14);ax.text(0,.43,tr('前轴：3 与 3，一一配对','First axis: 3 and 3 match'),fontsize=14);ax.text(0,.15,tr('B，20 min：1.16 / 1.02 − 1 = 0.137255','B, 20 min: 1.16 / 1.02 − 1 = 0.137255'),fontsize=13)
    save(fig,'selection-broadcast')

    fig=plt.figure(figsize=(12.5,8.1),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.4,1]);ax=fig.add_subplot(gs[0,:])
    for i,c in enumerate(COLORS):
        ax.plot(TIME,strain[i]*100,'o-',color=c,lw=2,label=f'{NAMES[i]} '+tr('原始','raw'))
        ax.plot(TIME,corrected_strain[i]*100,'s--',color=c,lw=1.8,ms=5,label=f'{NAMES[i]} '+tr('校正后','corrected'))
    ax.set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('相对厚度变化 / %','Relative thickness change / %'),title=tr('a  各样品用自己的初始厚度归一化','a  Normalize each specimen by its own initial thickness'));ax.legend(ncol=3,fontsize=11);ax.grid(alpha=.15)
    for k,(data,title) in enumerate([(correct_square,tr('b  (3,3) / (3,1)：按样品','b  (3,3) / (3,1): by specimen')),(wrong_square,tr('c  (3,3) / (3,)：误按时间列','c  (3,3) / (3,): wrong time columns'))]):
        ax=fig.add_subplot(gs[1,k]);im=ax.imshow(data*100,cmap='RdBu_r',vmin=-3,vmax=18,aspect='auto')
        for i in range(3):
            for j in range(3):ax.text(j,i,f'{100*data[i,j]:.2f}%',ha='center',va='center',fontsize=14,color='white' if data[i,j]>.13 else '#172b36')
        ax.set(xticks=range(3),xticklabels=[0,10,20],yticks=range(3),yticklabels=NAMES,xlabel=tr('时间 / min','Time / min'),title=title)
    fig.colorbar(im,ax=fig.axes[1:3],shrink=.8,pad=.02).set_label(tr('相对变化 / %','Relative change / %'));save(fig,'normalized-response')

    fig=plt.figure(figsize=(12.5,8.3),layout='constrained');gs=fig.add_gridspec(3,1,height_ratios=[.3,.8,1.3]);ax=fig.add_subplot(gs[0]);ax.axis('off');ax.text(0,.7,tr('数组思想：一个数值缓冲区，多种访问方式','Array programming: one numerical buffer, multiple access patterns'),fontsize=18,weight='bold');ax.text(0,.05,tr('NumPy作者2020年回顾的核心结构：数值数据与形状、类型、步长分开组织。','Core structure in the authors’ 2020 retrospective: values plus shape, dtype, and strides.'),fontsize=12)
    ax=fig.add_subplot(gs[1]);ax.axis('off');ax.set_xlim(-.7,15.3);ax.set_ylim(-.4,2.8)
    for k,v in enumerate(H.ravel()):
        selected_cell=k%5 in [1,2,3];ax.add_patch(Rectangle((k,1),.94,.9,facecolor=COLORS[k//5],alpha=.25 if selected_cell else .08,edgecolor=COLORS[k//5]));ax.text(k+.47,1.45,f'{v:.2f}',ha='center',va='center',fontsize=11);ax.text(k+.47,.5,str(k*8),ha='center',fontsize=10)
    ax.text(0,2.35,tr('写入前的连续float64缓冲区：3 × 5 × 8 = 120字节','Before editing — contiguous float64 buffer: 3 × 5 × 8 = 120 bytes'),fontsize=14);ax.text(0,-.1,tr('数字下方：相对起点的字节偏移；每个数占8字节','Below: byte offsets from the buffer start; each value uses 8 bytes'),fontsize=12)
    ax=fig.add_subplot(gs[2]);ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,5.5)
    for x,title,data,stride,c in [(0,tr('视图写入9.0：原表同格一起改变','Write 9.0 through view: source changes'),view,40,COLORS[0]),(6.2,tr('提前复制的数据：仍然保留1.08','Earlier copy: still retains 1.08'),isolated,24,COLORS[2])]:
        ax.text(x+.05,5.05,title,fontsize=14,weight='bold');ax.text(x+.05,4.45,f'shape = (3,3); strides = ({stride},8) bytes',fontsize=12)
        for i in range(3):
            for j in range(3):
                px=x+.2+j*1.7;py=3.1-i*.85;changed=x==0 and i==0 and j==0;ax.add_patch(Rectangle((px,py),1.55,.7,facecolor=COLORS[1] if changed else c,alpha=.22 if changed else .08));ax.text(px+.775,py+.35,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=15,color=COLORS[1] if changed else '#172b36')
        ax.text(x+.05,.35,tr('共享存储；从原缓冲区偏移8字节','Shared storage; start offset 8 bytes') if x==0 else tr('独立存储：3 × 3 × 8 = 72字节','Independent storage: 3 × 3 × 8 = 72 bytes'),fontsize=12)
    save(fig,'memory-history')
    summary={'dataset':'Constructed specimen thickness table','shape':list(H.shape),'selected_times_min':TIME[selected].tolist(),'selected_values_mm':selected_values.tolist(),'baseline_shape':list(baseline.shape),'strain':strain.tolist(),'corrected_strain':corrected_strain.tolist(),'qualifying_at_21_percent':[NAMES[i] for i in np.flatnonzero(qualifying)],'wrong_square_strain':wrong_square.tolist(),'correct_square_strain':correct_square.tolist(),'incompatible_shape_error':incompatible,'view_copy':{'view_shares_memory':bool(np.shares_memory(view,shared)),'copy_shares_memory':bool(np.shares_memory(isolated,shared)),'advanced_shares_memory':bool(np.shares_memory(advanced,shared)),'edited_original_value':float(shared[0,1]),'isolated_value':float(isolated[0,0]),'original_strides_bytes':list(H.strides),'view_strides_bytes':list(view.strides),'copy_strides_bytes':list(isolated.strides)}}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'selected_times_min':summary['selected_times_min'],'last_raw_percent':(strain[:,-1]*100).tolist(),'last_corrected_percent':(corrected_strain[:,-1]*100).tolist(),'view_copy':summary['view_copy']},indent=2))

if __name__=='__main__':main()
```

数值摘要保留选中时间10、20、40 min，三块试样完整的相对变化数组，以及内存共享检查。原始终点变化约为20.00%、21.57%、20.41%，校正后约为16.00%、17.65%、16.33%。程序另外用普通Python双重循环逐项执行同样的数值定义，与数组结果比较。这个循环刻意写得直白：外层确定试样，内层确定时间，每次都能指出分母来自哪一行。

阅读绘图部分时，留意热图的格子编号与时间曲线的横坐标采用不同布局。热图为方便阅读，把每一列画成相同宽度，并在列标签写出实际时间；曲线则按0、10、20、40、60的真实数值放置横坐标。两种图都表达同一批数据，却服务于不同问题：前者让人检查索引与配对，后者让人观察变化随时间如何展开。不能从热图格子的间距推断采样间隔。

## 改变选择、校正与写入方式，追踪同一个格子

交互实验把原始表、所选窗口和相对变化曲线连接起来。选择起止列时，界面同时显示位置与分钟，帮助区分索引和物理坐标；调整校准偏差强度时，三个样品在同一时刻一起变化；切换视图与副本后，再修改所选区域中的一个值，观察原始表是否跟随变化。这里每次调整都从固定教学表重建状态，所以重置能够回到完整的初始记录。归一化始终读取源数组的初始列；若通过视图修改的正是这一列，基准也随之更新。

### 实验：追踪一个切片里的改动

起止位置均包含在选择中。增量加到所选样品的窗口第一个值；视图修改源表，副本保留源表。蓝、橙、绿依次表示A、B、C。

[Figure: 源表与选中窗口](https://ml-biomat.com/tutorials/python-scientific/p08/#P08-grid)

[Figure: 相对变化随时间的曲线](https://ml-biomat.com/tutorials/python-scientific/p08/#P08-plot)

先只选10到40 min，确认得到三列而不是四列；再打开漂移校正，查看B在20 min的变化从13.73%降到11.76%。最后把选中区域的第一个值增加0.10 mm，比较视图模式与副本模式的原表。三个操作分别检验位置选择、方向配对和数据共享。掌握这些关系以后，数组代码的简短表达就有了可以逐格解释的含义，下一章再利用大量重复抽样观察测量结果怎样波动。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NumPy — Indexing on ndarrays](https://numpy.org/doc/2.4/user/basics.indexing.html)

   索引、选择形状和赋值规则

   BSD-3-Clause
2. [NumPy — Broadcasting](https://numpy.org/doc/2.4/user/basics.broadcasting.html)

   从末轴检查配对及结果大小

   BSD-3-Clause
3. [NumPy — Copies and views](https://numpy.org/doc/2.4/user/basics.copies.html)

   共享存储与独立数据

   BSD-3-Clause
4. [Harris et al. — Array Programming with NumPy (2020)](https://arxiv.org/html/2006.10256v1)

   数组编程史与数据/元信息结构，配原创教学图

   CC BY 4.0 article; no original artwork reproduced
