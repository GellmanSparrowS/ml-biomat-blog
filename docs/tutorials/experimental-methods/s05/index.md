# 圆二色谱：蛋白质折叠留下的光学线索

Source: https://ml-biomat.com/tutorials/experimental-methods/s05/
Language: zh-CN

从两种旋向光的微小吸收差，读出蛋白质整体构象的变化，再把浓度、参考光谱与升温条件纳入判断。

## 蛋白质还在，折叠是否已经改变？

把蛋清加热，透明的液体会逐渐变成白色固体。这个变化让我们直观看见蛋白质结构与相互作用发生了改变，但研究中的变化往往早得多，也细微得多：一种酶在储存后活性下降，溶液仍然清澈；蛋白质吸附到材料表面后，数量没有明显变化，作用方式却不同了。此时需要知道的不只是“有没有蛋白质”，还包括蛋白质链是否仍以原来的方式排列。圆二色谱，通常简称 CD，能够用溶液中蛋白质对两种偏振光的细微差别，观察这类构象变化。

先把结构层次分开。蛋白质由氨基酸连接成长链，连接顺序叫序列。链的某些片段按规则卷成 α 螺旋，另一些片段彼此并排形成 β 折叠；这些局部排列属于二级结构。整条链进一步折叠、把不同片段放到相应位置，形成三级结构。像一根写着特定字母顺序的长带，既有局部卷绕方式，也有整体收拢方式。相同的字母顺序可以处在不同构象中，所以只知道分子量或蛋白质含量，还没有回答折叠是否保持。

常见的远紫外 CD 关注肽链骨架的光学响应，帮助比较螺旋、折叠和其他构象的整体组成。近紫外 CD 则更多地利用芳香侧链等基团所处的不对称环境，提供关于整体折叠的另一类线索。两种观察的波段、信号强度和样品需求不同。读到“CD 表明结构发生变化”时，应继续看它测了哪一段波长、比较的是谱形还是幅度，以及浓度和光程是否已经统一；这些信息决定结构解释的具体含义。

本篇从左右手的差别讲到偏振光，再把仪器读出的毫度转换成可比较的结构信号。我们将构造一组明确标记的教学光谱，观察结构比例、浓度误差和测量波段如何影响分析，并用升温曲线练习定义转变中点。这样，CD 的曲线不再只是几条有正峰和负峰的线，而成为连接蛋白质样品状态、光学条件和研究判断的一条完整测量链。

## 两种旋转的光，为何会看到不同的分子？

把左手放在镜子前，镜中看起来像右手；无论怎样平移或旋转，左右手都不能完全重合。这种与镜像不能重合的性质叫手性。分子也可以具有手性，而蛋白质中氨基酸的排列及其折叠会构成多层次的不对称环境。手性不是“大分子一定绕成螺旋”的同义词：一个局部化学结构可以具有手性，一个吸光基团也可以因为周围环境不对称而表现出 CD。研究对象与哪一种电子跃迁相互作用，决定了具体波段的信号。

光是一种电磁波。讨论偏振时，可以先关注电场方向：线偏振光在固定方向上来回变化，圆偏振光在固定空间位置上的电场方向则随时间转动。两种相反转向的圆偏振光具有相同波长，却可以与手性样品发生略有不同的吸收。这里旋转的是电场方向，并不是光束像弹簧一样沿弯曲路线穿过样品。左右旋的命名还依赖观察方向与约定，因此处理仪器导出的正负信号时，应保持其定义一致，而不凭一张旋转箭头图重新指定符号。

![原创电场合成与检测原理图。虚线是相反转向的圆分量，绿色为合成轨迹；振幅相等时得到直线，不等时得到椭圆。C 显示现代调制检测的功能顺序，连接 Cotton 的光学观察与后来的光电测量；不复原具体历史设备。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/707b051d05e2654c85221fca.svg?v=707b051d05e2)

图 1原创电场合成与检测原理图。虚线是相反转向的圆分量，绿色为合成轨迹；振幅相等时得到直线，不等时得到椭圆。C 显示现代调制检测的功能顺序，连接 Cotton 的光学观察与后来的光电测量；不复原具体历史设备。

十九世纪末，Cotton 对有色手性溶液的研究把左右圆偏振光的吸收差异与出射光的椭圆偏振联系起来。到 1950 年，Mitchell 在讨论光电测量方法时仍以这两条观察路线说明 CD：可以比较两种圆偏振光的吸收，也可以测量出射光的椭圆程度。这个历史联系解释了今天看似奇怪的单位：研究者讨论的是吸收差，仪器常常却输出一个角度。它们描述同一光学差别的不同表达形式，而不是两种无关的测量。

$$
\Delta A=A_L-A_R
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b807cb2100c99c9e97d19c.svg) | 左右圆偏振光吸光度差，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/90999a9e9d00fa32ceb64a06.svg) | 左圆偏振吸光度，采用仪器一致的旋向约定，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f8a382ff514ba7cfa60fce3.svg) | 右圆偏振吸光度，无量纲。 |

