# 紫外—可见吸收：光如何变成浓度

Source: https://ml-biomat.com/tutorials/experimental-methods/s03/
Language: zh-CN

从颜色变浅的日常观察理解透过率和吸光度，再把标准曲线、稀释与光学误差连接成一次完整定量。

## 一杯水变浅了，怎样知道里面还剩多少分子

把一滴有颜色的液体加入清水，再逐渐加水，颜色会变浅。眼睛能够比较深浅，却很难说出浓度究竟降低了多少，也难以看见紫外区的吸收。紫外—可见分光光度计把这个日常观察变成测量：选择一种波长，比较光穿过空白和样品之后的强度，再把差别与目标物浓度联系起来。研究材料释放药物时，可以测量释放液中的吸收；研究蛋白质时，可以利用特定波长的吸收或显色反应估计含量；研究薄膜时，还可以比较不同波长的透过情况。这些用途共享光学原理，却需要不同的样品条件和校准方法。

颜色来自样品对不同波长的光采取了不同的“去留方式”。一种溶液若主要吸收某一段可见光，眼睛看到的是透过或散射到眼睛中的其他光共同形成的颜色。因此，看到蓝色并不意味着样品只在蓝色波段吸收。紫外吸收甚至可以发生在肉眼完全无色的溶液中。光谱的横坐标是波长，纵坐标表示样品削弱光束的程度；它比一个颜色名称保留了更多信息。读者可以把全谱看成一张按波长展开的检查表：目标峰在哪，背景是否倾斜，峰形是否随稀释改变，都比只记录一个数字更容易发现问题。

本篇用一个可复算的染料定量问题串起整个过程。我们先测定一组已知浓度的标准液，再测量一个经过五倍稀释的未知样品，从校准直线反推出原液浓度。随后把杂散光和浑浊加入光学模型，观察为什么同样的计算在高吸收或含颗粒样品中会出现偏差。数值练习中的吸收谱和标准液读数是明确构造的教学数据，参数与随机种子保存在程序中。它们让读者同时看见真实设定值、仪器模型的读数和最终计算值，从而区分光学测量、数学拟合与实验解释三个环节。

一个常见误解是，只要仪器显示“吸光度”，就已经知道目标物的浓度。事实上，仪器首先记录到达探测器的光。目标分子吸收、颗粒散射、比色皿表面污迹和其他溶质都可能让这束光减少。把减少量归给某一种分子，需要有选择的波长、匹配的空白、合适的标准和稳定的化学条件。目标物是自由分子、结合在蛋白质上还是处于不同酸碱形态，也可能改变吸收。把测量问题写成“在这些条件下，这一种化学形态的浓度是多少”，比简单地问颜色多深更接近一次可解释的定量实验。

## 为什么石英和光电检测改变了分析化学

人们很早就用颜色比较溶液，但肉眼比较依赖照明、观察者和参照。把光分成不同波长，再用电信号测量透过光，分析就能走向更稳定的定量。1941 年推出的 Beckman DU 分光光度计，是这段仪器发展史中的一个重要例子。它采用石英光学元件，把观察延伸到近紫外区域。石英在这里不是一个装饰性的材料名称：普通玻璃在某些紫外波段自身吸收较强，光还没到达样品就可能被光学元件削弱。仪器能测什么，既取决于电子学，也取决于光经过的每一种材料。

![以石英光路的历史作用连接现代分光测量。上图说明选取波段、样品与光电检测的功能关系，为原创原理图；下图比较相同光程中的空白与样品，箭头宽度只示意光强差别。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7d197b20856761c5a8aebd44.svg?v=7d197b208567)

图 1以石英光路的历史作用连接现代分光测量。上图说明选取波段、样品与光电检测的功能关系，为原创原理图；下图比较相同光程中的空白与样品，箭头宽度只示意光强差别。

在一种常见的扫描式光路中，光源先发出较宽波段的光，单色器用光栅或棱镜及狭缝选择其中较窄的一段，然后让这段光穿过样品，最后由探测器把光强变成电信号。改变选中的波长，就得到整张吸收谱。阵列式仪器可以采用不同顺序：宽波段光先穿过样品，再分散到阵列探测器的不同位置，同时记录多个波长。理解这两种安排，可以避免把所有仪器都想成同一条固定光路；它们都要回答相同的核心问题，即样品与参照在相应波长下让多少光到达探测器。

单光束仪器通常先记录空白，再记录样品；双光束设计则安排样品通道和参照通道，帮助跟踪光源等随时间的变化。参照通道并不会替代化学空白。若样品使用含盐和缓冲剂的溶液，空白通常也应含有对应的溶剂和非目标成分；若进行了显色反应，空白还应包含除目标物以外的相关试剂并经历相同处理。空白的作用是让共同贡献尽量相互抵消，而不是把任何不希望看到的信号都定义为零。目标与背景在化学上如何区分，仍然由实验设计决定。

