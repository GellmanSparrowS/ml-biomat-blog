# 力、能量和时间怎样连接

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l03/
Language: zh-CN

从势能的坡度走到一次完整的时间步，用同一起点的真实对照分清积分误差、截断效应与采样。

## 动画很顺畅，运动就算对了吗

用手机拍摄一根快速振动的琴弦，有时会看到弦缓慢摆动，甚至出现与真实运动不同的形状。问题出在观察间隔与运动速度之间的关系。分子模拟除了保存画面的间隔，还多了一层：计算机本身也按小时间段推进运动。如果一个时间步跨过了强烈碰撞的大部分过程，下一次计算作用力时，粒子可能已经走到了完全不同的位置。这一讲讨论怎样把势能、作用力和时间推进连接起来，并通过真实对照判断时间步是否适合当前模型。

这里需要回答两个看似相近、实际不同的问题。第一个是我们选择的相互作用是否适合研究对象，例如中性 LJ 粒子能保留哪类吸引和排斥；第二个是计算机是否足够准确地推进了这套已选定的方程。改变力场解决的是前一个问题，减小时间步主要针对后一个问题。对于水、长链和交联材料，两个层次都要逐步检查。先在简单体系中理解它们的区别，可以避免把数值不稳定误当成材料真的发生了突变。

本讲从上一讲保存的同一状态出发，去掉随机热浴，在固定盒中进行三次 NVE 运行。三次分别采用零点零零二五、零点零零五和零点零一的时间步，都推进二十个约化时间单位。比较时保留粒子、初始坐标和速度、势函数以及截断规则，集中观察时间步改变之后，能量曲线与温度怎样变化。相同物理时长是这项比较的关键；若只运行相同步数，大时间步的系统就会经历更长的运动，结果混入另一个变化。

为了读懂这些曲线，我们先把“力是能量的坡度”这句话展开，再跟着一个粒子走完一次速度 Verlet 更新。数学只在需要时引入：斜率描述位置变化一点时能量变化多少，平方根帮助连接振动时间与质量、弹性，求最大值则从一整条误差曲线中找到最明显的偏离。每个符号都与一个可以想象的量相连。最后，完整输入和分析程序会把这些关系落实到同一批实际模拟数据。

所谓数值准确，也要与目标量联系起来。研究一段很短的碰撞，可以比较力和轨迹细节；研究平衡结构，可能更关心距离分布与能量统计；研究流变，则需要关注应力和长时间相关。时间步太大往往同时影响多个量，而某一条总能量曲线比较平稳，也不自动回答全部性质是否已经收敛。这里选择能量作为最先检查的量，因为在这段没有热浴和外加功的模型中，它与动力学方程有直接联系。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s1)

图 1 · 从模型定义到数据解释，每一步都需要保持对应。

我们会保留原例的未平移截断 LJ 势，这让比较更有教育意义：实际能量变化可能既包含积分误差，也包含粒子对跨越截断时的势能跳变。读者不必预先猜哪一项更大，而要学会从定义和对照中辨认。把真实输入的细节带进解释，能够使“减小时间步看看”从一句经验建议，变成有明确对象、参照和判断依据的数值实验。

## 从能量地形的坡度读出作用力

想象把一个小球放在光滑山坡上，球受到的沿坡推动与当地倾斜程度有关。处在同一海拔的两个位置，倾斜程度可能不同；一个点海拔为零，也完全可能位于陡坡上。势能曲线中的零点与作用力之间也是这种关系。将两个粒子的距离作为横坐标，势能作为纵坐标，若距离稍微增加会使势能升高，系统就有倾向于减小距离的吸引作用；若距离增加反而降低势能，作用趋势便是分开。

斜率可以先从两个相近的点理解。把能量差除以距离差，得到这段曲线平均有多陡；让两个点越来越近，就得到该位置的局部斜率，数学上记作导数。作用力取这个斜率的负号，表示沿着降低势能的方向推动。这里约定正的径向力增加粒子间距，负的径向力减小间距。先说明正方向非常重要，否则相同的负号可能被误读成“能量为负，所以力向负方向”。

作用力与局部能量坡度式 1

