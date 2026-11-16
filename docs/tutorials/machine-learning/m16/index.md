# 语言模型怎样学会续写与回答

Source: https://ml-biomat.com/tutorials/machine-learning/m16/
Language: zh-CN

从小语料的因果预测走到 LoRA、偏好优化、量化与可核查的能力评价。

## 1. 从补全一句话，到完成一项语言任务

输入法预测下一个词，搜索系统改写查询，程序助手补全函数，这些用途都需要根据已有文字判断接下来可能出现什么。语言模型把这个问题写成条件概率：给定前文，为下一个 token 分配概率，再把一个个预测接成长序列。token 是模型处理的离散单位，可以是一个字、一个词的一部分或一段字节。模型并不直接接收屏幕上整段文字的含义，而是先接收这些单位的编号，逐层计算它们之间的关系。

把模型训练得善于续写，与让它按要求回答问题，是相关但不同的工作。预训练从大量文本中学习语言结构和规律，指令微调用任务示范调整输出方式，偏好优化再根据多个回答之间的比较塑造行为。量化和蒸馏关注怎样用更少资源保留所需能力，检索与工具则可以向系统提供额外信息或操作。本章沿训练链条解释这些环节，并用一个可以从头运行的小语言模型展示真正的因果预测与低秩适配。

实例的语言世界只有十八个 token，陈述句形如“the red dog runs .”。我们先用不同的完整句子划分训练、验证与测试，再冻结学到的底座，只训练少量 LoRA 参数，让它回答“color of the red dog ? :”。任务足够小，读者可以逐项核对：模型看到了哪些 token，哪些位置计入损失，多少参数真正更新，以及适配权重合并后是否给出同样输出。大型模型的预算、数据与评价问题则从这些具体计算继续展开。

## 2. 语料与分词决定模型究竟读到了什么

预训练文本不是越多越好的一堆文件。相同网页的转载、重复代码片段和模板内容会改变样本权重，低质量扫描文字可能带入系统性错误，不同语言和领域的配比则影响模型把计算花在哪里。去重应在文档、近重复片段和数据划分之间进行，记录保留规则。评价集污染还包括试题答案的解释、改写版本或同一题的镜像，并不只限于完全相同的字符串。先按文档或来源分组，再切训练窗口，能减少相邻片段跨越划分造成的泄漏。

BPE 分词从较小单位出发，反复合并语料中频繁相邻的 token，得到常见子词；字节级方案以字节作为基本覆盖单位，能表示不同字符组合。词表较大时，一段文字往往需要较少 token，但嵌入与输出层也更大；词表较小时，序列可能更长。中文、罕见术语和代码的切分效率可以不同，因此相同字符数不等于相同计算量。分词器的归一化、特殊符号和聊天模板必须与模型匹配，否则文本看起来相同，输入编号和边界却可能已经变化。

一个手算例子有助于理解合并：假设语料只有“ab”出现三次、“ac”出现一次，从字符 a、b、c 开始，相邻对 a–b 的频次最高，先合并为 token“ab”；之后“ab”由一个 token 表示，“ac”仍需两个。实际 BPE 要保存合并顺序，编码新文本时按学到的规则执行。它是在分配表示单位，并没有因为合并了“ab”就理解这个词。本章固定十八词表，让读者直接查看编号到词的映射，把注意力放在语言模型与适配机制上。

数据版本同样参与实验定义。更新清洗规则、替换分词器或调整领域采样比例，都会改变模型面对的训练分布。训练窗口是否跨越文档边界、结束符怎样插入、填充 token 是否计入损失，也应明确。在小例子中，每条陈述句都以开始符和结束符包围，二十七种句子先按完整文本分到十六条训练、六条验证和五条测试，没有相同完整句子跨越训练与测试。

## 3. 下一词预测怎样变成一个可训练的模型

统计语言模型曾使用有限长度的词历史估计下一词概率，例如根据前两个词统计第三个词。神经语言模型把词映射为可学习向量，让相似上下文共享参数；循环网络随后用状态压缩更长历史，Transformer 则通过注意力直接连接不同位置。这个发展过程始终围绕一个问题：已有文字中的哪些线索能帮助预测下一单位？规模扩大后，模型在许多任务上表现出更广的迁移能力，但训练目标仍可以从逐 token 的概率读起。

$$
p_\theta(x_{1:L})=\prod_{t=1}^{L}p_\theta(x_t\mid x_{<t}),\qquad \mathcal L=-\frac1{N_{\rm scored}}\sum_{t=1}^{L}m_t\log p_\theta(x_t\mid x_{<t}),\quad N_{\rm scored}=\sum_t m_t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cbb686effe661c228e62f064.svg) | 第 t 个 token 与其之前的前缀，token 是离散编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc947ed58e2957c8badfe9da.svg) | 序列长度与位置索引，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a564121e37890a2a9e2674a1.svg) | 模型参数与对应条件概率；概率无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ab8ec7e384ca94386628a21f.svg) | 损失掩码，计分位置为 1，提示或填充等不计分位置为 0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/808a7af514d2203e40910dce.svg) | 实际计分 token 个数，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a37d71725f7b516cbb9cf38.svg) | 平均负自然对数概率，单位 nat/token。 |

