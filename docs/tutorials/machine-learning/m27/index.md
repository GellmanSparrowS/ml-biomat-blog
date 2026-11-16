# 把模型交到别人手中：部署、压缩与持续观察

Source: https://ml-biomat.com/tutorials/machine-learning/m27/
Language: zh-CN

沿着一个手写数字模型完成导出、真实接口调用、压缩比较和灰度重放，理解数据、版本、速度与反馈怎样共同决定可用性。

## 1 模型出了实验室，还要带上什么

假设你做了一个识别手写数字的小工具。在自己的程序里，它能读懂大多数图片；同伴把它接进网页后，同一张图片却被认成另一个数字。问题可能出在网络权重，也可能出在更不起眼的地方：一边把灰度除以16，另一边又除了一次；一边按行展开图片，另一边按列排列；网页传来的是字符串，模型需要的却是浮点数。部署要解决的，正是从真实输入到最终答案这一整条路径。我们希望任何一次预测都能说明用了哪个版本、怎样处理输入、花了多少时间，以及出现问题时如何恢复。

可以把训练好的网络想成一张经过试做的食谱。要让另一家厨房做出同样的菜，还要交代原料规格、计量单位、设备条件和操作顺序。模型对应食谱中的计算规则，数据契约对应原料规格，推理环境对应厨房设备，监测则帮助我们发现原料和操作发生的变化。这个比喻还有一个值得保留的细节：菜品质量和出餐速度是不同的指标。识别准确率很高的模型可能赶不上请求到达的速度；跑得很快的程序也可能稳定地输出错误答案。

2015年，Sculley等人在《机器学习系统中的隐藏技术债》中讨论了模型周围的数据依赖、配置和反馈回路。2017年的ML Test Score进一步把数据、模型、基础设施和监测组织成可检查的问题。研究关注点由一次离线分数延伸到持续运行的系统。本章把这段发展放进一个完整的小实验：训练手写数字模型，制作可重载的版本包，导出ONNX，实际调用本地接口，再比较压缩、响应时间和输入变化。所有步骤围绕同一组图片，前后的差异因此可以追溯到具体操作。

![原创建模流程与研究发展示意：上方连接固定数据、包含预处理的ONNX图和运行反馈；下方三项公开研究为本章问题提供历史背景。图中分流点为机制示意。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f90b9ebbf5b08aefc2a34915.svg?v=f90b9ebbf5b0)

图 1原创建模流程与研究发展示意：上方连接固定数据、包含预处理的ONNX图和运行反馈；下方三项公开研究为本章问题提供历史背景。图中分流点为机制示意。

所谓MLOps，可以先理解为让数据、训练、交付和运行观察协同工作的方式。个人项目也用得上其中的思想：保存拆分索引、让预处理跟随模型、为接口写几个明确的例子、为替换版本留下恢复入口，就已经能解决许多实际问题。项目扩大以后，再把这些职责接入模型注册表、流水线和服务平台。工具的规模可以逐步增加，而输入定义、版本身份和评价口径应从第一个可用模型开始保持清楚。

## 2 让一次预测找到自己的来路

我们的图片来自scikit-learn随包提供的digits数据，共1797张8×8灰度图，像素范围为0到16，标签是十个数字。固定分层拆分得到1077张训练图片、270张验证图片和450张测试图片。训练集更新权重，验证集选择保存哪一轮，测试集用于最后比较已经确定的方案。大网络包含64个隐藏单元，小网络包含16个隐藏单元，二者都先把原始像素除以16，再经过线性层、ReLU和输出层。这里的尺寸足够小，普通CPU就能把交付流程从头走完。

保存模型时，我们同时写出manifest.json。它包含图片数组的摘要、脚本摘要、拆分索引、输入形状与单位、依赖版本、各模型文件摘要以及评价结果。摘要是根据完整字节内容计算的短标识；文件改变，摘要通常也会改变。它帮助我们回答“今天运行的是不是昨天验证过的那个文件”，但不会评价模型本身是否正确。要回答后一个问题，还需要数据定义和测试结果。文件身份、计算行为和任务质量是三个相互衔接的检查层次。

模型注册表把这种关系放到多人协作中管理。一个固定版本可以关联训练数据、参数和评价，而production或champion这样的别名指向当前准备提供服务的版本。更新别名就像把路牌移到新房间，房间本身的编号保持不变。MLflow提供了这类版本与别名的组织方式；本例用普通文件展示相同的基本关系。一次预测返回digits-v1，运行程序又能通过manifest核对实际文件，后续出现差异时便有一个明确的起点。

复现还需要说明“相同”比较到哪一层。本例重新载入学生ONNX文件后，450张图片的输出与保存前一致，最大差为0；从PyTorch换到ONNX Runtime，最大logit绝对差约为7.63×10⁻⁶。运算顺序和后端实现可能改变浮点舍入，因此跨后端的检查通常采用事先给定的绝对与相对容差，同时检查类别决策。只保存随机种子无法替代这些比较：拆分、预处理、库版本和权重文件都参与决定最终行为。

$$
|a_i-b_i|\le\epsilon_{\rm abs}+\epsilon_{\rm rel}|b_i|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64807847039db96a4a8ce3ac.svg) | 两个后端对同一样本、同一类别的logit；无量纲。批量输出形状B×10，i遍历全部元素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c5fcad9d6f8a9a1d4ee3d0ec.svg) | 非负绝对与相对容差；此处都无量纲，b为比较基准。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | 绝对值，衡量差值大小而不区分正负方向。 |

绝对容差照顾接近零的输出，相对容差随基准大小变化。取b=2、绝对和相对容差都为10⁻⁵，允许差为3×10⁻⁵；a=2.00002满足条件。全数组逐项通过后，再比较类别。

