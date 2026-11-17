# qPCR：从扩增曲线理解基因表达

Source: https://ml-biomat.com/tutorials/experimental-methods/l08/
Language: zh-CN

把每轮复制、荧光交点、效率、参照与低拷贝取样接成一条清楚的数量链。

## 细胞的回答，为什么藏在一条变亮的曲线里

把同一种细胞分别放在柔软与较硬的材料上，几天后它们的形状可能已经不同。研究者还想知道，负责黏附、炎症或组织形成的某些基因是否改变了表达。这里的“表达”先落到一个可以测量的对象：细胞中与目标基因对应的RNA。RNA可以理解为细胞从遗传信息中制作的工作副本，某类副本的数量与细胞当时的活动有关。把这些数量在条件之间比较，就能向细胞提出一个比“看起来有变化”更具体的问题。RT-qPCR先把RNA转成可供扩增的DNA，再通过扩增过程中的荧光变化估计起始目标量。

这个方法的直觉像观察两盘同时发起的面团：如果每一轮都按相同比例增长，起始较多的一盘会更早达到同一个高度。qPCR把“达到规定高度用了多久”换成“达到规定荧光用了多少个循环”。这个循环位置称为Cq，仪器也常使用Ct等名称；它可以是小数，因为软件能在相邻循环的测量点之间求交点。较早跨线通常对应较多的起始目标，但增长比例、荧光阈值和基线都参与了这个时间。先理解这些条件，后面的一串减法与指数运算就有了明确对象。

RT与real-time容易混淆。RT在RT-qPCR中指reverse transcription，即逆转录，是用RNA生成互补DNA的步骤；qPCR里的实时监测是边扩增边记录光。测DNA目标时可以直接做qPCR；研究RNA时加入逆转录，因此整条测量链又多了RNA提取、完整性和逆转录产率。两组样品得到相同的Cq，不一定代表每个细胞拥有相同数量的RNA：细胞数、每个细胞的总RNA、提取回收和加入反应的比例都影响最终进入小孔的目标量。

本节围绕“某种材料使目标RNA相对稳定参照改变多少”展开。先看复制怎样发生，再从原始曲线得到数量，最后处理参照、重复与低拷贝分配。实际代码会生成可追踪的构造数据，保留每个循环的荧光与每个独立样品的结果；真实论文图则展示实际反应中扩增曲线和熔解曲线如何相互补充。学完后，读者可以把一个倍数变化拆回原始测量，判断它来自目标增多、参照变化，还是扩增条件发生了改变。

## 从复制一段DNA，到连续看见复制过程

DNA的两条链能够按碱基配对关系互相充当模板。PCR利用这一点重复三个动作：加热使双链分开，降低温度让短DNA引物在相应位置结合，再让聚合酶沿模板延伸。两条引物分别限定目标区域的两端，连续循环后，这段区域在产物中越来越多。可以把引物想成两枚方向相对的书签，它们既指出从哪里开始，也使被复制的范围逐渐明确。温度程序与试剂共同决定引物能否准确定位、酶能否顺利延伸，具体数值需要随目标与试剂体系建立。

1985年Saiki及合作者报道了β-珠蛋白特定序列的酶促扩增，并将其与镰状细胞贫血相关的序列分析结合。那个阶段的重要变化是让极少的特定DNA先变得足够多，便于后续辨认。1992年Higuchi及合作者在封闭反应管中利用与双链DNA相关的荧光增强观察扩增，复制和观察由此接到同一条时间线上。这段历史解释了实时定量的核心：最终都有很多产物的两个孔，仍可能具有不同的起始量；连续观察保留了它们开始明显增长的先后顺序。

![原创复制机制示意，连接1985年特定序列扩增与1992年封闭管荧光观察；彩色短线表示引物，绿色表示延伸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/04cd4e998d185f7030e268bd.svg?v=04cd4e998d18)

图 1原创复制机制示意，连接1985年特定序列扩增与1992年封闭管荧光观察；彩色短线表示引物，绿色表示延伸。

理想情况下，每一份可复制模板在一轮之后变成两份，但实际反应通常没有每轮都达到完全倍增。我们把每轮新增比例记作效率η，100%效率对应η等于1，每轮乘数则是1加η，等于2。部分资料直接用E表示每轮乘数，因而会写出1.9这样的“效率”；另一些资料把同一状态写成90%。这不是反应不同，而是符号定义不同。阅读文献时先看作者定义，能够避免把1.9再加一次1，或把90当成指数底数。

