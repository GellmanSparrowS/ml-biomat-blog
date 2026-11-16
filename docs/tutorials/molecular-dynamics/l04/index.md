# 温度、压力与边界怎样控制

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l04/
Language: zh-CN

从同一温度下不同质量的速度分布，读懂热浴、压力和边界怎样进入分子模拟。

## 材料处在什么环境里，决定我们怎样模拟

一块水凝胶放在敞口培养皿、密封容器和受压夹具中，即使化学组成相同，也会面对不同的环境。它能否与周围交换热量，体积是否允许改变，表面附近有没有固体壁面，都会影响结构与运动。在模拟里，这些条件不是实验台上默认存在的背景，需要通过温度控制、压力控制和边界设置明确表达。前三讲建立了粒子、力与时间的关系，这一讲把盒子放回环境中，说明哪些量由外界规定，哪些量应该由体系自身响应产生。

为了把概念讲清，我们继续使用两类中性 LJ 粒子的固定周期盒。它不需要准备化学结构，就能够展示热运动、温度涨落和相互作用对压力的贡献。第一段和最后一段没有热浴，中间一段接触目标温度为一的 Langevin 热浴；盒子体积始终保持不变。因此，压力在本次运行中是被测量的响应量，不是另一个同时被指定的目标。读者将从同一段实际数据看到：温度受到调节时，压力仍然会随运动和构型改变。

在日常语言中，“恒温”容易让人想到温度计永远显示同一个数。分子尺度的体系却不断交换能量，瞬时动能有自然涨落；恒温算法要维持的是符合目标条件的统计状态。就像一个房间保持在合适温度附近，空调并不会要求每一小团空气在每一瞬间具有完全相同的运动速度。我们需要观察平均、分布与结构是否稳定，而不是把一条完全没有波动的温度线当作理想结果。

压力也不能只用“粒子撞墙”来理解，因为周期盒没有真实容器壁面，却仍然具有压力。粒子运动输运的动量，以及相互作用传递的力，共同决定体系对体积变化的响应。后面我们会把这两部分分别画出来，读者能够看见吸引作用为何可能使总压力小于单看热运动得到的值。这样的分解对理解凝胶溶胀、液体密度和材料受力都很有用，因为它让宏观读数与微观机制建立了具体联系。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s1)

图 1 · 环境耦合的概念图：热浴可以交换热量；体积改变时还涉及边界做功。本次LJ基线保持体积固定。

本讲读完后，你应该能够说明温度计算用了哪些速度，为什么较重粒子在同温度下具有较窄的速度分布，Langevin 的阻尼时间实际控制什么，以及固定盒和可变盒分别对应什么比较。代码部分会直接读取前几讲的真实轨迹，按类型画速度分布，并把压力拆成动能项和位力项。我们也会讨论表面和流动时需要改变哪些定义，使同一套术语能够继续用于后面的水、长链和网络课程。

选择环境条件时，先写出研究问题往往比先选择某个命令更有效。如果要比较固定浓度下的链构象，可以先固定组成和体积，观察不同温度；如果要得到某一压力下的体相密度，体积就需要有调整的自由度；如果研究表面吸附，则壁面附近的几何和非均匀密度成为中心。软件提供许多组合，但每一种组合都应该能够回答一句清楚的话：这次计算让材料与外界交换什么，又把什么固定下来？

## 温度描述热运动，不要求所有粒子一样快

在经典粒子模型中，温度通过许多自由度的动能联系到热运动。一个自由度可以先理解为一个独立运动方向：三维平移粒子具有三个速度分量。用各粒子的质量乘速度平方，再相加，就得到相关动能；按照参与的自由度数换算，得到瞬时温度。它是对一组运动的统计描述，不是贴在每个粒子上的固定属性。某个粒子一瞬间速度很小，不意味着它与周围粒子处于另一个独立温度环境。

从参与的运动计算温度式 1

