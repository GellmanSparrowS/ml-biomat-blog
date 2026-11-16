# 从轨迹读懂蛋白质的运动

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g08/
Language: zh-CN

把整体移动、内部形变和局部波动分开，再用一段真实泛素轨迹理解RMSD、回转半径与RMSF。

## 一段分子电影，三种不同的问题

拿起一把折叠伞，沿着桌面移动它、把它转半圈，再把伞面撑开，这三种动作看起来都让伞的位置发生了变化，改变的东西却不一样。前两种动作保留了伞内部各部分之间的距离，第三种动作改变了它的形状。蛋白质在水中也同时发生这些事情：整个分子缓慢移动和转向，内部的环、末端与侧链则各自调整。若把所有坐标变化混成一个数字，就很难知道测到的是分子在水里走了多远，还是它自己的结构改变了多少。轨迹分析的第一步，是把问题说到能选择一种测量方法的程度。

前一讲已经让含76个残基的泛素在水中完成准备，并记录了1 ns的无位置限制运动。本讲沿用其中第一条轨迹。它每隔1 ps保存一帧，从0到1000 ps共有1001帧；时间为0的帧属于生产阶段的起点，前面已经经历了控温和控压准备。我们将用这段记录回答三个问题：蛋白质相对共同的最小化参考结构改变了多少，整个分子的质量分布占据多大的空间，以及链上哪些位置在观察期间活动得更明显。它们分别对应均方根偏差RMSD、回转半径Rg和均方根波动RMSF。

这些读数的用处可以从生物问题出发理解。研究一种突变是否改变某段环的活动，需要知道变化集中在哪里；研究一条链在不同溶液中是否更伸展，需要比较它的空间尺度；研究某个结构在模拟中如何偏离实验出发构象，需要固定参考并追踪结构差异。同一条曲线能够帮助回答的问题，与选择了哪些原子、保留了哪些运动、观察了多长时间直接相关。把测量定义写清楚，后面改变盐浓度、温度或分子组成时，比较才有共同的标尺。

可以把轨迹想成一本按时间排列的立体相册。每页保存原子的位置，但页码本身没有写出“这一页代表一次新的构象”或“这一段已经充分采样”。相邻两页相隔很短，通常会非常相似；有的变化发生在几皮秒内，有的变化需要远长于本例1 ns的时间。我们先学习怎样从每一页中提取可重复的几何读数，再在下一讲讨论这些读数有多少独立信息。这样，几何上的解释与统计上的解释各有清楚的落点。

本讲还有一个实际目标：读者既能使用GROMACS完成标准分析，也能看懂Python怎样从坐标重新计算同一物理量。两条路径采用相同的原子、单位和参考，因而可以相互核对。理解这层关系之后，软件输出中的一个数字就有了可追溯的计算过程，而“画出一条线”也会成为“为一个具体问题建立测量”的自然结果。

保存间隔还决定了这本相册能够显示多快的变化。1 ps间隔足以让我们在本例中观察这些较慢的构象调整，但两个保存时刻之间的所有细节并没有逐一写进XTC。画图程序连接相邻数据点，是为了帮助阅读时间顺序；观看动画时快慢的播放速度，则由显示设置决定。它们都要与模拟实际经过的时间分开。讨论一个运动有多快时，应回到文件中的时间戳和相应分析，而不是用屏幕上看起来的速度作判断。

## 先把跨过边界的蛋白质接回来

周期边界给有限的水盒提供了周围环境，也给轨迹的显示带来一个容易误解的现象。设一条链从盒子的右侧伸出去，文件可能把越界的部分显示在左侧，因为那里是等价的周期映像。屏幕上看起来像两截分开的链，化学拓扑中的键却仍然连着。好比一张世界地图在某条经线上剪开，相邻的两个地点可能落在纸的两端；纸上的距离发生了跳变，地球上的邻接关系没有随之消失。计算分子的形状时，需要先恢复与化学连接一致的那一幅连续图像。

GROMACS的轨迹处理工具可以利用拓扑和盒矢量，使分子在每一帧中保持完整。本例用`gmx trjconv -pbc mol -center`处理生产轨迹，首先选择Protein作为居中对象，然后选择System写出全部原子。恢复完整分子与居中承担不同工作：前者整理跨边界的周期映像，后者把观察对象移到方便查看的位置。写出System使蛋白质、水和离子仍处在同一份轨迹中，后续需要研究溶剂环境时可以继续选择相应原子。

