# 等温滴定量热：用热量测量分子结合

Source: https://ml-biomat.com/tutorials/experimental-methods/c05/
Language: zh-CN

把逐针热量与分子占据联系起来，读懂亲和力、焓变和实验条件。

## 两个分子是否愿意待在一起，可以从热量问起

一种小分子药物进入蛋白质的结合口袋，或者一个客体进入环糊精的空腔，都会重新安排分子之间以及分子与水之间的相互作用。研究者关心的不只是“能不能结合”，还包括需要多高的浓度才能占据明显数量的位点、每个主体能容纳多少客体，以及结合时释放还是吸收热量。等温滴定量热法，通常简称 ITC，就是沿着热量这条线索观察相互作用的方法。它让两种溶液在控制温度下逐步混合，记录每一次加入带来的微小热效应，再把热量随加入量的变化与结合模型联系起来。

可以把结合想成一间不断有人进入的阅览室：开始时空座很多，新来的人容易找到座位；接近坐满时，继续进门的人更多地停留在走道中。分子的情况多了一层动态性，已结合的分子也会离开，游离分子又会进入，最终形成持续交换的平衡。如果每次形成结合都伴随一定的热变化，那么每次加样新增了多少结合，就会影响这一针的热量。先大的热峰逐渐变小，可能对应位点逐渐被占据；要读懂它，还需要知道混合本身是否产生热、原来的样品是否被稀释，以及仪器怎样把热变化转换成数字。

ITC 很适合把溶液中的亲和力与热力学性质放在一起研究，不需要先给分子加上荧光标记，也不要求把它固定在传感器表面。它所观察的是整个溶液中发生过程的总热效应，因此样品的纯度、活性比例和缓冲条件直接进入解释。材料研究中，比较不同主体对同一客体的结合，能够帮助理解载入与释放；生物研究中，比较蛋白质及其突变体，则可以追问某个结构变化怎样影响相互作用。下面用一套完整的构造数据贯通仪器信号、空白校正、结合模型和参数判断，使每个数字都能回到原来的测量过程。

## 温度几乎不变，为什么仍然能测到热

“等温”容易让人误以为没有热量变化。事实上，保持温度不变常常需要不断补偿能量，就像室内温度稳定时，空调仍可能在工作。ITC 的样品池旁边设有参比池，仪器比较两者的温度，并通过反馈调节加热功率。样品中发生放热过程时，为了维持温差接近零，所需补偿加热会暂时减少；发生吸热过程时，则需要更多补偿。记录下来的原始曲线通常是差分功率随时间的变化，而不是溶液温度不断上升或下降的曲线。功率表示单位时间转移多少能量，热量则是这段时间内转移能量的总和。

1989 年，Wiseman、Williston、Brandts 和 Lin 报道了一种用于快速测量结合常数与结合热的滴定量热仪，并以核糖核酸酶 A 与 2′-CMP 的结合展示测量过程。他们的论文把配对量热池、温差反馈、自动加样和曲线积分连成了一套方法。原文还比较了不同蛋白质浓度下的曲线，说明可提取的信息取决于实验落在怎样的浓度区间。图中的原理示意沿用这一测量逻辑，不复原某台历史仪器的尺寸；右侧则用现代教学模型说明，随配体逐步加入，位点占据比例与配体游离比例为何会以不同方式变化。

![原创配对量热池与反馈原理示意，联系 Wiseman 等 1989 年论文；尺寸不按比例。右图为本章构造的独立位点模型，两条曲线的分母分别是总位点与总配体。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/74670cdd6081d13d1a5a3c88.svg?v=74670cdd6081)

图 1原创配对量热池与反馈原理示意，联系 Wiseman 等 1989 年论文；尺寸不按比例。右图为本章构造的独立位点模型，两条曲线的分母分别是总位点与总配体。

热量刻度还需要独立校准，例如向校准加热器输入已知电能，再比较响应曲线的面积。1989 年论文同时讨论了电校准与化学校准。它们核查仪器怎样把热效应转换成数值；蛋白质浓度、活性比例以及峰对应哪一种过程，则由各自的样品测量与实验设计确定。

一针注射后，溶液混合、结合重新平衡，仪器反馈产生一个随时间展开的峰。峰的高度受到加样速度、混合和仪器响应时间影响，而峰相对于基线的面积对应这一针的热量。基线是没有该次注射扰动时预计的功率轨迹，可能缓慢漂移，并不总是一条水平直线。把曲线与基线之间的差在时间上相加，就是积分。即使暂时不熟悉积分符号，也可以把它理解为把时间切成许多短片段，每片段的功率差乘以持续时间，再把能量贡献累加起来。