比较相同波长与条件下的两个吸收值。0.5003−0.4997=0.0006；正负表示哪种旋向吸收更强，而不是光强为负。

如果左旋吸光度是 0.5003，右旋是 0.4997，二者平均吸光度接近 0.5，但差值只有 0.0006。这是一个大背景上的小差别。正 CD 表示按本篇约定左旋吸收更强，负 CD 表示右旋吸收更强；负峰不意味着样品产生了负吸收，也不意味着光强为负。它与上一节讨论的普通吸光度不同：普通吸收主要回答损失了多少光，CD 专门比较两种偏振状态损失量的差异。

现代仪器常借助光弹调制器快速改变偏振状态，再从探测器信号中提取与调制同步的微小变化。快速交替有助于让两种状态在接近相同的光源和样品条件下比较，但它仍需要足够的透射光。如果样品几乎把紫外光全部吸收，探测器再提高增益，也无法凭空增加通过样品的光子。理解这一点，会让后面的光程、缓冲液和高压监测不再像零散的操作要求。

## 毫度、浓度和平均残基：先让曲线站在同一把尺上

两束旋转方向相反、振幅相等的圆偏振分量可以合成为线偏振光。若样品使它们衰减得不同，合成电场的端点就会描出椭圆；椭圆率用一个角度描述长短轴的比例。实际 CD 信号很小，通常写成毫度，也就是一度的千分之一。在小信号条件下，椭圆率与吸光度差近似成正比，所以仪器可以在这两种表达之间换算。它不是把蛋白质本身转过的角度，也不是直接测量螺旋的几何扭转角。

$$
\theta_{\mathrm{mdeg}}\approx32980\,\Delta A
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e32cd7c782aaca32cd9cb448.svg) | 椭圆率角度的毫度数值，mdeg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b807cb2100c99c9e97d19c.svg) | 左右圆偏振吸光度差，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a78b5a609fa453a7cb2f8ab4.svg) | 吸光度差换算为毫度的近似系数，mdeg。 |

小椭圆率时，圆分量振幅差与吸光度差近似线性；对数吸收定义和弧度到角度的换算给出此系数。ΔA=0.0006 时约为 19.788 mdeg。

同一蛋白质溶液浓度加倍，光路中与光相互作用的分子通常也加倍，毫度信号便会随之增加；光程加倍也会产生类似效果。因此两条原始曲线一条更深，可能仅仅意味着样品更多。为了比较结构，需要把信号除以分子数量与光程。蛋白质大小又不同，一条长链包含的肽链单位比短链多，于是常进一步按平均氨基酸残基归一化，得到平均残基椭圆率。所谓残基，是氨基酸进入链后所留下的结构单元。

$$
[\theta]_{\mathrm{MR}}=\frac{\theta_{\mathrm{mdeg}}\,M_R}{10\,c_m\,l}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b20f1a1290e61c97a2fe6f9f.svg) | 平均残基椭圆率，deg·cm²·dmol⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e32cd7c782aaca32cd9cb448.svg) | 已扣匹配空白的椭圆率，mdeg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cad38889865553ac191f2a12.svg) | 平均氨基酸残基摩尔质量，g·mol⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/46293108d95e427e874bd905.svg) | 蛋白质质量浓度，mg·mL⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b725c065245400348075701d.svg) | 光程，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e2574f61b59164e433af2aee.svg) | 与本式指定浓度、角度和摩尔单位配套的数值换算因子。 |

信号除以残基浓度和光程后才可比较。−20 mdeg、MR=110 g/mol、cm=0.20 mg/mL、l=0.10 cm 得到 −11000 deg·cm²·dmol⁻¹。1 mm=0.10 cm；改变浓度单位必须同步改变换算因子。

举一个可以直接核对单位的例子：原始椭圆率为 −20 mdeg，平均残基摩尔质量取 110 g/mol，质量浓度为 0.20 mg/mL，光程为 0.10 cm。代入后得到 −11000 deg·cm²·dmol⁻¹。这里 0.10 cm 就是 1 mm；若误把 1 mm 写成 1 cm，结果会差十倍。若实际浓度为 0.20 mg/mL，却按 0.25 mg/mL 计算，归一化幅度则会缩小到正确值的 80%。这不是画图缩放的小问题，因为结构比例拟合常利用整条光谱的幅度。

平均残基摩尔质量应尽量按实际序列与分子量计算。用 110 作为教学近似有助于估算，但标签、修饰、特殊组成或较短肽链可能需要更具体的处理。浓度测量也要与样品相适应：若用紫外吸收，应知道对应消光系数及干扰物；若用显色法，应检查目标蛋白质与标准蛋白质的响应差异。CD 分析中看似很漂亮的曲线，可能仍受到浓度误差控制。把浓度、光程和单位写清楚，才能比较不同批次、不同蛋白质或不同实验室的结果。

