# 分子为何停留在表面

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l12/
Language: zh-CN

让水分子与储库交换，在一个真实裂隙中读懂吸附数量、空间分布和采样过程。

## 从干燥剂到分子停留的位置

打开一包需要防潮的食品，常会看到一小袋干燥剂。它的作用与材料内部的大量微小空间有关：水分子能够进入孔隙，与孔壁及其他水分子相互作用，使水在材料中的分布不同于周围环境。对多孔玻璃、涂层和用于分离的材料而言，知道“能吸多少水”还不够。水停在孔壁附近还是聚集在孔中央，孔道尺寸与表面化学怎样改变这种分布，往往决定材料在湿润环境中的表现。

吸附指分子在界面附近富集。它与分子进入材料内部体相的吸收有不同侧重点，但多孔材料把这两种直观图景联系起来：孔道在颗粒内部，孔壁却仍是固体与流体接触的表面。把一块材料切成许多小块，总体积可以相近，暴露的表面积却会增加；再把孔道做到纳米尺度，许多分子都可能处在距离孔壁很近的位置。因此，宏观看起来不大的颗粒，可以具有丰富的界面环境。

本讲研究一个带裂隙的二氧化硅小单元，固定720个固体原子，让水分子在其中运动，并与一个规定状态的虚拟储库交换。初态放入3个水分子，实际记录末态有64个水分子。我们将追踪这个数量变化，检查每次被接受的加入与删除如何对应总数，再沿裂隙方向计算水的空间分布。读完以后，你能把一张吸附动画拆成明确的模型、交换规则和测量量，知道每个数字究竟回答什么问题。

这次计算使用分子动力学与巨正则蒙特卡洛的组合。分子动力学让已有分子在力的作用下移动，蒙特卡洛则提出加入或移走一个完整水分子的尝试，再按统计规则决定是否接受。于是，盒子里的粒子数不再固定。可以把研究对象想成一间与大环境相连的小房间：我们关心房间里通常有多少分子、它们待在哪里，而大环境的状态由温度与化学势指定，不需要真的把整个环境都画进计算盒中。

“虚拟储库”是一个热力学边界条件。本例用300 K和100 bar的理想储库参数设置交换倾向，盒子本身的体积保持不变。实际水的非理想性质、空气中的相对湿度与材料表面化学，可以在后续研究中通过相应模型接入。先把这里的对象说清楚，便能理解一个小算例的用途：它展示开放体系怎样从稀少的水分子起点，逐渐形成由孔隙几何、相互作用和交换规则共同决定的分布。

### 裂隙中的实际水分子

真实保存帧；各帧原子数随完整水交换变化。基底固定，MD与GCMC按规定次序交替。

固定的720原子二氧化硅基底、三向周期盒，300 K及100 bar理想气体储库；TIP4P/2005水采用原教程的0.008 eV氧LJ参数。1 fs步长，累计25 ps的混合GCMC/MD。

[下载参考数据与完整输入（ZIP） 1.45 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-adsorption-reference-data.zip)

## 表面为什么值得单独研究

在表面科学建立起来以前，固体常被当成具有某种整体性质的物体。然而，同样的材料只要改变暴露面积或表面状态，就可能改变对气体的吸附。Langmuir在1918年讨论玻璃、云母和铂的平面表面对气体的吸附，把“表面上有多少位置被分子占据”变成可以计算的问题。他在1932年的诺贝尔演讲中也从炭对气体的吸附谈起，强调表面现象与材料细分程度的联系。这里的关键认识是：界面有自己的分子排列和占据状态，值得与体相分开描述。

先从一个容易画出的模型入手。设表面上有许多等价位置，每个位置最多容纳一个分子，位置之间没有额外相互影响。空位置可以接纳分子，已有分子也可以离开。压力增加时，环境提供分子的倾向增强；位置逐渐占满以后，再增加压力带来的占据变化就会减小。这种图景把吸附曲线的弯曲与有限位置联系起来，也让“容量”和“亲和性”成为不同的量：前者关心最多有多少位置，后者关心在什么环境条件下容易被占据。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s2)

图 1 · Langmuir位点图景：占据比例由到达与离开的统计平衡决定。图为原理示意，右侧曲线采用等价独立位点模型。

这个位点模型适合帮助我们建立直觉，实际裂隙则有更多结构。孔壁不是整齐的格点，局部凹凸使水分子遇到的环境各不相同；水分子之间还会互相作用，孔中央也可能容纳水。原子模型把这些位置和相互作用显式放进去，用统计采样得到空间分布。两种描述可以相互配合：简单位点模型说明曲线为什么可能出现有限占据的趋势，原子模拟则帮助识别具体几何与分子作用如何改变这一趋势。

设被占据位置的比例为θ，空位置比例就是1−θ。若到达空位置的倾向正比于压力P和空位比例，离开位置的倾向正比于已占据比例，那么在平均占据不再变化时，两种倾向相等。把它们的比例记为K，整理后得到下面的Langmuir关系。这里的推导没有要求某个分子永久停住；平均占据稳定的同时，具体分子仍可以不断交换。这是理解吸附平衡与微观运动能够同时存在的一条重要线索。

等价单层位点的平均占据式 5

