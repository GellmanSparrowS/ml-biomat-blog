# 从准备到采样：让蛋白质适应水环境

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g07/
Language: zh-CN

用位置限制、检查点与真实温压曲线，理解几何松弛、环境调整和蛋白质运动各自需要什么。

## 让刚刚装好的分子系统开始运动

把几种液体倒进同一个容器后，混合物需要一段时间才能达到均匀的温度和组成。分子模拟的起点也有类似问题：上一讲已经把泛素、水和离子放进盒子，但这些坐标来自结构准备、溶剂模板和随机替换，还没有共同适应所选的相互作用。若立即把第一帧后的运动都当作要研究的蛋白质行为，初始接触的调整就会混进结果。本讲从这份溶液出发，依次进行能量最小化、温度准备、体积准备和解除位置限制后的采样，学会用实际曲线判断每个阶段在做什么。

这里的“准备”包含几个不同层次。原子过近时，排斥作用可能很大，需要先改变位置；位置合理以后，还要给粒子分配速度，使系统能够在指定温度附近运动；盒子的体积则需要与外部压力条件相适应。蛋白质和水的运动时间也不相同：某些局部振动很快，整个蛋白质转动、柔性尾部改变构象或者跨越较高的构象势垒，往往需要更长时间。把这些层次分开，可以避免用一个模糊的“已经平衡”同时代替对几何、温度、体积和构象采样的判断。

本例的流程从同一个最小化结构开始，先运行 100 ps 的恒体积温度准备，再运行 200 ps 的恒压准备，最后得到 1 ns 的无位置限制生产轨迹。ps 是皮秒，等于 10⁻¹² s；1 ns 等于 1000 ps。动力学时间步为 0.002 ps，也就是 2 fs，因此 100 ps 需要 50000 步，1 ns 需要 500000 步。时间步是积分过程中推进状态的间隔，轨迹保存间隔则是从这些状态中每隔多少步记录一帧，两者承担不同任务。

分子组成沿用前一讲：1UBQ的76残基泛素，AMBER99SB-ILDN蛋白质参数，5868个TIP3P水，以及各17个Na⁺和Cl⁻。蛋白质端基和His68的化学状态保持固定。这套经典模型适合研究给定化学组成下的局部构象与水环境调整；成键反应和质子转移需要另行选择描述。初始几何准备、温压环境和后面的结构分析都围绕同一个明确的分子系统展开。

在前两段动力学里，泛素的重原子受到指向参考位置的弹性回复力，让水和离子能够先在相对稳定的蛋白质形状周围调整。正式采样时去掉这组附加回复力，保留分子本身的力场作用以及温压控制。这个变化需要在输入和图中标清：受限时测到的蛋白质波动，与自由蛋白质的波动来自不同的势能条件。我们会同时查看准备阶段与生产阶段，但根据各自的物理设置解释它们。

这一过程常用于为蛋白质构象、相互作用和溶剂环境研究建立起点。它也能帮助排查常见的运行问题：几何接触不合理、速度被意外重新生成、参考坐标用错，或者把尚在调整的体积当作稳定平均。了解这些问题的物理原因，比记住某个固定的平衡时长更有用。后面讨论轨迹分析和独立重复时，我们将继续追问较慢的结构变化；本讲先把一个组成正确的盒子变成条件明确、可继续分析的动力学系统。

