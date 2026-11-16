# 从文件到轨迹：准备一次分子模拟

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g02/
Language: zh-CN

打开水盒的坐标、拓扑与参数，理解它们如何组成一次运行，再用完整程序核对分子身份、位点数量和盒子几何。

## 让一份计算在另一台电脑上仍然说得清楚

做一杯咖啡时，水量、咖啡粉用量、水温和冲泡时间都会影响结果。如果只留下成品照片，下一次很难重现相同味道；如果把每一项条件记下来，就能有目的地调整其中一项。分子模拟也需要这样的准备。一个漂亮的水盒动画没有直接告诉我们用了哪种水模型、盒子有多大、原子受到什么作用，或者画面之间隔了多少物理时间。这些信息分别保存在不同文件里，理解文件的分工，就是理解一次计算怎样被定义。

本讲继续使用上一讲的 SPC/E 水盒，先不急着解释所有受力公式，而是沿着“输入怎样变成轨迹”的顺序打开文件。读完以后，你应能看出坐标、拓扑和运行参数各自负责什么，能检查水分子数量与原子数量是否对应，也能知道哪一种输出用于继续运行、哪一种用于看运动、哪一种用于画温度或密度曲线。这些能力会让后面的蛋白质和聚合物例题更容易理解，因为复杂体系仍然使用相同的信息分工。

这里的文件名有一个共同特点：名字的前半部分说明阶段，点号后面的扩展名说明常见格式。例如 npt.gro 表示 NPT 阶段输出的一份坐标，npt.edr 保存这一阶段的能量与热力学记录。扩展名是一种约定，真正决定内容的仍是文件本身。把一张照片改名为表格，不会让它变成可计算的数字；同样，把一个旧输入改成新名字，也不会自动改变其中的温度或分子模型。清楚的命名帮助阅读，内容检查保证含义准确。

这次计算使用 GROMACS 2026.4。版本号的用途不是让人记住软件更新史，而是把例题中的命令行为、默认值和输入格式固定下来。运行环境还会影响实际速度、可用的计算设备与数值细节，因此例题会保留引擎版本和运行条件。读者在自己的电脑执行时，先查看版本输出，再按对应文档理解参数。不同机器上的轨迹可能逐渐走向不同的微观路径，我们要比较的是相同模型与协议下的统计行为，同时保留足够的信息追查差异。

以下命令使用 Bash 形式的终端语法，可在 Linux、macOS 的合适环境，或 Windows 的本地 Linux 环境中执行。终端本身是一个文字界面，负责把指令交给程序；GROMACS 才负责分子计算。我们先学习少量会反复用到的写法，随后每个命令都连接到一个明确的文件变化。这样，命令不再是一串必须原样背下来的符号，而是一段能解释输入、动作和输出的操作说明。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/#zh-s1)

图 1 · 三个输入分别描述几何、模型和观察方式，经 grompp 装配后成为 TPR。图示中的箭头表示信息传递，不是物理时间。

## 科学为什么需要可以交换的原子坐标

生物分子的三维形状来自实验信息与结构模型之间的联系。研究者通过衍射、核磁共振、冷冻电镜等方法获得不同类型的数据，再建立能够解释这些数据的原子模型。模型可以画成漂亮的蛋白质图，也可以保存成逐个原子的坐标。图片帮助人理解整体形状，坐标则让其他研究者重新计算距离、比较结构、检查局部环境，并把同一结构用于新的问题。两种表达承担不同任务，能够交换的数字记录使这些任务接在一起。

