# 体积排阻色谱：聚合物分子有多大

Source: https://ml-biomat.com/tutorials/experimental-methods/c02/
Language: zh-CN

让溶解的链通过多孔空间，读懂尺寸分离、质量加权和一整群分子的分布。

## 同样叫聚合物，为什么一瓶很稠，另一瓶很稀

把两份透明质酸粉末各称取相同质量，加入同样多的水，得到的溶液可能有不同的黏稠程度。化学名称相同，只说明构成链的基本单元相同，并没有告诉我们每条链包含多少个单元。可以把它们想成由相同珠子串成的项链：一盒以短项链为主，另一盒混有少量很长的项链，盒子的总质量相同，拿起和缠绕时的表现仍会不同。真实溶液还受浓度、盐、温度和链间作用影响；要追问链长是否发生了变化，就需要一种能把不同大小的溶解分子逐渐分开的测量。体积排阻色谱，简称 SEC，正适合承担这个环节。

这个问题在生物实验里也很常见。一瓶蛋白质可能同时含有单个蛋白、两个蛋白结合形成的二聚体，以及更大的聚集体；凝胶过滤可以帮助分开这些组分，并收集后续实验需要的部分。在材料研究中，可降解聚合物经过一段时间后，外观可能依旧完整，链却已经断成较短片段。测量降解前后的 SEC 分布，能够把“外观看起来差不多”推进到“可溶部分的链群体怎样变化”。这里的可溶部分是一个实验对象：如果样品中还有未溶解网络或沉淀，就应同时称量、观察和记录它们，才能把色谱结果放回完整材料的质量平衡中。

SEC 的中文名称是体积排阻色谱。凝胶渗透色谱 GPC 常用于有机溶剂中的聚合物分析，凝胶过滤色谱 GFC 常用于水溶液中的生物大分子分离；三个名称背后共享同一种核心机制。柱内装满带有孔道的颗粒，不同大小的溶解分子能够访问不同数量的孔内空间，因此流出柱子的平均位置不同。仪器首先给出的是信号随洗脱时间或洗脱体积的变化。把这个位置转换成摩尔质量，还需要校准或联用检测器。理解这两步的分工，之后看到一个标有“分子量”的横坐标，就会自然追问它是怎样建立起来的。

本章沿着一份样品进入色谱柱的过程展开：先理解为什么大分子反而先出来，再认识校准曲线，接着区分按分子个数和按质量得到的平均值。我们会一起读一组公开发表的聚乙烯累计分布，并用完整程序把孔道机制、标准曲线、原始形式的色谱信号和积分选择连起来。学完以后，应能解释一条曲线的横纵坐标，判断一次峰位移动可能意味着什么，并为下一次实验选择有用的对照。

## 大分子先出来：多孔小球里的“侧边房间”

想象一条走廊，两侧有许多小房间。两组参观者从同一个入口出发：一组只能沿走廊前进，另一组还会进入沿途房间停留。即使两组在走廊里的移动方式相同，第二组平均也会更晚到达出口。SEC 中，颗粒之间的液体类似走廊，颗粒内部的孔道类似房间。较大的溶解分子能进入的孔内空间较少，较小的分子能进入较多空间，于是前者通常更早洗脱。这里并不是把大分子强行压过一个筛孔，也不是小分子被堵在出口；分离来自分子在可访问溶剂空间之间的分配。

这段历史很能帮助人摆脱“筛子总让小东西先通过”的直觉。耶克·波拉特在回顾早期研究时提到，即使没有施加电泳所用的电流，淀粉柱中不同分子仍出现分离。后来，波拉特与佩尔·弗洛丁研究交联葡聚糖凝胶，相关工作发表于 1959 年。孔道能够把大分子和小分子盐分开，成为蛋白质脱盐的重要工具。图中的柱和信号是围绕这个机制绘制的示意：大分子先形成一个流出带，盐随后出现。它表现的是脱盐的物理思路，曲线数值由本章构造，并非早期实验的复刻。

为了给“能够进入多少空间”一个量化尺度，先测两个参照体积。完全不能进入孔道、且不与填料发生额外作用的标记，提供排阻体积 V₀；足够小、能够访问全部相关孔内液体的标记，提供总可达体积 Vₜ。这里的 Vₜ 是由合适标记测得的色谱体积，不是拿直尺量柱子外壳之后算出的圆柱体积。目标分子的洗脱体积 Vₑ 落在两者之间时，可把它多访问的体积除以可供访问的孔体积，得到无量纲的 Kₐᵥ。下式把类比中的“进入了一部分房间”变成一个可比较的测量。

$$
K_{\mathrm{av}}=\frac{V_e-V_0}{V_t-V_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/17929f84b05c9c9ee6b7954d.svg) | 表观孔体积可达比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/daa1e83231d13f3a99351353.svg) | 目标分子的洗脱体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | 完全排阻的合适标记测得的体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ad460123890fe451611439a3.svg) | 完全进入相关孔空间的合适标记测得的总可达体积，mL。 |

