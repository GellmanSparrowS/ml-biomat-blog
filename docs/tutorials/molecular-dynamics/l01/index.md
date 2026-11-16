# 一盒粒子为什么会动

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l01/
Language: zh-CN

从墨水扩散和液体运动出发，建立一盒两类粒子的模型，理解相互作用、时间推进与热运动，再把完整输入、实际轨迹和能量曲线连起来。

## 从一滴液体开始，认识计算机里的粒子

把一滴墨水轻轻放进清水，即使没有持续搅拌，颜色也会逐渐向周围扩散。把同一杯水放到更冷的环境里，分子的运动、液体的黏度以及溶质扩散的快慢都会改变。眼睛看到的是颜色和形状，分子尺度上发生的却是无数次位置变化和相互作用。分子动力学要做的，是建立一个足够明确的微观模型，跟踪它随时间怎样演化，再把这些变化整理成能够与材料性质联系起来的量。第一讲从一盒简单粒子入手，把这条思路完整走一遍。

这里的“粒子”首先是一个模型对象。它有位置、质量和运动速度，还按规定与邻居相互作用；它可以代表一个原子，也可以代表把若干原子合在一起后得到的有效单元。屏幕上的圆球大小是显示方式，而相互作用究竟在多近时变得强烈，由模型参数决定。刚开始就分清这两件事很有用：把圆球画得更大，只会改变图像；把描述排斥尺度的参数调大，才会改变实际计算的运动。我们在这一讲使用两类中性粒子，暂时保留它们的平移运动和短程吸引、排斥。

这类模型适合观察粒子怎样聚集、混合、交换能量，以及一个局部相互作用规则怎样产生整体行为。它的简洁也使我们能把注意力放在计算的逻辑上。水分子的弯曲形状、电荷分布和氢键方向性没有包含在这套两类中性粒子的描述中；研究水和离子时，后面的课程会把这些具体结构加入模型。读完本讲，你应当能够说明每一类输入信息的作用，区分结构调整与真实时间推进，并从轨迹和能量图中读出相互一致的解释。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s1)

图 1 · 编号追踪同一个粒子，类型查找它使用的参数。箭头表示信息对应关系，不表示作用力。

给粒子编号就像给运动场上的人分配号码：号码帮助我们在不同时间认出同一个对象，不决定它的材料性质。类型则像一张参数表的索引，同类型粒子共用相应的质量和相互作用参数。轨迹中的第十个显示点不一定始终对应同一个编号，因为文件内记录的排序可能改变。因此，分析某个粒子走了多远时，需要按编号匹配；比较两类粒子的行为时，需要按类型分组。这种编号与类型的区别，会贯穿后面的分子、长链和网络模型。

一次模拟需要回答三个相互连接的问题：我们保留哪些对象，它们按什么规则相互作用，以及我们怎样观察运动。输入文件把这些选择写成软件能执行的命令。坐标和速度描述某一时刻的状态，势函数描述状态改变时的能量代价，积分方法则据此计算下一小段时间。输出文件记录我们选定的观察量。把这几个角色放在一起，便能看出为什么一段看起来很短的脚本，背后实际上包含了对材料、实验条件和测量方式的一整套假设。

接下来我们在三维周期盒中放入两类粒子，先整理结构，再推进运动并观察能量。整个练习使用同一套粒子参数，把变化分成三个连续阶段：首先暂不接触热浴，让构型和运动交换能量；随后接入规定温度的热浴；最后移除热浴，再看能量怎样演化。相同的对象处在不同环境下，正好帮助我们认识模拟条件如何进入一段真实轨迹。

## 把很大的世界装进一个有边界的盒子

真实液体里的分子数远远超过入门练习能够逐个跟踪的数量。一摩尔物质约含六点零二二乘十的二十三次方个指定对象；“摩尔”只是把极大数量打包计数的单位，像“打”表示十二个。这里没有必要把整杯液体都装进计算机，我们先选一个有限的代表性区域，明确其中粒子的数量和密度。有限体系是否能回答某个问题，要看相关结构有多大、变化需要多长时间。若一条链的空间尺寸已接近盒子边长，它就可能受到自己周期映像的影响，必须把盒子尺寸也纳入比较。

练习中的盒子沿三个方向都从负二十延伸到正二十，因此每条边的长度是四十，而不是二十。盒内有一千五百个第一类粒子和一百个第二类粒子，总数是一千六百。三维体积是三条边长相乘；粒子数除以体积，得到的是数密度，也就是单位体积平均分到多少粒子。这里的数密度相当低，体系最初也不是一块密排固体。标题里的“流体”强调粒子能够相互移动，不意味着我们可以在运行前就给它贴上某种真实液体的密度和相态。

