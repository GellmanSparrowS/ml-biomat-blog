# 流动的阻力从哪里来

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l11/
Language: zh-CN

让两面墙朝相反方向运动，从水分子的速度、壁面受力与温度记录中读懂剪切，并亲手测量限域盐水的一段流动。

## 把水夹在两块滑动的表面之间

把手掌隔着一层水在玻璃上推过去，水会改变手掌感到的阻力。类似的问题也出现在涂布材料、润滑接触和微流体装置中：液体贴近表面以后，怎样被带着走，又怎样把阻力传回表面？当间隙缩小到几个分子的宽度，表面附近的水分子会出现分层，离子周围还带着各自的水化环境。这时，一杯盐水的平均性质与夹在两面墙之间的盐水可以呈现不同的响应。分子模拟能把这种差别展开成可观察的运动与可测量的力。

本讲让两面墙沿相反方向滑动。上壁向右，下壁向左，盐水在它们之间被剪切。这里的“剪切”可以先理解为一叠纸牌的层间错动：相邻纸片沿横向移动不同距离，整叠纸的上部和下部便发生相对位移。液体中的层不是固定纸片，分子不断穿过层与层的分界；我们仍可按高度统计平均速度，由此描述不同位置的液体怎样相互错动。这个平均速度场，是从原子的随机运动走向流体描述的一座桥。

读完本讲，你可以运行一套包含水、钠离子、氯离子和显式壁面的LAMMPS案例，找到施加壁速、控制温度和记录受力的命令，画出沿窄缝高度变化的速度剖面，再把壁面阻力与液体内部的速度梯度配对。最终得到的数值有明确的对象：300 K附近、指定相互作用与壁面结构、上下壁各以20 m/s运动时，这段限域盐水在给定时间窗口中的应力与速度梯度之比。温度、几何、驱动和统计窗口共同构成这次测量的条件。

先分清三个方向会让后面的输入容易很多。x是墙移动的方向，z是从下壁指向上壁的方向，y沿着墙面并与x垂直。模拟盒在x、y方向周期重复，因此一小块墙面代表连续平铺的界面；z方向由两面真实的原子墙包围。盒子尺寸固定，墙的原子仍能在部分方向上热运动。这与把整个周期盒均匀拉斜的剪切方法采用不同的加载方式：本讲通过表面向液体传递动量，适合研究液体与界面的配合。

轨迹中的分子会跑得比平均流动更快，方向也不断变化。肉眼追踪几个分子，很容易把这种热运动误认成流动紊乱。我们的任务是把不同信息分别测出来：平均速度回答液体总体往哪里走，温度描述相关自由度中的动能，壁面合力描述维持运动需要多大阻力，空间密度则告诉我们液体在什么位置聚集。每一个量都有自己的定义，画在同一张图上之前，应先知道它来自哪些原子、哪些方向和哪些时刻。

### 受驱动的窄缝盐水

实际剪切轨迹，时间从墙开始滑动计起；原子运动与后面的分箱统计来自同一运行。

LAMMPS 30 Sep 2026 Update 1；Gravelle等人的纳米剪切电解质例，TIP4P/2005水，300 K，real单位，x/y周期边界、z固定边界；30 ps准备后进行200 ps剪切。

[下载参考数据与完整输入（ZIP） 19.29 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-electrolyte-shear-data.zip)

## 从旋转圆筒到纳米窄缝

今天人们说一种液体“黏”，往往会想到它倒出来慢、搅起来费力。把这种经验变成可比较的物理量，需要同时规定运动和测量方式。Couette在1890年的《液体摩擦研究》中，把两个问题放在开头：液体内部摩擦系数是否是定义清楚的物理量，以及应当遵循什么规则测量它。他使用同心圆筒等装置，让液体在受控运动的表面之间流动，再通过维持内筒静止所需的力矩读出液体的作用。圆筒几何把持续运动与持续受力连接起来，使“黏”有了可重复的实验安排。

力矩可以理解为力使物体转动的能力。同样大小的力，作用点离转轴越远，转动效果通常越明显，所以圆筒实验需要同时知道力的作用和装置尺寸。我们把圆筒之间的一小段弧形间隙在想象中展开，就得到两块平行表面之间的局部剪切。这个变换保留了由表面带动液体、从阻力测量响应的思想；在计算时，平板与圆筒仍分别使用各自的几何关系。本讲采用平板，是为了把空间分箱、速度梯度和壁面合力讲得直观。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s2)

图 1 · Couette的同心圆筒实验将受控运动与测得的力矩联系起来；右侧用局部平板示意把同一测量思想接到纳米剪切。图是原理示意，圆筒与窄缝采用不同几何。

液体传递阻力，并不是因为其中藏着许多彼此焊接的固体薄板。靠近上壁的分子受壁面作用获得横向动量，又通过碰撞和分子间相互作用把动量传给其他分子。下壁施加相反方向的运动，两种作用在液体内部建立速度差。分子不断交换位置，动量也不断在位置之间转移。宏观的黏性应力把大量这样的交换概括成单位面积上的切向作用力，而分子模拟让我们能够同时看到微观交换所依赖的结构。

一个熟悉的类比是两排人分别朝相反方向走动，中间的人通过接触把推力传递过去。类比帮助理解动量传递，却不需要把分子想成有目的地传递消息的人。分子的运动由力、质量和当前速度决定，水的带电位置、离子的电荷以及壁面势都进入这些力的计算。只要统计的时间和空间足够组织起许多这样的相互作用，杂乱的单个运动就能形成较平滑的平均速度剖面。

科学史在这里给出了一条实用的测量思路：先控制运动，再测量响应，并检查所用关系在哪一段条件下成立。对于牛顿流体，在一定温度和较小剪切速率范围内，应力与速度梯度近似成正比，比例系数就是黏度。对于界面附近的水、聚合物溶液或高驱动下的液体，改变速率还可能改变结构和响应。于是，同一套模拟既可以测某一驱动下的比值，也可以通过一系列驱动测量讨论这种比值是否保持稳定；两项研究由不同的数据设计来支撑。

## 流动的模型保留了哪些分子细节

