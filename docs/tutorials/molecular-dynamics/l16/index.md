# 完整研究：交联、网络结构与力学

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l16/
Language: zh-CN

把连接、链形状、加载与统计连成一个完整研究：同一批网络，逐项追踪结构如何对应机械响应。

## 把一块网络材料的结构与受力连起来

一块凝胶拿在手里是连续的，放大到分子尺度却是许多链、连接与周围介质组成的复杂体系。研究它为什么软、为什么能回弹，通常需要同时回答几个问题：哪些链被连在一起，连接以后链呈现怎样的形状，外部拉伸怎样传到分子，以及保持形变以后内部还会如何调整。单独一幅结构图或一条应力曲线只能照亮其中一部分。本讲把这些观察放在同一个研究案例里，让每个结构指标都能找到属于它自己的模拟与机械读数。

我们采用一个组成清楚的短链网络：八十条原始链，每条二十个等质量珠子，共一千六百个珠子。链上相邻珠子有有限伸长弹簧，非键接近通过排斥作用处理。在相同熔体上增加零、八十或一百六十条跨链连接，再让各分支静置、拉伸和保持。三套独立制备各包含这三个分支，形成九个条件。这个材料没有显式溶剂，也没有断键反应，所以它把注意力集中在永久连接、链的几何与热运动如何共同参与一次规定的加载过程。

这项完整练习的中心问题可以写成一句话：在相同准备规则、温度与定体积加载历程下，增加连接怎样改变网络连通性和原链形状，以及这些变化与有限时间机械响应怎样对应？句子里的每个条件都很有用。相同规则使比较有共同起点，温度规定热运动的尺度，加载历程规定形变速度与等待时间，有限时间则说明读数来自哪段实际观察。接下来所有图与代码都围绕这个问题组织，读者可以沿着输入、结构和时间记录逐步检查它。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s1)

图 1 · 凝胶化研究关注连接怎样形成大分子团，珠簧动力学关注链怎样排列与运动；网络力学把这些观察联系起来。

这里“完整”意味着各环节相互对应：建立模型时保存连接身份，运行时保存足够重建形状和应力的记录，分析时使用同一制备编号与连接数，作图时保留所有九个条件。它不要求一开始就使用最大的体系或最长轨迹。先让一个可检查的小研究贯通，才能知道增加粒子数、延长时间或加入水以后，需要重新检验哪些环节。读完本讲，你将得到一套可运行的研究流程，以及一张能够把连通性、链取向和机械响应逐行对应起来的条件表。

实际结果会显示两个同时成立的现象：新增连接显著改变了连通分量，而短时间机械响应还带有明显的制备与时间涨落。把它们放在一起，能够比预设“交联越多，任何一次读数都越大”得到更多信息。结构描述连接关系，机械读数描述给定状态与加载过程，两者之间还经过链的空间排列和动力学调整。理解这段中间过程，正是把一套软件操作发展成材料研究的关键。

## 从凝胶形成到珠簧模型：研究问题怎样汇合

凝胶形成曾提出一个鲜明的问题：分子为什么会从许多可以分别移动的小对象，发展成跨越样品的大连接体？Flory在1941年研究三维高分子的分子尺寸分布与凝胶化，Stockmayer在1943年进一步处理支化链中的分子尺寸分布与凝胶形成。这些工作把连接的统计关系与宏观材料状态联系起来。对今天的模拟而言，这段历史提醒我们先数清谁与谁相连，以及连接形成的是许多小团还是一个很大的团，而不只看图上是否显得密密麻麻。

链如何运动则带来了另一类问题。逐一描述真实高分子的所有原子，能够保留化学细节，也会把大量计算花在很快的局部振动上。珠簧模型选择保留链的连续连接、空间排斥和热运动，用较少自由度观察较集体的变化。Kremer与Grest在1990年的线性高分子熔体动力学研究，是这类模拟的一项经典工作。本例采用这一类FENE珠簧相互作用，通过短链和固定新增边学习网络响应。模型的教学价值来自保留了哪些机制，而不是把一个珠子直接指定成某个真实化学单元。

这两条思路在网络研究中汇合：连接统计告诉我们大团簇如何出现，分子动力学则继续问这个连接体在空间里怎样排列、运动与承载。一个闭合回路可以增加图中的循环数，却未必与另一个方向的回路产生相同拉伸响应；一段悬挂在网络边缘的链可以改变局部运动，却与连接两个远端区域的链段承担不同作用。因此，从“有多少边”到“怎样受力”之间，需要保留几何位置和运动历史。图论与动力学分别回答不同问题，结合起来才能描述这个过程。

生物网络也包含这种关系，例如细胞外基质中的纤维连接、蛋白质形成的网状结构，以及含水高分子凝胶中的永久或可逆连接。不过，它们还可能具有定向纤维、弯曲刚度、溶剂交换和化学结合过程。将当前例题扩展到这些对象时，可以保留“连接—几何—响应”的组织方法，同时逐项增加需要的物理机制。若问题是纤维弯曲，就加入合适的角度能；若问题是可逆结合，就选择能改变连接状态的模型和相应参数。具体研究对象决定下一步细化的方向。

因此，本例对历史思想的使用很具体：既计算团簇与循环，也记录链的方向、实际盒长和压力张量；既展示结构变化，也保留独立制备之间的差异。它不会用一个连通性阈值直接代替机械测量。一个模型可以连成大团，同时在所选时间窗口里表现出强烈波动；也可以局部连通性相似而具有不同空间取向。下面的解析交互先用几个可看清的点展示这种区别，再回到一千六百个真实模拟珠子的记录。

## 让每条新增连接有明确的物理含义

在零条新增边的条件里，八十条原始链已经各自拥有十九根链键，所以总键数为一千五百二十。增加八十条边后，总键数变成一千六百；增加一百六十条后，总键数变成一千六百八十。新增边从不同原始链之间的近邻珠子中选择，初始距离不超过1.15σ，而且每个珠子最多参与一条新增边。这样可以让连接在几何上局部形成，并控制新增连接对珠子配位数的影响。八十边列表是一百六十边列表的前半部分，便于在同一制备中比较逐步增加的连接。

选择一条新增边，就选择了一项持续作用的弹簧能。FENE势在键长接近上限R₀时迅速增大，限制了相连珠子无限分开。本例弹簧系数为30ε/σ²，R₀为1.5σ。原始链键与新增边使用同一种键形式，所以比较改变的是连接关系与由此引起的排列，而没有同时更换连接的刚度。键在拉伸过程中始终存在，最大键长可以作为实际运行状态的一个读数，与上限一起检查；它不是化学键断裂率，也不是反应转化率。

FENE键的弹性部分式 1

![FENE键的弹性部分](https://ml-biomat.com/static/agent-math/9daf9f66ba64c006a5ee3e20.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Uelastic | 单条键的FENE弹性能，完整键样式还含短程排斥 | ε |
| r, R₀ | 键长与最大伸长尺度，本例R₀=1.5σ | σ |
| K | 弹性系数，本例30ε/σ² | ε σ⁻² |
| ln | 自然对数，括号内量为正且无量纲 | 运算符 |
| ², 1, 2 | 平方、无量纲常数1与除数2 | 运算符与常数 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解r接近R₀时，对数内的正数趋近零，对数变为很大的负值；前面的负号使弹性能迅速增大。

算一个例子r=1σ时，U=−(30×1.5²/2)ln[1−(1/1.5)²]≈19.8378ε。这是弹性项；本例总键能还包含排斥。

使用条件0≤r<R₀；固定拓扑FENE模型，原始键和新增边采用相同参数。

FENE键的LAMMPS实现还包含直接成键珠子之间的短程排斥，配合special_bonds fene设置处理特殊邻居。直接相连的排斥项由键样式计入，非键列表不再重复同一项；隔一条和隔两条键的非键作用按相应权重保留。新增连接以后，数据文件中的键表改变，软件也要根据新的拓扑建立特殊邻居关系。完整生成程序通过新的network.data重新读入每个分支，让连接表和相互作用计数一起更新。只在结构图片上画一根线，当然不会改变实际受力。

连接建立后，局部键长与周围珠子的排布需要调整，所以三个分支各自先在固定体积下静置一百个时间单位。初始构型共享，并不要求静置后的坐标相同；不同连接关系恰好会引导它们向不同排列发展。随后再从各自静置后的状态开始同样的加载。第一套八十边分支在刚新增边时，势能增加约为每珠1.24037ε，这个变化可以由新增FENE弹性项独立复算。它帮助检查新键是否进入计算，也说明新增连接本身会改变准备阶段的能量与局部受力。

三套独立制备都采用相同密度0.85、温度1、步长0.005与热浴阻尼时间1，粒子质量也都设为1。这里长度、能量与质量分别由σ、ε和m定义，时间单位由它们组合而成。把结果映射到某种真实聚合物时，需要用目标材料的结构、密度、时间或力学观测来确定映射，而不能任意给σ附上一个纳米值就同时得到真实时间。当前研究保留约化单位，让各个条件在同一明确尺度下比较，后续再根据具体材料建立一致的物理映射。

原始链每条二十个珠子，是为了让构建、连接与加载过程都能在较小体系里完整检查。讨论较长链的缠结动力学时，链长本身就成为需要改变的参数，还要增加观察时间，检查链是否经历足够的整体运动。不同模型的缠结尺度依赖密度、刚度和相互作用，不能直接从珠子总数判断。这里的网络循环来自明确加入的键，缠结则涉及链在空间中的相互约束；两者可以同时影响力学，却对应不同的结构概念和测量方法。

## 从键表读出大团簇、循环与周期连接

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s4)