比色皿看起来只是一个小容器，却决定光程和部分背景。光程是光在样品中穿行的长度，常见比色皿标称 1 cm，但微量装置、流通池和微孔板可以不同。测紫外区时要检查容器在目标波段的透过能力；测量前应保持透光面清洁、方向一致，并让液面覆盖光束。气泡会改变光的传播，指纹会增加散射或吸收，装液体积不足会让光束部分穿过空气。与其在异常读数后反复拟合，不如把这些直接影响光路的条件先稳定下来，随后才讨论分子浓度的细微差别。

负吸光度也可以从参照关系理解。例如读数为 −0.01，表示样品通道的校正光强约为空白的 1.023 倍，并不是样品产生了“负吸收分子”。在接近零的区域，小幅随机读数波动可能越过零线；若整段光谱持续偏负，则可以重新测量空白、交换并检查比色皿，以及核对样品与空白的溶剂组成。特别是空白中存在样品没有的吸收成分时，参照本身会损失更多光。先寻找两次测量之间真正改变的条件，再决定如何处理读数，能够保留这类异常带来的实验信息。

## 为什么取对数：每一层吸收的是剩余光的一部分

把均匀溶液想成许多很薄的相同层。假如每层都让入射到该层的光剩下九成，第一层后剩下原来的九成，第二层后剩下九成的九成，第三层继续乘九成。每层移走的绝对光量越来越小，因为后面的层收到的光已经变少；相同的是留下的比例。这正是指数衰减的直观来源。增加浓度，就像在相同长度内增加能够吸收的分子；增加光程，就像让光多穿过几层。只要分子的吸收性质和传播条件保持相同，这两种增加会以相似方式影响透过比例。

![三个相同教学薄层各透过一半光：1000、500、250、125 的数列对应透过率连乘。右图把同一关系写成吸光度相加，帮助理解对数变换；计数与薄层均为原理模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2e10a22fd11aefd04db90df7.svg?v=2e10a22fd11a)

图 2三个相同教学薄层各透过一半光：1000、500、250、125 的数列对应透过率连乘。右图把同一关系写成吸光度相加，帮助理解对数变换；计数与薄层均为原理模型。

$$
T=\frac{I}{I_0},\qquad A=-\log_{10}T
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 透过率，无量纲；百分透过率为 100T%。 |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 样品测量中目标光的强度，已扣相应暗信号；与 I₀ 采用相同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 匹配空白中的目标光强度，已扣相应暗信号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以 10 为底的对数。 |

均匀薄层的透过比例连乘；对数把乘积转化成和。T=0.5 时 A=0.30103；两个相同层给出 T=0.25、A=0.60206。样品与空白须使用相同检测条件。

透过率是样品透过光强与空白透过光强的比值，通常先写成 0 到 1 之间的数，再按需要乘 100% 显示。吸光度对透过率取以 10 为底的负对数，于是连乘的衰减变成可以相加的量。透过率为 0.5 时，吸光度约为 0.301；再串接一层相同溶液，透过率变成 0.25，吸光度约为 0.602。两层吸光度相加，正好对应透过率相乘。这里的对数没有凭空增加物理信息，它改变的是表达方式，让与浓度、光程的线性关系更容易使用。

$$
A=\varepsilon l c
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 指定波长、化学形态和环境下的摩尔吸光系数，L·mol⁻¹·cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b725c065245400348075701d.svg) | 样品光程，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 目标物浓度，mol·L⁻¹。 |

适用于吸收性质稳定、足够窄波段、均匀且散射影响得到适当处理的条件。系数 50000、光程 1 cm、浓度 10 μmol/L = 10⁻⁵ mol/L，给出 A=0.5 和 T=0.31623。浓度若改用 μmol/L，数值斜率相应为 0.05，而不是 50000。

摩尔吸光系数描述指定化学形态在指定波长和条件下吸收光的能力。它的单位需要与浓度和光程配合：若浓度用 mol·L⁻¹，光程用 cm，系数就用 L·mol⁻¹·cm⁻¹，乘起来得到无量纲吸光度。假设系数为 50000 L·mol⁻¹·cm⁻¹，浓度为 10 μmol·L⁻¹，光程为 1 cm，则吸光度为 0.5，透过率约为 31.6%。这里的 μ 表示百万分之一，10 μmol·L⁻¹ 就是 0.000010 mol·L⁻¹。单位换算先写清楚，才不会把微摩尔数值直接当成摩尔数值带入。

