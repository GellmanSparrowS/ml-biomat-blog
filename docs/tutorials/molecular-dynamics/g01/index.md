# 分子模拟能告诉我们什么

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g01/
Language: zh-CN

从一盒水出发，理解模型怎样生成运动，运动怎样形成可测量的密度，以及一条曲线怎样回答一个具体的科学问题。

## 从一杯水开始，把问题缩小到分子能回答的范围

把一颗方糖放进水里，最初可以看见清楚的棱角，后来糖块逐渐缩小，杯底与杯口之间也不再有一道甜味的边界。生活经验让我们知道糖能溶解，却没有直接告诉我们：水分子怎样靠近糖的表面，哪些部位更容易被水包围，离开晶体的糖分子又怎样移动。类似的问题也藏在隐形眼镜的保水能力、药物在溶液中的分散，以及蛋白质能否维持形状之中。分子模拟把其中一小块空间变成可计算的模型，记录每个粒子在一段时间内的位置，再把这些位置整理成能够讨论的数量关系。

本讲先研究比糖水更简单的纯水。目标是认识一条完整的推理链：我们选定怎样的水分子模型，怎样让它们运动，怎样从不断变化的分子排列计算密度，以及这个密度对应什么条件。水在这里还有一个实际用途：后续的蛋白质、核酸、糖链和聚合物常常浸在水里。理解溶剂怎样被表示，就能看懂这些体系中相当大的一部分原子，也能发现“蛋白质没有变，结果却变了”的原因可能来自水模型、盐浓度或控制条件。

想象一段从高处拍摄的操场视频。视频保留了许多人的位置，但要回答“哪条出口更容易拥堵”，还需要定义出口区域、统计经过的人数，并说明观察了多久。分子轨迹也有这样的结构：画面提供位置，研究问题决定测量方式。密度关心一定体积内有多少质量；扩散关心粒子经过一段时间后离出发点多远；水化关心某个分子附近的水怎样分布。这些问题可以使用同一段轨迹，计算出的量却各不相同。读图之前先说清要测什么，会让后面的命令有明确的用途。

这次例题的系统是一盒采用 SPC/E 模型的水。初始盒子每条边长为 3 nm，水分子的数目由建盒步骤实际确定；控温目标为 300 K，控压目标为 1 bar。nm 是纳米，1 nm 等于十亿分之一米；K 是开尔文，300 K 约为 26.85 ℃；bar 是压力单位，1 bar 等于十万帕。我们将查看这个小盒子在准备、平衡和观察阶段的状态，把温度、体积、密度的曲线放在一起读。它们的联系比一个孤立的最终数字更能说明模拟在做什么。

真实的一滴水包含极多分子，计算机里的盒子要小得多。因此，每个问题都带着一个观察尺度。这里的短轨迹适合学习文件、运动、密度涨落与分析方法；要研究结冰、蒸发、长时间化学降解或稀有结构转变，就要重新选择模型、边界和采样时间。这样的选择与显微镜调倍率很相似：倍率决定能分辨什么，视野决定能统计多少对象。模型和时间窗口同样需要与目标现象配合。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/#zh-s1)

图 1 · 从模型、轨迹到测量与解释的示意流程，各步骤分别回答不同问题。

## 从“看不见的运动”到可以检验的液体模型

液体看上去连续而平静，分子尺度上的运动却没有停下来。若只画一张分子排列图，我们很难判断哪些邻居会持续相伴，哪些邻居很快交换。早期分子动力学的一个关键改变，是把这样的图变成按时间连接的许多张图。计算机根据粒子之间的相互作用推进位置，于是研究者能够提出一个更具体的问题：某种相互作用规则，能否同时解释液体的排列与运动？这个问题至今仍然贯穿力场的选择和验证。