整句概率按概率链式法则分解，训练则累计正确 token 的负对数。两个计分 token 的正确概率为 0.8 与 0.5 时，序列概率是 0.4，平均损失为 −(ln0.8+ln0.5)/2≈0.4581。提示不计分时 m=0，但提示仍通过因果注意力影响回答概率。代码先将输入与目标错开一位，再把适配提示的目标标为忽略；它不把答案提前放进需要预测答案的位置。

因果掩码规定每个位置只能读取自身和之前的位置，防止训练时偷看下一词。一次训练可以并行计算许多位置的预测，因为参考前文已经给定；真正生成时，下一个输入要等当前 token 选出后才能确定。把“the red dog”作为前缀时，模型输出的不是一个孤立答案，而是整个词表上的分布。贪心解码选最大项，采样根据概率随机选择，温度和 top-k 等策略又会改变随机性。评价时应记录这些选择，因为它们会影响答案和运行成本。

$$
\mathrm{PPL}=\exp(\mathcal L)=\left(\prod_{t\in\mathcal S}\frac1{p_\theta(x_t\mid x_{<t})}\right)^{1/|\mathcal S|}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e4e868f2fc2500459ddfb40.svg) | 有效 token 的平均负自然对数损失，nat/token。 |
| ![Formula](https://ml-biomat.com/static/agent-math/70e8b5284e565dcc725b6ae7.svg) | 参与评价的位置集合及其个数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5ee0d293718f519d772b8cea.svg) | 模型给正确 token 分配的条件概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f08cb97629674a8500700c57.svg) | 困惑度及自然指数函数；困惑度无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/092ff4a34fc8a0e4ab5d52f2.svg) | 位置、当前 token、前缀和模型参数。 |

平均对数先把许多概率稳定地累加，取指数后等价于逆概率的几何平均。若每个正确 token 都有概率 0.25，损失为 ln4，困惑度就是 4；若两个位置概率为 0.8 与 0.5，困惑度为 √(1/0.4)≈1.581。比较困惑度应使用相同分词、计分位置和语料，否则“一个 token”并非相同单位。

困惑度是平均负对数损失的指数。模型总给正确 token 概率 1/4，困惑度就是 4，可以理解为这种对数评分下的有效选择数；它不是“每句话有四种正确答案”。不同分词器把同一段文字拆成不同数量的单位，逐 token 困惑度不能直接横向比较。低困惑度也不等于指令遵循、事实核对或数学推理都好，后者需要对应任务的测试。本章同时检查测试困惑度、完整生成句子和适配后的回答，分别观察语言分布与任务行为。

## 4. 预算应分给参数、数据与实际计算

给定计算预算，增大模型与增加训练 token 会互相挤占资源。规模规律通过一组受控训练，拟合模型大小、数据量与验证损失之间的关系，用来规划下一批实验。Chinchilla 的原始研究强调了固定预算下同时考虑参数和训练数据的重要性；它的结论来自论文指定的模型、数据和计算范围。实际项目还要把数据质量、重复次数、上下文长度和后续推理成本放入选择，不能把某个参数—token 比例当作所有任务的固定常数。

数据配比可以理解为一张学习时间表。通用文本、代码、数学、不同语言与目标领域分别占多少，会改变模型遇到的错误和更新方向。重复一个小而优质的数据集，与增加新的独立样本不同；过多重复可能使训练损失继续下降而验证损失上升。先做几组规模适当的对照，记录处理 token 数、实际吞吐、验证损失与任务结果，再决定是否增大模型，往往比只比较参数数量更能说明预算的去向。

混合专家 MoE 在某些层准备多个前馈网络，由路由器为每个 token 选择少量专家参与计算。总参数量可以很大，而每个 token 实际激活的参数较少；Switch Transformer 是稀疏路由发展的一个清楚例子。路由并不意味着某个专家天生负责“物理”或“英语”，这种分工由训练形成，并可能混合多种因素。专家负载不均、容量限制和设备间通信都会影响运行，因此总参数、激活参数和真实延迟应分别报告。

$$
y=\sum_{e\in\mathcal E_k(x)}g_e(x)F_e(x),\qquad \sum_{e\in\mathcal E_k(x)}g_e(x)=1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | 一个 token 的输入与输出隐藏向量，通常同为 d 维，没有指定物理单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81766128040a367a6c93adfc.svg) | 第 e 个专家网络，把输入映射为输出向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bab1cdf2de84a62048077249.svg) | 路由器为输入选择的 k 个专家组成的集合、选择数量与专家索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/83c51e1af9178eecb57722fc.svg) | 在所选专家上归一化的非负权重，无量纲。 |

这给出一种 top-k 路由后重新归一化的汇总形式，具体 MoE 实现可采用不同门控约定。若两个所选专家输出 (2,0) 与 (0,4)，门控权重为 0.75 和 0.25，汇总结果为 (1.5,1)。未被选中的专家不参与这个 token 的前馈计算，但它们的参数仍需要存储。路由器也有计算与通信成本，因此激活专家数量不能直接当作完整运行时间。