## 把紫外光送到探测器，比把曲线磨平更重要

远紫外区常常是最有结构信息、也最难透光的区域。蛋白质、缓冲液、盐、添加剂和比色皿共同决定有多少光能穿过。短光程石英池能减少总吸收，但同时也减少 CD 信号；较高蛋白质浓度可以补回一部分信号，却可能引入聚集或浓度依赖的构象变化。合适条件因此不是一个固定浓度，而是样品状态、总吸收和所需波长范围之间的配合。先保住蛋白质的研究状态，再选择能测到目标波段的光程与缓冲条件。

背景必须与样品中的最终缓冲液匹配。蛋白质储液带入的盐、甘油、还原剂或少量溶剂，稀释后仍可能影响低波长透过率；若空白只用了另一瓶看似相同的缓冲液，差异可能被误留在扣背景后的曲线里。换液后的缓冲液或按实际组成配制的空白，更接近这条测量链。空白光谱还可以揭示比色皿残留、位置变化或应力双折射。每次插入方向保持一致，能减少几何条件变化给微小差值带来的影响。

许多仪器同时记录光电倍增管的高压或相关增益指标。透过光减少时，仪器提高增益以维持可测输出，所以该信号能提示低波长端是否已经缺少光子。可接受范围依赖具体探测器和仪器，不能把某台设备的电压阈值当成所有 CD 仪器的通用标准。观察到高压明显升高或重复扫描突然分散时，优先检查总吸收、光程和样品，而不是直接把曲线平滑到看起来连续。平滑能减少高频波动的外观，却补不回未被可靠记录的信息。

扫描速度、积分时间和光谱带宽也要一起考虑。若仪器在一个积分时间内扫过很宽的波长区间，邻近波长的信息会被混合，峰可能变钝或发生滞后。增加重复扫描并求平均有助于降低独立随机噪声，但样品随时间变化时，平均值会把这种变化一起混入。保留每次扫描，可以发现蛋白质正在聚集、沉降或因温度变化而缓慢重排。对生物大分子而言，样品在测量期间保持什么状态，往往比最后得到多少位小数更值得追踪。

![同一教学样品的原始重复扫描、匹配空白、扣空白结果和浓度归一化。D 中错误采用偏高浓度，使幅度缩小到正确值的 80%。归一化纵轴以 10³ deg·cm²·dmol⁻¹ 为一单位。所有曲线均由明确设定的测量模型生成。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0f61bde1af7eca4991e4eebe.svg?v=0f61bde1af7e)

图 2同一教学样品的原始重复扫描、匹配空白、扣空白结果和浓度归一化。D 中错误采用偏高浓度，使幅度缩小到正确值的 80%。归一化纵轴以 10³ deg·cm²·dmol⁻¹ 为一单位。所有曲线均由明确设定的测量模型生成。

图中把同一组教学样品的信号、背景和重复波动放在一起，并显示浓度归一化的影响。低波长区的信息不能只靠“截掉不好看的部分”处理：应给出为什么从某个波长开始使用数据，随后选择支持这个范围的参考集和分析方法。若一个方法要求包含更短波长，输入较窄谱段后仍得到一组百分比，并不意味着缺失信息已经被恢复。测量范围是结构分析的一部分，应该与结果一起解释。

## 结构比例像配色：组合能解释什么，哪里需要更多信息？

还要留意“整体比例”中的整体指什么。CD 通常同时接收光路中许多分子的响应，因此一个 50% 的平均螺旋比例，可能来自每个分子约一半链段形成螺旋，也可能来自多个构象群体的平均。只凭这一个平均值，还无法确定每个分子的具体状态。这个区别在折叠中间态、蛋白质混合物或部分聚集的样品中特别重要：平均谱形的变化可以来自同一群体内部重排，也可以来自不同群体所占比例改变。色谱分离、时间跟踪或其他结构观察，能够帮助把这两类情况进一步分开。

α 螺旋常在约 208 nm 与 222 nm 出现负带，在更短波长出现正带；β 折叠的典型谱形不同，而缺少稳定规则排列的链段又有另一类响应。这些特征帮助我们建立直觉，但蛋白质不是由几种完全固定的标准颜料组成。螺旋长度、折叠几何、侧链贡献、溶剂和不同结构之间的相互作用，都可能改变谱形。看到两个负峰可以支持进一步检查螺旋特征，却不应直接把某一个峰高换成一个普遍适用的螺旋百分比。

$$
y(\lambda)=\sum_{j=1}^{K}f_jS_j(\lambda)+r(\lambda),\qquad f_j\geq0,\quad\sum_{j=1}^{K}f_j=1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1dc9052b8842180988a4a8b2.svg) | 样品在波长 λ 的归一化椭圆率，deg·cm²·dmol⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 模型的参考组分数，本例为 3。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 组分编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea0efbb08d1d6502e2a12fed.svg) | 第 j 组分比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ab55d9e555768c0f2cd2ac4.svg) | 第 j 参考光谱，与 y 采用相同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d2c3a93795434a5ba3f1e2c2.svg) | 数据与组合模型之差，包含噪声和未解释贡献，与 y 同单位。 |