$$
N_n=N_0(1+\eta)^n=N_0f^n
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/194f19b40ecc87035bc06fa5.svg) | 第n轮后的目标量，与N0同单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 指数增长模型的起始目标量，拷贝或相对信号单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 循环数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 每轮新增比例，无量纲；1对应100%效率 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 每轮乘数1+η，无量纲 |

假设所分析区间内每轮新增比例恒定。100个单位以f=2经历10轮得到102400；f=1.9对应η=0.9即90%。真实反应仅在适合的扩增区间近似满足此式。

指数增长只是扩增曲线中的一段。起初目标产生的荧光被基础读数与噪声遮住，随后进入近似按固定比例增加的阶段；继续反应，试剂状态、产物积累和检测响应发生变化，曲线逐渐进入平台。数量比较需要利用已经看得见、又保持合适增长关系的部分。本节构造曲线为便于检查，把指数段到达高读数后直接截平；这个平顶是绘图模型的约定，实际反应进入平台通常更加平缓。我们用平台展示为什么终点亮度会丢失起始差异，计算使用平台之前的交点。

## 一小孔里的目标，来自怎样的一份样品

想比较两种材料上的细胞，首先要定义采样对象。相同面积的材料、相同初始细胞数和相同培养时间对应不同的问题，也可能在收样时含有不同的细胞数。若最终按相同总RNA质量进行逆转录，比较的是每份输入RNA中目标的相对丰度；若要讨论每个细胞的数量，还需要细胞计数和适合的外部标定。材料表面可能吸附核酸或带入影响酶反应的成分，因此从材料上回收的样品应与相应的提取空白、操作对照一起设计，沿着真实样品的路径检查回收和干扰。

RNA容易在提取和保存过程中受到降解。完整性下降意味着一条原本连续的RNA变成若干片段，目标扩增区域是否仍完整又取决于片段位置。测得总RNA浓度，并不能单独回答目标区是否保持了可复制状态。使用与样品类型相适合的完整性检查，统一采样到稳定保存的时间，记录进入逆转录的RNA量，能够让组间差异更多地对应生物状态。把同一份RNA分成两个独立逆转录反应，还能观察这一步给结果带来多大的额外分散。

逆转录酶把RNA转成互补DNA，简称cDNA。引导它开始工作的短序列可以识别特定目标，也可以覆盖更广的RNA群体；不同策略对不同目标的回收可能不同。随后取一小部分cDNA进入PCR，进入孔中的量又受稀释和移液体积控制。因此，DNA标准曲线很好地检查后半段扩增，却没有经历RNA提取和逆转录。若研究目标是原样中的RNA绝对拷贝数，应把对应的RNA参考材料和回收步骤接入这条链，明确每一步体积及回收含义，而不是把反应孔中的数值直接当作每个细胞的数值。

两个常用空白分别检查不同环节。无模板对照把样品模板换成相应空白，帮助发现扩增体系污染或引物之间产生的产物；无逆转录对照使用同一样品但省略逆转录酶，帮助观察残留DNA是否也能被这对引物扩增。它们像设置在不同路口的观察点，哪一个出现信号，就把排查范围指向不同位置。阳性对照则确认体系确实能够检测目标。某个样品没有明显扩增时，结合这些对照、输入量与抑制检查，才能选择是增加采样、调整提取，还是进一步检查生物学上的低表达。

## 先读原始曲线，再把循环数换成起始量

仪器每一轮记录一个荧光值，最初得到的是原始扩增曲线。它包含与扩增有关的信号，也包含染料、探针、耗材及光学系统的基础响应。扣基线要回答的是“如果没有目标产物增加，这个孔仍会有多少读数”，而不是随意让曲线看起来平整。基线高估会使早期净信号过小，低估则使它保留一段额外底座；在对数坐标中，两者都可能扭曲原本应近似直线的增长段。本节代码使用明确已知的构造基线10000来隔离这一问题，实际分析需要根据真实曲线选择并记录基线方法。

阈值是一条所有待比较反应共同面对的水平线，应位于适合定量的扩增区域。每孔曲线与它相交的位置给出Cq。把阈值向上移动，所有曲线通常会晚些跨线，但晚多少取决于各自的增长速度。如果不同实验使用了不同阈值，仅仅把Cq数字抄在一起比较就缺少共同尺度。下面的式子把阈值、每轮乘数和交点连起来：已知经过若干轮增长后达到的量，就连续除去每轮的增长，回到起始量。

