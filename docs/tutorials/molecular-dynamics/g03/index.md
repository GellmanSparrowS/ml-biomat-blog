# 一盒水的第一场模拟

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g03/
Language: zh-CN

让水经过几何整理、温度调整与体积调整，再从真实的力、能量和密度记录理解每一步的作用。

## 让水动起来之前，先给它一个合适的起点

把一袋玻璃珠倒进盒子，珠子刚落下时的排列通常还没有安定下来。轻轻晃动盒子后，一些过于拥挤的接触会松开，珠子也会重新填入空隙。构建分子模型时也会遇到类似的准备问题：坐标已经生成，并不表示这些位置已经适应所选相互作用和环境。上一讲把水分子放进了周期盒子，本讲要让这个模型经过几何整理、温度调整和体积调整，最后得到可以认真阅读的运动记录。

这次实际运行使用边长初始为 3 nm 的 SPC/E 水盒，温度目标为 300 K，压力目标为 1 bar。研究问题是：按这组明确条件准备水以后，温度、体积和密度怎样变化，我们怎样判断每个阶段完成了它的任务？这些问题看似基础，却决定了后续蛋白质、水凝胶或膜体系的起点是否合理。若起始溶剂仍在明显收缩，直接把大分子的变化解释为材料性质，就容易把准备过程与研究现象混在一起。

流程分成四类动作。能量最小化调整坐标，减轻较大的局部作用力；NVT 动力学保持盒子体积，让运动与目标温度相适应；NPT 动力学允许盒子大小响应压力控制；最后的 NVE 分支撤去温控和压控，用来观察数值积分中的能量行为。每一类动作留下不同证据，不能靠同一条曲线替它们全部作判断。最小化看势能与最大力，温度调整看动能和温度，压力调整看体积与相关涨落，孤立动力学则关注总能量随时间的变化。

本例的 NVT 时长为 20 ps，NPT 时长为 100 ps，后面的 NVE 分支各为 100 ps。这些时间是这个小水盒的教学观察安排，便于在本地计算并检查全过程。体系的慢变化并不会因为输入文件写了一个阶段名称就自动完成；如果关注的量仍然漂移，就需要继续采样或重新检查准备。我们将把实际记录展示出来，让“进入下一步”的决定与看到的物理量相联系。

同一个水盒里，质量、分子数和空间尺度也要始终对应。分子数量由建盒决定，后面的控温压控不会创造或删除水分子；体积在 NPT 阶段能够变化，浓度或密度便随之变化。对于本例纯水，可以通过拓扑计数和盒子体积交叉核对密度。未来把盐或聚合物加入体系时，也要保留这种守恒的直觉：先知道盒子里有什么，再讨论它们如何重新排列。

运行软件需要的全部文本输入都放在本页，命令与分析程序也直接展示。按第二讲的方法把它们保存到同一个例题目录，检查引擎版本，再执行运行脚本。脚本负责重复性的文件衔接，正文解释每个阶段为什么存在以及怎样读结果。第一次学习时，可以先看懂一个阶段，再对照对应输入和输出；已经熟悉流程以后，同一套脚本就能支持完整复现。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s1)

图 1 · 阶段目标与相应证据。最小化是优化过程，后面三类才沿物理时间推进；NVE分支的两个时间步在第四讲比较。

### 水盒拓扑模板

```
; Water-box workflow adapted from Wes Barnett and Vedran Miletic's GASERI tutorial.
; https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/
; Tutorial adaptations: CC BY-SA 4.0. The supplied force field retains its license.
; This example uses SPC/E rather than TIP4P/Ew and a 3 nm periodic cube.
#include "oplsaa.ff/forcefield.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
SPC/E water in a periodic cube
[ molecules ]
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

## 最小化在整理几何，不是在等待水冷却

势能取决于分子如何排列。如果两个位点被放得过近，模型的短程排斥通常会产生很大的力，直接开始动力学可能使一个更新跨过过大的位移。最小化让坐标沿着减小势能的方向调整，从初始构建中移除这类不合适的接触。它像在正式走路之前把脚下硌人的石子挪开：目的是准备可用的几何，而不是通过这段整理过程测量真实行走速度。

本例使用最速下降算法。可以想象在一张起伏地形上寻找较低的位置，每次根据当前位置的坡向尝试向下移动，再检查新位置的高度是否下降。实际计算在所有原子坐标构成的高维空间中进行，势能相当于“高度”，力给出与能量变化有关的方向。输入中的 emstep 控制尝试位移的尺度，程序还会根据尝试结果调整步长；它不是动力学中的时间步，也不能据此给最小化横轴标上真实的皮秒。

水的初始坐标还有一个细节。文本精度和建盒过程可能使内部几何与严格的刚性约束存在微小差别，因此这次最小化先启用配套水拓扑中的柔性键角分支，允许几何松弛。进入真正的 NVT、NPT 和 NVE 动力学后，水重新使用刚性 SPC/E 的 SETTLE 约束。两者服务于不同阶段：前者整理初始形状，后者规定我们要观察的刚性分子模型。后续分析水的运动时，使用的是动力学轨迹。

### 完整柔性几何最小化输入

```
integrator = steep
define = -DFLEXIBLE
emtol = 100.0
emstep = 0.001
nsteps = 10000
nstenergy = 10
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = none
constraint-algorithm = lincs
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

