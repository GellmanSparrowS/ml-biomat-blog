# 水和离子怎样相互作用

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l06/
Language: zh-CN

从盐水导电的认识出发，读懂刚性水、离子和壁面如何共同组织局部结构，再从真实轨迹测量水化邻居与分子朝向。

## 一粒盐消失以后，水里多了什么

把食盐放进水里搅拌，白色颗粒逐渐看不见了，水却保留了新的性质：它可以更容易地传导电流，也会改变某些高分子链周围的环境。对含水材料而言，这种变化很具体。水凝胶吸收的往往是含盐溶液，分离膜的孔道需要让水与不同离子通过，带电聚合物的伸展则取决于周围电荷怎样排列。要理解这些现象，首先需要看清盐溶解后留下的粒子，以及水为什么会围绕它们重新组织。本节从一份夹在两面固体壁之间的氯化钠水溶液出发，把“盐水”展开成可以计数、测量距离和辨认朝向的分子环境。

氯化钠晶体中的钠和氯本来就以带电离子的形式组成晶格。溶解时，离子离开有序排列，进入能够在液体中移动的状态；钠离子记作Na⁺，氯离子记作Cl⁻。这里的正负号说明电荷，而不是粒子的运动方向。离子周围有不断转动和交换位置的水分子，这些水与离子共同组成局部水化环境。可以把它想成一个会随主人移动、又不断有人进出的邻近人群：某一时刻有几位邻居，和同一批邻居能跟随多久，是两个不同的问题。前者是结构，后者需要进一步研究交换与动力学。

十九世纪研究者曾通过导电和渗透现象追问溶液中到底有哪些粒子。阿伦尼乌斯在1884年的博士研究及随后发展中提出电解离理论，把电解质溶液的行为与可移动的带电粒子联系起来。这个历史转折帮助我们理解今天输入文件里的电荷：Na⁺与Cl⁻各有自己的位置和运动，不必一直成对相邻；整盒溶液仍然可以保持电中性。下面的图把这一认识画成从晶格到溶液的概念过程。它也提出本节的两个观察任务：离子周围的水有多少，以及这些水的哪一端更靠近离子。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s1)

图 1 · 电解离认识把溶液导电与可移动离子联系起来；图中水的朝向表示局部电荷作用。

本例包含406个水分子、15个钠离子、15个氯离子和432个中性壁原子，共1680个显式原子。左右两侧及前后两侧采用周期边界，上下两面壁沿z方向限制液体。这个几何适合学习纳米孔道中的溶剂结构，也为后面研究流动阻力留下了同一个体系。当前先让水、离子和壁在300K附近运动，观察施加剪切之前的准备过程。我们会从实际轨迹算出邻近水数和水的朝向，并把每个统计量的距离范围与时间窗口写清楚，让“看起来围住了”变成有明确含义的测量。

## 从电中性到相互吸引：先把电荷和能量分开

电中性指所选对象的电荷代数和为零。代数和意味着保留正负号，把正电荷与负电荷相加；它不会把所有电荷都取成正数。本例15个Na⁺贡献15个单位正电荷，15个Cl⁻贡献15个单位负电荷，两项相抵。每个水分子的部分电荷也相抵，壁原子电荷为零，因此整盒电荷为零。但电荷在空间里仍然分散在不同位置。正如一笔收入与一笔支出相等，并不意味着两笔交易发生在同一地点，电中性也不意味着任何位置的电场和相互作用都消失。

把所选粒子的电荷相加式 1

