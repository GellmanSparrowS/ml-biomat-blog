# 荧光光谱：亮度、寿命与分子环境

Source: https://ml-biomat.com/tutorials/experimental-methods/s04/
Language: zh-CN

同样变暗的样品，可能少了分子，也可能改变了分子的能量去路。把强度、寿命与光路放在一起判断。

## 一管样品更亮了，是分子变多了，还是每个分子更会发光

荧光笔划过纸面，在适当的光照下会显得特别明亮；实验室里，带荧光标记的蛋白质、细胞和颗粒也可以从背景中显现出来。这种亮度来自样品吸收光之后重新发出的光。把激发光和发射光按颜色分开，就能在较低背景上观察目标，因此荧光适合检测少量物质。它还能报告分子周围的环境：有些探针遇到特定离子后变亮，有些在更黏稠的环境中发光更有效，有些蛋白质的内源荧光会随折叠状态变化。一个光信号于是既可能表示“有多少”，也可能表示“处在什么状态”。

这两种用途需要从一开始就分清。假设两管溶液中荧光分子数量相同，其中一管加入了能够让激发态更快失去能量的物质，亮度就可能下降。反过来，即使分子数量减少，环境变得更有利于发光，也可能让总亮度保持不变。仪器的光源、滤光片、狭缝和探测增益还会改变记录值。因此，本篇先解释一个分子从吸光到发光经历的过程，再比较强度、量子产率和寿命三种读数。它们分别回答收到多少光、吸收后多大比例发光，以及激发态平均维持多久。

贯穿本篇的实验问题是：加入另一种分子后，荧光为什么变弱？我们会比较浓度减少、动态猝灭和光学遮挡三种情况。它们都可能降低稳态强度，时间分辨读数却会给出不同线索。完整程序构造有已知寿命的光子计数衰减，加入仪器时间响应和背景，再从曲线中拟合寿命。另一组计算展示高浓度下的内滤效应。图中的模型数据会明确标注；绿色荧光蛋白的结构图则由真实公开晶体结构坐标重新绘制，让分子环境的讨论连接到可检查的空间结构。

对于生物材料，荧光常把许多尺度连起来。分子探针在水凝胶中的分布可以显示输运，标记蛋白质可以帮助观察吸附，带环境敏感基团的聚合物可以把局部变化转化为颜色或寿命变化。做这些实验时，需要同时询问标记是否改变了所研究对象。例如，疏水染料可能改变蛋白质或载体与界面的相互作用，游离染料也可能比真正被标记的对象扩散得更快。把游离染料、未标记材料和已标记对象分别设置对照，有助于让光信号追踪的是研究对象，而不只是染料自己的行为。

## 从荧光的命名到绿色荧光蛋白：发光中心需要怎样的环境

1852 年，George G. Stokes 用“荧光”这一名称讨论光被吸收后以不同颜色发出的现象。这个历史问题与今天的滤光设计直接相连：发出的光通常比有效激发它的光波长更长，因此可以筛掉较短波长的激发光，再观察发射。后来，荧光染料与特定生物分子的结合，把“哪里有会发光的物质”进一步变成“哪里有某种目标”。这种改变需要的不只是明亮染料，还包括能够把染料放到正确位置的识别与标记化学。理解光学和生物识别两部分，才能理解一张荧光图中的亮点代表什么。

绿色荧光蛋白提供了另一条路线：让蛋白质自身形成发光中心。1996 年公布的 GFP 结构研究展示了一个由 β 折叠围成的桶状结构，中央区域容纳由蛋白质自身残基形成的发色团。下面使用 PDB 条目 1EMA 的真实坐标绘制主链走向和发色团位置。这个条目是研究用 GFP 变体的晶体结构，分辨率为 1.90 Å；它提供的是空间结构，不是本篇数值衰减曲线的实验来源。把两种证据分清，可以用结构理解环境，同时保留时间测量各自的含义。

![PDB 1EMA 的真实晶体结构坐标经主轴投影形成两幅视图。颜色沿链序变化，红点是 CRO 发色团原子；链中缺口不连接。该工程化 GFP 结构发表于 1996 年，分辨率 1.90 Å。坐标 CC0，原论文 Ormö 等，Science，DOI 10.1126/science.273.5280.1392。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/400fff57befa7633f38202fc.svg?v=400fff57befa)

图 1PDB 1EMA 的真实晶体结构坐标经主轴投影形成两幅视图。颜色沿链序变化，红点是 CRO 发色团原子；链中缺口不连接。该工程化 GFP 结构发表于 1996 年，分辨率 1.90 Å。坐标 CC0，原论文 Ormö 等，Science，DOI 10.1126/science.273.5280.1392。

发色团可以理解为分子中的“吸光和发光核心”，周围结构则像一个精细组织的支架。支架会限制运动、安排氢键和电荷环境，并影响水或其他分子能否接近。对很多荧光体系，分子内部的转动、与溶剂的碰撞以及其他能量释放路线，会与发光竞争。改变这些路线，就可能改变亮度和寿命。这个比喻的用途在于强调发光中心与环境的关系；具体某一种突变或材料改性产生什么变化，仍需要光谱、寿命和结构等实验共同检验。