我们从一套完整的限域盐水模型出发。体系有406个水分子、15个钠离子、15个氯离子和432个壁面原子，总计1680个显式原子。水使用TIP4P/2005模型，每个水的氧和两个氢具有明确位置，负电荷的作用位置M由水的几何关系计算，因此名称中的“四点”与轨迹里的“三个原子”可以同时成立。正负离子数相等使整体电中性，但每个离子仍会与周围水分子的电荷位置相互作用；整体不带净电荷，绝不意味着内部没有静电作用。

水分子的O—H距离保持在0.9572 Å，H—O—H角保持在104.52°，SHAKE约束负责维持这些几何条件。约束使本例把注意力放在分子的平移、转动和周围环境的重排上。水分子的伸缩振动、化学键断裂与质子转移属于另一些研究对象，需要相应的可变键或电子结构描述。本讲的固定连接关系清楚地规定了模型保留哪些运动，也决定了温度计算时需要扣除哪些自由度。

壁面由中性原子组成，使用输入中给出的质量与Lennard-Jones相互作用参数。这样的墙能够形成有结构的分子接触面，能够受力并向水传递动量。它没有额外的表面电荷、羟基反应或电子响应，因此本例研究的是这套明确的中性壁面势与盐水的相互配合。若要讨论带电生物材料表面，下一步是给出相应的表面化学和电荷状态，再沿用本讲的速度、受力与空间统计方法，而不是把墙的材料名称直接换成另一种材料。

非键相互作用也要成套理解。专用的TIP4P长程静电处理会把负电荷作用在隐式M位置，不能用普通的氧位置电荷计算代替。x、y方向周期重复，z方向采用固定边界，同时使用slab修正处理平板几何中的长程静电。这个数值设置改变的是周期镜像之间的处理方式；两面墙之间真实的z方向静电作用仍然参与分子受力。这样，我们在一个有限盒子中构造出沿墙面延展的窄缝。

单个周期壁面的边长是24.24 Å，即2.424 nm。先用数量级把它放回日常尺度：1 nm等于十亿分之一米，一根头发的直径远大于这里的整个盒子。模拟中的表面面积虽然小，仍可通过周期重复描述均匀延展界面的一块代表区域。它适合研究均匀表面附近的局部结构与流动；大的表面缺陷、粗糙度分布或不同化学区域，需要在几何中明确加入相应尺度。所选周期尺寸决定哪些空间变化能在这一次计算里出现。

模型的物理内容最后落在输入文件里。`water.mol`给出水的几何和连接模板，`parameters.inc`给出质量、电荷和相互作用，`groups.inc`把水、离子、流体和上下壁分开。分组不只是给原子起名称：后面的温控、约束、施力和分析都使用这些选择。把分组读清楚，便能知道某条命令究竟改变了哪个对象，也能避免把壁面原子的运动混进液体的流速统计。

### 完整输入：water.mol

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

1        O
2        H
3        H

Charges

1       -1.1128
2        0.5564
3        0.5564

Bonds

1   O-H      1      2
2   O-H      1      3

Angles

1   H-O-H    2      1      3

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 O-H O-H H-O-H
2 O-H O-H H-O-H
3 O-H O-H H-O-H

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

### 完整输入：parameters.inc

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

mass O 15.9994
mass H 1.008
mass Na+ 22.990
mass Cl- 35.453
mass WALL 26.9815

pair_coeff O O 0.185199 3.1589
pair_coeff H H 0.0 1.0
pair_coeff Na+ Na+ 0.04690 2.4299
pair_coeff Cl- Cl- 0.1500 4.04470
pair_coeff WALL WALL 11.697 2.574
pair_coeff O WALL 0.4 2.86645

bond_coeff O-H 0 0.9572
angle_coeff H-O-H 0 104.52
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

### 完整输入：groups.inc

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

group H2O type O H
group Na type Na+
group Cl type Cl-
group ions union Na Cl
group fluid union H2O ions

group wall type WALL
region rtop block INF INF INF INF 0 INF
region rbot block INF INF INF INF INF 0
group top region rtop
group bot region rbot
group walltop intersect wall top
group wallbot intersect wall bot
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

## 平均流动和热运动怎样分开

假设一小片液体总体向右流动，里面的某个水分子仍可能在某个瞬间向左运动。这并不矛盾：平均流动描述许多分子的方向性趋势，单个分子的速度还包含热起伏。可以把速度想成在移动的人行道上走路：相对于地面的速度，是人行道速度与相对于人行道的走动速度相加。液体没有一条真实的人行道，我们用当前位置附近的平均流速来定义这个移动参照。

有方向的流动与横向温度式 3

![有方向的流动与横向温度](https://ml-biomat.com/static/agent-math/ba77495ddc5483bf11fa11e9.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| vᵢ,ₓ | 原子i的完整x速度 | m/s |
| uₓ(zᵢ) | 原子所在高度的平均流速 | m/s |
| cᵢ,ₓ | 相对于平均流动的速度起伏 | m/s |
| Tᵧz | 采用y、z速度分量定义的温度 | K |
| Kᵧz | 对应速度分量的总动能 | J |
| fᵧz | 扣除约束及平移修正后的有效自由度 | 无量纲 |
| kB | 玻尔兹曼常数1.380649×10⁻²³ | J/K |
| i、zᵢ | 原子编号及其高度 | 无量纲；m |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |
| 2 | 每个二次动能自由度平均能量为kBT/2，所以从动能换算温度时乘二。 | 无量纲 |

怎样理解完整速度由局部平均与相对起伏相加。每个经典二次动能自由度平均贡献kBT/2，因此横向动能除以相应自由度给出温度。

算一个例子教学算例取fᵧz=1000、T=300K，则Kᵧz=1000×1.380649×10⁻²³×300/2=2.0709735×10⁻¹⁸J。本例水受SHAKE约束，实际自由度由LAMMPS计算。

使用条件这里的分解解释温度定义；实际输入用temp/partial 0 1 1恒温y、z，x方向保留流动并通过分子间作用交换能量。

这个区分直接影响温度控制。若把全部有方向的x速度都当成需要压回目标温度的热运动，温控器可能同时抵消我们希望研究的平均流动。本例采用一个清楚的安排：用y、z方向的速度分量计算温度，并据此对这两个方向恒温。x方向的外加运动得以保留，同时通过原子间相互作用与其他方向交换能量。这样，控制温度与驱动流动承担不同任务，彼此的作用更容易追踪。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s4)

