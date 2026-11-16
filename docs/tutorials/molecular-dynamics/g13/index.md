# 膜怎样组织分子：脂质与界面

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g13/
Language: zh-CN

从两层脂质的方向出发，读取膜蛋白周围的面积、厚度、密度与分子取向。

## 一层薄膜，怎样同时隔开水和组织分子

把食用油倒进水里，静置后会出现清楚的分层；加入洗涤剂并摇晃，油又能分散成许多小滴。决定这些变化的一个因素，是分子的不同部位怎样与水接触。细胞膜也利用这种分子差异，但它承担的任务更精细：把细胞内外分开，让特定物质通过，还为蛋白质提供合适的工作环境。研究药物递送颗粒、人工囊泡或膜表面涂层时，我们经常要问，某个分子会停在膜外、插进膜里，还是改变膜中其他分子的排列。分子模拟能把这个问题变成可观察的空间分布和运动。

本讲观察一种叫POPC的磷脂。它有一个容易与水相互作用的头部，以及两条以碳和氢为主的尾链。头部与尾部的化学环境不同，分子因而具有两亲性。大量这样的分子可以把尾链收在内部，让两侧的头部接触水，形成脂质双层。这里的“双层”指两排方向相反的脂质分子，水位于膜的两边。肥皂泡则是一层水夹在两侧表面活性分子之间，尾部朝向空气；比较二者时，先找水在哪里，比把任何薄片都画成两排小圆圈更有帮助。

可以把脂质双层想成两队背靠背站立的人：朝外的一侧接触周围环境，朝内的一侧与另一队贴近。这个比喻帮助我们辨认两侧方向，但膜里的分子持续转动、摆动和交换邻居，尾链也会弯曲。头部通常处在界面附近，不等于所有头部都精确落在一个平面上。膜的厚度因此需要一个可测量的定义，例如两侧磷原子的平均高度差；膜的疏密也需要说明是统计原子数、质量，还是某类化学基团。定义不同，曲线回答的问题就不同。

例题中的膜还含有一组三聚体膜蛋白。它像嵌在柔软薄层中的通道结构，周围脂质必须与它共同安排位置。读完本讲，你将能核对一个膜体系的组成，理解为什么膜平面与垂直方向采用不同的压力缩放方式，从轨迹测量投影面积和厚度，并画出水、蛋白与脂质沿膜法线的分布。我们还会计算尾链的整体取向。所有这些量来自同一段真实轨迹，因而可以把图像中的空间组织与时间曲线联系起来，而不只凭一张好看的结构图判断体系。

## 从铺开的脂质，到会流动的分子拼图

在看清单个膜分子之前，人们已经尝试用面积判断膜的结构。1925年，戈特和格伦德尔从红细胞中提取脂质，把它们铺在水面上形成单分子层，再比较铺展面积与细胞总表面积。他们观察到面积比接近二，并据此支持脂质形成双分子层的解释。这个研究的关键是把难以直接观察的厚度，转换成能够测量的面积关系：同一批分子铺成一层需要较大面积，分成两层时，每一层覆盖的面积约减半。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s2)

图 1 · 面积比较与流动镶嵌观点的概念图。上方用同样数量的分子比较单层与双层覆盖；下方把膜蛋白放入双层。

做一个几何练习就能理解这种推理。假设共有二百个相同的小片，每片占一格位置。把它们全部铺在桌面上，会覆盖二百格；把其中一百片铺在下面，另一百片铺在上面，两层共同覆盖一百格。这个例子把分子数、每个分子的占地与层数分开了。实际脂质会改变排列、倾斜和压缩程度，实验测量还涉及提取量与细胞表面积估计，因此“约两倍”是带有测量条件的结构线索。学习模拟时也要保留这种思路：从一个数字推回结构，必须知道这个数字怎样定义。

1972年，辛格和尼科尔森提出的流动镶嵌模型，把膜蛋白与脂质放在同一幅动态图景中：两亲性蛋白嵌入脂质环境，亲水部分接触水，疏水部分与膜内部相容，组分可以沿膜面运动。这个视角让膜从一张固定的隔板变成具有分子排列和运动的界面。我们接下来观察的通道与周围脂质，正适合用这种方式理解：蛋白决定局部的空间边界，脂质的排列和波动又构成蛋白周围的环境。

“流动”还需要说明方向。一个脂质在同一层里更换邻居，与它把极性头部穿过疏水内部、进入另一层，是两种不同运动。前者主要发生在膜面内，后者改变所属叶片，需要跨越不同的分子环境。把两层分别称为上叶片和下叶片，只是相对于图上的坐标命名，并不自动对应细胞外侧和内侧。真实细胞还可能在两侧放置不同脂质、糖链和蛋白，本例采用单一POPC组成，适合集中学习平面膜的几何与分析定义。

在计算机里，历史上的面积问题变得更具体。我们知道每个分子的身份，能跟踪其位置，也能把一个时刻的膜切成许多薄片，分别统计水、脂质和蛋白。代价是需要明确相互作用模型与观察时间。这里采用固定化学连接的经典全原子模型，保留原子运动、脂质构象和非键相互作用；化学反应、随环境改变的质子化以及完整细胞结构，则需要另外的模型设计。围绕当前保留的运动定义测量，可以让膜结构、模型与问题保持一致。

## 认识这片膜：通道、脂质、水和离子

蛋白的结构起点是公共记录1MAL中的麦芽孔蛋白LamB。三条各含421个氨基酸残基的链组成三聚体，原实验采用X射线衍射，分辨率为3.10Å。每个亚基具有β桶状骨架，在膜中形成通道。这里的通道背景与糖的跨膜运输有关，但当前模拟体系没有加入运输中的糖，也没有施加跨膜浓度差。我们研究的是这个通道所处的膜环境，以及蛋白和脂质在已准备构型附近的局部运动；运输速率需要另行定义进入、通过和离开的事件。