同一个故事也出现在人工材料中。把染料固定在聚合物网络里，可能限制它的运动，也可能使它在局部聚集；两种变化对荧光的影响可以不同。将染料包入颗粒后，周围介电环境、氧气进入速度、局部酸碱度和浓度都可能改变。若目标是制作传感器，就有意让某一种环境变量控制荧光；若目标是用染料计量材料质量，则希望这些环境效应尽量稳定。发光中心并不是独立于样品的装饰，它本身就是测量链中的一个分子级环节。

## 吸收之后有几条路：量子产率与寿命为什么相关又不同

分子吸收一个光子后，电子状态获得能量。通常它会先经历很快的振动松弛，把部分能量交给周围环境，然后从较低的激发态振动能级返回基态。如果这一步以发出光子的方式发生，就观察到荧光；如果能量通过其他过程释放，就没有对应的荧光光子。能级图把这些可能路线画在一起，箭头表示过程，不表示分子在空间中的移动。发射能量通常较低，所以发射波长通常较长；这个常见的位移使激发与发射的光学分离成为可能。

![原创能级与谱带示意。S₀ 和 S₁ 表示基态、第一激发单重态；每组横线代表振动能级。吸收之后先失去一部分能量，发射因而通常移向长波。右图为构造谱带，非 1EMA 的实测光谱。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bf4ffbd167c1ed7c8750518c.svg?v=bf4ffbd167c1)

图 2原创能级与谱带示意。S₀ 和 S₁ 表示基态、第一激发单重态；每组横线代表振动能级。吸收之后先失去一部分能量，发射因而通常移向长波。右图为构造谱带，非 1EMA 的实测光谱。

$$
\Phi_F=\frac{N_{\mathrm{em}}}{N_{\mathrm{abs}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/640affc4e10d6a3e71336f70.svg) | 荧光量子产率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/179ba6249c87305283cae0ec.svg) | 所定义条件下发出的荧光光子总数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e580857aa2a9a5ffee93726.svg) | 相应荧光分子吸收的激发光子数。 |

量子产率比较发出与吸收的光子数，光路收集效率须另行处理。吸收 100 个光子而平均发出 60 个荧光光子时，产率为 0.60。

量子产率统计的是被吸收的光子中，有多少最终对应荧光发射。假设分子群吸收了 1000 个光子，其中 600 次过程产生荧光光子，量子产率就是 0.6。探测器也许只收到了其中 30 个，因为发射朝许多方向传播，还要经过滤光片、光栅和探测器转换。这个 30 不是量子产率，它同时包含收集与检测效率。测量绝对量子产率需要把吸收与发射光子数放到可比较的标定体系中；相对方法则使用适当参照并处理吸收、光谱响应和介质等差别。

寿命描述激发态群体随时间消失的特征速度。可以把同一时刻被激发的一群分子想成进入一个有多个出口的大厅：每条离开路线都有自己的概率速率。发光出口和不发光出口都能减少留在大厅里的分子，因此总离开速率是各条速率之和。若这些速率在观察期间保持不变，留下的比例会随时间指数下降，平均停留时间等于总速率的倒数。量子产率则看所有离开路线中有多少选择了发光出口，所以它还取决于各条路线的相对比例。

$$
\tau=\frac{1}{k_f+k_{nr}},\qquad \Phi_F=\frac{k_f}{k_f+k_{nr}}=k_f\tau
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 单指数激发态寿命；率用 ns⁻¹ 时寿命用 ns。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eb0658bce80f3e4e9eccf061.svg) | 荧光辐射速率常数，ns⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/03b58580d0df47598b5c77c3.svg) | 合并的非辐射失能速率常数，ns⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/640affc4e10d6a3e71336f70.svg) | 荧光量子产率，无量纲。 |

独立且恒定的失能路径的速率相加；辐射路径占总速率的比例就是发光概率。kf=0.15、knr=0.10 ns⁻¹ 时 τ=4 ns、ΦF=0.60；knr 增至 0.35 ns⁻¹ 时 τ=2 ns、ΦF=0.30。

用一组明确数字比较：发光速率为 0.15 ns⁻¹，其他离开速率合计为 0.10 ns⁻¹，总速率为 0.25 ns⁻¹，寿命是 4 ns，量子产率为 0.6。如果新加入的环境过程再提供 0.25 ns⁻¹ 的不发光速率，总速率变成 0.50 ns⁻¹，寿命降为 2 ns，量子产率也降为 0.3。另一方面，如果所有速率同比例加快，寿命会改变，量子产率却可以不变。亮度、效率和时间并不是同一个量；把它们同时观察，才能更具体地讨论分子环境发生了什么。

## 稳态光谱与时间分辨测量，分别怎样接住光

