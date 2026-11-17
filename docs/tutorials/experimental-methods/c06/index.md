# 表面等离子体共振：实时观察结合与解离

Source: https://ml-biomat.com/tutorials/experimental-methods/c06/
Language: zh-CN

从光学响应、参照和时间曲线，理解分子结合的亲和力、速度与输运。

## 结合得牢，和留得久，是同一回事吗？

设想要给一种血液检测装置挑选抗体。它的任务是在短短几分钟内抓住稀少的目标蛋白质，随后经受缓冲液冲洗，让已经结合的目标留在表面。另一种抗体的最终结合量也许完全相同，却需要更长时间才达到这个数量；还有一种抗体很快抓住目标，也很快放开。只测量一个长时间后的终点，容易把这些性格不同的分子放在同一栏里。表面等离子体共振，简称 SPR，把结合过程画成一条连续的时间曲线：目标分子流过表面时响应上升，换成不含目标的缓冲液后响应下降。上升与下降的速度，正是检测、筛选和材料表面设计中经常需要的信息。

这里的“表面”可以是一层固定了抗体的金膜，也可以是接有受体、核酸或特定化学基团的界面。固定的一方通常称为配体，随溶液流过的一方称为分析物；这是实验中的角色名称，同一种蛋白质交换固定方式后也可以交换角色。读曲线时，首先应当知道谁固定、谁流动、溶液中的浓度是多少。对生物材料而言，这种角色区别尤其有用：研究血浆蛋白在材料表面的吸附，和研究一种纯化蛋白质与固定受体的特异结合，虽然都能出现上升曲线，却对应不同的表面组成和解释问题。

可以先把结合想成一间有固定座位的阅览室。门外的人越多，空座被占据的机会越大；已经坐下的人也会离开。房间最终坐满多少人，取决于进入与离开两种过程的平衡，而不仅是人们离开得慢不慢。若进入和离开同时加快十倍，最后的占座比例可以不变，达到这个比例以及清空房间所需的时间却会显著改变。这个类比帮助我们分清亲和力与动力学：亲和力描述给定浓度下的平衡偏好，动力学描述接近或离开这种状态的速度。后面的实验和交互会用同一个解离常数，画出两种很不一样的时间过程。

SPR 的直接读数来自近表面光学环境的改变。要把它解释为分子结合，需要把光学读数、表面化学和溶液输运连接起来。本节将沿着一组构造的传感曲线，依次看到原始信号中的溶剂阶跃，参照扣除后剩下的扰动，多浓度拟合得到的速率，以及表面附近“供货不及时”时产生的偏差。这样，亲和力不再只是软件结果表中的一个数字，而是有相应实验条件和曲线形状支持的量。

## 从金属薄膜上的光，到分子结合的时间记录

光照到金属，并不只有普通镜面反射这一种结果。在合适的金属薄膜、入射角和偏振条件下，光能够通过棱镜耦合，激发表面附近电子的集体振荡。与这类表面振荡耦合时，反射光强在特定角度附近出现一个低谷。低谷的位置与金属两侧的光学条件有关，尤其对金属外侧很近的一小层溶液和附着物敏感。分子结合到表面后，近表面的折射率发生变化，共振位置随之移动。仪器连续跟踪这种变化，就能把看不见的分子积累转换成可记录的响应。

1983 年，Liedberg、Nylander 和 Lundström 在薄金属膜的表面等离子体共振实验中展示了气体检测与生物传感，并研究了免疫球蛋白层和抗体的相互作用。论文中的生物实验已经包含了后来传感研究很熟悉的思想：改变溶液浓度，比较随时间变化的响应，再用不同抗体考察结合选择性。这里值得注意的历史转折，是把光学界面对环境的敏感性变成观察生物分子相互作用的工具。现代仪器进一步把受控流路、稳定温度、自动进样和数据分析结合起来，使这种连续观察更容易重复。

图中的棱镜、金属膜和分子层是解释这一原理的原创示意。右侧两条共振谷也是概念轮廓，用来帮助读者理解位置变化，并没有把它们当作某一次历史实验的角谱。实际仪器可能跟踪角度、波长或其他相关光学量，并将变化转换为响应单位 RU。RU 是仪器响应的表达方式；将它进一步转换为表面质量，需要相应传感器、光学条件和折射率增量的关系。蛋白质和其他物质的光学响应并不总能用一个通用质量换算因子替代。

![原创棱镜耦合与金属膜示意，联系 1983 年的 SPR 生物传感实验；尺寸不按比例。右图为概念性的共振谷位置变化，不是实测角谱或完整电磁场计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e7cb036bd28dfbe4c17d1d8b.svg?v=e7cb036bd28d)

图 1原创棱镜耦合与金属膜示意，联系 1983 年的 SPR 生物传感实验；尺寸不按比例。右图为概念性的共振谷位置变化，不是实测角谱或完整电磁场计算。

折射率也解释了为什么一种看起来“直接观察结合”的技术仍然需要参照。分析物溶液中的盐、甘油或二甲基亚砜含量稍有变化，流过传感表面时也会改变光学环境。温度漂移、非特异吸附和表面水合状态改变，同样可能影响响应。把这些因素放回测量定义，读曲线就会更具体：尖锐的进样阶跃可能来自溶液整体折射率差，而逐渐积累并在冲洗后保留的部分更值得结合对照进一步分析。响应向上并不会自动告诉我们，究竟是哪一种分子过程贡献了它。