图 2 · 绿色与橙色箭头解释速度的分解，箭头为示意。实际输入对流体与壁分别用y、z分量恒温，保留x方向施加的滑动。

`compute Tfluid fluid temp/partial 0 1 1`中的三个数字依次对应x、y、z。0表示不把该分量计入这个温度定义，1表示计入。紧接着的`fix_modify mynvt1 temp Tfluid`把这个温度计算交给流体的恒温器。墙的原子使用自己的横向温度计算与恒温器，因而流体与壁可以分别把产生的热量传给热浴。这里的热浴是控制温度的算法对象，它通过调整相关运动来实现统计上的温度条件。

水分子的刚性约束使自由度计数更加重要。三个不受约束的原子在三维中有九个位置自由度；固定两个键长和一个夹角后，一个刚性水留下整体平移和转动的自由度。再选择速度方向、扣除整体平移等修正时，程序需要继续按实际选择处理。我们因此读取专用温度计算的结果，不拿“原子数乘二”直接充当本例所有阶段的精确自由度。前面的公式解释温度为什么与动能有关，实际数字则由与约束一致的计算对象给出。

同样要分清热控制与能量守恒的观察。两面墙不断做功，热浴不断交换能量，整个受驱动体系的机械能可以随时间变化。这里更有价值的检查是：墙是否保持目标速度，横向温度是否围绕300 K波动，液体是否建立持续的平均剪切，以及壁面阻力的时间统计是否稳定。若研究孤立体系的积分精度，可以另做无驱动、无热浴的能量守恒测试；本讲的温度与能量记录服务于受驱动的物理条件。

## 用完整输入建立并驱动盐水

把下列文件放进同一个例题目录后，`run.sh`依次执行建模、准备和剪切。第一阶段生成水、离子和墙，保存`create.data`；第二阶段最小化并进行30 ps准备，得到`equilibrate.data`；第三阶段读入这个状态，令两面墙滑动200 ps。data文件保存原子、连接和所需状态，参数文件则在各阶段重新包含进来，使计算继续使用同一套相互作用。第一次运行时，按这三个输出名字查看目录，就能知道计算走到了哪一步。

### 完整输入：create.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

lattice fcc 4.04
region box block -3 3 -3 3 -5 5
create_box 5 box &
  bond/types 1 &
  angle/types 1 &
  extra/bond/per/atom 2 &
  extra/angle/per/atom 1 &
  extra/special/per/atom 2
labelmap atom 1 O 2 H 3 Na+ 4 Cl- 5 WALL
labelmap bond 1 O-H
labelmap angle 1 H-O-H

region rbotwall block -3 3 -3 3 -4 -3
region rtopwall block -3 3 -3 3 3 4
region rwall union 2 rbotwall rtopwall
create_atoms WALL region rwall

region rliquid block INF INF INF INF -2 2
molecule h2omol water.mol
create_atoms 0 region rliquid mol h2omol 482793

create_atoms Na+ random 15 5802 rliquid overlap 0.3 maxtry 500
create_atoms Cl- random 15 9012 rliquid overlap 0.3 maxtry 500
set type Na+ charge 1
set type Cl- charge -1

include parameters.inc
include groups.inc

delete_atoms random fraction 0.15 yes H2O NULL 482793 mol yes


write_dump all custom created.lammpstrj id mol type q x y z ix iy iz modify sort id
run 0

write_data create.data nocoeff
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

### 完整输入：equilibrate.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

read_data create.data

include parameters.inc
include groups.inc

fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H kbond 2000


thermo 1
thermo_style custom step temp etotal press

minimize 1.0e-6 1.0e-6 1000 1000
reset_timestep 0

fix mynvt all nvt temp 300 300 100
fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H
fix myrct all recenter NULL NULL 0
timestep 1.0


variable walltopz equal xcm(walltop,z)
variable wallbotz equal xcm(wallbot,z)
variable deltaz equal v_walltopz-v_wallbotz

thermo 250
thermo_style custom step temp etotal press v_deltaz

# Numerical trajectory and thermodynamic records added to the original tutorial.
dump course all custom 500 equilibrate.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify course sort id
compute coursePE all pe
compute courseKE all ke
compute courseTemp all temp
compute coursePressure all pressure courseTemp
variable courseTime equal time
variable courseT equal c_courseTemp
variable courseU equal c_coursePE
variable courseK equal c_courseKE
variable courseE equal c_coursePE+c_courseKE
variable courseP equal c_coursePressure
thermo_style custom step v_courseT v_courseU v_courseK v_courseE v_courseP v_deltaz
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseK v_courseE v_courseP file equilibrate-thermo.dat

run 30000

write_data equilibrate.data nocoeff





write_restart equilibrate.restart
write_dump all custom equilibrate-final.lammpstrj id mol type q x y z ix iy iz modify sort id
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

剪切阶段的关键操作可以连成一段物理叙述。先定义流体和墙的横向温度，再启用各自的NVT积分与温控，随后加入水分子的SHAKE约束。接着，`fix setforce`把上下壁中每个原子的x向受力设为零，而`velocity set`分别赋给它们固定的正、负x速度。在这个安排下，墙的x速度按输入保持，y、z运动仍参与相应的热动力学过程。这里的墙不是每一步都被整体搬到指定坐标；它通过初速度、x方向零合力和保留该方向运动的积分来持续滑动。

速度单位值得亲手换算一次。`units real`下，长度用Å，时间用fs。1 Å等于10⁻¹⁰ m，1 fs等于10⁻¹⁵ s，因此1 Å/fs等于10⁵ m/s。输入中的2×10⁻⁴ Å/fs便是20 m/s，上下壁之间的速度差为40 m/s。速度看起来很大，跨越的距离却只有纳米量级，所以形成的速度梯度约为每秒10¹⁰量级。这一驱动使短时间内的流动响应容易从热噪声中辨认，也成为结果解释中必须保留的条件。

`fix setforce`还有一个关键功能：它保存取消之前作用在整个分组上的合力。`f_mysf1[1]`和`f_mysf2[1]`因此可以告诉我们流体对上下壁施加了多大的x向作用。力后来被加载装置抵消，并不意味着液体原先没有阻力。想象实验中电机维持圆筒匀速转动，电机输出与液体阻力相平衡；保存取消之前的力，就是读出维持指定运动需要补偿的作用。