$$
q_{\mathrm{obs}}=\int_{t_a}^{t_b}[P(t)-P_0(t)]\,dt,\qquad q_{\mathrm{bind}}=q_{\mathrm{obs}}-q_{\mathrm{blank}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0895523db4c85bc63aa1d0f.svg) | 样品一次注射的基线校正热量，μJ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | 时间及积分起止时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a3409bceea96cdc30708a469.svg) | 样品记录的差分功率，μW。 |
| ![Formula](https://ml-biomat.com/static/agent-math/88d494ac250584df35c39036.svg) | 没有该针扰动时估计的基线功率，μW。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e27726ac854afcaeac389fa8.svg) | 匹配空白的一次注射积分热量，μJ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4db474a27f52f79f2ec60b8e.svg) | 按所设空白校正得到的结合相关热量，μJ。 |

功率乘时间给出能量，面积而非峰高累计热效应。本章放热为负。平均 −2 μW 持续 10 s 得到 −20 μJ；第一针结合约 −22.66 μJ，叠加 +2 μJ 空白后原始积分约 −20.66 μJ。

本章规定放热对应负的热量和向下的功率偏转。若一段 10 s 的平均功率偏转为 −2 μW，贡献的热量就是 −20 μJ，因为 1 W 等于 1 J/s。不同仪器软件可能把放热绘成向上，阅读时应先看符号约定。构造实验第一针的真正结合热约为 −22.66 μJ，同时叠加约 +2 μJ 的混合背景，所以原始峰的面积接近 −20.66 μJ。只有把这两部分分开，才适合讨论每摩尔结合带来的能量变化。参比池负责热学比较，而“配体加入缓冲液”的独立空白实验负责观察混合背景，两者承担不同任务。

## 先数清游离、结合与总量，亲和力才有含义

把待结合的蛋白质记作 M，加入的配体记作 L，形成的复合物记作 ML。配体是结合伙伴的角色名称，可以是小分子、核酸，也可以是另一种蛋白质。最简单的模型假设一个蛋白质对应一个相同且独立的位点，结合和解离持续进行，在固定条件下建立平衡。解离常数 Kᴅ 用平衡时游离两方浓度的乘积除以复合物浓度来描述这个平衡。在同样温度、溶剂和模型定义下，较小的 Kᴅ 对应较低的游离配体浓度就能获得明显占据。因此比较亲和力时，浓度单位和实验条件应与数值一起出现。

$$
K_d=\frac{[M][L]}{[ML]},\qquad \theta=\frac{[ML]}{[M]+[ML]}=\frac{[L]}{K_d+[L]}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | 固定条件下单一独立位点的解离常数，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3124bff73534c41429e32897.svg) | 游离蛋白质浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dca9e27d90e6205901ab6f2.svg) | 游离配体浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6710b6da8dfbf55836dd7325.svg) | 复合物浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 已占据的蛋白质位点比例，无量纲。 |

平衡关系与蛋白质总量守恒共同给出占据公式。Kᴅ=1 μM、游离配体 1 μM 时 θ=0.5；蛋白质总浓度 20 μM 时，结合配体 10 μM，总配体需要 11 μM。

最容易记住的一点是，单一独立位点模型中，游离配体浓度等于 Kᴅ 时，位点占据一半。这里的“游离”不能省略。假设蛋白质总浓度是 20 μM、Kᴅ 是 1 μM，当一半蛋白质结合时，已有 10 μM 配体进入复合物，溶液中还需保留 1 μM 游离配体，所以总配体浓度为 11 μM。若把总浓度 1 μM 直接代入游离浓度公式，就会凭空多算许多可供结合的分子。μM 是微摩尔每升；它描述分子数对应的物质的量浓度，而不是质量浓度。换算蛋白质质量时，还需要其摩尔质量。

ITC 常把相当数量的配体结合起来，所以程序必须同时满足总量守恒与平衡关系。给定总位点浓度和总配体浓度，减去已经形成的复合物，就分别得到剩余游离位点和游离配体。把这些关系代入解离常数定义，会得到一个二次方程。两个数学根中，应选取让复合物浓度不超过任一方总量、并在没有配体时归零的那个根。这个选择有清楚的物理意义：模型不能结合比实际加入更多的配体，也不能制造不存在的位点。程序使用与下式等价、数值上较稳定的写法，减少很弱结合时相近数字相减带来的精度损失。

$$
S_T=nM_T,\qquad B=\frac{S_T+L_T+K_d-\sqrt{(S_T+L_T+K_d)^2-4S_TL_T}}{2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f0fe5be3234907cb3e30d80.svg) | 总独立位点浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 每个蛋白质的有效独立位点数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/92c1a28876c2005bfabddc66.svg) | 蛋白质总浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4bd6f81ef8f52025128f11e2.svg) | 配体总浓度，游离加结合，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | 每类相同独立位点的解离常数，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 结合配体浓度，μM。 |

由 KᴅB=(Sₜ−B)(Lₜ−B) 的二次方程取较小根，确保结合量不超过任一总量。Sₜ=20、Lₜ=11、Kᴅ=1 μM，B=10 μM。不同位点或协同作用需要相应平衡模型。

物质的量可以理解为一种数分子的计量方式，一摩尔对应约 6.022×10²³ 个指定粒子。把浓度乘以体积，就得到池内实际有多少摩尔：20 μM 蛋白质装在 200 μL 池中，对应 4 nmol。若蛋白质摩尔质量为 50,000 g/mol，质量浓度就是 1 mg/mL，池内约有 0.2 mg 蛋白质。这个换算能把“需要多高浓度”转成准备样品时实际要消耗多少材料。对于昂贵或难以纯化的样品，改变池体积可以减少用量，但热量总信号也会随参加过程的分子数量变化。

