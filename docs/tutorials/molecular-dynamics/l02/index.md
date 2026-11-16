# 从输入文件到第一段轨迹

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l02/
Language: zh-CN

把输入、轨迹、数值表和重启状态串起来，学会从真实坐标得到可解释的图。

## 把一段运动变成能够读懂的记录

拍一段植物生长的视频时，镜头里的变化只是实验的一部分。还需要知道拍摄间隔、光照条件和每个画面对应的时间，否则就难以比较两株植物长得谁快。分子模拟也一样：粒子在屏幕上移动，说明某个模型产生了一条轨迹；要解释这条轨迹，还需要把它与输入参数、积分时间、粒子身份和统计记录连接起来。这一讲学习的正是这种连接。我们继续使用上一讲的两类中性粒子，让已经见过的运动成为一份可以重新读取、分析和接着计算的材料。

读完本讲，你可以从输入中找到某一列数据的定义，判断它是瞬时读数还是时间平均，分清周期盒内的显示坐标与连续运动坐标，并运行完整的 Python 程序画出对应曲线。我们还会把“从头重复一次”和“从保存状态接着算”分开说明。前者重新生成初始条件，后者继承已有位置和速度；它们对研究的作用不同。学习这些操作并不要求先会写程序，后面的代码会先按读文件、挑选数据、计算和作图四个步骤解释。

一次模拟的文件可以看成同一项实验的不同记录。输入文件说明怎样建立体系和推进计算；日志记录程序执行时的条件、阶段与数值；轨迹保存选定时刻每个粒子的属性；结构数据文件把某个状态写成便于阅读和交换的文本；重启文件则保存更多供同一软件继续计算的内部状态。它们之间有内容重叠，却各有重点。只保存一段动画，会留下运动的视觉印象，却丢掉重新定义测量或检查单位所需的大量信息。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s1)

图 1 · 文件的角色由所保存的信息决定，多个文件通过同一次运行的定义与时间相联系。

可以用一个具体问题来检验文件是否保存得合适：如果后来想知道某个粒子在最后一段运行中移动了多远，需要哪些信息？首先要认出同一个粒子，因此需要编号；其次要知道每帧的时间，因此需要步数和时间步；还要接上跨周期边界的路径，因此需要连续坐标或映像编号。只有一张末态截图，甚至只有一列总能量，都无法完成这项测量。输出设计应当从想研究的问题往回推，而不是把软件能够输出的所有字段都不加选择地保存。

这种从轨迹读出物理量的思路，有一段很有代表性的科学史。Rahman 在1964年研究液态氩的计算中，跟踪了864个按经典方程运动、以 Lennard–Jones 势相互作用的粒子。他把这些运动记录转化为粒子间的空间相关和自扩散等量，再与实验比较。那项工作的意义之一，是让微观运动成为可以定量讨论的观察对象。今天的图形工具更加方便，仍然需要经过同一个关键步骤：先定义怎样从一批坐标得到一个物理问题的答案。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s1)

图 2 · Rahman 的液态氩研究说明轨迹可以连接微观运动与可比较的物理量。图中路径是概念示意。

本讲的体系仍然使用三维周期盒、两类粒子、约化单位和分段的 NVE 与 Langevin 计算。固定这个物理背景之后，我们可以集中检查记录和分析是否正确。改变一个输出列名，不会使模型中的吸引突然变强；改变一个温度计算所选的粒子组，却会改变这一列量的含义。把“文件如何呈现”与“物理量如何定义”联系起来，是从会运行示例走向会设计研究的重要一步。

## 输入是一组按顺序生效的动作

输入文件是纯文本：里面的字符表达命令、数字、名字和说明，不包含文字处理软件的字体或段落格式。文件扩展名 .lmp 方便人辨认用途，LAMMPS 真正读取的是文件内容。终端里的当前目录则像桌上正在打开的文件夹，写一个相对文件名时，程序会按这个位置寻找它。将本例输入和分析程序放在同一个练习目录，可以让运行命令只使用简短文件名；转移整个目录时，这些内部对应关系也容易保持。

LAMMPS 通常从上向下读取命令，并在读到时执行它们。定义单位和粒子属性必须出现在建立盒子之前，设置某个粒子的质量则要等相应类型已经存在。这个顺序可以类比准备一张实验记录表：先决定列的含义，再建立对象，随后填入参数，最后开始测量。为了帮助阅读而加上的注释标题不决定执行逻辑，真正起作用的是命令的次序和状态。把一段命令挪到脚本另一处时，需要考虑它执行时哪些信息已经存在。

井号后面的文字通常是注释，用来说明一行或一组命令的作用。命令之间的名字也需要分清：simbox 是几何区域的名字，integrator 是某个 fix 的名字，records 是另一个 fix 的名字，T 则是一个变量名。名字本身没有温度或积分的魔法含义，后面的命令类型才决定它做什么。给对象起稳定而清楚的名字，可以让 unfix bath 这样的操作容易理解：它移除名为 bath 的作用，而不是删除粒子，也不是关闭全部动力学。

fix 这个词在日常英语里容易让人想到“固定”，但在 LAMMPS 中它表示在模拟过程中持续执行的一类操作。fix nve 进行时间积分，fix langevin 修改受力以表示热浴，fix ave/time 按指定安排记录或平均数值。它们可以同时存在，因为负责的工作不同。读代码时，与其把 fix 一律翻译成“固定住”，不如每次连同后面的具体类型一起读，并在脑中问：它改变状态、施加条件，还是记录观察量？