流动池把分析物送到表面，却不会让所有分子同时到达同一个位置。紧贴表面的一层液体与主体流动之间存在传递过程，分子还要靠扩散穿过局部浓度变化区域。表面结合太快、位点过密或交换太慢时，表面附近的游离浓度就可能低于注射液的标称浓度。于是光学、化学和输运三部分已经同时在曲线上相遇：仪器读到的是近表面的变化，分子是否结合取决于可接近的位点，而位点周围有多少可结合分子又取决于输运。

## 把上升和下降写成可理解的速率

先从最容易解释的情形开始：表面位点相同且独立，一个分析物结合一个位点，表面附近的游离浓度等于设定浓度，响应与结合量成正比。若表面还有很多空位，分析物就有较多结合机会；随着空位减少，新结合的速度逐渐降低。同时，每一刻都有一部分已结合分子解离。净增长速度等于新结合速度减去离开速度。这种“流入减流出”的守恒思想，比直接记住曲线公式更重要，因为后面检查模型是否适合实验，正是检查这两项是否真的描述了过程。

$$
\frac{dR}{dt}=k_{\mathrm{on}}C(R_{\max}-R)-k_{\mathrm{off}}R
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 结合响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | 结合速率常数，L/(mol·s)，即 M⁻¹s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 近表面游离分析物浓度，在本模型中等于设定浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/005e161a184834c885d95173.svg) | 全部有效位点占据时的分析物响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 解离速率常数，s⁻¹。 |

相同独立位点、一对一结合、响应与结合量成正比且局部供给及时。空位项控制新结合，已结合项控制离开。kₒₙ=2×10⁵、C=10⁻⁸ mol/L、Rmax=120 RU，初始 R=0 时增长为 0.24 RU/s。

结合速率常数的单位同时包含浓度的倒数与时间的倒数，是因为分析物浓度加倍时，每个空位遇到分析物的机会也随之增加。解离速率常数只含时间的倒数，因为在这个模型里，某个已结合分子离开的概率由自身所处的结合状态决定。取结合速率常数每摩尔每秒二十万，解离速率常数每秒 0.002，分析物浓度 10 nM，最大响应 120 RU。刚开始全部空位可用，新结合使响应以每秒 0.24 RU 的速度增加；已结合量为零，因此这一刻没有解离损失。响应增加以后，两个方向开始同时贡献。

$$
K_D=\frac{k_{\mathrm{off}}}{k_{\mathrm{on}}},\quad R_{\mathrm{eq}}=\frac{R_{\max}C}{K_D+C},\quad k_{\mathrm{obs}}=k_{\mathrm{on}}C+k_{\mathrm{off}},\quad R(t)=R_{\mathrm{eq}}(1-e^{-k_{\mathrm{obs}}t})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a443778a30c5870335c56f4d.svg) | 平衡解离常数，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 解离速率常数，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | 结合速率常数，L/(mol·s)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98fcf8602db40c1c0cc09549.svg) | 给定浓度的平衡结合响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/005e161a184834c885d95173.svg) | 全部有效位点占据时的分析物响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 恒定游离分析物浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/557e93507479e84f43d62190.svg) | 接近平衡的表观速率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a187b42ecc9ef443adcbc568.svg) | 从空表面开始结合后 t 时刻响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 自进样开始的时间，s。 |

令净速率为零得到平衡响应，再求解恒定浓度下的一阶速率方程。kₒₙ=2×10⁵、kₒff=0.002，Kᴅ=10 nM；C=10 nM、Rmax=120，Req=60 RU，kobs=0.004 s⁻¹，180 s 时 R≈30.795 RU。

平衡不是分子停止移动，而是结合与解离平均相抵。上面的参数给出 10 nM 的解离常数；分析物浓度也为 10 nM 时，一半位点被占据，所以平衡响应为 60 RU。到达平衡需要时间。在这组条件下，接近平衡的速率为每秒 0.004，相应时间尺度为 250 s；只进样 180 s，响应约为 30.79 RU，离 60 RU 还有明显距离。看到曲线在进样结束时达到最高点，容易误以为它已经饱和，实际上这个最高点可能只是人为切换溶液造成的截断。

换成不含分析物的缓冲液后，如果表面附近的游离分析物被及时带走，新结合项消失，剩下已结合分子的解离。每个短时间间隔离开的都是现有结合量的一部分，因此下降呈指数形，而不是每秒减少相同的 RU。半衰期是结合量下降到起点一半所需的时间；它不依赖起点响应高低，却依赖解离速率。这个量对需要经历冲洗的捕获实验很直观，也能解释为什么相同平衡亲和力的候选分子在实际检测流程中表现不同。

$$
R(\tau)=R_0e^{-k_{\mathrm{off}}\tau},\qquad t_{1/2}=\frac{\ln 2}{k_{\mathrm{off}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93f17ccb2498eb79f09caaf2.svg) | 冲洗开始后 τ 时刻的结合响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31e316fb976f1ca84f57e4cb.svg) | 冲洗起点的结合响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 冲洗开始后的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 解离速率常数，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | 结合响应降为冲洗起点一半所需时间，s。 |

近表面游离分析物及时清除且没有再结合时，只有一阶解离损失。kₒff=0.002 s⁻¹，半衰期约 346.574 s；420 s 后保留 exp(−0.84)=0.431711。速率增至 0.02 s⁻¹，半衰期变为 34.657 s。

