# 跨过少见的变化：自由能与采样

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l14/
Language: zh-CN

从直接采样的空白出发，用相互重叠的伞形窗口重建自由能，并把误差与分子结构一同读懂。

## 想看见一次罕见变化，需要等多久

一颗药物分子从水里进入膜内部，离子经过狭窄通道，一段高分子从表面脱开，都可能经历这样一种情况：分子一直在动，真正关心的变化却迟迟没有出现。原因往往藏在途中的某些排列里。那些排列在当前温度下出现得很少，轨迹的大部分时间就花在较容易到达的区域。把电影播放得更快只能加快观看速度，增加计算步数才会增加实际观察时间；而且，如果所需时间远大于可承受的计算时长，还需要改变采样策略。

可以把这件事想成调查一座城市里不同街区的活动。若只跟随一位长期待在家附近的行人，很容易把附近街道记录得非常仔细，却对远处街区几乎一无所知。分子运动当然没有个人偏好，但不同构型的统计权重和路径障碍同样会造成不均匀访问。我们希望获得的是各位置在规定环境下的相对出现概率，而不只是把某条有限轨迹曾经走过的区域画得更精细。自由能轮廓正是把这种概率差异转换为能量尺度的一种表达。

本讲先用一个简单的三维粒子体系练习。盒子中央设置一段排斥外势，粒子之间保留短程排斥。外势低时，直接记录位置已经能访问中央区域；外势提高后，同样长的记录会留下空白。接下来，我们给其中一颗标记粒子增加可控制的弹簧，让它分别在不同位置附近活动，形成一组相互衔接的观察窗口。最后根据弹簧改变概率的方式，把各窗口组合成原来没有弹簧时的自由能轮廓。这条路线把“采不到”转成可以逐步诊断的具体问题。

这个模型里的中央区域由数学外势定义，便于把采样方法本身看清楚。将问题换成真实膜，需要建立脂质、水和目标分子之间的相互作用；换成高分子表面脱附，则要描述链的多个接触点、溶剂和表面结构。本例的坐标是一颗粒子的x位置，其他两个方向仍自由活动。后面每一步都围绕这个坐标展开：怎样统计它、怎样限制它，以及怎样检查其附近是否采到了足够的环境变化。掌握这些对应关系后，复杂体系的变量选择才有明确依据。

还要区分两个常被放在一起的问题：某个位置有多容易出现，以及从一个位置到另一个位置通常要花多久。自由能轮廓主要描述前一个问题，它是平衡统计的一种投影；运动时间还受到摩擦、扩散和路径上其他变化的影响。增加弹簧以后，标记粒子的运动受到人为约束，窗口中的时间记录用于统计该受限环境下的分布。要研究实际穿越速度，可以在得到可靠轮廓后，进一步设计动力学测量，把热力学倾向和运动时间分别对应到相应数据。

学习这一讲时，可以先抓住一条连续的思路：记录访问次数，理解为什么次数可以对应自由能，再用可计算的额外作用改善访问，最后检查不同窗口能否连成同一个统计整体。复杂的求解程序放在这些物理关系之后。完整输入、分析和实际图都在本页，既可以从头运行，也可以用已有记录逐段检查。尤其值得关注那些没有得到数据的位置：它们会告诉我们，下一批计算应该放在哪里，而不是让一条看起来完整的曲线替我们填补信息。

## 从访问次数到自由能：对数为什么出现

先把x轴划成等宽的小区间，像沿道路每隔相同距离放一个计数格。保存一次位置，就给相应格子加一。某格次数除以总次数，得到粒子落在这个区间的概率；再除以区间宽度，得到概率密度。二者的单位不同：概率没有单位，沿x的概率密度具有长度倒数单位。把格子宽度减半，一般会减少每格次数，却不会按相同比例改变平滑分布的密度。理解这一点，才能比较使用不同分格宽度的图，而不把绘图设置误认为材料性质。

分格概率与概率密度式 1

