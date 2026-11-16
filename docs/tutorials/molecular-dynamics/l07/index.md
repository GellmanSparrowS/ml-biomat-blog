# 一条高分子链的形状与运动

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l07/
Language: zh-CN

沿着真实PEG轨迹区分端点、轮廓与整体尺寸，观察恒力怎样改变构象，并从两个端点的位移计算外力功。

## 一根柔软的连接臂，怎样量它的大小

把一根鞋带平放在桌面上，可以摆成直线、弯曲的弧，也可以绕成一团。鞋带本身没有变短，两端之间的直线距离却变了。高分子链也有类似的几何自由：连接关系相同的一条链，在水中可以采取许多空间形状。这种柔软性让聚合物能够充当分子之间的连接臂和间隔层。连接臂需要允许两个对象靠近或分开，表面上的链则会占据周围一部分空间；两种用途都关心链的尺寸，但所需要的“尺寸”未必是同一个量。

本节回到前面已经放入水中的短PEG链。它含8个氧乙烯重复单元，分子式C₁₆H₃₄O₉，共59个显式原子，周围有670个柔性SPC/Fw水分子。先观察链在没有外加拉力时怎样变形，再沿x方向给两端氧原子施加大小相同、方向相反的恒定外力。我们会同时测量两端距离、沿拉力方向的投影、主链轮廓长和质量加权回转半径。把这些量放在同一段轨迹上比较，就能区分整体转向、局部弯曲和真正的空间伸展。

这里“运动”包含几种层次。整条链可以在水中平移，也可以保持内部形状而转动，还可以通过键角和二面角变化改变构象。把镜头跟着链移动，只会消除画面里的整体平移，链内部的变化仍然看得见。当前输入让PEG与周围水共同平移以保持链居中，适合研究相对位置和内部构象。我们因此把分析重点放在内部几何上。将来研究链在实验室坐标中的扩散时，再使用保留整体位移的轨迹与相应的周期解包方法，使记录方式与待测量的运动一致。

水在这个过程中一直参与运动。链的一段转向时，原先邻近的水可能离开，新的水靠近，局部相互作用随之变化；水的碰撞也持续改变链上原子的速度。因此，即使没有外加拉力，链也不会静止在一幅最漂亮的构象上。温度相同并不要求每一帧形状相同，而是给这些运动规定热能尺度。把柔软链想成水中不断调整姿态的细绳，比把它想成真空里的一根静止弹簧更接近当前模型。后面看到尺寸随时间上下波动时，首先应把它理解为需要统计的热运动，再检查是否有持续的准备过程或受力趋势。

这个例子的长度和时间都可以直接把握。1Å是0.1nm，链的两端距离在数Å到约30Å之间变化，对应不到几纳米的尺度。1ps等于1000fs，本例每个时间步是1fs，两个观察阶段各持续15ps。如此短的链和短时间片段足以演示如何施力、如何识别构象及如何读取变化；描述更长聚合物的平均尺寸、慢松弛或实验力谱时，接着增加链长、采样时间和独立重复。先用清楚的小例子把每个测量定义做对，后续扩展才有可比较的基础。

## 同一条链为何需要许多幅图：从连接关系走向构象统计

理解大分子是由共价键连接的长链之后，另一个问题自然出现：这样的链在空间里通常是什么样子？化学式说明有哪些原子，连接表说明谁与谁相连，却没有给出唯一的三维形状。单键附近的转动、键角变化以及相邻原子的排斥，使同一连接关系对应许多构象。用一幅画代表所有构象，就像只用一次天气快照描述一个季节。我们需要同时关注某一时刻的形状、这些形状出现的频率，以及从一种形状转到另一种需要多久。

Flory在1974年的诺贝尔演讲中以大分子链的空间构象为主题，将链的化学连接与其丰富的空间排列联系起来。这一视角让“分子结构”从一张静态结构式拓展为可统计的构象集合。下面的历史概念图保留同样的连线顺序，让链在几个不同位置弯曲；每幅图都代表同一连接关系的一种空间安排。图旁的尺寸分布则提醒我们，平均尺寸来自一组构象的权重。计算平均之前，需要先说明采集了哪些构象、采集条件是什么，以及它们在记录里怎样被计数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s2)

图 1 · 从静态连接关系走向构象集合的历史概念图；下方分布表示统计视角。

柔软的链通常有很多弯曲排列，而接近完全伸直的排列受到较多几何限制。可以用一串方向可变的短杆理解这一点：允许每根短杆选择很多方向时，组合方式很多；要求所有短杆都指向同一方向时，允许的组合就少了。这与构象熵有关，熵在这里反映可访问排列的多少。拉伸会改变这些排列的权重，所以链的回复趋势并不一定来自每一根化学键像金属弹簧那样显著拉长。对于具体分子，还要把键转动能量、相邻原子排斥和溶剂重排共同考虑进去。

PEG与水的耦合尤其适合说明溶剂的重要性。Liese等人的单分子力谱与分子模拟研究讨论了强拉伸下水化如何参与PEG的弹性响应，说明链构象与周围水的变化可以相互影响。当前例子承接的是观察这种问题所需的建模与测量步骤：同一条链在相同水环境中先自由运动，再受到恒力，比较其几何变化。我们保留给定的PEG与SPC/Fw参数组合，并把短时间响应与平衡统计分别叙述。若进一步研究水化的能量和熵贡献，就需要额外的水结构分析、不同条件采样和相应的热力学计算。

## 端点距离、方向投影和轮廓长各回答什么

首先把两端定义清楚。本例的拉力作用于链两端羟基中的氧原子，它们的类型名是OAlc；端点不是水里的氧，也不是端羟基的氢。给定左端位置和右端位置，用右端减左端得到端到端向量。这根箭头保留方向，其长度就是两端之间的直线距离。若只取箭头在x轴上的分量，就得到沿拉力方向的投影。两端距离始终非负，投影则可以带正负号；符号取决于所选端点顺序与坐标方向。实际程序从初始帧确定两端身份，后续始终跟踪同一对原子。

端到端向量、距离和拉力方向投影式 1

