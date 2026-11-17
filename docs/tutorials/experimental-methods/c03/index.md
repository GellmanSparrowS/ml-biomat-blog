# 质谱：用质量与电荷辨认分子

Source: https://ml-biomat.com/tutorials/experimental-methods/c03/
Language: zh-CN

让离子带路，把质量、电荷、碎片和浓度连接成可以逐步检验的分子证据。

## 一杯咖啡里，怎样把“像咖啡因”变成可检验的判断

一杯咖啡里有许多能够吸收紫外光的分子。液相色谱把它们逐渐分开，某个峰的保留时间又与咖啡因标准接近，这已经是有用的线索。接下来还能问得更具体：这个峰产生的离子质量是否符合咖啡因的组成，受控碰撞后是否产生相似的碎片，加入咖啡因标准后相应信号怎样变化？质谱把这些问题接到同一条证据链上。它既能研究饮料中的小分子，也能帮助确认一条合成肽、追踪材料释放的降解产物，或检查聚合物相邻成员之间是否具有预期的重复单元差异。

质谱仪并不是把一个分子放到微型天平上。它先让待测物形成带电粒子，也就是离子，再利用电场或磁场对离子的运动进行控制，最后记录与质荷比有关的信号。质量较大和电荷较多，对运动的影响方向不同；一个大分子带上多个电荷后，可能出现在很低的质荷比位置。因此，图上有十个峰，不一定代表十种分子；一个峰的位置，也不一定等于原来中性分子的质量。先把这两点讲清楚，很多看似复杂的谱图就有了可以拆解的顺序。

本章把任务分成两个相连的问题。第一个是辨认：观测到的离子与哪个候选分子相符，需要哪些结构信息来继续区分候选？第二个是定量：相应信号与样品中多少物质有关，提取和电离过程是否改变了响应？前一个问题需要质量、同位素、碎片和色谱保留等线索共同工作；后一个问题需要标准、内标、空白和基质效应实验。这样安排也能解释一个常见现象：质谱图很清楚，浓度却仍可能算得不准，因为信号产生的效率还没有被测量。

我们将使用一份公开的咖啡因参考串联质谱，保留记录中的真实峰位置和强度；另外构造可控制的电荷系列、液相质谱数据图和定量实验。真实参考谱负责让我们练习读懂实际记录，构造模型负责把电荷、分辨本领、质量误差和响应抑制逐个拆开。每一种图都说明自己展示的对象，最后再把它们连接成一次从进样到研究判断的完整分析。

## 先让分子完整地进入气相，再谈怎样测量

电场容易推动离子，却无法用同样的方式筛选一个完全中性的分子。因此，离子源是质谱与样品之间的入口。电子电离常用于能够进入气相的小分子，提供有特征的碎片；电喷雾电离，简称 ESI，则从溶液形成带电液滴。随着溶剂蒸发、液滴演化和离子释放，一部分待测分子进入气相，随后通过接口进入较低压力区域。不同离子释放机制适合描述不同大小和性质的物种，这里抓住共同结果：溶液中的分子获得一个可由分析器操纵的带电形式。

这个入口曾经是生物大分子质谱的关键困难。把一个大而脆弱的蛋白质加热到足以进入气相，往往先改变或破坏了它。芬恩及合作者在 1989 年的论文中讨论了电喷雾得到完整大分子离子以及连续多电荷峰系列的特点。多电荷最初增加了读谱的复杂程度，却也让很大的分子落入仪器能够测量的质荷比范围。图中以逐渐变化的带电液滴和一个分子的电荷系列，把这个历史进展需要解决的物理问题画出来：怎样将溶液中的大分子送进可测量的离子世界。

激光解吸提供另一种入口。样品与帮助吸收和传递能量的基质结合，激光脉冲使物质离开表面并形成离子。田中耕一团队在 1987 年报告了大质量分子的软激光解吸结果；此后基质辅助激光解吸电离，即 MALDI，成为蛋白质、肽和某些聚合物的重要测量方法。图中是对基质、激光和离子释放关系的原创示意，不把现代 MALDI 的所有实现都归成一个人的工作。两条发展路线的共同目标，是让足够完整的目标离子到达分析器，再决定何时主动使它碎裂以获取结构信息。

飞行时间分析器给出一个容易建立直觉的例子。离子通过相同加速电压时，电荷越多，获得的电能越多；在相同电荷下，质量越大，要达到同样速度就需要更多能量，因此加速后的速度较小。经过同样长度的飞行路径，重离子平均花费更长时间。把电场提供的能量与运动能量联系起来，便得到下式。它是忽略初始速度差异、采用理想加速与无场漂移的模型，实际仪器还会校正起始时间、能量分散和飞行路径。