这条关系把电子能级与定量联系起来。一个分子吸收光子，意味着获得与某种允许跃迁匹配的能量；紫外—可见吸收常涉及电子状态变化。不同分子和不同化学环境会改变允许跃迁的能量及强弱，因此吸光系数随波长变化，也可能随酸碱度、结合状态或溶剂变化。研究者常在目标吸收较强、背景较小且化学形态稳定的波长定量。峰顶附近还常有一个实际优点：很小的波长设定变化对吸光度的一阶影响较小。不过，选择波长仍要考虑其他成分的重叠和仪器在该波段的性能。

## 从标准液到未知液：一条直线怎样获得实验含义

已知吸光系数时，可以直接用物理关系估计浓度；更多实际任务会用标准液建立校准。标准液与未知样品采用相同溶剂、试剂、反应时间、容器和波长，使相同浓度尽量产生相同响应。示例采用 0、2、4、8、12 和 16 μmol·L⁻¹ 六个水平，每个水平测量三个教学重复值。重复值帮助观察同一水平的读数散布，多个水平则用于判断响应是否接近直线。浓度范围应覆盖预计的未知样品读数；把未知样品稀释到已验证范围内，通常比把直线延长到很远的地方更有根据。

$$
A=mc+b,\qquad c_{\mathrm{stock}}=D\frac{A_u-b}{m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 标准液吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 校准斜率，本篇单位为 L·μmol⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 标准液浓度，本篇用 μmol·L⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 校准截距，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8734e10f39fb90d4cce9d728.svg) | 未知稀释液的吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 总体积除以原液取样体积的稀释倍数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4cc5ee38ac5d83177d5a1ad.svg) | 原液浓度，μmol·L⁻¹。 |

先扣除模型截距，再按斜率反算稀释液浓度，最后乘稀释倍数。例如 Aᵤ=0.39、b=0.02、m=0.05 时稀释液为 7.4 μmol/L；D=5 时原液为 37 μmol/L。程序中的读数含噪声，估计值会与此理想例子略有差别。

斜率表示浓度每增加一个单位，吸光度平均增加多少；截距表示浓度为零时，校准模型预计的响应。空白扣除后，截距仍可能因随机误差或残余背景而稍偏离零，因此不要仅为了图形整齐就强迫所有直线穿过原点。是否使用零截距，应由方法定义和空白证据支持。示例保留截距，并把每个测量点画出来，再画出数据减去拟合值的残差。若低浓度残差偏正、中间偏负、高浓度又偏正，这种系统弯曲比一个很高的相关系数更能提示线性模型的不足。

![教学标准液、未知液与误差传播来自同一组数据。A 显示未知读数位于标准范围内；B 保留每个点的残差；C 显示固定标准浓度和稀释倍数下的读数误差传播；D 给出反算步骤。虚线 37 μmol/L 是设定原液浓度，区间为模型分位区间。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fe192a7adc4e64f0f4e40c5a.svg?v=fe192a7adc4e)

图 3教学标准液、未知液与误差传播来自同一组数据。A 显示未知读数位于标准范围内；B 保留每个点的残差；C 显示固定标准浓度和稀释倍数下的读数误差传播；D 给出反算步骤。虚线 37 μmol/L 是设定原液浓度，区间为模型分位区间。

反算浓度时，先从未知样品的吸光度中减去截距，得到模型归给目标浓度的响应，再除以斜率。示例未知液设定为 7.4 μmol·L⁻¹，测量前原液已经稀释五倍，因此原液设定浓度为 37 μmol·L⁻¹。实际计算会因教学噪声产生小幅偏差，程序在图和摘要中给出估计值。这个步骤有一个清楚的量纲检查：吸光度除以“每微摩尔每升的吸光度”，得到微摩尔每升；再乘无量纲稀释倍数，仍然是浓度。只看公式外形往往记不住，沿着单位走一遍就能检查是否少乘或多乘了一次稀释倍数。

稀释倍数来自总体积与取样体积的比例。例如取 200 μL 原液，加溶剂至 1000 μL，总体积是原来的五倍，所以浓度变为五分之一；“再加入 1000 μL”则会得到 1200 μL 总体积，稀释倍数变成六。实验记录应写清楚加至多少，而不是只记一个模糊的“加水五倍”。若进行多次连续稀释，总稀释倍数是各步倍数相乘。连续稀释还会共享前一步的配制误差，因此多个标准液并不总是具有完全独立的浓度误差。高精度定量需要把配液过程也纳入误差来源。