普通荧光光谱仪可以固定激发波长，扫描发射波长，得到发射谱；也可以固定一个发射波长，扫描激发波长，得到激发谱。对稀溶液中的单一荧光物种，经过适当校正的激发谱常能反映其吸收行为，但混合物、能量转移或仪器响应会改变这种关系。稀溶液常用与激发光方向成直角的方向收集荧光，减少直接透射激发光进入探测器。较浓或不透明样品可以采用其他收集几何。光路一变，采样体积和吸收影响也会变，因此跨几何比较强度需要相应的标定。

光谱图上的任意单位并不意味着读数可以任意比较。它通常表示仪器响应尚未换算为某种绝对辐射量，但在相同配置与线性范围内，仍可用于设计清楚的相对比较。狭缝变宽能让更多光通过，也会降低波长选择的精细程度；探测增益提高可能放大信号，也可能改变噪声和饱和风险。比较样品时，应固定并记录激发、发射带宽、积分时间、增益与温度等条件。若改变了配置，可以用稳定参照重新建立可比关系，而不是仅按图形最高点进行缩放。

时间分辨测量使用短光脉冲激发，再记录光子相对于激发脉冲的到达时间。把许多次重复过程中的到达时间放入小时间格，就得到一条衰减曲线。这里的纳秒是十亿分之一秒；仪器并不是追踪某一个分子连续发出的所有光，而是从大量激发与探测事件建立时间分布。时间相关单光子计数需要在合适计数率下工作，过高计数率可能偏重较早到达的事件而使分布失真。仪器的时间响应也有有限宽度，因此一个理想瞬时事件在记录中会变成一个小脉冲。

$$
C(t)=C_0e^{-t/\tau}+B
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4e857df82e09ece3691e350.svg) | 延迟 t 对应时间格的期望计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8e1f255f71ebe5898eee968b.svg) | 所选时间原点下的衰减振幅，计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 相对于所选原点的延迟，ns。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 寿命，ns。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 每时间格的恒定背景期望计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底，无量纲。 |

单一恒定总速率使相同比例的激发人口在等长时间段内离开。C₀=1000、τ=4 ns、B=5 时，t=4 ns 的期望值约 372.88。仪器响应会将此曲线卷积展宽；代码尾段拟合把时间原点放在 0.6 ns，以减小振幅与延迟的无关混淆。

若寿命远大于仪器响应的宽度，可以在响应峰之后选取合适尾段拟合指数衰减，并检查拟合起点改变时寿命是否稳定。若寿命与响应宽度接近，则需要把仪器响应与衰减模型结合，通常通过卷积模型拟合。卷积可以理解为把许多稍有时间抖动的相同事件叠加，得到实际记录形状。背景在尾部的相对贡献会越来越大，因此直接对全部计数取对数再做直线拟合容易被背景和低计数影响。程序保留背景项，并在计数空间拟合，随后通过残差检查模型是否合适。

一个样品也可能含有不同环境中的同类分子，或多种荧光组分，从而出现多指数衰减。增加指数项可以改善数值拟合，却也会增加参数之间的补偿。先检查空白、仪器响应、散射峰和样品组成，再决定需要几种时间成分。若确实报告平均寿命，还要说明是按振幅还是按积分光子贡献加权；两种平均强调不同的群体贡献。这个定义会直接影响样品之间的比较，所以应与拟合模型、时间窗口和误差表示一起说明。

## 变暗的三种原因：减少、猝灭与遮挡

先考虑把荧光溶液稀释一半，同时保持溶剂环境和检测条件稳定。在低吸收、无明显相互作用的范围内，参与发光的分子减少，总强度可以近似减半；每个分子的激发态离开速率没有改变，寿命则可以保持原值。动态猝灭的逻辑不同：猝灭剂在激发态存在期间提供额外的失能路线，分子更早离开激发态，发光机会和寿命都会下降。两种情况在稳态强度图上可能非常相似，时间分辨曲线却能够帮助把它们区分开。

$$
\frac{F_0}{F}=\frac{\tau_0}{\tau}=1+k_q\tau_0[Q]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5d9e14fe75a38925a319a02a.svg) | 无猝灭剂与加入猝灭剂后的荧光强度，采用同一单位和光学条件。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fae386ec28f71b21891ce220.svg) | 无猝灭剂与加入猝灭剂后的寿命，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0360f5bd937533952ffbd944.svg) | 双分子动态猝灭速率常数，L·mol⁻¹·s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b53c8032c8dea25111a89d21.svg) | 猝灭剂摩尔浓度，mol·L⁻¹。 |

均匀纯动态猝灭中增加速率 kq[Q]，并保持吸收、分子数与辐射速率不变。kq=5×10⁹、τ₀=4×10⁻⁹ s、[Q]=0.05 mol/L 时比值为 2，τ=2 ns。强度与寿命同时测量可检查这一模型。