$$
zeU=\tfrac12mv^2,\qquad t=\frac{L}{v}=L\sqrt{\frac{m}{2zeU}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 正离子电荷数，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 元电荷，1.602176634×10⁻¹⁹ C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | 加速电压的大小，V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 离子质量，kg；400 Da≈6.64216×10⁻²⁵ kg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 理想加速后的速度，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 无场飞行距离，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 飞行时间，s，图中换算为 μs。 |

忽略初始动能时，电势能转为动能；飞行时间是路程除以速度。L=1 m、U=5000 V、z=1、m=400 Da，t≈20.36 μs；质量增至四倍时飞行时间加倍。

![原创电喷雾、激光基质与理想飞行时间示意，联系芬恩团队 1989 年论文与田中团队 1987 年软激光解吸报告。结构不按比例；右图为 1 m、5 kV、单电荷的教学计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8c5d075f4a8c78e652bb01d1.svg?v=8c5d075f4a8c)

图 1原创电喷雾、激光基质与理想飞行时间示意，联系芬恩团队 1989 年论文与田中团队 1987 年软激光解吸报告。结构不按比例；右图为 1 m、5 kV、单电荷的教学计算。

四极杆则通过随时间变化的电场，使特定质荷比范围的离子具有合适的通过轨迹；离子阱和其他分析器采用不同方式约束或测量离子运动。选择仪器时，研究目标比名称本身更重要：要精确定量几个已知分子，还是筛查未知物，要分开很接近的质量，还是快速记录窄色谱峰，都对应不同的测量设置。检测器将到达或运动中的离子转成电信号，数据处理再把信号映射到质荷比轴上，仪器性能需要在这一整条链中理解。

## 一个分子为什么能出现许多峰

先用一个质量为 12,000 Da 的构造分子来计算。Da 是道尔顿，适合表示单个分子或离子的质量。若它结合六个质子，就有六个正电荷，其质荷比数值约为 2001.0073；结合十二个质子时，数值约为 1001.0073。两个峰都来自相同的中性分子，只是电荷不同。可以把电荷想成推动物体的“把手”：同样质量上有更多可受电场作用的把手，运动响应就会改变。这个类比说明为什么必须同时知道质量与电荷，并不表示电荷真的均匀分布成可见的机械把手。

$$
\mu=\frac{M_r+zh}{z},\qquad M_r=z(\mu-h)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 谱图上 m/z 的数值，采用 Da/e 刻度的数值约定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/74c324121c11267490a2341c.svg) | 中性分子相对质量，即其质量除以 1 Da，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 结合质子产生的正电荷数，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 质子质量除以 1 Da 的数值，约 1.007276466579，无量纲。 |

对 [M+zH]z+，先把 z 个质子的质量加入，再除以电荷数。Mᵣ=12,000、z=12，μ≈1001.007276；反算仍为 12,000。其他加合物必须按其实际组成改写质量项。

结合质子形成的离子常写成 [M+H]⁺，失去质子的负离子写成 [M−H]⁻；也可能出现钠离子加合物、其他加合物或多个分子形成的离子。方括号描述的是最终被检测的离子组成。计算高精度质量时，质子与中性氢原子的质量不能混用，因为中性氢还含有电子。对一个只带一个正电荷的质子化分子，应把中性分子的单同位素质量加上约 1.007276 Da。若直接拿书上的平均相对分子质量加 1，再与高分辨谱的多个小数位比较，就混合了两种不同的质量定义。

“单同位素”需要从原子讲起。同一种元素的原子可以拥有相同的质子数，却有不同的中子数，这些形式叫同位素。普通碳以碳十二为主，也含有少量碳十三。一个含有许多碳原子的分子群体里，有些分子完全由碳十二构成，有些恰好含一个碳十三，还有些含两个。因此即使化学组成相同，也会形成一组相近的质量峰。若其他元素的同位素也参与，真实包络会更丰富；图中的简化模型只改变五十个碳位点的碳十三数量，用来单独展示同位素间距如何随电荷变化。

碳十三替换碳十二增加的质量约为 1.003355 Da，单电荷离子的相邻峰间隔因此约为 1.003355 个质荷比单位；双电荷时约为 0.501677，三电荷时约为 0.334452。看到一串间隔接近一半的同位素峰，是判断双电荷的一条线索，前提是仪器确实把这些峰分开，且邻近信号没有造成混淆。确定电荷之后，便能把多个峰反算到同一个中性质量上，检查不同电荷态是否相互支持。这种从多个观察共同约束一个量的做法，比只读最高峰更可靠也更有意思。

![全部为构造模型。A 同一个 12,000 Da 分子的 6+ 至 12+ 电荷系列；B 只考虑 50 个碳位点的碳十三二项分布，各电荷组上下错开；C 两个相差 0.01435 的离子在不同半高宽分辨本领下的轮廓，上下错开显示。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d6b362ee30f9465de4c2ac87.svg?v=d6b362ee30f9)

图 2全部为构造模型。A 同一个 12,000 Da 分子的 6+ 至 12+ 电荷系列；B 只考虑 50 个碳位点的碳十三二项分布，各电荷组上下错开；C 两个相差 0.01435 的离子在不同半高宽分辨本领下的轮廓，上下错开显示。

对聚合物，峰系列还可能来自不同的重复单元数。例如，一个系列每增加一个相同结构单元，中性质量就增加一个固定值；如果电荷为二，谱上的间隔会缩小到该质量差的一半。末端基团和所结合的离子决定系列的整体位置。因此，研究材料时应同时考虑重复单元、端基、加合物和电荷，而不是看到等间距的峰就立即认定它们全部属于同一种结构。生物分子的多电荷系列与聚合物的同系物系列，在图上都可能形成规律，但背后的变量不同。

## 峰的位置、峰的宽度和碎片，分别告诉我们什么