数密度：每单位体积有多少粒子式 1

![数密度：每单位体积有多少粒子](https://ml-biomat.com/static/agent-math/1f1a9874b459f146bf7f5d3e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρₙ | 粒子数密度，脚本 density 输出的则是质量密度 | σ₁₁⁻³ |
| N | 盒内粒子总数 | 1 |
| V | 计算盒体积 | σ₁₁³ |
| Lₓ, Lᵧ, L_{z} | 三个方向的盒长 | σ₁₁ |
| /, × | 除法；相邻的盒长相乘 | 1 |
| = | 等号定义数密度与几何体积。 | 运算符和数值系数无量纲 |

怎样理解先用三条边长计算三维空间的体积，再把粒子数均分到这些体积中。数密度把粒子作为计数对象，不按质量加权。

算一个例子N = 1500 + 100 = 1600，V = 40 × 40 × 40 = 64000，故 ρₙ = 0.025。总质量为 1500 × 1 + 100 × 5 = 2000，因此 LAMMPS 输出的质量密度为 2000 / 64000 = 0.03125，两者不同。

使用条件这里使用正交三维盒与第一类粒子的约化长度尺度。数密度是全盒平均；局部区域可能聚集得更密。

如果给这个小盒子加上硬墙，靠近墙面的粒子和位于内部的粒子就会处在不同环境中。为研究近似均匀的体相，常用周期边界：把盒子在各个方向重复铺开，粒子穿过右边界后在左边重新出现，周围的相互作用按这些重复映像计算。可以把它想成无缝拼接的壁纸，不过拼接对象是三维空间。屏幕上的粒子看似瞬间跳到了另一边，连续运动本身没有中断。后面计算位移时，我们要保留穿越次数，将跨边界的连续路径重新接起来。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s2)

图 2 · 跨越边界的是同一粒子的连续路径。周期图像把坐标映回盒内，画面上的跳变需要与实际位移区分。

周期边界也规定了计算距离的方式。假设一维盒长为十，一个粒子在零点二，另一个在九点八，直接相减得到九点六；但沿边界接缝走，它们最近的距离只有零点四。短程相互作用应使用合适的邻近映像。把截断距离控制在与盒子几何相容的范围内，可以避免把同一个邻居的多个映像重复算作独立近邻。我们目前使用边长四十、全局截断距离四的立方盒，邻域长度与半盒长之间有清楚的余量。

盒子、边界和粒子数都确定后，才能理解一次修改究竟改变了什么。保持粒子数不变而缩小盒子，会提高数密度，让相遇更加频繁；保持密度不变同时增加粒子数和盒子体积，主要改变能够容纳的结构尺度与采样数量。这两种比较对应不同问题。观察更密的流体怎样运动，应采用前一种；检查小盒子的结果是否受有限尺寸影响，应采用后一种。明确比较对象，能避免把“粒子多了”误读成某一种材料机制。

## 吸引和排斥怎样写成一个能量地形

要让粒子运动，首先要告诉计算机粒子彼此靠近时发生什么。势能可以理解为与位置安排有关的能量：把两个吸引的粒子拉开，需要从外界做功；把两个强烈排斥的粒子硬挤在一起，也需要做功。用距离作为横坐标、势能作为纵坐标，我们就得到一条能量曲线。曲线低处对应这对粒子较有利的距离安排，但整个体系同时包含许多邻居、热运动和几何约束，因此一对粒子的最低点不会自动决定所有粒子的排列。

Lennard–Jones 势把短距离排斥和较远距离吸引合在一个简单表达式里。距离比值“σ除以r”没有单位，它的十二次方在距离缩短时增长很快，六次方项则给出吸引部分。十二次幂便于计算，并不是说电子云内部真的装着一个按十二次幂工作的机械弹簧；这种函数是对一类有效相互作用的数学描述。参数ε控制势阱深度，σ控制距离尺度。它们与粒子的质量是不同信息：质量决定给定力产生多大的加速度，势参数决定同样位置安排产生怎样的相互作用。

本例采用的截断 Lennard–Jones 势式 2

