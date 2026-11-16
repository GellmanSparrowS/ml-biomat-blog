# 怎样设计可信的模拟比较

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l15/
Language: zh-CN

从九条网络轨迹中读懂重复、配对与时间相关，让每一根误差条对应明确的测量问题。

## 两条曲线之间，究竟差了什么

把两块橡胶拉到同样长度，其中一块的拉力较大，最自然的问题是它为什么更难拉。也许它的交联更多，也许两块材料原先的链排列不同，也许读数恰好落在不同的波动时刻。分子模拟同样会遇到这些情况。即使输入的温度、粒子数和加载速度完全一样，不同初始排列也会产生不同的瞬时应力。因此，研究材料差别时，需要同时安排改变什么、保留什么，以及怎样把一段运动记录变成一个可以比较的数。这个安排从建立模型时就开始，而不是等画完曲线以后再补上。

本讲沿用由短链熔体建立的三种网络：每个盒子有八十条原始链，每条二十个珠子，共一千六百个珠子；在原有链键之外，分别增加零、八十或一百六十条连接。珠子之间保留排斥作用，连接采用有限伸长的弹簧模型。每种条件都经历一百个时间单位的静置、一百个时间单位的定体积拉伸，再保持形变一百个时间单位，最终伸长比为1.2。这里要回答的是这个具体操作过程中的机械响应怎样比较。温度、密度、链长、拉伸方向和时间安排共同构成问题的条件。

三种连接数各运行一次，能得到三条曲线，但这还没有告诉我们更换初始构型会怎样。本例另外准备三套不同的熔体，每套再分成三个连接数分支，形成九条运行。这样，同一套制备内部的差值关注连接数变化，不同制备之间的差别则反映这套准备与加载流程产生的变动。它很像从三批配制液中各取三份，分别施加三种处理：一批中的样品有共同的起点，批次之间又有自己的差异。保存这种分组关系，后面的统计才会对应真正做过的比较。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s1)

图 1 · 三层身份：独立制备、同一制备内的连接数分支，以及分支内连续保存的记录。

读完本讲，应当能够从一份原始压力记录中计算一个规定时间窗的响应，区分一条轨迹里的时间块与独立制备的重复，读懂标准差和均值标准误，并判断配对比较何时有帮助。Python程序会把九条记录同时读入，直接展示每一次制备的结果，而不是只剩三根平均值柱子。我们也会观察同一条轨迹采用不同分块长度、不同观察窗口时得到什么。这里每个统计量都对应一个清楚的问题，因此数值的大小可以转化为下一步的具体计算安排。

在这个模型中，一条新增连接从建立以后始终存在，热运动使珠子位置改变，却不会让键发生化学断裂。模拟盒中也没有显式水分子。它适合练习固定网络、热涨落与机械加载之间的关系。若研究水凝胶的脱水、可逆键的寿命或组织中的纤维重排，就需要增加相应自由度，再重新安排比较条件。统计方法可以沿用，但所比较的物理对象会改变。先把模型的组成讲清楚，可以让“重复三次”究竟重复了什么变得具体。

## 先找到真正的重复单位

一条轨迹每隔半个时间单位保存一次压力，从零到三百一共得到六百零一行。这些行沿着同一次运动前后相接。上一刻被拉直的链，下一刻很可能仍然较直；一次较大的应力波动也可能持续跨过多个记录。因而，文件里有六百零一行，不等于重新制备了六百零一块材料。行数告诉我们记录有多密，制备次数告诉我们从多少个不同起点重复了整个过程。两者都重要，却承担不同的统计角色。把它们混为同一种样本数，会使平均值看起来比实际更稳定。

本例的独立制备编号为一、二、三。每个编号使用不同的随机种子来生成起始链构型、速度与后续随机过程，并独立完成准备阶段。在同一个编号内，三个连接数分支读取同一个准备后的熔体，初始位置和速度相同；八十条新增边又是一百六十条新增边的子集。这个安排让分支之间具有可追踪的共同背景。因为网络构型相互关联，九条运行应当保留“制备编号、连接数”这两个字段。只把九个文件重命名成一到九，会丢掉比较最有用的结构。

同一制备的三个分支还使用相同的热浴随机种子。这是一种明确的配对安排，能够保留部分共同的随机背景，但粒子轨迹会因为力和连接的变化而逐渐分开。不能只看到“种子相同”就给结果指定一个相关系数；相关性的方向和大小要从配对结果中估计。反过来，独立制备使用不同种子，也不意味着它们一定已经探索到所有慢构象。这里的独立性说的是生成过程的重复方式，长时间构象覆盖则需要结合轨迹长度与结构观察另行判断。

还有一种常见操作是从同一个重启文件启动三条运行，只给热浴换种子。这样的三条轨迹确实会分开，适合观察给定起始网络的动力学变化；它们共享的网络拓扑却没有发生变化。如果问题关注交联形成时的随机连接，就要重新生成连接或重新准备材料，而不仅是换热浴。相应地，从一条蛋白质轨迹抽出很多帧，也不会自动形成很多个独立折叠过程。统计单位取决于想推广到哪一类变化：热运动、网络制备、分子构象，或者不同模型参数。