训练与推理的内存组成也不一样。训练需要参数、梯度、优化器状态和反向传播所需激活；自回归推理可以缓存先前 token 的注意力键和值，减少重复计算，却让缓存随上下文和批次增大。处理初始提示的 prefill 与逐步生成的 decoding 是不同阶段，报告吞吐时应说明是否包含两者，以及输入输出各有多长。模型能放进内存，并不说明交互延迟已经合适；增加批处理可能提高总吞吐，同时增加某个请求的等待。

## 5. 指令微调与 LoRA：把更新限制在小的变化空间

监督指令微调 SFT 使用“输入任务—目标回答”样本，把已有语言分布调到需要的任务形式。若只希望学习回答部分，损失应屏蔽提示与填充位置；模型仍能读取提示，但这些位置不直接贡献目标损失。对话模板还要区分角色、轮次与结束标记。示范的质量和覆盖决定模型学到什么：统一格式能帮助稳定输出，缺少例外、错误修正或复杂输入则会留下对应能力缺口。任务样本应按实际使用场景组织，而不是只追求条数。

$$
y=W_0x+\frac\alpha r BAx+b,\qquad W_{\rm merged}=W_0+\frac\alpha r BA,\qquad N_{\rm LoRA}=r(d_{\rm in}+d_{\rm out})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e69c4f8619ee3c1461e894d3.svg) | 输入 d_in 维向量、输出 d_out 维向量与输出偏置；神经表示没有指定物理单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/605abc76c378afdf9024a75f.svg) | 冻结的原权重矩阵，形状 d_out×d_in。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | 可训练因子，形状分别为 r×d_in 与 d_out×r。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2e532aa640b07a3f05077121.svg) | 正整数秩与缩放超参数；α/r 无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1deeadf66ae71d7cb0226d5a.svg) | 合并后的普通权重矩阵，与原权重同形状。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce72a13d053499294034e6ef.svg) | 低秩因子参数个数、输入维度与输出维度，整数。 |

先用 A 把输入压到 r 维，再由 B 映射回输出维度，增量的秩至多为 r。以 W₀ 为二阶单位阵、x=(1,2)、A=(1,1)、B=(0.5,−0.25)ᵀ、α=r=1 为例，Ax=3，BAx=(1.5,−0.75)，最终 y=(2.5,1.25)，偏置取零。32×32 层的 r=4 因子有 256 个参数；18×32 输出层有 200 个。本例两层 32×32 加输出层，共训练 256+256+200=712 个数。

LoRA 冻结原权重，用两个较小矩阵的乘积表示增量。可以把它想成保留原来的调音台，只增加少量联动旋钮：每个旋钮可以同时影响许多输出，但独立变化方向受秩限制。一个 32×32 权重矩阵有 1024 个数，秩为 4 的两个因子共有 4×32+32×4=256 个数。它限制的是可学习更新的结构，并不要求原权重本身低秩。选择更大秩会增加表达空间和参数成本，是否需要由验证任务决定。

本章把 LoRA 加到注意力的查询、值投影和输出词表层，秩都为 4，缩放系数取 α/r=2。一个因子随机初始化，另一个为零，所以适配开始时增量恰为零，模型输出与底座一致。训练后可以把增量乘积加回原权重，形成普通线性层；我们用合并前后的 logits 差检查这一等价关系。若同时服务多个任务，也可以保留共同底座与不同适配器，根据任务加载对应变化，而不必复制每套完整底座权重。

## 把低秩支路与合并权重算成同一个结果

这个二维例子用单位阵作为冻结底座。选择一个或两个变化方向，移动输入和缩放 α，查看 A、B、增量矩阵与两条计算路径的输出。二维用于手算，参数节省应查看正文的 32 维真实模型。

[Figure: 低秩因子、合并矩阵与输出数值](https://ml-biomat.com/tutorials/machine-learning/m16/#M16-svg)

## 6. 量化与蒸馏减少的资源并不相同

量化用较少位数表示数值，通常需要尺度和有时需要零点，把浮点数映射到有限整数或其他编码。权重的值域和异常值会影响误差，因此按张量、通道或小块设置尺度会产生不同取舍。存储字节变少，不自动等于运行更快；实际速度还取决于计算核是否支持对应低精度运算、反量化成本和设备。对比时应同时查看文件与内存大小、延迟、吞吐和任务误差，明确量化的是权重、激活还是缓存。

$$
s_i=\frac{\max_j|W_{ij}|}{127},\quad Q_{ij}=\operatorname{clip}\!\left(\operatorname{round}\frac{W_{ij}}{s_i},-127,127\right),\quad \hat W_{ij}=s_iQ_{ij}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33a5218183f1f6f9bd612ba0.svg) | 输出层第 i 行、第 j 列浮点权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 输出与输入维度的整数索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | 每行的正尺度，与权重同单位；全零行以数值下限处理。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e116ac59f0a50d2fdd88270.svg) | 存为 int8 的整数码，范围 −127 到 127，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a31f2474b0940d633856d1bb.svg) | 反量化后的浮点近似权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ef7f27c02f7a407ee9a0fbeb.svg) | 取最近整数与截断到给定范围的操作。 |

先按行最大绝对值设置尺度，使最大值对应整数 127，再将其他权重映射到最近格点。若一行是 (−1,0,0.5,1)，尺度为 1/127，整数码为 (−127,0,64,127)，反量化后的第三项约为 0.50394，误差约 0.00394。每个码占一字节，但每行还需要尺度。本例十八行、每行三十二个权重，整数码 576 字节，加十八个 float32 尺度 72 字节，总计 648 字节。

