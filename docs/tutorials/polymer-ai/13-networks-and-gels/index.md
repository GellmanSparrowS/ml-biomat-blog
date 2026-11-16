# 高分子网络与凝胶：交联、贯通和弹性

Source: https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/
Language: zh-CN

[下载代码合集 ↓](https://ml-biomat.com/static/tutorials/polymer-ai/polymer-ai-notebooks.zip)

从含水长链到可以学习的力学网络

杨云浩 · 复旦大学 · 高分子与生物大分子教程

一碗水会随容器改变形状，一块含有很多水的果冻却可以被切开、拿起，还会在轻碰后晃动。水没有突然变成硬材料，变化发生在水中的长链之间：一些连接把它们组织成能够共同响应变形的网络。研究这种结构，可以帮助我们理解食品的口感、软组织的支撑，以及怎样设计含水又有一定承载能力的生物材料。本节把这个问题交给物理计算和AI共同处理：先分清网络是否贯通，再预测它受到指定变形时需要多大的力。

[《分子怎样聚到一起：自组装、相分离与凝聚体》](https://ml-biomat.com/tutorials/polymer-ai/12-assembly-and-phase-separation/)讨论了分子在空间中怎样富集。现在把目光移到富集区域内部：即使有同样多的长链、同样多的连接，连接的位置也可能让样品表现完全不同。可以想象两张用相同数量绳子编成的网，一张把上下两端连在一起，另一张的绳子集中在两个互不相连的半边。计数相同，力却找不到相同的传递路线。这样的差别，正适合用图来表示，也为图神经网络提供了具体的科学任务。

## 01水留在网络里，长链开始共同响应

凝胶可以从两个相互穿插的部分理解：一部分是保持连接的网络，另一部分是充满其中的流体。水凝胶里的流体主要是水，网络则可以由柔性高分子链、蛋白质纤维或其他构件形成。水分子仍然能够运动，许多小分子也能在其中扩散；网络让整个样品在一定观察时间内具有弹性响应。于是，“能保住形状”与“内部存在流动和交换”可以同时发生，这也是含水软材料很有用的原因。

把凝胶想成浸在水中的渔网，可以先理解连接的作用，但真实凝胶通常没有肉眼可见的网孔。长链之间的间距可能远小于我们能直接看见的尺度，网络自身还会热运动、变形和重新结合。水也不是被一道密封外壳关在里面：它与长链混合，受到分子相互作用和溶液条件影响，并与外部水交换。网络限制长链无限分散，混合与弹性共同决定最后吸进多少水。

以海藻酸盐为例，它是一类由糖单元连接而成的多糖，其中不同糖醛酸单元的排列影响与离子的结合。某些连续的古洛糖醛酸单元能够参与钙离子的协同结合，使不同链上的局部区域靠近并形成连接区。这里的“交联”就是在原有长链骨架之外，增加把不同链或不同链段联系起来的约束。交联点之间的一段链仍然能够弯曲，但它的两端已不能随意独立地游走。

1973年，Grant等人提出描述海藻酸盐离子凝胶的[“蛋盒”模型](https://doi.org/10.1016/0014-5793%2873%2980770-7)；同年的[圆二色性研究](https://doi.org/10.1039/C39730000245)把古洛糖醛酸片段的配位与溶胶—凝胶转变联系起来。这个比喻来自链段提供的配位空间：钙离子像放在凹槽里的物件，帮助相邻链形成连接。它把看起来突然发生的“液体成胶”，拆成了可以研究的糖单元排列、离子结合和链间组织。

1973 · 从海藻酸盐的离子结合理解成胶

[Figure: 蛋盒模型研究思路的原创示意。绿色为糖链，棕色标出离子或连接区；末图蓝点表示网络中的水。局部配位与整体网络属于不同尺度。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-alginate)

[Figure: 蛋盒模型研究思路的原创示意。绿色为糖链，棕色标出离子或连接区；末图蓝点表示网络中的水。局部配位与整体网络属于不同尺度。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-alginate)

**图1** 蛋盒模型研究思路的原创示意。绿色为糖链，棕色标出离子或连接区；末图蓝点表示网络中的水。局部配位与整体网络属于不同尺度。

蛋盒图中的圆点不意味着每个糖单元都按同一比例绑定钙离子，也不意味着所有多糖的连接区完全相同。后续的[X射线衍射研究](https://pubmed.ncbi.nlm.nih.gov/17291070/)继续检查钙—海藻酸盐的链间结构。学习这个例子时，最有用的是建立一条因果线：局部化学结构决定有哪些结合方式，许多结合区组织成网络，网络再影响宏观变形。把这三个层次保留下来，才方便将生物化学信息接入材料预测。

蛋白质和核酸也能形成网络。蛋白质可以通过化学交联或局部结合区连接，纤维之间还可以建立接触；核酸则能利用互补片段组织连接。它们的共同点是构件之间形成了约束，但约束的寿命、方向性和强度不同。一个稳定的共价连接与一个能够反复解离的结合位点，在短时间的轻微拉动中可能都能传力，在较长时间的持续加载下却可能出现不同的松弛。

因此，记录一种凝胶时，需要同时写下构件、连接机制和观察时间。例如，在同样的小变形下记录刚加载时的力，再记录保持位移后的力如何变化，就能区分即时响应与后续松弛。若连接持续交换，网络可能慢慢改换形状；若水需要经过较长距离才能流出，尺寸也会影响响应时间。后面关于真实使用过程的一节会进一步研究这些变化，本节先固定连接，专门看结构与小变形响应的关系。

这也决定了AI数据表不能只填“是否加了交联剂”。相同加入量可能形成不同数量的有效连接，还可能改变离子条件、混合过程和局部聚集。实验研究可以分别记录配方与制备条件、结构表征、测试几何以及加载程序，再用相应证据构造预测目标。本节采用可直接检查每一条边的计算网络，让“谁与谁相连”成为明确输入，为以后处理实验中间接观察的网络打下基础。

## 02从几条连接，走到跨越样品的路径

把交联区域画成节点，把节点之间的链段画成边，就得到一张网络图。节点可以代表许多原子共同形成的连接区，边也可以代表一段较长的分子链，因此图的尺度由研究问题决定。若研究离子怎样配位，需要保留更细的化学结构；若研究载荷怎样跨越样品，可以把局部连接区合并成节点。这样的简化称为粗粒化，其价值在于保留当前问题真正需要的关系。

先数每个节点连着几条边，这个数量叫节点的**度**，记为zᵢ，下标i是节点编号。求全网平均度时，每条边会在两个端点各被数一次，所以全部度数之和等于边数的两倍，再除以节点数就是平均度。它像一张交通图上“每个路口平均有几条路”：数字相同的两张图，仍可能一张能从城南走到城北，另一张被分成几片。平均度概括局部连接的多少，是否贯通还要沿连接实际走一遍。下面的物理计算与图模型会分别利用这两类信息。

连接数量提供第一幅概貌

平均度z̄=(Σzi)/N=2M/N。N为节点数，M为无向边数，zi为节点i连接的边数；每条边贡献两个端点。

N表示节点总数，M表示无向边总数，本节的图没有节点连向自己的自环。假设N=16、M=32，平均度就是2×32/16=4。两张图都可以拥有这个平均值：一张在中间保留上下相连的边，另一张把连接集中在上、下两块。前者可能让路径跨越整个样品，后者则可能分成两个独立部分。后面的实际计算会保留相同的32条边，直接展示这项差别。

从一个节点沿边走，可以到达的所有节点组成一个连通分量。判断上下是否贯通，只需从底部节点开始，把它们能到达的邻居加入待访问清单，再依次访问新邻居；若最终到达任意顶部节点，就存在一条底到顶的路径。这相当于在地图上沿现有道路找路线。道路的编号、画在纸上的角度以及橡皮筋有多硬，都不改变路线是否存在，前提是连接关系本身没有变化。

还要区分贯通路径与网络中的其他部分。有些链段只有一端接在主网络上，另一端自由摆动，称为悬垂链；有些连接绕一圈回到已有区域，形成环。悬垂链与局部环都占用了材料，也能影响局部运动、溶胀和耗散，但它们对指定方向的整体承载未必与横跨两个区域的链段相同。把所有加入的链都直接计成有效承载链，会忽略网络结构中的这种分工。

Flory在[1941年的支化聚合研究](https://doi.org/10.1021/ja01856a061)中，从连接和分子大小分布分析凝胶化。其启发是：大量局部反应怎样累积成跨越体系的巨大结构，可以用分支增长来理解。设一种理想构件有f个可连接位点；沿一条已形成的连接走到它以后，有一个位点已被来路占用，还剩f−1个可能的出口。若每个出口独立地以概率p继续连接，平均可延伸出的新分支就能算出来。

1941 · Flory把分支增长与凝胶化联系起来

[Figure: 从来路、后续分支到带环网络的概念图。临界分支公式采用无环树状近似；程序中的有限图直接使用邻接关系判断贯通。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-branch)

[Figure: 从来路、后续分支到带环网络的概念图。临界分支公式采用无环树状近似；程序中的有限图直接使用邻接关系判断贯通。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-branch)

**图2** 从来路、后续分支到带环网络的概念图。临界分支公式采用无环树状近似；程序中的有限图直接使用邻接关系判断贯通。

理想分支何时从有限团簇走向大网络

无环树状分支近似中，后续平均分支数b=p(f−1)，临界占用概率pc=1/(f−1)。f为每个构件的可连接位点数，p为其余位点各自形成连接的概率。

b表示到达一个新构件后平均产生的后续分支数，f和p都没有单位。b小于1时，分支平均逐代减少；b大于1时，理想无限树中出现持续延伸分支的可能性。令b=1，便得到临界值p_{c}。例如f=3时，p_{c}=1/2：若其余两个出口各有40%的连接概率，平均后续分支数是0.8；若为60%，则变为1.2。减去的那个1有明确来由，它对应已经用于到达该构件的位点。

这个推导采用相同反应机会、独立连接和不形成闭环的树状近似，并以很大的体系讨论阈值。有限网络中的环会让某些新连接回到已访问区域，空间拥挤也会改变相遇机会。因此，真实体系或具体模拟需要按自己的结构重新判断贯通。本节程序直接搜索每个有限图的路径；它按给定边数抽取连接，并未按照上式的独立位点占用概率生成网络。两个计算各自回答清楚的问题。

从AI的角度，连接数量是最简单的输入，平均度、度的分布和连通分量数量则提供更多结构线索。更进一步，可以把完整邻接关系交给模型，让它自己学习哪些局部连接组合与贯通有关。不过，图搜索已经能够精确回答这个小图的贯通问题；在这里训练分类器，是为了学习怎样组织结构输入、标签与评价。随后预测力学响应时，同一张图还必须增加方向、刚度和边界信息，研究任务随之变得更丰富。

## 03连通以后，还要看网络怎样承受变形

拿四根细杆，用可以自由转动的接头连成方框。它的上下当然相连，但用手轻推上边，方框可以歪成平行四边形。若在对角线上增加一根斜撑，同样的推法便需要拉伸或压缩连接。这解释了一个关键区别：存在路径，意味着能沿连接走到另一端；产生指定方向的线性刚度，还要求这种位移必须付出弹性代价。接头的转动、纤维的弯曲和原有张力都会影响实际材料的表现。

先为“有多硬”选一把明确的尺子。设一个厚度为H、受剪面积为A的均匀样品，底面固定，顶面横向移动δ。位移相对于厚度的比例叫剪切应变γ，维持这个位移的力F除以面积叫剪切应力τ。在足够小的变形下，应力与应变近似成正比，它们的比值是剪切模量G。直接用力除位移，则得到整个样品的刚度K，两者通过样品几何联系起来。

把样品刚度与材料模量区分开

小剪切应变γ=δ/H，剪切应力τ=F/A，剪切模量G=τ/γ；样品刚度K=F/δ=GA/H。H为初始厚度，A为受剪面积，δ为顶面横向位移，F为维持位移的剪切力。

γ没有单位，τ和G的单位是帕斯卡，即牛顿每平方米；K的单位是牛顿每米。取H=2毫米、A=1平方厘米、δ=0.1毫米、F=0.01牛顿，先统一成米和平方米，得到γ=0.05、τ=100帕，因而G=2000帕，K=100牛顿每米。若材料相同而厚度加倍，简单均匀剪切条件下样品刚度会减半。由此可见，比较两个力—位移曲线之前，样品尺寸应与曲线一起记录。

柔性链网络还把前面学过的熵弹性带到了整体材料中。单条链被拉开时，可选构象减少；许多链段的端点由交联区域约束，就会共同对宏观变形作出响应。在理想的仿射高斯链网络中，小剪切模量可以写成下面的形式。“仿射”表示各连接点跟随均匀宏观变形移动，“高斯链”表示链段尚处在相应的柔性统计近似内。这些条件把单链的构象统计接到了宏观弹性。

许多链段的熵弹性，合成整体响应

理想仿射高斯链网络中G=νe kBT。νe是单位当前体积中有效承载链段的数密度，kB为玻尔兹曼常数，T为绝对温度。

ν_{e}是单位体积中有效承载链段的数目，单位为每立方米；k_{B}T是热能，单位为焦耳。两者相乘得到焦耳每立方米，正好等于帕斯卡。在T=300开尔文、ν_{e}=10^{24}每立方米时，取k_{B}=1.380649×10^{−23}焦耳每开尔文，得到G约为4142帕。这里的链段数对应网络中参与弹性响应的部分，不能简单用配方里加入的分子总数代替。

这个关系给出固定网络状态下的理想尺度，帮助理解为什么增加有效连接可能提高弹性。把一个已制备凝胶放入不同溶液后，吸水会改变体积、链的伸展和参考状态，离子条件也可能改变连接。因此，跨越不同溶胀状态预测模量时，需要把这些变化一起纳入自由能和结构模型。[Flory与Rehner在1943年对网络弹性的研究](https://doi.org/10.1063/1.1723791)及其[溶胀研究](https://doi.org/10.1063/1.1723792)，正是把网络约束与溶剂作用联系起来的历史路径。

1978年，Tanaka在[聚丙烯酰胺凝胶研究](https://doi.org/10.1103/PhysRevLett.40.820)中观察到，改变温度或流体组成可以使凝胶发生体积塌缩，并研究了相平衡中的临界端点。这里的实验对象是合成凝胶，却提供了理解含水网络的重要思路：网络弹性和混合倾向共同决定体积，外部条件改变时，平衡体积也可能显著改变。生物大分子凝胶还可以具有电荷与可逆结合，研究时继续加入相应的贡献。

1943—1978 · 从网络溶胀到凝胶体积转变

[Figure: Flory–Rehner的网络与溶剂思路，连接到Tanaka对合成凝胶体积塌缩的研究。轮廓与趋势线用于解释变量关系，未复刻实验数据。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-swelling)

[Figure: Flory–Rehner的网络与溶剂思路，连接到Tanaka对合成凝胶体积塌缩的研究。轮廓与趋势线用于解释变量关系，未复刻实验数据。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-swelling)

**图3** Flory–Rehner的网络与溶剂思路，连接到Tanaka对合成凝胶体积塌缩的研究。轮廓与趋势线用于解释变量关系，未复刻实验数据。

现在把问题收缩到能逐条检查的计算对象：一张二维、没有初始张力的轴向弹簧网。每条边只能沿自身初始方向伸缩，模型中没有弯曲能；固定边界后，让内部节点找到能量最低的位置。这个模型专门展示连接位置、几何方向和加载方向如何共同决定小变形刚度。它与上面的三维熵弹性表达式有不同的自由度和单位，程序输出以弹簧常数k₀为单位的样品刚度。

设节点i和j分别移动了向量u_{i}与u_{j}，两者相减得到相对位移。把它投影到原来连接的方向上，就得到一阶近似的轴向伸长。方向用单位向量n_{ij}表示，长度为1。这里的点积可以理解为沿着弹簧方向量一量两端相对拉开多少；与初始方向垂直的微小位移，在这个一阶表达式中没有贡献。

连接的方向决定哪些位移会拉长它

小位移下连接ij的轴向伸长Δℓij=nij·(uj−ui)。nij为初始连接方向的单位向量，ui和uj为两个节点的位移向量，点积只保留沿原连接方向的分量。

以向右上方倾斜45度的连接为例，n_{ij}=(1/√2,1/√2)。若上端相对下端向右移动0.01ℓ₀、竖直方向不动，那么轴向伸长为0.01ℓ₀/√2，约0.007071ℓ₀。ℓ₀是所选长度单位。对一条竖直连接，同样的横向相对位移与其方向垂直，一阶轴向伸长为0。这就是方框与斜撑差别的计算入口：不同方向的边，会把同一次位移投影成不同的伸长。

弹簧的能量等于弹簧常数乘伸长平方的一半。把每条边的贡献相加，再让没有被固定的内部节点自由调整，网络就会选择总能量最低的位移。这个过程好比在固定边缘的网中允许内部结点稍稍让位，找到彼此拉力平衡的位置。程序把问题写成线性最小二乘，保留那些不产生轴向能量的运动模式；不会为了得到一个正数而额外加入不存在的弹簧。

力学标签来自独立的能量最小化

U=(1/2)Σ边kij(Δℓij)²；固定边界位移后，让自由节点位移使U最小。小变形线性加载刚度K=2Umin/δ²=F/δ。kij为轴向弹簧常数，E是边集合；F为加载方向的边界合力。

E是所有边的集合，k_{ij}是第ij条边的弹簧常数，单位为力除以长度；U是能量。符号min表示在给定边界位移下，调整自由节点位移寻找最低值。线性模型的最低能量随加载幅度δ的平方变化，因此写成U_{min}=Kδ²/2，移项便得到K=2U_{min}/δ²。对δ求导可得维持位移的力F=Kδ，能量法与边界反力法于是给出相同的K。

对于边长ℓ₀的方框，底部两个节点固定，顶部两个节点都向右移动δ，所有弹簧常数取k₀。四条外边的一阶轴向伸长都为0，所以线性剪切刚度为0；增加一条45度斜撑后，它的伸长为δ/√2，能量为k₀δ²/4，于是K=k₀/2。这是可以手算核对的完整例子。真实方框在较大变形下会出现几何变化，而这里计算的是未变形状态附近的线性响应。

给方框加一根斜撑，再换一个加载方向

上下是否贯通**是**刚度 K / k₀**0.000**能量 U / (k₀ℓ₀²)**0.000000**

[Figure: 底边固定的方框，顶边向右位移；未加斜撑时线性剪切刚度为零](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#gel-network)

四条外边形成贯通方框；在零预应力、无弯曲能的线性模型中，横向剪切刚度为0。

**图4** 边长ℓ₀、每条边的弹簧常数k₀，底部固定，顶部另一方向的位移为0。动画在小位移范围内往复显示一系列加载状态，可随时暂停；它展示准静态线性模型，绿色位移放大12倍。关闭脚本时保留方框剪切的静态示意与数值。

交互中的拉伸选项把顶边位移改为竖直方向。此时两条竖边直接伸长，没有斜撑的方框也得到K=2k₀；加入斜撑后为2.5k₀。连接关系没有变，响应却随加载方向改变。由此还能理解，某个方向上K大于0，只说明该边界条件下存在恢复力；若要判断网络对其他变形的约束，必须继续检查那些运动方向。后面的模型会把加载方向作为力学预测的输入。

## 04让AI沿连接交换信息

在前面的糖链学习中，我们已经用过局部连接特征。这里进一步让模型直接沿网络的边交换信息。想象每个结点拿着一张记录卡，上面写着自己的位置、边界身份和连接数量；它从相邻结点收集记录，结合连接方向与弹簧常数，更新自己的卡片。重复几轮后，每张卡片便包含周围一片网络的信息。图神经网络中的消息传递，就是将这种局部汇总过程写成可训练的数值运算。

Scarselli等人在[2009年的图神经网络论文](https://doi.org/10.1109/TNN.2008.2005605)中系统讨论了如何用神经网络处理图结构，以及面向节点和整张图的预测。它的重要出发点是输入本身带有关系：分子键、区域邻接或网络连接都应参与计算。本节采用三层前向消息传递作为教学实现，让网络的连接决定信息从哪里来，再用训练数据调整如何组合这些信息。

2009 · Scarselli等人系统讨论图神经网络

[Figure: 图结构、节点状态更新与整图预测的原创概念图。本节使用三层前向消息传递，贯通和加载响应分别训练，各自使用与目标相符的输入。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-ai)

[Figure: 图结构、节点状态更新与整图预测的原创概念图。本节使用三层前向消息传递，贯通和加载响应分别训练，各自使用与目标相符的输入。](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/#history-ai)

**图5** 图结构、节点状态更新与整图预测的原创概念图。本节使用三层前向消息传递，贯通和加载响应分别训练，各自使用与目标相符的输入。

需要训练的两个任务各自保留一套模型。第一个预测底到顶是否贯通，输入为邻接关系、节点的底部或顶部身份及节点度。几何坐标、弹簧常数和加载方向在这个任务中设为0，因为它们不会改变既定图的路径。第二个预测指定加载下的刚度，保留完整几何、弹簧常数与加载方向。这样，标签定义与模型能读取的信息相互对应，也方便检查同一网络改变加载后，哪些预测应该改变。

力学任务为每个节点记录七个数：二维坐标、是否属于底部、是否属于顶部、二维加载方向，以及除以8后的节点度。这里8是所用方格邻域中可能的最大邻居数，起到缩放作用。每条有向消息还带四个边属性：初始方向的两个分量、连接长度和弹簧常数。从j看向i与从i看向j时方向相反，长度和弹簧常数相同；同一条无向物理边因此产生两个方向的信息传递。

模型先把七维输入转换成24个可学习的内部数值，形成节点状态向量h_{i}。这24个数是用于预测的表示，它们的含义由训练共同决定。对于每一层，模型用同一套规则处理所有节点：先变换邻居状态，再按边属性生成的门控向量调整各分量，求和并除以节点度，最后与本节点的信息相加。下面把一次更新写出来，便能看见“沿图计算”具体发生在哪一步。

同一套学习规则，在每个节点上重复使用

邻居消息mi=Σ邻居[门控向量gij逐分量乘Wn hj]/max(1,zi)。更新hi′=ReLU(Ws hi+bs+mi)。hi为节点状态向量，Wn、Ws与bs为训练参数，门控由边属性的线性变换与sigmoid得到。

𝒩(i)表示节点i的邻居集合，W_{n}和W_{s}是训练得到的矩阵，b_{s}是偏置向量。矩阵乘法就是把多个输入按不同权重组合成新的分量。g_{ij}是由边属性生成的门控向量，各分量在0和1之间；符号⊙表示对应分量相乘。分母使用max(1,z_{i})，使孤立节点也能正常计算：它没有邻居，消息和为0，分母则取1。

可以先用一个分量理解加权过程。若两个邻居经过变换后的值分别是2和4，相应门控为0.5和0.25，则邻居消息为(0.5×2+0.25×4)/2=1。假设本节点变换后连同偏置得到−0.3，相加为0.7；ReLU保留这个正数，若结果小于0则置为0。完整模型在24个分量上同时做类似运算，并通过训练决定哪些组合有助于预测。

重复三层之后，模型对16个节点的状态取平均，再经过两次线性变换和一次ReLU，得到整张图的输出。平均汇总让节点重编号不会改变预测：给同一张图换一组编号，同时同步调整边表与属性，计算的关系仍然相同。三层消息使局部信息最多沿三条边传播，随后由全图平均组合。对于更大、更长程的结构，传播层数与汇总方式需要结合目标重新设计。

贯通分类器将最终得分通过sigmoid变成0到1之间的值，以0.5为判断阈值，并用二元交叉熵训练。这个损失鼓励真实贯通样本得到较高分数、未贯通样本得到较低分数。力学回归的输出则经过softplus，得到非负数，用来预测下面定义的对数刚度。两种损失分别对应离散标签与连续响应，因此训练过程、保存的参数和最终评价都分开进行。

训练用的数值尺度，与读图用的单位分别写清

回归目标t=ln(1+K/k0)，训练损失为样本平均的(t̂−t)²。k0是弹簧常数单位，n为当前训练样本数。预测还原为K̂/k0=exp(t̂)−1；三个模型先平均t̂，再还原。

k₀是弹簧常数单位，先用K除以k₀，才能对无量纲数取对数。加1让K=0时也有定义，此时t=0；若K=k₀，t=ln2≈0.693；若K=3k₀，t=ln4≈1.386。对数变换压缩较大刚度的数值范围，让训练同时关注不同尺度。L是平方误差的样本平均，帽号表示模型预测。评价时再用指数还原，RMSE与MAE均回到k₀单位，读者可以直接比较预测与力学计算。

每个任务训练三个不同初始化的图模型，随机种子固定为13、23和33。分类时平均三个概率；回归时先平均三个对数输出，再按本节的变换执行exp(y)−1还原。例如两次对数输出为0和ln4，平均为ln2，还原刚度为1；若先分别还原为0和3，再平均，则得到1.5。两种顺序对应两种汇总方式，本例采用前一种。因此，从保存的预测复算结果时，要先在相同的对数尺度上求平均。每个图模型含4705个参数，训练最多120轮，最终保存哪一轮由验证损失决定。

比较模型时还需要容易解释的参照。贯通任务先用边数做逻辑回归，再加入度的离散程度、最大最小度、低度节点比例、连通分量数和三角形数量。力学任务的简单岭回归除了边数，还读取平均弹簧常数及加载方向；丰富特征进一步加入连接方向统计、刚度分布和一个仿射试探位移的能量估计。各模型标准化所用的均值和尺度都从训练数据得到，正则化强度由验证集选择。

仿射试探位移可以具体理解为：让每个节点按其高度y，沿加载方向移动δy，暂时不允许内部节点另外调整。将这种位移代入边能量，就得到一个有效刚度上界，因为之后的自由调整只会把最低能量降到相同或更低。这个特征从输入几何与弹簧常数直接计算，未读取平衡求解的标签。它也提供一种把物理知识放进AI的方法：先构造容易计算、有明确意义的近似量，再让学习模型补充结构差异。

## 05完整运行一次，分别检查连接与响应

下面的程序从16个节点组成的4×4方格开始。水平、竖直和相邻方格对角线共有42条候选边，每个母网络保留8到38条边。生成方式分为三族：均匀抽取连接、中部跨越连接较少，以及偏向水平连接。三族使用相同的一组边数预算，因而可以研究“放在哪里”的影响。每个母网络再生成两种几何与弹簧变体，分别施加横向剪切和竖直拉伸，共得到960个样本。

这些样本来自240个母网络，同一母网络的四条记录共享连接结构。划分数据时，四条记录一起进入同一个集合：96个母网络用于训练，32个用于验证，32个作为同族新网络测试；80个水平偏向母网络整族留出。因此，128条常规测试记录对应32张新母图，320条新族测试记录对应80张母图。保留这种分组，可以检查模型面对新连接结构时的表现，避免把同一结构的另一种加载当成独立新材料。

贯通标签由路径搜索获得，刚度标签来自边界位移固定后的能量最小化。底边全部固定，顶边所有节点沿指定方向移动0.01ℓ₀，顶边的另一个位移分量固定为0，内部节点的两个分量都可调整。程序同时计算自由节点的残余力，并比较能量法与边界反力法的刚度。运行需要NumPy、PyTorch、scikit-learn和Matplotlib，数据生成、两个任务的训练与六幅结果图都在同一段代码中。

完整Python例子 · NumPy · PyTorch · scikit-learn · Matplotlib[下载代码](https://ml-biomat.com/static/tutorials/polymer-ai/assets/86fd8c61166d905b2d7b096b.py)

```python
"""Network connectivity and loading response are two separate learning tasks.

Dependencies: NumPy, PyTorch, scikit-learn, Matplotlib.
All samples are generated 2D unstressed axial-spring networks.
Lengths use l0, springs use k0, effective stiffness uses k0.
"""
from pathlib import Path
import os, copy, json
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
OUT = Path("gel_outputs")
torch.set_num_threads(4)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)

def boundary_path(n, edges, bottom, top):
    reached=set(map(int,bottom))
    adjacent=[[] for _ in range(n)]
    for a,b in edges:adjacent[a].append(b);adjacent[b].append(a)
    frontier=list(reached)
    while frontier:
        a=frontier.pop()
        for b in adjacent[a]:
            if b not in reached:reached.add(b);frontier.append(b)
    return bool(reached & set(map(int,top)))


def solve(x,edges,k,bottom,top,loading,delta=.01):
    """Minimize spring extension norm; zero modes are allowed, without a penalty."""
    x=np.array(x,float);edges=np.array(edges,int);k=np.array(k,float)
    rows=[]
    for (a,b),value in zip(edges,k):
        d=x[b]-x[a];direction=d/np.linalg.norm(d)
        row=np.zeros(x.size);row[2*a:2*a+2]=-direction*np.sqrt(value)
        row[2*b:2*b+2]=direction*np.sqrt(value);rows.append(row)
    B=np.array(rows).reshape(-1,x.size)
    fixed=np.sort(np.ravel([[2*i,2*i+1] for i in list(bottom)+list(top)]))
    free=np.setdiff1d(np.arange(x.size),fixed)
    u=np.zeros(x.size)
    for i in top:u[2*i:2*i+2]=delta*np.array(loading)
    if len(free):u[free]=np.linalg.lstsq(B[:,free],-B[:,fixed]@u[fixed],rcond=1e-11)[0]
    ext=B@u;energy=.5*float(ext@ext);force=B.T@ext
    reaction=sum(float(force[2*i:2*i+2]@np.array(loading)) for i in top)
    effective=2*energy/delta**2
    residual=float(max(abs(force[free]),default=0))
    assert residual<1e-8
    assert abs(reaction/delta-effective)<1e-8
    if effective<1e-10:effective=0.
    return dict(stiffness=effective,energy=energy,reaction=reaction,residual=residual,
                displacement=u.reshape(-1,2).tolist(),
                free_zero_modes=int(len(free)-np.linalg.matrix_rank(B[:,free],tol=1e-10)))


def generate():
    rng=np.random.default_rng(1313);side=4
    x=np.array([(i/(side-1),j/(side-1)) for j in range(side) for i in range(side)])
    candidates=[]
    for a in range(len(x)):
        for b in range(a+1,len(x)):
            grid=np.round(abs(x[b]-x[a])*(side-1)).astype(int)
            if max(grid)==1:candidates.append((a,b))
    candidates=np.array(candidates)
    bottom=np.arange(4);top=np.arange(12,16);interior=np.arange(4,12)
    budget=rng.integers(8,39,size=80);seen=set();rows=[]
    for family in ["uniform","bottleneck","horizontal_bias"]:
        for parent,m in enumerate(budget):
            weights=np.ones(len(candidates))
            if family=="bottleneck":
                crossing=(x[candidates[:,0],1]<.5)&(x[candidates[:,1],1]>.5)
                weights[crossing]=.035
            if family=="horizontal_bias":
                weights[abs(x[candidates[:,0],1]-x[candidates[:,1],1])>1e-9]=.08
            while True:
                choice=np.sort(rng.choice(len(candidates),size=int(m),replace=False,p=weights/weights.sum()))
                fingerprint=tuple(map(int,choice))
                if fingerprint not in seen:seen.add(fingerprint);break
            edges=candidates[choice]
            basek=rng.uniform(.7,1.3,size=len(edges))
            group=family+"-"+str(parent).zfill(3)
            split="family_test" if family=="horizontal_bias" else (
                "test" if parent%5==2 else "validation" if parent%5==4 else "train")
            for variant in range(2):
                geom=x.copy()
                if variant:geom[interior]+=rng.uniform(-.025,.025,size=(len(interior),2))
                spring=basek*rng.uniform(.85,1.15,size=len(edges))
                for loading_name,loading in [("shear",[1.,0.]),("extension",[0.,1.])]:
                    physical=solve(geom,edges,spring,bottom,top,loading)
                    rows.append(dict(group=group,family=family,variant=variant,loading_name=loading_name,
                        loading=loading,split=split,x=geom.tolist(),edges=edges.tolist(),k=spring.tolist(),
                        bottom=bottom.tolist(),top=top.tolist(),edge_count=int(m),
                        spanning=boundary_path(len(x),edges,bottom,top),**physical))
    return rows



def encode(rows):
    nodes=[];edge_features=[];counts=[];rich=[]
    for r in rows:
        x=np.array(r['x']);edges=np.array(r['edges']);k=np.array(r['k']);v=np.array(r['loading'])
        a=np.zeros((16,16));ef=np.zeros((16,16,5))
        for (i,j),w in zip(edges,k):
            d=x[j]-x[i];length=np.linalg.norm(d);n=d/length
            a[i,j]=a[j,i]=1
            ef[i,j]=[n[0],n[1],length,w,1]
            ef[j,i]=[-n[0],-n[1],length,w,1]
        degree=a.sum(1);bottom=np.zeros(16);top=np.zeros(16)
        bottom[r['bottom']]=1;top[r['top']]=1
        nodes.append(np.c_[x,bottom,top,np.tile(v,(16,1)),degree/8])
        edge_features.append(ef)
        m=len(edges);mean=float(k.mean())
        counts.append([m/42,mean,*v,(m/42)*v[0],(m/42)*v[1]])
        d=x[edges[:,1]]-x[edges[:,0]];length=np.linalg.norm(d,axis=1);n=d/length[:,None]
        affine=float(np.sum(k*(n@v)**2*d[:,1]**2))
        # Descriptors depend only on input geometry/edges, not equilibrium labels.
        triangles=float(np.trace(a@a@a)/6)
        visited=set();components=0
        for start in range(16):
            if start in visited:continue
            components+=1;queue=[start];visited.add(start)
            while queue:
                i=queue.pop()
                for j in np.flatnonzero(a[i]):
                    if j not in visited:visited.add(j);queue.append(j)
        rich.append(counts[-1]+[degree.std(),degree.min(),degree.max(),float(np.mean(degree<=1)),
                    components,triangles,float(k.std()),float(k.min()),float(k.max()),
                    float(np.sum(k*n[:,0]**2)),float(np.sum(k*n[:,1]**2)),
                    float(np.sum(k*n[:,0]*n[:,1])),affine])
    return np.array(nodes),np.array(edge_features),{"count":np.array(counts),"graph_features":np.array(rich)}


class GraphModel(nn.Module):
    def __init__(self,regression):
        super().__init__();self.regression=regression
        self.input=nn.Linear(7,24)
        self.self_layers=nn.ModuleList([nn.Linear(24,24) for _ in range(3)])
        self.neighbor=nn.ModuleList([nn.Linear(24,24,bias=False) for _ in range(3)])
        self.gates=nn.ModuleList([nn.Linear(4,24) for _ in range(3)])
        self.head=nn.Sequential(nn.Linear(24,24),nn.ReLU(),nn.Linear(24,1))
    def forward(self,n,e):
        h=torch.relu(self.input(n));mask=e[:,:,:,4:5]
        degree=mask.sum(2).clamp(min=1)
        for ws,wn,wg in zip(self.self_layers,self.neighbor,self.gates):
            gate=torch.sigmoid(wg(e[:,:,:,:4]))*mask
            message=(gate*wn(h)[:,None,:,:]).sum(2)/degree
            h=torch.relu(ws(h)+message)
        out=self.head(h.mean(1)).ravel()
        return torch.nn.functional.softplus(out) if self.regression else out


def score(rows,pred,task):
    out={}
    for split in ["train","validation","test","family_test"]:
        ids=np.array([i for i,r in enumerate(rows) if r['split']==split])
        if task=="spanning":
            y=np.array([rows[i]['spanning'] for i in ids])
            out[split]=dict(balanced_accuracy=float(balanced_accuracy_score(y,pred[ids]>=.5)),
                           auroc=float(roc_auc_score(y,pred[ids])))
        else:
            y=np.array([rows[i]['stiffness'] for i in ids]);p=np.expm1(pred[ids])
            out[split]=dict(RMSE=float(np.mean((p-y)**2)**.5),MAE=float(np.mean(abs(p-y))),
                           log1p_RMSE=float(np.mean((pred[ids]-np.log1p(y))**2)**.5))
    return out


def main():
    OUT.mkdir(exist_ok=True)
    rows=generate()
    node,edge,features=encode(rows)
    train=np.array([i for i,r in enumerate(rows) if r['split']=='train'])
    valid=np.array([i for i,r in enumerate(rows) if r['split']=='validation'])
    results={"models":{},"split_counts":{s:sum(r['split']==s for r in rows) for s in ["train","validation","test","family_test"]}}
    for task in ["spanning","response"]:
        # A graph path is invariant to loading, positive spring constants and geometry.
        # Keep only boundary identities, degrees and adjacency for that task.
        task_node=node.copy();task_edge=edge.copy();task_features=features
        if task=="spanning":
            task_node[:,:,[0,1,4,5]]=0
            task_edge[:,:,:,:4]=0
            task_features={"count":features["count"][:,[0]],
                           "graph_features":features["graph_features"][:,[0,6,7,8,9,10,11]]}
        nt=torch.tensor(task_node,dtype=torch.float32);et=torch.tensor(task_edge,dtype=torch.float32)
        y=np.array([float(r['spanning']) if task=="spanning" else np.log1p(r['stiffness']) for r in rows])
        results['models'][task]={}
        for name,X in task_features.items():
            scaler=StandardScaler().fit(X[train]);Z=scaler.transform(X);best=None;history=[]
            for lam in [.01,.1,1.,10.,100.]:
                model=(LogisticRegression(C=1/lam,max_iter=3000,tol=1e-9) if task=="spanning" else Ridge(alpha=lam)).fit(Z[train],y[train])
                p=model.predict_proba(Z[valid])[:,1] if task=="spanning" else np.maximum(0,model.predict(Z[valid]))
                loss=-balanced_accuracy_score(y[valid],p>=.5) if task=="spanning" else np.mean((p-y[valid])**2)
                history.append({"lambda":lam,"validation_loss":float(loss)})
                if best is None or loss<best[0]:best=(loss,model,lam)
            model=best[1]
            p=model.predict_proba(Z)[:,1] if task=="spanning" else np.maximum(0,model.predict(Z))
            results['models'][task][name]=dict(predictions=p.tolist(),scores=score(rows,p,task),lambda_=best[2],
                validation_candidates=history,scaler_mean=scaler.mean_.tolist(),scaler_scale=scaler.scale_.tolist(),
                coef=np.asarray(model.coef_).tolist(),intercept=np.asarray(model.intercept_).tolist())
        seeds=[];predictions=[]
        target=torch.tensor(y,dtype=torch.float32)
        lossfn=nn.BCEWithLogitsLoss() if task=="spanning" else nn.MSELoss()
        for seed in [13,23,33]:
            torch.manual_seed(seed);model=GraphModel(task=="response")
            optimizer=torch.optim.Adam(model.parameters(),lr=.003)
            rng=np.random.default_rng(1315);bestloss=float('inf');wait=0;history=[]
            for epoch in range(1,121):
                model.train()
                order=rng.permutation(train)
                for start in range(0,len(order),64):
                    ids=order[start:start+64];optimizer.zero_grad()
                    loss=lossfn(model(nt[ids],et[ids]),target[ids]);loss.backward();optimizer.step()
                model.eval()
                with torch.no_grad():
                    tl=float(lossfn(model(nt[train],et[train]),target[train]))
                    vl=float(lossfn(model(nt[valid],et[valid]),target[valid]))
                history.append(dict(epoch=epoch,train=tl,validation=vl))
                if vl<bestloss-1e-7:
                    bestloss=vl;bestepoch=epoch;weights=copy.deepcopy(model.state_dict());wait=0
                else:wait+=1
                if wait>=20:break
            model.load_state_dict(weights);model.eval()
            with torch.no_grad():
                p=model(nt,et)
                if task=="spanning":p=torch.sigmoid(p)
            p=p.numpy().astype(float);predictions.append(p)
            seeds.append(dict(seed=seed,best_epoch=bestepoch,history=history,scores=score(rows,p,task),
                parameters=sum(t.numel() for t in model.parameters()),
                state_dict={k:v.numpy().tolist() for k,v in weights.items()}))
            print(task,seed,"best epoch",bestepoch,"validation loss",bestloss,flush=True)
        p=np.mean(predictions,axis=0)
        results['models'][task]['message_passing']=dict(predictions=p.tolist(),scores=score(rows,p,task),seeds=seeds)
        for name,model in results['models'][task].items():
            key="balanced_accuracy" if task=="spanning" else "RMSE"
            print(task,name,key,"test %.6f; new family %.6f" %
                  (model['scores']['test'][key],model['scores']['family_test'][key]),flush=True)
    results["scope"]="Generated, unstressed 2D axial-spring networks; loading response in k0 units"
    results["generator_seed"]=1313
    results["split_parent_counts"]={s:len({r["group"] for r in rows if r["split"]==s}) for s in results["split_counts"]}
    results["topology_task_inputs"]="Boundary identities, degree and adjacency only; independent of geometry/k/loading."
    results["response_ensemble"]="Average log1p stiffness outputs, then expm1."
    results["selected_pair"]=["uniform-007","bottleneck-007"]
    for i,r in enumerate(rows):
        r["predictions"]={task:{name:float(m["predictions"][i]) for name,m in models.items()}
                          for task,models in results["models"].items()}
    make_plots(rows,results)
    (OUT/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT/"samples.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")


def make_plots(rows,results):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
        "axes.spines.top":False,"axes.spines.right":False,"svg.hashsalt":"L13-gels",
        "text.color":"#29433a","axes.labelcolor":"#29433a","axes.titlepad":14,
        "figure.facecolor":"#fffdf8","savefig.facecolor":"#fffdf8"})
    colors=["#ae8656","#5c7f9f","#257a68"]
    names=["count","graph_features","message_passing"]
    labels=["Connection count","Graph features","Message passing"]

    def graph(ax,r,amplification=0):
        x=np.array(r["x"]);edges=np.array(r["edges"]);u=np.array(r["displacement"])
        ax.add_collection(LineCollection(x[edges],colors="#c2c9be",linewidths=1.2))
        moved=x+amplification*u
        if amplification:
            ax.add_collection(LineCollection(moved[edges],colors="#568f78",linewidths=1.5))
            ax.quiver(x[:,0],x[:,1],amplification*u[:,0],amplification*u[:,1],
                      angles="xy",scale_units="xy",scale=1,width=.004,color="#a97248")
        nodecolors=["#62848b" if i in r["bottom"] else ("#ac8053" if i in r["top"] else "#376d59") for i in range(len(x))]
        ax.scatter(moved[:,0],moved[:,1],s=20,c=nodecolors,zorder=4)
        ax.set_aspect("equal");ax.set_xlim(-.12,1.27);ax.set_ylim(-.12,1.15);ax.axis("off")

    def draw(ax,key):
        if key=="fixture":
            ax.axis("off");ax.set_title("A  A spanning square can have zero linear shear stiffness")
            x=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
            for j,edges in enumerate([[(0,1),(0,2),(1,3),(2,3)],[(0,1),(0,2),(1,3),(2,3),(0,3)]]):
                solved=solve(x,edges,np.ones(len(edges)),[0,1],[2,3],[1.,0.])
                r=dict(x=x.tolist(),edges=edges,bottom=[0,1],top=[2,3],**solved)
                sub=ax.inset_axes([.02+.5*j,.19,.46,.69]);graph(sub,r,20)
                sub.set_title(["Square","Add one diagonal"][j],fontsize=11)
                ax.text(.25+.5*j,.11,"Spanning: yes\nEffective stiffness / k0 = "+str(round(solved["stiffness"],2)),
                        ha="center",va="top",transform=ax.transAxes,fontsize=10)
            ax.text(.5,.01,"Displacement drawn 20 times larger; small-strain axial springs",ha="center",transform=ax.transAxes,fontsize=8)
        elif key=="fractions":
            rr=[r for r in rows if r["variant"]==0 and r["loading_name"]=="shear"]
            intervals=[8,14,20,26,32,39];centers=[];a=[];b=[];counts=[]
            for lo,hi in zip(intervals[:-1],intervals[1:]):
                selected=[r for r in rr if lo<=r["edge_count"]<hi]
                centers.append((lo+hi-1)/2);counts.append(len(selected))
                a.append(np.mean([r["spanning"] for r in selected]))
                b.append(np.mean([r["stiffness"]>1e-8 for r in selected]))
            ax.plot(centers,a,"o-",color=colors[1],label="Bottom-to-top path")
            ax.plot(centers,b,"s-",color=colors[2],label="Positive linear shear response")
            for cx,n in zip(centers,counts):ax.text(cx,.025,"n="+str(n),ha="center",fontsize=8)
            ax.set(xlabel="Number of edges / binned",ylabel="Fraction of generated parent networks",
                   title="B  Connections and shear response emerge differently",ylim=(0,1.06))
            ax.legend(fontsize=8,loc="upper left");ax.grid(alpha=.12)
        elif key=="displacement":
            ax.axis("off");ax.set_title("C  The same 32 edges can leave a mechanical bottleneck")
            for j,group in enumerate(results["selected_pair"]):
                r=next(r for r in rows if r["group"]==group and r["variant"]==0 and r["loading_name"]=="shear")
                sub=ax.inset_axes([.02+.5*j,.19,.46,.69]);graph(sub,r,14)
                sub.set_title(group,fontsize=11)
                ax.text(.25+.5*j,.11,"Spanning: "+str(r["spanning"])+"\nStiffness / k0 = %.4f"%r["stiffness"],
                        ha="center",va="top",transform=ax.transAxes,fontsize=10)
            ax.text(.5,.01,"Gray: reference; green: relaxed displacements amplified 14 times",ha="center",transform=ax.transAxes,fontsize=8)
        elif key=="parity":
            model=results["models"]["response"]["message_passing"]
            maximum=max(r["stiffness"] for r in rows if r["split"] in ["test","family_test"])
            for split,color,mark in [("test",colors[1],"o"),("family_test",colors[2],"^")]:
                ids=[i for i,r in enumerate(rows) if r["split"]==split]
                target=np.array([rows[i]["stiffness"] for i in ids]);pred=np.expm1(np.array(model["predictions"])[ids])
                ax.scatter(target,pred,s=20,alpha=.5,c=color,marker=mark,
                           label="New parents" if split=="test" else "New topology family",edgecolors="none")
            ax.plot([0,maximum],[0,maximum],":",color="#948f7b")
            ax.set(xlabel="Direct mechanical solution / k0",ylabel="Graph model prediction / k0",
                   title="D  Predict response on held-out networks")
            ax.legend(fontsize=8);ax.grid(alpha=.12)
        elif key=="classification":
            for j,split in enumerate(["test","family_test"]):
                vals=[results["models"]["spanning"][name]["scores"][split]["balanced_accuracy"] for name in names]
                ax.barh(np.arange(3)+(.17 if j else -.17),vals,height=.3,
                        color=["#9ebdaa","#567e9e"][j],label=["New parents","New family"][j])
            ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,1.03)
            ax.axvline(.5,color="#9a907c",ls=":")
            ax.set(xlabel="Balanced accuracy",title="E  Learn spanning from topology alone")
            ax.legend(fontsize=8,loc="lower right");ax.grid(axis="x",alpha=.12)
        elif key=="regression":
            ax.axis("off");ax.set_title("F  Response errors in physical stiffness units")
            for j,metric in enumerate(["RMSE","MAE"]):
                sub=ax.inset_axes([.28,.56-.49*j,.68,.34])
                for i,split in enumerate(["test","family_test"]):
                    vals=[results["models"]["response"][name]["scores"][split][metric] for name in names]
                    sub.barh(np.arange(3)+(.16 if i else -.16),vals,height=.28,
                             color=["#9ebdaa","#567e9e"][i],label=["New parents","New family"][i])
                sub.set_yticks(range(3),labels,fontsize=8);sub.invert_yaxis()
                sub.set_xlabel(metric+" / k0",fontsize=9);sub.tick_params(labelsize=8)
                sub.grid(axis="x",alpha=.12)
                if j==0:sub.legend(fontsize=8,loc="upper center",bbox_to_anchor=(.5,1.3),ncol=2)

    keys=["fixture","fractions","displacement","parity","classification","regression"]
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.4,5.2),layout="constrained");draw(ax,key)
        fig.savefig(OUT/(key+".svg"),metadata={"Date":None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(14.8,15.6),layout="constrained")
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(OUT/"network_learning.svg",metadata={"Date":None})
    fig.savefig(OUT/"network_learning.png",dpi=180);plt.close(fig)


if __name__ == "__main__":
    main()
```

本次实际运行输出

```
spanning 13 best epoch 33 validation loss 0.17148548364639282
spanning 23 best epoch 44 validation loss 0.16226471960544586
spanning 33 best epoch 78 validation loss 0.15127524733543396
spanning count balanced_accuracy test 0.562500; new family 0.875000
spanning graph_features balanced_accuracy test 0.750000; new family 0.891667
spanning message_passing balanced_accuracy test 0.843750; new family 0.941667
response 13 best epoch 38 validation loss 0.008396297693252563
response 23 best epoch 58 validation loss 0.008104164153337479
response 33 best epoch 77 validation loss 0.00817214883863926
response count RMSE test 0.213093; new family 0.180015
response graph_features RMSE test 0.138487; new family 0.135067
response message_passing RMSE test 0.122820; new family 0.115361
```

A图是方框的手算核对。灰色表示初始位置，绿色表示施加边界位移后的形状，位移为了看清放大了20倍。两幅图都存在底到顶路径，线性剪切刚度分别为0和0.5k₀。这里横向移动与弹簧轴向伸长的关系已经在前面逐步算出，图像则让读者看到同一个计算对应怎样的几何变化。图中的大幅歪斜是显示放大后的轮廓，求解使用的仍是0.01ℓ₀的小位移。

B图从240个母网络中各取规则几何下的一次剪切计算，按边数区间分组。蓝线统计存在上下路径的比例，绿线统计剪切刚度大于10^{−8}k₀的比例，底部n标出每组母网络数。随着边数增加，两种比例总体上升，但数值并不相同。这个图描述三种指定生成规则下的样本频率，可以用来观察结构差别；它的横轴是边数，不能直接替换成前面树状近似中的位点反应概率p。

C图选取同为32条边的一对母网络。均匀族的网络贯通，剪切刚度约为0.5419k₀；中部连接稀少的网络在这一实例中完全分成上下两部分，刚度为0。后者虽然上下各自看起来很密，仍缺少跨越中间的路径。绿色位移放大14倍，帮助看见上半部怎样跟随顶边整体移动。挑选这种输入边数相同的比较，能把连接数量与连接位置的作用分开观察。

一次运行 · 六幅结果图

![A｜都已贯通的方框，加斜撑前后线性剪切刚度不同；位移放大20倍。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/decfff275f73669a58bfc0e5.svg)

A｜都已贯通的方框，加斜撑前后线性剪切刚度不同；位移放大20倍。

![B｜240个母网络按边数分组：贯通比例与具有正剪切响应的比例分别统计。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/a1acadbd5072bd90a01609fa.svg)

B｜240个母网络按边数分组：贯通比例与具有正剪切响应的比例分别统计。

![C｜同为32条边，连接的位置改变贯通和剪切响应；位移放大14倍。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/aab478c2d2c9fb655384abc3.svg)

C｜同为32条边，连接的位置改变贯通和剪切响应；位移放大14倍。

![D｜每个点对应一个留出加载样本，横轴为独立力学解，纵轴为图模型预测。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/68b186d69bdaca374c65b426.svg)

D｜每个点对应一个留出加载样本，横轴为独立力学解，纵轴为图模型预测。

![E｜两套留出数据上的贯通分类：连接计数、图特征和消息传递。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/0b6d59e34b34ccb7fd5427f2.svg)

E｜两套留出数据上的贯通分类：连接计数、图特征和消息传递。

![F｜用相同刚度单位同时比较RMSE与MAE，观察两种误差如何评价同一预测。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/2147b5643376be19eb4220f2.svg)

F｜用相同刚度单位同时比较RMSE与MAE，观察两种误差如何评价同一预测。

**图6** 960个受控二维轴向弹簧样本来自240个母网络，每个母网络包含两种几何/弹簧变体及两个加载方向。96个母网络训练、32个验证、32个同族测试，另80个水平偏向网络整族留出。贯通标签来自图搜索，加载刚度由能量最小化求得。

[矢量组图SVG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/cf86208e6afbaa14c1a24505.svg)[高清组图PNG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/6b42cdc430b6b7d08b8a5899.png)[完整样本JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/11f3610d04fe6f93f4866922.json)[模型与结果JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/cf2b15985d9287e52506c1e7.json)

D图把图模型的刚度预测与独立力学解逐点比较，理想预测落在对角线上。圆点是同族新母网络的加载样本，三角形是整族留出的水平偏向网络。横轴为0附近仍有预测大于0的点，表示模型对零响应结构给出了正的近似；其他点偏离对角线的距离则显示数值误差。由于同一母网络拥有多种加载与变体，图上的点是加载样本，评价独立结构数量时仍应回到母网络分组。

E图比较贯通分类的平衡准确率。它先分别算出贯通与不贯通两类各自被正确识别的比例，再对两个比例取平均。例如两类识别率分别为90%和60%，平衡准确率就是75%；始终判断为同一类时为50%。在本次常规测试中，连接计数、丰富图特征与消息传递分别得到0.5625、0.7500和0.8438。输入保留更多连接关系后，模型可以区分一些边数相近但路径不同的结构。

整族留出的水平偏向网络上，三种方法的平衡准确率分别为0.8750、0.8917和0.9417，高于这次常规测试的对应值。新族并不天然更难：本例新族的边数与贯通标签之间恰好存在较清楚的关系，连接计数就能提供较强线索。因此，两套测试应分别报告，并联系生成方式解释。若希望评价对另一种连接机制的推广，可以另设新的拓扑族，继续保持整组留出。

F图回到连续刚度，用两种误差查看同一组预测。MAE先对每个误差取绝对值再平均，容易理解为典型绝对偏差；RMSE先平方再平均最后开平方，对少量较大的误差更敏感。若两个样本误差为0和2k₀，MAE为1k₀，RMSE约1.414k₀。将两项同时展示，可以看出一种方法是在减少大偏差，还是让大部分样本更接近，而不必把不同含义压成一个分数。

常规测试的RMSE依次为0.2131、0.1385和0.1228k₀；新族测试依次为0.1800、0.1351和0.1154k₀。这次消息传递在两套测试中都有较小的平方误差。新族测试的MAE则由丰富图特征得到0.0676k₀，消息传递为0.0746k₀，说明两种误差指标关注的预测分布有所不同。研究者可以结合允许的最大偏差、典型精度与后续筛选用途，决定怎样评价候选模型。

还可以做两项有明确预期的检查。给节点重新编号，同时更新边表、坐标和边界身份，物理响应与图模型输出都应保持一致；只改变同一网络的加载方向，贯通标签应不变，而刚度通常会变。前者检验模型是否依赖任意编号，后者检验它是否区分拓扑与力学。这样的检查直接来自问题定义，能够帮助发现输入遗漏或数据组织错误，也比单纯再看一遍训练分数更有针对性。

若把这项研究接到真实凝胶上，下一步可以从可观测结构入手：用成像或其他表征估计连接与方向，用力学实验记录尺寸、加载和响应，再将这些信息整理为带来源的图样本。连接寿命、弯曲刚度与溶胀状态也可以逐项加入模型。每增加一项机制，就安排对应测量或计算来确定参数，让AI学习的输出继续与明确的实验对象相连。

本节把含水材料中的三个层次接了起来：局部结合形成连接，连接构成网络，网络在边界加载下产生响应。AI沿着同样的层次读取结构，而评价始终回到路径与刚度这两个具体问题。[《纤维网络的承载机制：取向、拉伸与弯曲》](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/)将把边从柔性链段换成具有方向和弯曲能力的纤维，进一步观察生物大分子怎样织成能够承载的网，以及为什么纤维的排列和弯曲也值得进入模型。

## 资料与延伸阅读

Grant等，1973，[Biological interactions between polysaccharides and divalent cations: The egg-box model](https://doi.org/10.1016/0014-5793%2873%2980770-7)；Morris、Rees与Thom，1973，[Characterization of polysaccharide structure and interactions by circular dichroism: order–disorder transition in the calcium alginate system](https://doi.org/10.1039/C39730000245)；Li等，2007，[Reexamining the egg-box model in calcium-alginate gels with X-ray diffraction](https://pubmed.ncbi.nlm.nih.gov/17291070/)。这些研究把糖单元结构、离子结合与连接区组织联系起来。

Flory，1941，[Molecular Size Distribution in Three Dimensional Polymers. I. Gelation](https://doi.org/10.1021/ja01856a061)；Flory与Rehner，1943，[网络的橡胶弹性](https://doi.org/10.1063/1.1723791)与[溶胀](https://doi.org/10.1063/1.1723792)；Tanaka，1978，[Collapse of Gels and the Critical Endpoint](https://doi.org/10.1103/PhysRevLett.40.820)。本节的分支推导、理想弹性尺度与凝胶体积讨论分别保留各自的近似条件。

Scarselli等，2009，[The Graph Neural Network Model](https://doi.org/10.1109/TNN.2008.2005605)。本节实现为三层门控消息传递，使用受控轴向弹簧网络训练两个独立任务；六幅结果图来自同页代码运行。科学史插图按研究对象与概念关系原创绘制，计算样本、模型权重与预测均可在结果区下载。