斯特恩—沃尔默关系把这个简单动态模型写成可检验的比例。若原寿命为 4 ns，双分子猝灭速率常数为 5 × 10⁹ L·mol⁻¹·s⁻¹，猝灭剂浓度为 0.05 mol·L⁻¹，则无量纲附加项为 1，原强度与当前强度之比为 2，原寿命与当前寿命之比也为 2。于是寿命变为 2 ns，强度降为原来的一半。这个相等关系依赖激发吸收、检测条件和纯动态机制等假设。把强度比与寿命比分别画出来，比只拟合其中一条线更能检验这些假设。

## 把变暗的三种原因分开

先降低分子数量，再恢复并加入动态猝灭剂，最后只降低出射光的透过比例。比较绝对强度与各自归一化后的衰减：哪些操作改变了分子的等待时间？这里使用单一发光环境、弱激发和理想光学衰减模型。

灰色虚线为初始 4 ns 状态。积分信号表示相对数量 × 量子产率 × 光学透过比例；归一化曲线除去了数量和光路造成的振幅差异。

静态猝灭常涉及在激发前形成不发光的复合物，减少能够贡献荧光的群体。对理想的简单情形，剩余可发光群体的寿命可以保持不变，因此总强度下降而寿命不明显变化。光漂白又是另一种过程，通常使部分发光分子经历不可逆化学改变；连续照射时强度随实验时间下降，需要与纳秒尺度的单次激发寿命区分。前者是许多次激发过程中样品逐渐变化，后者是一次激发后群体如何衰减。把两个时间轴都记录下来，可以避免把漂白造成的信号衰减误写成寿命缩短。

内滤效应不要求分子的发光能力发生变化。激发光在样品前部已被吸收，后部接收到的激发较少；发出的光又可能在到达探测器前被其他分子重新吸收。浓度增加时，分子数量增加与光学遮挡会竞争，测得强度便可能偏离线性，甚至下降。下面的近似用样品中心的激发与发射平均传播距离估计衰减，适合帮助理解透明溶液中一种常见几何模型。真正的修正应考虑收集体积、光程和光谱分布；对强散射或空间分布不均匀样品，改善测量几何与稀释常比套用一个系数更直接。

$$
F_{\mathrm{obs}}\approx F_{\mathrm{ideal}}\,10^{-(A_{\mathrm{ex}}+A_{\mathrm{em}})/2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6801b4fb188ade5ad0c3a6a0.svg) | 有内滤衰减时的观测强度，相对单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/779a333ebe703b3b7c55e3ce.svg) | 忽略样品内激发与发射衰减的理想强度，相同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/19bd174de2b2325f0a926e4c.svg) | 激发与发射波长在整条比色皿光程上的吸光度，无量纲。 |

矩形比色皿中心采样近似中，两段光各走半个全光程，透过率相乘。Aex=0.40、Aem=0.20 时因子为 10⁻⁰·³≈0.5012。实际采样体积与光路决定需要何种积分或校正。

## 完整计算：从光子计数拟合寿命，再检查变暗的原因

程序首先读取随示例包附带的 1EMA 坐标，重新绘制 GFP 主链与发色团位置。后面的时间曲线独立使用教学速率模型生成，分别设定 4 ns 和 2 ns 寿命，再加入有限宽度的仪器响应、背景和泊松计数波动。拟合时选取响应峰之后的尾段，估计振幅、寿命和背景，并保留残差。输出文件把理论寿命、拟合寿命、量子产率、原始计数和拟合值分开保存，读者可以直接核对图形与数字，而不必从一张对数坐标图中目测所有结果。

![构造的 4 ns 和 2 ns 光子计数实验。A 保留计数量级并显示 1.2 ns 之后的拟合；B 扣背景后除以拟合振幅；C 残差按估计计数标准差缩放；D 移动拟合起点，误差棒为拟合协方差给出的参数标准误。数据包含 0.12 ns 宽度的响应及泊松波动。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c767787d72c8c54154c347ff.svg?v=c767787d72c8)

图 3构造的 4 ns 和 2 ns 光子计数实验。A 保留计数量级并显示 1.2 ns 之后的拟合；B 扣背景后除以拟合振幅；C 残差按估计计数标准差缩放；D 移动拟合起点，误差棒为拟合协方差给出的参数标准误。数据包含 0.12 ns 宽度的响应及泊松波动。

### 从真实蛋白质坐标到光子计数与寿命诊断

完整程序离线读取所附 1EMA 坐标，另外构造计数数据、拟合衰减、检查拟合起点，并输出全部图和 CSV；真实结构与模拟计数明确区分。

