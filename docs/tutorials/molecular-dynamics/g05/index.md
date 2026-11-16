# 从实验结构到可计算的蛋白质

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g05/
Language: zh-CN

从泛素的分子标签功能出发，读懂序列、坐标与实验记录，明确氢、末端和电荷，再把同一个分子交给GROMACS。

## 从细胞里的分子标签说起

细胞不断制造蛋白质，也不断整理已经损坏、完成任务或需要调整数量的蛋白质。这个过程有些像一座繁忙仓库：货物能否进入某条处理通道，取决于它携带什么标记，以及负责识别的装置能否读懂标记。泛素就是参与这种识别的小蛋白质。它可以通过共价连接附着到其他蛋白质上，多个泛素还可以组成具有不同连接方式的链。其中一些泛素链会参与把目标蛋白质送往蛋白酶体降解，另一些连接形式则参与细胞信号或运输等过程。因此，“泛素是分子标签”是一个有用的起点；进一步理解标签怎样被读取，就要研究它表面的形状、电荷和运动。

这一讲选择游离的泛素单体作为第一种蛋白质模型。它只有76个氨基酸残基，既有折叠紧凑的主体，也有伸向外侧的末端，适合把“组成一条链”与“在空间中形成结构”联系起来。我们先从公开的实验结构1UBQ出发，识别其中的蛋白质、水和原子信息，再给蛋白质建立适合GROMACS计算的化学模型。后续各讲会把同一个模型放进盐水中，观察它的结构变化，并比较独立轨迹的统计结果。这样，文件里的每一个选择都能在后面的运动和测量中找到对应含义。

为什么研究运动以前，值得花一整讲处理初始结构？可以想象，要研究一把折叠伞怎样张开，首先要知道哪些杆件相连、哪些地方是铰链、伞布连接在哪里。仅凭一张照片，能够测量外形，却未必能完整确定机械连接。蛋白质结构文件也包含类似的区别：坐标告诉我们原子当前放在哪里，拓扑告诉我们原子如何连接、带有怎样的电荷和相互作用。把这两类信息配对，才能用上一讲的力学规则计算下一时刻的运动。一个缺失的残基、一个选错的末端状态，都会改变这把“分子折叠伞”的连接或受力。

实验结构1UBQ描述的是晶体中泛素的构象，接下来建立的体系则是水溶液里的游离单体。晶体中的分子排列、实验条件与溶液模型的边界条件有所不同，所以我们会明确保留哪一条链、怎样处理晶体水，以及如何给不可见的氢补充位置。我们关注的是这个具体化学模型在所设环境中的构象和波动。泛素与酶形成共价连接、识别某个底物或参与降解时，还需要把相应伙伴和连接关系加入体系；当前的单体是理解这些复杂问题的一块清楚的基础。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g05/#zh-s1)

图 1 · 1UBQ实验结构：602个蛋白质重原子与58个晶体水氧。Cα连线帮助辨认链的走向；投影用于观察结构整体。

先观察图中的主链走向，再看分布在周围的原子。把视线沿链移动，可以发现“序列上相邻”与“空间中相近”是两种关系：沿链很远的两段，折叠后也可能彼此贴近；链末端则可能伸出主体。这正是蛋白质与一长串独立小分子的区别。它既是一种由重复骨架连接起来的高分子，又是一种沿链安排了不同化学侧基的生物大分子。两种身份共同决定了它的形状，而这张结构图为后面的每一个原子选择提供了直观坐标。

## 读懂一条蛋白质链的化学语言

氨基酸可以先理解为带有共同连接部位、同时具有不同侧基的一组小分子。它们组成蛋白质以后，骨架沿着氮原子N、中心碳原子Cα和羰基碳原子C反复延伸。相邻单元通过肽键连接，留在链里的氨基酸单元称为“残基”。这个词强调它已经参与成链，不是把一个完整、游离的氨基酸直接放在旁边。1UBQ中的残基编号从1到76；编号是沿链的地址，原子名称则是这个地址内部的房间名。比如第3个残基的CA与第4个残基的CA都是中心碳，却是两个不同原子。

侧基从骨架伸向周围，使各个残基具有不同的化学性质。赖氨酸和精氨酸在这里采用带正电的状态，天冬氨酸和谷氨酸采用带负电的状态；亮氨酸、异亮氨酸等残基具有较大的非极性部分。水中的折叠结构涉及这些基团与水、与其他基团之间的共同作用，也受到链连接和可用构象数的影响。把某个残基简单称为“亲水”或“疏水”，有助于初步辨认表面，但真正计算时仍要回到原子电荷、原子类型、几何和整个环境。一个带电侧基还包含碳氢部分，空间朝向不同，就会暴露不同的相互作用区域。