在大小排阻主导且参照标记适合时，以多访问的体积除以孔内可达体积。Vₑ=9、V₀=3、Vₜ=18 mL，Kav=6/15=0.4。0 与 1 对应两端参照；额外吸附或排斥会改变这个解释。

![原创孔道与脱盐机制示意。颗粒间与孔内空间不按真实尺度绘制；B 为构造脱盐曲线，连接 1959 年凝胶过滤的机制。C 用 V₀=3、Vₜ=18 mL 展示可达比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/332d0565684a77299bb67fb8.svg?v=332d0565684a)

图 1原创孔道与脱盐机制示意。颗粒间与孔内空间不按真实尺度绘制；B 为构造脱盐曲线，连接 1959 年凝胶过滤的机制。C 用 V₀=3、Vₜ=18 mL 展示可达比例。

当目标大到几乎所有孔都进不去时，不同的大分子可能一起在 V₀ 附近流出；当目标小到能够访问几乎所有孔时，不同的小分子也可能一起靠近 Vₜ。真正适合按大小区分的区域在两端之间，这就是选择填料孔径范围的原因。把一根适合分离盐与蛋白质的脱盐柱，直接拿来精细区分两个大小相近的蛋白质，往往得不到同样的分离效果。前者要求把两大组分开，后者要求在很窄的大小差别上获得足够的位置差异，还需要较小的进样体积和更高的柱效。

真实分子还会与孔壁发生静电、疏水或其他相互作用。例如，带电的多糖在盐浓度很低时，链可能伸展得更开，也可能受到填料表面电荷影响。两种效应都能改变峰位，因此增加盐后峰位变化并不自动等于链断了。建立方法时，可以通过合适的缓冲液、离子强度和填料化学，尽量让大小分配成为主要保留机制，再用浓度系列和已知样品检查这一判断。类比帮助我们理解机制，实验对照则负责检查真实体系是否满足它。

## 从流出位置到摩尔质量，中间要搭一把尺子

检测器看到某个峰出现在 10 mL，并不会直接知道它是一万还是十万克每摩尔。常规校准的做法，是让一组摩尔质量已知、分布较窄的标准聚合物分别通过同一套系统，记录每个标准的峰位。在适当的工作范围内，摩尔质量的十进对数往往与洗脱体积近似呈线性关系。对数在这里相当于把“乘十倍”变成相同的刻度间隔，使几千、几万、几十万能够放在一张图里清楚比较。图中的标准点从小质量到大质量依次向较小的洗脱体积移动，正与前面的孔道机制一致。

1964 年，约翰·摩尔发表了以交联聚苯乙烯凝胶进行聚合物分离的工作，GPC 随后把聚合物分布测量变成更连续的仪器过程。这个发展也把校准问题推到了中心：记录一条流出曲线只是第一步，必须知道曲线上每个位置对应什么样的分子。我们用一条教学标准曲线说明计算，斜率表示洗脱体积每变化 1 mL，对数摩尔质量变化多少；截距则决定整把尺子在纵向的位置。实际方法应使用标准样覆盖目标分布，观察残差和两端弯曲，而不是为了让公式简单，强行把整个柱范围拟合成直线。

$$
\log_{10}\!\left(\frac{M}{1\,\mathrm{g\,mol^{-1}}}\right)=a-bV_e
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 校准赋予的摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 线性校准截距，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 校准下降斜率的大小，mL⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/daa1e83231d13f3a99351353.svg) | 洗脱体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 十进对数；括号内先除以单位量，使其无量纲。 |

在标准覆盖、近似线性的分离范围内，以对数连接大小位置与标准质量。a=7、b=0.25 mL⁻¹、Vₑ=10 mL，log₁₀ M=4.5，对应约 31,623 g/mol；Vₑ=12 mL 对应 10,000 g/mol。同一化学系列与溶液条件支持该转换。

![构造标准与链群体：log₁₀ M 的数量分布均值 4.2、标准差 0.35，质量分布随权重改变。色谱额外展宽 σV=0.25 mL，面积归一化为 1。D 按流出顺序累计，从大分子到小分子。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/da13b991941f2f714ab8cc5b.svg?v=da13b991941f)

图 2构造标准与链群体：log₁₀ M 的数量分布均值 4.2、标准差 0.35，质量分布随权重改变。色谱额外展宽 σV=0.25 mL，面积归一化为 1。D 按流出顺序累计，从大分子到小分子。

标准的化学结构很重要。两条质量相同的链，如果一种在溶剂里伸展较开，另一种较紧凑，就会访问不同的孔内空间。一个支化聚合物与同质量的线性聚合物也可能表现出不同的溶液尺寸。因此，用聚苯乙烯标准校准未知聚合物时，直接得到的是该条件下的聚苯乙烯等效摩尔质量。把“等效”写清楚，相当于告诉读者尺子的刻度依据；它也让不同实验室的结果更容易比较。若研究的重点是链支化前后真实质量是否改变，单靠同一把尺寸尺还需要补上其他测量。