在本例中，解离半衰期约 346.6 s。把两个速率常数都乘以十，解离常数仍为 10 nM，但半衰期缩短为约 34.7 s，结合阶段也更快接近平衡。后面的交互把亲和力、共同速率倍率和分析物浓度分开控制。先保持亲和力和浓度不变，只移动速率倍率，可以直接看见平衡虚线不动、时间曲线却发生变化。再改变浓度，就会同时改变平衡占据和接近平衡的速度，这正是设计多浓度实验时需要利用的信息。

## 相同亲和力，不同的时间过程

一对一独立位点模型，容量 120 RU；进样 180 s 后换为分析物浓度为零的缓冲液。保持 Kᴅ 和浓度不变，只改变速率倍率，比较时间曲线与平衡虚线。

[Figure: 动力学时间曲线与平衡响应](https://ml-biomat.com/tutorials/experimental-methods/c06/#C06-plot)

## 曲线质量从表面和样品开始

固定配体时，目标是让分析物能够接近有效位点，并让这种表面在整组实验中保持稳定。将蛋白质共价接到传感层、通过标签捕获或用其他亲和方式固定，会形成不同的取向与距离。若关键结合面贴在表面上，即使固定了很多蛋白质，可用位点也可能很少。多价分析物还可能同时接触相邻配体，产生多点结合；这时解离过程会受到重新抓住邻近位点的影响。选择较低的表面装载量，通常有助于观察较接近单次分子相互作用的过程，同时也要保留足够的信号。

配体固定时的响应和后续分析物可达到的最大结合响应，是两种不同读数。前者对应已经装上表面的配体层，后者还取决于分析物分子质量、结合计量关系、可用位点比例及光学响应特性。把固定响应直接当成分析物的最大响应，会让拟合从一开始就使用错误尺度。实际分析可以把最大响应作为共享参数估计，再检查它是否与表面设计相符。若不同浓度只能靠大幅改变最大响应才能拟合，应当回头检查表面活性、样品状态或相互作用模型。

样品准备首先要保持分析物浓度的含义清楚。总蛋白质浓度与有结合活性的单体浓度可能不同；聚集体既改变有效浓度，也可能引入多价结合。运行缓冲液与样品缓冲液应尽量匹配，尤其是会显著改变折射率的有机溶剂组分。对小分子筛选，二甲基亚砜含量的微小差别就值得进行专门的溶剂校正。稀释系列最好覆盖预计解离常数附近，并包含较低与较高浓度，使曲线同时提供上升速度、平衡趋势和容量信息。

参照表面应尽量保留与活性表面相近的基底、连接化学和非特异吸附条件，只去掉要研究的特异结合因素。空白基底很容易准备，却未必能复制一层固定蛋白质对其他分子的吸附。若使用无关蛋白质作为参照，还要考虑其电荷、表面密度和稳定性。参照是对实验中某类贡献的匹配测量，匹配得越好，相减后的量越接近研究问题。空白进样周期则通过注入运行缓冲液，记录重复出现的阀切换、液路和表面扰动。

注射时间、冲洗时间和循环顺序同样属于实验设计。解离很慢时，过短的观察窗只能看到接近水平的一小段下降，难以稳定估计斜率；结合很快时，初始几秒的混合与输送过程可能占据主要变化。重复中间浓度、穿插空白周期，有助于发现表面逐步失活或基线漂移。若每轮需要再生表面，应确认再生能释放前一轮分析物，同时保留配体活性。把传感曲线按实验顺序一起查看，常常比只查看最后一张拟合参数表更早发现问题。

## 从四条原始记录，到一组共享参数

本章完整例子构造了五种分析物浓度，从 1 nM 到 100 nM，记录 180 s 结合和 420 s 冲洗。每种浓度都保留活性表面、参照表面、空白周期活性表面和空白周期参照表面的原始记录。活性表面除了真实结合，还包含进样时 12 RU 的溶剂阶跃、缓慢漂移和短暂注射扰动。参照通道拥有相同的溶剂阶跃与漂移，但这里特意留下一个活性表面独有且能在空白周期重复出现的短暂扰动，用来展示为什么一次相减还不够。

$$
R_{\mathrm{corr}}=(R_{\mathrm{active}}-R_{\mathrm{ref}})_{\mathrm{sample}}-(R_{\mathrm{active}}-R_{\mathrm{ref}})_{\mathrm{blank}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f3aa7cba0902d6a924f22a23.svg) | 双参照校正后的响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/583d6435926c509afd302f04.svg) | 活性表面通道响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f556b6dcf070fc7983979795.svg) | 参照表面通道响应，RU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea4973df6ab1d58c52662533.svg) | 含分析物的样品注射周期，下标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4e1cf44e3abaae399d3584a3.svg) | 匹配空白注射周期，下标。 |

各记录按相同注射时间对齐，参照匹配体相贡献，空白匹配重复扰动，之后扣进样前均值。某时刻活性 45、参照 13、空白活性 2、空白参照 1 RU，双参照结果为 31 RU。四条独立通道各有 0.2 RU 噪声标准差，合成后约 0.4 RU。