![端到端向量、距离和拉力方向投影](https://ml-biomat.com/static/agent-math/d263004afb198becaf6a3559.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| rR, rL | 固定身份的右、左端氧位置向量 | Å |
| R | 从左端指向右端的端到端向量 | Å |
| Re | 端到端向量的长度，即端点直线距离 | Å |
| Rx, Ry, Rz, X | 向量的三个分量，以及沿x施力方向的有符号投影 | Å |
| R, L, e, x, y, z | 下标分别标记右端、左端、端点距离和坐标方向 | 1 |
| −, \|…\|, √, ², +, = | 位置相减得到位移；竖线取向量长度；分量平方相加后开正平方根；等号连接定义 | 1 |

怎样理解三个垂直方向的距离平方相加给三维距离平方；投影则只保留指定轴分量。

算一个例子R=(3,4,0)Å时，Re=√(9+16)=5Å，X=3Å；整体转向x轴可得到X=5Å而Re不变。

使用条件用同一对端氧的解包坐标计算，端点身份在整段轨迹中保持一致。

假设端到端向量为(3,4,0)Å，两端距离就是5Å，而x投影只有3Å。保持这条链的内部形状不变，把它整体转向x轴，可以让投影增大到5Å，但两端距离仍然是5Å。这个简单例子说明，看到x方向长度增加时，要同时检查链是否只是转了方向。当前实际轨迹在施加外力后，两端距离和x投影逐渐接近，说明端到端方向与拉力方向趋于一致；两者的共同增大则进一步表明链的端点确实分得更开。把两个量同时画出来，比只看一个坐标差更完整。

沿指定主链路径相加得到轮廓长式 2

![沿指定主链路径相加得到轮廓长](https://ml-biomat.com/static/agent-math/316255eb74598990c876772f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Lc | 沿两端氧之间共价路径的总长度 | Å |
| ra, rₐ₊₁ | 该路径上相邻两个原子的位置向量 | Å |
| Nb, a | 路径中的键数与键的编号 | 1 |
| Re | 同一对端点的直线距离 | Å |
| Σ, \|…\|, −, +, ≤, = | 逐段求和；竖线取每段长度；坐标相减；a+1为下一点；直线距离不大于路径总长；等号定义 | 1 |

怎样理解沿路径累积每段实际长度，保留弯曲路线；三角不等式给出端点距离的上界。

算一个例子两根长度各1Å的垂直连接，轮廓长2Å，端点距离√2Å约1.414Å。

使用条件本例为唯一的25原子、24键主链路径；柔性键使轮廓长随帧小幅变化。

轮廓长则沿着主链一段一段走。程序从一个端氧沿共价连接找到另一个端氧，得到包含25个主链原子、24根连接的路径，再把每根连接的实际长度相加。侧面的氢连接不在这条端到端路径上，因此不会全部加入轮廓长。轮廓长像沿鞋带表面量出的长度，端点距离像直接拉一根直尺跨过两端。折线的总长度不小于两端的直线距离；只有每段都沿同一方向排齐时，才可能相等。这项几何关系也可以作为分析程序的检查。

沿路径行走与直接连接端点之间，还有一个容易理解的向量关系。把每一段键向量首尾相接，中间原子的位置会在相邻两项中一正一负相消，最后剩下的就是端到端向量。若先把每段都换成正的长度再相加，弯曲方向的信息便被去掉，得到轮廓长。两种加法保留的信息不同，所以数值不同。当前PEG的主链路径由连接表唯一确定；面对支化分子或带环结构时，先指定哪两个端点、沿哪条化学路径测量，才能给“轮廓长”同样清楚的含义。这个原则以后分析交联网络时也会继续使用。

实际结果中，无外加拉力阶段的平均轮廓长约35.20Å，恒力阶段约35.39Å；平均两端距离却从约7.39Å增加到约28.29Å。两种变化量相差很大，直接说明本次端点分离主要伴随着已有主链路径在空间中的重新排布，而不是把每根键拉长到原来的几倍。具体哪些二面角变化、溶剂怎样配合，还可以进一步逐项分析。轮廓长也不是不变的数学常数：本例采用柔性键，键长会振动，因此应从每一帧实际坐标计算，再观察它的分布。

端点接近也不意味着整条链都缩成了一个小点。一条很长的弯曲链可以让两端相遇，中间部分却伸到很远；反过来，许多局部折叠也可能集中在相对紧凑的区域。因此，两端距离特别适合回答连接臂两头能相隔多远，却没有使用链中间所有原子的位置。若关心链整体占据空间的尺度，例如它与邻近分子是否容易接近，就需要一个同时考虑所有原子的尺寸量。回转半径正是为这类问题提供的测量。

## 回转半径：让每个原子都参与尺寸测量

计算回转半径之前，先找到链的质心。质心可以理解为把整个分子的质量分布集中后对应的平衡位置：较重的原子对它影响更大。把每个原子的位置乘以质量，再把这些结果相加，最后除以总质量，就得到质量加权的位置平均。对本例而言，碳、氧和氢的质量不同，所以简单把59个坐标等权平均，得到的是几何中心，通常与质心不同。LAMMPS的compute gyration使用质量加权定义，独立分析也必须保持同样的权重。

用质量加权找到链的质心式 3

![用质量加权找到链的质心](https://ml-biomat.com/static/agent-math/efb9ee4e815e85ed580ab7a2.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| M, mi | 整条链的总摩尔质量与原子i的摩尔质量数值 | g mol⁻¹ |
| ri, rcm | 原子i的位置与质量加权质心位置 | Å |
| N, i | 所选链原子总数和原子编号 | 1 |
| cm | 质心下标 | 1 |
| Σ, /, ×, = | 求和累积质量或质量乘位置；除以总质量；等号定义 | 1 |

怎样理解每个位置按质量贡献权重，除以总质量使所有权重之和为1。

算一个例子位置0Å和4Å的两个点，质量比1:3，质心为(1×0+3×4)/4=3Å。

使用条件所有位置来自同一解包坐标表示；碳、氧和氢分别使用对应参数质量。

找到质心后，计算每个原子到它的距离，先平方，再按质量平均，最后开平方，这就是回转半径。平方让各方向的距离都以正值贡献，并让离中心较远的原子产生较大影响；最后开平方把单位从长度平方恢复为长度。可以把它理解为质量分布相对于中心的均方根尺度。它并不是包住所有原子的最小球半径，链上仍然可能有原子位于这个数值之外。名称里的“半径”表达的是一种整体尺度，而不是一层所有原子都必须落在其中的硬边界。

质量分布相对质心的均方根尺度式 4

![质量分布相对质心的均方根尺度](https://ml-biomat.com/static/agent-math/79cf2c37cc2dc098dd703113.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Rg | 质量加权回转半径 | Å |
| Rg,x, Rg,y, Rg,z | 各坐标方向的质量加权均方根尺寸 | Å |
| ri, rcm | 原子位置与质心位置向量 | Å |
| mi, M | 原子与整条链的质量，采用一致单位 | g mol⁻¹ |
| N, i | 原子总数与求和编号 | 1 |
| g, x, y, z | g标记回转半径；x、y、z标记坐标方向 | 1 |
| Σ, −, \|…\|, ², √, /, ×, +, = | 位置减质心、取距离平方、按质量求和平均、最后开方；方向平方贡献相加 | 1 |

怎样理解平方使各方向偏离都作正贡献；质量平均后开方得到长度尺度。

算一个例子两点0Å和4Å，质量比1:3，质心3Å，Rg=√[(1×9+3×1)/4]=√3Å≈1.732Å。

使用条件标量对整体平移和旋转不变；分方向尺寸依赖坐标轴。本例与LAMMPS质量加权定义一致。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s4)

图 2 · 同一折线上的轮廓、端点与质量尺度。虚线圆半径取该等质量点集的回转半径，质心用十字标出。

用两个点就能看清质量权重的影响。两点位于0Å和4Å，质量相同，质心在2Å，回转半径为2Å。若右侧质量是左侧的3倍，质心移到3Å，按质量求出的回转半径变成√3Å，约1.732Å。两个点的几何距离没有变，但质量在空间里的分布发生了变化。对真实PEG，我们从参数读取每类原子质量，算得总摩尔质量约370.4426g/mol。这样得到的回转半径与按等权重小珠定义的粗粒化链尺寸属于不同的测量约定，比较时应把权重定义一起写出。

整体平移不改变回转半径，也可以从计算过程直接看出来。若给所有原子的位置都加上相同位移，质心也增加同样位移；原子位置减去质心时，这一共同项正好相消。整体转动则保持每个原子到质心的距离，所以质量加权平均距离平方也保持不变。正因为有这两种性质，回转半径能够把分子“在哪里、朝哪个方向”与“内部展开到什么程度”区分开。质量数值虽然使用g/mol，只要分子和分母采用同一单位，质量因子会相除，最后留下的仍然是长度单位。

几何练习：五个点由四根1Å线段连接。改变折叠、整体方向或第5点的质量。

[Figure: 五点链的几何与质心](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s4)

五点几何模型中每段长度固定。折叠参数控制交替线段方向，整体转动保留标量尺寸，质量选择控制加权方式。

交互练习用一条五点折线把几何因素分开。改变折叠角时，四段长度保持不变，端点距离和回转半径随形状变化；转动整条折线时，这两个标量保持不变，而x方向投影改变；切换最后一个点的质量时，质心和质量加权回转半径改变，端点距离则保持原值。这些操作帮助我们辨认一个量究竟依赖什么。实际分析还可以把回转半径平方拆成x、y、z三个方向的贡献；三项相加得到总回转半径平方，分别开平方则展示各方向的均方根尺寸。

周期边界的处理同样决定尺寸是否正确。一条跨过盒边的链在包装坐标中会显得被分成两部分，直接计算质心可能把它放在盒子中央的错误位置。这里保存的xu、yu、zu是已经根据周期像信息解包的坐标，保持链在空间里的连续性。我们用这些坐标逐帧重算回转半径，再与LAMMPS记录比对，最大差约1.39×10⁻⁵Å，符合保存坐标的有限精度。这个核对同时检查了原子选择、质量权重、周期几何和公式实现，任何一项混用都可能造成明显偏差。

## 让同一条链先松动，再承受明确的恒力

准备好的merge.restart包含链、水、坐标、速度、盒子和相互作用设置。拉伸输入先读取它，再恢复长程静电求解设置，选出两个OAlc端氧。程序用这两个氧的初始x位置判断谁在右侧、谁在左侧，然后创建两个固定成员的分组。后面即使链弯曲或转动，受力对象仍然是这两个已经选定的原子。这里的原子变量用于建组时判断成员，分组不会每一步根据当前谁更靠右重新交换身份。这个细节保证施力协议与后续端点跟踪一致。

### 完整两阶段链运动与恒力输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart merge.restart

group ends type OAlc
variable xcm equal xcm(ends,x)
variable oxies atom type==label2type(atom,OAlc)
variable end1 atom v_oxies*(x>v_xcm)
variable end2 atom v_oxies*(x<v_xcm)
group topull1 variable end1
group topull2 variable end2


timestep 1.0
fix mynvt all nvt temp 300 300 100
fix myrct PEG recenter 0 0 0 shift all

compute rgyr PEG gyration
compute dphi PEG dihedral/local phi

thermo_style custom step temp etotal c_rgyr
thermo 250

dump mydmp all local 50 pull.dat index c_dphi


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file pull-thermo.dat format " %.15g"
dump trajectory all custom 250 pull.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 pull-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 15000

write_restart unforced.restart
write_data unforced.data

fix myaf1 topull1 addforce 10 0 0
fix myaf2 topull2 addforce -10 0 0

run 15000
write_restart pulled.restart
write_data pulled.data
```

从merge.restart继续，先无外力15ps，再施力15ps。

读取准备状态后，模拟时间从25ps继续。先运行15000步NVT，到40ps结束无外加拉力阶段；再对右端加+x方向的10kcal/(molÅ)，对左端加−x方向的同样大小外力，并继续15000步到55ps。每端的力约为694.77pN。恒力表示加到原子上的这部分外力每步保持给定值，原子的速度和位移仍由全部作用力共同决定。它与固定速度把端点拖走的协议不同：本例没有预先指定链每皮秒增长多少，伸展速度从链、溶剂、热浴和外力的共同响应中产生。

施力命令还要与分组大小一起读。addforce给组内每个原子添加指定分量，如果一个组里有10个原子，写入10这个力值就意味着每个原子都受到10，而不是全组共同分到10。本例两个受力组各只有一个端氧，所以每端外力大小与命令参数直接对应。复制这个方法到较大的端基或一段链时，先决定控制的是每原子力还是整个选区的总力，再按成员数处理。与此同时，记录受力原子的编号比只记“左边那一团”可靠，因为分子会在运动中改变形状和朝向。

NVT把温度目标保持在300K，体积沿用前面准备后的数值，因此本段密度固定在约0.94018g/cm³。这个实际准备状态必须跟随结果一起保留：更换水模型、延长压力松弛或改变体积，都可能改变水化和链响应。原参数组合给出了一个清楚的原子级操作实例。若要与某种实验力谱比较，就围绕实验的温度、溶剂组成、链长和拉伸协议检查参数与采样，并记录准备后的密度和构象。这样，模型条件与比较目标通过具体可测量的量连接起来。

### 从水开始运行完整例题

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=2
"$lmp" -in water.lmp -log water.log > water.stdout.log 2>&1
"$lmp" -in merge.lmp -log merge.log > merge.stdout.log 2>&1
"$lmp" -in pull.lmp -log pull.log > pull.stdout.log 2>&1
```

在例题目录执行bash run.sh；LAMMPS环境变量可指定可执行程序。

完整运行脚本按水准备、插入PEG、链运动与拉伸的顺序调用三个输入。它将日志分别保存在对应文件中，便于确认每个阶段的原子数、时间和状态。下面保留全部配套输入，重新运行时把它们放在同一个例题目录。水模板与PEG模板定义初始几何及连接，参数文件定义作用形式所需的系数，准备输入产生后续读取的状态文件。依赖关系因此是一条可以从头执行的链：先得到水，再得到水中的PEG，最后得到本节的两阶段轨迹。

### 完整水准备输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units real
atom_style full
bond_style harmonic
angle_style harmonic
dihedral_style harmonic
pair_style lj/cut/coul/long 10
kspace_style ewald 1e-5
special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes

region box block -30 30 -15 15 -15 15
  create_box 8 box &
  bond/types 7 &
  angle/types 8 &
  dihedral/types 4 &
  extra/bond/per/atom 3 &
  extra/angle/per/atom 6 &
  extra/dihedral/per/atom 10 &
  extra/special/per/atom 14

include parameters.inc

molecule h2omol water.mol
create_atoms 0 random 700 87910 NULL mol h2omol 454756 overlap 1.0 maxtry 50

group H2O type OW HW
minimize 1.0e-4 1.0e-6 100 1000
reset_timestep 0

fix mynpt all npt temp 300 300 100 iso 1 1 1000


thermo 500
thermo_style custom step temp etotal vol density


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho file water-thermo.dat format " %.15g"
dump trajectory all custom 250 water.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id

timestep 1.0
run 15000

write_restart water.restart
# write_data water.data # uncomment to write a .data file as well
write_data water.data
```

生成700个水并保存water.restart。

### 完整PEG插入与准备输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart water.restart

molecule pegmol peg.mol
create_atoms 0 single 0 0 0 mol pegmol 454756

group PEG type C CPos H HC OAlc OE

delete_atoms overlap 2.0 H2O PEG mol yes


fix mynpt all npt temp 300 300 100 x 1 1 1000
fix myrct PEG recenter 0 0 0 shift all
timestep 1.0

thermo 500

# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file merge-thermo.dat format " %.15g"
dump trajectory all custom 250 merge.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 merge-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 10000

write_restart merge.restart
# write_data merge.data # uncomment to write a .data file as well
write_data merge.data
```

插链后删除重叠整水并保存merge.restart。

### 完整PEG与SPC/Fw参数

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

labelmap atom 1 OE 2 C 3 HC 4 H 5 CPos 6 OAlc 7 OW 8 HW
labelmap bond 1 g4 2 g18 3 g26 4 g27 5 g56 6 g71 7 OW-HW
labelmap angle 1 g12 2 g13 3 g14 4 g15 5 g51 6 g56 7 g102 8 HW-OW-HW
labelmap dihedral 1 g23 2 g34 3 g46 4 glj14

mass OE 15.9994 # PEG O (GROMOS 54A7)
mass C 12.011 # PEG C (GROMOS 54A7)
mass HC 1.008 # PEG H (GROMOS 54A7)
mass H 1.008 # PEG H (GROMOS 54A7)
mass CPos 12.011 # PEG C (GROMOS 54A7)
mass OAlc 15.9994 # PEG O (GROMOS 54A7)
mass OW 15.9994 # H2O O (SPC/Fw)
mass HW 1.008 # H2O H (SPC/Fw)

pair_coeff OE OE 0.2526 2.8492
pair_coeff C C 0.0663 3.5812
pair_coeff HC HC 0.0283 2.3734
pair_coeff H H 0.0 0.0
pair_coeff CPos CPos 0.2450 2.8114
pair_coeff OAlc OAlc 0.1195 3.1000
pair_coeff OW OW 0.155 3.165
pair_coeff HW HW 0.0 0.0

bond_coeff g4 1109.2926 1.12
bond_coeff g18 399.7916 1.43
bond_coeff g26 299.8440 1.52
bond_coeff g27 400.0343 1.53
bond_coeff g56 310.7075 1.41
bond_coeff g71 179.2543 0.971
bond_coeff OW-HW 529.581 1.012

angle_coeff g12 47.6940 109.5
angle_coeff g13 55.1271 109.5
angle_coeff g14 47.6350 109.6
angle_coeff g15 55.1139 111.0
angle_coeff g51 54.9931 110.3
angle_coeff g56 180.4602 109.0
angle_coeff g102 30.1731 110.0
angle_coeff HW-OW-HW 37.95 113.24

dihedral_coeff g23 0.3011 1 3
dihedral_coeff g34 1.4149 1 3
dihedral_coeff g46 0.2390 -1 3
dihedral_coeff glj14 0.0 1 1
```

几何、作用形式和参数组合与本次实际运行一致。

### 完整柔性水模板

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

3 atoms
2 bonds
1 angles

Coords

1 0 0 0 # H2O O
2 1.012 0 0	# H2O H
3 -0.4 0.929 0 # H2O H

Types

1 OW
2 HW
3 HW

Charges

1 -0.82 # H2O O (SPC/Fw)
2 0.41 # H2O H (SPC/Fw)
3 0.41 # H2O H (SPC/Fw)

Bonds

1 OW-HW 1 2
2 OW-HW 1 3

Angles

1 HW-OW-HW 2 1 3
```

配套水模板与上述参数同时使用。

### 完整59原子PEG模板

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PEG molecule

59 atoms
58 bonds
104 angles
116 dihedrals

Coords

1 -3.0661409 -3.1122069 -1.2331413
2 -3.0905955 -3.1901295 -0.3069935
3 -1.7871211 -3.4628029 0.1677571
4 -1.7892607 -3.9757321 1.1640826
5 -1.4364998 -2.4400568 0.4558979
6 -0.9585523 -4.2486658 -0.9052389
7 -1.5905948 -5.0815649 -1.3120303
8 -0.0526673 -4.7456765 -0.4700128
9 -0.63208 -3.3539891 -2.0115812
10 0.2145577 -4.0010762 -2.9207664
11 -0.3729619 -4.5629487 -3.6922491
12 1.0240761 -4.5117416 -2.3388433
13 0.9711505 -2.8357534 -3.5251923
14 0.3408715 -1.9581318 -3.822669
15 1.6180273 -3.1186311 -4.3940263
16 1.8975644 -2.4613039 -2.5075514
17 3.0585685 -1.8075132 -3.006783
18 2.8443427 -0.8083913 -3.4607034
19 3.6249113 -2.4323449 -3.7466593
20 3.992363 -1.7272376 -1.8733916
21 4.9511518 -1.186389 -2.07637
22 4.254519 -2.795933 -1.6625937
23 3.423965 -1.0901105 -0.7496133
24 3.8947239 -1.659389 0.516987
25 3.9258208 -0.8841055 1.3251652
26 4.9554296 -2.0063238 0.4150401
27 3.0359709 -2.8971462 1.0103722
28 3.8185678 -3.6568248 1.2752906
29 2.4917984 -3.195833 0.0744643
30 2.0725911 -2.848428 2.0760021
31 1.638817 -1.4838974 2.5253139
32 2.5752075 -1.0062795 2.9080422
33 0.9012089 -1.6500344 3.3573053
34 0.8815328 -0.5306711 1.5538689
35 0.5519052 -1.1815579 0.7041188
36 1.6224746 0.2331944 1.1997508
37 -0.2989756 -0.0199954 2.1694908
38 -0.3033598 1.4095408 2.1280825
39 0.0521263 1.761717 1.1273303
40 0.4747811 1.7876458 2.8392599
41 -1.6030958 1.9523106 2.4553161
42 -1.5646386 2.9988577 2.8519616
43 -1.9732467 1.2583804 3.2576206
44 -2.5225735 1.8953969 1.3081864
45 -3.3669469 3.0741107 1.0973018
46 -3.0220368 3.8450892 1.8318384
47 -4.4858675 3.0095129 1.1439484
48 -3.0599689 3.6382723 -0.3005937
49 -3.982976 3.5193791 -0.9249329
50 -2.1988642 3.09917 -0.7700861
51 -2.7010767 5.025878 -0.199455
52 -1.3877664 5.5169363 -0.1698399
53 -0.8882234 5.1431508 -1.0995853
54 -0.935725 4.957068 0.6896982
55 -1.3304483 7.055419 0.0381237
56 -2.0611646 7.6166778 -0.601446
57 -0.3436857 7.3639388 -0.3955144
58 -1.5631742 7.5380082 1.3714558
59 -2.4256234 7.9039402 1.5299768

Types

1 H 
2 OAlc 
3 CPos 
4 HC 
5 HC 
6 C 
7 HC 
8 HC 
9 OE 
10 C 
11 HC 
12 HC 
13 C 
14 HC 
15 HC 
16 OE 
17 C 
18 HC 
19 HC 
20 C 
21 HC 
22 HC 
23 OE 
24 C 
25 HC 
26 HC 
27 C 
28 HC 
29 HC 
30 OE 
31 C 
32 HC 
33 HC 
34 C 
35 HC 
36 HC 
37 OE 
38 C 
39 HC 
40 HC 
41 C 
42 HC 
43 HC 
44 OE 
45 C 
46 HC 
47 HC 
48 C 
49 HC 
50 HC 
51 OE 
52 C 
53 HC 
54 HC 
55 CPos 
56 HC 
57 HC 
58 OAlc 
59 H 

Charges

1 0.211 
2 -0.328 
3 -0.019 
4 0.093 
5 0.093 
6 -0.063 
7 0.079 
8 0.079 
9 -0.295 
10 -0.021 
11 0.084 
12 0.084 
13 -0.023 
14 0.083 
15 0.083
16 -0.283 
17 -0.023 
18 0.083 
19 0.083 
20 -0.023 
21 0.083
22 0.083 
23 -0.283 
24 -0.023 
25 0.082 
26 0.082 
27 -0.023 
28 0.082 
29 0.082 
30 -0.283 
31 -0.023 
32 0.082 
33 0.082 
34 -0.023 
35 0.082 
36 0.082 
37 -0.283 
38 -0.023 
39 0.082 
40 0.083
41 -0.023 
42 0.083 
43 0.083 
44 -0.283 
45 -0.023 
46 0.083 
47 0.083
48 -0.021 
49 0.084 
50 0.084 
51 -0.295 
52 -0.063 
53 0.079 
54 0.079 
55 -0.019 
56 0.093 
57 0.093 
58 -0.328 
59 0.211 

Bonds

1 g18 13 16 
2 g18 16 17 
3 g18 20 23 
4 g18 23 24 
5 g18 27 30 
6 g18 30 31 
7 g18 34 37 
8 g18 37 38 
9 g18 41 44 
10 g18 44 45 
11 g18 48 51 
12 g18 51 52 
13 g18 6 9 
14 g18 9 10 
15 g26 17 20 
16 g26 24 27 
17 g26 31 34 
18 g26 38 41 
19 g27 10 13 
20 g27 3 6 
21 g27 45 48 
22 g27 52 55 
23 g4 10 11 
24 g4 10 12 
25 g4 13 14 
26 g4 13 15 
27 g4 17 18 
28 g4 17 19 
29 g4 20 21 
30 g4 20 22 
31 g4 24 25 
32 g4 24 26 
33 g4 27 28 
34 g4 27 29 
35 g4 3 4 
36 g4 3 5 
37 g4 31 32 
38 g4 31 33 
39 g4 34 35 
40 g4 34 36 
41 g4 38 39 
42 g4 38 40 
43 g4 41 42 
44 g4 41 43 
45 g4 45 46 
46 g4 45 47 
47 g4 48 49 
48 g4 48 50 
49 g4 52 53 
50 g4 52 54 
51 g4 55 56 
52 g4 55 57 
53 g4 6 7 
54 g4 6 8 
55 g56 2 3 
56 g56 55 58 
57 g71 1 2 
58 g71 58 59 

Angles

1 g102 14 13 16 
2 g102 15 13 16 
3 g102 2 3 4 
4 g102 2 3 5 
5 g102 21 20 23 
6 g102 22 20 23 
7 g102 23 24 25 
8 g102 23 24 26 
9 g102 30 31 32 
10 g102 30 31 33 
11 g102 35 34 37 
12 g102 36 34 37 
13 g102 37 38 39 
14 g102 37 38 40 
15 g102 4 3 5 
16 g102 4 3 6 
17 g102 44 45 46 
18 g102 44 45 47 
19 g102 5 3 6 
20 g102 52 55 56 
21 g102 52 55 57 
22 g102 56 55 57 
23 g102 56 55 58 
24 g102 57 55 58 
25 g12 1 2 3 
26 g12 13 16 17 
27 g12 20 23 24 
28 g12 27 30 31 
29 g12 34 37 38 
30 g12 41 44 45 
31 g12 48 51 52 
32 g12 55 58 59 
33 g12 6 9 10 
34 g13 10 13 16 
35 g13 16 17 20 
36 g13 17 20 23 
37 g13 23 24 27 
38 g13 3 6 9 
39 g13 30 31 34 
40 g13 31 34 37 
41 g13 37 38 41 
42 g13 38 41 44 
43 g13 44 45 48 
44 g13 45 48 51 
45 g13 51 52 55 
46 g13 9 10 13 
47 g14 11 10 12 
48 g14 14 13 15 
49 g14 18 17 19 
50 g14 21 20 22 
51 g14 25 24 26 
52 g14 28 27 29 
53 g14 32 31 33 
54 g14 35 34 36 
55 g14 39 38 40 
56 g14 42 41 43 
57 g14 46 45 47 
58 g14 49 48 50 
59 g14 51 52 53 
60 g14 51 52 54 
61 g14 53 52 54 
62 g14 7 6 8 
63 g14 7 6 9 
64 g14 8 6 9 
65 g15 2 3 6 
66 g15 3 6 7 
67 g15 3 6 8 
68 g15 52 55 58 
69 g15 53 52 55 
70 g15 54 52 55 
71 g51 10 13 14 
72 g51 10 13 15 
73 g51 11 10 13 
74 g51 12 10 13 
75 g51 16 17 18 
76 g51 16 17 19 
77 g51 17 20 21 
78 g51 17 20 22 
79 g51 18 17 20 
80 g51 19 17 20 
81 g51 24 27 28 
82 g51 24 27 29 
83 g51 25 24 27 
84 g51 26 24 27 
85 g51 28 27 30 
86 g51 29 27 30 
87 g51 31 34 35 
88 g51 31 34 36 
89 g51 32 31 34 
90 g51 33 31 34 
91 g51 38 41 42 
92 g51 38 41 43 
93 g51 39 38 41 
94 g51 40 38 41 
95 g51 42 41 44 
96 g51 43 41 44 
97 g51 45 48 49 
98 g51 45 48 50 
99 g51 46 45 48 
100 g51 47 45 48 
101 g56 49 48 51 
102 g56 50 48 51 
103 g56 9 10 11 
104 g56 9 10 12 

Dihedrals

1 g23 1 2 3 6 
2 g23 10 13 16 17 
3 g23 13 16 17 20 
4 g23 17 20 23 24 
5 g23 20 23 24 27 
6 g23 27 30 31 34 
7 g23 3 6 9 10 
8 g23 31 34 37 38 
9 g23 34 37 38 41 
10 g23 38 41 44 45 
11 g23 41 44 45 48 
12 g23 45 48 51 52 
13 g23 48 51 52 55 
14 g23 52 55 58 59 
15 g23 6 9 10 13 
16 g34 2 3 6 9 
17 g34 51 52 55 58 
18 g46 16 17 20 23 
19 g46 30 31 34 37 
20 g46 37 38 41 44 
21 g46 44 45 48 51 
22 g46 9 10 13 16 
23 glj14 1 2 3 4 
24 glj14 1 2 3 5 
25 glj14 11 10 13 14 
26 glj14 11 10 13 15 
27 glj14 11 10 13 16 
28 glj14 12 10 13 14 
29 glj14 12 10 13 15 
30 glj14 12 10 13 16 
31 glj14 13 16 17 18 
32 glj14 13 16 17 19 
33 glj14 14 13 16 17 
34 glj14 15 13 16 17 
35 glj14 16 17 20 21 
36 glj14 16 17 20 22 
37 glj14 18 17 20 21 
38 glj14 18 17 20 22 
39 glj14 18 17 20 23 
40 glj14 19 17 20 21 
41 glj14 19 17 20 22 
42 glj14 19 17 20 23 
43 glj14 2 3 6 7 
44 glj14 2 3 6 8 
45 glj14 20 23 24 25 
46 glj14 20 23 24 26 
47 glj14 21 20 23 24 
48 glj14 22 20 23 24 
49 glj14 23 24 27 28 
50 glj14 23 24 27 29 
51 glj14 25 24 27 28 
52 glj14 25 24 27 29 
53 glj14 26 24 27 28 
54 glj14 26 24 27 29 
55 glj14 27 30 31 32 
56 glj14 27 30 31 33 
57 glj14 28 27 30 31 
58 glj14 29 27 30 31 
59 glj14 30 31 34 35 
60 glj14 30 31 34 36 
61 glj14 32 31 34 35 
62 glj14 32 31 34 36 
63 glj14 32 31 34 37 
64 glj14 33 31 34 35 
65 glj14 33 31 34 36 
66 glj14 33 31 34 37 
67 glj14 34 37 38 39 
68 glj14 34 37 38 40 
69 glj14 35 34 37 38 
70 glj14 36 34 37 38 
71 glj14 37 38 41 42 
72 glj14 37 38 41 43 
73 glj14 39 38 41 42 
74 glj14 39 38 41 43 
75 glj14 39 38 41 44 
76 glj14 4 3 6 7 
77 glj14 4 3 6 8 
78 glj14 4 3 6 9 
79 glj14 40 38 41 42 
80 glj14 40 38 41 43 
81 glj14 40 38 41 44 
82 glj14 41 44 45 46 
83 glj14 41 44 45 47 
84 glj14 42 41 44 45 
85 glj14 43 41 44 45 
86 glj14 44 45 48 49 
87 glj14 44 45 48 50 
88 glj14 46 45 48 49 
89 glj14 46 45 48 50 
90 glj14 46 45 48 51 
91 glj14 47 45 48 49 
92 glj14 47 45 48 50 
93 glj14 47 45 48 51 
94 glj14 48 51 52 53 
95 glj14 48 51 52 54 
96 glj14 49 48 51 52 
97 glj14 5 3 6 7 
98 glj14 5 3 6 8 
99 glj14 5 3 6 9 
100 glj14 50 48 51 52 
101 glj14 51 52 55 56 
102 glj14 51 52 55 57 
103 glj14 53 52 55 56 
104 glj14 53 52 55 57 
105 glj14 53 52 55 58 
106 glj14 54 52 55 56 
107 glj14 54 52 55 57 
108 glj14 54 52 55 58 
109 glj14 56 55 58 59 
110 glj14 57 55 58 59 
111 glj14 6 9 10 11 
112 glj14 6 9 10 12 
113 glj14 7 6 9 10 
114 glj14 8 6 9 10 
115 glj14 9 10 13 14 
116 glj14 9 10 13 15 
```

全部原子和连接定义保留在当前页面。

在比较曲线之前，还要固定时间窗口的边界。本节无外力平均采用25≤t<40ps，恒力平均采用40

## 读真实构象：尺寸增加的同时，形状怎样改变

先看35ps、40ps和55ps的三幅实际构象。图中采用相同的长度比例，并以各帧质心为原点，所以画面大小可以直接比较；展示的是xy投影，z方向的信息仍然包含在完整三维尺寸计算里。两端氧用圈标出，避免把附近水或端氢误认为端点。35ps对应无外加拉力的一个时刻，40ps对应力切换位置，55ps是恒力阶段末端。每一幅都是具体时刻的构象，三幅图共同说明这次轨迹怎样从弯曲形态走向较沿x伸展的形态。

### 同一比例尺下的三个实际构象

35、40、55ps的xy投影；每帧平移到质心，保留实际构象。

LAMMPS 30 Sep 2026 Update 1；Gravelle等人的PEG/SPC-Fw开源例，300 K，real单位。保持原分阶段准备与恒力拉伸流程，增加可逐项核对的观测记录。

[下载参考数据与完整输入（ZIP） 4.47 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-peg-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s6)

35、40、55 ps的真实PEG构象，用同一比例尺绘制xy投影。每帧按全部59个原子的质量质心平移；橙色圆环标出受力氧，主链连接由实际键表确定。

二维投影有它自己的读图规则。两个原子在图上重叠，可能只是沿z方向分开而落在同一个xy位置；两条键在平面里交叉，也可能在三维空间中互不接触。因此，构象图负责帮助辨认整体排布，而距离与接触判断使用完整三维坐标。三幅图没有分别放大到填满画框，是为了让“看起来更长”保留相同尺子的含义。对于更复杂的链，还可以切换观察方向或使用三维轨迹播放器；无论选择哪种显示方式，数值分析都应保留同一组原子身份与三维几何。

再把所有601帧连成时间记录，就能看清快照之间发生了什么。无外力阶段的回转半径在约4.00–6.15Å之间变化，平均约4.91Å；两端距离变化更明显，范围约2.84–13.01Å。这说明端点可以在整体尺寸改变不那么剧烈时相互靠近或远离。恒力加入后，两端距离很快增加，随后在较大的数值附近波动；恒力窗口平均约28.29Å，回转半径平均约8.65Å。这里两个统计量分别从端点与全体质量分布的角度描述同一伸展响应。

### 端点、轮廓与质量尺寸的完整记录

解包轨迹每0.05ps一帧；40ps施力，阴影为恒力阶段。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s6)

25–55 ps的质量回转半径、两端氧原子距离、端点x投影与主链轮廓长。40 ps开始恒力拉伸；轮廓长按连续主链键长相加，保持与直线端距的区别。

分方向尺寸进一步解释形状变化。总回转半径增加时，如果x方向贡献明显增大而y、z方向保持较小，就说明链形成了沿拉力方向延伸的质量分布。它与各方向同时等比例变大的球状膨胀不同。分方向数值依赖坐标轴，所以整体转动也能交换这些贡献；总回转半径则在旋转下保持不变。本例外力给出了固定的x方向，使这些分量具有明确的物理参照。比较各向异性时先写出轴的定义，就能把分量变化与施力方向联系起来。

### 水中PEG的实际无外力与恒力轨迹

25–40ps无外加拉力，40–55ps两端恒力。PEG与水共同平移以保持链居中，内部构象由实际坐标给出。

播放实际轨迹时，可以结合端点和主链同时观察。链的伸展伴随许多局部转向，并没有要求所有原子沿一根直线排齐；主链键角与侧基仍然存在，水分子也在周围不断运动。55ps时两端氧距离约29.124Å，而主链轮廓长约35.359Å，这个差别正体现了真实共价路径的折线几何。当前模型保持固定连接，拉力引起的是这一连接关系内的形变。若要研究断链，需要能够描述键断裂的相互作用及相应条件，不能把固定谐振连接的持续伸长直接解释为化学断裂。

## 两端的力相互抵消，为什么仍然做功

两端外力大小相等、方向相反，整条链受到的外加合力为零。这有助于把作用集中到端点分离，而不是用合力把整条链向同一方向推走。但是合力为零并不意味着外力功为零。想象两个人向相反方向拉一条橡皮筋：左手向左移动、左向力做正功，右手向右移动、右向力也做正功。功取决于每个受力点的力与位移是否同向，不能先把作用在不同位置的力相加为零，再把所有位移信息丢掉。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s7)

图 3 · 两端相反恒力分别做功；投影变化已经包含两个端点的位移。

恒定相反端点力的总功式 5

![恒定相反端点力的总功](https://ml-biomat.com/static/agent-math/5f06fc4847d97773c1e34c43.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| W | 从施力起点到当前时刻的有符号累计外力功 | kcal mol⁻¹ |
| F | 每个端点外力的大小；右端+F、左端−F | kcal mol⁻¹ Å⁻¹ |
| ΔxR, ΔxL | 固定身份右、左端氧在时间区间内的x位移 | Å |
| X(t), X(t₀) | 当前与起始时刻的右端减左端x投影 | Å |
| t, t₀ | 当前时间和施力起点，本例起点40ps | ps |
| Δ, −, [], ×, = | Δ表示末值减初值；分别计算两端功后相加；括号先求投影差；相邻量相乘；等号连接等价形式 | 1 |

怎样理解功按每个受力点的力乘位移计算；两个端点位移已包含在投影差中。

算一个例子每端F=10kcal/(molÅ)，若两端各向外移动1Å，ΔX=2Å，W=20kcal/mol。实际40–55ps得到178.7617kcal/mol≈1241.98pN·nm。

使用条件固定方向与大小、固定端点身份；共同平移在端点差中相消。热浴交换与力场能量另行记录。

对本例的恒力，右端功是F乘右端x位移，左端功是−F乘左端x位移。两项相加，正好等于F乘端点x投影的增加量。这里的F是每端力的大小，所以公式中不需要再乘2；两个端点的运动已经包含在投影变化里。若两端各向外移动1Å，端点投影总共增加2Å，功就是F乘2Å。若两端仅整体同向平移相同距离，投影不变，两项功互相抵消。这个推导也说明共同居中平移不会改变本例按端点差计算的外力功。

### 实际施力协议与累计外力功

外力大小取输入参数，功按实际端点投影相对40ps的变化计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s7)

恒力在40 ps开启，每端大小为694.77 pN。累计功由单端力乘端点投影相对40 ps的变化得到；两端的相反力已包含在投影差中。曲线记录该非平衡拉伸过程的外力功。

以40ps的实际端点投影为起点，到55ps累计外力功约178.762kcal/mol，换算成单次分子作用常用的力乘长度单位约1241.98pN·nm。曲线在链快速伸展时上升较快，随后随着端点投影的涨落而小幅变化。功并不要求每一小段都增加：若端点短暂向内回缩，位移与施力相反，该小段功可以为负。只有把正负贡献保留下来相加，得到的才是此协议下的有符号累计功。固定力让这个积分简化为端点投影差，程序因此可以直接用记录坐标计算。

这项外力功与日志里的势能变化还不是同一个量。当前记录的势能来自所选分子力场，addforce默认没有把外加力势能并入热力学输出；同时NVT热浴能够与体系交换能量。施力后，一部分能量可以改变分子构象和溶剂排列，另一部分通过热浴交换，动能也会涨落。因此，解释能量平衡时需要同时记录力场能量、外力功和热浴交换的定义。把一次有耗散的拉伸功直接写成平衡自由能差，会跳过所需的采样与热力学条件；自由能问题将在专门的采样课程里展开。

## 把一段变化整理成可以继续研究的结果

完整Python程序从实际准备后的数据文件读取质量、类型和连接关系，再读取链的解包轨迹。它用端氧之间的共价路径计算轮廓长，用全部59个原子的质量与位置计算回转半径，并把每帧结果与LAMMPS输出对齐。程序还保留力切换帧、两阶段的精确筛选条件及外力功的起点。所有曲线来自同一套定义，避免一张图用端氧、另一张图用端氢，或者一处采用质量权重、另一处采用等权重。代码中的这些选择正是科学测量本身的一部分。

### 完整Python：尺寸、构象与外力功

```
"""Reproduce chain geometry and pulling plots from the actual PEG example.

python analyze_chain.py --run . --out analysis --language en

Dependencies: numpy, matplotlib. Inputs: merge.data, pull-peg.lammpstrj,
pull-thermo.dat. The dump supplies unwrapped xu,yu,zu coordinates.
"""
from pathlib import Path
from collections import deque
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_data(path):
    sections, current = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line in {"Masses", "Atoms", "Bonds", "Atom Type Labels"}:
            current = line
            sections[current] = []
        elif line[0].isalpha():
            current = None
        elif current:
            sections[current].append(line.split())
    masses = {int(r[0]): float(r[1]) for r in sections["Masses"]}
    labels = {int(r[0]): r[1] for r in sections["Atom Type Labels"]}
    atoms = {int(r[0]): {"mol": int(r[1]), "type": int(r[2])} for r in sections["Atoms"]}
    bonds = [(int(r[2]), int(r[3])) for r in sections["Bonds"]]
    return masses, labels, atoms, bonds


def read_frames(path):
    with path.open(encoding="utf-8") as handle:
        while line := handle.readline():
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(handle.readline())
            assert handle.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(handle.readline())
            assert handle.readline().startswith("ITEM: BOX BOUNDS")
            box = np.array([list(map(float, handle.readline().split())) for _ in range(3)])
            keys = handle.readline().split()[2:]
            a = np.array([list(map(float, handle.readline().split())) for _ in range(n)])
            a = a[np.argsort(a[:, keys.index("id")])]
            yield step, box, {key: a[:, i] for i, key in enumerate(keys)}


def shortest_path(edges, start, end):
    neighbours = {}
    for a, b in edges:
        neighbours.setdefault(a, []).append(b)
        neighbours.setdefault(b, []).append(a)
    queue, previous = deque([start]), {start: None}
    while queue:
        i = queue.popleft()
        if i == end:
            break
        for j in neighbours[i]:
            if j not in previous:
                previous[j] = i
                queue.append(j)
    if end not in previous:
        raise ValueError("Terminal oxygens are disconnected")
    result = [end]
    while result[-1] != start:
        result.append(previous[result[-1]])
    return result[::-1]


def stats(x):
    return {"frames": int(len(x)), "mean": float(np.mean(x)),
            "frame_sd": float(np.std(x, ddof=1)),
            "min": float(np.min(x)), "max": float(np.max(x))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    tr = lambda cn, en: cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16, "svg.fonttype": "path",
                         "figure.facecolor": "#f8f7f2", "axes.facecolor": "#f8f7f2",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.unicode_minus": False})
    masses_by_type, labels, all_atoms, all_bonds = read_data(args.run / "merge.data")
    records, coordinates = [], []
    reference_ids, atom_masses, end_indices, edges, backbone = None, None, None, None, None
    for step, box, data in read_frames(args.run / "pull-peg.lammpstrj"):
        ids = data["id"].astype(int)
        types = data["type"].astype(int)
        xyz = np.column_stack([data[k] for k in ("xu", "yu", "zu")])
        if reference_ids is None:
            reference_ids = ids.copy()
            row = {int(atom_id): i for i, atom_id in enumerate(ids)}
            atom_masses = np.array([masses_by_type[int(t)] for t in types])
            terminal = [i for i, t in enumerate(types) if labels[int(t)] == "OAlc"]
            assert len(terminal) == 2
            # Match the source's fixed membership established before the first run.
            left, right = sorted(terminal, key=lambda i: xyz[i, 0])
            end_indices = (left, right)
            chain_edges = [(a, b) for a, b in all_bonds if a in row and b in row]
            edges = [(row[a], row[b]) for a, b in chain_edges]
            backbone_ids = shortest_path(chain_edges, int(ids[left]), int(ids[right]))
            backbone = np.array([row[i] for i in backbone_ids])
            assert len(ids) == 59 and len(edges) == 58
        assert np.array_equal(ids, reference_ids)
        centre = np.sum(atom_masses[:, None] * xyz, axis=0) / atom_masses.sum()
        centred = xyz - centre
        rg_components_sq = np.sum(atom_masses[:, None] * centred**2, axis=0) / atom_masses.sum()
        rg = np.sqrt(rg_components_sq.sum())
        end = xyz[end_indices[1]] - xyz[end_indices[0]]
        re = np.linalg.norm(end)
        contour = np.linalg.norm(np.diff(xyz[backbone], axis=0), axis=1).sum()
        assert re <= contour + 1e-8
        records.append([step, step / 1000, rg, re, end[0], contour, *rg_components_sq])
        coordinates.append(centred)
    records = np.array(records)
    coordinates = np.array(coordinates)
    time = records[:, 1]
    unforced = time < 40
    pulled = time > 40
    switch = np.flatnonzero(time == 40)
    assert len(switch) == 1 and len(time) == 601
    switch = int(switch[0])
    thermo = np.loadtxt(args.run / "pull-thermo.dat", comments="#")
    assert np.array_equal(thermo[:, 0], records[:, 0])
    rg_error = np.max(abs(thermo[:, -1] - records[:, 2]))
    assert rg_error < 2e-5, rg_error
    # Equal/opposite constant endpoint forces: W = F * Delta(x_right-x_left).
    force_per_end = 10.0
    work = np.zeros(len(time))
    work[switch:] = force_per_end * (records[switch:, 4] - records[switch, 4])
    work_pN_nm = work * 6.947695457055374
    np.savetxt(args.out / "chain_shape.csv", np.column_stack([records, work]), delimiter=",",
               header="step,time_ps,Rg_A,terminal_O_distance_A,terminal_O_x_A,backbone_contour_A,Rgx_squared_A2,Rgy_squared_A2,Rgz_squared_A2,external_work_kcal_mol", comments="")
    summary = {"atoms": len(reference_ids), "mass_g_mol": float(atom_masses.sum()),
               "terminal_oxygen_ids_left_right": [int(reference_ids[i]) for i in end_indices],
               "backbone_atom_ids": backbone_ids,
               "native_Rg_max_error_A": float(rg_error), "switch_time_ps": 40,
               "force_per_end_pN": force_per_end * 69.47695457055374,
               "fixed_density_g_cm3": float(thermo[0, 8]),
               "unforced_window": "25 <= t < 40 ps", "pulled_window": "40 < t <= 55 ps",
               "transition_frame": "t=40 ps retained on time plots and as the work reference; excluded from phase means",
               "unforced": {}, "pulled": {},
               "final": {"Rg_A": float(records[-1, 2]), "terminal_O_distance_A": float(records[-1, 3]),
                         "terminal_O_x_A": float(records[-1, 4]), "contour_A": float(records[-1, 5]),
                         "external_work_kcal_mol": float(work[-1]), "external_work_pN_nm": float(work_pN_nm[-1])}}
    for phase, mask in [("unforced", unforced), ("pulled", pulled)]:
        for name, col in [("Rg_A", 2), ("terminal_O_distance_A", 3), ("terminal_O_x_A", 4), ("contour_A", 5)]:
            summary[phase][name] = stats(records[mask, col])
    (args.out / "chain_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def finish(fig, name):
        for ext in ("svg", "png"):
            fig.savefig(args.out / f"{name}.{ext}", dpi=180, bbox_inches="tight")
        plt.close(fig)

    colors = ["#167d84", "#c16b3d", "#466eaa"]
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, layout="constrained")
    axes[0].plot(time, records[:, 3], color=colors[0], label=tr("两端氧距离", "Terminal O distance"))
    axes[0].plot(time, records[:, 4], color=colors[1], linestyle="--", label=tr("沿x的端点投影", "Endpoint projection on x"))
    axes[0].plot(time, records[:, 5], color="#98a5a5", label=tr("主链轮廓长", "Backbone contour"))
    axes[0].set_ylabel(tr("长度 / Å", "Length / Å"))
    axes[1].plot(time, records[:, 2], color=colors[0], label=tr("质量加权回转半径", "Mass-weighted Rg"))
    axes[1].set_ylabel("Rg / Å")
    for k, col in enumerate([6, 7, 8]):
        axes[2].plot(time, np.sqrt(records[:, col]), color=colors[k], label=f"Rg,{['x','y','z'][k]}")
    axes[2].set_ylabel(tr("分方向均方根尺寸 / Å", "Directional RMS size / Å"))
    axes[2].set_xlabel(tr("从最初水准备开始的时间 / ps", "Time from the initial water preparation / ps"))
    for ax in axes:
        ax.axvline(40, color="#809393", linestyle=":")
        ax.axvspan(40, 55, alpha=.06, color=colors[1])
        ax.legend(frameon=False, loc="best", ncol=1)
        ax.grid(axis="y", alpha=.15)
        ax.set_xlim(25, 55)
    axes[0].set_title(tr("40 ps起，两端氧分别受±694.77 pN恒力", "Constant forces of ±694.77 pN act on terminal oxygens from 40 ps"))
    finish(fig, "chain-shape-records")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4), layout="constrained")
    type_colors = {1: "#c16b3d", 2: "#254952", 3: "#a0b2b4", 4: "#a0b2b4", 5: "#254952", 6: "#c16b3d"}
    for ax, target in zip(axes, [35, 40, 55]):
        idx = int(np.flatnonzero(time == target)[0])
        xy = coordinates[idx, :, :2]
        for a, b in edges:
            ax.plot(xy[[a, b], 0], xy[[a, b], 1], color="#90a3a2", linewidth=1, zorder=1)
        ax.scatter(xy[:, 0], xy[:, 1], s=[22 if masses_by_type[int(t)] < 2 else 60 for t in types],
                   c=[type_colors[int(t)] for t in types], zorder=2)
        ax.scatter(xy[list(end_indices), 0], xy[list(end_indices), 1], s=160,
                   facecolors="none", edgecolors="#c16b3d", linewidths=1.5, zorder=3)
        ax.axhline(0, color="#d3dcda", linewidth=.5)
        ax.axvline(0, color="#d3dcda", linewidth=.5)
        ax.set_xlim(-17, 17)
        ax.set_ylim(-10, 10)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel(tr("相对质心的x / Å", "x relative to COM / Å"))
        ax.set_ylabel(tr("相对质心的y / Å", "y relative to COM / Å"))
        ax.set_title(f"{target} ps\nRg = {records[idx,2]:.2f} Å, Re = {records[idx,3]:.2f} Å")
    fig.suptitle(tr("实际构象的xy投影；所有图采用相同长度比例", "Actual conformations projected onto xy; the length scale is shared"), fontsize=17)
    finish(fig, "chain-conformations")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), layout="constrained")
    for ax, col, label in [(axes[0], 3, tr("两端氧距离 / Å", "Terminal O distance / Å")),
                           (axes[1], 2, "Rg / Å")]:
        bins = np.linspace(records[:, col].min(), records[:, col].max(), 26)
        for mask, color, name in [(unforced, colors[0], tr("25≤t<40 ps，无外加拉力", "25≤t<40 ps, unforced")),
                                  (pulled, colors[1], tr("40<t≤55 ps，恒力阶段", "40<t≤55 ps, constant force"))]:
            ax.hist(records[mask, col], bins=bins, density=True, histtype="step", color=color, linewidth=2, label=name)
        ax.set_xlabel(label)
        ax.set_ylabel(tr("概率密度 / Å⁻¹", "Probability density / Å⁻¹"))
        ax.legend(frameon=False, fontsize=12)
        ax.grid(axis="y", alpha=.15)
    fig.suptitle(tr("两个实际时间窗口内的尺寸分布", "Size distributions in the two actual observation windows"), fontsize=17)
    finish(fig, "chain-shape-distributions")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, layout="constrained")
    force = np.where(time >= 40, 694.7695457055374, 0.0)
    axes[0].step(time, force, where="post", color=colors[1], label=tr("右端氧：+x", "Right oxygen: +x"))
    axes[0].step(time, -force, where="post", color=colors[2], label=tr("左端氧：−x", "Left oxygen: −x"))
    axes[0].set_ylabel(tr("施加力的x分量 / pN", "Applied x force / pN"))
    axes[0].legend(frameon=False)
    axes[1].plot(time, work_pN_nm, color=colors[0])
    axes[1].set_ylabel(tr("累计外力功 / pN nm", "Accumulated external work / pN nm"))
    axes[1].set_xlabel(tr("从最初水准备开始的时间 / ps", "Time from the initial water preparation / ps"))
    for ax in axes:
        ax.axvline(40, color="#809393", linestyle=":")
        ax.set_xlim(25, 55)
        ax.grid(axis="y", alpha=.15)
    axes[0].set_title(tr("两端力相反；功由端点投影变化计算", "Opposite endpoint forces; work follows the change in projected separation"))
    finish(fig, "pulling-work")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