![本例采用的截断 Lennard–Jones 势](https://ml-biomat.com/static/agent-math/589524aba471288945c63ef5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U(r) | 这一对粒子的势能 | ε₁₁ |
| r | 粒子中心之间的距离 | σ₁₁ |
| ε | 该对类型的势阱深度 | ε₁₁ |
| σ | 该对类型的势能零点距离尺度 | σ₁₁ |
| r_{c} | 该对相互作用的截断距离，本例均为 4 | σ₁₁ |
| 12, 6 | 将无量纲距离比连续相乘十二次或六次 | 1 |
| <, ≥ | 按距离选择相应分支 | 1 |
| =, /, −, ×, [ ], 4, 0 | 等号定义分段势能；长度相除后无量纲；相减组合排斥与吸引；相邻因子相乘；方括号分组；4为数值系数，0为截断外的能量约定。 | 运算符和数值系数无量纲 |

怎样理解十二次方项在距离缩短时增长快，给出强排斥；减去六次方项形成吸引势阱。因 σ/r 没有单位，乘 ε 后得到能量。

算一个例子对第一类粒子，ε = σ = 1。r = 1 时 U = 4(1 − 1) = 0；r = 2^(1/6) ≈ 1.122462 时，十二次方项为 1/4、六次方项为 1/2，因此 U = −1。

使用条件本例不平移势能，且不加长程尾部修正。因此截断点的势能通常不连续，跨越截断可能影响能量轨迹；两粒子最低点也不等于多粒子体系的唯一邻距。

在距离等于σ时，这个势能为零；最低点位于约一点一二二倍σ，最低能量为负ε。零势能只是所选参考，不表示这个距离处的力一定为零。理解这点可以借助山坡：同样的海拔可能出现在上坡、下坡和水平地面，推动物体的趋势与局部坡度有关。势能曲线也是如此。最低点附近的坡度为零；过于接近时，能量随靠近迅速升高，粒子受到推开的力；在适当的较远距离，吸引使它们趋向靠近。下一讲中的图表会反复用到能量与坡度的区别。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s3)

图 3 · 势能零点位于 σ，最低点位于约 1.122σ；力为零对应曲线的水平切线。曲线由解析LJ公式逐点评估得到。

两类粒子需要三种成对相互作用：第一类与第一类、第二类与第二类，以及两类之间。练习显式给出前两组参数，交叉参数按几何平均生成。几何平均先相乘再开平方，因此两个正数之间不会简单地取算术中点。这里第二类粒子的质量是第一类的五倍，σ是三倍，ε则是一半；这些差别分别作用于惯性、有效大小和吸引尺度。它们共同塑造运动，却不应该被一句“第二类粒子更大，所以更慢”全部替代。比较速度还需要考虑温度、质量以及粒子所处的局部环境。

交叉参数的几何混合规则式 3