一个实用的发布包还应带上可重跑的入口和少量有代表性的输入输出。这里完整代码从原始digits数据开始运行，保存全部拆分与模型，并生成一个能检查类别、数值范围和文件身份的例子。之后如果只想做推理，可以直接加载已经生成的ONNX文件，无须重新训练。训练环境和推理环境因此可以分别维护；后者只需保留执行图和接收请求所需的依赖。

## 3 把图片变成接口能够理解的约定

接口不是把一个Python函数换个名字，而是为调用双方建立共同约定。本例接收一个只有pixels字段的JSON对象，内容是1到256行、每行64个数字的二维数组。64个值按照8×8图片的逐行顺序展开，表示尚未归一化的原始灰度。输入必须有限，范围必须在0到16之间。输出包含模型版本、每张图片的预测类别和十个logit。logit是分类前的分数，其大小还需要通过softmax和校准问题来理解。

$$
X=P/16,\qquad H=\operatorname{ReLU}(XW_1+\mathbf b_1),\qquad Z=HW_2+\mathbf b_2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e034ee6fc2f7c49c91499907.svg) | 原始灰度与归一化输入，形状B×64；P以0至16的灰度单位计，X无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2a43927f8ea27ee9dedf59dd.svg) | B为批量样本数；H为B×h隐藏激活，Z为B×10 logits，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a57aa09f24b92830de67d596.svg) | 两层权重与偏置，形状64×h、h、h×10、10；教师h=64，学生h=16，数值无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dfc64c58afee6ca11adda4a.svg) | ReLU逐元素取max(0,x)；16是原始灰度满量程，用于缩放。偏置沿批次广播。 |

一个灰度8先变为0.5；若某隐藏单元只有该位置权重2、偏置−0.2，激活为max(0,0.5×2−0.2)=0.8。原始数组先被调用者除以16，再被图除以16，会把8变为0.03125。

这些要求看起来琐碎，却决定了数学表达式中的每一个数从哪里来。一个数值数组即使形状正确，也可能采用错误的单位：已经缩到0到1的图片仍然落在0到16范围内，范围检查会接受它。若推理图随后再次除以16，图像就被缩小了256倍。在本例中，这种重复归一化把准确率从96.22%降到34.22%。因此契约既要有能执行的形状与范围检查，也要在调用示例中写清单位和处理顺序，并用固定样本比较完整输出。

程序实际启动一个绑定本机地址的短期HTTP服务，发送七次请求，然后关闭服务。两张合法图片得到200响应；错误列数、越界值、文字、非有限值、空批次和错误字段名分别得到400响应。返回200表示请求完成了约定的计算，预测正确与否要再与标签比较。我们把这两类问题分开观察：接口错误率寻找传输和数据约定问题，分类错误率衡量任务表现，响应时间则回答调用者需要等多久。

批推理、在线推理和边缘推理围绕同一计算图，使用方式却不同。夜间一次处理几万张图片，可以积攒大批次，把模型加载和调用成本分摊出去；交互网页需要及时回应单个请求，等待凑齐批次本身也计入延迟；手机或传感器上的边缘推理则关心内存、耗电、网络中断与设备支持的算子。选择运行方式时，先说明输入多久到达一次、答案多久必须返回，以及哪些数据可以留在设备上，再确定批量大小和服务形式。

## 4 导出一张可以检查的计算图

ONNX把模型表示成张量、算子和它们之间的连接。它可以看成一道计算题的详细步骤表：pixels进入Div节点完成除以16，随后进入矩阵乘法和偏置相加，再经过ReLU，最后形成十个输出分数。本例直接用ONNX的图构造接口导出这些节点，因此读者能够逐个核对张量形状。图的批次维采用动态符号，同一文件可以处理1张或128张图片；输入特征维仍固定为64，因为它代表明确的图片排列方式。

把预处理写进图有一个实际好处：调用者传入原始灰度后，每个后端都会经过同一除法节点。若把缩放留在训练脚本里，而发布时只取线性层权重，交付物就丢失了计算的一部分。图检查器会检查节点连接、类型和算子约定，运行时再把图交给指定的执行后端。本例明确选择CPU执行，并把运行线程数固定为1，便于解释后面的测量。更复杂模型可能含有动态控制流、自定义算子或不同形状范围，导出时应为这些路径准备对应输入。

图合法、图能运行、图与原模型等价，是三个依次推进的问题。我们先运行ONNX检查器，再在全部450张测试图片上比较PyTorch与ONNX的logit。最后重新从磁盘加载文件，再比较一次结果。这样的次序很像检查一份电路图：连线符合规则之后，还要上电测量，最后再验证装配好的成品。相同类别也值得继续检查分数，因为轻微输入变化可能把接近边界的样本推向另一类。

本例还保留了一次漏掉归一化的计算。它恰好得到相同的总体准确率96.22%，但最大logit差约为483.77。对于以ReLU为主的网络，整体缩放可能保留不少类别次序，却显著改变分数尺度。这个结果说明为什么发布检查需要同时看数值与任务指标：一个相同的准确率数字，并没有把全部计算行为描述出来。下一节的量化也沿用这种比较，先测误差，再看类别变化和资源代价。

## 5 用更小的模型承担同一项工作

压缩有几种不同的着力点。蒸馏把大模型学到的输出关系传给一个小模型；剪枝让部分连接失去作用；量化把参数存储在更少的数值档位上。它们可以组合，但每一步改变的对象不同。Hinton、Vinyals与Dean在2015年发表的蒸馏论文强调，老师给出的完整类别分布包含比单个正确标签更丰富的信息。例如一张模糊的3同时有一点像8，这种相似关系可以成为学生学习的目标，而不必只收到“答案是3”这一条指令。