[Figure: 四阶段蛋白质准备流程](https://ml-biomat.com/tutorials/molecular-dynamics/g07/#zh-s1)

图 1 · 最小化按优化步计数，后面三段按真实动力学时间计数。位置限制只用于本例的前两段动力学准备。

## 最低点附近仍然有生命分子的运动

研究者最早得到蛋白质三维结构时，常把它画成一幅确定的形状。这样的图对识别折叠方式和化学基团很有效，却把运动压缩到了同一张图里。1977 年，McCammon、Gelin 和 Karplus 研究牛胰蛋白酶抑制剂的分子动力学，用经验势能与原子的运动方程追踪折叠蛋白质内部的涨落。他们关心的是原子围绕平均结构怎样移动、运动之间怎样相关，以及这些相关性如何随时间改变。这个问题把“结构是什么样”推进到“结构周围有哪些活动”。

一个折叠蛋白质可以保持总体形状，同时让侧链转动、环区摆动、内部原子产生相关位移。就像一座吊桥仍然保持桥的结构，却会在风和行人作用下发生小幅振动，结构稳定与完全静止是两回事。蛋白质当然没有桥梁那样的宏观支架，它的形状来自许多分子相互作用的共同作用。类比帮助我们理解的是：观察到一个平均形状，并不意味着组成它的每个位置在每一时刻都不变。模拟中值得研究的正是这些运动及其分布。

能量最小化解决的是另一个问题。给定一组坐标与势能函数，优化程序沿着有利于降低势能的方向调整原子，直到满足预设的力或收敛条件。它像沿山坡走向附近的低处，能够消除初始构型中的不合适接触，却不会自动翻过所有山脊去寻找整个地形中的最低谷。一个大分子的势能由许多位置共同决定，通常存在大量局部低谷。因此，本讲使用最小化来准备几何，而蛋白质在有限温度下访问哪些状态，仍由随后的动力学与采样决定。

温度控制方法的发展，也体现了从“得到一个数值”转向“得到正确的分布”。2007 年，Bussi、Donadio 和 Parrinello 提出随机速度缩放方法，在调整整体动能时引入经过设计的随机性，使系统能够采样正则分布。2020 年，Bernetti 和 Bussi 把相近的思路用于体积控制，在平均压力调节之外保留与恒压系综相容的体积涨落。本例使用的 v-rescale 与 C-rescale 就与这两项工作相联系：目标温度和压力描述环境，瞬时状态则保留热运动带来的波动。

因此，平衡曲线通常是一条有起伏的带，而不是一根精确贴住目标值的直线。目标为 300 K 的有限体系，其瞬时温度会围绕附近变化；目标为 1 bar 的小盒子，瞬时压力也可能在很宽的范围内起伏。判断时需要问：是否仍有持续趋势、平均值使用了哪段时间、波动的定义是什么、数据来自哪一种势能条件。这些问题把科学史中的核心认识带回实际操作：我们要研究的是运动形成的统计规律，而不是把运动调节成一幅静态图片。

[Figure: 蛋白质运动与温压控制科学史](https://ml-biomat.com/tutorials/molecular-dynamics/g07/#zh-s2)

图 2 · 1977年的蛋白质模拟关注平均结构周围的涨落；后来的随机温压控制方法把分布和涨落放进采样设计。图中的线条与盒子是概念示意。

## 先松开过近接触，再给系统真实的时间

分子力场中的排斥作用在很近的距离上变化得很快。如果一个新加入的水分子靠某个蛋白质原子太近，初始力可能远大于正常热运动中常见的值。直接用较长时间步推进，会让原子在一个积分步内移动过多，后续约束与力计算也可能失去合适的几何条件。最陡下降法利用当前力指向势能下降的方向，并调整尝试位移，在开始真实动力学之前减轻这种局部不匹配。本例的 emstep 为 0.001 nm，是优化尝试的步长尺度，而非动力学速度或物理时间。

在这段几何准备中，我们采用软件所提供的柔性水键角定义，并设置 constraints=none。这样，水内部几何和溶剂接触可以一起松弛。进入动力学后，水恢复 TIP3P 的刚性几何，由 SETTLE 处理；蛋白质中涉及氢的键长使用 LINCS 约束。两种阶段的自由度不同，势能项也随之改变。比较最小化末态和动力学起点时，应该分别阅读各自的模型设置，而不是把它们的能量连成一条同一势能函数下的守恒曲线。

最小化输入中的 emtol=500 表示希望最大原子受力降到 500 kJ mol⁻¹ nm⁻¹ 以下。这里的“最大”取的是所有原子受力大小中的最大值，便于发现局部仍然很紧张的位置。nsteps=50000 给出允许尝试的步数上限；如果已经满足停止条件，程序会提前结束。在本次实际运行中，程序尝试了 1704 步后达到最大力约 452.11 kJ mol⁻¹ nm⁻¹，最终记录的步编号为 1703。编号从零开始，且优化中被拒绝的尝试未必输出能量点，因此图上的点数、末编号和尝试次数需要分别理解。

### 柔性几何最小化

```
integrator = steep
define = -DFLEXIBLE
constraints = none
emtol = 500
emstep = 0.001
nsteps = 50000
nstenergy = 20
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

用于含盐溶液；FLEXIBLE启用柔性水准备，后续动力学恢复刚性水。

势能从初始约 −3069.56 kJ/mol 降到约 −319180.06 kJ/mol，开始下降很快，后面逐渐平缓。较大的负数来自整个蛋白质水溶液中所有相关相互作用项的总和，零点由势能模型定义。它的绝对大小随系统组成和粒子数改变，不能把不同大小体系的总势能直接拿来评判“哪个蛋白质更稳定”。在同一段最小化里，这条曲线帮助我们观察几何松弛；最后是否满足设定的最大力条件，则从日志读出。

最小化结束以后，系统才开始有可解释的动力学时间。NVT 起点通过 gen-vel=yes 按 300 K 的目标分布生成速度，并用固定种子记录这次随机选择。约束会使允许的运动方式减少，程序据此计算用于温度的自由度。此后速度与位置共同演化，动能可以转化成势能，热浴也与系统交换能量。初始赋速只是给出起点，所以一个写着 300 K 的 gen-temp 不会让以后每一帧温度都等于 300 K。

在本例中，起点温度记录为约 300.56 K，最初 0.2 ps 的保存值降到约 166.29 K，随后在准备过程中恢复到目标附近。这段变化出现在新几何开始进行受约束运动的初期，与后段稳定波动具有不同含义。分析时保留整段曲线，能够清楚看到准备过程，而统计后段 50–100 ps 则得到平均约 300.06 K、保存值标准差约 2.34 K。设定的目标温度与实际轨迹分别提供输入条件和测量信息，而是让输入条件与实际轨迹各自提供信息。

## 位置限制像弹簧，键长约束像固定连接

中文里“限制”和“约束”很容易混用，在分子动力学中却对应不同操作。位置限制为某个原子增加一项势能：离参考位置越远，附加回复力通常越大。原子仍然可以移动，移动幅度由这项势能和周围作用共同决定。键长约束则要求某一对原子之间的距离满足给定值，算法在推进时修正几何，使这个条件保持在数值精度内。前者改变能量地形，后者改变允许的自由度；它们可以同时存在，但承担不同用途。

想象把一个小球通过弹簧接到墙上的某一点。你仍然能把球拉开，弹簧会越来越用力地把它往回拉；如果换成长度固定的杆，小球可以绕连接点转动，却不能任意改变到连接点的距离。蛋白质的坐标与这些装置并不完全相同，但这个区别能够帮助阅读两个输入关键词：POSRES 对应额外的位置回复项，constraints=h-bonds 则把涉及氢的键长转为固定长度条件。解除 POSRES 后，蛋白质原有的化学连接和键长约束仍然保留。

[Figure: 位置限制弹簧与固定长度连接对照](https://ml-biomat.com/tutorials/molecular-dynamics/g07/#zh-s4)

图 3 · 位置限制让原子偏离参考位置时受到回复力；键长约束保持一对原子的距离。示意中的x是当前坐标，x₀是参考坐标，r₀是指定的固定距离。

对于本例各方向具有相同强度的位置限制，可以用原子偏离参考位置的距离来表达附加势能。距离增加一倍时，势能增加到四倍，回复力的大小增加一倍。这种二次势能在小位移问题中很常见，数学上也容易理解：如果每多拉开一点需要的力都变大，累计做功就会比距离本身增长得更快。下面的公式同时给出一维方向上的势能与回复力，便于把数值与运动方向联系起来。

一个方向的位置限制式 1

![一个方向的位置限制](https://ml-biomat.com/static/agent-math/4e69228cb98d44164bc7b4b3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| x, x₀ | 原子的当前位置与参考位置，下标0标记参考位置 | nm |
| Δx | 有方向的坐标差；正值表示当前坐标大于参考坐标 | nm |
| U_{r} | 一个原子沿这个方向的附加限制势能；下标r表示限制项 | kJ/mol |
| k | 位置限制力常数，控制偏移相同时回复作用的强度 | kJ mol⁻¹ nm⁻² |
| F_{x} | 限制力沿x方向的分量；下标x表示方向 | kJ mol⁻¹ nm⁻¹ |
| Δ, =, −, ½, ², × | Δ表示差；等号连接相等量；减法计算坐标差；力前负号让力指向参考；½乘以一半；平方是自身相乘，相邻量相乘 | 符号与运算，无单位 |

怎样理解回复力随偏移线性增大，沿位移累计做功得到二次势能。负号保证正向偏移受到负向的回复力。

算一个例子k=1000 kJ mol⁻¹ nm⁻²、Δx=0.05 nm时，U_r=½×1000×0.05²=1.25 kJ/mol，F_x=−50 kJ mol⁻¹ nm⁻¹。偏移0.10 nm时能量为5、力为−100。

使用条件一个原子、一个方向的谐和位置限制。整体限制能量需对选定原子及方向求和；其他力场相互作用仍同时存在。

本例对 602 个蛋白质重原子施加 1000 kJ mol⁻¹ nm⁻² 的位置限制，氢、水和离子没有包含在这份蛋白质重原子列表中。以某一个方向偏离 0.05 nm 为例，该方向增加的限制势能为 1.25 kJ/mol，回复力大小为 50 kJ mol⁻¹ nm⁻¹。若偏离到 0.10 nm，势能变成 5 kJ/mol，力大小变成 100 kJ mol⁻¹ nm⁻¹。这里计算的是一个原子、一个方向的附加项，整个蛋白质的限制能量还要把选定原子与各方向贡献相加。

改变一个原子的一个坐标方向，查看附加位置限制的能量与回复力。

[Figure: 谐和位置限制势能图](https://ml-biomat.com/tutorials/molecular-dynamics/g07/#zh-s4)

谐和位置限制的解析算例。k=0关闭这一附加势能项，分子原有的其他相互作用仍保留。

参考位置同样需要明确。NVT 与受限 NPT 都通过 grompp 的 -r em.gro 使用同一份最小化坐标作为参考，避免在每个阶段悄悄把已移动的位置重新定义为零点。NPT 的盒子会变化，本例使用 refcoord-scaling=com，让参考坐标集合的质心随盒缩放，而各参考原子相对这个质心的向量不随盒整体拉伸。这样保留蛋白质参考形状，适合此处的保形准备；它也使受限阶段的压力和维里量带有参考位置处理的特殊性，因此本讲把通常的压力统计解释放在解除位置限制后的生产段。

位置限制的用途是帮助安排准备阶段的调整次序。选择哪些原子、参考哪个结构以及用多大力常数，都应与目的相连。如果研究对象本来就需要在外部支架上受限，限制也可以成为正式模型的一部分；如果研究自由泛素在溶液中的运动，生产阶段就要移除这项准备用的附加势能。本例通过在 md.mdp 中去掉 define=-DPOSRES 完成这个变化，分析时也以这段无位置限制轨迹为主要的蛋白质运动记录。

## 温度、压力与体积怎样共同准备

温度与粒子的热运动有关，但不等于某一个原子的速度。较重原子在相同动能下速度较小，分子约束又会减少独立运动方式，所以需要把整个温控组的动能与自由度结合起来。本例把系统放在同一个 System 温控组中，自由度由程序依据粒子数、键约束、水的刚性几何和整体平动处理计算。对于这套经典模型，温度与动能之间的关系给出了一个可以检查数量级的桥梁。

用动能核对温度式 2

![用动能核对温度](https://ml-biomat.com/static/agent-math/0b3e0196bc87aae9d2c1eab6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| T | 由所选温控组动能定义的瞬时温度 | K |
| K | 整个所选温控组的动能，采用GROMACS摩尔能量表达 | kJ/mol；此处K是变量名，温度单位K另由位置区分 |
| f | 参与动能温度计算的自由度数，已考虑约束与整体运动处理 | 无量纲 |
| R | 气体常数约0.008314462618 kJ mol⁻¹ K⁻¹ | kJ mol⁻¹ K⁻¹ |
| =, 2, /, × | 等号、无量纲常数2、分数线除法与相邻量乘法；动能除以整个fR | 运算与常数，无单位 |

怎样理解经典二次动能自由度在平衡时平均各携带½RT的摩尔能量；程序用同一关系从当前动能定义瞬时温度。

算一个例子f=38371、K=47833.17788 kJ/mol，代入得到T≈299.86234 K，与生产500–1000 ps平均温度一致。自由度保持不变时，这个线性关系也适用于时间平均。

使用条件经典模型、所列温控组与GROMACS摩尔能量单位。约束减少自由度；位置限制是附加势能，不像固定距离约束那样直接删除一个运动自由度。

实际输入中 System 的自由度为 38371，生产后段的平均动能约为 47833.18 kJ/mol。把它们与气体常数代入公式，得到约 299.86 K，与输出的平均温度一致。这里的 kJ/mol 是 GROMACS 对整盒能量所采用的摩尔能量表达习惯，所以公式使用气体常数 R；如果改用单个真实盒子的焦耳能量，就要相应使用玻尔兹曼常数。保持单位体系一致，比背下“温度等于某个系数乘动能”更容易避免错误。

NVT 阶段固定粒子数和盒体积，通过 v-rescale 与 300 K 热浴交换能量，时间常数 tau-t 为 1 ps。这个时间常数控制耦合的时间尺度，并不是每隔 1 ps 才测一次温度，也不是承诺系统在 1 ps 后已经准备完毕。温度接近目标时，局部构象和溶剂仍可能继续调整。这里使用 100 ps 的准备段，并保留整段输出以观察早期瞬态和后段波动；对其他体系，应按具体曲线和结构变化选择所需时长。

### 100 ps受限NVT准备

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
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
define = -DPOSRES
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261121
ld-seed = 20261201
```

以共同最小化结构为参考，生成本条轨迹的初始速度。

随后开启 C-rescale 压力耦合，参考压力为 1 bar，tau-p 为 5 ps，采用各向同性缩放，使三个方向保持原有盒形关系而共同改变尺度。压缩率 4.5×10⁻⁵ bar⁻¹ 描述体积对压力变化的响应尺度，参与调节过程。对近似各向同性的蛋白质溶液，这种盒形处理直观而常用；膜体系具有平面方向和法向方向的区别，后面会使用分别调节这两个方向的设置。环境的几何特征进入压力控制的方式，而非所有体系共用一个盒子选项。

### 200 ps受限NPT准备

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
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
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
define = -DPOSRES
refcoord-scaling = com
nsteps = 100000
ld-seed = 20261301
```

继承NVT状态；参考坐标质心随盒缩放，保留参考蛋白质形状。

本例初始体积约为 193.424 nm³，受限 NPT 后段 100–200 ps 的平均体积约为 189.422 nm³。进入无位置限制生产后，后段 500–1000 ps 的平均体积约为 189.137 nm³，保存值标准差约为 0.670 nm³。盒子在准备中收缩，使固定数量的粒子占据略小空间。生产后段的平均质量密度约为 1012.09 kg/m³，它包含蛋白质、离子和水的总质量，因此比较实验时应选择组成相符的溶液，而不是把这个混合体系的密度当作纯水密度。

无位置限制生产段的瞬时压力波动很大，后段平均值约为 2.45 bar，保存值标准差约为 183.65 bar。对一个很小的盒子，热运动与分子相互作用造成的瞬时压力涨落可以远大于环境压力值。图中同时画出每 1 ps 保存的原始值和 50 ps 分块均值，帮助区分瞬时起伏与较慢变化。标准差描述保存记录的散布，平均值的不确定度还需要考虑时间相关；第九讲会用独立重复和相关时间进一步处理这一点。

压力常从气体分子撞击容器壁的图像来理解：单位面积承受的平均作用越大，压力越高。这里使用周期边界，没有一堵真实的容器墙，程序改由粒子的运动和相互作用计算内部应力，再从三个方向的贡献得到所报告的标量压力。1 bar 等于 100000 Pa，Pa 表示每平方米对应一牛顿的力。瞬时计算中，粒子运动与相互作用的贡献可以很大并部分抵消，所以小盒子的压力比日常压力表读数更剧烈地变化。压力表本身则在宏观空间和测量时间上做了平均，两种读数的观察尺度不同。

同样，恒压也不意味着每一帧都被强制改成正好 1 bar。控制方法让盒子与所设定的压力环境相联系，同时保留有限体系允许的涨落。某一保存时刻出现负的内部压力，表示当时计算的运动与相互作用合量对应拉伸方向的应力状态；应结合持续时间、体积变化和统计分布理解。若长期出现持续偏离或异常收缩，就要回到模型与控制条件检查。把单帧数值、时间平均和外部参考值分开，读者就能理解为什么一条看起来很吵的曲线仍然可能包含稳定的统计信息。

## 把状态接下去，而不是在每段重新开始

一次动力学运行结束时，坐标只记录了状态的一部分。接下来怎样运动，还取决于速度、积分器和温压控制的内部信息。GROMACS 的检查点文件 CPT 保存继续运行所需的状态，因此从 NVT 转到 NPT 时，我们同时给出 nvt.gro 和 nvt.cpt，再将 continuation 设为 yes、gen-vel 设为 no。这样，第二段继承前一段已经形成的运动，而不是重新抽一套速度。转入生产阶段时，同样读取 npt.cpt，并移除准备用的位置限制。

可以把坐标比作一张交通路口的照片，而速度说明每辆车正往哪里走、走得多快。两张照片里车辆位置完全相同，也可能对应不同的下一秒：一辆车正在刹车，另一辆正在加速。检查点保存的状态比照片更完整，所以对连续模拟尤其有用。我们在新阶段改变的是明确指定的控制条件，例如开启压力耦合或去掉位置限制，同时尽量连续传递其他状态。这样的衔接使每一段的作用更容易解释。

几个输出文件的用途也可以据此分清。XTC 以指定精度压缩保存坐标帧，适合观看运动以及计算距离、形状等结构量；EDR 保存能量与温度、压力等记录，便于按名称提取；CPT 保存接续计算所需的状态。把 XTC 中的一帧拿出来，可以作为建立另一项计算的坐标起点，但这与从检查点延续同一条动力学不同。分析副本和检查点各有用途，保存时让它们与对应的输入条件关联起来，就能既方便查看结果，又保留继续运行的能力。

生产输入保留 300 K 与 1 bar 的环境条件，时间步仍为 2 fs，运行长度为 500000 步。每 500 步保存一次压缩坐标，即每 1 ps 一帧，得到包含首尾时刻的 1001 帧记录。能量也在这一生产段每 1 ps 保存一次，而准备段的能量记录更密，为每 0.2 ps 一次。分析程序根据各文件实际时间列处理它们，绘图时若使用累计时间，会明确加上前面动力学阶段的时长；最小化的优化步数没有被加进物理时间。

### 1 ns无位置限制生产

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 500
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
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
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
nsteps = 500000
ld-seed = 20261401
```

继承NPT状态；不启用POSRES；每1 ps保存坐标与能量。

下面的脚本从上一讲的含盐坐标与配套拓扑开始，依次生成并运行各阶段输入，再提取我们要看的能量与状态量。setup 保存共同的最小化结果，replica-1 保存这一组速度种子对应的动力学。这样的目录组织让“同一个最小化起点”与“某一条独立轨迹”之间的关系清楚，后面做重复模拟时也容易沿用。脚本中的四个计算线程只是本例的执行设置，分子模型由前面的输入文件和拓扑规定。

### 完整准备与采样流程

```
#!/usr/bin/env bash
set -euo pipefail

# Start beside the solution coordinates, topology, and the four MDP files.
mkdir -p setup replica-1
gmx grompp -f em.mdp -c solvated-ions.gro -p topol.top -o setup/em.tpr
gmx mdrun -deffnm setup/em -ntmpi 1 -ntomp 4 -pin off
printf 'Potential\n0\n' | gmx energy -f setup/em.edr -o setup/em-potential.xvg
cp setup/em.gro topol.top posre.itp nvt.mdp npt.mdp md.mdp replica-1/
(
  cd replica-1
  gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
  gmx mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off
  gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr
  gmx mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off
  gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
  gmx mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off
  printf 'Temperature\n0\n' | gmx energy -f nvt.edr -o nvt-temperature.xvg
  printf 'Temperature\nPressure\nVolume\nDensity\n0\n' | gmx energy -f npt.edr -o npt-properties.xvg
  printf 'Temperature\nPotential\nKinetic-En.\nTotal-Energy\nPressure\nVolume\nDensity\n0\n' | gmx energy -f md.edr -o md-energy.xvg
)
python analyze_preparation.py . --output preparation-analysis --language en
```

与上一讲的solvated-ions.gro、topol.top、posre.itp和本讲四个MDP、分析程序同目录运行。

运行过程中，日志中的约束偏差、最大力、能量输出和最终时间都值得检查。某条命令正常结束，说明程序完成了这一计算步骤；对科学结果，还要继续核对是否采用了预期的限制、是否继承了正确的状态，以及观测量是否符合这一阶段的物理条件。如果中途需要恢复同一段运行，应使用相应检查点继续，而不是把一份已经运行过的坐标再次交给 gen-vel=yes 当作延续。重新赋速可以用来设计独立重复，但那是另一种明确的研究安排。

## 让四幅图回答四个具体问题

完整分析程序首先读取 XVG 中的 legend 标签来识别每一列，再读取时间与数值。这个步骤很实用，因为 energy 命令的输出列顺序由可选能量项决定，未必等于你输入名称的顺序。程序不会根据“我先输入了温度”就认定第一列一定是温度。最小化文件的第一列按优化步处理；三段动力学的时间则分别根据各自起止时刻核对。把变量身份与坐标轴先确定好，后面的平均、波动与可视化才有一致含义。

图 A 使用优化步横轴，显示最小化势能的下降。图 B 将 100 ps NVT、200 ps 受限 NPT 和 1000 ps 生产段放在同一条累计动力学时间轴上，以颜色区分阶段。图 C 从 NPT 准备开始计时，在 200 ps 处标出移除位置限制的边界，便于观察体积在环境调整后的变化。图 D 则只取无位置限制的生产压力，保留原始起伏，并叠加明确定义的分块均值。每幅图围绕一个问题组织，避免把所有输出量堆在一条坐标轴上。

### 完整Python：读取阶段与绘图

```
"""Inspect the recorded preparation and production of ubiquitin replica 1."""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def xvg(path):
    legends, values = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
        if match:
            legends[int(match[1])] = match[2]
        if line and not line.startswith(("#", "@")):
            values.append([float(x) for x in line.split()])
    a = np.asarray(values)
    return a[:, 0], {name: a[:, i+1] for i, name in legends.items()}


def stats(t, series, start, stop):
    select = (t >= start) & (t <= stop)
    return {"start_ps": start, "stop_ps": stop, "n_records": int(select.sum()),
            "observables": {name: {"mean": float(y[select].mean()),
                                   "sample_sd": float(y[select].std(ddof=1))}
                            for name, y in series.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path,
                        help="Contains setup/ and replica-1/ subdirectories")
    parser.add_argument("--output", type=Path, default=Path("preparation-analysis"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    em_t, em = xvg(args.directory / "setup/em-potential.xvg")
    rep = args.directory / "replica-1"
    tv, nvt = xvg(rep / "nvt-temperature.xvg")
    tp, npt = xvg(rep / "npt-properties.xvg")
    tm, md = xvg(rep / "md-energy.xvg")
    assert np.isclose(tv[-1], 100) and np.isclose(tp[-1], 200)
    assert np.isclose(tm[-1], 1000)
    log = (args.directory / "setup/em.log").read_text(encoding="utf-8")
    steps = int(re.search(r"converged to Fmax < 500 in (\d+) steps", log)[1])
    fmax = float(re.search(r"Maximum force\s*=\s*([\d.eE+-]+)", log)[1])
    means, centers = [], []
    for start in np.arange(0, 1000, 50):
        selected = (tm >= start) & (tm < start+50)
        means.append(float(md["Pressure"][selected].mean()))
        centers.append(float(tm[selected].mean()))
    summary = {
        "minimization": {"attempted_steps": steps,
                         "last_recorded_step": int(em_t[-1]),
                         "Fmax_kJ_mol_nm": fmax,
                         "initial_potential_kJ_mol": float(em["Potential"][0]),
                         "final_potential_kJ_mol": float(em["Potential"][-1])},
        "nvt_50_100ps": stats(tv, nvt, 50, 100),
        "restrained_npt_100_200ps": stats(tp, {k: npt[k] for k in
            ("Temperature", "Volume", "Density")}, 100, 200),
        "unrestrained_npt_500_1000ps": stats(tm, md, 500, 1000),
        "pressure_blocks": {"window_ps": "0 <= t < 1000", "width_ps": 50,
                            "centers_ps": centers, "means_bar": means},
        "pressure_scope": "Unrestrained production; restrained preparation uses refcoord-scaling=com",
        "sd_definition": "Sample spread of saved records, not an uncertainty of the mean"
    }
    (args.output / "preparation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    zh = args.language == "zh"
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC",
                         "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
                         if zh else ["DejaVu Sans"], "font.size": 14,
                         "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(em_t, em["Potential"]/1000, color="#267b7e", lw=1.6)
    ax.set_xlabel("最小化优化步" if zh else "Minimization step")
    ax.set_ylabel("势能 / (10³ kJ mol⁻¹)" if zh else "Potential / (10³ kJ mol⁻¹)")
    ax.set_title("A  几何松弛" if zh else "A  Geometrical relaxation")
    ax = axes[0, 1]
    ax.plot(tv, nvt["Temperature"], color="#a77747", alpha=.75,
            label="NVT + 位置限制" if zh else "NVT + restraints")
    ax.plot(tp+100, npt["Temperature"], color="#6e8d7a", alpha=.75,
            label="NPT + 位置限制" if zh else "NPT + restraints")
    ax.plot(tm+300, md["Temperature"], color="#267b7e", alpha=.6,
            label="NPT生产" if zh else "NPT production")
    ax.axhline(300, color="#4d5456", ls="--", lw=1)
    ax.set_xlabel("累计动力学时间 / ps" if zh else "Cumulative dynamics time / ps")
    ax.set_ylabel("温度 / K" if zh else "Temperature / K")
    ax.set_title("B  温度与阶段" if zh else "B  Temperature and stages")
    ax.legend(fontsize=11, frameon=False, loc="lower right")
    ax = axes[1, 0]
    ax.plot(tp, npt["Volume"], color="#6e8d7a", label="受限准备" if zh else "Restrained preparation")
    ax.plot(tm+200, md["Volume"], color="#267b7e", alpha=.75,
            label="解除位置限制" if zh else "Position restraints removed")
    ax.axvline(200, color="#4d5456", ls="--", lw=1)
    ax.set_xlabel("自NPT准备开始的时间 / ps" if zh else "Time from NPT preparation / ps")
    ax.set_ylabel("盒体积 / nm³" if zh else "Cell volume / nm³")
    ax.set_title("C  溶液体积的调整" if zh else "C  Solution-volume adjustment")
    ax.legend(fontsize=11, frameon=False)
    ax = axes[1, 1]
    ax.plot(tm, md["Pressure"], color="#a9c8c1", lw=.8,
            label="每1 ps保存值" if zh else "Records every 1 ps")
    ax.plot(centers, means, "o-", color="#b47742", ms=4,
            label="50 ps分块均值" if zh else "50 ps block means")
    ax.axhline(1, color="#34484b", ls="--", lw=1, label="1 bar")
    ax.set_xlabel("生产时间 / ps" if zh else "Production time / ps")
    ax.set_ylabel("压力 / bar" if zh else "Pressure / bar")
    ax.set_title("D  无位置限制的压力波动" if zh else "D  Pressure without position restraints")
    ax.legend(fontsize=11, frameon=False)
    for ax in axes.flat:
        ax.grid(alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle("泛素：从初始几何到溶液动力学" if zh else
                 "Ubiquitin: from initial geometry to solution dynamics", fontsize=21)
    fig.savefig(args.output / "protein_preparation.svg")
    fig.savefig(args.output / "protein_preparation.png", dpi=140)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

依赖NumPy与Matplotlib。读取setup与replica-1下的真实能量文件；--language zh或en选择图的语言。

### 泛素从几何准备到生产的实际记录

同一最小化起点，100 ps受限NVT、200 ps受限NPT与1000 ps无位置限制NPT。压力面板只用无位置限制生产，50 ps分块覆盖0≤t<1000 ps；完整原始压力记录包括1000 ps末帧。

GROMACS2026.4；PDB 1UBQ链A、76个残基；AMBER99SB-ILDN与TIP3P。保留602个实验重原子，加入629个氢原子；His68选中性NE2质子化状态，采用带电游离末端。

[下载参考数据与完整输入（ZIP） 0.37 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-preparation-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g07/#zh-s7)

真实最小化、受限NVT、受限NPT及无位置限制生产记录。最小化横轴是优化编号；各动力学阶段以自己的起点计时。位置限制配合refcoord-scaling=com的准备阶段用于观察几何、温度与体积调整；压力面板取无位置限制生产，细线为保存记录，深色点为50 ps区间均值。

四幅图放在一起，可以读出一个连贯过程。几何松弛首先降低局部高能接触；赋速后，初始几皮秒内仍有明显的能量重新分配，温控随后把平均动能维持在目标附近；开启压力耦合后，盒子从初始几何体积调整到溶液更常访问的范围；解除位置限制后，蛋白质与溶剂在新的势能条件下继续运动。与此同时，温度和体积曲线仍然有起伏，压力更显示出宽幅涨落。这些变化分别对应准备、环境交换和有限体系热运动。

图 D 的每个橙色点平均一个 50 ps 区间内的保存记录，区间采用包含左端、不包含右端的定义。例如第一块使用 0≤t<50 ps，第二块使用 50≤t<100 ps，以此覆盖 0≤t<1000 ps。原始曲线仍包括 1000 ps 末帧，后段统计也包括 500 ps 和 1000 ps 两个端点。把这些边界写清，可以让别人用相同文件得到相同数字。分块线让较慢的变化更容易看见，但没有把原始波动删去，也没有把各块自动当成相互独立的样本。

观察这些图后，我们可以说这一套输入已经形成了可检查的准备过程，并在无位置限制阶段记录了目标温压附近的溶液动力学。若接下来问泛素尾部通常能伸展多远、某个侧链有几种构象或者蛋白质是否会发生较大结构改变，还要分析对应的结构变量和采样情况。能量、温度和体积是进入这些问题的基础检查，它们与具体的蛋白质构象统计承担互补作用。下一讲将把注意力转向坐标轨迹本身。

## 根据要测的现象决定准备是否充分

“平衡多久”没有脱离体系与观测量的统一答案。水的局部位置、溶液整体密度、蛋白质侧链和长环区可能以不同速度调整。一条体积曲线已经围绕某个范围波动，蛋白质仍可能停留在起始结构附近的某个构象区域。相反，一段侧链看起来活动很多，也不保证盒子的温度或组成设置正确。可靠的判断应当沿着研究问题选择观测量，再把相关的准备曲线、结构变化和独立轨迹放在一起看。

对本例的入门目标，短轨迹足以练习如何组织输入、继承状态、区分附加位置限制与化学键约束，以及读取基本物理量。研究泛素更慢的构象交换时，可以延长生产并采用独立重复，检查关心的结构分布是否稳定。延长前仍应保留已经确定的分析定义，例如统一的结构参考、相同的原子选择以及清楚的统计窗口。这样，更多计算时间会增加对同一个问题的证据，而不会因为定义不断改变而难以比较。

如果曲线显示持续漂移，下一步应与漂移对象对应。温度偏离时检查赋速、温控组、自由度与能量交换；体积持续变化时检查压力耦合、体系组成与初始密度；局部几何异常时检查原子身份、拓扑连接、初始接触和约束设置。每个检查都有具体入口，也有可以观察的结果。把问题拆成这样一条因果链，往往比同时改动多个参数更容易理解究竟是哪一个条件改变了系统行为。

本讲也建立了一种读结果的习惯：先辨认数据属于哪个物理阶段，再解释数值。最小化的 1704 次尝试是几何优化记录；100 ps 与 200 ps 是受限准备的动力学时长；生产后段约 299.86 K、189.14 nm³ 和 2.45 bar 则是指定时间窗口里的实际平均值，各自带有不同幅度和相关性的波动。模型条件、时间窗口与统计定义一起构成这些数字的意义。带着这套习惯去看蛋白质轨迹，分子动画中的每一次移动才会逐渐转化成可以讨论的科学量。

## 延伸阅读与开放资料

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  最小化、受限NVT/NPT与生产的基本顺序。

  采用1UBQ与明确的2026.4输入，详细解释参考坐标、检查点、限制与约束；加入真实分阶段分析。
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  蛋白质水溶液平衡与连续运行的实践流程。

  使用当前随机温压控制与泛素案例，区分受限准备和无位置限制生产。
- [Restraints — GROMACS 2026.4](https://manual.gromacs.org/2026.4/reference-manual/functions/restraints.html) · GROMACS developers · GROMACS documentation terms; factual reference

  位置限制势能、回复力和参考位置定义。

  以一个坐标方向的完整算例和交互说明。
- [Molecular dynamics parameters — GROMACS 2026.4](https://manual.gromacs.org/2026.4/user-guide/mdp-options.html) · GROMACS developers · GROMACS documentation terms; factual reference

  continuation、约束、速度生成和refcoord-scaling的实际含义。

  把具体选项与本例数据阶段对应，说明com参考处理与受限压力的条件。
- [Dynamics of folded proteins](https://doi.org/10.1038/267585a0) · J. Andrew McCammon; Bruce R. Gelin; Martin Karplus · Publisher copyright; factual historical citation

  1977年蛋白质内部涨落研究的科学问题。

  历史问题重新叙述，配平均结构周围运动的概念图。
- [Canonical sampling through velocity rescaling](https://doi.org/10.1063/1.2408420) · Giovanni Bussi; Davide Donadio; Michele Parrinello · Author preprint publicly readable; factual citation

  2007年随机速度缩放与正则分布采样。

  解释平均值与分布的区别，使用概念图。
- [Pressure control using stochastic cell rescaling](https://doi.org/10.1063/5.0020514) · Mattia Bernetti; Giovanni Bussi · Author preprint publicly readable; factual citation

  2020年随机晶胞缩放的体积涨落思路。

  以当前溶液的压力与体积记录说明方法用途。