### 完整输入：shearing.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

read_data equilibrate.data

include parameters.inc
include groups.inc

compute Tfluid fluid temp/partial 0 1 1
fix mynvt1 fluid nvt temp 300 300 100
fix_modify mynvt1 temp Tfluid

compute Twall wall temp/partial 0 1 1
fix mynvt2 wall nvt temp 300 300 100
fix_modify mynvt2 temp Twall

fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H
fix myrct all recenter NULL NULL 0
timestep 1.0

fix mysf1 walltop setforce 0 NULL NULL
fix mysf2 wallbot setforce 0 NULL NULL
velocity wallbot set -2e-4 NULL NULL
velocity walltop set 2e-4 NULL NULL


thermo 250
thermo_modify temp Tfluid
thermo_style custom step temp etotal f_mysf1[1] f_mysf2[1] 

compute cc1 H2O chunk/atom bin/1d z 0.0 0.25
compute cc2 wall chunk/atom bin/1d z 0.0 0.25
compute cc3 ions chunk/atom bin/1d z 0.0 0.25

fix myac1 H2O ave/chunk 10 15000 200000 &
  cc1 density/mass vx file shearing-water.dat
fix myac2 wall ave/chunk 10 15000 200000 &
  cc2 density/mass vx file shearing-wall.dat
fix myac3 ions ave/chunk 10 15000 200000 &
  cc3 density/mass vx file shearing-ions.dat

# Numerical trajectory and thermodynamic records added to the original tutorial.
dump course all custom 500 shearing.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify course sort id
compute coursePE all pe
compute courseKE all ke
compute courseTemp all temp
compute coursePressure all pressure courseTemp
variable courseTime equal time
variable courseT equal c_Tfluid
variable courseU equal c_coursePE
variable courseK equal c_courseKE
variable courseE equal c_coursePE+c_courseKE
variable courseP equal c_coursePressure
thermo_style custom step v_courseT v_courseU v_courseK v_courseE v_courseP f_mysf1[1] f_mysf2[1]
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseK v_courseE v_courseP file shearing-thermo.dat

run 200000

write_restart shearing.restart
write_dump all custom shearing-final.lammpstrj id mol type q x y z ix iy iz modify sort id
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

### 完整输入：run.sh

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=4
for stage in create equilibrate shearing; do
  "$lmp" -sf omp -pk omp 4 -in "$stage.lmp" -log "$stage.log" > "$stage.stdout.log" 2>&1