总量还会在每次加样后变化。教学程序采用明确的离散混合过程：从充分混合的 200 μL 池中先移走 2 μL，再加入 2 μL、浓度为 300 μM 的配体溶液。因此每针保留原有组分的 99%，同时加入 0.6 nmol 配体；25 针之后，初始 20 μM 蛋白质降到约 15.56 μM。真实满池仪器在注射过程中连续置换液体，通常使用对应的体积校正模型。这个例子把移出与加入分成两步，便于逐针核对守恒，并由“本针平衡后的结合量”减去“移出后留下的原有结合量”计算新形成的结合。

$$
r=1-\frac{v}{V_0},\quad M_j=rM_{j-1},\quad L_j=rL_{j-1}+(1-r)L_s,\quad q_j=V_0\Delta H(B_j-rB_{j-1})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 取出并补回后，原有物质的保留比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 每针先取出再补回的体积，L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | 保持固定的池体积，L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 针次编号，正整数；j=0 表示初始状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f3f75911c33257cfd1ffbd74.svg) | 本针及前针结束后的蛋白质总浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa1a2468e58547721f470bd0.svg) | 本针及前针结束后的配体总浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/56d0edb2c8fe78865b80653e.svg) | 注射溶液配体浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0d29cc80036a5952d1a46d56.svg) | 本针及前针平衡后的结合配体浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | 每摩尔新结合的焓变，J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06a99ed1ee9cf7423b7ab887.svg) | 本针的结合热量，J。 |

离散模型先移出充分混合溶液，再补入配体并平衡。200 μL 池每次取出 2 μL，r=0.99；25 针后 20 μM 蛋白质变为约 15.556 μM。300 μM 配体每针加入 0.6 nmol。代码用 μL、μM、kJ/mol，并乘 0.001 转为 μJ。

保留的复合物这一项可以帮助核查计算。随取样移出的复合物只是离开量热池，并不是在池内重新发生了解离。若直接减去上一针结束时的全部结合量，就会把这部分物质转移误记成化学吸热。先扣除移出的部分，再比较新平衡形成多少结合，才能让物质守恒和反应热对应同一个过程。

## 把实验做在曲线能够说话的区间

设想用一杯蛋白质溶液去接住一针针配体。如果亲和力非常强，几乎每个加入的分子都立即被占位，直到突然接近饱和；曲线会很像一个台阶。这样容易看出总容量与每摩尔的热量，但不同的极强亲和力可能产生几乎相同的台阶。如果结合很弱，多数配体始终游离，热量变化平缓，曲线也不容易区分位点数、亲和力和焓变。中间区间的弯曲形状提供了更多相互区分的信息。实验设计因而需要让起始段、过渡段和接近饱和的后段都得到合适的采样，而不是只追求最大的第一个峰。

$$
c=\frac{nM_0}{K_d}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 初始浓度与亲和力构成的设计参数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 有效相同独立位点数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | 池中初始蛋白质总浓度，μM。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | 解离常数，使用与 M₀ 相同的浓度单位。 |

位点浓度相对于解离常数决定滴定过渡形状。n=1、M₀=20 μM、Kᴅ=1 μM 时 c=20；Kᴅ=100 或 0.01 μM 分别给出 c=0.2 或 2000。可提取信息还取决于热量和噪声。

常用的 c 值把起始位点浓度与解离常数联系起来。它是无量纲的实验设计指标；本例一个蛋白质一个位点，初始蛋白质 20 μM、Kᴅ 1 μM，因此 c=20。图中保持其他设置相同，比较 c=0.2、20 和 2000：小 c 曲线浅而平，大 c 曲线近似阶跃，中间曲线有明显过渡。具体可用范围还取决于热量大小、噪声、溶解性和样品消耗。若把浓度降低以展开很强结合的过渡，也会同时减小热信号；若把浓度升高以观察弱结合，还要检查聚集或非特异相互作用是否出现。c 值帮助安排实验，并不替代样品状态的判断。

![构造设计诊断。A 固定初始蛋白质 20 μM、n=1、焓变 −40 kJ/mol，改变 Kᴅ 得到三种 c 值。B 固定 n=1，颜色为逐针热量的均方根残差，白叉为该网格最小值；色块不是置信区间。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ce7965441529646d3007b375.svg?v=ce7965441529)

图 2构造设计诊断。A 固定初始蛋白质 20 μM、n=1、焓变 −40 kJ/mol，改变 Kᴅ 得到三种 c 值。B 固定 n=1，颜色为逐针热量的均方根残差，白叉为该网格最小值；色块不是置信区间。

浓度核对尤其值得花时间。蛋白质的总浓度与真正具有结合活性的浓度可能不同，部分变性或聚集会让可用位点减少。拟合中的位点数 n 也可能吸收浓度误差，得到 0.8 并不等于每个分子真的长着“八成个口袋”。可以比较不同制备批次、独立测定浓度、检查蛋白质状态，或交换注射池与样品池的角色，观察这些实验能否由一致的模型解释。上一节的电泳有助于检查组分与降解，尺寸排阻可以进一步观察溶液中的聚集状态；它们为量热模型提供的是样品层面的约束。

另一个重点是两种溶液的缓冲条件。即使不发生目标结合，盐浓度、pH 或溶剂比例的差别也可能在混合时产生热。尽量使用匹配的缓冲液，并测量配体加入相应缓冲液的空白，能把这类贡献单独观察出来。混合背景随浓度变化时，应按针次或适当模型处理，而不总是扣去一个任意常数。气泡、沉淀、进样不完整和较慢的回到基线过程，也可以从原始曲线中留下线索。第一针是否适合参与拟合，应结合实际加样记录和曲线检查；本章的构造实验没有人为设置第一针异常，因此完整保留它。