QLoRA 将冻结底座的低位存储与可训练低秩适配器结合，反向传播仍通过底座计算把梯度传到适配器。原始工作讨论 NF4、量化尺度的再次量化以及管理内存峰值的优化器策略。这里不能把“底座是四位存储”理解为所有计算、激活和优化器状态都只用四位。本章只对合并后的输出层演示逐行 int8 权重量化，并反量化检查数值误差；实际训练过程是浮点 LoRA，二者在代码和结果中分开标明。

蒸馏则让较小学生模型学习教师提供的输出分布、回答或中间表示。软目标可以告诉学生“哪些错误候选仍然较相似”，而不仅给一个正确编号；生成式蒸馏还可使用教师生成的任务示范。温度、教师准确性和样本覆盖都会影响结果，教师的系统性错误也可能传给学生。量化改变数值表示，蒸馏改变模型或训练目标，LoRA改变适配参数化，三者可以组合，却应分别比较各自增加的收益与误差。

一个三分类例子能说明软监督传递了什么。教师给三个类别的概率为 0.7、0.2、0.1，学生为 0.4、0.35、0.25，匹配教师分布会提高第一类权重，同时保留第二类比第三类更接近的关系。只给第一类的硬标签，则没有传递后两项之间的差别。温度可以显露较弱候选的关系，也可能放大教师不合适的判断，因此学生仍需在独立任务样本上评价，并同时报告模型大小和推理成本。

## 7. 偏好优化怎样利用两个回答之间的比较

有时写出唯一标准答案很困难，但比较两个回答更容易。例如一个回答直接解释实验步骤，另一个遗漏关键条件；标注者可以选择更有用的一项。经典 RLHF 流程先从这类比较训练奖励模型，再让语言模型生成回答，根据奖励与相对参考策略的偏离代价更新。奖励模型是对偏好数据的近似，优化过强可能让模型利用评分中的漏洞，因此训练要同时检查奖励变化与独立任务表现。强化学习部分可以使用 PPO 等方法，其策略更新细节见深度强化学习章节。

$$
\mathcal L_{\rm DPO}=-\log\sigma\!\left[\beta\left(\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\rm ref}(y_w\mid x)}-\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\rm ref}(y_l\mid x)}\right)\right],\qquad \sigma(z)=\frac1{1+e^{-z}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dba9bd8d1a5e5f99648a8f0a.svg) | 同一个提示、偏好回答和非偏好回答，均为 token 序列。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a30d99dab0379f2f58aac9b9.svg) | 当前策略与固定参考策略的完整回答条件概率，无量纲；由回答 token 对数概率求和计算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1cc8c189acd9786d014e26f9.svg) | 可训练策略参数与正的偏好目标系数；β 无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff377425645f91fe4ca4ec1d.svg) | Sigmoid 函数及其无量纲输入。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cefac4625b95ed29e1d4d22.svg) | 一个偏好对的负自然对数损失，nat。 |

两个对数比先分别衡量当前策略相对参考策略对两个回答的改变，再比较偏好回答是否获得更大提升。当前对数概率 −1、−2，参考均为 −1.5，则括号内差为 1；β=0.2 给出 −lnσ(0.2)≈0.59814。当前与参考完全相同则差为零、损失 ln2≈0.6931。实际训练对许多偏好对取平均；整段对数概率随长度变化，数据与评价需要处理长度偏好。

DPO 把成对偏好直接写成相对参考模型的对数概率比目标，在这一训练形式中不需要另外训练奖励模型并在线采样完成强化学习循环。它要求比较的是同一个提示下的偏好回答与非偏好回答，也需要固定的参考概率。若只提高偏好回答概率而不考虑另一回答和参考分布，优化含义就改变了。偏好标注的标准、回答长度和数据来源也会影响学习方向；“更长”有时会被误当成“更好”，因此评价应包含内容质量与格式等具体维度。

本章给出一个可计算的 DPO 数值例子：当前模型对偏好和非偏好回答的对数概率分别为 −1、−2，参考模型均为 −1.5，温度系数 β=0.2，得到损失约 0.5981。它验证的是目标函数的运算，不是一次大型偏好训练。进一步开展偏好实验时，应保存成对样本、判断规则和独立评价集，查看不同任务或语言上的变化，避免把一个总胜率当作全部能力的概括。

偏好批次中的 token 计分必须一致。两个回答接在相同提示后面，但完整回答概率只累计回答 token，排除提示与填充；参考模型也应使用相同分词和回答边界。对数概率求和对应整段序列，随手改成按长度平均就定义了另一种目标，除非采用的方法明确要求这样做。偏好标签颠倒也会反转学习方向，因此训练前核对几组可读的成对样本，能把公式中的量与标注者实际比较的内容对应起来。

## 8. 完整实验：先学句子，再只更新 712 个参数