[Figure: 周期边界与完整分子](https://ml-biomat.com/tutorials/molecular-dynamics/g08/#zh-s2)

图 1 · 周期成像示意。沿键连接选择一致的周期映像，可以恢复一条连续分子；居中随后改变整条分子的显示位置。

这一步为什么会影响回转半径？想象两个相邻原子本来只相距0.15 nm，却因为周期显示分别位于盒子的两端。如果直接用文件里的两个坐标求普通欧氏距离，得到的可能是几纳米。质心也会被这种分裂的坐标表示带到错误的位置，整个分子的空间分布看上去突然扩大。先把分子重组完整，再计算内部距离，就能让几何读数与实际连接对应起来。对于本例这种单条、有限长度的蛋白质，拓扑中的分子连接提供了明确的重组依据。

恢复完整分子也要和研究扩散时的连续轨迹区分。蛋白质在水中移动时，质心可能反复穿过盒边界。如果每次都把它搬回盒中央，显示会很清楚，但分子累计走过的距离就被这种坐标处理隐藏了。计算质心扩散需要保留跨边界的连续位移；计算内部形状则希望去掉无关的整体位置。本讲研究的是构象，所以采用完整、居中的蛋白质，再根据指标决定是否进一步旋转拟合。后面遇到运输或扩散问题时，应从保存的原始轨迹重新选择相应处理。

实际操作时，先看轨迹的开始、中间和结尾，通常比直接相信一条平滑曲线更有效。检查链是否连续、是否突然跳成跨盒长线、所选原子数是否稳定，同时确认输出时间仍然从0到1000 ps。对于跨边界共价连接的无限链、多分子复合物和膜体系，重组规则还要服从各自的模型定义。到了核酸和膜的章节，我们会看到这些差异。这里先建立一个清楚的原则：坐标文件中的位置表示，要与正在测量的物理对象保持一致。

## 让两幅结构站在同一个坐标系里

把两张画着相同图形的透明纸叠起来，如果其中一张稍微平移或旋转，图上的点就不能重合。此时逐点测量距离，会把纸张的位置差异也算进去。比较蛋白质的内部形状时，同样需要先让两幅结构站在共同的坐标系里。通常先把两组所选原子的中心移到一起，再寻找一个整体旋转，使对应原子之间的平方偏差总和尽可能小。这个操作保持每幅结构内部的所有距离，所以它能够消除共同姿态的差异，同时保留真正的形变。

结构比较中的这个几何问题，在1976年由Wolfgang Kabsch给出了一个求最佳旋转的解法。他处理的是两个具有对应关系的点集，并允许不同点带有不同权重。今天，比较实验结构、叠合蛋白质构象和分析分子轨迹时，仍然会遇到同一类问题：哪些点应该对应，怎样转动整个对象，才能把形状差别与观察角度分开。历史上的方法之所以能跨越许多应用，是因为它解决了一个清楚的共同几何问题。图中橙色和青色的差异，在整体重叠之后仍保留下来的部分，才进入接下来的内部结构比较。

[Figure: 让结构比较从观察角度中分离出来](https://ml-biomat.com/tutorials/molecular-dynamics/g08/#zh-s3)

图 2 · Kabsch在1976年提出以加权平方偏差求最佳旋转的解法。图示原子对应、整体重叠与残余形变的关系。

对应关系需要由原子的化学身份决定。第10个残基的Cα应当对应参考结构中同一个残基的Cα，而不是空间里恰好离它最近的任意碳原子。若结构经过删残基、改变排序或连接不同分子，必须先建立一致的原子映射。本例从同一拓扑和同一模拟流程得到参考与轨迹，原子顺序保持一致，因此可以直接按索引配对。我们选择主链N、Cα和羰基C，共228个原子作为RMSD的拟合组和测量组；这种选择把注意力放在肽链骨架上，避免所有侧链末端的活动共同主导读数。

拟合组和测量组也可以不同。例如研究蛋白质上伸出的柔性环，可以用较稳定的核心来确定整体姿态，然后在这个坐标系里观察环的运动。这样得到的读数回答“环相对核心怎样移动”。如果改为用整个蛋白质拟合，活动较大的环也会参与决定最佳姿态，核心与环之间的偏差分配就会有所变化。这不是软件前后矛盾，而是测量参照改变了。本讲先把两个组固定为同一主链组，让定义容易检查；以后有明确的局部问题，再据此建立新的原子选择。

四个等质量点的二维对齐算例。先改变整体位置与角度，再拉动右上角，比较三种处理。

[Figure: 四点对齐示意](https://ml-biomat.com/tutorials/molecular-dynamics/g08/#zh-s3)

四点二维几何模型，所有点等权。整体平移与旋转保留点间距离；移动一个点会留下完成拟合之后的形变。

交互中的四个点可以帮助建立直觉。保持局部变形为0，只移动位置或改变旋转角度，原始坐标的均方根偏差会改变，完整拟合后的偏差则回到0。只把中心移到一起时，旋转造成的偏差仍然存在。随后拉动右上角的一个点，完整拟合也会留下非零偏差，因为整体移动无法恢复已经改变的点间距离。这里各点等权，真实蛋白质的计算则会按所选定义使用质量权重。这个小模型把拟合的几何作用单独展示出来，便于理解接下来长公式中的每一个坐标到底经过了什么处理。

## RMSD：相对一幅参考结构改变了多少

完成拟合之后，每个所选原子都有一个相对参考位置的偏移。偏移有方向：有的向左，有的向右。若直接平均这些带方向的差值，两边的移动可能互相抵消，甚至让一个已经明显变形的结构得到接近零的读数。RMSD先把每个偏移的长度平方，再对原子求平均，最后开平方，因而把结构差异汇总成一个非负的长度。平方、平均、开方这三个动作，也正是“均方根”这个名字的来源。

对齐后的质量加权均方根偏差式 1

![对齐后的质量加权均方根偏差](https://ml-biomat.com/static/agent-math/a7ab7931514980b82c13aae2.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| RMSD(t) | 时刻t这一帧相对参考的均方根偏差 | nm |
| t | 保存这一帧的生产时间 | ps |
| i, N | 原子编号与所选原子总数；本例主链组N=228 | 1 |
| mᵢ | 拓扑赋给第i个原子的质量 | u |
| r̃ᵢ(t), rᵢʳᵉᶠ | 经过整体平移与旋转对齐的当前坐标，以及对应原子的固定参考坐标；粗体表示三维向量 | nm |
| Σᵢ₌₁ᴺ | 从原子1到N逐项相加；分母是所选原子的总质量 | 求和运算无单位；分母总质量单位为 u |
| ‖·‖² | 向量长度的平方，即三个坐标差平方之和 | nm² |
| √, /, −, =, × | 非负平方根、除法、减法、定义等号与乘法；开方把均方偏差的 nm² 恢复为 nm | 运算符无单位 |
| mᵢ‖·‖² | 质量乘以该原子的距离平方，为分子中的一项 | u nm² |

怎样理解先去掉共同平移和旋转，再把所有所选原子的偏离合成一个长度。平方使相反方向的位移不会相消，质量权重与本例gmx rms的设置一致。

算一个例子若两个等质量原子在完成相同对齐后，距离各自参考位置分别为0.10与0.20 nm，结果为√[(0.10²+0.20²)/2]=0.1581 nm。这里给出的是对齐之后的距离，不能再把它们当作待拟合的两点坐标。

使用条件固定原子对应、参考结构、拟合组、测量组和权重后比较。本例拟合与测量都用N、Cα、C这228个主链原子，参考是共同最小化结构。

本例采用质量加权，与`gmx rms -mw`的设置一致。N、Cα、C的质量并不完全相同，质量权重使较重原子的偏移在总和中占更大比重；分母再除以全部所选原子的总质量，恢复为可比较的平均。质量单位在分子和分母中抵消，坐标用nm，最后的RMSD也就是nm。若改为所有原子等权，也可以构成有意义的几何指标，但计算和解释都应同步采用这个新定义。尤其在不同分析软件之间对照时，先核对权重，比只比较输出小数位更重要。

参考结构在本讲固定为三条重复模拟共同使用的最小化结构。它是所有分支的同一把尺子，也与生产阶段的第一帧不同。第一帧已经经过100 ps受限NVT和200 ps受限NPT，蛋白质在准备过程中发生了小幅调整，因此它相对这个参考的RMSD约为0.0218 nm，而不是必然从零开始。如果把生产第一帧改为参考，这个起点会变成零，之后整条曲线也会改变。两种做法分别描述相对不同起点的偏离；本课程保留共同参考，便于下一讲比较独立重复。

怎样判断0.15 nm这样的读数意味着什么？先换成常见的结构尺度：0.15 nm等于1.5 Å，但它是228个主链原子经过拟合后的质量加权汇总，不表示每个原子都恰好移动了1.5 Å。少量原子大幅移动，与许多原子小幅移动，可能得到相近的RMSD。一个铰链附近的小转动，也可能让离铰链较远的末端产生较大位移。因此读数需要回到结构上定位，再结合局部接触、二级结构或特定距离，判断变化发生在什么部位。

本例的曲线在前段上升，中间经历更大的偏离，接近末尾又有回落。它保留了时间方向，所以能告诉我们某次改变发生在什么阶段。把整段平均成一个数，可以概括观察窗口的总体偏离，却会遮住这些阶段差异。后面的四面板图将同时保留完整曲线和局部波动信息。对于一个实际研究问题，先看轨迹中发生了什么，再决定需要什么统计摘要，通常比给RMSD寻找一个统一的“合格阈值”更能推进解释。

还可以把参考的作用想成从某个城市出发测量旅行距离。两个不同城市都可能离出发地100 km，但它们彼此未必相邻。同样，两帧具有相同RMSD，并不意味着它们彼此具有相同构象；一条曲线重新回到早先的数值，也需要通过结构叠合或其他特征来判断是否回到了早先的状态。若研究的核心问题是构象之间怎样分组，可以进一步计算帧与帧之间的距离矩阵，再结合具有物理意义的局部变量建立分类。这层几何关系有助于把一维曲线当作有用的摘要，同时保留它背后的丰富结构。

## 回转半径：质量分布在多大的范围里

把一根柔软的电线团成球，再轻轻松开一些圈，电线的总质量没有变，但质量分布的范围变大了。回转半径量化的正是这种空间分散程度。它先找出所选原子的质心，再测量每个原子到质心的距离，按质量加权求均方根。一个原子离质心越远，距离平方越大，对结果的贡献也越明显。与RMSD相比，这里无需另外找一幅参考结构：每一帧都用自己的质心作为中心。

质心与质量加权回转半径式 2

![质心与质量加权回转半径](https://ml-biomat.com/static/agent-math/2b008944c37a86dc9e5d53d2.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| r_{cm} | 这一帧所选原子的质心坐标；cm标记质心 | nm |
| R_{g} | 围绕质心的均方根距离；g标记回转 | nm |
| i, N | 所选原子编号和数量；本例全蛋白N=1231 | 1 |
| mᵢ, rᵢ | 原子i的质量与当前三维坐标 | u; nm |
| Σ, /, −, = | 求和；除以总质量归一化；减去同一帧质心；等号给出定义 | 1 |
| ‖·‖² | 原子相对质心的距离平方 | nm² |
| √ | 非负平方根；对 nm² 开方得到 nm | 运算符无单位 |
| mᵢrᵢ | 质量乘以坐标，是质心分子中的一项 | u nm |
| mᵢ‖·‖² | 质量乘以相对质心的距离平方 | u nm² |

怎样理解质心把整个分子的平移消掉，围绕质心的距离把质量在空间里分散的程度表达出来。旋转不改变这些距离，因此标量Rg不需要先与另一幅结构拟合。

算一个例子两个等质量点在一条直线上，坐标为−1和+1 nm，质心为0，Rg=1 nm。把两点一起移到4和6 nm，质心变成5 nm，Rg仍为1 nm。

使用条件一个完整分子的所选质量分布；周期盒内必须先使分子完整。Rg是分布尺度，不能直接当作分子表面的半径，也不同于整个溶液盒的大小。

质心可以理解为把所有原子的质量集中后，整个物体最容易保持平衡的位置。它不是简单找坐标的中点，因为不同原子的质量可能不同；对于密度均匀、形状对称的物体，质心才会落在熟悉的几何中心。蛋白质由不同元素和空间不均匀的原子排列组成，计算时直接使用拓扑中的质量最清楚。本例选择全部1231个蛋白质原子，包括氢，得到全蛋白的质量加权Rg。水和离子属于周围溶液，参与动力学，却没有加入这个蛋白质尺寸指标。

把一个完整蛋白质整体平移，原子和质心会一起移动，它们之间的距离保持不变；把蛋白质整体旋转，距离也不变。因此标量Rg天然对整体平移和旋转不敏感。我们仍然要先处理周期边界，因为一条被显示在盒两端的链，会把“同一个完整分子”的坐标条件破坏掉。这个区别很实用：Rg不需要和参考结构做姿态拟合，却需要每一帧的分子几何是完整的。不同处理步骤分别解决不同问题，不能因为某个指标对旋转不敏感，就跳过全部轨迹检查。

[Figure: 三种长度，三种测量基准](https://ml-biomat.com/tutorials/molecular-dynamics/g08/#zh-s5)

图 3 · 三种测量的概念对照。RMSD比较对应的参考位置，Rg量化同一帧的质量分散，RMSF比较同一原子在多帧中围绕自身均值的偏移。

“半径”这个名字容易让人想到球面。对蛋白质而言，Rg是质量分布的平均尺度，表面通常并不是以质心为中心的一张球面。两种形状可以有相同的Rg：一团较圆的链和一团稍扁的链，只要质量到质心的平方距离平均相同，读数就相同。若需要分清伸长、扁平和方向性，可以进一步计算惯性或回转张量的主轴；若关心分子能否穿过孔道，则需要比较具体横截面和构象。当前这一标量适合追踪整体紧凑程度的变化，读者可以先用它把尺寸问题独立出来。

在本例中，全窗口Rg平均约为1.19153 nm，保存帧的标准差约为0.00603 nm。相比之下，RMSD在同一窗口内有更明显的阶段变化。这组结果展示了一种常见情形：分子的质量分布范围可以保持接近，同时内部原子相对参考的排布逐渐调整。像一团电线在近似相同的外形内改变缠绕方式，整体大小与局部构造并不是同一个问题。后面的散点图会把同一帧的RMSD与Rg放在一起，让这种差异直接可见。

## RMSF：哪些位置在自己的平均位置附近移动

现在把观察方向从时间轴转到蛋白质的序列。RMSD每一帧给出一个数，适合问整体结构随着时间改变多少；RMSF则对一个原子在许多帧中的位置求统计，适合问链上哪个位置活动更大。可以把它想成拍摄一棵树：先把相机画面中的树干对齐，再观察每根树枝尖端在一段时间内分布于多大的范围。树枝的平均位置给出自己的中心，围绕这个中心的位移幅度反映局部活动。蛋白质的RMSF也是在完成指定拟合之后，围绕每个原子自己的时间平均位置计算。

一个位置的时间平均与均方根波动式 3

![一个位置的时间平均与均方根波动](https://ml-biomat.com/static/agent-math/8030f8d29f932ff6a231f387.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i | 待观察的原子编号；本例每个残基取一个Cα | 1 |
| j, M | 保存帧的编号与总数；本例0–1000 ps共M=1001帧 | 1 |
| tⱼ | 第j帧对应的生产时间，下标j用于区分帧 | ps |
| r̃ᵢ(tⱼ) | 第j帧经过指定整体对齐后的原子坐标 | nm |
| r̄ᵢ | 该原子全部所选对齐坐标的时间平均，上横线表示平均 | nm |
| RMSFᵢ | 原子i围绕自身时间平均位置的均方根位移 | nm |
| Σⱼ₌₁ᴹ, 1/M, −, √, =, × | 对帧求和、等权平均、减去自身时间平均位置、非负平方根、定义等号与乘法；开方把 nm² 恢复为 nm | 运算符和平均权重无单位 |
| ‖·‖² | 该帧坐标相对自身时间平均位置的距离平方 | nm² |

怎样理解先求一个原子在观察窗口内的平均位置，再量化它偏离这个中心的幅度。每个原子得到一个数，按残基排开就能看见局部活动的分布。

算一个例子某个已对齐坐标只沿x变化，连续三帧为−0.10、0、+0.10 nm，其平均为0，RMSF=√[(0.01+0+0.01)/3]=0.08165 nm。这是这三帧的均方位移平均，分母用3。

使用条件本例以76个Cα共同拟合，并在全1 ns窗口计算每个Cα的RMSF。时间窗口或拟合区域改变时，平均位置与读数也随之改变。

本例每个残基选择一个Cα，共76个原子。Cα位于氨基酸骨架上，沿序列每个残基通常都有一个，因而适合作为观察链形状的简洁代表。我们用这76个Cα共同确定每帧的最佳姿态，再计算每个Cα的平均坐标和RMSF。这样，横轴可以直接标成残基编号，纵轴仍然是nm。这里的拟合组与RMSD使用的228原子主链组不同，两者各自对应明确的分析定义；比较同一种指标的不同条件时，再把其定义保持一致。

参考结构在RMSF里帮助确定共同坐标系，而进入波动公式的中心是原子在整段轨迹中的时间平均位置。这个区别可以通过一个简单情形理解：某个原子移动到一个新的位置后，长时间只在新位置周围小幅振动，它相对旧参考的偏差可能较大，但在后面那段时间内的RMSF可以较小。若把移动之前和之后的两段一起纳入平均，RMSF又会增大，因为两个位置都进入同一个分布。因此观察窗口是RMSF定义的一部分，计算时需要把起止时间和拟合方式一并记录。

在本例1 ns窗口内，C端的Gly76和Gly75分别有约0.4845和0.3078 nm的Cα RMSF，邻近的Arg74与Leu73也比多数核心位置更活跃。这条空间分布比一个全蛋白平均值更容易指向下一步观察：回到轨迹中，看末端怎样摆动、与周围水及蛋白质表面保持什么接触。泛素末端是分子的一部分，局部活动可以与主体维持紧凑构象同时存在。读这条曲线时，应把最高点与它的结构位置联系起来，而不是简单把最高点当成整个体系最需要“压住”的位置。

第05讲中实验结构的B因子也涉及位置分布，但它所对应的实验环境、模型拟合和无序贡献，与这段溶液MD轨迹不同。这里得到的是给定力场、温度、溶剂和观察窗口下，经过指定拟合的坐标波动。若要与实验作定量比较，需要把实验可观测量、晶体或溶液环境、时间尺度以及相应理论关系接起来。当前这条曲线首先服务于本次轨迹内部的空间比较，让我们知道后续应该把目光放在哪些残基上。

RMSF描述的是位置分布的宽度，运动的快慢还需要另一类时间信息。一个末端在两个位置之间缓慢切换，与它在相同范围内快速来回移动，可能得到接近的RMSF。区分这两种情况，可以检查所选原子的位移时间序列、接触持续时间或相关函数。这个区别也解释了为什么本讲把局部波动曲线和完整轨迹一起使用：曲线帮助找到活跃的位置，时间记录进一步告诉我们这种活动以什么方式发生。

公式对保存的M帧直接求均方平均，因此分母是M。后面描述一条标量曲线的保存帧标准差时，程序使用样本标准差约定，分母则为帧数减1。这两个统计操作分别服务于已定义的位置波动和曲线分散程度，使用时应跟随各自的定义。更关键的是，相邻帧存在相关性；两种分母的差别都没有替我们计算均值的不确定度。下一讲会用时间分块和独立重复把这个问题继续展开。

## 用完整程序把轨迹变成可读的图

下面的命令把处理顺序写成一个可以完整执行的脚本。输入包括生产拓扑`md.tpr`、生产坐标轨迹`md.xtc`和共同最小化参考`reference.tpr`。TPR提供原子身份与质量，XTC提供按时间保存的坐标。脚本先生成完整、居中的轨迹，再依次调用RMSD、回转半径和RMSF工具。每次选择都在命令附近给出，因而可以清楚地看到哪一组原子参与拟合，哪一组原子进入最终测量。

### 重组轨迹并计算三种运动读数

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python=${PYTHON:-python}
# Run beside md.tpr, md.xtc, and the common minimized reference.tpr.
printf 'Protein\nSystem\n' | "$gmx" trjconv \
  -s md.tpr -f md.xtc -o md-whole.xtc -pbc mol -center
printf 'Backbone\nBackbone\n' | "$gmx" rms \
  -s reference.tpr -f md-whole.xtc -o rmsd.xvg -fit rot+trans -mw
"$gmx" gyrate -s md.tpr -f md-whole.xtc -o gyrate.xvg \
  -sel 'group "Protein"' -mode mass
printf 'C-alpha\n' | "$gmx" rmsf \
  -s reference.tpr -f md-whole.xtc -o rmsf.xvg -res -fit
"$python" analyze_motion.py . --language en --output motion-analysis-en
"$python" analyze_motion.py . --language zh --output motion-analysis-zh
```

在md.tpr、md.xtc、共同参考reference.tpr与analyze_motion.py同一目录运行。先选择Protein居中，再选择System写出完整轨迹；两次Backbone分别指定拟合组和测量组。

两次输入Backbone有不同用途：第一次告诉程序用哪些原子寻找最佳平移与旋转，第二次告诉程序对哪些原子计算偏差。这里两次相同，使RMSD定义保持直接。回转半径命令选择Protein并明确使用质量模式，RMSF命令选择C-alpha、按残基输出并启用拟合。这三个输出的横轴也不同：前两个按生产时间排列，第三个按残基排列。读取文件时保留这种差别，绘图才不会把局部空间分布误画成时间演化。

Python程序先读入同一份TPR与已经处理好的XTC，再用明确的原子名称构造主链组。这里写的是`protein and name N CA C`，以准确对应GROMACS的Backbone组。不同程序对某个方便的组名可能采用略有差别的约定，把组成写出来能减少这种歧义。程序随后检查主链、Cα和全蛋白分别为228、76和1231个原子；若输入换成另一种蛋白质，这些数字需要随模型更新。这样的检查把模型身份与后续计算连在一起，也让原子选择错误更早暴露。

### 从真实坐标复算、核对并绘图

```
"""Read a protein trajectory, recompute structural observables, and plot them."""
import argparse
import json
from pathlib import Path

import MDAnalysis as mda
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_xvg(path):
    rows = [line.split() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith(("#", "@"))]
    return np.asarray(rows, dtype=float)


def fit_positions(mobile, reference, masses):
    """Weighted proper rotation; coordinates are rows, with equal atom order."""
    w = masses / masses.sum()
    x = mobile - np.sum(w[:, None] * mobile, axis=0)
    y = reference - np.sum(w[:, None] * reference, axis=0)
    left, singular_values, right = np.linalg.svd((w[:, None] * x).T @ y)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(left @ right)
    rotation = left @ correction @ right
    return x @ rotation, y


def describe(values):
    return {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)),
            "min": float(values.min()), "max": float(values.max())}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path, help="Contains reference.tpr, md-whole.xtc and XVG files")
    p.add_argument("--output", type=Path, default=Path("motion-analysis"))
    p.add_argument("--language", choices=("zh", "en"), default="en")
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    ref = mda.Universe(str(a.directory / "reference.tpr"))
    traj = mda.Universe(str(a.directory / "reference.tpr"),
                        str(a.directory / "md-whole.xtc"))
    backbone = traj.select_atoms("protein and name N CA C")
    ca = traj.select_atoms("protein and name CA")
    protein = traj.select_atoms("protein")
    assert (len(backbone), len(ca), len(protein)) == (228, 76, 1231)
    ref_bb = ref.atoms[backbone.indices].positions.astype(float) / 10
    ref_ca = ref.atoms[ca.indices].positions.astype(float) / 10
    times, rmsd, rg, fitted_ca = [], [], [], []
    for ts in traj.trajectory:
        bb, target = fit_positions(backbone.positions.astype(float) / 10,
                                   ref_bb, backbone.masses)
        rmsd.append(np.sqrt(np.average(np.sum((bb-target)**2, axis=1),
                                       weights=backbone.masses)))
        xyz = protein.positions.astype(float) / 10
        center = np.average(xyz, axis=0, weights=protein.masses)
        rg.append(np.sqrt(np.average(np.sum((xyz-center)**2, axis=1),
                                     weights=protein.masses)))
        fitted, _ = fit_positions(ca.positions.astype(float) / 10, ref_ca, ca.masses)
        fitted_ca.append(fitted)
        times.append(ts.time)
    times, rmsd, rg, fitted_ca = map(np.asarray, (times, rmsd, rg, fitted_ca))
    mean_ca = fitted_ca.mean(axis=0)
    rmsf = np.sqrt(np.mean(np.sum((fitted_ca-mean_ca)**2, axis=2), axis=0))
    native_rmsd = read_xvg(a.directory / "rmsd.xvg")
    native_rg = read_xvg(a.directory / "gyrate.xvg")
    native_rmsf = read_xvg(a.directory / "rmsf.xvg")
    assert len(times) == 1001 and np.allclose(times, np.arange(1001))
    assert np.allclose(times, native_rmsd[:, 0]) and np.allclose(times, native_rg[:, 0])
    differences = {
        "rmsd_nm": float(np.max(np.abs(rmsd-native_rmsd[:, 1]))),
        "rg_nm": float(np.max(np.abs(rg-native_rg[:, 1]))),
        "rmsf_nm": float(np.max(np.abs(rmsf-native_rmsf[:, 1])))}
    assert differences["rmsd_nm"] < 2e-5
    assert differences["rg_nm"] < 2e-5
    assert differences["rmsf_nm"] < 6e-5  # Native RMSF is printed to four decimals.
    largest = np.argsort(rmsf)[-5:][::-1]
    summary = {
        "n_frames": len(times), "time_ps": [float(times[0]), float(times[-1])],
        "selection_counts": {"backbone": len(backbone), "C_alpha": len(ca), "protein": len(protein)},
        "native_rmsd_nm": describe(native_rmsd[:, 1]),
        "native_rg_nm": describe(native_rg[:, 1]),
        "python_minus_native_max_abs": differences,
        "highest_C_alpha_rmsf": [{"residue": int(ca.resids[i]), "name": str(ca.resnames[i]),
                                  "rmsf_nm": float(rmsf[i])} for i in largest],
        "windows": {str(start): {"rmsd_nm": describe(native_rmsd[(times >= start) & (times < start+200), 1]),
                                  "rg_nm": describe(native_rg[(times >= start) & (times < start+200), 1])}
                    for start in range(0, 1000, 200)}}
    (a.output / "motion_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(a.output / "motion_recomputed.csv", np.column_stack((times, rmsd, rg)),
               delimiter=",", header="time_ps,backbone_rmsd_nm,protein_rg_nm", comments="")
    np.savetxt(a.output / "rmsf_recomputed.csv", np.column_stack((ca.resids, rmsf)),
               delimiter=",", header="residue,C_alpha_rmsf_nm", comments="")
    zh = a.language == "zh"
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [name for name in candidates if name in installed],
                         "font.size": 13, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    fig, axes = plt.subplots(2, 2, figsize=(13.6, 9.8), constrained_layout=True)
    colors = {"teal": "#087f8c", "orange": "#cb6a36", "ink": "#203446"}
    t_ns = times/1000
    axes[0, 0].plot(t_ns, native_rmsd[:, 1], color=colors["teal"], lw=1.3)
    axes[0, 0].set(xlabel="时间 / ns" if zh else "Time / ns", ylabel="RMSD / nm",
                   title="A  主链相对共同参考的偏离" if zh else "A  Backbone deviation from a common reference")
    axes[0, 1].plot(t_ns, native_rg[:, 1], color=colors["orange"], lw=1.3)
    axes[0, 1].set(xlabel="时间 / ns" if zh else "Time / ns", ylabel="Rg / nm",
                   title="B  全蛋白的质量分布尺度" if zh else "B  Mass-distribution size of the full protein")
    axes[1, 0].plot(ca.resids, native_rmsf[:, 1], color=colors["ink"], lw=1.6)
    axes[1, 0].fill_between(ca.resids, 0, native_rmsf[:, 1], color=colors["teal"], alpha=.15)
    axes[1, 0].set(xlabel="残基编号" if zh else "Residue number", ylabel="Cα RMSF / nm",
                   title="C  对齐后的局部位置波动" if zh else "C  Local positional fluctuations after fitting", xlim=(1, 76), ylim=(0, .55))
    for i in (74, 75):
        axes[1, 0].annotate(str(ca.resids[i]), (ca.resids[i], native_rmsf[i, 1]),
                             xytext=(-22 if i == 74 else 6, 8), textcoords="offset points", fontsize=11)
    dots = axes[1, 1].scatter(native_rmsd[:, 1], native_rg[:, 1], c=t_ns,
                               s=13, cmap="viridis", alpha=.8, edgecolors="none", rasterized=False)
    axes[1, 1].set(xlabel="RMSD / nm", ylabel="Rg / nm",
                   title="D  同一帧的形变与尺寸" if zh else "D  Deviation and size in the same frame")
    bar = fig.colorbar(dots, ax=axes[1, 1], pad=.02)
    bar.set_label("时间 / ns" if zh else "Time / ns")
    for ax in axes.flat:
        ax.grid(alpha=.18)
        ax.tick_params(labelsize=11)
    fig.suptitle("泛素 · 0–1 ns 的三种运动读数" if zh else "Ubiquitin · three structural measurements over 0–1 ns", fontsize=19)
    fig.savefig(a.output / "protein_motion.svg")
    fig.savefig(a.output / "protein_motion.png", dpi=155)
    plt.close(fig)


if __name__ == "__main__":
    main()
```

使用MDAnalysis、NumPy与Matplotlib读取1001帧；从TPR取质量，从XTC取坐标，以nm复算三种读数并与GROMACS输出对照。--language zh/en生成对应语言图，JSON与CSV保留相同数据定义。

MDAnalysis读入坐标时以Å表示长度，而本课程和GROMACS的这些输出使用nm，因此程序在进入几何计算前把坐标统一除以10。时间仍以ps读取，绘图时再除以1000显示为ns。拟合函数先减去质量中心，再根据两组中心化坐标求一个保持方向的旋转；其中的修正项使旋转不会变成镜面反射。读者暂时不熟悉矩阵分解，也可以先沿着“取坐标—统一单位—移到中心—寻找整体旋转—计算残余距离”的顺序理解整个函数，再回到四点交互检查几何作用。

程序把逐帧复算值与GROMACS原生XVG逐项对照。RMSD的最大差约为0.00000015 nm，Rg的最大差约为0.0000085 nm；RMSF原生文件保留四位小数，复算与之的最大差约为0.000050 nm。不同算法路径、浮点运算与文本输出精度会留下细小差异，三个量在相同定义下彼此吻合。最终图使用原生读数，CSV保留复算结果，JSON记录原子数量、时间范围和数值比较。这让一个新的数据文件接入后，仍能沿着同样的定义得到可以检查的图与摘要。

这种逐项对照同时检查了坐标单位、原子身份、权重和参考结构。即使图像看起来很平滑，十倍的长度换算错误或意外加入侧链的选择，仍然会改变其中的物理量。把这些条件直接写在代码里，换用另一种分子时就更容易知道哪些部分可以复用，哪些定义需要跟着问题调整。

## 把三种读数放回同一段运动

先看图A，主链RMSD在最初200 ps的平均约为0.0931 nm，在600至800 ps这一段平均约为0.1970 nm，随后又有下降。这里分段采用左端包含、右端不包含的200 ps区间，避免边界帧重复计入两个段；完整曲线仍保留1000 ps末帧。它显示出相对共同参考的偏离程度随时间改变。再看图B，Rg在整个窗口内主要围绕1.19 nm上下波动，变化幅度远小于它的平均尺寸。把两个面板放在同一时间尺度上，就能看到结构排布变化与整体质量尺度变化并没有同步增大。

### 同一段泛素轨迹的四幅读图

副本1的0–1000 ps，共1001帧。RMSD以共同最小化主链为参考；Rg用全蛋白质量；RMSF使用全窗口Cα拟合坐标。散点图以保存时间着色。

GROMACS2026.4；PDB 1UBQ链A、76个残基；AMBER99SB-ILDN与TIP3P。保留602个实验重原子，加入629个氢原子；His68选中性NE2质子化状态，采用带电游离末端。

[下载参考数据与完整输入（ZIP） 129.06 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-motion-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g08/#zh-s8)

同一条1 ns轨迹的主链RMSD、全蛋白质量回转半径、Cα的RMSF，以及按时间着色的RMSD–Rg散点。主链RMSD以共同最小化结构为参考；RMSF先拟合各帧，再围绕每个Cα的窗口平均位置计算。

图C把时间信息压缩到每个Cα的位置分布中，末端73至76位的升高很醒目。它提供了一个具体观察方向：在RMSD较高和较低的阶段分别看末端位置，同时查看主体是否维持原有的接触与骨架排列。要进一步判断末端对总体RMSD贡献多大，可以按预先选定的核心重新拟合，或把全链与去掉末端的测量并列比较。每一步都需要保留相应的选择定义；这样得到的是对空间贡献的分解，而不是通过换原子组去寻找更好看的数值。

图D为每个保存帧画一个点，横轴是该帧的RMSD，纵轴是同一帧的Rg，颜色表示时间。靠右的点表示它相对参考偏离更大，靠上的点表示质量分布更分散。颜色让我们看到不同阶段在这张图上的位置，也能找出两个指标并不同步的时刻。例如一段较大的参考偏离可以仍对应接近原来的Rg，而末尾一些尺寸稍大的构象又可能有较小的RMSD。散点与时间曲线互相配合，能把“某个数字变大了”推进为“哪个几何特征在什么时候改变”。

下面的轨迹按20 ps间隔展示这段记录中的51幅Cα构象。画面沿用RMSD的主链拟合参照，便于把某个时间点与上面的曲线对应起来。可以先暂停在较早的构象，再拖动到约700 ps附近观察末端和主体的相对变化；随后回到末尾，查看RMSD下降时各个部位怎样重新排列。显示中减少了原子数量，完整1231原子的质量仍用于上面的Rg计算。

### 在同一参照里观察泛素运动

副本1的51幅真实Cα构象，每20 ps一帧。以228个主链原子质量加权拟合共同参考，查看局部形变与曲线的对应。

接下来若研究温度或突变的影响，最有用的是先写下同样清楚的比较方案：采用哪一幅共同参考，哪些原子用于拟合，哪些原子用于测量，使用多长的观察窗口，以及需要多条怎样独立开始的轨迹。对于本例，1 ns记录已经足以展示多种几何指标的区别，并揭示这条轨迹里的末端活动与整体形状调整。更慢的环区交换、远离初始构象的转换和长期分布，需要在相应时间尺度上继续观察。把问题的时间尺度与轨迹的时间尺度连接起来，才能决定下一次计算怎样增加有效信息。

读完这段分析，再回头观看分子动画，通常会看到更多内容：一段看似剧烈的运动，可能主要来自整体旋转；一段外形近似不变的运动，内部却可能持续调整；一条末端的摆动，也可能在残基图上留下十分明确的峰。动画负责帮助我们发现和定位现象，几何读数负责在固定定义下比较它们。下一讲将沿着同一组数据进一步追问：这些保存帧彼此有多相似，换一组初始速度后会得到怎样的曲线，以及怎样把有限记录组织成更可靠的比较。

## 延伸阅读与开放资料

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  蛋白质轨迹的周期处理、RMSD、回转半径与原子选择流程。

  改为泛素1UBQ，明确质量权重与共同参考，补入RMSF、Kabsch几何、独立坐标复算与双语多面板图。
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  蛋白质水溶液模拟后的构象分析。

  围绕三种不同测量基准展开，并用2026.4实际轨迹演示。
- [gmx rms — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-rms.html) · GROMACS developers · GROMACS documentation terms; factual reference

  参考结构、质量权重与拟合选项。

  结合本例选择、单位与完整算例说明。
- [gmx rmsf — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-rmsf.html) · GROMACS developers · GROMACS documentation terms; factual reference

  拟合后的位置波动定义。

  结合本例选择、单位与完整算例说明。
- [gmx gyrate — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-gyrate.html) · GROMACS developers · GROMACS documentation terms; factual reference

  质量加权回转半径及当前命令。

  结合本例选择、单位与完整算例说明。
- [A solution for the best rotation to relate two sets of vectors](https://doi.org/10.1107/S0567739476001873) · Wolfgang Kabsch · Publisher copyright; factual historical citation

  1976年加权最小平方结构对齐问题。

  以纸上图形和四点交互解释几何问题，配结构比较概念图。