按文件开头命令分析实际记录，--language zh或en控制图中文字。

尺寸分布把时间记录换成另一个视角：在某个观察窗口里，哪些尺寸出现得多，哪些出现得少。直方图按概率密度归一化，柱子的面积相加为1，纵轴单位因此是长度的倒数。两阶段分布的位置变化可以直观比较伸展前后的尺寸范围，分布宽度则反映该窗口中的波动。恒力窗口包含刚开始伸展的过渡过程，低尺寸一侧留下的少量记录正有这个时间来源。读分布时回到时间曲线，可以区分持续波动与启动过程带来的宽度。

### 两阶段有限时间窗口的尺寸分布

25≤t<40ps与40<t≤55ps各300帧；概率密度面积归一化为1。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/#zh-s8)

25≤t<40 ps与40<t≤55 ps各300帧的描述性尺寸分布，每条概率密度曲线的面积为1。两窗口包含实际的构象波动及拉伸响应，帧之间具有时间相关性。

平均值也依赖观察方式。本节报告的是每帧回转半径先算出、再平均的结果；若先把回转半径平方平均再开平方，得到的是另一个量，通常略大。对端点也是如此：平均向量可以因为方向相反而抵消，平均距离则始终保留大小。一个在各方向自由转动的链，即使平均端到端向量接近零，每一帧仍然可以有明显的端点距离。把“先做什么、再平均什么”写清楚，能够消除很多表面上的数值矛盾，特别是在比较实验、理论与模拟时。

