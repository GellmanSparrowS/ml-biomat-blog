# 拉伸与松弛：从分子读出力学

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l10/
Language: zh-CN

从盒子形变到压力张量，把网络拉伸、链取向和固定形变后的调整联系起来。

## 拉长以后再停住，材料还在做什么

把一条橡皮筋拉长，保持双手之间的距离，再感受维持这个长度需要多大的力。距离固定以后，材料内部仍可能继续调整。水凝胶敷料贴在活动部位、弹性密封圈受到长期挤压、软组织被拉伸时，都涉及类似的问题：外面的形状已经规定，里面的链段是否还在运动，传递的力又怎样随时间改变？本讲把这件事变成一个可观察的分子模拟。我们会先缓慢改变周期盒子的形状，再把盒子固定下来，同时记录链的形状与体系的受力统计，从内部结构的调整理解宏观响应的来由。

上一讲已经准备了三种连接程度的珠簧体系。它们都有一千六百颗等质量珠子，八十条原始链，每条二十颗珠子；区别在于新增了零、八十或一百六十条永久连接。每一种条件有三组独立准备的初始构型。本讲沿用这些实际体系，不再重新挑选一张更好看的网络。这样，连接图、局部结构和后面的力学曲线可以一一对应。零新增连接的体系也参与相同加载，它让我们观察：即使没有跨链永久键，密集链的运动和相互作用仍会在有限加载时间内产生响应。

还有一个容易混淆的地方是力与应力。力描述整个试样受到多大的拉拽，应力则把这个作用按面积分配。同样的力作用在细线和粗绳上，内部承担的单位面积载荷不同；比较材料时，需要把试样尺寸带来的影响区分开。模拟中的全局压力张量已经按盒子体积归一化，它与单个珠子受到的力也不是同一种量。因此我们先从整块材料的几何与平均作用出发，再回到链段解释它们怎样产生。这样安排，既能连接实验测量，也能避免把微观某个特别大的瞬时力误认为整个网络的强度。

“拉伸”首先是一个操作条件，而不是一条材料定律。我们要规定沿哪个方向拉、拉多快、横向能否收缩以及温度如何控制。实验中的细长试样可以在自由侧面自然变细，周期盒子则没有这样一圈自由表面，需要明确告诉程序横向盒长怎样变化。本例沿x方向把盒长增加到原来的1.2倍，同时让y和z方向按相同比例收缩，保持总体积不变。这种设置把密度变化与形状变化分开，适合学习近似不可压缩网络的变形。若研究材料在拉伸时的体积变化，就要改用与那个问题对应的横向约束。

最后要读出的量，也需要先说清。轨迹告诉我们珠子怎样排列，盒长告诉我们规定了多大的形变，压力张量则提供不同方向上的机械作用。把这些量放在同一时间轴上，可以区分加载阶段与固定形变后的阶段。本讲会从最容易手算的长度比出发，逐步解释应变、横向收缩、拉伸应力差、链取向和时间平均。实际小体系的应力有明显起伏，三组构型都保留在图里。理解这些起伏与结构信号的关系，本身就是从“运行了一个拉伸命令”走向“解释了一次材料比较”的关键一步。

## 从力和长度，走到热运动与链的形状

弹性最直观的图像是一根弹簧：拉开它的两端，需要施加回复力。这个图像对理解局部键长很有帮助，但高分子网络还多了一层结构。一段卷曲的链可以先改变弯曲方式和空间方向，使两端相距更远，而不必让每一条化学键都显著变长。把一串松散摆放的珠子慢慢展开，就能看见这种区别。网络的整体伸长由许多链段的方向、构象和局部距离共同承担，因此我们既记录局部键的方向，也记录整条原链在三个方向上的尺寸。只看最长的一条键，会遗漏大量发生在更大尺度上的调整。

把形变与热联系起来，是理解弹性的另一条历史线索。高夫在1805年发表了关于天然橡胶性质的研究；焦耳在1859年的《论固体的某些热力学性质》中，把机械变化与热效应放到同一个研究框架中。早期研究面对的是可以夹持、加载和测温的材料，而今天的模拟能够进一步查看内部的链。图中把这两种观察连接起来：左边记录外部长度、作用力和温度，右边查看链段可采取的形状。这样的联系提醒我们，讨论橡胶或凝胶的回复时，温度和构象分布都是问题的一部分。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s2)

图 1 · 弹性研究把外部加载、尺寸与温度联系起来；现代分子图像进一步追踪内部链的构象。左侧为这些测量关系的概念示意。

用现代分子图像来想，一段两端靠近的柔性链通常能采取许多卷曲方式；把两端拉远后，可用的形状会受到更多限制。热运动持续探索这些形状，所以形状的数量也会影响平均回复趋势。这就是理解构象熵的一种入口：“熵”在这里与满足约束的微观排列数量有关，而不是画面看起来整齐与否。真正的网络还包含排斥、连接点涨落和有限伸长等因素。本讲的FENE珠簧模型把弹簧能量、珠子排斥和热运动一起保留，因而可以观察整体尺寸变化如何分配到局部键与链构象上。

温度控制也因此要和加载方式一起说明。如果在固定温度下拉伸，热浴会与体系交换能量，使链始终在规定的热环境中运动；如果希望研究快速变形造成的温升，就需要设计相应的能量交换条件和测温方法。本例持续使用T*=1的Langevin热浴，阻尼时间为一τ，关注这个热环境下的结构与力学响应。温度曲线会检查实际运动统计是否围绕目标值波动，而链形状曲线进一步说明材料内部正在怎样改变。两张图各自回答一个问题，不能用温度稳定代替对结构调整的观察。

时间尺度决定了这些内部变化有多少机会发生。局部键振动通常比整条链改变形状快，网络接点之间的长链段还可能需要更长时间重新安排。想象把一团松散的线快速拉开，再慢慢拉开：在后一个过程中，线有更多时间调整位置。分子体系中的热运动为这种调整提供了持续的微观运动来源，所以同一最终长度可以通过不同速度到达，并留下不同的结构与应力。分析时把加载时间写在伸长比旁边，能让读者立即看见这个实验包含了多少内部调整时间。

## 应变是怎样从盒长中算出来的

先选定加载开始时的长度作为参照。如果盒子沿x方向原长十个长度单位，后来变成十二个，那么伸长比就是十二除以十，等于1.2；工程应变则是增加的两份长度除以原长，等于0.2。应变没有长度单位，因为分子和分母使用同一种单位。这样的写法方便比较不同大小的试样：两毫米增加到二点四毫米，与两厘米增加到二点四厘米，工程应变相同。它们的实际伸长量不同，材料受到的相对几何变化却可以放在同一个尺度上讨论。

伸长比、工程应变与对数应变式 1