差示折光检测器常与 SEC 配合。它比较流出溶液与纯流动相的折射率差；在给定聚合物、溶剂和温度下，稀溶液的响应可与浓度联系起来。于是每一个小体积切片下面的信号面积可以表示该切片携带的质量。紫外检测器则只对能吸收所选波长的组分产生相应信号，同一混合物里不同组分的吸收能力可能不同。一个蛋白质与一个几乎没有该波长吸收的多糖即使同时流出，在紫外图上也不会自动按质量公平显示。解释峰面积之前，要先回答检测器对什么敏感，以及这种敏感度在各组分之间是否一致。

联用多角度光散射与浓度检测器，可以进一步从散射强度、角度和浓度推求各切片的摩尔质量，减少对同类标准校准的依赖。浓度测量所需的折射率增量、检测器之间的时间对齐、峰展宽以及尘埃或聚集体的贡献，都仍是数据链的一部分。把它称为不依赖常规分子量标准的测量，比把“绝对分子量”理解成完全不需要假设更有帮助。对于初次分析，先学会常规校准和质量响应，之后再加入联用检测器，推理会连贯得多。

## 一群长短不同的链，为什么需要两个平均值

假设一份样品只有两种链：九十条链的摩尔质量都是 10,000 g/mol，十条链都是 100,000 g/mol。按链数看，短链占九成；按质量看，十条长链贡献的质量反而略多于九十条短链。这里使用摩尔质量，是指一摩尔这类链的质量；g/mol 是单位，数值随链长增加。描述这群链时，我们可以让每条链各投一票，得到数均摩尔质量 Mₙ；也可以让每份质量各投一票，得到重均摩尔质量 M𝑤。两种平均都正确，差别在于研究问题选择了怎样的权重。

数均值的计算最接近日常的平均数：把各类链的数量乘以相应摩尔质量，全部加起来，再除以总链数。上面的例子得到 19,000 g/mol。它不是“有一半链比它轻、另一半比它重”的分界；那个分界叫中位数。在这组离散例子里，按链数的中位数是 10,000 g/mol，因为九成的链都在这里。把平均数与中位数区分开，对阅读宽分布尤其重要：少量长链能够推高平均数，而多数链仍可能较短。

$$
M_n=\frac{\sum_i N_iM_i}{\sum_i N_i}=\left(\sum_i\frac{w_i}{M_i}\right)^{-1},\qquad w_i=\frac{N_iM_i}{\sum_j N_jM_j}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | 数均摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2e48d6441cb55e92796c4f28.svg) | 对应类别中的链数，无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/80f8ce36f42008dae6d1d510.svg) | 对应类别的摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | 类别 i 的质量分数，无量纲，各类之和为 1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 对所有相关链类别或质量切片求和的索引。 |

每条链等权平均；从质量切片出发，质量除以摩尔质量得到与链数成比例的权重。90 条 10,000 和 10 条 100,000 g/mol 的链给出 Mn=19,000 g/mol。质量分数分别为 9/19 与 10/19。

重均值则先问每一类链贡献多少质量，再用这些质量比例去平均摩尔质量。长链既有较大的摩尔质量，又贡献较大的质量权重，因此高质量尾部对 M𝑤 的影响更显著。同一个例子得到约 57,368 g/mol，明显高于 Mₙ。把两者相除得到分散系数 Đ，描述这两种加权平均相差多少。所有链完全相同时，两种平均相等，Đ 为 1；存在链长差异时，重均值通常更大。本例的 Đ 约为 3.019。这个数字概括了分布宽度的一个方面，但两条形状不同的分布仍可能具有相同的比值。

$$
M_w=\sum_i w_iM_i=\frac{\sum_iN_iM_i^2}{\sum_iN_iM_i},\qquad \mathit{Đ}=\frac{M_w}{M_n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | 重均摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | 类别 i 的质量分数，无量纲，总和为 1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | 类别 i 的链数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b5817fb0c0bac5188945802.svg) | 类别 i 的摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | 数均摩尔质量，g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/40bf2c4da5241a580e5118bc.svg) | 分散系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 链类别或质量切片索引。 |

每份质量等权平均，长链的权重更大。同一 90:10 例得到 Mw≈57,368.42 g/mol，Đ≈3.01939。比较同一完整群体、非负权重时 Đ≥1；仪器展宽和截断积分会改变表观值。

SEC 的浓度型检测器通常先提供质量信息，而不是直接数出链的条数。要由质量切片求 Mₙ，就需要先用切片质量除以该处的摩尔质量，得到与链数成比例的量，再进行总质量除以总链数的计算。因此低摩尔质量尾部虽然质量不大，却可能代表很多条链，对 Mₙ 很有影响。图中同一构造群体的按数目分布和按质量分布，峰位并不重合；这不是画错，而是权重改变后自然产生的结果。软件导出“distribution”时，应读清它究竟按数量、质量、线性质量轴还是对数质量轴归一化。

