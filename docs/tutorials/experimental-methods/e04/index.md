# 释放实验：药物与蛋白质怎样离开载体

Source: https://ml-biomat.com/tutorials/experimental-methods/e04/
Language: zh-CN

从分子路程、标准曲线和取样账本出发，重建累计释放，分辨材料、介质与装置的作用。

## 同样装进去一份分子，为什么出来的时间不同

把一包茶叶放进水里，杯中的颜色会逐渐加深；换成一块装有蛋白质的水凝胶，肉眼可能看不到变化，却同样可以追问：分子已经出来多少，还留在里面多少，接下来会以怎样的速度出来？释放实验把这个问题变成一条随时间变化的曲线。对于局部递送材料，研究者关心的是分子能否在需要的时间内到达周围环境；对于含抗菌成分的涂层，关心的可能是最初的快速释放与后续维持之间的配合。曲线的用途首先来自这种时间安排，而不是来自曲线是否平滑、最终数字是否接近百分之百。

这里的“载体”是储存目标分子的材料，例如微球、薄膜、凝胶或多孔支架；“接收液”是包围载体、接受已释放分子的液体。一次实验通常从已知载药量出发，在几个时间点测接收液中的浓度，再换算已经进入外部环境的总量。浓度表示每单位体积含有多少目标物，质量则表示这一整份液体里共有多少。两者的区别很像糖水的甜度与整杯糖水中的糖量：一杯更甜的水，未必含有更多糖；只有同时知道杯子的容量，才能完成比较。这个简单区分贯穿后面所有的取样计算。

“释放”“溶出”和“渗透”侧重的环节也不同。固体药物先变成溶液中的分子，强调的是溶出；已经溶解的分子从材料内部到外部，强调的是释放；分子穿过一层膜到达另一侧，强调的是渗透。一个实验可能同时包含这三个环节。若把载药颗粒装进透析袋，外液里测到的分子既经历了离开颗粒，也经历了穿过透析膜。把路线画出来，就能看出哪一个环节需要单独测量。下面先以直接浸泡载体的实验为主，再讨论膜、蛋白质稳定性和材料变化怎样影响结果。

![原创示意图把直接浸泡、取样补液和 Higuchi 移动耗尽前沿连接起来。1961 年的历史思想解释平方根时间关系所对应的空间过程，图示不表示某个真实装置的尺寸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/219c543d8dad34d3653187a5.svg?v=219c543d8dad)

图 1原创示意图把直接浸泡、取样补液和 Higuchi 移动耗尽前沿连接起来。1961 年的历史思想解释平方根时间关系所对应的空间过程，图示不表示某个真实装置的尺寸。

研究开始时还应确定“出来了”的化学含义。对稳定小分子，可以测其完整分子的色谱峰；对蛋白质，显色法可能给出可反应蛋白质总量，荧光法则追踪带荧光的物种。一个蛋白质断成仍带染料的片段后，外液可能依旧很亮，但完整蛋白质和生物活性已经改变。因而释放量、完整性和功能通常对应不同测量。先把目标写成“完整蛋白的累计释放”或“带标记物种的累计进入量”，就能选对分析手段，也能理解两个检测方法为什么可能得到不同的曲线。

## 一条释放曲线里，藏着哪几段路程

材料内部的分子持续做热运动。在没有整体流动时，某一区域分子更多，平均便会有更多分子从那里走向分子较少的区域，这形成扩散。凝胶网络像一座有通道和可停留位置的城市：通道宽度影响分子通过的难易，分子与网络的亲和作用影响它停留多久。这个比喻中的“停留”有明确的物理对应，例如电荷吸引、疏水相互作用或可逆结合。同样大小的两个蛋白质若与网络的作用不同，释放速度也可以明显不同，分子量因此只提供结构线索，还需要结合分子的形状、表面性质和介质条件解释。

扩散到材料表面以后，分子还要穿过靠近表面的液体层，再进入充分混合的外液。搅拌主要改变这段外部传质路径；它不能直接把网络内部的所有阻力都消除。若提高搅拌速度后释放明显加快，可能说明外部液层参与控制过程；若过强搅拌使脆弱凝胶破碎，观察到的变化又包含表面积和结构改变。因此，选择混合条件要同时考虑样品完整性与外液均匀性。比较配方时固定容器形状、液体高度、样品位置和混合方式，往往比只记录一个转速更能解释结果。