done
```

把这些文件放在同一目录，运行bash run.sh依次建模、准备和剪切。

本例每一步为1 fs，200000步覆盖200 ps。轨迹每500步保存一次，因此两个相邻坐标帧相隔0.5 ps，总共401帧；全局温度记录每250步一次。原生空间分箱更密，每10步采样一次，在最后150000步累计15000次，最终只输出一次平均剖面。一次运行因此可以同时拥有稀疏的可播放轨迹和密集的空间统计。读取文件时，要分别看清它们的采样间隔，不能用播放帧数替代原生剖面的样本数。

实际记录中，50到200 ps的横向温度均值为299.978 K，记录之间的标准差约9.816 K。单次记录在目标值上下起伏是这个小体系的正常统计行为，平均值与起伏幅度描述不同信息。每一帧中的两面墙分别保持+20和−20 m/s。下面的图还给出原始壁面应力与50 ps区间平均：先看较密的波动，再看跨越许多记录的平均，比只保留一条平滑曲线更容易理解测量从哪里来。

### 温度与阻力怎样随时间变化

横向温度与取消力之前记录的壁面力；区间均值保留实际波动。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s5)

以壁开始运动为零时刻，温度使用去掉x流动分量后的横向自由度。剪切应力由两壁阻力与投影面积计算，细线保留保存记录，粗线连接50 ps区间的平均。

## 沿窄缝切片，读出速度和层化

一张轨迹展示某一时刻原子在哪里，一条速度剖面则要把许多原子、许多时刻组织到同一坐标体系中。做法像把一条走廊按位置分成若干段，分别统计经过每段的人向哪个方向走。这里沿z把窄缝切成薄片，记录进入每片的水原子速度，并把这些样本累加。分子可以从一个薄片走到另一个薄片；薄片固定在空间中，统计的对象是当时处于其中的原子，而不是一批永远不变的原子编号。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s6)

图 3 · 切片把位置和速度组织成空间统计。实际原生薄片宽0.25Å，采用50.01–200ps的15000次采样；中心拟合范围为−8至8Å。

一个薄片中的平均流速式 1

![一个薄片中的平均流速](https://ml-biomat.com/static/agent-math/4d083dfd2bcd52269169bae6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| uₓ(zⱼ) | 第j个z薄片的平均x速度 | m/s |
| vᵢ,ₓ(s) | 第s次记录中原子i的x速度 | m/s |
| Bⱼ(s) | 该次记录中位于薄片j的原子集合 | 集合 |
| Nⱼ(s) | 该薄片在该次记录中的原子数 | 无量纲 |
| i、j、s | 原子、薄片和记录的编号 | 无量纲 |
| ∑、∈ | 求和；属于给定集合 | 运算符 |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |

怎样理解先累加被记录的每个原子速度，再除以被记录的原子总次数。原子数较多的记录提供较多原子样本，这对应原生norm all的原子数加权。

算一个例子两个时刻分别有2个和1个原子，速度为10、30及50m/s，平均为(10+30+50)/3=30m/s；逐时刻先平均再平均则得到35m/s，属于另一种权重。

使用条件用于本例水、壁和离子的原子速度分箱。水原子平均速度与按分子质心分箱的定义需分别注明。

本例原生剖面把每次记录的原子速度直接汇总，属于原子数加权。设某片在一个时刻有十个原子，另一个时刻只有一个原子，那么前一个时刻提供十次原子观测，后一个提供一次。另一种算法会先算每个时刻的片内平均，再让所有时刻等权；当原子数波动明显时，两种结果会有差别。这里把权重说清楚，是为了让公式、LAMMPS的`norm all`默认值和Python分析对应起来。

密度剖面使用同样的空间切片，但累加的是质量。把某片所有原子的摩尔质量换成真实质量，再除以薄片体积，便得到g/cm³等单位下的密度。靠近壁面的峰表示原子在这些高度出现得更频繁，通常反映壁与液体相互作用形成的层化。峰的位置、宽度和高度都属于空间结构信息；它们与速度曲线各自回答不同问题。一个位置的密度高，并不直接规定那里的流速必须高或低，需要把两张实际曲线放在一起观察。

### 实际分层与速度梯度

来自原生ave/chunk输出的密度与原子平均速度。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s6)

原生分箱以15000次采样形成50.01–200 ps的密度和原子数加权速度剖面。两壁分别以±20 m/s运动，中心|z|≤8 Å范围的线性拟合提供实际速度梯度；靠近壁的层化在原始空间分箱中显示。

速度梯度是剖面随高度变化的斜率。高中数学里，直线斜率是纵坐标变化除以横坐标变化；在这里，若横轴是高度z、纵轴是平均x速度，得到的便是剪切速率。实际分箱曲线有噪声，我们对中心区域多个点拟合直线，比只选择两个点相减更能利用这些记录。本例明确选用−8至8 Å的水速度，得到2.43529 (m/s)/Å。这个选择留在完整分析程序里，读者可以改动范围，观察界面附近的结构怎样影响斜率。

速度随高度改变的速率式 2

![速度随高度改变的速率](https://ml-biomat.com/static/agent-math/e0bc69b7b30fd9b04ba67be5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| γ̇ | 剪切速率，表示速度梯度 | s⁻¹ |
| uₓ | 沿x的平均流速 | m/s |
| z | 垂直于壁的坐标 | m |
| d、Δ | 局部微小变化；选定区间的变化 | 运算符 |
| ≈ | 用有限区间斜率近似局部导数 | 运算符 |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |

怎样理解相邻液层速度不同，单位高度上的速度差描述它们相互错动的快慢。拟合直线斜率把许多薄片的信息结合起来。

算一个例子本例中心斜率2.43529(m/s)/Å，因1Å=10⁻¹⁰m，剪切速率为2.43529×10¹⁰s⁻¹。示意的40m/s速度差跨2nm时得到2×10¹⁰s⁻¹。

使用条件本例对−8≤z≤8Å水速度作直线拟合。平板无滑移公式需另给实际流体边界位置。

讨论“无滑移”或“滑移”时，还要把流体边界面放到正确的位置。原子墙有厚度，最内层原子、整块墙的质心、排斥势形成的有效边界，并不是同一个平面。本例两壁质心的平均间距约27.405 Å，而参与流动的水主要分布在内侧区域。若直接用40 m/s除以墙质心间距，得到的是一个几何估计；若从液体中心实际剖面求斜率，得到的是测量定义明确的内部梯度。二者的差别可以提醒我们检查边界位置，而不必急着把它命名为一种新的界面效应。

下面的交互用一个可算清楚的平板模型，把这种边界问题单独拿出来。读者指定间隙H、墙速U和两面相同的滑移长度b，程序按线性速度场画出流体剖面。b表示把液体直线速度场向墙内延长时需要的额外距离，物理边界处的速度差等于b乘速度梯度。这个模型适合做数量级练习；真实分子轨迹的密度层、有效边界与采样波动仍由前面的记录来判断。

对称滑移的平板算例式 6

![对称滑移的平板算例](https://ml-biomat.com/static/agent-math/adedf7e7e01e21951203d6e0.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U | 上壁速度幅值；下壁为−U | m/s |
| H | 两选定流体边界平面的距离 | m |
| b | 两面相同的Navier滑移长度 | m |
| γ̇ | 平板中心区域的恒定速度梯度 | s⁻¹ |
| uₓ、z | 平均流速及以窄缝中心为零点的高度 | m/s；m |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |
| 2 | 2U为两壁的速度差；2b为两侧各一个滑移长度之和。 | 无量纲 |

怎样理解每一面边界的速度差等于b乘液体速度梯度，因此两壁总速度差由流体内部H和两端各b共同承担。

算一个例子U=20m/s、H=2nm、b=0时γ̇=2×10¹⁰s⁻¹；b=1nm时γ̇=1×10¹⁰s⁻¹，流体边界速度为±10m/s。

使用条件离线交互采用的连续介质示意：平行平板、对称滑移、稳态线性速度场。它的b由读者指定，独立于实际分子轨迹的拟合。

平行平板示意：调节墙速度、流体间隙和滑移长度，观察同一墙速如何对应不同流体梯度。

静态滑块可用方向键调整：Navier平板解析模型中，b=0给出无滑移条件，b增大时同一墙速对应较小液体梯度。

## 从壁面受力走到黏度

流动剖面告诉我们液体被剪切得多快，壁面受力告诉我们维持这样的运动要付出多大作用。上壁向+x移动时，液体平均向−x阻碍它；下壁向−x移动时，液体平均向+x阻碍它。因此，把两面力直接相加会让主要的阻力信号互相抵消。我们先统一符号，用下壁x力减去上壁x力，再除以二，得到两面阻力幅值的平均。对称加载中，两面墙为同一测量提供了两份有联系的记录。

用两面墙的受力测量剪切应力式 4

![用两面墙的受力测量剪切应力](https://ml-biomat.com/static/agent-math/1bd5d65b6b3f6915343f3554.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| τ | 正向阻力幅值对应的剪切应力 | Pa=N/m² |
| Fb,ₓ、Ft,ₓ | 液体对下壁、上壁的x合力 | N |
| ⟨ ⟩ | 指定时间窗口内的平均 | 运算符 |
| A | 单个壁面的投影面积 | m² |
| Lₓ、Lᵧ | 周期盒在x、y方向的长度 | m |
| 2 | 平均两面墙的阻力幅值 | 无量纲 |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |

怎样理解上壁向+x滑动，液体一般向−x阻碍它；下壁方向相反。先统一两面的符号，再取平均，最后除以单壁面积。

算一个例子本例阻力均值2.835339kcal/(mol·Å)。每单位等于4184/(6.02214076×10²³×10⁻¹⁰)=6.94769546×10⁻¹¹N。面积24.24²Å²=5.875776×10⁻¹⁸m²，得到τ=33.5259MPa。

使用条件使用setforce取消x力之前保存的合力，取50<t≤200ps的记录平均；面积包括一次周期平铺的完整壁面。

应力是单位面积上的力，因而面积选择必须与力的对象匹配。我们读到的是一块完整周期壁面分组的合力，使用的就是单块周期壁面的投影面积Lx乘Ly。把面积再乘二会额外稀释结果，因为公式已经先平均了两面墙；把上下壁原子的总表面积逐颗相加，也会换成另一个没有对应实验定义的量。这里的一次受力、一次面积相除，与宏观“多少牛顿作用在多少平方米上”的定义完全一致。

将LAMMPS的力换成牛顿，可以把“每摩尔”这个常见但容易混淆的单位讲透。kcal/mol表示把同一能量尺度按阿伏伽德罗常数倍放大来报告，求一个粒子的能量要除以这个常数。再把对Å的能量变化换成对米的变化，便得到牛顿。本例50到200 ps的阻力均值2.835339 kcal/(mol·Å)，换成力后再除以5.875776×10⁻¹⁸ m²的壁面面积，给出33.5259 MPa。数值大，既与纳米面积有关，也与这次较大的速度梯度有关。

把同一时间窗口的应力除以实际液体速度梯度，得到1.37667 mPa·s。这个比值可以称为该驱动条件下的有效黏度，名称中的“有效”说明它包含本例的空间选择与界面条件。它把复杂轨迹压缩成一个便于比较的量，同时保留明确的测量定义：中心区拟合速度梯度、壁面投影应力、300 K附近的横向温度以及50到200 ps的观测窗口。这样的定义使更换墙参数、盐浓度或温度后的比较能够使用同一个尺子。

把阻力与实际速度梯度配对式 5

![把阻力与实际速度梯度配对](https://ml-biomat.com/static/agent-math/18c9647c9fb4955753ab65eb.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ηeff | 该温度、限域和驱动下的应力/梯度比值 | Pa·s |
| τ | 同一统计窗口的剪切应力 | Pa |
| γ̇ | 液体内部测得的剪切速率 | s⁻¹ |
| =、/、+、−、× | 相等；除法；相加；相减；相乘。分数横线同样表示除法。 | 运算符 |

怎样理解在给定剪切速率下，黏度把需要的应力与液层相对错动联系起来。牛顿流体在线性响应区的该比例随速率保持不变；多速率测量可以检验这一条件。

算一个例子33.5259×10⁶Pa除以2.43529×10¹⁰s⁻¹，得到0.00137667Pa·s=1.37667mPa·s。这里的分子与分母均来自同一50–200ps观测窗口。

使用条件这是TIP4P/2005盐水与指定壁面、±20m/s驱动下的有限窗口比值。研究体相零剪切黏度时，另设体相模型和较小速率序列。

完整Python程序既读原生密度和速度分箱，也读更稀疏的轨迹来重建三个连续时间块的剖面。它还输出清洁的壁面力CSV，使参考数据可以直接被复算。程序中的时间、空间和单位转换都写成了明确的数值，因而结果不依赖绘图软件的隐含设置。先用参考数据运行一次，确认你看到相同的图和摘要；再改变一个分析条件，例如中心拟合范围或时间块宽度，就能区分“重新分析同一段数据”与“改变模型重新模拟”这两种工作。

### 完整Python：速度剖面、壁面受力与时间块

```
"""Measure the recorded nanoslit shear flow.

python analyze_shear.py --run . --out figures --language en
Dependencies: NumPy and Matplotlib.
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

def frames(path):
    with path.open(encoding='utf-8') as f:
        while line:=f.readline():
            if line.strip()!='ITEM: TIMESTEP':raise ValueError('Timestep header expected')
            step=int(f.readline());assert f.readline().strip()=='ITEM: NUMBER OF ATOMS'
            n=int(f.readline());header=f.readline().split();assert header[:3]==['ITEM:','BOX','BOUNDS']
            bounds=np.array([list(map(float,f.readline().split())) for _ in range(3)])
            assert bounds.shape==(3,2)
            names=f.readline().split()[2:]
            a=np.array([list(map(float,f.readline().split())) for _ in range(n)])
            a=a[np.argsort(a[:,names.index('id')])]
            yield step,bounds,{key:a[:,j] for j,key in enumerate(names)}

def force_records(run):
    clean=run/'wall-forces.csv'
    if clean.exists():return np.loadtxt(clean,delimiter=',',skiprows=1)
    rows=[];active=False
    for line in (run/'shearing.log').read_text(encoding='utf-8').splitlines():
        if 'Step' in line and 'f_mysf1[1]' in line:active=True;continue
        if active and line.startswith('Loop time'):break
        if active:
            try:values=list(map(float,line.split()))
            except ValueError:continue
            if len(values)==8:rows.append([values[0]/1000,values[-2],values[-1]])
    a=np.array(rows);assert a.shape==(801,3)
    return a

def chunk(path):
    lines=[line for line in path.read_text().splitlines() if line.strip() and not line.startswith('#')]
    step,n,total=map(float,lines[0].split());a=np.array([list(map(float,s.split())) for s in lines[1:]])
    assert step==200000 and len(a)==int(n) and a.shape[1]==5
    return a

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,default=Path('.'));p.add_argument('--out',type=Path,default=Path('figures'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    zh=a.language=='zh';tr=lambda z,e:z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist};family=[f for f in ['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family':family if zh else ['DejaVu Sans'],'font.size':13,'axes.titlesize':15,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#f8f7f2','figure.facecolor':'#f8f7f2','axes.unicode_minus':False})
    colors=['#147d85','#c46938','#4876b7'];thermo=np.loadtxt(a.run/'shearing-thermo.dat',comments='#');forces=force_records(a.run)
    np.savetxt(a.out/'wall-forces.csv',forces,delimiter=',',header='time_ps,force_top_kcal_mol_A,force_bottom_kcal_mol_A',comments='')
    history=[];edges=np.arange(-12,12.0001,1.0);mid=(edges[:-1]+edges[1:])/2
    sums=np.zeros((3,len(mid)));counts=np.zeros_like(sums);block_frame_counts=np.zeros(3,dtype=int)
    for step,bounds,d in frames(a.run/'shearing.lammpstrj'):
        typ=d['type'].astype(int);z=d['z'];wall=typ==5;top=wall&(z>0);bottom=wall&(z<0);fluid=typ<5
        assert len(typ)==1680
        area=np.prod(bounds[:2,1]-bounds[:2,0]);gap=z[top].mean()-z[bottom].mean()
        history.append([step/1000,gap,d['vx'][top].mean()*1e5,d['vx'][bottom].mean()*1e5])
        if 50000 < step <= 200000:
            block=int((step-50001)//50000);sel=typ<=2
            block_frame_counts[block]+=1
            sums[block]+=np.histogram(z[sel],edges,weights=d['vx'][sel]*1e5)[0]
            counts[block]+=np.histogram(z[sel],edges)[0]
    h=np.array(history);assert h.shape==(401,4)
    assert np.allclose(h[:,2],20,atol=1e-9) and np.allclose(h[:,3],-20,atol=1e-9)
    water=chunk(a.run/'shearing-water.dat');walls=chunk(a.run/'shearing-wall.dat');ions=chunk(a.run/'shearing-ions.dat')
    fit=(abs(water[:,1])<=8)&(water[:,2]>0)
    slope,intercept=np.polyfit(water[fit,1],water[fit,4]*1e5,1)
    shear_rate=slope*1e10
    last=(forces[:,0]>50)&(forces[:,0]<=200)
    fdrag=(forces[:,2]-forces[:,1])/2
    force_to_newton=4184/(6.02214076e23*1e-10);stress=fdrag*force_to_newton/(area*1e-20)
    native_temp=(thermo[:,1]>50000)&(thermo[:,1]<=200000)
    block_rows=[]
    for i in range(3):
        lo,hi=50+50*i,100+50*i;mask=(forces[:,0]>lo)&(forces[:,0]<=hi)
        profile=np.divide(sums[i],counts[i],out=np.full(len(mid),np.nan),where=counts[i]>0)
        m=(abs(mid)<=8)&np.isfinite(profile);b,c=np.polyfit(mid[m],profile[m],1)
        block_rows.append([lo,hi,float(stress[mask].mean()/1e6),b,b*1e10,float(stress[mask].mean()/(b*1e10)*1e3)])
    blocks=np.array(block_rows)
    assert block_frame_counts.tolist()==[100,100,100]
    summary={'native_averaging_time_ps':[50.01,200],'native_samples':15000,'native_profile_bin_A':.25,'trajectory_frames':len(h),'wall_speeds_m_s':[20,-20],'wall_center_gap_mean_A':float(h[h[:,0]>50,1].mean()),'area_A2':float(area),'temperature_yz_mean_K':float(thermo[native_temp,2].mean()),'temperature_yz_sd_K':float(thermo[native_temp,2].std(ddof=1)),'mean_drag_force_kcal_mol_A':float(fdrag[last].mean()),'mean_shear_stress_MPa':float(stress[last].mean()/1e6),'central_fit_range_A':[-8,8],'central_gradient_m_s_per_A':float(slope),'central_shear_rate_s-1':float(shear_rate),'central_intercept_m_s':float(intercept),'effective_viscosity_mPa_s':float(stress[last].mean()/shear_rate*1e3),'blocks_50ps':[dict(zip(['start_ps','end_ps','stress_MPa','gradient_m_s_per_A','shear_rate_s-1','viscosity_mPa_s'],row)) for row in block_rows],'sampling_definition':'Native profile pools atom velocities over 15000 samples; block profiles pool atoms over saved 0.5 ps frames in 1 Å slices. Blocks describe temporal sensitivity and are not independent confidence intervals. Wall forces are read before x force cancellation; projected wall area is LxLy. The viscosity ratio uses the actual central fitted gradient at this drive and confined model.'}
    (a.out/'shear_summary.json').write_text(json.dumps(summary,indent=2));np.savetxt(a.out/'shear-blocks.csv',blocks,delimiter=',',header='start_ps,end_ps,stress_MPa,slope_m_s_A,shear_rate_s-1,eta_mPa_s',comments='')
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(a.out/f'{name}.{ext}',dpi=170,bbox_inches='tight')
        plt.close(fig)
    fig,ax=plt.subplots(2,1,figsize=(11,7),sharex=True,layout='constrained');ax[0].plot(thermo[:,1]/1000,thermo[:,2],c=colors[0],lw=.8);ax[0].axhline(300,c='#7d9191',ls='--');ax[0].set_ylabel(tr('横向温度 / K','Transverse temperature / K'));ax[0].set_title(tr('以剪切开始为零时刻','Time starts when wall motion begins'));ax[1].plot(forces[:,0],stress/1e6,c='#aebdbb',lw=.7,label=tr('瞬时记录','Saved samples'));ax[1].plot((blocks[:,0]+blocks[:,1])/2,blocks[:,2],'o-',c=colors[1],lw=2,label=tr('50 ps区间均值','50 ps block means'));ax[1].set(xlabel=tr('时间 / ps','Time / ps'),ylabel=tr('剪切应力 / MPa','Shear stress / MPa'));ax[1].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=2,fontsize=10);save(fig,'shear-history')
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for data,color,label in [(water,colors[0],tr('水','Water')),(walls,colors[1],tr('壁','Walls')),(ions,colors[2],tr('离子','Ions'))]:
        ax[0].plot(data[:,1],data[:,3],c=color,label=label)
        mask=data[:,2]>.05
        ax[1].plot(data[mask,1],data[mask,4]*1e5,'.',c=color,ms=4,label=label)
    ax[1].plot([-8,8],np.array([-8,8])*slope+intercept,c='#263f42',ls='--',label=tr('中心线性拟合','Central linear fit'))
    for aa in ax:aa.set_xlabel('z / Å')
    ax[0].legend(loc='upper center',fontsize=10);ax[1].legend(loc='upper left',fontsize=10)
    ax[0].set(ylabel=tr('质量密度 / g cm⁻³','Mass density / g cm⁻³'),title=tr('分层结构来自实际分箱','Layering from recorded bins'));ax[1].set(ylabel=tr('平均x速度 / m s⁻¹','Mean x velocity / m s⁻¹'),title=tr('原子数加权速度；50.01–200 ps','Atom-weighted velocity; 50.01–200 ps'));save(fig,'flow-profiles')
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for i,color in enumerate(colors):
        prof=np.divide(sums[i],counts[i],out=np.full(len(mid),np.nan),where=counts[i]>0)
        ax[0].plot(mid,prof,'o-',ms=3,c=color,label=f'{50+50*i}–{100+50*i} ps')
    ax[0].set(xlabel='z / Å',ylabel=tr('水原子平均x速度 / m s⁻¹','Mean water-atom x velocity / m s⁻¹'),title=tr('分别读取三个连续时间块','Three consecutive observation blocks'));ax[0].legend(loc='upper right',fontsize=10)
    ax[1].plot((blocks[:,0]+blocks[:,1])/2,blocks[:,5],'o-',c=colors[1]);ax[1].axhline(summary['effective_viscosity_mPa_s'],c=colors[0],ls='--',label=tr('原生全窗口比值','Ratio from full native window'));ax[1].set(xlabel=tr('区间中心时间 / ps','Block midpoint / ps'),ylabel=tr('应力/速度梯度 / mPa s','Stress/velocity-gradient ratio / mPa s'),title=tr('时间窗口怎样影响估计','Sensitivity to the time window'));ax[1].legend(loc='best',fontsize=10);save(fig,'shear-blocks')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

在参考数据目录执行python analyze_shear.py --run . --out figures --language zh；英文图改用en。

平均流速和黏性响应之间还隔着一个重要的统计步骤：我们用有限时间里的平均近似描述持续的流动。若某一段突然出现较大壁面力，它可能是瞬时碰撞、结构重排或更慢的漂移。单独删掉这个点会改变所观察到的分布；更好的起点是查看它在轨迹和邻近时间里怎样出现，再考察较长时间块是否仍呈现同一趋势。数据清理应围绕可解释的记录错误展开，热涨落本身则是液体响应的一部分。

## 让时间窗口和实验条件对得上

同一条200 ps剪切轨迹可以给出多种平均。使用最后150 ps得到一个较长窗口的描述，再把它拆成三个50 ps窗口，可以看清这个描述随时间怎样变化。实际三个窗口的壁面应力均值约为29.924、35.508和35.146 MPa。用保存轨迹中的水原子速度重新分箱并拟合，各窗口的应力/梯度比值约为1.182、1.620和1.395 mPa·s。它们让一个总平均背后的波动有了具体形状，也指出继续增加采样时应该关注什么。

三个区间都采用左端点不计入、右端点计入的规则，即50<t≤100、100<t≤150、150<t≤200 ps；每段包含100帧坐标。壁面力按同样区间取样，使分子运动与受力使用一致的时间定义。

### 改变统计窗口后，估计怎样变化

三个连续50ps窗口分别计算剖面与应力/梯度比值，展示采样的时间敏感性。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/#zh-s8)

三个连续50 ps区间分别统计阻力和中心速度梯度，再计算相应比值。分块剖面从0.5 ps间隔保存的轨迹、1 Å空间层重新统计；它们呈现时间区间敏感性，与原生15000次采样的0.25 Å分箱有所区分。

这些时间块彼此相邻，液体结构也从前一块延续到后一块，因此三个数首先是时间敏感性的描述。要把误差条解释成独立重复之间的不确定度，需要建立多条独立速度历史，并给每条历史一致的准备、驱动和统计规则。要判断200 ps内是否覆盖了离子重新分布，还可以追踪离子的空间密度和位移。温度快速围绕目标值波动，并不自动把所有较慢的结构过程也变成同样快的过程；不同测量量各有自己的相关时间。

从这次结果走向材料比较，一种清楚的设计是先固定水模型、盐浓度、温度、盒尺寸和驱动，只改变水—壁相互作用，再同时观察密度层、速度剖面与壁面应力。这样，阻力变化便能与界面结构的变化联系起来。若一次同时改变墙的化学、粗糙度、离子数和盒子面积，最后的差别会混合多种机制。将问题拆成有共同参照的系列，比收集许多彼此条件不同的黏度数字更容易形成物理解释。

走向实验时，则先写下实验测的是什么。旋转流变仪常从宏观样品的力矩和几何换算黏度，微流体装置可能从压差与流量推断输运，表面力实验关注两面材料之间的局部阻力。它们与本讲共享动量传递的物理基础，却采用不同的空间和驱动条件。本例最直接对应的是均匀表面之间的纳米限域剪切。若研究目标是体相盐水的低速率黏度，可改建无墙的体相体系，并逐级降低剪切速率、增加统计时长，观察应力与速率是否形成稳定的线性关系。

读者还可以用同一份结果做一个不需要重新计算轨迹的练习：把中心拟合范围从±8 Å改成±6 Å，比较梯度和应力/梯度比值；然后把轨迹分箱宽度从1 Å改成2 Å，观察局部噪声和空间细节怎样改变。应力来自壁面记录，在这两个练习中保持同一测量窗口。变化发生在空间统计的组织方式，因而这是一堂关于测量定义的练习。把每次所用的范围、样本和单位一起保存，结果才有可检查的来龙去脉。

完成这些步骤后，一段看起来杂乱的盐水动画就有了清楚的阅读顺序：表面规定驱动，分子相互作用传递动量，横向温控管理热量，空间分箱提取流速，壁面受力给出阻力，时间窗口说明这次观察覆盖了怎样的变化。以后把体系换成聚合物溶液、带电界面或更宽的孔道，可以继续沿着这些问题组织计算，并把新增的分子机制接到相应的结构和运动测量上。

## 延伸阅读与开放资料

- [Nanosheared electrolyte](https://lammpstutorials.github.io/sphinx/build/html/tutorial4/nanosheared-electrolyte.html) · Simon Gravelle,Cecilia M.S.Alvares,Jacob R.Gissinger,Axel Kohlmeyer · CC BY4.0

  TIP4P/2005盐水建模、准备和移动壁剪切。

  保留原相互作用、驱动与分箱参数；增加数值轨迹、完整双语解释与实际时间块分析。
- [Études sur le frottement des liquides(1890)](https://fr.wikisource.org/wiki/Études_sur_le_frottement_des_liquides) · Maurice Couette · Public-domain original scientific text;new schematics

  圆筒实验与黏性测量的科学史。
- [compute temp/partial](https://docs.lammps.org/compute_temp_partial.html)
- [fix ave/chunk](https://docs.lammps.org/fix_ave_chunk.html)
- [fix setforce](https://docs.lammps.org/fix_setforce.html)
- [units](https://docs.lammps.org/units.html)