![把所选粒子的电荷相加](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Q | 所选对象的总电荷 | e |
| qᵢ | 第i个粒子的带符号电荷 | e |
| i, N | 粒子编号与所选粒子总数 | 1 |
| Σ, =, 1 | Σ从编号1累加到N；等号定义总电荷；1是起始编号 | 1 |

怎样理解同号电荷相加，异号电荷相抵，保留每个电荷的正负。

算一个例子15个+1e与15个−1e离子相加为0；每个水的−1.1128e+2×0.5564e也等于0。

使用条件总电荷与电荷的空间分布分别描述整体组成和局部静电环境。

水分子里的电荷还需要多理解一层。氧与氢共同形成化学键，电子分布并不均匀，因而可以用分布在不同位置的正、负部分电荷近似描述分子对外的静电作用。“部分”表示这些数值是模型中的电荷分配，可能不是整数；它们并不要求一个完整电子在每一步都从一个原子转移到另一个原子。钠离子在本例中取+1e，氯离子取−1e，水的正电荷则分别取+0.5564e。e是元电荷的大小。给定电荷后，我们还需要知道两处电荷之间有多远，才能计算静电能量。

两个指定电荷位置的直接库仑能量式 2

![两个指定电荷位置的直接库仑能量](https://ml-biomat.com/static/agent-math/3ca18331aa01f2b1bc0a93f1.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Uᵢⱼ | 这两个电荷位置的直接静电能量 | kcal mol⁻¹ |
| qᵢ, qⱼ | 带符号的模型电荷 | e |
| rᵢⱼ | 两个电荷位置之间的距离 | Å |
| εᵣ | 相对介电常数，本例取1 | 1 |
| C | 约332.06371的单位换算常数 | kcal mol⁻¹ Å e⁻² |
| i, j | 电荷位置的编号 | 1 |
| =, /, × | 等号定义能量；分式表示相除；相邻因子相乘 | 1 |

怎样理解电荷乘积决定符号；除以距离使该项随距离增大而减弱。

算一个例子+1e与−1e相隔5Å、εᵣ=1时，U约−332.06371/5=−66.4127kcal/mol。

使用条件这是指定电荷对的直接项。周期体系由短程与长程求解共同计算静电，水的显式电荷参与整体响应。

公式里的kcal/mol也值得停下来读。分子模拟借用每摩尔的能量单位表示微观相互作用，便于与化学参数保持一致；一个给定粒子对的物理能量可通过除以阿伏伽德罗常数换成单次相互作用的焦耳数。能量为负说明相对于所选零点处于更低的位置，而不是粒子拥有“负的运动量”。动能则由质量和速度决定，是另一类能量。把势能、动能、温度和电荷分别辨认清楚，看到日志中的负势能、大的总能量或者不断变化的温度时，才知道应该检查哪个量之间的关系。单位与对象是阅读数值的第一步。

库仑能量中的电荷乘积决定正负：异号电荷相乘得到负值，它们靠近时能量降低；同号电荷相乘得到正值，它们靠近时能量升高。距离放在分母，是因为这项相互作用随距离增大逐渐减弱。以相隔5Å的一对+1e与−1e点电荷为例，按本节单位计算的直接静电项约为−66.41kcal/mol。这个数值描述指定距离下的一项势能；溶液里的离子同时面对许多水和其他离子，完整环境的能量与熵共同影响它们的排列。因此，判断盐是否形成离子对，需要统计离子间距离及其变化，并把水化环境一起纳入观察。

显式水模型已经把水分子的方向和部分电荷放进计算，水的集体重排由这些相互作用产生。本例没有再给库仑公式乘上水的宏观介电屏蔽，LAMMPS中的相对介电常数保持默认值1。把日常见到的水介电常数约78直接填进去，会把另一种连续介质描述叠加到现有模型之上，改变整套参数的物理含义。学习时可以把两种层次区分开：显式水逐个描述水分子，连续介质则用整体响应概括没有逐个表示的溶剂。本节沿用前一种方式，水的方向本身正是要测量的内容。

## 三个原子、四个作用位置：读懂TIP4P/2005

上一节的柔性水允许键长和键角围绕偏好的数值振动，本节改用刚性TIP4P/2005水。刚性表示保持两个氧—氢距离及氢—氧—氢夹角，整个水分子仍然可以平移、转动。模型名称中的“四点”说的是相互作用位置：两个氢位置各有正电荷，氧位置承担主要的短程Lennard–Jones作用，另有一个M位置承担负电荷。M位于氧朝向两氢之间的角平分线方向，距离氧0.1546Å。它是根据分子几何计算出来的无质量作用点；每个水在轨迹里仍然只有一个氧和两个氢，共三个显式原子。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s3)

图 2 · TIP4P/2005几何与作用位置。M沿角平分线从氧朝两氢方向偏移；Lennard–Jones中心仍在氧。

为什么要把负电荷从氧位置移开一点？水模型的发展围绕几何、电荷位置与液体性质之间的联系展开，需要在计算成本与可描述的性质之间选择合适的表达方式。TIP4P/2005由Abascal与Vega在2005年提出，把四点几何和参数组合用于描述水的凝聚态性质。移动负电荷位置会改变电荷分布，进而改变水之间及水与离子之间的方向性作用。同样写着“水”，不同模型的几何、部分电荷和Lennard–Jones参数可能不同，应该成套使用。本例采用氧—氢距离0.9572Å、夹角104.52°，两氢各带+0.5564e，M带−1.1128e。

从氧和氢的位置恢复M作用点式 3

![从氧和氢的位置恢复M作用点](https://ml-biomat.com/static/agent-math/4277c9bc5ad17c35117962d6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| rO, rHₐ, rM | 氧、编号a的氢及M作用点的位置向量 | Å |
| a, 1, 2 | 氢编号a取1或2 | 1 |
| uₐ | 从氧指向氢a的单位向量 | 1 |
| b | 指向两氢之间的角平分线单位向量 | 1 |
| dOM | 氧到M的距离，本例0.1546Å | Å |
| \|…\| | 向量的长度；分子分母同单位，相除得到单位向量 | 由所包围的向量决定 |
| +, −, /, =, × | 向量相加、相减；除以长度归一化；等号定义；相邻因子相乘 | 1 |

怎样理解两根单位键方向相加指向角平分线，再沿该单位方向从氧移动指定距离。

算一个例子氧在原点，两氢关于x轴对称且位于正x一侧时，b=(1,0,0)，M=(0.1546,0,0)Å。

使用条件分子先按x、y周期像恢复完整几何；刚性目标夹角104.52°，两根键长均0.9572Å。

角平分线可以从两根氧—氢方向得到。先把每根方向向量除以自身长度，得到只说明朝向的单位向量；将两者相加，方向落在两根键之间；再除以相加结果的长度，就得到角平分线的单位方向。最后沿该方向走0.1546Å，便从氧到达M。这个过程也解释了分析程序为什么要先处理周期边界：若一个氢恰好显示在盒子的另一侧，直接相减会得到跨越整盒的假长键。程序先把氢放回相对于氧最近的周期像，再计算分子内部方向。z方向不是周期方向，因此只在x和y上做这一步。

中性水分子的电偶极矩式 4

![中性水分子的电偶极矩](https://ml-biomat.com/static/agent-math/2e060d62f5574bfbeee732e7.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| μ | 水分子的电偶极矩向量 | e Å |
| qH, qM | 每个氢及M的电荷，分别+0.5564e与−1.1128e | e |
| rH₁, rH₂, rM, rO | 两个氢、M与氧的位置向量 | Å |
| H₁, H₂, M, O | 作用点标签，1与2区分两个氢 | 1 |
| +, −, =, × | 位置差给相对位移，各电荷乘位移后相加；等号定义偶极矩 | 1 |

怎样理解电荷乘位置衡量电荷分离；总电荷为0时，改变整体坐标原点不会改变该向量。

算一个例子本例沿角平分线的大小为2×0.5564×[0.9572cos(52.26°)−0.1546]≈0.479931eÅ；1eÅ≈4.803205D，得到2.305206D。

使用条件使用TIP4P/2005的M位置计算负电荷贡献；偶极方向由负电荷一侧指向正电荷一侧。

电偶极矩把分子的电荷分离写成一个有方向的量。对于电中性的水，用氧作为坐标原点后，将各处电荷乘以相应位置向量再相加，就得到从负电荷一侧指向正电荷一侧的方向。两个氢的横向分量互相抵消，沿角平分线的分量相加，而M处负电荷贡献相反方向。按本例参数，偶极矩大小约为2.305D，D叫德拜，是分子偶极矩常用的单位。输入文件虽然把−1.1128暂存在氧原子的电荷字段里，专门的TIP4P相互作用会把它放到M处计算；自行分析偶极矩时同样要恢复M的位置。

孤立离子—水静电练习：在固定离子—氧距离下转动一个刚性TIP4P/2005水分子。

[Figure: 水分子朝向与解析库仑能量](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s3)

解析静电朝向练习。水的刚性几何与电荷取本例参数，液体的完整结构另外由实际轨迹统计。

交互图把一个离子和一个水分子单独拿出来，在固定离子—氧距离下转动水，只计算三个电荷位置与离子的直接库仑能量。正离子更容易吸引水的负电荷一侧，负离子更容易吸引氢所在的一侧；详细能量曲线还保留了有限的键长与夹角。这个练习把朝向偏好讲清楚，完整液体里则还有邻近水、短程排斥和热运动共同作用，所以真实朝向表现为一个分布。下面完整模板的O、H、H顺序也有实际用途：隐式TIP4P实现要求同一水的氧及两个氢具有连续原子编号，氧排在最前。

### 完整刚性水模板

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

O、H、H顺序与约束信息共同定义每个水。

## 让水保持形状，也让参数保持一致

刚性水仍然需要在输入文件里列出氧—氢键和氢—氧—氢角，因为程序必须知道约束哪些原子。本例的谐振键系数与角系数都写成零，后面却跟着0.9572和104.52两个目标几何值。这里的零表示不靠普通谐振弹簧提供恢复力；在动力学阶段，SHAKE约束会计算附加的约束力，使水分子维持指定几何。把它比作一个会移动的小三角形比较容易理解：三角形整体可以转动，各顶点到彼此的距离由形状规则限定。关闭这项约束而保留零系数，会改变模型本身。

SHAKE源于1977年Ryckaert、Ciccotti与Berendsen关于受约束分子运动的工作。它解决的计算问题是：极快的键振动迫使时间步很短，而有些研究关心的是较慢的分子转动、平移和结构变化。通过约束选定的内部几何，可以把计算集中到保留下来的运动。本例仍然使用1fs时间步，并在每一步迭代满足约束。约束容差、最大迭代次数和输出精度是不同概念。保存的坐标经过有限位数记录后，重新算出的键长会出现很小偏差；分析时需要把记录精度与约束求解本身的精度区分开。

最小化阶段与动力学阶段的约束处理又有区别。本例先在最小化中给SHAKE指定kbond 2000，以较强的谐振约束近似维持几何，消除初始拥挤；进入动力学后，再使用真正的几何约束。水模板最初写出的键长接近0.9584Å，略不同于目标0.9572Å，这正说明模板坐标是放置分子的初始姿态，目标几何由参数和约束共同确定。实际轨迹后段的氧—氢平均距离为0.9571999Å，平均夹角为104.51999°，与约束目标一致。检查这些基本几何量，可以在讨论复杂水化结构之前先确认模型确实按预期运动。

### 水、离子与壁的完整参数

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

保持几何、电荷与相互作用参数成套使用。

参数文件也给出了离子和壁的质量，以及不同原子类型的Lennard–Jones参数。离子带电并不意味着只有静电作用：短程排斥阻止原子无限靠近，色散项还提供另一部分相互作用。没有显式指定的异类配对按本例的默认几何混合规则生成，而氧—壁配对被直接指定为单独参数。这样的壁有质量、位置和相互作用，它通过原子层的排列形成限域边界。这里WALL的质量数值接近铝原子，但采用的是给定Lennard–Jones壁模型；理解界面行为时，应围绕这组具体壁参数讨论润湿与分层，而不把它自动等同于所有真实金属表面的性质。

还常会遇到“水中的氢键”这个词。一个水的氢可以朝向另一个水较富电子的一侧，从而形成具有方向偏好的邻近关系；它与同一水内部的氧—氢共价连接是不同层次的结构。在当前固定电荷水模型中，水之间的这种排列倾向来自所给电荷与短程相互作用，并不需要在两个水之间额外添加一条永久共价键。若要统计氢键，就另外规定供体、受体、距离与夹角判据，再在轨迹中逐帧识别。这样的定义允许邻近关系形成、消失和交换，同时每个水自己的两根氧—氢连接始终保留。

## 把盐水放进窄缝：边界和长程静电一起考虑

生成体系时，先用晶格摆出上下两块固体，再把水放进中间区域，并插入15个钠离子和15个氯离子。晶格常数是4.04Å，x与y方向各跨6个晶格尺度，因此实际边长为24.24Å。region命令在这里沿用晶格单位，写成−3到3并不是−3Å到3Å。z方向盒子总长40.4Å，壁原子位于其中两个较薄的区域。把这些数字换成实际长度之后，才能判断液体是否拥挤、邻居搜索距离是否合理，以及后续密度统计的切片体积应该多大。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s5)

图 3 · 左侧为x–z限域示意，y方向垂直图面；右侧示意静电求解的空白延展，物理平板内部各方向相互作用保留。

boundary p p f表示x和y周期、z边界固定且非周期。固定边界指盒子边界的位置固定，不等于其中每个壁原子被钉住。当前准备阶段的NVT积分作用于全部原子，壁也能振动和重排。液体受到壁原子的实际相互作用限制，而不是受到字母f产生的一面数学反弹墙。周期方向则相当于把同样的窄缝在平面内铺开；距离计算需要采用相邻周期像。对沿z分层的体系，应保留真实的上下方向，不能把顶端和底端像周期液体那样直接接在一起。

### 生成完整限域盐水体系

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

将water.mol、parameters.inc与groups.inc放在同一例题目录，运行lmp -in create.lmp。

静电相互作用衰减较慢，不能只像短程排斥那样找到附近邻居就结束。本例的lj/cut/tip4p/long负责短程部分，并与pppm/tip4p共同计算长程静电。可以把这个分工想成同时看清附近街区和整个城市：附近作用用粒子间距离直接计算，较平滑的远程部分在网格上处理，再合成为同一个静电问题的结果。两部分必须与M电荷位置一致，所以TIP4P专用的配对形式和长程求解器成套使用。参数1.0e−5是长程力计算的目标精度设置，与时间步1fs、SHAKE容差属于不同的数值控制。

平板几何还需要处理长程算法中的周期像。kspace_modify slab 3.0在静电求解使用的延展区域里加入空隙，并配合平板修正减小上下重复层之间的耦合。这里的3.0是延展体积与实际模拟盒体积的比值，不是把液体厚度变成三倍。液体内部沿z方向的吸引与排斥仍然存在，否则水化和壁面结构都将改变。这个设置表达的是一个二维周期、沿法向隔离的平板近似。以后提高数值精度时，可以增加延展尺度并比较结构和力的变化，检查该几何下的剩余周期像影响。

### 水、离子和壁的分组

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

分组供后续约束、积分和分析选择使用。

分组文件把水、离子、流体和上下壁组织成可选择的对象。group只是给原子集合命名，具体怎样运动仍由后面的积分、约束和外力命令决定。生成过程中还随机移去一定比例的完整水分子，使初始排布更适合后续松弛；mol yes要求按整分子处理，避免只删除一个氢而留下破碎水。最终数量应从实际生成结果读取，本次得到406个完整水。理解命名、分组、数量和运动规则之间的关系，后面改变离子数或壁面条件时就能清楚知道究竟改变了哪一层设置。

浓度也需要先选定分母。一个普通烧杯里的盐浓度通常以溶液体积计算，而这个盒子同时包含液体、固体和空隙。若把15个离子直接除以整个盒子体积，得到的是按全盒体积定义的平均数密度；若采用两壁之间某个指定区域，则得到对应区域的浓度。两种数字回答的问题不同，都必须带着体积定义。局部水化计数本身不需要先指定一个宏观溶液体积，因此本节先报告粒子组成和局部结构；建立不同浓度的比较时，再统一可访问区域或使用另一个明确的组成指标，使盐量变化和几何变化能够分开讨论。

## 先看准备过程，再读分子结构

运行顺序是先执行create.lmp生成create.data，再执行equilibrate.lmp读取它。后一文件先最小化，然后把步数重新设为零，以1fs时间步运行30000步，因此准备轨迹长30ps。这里ps是皮秒，1ps等于1000fs。NVT的目标温度为300K，盒子大小固定；壁面间距则可以随壁原子的运动变化。文件还在z方向整体平移所有原子以维持居中，平移改变坐标原点的选择，保留原子间距离。观察局部水化与两壁间距时，这种共同平移不会改变相对几何。

### 最小化与30ps准备的完整输入

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

生成create.data后运行lmp -in equilibrate.lmp。

温度曲线与壁面间距应放在一起读。实际记录中，体系从初始低温升到300K附近，随后持续涨落；取15–30ps的61个温度记录，平均值约299.74K。相同时间范围中，31个轨迹帧给出的两壁质心间距平均约28.33Å，并仍有缓慢起伏。温度接近目标值说明热运动已达到相应量级，壁面曲线则展示结构还在怎样调整。这里两壁质心间距包含壁自身位置，液体能够进入的净宽度还与壁层厚度、原子尺寸和相互作用有关，分析局部密度时应直接看液体分布。

### 固定盒子中的真实准备记录

全体系温度与两壁质心间距来自0–30ps准备段；阴影标出15–30ps结构统计窗口。

LAMMPS 30 Sep 2026 Update 1；Gravelle等人的纳米剪切电解质例，TIP4P/2005水，300 K，real单位，x/y周期边界、z固定边界；30 ps准备后进行200 ps剪切。

[下载参考数据与完整输入（ZIP） 3.17 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-electrolyte-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s6)

真实0–30 ps准备记录：全体系温度与两壁质心间距。盒子长度固定，两壁内部的原子仍可运动；浅色区域对应后续结构分析的15–30 ps窗口。

本节选15–30ps计算结构，得到的是这段准备轨迹中的局部描述。曲线里相邻时刻往往彼此相关：同一个离子会连续留在相近位置，部分水也会多次出现在它的邻域。因此，31帧乘以15个离子虽然产生许多观测，却不是同样多次独立实验。我们保留平均值和分布，同时把窗口长度写在图上。若研究目标变成准确比较两种盐或两种表面，就继续延长轨迹，检查前后时间块是否一致，并运行独立初始排布；这些操作分别增加时间覆盖和独立重复。

### 盐水与移动壁的准备轨迹

真实0–30ps准备段；水、离子与壁共同在z方向平移以居中，保留相对位置。

轨迹中的彩色原子提供直观入口：水靠近某个离子时会改变朝向，在壁附近的排布也与中间区域不同。把动画暂停在一个时刻，可以辨认局部拥挤；沿时间推进，则能看到这种结构怎样变化。模型中的水保持固定连接关系，离子也保持给定电荷，所以本节研究的是既定化学物种的空间组织。涉及水解、质子转移或表面化学反应时，需要另外选择描述相应反应的模型。对当前问题而言，先把固定物种的几何、电荷和统计搞清楚，已经能够解释许多水化结构的特征。

## 怎样量出水化层：邻居数量和分子朝向

给离子画一个半径为r的球，并数球内有多少个水氧，是最直接的水化结构测量。选水氧作为每个水的位置代表，可以避免同一分子的两个氢被重复计成两份水。对每个离子、每个时刻都做同样的计数，再求平均，得到“半径r内的平均邻近水数”。逐渐增大r，曲线会不断上升：先越过很少有水氧进入的近距离区，再把较近的一批水纳入，随后继续包括更远的水。曲线的起伏和斜率变化比一张快照更容易看出不同离子的局部尺寸与排列差异。

对离子和时间平均的累积邻近水数式 5

![对离子和时间平均的累积邻近水数](https://ml-biomat.com/static/agent-math/db88778fdc6e3bf7154ee436.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n̄(r) | 半径r内每个离子的平均邻近水数 | 1 |
| r, dᵢⱼ⁽ᶠ⁾ | 报告半径与帧f中离子i到水氧j的距离 | Å |
| Nf, NI, NW | 轨迹帧数、所选离子数与水分子数 | 1 |
| f, i, j | 轨迹帧、离子和水的求和编号 | 1 |
| 1[…], ≤ | 条件满足时记1，否则记0；≤包含距离恰好等于半径的情况 | 1 |
| Σ, /, ×, = | 求和累积配对计数；除以帧数与离子数的乘积求平均；等号定义 | 1 |

怎样理解每个符合距离条件的水贡献一次计数；先累积，再对观察对象与帧求平均。

算一个例子31帧、15个Na⁺，3.3Å内累计2283个配对观测，平均2283/(31×15)≈4.90968。

使用条件x、y采用最近周期像，z保持非周期距离；相邻帧和重复配对可以相关，平均值保留15–30ps窗口定义。

公式中的指示函数像一个简单的计数开关：距离满足条件就记1，不满足就记0。这样，内层求和数出某个离子的邻近水，外层再把不同离子和时刻合并平均。距离必须按本节的边界条件计算，x与y取最近周期像，z保持真实差值。为了给曲线加上可比较的读数，本节对Na⁺选择3.3Å，对Cl⁻选择3.9Å作为报告半径；这些是明确写出的分析阈值，可以通过完整累积曲线检查其影响。阈值选择与“一个离子必然拥有几个水”的断言不同，后者会忽略温度、浓度、模型和界面的变化。

本次15–30ps窗口中，Na⁺在3.3Å内平均有约4.91个邻近水，Cl⁻在3.9Å内平均有约7.15个。它们使用不同距离阈值，读数也应与各自完整曲线一起理解。这里没有把球壳计数除以“整盒平均水密度”来直接称为体相径向分布函数，因为盒子里含有固体和空隙，而且靠近壁的球壳并非处处可被水占据。直接计数保留了所选体系的真实几何。以后需要与均匀体相的径向分布函数比较时，应另建均匀体系，或明确处理空间非均匀性和可访问体积。

可以把累积邻居曲线看成围绕离子逐渐扩大的观察圈。半径很小时，圈内通常没有水氧；扩大到第一批水所在的距离，计数迅速增加；如果第一批水与外层之间有较稀疏的区域，曲线便出现比较平缓的部分。把报告半径放在平缓区附近，微小的半径改动往往只影响少数计数；放在陡升段，同样改动就可能改变很多邻居。这个读图方法帮助我们理解阈值敏感性。遇到清晰度较差的层次时，可以直接保留整条曲线进行比较，让不同距离上的差异共同表达结构，而不强迫所有结果压缩成一个配位数。

用方向余弦表示水朝向离子的哪一侧式 6

![用方向余弦表示水朝向离子的哪一侧](https://ml-biomat.com/static/agent-math/0c760e4df4e117811c5f9910.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| s | 两个单位方向的点积，即朝向余弦 | 1 |
| μ̂ | 水偶极矩方向的单位向量 | 1 |
| R, rO, rI | 从离子到水氧的向量，以及水氧、离子的位置 | Å |
| R̂, ^ | R的单位方向；帽号表示除以向量长度 | 1 |
| β | 水偶极方向与离子向外径向之间的夹角 | rad |
| ·, cos, =, − | 点积比较方向；cos取角的余弦；等号连接相同定义；位置相减得到位移 | 1 |

怎样理解两单位向量的点积等于它们夹角的余弦，因此范围为−1到+1。

算一个例子β=0°时s=+1，正电荷一侧朝外；β=90°时s=0；β=180°时s=−1，正电荷一侧朝向离子。

使用条件方向分布按给定离子—氧距离阈值选取配对；该量描述瞬时朝向。

数量只告诉我们水是否靠近，朝向则告诉我们哪一侧靠近。这里从离子指向水氧画一根径向箭头，再与水的偶极方向比较。两箭头同向时余弦接近+1，表示水的正电荷一侧更朝外、负电荷一侧更靠近离子；反向时余弦接近−1，表示正电荷一侧更朝向离子；接近0时两方向大致垂直。把每一对满足距离条件的离子和水都纳入直方图，就能看到热运动中的朝向分布。Na⁺周围的分布偏向正值，Cl⁻周围偏向负值，这与前面的电荷作用图景相互呼应。

### 完整Python：水化、朝向与局部密度

```
"""Analyze the actual confined electrolyte preparation trajectory.

python analyze_hydration.py --run . --out analysis --language en

Dependencies: numpy and matplotlib. Inputs: equilibrate.lammpstrj,
equilibrate-thermo.dat. Times are absolute preparation times in fs.
The 15--30 ps window describes this finite preparation segment.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

AVOGADRO = 6.02214076e23
MASS = {1: 15.9994, 2: 1.008, 3: 22.990, 4: 35.453, 5: 26.9815}


def frames(path):
    """Read orthogonal LAMMPS custom dumps without assuming row order."""
    with path.open(encoding="utf-8") as handle:
        while line := handle.readline():
            if line.strip() != "ITEM: TIMESTEP":
                raise ValueError("Expected a timestep header")
            step = int(handle.readline())
            assert handle.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(handle.readline())
            header = handle.readline().split()
            assert header[:3] == ["ITEM:", "BOX", "BOUNDS"]
            bounds = np.array([list(map(float, handle.readline().split())) for _ in range(3)])
            assert bounds.shape == (3, 2), "This analysis expects an orthogonal box"
            keys = handle.readline().split()[2:]
            arr = np.array([list(map(float, handle.readline().split())) for _ in range(n)])
            order = np.argsort(arr[:, keys.index("id")])
            yield step, bounds, {key: arr[order, j] for j, key in enumerate(keys)}


def in_plane_image(delta, lengths):
    """Nearest periodic image in x and y; z is physically nonperiodic."""
    result = np.array(delta, copy=True)
    result[..., :2] -= lengths[:2] * np.rint(result[..., :2] / lengths[:2])
    return result


def sample_stats(values):
    a = np.asarray(values, dtype=float)
    return {"count": int(a.size), "mean": float(a.mean()),
            "frame_or_pair_sd": float(a.std(ddof=1)) if a.size > 1 else 0.0,
            "minimum": float(a.min()), "maximum": float(a.max())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    font_candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                       "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed_fonts = {font.name for font in font_manager.fontManager.ttflist}
    chinese_fonts = [name for name in font_candidates if name in installed_fonts]
    plt.rcParams.update({"font.family": chinese_fonts if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16,
                         "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "#f8f7f2",
                         "axes.facecolor": "#f8f7f2", "axes.unicode_minus": False})
    tr = lambda cn, en: cn if zh else en
    radii = np.linspace(1.0, 6.0, 101)
    zedges = np.arange(-20.5, 20.5001, .5)
    zmid = (zedges[:-1] + zedges[1:]) / 2
    neighbour_records = {3: [], 4: []}
    orientation = {3: [], 4: []}
    cutoffs = {3: 3.3, 4: 3.9}
    profiles = {"water": [], "Na": [], "Cl": [], "wall": []}
    geometry = []
    history = []
    selection_times = []
    last = None
    for step, bounds, data in frames(args.run / "equilibrate.lammpstrj"):
        ids = data["id"].astype(int)
        typ = data["type"].astype(int)
        xyz = np.column_stack([data[k] for k in ("x", "y", "z")])
        lengths = bounds[:, 1] - bounds[:, 0]
        oi = np.flatnonzero(typ == 1)
        id_to_row = {int(atom_id): i for i, atom_id in enumerate(ids)}
        # Implicit TIP4P requires O,H,H consecutive atom IDs with O first.
        h1 = np.array([id_to_row[int(ids[i] + 1)] for i in oi])
        h2 = np.array([id_to_row[int(ids[i] + 2)] for i in oi])
        assert np.all(typ[h1] == 2) and np.all(typ[h2] == 2)
        assert np.all(data["mol"][oi] == data["mol"][h1])
        assert np.all(data["mol"][oi] == data["mol"][h2])
        v1 = in_plane_image(xyz[h1] - xyz[oi], lengths)
        v2 = in_plane_image(xyz[h2] - xyz[oi], lengths)
        l1 = np.linalg.norm(v1, axis=1)
        l2 = np.linalg.norm(v2, axis=1)
        u1, u2 = v1 / l1[:, None], v2 / l2[:, None]
        bisector = u1 + u2
        bisector /= np.linalg.norm(bisector, axis=1)[:, None]
        angle = np.degrees(np.arccos(np.clip(np.sum(u1 * u2, axis=1), -1, 1)))
        # The negative site is M, not the oxygen location.
        m_relative = .1546 * bisector
        dipole_eA = .5564 * (v1 + v2) - 1.1128 * m_relative
        dipole_magnitude = np.linalg.norm(dipole_eA, axis=1)
        dipole_direction = dipole_eA / dipole_magnitude[:, None]
        dipole_D = dipole_magnitude * 4.80320471257
        wall = typ == 5
        top = wall & (xyz[:, 2] > 0)
        bottom = wall & (xyz[:, 2] < 0)
        wall_gap = xyz[top, 2].mean() - xyz[bottom, 2].mean()
        history.append([step / 1000, wall_gap, angle.mean(), dipole_D.mean()])
        if 15000 <= step <= 30000:
            selection_times.append(step / 1000)
            geometry.extend(np.column_stack([l1, l2, angle, dipole_D]).tolist())
            for ion_type in (3, 4):
                ion_xyz = xyz[typ == ion_type]
                # delta points from the ion toward oxygen.
                delta = in_plane_image(xyz[oi][None, :, :] - ion_xyz[:, None, :], lengths)
                distance = np.linalg.norm(delta, axis=2)
                assert distance.min() > 0
                counts = (distance[..., None] <= radii).sum(axis=1)
                neighbour_records[ion_type].append(counts.mean(axis=0))
                # Normalize the reconstructed charge-weighted dipole itself.
                cosine = np.einsum("ijk,jk->ij", delta, dipole_direction) / distance
                orientation[ion_type].extend(cosine[distance <= cutoffs[ion_type]].tolist())
            for name, selection in {"water": typ <= 2, "Na": typ == 3,
                                    "Cl": typ == 4, "wall": wall}.items():
                masses = np.array([MASS[int(t)] for t in typ[selection]])
                mass_in_slice = np.histogram(xyz[selection, 2], bins=zedges, weights=masses)[0]
                # 1 A^3 = 1e-24 cm^3; input atomic masses are g/mol.
                volume_cm3 = lengths[0] * lengths[1] * np.diff(zedges) * 1e-24
                profiles[name].append(mass_in_slice / AVOGADRO / volume_cm3)
        last = (ids, typ, data)
    if not selection_times:
        raise ValueError("The selected 15--30 ps window contains no frames")
    ids, typ, data = last
    assert len(ids) == 1680
    counts = {str(t): int((typ == t).sum()) for t in range(1, 6)}
    assert counts == {"1": 406, "2": 812, "3": 15, "4": 15, "5": 432}
    assert abs(data["q"].sum()) < 1e-8
    hist = np.array(history)
    geom = np.array(geometry)
    thermo = np.loadtxt(args.run / "equilibrate-thermo.dat", comments="#")
    late = (thermo[:, 1] >= 15000) & (thermo[:, 1] <= 30000)
    summary = {
        "analysis_window_ps": [15, 30], "frames": len(selection_times),
        "type_counts": counts, "total_charge_e": float(data["q"].sum()),
        "temperature_K": sample_stats(thermo[late, 2]),
        "wall_center_gap_A": sample_stats(hist[hist[:, 0] >= 15, 1]),
        "OH_A": sample_stats(geom[:, :2].ravel()),
        "HOH_deg": sample_stats(geom[:, 2]), "water_dipole_D": sample_stats(geom[:, 3]),
        "geometry_count_water_frames": int(geom.shape[0]),
        "neighbour_counts": {}, "orientation_cosine": {},
        "interpretation": "Correlated finite-window descriptors. No independent-sample error bars or bulk homogeneous RDF normalization."
    }
    for it, name in [(3, "Na"), (4, "Cl")]:
        index = int(np.argmin(abs(radii - cutoffs[it])))
        assert abs(radii[index] - cutoffs[it]) < 1e-12
        summary["neighbour_counts"][name] = {"radius_A": cutoffs[it],
                                              **sample_stats(np.array(neighbour_records[it])[:, index])}
        summary["orientation_cosine"][name] = {"radius_A": cutoffs[it], **sample_stats(orientation[it])}
    (args.out / "hydration_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def finish(fig, stem):
        for suffix in ("svg", "png"):
            fig.savefig(args.out / f"{stem}.{suffix}", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, layout="constrained")
    axes[0].plot(thermo[:, 1] / 1000, thermo[:, 2], color="#167d84")
    axes[0].axhline(300, color="#819394", linestyle="--")
    axes[0].set_ylabel(tr("全体系温度 / K", "Whole-system T / K"))
    axes[1].plot(hist[:, 0], hist[:, 1], color="#c16b3d")
    axes[1].set_ylabel(tr("两壁质心间距 / Å", "Wall-centre separation / Å"))
    axes[1].set_xlabel(tr("准备时间 / ps", "Preparation time / ps"))
    for ax in axes:
        ax.axvspan(15, 30, alpha=.08, color="#167d84")
        ax.set_xlim(0, 30)
        ax.grid(axis="y", alpha=.15)
    axes[0].set_title(tr("固定盒子中的升温与壁面重排；阴影为结构统计窗口", "Heating and mobile walls in a fixed box; shading marks the structural window"))
    finish(fig, "electrolyte-preparation")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), layout="constrained")
    for it, name, color in [(3, "Na⁺", "#466eaa"), (4, "Cl⁻", "#c16b3d")]:
        neighbour = np.array(neighbour_records[it]).mean(axis=0)
        axes[0].plot(radii, neighbour, label=name, color=color, linewidth=2)
        axes[0].scatter([cutoffs[it]], [np.interp(cutoffs[it], radii, neighbour)], color=color)
        axes[1].hist(orientation[it], bins=np.linspace(-1, 1, 31), density=True,
                     histtype="step", linewidth=2, color=color,
                     label=f"{name}, r ≤ {cutoffs[it]:.1f} Å")
    axes[0].set_xlabel(tr("离子—氧距离阈值 / Å", "Ion–oxygen distance threshold / Å"))
    axes[0].set_ylabel(tr("每个离子的平均邻近水数", "Mean neighbouring waters per ion"))
    axes[0].set_title(tr("直接计数的累积邻近水", "Cumulative water-neighbour counts"))
    axes[1].set_xlabel(tr("水的偶极方向与离子向外径向的余弦", "Cosine: water dipole vs outward radial direction"))
    axes[1].set_ylabel(tr("概率密度", "Probability density"))
    axes[1].set_title(tr("给定距离窗口内的水朝向", "Water orientation within stated distance windows"))
    for ax in axes:
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=.15)
    finish(fig, "hydration-structure")
    np.savetxt(args.out / "neighbour_counts.csv",
               np.column_stack([radii, np.array(neighbour_records[3]).mean(axis=0),
                                np.array(neighbour_records[4]).mean(axis=0)]),
               delimiter=",", header="radius_A,Na_mean_waters,Cl_mean_waters", comments="")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7.5), sharex=True, layout="constrained")
    pmean = {k: np.array(v).mean(axis=0) for k, v in profiles.items()}
    axes[0].plot(zmid, pmean["water"], label=tr("水", "Water"), color="#167d84")
    axes[0].plot(zmid, pmean["wall"], label=tr("壁原子", "Wall atoms"), color="#89999c")
    axes[1].plot(zmid, pmean["Na"], label="Na⁺", color="#466eaa")
    axes[1].plot(zmid, pmean["Cl"], label="Cl⁻", color="#c16b3d")
    axes[1].set_xlabel("z / Å")
    for ax in axes:
        ax.set_ylabel(tr("质量密度 / g cm⁻³", "Mass density / g cm⁻³"))
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=.15)
        ax.set_xlim(-20.2, 20.2)
    axes[0].set_title(tr("沿限域方向的切片密度：15–30 ps，切片宽0.5 Å", "Density across confinement: 15–30 ps, 0.5 Å slices"))
    finish(fig, "electrolyte-density")
    np.savetxt(args.out / "density_profiles.csv",
               np.column_stack([zmid] + [pmean[k] for k in ("water", "Na", "Cl", "wall")]),
               delimiter=",", header="z_A,water_g_cm3,Na_g_cm3,Cl_g_cm3,wall_g_cm3", comments="")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

按文件开头命令分析例题目录，--language zh或en选择图中文字。

完整程序把读取、几何复原、统计和绘图连在一起。它按原子编号排序，核对每个氧后面两个编号确实对应同一个水的两个氢，再检查总电荷与各类型数量；随后分别计算水的约束几何、偶极方向、邻近水数和沿z的质量密度。Na⁺距离窗口里累计记录2283个离子—水配对，平均朝向余弦约0.680；Cl⁻窗口里有3324个配对，平均约−0.426。这些是重复出现的局部配对观测，数目本身不提供独立样本数量。程序把摘要和曲线数据同时保存，图上的每个结果都可以回到相应的距离与时间定义。

### 离子周围的水数与朝向分布

对15–30ps的31帧和每类15个离子统计。Na⁺报告半径3.3Å，Cl⁻为3.9Å，朝向配对分别2283与3324次。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s7)

15–30 ps的31帧中，按指定半径数水氧邻居，并统计离子—水方向与水偶极方向的夹角余弦。Na⁺半径3.3 Å，Cl⁻半径3.9 Å；右图每一对离子和邻水构成一次观测，同一水可在多个保存时刻出现。

## 从局部水化走向界面：把平均量放回空间里

现在把整条窄缝沿z切成许多薄片，每片厚0.5Å，横截面积等于盒子的x边长乘y边长。对每一帧，分别把水、钠、氯和壁原子落在各切片中的质量相加，再除以切片的实际体积，最后在选定时间窗口平均。这就得到沿限域方向的质量密度曲线。切片越薄，位置分辨越细，但一片中包含的粒子也越少，曲线会更有起伏。改变切片厚度时，应该同时比较空间细节和统计平滑程度，而不是认为越尖锐的峰就一定越接近真实结构。

在物理切片体积内统计质量密度式 7

![在物理切片体积内统计质量密度](https://ml-biomat.com/static/agent-math/faa289b21865b52afc9a2080.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρk | 切片k内所选粒子的平均质量密度 | g cm⁻³ |
| mi | 原子i的摩尔质量数值 | g mol⁻¹ |
| NA | 阿伏伽德罗常数6.02214076×10²³ | mol⁻¹ |
| A | 切片横截面积，此式换算成cm² | cm² |
| Δz | 切片厚度，此式换算成cm | cm |
| Nf, f, i, k(f) | 帧总数、帧编号、原子编号与帧f中位于切片k的原子集合 | 1 |
| Σ, ∈, /, ×, = | 对帧和属于切片的原子求和；除以帧数、阿伏伽德罗常数和体积；相邻因子相乘；等号定义 | 1 |

怎样理解摩尔质量除以阿伏伽德罗常数得到单原子质量，再除以切片体积并对帧平均。

算一个例子24.24Å×24.24Å×0.5Å=293.7888Å³=2.937888×10⁻²²cm³；10个完整水的质量取10×18.0154/NA克，密度约1.01826g/cm³。

使用条件质量逐原子分配到切片；水、离子和壁分别统计。电荷密度需另外把TIP4P负电荷放到M位置。

公式中出现阿伏伽德罗常数，是因为输入的原子质量按g/mol给出，而切片里放的是有限个原子。先用每摩尔质量除以每摩尔的粒子数，就换成单个原子的克数。长度也要统一：1Å等于10⁻⁸cm，所以1Å³等于10⁻²⁴cm³。以一个24.24Å×24.24Å×0.5Å切片为例，它的体积约293.789Å³；若某一时刻正好包含10个完整水分子，对应的水质量密度约1.018g/cm³。实际程序逐原子分配质量，因此一个跨越两片的水会把氧和氢质量放进各自所在的切片，总质量仍然守恒。

### 沿窄缝法向的真实质量密度

0.5Å切片按实际横截面积归一化，分别显示水、壁与两种离子；平均窗口15–30ps。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/#zh-s8)

沿z方向以0.5 Å厚度分箱，在15–30 ps平均的质量密度。各切片按实际横截面积与厚度归一化，水、壁与两类离子分别绘制，保留窄缝内不均匀的分布。

实际曲线中，壁原子形成多层较窄的峰，水在接近壁的区域出现比中间区域更明显的分层。离子数较少，钠和氯的曲线起伏更强，而且本次有限时间窗口的上下分布并不完全对称。质量密度还包含粒子质量差异：Cl⁻比Na⁺更重，即使两处离子个数相同，氯的质量密度也可以更高。若要比较富集了多少离子，应进一步使用数密度或切片计数；若要比较水层和壁层的质量分布，则当前质量密度正合适。先把纵轴对应的对象说清楚，才能把峰高变化解释成相应的物理变化。

把本节移到一个新的生物材料问题时，可以沿着相同的测量顺序展开。先确认聚合物或表面的电荷状态、所用水模型和离子参数，再决定用体相盒子还是孔道几何；保持这些条件明确后，比较水化邻居、朝向分布和空间浓度。若只改变盐含量，就同时记录实际离子数、所采用的浓度体积和电中性条件；如果材料本身带电，中和它所需的反离子与额外加入的盐也分别计数。这样，含盐环境怎样改变链附近的结构就可以被逐步拆解，而不是只用一个含糊的“加盐以后”概括所有变化。

到这里，一份盐水已经有了几种互相配合的描述：电荷和参数规定相互作用，约束规定水的内部形状，轨迹给出实际排列，邻近计数与朝向分布刻画水化，切片密度把结构放回界面位置。接下来研究一条高分子链时，这些溶剂概念仍然有用。链的伸展、蜷缩和外力响应都发生在周围分子的共同作用之中。我们将把视线移到链本身，用端点距离和回转半径区分“伸得多长”与“占据多大空间”，再把这些几何量与已经建立的分子相互作用联系起来。

## 延伸阅读与开放资料

- [Nanosheared electrolyte — A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial4/nanosheared-electrolyte.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0

  TIP4P/2005限域盐水的生成与准备流程。

  保留原模型与准备参数；增加数值轨迹、局部水化分析及双语解释，剪切专题见后续课程。
- [TIP4P and OPC water models; lj/cut/tip4p pair styles](https://docs.lammps.org/Howto_tip4p.html) · LAMMPS developers · Official technical documentation; referenced for definitions and parameters

  核对TIP4P/2005几何、电荷及隐式M位置。

  几何图和公式说明重新绘制与组织。
- [pair_style lj/cut/tip4p/long](https://docs.lammps.org/pair_lj_cut_tip4p.html) · LAMMPS developers · Official technical documentation; referenced for implementation definitions

  连续O/H/H编号、M电荷与几何混合规则。

  以完整输入和解析朝向练习解释。
- [fix shake and kspace_modify commands](https://docs.lammps.org/fix_shake.html) · LAMMPS developers · Official technical documentation; referenced for algorithm definitions

  约束、最小化阶段强谐振限制及历史算法说明。

  补充初始几何与实际记录的核对。
- [kspace_modify — slab geometry](https://docs.lammps.org/kspace_modify.html) · LAMMPS developers · Official technical documentation; referenced for numerical geometry

  平板延展体积与二维周期静电近似。

  重新绘制物理区域与延展区域示意。
- [Svante Arrhenius — Facts; The development of modern chemistry](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-chemistry-the-development-of-modern-chemistry/) · Nobel Prize Outreach · Historical source cited; archival images are not reused

  1884年研究及电解离理论的历史背景。

  采用离子晶格与水化环境的原创概念图。
- [A general purpose model for the condensed phases of water: TIP4P/2005](https://doi.org/10.1063/1.2121687) · J. L. F. Abascal and C. Vega · Research article citation; model parameters cross-checked against official documentation

  水模型名称、提出者及2005年的科学背景。

  模型几何和电荷分布用原创图解展开。
