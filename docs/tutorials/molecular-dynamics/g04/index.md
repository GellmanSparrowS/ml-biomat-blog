# 分子为什么这样运动：力场、时间步与边界

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g04/
Language: zh-CN

从吸引和排斥到周期空间，再用同一盒水的1飞秒与2飞秒计算分开观察快速波动和缓慢漂移。

## 同一杯水，可以有不同的计算描述

把一滴水放在叶片上，它会聚成圆润的水珠；把盐放进水中，晶体会逐渐消失；把一条蛋白质链放进水中，水分子又会参与它的形状变化。这些现象都与分子间的作用有关。分子动力学想做的事情，是给这些作用一个可以计算的描述，让计算机根据当前的位置求出受力，再向前推进一小段时间。因此，看到轨迹里分子动起来之后，接下来最值得追问的是：程序依据什么判断吸引或排斥，它每一步走得有多远，又把盒子外面的世界处理成什么样？这些选择共同决定了我们正在研究哪一种“水”。

可以把一次模拟想成在地图上规划行程。地图标注了道路怎样连接，对应模型里有哪些原子、哪些原子相连；路面的坡度影响车辆怎样加速，对应势能随构型的变化；导航多长时间更新一次位置，对应数值积分的时间步；地图边缘怎样继续，则对应边界条件。这个比喻最有用的地方，是帮助我们区分几种改动：增加导航更新频率能够更细致地描述同一段道路，却不会自动修正一张画错了道路的地图。同样，把时间步从2飞秒减为1飞秒，主要是在检验计算方法对既定模型的描述，水模型本身的电荷和相互作用参数仍然保持原样。

本讲继续使用前面准备好的884个SPC/E水分子。每个水分子由一个氧位点和两个氢位点组成，分子动力学阶段保持固定的内部几何，水分子仍然能够整体平移和转动。这个选择适合从分子间运动理解液态水的组织与涨落，也让我们能在普通电脑上比较计算设置。水的O—H伸缩振动和质子在分子之间的转移需要另外的描述，不能从这套固定连接关系中读出来。把研究问题说到具体运动上，模型的用途就清楚了：我们现在关心的是一套经典刚性水模型怎样被数值推进，以及怎样检查推进过程中的能量变化。

这一讲最终会得到一组真实的对照图。两条分支从同一份已经经过温控和压控的状态出发，一条每1飞秒推进一次，另一条每2飞秒推进一次，各计算100皮秒。观察时将分别扣除两条分支自己的起始能量，再把缓慢的整体变化和较快的波动分开。理解这组图需要一点力学、周期几何和数据分析知识，我们会在用到它们的地方逐步补齐。读到最后，你应当能够解释输入文件中的时间步、截断距离、约束和PME分别在解决什么问题，并且能为一个具体结果选择合适的检查方法。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/#zh-s1)

图 1 · LJ单对势说明吸引与排斥的距离尺度；刚性水还具有带方向的电荷分布。

## 从吸引和排斥理解力场里的数字

“力场”这个名字容易让人想到一张已经画好的力的地图。实际使用时，它更接近一套根据构型计算势能的规则：有哪些相互作用，每种相互作用采用什么数学形式，以及不同原子类型对应哪些参数。势能可以先理解为与排列方式有关的一本能量账。把两个原子挤到非常近的位置，账面代价往往迅速上升；在适当距离，吸引作用又可能让势能下降。力则告诉我们这个账面数值沿哪个方向下降得最快。山坡上的小球会沿坡面加速，分子也会对势能随位置的变化作出响应，只是它同时受到许多邻居的影响。

一个常见的距离作用项是Lennard–Jones势，简称LJ势。它把近距离的强排斥和稍远距离的色散吸引写进同一个表达式。排斥与电子云重叠所产生的量子效应有关，在这里由一个方便计算的陡峭函数近似；色散吸引来自电子分布涨落之间的关联，也被折合为距离函数。知道这层物理来历，可以避免把图上的圆球当成真的硬球：原子没有一层严格不可穿过的彩色外壳，图中的大小只是帮助我们看懂空间关系，而势能函数规定了接近时的代价怎样变化。

用距离描述LJ吸引与排斥式 1