变量把一个可重复使用的名字与数值或表达式联系起来。脚本中的 equal 风格变量可以在需要时根据当前状态重新计算，例如温度、时间和总能量。表达式里写 pe/atoms，是把全体系势能除以当前粒子数，明确得到每粒子势能。本例先用 thermo_modify norm no 明确保留热力学总量，再由变量完成这一次除法；分析文件按实际得到的每粒子量命名。一个变量叫 U 并不能自动保证它是总势能，必须看等号后面的定义。

下面再次给出完整输入，便于把这些解释直接与运行对象对应。阅读时先找到建立对象的部分，再标出改变状态的命令，最后圈出记录数据的命令。三次 run 之间没有重新创建粒子，因此下一段从上一段结束的位置和速度继续。中间加入热浴，随后移除热浴，是在已有状态上改变环境。理解这个连续性之后，就能看出为什么不能把每个 run 都当成一次互不相关的新实验。

### 建立体系、分段推进并保存记录

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

与第一讲共用同一份输入。dump 中的 ix、iy、iz 为周期展开保留信息；thermo.dat 依次包含步号和七个数值字段。

## 给数字装上单位，也给时间找到起点

输入里的数值只有与单位体系结合起来才有物理含义。长度写成一，既可能是一米，也可能是一埃，还可能是一个约化长度单位。LJ 单位选定参考质量、参考长度和参考能量，然后用它们量度模型中的数值。可以把它想成先选一把尺子，再记录某件东西有几把尺子长。把参考尺子换长而不换数值，会改变对应的实际长度；若只是换单位而保留同一物理系统，所有相关参数都必须一起正确换算。

时间尺度不是可以随意补上的第四个独立数字。能量的量纲与质量、长度和时间相联系，所以当质量、长度和能量基准给定后，约化时间基准也随之确定。下面的关系可以通过动能来理解：速度有长度除以时间的单位，质量乘速度平方具有能量单位。让用这些基准组成的能量等于所选参考能量，就能解出时间基准。对于还没有映射到具体材料的双粒子类型模型，直接报告约化时间，往往比擅自把它称作某个真实液体的皮秒更清楚。

约化时间怎样联系到物理时间式 1

![约化时间怎样联系到物理时间](https://ml-biomat.com/static/agent-math/6c83e924ecd276859ba28f61.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| τ₀ | 由三个参考尺度确定的时间基准 | s |
| σ₀ | 参考长度；此例以第一类粒子参数作为约化基准 | m |
| m₀ | 参考质量 | kg |
| ε₀ | 参考能量 | J |
| t | 以秒表示的物理时间 | s |
| t* | 相对于 τ₀ 的约化时间 | 1 |
| √, / | 开平方与除法 | 1 |
| =, /, × | 等号连接同一个物理量的两种表达；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解由能量量纲 kg·m²/s² 可知，m₀σ₀²/ε₀ 具有时间平方的单位，开平方得到时间。约化时间乘这个基准即可换回物理时间。

算一个例子作为单纯的换算练习，取 m₀ = 10⁻²⁶ kg、σ₀ = 10⁻¹⁰ m、ε₀ = 10⁻²¹ J，则 τ₀ = √(10⁻²⁵ s²) ≈ 3.1623 × 10⁻¹³ s。约化时间 10 对应 3.1623 × 10⁻¹² s。

使用条件这些示例基准用于演示单位运算，没有把本讲的双粒子类型体系指定为某种实际材料。真实材料映射还需验证相互作用及目标性质。

步号还需要一个起点。输入先最小化，然后 reset_timestep 0，将接下来动力学的计数起点设为零。此后每步推进零点零零五个约化时间单位，第一段结束于步号五千，第二段结束于两万，第三段结束于三万。重设步号改变的是计数标签，粒子坐标和速度不会因此自动回到初始状态。因此，把两份步号都从零开始的文件拼在一起时，应先弄清它们是独立重复，还是同一段运动在不同位置重新编号。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s3)

图 3 · 本例时间轴与实际输入一致。输出间隔选择保存哪些状态，积分间隔决定程序怎样推进。

保存间隔和积分间隔也要分开记。轨迹每二百步保存一次，相邻帧相隔一个约化时间单位；热力学数据每一百步写一次，相邻行相隔半个时间单位。两种输出并不拥有相同的行数，也不能按“第一百行对第一百帧”的方式直接拼接。对齐数据时应使用真实时间或步号，就像把不同相机拍摄的视频按时间戳对齐。若需要比较瞬间结构与对应能量，可以选择两者共同保存的时间点。

数据记录得稀一些，文件会小一些，但失去的信息与问题有关。如果只想看一段慢速聚集过程，较稀的坐标记录可能已经足够；如果要分析短时间的速度变化，过大的保存间隔会跳过相互作用发生的细节。之后再把曲线插值得更光滑，并不会找回没有保存的真实瞬间。这里我们主要练习文件读取与连续坐标，保存安排能够展示较长时间的运动路径；研究快速碰撞或速度相关时，应重新按该过程的时间尺度设计输出。

文件里出现密度时，还要看它数的是什么。当前体系总共有一千六百个粒子，但由于两类质量不同，总质量是两千个参考质量单位。盒体积为六万四千个参考体积单位，于是数密度是零点零二五，质量密度是零点零三一二五。LAMMPS 的 density 关键字输出后者。这是一个很实用的例子：两列数可能都被笼统称为“密度”，却只有在分子、分母和单位都明确时才能比较。

## 轨迹是一张反复出现的粒子表

custom 轨迹由一帧接一帧的记录组成。每帧先给步号和粒子数，再给盒子边界，最后列出粒子属性。ITEM: ATOMS 后面的字段名就是读懂每列的钥匙。这里保存编号、类型、坐标、速度和三个映像编号；读程序按字段名寻找位置，而不把某个数字列永久认作 x 坐标。这样以后增加电荷或换一个列顺序时，分析逻辑仍然能够明确检查自己读到了什么。