一张质谱的横轴是质荷比，纵轴是信号强度。信号可以来自连续轮廓数据，也可以经过处理变成每个峰的位置和强度列表，后者常画成一根根竖线。最大强度峰称为基峰，把它设为百分之百，其他峰按比例缩放，便得到容易比较的相对强度。这个百分之百是图内的归一化参照，既不是样品纯度，也不是该分子在所有物质中占据百分之百。不同分子的电离效率、传输效率和碎裂方式都可能不同，峰高不能直接拿来当作混合物的质量配比。

质量准确度与分辨本领是两件相连但不同的事。准确度关心峰中心离预期位置有多远，通常用相对于理论值的百万分比误差表示；分辨本领关心在某个质荷比位置，峰有多窄，因而能否区分附近的离子。图中相隔很近的两个构造峰，在较低分辨本领下合成一个宽包，在较高分辨本领下逐渐分开。一个很窄的峰仍可能因校准偏移而处在错误位置；一个中心恰好接近理论值的宽包，也可能混有多个离子。评估数据时，要同时看校准、峰形、离子量和邻近干扰。

$$
R=\frac{\mu}{\Delta\mu_{\mathrm{FWHM}}},\qquad \epsilon_{\mathrm{ppm}}=10^6\frac{\mu_{\mathrm{measured}}-\mu_{\mathrm{theory}}}{\mu_{\mathrm{theory}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 按半高宽定义的分辨本领，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 所讨论峰的质荷比数值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8ff1b2b09c124f9145acbad7.svg) | 峰在半高处的全宽，与 μ 使用同一刻度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9da3797043bf140e00a4f1c3.svg) | 相对质量偏差的百万分比数值，ppm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e6c6cab688b1542e9c4cd71c.svg) | 实测与按所选离子组成计算的理论质荷比数值。 |

位置相对峰宽给出分辨本领；中心偏移相对理论位置给出误差。μ≈195.087652、R=40,000，半高宽≈0.00487719；比理论值高 0.001 时，误差约 +5.126 ppm。两种指标描述不同性能。

现在读真实咖啡因记录。分子式为 C₈H₁₀N₄O₂，由指定同位素原子质量相加，得到中性单同位素质量约 194.080376 Da；质子化离子对应的理论质荷比约 195.087652。公开记录的前体元数据写为 195.0877，谱内另有一个保留下来的 195.0873 峰，两者分别保留。图中最强峰位于 138.0657，这是受控碰撞后的产物离子信号。记录提供了正离子电喷雾、四极杆飞行时间分析和 40 V 碰撞设置，因此它是一份明确条件下的串联质谱，而不是未经过碰撞的完整分子谱。

![真实咖啡因参考谱 MSBNK-BAFG-CSL2311094663，正离子 LC-ESI-QTOF、CID、40 V。数据：Björn Ehlig、Ole Lessmann、Kevin S. Jewell、Arne Wick，德国联邦水文研究所，CC BY。保留 23 个峰，以原强度归一化为 100%；右图区分理论值、前体元数据与谱内峰。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ce64459a2879a9cdc25218ae.svg?v=ce64459a2879)

图 3真实咖啡因参考谱 MSBNK-BAFG-CSL2311094663，正离子 LC-ESI-QTOF、CID、40 V。数据：Björn Ehlig、Ole Lessmann、Kevin S. Jewell、Arne Wick，德国联邦水文研究所，CC BY。保留 23 个峰，以原强度归一化为 100%；右图区分理论值、前体元数据与谱内峰。

串联质谱可概括为先选择、再改变、再分析。先选定前体离子范围，让这部分离子在碰撞等作用下发生碎裂，再测量产物离子。不同分子即使具有相同的总组成，也可能在不同连接方式下产生不同碎片组合，所以碎片谱能够增加结构辨认能力。比较参考谱时，应核对前体、正负离子模式、碰撞条件和仪器记录方式；同一分子在不同碰撞条件下，强度分配可以明显变化。选中的前体窗口若还包含邻近离子，产物谱也可能混合多个来源，这时色谱分离和更合适的选择窗口就很重要。

精确质量可以排除很多不合适的组成，却不会自动给出原子怎样连接，也不会仅凭一个峰决定立体结构。实际辨认通常逐步收敛：先确定合理离子形式和电荷，再检查质量与同位素，随后比较产物谱和保留行为，必要时用真实标准或其他结构方法确认。把结果写成“在这些条件下与某参考标准相符”，就把证据放在了具体可复查的对象上；每增加一种独立线索，候选解释便进一步收窄。

## 液相质谱是一张随时间展开的地图

液相色谱与质谱联用后，数据不再只是一条曲线。每个时间点都有一张质谱，把所有时间点叠起来，就得到“时间—质荷比—强度”的数据地图。地图中的一个斑点表示某个离子在一段时间内出现。把全部测量范围的信号相加得到总离子流色谱；只选定某个质荷比窗口相加，则得到提取离子流色谱，常缩写为 XIC 或 EIC。图中的总和只覆盖所展示的窄质量范围，专门用来观察目标与近邻干扰；真实仪器的总离子流通常覆盖它实际采集的完整范围。