完整模型共有138195个原子：蛋白19260个，277个POPC分子共37118个，27204个水分子共81612个，另有131个钠离子和74个氯离子。三条蛋白的总电荷为−57个基本电荷，多出的57个钠离子负责中和，剩余74对钠、氯离子形成额外盐组分。POPC的头部同时含有正负电荷区域，整个分子净电荷为零；这种带局部电荷而总电荷为零的性质，与完全没有电荷相互作用的分子有明显区别。水和离子仍然能感受到头部不同原子附近的电场。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s3)

图 2 · 本段生产轨迹第一幅构型的正交投影。Cα连线表示主链走向，磷到尾端碳的线表示脂质整体方向，均为结构导引线；水、离子和其余原子参与原模拟。

结构中的化学状态已经写进拓扑。每条蛋白保留第22与38号半胱氨酸之间的二硫键；每条链的六个组氨酸采用中性HSD形式，氢位于环上的Nδ1。N端带三个端氢，C端为带负电的羧酸根形式。三条链采用同样的残基与端基定义。继续使用这个模型时，这些状态随拓扑保留，温度控制器不会自动依据溶液条件改变它们。若研究问题涉及某个位点的质子化变化，应先比较相应化学状态的模型，再讨论其对通道局部作用的影响。

蛋白、POPC和水采用同一套随例题提供的CHARMM拓扑与参数。水的残基名为TIP3，它对应本参数体系中的CHARMM TIP3P形式；名称相近的其他三点水模型具有不同参数，不能只改一个文件名就认为物理模型相同。范德华作用在1.0到1.2nm之间按力切换方式逐渐截断，静电采用PME，短程截断为1.2nm，含氢键长受到约束，时间步为2fs。这些选择共同定义本例的能量与运动规则，修改其中一项时，应检查它与其余参数的配合。

启动文件已经包含脂质和蛋白共同准备后的坐标及速度。膜的初始准备通常需要先处理近距离接触，再逐步减弱蛋白与脂质的限制，让水、头部和尾链逐渐适应彼此。本例从准备流程最后一个NPT阶段的保存状态继续，先运行20ps无位置限制的衔接段，再记录200ps。这样可以把注意力放在完整膜体系的分析。记录的起点因此是一个已有膜组织的状态，二百皮秒回答的是局部结构怎样波动；从分散脂质形成膜的过程，将在粗粒化章节用另一组实际轨迹观察。

组成表还说明了这个体系的层次。蛋白结构来自细菌外膜通道，周围却是已经明确指定的POPC环境；当前问题是该通道在这种脂质环境中的局部组织。若要讨论细菌外膜的整体通透性，还要建立相应的复杂脂质组成、两侧差异与溶液条件。另一方面，单一组分环境也有分析上的用途：当比较同一蛋白在不同脂质中的行为时，可以把脂质种类作为明确改变的变量，同时保留蛋白化学状态和温压设置。模型的简化因此应与所比较的问题一起表达。

## 膜有两个方向，盒子也要分别调整

把膜平面放在x、y方向，把穿过膜的法线放在z方向后，盒子的宽度与高度具有不同的物理含义。增大横向面积，会改变每一层里脂质与蛋白能够占据的空间；增大z方向长度，则主要改变膜外水层以及膜法线方向的间隔。对一盒近似均匀的水，同步缩放三个方向常是自然选择；对膜，让横向面积和法线尺寸分别响应压力，更容易表达这种方向差别。本例使用半各向同性压力耦合：x与y采用同一个缩放因子，z使用另一个。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s4)

图 3 · 半各向同性压力耦合的几何示意。x、y共享缩放因子，z独立；实际因子由压力耦合算法确定。

这里的“半各向同性”并不是把膜固定在原来大小。横向边长可以一起伸缩，法线方向也可以独立伸缩，所设定的是两组压力目标，各为1bar。体积由三个边长的乘积给出，投影面积由两个横向边长的乘积给出。一个只有一千分之一的横向线性变化，会同时作用于面积的两个方向，因此面积的相对变化约为千分之二。把边长、面积与体积放在同一个算例里，可以避免把长度变化直接当成面积变化。

盒长、面积与半各向同性缩放式 1