1961 年，Higuchi 从含有未溶解药物颗粒的软膏出发，把药物溶解和向外扩散联系起来。靠近表面的药物先被耗尽，内部仍有固体药物补充，耗尽区域的边界逐渐向深处移动。随着这段路程变长，单位时间出来的量逐渐减小，在相应条件下累计释放量与时间的平方根成正比。图中的移动前沿正是这一历史模型的核心。它说明一种曲线形状可以来自明确的空间过程，也提醒我们在使用方程时同时带上原来的几何、装载状态和边界条件。

$$
Q(t)=k_H\sqrt{t}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/152cda6bbc8d048536474158.svg) | 单位暴露面积的累计释放质量，μg/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a60ad9059bb079f3031bcf0.svg) | 固定几何与实验条件下的 Higuchi 系数，μg cm^{-2} h^{-1/2}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从相应模型起点计算的时间，h。 |

用于满足相应扩散控制条件的阶段，如近似平面、不显著溶胀、内部有固体药物补给且外部维持低浓度的体系。系数为 10 μg cm⁻² h⁻¹ᐟ² 时，1 h 和 4 h 的 Q 分别为 10 和 20 μg/cm²：时间增为四倍，累计量增为两倍。

平方根关系适合讨论特定扩散控制阶段。若凝胶明显溶胀、网孔持续变化、药物与网络强烈结合，或外液浓度逐渐升高，控制过程也随之改变。后续研究已经直接求解合适边界条件下的扩散方程，考察初始药物浓度接近溶解度时的变化。学习这些工作时，可以先问材料里是否还有固体药物、几何是否保持、外部是否不断带走分子，再选择模型。对任何一条递增曲线都尝试平方根拟合，容易让不同的物理过程被相似的线条掩盖。

真实材料还可能出现“突释”：实验早期有一部分分子迅速进入外液。表面附近的装载、干燥后形成的微裂纹、未结合的游离组分，都可能贡献这一部分。突释也可能与实验起点定义有关，例如把预洗过程漏出记录后，第一份样液就已经错过了最快阶段。判断它的原因，可以比较预洗液、表面装载量、样品尺寸与早期密集取样。需要早期作用的应用可能利用这部分释放，要求长期平缓供给的应用则会调整它；研究目标决定如何评价，而不是给突释一个固定的好坏标签。

## 让外液和检测方法配合研究问题

接收液的体积有两个作用：它决定浓度如何换算成质量，也决定外部环境还能接纳多少目标物。若溶解度有限，外液越来越接近饱和，分子继续离开材料的驱动力便会减小。这时的缓慢释放部分来自外液容量，而不是材料内部阻力。常说的“漏槽条件”就是让外部环境有足够的接纳能力。可以把它理解成一个不断留出空位的接收站。实际设计时测目标物在所用温度、pH 和介质中的溶解度，再将预计释放量与外液容量比较；对存在结合或分配的蛋白质，还要检查外液浓度是否足够低。

不同研究目的需要不同边界条件。寻找材料内部传输规律时，较大的接收液体积和适当混合可以减小外部限制；研究局部有限液体环境时，则可能主动采用有限体积，并把它作为模型的一部分。补液会带走已释放分子，也可能带走材料降解产物、改变缓冲能力。因此，补液频率本身就是实验条件。表面活性剂能改善某些疏水分子的溶解，却也可能影响材料结构、蛋白构象和检测信号。选介质时应同时考虑溶解、稳定、材料响应与分析兼容性，而不是只追求释放曲线尽快到达平台。

载药量需要实际测定。设制备时投入 100 μg 药物，最终载体中测得 80 μg，包封效率是投入量中进入载体的比例，即 80%；如果载体的总干质量为 1000 μg，载药量按这个总质量定义则为 8%。前者回答制备过程中保留了多少，后者回答单位制剂带有多少，两者的分母不同。释放百分数通常以实验开始时载体内真实存在的药物量为分母。用制备投料量代替它，会把制备损失混进释放结果，让平台偏低的原因变得难以辨认。