![等价单层位点的平均占据](https://ml-biomat.com/static/agent-math/60d220a6a60587f40681fe4d.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| θ | 被占据的位点比例，从0到1 | 无量纲 |
| K | 固定温度下的亲和参数 | bar⁻¹ |
| P | 储库压力 | bar |
| 1 | 全部位点比例的归一化常数 | 无量纲 |
| =、+、−、×、/ | 相等、相加、相减、乘法、除法；分数横线同样表示除法。 | 运算符 |

怎样理解设进入倾向与P(1−θ)成正比，离开倾向与θ成正比。两者平衡后得到θ=KP(1−θ)，移项并除以1+KP得到此式。

算一个例子K=0.1 bar⁻¹、P=10 bar时KP=1，θ=1/2。若P=100 bar，θ=10/11≈0.9091。

使用条件用于等价、独立、每位点最多一个分子的单层模型。此处是解析概念交互；实际裂隙结果来自原子轨迹。

下面的交互展示等价单层位点模型。改变K相当于改变给定温度下的亲和参数，改变P则改变储库条件；曲线上的点与位置填充示意会同时更新。它说明一个明确解析模型的行为，实际裂隙的计算结果放在后面的轨迹和密度图中。观察时可以先固定K，找出占据达到一半所需的压力，再固定压力改变K。两种操作都能提高占据，却对应不同的实验或模型设计。

等价独立位点的解析模型：调节压力与亲和参数，观察平均占据。图中每格的填充高度表示平均比例，不是一次随机的分子快照。

若把这个思路用于材料比较，需要先保持测量定义一致。同样数量的水，分布在更大表面积或更多孔体积中，含义就会改变。实验常按材料质量报告吸附量，也可以按表面积或孔体积归一化；模拟则从分子计数起步，再通过明确的质量和几何换算接到这些单位。理解归一化选择，比把所有曲线都拟合成同一种形状更早一步，因为拟合参数的物理含义取决于纵轴究竟测量了什么。

## 开放体系怎样与储库交换分子

在固定粒子数的水盒里，温度控制器可以交换能量，但不会凭空增减水分子。吸附问题需要另一种自由度：允许盒子与环境交换分子。巨正则系综通常记作μVT，分别表示化学势、体积和温度被指定，粒子数随状态变化。这里的“系综”可以理解为符合这些外部条件的一组可能微观状态；采样的任务是按照相应权重访问它们，而不只是找到一个最低势能构型。

化学势可以先理解为把一个分子从大环境转移出来时所涉及的自由能尺度。它把环境的供给倾向带进小体系，同时考虑能量与可出现状态的多少。对固定温度的理想储库，提高压力会提高化学势，二者通过对数联系。对数并不神秘：它把压力的倍数变化变成可相加的变化。压力从1 bar增加到10 bar，与从10 bar增加到100 bar，都是增大十倍，因此对应相同的理想化学势增量。

压力怎样改变化学势式 2

![压力怎样改变化学势](https://ml-biomat.com/static/agent-math/a13d063b19a27a0fb6670903.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| μ(P₁)、μ(P₂) | 两个压力下每个分子的理想储库化学势 | eV |
| P₁、P₂ | 比较的两种正压力，使用相同单位 | bar |
| kB | 玻尔兹曼常数，8.617333262×10⁻⁵ eV/K | eV/K |
| T | 固定的绝对温度 | K |
| ln | 自然对数，输入的压力比无量纲 | 运算符 |
| 1、2、B | 两个比较状态与玻尔兹曼常数的下标 | 标签 |
| =、+、−、×、/ | 相等、相加、相减、乘法、除法；分数横线同样表示除法。 | 运算符 |

怎样理解对固定温度的理想储库，分子供给倾向随数密度增加；压力与数密度成正比，倍数变化通过对数转换为化学势增量。

算一个例子300 K时kBT≈0.025852 eV。从1到100 bar，增量为0.025852×ln100≈0.11905 eV/分子，换算为每摩尔约11.49 kJ。

使用条件这是同一温度下理想储库的差值。非理想储库使用逸度；绝对化学势还依赖标准态约定。

实际输入采用`pressure 100`。LAMMPS由这个压力和温度设置储库的化学势，因此同一命令前面写出的`-0.5`不再作为直接化学势值起作用。该文件使用`units metal`，其中时间单位是ps、长度单位是Å、能量单位是eV、压力单位是bar。把100写成100 atm，或把0.001 ps读成0.001 fs，都会改变物理问题。单位约定应在读输入的第一步确定，再解释后面的每个数字。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s3)

图 2 · 储库以热力学条件影响分子加入与离开的权重。MD时间推进与GCMC交换承担不同职责。

一次插入尝试会随机选择位置与取向，放入一个完整水分子，并比较尝试前后的相互作用能。接受概率还包含储库供给与可用状态数的因素，所以“势能降低就接受，升高就拒绝”不是完整的开放体系规则。适当接受部分能量上升的变化，有助于访问有限温度下应出现的状态；插入和删除共同满足相应统计关系，使分子数有机会在多个值之间探索。随机数决定某次尝试的结果，而许多次尝试的统计组织由模型条件规定。

本例每推进100个1 fs的MD步，就进行平均100次分子交换尝试。插入与删除以相同机会被选为尝试类型，实际总次数因此略有差别。另一个参数把普通蒙特卡洛平移或转动尝试数设为0；已有分子的移动主要由两次交换批次之间的MD完成。插入时仍会随机选择分子取向，这与额外尝试转动一个已经存在的分子是两件事。把这些操作区分开，就能准确读懂命令中连续出现的几个数字。

混合方法的时间轴需要按这种组织来读。图上25 ps是MD累计推进的时间，在其间插入了蒙特卡洛交换。一个新水分子可以直接出现在孔内某个被接受的位置，它没有经历从材料外部穿过整条孔道的运动路径。因此，这条数量曲线适合观察采样和填充过程；要研究真实吸水速度、扩散系数或滞留时间，应安排保留连续分子运动路径的动力学阶段，并定义相应的边界与进出过程。

## 把裂隙与水写成明确的相互作用

本例的固体由240个Si和480个O组成，对应二氧化硅的组成比例。盒边约为4.494、1.716和1.698 nm，三个方向均采用周期边界。中间的低固体密度区域形成不规则裂隙，周围的结构会在相邻周期单元中重复。水看到的是这样一个固定孔隙几何，而不是一整颗具有外表面的干燥剂颗粒。研究孔径分布、颗粒尺度运输或不同裂面时，需要分别建立相应几何及其代表范围。

吸附阶段只给水分子安排时间积分，固体原子位置保持不动。固体Si和O在这里的电荷为0，它们与水氧之间通过指定的Lennard–Jones作用形成排斥与吸引。这个设置让孔隙形状和表面吸引成为清楚的控制因素。它也明确了模型保留的机制：水能够平移、转动并与其他水相互作用，基底不发生振动、裂纹扩展或表面羟基化。要研究水引起的表面反应，需要在原子模型中加入相应的反应与电荷描述。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s4)