第一步用样品的活性通道减去参照通道，消去共同的溶剂和漂移贡献；第二步再减去空白周期中的通道差，去掉重复的注射扰动；最后用进样前的平均值把基线设为零。图中初始几十秒的放大窗口把这些步骤放在同一个尺度上。这里的设计也让噪声传播看得很清楚：每条原始记录的独立噪声标准差为 0.2 RU，四条记录带正负号相加后，标准差约为 0.4 RU。校正减少了系统偏差，却不会凭空增加测量精度，因此对照本身也要有足够稳定的读数。

![构造数据，随机种子 660。五种浓度共享内在速率和 120 RU 容量。A 保留溶剂阶跃，B 比较双参照校正前后偏差，C 为校正记录及全局拟合，D 为数据减模型。每个原始通道噪声标准差 0.2 RU。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7285fa52b1f64ea0872c038e.svg?v=7285fa52b1f6)

图 2构造数据，随机种子 660。五种浓度共享内在速率和 120 RU 容量。A 保留溶剂阶跃，B 比较双参照校正前后偏差，C 为校正记录及全局拟合，D 为数据减模型。每个原始通道噪声标准差 0.2 RU。

基线归零还有一个统计上的影响。进样前均值由有限个带噪声的读数估计而来，把它从整条记录中减去，会让同一周期中的各点共同受到这个估计量的影响。因此，时间点很多并不等于进行了同样多次独立实验。重复注射可以检查周期重复性，独立制备表面可以检查固定过程的差异，独立准备样品又对应另一类变异。比较不同候选时，把重复层面的参数结果与拟合曲线一起保留，便能同时看见平均行为和重复性，而不是只留下一个过于精细的小数。

随后把五条校正曲线放进同一个拟合中，让它们共享结合速率、解离速率和最大响应。这样做的理由来自实验设计：同一种表面、同一种分析物和相同温度缓冲条件下，改变的是分析物浓度，而不是每次都产生一套新的分子性质。全局拟合得到的结合速率约为每摩尔每秒 201179，解离速率约为每秒 0.0019996，解离常数约为 9.94 nM，最大响应约为 119.78 RU。它们接近构造数据时设定的数值；这项比较检验的是所示计算过程在已知模型数据上的恢复能力。

拟合之后应当读残差，也就是数据减去模型。残差若在整个结合阶段都呈弯曲结构，说明模型遗漏了有方向性的变化；若只在注射切换处出现尖峰，可能需要检查输送延迟和体相校正；若高浓度曲线总是偏离，而低浓度相对吻合，传质、非特异吸附或浓度相关聚集值得分别检查。本例的残差均方根约为 0.401 RU，与四通道独立噪声的预期尺度相近。这里的残差并不是亲和力的误差条，它描述的是响应空间中的拟合差异。

还可以故意采用一个容易发生的错误：直接取每条曲线在 180 s 的响应，把它们当成已经达到平衡的终点。对于这组数据，允许最大响应同时变化时，会得到约 35.16 nM 的解离常数和约 145.37 RU 的最大响应；将容量固定在真实的 120 RU 时，也得到约 22.96 nM 的解离常数。偏差的方向由数据覆盖和模型约束共同决定。本例最有价值的观察是，平滑的终点拟合曲线仍能对应错误参数。是否达到平衡，必须从原始时间过程判断。

![构造模型。A 两组速率之比相同，Kᴅ=10 nM，但时间过程不同；虚线为 60 RU 平衡响应。B 展示将 180 s 端点误作平衡得到的偏差，端点模型同时拟合 Kᴅ 与容量。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b28a48a60f09e6d9d449c859.svg?v=b28a48a60f09)

图 3构造模型。A 两组速率之比相同，Kᴅ=10 nM，但时间过程不同；虚线为 60 RU 平衡响应。B 展示将 180 s 端点误作平衡得到的偏差，端点模型同时拟合 Kᴅ 与容量。

## 表面附近的浓度，为什么可能与注射液不同

现在回到阅览室，但把入口改成一条狭窄通道。门外即使有很多人，空座也不一定能立刻接到足够的人。SPR 中的相似情形是传质限制：分析物到达近表面的速度跟不上结合消耗，局部游离浓度下降。若仍把注射液浓度直接代入最简单的结合模型，曲线变慢就可能被误读为分子结合速率较小。增加流动交换、降低表面位点密度，分别改变供给和消耗；比较这些条件下的曲线，能够帮助区分输运与内在结合过程。

本例把溶液简化为主体区域和近表面区域。主体浓度在进样时为 30 nM，冲洗时变为零；近表面浓度由交换、结合消耗和解离释放共同决定。用位点占据比例描述表面，就能把分子结合和物质守恒写在同一组方程里。等效位点浓度把“表面有多少位点”换算成近表面这小块体积中的浓度尺度；它越大，同样比例的占据变化就消耗越多游离分析物。这个参数是模型定义，和直接读出的表面 RU 并不是同一个量。

$$
\frac{d\theta}{dt}=k_{\mathrm{on}}C_s(1-\theta)-k_{\mathrm{off}}\theta,\qquad \frac{dC_s}{dt}=k_{\mathrm{tr}}(C_b-C_s)-\Gamma\frac{d\theta}{dt}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 被占据位点比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | 内在结合速率常数，L/(mol·s)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 内在解离速率常数，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | 近表面区域的游离分析物浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a2c7455873446449e6636a4.svg) | 主体溶液分析物浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0403bdc848dfd0bb7d52ccc7.svg) | 本两区域模型的交换速率，s⁻¹，不是体积流量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | 以近表面区域体积换算的总位点浓度，mol/L。 |