判断最小化是否达到设定目标，需要看最大力与停止原因。总势能明显降低可以说明排列发生了有意义的调整，但一个很大的体系可能在总势能变化不明显时仍有一个局部接触受到很大作用力。最大力把注意力放到当前最强的原子受力上，帮助找出这种局部问题。本例的阈值为 100 kJ·mol⁻¹·nm⁻¹，最大允许更新次数为 10000；程序可能先达到阈值，也可能先用完允许的次数，二者要按日志区分。

从三方向受力得到最大原子力式 1

![从三方向受力得到最大原子力](https://ml-biomat.com/static/agent-math/f4ef89e41fe66c3553fefa61.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Fmax | 所有原子受力大小中的最大值 | kJ·mol⁻¹·nm⁻¹ |
| i | 原子的编号 | 无量纲 |
| Fix, Fiy, Fiz | 第i个原子在x、y、z三个垂直方向上的受力分量 | kJ·mol⁻¹·nm⁻¹ |
| max, √, ², +, = | max取最大值；平方后相加并开平方得到向量大小；等号给出定义 | 运算符无单位 |

怎样理解先计算每个原子的受力大小，再找出最大的一个，避免局部强受力被整体平均掩盖。

算一个例子若一个原子的两个分量为60和80，第三分量为0，单位均为kJ·mol⁻¹·nm⁻¹，则大小为100。若另一个原子大小为120，整体最大力就是120，仍高于本例阈值100。

使用条件用于解释最小化日志中的最大力；它不等于总势能，不表示分子已经在目标温度下完成热平衡。

阈值的单位可以从“能量随距离变化”来理解。每摩尔的能量除以纳米，描述改变位置所对应的受力尺度。把 100 kJ·mol⁻¹·nm⁻¹ 换成单个粒子的 SI 力单位，约为 1.66×10⁻¹⁰ N，即 166 pN；这里用阿伏伽德罗常数把摩尔表达换成单粒子表达。数值的用途是说明停止条件的量级，不是把它当成所有模型都应使用的统一标准。更精细的振动分析与普通动力学准备，可能需要不同的最小化要求。

最小化以后仍然可以存在许多局部较低能排列。算法从当前起点沿附近的能量变化前进，不会自动把所有可能的分子排列都搜索一遍。对于液体，我们接下来需要热运动在不同排列之间交换，因此也不追求把所有水分子永远锁在一个极低能结构。准备阶段的目的，是获得适合动力学起步的几何，并明确知道它怎样得到。

势能的绝对正负也要结合模型的参考零点解释。若把同一势能函数整体加上一个常数，位置变化引起的能量差与力都不变，运动规律也不会因此改变。因此，看到总势能是负数，不能只凭这个符号判断结构已经合适；同一模型中的下降趋势、最大力和局部几何更有直接意义。更换力场后，总能量的零点和分解方式可能改变，跨模型比较需要先明确共同的物理定义。

### 最小化势能与终止条件

来自em.log的实际优化步号与势能；横轴不是物理时间。最大力和停止情况同时来自该次日志。

GROMACS 2026.4；884 个 SPC/E 水分子，初始立方盒边长 3 nm；目标温度 300 K、压力 1 bar。NPT 记录 100 ps，描述统计窗口为 50–100 ps；轨迹播放器显示另一个 100 ps NVE 阶段。

[下载参考数据与完整输入（ZIP） 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s2)

最速下降过程中的势能记录。横轴是优化更新编号，记录跳过被拒绝的试探步骤；它不表示分子经过的物理时间。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 终止时最大力 | 96.9421 | kJ mol⁻¹ nm⁻¹ |
| 最后保存的优化步号 | 2049 | 1 |
| 最大力低于 100 | ✓ | kJ mol⁻¹ nm⁻¹ |

这次最小化在编号 2049 的最后保存步骤达到 96.94 kJ·mol⁻¹·nm⁻¹ 的最大力，低于设定的 100 阈值；从编号 0 开始计数，共经历 2050 个优化步，包含尝试过程。势能曲线先快速下降，再逐渐放缓，反映初始较强接触先被调整，后面的几何变化较小。这里完成的是给定柔性准备模型的力阈值任务，接下来仍要恢复刚性水并建立目标温度下的运动。

## 控温要保留热涨落，不能只追求一条平直曲线

几何整理之后，水分子还需要运动。第一次进入动力学时，我们根据 300 K 生成初始速度，使不同粒子具有与目标温度相配合的速度分布。温度描述的是许多运动自由度的统计能量尺度，并不要求每个水分子具有相同速率。就像一群人在操场上活动，有人走得快，有人走得慢，整体的运动强度可以有一个平均水平，个体之间仍然存在差别。

动能把质量和速度联系起来。对于经典模型中的二次型动能自由度，平衡统计给出了平均动能与温度的关系。自由度可以先理解为能够独立改变的运动方向或方式：一个在三维空间自由移动的点有三个平移方向，刚性水分子还能整体转动，而受约束的内部伸缩不再单独贡献相同的自由变化。软件根据粒子、约束和去除整体运动等设置确定有效自由度，再据此报告温度。

平均动能与温度的联系式 2

![平均动能与温度的联系](https://ml-biomat.com/static/agent-math/89aa7bd20b939a88f3fec6e0.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ⟨K⟩ | 相应运动自由度的平均总动能 | 焦耳J，整个模型的能量 |
| f | 独立二次型动能自由度数，按约束和整体运动处理调整 | 无量纲 |
| kB | 玻尔兹曼常数，1.380649×10⁻²³ | J·K⁻¹ |
| T | 热力学温度 | 开尔文K |
| ⟨ ⟩, /, ×, = | 尖括号表示统计平均；分数线表示除法；相邻因子相乘；等号表示平衡关系 | 运算符无单位 |

怎样理解经典平衡条件下，每个独立二次型动能自由度平均贡献kBT/2，累加f个便得到总平均动能。

算一个例子指定f=60、T=300K的算例，平均动能为30×1.380649×10⁻²³×300=1.2425841×10⁻¹⁹J。GROMACS能量表采用kJ/mol数值约定；代入本式前应统一为J，或在一致的摩尔单位表达中使用气体常数R。

使用条件适用于经典平衡中的相应二次型自由度。瞬时温度可由动能估计但会涨落；约束、质心运动处理和离散积分中的动能定义需要一致。

NVT 阶段通过温控算法与一个理想化热环境交换能量。环境并不是在水盒外又模拟了一个巨大的浴缸，而是用算法表示它对系统能量统计的影响。温控过强或使用方式不合适，会改变某些动力学相关性质；因此温控参数除了让平均温度接近目标，还要与研究用途配合。本例对整个纯水系统使用一组温控，耦合时间设为 1 ps，先观察整体热运动适应情况。

2007 年，Bussi、Donadio 和 Parrinello 提出的随机速度重标度方法，针对的是一个清楚的统计问题：怎样调整速度，同时保留正则系综所要求的动能分布。正则系综可以理解为许多处于相同温度环境、粒子数和体积条件相同的系统所形成的统计集合。它允许能量涨落。因此，好的温控并不是把每一帧温度都强行拉到同一个数，而是让相应的分布符合所选条件。GROMACS 中的 v-rescale 与这项工作对应。[Bussi 等，2007](https://doi.org/10.1063/1.2408420)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s3)

图 2 · 2007年随机速度重标度关注动能统计，2020年随机晶胞重标度关注体积统计。两条曲线示意分布的宽度，说明平衡条件下仍然存在涨落。

### 完整NVT输入：20ps

```
integrator = md
dt = 0.002
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
nsteps = 10000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261110
ld-seed = 20261111
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

初始速度的随机种子与温控中随机过程的种子都在输入中固定，方便追踪这一次设置。不同种子能够产生不同微观路径，即使曲线上的平均温度接近，分子也不会在每一个时刻走到同一个位置。我们观察的是统计规律，所以日后需要独立重复时，会有意识地改变相关种子，同时保留力场、温度和其他控制条件。固定种子用于记录具体一次运行，独立重复用于了解不同运行之间的变动。

读 NVT 的温度曲线时，应同时看均值附近的涨落和是否存在持续趋势。曲线在开始阶段变化较快，可能反映初始状态在适应；后段若仍有明显单向漂移，就需要进一步观察。动能与温度之间的联系也提供交叉检查：当自由度固定时，它们应按同一关系变化。图中的小幅上下起伏是热运动的一部分，不能通过随意加大控制强度或过度平滑，把“看起来安静”当成物理上更合适。

温度对应的是体系中合适的内部运动统计。如果整盒水一起向某个方向漂移，整体平移会贡献动能，却不是我们要描述的相对热运动。程序对质心运动的处理因此会影响自由度和温度解释。这里的质心可以理解为把所有质量平均起来得到的代表位置，它的运动描述整个系统的平移。阅读温度时，把整体运动、内部自由度和约束一起考虑，比只看速度是否“很快”更准确。

### NVT中的温度、动能和势能

由G03分析程序读取nvt-energy.xvg真实列标签，显示实际时间轴与300K目标。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s3)

20 ps NVT 阶段的实际温度、动能与势能。虚线表示 300 K 控温目标；水从柔性最小化结构进入刚性动力学，最初的能量重新分配也保留在图中。

这次温度记录在最初的 300 K 附近起步，紧接着明显下降到约 160 K，再随温控与结构调整逐渐回到目标附近。对应时段中，动能下降而势能上升，说明最小化后的初态正在重新分配运动和相互作用能量。生成 300 K 的速度只是指定了初始运动分布，空间排列并不会因此立即成为该温度下的平衡液体。图中这段变化正好说明了为什么需要保留准备阶段，而不是从第一帧就开始统计目标条件下的性质。

## 让体积响应压力，水才有机会选择自己的密度

建盒时指定 3 nm 边长，是给水一个初始空间。这个体积未必就是当前模型在目标温度、压力下最合适的平均体积。NVT 保持它不变，所以可以调整热运动，却不会让盒子自行膨胀或收缩。进入 NPT 后，压控算法允许盒子尺寸变化，在既定分子数下探索相应的体积分布。密度随体积反向变化，正好把上一讲的几何关系连接到这次真实的运动记录。

压力可以借助一个带活塞的容器理解：容器内部的运动与相互作用对边界产生作用，外界也施加压力，活塞能够移动，于是体积可以调整。周期盒子没有真实墙壁和活塞，算法通过盒矢量与坐标的变化实现相应统计条件。这个类比帮助理解体积为什么能变，同时也提醒我们，模拟中的压控参数是计算方法的一部分，不能把算法的每次缩放都想成实验仪器的一次真实机械动作。

纯水在这里采用各向同性压控，三个空间方向按同样的尺度调整，立方盒子的形状保持一致。对于膜，面内与法向可能需要不同处理；对于某些晶体，盒子形状也可能成为研究变量。当前选择来自体系的均匀体相液体性质。了解这一点以后，就能理解为什么不能把水盒的压控设置不加解释地搬到任何材料上。

2020 年，Bernetti 和 Bussi 研究了随机晶胞重标度压控。其目标同样包括涨落：既让体积向目标压力条件调整，又保留合适的体积分布。这使“平均值看起来正常”与“分布是否采样正确”的区别变得具体。两个算法可能给出相近的平均体积，却产生不同大小的体积涨落；当研究压缩性等与涨落有关的性质时，这种差别就会进入结果。GROMACS 的 C-rescale 用于本例的压控阶段。[Bernetti 与 Bussi，2020](https://doi.org/10.1063/5.0020514)

### 完整NPT输入：100ps

```
integrator = md
dt = 0.002
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
nsteps = 50000
continuation = yes
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
gen-vel = no
ld-seed = 20261112
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

输入中的 ref-p 为 1 bar，tau-p 为 5 ps，compressibility 为 4.5×10⁻⁵ bar⁻¹。最后一个量描述用于压控响应的可压缩性尺度，反映体积对压力变化的相对响应；在本例中，它是压控算法的输入参数，不是我们从这段短轨迹测得的新结果。温控继续保持 300 K，速度从上一阶段延续而来，gen-vel 设为 no。这样，NPT 接续的是已经开始运动的水盒，而不是每进入一个阶段都重新随机启动。

瞬时压力的波动通常比初学者想象得大。纳米盒子中的压力来自有限粒子的运动与相互作用统计，它不像日常气压计显示的长时间、较大尺度平均那样平稳。本讲用体积与密度的记录观察压控后的状态调整，并保留压力用于诊断；解释是否达到目标时，需要考虑统计窗口和涨落，而不是要求每一个时刻都等于 1 bar。若体积持续收缩或膨胀，说明这一记录仍包含显著的准备变化。

体积涨落还有实际的材料意义。容易压缩的材料，在相同热力学条件下可以表现出不同的体积响应，统计力学把一些响应性质与涨落联系起来。我们暂时不从这段短水轨迹估计精确压缩性，但可以先认识为什么需要保留涨落：把体积每一步都强行固定在一个“正确”数值，会失去 NPT 分布本来要提供的信息。正是这种问题，推动了能够同时处理平均状态和涨落的压控方法发展。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s4)

图 3 · 相同分子数在更大体积中形成更低质量密度。圆点表示计数，不描绘真实水结构；实际NPT曲线在结果面板中给出。

切换系综条件，观察哪些量受到控制、哪些可以与环境交换。

[Figure: 系统与热、压环境的关系](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s4)

系综条件示意；虚线盒框表示允许体积响应压力变化。

## 完整运行脚本怎样把阶段连接起来

现在，拓扑模板和各阶段 MDP 已经分别说明。脚本从模板生成本次拓扑，建立水盒，预处理并最小化，然后把每一阶段的末态传给下一阶段。GROMACS 的检查点包含坐标、速度及相应算法状态，阶段衔接时与坐标文件一起提供。这样，文本中“继续上一阶段”具有具体实现，读者也可以从每个命令看出使用了哪份状态。

本例在 NPT 之后还生成两条 NVE 分支，为第四讲的时间步比较作准备。它们都从同一份 npt.gro 与 npt.cpt 出发，不重新生成速度，物理时长同为 100 ps，分别采用 2 fs 和 1 fs 时间步。下面把两个输入都完整列出。你会发现步数随时间步改变，而固定的物理观察时间保持不变；邻居表的相关设置也按比较目的固定，以减少额外变化。

### 完整NVE输入：2fs时间步

```
integrator = md
dt = 0.002
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 50000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

### 完整NVE输入：1fs时间步

```
integrator = md
dt = 0.001
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 100000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

NVE 关闭温控与压控，使总能量的数值行为更容易解释。固定体积意味着这一分支的盒子密度不会通过压控再调整。它适合检查能量误差与观察某些动力学量，NPT 的体积统计则仍应从 NPT 记录读取。把不同阶段的记录按各自目的使用，能够避免把固定体积产生的平直密度线误解为密度估计已经没有误差。

### 从建盒到观测量导出的完整脚本

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
cp topol.template.top topol.top
"$gmx" solvate -cs spc216.gro -box 3 3 3 -o water.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c water.gro -p topol.top -o em.tpr -pp em.top -po em.processed.mdp > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 4 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr -po nvt.processed.mdp > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr -po npt.processed.mdp > npt.grompp.log 2>&1
"$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off > npt.stdout.log 2>&1
for step in 2fs 1fs; do
  "$gmx" grompp -f "nve-$step.mdp" -c npt.gro -t npt.cpt -p topol.top -o "nve-$step.tpr" -po "nve-$step.processed.mdp" > "nve-$step.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "nve-$step" -ntmpi 1 -ntomp 4 -pin off > "nve-$step.stdout.log" 2>&1
done
printf 'Potential\n0\n' | "$gmx" energy -f em.edr -o em-potential.xvg > em-potential.log 2>&1
printf 'Temperature\nPotential\nKinetic-En.\nTotal-Energy\nPressure\n0\n' | "$gmx" energy -f nvt.edr -o nvt-energy.xvg > nvt-energy.log 2>&1
printf 'Density\nVolume\nTemperature\n0\n' | "$gmx" energy -f npt.edr -o npt-density-volume-temperature.xvg > npt-properties.log 2>&1
for step in 2fs 1fs; do
  printf 'Total-Energy\nTemperature\nPotential\nKinetic-En.\n0\n' | "$gmx" energy -f "nve-$step.edr" -o "nve-$step-energy.xvg" > "nve-$step-energy.log" 2>&1
done
printf 'System\n' | "$gmx" trjconv -f nve-2fs.xtc -s nve-2fs.tpr -o trajectory.gro -dt 2 -pbc mol > trajectory-export.log 2>&1
"$gmx" check -f nve-2fs.xtc > trajectory-check.log 2>&1
```

与本例本地运行采用的输入一致。文本文件保存在同一例题目录，力场定义由指定GROMACS安装提供。

脚本中的输出重定向把每一步的终端信息保存到相应日志，便于查看实际停止位置。grompp 负责检查和组装运行输入，mdrun 负责推进，energy 提取所选物理量，trjconv 负责生成用于观看的轨迹表示。最后的 check 检查轨迹帧和时间信息。这些工具各自完成一件明确的事，组合起来以后仍能逐步检查；如果某一步失败，后面的命令不会凭空得到正确输入。

输入中的 constraints = h-bonds 还容易引起一个词义误会。这里指的是涉及氢原子的共价键约束，并不是把不同水分子之间的氢键网络固定住。水的刚性几何按相应拓扑使用 SETTLE，而水分子之间仍能改变相对位置和取向，氢键接触也可以形成和断开。化学键、几何约束与分子间氢键是不同概念，理解这个区别，才能正确阅读水的动态网络。

运行时可以先查看最小化日志，确认几何整理是否达到阈值，再查看 NVT 和 NPT 的输出。在已有完整结果时，重新执行分析不需要重新计算全部轨迹；若修改了力场或动力学参数，则需要产生与新输入对应的新运行结果。这里“修改分析”和“修改模拟”是两种不同工作：前者改变如何测量已有运动，后者改变运动本身怎样产生。把它们分开，也能让计算资源花在真正需要更新的地方。

本地电脑的运行时间会随处理器、线程、编译方式和系统负载变化。例题把可复查的对象放在物理时长、体系规模、输入设置和实际输出上，并记录真实执行环境。线程数影响工作怎样分配给处理器，不会把 100 ps 自动变成更长的分子观察时间。对于更大体系，可以进一步考虑并行和加速，但首先需要确认当前模型与分析已经能回答所设定的问题。

## 把分阶段记录画在合适的坐标轴上

一张能够解释的图，需要先区分横轴代表什么。最小化的横轴是更新步骤，反映坐标优化的进程；NVT 和 NPT 的横轴是物理时间，反映动力学演化。把它们连成一条没有说明的时间曲线，会制造一种错误印象，好像水先经历了若干皮秒的“能量下降”，才开始正常运动。我们将两类记录放在不同面板，保留它们各自的量纲与意义。

不同阶段的时间还可能从各自的起点重新计数，或者根据输入设置延续已有时间。程序应读取文件中的真实时间值，并在图上说明所处阶段，再决定是否为了展示全过程而增加明确的阶段偏移。最小化使用柔性几何、动力学恢复刚性模型时，能量分项的定义也会变化，因此不把它们直接连成一条要求处处连续的能量线。阶段边界上的解释，与曲线本身同样属于测量的一部分。

提取 XVG 时，程序从列标签识别物理量，避免依赖交互选择的输入顺序。最小化面板画势能，并在文字结果中给出日志中的最终最大力和停止信息；NVT 面板显示温度与能量；NPT 面板把体积和密度配合起来阅读。原始曲线保留细节，统计概括则说明采用了哪一段数据。这样可以看到调整过程，又能看清后段记录的平均水平与波动。

### 完整Python：按阶段读取并绘图

```
#!/usr/bin/env python3
"""Read actual water-stage records and plot each on its proper axis.

Usage: python analyze_stages.py RUN_DIRECTORY --output figures --language en
The directory contains em.log, nvt-energy.xvg, and
npt-density-volume-temperature.xvg. Dependencies: numpy, matplotlib.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_xvg(path: Path):
    legends, rows = {}, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = re.sub(r"[^a-z]", "", match[2].casefold())
            continue
        if line == "&":
            raise ValueError("Expected one dataset in the XVG file.")
        rows.append([float(value) for value in line.split()])
    values = np.asarray(rows, dtype=float)
    if values.ndim != 2 or len(values) < 2 or not np.all(np.isfinite(values)):
        raise ValueError("Missing or nonfinite XVG data.")
    if np.any(np.diff(values[:, 0]) <= 0):
        raise ValueError("Physical times must increase strictly.")
    columns = {}
    for index, name in legends.items():
        if name in columns or index + 1 >= values.shape[1]:
            raise ValueError("Ambiguous XVG legends.")
        columns[name] = values[:, index + 1]
    return values[:, 0], columns


def read_minimization(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    records = {}
    current_step = None
    for index, line in enumerate(lines[:-1]):
        if re.fullmatch(r"\s*Step\s+Time\s*", line):
            current_step = int(lines[index + 1].split()[0])
        # GROMACS energy tables use 15-character fields.
        headings = [line[j:j + 15].strip() for j in range(0, len(line), 15)]
        if "Potential" in headings and current_step is not None:
            numbers = lines[index + 1].split()
            if len(numbers) != len(headings):
                raise ValueError("Energy-table headings and numbers disagree.")
            records[current_step] = float(numbers[headings.index("Potential")])
    if len(records) < 2:
        raise ValueError("Cannot identify minimization step and potential records.")
    match = re.search(r"Maximum force\s*=\s*([+\-\d.eE]+)", text)
    if not match:
        raise ValueError("Final maximum-force summary is missing.")
    final_force = float(match[1])
    convergence = re.search(r"Steepest Descents converged to Fmax", text) is not None
    steps = np.array(sorted(records), dtype=int)
    potential = np.array([records[int(step)] for step in steps])
    return steps, potential, final_force, convergence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figures"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    stage = args.run_directory
    steps, potential, fmax, converged = read_minimization(stage / "em.log")
    tnvt, nvt = read_xvg(stage / "nvt-energy.xvg")
    tnpt, npt = read_xvg(stage / "npt-density-volume-temperature.xvg")
    for key in ("temperature", "potential", "kineticen"):
        if key not in nvt:
            raise ValueError(f"NVT series is missing: {key}")
    for key in ("density", "volume", "temperature"):
        if key not in npt:
            raise ValueError(f"NPT series is missing: {key}")
    mask = tnpt >= tnpt[0] + 0.5 * (tnpt[-1] - tnpt[0])
    count = int(mask.sum())
    if count < 2:
        raise ValueError("Too few samples in the NPT observation window.")
    units = {"density": "kg/m^3", "volume": "nm^3", "temperature": "K"}
    summary = [{"quantity": key, "unit": units[key], "samples": count,
        "start_ps": float(tnpt[mask][0]), "end_ps": float(tnpt[mask][-1]),
        "mean": float(np.mean(npt[key][mask])),
        "sample_standard_deviation": float(np.std(npt[key][mask], ddof=1))}
        for key in ("density", "volume", "temperature")]
    report = {"minimization": {"last_saved_step": int(steps[-1]),
        "final_maximum_force_kJ_mol_nm": fmax,
        "force_criterion_met": converged},
        "npt_window": summary,
        "spread_definition": "Sample SD describes fluctuations, not uncertainty of the mean."}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "stages_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (args.output / "npt_window.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    zh = args.language == "zh"
    tr = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
        "axes.spines.right": False, "figure.facecolor": "#faf9f4",
        "axes.facecolor": "#faf9f4", "savefig.facecolor": "#faf9f4"})

    def save(fig, name):
        fig.savefig(args.output / (name + ".svg"))
        fig.savefig(args.output / (name + ".png"), dpi=180)
        plt.close(fig)

    fig, axis = plt.subplots(figsize=(11, 5), constrained_layout=True)
    axis.plot(steps, potential, color="#2b7b70", linewidth=1.6)
    axis.set(xlabel=tr("最小化更新步号", "Minimization update index"),
             ylabel=tr("势能 / kJ mol⁻¹", "Potential energy / kJ mol⁻¹"),
             title=tr("初始几何的最速下降整理", "Steepest-descent preparation of the initial geometry"))
    axis.grid(axis="y", alpha=0.2)
    save(fig, "em_minimization")

    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True, constrained_layout=True)
    fields = [("temperature", tr("温度 / K", "Temperature / K")),
              ("kineticen", tr("动能 / kJ mol⁻¹", "Kinetic energy / kJ mol⁻¹")),
              ("potential", tr("势能 / kJ mol⁻¹", "Potential energy / kJ mol⁻¹"))]
    for axis, (key, label) in zip(axes, fields):
        axis.plot(tnvt, nvt[key], color="#2b7b70", linewidth=1)
        axis.set_ylabel(label)
        axis.grid(axis="y", alpha=0.2)
    axes[0].axhline(300, color="#ad6b40", linestyle="--", label=tr("300 K 目标", "300 K target"))
    axes[0].legend(frameon=False, fontsize=12)
    axes[-1].set_xlabel(tr("NVT 记录时间 / ps", "Recorded NVT time / ps"))
    fig.suptitle(tr("固定体积下的热运动", "Thermal motion at fixed volume"), fontsize=20)
    save(fig, "nvt_preparation")

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True, constrained_layout=True)
    for axis, key, label in [(axes[0], "volume", tr("体积 / nm³", "Volume / nm³")),
                             (axes[1], "density", tr("密度 / kg m⁻³", "Density / kg m⁻³"))]:
        axis.axvspan(tnpt[mask][0], tnpt[-1], color="#dbe9df", alpha=0.7)
        axis.plot(tnpt, npt[key], color="#2b7b70", linewidth=1)
        axis.axhline(np.mean(npt[key][mask]), color="#ad6b40", linestyle="--",
                     label=tr("后半窗口均值", "Second-half window mean"))
        axis.set_ylabel(label)
        axis.legend(frameon=False, fontsize=12)
        axis.grid(axis="y", alpha=0.2)
    axes[-1].set_xlabel(tr("NPT 记录时间 / ps", "Recorded NPT time / ps"))
    fig.suptitle(tr("固定分子数下的体积与密度", "Volume and density at fixed molecule count"), fontsize=20)
    save(fig, "npt_preparation")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

脚本从em.log明确读取更新步号，从XVG列标签读取动力学量；支持双语，生成分阶段SVG/PNG及窗口统计。

程序把 NPT 记录的后半段作为本次描述窗口，计算均值与样本标准差。均值是把选定数值相加后除以数目，表示窗口内的平均水平；标准差描述这些数值围绕均值散开的程度。若不同时间点存在相关性，标准差仍然可以描述波动，但平均值的不确定度需要进一步考虑有效独立信息量。第九讲会展开相关时间与分块统计，本讲先把观测窗口和量的定义写清楚。

观察窗口内的平均水平与波动式 3

![观察窗口内的平均水平与波动](https://ml-biomat.com/static/agent-math/8a1a2bfe926e22e3fe99c0a4.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Ak | 选定窗口中第k个测量值 | 与观测量相同；密度例为kg·m⁻³ |
| Ā | 窗口内算术平均值 | 与Ak相同 |
| sA | 样本标准差，描述数值散开的程度 | 与Ak相同 |
| n, k | n为测量数目且至少为2；k为测量编号 | 无量纲 |
| Σ, −, ², √, /, = | Σ从k=1累加到n；减去均值后平方；除以n−1并开方得到样本标准差；等号给出定义 | 运算符无单位 |

怎样理解均值概括中心，平方偏差让正负偏离不会相互抵消，开平方恢复原观测量单位。样本标准差的n−1是常用样本方差定义。

算一个例子三个示意密度998、1000、1002kg·m⁻³的均值为1000，样本标准差为2kg·m⁻³。本例统计使用选定窗口内的全部实际记录。

使用条件这些量描述选定记录。轨迹帧可能相关，标准差不是均值标准误，也不是置信区间；不确定度分析还需考虑相关与重复。

统计窗口必须与图中可见的过程相配合。后半段只是这次例题明确采用的描述规则；如果这段仍有明显缓慢趋势，就应继续观察并解释趋势，而不是因为规则已经写好就把它宣布为平衡。也可以把窗口分成两段，对比平均水平是否明显移动，再结合独立重复检查。这里每一个操作都在回答“这段记录还记得多少起始准备”，为后续更严格的误差分析提供直觉。

### NPT中互相联系的体积与密度

完整NPT时间记录与后半段描述窗口，均值和样本标准差按相同窗口计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/#zh-s6)

同一固定分子数的水盒，体积增大时密度降低。阴影为 50–100 ps 描述窗口，两幅图的虚线均按这同一个窗口计算。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 密度窗口均值 | 997.8 | kg m⁻³ |
| 密度样本标准差 | 11.26 | kg m⁻³ |
| 体积窗口均值 | 26.51 | nm³ |
| 体积样本标准差 | 0.2976 | nm³ |

在 50–100 ps 窗口中，平均体积为 26.506 nm³，样本标准差为 0.298 nm³；平均密度为 997.83 kg·m⁻³，样本标准差为 11.26 kg·m⁻³。两个面板的峰谷方向相反，体现同样多的水在不同体积中的质量密度变化。记录中还存在连续几皮秒甚至更久的起伏，短窗口平均会受到这些相关变化影响。这里保留完整曲线与窗口定义，下一步可以通过延长观察和独立重复比较平均值的稳定程度。

比较温度、体积和密度时，先确认它们来自同一阶段和相同时间范围。NVT 的体积由条件固定，NPT 的体积会变化；NVE 的温度可以随能量在动能与势能之间交换而涨落。不同阶段具有不同控制方式，因此不要把曲线是否水平当作唯一标准。图旁边标出的模型、目标条件、时间范围和测量定义，才是理解曲线的共同上下文。

总能量的曲线同样需要阶段背景。温控会与体系交换能量，压控还涉及体积变化及相应功，因此 NVT 或 NPT 中分子的动能与势能之和不必像孤立系统那样保持常数。某些算法另有可用于检查的扩展或有效守恒量，其定义包含控制器的作用。我们先在撤去控制的 NVE 分支中检查分子总能量，再逐步认识这些更完整的算法量，避免把受控系统的正常能量交换误判为积分失稳。

## “稳定”需要说明稳定的是哪一种观察

模拟能够顺利运行，说明数值步骤没有在当前设置下直接中断；温度围绕目标变化，说明温控记录具有相应表现；密度在一个窗口内没有明显趋势，则说明这一观察量在该窗口中的变化方式。它们各自提供一部分信息。若研究的是水分子的扩散、介电响应或稀有氢键排列，还需要对相应量建立采样与误差检查。一个已经看起来平稳的密度，不能替代所有其他物理量的时间尺度。

可以用一个开学后的教室作类比。到课人数很快稳定，不表示同学之间的座位交换、学习小组形成和交流方式都已经停止变化。人数相当于某个较快稳定的整体量，内部组织则可能需要更长时间。液体里同样存在不同尺度的运动；到大分子体系中，局部水的调整、侧链转动和整体构象变化之间的时间差还会更明显。因此，“平衡了多久”要结合“为了测什么”一起说。

周期边界下的视觉跳跃也需要按表示方式判断。画面中的一个分子从右侧跨到左侧，可能只是相同粒子经过周期边界；若把整个分子重组后观看，其内部形状应保持符合刚性模型。动画可以帮助发现明显空洞、局部重叠和错误的分子显示，也能直观认识移动与转动。正式统计仍要采用与物理问题相配合的坐标处理，例如扩散需要连续位移，局部结构则需要正确的周期距离。

### 准备后的水分子运动

真实nve-2fs轨迹，保留物理时间与周期盒信息，按完整分子表示。

NVE 能量检查将把“数值稳定”进一步拆开。总能量可能有小幅快速波动，也可能有缓慢漂移；二者影响不同，应该分别测量。改变时间步还可能改变某些输出能量定义中的离散时间关系，所以比较时使用各自初始值作基线，并保持相同起始状态与观察时长。第四讲会把这些记录和积分算法联系起来，让时间步选择建立在实际证据上。

若某个结果与预期不同，排查可以沿着文件与物理层次展开：先确认读的是哪一阶段、单位和列标签是否正确，再核对输入组合与几何，之后检查控制参数、相互作用设置与采样长度。这种顺序让分析从可直接检查的事实开始。它也保留了发现新物理现象的空间，因为只有先分清数据解释和数值设置，才知道一个持续存在的差异值得怎样进一步研究。

模型也规定了哪些化学过程会出现在记录中。这盒固定连接关系的水可以展示平移、转动和分子间接触，却没有通过电子重排来产生水的自解离。我们因此不把这条轨迹中的离子数变化作为酸碱平衡结果。以后研究核酸或蛋白质时，质子化状态会作为模型准备的重要选择；若问题本身涉及质子转移，则需要把能够描述该过程的方法纳入设计。

## 从第一次运行走向有目的的比较

完成水盒以后，可以把下一次计算设计成一个明确的比较。例如保持模型、粒子数与压强目标相同，将温度从 300 K 改为另一个选定值，重新准备并比较密度分布；或者保持物理条件相同，只改变时间步，检查数值结果。两类比较回答的问题不同：前者改变热力学条件，后者检查计算近似。若把它们同时改变，曲线差别的原因就会难以区分。

每次比较都应同时说明保持不变的对象和主动改变的条件，并使用一致的观测定义。对密度而言，窗口、单位和统计方式要一致；对结构而言，原子选择与周期处理要一致；对动力学而言，物理时间和采样间隔要足以描述关注的变化。随后再通过重复运行了解波动幅度。这样，输入文件、实际轨迹和最终图表就沿着同一个问题连接起来。

这盒水已经提供了完整的起点：从坐标与拓扑出发，经过有明确目的的准备阶段，得到真实的运动和热力学记录，再用可重复的程序解释它们。接下来我们会打开相互作用和积分过程，理解力场、时间步与周期边界怎样共同决定这些记录。等到体系里加入蛋白质、核酸和聚合物时，这些选择仍然需要逐项说明，但它们已经有了可以追踪的物理含义。

## 延伸阅读与开放资料

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  分阶段水盒准备、运行与密度观测流程改编。

  SPC/E、300K、1bar与2026.4算法；柔性几何整理后恢复刚性MD；增加双NVE诊断和原创双语分析。流程改编保留CC BY-SA4.0。
- [Canonical sampling through velocity rescaling](https://doi.org/10.1063/1.2408420) · Giovanni Bussi; Davide Donadio; Michele Parrinello · Factual scientific citation; no reused figure

  2007年v-rescale的统计目标与历史。

  概念图和教学叙述原创。
- [Pressure control using stochastic cell rescaling](https://doi.org/10.1063/5.0020514) · Mattia Bernetti; Giovanni Bussi · Factual scientific citation; no reused figure

  2020年C-rescale与体积涨落。

  按水盒问题独立解释。
- [Energy minimization, GROMACS2026.4](https://manual.gromacs.org/2026.4/reference-manual/algorithms/energy-minimization.html) · GROMACS developers · Technical reference

  最速下降与最大力停止含义。

  独立类比与本例参数解释。