比较两阶段平均值时，还应把热涨落的宽度与平均值的不确定性区分开。曲线中的标准差描述该窗口内尺寸变化有多大，而平均值的不确定性取决于有效独立信息有多少。每0.05ps保存一次并不等于链每0.05ps就忘记过去的形状，因此用记录总数直接缩小误差容易低估相关性的影响。可以把轨迹分成长度逐渐增加的时间块，比较块平均，并与独立重复相互核对。若块与块之间仍然存在系统漂移，就先延长准备和采样，让要比较的状态在观察尺度上形成稳定的统计描述。

如果要把这个例子推进成一组力—伸长关系，就为多个外力准备相同条件的独立重复，给每个条件足够时间调整，再比较稳定窗口里的端点投影及波动。不同力条件之间保持链长、水模型、温度和浓度定义一致，并检查拉伸方向的盒子大小是否允许链与周期像保持合适距离。若要讨论链长规律，则另外改变重复单元数，记录每条链的端基和总质量。这样，每一条曲线都对应明确的物理变量，观察到的差异才能与所改变的条件联系起来。

单链尺寸是走向多链材料的起点。把很多链放进同一个盒子后，它们既与自身相互作用，也受到其他链的拥挤与接触；同样的回转半径、轮廓长和端点定义仍然可以使用，但需要逐链统计并考虑链间关系。下一节将从这一步展开：用可追踪的珠链模型构建多链体系，解释密度、重叠处理和准备过程如何影响后续结构。当前已经建立的原则会继续保留——先确定对象与几何，再检查实际运动，最后用与问题相匹配的统计量作比较。