图 3 · TIP4P水的虚拟负电荷位置由几何构造。基底Si/O在本例中保持固定和电中性，水与固体的交叉作用由输入中的LJ参数给定。

水采用TIP4P/2005的刚性几何与电荷布局，氧—氢距离约0.9572 Å，氢—氧—氢角为104.52°。每个水在坐标文件中有一个氧和两个氢，负电荷的作用位置则位于从氧朝两氢之间伸出的虚拟M点，距氧0.1546 Å。两个氢各带+0.5564个元电荷，M点对应−1.1128个元电荷，合起来电中性。专门的TIP4P相互作用计算会构造这个虚拟位置，所以轨迹中的三个原子记录与模型名称里的四个作用位点并不矛盾。

水氧之间的Lennard–Jones参数为ε=0.008 eV、σ=3.1589 Å，其中ε沿用本例输入中的舍入值。Si—水氧与固体O—水氧分别使用0.0057 eV、4.42 Å，以及0.0043 eV、3.12 Å。σ主要规定排斥与吸引转换的距离尺度，ε规定相互作用的能量尺度；几何形状相同而参数不同的孔壁，仍可能产生不同的水分布。长程静电使用与TIP4P相配的PPPM处理，实空间截断为10 Å。

刚性水需要约束算法维持内部几何。这里的SHAKE固定两条O—H共价键和H—O—H角，并把新插入的分子纳入同一约束。模板里的坐标给出初始摆放形状，正式运动遵循约束参数。键与角的谐振系数写成0，不能据此说水是三个互不相连的粒子；拓扑提供连接，SHAKE执行几何约束，电荷和非键作用决定分子之间的相互作用。分别理解这些职责，能避免只看某一个系数就误读整个模型。

粒子数变化还会影响温度计算。温度来自可运动自由度对应的动能，随着水分子加入或删除，分母也需要更新。`dynamic/dof yes`让水温度计算采用当前粒子数，约束再决定哪些内部运动自由度被移除。热浴针对水组，目标300 K；冻结基底不应被当成一群温度很低的流体粒子混进这个平均。输入还保留插入速度调整因子5/3，用来调节新分子的速度初始化，它不改变300 K的目标温度。

## 运行一次能够逐项检查的交换过程

完整运行需要基底坐标`cracking-mod.data`、水模板`H2O.mol`、主输入`gcmc.lmp`和`run.sh`。它们放在同一个目录后即可运行。基底文件含原子类型、质量、坐标及为新增分子预留的键角存储；水模板说明一次加入的整个分子有哪些原子、哪些电荷和哪些连接。下面的检查程序先确认720个基底原子的组成、电荷和盒尺寸，使模型身份在真正开始采样前就清楚可见。

### 检查固定基底

```
"""Check the prepared neutral silica geometry before adding water.

python check_surface.py
"""
from pathlib import Path
import re
import json
import numpy as np

lines = Path('cracking-mod.data').read_text().splitlines()
declared = next(int(s.split()[0]) for s in lines if re.fullmatch(r'\s*\d+ atoms\s*', s))
start = next(i for i, s in enumerate(lines) if s.strip().startswith('Atoms #'))+1
rows = []
for s in lines[start:]:
    if not s.strip():
        continue
    if not s.split()[0].isdigit():
        break
    rows.append(list(map(float, s.split())))
a = np.array(rows)
assert len(a) == declared == 720
assert len(np.unique(a[:, 0])) == 720
assert np.count_nonzero(a[:, 2] == 1) == 240
assert np.count_nonzero(a[:, 2] == 2) == 480
assert np.all(a[:, 3] == 0)
box = np.array([list(map(float, s.split()[:2])) for s in lines
                if s.strip().endswith(('xlo xhi', 'ylo yhi', 'zlo zhi'))])
assert box.shape == (3, 2)
assert np.all((a[:, 4:7] >= box[:, 0]) & (a[:, 4:7] <= box[:, 1]))
print(json.dumps({'Si': 240, 'substrate_O': 480, 'total_charge_e': float(a[:, 3].sum()),
                  'cell_lengths_nm': ((box[:, 1]-box[:, 0])/10).tolist()}, indent=2))
```

在输入目录执行python check_surface.py，读取并核对实际基底。

### 完整水分子模板

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

1    0 0 0
2    0.9584 0 0
3    -0.23996 0.92787 0

Types

1        OW
2        HW
3        HW

Charges

1       -1.1128
2        0.5564
3        0.5564

Bonds

1   OW-HW      1      2
2   OW-HW      1      3

Angles