底座采用一层因果 Transformer，隐藏维度为 32，四个注意力头，每个头八维，前馈隐藏层为 64，共 10290 个参数。每个陈述句有六个预测位置，每个训练批次从十六条训练句中有放回抽取 24 条，同一句可在批次内重复，最多进行 400 次更新；每十步评价一次独立验证句子，并保留验证损失最低的检查点。适配任务固定使用六种颜色—动物问句组合训练，另外三种组合用于回答评价，提示部分不计损失，只训练颜色词与结束符这两个回答 token。

### 从头预训练、低秩适配与权重合并

完整实现单层因果 Transformer 和 LoRA；不下载大模型。保存训练曲线、完整生成、量化与偏好损失算例，并检查冻结权重、因果边界和合并误差。

```
"""A tiny causal language model, genuine low-rank adaptation, and exact checks."""
import argparse,copy,json,math,time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
WORDS=['<pad>','<bos>','<eos>','the','red','green','blue','fox','dog','cat','runs','sleeps','jumps','.','color','of','?',':']
VOCAB={w:i for i,w in enumerate(WORDS)};D=32
def ids(words):return [VOCAB[w]for w in words]

class Attention(nn.Module):
    def __init__(self):
        super().__init__();self.q=nn.Linear(D,D);self.k=nn.Linear(D,D);self.v=nn.Linear(D,D);self.out=nn.Linear(D,D)
    def forward(self,x):
        b,t,d=x.shape
        q,k,v=[layer(x).reshape(b,t,4,8).transpose(1,2)for layer in [self.q,self.k,self.v]]
        scores=q@k.transpose(-2,-1)/math.sqrt(8);mask=torch.triu(torch.ones(t,t,dtype=torch.bool),diagonal=1);scores=scores.masked_fill(mask,float('-inf'))
        return self.out((scores.softmax(-1)@v).transpose(1,2).reshape(b,t,d))

class TinyLM(nn.Module):
    def __init__(self):
        super().__init__();self.token=nn.Embedding(len(WORDS),D);self.position=nn.Embedding(16,D);self.norm1=nn.LayerNorm(D);self.attn=Attention();self.norm2=nn.LayerNorm(D);self.ff=nn.Sequential(nn.Linear(D,64),nn.GELU(),nn.Linear(64,D));self.final=nn.LayerNorm(D);self.head=nn.Linear(D,len(WORDS))
    def forward(self,tokens):
        x=self.token(tokens)+self.position(torch.arange(tokens.shape[1]))[None];x=x+self.attn(self.norm1(x));x=x+self.ff(self.norm2(x));return self.head(self.final(x))

class LoRALinear(nn.Module):
    def __init__(self,base,rank=4,alpha=8):
        super().__init__();self.base=base;self.A=nn.Parameter(torch.randn(rank,base.in_features)*.02);self.B=nn.Parameter(torch.zeros(base.out_features,rank));self.scale=alpha/rank
        for p in self.base.parameters():p.requires_grad=False
    def forward(self,x):return self.base(x)+(x@self.A.T@self.B.T)*self.scale
    def merged(self):
        layer=copy.deepcopy(self.base)
        with torch.no_grad():layer.weight.add_(self.scale*self.B@self.A)
        return layer

def corpus():
    parts=[[],[],[]];sentences=[[],[],[]]
    for c,color in enumerate(['red','green','blue']):
        for a,animal in enumerate(['fox','dog','cat']):
            for v,verb in enumerate(['runs','sleeps','jumps']):
                residue=(c+2*a+v)%5;split=2 if residue==0 else 1 if residue==1 else 0
                words=['<bos>','the',color,animal,verb,'.','<eos>'];parts[split].append(ids(words));sentences[split].append(' '.join(words))
    return [torch.tensor(p)for p in parts],sentences

def prompts():
    allrows=[];istrain=[]
    for c,color in enumerate(['red','green','blue']):
        for a,animal in enumerate(['fox','dog','cat']):
            allrows.append(ids(['<bos>','color','of','the',color,animal,'?',':',color,'<eos>']));istrain.append(c!=a)
    return torch.tensor(allrows),np.array(istrain)

def lm_loss(model,rows):
    out=model(rows[:,:-1]);return nn.functional.cross_entropy(out.reshape(-1,len(WORDS)),rows[:,1:].reshape(-1))

def generate(model,prompt,steps=8):
    tokens=list(prompt)
    for _ in range(steps):
        with torch.no_grad():n=int(model(torch.tensor([tokens]))[0,-1].argmax())
        tokens.append(n)
        if n==VOCAB['<eos>']:break
    return ' '.join(WORDS[n]for n in tokens)

def run(out,language):
    out.mkdir(parents=True,exist_ok=True);torch.manual_seed(16);rng=np.random.default_rng(16);text=lambda z,e:z if language=='zh' else e
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
    save=lambda fig,n:(fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight'),fig.savefig(out/f'{n}-{language}.png',dpi=140,bbox_inches='tight'),plt.close(fig))
    (train,valid,test),sentences=corpus();base=TinyLM();optimizer=torch.optim.Adam(base.parameters(),lr=.003);trace=[];best=float('inf');selected=0;start=time.perf_counter()
    for step in range(1,401):
        batch=train[torch.randint(len(train),(24,))];optimizer.zero_grad();loss=lm_loss(base,batch);loss.backward();optimizer.step()
        if step%10==0:
            with torch.no_grad():vl=lm_loss(base,valid).item()
            trace.append([step,loss.item(),vl])
            if vl<best:best=vl;weights=copy.deepcopy(base.state_dict());selected=step
    elapsed=time.perf_counter()-start;base.load_state_dict(weights);base.eval()
    with torch.no_grad():test_loss=lm_loss(base,test).item()
    rows,adapttrain=prompts();labels=rows[:,1:].clone();labels[:,:7]=-100
    with torch.no_grad():before=base(rows[:,:8])[:,-1].softmax(1).numpy()
    adapted=copy.deepcopy(base)
    for p in adapted.parameters():p.requires_grad=False
    adapted.attn.q=LoRALinear(adapted.attn.q);adapted.attn.v=LoRALinear(adapted.attn.v);adapted.head=LoRALinear(adapted.head)
    with torch.no_grad():initial_error=float((base(rows[:,:8])-adapted(rows[:,:8])).abs().max())
    frozen={n:p.detach().clone()for n,p in adapted.named_parameters()if not p.requires_grad};opt=torch.optim.Adam([p for p in adapted.parameters()if p.requires_grad],lr=.015);atrace=[]
    for step in range(1,401):
        opt.zero_grad();logits=adapted(rows[adapttrain,:-1]);loss=nn.functional.cross_entropy(logits.reshape(-1,len(WORDS)),labels[adapttrain].reshape(-1),ignore_index=-100);loss.backward();opt.step()
        if step%10==0:atrace.append([step,loss.item()])
    with torch.no_grad():after=adapted(rows[:,:8])[:,-1].softmax(1).numpy();adapt_test_loss=nn.functional.cross_entropy(adapted(rows[~adapttrain,:-1]).reshape(-1,len(WORDS)),labels[~adapttrain].reshape(-1),ignore_index=-100).item()
    frozen_error=max(float((p-frozen[n]).abs().max())for n,p in adapted.named_parameters()if n in frozen)
    merged=copy.deepcopy(adapted);merged.attn.q=merged.attn.q.merged();merged.attn.v=merged.attn.v.merged();merged.head=merged.head.merged()
    with torch.no_grad():merge_error=float((merged(rows[:,:8])-adapted(rows[:,:8])).abs().max())
    torch.save(base.state_dict(),out/'base.pt');torch.save(merged.state_dict(),out/'merged.pt')
    metadata={'vocabulary':WORDS,'architecture':{'hidden_dimension':32,'heads':4,'blocks':1,'feedforward_dimension':64,'max_positions':16},'adaptation':{'targets':['attn.q','attn.v','head'],'rank':4,'alpha':8},'selected_pretrain_step':selected}
    (out/'model.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    reloaded=load_model(out/'merged.pt')
    with torch.no_grad():reload_error=float((reloaded(rows[:,:8])-merged(rows[:,:8])).abs().max())
    true=rows[:,8].numpy();pred=after.argmax(1);bpred=before.argmax(1);delta=(adapted.head.scale*adapted.head.B@adapted.head.A).detach().numpy();singular=np.linalg.svd(delta,compute_uv=False)
    w=merged.head.weight.detach();scale=w.abs().amax(1,keepdim=True).clamp_min(1e-8)/127;quant=(w/scale).round().clamp(-127,127).to(torch.int8);recovered=quant.float()*scale;quant_error=float((w-recovered).abs().max())
    # Causal attention should leave a prefix unchanged when only its suffix changes.
    modified=test[:1,:-1].clone();modified[0,-1]=VOCAB['?']
    with torch.no_grad():causal_error=float((base(test[:1,:-1])[:,:-1]-base(modified)[:,:-1]).abs().max())
    dpo_loss=float(nn.functional.softplus(torch.tensor(-.2)));params=sum(p.numel()for p in base.parameters());trainable=sum(p.numel()for p in adapted.parameters()if p.requires_grad)
    summary={'vocabulary_size':len(WORDS),'unique_sentence_splits':[len(train),len(valid),len(test)],'unique_split_overlap':len(set(sentences[0])&set(sentences[2])),'base_parameters':params,'lora_trainable_parameters':trainable,'pretrain_selected_step':selected,'pretrain_test_loss':test_loss,'pretrain_test_perplexity':math.exp(test_loss),'pretrain_seconds':elapsed,'pretrain_tokens_per_second':400*24*6/elapsed,'base_color_accuracy':float(np.mean(bpred==true)),'lora_seen_pair_accuracy':float(np.mean(pred[adapttrain]==true[adapttrain])),'lora_unseen_pair_accuracy':float(np.mean(pred[~adapttrain]==true[~adapttrain])),'adapt_test_response_loss':adapt_test_loss,'lora_initial_output_error':initial_error,'frozen_parameter_max_change':frozen_error,'merged_logits_max_error':merge_error,'causal_prefix_error':causal_error,'lora_head_numerical_rank':int(np.sum(singular>1e-5)),'quant_head_max_weight_error':quant_error,'quant_head_storage_bytes':quant.numel()+scale.numel()*4,'float_head_storage_bytes':w.numel()*4,'dpo_hand_loss':dpo_loss,'base_generated':generate(base,ids(['<bos>'])),'adapted_outputs':[generate(adapted,row[:8].tolist(),3)for row in rows]}
    summary.update({'reloaded_logits_max_error':reload_error,'reloaded_example':generate(reloaded,ids(['<bos>','color','of','the','red','fox','?',':']),3)})
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'data.npz',pretrain_trace=trace,adapt_trace=atrace,before=before,after=after,targets=true,train_mask=adapttrain,head_delta=delta,singular_values=singular)
    (out/'corpus.json').write_text(json.dumps({'train':sentences[0],'validation':sentences[1],'test':sentences[2]},indent=2),encoding='utf-8')
    assert initial_error==0 and frozen_error==0 and causal_error<1e-6 and merge_error<1e-4 and reload_error==0
    fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained');tr=np.array(trace);at=np.array(atrace)
    axs[0].plot(tr[:,0],tr[:,1],label=text('训练','Train'),color='#176b91');axs[0].plot(tr[:,0],tr[:,2],label=text('验证：独立句子','Validation: held-out sentences'),color='#bc584d');axs[0].axvline(selected,color='#9a9a9a',ls='--');axs[0].set(xlabel=text('预训练步数','Pretraining step'),ylabel=text('每token交叉熵','Cross entropy per token'));axs[0].legend()
    axs[1].plot(at[:,0],at[:,1],color='#267c6a');axs[1].set(xlabel=text('LoRA步数','LoRA step'),ylabel=text('仅回答token的交叉熵','Cross entropy on answer tokens'));save(fig,'training')
    fig,axs=plt.subplots(1,2,figsize=(11,5),layout='constrained');promptnames=[f'{WORDS[row[4]]} {WORDS[row[5]]}'for row in rows]
    for ax,probs,title in zip(axs,[before,after],[text('适配前','Before adaptation'),text('LoRA之后','After LoRA')]):
        im=ax.imshow(probs[:,4:7],vmin=0,vmax=1,cmap='Blues',aspect='auto');ax.set(xticks=range(3),xticklabels=['red','green','blue'],yticks=range(9),yticklabels=[s+(' *'if not adapttrain[i]else'')for i,s in enumerate(promptnames)],title=title,xlabel=text('颜色token','Color token'))
        for i in range(9):
            for j in range(3):ax.text(j,i,f'{probs[i,4+j]:.2f}',ha='center',va='center',color='white'if probs[i,4+j]>.5 else '#193b50',fontsize=9)
    fig.colorbar(im,ax=axs,label=text('在完整18词表中的概率','Probability in the full 18-token vocabulary'));save(fig,'answers')
    fig,axs=plt.subplots(1,3,figsize=(12,3.5),layout='constrained');lim=max(abs(delta).max(),1e-9);im=axs[0].imshow(delta,cmap='RdBu_r',vmin=-lim,vmax=lim,aspect='auto');axs[0].set(xlabel=text('输入维度','Input dimension'),ylabel=text('输出token','Output token'),title=text('输出层低秩增量','Low-rank output-head update'));fig.colorbar(im,ax=axs[0])
    axs[1].semilogy(np.arange(1,len(singular)+1),np.maximum(singular,1e-9),'o-',color='#176b91');axs[1].axvline(4.5,color='#aaa',ls='--');axs[1].set(xlabel=text('奇异值编号','Singular value index'),ylabel=text('奇异值','Singular value'),title=text('秩4的结构','Rank-four structure'))
    axs[2].bar([text('全模型','Base model'),'LoRA'],[params,trainable],color=['#9babb5','#267c6a']);axs[2].set(ylabel=text('参数个数','Parameter count'),title=text('冻结与训练','Frozen and trainable'));save(fig,'adapters')
    print(json.dumps(summary,indent=2))

def load_model(checkpoint):
    metadata=json.loads(checkpoint.with_name('model.json').read_text(encoding='utf-8'))
    expected={'hidden_dimension':32,'heads':4,'blocks':1,'feedforward_dimension':64,'max_positions':16}
    if metadata['vocabulary']!=WORDS or metadata['architecture']!=expected:raise ValueError('Checkpoint vocabulary or architecture does not match TinyLM.')
    model=TinyLM();model.load_state_dict(torch.load(checkpoint,map_location='cpu',weights_only=True));return model.eval()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');p.add_argument('--load',type=Path);p.add_argument('--prompt',default='<bos> color of the red fox ? :');args=p.parse_args()
    if args.load:print(generate(load_model(args.load),ids(args.prompt.split()),3))
    else:run(args.output,args.language)
```