提取窗口像在地图上划定一条窄走廊。走廊过宽，邻近离子也可能被纳入，造成峰变宽、出现肩部或面积偏大；走廊过窄，质量偏移和峰本身的宽度又可能让目标信号被漏掉。以百万分比指定窗口时，窗口的绝对宽度随目标质荷比变化。因此要结合质量稳定性、分辨本领和采样方式选择，而不是把一个数字机械套用到所有分析。图中把同一数据分别用 ±5 ppm 与 ±100 ppm 提取，读者可以直接看到后者怎样把较晚流出的近邻带入目标轨迹。

![固定种子的构造 LC-MS 数据：目标 4.0 min、近邻 4.4 min，质量相差 0.01435，R=40,000。热图采用 log₁₀(1+信号)；右图每条曲线分别按自身最大值归一化，只比较形状，不能据此比较绝对面积。总和只包含图示质量窗口。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9e93f2371dbc2d133e361ae7.svg?v=9e93f2371dbc)

图 4固定种子的构造 LC-MS 数据：目标 4.0 min、近邻 4.4 min，质量相差 0.01435，R=40,000。热图采用 log₁₀(1+信号)；右图每条曲线分别按自身最大值归一化，只比较形状，不能据此比较绝对面积。总和只包含图示质量窗口。

时间方向也有分辨率。色谱峰只有几秒宽时，质谱必须在这几秒内取得足够多的扫描点，才能稳定描出峰形和面积。每次扫描花费越长，或要轮流监测的目标越多，分配给单个目标的时间就越有限。设置应让所需质量信息与色谱采样速度协调。对于已知目标，可选择针对性的前体到产物离子组合监测，减少无关信号；对于未知物筛查，则更重视较广的质量覆盖和可追溯的碎片信息。两者围绕不同任务优化，不宜只用一个“灵敏度更高”概括所有选择。

样品进入电喷雾前，溶剂和盐也是测量的一部分。蛋白样品里常见的非挥发性缓冲盐、去污剂或大量其他溶质，可能影响带电液滴的形成、蒸发和目标离子产生。选择兼容的挥发性流动相、进行适当净化或稀释，可以改善分析，但每一步也可能损失待测物。应根据目标的溶解性、稳定性和吸附行为设计提取，不把适合咖啡因的方法直接当成肽、多糖或所有聚合物的通用方案。对于会随时间变化的样品，还应安排保存温度和分析顺序，使制备之后的等待过程具有可比性。

在一个材料释放实验中，可以把初始材料、释放液、容器空白和溶剂空白放在同一分析思路中比较。如果某峰也出现在容器空白里，它就可能来自容器或处理过程；如果只在材料处理后增加，再结合质量和碎片寻找合理的化学变化。将空白与样品画在相同坐标上，比在完成计算后仅附上一句“做了空白”更容易识别真正值得追踪的信号。

## 同样多的分子，为什么信号会变小

把同样浓度的咖啡因分别加入纯溶剂和处理后的复杂样品提取液，后者的信号可能更弱。两份溶液里咖啡因的量相同，差别出在其他共存物影响了响应，这就是基质效应的一种表现。为了把它与提取损失区分开，可以在提取完成后再加入已知目标物，并与纯溶剂中相同浓度的响应比较。若基质中响应为纯溶剂的 55%，基质因子就是 0.55。另将已知量在提取前加入，再与提取后加入的结果比较，才能进一步估计提取步骤造成的回收变化。

$$
\mathrm{MF}=\frac{A_{\mathrm{post}}}{A_{\mathrm{neat}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c7daa1ef3fa0bc9c86be752f.svg) | 基质因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e9a43225a844d0d4bf10d657.svg) | 提取完成后向基质加入目标物所测的净峰面积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/13e8115a017499920ae8842a.svg) | 相同目标浓度在纯溶剂中测得的净峰面积，单位与分子相同。 |

等浓度与一致进样条件下，比较基质对检测响应的影响，并扣除合适空白。纯溶剂面积 10,000、基质面积 5,500，MF=0.55；这个提取后比较与提取回收率回答不同问题。

内标提供了随样品同行的参照。向每份样品和校准液加入已知量的另一种可区分信号的物质，计算目标峰面积与内标峰面积的比值。如果目标和内标在进样与电离中受到相同的比例影响，这个共同因子会在相除时消掉。稳定同位素标记的同类分子常适合承担这个角色，因为其化学行为接近而质量可以区分；加入时机又决定了它能够跟踪哪些步骤。提取之后才加入的内标，可以跟踪后续测量变化，提取之前发生的损失则需要其他对照来评价。

比值也需要验证。假设目标响应被压到 55%，内标却只降到 80%，两者相除后仍保留了不同步的偏差。图中把这个关系直接画出，说明挑选内标不只是找一个“附近有峰”的分子。需要检查它与目标的保留行为、提取回收和基质响应是否足够一致，并观察不同真实样品之间是否仍成立。共洗脱有助于经历相近环境，但同位素串扰、天然同位素峰重叠和内标纯度也值得在具体方法中检查。

$$
r=\frac{A}{A_{\mathrm{IS}}}=sc+b,\qquad c=\frac{r-b}{s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 目标与内标的峰面积比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 目标峰面积，与内标采用一致面积单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a182fb4a475d2faaa4f36411.svg) | 内标峰面积；所有相关样品按定义加入相同已知量内标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 比值校准斜率，mL/ng。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 进样溶液中的目标浓度，ng/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 比值校准截距，无量纲。 |