$$
C_q=\frac{\ln(N_q/N_0)}{\ln f},\qquad N_0=N_qf^{-C_q}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/612fc124ab16c82e17432359.svg) | 达到量化阈值的分数循环位置，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/99f414f1f400292a1cc8fff5.svg) | 阈值对应的净目标信号量，与N0同单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 指数模型回推的起始量，相对信号单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 每轮乘数，大于1，无量纲 |

由Nq=N0乘f的Cq次幂取对数得到；比值Nq/N0无量纲。Nq=1000000、N0=100、f=2时Cq约13.288；400单位约11.288，提前2轮。荧光尺度换为拷贝需合适标准校准；相同模板定义与反应条件用于比较。

荧光单位下算出的起始量具有同一检测体系内的相对意义。要换成拷贝数，需要已知量的合适标准把光与分子数量连接起来；不同扩增片段的长度、染料结合和探针响应可能不同，因此直接把两种基因的荧光尺度当成绝对分子比值需要额外校准。基因表达研究经常在每种测定内部先比较样品与共同参照，再组合这些相对变化，这样能让每种测定的固定响应系数在比值中消去。计算清楚地保留了什么、消去了什么，比“归一化之后就能比”更有解释力。

![实际代码输出的构造原始曲线、对数净信号、标准曲线与残差。每个浓度三个技术复孔；高信号直接截平仅是教学模型的约定。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2190e528fd489d57771eada0.svg?v=2190e528fd48)

图 2实际代码输出的构造原始曲线、对数净信号、标准曲线与残差。每个浓度三个技术复孔；高信号直接截平仅是教学模型的约定。

标准曲线提供另一个直观入口。准备一系列已知起始量，在同一测定中记录各自Cq，把横轴设为起始量的十进对数。每稀释十倍，曲线应晚若干轮跨线；在每轮完全倍增时，这个间隔约为3.322轮。因为十倍不是2的整数次幂，所以不会刚好晚三轮。拟合线的负斜率描述了这段延迟，进而可以求每轮乘数。检查每个浓度的重复孔与残差，能够发现低量分配、移液和高浓度抑制所留下的结构。

$$
C_q=a+s\log_{10}(N_0/N_*),\quad f=10^{-1/s},\quad \eta=f-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/612fc124ab16c82e17432359.svg) | 量化循环位置，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 校准截距，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 每十倍起始量的Cq变化，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 标准起始目标量，相对单位或拷贝 |
| ![Formula](https://ml-biomat.com/static/agent-math/a1357c231e808ab781f04f48.svg) | 与N0相同单位的固定参考量，本例1单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 每轮扩增乘数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 每轮新增比例，无量纲 |

指数式取十进对数，斜率为−1/log10(f)。f=2得到s约−3.322；f=1.9得到s约−3.587，反算仍得1.9。标准与未知样品须处于相应校准范围，横轴实际量应与稀释记录一致。

构造例用10、100、1000和10000个初始信号单位，每个水平三个技术复孔，真实每轮乘数设为1.9。程序从带噪声曲线的相邻交点做对数插值，拟合的斜率应接近理论值约负3.587。这里横轴是初始信号单位，未标成真实分子拷贝。若把实际稀释配错却仍使用计划浓度拟合，回归线可能看起来非常整齐，斜率却给出错误效率；因此高拟合优度不替代稀释准确性。已知标准、独立稀释核对与曲线形状分别回答不同的问题。

## 为什么要减两次，又为什么不能总用2作底数

假设对照样品的目标Cq为25、参照为20，处理样品目标为23、参照仍为20。目标提前两轮出现，而参照没有移动；在两种测定均每轮倍增且条件匹配时，目标相对参照增加4倍。第一次相减把每个样品的目标与自己的参照联系起来，第二次相减比较处理与对照的关系。负号则来自方向：起始量多会更早达到阈值，Cq更小，所以把循环差变成数量倍数时要反转这个方向。

$$
\Delta C_{q,i}=C_{q,t,i}-C_{q,r,i},\quad \Delta\Delta C_q=\Delta C_{q,T}-\Delta C_{q,C},\quad F=2^{-\Delta\Delta C_q}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/abc03db846fac332025557a4.svg) | 样品i内目标减参照的循环差，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样品编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e784fcda0647d6b9c48e034.svg) | 样品i的目标与参照Cq，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/bfecbeb29196c3f7ea9907ed.svg) | 处理与对照条件标签 |
| ![Formula](https://ml-biomat.com/static/agent-math/718ed6d7a0bf7ddb894c75d1.svg) | 处理与对照的归一化循环差，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 目标相对参照的条件变化倍数，无量纲 |

在目标和参照每轮都近似倍增、测定内部阈值一致且参照适当时，循环差能转成此倍数。对照25−20=5、处理23−20=3，差−2，得到4倍。普通实际分析使用经检查的效率校正量。

这个简式的2来自每轮倍增，不能只因为它常见就固定使用。若目标测定每轮乘1.8、参照每轮乘1.9，处理后目标提前两轮，参照提前一轮，正确的相对变化是1.8的平方除以1.9，约1.705。统一使用2则给2倍，差异来自计算假设。实际数据应采用经检查的测定效率，把每个反应转换为目标量，再进行参照归一化和条件比较。2025年更新的MIQE建议也强调把Cq作为中间量处理，让效率校正后的数量和相应范围成为结果的主体。

$$
F=\frac{f_t^{C_{q,t,C}-C_{q,t,T}}}{f_r^{C_{q,r,C}-C_{q,r,T}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 目标相对参照的变化倍数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/4fe32bcaed367c9f18c66248.svg) | 目标、参照测定各自的每轮乘数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a3eeab9ca584e4a0d4cab9ea.svg) | 对照、处理中目标的Cq，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e237c6d8d9032b8f025d1d4.svg) | 对照、处理中参照的Cq，无量纲 |