校准不确定度包含多种来源。未知样品重复测量的散布、斜率与截距估计的不确定性、标准物质浓度、移液与定容、反应完成程度都可能贡献误差。程序用一个明确的模型演示其中一部分：在已知标准浓度和固定稀释倍数下，利用拟合残差估计读数波动，再重复生成校准读数与未知读数，得到反算浓度的分布。这个分布描述指定噪声模型中的传播效果。把它应用到真实实验时，可以进一步加入配液浓度和体积的不确定度，而不是把程序输出的小数位数误认为测量具有同样精度。

## 吸收很强与样品浑浊，为什么是两类不同问题

吸光度越大，到达探测器的目标波长光越少。吸光度为 1 时，透过率是 10%；吸光度为 2 时只剩 1%；吸光度为 3 时只剩 0.1%。这时原本很小的额外光就可能占据相当大的比例。杂散光指到达探测器、却处于单色器选定波段之外等非理想光学贡献中的相关部分。它会让探测器以为透过光比实际多，从而低估吸光度。信号接近杂散光背景时，再增加样品浓度，测得的吸光度会逐渐趋于上限，校准曲线也会向下弯曲。

$$
A_{\mathrm{meas}}=-\log_{10}\!\left(\frac{10^{-A_{\mathrm{true}}}+s}{1+s}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/484437b4906af10337d8a00b.svg) | 加入杂散光后的测得吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8a413ff8e77959d2570fd134.svg) | 只有目标波长光时的真实吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 杂散光强度除以空白目标光强度的比值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以 10 为底的对数。 |

样品和空白都收到相同、未被目标物衰减的额外光，所以分子与分母分别加 s。Atrue=3、s=0.001 时，读数约为 2.6994；浓度无限增大时，上限为 log₁₀[(1+s)/s]，约 3.0004。真实杂散光的光谱分布与吸收情况需要按仪器和样品确定。

模型假设样品和空白读数中都加入相同的杂散光，且这部分光不被目标物衰减。设杂散光为空白目标光强的 0.1%，理想吸光度为 3 时，目标透过光也恰好是空白的 0.1%。两者加在一起后，测得吸光度约为 2.699，而不是 3；浓度继续增加，读数逐渐逼近约 3.0004 的上限。这个简单计算解释了为何高吸收样品常需要稀释或缩短光程。下面的交互允许分别改变浓度、光程和杂散光比例，观察理想直线与实际读数如何分离。

## 浓度继续增加时，吸光度为什么停住了

目标物在选定波长下的摩尔吸光系数设为 50000 L·mol⁻¹·cm⁻¹。改变浓度、光程和未被样品吸收的杂散光比例，比较理想直线与仪器模型读数。圆点表示当前浓度；下方同时显示真实透过率，帮助把对数读数还原为光强比例。