按比例叠加各参考响应。0.55、0.25、0.20 非负且总和为 1。参考必须匹配对象与波段；本例构造基础曲线只用于理解组合与误差传递。

线性组合模型提供一个清楚的起点：把若干参考光谱按比例加起来，寻找能解释样品曲线的组合。像用几种基础颜色调出目标颜色，比例必须与采用的参考体系相匹配。拟合时常要求比例非负、总和为一，这表达了各部分组成一个整体的条件。真正的分析工具通常使用经过结构表征的蛋白质参考集和经过检验的算法，而本篇代码使用人为构造的三条基础曲线，只用于展示组合、残差和灵敏度，不把它们作为真实蛋白质数据库。

本例设定螺旋、折叠与其他构象的比例分别为 0.55、0.25 和 0.20，再加入背景与重复测量波动。分析先扣除匹配背景，按浓度和光程归一化，然后用约束拟合估计比例。残差告诉我们模型在哪些波长还没有解释数据；重复样本或噪声重采样展示估计受读数波动影响的程度。重采样区间只覆盖所设定的噪声，不自动包含浓度误差、参考集不适合或模型缺项。因此我们另外改变浓度和低波长截点，观察结果如何移动。

![A 的三条构造基础曲线用于解释组合；B 同时展示混合拟合与残差，纵轴单位为 10³ deg·cm²·dmol⁻¹。C 改变最低波长，误差棒为 160 次指定噪声重采样的两倍标准差；D 单独改变采用的浓度。点虚线标记设定比例，结构库误差未加入这些教学计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/522ccbb65a33d2aab28fe70b.svg?v=522ccbb65a33)

图 3A 的三条构造基础曲线用于解释组合；B 同时展示混合拟合与残差，纵轴单位为 10³ deg·cm²·dmol⁻¹。C 改变最低波长，误差棒为 160 次指定噪声重采样的两倍标准差；D 单独改变采用的浓度。点虚线标记设定比例，结构库误差未加入这些教学计算。

## 是结构变了，还是归一化变了？

改变螺旋比例观察谱形，再把实际浓度与用于归一化的浓度一起改变。随后只改其中一个，比较两幅图。剩余非螺旋部分按 55% 折叠、45% 其他构象分配；参考曲线为教学构造，光程固定 0.10 cm，平均残基摩尔质量取 110 g/mol。

绿色曲线为当前结果，右图灰色虚线是正确浓度归一化的曲线。纵轴 10³ 单位对应 10³ deg·cm²·dmol⁻¹。

交互图让你改变螺旋比例，并把剩余部分按指定比例分给折叠和其他构象。它同时显示原始毫度与归一化光谱：改变浓度时，前者变化，正确归一化后的后者保持一致；输入错误的归一化浓度时，后者也会被错误缩放。这个实验把一个常见误解拆开：仪器并不直接输出“55% 螺旋”，它输出光学差值；结构比例是依赖样品信息和参考模型的下一层解释。

选择参考集时，要看它是否包含与研究对象相近的结构类型。以球状蛋白质为主的集合，未必充分代表胶原三螺旋、长卷曲螺旋、膜环境中的蛋白质或某些聚集体。不同结构之间的谱形相似性也会影响区分能力：如果两条参考曲线在使用波段内很相像，很多相邻比例都能产生相似拟合。此时扩大可靠波段、加入独立结构观察，或把结论表述为“整体谱形发生一致变化”，通常比过度解释末位百分数更贴近实验信息。

## 跟着温度观察折叠：中点为什么要有基线？

只测一个波长能节省时间，却会丢失谱形变化的信息。可以先在几个代表温度采集完整光谱，再选择对目标变化敏感、且透射条件可靠的波长做密集温度扫描。如果一组光谱近似通过同一个交点，说明在这些条件下某些响应变化彼此抵消，这常可为简单组合模型提供线索；但交点也可能由更多组分或相互补偿的变化形成。检查整组光谱的残差与可逆性，比仅凭一个交点宣布存在两个结构状态更能说明模型与数据的关系。

若一种蛋白质在 222 nm 有明显螺旋相关信号，可以在升温过程中跟踪这一波长。随着构象改变，信号从低温状态向高温状态过渡。曲线像一个斜放的台阶，但台阶两端通常也会随温度缓慢变化：折叠态与展开态各自的光学响应都可能有温度依赖。直接取最低点与最高点的平均值，可能把两端基线的倾斜误当成转变。因此分析应在同一温度上比较两种状态预期的基线。

$$
f_U(T)=\frac{y(T)-y_F(T)}{y_U(T)-y_F(T)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38d847ee4f90227f3c1be623.svg) | 两态线性响应模型中的展开比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 温度，本例用 °C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48104f5cab9f6f1a70ef94f5.svg) | 温度 T 的观测信号，本例为 mdeg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/52bd6fd49934aeeb04b153c1.svg) | 同一温度下折叠态基线信号，mdeg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a600d0bd5b133dd9faf3ebe2.svg) | 同一温度下展开态基线信号，mdeg。 |