各测定在条件间保持自己的效率与阈值，分别把循环差转换成数量变化，再除去参照变化。目标提前2轮且ft=1.8，参照提前1轮且fr=1.9，F=3.24/1.9约1.705。样品间效率若改变，需按各反应适用的模型回推后再组合。

参照基因承担的是分母的工作，名称熟悉并不意味着在任何处理下都稳定。材料硬度、营养、分化和应激可能同时改变常用参照的表达。设目标真实增加4倍，选中的参照也增加2倍，计算最终就得到2倍；算术没有错，回答的是“目标相对于这个变化的参照增加多少”。选择来自不同调控路径的候选参照，在本实验的全部条件中检查稳定性，可以减少分母与目标共同变化的影响。多个参照通常在数量尺度上通过几何平均组合，它适合表达乘法变化，也让某个基因的固定单位缩放在组间比较时消去。

几何平均可以从一个小例子理解。两个参照在某样品的相对量为0.5和2，它们乘积为1，平方根也是1，表示一低一高的对称倍数变化在这个合成尺度上抵消。算术平均为1.25，则对“加多少”而非“乘多少”作了概括。抵消本身不等于参照稳定，两个共同受处理影响的基因也可能给出整齐结果；选择依据仍来自实验中的候选检查。对于组织或混合培养物，细胞类型比例变化也会改变RNA组成，解释结果时要把组织构成与单个细胞内部的表达变化联系起来。

## 交互实验：同样的起始差异，不同的增长速度

蓝色反应从100单位开始，每轮乘1.9；橙色起始量由真实倍数确定。调整橙色效率与公共阈值，看Cq差怎样变化。实线是理想指数信号；横轴循环，纵轴对数信号。

[Figure: 两条指数增长曲线和阈值](https://ml-biomat.com/tutorials/experimental-methods/l08/#L08-lab)

交互图把这些关系暂时缩减到两个目标反应，专门观察起始量、效率和阈值。蓝色反应的每轮乘数固定1.9，橙色反应可以改变；真实起始比例始终显示在旁边。用统一的2作底数计算时，改变橙色效率会让估计值明显偏移，而按各自已知效率回推能恢复设定比例。提高阈值还会放大增长速度不同造成的时间差。这样得到的规律适用于实验设计：同一Cq差只有放回相应阈值和效率中，才是一条完整的数量信息。

## 亮起来的是什么，没亮的孔又装了什么

双链DNA结合染料会随双链产物增加而变亮，目标产物与某些非特异产物都可能贡献信号。熔解曲线在扩增之后逐渐升温，观察双链分开时荧光怎样下降。把荧光对温度变化的负导数画出来，下降最快的位置成为峰，看起来像给产物做了一次热响应辨认。峰的位置与序列、长度、盐条件及加热程序有关。与经过身份核对的目标对照比较，能够发现新的低温峰或混合产物；一个峰的位置接近预期时，再结合引物设计和必要的序列检查建立身份。

两种不同序列可能拥有相近熔解温度，同一较长片段也可能分段熔解，所以不能把“一个峰”机械翻译成“只有目标”。探针法通过额外的序列识别步骤收集信号，有另一套特异性与背景检查。下面的真实LinRegPCR图把同一反应的原始扩增、扣基线曲线、效率估计与熔解结果放在一起：先确认用于数量回推的曲线部分，再检查发光产物是否符合目标特征。论文的多栏表格保留了这一判断链，读者可以将自己的导出数据与这些栏目逐一对应。

![Untergasser等2021年图1，CC BY4.0，完整转载。A与B是D8孔A75_CRE25样品的真实扩增和熔解分析；C–E为相应结果表和校正计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1c47ea17bb38815e00093ea0.svg?v=1c47ea17bb38)

图 3Untergasser等2021年图1，CC BY4.0，完整转载。A与B是D8孔A75_CRE25样品的真实扩增和熔解分析；C–E为相应结果表和校正计算。

当每孔只有很少分子时，重复孔之间的差异还有一个更朴素的原因：分子不是连续液体。即使平均每孔分到一个拷贝，也会有一些孔没有分子，有一些孔得到两个或更多。均匀独立随机分配的泊松模型给出，平均一个时约36.8%的孔为空，平均三个时仍约5.0%为空。这个例子把“平均浓度”与“每孔实际装入”分开。增加有效采样体积或重复孔数可以获取更多分配信息，而把没有跨线的孔随意填写成最后一个循环，会把缺失事件改造成一个人为确定的数量。

$$
P(K=0)=e^{-\lambda}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/065cbeda1c8b4a2279014fa8.svg) | 孔内没有目标拷贝的概率，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 孔内实际拷贝数，非负整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 每孔平均进入拷贝数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底数，约2.718，无量纲 |