```
"""Fluorescence: real PDB structure and explicitly constructed photon-count data.

Run: python main.py --output results --language en
Dependencies: numpy, scipy, matplotlib. No network access is needed.
1EMA coordinates: PDB archive CC0; Ormo et al., Science (1996),
https://doi.org/10.1126/science.273.5280.1392 .
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

P = argparse.ArgumentParser()
P.add_argument("--output", type=Path, default=Path("results"))
P.add_argument("--language", choices=["zh", "en"], default="en")
args = P.parse_args()
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
ZH = args.language == "zh"
def tr(zh, en): return zh if ZH else en
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#263d49", "text.color": "#263d49", "axes.edgecolor": "#9bacb1",
    "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6", "svg.fonttype": "path"})
BLUE, TEAL, CORAL, GOLD, GRAY = "#265f85", "#078579", "#d6604d", "#ba8e2f", "#81949a"
def save(fig, name):
    fig.savefig(OUT / f"{name}-{args.language}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}-{args.language}.png", dpi=155, bbox_inches="tight")
    plt.close(fig)
def panel(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left", weight="bold", pad=14)

# Preserve the real coordinate file; the plotted traces stop at sequence gaps.
atoms, chromophore = [], []
for line in (Path(__file__).parent / "data" / "1EMA.pdb").read_text().splitlines():
    if line[:6].strip() not in {"ATOM", "HETATM"} or line[21] != "A":
        continue
    xyz = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
    if line[17:20] == "CRO": chromophore.append(xyz)
    if line[12:16].strip() == "CA": atoms.append((int(line[22:26]), xyz))
ca = np.array([a[1] for a in atoms]); seq = np.array([a[0] for a in atoms])
cro = np.array(chromophore)
center = ca.mean(axis=0)
# A principal-coordinate projection shows the architecture without inventing atoms.
_, _, basis = np.linalg.svd(ca - center, full_matrices=False)
ca_p = (ca - center) @ basis.T; cro_p = (cro - center) @ basis.T
fig, axs = plt.subplots(1, 2, figsize=(11.6, 5.3))
for ax, dims, letter, title in zip(axs, [(0,1),(1,2)], ["A","B"],
    [tr("沿长轴展开的侧视", "Side view along the long dimension"), tr("沿长轴观察的端视", "End view along the long dimension")]):
    for i in range(len(seq)-1):
        if seq[i+1]-seq[i] == 1:
            ax.plot(ca_p[i:i+2,dims[0]], ca_p[i:i+2,dims[1]], lw=2.1, alpha=.8,
                    color=plt.cm.viridis(i/(len(seq)-1)))
    ax.scatter(cro_p[:,dims[0]], cro_p[:,dims[1]], s=42, color=CORAL, edgecolor="white", lw=.4,
               label=tr("发色团原子", "Chromophore atoms"), zorder=5)
    ax.set_aspect("equal"); ax.set_xlabel(tr("投影坐标 / Å", "Projected coordinate / Å")); ax.set_ylabel(tr("投影坐标 / Å", "Projected coordinate / Å"))
    panel(ax, letter, title); ax.legend(loc="lower left", fontsize=9)
fig.suptitle(tr("GFP 结构 1EMA：真实坐标，原创投影 · 1996", "GFP structure 1EMA: real coordinates, original projection · 1996"), fontsize=15, weight="bold")
fig.text(.5,.01,tr("链 A 的 Cα 轨迹；缺失或非连续残基处断开。CRO 以原子点显示。", "Chain-A Cα trace; gaps are not bridged. CRO is shown as atomic positions."),ha="center",fontsize=10)
fig.tight_layout(rect=[0,.10,1,.94]); save(fig,"structure")

# A conceptual energy diagram: its level spacings are not measured GFP energies.
fig, axs=plt.subplots(1,2,figsize=(11.6,5.2),gridspec_kw={"width_ratios":[1.15,1]})
ax=axs[0];ax.set_xlim(0,10);ax.set_ylim(-.4,5.2);ax.axis("off")
for y in [0,.4,.8]:ax.plot([.5,4.5],[y,y],color=BLUE,lw=2)
for y in [3,3.4,3.8,4.2]:ax.plot([.5,7.8],[y,y],color=BLUE,lw=2)
def arrow(a,b,c):ax.annotate("",xy=b,xytext=a,arrowprops={"arrowstyle":"-|>","color":c,"lw":2.5})
arrow((1.2,0),(1.2,4.2),BLUE);arrow((1.8,4.2),(3.5,3),GOLD);arrow((4.2,3),(4.2,.4),TEAL)
yy=np.linspace(3,0,150);xx=6.5+.16*np.sin(np.linspace(0,10*np.pi,150));ax.plot(xx,yy,color=CORAL,lw=2.3)
ax.text(.05,-.2,r"$S_0$",fontsize=14);ax.text(.05,4.7,r"$S_1$",fontsize=14)
ax.text(.95,2,tr("吸收", "Absorb"),rotation=90,ha="right",color=BLUE)
ax.text(2.1,4.5,tr("振动弛豫", "Vibrational relaxation"),fontsize=10,color=GOLD)
ax.text(4.45,1.5,tr("荧光", "Fluorescence"),rotation=90,va="center",color=TEAL)
ax.text(7.1,1.5,tr("非辐射\n失能", "Nonradiative\nrelaxation"),va="center",fontsize=10,color=CORAL)
panel(ax,"A",tr("Stokes 位移的能量路径", "Energy paths behind the Stokes shift"))
w=np.linspace(380,680,500);exc=np.exp(-.5*((w-470)/22)**2);emi=np.exp(-.5*((w-535)/30)**2)
axs[1].fill_between(w,exc,color=BLUE,alpha=.17);axs[1].plot(w,exc,color=BLUE,label=tr("激发", "Excitation"))
axs[1].fill_between(w,emi,color=TEAL,alpha=.17);axs[1].plot(w,emi,color=TEAL,label=tr("发射", "Emission"))
axs[1].annotate("",xy=(535,1.05),xytext=(470,1.05),arrowprops={"arrowstyle":"<->","color":GRAY})
axs[1].text(502.5,1.1,tr("65 nm（示意）", "65 nm (schematic)"),ha="center",fontsize=10)
axs[1].set(xlim=(380,680),ylim=(0,1.3),xlabel=tr("波长 / nm", "Wavelength / nm"),ylabel=tr("归一化谱强度", "Normalized spectral intensity"));axs[1].legend(frameon=False)
panel(axs[1],"B",tr("分开照明与发射", "Separate illumination and emission"))
fig.text(.5,.01,tr("原理模型；不代表 1EMA 的实测光谱。纵向能级位置表示相对能量。", "Conceptual model, not measured spectra of 1EMA. Vertical energy levels show relative energy."),ha="center",fontsize=10)
fig.tight_layout(rect=[0,.06,1,1]);save(fig,"pathways")

# Two constructed experiments. Time is in ns. The IRF is normalized discretely.
rng=np.random.default_rng(540)
t=np.arange(0,30.0001,.05)
irf=np.exp(-.5*((t-.6)/.12)**2);irf/=irf.sum()
lifetimes=[4.,2.];counts=[];fits=[];sensitivity=[]
def tail(x, amplitude, lifetime, background):return amplitude*np.exp(-(x-.6)/lifetime)+background
for tau in lifetimes:
    expected=np.convolve(1800*np.exp(-t/tau),irf,mode="full")[:len(t)]+5
    observed=rng.poisson(expected);counts.append(observed)
    results=[]
    for start in [.35,.6,.9,1.2,2,4,6]:
        mask=t>=start
        p,cov=curve_fit(tail,t[mask],observed[mask],p0=[1800,tau,5],sigma=np.sqrt(np.maximum(observed[mask],1)),
            absolute_sigma=True,bounds=([0,.1,0],[10000,20,100]),maxfev=15000)
        results.append([start,p[1],np.sqrt(cov[1,1])])
        if start==1.2:fits.append(p)
    sensitivity.append(np.array(results))
fig,axs=plt.subplots(2,2,figsize=(11.6,8.1))
for i,(tau,y,p,col) in enumerate(zip(lifetimes,counts,fits,[TEAL,CORAL])):
    label=tr(f"设定 {tau:g} ns；拟合 {p[1]:.3f} ns",f"Set {tau:g} ns; fit {p[1]:.3f} ns")
    axs[0,0].scatter(t[::3],y[::3],s=9,alpha=.4,color=col)
    mask=t>=1.2;axs[0,0].plot(t[mask],tail(t[mask],*p),color=col,lw=2,label=label)
    norm=(y-p[2])/p[0];axs[0,1].plot(t,norm,color=col,alpha=.7,label=tr(f"{tau:g} ns 组",f"{tau:g} ns group"))
    residual=(y[mask]-tail(t[mask],*p))/np.sqrt(np.maximum(y[mask],1));axs[1,0].plot(t[mask],residual,color=col,alpha=.65,lw=.7)
    ss=sensitivity[i];axs[1,1].errorbar(ss[:,0],ss[:,1],yerr=ss[:,2],color=col,marker="o",capsize=3,label=label)
    axs[1,1].axhline(tau,color=col,ls=":",alpha=.5)
axs[0,0].axvspan(0,1.2,color=GRAY,alpha=.1);axs[0,0].legend(fontsize=9,frameon=False)
axs[0,0].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("每时间格计数","Counts per time bin"),xlim=(0,25))
axs[0,1].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("扣背景后除以拟合振幅","Background-subtracted / fitted amplitude"),xlim=(0,15));axs[0,1].legend(fontsize=9,frameon=False)
axs[1,0].axhline(0,color=GRAY,lw=1);axs[1,0].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("残差 / 估计计数标准差","Residual / estimated count SD"))
axs[1,1].set(xlabel=tr("拟合起点 / ns","Fit starting time / ns"),ylabel=tr("拟合寿命 / ns","Fitted lifetime / ns"));axs[1,1].legend(fontsize=9,frameon=False)
for ax,l,z,e in zip(axs.flat,"ABCD",["保留光子量级","比较衰减形状","检查加权残差","改变拟合起点"],["Retain the count scale","Compare decay shape","Inspect weighted residuals","Change the fit start"]):panel(ax,l,tr(z,e))
fig.tight_layout();save(fig,"decays")

q=np.linspace(0,.1,200);ratio=1+20*q
c=np.linspace(0,50,200);ideal=c*.6;observed=ideal*10**(-(.05*c+.02*c)/2)
fig,axs=plt.subplots(1,2,figsize=(11.6,4.8))
axs[0].plot(q,ratio,color=TEAL,lw=3,label=tr("动态：强度比与寿命比","Dynamic: intensity and lifetime ratios"))
axs[0].plot(q,np.ones_like(q),color=CORAL,lw=2,ls="--",label=tr("纯光学衰减：寿命比","Pure optical attenuation: lifetime ratio"))
axs[0].set(xlabel=tr("猝灭剂浓度 / mol L$^{-1}$","Quencher / mol L$^{-1}$"),ylabel=tr("无猝灭值 / 当前值","Unquenched value / current value"));axs[0].legend(fontsize=9,frameon=False)
axs[1].plot(c,ideal,color=GRAY,ls="--",label=tr("理想浓度响应","Ideal concentration response"));axs[1].plot(c,observed,color=BLUE,lw=3,label=tr("加入内滤的中点近似","With midpoint inner-filter approximation"))
axs[1].set(xlabel=tr("浓度 / μmol L$^{-1}$","Concentration / μmol L$^{-1}$"),ylabel=tr("相对荧光信号","Relative fluorescence signal"));axs[1].legend(fontsize=9,frameon=False)
panel(axs[0],"A",tr("强度与寿命是否一起改变？","Do intensity and lifetime change together?"));panel(axs[1],"B",tr("浓度增加也可能变暗","More concentrated can become dimmer"))
fig.tight_layout();save(fig,"diagnostics")
np.savetxt(OUT/"decay_counts.csv",np.column_stack([t,*counts]),delimiter=",",header="delay_ns,counts_tau4,counts_tau2",comments="")
np.savetxt(OUT/"fit_sensitivity.csv",np.vstack([np.column_stack([np.full(len(s),tau),s]) for tau,s in zip(lifetimes,sensitivity)]),delimiter=",",header="true_tau_ns,start_ns,fitted_tau_ns,standard_error_ns",comments="")
np.savetxt(OUT/"inner_filter.csv",np.column_stack([c,ideal,observed]),delimiter=",",header="concentration_uM,ideal_relative_signal,attenuated_relative_signal",comments="")
summary={"tau_unquenched_ns":1/(.15+.1),"yield_unquenched":.15/(.15+.1),"tau_quenched_ns":1/(.15+.1+5*.05),
    "yield_quenched":.15/(.15+.1+5*.05),"fit_tau4_ns":float(fits[0][1]),"fit_tau2_ns":float(fits[1][1]),
    "chromophore_atoms":len(cro),"backbone_CA_atoms":len(ca),"inner_filter_factor_A04_A02":10**(-.3),
    "data_kind":{"structure":"real crystallographic PDB 1EMA coordinates","decays":"constructed Poisson teaching data"}}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
print(json.dumps(summary,indent=2))
```