![用距离描述LJ吸引与排斥](https://ml-biomat.com/static/agent-math/cb02485b464c14b929bd8ac8.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ULJ | 一对位点的Lennard–Jones势能项 | kJ·mol⁻¹ |
| r | 两个位点之间的距离 | nm |
| σ | 本表达式势能为零时的距离参数 | nm |
| ε | 正的势阱深度，决定能量尺度 | kJ·mol⁻¹ |
| 4, 12, 6 | 数值系数4与两项的幂指数12、6 | 无量纲 |
| =, /, −, [ ], ( ), × | 等号定义势能；分数线相除；减号组合排斥与吸引；括号分组；相邻因子相乘 | 运算符无单位 |

怎样理解距离比σ/r无量纲；短距离时十二次方项增长更快，稍远处六次方吸引项占优。ε恢复能量单位。

算一个例子取示意参数σ=0.30nm、ε=0.65kJ·mol⁻¹。r=0.30nm时U=0；最低点r=2^(1/6)σ≈0.3367nm，U=−0.65kJ·mol⁻¹。这组数用于读曲线，不是本次SPC/E参数表。

使用条件展示未截断、未平移的单对LJ项。水的总势能还包含电荷作用；实际短程算法、能量平移与长程修正按运行设置处理。

式子中最先需要看懂的是距离比值。距离r与参数σ都用纳米表示，二者相除后单位抵消，所以十二次方和六次方作用在一个纯数上。若r等于σ，两项刚好相消，势能为零；再稍微拉开一些，吸引项占上风，势能变成负数；接近到比σ更短时，十二次方项增长得特别快，排斥占主导。ε给出势阱深度，也就是曲线最低处相对于远距离零点下降了多少。最低点位于约1.122σ处，因此σ并不是最低能量间距。把两个参数的作用分开看，改变σ主要是在横向移动距离尺度，改变ε主要是在纵向改变相互作用强度。

在这套SPC/E模型里，LJ作用放在氧位点之间，分子之间还存在各个带电位点的静电作用。氧带负的部分电荷，两个氢各带正的部分电荷，总电荷相加为零。这里的“部分”说明它们是用来近似分子电荷分布的模型参数，并不是把氧当成一个游离氧离子、把氢当成两个游离质子。两个整体中性的水分子仍然能够感受到对方不同位置的正负电荷，转向不同，多个电荷对的距离也随之改变，于是相互作用具有方向性。水分子在合适取向下形成的氢键网络，正是研究液态水组织时经常观察的对象。

日常说“异号电荷相吸”，可以从库仑能的符号理解：两个电荷相乘为负，适当接近会降低这部分能量；同号电荷的乘积为正，接近则提高能量。完整液体中的静电能需要把许多电荷对及周期环境的贡献一起处理。显式水模型已经用许多水分子的取向响应来描述屏蔽，因此本例没有再把所有电荷相互作用除以一个约80的宏观水介电常数。宏观介电常数概括的是大量分子共同响应后的结果，将它随手叠加到这一显式模型里，会改变原有参数所对应的物理描述。

选择力场时还要注意“配套”。水分子的电荷、氧的LJ参数、约束几何和长程作用处理一起构成模型；蛋白质体系中，还会增加键角、二面角及不同原子类型之间的组合规则。只因为两个文件都能被程序读入，就把来自不同体系的参数拼起来，得到的整体未必保留任何一套原模型的性质。比较不同模型时，应把它们各自规定的参数组合完整写清楚，再选择密度、构象分布或水化等与问题有关的观测量。这样，数值差异才有明确的科学对象，而不只是两个文件夹的输出不一样。

## 每一步走多远，取决于需要追踪多快的运动

电影每秒播放许多画面，连续运动便出现在眼前。分子动力学也采用离散时刻，但这里的下一帧需要根据当前受力计算出来。假设一个粒子在很短时间里受到近似不变的力，那么就可以先更新速度，再用速度更新位置；新的位置又决定新的受力，如此反复。时间步越大，每次更新跨过的时间越长，完成同样物理时长所需的更新次数越少。与此同时，跨步期间的受力变化也更容易被粗略处理。这就是速度与精细程度之间最直接的联系。

怎样判断时间步是不是太大？想象用手指逐次记录一个摆球的位置。如果摆球往返一次需要一秒，每半秒记一次就可能错过转折处的细节；如果还有一个快速振动的细小部件，记录频率还要照顾这个更快的运动。分子中也存在不同时间尺度：含氢共价键的伸缩很快，水分子的转向和邻居重排较慢，蛋白质的整体构象变化又可能更慢。积分步长需要稳定地处理模型里实际保留的快速运动，不能只根据我们最终想观察的慢过程来设定。

约束提供了一种明确改变模型自由度的方法。SPC/E水在动力学阶段把分子内部的两条O—H距离和H—H距离固定下来，三个位点形成的几何便保持不变。程序需要求出维持这些几何关系所需的约束修正，同时继续计算水分子之间的作用。这样一来，模型不再显式追踪内部键长振动，可以采用适合刚性水的时间步。输入中出现的h-bonds指含氢的共价键约束选项；本例的水几何具体由拓扑中的SETTLE处理。它没有把水分子之间不断变化的氢键网络固定成一张不动的网。

1967年，Loup Verlet用Lennard–Jones粒子研究经典流体，推进算法与邻居信息的有效组织成为分子模拟发展的重要工具。这个历史节点对应的是一个一直存在的实际问题：计算机怎样把大量简单的局部更新积累成有用的流体统计？今天使用的算法仍然要在计算成本、误差和物理量的定义之间取得一致。GROMACS中本例的md积分器采用蛙跳形式，位置与速度记录在交错的时间位置上，名字也由这种“跨过去再跨回来”的更新方式而来。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/#zh-s3)

图 2 · Verlet在1967年的经典流体工作提供历史背景；图示为本例GROMACS所用蛙跳积分的位置与速度时间安排。

交错时间的细节会影响能量的比较。动能与速度平方有关，蛙跳算法在整步时刻报告的动能使用相邻半步动能的平均，而半步间隔随时间步改变。本次1飞秒和2飞秒分支的初始报告总能量分别为−34831.664062与−34812.765625kJ·mol⁻¹，它们读取同一份NPT保存状态，却具有不同的离散能量基线。这一差值需要结合速度的时间位置及动能定义理解，不能直接解释成某条分支突然获得了额外热量。我们更关心的是每条分支相对于自己的起点怎样变化。因此后面的图会让两条能量变化曲线都从零开始，再比较各自随时间的趋势和波动。

还有两个容易混在一起的时间设置：积分步长与保存间隔。每2飞秒算一步、每100步保存一次能量，意味着能量表每0.2皮秒一行；每1飞秒算一步但仍每100步保存，表格就每0.1皮秒一行。第二张表行数更多，并不意味着它拥有更多独立的分子构型，也不代表两条轨迹研究了不同的总时长。本例把两条分支都算到100皮秒，并在分析时选择它们共同拥有的0.2皮秒保存时刻。这样，每条拟合使用501个相同时间位置的测量，比较的是同一时间窗口下的数值行为。

## 走出盒子边缘，为什么会从另一边回来

一小盒水如果直接放在真空里，外层水分子与里面的水分子会处在完全不同的环境中：里面的分子四周都有邻居，表面分子的一侧却没有水。研究水滴或界面时，这种差异正是问题的一部分；研究普通体相液体时，大量人为表面会妨碍我们观察内部环境。周期性边界把盒子想象成向三个方向重复铺开的单元。一个分子从右侧离开，就以等价的位置出现在左侧；边界不是墙，也没有在越界时把分子弹回去。

先在一维上理解距离。长度3纳米的周期区间里，一个位点在0.1纳米处，另一个在2.9纳米处。如果只看坐标数值相减，两者相距2.8纳米；如果跨过周期边缘，它们实际最近的镜像却只相隔0.2纳米。短程相互作用需要使用与这种周期几何一致的距离。最小镜像规则就是在等价的周期复制中选择最近的一份。这里说的复制，是同一个模拟单元的周期映像，不是额外生成一批独立随机运动的水分子。

在一维周期区间里找最近的位移式 2

![在一维周期区间里找最近的位移](https://ml-biomat.com/static/agent-math/e61e73c822f13935af958b4b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Δx | 直接坐标差，本例采用x2−x1 | nm |
| ΔxMI | 最小镜像下带方向的位移；其绝对值是距离 | nm |
| L | 周期区间长度且为正 | nm |
| round | 将无量纲比值取到最近整数，表示跨越的盒长数 | 无量纲 |
| Δ, MI, =, −, /, ×, ( ) | Δ表示差；MI标注最小镜像；等号定义；减去整数倍盒长；分数线相除；相邻因子相乘；括号分组 | 运算符与标注无单位 |

怎样理解等价周期位移相差整数倍盒长。减去最近的整数倍L，把位移放到最靠近零的一段区间内。

算一个例子x1=0.1nm、x2=2.9nm、L=3nm，直接位移2.8nm，round(2.8/3)=1，因此最小镜像位移−0.2nm，距离为0.2nm。

使用条件用于一维区间或正交盒的对应分量。斜盒应使用完整盒矢量。恰好相隔半个盒长时有两个等距方向，距离相同。

[Figure: 一维周期最小镜像距离](https://ml-biomat.com/tutorials/molecular-dynamics/g04/#zh-s4)

灰线为直接坐标间隔，橙线为最短周期路径。A固定在0.10nm。

移动位点，比较同一对坐标的直接距离与最短周期距离。

交互图固定一个位点的位置，让另一个沿着3纳米的周期区间移动。你会看到直观的坐标差与最短周期距离有时相同，有时不同。尤其在两点分别靠近左右边缘时，画面上它们分得很开，周期几何里却成了近邻。这也解释了为什么直接看轨迹可能出现“分子被切开”或“突然跳过盒子”的现象：显示程序把等价坐标放回选定单元，改变的是展示位置。分析分子内部距离、整条链的形状或连续位移时，需要分别采用合适的重组、居中或展开处理，让所用坐标与观测量的定义一致。

周期边界把表面问题转变成有限尺寸和周期重复的问题。盒子里的长波长涨落受到可容纳空间的限制，溶质也会通过周期环境感受到其映像的影响。对于纯水，增加盒子大小能够帮助我们检查某些统计量是否明显依赖尺寸；对于一条较长的聚合物，还要检查它在运动中是否靠近自己的周期映像。最小镜像距离处理正确，并不自动说明盒子已经足够大，因为“距离怎么算”和“这个有限环境是否适合问题”属于两个相连但不同的检查。

在简单立方盒中，短程截断半径应小于盒长的一半，才能为这一短程相互作用保持所需的最小镜像几何。本例初始盒长3纳米，短程截断为1纳米，NPT调整后的盒子也要继续满足相应条件。蛋白质章节会使用节省溶剂数量的非立方单元，那时应根据实际盒矢量理解限制，不能机械地把本节一维公式逐坐标套到所有斜盒上。现在掌握立方情形，已经足以解释为什么密度、邻居距离和分子在画面中的位置需要同时考虑边界。

## 近邻逐个计算，远处的电荷怎样处理

如果每一步都让每个粒子与其他所有粒子配对，体系规模增大时，计算次数会迅速上升。对于随距离衰减较快的某些作用，可以在一定范围内显式计算，并按照模型和算法的规定处理远处贡献。输入里的截断半径因此不是原子影响力突然在自然界消失的位置，而是计算分工的一部分。本例LJ短程半径为1纳米，同时使用能量和压力的长程色散修正。修正依赖远处环境近似均匀等条件，理解这一点有助于将来区分均匀水盒和具有明显界面的膜体系。

邻居表则进一步减少了查找工作的重复。程序先列出可能进入相互作用范围的粒子对，在随后若干步中复用这份名单。为给粒子移动留出余量，名单覆盖的范围通常比实际计算短程作用的范围更大。可以把它想成商店提前列好的周边配送名单：名单半径之外的人短时间内很难进入服务区，名单范围之内的人也并非每一刻都需要配送。相互作用截断与名单缓冲承担不同职责，前者规定这一部分力算到哪里，后者帮助名单在更新之间仍能包含需要计算的邻居。

这次比较把邻居表半径固定为1.2纳米，短程作用半径保持1纳米，并让两条分支都每10步更新邻居表。这样可以避免自动缓冲选择随时间步改变后，再把缓冲差异混进比较。不过，相同的10步在1飞秒分支中对应10飞秒，在2飞秒分支中对应20飞秒，因此我们固定的是更新步数规则，不是完全相同的物理更新时间。后续若要进一步分离这一影响，可以让1飞秒分支每20步更新，建立另外一组匹配物理时间的对照。本节先把实际采用的条件说完整，再据此解释结果。

静电作用衰减得更慢，简单地在某个距离外全部丢弃容易造成明显误差。粒子网格Ewald方法，通常写作PME，把周期电荷体系中的计算拆成适合近距离直接求和的部分和适合在网格上处理的平滑长程部分。Darden、York和Pedersen在1993年提出的PME方法，让周期体系的长程静电计算可以借助网格和快速傅里叶变换提高效率。这里的网格是一种数值工具，不是把水变成了固定在格点上的粒子；水分子仍然在连续空间中运动，电荷信息按算法映射到网格再计算相应贡献。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/#zh-s5)

图 3 · PME方法的计算分工示意：近处直接计算和网格长程部分共同处理周期电荷体系。

因此，coulombtype等于PME且rcoulomb等于1.0，并不意味着1纳米之外的电荷被忽略。这个距离主要参与实空间和网格空间工作的划分，整个计算还受网格间距、插值阶数和误差容限等参数影响。初学时可以先把PME看成一种保持周期长程作用的计算方案，再逐步学习各项精度设置。调整这些参数时，要同时观察能量、力或目标观测量怎样改变，以及运行成本增加了多少，才能判断额外精度是否服务于当前科学问题。

从这一层看，输入文件里的几个短单词已经连成了一幅完整图景：pbc规定重复的空间，PME规定周期电荷的长程处理，rvdw规定LJ显式短程范围，rlist和nstlist组织近邻计算，dt规定时间推进的间隔。每一个都能影响结果，但影响途径不同。遇到一条异常曲线时，先沿着这幅图景定位问题，比同时更改许多参数更容易得到可解释的结论。例如，已经存在严重原子重叠的起点应先处理几何；增加PME精度不能替代这一步。

## 让两条分支从同一个状态出发

本次对照使用同一份NPT末态坐标和检查点，保留884个水分子的数目、拓扑、电荷、相互作用参数以及已经形成的速度状态。随后关闭温度和压力耦合，让盒子体积固定，考察能量在数值推进中的行为。这样的NVE设置有明确用途：没有持续的热浴或压浴交换来掩盖体系总能量的变化，数值误差会更容易在记录中显现。瞬时温度仍然会随动能与势能的交换而涨落，所以判断这项测试时应首先看总能量，而不是要求温度始终等于300开尔文。

下面两份输入文件保留了实际比较的设置。1飞秒分支使用0.001皮秒的dt和100000步，2飞秒分支使用0.002皮秒和50000步，两者总时长都为100皮秒。gen-vel设为no，表示不在分支开始时重新随机生成速度；continuation设为yes，配合检查点继续已有状态。两个分支都没有控温和控压。邻居表参数也按上一部分说明固定下来。文件看起来高度相似，正是因为对照实验需要把改变集中在事先明确的条件上。

### 1飞秒分支的完整输入

```
integrator = md
dt = 0.001
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 100000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

从NPT状态继续100ps，固定体积并关闭温控，保留本例固定邻居表设置。

### 2飞秒分支的完整输入

```
integrator = md
dt = 0.002
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 50000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

物理时长相同，时间步与总步数相应变化。

运行脚本在已经准备好的水体系目录中执行，目录内包含npt.gro、npt.cpt和topol.top。这三份文件来自前一讲展示的完整准备过程；它们分别承载坐标、继续运行所需的状态，以及分子组成和参数连接。脚本为两条分支生成各自的运行输入并运行，再导出势能、动能、总能量和温度。grompp中的-t读取检查点，-c提供结构坐标，二者用途相关但并不相同。为保持本次实际比较的执行方式，示例把计算放在CPU上，并指定一致的并行配置。

### 运行两条分支并导出能量

```
#!/usr/bin/env bash
set -euo pipefail
# Start in the prepared water case containing npt.gro, npt.cpt, topol.top,
# nve-1fs.mdp and nve-2fs.mdp. G03 displays the complete preparation inputs.
for branch in 1fs 2fs; do
    gmx grompp -f "nve-${branch}.mdp" -c npt.gro -t npt.cpt -p topol.top -o "nve-${branch}.tpr"
    gmx mdrun -deffnm "nve-${branch}" -ntmpi 1 -ntomp 4 -pin off
    printf 'Potential\nKinetic-En.\nTotal-Energy\nTemperature\n0\n' | gmx energy -f "nve-${branch}.edr" -o "nve-${branch}-energy.xvg"
done
python compare_nve.py . --output figures --language en
```

在包含前一讲已准备好NPT状态与拓扑的目录中执行；同目录放两份MDP和本讲分析脚本。

分析脚本首先读取XVG文件中每一列的legend，按“Total Energy”找到总能量，而不是假定它永远位于某个固定列号。随后对两份表的时间进行核对，找出共有的保存时刻。1飞秒分支原来有1001条记录，2飞秒分支有501条；共有网格包含从0到100皮秒、间隔0.2皮秒的501个时刻。这个步骤没有在两帧之间插入人为数据，而是从真实记录中选取能够直接对应的时间。输出CSV保留每个共有时刻的能量变化和残差，便于重新核对图中细节。

把能量变化分成线性趋势与残差幅度式 3

![把能量变化分成线性趋势与残差幅度](https://ml-biomat.com/static/agent-math/8cdb58bbc54f1396f470f1d5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| E(tk), E(0) | 在保存时刻tk和本分支起点的总能量 | kJ·mol⁻¹ |
| ΔEk | 第k个保存时刻相对本分支起点的能量变化 | kJ·mol⁻¹ |
| tk | 第k个共有保存时刻 | ps |
| a | 对ΔE随时间做最小二乘直线拟合得到的截距 | kJ·mol⁻¹ |
| b | 同一拟合的斜率，描述窗口内线性漂移 | kJ·mol⁻¹·ps⁻¹ |
| R | 扣除拟合直线后的残差均方根 | kJ·mol⁻¹ |
| n, k | n是共有时刻数，本例501；k是记录编号，首条对应0ps | 无量纲 |
| Σ, √, ², /, −, +, =, [ ], × | Σ累加所有记录；差值平方后除以n再开方；减去初值和趋势；加号构造直线；等号定义；括号分组；相邻因子相乘 | 运算符无单位 |

怎样理解各自扣除起点避免混淆离散能量基线；最小二乘用残差平方和最小确定a和b；R量化偏离该趋势的幅度，和b承担不同描述。

算一个例子若三个已拟合残差为−1、2、−1kJ·mol⁻¹，则R=√[(1+4+1)/3]=√2≈1.414kJ·mol⁻¹。若某拟合斜率为−0.1kJ·mol⁻¹·ps⁻¹，其直线在100ps内下降10kJ·mol⁻¹。

使用条件描述指定窗口的线性趋势与残差；分母n定义均方根，不是估计噪声方差时的自由度修正。相关轨迹的这些量本身不提供均值置信区间。

线性拟合在这里承担的是描述作用：用一条直线概括整个窗口内的缓慢趋势，再用残差的均方根描述围绕这条直线的波动幅度。斜率带有每皮秒的单位，因此可以区分“总共降低了多少”和“平均每单位时间降低多少”；残差均方根仍然是能量单位，描述另一种误差特征。程序没有把501个时刻当成501个独立实验，也没有据此给出置信区间。运行命令中的language选择图中文字，数据处理和选取窗口保持一致。

### 在共有保存时刻比较漂移和波动

```
#!/usr/bin/env python3
"""Compare real 1 fs / 2 fs water records on their common saved-time grid.

python compare_nve.py RUN_DIRECTORY --output figures --language en
Dependencies: numpy, matplotlib.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def read_energy(path):
    legends, rows = {}, []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = re.sub(r'[^a-z]', '', match[2].casefold())
            continue
        if line == '&':
            raise ValueError('One XVG dataset per file is required.')
        rows.append([float(value) for value in line.split()])
    values = np.asarray(rows)
    matches = [index + 1 for index, name in legends.items() if name == 'totalenergy']
    if len(matches) != 1 or values.ndim != 2 or len(values) < 3:
        raise ValueError('Missing or ambiguous Total Energy column.')
    if matches[0] >= values.shape[1] or not np.all(np.isfinite(values)):
        raise ValueError('Invalid energy table.')
    time, energy = values[:, 0], values[:, matches[0]]
    if np.any(np.diff(time) <= 0):
        raise ValueError('Saved times must increase strictly.')
    return time, energy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    labels = ['1 fs', '2 fs']
    raw = [read_energy(args.run_directory / f'nve-{step}fs-energy.xvg') for step in (1, 2)]
    # XVG times here have six decimal places; verify rounded times remain unique.
    rounded = [np.round(time, 6) for time, _ in raw]
    if any(len(np.unique(time)) != len(time) for time in rounded):
        raise ValueError('Time rounding merged distinct saved frames.')
    common = np.intersect1d(*rounded)
    if len(common) < 3:
        raise ValueError('Too few common saved times for comparison.')
    changes, trends, residuals, summary = [], [], [], {}
    for label, (time, energy), grid in zip(labels, raw, rounded):
        indices = np.searchsorted(grid, common)
        if not np.allclose(time[indices], common, atol=5e-7, rtol=0):
            raise ValueError('Common-grid matching failed.')
        selected = energy[indices]
        change = selected - selected[0]
        slope, intercept = np.polyfit(common, change, 1)
        trend = intercept + slope * common
        residual = change - trend
        changes.append(change)
        trends.append(trend)
        residuals.append(residual)
        summary[label] = {
            'original_samples': int(len(time)), 'common_samples': int(len(common)),
            'start_ps': float(common[0]), 'end_ps': float(common[-1]),
            'drift_kJ_mol_ps': float(slope),
            'residual_rms_kJ_mol': float(np.sqrt(np.mean(residual ** 2))),
            'end_minus_start_kJ_mol': float(change[-1]),
            'initial_energy_kJ_mol': float(selected[0]),
        }
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'],
                         'font.size': 14, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'path',
                         'axes.unicode_minus': False})
    colors = ['#147d92', '#c56a32']
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.8), constrained_layout=True)
    for i, label in enumerate(labels):
        axes[0, 0].plot(common, changes[i], color=colors[i], lw=1.2, alpha=.85, label=label)
        axes[0, 0].plot(common, trends[i], color=colors[i], lw=2.1, ls='--')
        axes[1, 0].plot(common, residuals[i], color=colors[i], lw=1.0, label=label)
    axes[0, 0].set(title='相对于各自起点的能量变化' if zh else 'Energy change from each branch’s own start',
                   xlabel='时间 / ps' if zh else 'Time / ps', ylabel='ΔE / kJ mol⁻¹')
    axes[1, 0].set(title='去除线性趋势后的波动' if zh else 'Fluctuations after removing the linear trend',
                   xlabel='时间 / ps' if zh else 'Time / ps', ylabel='残差 / kJ mol⁻¹' if zh else 'Residual / kJ mol⁻¹')
    for ax in axes[:, 0]:
        ax.legend(frameon=False)
        ax.grid(alpha=.16)
    drift = [summary[label]['drift_kJ_mol_ps'] for label in labels]
    rms = [summary[label]['residual_rms_kJ_mol'] for label in labels]
    axes[0, 1].bar(labels, drift, color=colors, width=.52)
    axes[0, 1].axhline(0, color='#333333', lw=.8)
    axes[0, 1].set(title='整个100 ps窗口的线性漂移' if zh else 'Linear drift over the full 100 ps window',
                   ylabel='斜率 / kJ mol⁻¹ ps⁻¹' if zh else 'Slope / kJ mol⁻¹ ps⁻¹')
    axes[0, 1].set_ylim(min(drift) * 1.35, .035)
    for i, value in enumerate(drift):
        axes[0, 1].text(i, value - .012, f'{value:.4f}', ha='center', va='top')
    axes[1, 1].bar(labels, rms, color=colors, width=.52)
    axes[1, 1].set(title='去趋势均方根幅度' if zh else 'Root-mean-square residual amplitude',
                   ylabel='RMS / kJ mol⁻¹', ylim=(0, max(rms) * 1.25))
    for i, value in enumerate(rms):
        axes[1, 1].text(i, value + .045, f'{value:.3f}', ha='center', va='bottom')
    fig.savefig(args.output / 'nve_comparison.svg')
    fig.savefig(args.output / 'nve_comparison.png', dpi=170)
    plt.close(fig)
    with (args.output / 'nve_common_grid.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['time_ps', 'deltaE_1fs_kJ_mol', 'deltaE_2fs_kJ_mol',
                         'residual_1fs_kJ_mol', 'residual_2fs_kJ_mol'])
        writer.writerows(zip(common, *changes, *residuals))
    report = {'definition': 'Each branch referenced to its own initial energy; least-squares line and population RMS of its residual on common saved times; no interpolation.',
              'time_grid_ps': float(np.median(np.diff(common))), 'branches': summary}
    (args.output / 'nve_summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
```

需要NumPy和Matplotlib。读取实际XVG，比较两条记录共有的保存时刻，保存中英文图、共有时间CSV与指标JSON。

## 快速波动变小，为什么缓慢漂移仍可能更大

先看左上角的能量变化图，两条曲线都扣除了各自起点的总能量，因此共同从零出发。虚线是整个100皮秒窗口内的最小二乘直线。两条曲线总体都向下变化，但下降速度不同：本次1飞秒分支的拟合斜率约为−0.2287千焦每摩尔每皮秒，2飞秒分支约为−0.0956千焦每摩尔每皮秒。负号表示按这个定义，总能量随时间缓慢降低。这里的每摩尔采用GROMACS对系统能量的输出约定，数值没有再除以884来换成每摩尔水分子的平均能量。

### 1飞秒与2飞秒的NVE能量对照

884个刚性SPC/E水分子；同一NPT起点；各100ps，使用共有0.2ps保存网格的501条记录。曲线分别扣除本分支初始能量，虚线为全窗口直线拟合。

GROMACS 2026.4；884 个 SPC/E 水分子，初始立方盒边长 3 nm；目标温度 300 K、压力 1 bar。NPT 记录 100 ps，描述统计窗口为 50–100 ps；轨迹播放器显示另一个 100 ps NVE 阶段。

[下载参考数据与完整输入（ZIP） 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/#zh-s7)

两条 100 ps NVE 分支在共同的 501 个保存时刻比较，每条曲线都减去自身初始总能量。直线斜率描述这段记录的漂移；下图显示去掉各自拟合直线后的波动，均方根使用总体定义。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 1 fs 共同时间网格能量漂移 | -0.228706 | kJ mol⁻¹ ps⁻¹ |
| 1 fs 去趋势能量均方根 | 0.488938 | kJ mol⁻¹ |
| 2 fs 共同时间网格能量漂移 | -0.095561 | kJ mol⁻¹ ps⁻¹ |
| 2 fs 去趋势能量均方根 | 1.910275 | kJ mol⁻¹ |

再看左下角，把各自拟合直线扣除后，1飞秒分支的快速起伏明显更窄。它的残差均方根约为0.489千焦每摩尔，2飞秒分支约为1.910千焦每摩尔。这个现象与更小步长对快速运动的细致描述相符，也说明为什么只给出一项“能量误差”很容易遗漏信息：在这次对照里，减小时间步使去趋势波动降低，却没有使缓慢漂移的绝对值同时降低。两个指标都来自同一组实际记录，应该一起解释。

能量漂移不仅受时间离散影响，还与力计算的近似、邻居表更新、约束求解以及浮点运算有关。在固定物理时长下，1飞秒分支进行了更多次更新，数值舍入和算法细节的影响也会沿着不同轨迹积累。水的多体运动还会使最初很接近的轨迹逐渐分离，所以100皮秒后两个分子的位置不同，本身不构成程序出错的证据。我们更适合比较清楚定义的统计量和数值诊断，而不是要求每个原子在每个时刻重合。

要进一步追查缓慢漂移，可以有次序地设计新的对照。先保持模型和起点不变，把邻居表更新改成相同的物理时间间隔；再单独提高长程静电或约束求解精度；如果研究目标需要很高的能量守恒精度，还可以比较不同算术精度下的行为。每一次都保留相同的分析窗口和指标定义，才能判断哪项改变产生了什么影响。这样得到的是一条逐步缩小原因范围的证据链，而不是在许多参数同时变化后，挑选一条看上去最平的曲线。

这一组结果也提醒我们，图形的坐标轴要和问题相称。把总能量画在一个包含零点的巨大纵轴范围里，几十千焦每摩尔的变化可能几乎看不见；扣除起始值后，同样的变化便能够清晰呈现。反过来，过度放大的纵轴又可能让很小的数值起伏显得惊人。因此这里同时给出曲线、单位、时间窗口、斜率和残差幅度，让视觉印象可以回到明确的量上。你可以下载CSV重新画图，或选择另一个有物理理由的窗口，观察结论对观察尺度有多敏感。

## 把数值检查带到真正的分子问题里

现在可以回到开头的“地图与更新频率”。力场决定模型如何描述物质，时间步决定怎样推进这一模型，边界和长程处理决定它所处的计算环境，采样时间决定我们观察到了多少运动。它们共同构成一次模拟，但各自回答不同问题。密度接近某个实验值，可以作为检验水模型某项性质的线索；总能量在NVE下表现怎样，可以作为数值推进的检查；聚合物是否充分探索伸展和卷曲状态，则需要关注构象采样。把这几类证据接在一起，才能让模拟结论对应到具体研究对象。

例如，想研究PEG链在水中更舒展还是更紧凑，首先需要一套能一致描述PEG与水相互作用的参数。随后检查键和约束是否允许所选时间步稳定运行，再确认链与周期映像之间的距离是否适合所研究的构象，最后观察链的尺寸和接触分布是否在不同初态、不同时间段中得到足够采样。只把时间步减半而保持一段很短的轨迹，并不会自动让链跨过所有构象障碍；只把模拟延长而保留不合适的相互作用，也不会自动改进材料描述。每个改动都应当对应一个可以检查的问题。

学习时可以先做一个不需要增加模拟成本的练习：在本节两份MDP中分别找到描述物质、时间推进、空间环境和输出记录的选项，然后解释它们为什么属于这一类。接着尝试用相同的CSV选取0到50皮秒和50到100皮秒，重新计算趋势与残差，观察有限窗口怎样影响描述。更进一步的计算练习则应一次改变一个有明确目的的设置，并保存原始输入、软件版本和分析定义。保留这些信息的价值，在于后来遇到不同结果时能够把差异追溯到模型或方法，而不是依赖记忆猜测。

下一讲开始把这套思路用到蛋白质。实验结构会提供原子的位置，但模型还需要确定哪些原子属于蛋白质、如何补充氢、怎样处理端基和带电基团。那时，力场不再只是水的几个参数，而是一套覆盖复杂化学结构的规则。本讲建立的判断顺序仍然适用：先明确分子是什么、周围环境是什么，再问它怎样运动，最后用合适的观测量解释运动。这样读一份运行输入，才能从“软件接受了这些选项”走向“这些选项组成了我要研究的物理体系”。

## 延伸阅读与开放资料

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  周期水盒、参数设置和分阶段准备流程的基础。

  将原TIP4P/Ew流程改为SPC/E、300K、1bar；增加同一起点1fs/2fs的NVE比较、双语教学与独立分析。流程改编保留CC BY-SA4.0。
- [Computer Experiments on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules](https://doi.org/10.1103/PhysRev.159.98) · Loup Verlet · Scientific citation; no reused figure

  1967年经典流体模拟的历史与时间推进问题。

  时间示意图与解释独立绘制和撰写。
- [Particle mesh Ewald: An N·log(N) method for Ewald sums in large systems](https://doi.org/10.1063/1.464397) · Tom Darden; Darrin York; Lee Pedersen · Scientific citation; no reused figure

  1993年PME方法的历史与计算分工。

  绘制短程与长程概念图。
- [GROMACS 2026.4: nonbonded-interactions](https://manual.gromacs.org/2026.4/reference-manual/functions/nonbonded-interactions.html) · GROMACS developers · Technical reference

  核对相互作用、周期几何和积分定义。

  结合本例独立解释和算例。
- [GROMACS 2026.4: periodic-boundary-conditions](https://manual.gromacs.org/2026.4/reference-manual/algorithms/periodic-boundary-conditions.html) · GROMACS developers · Technical reference

  核对相互作用、周期几何和积分定义。

  结合本例独立解释和算例。
- [GROMACS 2026.4: molecular-dynamics](https://manual.gromacs.org/2026.4/reference-manual/algorithms/molecular-dynamics.html) · GROMACS developers · Technical reference

  核对相互作用、周期几何和积分定义。

  结合本例独立解释和算例。