目标与内标同受比例因子影响时，相除消去共同变化。s=0.08 mL/ng、b=0.01、r=0.65，c=8 ng/mL。交互采用扣除背景后的 b=0；目标与内标响应因子不同时，比值保留其比值造成的偏差。

![构造基质与校准实验。A 为提取后等浓度加标响应比；B、D 使用真实浓度 8 ng/mL，比较共同抑制与不同步抑制。C 每个浓度三个重复，面积比真值为 0.08c+0.01，程序由带噪声数据拟合。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/aa868068bf8189f5073c7a8b.svg?v=aa868068bf81)

图 5构造基质与校准实验。A 为提取后等浓度加标响应比；B、D 使用真实浓度 8 ng/mL，比较共同抑制与不同步抑制。C 每个浓度三个重复，面积比真值为 0.08c+0.01，程序由带噪声数据拟合。

下面的交互让浓度、目标响应因子和内标响应因子分别变化。纯溶剂外标把降低的信号读成较低浓度；当目标与内标同受影响时，面积比能够恢复原来的浓度；当两者不同步时，偏差又出现。柱高表示检测响应，旁边显示反算浓度，两者用不同单位标明。这个实验把“检测到了多少信号”和“样品中实际有多少物质”放在同一张图里，读者可以自己预测哪些变化会被比值抵消，哪些会留下来。

## 同一浓度，响应为什么变了

信号已扣除背景。内标浓度固定；比较纯溶剂外标与目标/内标面积比。先令两个响应因子相同，再单独改变一个，观察何种偏差会保留下来。