![分格概率与概率密度](https://ml-biomat.com/static/agent-math/342ab69e242acd5019c6939f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Hₖ | 第k个分格的访问次数 | 1 |
| N | 总记录数 | 1 |
| k, xₖ | 分格编号及中心位置 | 1, Å |
| Pₖ | 该格概率 | 1 |
| p(xₖ) | 该格中心附近的概率密度估计 | Å⁻¹ |
| Δx | 各格相同的宽度 | Å |
| =, ≈, /, Δ | 相等、近似、相除；Δ标记区间宽度 | 1 |

怎样理解次数除以总次数给出比例，再除以宽度，使密度乘宽度恢复该格概率。

算一个例子二十次记录中四次落入0.5Å宽的格子：P=4/20=0.2，p≈0.2/0.5=0.4Å⁻¹。

使用条件统计同一坐标与同一观察条件，分格等宽；密度近似取决于分格分辨率。

假设在足够充分、条件稳定的观察中，甲位置附近的等宽区间比乙位置附近出现得少十倍。统计力学把这种概率比例写成自由能差的指数，反过来求自由能时就会出现自然对数。负号使稀少的位置对应较高自由能：小于一的比例取对数后为负，再乘负号得到正值。温度提供将无量纲对数转换为能量的尺度。本例使用每摩尔能量，所以系数写作气体常数R乘温度T；若用单个粒子的焦耳能量，则相应使用玻尔兹曼常数乘温度。

用概率比例定义相对平均力势式 2

![用概率比例定义相对平均力势](https://ml-biomat.com/static/agent-math/e27a8ed8ae3ba1317078d846.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ΔA | 相对于参考位置的摩尔PMF差 | kcal mol⁻¹ |
| x, xᵣₑ𝒻 | 所选位置与参考位置 | Å |
| p(x), p(xᵣₑ𝒻) | 两处同定义的概率密度 | Å⁻¹ |
| R | 气体常数，0.00198720426 | kcal mol⁻¹ K⁻¹ |
| T | 绝对温度 | K |
| ln | 无量纲正比例的自然对数 | 1 |
| =, −, /, ×, Δ | 相等、负号、相除、相乘、差值；相邻RT相乘 | 1 |

怎样理解平衡概率的指数关系取对数后得到自由能差，负号使较小概率对应较高PMF。

算一个例子T=119.8K、密度比0.1时，RT≈0.238067kcal/mol，ΔA=−RT ln0.1≈0.548170kcal/mol。

使用条件沿相同笛卡尔坐标、相同温度和定N/V条件的平衡分布；两处密度均为正且单位一致。

119.8K下，RT约为0.2381kcal/mol。概率相差十倍，对应自由能差约0.5482kcal/mol；相差一百倍，差值就是它的两倍，因为一百是两个十相乘，而对数会把相乘变成相加。这一性质也说明为什么概率跨越很多数量级时，自由能图仍能保持容易阅读的尺度。需要比较的是具有相同定义和单位的两个概率密度，比例才没有单位。把“每埃的密度”直接除以“每纳米的密度”之前，应先把长度单位统一。

自由能包含了所有没有单独画在横轴上的自由度。当我们固定一个x位置，粒子仍可沿y和z移动，周围粒子也有许多排列方式；这些可能性都影响该位置的统计权重。因此，自由能轮廓一般不同于某张构型的势能曲线。它可以用“能量代价与可用排列共同决定访问机会”来理解。本例在定粒子数、定体积和恒温环境中计算沿笛卡尔x坐标的平均力势，简称PMF。这样的名称明确了控制条件和投影变量，适合后续解释。

坐标选择还会改变几何计数。沿一条直线划等宽格子，与把空间划成半径相差相同数值的球壳，是两种不同分区方式；远离球心的球壳拥有更大的体积。如果研究两个分子的距离分布，就应考虑球壳体积和问题所需的参考定义。本讲保持笛卡尔x坐标及等宽分格，避免把这些不同定义混在一起。类似地，比较一整片区域的稳定性时，应把该区域的概率累加，再计算区域间的比例；图上单个最低点的高低回答的是局部坐标附近的问题。

自由能的零点可以自由选择，因为概率比例只决定差值。把整条曲线向上平移一单位，不会改变任何两点的差。实际分析把左侧−26到−22Å区间的平均轮廓设为零，再测中央−2到2Å平台相对它的高度。所有时间分段和重采样结果采用同一个参考规则，这样曲线之间的比较才一致。这里的平台高度是指定区间内PMF数值的平均差；若要得到整个中央区相对于左侧区的状态自由能，应改为分别积分概率。

## 先直接观察：同样四纳秒，哪里留下空白

模拟盒子的三个边长为100、30和100Å，三个方向都是周期边界，里面放入二百颗粒子。粒子的质量取39.948g/mol，排斥尺度σ为3.405Å，能量尺度ε为0.238kcal/mol。粒子间使用在LJ最低点截断并平移后的WCA作用，只保留排斥部分。虽然参数采用熟悉的原子尺度，这里观察的是设定外势中的排斥粒子模型。温度为119.8K，时间步为2fs，Langevin阻尼时间为500fs，准备100ps后记录4ns生产过程。

中央外势由两个反正切函数相减得到。反正切把一个从负到正变化的数平滑地压到有限范围；把两个这样的转折分别放在−10Å和10Å附近，相减后就形成中央较高、两边较低的平台。参数δ为1Å，控制边缘转折的宽度；U₀则控制整体能量尺度。实际高度还要乘以两个反正切之差，所以U₀的数值不是平台相对远处的高度。把函数在目标位置算一遍，是读懂这个输入比只看变量名更可靠的方法。

中央排斥外势及相应的力式 3

![中央排斥外势及相应的力](https://ml-biomat.com/static/agent-math/b868d4bb7059d69e11b1cd36.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U(x), U₀ | 位置处外势与控制幅度的能量系数 | kcal mol⁻¹ |
| Fₓ | 外势产生的x方向力，等于−dU/dx | kcal mol⁻¹ Å⁻¹ |
| x | 粒子x坐标 | Å |
| a | 两侧过渡位置的距离参数，本例10Å | Å |
| δ | 过渡宽度，本例1Å | Å |
| arctan | 反正切，输入为无量纲比例，输出角度数值按弧度 | 1 |
| =, +, −, /, ², [, ], 1 | 相等、加减、相除、平方、分组及常数一；相邻量相乘 | 1 |

怎样理解两个平滑转折相减形成中央平台。对位置求导并取负值得到力，外势上升方向对应反向推力。

算一个例子U₀=2.38kcal/mol、a=10Å、δ=1Å时，U(0)=2×2.38×arctan10≈7.002568kcal/mol，中心的Fx=0。

使用条件本讲给每颗粒子施加的原始外势；其能量零点由函数定义，区间间高度另行计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s3)

图 2 · 按公式逐点计算的两条外势曲线。箭头表示外势边缘处推向两侧的力方向；中央高度由完整反正切函数决定。

外势对应的力是能量沿位置变化率的负值。中央平台附近变化较缓，力较小；两个边缘上能量变化明显，力会把粒子推向较低的两侧。完整输入同时写入这个力与相应能量函数，让外加作用的定义保持一致。低外势分支使用U₀=1.5ε，高外势分支使用U₀=10ε。除这个幅度外，两次直接采样的粒子数、盒子和温度等条件相同。图中用实际占据密度恢复轮廓，并同时画出外势的解析参考，帮助观察两种描述之间的联系。

### 低外势完整直接采样

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 1.5*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 1 myreg
create_atoms 1 random 200 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

region mymes block -${x0} ${x0} INF INF INF INF
variable n_center equal count(all,mymes)
thermo_style custom step temp etotal v_n_center
thermo 2000


timestep 2.0
run 50000
reset_timestep 0

thermo 20000
compute cTemp all temp
variable T equal c_cTemp
variable clock equal time
variable population equal count(all,mymes)
fix record all ave/time 1000 1 1000 v_clock v_T v_population file population.dat format " %.15g"
dump trajectory all custom 10000 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id


compute cc1 all chunk/atom bin/1d x 0.0 2.0
fix myac all ave/chunk 100 20000 2000000 &
    cc1 density/number file free-sampling.dat

run 2000000

write_restart final.restart
write_data final.data
```

100ps准备与4ns生产，保存空间密度与中央粒子数。

### 高外势完整直接采样

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 1 myreg
create_atoms 1 random 200 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

region mymes block -${x0} ${x0} INF INF INF INF
variable n_center equal count(all,mymes)
thermo_style custom step temp etotal v_n_center
thermo 2000


timestep 2.0
run 50000
reset_timestep 0

thermo 20000
compute cTemp all temp
variable T equal c_cTemp
variable clock equal time
variable population equal count(all,mymes)
fix record all ave/time 1000 1 1000 v_clock v_T v_population file population.dat format " %.15g"
dump trajectory all custom 10000 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id


compute cc1 all chunk/atom bin/1d x 0.0 2.0
fix myac all ave/chunk 100 20000 2000000 &
    cc1 density/number file free-sampling.dat

run 2000000

write_restart final.restart
write_data final.data
```

改变外势幅度并采用相同观察定义。

### 直接采样实际覆盖

低、高外势各4ns；上图点线来自实际密度，虚线为外势；下图记录中央区粒子数。

开源LAMMPS自由能案例：200个LJ粒子、119.8 K，外势随x变化。低/高外势各4 ns；15个原窗口与32个补充窗口各采样400 ps。

[下载参考数据与完整输入（ZIP） 1.04 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-free-energy-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s3)

低、高外势的原生4 ns直接采样，以空间密度和中央区域粒子数显示实际覆盖。

直接采样图中的低外势记录访问了所有用于统计的x分格，中央区域平均约有1.31颗粒子。高外势记录在中央−10到10Å区域的保存时刻没有观测到粒子，密度分格的中心从−9到9Å出现一串零值。零次观察说明这段记录在这些位置没有提供非零概率估计。程序将相应自由能留空，因为对零取对数没有有限值。若人为给所有空格添上一个小数，画出的高度就会受到那个补数支配，脱离实际访问次数所提供的信息。

四纳秒听起来很短，却已经包含二百万个积分步。这正是罕见变化计算中值得理解的尺度关系：计算机可以执行很多步，而目标过程仍可能很少出现。另一方面，粒子没有进入中央并不表示它们停止运动；两侧的碰撞、扩散和温度涨落仍在进行。应当把“体系有运动”和“关心的坐标区域被充分访问”分别检查。沿位置的密度图与中央粒子数时间记录放在一起，能够更直观地说明这两个层次，也给后续窗口布置确定目标。

这个体系还说明了周期边界下“左右两边”的含义。粒子可以从盒子的一侧穿过周期边界到另一侧，因此左右低势区域通过盒子外沿相连；中央高势区是本讲关心的低概率位置。这里测量的是沿x的占据轮廓，若把它解释成一颗粒子必须穿过中央才能抵达另一端的唯一通道，就改变了实际几何。研究真实膜穿越时，可以围绕膜法向选择坐标，并把周期重复、溶液储库和目标路径一起定义清楚。

## 给少见的位置安排观察窗口

伞形采样的想法是增加一个已知的额外势，使原来很少访问的位置变得容易观察，再在分析中去掉这个额外势改变统计权重的影响。托里和瓦洛在1977年的工作中系统讨论了用专门选择的采样分布估计自由能，并在LJ体系中进行了检验。这个历史出发点很实用：目标分布难采样时，可以先设计更方便的观察分布，只要两者之间的关系可以计算。它把计算资源分配给需要了解的区域，而不要求一条自由运动轨迹自己完成所有访问。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s4)

图 1 · 1977年的伞形采样、1992年的生物分子WHAM应用和2012年的求解与误差分析连接同一个问题：怎样由有意改变的观察分布恢复目标统计。

本例选择一颗粒子作为标记对象，只在x方向增加谐和弹簧。弹簧有一个中心c，粒子偏离中心越远，额外能量按偏离距离的平方增加，回复力则与偏离距离成正比。中心依次移到不同位置，就形成不同窗口。在每个窗口内，粒子仍会围绕平均位置涨落，周围一百九十九颗粒子也继续运动。这样得到的是一段分布而非一个固定点。如果把标记粒子完全冻结，只保存中心数值，就没有办法获得窗口内的概率宽度。

窗口弹簧、回复力与平坦区域宽度式 4

![窗口弹簧、回复力与平坦区域宽度](https://ml-biomat.com/static/agent-math/ee38039566c7e968cbff208b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Wᵢ | 窗口i的附加弹簧势 | kcal mol⁻¹ |
| kᵢ | 该窗口的弹簧系数 | kcal mol⁻¹ Å⁻² |
| x, cᵢ | 标记粒子的位置及弹簧中心 | Å |
| Fᵢᵇⁱᵃˢ | 弹簧产生的x方向回复力 | kcal mol⁻¹ Å⁻¹ |
| s𝒻ₗₐₜ | 平坦原势中谐和位置分布的标准差 | Å |
| R, T | 气体常数与温度 | kcal mol⁻¹ K⁻¹, K |
| i, bias, flat | 窗口编号、附加作用与平坦原势的标记 | 1 |
| =, 1/2, −, ², √, /, × | 相等、二分之一、相减/负号、平方、开方、相除及相乘 | 1 |

怎样理解谐和能量对位置求负导数得到线性回复力；平坦原势下的玻尔兹曼分布为高斯，方差为RT/k。

算一个例子k=0.5kcal/(mol Å²)、x−c=1Å时，W=0.25kcal/mol，F=−0.5kcal/(mol Å)；119.8K下sflat≈0.690025Å。

使用条件弹簧只约束x；宽度公式用于平坦原势与足够宽的空间，实际斜坡和粒子作用会改变分布。

[Figure: 外势和有偏玻尔兹曼位置分布](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s4)

一维玻尔兹曼数值积分：119.8K，范围−32至32Å，网格0.05Å；忽略粒子间作用。

改变中心、弹簧强度或原势，观察一维参考分布的偏移与宽度。概率来自所示外势加弹簧后的玻尔兹曼积分。

这里spring tether命令的弹簧能量是二分之一乘k再乘位移平方。不同软件或不同势函数可能把二分之一吸收到系数里，所以分析一定要使用实际命令的约定。y和z参数写成NULL，表示这两个方向不参加弹簧距离与力的计算；最后的零表示平衡位移为零。若把NULL写成数值零，弹簧就会同时限制横向位置，改变采样的物理问题。这个区别在分子穿膜或表面脱附中尤其重要，因为横向运动本身可以贡献可访问构型的数量。

### 原十五窗口的完整输入

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 0.5

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a loop 15
label loop
variable xdes equal 4*${a}-32
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a
jump SELF loop
```

只约束标记粒子的x坐标，位置每0.2ps瞬时保存。

原始窗口中心从−28Å排到28Å，每隔4Å设置一个，共十五个，弹簧系数为0.5kcal/(mol Å²)。每个中心先准备40ps，再记录400ps，位置每0.2ps保存一次。输入中的ave/time设置为每次只取一个值，因此保存的是瞬时位置。如果先把许多位置平均，再拿平均值画直方图，分布会被压窄；那张图描述的是时间平均位置的涨落，已经不再是PMF所需的原始坐标分布。这个记录设置直接决定后面统计的对象。

可以先在没有外势斜坡的平坦区域估算弹簧窗口的宽度。谐和分布的标准差为RT除以k后开方；在本例温度和k=0.5下约为0.690Å。这个估算说明4Å间距相当于多个分布宽度，窗口之间可能只有很少共同访问。它也提供一个直观取舍：弹簧更硬，粒子更接近指定区域，但分布更窄，需要更密的中心；弹簧较软，分布变宽，却可能被原有势能坡度推离目标位置。两种效果都要在实际位置直方图中检查。

标记粒子在每个窗口里感受到的是原有外势、粒子间作用和新弹簧共同产生的力。因而窗口中心并不必然等于平均位置，特别是在外势的陡坡附近。理解这一点后，就不会把输入表中整齐排列的中心直接当作已经实现的覆盖。我们需要保存实际平均位置、波动范围和访问次数，再据此决定是否补窗口。下一步的窗口图展示了一个很具体的例子：中心写在−8Å附近，粒子却更常停留在比它更靠外的位置。

## 窗口要相互认识：重叠怎样指导补充计算

想把几张局部地图接成一张大地图，相邻地图需要共同标记。伞形窗口的概率分布也需要共同访问的坐标区间，才能确定它们之间的相对统计权重。这里的重叠可以用一个简单量来观察：把两个窗口分别归一化，在每个格子取较小的概率，再把这些较小值加起来。完全相同的两个分布得到一，完全没有共同格子的两个分布得到零。这个量描述当前直方图的公共部分，分格宽度和采样长度都会影响它。

两个窗口的直方图重叠式 5

![两个窗口的直方图重叠](https://ml-biomat.com/static/agent-math/ff7836ba66a7699584caedd2.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Oᵢⱼ | 窗口i、j的重叠，范围0至1 | 1 |
| Hᵢₖ, Hⱼₖ | 两个窗口在格子k的记录次数 | 1 |
| Nᵢ, Nⱼ | 两个窗口的总记录数 | 1 |
| i, j, k | 窗口编号i/j与分格编号k | 1 |
| Σ, min | 对格子求和；每格取两个归一化概率中的较小值 | 1 |
| =, /, (, ) | 相等、相除和分组括号 | 1 |

怎样理解每个格子共同拥有的概率最多等于较小的那份，累加便得到两个分布公共部分的总量。

算一个例子两个两格分布(0.6,0.4)和(0.3,0.7)，重叠为min(0.6,0.3)+min(0.4,0.7)=0.7。

使用条件两窗口使用完全相同的分格，计数非负且总数为正；该量描述所观测坐标的覆盖。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s5)

图 3 · 固定相同的高斯窗口宽度，比较4Å和2Å中心间距。较密中心增加共同访问区域。

### 原十五窗与补充后的覆盖

同一0.1Å分格；下图四十七个窗口按实际平均位置排列，白点标出输入中心。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s5)

15个原始窗口和补充后47个窗口在共同0.1 Å分格中的实际覆盖；中心标记与实际采样位置分别显示。

原十五个窗口的直方图显示，多个相邻区域几乎不相接。中心设在−8Å和8Å的两个窗口，实际均值分别偏到约−10.84Å和10.83Å，因为原有外势斜坡与弹簧回复共同决定了最常停留的位置。也就是说，输入中心位于坡上，并不保证粒子真的把坡上各处都走过。此时把窗口序号简单连成一条曲线，会掩盖相对权重缺少联系的问题。覆盖图把每个窗口放成一行，亮的区域直接显示它真正访问的位置，比只看中心表更容易发现空缺。

补充计算先在原中心之间加入十四个中点，继续使用k=0.5。随后在左右斜坡附近，以0.5Å间距加入十八个较硬窗口，系数改为2.0kcal/(mol Å²)。更硬弹簧在平坦势下的宽度估算约为0.345Å，中心间距也相应缩小。这两类调整解决不同问题：中点帮助连接原来过稀的区域，斜坡上的硬弹簧则提高对目标位置的控制。最终共有四十七个窗口，每个仍保存四百皮秒的实际位置记录，所有窗口采用相同温度和原有粒子相互作用。

### 十四个中点窗口

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 0.5

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30918

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a loop 14
label loop
variable xdes equal 4*${a}-30
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a
jump SELF loop
```

在原中心之间补充k=0.5的窗口。

### 十八个斜坡密集窗口

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 2.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30919

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a index 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
variable centerlist index -11.0 -10.5 -10.0 -9.5 -9.0 -8.5 -8.0 -7.5 -7.0 7.0 7.5 8.0 8.5 9.0 9.5 10.0 10.5 11.0
label loop
variable xdes equal ${centerlist}
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a centerlist
jump SELF loop
```

左右斜坡以0.5Å间距放置k=2.0窗口。

本次分析使用0.1Å宽的分格，把窗口按实际平均位置排序。加入补充窗口以后，排序后相邻窗口的最小直方图重叠约为0.110，整个窗口集合在采用的重叠判断下相连。原十五窗则分成多个弱联系部分。这个结果说明新的记录建立了沿x的连续统计联系。我们同时保留原图，因为它解释了为何增加这些计算、为何在某些位置需要更密的窗口。相同方法换到另一种温度或外势时，应重新查看实际分布，再决定间距与弹簧强度。

一维重叠之外，还要关心同一个x位置对应的其他结构。例如，蛋白质侧链可能有两种转角，水可能以两种方式排列，高分子可能有不同接触状态。两个窗口即使访问相同x范围，也可能各自停在不同的隐藏结构里。对于本例，可以从时间前后分段与周围粒子的运动检查稳定性；在复杂生物分子中，则应增加相关结构变量、不同初始构象或往返准备。这样，沿主坐标的覆盖与环境自由度的调整都有对应观察，而不是只凭一张连续热图判断全部采样。

补充窗口也应保留原始身份。中心位置、弹簧系数、温度、准备时长和记录间隔共同定义了一条观察分布，缺少其中一项，就可能在合并时使用错误权重。本页的完整分析根据实际中心列核对输入表，并检查每条位置记录的步数间隔。文件夹名只帮助组织数据，统计计算依赖的是这些明确参数。若改变一个窗口的弹簧系数，就应同时更新模拟输入与分析表；只改文件名不会改变施加的力，也不会让后处理自动知道新的物理条件。

## 怎样把弹簧的影响从概率中取走

在一个窗口内，某个位置的出现概率由原体系概率再乘以弹簧带来的指数权重，并重新归一化得到。弹簧惩罚越大的位置，在这个窗口中越少出现；要恢复原来的相对概率，就把这个已知惩罚反向补回。比较同一窗口内两个位置时，归一化常数会抵消，因此可以直接写出概率比的修正关系。这个推导解释了为什么必须准确保存k、中心和二分之一约定：它们进入指数，较小的能量定义错误也可能造成明显的统计权重偏差。

在一个窗口里恢复原来的概率比式 6

![在一个窗口里恢复原来的概率比](https://ml-biomat.com/static/agent-math/90f92608a84692880bd989c1.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| p(x), p(y) | 没有附加弹簧时两处的原体系概率密度 | Å⁻¹ |
| pᵢ(x), pᵢ(y) | 窗口i中有弹簧时两处的概率密度 | Å⁻¹ |
| x, y | 同一一维坐标上的两个取值，y在此是第二个取值符号 | Å |
| Wᵢ(x), Wᵢ(y) | 弹簧在两处的附加能量 | kcal mol⁻¹ |
| β | 摩尔热能的倒数 | mol kcal⁻¹ |
| R, T | 气体常数和温度 | kcal mol⁻¹ K⁻¹, K |
| exp | 指数函数，输入无量纲 | 1 |
| =, /, −, ×, [, ], 1 | 相等、相除、相减、相乘、分组及常数一 | 1 |

怎样理解有偏密度正比于原密度乘exp(−βW)。同窗两位置取比消去归一化常数，移项得到修正。

算一个例子若有偏密度比为exp(−1)，而两处弹簧能量差为RT，则原密度比为exp(−1)×exp(1)=1。

使用条件比较同一窗口、同一温度、相同坐标密度；两处都有采样，偏置仅通过所用坐标定义。

多个窗口之间还各有一个归一化常数，需要利用共同访问区来确定。加权直方图分析方法WHAM把所有窗口放进同一组自洽关系：一方面，合并访问次数并按各窗口偏置重新加权，估计原体系概率；另一方面，用这个概率反过来计算每个窗口应有的归一化。反复满足这两种要求，就得到彼此一致的结果。可以把它理解为一组局部地图共同调整比例与高度，使重叠区域相互吻合；这里实际调整的是概率归一化，而非任意平移实验数据。

WHAM的概率与窗口归一化自洽关系式 7

![WHAM的概率与窗口归一化自洽关系](https://ml-biomat.com/static/agent-math/425dba864c798cd4b67cd857.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Pₖ | 无偏体系在格子k的概率 | 1 |
| Hᵢₖ, Nᵢ | 窗口i在格子k的次数与该窗口总次数 | 1 |
| i, k, xₖ | 窗口编号、分格编号及中心位置 | 1, 1, Å |
| fᵢ | 窗口i的无量纲归一化参数 | 1 |
| Wᵢ(xₖ) | 窗口i在格子中心的附加弹簧能量 | kcal mol⁻¹ |
| β | 1/(RT)，摩尔热能倒数 | mol kcal⁻¹ |
| Σᵢ, Σₖ | 分别对窗口与分格求和 | 1 |
| exp, ln | 指数与自然对数，输入均无量纲 | 1 |
| =, /, −, ×, [, ], 1 | 相等、相除、相减/负号、相乘、分组及常数一 | 1 |

怎样理解合并访问次数时扣除每个窗口已知偏置，同时用恢复的概率重新求各窗口归一化；两式共同满足，才能一致连接各段分布。

算一个例子若两个窗口都没有偏置，各有50条记录，其中某格分别出现10与30次，则fi=0，Pk=(10+30)/(50+50)=0.4。

使用条件同温度、同一原体系、等宽分格和连通覆盖的计数WHAM；偏置在格心近似求值，相关性通过时间分块另行评估。

1992年，库马尔、罗森伯格、布齐达、斯文森和科尔曼把这类加权直方图关系发展为适用于复杂生物分子哈密顿量的形式，并用脱氧腺苷糖环的假旋转相位角演示平均力势计算。糖环并非只能保持一张平面多边形的形状，它可以通过多个原子的协同偏离平面改变起伏方式；用一个角度参数概括这种变化，就把许多坐标投影成可采样的集体变量。这段历史把本讲的一颗粒子位置，与生物大分子的内部构象问题联系了起来。

公式里Pₖ是第k个等宽分格的概率，所有格子相加为一；Hᵢₖ记录窗口i在该格出现了多少次；Nᵢ是那个窗口的总记录数。Wᵢ是已知弹簧能量，β等于RT的倒数，fᵢ是无量纲的归一化参数。每个指数中的量因此没有单位。程序先求这些参数，再从概率取对数得到PMF，最后按约定参考区平移零点。理解每个量在数据里对应哪一列，比记住求解器名称更重要，因为同样的求解器无法自行纠正错误的窗口系数或坐标单位。

直接迭代是求解这组关系的一种办法，也可以把它写成等价的概率拟合优化问题。朱方强和胡默在2012年的研究中讨论了更快的优化求解以及统计误差与隐藏自由度采样问题。本页完整程序使用带步长控制的牛顿方法，并在结束后重新代回自洽关系检查残差。实际四十七窗计算用了十二轮迭代，归一化概率和约为一，自洽残差约为1.5×10⁻¹²。这个残差说明方程被精确求解；它与轨迹是否足够长是两个需要分别检验的问题。

### 完整WHAM与统计分析

```
"""Reconstruct the Cartesian-x PMF from instantaneous umbrella coordinates.

Usage: python analyze_wham.py records --output figures --language en
Use --refined other_records when the 32 added windows live in another folder.
Requires NumPy and Matplotlib. Energies are kcal/mol; positions are Angstrom.
The binned WHAM likelihood follows Zhu & Hummer, JCC 33, 453 (2012),
doi:10.1002/jcc.21989. This implementation uses a damped Newton solve.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

R = 0.00198720425864083
TEMPERATURE = 119.8
RT = R * TEMPERATURE


def logsumexp(a, axis=0):
    top = np.max(a, axis=axis, keepdims=True)
    return np.squeeze(top + np.log(np.sum(np.exp(a-top), axis=axis,
                                         keepdims=True)), axis=axis)


def wham(hist, centers, springs, x, initial=None):
    """Solve counts-based WHAM; f_i are dimensionless log normalizers."""
    total = hist.sum(axis=0)
    keep = total > 0
    count = total[keep]
    n = hist.sum(axis=1)
    if np.any(n == 0):
        raise ValueError("An umbrella window has no samples in the histogram.")
    bias = 0.5 * springs[:, None] * (x[None, keep]-centers[:, None])**2 / RT
    base = np.log(n)[:, None] - bias
    f = np.zeros(len(n)) if initial is None else initial.copy()
    f -= f[0]

    def objective(v, derivatives=False):
        logits = base + v[:, None]
        denominator = logsumexp(logits)
        value = count @ denominator - n @ v
        if not derivatives:
            return value
        membership = np.exp(logits-denominator)
        weighted = membership * count
        expected = weighted.sum(axis=1)
        grad = expected-n
        hess = np.diag(expected) - weighted @ membership.T
        return value, grad, hess, denominator

    for iteration in range(300):
        value, grad, hess, denominator = objective(f, True)
        residual = np.max(np.abs(grad)/n)
        if residual < 2e-10:
            break
        # Fix the additive gauge by holding f[0] at zero.
        step = np.linalg.solve(hess[1:, 1:], -grad[1:])
        if np.max(np.abs(step)) > 20:
            step *= 20 / np.max(np.abs(step))
        slope = grad[1:] @ step
        scale = 1.0
        while scale > 2**-30:
            candidate = f.copy()
            candidate[1:] += scale*step
            # A tiny allowance avoids stagnation at machine-precision objective.
            if objective(candidate) <= value + 1e-4*scale*slope + 1e-9:
                f = candidate
                break
            scale *= 0.5
        else:
            raise RuntimeError("WHAM line search failed.")
    else:
        raise RuntimeError("WHAM failed the gradient convergence criterion.")
    probability = np.zeros(len(x))
    logp = np.log(count)-denominator
    logp -= logsumexp(logp)
    probability[keep] = np.exp(logp)
    new_f = -logsumexp(logp[None, :] - bias, axis=1)
    new_f -= new_f[0]
    fixed_point_error = float(np.max(np.abs(new_f-f)))
    if fixed_point_error > 1e-7:
        raise RuntimeError("WHAM self-consistency check failed.")
    pmf = np.full(len(x), np.nan)
    pmf[keep] = -RT*np.log(probability[keep])
    # All curves share the same left reference interval, not their noisy minima.
    reference = (x >= -26) & (x < -22)
    pmf -= np.nanmean(pmf[reference])
    return pmf, f, dict(iterations=iteration+1,
                        relative_gradient=float(residual),
                        fixed_point_error=fixed_point_error,
                        probability_sum=float(probability.sum()))


def correlation_factor(values):
    """Initial-positive ACF estimate in saved-frame units; diagnostic only."""
    y = values-values.mean()
    size = 1 << (2*len(y)-1).bit_length()
    spectrum = np.fft.rfft(y, n=size)
    acf = np.fft.irfft(spectrum*spectrum.conjugate(), n=size)[:len(y)]
    acf /= np.arange(len(y), 0, -1)
    acf /= acf[0]
    stop = np.flatnonzero(acf[1:] <= 0)
    end = int(stop[0]+1) if len(stop) else min(500, len(y)//4)
    return float(max(1.0, 1+2*acf[1:end].sum()))


def overlap_matrix(hist):
    normalized = hist / hist.sum(axis=1, keepdims=True)
    return np.minimum(normalized[:, None, :], normalized[None, :, :]).sum(axis=2)


def component_sizes(overlap, threshold=0.005):
    remaining = set(range(len(overlap)))
    sizes = []
    while remaining:
        todo = [remaining.pop()]
        size = 0
        while todo:
            i = todo.pop()
            size += 1
            neighbors = remaining.intersection(np.flatnonzero(overlap[i] > threshold))
            todo.extend(neighbors)
            remaining.difference_update(neighbors)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def load_windows(baseline, refined):
    windows = []
    grids = [(baseline/'umbrella-original-grid', np.arange(-28, 29, 4), 0.5),
             (refined/'midpoints', np.arange(-26, 27, 4), 0.5),
             (refined/'steep-regions',
              np.r_[np.arange(-11, -6.99, 0.5), np.arange(7, 11.01, 0.5)], 2.0)]
    for folder, centers, spring in grids:
        for number, center in enumerate(centers, 1):
            data = np.loadtxt(folder/f'umbrella-sampling.{number}.dat')
            if not np.allclose(data[:, 2], center):
                raise ValueError("Recorded center differs from its metadata.")
            if not np.all(np.diff(data[:, 0]) == 100):
                raise ValueError("Expected instantaneous coordinates every 200 fs.")
            windows.append(dict(center=float(center), spring=spring,
                                values=data[:, 1], stage=folder.name))
    return windows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--refined', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    parser.add_argument('--bootstrap', type=int, default=80)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    def tr(a, b): return a if zh else b
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in installed],
                         'font.size': 13, 'axes.titlesize': 15,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6'})
    windows = load_windows(args.records, args.refined or args.records)
    xdata = [w['values'] for w in windows]
    centers = np.array([w['center'] for w in windows])
    springs = np.array([w['spring'] for w in windows])
    edges = np.linspace(-32, 32, 641)
    x = (edges[1:]+edges[:-1])/2
    hist = np.array([np.histogram(v, edges)[0] for v in xdata])
    if not np.array_equal(hist.sum(axis=1), [len(v) for v in xdata]):
        raise ValueError("Extend the histogram range to include every sample.")
    overlap = overlap_matrix(hist)
    original = np.arange(15)
    if component_sizes(overlap) != [47]:
        raise ValueError("The umbrella overlap graph is disconnected.")
    pmf, solution, solver = wham(hist, centers, springs, x)
    halves = []
    for part in range(2):
        hh = np.array([np.histogram(np.array_split(v, 2)[part], edges)[0]
                       for v in xdata])
        halves.append(wham(hh, centers, springs, x, solution)[0])
    quarters = []
    for part in range(4):
        hh = np.array([np.histogram(np.array_split(v, 4)[part], edges)[0]
                       for v in xdata])
        quarters.append(wham(hh, centers, springs, x, solution)[0])
    # Resample contiguous 20 ps blocks independently within each window.
    # 2000 points form 20 blocks of 100 saved frames; the final point is omitted
    # only in the bootstrap so all blocks have the same duration and weight.
    rng = np.random.default_rng(14027)
    blocks = [np.array([np.histogram(v[j:j+100], edges)[0]
                        for j in range(0, 2000, 100)]) for v in xdata]
    bootstrap = []
    for repeat in range(args.bootstrap):
        sampled = np.array([b[rng.integers(0, 20, 20)].sum(axis=0) for b in blocks])
        if component_sizes(overlap_matrix(sampled)) != [47]:
            raise ValueError("A block resample has disconnected sampling support.")
        bootstrap.append(wham(sampled, centers, springs, x, solution)[0])
    boot = np.array(bootstrap)
    # The displayed coordinate interval is covered by every resampled profile.
    display = (x >= -28) & (x <= 28)
    if not np.isfinite(boot[:, display]).all():
        raise ValueError("A displayed PMF bin is empty in a block resample.")
    lower, upper = np.full(len(x), np.nan), np.full(len(x), np.nan)
    lower[display], upper[display] = np.percentile(boot[:, display], [2.5, 97.5], axis=0)
    g = np.array([correlation_factor(v) for v in xdata])
    plateau = (x >= -2) & (x < 2)
    barrier = float(np.nanmean(pmf[plateau]))
    barrier_boot = np.mean(boot[:, plateau], axis=1)
    mean_x = np.array([v.mean() for v in xdata])
    ordered = np.argsort(mean_x)
    adjacent = overlap[ordered[:-1], ordered[1:]]
    def save(fig, name):
        fig.savefig(args.output/f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    density_summary = {}
    for stage, color, label, scale in [('free-low', '#167d84', tr('低势垒', 'Low barrier'), 1.5),
                                       ('free-high', '#c16b3d', tr('高势垒', 'High barrier'), 10)]:
        rows = np.loadtxt(args.records/stage/'free-sampling.dat', skiprows=4)
        position, density = rows[:, 1], rows[:, 3]
        ref = density[(position >= -46) & (position <= -34)].mean()
        measured = np.full(len(position), np.nan)
        valid = density > 0
        measured[valid] = -RT*np.log(density[valid]/ref)
        axes[0].plot(position, measured, 'o-', ms=4, color=color, label=label)
        u = scale*0.238*(np.arctan(position+10)-np.arctan(position-10))
        u -= u[(position >= -46) & (position <= -34)].mean()
        axes[0].plot(position, u, '--', color=color, alpha=0.65)
        population = np.loadtxt(args.records/stage/'population.dat')
        axes[1].plot(population[:, 1]/1e6, population[:, 3], color=color,
                     alpha=0.8, linewidth=1, label=label)
        density_summary[stage] = {'zero_density_bin_centers_A': position[~valid].tolist(),
                                  'mean_center_population': float(population[:, 3].mean()),
                                  'density_integral_particles': float((density*6000).sum())}
    axes[0].set(xlabel=tr('位置 x / Å', 'Position x / Å'),
                ylabel=tr('相对自由能 / kcal mol⁻¹', 'Relative free energy / kcal mol⁻¹'),
                title=tr('4 ns 无偏采样：实线来自占据概率，虚线是外势',
                         '4 ns unbiased sampling: probability profiles and external potentials'))
    axes[0].legend(frameon=False)
    axes[1].set(xlabel=tr('生产阶段时间 / ns', 'Production time / ns'),
                ylabel=tr('中央区粒子数', 'Particles in central region'),
                title=tr('中央区：−10 Å < x < 10 Å', 'Central region: −10 Å < x < 10 Å'))
    axes[1].legend(frameon=False)
    save(fig, 'free-sampling-limit')

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    for i in original:
        axes[0].plot(x, hist[i]/hist[i].sum()/0.1, lw=1.3)
    axes[0].set(xlim=(-32, 32), ylabel=tr('概率密度 / Å⁻¹', 'Probability density / Å⁻¹'),
                title=tr('原来的 15 个窗口：势垒斜坡附近出现覆盖缺口',
                         'Original 15 windows: coverage gaps around the barrier slopes'))
    image = axes[1].imshow(hist[ordered]/hist[ordered].sum(axis=1)[:, None]/0.1,
                           origin='lower', aspect='auto', extent=(-32, 32, -0.5, 46.5),
                           cmap='viridis', vmin=0, vmax=1.4)
    axes[1].plot(centers[ordered], np.arange(47), 'w.', ms=3,
                 label=tr('约束中心', 'Restraint centers'))
    axes[1].set(xlabel=tr('位置 x / Å', 'Position x / Å'),
                ylabel=tr('按平均位置排列的窗口', 'Windows ordered by mean position'),
                title=tr('补充到 47 个窗口后的真实覆盖', 'Observed coverage with 47 windows'))
    axes[1].legend(frameon=True, loc='upper left', facecolor='#263d4d', labelcolor='white')
    fig.colorbar(image, ax=axes[1], label=tr('概率密度 / Å⁻¹', 'Probability density / Å⁻¹'))
    save(fig, 'umbrella-coverage')

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    external = 2.38*(np.arctan(x+10)-np.arctan(x-10))
    external -= external[(x >= -26) & (x < -22)].mean()
    axes[0].fill_between(x[display], lower[display], upper[display], color='#167d84', alpha=0.22,
                         label=tr('20 ps 分块重采样 95% 区间', '95% interval from 20 ps block resampling'))
    axes[0].plot(x[display], pmf[display], color='#167d84', label=tr('47 窗口 WHAM', '47-window WHAM'))
    axes[0].plot(x[display], external[display], '--', color='#c16b3d',
                 label=tr('外势：稀薄极限的参照', 'External potential: dilute-limit reference'))
    for i, half in enumerate(halves):
        axes[1].plot(x[display], half[display], label=tr(f'每窗第 {i+1} 个 200 ps',
                                                       f'{"First" if i == 0 else "Second"} 200 ps in each window'))
    for ax in axes:
        ax.set(xlabel=tr('位置 x / Å', 'Position x / Å'),
               ylabel=tr('PMF / kcal mol⁻¹', 'PMF / kcal mol⁻¹'))
        ax.legend(frameon=False, fontsize=12)
    axes[0].set_title(tr('相对于左侧 −26 至 −22 Å 区间的自由能',
                         'Free energy relative to the left interval, −26 to −22 Å'))
    axes[1].set_title(tr('时间分段：分别重建两段记录的轮廓',
                         'Chronological split: two separately reconstructed profiles'))
    save(fig, 'umbrella-pmf')

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), layout='constrained')
    for spring, color in [(0.5, '#163840'), (2.0, '#c16b3d')]:
        selected = springs == spring
        axes[0].scatter(mean_x[selected], g[selected], color=color, s=35,
                        label=f'k = {spring:g} kcal mol⁻¹ Å⁻²')
    axes[0].legend(frameon=False, fontsize=11)
    axes[0].set(xlabel=tr('窗口平均位置 / Å', 'Window mean position / Å'),
                ylabel=tr('初始正值相关因子 g', 'Initial-positive correlation factor g'),
                title=tr('相邻 0.2 ps 记录的相关性', 'Correlation between 0.2 ps records'))
    axes[1].hist(barrier_boot, bins=15, color='#167d84', alpha=0.8)
    axes[1].axvline(barrier, color='#c16b3d', lw=2,
                    label=tr('全记录结果', 'Full-record estimate'))
    axes[1].set(xlabel=tr('中央平台与左侧之差 / kcal mol⁻¹',
                         'Central plateau minus left reference / kcal mol⁻¹'),
                ylabel=tr('重采样次数', 'Resample count'),
                title=tr(f'{args.bootstrap} 次连续分块重采样',
                         f'{args.bootstrap} contiguous-block resamples'))
    axes[1].legend(frameon=False)
    save(fig, 'umbrella-statistics')
    summary = {'temperature_K': TEMPERATURE, 'RT_kcalmol': RT,
               'window_count': len(windows), 'samples_per_window': [len(v) for v in xdata],
               'bin_width_A': 0.1, 'solver': solver,
               'original_overlap_components': component_sizes(overlap[np.ix_(original, original)]),
               'refined_overlap_components': component_sizes(overlap),
               'minimum_adjacent_overlap_by_sample_mean': float(adjacent.min()),
               'central_plateau_minus_left_kcalmol': barrier,
               'block_bootstrap': {'samples': args.bootstrap, 'seed': 14027,
                                   'block_ps': 20, 'blocks_per_window': 20,
                                   'interval_percentiles': [2.5, 97.5],
                                   'plateau_interval_kcalmol': np.percentile(barrier_boot, [2.5, 97.5]).tolist(),
                                   'conditional_scope': 'Resampling recorded 20 ps segments within each window; fixed model, windows and initial trajectories.'},
               'half_plateaus_kcalmol': [float(np.mean(h[plateau])) for h in halves],
               'quarter_plateaus_kcalmol': [float(np.mean(h[plateau])) for h in quarters],
               'correlation_factor_range': [float(g.min()), float(g.max())],
               'external_reference_plateau_kcalmol': float(external[plateau].mean()),
               'unbiased': density_summary,
               'window_statistics': [{'center_A': w['center'], 'spring_kcalmolA2': w['spring'],
                                      'mean_A': float(v.mean()), 'sd_A': float(v.std(ddof=1)),
                                      'correlation_factor': float(g[i])}
                                     for i, (w, v) in enumerate(zip(windows, xdata))]}
    (args.output/'wham_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    np.savetxt(args.output/'pmf.csv', np.c_[x, pmf, lower, upper, external, *halves],
               delimiter=',', header='x_A,pmf_kcalmol,lower_2p5,upper_97p5,external,first_half,second_half', comments='')
    np.savetxt(args.output/'window_overlap.csv', overlap, delimiter=',')
    print(json.dumps({k: summary[k] for k in ['window_count', 'solver',
                                            'central_plateau_minus_left_kcalmol', 'block_bootstrap']}))


if __name__ == '__main__':
    main()
```

核窗口、重叠和自洽关系，计算分段轮廓与连续分块重采样，输出四组图。

重建后的中央平台相对于左侧参考区约高6.8321kcal/mol。外势函数在相同区间与相同零点下给出的参考差约为6.8954kcal/mol。二者接近，符合这个较稀粒子体系中外势对分布的主要影响；粒子间排斥、有限采样和分格处理仍参与实际结果。程序把两条曲线分别计算并展示，没有把一条强行对齐成另一条。对真实生物材料而言，环境重排和构象数量往往更复杂，比较外势与PMF的这一步正好帮助理解为什么平均力势需要从统计中求得。

### 重建PMF与时间分段

左侧−26至−22Å区间平均设零；带为当前轨迹20ps分块的逐点95%分位范围。下图分别使用每窗前后200ps。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s6)

所有窗口以同一左侧区间平均为零；显示连续20 ps分块的80次重采样，以及每窗前后200 ps分别重建的轮廓。

## 一条平滑曲线之后，还有哪些统计问题

每个窗口保存了二千零一条位置记录，但相邻0.2ps的两个位置通常相近，因为粒子运动具有连续性。同一个分子还没来得及离开附近区域，再拍一张照片不等于获得一个完全新的构象样本。增加保存频率能更细致地描述运动，却不必然按比例增加统计独立的信息。分析因此同时计算位置自相关的初始正值估计，本次相关因子大约在1.9到7.5之间。这个量用于观察记录之间的相关程度，实际PMF误差则进一步通过保留连续片段的重采样评估。

先把每个窗口按时间分成前后两段，每段约二百皮秒，分别重建完整轮廓。两段中央平台差为约6.8498和6.8137kcal/mol，使用的都是同一个左侧参考区。再分成四段时，平台值约为6.9905、6.7411、6.8329和6.7947kcal/mol。这些数值让时间变化直接可见：较短子段会有更大的起伏，也能帮助发现持续漂移。分段比较保持了各窗口原有时间顺序，适合检查早期与后期是否给出相容的观察，而不是只看合并后的一条曲线。

另一种检查把每个窗口的前二千条记录划成二十个连续片段，每片一百条，对应二十皮秒。重采样时，从这个窗口自己的二十片中有放回地抽取二十片，再把抽中的访问次数合并；对四十七个窗口分别这样做，然后重新求一次WHAM。一个片段可能被抽到两次，另一个没有被抽到，这模拟了同类有限观察可能出现的统计波动。最后多出的一条记录只在这个等长分块步骤中略去，完整轮廓仍使用二千零一条。

### 相关性与平台差的变化

左图为位置相关因子诊断，右图为80次连续分块重采样的平台差；所有运行保持相同模型与窗口安排。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/#zh-s7)

位置相关性诊断与平台差的分块重采样分布，保留相同模型、窗口和时间序列。

本例做八十次连续分块重采样，中央平台差的2.5%与97.5%分位数约为6.7131和6.9990kcal/mol。图中的带状区域用相同方式逐位置计算。它描述固定模型、当前窗口安排和已有轨迹下的有限采样变化范围。若更换力场、温度或隐藏构象的初始状态，变化来源就扩大了，需要相应的新比较。实际研究可以增加独立窗口运行，并试验不同分块时长，检查区间是否稳定；二十皮秒这一选择也应结合要研究的慢运动重新判断。

重复的层级在这里很重要。八十条重采样曲线都来自同一组原始记录，不是八十次从不同环境重新开始的完整分子模拟。它们擅长利用已有时间片段估计一种统计变化，却不会自动生成原轨迹从未访问过的构象。对比较困难的生物分子，可以分别从结合与分离方向准备窗口，或从不同侧链状态开始，并把这些运行作为独立重复保存。然后在每个重复内部做时间分段，再比较重复之间的轮廓，把局部时间相关与不同初始结构的影响分开观察。

还可以把计算资源安排得更有针对性。如果某两个窗口缺少共同访问，先补位置或改变弹簧；如果覆盖已经连续而某个窗口存在长时间漂移，先延长准备或增加不同初态；如果所有窗口都较平稳，但平台差的区间仍较宽，就增加相关窗口的有效观察时间。这样，每次追加计算都对应一个诊断结果。把窗口覆盖、时间分段和重采样图放在同一页，目的就在于让读者能从具体证据决定下一步，而不是只依据最终曲线是否光滑来判断任务已经完成。

## 把例题变成生物材料中的路径问题

完整运行脚本依次生成低外势直接采样、高外势直接采样、原十五窗、补充中点和斜坡密集窗。每个阶段使用自己的目录保存输出，再由同一个分析程序读取。重建时应保留原始位置文件，不只保存最后一张PMF图，因为窗口中心、分布重叠和时间切片都需要这些记录。若修改温度，分析中的RT也要同步；若更换单位体系，则长度、弹簧系数和能量尺度需要成套转换。能够从输入一路追到每个图上的量，是这个完整例题的基本结构。

### 运行所有采样并分析

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=1
for stage in free-low free-high umbrella-original-grid midpoints steep-regions; do
  mkdir -p "$stage"
  cp "$stage.lmp" "$stage/input.lmp"
  ( cd "$stage"; "$lmp" -in input.lmp -log simulation.log > stdout.log 2>&1 )
done
python analyze_wham.py . --output figures --language en
python analyze_wham.py . --output figures --language zh
```

五个采样阶段各有独立目录；末尾分别生成两语言图。

将标记粒子换成药物分子时，可以用分子质心沿膜法向的位置作为第一种候选坐标，但还要观察分子朝向、氢键与局部膜结构是否能在每个窗口充分调整。分子进入膜内部时，周围水的数量可能变化，脂质也可能重新排列；这些环境变化会进入平均力势。因而较低的某一段轮廓，可以来自更有利的相互作用，也可以与可用构象数量有关。把水化数、接触数和取向一起保存，能帮助把一维轮廓解释成具体的分子过程。

换成高分子从表面脱附，质心高度可能不足以描述全部状态。同样的平均高度下，一条链可能只有一端离开，也可能中段拱起、两端仍贴住，还可能只有少数接触点残留。可以先用轨迹观察这些区别，再考虑加入接触数量、自由端高度或链尺寸作为补充坐标。选择变量时，关键是它能否区分研究关心的状态，并让相同坐标附近的其他结构有机会相互转化。一个容易计算的变量是起点，清楚对应实际变化的变量才能支持后续解释。

最后的比较也要保持状态定义一致。如果研究两种表面对同一条链的吸附倾向，可以使用相同的温度、溶剂条件、接触定义和参考区间，分别得到对应概率，再按需要计算局部PMF或整个吸附状态的概率。若研究链长增加的影响，较长链还会引入更多内部构象与接触组合，应同时检查采样所需时间是否增长。这样，表面、分子结构和采样条件各有明确身份，曲线差异才容易追溯到所改变的材料因素。

通过这一节，可以把一条自由能曲线读成一系列具体事实：横轴规定观察哪种变化，纵轴由相对概率与温度确定，窗口说明数据在哪里得到，重叠连接局部记录，时间统计描述现有观察的波动。再把这些事实与结构图对应起来，计算结果就能够解释分子为什么偏向某些区域，以及怎样设计下一次采样去了解仍不清楚的部分。下一讲将把这种思路扩展到多组模拟比较，讨论怎样安排重复、配对条件和统计单位。

## 延伸阅读与开放资料

- [Tutorial 7: Free energy calculation](https://lammpstutorials.github.io/sphinx/build/html/tutorial7/free-energy-calculation.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0; original input headers retained

  排斥粒子、中央外势、直接采样和伞形采样的原始流程。

  固定源版本dd3dce70，x单独约束、瞬时位置记录、补充32窗、原创统计分析与图。
- [fix spring command](https://docs.lammps.org/fix_spring.html) · LAMMPS developers · Official documentation; command semantics cited

  二分之一弹簧能量与NULL方向约定。

  逐符号解释与可调整的一维分布练习。
- [Nonphysical sampling distributions in Monte Carlo free-energy estimation: Umbrella sampling (1977)](https://doi.org/10.1016/0021-9991%2877%2990121-8) · G. M. Torrie and J. P. Valleau · Research article citation; no original image/text copied

  选择采样分布及LJ验证的历史。

  原创方法历史概念图。
- [The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method (1992)](https://doi.org/10.1002/jcc.540130812) · Shankar Kumar, John M. Rosenberg, Djamal Bouzida, Robert H. Swendsen, Peter A. Kollman · Research article citation; no original image/text copied

  WHAM与脱氧腺苷糖环假旋转的历史应用。

  将概率计数、自洽关系与生物分子变量连贯解释。
- [Convergence and error estimation in free energy calculations using the weighted histogram analysis method (2012)](https://doi.org/10.1002/jcc.21989) · Fangqiang Zhu and Gerhard Hummer · Research article citation; original equations used for independently written analysis

  WHAM优化、自洽检验与采样统计诊断。

  独立实现牛顿求解、时间分段与连续分块重采样；数值另经固定点迭代复核。