![伸长比、工程应变与对数应变](https://ml-biomat.com/static/agent-math/fffc4df63ffaf3521633a239.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| λ | 沿x方向的伸长比 | 1 |
| Lₓ | 当前x方向盒长 | σ |
| Lₓ₀ | 加载开始时的x方向盒长 | σ |
| e | 相对初始长度的工程应变 | 1 |
| h | 对数应变，又称Hencky应变 | 1 |
| ln | 自然对数，作用于正的无量纲伸长比 | 1 |
| =, /, −, 1 | 相等、相除、相减、常数一；下标0表示参考状态 | 1 |

怎样理解长度相除得到相对变化尺度，减去一得到相对于原长增加的比例；自然对数对应按当前长度逐步累计的小应变。

算一个例子原长10σ、当前12σ时，λ=1.2，e=0.2，h=ln1.2≈0.182322。

使用条件长度保持正值；本例沿固定x轴加载，并明确使用加载开始时的盒长作参照。

还有一种常用量叫对数应变。它把许多小的伸长按当时已有的长度逐次累计，最后得到伸长比的自然对数。对于1.2倍伸长，工程应变为0.2，对数应变约为0.1823。小形变时二者很接近，形变增大以后区别逐渐明显。计算机输入中也区分恒定工程应变率与恒定对数应变率：前者让长度随时间线性增长，后者让长度按相同比例不断增长。本例用scale设置最终盒长，LAMMPS在加载时间内线性改变x长度，因此对应恒定工程应变率。读图时，应变定义要与实际输入一致。

横向收缩可以从体积守恒直接算出。正交盒子的体积是三个边长的乘积；若x变成原来的λ倍，y与z都变成原来的a倍，那么体积比例就是λ乘a的平方。保持体积要求这个乘积为一，因此a等于λ的负二分之一次方。λ为1.2时，两个横向长度各变成约0.9129倍，横截面积变为原来的六分之五。这里的收缩是我们施加的几何条件。它与让横向压力自动调整到某个目标值是两种不同实验安排，读者可以依据材料是否受到横向约束来选择相应方案。

等体积、对称横向收缩式 2

![等体积、对称横向收缩](https://ml-biomat.com/static/agent-math/402c2fd71657a1d7748c5376.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Lᵧ, L𝓏 | 当前y与z方向盒长 | σ |
| Lᵧ₀, L𝓏₀ | 参考y与z方向盒长 | σ |
| λ | x方向伸长比 | 1 |
| V, V₀ | 当前与参考盒子体积 | σ³ |
| J | 体积比 | 1 |
| −1/2 | 先取平方根再取倒数 | 1 |
| =, /, 1 | 相等、相除、常数一；相邻量相乘 | 1 |

怎样理解正交盒子的体积是三个长度的乘积。两个横向方向保持相同相对缩放时，λ乘横向缩放的平方应等于一。

算一个例子λ=1.2时，两个横向比均为1/√1.2≈0.912871，体积比1.2×0.912871²≈1。

使用条件这是本例施加的等体积几何协议；横向按相同比例缩放，并保留原y/z长宽比。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s3)

图 2 · 等体积加载的几何关系：轴向伸长比为λ，两个横向比各为λ的负二分之一次方。

[Figure: 盒子几何变化](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s3)

几何映射练习：初始三个边长都是10σ，点保留各自分数位置。

用同一轴向伸长比较两种横向约束，直接观察面积、体积和应变定义。

这组模拟先固定盒子一百τ，再用一百τ把x长度从一倍增加到1.2倍，最后保持一百τ。加载段的工程应变率因此是0.2除以一百τ，即每τ增加0.002。每一步的盒长都保存在实际输出中，分析直接从这些数值计算伸长比，并检查三个边长的乘积。这样的检查比只读输入文件更进一步：输入规定了目标，输出说明程序在记录时刻实际使用了什么几何状态。时间轴上的一百τ和二百τ分别标出加载开始与结束，后面所有结构和应力曲线都沿用这两个阶段边界。

可以用一个简单的对照熟悉应变率：最终仍增加百分之二十，但把加载时间从一百τ改为二百τ，工程应变率就减半。最终几何相同，链段在加载中可以调整的时间却增加了一倍。这个对照适合研究速度的影响；如果同时改变最终伸长、链长和温度，看到曲线变化后就需要更多比较才能区分各自作用。实际研究通常先固定材料结构和热环境，逐项改变一个加载条件。图中的横轴也要随问题选择：比较不同速度到达同一形变时可用应变轴，观察保持过程则使用停止加载后的经过时间。

## 用周期盒子加载，珠子怎样跟着变化

本例的核心命令是fix deform，其中x scale 1.2指定最终x长度，y volume和z volume让两个横向尺寸共同维持体积。remap x则在每次盒子更新时，把珠子位置按同样的几何比例映射到新盒子。这个词容易被误读：x在这里代表坐标映射方式，映射会按照盒子改变的所有方向处理位置，不是只把珠子的x坐标随意平移。盒子以中心为基准变化，珠子相对于盒子的分数位置在映射瞬间保持对应。随后，作用力和热运动继续使珠子偏离这种统一几何变换，形成局部调整。

把所有位置按照同一个线性几何规则变换，称为仿射变形。可以想象先在一张柔软方格纸上画一些点，再沿一个方向拉长整张纸：点会跟着方格一起移动。分子体系还多了点与点之间的作用力，因此映射之后它们可以进一步重新排列。这种固体式加载方式与建立连续流动的速度场有所区别。remap x改变位置而不直接把盒子运动速度加到每颗珠子的速度上；若研究流体在持续剪切中的流动与黏度，通常需要相容的速度处理、热运动定义和非平衡积分安排。下一讲的流变问题会把这些条件放到流动背景中讨论。

周期加载还改变了我们怎样理解“试样两端”。盒子内部没有实验夹具，也没有被夹住而几乎不动的端部区域，形变通过整个重复单元的几何变化施加。它很适合观察均匀体相中的链取向、应力与内部调整。若问题转向夹具附近的应力集中、自由表面的变薄或者裂纹尖端，则需要把相应几何与边界实际建进体系。区分这些情形以后，周期盒子的优点就很清楚：用有限数目的珠子表示连续材料的一小部分，使注意力集中在规定的体相加载与分子结构之间的关系上。

### 完整的准备—拉伸—保持输入

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
```

第一组80新增边实例；其他分支只按各自数据和随机种子变化。

运行输入保留NVE积分器与Langevin热浴的组合，时间步为0.005τ。NVE这个命令名在这里表示用于推进位置和速度的积分操作；热浴持续交换能量，加载又改变盒子与粒子位置，所以需要结合全部命令理解实际物理过程。三段run各自结束时保存数据文件，便于把原始网络、松弛后网络和拉伸后网络对应起来。最后一段先撤去fix deform，再继续积分，盒子因此保持在拉伸后的形状。珠子仍然受力并与热浴交换能量，只有施加的整体形变停止继续增加。

完整生成程序会从各自熔体构型产生零、八十和一百六十条新增连接，并连续完成准备、加载与保持。已经运行上一讲例题的读者，可以直接使用那些输出进行本讲分析；从头练习时，下面的程序和运行脚本给出完整流程。每一组都保存自己的连接列表，因此不同重复中的八十条新边是相同规则生成的不同网络。比较时同时保留连接数与构型编号。这样既能观察同一连接数下的变化，也能在同一初始熔体中比较连接数增加的影响，避免将两种变化混在一起。

### 完整生成并运行三个连接方案

```
"""Prepare, connect, relax and stretch a FENE bead-spring network.

python run_network.py --beads 1600 --replica 1 --out-dir network-runs
The LAMMPS executable is selected by --lmp or the LAMMPS environment variable.
Each independent preparation is followed by zero, one or two links per
original chain in total. The linked cases share nested selected-edge lists.
The output retains the exact selected endpoints, inputs and simulation logs.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,re,math
import numpy as np
import os,shutil
p=argparse.ArgumentParser();p.add_argument('--beads',type=int,default=1600);p.add_argument('--replica',type=int,default=1);p.add_argument('--out-dir',type=Path,default=Path('network-runs'));p.add_argument('--lmp',default=os.environ.get('LAMMPS','lmp'));a=p.parse_args()
N=a.beads;M=N//20;assert N%20==0
base=a.out_dir.resolve();d=base/f'n{N}-rep{a.replica}'
if d.exists():raise SystemExit('Choose a new output directory for this configuration.')
d.mkdir(parents=True)
seed=20263000+a.replica;generator=np.random.default_rng(seed);L=(N/.85)**(1/3);coords=[];bonds=[]
# Pack open chains while retaining the seeded sequence of random draws.
for chain in range(M):
 current=generator.uniform(0,L,3)
 for local in range(20):
  for attempt in range(100000):
   candidate=generator.uniform(0,L,3) if local==0 else current+.97*(v:=generator.normal(size=3))/np.linalg.norm(v)
   if coords:
    dr=np.array(coords)-candidate;dr-=L*np.round(dr/L)
    if np.min(np.sum(dr*dr,axis=1))<.65**2:continue
   break
  else:raise RuntimeError('Chain packing did not find a valid location')
  coords.append(candidate.copy());current=candidate
  if local:bonds.append((len(coords)-1,len(coords)))
lines=['Generated FENE chain starting configuration','',f'{N} atoms',f'{len(bonds)} bonds','','1 atom types','2 bond types','',f'0 {L:.15g} xlo xhi',f'0 {L:.15g} ylo yhi',f'0 {L:.15g} zlo zhi','','Masses','','1 1.0','','Atoms # bond','']
for i,xyz in enumerate(coords):
 image=np.floor(xyz/L).astype(int);wrapped=xyz-L*image;lines.append(f'{i+1} {i//20+1} 1 '+' '.join(f'{x:.15g}' for x in wrapped)+' '+' '.join(str(x) for x in image))
lines+=['','Bonds','']+[f'{j+1} 1 {i} {k}' for j,(i,k) in enumerate(bonds)]
(d/'initial.data').write_text('\n'.join(lines)+'\n')
# Shared reduced-unit, neighbour and special-pair definitions.
header='''units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
'''
# Instantaneous records: time, T, U/N, K/N, E/N, pressure, box and longest bond.
record='''compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
'''
# Soft separation, FENE switch, minimization and 100 tau melt preparation.
prepare=header+f'''read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 {seed+100} mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+200} zero yes
variable softA equal ramp(0,100)
fix soften all adapt 1 pair soft a * * v_softA
timestep 0.002
thermo 1000
thermo_style custom step temp pe ke etotal
run 20000
unfix soften
unfix dyn
unfix bath
write_data after-soft.data
pair_style lj/cut 1.122462048309373
pair_modify shift yes
pair_coeff * * 1 1 1.122462048309373
bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0
min_style cg
min_modify dmax 0.01
minimize 1e-8 0.01 10000 100000
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+300} zero yes
'''+record+'''run 20000
write_restart melt.restart
write_data melt.data
'''
(d/'prepare.lmp').write_text(prepare,encoding='utf-8',newline='\n')
found=shutil.which(a.lmp);assert found, f'LAMMPS executable not found: {a.lmp}';binary=Path(found).resolve();logs=[]
def run(where,script):
 cmd=[str(binary),'-in',script,'-log','simulation.log']
 r=dict(command=cmd,directory=where.relative_to(base).as_posix(),input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});t=time.perf_counter()
 with (where/'stdout.log').open('wb') as f:q=subprocess.run(cmd,cwd=where,env={**os.environ,'OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 r.update(exit_code=q.returncode,wall_seconds=time.perf_counter()-t,output_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});logs.append(r)
 (d/'progress.json').write_text(json.dumps(logs,indent=2));print(json.dumps({'directory':str(where),'exit_code':q.returncode,'wall_seconds':r['wall_seconds']}),flush=True)
 if q.returncode:raise SystemExit(q.returncode)
run(d,'prepare.lmp')
data=(d/'melt.data').read_text();atompart=re.search(r'\nAtoms[^\n]*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',data,re.S)[1]
atoms=np.array([[float(x) for x in line.split()] for line in atompart.splitlines() if line.strip()]);atoms=atoms[np.argsort(atoms[:,0])];xyz=atoms[:,3:6];mol=atoms[:,1].astype(int)
# Candidate edges connect nearby beads with different original chain IDs.
candidate=[]
for i in range(N-1):
 dr=xyz[i+1:]-xyz[i];dr-=L*np.round(dr/L);r2=np.sum(dr*dr,1)
 for j in np.flatnonzero((r2<=1.15**2)&(mol[i+1:]!=mol[i])):candidate.append((i,int(i+1+j),float(np.sqrt(r2[j]))))
# Greedy matching uses each bead once; prefixes of one list give nested cases.
edgegen=np.random.default_rng(seed+400);edgegen.shuffle(candidate);edges=[];used=set()
for i,j,dist in candidate:
 if i not in used and j not in used:edges.append((i+1,j+1,dist));used.update((i,j))
target=M*2
if len(edges)<target:raise RuntimeError(f'Only {len(edges)} available edges for {target} target')
# Each branch: 100 tau relaxation, 100 tau extension, 100 tau fixed strain.
choices=[0,M,2*M]
for nc in choices:
 sub=d/f'links-{nc}';sub.mkdir();selected=edges[:nc];text=data
 text=re.sub(r'^\d+ bonds$',f'{len(bonds)+nc} bonds',text,flags=re.M)
 match=re.search(r'\nBonds\s*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',text,re.S)
 original=match[1].strip();addition='\n'.join(f'{len(bonds)+j+1} 2 {i} {k}' for j,(i,k,_) in enumerate(selected))
 text=text[:match.start(1)]+original+'\n'+addition+'\n'+text[match.end(1):]
 (sub/'network.data').write_text(text)
 (sub/'selected-crosslinks.json').write_text(json.dumps(dict(seed=seed+400,candidates=len(candidate),selected=selected,definition='Different original chain IDs, minimum-image distance<=1.15, at most one added edge per bead; common ordered candidate list gives nested link sets.'),indent=2))
 protocol=header+f'''bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+500} zero yes
'''+record+'''run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
'''
 (sub/'network.lmp').write_text(protocol,encoding='utf-8',newline='\n');run(sub,'network.lmp')
receipt=dict(case='lammps-network',N=N,chains=M,replica=a.replica,seed=seed,rho=.85,chain_length=20,links=choices,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),source='Official LAMMPS30Sep2026Update1 bench/in.chain interaction model; independently generated coordinates and explicitly added crosslink/deformation protocols',runs=logs,exit_code=0)
(d/'receipt.json').write_text(json.dumps(receipt,indent=2));print('Network comparison complete',flush=True)
```

从熔体准备开始保存连接与三个运行阶段。

### 从头运行三个独立构型

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python analyze_mechanics.py network-runs --out mechanics/en --language en
python analyze_mechanics.py network-runs --out mechanics/zh --language zh
```

若已有上一讲network-runs输出，可直接执行末尾两条分析命令。

### 实际形变与温度控制

上图为第一组160边网络的实际盒长比；下图是5τ温度块均值，再对三组构型求均值与样本标准差。浅色背景标记加载100–200τ。

LAMMPS 30 Sep 2026 Update 1；官方珠簧相互作用模型，1600个珠子、80条20珠链，ρ*=0.85、T*=1，三个初始构型；FENE/WCA正式动力学时间步0.005τ。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s4)

原9个条件的加载与保持记录。盒子沿x方向从1倍延伸至1.2倍，y、z方向同时收缩以保持体积；温度与体积记录用于核对执行的物理条件。

## 从压力张量读出拉伸方向的机械响应

日常说一杯水有多大的压力，常常用一个数就够了，因为平衡液体在各个方向上的平均作用近似相同。拉伸中的材料却可能沿不同方向传递不同的力，需要把方向保留下来。压力张量可以理解为一组按方向排列的机械量：Pxx、Pyy和Pzz分别对应三个法向分量，还有描述切向作用的分量。LAMMPS的全体系压力计算同时包含粒子运动与相互作用贡献。当前珠簧模型中，珠子间排斥与成键作用都进入相互作用部分，因此仅观察某一类键的伸长，无法替代对整个机械量的计算。

压力通常把压缩取为正，而固体力学讨论拉伸时常把拉伸应力取为正，所以从压力张量到拉伸为正的应力张量需要改变符号。本例进一步取x方向应力减去两个横向应力的平均，得到法向应力差S。这样，各个方向相同的静水压力部分会抵消，留下与方向差异有关的量。若三个压力分量都是五，S为零；若Pxx降为四而横向仍为五，S为一。这个算例说明，总压力仍为正时，也可以出现拉伸方向相对于横向的正应力差。

拉伸为正的法向应力差式 3

![拉伸为正的法向应力差](https://ml-biomat.com/static/agent-math/b95c88cf7dd466c999a902e1.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| S | x方向拉伸应力减去两个横向拉伸应力的平均 | ε/σ³ |
| Pₓₓ, Pᵧᵧ, P𝓏𝓏 | LAMMPS全体系压力张量的三个法向分量 | ε/σ³ |
| ε | 珠簧模型的能量单位 | 能量 |
| σ | 珠簧模型的长度单位 | 长度 |
| =, −, +, /, 2 | 相等、负号、相加、相除；二用于两个横向量取平均 | 1 |

怎样理解拉伸为正的应力与压缩为正的压力相反。再减去横向平均，使各方向相同的静水项抵消。

算一个例子若Pxx=4、Pyy=Pzz=5，单位均为ε/σ³，则S=−4+(5+5)/2=1ε/σ³。三个分量均为5时，S=0。

使用条件用于本例周期等体积加载，包含记录压力的动能与相互作用贡献；它测量法向差异。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s5)

图 3 · 两个手算压力张量示例。三个方向压力相同时，法向应力差为零；轴向压力较低时，相对横向的拉伸应力差为正。

这个S与实验拉力的关系取决于边界条件。自由侧面的试样常在近似零横向应力条件下受拉，此时轴向应力与轴向减横向的差接近；本例则施加等体积横向收缩，横向压力由相互作用自行产生。因而我们把图明确称作法向应力差，并保留它的定义。也要区别真实应力和按初始面积计算的名义应力：试样变细以后，同一拉力除以当前面积与除以原面积会得到不同数值。对于这里的周期体系，首先解释清楚压力分量和几何约束，比直接给一条曲线贴上“拉伸强度”的名称更有用。

瞬时应力会随着碰撞、键振动和局部结构变化而起伏。把一段时间内的保存值求平均，可以减小图中的快速变化，同时保留较慢的加载趋势。本讲把加载的一百τ分成二十段，每段五τ，对每组构型分别求平均，再显示三组平均以及三组之间的样本标准差。阴影描述不同初始网络之间的离散程度，细线保留每一个重复。它帮助我们观察某个趋势是否在各组中都出现，也让一段偶然偏高的应力不会独自决定材料比较。分段长度还会影响时间分辨率：段越长，快速过程越容易被合并。

### 原九组网络的加载应力

每条细线是一组实际构型的5τ块均值，深色线是三组平均，阴影为三组间样本标准差。横轴从同一热力学记录的实际盒长计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s5)

加载阶段以5τ为一块计算法向应力差S。每种连接数保留三组构型的统计，深色线和阴影分别表示三组的均值和样本标准差；横轴为工程应变。

这里的应力单位是ε/σ³，可以从能量与体积的关系理解它。把一个体积压缩或拉伸需要做功，而功等于力沿位移的累积；因此能量除以体积具有力除以面积的量纲。约化模型把ε和σ留作可选择的尺度，图上就用这个组合报告应力。要换算为帕，需要给能量和长度一个相互一致的物理对应；若ε以每摩尔给出，还应先转成单个模拟相互作用使用的能量。这样的单位检查常能发现漏掉体积因子、混用总能量与每粒子能量等问题。

## 拉伸改变了哪些方向：局部键与整条链

要看清内部结构怎样响应，可以先观察原链上每一段键与x轴的夹角。沿x方向排列的键，其方向向量在x上的分量较大；横着排列的键，这个分量较小。把夹角的余弦平方做适当组合，就得到常用的二阶取向量P₂。它在全部键平行于x轴时等于一，在全部键垂直于x轴时等于负二分之一，对三维各向同性方向分布的平均为零。取平方让朝正x与朝负x的两条键都算作沿同一轴排列，适合研究拉伸引起的轴向取向。

沿拉伸轴的原链键取向式 4

![沿拉伸轴的原链键取向](https://ml-biomat.com/static/agent-math/d10a6bc5ac632f32cbfc72a8.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| P₂ | 原链键相对x轴的二阶取向量 | 1 |
| B₀ | 原链键总数，本例80×19=1520 | 1 |
| j | 原链键编号 | 1 |
| bⱼ, bⱼₓ | 第j条原链键的位移向量及x分量 | σ |
| \|bⱼ\| | 该键向量的长度 | σ |
| uⱼₓ | 归一化键方向在x上的分量，也等于夹角余弦 | 1 |
| Σ, ² | 对全部原链键求和；平方 | 1 |
| =, /, −, 1, 2, 3 | 相等、相除、相减和常数一二三；相邻量相乘 | 1 |

怎样理解方向平方把正x与负x视为同一轴。三维各向同性分布中uₓ²的平均为1/3，减去一并除以二后得到零基线。

算一个例子全部键平行于x时uₓ²=1，P₂=(3−1)/2=1；全部垂直时uₓ²=0，P₂=−0.5。

使用条件本讲只统计原链上的1520条键，各键等权；新增交联边另有定义。方向由展开后的实际键向量计算。

局部键方向与整条链的形状仍然是不同尺度。很多键可能各自只有一点方向偏好，累积起来却让一条卷曲链在x方向明显展开。我们把每颗珠子相对于原链中心的位置分成x、y、z三个分量，分别求平方并取平均，得到三个方向的回转尺寸分量。它们相加就是回转半径的平方。再用x分量除以总和，便得到整条链尺寸中沿x方向的比例。一个方向统计上均匀的链群体，这个比例接近三分之一；向x方向拉伸后，它通常会增加。

原链的方向尺寸及轴向占比式 5

![原链的方向尺寸及轴向占比](https://ml-biomat.com/static/agent-math/f4ff8fb7c831934b5e95dc63.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| M, n | 原链条数与每条原链的珠子数 | 1 |
| m, i | 原链编号与该链内的珠子编号 | 1 |
| a | 方向下标，取x、y或z | 1 |
| rₘᵢₐ | 第m条链第i颗珠子在a方向的展开坐标 | σ |
| Rₘₐ | 第m条等质量原链中心在a方向的位置 | σ |
| Gₐₐ, Gₓₓ, Gᵧᵧ, G𝓏𝓏 | 原链群体平均的方向回转尺寸分量 | σ² |
| fₓ | x方向尺寸平方占总尺寸平方的比例 | 1 |
| Σ, ² | 对指定链或珠子求和；平方 | 1 |
| =, /, −, +, 1, (, ) | 相等、相除、相减、相加、常数一、分组括号；相邻量相乘 | 1 |

怎样理解先减去每条原链自己的中心去掉整体平移，再按方向计算平方距离。三个分量相加得到平均回转半径平方，轴向分量除以总和得到占比。

算一个例子一条三珠链沿x位于−1、0、1σ，y=z=0：中心为0，Gxx=(1+0+1)/3=2/3σ²，Gyy=Gzz=0，fx=1。

使用条件所有珠子等质量；各原链按本帧盒长与镜像标记展开。fx是群体平均分量之比，与逐链比例再平均的统计定义不同。

计算这些量时，要先把每条原链按轨迹中的镜像标记展开，使用该帧实际的盒长。加载过程中盒长持续变化，拿初始盒长去展开后来的坐标，会把跨边界链段的位置放错。每条原链仍有二十颗等质量珠子，所以它的中心可以直接取这二十个位置的平均。这里沿用原链编号，观察的是同一批有限链段的尺寸变化；交联后的整个周期网络则可能沿盒子无限重复，整体尺寸需要另一种定义。程序同时检查原链键长，确保展开后的相邻珠子仍然保持合理距离。

实际曲线把这两种尺度放在一起。加载期间，原链键的取向量逐渐偏向正值，整条链的x方向尺寸占比也上升；达到固定盒长以后，这些量仍会继续调整。后者尤其直观：外部尺寸已经停住，内部链段却可以通过转动和重新分配弯曲改变形状。三种连接数的曲线有重叠，各组初始构型也有差别，因此图中显示三组均值与组间离散。它们给应力曲线补充了结构信息，让“材料仍在松弛”对应到实际可计算的内部运动，而不只是一个抽象词语。

### 实际链的取向和方向尺寸

原链坐标按每帧盒长及镜像展开。上图为1520条原链键的P₂，下图为群体平均Gxx除以三个方向分量之和；阴影为三组构型间样本标准差。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s6)

上图统计原链相邻键相对于拉伸轴的二阶取向参数；下图比较原链回转张量x分量占总尺寸的比例。通过周期映像恢复每条原链后，局部方向与整链形状在同一加载历史下比较。

还可以把统一的几何映射作为一个参照图像。假如一条链只是跟随方格纸改变位置，随后没有内部调整，那么它的x方向尺寸会按拉伸比例增大，横向尺寸则按收缩比例减小。真实轨迹在每次映射之间继续经历作用力和热运动，因此最终形状可以偏离这个参照。比较两者，有助于识别哪些变化直接来自施加的几何，哪些来自链段自行重新排列。这里把局部键取向与整体方向尺寸同时展示，也是为了让读者看到材料并非靠一种单一尺度的运动完成变形，而是多个尺度共同响应。

## 固定形变后的应力，怎样读才有物理意义

加载结束后继续保持盒子，并不是把粒子冻结。链段仍在热运动，局部受力仍在改变，某些方向偏好也会缓慢调整。对于黏弹性材料，这正是应力松弛实验关心的过程：维持形变，观察维持它所对应的应力怎样变化。与此相对，保持外力而观察形变随时间增加的过程叫蠕变。两者需要不同的控制条件。本例固定的是盒子形状，所以应力是随内部运动变化的读出量。把控制量与读出量分开，便能清楚地区分实验问题，也知道应该修改哪一段输入命令。

有限体系在加载之前，也可能因为构象与有限时间平均而留下非零的法向应力差。为了比较各自加载后的变化，保持阶段的图减去每个分支在五十到一百τ静置窗口的平均应力。这一操作定义了相对于该分支参考状态的变化量，同时仍保留原始应力数值。选择参考窗口时应使用加载之前、物理条件一致的一段记录，并在不同体系间采用同样规则。如果把参考窗口移到加载以后，或者按结果高低挑选起点，得到的变化量就会回答另一个问题。这里将窗口与各分支基线一并写进数值输出。

相对于本分支静置状态的应力变化式 6

![相对于本分支静置状态的应力变化](https://ml-biomat.com/static/agent-math/8913bd3f4a29e7121d0e91fa.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Sⱼ | 静置参考窗口中第j个法向应力差记录 | ε/σ³ |
| n₀ | 参考窗口内记录数，本例为100 | 1 |
| j | 参考记录编号 | 1 |
| S̄₀ | 该分支参考窗口平均值 | ε/σ³ |
| S(t), ΔS(t) | 时刻t的原始应力差与相对基线的变化 | ε/σ³ |
| t | 记录时间 | τ |
| Σ, =, /, −, Δ | 求和、相等、相除、相减、变化量标记 | 1 |

怎样理解用同一分支的加载前均值作参照，把原有有限构型的偏置与加载后的变化分开记录。

算一个例子第一组160边网络基线约−0.009295ε/σ³；若某个保持段S=0.18ε/σ³，则ΔS=0.18−(−0.009295)=0.189295ε/σ³。

使用条件参考窗口为50≤t<100τ，每0.5τ一条记录，每个网络分别计算基线；原始S同时保存。

### 固定1.2倍伸长后的调整

各分支减去50≤t<100τ静置基线；保持段按10τ分段，区间左开右闭。细线为各构型，深色线为三组均值，阴影为组间样本标准差。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s7)

固定形变后的100τ记录，每10τ分块。各分支先减去自身50≤t<100τ的静置应力基线，再比较三组构型的均值和样本标准差；同一时间窗的热涨落保留在曲线中。

这组百分之二十伸长的短时记录中，带连接体系在加载末段的平均应力差为正，保持阶段仍有明显的构型间起伏。以一百六十条新增边为例，三组在一百九十到二百τ末段的平均值约为0.1120ε/σ³，组间样本标准差约为0.0545ε/σ³。到了二百八十到三百τ，原始应力差的三组平均约为0.0344ε/σ³，组间标准差约为0.0770ε/σ³。读这两个窗口时，既要看均值变化，也要看三条具体记录。它们支持继续测量固定形变下的调整过程，并为下一步选择更长观察时间和更多独立构型提供了量级依据。

为了把保持过程观察得更清楚，同三组一百六十条新增边的网络还进行了一次较长的加载：从各自相同的松弛终点出发，用三百τ拉到1.5倍，再固定形变保持五百τ。这个分支重新建立Langevin随机过程，温度、阻尼时间、键参数和等体积条件保持相同。它同时增加最终形变与观察时长，给我们一组载荷信号更清楚的保持记录。原先百分之二十伸长的九组结果仍然保留，用于比较初始小幅加载的结构变化与波动；两个协议各自按完整条件解释。

### 1.5倍伸长与较长保持的完整输入

```
units lj
atom_style bond
boundary p p p
read_restart initial.restart
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
pair_modify shift yes
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 0
fix stretch all deform 1 x scale 1.5 y volume z volume remap x units box
run 60000
unfix stretch
write_data stretched.data
write_restart stretched.restart
run 100000
write_data final.data
write_restart final.restart
```

从原160边网络的relaxed.restart继续，时间归零并开始新的Langevin随机历史。

### 把同一协议施加到三个原网络

```
"""Run three 1.5-stretch branches from the prepared 160-link networks.

python run_extension.py --base-runs network-runs --out-runs network-extension
Use the same LAMMPS build that produced the binary restart files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--base-runs", type=Path, default=Path("network-runs"))
parser.add_argument("--out-runs", type=Path, default=Path("network-extension"))
parser.add_argument("--lmp", default=os.environ.get("LAMMPS", "lmp"))
args = parser.parse_args()
binary = shutil.which(args.lmp)
if binary is None:
    raise SystemExit(f"LAMMPS executable not found: {args.lmp}")
template = Path(__file__).with_name("extension.lmp").read_text(encoding="utf-8")
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for replica in (1, 2, 3):
    source = args.base_runs/f"n1600-rep{replica}"/"links-160"/"relaxed.restart"
    target = args.out_runs/f"n1600-rep{replica}-links160"
    if target.exists():
        raise SystemExit(f"Choose a new output directory: {target}")
    if not source.is_file():
        raise SystemExit(f"Prepare the source network first: {source}")
    target.mkdir(parents=True)
    shutil.copy2(source, target/"initial.restart")
    text = template.replace("20263501", str(20263500+replica))
    (target/"extension.lmp").write_text(text, encoding="utf-8", newline="\n")
    command = [str(Path(binary).resolve()), "-in", "extension.lmp", "-log", "simulation.log"]
    started = time.perf_counter()
    with (target/"stdout.log").open("wb") as stream:
        result = subprocess.run(command, cwd=target, env={**os.environ, "OMP_NUM_THREADS": "1"},
                                stdout=stream, stderr=subprocess.STDOUT)
    receipt = {"replica": replica, "exit_code": result.returncode,
               "wall_seconds": time.perf_counter()-started,
               "source_restart_sha256": digest(source),
               "input_sha256": digest(target/"extension.lmp"),
               "new_Langevin_history_after_restart": True,
               "Langevin_seed": 20263500+replica,
               "protocol": "300tau to lambda1.5, constant volume;500tau hold;T1,damping1,dt0.005"}
    (target/"receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
```

复制对应重启状态并写出各组输入。使用生成重启文件的同一LAMMPS版本。

### 运行追加协议并绘制双语图

```
#!/usr/bin/env bash
set -euo pipefail
python run_extension.py --base-runs network-runs --out-runs network-extension
python analyze_extension.py network-extension --base-runs network-runs --out extension-analysis/en --language en
python analyze_extension.py network-extension --base-runs network-runs --out extension-analysis/zh --language zh
```

先具备原始network-runs目录及其三个160边松弛重启文件，再运行此脚本。

较长保持记录按五十τ分段，每组有十个保持段。最后二百五十τ内，三组网络的平均法向应力差依次约为0.1752、0.1088和0.1144ε/σ³，三组均值为0.1328ε/σ³，组间样本标准差约为0.0368ε/σ³。这里的组间离散与一条轨迹内部不同时间段的起伏分别保存。每条网络都有自己的连接位置与构象，因此即使连接数相同，保持载荷也不会完全相同。图中保留各组线条和共同均值，让这两类信息一起出现，而不把不同网络的差别藏在一条平滑曲线后面。

### 同三组网络的较大伸长与较长保持

同三组160边网络从原松弛终点重新开始：300τ至1.5倍、500τ保持。左图20τ块、右图50τ块，区间左闭右开；阴影为三组间样本标准差。

三组各1600珠、160条新增链间键的FENE网络，从各自原100τ整理末态继续。T*=1、恒定体积；300τ沿x伸长到1.5倍，再保持500τ；时间步0.005τ。

[下载参考数据与完整输入（ZIP） 47.14 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-extended-mechanics-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/#zh-s7)

同三组160条新增键网络从各自整理末态重新开始，300τ伸长至1.5倍，再保持500τ。两图均显示未减静置基线的法向应力差S，各重复、均值和组间样本标准差分别保留。这组协议同时改变伸长程度与观察时长。

### 完整较长保持分析

```
"""Analyse the independently restarted 1.5-stretch, 500tau-hold networks.

python analyze_extension.py network-extension --base-runs network-runs \
    --out extension-analysis --language en
Input: thermo.dat in three n1600-repN-links160 extension directories and the
original n1600-repN/links-160 directories used for preloading baselines.
"""
from pathlib import Path
import argparse
import json
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def stress(table):
    return -table[:, 6]+(table[:, 7]+table[:, 8])/2


def blocks(time, value, left, right, width):
    rows = []
    for lo in np.arange(left, right, width):
        mask = (time >= lo) & (time < lo+width)
        assert np.any(mask)
        rows.append([lo+width/2, np.mean(value[mask])])
    return np.asarray(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--base-runs", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("extension-analysis"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], []
    for rep in (1, 2, 3):
        table = np.loadtxt(args.directory/f"n1600-rep{rep}-links160"/"thermo.dat")
        base = np.loadtxt(args.base_runs/f"n1600-rep{rep}"/"links-160"/"thermo.dat")
        time = table[:, 1]
        assert table.shape == (1601, 13) and np.allclose(time, np.arange(1601)*.5)
        S = stress(table)
        base_window = (base[:, 1] >= 50) & (base[:, 1] < 100)
        baseline = float(stress(base)[base_window].mean())
        ratios = table[:, 9:12]/table[0, 9:12]
        assert np.max(abs(np.prod(ratios, axis=1)-1)) < 1e-12
        assert np.allclose(ratios[-1], [1.5, 1.5**(-.5), 1.5**(-.5)], atol=1e-12)
        hold = blocks(time, S, 300, 800, 50)
        loading = blocks(time, S, 0, 300, 20)
        strains = blocks(time, ratios[:, 0]-1, 0, 300, 20)[:, 1]
        late = hold[-5:, 1]
        records.append({"replica": rep, "temperature_mean": float(table[:, 2].mean()),
                        "temperature_sd": float(table[:, 2].std(ddof=1)),
                        "max_bond_sigma": float(table[:, 12].max()),
                        "final_stretches": ratios[-1].tolist(),
                        "old_baseline_50_le_t_lt_100": baseline,
                        "late_hold_stress_550_le_t_lt_800": float(late.mean()),
                        "late_hold_timeblock_sd": float(late.std(ddof=1)),
                        "late_change_from_baseline": float(late.mean()-baseline),
                        "holding_50tau_block_means": hold.tolist()})
        raw.append((loading, strains, hold))
        np.savetxt(args.out/f"hold-blocks-rep{rep}.csv", hold, delimiter=",",
                   header="time_from_restart_tau,normal_stress_difference_epsilon_per_sigma3", comments="")
    late = np.array([r["late_hold_stress_550_le_t_lt_800"] for r in records])
    changes = np.array([r["late_change_from_baseline"] for r in records])
    result = {"definition": "Tension-positive normal difference S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma3",
              "protocol": "Restart each original160-link relaxed state, new Langevin history; lambda1 to1.5 in300tau, hold500tau",
              "blocks": "20tau loading,50tau holding; intervals[left,right). Late window550<=t<800 is the final250tau of holding.",
              "records": records,
              "late_hold_mean_across_three": float(late.mean()),
              "late_hold_sample_sd_across_three": float(late.std(ddof=1)),
              "late_change_mean_across_three": float(changes.mean()),
              "late_change_sample_sd_across_three": float(changes.std(ddof=1))}
    (args.out/"extension_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    zh = args.language == "zh"
    tr = lambda c,e: c if zh else e
    installed = {f.name for f in font_manager.fontManager.ttflist}
    font_candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [x for x in font_candidates if x in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5",
                         "text.color": "#193d43", "axes.labelcolor": "#193d43"})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, stage in zip(axes, (0, 2)):
        values = np.stack([r[stage][:, 1] for r in raw])
        x = raw[0][1] if stage == 0 else raw[0][2][:, 0]-300
        for i, (color, ls) in enumerate(zip(("#167d84", "#c16b3d", "#466eaa"), ("-", "--", ":"))):
            ax.plot(x, values[i], color=color, ls=ls, lw=1.3, label=tr(f"构型 {i+1}", f"Config. {i+1}"))
        mean, sd = values.mean(0), values.std(0, ddof=1)
        ax.fill_between(x, mean-sd, mean+sd, color="#557b80", alpha=.13)
        ax.plot(x, mean, color="#193d43", lw=2.5, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#777777", lw=.8); ax.grid(alpha=.15)
    axes[0].set(title=tr("300τ 加载；20τ 分段", "300τ loading; 20τ blocks"),
                xlabel=tr("工程应变 e", "Engineering strain e"), ylabel=tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[1].set(title=tr("500τ 保持；50τ 分段", "500τ holding; 50τ blocks"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同三组160边网络：伸长到1.5倍并延长保持", "The same three 160-link networks: stretch to 1.5 and hold longer"), fontsize=18)
    for ext in ("svg", "png"):
        fig.savefig(args.out/f"network-extended-hold-{args.language}.{ext}", dpi=180)
    plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k.startswith("late_")}, indent=2))


if __name__ == "__main__":
    main()
```

加载按20τ、保持按50τ分段，区间左闭右开；后250τ统计三组之间的样本标准差。

这次较长观察显示，在所给固定形变下，三组网络的后段都维持了正的平均法向应力差。它与永久连接对相对运动的持续约束相联系，也为进一步研究长时间平台提供了起点。若需要区分最终伸长与加载速度各自的作用，可以保持三百τ加载时间，增加一个最终1.2倍的分支；也可以固定最终1.5倍，改变到达它的时间。这样的后续比较围绕一个具体问题展开，能把当前图中看见的现象逐步拆解成材料结构、加载速率和观察时间之间的关系。

如果要进一步提取松弛时间，先需要一段能够分辨持续变化与稳定后段的曲线。单指数函数常用于描述一个主要时间尺度，但高分子网络可以同时存在局部转动、链段调整和更长尺度的运动，曲线未必由一个指数覆盖。可以先比较多个观察窗口、重复构型和加载速度，检查拟合参数是否保持一致，再决定采用怎样的函数。对于永久连接模型，还要把保持后的残余弹性响应与能够随时间消失的部分分别考虑。模型选择应顺着实际曲线中的时间结构推进，而不是先指定一个松弛时间，再让数据围绕它排列。

## 让加载、统计与材料条件对应起来

下面的完整分析程序读取实际盒长、压力分量和全部原链坐标。它先核对三段几何协议，再从压力张量计算法向应力差，对加载与保持分别做不重叠的时间分段平均，最后计算键取向和链的方向尺寸。数值表保留每一组重复，图里的阴影使用三组之间的样本标准差。输入文件中的时间步、轨迹中的保存步数和热力学记录中的时间都被显式对应，因此可以检查不同输出是否讨论同一个阶段。这样的分析结构也便于更换加载时间或连接数：先改模型与运行协议，再让相应的检查和图例同步更新。

### 完整几何、应力和链取向分析

```
"""Read network deformation, stress and original-chain orientation.

python analyze_mechanics.py network-runs --out mechanics --language en
Requires NumPy and Matplotlib. Each n1600-rep1/2/3 directory contains
links-0/80/160 with thermo.dat and trajectory.lammpstrj.
Stress uses the tension-positive normal difference -Pxx+(Pyy+Pzz)/2.
Shading is the sample SD across three independently prepared configurations.
"""
from pathlib import Path
import argparse
import csv
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    """Read orthogonal LAMMPS custom dumps and preserve atom identity."""
    with path.open(encoding="utf-8") as stream:
        while line := stream.readline():
            if not line.strip():
                continue
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(stream.readline())
            assert stream.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(stream.readline())
            assert stream.readline().strip() == "ITEM: BOX BOUNDS pp pp pp"
            bounds = np.array([[float(x) for x in stream.readline().split()] for _ in range(3)])
            columns = stream.readline().split()[2:]
            atoms = np.array([[float(x) for x in stream.readline().split()] for _ in range(n)])
            index = {name: i for i, name in enumerate(columns)}
            atoms = atoms[np.argsort(atoms[:, index["id"]])]
            assert np.array_equal(atoms[:, index["id"]], np.arange(1, n+1))
            xyz = atoms[:, [index[k] for k in ("x", "y", "z")]]
            image = atoms[:, [index[k] for k in ("ix", "iy", "iz")]]
            box = bounds[:, 1]-bounds[:, 0]
            yield step*.005, xyz+image*box, atoms[:, index["mol"]].astype(int), box


def chain_shape(path):
    """Equal-mass original chains: gyration components and bond alignment."""
    rows = []
    for time, xyz, mol, box in frames(path):
        assert len(xyz) == 1600
        assert np.array_equal(mol, np.repeat(np.arange(1, 81), 20))
        chains = xyz.reshape(80, 20, 3)
        relative = chains-chains.mean(axis=1, keepdims=True)
        gyration = np.mean(relative**2, axis=(0, 1))
        vectors = np.diff(chains, axis=1)
        distances = np.linalg.norm(vectors, axis=2)
        assert distances.max() < 1.5
        orientation = np.mean((3*(vectors[:, :, 0]/distances)**2-1)/2)
        rows.append([time, *gyration, orientation, distances.mean(), distances.max()])
    rows = np.asarray(rows)
    assert len(rows) == 121 and np.isclose(rows[-1, 0], 300)
    return rows


def block_means(time, values, start, stop, width):
    """Non-overlapping blocks (left, right], with one mean per block."""
    out = []
    for left in np.arange(start, stop, width):
        mask = (time > left+1e-9) & (time <= left+width+1e-9)
        assert mask.any()
        out.append([left+width/2, np.mean(values[mask])])
    return np.asarray(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("mechanics"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        for links in (0, 80, 160):
            base = args.directory/f"n1600-rep{replica}"/f"links-{links}"
            thermo = np.loadtxt(base/"thermo.dat", comments="#")
            assert thermo.shape == (601, 13)
            time = thermo[:, 1]
            assert np.allclose(time, np.arange(601)*.5)
            box = thermo[:, 9:12]
            stretches = box/box[0]
            volume_ratio = np.prod(stretches, axis=1)
            # ave/time precedes fix deform in the end-of-step fix order.
            # During loading its recorded box is one integration step behind
            # the post-remap box saved in trajectory/data output.
            recorded_elapsed = np.clip(time-100, 0, 100)
            loading_record = (time > 100) & (time <= 200)
            recorded_elapsed[loading_record] -= .005
            expected_x = 1+.002*recorded_elapsed
            expected_yz = expected_x**(-.5)
            assert np.max(np.abs(stretches[:, 0]-expected_x)) < 1e-12
            assert np.max(np.abs(stretches[:, 1:]-expected_yz[:, None])) < 1e-12
            stress = -thermo[:, 6]+.5*(thermo[:, 7]+thermo[:, 8])
            baseline_mask = (time >= 50) & (time < 100)
            baseline = float(stress[baseline_mask].mean())
            shape = chain_shape(base/"trajectory.lammpstrj")
            start_shape = shape[np.isclose(shape[:, 0], 100)][0]
            end_shape = shape[np.isclose(shape[:, 0], 200)][0]
            final_shape = shape[-1]
            summary = {
                "replica": replica, "added_links": links,
                "initial_box_sigma": box[0].tolist(), "final_box_sigma": box[-1].tolist(),
                "final_stretches": stretches[-1].tolist(),
                "final_engineering_strain": float(stretches[-1, 0]-1),
                "final_hencky_strain": float(np.log(stretches[-1, 0])),
                "engineering_strain_rate_per_tau": .002,
                "max_volume_ratio_error": float(np.max(np.abs(volume_ratio-1))),
                "baseline_stress_50_le_t_lt_100": baseline,
                "loading_end_stress_190_lt_t_le_200": float(stress[(time > 190) & (time <= 200)].mean()),
                "early_hold_stress_200_lt_t_le_220": float(stress[(time > 200) & (time <= 220)].mean()),
                "late_hold_stress_280_lt_t_le_300": float(stress[(time > 280) & (time <= 300)].mean()),
                "loading_temperature_mean": float(thermo[(time > 100) & (time <= 200), 2].mean()),
                "holding_temperature_mean": float(thermo[(time > 200) & (time <= 300), 2].mean()),
                "max_bond_sigma": float(thermo[:, 12].max()),
                "gyration_components_t100": start_shape[1:4].tolist(),
                "gyration_components_t200": end_shape[1:4].tolist(),
                "gyration_components_t300": final_shape[1:4].tolist(),
                "bond_P2_t100": float(start_shape[4]), "bond_P2_t200": float(end_shape[4]),
                "bond_P2_t300": float(final_shape[4]),
                "shape_frames": len(shape), "thermo_records": len(time),
            }
            summary["late_hold_change_from_baseline"] = summary["late_hold_stress_280_lt_t_le_300"]-baseline
            records.append(summary)
            raw[(replica, links)] = {"time": time, "thermo": thermo, "stretches": stretches,
                                     "stress": stress, "baseline": baseline, "shape": shape}
            np.savetxt(args.out/f"shape-rep{replica}-links{links}.csv", shape, delimiter=",",
                       header="time_tau,Gxx_sigma2,Gyy_sigma2,Gzz_sigma2,original_bond_P2,mean_bond_sigma,max_bond_sigma", comments="")
    aggregate = []
    for links in (0, 80, 160):
        group = [row for row in records if row["added_links"] == links]
        row = {"added_links": links, "independent_configurations": 3}
        for key in ("baseline_stress_50_le_t_lt_100", "loading_end_stress_190_lt_t_le_200",
                    "early_hold_stress_200_lt_t_le_220", "late_hold_stress_280_lt_t_le_300",
                    "late_hold_change_from_baseline"):
            values = np.array([g[key] for g in group])
            row[key] = {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)), "values": values.tolist()}
        aggregate.append(row)
    result = {"protocol": "100tau fixed volume preparation; 100tau linear Lx ramp to1.2 with constant volume;100tau hold",
              "stress_definition": "S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma^3; tension-positive normal difference",
              "block_definition": "Loading5tau and holding10tau blocks with intervals(left,right]; shading sample SD across3 configurations, not confidence interval",
              "baseline_definition": "50<=t<100, subtracted separately from each branch for holding-change plot",
              "records": records, "aggregate": aggregate}
    (args.out/"mechanics_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    scalar_keys = [k for k, v in records[0].items() if not isinstance(v, list)]
    with (args.out/"mechanics_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=scalar_keys, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    zh = args.language == "zh"
    tr = lambda c, e: c if zh else e
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in candidates if f in installed] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts, "font.size": 14, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "path", "text.color": "#193d43",
                         "axes.labelcolor": "#193d43", "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    colors = ["#167d84", "#c16b3d", "#466eaa"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}-{args.language}.svg")
        fig.savefig(args.out/f"{name}-{args.language}.png", dpi=180)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.8), sharex=True, constrained_layout=True)
    first = raw[(1, 160)]
    for i, (label, color, ls) in enumerate(zip(("x", "y", "z"), colors, ("-", "-", "--"))):
        axes[0].plot(first["time"], first["stretches"][:, i], label=label, color=color, ls=ls, lw=2)
    for links, color in zip((0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["thermo"][:, 2], 0, 300, 5) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        axes[1].plot(blocks[0][:, 0], avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
        axes[1].fill_between(blocks[0][:, 0], avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
        ax.legend(frameon=False, ncol=3); ax.grid(alpha=.18)
    axes[0].set_ylabel(tr("盒长 / 初始盒长", "Box length / initial length"))
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("温度 T*", "Temperature T*"))
    axes[1].axhline(1, color="#687574", lw=1, ls="--")
    fig.suptitle(tr("先规定形变，再核对温度和体积", "Specify deformation, then check thermal and geometric conditions"), fontsize=18)
    save(fig, "network-deformation")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"], 100, 200, 5) for rep in (1, 2, 3)]
        strain = block_means(raw[(1, links)]["time"], raw[(1, links)]["stretches"][:, 0]-1, 100, 200, 5)[:, 1]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(strain, values[rep], color=color, ls=ls, alpha=.5, lw=1, label=tr(f"构型{rep+1}", f"Config. {rep+1}"))
        ax.fill_between(strain, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(strain, avg, color="#213b40", lw=2.3, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("工程应变 e", "Engineering strain e"))
    axes[0].set_ylabel(tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("加载段：5τ 分段平均与三组构型的离散", "Loading: 5τ block means and variation across configurations"), fontsize=18)
    save(fig, "network-stress-strain")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"]-raw[(rep, links)]["baseline"], 200, 300, 10) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(blocks[0][:, 0]-200, values[rep], ls=ls, color=color, alpha=.5, lw=1)
        ax.fill_between(blocks[0][:, 0]-200, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(blocks[0][:, 0]-200, avg, color="#213b40", lw=2.3)
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].set_ylabel(tr("相对各自静置基线的 ΔS / (ε σ⁻³)", "ΔS from each resting baseline / (ε σ⁻³)"))
    fig.suptitle(tr("固定形变后：10τ 分段平均，阴影为三组间标准差", "Fixed deformation: 10τ blocks; shading is the SD across three configurations"), fontsize=17)
    save(fig, "network-stress-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for links, color in zip((0, 80, 160), colors):
        shapes = np.stack([raw[(rep, links)]["shape"] for rep in (1, 2, 3)])
        time = shapes[0, :, 0]
        for ax, vals in zip(axes, (shapes[:, :, 4], shapes[:, :, 1]/np.sum(shapes[:, :, 1:4], axis=2))):
            avg, sd = vals.mean(0), vals.std(0, ddof=1)
            ax.plot(time, avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
            ax.fill_between(time, avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0); ax.grid(alpha=.18)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
    axes[0].axhline(0, color="#777777", lw=.8, ls="--")
    axes[1].axhline(1/3, color="#777777", lw=.8, ls="--")
    axes[0].set_ylabel(tr("原链键取向 P₂", "Original-chain bond P₂")); axes[0].legend(frameon=False, ncol=3)
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("链尺寸的 x 方向占比 Gxx / tr(G)", "Chain-shape x fraction Gxx / tr(G)"))
    fig.suptitle(tr("从局部键取向到整条原链的形状", "From local bond orientation to whole original-chain shape"), fontsize=18)
    save(fig, "network-chain-orientation")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
```

读取各分支thermo.dat与trajectory.lammpstrj，保存每组统计与双语图。

关于输出时刻，还有一个小细节值得了解。本输入先定义记录操作，后定义盒子形变操作，因此加载过程中的热力学记录保存的是该步映射之前的盒长，而轨迹与阶段终点的数据文件保存更新后的盒子。两者只差一个0.005τ积分步，对应本例伸长比相差十万分之一。分析把应力和同一行实际盒长配对，展开轨迹时则使用轨迹自己保存的边界，保持每种记录内部一致。这个差别对图的整体形状很小，却说明精确分析应从真实输出及其记录顺序出发。

把结果转向材料研究时，首先明确需要比较的是哪一种实验。对于固定温度、近似等体积的网络拉伸，本例已经给出几何、应力和结构分析的完整路径；研究水凝胶溶胀后的力学，要先确定含水量与平衡体积；研究快速冲击，则要考察热交换和加载时间；研究裂纹扩展或化学断裂，则要加入允许相应损伤发生的模型。相同的拉伸比并不保证这些体系具有相同物理过程。把制备状态、连接寿命、体积约束和时间尺度逐项对应起来，才能让一个可运行的例题逐渐成为针对具体材料的研究模型。

可以用三个问题检查自己的结论是否与数据相连。第一，施加的是什么：方向、伸长比、时间和横向条件都能从实际盒长恢复吗？第二，测量的是什么：应力符号、压力分量、参考窗口与平均方式是否明确？第三，内部怎样响应：键方向、链尺寸和温度是否与力学变化相互对应？把这三个层次放在一起，看到曲线差异时就有具体的解释路径。继续研究时，可以增加独立构型、改变加载速率或延长保持时间，每次针对一个问题改变条件，并保留上一组结果作为比较。

生物材料的力学问题往往还跨越多个尺度。例如，组织或含水网络的宏观松弛可能同时包含链段调整与水在内部重新分布；其中水移动的时间还与试样尺寸有关。当前固定密度、没有显式溶剂的珠簧网络把注意力集中在链与连接的作用。将它扩展到含水体系时，可以保留本讲的几何检查、应力定义与独立重复策略，再增加溶剂分布、流动和化学作用的测量。这样，新的物理过程会有对应的读出量，原有链网络分析也能继续使用，逐步组成对实际材料更完整的解释。

## 延伸阅读与开放资料

- [LAMMPS 30 September 2026 Update1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE珠簧基础相互作用及L08—09的同一实际网络。

  追加等体积拉伸、固定形变保持、三组独立构型及结构与应力分析；协议参数在正文完整说明。
- [fix deform command](https://docs.lammps.org/fix_deform.html) · LAMMPS developers · Official documentation; cited for command semantics

  线性盒长变化、volume横向约束及remap x位置映射。

  原创几何图、可交互映射与实跑协议。
- [compute pressure command](https://docs.lammps.org/compute_pressure.html) · LAMMPS developers · Official documentation; cited for physical definitions

  压力张量分量、动能与相互作用贡献。

  逐步推导本讲法向应力差并用实际记录统计。
- [NEMD simulations](https://docs.lammps.org/Howto_nemd.html) · LAMMPS developers · Official documentation; citation

  区分固体式位置映射与流体速度场/SLLOD安排。

  将控制条件解释放入拉伸与流变的衔接。
- [A Description of a Property of Caoutchouc or Indian Rubber (1805)](https://www.biodiversitylibrary.org/part/304904) · John Gough · Original historical article; BHL catalogue lists public domain; citation, no scan reproduced

  天然橡胶性质研究的历史题目与发表年代。

  原创外部观测与分子构象关系图。
- [On Some Thermo-Dynamic Properties of Solids (1859)](https://doi.org/10.1098/rstl.1859.0005) · James Prescott Joule · Historical research article; citation, no original text or image reproduced

  机械变化与热效应共同研究的历史背景。

  用概念图连接宏观测量与现代链模型。
- [On Some Thermo-Dynamic Properties of Solids: original 1858 abstract, p.254](https://darwin-online.org.uk/converted/pdf/1858_Lyell_tabular_masses_A4980.pdf) · James Prescott Joule; Proceedings of the Royal Society of London · Historical primary text scan; citation and paraphrase

  原始摘要中机械作用、温度与材料尺寸共同讨论的研究问题。

  历史信息用于原创教学叙述；不复制原文或图像。