![作用力与局部能量坡度](https://ml-biomat.com/static/agent-math/f09df8fc30a513a541af562c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Fᵣ | 使粒子间距增大的方向取正的径向力 | ε₁₁/σ₁₁ |
| U | 一对粒子的势能 | ε₁₁ |
| r | 两粒子间距 | σ₁₁ |
| h | 用于理解或估计坡度的小距离增量 | σ₁₁ |
| dU/dr | 能量对距离的局部变化率，即导数 | ε₁₁/σ₁₁ |
| ≈, − | 近似相等；负号表示沿能量降低方向作用 | 1 |
| =, +, −, /, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解两侧点的能量差除以它们相隔的 2h，给出中心附近坡度的估计。取负号把能量升高的方向转成降低能量的作用方向。

算一个例子若 r − h 与 r + h 相距 0.02，势能从 −0.50 增加到 −0.48，坡度约为 0.02/0.02 = 1，径向力约为 −1，即趋向缩短间距。

使用条件用来说明在平滑区间中的保守力。跨越未平移势能的截断跳变时，这个普通差分不能当作 LAMMPS 截断力的定义。

对 LJ 势求这个坡度，会得到一条与能量曲线相关但形状不同的力曲线。很近时，排斥力迅速增加；在势阱最低点，吸引与排斥项相抵，径向力为零；再远一些，力变成吸引，并逐渐减弱。距离等于 σ 时势能为零，而力仍为正。用第一类粒子的约化参数计算，这一点的径向力数值为二十四，远远谈不上“没有相互作用”。把能量值和能量变化率分开，许多关于平衡距离的疑惑就会消失。

对坡度作数值估计时，小距离 h 的选择也包含一种平衡。距离太大，得到的是横跨一段弯曲地形的平均坡度，不能很好代表某一点；距离极小，两个非常接近的能量相减又可能损失有效数字。实际 LJ 力使用解析表达式计算，这里的两点差分帮助理解导数，也可以在检查自定义势时作为独立核对。核对时让 h 在一段合理范围内变化，观察结果是否稳定，比只计算某一个极小增量更有信息。

Lennard–Jones 径向力式 2

![Lennard–Jones 径向力](https://ml-biomat.com/static/agent-math/4cf7a53bed184bd96196cbe0.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Fᵣ | 正值排斥、负值吸引的径向力 | ε₁₁/σ₁₁ |
| ε | 势阱深度 | ε₁₁ |
| σ | 势能零点的距离尺度 | σ₁₁ |
| r, r_{c} | 粒子间距与该对截断距离 | σ₁₁ |
| 12, 6 | 无量纲比值的幂次 | 1 |
| =, −, /, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解对 12/6 势分别求距离导数，再取负号，得到排斥和吸引的两项。括号内没有单位，ε/r 提供力的单位。

算一个例子ε = σ = 1、r = 1 时，Fᵣ = 24(2 − 1) = 24；r = 2^(1/6) 时括号为 2 × 1/4 − 1/2 = 0；r = 1.5 时 Fᵣ ≈ −1.15803。

使用条件适用于截断内的普通 LJ 力；截断外设为零。这里的标量还需乘沿粒子连线的单位方向，形成三维受力。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s2)

图 2 · 势能为零与力为零对应不同间距；这三组数由解析 LJ 公式计算。

在三维中，径向力还要沿粒子连线分配到三个方向。若把从粒子一指向粒子二的方向作为单位方向，正的径向力把粒子二沿这个方向推远，粒子一受到相反方向的力。单位方向只表示方向，其长度为一；乘以径向力后，才得到有大小的矢量。每个粒子周围同时有多个邻居，程序把各个力的三个分量分别相加。两个大小相等、方向相反的作用可以抵消，因此一个粒子的合力为零，也可能意味着它正受到多个相互平衡的作用。

这个关系也解释了为什么改变势能参考零点通常不改变局部受力。把一条光滑曲线整体上移同样高度，坡度保持不变；同一区域的导数也不变。但在截断势中，还要考虑哪些粒子对被计入，以及跨越边界时函数是否连续。我们稍后专门讨论这种情况。现在先抓住基本关系：势能描述位置安排的能量代价，导数描述这种代价对位移的敏感程度，力再通过质量转化为速度变化。

当模型扩展到键、键角和二面角时，仍然会使用同样的思想，只是能量不再只依赖两个粒子的距离。拉长一根键、改变三个粒子构成的夹角，或转动四个粒子定义的扭转角，都可能改变势能。软件按照各项对坐标的变化求出相应作用力。第五讲会介绍这些连接关系；本讲从双粒子势开始，是为了让“先定义能量，再由其变化求力”的逻辑能够在一张图中看清。

## 一次时间步怎样把位置和速度接起来

已有位置和速度之后，最直观的做法是先假设速度暂时不变，用“速度乘时间”估计位移，再用力估计速度的变化。这个想法说明了积分的基本任务，但过于简单的更新会在反复使用时积累明显偏差。速度 Verlet 采用更对称的安排：先用旧作用力更新半步速度，再用这个半步速度更新完整一步的位置；到了新位置，重新计算作用力，最后用新作用力补上另一半速度更新。新旧位置的信息因此都进入了一步运动。

“半步速度”首先是算法内部的中间量，不需要把它想成又生成了一段单独的真实轨迹。它的作用是让位置更新利用这一小段运动中较合适的速度估计。整步结束后，位置和最终速度对应同一个新的时刻。LAMMPS 的 fix nve 使用速度形式的 Verlet 积分来完成这项任务。恒温方法如果另外修改力或速度，也会参与整个更新过程，因此读懂具体设置之后，才能判断实际推进的是哪套动力学。

速度 Verlet 的一次完整更新式 3

![速度 Verlet 的一次完整更新](https://ml-biomat.com/static/agent-math/e48170fbae5cd8d47b96eb9e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| rₙ, rₙ₊₁ | 当前与下一整步的粒子位置矢量 | σ₁₁ |
| vₙ, vₙ₊₁ | 两个整步时刻的速度矢量 | σ₁₁/τ |
| vₙ₊₁/₂ | 更新位置所用的中间半步速度 | σ₁₁/τ |
| Fₙ, Fₙ₊₁ | 旧位置与新位置分别计算的合力 | ε₁₁/σ₁₁ |
| m | 粒子质量 | m₁ |
| Δt | 固定积分时间步 | τ |
| n, n+1, n+1/2 | 当前步、下一整步与中间更新标签 | 1 |
| =, +, /, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解先用旧力推进半步速度，再推进整步位置，在新位置重算力后补上另一半速度。新旧受力都参与更新，形成对称安排。

算一个例子对 m = 1、F = −x 的一维弹簧，从 x = 1、v = 0、Δt = 0.1 开始：半步 v = −0.05；新 x = 0.995；新 F = −0.995；最后 v = −0.09975。

使用条件这里展示固定质量、位置依赖力的基本更新。刚体约束、随机热浴、压力控制等需要其完整算法安排。

不妨跟着一维弹簧模型算一次。取质量一、弹簧刚度一，起点位置一、速度零，时间步零点一；弹簧总是把物体拉向原点。旧加速度为负一，先得到半步速度负零点零五；位置随后变成零点九九五；新加速度为负零点九九五，补上后半步后，速度为负零点零九九七五。每个数字都来自前一步已经知道的量。这个短算例帮助我们理解为什么必须在新位置重新计算力，而不是让第一步的力一直沿用下去。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s3)

图 3 · 科学史与算法结构相连：早期经典流体研究需要反复推进动力学，本图用现代速度形式展开一次更新。

在这一更新中，单位也能够帮助检查运算。加速度乘时间是速度，所以可以加到旧速度上；速度乘时间是长度，所以可以加到旧位置上；直接把力加到位置上，则把不同量纲混在了一起。计算机执行的是数字运算，不会自动替读者解释模型单位是否选对。写出或修改自定义作用力时，这种量纲检查尤其有用。它不能发现所有模型错误，却能很快指出某些根本不相容的相加和相乘。

Verlet 在1967年发表的经典流体计算，用包含864个粒子的 LJ 模型研究不同温度和密度下的平衡性质。它所代表的一个重要转变，是把反复求力与时间推进组织成能长期使用的计算实验方法。今天常用的速度形式与经典位置形式属于同一类时间对称积分思想，书写和保存速度的方式有所不同。沿着旧力、半步速度、新位置和新力这一顺序，可以把抽象的时间推进还原为逐项可算的动作。

时间对称的安排使这类方法在保守系统中具有有用的长期数值性质，但固定有限时间步得到的运动仍是近似的。对于足够平滑的势和稳定的时间步，能量误差经常表现为围绕某个水平的有界波动，而不只是单方向越来越偏。是否出现持续漂移、波动有多大，仍要看模型、截断与实际记录。这正是我们同时画完整能量曲线和几个误差指标的原因：一个终点差值可能恰好很小，却掩盖中途较大的起伏。

## 最快的运动怎样限制时间步

一个材料内部往往同时有快慢不同的过程。整条高分子链重新舒展可能很慢，相邻原子的键振动却很快；水分子的转动与溶质扩散也发生在不同尺度。显式积分必须处理当前模型实际保留的最快运动，不能只按最终想观察的慢过程来选时间步。为了看一条链慢慢扩散就把时间步加大，并不会自动让键振动变慢。若希望跨过这些快速自由度，需要通过约束或粗粒化改变模型，再重新考虑对应时间尺度。

弹簧振动提供了一个容易理解的起点。同样的弹簧拉着更重的物体，运动反应较慢；同样的物体接上更硬的弹簧，回复力更强，振动更快。这两个影响通过质量与刚度的比值共同决定振动周期。周期表示完成一次完整往复所需的时间。若一个时间步已经占据周期很大一部分，算法在两次求力之间就可能跳过运动方向的改变；把一个周期分成足够多的小步，才能较好跟踪这种变化。

弹簧的时间尺度与线性稳定区间式 4

![弹簧的时间尺度与线性稳定区间](https://ml-biomat.com/static/agent-math/72270c1b9cec6da61bd257f6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| F, x | 弹簧回复力与相对于平衡点的位移 | ε₁₁/σ₁₁; σ₁₁ |
| k | 弹簧刚度，力对位移的比例系数 | ε₁₁/σ₁₁² |
| m | 运动物体的质量 | m₁ |
| ω | 振动角频率，每单位时间积累的相位 | τ⁻¹ |
| P | 一次完整往复的周期 | τ |
| Δt | 积分时间步 | τ |
| π, √, < | 圆周率、平方根、小于号 | 1 |
| =, −, /, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解质量越大，运动响应越慢；弹簧越硬，回复越快。谐振子的解析方程给出角频率与周期，离散更新的线性稳定要求 ωΔt 小于 2。

算一个例子取 m = k = 1，则 ω = 1、P ≈ 6.283。Δt = 0.1 对应每周期约 62.8 步，ωΔt = 0.1；Δt = 2.1 则超出这个稳定区间。稳定边界内仍需检查相位和能量准确性。

使用条件稳定条件专指无阻尼线性谐振子和速度 Verlet。多体 LJ 碰撞、约束及热浴具有各自的时间尺度，不能直接照搬这个数值界限。

在小振幅谐振子这个特定模型里，还能够推导速度 Verlet 的线性稳定条件。条件说明时间步超过某个界限后，离散运动会出现不断增长的振幅，即使真实无阻尼振子的振幅原本固定。稳定只表示这种无限增长没有发生，准确跟踪相位和能量通常要求更小的步长。下面的交互把这些层次分开呈现：它是一个解析弹簧练习，用来观察算法；本讲的 LJ 结果仍来自后面的真实 LAMMPS 运行。

数值弹簧演示：m = k = 1，初始 x = 1、v = 0。它与下方 LAMMPS 实跑数据分开展示。

[Figure: 弹簧位移随时间变化](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s4)

固定模型，只改时间步；解析解与数值解都从同一位置和速度出发。该图是算法演示，实际 LJ 对照见下方结果。

LJ 碰撞没有一个适用于全部距离的固定弹簧刚度。在势阱最低点附近，可以把曲线局部近似成弹簧；当粒子靠得更近时，排斥曲线急剧变陡，有效回复变化会快得多。随机初态中的过近接触，因而可能比平衡附近的小振动更严苛。先进行适当最小化，既改善起始几何，也减少把极端排斥直接交给常规时间步处理的情况。随后仍要检查实际运动是否在所选参数下保持合适的数值行为。

质量也参与决定快速运动。两种粒子的势参数不同，质量又相差五倍，单凭“第二类比较重”无法确定整个体系该用多大时间步。第一类粒子的快速碰撞、异类接近和大粒子之间的相互作用都可能贡献约束。时间步是在整个模型中使用的共同安排，选取时应考虑其中最难分辨的相关运动。后面加入轻的氢原子、刚性水或 FENE 链时，我们会再次从质量、势能变化与约束这三个方面判断。

数值对照应当一次缩小一个主要不确定因素。本讲先保持力场与初态不变，只改变时间步，并选择相同的观察时长。若曲线随步长缩小明显收敛，就获得时间离散方面的证据；若误差变化不大，则继续检查截断不连续、输出精度或其他算法设置。这个思路没有预设一定得到某种漂亮的比例关系，而是让已定义的计算问题决定接下来最有用的对照。

## 势能截断为什么会留在能量曲线上

LJ 表达式在很远处仍有一个逐渐减弱的吸引尾部。如果对所有粒子对都一直算到无限远，计算组织和边界处理都会变得不同。当前例题选择在距离四处截断，超过这个范围的该项相互作用不再计算。截断首先是模型的一部分，同时也影响数值曲线应怎样读。知道截断位置的数值还不够，还要将它与每对粒子的 σ 比较，看看它在那条能量曲线上究竟处于哪里。

对第一类粒子，σ 等于一，所以截断位于四倍 σ；对第二类，σ 等于三，同一个距离四只相当于约一点三三三倍 σ。第二类粒子的势阱最低点在约三点三六七，因此截断仍然处在相对明显的吸引区域。不同类型共享一个绝对截断值，不等于它们保留了相同长度比例的吸引尾部。这一细节来自实际输入，也说明为什么不能不看参数，就把“截断四”理解成对每一种相互作用都很长。

原例使用的未平移形式，在截断内保留原来的 LJ 势能，在截断外写成零。由于截断内侧的能量通常还没有到零，粒子对跨过这里时，记录的势能会发生一个跳变。普通的截断力计算并不加入与这一能量台阶对应的瞬时冲量。因此，即使把积分步长缩小，原样报告的未平移能量也可能继续显示跨截断造成的变化。这个效应与某次碰撞没有被时间积分充分分辨，是两个不同来源。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s5)

图 4 · 势能平移去除截断处的能量台阶；力的截断不连续仍然保留。

一种常见处理是把截断内的势能整体减去截断处的值，使能量在边界接到零。这称为势能平移。对于截断内同一对粒子，减去常数不改变力；跨越截断时，能量函数的连续性得到改善。但力在截断处仍可能突然从非零变为零，因此势能平移和力平滑是不同操作。若采用力平移或切换函数，使力也更平滑，通常会改变一定距离范围内的实际相互作用，应当把这些选择写进模型定义。

把截断内势能接到边界的零点式 5

![把截断内势能接到边界的零点](https://ml-biomat.com/static/agent-math/de3322fb083f1775bc032237.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Uₛ | 势能平移后的成对能量 | ε₁₁ |
| U_{LJ} | 原始 12/6 Lennard–Jones 表达式 | ε₁₁ |
| r, r_{c} | 当前间距与截断距离 | σ₁₁ |
| U_{LJ}(r_{c}) | 原始势在截断处的值，对这一类粒子对是常数 | ε₁₁ |
| <, ≥ | 按所在距离区间选取分支 | 1 |
| =, −, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；相邻因子相乘。 | 运算符无量纲 |

怎样理解减去截断处的值，使内侧能量在接近截断时趋向零。截断内减去常数不改变导数，因此保留原来的局部力。

算一个例子第二类粒子 ε = 0.5、σ = 3、r_c = 4，U_LJ(r_c) ≈ −0.292604。最低点原能量为 −0.5，平移后为约 −0.207396；最低点位置和截断内作用力保持原样。

使用条件势能连续但力仍可能在截断处跳变。此操作适用于本例 lj/cut 的 shift yes，不等同于力平移、切换函数或延长截断。

这一讲的三次主要对照保留同一种截断设置，保证比较的对象一致。分析时把总能量变化与时间步一起看，并说明未平移截断仍然存在。如果想进一步分离截断贡献，可以在下一组明确标注的对照中使用平移势能，再检查同样的时间步序列；如果改变截断长度，也应同步考虑密度、压力与平衡结构可能如何变化。数值分析不只是把曲线磨得更平，而是弄清每个修改究竟改变了报告方式还是运动本身。

对生物材料的复杂力场，这种细节同样重要。短程范德华作用、长程静电、键约束和外加壁面各有自己的处理方式。一个能量检查应当包括当前模型真正具有的能量项，也需要知道外界是否做功、约束求解是否存在有限容差。此时从简单 LJ 模型学到的习惯仍然适用：先写清能量由什么组成，再看哪些算法近似会影响它，最后设计针对这些因素的对照。

## 邻居表让计算更快，也需要及时更新

一个粒子只与截断范围内的邻居计算短程力，但程序仍要知道谁可能成为邻居。若每一步都把所有粒子两两检查，数量增加后会花费很多工作。邻居表提前收集一个稍大范围内的候选对象，之后的若干步只检查这张表。这个想法像先把附近商店列在地图上，出门时再判断哪家实际在步行范围内。候选范围比实际作用范围多出来的一圈，给粒子在两次建表之间移动留出余量。

这个额外距离称为 skin。候选列表的距离范围是截断距离加 skin，而实际计算某一对力时仍然检查真正的截断。把 skin 调大，通常会增加每步需要检查的候选数，同时可以减少某些情况下的建表频率；把它调小则有相反的权衡。它主要影响计算组织，不应被误认为延长了势函数的物理作用范围。读日志中的邻居数量和建表次数，能够帮助理解成本来自哪里。

候选邻居范围比作用范围多一圈式 6

![候选邻居范围比作用范围多一圈](https://ml-biomat.com/static/agent-math/14ce6948f10439ee18739497.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| r_{list} | 建立候选邻居表使用的距离上限 | σ₁₁ |
| r_{c} | 实际成对力的截断距离 | σ₁₁ |
| s | skin，即额外的候选距离 | σ₁₁ |
| =, +, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；相邻因子相乘。 | 运算符无量纲 |

怎样理解多保留一圈候选粒子，让它们在两次重建之间可以移动。真正求力时仍按 r_c 判断。

算一个例子r_c = 4、s = 0.3 时，候选距离为 4.3。距离 4.2 的粒子对可以在表中，但此时的 LJ 截断力仍为零。

使用条件用于解释短程邻居列表；及时重建与相应通信仍是正确更新近邻关系的组成部分。

邻居表如果长期不更新，原本在表外的粒子可能已经移动到作用范围内，却没有被正确纳入受力计算。开启位移检查后，程序根据粒子自上次建表以来移动的距离判断是否需要重建，相关检查仍受到 every 和 delay 等设置的安排。这里保持正常的动态更新，让算法追踪变化的近邻关系。为了省时间而直接把更新关闭，改变的可能是受力是否完整，而不只是运行速度。

时间步增大时，每一步的位移通常也会增加，因此积分与邻居更新的问题可能同时显现。若出现粒子丢失、异常巨大能量或近邻相关的警告，应同时检查初始几何、速度尺度、时间步以及列表更新安排。一个很大的 skin 也不能修复粒子在一步里跨过强排斥区的积分错误；反过来，时间步很小也不适合长期沿用已经过时的邻居表。这两层设置各自承担不同任务，需要分别理解。

在简单例题中理解这些机制，能够为后面的长链和网络计算节省许多排查时间。链上的键连接会使相隔多个处理器区域的原子仍然具有拓扑关系，交联又会改变哪些近邻需要作为特殊连接处理。那时不仅要寻找几何邻居，还要维护正确的连接与通信范围。本讲暂时只处理无键粒子，先把“候选列表”和“真实相互作用”分开；这种区分是复杂模型中检查受力完整性的基础。

## 用同一起点完成三次真实对照

实际比较从热浴阶段结束时保存的 equilibrated.restart 读取同一组位置和速度。输入随后将步号设为零，以便把三条曲线都画成从共同起点经过的时间，再选择各自的时间步。run 0 只在当前状态计算需要的量，不推进动力学，因此可以保存三次比较共同的初始能量。这个起点尤其重要，因为后面的数值表每十步写一次，不同时间步对应不同的第一条记录时间，不能把它们都无区别地当成同一个零时刻。

### 从共同状态比较时间步

```
# Same tutorial-derived state and interaction model at several time steps.
# Run with: lmp -var dt 0.005 -in timestep.lmp
variable dt index 0.005
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep ${dt}
variable count equal round(20.0/v_dt)
variable t equal time
variable T equal temp
variable E equal etotal/atoms
thermo 100
thermo_style custom step time temp pe ke etotal press
thermo_modify norm no flush yes
fix integrator all nve
run 0
print "$(step) $(time) $(temp) $(etotal/atoms)" file timestep-${dt}-initial.dat screen no
fix records all ave/time 10 1 10 v_t v_T v_E file timestep-${dt}.dat
run ${count}
write_dump all custom timestep-${dt}-final.lammpstrj id type x y z vx vy vz modify sort id
```

读取同一重启状态，先记录 t = 0 的温度和每粒子总能量，再推进 20 个约化时间单位。

输入根据二十除以时间步计算步数，因此三个分支分别需要八千、四千和两千步。命令行的 -var 选项把时间步传给同一份输入，避免维护三份只差一个数字却可能逐渐产生其他差别的脚本。文件名中保留时间步，输出便能与条件直接对应。每次运行仍然从同一个重启文件读取，而不是让后一种时间步接着前一种的末态继续。这样才是对同一起点的并列比较。

### 三种步长，相同经过时间

```
lmp -var dt 0.0025 -in timestep.lmp
lmp -var dt 0.005 -in timestep.lmp
lmp -var dt 0.01 -in timestep.lmp
```

运行目录需有第一讲产生的 equilibrated.restart。每个分支重新读取它，输出名包含各自时间步。

分析程序同时读取初始状态文件和时间序列表，把每粒子总能量减去该分支的初始每粒子总能量。减去参照后，纵轴直接显示能量改变，而不需要在一个较大的绝对基线上辨认小差别。这里使用绝对的约化能量差，没有除以可能接近零的初始总能量。若初始总能量恰好因势能与动能抵消而很小，相对百分误差会变得非常敏感，反而不便于比较实际误差尺度。

从共同初态定义能量偏离式 7

![从共同初态定义能量偏离](https://ml-biomat.com/static/agent-math/30b63b613d40933f954aa913.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| e(t), e(0) | 时刻 t 与共同起点的每粒子总能量 | ε₁₁ |
| Δe(t) | 相对初态的能量改变 | ε₁₁ |
| t_{end}, tⱼ | 终止时间与第 j 个保存记录的时间 | τ |
| Δe_{end} | 首尾能量差 | ε₁₁ |
| A_{e} | 已保存记录中最大的绝对能量偏离 | ε₁₁ |
| max, \| · \| | 取最大值；取绝对值 | 1 |
| =, −, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；相邻因子相乘。 | 运算符无量纲 |

怎样理解所有能量先与同一个定义明确的起点相减，便于显示小变化；再分别读首尾变化和保存记录中的最大偏离。

算一个例子若 e(0) = 1.10，后续记录依次为 1.10003、1.09998、1.10001，则 Δe_end = 0.00001，而 A_e = 0.00003。首尾较接近并不意味着中途没有更大波动。

使用条件三次运行使用相同初态和相同终止时间。A_e 针对实际保存值；不同输出间隔对快速极值的分辨率不同。

程序报告末态相对初态的能量差，以及已保存记录中最大的绝对偏离。两者共同说明曲线的一部分性质：前者关注首尾改变，后者关注观察到的最大起伏。由于三个分支都每十步输出一次，保存间隔分别是零点零二五、零点零五和零点一；图中保留这些真实采样点，不伪装成相同密度。最大偏离因此严格对应保存下来的记录，若要比较未保存的快速极值，应重新统一更密的物理时间采样。

### 完整的初态对齐与能量对照分析

```
"""Compare actual LAMMPS NVE energy traces at equal elapsed time.

python analyze_timestep.py --data-dir . --shifted-dir shifted --language en
Requires NumPy and Matplotlib.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_series(directory, prefix, label):
    initial = np.loadtxt(directory / f'{prefix}-{label}-initial.dat', ndmin=1)
    table = np.loadtxt(directory / f'{prefix}-{label}.dat', comments='#', ndmin=2)
    if initial.shape != (4,) or table.shape[1] != 4:
        raise ValueError('Expected step,time,temperature,energy_per_particle.')
    if not np.all(np.isfinite(initial)) or not np.all(np.isfinite(table)):
        raise ValueError('All recorded values must be finite.')
    # Use the explicitly recorded common initial state, never a later first sample.
    table = table[table[:, 1] > initial[1]]
    table = np.vstack((initial, table))
    time = table[:, 1] - initial[1]
    if not np.all(np.diff(time) > 0) or not np.isclose(time[-1], 20.0):
        raise ValueError('Each comparison must advance monotonically to time 20.')
    delta = table[:, 3] - initial[3]
    return time, delta, {
        'step_size': float(label),
        'initial_energy_per_particle': float(initial[3]),
        'elapsed_reduced_time': float(time[-1]),
        'saved_values_including_initial_state': len(time),
        'final_energy_change_per_particle': float(delta[-1]),
        'max_absolute_recorded_energy_change_per_particle': float(np.abs(delta).max()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('.'))
    parser.add_argument('--shifted-dir', type=Path)
    parser.add_argument('--out-dir', type=Path, default=Path('comparison'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else ['DejaVu Sans'],
                         'font.size': 14, 'svg.fonttype': 'path',
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': '#173c42', 'text.color': '#173c42'})
    sources = [('unshifted', args.data_dir, 'timestep')]
    if args.shifted_dir is not None:
        sources.append(('shifted', args.shifted_dir, 'shifted'))
    fig, axes = plt.subplots(len(sources), 1, figsize=(11.5, 4.8 * len(sources)),
                             squeeze=False, layout='constrained')
    fig.set_facecolor('#faf9f5')
    summary = {}
    for ax, (name, directory, prefix) in zip(axes[:, 0], sources):
        ax.set_facecolor('#faf9f5')
        rows = []
        initial_values = []
        for label, color in [('0.0025', '#167d84'), ('0.005', '#bb7448'), ('0.01', '#486fa9')]:
            time, delta, row = load_series(directory, prefix, label)
            rows.append(row)
            initial_values.append(row['initial_energy_per_particle'])
            ax.plot(time, delta, color=color, linewidth=1.5, label=f'Δt = {label}')
        if not np.allclose(initial_values, initial_values[0], rtol=0, atol=1e-10):
            raise ValueError('Initial energies must agree across step sizes for each model.')
        summary[name] = rows
        if name == 'unshifted':
            title = '原截断模型：保留未平移势能' if zh else 'Original cutoff: unshifted energy'
        else:
            title = '势能平移对照：相同的截断力' if zh else 'Energy-shift comparison: unchanged truncated forces'
        ax.set_title(title, loc='left', fontsize=16, pad=15)
        ax.axhline(0, color='#879995', linewidth=0.7)
        ax.set_xlim(0, 20)
        ax.set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
        ax.set_ylabel(('每粒子能量变化 ' if zh else 'Energy change per particle ') + r'$\Delta e/\epsilon_{11}$')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useMathText=True)
        ax.grid(axis='y', alpha=0.16)
        ax.legend(frameon=False, ncol=3)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out_dir / f'timestep-comparison-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'timestep-comparison-{args.language}.svg')
    plt.close(fig)
    (args.out_dir / 'timestep-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

读取每个分支单独保存的 t = 0 能量，并检查相同模型各步长的初始能量一致、终点均为 20。

### 原截断模型的时间步比较

三种时间步从同一初态走到 20τ。每条曲线减去各自明确保存的初始每粒子能量，保留未平移截断的影响。

LAMMPS 30 Sep 2026 update 1；三维周期盒，1500 个类型 1 粒子与 100 个类型 2 粒子；约化单位，时间步 0.005，总时长 150。物理输入沿用 Gravelle 等人的双组分 Lennard–Jones 教程，增加 NVE 对照及数值记录。

[下载参考数据与完整输入（ZIP） 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s7)

从相同的平衡重启文件出发，各运行到 t* = 20。每条曲线减去单独记录的共同初始时刻 t* = 0 的自身总能量，并除以粒子数。

这个额外对照沿用相同重启状态、三种时间步和二十个时间单位，只增加 pair_modify shift yes。它调整每类相互作用在截断处的能量连接，截断内受力与原来相同。运行后按粒子编号比较相同时间步的末态，保存的坐标和速度与原分支一致；两种能量记录却表现出明显不同的变化尺度。因此，我们可以把两组图并排，用来观察能量定义如何影响数值诊断，而没有同时把材料运动换成另一个体系。

在这一段二十个时间单位的实际记录中，平移对照的最大每粒子能量偏离，在时间步零点零一时约为一点三四乘十的负四次方，零点零零五时约为四点零零乘十的负五次方，零点零零二五时约为一点四五乘十的负五次方。这些数值对应本次初态和保存间隔，显示减小步长后观测到的偏离收缩。原未平移记录中的最大偏离则都在约零点零零五附近，截断能量台阶遮住了较小的积分差异。

### 只增加势能平移的完整对照输入

```
# Same checkpoint as the unshifted branches; potential shifted to zero at rc.
# Forces retain the original cutoff discontinuity.
# Same tutorial-derived state and interaction model at several time steps.
# Run with: lmp -var dt 0.005 -in timestep.lmp
variable dt index 0.005
units lj
read_restart equilibrated.restart
pair_modify shift yes
reset_timestep 0
timestep ${dt}
variable count equal round(20.0/v_dt)
variable t equal time
variable T equal temp
variable E equal etotal/atoms
thermo 100
thermo_style custom step time temp pe ke etotal press
thermo_modify norm no flush yes
fix integrator all nve
run 0
print "$(step) $(time) $(temp) $(etotal/atoms)" file shifted-${dt}-initial.dat screen no
fix records all ave/time 10 1 10 v_t v_T v_E file shifted-${dt}.dat format " %.15g"
run ${count}
write_dump all custom shifted-${dt}-final.lammpstrj id type x y z vx vy vz modify sort id
```

pair_modify shift yes 保持截断内力和原截断规则，只改变能量连续连接方式；另提高数值输出精度。

### 运行势能平移对照并生成双语比较图

```
lmp -var dt 0.0025 -in shifted.lmp
lmp -var dt 0.005 -in shifted.lmp
lmp -var dt 0.01 -in shifted.lmp
python analyze_timestep.py --data-dir . --shifted-dir . --out-dir comparison --language zh
python analyze_timestep.py --data-dir . --shifted-dir . --out-dir comparison --language en
```

两套输出用 timestep 与 shifted 前缀区分，可以保存在同一个例题目录。

### 平移能量之后，时间步差异更清楚

上图为原未平移能量，下图为平移能量；每个相同时间步的末态坐标和速度在保存精度内一致，力保持原样。

LAMMPS 30 Sep 2026 update 1；1600 个双组分 Lennard–Jones 粒子；NVE，Δt* 分别为 0.0025、0.005、0.01；对照增加 pair_modify shift yes。截断内的力与原流程一致，截断处的力仍未平滑。

[下载参考数据与完整输入（ZIP） 0.29 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-shifted-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/#zh-s7)

同一重启状态、相同的三种步长与 20τ 观察时间。上排读取原截断势的能量，下排读取平移后的能量，两排各自保留可辨认的纵轴尺度。每种步长的末态坐标与速度在保存精度内一致；纵轴差异来自能量定义。

两幅图的纵轴尺度因此相差很大。阅读时先看轴上的数量级，再比较线条起伏，避免把同样高的屏幕波动看成同样大的能量误差。平移后的力依然在截断处不连续，三条有限时长曲线也没有被强制拟合成某个固定幂律。这组对照直接回答一个更具体的问题：当原轨迹的力保持不变时，把能量函数在截断处接连续，能否让不同时间步的数值表现更容易区分？实际结果给出了清楚的区分。

这种诊断也提醒我们同时保留原模型和修改条件。若今后为了改善数值行为采用不同的切换函数，需要检查它对结构、压力和目标动力学有什么影响；若只是修改输出精度或单位表达，则应检查数据是否保持同一含义。每项改动都有自己的比较对象。把改动前后的输入、共同初态和分析定义配在一起，读者便能重复这一步推理，而不必把一张更平滑的曲线当成独立的证据。

读图时，先确认三条曲线起点来自同一状态、终点都在二十，再比较整体变化与短时间波动。如果减小时间步后某一部分起伏收缩，可以联系积分分辨率讨论；如果仍存在接近的跳变或基线变化，就回到未平移截断的定义。还可以把温度曲线与能量并排查看，判断动能是否发生持续偏移。解释应当使用实际曲线表现出的关系，而不是因为采用了某种算法，就预先规定误差一定按时间步平方下降。

运行代价也值得记录，但要与相同计算条件联系起来。更小的时间步需要更多步才能覆盖同样时长，实际耗时还受邻居重建、硬件、并行配置和输出量影响。选择时间步时，关心的是在目标量达到合适准确程度后，怎样获得足够长的有效采样。把步长一直缩小到时间预算主要花在重复解析已经足够精细的快速运动上，可能挤掉慢结构真正需要的观察时长。数值准确和采样充分应一起设计。

## 把数值证据带到更复杂的材料中

完成这一组对照之后，可以用三种不同语言描述同一段计算。物理语言说，粒子按给定相互作用在固定盒中交换势能和动能；算法语言说，速度 Verlet 用新旧作用力推进坐标和速度，邻居表及时提供候选相互作用；数据语言说，记录的能量相对于共同初态发生了怎样的变化。三种描述彼此连接，却各有自己的概念。把它们分清以后，软件参数不再只是需要背下来的数值，而是可以解释选择依据的条件。

如果后来加入化学键，最快振动可能来自键伸缩；把某些键约束成固定长度后，允许的时间尺度安排也随之改变。若把若干原子合并成一个粗粒化珠子，一部分内部自由度被移除，势参数和动力学映射需要重新理解。它们都不是单纯把当前脚本的 timestep 改大，而是在模型、算法与目标性质之间重新建立对应。每次增加复杂性，可以沿用本讲的对照结构：保持明确起点，改变一个选择，检查相关量。

对于有热浴的计算，总能量随时间改变可以来自合理的能量交换，因此不能直接套用这一讲孤立段的判断。在受拉伸的网络中，外界做功会改变能量；在压力控制的盒子里，体积变化也参与能量交换。数值检查应当先弄清系统与环境之间有什么通道，再选择相应的守恒量或统计量。下一讲将从这里出发，讨论温度、压力和边界怎样表示实验环境，以及这些控制会怎样影响我们看到的运动。

可以用一个具体例子检验理解：若在不改变力的前提下把截断内势能平移，为什么轨迹可以保持相同，而报告的能量曲线却发生变化？答案需要同时提到常数的导数为零，以及相互作用范围内粒子对的数量会随运动改变。再问，如果把时间步减半、步数不变，为何不能直接与原结果比较同一个终点？因为它只走过一半物理时间。这样的问答把数学运算与实际实验设计连起来，比孤立记住一个“推荐步长”更容易迁移到新体系。

在后面的每个材料模型中，数值选择都应能回到这种完整解释：哪些运动被保留，哪些力变化最快，哪些量用来检查结果，比较覆盖了多少真实模拟时间，以及输出是否足以看见相关变化。复杂体系不会让这些基础问题消失，只会让回答更加具体。先把一盒粒子的力、能量和时间连接清楚，就能够在研究分子、长链和网络时，知道某条曲线的可信程度究竟来自哪些证据。

## 延伸阅读与开放资料

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  原双粒子类型体系、LJ 力场与 NVE 流程。

  增加力的推导、积分分解、等时长步长比较及势能平移诊断。
- [LAMMPS stable manual: fix nve](https://docs.lammps.org/stable/fix_nve.html) · LAMMPS developers · Official technical documentation; software source GPL-2.0; no copied figures

  速度 Verlet 算法及 NVE 条件。

  原创算例与算法图。
- [LAMMPS stable manual: pair_style lj/cut](https://docs.lammps.org/stable/pair_lj.html) · LAMMPS developers · Official technical documentation; no copied figures

  势函数、截断、混合与 shift 选项。

  对实际两类型参数作解析图与实跑对照。
- [Computer Experiments on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules](https://doi.org/10.1103/PhysRev.159.98) · Loup Verlet (1967) · Cited paper; no article text or figures reproduced

  经典液体计算的科学史。

  自绘计算流程图，将历史研究问题与当前积分练习相连接。