$$
\mathrm{EE}=\frac{M_0}{M_{\rm feed}},\qquad \mathrm{LC}=\frac{M_0}{m_{\rm formulation}},\qquad F_n=\frac{M_n}{M_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e74566520b2ff9dc2654ee32.svg) | 包封效率，无量纲；乘 100 为百分数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fe3f0356dce96af85bcb9aa5.svg) | 本节按制剂总干质量定义的载药质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d39d4c6ec0676acff39eb9eb.svg) | 第 n 次取样时相对初始实际装载量的累计释放比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | 释放实验开始时实际装载的目标物质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a287a1335b8b0aa8e20296d1.svg) | 制备时投入的目标物质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/907e414ff4732c512fcc64d7.svg) | 含目标物的完整制剂干质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | 第 n 次取样时累计已释放目标物质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 取样序号，无量纲。 |

三个比例分别回答制备保留、制剂组成和释放进度。投入 100 μg、实际装入 80 μg、制剂总干质量 1000 μg 时 EE=80%、LC=8%；另一个初始装载 100 μg 的释放示例，累计 60 μg 对应 Fn=60%。

测装载量可以直接提取载体，也可以测制备和清洗液后做质量差额。直接提取需要验证回收率，即已知加入多少、最终能测回多少；间接方法则要检查药物是否吸附在容器、滤膜和管路上。空白载体浸泡液可以揭示材料自身的吸收、荧光或显色反应；已知浓度目标物经过同样储存和过滤的对照可以检查处理损失。对蛋白质，冻融、长时间温育与表面吸附都可能影响测得量。把这些对照放在实验设计中，后面出现低回收时就有具体路径可以追查。

时间点应跟随过程安排。若预期最初一小时变化快，可以在这段时间增加取样密度；后期缓慢变化时适当拉长间隔。每个载体持续取样得到的是一条完整轨迹，同一轨迹上的多个时间点来自同一个实验单位。比较多个配方时，应有独立载体或独立制备批次，并保存每条轨迹，再在相同时间点汇总。把一条轨迹上的八个时间点当成八个独立样品，会把时间上的连续性误当成样品间重复性，也会低估制备差异。

## 已经取走的那一份，也属于累计释放

检测仪器先给出信号，再由标准曲线换成浓度。标准曲线应尽量使用与样液相同的介质和处理过程，因为盐、缓冲组分和材料浸出物可能改变背景或反应效率。在线性范围内，斜率告诉我们浓度增加一个单位时信号增加多少，截距表示零浓度附近的背景。先减去背景，再除以斜率，就像从一把带零点偏移的尺子读出真正长度。若样液经过稀释，还要乘回稀释倍数。示例中吸光度为 0.090、背景为 0.030、斜率为 0.012 mL/μg，测量液浓度为 5 μg/mL；若此前做了两倍稀释，原样液浓度就是 10 μg/mL。

$$
C=d\frac{A-b}{a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 原样液浓度，μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 取样后分析前的稀释倍数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 测量液吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 同介质标准曲线的截距，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 标准曲线斜率，mL/μg。 |

在线性校准范围内先扣背景再除以灵敏度，最后恢复稀释。A=0.090、b=0.030、a=0.012 mL/μg、d=2 时，测量液为 5 μg/mL，原样液 C=10 μg/mL。

现在看最容易漏掉的质量账本。容器始终保持 10 mL 接收液，每次取出 2 mL 并补回同体积新液。第一次共释放 20 μg，浓度是 2 μg/mL，取样带走 4 μg。第二次累计已经释放 40 μg，但容器里只有 36 μg，因为前一次的 4 μg 已经进入收集管；此时浓度是 3.6 μg/mL，第二次取样再带走 7.2 μg。到第三次累计释放 60 μg 时，当前容器里还有 48.8 μg，浓度为 4.88 μg/mL。把当前质量与此前取走的 11.2 μg 相加，才得到完整的 60 μg。

$$
M_n=VC_n+\sum_{i=1}^{n-1}v_iC_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | 第 n 次取样前的累计释放质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 每次补液后维持的接收液总体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd358f69abfbebbae37cb3dc.svg) | 第 n 次取样前混匀外液浓度，μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/03fe412bc6d88c2f14c43e45.svg) | 此前第 i 次取出的样液体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/971aeb8f6c70c0afe2138963.svg) | 此前第 i 次取样时的外液浓度，μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 当前取样编号，无量纲正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 此前取样编号；求和只累加 1 至 n−1。 |

假设新补液不含目标物、外液混匀且目标物在收集期间保持所测形式。10 mL 外液、前两次各取 2 mL，浓度依次为 2、3.6、4.88 μg/mL 时，M3=10×4.88+2×2+2×3.6=60 μg。