第二式按物质守恒，把交换供给与结合消耗相减；解离时占据变化为负，向局部溶液释放分析物。Cb=30 nM、Cs=0、ktr=0.005 s⁻¹，初始交换供给为 0.15 nM/s。Γ=200 nM、θ 增加 0.01，将消耗 2 nM 局部游离分析物。

图中比较高容量慢交换、高容量快交换和低容量慢交换三种条件。三个模型使用相同的内在结合与解离速率，只改变交换速度或等效位点浓度。高容量慢交换时，180 s 末的近表面游离浓度约为 4.40 nM，远低于主体的 30 nM，表面占据上升受到供应限制。降低容量后，消耗对局部浓度的影响减小；加快交换则让近表面更及时地跟随主体浓度。这种比较也说明，较大的原始响应并不天然意味着更适合测量动力学的表面。

![两区域构造模型，内在速率保持不变。容量分别为 200 或 2 nM 等效位点浓度，交换速率为 0.005 或 0.5 s⁻¹。A 用占据比例比较，C 除以各曲线冲洗起点占据量；慢交换时局部残留分析物可继续结合。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c2a0e75ecf35e7de69664d33.svg?v=c2a0e75ecf35)

图 4两区域构造模型，内在速率保持不变。容量分别为 200 或 2 nM 等效位点浓度，交换速率为 0.005 或 0.5 s⁻¹。A 用占据比例比较，C 除以各曲线冲洗起点占据量；慢交换时局部残留分析物可继续结合。

冲洗开始时，主体浓度变成零，近表面的小区域却不会瞬间清空。已经离开位点的分析物，也可能在被带走之前再次结合。慢交换高容量模型在切换后甚至还能暂时继续增加占据；经过 420 s，其占据量约为冲洗起点的 1.040 倍。这个超过一的比例来自局部残留分析物和再结合，不是生成了额外分子。对照之下，及时清除游离分析物的单指数模型在同样时间只保留约 0.432。若只看缓慢下降或短暂上升而忽略传递过程，就容易把表观停留时间解释得过长。

双价或多价结合与传质再结合可以同时出现，但它们需要不同的实验比较。前者涉及一个分析物与多个位点的连接关系，后者涉及已经游离的分子在局部溶液中的去留。改变配体密度、比较单价片段、改变流动条件和延长观察时间，分别为这些机制提供信息。增加模型参数可以让曲线更贴近数据，却不会自动确定微观机制；更有力的解释来自某个可检验的机制预期，在相应实验改变后确实出现。这样，模型选择就成为实验推理的一部分。

## 完整重建一次分析，并把结果用于下一步实验

下面的程序保留从原始四通道记录到参数表的完整路径。运行后会输出每种浓度的时间、原始响应、校正响应和拟合值，还会保存传质模型中的占据比例与近表面浓度。图中的光学轮廓和传感数据都是明确构造的教学例子，随机种子固定，因此同一环境下能够重复比较处理步骤。数值积分负责计算两区域模型，最小二乘拟合负责寻找能够同时解释多浓度记录的参数；两者分别解决“给定参数会出现什么曲线”和“什么参数能解释这些曲线”。

读代码时可以先跟踪一个 10 nM 周期：找到活性通道中的溶剂阶跃，逐次相减，再检查 180 s 的响应为什么只有约 30.79 RU。随后把结合和解离速率一起乘十，观察平衡响应保持 60 RU，而半衰期缩短十倍。最后查看传质文件中的近表面浓度，理解为什么冲洗后仍可能有新的结合。三次操作分别对应光学校正、动力学与平衡的区分、以及输运和化学的区分，能够把同一张传感图拆成有明确物理意义的部分。

### 完整 SPR 双参照、动力学拟合与传质比较

构造并保留四通道记录，完成全局拟合与端点误读比较，再积分两区域传质模型。输出原始数组、逐浓度 CSV、参数和全部图形。