## 从一串热峰，走到可以核查的结合参数

完整示例设置 25 次注射，每针之间相隔 180 s，并分别生成样品与配体空白的原始功率曲线。两条曲线都包含缓慢漂移的基线与固定种子的随机噪声。程序从各针尾部和加样前的安静区段拟合基线，再积分每一针的面积。尾部是否已充分回到基线，是选择这些区段的前提；若过程很慢而尾部仍含有反应信号，拟合就会把一部分真实热量当成背景。图中放大第一针，使读者可以同时看到向下的样品峰、向上的空白峰和积分的面积，而不必只面对最后的拟合参数表。

![全部为构造数据，随机种子 650。样品与空白有独立功率噪声；每针 2 μL、间隔 180 s、25 针。A、B 显示原始功率及基线，C 除以每针 0.6 nmol 配体，D 残差为校正数据减模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/28d0443f9203a72bd026f5dd.svg?v=28d0443f9203)

图 3全部为构造数据，随机种子 650。样品与空白有独立功率噪声；每针 2 μL、间隔 180 s、25 针。A、B 显示原始功率及基线，C 除以每针 0.6 nmol 配体，D 残差为校正数据减模型。

基线误差虽然看起来只是曲线很小的上下移动，积分后却可能相当可观。如果在 180 s 的区间里把基线整体估高 0.001 μW，计算的热量就会偏移 −0.18 μJ。这个数已经大于本例约 0.066 μJ 的拟合残差均方根。因此，选择哪一段作为基线、是否使用随时间变化的背景，应从原始功率轨迹和实验过程出发；根据自己期待的结合常数去反复移动基线，会让数据处理悄悄改变研究问题的答案。完整保存功率、基线和积分窗口，可以直接比较几种有物理依据的处理选择影响多大。

把样品每针热量减去相应空白热量后，再除以该针加入的配体物质的量，就得到常见的归一化滴定曲线。单位换算在这里很有帮助：1 μJ 除以 1 nmol 等于 1 kJ/mol。本例每针加入 0.6 nmol，第一针约 −22.66 μJ 的结合热，对应约 −37.77 kJ/mol 加入配体。这个数略小于设定的结合焓绝对值 40 kJ/mol，因为第一针加入的配体并没有全部形成新结合。后段多数位点已被占据，每针新形成的结合越来越少，所以归一化热量逐渐接近零。

程序实际拟合的是逐针热量，调整解离常数、焓变和有效位点数，使模型与数据之间的平方偏差尽量小。构造真值是 Kᴅ=1 μM、焓变 −40 kJ/mol、n=1；从带噪声功率数据反算得到约 0.995 μM、−39.97 kJ/mol 和 1.000。若省略空白扣除，在同样的拟合设置下会得到约 0.420 μM 和 −34.13 kJ/mol。这一比较说明，拟合程序即使能够返回整齐的数字，也会把未处理的实验贡献解释为模型参数的变化。真正需要检查的是输入模型的热量是否对应了所研究的过程。

残差是数据减去模型的差。把它按针次画出来，可以观察偏差是否在过渡段连续同向、是否尾段仍有趋势，或是否只有一针特别异常。参数误差图则进一步展示不同 Kᴅ 与焓变组合会产生多大的残差：沿着倾斜低谷移动时，一个参数的改变可被另一个参数部分补偿。图中固定 n=1，只显示这一条件下的均方根残差，并不把色块直接解释成置信区间。程序另做 80 次固定噪声水平的重新拟合，记录噪声造成的参数波动；浓度误差、批次差异和模型选择需要通过相应实验另行进入不确定性分析。

## 热量、亲和力与熵，分别回答什么

结合放出的热越多，是否就一定结合得越牢？把焓变与自由能放在同一张图上，就能看出它们描述的侧面不同。焓变与固定压力下过程的热效应相关；标准结合自由能则把平衡常数转成统一的能量表达。熵涉及可访问微观状态的统计，既包含分子本身，也包含周围溶剂。结合可能限制分子的构象和相对运动，同时释放原先受限的水分子；这些贡献共同进入总的熵变化。把熵简单等同于肉眼看见的“混乱程度”，很难解释溶液中的分子结合。

$$
\Delta G^\circ=RT\ln\!\left(\frac{K_d}{c^\circ}\right)=\Delta H^\circ-T\Delta S^\circ
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9824e74d6293e33988b52fed.svg) | 标准摩尔结合自由能变化，J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 气体常数，8.314462618 J/(mol·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | 以 mol/L 表示的解离常数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c2b399340d1e66a535bf58cf.svg) | 标准浓度，1 mol/L，使对数内比值无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e230c0e277e7c47581e0b74.svg) | 标准摩尔结合焓变，J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e61a5fff73bfe0205f88db4f.svg) | 标准摩尔结合熵变，J/(mol·K)。 |

在所选溶液条件的理想稀溶液浓度近似中，平衡常数转换为标准自由能。T=298.15 K、Kᴅ=10⁻⁶ mol/L，ΔG°≈−34.248 kJ/mol；若 ΔH°=−40 kJ/mol，ΔS°≈−19.292 J/(mol·K)。

