# 把蛋白质放进水里：拓扑、溶剂与离子

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g06/
Language: zh-CN

从泛素的水环境出发，读懂周期晶胞、三位点水和盐的整数计数，逐步建立组成明确的溶液。

## 水为什么必须进入我们的模型

把一颗盐放进水里，它很快就失去了原来的形状；把蛋白质从水溶液中取出来，周围环境的改变也会影响它的结构和活动。研究生物分子时，水通常占据模拟盒子的绝大部分，却很容易在观看分子图时被隐藏。这样的显示方式便于看清蛋白质，也容易让人误以为水只是背景。本讲继续使用泛素，从上一讲准备好的蛋白质坐标出发，把它放进具有明确水模型、盐含量和周期边界的溶液。读完以后，你应当能够解释每一步加入了什么，核对坐标与拓扑是否一致，并根据实际分子数算出这个小盒子的盐浓度。

水分子的氧附近带有较多电子，两个氢附近相对缺少电子，因此分子内部存在电荷分布的不均匀。一个整体不带净电荷的水分子，仍然可以转动身体，让不同部位朝向带电的邻居。蛋白质表面的带电侧链、可以形成氢键的基团以及较少与水形成有利接触的区域，会使附近水分子的排列与运动发生变化。与此同时，水分子也在彼此作用，热运动使这些邻接关系不断更新。因此，蛋白质接触水的面积、表面基团的位置以及分子自身的构象，都进入了同一个相互影响的系统。

可以用人群中的交谈来理解这种联系。一个人的转身既改变他与身边人的距离，也会促使其他人调整位置；人群的活动由许多局部反应共同组成。分子没有意图，运动来自力和热涨落，但“周围环境也参与变化”这个特点很相似。显式溶剂模拟把每个水分子的相互作用位点放入计算中，于是能够逐帧查看水在哪里、朝向怎样、在某个位置停留多久。研究蛋白质表面的水合层、离子的分布或者小分子接近蛋白质的过程时，这种分辨率很有帮助，计算代价也随水分子数量增加。

本例采用 AMBER99SB-ILDN 蛋白质参数和与它配套使用的 TIP3P 三位点水模型，研究对象是自由的泛素单体及周围水和离子。三个水位点分别位于一个氧和两个氢上，在后续动力学中保持指定的分子几何。蛋白质与水、离子之间的相互作用由选定参数共同决定。经典固定拓扑描述的是这些分子的运动和接触；如果研究问题涉及水分解、质子沿氢键网络转移或者蛋白质发生化学反应，就需要能够处理电子或成键变化的模型。先把研究对象与模型能表达的过程对应起来，后面的命令才有明确用途。

准备溶液也像安排一次实验：容器多大、加入多少溶质、使用哪一种溶剂，都影响最终条件。在计算中，容器由周期晶胞定义，分子数量必须是整数，而盐浓度需要由数量与体积共同计算。我们会先得到一个包含 1 个泛素、5868 个水分子、17 个钠离子和 17 个氯离子的初始体系，再在下一讲让它经过能量最小化与温压调整。此处的主要任务是把系统组成建立正确，给之后的运动提供一个化学身份和空间安排都清楚的起点。