![盒长、面积与半各向同性缩放](https://ml-biomat.com/static/agent-math/61873ca8714f13c97d68c885.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Lₓ, Lᵧ, L𝓏 | 正交盒子沿三个方向的边长 | nm |
| A, A′ | 缩放前、后的膜面投影面积 | nm² |
| V, V′ | 缩放前、后的体积 | nm³ |
| s∥, s⊥ | 横向和法线方向的长度缩放因子 | 1 |
| ′, ∥, ⊥ | 撇号标记缩放后；平行于膜面、垂直于膜面的方向标记 | 1 |
| ² | 平方，即该因子乘自身 | 1 |
| =, ×, /, −, + | 相等、相乘、相除、相减、相加；相邻数量也表示相乘 | 1 |

怎样理解矩形面积是两边长之积，体积再乘高度；两个横向边都乘s∥，所以面积乘其平方。

算一个例子Lₓ=Lᵧ=10nm、L𝓏=8nm时，A=100nm²、V=800nm³。s∥=1.01、s⊥=0.99时，A′=102.01nm²，V′=807.9192nm³。

使用条件正交盒子，膜法线沿z；缩放因子用于几何算例。

压力控制器根据压力反馈改变盒子，分子仍然受到热运动和相互作用的共同影响。压力的瞬时波动可以比温度曲线显眼得多，因为它同时包含粒子运动与相互作用对体积变化的响应。当前记录在100到200ps内的平均温度为300.069K，逐点样本标准差为0.766K；同一时间段压力均值约为−1.60bar，逐点样本标准差约为119.71bar。这两个标准差描述保存记录的起伏，而不是均值的置信区间。对压力目标的统计判断，还要结合相关时间和更长的分段记录。

温度采用v-rescale控制，耦合时间为1ps；压力采用C-rescale，耦合时间为5ps。热浴对整个体系这一组原子进行温度控制，蛋白与膜、水与离子的质心平动则按既定分组处理。这些参数决定模型怎样与外部温度和压力环境交换能量、调整尺寸。对于初学者，先逐项读懂输入比一次改变许多参数更有效：明确哪些参数是温压目标，哪些是响应时间，哪些是数值步长，再比较修改后的真实轨迹。

### 20 ps衔接段的完整参数

```
;;Preprocessing
title                   = Production

;; no position constraints

;;Run and Output control
integrator              = md
dt                      = 0.002      ;0.002 ps or 2 fs
nsteps = 10000
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstcalcenergy = 100
nstenergy = 100
nstlog = 1000
;
nstcomm = 100
comm_mode               = linear
comm_grps               = SOLU_MEMB SOLV 

;;VdW
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

;;VdW
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw_switch             = 1.0
rvdw                    = 1.2

;;Electrostatics
coulombtype             = pme
rcoulomb                = 1.2

;;Bonds
constraints             = h-bonds
constraint_algorithm    = LINCS
continuation            = yes

;;Temperature coupling
tcoupl                  = V-rescale 
tc_grps                 = SYSTEM
tau_t                   = 1.0 
ref_t                   = 300

;;Pressure coupling is on
pcoupl                  = C-rescale 
pcoupltype              = semiisotropic
tau_p                   = 5.0
compressibility         = 4.5e-5  4.5e-5
ref_p                   = 1.0     1.0
refcoord_scaling        = com


; periodic boundary condition
;pbc                     = xyz       

ld-seed = 20263131
```

从准备状态继续；保留键长约束，释放位置限制。

### 200 ps生产记录的完整参数

```
;;Preprocessing
title                   = Production

;; no position constraints

;;Run and Output control
integrator              = md
dt                      = 0.002      ;0.002 ps or 2 fs
nsteps = 100000
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstcalcenergy = 100
nstenergy = 100
nstlog = 1000
;
nstcomm = 100
comm_mode               = linear
comm_grps               = SOLU_MEMB SOLV 

;;VdW
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

;;VdW
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw_switch             = 1.0
rvdw                    = 1.2

;;Electrostatics
coulombtype             = pme
rcoulomb                = 1.2

;;Bonds
constraints             = h-bonds
constraint_algorithm    = LINCS
continuation            = yes

;;Temperature coupling
tcoupl                  = V-rescale 
tc_grps                 = SYSTEM
tau_t                   = 1.0 
ref_t                   = 300

;;Pressure coupling is on
pcoupl                  = C-rescale 
pcoupltype              = semiisotropic
tau_p                   = 5.0
compressibility         = 4.5e-5  4.5e-5
ref_p                   = 1.0     1.0
refcoord_scaling        = com


; periodic boundary condition
;pbc                     = xyz       

ld-seed = 20263131
```

300 K、1 bar半各向同性、2 fs；每1 ps记录坐标。

完整运行脚本先把坐标、拓扑、索引和运行参数组合成二进制输入，再执行动力学，并按名称提取能量项。保存轨迹的间隔为1ps，保存能量的间隔为0.2ps；因此二百皮秒产生201幅坐标记录与1001个能量记录，均包含起点。重启衔接还会使用保存的状态文件，使速度与相关状态进入下一段。下面的脚本在已经包含准备输入的目录运行，输出的md.tpr、md.xtc和md-properties.xvg直接供本讲的分析程序读取。

### 完整运行与能量提取

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f pilot.mdp -c prepared.gro -t prepared.cpt -p topol.top -n index.ndx -o pilot.tpr > pilot.grompp.log 2>&1
"$gmx" mdrun -deffnm pilot -ntmpi 1 -ntomp 4 -pin off > pilot.stdout.log 2>&1
"$gmx" grompp -f md.mdp -c pilot.gro -t pilot.cpt -p topol.top -n index.ndx -o md.tpr > md.grompp.log 2>&1
"$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off > md.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

在含prepared.gro、prepared.cpt、topol.top、index.ndx和toppar的准备目录运行。

输入中的键长约束与准备时的位置限制也要分开理解。键长约束固定指定原子对的相对距离，让含氢键的快速伸缩不再作为自由振动被积分；位置限制则把选定原子拉向参考位置，影响它在空间中的移动。本段动力学保留含氢键长约束，释放准备阶段的位置限制。因而脂质和蛋白可以整体运动并改变许多内部角度，同时仍遵守已约束的键长。看到constraints这一行时，不应把整个分子理解成被钉在原处。

## 先找到两层，再定义面积和厚度

屏幕上的盒子边界只是周期空间的一种切法。膜整体稍微移动，某些分子就可能从盒子顶部离开、从底部进入；如果直接平均原始z坐标，两个本来相邻的位置可能被误算成相距很远。分析首先沿化学键逐段恢复完整分子，再为膜选取一致的中心。这里用两条尾链末端碳原子的周期圆平均定位膜中面。可以把z方向卷成一个圆：盒子的上下边界在圆上相接，相邻位置就不会因为写成零附近和盒长附近而被分开。

确定中面后，每个磷原子的高度都取相对中面的最近周期位移。正侧归为上叶片，负侧归为下叶片，第一次记录中的归属随后用于检查整段轨迹。这个体系实际有137个上叶片脂质和140个下叶片脂质，在201幅记录中归属保持一致。上下数量不相等并不自动意味着构建错误：嵌入的蛋白在两侧占据的截面可以不同，准备过程也要让各侧几何相容。统计时应保留实际数量，不能把277直接除以二再假装每侧都有138.5个分子。

把高度写在同一个膜中心附近式 2

![把高度写在同一个膜中心附近](https://ml-biomat.com/static/agent-math/c9a17b7e0182a21bcd7b88eb.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| zᵢ | 第i个原子的原始高度 | nm |
| z₀ | 选定的周期膜中面位置 | nm |
| L𝓏 | z方向盒长 | nm |
| δzᵢ | 相对中面的最近周期高度 | nm |
| i, 0 | 原子编号；中面参考标记 | 1 |
| round | 取最近整数，计算要加减几个盒长 | 1 |
| ( ), / | 括号分组；分数线表示除法 | 1 |
| =, ×, /, −, + | 相等、相乘、相除、相减、相加；相邻数量也表示相乘 | 1 |

怎样理解先算原子与中面的高度差，再减去最接近的整数个盒长，把它放到中面两边半盒长范围内。

算一个例子L𝓏=10nm、z₀=0.2nm、zᵢ=9.8nm：原始差9.6nm，round(0.96)=1，所以δzᵢ=−0.4nm。

使用条件正交周期盒子的z坐标；恰在半盒长边界时，两侧镜像等距。

膜厚度可以定义为上叶片磷原子平均高度减去下叶片的平均高度。这样得到的是磷酸头部两个平均平面的距离，通常记作头基间距。尾链疏水区域的厚度、两侧水密度达到某个数值的位置间距，以及电子密度曲线上两个峰的位置差，是相关但各有定义的量。头部会起伏，局部蛋白也会让周围界面变形，因此先把当前测量叫准确，再与采用相同定义的实验或模拟比较，能够减少“膜厚不一致”中的口径差异。

两个磷酸头部平均平面的距离式 3

![两个磷酸头部平均平面的距离](https://ml-biomat.com/static/agent-math/f5bbe5e6120a5b5899a95abf.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dPP | 上、下叶片磷原子平均高度之差 | nm |
| N₊, N₋ | 上、下叶片磷原子数，每个POPC有一个磷 | 1 |
| δzᵢ, δzⱼ | 相对同一膜中面的原子高度 | nm |
| i, j, +, − | 原子索引及所属上、下叶片的标记 | 1 |
| Σ, ∈ | 对指定叶片的所有原子求和；属于该集合 | 1 |
| 1 | 除以数量形成算术平均的常数一 | 1 |
| =, ×, /, −, + | 相等、相乘、相除、相减、相加；相邻数量也表示相乘 | 1 |

怎样理解先分别计算两组高度的平均，再相减；同一参考中面的平移在差中抵消。

算一个例子上叶片高度1.8、2.0nm，平均1.9nm；下叶片−2.0、−1.8、−1.9nm，平均−1.9nm；间距3.8nm。

使用条件两叶片明确、膜近似平面；测量磷原子平均平面间距。

在这段轨迹的100到200ps内，盒投影面积平均为139.065nm²，逐帧样本标准差为0.190nm²；磷酸平面间距平均为3.8516nm，逐帧样本标准差为0.0117nm。这两条曲线分别描述横向尺度和法线方向的组织。图中的蛋白RMSD则把1263个Cα原子整体平移、旋转对齐到本段第一幅构型，再计算位置差，后段均值约为0.0846nm。膜的几何变化与蛋白内部的局部变化由不同量表达，温度则提供同一段记录的热环境。

### 膜几何与同一段蛋白运动

真实0–200ps；浅色背景标记100–200ps统计区间。

官方1MAL/POPC准备模型；138195原子、三条421残基蛋白链、277 POPC。CHARMM参数包、300 K、1 bar半各向同性；20 ps衔接后记录200 ps，每1 ps保存坐标。

[下载参考数据与完整输入（ZIP） 110.85 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-membrane-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s5)

同一段0–200 ps轨迹中的投影面积、磷酸头部平面间距与三聚体Cα对齐RMSD；阴影为100–200 ps统计区间。

若把139.065nm²直接除以上叶片的137个脂质，会得到约1.015nm²。这个商把蛋白占据的面积也分给了脂质，所以应称作按脂质数分摊的总投影面积。对纯脂质平面双层，单叶片面积除以该叶片分子数常能给出平均分子面积；含蛋白时，还需要定义蛋白截面以及脂质可使用的面积。蛋白截面随高度改变，附近脂质的局部面积也可能不同，所以扣除面积的方法本身就是分析的一部分。下面的交互用一个已指定截面的几何模型，让这种区别直接显示出来。

蛋白截面怎样改变面积的分摊式 4

![蛋白截面怎样改变面积的分摊](https://ml-biomat.com/static/agent-math/7b7bd4af48baa5ee0ef32051.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| aℓ | 在所给蛋白截面定义下，单叶片可用面积除以脂质数 | nm² |
| atotal,ℓ | 总盒投影面积按该叶片脂质数分摊 | nm² |
| A | 整个盒子的膜面投影面积 | nm² |
| Aprot,ℓ | 在选定高度与规则下的蛋白占据截面 | nm² |
| Nℓ | 该叶片脂质分子数 | 1 |
| ℓ, prot, total | 叶片标签；蛋白占据部分；总面积标签 | 1 |
| =, ×, /, −, + | 相等、相乘、相除、相减、相加；相邻数量也表示相乘 | 1 |

怎样理解从总面积中扣除按同一平面定义的蛋白占据部分，剩余面积再分给脂质。

算一个例子几何例题：A=100nm²，Aprot,ℓ=20nm²，Nℓ=100，则aℓ=0.8nm²，而atotal,ℓ=1.0nm²。

使用条件占据面积需另行定义；本交互指定截面作算例，真实轨迹只报告总投影面积与实际叶片数。

[Figure: 指定蛋白占据部分后的几何面积分配](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s5)

指定蛋白截面的平面几何算例：比较总面积分摊与扣除占据部分后的面积分摊。

## 沿膜切薄片，看见水和脂质怎样分层

想知道膜中间究竟有哪些分子，可以把整个盒子沿z方向切成薄片。对每一片，分别把蛋白、脂质、水和离子的原子质量相加，再除以这一片的体积，就得到各组分的质量密度。它类似从一块多层蛋糕上逐片取样，只是这里每片厚0.1nm，而且分子不停运动。对许多时刻重复统计后，曲线展示的是这段观察时间里的平均分布。水在膜外较多、脂质集中在中间、蛋白跨越界面等信息，会在同一个坐标系里显现。

先按薄片体积归一，再对时间平均式 5

![先按薄片体积归一，再对时间平均](https://ml-biomat.com/static/agent-math/a1aaec612369a18c2bb27e89.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρ̄b | 第b片的时间平均质量密度 | kg m⁻³ |
| M, t | 保存帧数和帧索引 | 1 |
| b(t), i∈b(t) | 第t帧落在该相对高度薄片中的原子集合及其中的原子 | 1 |
| mᵢ | 原子i的质量；代入此SI表达式时用kg | kg |
| Aₜ | 第t帧的盒投影面积；SI表达式用m² | m² |
| Δz | 固定薄片厚度；SI表达式用m | m |
| Σ, /, =, 1 | 求和、相除、相等、常数一；相邻量相乘 | 1 |
| b, Δ, ¯ | 薄片标签、宽度标记、平均标记 | 1 |

怎样理解质量除以体积给出密度，薄片体积为该帧面积乘厚度；把每帧密度相加再除以帧数。

算一个例子一帧薄片含3000u质量，面积140nm²，厚0.1nm，密度=(3000/14)×1.660539=355.830kg m⁻³。1u=1.66053906660×10⁻²⁷kg，1nm³=10⁻²⁷m³。

使用条件每帧按同一膜中心定义对齐；先按各帧体积归一化，适用于这里变化的正交盒子。

每一帧都先按膜中面对齐，再把相对高度放入固定宽度的小格。这样，整片膜沿盒子方向的平移不会被误当成界面变厚。与此同时，NPT盒子的横向面积在变化，每帧薄片体积都要用该帧面积乘以0.1nm，而不能始终使用第一帧的体积。程序在相对中面−4.5到4.5nm内绘图，范围位于所有帧的半盒高度以内。它分别归一化每帧的质量，再对100到200ps的101幅构型取平均，确保“平均密度”的计算顺序清楚。

### 质量密度与头部位置

相对周期膜中面，固定0.1nm薄片；100–200ps共101帧平均。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s6)

先按每帧周期膜中面平移，再在0.1 nm薄片中累计质量，以该帧面积乘薄片厚度归一化；平均101帧。

图中水的质量密度在膜外接近一千千克每立方米，靠近脂质内部后明显降低；蛋白曲线穿过膜中部，并在一侧向水层延伸，体现通道结构的空间不对称。膜中心仍然出现少量水密度，需要结合三维位置理解：对整个横向面积取平均时，通道内的水与脂质区域的水被放进同一薄片。要研究水究竟沿哪个孔道出现，可以进一步把薄片限制在某个通道附近，或者画二维横向分布。一个一维平均把信息整理得更清楚，也同时合并了横向位置差异。

右侧只统计磷原子的数量，并除以薄片体积，因此纵轴单位是每立方纳米的原子数。磷原子是定位脂质头部的标记，曲线显示两个分开的峰；峰的宽度来自头部高度的分散、局部起伏和时间变化。两边峰高不必相等，因为分子数、空间分布和局部环境都可能不同。这个数密度与左侧质量密度采用不同权重，不能直接比较纵轴大小；能比较的是它们在同一高度上是否同时出现，以及峰的位置与头基间距怎样对应。

密度曲线还可以帮助选择后续问题。如果某个添加分子主要分布在水层与头部交界处，可以围绕界面停留与接触设计分析；如果它进入疏水区域，则应查看进入深度、朝向和附近脂质排列。若研究膜曲率很大或膜面形成长波起伏，全局z方向薄片会把不同局部高度叠在一起，此时需要局部中面与局部法线。当前平面膜和短时间记录适合先建立全局坐标分析，再把空间分辨率提高到问题所需的程度。

## 尾链怎样排列，为什么一个角度还不够

POPC的两条尾链化学结构不同：一条为含十八个碳并具有顺式双键的油酰链，另一条为十六碳的饱和棕榈酰链。顺式双键限制相邻部分的几何，通常使链的局部形状与饱和链不同；整条链同时还受到周围脂质、蛋白和热运动影响。观察结构时，先区分这些化学身份，再讨论哪一段更弯、哪条链更倾斜。把两条尾链都画成等长直线可以帮助认识双层，却无法表达本例中所有与构象有关的细节。

这里用一个容易理解的整体量描述方向：从尾链的羰基碳指向末端碳，画一根端到端箭头，再测它与z方向的夹角。箭头几乎沿法线时，链在这个意义上朝膜内部伸展；箭头偏向膜面时，整体方向更倾斜。由于上下叶片的尾链方向相反，直接平均带正负号的余弦会让两侧互相抵消。把余弦平方后再做适当平移和缩放，就能让平行与反平行法线的链具有相同取向值，同时把随机三维方向的平均设为零。

尾链整体轴相对膜法线的取向式 6

![尾链整体轴相对膜法线的取向](https://ml-biomat.com/static/agent-math/1c1e99943c77eda7ae0a4d6a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| S | 本帧的链轴取向平均值 | 1 |
| N, i | 参与平均的尾链数和链索引 | 1 |
| θᵢ | 羰基碳到末端碳的向量与z轴的夹角 | rad；算例用° |
| cos, ² | 余弦；先求余弦再平方 | 1 |
| Σ | 把每条链的取向值相加 | 1 |
| 1, 2, 3 | 使沿法线为1、随机三维方向平均为0的常数 | 1 |
| =, ×, /, −, + | 相等、相乘、相除、相减、相加；相邻数量也表示相乘 | 1 |

怎样理解平方让上下叶片相反方向等价；随机三维方向的cos²均值为1/3，代入后为零。

算一个例子每条轴θ=60°时，cosθ=0.5，S=(3×0.25−1)/2=−0.125。θ=0°或180°时S=1，θ=90°时S=−0.5。

使用条件测量整条尾链端到端轴；逐个C—H键的链段序参数需要另外选取向量。

该取向参数在完全沿法线时为一，在完全位于膜面内时为负二分之一。它的零点有一个具体几何原因：对于均匀分布在三维空间的方向，三个坐标方向的余弦平方平均相同，且它们相加为一，所以每个平均为三分之一。代入公式便得到零。要注意，零值也可能由几类特定方向混合得到，因此解释分布时可以同时查看角度直方图。平均取向把许多方向压成一个数，适合比较，但完整方向分布仍然提供更多结构信息。

### 尾链取向和压力波动

每帧277条同类尾链取平均；压力记录来自原始能量输出。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/#zh-s7)

各类尾链的羰基碳—末端碳轴相对膜法向的二阶取向参数，与原生能量记录中的瞬时压力。

这段记录后半段的油酰链轴取向平均为0.5295，棕榈酰链为0.5449；逐帧样本标准差分别为0.0068和0.0063。两组数字来自277个脂质在每帧的平均，再对101帧统计。它们描述的是整条尾链端到端轴相对膜法线的取向，不能直接代入逐个碳氢键定义的氘序参数。若要与核磁共振中的链段取向比较，应选定相应C—H方向，采用匹配的角度、平均和符号约定，逐个碳位置绘图。测量定义相同，比较才有明确对象。

两个取向均值接近，却没有让两条链成为同一种结构。它们可能在不同位置弯曲，有不同的端到端长度，也可能通过不同局部构象产生相似整体方向。类似地，膜厚度几乎稳定时，尾链仍可以快速交换局部构象；温度围绕目标波动时，较慢的横向重排也可以继续进行。把取向、厚度、密度和三维结构一起阅读，可以把这些运动分开。二百皮秒内的记录支持当前准备状态附近的这些局部描述，扩展到长期侧向扩散或脂质重排，需要相应更长的位移记录与重复。

计算取向时，先对每条链的余弦平方取值，再对所有链求平均，顺序也有物理含义。假设一半箭头向上、一半向下，直接把箭头相加会得到零向量；每条箭头却都沿膜法线排列，当前取向参数应该是一。类似地，先平均角度再取余弦平方，一般不会等于先逐条计算后平均。程序保留每条链的身份，在同一帧中逐条构造方向并计算，再汇成帧平均。这个例子也提醒我们，非线性的几何运算与平均常常不能随意交换。

## 让结构图、曲线和完整代码回答同一个问题

分析程序从同一套拓扑读取原子名称、质量、残基和化学键，再逐帧处理轨迹。它不会凭屏幕上的距离猜测哪些原子相连，而是沿明确的键图恢复整条分子，并检查每条恢复后的共价键长度。对于三聚体，先恢复各条蛋白链，再把三条链放到相邻的周期镜像中，进行一次整体Cα对齐；对于脂质，利用相同的POPC键图同时处理277个分子。这样，显示边界的选择就与真实内部几何分开，膜厚、尾链方向和蛋白RMSD各自使用合适的坐标表示。

### 完整膜几何、密度与取向分析

```
"""Measure a membrane-protein trajectory in its membrane coordinate frame.

python analyze_membrane.py --records records --out analysis --language en
Inputs: md.tpr, md.xtc, md-properties.xvg. Dependencies: MDAnalysis, NumPy,
Matplotlib. Coordinates are converted from angstrom to nm explicitly.
"""
from pathlib import Path
import argparse
import csv
import json
import re
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def xvg(path):
    legends = {}
    rows = []
    for line in path.read_text().splitlines():
        found = re.search(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
        if found:
            legends[int(found[1])] = found[2]
        if line.strip() and not line.startswith(("@", "#")):
            rows.append([float(x) for x in line.split()])
    values = np.asarray(rows)
    return {"time": values[:, 0], **{label: values[:, i+1] for i, label in legends.items()}}


def bond_plan(group):
    local = {int(x): i for i, x in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                seen.add(b); queue.append(b); plan.append((a, b, k, sign))
    if len(seen) != len(group):
        raise ValueError("A molecule selection must have one connected bond graph")
    return edges, plan


def restore_batch(raw, edges, plan, box):
    """Traverse every bond; raw has shape (molecules, atoms, 3), in angstrom."""
    vectors = raw[:, edges[:, 1]] - raw[:, edges[:, 0]]
    vectors = minimize_vectors(vectors.reshape(-1, 3), box).reshape(vectors.shape)
    whole = np.empty_like(raw, dtype=float)
    whole[:, 0] = raw[:, 0]
    for parent, child, k, sign in plan:
        whole[:, child] = whole[:, parent] + sign*vectors[:, k]
    actual = whole[:, edges[:, 1]] - whole[:, edges[:, 0]]
    if np.max(np.linalg.norm(actual-vectors, axis=2)) > .005:
        raise ValueError("Bond-cycle reconstruction differs by more than 0.005 angstrom")
    maximum = np.linalg.norm(actual, axis=2).max()/10
    if maximum > .25:
        raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
    return whole/10, float(maximum)


def circular_center(z, length):
    phase = np.mean(np.exp(2j*np.pi*z/length))
    if abs(phase) < .2:
        raise ValueError("Tail markers do not define one localized membrane midplane")
    return float(np.angle(phase)*length/(2*np.pi) % length)


def wrap(dz, length):
    return (dz+length/2) % length-length/2


def fit_rmsd(moving, reference):
    moving = moving-moving.mean(axis=0)
    target = reference-reference.mean(axis=0)
    left, _, right = np.linalg.svd(moving.T@target)
    correction = np.eye(3); correction[-1, -1] = np.linalg.det(left@right)
    return float(np.sqrt(np.mean(np.sum((moving@left@correction@right-target)**2, axis=1))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    u = mda.Universe(str(args.records/"md.tpr"), str(args.records/"md.xtc"))
    lipid = u.select_atoms("resname POPC")
    groups = [u.select_atoms(s) for s in ["protein", "resname POPC", "resname TIP3", "resname SOD CLA"]]
    assert [len(x) for x in groups] == [19260, 37118, 81612, 205]
    residues = lipid.residues
    assert len(residues) == 277 and all(len(r.atoms) == 134 for r in residues)
    edges, plan = bond_plan(residues[0].atoms)
    for residue in residues:
        assert np.array_equal(bond_plan(residue.atoms)[0], edges)
    names = residues[0].atoms.names.tolist()
    P, tail1, tail2, start1, start2 = [names.index(n) for n in ["P", "C218", "C316", "C21", "C31"]]
    protein_segments = groups[0].segments
    protein_plans = [bond_plan(s.atoms) for s in protein_segments]
    ca_local = [np.flatnonzero(s.atoms.names == "CA") for s in protein_segments]
    bins = np.linspace(-4.5, 4.5, 91)
    mass_profiles = np.zeros((4, 90))
    phosphate_profile = np.zeros(90)
    records = []; late_frames = 0; maximum_bond = 0.
    for frame, ts in enumerate(u.trajectory):
        box_nm = ts.dimensions[:3]/10
        if not np.allclose(ts.dimensions[3:], 90) or box_nm[2]/2 < 4.5:
            raise ValueError("This analysis expects an orthogonal box with Lz >= 9 nm")
        whole, longest = restore_batch(lipid.positions.astype(float).reshape(277, 134, 3), edges, plan, ts.dimensions)
        maximum_bond = max(maximum_bond, longest)
        z0 = circular_center(whole[:, [tail1, tail2], 2].ravel(), box_nm[2])
        pz = wrap(whole[:, P, 2]-z0, box_nm[2])
        if frame == 0:
            upper = pz > 0
        if np.any((pz > 0) != upper):
            raise ValueError("A phosphate changes assigned leaflet; inspect that event")
        thickness = pz[upper].mean()-pz[~upper].mean()
        order = []
        for start, end in [(start1, tail1), (start2, tail2)]:
            v = whole[:, end]-whole[:, start]
            cos = v[:, 2]/np.linalg.norm(v, axis=1)
            order.append(float(np.mean((3*cos*cos-1)/2)))
        cas = []
        for segment, (pe, pp), indices in zip(protein_segments, protein_plans, ca_local):
            protein, longest = restore_batch(segment.atoms.positions.astype(float)[None], pe, pp, ts.dimensions)
            maximum_bond = max(maximum_bond, longest)
            ca = protein[0, indices]
            if cas:
                ca -= np.rint((ca.mean(axis=0)-cas[0].mean(axis=0))/box_nm)*box_nm
            cas.append(ca)
        ca = np.concatenate(cas)
        if frame == 0:
            reference = ca.copy()
            snapshot = {"box_nm": box_nm.tolist(), "ca_nm": ca.tolist(),
                        "lipid_P_nm": whole[:, P].tolist(),
                        "lipid_tail_nm": whole[:, [tail1, tail2]].tolist(),
                        "midplane_nm": z0, "upper_leaflet": upper.tolist()}
        records.append([float(ts.time), float(box_nm[0]*box_nm[1]), float(box_nm[2]),
                        float(thickness), order[0], order[1], fit_rmsd(ca, reference)])
        if ts.time >= 100:
            late_frames += 1
            volume_slice = box_nm[0]*box_nm[1]*(bins[1]-bins[0])
            for k, group in enumerate(groups):
                z = wrap(group.positions[:, 2]/10-z0, box_nm[2])
                mass_profiles[k] += np.histogram(z, bins, weights=group.masses)[0]/volume_slice*1.66053906660
            phosphate_profile += np.histogram(pz, bins)[0]/volume_slice
    a = np.asarray(records)
    assert len(a) == 201 and np.allclose(a[:, 0], np.arange(201)) and late_frames == 101
    mass_profiles /= late_frames; phosphate_profile /= late_frames
    columns = ["time_ps", "projected_area_nm2", "Lz_nm", "phosphate_plane_distance_nm",
               "oleoyl_axis_order", "palmitoyl_axis_order", "trimer_CA_RMSD_nm"]
    with (args.out/"membrane_observations.csv").open("w", encoding="utf8", newline="") as handle:
        writer = csv.writer(handle); writer.writerow(columns); writer.writerows(records)
    energy = xvg(args.records/"md-properties.xvg")
    stats = lambda v: {"mean": float(np.mean(v)), "frame_sd": float(np.std(v, ddof=1))}
    summary = {"frames": len(a), "time_ps": [0, 200], "profile_frames": late_frames,
               "leaflet_counts": {"upper": int(sum(upper)), "lower": int(sum(~upper))},
               "late_100_200ps": {key: stats(a[a[:, 0] >= 100, i]) for i, key in enumerate(columns) if i},
               "energy_100_200ps": {key: stats(v[energy["time"] >= 100]) for key, v in energy.items() if key != "time"},
               "maximum_reconstructed_bond_nm": maximum_bond,
               "density_definition": "Mass in fixed 0.1 nm slabs divided by instantaneous xy area times slab width; mean over 101 frames. Window -4.5 to4.5 nm about circular tail-terminal midplane.",
               "orientation_definition": "P2 of each carbonyl-carbon to terminal-carbon chain axis versus z; distinct from segmental C-H deuterium order.",
               "rmsd_definition": "All 1263 C-alpha atoms, equal weights, one proper rigid fit to first local production frame."}
    (args.out/"membrane_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf8")
    (args.out/"membrane_snapshot.json").write_text(json.dumps(snapshot)+"\n", encoding="utf8")
    np.savez(args.out/"membrane_profiles.npz", z_nm=(bins[1:]+bins[:-1])/2,
             mass_density_kg_m3=mass_profiles, phosphate_number_density_nm3=phosphate_profile)
    tr = lambda zh, en: zh if args.language == "zh" else en
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [f for f in fonts if f in installed] if args.language == "zh" else ["DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#faf8f2", "axes.facecolor": "#faf8f2"})
    colors = ["#995a42", "#177e89", "#537dbb", "#9067a0"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}.svg"); fig.savefig(args.out/f"{name}.png", dpi=150); plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), constrained_layout=True)
    for ax, i, label in zip(axes.flat, [1, 3, 6], [tr("盒投影面积 / nm²", "Projected box area / nm²"),
                           tr("磷酸平面间距 / nm", "Phosphate-plane distance / nm"), tr("三聚体 Cα RMSD / nm", "Trimer Cα RMSD / nm")]):
        ax.plot(a[:, 0], a[:, i], color=colors[i % 4]); ax.set_ylabel(label)
    axes[1, 1].plot(energy["time"], energy["Temperature"], color=colors[2], lw=.8)
    axes[1, 1].axhline(300, color="#777", ls="--", lw=1); axes[1, 1].set_ylabel(tr("温度 / K", "Temperature / K"))
    for ax in axes.flat:
        ax.set_xlabel(tr("本段记录时间 / ps", "Local production time / ps")); ax.axvspan(100, 200, color="#e2e9dc", alpha=.4); ax.grid(alpha=.15)
    fig.suptitle(tr("膜、蛋白与水共同运动：0–200 ps", "Membrane, protein and water: 0–200 ps"), fontsize=19)
    save(fig, "membrane-geometry")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), constrained_layout=True)
    z = (bins[1:]+bins[:-1])/2
    for density, color, label in zip(mass_profiles, colors, [tr("蛋白", "Protein"), "POPC", tr("水", "Water"), tr("离子", "Ions")]):
        axes[0].plot(z, density, color=color, label=label, lw=2)
    axes[1].plot(z, phosphate_profile, color=colors[1], lw=2)
    axes[0].set_ylabel(tr("质量密度 / kg m⁻³", "Mass density / kg m⁻³")); axes[0].legend(frameon=False)
    axes[1].set_ylabel(tr("磷原子数密度 / nm⁻³", "Phosphorus number density / nm⁻³"))
    for ax in axes:
        ax.set_xlabel(tr("相对膜中面的位置 / nm", "Position relative to membrane midplane / nm")); ax.axvline(0, color="#888", ls=":"); ax.grid(alpha=.15)
    fig.suptitle(tr("沿膜法线切薄片：100–200 ps 的平均分布", "Slices along the membrane normal: mean over 100–200 ps"), fontsize=18)
    save(fig, "membrane-profiles")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), constrained_layout=True)
    for i, label, color in [(4, tr("油酰链端到端轴", "Oleoyl chain axis"), colors[0]), (5, tr("棕榈酰链端到端轴", "Palmitoyl chain axis"), colors[1])]:
        axes[0].plot(a[:, 0], a[:, i], color=color, label=label, lw=1.5)
    axes[0].set(xlabel=tr("本段记录时间 / ps", "Local production time / ps"), ylabel=tr("链轴取向参数 S", "Chain-axis order S")); axes[0].legend(frameon=False, fontsize=11)
    axes[1].plot(energy["time"], energy["Pressure"], color=colors[3], lw=.8)
    axes[1].axhline(1, color="#777", ls="--"); axes[1].set(xlabel=tr("本段记录时间 / ps", "Local production time / ps"), ylabel=tr("瞬时平均压力 / bar", "Instantaneous mean pressure / bar"))
    for ax in axes: ax.grid(alpha=.15)
    fig.suptitle(tr("局部取向与整体热力学量的不同变化", "Local orientation and a fluctuating thermodynamic observable"), fontsize=18)
    save(fig, "membrane-orientation")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

读取md.tpr、md.xtc与md-properties.xvg；输出三组双语图和逐帧数据。

代码输出三组图、逐帧CSV、数值摘要和密度数组。几何图包含投影面积、头基间距、蛋白RMSD与温度；剖面图把质量密度与磷原子数密度分开；取向图则同时保留两条尾链的结果与压力波动。图中的浅色背景标出100到200ps统计窗口。能量记录每0.2ps保存一次，坐标每1ps保存一次，所以同一个时间区间内两类统计的样本数不同。程序分别按各自实际时间选择数据，避免把第几个保存点误当成统一的物理时刻。

读者可以从两个小改动继续练习。把密度格宽从0.1nm改成0.2nm，峰形通常会更平滑，但细节也会被合并；把统计窗口改成前一百皮秒，则能观察这一短段中几何量和分布是否随时间改变。这样的练习只改变分析定义，原来的轨迹保持同一份。比较前应写清新的格宽、窗口与原子选择，随后检查两个版本之间的差异来自哪里。更平滑的曲线表示采用了更粗的空间统计，并不自动说明分子运动更稳定。

回到生物材料的问题，一层膜的作用来自不同分子的共同组织。脂质把水环境与疏水内部连接起来，蛋白占据局部空间并提供通道，离子响应带电原子周围的环境。当前例题让这些组分在同一模型中运动，再用清楚的几何和统计定义读出它们的位置与变化。研究新的配方时，可以先保持温度、力场体系、蛋白状态和分析方式一致，再有目的地改变某一种脂质或添加分子，安排独立重复，把差异与具体化学变化联系起来。

接下来的聚合物章节会把目光转向一条链在水中的伸展与蜷缩；随后，我们再把聚合物接到膜上，研究链密度如何改变界面外侧的空间组织。本讲留下的坐标习惯会继续使用：先确定膜中面和朝外方向，再测链离膜面的高度；先保留真实叶片数与面积，再计算每侧的接枝密度。把这些定义贯穿起来，膜、聚合物和水就能在同一幅可计算的界面图景中相遇。

## 延伸阅读与开放资料

- [A Beginner’s Guide to Perform Molecular Dynamics Simulation of a Membrane Protein using GROMACS](https://tutorials.gromacs.org/docs/membrane-protein.html) · Farzaneh Jalalypour, Maryam Majdolhosseini, Alessandra Villa · CC BY 4.0; archived tutorial and supplied inputs

  1MAL/POPC模型、完整CHARMM拓扑、分阶段准备及修订生产参数。

  从公开最终准备状态起步，GROMACS 2026.4运行20ps衔接与200ps记录；新增叶片、面积、密度和取向分析，完整双语解释与图。
- [1MAL: Structural basis for sugar translocation through maltoporin channels](https://www.rcsb.org/structure/1MAL) · T. Schirmer, T. A. Keller, Y. F. Wang, J. P. Rosenbusch · PDB structural data: CC0; original article cited for scientific context

  三聚体实验结构身份、3.10Å分辨率与通道背景。

  采用膜中准备后的模型；结构图使用本例实际记录。
- [On bimolecular layers of lipoids on the chromocytes of the blood (1925)](https://doi.org/10.1084/jem.41.4.439) · E. Gorter and F. Grendel · Historical article citation; new conceptual illustration

  脂质单层面积与细胞表面积比较的历史问题。

  用分子数与覆盖面积的几何图解释推理。
- [The fluid mosaic model of the structure of cell membranes (1972)](https://doi.org/10.1126/science.175.4023.720) · S. J. Singer and G. L. Nicolson · Research citation; independently drawn conceptual diagram

  蛋白与流动脂质共同组织的历史视角。

  联系膜内蛋白与局部脂质排列。
- [GROMACS 2026.4: gmx density](https://manual.gromacs.org/2026.4/onlinehelp/gmx-density.html) · GROMACS development team · Official documentation citation

  相对膜中心的密度、周期与尺寸波动问题。

  给出固定宽度薄片、逐帧体积归一的完整Python实现。