```
"""Constructed SPR sensorgrams, double referencing and kinetic/transport diagnostics."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares,curve_fit
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle

def response(t,concentration,kon=2e5,koff=.002,capacity=120.,contact=180.):
 t=np.asarray(t);c=concentration*1e-9;rate=kon*c+koff;equilibrium=capacity*kon*c/rate
 assoc=equilibrium*(-np.expm1(-rate*np.maximum(t,0)));end=equilibrium*(-np.expm1(-rate*contact))
 return np.where(t<0,0,np.where(t<=contact,assoc,end*np.exp(-koff*np.maximum(t-contact,0))))

def transport(exchange,site_equivalent,concentration=30.,contact=180.,stop=600.):
 """exchange: s^-1; site_equivalent: mol/L of near-surface compartment."""
 def rhs(bulk):
  def f(t,y):
   theta,cs=y;binding=2e5*cs*(1-theta)-.002*theta
   return [binding,exchange*(bulk-cs)-site_equivalent*binding]
  return f
 a=solve_ivp(rhs(concentration*1e-9),(0,contact),[0,0],t_eval=np.arange(contact+1),rtol=1e-9,atol=[1e-11,1e-16])
 b=solve_ivp(rhs(0),(contact,stop),a.y[:,-1],t_eval=np.arange(contact,stop+1),rtol=1e-9,atol=[1e-11,1e-16])
 return np.r_[a.t,b.t[1:]],np.c_[a.y,b.y[:,1:]]

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);T=lambda z,e:z if a.language=='zh' else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35';cols=[B,G,Y,R,'#775f91']
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 rng=np.random.default_rng(660);t=np.arange(-30,601,dtype=float);cs=np.array([1,3,10,30,100.]);binding=np.array([response(t,c) for c in cs]);on=(t>=0)&(t<180);bulk=12*on;drift=.5+.005*(t+30)
 artifact=np.where(t>=0,1.5*np.exp(-np.maximum(t,0)/8),0)-np.where(t>=180,1.2*np.exp(-np.maximum(t-180,0)/8),0)
 active=binding+bulk+drift+artifact+rng.normal(0,.2,binding.shape);reference=np.broadcast_to(bulk+drift,binding.shape)+rng.normal(0,.2,binding.shape)
 blankactive=np.broadcast_to(drift+artifact,binding.shape)+rng.normal(0,.2,binding.shape);blankref=np.broadcast_to(drift,binding.shape)+rng.normal(0,.2,binding.shape)
 single=active-reference;corrected=single-(blankactive-blankref);corrected-=corrected[:,t<0].mean(axis=1,keepdims=True)
 def residual(p):return (np.array([response(t,c,*np.exp(p)) for c in cs])-corrected).ravel()
 fitted=least_squares(residual,np.log([2e5,.002,120]),bounds=(np.log([1e3,1e-5,10]),np.log([1e8,1,1000])),xtol=1e-12,ftol=1e-12,gtol=1e-12)
 kon,koff,cap=np.exp(fitted.x);prediction=np.array([response(t,c,kon,koff,cap) for c in cs]);kd=koff/kon*1e9
 endpoint=binding[:,t==180].ravel();eqfun=lambda c,k,r:r*c/(k+c);wrong,_=curve_fit(eqfun,cs,endpoint,p0=[20,130],bounds=(0,np.inf));earlyfixed,_=curve_fit(lambda c,k:eqfun(c,k,120),cs,endpoint,p0=[20],bounds=(0,np.inf))
 # Optical curves below are conceptual Lorentzian sketches, not Maxwell solutions.
 f,axes=plt.subplots(1,2,figsize=(13.5,5.5),layout='constrained');ax=axes[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(T('A  1983：薄金属膜把结合变成光学变化','A  1983: Thin metal films turn binding into an optical change'),loc='left')
 ax.add_patch(Polygon([[1,4.5],[9,4.5],[5,.8]],fc='#dce9ed',ec=B));ax.add_patch(Rectangle((1,4.5),8,.2,fc=Y));ax.add_patch(Rectangle((1,4.7),8,2,fc='#e6f0ee',ec=G));ax.annotate('',xy=(8.5,6.3),xytext=(1.5,6.3),arrowprops={'arrowstyle':'->','color':G,'lw':2});ax.text(5,7.1,T('溶液流动；表面附近折射率改变','Flowing solution; refractive index changes near the surface'),ha='center',fontsize=10)
 for x in [2,3.5,5,6.5,8]:
  ax.plot([x,x],[4.7,5.1],c=B,lw=2);ax.add_patch(Circle((x,5.3),.22,fc=B))
 for x in [3.5,6.5]:ax.add_patch(Circle((x,5.67),.18,fc=R))
 ax.annotate('',xy=(5,4.5),xytext=(2,1.7),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.annotate('',xy=(8,1.7),xytext=(5,4.5),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.plot([5,5],[2.5,4.5],ls=':',c='#657785');ax.text(2,1.1,T('入射光','Incident light'),ha='center');ax.text(8,1.1,T('反射光','Reflected light'),ha='center');ax.text(5,.05,T('棱镜耦合原理图；尺寸不按比例','Prism-coupling principle; not to scale'),ha='center',fontsize=10)
 ax=axes[1];angle=np.linspace(69.5,71,500)
 for center,c,l in [(70.2,B,T('结合前','Before binding')),(70.35,R,T('近表面环境变化后','After near-surface change'))]:ax.plot(angle,1-.75*.12**2/((angle-center)**2+.12**2),c=c,label=l)
 ax.annotate('',xy=(70.35,.2),xytext=(70.2,.2),arrowprops={'arrowstyle':'->','color':G,'lw':2});ax.set(xlabel=T('入射角 / degree','Incidence angle / degree'),ylabel=T('相对反射强度','Relative reflected intensity'),title=T('B  共振谷的位置移动','B  The resonance minimum shifts'),ylim=(.1,1.05));ax.legend(fontsize=9);ax.text(.04,.025,T('示意轮廓；非实测角谱','Conceptual profiles; not measured angle spectra'),transform=ax.transAxes,fontsize=9)
 save(f,'optics-history')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.3),layout='constrained');j=2;ax=axes[0,0];ax.plot(t,active[j],c=B,label=T('活性表面','Active surface'));ax.plot(t,reference[j],c=Y,label=T('参照表面','Reference surface'));ax.plot(t,binding[j],c=R,ls='--',label=T('构造结合真值','Constructed binding truth'));ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('响应 / RU','Response / RU'),title=T('A  10 nM：结合与溶剂阶跃叠在一起','A  10 nM: Binding plus solvent steps'));ax.legend(fontsize=9)
 ax=axes[0,1];sl=(t>=-10)&(t<=45);ax.plot(t[sl],single[j,sl]-binding[j,sl],c=Y,label=T('参照相减后 − 真值','Reference-subtracted minus truth'));ax.plot(t[sl],corrected[j,sl]-binding[j,sl],c=B,label=T('再扣空白后 − 真值','Double-referenced minus truth'));ax.axhline(0,c='#647681',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('剩余偏差 / RU','Remaining deviation / RU'),title=T('B  空白周期去除重复进样扰动','B  Blank cycles remove repeatable injection artifacts'));ax.legend(fontsize=9)
 ax=axes[1,0]
 for i,c in enumerate(cs):ax.plot(t,corrected[i],c=cols[i],lw=.7,alpha=.65,label=f'{c:g} nM');ax.plot(t,prediction[i],c=cols[i],lw=1.4)
 ax.axvline(180,c='#647681',ls='--',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('双参照校正响应 / RU','Double-referenced response / RU'),title=T('C  多浓度共享一组动力学参数','C  Concentrations share kinetic parameters'));ax.legend(ncol=2,fontsize=9)
 ax=axes[1,1]
 for i,c in enumerate(cs):ax.plot(t,corrected[i]-prediction[i],c=cols[i],lw=.55,alpha=.55)
 ax.axhline(0,c='#647681',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('数据 − 模型 / RU','Data − model / RU'),title=T('D  从残差检查遗漏的时间结构','D  Inspect residuals for missing time structure'))
 save(f,'reference-kinetics')
 f,axes=plt.subplots(1,2,figsize=(13.6,5.5),layout='constrained');ax=axes[0]
 for rate,c in [(1,B),(10,R)]:ax.plot(t,response(t,10,2e5*rate,.002*rate),c=c,label=T(f'速率 ×{rate}',f'Rates ×{rate}'))
 ax.axhline(60,c='#647681',ls=':',label=T('平衡响应 60 RU','Equilibrium: 60 RU'));ax.axvline(180,c='#647681',ls='--');ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('结合响应 / RU','Binding response / RU'),title=T('A  同为 Kᴅ=10 nM，不同的到达与离开','A  Both Kᴅ=10 nM, different arrival and departure'));ax.legend(fontsize=9)
 ax=axes[1];grid=np.geomspace(.3,300,200);ax.semilogx(grid,eqfun(grid,10,120),c=B,label=T('真正的平衡关系','True equilibrium'));ax.scatter(cs,endpoint,c=R,label=T('180 s 时的端点','Endpoints at 180 s'));ax.semilogx(grid,eqfun(grid,*wrong),c=R,ls='--',label=T('将端点误作平衡拟合','Premature equilibrium fit'));ax.set(xlabel=T('分析物浓度 / nM','Analyte concentration / nM'),ylabel=T('响应 / RU','Response / RU'),title=T('B  停止进样不等于达到平衡','B  Injection end is not equilibrium'));ax.legend(fontsize=9);ax.text(.04,.53,T(f'端点拟合 Kᴅ = {wrong[0]:.1f} nM\nRmax = {wrong[1]:.1f} RU',f'Endpoint fit Kᴅ = {wrong[0]:.1f} nM\nRmax = {wrong[1]:.1f} RU'),transform=ax.transAxes,fontsize=10)
 save(f,'affinity-versus-time')
 cases=[(.005,2e-7,R,T('高容量，慢交换','High capacity, slow exchange')),(.5,2e-7,B,T('高容量，快交换','High capacity, fast exchange')),(.005,2e-9,G,T('低容量，慢交换','Low capacity, slow exchange'))];traces=[];f,axes=plt.subplots(2,2,figsize=(13.6,8.1),layout='constrained')
 for k,g,c,l in cases:
  tt,yy=transport(k,g);traces.append((tt,yy));axes[0,0].plot(tt,yy[0],c=c,label=l);axes[0,1].plot(tt,yy[1]*1e9,c=c);axes[1,0].semilogy(tt[180:]-180,yy[0,180:]/yy[0,180],c=c)
 for ax in axes[0]:ax.axvline(180,c='#647681',ls='--',lw=1);ax.set_xlabel(T('时间 / s','Time / s'))
 axes[0,0].set(ylabel=T('位点占据比例','Fraction occupied'),title=T('A  固定内在速率，改变运输条件','A  Same intrinsic rates, different transport'));axes[0,0].legend(fontsize=9)
 axes[0,1].plot([0,180,180,600],[30,30,0,0],c='#647681',ls=':',label=T('主体溶液','Bulk solution'));axes[0,1].set(ylabel=T('近表面游离浓度 / nM','Near-surface free concentration / nM'),title=T('B  消耗与释放改变近表面浓度','B  Uptake and release alter local concentration'));axes[0,1].legend(fontsize=9)
 axes[1,0].plot(np.arange(421),np.exp(-.002*np.arange(421)),c='#647681',ls='--',label=T('没有再结合的指数解离','Exponential decay without rebinding'));axes[1,0].set(xlabel=T('洗脱开始后时间 / s','Time after wash begins / s'),ylabel=T('相对于洗脱起点的占据','Occupancy relative to start of wash'),title=T('C  邻近分析物再结合会拖慢下降','C  Rebinding slows the apparent decay'));axes[1,0].legend(fontsize=8)
 ax=axes[1,1];ax.axis('off');ax.set(xlim=(0,10),ylim=(0,7));ax.add_patch(Rectangle((1,4.4),8,1.5,fc='#deebe6',ec=G));ax.add_patch(Rectangle((1,2.2),8,1.5,fc='#dce9ee',ec=B));ax.text(5,5.15,T('主体浓度 Cb：进样 30 nM，洗脱 0','Bulk Cb: 30 nM during injection, 0 during wash'),ha='center',fontsize=10);ax.text(5,2.95,T('近表面浓度 Cs：运输与结合共同决定','Near-surface Cs: exchange plus binding'),ha='center',fontsize=10);ax.annotate('',xy=(5,4.35),xytext=(5,3.75),arrowprops={'arrowstyle':'<->','color':R,'lw':2});ax.text(5,.6,T('容量：200 或 2 nM 的等效位点浓度\n交换速率：0.005 或 0.5 s⁻¹；非直接流速','Capacity: 200 or 2 nM equivalent sites\nExchange: 0.005 or 0.5 s⁻¹; not a direct flow rate'),ha='center',fontsize=10);ax.set_title(T('D  两区域教学模型','D  Two-compartment teaching model'),loc='left')
 save(f,'transport-rebinding')
 np.savez_compressed(a.output/'constructed_sensorgrams.npz',time_s=t,concentration_nM=cs,binding_truth_RU=binding,active_RU=active,reference_RU=reference,blank_active_RU=blankactive,blank_reference_RU=blankref,corrected_RU=corrected,fitted_RU=prediction)
 for i,c in enumerate(cs):np.savetxt(a.output/f'sensorgram_{c:g}nM.csv',np.c_[t,active[i],reference[i],blankactive[i],blankref[i],corrected[i],prediction[i]],delimiter=',',header='time_s,active_RU,reference_RU,blank_active_RU,blank_reference_RU,corrected_RU,fitted_RU',comments='')
 np.savetxt(a.output/'transport.csv',np.c_[traces[0][0],*[arr for tt,yy in traces for arr in [yy[0],yy[1]*1e9]]],delimiter=',',header='time_s,high_slow_theta,high_slow_Cs_nM,high_fast_theta,high_fast_Cs_nM,low_slow_theta,low_slow_Cs_nM',comments='')
 summary={'fitted_kon_M_inv_s_inv':float(kon),'fitted_koff_s_inv':float(koff),'fitted_Kd_nM':float(kd),'fitted_capacity_RU':float(cap),'residual_RMS_RU':float(np.sqrt(np.mean((prediction-corrected)**2))),'half_life_s':float(np.log(2)/.002),'fast_half_life_s':float(np.log(2)/.02),'equilibrium_at_10nM_RU':60.,'response_at_180s_10nM_RU':float(response(180,10)),'premature_endpoint_Kd_nM':float(wrong[0]),'premature_endpoint_capacity_RU':float(wrong[1]),'premature_fixed_capacity_Kd_nM':float(earlyfixed[0]),'high_slow_retained_after_420s':float(traces[0][1][0,-1]/traces[0][1][0,180]),'no_rebinding_retained_after_420s':float(np.exp(-.002*420)),'high_slow_Cs_at_180s_nM':float(traces[0][1][1,180]*1e9)}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

把这种分析带回抗体筛选，可以根据实际流程安排下一轮比较。若检测只有短暂接触时间，应比较该时间内的捕获量，而不是只按平衡解离常数排序；若洗涤持续数分钟，应检查相应时间窗内的保留量，并核实表面密度和流动条件是否引入再结合。若目标是材料抗污染性能，实验需要把不同蛋白质、运行缓冲和表面处理放入同一套对照关系，关注吸附与释放的整体行为。每一种应用都从它真正要经历的过程出发，再选择曲线上相应的量。

最后，把一个可比较的 SPR 结果写完整，需要同时交代固定对象、分析物状态、浓度系列、温度与缓冲条件、表面装载、参照方式、接触和冲洗时间以及所用模型。速率常数与解离常数对应的是这些条件下的相互作用。与溶液中的等温滴定量热结合时，两种方法分别提供时间过程与热效应，并帮助检查表面固定是否改变了原来的行为。读懂 SPR 的目的，正是让一条不断变化的线，成为下一次样品设计和实验选择的依据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Harvard CMI: Surface plasmon resonance](https://cmi.hms.harvard.edu/surface-plasmon-resonance)

   折射率响应、固定配体、参照与匹配溶剂。
2. [Liedberg, Nylander & Lundström (1983): Surface plasmon resonance for gas detection and biosensing](https://bdt.semi.ac.cn/download/0.143812733726721.pdf)

   原始免疫结合与浓度依赖时间记录的历史。
3. [Biacore T200 Getting Started Handbook](https://cmi.hms.harvard.edu/sites/g/files/omnuum4016/files/cmi/files/biacoret200_gettingstarted_handbook.pdf)

   参照、空白周期、再生和浓度系列。
4. [Cytiva: Kinetics and affinity measurements with Biacore systems](https://cdn.cytivalifesciences.com/api/public/content/digi-33041-pdf)

   浓度设计、传质与平衡分析。
5. [Biacore Insight Evaluation Software User Manual, 29287248 AH](https://d3.cytivalifesciences.com/prod/IFU/29287248.pdf)

   同亲和力不同速率、残差与动力学模型。