1971 年，Protein Data Bank，即蛋白质结构数据库 PDB，建立时收录了七个结构。这个历史起点说明，结构共享从一开始就不只是“给别人看一幅图”。保存原子位置及相关信息，使同一份结构能够被不同实验室阅读、分析和重新使用。之后结构数量与复杂程度不断增长，文件格式和数据规范也随之发展。我们今天下载一个结构并立即在电脑中显示，依赖的正是这种长期积累的公共数据约定。[PDB 的历史](https://www.rcsb.org/pages/about-us/history)

可以把坐标记录理解为一份空间地址簿。每一行说明一个原子的身份以及它在某个坐标系中的位置。地址簿里的数字通常不依赖我们把分子朝哪个方向摆在屏幕上：整体旋转会改变坐标值，却不会改变分子内部原子间的距离。显示软件可以任意旋转观察方向，研究者则需要决定哪些量对整体平移、转动不敏感。这个区别会在蛋白质结构比较时变得重要，也解释了为什么“看起来朝向不同”不等于“分子构象已经改变”。

不过，一份实验结构还没有包含一次分子模拟需要的所有条件。部分氢原子可能没有在实验模型中明确给出，溶液中的质子化状态需要结合环境判断，缺失片段与结晶水的处理也会影响体系。第五讲会专门讨论这些选择。本讲的纯水例子避开了大分子结构准备的复杂性，让我们先把文件之间的关系学清楚：坐标提供起始几何，力场赋予相互作用，运行参数规定这次怎样推进和观察。

这种分工也让改动更容易解释。如果只想把观察时间从一百皮秒延长到两百皮秒，通常关注的是运行参数与续算状态；如果换一种水模型，就需要检查相互作用位点、拓扑与参数的配合；如果加入一个蛋白质，坐标和分子清单都需要改变。每一种科学操作都有对应的信息位置。文件格式看起来像技术细节，却承载着这些操作到底改变了哪一部分物理模型。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/#zh-s2)

图 2 · 1971年PDB开始共享七份结构，坐标记录使结构可以被重新分析。分子模拟还需加入相互作用模型与运行条件。图中圆点代表结构记录。

## 读懂一行坐标：身份、位置与长度单位

本例的 water.gro 是一份文本坐标文件。第一行给出说明，第二行给出原子总数，接下来每一行描述一个原子，最后一行给出盒子信息。对标准精度的 GRO 文件，原子行采用固定宽度：残基编号、残基名称、原子名称、原子编号与三个坐标分别占据约定位置。固定宽度意味着某些字段可能紧挨着，不能总是把“空格隔开的词”当成完整字段。读取程序需要尊重这个约定，才能区分名字与数字。

“残基”一词在蛋白质里通常指一段氨基酸单位；在水盒文件里，每个水分子也用一个残基记录来组织三个原子。SOL 是本例的水残基名，OW、HW1、HW2 分别标记氧与两个氢。编号帮助我们定位某一行，名称帮助我们理解它是什么。用于相互作用计算的原子类型则属于拓扑信息，与显示名称是两类概念。一个叫 OW 的原子不会仅凭名字自动获得正确电荷，因此坐标和拓扑还必须按照相同顺序对应。

三个坐标通常写作 x、y、z，可以理解为从选定原点沿三个互相垂直方向走多远。若一行中的位置是 0.500、1.000、1.500，它表示在 GRO 的纳米单位下，该原子分别位于三个方向的这些位置。负坐标或大于盒子边长的坐标也不一定代表错误，因为周期体系可以使用不同的等价位置表示。判断几何时，需要结合盒矢量和周期规则，而不是只要求所有数字落在一个看起来整齐的区间。

长度单位尤其值得在第一次读文件时讲清楚。GRO 坐标使用纳米，传统 PDB 坐标使用埃，符号为 Å；1 nm 等于 10 Å。把一个在 PDB 中长 30 Å 的结构直接按 30 nm 解释，就会让长度放大十倍，体积放大一千倍。许多程序在正规格式转换时会自动处理单位，因此正确做法是使用理解格式的转换工具，并检查转换后的尺寸，而不是手动把所有数字乘一遍又交给会再次换算的程序。

同一段长度的两种单位式 1

![同一段长度的两种单位](https://ml-biomat.com/static/agent-math/553e7ab04459713db651b865.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| nm | 纳米，十亿分之一米 | 长度单位 |
| Å | 埃，百亿分之一米 | 长度单位 |
| 1, 10, = | 数字表示单位的份数；等号表示两侧是同一物理长度 | 数字与等号无单位 |

怎样理解一个纳米包含十个埃。改变长度单位会改变数值，所描述的实际距离保持不变。

算一个例子盒边长 3 nm 等于 30 Å；位置坐标 0.500 nm 等于 5.00 Å。体积为 27 nm³ 时，对应 27,000 Å³，因为三条边都要换算。

使用条件本例标准 GRO 长度采用 nm，传统 PDB 长度采用 Å；格式转换应遵循对应规范，避免重复换算。

下方交互用一个原子的示意位置展示这种换算。切换单位时，原子的实际位置保持不变，改变的是描述它的数字与单位；移动滑块时，才真正改变位置。这个区别像用厘米和米描述同一张桌子的长度：180 cm 与 1.8 m 表示同一个对象。对分子坐标也应采用这种思路，把数值和单位一起读取，避免把一个单独的数字当成完整的物理信息。

移动粒子会改变位置；切换单位只改变表达同一位置的数字。

[Figure: 同一个位置的纳米与埃表示](https://ml-biomat.com/tutorials/molecular-dynamics/g02/#zh-s3)

单位换算示意：改变显示单位，粒子的实际位置保持不变。

最后一行的盒子信息也不只是一个装饰性的边框。对于本例的正交立方盒子，三项长度就能描述盒子；更一般的晶胞需要三个盒矢量，它们可以带有非对角分量。盒子决定周期映像之间怎样排列，因此影响邻居搜索、最短距离和密度计算。我们会在检查脚本中把盒子记录转换为一个三乘三矩阵，再由它计算体积。本例得到的体积可以与三个边长相乘核对，未来遇到斜盒子时仍能保留相同的处理思路。

文本中保留的小数位数也有物理含义。若坐标写到小数点后三位纳米，最后一位对应 0.001 nm，也就是 0.01 Å。写入时的舍入会让坐标与内部计算值有微小差别，因此一份便于阅读的末态坐标并不自动等于完整精度的运行状态。需要精确继续运行时使用检查点，需要观察结构时可以使用相应精度的坐标。输出格式的选择，应当跟随下一步想做的事情，而不只是看哪个文件更小。

## 拓扑把坐标上的名字变成一个物理模型

打开 topol.top，会看到几行包含文件的指令，以及 system 和 molecules 两个区块。井号开头的 include 指令把其他文件中的定义接进来，好比一本操作手册先声明需要使用哪一套材料规格，再列出这次装配的部件。这里先包含 oplsaa.ff 中的 forcefield.itp，建立相互作用参数的组织框架；再包含 spce.itp，定义所用的 SPC/E 水分子。水模型的性质来自这一套配合后的定义，不能只看最外层文件名就判断全部相互作用。

system 区块是给人阅读的体系名称，molecules 区块则列出软件要建立哪些分子类型以及各有多少个。本例只有 SOL，因此清单很短。构建水盒之前，这一清单还没有水的数量；gmx solvate 添加水分子后，会更新相应计数。拓扑里的数量必须与坐标中的分子排列一致。若坐标里已经有许多水，而清单仍然为空，预处理就没有足够的信息把这些坐标赋予对应的分子定义。

### 构建前的水盒拓扑模板

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

在 gmx solvate 添加水后，molecules 区块得到实际 SOL 数量。包含的力场文件随指定 GROMACS 安装提供，水模型由 spce.itp 定义。

在 SPC/E 的分子定义里，每个水分子按氧、氢、氢的顺序列出三个位点，并给出相应的原子类型与部分电荷。刚性几何通过约束定义保持，非键相互作用则使用相应参数。这里最容易理解的一项一致性检查，就是每个水分子应对应三行坐标。它不能替代完整的化学检查，却能够快速发现漏掉原子、重复水分子或分子清单没有更新等常见问题。对更复杂的体系，同样思路会扩展为逐种分子的位点数与数量相加。

三位点纯水的数量关系式 2

![三位点纯水的数量关系](https://ml-biomat.com/static/agent-math/2d92f9d8f093d6e9ab198232.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Nsite | 坐标文件中的相互作用位点数；本例各位点对应一个原子 | 计数，无量纲 |
| Nwater | 拓扑 molecules 区块中的 SOL 水分子数 | 计数，无量纲 |
| 3 | 每个 SPC/E 分子的位点数：一个氧和两个氢 | 无量纲 |
| =, × | 等号要求数量相符；相邻符号表示位点数乘以分子数 | 运算符无单位 |

怎样理解每个完整水分子贡献相同的三个位点，重复列出 Nwater 次便得到总位点数。

算一个例子一个指定含 900 个 SPC/E 水分子的算例需要 2700 个坐标位点。实际例题使用建盒输出的分子数，检查程序直接读取它，不把 900 写成真实运行数量。

使用条件适用于本例纯三位点水。混合物需逐类求和；四位点水含虚拟位点时，要区分原子数与相互作用位点数。

相同总数也可能隐藏不同错误。假设把两个相邻水分子的某个氢坐标交换，原子总数没有改变，分子内部几何却可能变得不合理；如果把原子顺序打乱，总数仍然正确，拓扑给出的身份与坐标也可能错位。因此，数量检查以后还要核对名称顺序、局部几何及实际展开的拓扑。我们把这些检查看作互相补充的观察：计数回答“有多少”，顺序回答“对应谁”，几何回答“放在哪里”。

电荷还能提供另一个容易理解的核对。SPC/E 的氧电荷为 −0.8476 e，每个氢为 +0.4238 e，其中 e 是元电荷；一个水分子的三项相加为零，任何整数个这样的水分子仍然电中性。这里的零说明总电荷，并没有抹掉分子内部正负电荷分离带来的作用。以后加入离子时，总电荷检查会帮助确认组成是否符合设计，盐浓度则还需要结合离子数量与溶液体积计算。

选择力场还涉及参数之间的相容性。不同体系可能使用不同的电荷、非键组合规则、水模型或特定修正，把文件复制到同一目录不会让它们自动形成一致的模型。当前纯水例子直接使用安装中配套的 SPC/E 定义，关系比较清楚。后面加入蛋白质、小分子或糖时，会逐项说明为什么选择某套参数，以及水与溶质怎样配合。先学会从 include 关系追踪定义，才能在复杂例子中找到真正决定物理行为的地方。

实际展开的拓扑可以用 grompp 的 -pp 选项保存。它把包含关系和条件选择处理之后的内容写出来，帮助我们确认程序最终使用了什么。原始 topol.top 简短易读，展开文件更接近程序接收到的定义，两者各有用途。平时修改应针对有明确来源的输入文件，再重新预处理；如果只改已经生成的展开文件，却仍让程序读取原来的输入，计算就不会按照期待改变。

## 参数文件描述一次观察怎样进行

MDP 文件保存运行参数。它通常由“名称 = 取值”的行组成，分号后面可以写注释。名称告诉程序需要设置哪一项，取值规定本次选择。对于动力学阶段，integrator 决定运动推进算法，dt 给出时间步，nsteps 给出推进步数。其他参数描述邻居搜索、相互作用处理、温控压控与输出频率。第一次看到这些名字时，不必把所有选项同时背下来；先按它们在一次观察中承担的任务分组，会容易得多。

本例的准备阶段有不同目标。em.mdp 使用能量最小化，关注如何解除初始接触中的较大作用力；nvt.mdp 让盒子在固定体积下适应目标温度；npt.mdp 再允许体积随压力控制变化。最后的两个 NVE 输入使用相同初态与物理时长，分别采用 1 fs 和 2 fs 时间步，用来比较数值积分行为。文件分开保存，使每个阶段的条件可读，也使我们能够在进入下一阶段之前检查当前状态。

下面完整列出本讲准备命令使用的 em.mdp。define 中的 FLEXIBLE 选择配套水拓扑的柔性键角分支，让初始几何先松弛；真正进入 NVT、NPT 与 NVE 动力学时恢复刚性水。最小化的 nsteps 是允许的最大更新次数，满足力阈值时可以提前停止，不应把它乘以动力学步长解释成一段真实运动时间。这里先认识文件中每类信息的位置，下一讲会逐项解释力阈值、步长和收敛曲线。

### 完整最小化输入 em.mdp

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

初始最小化启用随水拓扑提供的柔性键角分支，随后动力学恢复刚性水。最大更新次数为10000，力阈值为100 kJ·mol⁻¹·nm⁻¹，最小化步长参数为0.001 nm；实际停止点由运行结果确定。

输出频率是观察设计的一部分。每一步都计算运动，不表示每一步都把位置、能量和日志写到磁盘。nstxout-compressed 控制压缩坐标轨迹的保存间隔，nstenergy 控制能量文件中的记录间隔，nstlog 控制运行日志中详细记录的频率。若一个文件每隔 1 ps 保存一帧，另一个每隔 0.2 ps 保存一行，它们的行号就不能直接当成相同时间。把数据放在一起比较时，应使用各自记录的物理时间进行对应。

初始速度的处理也会改变模拟含义。第一次开始动力学时，可以根据目标温度生成一组速度；继续已经平衡的运动时，则希望保留前一阶段的状态。固定随机种子可以记录生成规则的一次具体选择，方便复现与比较，但它不是“消除涨落”的开关。不同种子代表不同的初始运动或随机控制序列，独立重复正可以利用这种差别来评估统计行为。后续章节会把种子、重复与误差联系起来，本讲先注意哪些阶段在生成状态，哪些阶段在延续状态。

数值相同的参数也可能具有不同单位。dt 的 0.002 表示皮秒，某个输出间隔的 500 表示步数，ref-t 的 300 表示开尔文。温控的耦合时间又是一种物理时间，它描述控制算法的特征尺度，不等于总运行时长。把每项设置读成“名字、数值、单位、作用”四个部分，能够避免把参数表当作没有物理含义的数字清单，也能看出改变一个数以后，真正改变的是时间分辨率、观察频率还是环境耦合。

程序会为许多没有显式写出的选项采用默认值。默认值能让输入保持简短，却不应让我们忘记最终条件。grompp 的 -po 选项保存处理后的参数文件，其中可以查看程序实际采用的设置。于是，一个可读的原始 MDP 与一份处理后的 MDP 形成互补：前者表达作者主动选择了什么，后者帮助确认程序实际解释成什么。这种区分在更新软件版本、比较两次计算或排查结果变化时很实用。

参数文件也需要保持物理上的相互配合。例如，截断距离与盒子尺寸有关，时间步与最快的运动及约束有关，温控算法与所采样的统计条件有关。把一个在蛋白质例子里运行成功的 MDP 直接用于膜或粗粒化聚合物，未必保持相同含义。我们会在每个新体系中解释哪些设置延续了共同原则，哪些需要针对模型重新选择。当前这组水文件首先承担一个清楚的任务：为后续实际运行提供一致、可检查的初始条件。

## 预处理、运行与续算，三个动作怎样接起来

gmx grompp 是把输入装配为一次运行的步骤。它读取坐标、拓扑和参数，解析包含文件，将每一种分子定义复制成所需数量，并检查多项一致性，最后生成 tpr 文件。这个文件包含运行所需的结构与模型信息，供 mdrun 读取。可以把 grompp 理解为准备出发前核对行程、乘客与车辆，而 mdrun 才真正让运动按时间推进。预处理成功说明输入通过了相应技术检查，物理设置是否回答研究问题，还要结合前面所做的模型选择。

### 从模板建盒、预处理并最小化

```
#!/usr/bin/env bash
set -euo pipefail
# Run inside the water example directory with its supplied input files.
gmx --version
cp topol.template.top topol.top
gmx solvate -cs spc216.gro -box 3 3 3 -o water.gro -p topol.top
gmx grompp -f em.mdp -c water.gro -p topol.top \
  -o em.tpr -pp em.top -po em.processed.mdp
gmx mdrun -deffnm em -ntmpi 1 -ntomp 4 -pin off
```

在装有本页拓扑模板和 em.mdp 的例题目录中执行。set -euo pipefail 使脚本遇到未定义变量或失败命令时停止，避免把不完整前置结果继续传给后续命令；本机运行使用4个CPU线程。

这段命令明确列出每个输入与输出。-f 指向运行参数，-c 指向坐标，-p 指向拓扑，-o 指定生成的 tpr 名称；-pp 和 -po 分别保存展开拓扑与处理后的参数。后面的 mdrun 使用 -deffnm em，把这一阶段的文件放在共同的 em 前缀下。前缀不影响分子运动，却让 em.gro、em.edr、em.log 等结果容易彼此对应。文件名与阶段一致，读者就能沿着计算路径找到需要的信息。

命令查找文件时会从当前工作目录出发。写 water.gro 表示当前目录中的同名文件，写 input/water.gro 表示其下 input 文件夹中的文件。例题采用相对位置，让整套文件移动到另一台电脑后仍保持关系。命令中的反斜杠如果放在行尾，表示同一条 Bash 指令接着下一行写；复制时要连同后续行一起执行。程序在终端打印的信息与写入磁盘的结果各有用途，看到进度文字并不等于需要的输出已经完整保存。

运行结束后，GRO 保存某个时刻的坐标，并可能包含速度；XTC 保存按时间排列的压缩坐标；EDR 保存能量与热力学记录；LOG 记录程序设置、进度与诊断。CPT 检查点保存更完整的运行状态，包括继续某些算法所需要的内部变量。因此，保存一张最终坐标与保存可续算的完整状态，是两个不同的任务。若只保留坐标而重新生成速度，虽然可以启动新的计算，所得运动已经不再是原来那段轨迹的直接延续。

阶段之间的衔接通常同时给出坐标和检查点，例如用前一阶段的 nvt.gro 与 nvt.cpt 准备 NPT。坐标便于明确结构输入，检查点帮助传递状态；是否生成新速度、是否延续约束和相应参数仍要按协议设置。对已经中断、需要继续同一阶段的运行，还可以使用 mdrun 的检查点续算选项。两种情况的意图不同：一类是进入条件改变的新阶段，另一类是在相同运行设置下接着完成未结束的时间段。

警告信息应放回具体的输入关系中理解。如果软件发现坐标数量与拓扑数量不一致，继续运行不会自动补齐科学模型；如果某个选项已经不适用于当前版本，应先找到对应设置并改正。我们不把忽略警告当成通用操作，也不把每条提示都当成同一种故障。日志提供了具体对象、参数和发生位置，从那里回到输入文件，通常比反复换命令更有效。后面每个实例都会把检查与物理问题连接起来，帮助判断应修改哪一项。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/#zh-s6)

图 3 · 同一运行产生的文件保留不同信息。XTC不包含完整续算状态，GRO的文本精度也与检查点保存状态不同。

## 用一段完整程序检查水盒的身份与几何

现在把前面的阅读方法写成一个可以重复执行的检查。程序输入 water.gro 和 topol.top，先读取坐标文件声明的原子数，再核对实际数据行；接着从 molecules 区块读取 SOL 数量，检查三位点水应有的总位点数；最后逐个水分子核对原子名称顺序，并计算盒子体积。每一项都有明确目的：避免把错误的文件组合送入后续计算，也让原本藏在文本里的体系信息成为可见的图表。

这里的读取器针对本例采用的标准三位小数 GRO 坐标和纯水拓扑。它按固定列位置取出名称与坐标，因此比直接按空格拆分更符合这种格式。GRO 可以使用其他精度，复杂体系也可以在拓扑中采用更丰富的组织方式；处理这些文件时，应使用支持对应格式的库或扩展读取规则。我们把本例的适用对象写在程序开头，读者就能清楚判断什么时候可以直接复用，什么时候需要先调整输入解析。

### 完整 Python：坐标、拓扑与几何核对

```
#!/usr/bin/env python3
"""Inspect this example's standard-precision GRO and pure-SOL topology.

Usage: python inspect_water.py water.gro topol.top --output inspection --language en
Dependencies: numpy, matplotlib. Input files are never modified.
The reader targets GRO coordinate fields with three decimal places (width 8).
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_gro(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 3:
        raise ValueError("Incomplete GRO file.")
    n_atoms = int(lines[1].strip())
    if n_atoms < 3 or len(lines) != n_atoms + 3:
        raise ValueError("Declared atom count does not match coordinate lines.")
    coordinates, names, residues = [], [], []
    for line in lines[2:2 + n_atoms]:
        if len(line) < 44:
            raise ValueError("An atom record is too short for standard GRO fields.")
        residues.append((int(line[0:5]), line[5:10].strip()))
        names.append(line[10:15].strip())
        coordinates.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
    xyz = np.asarray(coordinates, dtype=float)
    box_values = [float(value) for value in lines[-1].split()]
    if len(box_values) == 3:
        box = np.diag(box_values)
    elif len(box_values) == 9:
        b = box_values
        box = np.array([[b[0], b[3], b[4]], [b[5], b[1], b[6]], [b[7], b[8], b[2]]])
    else:
        raise ValueError("A GRO box must contain three or nine components.")
    if not np.all(np.isfinite(xyz)) or not np.all(np.isfinite(box)):
        raise ValueError("Nonfinite coordinate or box component.")
    volume = float(np.linalg.det(box))
    if volume <= 0:
        raise ValueError("Box volume must be positive.")
    return xyz, names, residues, box, volume


def read_water_count(path: Path) -> int:
    section = ""
    inventory = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().casefold()
        elif section == "molecules":
            fields = line.split()
            if len(fields) != 2:
                raise ValueError("Expected molecule name and count.")
            inventory.append((fields[0], int(fields[1])))
    if len(inventory) != 1 or inventory[0][0] != "SOL" or inventory[0][1] <= 0:
        raise ValueError("This reader requires one positive SOL entry in [ molecules ].")
    return inventory[0][1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gro", type=Path)
    parser.add_argument("topology", type=Path)
    parser.add_argument("--output", type=Path, default=Path("inspection"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    xyz, names, residues, box, volume = read_gro(args.gro)
    n_water = read_water_count(args.topology)
    if len(xyz) != 3 * n_water:
        raise ValueError("Coordinate sites do not equal three times the SOL count.")
    for i in range(n_water):
        begin = 3 * i
        if names[begin:begin + 3] != ["OW", "HW1", "HW2"]:
            raise ValueError(f"Water {i + 1}: expected OW, HW1, HW2 order.")
        group = residues[begin:begin + 3]
        if not (group[0] == group[1] == group[2] and group[0][1] == "SOL"):
            raise ValueError(f"Water {i + 1}: inconsistent residue identity.")
    oxygen = xyz[::3]
    summary = {
        "coordinate_file": args.gro.name,
        "topology_file": args.topology.name,
        "coordinate_sha256": hashlib.sha256(args.gro.read_bytes()).hexdigest(),
        "topology_sha256": hashlib.sha256(args.topology.read_bytes()).hexdigest(),
        "molecules_SOL": n_water, "sites_from_coordinates": len(xyz),
        "sites_from_topology": 3 * n_water, "atom_order": "OW, HW1, HW2",
        "box_vectors_nm": box.tolist(), "volume_nm3": volume,
        "structure_stage": "initial solvent construction",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "water_input_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    with (args.output / "water_input_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["quantity", "value", "unit"])
        writer.writerows([
            ["SOL molecules", n_water, "count"],
            ["coordinate sites", len(xyz), "count"],
            ["topology sites", 3 * n_water, "count"],
            ["box volume", volume, "nm^3"],
        ])
    zh = args.language == "zh"
    tr = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14, "svg.fonttype": "path", "figure.facecolor": "#faf9f4",
        "axes.facecolor": "#faf9f4", "savefig.facecolor": "#faf9f4",
        "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    corners = {bits: np.asarray(bits) @ box for bits in itertools.product((0, 1), repeat=3)}
    for axis, (a, b) in zip(axes.flat, ((0, 1), (0, 2), (1, 2))):
        axis.scatter(oxygen[:, a], oxygen[:, b], s=10, alpha=0.55, color="#387d70", linewidths=0)
        for bits, origin in corners.items():
            for dimension in range(3):
                if bits[dimension] == 0:
                    target_bits = list(bits)
                    target_bits[dimension] = 1
                    target = corners[tuple(target_bits)]
                    axis.plot([origin[a], target[a]], [origin[b], target[b]],
                              color="#b06b41", linewidth=1.0)
        axis.set(xlabel=f"{'xyz'[a]} / nm", ylabel=f"{'xyz'[b]} / nm", aspect="equal")
        axis.set_title(tr("初始水氧投影", "Initial oxygen projection"), fontsize=14)
    axis = axes[1, 1]
    labels = [tr("坐标记录", "Coordinate records"), tr("拓扑预期", "Topology expectation")]
    counts = [len(xyz), 3 * n_water]
    bars = axis.bar(labels, counts, color=["#387d70", "#b06b41"], width=0.56)
    axis.bar_label(bars, padding=5, fontsize=15)
    axis.set_ylim(0, max(counts) * 1.2)
    axis.set_ylabel(tr("位点数", "Number of sites"))
    axis.set_title(tr("三位点水的数量核对", "Three-site water count check"), fontsize=14)
    fig.suptitle(tr("初始结构：坐标、拓扑与盒子", "Initial structure: coordinates, topology, and box"), fontsize=20)
    fig.savefig(args.output / "water_input_inspection.svg")
    fig.savefig(args.output / "water_input_inspection.png", dpi=180)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

按脚本开头的命令读取建盒后的 water.gro 与 topol.top；--language zh 或 en 选择图表语言。输出不改写输入，图为初始结构投影，计数与体积直接来自输入文件。

程序画出初始水氧坐标在三个平面上的投影，并用两种计数方式比较位点总数。投影像把立体物体的影子投在墙上：它保留两个方向的位置信息，沿视线方向的信息会重叠。因此图上两个点靠得很近，不等于三维空间里两个氧原子真的碰撞。我们使用投影检查整体填充、盒子范围和明显空洞，而把精确邻近距离留给考虑周期边界的三维计算。图注会说明所画的是初始结构，不把它解释成平衡后的空间分布。

### 初始水盒的实际坐标与拓扑计数

由 G02/inspect_water.py 读取最终例题建盒后的 water.gro 与 topol.top 绘制。三个面板是氧坐标的平面投影，另一面板比较坐标位点数与拓扑预期数；它们描述初始构建状态。

GROMACS 2026.4；884 个 SPC/E 水分子，初始立方盒边长 3 nm；目标温度 300 K、压力 1 bar。NPT 记录 100 ps，描述统计窗口为 50–100 ps；轨迹播放器显示另一个 100 ps NVE 阶段。

[下载参考数据与完整输入（ZIP） 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/#zh-s7)

实际初始结构的三个正交投影，每点是一枚水氧。最后一幅核对坐标文件的原子记录数与拓扑指定的三位点水总位点数；这里观察的是建盒后的起始坐标。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 水分子数 | 884 | 1 |
| 坐标位点数 | 2652 | 1 |
| 拓扑位点数 | 2652 | 1 |
| 初始盒体积 | 27.0 | nm³ |

这次初始构建得到 884 个水分子，对应 2652 个坐标位点，恰好满足每个 SPC/E 水分子三个位点的关系；拓扑预期计数与坐标计数一致。初始盒子体积为 27 nm³，对应三条 3 nm 的边。三个投影让我们从不同方向检查水是否填入同一个周期盒子，计数图则确认了分子清单与坐标之间的对应。后面 NPT 阶段的平均体积会改变，因此 27 nm³ 描述的是建盒起点，不能直接当成后续所有帧的体积。

得到相等的计数以后，还可以人工看一看最前面的几个水分子，确认氧与氢是否按预期组织，再查看 grompp 保存的展开拓扑。检查脚本不会替代这些物理阅读，它把最容易重复遗漏的步骤固定下来，使人有更多注意力放在模型选择上。如果未来在水盒中加入盐，分子清单、位点数和图中的颜色分类都需要扩展；如果换成四位点水，总位点数与真实原子数的关系也需要重新说明。

本讲输出的 JSON 和 CSV 只保存文件的相对名称、实际计数、盒子几何与检查结果，方便后续绘图与比较。它们不是新的分子模拟结果，而是从已有输入提取的结构描述。轨迹的温度、密度和运动统计仍来自真正运行后的文件。把“输入描述”和“运行观测”分清，能够避免用一张初始结构图来证明体系已经平衡，也能在遇到异常曲线时明确应该先检查哪一层信息。

若对比两份输入，文件摘要提供一种直接的内容核对。摘要算法把文件内容转换成固定长度的标识，内容改变通常会产生不同标识，适合确认下载、复制或归档后的文件是否相同。它回答的是“字节内容有没有变化”，不回答“这个模型是否适合研究目标”。后一个问题仍然需要看分子组成、参数选择、几何和观察条件。把这两类检查分开，既能管理文件，也能保留科学判断的位置。

## 把一套输入整理成可以继续研究的起点

完成这一轮准备后，我们应能用一句话说明每个文件的作用：坐标给出起点，拓扑定义粒子与相互作用，参数规定推进和观察方式，TPR 把本次运行组装起来，检查点保留可延续的状态，轨迹与能量文件保存不同类型的观测。这样的认识比记住一张扩展名清单更耐用，因为以后遇到新工具或新文件格式，仍然可以按信息的作用寻找对应位置。

保留输入时，最好保留完整的可解析组合，而不是只留下最外层的 topol.top。它引用的力场版本、局部 itp 文件、坐标和参数都决定模型。文件摘要可以帮助确认某份输入在比较前后是否改变，清楚的阶段名称则帮助定位运行顺序。科学上可复查的计算，依赖这些具体信息能够重新组合；它不要求每次打开目录时都重新猜测哪个文件才是最后使用的一版。

现在可以做一个小的判断练习：如果把 npt.mdp 中的目标温度改为 310 K，却直接运行原来的 npt.tpr，程序会采用哪个温度？答案来自文件关系：mdrun 读取已经生成的 TPR，所以修改文本后需要重新预处理，新的选择才会进入运行输入。再想一个例子：如果坐标中的水数量增加，而 molecules 区块没有更新，哪一步应当发现问题？这次是模型装配前的一致性检查。理解文件流向，就能自己推出这些答案。

下一讲将使用这组输入真正推进水分子运动。我们会按最小化、控温、控压与观察的顺序读曲线，解释为什么要分阶段，以及怎样从实际记录判断应不应该进入下一步。现在已经知道每个设置住在哪里，后面的参数变化就能与它影响的物理过程一一对应。

## 延伸阅读与开放资料

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  坐标、拓扑、参数分工与水盒预处理流程的改编。

  改为 SPC/E 与2026.4输入；增加初学者文件解释、双语图示、单位交互和独立编写的检查程序。改编流程沿用 CC BY-SA 4.0。
- [GROMACS 2026.4 file formats](https://manual.gromacs.org/2026.4/reference-manual/file-formats.html) · GROMACS developers · Technical reference; no copied figure or extended prose

  GRO 固定字段与输出文件含义。

  独立讲解与本例专用读取器。
- [gmx grompp, GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-grompp.html) · GROMACS developers · Technical reference

  输入预处理、包含关系和输出选项。

  按本例文件组织说明。
- [PDB History](https://www.rcsb.org/pages/about-us/history) · RCSB Protein Data Bank · Factual historical citation; no image reuse

  1971年建立与初始七个结构的历史。

  历史示意图原创。