现在看真实数据。罗斯与弗洛伦在 1972 年发表的 NBS 聚乙烯 SRM 1475 研究，给出了累计质量百分数随对数摩尔质量的表格。图中点直接对应公开表格的数字，纵轴回答“低于这个摩尔质量的聚合物，占总质量的百分之几”。本章用相邻点在对数轴上作线性插值，读出质量中位数；它与论文报告的 Mₙ 和 M𝑤 是不同的统计量。累计曲线从低质量向高质量累加，也与色谱图中从先流出的大分子向后累加的方向不同。读懂轴的方向，才能把一张真实的旧表格准确地转换成新的图。

![A 重绘 Ross 与 Frolen（NBS，1972）表 4 的真实累计质量数据；质量中位数由对数轴线性插值得到，原表印刷数值全部保留。B 是独立构造例：90 条 10,000 g/mol 短链和 10 条 100,000 g/mol 长链，比较链数与质量百分比。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6f9862f4014067ff892935bf.svg?v=6f9862f40140)

图 3A 重绘 Ross 与 Frolen（NBS，1972）表 4 的真实累计质量数据；质量中位数由对数轴线性插值得到，原表印刷数值全部保留。B 是独立构造例：90 条 10,000 g/mol 短链和 10 条 100,000 g/mol 长链，比较链数与质量百分比。

## 真正进入色谱柱的，是经过制备的一份样品

一个聚合物粉末消失在液体里，并不一定意味着所有链都已经达到稳定、均匀的溶解状态。高摩尔质量组分可能溶解较慢，交联微凝胶可能只吸液膨胀，蛋白质可能在等待期间发生聚集。制备时要选择能够溶解目标、又与填料和检测器相容的流动相，并给出温度、时间和混合方式。对于容易受到机械剪切影响的大分子，过强的处理本身就可能改变分布；对于不稳定蛋白质，温度和缓冲条件又关系到构象与聚集状态。样品准备因此属于测量定义，而不是进样之前可以省略描述的杂务。

过滤可以去除堵柱颗粒，也可能改变我们准备测量的群体。若聚集体或高质量组分被滤膜截留，后面的色谱就只代表通过滤膜的部分；若目标吸附在膜上，回收量还会下降。可以将过滤前后浓度、可见沉淀、过滤器材质与样品回收联系起来检查。对于要研究可溶聚集体的蛋白质，选用合适的澄清步骤，并比较回收和尺寸分布，比把所有大颗粒统一移除后再宣称样品完全单一更有解释力。对难溶网络材料，记录可溶分数同样关键，因为柱子只接收溶液里的组分。

进样体积决定初始样品带有多宽。若一开始就注入很长的一段样品，即使孔道能够让不同组分产生位置差，最后也可能互相重叠。浓度过高还会改变溶液黏度、链间相互作用或局部流动，使峰形和位置出现浓度依赖。一个有用的小实验，是在其他条件不变时，改变进样浓度或体积并比较归一化曲线。若位置和形状稳定，浓度型检测器的面积又按加入量增加，就为所选条件提供了支持。若稀释后早出峰减少，则应同时考虑聚集平衡变化，而不仅是仪器负荷降低。

空白、窄分布标准和稳定参考样分别回答不同问题。溶剂空白帮助识别流动相或进样溶剂引起的系统峰；窄分布标准检查峰位与仪器展宽；稳定参考样监测整套方法的长期一致性。差示折光检测对温度与流动相差异敏感，充分平衡和稳定基线对积分尤其重要。用不同于流动相的溶剂配样，会把一个溶剂扰动与样品一起送进检测器。若它刚好落在低质量尾部，自动积分可能把它当成很多短链。比较空白图、样品图和标准图，能让这个问题在计算平均值之前就显现出来。

保存完整原始时间信号和实际流量，还有一个很实用的理由：时间与体积不是同一个量。流量稳定时，流过体积可由流量乘经过时间得到；比较不同流量下的峰位，宜先在统一的体积坐标上检查。过高流量可能增加某些展宽贡献，也可能使很大的链受到剪切作用。选择条件应围绕所需分辨率、样品稳定性和可用分析时间，而不是单纯把出峰越快当成越好。

## 峰变宽、峰移动，各自怎样影响结论

仪器会把一群到达时间非常接近的分子摊开。流动路径差异、孔内外交换、连接管路和检测池都可以贡献展宽。因此测得的宽度包含样品本来的分布，也包含系统增加的宽度。对于一个很窄的标准样，这个问题格外显眼；对于一个很宽的真实样品，仪器增加的部分可能相对较小。图中的模型让同一个链群体通过三种额外展宽条件，保持总面积和平均流出位置不变，只改变信号的宽度。把所有宽度都当成链长差异，计算出的分散系数就会升高。