运行后会保存底座权重 base.pt、合并适配后的权重 merged.pt，以及记录十八词词表、架构、适配目标层、秩与缩放的 model.json。代码重新建立一个全新的 TinyLM，载入 merged.pt，在同一组原始 token 上得到与保存前完全一致的 logits，最大差为零。完成训练后，执行 `python main.py --load output/merged.pt --prompt "<bos> color of the red fox ? :"`，即可读回模型并得到 `red <eos>`；其中 output 应与训练时选择的输出目录一致。这条命令直接使用已保存权重，不再训练模型。

固定种子的实际运行选择第 50 步的底座，五条独立完整测试句的平均 token 损失为 0.72775，困惑度为 2.0704。贪心生成得到“the red dog runs .”。继续把底座训练到最后并没有改善验证表现，图中可以看到训练与验证曲线逐渐分开。小语料也会过拟合，因此选择检查点同样应依赖独立验证，而不是最后一个训练步或最低训练损失。

![实际预训练与 LoRA 曲线。底座按验证损失选择第 50 步，虚线表示所选检查点；适配曲线只统计颜色回答与结束符的损失。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b53d7002ecc1010209df94d7.svg?v=b53d7002ecc1)

图 1实际预训练与 LoRA 曲线。底座按验证损失选择第 50 步，虚线表示所选检查点；适配曲线只统计颜色回答与结束符的损失。