公式中的求和只包括当前时间点之前的样液。当前取样前，当前那一份仍包含在整杯液体的质量中；如果又把它额外相加，就会算两次。每次取样体积相同，可以使用一个固定体积；体积不同时，就逐次记录各自的体积与浓度。若不补液，当前液体体积会减少，第一项要使用实际剩余体积。若每次完全换液，每段收集量直接累加；若实验采用连续流动，则需要对出口浓度与流量随时间的乘积积分。各种写法背后的共同规则，是每一份目标物只进入账本一次。

![固定随机种子的构造数据：标准曲线、累计取样校正、质量账本和取样体积敏感性。每次校正都把当前外液质量与此前取走的质量相加；灰线为用于生成信号的已知过程。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/44487c87255c5a355a6d6a08.svg?v=44487c87255c)

图 2固定随机种子的构造数据：标准曲线、累计取样校正、质量账本和取样体积敏感性。每次校正都把当前外液质量与此前取走的质量相加；灰线为用于生成信号的已知过程。

取样校正还能解释一个看似奇怪的现象：即使材料不断释放，当前外液浓度也可能在后期下降。原因是新释放的量已经很少，而每次取样和补液仍在稀释外液。图中改变每次取样体积，未校正曲线的形状随之改变，真正的构造释放过程却完全相同。这说明浓度曲线、当前外液中的质量曲线和累计释放曲线是三个不同对象。写图轴时明确是哪一个对象，比把它们统称为“释放量”更能避免误读。

累计计算还会让误差沿时间传播。早期某一份样液的浓度偏高，它带来的取样质量偏差会进入后续每个累计点；标准曲线斜率偏差则会一起影响整条轨迹。逐点误差棒因此不等于各时间点彼此独立。保存原始信号、稀释倍数、取样体积和每条独立轨迹，便能重新计算误差来源。出现略高于百分之百的值时，应先检查装载量分母、标准曲线、体积和回收率，而不是直接截断到百分之百，让原本有用的测量线索消失。

## 取样多一点，累计释放会变少吗

三个时间点的真实累计释放固定为 20、40、60 μg。每次取样后补回相同体积的空白介质；比较当前外液与校正累计量。