均匀悬液中分子独立随机分配，采用泊松取样。λ=1时空孔概率约0.3679，λ=3时约0.04979；这描述进入孔的采样，与后续扩增失败分开。

检出限关心在规定条件下能够多稳定地发现目标，定量限还要求数量估计达到既定的精密度和准确度；能偶尔看到一条晚起的曲线，与能可靠比较1.2倍差异是不同的任务。低拷贝区间需要专门安排足够的重复与阳性对照，保留未检出的比例及判断规则。构造诊断图把空孔概率与效率偏差放在同一页，是为了让读者区分两个来源：前者发生在取样时，后者发生在扩增和解释时。增加循环数可以延长观察，不能把一个本来没有目标的孔变成有效目标采样。

![实际代码输出：A每个柱对应一个独立构造样品，三个技术孔先合并；B为构造熔解信号；C为空孔理论概率；D为固定真实4倍时的效率影响。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ad0ce21b0d46cd09ad108f11.svg?v=ad0ce21b0d46)

图 4实际代码输出：A每个柱对应一个独立构造样品，三个技术孔先合并；B为构造熔解信号；C为空孔理论概率；D为固定真实4倍时的效率影响。 A中每个样品的目标与参照比值，再除以三个对照样品比值的几何平均；对照组几何平均为1，算术平均约为1.003。

## 完整例子：让每个倍数都能回到那条曲线

下面的完整程序先生成标准系列，再生成六个独立构造样品，每个样品分别测目标和参照，各有三个技术复孔。输入量在样品之间变化，处理组的目标相对比例约为对照的4倍，同时保留适度的样品差异。程序把原始每循环读数写入数组文件，把标准、每孔Cq和回推量写入CSV，再展示效率校正与直接套用2的幂所产生的不同结果。构造数据提供已知答案，读者可以检查计算链是否真的把预先设定的差异找回来。

### 完整 Python：扩增、效率、归一化与熔解

离线生成逐循环构造荧光、逐孔数量、拟合与诊断图，真实论文图随包提供。