另一种容易混淆的变化是整体峰位移动。设同质量的链因构象更紧凑而向后移动 0.5 mL，仍用原来的标准曲线换算，所有表观摩尔质量都会乘上约 0.750 的因子。图中的这一步没有让任何化学键断裂，却产生了约四分之一的表观质量下降。这说明研究链降解时，溶剂、盐、温度和标准校准应尽量保持可比，并结合反应化学、端基信息或其他检测结果来建立解释。若研究本来关注构象变化，峰位移动本身又成为有价值的信号，只是应把它放在尺寸变化的问题里。

积分范围也会悄悄改变答案。色谱后段对应较小的分子，删去这段信号会删掉相当数量的短链，使 Mₙ 升高。早段的高质量尾部即使面积较小，也可能对 M𝑤 产生明显影响。一个可复查的分析应同时展示原始信号、所选基线、积分起止点和换算曲线，再比较合理范围内改变这些选择后结果的变化。图中的积分终点扫描保留前段不变，只逐渐纳入低质量尾部，清楚显示两个平均值并不同步收敛。这样便能把“软件显示一个数字”变成“知道这个数字受哪些选择影响”。

![同一构造链群体的四种诊断。A、B 只增加高斯仪器展宽；C 只平移峰位，按原标准换算；D 只改变积分终点。各曲线揭示不同计算选择如何影响表观分布，未把这些变化当作实测降解。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/44c18f54d8175d084d7a5ad9.svg?v=44c18f54d817)

图 4同一构造链群体的四种诊断。A、B 只增加高斯仪器展宽；C 只平移峰位，按原标准换算；D 只改变积分终点。各曲线揭示不同计算选择如何影响表观分布，未把这些变化当作实测降解。

下面的交互实验保留两种真实链质量，分别为 10,000 和 100,000 g/mol。先改变长链的数量比例，观察数量很少的长链何时已经占据显著质量；再增加仪器展宽，比较真实与表观平均值；最后移动整个流出位置，模拟尺寸与标准不匹配造成的统一换算偏差。三个控制量回答不同问题，图上可以出现相似的变化，真实链群体却并不总是相同。先只动一个控制量并预测方向，再看计算结果，会比同时拖动所有滑块更容易建立因果关系。

## 同一群链怎样变成不同的表观分布

两种链为 10,000 和 100,000 g/mol。只改变一个控制量，比较真实与表观平均值。高斯展宽与统一峰位移动是这里明确定义的测量模型。