图中同时显示线性计数轴和扣背景后的归一化衰减，使两种读图任务分开：线性轴保留真实记录量级，归一化曲线帮助比较衰减形状。归一化会丢掉总光子量差异，因此不能仅用归一化后重合的曲线判断两个样品同样明亮。程序还将拟合起点前后移动，观察尾段寿命估计的变化。起点太早会混入仪器响应，太晚则丢失大量光子并使背景占比增加；稳定的平台区域比某一个最漂亮的拟合值更有解释力。

泊松计数模型意味着每个时间格的波动与其平均计数有关。亮的前段和暗的尾段不具有相同的绝对噪声，代码使用与计数规模相应的权重来拟合，并保留已知生成模型供检查。对于计数极少的数据，可以进一步采用直接针对泊松统计的似然方法。这里优先让读者看清时间轴、背景和仪器响应之间的关系。把真实仪器数据接入时，先确认时间格宽度、重复频率、响应函数和背景测量，再决定拟合区间与统计模型，能避免把一个格式相同的数组误当成相同的实验。

![理想动态猝灭同时改变强度和寿命，而纯光学衰减保留寿命。右图采用矩形比色皿中心采样的内滤近似：浓度增加一方面增加发光分子，另一方面削弱激发与出射光；两者竞争可产生峰值。两图均为明确设定的原理模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/410b8793019280525d726aad.svg?v=410b87930192)