观测信号在两条状态基线之间线性插值。yF=−24、yU=−2、y=−13 时 fU=0.5。只有平衡、可逆且两态模型适用时，才将这一比例进一步解释为相应的平衡展开人口。

例如某温度下折叠态基线是 −24，高温态基线是 −2，而实际读数为 −13，那么按两态线性响应得到展开比例 0.5。若已满足平衡、可逆且两态描述适用，这个比例对应转变中点。代码用一个带倾斜基线的经验 S 形模型生成教学升温数据，并拟合中点与过渡宽度。宽度参数描述曲线在多少摄氏度范围内变化，不直接等于热力学焓。要从温度曲线讨论自由能或焓，还需要相应平衡模型及实验条件支持。

![构造的升温信号与经验模型拟合，包含两条倾斜状态基线。偏移的冷却曲线用于解释路径依赖。右图在同温度基线之间归一化，模型比例为 0.5 的位置定义该模型的中点；把它解释为平衡热稳定性还需要可逆与平衡条件。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2a4ded1e9856a2a405558835.svg?v=2a4ded1e9856)

图 4构造的升温信号与经验模型拟合，包含两条倾斜状态基线。偏移的冷却曲线用于解释路径依赖。右图在同温度基线之间归一化，模型比例为 0.5 的位置定义该模型的中点；把它解释为平衡热稳定性还需要可逆与平衡条件。

升温之后再降温，是一次很有信息量的检查。如果冷却后谱形恢复，并且不同扫描速率与等待时间下得到一致曲线，平衡描述就有更好的实验基础。若冷却曲线与升温曲线分离，或样品出现浑浊与沉淀，则需要考虑重折叠缓慢、聚集或不可逆变化。图中专门加入一条人为偏移的冷却曲线，说明相同的 S 形外观可以对应不同的实验路径；它不是某种具体蛋白质的实测热稳定性结果。

### 从重复扫描到组合拟合与温度中点

程序生成明确标记的教学数据，保留空白与重复扫描，计算浓度与波段灵敏度，并拟合带基线的经验热转变。全部图与 CSV 来自实际执行。