$$
p^{(T)}_j=\frac{e^{z^{\rm teacher}_j/T}}{\sum_k e^{z^{\rm teacher}_k/T}},\quad q^{(T)}_j=\frac{e^{z^{\rm student}_j/T}}{\sum_k e^{z^{\rm student}_k/T}},\quad \mathcal L=\alpha(-\log q_y^{(1)})+(1-\alpha)T^2\sum_j p_j^{(T)}\log\frac{p_j^{(T)}}{q_j^{(T)}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c671ba92b071f80f71d8772.svg) | j和k遍历十个类别，y为真实类别索引；计数无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3f7a856793a46b4d4b0ff2ab.svg) | 教师与学生的十维logit及温度化概率向量；教师输出在学生训练时固定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/11b913c202121dc8431c2214.svg) | 正温度与硬标签损失权重；本例T=3、alpha=0.4，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/10b2710f583efc874c9bdc82.svg) | 单样本目标，批次取平均；log为自然对数，损失以nats计。T²补偿温度造成的梯度尺度变化。 |

两类教师分数为(2,0)时，T=1的概率约(0.881,0.119)，T=2时约(0.731,0.269)，次要类别的信息更显著。若学生分布等于教师，KL项为0；硬标签项仍要求把概率分给真实答案。

本例教师有4810个参数，两个学生各有1210个参数。一个学生只学习真实标签，另一个使用温度3，把真实标签交叉熵与教师软目标按0.4和0.6组合。两种学生从相同初始化开始，训练轮数都为300，各自按验证交叉熵选择保存轮次。最终教师准确率为97.11%，两个学生均为96.22%。这个实验展示了蒸馏的实际计算流程，也保留了本次没有提高准确率的结果；教师能力、学生容量、软目标权重和训练时间共同影响它能传递多少有用信息。

剪枝实验从蒸馏学生出发，将两个权重矩阵中绝对值最小的一半置零，共592个权重变为零，偏置保持原样，也没有额外微调。准确率变为95.11%。权重图能够直接显示哪些连接消失；文件大小却仍为5146字节，因为ONNX中保存的还是同样形状的稠密矩阵，零也占一个浮点位置。若要减少实际乘加和内存访问，还要采用可利用稀疏结构的表示与执行方式，或删去整组通道并相应缩小下一层矩阵。

$$
s_j=\max_i|W_{ij}|/127,\quad Q_{ij}=\operatorname{clip}(\operatorname{round}(W_{ij}/s_j),-127,127),\quad \widehat W_{ij}=s_j(Q_{ij}-0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a897ff986da9ea876108627a.svg) | 原权重与反量化权重；i为输入维，j为输出通道。本例权重无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fa530fa6ab8c96f5457e2164.svg) | 每输出通道的正刻度与有符号8位整数；全零通道用极小正刻度避免除零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/23d65448edb24bc1c870044f.svg) | 四舍五入到整数，半整数按NumPy偶数舍入；截到给定区间；对称量化零点为0。 |

一个通道最大绝对权重为1.27时，刻度为0.01。权重0.026映射到整数3，再恢复为0.03，误差0.004。每个通道单独确定刻度，可让小幅值通道也充分使用整数档位。

量化实验采用逐输出通道的对称8位权重存储。每个输出通道先根据最大绝对权重确定刻度，再把数值四舍五入到−127至127的整数档位。图里附带DequantizeLinear节点，用整数、刻度和零点还原参与运算的浮点权重。激活仍为32位浮点数，因此这里称为W8A32。量化文件为1922字节，相比5146字节减少约62.65%；450张测试图的类别全部保持一致，但最大logit差为0.365。完整数值和最终决策提供了两种互补的观察尺度。

![左：同一验证集的交叉熵；中：实际ONNX文件大小和450图准确率，hard与student位置重合；右：学生第一层原权重与全局50%剪枝后的权重，共用颜色范围。剪枝比例针对两层矩阵合计。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b0b8acba4d596d621de476e9.svg?v=b0b8acba4d59)

图 2左：同一验证集的交叉熵；中：实际ONNX文件大小和450图准确率，hard与student位置重合；右：学生第一层原权重与全局50%剪枝后的权重，共用颜色范围。剪枝比例针对两层矩阵合计。

静态激活量化还需要用有代表性的校准输入确定范围，动态量化则在运行中估计部分范围，量化感知训练把舍入效应纳入训练过程。具体后端也会决定这些表示如何执行。本例显式反量化后使用浮点计算，运行时可能折叠常量反量化节点，所以它展示的是权重存储压缩；是否降低运行内存、是否使用整数矩阵核，要进一步检查后端执行计划。将这些问题分别测量，才能把“文件更小”“计算更少”和“响应更快”联系到各自的实际机制。

## 6 测量等待时间，而不只数参数

想象咖啡店收到十杯订单。把十杯一起准备，平均每杯可能更快，但第一位顾客会等得更久。推理服务也有这样的批处理取舍。吞吐量表示单位时间处理多少样本，延迟表示一次调用花多长时间；服务端的排队、输入解析、数据传输和模型计算还会共同组成顾客实际感受到的等待。小模型的矩阵乘法很快，函数调用和调度开销反而可能占据相当比例，因此参数减少四倍，并不意味着单次调用也会快四倍。