理解这些层级以后，可以在保存数据时同时保存一张简洁的条件表：制备编号、粒子数、原始链长、新增边数、密度、温度、热浴时间尺度、加载历程和记录间隔。它不需要包含任何个人信息。条件表的作用是让比较双方共享同样的解释：零条新增边的体系仍有原始链键，三百个时间单位包含不同阶段，而一百六十条边也不是一百六十个独立材料样品。名称与数量对应实际对象，后面的平均、相减和误差计算就有了可靠的起点。

增加输出频率与增加观察时间也要分开。把同一段运动每半个时间单位保存一次改成每四分之一个单位保存一次，文件行数接近翻倍，却没有让网络经历更久的松弛。较密记录有利于观察快速波动、准确定位阶段边界，较长轨迹则有机会覆盖较慢的重新排列。两种选择解决不同问题，还会带来不同的存储和计算成本。先看目标观测量变化的时间尺度，再决定保存多密、运行多久以及重新制备多少次，通常比单纯追求数据行数更能改善比较。

## 把运动记录变成一个定义清楚的响应

先决定测量什么，再决定怎样平均。本例读取压力张量的三个对角分量，用负的轴向压力加上两个横向压力的平均值，得到沿拉伸方向的法向应力差S。这样取差会消去三个方向共有的各向同性压力部分，留下与方向差异有关的机械响应。S的单位是能量尺度ε除以长度尺度σ的三次方，也就是这个粗粒化模型的应力单位。它与自由侧面实验中的单独轴向应力有不同的边界条件：这里两个横向盒长随轴向伸长同时缩小，总体积保持固定。

从压力得到法向应力差式 1