[Figure: 当前外液与此前取样的质量组成](https://ml-biomat.com/tutorials/experimental-methods/e04/#E04-plot)

## 读懂曲线的速度、平台和残差

如果释放量要用于比较两种材料，先选出与用途对应的比较量。例如早期需要多少分子，可以比较明确时间点的绝对释放量；希望维持较稳定的供给，可以比较目标时间窗内的区间速率；关心剩余储备，可以测末期载体中的残留量。某个配方更早达到自身终点的百分之五十，并不一定意味着它在同一时刻释放了更多绝对质量，因为两者的实际装载量可能不同。把用途、绝对量和归一化曲线并排，比较才不会被一个单独的时间指标带偏。

累计曲线告诉我们到某一时刻总共出来多少，释放速率则告诉我们一段时间里出来得有多快。最直观的平均速率是相邻两次累计量之差，再除以时间间隔。例如一小时到两小时之间累计量从 20 μg 增至 40 μg，这一小时的平均释放速率就是 20 μg/h。若采样间隔长，短暂的快速变化会被平均掉；若间隔很短，浓度测量的小误差又可能在相减后变得显眼。因此速率曲线需要与原始累计曲线、采样时间和测量精度一起阅读。

$$
\overline{r}_n=\frac{M_n-M_{n-1}}{t_n-t_{n-1}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4ab9018ce0331a4605783315.svg) | 相邻两次取样之间的平均释放速率，μg/h。 |
| ![Formula](https://ml-biomat.com/static/agent-math/99086759c8e6738285d27c72.svg) | 当前与前一次的累计释放质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/93d9aabfdc04713b7cefd665.svg) | 当前与前一次的取样时间，h。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 当前取样编号，n≥2。 |

相邻累计量之差就是这段时间新增的释放质量。1 h 时 20 μg、2 h 时 40 μg，平均速率为 (40−20)/(2−1)=20 μg/h；这是区间平均值。

平台也需要质量去向来解释。它可能意味着可释放部分已经离开，也可能意味着剩余分子强烈结合、外液接近饱和、目标物发生降解，或者检测低于可定量范围。实验终点可以提取载体中的残留量，同时分析已收集样液和容器冲洗液，建立“已释放、仍保留、处理损失或转化”的账本。若平台之后改变介质体积、混合或pH，曲线再次上升，这些有目的的条件改变还能帮助区分外部容量、结合平衡和传输路径的贡献。

拟合模型应回答一个具体问题，例如比较同一几何与介质下的特征时间，或检验早期过程是否符合某种扩散描述。先看数据再画残差，即每个观测值减去模型预测值。示例的构造过程包含一小部分快速释放和一大部分慢速释放，却用只有一个时间尺度的指数曲线拟合。拟合线整体看起来可以贴近数据，但早期残差呈有方向的变化，指出模型遗漏了一个过程。随机散布的小残差与连续偏向一侧的残差意义不同，后者常常提示模型结构或实验条件需要重新审视。

![构造诊断：一个时间尺度拟合两个时间尺度的释放过程，残差显示早期偏差；右图固定载体特征时间 4 h，只改变串联膜过程的特征时间，展示装置对外液曲线的影响。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0f5ef578e52dbb8473303070.svg?v=0f5ef578e52d)

图 3构造诊断：一个时间尺度拟合两个时间尺度的释放过程，残差显示早期偏差；右图固定载体特征时间 4 h，只改变串联膜过程的特征时间，展示装置对外液曲线的影响。

透析实验尤其需要分开考虑两道传质过程。载体先把分子释放到袋内，再由袋内穿膜进入外液；如果膜过程很慢，外液曲线主要反映膜的筛选与传输，而载体本身的差异可能被压缩。可以将等量游离目标物放入相同透析装置，测它的通过时间，并检查膜吸附和总回收。图中的两阶段模型固定载体自身的时间尺度，只改变膜过程的时间尺度，外液曲线就明显改变。这个比较把一项装置对照与一个可观察的曲线变化直接连在一起。

## 把材料变化与真正的释放证据放在一起

前面几章已经讨论过溶胀、网络连接和降解。它们在释放实验中会共同改变通道：溶胀可能增加分子可通过的空间，也会增加从内部到表面的距离；降解可能松开网络，也可能使样品形状和表面积改变。这些效应方向未必一致。于是，单看释放变快或变慢，很难直接反推出某个网孔尺寸。更有信息量的做法，是在相同时间窗测厚度、含水变化、分子迁移和结构完整性，再把这些测量放进同一幅机制图中解释。

Sheth 等在 2019 年研究可降解凝胶中的蛋白质释放时，分别测量蛋白质扩散和凝胶厚度随时间的变化，再用于预测外液释放曲线。这项工作的可借鉴之处，是模型输入来自独立测量，随后与整体释放实验比较。图中保留了两种蛋白质的实测点与模型线，读者可以观察偏差出现在哪一段，而不是只看“符合”与“不符合”两个标签。原研究也比较了时间变化参数和平均参数的预测，展示了结构变化有时会以相互补偿的方式影响整体结果。

![真实研究图完整转载自 Sheth 等（2019）Figure 5，Frontiers in Bioengineering and Biotechnology 7:410，DOI 10.3389/fbioe.2019.00410，CC BY 4.0。原图保留 BSA 和 IgG 的实验点与模型线；原文报告 n=9、误差为一个标准差。仅新增外部标题与署名。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f481b01d16422409666dc33f.svg?v=f481b01d1642)

图 4真实研究图完整转载自 Sheth 等（2019）Figure 5，Frontiers in Bioengineering and Biotechnology 7:410，DOI 10.3389/fbioe.2019.00410，CC BY 4.0。原图保留 BSA 和 IgG 的实验点与模型线；原文报告 n=9、误差为一个标准差。仅新增外部标题与署名。

这里还有一个值得追问的测量层次。观察单个示踪分子的局部运动，与在浓度梯度下测一整块材料的净传输，获得的扩散信息并不总是完全等价；示踪标记、结合、非均匀性和分子间相互作用都可能参与。对于蛋白质，还可以把释放样液接入结构或功能测量，例如检查分子大小分布、保留的结合能力或相应生物反应。这样，材料研究中的“释放完成”就能进一步分解为分子已离开、结构仍完整、所需功能仍保留几个可测的问题。

读公开曲线时，也要查看分母如何定义。以初始实际载药量归一化，回答最初装载的目标物释放了多少；以实验最后回收到的总量归一化，回答本次可回收部分的时间分布；以拟合平台归一化，则额外依赖模型。三种曲线可能都在终点接近百分之百，却表达不同事实。将质量基准与原始绝对量一起保留，才能让不同配方、不同研究和不同检测方法之间的比较具有共同尺度。

## 从原始吸光度重建一条释放轨迹

过滤也是一个可以单独检验的步骤。用已知浓度目标物分别测过滤前后信号，同时用空白介质检查滤膜浸出物；不同浓度下重复这一比较，可以发现低浓度时吸附损失比例更大的情况。如果样品里存在带药颗粒，过滤还会改变所测对象：滤液可能代表溶解部分，而未经分离的样液包含颗粒散射或颗粒相关目标物。根据研究问题选择这一分离步骤，并在结果中沿用相同定义，便能将样品处理与最终曲线连接起来。

下面的完整示例从已知构造释放过程出发，依次模拟取样、补液、标准曲线和小幅测量噪声，再从吸光度重建浓度与累计量。程序同时导出当前外液质量、此前取样质量和校正后的累计量，每一列都能与前面的账本对应。四联图展示标准曲线、校正前后差异、各时间点的质量组成以及取样体积敏感性；另一个诊断图展示单时间尺度拟合的残差和透析膜的影响。公开研究图与许可说明也随示例提供，可以在相同页面查看计算输出和真实研究证据。

### 完整 Python：从吸光度到累计释放和模型诊断

代码导出原始信号、校准数据、质量账本、模型残差及四幅图；取样校正首先接受独立质量守恒检查。

```
"""Serial-sampling release accounting and constructed transport diagnostics."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch,Circle

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def sampled_concentration(cumulative,bath=10.,aliquot=2.):
    removed=0.;concentrations=[]
    for released in cumulative:
        c=(released-removed)/bath;concentrations.append(c);removed+=aliquot*c
    return np.asarray(concentrations)

def correct(concentration,bath=10.,aliquot=2.):
    c=np.asarray(concentration);return bath*c+aliquot*np.r_[0,np.cumsum(c[:-1])]

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.5))
    for a in ax:a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    for i,a in enumerate(ax[:2]):
        a.add_patch(Rectangle((1,2),8,6,facecolor='#c9e3e9',edgecolor='#186e83',lw=2));a.add_patch(Rectangle((3.3,3),3.4,1.7,facecolor='#8160a1',alpha=.65));a.text(5,3.8,tr('载体','Carrier'),ha='center',va='center',color='white');a.add_patch(FancyArrowPatch((5,5),(5,7),arrowstyle='->',mutation_scale=16,color='#186e83'));a.text(5,1,tr('混匀的接收液','Mixed receiving medium'),ha='center',fontsize=10)
    ax[0].set_title(tr('A  载体中储存的分子','A  Molecules stored in a carrier'));ax[1].set_title(tr('B  取出样液，补入新液','B  Sample out, fresh medium in'))
    for x,direction,label,color in [(2.5,1,tr('取样','Sample'),'#cd803f'),(7.5,-1,tr('补液','Replace'),'#3c8a6a')]:ax[1].add_patch(FancyArrowPatch((x,7 if direction==1 else 9),(x,9 if direction==1 else 7),arrowstyle='->',mutation_scale=15,color=color));ax[1].text(x,9.3,label,ha='center',fontsize=9)
    ax[2].add_patch(Rectangle((1,2),8,6,facecolor='#e6dcc7'));ax[2].add_patch(Rectangle((1,6),8,2,facecolor='#c9e3e9'))
    for x,y in [(2,3),(4,3.4),(7,2.8),(3,4.8),(6,4.7),(8,4)]:ax[2].add_patch(Circle((x,y),.2,color='#8160a1'))
    ax[2].plot([1,9],[5.8,5.8],'--',color='#cd803f');ax[2].text(5,7,tr('已耗尽区域','Depleted region'),ha='center',fontsize=10);ax[2].text(5,1,tr('1961：Higuchi 的移动前沿思想','1961: Higuchi’s moving-front idea'),ha='center',fontsize=9);ax[2].set_title(tr('C  固体药物逐步溶出','C  Solid drug dissolves progressively'));fig.tight_layout();save(fig,'apparatus')
    rng=np.random.default_rng(404);time=np.array([.25,.5,1,2,4,8,12,24]);truth=100*(.2*(-np.expm1(-time/.25))+.8*(-np.expm1(-time/8)));raw=sampled_concentration(truth)
    standards=np.linspace(0,10,7);abs_std=.03+.012*standards+rng.normal(0,.0004,len(standards));slope,intercept=np.polyfit(standards,abs_std,1)
    absorbance=.03+.012*raw+rng.normal(0,.0007,len(raw));estimated=(absorbance-intercept)/slope;corrected=correct(estimated);naive=10*estimated;observed_removed=2*np.r_[0,np.cumsum(estimated[:-1])]
    np.savetxt(output/'release.csv',np.column_stack([time,truth,raw,absorbance,estimated,naive,observed_removed,corrected]),delimiter=',',header='time_h,true_cumulative_ug,true_bath_ug_ml,absorbance,estimated_ug_ml,bath_mass_ug,previously_removed_ug,corrected_cumulative_ug',comments='')
    np.savetxt(output/'calibration.csv',np.column_stack([standards,abs_std]),delimiter=',',header='concentration_ug_ml,absorbance',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.3));ax=ax.ravel();ax[0].scatter(standards,abs_std);ax[0].plot(standards,slope*standards+intercept);ax[0].set(xlabel=tr('浓度 / μg mL⁻¹','Concentration / μg mL⁻¹'),ylabel=tr('吸光度','Absorbance'),title=tr('A  同介质标准曲线','A  Matrix-matched calibration'))
    ax[1].plot(time,truth,color='#a4abad',ls='--',label=tr('构造真值','Constructed truth'));ax[1].plot(time,corrected,'o-',label=tr('累计取样校正','Sampling corrected'));ax[1].plot(time,naive,'s-',label=tr('只算当前溶液','Current bath only'));ax[1].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('药物质量 / μg','Drug mass / μg'),title=tr('B  校正把已取走的量加回来','B  Correction restores removed mass'));ax[1].legend(fontsize=8)
    x=np.arange(len(time));ax[2].bar(x,naive,label=tr('当前溶液','Current bath'));ax[2].bar(x,observed_removed,bottom=naive,label=tr('此前取样','Earlier samples'));ax[2].set(xticks=x,xticklabels=[f'{t:g}' for t in time],xlabel=tr('时间 / h','Time / h'),ylabel=tr('累计质量 / μg','Cumulative mass / μg'),title=tr('C  每个时间点的质量账本','C  Mass ledger at each time'));ax[2].legend(fontsize=8)
    for v in [0,1,2,4]:ax[3].plot(time,10*sampled_concentration(truth,aliquot=v),label=f'{v:g} mL')
    ax[3].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('未校正的当前质量 / μg','Uncorrected current mass / μg'),title=tr('D  同一释放过程，不同取样体积','D  Same release, different aliquots'));ax[3].legend(title=tr('每次取样','Sample volume'),fontsize=8);fig.tight_layout();save(fig,'sampling')
    tt=np.linspace(0,24,241);single=lambda t,tau:100*(-np.expm1(-t/tau));tau=float(curve_fit(single,time,corrected,p0=[5],bounds=(.01,100))[0][0]);pred=single(time,tau)
    fig,ax=plt.subplots(1,3,figsize=(12,4.2));ax[0].plot(time,corrected,'o',label=tr('构造数据','Constructed data'));ax[0].plot(tt,single(tt,tau),label=tr('单时间尺度拟合','Single-timescale fit'));ax[0].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('累计释放 / %','Cumulative release / %'),title=tr('A  拟合曲线','A  Fitted curve'));ax[0].legend(fontsize=8)
    ax[1].axhline(0,color='#a4abad');ax[1].plot(time,corrected-pred,'o-');ax[1].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('数据−拟合 / 百分点','Data − fit / percentage points'),title=tr('B  残差保留了早期快过程','B  Residuals reveal the early fast process'))
    for tau_m in [.5,2,8]:
        tau_c=4.;fraction=1-(tau_c*np.exp(-tt/tau_c)-tau_m*np.exp(-tt/tau_m))/(tau_c-tau_m);ax[2].plot(tt,100*fraction,label=f'{tau_m:g} h')
    ax[2].plot(tt,100*(-np.expm1(-tt/4)),color='#a4abad',ls='--',label=tr('载体自身','Carrier alone'));ax[2].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('外液累积量 / %','Cumulative outer-bath amount / %'),title=tr('C  透析膜增加第二道传质过程','C  Dialysis adds a transport step'));ax[2].legend(title=tr('膜过程时间尺度','Membrane timescale'),fontsize=8);fig.tight_layout();save(fig,'diagnostics')
    from PIL import Image
    fig,ax=plt.subplots(figsize=(11,4.6));ax.imshow(Image.open(Path(__file__).with_name('sheth2019-figure5.webp')));ax.axis('off');ax.set_title(tr('真实研究：独立测得扩散与厚度，再预测释放','Published study: measured diffusion and thickness predict release'),fontsize=12,pad=12);fig.text(.5,.015,'Sheth et al. (2019), Figure 5 · Frontiers in Bioengineering and Biotechnology · CC BY 4.0',ha='center',fontsize=8.5);save(fig,'published')
    worked=sampled_concentration([20,40,60]);wcorrect=correct(worked);summary={'worked_example':{'concentrations_ug_ml':worked.tolist(),'third_bath_mass_ug':float(10*worked[-1]),'third_removed_ug':float(2*sum(worked[:-1])),'third_corrected_ug':float(wcorrect[-1]),'release_percent':60,'loading_efficiency_percent':80,'loading_content_percent':8,'calibration_concentration_ug_ml':(.09-.03)/.012,'diluted_original_ug_ml':10},'calibration':{'slope':float(slope),'intercept':float(intercept)},'fit':{'single_tau_h':tau,'residual_rmse':float(np.sqrt(np.mean((corrected-pred)**2)))},'mass_balance':{'max_exact_error_ug':float(np.max(np.abs(correct(raw)-truth)))},'final':{'true_ug':float(truth[-1]),'corrected_ug':float(corrected[-1]),'naive_ug':float(naive[-1])}}
    assert abs(wcorrect[-1]-60)<1e-12;assert abs(10*worked[-1]-48.8)<1e-12;assert summary['mass_balance']['max_exact_error_ug']<1e-10
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

运行后先检查不加测量噪声的质量守恒：校正结果应恢复构造的累计量。然后改变每次取样体积，观察未校正曲线怎样变化；再改变标准曲线背景，观察整条轨迹受到什么影响。这种顺序把账本错误与仪器误差分开。对实际数据，可以沿用相同的列结构，将示例信号替换为自己的原始测量，并逐条保留载体编号和制备批次。若要估计参数差异，先对独立轨迹拟合，再根据实验设计汇总，便能把材料重复性与测量重复性放在合适层次。

一份有用的释放结果应能回答材料在何种外部环境中、以什么完整性和功能状态、在多长时间内交付了多少目标分子。累计量、速率、残留量、回收率和独立重复各自补充这一问题的一部分。接下来讨论扩散与渗透时，我们会把“分子离开载体”进一步拆成浓度差、材料厚度、界面分配和单位面积通量。这些量让释放曲线背后的空间过程变得可以测量，也帮助选择真正能区分机制的下一次实验。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Higuchi (1961). Rate of release of medicaments from ointment bases containing drugs in suspension](https://doi.org/10.1002/jps.2600501018)

   移动耗尽前沿与平方根时间关系的历史论文。
2. [Koizumi et al. (1975). Rate of Release of Medicaments from Ointment Bases Containing Drugs in Suspension](https://www.jstage.jst.go.jp/article/cpb1958/23/12/23_12_3288/_article)

   初始浓度、溶解度及边界条件对 Higuchi 近似的影响。
3. [FDA. Compilation of Guidance and Resources for in vitro Dissolution Testing](https://www.fda.gov/animal-veterinary/new-animal-drug-applications/compilation-fda-guidance-and-resources-in-vitro-dissolution-testing-immediate-release-solid-oral-dosage)

   取样体积、补液、介质、稳定性、过滤和分析验证的测量原则。

   Official technical reference; no assets reproduced.
4. [Sheth et al. (2019). Predicting Drug Release From Degradable Hydrogels Using Fluorescence Correlation Spectroscopy and Mathematical Modeling](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00410/full)

   实测扩散、凝胶厚度与蛋白释放的关联实验，以及 Figure 5。

   CC BY 4.0; Figure 5 reproduced with attribution.
5. [SciPy documentation: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   非线性最小二乘、参数边界及残差定义。