[Figure: 蛋白质、水和离子组成示意](https://ml-biomat.com/tutorials/molecular-dynamics/g06/#zh-s1)

图 1 · 水与离子也是可运动的组成部分。图形表示组分类别，数量取自本例实际加盐后的结构。

## 从盐溶液导电到计算中的带电粒子

盐进入水后为什么能帮助导电，是十九世纪物理化学面临的重要问题。固体氯化钠可以看作正负离子有序排列形成的晶体，溶解后其中的带电组分能够在液体中移动。Arrhenius 在十九世纪八十年代发展的电解质解离观点，把溶液中的电流与可移动的离子联系起来，也帮助解释一些溶液性质为何与加入的化学式单位数不成简单比例。这里最值得带入模拟的认识，是“加入一个化学式单位”与“溶液中出现多少个运动粒子”之间的区别：一个 NaCl 单位对应一个钠离子和一个氯离子。

两种离子的电荷符号相反，数量相等时总电荷相互抵消，但它们仍然各自与周围水分子和蛋白质作用。对钠离子而言，水分子较负的氧端往往更容易靠近；对氯离子而言，水分子较正的氢端会参与邻近的取向排列。这种水合结构处于热运动之中，邻近水分子能够交换。图中的定向水只是帮助识别电荷与取向的关系，实际分布还受空间拥挤、水与水的作用和温度影响。正因为这些因素同时存在，模拟才需要计算整个环境，而不是把每个离子周围安排一圈永久不动的水。

离子在溶液中的作用也不等同于给蛋白质表面逐个贴上配对电荷。较远处的离子通过集体分布改变静电环境，较近处的离子还可能与某些表面基团形成更直接的接触。具体离子种类、浓度、蛋白质表面化学性质以及采用的参数，都会影响这些分布。本例先选常见的一价钠离子和氯离子，是为了把数量、电荷和浓度的关系讲清楚。若换成钙离子，电荷数、水合性质和相互作用参数都要一起改变，不能只把名字从 NA 改成 CA 后继续沿用同一套解释。

二十世纪后期，研究者逐渐能够在计算机中追踪许多水分子的运动。1983 年，Jorgensen 等人比较了一系列简单液态水势模型，TIP3P 是这一水模型研究的重要成员。模型把复杂的电子分布压缩成少量相互作用位点及参数，用相对少的运算描述液体的统计性质。这样的简化为把水加入蛋白质模拟提供了实际可用的办法，也让模型选择成为研究的一部分：不同的水模型对密度、扩散、介电响应等性质的表现各有特点，模型名称因此承载着具体的几何和相互作用定义。

从离子理论到水模型，贯穿其中的是对“液体里有哪些会运动、会相互作用的对象”的不断澄清。我们在坐标文件中写下 NA、CL、OW 和 HW，并不是已经把这些对象的全部性质说明了；名称需要与拓扑中的质量、电荷、非键相互作用及几何约束配合。历史上对溶液的理解与现代模拟在这里相接：先确认有哪些粒子，再规定它们怎样相互影响，最后用运动的统计结果回答问题。下面的准备流程正是把这三个层次逐一落实到文件中。

[Figure: 离子导电与三位点水的科学史概念图](https://ml-biomat.com/tutorials/molecular-dynamics/g06/#zh-s2)

图 2 · 离子导电需要可移动的带电对象；三位点水模型用有限的几何与参数表达分子内部的电荷分布。δ表示相对于中性原子的部分电荷符号。

## 坐标告诉我们在哪里，拓扑告诉我们是什么

上一讲得到的 processed.gro 包含泛素各原子的坐标，而 topol.top 包含蛋白质的拓扑和对力场文件的引用。可以把前者理解为带编号的座位图，把后者理解为每个编号所对应的身份、连接关系和相互作用规则。座位图允许我们量距离，规则决定在这些距离下会产生多大的力。两个文件需要保持同一套原子顺序与分子组成。只要其中一个文件增加了水或改变了原子数，另一个文件就必须有相应的描述，否则软件无法把位置准确交给对应的物理对象。

topol.top 开头对 amber99sb-ildn.ff/forcefield.itp 的引用提供力场的总体定义，蛋白质部分随后列出原子、键、角及其他作用项，水和离子也各有对应的定义。文件末尾的 molecules 区域则给出系统实际包含多少个某类分子。这里的层次很重要：某一种水分子的模型可以只定义一次，molecules 区域再告诉程序重复使用多少次。本例的 SOL 数目在加盐前是 5902，加盐后是 5868；水模型本身没有因这个计数变化而改写，变化的是模型在系统中出现的次数。

执行 solvate 时，我们使用名为 spc216.gro 的水坐标模板。这个名字容易引起误会：本例的水力场仍是 TIP3P。模板提供的是一组已经排在小盒子里的水分子坐标，程序把这些坐标平铺到新的盒子，再删除与蛋白质发生过近接触的完整水分子。对于这种三位点水，坐标模板可以服务于不同的三位点模型；真正决定电荷、几何和相互作用参数的是已经选定的水拓扑。初始坐标与目标模型几何之间的小差别，会在准备和平衡阶段处理。

这也说明了为什么不能根据文件名随意拼接参数。水模型的氧氢电荷、氧上的色散与排斥参数、分子内部几何以及离子参数的适配关系，共同影响溶液的行为。蛋白质力场和水模型通常在特定组合下使用和检验。若把另一套水的电荷拿来，再保留原来的相互作用参数，就形成了一个新的混合模型，需要重新评价它的性质。本例沿用明确的 AMBER99SB-ILDN/TIP3P 组合，并通过软件所带力场定义选择 NA 和 CL，以便把注意力放在建模流程和结果解释上。

水的加入不是在蛋白质的外轮廓之外机械地填满一个空壳。蛋白质表面有凹槽，内部也可能有几何上允许水进入的位置。solvate 根据坐标、原子尺度和重叠判断选择初始水位置，这一步建立空间排布；后续运动才让这些位置与周围环境共同调整。观察初始结构时，可以检查是否有明显穿入原子的水、异常大的空洞或者蛋白质与周期映像过近的区域。对存在已知紧密结合水的研究体系，还应在准备结构时明确保留哪些实验水。本例已在上一讲选择去除 58 个结晶水氧，再统一建立显式溶剂环境。

加盐时，genion 会把选定的整个水分子替换为单个离子，并更新系统组成。三位点水包含三个原子位点，一个单原子离子只占一个位点，因此替换一个水会使坐标总原子数减少两个。这个简单的数量关系可以成为很实用的检查：34 个离子一共替换 34 个水，总位点数应减少 68。程序结束后的“成功”提示与这种化学计数是不同层次的信息；把二者对应起来，我们才能确信新坐标与新拓扑描述的是同一个溶液。

## 用周期晶胞给蛋白质留出水的空间

如果把一颗蛋白质放进一个很小的水滴，水滴表面会成为显著的环境因素。常见溶液模拟希望关注体相环境，于是采用周期边界：一个晶胞沿三个方向不断平移复制，分子从一侧离开时，可以用另一侧的等价位置来表示。这样，边界两侧仍然有邻居。计算中真正存储的是一个晶胞的粒子，周期映像由几何关系给出。对蛋白质来说，这相当于研究一套周期排列的蛋白质及其溶剂，因此蛋白质与自身映像之间的距离值得特别检查。

本例通过 editconf 选择菱形十二面体对应的周期晶胞，并设置 1.0 nm 的距离参数。GROMACS 在这种盒型下根据溶质的最大原子间直径确定大小，再加上两侧的余量。泛素在此起始构象中的最大直径约为 4.491 nm，得到的周期几何尺度约为 6.491 nm。这个设置为初始蛋白质周围提供水的空间，也与 1.0 nm 的短程相互作用截断相配合。随着蛋白质转动、构象变化和盒子在恒压过程中调整，实际最近映像距离仍应从轨迹检查；初始的距离参数不是整个运动过程中固定不变的最小间隙。

为什么不直接使用立方体？对于近似紧凑的溶质，菱形十二面体能够在保持同等周期映像间距的条件下减少需要填充的空间，因而减少水分子和运算量。它相对于同等映像间距的立方体，体积约为 0.707 倍。这一比较限定了相同的几何条件，不能拿任意两个边长相近的盒子直接套用比例。对于很长的纤维、膜片或明显各向异性的分子，适合的盒形还要顺着研究对象的形状选择。盒子服务于物理问题，节省水分子只是选择中的一个考虑。

在 GRO 文件里，这种周期几何常用三个倾斜的晶胞矢量来记录，而不是用一张十二面体外壳图来记录。矢量可以想成从同一起点出发的三个有方向的箭头，分别说明沿哪个方向平移多少距离就到达等价晶胞。本例三个矢量依次是 a=(6.49145, 0, 0) nm、b=(0, 6.49145, 0) nm 和 c=(3.24572, 3.24572, 4.59015) nm。c 同时带有水平和竖直分量，所以它是斜着走的。某些软件把粒子显示在一个倾斜平行六面体里，另一些显示成更紧凑的十二面体；只要周期映像关系相同，两种显示可以表达同一个系统。

[Figure: 倾斜晶胞底面和垂直高度](https://ml-biomat.com/tutorials/molecular-dynamics/g06/#zh-s4)

图 3 · 三个晶胞矢量记录周期平移。对正文的矢量排列，体积由水平底面积与c的竖直分量相乘得到；GRO格式的9个分量在代码中完整读取。

计算体积时，底面积乘垂直高度比“把三条边长相乘”更准确地揭示了原因。这里 a 与 b 在水平面内互相垂直，构成面积为 6.49145×6.49145 nm² 的底面；c 的竖直分量 4.59015 nm 才是这个底面对应的高度。c 的水平分量让上表面发生平移，却没有额外增加体积，就像把一摞等厚纸逐张错开后，纸的总体积仍由面积和总厚度决定。对于这种坐标排列，公式可以直接写成三个分量的乘积；一般倾斜晶胞则由完整矩阵的行列式计算体积。

这个倾斜晶胞的体积式 1

![这个倾斜晶胞的体积](https://ml-biomat.com/static/agent-math/f2cda83301b667c908567f1f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| V | 周期晶胞的体积，包括蛋白质和溶剂所占空间 | nm³ |
| a_{x}, b_{y}, c_{z} | 晶胞矢量a的x分量、b的y分量和c的z分量；本例分别为底面的两条垂直边与垂直高度 | 每个分量均为nm |
| x, y, z | 三个笛卡尔坐标方向的下标 | 方向标签，无单位 |
| =, × | 等号表示左右相等；相邻的三个分量相乘，单位也相乘 | 运算符，无单位 |

怎样理解本例a沿x方向，b沿y方向，底面面积为aₓbᵧ；c的竖直分量c_z是高度。倾斜的水平位移不增加底面积或高度。

算一个例子6.49145 nm×6.49145 nm×4.59015 nm=193.4239779 nm³。将nm³转为L时乘10⁻²⁴，得到1.934239779×10⁻²² L。

使用条件这个乘积适用于正文给出的下三角晶胞矢量排列；一般晶胞使用三个矢量组成矩阵的行列式绝对值。

代入这三个分量得到约 193.424 nm³。这个体积属于加盐时的初始晶胞，之后的恒压平衡会让它随时间变化。体积的意义也与观察对象相关：它包含蛋白质所占空间和水、离子的空间，是整个周期晶胞的体积。下一节使用的 genion 浓度定义正是基于这个总体积。把“整盒体积”提前说清楚，可以避免在计数时悄悄改用估计的水体积，造成两个看起来相近却定义不同的浓度。

## 一盒盐水里究竟有多少盐

日常配溶液时，人们可能称取几克盐，再加入一定体积的水；在分子模拟中，我们直接决定放入多少个离子。两种表达通过摩尔联系起来。一摩尔是一个固定数量的对象，包含 6.02214076×10²³ 个对象，这个数称为阿伏伽德罗常数的数值。所计数的对象必须说清楚，可以是水分子，也可以是钠离子或 NaCl 化学式单位。浓度 0.15 mol/L 的 NaCl 表示每升溶液含有相当于 0.15 mol 的 NaCl 单位；完全解离的一价盐相应提供同样物质的量的钠离子和氯离子。

模拟盒子太小，常用纳米来描述长度。1 nm 等于十亿分之一米，体积换算时要把长度的换算因子连乘三次，所以 1 nm³ 等于 10⁻²⁷ m³，也就是 10⁻²⁴ L。我们的盒子体积约为 193.424×10⁻²⁴ L。先把 17 个钠离子除以阿伏伽德罗常数，得到它们的物质的量，再除以体积，就得到钠离子的摩尔浓度。氯离子数也为 17，因此它的浓度相同。对于这个电中性的 NaCl 例子，盐的化学式单位浓度与任一种离子的浓度在数值上相等。

由粒子数计算摩尔浓度式 2

![由粒子数计算摩尔浓度](https://ml-biomat.com/static/agent-math/257497979f3e07ea10b6ac21.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| c | 所指定对象的摩尔浓度，本例按NaCl化学式单位或单种离子计 | mol/L；乘1000变成mM |
| N | 所计对象的数量；17对NaCl对应17个化学式单位 | 整数计数，无量纲 |
| N_{A} | 阿伏伽德罗常数6.02214076×10²³，每摩尔对象的数量 | mol⁻¹ |
| V_{L} | 以升为单位表达的整盒体积；下标L标明所用体积单位 | L |
| =, /, × | 等号、除法和乘法；分数线将N除以整个分母，相邻N_A与V_L相乘 | 运算符，无单位 |

怎样理解先用N/N_A把对象数换成摩尔数，再除以溶液体积；分母单位mol⁻¹×L使结果单位成为mol/L。

算一个例子N=17，V_L=193.4239779×10⁻²⁴ L，得到c=0.14594449 mol/L=145.94449 mM；18对给出154.52946 mM。

使用条件以当前盒体积定义平均浓度；局部水合层的浓度与整盒平均需要分别测量。对本例NaCl计化学式单位，不把正负离子数相加当作盐单位数。

按实际晶胞体积计算，17 对离子对应 0.145944 mol/L，即约 145.94 mM。mM 是毫摩尔每升，1000 mM 才等于 1 mol/L。命令里填写的目标是 150 mM，实际得到的数值稍低，是因为离子数必须是整数。在这个盒子里增加一对 NaCl，浓度会增加约 8.585 mM；18 对离子对应约 154.53 mM。目标值落在两个整数方案之间。放大模拟盒子后，同样增加一对离子引起的浓度变化会更小，这正是有限粒子数给小体系带来的分辨率。

这里还有一个容易混淆的数量：17 个钠离子加 17 个氯离子，一共是 34 个离子，但盐浓度不是把 34 直接代入 17 的位置。NaCl 的一个化学式单位同时提供正负两种离子，按化学式单位计数时仍然是 17。若关注全部离子粒子的总数密度，则可以把两种离子相加，并明确写成总离子浓度。不同物理问题需要不同的计数对象，术语后的定义比单独的数字更重要。后续讨论离子强度、渗透性质或扩散时，还会根据问题分别使用这些数量。

中和与加盐也需要分开理解。中和是让系统的净电荷达到所设定的目标，通常选择总电荷为零；加盐是为了建立一定浓度的正负离子环境。本例泛素在所选端基与 His68 状态下的净电荷为零，因此 17 个 Na⁺ 和 17 个 Cl⁻ 已经保持整个体系电中性。如果另一颗蛋白质带有 −5e 的净电荷，在同样加入 17 对 NaCl 后，还需要额外 5 个 Na⁺ 才能中和。此时钠离子数为 22，氯离子数为 17，两种离子的浓度不再相等，差别对应补偿蛋白质电荷的反离子。

一价盐体系的电荷计数式 3

![一价盐体系的电荷计数](https://ml-biomat.com/static/agent-math/a5706ea1e858b84d4c286486.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Q, Q_{p} | 系统总净电荷与蛋白质净电荷；下标p表示蛋白质 | C，或用e的倍数表达 |
| e | 正的元电荷，1.602176634×10⁻¹⁹ C | C |
| N_{Na}, N_{Cl} | Na⁺与Cl⁻的离子数量；Na和Cl下标标识化学种类 | 整数计数，无量纲 |
| Q/e, Q_{p}/e | 以元电荷为尺度的总净电荷与蛋白质净电荷 | 无量纲 |
| =, −, +, / | 等号、减法、加法与除法；每个Na⁺贡献+1，每个Cl⁻贡献−1 | 运算符，无单位 |

怎样理解把带电组分逐项相加；本例每个水的净电荷为零，所以在总电荷计数中不另加水项。

算一个例子本例17−17+0=0。若蛋白质带−5e，22−17−5=0，需比盐对多5个Na⁺。

使用条件适用于所列Na⁺、Cl⁻和中性水组成；多价离子或其他带电分子需要加入对应电荷数。

genion 的 -conc 按输入 TPR 中的整盒体积确定要加入的盐数量；-neutral 则在此基础上加入所需的中和离子。若系统原本已有离子，还要注意 -conc 所指定的盐是新增的，程序不会据已有离子自动扣减到一个最终总浓度。因此，给已经含盐的坐标再次执行同一条命令，会改变组成。实际准备中应保存每一步的计数，并在末态重新计算浓度。下面的交互把盒体积、离子对数与蛋白质电荷放在一起，便于看到哪个量影响浓度、哪个量决定额外的反离子。

调整离子对数与整盒体积，比较加盐和中和的数量关系。

[Figure: 钠离子和氯离子数量比较](https://ml-biomat.com/tutorials/molecular-dynamics/g06/#zh-s5)

按整盒体积进行的整数计数算例。反离子自动补偿蛋白质净电荷；离子位置和运动由后续分子动力学描述。

## 把建盒、加水和加盐连成可重复的操作

本节从上一讲选出的 protein.pdb 开始，它包含 1UBQ 的 A 链蛋白质重原子。脚本首先使用与上一讲相同的 pdb2gmx 选项建立拓扑：AMBER99SB-ILDN、TIP3P、显式选择 His68 的 HIE 状态，以及这一构建所使用的自由带电端基。这样，同一套输入可以独立重建本讲的准备步骤。命令前的 printf 把选择 1 交给组氨酸选项，对应氢位于 NE2 的中性状态；它依赖本例的残基组成和所列力场，因此更换蛋白质时应重新阅读交互提示与生成的拓扑。

editconf 读取 processed.gro，把蛋白质放到所选周期晶胞中；-c 表示居中，-d 1.0 与 -bt dodecahedron 一起确定盒型和初始尺度。居中会改变绝对坐标，却保留分子内部的距离与连接。接着 solvate 用 -cp 指定含蛋白质的盒子，用 -cs 指定溶剂坐标模板，以 -o 给出加水后的坐标，并通过 -p 更新拓扑末尾的水分子数量。这里每个输出文件都保留单独名字，便于比较加水前后究竟改变了什么。

genion 需要一个包含系统定义的 TPR 文件，所以加盐之前先执行 grompp。用于这一步的 ions.mdp 把 nsteps 设为零：它的作用是把坐标、拓扑与必要的计算设置编译成供 genion 读取的系统描述。脚本没有在这一阶段调用 mdrun，因而没有产生一段粒子运动。设置中的 PME 指定长程静电处理方式，1.0 nm 给出短程截断；这些条件与后续流程相协调。理解 TPR 在这里的用途，可以把“准备运行输入”和“已经运行模拟”两个状态分清。

### 为离子替换准备系统定义

```
integrator = steep
nsteps = 0
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
```

nsteps=0；此文件供grompp构建ions.tpr，随后由genion读取。

最后的 genion 命令使用 -pname NA 和 -nname CL 指定离子类型，-conc 0.15 设置加入盐的名义浓度，-neutral 要求中和总电荷，-seed 20261120 固定这一随机替换步骤的种子。选择 SOL 组表示从水分子中挑选替换位置。随机种子使同一准备条件下的选择可追踪，但初始离子位置只是后续动力学的起点；溶液的平衡分布需要通过运动建立。程序要求被替换的溶剂分子具有一致的组成，并按连续的溶剂组提供，这也解释了为什么这里选择完整的 SOL，而不是任意挑一批氧原子。

### 从选定蛋白质建立含盐水溶液

```
#!/usr/bin/env bash
set -euo pipefail

# protein.pdb contains the complete selected chain A of 1UBQ.
printf '1\n' | gmx pdb2gmx -f protein.pdb -o processed.gro -p topol.top \
    -i posre.itp -ff amber99sb-ildn -water tip3p -his
gmx editconf -f processed.gro -o boxed.gro -c -d 1.0 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
printf 'SOL\n' | gmx genion -s ions.tpr -o solvated-ions.gro -p topol.top \
    -pname NA -nname CL -conc 0.15 -neutral -seed 20261120
python inspect_solution.py . --output solution-analysis --language en
```

把protein.pdb、ions.mdp和inspect_solution.py放在同一例题目录；protein.pdb来自上一讲的A链选择。使用GROMACS 2026.4，末行生成计数与图。

运行后，最值得并排查看的是 solvated.gro、solvated-ions.gro 和 topol.top。前两个文件显示坐标与粒子数的变化，最后一个文件给出变化后的分子数。保持修改后的拓扑与对应坐标成对保存，就能在后续最小化时直接使用它们。若检查中发现数量不符，应回到产生不一致的那一步重新生成配套文件；手工随意增加或减少拓扑中的数字，只会让表面计数看起来匹配，却可能把某类分子的身份交给错误的坐标序列。

这些命令可以在准备好的 GROMACS 2026.4 环境中顺序执行。完整脚本把每一步失败都作为停止条件，使后面的操作不会继续使用缺失或不完整的输出。对第一次接触命令行的读者，最有效的学习方式是先读每行的输入与输出，再运行整个小体系，最后打开计数报告核对预测。此时你已经知道应该出现水分子、离子和新的盒信息，报告中的每个数字都有可解释的来处。

## 从真实输出中核对组成与浓度

下面的 Python 程序读取两个 GRO 坐标文件和拓扑的 molecules 区域，完成与本讲问题直接相关的检查。GRO 的前三个盒参数在正交盒中可以直接作为对角线；倾斜盒还会提供另外六个分量，程序按格式规定重排为三个晶胞矢量，再计算矩阵行列式的绝对值。行列式在这里给出带方向的平行六面体体积，绝对值保留实际占据空间的大小。这样，无论是否把蛋白质盒子显示成一个端正的立方体，浓度都从真正的周期几何出发。

计数时，程序根据本例 TIP3P 的 OW 名称统计水分子数，并核对每个水对应三个位点；NA 与 CL 按单原子离子计数。它还检查加盐前后的晶胞相同、减少的水分子数等于加入的离子数，以及坐标计数与拓扑计数一致。这样的检查与本例的命名和三位点水组成相联系。若换成四位点水、其他离子命名或多个蛋白质分子，就要相应更新计数规则，而保留“模型组成决定如何计数”的思路。

### 完整Python：核对组成、体积与盐浓度

```
"""Count molecules and quantify salt concentration in the prepared solution."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AVOGADRO = 6.02214076e23


def gro(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n = int(lines[1])
    rows = [dict(resid=int(line[:5]), resname=line[5:10].strip(),
                 name=line[10:15].strip(),
                 xyz_nm=[float(line[i:i+8]) for i in (20, 28, 36)])
            for line in lines[2:2+n]]
    v = [float(x) for x in lines[2+n].split()]
    if len(v) == 3:
        cell = np.diag(v)
    elif len(v) == 9:
        cell = np.array([[v[0], v[3], v[4]],
                         [v[5], v[1], v[6]],
                         [v[7], v[8], v[2]]])
    else:
        raise ValueError("A GRO cell requires three or nine components.")
    return rows, cell


def molecule_counts(path):
    counts, section = {}, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split(";", 1)[0].strip()
        if line.startswith("["):
            section = line.strip("[] ")
        elif section == "molecules" and line and not line.startswith("#"):
            name, count = line.split()[:2]
            counts[name] = counts.get(name, 0) + int(count)
    return counts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    p.add_argument("--output", type=Path, default=Path("solution-analysis"))
    p.add_argument("--language", choices=("zh", "en"), default="en")
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    before, cell0 = gro(args.directory / "solvated.gro")
    after, cell = gro(args.directory / "solvated-ions.gro")
    top = molecule_counts(args.directory / "topol.top")
    if not np.allclose(cell, cell0):
        raise ValueError("Ion replacement should preserve the initial cell.")
    water_before = sum(a["resname"] == "SOL" and a["name"] == "OW" for a in before)
    water_after = sum(a["resname"] == "SOL" and a["name"] == "OW" for a in after)
    water_sites = sum(a["resname"] == "SOL" for a in after)
    na = sum(a["resname"] == "NA" for a in after)
    cl = sum(a["resname"] == "CL" for a in after)
    protein_atoms = len(after) - water_sites - na - cl
    assert water_sites == 3 * water_after
    assert (top["SOL"], top["NA"], top["CL"]) == (water_after, na, cl)
    assert top["Protein_chain_A"] == 1
    assert water_before - water_after == na + cl
    volume = float(abs(np.linalg.det(cell)))
    litre_volume = volume * 1e-24
    pair_increment_mM = 1000 / (AVOGADRO * litre_volume)
    summary = dict(initial_cell_vectors_nm=cell.tolist(),
                   initial_cell_volume_nm3=volume,
                   protein_atoms=protein_atoms, waters_before=water_before,
                   waters_after=water_after, sodium_ions=na, chloride_ions=cl,
                   total_atoms=len(after), topology_molecules=top,
                   sodium_concentration_mM=na*pair_increment_mM,
                   chloride_concentration_mM=cl*pair_increment_mM,
                   one_pair_increment_mM=pair_increment_mM,
                   nominal_added_salt_mM=150,
                   ionic_charge_e=na-cl,
                   atom_count_expected=protein_atoms+3*water_after+na+cl)
    (args.output / "solution_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (args.output / "salt_count_concentration.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["NaCl_pairs", "concentration_mM"])
        writer.writerows((n, n*pair_increment_mM) for n in range(36))
    zh = args.language == "zh"
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts,
                         "font.size": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    axes[0].bar([0, 1], [water_before, water_after], color=["#a9c9c0", "#257d85"])
    axes[0].set_xticks([0, 1], ["加盐前", "加盐后"] if zh else ["Before ions", "After ions"])
    axes[0].set_ylabel("水分子数" if zh else "Water molecules")
    axes[0].set_ylim(0, water_before*1.15)
    for i, n in enumerate([water_before, water_after]):
        axes[0].text(i, n+80, str(n), ha="center")
    axes[1].bar([0, 1], [na, cl], color=["#b6773f", "#567795"])
    axes[1].set_xticks([0, 1], ["Na⁺", "Cl⁻"])
    axes[1].set_ylim(0, max(na, cl)*1.2)
    axes[1].set_ylabel("离子数" if zh else "Ions")
    for i, n in enumerate([na, cl]):
        axes[1].text(i, n+.4, str(n), ha="center")
    n = np.arange(36)
    axes[2].plot(n, n*pair_increment_mM, color="#8fa8a1", lw=1.5)
    axes[2].scatter(n, n*pair_increment_mM, color="#257d85", s=20)
    axes[2].axhline(150, color="#b6773f", linestyle="--", label="150 mM")
    axes[2].scatter([na], [na*pair_increment_mM], color="#b6773f", s=80, zorder=4)
    axes[2].set_xlabel("NaCl离子对数" if zh else "Number of NaCl pairs")
    axes[2].set_ylabel("按整盒体积计算的浓度 / mM" if zh else "Whole-cell concentration / mM")
    axes[2].legend(frameon=False)
    for ax in axes:
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle("泛素溶液：组成与整数离子数" if zh else "Ubiquitin solution: composition and integer ion counts", fontsize=19)
    fig.savefig(args.output / "solution_composition.svg")
    fig.savefig(args.output / "solution_composition.png", dpi=150)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

依赖NumPy和Matplotlib。读取同目录solvated.gro、solvated-ions.gro与topol.top；--language zh或en选择图的语言。

实际输出中，加盐前有 5902 个水分子，加盐后为 5868 个；差值 34 正好等于 17 个钠离子与 17 个氯离子的总数。泛素的 1231 个原子保持不变，加盐后的总原子数为 1231+3×5868+17+17=18869。这里的加号把不同组分的位点数相加，乘号把每个水的三个位点乘以水分子数。也可以从另一条路径复核：加盐前有 18937 个位点，34 次三位点水替换成单个位点离子，共减少 68，得到同样的 18869。两条计数路径相互吻合，说明水与离子的替换关系清楚。

### 泛素溶液的实际组成

初始周期晶胞193.4239779 nm³；加盐前5902水，加盐后5868水、17 Na⁺与17 Cl⁻。右图按整盒体积计算整数离子对对应的浓度，橙点为实际采用的17对。

GROMACS2026.4；PDB 1UBQ链A、76个残基；AMBER99SB-ILDN与TIP3P。保留602个实验重原子，加入629个氢原子；His68选中性NE2质子化状态，采用带电游离末端。

[下载参考数据与完整输入（ZIP） 0.53 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-solution-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g06/#zh-s7)

由实际GRO和拓扑核对的溶液组成。17个Na⁺和17个Cl⁻替换34个完整水分子。右图用初始晶胞的193.4239779 nm³体积换算整对离子浓度；每增加一对离子都会使浓度离散地增大。

图的左侧显示水分子数量略有减少，中间显示正负离子数量相等，右侧把所有整数离子对数转换为整盒浓度。150 mM 的水平虚线落在 17 与 18 对离子对应的两个点之间，而实际准备结果位于 17 对的点上。把连续的浓度刻度与离散的分子数同时画出来，比单独报告“150 mM”更能说明这个小体系究竟包含什么。数值报告保留更多有效数字以便核对计算，讨论模型条件时使用约 146 mM 已经足够清晰。

这些图记录的是系统准备阶段的组成与几何。它们能回答“加入了多少水和盐、文件是否彼此一致”，而水的局部排列、蛋白质附近的离子富集、密度与压力的时间变化，将由后续轨迹回答。特别是在恒压阶段，粒子数保持固定而盒体积变化，按瞬时体积计算的浓度也会随之变化。因此，研究报告可以同时说明名义加盐条件、实际离子数和所分析轨迹的平均体积，让其他人准确理解浓度的定义与所处阶段。

## 让溶液条件与研究问题保持一致

现在的系统已经具有明确的化学组成、周期几何和参数来源，下一步是让初始位置在这些相互作用下调整。刚铺入的水与随机替换的离子还没有经历充分的局部重排，蛋白质也需要适应当前溶液环境。能量最小化首先处理过近接触，随后在所选温度与压力下逐步准备动力学状态。把“组成准备”和“状态准备”分成两个有联系的阶段，有助于定位问题：数量或电荷不对时回到本讲，温度、体积或局部接触异常时再检查下一讲的具体过程。

对于泛素表面运动这样的入门问题，这个体系已经可以提供一个清楚的起点：一个自由单体、显式水、一价盐环境、固定的质子化选择和周期边界。蛋白质净电荷为零也并未抹去表面正负电荷区域，水与离子仍会对这些区域作出不同响应。后面观察结构波动时，应同时想到溶液中的这些相互作用，而不是把泛素当作在真空中自行摆动的物体。相同的建模逻辑也会延伸到 DNA、糖链和聚合物溶液，只是各体系需要的分子参数和具体问题不同。

如果研究目标改为某种盐对蛋白质结构的影响，比较设计就应围绕这个变化展开：尽量保持蛋白质模型、温度、压力、分析定义和准备步骤一致，明确改变的是离子种类还是盐含量，并核对实际粒子数与最终体积。较小盒子中的浓度步进可能使两个名义条件落到相同的整数离子数，此时需要调整体系尺度或选择能在粒子数上区分的条件。通过这种检查，实验问题会被转化成真正不同且可比较的计算系统。

另一些问题更关心单个离子长期停留的部位、稀有接触或者盐引起的缓慢构象改变。这些过程需要相应的采样时间与重复模拟，也需要关注离子参数是否适合所研究的配位环境。明确这些条件可以帮助选择下一步该测量什么：短时间的局部水合变化、较稳定的平均分布，或者跨越多个构象状态的概率。一个准备正确的溶液盒子为这些研究提供共同基础；真正的结论则由与问题匹配的轨迹、统计量和模型检验逐步形成。

回看本讲的准备结果，每个数字已经可以对应到具体物理意义：193.424 nm³ 是初始周期晶胞体积，5868 是剩余的水分子数，17 与 17 是正负离子数量，约 146 mM 是按整盒体积算出的盐浓度，18869 是程序实际推进的原子位点总数。理解这些数值之后，建盒、溶剂化和加盐就成为一组可检查的建模决定。下一讲会从这份组成明确的系统出发，观察能量、温度和体积如何帮助我们准备一段可分析的蛋白质动力学轨迹。

## 延伸阅读与开放资料

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  建盒、加水、准备TPR与离子替换流程。

  沿用操作顺序，改为1UBQ/AMBER99SB-ILDN/TIP3P；补充晶胞体积、整数盐浓度和组成检查。
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  蛋白质水溶液的准备与拓扑更新顺序。

  采用泛素小体系，使用2026.4命令，加入双语长文、计数图与完整分析程序。
- [gmx editconf — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-editconf.html) · GROMACS developers · GROMACS documentation terms; factual reference

  命令选项与几何、计数行为核对。

  独立说明本例使用的参数与输出。
- [gmx solvate — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-solvate.html) · GROMACS developers · GROMACS documentation terms; factual reference

  命令选项与几何、计数行为核对。

  独立说明本例使用的参数与输出。
- [gmx genion — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-genion.html) · GROMACS developers · GROMACS documentation terms; factual reference

  命令选项与几何、计数行为核对。

  独立说明本例使用的参数与输出。
- [The Nobel Prize in Chemistry: The Development of Modern Chemistry](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-chemistry-the-development-of-modern-chemistry/) · Bo G. Malmström; Bertil Andersson; Nobel Foundation · Public historical reference; factual discussion

  Arrhenius电解质解离研究的历史背景。

  以溶液粒子概念重新叙述，配离子迁移概念图。
- [Comparison of simple potential functions for simulating liquid water](https://doi.org/10.1063/1.445869) · William L. Jorgensen; Jayaraman Chandrasekhar; Jeffry D. Madura; Roger W. Impey; Michael L. Klein · Publisher copyright; factual citation

  1983年水模型比较与TIP3P的科学背景。

  概述模型思想；水位点与电荷关系用概念示意表达。