蛋白质图里常见的螺旋、箭头和平滑带状线，是为了帮助人眼识别结构层次。α螺旋表示主链形成的一类局部卷曲排列，β折叠中的箭头强调较伸展链段及其方向，连接这些区域的环则具有其他主链构象。这些图形由原子结构推得，并不会作为额外的“螺旋物体”加入GROMACS。程序处理的依然是原子、连接和势能。把带状图与原子图来回对照很有帮助：前者告诉我们整条链怎样组织，后者让我们看见参与接触的具体原子。

空间距离从坐标计算，所用的几何仍然是熟悉的勾股定理。两个原子的横、纵和高三个方向差值，组成一条空间线段的三个分量；先将各分量平方相加，再开平方，得到线段长度。平方的作用是让不同方向的正负不互相抵消，开平方则把长度平方恢复为长度。在一条尚未经过周期包装的完整蛋白质结构上，这样就能计算相邻Cα之间的间距。后面处理穿过周期边界的轨迹时，要先恢复分子连续性，再沿用同一个距离定义。

由两个原子的坐标计算距离式 1

![由两个原子的坐标计算距离](https://ml-biomat.com/static/agent-math/8f4bea339fd28c77b7cf71d8.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dᵢⱼ | 原子i与j之间的空间距离 | Å或nm，与坐标单位一致 |
| xᵢ, yᵢ, zᵢ; xⱼ, yⱼ, zⱼ | 两个原子沿三个笛卡尔方向的位置分量 | Å或nm |
| i, j | 用于区分原子的编号下标 | 1（无量纲） |
| =, −, + | 等号表示相等；减号计算坐标差；加号将三个平方项相加 | 1（无量纲） |
| ², √ | 平方表示与自身相乘；平方根恢复非负距离 | 平方项为长度²；开方后为长度 |

怎样理解三个相互垂直方向的差值组成空间线段。勾股定理把各分量的平方相加，平方根恢复长度；方向的正负因而不会彼此抵消。

算一个例子若两个原子的坐标差为3、4、0Å，则d=√(9+16+0)=5Å=0.5nm。1UBQ相邻Cα的实际距离约3.759–3.854Å。

使用条件直接用于当前完整的非包装结构。处理周期轨迹时先使分子连续，或按测量问题使用合适的周期距离；相邻Cα距离是跨主链多个键的几何量。

本例相邻Cα的实际间距约为3.759到3.854Å，也就是0.376到0.385nm。它们并不直接由一根共价键相连，中间还经过主链的羰基碳和下一个氮，因此不要把这个距离误当作单根碳碳键长。这个简单测量可以帮助发现显著的链断裂：如果某两个连续编号的Cα相隔很远，就应检查是否缺少中间残基、是否存在编号跳跃，或者是否错误地把两条链拼在一起。它提供的是几何线索，完整的化学检查还要核对每个残基应有的重原子和实际肽键连接。

## 从序列到立体结构：实验怎样补齐这张图

今天打开结构数据库，几秒钟就能看到一个蛋白质模型，很容易忽略其中两种知识曾经需要分别建立：一条链上按什么顺序排列，以及这条链在空间中怎样折叠。20世纪50年代，Sanger和同事通过研究胰岛素的片段，逐步确定了氨基酸顺序和链间连接。这类工作像把一段长句剪成相互重叠的短语，再根据重叠关系恢复原句。关键不在于知道袋子里有多少种字母，而在于确定字母的顺序。序列成为可以逐项核对的化学事实，也让不同蛋白质之间的比较具有明确基础。

知道顺序以后，立体形状仍然需要另一种测量。Kendrew及同事在1958年发表了通过X射线分析得到的肌红蛋白三维模型。早期较低分辨率的电子密度已经能够显示链如何弯曲、折叠以及血红素所在的区域；随着数据和方法改进，1960年的工作把分析推进到2Å分辨率。这里的历史线索很重要：先看见整体折叠，再分辨更细的结构，而不是从一开始就拥有每个原子的清晰照片。结构测定的发展也与计算机处理大量衍射数据的能力相互推动。

[Figure: 蛋白质序列、三维结构与泛素连接的科学史](https://ml-biomat.com/tutorials/molecular-dynamics/g05/#zh-s3)

图 2 · 序列测定、X射线结构分析和泛素连接研究分别回答化学顺序、空间排列与生物学作用的问题。图中的链和连接为概念示意。

X射线晶体学的原始观测是衍射信号。研究者根据这些信号和相位信息构建电子密度，再建立与数据相符的原子模型，并通过精修调整坐标等参数。PDB中的坐标是这一过程得到的结构表达。分辨率可以理解为数据支持区分空间细节的尺度，但“1.8Å分辨率”并不是说每个原子的坐标误差都恰好为1.8Å。不同区域的密度清晰程度、占据状态和局部无序程度可以不同，因此既要读结构整体的分辨率，也要查看局部记录。像地图注明比例尺以后，仍然需要知道某条小路是否实际测绘过。

泛素的生物学历史又提出了一个不同的问题：细胞为什么要消耗能量来有选择地拆解蛋白质？Hershko、Ciechanover、Rose及合作者通过生化分离、重组和标记实验，逐步揭示了泛素参与的蛋白质降解过程。Rose的回顾特别讨论了一个小蛋白质与待处理蛋白质形成共价连接这一发现。它把“分子结构是什么”与“结构参与什么任务”联系起来：泛素既需要保持能够被识别的表面，也需要通过特定部位连接到其他分子。我们选择它进行模拟，正因为一个小而完整的折叠体里已经包含了结构、连接和识别之间的关系。

从这些问题回到计算准备，可以得到一条很具体的工作顺序。先把序列与结构记录对应，确定究竟有哪些残基；再辨认实验模型中较清晰和较不确定的区域；最后选择与研究任务一致的化学状态。在这里，76个残基全部进入游离单体模型，末端保持游离的带电形式。将来研究泛素连接到其他蛋白质的情形时，末端的连接、局部电荷和拓扑都要相应改变。历史所揭示的结构层次，直接变成了今天准备模拟时必须回答的几个问题。

## 把1UBQ中的每一类记录读清楚

打开1UBQ，最先需要核对的是对象数量。这个条目采用X射线晶体学测定，分辨率为1.8Å；我们选择的A链含76个残基、602个蛋白质重原子，另外有58个晶体水氧原子。“重原子”在这里指氢以外的原子，并不是说它们全部属于重金属。原文件中没有蛋白质氢坐标，也没有替代位置标识。602个重原子加上58个水氧构成660条原子记录；而76是残基数，四个数字分别数的是不同对象。把这些层次分开，后面看到1231个蛋白质原子时，就知道新增的是氢，而不是蛋白质突然长出了更多残基。

PDB的传统文本格式按固定列存储记录。原子名称、残基名称、链标识、残基编号、三维坐标、占据率和B因子各有位置。固定列意味着某些空格具有结构含义，读取时不能把整行随意拆成“第几个单词”后就假定所有文件都相同。脚本用字符区间读取坐标，也是为了保留这种约定。坐标采用Å，GROMACS常用的GRO文件采用nm，两者相差十倍。长度单位改变后，体积相差一千倍；因此单位核对是读取结构的一部分，不能等到曲线画出来以后再猜数值是否合理。

占据率描述某个原子位置在晶体结构模型中的占据程度。它通常位于0到1之间，部分占据可以与不同构象、无序或特定实验建模情况有关。B因子则是精修模型中描述原子散射随空间频率衰减的参数，常与热运动和静态无序共同相关，单位是Å²。本例有28个蛋白质原子的占据率低于1，另外29个低占据记录属于水；把二者合并后得到57，但这并不等于“57个蛋白质原子都有问题”。按对象分别统计，才能知道需要进一步观察的是哪一部分。

### 实验结构中的末端特征

从原始1UBQ记录计算每个残基的最小原子占据率与平均重原子B因子；浅色区域为73–76号残基。

GROMACS2026.4；PDB 1UBQ链A、76个残基；AMBER99SB-ILDN与TIP3P。保留602个实验重原子，加入629个氢原子；His68选中性NE2质子化状态，采用带电游离末端。

[下载参考数据与完整输入（ZIP） 0.09 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g05/#zh-s4)

PDB 1UBQ每个残基的最小重原子占据率和平均重原子B因子。阴影对应73–76号残基。占据率描述实验结构模型中的位点占据，B因子描述衍射模型中的位置分散；两条曲线提供末端结构特征的不同线索。

图中可以看到，低占据率集中出现在链的C端，最后几个残基的平均B因子也升高。上图取每个残基中最小的原子占据率，下图取该残基所有重原子B因子的算术平均，因此它们回答的是两个相关但不同的问题。最小值便于发现局部部分占据，平均值便于比较整段结构的精修参数水平。当前模型保留这些末端原子，并把这一局部特征带入后续观察：当末端在溶液模拟中活动较大时，我们会分别讨论实验结构中的无序信息与轨迹里实际计算的位移。

B因子不能直接当作本例分子动力学的RMSF曲线来读。前者来自晶体衍射模型，包含晶体环境、静态无序和精修等因素；后者是在选定轨迹、对齐方式和时间窗口中计算的原子位置波动。二者可以帮助提出同一段链是否较灵活的问题，但比较时要说明对象和测量定义。也不应因为某个末端占据率小于1，就把它的原子质量乘上占据率，或随机删去其中一部分。我们建立的是一个完整泛素分子的化学模型，实验占据率用来理解结构信息的清晰程度，原子质量则来自所选力场的化学定义。

## 选择保留什么，也是在选择研究对象

准备结构时，经常能见到“删除所有HETATM”的简短命令。理解它以前，先要看清HETATM是一类文件记录标签，里面可能包括水、离子、小分子配体、辅因子或经过修饰的残基。对某些蛋白质而言，金属离子或辅因子正是功能中心，删去以后研究对象就改变了。这里的1UBQ组成比较清楚：A链是完整泛素，其他原子记录对应58个水氧。我们的目标是建立游离泛素的水溶液模型，因此选择保留A链全部602个重原子，并在下一讲重新构建体相水环境。

晶体水与后面加入的水，并不是两种化学元素不同的“特殊水”和“普通水”。晶体水指实验结构中能够建模并登记位置的水分子；体相溶剂则是围绕蛋白质、形成模拟环境的大量水分子。保留某个实验水可以为特定口袋提供已知的初始占位，但还需要补氢、选择水模型，并检查它与其他组成是否重叠。本例整体去掉这些晶体水后重新溶剂化，是一个明确的初始条件选择。若研究问题变成某个结合位点里的水是否参与识别，就应专门考虑相应的结构水及其替代模型。

结构完整性还涉及“看起来连续”和“化学上完整”的区别。残基编号1到76都出现，说明没有整段残基在坐标表中缺席；每个残基是否拥有所需的侧链重原子，则要继续按残基类型核对。一个赖氨酸即使保留了主链，缺少侧链末端氮也会影响电荷与接触。pdb2gmx根据所选力场的残基模板检查这些内容，并能按规则补充氢。遇到缺失的重原子或内部残基时，需要先进行相应的结构建模和检查，因为补氢规则并不包含任意缺失环段的空间结构。

本例的相邻Cα距离、完整编号和后续模板匹配一起，构成了互相补充的检查。我们还保留了原子身份与原始坐标之间的对应。GROMACS按照力场规则重新排列原子时，某些名称会变化：这里异亮氨酸的CD1写成CD，C端两个氧写成OC1和OC2。若把两个文件逐行相减，就会把排列差异误认为结构移动。正确的比较方式是先根据残基、化学位置和必要的命名对应找到同一个原子，再换算单位后比较坐标。这和比较两份通讯录时先按姓名配对、再比较地址的道理相同。

在实际生成的模型中，602个重原子都找到了对应，最大坐标差约为0.000866nm。这一差值与GRO把每个坐标写到小数点后三位的舍入精度一致：三个方向各自最多产生约0.0005nm的舍入差，空间距离最多接近这三个差值平方和的平方根。这个结果说明当前转换保留了重原子几何，同时补充了力场所需的氢和名称。到真正执行最小化时，原子位置才会根据势能进行调整；把文件转换与几何松弛分开理解，能让每一步结构变化都找到原因。

## 氢的位置、链的两端和电荷怎样决定

氢原子很轻，在许多常规X射线蛋白质结构中不容易逐个定位；它们对化学却并不次要。一个氮上是否连着氢，会影响它怎样参与氢键；一个羧基是否失去质子，会改变局部电荷。给蛋白质补氢因此包含两件事：确定采用哪一种化学状态，再按相应几何规则放置氢。所谓“质子化状态”，就是讨论这些可获得或失去的质子处于什么位置。溶液酸碱条件与局部环境会共同影响这些状态，而结构文件里的重原子坐标往往只提供其中一部分信息。

泛素的第68个残基是组氨酸，它的侧链包含一个五元咪唑环。环上有两个不同的氮位置，名称ND1与NE2中的D、E属于原子命名层级，数字用于区分位置，并不是电荷数。中性的组氨酸可以把环上的质子放在ND1，也可以放在NE2；两种状态拥有相同的总电荷，却具有不同的氢键供受体排列。两个位置都质子化时，侧链整体通常带正电。对模拟而言，仅仅写“组氨酸中性”还不够，还要决定采用哪个互变异构体。

[Figure: 组氨酸环上氮位置与质子化状态](https://ml-biomat.com/tutorials/molecular-dynamics/g05/#zh-s6)

图 3 · HID与HIE具有相同形式净电荷，但质子位置不同；HIP在两个环氮上都有氢，形式净电荷为+1e。本例选择HIE68。

本例明确选择NE2带氢的中性状态，即AMBER命名中的HIE；GROMACS处理后可能显示为HISE，关键检查是HE2存在而HD1不存在。pdb2gmx也能依据周围几何提出自动选择，但这是根据输入结构和几何规则得到的建议。这里的重原子结构没有直接给出该质子的实验位置，因此我们把HIE作为固定的建模选择，并让命令中的交互选项和最终拓扑共同记录它。若研究涉及His68附近的结合或酸碱变化，可以建立另一个合理状态的模型，按照一致的模拟与分析步骤比较差异。

选择组氨酸状态，观察环上氢位置与侧链形式电荷。

[Figure: 组氨酸环上的氢位置](https://ml-biomat.com/tutorials/molecular-dynamics/g05/#zh-s6)

组氨酸化学状态示意；选择状态会改变应写入拓扑的氢位置与部分电荷。

链的两个末端也需要确定化学形式。当前模拟的是游离泛素，N端甲硫氨酸采用带正电的氨基端，C端甘氨酸采用带负电的羧酸端。链内部的肽键和自由末端具有不同连接，因此末端不能机械照搬内部残基的氢数与电荷。原始PDB已经提供C端的两个氧，力场模板将它们对应到末端羧酸基。将来如果把这个C端连接到另一种分子上，连接原子、失去的氢或其他离去基团，以及相应的电荷分布都要按新的化学拓扑处理。

从原子部分电荷得到净电荷式 2

![从原子部分电荷得到净电荷](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Q | 整个所选分子的净电荷 | e（基本电荷单位） |
| qᵢ | 拓扑中第i个原子的部分电荷 | e |
| N | 所选分子的原子总数；本例为1231 | 1（无量纲） |
| i, 1 | i为求和编号，从第1个原子开始 | 1（无量纲） |
| Σ, = | Σ表示将第1至第N个电荷逐项相加；等号表示相等 | 1（无量纲） |

怎样理解电荷是可相加的量。部分电荷可以不是整数，但完整分子的总和应与所选化学状态相符；空间上分离的正负电荷即使相互抵消，也仍产生局部静电作用。

算一个例子若三个原子的电荷为−0.4e、+0.2e和+0.2e，净电荷为0e。本例1231个原子的实际拓扑求和约3×10⁻¹⁵e，按浮点精度等于0e。

使用条件求和只包含当前分子的原子。本例为固定质子化态和固定部分电荷模型；改变化学状态或共价连接，需要相应的新拓扑。

净电荷是所有原子部分电荷相加的结果，而“净电荷为零”不意味着表面每处都没有电场。本例含7个赖氨酸和4个精氨酸，与5个天冬氨酸和6个谷氨酸的形式电荷相互抵消，两个游离末端的形式电荷也相互抵消，His68采用中性状态。实际拓扑中1231个原子的部分电荷相加约为零，极小的非零尾数来自浮点求和。正负电荷依然分布在不同空间位置，水和离子会感受到这些局部差别。下一讲添加盐时，电中性与盐浓度也会分别核对。

## 完整示例：从结构检查到生成拓扑

下面的程序把前面几个问题变成可重复的检查。它首先按PDB固定列读取记录，再明确选取A链的蛋白质原子，统计残基、水、占据率和相邻Cα距离。程序为这个1UBQ例子写出了预期的602个重原子、76个连续残基和58个水氧，因此输入若换成其他结构，会停下来要求重新设计选择规则。这样的检查把研究对象固定在清楚的范围内。接着输出每个残基的统计表和蛋白质坐标文件，图中的占据率与B因子就从同一份读取结果生成。

### 读取结构、统计残基并核对生成的蛋白质

```
"""Inspect 1UBQ records and, optionally, its generated protein model."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_pdb(path):
    atoms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        record = line[:6].strip()
        if record not in {"ATOM", "HETATM"}:
            continue
        atoms.append(dict(record=record, name=line[12:16].strip(),
                          altloc=line[16].strip(), resname=line[17:20].strip(),
                          chain=line[21], resid=int(line[22:26]),
                          insertion=line[26].strip(),
                          xyz_A=[float(line[i:i+8]) for i in (30, 38, 46)],
                          occupancy=float(line[54:60]), b_A2=float(line[60:66]),
                          element=line[76:78].strip(), line=line))
    return atoms


def protein_topology_atoms(path):
    rows, section = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split(";", 1)[0].strip()
        if line.startswith("["):
            if section == "atoms" and rows:
                break
            section = line.strip("[] ")
        elif section == "atoms" and line and not line.startswith("#"):
            parts = line.split()
            rows.append(dict(index=int(parts[0]), resid=int(parts[2]),
                             resname=parts[3], name=parts[4],
                             charge_e=float(parts[6]), mass_u=float(parts[7])))
    if not rows:
        raise ValueError("The input topology must contain the explicit protein [ atoms ] block.")
    return rows


def read_gro(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    count = int(lines[1])
    return [dict(resid=int(line[:5]), name=line[10:15].strip(),
                 xyz_nm=[float(line[i:i+8]) for i in (20, 28, 36)])
            for line in lines[2:2+count]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdb", type=Path)
    parser.add_argument("--gro", type=Path)
    parser.add_argument("--topology", type=Path)
    parser.add_argument("--output", type=Path, default=Path("inspection"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    atoms = read_pdb(args.pdb)
    protein = [a for a in atoms if a["record"] == "ATOM" and a["chain"] == "A"]
    waters = [a for a in atoms if a["resname"] == "HOH"]
    if len(protein) != 602 or len(waters) != 58:
        raise ValueError("This worked example expects the original 1UBQ: 602 protein atoms and 58 HOH oxygens.")
    if any(a["altloc"] or a["insertion"] for a in protein):
        raise ValueError("Resolve alternative positions or insertion codes explicitly before selection.")
    residues = sorted({a["resid"] for a in protein})
    if residues != list(range(1, 77)):
        raise ValueError("The example requires the continuous chain A, residues 1 to 76.")
    (args.output / "protein.pdb").write_text(
        "\n".join(a["line"] for a in protein) + "\nTER\nEND\n", encoding="utf-8")
    rows = []
    for resid in residues:
        selected = [a for a in protein if a["resid"] == resid]
        rows.append(dict(resid=resid, resname=selected[0]["resname"],
                         heavy_atoms=len(selected),
                         occupancy_min=min(a["occupancy"] for a in selected),
                         b_mean_A2=float(np.mean([a["b_A2"] for a in selected]))))
    with (args.output / "residue_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    ca = np.array([a["xyz_A"] for a in protein if a["name"] == "CA"], float)
    ca_steps = np.linalg.norm(np.diff(ca, axis=0), axis=1)
    summary = dict(pdb_id="1UBQ", source_sha256=hashlib.sha256(args.pdb.read_bytes()).hexdigest(),
                   protein_heavy_atoms=len(protein), residues=len(residues),
                   crystal_water_oxygens=len(waters), alternative_atom_positions=0,
                   protein_atoms_occupancy_below_one=sum(a["occupancy"] < 1 for a in protein),
                   water_atoms_occupancy_below_one=sum(a["occupancy"] < 1 for a in waters),
                   adjacent_CA_distance_min_A=float(ca_steps.min()),
                   adjacent_CA_distance_max_A=float(ca_steps.max()),
                   sequence_counts=dict(Counter(row["resname"] for row in rows)))
    if bool(args.gro) != bool(args.topology):
        raise ValueError("Supply --gro and --topology together for the generated-model comparison.")
    if args.gro:
        gro, top = read_gro(args.gro), protein_topology_atoms(args.topology)
        if len(gro) != len(top):
            raise ValueError("The GRO and explicit protein topology must contain the same atoms.")
        names = {(a["resid"], a["name"]): a for a in gro}
        errors = []
        for atom in protein:
            name = atom["name"]
            if atom["resname"] == "ILE" and name == "CD1":
                name = "CD"
            if atom["resid"] == 76:
                # The terminal carboxylate oxygens were reordered in this model.
                name = {"O": "OC2", "OXT": "OC1"}.get(name, name)
            generated = names[(atom["resid"], name)]
            errors.append(np.linalg.norm(np.array(atom["xyz_A"])/10 - generated["xyz_nm"]))
        his_names = sorted(a["name"] for a in top if a["resid"] == 68)
        summary["generated_model"] = dict(
            protein_atoms=len(top), hydrogen_atoms=sum(a["mass_u"] < 2 for a in top),
            heavy_atoms_retained=len(errors),
            max_heavy_coordinate_rounding_nm=float(max(errors)),
            total_charge_e=float(sum(a["charge_e"] for a in top)),
            his68_has_HE2="HE2" in his_names, his68_has_HD1="HD1" in his_names,
            n_terminal_atoms=[a["name"] for a in top if a["resid"] == 1],
            c_terminal_atoms=[a["name"] for a in top if a["resid"] == 76])
    (args.output / "inventory.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    zh = args.language == "zh"
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, constrained_layout=True)
    x = [r["resid"] for r in rows]
    axes[0].plot(x, [r["occupancy_min"] for r in rows], color="#137b88", lw=2.2)
    axes[0].set_ylabel("残基最小原子占据率" if zh else "Minimum atom occupancy")
    axes[0].set_ylim(0, 1.06)
    axes[1].plot(x, [r["b_mean_A2"] for r in rows], color="#b16b36", lw=2.2)
    axes[1].set_ylabel("平均B因子 / Å²" if zh else "Mean B factor / Å²")
    axes[1].set_xlabel("残基编号" if zh else "Residue number")
    axes[1].set_xlim(1, 76)
    for ax in axes:
        ax.axvspan(72.5, 76, color="#d7bb8d", alpha=.18)
        ax.grid(axis="y", color="#d7dfdd", alpha=.65)
    fig.suptitle("1UBQ：实验结构的局部信息" if zh else "1UBQ: local information in the experimental structure", fontsize=18)
    fig.savefig(args.output / "pdb_inventory.svg")
    fig.savefig(args.output / "pdb_inventory.png", dpi=160)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

读取1UBQ固定列，输出完整蛋白质选择、残基统计表和图；同时提供GRO与TOP时核对原子、电荷与重原子几何。依赖NumPy和Matplotlib。

程序中的xyz_A和xyz_nm在变量名中保留了长度单位。重原子比较时先把原始Å坐标除以10，再与GRO中的nm坐标相减；这样得到的差也自然以nm表示。通过字典按“残基编号、原子名”查找对应，比假定原子行号不变更稳妥。异亮氨酸与末端氧的命名对应在代码中单独写出，作用就是把同一个化学位置连接起来。当前文件不含替代位置和插入编号，因此这些字段若出现，程序会提示先处理相应结构情况，而不会默默选取第一条记录。

实际生成蛋白质模型的命令使用amber99sb-ildn力场与TIP3P水模型。力场名称确定蛋白质残基模板和相互作用参数，水模型选项决定稍后加入的水应按哪套拓扑解释。现在尚未加入体相水，但选项已经为完整体系安排了兼容的组成。命令中的-his要求显式选择组氨酸状态；在本例GROMACS2026.4与该力场的菜单里，输入1选择NE2带氢。对于另一个版本或另一套模板，应该先读实际菜单和生成结果，再使用相应选项，不能把菜单序号当作跨所有软件配置的化学名称。

### 生成明确采用HIE68的蛋白质模型

```
#!/usr/bin/env bash
set -euo pipefail

# Run beside the supplied 1UBQ.pdb and inspect_pdb.py.
python inspect_pdb.py 1UBQ.pdb --output inspection --language en
cp inspection/protein.pdb protein.pdb

# In GROMACS 2026.4 with amber99sb-ildn, option 1 places His68 H on NE2.
printf '1\n' | gmx pdb2gmx -f protein.pdb -o processed.gro \
    -p topol.top -i posre.itp -ff amber99sb-ildn -water tip3p -his

python inspect_pdb.py 1UBQ.pdb --gro processed.gro --topology topol.top \
    --output inspection --language en
```

在具有1UBQ.pdb与inspect_pdb.py的目录中运行。菜单选项1对应本例GROMACS2026.4、AMBER99SB-ILDN的NE2质子化状态；处理后检查实际氢名称。

pdb2gmx产生三个主要输出。processed.gro保存补氢并重新排列后的坐标，topol.top保存蛋白质连接、电荷、原子类型和力场引用，posre.itp列出可在后续平衡阶段启用的位置限制。生成位置限制文件，并不等于从此把蛋白质永久钉住；是否启用要看后续输入是否定义对应选项。这里还没有对蛋白质施加一段动力学，也没有把它调整到溶液平衡。这个阶段完成的是一份结构与拓扑彼此匹配的初始化学模型，下一步才能给它构建环境并进行几何松弛。

### 生成模型的数量与化学状态

GROMACS2026.4采用AMBER99SB-ILDN生成的游离泛素；His68为NE2带氢的中性状态，两个末端带相反电荷。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 保留的蛋白质重原子 | 602 | 1 |
| 生成的蛋白质氢原子 | 629 | 1 |
| 蛋白质总原子数 | 1231 | 1 |
| 蛋白质残基数 | 76 | 1 |
| 所选化学状态的净电荷 | 0 | e |
| 匹配重原子的最大坐标差 | 0.000866025 | nm |

这次实际处理得到1231个蛋白质原子，其中602个是保留的重原子，629个是补充的氢，残基数仍为76。His68具有HE2而没有HD1，N端具有H1、H2和H3，C端具有两个羧酸氧；这些结果与前面的化学选择对应。程序同时输出净电荷和重原子坐标差，让数量检查、化学状态检查和几何检查分别有据可查。这里最值得养成的习惯，是从输入对象追踪到输出对象：每多出一个原子、每改一个名称、每个新文件中的信息，都能用化学或文件规则解释清楚。

## 把准备好的模型接到真正的科学问题上

完成这一讲后，我们拥有一条在化学定义和坐标上相互对应的泛素链。它保留了实验结构给出的折叠形状，补齐所选全原子力场需要的氢，并明确采用HIE68与带电游离末端。这个起点适合继续研究水溶液中的结构保持、末端活动和局部构象波动。它也给后续比较划定了参照：如果改变盐浓度，蛋白质本身的拓扑保持一致；如果研究另一种组氨酸状态，就把该状态作为明确变化，而不是让它混在不同的准备命令里。

可以先给自己提出三个相互连接的问题。折叠主体在观察时间内是否保持相近的整体形状？伸向外侧的末端是否比主体中的某些区域活动更明显？不同初始速度得到的轨迹，在这些测量上是否呈现一致的特征？第一问需要对齐结构后比较坐标，第二问需要定义每个残基的波动，第三问需要重复模拟和统计。它们都比“动画看起来在动”更具体，而且能够沿着同一个案例逐步展开。科学问题越清楚，保存什么轨迹、分析哪些原子、选择多长窗口就越有依据。

也可以反过来检查模型与问题是否匹配。如果问题是泛素在蛋白酶体中的识别，那么游离单体缺少识别伙伴与相应环境，下一步应建立复合物；如果问题是共价连接的形成，则需要能够描述化学反应的模型；如果问题是游离泛素末端在水中的构象分布，则当前模型提供了合适的起点，接下来重点放在采样和分析。这样理解模型范围，会把“还需要什么”转化为明确的建模任务。不同任务对系统组成和方法的要求，本来就是研究设计的一部分。

试着再看一次占据率与B因子图，并把目光移到结构图的末端。实验记录提示哪些区域的结构表达较分散，模拟则将给出特定环境中随时间变化的位置。我们会先加入水和盐，让环境能够与蛋白质交换动量和能量；随后通过最小化消除初始几何接触，再逐步放开平衡阶段的位置限制。每一项操作都服务于同一个目的：让可计算的分子模型与想研究的溶液条件对接，而不是把一张实验结构图直接当作已经平衡的动力学起点。

至此，结构文件里原本密集的字母与数字有了清楚的分工。残基序列定义链的化学顺序，坐标给出初始构象，占据率和B因子帮助阅读实验模型，力场模板把连接与相互作用补充进来，程序检查则确保这些信息确实指向同一个分子。下一讲将在这个基础上建立水盒、加入离子并核对完整体系。到那时，蛋白质不再孤零零地摆在坐标表里，而是处在一个具有明确体积、组成和浓度的溶液模型中。

## 延伸阅读与开放资料

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  结构检查、拓扑生成与溶液准备的教学流程。

  改为1UBQ与AMBER99SB-ILDN/TIP3P，显式记录HIE68及端基；加入原子对应检查与双语解释。
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  从结构到力场拓扑的操作顺序与分子模拟教学背景。

  以泛素贯穿示例，补充实验记录、化学状态与数量检查。
- [1UBQ: Structure of ubiquitin refined at 1.8 Å resolution](https://www.rcsb.org/structure/1UBQ) · S. Vijay-Kumar; C. E. Bugg; W. J. Cook · PDB archive data: CC0; associated publication retains its own terms

  实际结构坐标、占据率与B因子。

  结构数据重新绘图，选取A链，统计局部记录；原始数据保持独立提供。
- [gmx pdb2gmx—GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-pdb2gmx.html) · GROMACS developers · GROMACS documentation terms; factual reference

  残基模板、补氢、组氨酸选项与端基处理。

  用独立叙述解释本例所用命令。
- [1958: Fred Sanger](https://mrclmb.ac.uk/achievements/awards-and-prizes/nobel-prizes/1958-fred-sanger/) · MRC Laboratory of Molecular Biology · Publicly readable historical reference; no image/text reproduction

  胰岛素序列测定的历史事实。

  历史事实重新叙述，配概念图。
- [A Three-Dimensional Model of the Myoglobin Molecule Obtained by X-Ray Analysis](https://www.nature.com/articles/181662a0) · J. C. Kendrew and colleagues · Publisher copyright; factual citation

  1958年肌红蛋白三维模型及结构层次。

  讨论历史事实，使用概念示意图。
- [Ubiquitin at Fox Chase](https://pmc.ncbi.nlm.nih.gov/articles/PMC1187975/) · Irwin A. Rose · Nobel Foundation copyright; publicly readable, factual citation

  泛素连接与蛋白质降解研究的历史问题。

  事实概述；图为分子连接概念示意。