[Figure: 目标和内标响应及浓度计算交互图](https://ml-biomat.com/tutorials/experimental-methods/c03/#C03-plot)

建立定量方法时，校准点应覆盖目标范围，保留重复测量和残差，另用独立配制的质控样检查反算结果。低浓度区域的波动、空白贡献和高浓度饱和，对拟合的影响并不相同，是否加权应由数据的变异特点决定。质量轴校准让峰出现在正确位置，浓度校准则把面积或面积比换成物质量，两种校准不能互相替代。若样品曾稀释或提取，最终报告还要把相应体积与稀释关系接回原始样品的单位。

## 从完整例子走向一份可追问的研究结果

程序先读取随例子保存的公开参考记录，提取二十三个原始峰，并把原强度除以最大原强度后画成百分比。这样可以保留真实峰表，又明确图中的归一化规则。构造的液相质谱数据则从两个不同质量、不同保留位置的组分出发，叠加固定随机种子的背景，形成完整二维数组，再分别提取窄窗口和宽窗口的时间轨迹。所有数组与关键结果都会保存，便于改变窗口、检查峰顶位置，或将整个处理过程替换成自己的数据。

定量例子还包含六个浓度水平的重复面积比、拟合曲线和一个已知构造浓度的未知样。它允许我们检查程序是否能从带有小幅波动的校准中找回设定值，同时把基质响应问题与校准随机波动分开。读代码时，先看每个数组的轴和单位，再看归一化与积分或求和发生在哪里。把一张质谱按基峰归一化适合比较碎片形状，而用这种归一化后的峰高跨样品计算绝对浓度，就会丢掉原始响应大小的信息；处理选择必须跟着问题走。

重复测量也应说明重复了什么。同一瓶溶液连续进样三次，主要观察制备完成之后的进样与仪器波动；同一材料独立提取三份，把更多制备过程纳入比较；独立制备的不同材料，则涉及样品之间的差异。这些层次都可以有价值，但误差棒回答的问题不同。重复进样很接近，并不会自动给出批次之间的变化范围。把样品之间的关系保存在数据表里，作图时才能选择与研究比较相符的重复层级。

测量顺序还能揭示另一类问题。若所有未处理样品都在前面，所有处理样品都在最后，离子源响应随时间漂移就可能与处理效应同向。适当交错组别、定期插入质控样，并在高浓度样品后安排空白，有助于区分漂移、残留和样品化学变化。高浓度样之后的空白仍有目标信号，提示进样或色谱系统可能保留了上一份物质；随后比较清洗和稀释条件，就把观察转成了改进方法的具体实验。

### 完整质谱、LC-MS 地图和内标定量例子

读取随例子保存的 CC BY 咖啡因参考记录，生成明示的教学模型、实际图、原始形式数组和计算结果。

```
"""Mass spectrometry: charge, real MS/MS, LC-MS extraction and quantitation.
Run: python main.py --output results --language en
Requires numpy and matplotlib. Reads the bundled CC BY MassBank record offline.
Other signals are explicitly constructed teaching data, seed 630.
"""
from pathlib import Path
import argparse,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon,FancyArrowPatch
P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True);P.add_argument('--language',choices=['zh','en'],default='en');a=P.parse_args();O=a.output;O.mkdir(parents=True,exist_ok=True);L=a.language
def t(z,e):return z if L=='zh' else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#25364a','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';D='#25364a'
def save(f,n):f.savefig(O/f'{n}-{L}.svg',bbox_inches='tight');f.savefig(O/f'{n}-{L}.png',bbox_inches='tight',dpi=145);plt.close(f)
def g(x,m,s):return np.exp(-.5*((x-m)/s)**2)
def csv(n,h,x):np.savetxt(O/n,x,delimiter=',',header=','.join(h),comments='',fmt='%.10g')
h=1.0072764665789;u=1.66053906892e-27;e=1.602176634e-19
neutral=8*12+10*1.00782503223+4*14.00307400443+2*15.99491461957;target=neutral+h
fig,axs=plt.subplots(1,3,figsize=(14.4,4.6),layout='constrained')
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(t('A  电喷雾：从液滴到离子','A  Electrospray: droplets to ions'))
ax.add_patch(Rectangle((.2,3.2),2,1.2,facecolor='#d3e2e6',edgecolor=B));ax.add_patch(Polygon([[2.2,3.2],[3,3.8],[2.2,4.4]],facecolor='#d3e2e6',edgecolor=B))
for x,y,r in [(3.5,3.8,.48),(4.8,4.3,.32),(5.6,3.4,.23),(6.7,4,.15)]:ax.add_patch(Circle((x,y),r,fc='#bad8df',ec=B));ax.text(x,y,'+',ha='center',va='center',color=B)
for y in [3.4,4,4.6]:ax.text(8,y,'M⁺',fontsize=12,color=R)
ax.annotate('',(9.5,3.9),(7.4,3.9),arrowprops={'arrowstyle':'->','color':R});ax.text(.5,6.4,t('电压 + 溶液\n蒸发与带电液滴演化','Voltage + solution\nEvaporation and charged droplets'),fontsize=10);ax.text(.5,1,t('1989：Fenn 等报告完整生物分子多电荷谱','1989: Fenn et al., multiply charged biomolecules'),fontsize=9,wrap=True)
ax=axs[1];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(t('B  激光解吸：基质帮助能量传递','B  Laser desorption: a supporting matrix'))
ax.add_patch(Rectangle((1,1.4),8,.4,fc='#8f9aab'));ax.add_patch(Polygon([[2,1.8],[3,2.5],[4,1.8],[5,2.7],[6,1.8],[7,2.4],[8,1.8]],fc='#e4c775',ec=Y));ax.annotate('',(4.8,2.6),(2,6.5),arrowprops={'arrowstyle':'->','lw':3,'color':R})
for x,y in [(5.5,3.7),(6.4,4.9),(7.4,5.8)]:ax.text(x,y,'M⁺',color=B)
ax.text(1,7,t('脉冲激光','Pulsed laser'),color=R);ax.text(1,.2,t('基质 + 待测分子；示意不按尺度','Matrix + analyte; schematic dimensions'),fontsize=9);ax.text(1,.95,t('1987：Tanaka 团队的软激光解吸','1987: Tanaka team, soft laser desorption'),fontsize=9)
ax=axs[2];mass=np.array([100,400,1600]);tof=1*np.sqrt(mass*u/(2*e*5000))*1e6;ax.plot(mass,tof,'o-',color=G);ax.set(xlabel=t('单电荷离子质量 / Da','Singly charged ion mass / Da'),ylabel=t('理想飞行时间 / μs','Ideal flight time / μs'),title=t('C  飞行时间：质量越大越慢','C  Flight time: larger mass, slower ion'));ax.text(.04,.83,'L=1 m; U=5 kV; z=1',transform=ax.transAxes,fontsize=10)
save(fig,'ionization')

fig,axs=plt.subplots(1,3,figsize=(14.4,4.8),layout='constrained');charge=np.arange(6,13);mz=12000/charge+h;intens=g(charge,9,1.6)
ax=axs[0];ax.vlines(mz,0,intens,color=B,lw=3)
for x,z,y in zip(mz,charge,intens):ax.text(x,y+.04,f'{z}+',ha='center',fontsize=9)
ax.set(xlabel='m/z',ylabel=t('构造相对强度','Constructed relative intensity'),title=t('A  一个 12,000 Da 分子的电荷系列','A  Charge series of one 12,000 Da molecule'),ylim=(0,1.25))
ax=axs[1];k=np.arange(5);pr=np.array([math.comb(50,int(i))*.0107**i*(1-.0107)**(50-i) for i in k]);pr/=pr.max()
for z,col in [(1,B),(2,R),(3,G)]:ax.vlines(k*1.00335483507/z,z-1,z-1+.65*pr,color=col,lw=3,label=f'z={z}')
ax.set(xlabel=t('相对首峰的 m/z 间隔','m/z displacement from first isotope'),ylabel=t('为比较而上下错开','Vertically offset for comparison'),title=t('B  同位素间距随电荷压缩','B  Charge compresses isotope spacing'),yticks=[]);ax.legend(frameon=False)
ax=axs[2];x=np.linspace(195.02,195.17,3000)
for j,(res,col) in enumerate([(5000,Y),(50000,B)]):
 sig=target/res/2.354820045;yy=g(x,target,sig)+.7*g(x,target+.01435,sig);ax.plot(x,yy+j*1.8,color=col,label=f'R={res:,}')
ax.set(xlabel='m/z',ylabel=t('构造信号，垂直错开','Constructed signal, offset'),title=t('C  分辨本领决定能否分开近邻','C  Resolving nearby ions'));ax.ticklabel_format(useOffset=False,axis='x');ax.legend(frameon=False,fontsize=9)
save(fig,'charge-resolution')

record=(Path(__file__).parent/'data/MSBNK-BAFG-CSL2311094663.txt').read_text(encoding='utf8');peaktext=record.split('PK$PEAK: m/z int. rel.int.')[1].split('//')[0];peaks=np.array([[float(x) for x in ln.split()] for ln in peaktext.splitlines() if ln.strip()]);assert len(peaks)==23
relative=100*peaks[:,1]/peaks[:,1].max();base=peaks[np.argmax(peaks[:,1]),0]
fig,axs=plt.subplots(1,2,figsize=(12.8,4.9),gridspec_kw={'width_ratios':[1.55,1]},layout='constrained');ax=axs[0];ax.vlines(peaks[:,0],0,relative,color=B,lw=1.8)
for i in np.argsort(relative)[-5:]:ax.text(peaks[i,0],relative[i]+3,f'{peaks[i,0]:.4f}',ha='center',fontsize=9,rotation=50)
ax.set(xlabel='m/z',ylabel=t('相对最大峰的强度 / %','Intensity relative to base peak / %'),ylim=(0,130),title=t('A  真实咖啡因 MS/MS：40 V','A  Actual caffeine MS/MS: 40 V'));ax.text(.03,.88,'MSBNK-BAFG-CSL2311094663',transform=ax.transAxes,fontsize=8)
ax=axs[1];ax.axis('off');ax.text(.02,.93,t('B  一个记录里的不同质量信息','B  Different mass information in one record'),weight='bold');lines=[t('分子式：C₈H₁₀N₄O₂','Formula: C₈H₁₀N₄O₂'),t('由同位素质量计算中性质量','Neutral mass calculated from isotope masses')+f'\n{neutral:.6f} Da',t('计算 [M+H]⁺','Calculated [M+H]⁺')+f'\nm/z {target:.6f}',t('记录前体设置：195.0877','Record precursor metadata: 195.0877'),t('谱内保留的峰：195.0873','Retained spectral peak: 195.0873'),t('CC BY；Ehlig, Lessmann, Jewell, Wick / BfG','CC BY; Ehlig, Lessmann, Jewell, Wick / BfG')]
for j,txt in enumerate(lines):ax.text(.02,.79-j*.145,txt,fontsize=10,va='top')
save(fig,'reference-spectrum');csv('reference_peaks.csv',['mz','original_intensity','record_relative_0_999','replotted_percent'],np.c_[peaks,relative])

# Constructed LC-MS scan matrix with target and nearby interfering ion.
rng=np.random.default_rng(630);time=np.linspace(0,8,801);masses=np.linspace(target-.04,target+.04,801);sig=target/40000/2.354820045
lc=g(time,4,.22);inter=g(time,4.4,.28);spectra=1000*lc[:,None]*g(masses,target,sig)[None,:]+800*inter[:,None]*g(masses,target+.01435,sig)[None,:]+rng.uniform(0,1,(len(time),len(masses)))
tic=spectra.sum(axis=1);narrow=np.abs(masses-target)<=target*5e-6;wide=np.abs(masses-target)<=target*100e-6;xic=spectra[:,narrow].sum(axis=1);broad=spectra[:,wide].sum(axis=1)
fig=plt.figure(figsize=(12.8,8),layout='constrained');gs=fig.add_gridspec(2,2);ax=fig.add_subplot(gs[:,0]);im=ax.imshow(np.log10(1+spectra),aspect='auto',origin='lower',extent=[masses[0],masses[-1],time[0],time[-1]],cmap='magma');ax.set(xlabel='m/z',ylabel=t('保留时间 / min','Retention time / min'),title=t('A  每个时间都有一张质谱','A  A spectrum at each time'));ax.ticklabel_format(useOffset=False,axis='x');fig.colorbar(im,ax=ax,label='log₁₀ (1 + signal)')
ax=fig.add_subplot(gs[0,1]);ax.plot(time,tic/tic.max(),color=Y,label=t('所示质量窗口总信号','Total in displayed mass window'));ax.plot(time,xic/xic.max(),color=B,label=t('目标 ±5 ppm','Target ±5 ppm'));ax.set(xlim=(3,5.5),xlabel=t('时间 / min','Time / min'),ylabel=t('各曲线除以自身最大值','Each curve / its own maximum'),title=t('B  提取目标的时间轨迹','B  Extract the target time trace'));ax.legend(frameon=False,fontsize=9)
ax=fig.add_subplot(gs[1,1]);ax.plot(time,xic/xic.max(),color=B,label='±5 ppm');ax.plot(time,broad/broad.max(),color=R,label='±100 ppm');ax.set(xlim=(3,5.5),xlabel=t('时间 / min','Time / min'),ylabel=t('各自归一化信号','Individually normalized signal'),title=t('C  宽窗口混入近邻','C  A wide window admits interference'));ax.legend(frameon=False)
save(fig,'lcms-map');csv('extracted_chromatograms.csv',['time_min','displayed_window_total','target_5ppm','target_100ppm'],np.c_[time,tic,xic,broad]);np.savez_compressed(O/'constructed_lcms.npz',time_min=time,mz=masses,signal=spectra)

c=np.repeat([0,1,2,5,10,20],3);ratio=.08*c+.01+rng.normal(0,.008,len(c));slope,intercept=np.polyfit(c,ratio,1);sample_true=8.;supp=.55;IS=500.;response=1000.;analyte=sample_true*response*supp;internal=IS*supp
# This separate ratio calibration uses response ratio = 0.08*c+0.01.
unknown_ratio=.08*sample_true+.01;estimated=(unknown_ratio-intercept)/slope
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained');ax=axs[0,0];ax.bar([0,1],[100,55],color=[G,R]);ax.set_xticks([0,1],[t('纯溶剂','Neat solvent'),t('提取后基质','Post-extraction matrix')]);ax.set(ylabel=t('等浓度目标响应 / %','Equal-concentration response / %'),title=t('A  基质因子 0.55','A  Matrix factor 0.55'),ylim=(0,115))
ax=axs[0,1];supps=np.linspace(.3,1,100);ax.plot(supps,sample_true*supps,color=R,label=t('按纯溶剂外标','Neat external calibration'));ax.plot(supps,np.full_like(supps,sample_true),color=B,label=t('同受抑制的内标比值','Matched internal-standard ratio'));ax.set(xlabel=t('共同响应因子','Common response factor'),ylabel=t('估计浓度 / ng/mL','Estimated concentration / ng/mL'),title=t('B  比值抵消共同变化','B  Ratios cancel shared changes'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,0];ax.scatter(c,ratio,color=B,s=18);ax.plot([0,20],[intercept,20*slope+intercept],color=D);ax.set(xlabel=t('目标浓度 / ng/mL','Analyte concentration / ng/mL'),ylabel=t('目标 / 内标面积比','Analyte / internal-standard area'),title=t('C  构造比值校准与重复值','C  Constructed ratio calibration'))
ax=axs[1,1];xx=np.linspace(.3,1,100);ax.plot(xx,sample_true*.55/xx,color=R);ax.axhline(8,color=B,ls='--');ax.axvline(.55,color=Y,ls='--');ax.set(xlabel=t('内标响应因子','Internal-standard response factor'),ylabel=t('估计浓度 / ng/mL','Estimated concentration / ng/mL'),title=t('D  内标与目标不同步时','D  When the standard does not track analyte'))
save(fig,'quantitation');csv('ratio_calibration.csv',['concentration_ng_per_mL','area_ratio'],np.c_[c,ratio])
summary={'neutral_caffeine_Da':neutral,'protonated_caffeine_mz':target,'reference_peak_count':len(peaks),'reference_base_peak_mz':base,'reference_precursor_metadata_ppm':(195.0877-target)/target*1e6,'reference_retained_peak_ppm':(195.0873-target)/target*1e6,'charge_12_mz':12000/12+h,'isotope_spacing_z2':1.00335483507/2,'tof_400Da_5kV_us':float(tof[1]),'resolution_FWHM_R40000':target/40000,'matrix_factor':.55,'neat_external_apparent_ng_per_mL':8*.55,'matched_internal_standard_ng_per_mL':8.,'ratio_calibration_slope':float(slope),'ratio_calibration_unknown_ng_per_mL':float(estimated),'target_XIC_apex_min':float(time[np.argmax(xic)])}
assert abs(target-195.087652)<1e-6 and base==138.0657
assert abs(estimated-8)<.3 and abs(time[np.argmax(xic)]-4)<=.01
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

蛋白质研究可以把质谱用于完整质量确认，也可以先将蛋白切成肽段，再根据碎片系列分析序列及修饰。材料研究则可能关注单体残留、释放物、氧化产物或聚合物端基。它们都需要说明自己测的是完整分子、提取组分、酶解产物还是碰撞后的离子，并保存对应的制备与采集条件。最后的结果应让读者顺着“样品是什么—产生了什么离子—用了哪些质量与碎片线索—怎样完成浓度换算”继续追问。这样的质谱图既能回答当下问题，也能成为下一次实验设计的起点。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Fenn et al. (1989): Electrospray ionization for mass spectrometry of large biomolecules](https://pubmed.ncbi.nlm.nih.gov/2675315/)

   原始论文摘要中的完整大分子与多电荷系列。
2. [Shimadzu: Koichi Tanaka research history](https://www.shimadzu.com/about/nobel/noblesoul/re_hstry.html)

   1987 年软激光解吸报告与后续仪器发展。
3. [MassBank: MSBNK-BAFG-CSL2311094663](https://github.com/MassBank/MassBank-data/blob/dev/BAFG/MSBNK-BAFG-CSL2311094663.txt)

   咖啡因参考谱、23 个峰、条件与原始许可。

   CC BY as specified in the record; authors and copyright retained; replotted intensities normalized to base peak.
4. [MassBank record format 2.6](https://github.com/MassBank/MassBank-documentation/blob/dev/MassBankRecordFormat.md)

   记录字段、谱内峰与前体元数据、逐记录许可。
5. [Waters: Mass accuracy and resolution](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/mass-accuracy-and-resolution.html)

   峰宽与中心误差、校准和干扰。
6. [Waters: Solvents and caveats for LC-MS](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/solvents-and-caveats-for-lcms.html)

   电离兼容性、基质响应与提取后加标。
7. [Waters: Quantitation and calibration](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/quantitation-and-calibration.html)

   内标、同位素标记与质量轴校准。
8. [NIST: Atomic weights and isotopic compositions](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl)

   C、H、N、O 指定同位素质量与碳同位素差。
9. [NIST: CODATA recommended constants 2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf)

   质子质量、元电荷与原子质量单位。