![从参与的运动计算温度](https://ml-biomat.com/static/agent-math/ec004a10442098247716a218.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| K | 温度计算包含的平移动能总和 | ε₁₁ |
| mᵢ, vᵢ | 第 i 个粒子的质量和速度矢量 | m₁; σ₁₁/τ |
| T | 瞬时温度 | ε₁₁/k_B |
| k_{B} | 玻尔兹曼常数，LJ 约化单位中数值为 1 | 能量/温度 |
| f, N | 参与的独立速度自由度数与粒子数 | 1 |
| Σ | 对参与统计的全部粒子逐项求和 | 无量纲运算符 |
| \|vᵢ\|² | 第i个粒子三个速度分量的平方和 | σ₁₁²/τ² |
| =, −, /, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解经典平衡时，每个二次型速度自由度平均具有 k_BT/2 的动能。用当前总动能反算，得到会随运动波动的瞬时温度。

算一个例子N = 1600 时，f = 4797；K = 2398.5 时，T = 2 × 2398.5 / 4797 = 1。这里的 K 是总量；每粒子动能为 2398.5/1600 = 1.4990625。

使用条件本讲无内部约束且没有施加平均流动；自由度按默认三维温度约定扣除三个整体平移自由度。刚体、固定原子和流速偏置需要相应定义。

第一类粒子的质量为一，第二类为五。相同温度下，每个独立平移方向具有相同的平均动能尺度，因此较大质量对应较小的平均速度平方。把这个平方关系开平方，得到第二类速度宽度大约是第一类的五的平方根分之一。这里比较的是分布宽度，绝不是要求每个较重粒子都比每个较轻粒子慢。两类分布有重叠，也都有速度随时间改变的个体；统计规律组织的是这些不同瞬间出现的频率。

我们选择 x 方向速度来画分布，因为它可以为正、为负，容易看到整体是否围绕零对称。没有平均流动的经典平衡分布中，一个速度分量具有高斯形状，也就是中间较高、向两边平滑降低的钟形曲线。横轴的小区间宽度乘以曲线高度，近似给出速度落在这一区间的概率。因此纵轴叫概率密度，具有速度单位的倒数；只有把整个区间面积加起来，才得到没有单位的概率。

同一热环境中的速度分量分布式 2

![同一热环境中的速度分量分布](https://ml-biomat.com/static/agent-math/088377e2d97fa235099337e6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| p(vₓ) | x 速度分量的概率密度 | τ/σ₁₁ |
| vₓ | 带正负号的 x 方向速度 | σ₁₁/τ |
| m | 该类粒子的质量 | m₁ |
| T | 平衡参考温度 | ε₁₁/k_B |
| k_{B} | 连接温度和能量的常数 | 能量/温度 |
| s_{v}ₓ | 这一分布的标准差，即宽度尺度 | σ₁₁/τ |
| π, exp, √, ² | 圆周率、指数函数、平方根、平方 | 1 |
| =, −, /, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解速度的动能随 m vₓ²/2 增加，热平衡权重随这部分能量相对 k_BT 的大小指数衰减。前面的系数使全速度范围内的概率面积等于 1。

算一个例子T = k_B = 1 时，m = 1 的宽度为 1；m = 5 的宽度为 √0.2 ≈ 0.447214。两类 x 方向的平均动能都为 k_BT/2 = 0.5。

使用条件这是无平均流动时、经典平衡的单个速度分量参考；有限体系整体动量约束可带来细小修正。它与非负三维速率的分布不同。

速度分量与速率的区别值得再想一遍。一个粒子沿 x 方向向左走，x 速度为负；沿 y 方向走得很快但 x 方向几乎不动，x 速度仍接近零。三维速率则把三个分量平方相加后开平方，总是非负。把所有分量的绝对值混在一起画图，会改变分布形状和归一化。本讲固定观察 vx，是为了让符号、平均流动和质量关系能够在同一张图里辨认。

有限自由度下的温度波动还可以估计一个参考尺度。经典正则分布中，若有 f 个独立二次型速度自由度，瞬时温度的相对标准差与 f 的平方根成反比。当前自由度计数给出约零点零二零四的温度标准差，与实际窗口约零点零二一一处于相近尺度。这个联系说明波动并非全部来自程序误差；粒子越多，整体温度通常显得更平稳，但单个粒子的热运动依然存在。

有限自由度为何会有温度涨落式 5

![有限自由度为何会有温度涨落](https://ml-biomat.com/static/agent-math/94604f47d2c04ca8636dcf5e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| T₀ | 经典正则分布的目标温度 | ε₁₁/k_B |
| s_{T} | 该分布中瞬时动能温度的标准差 | ε₁₁/k_B |
| f | 独立二次型速度自由度数 | 1 |
| √ | 平方根 | 1 |
| =, /, × | 等号连接同一个物理量的两种表达；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解每个速度平方贡献都有涨落；把 f 个独立二次型自由度合起来，动能相对涨落随自由度增加而变小。

算一个例子f = 4797、T₀ = 1 时，参考标准差为 √(2/4797) ≈ 0.020419。实际 50 至 100 时间窗口内的读数标准差约 0.021081，数值处在相近尺度。

使用条件这是经典正则分布下二次型自由度的统计关系。有限窗口的标准差会有取样变化；应与速度分布及慢结构观察共同使用。

实际直方图来自许多粒子和时刻的记录。把速度轴分成小箱，数出每个箱子里有多少读数，再按总读数和箱宽归一化，就能与理论概率密度叠在一起。箱子太窄时，曲线显得锯齿很多；太宽时，又会把分布形状抹平。这里两类粒子使用相同的速度范围和分箱，让宽窄可以直接比较。读数来自同一段轨迹，数量很多也仍然可能彼此相关，因而这些计数不等于同样数量的独立实验。

温度定义还需要区分热运动与整体移动。如果整盒粒子一起沿同一个方向平移，所有速度都会增加一个共同分量，但内部并没有因此变得更热。流动材料中，更常见的是不同位置具有不同平均流速；温度应当依据相对于适当流场的随机运动定义。LAMMPS 提供减去质心运动或流速偏置的温度计算。关键是让用于恒温的速度定义与科学问题一致，否则热浴可能把我们本来要研究的流动当成需要消除的热量。

这一讲没有施加宏观流动，初始化也移除了整体线动量，因而使用基本平移温度作为起点。刚性水分子会减少独立自由度，固定的基底不应像活动流体一样参与温度平均，有限大小粒子还可能具有转动动能。后续遇到这些对象时，我们会重新统计哪些运动真正存在。温度公式能够反复使用，靠的是每次都重新核对其分子和分母，而不是把“三乘粒子数”当作任何体系都相同的常数。

## 从布朗运动理解 Langevin 热浴

显微镜下悬浮微粒的持续不规则运动，曾经把一个难题摆在研究者面前：黏性阻力似乎应该让运动停下来，为什么颗粒却一直受到扰动？Langevin 在1908年的分析中，把流体对颗粒的作用分成与速度有关的阻力，以及不断改变方向的附加作用。前一项消耗已有运动，后一项保留周围分子热运动带来的扰动。这种分解把可见颗粒的运动与没有逐个追踪的流体分子联系起来，也成为今天许多随机动力学方法的出发点。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s3)

图 2 · 以 Langevin 的分解思想解释热浴：阻力耗散运动，随机作用保留热扰动。

在当前模拟中，显式的 LJ 相互作用负责粒子之间的保守力，Langevin 热浴另外给每个粒子加入阻力和随机力。可以把它想成在保留模型中粒子碰撞的同时，让每个粒子还接触一个没有画出来的热环境。这个环境不是一盒具有水分子形状、电荷和氢键的真实水；它通过选定的阻尼和噪声规律表示某些交换作用。研究溶剂的具体局部结构时，需要后面水和离子章节的显式模型。

阻力和随机扰动共同表示热环境式 3

![阻力和随机扰动共同表示热环境](https://ml-biomat.com/static/agent-math/e095fcbec0db61a4192d2f8a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| m, v | 粒子质量与某一方向的速度 | m₁; σ₁₁/τ |
| dv/dt | 速度对时间的变化率，即加速度 | σ₁₁/τ² |
| F_{c} | 所选方向的保守相互作用力 | ε₁₁/σ₁₁ |
| τ_{d} | 阻尼时间，对应输入中的 damp | τ |
| ξ(t) | 统计强度与温度及耗散配合的随机力 | ε₁₁/σ₁₁ |
| t | 时间 | τ |
| =, +, −, /, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解保守力描述显式粒子相互作用，速度反向的阻力消耗运动，随机力补充热涨落。为了维持目标热状态，随机力的统计强度与阻尼及温度相联系。

算一个例子m = 1、v = 0.2、τ_d = 0.1 时，阻力为 −2；同样速度与质量下，τ_d = 1 时阻力为 −0.2。这两种设置的随机力强度也需要按各自阻尼匹配，不能只改一项。

使用条件这是一维分量的连续模型说明，三个方向对应处理；具体离散随机力由 fix langevin 的算法给出。它修改力，需与积分器配合。

改变时间步时，也要决定阻尼时间是否保持同一物理含义。如果把 timestep 减半而 damp 仍为零点一，热环境的响应时间保持原样，只是一个阻尼时间由更多积分步分辨；如果同时让 damp 减半，就把热浴耦合也改强了。前一种适合隔离积分误差，后一种研究的是不同耦合条件。两个命令中的数字看起来只差一个比例，却对应不同问题，这正是先用单位解释参数的实际价值。

只加入阻力会让动能不断降低，最终使一个无其他驱动的系统趋于停下；只加入随机扰动而没有配套耗散，则可能让动能持续增加。为了维持给定温度的统计状态，两者强度需要按照热涨落与耗散之间的关系配合。随机力的平均方向可以为零，但它仍然会增加速度平方的平均，因为正负扰动平方后都产生正贡献。这一点解释了为什么“平均随机力为零”与“没有热运动作用”是两回事。

输入里的 damp 是时间单位，不是阻力系数本身。当前值为零点一，时间步为零点零零五，两者相差二十个时间步。阻力中质量除以 damp 的系数说明，damp 越小，同样速度对应的阻力越强，随机作用的强度也随之调整。这会影响速度记忆和动力学时间，而不只是温度曲线看起来多快接近目标。若要将模拟扩散或黏度对应到某种真实溶剂，就需要进一步建立并检查阻尼的物理映射。

随机种子规定伪随机数序列的起点，让某个具体运行具有明确记录。更换种子会改变一段轨迹里的随机扰动历史，即使温度、质量和相互作用完全相同。多次种子重复可以帮助观察统计量在不同历史之间怎样波动。这里还使用 zero yes，让加入体系的随机力在每一步总体相加为零，减少随机热浴对整个盒子质心的无意推动。它不是把每个粒子的随机力都设为零，也不是把每个方向的热运动消掉。

这段热浴由两条命令配合实现：fix nve 推进位置和速度，fix langevin 只修改作用力。两者一起使用时，运动接触热浴，已经不再是孤立 NVE 系综。与之不同，fix nvt 自身就包含相应的恒温与积分操作；若在同一批原子上再叠加另一套积分，会使更新重复。读脚本时先画清每条操作的职责，再决定哪些可以并用，比根据命令名称中出现的 NVE 或 NVT 字母判断物理条件更可靠。

## NVE、NVT 与 NPT 说的是哪些量受到约束

系综可以理解为在同一组宏观条件下，许多可能微观状态组成的统计描述。这里的“许多”不要求同时在电脑里生成许多独立盒子；一段足够合适的轨迹可以对这些状态进行采样，但采样是否充分仍要检查。字母 N 表示粒子数，V 表示体积，E 表示能量，T 表示温度，P 表示压力。不同组合说明系统怎样与环境联系，也决定哪些量固定、哪些量允许波动。

NVE 描述固定粒子数和体积、没有外界能量交换的条件。温度由体系当前动能决定，可以因为势能与动能转换而改变。比如一个较低势能的初始结构获得初始速度后，运动可能把它带到较高势能的构型，相应动能下降，温度也随之降低。这并不需要一个隐藏的冷却器。读第一段实际结果时，把温度和势能一起看，就能追踪这种能量重新分配，而不是只盯着最初设置的速度温度。

NVT 固定粒子数、体积，并与规定温度的热环境联系。系统自身的总能量可以涨落，因为热浴能够向它提供或从它取走能量。当前中间阶段采用 Langevin 实现这种接触，目标温度保持为一。温度接近目标之后，结构仍可能缓慢改变，热浴会继续交换能量以配合这个过程。因此，“温度已经到一”并不说明粒子团簇、长链构象或网络结构已经完成所有松弛；这些慢变量需要自己的观察量。

NPT 再允许盒子通过尺寸变化响应外界压力，常用于调整体相材料的平均密度。可以类比一个能移动的活塞：外界压强与内部响应共同决定容积，而温度由另一条热交换通道控制。模拟中的压力控制器通常通过附加动力学变量调整盒子，不等于每一步都把盒长直接设成某个理想气体公式给出的值。粒子相互作用、压缩性以及控制器的响应时间共同影响体积如何变化。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s4)

图 3 · 字母表示指定条件，不要求每一个瞬时读数都固定为同一个值。

允许体积变化还会同时改变浓度。保持溶质数目不变而让盒子变大，单位体积中的溶质变少；反过来压缩，浓度随之升高。因而，用压力控制比较两种材料时，应记录它们得到的平均体积与组成，说明是否仍在比较同一浓度条件。如果研究问题要求严格固定浓度，固定体积往往是更直接的安排，或者需要先通过准备过程找到对应的状态。这种选择将环境条件与实验能够控制的量连接起来。

压力控制的响应时间过短，可能使盒子对瞬时噪声反应过强，出现剧烈的体积摆动；响应过慢，又会让密度调整耗费较长时间。这个参数也有时间单位，不能把“多少个时间步”的建议原封不动填进 fs、ps 或约化单位脚本。先确定单位和时间步，再将期望的响应尺度写成正确数字，随后检查体积、压力、能量和结构的实际变化。控制器的参数选择仍然属于需要验证的数值设计。

本次实际例题始终固定体积，因此展示的是 NVE 与固定体积热浴之间的转换。NPT 在这里帮助读者区分另一类研究条件；后面的熔体与网络例题会结合具体结构准备过程再讨论密度调整。对于有自由表面的薄层或固定基底，整个盒体积可能包括真空或不参与运动的区域，直接把体相各向同性压力控制套上去，会改变本来要研究的几何。条件的选择必须与对象的结构同时考虑。

同一个材料并不只有一种永远正确的系综。先在指定温度和压力下准备一个体相状态，再固定其体积观察一段运动，是一种具有清楚目的的组合；在固定应变下观察应力松弛，则对应另一种安排。每次切换都要说明继承了什么状态、改变了哪个环境条件，以及从哪一段开始测量。前三讲的重启和分段记录，正好使这些切换能够在文件与物理解释中保持一致。

## 没有墙的周期盒，压力从哪里来

压力的单位是力除以面积。可以从一个活塞受到的推力开始理解：同样大小的面积上，内部传给活塞的平均推力越大，压力越大。在周期体系里，虽然没有这个真实活塞，仍然可以通过微观动量输运和相互作用计算对应的压力。把盒子想象成能够做一个很小的均匀体积变化，内部状态对这种变化的响应就与压力相联系。这个想象并不要求当前固定盒真的发生变化，它帮助我们理解被测量的量。

对本讲的无键成对作用体系，压力可以拆成动能贡献和位力贡献。动能项来自运动携带的动量，与全体系动能除以体积有关。位力项把每对粒子的间距与沿连线的作用力相乘，再对不同粒子对求和。这个乘积具有能量单位，再除以体积就得到压力单位。三维中除以三，表示把三个方向的对角贡献取平均，得到一个标量压力。后面研究拉伸或剪切时，还需要保留各个方向的张量分量。

压力的动能与位力贡献式 4

![压力的动能与位力贡献](https://ml-biomat.com/static/agent-math/ed5131661fd03a90d6868d43.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| P, P_{kin}, P_{vir} | 总标量压力、动能项与位力项 | ε₁₁/σ₁₁³ |
| K | 全体系平移动能 | ε₁₁ |
| V | 三维盒体积 | σ₁₁³ |
| rᵢⱼ | 粒子对采用相应周期映像的间距 | σ₁₁ |
| Fᵣ,ᵢⱼ | 正值增大间距的成对径向力 | ε₁₁/σ₁₁ |
| Σᵢ<ⱼ | 把每个不同粒子对计入一次 | 1 |
| 3 | 三维对角方向的平均因子 | 1 |
| =, +, /, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解动量输运给出动能贡献，间距乘力给出相互作用对压力的贡献。两项分子都有能量单位，除以体积得到压力。

算一个例子取 K = 2398.5、V = 64000，动能压力为 4797/192000 ≈ 0.0249844。若某个说明性状态的成对位力和为 −960，则位力压力为 −0.005，总压力约 0.0199844。

使用条件适用于本讲无键、各向同性标量描述的三维成对体系。约束、长程项与其他力场会增加对应贡献；非均匀或受载体系还需分析张量和所选体积。

如果只考虑无相互作用的理想气体，压力的动能项就承担全部贡献，常见关系把压力、粒子数、温度与体积连起来。本例具有吸引和排斥，实际位力项并不为零，因而不能只用数密度乘温度代替测得压力。此外，我们使用的温度扣除了三个整体自由度，直接从总动能计算动能压力，可以避免在小体系里忽略这项计数约定。单位一致之外，公式所描述的对象也必须一致。

排斥作用沿着增大间距的方向，因此间距乘径向力的贡献为正；吸引作用趋向缩短间距，这一贡献为负。一个处于吸引主导环境的粒子群，可能具有正的动能压力，却被负的位力项抵消一部分。当前热浴后段50≤t<100窗口的实际数据就展示了这种情况：动能项平均约零点零二四九七，位力项平均约负零点零零四八七，总压力约零点零二零一零。把两项相加，宏观压力便与这一段运动和相互作用的共同结果对应起来。

瞬时压力往往比初学者预期的更容易波动，因为它把当时许多粒子相互作用的瞬间安排叠加在一起。一个短暂而较强的近接触，就可能改变某一时刻的位力。时间平均可以帮助读出较慢的中心趋势，但仍要说明窗口、相关性和单位。将每一条压力记录都强行拉到目标数字，会改变自然涨落，也可能扰动结构。压力控制器的工作方式应当与所需系综及模型响应一致，而不只是追求屏幕上的读数整齐。

标量压力还隐藏了方向信息。处于各向同性平衡液体中的三个法向分量，经过充分平均后应有相应对称性；受拉伸的网络、靠近墙面的液体以及有剪切流动的体系，则可能具有不同的法向与切向响应。这时用一个平均值描述全部受力会丢掉关键结构。以后看应力曲线时，我们会明确张量分量、符号约定和归一化体积，让“压力增加”和“某方向拉应力增加”不再被笼统地混写。

这里的位力图由实际输出压力减去根据动能计算的动能项得到，适用于当前只有该类成对作用、没有内部刚性约束的模型。加入水分子约束或长程静电之后，位力会包含相应额外贡献；固定基底、外加墙力和外场的处理也需要结合具体定义。分解的思想保持不变，参与求和的物理对象却会随模型改变。读者可以把它当作检查新模型的一个问题：现在这列压力究竟包括了哪些力？

## 周期、自由表面和墙面是三种不同几何

周期边界把有限盒子重复铺开，让一个穿过边界的粒子在相邻映像中继续运动。它适合近似均匀体相，却也规定了模型与自己的复制品相互邻接。一个过大的团簇、一条很长的链或某种相关长度接近盒长时，这种复制可能影响结果。因此，周期条件解决的是怎样表示周围环境的问题，有限尺寸是否足够仍要通过盒子大小比较来研究。盒子看起来没有墙，并不意味着它没有几何假设。

非周期边界则让某个方向不再重复。LAMMPS 中固定的非周期边界字母 f，说明盒面位置保持固定，但它本身不会自动产生反弹墙力。粒子越过这样的边界可能在更新时被移出体系，并触发粒子丢失问题。若希望粒子被一个物理或模型墙面阻挡，需要另外定义墙势或由显式基底原子产生作用。把边界方式与墙面相互作用分开理解，能够避免在文件中写了一个 f 就以为容器已经建好。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s6)

图 4 · 周期延伸、自由表面和显式墙面形成不同的邻居环境。

自由表面又是另一种对象。液体薄层的一侧如果留有真空，表面附近的粒子会缺少某些方向的邻居，密度和取向可能与内部不同。若用整个盒体积去除包括薄层在内的能量或位力，增加真空厚度就会改变某些归一化结果，即使液体层本身几乎没有变化。讨论薄层的局部密度、表面张力或膜的横向压力时，必须说明具体使用哪个区域和几何定义。这些量比一列没有范围说明的“整体压力”更接近问题本身。

有墙的体系还可能在壁面附近形成密度层化。粒子受到壁面的吸引和排斥，沿法向的分布不再均匀；墙如果移动，还会向流体输入动量和能量。此时热浴应如何作用、温度是否先减去流动速度、压力需要看哪个方向，都要与墙的运动配合考虑。第六讲的受限水与离子以及第十一讲的流动，都会把这些因素带入真实模型。现在先把几何关系画清，能够减少后来把局部现象当作均匀体相性质的混淆。

另一种常见误解是把 shrink-wrap 边界想成一个主动压缩材料的活塞。这类边界主要根据粒子所在范围调整计算盒的包围尺寸，属于空间管理；它不是按照给定外压对材料施加力的压力控制器。材料是否受压，应从真实作用力与加载条件判断，而不是只看盒子边界是否跟着粒子位置变化。名称中相近的“收缩”和“压缩”在物理上可能完全不同，具体命令的职责仍然是理解几何的出发点。

对于生物材料，几何选择通常直接对应样品形态：溶液中的一条链需要足够溶剂空间，体相熔体适合周期表示，膜和界面需要保留方向差异，吸附则需要明确表面。一个软件能够处理很多几何，并不意味着所有对象都应使用同一个立方周期盒。我们会在后续例题中逐项改变这些条件，让新增的几何复杂性始终对应一个具体研究问题。

## 用真实速度和压力读懂三段运行

下面的完整输入与前三讲保持同一模型，重点关注热浴的添加与移除，以及为分析保存的速度和热力学字段。第一段运行五千步，中间热浴段一万五千步，最后一万步；对应时间区间分别为零至二十五、二十五至一百、一百至一百五十。代码中的目标温度只在中间区间起作用。后面作图也只在这个区间画出目标水平线，使图中的标记与模型实际经历的环境一致。

### 固定体积下添加并移除热浴的完整输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PART A - ENERGY MINIMIZATION
# 1) Initialization
units lj
dimension 3
atom_style atomic
boundary p p p

# 2) System definition
region simbox block -20 20 -20 20 -20 20
create_box 2 simbox
create_atoms 1 random 1500 34134 simbox overlap 0.3
create_atoms 2 random 100 12756 simbox overlap 0.3

# 3) Settings
mass 1 1.0
mass 2 5.0
pair_style lj/cut 4.0
pair_coeff 1 1 1.0 1.0
pair_coeff 2 2 0.5 3.0


# Tutorial extension: numerical records, NVE/NVT comparison and restart files.
# Original particle population, box, pair coefficients and random seeds are kept.
# Output units: reduced LJ; energy values below are per atom.
pair_modify mix geometric
thermo 10
thermo_style custom step pe press
minimize 1.0e-6 1.0e-6 1000 10000
reset_timestep 0
velocity all create 1.0 49284 mom yes dist gaussian
timestep 0.005
thermo 100
thermo_style custom step time temp pe ke etotal press density
thermo_modify norm no flush yes
variable t equal time
variable T equal temp
variable U equal pe/atoms
variable K equal ke/atoms
variable E equal etotal/atoms
variable P equal press
variable rho equal density
fix records all ave/time 100 1 100 v_t v_T v_U v_K v_E v_P v_rho file thermo.dat
dump coordinates all custom 200 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify coordinates sort id
fix integrator all nve
# First NVE interval: 25 reduced time units.
run 5000
# NVT interval: 75 reduced time units, Langevin bath from the original tutorial.
fix bath all langevin 1.0 1.0 0.1 10917 zero yes
run 15000
unfix bath
write_restart equilibrated.restart
# Final isolated interval: 50 reduced time units.
run 10000
write_restart final.restart
write_data final.data
```

与前几讲使用同一份已运行输入，热浴只在 25 至 100τ 起作用；没有压力控制器。

分析程序从 thermo.dat 读取温度、每粒子动能和总压力，再用已知粒子数与盒体积计算动能压力。它还逐帧读取轨迹，在五十至一百的时间窗口里，把两类粒子的 x 方向速度分别收集起来。这一窗口包含五十帧，因此第一类有七万五千个速度读数，第二类有五千个。两类拥有不同计数，直方图都按概率密度归一化后，才能比较分布形状，而不是让粒子多的一类仅仅因为数量多就画得更高。

### 完整的速度分布与压力分解分析

```
"""Read actual LJ temperature, pressure and type-resolved velocities.
python analyze_ensemble.py --data-dir . --language en
Requires NumPy and Matplotlib.
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def velocities_in_window(filename, start=50.0, end=100.0):
    selected={1:[],2:[]}
    frames=0
    with Path(filename).open(encoding='utf-8') as f:
        while True:
            line=f.readline()
            if line=='':break
            if line.strip()!='ITEM: TIMESTEP':raise ValueError('Expected frame header.')
            time=int(f.readline())*.005
            if f.readline().strip()!='ITEM: NUMBER OF ATOMS':raise ValueError('Missing count.')
            count=int(f.readline())
            if not f.readline().startswith('ITEM: BOX BOUNDS'):raise ValueError('Missing box.')
            for _ in range(3):f.readline()
            fields=f.readline().split()
            if fields[:2]!=['ITEM:','ATOMS']:raise ValueError('Missing particle fields.')
            names=fields[2:]
            ti,vi=names.index('type'),names.index('vx')
            use=start<=time<end
            for _ in range(count):
                row=f.readline().split()
                if len(row)!=len(names):raise ValueError('Truncated trajectory.')
                if use:
                    kind=int(row[ti])
                    if kind not in selected:raise ValueError('Unexpected particle type.')
                    selected[kind].append(float(row[vi]))
            if use:frames+=1
    if frames==0:raise ValueError('No frames in selected window.')
    return {k:np.asarray(v) for k,v in selected.items()},frames


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path('.'))
    parser.add_argument('--out-dir',type=Path,default=Path('ensemble-analysis'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args()
    a=np.loadtxt(args.data_dir/'thermo.dat',comments='#',ndmin=2)
    if a.shape[1]!=8 or not np.all(np.isfinite(a)):raise ValueError('Expected eight finite columns.')
    time,T,ke,P=a[:,1],a[:,2],a[:,4],a[:,6]
    velocity,frames=velocities_in_window(args.data_dir/'trajectory.lammpstrj')
    N,V=1600,40**3
    kinetic_pressure=2*ke*N/(3*V)
    virial_pressure=P-kinetic_pressure
    summary={'velocity_window_reduced_time':[50,100],'saved_frames':frames,
             'velocity_reference_temperature_reduced':1.0,'particle_types':{},'stages':{}}
    for kind,mass in [(1,1.0),(2,5.0)]:
        v=velocity[kind]
        summary['particle_types'][str(kind)]={'mass_reduced':mass,'pooled_vx_records':len(v),
            'mean_vx':float(v.mean()),'vx_standard_deviation':float(v.std(ddof=0)),
            'equilibrium_reference_sigma_vx':float(np.sqrt(1/mass))}
    for name,left,right in [('initial_NVE_late',10,25),('bath_late',50,100),('final_NVE_late',120,150.000001)]:
        mask=(time>=left)&(time<right)
        summary['stages'][name]={'start':left,'end':min(right,150),'records':int(mask.sum()),
            'mean_T':float(T[mask].mean()),'std_T_readings':float(T[mask].std(ddof=1)),
            'mean_P':float(P[mask].mean()),'std_P_readings':float(P[mask].std(ddof=1)),
            'mean_kinetic_pressure':float(kinetic_pressure[mask].mean()),
            'mean_virial_pressure':float(virial_pressure[mask].mean())}
    zh=args.language=='zh'
    plt.rcParams.update({'font.family':['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans'] if zh else ['DejaVu Sans'],
        'font.size':14,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,
        'axes.labelcolor':'#173c42','text.color':'#173c42'})
    fig,axes=plt.subplots(2,1,figsize=(11.5,8),sharex=True,layout='constrained')
    fig.set_facecolor('#faf9f5')
    for ax in axes:
        ax.set_facecolor('#faf9f5');ax.axvspan(25,100,color='#e4eeeb');ax.grid(axis='y',alpha=.17);ax.set_xlim(0,150)
    axes[0].plot(time,T,color='#167d84',lw=1.2)
    axes[0].hlines(1,25,100,color='#b57448',linestyle='--',lw=1.2)
    axes[0].set_ylabel(('温度 ' if zh else 'Temperature ')+r'$k_BT/\epsilon_{11}$')
    for values,name,color in [(P,'总压力' if zh else 'Total','#173c42'),
        (kinetic_pressure,'动能项' if zh else 'Kinetic','#b57448'),
        (virial_pressure,'位力项' if zh else 'Virial','#4974ac')]:
        axes[1].plot(time,values,label=name,color=color,lw=1.2)
    axes[1].set_ylabel(('压力 / ' if zh else 'Pressure / ')+r'$(\epsilon_{11}/\sigma_{11}^3)$')
    axes[1].set_xlabel(('约化时间 ' if zh else 'Reduced time ')+r'$t/\tau$')
    axes[1].legend(frameon=False,ncol=3)
    fig.suptitle('热浴改变温度；固定盒中压力由状态产生' if zh else 'The bath controls temperature; fixed-volume pressure follows the state',fontsize=16)
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for ext in ['png','svg']:fig.savefig(args.out_dir/f'thermodynamic-stages-{args.language}.{ext}',dpi=200)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(11.5,6.5),layout='constrained')
    fig.set_facecolor('#faf9f5');ax.set_facecolor('#faf9f5')
    limit=max(4.0,float(np.ceil(max(np.abs(v).max() for v in velocity.values())*2)/2))
    bins=np.linspace(-limit,limit,71);x=np.linspace(-limit,limit,701)
    for kind,mass,color in [(1,1.0,'#167d84'),(2,5.0,'#b57448')]:
        ax.hist(velocity[kind],bins=bins,density=True,histtype='step',linewidth=1.8,color=color,
                label=(f'类型 {kind} 实际记录' if zh else f'Type {kind}: actual records'))
        pdf=np.sqrt(mass/(2*np.pi))*np.exp(-mass*x*x/2)
        ax.plot(x,pdf,color=color,linestyle='--',lw=1.5,
                label=(f'm = {mass:g}，T = 1 参考' if zh else f'm = {mass:g}, T = 1 reference'))
    ax.set_xlabel(('速度分量 ' if zh else 'Velocity component ')+r'$v_x/(\sigma_{11}/\tau)$')
    ax.set_ylabel(('概率密度 / ' if zh else 'Probability density / ')+r'$(\tau/\sigma_{11})$')
    ax.set_title('同一热浴，两种质量的速度宽度' if zh else 'One bath, two mass-dependent velocity widths',loc='left',fontsize=17)
    ax.legend(frameon=False,ncol=1,fontsize=12,loc='upper right');ax.grid(axis='y',alpha=.17)
    for ext in ['png','svg']:fig.savefig(args.out_dir/f'velocity-distributions-{args.language}.{ext}',dpi=200)
    plt.close(fig)
    (args.out_dir/'ensemble-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

从实际数值表和轨迹计算，按类型分组速度，并由总压力减动能项得到当前模型的位力项。

### 重现两种语言的全部图

```
python analyze_ensemble.py --data-dir . --out-dir ensemble-analysis --language zh
python analyze_ensemble.py --data-dir . --out-dir ensemble-analysis --language en
```

将程序与 thermo.dat、trajectory.lammpstrj 放在同一例题目录；需要 NumPy 和 Matplotlib。

实际结果中，两类 x 速度的标准差分别约为零点九九九一和零点四四四四；温度为一时，对应质量的高斯参考宽度分别为一和零点四四七二。图中把实际直方图与参考曲线一起显示，可以直观看到质量如何改变热速度尺度。参考线是由已知温度和质量计算出的分布，阶梯线来自实际轨迹；两者的角色不同。有限粒子数、整体动量约定和采样波动会影响精细差别，判断时应回到它们各自定义的条件。

### 两类粒子的实际速度宽度

50≤t<100 的 50 帧；类型 1 为 75000 个 vx 读数，类型 2 为 5000 个。阶梯线来自轨迹，虚线为 T = 1 的高斯参考。

LAMMPS 30 Sep 2026 update 1；三维周期盒，1500 个类型 1 粒子与 100 个类型 2 粒子；约化单位，时间步 0.005，总时长 150。物理输入沿用 Gravelle 等人的双组分 Lennard–Jones 教程，增加 NVE 对照及数值记录。

[下载参考数据与完整输入（ZIP） 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s7)

按粒子类型分别统计 50≤t*<100 内 50 帧的 x 方向速度，类型 1 与类型 2 各有 75000 和 5000 个读数。虚线为 T*=1 的高斯参考；速度宽度随质量变化。

再看热力学记录，热浴后段50≤t<100窗口的平均温度约为零点九九九六，而瞬时读数的样本标准差约为零点零二一一。这个数字表达该窗口内温度在怎样波动，并不是平均值的不确定度。移除热浴之后，动能可以继续与势能交换，最后一段的温度也不再被保持在一附近的同样分布。将两段的温度变化放到各自的能量交换条件下看，就能理解为什么“热浴已经关掉”会改变我们对曲线的期待。

### 热运动和相互作用怎样共同决定压力

实际温度与总压力；动能项由 2K/(3V) 计算，位力项由总压力减动能项得到，使用本例的固定盒与粒子数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s7)

温度与压力的实际时间记录。压力的动能贡献由全盒动能和体积计算，位力贡献由总压力减去动能项得到；正负贡献共同决定总压力。

压力图则揭示另一层关系：体积与粒子数相同，温度提高会改变动能贡献，而构型和相互作用改变会调整位力贡献。因此，即使数密度始终为零点零二五，三个阶段也可以具有不同的平均压力。程序同时保存窗口定义、记录数和两部分平均值，使这种比较可以由数据重新算出。读者还可以缩短或平移窗口，观察平均怎样随慢变化和取样范围改变，再把问题带到第十五讲的系统统计设计中。

## 把环境条件变成可解释的研究选择

当研究对象换成溶液中的高分子，首先要说明希望保留什么溶剂作用。若关心显式水分子在链周围怎样排列，就需要包含水的形状、电荷与相互作用；若研究较长尺度的链运动，隐式环境可能通过有效相互作用和阻尼保留选定效应。两者的动力学时间映射和可观察结构不同。Langevin 热浴提供的是一种明确的模型工具，选用它时应把所保留的交换作用与目标问题对应，而不是把它直接称作“水环境”。

若研究扩散、黏度或松弛时间，热浴参数会直接进入需要检查的因素。两个阻尼不同的模型可能具有相近的平衡构象分布，却以不同速度在这些构象之间移动。选择热浴时，应当把平衡性质与动力学性质分开安排验证。例如先检查温度和结构分布，再在确定的动力学条件下分析位移或应力相关；如果改变阻尼，比较时明确它是模型的一项变化。这样既能利用热浴帮助采样，也能保留对运动机制的清楚解释。

若研究材料受拉伸或剪切，整体速度场和外界做功需要加入温度、能量与应力的解释。测量热运动时要扣除哪部分有组织的流动，热浴作用在全部方向还是合适的子空间，边界怎样传递加载，都应与实际问题一致。一个“温度控制得很好”的运行，也可能把目标流动过度耗散掉。因此，后面的力学章节会把加载、恒温和测量放在同一张流程中说明，而不把恒温作为不影响结果的背景选项。

本讲的交互可以用一个直接的问题帮助检查理解：保持温度不变，把粒子质量从一调到五，速度分布为什么变窄，但它所代表的平均动能尺度没有因此变小？再把目标温度提高，分布会怎样展开？用图形观察后，回到质量乘速度平方的关系，就能把这些变化串起来。相比只记住“重的慢、热的快”，这种推理明确了比较时保持的条件，也能解释两个不同质量的群体如何处于同一个热环境。

探索单速度分量的高斯统计参考：质量和温度共同决定解析分布。

[Figure: 高斯速度概率密度](https://ml-biomat.com/tutorials/molecular-dynamics/l04/#zh-s8)

横轴是有正负方向的速度分量；质量和温度各自改变分布宽度。

从这里进入分子与长链，新增的每一种结构都会带来新的运动与约束：键有伸缩，角度有弯曲，刚性几何减少自由度，壁面使空间不再均匀。温度、压力和边界的基本问题仍然相同，只是参与的对象更丰富。下一讲开始把一个分子写进计算机，把粒子编号进一步连接成明确拓扑；我们将沿着已经建立的环境与统计语言，解释这些连接如何改变模型能够回答的问题。

## 延伸阅读与开放资料

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  两类 LJ 粒子、NVE 与 Langevin 流程、周期几何。

  增加环境选择解释、速度分布与压力分解的完整真实分析。
- [LAMMPS stable manual: fix langevin](https://docs.lammps.org/stable/fix_langevin.html) · LAMMPS developers · Official documentation consulted; software source GPL-2.0; original figures here

  阻尼、随机力、积分职责与 zero yes 含义。

  重新解释参数与实际模型的对应。
- [LAMMPS stable manual: compute pressure](https://docs.lammps.org/stable/compute_pressure.html) · LAMMPS developers · Official documentation consulted; no copied images

  动能与位力压力、自由度及张量定义。

  围绕当前成对模型推导算例并作数据分解。
- [Paul Langevin’s 1908 paper: On the Theory of Brownian Motion](https://www.physik.uni-augsburg.de/theo1/hanggi/History/Langevin1908.pdf) · Paul Langevin; translation by Anthony Gythiel, introduction by Don S. Lemons (1997) · Primary historical text in published translation; cited, no text or figures reproduced

  阻力与不规则分子扰动的历史分解思想。

  原创机制示意，没有使用论文图片。