![从压力得到法向应力差](https://ml-biomat.com/static/agent-math/b95c88cf7dd466c999a902e1.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| S | 沿x方向相对于横向的法向应力差 | ε σ⁻³ |
| Pₓₓ, Pᵧᵧ, Pzz | 压力张量三个对角分量，正值采用压缩约定 | ε σ⁻³ |
| x, y, z | 加载方向x与两个横向y、z | 1 |
| 2 | 两个横向分量取算术平均的除数 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解应力与压力符号相反；减去横向应力平均值，消去三方向共有的各向同性部分。

算一个例子Pₓₓ=4.8、Pᵧᵧ=5.0、Pzz=5.2时，S=−4.8+(5.0+5.2)/2=0.3ε/σ³。

使用条件本例定体积、周期盒的压力张量；后续比较使用同一个S定义。

瞬时S可以在正值与负值之间波动。为了比较加载后的变化，我们为每条分支先计算静置后段50≤t<100的平均值，再计算保持阶段后段280<t≤300的平均值，后者减前者定义为响应Y。静置窗口有一百条记录，保持窗口有四十条记录，分别覆盖五十和二十个时间单位。基线相减使每个分支的响应相对于自己的加载前状态表达，减少初始残余应力对比较的直接影响。它仍然是规定流程中的有限时间测量，窗口位置本身也是测量定义的一部分。

时间平均与基线响应式 2

![时间平均与基线响应](https://ml-biomat.com/static/agent-math/333c1f430f749ce967898b0e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| W, j ∈ W | W是选定记录集合；j是其中一条记录的编号，∈表示属于 | 1 |
| nW | 窗口内等时间间隔记录数 | 1 |
| Sⱼ, S̄W | 单条记录的应力差及窗口算术平均 | ε σ⁻³ |
| Σ | 把窗口内所有记录的S相加 | 求和运算符 |
| Y | 保持窗口平均减去同一分支静置窗口平均 | ε σ⁻³ |
| hold, rest | hold为280<t≤300；rest为50≤t<100，t以τ计 | 1 |
| 1, overbar | 1为取倒数的分子；横线表示平均 | 1 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解等间隔记录具有相同时间权重；保持平均减去加载前平均，使响应相对于各分支自身基线表达。

算一个例子保持段S为0.2、0.4，平均0.3；静置段为0.1、0.2，平均0.15；Y=0.3−0.15=0.15ε/σ³。实际窗口分别有40与100条记录。

使用条件等间隔保存；窗口端点与本文代码一致。Y是有限加载流程的响应。

平均值的计算并不复杂：把窗口里所有S相加，再除以记录数。由于本例等时间间隔保存数据，每行权重相同。若保存间隔不等，就需要根据各段代表的时间考虑加权，不能把稀疏和密集记录直接混在一起。窗口端点同样值得明确：50≤t<100包括50而不包括100，280<t≤300包括300而不包括280。把时间数组与这些条件一起写进程序，可以让记录数自动检查，避免一条分支多取一帧、另一条少取一帧而无人察觉。

例如第一套制备中，零条新增边的基线约为0.06928，后段Y约为−0.04163；一百六十条新增边的基线约为−0.009295，后段Y约为−0.04285。两个Y都为负，说明所选保持后段的平均S低于各自的静置窗口平均值。它并不要求整个加载过程中应力始终为负，也不等同于材料具有负的弹性模量。读数是两个带涨落的时间平均之间的差，必须放回实际的加载、保持与参考窗口中理解，不能只根据符号给材料贴标签。

程序同时保留早、中、晚三个等长保持窗口，分别为200<t≤220、240<t≤260和280<t≤300。主比较使用事先定义的最后一个窗口，另外两个帮助观察时间位置的影响。三组窗口都减去同一个分支基线，所以它们相互之间也共享信息。如果把其中看起来最符合预期的一个挑出来作为唯一结果，测量问题便随着结果改变了。更清楚的做法是先说明哪一个窗口承担主问题，再把其余窗口作为时间敏感性的图放在旁边。

## 同一制备内相减，再比较三次制备

现在把每条轨迹缩成了一个Y，但不要急着把同一连接数的三个Y分别平均。对于零边和一百六十边的比较，可以先在每套制备内部做一次相减：一百六十边的Y减零边的Y，得到配对差d。这样，第一套与第一套比较，第二套与第二套比较，第三套与第三套比较。共同起点的信息保留在每个差值里。最后再平均这三个d，得到配对差的平均值。配对没有增加材料数量，它改变的是利用已有关系的计算方式。

每次制备内的配对差式 3

![每次制备内的配对差](https://ml-biomat.com/static/agent-math/5f63f5f2493fe77c68012208.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| r, R | r为独立制备编号；R为独立制备数，本例R=3 | 1 |
| 0, 160 | 新增边数标签，零边仍有原始链键 | 1 |
| Yᵣ,₁₆₀, Yᵣ,₀ | 同一制备的两个分支响应 | ε σ⁻³ |
| dᵣ, d̄ | 单次制备的配对差及跨制备平均差 | ε σ⁻³ |
| Σᵣ₌₁ᴿ, 1/R | 从第1到第R套相加，再除以制备数 | 求和与平均 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解先在同一制备内相减，保留共享起点的关系；再对独立制备取平均。

算一个例子三个实际d约为−0.001216、0.122640、−0.073884，相加后除以3，d̄≈0.015846ε/σ³。

使用条件同一编号内两分支具有相同准备起点与测量定义；不同制备独立生成。

### 九条运行与三个配对差

线连接同一制备的分支；右侧保留三个差值，误差条为平均值±配对差样本标准差。

LAMMPS 30 Sep 2026 Update 1；官方珠簧相互作用模型，1600个珠子、80条20珠链，ρ*=0.85、T*=1，三个初始构型；FENE/WCA正式动力学时间步0.005τ。

[下载参考数据与完整输入（ZIP） 0.41 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-comparison-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s4)

同一制备的0、80和160连接分支按身份相连；保留三组160减0配对差及其符号。

实际三个配对差约为−0.00122、0.12264和−0.07388，平均值约为0.01585，单位均为ε/σ³。第一组很接近零，第二组为正，第三组为负。把这些点全部画出来，比只给平均值更能说明这组计算：不同制备在该有限时间流程里产生了明显不同的差值。图左侧把同一制备的三个连接数连起来，线段用于追踪配对身份；它并没有假设八十边处的变化必然位于另两个结果之间。原始点、分组关系与均值应当一起阅读。

配对为什么有时能使差值更稳定？想象两把尺子都在一间温度稍有变化的房间里测量，温度引起的共同偏移可能在相减时抵消。网络分支也可能共享某些由初始排列带来的高低变化。不过，这只是理解协方差的类比：实际两个分支的响应也可能朝相反方向变化，配对差反而更分散。协方差描述两种响应是否倾向一起高、一起低，相关系数则把这种共同变化除以两边各自的标准差，变成−1到1之间的无量纲数。

配对中的共同变化式 6

![配对中的共同变化](https://ml-biomat.com/static/agent-math/51fa93bc2ac864e337046973.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| A, B | 每次独立制备的一对响应；本式B是响应标签，分块公式中的B表示块数 | ε σ⁻³ |
| Ā, B̄ | 对R次制备取平均的响应 | ε σ⁻³ |
| σA, σB | 两侧响应总体标准差；此处σ带下标，不是模型长度单位σ | ε σ⁻³ |
| ρ | 同一制备内A与B的总体相关系数，−1≤ρ≤1 | 1 |
| R | 相互独立的配对制备数 | 1 |
| Var, σA², σB² | 方差及两侧标准差的平方 | ε² σ⁻⁶ |
| ρσAσB | 协方差，表示两侧共同变化 | ε² σ⁻⁶ |
| 2 | 展开差值平方时出现的两个交叉乘积 | 1 |
| ² | 自乘得到平方 | 运算符 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解展开(B−A)的平方产生负的交叉项；不同配对制备独立，使平均差方差再除以R。

算一个例子交互设置σA=σB=1、R=4。ρ=0时方差为0.5，SE=√0.5≈0.7071；ρ=0.5时方差为0.25，SE=0.5；ρ=−0.5时SE≈0.8660。

使用条件同分布的独立配对制备、有限方差。交互采用已知总体参数；实际数据使用样本估计。

配对方差解析模型：两侧总体标准差均为1个应力单位。调节总体相关系数与独立制备数。

[Figure: 均值标准误比较](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s4)

交互中的相关系数是解析模型的已知参数；实际配对响应的关系由记录估计。

交互图把两侧单个制备响应的标准差固定为一个应力单位，调节配对相关系数与独立制备数，查看平均差的理论标准误。相关系数取零时，两侧没有共同变化，配对与非配对表达式给出同样的数；取正值时共同变化部分抵消；取负值时相减会放大变化。这里的相关系数是为理解公式设置的已知参数，实际九条轨迹的相关性则来自数据。将这个解析练习和前面的真实散点放在一起，可以同时理解数学机制与实际研究中的估计问题。

在这三套实际制备中，按配对差计算的均值标准误约为0.05737。如果忽略配对，用两组各自的方差拼出非配对标准误，约为0.07377。两者的差别来自如何处理同一制备内部的共同变化，而不是多运行了模拟。当前三组差值也清楚显示，平均0.01585与组间波动需要一起呈现。下一步若想更稳定地估计这个固定流程下的平均差，可以增加独立制备并延长关键观察窗口，同时继续保持每套制备内部的条件匹配。

## 标准差、标准误与误差条各在说什么

标准差描述一组数本身分散到什么程度。计算时，先用每个数减去这组数的平均值，得到偏差；把偏差平方，避免正负相互抵消；把平方相加并除以重复数减一，最后开平方，使结果回到原来的应力单位。这里减一与用同一组数据估计平均值有关：知道其中两个偏差以后，第三个偏差受“偏差总和为零”的关系约束。三个配对差的样本标准差约为0.09937，它描述的是这三次制备所产生差值的分散程度。

分散程度与平均值精度式 4

![分散程度与平均值精度](https://ml-biomat.com/static/agent-math/8ebe5a076eaa9d9f5046183c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dᵣ, d̄, s_{d} | 单次差值、平均差与配对差的样本标准差 | ε σ⁻³ |
| R, r | 独立制备数与编号，R必须大于1 | 1 |
| SE(d̄) | 平均配对差的标准误估计 | ε σ⁻³ |
| (dᵣ−d̄)² | 偏差平方；上标2表示自乘 | ε² σ⁻⁶ |
| Σ, R−1 | 累加全部平方偏差；用样本估计均值后以R−1归一 | 求和与无量纲除数 |
| √ | 非负平方根，使平方单位回到原量单位 | 运算符 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解标准差描述各差值的分散；独立同分布且方差有限时，平均值方差缩小为原方差的1/R。

算一个例子实际s_d=0.0993668ε/σ³，R=3，因此SE=0.0993668/√3=0.0573695ε/σ³。若s_d=0.1且R=4，则SE=0.05。

使用条件标准差使用ddof=1；SE针对相同准备与加载流程下的平均值。图中误差条标明均值±标准差。

均值标准误关心另一个问题：如果按照相同准备和加载流程，再做很多组包含三次制备的研究，各组平均差会怎样变化？在不同制备相互独立、遵循同一统计生成过程且方差有限的条件下，平均值的方差等于单个差值方差除以制备数。因此，用样本标准差除以制备数的平方根，得到均值标准误的估计。它通常随着独立制备数增加而减小。这里开方很重要：把制备数从三增加到十二，在其他条件相似时，标准误的理论尺度缩小到原来的一半。

把标准差除以根号三，并不会使原来的三次制备更接近。标准差仍然约为0.09937，均值标准误则约为0.05737，它们回答不同问题。图中的误差条采用均值加减组间标准差，目的是让三次制备的分散程度与单独点对应起来。若换成标准误，图注就应明确标成标准误；若进一步构造置信区间，还要给出区间方法、假设与重复数。看到一个短误差条时，先读清它是什么，比直接把它理解成“结果可靠程度”更有帮助。

这些统计量描述当前模型和计算流程中的变化，模型参数则属于另一个层级。例如将粗粒化珠子的排斥强度、键刚度或热浴阻尼改掉，平均响应可能整体移动；把一百个时间单位的加载延长到三百，也可能改变保持阶段的状态。对这些改变，应当设计新的成组比较，而不是把它们混进同一个“随机误差”数值里。这样做有一个实际好处：如果差异主要来自制备，就增加制备；如果主要来自加载速度，就安排速率系列；如果关心真实材料，则引入实验可对应的参数与观测量。

样本数较少时，保留原始点尤其重要。三个数足以展示一次明确的配对练习，也足以算出平均值和样本标准差；它们对分布形状的描述还很粗。把所有点画出来，读者就能看到平均值由怎样的正负差组成，而不是通过一根对称误差条猜测数据。随着独立制备逐渐增加，再检查结果是否由某一个制备主导、分布是否偏斜，以及同一测量定义下的平均值是否稳定。统计图应当随着实际信息增加而变得更细致，而不是一开始就赋予少量点过于复杂的分布解释。

标准差还可以提供一个数量级练习。若同一流程下配对差的标准差保持在0.1附近，四次独立制备的均值标准误约为0.05，十六次约为0.025。这个估算适合安排计算规模，实际新增制备仍要重新估计分散程度。若一次新制备访问到此前没有出现的网络状态，标准差也可能增大；这时增加重复带来的收获，是对制备分布有了更充分的认识。精度安排应当根据逐步积累的数据更新，而不是把最初三次的标准差当作一个固定材料常数。

## 一条轨迹里的连续记录，怎样分块观察

时间相关并不是分子模拟特有的麻烦。天气、河流水位和细胞运动的连续记录都带着过去的影响。对分子而言，邻近时刻的原子共享位置、速度与周围结构；高分子链的整体方向尤其可能比局部振动改变得慢。1989年，Flyvbjerg和Petersen讨论了相关数据平均值的误差估计，分块方法由此成为理解模拟时间序列的一条重要线索。它的核心直觉是把相邻记录先合成较长片段的平均值，再观察这些片段之间还有多大变化。时间顺序在这一过程中得到保留。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s6)

图 2 · 分块保留时间顺序；分子采样还要关注较慢的构象转换。图中的曲线与链形为概念示意。

把本例一百六十边分支的静置后段取出，每套制备正好有一百条记录。每条记录代表半个时间单位，把相邻两条平均可以得到五十个长度为一个时间单位的块；把相邻十条平均得到十个长度为五个时间单位的块。分块变长时，每个块内部会包含更多共同的运动历史，块与块之间的关联有可能减弱。与此同时，块的数量也减少。二十五个时间单位一块时，只剩两个块，两个平均值之间的偶然接近或远离就会明显影响估计。

按时间连续分块式 5

![按时间连续分块](https://ml-biomat.com/static/agent-math/9272063b38465c5e9be925fa.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n, m, B | 总记录数、每块记录数、块数；本例n=100，m整除n | 1 |
| k, j | 块编号及块内编号，从1开始 | 1 |
| (k−1)m+j | 第k块内第j条记录在原序列中的编号 | 1 |
| S, bₖ, s_{b} | 原始应力差、块均值、块均值的样本标准差 | ε σ⁻³ |
| eB | 分块标准误诊断值 | ε σ⁻³ |
| Σ, √ | 求和与非负平方根；s_b按样本标准差公式计算 | 运算符 |
| =, +, −, /, × | 等于、相加、相减、相除与相乘；相邻量表示乘法 | 运算符 |

怎样理解先把相邻记录平均，再观察块均值之间的变化；块长增加时需同时检查剩余块数。

算一个例子n=100、m=10时有B=10个块，每块长5τ。第一套160边分支块均值SD≈0.139170，因此eB≈0.139170/√10=0.0440094ε/σ³。

使用条件本讲作为块长敏感性诊断；用于时间均值标准误时，需要稳定过程、相对相关时间足够长的块与足够多块。

### 块长与时间平均诊断

三个160边分支在50≤t<100的原始应力与分块SE。长块下剩余块数较少，结合全部曲线判断。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s6)

改变时间块长度，比较每个条件的时间序列误差诊断；时间块与独立制备分别统计。

分块图上方显示三个实际静置应力序列，下方把块均值的标准差除以块数平方根，画成随块长度变化的曲线。如果记录来自稳定状态、块长超过主要相关时间且还保留足够多块，这个量可以帮助估计该时间平均的标准误。当前五十个时间单位的片段则适合直接观察估计怎样随分块改变：第一套制备从单帧时约0.03660变化到十个时间单位块时约0.05093，第三套也有明显变化。曲线揭示记录之间的关系，不能由某一个最低点自动决定最佳块长。

第二套制备在十二点五与二十五个时间单位块长时反而得到较小数值。这种现象并不与相关性的存在矛盾，因为此时分别只有四个和两个块平均值。短记录中的块均值可能碰巧接近，估计本身也会波动。判断较长块是否已经足够，应结合更长轨迹、不同时间段以及多个独立制备，看估计是否在有足够块数的范围内保持稳定。把所有块长结果一起展示，能帮助读者理解为什么分块是一种诊断过程，而不是找到最小误差条的优化任务。

二〇一九年发表的分子模拟采样与不确定度指南把这些问题带到更广的分子研究场景：一个分子可以在某个构象附近频繁振动，却很少访问另一种构象。蛋白质侧链、聚合物折叠和离子配位都可能出现快慢运动并存的情况。因此，压力的分块图平稳时，还可以同时检查链尺寸、取向或配位状态。不同观测量对慢运动的敏感程度不同；给压力选择的块长，也应根据另一观测量的实际时间变化重新检查。

## 观察窗口改变时，问题也要保持清楚

保持盒长不变以后，链段仍在重新排列，热浴仍在交换能量，微观应力继续涨落。于是，保持初期、保持中期和保持后期的平均值可能不同。下面把三套制备分别放在三个面板里，每个面板都显示零、八十和一百六十条新增边在三个二十时间单位窗口中的Y。横坐标标的是窗口中点二百一十、二百五十和二百九十，点之间的线用于连接同一分支的时间观察。三个面板使用相同纵轴范围，让同一应力单位下的变化可以直接比较。

### 同一流程中的观察窗口

每个点是20τ保持窗口均值减去各分支的同一个静置基线；面板分别对应三套独立制备。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s7)

按制备分面，比较保持阶段早、中、晚窗口相对各自静置基线的响应。

第一套制备的一百六十边分支，从早段约0.13283、中段约0.16652变为后段约−0.04285；第二套同样连接数的分支则约为0.08621、0.16222和0.15836。两个例子说明，在当前时长下，不同制备的时间变化并不完全相同。若只挑第一套的中段或第二套的后段，材料比较就会混入不同观察时刻。统一窗口并保留时间敏感性图，能够把这种混合拆开：我们既知道同一时段不同分支怎样比较，也知道同一分支沿时间怎样变化。

基线本身也有波动，并且每个Y都减去了一个估计的基线。因此，误差不是只由保持阶段的四十条记录决定。对于同一分支，三个窗口共享基线，它们之间的差值会消去这一个共同基线；对于不同分支，各自基线的变化仍然参与比较。当前程序直接按完整测量定义计算Y，再在独立制备之间比较它，这样可以把基线与保持段的共同影响保留在每次制备的一个数中。若专门研究单次轨迹的时间平均误差，则需要同时处理两段记录及其可能的时间关联。

若下一步增加计算，应当让新增运行对应一个明确原因。想了解保持后的长时间响应，可以延长保持阶段并保持加载方式相同；想比较加载速率，可以保留最终伸长比，成组改变加载时长；想检验网络制备的波动，可以增加独立熔体及连接实现。把这几项同时改掉，也可以得到一个新的有用流程，但它回答的是整个新流程与旧流程的差异。将每次改变写成具体物理操作，有助于避免把一个更强的信号误归因于某一个没有被单独控制的参数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l15/#zh-s7)

图 3 · 不同变化对应不同计算安排：制备、时间与速率分别设计，使新增证据能回答一个清楚的问题。

生物材料研究尤其需要这样的对应关系。比如两种水凝胶在相同拉伸速度下比较，含水量与交联制备方式都可能影响结果；蛋白质吸附的重复模拟中，初始朝向与表面化学也处在不同层级。可以先用简化模型把统计设计练清楚，再在更具体的模型里保留同样的分组逻辑。对某一个完整的研究问题，结构、动力学和机械读数应当来自同一批有身份的样本。这样既能追踪差异，也能把追加计算集中在真正影响解释的因素上。

## 运行完整比较，并安排下一组计算

下面的生成程序从准备熔体到建立网络、拉伸与保持，保留三个独立制备和每套内部的三个连接数分支。运行目录名直接包含制备编号与连接数。输入采用LAMMPS约化单位，温度为1，数密度为0.85，积分步长为0.005，热浴阻尼时间为1。新增连接只选不同原始链上的邻近珠子，每个珠子最多获得一条新增边，分支在加载前各自完成静置。相同输入中的随机数种子规定了可复现的生成流程，也使分支之间的共同关系能够被检查。

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

每套独立准备后分成三个连接数分支；保持匹配身份、记录输入与数据。

### 第一套80边分支的完整输入

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

生成器在各分支目录写出相应输入，旁边的network.data提供该分支结构；此处展示第一套80边的完整文件。

运行脚本按制备编号一到三依次建立这些目录，再执行完整分析。若已下载参考记录，可以直接把包含三个制备目录的文件夹交给分析程序，不需要重复生成已有的轨迹。分析读取每条分支的thermo.dat，其中时间、温度、总能量与压力分量各占固定列。程序先检查记录数量与时间间隔，再计算S、基线与Y，最后保存每个条件的明细表。这样的顺序让异常输入在计算平均值之前就被发现，也让读者能在CSV中逐行核对图上的点。

### 运行三套制备并生成双语图

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python analyze_comparisons.py network-runs --out comparison/en --language en
python analyze_comparisons.py network-runs --out comparison/zh --language zh
```

在含本节四个文件的目录执行；LAMMPS可通过LAMMPS环境变量指定。

### 完整配对、分块与窗口分析

```
"""Compare independently prepared networks with matched branches.

python analyze_comparisons.py network-runs --out comparison --language en
Each n1600-rep1/2/3/links-0/80/160 folder supplies thermo.dat.
Requires NumPy and Matplotlib. Stress units are epsilon/sigma cubed.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--out', type=Path, default=Path('comparison'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    summaries, blocks, raw = [], [], {}
    windows = [(200, 220), (240, 260), (280, 300)]
    for rep in (1, 2, 3):
        for links in (0, 80, 160):
            p = args.records/f'n1600-rep{rep}'/f'links-{links}'/'thermo.dat'
            a = np.loadtxt(p, comments='#')
            if a.shape != (601, 13) or not np.allclose(a[:, 1], np.arange(601)*.5):
                raise ValueError(f'Unexpected observation grid: {p.name}')
            t = a[:, 1]
            stress = -a[:, 6]+(a[:, 7]+a[:, 8])/2
            rest = (t >= 50) & (t < 100)
            baseline = float(stress[rest].mean())
            hold = []
            for left, right in windows:
                values = stress[(t > left) & (t <= right)]
                assert len(values) == 40
                hold.append(float(values.mean()-baseline))
            summaries.append({'replica': rep, 'added_links': links,
                              'resting_records': int(rest.sum()),
                              'resting_mean': baseline,
                              'early_change': hold[0], 'middle_change': hold[1],
                              'late_change': hold[2], 'records_per_hold_window': 40})
            raw[(rep, links)] = {'time': t, 'stress': stress, 'baseline': baseline}
            # Equal-duration contiguous blocks of the same 50tau resting window.
            # SE is a block-length diagnostic; successive blocks may be correlated.
            if links == 160:
                v = stress[rest]
                for frames in (1, 2, 5, 10, 20, 25, 50):
                    means = v.reshape(-1, frames).mean(axis=1)
                    blocks.append({'replica': rep, 'block_tau': frames*.5,
                                   'blocks': len(means), 'mean': float(means.mean()),
                                   'block_sd': float(means.std(ddof=1)),
                                   'block_SE_diagnostic': float(means.std(ddof=1)/np.sqrt(len(means)))})
    table = {(r['replica'], r['added_links']): r for r in summaries}
    left = np.array([table[(rep, 0)]['late_change'] for rep in (1, 2, 3)])
    right = np.array([table[(rep, 160)]['late_change'] for rep in (1, 2, 3)])
    differences = right-left
    groups = {}
    for links in (0, 80, 160):
        values = np.array([table[(rep, links)]['late_change'] for rep in (1, 2, 3)])
        groups[str(links)] = {'values': values.tolist(), 'mean': float(values.mean()),
                              'sample_sd': float(values.std(ddof=1)),
                              'SE_of_preparation_mean': float(values.std(ddof=1)/np.sqrt(3))}
    result = {'definition': 'Y=meanS(280<t<=300)-meanS(50<=t<100); S=-Pxx+(Pyy+Pzz)/2',
              'replicate_unit': 'Three independently seeded prepared melts; link branches matched within each melt',
              'paired_difference': 'd=Y160-Y0 within each preparation',
              'paired_values': differences.tolist(), 'paired_mean': float(differences.mean()),
              'paired_sample_sd': float(differences.std(ddof=1)),
              'paired_SE': float(differences.std(ddof=1)/np.sqrt(3)),
              'unpaired_SE_formula_on_same_marginals': float(np.sqrt(left.var(ddof=1)/3+right.var(ddof=1)/3)),
              'groups': groups, 'window_means': summaries, 'block_diagnostics': blocks,
              'interpretation': 'Fixed finite-protocol responses. Block-SE curves diagnose the chosen resting window; independent-preparation SE is conditional on this preparation and loading protocol.'}
    (args.out/'comparison_summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    for name, rows in [('comparison_metrics.csv', summaries), ('block_diagnostics.csv', blocks)]:
        with (args.out/name).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    zh = args.language == 'zh'
    tr = lambda a, b: a if zh else b
    available = {x.name for x in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in available] if zh else ['DejaVu Sans'],
                         'font.size': 14, 'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'figure.facecolor': '#faf9f5', 'axes.facecolor': '#faf9f5',
                         'text.color': '#193d43', 'axes.labelcolor': '#193d43'})
    colors = ['#167d84', '#c16b3d', '#466eaa']
    def save(fig, name):
        fig.savefig(args.out/f'{name}-{args.language}.svg')
        fig.savefig(args.out/f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)
    for rep, color in zip((1, 2, 3), colors):
        values = [table[(rep, links)]['late_change'] for links in (0, 80, 160)]
        axes[0].plot([0, 80, 160], values, 'o-', color=color, lw=1.6, ms=7,
                     label=tr(f'制备 {rep}', f'Preparation {rep}'))
        axes[1].scatter(rep, differences[rep-1], color=color, s=65, zorder=3)
    axes[0].set(xlabel=tr('新增边数', 'Added links'), ylabel=tr('后段响应 Y / (ε σ⁻³)', 'Late-window response Y / (ε σ⁻³)'),
                xticks=[0, 80, 160], title=tr('同一制备内连接三个分支', 'Matched branches within a preparation'))
    axes[0].legend(frameon=False, loc='lower center', bbox_to_anchor=(.5, 1.10), ncol=3, fontsize=11)
    axes[1].errorbar(4.3, differences.mean(), yerr=differences.std(ddof=1), fmt='D', color='#193d43', capsize=7,
                     label=tr('均值 ± 组间SD', 'Mean ± between-pair SD'))
    axes[1].set(xticks=[1, 2, 3, 4.3], xticklabels=['1', '2', '3', tr('平均', 'Mean')],
                ylabel=tr('配对差 d / (ε σ⁻³)', 'Paired difference d / (ε σ⁻³)'),
                title=tr('160边减去0边', '160 links minus 0 links'))
    axes[1].legend(frameon=False, loc='lower center', bbox_to_anchor=(.5, 1.10), fontsize=11)
    for ax in axes: ax.axhline(0, color='#8a9390', lw=.8); ax.grid(alpha=.18)
    fig.suptitle(tr('比较单位是三组独立制备', 'The comparison contains three independent preparations'), fontsize=18)
    save(fig, 'comparison-paired')
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), constrained_layout=True)
    for rep, color in zip((1, 2, 3), colors):
        rr = raw[(rep, 160)];mask = (rr['time'] >= 50) & (rr['time'] < 100)
        axes[0].plot(rr['time'][mask], rr['stress'][mask], color=color, lw=1.1, alpha=.85,
                     label=tr(f'制备 {rep}', f'Preparation {rep}'))
        b = [r for r in blocks if r['replica'] == rep]
        axes[1].plot([r['block_tau'] for r in b], [r['block_SE_diagnostic'] for r in b], 'o-', color=color)
    axes[0].set(xlabel=tr('静置阶段时间 / τ', 'Resting-stage time / τ'), ylabel=tr('S / (ε σ⁻³)', 'S / (ε σ⁻³)'))
    axes[0].legend(frameon=False, ncol=3, loc='lower center', bbox_to_anchor=(.5, 1.02))
    axes[1].set(xlabel=tr('连续块长度 / τ', 'Contiguous-block length / τ'),
                ylabel=tr('分块SE诊断 / (ε σ⁻³)', 'Block-SE diagnostic / (ε σ⁻³)'), xscale='log')
    for ax in axes: ax.grid(alpha=.18)
    fig.suptitle(tr('相同50τ窗口：改变分块长度，观察估计怎样变化',
                     'One 50τ window: inspect the effect of block duration'), fontsize=17)
    save(fig, 'comparison-blocking')
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.8), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for rep, ax in zip((1, 2, 3), axes):
        for links, color in zip((0, 80, 160), colors):
            rr=table[(rep, links)]
            ax.plot([210, 250, 290], [rr['early_change'], rr['middle_change'], rr['late_change']], 'o-', color=color,
                    label=tr(f'{links} 边', f'{links} links'))
        ax.set(title=tr(f'制备 {rep}', f'Preparation {rep}'), xticks=[210, 250, 290],
               xlabel=tr('窗口中点 / τ', 'Window midpoint / τ'))
        ax.axhline(0,color='#8a9390',lw=.8);ax.grid(alpha=.18)
    axes[0].set_ylabel(tr('相对静置基线的 Y / (ε σ⁻³)', 'Y relative to resting baseline / (ε σ⁻³)'))
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
    save(fig, 'comparison-windows')
    print(json.dumps({k:result[k] for k in ['paired_values','paired_mean','paired_sample_sd','paired_SE']},indent=2))


if __name__ == '__main__':
    main()
```

读取三个制备下的九份thermo.dat，保存逐分支表、统计表和三幅双语图。

comparison_metrics.csv保存九条分支各自的基线及早、中、晚响应；block_diagnostics.csv保存不同块长下的块数、块均值分散程度与分块标准误诊断；comparison_summary.json则保存三组配对差、均值、标准差及标准误。图像分别展示匹配关系、分块变化和观察窗口变化。中英文图使用同一套数值，只有轴标题与图例语言改变。保留数值表与图的共同生成程序，后续更换窗口或增加制备时，就能重新计算所有相互关联的结果，而不是手动修改某一张图。

练习可以从一项可解释的变化开始：把主响应的保持窗口加宽为260<t≤300，保留静置基线与其余所有条件，再重新计算三个配对差。先预测加宽窗口会怎样影响时间平均的波动，再读取结果，并把新旧窗口同时显示。接着可以增加一个独立制备，检查均值与组间标准差怎样变化。这里真正有价值的练习成果是一张定义清楚的比较表：每一行的样本来自哪里、测量哪一段、进行了何种相减，都能够从输入和原始记录重新算出。

至此，一组材料模拟比较可以由四个相互连接的问题组织起来：模型中改变了什么，哪些运行共享同一个起点，响应是怎样从时间记录中定义的，以及观察到的差异会随制备和时间窗口怎样变化。下一讲把这些统计关系与网络连通性、链取向和机械加载放回同一个完整案例。结构分析将回答哪些链被连在一起，力学分析回答它们在规定流程中怎样响应，而本讲的配对与重复设计负责让这两类信息来自同一组可追踪的样本。

## 延伸阅读与开放资料

- [LAMMPS 30Sep2026 Update1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · LAMMPS source and bundled example: GPL-2.0; retain the distributed licence.

  FENE链与排斥珠子基线。

  保留链模型，使用1600珠子三套制备；新增0/80/160跨链边，定体积拉伸保持并开展配对统计；步长0.005、阻尼1τ、截断精确取2^(1/6)σ。
- [Error estimates on averages of correlated data (1989)](https://doi.org/10.1063/1.457480) · Henrik Flyvbjerg and H. G. Petersen · Scholarly citation; no paper text or figure reproduced.

  相关时间序列与分块误差估计的科学史。

  独立绘制分块概念图，并对本例真实记录采用多个指定块长。
- [Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations (2019)](https://doi.org/10.33011/livecoms.1.1.5067) · Alan Grossfield, Paul N. Patrone, Daniel R. Roe, Andrew J. Schultz, Daniel W. Siderius and Daniel M. Zuckerman · Scholarly citation; original explanations and figures here, no third-party figure reproduced.

  分子采样、相关性与不同观测量的统计含义。

  以九条网络轨迹具体解释独立制备、配对差与时间窗口。