```
"""Offline qPCR teaching experiment; constructed arrays and a licensed measured figure."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def cq(n0,factor=1.9,threshold=1e6):return np.log(threshold/n0)/np.log(factor)
def crossing(cycles,signal,threshold):
    j=np.flatnonzero(signal>=threshold)[0]
    return float(cycles[j-1]+(np.log(threshold)-np.log(signal[j-1]))/(np.log(signal[j])-np.log(signal[j-1])))
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda a,b:a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(808);cycles=np.arange(41);threshold=1e6;baseline=10000;standard_n=np.array([10,100,1000,10000]);standard=[];curves=[]
    for n0 in standard_n:
        for rep in range(3):
            # The cap is a drawing convention, not a biochemical plateau fit.
            raw=baseline+np.minimum(n0*1.9**cycles,2e7)+rng.normal(0,500,len(cycles));curves.append(raw)
            standard.append([n0,rep+1,crossing(cycles,raw-baseline,threshold)])
    standard=np.array(standard);slope,intercept=np.polyfit(np.log10(standard[:,0]),standard[:,2],1)
    with(out/'standards.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['initial_target_units','technical_replicate','Cq']);w.writerows(standard)
    rows=[];sample_curves=[];truth=np.array([1,1.1,.9,4,4.4,3.6]);loads=np.array([.85,1,1.2,.9,1.1,1.25])
    for i in range(6):
        for gene,factor,n0 in [('target',1.9,100*loads[i]*truth[i]),('reference',1.95,1000*loads[i])]:
            for rep in range(3):
                raw=baseline+np.minimum(n0*factor**cycles,2e7)+rng.normal(0,500,len(cycles));sample_curves.append(raw);c=crossing(cycles,raw-baseline,threshold)
                rows.append([i+1,'control'if i<3 else'treated',gene,rep+1,factor,c,threshold/factor**c])
    with(out/'samples.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['sample','group','assay','technical_replicate','amplification_factor','Cq','inferred_initial_units']);w.writerows(rows)
    ratios=[];naive=[]
    for i in range(6):
        target=[r for r in rows if r[0]==i+1 and r[2]=='target'];ref=[r for r in rows if r[0]==i+1 and r[2]=='reference']
        # Geometric mean summarizes multiplicative quantities within technical replicates.
        ratios.append(np.exp(np.mean(np.log([r[-1]for r in target]))-np.mean(np.log([r[-1]for r in ref]))))
        naive.append(2**(-np.mean([r[-2]for r in target])+np.mean([r[-2]for r in ref])))
    ratios=np.array(ratios);naive=np.array(naive);normalized=ratios/np.exp(np.mean(np.log(ratios[:3])));naive/=np.exp(np.mean(np.log(naive[:3])))
    np.savez_compressed(out/'amplification.npz',cycles=cycles,standard_raw=np.array(curves),sample_raw=np.array(sample_curves),known_baseline=baseline,threshold=threshold)
    temperature=np.linspace(65,95,301);single=1/(1+np.exp((temperature-82)/.65));mixed=.75*single+.25/(1+np.exp((temperature-73)/.6))
    with(out/'melting.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['temperature_C','single_normalized','mixed_normalized','single_negative_derivative_per_C','mixed_negative_derivative_per_C']);w.writerows(zip(temperature,single,mixed,-np.gradient(single,temperature),-np.gradient(mixed,temperature)))
    fig,ax=plt.subplots(figsize=(11,5));ax.axis('off');ax.set(xlim=(0,12),ylim=(0,6))
    labels=[T('分开双链','Separate strands'),T('引物定位','Primers locate target'),T('酶延伸复制','Polymerase extends')]
    for j,label in enumerate(labels):
        x=1+j*3.6;ax.add_patch(FancyBboxPatch((x,.9),2.7,3.5,boxstyle='round,pad=.1',fc=[BLUE,PURPLE,GREEN][j],alpha=.12));ax.text(x+1.35,3.9,label,ha='center')
        for y in [2,2.7]:ax.plot([x+.3,x+2.4],[y,y],color=BLUE,lw=3)
        if j:ax.plot([x+.3,x+.8],[2.7,2.7],color=AMBER,lw=6);ax.plot([x+1.9,x+2.4],[2,2],color=AMBER,lw=6)
        if j==2:
            ax.plot([x+.8,x+2.4],[2.7,2.7],color=GREEN,lw=3);ax.plot([x+.3,x+1.9],[2,2],color=GREEN,lw=3)
        if j<2:ax.annotate('',xy=(x+3.4,2.6),xytext=(x+2.9,2.6),arrowprops={'arrowstyle':'->','lw':2})
    ax.text(6,5.3,T('1985：特定DNA扩增 → 1992：在封闭反应管中观察荧光','1985: specific DNA amplification →1992: fluorescence in closed reaction tubes'),ha='center',fontsize=12)
    ax.text(6,.2,T('原创机制图；每轮的复制比例决定达到同一亮度要多久。','Original mechanism: per-cycle multiplication controls time to a shared fluorescence threshold.'),ha='center');save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8.5))
    for j,n0 in enumerate(standard_n):
        color=[BLUE,AMBER,PURPLE,GREEN][j];raw=curves[3*j]
        ax[0,0].plot(cycles,raw,color=color,label=str(n0));ax[0,1].plot(cycles,np.maximum(raw-baseline,1),color=color)
    ax[0,0].set(xlabel=T('循环数','Cycle'),ylabel=T('原始荧光 / a.u.','Raw fluorescence / a.u.'),title=T('A  构造原始扩增曲线','A  Constructed raw amplification'));ax[0,0].legend(title=T('初始单位','Initial units'),fontsize=8)
    ax[0,1].set_yscale('log');ax[0,1].set_ylim(1e3,3e7);ax[0,1].axhline(threshold,color='gray',ls='--');ax[0,1].set(xlabel=T('循环数','Cycle'),ylabel=T('扣基线荧光 / a.u.','Baseline-corrected fluorescence / a.u.'),title=T('B  对数轴显出指数增长段','B  Log axes reveal exponential growth'))
    x=np.log10(standard[:,0]);ax[1,0].scatter(x,standard[:,2],color=BLUE);ax[1,0].plot([1,4],np.polyval([slope,intercept],[1,4]),color=AMBER);ax[1,0].set(xlabel=T('初始量的log10','log10(initial units)'),ylabel=T('Cq / 循环','Cq / cycle'),title=T('C  三个技术复孔的校准','C  Calibration with3technical replicates'))
    ax[1,1].scatter(x,standard[:,2]-np.polyval([slope,intercept],x),color=PURPLE);ax[1,1].axhline(0,color='gray',lw=1);ax[1,1].set(xlabel=T('初始量的log10','log10(initial units)'),ylabel=T('Cq残差 / 循环','Cq residual / cycle'),title=T('D  检查拟合剩下的结构','D  Examine residual structure'))
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'amplification')
    fig,ax=plt.subplots(2,2,figsize=(11,8.4));x=np.arange(6)
    ax[0,0].bar(x-.18,normalized,.36,color=BLUE,label=T('各自效率校正','Assay-specific correction'));ax[0,0].bar(x+.18,naive,.36,color=AMBER,label=T('统一假设每轮2倍','Assume2×per cycle'));ax[0,0].set_xticks(x,range(1,7));ax[0,0].set(xlabel=T('样品1–3对照，4–6处理','Samples1–3control;4–6treated'),ylabel=T('归一化倍数','Normalized fold'),title=T('A  保留独立样品的差异','A  Preserve individual-sample differences'));ax[0,0].legend(fontsize=8)
    ax[0,1].plot(temperature,-np.gradient(single,temperature),color=BLUE,label=T('一种构造产物','One constructed product'));ax[0,1].plot(temperature,-np.gradient(mixed,temperature),color=AMBER,label=T('两种构造产物','Two constructed products'));ax[0,1].set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('负导数 / °C⁻¹','Negative derivative / °C⁻¹'),title=T('B  熔解曲线提供产物线索','B  Melting informs product interpretation'));ax[0,1].legend(fontsize=8)
    lam=np.linspace(.01,8,200);ax[1,0].plot(lam,np.exp(-lam)*100,color=PURPLE);ax[1,0].scatter([1,3],[100/np.e,100*np.exp(-3)],color=AMBER);ax[1,0].set(xlabel=T('每孔平均进入拷贝数','Mean input copies per well'),ylabel=T('没有拷贝的孔 / %','Wells with zero copies / %'),title=T('C  少量分子如何分配到小体积','C  Low-copy sampling into small volumes'))
    eff=np.linspace(1.6,2,100);cqcontrol=cq(100);cqtreat=cq(400,eff);ax[1,1].plot(eff,2**(cqcontrol-cqtreat),color=AMBER);ax[1,1].axhline(4,color=BLUE,ls='--');ax[1,1].set(xlabel=T('处理样品每轮扩增倍数','Treated-sample multiplication per cycle'),ylabel=T('直接用2的幂得到的倍数','Fold inferred with powers of2'),title=T('D  真实4倍遇到不同扩增效率','D  True4×change with changing efficiency'));ax[1,1].set_ylim(0,10)
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(11,10.7));ax.imshow(Image.open(Path(__file__).resolve().parent/'linreg2021-figure1.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实反应D8：把扩增与熔解结果一起读','Measured reactionD8: read amplification and melting together'),fontsize=12);fig.text(.5,.015,T('Untergasser等2021，图1；CC BY4.0。完整转载，外加双语标题。','Untergasser et al.2021,Fig1; CC BY4.0. Full reproduction with an added external title.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,1]);save(fig,'published')
    ideal_slope=-1/np.log10(1.9);summary={'growth':{'hundred_after_ten_doublings':100*2**10,'tenfold_delay_at_two':np.log(10)/np.log(2),'fourfold_delay_at_19':float(cq(100)-cq(400))},'calibration':{'ideal_slope':float(ideal_slope),'factor_from_ideal_slope':float(10**(-1/ideal_slope)),'fitted_slope':float(slope),'fitted_factor':float(10**(-1/slope))},'normalization':{'ideal_ddcq_fold':2**(-(23-20-(25-20))),'efficiency_example':1.8**2/1.9,'reference_doubled_fold':4/2,'observed_control_mean':float(normalized[:3].mean()),'observed_treated_mean':float(normalized[3:].mean())},'sampling':{'empty_at_one':float(np.exp(-1)),'empty_at_three':float(np.exp(-3))}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

技术复孔在数量尺度上按几何平均合并，再计算每个样品的目标与参照关系；独立样品仍各自保留一个值。随后，六个样品的目标与参照比值，都除以三个对照样品比值的几何平均，得到图中共同标尺下的倍数。因此对照组的几何平均为1，算术平均可以略高于1；本例约为1.003，这来自乘法标尺上的校准，并非额外的生物变化。图中的六根柱子对应六个样品，而不是十八个独立生物重复。对真实数据进行组间分析时，可以根据研究设计在效率校正、归一化后的数量或其对数上建立统计模型，保留配对、批次和独立取样结构。两组平均值相差多少与样品之间有多分散，是需要一起呈现的信息，不能用大量技术复孔把生物差异的分散隐藏起来。

可以先把处理样品的参照也提高2倍，再看归一化结果如何从约4倍变成约2倍；随后保持生物量不变，改变目标扩增效率，比较原始曲线与直接Cq算法。还可以移动阈值，观察所有交点变化时，采用一致模型回推的起始量是否保持稳定。每次只改一个环节，把输入、原始曲线、反算数量和最终分母依次对照，便能把一套容易背成口诀的方法转成可以推理的实验。

最后回到材料与细胞的研究问题。目标RNA的变化描述转录本丰度，蛋白丰度还受到翻译和降解影响，细胞行为又由位置、活性及环境共同决定。可以用同一研究中的蛋白检测、显微观察和功能实验接着追问，而不是让RNA倍数替所有层次作答。一个清楚的结果应说出比较的细胞或组织、采样时点、目标与参照、数量换算及样品差异。如此，荧光曲线所携带的信息就能与真实的生物过程相接，成为下一步研究的可靠起点。

板上样品的位置也属于实验设计。若所有对照都放在一张板、所有处理都放在另一张板，条件差异会与运行差异重合。把组别均衡安排，并在不同运行中加入同一份分装校准样品，可以把运行尺度接起来。共同校准样品的量需要足够、保存条件一致，且在目标和参照测定中都处于合适范围。它与无模板对照承担不同职责：前者连接数量尺度，后者检查体系背景或污染。两者同时存在时，一张板才既有组间比较的坐标，也有检测异常的观察点。

平均值的算法同样要与数量定义相配。两个相同测定的Cq先求算术平均，再换成数量，得到的是对应数量的几何平均。例如两个孔回推量为100和400，几何平均为200，而算术平均为250。两种汇总各有明确含义，选择后应贯穿分析。对于独立样品，还要保留原始分散以及实验中的配对关系；同一个体处理前后与两组不同个体，并非同一种统计设计。计算表中的每一行最好能够回到样品、反应和原始曲线，使数量汇总与实际取样保持一致。

绝对量换算还需要逐步核对体积。例如十倍稀释的cDNA取2微升进孔，相当于原液0.2微升；若该孔标定为100拷贝，便对应原液每微升500拷贝。继续推回RNA需要逆转录体积、产率和模板定义。单链cDNA与双链DNA标准经历的起始复制步骤也有区别，绝对校准应明确接上这一关系。若某个复孔偏离其余孔，保留曲线并检查孔位、移液和熔解产物，再按事先确定的测量标准处理；这样每次取舍都有可追踪的实验原因。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Saiki et al. (1985): Enzymatic amplification of beta-globin genomic sequences](https://pubmed.ncbi.nlm.nih.gov/2999980/)

   扩增技术早期工作与研究目的。

   Abstract and bibliographic reference
2. [Higuchi et al. (1992): Simultaneous amplification and detection of specific DNA sequences](https://pubmed.ncbi.nlm.nih.gov/1368485/)

   封闭管内以荧光连续观察扩增。

   Abstract and bibliographic reference
3. [Bustin et al. (2010): MIQE precis](https://pmc.ncbi.nlm.nih.gov/articles/PMC2955025/)

   样品、逆转录、空白和参照的实验设计。
4. [Bustin et al. (2025): MIQE 2.0](https://doi.org/10.1093/clinchem/hvaf043)

   效率校正量、定量范围、原始数据和预测区间。
5. [Untergasser et al. (2021): Web-based LinRegPCR](https://link.springer.com/article/10.1186/s12859-021-04306-1)

   实际扩增与熔解分析、基线和结果表；图1。

   CC BY 4.0; Fig. 1 reproduced in full