图 2 · 键表、坐标与压力记录使用相同制备编号和连接数，合并时保留一对一对应。

把珠子看成点，把键看成边，结构就成为一个图。沿着键可以相互到达的所有珠子属于同一个连通分量。我们把最大分量中的珠子数除以总珠子数，得到最大分量占比f。因为本例珠子质量相同，这个数也等于最大分量的质量占比。零新增边时，每条原始链独立，最大分量有二十个珠子，占比为0.0125。新增连接把一些原始链合在一起；占比增加说明连接范围扩大，但并没有给出这些连接在三维空间中朝向哪里。

最大连通分量占比式 2

![最大连通分量占比](https://ml-biomat.com/static/agent-math/8fab9aba4182769e3b97a1bb.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| fmax | 最大连通分量的珠子占比 | 1 |
| Nmax, N | 最大连通分量珠子数和总珠子数，本例N=1600 | 1 |
| max | 最大分量标签，不是乘法 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解最大分量珠子数除以全体系珠子数得到占比；等质量珠子使珠子占比同时等于质量占比。

算一个例子第一套80边网络的最大分量含63条20珠链，Nmax=1260，fmax=1260/1600=0.7875。

使用条件以实际Bonds表定义无向图；连通分量统计包含原始链键与新增边。

三套八十边网络的最大分量分别包含六十三、六十二和六十二条原始链，珠子占比分别为0.7875、0.7750和0.7750；一百六十边时分别包含七十九、七十九和七十八条链，占比为0.9875、0.9875和0.9750。同样的新增边数可以产生不同的连通细节，因为边落在哪些链之间取决于准备构型与局部候选。总连通分量数也随之不同：八十边时为十三、十三和十八，一百六十边时为二、二和三。保留这些逐制备结果，可以看到随机网络形成的具体变化。

每新增一条边，还可以问它是在连接两个原本分开的团，还是在同一团内部多开出一条闭合路线。全图的独立循环数由边数减点数再加连通分量数得到。对三个八十边网络，这个数分别为十三、十三和十八；一百六十边时为八十二、八十二和八十三。这里的循环数是一个严格的图结构数量。它并不自动等于承载链段数，因为循环可以具有不同的长度、位置与方向，而且网络中还可能存在悬挂部分和连接瓶颈。

独立循环数式 3

![独立循环数](https://ml-biomat.com/static/agent-math/877650cab8d715b2a8d996ce.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| β | 全图的独立循环数 | 1 |
| E | 总边数，包含原始链键与新增边 | 1 |
| N | 节点数，也就是珠子总数 | 1 |
| C | 连通分量数 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解每个连通分量的生成树用节点数减一条边；全图生成森林需N−C条边，其余E−(N−C)条各增加一个独立循环。

算一个例子第一套80边网络E=1520+80=1600，N=1600，C=13，所以β=13。两个三角形加一条桥的交互图E=7、N=6、C=1，β=2。

使用条件固定无向连接图的循环空间维数；周期绕行的独立方向需要另用边的镜像平移计算。

周期边界还要求检查连接是否绕过模拟盒。一个珠子在左边界附近，另一个在右边界附近，两者可以通过最短周期距离成键。沿一条闭合路线前进时，记录每条边跨越了多少个盒长；回到原来的珠子编号后，累计平移可能不是零。不同方向的独立平移向量构成周期绕行的维数。本例所有新增边网络的最大分量都具有三维绕行，而零新增边的原始链分量没有这种闭合绕行。这里同时用到连接与坐标，能区分普通小回路和跨周期单元的连接。

对贯穿周期盒的整个网络，通常无法挑选一组单一的展开坐标，让所有跨周期闭合路线都同时变成有限盒内的短边。因此，本讲的链形状分析继续沿用原始八十条链的身份，每条链用自己的珠子镜像标记展开，然后围绕该链质心计算尺寸。网络连通性则由完整键表和周期边关系计算。两个分析的对象有明确区别：一个关注连接后的整体图，另一个追踪组成网络的原始链段。它们通过相同样本身份相连，而不是强行共用一种坐标展开方式。

## 相同连接关系，也可以有不同空间响应

先看一个小网络：六个点组成两个三角形，中间有一条桥边。无论把整张图转过多少角度，它始终有六个点、七条边、一个连通分量和两个独立循环，最大分量占比始终为1。现在沿水平方向拉长，并在竖直方向适当缩短，使这张平面示意对应三维定体积映射中的一个切面。某些边接近拉伸方向，会增长较多；另一些边接近横向，会缩短。即使连接完全不变，边的原始方向也会影响各弹簧储存的能量。

仿射二次弹簧模型：六个点、七条边、一个分量、两个独立循环。先旋转同一个网络，再进行拉伸。

[Figure: 旋转与拉伸后的六点弹簧网络](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s5)

连接保持不变，改变初始方向与伸长比，比较指定仿射形变下的二次弹簧能。

几何交互中的二次弹簧能式 7

![几何交互中的二次弹簧能](https://ml-biomat.com/static/agent-math/487088030e84a15a5e28ba91.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Ugeom | 指定仿射形变后的总弹簧能 | ε |
| k | 弹簧刚度，交互取1ε/σ² | ε σ⁻² |
| e, E | 边编号和边数E=7 | 1 |
| re, re,0 | 当前两端点欧氏距离及变形前长度 | σ |
| Σ, ², 2 | 对7条边累加、平方与二次弹簧能的除数2 | 运算符与常数 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解每条边偏离自身平衡长度后储能，伸长和压缩都产生正的平方项；方向通过形变后的距离进入计算。

算一个例子一条水平桥边原长2σ，λ=1.2后长2.4σ，它的能量为(1/2)×(0.4)²=0.08ε；总能量还要加上其余六条边。

使用条件解析几何模型，所有点按指定映射移动；不含热运动或节点后续松弛。完整原生网络使用FENE。

交互中的弹簧采用简单的二次能量，平衡长度取每条边变形前的长度，刚度取1。节点按指定形变一起移动，所以计算的是这一几何操作下的弹簧能，而不是节点自行松弛后的平衡响应。没有拉伸时，各边恰好处于各自平衡长度，能量为零；拉伸以后，伸长和压缩都会贡献正的平方项。旋转网络时，程序重新计算每条边与加载方向的夹角，然后得到新的能量。这个解析模型用来说明几何的重要性，完整分子模拟仍使用前面的FENE与热运动。

完整网络的盒长也有清楚的形变规则：x方向伸长比从1线性增加到1.2，y、z两个方向都按x伸长比平方根的倒数缩短，使三个方向伸长比的乘积保持为1。最终横向伸长比约为0.91287。加载阶段持续一百个时间单位，然后三方向盒长保持不变。程序读取实际记录的盒长来核对体积与伸长，而不只根据输入的目标值给图标注坐标。这样可以把施加的几何操作和记录时刻的真实状态对应起来。

定体积形变式 4

![定体积形变](https://ml-biomat.com/static/agent-math/170d612a42c33b5239e47004.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| λx, λy, λz | 各方向当前盒长除以参考盒长 | 1 |
| λ | 指定的轴向伸长比，模拟从1变到1.2；交互范围1至1.5 | 1 |
| x, y, z | 加载方向与两个横向坐标标签 | 1 |
| −1/2 | 先开平方再取倒数 | 指数 |
| 1 | 参考体积归一后等于1 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解正交盒体积等于三个边长相乘；三个伸长比的乘积为1，故总体积保持。交互将每个坐标乘相应伸长比。

算一个例子λ=1.2时，λy=λz=1/√1.2≈0.912871，1.2×0.912871²≈1。

使用条件三维正交盒、两个横向采用相同缩放；交互节点在z=0平面，是该三维映射的一个切面。

原始链的空间变化用三个方向的均方尺寸来描述。先找到一条链的质心，再计算所有珠子在x、y、z各方向离质心多远，平方后对珠子平均；然后对八十条原始链平均，得到Gₓₓ、Gᵧᵧ和Gzz。x方向占比fₓ是Gₓₓ除以三个方向之和。各向同性的统计参考为三分之一，较大的fₓ表示尺寸更多分配在x方向。它与单根键是否朝向x有关，却是不同尺度的观测：整条链可以在多个局部弯折之间整体展开。

原始链群体的方向尺寸式 5

![原始链群体的方向尺寸](https://ml-biomat.com/static/agent-math/60426c1a306412afb2a29ddb.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| M, n | 原始链数M=80，每条链珠子数n=20 | 1 |
| c, i | 原始链编号与链内珠子编号 | 1 |
| xci, x̄c | 第c条链第i珠子的展开x坐标及该链质心x坐标 | σ |
| Gxx, Gyy, Gzz | 先在每条链内平均平方偏差，再对80条链平均；另两方向同理 | σ² |
| fx | 链群体均方尺寸的x方向占比 | 1 |
| Σ, ², overbar | 累加、平方与平均符号 | 运算符 |
| 1/M, 1/n | 链数和珠子数的归一化因子 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解围绕每条链自身质心测量，消去整体平移；三方向平方偏差之和为群体平均Rg²，取比得到方向占比。

算一个例子若Gxx=2、Gyy=1.5、Gzz=1.5σ²，则fx=2/5=0.4。第一套160边网络在200τ的实际fx≈0.410463。

使用条件等质量、等长原始链，按镜像标记展开；先平均G再取比。使用100、200、300τ保存帧。

### 原始链在三个阶段的方向尺寸

100、200与300τ的保存帧；先对80条链平均G，再计算x方向占比。虚线为1/3各向同性参考。

LAMMPS 30 Sep 2026 Update 1；官方珠簧相互作用模型，1600个珠子、80条20珠链，ρ*=0.85、T*=1，三个初始构型；FENE/WCA正式动力学时间步0.005τ。

[下载参考数据与完整输入（ZIP） 48.70 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-study-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s5)

比较100、200和300τ保存帧中的原链形状；先平均80条链的回转张量，再计算x方向占比。

第一套一百六十边网络的fₓ在静置末端约为0.30864，加载末端约为0.41046，保持末端约为0.39444。加载使该时刻的链尺寸更偏向x，随后发生部分调整。图中三个时刻分别对应100、200和300τ，展示的是各自保存帧的原链群体尺寸，不是二十时间单位窗口平均。应力响应Y采用时间窗平均，因此在比较形状与Y时要同时读清时间定义。更细的动力学关系可以使用全部形状时间序列，与相同窗口中的应力共同分析。

## 把结构与力学放进同一张条件表

力学部分继续使用沿x方向的法向应力差S，再把保持后段280<t≤300的平均值减去静置后段50≤t<100的平均值，得到Y。这样的响应定义保留各分支自身的加载前基线，单位为ε/σ³。九条分支都使用相同时间窗。分析程序先分别读取连接表与压力记录，再用“制备编号、连接数”这对键连接结果。如果某个条件缺失、重复，或结构表与力学表身份不一致，程序会停止并要求整理数据，而不会按照文件排序把两份表强行拼接。

有限时间机械响应式 6

![有限时间机械响应](https://ml-biomat.com/static/agent-math/c773bd32faf52f1f21d2e703.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Pxx, Pyy, Pzz | 压力张量三个对角分量，正号采用压力约定 | ε σ⁻³ |
| S | 轴向相对横向平均的法向应力差 | ε σ⁻³ |
| S̄hold, S̄rest | 280<t≤300及50≤t<100的算术时间平均，t以τ计 | ε σ⁻³ |
| Y | 相对各分支静置基线的后段保持响应 | ε σ⁻³ |
| 2, overbar | 两个横向取平均的除数2；横线表示窗口平均 | 常数与运算符 |
| =, +, −, /, × | 等于、相加、相减、相除、相乘；相邻量表示乘法 | 运算符 |

怎样理解方向相减消去共有的各向同性压力；窗口相减表达加载后相对自身基线的变化。

算一个例子第一套80边基线约−0.0114838，保持后段平均约0.0407141，故Y≈0.0521979ε/σ³。

使用条件每0.5τ等间隔记录，基线100条、后段40条；定体积加载的有限流程响应。

### 同一条件的连通性与后段机械响应

每个点对应一个完整条件，颜色为新增边数，数字为制备编号；结构与力学通过共同身份配对。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s6)

每点对应同一制备与新增边数；结构量和规定时间窗的应力响应按共同身份连接，点旁数字表示制备编号。

散点图左侧用最大分量占比作为横坐标，右侧用独立循环数；纵坐标都是同一条件的Y。颜色区分新增边数，点旁数字区分制备编号。这样，一百六十边的三个点虽然在结构指标上靠近，却仍保留了各自的机械响应。第一与第二套的最大分量占比同为0.9875，而Y分别约为−0.04285和0.15836。这个对照说明最大分量占比并没有记录所有与本次响应相关的信息：局部连接位置、空间排列、热运动和时间平均都还参与其中。

三套制备内的一百六十边减零边的配对差分别约为−0.00122、0.12264和−0.07388。这里同一制备内部保留共同起点，跨制备则保留独立准备。把九个点全部塞进一条回归直线，既容易忽略这种层级，也会把连接数、团簇占比和循环数之间的共同变化混在一起。当前图的任务是展示已发生的对应关系，并据此设计更有针对性的比较。例如固定新增边数，选择不同局部连接规则，再检查几何与机械读数，就能够专门研究连接安排的影响。

### 九个研究条件的综合表

每行连接同一制备与连接数的图结构、形状变化和规定窗口响应；完整数值保存在CSV与JSON。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s6)

九个条件的连通性、周期绕行、局部键长、原链形状及规定窗口应力响应汇于同一表。

条件表把最大分量占比、分量数、循环数、周期绕行秩、最大键长、加载后的形状变化和Y并排保存。每行都代表一条完整运行，表中的数来自对应原始记录。其中最大键长用于查看FENE键在整个流程里的伸长范围，周期绕行秩用于描述连接跨盒的方向，形状变化则比较两个保存时刻。它们虽然放在同一行，却有不同单位和时间含义。保留这些定义，可以避免把一列数简单当作另一列的替代测量，也便于在异常条件出现时定位到具体运行。

还可以对照温度、体积与键长来理解运行条件是否按设计执行。九条分支的加载与保持平均温度都接近设定的1，体积比偏差处于浮点记录精度尺度，最大键长低于1.21σ，距离FENE上限1.5σ有明确间隔。这些读数支撑的是数值流程和规定模型状态的检查。对材料机制的解释继续依赖前面的结构、方向和响应数据。将执行状态与科学观测各自讲清楚，可以让一张完整条件表同时服务于复现和理解。

同一个静置后的网络还可以接受另一种加载方案，例如更大的最终伸长或更长保持。这样的比较应保存为另一个明确流程，并继续使用相同的结构身份。若同时改变伸长幅度和加载时长，差异归属于整套操作；若要分辨某一参数的作用，则逐项安排成组变化。现有短流程已经给出起始网络、数值范围和真实波动，可以据此决定下一轮计算的规模，而不需要改变已有数据的解释。每一轮新的测量都应当使问题更具体。

## 从完整输入运行到可追踪的综合图

完整生成程序建立初始链、准备熔体、选择新增边，并为每条分支写入结构和LAMMPS输入。三个制备使用不同种子，同一制备中的零、八十和一百六十边分支共享准备起点，连接列表保持嵌套。调用时指定一千六百珠子和制备编号，程序会把每个条件放在清楚命名的子目录中。输入文件保留原始链编号、新增边清单和镜像信息，这些数据分别服务于图分析、配对比较和链尺寸重建。保存它们的原因来自后续测量，而不是为了积累尽可能多的文件。

### 完整构建与模拟程序

```
"""Prepare, connect, relax and stretch a FENE bead-spring network.

python run_network.py --beads 1600 --replica 1 --out-dir network-runs
The LAMMPS executable is selected by --lmp or the LAMMPS environment variable.
Each independent preparation is followed by zero, one or two links per
original chain in total. The linked cases share nested selected-edge lists.
The output retains the exact selected endpoints, inputs and simulation logs.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,re,math
import numpy as np
import os,shutil
p=argparse.ArgumentParser();p.add_argument('--beads',type=int,default=1600);p.add_argument('--replica',type=int,default=1);p.add_argument('--out-dir',type=Path,default=Path('network-runs'));p.add_argument('--lmp',default=os.environ.get('LAMMPS','lmp'));a=p.parse_args()
N=a.beads;M=N//20;assert N%20==0
base=a.out_dir.resolve();d=base/f'n{N}-rep{a.replica}'
if d.exists():raise SystemExit('Choose a new output directory for this configuration.')
d.mkdir(parents=True)
seed=20263000+a.replica;generator=np.random.default_rng(seed);L=(N/.85)**(1/3);coords=[];bonds=[]
# Pack open chains while retaining the seeded sequence of random draws.
for chain in range(M):
 current=generator.uniform(0,L,3)
 for local in range(20):
  for attempt in range(100000):
   candidate=generator.uniform(0,L,3) if local==0 else current+.97*(v:=generator.normal(size=3))/np.linalg.norm(v)
   if coords:
    dr=np.array(coords)-candidate;dr-=L*np.round(dr/L)
    if np.min(np.sum(dr*dr,axis=1))<.65**2:continue
   break
  else:raise RuntimeError('Chain packing did not find a valid location')
  coords.append(candidate.copy());current=candidate
  if local:bonds.append((len(coords)-1,len(coords)))
lines=['Generated FENE chain starting configuration','',f'{N} atoms',f'{len(bonds)} bonds','','1 atom types','2 bond types','',f'0 {L:.15g} xlo xhi',f'0 {L:.15g} ylo yhi',f'0 {L:.15g} zlo zhi','','Masses','','1 1.0','','Atoms # bond','']
for i,xyz in enumerate(coords):
 image=np.floor(xyz/L).astype(int);wrapped=xyz-L*image;lines.append(f'{i+1} {i//20+1} 1 '+' '.join(f'{x:.15g}' for x in wrapped)+' '+' '.join(str(x) for x in image))
lines+=['','Bonds','']+[f'{j+1} 1 {i} {k}' for j,(i,k) in enumerate(bonds)]
(d/'initial.data').write_text('\n'.join(lines)+'\n')
# Shared reduced-unit, neighbour and special-pair definitions.
header='''units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
'''
# Instantaneous records: time, T, U/N, K/N, E/N, pressure, box and longest bond.
record='''compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
'''
# Soft separation, FENE switch, minimization and 100 tau melt preparation.
prepare=header+f'''read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 {seed+100} mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+200} zero yes
variable softA equal ramp(0,100)
fix soften all adapt 1 pair soft a * * v_softA
timestep 0.002
thermo 1000
thermo_style custom step temp pe ke etotal
run 20000
unfix soften
unfix dyn
unfix bath
write_data after-soft.data
pair_style lj/cut 1.122462048309373
pair_modify shift yes
pair_coeff * * 1 1 1.122462048309373
bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0
min_style cg
min_modify dmax 0.01
minimize 1e-8 0.01 10000 100000
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+300} zero yes
'''+record+'''run 20000
write_restart melt.restart
write_data melt.data
'''
(d/'prepare.lmp').write_text(prepare,encoding='utf-8',newline='\n')
found=shutil.which(a.lmp);assert found, f'LAMMPS executable not found: {a.lmp}';binary=Path(found).resolve();logs=[]
def run(where,script):
 cmd=[str(binary),'-in',script,'-log','simulation.log']
 r=dict(command=cmd,directory=where.relative_to(base).as_posix(),input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});t=time.perf_counter()
 with (where/'stdout.log').open('wb') as f:q=subprocess.run(cmd,cwd=where,env={**os.environ,'OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 r.update(exit_code=q.returncode,wall_seconds=time.perf_counter()-t,output_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});logs.append(r)
 (d/'progress.json').write_text(json.dumps(logs,indent=2));print(json.dumps({'directory':str(where),'exit_code':q.returncode,'wall_seconds':r['wall_seconds']}),flush=True)
 if q.returncode:raise SystemExit(q.returncode)
run(d,'prepare.lmp')
data=(d/'melt.data').read_text();atompart=re.search(r'\nAtoms[^\n]*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',data,re.S)[1]
atoms=np.array([[float(x) for x in line.split()] for line in atompart.splitlines() if line.strip()]);atoms=atoms[np.argsort(atoms[:,0])];xyz=atoms[:,3:6];mol=atoms[:,1].astype(int)
# Candidate edges connect nearby beads with different original chain IDs.
candidate=[]
for i in range(N-1):
 dr=xyz[i+1:]-xyz[i];dr-=L*np.round(dr/L);r2=np.sum(dr*dr,1)
 for j in np.flatnonzero((r2<=1.15**2)&(mol[i+1:]!=mol[i])):candidate.append((i,int(i+1+j),float(np.sqrt(r2[j]))))
# Greedy matching uses each bead once; prefixes of one list give nested cases.
edgegen=np.random.default_rng(seed+400);edgegen.shuffle(candidate);edges=[];used=set()
for i,j,dist in candidate:
 if i not in used and j not in used:edges.append((i+1,j+1,dist));used.update((i,j))
target=M*2
if len(edges)<target:raise RuntimeError(f'Only {len(edges)} available edges for {target} target')
# Each branch: 100 tau relaxation, 100 tau extension, 100 tau fixed strain.
choices=[0,M,2*M]
for nc in choices:
 sub=d/f'links-{nc}';sub.mkdir();selected=edges[:nc];text=data
 text=re.sub(r'^\d+ bonds$',f'{len(bonds)+nc} bonds',text,flags=re.M)
 match=re.search(r'\nBonds\s*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',text,re.S)
 original=match[1].strip();addition='\n'.join(f'{len(bonds)+j+1} 2 {i} {k}' for j,(i,k,_) in enumerate(selected))
 text=text[:match.start(1)]+original+'\n'+addition+'\n'+text[match.end(1):]
 (sub/'network.data').write_text(text)
 (sub/'selected-crosslinks.json').write_text(json.dumps(dict(seed=seed+400,candidates=len(candidate),selected=selected,definition='Different original chain IDs, minimum-image distance<=1.15, at most one added edge per bead; common ordered candidate list gives nested link sets.'),indent=2))
 protocol=header+f'''bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+500} zero yes
'''+record+'''run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
'''
 (sub/'network.lmp').write_text(protocol,encoding='utf-8',newline='\n');run(sub,'network.lmp')
receipt=dict(case='lammps-network',N=N,chains=M,replica=a.replica,seed=seed,rho=.85,chain_length=20,links=choices,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),source='Official LAMMPS30Sep2026Update1 bench/in.chain interaction model; independently generated coordinates and explicitly added crosslink/deformation protocols',runs=logs,exit_code=0)
(d/'receipt.json').write_text(json.dumps(receipt,indent=2));print('Network comparison complete',flush=True)
```

建立三分支固定网络，保存连接、坐标与实际压力记录。

### 第一套80边分支完整输入

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
```

由生成程序写入相应分支目录，在network.data旁执行。

连接分析程序读取network.data与relaxed.data，核对新增边、计算分量、循环和周期绕行，并检查静置前后的键长。力学程序读取thermo.dat与轨迹，重建原始链形状，核对实际盒长，计算压力差与规定时间窗口的响应。两个程序都完整显示在下方，可以单独运行并检查中间表。综合程序再读取它们的数值输出，用明确的样本键合并，生成本讲三幅图和study_conditions.csv。每个图上的数值都来自这条可追踪的路径。

### 完整连通性与周期绕行分析

```
"""Measure the actual fixed-topology networks and their initial relaxation.

python analyze_network.py network-runs --out network-analysis --language en
Requires NumPy and Matplotlib. The input directory contains n1600-rep1/2/3.
Each replica contains links-0/80/160 with network.data, relaxed.data,
selected-crosslinks.json and thermo.dat. 
"""
from pathlib import Path
import argparse
import csv
import json
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.collections import LineCollection


def read_data(path):
    """Read the orthogonal atom_style bond files used in this example."""
    text = path.read_text(encoding="utf-8")
    sections, section = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z ]*", line):
            section = line
            sections[section] = []
        elif section:
            sections[section].append(line.split())
    atoms = np.asarray(sections["Atoms"], float)
    atoms = atoms[np.argsort(atoms[:, 0])]
    assert np.array_equal(atoms[:, 0], np.arange(1, len(atoms) + 1))
    bonds = np.asarray(sections["Bonds"], int)
    bounds = []
    for direction in "xyz":
        found = re.search(rf"^([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+{direction}lo {direction}hi", text, re.M)
        bounds.append([float(found[1]), float(found[2])])
    bounds = np.asarray(bounds)
    return {"xyz": atoms[:, 3:6], "mol": atoms[:, 1].astype(int),
            "box": bounds[:, 1]-bounds[:, 0], "bonds": bonds}


def bond_geometry(data):
    ends = data["bonds"][:, 2:4] - 1
    delta = data["xyz"][ends[:, 1]] - data["xyz"][ends[:, 0]]
    shift = -np.rint(delta / data["box"]).astype(int)
    minimum_image = delta + shift * data["box"]
    return ends, shift, np.linalg.norm(minimum_image, axis=1)


def connectivity(data):
    """Graph components, cycle counts and independent periodic directions.

    Integer image offsets are propagated along a spanning tree. A cycle that
    closes at a different periodic image leaves a nonzero integer vector.
    The rank of these vectors counts independent periodic winding directions.
    """
    n = len(data["xyz"])
    ends, shifts, lengths = bond_geometry(data)
    graph = [[] for _ in range(n)]
    for edge_id, ((i, j), shift) in enumerate(zip(ends, shifts)):
        graph[i].append((j, shift, edge_id))
        graph[j].append((i, -shift, edge_id))
    labels = np.full(n, -1, int)
    offsets = np.zeros((n, 3), int)
    components = []
    for root in range(n):
        if labels[root] >= 0:
            continue
        label = len(components)
        labels[root] = label
        stack, vertices, edge_ids, closures = [root], [], set(), []
        while stack:
            i = stack.pop()
            vertices.append(i)
            for j, shift, edge_id in graph[i]:
                edge_ids.add(edge_id)
                trial = offsets[i] + shift
                if labels[j] < 0:
                    labels[j] = label
                    offsets[j] = trial
                    stack.append(j)
                else:
                    assert labels[j] == label
                    closure = trial - offsets[j]
                    if np.any(closure):
                        closures.append(closure.tolist())
        unique_closures = np.unique(closures, axis=0) if closures else np.empty((0, 3), int)
        rank = int(np.linalg.matrix_rank(unique_closures.astype(float), tol=1e-10)) if len(unique_closures) else 0
        components.append({"beads": len(vertices), "edges": len(edge_ids),
                           "original_chains": len(np.unique(data["mol"][vertices])),
                           "independent_cycles": len(edge_ids)-len(vertices)+1,
                           "winding_rank": rank,
                           "integer_closure_vectors": unique_closures.tolist()})
    largest_id = int(np.argmax([c["beads"] for c in components]))
    largest = components[largest_id]
    degree = np.array([len(x) for x in graph])
    return {"components": components, "component_count": len(components),
            "largest": largest, "largest_id": largest_id, "labels": labels,
            "total_cycles": len(ends)-n+len(components), "degree": degree,
            "lengths": lengths, "ends": ends}


def numeric_rows(path):
    return np.loadtxt(path, comments="#")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("network-analysis"))
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        base = args.directory / f"n1600-rep{replica}"
        previous_edges = set()
        for count in (0, 80, 160):
            folder = base / f"links-{count}"
            before = read_data(folder / "network.data")
            after = read_data(folder / "relaxed.data")
            graph = connectivity(before)
            later = connectivity(after)
            n = len(before["xyz"])
            assert n == 1600 and len(np.unique(before["mol"])) == 80
            selected = json.loads((folder / "selected-crosslinks.json").read_text(encoding="utf-8"))["selected"]
            chosen = {tuple(sorted((int(x[0]), int(x[1])))) for x in selected}
            assert len(chosen) == count and previous_edges <= chosen
            previous_edges = chosen
            added = before["bonds"][:, 1] == 2
            endpoints = graph["ends"][added]
            assert len(endpoints) == count
            assert len(np.unique(endpoints)) == 2*count
            assert np.all(before["mol"][endpoints[:, 0]] != before["mol"][endpoints[:, 1]])
            assert np.all(graph["lengths"][added] <= 1.15 + 1e-10)
            assert graph["component_count"] == later["component_count"]
            assert graph["largest"]["winding_rank"] == later["largest"]["winding_rank"]
            # Equal masses make the largest bead fraction a mass fraction too.
            largest_fraction = graph["largest"]["beads"] / n
            t = numeric_rows(folder / "thermo.dat")
            t = t[(t[:, 1] >= 0) & (t[:, 1] <= 100)]
            assert len(t) == 201
            elastic_added = float(np.sum(-.5*30*1.5**2*np.log1p(-(graph["lengths"][added]/1.5)**2)))
            if count == 0:
                reference_energy = t[0, 3]
            observed_change = float(t[0, 3]-reference_energy)
            assert abs(observed_change-elastic_added/n) < 1e-9
            assert np.max(graph["degree"]) <= 3
            old_lengths = graph["lengths"][~added]
            new_lengths = graph["lengths"][added]
            relaxed_new = later["lengths"][after["bonds"][:, 1] == 2]
            rec = {"replica": replica, "added_links": count,
                   "beads": n, "total_bonds": len(before["bonds"]),
                   "component_count": graph["component_count"],
                   "largest_component_beads": graph["largest"]["beads"],
                   "largest_component_chains": graph["largest"]["original_chains"],
                   "largest_mass_fraction": largest_fraction,
                   "total_independent_cycles": graph["total_cycles"],
                   "largest_winding_rank": graph["largest"]["winding_rank"],
                   "modified_bead_fraction": 2*count/n,
                   "mean_degree": float(graph["degree"].mean()),
                   "degree_counts": {str(k): int(np.sum(graph["degree"] == k)) for k in (1, 2, 3)},
                   "initial_U_change_per_bead": observed_change,
                   "sum_added_FENE_elastic_per_bead": elastic_added/n,
                   "original_bond_initial_mean": float(old_lengths.mean()),
                   "added_bond_initial_mean": float(new_lengths.mean()) if count else None,
                   "added_bond_after_100tau_mean": float(relaxed_new.mean()) if count else None,
                   "max_bond_before": float(graph["lengths"].max()),
                   "max_bond_after_100tau": float(later["lengths"].max()),
                   "late_50_100tau_temperature_mean": float(t[t[:, 1] >= 50, 2].mean()),
                   "components": graph["components"]}
            records.append(rec)
            raw[(replica, count)] = (before, after, graph, later, t)
    summary = {"case": "fixed FENE networks", "records": records,
               "topology": "All edges retained, including parallel connections between original chains.",
               "winding": "Rank of integer closure vectors; connectivity is distinct from mechanical response.",
               "time_scope": "Topology at insertion; before/after100tau fixed-volume relaxation. All statistics are finite-window descriptors."}
    (args.out / "network_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    table = [{k: v for k, v in rec.items() if k not in ("components", "degree_counts")} for rec in records]
    with (args.out / "network_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    colors = ["#187e89", "#ca713f", "#7663a0"]
    def save(fig, name):
        fig.savefig(args.out / f"{name}.svg")
        fig.savefig(args.out / f"{name}.png", dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for replica, color in enumerate(colors, 1):
        rr = [x for x in records if x["replica"] == replica]
        for ax, key in zip(axes, ["largest_mass_fraction", "component_count", "total_independent_cycles"]):
            ax.plot([x["added_links"] for x in rr], [x[key] for x in rr], "o-", color=color,
                    label=tr(f"构型 {replica}", f"Configuration {replica}"), alpha=.8)
    axes[0].set_ylabel(tr("最大连通分量质量分数", "Largest-component mass fraction"))
    axes[0].set_ylim(0, 1.05)
    axes[1].set_ylabel(tr("连通分量数", "Connected components"))
    axes[2].set_ylabel(tr("独立环数 E − V + C", "Independent cycles E − V + C"))
    for ax in axes:
        ax.set_xlabel(tr("新增连接数", "Added connections")); ax.set_xticks([0, 80, 160]); ax.grid(alpha=.2)
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同一熔体逐步加边：哪些链已经连在一起", "Adding edges to each melt: which chains are connected"), fontsize=19)
    save(fig, "network-connectivity")
    # A chain-level circular graph is a connectivity drawing, not a spatial projection.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    theta = np.linspace(0, 2*np.pi, 80, endpoint=False)
    positions = np.column_stack([np.cos(theta), np.sin(theta)])
    for ax, count in zip(axes, (0, 80, 160)):
        data, _, graph, _, _ = raw[(1, count)]
        selected = data["bonds"][:, 1] == 2
        chain_ends = data["mol"][graph["ends"][selected]]-1
        segments = positions[chain_ends]
        if len(segments):
            ax.add_collection(LineCollection(segments, colors="#6c9c99", linewidths=.7, alpha=.5))
        chain_labels = graph["labels"][np.arange(80)*20]
        in_largest = chain_labels == graph["largest_id"]
        # At zero links all components are tied; use the same color for all chains.
        node_colors = np.where(in_largest, "#177d88", "#d59564") if count else ["#d59564"]*80
        ax.scatter(positions[:, 0], positions[:, 1], c=node_colors, s=26, zorder=3)
        rr = next(x for x in records if x["replica"] == 1 and x["added_links"] == count)
        ax.set_title(tr(f"{count} 条新增边", f"{count} added edges"))
        ax.text(0, -1.3, tr(f"最大分量：{rr['largest_component_chains']}/80 条链", f"Largest component: {rr['largest_component_chains']}/80 chains"), ha="center", fontsize=12)
        ax.set_aspect("equal"); ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.46, 1.15); ax.axis("off")
    fig.suptitle(tr("构型 1 的连接图：每个圆点代表一条原始链", "Configuration 1 connectivity: one node per original chain"), fontsize=18)
    save(fig, "network-chain-graph")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), constrained_layout=True)
    bins = np.linspace(.85, 1.20, 36)
    for count, color in zip((80, 160), colors[:2]):
        for stage, linestyle in [(0, "--"), (1, "-")]:
            vals = []
            for replica in (1, 2, 3):
                before, after, graph, later, t = raw[(replica, count)]
                dat, gg = (before, graph) if stage == 0 else (after, later)
                vals.extend(gg["lengths"][dat["bonds"][:, 1] == 2])
            axes[0].hist(vals, bins=bins, density=True, histtype="step", lw=2, color=color, linestyle=linestyle,
                         label=f"{count}: " + (tr("刚加边", "Just connected") if stage == 0 else tr("100τ 后", "After 100τ")))
    for replica, color in enumerate(colors, 1):
        for count, linestyle in [(80, "--"), (160, "-")]:
            t = raw[(replica, count)][4]
            axes[1].plot(t[:, 1], t[:, 12], color=color, ls=linestyle, lw=1.1, alpha=.7,
                         label=tr(f"构型{replica} · {count}边", f"Config. {replica} · {count} links"))
    axes[0].set(xlabel=tr("新增键长 / σ", "Added-bond length / σ"), ylabel=tr("概率密度 / σ⁻¹", "Probability density / σ⁻¹"))
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("全体系最大键长 / σ", "Largest bond length / σ"))
    for ax in axes:
        ax.legend(frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2); ax.grid(alpha=.2)
    fig.suptitle(tr("连接后的局部几何松弛", "Local geometrical relaxation after adding connections"), fontsize=19)
    save(fig, "network-bond-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.4), sharex=True, constrained_layout=True)
    for count, color in zip((0, 80, 160), colors):
        t = raw[(1, count)][4]
        axes[0].plot(t[:, 1], t[:, 2], color=color, lw=1.1, label=tr(f"{count} 条新增边", f"{count} added edges"))
        axes[1].plot(t[:, 1], t[:, 3]-t[0, 3], color=color, lw=1.3)
    axes[0].axhline(1, color="#6d7779", ls="--", lw=1)
    axes[0].set_ylabel(tr("温度 T*", "Temperature T*")); axes[0].legend(frameon=False, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=3, fontsize=11)
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("相对各分支起点的 Δ(U/N) / ε", "Δ(U/N) from each branch's start / ε"))
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle(tr("构型 1：固定连接后的温度与势能调整", "Configuration 1: temperature and energy after fixing the connections"), fontsize=18)
    save(fig, "network-preparation")
    print(json.dumps(table, indent=2))


if __name__ == "__main__":
    main()
```

读取连接与静置结构，计算图与周期连接指标。

### 完整形状与力学分析

```
"""Read network deformation, stress and original-chain orientation.

python analyze_mechanics.py network-runs --out mechanics --language en
Requires NumPy and Matplotlib. Each n1600-rep1/2/3 directory contains
links-0/80/160 with thermo.dat and trajectory.lammpstrj.
Stress uses the tension-positive normal difference -Pxx+(Pyy+Pzz)/2.
Shading is the sample SD across three independently prepared configurations.
"""
from pathlib import Path
import argparse
import csv
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    """Read orthogonal LAMMPS custom dumps and preserve atom identity."""
    with path.open(encoding="utf-8") as stream:
        while line := stream.readline():
            if not line.strip():
                continue
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(stream.readline())
            assert stream.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(stream.readline())
            assert stream.readline().strip() == "ITEM: BOX BOUNDS pp pp pp"
            bounds = np.array([[float(x) for x in stream.readline().split()] for _ in range(3)])
            columns = stream.readline().split()[2:]
            atoms = np.array([[float(x) for x in stream.readline().split()] for _ in range(n)])
            index = {name: i for i, name in enumerate(columns)}
            atoms = atoms[np.argsort(atoms[:, index["id"]])]
            assert np.array_equal(atoms[:, index["id"]], np.arange(1, n+1))
            xyz = atoms[:, [index[k] for k in ("x", "y", "z")]]
            image = atoms[:, [index[k] for k in ("ix", "iy", "iz")]]
            box = bounds[:, 1]-bounds[:, 0]
            yield step*.005, xyz+image*box, atoms[:, index["mol"]].astype(int), box


def chain_shape(path):
    """Equal-mass original chains: gyration components and bond alignment."""
    rows = []
    for time, xyz, mol, box in frames(path):
        assert len(xyz) == 1600
        assert np.array_equal(mol, np.repeat(np.arange(1, 81), 20))
        chains = xyz.reshape(80, 20, 3)
        relative = chains-chains.mean(axis=1, keepdims=True)
        gyration = np.mean(relative**2, axis=(0, 1))
        vectors = np.diff(chains, axis=1)
        distances = np.linalg.norm(vectors, axis=2)
        assert distances.max() < 1.5
        orientation = np.mean((3*(vectors[:, :, 0]/distances)**2-1)/2)
        rows.append([time, *gyration, orientation, distances.mean(), distances.max()])
    rows = np.asarray(rows)
    assert len(rows) == 121 and np.isclose(rows[-1, 0], 300)
    return rows


def block_means(time, values, start, stop, width):
    """Non-overlapping blocks (left, right], with one mean per block."""
    out = []
    for left in np.arange(start, stop, width):
        mask = (time > left+1e-9) & (time <= left+width+1e-9)
        assert mask.any()
        out.append([left+width/2, np.mean(values[mask])])
    return np.asarray(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("mechanics"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        for links in (0, 80, 160):
            base = args.directory/f"n1600-rep{replica}"/f"links-{links}"
            thermo = np.loadtxt(base/"thermo.dat", comments="#")
            assert thermo.shape == (601, 13)
            time = thermo[:, 1]
            assert np.allclose(time, np.arange(601)*.5)
            box = thermo[:, 9:12]
            stretches = box/box[0]
            volume_ratio = np.prod(stretches, axis=1)
            # ave/time precedes fix deform in the end-of-step fix order.
            # During loading its recorded box is one integration step behind
            # the post-remap box saved in trajectory/data output.
            recorded_elapsed = np.clip(time-100, 0, 100)
            loading_record = (time > 100) & (time <= 200)
            recorded_elapsed[loading_record] -= .005
            expected_x = 1+.002*recorded_elapsed
            expected_yz = expected_x**(-.5)
            assert np.max(np.abs(stretches[:, 0]-expected_x)) < 1e-12
            assert np.max(np.abs(stretches[:, 1:]-expected_yz[:, None])) < 1e-12
            stress = -thermo[:, 6]+.5*(thermo[:, 7]+thermo[:, 8])
            baseline_mask = (time >= 50) & (time < 100)
            baseline = float(stress[baseline_mask].mean())
            shape = chain_shape(base/"trajectory.lammpstrj")
            start_shape = shape[np.isclose(shape[:, 0], 100)][0]
            end_shape = shape[np.isclose(shape[:, 0], 200)][0]
            final_shape = shape[-1]
            summary = {
                "replica": replica, "added_links": links,
                "initial_box_sigma": box[0].tolist(), "final_box_sigma": box[-1].tolist(),
                "final_stretches": stretches[-1].tolist(),
                "final_engineering_strain": float(stretches[-1, 0]-1),
                "final_hencky_strain": float(np.log(stretches[-1, 0])),
                "engineering_strain_rate_per_tau": .002,
                "max_volume_ratio_error": float(np.max(np.abs(volume_ratio-1))),
                "baseline_stress_50_le_t_lt_100": baseline,
                "loading_end_stress_190_lt_t_le_200": float(stress[(time > 190) & (time <= 200)].mean()),
                "early_hold_stress_200_lt_t_le_220": float(stress[(time > 200) & (time <= 220)].mean()),
                "late_hold_stress_280_lt_t_le_300": float(stress[(time > 280) & (time <= 300)].mean()),
                "loading_temperature_mean": float(thermo[(time > 100) & (time <= 200), 2].mean()),
                "holding_temperature_mean": float(thermo[(time > 200) & (time <= 300), 2].mean()),
                "max_bond_sigma": float(thermo[:, 12].max()),
                "gyration_components_t100": start_shape[1:4].tolist(),
                "gyration_components_t200": end_shape[1:4].tolist(),
                "gyration_components_t300": final_shape[1:4].tolist(),
                "bond_P2_t100": float(start_shape[4]), "bond_P2_t200": float(end_shape[4]),
                "bond_P2_t300": float(final_shape[4]),
                "shape_frames": len(shape), "thermo_records": len(time),
            }
            summary["late_hold_change_from_baseline"] = summary["late_hold_stress_280_lt_t_le_300"]-baseline
            records.append(summary)
            raw[(replica, links)] = {"time": time, "thermo": thermo, "stretches": stretches,
                                     "stress": stress, "baseline": baseline, "shape": shape}
            np.savetxt(args.out/f"shape-rep{replica}-links{links}.csv", shape, delimiter=",",
                       header="time_tau,Gxx_sigma2,Gyy_sigma2,Gzz_sigma2,original_bond_P2,mean_bond_sigma,max_bond_sigma", comments="")
    aggregate = []
    for links in (0, 80, 160):
        group = [row for row in records if row["added_links"] == links]
        row = {"added_links": links, "independent_configurations": 3}
        for key in ("baseline_stress_50_le_t_lt_100", "loading_end_stress_190_lt_t_le_200",
                    "early_hold_stress_200_lt_t_le_220", "late_hold_stress_280_lt_t_le_300",
                    "late_hold_change_from_baseline"):
            values = np.array([g[key] for g in group])
            row[key] = {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)), "values": values.tolist()}
        aggregate.append(row)
    result = {"protocol": "100tau fixed volume preparation; 100tau linear Lx ramp to1.2 with constant volume;100tau hold",
              "stress_definition": "S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma^3; tension-positive normal difference",
              "block_definition": "Loading5tau and holding10tau blocks with intervals(left,right]; shading sample SD across3 configurations, not confidence interval",
              "baseline_definition": "50<=t<100, subtracted separately from each branch for holding-change plot",
              "records": records, "aggregate": aggregate}
    (args.out/"mechanics_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    scalar_keys = [k for k, v in records[0].items() if not isinstance(v, list)]
    with (args.out/"mechanics_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=scalar_keys, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    zh = args.language == "zh"
    tr = lambda c, e: c if zh else e
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in candidates if f in installed] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts, "font.size": 14, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "path", "text.color": "#193d43",
                         "axes.labelcolor": "#193d43", "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    colors = ["#167d84", "#c16b3d", "#466eaa"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}-{args.language}.svg")
        fig.savefig(args.out/f"{name}-{args.language}.png", dpi=180)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.8), sharex=True, constrained_layout=True)
    first = raw[(1, 160)]
    for i, (label, color, ls) in enumerate(zip(("x", "y", "z"), colors, ("-", "-", "--"))):
        axes[0].plot(first["time"], first["stretches"][:, i], label=label, color=color, ls=ls, lw=2)
    for links, color in zip((0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["thermo"][:, 2], 0, 300, 5) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        axes[1].plot(blocks[0][:, 0], avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
        axes[1].fill_between(blocks[0][:, 0], avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
        ax.legend(frameon=False, ncol=3); ax.grid(alpha=.18)
    axes[0].set_ylabel(tr("盒长 / 初始盒长", "Box length / initial length"))
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("温度 T*", "Temperature T*"))
    axes[1].axhline(1, color="#687574", lw=1, ls="--")
    fig.suptitle(tr("先规定形变，再核对温度和体积", "Specify deformation, then check thermal and geometric conditions"), fontsize=18)
    save(fig, "network-deformation")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"], 100, 200, 5) for rep in (1, 2, 3)]
        strain = block_means(raw[(1, links)]["time"], raw[(1, links)]["stretches"][:, 0]-1, 100, 200, 5)[:, 1]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(strain, values[rep], color=color, ls=ls, alpha=.5, lw=1, label=tr(f"构型{rep+1}", f"Config. {rep+1}"))
        ax.fill_between(strain, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(strain, avg, color="#213b40", lw=2.3, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("工程应变 e", "Engineering strain e"))
    axes[0].set_ylabel(tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("加载段：5τ 分段平均与三组构型的离散", "Loading: 5τ block means and variation across configurations"), fontsize=18)
    save(fig, "network-stress-strain")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"]-raw[(rep, links)]["baseline"], 200, 300, 10) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(blocks[0][:, 0]-200, values[rep], ls=ls, color=color, alpha=.5, lw=1)
        ax.fill_between(blocks[0][:, 0]-200, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(blocks[0][:, 0]-200, avg, color="#213b40", lw=2.3)
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].set_ylabel(tr("相对各自静置基线的 ΔS / (ε σ⁻³)", "ΔS from each resting baseline / (ε σ⁻³)"))
    fig.suptitle(tr("固定形变后：10τ 分段平均，阴影为三组间标准差", "Fixed deformation: 10τ blocks; shading is the SD across three configurations"), fontsize=17)
    save(fig, "network-stress-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for links, color in zip((0, 80, 160), colors):
        shapes = np.stack([raw[(rep, links)]["shape"] for rep in (1, 2, 3)])
        time = shapes[0, :, 0]
        for ax, vals in zip(axes, (shapes[:, :, 4], shapes[:, :, 1]/np.sum(shapes[:, :, 1:4], axis=2))):
            avg, sd = vals.mean(0), vals.std(0, ddof=1)
            ax.plot(time, avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
            ax.fill_between(time, avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0); ax.grid(alpha=.18)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
    axes[0].axhline(0, color="#777777", lw=.8, ls="--")
    axes[1].axhline(1/3, color="#777777", lw=.8, ls="--")
    axes[0].set_ylabel(tr("原链键取向 P₂", "Original-chain bond P₂")); axes[0].legend(frameon=False, ncol=3)
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("链尺寸的 x 方向占比 Gxx / tr(G)", "Chain-shape x fraction Gxx / tr(G)"))
    fig.suptitle(tr("从局部键取向到整条原链的形状", "From local bond orientation to whole original-chain shape"), fontsize=18)
    save(fig, "network-chain-orientation")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
```

原始链按镜像标记展开；从保存坐标、盒长与压力计算形状和响应。

### 按样本身份连接结构与机械结果

```
"""Join connectivity, chain geometry and mechanics by matched sample identity.

python study_report.py network-runs --out study --language en
Keep analyze_network.py and analyze_mechanics.py beside this file.
Requires NumPy and Matplotlib; each condition supplies the five records
network.data, relaxed.data, selected-crosslinks.json, thermo.dat and
trajectory.lammpstrj.
"""
from pathlib import Path
import argparse
import csv
import json
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def unique_index(rows):
    keyed = {}
    for row in rows:
        key = (row['replica'], row['added_links'])
        if key in keyed:
            raise ValueError(f'Duplicate sample identity: {key}')
        keyed[key] = row
    expected = {(r, k) for r in (1, 2, 3) for k in (0, 80, 160)}
    if set(keyed) != expected:
        raise ValueError('Expected three preparations with three branches each')
    return keyed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('records', type=Path)
    p.add_argument('--out', type=Path, default=Path('study'))
    p.add_argument('--language', choices=['zh', 'en'], default='en')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    for script, folder in [('analyze_network.py', 'connectivity'),
                           ('analyze_mechanics.py', 'mechanics')]:
        subprocess.run([sys.executable, str(here/script), str(a.records),
                        '--out', str(a.out/folder), '--language', a.language],
                       check=True, stdout=subprocess.DEVNULL)
    graph = unique_index(json.loads((a.out/'connectivity/network_summary.json').read_text())['records'])
    mechanical = unique_index(json.loads((a.out/'mechanics/mechanics_summary.json').read_text())['records'])
    rows = []
    for key in sorted(graph):
        g, m = graph[key], mechanical[key]
        row = {'replica': key[0], 'added_links': key[1],
               'largest_fraction': g['largest_mass_fraction'],
               'component_count': g['component_count'],
               'independent_cycles': g['total_independent_cycles'],
               'winding_rank_largest': g['largest_winding_rank'],
               'modified_bead_fraction': g['modified_bead_fraction'],
               'initial_added_energy_per_bead': g['initial_U_change_per_bead'],
               'late_response_Y': m['late_hold_change_from_baseline'],
               'max_bond': m['max_bond_sigma'],
               'loading_T': m['loading_temperature_mean'],
               'holding_T': m['holding_temperature_mean'],
               'volume_ratio_error': m['max_volume_ratio_error']}
        for time in (100, 200, 300):
            tensor_diagonal = np.array(m[f'gyration_components_t{time}'])
            row[f'fx_t{time}'] = float(tensor_diagonal[0]/tensor_diagonal.sum())
        row['shape_change_after_load'] = row['fx_t200']-row['fx_t100']
        row['shape_change_after_hold'] = row['fx_t300']-row['fx_t100']
        rows.append(row)
    pairs = []
    for rep in (1, 2, 3):
        at = {r['added_links']: r for r in rows if r['replica'] == rep}
        pairs.append({'replica': rep,
                      'dY_160_minus_0': at[160]['late_response_Y']-at[0]['late_response_Y'],
                      'dfmax_160_minus_0': at[160]['largest_fraction']-at[0]['largest_fraction']})
    summary = {'join_keys': ['replica', 'added_links'],
               'shape_definition': 'fx = mean-chain Gxx / sum of mean-chain diagonal G, original 80 chains, equal bead mass',
               'response_definition': 'Y=meanS(280<t<=300)-meanS(50<=t<100), S=-Pxx+(Pyy+Pzz)/2',
               'scope': 'Nine finite-protocol cases; graph descriptors and geometry joined to their own mechanics. No constitutive regression.',
               'records': rows, 'paired_160_minus_0': pairs}
    (a.out/'study_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    with (a.out/'study_conditions.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    zh = a.language == 'zh'
    tr = lambda x, y: x if zh else y
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in available] if zh else ['DejaVu Sans'],
                         'font.size': 14, 'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#faf9f5', 'axes.facecolor': '#faf9f5',
                         'text.color': '#193d43', 'axes.labelcolor': '#193d43'})
    colors = {0:'#167d84',80:'#c16b3d',160:'#466eaa'}
    markers = {1:'o',2:'s',3:'^'}
    def save(fig, name):
        fig.savefig(a.out/f'{name}-{a.language}.svg')
        fig.savefig(a.out/f'{name}-{a.language}.png', dpi=160)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.3), constrained_layout=True)
    for row in rows:
        for ax, key in zip(axes, ['largest_fraction', 'independent_cycles']):
            ax.scatter(row[key], row['late_response_Y'], c=colors[row['added_links']],
                       marker=markers[row['replica']], s=85, zorder=3)
            ax.annotate(str(row['replica']), (row[key], row['late_response_Y']),
                        xytext=(7, 3), textcoords='offset points', fontsize=10)
    axes[0].set_xlabel(tr('最大连通分量珠子占比', 'Largest-component bead fraction'))
    axes[1].set_xlabel(tr('全图独立循环数', 'Independent cycles in the full graph'))
    for ax in axes:
        ax.set_ylabel(tr('后段响应 Y / (ε σ⁻³)', 'Late response Y / (ε σ⁻³)'))
        ax.axhline(0, color='#879793', lw=.8);ax.grid(alpha=.18);ax.margins(x=.15)
    handles = [plt.Line2D([], [], marker='o', color='none', markerfacecolor=colors[k],
                         markeredgecolor=colors[k], markersize=8, label=tr(f'{k} 新增边',f'{k} added links')) for k in (0,80,160)]
    fig.legend(handles=handles, loc='outside upper center', ncol=3, frameon=False)
    fig.supxlabel(tr('点旁数字为制备编号；结构与响应来自同一条件',
                     'Numbers identify preparations; each structure is paired with its own response'), fontsize=12)
    save(fig, 'study-structure-response')
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.8), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.1)
    for rep, ax in zip((1,2,3), axes):
        for row in [r for r in rows if r['replica']==rep]:
            k=row['added_links']
            ax.plot([100,200,300], [row[f'fx_t{t}'] for t in (100,200,300)],
                    'o-', color=colors[k], label=tr(f'{k} 边',f'{k} links'), lw=1.7)
        ax.axhline(1/3, color='#879793', ls='--', lw=.8);ax.grid(alpha=.18)
        ax.set(title=tr(f'制备 {rep}',f'Preparation {rep}'), xticks=[100,200,300], xlabel=tr('记录时刻 / τ','Recorded time / τ'))
    axes[0].set_ylabel(tr('原链尺寸 x 方向占比 fₓ','Original-chain shape fraction fₓ'))
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=3,frameon=False)
    fig.supxlabel(tr('100τ：静置末端；200τ：加载末端；300τ：保持末端',
                     '100τ: end of rest; 200τ: end of loading; 300τ: end of hold'), fontsize=12)
    save(fig, 'study-shape-stages')
    fig, ax = plt.subplots(figsize=(14,6.6), constrained_layout=True);ax.axis('off')
    labels = [tr('制备','Prep.'),tr('新边','Links'),tr('最大占比','Largest frac.'),tr('分量数','Components'),
              tr('循环数','Cycles'),tr('绕行秩','Winding rank'),tr('最大键长/σ','Max bond / σ'),
              tr('Δfₓ (200−100τ)','Δfₓ (200−100τ)'),tr('Y / (ε σ⁻³)','Y / (ε σ⁻³)')]
    cells=[]
    for r in rows:
        cells.append([str(r['replica']),str(r['added_links']),f"{r['largest_fraction']:.4f}",str(r['component_count']),
                      str(r['independent_cycles']),str(r['winding_rank_largest']),f"{r['max_bond']:.4f}",
                      f"{r['shape_change_after_load']:+.4f}",f"{r['late_response_Y']:+.5f}"])
    table=ax.table(cellText=cells,colLabels=labels,cellLoc='center',loc='center',
                   colWidths=[.06,.07,.12,.105,.075,.115,.14,.15,.135])
    table.auto_set_font_size(False);table.set_fontsize(12);table.scale(1,2.35)
    for (i,j),cell in table.get_celld().items():
        cell.set_edgecolor('#e1e7e2')
        cell.set_facecolor('#dfeae6' if i==0 else ('#f4f2eb' if ((i-1)//3)%2==0 else '#faf9f5'))
        if i==0:cell.set_text_props(weight='bold')
    ax.set_title(tr('九个条件保留共同身份，逐项连接结构与力学','Nine identified conditions connect structure with mechanics'),fontsize=17,pad=15)
    fig.supxlabel(tr('Δfₓ为两个保存时刻之差；Y为规定窗口的应力差变化',
                     'Δfₓ compares two saved frames; Y compares the specified stress windows'),fontsize=12)
    save(fig,'study-condition-table')
    print(json.dumps({'conditions':len(rows),'paired_differences':pairs},indent=2))


if __name__=='__main__':
    main()
```

自动运行两份分析，以制备编号和连接数连接，生成九条件表与三幅综合图。

运行脚本按顺序完成三次制备，再生成中英文两套综合图。如果使用已有参考记录，直接运行study_report.py并指向包含三个制备目录的父文件夹即可；每个条件需要network.data、relaxed.data、新增边JSON、thermo.dat和轨迹文件。分析程序使用NumPy处理数值，Matplotlib生成图像，图中文字转为SVG路径，便于离线阅读。两种语言共用相同的分析定义，数值结果应当一致。文件名与目录层级承担样本身份，不依赖个人电脑的绝对位置。

### 完整三制备研究运行脚本

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python study_report.py network-runs --out study/en --language en
python study_report.py network-runs --out study/zh --language zh
```

先运行三套独立制备，再生成两种语言的图；已有参考记录可以直接运行study_report.py。

综合表中的fₓ由八十条原始链的平均G分量计算，是先对链求平均，再将x分量除以三个平均分量之和。它和“逐链计算fₓ后再平均”是两种不同的加权方式：前者会让尺寸较大的链对群体方向占比贡献更多。正文、公式与程序统一采用前者。类似的细节还有循环数统计全部分量、绕行秩报告最大分量，以及Y对每个分支单独减去自己的基线。完整研究需要把这些看似细小的定义留在公式与代码附近，因为它们会改变最后一个数的意义。

一个有用的复现练习是任选一行，例如第一套八十边网络，沿着程序重新得到它的最大分量占比0.7875、循环数十三与后段响应约0.05220。随后把这行与同一制备的零边和一百六十边对应起来，再跨制备比较相同连接数。这个阅读顺序同时保留配对关系和材料条件。研究数据较大时，也可以用完全相同的方法先检查一条可追踪的路径，再让程序批量处理其他条件；每次扩大规模都保留同样的身份与定义。

## 把研究继续推进到具体生物材料

完整案例最有用的产物，不是一句脱离条件的材料规律，而是一套可以继续提问的关系。当前结果清楚展示了连接数增加如何扩大连通分量，也展示了链在加载中的方向变化与有限时间应力的制备差异。如果下一步关注连接安排，可以固定边数并改变近邻选择规则；如果关注网络尺寸，可以增加原始链数并保持密度和链长；如果关注链长，则需要同步考虑松弛时长和缠结相关的动力学尺度。每种扩展都从一个已经定义好的观测问题出发。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/#zh-s8)

图 3 · 含水、纤维弯曲和可逆连接对应不同物理机制；每次扩展保持观测问题与模型条件相连。

若目标是含水凝胶，首先要决定水以什么方式进入模型。显式水允许观察局部水化、离子与溶剂迁移，但需要匹配聚合物—水相互作用并增加计算量；有效介质处理则把部分溶剂影响并入参数和动力学阻尼，适合另一些时间与空间尺度。接着需要规定含水量、是否允许溶胀以及边界怎样交换物质。定体积网络拉伸与可以排水的凝胶实验存在不同约束，比较时应当把相应观测过程写进模拟设计，让模型回答真正关心的物理问题。

若目标是蛋白质或纤维构成的生物网络，连接还可能有方向性，链段可能有显著弯曲刚度，连接寿命可能与受力有关。可以用同样的图分析描述谁与谁相连，但力学模型需要为这些自由度提供相应的能量和演化规则。研究中应保留连接生成与失效的事件记录，再把结构指标与同一时刻的机械变化对应起来。当前固定拓扑案例已经提供了这种组织方式；新增物理机制后，分析所需记录和时间定义也应同步扩展。

材料对比也可以与实验采用共同的可观察量。例如，加载方向的平均应力、保持阶段的时间变化、链或纤维的取向，以及样品体积的变化，都是可以围绕测量条件进行连接的对象。选择其中一个主问题，再决定模型精细程度、体系大小和统计重复，通常比把所有可能指标都计算一遍更容易形成清楚的研究。对当前例题，主线已经明确：先建立连接，再观察几何与受力，最后用配对制备和规定窗口解释差异。下一次研究可以在这个结构上改变一个真正重要的物理环节。

从最初的粒子盒子到这项网络研究，LAMMPS始终在做同一类事情：根据指定相互作用计算力，推进坐标，并记录可以分析的物理量。研究能力来自把模型选择、单位、结构、边界、时间与统计组织成一个相互对应的问题。现在每条新增边都能在连接表里找到，每次形变都能在盒长记录里核对，每个结构指标都对应同一行机械结果。带着这种可追踪的关系继续增加材料细节，计算就能逐渐回答更具体的生物与高分子问题。

## 延伸阅读与开放资料

- [LAMMPS 30 September 2026 Update 1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE珠簧相互作用、约化单位和Langevin积分组合。

  在已验证的1600珠固定网络流程上增加按样本身份连接的结构—力学综合分析；原始动力学与九个条件保持。
- [bond_style fene; special_bonds; read_data](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation; cited for definitions

  FENE能量项、直接成键排斥与数据拓扑定义。

  公式解释、算例与图解独立编写。
- [special_bonds command](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation; cited for command semantics

  fene权重0、1、1及键表对特殊邻居的定义。

  围绕新增连接解释相互作用计数。
- [read_data command](https://docs.lammps.org/read_data.html) · LAMMPS developers · Official documentation; cited for command semantics

  Bonds数据格式和周期贯穿体系的镜像关系。

  原创闭合路线图与周期绕行分析。
- [Molecular Size Distribution in Three Dimensional Polymers. I. Gelation (1941)](https://doi.org/10.1021/ja01856a061) · Paul J. Flory · Research article citation; no original text or image reproduced

  凝胶化与分子尺寸分布的科学史。

  用原创团簇图解释研究问题。
- [Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers (1943)](https://doi.org/10.1063/1.1723803) · Walter H. Stockmayer · Research article citation; no original text or image reproduced

  支化连接与凝胶形成的统计思路。

  历史叙述结合公开学术传记核对。
- [Walter Hugo Stockmayer: A Biographical Memoir (2017)](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf) · Jeffrey Kovac and Marshall Fixman · National Academy of Sciences memoir; citation and paraphrase, no image reproduced

  核对1941—1943年凝胶研究的背景与联系。

  历史信息用于本讲原创概念解释。
- [Dynamics of entangled linear polymer melts: A molecular-dynamics simulation (1990)](https://doi.org/10.1063/1.458541) · Kurt Kremer and Gary S. Grest · Scholarly citation; no original text or image reproduced.

  珠簧模型与高分子熔体动力学的科学史。

  历史概念图独立绘制；本例采用短链固定网络。