$$
\text{throughput}=\frac{B}{\operatorname{median}(t_1,\ldots,t_R)},\qquad t_{95}=\operatorname{quantile}_{0.95}(t_1,\ldots,t_R)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5230febb20293ad37084280.svg) | 一次调用的图像数和重复测量次数；本例B取1/32/128，R=120。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c17639b1b0d2032abf884074.svg) | 第r次调用耗时和95%分位耗时；公式以秒计，图中换成毫秒。 |
| ![Formula](https://ml-biomat.com/static/agent-math/99e21cc7739fc3403e487912.svg) | 中位数与NumPy默认线性插值分位数；吞吐单位为图像/秒。 |

一批32张若中位耗时0.002秒，吞吐为16000张/秒。对有序耗时(1,1,2,2,4)毫秒，线性插值p95位于第4和第5项之间的80%处，为3.6毫秒；不同分位数约定应明确记录。

我们为每个ONNX模型分别测量批次1、32和128的推理调用。每个配置先预热20次，再记录120次调用，输入已经在内存中，运行线程数为1。图中左侧把全部单样本耗时画成累计分布，右侧用批次大小除以调用耗时中位数计算吞吐。这里测量的边界是ONNX Runtime调用，HTTP解析和排队时间在边界之外。读者可以在同一台设备上改变这一边界，把网络请求也包进计时，再比较端到端等待与纯推理时间的差别。

![同一次运行的双语图：每配置预热20次、记录120次，CPU执行、单线程。左为单图调用实测累计分布；右为批量除以耗时中位数。包含ONNX调用开销，输入在内存，不含HTTP与排队。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0ce21f28895199f2aaef3e21.svg?v=0ce21f288951)

图 3同一次运行的双语图：每配置预热20次、记录120次，CPU执行、单线程。左为单图调用实测累计分布；右为批量除以耗时中位数。包含ONNX调用开销，输入在内存，不含HTTP与排队。

p95表示95%的测量值不超过该时间，它关注的是较慢一端的体验。平均值很小的系统，也可能偶尔让用户等待很久。对于本章这样极短的CPU调用，后台任务、缓存和计时粒度都会影响分布，所以图中保留重复测量，而不把一次调用当成稳定速度。量化模型在这次配置中也没有因文件缩小而自动获得更短延迟；反量化、算子融合和调用开销都可能参与其中。更换设备或执行后端后，应重新测量相同输入与批次。

成本可以沿着同样的边界计算。如果服务每秒稳定完成一定请求量，单次请求成本由设备时间、实际利用率、存储和传输共同决定。峰值吞吐不是全天利用率，空闲时段也可能付出设备成本。边缘部署还要观察模型加载时间、持续运行温度和电池消耗。一个有用的比较表应同时放入质量指标、文件大小、运行内存、吞吐和尾部延迟，让应用需求决定哪些指标优先，而不是用参数量替代所有资源问题。

## 7 输入看起来没变，任务也可能已经改变

监测先从数据契约开始：请求是否缺字段，输入是否越界，图片尺寸是否改变。随后可以观察特征分布，例如本例每张图的平均灰度。我们以训练图片作为参考，把灰度分成固定区间，比较新数据落入各区间的比例。人口稳定指数PSI把这种比例变化汇总为一个数。计算时给每个区间加入0.5个平滑计数，再分别归一化，避免某个空区间让对数无法计算。区间边界和平滑方式应固定记录，数值才有可比较的含义。

$$
p_k=\frac{n_k+a}{N+Ka},\quad q_k=\frac{m_k+a}{M+Ka},\qquad \operatorname{PSI}=\sum_{k=1}^{K}(q_k-p_k)\log(q_k/p_k)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e5f01e3334ca6eea7725b3d8.svg) | 直方图区间索引与区间总数；本例0至16按宽度1划分成16格。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96c0c6e9a14b9316d52b1df6.svg) | 参考集与新数据第k格计数、两组总数；本例N=1077，M=450。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d3f9077282c047751278416.svg) | 每格平滑计数a=0.5，归一化后的参考与新数据比例；比例和PSI无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8695a3f226258d2bce68824.svg) | 自然对数，把每个区间的比例变化贡献相加。 |

若两组归一化比例完全相同，每项都为0，PSI=0。两格比例p=(0.5,0.5)、q=(0.75,0.25)时，PSI=0.25log(1.5)−0.25log(0.5)≈0.27465。它只观察所选特征的直方图。

本例准备三种输入：原始测试图、亮度减半的图、旋转90度的图，三组各450张。亮度减半使平均灰度分布明显移动，PSI约12.11，准确率从96.22%变为95.56%。旋转则保留每张图片的全部像素值，只改变它们的位置；因此平均灰度及其PSI与原始图完全相同，准确率却降到9.33%。一种变化在所选统计量上很明显，却只轻微影响本次任务；另一种变化被这个统计量完全忽略，却改变了模型依赖的几何结构。