[Figure: 浓度、光程与杂散光对吸光度的影响](https://ml-biomat.com/tutorials/experimental-methods/s03/#S03-plot)

先将浓度调到 60 μmol·L⁻¹，再把光程从 1 cm 改为 0.2 cm。相同样品在较短光程下透过更多光，杂散光占检测信号的比例随之减小。这里比较的是固定化学形态和均匀澄清溶液中的光学效应。

浑浊则涉及光的传播方向变化。颗粒把一部分光散射到探测器没有收集到的方向，仪器也会观察到透过光减少。若把这部分减少全部套进吸收定量模型，就可能把颗粒的存在误算成目标分子增加。对细胞或菌悬液，所谓光密度读数常被用作经过特定校准的浊度指标，其含义与澄清溶液中单一溶质的吸收不同。对材料释放液，可以比较全谱背景、观察离心或合适分离前后的变化，并确认分离过程是否同时移除了目标物；实验处理要服务于想测量的是游离部分还是总含量。

化学变化还会使比尔—朗伯关系中的吸光系数发生变化。酸碱指示剂的两种形态具有不同颜色，就是容易理解的例子。若稀释同时改变了酸碱度或结合平衡，浓度降低与光谱形状改变会一起发生，简单的比例缩放就可能失效。比较不同稀释倍数下按浓度归一化的整张谱，可以检查峰位和相对形状是否保持一致；对受缓冲条件控制的体系，应让标准与样品进入相同测量条件。把光学非线性、散射背景和化学形态变化分别考虑，后续补充实验才会有明确方向。

![两种不同偏差的计算示意。左图显示未被目标物吸收的杂散光让高吸收读数趋于上限，s 是相对于空白目标光的比例；右图将构造吸收峰与按波长四次方反比变化的散射损失分开，展示全谱诊断的价值。右图采用可相加的表观衰减近似。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a15b53022b35e764544f51e7.svg?v=a15b53022b35)

图 4两种不同偏差的计算示意。左图显示未被目标物吸收的杂散光让高吸收读数趋于上限，s 是相对于空白目标光的比例；右图将构造吸收峰与按波长四次方反比变化的散射损失分开，展示全谱诊断的价值。右图采用可相加的表观衰减近似。

## 完整计算：让浓度结果和诊断图一起出现

完整程序先生成标准液和未知液的教学读数，拟合带截距的校准直线，绘制逐点残差，再传播读数误差得到原液浓度分布。它还计算吸光度与透过率的关系、杂散光造成的高吸收偏差，以及一个吸收峰叠加波长相关散射背景的示例。输出包含可以直接查看的双语图、标准液 CSV、全谱 CSV 和计算摘要。程序采用固定种子，因此同一环境中重复运行可核对相同结果；将自己的数据放进来时，应保留浓度单位、空白处理方式和稀释记录，而不仅替换最后一列数字。

### 从标准读数到原液浓度与诊断图

完整程序生成明确标记的教学数据，运行校准、稀释反算与读数误差传播，并输出 CSV、计算摘要和本篇四组图。

```
"""UV-visible calibration with a declared teaching dataset and optical models.

Run: python main.py --output output --language en
Concentrations are in micromoles per liter unless explicitly stated otherwise.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

BLUE,TEAL,ORANGE,INK='#245ca6','#087f80','#ce6b35','#233446'


def measured_absorbance(true_absorbance,stray_fraction):
    """Equal unattenuated stray intensity enters sample and blank readings."""
    return -np.log10((10.**(-np.asarray(true_absorbance))+stray_fraction)/(1+stray_fraction))


def main(output,language):
    output.mkdir(parents=True,exist_ok=True);zh=language=='zh';tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'],
        'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none',
        'axes.unicode_minus':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6',
        'savefig.facecolor':'#fbfaf6','text.color':INK,'axes.labelcolor':INK})
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(output/f'{name}-{language}.{ext}',bbox_inches='tight',dpi=140)
        plt.close(fig)
    def arrow(ax,start,end,color=BLUE,lw=2):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=13,lw=lw,color=color))

    # Original historical-principle illustration, without copied apparatus art.
    fig,axes=plt.subplots(2,1,figsize=(11.8,6.8),layout='constrained')
    ax=axes[0];ax.axis('off');ax.set(xlim=(0,11),ylim=(0,3.2))
    ax.set_title(tr('石英让光路进入紫外：1941 年 DU 仪器的一个关键选择','Quartz opens the ultraviolet: a key choice in the 1941 DU instrument'),loc='left')
    ax.add_patch(Circle((.8,1.6),.22,color='#dfae56'));arrow(ax,(1.1,1.6),(2.5,1.6),INK)
    ax.add_patch(Polygon([[2.6,1.1],[3.3,1.1],[2.95,2.35]],closed=True,facecolor='#d9e8ec',edgecolor=INK))
    for y,color in [(1.2,ORANGE),(1.7,TEAL),(2.2,'#7850a2')]:arrow(ax,(3.1,1.65),(4.65,y),color)
    ax.plot([4.8,4.8],[.8,1.55],color=INK,lw=4);ax.plot([4.8,4.8],[1.85,2.6],color=INK,lw=4)
    arrow(ax,(4.95,1.7),(6.2,1.7),TEAL)
    ax.add_patch(Rectangle((6.3,1.1),.8,1.2,facecolor='#b9d7ce',edgecolor=INK))
    arrow(ax,(7.2,1.7),(8.7,1.7),TEAL,lw=1)
    ax.add_patch(Rectangle((8.8,1.25),.7,.9,facecolor='#e1e8ed',edgecolor=INK))
    for x,label in [( .8,tr('光源','Source')),(2.95,tr('分光','Disperse')),(4.8,tr('狭缝选色','Select band')),(6.7,tr('样品','Sample')),(9.15,tr('光电检测','Photoelectric detector'))]:ax.text(x,.5,label,ha='center',fontsize=10)
    ax.text(6.1,2.75,tr('功能示意；不按历史装置尺寸绘制','Functional illustration, not a scale drawing of the historical device'),fontsize=9,ha='center')
    ax=axes[1];ax.axis('off');ax.set(xlim=(0,11),ylim=(0,2.7));ax.set_title(tr('相同光路长度，比较空白与样品','Compare blank and specimen at the same path length'),loc='left')
    for y,label,color,width in [(1.9,tr('空白','Blank'),'#eef2f3',2.8),(.7,tr('样品','Sample'),'#a9cebf',1.3)]:
        arrow(ax,(1,y),(4.1,y),BLUE)
        ax.add_patch(Rectangle((4.2,y-.36),1.4,.72,facecolor=color,edgecolor=INK));ax.text(4.9,y,label,ha='center',va='center')
        arrow(ax,(5.7,y),(8.5,y),TEAL,lw=width)
        ax.add_patch(Rectangle((8.6,y-.3),.55,.6,facecolor='#e1e8ed',edgecolor=INK))
    ax.text(2.5,2.4,tr('相同入射条件','Same illumination'),ha='center')
    ax.text(7.1,2.4,tr('比较透过光强','Compare transmitted light'),ha='center')
    ax.text(4.9,.08,tr('光程 l','Path length l'),ha='center')
    save(fig,'optics')

    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained')
    ax=axes[0];ax.axis('off');ax.set(xlim=(-.4,5),ylim=(0,3.6));ax.set_title(tr('A · 相同薄层让透过比例相乘','A · Equal layers multiply transmission'),loc='left')
    for i in range(3):
        ax.add_patch(Rectangle((i*1.3+.7,.8),.4,1.7,facecolor=TEAL,alpha=.35,edgecolor=TEAL))
        ax.text(i*1.3+.9,.45,tr('一层','One layer'),ha='center')
    for i,count in enumerate([1000,500,250,125]):
        x=i*1.3+.2;arrow(ax,(x-.35,1.65),(x+.35,1.65),BLUE,lw=max(.8,count/260))
        ax.text(x,2.8,str(count),ha='center',color=BLUE)
    ax.text(2,3.25,tr('光子数比例示意','Illustrative photon-count ratios'),ha='center',fontsize=10)
    ax.text(2,.05,tr('0.5 × 0.5 × 0.5 = 0.125','0.5 × 0.5 × 0.5 = 0.125'),ha='center')
    ax=axes[1];layers=np.arange(0,7);a=-np.log10(.5)*layers
    ax.plot(layers,a,'o-',color=TEAL,label=tr('吸光度相加','Absorbances add'))
    ax.set(xlabel=tr('相同薄层数','Number of identical layers'),ylabel=tr('吸光度','Absorbance'),title=tr('B · 对数把连乘变成相加','B · Logarithms turn products into sums'))
    for n in [1,2,3]:ax.annotate(f'T={.5**n:g}',(n,a[n]),xytext=(8,-20),textcoords='offset points',fontsize=9)
    ax.legend();save(fig,'layers')

    rng=np.random.default_rng(530)
    levels=np.array([0,2,4,8,12,16.]);c=np.repeat(levels,3)
    a=.02+.05*c+rng.normal(0,.006,len(c))
    m,b=np.polyfit(c,a,1);residual=a-(m*c+b)
    sigma=float(np.sqrt(np.sum(residual**2)/(len(c)-2)))
    unknown=.02+.05*7.4+rng.normal(0,.006,3);dilution=5
    estimate=float(dilution*(unknown.mean()-b)/m)
    samples=[]
    for _ in range(3000):
        ym=m*c+b+rng.normal(0,sigma,len(c));mm,bb=np.polyfit(c,ym,1)
        yu=unknown.mean()+rng.normal(0,sigma,3).mean();samples.append(dilution*(yu-bb)/mm)
    samples=np.asarray(samples);lo,hi=np.quantile(samples,[.025,.975])
    np.savetxt(output/'calibration.csv',np.column_stack([c,a,m*c+b,residual]),delimiter=',',
       header='concentration_umol_L,absorbance,fitted_absorbance,residual',comments='')
    np.savetxt(output/'unknown.csv',unknown,delimiter=',',header='absorbance',comments='')
    np.savetxt(output/'propagated_concentration.csv',samples,delimiter=',',header='original_concentration_umol_L',comments='')
    fig,axes=plt.subplots(2,2,figsize=(12,7.8),layout='constrained')
    grid=np.linspace(0,16,200)
    axes[0,0].scatter(c,a,s=30,color=BLUE,label=tr('标准读数','Standard readings'))
    axes[0,0].plot(grid,m*grid+b,color=TEAL,label=tr('带截距拟合','Fit with intercept'))
    axes[0,0].scatter([(unknown.mean()-b)/m],[unknown.mean()],marker='D',s=60,color=ORANGE,label=tr('未知液','Unknown'))
    axes[0,0].set(title=tr('A · 标准与未知在同一量尺上','A · Standards and unknown on one scale'),xlabel=tr('浓度 / μmol L$^{-1}$','Concentration / μmol L$^{-1}$'),ylabel=tr('吸光度','Absorbance'));axes[0,0].legend(fontsize=9)
    axes[0,1].scatter(c,residual,color=BLUE);axes[0,1].axhline(0,color=INK,lw=1)
    axes[0,1].set(title=tr('B · 残差检查线性关系','B · Residuals check the linear relationship'),xlabel=tr('浓度 / μmol L$^{-1}$','Concentration / μmol L$^{-1}$'),ylabel=tr('测量 − 拟合','Observed − fitted'))
    axes[1,0].hist(samples,bins=42,color=TEAL,alpha=.8,density=True)
    axes[1,0].axvline(37,color=INK,ls='--',label=tr('设定值 37','Prescribed 37'))
    axes[1,0].axvline(estimate,color=ORANGE,label=f'{estimate:.2f}')
    axes[1,0].set(title=tr('C · 读数误差传播到原液浓度','C · Reading error propagates to stock concentration'),xlabel=tr('原液浓度 / μmol L$^{-1}$','Stock concentration / μmol L$^{-1}$'),ylabel=tr('概率密度 / (μmol L$^{-1}$)$^{-1}$','Density / (μmol L$^{-1}$)$^{-1}$'));axes[1,0].legend(fontsize=9)
    ax=axes[1,1];ax.axis('off');ax.set_title(tr('D · 逐步反算，保留单位','D · Back-calculate while retaining units'),loc='left')
    lines=[tr('未知液平均吸光度','Mean unknown absorbance')+f'  {unknown.mean():.4f}',
       tr('斜率','Slope')+f'  {m:.5f}  A / (μmol/L)',tr('截距','Intercept')+f'  {b:.5f}',
       tr('稀释液浓度','Diluted concentration')+f'  {estimate/5:.3f} μmol/L',
       tr('乘稀释倍数 5','Multiply dilution factor 5'),tr('原液浓度','Stock concentration')+f'  {estimate:.3f} μmol/L',
       tr('模型中 95% 分位区间','Model 95% quantile interval')+f'  [{lo:.2f}, {hi:.2f}]']
    for i,line in enumerate(lines):ax.text(.04,.9-i*.13,line,fontsize=10,transform=ax.transAxes)
    save(fig,'calibration')

    wave=np.linspace(350,750,801);absorption=.7*np.exp(-.5*((wave-530)/32)**2);scatter=.15*(530/wave)**4
    np.savetxt(output/'spectrum.csv',np.column_stack([wave,absorption,scatter,absorption+scatter]),delimiter=',',
       header='wavelength_nm,constructed_absorption,constructed_scattering_loss,total_apparent_absorbance',comments='')
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained');true=np.linspace(0,5,301)
    axes[0].plot(true,true,color=INK,ls='--',label=tr('理想响应','Ideal response'))
    for s,col in [(.0001,BLUE),(.001,TEAL),(.01,ORANGE)]:axes[0].plot(true,measured_absorbance(true,s),color=col,label=f's = {s:g}')
    axes[0].set(xlabel=tr('真实吸光度','True absorbance'),ylabel=tr('测得吸光度','Measured absorbance'),title=tr('A · 杂散光使高吸收响应弯曲','A · Stray light bends high-absorbance response'));axes[0].legend(fontsize=9)
    axes[1].plot(wave,absorption,color=TEAL,label=tr('构造吸收峰','Constructed absorption'))
    axes[1].plot(wave,scatter,color=ORANGE,label=tr('构造散射背景','Constructed scattering loss'))
    axes[1].plot(wave,absorption+scatter,color=BLUE,label=tr('总表观响应','Total apparent response'))
    axes[1].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('表观吸光度','Apparent absorbance'),title=tr('B · 全谱帮助发现不同贡献','B · Full spectra expose different contributions'));axes[1].legend(fontsize=9)
    save(fig,'diagnostics')
    summary={'data_kind':'constructed teaching calibration and optical models','seed':530,
       'absorbance_T05':float(-np.log10(.5)),'transmission_A05':float(10**(-.5)),
       'slope':float(m),'intercept':float(b),'unknown_diluted_estimate':estimate/5,
       'unknown_stock_estimate':estimate,'stock_true':37.,'reading_sigma':sigma,
       'stock_interval_reading_model':[float(lo),float(hi)],
       'stray_001_at_true3':float(measured_absorbance(3,.001)),
       'stray_001_plateau':float(np.log10(1001))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    main(args.output,args.language)
```

这里把校准点等权处理，意味着模型假设各点的吸光度误差具有近似相同方差。如果仪器在不同吸光度区域的读数波动明显不同，可以使用与测量方差相对应的权重，但权重应来自重复测量或合理噪声模型。高浓度区域已经发生系统弯曲时，单纯降低这些点的权重并不会恢复比尔—朗伯线性关系。更直接的做法是查明弯曲原因，重新确定适用浓度范围，并通过稀释把未知样品放回这个范围。计算方法与实验条件一起调整，得到的浓度才具有清楚含义。

程序中的误差传播没有把每个重复测量值看成一份独立制备样品，也没有把一条校准线的所有点当成所有实验条件。它固定标准浓度和稀释倍数，重复模拟读数噪声，然后重新拟合与反算。读者可以有针对性地扩展：给母液浓度加入一次共同扰动，再给各次移液加入独立扰动，观察共享误差怎样影响整条校准线。这种设计比给每个数据点随意增加相同噪声更接近配液过程，也能解释为什么增加读数重复次数无法消除一个共同的母液浓度偏差。

实际绘图时，标准液的原始点、拟合线和残差应当相互对应。未知样品的位置可以用不同符号标在校准图上，使读者直接判断它是否位于标准范围内。浓度分布或误差区间应标明表示读数重复、拟合传播还是独立样品差异，避免把含义不同的误差棒放在同一张图中却不给解释。对整张光谱，保留波长单位和空白处理说明；若比较经过归一化的谱，应同时保留能够恢复原始强度的信息。图既要便于读，也要让读者能沿着图找到具体的计算对象。

## 在材料与生物实验里，怎样选择下一步测量

在药物释放实验中，光谱定量通常位于一条更长的计算链中：取出一定体积释放液，测浓度，再计算释放质量；若补回等体积新液，还要把此前取走的质量计入累计释放。此时本篇得到的是所测 aliquot 的浓度，累计质量还需要各次取样体积和容器总体积。容器吸附、药物降解和载体碎片的散射也会影响读数。可以为释放介质、空白载体和药物标准分别建立对照，并使用不同浓度的加标回收检验基质是否改变响应。把这些步骤接起来，吸收谱才能支持材料释放行为的解释。

测蛋白质时，直接紫外吸收和显色法强调的化学过程不同。直接吸收与蛋白质中相关基团的含量及环境有关，不同蛋白质可能具有不同响应；显色法通过特定反应把含量转化为可见吸收，也会受到试剂相容性、反应时间和标准蛋白选择的影响。因此，选择一种方法时要先说明想测总蛋白、某种纯化蛋白还是混合样品中的相对变化。若需要区分具体蛋白质身份，分离、免疫识别或质谱等方法会提供吸收读数之外的信息。方法的选择由问题决定，而不只是由实验室里哪台仪器空着决定。

研究薄膜或多孔材料的光学性质时，透射、反射和散射也需要分别考虑。普通透射配置记录的是特定收集几何下到达探测器的光，表面反射和漫散射会改变结果。积分球等配置能够收集更广角度的光，适合进一步分解不同贡献。用溶液校准思路解释固体材料前，应先确定光程、表面状态和收集方式是否支持相同模型。把样品放进仪器得到曲线只是起点，知道哪些光被收集、哪些光离开了收集方向，才知道纵坐标包含哪些物理过程。

读完一次紫外—可见定量，应能沿着四个对象往回检查：最终原液浓度来自哪一次稀释，稀释液浓度来自哪条校准线，校准响应来自哪种空白与波长，光强变化又对应怎样的样品状态。若未知读数高于标准范围，就选择合适稀释或光程；若稀释后的谱形改变，就检查化学形态与基质；若全谱呈现明显散射背景，就明确所测对象是溶解部分还是含颗粒总体。一个简单的颜色实验因此可以逐渐发展为有层次的研究方法，每一步都有可以观察和计算的依据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Raja and Barron: UV-Visible Spectroscopy](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Physical_Methods_in_Chemistry_and_Nano_Science_%28Barron%29/04%3A_Chemical_Speciation/4.04%3A_UV-Visible_Spectroscopy)

   吸光关系、常见光路及波段选择。

   CC BY 4.0 page; open further reading.
2. [Agilent: Understanding Your UV-visible Spectroscopy System](https://www.agilent.com/Library/usermanuals/Public/G1115-90041_UnderstandingGP.pdf)

   第 1 章暗信号、参照与吸光度；第 5 章校准与反算。
3. [Shimadzu: What is stray light?](https://www.ssi.shimadzu.com/service-support/faq/uv-vis/resolution-and-stray-light/3/index.html)

   杂散光的定义及高吸收区响应偏差。
4. [Smithsonian: Beckman DU Spectrophotometer](https://americanhistory.si.edu/collections/object/nmah_378)

   1941 年 DU 仪器与石英光学元件的历史记录。
5. [Beckman Foundation: Spectrophotometer](https://www.beckman-foundation.org/about-foundation/inventions/spectrophotometer/)

   仪器发展及紫外分析用途的历史背景。