```
"""CD measurement and interpretation using explicit teaching models.
Run: python main.py --output results --language en
All spectra are constructed; the basis curves are not a protein reference library.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import minimize,curve_fit
from scipy.special import expit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#263d49','axes.labelcolor':'#263d49','axes.edgecolor':'#9bacb1','svg.fonttype':'path'})
cols=['#078579','#265f85','#d6604d'];gray='#84969b';gold='#bb9033'
def save(f,n):
 f.savefig(out/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{a.language}.png',dpi=155,bbox_inches='tight');plt.close(f)
def title(ax,l,z,e):ax.set_title(l+'  '+tr(z,e),loc='left',weight='bold',pad=14)

# Polarization components are schematic field amplitudes, not beam trajectories.
fig,axs=plt.subplots(1,3,figsize=(12.4,4.1))
u=np.linspace(0,2*np.pi,300)
for ax,k,heading in zip(axs[:2],[1,.65],[('等幅分量 → 直线','Equal components → line'),('不等幅分量 → 椭圆','Unequal components → ellipse')]):
 x=np.cos(u)+k*np.cos(u);y=np.sin(u)-k*np.sin(u)
 ax.plot(np.cos(u),np.sin(u),color=cols[1],alpha=.4,ls='--');ax.plot(k*np.cos(u),-k*np.sin(u),color=cols[2],alpha=.4,ls='--');ax.plot(x,y,color=cols[0],lw=3)
 ax.annotate('',xy=(np.cos(.8),np.sin(.8)),xytext=(np.cos(.55),np.sin(.55)),arrowprops={'arrowstyle':'->','color':cols[1]})
 ax.annotate('',xy=(k*np.cos(.8),-k*np.sin(.8)),xytext=(k*np.cos(.55),-k*np.sin(.55)),arrowprops={'arrowstyle':'->','color':cols[2]})
 ax.set_aspect('equal');ax.set(xlim=(-2.2,2.2),ylim=(-1.4,1.4),xlabel=tr('电场分量 x（相对）','Field x (relative)'),ylabel=tr('电场分量 y（相对）','Field y (relative)'));title(ax,'A' if k==1 else 'B',*heading)
ax=axs[2];ax.axis('off');ax.set_xlim(0,5);ax.set_ylim(0,5)
for y,z,e in [(4,'选定波长与线偏振','Selected wavelength / linear polarization'),(2.8,'调制两种旋向','Modulate opposite handedness'),(1.6,'样品产生吸收差','Specimen absorbs differently'),(.4,'同步读取光电信号','Read synchronized detector signal')]:
 ax.add_patch(Rectangle((.3,y-.28),4.3,.6,fc='#e8efed',ec=gray));ax.text(2.45,y+.02,tr(z,e),ha='center',va='center',fontsize=9)
 if y>.4:ax.annotate('',xy=(2.45,y-.88),xytext=(2.45,y-.3),arrowprops={'arrowstyle':'-|>','color':cols[1]})
title(ax,'C','光电比较','Detect the difference')
fig.text(.5,.01,tr('Cotton 的吸收差与椭圆率联系，延续到光电测量。示意图不复原某台历史仪器。','Cotton linked differential absorption to ellipticity; photoelectric methods measure the difference. Conceptual apparatus, not a historical reconstruction.'),ha='center',fontsize=9)
fig.tight_layout(rect=[0,.08,1,1]);save(fig,'polarization')

# Basis units are mean residue ellipticity, deg cm^2 dmol^-1.
w=np.arange(190.,251.)
def g(mu,sd):return np.exp(-.5*((w-mu)/sd)**2)
basis=1000*np.column_stack([35*g(193,5)-23*g(208,5)-20*g(222,6),22*g(195,6)-17*g(218,8),-30*g(198,6)+3*g(220,9)])
truth=np.array([.55,.25,.20]);mre=basis@truth
concentration=.20;path=.10;mrw=110.;factor=10*concentration*path/mrw
background=.8+.01*(w-220);rng=np.random.default_rng(550)
scans=mre[:,None]*factor+background[:,None]+rng.normal(0,.25,(len(w),5))
blanks=background[:,None]+rng.normal(0,.08,(len(w),8))
corrected=scans.mean(axis=1)-blanks.mean(axis=1);normalized=corrected/factor
def fractions(y,mask=None):
 if mask is None:mask=np.ones(len(w),bool)
 X=basis[mask]/1000;target=y[mask]/1000
 r=minimize(lambda f:np.mean((X@f-target)**2),[.4,.3,.3],method='SLSQP',bounds=[(0,1)]*3,constraints=[{'type':'eq','fun':lambda f:f.sum()-1}],options={'ftol':1e-12,'maxiter':300})
 if not r.success:raise RuntimeError(r.message)
 return r.x
fit=fractions(normalized);fitted=basis@fit
fig,axs=plt.subplots(2,2,figsize=(11.6,7.6))
axs[0,0].plot(w,scans,lw=.8,alpha=.55,color=cols[1]);axs[0,0].plot(w,scans.mean(axis=1),lw=2,color=cols[1]);axs[0,0].set_ylabel(tr('原始椭圆率 / mdeg','Raw ellipticity / mdeg'));title(axs[0,0],'A','五次样品扫描','Five specimen scans')
axs[0,1].plot(w,blanks,lw=.8,alpha=.4,color=gray);axs[0,1].plot(w,blanks.mean(axis=1),color=gray,lw=2);axs[0,1].set_ylabel(tr('空白椭圆率 / mdeg','Blank ellipticity / mdeg'));title(axs[0,1],'B','匹配缓冲空白','Matched buffer blanks')
axs[1,0].plot(w,corrected,color=cols[0],lw=2);axs[1,0].set_ylabel(tr('扣空白信号 / mdeg','Blank-corrected / mdeg'));title(axs[1,0],'C','先做光学比较','Subtract before normalization')
axs[1,1].plot(w,normalized/1000,color=cols[0],lw=2,label=tr('正确浓度 0.20 mg/mL','Correct concentration 0.20 mg/mL'));axs[1,1].plot(w,normalized*.8/1000,color=cols[2],ls='--',label=tr('误用 0.25 mg/mL','Incorrectly use 0.25 mg/mL'));axs[1,1].set_ylabel(tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));axs[1,1].legend(fontsize=8,frameon=False);title(axs[1,1],'D','归一化也会引入系统误差','Normalization can introduce bias')
for ax in axs.flat:ax.set_xlabel(tr('波长 / nm','Wavelength / nm'));ax.axhline(0,color=gray,lw=.6)
fig.tight_layout();save(fig,'measurement')

boot=np.array([fractions(mre+rng.normal(0,.25/np.sqrt(5)/factor,len(w))) for _ in range(160)])
cuts=[190,205,220];cutfit=np.array([fractions(normalized,w>=v) for v in cuts]);cutboot=np.array([[fractions(mre+rng.normal(0,.25/np.sqrt(5)/factor,len(w)),w>=v) for _ in range(160)] for v in cuts]);cutSD=np.std(cutboot,axis=1,ddof=1);scales=np.array([.8,1.,1.2]);scalefit=np.array([fractions(normalized/v) for v in scales])
fig,axs=plt.subplots(2,2,figsize=(11.6,7.8));names=[tr('螺旋','Helix'),tr('折叠','Sheet'),tr('其他','Other')]
for k in range(3):axs[0,0].plot(w,basis[:,k]/1000,color=cols[k],label=names[k])
axs[0,0].legend(frameon=False,fontsize=9);axs[0,0].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));title(axs[0,0],'A','构造参考，解释组合','Constructed references explain mixing')
axs[0,1].plot(w,normalized/1000,'o',ms=3,color=gray,label=tr('测量模型','Measurement model'));axs[0,1].plot(w,fitted/1000,color=cols[0],lw=2,label=tr('约束组合','Constrained mixture'));axs[0,1].plot(w,(normalized-fitted)/1000,color=cols[2],label=tr('残差','Residual'));axs[0,1].legend(frameon=False,fontsize=9);axs[0,1].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));title(axs[0,1],'B','拟合之外还看残差','Inspect residuals as well as fit')
for k in range(3):
 axs[1,0].errorbar(cuts,cutfit[:,k],yerr=2*cutSD[:,k],fmt='-o',capsize=4,color=cols[k],label=names[k]);axs[1,0].axhline(truth[k],color=cols[k],ls=':',alpha=.4)
 axs[1,1].plot(scales,scalefit[:,k],'-o',color=cols[k],label=names[k]);axs[1,1].axhline(truth[k],color=cols[k],ls=':',alpha=.4)
axs[1,0].set(xlabel=tr('最低使用波长 / nm','Lowest fitted wavelength / nm'),ylabel=tr('拟合比例','Fitted fraction'),ylim=(0,.75));axs[1,0].legend(frameon=False,fontsize=9);title(axs[1,0],'C','波段改变可用信息','Wavelength coverage changes information')
axs[1,1].set(xlabel=tr('采用浓度 / 实际浓度','Assumed / actual concentration'),ylabel=tr('拟合比例','Fitted fraction'),ylim=(0,1));axs[1,1].legend(frameon=False,fontsize=9);title(axs[1,1],'D','浓度误差传到结构解释','Concentration error reaches interpretation')
fig.tight_layout();save(fig,'mixture')

T=np.linspace(20,90,71)
def thermal(temp,f0,fs,u0,us,mid,width):
 unfolded=expit((temp-mid)/width);return (f0+fs*(temp-20))*(1-unfolded)+(u0+us*(temp-20))*unfolded
thermal_true=[-25,.02,-3,.01,60,4]
heating=thermal(T,*thermal_true)+rng.normal(0,.12,len(T))
params,cov=curve_fit(thermal,T,heating,p0=thermal_true,bounds=([-50,-.5,-20,-.5,35,.5],[0,.5,20,.5,80,15]),maxfev=15000)
cooling=thermal(T,-25,.02,-3,.01,57,4)
frac=expit((T-params[4])/params[5]);baselineF=params[0]+params[1]*(T-20);baselineU=params[2]+params[3]*(T-20)
fig,axs=plt.subplots(1,2,figsize=(11.6,4.8));axs[0].scatter(T,heating,s=15,color=cols[1],alpha=.6,label=tr('构造升温读数','Constructed heating readings'));axs[0].plot(T,thermal(T,*params),color=cols[1],label=tr('升温拟合','Heating fit'));axs[0].plot(T,cooling,color=cols[2],ls='--',label=tr('示意冷却路径','Illustrative cooling path'));axs[0].plot(T,baselineF,color=gray,ls=':',lw=1);axs[0].plot(T,baselineU,color=gray,ls=':',lw=1);axs[0].set(xlabel=tr('温度 / °C','Temperature / °C'),ylabel=tr('222 nm 椭圆率 / mdeg','222 nm ellipticity / mdeg'));axs[0].legend(frameon=False,fontsize=9);title(axs[0],'A','同一信号，不同温度路径','One signal, different temperature paths')
axs[1].plot(T,frac,color=cols[0],lw=3);axs[1].axhline(.5,color=gray,ls='--');axs[1].axvline(params[4],color=gray,ls='--');axs[1].text(params[4]+2,.2,tr(f'中点 {params[4]:.2f} °C',f'Midpoint {params[4]:.2f} °C'),fontsize=10);axs[1].set(xlabel=tr('温度 / °C','Temperature / °C'),ylabel=tr('基线修正后的模型展开比例','Baseline-corrected model unfolded fraction'),ylim=(-.03,1.03));title(axs[1],'B','在同温度基线之间定位','Locate between same-temperature baselines')
fig.tight_layout();save(fig,'thermal')
np.savetxt(out/'spectra.csv',np.column_stack([w,scans,blanks.mean(axis=1),corrected,normalized,fitted]),delimiter=',',header='wavelength_nm,scan1_mdeg,scan2_mdeg,scan3_mdeg,scan4_mdeg,scan5_mdeg,blank_mean_mdeg,corrected_mdeg,mean_residue_ellipticity,fitted_mean_residue_ellipticity',comments='')
np.savetxt(out/'basis.csv',np.column_stack([w,basis]),delimiter=',',header='wavelength_nm,constructed_helix,constructed_sheet,constructed_other',comments='')
np.savetxt(out/'thermal.csv',np.column_stack([T,heating,thermal(T,*params),cooling,frac]),delimiter=',',header='temperature_C,heating_mdeg,fitted_mdeg,cooling_model_mdeg,model_unfolded_fraction',comments='')
np.savetxt(out/'fraction_resampling.csv',boot,delimiter=',',header='helix,sheet,other',comments='')
summary={'delta_absorbance_example':.5003-.4997,'ellipticity_example_mdeg':32980*.0006,'normalization_example':-20*110/(10*.20*.10),'fraction_helix':float(fit[0]),'fraction_sheet':float(fit[1]),'fraction_other':float(fit[2]),'fraction_sum':float(fit.sum()),'thermal_midpoint_C':float(params[4]),'thermal_width_C':float(params[5]),'midpoint_fraction':.5,'fraction_noise_interval':np.quantile(boot,[.025,.975],axis=0).tolist(),'data_kind':'constructed teaching spectra and thermal signals; no measured protein reference library'}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

完整程序将原始重复扫描、扣背景结果、参考组合、比例灵敏度与热转变都导出为 CSV，并保存计算摘要。你可以改变一个条件，再追踪它影响了哪一层：原始信号、单位归一化、比例模型，还是温度拟合。这样做比直接替换最终百分数更容易发现错误。接入真实数据时，保留每次扫描与缓冲空白，并把实际光程、浓度、波段和温度记录填入分析；不要把教学基础曲线当成真实结构库继续使用。

## 让 CD 与研究问题对齐

远紫外与近紫外的配合可以把问题继续细化。肽链局部二级结构仍然存在时，芳香侧链周围的空间排列可能已经改变，近紫外响应因此发生变化。反过来，某些蛋白质的芳香残基少，或局部运动使其贡献相互抵消，近紫外信号本来就较弱。选择这项测量前先看序列与样品光学性质，才能判断弱信号反映的是测量条件还是对象本身。比较两段光谱时也要分别做好浓度和光程处理，因为近紫外常需要与远紫外不同的样品量和检测条件。

比较蛋白质突变体时，可以先在相同缓冲液和温度下观察归一化谱形，再比较升温转变与功能测量。如果两个样品的远紫外谱相近，而活性不同，研究方向可以转向局部位点、三级结构、结合能力或动力学；整体二级结构相似与功能完全相同不是同一个命题。若谱形明显不同，则进一步检查浓度、纯度、聚集状态和折叠条件，才能把差别稳妥地连接到序列变化带来的构象效应。

研究蛋白质与材料的相互作用时，还要关注实际进入光路的对象。悬浮颗粒可能产生散射，表面固定的蛋白质可能具有取向，而薄膜中的线性二色性和双折射可能进入偏振测量。溶液中随机取向分子的分析习惯不能直接照搬到定向薄膜。可以比较不同方位、适当的基底空白及独立的结构方法，并说明测量针对悬浮液、上清液还是表面层。对象定义清楚后，CD 才能与吸附量、显微观察或材料性能形成有意义的联系。

蛋白质制剂储存则更适合做连续比较：初始样品与不同储存条件下样品的谱形、可溶比例和功能是否一起改变？若原始毫度减小，先区分蛋白质浓度降低与单个分子结构改变；若归一化谱形改变，再结合粒径或色谱检查是否出现新的群体。这样的组合让 CD 发挥它快速观察整体构象的长处，同时把数量变化、聚集和功能放到各自对应的测量中。

最后保留一条能被别人重新走通的解释路径：样品在什么条件下稳定存在，光路中有多少蛋白质，哪些波长可靠，如何扣空白与归一化，参考模型解释了哪些特征，下一项测量准备区分什么。圆二色谱最有用的地方，是让“这条链似乎变了”成为可比较、可追踪的光学观察。它可以帮助选择缓冲条件、比较变体、寻找温度窗口，也能让材料与蛋白质之间原本看不见的相互作用留下可读的线索。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Greenfield: Using circular dichroism spectra to estimate protein secondary structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC2728378/)

   基础机制、样品条件、单位与结构拟合。

   Public author manuscript; technical reference, no figures copied.
2. [JASCO: Circular Dichroism Spectroscopy](https://jascoinc.com/learning-center/theory/spectroscopy/circular-dichroism-spectroscopy/)

   偏振、调制光路与不同谱段用途。
3. [JASCO: Circular Dichroism Tips & Tricks](https://jascoinc.com/learning-center/best-practices/circular-dichroism-tips-tricks/)

   光程、总吸收、探测器高压和积分时间。
4. [Harvard CMI: Circular Dichroism](https://cmi.hms.harvard.edu/circular-dichroism)

   缓冲匹配、浓度与聚集检查及分析工具。
5. [Mitchell: A Photo-electric Method for Measuring Circular Dichroism](https://www.nature.com/articles/166434b0)

   1950 年原文摘要回顾吸收差与椭圆率的两种测量路线。

   Primary historical abstract consulted; no original figures reproduced.