[Figure: 质量加权双峰色谱交互图](https://ml-biomat.com/tutorials/experimental-methods/c02/#C02-plot)

若一个新样品出现很早的肩峰，可以据此设计下一步：检查它是否接近排阻边界，降低进样量确认峰形，改变适当的溶液条件观察聚集是否可逆，再收集该组分进行其他分析。若整个主峰稳定向后移动，首先核对标准和流动条件，然后围绕降解或构象改变选择补充测量。每一种后续动作都对应一个具体解释，SEC 就成为研究路径中的分流点，而不只是最后附上一张曲线。

## 把一条曲线变成能重新检查的完整分析

完整例子同时包含构造模型和公开数据，两者在图注与文件中分别标明。构造模型从一群对数摩尔质量呈正态分布的链出发，计算按质量加权后的色谱，再人为加入可控的仪器展宽。因此可以比较输入的真实平均值与测量模型输出的表观平均值，检查偏差究竟从哪里产生。公开数据部分读取 NBS 表格的累计质量百分数，保留原表的非均匀横坐标和舍入数字，不把它伪装成原始检测器信号。程序会把标准、色谱、展宽扫描和积分范围扫描保存为表格，便于逐项核对。

阅读代码时，建议先找到体积坐标和校准函数，再找到信号面积如何归一化，最后看两个平均值的积分。每个小切片都先有一个质量权重，除以该位置的摩尔质量才能得到与数量有关的权重。这里用数值积分近似连续曲线下面积，坐标间隔已经包含在计算中；若换成间距不均匀的真实采样数据，仍应让积分函数接收实际横坐标。把所有点的高度直接相加，只在间距相同且比例因子能够抵消时才有相应含义。

### 完整 SEC 分布、校准和诊断例子

构造模型与真实公开累计数据分别处理；输出四幅图及可复查的标准、色谱、展宽和积分表。

```
"""SEC/GPC: porous exclusion, calibration, mass weighting and real NBS data.

Run: python main.py --output results --language en
Dependencies: numpy, scipy, matplotlib. Only bundled data are read.
All chromatograms are constructed teaching models. The cumulative SRM curve
is a transcription of the published NBS 1972 table, identified in data/README.md.
"""
from pathlib import Path
import argparse, csv, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True);P.add_argument('--language',choices=['zh','en'],default='en');args=P.parse_args()
O=args.output;O.mkdir(parents=True,exist_ok=True);L=args.language
def t(z,e):return z if L=='zh' else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#25364a','text.color':'#25364a','axes.titleweight':'bold','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','svg.fonttype':'none','savefig.facecolor':'#fcfbf7'})
blue='#167d9a';red='#d35f47';gold='#c49b35';dark='#25364a';green='#37967d'
def save(fig,n):
    fig.savefig(O/f'{n}-{L}.svg',bbox_inches='tight');fig.savefig(O/f'{n}-{L}.png',dpi=145,bbox_inches='tight');plt.close(fig)
def gauss(x,m,s):return np.exp(-.5*((x-m)/s)**2)/(s*np.sqrt(2*np.pi))
def csvsave(n,h,a):np.savetxt(O/n,a,delimiter=',',header=','.join(h),comments='',fmt='%.10g')

# Original mechanism drawing. Side pores hold solvent; macromolecules exchange
# with accessible pore volume. They are not forced through a sieve membrane.
fig,axs=plt.subplots(1,3,figsize=(14.4,4.5),gridspec_kw={'width_ratios':[1.1,1,1]},layout='constrained')
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
ax.add_patch(Rectangle((.4,1),9.1,5.5,facecolor='#e8f0f0',edgecolor='#9aafaf',lw=1.5))
for x,y in [(2,2.4),(5,5),(8,2.4)]:
    ax.add_patch(Circle((x,y),1.1,facecolor='#d6dfd9',edgecolor='#829a8b'))
    for dx,dy in [(-.3,.3),(.35,.1),(0,-.4)]:ax.add_patch(Circle((x+dx,y+dy),.20,facecolor='#fcfbf7',edgecolor='#b4c5bb'))
ax.plot([.5,2,3.3,4,6,7.2,9.3],[4,4,4,3.3,3.3,4.6,4.6],color=red,lw=3)
ax.scatter([.7,9],[4,4.6],s=120,color=red,zorder=5)
ax.plot([.5,2,2,3.4,5,5,6.4,8,8,9.3],[3.4,3.4,2.3,3.4,3.4,4.7,3.6,3.6,2.3,3.6],color=blue,lw=1.8,ls='--')
ax.scatter([.7,9],[3.4,3.55],s=20,color=blue,zorder=5)
ax.text(.5,7.25,t('A  多孔填料中的两种可达空间','A  Two accessible solvent spaces'),weight='bold')
ax.text(.55,.35,t('大分子：孔外较多  /  小分子：也进入孔内','Large: mostly outside  /  Small: also inside'),fontsize=10)
v=np.linspace(0,22,1000);ax=axs[1]
ax.plot(v,gauss(v,8,.6),color=red,label=t('大分子','Macromolecule'));ax.plot(v,gauss(v,16,.8),color=blue,label=t('小分子盐','Small solute / salt'))
ax.axvspan(6,10,color=red,alpha=.09);ax.set(xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('归一化检测信号 / mL⁻¹','Normalized signal / mL⁻¹'),title=t('B  脱盐：先收集大分子','B  Desalting: collect the first band'));ax.legend(frameon=False,fontsize=9)
ax=axs[2];vol=np.linspace(3,18,100);ax.plot(vol,(vol-3)/15,color=green,lw=2.5)
ax.scatter([3,9,18],[0,.4,1],color=[red,gold,blue],zorder=5);ax.set(xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('孔体积可达比例 Kav','Accessible fraction Kav'),ylim=(-.06,1.1),title=t('C  在两个参照体积之间','C  Between two reference volumes'))
ax.annotate(t('完全排阻','Excluded'),(3,0),(5,.07),arrowprops={'arrowstyle':'-','color':dark},fontsize=9);ax.annotate(t('完全进入','Fully included'),(18,1),(12,.82),arrowprops={'arrowstyle':'-','color':dark},fontsize=9)
save(fig,'pores')

# Constructed narrow-standard calibration and lognormal molecular population.
a,b=7.,.25;standards=np.array([1e3,3e3,1e4,3e4,1e5,3e5,1e6]);ve=(a-np.log10(standards))/b
mu,s=4.2,.35;ln10=np.log(10);mass_mu=mu+ln10*s*s
V=np.linspace(2,20,6001);M=10**(a-b*V);ideal=gauss(V,(a-mass_mu)/b,s/b)
def moments(signal):
    area=np.trapezoid(signal,V)
    return float(area/np.trapezoid(signal/M,V)),float(np.trapezoid(signal*M,V)/area)
Mn=10**mu*np.exp(.5*(ln10*s)**2);Mw=10**mu*np.exp(1.5*(ln10*s)**2);disp=Mw/Mn
sig=.25;observed=gauss(V,(a-mass_mu)/b,np.sqrt((s/b)**2+sig**2));mn_obs,mw_obs=moments(observed)
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained')
ax=axs[0,0];ax.plot(ve,standards,'o-',color=blue);ax.set_yscale('log');ax.set(xlabel=t('标准样峰位 / mL','Standard peak volume / mL'),ylabel=t('摩尔质量 / (g/mol)','Molar mass / (g/mol)'),title=t('A  先校准位置','A  Calibrate position first'));ax.text(.04,.1,'log₁₀ M = 7 − 0.25 V',transform=ax.transAxes)
ax=axs[0,1];ax.plot(V,observed,color=blue);ax.fill_between(V,observed,where=(V>10)&(V<11),color=gold,alpha=.5);ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('质量响应 / mL⁻¹','Mass response / mL⁻¹'),title=t('B  面积切片包含质量','B  Each slice contains mass'))
x=np.linspace(2.5,6.5,1000);ax=axs[1,0];ax.plot(x,gauss(x,mu,s),color=green,label=t('按链数归一化','Number density'));ax.plot(x,gauss(x,mass_mu,s),color=red,label=t('按质量归一化','Mass density'));ax.set(xlabel=t('log₁₀ [M / (g/mol)]','log₁₀ [M / (g/mol)]'),ylabel=t('每单位 log₁₀ M 的概率密度','Density per unit log₁₀ M'),title=t('C  同一群链，两种加权','C  Same chains, two weightings'));ax.legend(frameon=False)
ax=axs[1,1];ax.plot(V,np.cumsum(observed)/np.sum(observed)*100,color=blue);ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('已流出质量 / %','Eluted mass / %'),title=t('D  先流出的是大分子','D  Larger molecules elute first'));ax.text(.03,.84,t('此累计方向：大 → 小','This cumulative direction: large → small'),transform=ax.transAxes)
save(fig,'calibration')
csvsave('calibration.csv',['elution_volume_mL','molar_mass_g_per_mol'],np.c_[ve,standards])
csvsave('constructed_chromatogram.csv',['elution_volume_mL','assigned_molar_mass_g_per_mol','ideal_mass_response_per_mL','broadened_mass_response_per_mL'],np.c_[V,M,ideal,observed])

raw=np.genfromtxt(Path(__file__).parent/'data/srm1475_table4.csv',delimiter=',',names=True)
logm=raw['log10_molar_mass_g_per_mol'];cdf=raw['cumulative_mass_percent'];median=10**np.interp(50,cdf,logm)
assert np.all(np.diff(logm)>0) and np.all(np.diff(cdf)>=0) and cdf[0]==0 and cdf[-1]==100
fig,axs=plt.subplots(1,2,figsize=(12.8,4.9),layout='constrained')
ax=axs[0];ax.semilogx(10**logm,cdf,'o-',color=blue,ms=3);ax.axhline(50,color=gold,ls='--',lw=1);ax.axvline(median,color=gold,ls='--',lw=1)
ax.set(xlabel=t('摩尔质量 / (g/mol)','Molar mass / (g/mol)'),ylabel=t('低于横坐标的累计质量 / %','Cumulative mass below M / %'),title=t('A  真实公开数据：聚乙烯 SRM 1475','A  Published data: polyethylene SRM 1475'),ylim=(-2,103))
ax.text(.05,.68,t('1972 年 NBS，表 4\n按质量的中位数 ≈ ','NBS 1972, Table 4\nMass median ≈ ')+f'{median:,.0f} g/mol',transform=ax.transAxes,fontsize=10)
ax=axs[1];xx=np.arange(2);nw=np.array([.9,.1]);ww=np.array([.9*1e4,.1*1e5]);ww/=ww.sum()
ax.bar(xx-.18,nw*100,.34,color=green,label=t('链数占比','Number fraction'));ax.bar(xx+.18,ww*100,.34,color=red,label=t('质量占比','Mass fraction'))
ax.set_xticks(xx,['10,000 g/mol','100,000 g/mol']);ax.set(ylim=(0,110),ylabel=t('占比 / %','Fraction / %'),title=t('B  构造例：90 条短链与 10 条长链','B  Constructed: 90 short and 10 long chains'));ax.legend(frameon=False,ncol=2,loc='upper right',fontsize=9)
for p in ax.patches:ax.text(p.get_x()+p.get_width()/2,p.get_height()+2,f'{p.get_height():.1f}',ha='center',fontsize=10)
save(fig,'mass-distribution')

widths=np.linspace(0,1.2,61);factor=np.exp((ln10*b*widths)**2);rows=[]
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained')
ax=axs[0,0]
for w,c in zip([0,.6,1.2],[blue,gold,red]):
    y=gauss(V,(a-mass_mu)/b,np.sqrt((s/b)**2+w*w));ax.plot(V,y,color=c,label=f'σV = {w:.1f} mL')
ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('质量响应 / mL⁻¹','Mass response / mL⁻¹'),title=t('A  仪器把同一分布展宽','A  Instrument broadening'));ax.legend(frameon=False,fontsize=9)
ax=axs[0,1];ax.plot(widths,disp*factor,color=red);ax.axhline(disp,color=green,ls='--',label=t('真实分散系数','True dispersity'));ax.set(xlabel=t('额外展宽 σV / mL','Extra broadening σV / mL'),ylabel=t('表观分散系数','Apparent dispersity'),title=t('B  展宽被误读为链长差异','B  Width becomes apparent heterogeneity'));ax.legend(frameon=False)
shifts=np.linspace(0,1.2,100);ax=axs[1,0];ax.plot(shifts,100*10**(-b*shifts),color=blue);ax.set(xlabel=t('向后移动的峰位 / mL','Later elution shift / mL'),ylabel=t('表观质量 / 真值 × 100%','Apparent / true mass × 100%'),title=t('C  同一质量，构象变紧凑','C  Same mass, more compact conformation'),ylim=(45,105))
ax=axs[1,1];cuts=np.linspace(12,18,70);mns=[];mws=[]
for cut in cuts:
    keep=V<=cut;ar=np.trapezoid(ideal[keep],V[keep]);mns.append(ar/np.trapezoid((ideal/M)[keep],V[keep]));mws.append(np.trapezoid((ideal*M)[keep],V[keep])/ar)
ax.plot(cuts,np.array(mns)/Mn,color=green,label='Mn');ax.plot(cuts,np.array(mws)/Mw,color=red,label='Mw');ax.axhline(1,color=dark,lw=.8,ls='--');ax.set(xlabel=t('积分终点 / mL','Integration endpoint / mL'),ylabel=t('截取值 / 完整值','Truncated / full value'),title=t('D  删掉小分子尾部的代价','D  Cost of deleting the low-mass tail'));ax.legend(frameon=False)
save(fig,'diagnostics')
csvsave('broadening.csv',['extra_sigma_mL','apparent_dispersity_analytic'],np.c_[widths,disp*factor])
csvsave('integration_sensitivity.csv',['integration_endpoint_mL','Mn_g_per_mol','Mw_g_per_mol'],np.c_[cuts,mns,mws])
toy_mn=.9*1e4+.1*1e5;toy_mw=(.9*1e8+.1*1e10)/toy_mn
summary={'Kav_example':.4,'toy_Mn_g_per_mol':toy_mn,'toy_Mw_g_per_mol':toy_mw,'toy_dispersity':toy_mw/toy_mn,'lognormal_true_Mn':float(Mn),'lognormal_true_Mw':float(Mw),'lognormal_true_dispersity':float(disp),'broadened_Mn':mn_obs,'broadened_Mw':mw_obs,'broadened_dispersity':mw_obs/mn_obs,'NBS_table_rows':len(raw),'NBS_mass_median_log_interpolation_g_per_mol':float(median),'NBS_reported_Mn_g_per_mol':17900,'NBS_reported_Mw_g_per_mol':52900,'NBS_reported_dispersity':52900/17900,'half_mL_shift_mass_ratio':10**(-.25*.5)}
assert abs(toy_mn-19000)<1e-8 and abs(toy_mw-57368.42105263158)<1e-7
assert abs(mn_obs/(Mn*np.exp(-.5*(ln10*b*sig)**2))-1)<1e-5
assert abs(mw_obs/(Mw*np.exp(.5*(ln10*b*sig)**2))-1)<1e-5
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

最后，把结论写成一个明确的实验回答。例如，在相同溶剂、温度、标准体系和积分规则下，两批可溶聚合物的表观分布是否变化，变化主要发生在主峰、短链尾部还是高质量肩峰；对于蛋白质，收集的峰是否对应后续实验需要的主要尺寸组分，以及回收的质量是否足够。保存分布本身、两个平均值和测量条件，比只保存一个“分子量”更能支撑之后的讨论。下一章的质谱将从另一种信号进入分子世界：它按离子的质荷比分开物种，与本章按溶液尺寸分配的机制形成清楚的互补。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Waters: Calibration of the GPC system](https://www.waters.com/nextgen/us/en/education/primers/beginners-guide-to-size-exclusion-chromatography/calibration-of-the-gpc-system1.html)

   常规、相对与通用校准的条件。
2. [Cytiva: Size exclusion chromatography selection guide](https://cdn.cytivalifesciences.com/api/public/content/digi-13947-pdf)

   孔道、脱盐与高分辨率分离、进样体积。
3. [Porath: Citation Classic retrospective on gel filtration](https://garfield.library.upenn.edu/classics1981/A1981LM54000002.pdf)

   波拉特对早期淀粉柱与交联葡聚糖发现的第一人称回顾。
4. [NIST author manuscript: Size-exclusion chromatography](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=933552)

   SEC 历史、平衡尺寸分配、额外相互作用和展宽。
5. [Malvern Panalytical: An introduction to SEC/GPC](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp150625introtosecgpc)

   溶液尺寸、检测器与摩尔质量解释。
6. [Ross and Frolen (1972): Polyethylene SRM 1475, gel permeation chromatography](https://nvlpubs.nist.gov/nistpubs/jres/76A/jresv76An2p163_A1b.pdf)

   表 4 真实累计质量数据及该分布报告的平均值。

   NBS government-authored numerical table; reproduced with attribution under NIST public-information policy.