## 延伸阅读与开放资料

- [Polymer in water — A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial3/polymer-in-water.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0

  PEG/SPC/Fw体系的生成、准备和恒力端点拉伸流程。

  保留模型和运行参数，增加解包坐标、质量加权尺寸、主链路径和外力功的分析与双语教学。
- [compute gyration](https://docs.lammps.org/compute_gyration.html) · LAMMPS developers · Official technical documentation; referenced for mathematical definitions

  质量加权回转半径、分方向平方贡献与周期解包。

  补充逐原子独立复算、算例与几何交互。
- [fix addforce](https://docs.lammps.org/fix_addforce.html) · LAMMPS developers · Official technical documentation; referenced for force and output conventions

  逐原子恒力及默认能量输出约定。

  推导两个固定端点的功，并用实际位移计算。
- [Spatial Configuration of Macromolecular Chains — Nobel Lecture, 1974](https://www.nobelprize.org/uploads/2018/06/flory-lecture.pdf) · Paul J. Flory · Historical lecture cited; figures are newly drawn

  从化学连接走向空间构象的历史背景。

  使用构象集合的原创概念图。
- [Hydration Effects Turn a Highly Stretched Polymer from an Entropic into an Energetic Spring](https://doi.org/10.1021/acsnano.6b07071) · Susanne Liese and colleagues · Research article cited; no article figures reproduced

  PEG强拉伸与水化相互影响的研究背景。

  将研究问题与当前短时间教学模型的实际测量分开说明。