![三组各450张：原始、亮度减半、旋转90度。上方为同一测试图片，共用0至16灰度；下方亮度直方图中原始实线与旋转虚线重合，右侧准确率则明显不同。](https://ml-biomat.com/static/tutorials/machine-learning/figures/c77275da51770cade0df25f2.svg?v=c77275da5177)

图 4三组各450张：原始、亮度减半、旋转90度。上方为同一测试图片，共用0至16灰度；下方亮度直方图中原始实线与旋转虚线重合，右侧准确率则明显不同。

这组对照帮助我们把数据变化、概念变化和任务退化分开理解。数据漂移关注输入分布是否变化；如果相同输入对应的真实答案规律发生变化，问题还涉及条件关系。仅观察输入时，可以及时发现许多格式、设备和采集变化；标签到达以后，才能计算准确率、分组错误和实际成本。对贷款违约、设备寿命等任务，标签可能很晚才出现，监测面板应显示已回流标签的数量与覆盖时段，而不是把尚未观察到错误理解成没有错误。

阈值应结合稳定时期的波动、样本量和处理成本来设定。PSI没有跨任务通用的一条报警线；不同分箱、不同特征及不同参考样本都会改变它。真正触发信号后，还要沿输入、模型版本和人群分组继续定位：是图片方向变了、某一类样本增加了，还是新版本对某些样本更差？补采有代表性的标签、对变化最明显的分组重新评价，再决定更新预处理、校准阈值或重新训练，才能让监测结果进入下一步改进。

## 8 逐步替换版本，让反馈形成下一轮实验

新模型通过离线评价后，可以先在影子模式下处理相同请求，保留旧模型的实际回答，比较两者输出和计算成本。灰度发布再把一部分请求交给新版本，逐步扩大范围；回滚则把后续请求重新指向已保存的旧版本。它们解决的是不同阶段的问题。影子模式观察候选计算行为，灰度发布观察新版本参与实际流程后的结果，回滚缩短问题继续影响后续请求的时间。已经产生的回答和后续业务动作还需要单独记录和处理。

下面把450张固定测试图片当作依次到达的请求，每批50张。旧版本为教师模型，候选可以选择学生、8位权重版本、剪枝版本或重复归一化版本。路由按固定的请求编号分配，比例变化会改变实际进入候选的样本。标签延迟决定最近几批的答案何时可见；你可以先观察放量，再等标签回流，比较相同已标注请求在候选与旧版本下的差异。所有预测都来自上面的真实运行，交互只重放这些输出，不会在浏览器中重新训练。

### 把真实预测放进一次灰度发布

每批50张，旧版本为教师模型。调整比例只影响后续请求；改变候选或标签延迟会开始新实验。先处理几批，再回滚，观察历史请求与后续路由的区别。

[Figure: 真实请求路由和延迟标签重放](https://ml-biomat.com/tutorials/machine-learning/m27/#M27-plot)

这个小实验适合手算路由与评价口径：候选样本很少时，一个错误就会使比例跳动；标签尚未返回时，应该先看请求和运行状态；回滚后，后续请求转回旧模型，历史结果仍保留。实际灰度设计还需要让分流与用户群体、重复访问和业务反馈相匹配，必要时按用户而非单次请求保持分组。若边观察边不断试探阈值，还应预先规定评价窗口和停止规则，避免把偶然波动当成稳定改进。

持续训练把新收集的数据带回训练流程，持续学习则进一步涉及模型如何吸收新知识并保留旧能力。两者都需要新的评价安排：新标签先完成质量检查，训练与评价按时间或群体分开，更新后同时观察新工况和重要旧工况。推荐系统尤其容易形成反馈回路，因为模型决定展示什么，而展示又决定能收集到什么点击。保留适当的探索、记录曝光机制，并补充独立评价，可以帮助下一轮训练理解数据是怎样产生的。

### 从训练到本地预测服务的完整程序

安装numpy、torch、onnx、onnxruntime、scikit-learn和matplotlib，运行python main.py --output results --language zh。再运行python main.py --serve results --port 8765，向本机/predict发送pixels二维数组；Ctrl+C结束。主实验会自行关闭契约检查用的临时服务。

```
"""A complete local model release: training, compression, ONNX, HTTP and monitoring.
Run: python main.py --output results --language en
Serve a previously generated bundle: python main.py --serve results --port 8765
"""
from pathlib import Path
import argparse, copy, hashlib, importlib.metadata, json, platform, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen, build_opener, ProxyHandler
from urllib.error import HTTPError
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import onnx
from onnx import helper, numpy_helper, TensorProto
import onnxruntime as ort
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Network(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.fc1 = nn.Linear(64, width)
        self.fc2 = nn.Linear(width, 10)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


def fit(width, x, y, xv, yv, teacher=None):
    torch.manual_seed(270 + width)
    model = Network(width)
    optimizer = torch.optim.Adam(model.parameters(), lr=.01)
    history, best, chosen = [], float('inf'), 0
    teacher_logits = None if teacher is None else teacher(x).detach()
    for epoch in range(300):
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        if teacher is not None:
            temperature = 3.
            soft = F.kl_div(F.log_softmax(logits / temperature, dim=1),
                            F.softmax(teacher_logits / temperature, dim=1), reduction='batchmean')
            loss = .4 * loss + .6 * temperature ** 2 * soft
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        with torch.no_grad():
            validation = F.cross_entropy(model(xv), yv).item()
        history.append([float(loss.detach()), validation])
        if validation < best:
            best, chosen, state = validation, epoch + 1, copy.deepcopy(model.state_dict())
    model.load_state_dict(state); model.eval()
    return model, np.array(history), chosen


def export_graph(model, path):
    # The raw-pixel /16 transform travels inside the inference graph.
    arrays = {'scale': np.array(16, dtype=np.float32),
              'w1': model.fc1.weight.detach().numpy().T.copy(),
              'b1': model.fc1.bias.detach().numpy(),
              'w2': model.fc2.weight.detach().numpy().T.copy(),
              'b2': model.fc2.bias.detach().numpy()}
    nodes = [helper.make_node('Div', ['pixels', 'scale'], ['scaled']),
             helper.make_node('MatMul', ['scaled', 'w1'], ['m1']),
             helper.make_node('Add', ['m1', 'b1'], ['a1']),
             helper.make_node('Relu', ['a1'], ['hidden']),
             helper.make_node('MatMul', ['hidden', 'w2'], ['m2']),
             helper.make_node('Add', ['m2', 'b2'], ['logits'])]
    graph = helper.make_graph(nodes, 'digits-release',
        [helper.make_tensor_value_info('pixels', TensorProto.FLOAT, ['batch', 64])],
        [helper.make_tensor_value_info('logits', TensorProto.FLOAT, ['batch', 10])],
        [numpy_helper.from_array(v, name=k) for k, v in arrays.items()])
    model_proto = helper.make_model(graph, opset_imports=[helper.make_opsetid('', 18)])
    model_proto.ir_version = 10
    onnx.checker.check_model(model_proto)
    onnx.save(model_proto, path)


def session(path):
    settings = ort.SessionOptions()
    settings.intra_op_num_threads = 1; settings.inter_op_num_threads = 1
    return ort.InferenceSession(str(path), settings, providers=['CPUExecutionProvider'])


def quantize_weights(source, destination):
    """Store signed8-bit weights per output channel, with explicit dequantization.

    Activations remain float32; this graph demonstrates W8A32 storage.
    Execution providers may fold constant dequantization back into float matrices.
    """
    graph_model = onnx.load(source)
    additions, replacements = [], []
    for tensor in list(graph_model.graph.initializer):
        if tensor.name not in ['w1', 'w2']:
            continue
        weight = numpy_helper.to_array(tensor)
        scale = np.maximum(np.abs(weight).max(axis=0) / 127, 1e-12).astype(np.float32)
        quantized = np.clip(np.rint(weight / scale), -127, 127).astype(np.int8)
        name = tensor.name
        replacements.extend([numpy_helper.from_array(quantized, name + '_q'),
                             numpy_helper.from_array(scale, name + '_scale'),
                             numpy_helper.from_array(np.zeros(scale.shape, np.int8), name + '_zero')])
        additions.append(helper.make_node('DequantizeLinear',
                         [name + '_q', name + '_scale', name + '_zero'], [name], axis=1))
        graph_model.graph.initializer.remove(tensor)
    graph_model.graph.initializer.extend(replacements)
    original_nodes = list(graph_model.graph.node)
    del graph_model.graph.node[:]
    graph_model.graph.node.extend(additions + original_nodes)
    onnx.checker.check_model(graph_model)
    onnx.save(graph_model, destination)


def predict(sess, payload):
    if not isinstance(payload, dict) or set(payload) != {'pixels'}:
        raise ValueError('Expected one field: pixels')
    raw = np.asarray(payload['pixels'])
    if raw.ndim != 2 or raw.shape[1] != 64 or not 1 <= raw.shape[0] <= 256:
        raise ValueError('pixels must have shape [1..256,64]')
    if raw.dtype.kind not in 'fiu' or not np.isfinite(raw).all():
        raise ValueError('pixels must contain finite numbers')
    if raw.min() < 0 or raw.max() > 16:
        raise ValueError('Raw pixel range is 0..16')
    logits = sess.run(None, {'pixels': raw.astype(np.float32)})[0]
    return {'version': 'digits-v1', 'classes': logits.argmax(1).tolist(),
            'logits': logits.tolist()}


def handler(sess):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # No request features are written to a log.

        def do_POST(self):
            try:
                if self.path != '/predict':
                    self.send_error(404); return
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 1000000:
                    raise ValueError('Invalid request size')
                result = predict(sess, json.loads(self.rfile.read(length)))
                code = 200
            except (ValueError, TypeError, OverflowError):
                result, code = {'error': 'Request does not match the pixel contract'}, 400
            data = json.dumps(result, allow_nan=False).encode()
            self.send_response(code); self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
    return Handler


def http_checks(sess, sample):
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler(sess))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    client = build_opener(ProxyHandler({})); records = []
    payloads = [{'pixels': sample.tolist()}, {'pixels': [[0] * 63]},
                {'pixels': [[17] * 64]}, {'pixels': [['zero'] * 64]},
                {'pixels': [[float('nan')] * 64]}, {'pixels': []}, {'image': sample.tolist()}]
    try:
        for payload in payloads:
            request = Request(f'http://127.0.0.1:{server.server_port}/predict',
                              json.dumps(payload).encode(), {'Content-Type': 'application/json'})
            try:
                with client.open(request, timeout=10) as response:
                    code, body = response.status, json.loads(response.read())
            except HTTPError as error:
                code, body = error.code, json.loads(error.read())
            records.append({'status': code, 'body': body})
    finally:
        server.shutdown(); server.server_close(); thread.join()
    assert [r['status'] for r in records] == [200, 400, 400, 400, 400, 400, 400]
    assert records[0]['body']['classes'] == predict(sess, payloads[0])['classes']
    return records


def psi(reference, current, edges):
    p = np.histogram(reference, edges)[0].astype(float) + .5
    q = np.histogram(current, edges)[0].astype(float) + .5
    p /= p.sum(); q /= q.sum()
    return float(np.sum((q - p) * np.log(q / p)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results')
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    parser.add_argument('--serve', type=Path); parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if args.serve:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler(session(args.serve / 'student.onnx')))
        print(f'Local prediction endpoint: http://127.0.0.1:{args.port}/predict', flush=True)
        try: server.serve_forever()
        except KeyboardInterrupt: pass
        finally: server.server_close()
        return
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'; tr = lambda z, e: z if zh else e
    torch.set_num_threads(1); torch.manual_seed(271); np.random.seed(271)
    data = load_digits(); pixels = data.data.astype(np.float32); labels = data.target
    development, test = train_test_split(np.arange(len(labels)), test_size=450, stratify=labels, random_state=271)
    train, validation = train_test_split(development, test_size=270, stratify=labels[development], random_state=272)
    tensor = lambda ids: torch.from_numpy(pixels[ids] / 16)
    target = lambda ids: torch.from_numpy(labels[ids])
    teacher, ht, et = fit(64, tensor(train), target(train), tensor(validation), target(validation))
    hard, hh, eh = fit(16, tensor(train), target(train), tensor(validation), target(validation))
    student, hs, es = fit(16, tensor(train), target(train), tensor(validation), target(validation), teacher)
    pruned = copy.deepcopy(student)
    weights = torch.cat([pruned.fc1.weight.flatten(), pruned.fc2.weight.flatten()])
    threshold = torch.quantile(weights.abs(), .5)
    with torch.no_grad():
        for layer in [pruned.fc1, pruned.fc2]: layer.weight.mul_(layer.weight.abs() > threshold)
    models = {'teacher': teacher, 'hard': hard, 'student': student, 'pruned': pruned}
    for name, model in models.items():
        export_graph(model, out / f'{name}.onnx')
        torch.save(model.state_dict(), out / f'{name}.pt')
    quantize_weights(out / 'student.onnx', out / 'int8.onnx')
    sessions = {name: session(out / f'{name}.onnx') for name in [*models, 'int8']}
    raw = pixels[test]; truth = labels[test]
    logits = {name: sess.run(None, {'pixels': raw})[0] for name, sess in sessions.items()}
    with torch.no_grad():
        export_error = float(np.abs(logits['student'] - student(tensor(test)).numpy()).max())
        logits['wrong_scale'] = student(torch.from_numpy(raw)).numpy()
    logits['double_scale'] = sessions['student'].run(None, {'pixels': raw / 16})[0]
    predictions = {name: value.argmax(1) for name, value in logits.items()}
    accuracy = {name: float((prediction == truth).mean()) for name, prediction in predictions.items()}
    timings = {}
    for name, sess in sessions.items():
        timings[name] = {}
        for batch in [1, 32, 128]:
            feed = {'pixels': raw[:batch]}
            for _ in range(20): sess.run(None, feed)
            elapsed = []
            for _ in range(120):
                start = time.perf_counter_ns(); sess.run(None, feed)
                elapsed.append((time.perf_counter_ns() - start) / 1e6)
            timings[name][str(batch)] = elapsed
    contracts = http_checks(sessions['student'], raw[:2])
    # Rotation preserves each image's mean brightness exactly but changes its geometry.
    streams = {'clean': raw, 'dimmed': raw * .5,
               'rotated': np.rot90(raw.reshape(-1, 8, 8), k=1, axes=(1, 2)).reshape(-1, 64).copy()}
    edges = np.linspace(0, 16, 17); baseline = pixels[train].mean(1)
    drift = {}
    for name, value in streams.items():
        pred = sessions['student'].run(None, {'pixels': value})[0].argmax(1)
        drift[name] = {'psi_mean_brightness': psi(baseline, value.mean(1), edges),
                       'accuracy': float((pred == truth).mean())}
    model_files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.onnx')}
    manifest = {'version': 'digits-v1', 'data_sha256': hashlib.sha256(pixels.tobytes() + labels.tobytes()).hexdigest(),
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'split': {'train': train.tolist(), 'validation': validation.tolist(), 'test': test.tolist()},
                'schema': {'field': 'pixels', 'shape': ['batch<=256', 64], 'range': [0, 16],
                           'order': '8x8 row-major', 'transform': 'divide by16 inside ONNX'},
                'versions': {n: importlib.metadata.version(n) for n in ['numpy', 'torch', 'onnx', 'onnxruntime', 'scikit-learn']},
                'python': platform.python_version(), 'models': model_files, 'evaluation': accuracy}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
    # Reload from the written file and verify both identity and prediction parity.
    restored = json.loads((out / 'manifest.json').read_text(encoding='utf8'))
    for name, expected in restored['models'].items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == expected
    replay = session(out / 'student.onnx').run(None, {'pixels': raw})[0]
    reload_error = float(np.abs(replay - logits['student']).max())
    summary = {'samples': len(labels), 'train': len(train), 'validation': len(validation), 'test': len(test),
        'selected_epochs': {'teacher': et, 'hard': eh, 'student': es}, 'accuracy': accuracy,
        'onnx_max_logit_error': export_error, 'reload_error': reload_error,
        'int8_max_logit_error': float(np.abs(logits['int8'] - logits['student']).max()),
        'wrong_scale_max_logit_error': float(np.abs(logits['wrong_scale'] - logits['student']).max()),
        'int8_changed_predictions': int(np.count_nonzero(predictions['int8'] != predictions['student'])),
        'parameters': {name: sum(p.numel() for p in model.parameters()) for name, model in models.items()},
        'pruned_weight_zeros': sum(int((layer.weight == 0).sum()) for layer in [pruned.fc1, pruned.fc2]),
        'total_weights': len(weights), 'onnx_bytes': {name: (out / f'{name}.onnx').stat().st_size for name in sessions},
        'contract_statuses': [r['status'] for r in contracts], 'monitoring': drift,
        'timing_ms': {name: {batch: {'median': float(np.median(t)), 'p95': float(np.quantile(t, .95)),
                       'throughput': int(batch) * 1000 / float(np.median(t))} for batch, t in values.items()} for name, values in timings.items()}}
    np.savez_compressed(out / 'experiment.npz', train=train, validation=validation, test=test, labels=truth,
                        pixels=raw, teacher_history=ht, hard_history=hh, student_history=hs,
                        **{'logits_' + k: v for k, v in logits.items()},
                        **{'timing_' + k + '_' + b: np.array(t) for k, a in timings.items() for b, t in a.items()})
    (out / 'replay.json').write_text(json.dumps({'labels': truth.tolist(), 'predictions': {k: v.tolist() for k, v in predictions.items()}}), encoding='utf8')
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    for language in ['zh', 'en']:
        zh = language == 'zh'
        plt.rcParams.update({'font.family': ['Microsoft YaHei', 'DejaVu Sans'], 'font.size': 11,
                             'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False,
                             'figure.facecolor': '#faf8f3', 'axes.facecolor': '#faf8f3'})
        colors = ['#1b4660', '#897d68', '#1c8282', '#bd7049', '#77649b']
        def save(fig, name):
            fig.savefig(out / f'{name}-{language}.svg', bbox_inches='tight')
            fig.savefig(out / f'{name}-{language}.png', dpi=150, bbox_inches='tight'); plt.close(fig)
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), layout='constrained')
        for h, name, color in zip([ht, hh, hs], ['teacher', 'hard', 'student'], colors):
            axes[0].plot(np.arange(1, 301), h[:, 1], label=name, color=color)
        axes[0].set(xlabel=tr('训练轮数', 'Training epoch'), ylabel=tr('验证交叉熵 / nats', 'Validation cross entropy / nats')); axes[0].legend(frameon=False)
        for i, name in enumerate(sessions):
            axes[1].scatter(summary['onnx_bytes'][name] / 1024, accuracy[name], s=70, color=colors[i])
            if name != 'student':
                offsets = {'teacher': (-35, 14), 'hard': (-35, 22), 'pruned': (-20, -24), 'int8': (0, 14)}
                axes[1].annotate('hard / student' if name == 'hard' else name, (summary['onnx_bytes'][name] / 1024, accuracy[name]), xytext=offsets[name], textcoords='offset points', arrowprops={'arrowstyle': '-', 'color': '#7c898e'})
        axes[1].set(xscale='log', xlabel=tr('ONNX文件 / KiB', 'ONNX file / KiB'), ylabel=tr('450张测试准确率', 'Accuracy on 450 test images'), ylim=(.93, 1.005))
        original = student.fc1.weight.detach().numpy(); sparse = pruned.fc1.weight.detach().numpy()
        im = axes[2].imshow(np.concatenate([original, sparse], axis=0), cmap='RdBu_r', vmin=-abs(original).max(), vmax=abs(original).max(), aspect='auto')
        fig.colorbar(im, ax=axes[2], label=tr('权重 / 无量纲', 'Weight / dimensionless'))
        axes[2].axhline(15.5, color='#253d4a'); axes[2].set(xlabel=tr('输入像素编号', 'Input pixel index'), yticks=[7.5, 23.5], yticklabels=['student', '50% zeros'], title=tr('同一矩阵：上原始、下剪枝', 'Same matrix: original / pruned'))
        save(fig, 'compression')
        fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
        for i, name in enumerate(sessions):
            t = np.sort(timings[name]['1']); axes[0].plot(t, np.arange(1, 121) / 120, label=name, color=colors[i])
            medians = [np.median(timings[name][str(b)]) for b in [1, 32, 128]]
            axes[1].plot([1, 32, 128], np.array([1, 32, 128]) * 1000 / medians, 'o-', label=name, color=colors[i])
        axes[0].set(xlabel=tr('单次推理 / ms', 'Inference call / ms'), ylabel=tr('实测累计比例', 'Empirical cumulative fraction'), xscale='log'); axes[0].legend(frameon=False)
        axes[1].set(xlabel=tr('批量大小', 'Batch size'), ylabel=tr('吞吐 / 图像每秒', 'Throughput / images per second'), xscale='log', yscale='log'); axes[1].legend(frameon=False)
        save(fig, 'latency')
        fig = plt.figure(figsize=(12, 6.5), layout='constrained'); gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.6])
        for i, (name, value) in enumerate(streams.items()):
            ax = fig.add_subplot(gs[0, i]); ax.imshow(value[0].reshape(8, 8), cmap='gray_r', vmin=0, vmax=16); ax.set_title(name); ax.axis('off')
        ax = fig.add_subplot(gs[1, :2])
        for i, (name, value) in enumerate(streams.items()): ax.hist(value.mean(1), bins=edges, histtype='step', linewidth=4 if name == 'clean' else 2, linestyle='--' if name == 'rotated' else '-', label=name, color=colors[i])
        ax.set(xlabel=tr('每张图片的平均灰度', 'Mean intensity per image'), ylabel=tr('样本数', 'Image count')); ax.legend(frameon=False)
        ax = fig.add_subplot(gs[1, 2]); names = list(streams)
        ax.bar(names, [drift[n]['accuracy'] for n in names], color=colors[:3]); ax.set(ylim=(0, 1.08), ylabel=tr('标签到达后：准确率', 'After labels arrive: accuracy'))
        for i, n in enumerate(names): ax.text(i, drift[n]['accuracy'] + .025, f"{drift[n]['accuracy']:.3f}", ha='center')
        save(fig, 'monitoring')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
```

运行完整程序后，输出目录包含五个ONNX版本、对应训练权重、版本清单、实际预测与计时数组、重放数据和全部图像。使用serve选项可以再次启动本机预测接口，按相同JSON约定调用。把这个小服务迁移到实际应用时，可以依次加入鉴权、资源限额、并发与排队测量、故障恢复和业务反馈关联，每增加一项都说明它解决什么问题，并给出能观察其行为的例子。这样，部署过程就成为一组可以解释和重复的实验，而不只是复制一个权重文件。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M27.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Sculley et al. (2015), Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/)

   从模型分数扩展到数据、配置和系统依赖。

   Primary paper reference; no reproduced figure.
2. [Breck et al. (2017), The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

   数据、模型、基础设施和监测的测试思路。

   Primary paper reference; original teaching diagram.
3. [Hinton, Vinyals & Dean (2015), Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)

   温度软目标与学生网络。

   Paper referenced; all experiments newly computed.
4. [ONNX — Python introduction](https://onnx.ai/onnx/intro/python.html)

   用节点、张量和动态批次组成可交换推理图。

   Apache-2.0 project; conceptual reference.
5. [ONNX — DequantizeLinear](https://onnx.ai/onnx/operators/onnx__DequantizeLinear.html)

   逐通道量化参数、轴和反量化定义。

   Apache-2.0 project; original implementation.
6. [ONNX Runtime — Quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)

   区分权重量化、激活精度、校准及执行后端。

   MIT project; technical reference.
7. [PyTorch — Pruning tutorial](https://docs.pytorch.org/tutorials/intermediate/pruning_tutorial.html)

   权重掩码、结构化与非结构化剪枝。

   BSD-3-Clause documentation/code; no figure copied.
8. [MLflow — Model Registry](https://mlflow.org/docs/latest/registry/)

   固定版本与可变别名的工作关系。

   Apache-2.0 project; no MLflow server needed for the example.
9. [TensorFlow Data Validation](https://www.tensorflow.org/tfx/guide/tfdv)

   输入契约、训练服务偏差与分布漂移。

   CC BY4.0 documentation; original figures.
10. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

    1797张8×8手写数字、0至16灰度及数据出处。

    UCI Optical Recognition of Handwritten Digits; see dataset terms.