粒子编号是跨时间连接记录的关键。并行计算可能改变粒子在文件中的输出次序，按坐标排序的显示软件也可能重排它们。输入中要求按编号排序，有助于人阅读；分析仍然显式寻找目标编号，让物理身份不依赖当前表格位置。类型则用于区分两类粒子，整个固定类型模型中，一个粒子的编号与类型都应保持相应的一致性。如果编号重复或粒子数发生意外变化，先检查数据完整性，再继续讨论运动。

周期坐标像把一条无限延伸的路折回同一张地图。粒子从盒子右侧走出去后，显示坐标回到左侧，而映像编号记录它已经跨过了多少个盒子。对于边长固定的正交盒，把盒内坐标加上映像编号乘盒长，就得到同一连续路径上的展开坐标。正向跨越使相应计数增加，反向跨越使它减少。两个连续坐标之差可以计算位移，两个显示坐标之差则可能把一次短的跨界运动误读成几乎整个盒长的跳跃。

把周期显示坐标接回连续路径式 2

![把周期显示坐标接回连续路径](https://ml-biomat.com/static/agent-math/6fa6bc506e7f3bdb2261eb69.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| x(t) | 时刻 t 的盒内显示坐标 | σ₁₁ |
| xᵤ(t) | 同一时刻的展开坐标 | σ₁₁ |
| iₓ(t) | x 方向有正负号的整数映像编号 | 1 |
| Lₓ | 固定正交盒沿 x 的边长 | σ₁₁ |
| t, t₀ | 当前时刻与选定的起始时刻 | τ |
| Δx | 起点到当前时刻的 x 位移 | σ₁₁ |
| Δ | 相对于起始值的差 | 1 |
| =, +, −, × | 等号连接同一个物理量的两种表达；加号将各贡献相加；减号取差或给出负方向；相邻因子相乘。 | 运算符无量纲 |

怎样理解每跨过一个周期盒，显示坐标会平移一个盒长。映像编号把被减掉或加上的整数个盒长重新补回，使不同帧属于同一条连续路径。

算一个例子盒边界为 −20 至 20，Lₓ = 40。起点 x = 19.8、iₓ = 0；稍后 x = −19.7、iₓ = 1。展开末坐标为 −19.7 + 40 = 20.3，因此位移为 0.5，而不是 −39.5。

使用条件用于本讲固定、正交的周期盒，并依赖记录下来的正确映像编号。倾斜或变形盒需要相应的盒矢量与形变处理。

把连续位置移过周期盒；每个盒长为 40，显示地图始终位于 −20 至 20。

[Figure: 周期盒内位置](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s4)

跨过边界时，显示坐标跳回另一侧，映像编号保留连续路径的信息。拖动滑块或用方向键逐步观察。

仅凭相隔很远的两帧显示坐标，通常无法唯一知道粒子中途跨过几次边界。假设两帧都显示在同一个位置，粒子可能几乎没动，也可能已经绕盒子走了一圈。用“相邻帧之间总是走最短距离”来猜测跨界，额外假定了每个方向的位移小于半盒长；保存太稀时这个假定会失效。本例直接记录映像编号，因此展开路径不需要依赖这个猜测。分析程序检查这些列是否存在，缺失时会明确指出需要重新输出的字段。

展开坐标的用法也有几何条件。这里盒子正交、长度固定，三个方向可以分别处理；倾斜盒需要用盒矢量组合映像编号，随时间变形的盒子还涉及整体形变与粒子相对运动的分离。等到拉伸和流动章节，我们会重新说明这些条件。现在选择简单盒子的好处，是让编号、位置和位移的关系清楚可见，再把几何复杂性逐步加回去。一个简单公式之所以可靠，正是因为使用它时知道它对应哪一种盒子。

下面的实际路径图同时保留显示坐标和展开坐标，并标出同一个粒子编号。对照曲线可以看见，显示坐标中的突跳发生在边界接缝处，而展开坐标把运动接成同一段历史。把其他粒子换进来，可以观察不同路径；单个粒子的轨迹用于理解记录方式，整个体系的扩散统计则需要对合适的粒子和多个时间起点进行平均。把这个测量层次分清，之后就不会从一条看起来很曲折的路线直接给出一个材料的扩散系数。

### 同一粒子的显示坐标与连续路径

来自实际轨迹的编号 1 粒子 x 坐标；展开坐标使用记录的映像编号，横轴与 thermo.dat 的约化时间对应。

LAMMPS 30 Sep 2026 update 1；三维周期盒，1500 个类型 1 粒子与 100 个类型 2 粒子；约化单位，时间步 0.005，总时长 150。物理输入沿用 Gravelle 等人的双组分 Lennard–Jones 教程，增加 NVE 对照及数值记录。

[下载参考数据与完整输入（ZIP） 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s4)

记录的映像编号把显示在周期盒两侧的位置接成连续路径。盒内坐标的跳变与展开坐标的连续变化描述同一粒子，横轴为相同的物理时间。

## 先看一列数据怎样产生，再谈平均

日志适合追踪程序经历了哪些阶段，但包含标题、警告、性能信息和多张数值表。直接把整份日志当成一张矩形表格读取，往往会在文本行处出错。为了让本讲的分析清楚，输入用一个独立的 thermo.dat 文件保存指定数值。它的注释行说明列名，后面的每一行按同样顺序写步号、时间、温度、每粒子势能、动能、总能量、压力和质量密度。日志仍然保留，用于解释运行条件和检查停止原因。

fix ave/time 后面的三个整数规定采样和输出安排，不能只看命令名字便断定做了很长的平均。本例使用 100 1 100：每一百步取一次值，每次输出只包含一个取样点，每一百步写一行，所以这里得到的是按间隔保存的瞬时读数。若改成 10 10 100，则每十步取一次，十次取样形成一组平均，每一百步输出一次。两种文件行数可能相同，却已经回答了不同时间分辨率的问题。

计算区间平均前，先选定对应的物理阶段。前二十五个时间单位没有热浴，中间七十五个时间单位有热浴，最后五十个再次没有热浴。把所有温度或能量不分阶段地平均，会把环境改变和自身涨落混合起来。若我们想观察热浴接入后的后段，可以选择时间大于等于五十且小于一百的记录；这个区间选择本身也应出现在图注和计算中，使读者知道平均覆盖哪一段运动。

窗口平均与读数波动式 3

![窗口平均与读数波动](https://ml-biomat.com/static/agent-math/a90ab6cb23a637e3e2e1b784.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Tⱼ | 选定窗口中第 j 次保存的温度 | ε₁₁/k_B |
| T̄ | 窗口内温度的算术平均 | ε₁₁/k_B |
| M, j | 记录数与记录的求和编号 | 1 |
| s_{T} | 使用 M − 1 分母的样本标准差 | ε₁₁/k_B |
| Σ, √, ² | 逐项相加、开平方、一个数与自身相乘 | 1 |
| =, −, /, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；分数线表示相除；相邻因子相乘。 | 运算符无量纲 |

怎样理解先把各次读数均分得到平均，再把偏离平均的差平方相加，度量波动。最后开平方，使结果恢复温度单位；M − 1 是常用样本方差约定。

算一个例子三个读数 0.9、1.0、1.1 的平均为 1.0；偏差平方和为 0.01 + 0 + 0.01 = 0.02，除以 2 后开平方得到 s_T = 0.1。

使用条件这里 M ≥ 2，所有读数具有相同定义和单位。此量描述窗口内的读数波动；相关数据中，它不是平均值的标准误差，M − 1 也不消除时间相关性。

平均值把许多读数压缩为一个中心位置，标准差则描述读数围绕这个中心的分散程度。这里的标准差是选定窗口内瞬时值的波动尺度，不能直接叫作平均值的误差。相邻温度记录可能相关，一百行数据中真正独立的信息少于一百次独立实验。第十五讲会把相关时间、分块与重复运行串起来处理这个问题；现在先把曲线、窗口和波动幅度同时保存，避免一个小数把它原本具有的时间结构全部遮住。

还有一种很有效的检查，是利用已经知道的代数关系核对不同列。总能量应等于动能加势能，只要三列采用相同的归一化和记录时刻。我们的程序计算每一行的差值，并报告最大的绝对差。文件输出有有限位数，读取后的微小差异可以来自十进制舍入；若差异达到能量本身的量级，就要检查列顺序、总量与每粒子量，或是否把不同时刻拼在了一起。这类检查直接针对数据含义，比单纯看到一张曲线没有报错更有判断力。

用能量加和检查列是否对应式 4

![用能量加和检查列是否对应](https://ml-biomat.com/static/agent-math/455d9e6f35cac1d609db80b5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| eⱼ, kⱼ, uⱼ | 第 j 行的每粒子总能量、动能、势能 | ε₁₁/粒子 |
| j | 记录编号 | 1 |
| δ_{E} | 所有记录中的最大能量加和残差 | ε₁₁/粒子 |
| \| · \| | 绝对值，只取偏差大小 | 1 |
| max | 在全部指定记录中选最大值 | 1 |
| =, −, × | 等号连接同一个物理量的两种表达；减号取差或给出负方向；相邻因子相乘。 | 运算符无量纲 |

怎样理解同一时刻且同一归一化下，总能量等于动能加势能。逐行相减再找最大偏差，可以发现列顺序、时间对齐或归一化问题。

算一个例子若一行 e = 0.750001、k = 1.25、u = −0.5，该行残差为 0.000001。最后比较全部行，取其中最大的绝对值。输出保留位数会影响这类很小的残差。

使用条件这是同一记录内的代数一致性检查，不是能量随时间的守恒误差；后者在第三讲用 NVE 对照分析。

图形中的连接线也包含一种读法：它连接已经保存的离散记录，不保证中间每一点都经过直接测量。对于热涨落，过度平滑容易把尖峰和相关结构抹去。这里用细线保留原始曲线，再用淡色背景区分阶段；如果另外画窗口平均，就清楚标出它覆盖的时间宽度。纵轴直接写物理量和约化单位，能量注明“每粒子”，比在图外写一段笼统说明更便于读者判断不同图之间是否可以比较。

保存数值时，还可以留意小数位数的作用。计算内部使用的浮点数通常比文本显示保留更多有效数字，写成文件后再读回，最后几位就可能发生舍入。对于展示温度趋势，适当的小数位数已经足够；对于比较重启后的坐标，我们会保存更多位数。增加显示精度不会提高积分算法本身的准确性，它只是减少记录时丢失的信息。文件中的有效数字、模型的数值误差和采样的不确定性因此是三件需要分别理解的事。

### 实际数值表生成的多面板记录图

由本页完整分析程序生成，保留三段环境、温度、每粒子能量和坐标定义。标准差描述窗口内读数波动。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s5)

由本页完整 Python 分析程序直接生成。所有面板来自同一次真实运行；阴影表示热浴阶段，坐标曲线追踪同一个编号的粒子。

## 从文件到图：一段完整而可检查的分析

下面的程序使用 Python 读取文本，用 NumPy 处理成列数值，再用 Matplotlib 绘图。可以先把它理解成三位分工明确的助手：Python 安排读取和判断顺序，NumPy 对整列数做同一种运算，Matplotlib 把数值映射成坐标和线条。程序中的变量名承担标签作用，例如 time 表示时间列、energy 表示能量列。方括号用于选择数组的一部分，布尔条件则生成哪些行被选中的标记。知道这些角色，就能沿着数据流读懂程序的大部分工作。

读 thermo.dat 时，程序跳过以井号开头的说明行，并检查每行是否具有预期列数。随后把时间、温度和三种能量分别取出，检查时间是否严格递增。一个重复或倒退的时间点，可能来自把两段重启记录拼接时保留了共同端点，也可能意味着计数曾经重设。程序把这种情况作为需要明确处理的输入条件，避免在尚未判断原因时便用排序隐藏它。对于本例的一次连续运行，时间应该按照设定的记录间隔向前推进。

读取轨迹时，程序逐帧处理，而不把整个文件当成一个长数组。它先读步号和盒子，再读该帧的属性标题，随后根据编号找到目标粒子，并取出 x 坐标和 x 方向映像编号。展开坐标由这两者与盒长共同计算。这个处理顺序与文件结构一一对应，因此当文件中途截断或缺少字段时，程序能够指向缺少的那一类信息。逐帧读取也节省内存：绘制一个粒子的路径，不需要把所有粒子的所有帧永久留在内存里。

### 完整的数值表与轨迹分析程序

```
"""Read the binary-particle tutorial outputs and reproduce the record plots.

Requires Python 3, NumPy and Matplotlib. All paths are relative by default.
Run: python analyze_records.py --data-dir . --out-dir analysis
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_selected_path(filename, particle_id, timestep=0.005):
    rows = []
    with Path(filename).open(encoding='utf-8') as stream:
        while True:
            first = stream.readline()
            if first == '':
                break
            if first.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a TIMESTEP frame header.')
            step = int(stream.readline())
            if stream.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Missing particle-count header.')
            count = int(stream.readline())
            box_header = stream.readline().split()
            if box_header[:3] != ['ITEM:', 'BOX', 'BOUNDS']:
                raise ValueError('Missing box-bounds header.')
            if any(name in box_header for name in ('xy', 'xz', 'yz', 'abc')):
                raise ValueError('This reader expects the fixed orthogonal tutorial box.')
            bounds = np.array([list(map(float, stream.readline().split()))
                               for _ in range(3)])
            if bounds.shape != (3, 2):
                raise ValueError('Expected three lower/upper box bounds.')
            names_line = stream.readline().split()
            if names_line[:2] != ['ITEM:', 'ATOMS']:
                raise ValueError('Missing particle-column header.')
            names = names_line[2:]
            required = ['id', 'x', 'ix']
            missing = [name for name in required if name not in names]
            if missing:
                raise ValueError('Required trajectory fields: ' + ', '.join(missing))
            columns = {name: names.index(name) for name in required}
            chosen = None
            ids = set()
            for _ in range(count):
                fields = stream.readline().split()
                if len(fields) != len(names):
                    raise ValueError('Incomplete particle record.')
                atom_id = int(fields[columns['id']])
                if atom_id in ids:
                    raise ValueError('Duplicate particle ID in one frame.')
                ids.add(atom_id)
                if atom_id == particle_id:
                    x = float(fields[columns['x']])
                    image = int(fields[columns['ix']])
                    length = bounds[0, 1] - bounds[0, 0]
                    chosen = (step * timestep, x, x + image * length)
            if chosen is None:
                raise ValueError(f'Particle {particle_id} absent from a frame.')
            rows.append(chosen)
    data = np.asarray(rows, dtype=float)
    if data.ndim != 2 or data.shape[1] != 3 or len(data) < 2:
        raise ValueError('At least two complete trajectory frames are required.')
    if not np.all(np.diff(data[:, 0]) > 0):
        raise ValueError('Trajectory times must increase strictly.')
    return data


def load_thermo(filename):
    table = np.loadtxt(filename, comments='#', ndmin=2)
    if table.shape[1] != 8 or len(table) < 2:
        raise ValueError('Expected eight columns: step,time,T,U/N,K/N,E/N,P,mass_density.')
    if not np.all(np.isfinite(table)) or not np.all(np.diff(table[:, 1]) > 0):
        raise ValueError('Thermodynamic data must be finite and strictly ordered in time.')
    return table


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('.'))
    parser.add_argument('--out-dir', type=Path, default=Path('analysis'))
    parser.add_argument('--particle', type=int, default=1)
    parser.add_argument('--window', type=float, nargs=2, default=[50.0, 100.0])
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    if args.window[0] >= args.window[1]:
        raise ValueError('The analysis window must have positive duration.')
    table = load_thermo(args.data_dir / 'thermo.dat')
    step, time, temperature, potential, kinetic, energy, pressure, density = table.T
    path = read_selected_path(args.data_dir / 'trajectory.lammpstrj', args.particle)
    selected = (time >= args.window[0]) & (time < args.window[1])
    if np.count_nonzero(selected) < 2:
        raise ValueError('The selected window needs at least two records.')
    residual = energy - kinetic - potential
    summary = {
        'thermodynamic_rows': int(len(table)),
        'trajectory_frames': int(len(path)),
        'particle_id': args.particle,
        'window_reduced_time_left_inclusive_right_exclusive': args.window,
        'window_records': int(np.count_nonzero(selected)),
        'mean_temperature_reduced': float(temperature[selected].mean()),
        'temperature_sample_standard_deviation_not_standard_error':
            float(temperature[selected].std(ddof=1)),
        'max_energy_sum_residual_per_particle': float(np.max(np.abs(residual))),
        'x_displacement_reduced': float(path[-1, 2] - path[0, 2]),
        'mean_mass_density_reduced': float(density.mean()),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'record-summary.json').write_text(
        json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out_dir / 'selected-particle-path.csv', path, delimiter=',',
               header='time_reduced,x_wrapped,x_unwrapped', comments='')
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else ['DejaVu Sans'], 'font.size': 14,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': '#173c42', 'text.color': '#173c42',
                         'xtick.color': '#50656a', 'ytick.color': '#50656a',
                         'svg.fonttype': 'path'})
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 10), sharex=True,
                             layout='constrained')
    fig.set_facecolor('#faf9f5')
    for ax in axes:
        ax.set_facecolor('#faf9f5')
        ax.axvspan(25, 100, color='#e4eeeb', zorder=0)
        ax.grid(axis='y', alpha=0.18)
        ax.set_xlim(0, 150)
    axes[0].plot(time, temperature, color='#177c83', linewidth=1.0)
    axes[0].hlines(1, 25, 100, color='#a76d45', linewidth=1, linestyle='--',
                    label='热浴目标：25 ≤ t < 100' if zh else 'Bath target: 25 ≤ t < 100')
    axes[0].set_ylabel(('温度 ' if zh else 'Temperature ') + r'$k_B T / \epsilon_{11}$')
    axes[0].legend(frameon=False, loc='best')
    for values, name, color in [(potential, '势能 U/N' if zh else 'Potential U/N', '#496fa8'),
                                (kinetic, '动能 K/N' if zh else 'Kinetic K/N', '#bd7548'),
                                (energy, '总能量 E/N' if zh else 'Total E/N', '#177c83')]:
        axes[1].plot(time, values, label=name, color=color, linewidth=1.1)
    axes[1].set_ylabel(('每粒子能量 / ' if zh else 'Energy per particle / ') + r'$\epsilon_{11}$')
    axes[1].legend(frameon=False, ncol=3, loc='best')
    axes[2].plot(path[:, 0], path[:, 1], color='#bb754a', linewidth=0.9,
                 alpha=0.75, label='显示坐标 x' if zh else 'Wrapped x')
    axes[2].plot(path[:, 0], path[:, 2], color='#177c83', linewidth=1.5,
                 label='展开坐标 x' if zh else 'Unwrapped x')
    axes[2].set_ylabel(('位置 / ' if zh else 'Position / ') + r'$\sigma_{11}$')
    axes[2].set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
    axes[2].legend(frameon=False, loc='lower center', bbox_to_anchor=(.5, 1.02), ncol=2, title=f'粒子编号 {args.particle}' if zh else f'Particle ID {args.particle}')
    fig.suptitle('同一次运动，不同记录\n两类 LJ 粒子 · NVE → Langevin 热浴 → NVE' if zh else
                 'One run, several records\nLJ binary particles · NVE → Langevin bath → NVE',
                 fontsize=17, x=0.07, ha='left')
    fig.savefig(args.out_dir / f'records-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'records-{args.language}.svg')
    # The first two panels reproduce the figure embedded in Lesson 1.
    axes[2].set_visible(False)
    axes[1].tick_params(labelbottom=True)
    axes[1].set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
    axes[0].set_position([0.11, 0.55, 0.86, 0.31])
    axes[1].set_position([0.11, 0.13, 0.86, 0.33])
    fig.set_layout_engine(None)
    fig.set_size_inches(11.5, 8.0)
    fig.suptitle('温度与能量如何随阶段改变' if zh else 'Temperature and energy across the run stages',
                 fontsize=17, x=0.11, y=0.96, ha='left')
    fig.savefig(args.out_dir / f'energy-temperature-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'energy-temperature-{args.language}.svg')
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
```

读取实际 thermo.dat 和 trajectory.lammpstrj，按粒子编号重建展开坐标，保存 PNG/SVG 图、CSV 路径和 JSON 数值汇总。

运行分析后，会得到一张多面板图和一份简短的数值汇总。图的上部把温度和能量与分段时间联系起来，下部对照同一粒子的显示坐标与展开坐标。汇总中记录读到多少行、多少帧、选择哪个粒子和平均窗口，以及能量列相加后的最大差异。这样的数值不是为图添加装饰，而是回答“这张图究竟用了什么”的问题。改变粒子编号或时间窗口后重新运行，可以直接观察测量定义怎样改变呈现结果。

### 在例题目录运行分析

```
python analyze_records.py --data-dir . --out-dir analysis --particle 1 --window 50 100 --language zh
python analyze_records.py --data-dir . --out-dir analysis --particle 1 --window 50 100 --language en
```

目录中需有已运行的两个输出文件以及上述程序。窗口左端包含、右端不包含。程序需要 NumPy 和 Matplotlib。

程序保存 PNG 便于直接查看，也保存 SVG 便于放大阅读坐标和文字。SVG 中的曲线来自同一批实际数值，不是另外手工描出的趋势线。每次修改分析规则，都应让图和汇总一起更新。若只在图片编辑器里改一个图例或移除一个点，却没有同步计算脚本，就会使呈现与数据处理分开。对于以后比较不同交联密度或不同溶液浓度的研究，保持这条对应关系能够显著减少结果整理时的混淆。

读者还可以用已知的简单关系检查程序。选一个不跨边界的短区间，两种 x 坐标的变化应该一致；在发生跨界的位置，展开坐标与显示坐标相差整数倍盒长；把能量三列按行相加应回到总能量。这里检查的是能够解释的物理和文件关系，而不是要求记住某台电脑的一段屏幕文字。程序遇到真实数据后是否满足这些关系，构成了分析可信度的一部分；采样是否充分则是下一层问题，需要更长观察和合适的统计设计。

## 保存状态之后，怎样把计算接下去

长时间模拟经常需要分段执行。可能是先让体系接触热浴，再研究孤立演化；也可能是一次运行到达预定时长后，发现某个慢过程值得继续观察。重启文件相当于在合适位置保存一个计算状态，让下一次运行继承粒子位置、速度、盒子与相应模型设置。它比末态图片包含更多信息，也比只写坐标的文件更适合继续同一段动力学。当前例题在移除热浴后写出 equilibrated.restart，我们使用它建立一个确定性 NVE 续算。

二进制重启文件适合由兼容的同一 LAMMPS 可执行程序读取，因为其中存储方式会受到软件版本、编译和平台的影响。文本 data 文件则较容易阅读和转换，但重新开始计算时需要明确恢复没有写入其中的设置。两种格式各有用途：重启文件方便连续计算，结构数据和输入脚本方便长期解释模型。保存模型时把这些角色配合起来，比只保留一个看不见内容的二进制文件更有利于以后检查参数、迁移版本或重新组织计算。

读取重启状态以后，还要重新声明接下来需要的积分、计算和输出命令。重启文件并不是把整份输入脚本自动重新执行一遍。下面的续算输入重新指定 NVE 积分器、数值记录和轨迹，并保持与上一段相同的时间步。它不再调用 velocity create，因为这会重新生成速度，改变原本要继续的状态。若研究问题恰好需要重新赋予温度或改变速度，可以这样做，但那已经是一个明确改变初始条件的新分支。

### 保存、清空并读回中间状态的分段计算

```
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 100
write_restart middle.restart
clear
units lj
read_restart middle.restart
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 100
write_dump all custom restart-split.lammpstrj id type x y z vx vy vz modify sort id format float %.17g
```

读取热浴结束状态，推进 100 步，保存并清空体系，读回后再推进 100 步；总时长为 1 个约化时间单位。

### 保持计算状态连续推进的对照

```
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 200
write_dump all custom restart-continuous.lammpstrj id type x y z vx vy vz modify sort id format float %.17g
```

从相同起点直接推进 200 步，比较末态中相同编号粒子的坐标与速度。末态以 17 位有效数字保存。

### 运行两种续算

```
lmp -in restart-continuous.lmp
lmp -in restart-split.lmp
```

两个输入与 equilibrated.restart 位于同一练习目录。它们产生各自的末态，比较前按粒子编号对齐。

检验续算时，可以从同一个保存点出发做一个小比较：一条路径保持状态连续推进，另一条路径在中间保存状态、清空体系，再读回后继续，随后比较相同步号的坐标、速度和能量。在相同可执行程序、处理器配置和确定性设置下，这能够检查状态是否正确接回。若改变处理器数量或其他影响浮点求和次序的设置，微小舍入差异可能逐步扩大；这时还应比较能量行为与统计量，而不是把长时间后的坐标差异直接解释成模型发生变化。

### 按粒子ID比较两条续算分支的末态

```
#!/usr/bin/env python3
"""Compare the saved final states of a continuous and split NVE run.

python compare_restart.py restart-continuous.lammpstrj restart-split.lammpstrj
Requires NumPy. Atom IDs identify corresponding particles; row order may differ.
"""
from pathlib import Path
import argparse
import numpy as np


def final_frame(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    frames = []
    i = 0
    while i < len(lines):
        if lines[i] != "ITEM: TIMESTEP":
            raise ValueError("Expected a LAMMPS timestep header.")
        step = int(lines[i + 1])
        if lines[i + 2] != "ITEM: NUMBER OF ATOMS":
            raise ValueError("Expected an atom-count header.")
        count = int(lines[i + 3])
        if not lines[i + 4].startswith("ITEM: BOX BOUNDS"):
            raise ValueError("Expected box bounds.")
        bounds = np.asarray([[float(x) for x in line.split()]
                             for line in lines[i + 5:i + 8]])
        fields = lines[i + 8].split()[2:]
        if not lines[i + 8].startswith("ITEM: ATOMS "):
            raise ValueError("Expected atomic field names.")
        required = ["id", "type", "x", "y", "z", "vx", "vy", "vz"]
        if not all(name in fields for name in required):
            raise ValueError("Missing an identity, position, or velocity field.")
        rows = np.asarray([[float(x) for x in line.split()]
                           for line in lines[i + 9:i + 9 + count]])
        if rows.shape != (count, len(fields)) or not np.all(np.isfinite(rows)):
            raise ValueError("Incomplete or nonfinite atomic records.")
        selected = rows[:, [fields.index(name) for name in required]]
        selected = selected[np.argsort(selected[:, 0])]
        if len(np.unique(selected[:, 0])) != count:
            raise ValueError("Duplicate atom IDs.")
        frames.append((step, bounds, selected))
        i += 9 + count
    if not frames:
        raise ValueError("No frames found.")
    return frames[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("continuous", type=Path)
    parser.add_argument("split", type=Path)
    args = parser.parse_args()
    step_a, box_a, a = final_frame(args.continuous)
    step_b, box_b, b = final_frame(args.split)
    if step_a != step_b or a.shape != b.shape:
        raise ValueError("Final step or particle count differs.")
    if not np.array_equal(a[:, :2], b[:, :2]):
        raise ValueError("The atom IDs or their types differ.")
    if not np.array_equal(box_a, box_b):
        raise ValueError("The box bounds differ; inspect coordinate representations.")
    position = float(np.max(np.abs(a[:, 2:5] - b[:, 2:5])))
    velocity = float(np.max(np.abs(a[:, 5:8] - b[:, 5:8])))
    print(f"particles = {len(a)}; final step = {step_a}")
    print(f"maximum absolute saved coordinate difference = {position:.17g} [sigma_11]")
    print(f"maximum absolute saved velocity difference = {velocity:.17g} [sigma_11/tau]")


if __name__ == "__main__":
    main()
```

在包含两份末态轨迹的目录运行脚本开头的命令。它按字段名读坐标与速度，再按ID配对，分别报告所有分量中的最大绝对差，单位为约化长度与约化速度。

### 连续推进与保存后读回的比较

同一起点、同一确定性 NVE 模型、0.005 时间步，总计 200 步；比较按编号对齐的末态坐标和速度。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/#zh-s7)

同一状态连续运行 200 步，与运行 100 步、写入并读取二进制重启文件、再运行 100 步比较。位置差采用最小镜像距离；速度差为三维差向量的长度。

Langevin 热浴还包含另一层情况：随机力随时间取样，重启后的随机数历史不一定与未中断的一次运行逐步相同。用相同种子重新建立命令，也不等于恢复已经走到中途的随机数生成器状态。因而，本讲选择移除热浴后的 NVE 段做严格续算比较；涉及随机热浴的续算，则在正确继承物理状态之后，再检查温度分布、能量统计和其他目标量。明确比较规则来自哪一种动力学，比笼统地要求所有重启都逐位相同更有用。

文件名中的 equilibrated 只是一个方便辨认的名字，平衡是否充分仍要从观察量判断。某个状态已经完成预定热浴运行，表示它经历了那段处理；是否足以让慢结构松弛，需要比较结构和能量在后续区间的变化。这里保留文件名以便串起例题，把其含义准确理解为热浴阶段结束时保存的状态。以后研究长链或网络时，给文件起名与确认结构已经充分松弛之间的区别，会变得尤其重要。

## 让文件组织服务于一个明确的比较

当第一次分析完成后，可以做一个非常具体的练习：只改变轨迹保存间隔，保持粒子、力场、时间步和积分条件一致，再比较文件大小和路径细节。更稀的记录通常保留较少的瞬间，但没有改变积分器实际推进的步数。把这项练习与改变时间步的练习并排看，就能分清“计算怎样近似运动”和“我们保存了多少运动信息”。第三讲会进一步用数值结果检查时间步，而这里先从数据记录的角度把两件事区分开。

每个比较条件使用一个独立目录，里面保存对应输入和输出，可以减少覆盖和错配。目录名可以描述真正改变的条件，例如温度或时间步；一份简洁的参数记录再说明版本、随机种子、粒子数、单位、运行阶段和分析窗口。名字帮助人找到文件，内容则决定文件究竟描述什么。只依赖“最终版”或“第二次”这样的命名，很容易在新增比较后失去意义。把实验条件作为组织中心，能够让之后的多条链、多种交联程度保持清楚。

还可以为关键文件计算哈希值，把它理解为依据文件内容生成的指纹。内容改动后，指纹通常随之改变，适合检查分析时用的输入和后来保存的输入是否还是同一份。哈希不会告诉我们物理模型是否正确，也不会替代读懂参数，但能回答“这两份文件的字节是否一致”这种明确问题。数据分析中的许多可靠习惯就是这样组成的：每个检查只回答自己能够回答的问题，合起来保证模型、计算和呈现之间的联系。

如果某张图出现不合理跳变，沿着数据流回查通常最有效。先看是显示坐标还是展开坐标，再检查粒子编号、帧时间和盒长；若能量大小差了一千多倍，则优先检查是否混用了总能量与每粒子能量；若重启后温度突然变化，查看是否重新赋过速度或改变了温度定义。这样的排查把图形现象与产生它的具体字段联系起来。修正之后重新生成整张图，能够让解释也跟着真正的数据处理改变。

到这里，一次模拟已经不只是运行命令后得到的动画，而是一条可解释的链路：输入决定模型与过程，计算产生状态记录，分析把记录变成定义明确的观察量，图形再帮助我们比较它们。下一讲将沿着这条链路往计算内部再走一步，看看势能怎样产生作用力、积分器怎样更新坐标，以及时间步为什么会影响能量轨迹。文件仍然是这些推理的载体；读懂它们之后，数值误差就可以通过实际对照研究，而不只是凭动画是否流畅来判断。

## 延伸阅读与开放资料

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  原例的命令顺序、监测、轨迹与续算流程。

  增加单位与文件解释、映像编号、独立分析程序和确定性续算比较。
- [LAMMPS stable manual: dump](https://docs.lammps.org/stable/dump.html) · LAMMPS developers · Official documentation consulted; software source GPL-2.0; no copied figures

  坐标字段、映像编号与粒子身份。

  原创坐标图解与分析程序。
- [LAMMPS stable manual: read_restart](https://docs.lammps.org/stable/read_restart.html) · LAMMPS developers · Official documentation consulted; no copied figures

  保存字段、需要重新声明的设置和随机热浴重启性质。

  围绕同一粒子体系重新组织完整比较。
- [Correlations in the Motion of Atoms in Liquid Argon](https://doi.org/10.1103/PhysRev.136.A405) · A. Rahman (1964) · Cited paper; no article text or images reproduced

  从轨迹到相关和扩散测量的科学史。

  原创概念图，不使用论文数据重绘。