未适配的底座没有在这套问句格式上给出正确颜色；训练 712 个 LoRA 参数后，六个训练问句组合与三个适配留出组合的颜色回答全部正确。留出的是适配阶段的问句组合，底座预训练中可能已经见过同样颜色和动物组成的陈述句；测试衡量的是在这个小任务上读取提示中的颜色并按格式回答。完整词表有十八项，概率图只显示三个颜色项，其数值仍使用完整词表归一化。

![九种问句的三个颜色 token 概率，按完整十八词表归一化；星号标记适配阶段留出的三个问句组合。前后使用同样提示。](https://ml-biomat.com/static/tutorials/machine-learning/figures/1972107a08975644a33fa8a5.svg?v=1972107a0897)

图 2九种问句的三个颜色 token 概率，按完整十八词表归一化；星号标记适配阶段留出的三个问句组合。前后使用同样提示。

初始适配输出与底座差为零，所有冻结参数训练后的最大变化为零，改变句子后缀也没有影响之前位置的输出。LoRA 合并前后 logits 最大差约为 7.63×10⁻⁶，与浮点运算次序差异相符。输出层增量的数值秩为 4；图中的奇异值让这一结构可见。输出层逐行 int8 权重与尺度共占 648 字节，原浮点权重为 2304 字节，最大权重误差约 0.00635；这里统计的是这一层的权重与尺度，未把其他模型状态计入。

![输出词表层的真实 LoRA 增量、奇异值与参数数量。秩为 4，前四个奇异值之后出现数值舍入尺度；右图比较原模型参数与可训练适配参数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/a89f602a6081615320013cc2.svg?v=a89f602a6081)

图 3输出词表层的真实 LoRA 增量、奇异值与参数数量。秩为 4，前四个奇异值之后出现数值舍入尺度；右图比较原模型参数与可训练适配参数。

## 9. 推理计算、能力评价与可复用模型

生成多个候选时，应区分“候选里是否有正确答案”和“系统最后是否选对”。前者描述给定采样预算下的覆盖，后者还包含选择器的能力。代码任务可以用执行测试筛选候选，但筛选用测试与最终独立测试应分开；其他任务的验证器也可能与生成模型共享盲点。记录候选数量与筛选过程，才能判断收益来自生成器本身、更多搜索，还是更好的检查方法。

训练结束后，推理仍可以分配不同计算量。一次直接生成、重复生成多个候选后选择、逐步修订答案、调用验证器或执行程序检查，消耗的 token 与时间不同。推理时计算研究关心怎样把这些资源分配给难度不同的问题。重复采样只有在模型有机会产生正确候选、选择器能识别它时才有价值；把候选数量加倍并不自动提高最终答案质量。比较方法时应固定总生成预算，或明确画出质量随预算变化的关系。

推理能力评价应尽量把答案正确、过程可检验和表达流畅分开。数学题可以核对最终数值与关键推导，代码题可以执行独立测试，长文问答可以回到材料逐项核对。选择题的候选顺序、提示模板、少样本示例、解码设置和答案提取规则都可能改变成绩；记录这些因素后，再做重复与分组评价。更长的推理文本本身不是能力指标，能够在新条件下稳定得到正确结果才是任务关心的行为。

复用开放权重时，模型权重、代码、分词器和训练数据各有各的发布条件，应读取具体版本的模型卡与许可。模型卡应说明架构、语言、训练范围、适用输入、评价协议和结果；适配器还要记录准确底座版本、目标层、秩与缩放。仅有一个权重文件，无法保证别人使用了相同聊天模板或数值精度。将这些配置与数据划分、环境和推理示例一同保存，才能把一次成功运行变成可以继续研究的模型资产。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M16.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Language Modeling from Scratch](https://cs336.stanford.edu/)

   从分词、语料到训练预算的完整开放课程结构。
2. [Hugging Face — BPE tokenization](https://huggingface.co/learn/llm-course/chapter6/5)

   子词合并与字节级覆盖。
3. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

   低秩更新的原始论文，图只作链接阅读。
4. [Hugging Face PEFT — LoRA](https://huggingface.co/docs/peft/main/conceptual_guides/lora)

   冻结、因子维度和权重合并。
5. [QLoRA](https://arxiv.org/abs/2305.14314)

   低位冻结底座与低秩适配器。
6. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)

   相对参考策略的成对偏好目标。
7. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)

   给定预算下参数与数据的配比研究。
8. [Switch Transformers](https://arxiv.org/abs/2101.03961)

   稀疏专家路由、容量与通信。
9. [Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314)

   随问题难度分配推理计算。
10. [Hugging Face — Model Cards](https://huggingface.co/docs/hub/model-cards)

    模型、数据、评价与版本信息的组织。