图 4理想动态猝灭同时改变强度和寿命，而纯光学衰减保留寿命。右图采用矩形比色皿中心采样的内滤近似：浓度增加一方面增加发光分子，另一方面削弱激发与出射光；两者竞争可产生峰值。两图均为明确设定的原理模型。

第二组计算把纯动态猝灭中的强度比与寿命比放在一起，并与一个不改变寿命的光学衰减示例比较。它展示的是区分解释的思路：若强度下降与寿命缩短相互对应，动态失能是一条值得检验的路线；若强度下降而寿命稳定，则继续检查浓度、静态复合、光漂白或内滤等因素。每种解释都应有对应的补充实验，例如吸收谱、稀释序列、时间序列或结合测量。图中的模型不替实验样品选择答案，而是帮助把下一步测量设计成能够区分答案的观察。

## 让荧光真正参与研究：先决定光信号代表哪个对象

长期比较还需要一个稳定的参照。仪器在不同波长的检测灵敏度不同，灯强度和光学元件状态也可能随时间变化；同一染料的谱峰看起来改变，有时来自检测链而非分子。波长校准、相对光谱响应校正和稳定参照样品分别检查不同环节，寿命测量还需要合适的响应或寿命参照。参照的溶剂、温度和储存条件会影响其行为，所以“用了同一种染料”本身并未完整定义参照实验。把参照读数与样品测量交替安排，可以更直接地区分随时间发生的仪器变化和样品变化。