温度 298.15 K、Kᴅ=1 μM 时，以 1 mol/L 为标准浓度，标准结合自由能约为 −34.25 kJ/mol。若焓变为 −40 kJ/mol，那么 −TΔS° 约为 +5.75 kJ/mol，即这个模型的熵项抵消了一部分有利焓项。另一个体系可以具有相同 Kᴅ，但焓变只有 −20 kJ/mol，此时需要更有利的熵项，使两者仍相加为同一个自由能。图中这两个体系是为了比较而构造的，不对应两种指定药物。它们说明，亲和力相同并不意味着量热曲线的幅度相同，也说明不能仅凭一个放热峰的大小排列结合强弱。

![构造热力学比较。A 两个体系 Kᴅ 同为 1 μM、温度 298.15 K，标准自由能相同而焓和熵项不同。B 对同一个 Kᴅ，分别以游离和总配体浓度作为横轴；20 μM 蛋白质半占据时，总配体需 11 μM。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0a934aed0166f9faa0728850.svg?v=0a934aed0166)

图 4构造热力学比较。A 两个体系 Kᴅ 同为 1 μM、温度 298.15 K，标准自由能相同而焓和熵项不同。B 对同一个 Kᴅ，分别以游离和总配体浓度作为横轴；20 μM 蛋白质半占据时，总配体需 11 μM。

公式中的标准态也有具体作用。对有单位的 Kᴅ，先除以标准浓度，再取自然对数，才能得到无量纲的对数自变量。负的标准自由能描述这一标准态定义下的结合倾向；实际溶液能否达到较高占据，还取决于游离浓度。平衡时正反过程仍然发生，宏观组成不再持续改变。另一方面，Kᴅ 描述平衡关系，并不单独告诉我们一个复合物能停留多久。两个体系可能有相似的平衡亲和力，却具有不同的结合与解离速率；后续的表面等离子体共振可以沿时间维度继续追问这一差别。

溶液中的热量还可能包含与结合相连的质子交换。如果形成复合物时分子吸收或释放质子，缓冲液也参与相应的吸放热过程；测得焓变于是与缓冲体系有关。配体加入缓冲液的普通稀释空白，处理的是缺少结合伙伴时的混合背景，而结合引发的质子交换仍与目标过程共同发生。比较相同 pH、不同电离焓的缓冲体系，可以进一步研究这种联系。这个认识也使热力学解释更具体：焓变是指定溶液条件下整个相关过程的结果，不能只凭符号把它拆成若干个氢键，或直接认定某一种微观作用占主导。

交互把解离常数、焓变和蛋白质浓度分别作为可调参数。先固定焓变，只改变 Kᴅ，观察过渡形状和 c 值；再固定 Kᴅ，只改变焓变，观察热量幅度和方向。即使把焓变调为正值，体系仍可保持同一个有利的标准结合自由能，此时熵项需要作出相应贡献。最后改变蛋白质浓度，思考曲线形状与样品消耗如何一起变化。把三个影响分开操作，能帮助读者辨认一条滴定曲线中究竟有哪些独立的信息。

当某种温度和缓冲条件下的结合焓接近零时，明显结合也可能只产生很小的热信号。此时可使用其他可观察量测定占据变化，再通过温度或缓冲条件系列研究热量平衡。交互允许焓变穿过零点，同时保留结合平衡模型，正是为了区分“分子处于什么状态”和“用什么信号看见它”。

## 分别改变亲和力、热量与浓度

一类独立位点 n=1；池体积 200 μL，每针先取出再补入 2 μL，共 25 针。注射液浓度为初始蛋白质的 15 倍。曲线已扣除空白，纵轴按加入配体量归一化；温度 298.15 K。