1   HW-OW-HW    2      1      3

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 OW-HW OW-HW HW-OW-HW
2 OW-HW OW-HW HW-OW-HW
3 OW-HW OW-HW HW-OW-HW

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
```

三个原子、两条键、一个角与SHAKE信息共同定义一个被交换分子。

主输入先读入基底，再随机放置3个水分子作为起点。这里为基底设置零速度，随后只积分水组，因此基底不会携带无关的动能记录。参数命令设置水—水和水—表面的作用，SHAKE与热浴管理水的内部约束及温度，GCMC负责完整分子交换。把这些功能按模型对象分开阅读，比把几十行命令背成固定配方更有用：换表面材料时主要检查基底与交叉参数，换交换分子时则要重建模板、约束和储库条件。

软件也需要具备与这些命令匹配的功能。GCMC属于分子交换功能包，刚性水需要SHAKE，长程静电需要相应的求解器；运行脚本使用四个OpenMP线程执行本例。先按环境准备页建立软件，再检查版本与可用功能，可以把“输入语法不被识别”和“物理体系运动不稳定”区分开。前者应核对程序构建，后者则回到几何、参数、约束和时间步。两类问题对应不同的检查入口。

### 完整吸附输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units metal
boundary p p p
atom_style full

pair_style lj/cut/tip4p/long OW HW OW-HW HW-OW-HW 0.1546 10
kspace_style pppm/tip4p 1.0e-5
bond_style harmonic
angle_style harmonic

read_data cracking-mod.data
molecule h2omol H2O.mol
create_atoms 0 random 3 3245 NULL mol h2omol 4585 overlap 2.0 maxtry 50

group SiO type Si O
group H2O type OW HW
# The frozen substrate has no kinetic motion in this adsorption stage.
velocity SiO set 0.0 0.0 0.0

pair_coeff * * 0 0
pair_coeff Si OW 0.0057 4.42
pair_coeff O OW 0.0043 3.12
pair_coeff OW OW 0.008 3.1589
pair_coeff HW HW 0.0 0.0
bond_coeff OW-HW 0 0.9572
angle_coeff HW-OW-HW 0 104.52

variable oxygen atom type==label2type(atom,OW)
group oxygen dynamic all var oxygen
variable nO equal count(oxygen)

fix shak H2O shake 1.0e-5 200 0 b OW-HW a HW-OW-HW mol h2omol


compute ctH2O H2O temp
compute_modify thermo_temp dynamic/dof yes
compute_modify ctH2O dynamic/dof yes
fix mynvt H2O nvt temp 300 300 0.1
fix_modify mynvt temp ctH2O

timestep 0.001

variable tfac equal 5.0/3.0 
fix fgcmc H2O gcmc 100 100 0 0 65899 300 -0.5 0.1 &
  mol h2omol tfac_insert ${tfac} shake shak full_energy pressure 100

thermo 250
thermo_style custom step c_ctH2O etotal v_nO &
  f_fgcmc[3] f_fgcmc[4] f_fgcmc[5] f_fgcmc[6]

# Numerical records preserve the original 25 ps hybrid GCMC/MD schedule.
dump course all custom 250 adsorption.lammpstrj id mol type q x y z ix iy iz
dump_modify course sort id
variable courseTime equal time
variable courseT equal c_ctH2O
variable courseU equal pe
variable courseE equal etotal
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseE v_nO f_fgcmc[3] f_fgcmc[4] f_fgcmc[5] f_fgcmc[6] file adsorption-thermo.dat
run 25000
write_data adsorption-final.data
write_restart adsorption-final.restart
```

300 K、100 bar理想储库，1 fs时间步，25 ps混合GCMC/MD。

`full_energy`要求交换尝试前后比较完整体系的势能，适应这里的长程静电计算。一个新分子不仅与近处原子发生作用，也会影响周期体系的静电能；只考虑某个局部原子对可能漏掉这部分变化。每250步保存一次轨迹和数值记录，正好间隔0.25 ps。25000步运行连同初态一共保存101帧。轨迹每帧都带有自己的原子数、原子编号、分子编号和类型，方便分析程序正确处理不断变化的分子集合。