1964 年，Aneesur Rahman 研究了由 864 个粒子构成的液氩模型。氩是稀有气体元素，一个粒子可以对应一个原子，不需要先处理复杂的化学键。研究使用连续的 Lennard–Jones 相互作用，并把粒子的运动与结构统计联系起来，包括相邻原子在不同距离处出现的倾向以及原子的自扩散。这个例子的重要之处在于，它把“计算出了许多位置”推进到了“把位置整理成实验可以比较的量”。原论文的研究对象、温度和密度都有具体设定，模型的意义也在这些条件中建立。[Rahman，1964](https://doi.org/10.1103/PhysRev.136.A405)

氩原子的简洁帮助我们抓住方法，水则提出了新的要求。一个水分子有一个氧原子和两个氢原子，原子之间的电子分布并不均匀，因此分子不同部位对周围电荷的作用不同。水分子也有方向：把两个水分子转一转，即使它们的氧原子间距相同，相互作用仍可能改变。模拟水需要同时处理位置与取向，不能只给每个分子画一个没有方向的圆点，再期待它表现出相同的氢键网络。

SPC/E 水模型与这一问题有关。1987 年，Berendsen、Grigera 和 Straatsma 在讨论有效成对势时，强调了极化相关能量在模型与热力学量比较中的作用，并在 SPC 模型基础上形成 SPC/E。这里的“有效”是一个值得理解的词：计算没有逐个追踪电子怎样响应环境，而是让经过选择的固定参数包含一部分平均效应。这样一来，计算可以覆盖更多分子与更长时间；代价也很具体，电荷不会随着每一帧环境即时重新分布。[Berendsen 等，1987](https://doi.org/10.1021/j100308a038)

从液氩到水，这些模型的发展由具体物理问题串联起来：先看粒子怎样碰撞与被吸引，再考虑有方向的分子相互作用，进一步考虑周围环境如何改变分子的电性。我们在使用一个成熟模型时，也应沿着同样的顺序提问。它把什么当成粒子？给了粒子哪些性质？哪些变化交给运动方程，哪些变化已经被固定在参数里？这些问题会在后面解释蛋白质电荷、糖链构象和聚合物水化时反复出现。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/#zh-s2)

图 2 · 液氩模型把原子运动连接到结构与扩散；三位点水模型进一步引入分子取向和电荷分布。

## 一盒“水”在计算机里究竟由什么组成

可以把分子模型的准备分成三张互相配合的纸。第一张记录“此刻在哪里”，也就是原子坐标；第二张记录“它是什么、怎样相互作用”，也就是拓扑与力场；第三张记录“这次怎样观察”，也就是运行参数。坐标文件可以告诉我们氧原子位于盒子中的某个位置，却不能单凭这个位置决定它的电荷。参数文件可以指定 300 K，却不会自动补出缺失的水分子。只有三者一致，软件才知道下一步应如何计算。

“拓扑”在这里主要描述分子身份和连接关系，例如哪些原子属于同一个水分子、哪些原子相连，以及使用哪组相互作用参数。它与地图上的道路连接有些相似：道路怎样连通，与今天每辆车停在哪里是两类信息。水的坐标可以不断变化，分子内部的连接规则仍保持不变。本例使用固定连接关系的经典模型，适合观察分子平移、转动和相互排列；若研究水分解或质子在水链中转移，连接关系与电子状态就进入了研究问题，需要相应的反应性或电子结构方法。

SPC/E 用三个相互作用位点表示一个水分子，分别放在氧和两个氢的位置上。每个位点有质量和部分电荷，氧位点还承担模型中的 Lennard–Jones 非键相互作用。部分电荷不是把一个水分子变成了带净电荷的离子，而是在整体电中性的分子中表示电荷分布不均匀。两个正的氢电荷与一个负的氧电荷相加为零。这种分布使水可以与带电或极性的分子基团发生有方向的作用，帮助我们理解盐为什么能被水包围，以及亲水表面为什么会形成有结构的水层。

在这次动力学设置中，水分子的内部几何通过约束保持为刚性，分子仍然可以在空间中移动和转动。可以把它想成一个保持夹角的小三脚架：整个架子可以翻转，三条固定几何关系不会像橡皮筋一样自由振动。刚性处理移除了很快的内部振动，允许我们把计算时间更多用于关注的分子间运动。它也决定了结果的解释方式：动力学轨迹中的水分子没有独立的伸缩振动，不能拿这段轨迹直接重现完整的真实水分子振动光谱。初始最小化则先采用配套的柔性键角定义松弛几何，再进入刚性水的动力学阶段；这一步不作为水的真实时间演化来解释。

我们还需要区分“用什么坐标搭起最初的盒子”和“盒子里采用什么水模型”。GROMACS 的 spc216.gro 提供可用于三位点水模型的起始坐标，而拓扑中的 spce.itp 指定本例的 SPC/E 参数。文件名中的 spc 不会把后来选择的拓扑偷偷改成 SPC。类似地，一张房屋平面图可以为不同用途提供初始布置，房间的实际功能仍由后面的设计决定。建盒以后进行最小化与平衡，就是让这一初始排列适应本次参数和控制条件。

盒子边界使用周期性处理。一个水分子从右侧离开时，可以在左侧找到它的周期映像；计算相互作用时，也会按周期规则处理盒子外的邻居。把相同图案铺满地面的瓷砖能够帮助理解这种空间重复，但每块瓷砖并不是一个独立的新样本。所有映像都来自同一个基本盒子，运动彼此对应。这样可以研究没有自由表面的体相水，同时也引入有限盒子与重复结构的影响。盒子尺寸、截断距离和长程静电处理要共同设定，后面会逐步解释。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/#zh-s3)

图 3 · SPC/E 部分电荷来自 GROMACS 2026.4 的 spce.itp。电荷以元电荷 e 为单位；图中的小球不是电子云的真实轮廓。周期图为二维截面，实际水盒在三个空间方向周期重复。

## 为什么位置可以一步一步算出来

要预测下一瞬间的位置，我们至少需要知道现在的位置、运动速度，以及受到的力。推一辆空购物车和推一辆满载购物车时，同样的推力带来的速度变化不同；质量越大，在相同力下加速度越小。分子动力学采用的牛顿运动关系也遵循这个结构，只是物体换成了模型里的原子或粒子，力来自所选的相互作用规则。把这层关系弄清楚，比一开始记住大量参数名称更有帮助。

同样的力怎样改变不同质量粒子的运动式 1

![同样的力怎样改变不同质量粒子的运动](https://ml-biomat.com/static/agent-math/853ef63f52b532f6977494a6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i | 粒子的编号，用来区分不同粒子，不是乘号 | 无量纲 |
| Fᵢ | 作用于第 i 个粒子的合力向量，粗体表示带方向 | 牛顿 N = kg·m·s⁻² |
| mᵢ | 第 i 个粒子的质量 | 千克 kg |
| aᵢ | 第 i 个粒子的加速度向量，即速度随时间的变化率 | 米每二次方秒 m·s⁻² |
| =, × | 等号表示两侧相等；质量乘以加速度，分别作用于三个方向分量 | 运算符无单位 |

怎样理解质量衡量改变运动的惯性。在相同合力下，质量越大，加速度越小；逐个粒子计算这一关系，就能把相互作用连接到运动变化。

算一个例子设一个示意粒子的质量为 3.0×10⁻²⁶ kg，沿 x 方向受力 6.0×10⁻¹² N，则该方向加速度为力除以质量，即 2.0×10¹⁴ m·s⁻²。分子尺度的质量很小，所以加速度数值可以很大；这里的数字是算例，不是水盒的测量结果。

使用条件本例采用经典粒子运动；受约束时合力还包含保持几何关系所需的约束作用。控温或控压阶段按相应算法改变运动或盒子，因此不同阶段的守恒性质需要分别解释。

式子中的向量表示一个既有大小又有方向的量。沿着桌面向东推与向北推，力的大小相同，带来的位置变化却不同；在三维盒子中，我们需要用三个分量描述这种区别。加速度表示速度随时间的变化，速度本身则表示位置随时间的变化。软件在每个很短的时间间隔内计算力，再按积分算法更新这些量。这里“积分”可以先理解为把许多很小的运动变化连接起来，而不必先掌握整套微积分计算。

力从哪里来？模型先规定不同排列对应怎样的势能。把两块同极磁铁推近会越来越费力，可以帮助理解“某些排列能量较高，改变排列会产生力”的关系。分子力场中的排斥、色散和静电作用各有数学表达，它们共同决定局部位置变化会让能量怎样改变。软件依据这种变化计算作用力，再推进运动。势能较低的位置通常较容易被访问，但温度带来的运动使体系持续离开某些低能排列，因此热平衡中的分子并不会全部停在一个最低点。

时间步就是每次推进的物理时间间隔。本例的动力学时间步为 0.002 ps，也就是 2 fs；1 ps 等于万亿分之一秒，1 fs 等于千万亿分之一秒。它与电脑花了多久执行程序是不同概念。计算机运行十分钟，可能模拟的是几十或几百皮秒，具体取决于体系大小、硬件和设置。轨迹中的横坐标应来自模拟的物理时间，不能把操作系统的耗时填进分子运动图。

把计算步数换成物理时间式 2

![把计算步数换成物理时间](https://ml-biomat.com/static/agent-math/133b8e3a1a3c1adeaeaa8352.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| tₛᵢₘ | 这段运行覆盖的物理时长 | 皮秒 ps |
| Nₛₜₑₚ | 积分步数，是非负整数 | 无量纲 |
| Δt | 一个积分步推进的时间；Δ表示一段变化量 | 皮秒 ps |
| =, × | 步数乘以每步时长，得到总时长 | 运算符无单位 |

怎样理解每步时间相同，重复推进 N 次相当于把同一时间间隔相加 N 次，因此可以直接相乘。

算一个例子NVT 设置 10,000 步，每步 0.002 ps，总时长为 20 ps。100 ps 的 NVE 在 2 fs 步长下需要 50,000 步，在 1 fs 步长下需要 100,000 步。

使用条件适用于固定时间步，不包含初始时间偏移，也不表示电脑耗时。不同阶段衔接时，应从记录读取实际时间轴。

把时间步放大，意味着用更少的更新去覆盖同一段物理时间，看起来很省事；但若粒子在两次计算之间已经跨过重要的受力变化，近似就会变差。这个问题像用很稀疏的照片重建快速挥动的手：照片之间发生了什么，可能已经无法可靠补回。约束快速振动有助于选用 2 fs 时间步，实际可用的步长还与力场、温度、约束精度和数值算法有关。第四讲会用相同初态下的能量变化检查这种选择，本讲先记住：时间步需要物理依据与数值检查共同支持。

程序也不会把每一步都保存成一幅图。更新运动可以很频繁，写出坐标则可以较稀疏，以免生成过大的文件。假设每 500 步保存一帧，2 fs 的步长对应每 1 ps 保存一帧。这些帧适合观察较慢的位移或结构变化，却会漏掉帧间发生的更快细节。因此，“模拟运行了多久”“每隔多久计算一步”“每隔多久保存一帧”是三个分别设置的量。之后读到任何动画或时间曲线，都应把这三个量区分清楚。

## 密度怎样把许多分子的运动连到日常测量

密度是一个适合作为起点的量。拿两个同样大小的量杯，分别装水和食用油，称得的质量不同，就说明相同体积容纳的质量不同。在模拟中，我们同样可以把总质量除以盒子体积。总质量由分子数和每个分子的质量决定；体积则来自盒子的三条边，采用控压算法时还会随时间变化。即使我们没有给每个水分子安排一个“应当具有的密度”，大量分子在相互作用与外部条件下共同形成的排列，也会产生一个可测的密度。

由水分子数和盒子尺寸计算密度式 3

![由水分子数和盒子尺寸计算密度](https://ml-biomat.com/static/agent-math/ebf7b509d88b138b00b1accd.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρ | 质量密度，希腊字母 rho | kg·m⁻³ |
| m | 盒中水的总质量 | kg |
| V | 盒子体积 | m³ |
| Nw | 水分子个数 | 无量纲 |
| Mw | 水的摩尔质量，算例取 0.01801528 | kg·mol⁻¹ |
| NA | 阿伏伽德罗常数，6.02214076×10²³，表示每摩尔的粒子数 | mol⁻¹ |
| L | 立方盒子的边长 | m；输入 nm 时先乘以 10⁻⁹ |
| /, ³, =, × | 分数线是除法；三次方表示三个边长相乘；等号表示两种写法相等；相邻符号表示乘法 | 运算符无单位 |

怎样理解摩尔质量除以每摩尔的分子数得到单分子质量，乘以实际分子数得到总质量，再除以体积。立方体体积是边长的三次方。

算一个例子几何算例：900 个水分子放在边长 3.000 nm 的立方体中，密度约为 997.17 kg·m⁻³。若边长增大 10%，体积变为原来的 1.1³ = 1.331 倍，密度变为原来的约 0.7513 倍。900 是算例的指定数目；实际水盒数目由建盒输出确认。

使用条件这里假定纯水与立方盒子。混合物应逐种累加质量；非立方盒子应使用完整盒矢量确定体积。精确复核模拟密度时应采用拓扑中的实际原子质量。

这条公式把几种尺度连了起来。化学里常用“摩尔”来数极多的粒子，好比用“打”表示十二个物品，只是一个摩尔包含的个数大得多。水的摩尔质量约为 18.01528 g/mol，意思是一摩尔水分子的质量约为 18.01528 g。先除以阿伏伽德罗常数，就得到一个水分子的质量；再乘以盒中的水分子数，得到总质量。纳米体积转换成立方米时，要把长度换算连续乘三次，不能只换一次单位。单位逐步跟随计算，许多看似神秘的换算就会变得可检查。

在控温控压阶段，分子数保持不变，盒子体积允许变化。盒子收缩时，同样多的水挤在更小空间中，密度升高；盒子膨胀时，密度降低。这种变化不是水分子忽然变重或变轻，而是分母改变。下方交互固定水分子数，让你改变立方盒子的边长，查看密度如何变化。它计算的是质量与体积的几何关系，并不推进分子运动，所以适合先建立直觉，再与真实轨迹中的曲线比较。

几何算例：由水分子数、摩尔质量和立方盒体积计算质量密度。

[Figure: 立方盒子几何算例及密度读数](https://ml-biomat.com/tutorials/molecular-dynamics/g01/#zh-s5)

调节分子数与盒边长，观察质量和体积如何共同决定密度。

温度与压力也需要按统计量理解。单个原子没有一个像温度计读数那样独立而稳定的“自身温度”；系统温度通过许多运动自由度的动能联系到热力学描述。压力则涉及粒子运动及相互作用对体积的响应。在纳米尺度的小盒子中，瞬时压力可以有很大的涨落，控压目标为 1 bar 并不意味着每个保存时刻都显示 1.000 bar。我们更关心适当观察窗口内的分布、平均水平和是否仍有持续漂移。

本例先最小化，减轻初始结构中不合适的近距离接触；接着在固定体积下控温，让运动适应目标温度；随后加入控压，让盒子尺寸调整。习惯上把固定粒子数、体积、温度的条件写作 NVT，把固定粒子数、压力、温度的条件写作 NPT。这里的“固定温度或压力”指的是所采样统计条件与控制目标，瞬时测量仍会涨落。另一个 NVE 阶段固定粒子数和体积，并撤去温控与压控，用来观察近似孤立动力学的总能量行为。不同阶段要回答的问题不同，不能把 NVE 中固定不变的盒子密度当成控压已经收敛的证据。

从曲线中挑出一个最接近实验值的时刻，很容易得到一个漂亮数字，但这会丢掉其他时刻的信息。更合适的做法是先查看完整记录，再明确选取哪一段做描述统计，并报告这一段中的波动。在这次入门分析中，我们把 NPT 记录的后半段作为清楚、可重复的观察窗口，比较原始曲线、累积平均与分布。窗口规则让读者知道数字怎样得到；体系是否已充分平衡，还要结合更长观察、独立重复和相关时间来判断，这些内容会在第九讲继续展开。

## 把真实记录变成一张能解释的图

GROMACS 把能量与热力学量写入 edr 文件。它是一种适合程序读取的二进制记录，不能像普通文章那样直接打开逐行阅读。gmx energy 可以从中选择需要的量，导出为带有列说明的 xvg 文本。xvg 文件中，开头带井号或 @ 的行通常保存注释、标题与坐标轴信息；其余数据行保存数值。这里选择 Density、Volume 和 Temperature，便能得到时间加三种观测量。程序可能按内部编号排列输出列，因此分析脚本会读取文件中的实际列标签，再找到对应数据，不把输入名称的先后顺序当成输出顺序。

下面的命令在包含本讲水例结果的目录中执行。命令行可以先看作一种按文字下达指令的界面：gmx 是程序入口，energy 是工具名称，-f 后面给出要读的文件，-o 后面给出要写的文件。管道符把前面产生的文字送给后面的程序，相当于替我们在交互选择界面依次输入几个名称。0 表示结束选择。命令只提取已有记录，不改变模拟时的温度或压力，也不会重新生成分子的运动。

### 从 NPT 能量文件提取三种观测量

```
#!/usr/bin/env bash
set -euo pipefail
printf 'Density\nVolume\nTemperature\n0\n' | gmx energy \
  -f npt.edr -o npt-density-volume-temperature.xvg
```

在含有 npt.edr 的例题结果目录中执行。XVG 的 @ sN legend 标签给出各数据列的实际物理量；下一段程序按标签查找。

接下来的 Python 程序完成三个步骤：读出有效数据、选择记录后半段、绘制同时保留原始信息与统计概括的图。Python 是一种编程语言，适合把重复的分析操作写成可再次执行的文本；NumPy 负责数组计算，Matplotlib 负责作图。数组可以理解为按顺序排好的一列或几列数字。我们对密度列做累计求和，再除以目前累计的样本数，就能看到平均值如何随记录增长而变化。代码写在同一页，变量名也与图中物理量对应，方便逐行对照。

程序输出的表包括样本数、起止时间、均值和样本标准差。标准差描述这一窗口内数据散开的程度；它与平均值的不确定度是不同的量。相邻两帧来自连续运动，常常相似，把每帧都当成互相独立的一次实验会低估平均值的不确定度。因此，这里直接展示波动大小，并保留完整时间顺序。若看到缓慢漂移，就应延长观察或检查准备过程，而不是通过一条更平滑的曲线把漂移隐藏起来。

### 完整 Python 分析：时间曲线、分布与观察窗口

```
#!/usr/bin/env python3
"""Analyze the recorded NPT water box and plot its thermodynamic observables.

From a directory containing this script and the exported XVG:
    python analyze_water.py npt-density-volume-temperature.xvg --output figures

Dependencies: numpy, matplotlib. The output window is the second half in time.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_xvg(path: Path) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    legends: dict[int, str] = {}
    rows: list[list[float]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("@"):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = match[2]
            continue
        if line.startswith("#"):
            continue
        if line == "&":
            raise ValueError("Expected one XVG dataset, found a dataset separator.")
        rows.append([float(value) for value in line.split()])
    if len(rows) < 4:
        raise ValueError("At least four saved samples are required.")
    if len({len(row) for row in rows}) != 1:
        raise ValueError("The number of columns changes inside the XVG file.")
    values = np.asarray(rows, dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("The data contain a nonfinite value.")
    time_ps = values[:, 0]
    if not np.all(np.diff(time_ps) > 0):
        raise ValueError("Saved times must increase strictly.")
    columns: dict[str, np.ndarray] = {}
    for index, label in legends.items():
        if index + 1 >= values.shape[1]:
            raise ValueError(f"Legend {label!r} refers to a missing column.")
        key = re.sub(r"[^a-z]", "", label.casefold())
        if key in columns:
            raise ValueError(f"Duplicate series label: {label}")
        columns[key] = values[:, index + 1]
    for key in ("density", "volume", "temperature"):
        if key not in columns:
            raise ValueError(f"Required XVG legend missing: {key}")
    if np.any(columns["volume"] <= 0) or np.any(columns["density"] <= 0):
        raise ValueError("Volume and density must be positive.")
    return time_ps, columns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xvg", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figures"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    time_ps, data = read_xvg(args.xvg)
    start = time_ps[0] + 0.5 * (time_ps[-1] - time_ps[0])
    selected = time_ps >= start
    n = int(selected.sum())
    if n < 2:
        raise ValueError("The observation window contains fewer than two samples.")
    args.output.mkdir(parents=True, exist_ok=True)
    units = {"density": "kg/m^3", "volume": "nm^3", "temperature": "K"}
    stats = []
    for quantity in ("density", "volume", "temperature"):
        y = data[quantity][selected]
        stats.append({
            "quantity": quantity, "unit": units[quantity],
            "samples": n, "start_ps": float(time_ps[selected][0]),
            "end_ps": float(time_ps[selected][-1]),
            "mean": float(np.mean(y)),
            "sample_standard_deviation": float(np.std(y, ddof=1)),
        })
    with (args.output / "water_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(stats[0]))
        writer.writeheader()
        writer.writerows(stats)
    report = {
        "input": args.xvg.name,
        "window_rule": "second half of the recorded physical-time interval",
        "spread_definition": "sample standard deviation; not uncertainty of the mean",
        "series": stats,
    }
    (args.output / "water_summary.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    zh = args.language == "zh"
    label = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({
        "font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": "#173534", "text.color": "#173534",
        "axes.edgecolor": "#75918c", "svg.fonttype": "path",
        "figure.facecolor": "#faf9f4", "axes.facecolor": "#faf9f4",
        "savefig.facecolor": "#faf9f4",
    })
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    panels = [(axes[0, 0], "density", label("密度 / kg m⁻³", "Density / kg m⁻³")),
              (axes[0, 1], "volume", label("体积 / nm³", "Volume / nm³")),
              (axes[1, 0], "temperature", label("温度 / K", "Temperature / K"))]
    for axis, key, ylabel in panels:
        axis.axvspan(time_ps[selected][0], time_ps[-1], color="#dbe9e0", alpha=0.6)
        axis.plot(time_ps, data[key], color="#598a89", lw=0.7, alpha=0.7,
                  label=label("逐帧记录", "Recorded samples"))
        running = np.cumsum(data[key][selected]) / np.arange(1, n + 1)
        axis.plot(time_ps[selected], running, color="#994b2a", lw=2.0,
                  label=label("窗口内累积均值", "Window cumulative mean"))
        axis.set(xlabel=label("物理时间 / ps", "Physical time / ps"), ylabel=ylabel)
        axis.grid(axis="y", color="#c9d7cf", linewidth=0.5)
    axes[0, 0].legend(frameon=False, fontsize=11, loc="best")
    axis = axes[1, 1]
    density = data["density"][selected]
    axis.hist(density, bins="fd", density=True, color="#4f8980",
              edgecolor="#faf9f4", linewidth=1.0)
    axis.axvline(np.mean(density), color="#994b2a", lw=2,
                 label=label("窗口均值", "Window mean"))
    axis.set(xlabel=label("密度 / kg m⁻³", "Density / kg m⁻³"),
             ylabel=label("概率密度 / m³ kg⁻¹", "Probability density / m³ kg⁻¹"))
    axis.legend(frameon=False, fontsize=11)
    fig.suptitle(label("SPC/E 水：NPT 阶段的实际记录", "SPC/E water: the recorded NPT window"), fontsize=19)
    for panel_label, axis in zip("ABCD", axes.flat):
        axis.set_title(panel_label, loc="left", fontweight="bold", pad=9)
    fig.savefig(args.output / "water_observables.svg")
    fig.savefig(args.output / "water_observables.png", dpi=180)
    plt.close(fig)
    for row in stats:
        print(f"{row['quantity']}: mean={row['mean']:.6g} {row['unit']}; "
              f"sample SD={row['sample_standard_deviation']:.6g}; "
              f"n={row['samples']}; "
              f"window={row['start_ps']:g}–{row['end_ps']:g} ps")


if __name__ == "__main__":
    main()
```

安装 NumPy、Matplotlib 后，按脚本开头的命令运行；程序生成 SVG、PNG、CSV 和 JSON。程序读取本例的 NPT XVG 记录。绿色底色是记录后半段，深色线是该窗口内的累积均值；统计表的标准差描述波动。

作图时，横轴必须写明物理时间及单位，纵轴应写明所测量的量。密度曲线保留细线表示逐帧变化，另用较醒目的线表示所选窗口内的累积平均；分布图展示同一窗口的数据落在哪些范围。直方图把连续数值按区间分组，某个区间较高表示落入其中的帧更多。这里使用概率密度归一化，让所有柱子的面积合计为一，因此纵轴单位是密度单位的倒数。它不是水分子的空间密度图，也不表示盒子里有多个独立的水样品。

### NPT 水盒的密度、体积与温度记录

由 G01/analyze_water.py 对 npt-density-volume-temperature.xvg 读取实际列标签生成。显示完整记录与后半段窗口，图表给出时间范围、均值及样本标准差。标准差描述窗口内波动，不是平均值置信区间。

GROMACS 2026.4；884 个 SPC/E 水分子，初始立方盒边长 3 nm；目标温度 300 K、压力 1 bar。NPT 记录 100 ps，描述统计窗口为 50–100 ps；轨迹播放器显示另一个 100 ps NVE 阶段。

[下载参考数据与完整输入（ZIP） 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/#zh-s6)

实际 NPT 记录。阴影为后半段 50–100 ps；细线保留各时刻的数值，深色线为从 50 ps 起计算的累计均值。直方图对该时间窗内的密度采样作概率密度归一化。

| 测量量 | 数值 | 单位 |
| --- | --- | --- |
| 密度窗口均值 | 997.8 | kg m⁻³ |
| 密度样本标准差 | 11.26 | kg m⁻³ |
| 体积窗口均值 | 26.51 | nm³ |
| 体积样本标准差 | 0.2976 | nm³ |
| 温度窗口均值 | 300.9 | K |
| 温度样本标准差 | 5.612 | K |

这次 50–100 ps 的观察窗口含有 251 个记录点，平均密度为 997.83 kg·m⁻³，样本标准差为 11.26 kg·m⁻³；平均体积为 26.506 nm³。图中体积向上变化时，密度随之向下，因为盒中的 884 个水分子没有改变。温度均值为 300.86 K，围绕 300 K 目标涨落。密度曲线还保留了持续数皮秒的高低起伏，相邻记录因此共享一部分运动信息；251 个记录点并不等于 251 次独立实验。这里的数字描述这个模型和窗口，为后续更长采样与重复比较提供起点。

读这组结果时，可以先看温度是否围绕目标附近变化，再看体积与密度是否呈现相反方向的波动，最后检查选定窗口中的平均值是否仍持续偏移。原始轨迹中的每个数字都应能回到明确的输入、阶段和时间范围。若换了水模型或控制条件，就重新运行并分析新的记录。同一分析程序让我们能在相同定义下比较不同设置产生的新数据。

## 动画里发生了什么，统计图又多告诉了什么

观看水的轨迹时，最容易注意到的是原子移动与分子转动。画面中的小球大小和颜色通常是显示规则，氧画得较大、氢画得较小，有助于辨认分子；它们并不表示电子云的完整形状。连接原子的细杆也主要帮助我们识别分子内部的连接。要把可视化用于解释，最好同时给出盒子范围、物理时间和表示方式，让读者知道自己正在看什么。一个色彩丰富却没有尺度的动画，很难帮助判断分子移动得有多远。

周期边界还会产生一种特别的视觉现象：同一个分子可能被显示在盒子的两侧。某些画法按每个原子的位置分别包回盒子，于是一个水分子的氧在右边，氢却出现在左边，看上去像有一根横穿整个盒子的长键。这是坐标表示的问题，并不意味着化学键真的拉长到盒子尺度。把分子重组为完整形状，再按需要居中显示，可以帮助阅读；后续测量扩散时又需要保留连续跨边界位移，因此显示用轨迹与分析用轨迹的处理目的应当区分。

### 水分子的移动、转动与周期性表示

来自同一 SPC/E 水盒的 nve-2fs 轨迹；显示物理时间、盒子范围及完整分子的周期性表示。播放、暂停与逐帧观察用于区分真实运动与边界显示。

从动画中看见两个分子靠近，只能说明这一时刻的排列。若想说“某个距离处更常出现水分子”，就需要在许多时刻、许多参考分子周围统计距离分布；若想说“分子运动较快”，就需要定义位移随时间的增长，再与其他条件下的结果比较。这样的统计相当于把许多镜头叠起来，寻找反复出现的规律。它既保留微观解释，又避免让一段恰好被选中的漂亮片段承担整个研究结论。

有时两段轨迹看起来很像，密度却不同；有时平均密度接近，局部取向与扩散却不同。这些情况都可以理解，因为密度把大量信息压缩成了一个数。两个教室的每平方米人数可以相同，桌椅排列、走动方式和交流范围仍然不同。评价一个水模型时，密度是有用的检验项目，此外还可以比较径向分布、扩散、介电响应和其他热力学量。选择哪些量，应由接下来的研究问题决定，而不是把所有能算的曲线都放进正文。

对于生物材料，这种取舍尤其实际。研究一种涂层是否形成稳定的水化层，可能需要关注界面附近的水数目、驻留行为和取向；研究一条聚合物在水中是否伸展，可能需要同时观察链的尺寸与链水接触；研究蛋白质构象，则要区分整体平移、整体转动与内部结构变化。同一套“定义对象—跟踪运动—统计观测量”的方法会贯穿这些章节，水盒提供了一个足够简单、又能认真检验这套方法的起点。

## 怎样把一个好奇心变成可计算的问题

“这种材料好不好”包含许多相互不同的判断，很难直接交给分子动力学。我们可以先把它缩小为一个具体比较：在相同温度、盐浓度与链长下，两种表面化学组成是否形成不同的近表面水分布？这样一来，体系组成、控制条件和测量对象都有了位置。材料的宏观表现仍需要实验与更大尺度的描述来连接，而分子模拟提供的是其中一段可追踪的结构与运动关系。

设计计算时，先写一句完整的问题会很有帮助。例如，“在 300 K、1 bar 的周期性 SPC/E 水盒中，NPT 记录后半段的密度如何涨落？”这句话同时说明对象、模型、条件、阶段、时间窗口和观测量。把“密度”换成“结冰速率”，原来的短时水盒设置就不再足以支持这个新任务，需要考虑成核过程、过冷条件、体系尺寸和更长采样。问题一变，模型设计也要跟着变，而不是只把同一个程序多运行几次。

比较两种设置时，还要决定哪些条件保持一致。若同时改变温度、水模型、盒子大小和分析窗口，曲线变化的原因就会纠缠在一起。可以先固定其余设置，只改变一个与问题直接相关的因素，再用重复运行评估波动。比如第四讲检查时间步时，会尽量保持起始状态和总物理观察时间一致，这样更容易把数值差异与步长联系起来。后面的 PEG 链长研究则会保留相同的化学与溶剂定义，让链长变化成为主要比较因素。

现在再回看那杯糖水，分子模拟能帮助我们把日常现象拆成可以测量的局部问题：水在哪里停留，糖分子怎样转动，某种接触保持多久，某条链在多大范围内改变形状。每个问题都需要一套合适的模型和统计方法。接下来，我们会把水盒需要的坐标、拓扑与运行参数逐一打开，理解它们怎样组成一次可以重复的计算，再亲自让这盒水开始运动。

## 延伸阅读与开放资料

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  水盒构建、分阶段平衡与密度测量的教学流程改编。

  水模型改为 SPC/E，初始盒边长 3 nm，目标 300 K 与 1 bar；更新控制算法并加入 NVE 检查。教学文字、图示、交互与统计分析重新编写；流程改编部分沿用 CC BY-SA 4.0。
- [GROMACS 2026.4: Water solvation](https://manual.gromacs.org/2026.4/how-to/topology.html#water-solvation) · GROMACS developers · Consult GROMACS documentation distribution license

  三位点水初始坐标与拓扑选择的技术依据。

  独立解释坐标与模型参数的区别。
- [Correlations in the Motion of Atoms in Liquid Argon](https://doi.org/10.1103/PhysRev.136.A405) · A. Rahman · Publisher copyright; bibliographic and factual citation

  1964 年液氩模拟与可测观测量的科学史。

  历史机制图为原创示意，没有复制论文图片或数据。
- [The missing term in effective pair potentials](https://doi.org/10.1021/j100308a038) · H. J. C. Berendsen; J. R. Grigera; T. P. Straatsma · Publisher copyright; bibliographic and factual citation

  SPC/E 有效模型与极化能量处理的历史背景。

  独立叙述与原创三位点水示意。