![交叉参数的几何混合规则](https://ml-biomat.com/static/agent-math/3042936304a31731d2dde39b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ε₁₁, ε₂₂, ε₁₂ | 同类与异类粒子对的势阱深度 | ε₁₁ |
| σ₁₁, σ₂₂, σ₁₂ | 同类与异类粒子对的长度尺度 | σ₁₁ |
| 11, 22, 12 | 相互作用的两个粒子类型 | 1 |
| √ | 取非负平方根，即求哪个非负数的平方等于根号内的数 | 1 |
| =, × | 等号给出交叉参数；根号内相邻的同类参数先相乘。 | 运算符和数值系数无量纲 |

怎样理解先把两个同类参数相乘，再开平方，得到处于两者之间且单位仍正确的交叉参数。这个规则由 pair_modify mix geometric 明确选择。

算一个例子ε₁₂ = √(1 × 0.5) ≈ 0.707107；σ₁₂ = √(1 × 3) ≈ 1.732051。对应的交叉势最低点在约 1.94416 的距离。

使用条件这是本例的模型选择。其他力场可能用算术平均、专门拟合的异类参数或完全不同的规则，迁移模型时需要同时迁移其混合规则。

真正计算时，还要指定相互作用计算到多远。这里的 LJ 相互作用在距离四之外截断，意味着超过这个范围的该成对项不再纳入力和势能。截断能够降低计算成本，同时改变相对于无限程表达式的模型。选择势能是否平移、是否添加长程尾部修正，也属于模型定义，不能在比较结果时悄悄改变。第一讲保持公开例题的截断设定，第三讲再用能量轨迹讨论它与时间步长共同影响数值行为的方式。

改变间距，观察双粒子的能量和径向力。正的径向力使间距增大。

[Figure: 可调间距的双粒子示意](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s3)

解析势能练习：取 ε = σ = 1。径向力由势能对距离的负斜率计算；它描述相对靠近或远离的趋势。曲线由当前间距直接计算。

## 从局部规则到运动：计算为什么能够推进

坐标告诉我们粒子在哪里，速度告诉我们它正在朝哪里移动以及移动得多快。速度带方向，因此在三维空间通常用沿三个坐标轴的分量表示。力也带方向，它改变速度；质量把力与速度改变的快慢联系起来。即使某一瞬间合力为零，粒子仍然可以凭已有速度继续运动。相反，一个最初速度为零但受到非零合力的粒子，会开始加速。这解释了为什么“没有给初速度”与“之后永远不运动”并不是同一件事。

力怎样改变一个方向上的速度式 4

![力怎样改变一个方向上的速度](https://ml-biomat.com/static/agent-math/8b6ddbbb9024ecb737b7d256.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| aₓ | 沿 x 方向的加速度，即速度每单位时间的变化 | σ₁₁/τ² |
| Fₓ | 沿 x 方向的合力分量 | ε₁₁/σ₁₁ |
| m | 粒子质量 | m₁ |
| τ | 约化时间的基准，下一讲解释其换算 | 时间 |
| =, /, x | 等号表示牛顿第二定律的这个方向分量；分数线以力除以质量；下标x指定空间方向。 | 运算符和数值系数无量纲 |

怎样理解牛顿第二定律把运动响应与所受合力联系起来。相同力作用于较大质量时，单位时间内速度改变较小；另外两个方向分别使用相同关系。

算一个例子在约化单位中，Fₓ = 2、m = 4，则 aₓ = 0.5。若这段短时间内力近似恒定，经过 0.1 个时间单位，x 方向速度增加约 0.05。

使用条件采用经典平移动力学，质量为正。这里的合力是该时刻所有相关相互作用及外加力的矢量和；合力为零时速度可以为非零。

计算机不能连续写下每一个无限短的瞬间，而是用一系列小时间间隔近似这段运动。一个时间步结束时，程序根据当前状态计算下一组位置和速度，然后重新求相互作用，再继续推进。像用许多照片记录一段动作，时间间隔越粗，快速变化越容易被错过；不过积分算法还会利用力的信息预测运动，所以它也不等同于简单地沿两张照片之间画直线。时间步应当足以分辨模型中最快且实际保留的运动，是否合适需要通过相应的数值比较来判断。

步数和时间步长相乘，得到模拟推进的时间。输出间隔则决定保存多少记录，与实际积分间隔是另一回事。每一百步保存一帧，不表示程序只在这一百步的末尾计算一次力；中间的运动仍然按原时间步推进，只是没有把每个瞬间都写到轨迹文件里。保存太稀会失去快速过程的细节，保存太密会增加文件和分析负担。选择输出频率时，应先想清楚要观察的运动有多快、需要怎样的时间分辨率。

步数、模拟时间和记录间隔式 5

![步数、模拟时间和记录间隔](https://ml-biomat.com/static/agent-math/6ecf085e071d0a4986257f68.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| t | 从选定起点经过的模拟时间 | τ |
| n | 经过的积分步数 | 1 |
| Δt | 每次积分推进的时间 | τ |
| q | 相邻记录间的积分步数 | 1 |
| Δt_{out} | 相邻记录对应的时间间隔 | τ |
| Δ | 这里表示一个间隔或增量 | 1 |
| =, ×, out | 等号连接步数与时间；相邻因子相乘；下标out表示输出记录。 | 运算符和数值系数无量纲 |

怎样理解各步的时间间隔相同时，把相同的间隔累加 n 次就是乘法。输出只从这些积分状态中选取一部分保存。

算一个例子本例 Δt = 0.005。第一段 5000 步对应 25，热浴段 15000 步对应 75，最后 10000 步对应 50，总计 150。轨迹每 200 步保存一次，所以帧间隔为 1；热力学量每 100 步保存一次，间隔为 0.5。

使用条件这里使用固定时间步。最小化迭代没有这种动力学时间含义；帧数还受是否保存起点和分段端点影响，应读取实际文件。

当计算对象变多时，逐一检查所有粒子对会变得昂贵。短程相互作用提供了一个机会：只给每个粒子寻找截断范围附近的候选邻居，并在粒子移动后适时更新。[Plimpton 在1995年讨论的并行算法](https://doi.org/10.1006/jcph.1995.1039)比较了按粒子、按力和按空间区域分配计算的办法。把空间分成区域后，不同处理器各自处理附近粒子，并交换边界所需的信息。这段历史帮助我们理解一个核心设计：计算工作围绕相互作用的局部性组织，而不是围绕屏幕上画出的球来组织。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s4)

图 4 · 历史问题是怎样有效计算大量短程相互作用。空间分解把区域分配给处理器，区域边界的邻居信息仍需要共享；区域用于说明空间分解概念。

并行运行带来的细微数值差异也可以从这里理解。同一批作用力以不同顺序相加，有限精度的舍入结果可能略有不同；这些很小的差异随着动力学演化，能够逐渐改变单个粒子的具体路径。比较两个正确的运行时，因而应同时看守恒性质、统计分布和相关物理量。要求长时间以后每个坐标都逐位相同，适合某些严格限定的回归测试，却不是普遍衡量材料统计结果的唯一方法。对初学者来说，先保存版本、输入和随机种子，再学会比较物理统计，是更完整的重现思路。

本讲先把积分理解为“根据状态和力逐步推进时间”。第三讲会展开速度 Verlet 的两次半步更新，解释它如何把位置、速度和新旧作用力连接起来。这样安排的目的是让第一次操作时已经知道每类量在做什么，而在需要检查能量误差时，再进一步理解具体算法。知识之间的联系很直接：势函数给出力，质量决定响应，积分器推进状态，输出程序保存观察；缺少任何一环，都无法从一张初始结构图得到具有时间含义的轨迹。

## 结构最小化与动力学回答不同的问题

随机摆放粒子很方便，却可能把某些粒子放得过近。LJ 势在短距离急剧升高，这样的局部重叠会产生很大的排斥力。若立即用一个普通时间步推进，粒子可能在一步里移动得过远，让初始摆放问题演变为数值问题。能量最小化先调整坐标，沿降低势能的方向缓解不合理的近接触。它像把杂乱塞进抽屉的物件重新摆好，为后续运动提供起点；这一步本身并不描述现实中物件用多少秒完成整理。

最小化中的迭代次数，记录的是优化算法尝试了多少次坐标更新；动力学中的步数，记录的则是时间积分的推进。它们都可能在日志里以一列数字出现，却不应接成一条统一的物理时间轴。在最小化过程中，势能通常向较低处移动，最后可能因为力足够小、能量变化足够小，或者达到允许的迭代次数而停止。读日志时要看停止原因。如果因为迭代上限停止，就继续检查剩余最大力和近接触，而不是把任何停止都称为已经找到稳定平衡。

更深的区别在于，有限温度下的体系会不断探索许多构型。一个势能最低的局部结构，未必是该温度下最常见的整体状态，因为能够实现某类状态的构型数也参与决定它的出现概率。想象两个区域，一个只有一把很舒适的椅子，另一个有许多稍普通的座位；问“哪把椅子最低”与问“人群经常出现在什么区域”不同。最小化帮助我们整理起点，热运动与采样则帮助我们理解有限温度下的分布。后面研究链构象、膜和自由能时，这种区别会更加明显。

随后进行的 NVE 计算保留粒子数 N、盒子体积 V，并在所选保守模型与数值精度下追踪能量 E 的变化。势能和动能可以相互转换。例如一对处于吸引区的粒子开始靠近，势能降低，同时运动速度可能增加。只看动能曲线上升，容易误以为程序无缘无故“加热”；把势能同时画出来，就能看见能量来自哪里。截断方式、时间步长和舍入会影响数值能量轨迹，第三讲会用对照运行把这些影响分开讨论。

动能与模型总能量式 6

![动能与模型总能量](https://ml-biomat.com/static/agent-math/2b0d19028fd552c116fc074f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| K | 全体系平移动能 | ε₁₁ |
| N, i | 粒子总数及逐粒子编号 | 1 |
| mᵢ | 第 i 个粒子的质量 | m₁ |
| vᵢ | 第 i 个粒子的三维速度矢量 | σ₁₁/τ |
| \|vᵢ\|² | 速度三个分量分别平方再相加 | σ₁₁²/τ² |
| Σ | 把 i = 1 至 N 的各粒子贡献相加 | 1 |
| U, E | 全体系势能与总能量 | ε₁₁ |
| =, +, ×, 1/2 | 等号定义能量；加号合并动能与势能；相邻因子相乘；1/2为动能的数值系数。 | 运算符和数值系数无量纲 |

怎样理解每个粒子因运动具有动能，按质量和速度平方计算。把所有粒子动能相加，再加上全体系相互作用势能，得到这个模型的机械能。

算一个例子两个质量均为 1 的粒子，速率分别为 1 和 2，则 K = 0.5 × 1² + 0.5 × 2² = 2.5。若全体系 U = −1，则 E = 1.5；除以粒子数后，三项分别为 1.25、−0.5、0.75。

使用条件本例只含平移自由度。NVE 能量检查要使用一致归一化，并考虑截断与积分误差；有热浴时，还发生与外界的能量交换。

热浴则使模型能够与一个规定温度的环境交换能量。Langevin 恒温方法用与速度有关的阻力和随机扰动力表示这种接触：阻力消耗动能，随机扰动补充热运动，两者的强度按照温度与阻尼参数相联系。它不是把每个粒子的速度强制固定成同一个值，温度曲线也会围绕目标值波动。对本练习，Langevin 命令修改作用力，另一个 NVE 积分命令负责推进位置和速度；“NVE”出现在这个积分器的名字里，并不意味着加上热浴之后整个体系仍然隔绝能量交换。

因此，读取分阶段结果时，要先辨认横轴和环境。最小化图的横轴是优化迭代；NVE 图的横轴是积分时间，重点是能量交换和数值守恒；NVT 图允许热浴交换能量，重点是温度分布以及结构、能量统计是否在持续变化。把三段曲线放在一起有助于理解完整操作，但每段的判断依据仍然来自它各自回答的问题。下面的实际结果按这些阶段分别显示，避免把坐标整理、孤立演化和接触热浴混成同一段实验。

## 读懂完整输入，而后运行它

LAMMPS 的输入文件是一份按顺序执行的纯文本说明。命令行可以看成一个接收具体任务的入口：输入程序名和参数，程序读取文件、计算，并把信息写回屏幕或磁盘。这里用 lmp 表示可执行程序，用 -in 后面的名字指定输入文件。文件名是相对于当前工作目录寻找的，所以把输入文件放在一个明确的练习目录里再运行，会使后续分析更容易对应。程序版本先由帮助信息或日志首行确认，本课程的输入与实际结果使用同一固定版本进行比较。

### 确认程序并运行本例

```
lmp -help
lmp -in initial.lmp
```

在含 initial.lmp 的练习目录运行。第一行显示版本和可用命令，第二行读取完整输入；计算随后生成日志、thermo.dat、轨迹及重启文件。

完整脚本的开头定义单位、空间维数、粒子所携带的属性和边界方式。units lj 使用一套约化尺度：我们选定质量、长度和能量的基准，然后用这些基准表示相应数值。dimension 3 指定三维运动；atom_style atomic 表明这些粒子没有显式键、电荷或分子拓扑；boundary p p p 则把三个方向都设为周期。把默认选项也清楚写出来，有助于读者看见模型假设，也让后来修改体系时能够找到应该改变的位置。

region 描述一个几何区域，create_box 根据区域建立计算盒并预留类型，create_atoms 再向其中加入粒子。这里两次随机创建分别使用固定种子，方便重新生成同一套初始化过程。种子是伪随机数生成器的起点，不是温度，也不是某种物理性质。初始位置中设置最小间距可以减少过近接触，但两类粒子的有效大小不同，几何上的一个统一间距仍然需要结合势能与最小化结果来检查。读输入时应把几何条件和力场尺度一起考虑。

接下来的 mass、pair_style 和 pair_coeff 把数字与物理角色对应起来。写下一个势函数名称并不等于完成力场定义：哪些类型存在、各对类型的参数怎样取、交叉参数如何生成、相互作用在哪截断，必须共同明确。thermo 与 thermo_style 决定屏幕和日志记录哪些量、多久写一次；dump 决定轨迹记录的粒子属性和频率。它们通常改变的是观察方式。若修改保存频率就得到明显不同的物理结果，应继续寻找是否同时改动了积分、随机过程或其他相关设置。

### 两类粒子的完整输入

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

保留公开原例的粒子数、盒子、两类质量、成对参数和位置种子，增加分阶段数值输出与重启文件。动力学依次推进 25、75、50 个约化时间单位；中段接触 Langevin 热浴。

运行过程中，读者应能找到起始粒子数、最小化停止原因、动力学各阶段的输出表和结束信息。日志记录的是计算发生了什么，轨迹记录的是哪些粒子在哪里，两者需要共同保存。输入中的相同名字可能会在重复运行时覆盖旧文件，所以用于参数比较的各次运行应各自保留目录和输入副本。给输出加上能说明物理条件的名字，比事后凭记忆猜测曲线更可靠。这里先掌握一次完整运行；第二讲将把多个文件之间的关系画成明确的流程。

如果程序指出某条命令不认识，首先核对版本和输入拼写；如果文件找不到，核对工作目录和相对路径；如果出现粒子丢失或极大能量，检查初始几何、参数单位、积分时间步与邻居更新。这样的诊断顺序分别对应语法、文件组织和物理数值三个层次。它把报错变成可定位的问题，也避免在几何重叠尚未处理时，就盲目增加运行步数。每次修正应能够说明改的是哪一层，以及重新运行后应该观察哪个量来判断影响。

## 把轨迹和曲线放在一起看

轨迹提供空间信息：粒子是否分散、是否形成暂时团簇、两种类型是否处在相似环境、周期边界有没有把一个团簇在图上切成两半。能量曲线则提供整体变化的信息。只看动画，运动顺滑也可能掩盖持续能量漂移；只看一个平均值，又可能遗漏结构在缓慢改变。把同一时间段的轨迹和统计量联系起来，才能把“看起来在运动”推进为对具体模型的解释。下面的轨迹来自本讲输入的实际运行，颜色区分粒子类型，图例中的显示大小与势参数分别说明。

### 实际运行的双粒子类型轨迹

实际坐标按类型着色。播放时显示模拟时间和所在阶段，跨边界位置按周期盒显示。

LAMMPS 30 Sep 2026 update 1；三维周期盒，1500 个类型 1 粒子与 100 个类型 2 粒子；约化单位，时间步 0.005，总时长 150。物理输入沿用 Gravelle 等人的双组分 Lennard–Jones 教程，增加 NVE 对照及数值记录。

[下载参考数据与完整输入（ZIP） 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

读取能量轴时，必须先知道数值是整个体系的总量，还是除以粒子数后的平均量。在 LJ 单位体系中，LAMMPS 的默认热力学输出会把某些随粒子数增加的广延量按粒子数归一化，势能和动能属于这一类；温度和压力则按各自定义输出。如果整个体系的势能为负八百，而粒子数为一千六百，每粒子势能就是负零点五。两种写法描述同一状态，但如果把一条总能量曲线与一条每粒子能量曲线直接相加，结果就失去物理意义。

温度也需要从运动中定义。平移自由度可以理解为描述独立运动所需的速度分量数；三维中每个自由粒子通常提供三个分量。整体平移、刚性约束或其他被去掉的运动会改变计数。当前模型没有分子内部约束，默认温度计算对整体平移扣除三个自由度，因此一千六百个粒子的温度分母使用四千七百九十七，而不是四千八百。对大体系这个差异很小，明确它仍然有价值，因为水、刚体或很小的粒子组会使自由度处理变得更明显。

本例输入明确使用 thermo_modify norm no，让日志中的 pe、ke、etotal 保留全体系总量，再由记录变量各自除以粒子数，把每粒子能量写入 thermo.dat。因此日志能量与本页图的纵轴相差粒子数这个因子，而不是出现了两套不同物理结果。先读设置再读列名，能够避免自动归一化与手动除法叠加。

从运动定义瞬时温度式 7

![从运动定义瞬时温度](https://ml-biomat.com/static/agent-math/3727bd68d879c192724c8c0b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| T | 该温度计算所定义的瞬时温度 | ε₁₁/k_B |
| K | 纳入温度计算的平移动能总和 | ε₁₁ |
| f | 参与统计的独立速度自由度数 | 1 |
| k_{B} | 玻尔兹曼常数，连接温度和能量；LJ 约化单位中数值为 1 | 能量/温度 |
| N | 粒子数 | 1 |
| 3N − 3 | 三维速度分量数扣除默认的三个整体平移自由度 | 1 |
| =, /, ×, −, 2, 3 | 等号定义温度与自由度；分数线相除；相邻因子相乘；减号扣除整体平移；2来自每个二次型自由度的平均动能，3对应三个空间方向。 | 运算符和数值系数无量纲 |

怎样理解经典平衡下，每个二次型速度自由度的平均动能为 k_BT/2。反过来用当前动能构造温度估计量，得到这个关系。瞬时动能会变，温度因而会波动。

算一个例子N = 1600 时，f = 4797。若 T = 1、k_B = 1，则 K = 4797/2 = 2398.5，每粒子动能为 1.4990625。直接把每粒子动能代入 K 的位置，会少乘 1600。

使用条件这是无内部约束的三维体系中 LAMMPS 默认温度计算的自由度约定。刚性约束、流速偏置、不同粒子组及自定义温度计算需要相应调整。

### 势能、动能与总能量怎样交换

同一输入产生的每粒子势能、动能、总能量和温度；阶段分界为 t = 25 与 t = 100，终点为 t = 150。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/#zh-s7)

全部实际记录，能量除以粒子数。阴影为 t* = 25–100 的 Langevin 热浴阶段，前后为 NVE；温度虚线只画在启用热浴的区间。

### 从同一次运行重现能量与坐标图

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

把程序与 thermo.dat、trajectory.lammpstrj 放在同一练习目录，运行 python analyze_records.py --language zh 或 --language en。它读取原始数值，生成温度、每粒子能量及连续坐标图；第二讲逐段讲解读取方法。

NVE 段的势能和动能常常一升一降，显示构型与运动之间的能量转换；总能量应结合时间步、截断和输出精度来检查。NVT 段的温度向设定范围靠拢，并在其附近产生热涨落。我们关心的是合适时间段内的分布和平均，而不是要求每一行输出都等于目标数字。若前后两段的平均势能仍然明显不同，就继续观察结构和能量是否在调整，并把初始过渡与之后用于统计的区间分开。一个平坦的温度均值还不能替代对慢结构变化的检查。

一次平均的计算方法很简单：把选定区间的各次读数相加，再除以读数个数。但相邻记录往往彼此相关，保存一千行并不一定等于得到一千次独立观察。像每隔一秒观察同一个尚未改变的姿势，记录数增加了，新的信息却没有按同样速度增加。本讲先学会说明平均取自哪一阶段、哪一段时间；第十五讲再用分块、相关时间和独立重复，判断误差条怎样对应真正获得的信息量。

## 用一次小改变，建立模拟比较的习惯

第一次练习之后，最有帮助的下一步是只改变一个能够说清楚的条件。例如保持粒子数、盒子和势参数不变，把热浴目标温度调高，再比较速度分布、能量和团簇外观。提高温度意味着更大的热运动尺度，但对具体结构的影响要由势能尺度、密度和充分采样共同决定。不要在同一次比较里又改变盒子、粒子数和相互作用强度，否则即使曲线变化很大，也很难把原因与某一个选择联系起来。

也可以只改变第二类粒子的质量，保持势参数和温度相同。质量较大的粒子在相同动能尺度下通常具有较小的速度尺度，所以动力学过程可能变慢；但经典平衡分布中，固定位置的势能函数没有因此改变。这个比较帮助我们区分“运动快慢”和“哪些构型受到偏好”。如果观察时间很短，较慢体系可能尚未探索到与较快体系相同的区域，有限采样会进一步影响看到的分布。这样一个看似简单的参数练习，已经把动力学与平衡统计联系起来。

做任何比较，都要把图中的单位和归一化保持一致。若改了粒子数，检查能量是总量还是每粒子量；若改了盒子，检查密度是否保持；若改了时间步，比较相同物理时长，而不是相同步数。随机种子则提供另一种变化：模型参数不变，但初始位置或随机热浴历史改变。多个种子的结果可以显示观察量有多大运行间波动，帮助区分一个持续存在的趋势与偶然的轨迹特征。

对于生物材料，这一讲的价值在于建立一套能够扩展的观察语言。以后把粒子连成高分子链，位置关系会多出连接约束；加入水和离子，会出现电荷、分子几何和长程相互作用；构建交联网络，会开始关心连接是否形成贯通结构。无论模型多复杂，仍然需要说明对象、相互作用、边界、时间推进和观察量。基础案例把这些要素分别摆清楚，之后增加复杂性时，我们就知道新加的一项具体改变了什么。

可以用三个问题检查自己是否真正读懂了第一次模拟：最小化期间为什么不把迭代次数换成秒；粒子跨过周期边界时，为什么动画中的跳跃不等于真实瞬移；加入热浴后，为什么体系总能量会改变而温度仍然只是围绕目标波动。回答这些问题需要把计算步骤与物理含义联系起来，光记住命令名称并不够。你可以先用自己的话写出理由，再回到对应的图和公式核对。下面给出的解释也适合在重复运行前作为一次简短的理解检查。

查看解释

最小化沿降低势能的方向寻找坐标，不按所选动力学方程推进真实时间；周期图像把同一条连续路径重新映射回盒子，显示坐标发生跳变但连续坐标可以接回；热浴通过阻力与随机力交换能量，温度是许多自由度动能的统计量，因此瞬时值仍有涨落。判断一次比较时，要对照对应阶段、模型条件与采样区间。

下一讲会从这些实际文件出发，把输入、日志、轨迹、结构和重启文件连接起来。读者将练习在文件中定位一次运行的条件，选择需要保存的粒子属性，并用一段完整的分析程序把记录变成图。到了那时，“让一盒粒子动起来”就会进一步变成“能够追溯、继续和比较一次模拟”。这一步对后来研究一条链、一片膜或一个网络都同样适用，因为科学解释始终需要与产生它的数据保持对应。

## 延伸阅读与开放资料

- [A Set of Tutorials for the LAMMPS Simulation Package — Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  三维双粒子类型、最小化及 NVE/Langevin 流程与公开输入。

  重新组织双语解释，增加解析图、交互、阶段统计与重启输出；运行版本 30Sep2026 update1。
- [LAMMPS stable manual: Lennard-Jones, units, temperature and output normalization](https://docs.lammps.org/stable/pair_lj.html) · LAMMPS developers · Official technical documentation; software source is GPL-2.0, independently drawn figures here

  公式、默认混合规则、温度自由度及命令含义。

  自行推导算例与绘图，没有转载手册图片。
- [Fast Parallel Algorithms for Short-Range Molecular Dynamics](https://doi.org/10.1006/jcph.1995.1039) · Steve Plimpton (1995) · Cited scientific paper; no copied figures or article text

  空间分解科学史。

  绘制新的区域和邻居交换示意图。