### 运行并保存原始数值记录

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=4
"$lmp" -sf omp -pk omp 4 -in gcmc.lmp -log adsorption.log > adsorption.stdout.log 2>&1
```

同目录执行bash run.sh。使用包含MC、刚性水和长程静电能力的LAMMPS及OPENMP后缀。

运行后，首先检查水氧数量与完整水分子组成。本例每个水恰有一个氧，因此水氧数就是水分子数；每个水还应有两个氢。接着检查固定基底的720个原子在每帧保持相同位置，再核对插入、删除与总数之间的关系。这种检查不是额外的抽象规范，而是直接回答画面里那些新点究竟代表什么：它们应属于完整分子，新增数量也应由交换记录逐项解释。

用分子交换核对总数式 1

![用分子交换核对总数](https://ml-biomat.com/static/agent-math/85559284361036d4692b16f4.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N(t)、N₀ | 时刻t与初始时刻的水分子数 | 个分子 |
| Ains(t)、Adel(t) | 截至时刻t累计接受的完整分子插入、删除次数 | 次 |
| t | 混合算法中累计推进的MD时间 | ps |
| ins、del、0 | 插入、删除、初始的下标标签 | 标签 |
| =、+、−、×、/ | 相等、相加、相减、乘法、除法；分数横线同样表示除法。 | 运算符 |

怎样理解每次接受插入增加一个水，接受删除减少一个水。把这些整数变化累加，就得到任一保存时刻的数量。

算一个例子末态N=3+77−16=64个水；总原子数为720+3×64=912。这里每个水的三个原子共同加入或删除。

使用条件适用于本例只有完整水分子交换、固定基底不变的记录。

末态记录为12470次插入尝试中接受77次，12530次删除尝试中接受16次。初态3个水加上77次成功插入，再减去16次成功删除，得到64个水，与末帧坐标一致。总原子数相应为720+3×64=912。整条记录逐帧满足同一关系，说明轨迹中的粒子变化与蒙特卡洛计数相互对应。接受一次分子插入会增加三个原子，不能把原子数的变化直接当成水分子数。

开始时3个水没有被单独赋予一套热速度，首条水温度记录为0 K，随后在热浴、交换和相互作用中进入目标温度附近。因此，分析后段温度时明确采用12.5<t≤25 ps的50帧，均值约294.898 K、样本标准差约22.292 K。这里体系规模小，分子数又持续变化，瞬时温度自然比大水盒更明显地起伏。读图时要同时保留初始化过程与后段统计，既看见起点，也清楚平均包含了哪些记录。

### 数量、温度与势能

101条0至25 ps记录。橙色空心点按接受插入与删除重建数量；温度虚线为300 K目标。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s5)

101个实际保存时刻的水分子数、温度和体系势能。数量同时用3个初始水加接受插入、减接受删除独立重建。横轴累加MD积分时间，插入与删除表示储库交换。

## 接受率怎样帮助阅读数量曲线

总分子数增长以后，曲线会出现较长的平段。但平段可能有不同来源：插入和删除都很活跃而彼此抵消，或者两类尝试都很难被接受。它们对采样的含义不同，因此需要同时观察尝试次数与成功次数。前一种情形显示分子集合持续交换，后一种情形则提示当前构型附近的交换受到位置拥挤或能量因素影响。只看总数，就像只看停车场里有多少辆车，却不知道门口究竟有多少车进出。

分别计算插入与删除的接受比例式 3

![分别计算插入与删除的接受比例](https://ml-biomat.com/static/agent-math/55109e38751896b5e68070f3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ains、adel | 插入与删除被接受的比例 | 无量纲 |
| Ains、Adel | 选定时间窗口内被接受的尝试数 | 次 |
| Mins、Mdel | 同一窗口内相应的全部尝试数 | 次 |
| ins、del | 两种交换操作的标签 | 标签 |
| =、+、−、×、/ | 相等、相加、相减、乘法、除法；分数横线同样表示除法。 | 运算符 |

怎样理解每类成功次数除以自己的尝试次数，才是该类操作的接受比例。分块时先对累计计数作差，得到窗口内的次数。

算一个例子77/12470≈0.00617482，即0.617482%；16/12530≈0.00127694，即0.127694%。百分数等于无量纲比例乘100%。

使用条件接受率描述交换算法在指定状态和窗口中的行为，与真实材料的到达速率有不同定义。

这条记录的总体插入接受比例约0.6175%，删除接受比例约0.1277%。这些比例由各自的成功次数除以尝试次数得到，分母不同，不能直接比较两个成功总数来代替。进一步按5 ps分块，第一块接受56次插入，插入接受率约2.300%；最后一块接受3次插入，约0.1226%。随着空间中已有更多水，随机放入一个完整分子更容易遇到近距离排斥，加入后的能量变化也随周围水的组织而改变。

### 分块交换活动

每块左开右闭5 ps，接受率由累计尝试与成功次数的端点差得到。下图按该块20帧平均水数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s6)

五个连续5 ps窗口的插入、删除接受比例，以及各窗口20帧的平均水数。窗口均为左开右闭；尝试和接受次数由累计计数的端点差得到。

分块平均数量同样揭示了这段过程的组织。五个连续窗口的平均水分子数依次约为32.9、53.4、57.95、60.45和62.55。后面增长比前面缓慢，但仍有方向明确的变化；末端64个分子应作为这条25 ps记录的末态数量来读。若目标是报告平衡吸附量，下一步就从稀水与较满的起点分别延长交换采样，比较后段分布、交换活动及重复之间的一致程度，再选择用于平均的窗口。

接受率本身也不是越大越好。一次容易接受的很小变化，可能只在很窄的状态范围内来回移动；一次较难接受的加入，可能打开原来访问不到的分子数状态。评估方法时，需要看它在相同计算投入下，能否有效访问研究所需的数量和构象。这里每批100次交换保留了简单、可读的节奏；对更密集的流体或更复杂的分子，可以进一步研究偏置插入、构象采样与其他适合该体系的交换策略。

温度曲线与势能曲线也有各自的解释。水组的温度由动能定义，热浴使其围绕300 K变化；体系总势能则随着新增相互作用和分子重新排列整体下降。因为粒子数在变，总势能下降同时包含“加入了更多有相互作用的分子”这一因素，不能直接把整段下降除以时间当作释放热量的速率。若要计算吸附能或吸附热，需要明确参照态、交换能量定义及所需的平衡统计。

还有一个容易忽略的采样细节：相邻保存帧通常彼此相关。0.25 ps间隔便于看清变化，但不会自动创造101次独立实验。分块统计可以显示时间窗口敏感性，独立随机种子与不同初态的重复则提供另一层比较。把这些设计接到具体问题上，就能决定增加采样最值得放在哪里：交换太少时关注状态访问，空间分布仍在变化时关注结构调整，不同起点给出不同后段分布时关注初态依赖。

## 从分子计数走向空间分布

总数告诉我们盒子里有多少水，密度图则回答水在哪里。沿x方向把盒子切成60个薄片，逐帧数每片包含多少个水氧，再在指定时间窗口内取平均。因为每个水有一个氧，这相当于给水分子指定一个清楚的位置代表。用平均数除以薄片体积，得到数密度，单位是每立方纳米的分子数。切片宽度、横截面积和平均窗口都进入这个定义，任何一项改变都应在图注中说明。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s7)

图 4 · 密度按完整几何切片体积计算。孔内可达体积是另一个需要探针与几何定义的量；切片图保留固定的空间分母。

由切片计数得到数密度式 4

![由切片计数得到数密度](https://ml-biomat.com/static/agent-math/832ed25783cf5882a6aa84c6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρj | 第j个切片的时间平均水分子数密度 | nm⁻³ |
| Nj,k | 第k帧第j切片内的水氧数 | 个 |
| M、k、j | 采用的帧数、帧编号与切片编号 | 无量纲 |
| Vj | 完整几何切片体积 | nm³ |
| Ly、Lz、Δx | 盒子的y、z长度和x方向切片宽度 | nm |
| ∑、Δ | 把各帧计数相加；区间宽度 | 运算符 |
| =、+、−、×、/ | 相等、相加、相减、乘法、除法；分数横线同样表示除法。 | 运算符 |

怎样理解先按相同时间权重平均每片数量，再除以该片体积。各片ρjVj相加应恢复平均总数。

算一个例子若横截面2 nm²、片宽0.1 nm，体积0.2 nm³；50帧累计200个水氧记录，平均每片4个水，密度4/0.2=20 nm⁻³。

使用条件本例盒子固定，按完整切片体积归一化；孔内可达体积密度需要另行定义分母。

本例横截面积由固定盒子的y、z边长相乘得到，每片使用完整截面。这个体积包含该片中可能被固体占据的部分，因此得到的是按整个几何切片归一化的数密度。若要报告水在可进入孔体积中的平均密度，需要另行定义探针大小与可达体积。两种定义都可以有用途，关键是把分母对应的空间说清楚。这里把固体原子数密度放在同一x轴下方，帮助读者看到哪里固体稠密，哪里形成裂隙。

### 水与固体的空间分布

60个等宽x切片，水在12.5<t≤25 ps的50帧平均；两图都按完整切片体积归一化。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s7)

沿x方向60个等宽切片的数密度。水按12.5 < t ≤ 25 ps的50帧平均，固体位置固定；分母采用完整切片体积，积分恢复平均分子数或原子数。

12.5<t≤25 ps的50帧中，水的平均数量为60.98，样本标准差约1.545。水密度主要集中在低固体密度的裂隙区域，左右并不完全对称，这与实际不规则几何相联系。把每片数密度乘回它的体积，再把60片相加，可以恢复60.98这个平均总数。这个积分检查把曲线的高度、单位和总量联系起来，能够及时发现忘记Å与nm换算、误把氢也当成一个水，或对每帧按变化的总数归一化等问题。

还可以直接量水与固体的距离。对每个水氧，寻找它到任一Si或固体O的最短周期距离；距离不超过3.5 Å时，记为一个近表面水。即使同一个水靠近多个固体原子，也只计一次。后段平均约16.9个水满足这一规则。这个数字描述选定距离壳层里的分子数量，阈值越大，划入的空间通常越多。它与盒内全部60.98个水的平均数不同，也没有自动给每个水分子赋予一个固定吸附位点。

由于基底电荷为0、表面没有显式羟基，这个距离计数表达的是几何邻近。研究表面氢键时，应采用具有相应供体与受体化学的模型，再结合距离与方向判据。研究分子驻留时，还要沿时间追踪同一身份，并区分它是真正移出某个区域，还是被GCMC删除。变量粒子数轨迹中，数组的第十行并不保证在下一帧仍是同一个原子；程序因此读取每帧的原子编号、分子编号和类型，不按固定行号猜测身份。

### 同一裂隙的三个实际时刻

0、5、25 ps的xz投影，显示Si、固体O与水O；省略水H以清楚辨认分子位置。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/#zh-s7)

原生0、5、25 ps坐标的xz投影，显示固定Si、固体O和水O。省略H以便辨认水分子位置；各时刻分子数量由实际轨迹确定。

三个投影快照分别取0、5和25 ps，水分子数为3、46和64。它们把数量增长与裂隙中的实际位置放在一起，水氧用同一种颜色表示，固体Si与O分开标色。投影会把不同y位置的原子叠到同一平面上，所以看似重叠的点不一定在三维空间中重合。完整分析程序保留三维坐标和周期距离计算，图形则承担概括空间组织的作用；将两者配合，能既看清结构，也保持测量定义准确。

### 完整数量、交换与空间分析

```
"""Read a variable-population GCMC/MD trajectory and its exchange record.

python analyze_adsorption.py --run . --out figures --language en
Dependencies: NumPy and Matplotlib.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    with path.open(encoding='utf-8') as f:
        while line := f.readline():
            if line.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a timestep header.')
            step = int(f.readline())
            if f.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Expected an atom-count header.')
            n = int(f.readline())
            header = f.readline().split()
            if header != ['ITEM:', 'BOX', 'BOUNDS', 'pp', 'pp', 'pp']:
                raise ValueError('This analysis expects the orthogonal periodic cell.')
            box = np.array([list(map(float, f.readline().split())) for _ in range(3)])
            names = f.readline().split()[2:]
            values = np.array([list(map(float, f.readline().split())) for _ in range(n)])
            if values.shape != (n, len(names)) or not np.isfinite(values).all():
                raise ValueError('Incomplete or non-finite atom records.')
            data = {name: values[:, i] for i, name in enumerate(names)}
            if len(np.unique(data['id'])) != n:
                raise ValueError('Atom identifiers must be unique within a frame.')
            yield step, box, data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, default=Path('.'))
    ap.add_argument('--out', type=Path, default=Path('figures'))
    ap.add_argument('--language', choices=['zh', 'en'], default='en')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'; tr = lambda z, e: z if zh else e
    names = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Source Han Sans SC', 'Noto Sans CJK SC',
                         'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in names]
    plt.rcParams.update({'font.family': fonts if zh else ['DejaVu Sans'], 'font.size': 12,
        'svg.fonttype': 'path', 'axes.unicode_minus': False, 'axes.spines.top': False,
        'axes.spines.right': False, 'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2'})
    thermo = np.loadtxt(args.run / 'adsorption-thermo.dat', comments='#')
    if thermo.ndim != 2 or thermo.shape[1] != 10 or not np.isfinite(thermo).all():
        raise ValueError('Expected ten finite thermo columns.')
    if np.any(np.diff(thermo[:, 0]) <= 0):
        raise ValueError('Thermo steps must increase.')
    initial = int(thermo[0, 5]); counts = []; reference = None; bins = None
    hist = []; nearest = []; snapshots = []; boxes = []; water_positions = []
    for step, box, d in frames(args.run / 'adsorption.lammpstrj'):
        typ = d['type'].astype(int); ids = d['id'].astype(int); mol = d['mol'].astype(int)
        xyz = np.column_stack([d[k] for k in ['x', 'y', 'z']])
        substrate = typ <= 2; ow = typ == 3; hw = typ == 4
        order = np.argsort(ids[substrate]); solid = xyz[substrate][order]
        if np.count_nonzero(substrate) != 720 or np.count_nonzero(hw) != 2*np.count_nonzero(ow):
            raise ValueError('Expected 720 substrate atoms and intact three-site water molecules.')
        if reference is None:
            reference = solid.copy(); bounds = box.copy()
            bins = np.linspace(box[0, 0], box[0, 1], 61)
        if not np.array_equal(box, bounds) or not np.array_equal(solid, reference):
            raise ValueError('The substrate and cell must remain fixed.')
        for m in np.unique(mol[ow]):
            if sorted(typ[mol == m].tolist()) != [3, 4, 4]:
                raise ValueError('Water molecule identity or composition changed.')
        water = xyz[ow]; lengths = box[:, 1]-box[:, 0]
        dx = water[:, None, :]-solid[None, :, :]
        dx -= lengths*np.rint(dx/lengths)
        distance = np.sqrt((dx*dx).sum(axis=2)).min(axis=1)
        counts.append([step, step*.001, len(water), len(ids), int(np.count_nonzero(distance <= 3.5))])
        hist.append(np.histogram(water[:, 0], bins)[0]); nearest.append(distance)
        snapshots.append((typ.copy(), xyz.copy())); boxes.append(box)
        water_positions.append(water)
    counts = np.array(counts); hist = np.array(hist)
    if not np.array_equal(counts[:, 0], thermo[:, 0]) or not np.array_equal(counts[:, 2], thermo[:, 5]):
        raise ValueError('Coordinate populations and thermo populations disagree.')
    balance = initial+thermo[:, 7]-thermo[:, 9]
    if not np.array_equal(balance, thermo[:, 5]):
        raise ValueError('Insertion/deletion mass balance failed.')
    times = counts[:, 1]; later = (times > 12.5) & (times <= 25)
    widths = np.diff(bins); area = np.prod(bounds[1:, 1]-bounds[1:, 0])
    rho = hist[later].mean(axis=0)/(area*widths)*1000  # molecules per nm^3
    centres = (bins[:-1]+bins[1:])/2
    solid_rho = np.histogram(reference[:, 0], bins)[0]/(area*widths)*1000
    blocks = []
    for lo, hi in [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25)]:
        start = thermo[np.isclose(times, lo)][0]; end = thermo[np.isclose(times, hi)][0]
        delta = end[6:10]-start[6:10]; mask = (times > lo) & (times <= hi)
        blocks.append([lo, hi, thermo[mask, 5].mean(), thermo[mask, 2].mean(), *delta,
                       delta[1]/delta[0], delta[3]/delta[2]])
    blocks = np.array(blocks)
    summary = {'frames': len(times), 'time_ps': [float(times[0]), float(times[-1])],
        'fixed_substrate_atoms': 720, 'initial_water': initial, 'final_water': int(thermo[-1, 5]),
        'final_atom_count': int(counts[-1, 3]), 'reservoir_pressure_bar': 100, 'temperature_target_K': 300,
        'insertion_attempts': int(thermo[-1, 6]), 'insertion_successes': int(thermo[-1, 7]),
        'deletion_attempts': int(thermo[-1, 8]), 'deletion_successes': int(thermo[-1, 9]),
        'insertion_acceptance': float(thermo[-1, 7]/thermo[-1, 6]),
        'deletion_acceptance': float(thermo[-1, 9]/thermo[-1, 8]),
        'mass_balance_max_error': float(np.max(np.abs(balance-thermo[:, 5]))),
        'box_lengths_A': (bounds[:, 1]-bounds[:, 0]).tolist(), 'box_volume_nm3': float(np.prod(bounds[:, 1]-bounds[:, 0])/1000),
        'later_window_ps': '(12.5,25]', 'later_frames': int(later.sum()),
        'later_water_mean': float(thermo[later, 5].mean()), 'later_water_sd': float(thermo[later, 5].std(ddof=1)),
        'later_temperature_mean_K': float(thermo[later, 2].mean()),
        'later_temperature_sd_K': float(thermo[later, 2].std(ddof=1)),
        'later_near_solid_water_mean': float(counts[later, 4].mean()),
        'near_solid_definition': 'Each water oxygen within 3.5 A of any Si/O atom is counted once, using orthogonal minimum-image distances.',
        'density_integral_water_count': float(np.sum(rho/1000*widths*area)),
        'blocks_5ps': [dict(zip(['start_ps','end_ps','water_mean','temperature_mean_K','insert_attempts','insert_successes','delete_attempts','delete_successes','insert_acceptance','delete_acceptance'], row)) for row in blocks],
        'definition': 'Time follows the hybrid MD clock. GCMC insertions and deletions exchange molecules with the reservoir. Densities use the full slice volume and an average over 50 equally spaced frames; the changing water population is retained in the number density.'}
    (args.out/'adsorption_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out/'adsorption_counts.csv', counts, delimiter=',', comments='', header='step,time_ps,water_count,atom_count,water_within3p5A_solid')
    np.savetxt(args.out/'adsorption_blocks.csv', blocks, delimiter=',', comments='', header='start_ps,end_ps,water_mean,temperature_mean_K,insert_attempts,insert_successes,delete_attempts,delete_successes,insert_acceptance,delete_acceptance')
    np.savetxt(args.out/'adsorption_density.csv', np.column_stack([centres/10,rho,solid_rho]), delimiter=',', comments='', header='x_nm,water_number_density_nm-3,substrate_number_density_nm-3')
    def save(fig, name):
        fig.savefig(args.out/(name+'.svg'), bbox_inches='tight')
        fig.savefig(args.out/(name+'.png'), dpi=160, bbox_inches='tight'); plt.close(fig)
    teal, orange, blue = '#147d85', '#c46938', '#4876b7'
    fig, ax = plt.subplots(3,1,figsize=(10.5,9),sharex=True,layout='constrained')
    ax[0].step(times,thermo[:,5],where='mid',color=teal,label=tr('水分子数','Water molecules'))
    ax[0].plot(times,balance,'o',ms=2.5,mfc='none',color=orange,label=tr('3 + 接受插入 − 接受删除','3 + accepted insertions − accepted deletions'))
    ax[0].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=1,fontsize=10)
    ax[0].set(ylabel=tr('分子数','Molecule count'),ylim=(0,70))
    ax[1].plot(times,thermo[:,2],color=blue);ax[1].axhline(300,color=orange,ls='--')
    ax[1].set(ylabel=tr('水温度 / K','Water temperature / K'))
    ax[2].plot(times,thermo[:,3],color=teal);ax[2].set(ylabel=tr('体系势能 / eV','System potential energy / eV'),xlabel=tr('MD累计时间 / ps','Accumulated MD time / ps'))
    save(fig,'adsorption-history')
    fig,ax=plt.subplots(2,1,figsize=(10.5,7),sharex=True,layout='constrained')
    x=np.arange(5);labels=[f'{int(a)}–{int(b)}' for a,b in blocks[:,:2]]
    ax[0].bar(x-.18,100*blocks[:,-2],.36,color=teal,label=tr('插入','Insertion'))
    ax[0].bar(x+.18,100*blocks[:,-1],.36,color=orange,label=tr('删除','Deletion'))
    ax[0].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=2)
    ax[0].set(ylabel=tr('尝试接受比例 / %','Accepted attempts / %'))
    ax[1].bar(x,blocks[:,2],color=blue);ax[1].set(ylabel=tr('窗口平均水分子数','Mean water count in window'),xticks=x,xticklabels=labels,xlabel=tr('MD时间窗口 / ps','MD time window / ps'),ylim=(0,70))
    save(fig,'adsorption-exchanges')
    fig,ax=plt.subplots(2,1,figsize=(10.5,7.5),sharex=True,layout='constrained')
    ax[0].plot(centres/10,rho,color=teal);ax[0].fill_between(centres/10,0,rho,color=teal,alpha=.15)
    ax[0].set(ylabel=tr('水数密度 / nm⁻³','Water number density / nm⁻³'),title=tr('12.5 < t ≤ 25 ps；按完整切片体积归一化','12.5 < t ≤ 25 ps; normalized by full slice volume'))
    ax[1].plot(centres/10,solid_rho,color=orange);ax[1].set(ylabel=tr('固体原子数密度 / nm⁻³','Solid-atom number density / nm⁻³'),xlabel='x / nm')
    save(fig,'adsorption-density')
    fig,ax=plt.subplots(1,3,figsize=(13,2.9),sharex=True,sharey=True,layout='constrained')
    for panel,t in zip(ax,[0,5,25]):
        i=int(np.flatnonzero(np.isclose(times,t))[0]);typ,xyz=snapshots[i]
        panel.scatter(xyz[typ==1,0]/10,xyz[typ==1,2]/10,s=9,c='#b79d62',alpha=.6,label='Si')
        panel.scatter(xyz[typ==2,0]/10,xyz[typ==2,2]/10,s=7,c='#ba7464',alpha=.45,label=tr('固体O','Solid O'))
        panel.scatter(xyz[typ==3,0]/10,xyz[typ==3,2]/10,s=22,c=teal,label=tr('水O','Water O'))
        panel.set(title=f'{t} ps · {int(counts[i,2])} '+tr('个水','waters'),xlabel='x / nm',xlim=bounds[0]/10,ylim=bounds[2]/10);panel.set_aspect('equal')
    ax[0].set_ylabel('z / nm');handles,labels=ax[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=3)
    save(fig,'adsorption-snapshots')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
```

执行python analyze_adsorption.py --run . --out figures --language zh。仅读取两份原始记录，输出图与CSV。

## 把一个吸附算例发展成材料比较

完成这个例题后，已经可以设计一个清楚的比较：固定同一裂隙几何、水模型和温度，在多个储库条件下重复计算，得到平均水数量随压力或逸度变化的关系。每个点都需要自己的准备与采样检查，不能把单条100 bar轨迹中的不同时间点当成不同压力下的平衡状态。“等温线”中的等温是温度相同，横轴上的每个压力点则对应一个独立规定的热力学条件。

对真实水蒸气，储库的状态需要用合适的热力学描述接入。理想储库把逸度系数设为1，压力直接进入化学势关系；使用非理想状态方程时，则以逸度修正供给倾向。相对湿度还涉及给定温度下的饱和蒸气压。把这些关系接好以后，模拟横轴才能与具体实验环境对应。当前100 bar参数提供的是明确的理想储库驱动条件，课程中的数值和曲线都按这个条件解释。

材料之间的比较还可以分成几何与化学两类。改变裂隙宽度而保留作用参数，主要考察可达空间与限域；保留坐标而改变经过验证的表面参数，则考察相互作用。真实表面羟基化会同时改变原子组成、电荷与局部几何，应作为完整模型来建立，而不是随意给某个原子加电荷。将变化因素逐项控制，得到的密度和数量差异才容易对应到具体材料机制。

若研究关注动力学，可以从经过充分采样的含水构型出发，关闭分子交换，保留明确的温度与边界条件，再跟踪水分子的连续运动。这样得到的位移、取向变化与驻留记录，有自己的时间含义。若关注基底软化或裂面变形，则需要让固体也按匹配的势函数运动，并检查水—固体交叉作用。每个扩展都由研究问题决定新增哪些自由度，使模型复杂度服务于想测量的量。

本讲的练习可以直接从现有数据开始：把平均窗口改为最后5 ps，比较水数量与密度图怎样变化；再把切片数从60改为30，检查峰形变平滑时总量积分是否保持。第一个操作改变观察时间，第二个改变空间分辨率，它们都不改动原轨迹。完成这些练习后，吸附便不再只是“分子粘在表面”的一句话，而是一组可以逐项回答的问题：环境提供怎样的交换条件，孔壁保留哪些作用，分子访问哪些状态，以及怎样把这些状态转成可比较的材料性质。

## 延伸阅读与开放资料

- [Water adsorption in silica](https://lammpstutorials.github.io/sphinx/build/html/tutorial6/water-adsorption-in-silica.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY4.0

  固定裂隙、TIP4P水和GCMC/MD基本流程

  保留原参数与25 ps流程；采用准备好的基底，增加数值记录与分析。
- [The adsorption of gases on plane surfaces of glass, mica and platinum](https://doi.org/10.1021/ja02242a004) · Irving Langmuir · Scholarly citation

  1918年表面吸附研究与位点模型背景
- [Surface chemistry: Nobel lecture](https://www.nobelprize.org/uploads/2018/06/langmuir-lecture.pdf) · Irving Langmuir · Scholarly citation

  1932年对吸附及表面作用的回顾
- [fix gcmc command](https://docs.lammps.org/fix_gcmc.html) · LAMMPS developers · Official documentation

  储库、压力覆盖化学势、分子约束与计数含义
- [units command](https://docs.lammps.org/units.html) · LAMMPS developers · Official documentation

  metal单位中的ps、Å、eV与bar
- [TIP4P water models](https://docs.lammps.org/Howto_tip4p.html) · LAMMPS developers · Official documentation

  四位点几何与虚拟负电荷位置