[Figure: 相互独立调节亲和力焓变浓度的滴定曲线](https://ml-biomat.com/tutorials/experimental-methods/c05/#C05-plot)

## 把测量过程保留在完整分析里

下面的完整程序同时保留原始功率曲线、拟合基线、每针积分、空白热量以及模型预测。构造数据使每一步都能与已知真值对照：先检查质量守恒，再检查热量归一化，最后检查参数能否从噪声中恢复。响应峰采用具有上升和衰减过程的形状，并在离散时间上归一化，使面积精确对应指定热量。这个响应模型用于解释仪器如何把热量铺展到时间轴上；判断真实过程的快慢时，还需要把仪器响应与实际反应动力学分开。

### 完整功率曲线、逐针校正与结合拟合

固定种子构造样品与空白功率，积分并校正，再拟合独立位点模型，输出原始数组、参数误差地形与噪声重拟合。

```
"""Constructed ITC experiment with explicit discrete withdrawal/replacement mixing."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

def titration(kd=1.,enthalpy=-40.,sites=1.,protein=20.,ligand=300.,cell=200.,injection=2.,number=25):
 """uM, kJ/mol, uL -> microjoules. Remove a mixed aliquot, then replace it."""
 retain=1-injection/cell;M=protein;L=0.;bound=0.;rows=[]
 for j in range(number):
  M*=retain;L=L*retain+ligand*injection/cell;S=sites*M
  # Stable quadratic root; avoids subtraction cancellation at weak binding.
  B=2*S*L/(S+L+kd+np.sqrt((S+L+kd)**2-4*S*L))
  q=cell*.001*enthalpy*(B-retain*bound)
  rows.append([j+1,M,L,B,q,L/M]);bound=B
 return np.array(rows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 truth=titration();q=truth[:,4];ratio=truth[:,5];rng=np.random.default_rng(650);time=np.arange(26*180,dtype=float);baseline=.08+.000015*time
 power=baseline.copy();blank=baseline.copy();pulse_t=np.arange(180,dtype=float);kernel=pulse_t/12**2*np.exp(-pulse_t/12);kernel/=np.trapezoid(kernel,pulse_t)
 dil=2+.02*np.arange(25)
 for i in range(25):
  sl=slice((i+1)*180,(i+2)*180);power[sl]+=(q[i]+dil[i])*kernel;blank[sl]+=dil[i]*kernel
 power+=rng.normal(0,.004,time.size);blank+=rng.normal(0,.004,time.size)
 quiet=(time<170)|((time%180)>=150);basefit=np.polyval(np.polyfit(time[quiet],power[quiet],1),time);blankfit=np.polyval(np.polyfit(time[quiet],blank[quiet],1),time)
 measured=[];control=[]
 for i in range(25):
  sl=slice((i+1)*180,(i+2)*180);measured.append(np.trapezoid(power[sl]-basefit[sl],time[sl]));control.append(np.trapezoid(blank[sl]-blankfit[sl],time[sl]))
 measured=np.array(measured);control=np.array(control);corrected=measured-control
 def fit(data):
  fun=lambda v:titration(np.exp(v[0]),v[1],v[2])[:,4]-data
  out=least_squares(fun,[0,-40,1],bounds=([-6,-150,.4],[5,-1,2]),xtol=1e-12,ftol=1e-12,gtol=1e-12)
  return np.array([np.exp(out.x[0]),out.x[1],out.x[2]])
 fitted=fit(corrected);pred=titration(*fitted)[:,4];wrong=fit(measured);rms=float(np.sqrt(np.mean((pred-corrected)**2)))
 # Independent parametric noise exercise, not variation among biological specimens.
 boots=np.array([fit(pred+rng.normal(0,.08,25)) for _ in range(80)]);ci=np.percentile(boots,[2.5,97.5],axis=0)
 f,ax=plt.subplots(1,2,figsize=(13.5,5.4),layout='constrained')
 ax[0].set(xlim=(0,10),ylim=(0,8));ax[0].axis('off');ax[0].set_title(T('A  1989：配对量热池与功率反馈','A  1989: Matched cells and power feedback'),loc='left')
 ax[0].add_patch(Rectangle((.6,1.4),8.8,4.3,fc='#e6edf0',ec=B,lw=2))
 for x,c,label in [(2.5,B,T('参比池','Reference')),(7,R,T('样品池','Sample'))]:
  ax[0].add_patch(Circle((x,3.4),1.25,fc='#fcfbf7',ec=c,lw=2));ax[0].text(x,3.4,label,ha='center',va='center');ax[0].plot([x-.6,x+.6],[2.8,2.8],c=Y,lw=4)
 ax[0].plot([7,7],[4.7,7.2],c=R,lw=3);ax[0].add_patch(Rectangle((6.6,6.3),.8,.9,fc='#f4d5cb',ec=R));ax[0].annotate('',xy=(7,4.8),xytext=(7,6),arrowprops={'arrowstyle':'->','color':R})
 ax[0].text(5,7.5,T('逐针加入结合伙伴','Inject binding partner'),ha='center');ax[0].annotate('',xy=(5.7,3.4),xytext=(3.8,3.4),arrowprops={'arrowstyle':'<->','color':G});ax[0].text(4.75,4,T('温差','ΔT'),ha='center');ax[0].text(5,.6,T('放热 → 补偿加热减少；积分得到热量','Heat release → less heater power; integrate for heat'),ha='center',fontsize=10)
 ax[1].set_title(T('B  加入的分子：先占位，后积累','B  Added molecules: Occupy, then accumulate'),loc='left');ax[1].plot(ratio,truth[:,3]/truth[:,1],c=R,lw=2,label=T('位点占据比例','Fraction of sites occupied'));ax[1].plot(ratio,(truth[:,2]-truth[:,3])/truth[:,2],c=B,lw=2,label=T('配体中游离的比例','Fraction of ligand free'));ax[1].set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('比例','Fraction'),ylim=(0,1.05));ax[1].legend(loc='lower right');ax[1].text(.48,.35,T('Kᴅ = 1 μM；初始蛋白质 20 μM\n构造的一类独立位点模型','Kᴅ = 1 μM; initial protein 20 μM\nConstructed independent-site model'),transform=ax[1].transAxes,fontsize=10)
 save(f,'feedback-binding')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.2),layout='constrained');ax=axes[0,0];ax.plot(time/60,power,c=B,lw=.8,label=T('样品','Sample'));ax.plot(time/60,blank,c=Y,lw=.7,label=T('配体 → 缓冲液','Ligand → buffer'));ax.plot(time/60,basefit,c='#60717c',ls='--',lw=1,label=T('拟合基线','Fitted baseline'));ax.set(xlabel=T('时间 / min','Time / min'),ylabel=T('差分功率 / μW','Differential power / μW'),title=T('A  原始功率：放热向下','A  Raw power: Exothermic downward'));ax.legend(fontsize=9)
 ax=axes[0,1];sl=slice(180,360);ax.plot(pulse_t,power[sl],c=B,label=T('第一针','First injection'));ax.plot(pulse_t,basefit[sl],c='#60717c',ls='--');ax.fill_between(pulse_t,power[sl],basefit[sl],color=B,alpha=.18);ax.plot(pulse_t,blank[sl],c=Y,label=T('空白','Blank'));ax.set(xlabel=T('注射后时间 / s','Time after injection / s'),ylabel=T('差分功率 / μW','Differential power / μW'),title=T('B  面积是热量；峰高还受响应时间影响','B  Area gives heat; height also depends on response'));ax.legend()
 ax=axes[1,0];mol_in=.6;ax.scatter(ratio,measured/mol_in,s=19,color=Y,label=T('未扣除空白','Before blank correction'));ax.scatter(ratio,corrected/mol_in,s=19,color=B,label=T('已扣除空白','Blank-corrected'));ax.plot(ratio,pred/mol_in,c=R,label=T('拟合','Fit'));ax.set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('每摩尔加入配体的热量 / kJ/mol','Heat per mole of injected ligand / kJ/mol'),title=T('C  校正、归一化、拟合','C  Correct, normalize and fit'));ax.legend(fontsize=9)
 ax=axes[1,1];ax.axhline(0,c='#60717c',lw=1);ax.plot(np.arange(1,26),corrected-pred,'o-',c=G);ax.set(xlabel=T('针次','Injection'),ylabel=T('数据 − 模型 / μJ','Data − model / μJ'),title=T('D  残差是否留下系统形状','D  Does a systematic pattern remain?'))
 save(f,'thermogram-analysis')
 f,axes=plt.subplots(1,2,figsize=(13.4,5.4),layout='constrained');ax=axes[0]
 for kd,c in [(100,Y),(1,B),(.01,R)]:
  row=titration(kd);ax.plot(row[:,5],row[:,4]/.6,color=c,label=f'c = {20/kd:g}')
 ax.set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('热量 / 加入配体量 / kJ/mol','Heat / injected ligand amount / kJ/mol'),title=T('A  平缓、可弯曲、近似阶跃','A  Shallow, curved and nearly step-like'));ax.legend();ax.text(.48,.45,T('所有曲线：ΔH = −40 kJ/mol\n位点数 n = 1','All curves: ΔH = −40 kJ/mol\nSite number n = 1'),transform=ax.transAxes,fontsize=10)
 kds=np.geomspace(.5,2,61);hs=np.linspace(-44,-36,61);err=np.array([[np.sqrt(np.mean((titration(k,h,1)[:,4]-corrected)**2)) for k in kds] for h in hs]);ax=axes[1];im=ax.pcolormesh(kds,hs,err,cmap='viridis_r',shading='auto');ax.set_xscale('log');ij=np.unravel_index(np.argmin(err),err.shape);ax.scatter(kds[ij[1]],hs[ij[0]],marker='x',c='white',s=80);ax.set(xlabel=T('解离常数 Kᴅ / μM','Dissociation constant Kᴅ / μM'),ylabel=T('焓变 ΔH / kJ/mol','Enthalpy ΔH / kJ/mol'),title=T('B  固定 n=1 的条件误差地形','B  Conditional error landscape with n=1'));f.colorbar(im,ax=ax,label=T('均方根残差 / μJ','RMS residual / μJ'))
 save(f,'design-diagnostics')
 gas=.00831446261815324;temperature=298.15;dg=gas*temperature*np.log(1e-6);f,axes=plt.subplots(1,2,figsize=(13.4,5.4),layout='constrained');ax=axes[0];positions=np.arange(3)
 for j,h in enumerate([-40,-20]):ax.bar(positions+(j-.5)*.32,[dg,h,dg-h],.30,color=[B,R][j],label=T(f'体系 {j+1}',f'System {j+1}'))
 ax.set_xticks(positions,['ΔG°','ΔH°','−TΔS°']);ax.axhline(0,c='#61758a',lw=1);ax.set(ylabel=T('摩尔能量 / kJ/mol','Molar energy / kJ/mol'),title=T('A  同一亲和力，可以有不同的热量','A  Same affinity, different heat'));ax.legend();ax.text(.04,.92,T('Kᴅ = 1 μM；T = 298.15 K','Kᴅ = 1 μM; T = 298.15 K'),transform=ax.transAxes,fontsize=10)
 ax=axes[1];L=np.geomspace(.01,200,250);M=20.;bound=2*M*L/(M+L+1+np.sqrt((M+L+1)**2-4*M*L));ax.semilogx(L,L/(1+L),c=B,label=T('横轴作为游离浓度','Axis interpreted as free concentration'));ax.semilogx(L,bound/M,c=R,label=T('横轴作为总浓度，蛋白质20 μM','Axis is total concentration; protein 20 μM'));ax.axhline(.5,c='#61758a',ls='--');ax.scatter([1,11],[.5,.5],c=[B,R],zorder=3);ax.set(xlabel=T('所采用的配体浓度 / μM','Specified ligand concentration / μM'),ylabel=T('位点占据比例','Fraction occupied'),title=T('B  游离配体与总配体是不同的横轴','B  Free ligand and total ligand differ'));ax.legend(fontsize=9,loc='upper left')
 save(f,'thermodynamics')
 np.savetxt(a.output/'thermogram.csv',np.c_[time,power,blank,basefit,blankfit],delimiter=',',header='time_s,sample_power_uW,blank_power_uW,sample_baseline_uW,blank_baseline_uW',comments='')
 np.savetxt(a.output/'injections.csv',np.c_[truth,measured,control,corrected,pred],delimiter=',',header='injection,protein_total_uM,ligand_total_uM,bound_uM,true_heat_uJ,molar_ratio,measured_heat_uJ,blank_heat_uJ,corrected_heat_uJ,fitted_heat_uJ',comments='')
 np.savetxt(a.output/'noise_refits.csv',boots,delimiter=',',header='Kd_uM,enthalpy_kJ_per_mol,site_number',comments='')
 summary={'fitted_Kd_uM':float(fitted[0]),'fitted_enthalpy_kJ_per_mol':float(fitted[1]),'fitted_site_number':float(fitted[2]),'RMS_residual_uJ':rms,'uncorrected_fit_Kd_uM':float(wrong[0]),'uncorrected_fit_enthalpy_kJ_per_mol':float(wrong[1]),'initial_c_value':20.,'standard_free_energy_kJ_per_mol':float(dg),'entropy_J_per_mol_K':float((-40-dg)/temperature*1000),'final_protein_uM':float(truth[-1,1]),'first_binding_heat_uJ':float(q[0]),'last_binding_heat_uJ':float(q[-1]),'injected_ligand_nmol':.6,'half_occupancy_free_ligand_uM':1.,'half_occupancy_total_ligand_uM_at_20uM_protein':11.,'noise_refit_95_percentile_interval':{'Kd_uM':ci[:,0].tolist(),'enthalpy_kJ_per_mol':ci[:,1].tolist(),'site_number':ci[:,2].tolist()}}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

80 次噪声重拟合回答的是一个具体问题：如果模型和浓度正确，而逐针热量具有设定的随机波动，参数会怎样变化。导出的分位数区间只对应这种计算定义。独立制备的样品还包含组成与活性差别，同一制备的重复滴定则处于另一层次；在误差条旁写明重复类型，能让读者理解它支持哪一种实验判断。

用自己的数据替换时，先确认功率与时间的单位、放热方向、实际注射体积和有效池体积，然后建立适合该仪器的置换校正。有效池体积参与浓度与热量计算，装载液体的总体积还可能包含池口和填充余量，两者不应混用。接着检查原始峰是否完整、注射间隔是否足够，再决定基线和空白处理方式。已经处理好的每针热量也可以作为输入，但保留原始轨迹有助于解释异常点。模型增加第二类位点前，可以先比较残差、浓度系列和独立样品状态，确认新增参数对应一个有实验依据的问题。

如果目标是比较两种材料主体对同一客体的结合，可以在一致温度、溶剂条件下测量，并把位点浓度的定义写清楚：是按单个主体、重复单元，还是独立可用的结合位点计算。对于多价聚合物和颗粒，多个接触、协同作用及聚集可能使简单独立位点模型不足以描述整个过程。可以先用浓度系列寻找可重复的曲线变化，再选择结构或粒径测量来区分结合与组装。若只是想获得某个范围内的经验热响应，则保持测量定义清楚，也能服务于配方比较；研究问题决定需要把模型推进到多细。

完成一次分析后，下一步最有价值的实验通常来自当前曲线缺少的信息。过渡太陡时可调整浓度或安排竞争滴定；信号太小而样品状态稳定时，可重新设计浓度与注射量；n 值随批次变化时，优先核查浓度和活性组分。比较不同实验时，同时保存温度、缓冲液、浓度测定方法、样品处理与重复类型。这样得到的亲和力和焓变就不再是脱离条件的一串数字，而能与分子结构、材料配方和后续的结合动力学实验相互连接。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Wiseman et al. (1989): Rapid measurement of binding constants and heats of binding](https://web.iitd.ac.in/~nkurur/2012-13/Isem/cyl501/analbiochem179_131.pdf)

   原始配对池、功率反馈、曲线积分和浓度设计。
2. [Harvard CMI: Isothermal titration calorimetry](https://cmi.hms.harvard.edu/isothermal-titration-calorimetry)

   样品和参比、匹配缓冲条件与浓度准备。
3. [TA Instruments: Quick Start ITC, MCAPN-2016-1](https://www.tainstruments.com/pdf/literature/MCAPN-2016-1.pdf)

   功率符号、有效池体积与装载体积。
4. [Malvern: Best practices for ITC, Part 1](https://www.malvernpanalytical.com/en/learn/knowledge-center/insights/best-practices-for-isothermal-titration-calorimetry-to-study-binding-interactions-part-1)

   c 值与样品状态、缓冲液匹配。
5. [TA Instruments: Protein-protein interactions by ITC, MC176](https://www.tainstruments.com/applications-notes/characterizing-protein-protein-interactions-by-itc-mc176/)

   结合热、溶剂和质子交换的关联。
6. [Brautigam et al. (2016): Integration and Global Analysis of ITC Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC7466939/)

   基线、全局分析、浓度与 n 值混淆。