实验顺序也会影响结果。若低浓度样品总先测、高浓度样品总后测，逐渐变化的光源或样品光漂白可能被误读成浓度效应。可以交错测量不同组别，在中间重复一个固定样品，并记录照射时间。含氧环境同样值得保持一致：氧可能参与某些激发态失能和光化学反应，开盖、脱气和密封会改变它的供应。这里的控制并非增加一串形式化步骤，而是把所要研究的变量从容易一同变化的条件中分离出来，使每条曲线都能回答原先的问题。

用荧光研究蛋白质吸附时，溶液变暗可能意味着蛋白质被表面移走，也可能意味着吸附改变了标记染料环境。可以测量上清液、表面和洗脱液中的相关信号，结合质量守恒与合适参照检查去向。若只用溶液强度差估计吸附量，应先确定材料不会使游离染料响应改变，也不会带来额外散射或吸收。标签比例、游离染料去除情况和标记蛋白质的功能状态，都属于这条测量链。把这些条件与校准放在一起，荧光才能从“看见亮点”进一步支持定量。

环境敏感探针的研究目标则恰好利用环境影响。例如让探针寿命随局部黏度变化，需要先在可控制的参照环境中建立关系，再检查温度、极性或结合是否同时影响寿命。将探针放进细胞或水凝胶后，它可能分布在多个微环境中，平均读数会混合这些区域。空间分辨成像和光谱或寿命信息可以帮助分开贡献。此时荧光分子的选择、定位和校准共同决定研究问题能够回答到什么尺度，而不是仅由仪器标称的时间或空间分辨率决定。

多色实验还要考虑谱带重叠。一个发射通道可能同时收集两个染料的光，某个激发波长也可能激发多个组分。单标样品帮助测量每种组分进入各通道的比例，未标记样品帮助观察自发荧光，光谱扫描则展示重叠发生在哪。若研究分子间能量转移，还要把直接激发、通道串色和供受体数量关系分别处理。能量转移可以改变供体寿命，但观察到一个通道变暗、另一个变亮本身还不足以完成机制归属；合适对照把颜色变化连接到具体的能量传递路径。

一份清楚的荧光结果应让读者知道：谁在发光，怎样被激发，哪些光进入探测器，读数代表数量、光谱形状还是时间，以及哪个参照支持了比较。选择稳态光谱时，关注吸收、发射与背景；选择寿命时，关注时间响应、计数和模型；选择材料或生物应用时，继续追问标记是否改变了对象及其环境。荧光的趣味就在于，同样一束光可以连接分子结构、局部环境和生命活动。把每一层关系说清楚，亮度才会成为有明确物理意义的研究信息。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Molecular Probes Handbook: Introduction to Fluorescence Techniques](https://www.thermofisher.com/us/en/home/references/molecular-probes-the-handbook/introduction-to-fluorescence-techniques.html)

   量子产率、光谱、光漂白及内滤。
2. [Molecular Expressions: Introduction to Fluorescence](https://micro.magnet.fsu.edu/primer/techniques/fluorescence/fluorescenceintro.html)

   Stokes 1852 年命名、能级与寿命。
3. [Ormö et al.: Crystal structure of GFP; PDB 1EMA](https://www.rcsb.org/structure/1EMA)

   1996 年晶体结构、工程化序列及发色团环境。

   PDB archive coordinates CC0; entry paper DOI 10.1126/science.273.5280.1392.
4. [RCSB PDB: Data usage policies](https://www.rcsb.org/pages/policies)

   PDB 坐标再利用条件。

   PDB archive data CC0.
5. [NISTIR 7457: Recommendations and Guidelines for Standardization of Fluorescence Spectroscopy](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7457.pdf)

   仪器、样品及光谱校正的计量学框架。

   US government technical reference.
6. [Margineanu: Calibration approaches for fluorescence lifetime applications using time-domain measurements](https://pmc.ncbi.nlm.nih.gov/articles/PMC11969142/)

   响应函数、参考染料及光子计数时间测量。

   CC BY 4.0 article; no source figures reproduced.
