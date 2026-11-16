# 标签不够时怎样学习：表示、提问与记忆

Source: https://ml-biomat.com/tutorials/machine-learning/m11/
Language: zh-CN

从同一张照片的两种视图出发，学会安排无标签训练、人工标注、新任务适应与旧知识回放。

## 照片很多，答案很少：学习从哪里开始

整理一万张照片，最费时间的往往不是保存文件，而是逐张写下“这里有什么”。给一封邮件判断类别只需几秒，给显微图标出所有细胞却可能需要很久。机器学习因此面对两种不同的资源：我们能收集多少输入，以及我们能为多少输入提供可靠答案。如果把两者混成“数据量”，很容易错过一个机会：即使不知道照片的类别，模型仍能观察其中的边缘、形状和变化规律。本章讨论怎样利用这些规律，并把有限的人工判断花在合适的位置。

先把几条路线放进同一个场景。模型从照片自身构造学习题目，叫自监督学习；用少量有标签照片加大量无标签照片训练分类器，属于半监督学习；由模型挑出最值得请人回答的照片，是主动学习。它们可以接在一起：先学表示，再请人标注，再更新分类器。相反，“弱监督”强调答案的可靠程度，例如关键词规则、历史记录或粗粒度标签带来的近似答案。区分这些名称，最直接的方法是追问：这一轮更新的监督信号是谁提供的，它具体要求模型预测什么？

2020年的SimCLR把图像增强、表示网络和对比目标组合成清楚的实验框架；同年的BYOL探索没有显式负样本的表示学习，2021年的MAE则让模型从可见图块恢复被遮住的内容。这些工作把“先理解输入，再学习任务”推进成了可以比较的训练方法。下面的公开教程原图展示了一个实际问题：随着标签预算增加，学好的表示能够支持怎样的分类结果。读图时先看横轴每类图像数量，再沿曲线观察识别准确率；随后我们用更小的手写数字实验，把训练、选样和遗忘过程逐步打开。

![STL10标签预算与分类表现的原教程实验，横轴为每类训练样本数，曲线给出SimCLR表示上分类器的测试准确率；此图的数据和模型属于原教程。Phillip Lippe，UvA Deep Learning Tutorials，Tutorial 17，代码单元\[18\]输出，MIT，未改动；本章手写数字结果见后续图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3e35017595ab122ddb2bbc46.svg?v=3e35017595ab)

图 1STL10标签预算与分类表现的原教程实验，横轴为每类训练样本数，曲线给出SimCLR表示上分类器的测试准确率；此图的数据和模型属于原教程。Phillip Lippe，UvA Deep Learning Tutorials，Tutorial 17，代码单元[18]输出，MIT，未改动；本章手写数字结果见后续图。

## 表示空间：把相似性变成能计算的距离

一张8×8的灰度图可以写成64个数字，可是“两个数组接近”未必等于“两个数字写得像”。同一个笔画向右移动一个像素，许多位置都会发生变化；两个不同数字却可能共享大片背景。表示网络尝试重新组织这些信息，把输入变成较短的向量，使后续任务更容易读取有用结构。可以把它理解为重新编排图书馆：原始像素像按书页纸张颜色排书，好的表示则逐渐把内容相关的书放到附近。分类器随后在这个书架上划分类别，表示网络本身不必已经知道最终书架名称。

本章编码器把64维输入变成32维向量。比较方向时，先除以向量长度，再做内积；这样一个向量整体放大两倍不会改变相似度。这个选择把长度信息从比较中拿走，适合我们关注笔画结构的任务。若向量长度本来代表置信度、强度或某种物理量，归一化就会改变问题，需要根据用途决定。零向量没有方向，实际代码用库的数值稳定实现处理极小长度。表示的每一维通常没有现成的名称，维度之间共同编码信息，因此不能把第七维直接叫作“圆圈程度”。

$$
\widehat h=\frac{h}{\|h\|_2},\qquad s(h,g)=\widehat h^{\mathsf T}\widehat g
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6d2cac1d7937c055c2fc3fad.svg) | 两个输入的d维表示向量，本章d=32；坐标无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86a6ff610030486a41b7d0b1.svg) | 向量的欧氏长度；j是坐标索引，非零向量才能直接使用此除法。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0cf8e03c42a61e2ae1cdb0d.svg) | 长度为1的归一化向量，形状与原表示相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/04ad2f8aaa01d02353cfeba2.svg) | 余弦相似度及转置记号；s无量纲，范围−1至1。 |

h=(0.6,0.8)、g=(0,1)的长度均为1，内积为0.6×0+0.8×1=0.8。把h改成(1.2,1.6)，其长度变成2，归一化后仍得同一结果。内积通过坐标乘积相加衡量方向对齐程度；反向为−1、正交为0、同向为1。

学好表示之后，有三种常用读法。冻结编码器、只训练线性分类头，可以观察现有表示怎样支持类别分离；把编码器一起更新，叫微调；直接比较与少量示例的距离，则可以做检索或原型分类。迁移学习发生在表示或参数从一个学习阶段流向另一个任务时，两个阶段的监督形式可以不同。我们会把同样的50个标签交给原始像素、随机初始化表示和对比学习表示上的线性分类器，保持标注预算一致。这样才能分清“见过更多无标签输入”与“使用了更多人工答案”。

## 对比学习：同一张图为什么要看两遍

对比学习先制造一对观察。对同一张数字图独立加上轻微噪声、遮去少量像素，得到视图A和视图B；它们的来源相同，构成正样本对。一个批次里其他原图的视图作为候选负样本。网络看到A时，要从候选中找回对应的B。这里的标签不是“这张图是8”，而是“这两张图来自同一个输入”。增强规定了模型应忽略哪些变化：轻微噪声可以忽略，若把6旋转成9还强迫它们一致，就会教错任务。先查看增强图，比直接追求更低的损失更有帮助。

![同十张训练图的原图与两次独立增强。强度统一为0–1，噪声标准差0.08，像素以0.15概率置零。数字标题只用于读图，未送入对比训练。原图数据：E. Alpaydin、C. Kaynak，UCI，CC BY 4.0。](https://ml-biomat.com/static/tutorials/machine-learning/figures/65ccbbea0bd3e3a69286787b.svg?v=65ccbbea0bd3)

图 2同十张训练图的原图与两次独立增强。强度统一为0–1，噪声标准差0.08，像素以0.15概率置零。数字标题只用于读图，未送入对比训练。原图数据：E. Alpaydin、C. Kaynak，UCI，CC BY 4.0。

编码器后面还有一个投影头，把32维表示变成16维向量，再归一化。投影头专门服务于对比目标，后续分类读取编码器输出。这样，输入信息不必全部按照对比目标在同一个空间里压缩。每个批次含128张原图时，一共产生256个视图；对一个锚点，排除它自己后有255个候选，其中只有一个配对正样本。小批次末尾的候选数量随实际样本数变化，代码据此构造目标位置。正确配对在候选分布中的概率越高，损失越小，这就是下面对比目标的计算思路。

$$
\ell_i=-\log\frac{\exp(s_{i,p(i)}/\tau)}{\sum_{k\ne i}^{2B}\exp(s_{ik}/\tau)},\qquad L=\frac1{2B}\sum_{i=1}^{2B}\ell_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4b3e0810d86961c413c0d22d.svg) | 原图批量、由两次增强产生的视图总数；最后一批按实际B计算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eee47ba016d4b0ec84f4b688.svg) | 锚点索引、候选索引、锚点对应的另一个视图索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96e5c22b3bf6f2ac2a0feadc.svg) | 第i与第k个归一化投影的余弦相似度，无量纲；投影为16维。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa8e2e336dcfa0bdaadf756.svg) | 温度，本例0.2，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc3c3e662e2bd7210059aba7.svg) | 单锚点损失、所有视图平均损失、自然指数、自然对数；损失以nats计。 |

排除自己避免把“找到原向量”当成学习任务。若B=2，共4个视图，某锚点的3个候选相似度相同，则正样本概率为1/3，损失ln3≈1.09861。若正样本相似度1、另外两个为0，温度1，概率e/(e+2)，损失约0.55144。每个视图都轮流做锚点，平均后两种增强对称地参与训练。

温度控制相似度差异进入概率时被放大多少。温度较小时，相似度稍高的候选会占据更大权重，错误近邻的影响也更突出。负样本还带来一个有趣的矛盾：两张不同的“8”在当前目标里属于负样本，尽管未来分类时希望把它们归为一类。实例区分与类别识别不是同一任务，因此我们既看损失，也看后续有标签任务。图中的相似度矩阵把十对视图摆在两轴，对角线是配对关系；二维投影只用于查看32维表示的部分结构，颜色来自测试标签，没有参与无标签训练。

![A：真实80轮平均对比损失。B：十对视图的余弦相似度，两个轴的同一编号来自同一原图。C：360张测试图的32维编码器输出投影到两个主成分，投影轴由训练表示拟合；颜色为测试真值，仅用于展示。](https://ml-biomat.com/static/tutorials/machine-learning/figures/162fb3a13b506d28a8012c00.svg?v=162fb3a13b50)

图 3A：真实80轮平均对比损失。B：十对视图的余弦相似度，两个轴的同一编号来自同一原图。C：360张测试图的32维编码器输出投影到两个主成分，投影轴由训练表示拟合；颜色为测试真值，仅用于展示。

## 补缺口、跟老师学、使用不完整的答案

对比学习靠“找同伴”组织表示，掩码建模则靠“补缺口”。把图像分成小块，隐藏一部分，只让编码器读取可见块，再由解码器根据表示和位置恢复隐藏内容。MAE的一个重要设计是把计算量较大的编码器用于可见块，把补全任务交给较轻的解码器。文字中的掩码建模也采用类似思路，只是预测对象变为离散词元。关键不在遮挡动作本身，而在隐藏内容是否必须借助上下文才能猜到；如果答案能直接从输入复制，模型学不到我们期待的依赖关系。

$$
L_{\mathrm{mask}}=\frac1{|M|}\sum_{j\in M}(\widehat x_j-x_j)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3338e5ecd5025495beebe602.svg) | 隐藏位置j的真实像素强度与预测强度；本例均归一化为无量纲值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e7fd209208b840d9771c9d72.svg) | 被隐藏的位置集合及其元素数；本式假定至少一个位置被遮挡。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2dd22608cd95890d21973e89.svg) | 只在隐藏位置求平均的平方误差，单位是归一化强度的平方。 |

隐藏的两项真实值为(0.2,0.8)，预测为(0.3,0.6)，误差平方是0.01和0.04，平均0.025。可见位置不进入这里的损失，避免大量容易复制的位置主导目标。真实MAE按图块恢复像素；公式用像素索引展开同样的计算。隐藏标记需要与真实零强度区分。

自蒸馏提供另一种监督：同一模型的另一个版本充当老师。以BYOL为例，在线网络读取一个视图，经过预测头，去接近目标网络对另一个视图给出的表示；目标分支停止接收这项损失的梯度，其参数随在线网络做缓慢的移动平均。老师因此不会在每一步追着学生的最新噪声跳动。若所有图像都输出同一个向量，表面上也能保持一致，这叫表示坍塌。预测头、分支的不对称更新以及归一化等设计共同影响训练，不能把“停止梯度”四个字当成任何结构都不会坍塌的保证。实际使用时，要同时检查不同输入的表示差异和下游任务。

$$
\xi\leftarrow m\xi+(1-m)\theta_{\mathrm{ep}},\qquad L_{\mathrm{distill}}=\|\widehat q_\theta(v_1)-\operatorname{sg}(\widehat z_\xi(v_2))\|_2^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/82b55e8ce69542eb61b08c56.svg) | θ为在线网络全部可训练参数，ξ为目标编码器与投影头参数；目标分支没有预测头。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0030058cb275aaad3114e821.svg) | 在线参数中与目标对应的编码器和投影头部分，只有这部分进入移动平均；预测头仅在线接受梯度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8673ecb2a5bdfceacd858b53.svg) | 目标更新动量；越接近1，单次更新越慢。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0315e8b8aea066fef3c4e73d.svg) | 同一原始输入的两个增强视图。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2465c23fdfd871da565282f3.svg) | 在线预测头输出与目标表示，均归一化为同维度单位向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/92e7a9bd6c7eaacb185459e8.svg) | 停止梯度操作与单方向蒸馏平方距离；无量纲。 |

某个目标参数为0.2、在线参数为0.6、m=0.9，更新后为0.24。若两个单位输出为(1,0)和(0.8,0.6)，平方距离为0.2²+0.6²=0.4。停止梯度使目标值参与比较而不接收该损失的反向更新；完整BYOL还交换两个视图计算另一方向。

当已经有少量人工标签时，半监督学习可以让分类目标直接参与。FixMatch先对无标签输入做弱增强，若预测足够自信，就把最高概率类别作为伪标签，再要求强增强后的输入预测一致。比如弱视图输出(0.92,0.08)，阈值0.9会接受第一类；若输出(0.58,0.42)，本轮就不使用这条伪标签。阈值筛选改变的是参与训练的样本集合，置信度仍需结合验证数据理解。本章50标签分类器在剩余训练池中，以0.8阈值选出123张图，这次选出的预测全部正确；这里隐藏的真值只用于事后检查，没有加入训练。若真的开展伪标签更新，还要另外运行更新后的模型并检查错误是否累积。

弱监督的答案来源不同。假设用“refund”给邮件打退款标签，用订单记录给交易打售后标签，两条规则可能冲突，也可能同时漏掉一种表达。Snorkel一类方法把这些标注函数产生的覆盖、冲突和相关性纳入标签建模，再训练最终预测器。粗粒度框、带噪文本标签和历史业务字段也都可能成为弱监督信号。它们把人类知识扩展到更多样本，但规则提供了什么信息、在哪些区域会系统性出错，应当成为数据设计的一部分。无标签输入、伪标签和有噪规则答案之间的区别，在这里就十分具体了。

## 把下一次提问留给哪张图

主动学习把训练流程中的一个决定交给模型：下一批人工标签该买在哪里。先用已有标签训练分类器，再对未标注池评分，请人标注选中的样本，最后重训。最容易理解的评分是不确定性。如果二分类器给出(0.5,0.5)，两种答案都说得通；给出(0.99,0.01)时，当前模型已有明确倾向。熵把这种分散程度压成一个数。它衡量的是模型自己的犹豫，因而适合发现决策边界附近的样本，却也可能反复挑中模糊、损坏或与任务无关的输入。

$$
H(p)=-\sum_{k=1}^{C}p_k\log p_k
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0547280d94d95a6b3705ca72.svg) | 类别总数与类别索引，本章C=10。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e02cdc3c22c69f868e141570.svg) | 分类器对一个未标注样本给出的类别概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/295b5229388ab789074fb769.svg) | 预测分布的熵与自然对数；熵以nats计，约定0log0=0。 |

二分类(0.5,0.5)的熵为ln2≈0.69315，(0.9,0.1)约0.32508。平均到两个类别的不确定性更高。十类均匀概率的熵为ln10≈2.30259。选取高熵样本使用的是当前模型的概率；错误但极自信的样本反而可能得分很低，因此要结合覆盖与多样性。

因此，选样常常还考虑代表性和多样性。连续挑出二十张几乎一样的模糊照片，可能只回答了同一个问题；在表示空间覆盖不同区域，则能让有限标签触及更多变化。可以先按不确定性筛出一批候选，再从中挑选相互较远的样本；也可以给罕见类别、不同设备或不同时间段设置覆盖目标。选样过程必须发生在训练池，测试集保留为固定考题。若用测试标签决定下一张问什么，再用同一测试集评价，标签预算的比较就失去原来的含义。

本章从每类5张、合计50张标签开始，每轮新增20张，共五轮。熵选样和随机选样使用同一初始标签集、同一冻结表示和同一种线性分类器。150标签时，熵选样准确率为86.11%，随机选样为88.06%；两条曲线中间还有交叉。增加标签改善了整体识别，却没有让这次熵选样持续占优。观察这种结果，可以进一步问被选样本是否集中在少数难例上，以及表示是否把类别边界组织得足够合理。交互中可以亲自决定询问哪一个点，查看新增答案怎样移动原型与分类区域。

![左：同一初始50标签，五次各增加20标签的实际测试准确率，两种选样都在训练池进行。右：完全相同50标签下的四种读取方式。每条曲线对应一个固定随机种子实验，没有绘制重复实验误差条。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e4729983534033b90d24202a.svg?v=e47299835340)

图 4左：同一初始50标签，五次各增加20标签的实际测试准确率，两种选样都在训练池进行。右：完全相同50标签下的四种读取方式。每条曲线对应一个固定随机种子实验，没有绘制重复实验误差条。

## 亲自挑选下一条标签

这是二维教学数据，类别由固定规则x+0.55y>0.05确定。初始只公开两个答案。点击灰色点或用Tab与回车选点，请求一个答案；原型与最近原型分类区域随之更新。选择“最不确定”可以观察熵规则的偏好。灰色点上的真实类别在查询后才显示。随机询问使用固定种子114的伪随机序列，在当前未询问池中等概率抽取，重置后可复现。

[Figure: 二维标签查询与原型](https://ml-biomat.com/tutorials/machine-learning/m11/#M11-board)

浅蓝、浅橙区域由当前两个原型决定；十字是已公开样本的类别平均。点内数字为样本编号。横纵轴为无量纲特征，不是图像的物理坐标。

## 少量示例、快速适应与换一个环境

给出一种新鸟的几张照片，人常常会先记住共同特征，而不是重新学习所有视觉规律。原型方法采用类似思路：把同一类别的支持样本映射到表示空间，取平均作为类别中心，再根据查询样本到各中心的距离分类。“支持集”负责告诉模型这一轮有哪些类别，“查询集”负责检查它能否识别同类的新样本。2017年的原型网络把这种按任务组织的训练方式系统化。本章只在已经学好的表示上计算原型，实际测试准确率为78.33%；它展示距离分类机制，训练阶段没有额外进行原型网络的任务式优化。

$$
c_k=\frac1{|S_k|}\sum_{i\in S_k}h_i,\qquad p(y=k\mid h)=\frac{\exp(-\|h-c_k\|^2/T)}{\sum_j\exp(-\|h-c_j\|^2/T)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4609563f79194104c68e45e5.svg) | 第k类支持样本索引集合、样本数、集合中的索引；每类至少一项。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eb9d55748d8bb4c809677e9d.svg) | 支持表示、查询表示、类别原型；本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea1243653251291ec000c74d.svg) | 待预测类别、当前类别索引、所有类别的求和索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85a38e0eee398d3b92ce3dea.svg) | 距离概率转换的温度与类别概率；T的量纲与距离平方一致。 |

支持点(0,1)、(2,1)的原型是(1,1)。查询(1,0)到它的距离平方为1；到另一个原型(3,0)的距离平方为4。T=1时第一类概率为1/(1+exp(−3))≈0.95257。取最大概率等于选最近原型。交互使用二维教学点与T=1；数字实验在32维表示上直接选最近原型。

元学习进一步把“怎样利用少量新样本”也放进训练目标。MAML在每个训练任务上先走一次小更新，再看更新后的参数能否预测该任务另一组查询样本；外层更新的是适合快速调整的初始参数。用一个可以手算的例子来看：三种任务分别是斜率−1、1、3的直线，模型只有一个待学斜率。每个任务的支持点位于横坐标1，查询点位于2。初始斜率0经过一次学习后分别变为−0.5、0.5、1.5，查询误差则推动共同初始值朝1移动。代码保留内层更新的计算图，得到外层梯度−1；以0.1步长更新，初始斜率变成0.1。

$$
w^{\prime}_a=w-\alpha\nabla_w\tfrac12(w-a)^2,\qquad J(w)=\frac13\sum_{a\in\{-1,1,3\}}\tfrac12(2w^{\prime}_a-2a)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a286aa7eca10e8b965a0853b.svg) | 共享初始斜率、对任务a适应后的斜率、该任务真实斜率；本例坐标与斜率均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4c587223ad233e42e6a867df.svg) | 内层学习率，以及对初始斜率的导数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d412557ea41f341470c49c0.svg) | 支持点和查询点的输入横坐标；预测分别为w和2w′。 |
| ![Formula](https://ml-biomat.com/static/agent-math/246a35cd24461118c16c775e.svg) | 三个任务查询损失的平均，以及任务平均系数。 |

内层导数为w−a，所以w′=(w+a)/2。代入查询项，2w′−2a=w−a，每个查询损失化为(w−a)²/2。平均斜率是1，因此J′(0)=−1。外层步长0.1把w从0更新为0.1。代码以create_graph=True保留内层导数对w的依赖；直接把适应结果转成普通数值会丢失这条元梯度路径。

领域适应处理另一种变化：类别含义相近，但输入分布换了环境，例如白天相机拍摄的零件与车间暗光下的零件。简单的曝光差异可以先通过测量和归一化校正；更复杂的变化需要学习合适的特征。域对抗方法同时训练类别头和域分类头：类别头判断零件类别，域头判断图像来自哪个环境，表示网络收到反向的域梯度，试着去掉能暴露环境身份的因素。2015年提出的DANN把这件事实现为梯度反转层，使普通反向传播就能完成两种相反的优化方向。

这个设计依赖我们确实希望保留的关系。若某一环境只拍A类、另一环境只拍B类，环境差异与类别信息缠在一起，盲目消除域差异也可能抹去分类线索。做领域适应时，先列出源域标签、目标域无标签样本、类别对应关系以及可用于选模型的验证数据，再决定需要对齐哪些变化。少样本学习关注新任务答案很少，元学习关注适应规则怎样学来，领域适应关注输入分布如何变化；这些条件能够同时出现，但各自需要的实验划分不同。

## 学会新东西，为什么会忘记旧东西

线上系统经常按时间收到数据。每来一批就更新参数，属于在线学习；如果新批次的类别、环境或目标发生变化，还要保留过去的能力，就进入持续学习的问题。共享参数让知识可以迁移，也让新的梯度能够改变旧任务依赖的特征。想象不断重写同一页笔记：新内容写得越完整，旧内容可能越难辨认。这里的“遗忘”可以直接测量：先在旧任务测试集上取得一个成绩，再学习新任务，最后回到同一份旧考题，看成绩改变了多少。

实验先公开0–4的类别标签，再公开5–9。每个阶段各训练200次更新，分类头始终保留十个输出。编码器此前已经见过全部训练图的无标签版本，因此这个实验关注标签顺序带来的变化。学完第一阶段，旧类测试准确率为100%，新类为0%；只用新类继续训练后，新类达到95.56%，旧类降到0%。新阶段的交叉熵既提高新类分数，也会通过归一化压低旧类输出，所以遗忘不只是“某几个笔画特征消失”，还涉及分类竞争和共享表示共同改变。

![旧类0–4、新类5–9各有180张测试图。A阶段只公开旧类标签；B阶段两种方式从同一A模型出发，各训练200步、每批64张。回放每批使用32张新图与32张旧图，缓冲区80张；右侧列出实际准确率。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2cfd02e2ca11d2a3d8f87fa4.svg?v=2cfd02e2ca11)

图 5旧类0–4、新类5–9各有180张测试图。A阶段只公开旧类标签；B阶段两种方式从同一A模型出发，各训练200步、每批64张。回放每批使用32张新图与32张旧图，缓冲区80张；右侧列出实际准确率。

回放给更新过程保留了一小份旧经验。本例每个旧类保存16张，共80张；第二阶段每批使用32张新图和32张回放图，总批量与更新次数保持一致。结果旧类保留90.00%，新类达到93.89%。回放让旧任务重新出现在梯度中，同时把一部分新样本位置让给旧样本，这正是稳定性与可塑性之间可观察的取舍。更大的缓冲区、更多样的样本、蒸馏旧模型输出或约束重要参数，都在调整如何保留过去。本章先把回放做成能看见数据和计算的基线，再讨论更复杂的机制才有清楚的参照。

## 把一份数据拆成几种学习问题

下面的完整程序使用随scikit-learn提供的1797张手写数字图，像素除以16。随机种子110和111产生分层划分：1077张训练图、360张验证图、360张测试图。表示训练固定80轮，不使用类别标签；本例的预算和参数预先指定，验证部分保留而未用于搜索。之后每类随机公开5个训练标签，线性分类、原型、伪标签检查和主动学习都从这个共同起点出发。数据属于现成图像的随机划分，并未按书写者重新分组；如果研究新书写者的泛化，应另行建立按人的划分。

50标签时，原始像素上的线性模型达到86.67%，对比表示达到82.78%，随机表示为77.50%。对比训练改善了这次随机表示，却没有超过简单的像素基线。手写小图本来已对齐，像素里保留了许多直接可读的结构；我们施加的噪声和遮挡又要求模型忽略部分信息。读完结果，应当能把表示目标、增强规则和任务需求连起来，而不把“预训练”当成自动提升的按钮。程序保存实际划分索引、每轮查询、表示、增强视图和模型参数，便于改变一个环节后追踪影响。

### 完整Python：无标签表示、标签预算与回放

依赖NumPy、Matplotlib、scikit-learn与PyTorch。运行python main.py --output results --language zh，产生四幅实际实验SVG、summary.json、模型权重与experiment.npz。投影头与编码器实际训练80轮；元梯度独立手算为−1，程序使用自动微分复核。

```
"""Representation, label budgets, and forgetting: an entirely local CPU experiment.

Data: sklearn digits (E. Alpaydin / C. Kaynak, UCI, CC BY 4.0).
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse, copy, json, platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path('results'))
parser.add_argument('--language',choices=['zh','en'],default='en')
args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
zh=args.language=='zh'
def tr(a,b): return a if zh else b
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5',
 'axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):
 fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)

data=load_digits();X=(data.data/16).astype('float32');y=data.target
train,other=train_test_split(np.arange(len(y)),test_size=720,stratify=y,random_state=110)
val,test=train_test_split(other,test_size=360,stratify=y[other],random_state=111)
xt=torch.tensor(X[train]);yt=torch.tensor(y[train]);xte=torch.tensor(X[test]);yte=y[test]
class Encoder(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,32))
 def forward(self,x): return self.net(x)
class Contrastive(nn.Module):
 def __init__(self):
  super().__init__();self.encoder=Encoder();self.projector=nn.Sequential(nn.Linear(32,32),nn.ReLU(),nn.Linear(32,16))
 def forward(self,x): return F.normalize(self.projector(self.encoder(x)),dim=1)
def augment(x,g):
 noise=.08*torch.randn(x.shape,generator=g)
 visible=torch.rand(x.shape,generator=g)>.15
 return (x+noise).clamp(0,1)*visible
def ntxent(a,b,tau=.2):
 z=torch.cat([a,b]);n=len(a);scores=z@z.T/tau
 scores=scores.masked_fill(torch.eye(2*n,dtype=torch.bool),-1e9)
 target=(torch.arange(2*n)+n)%(2*n)
 return F.cross_entropy(scores,target)
torch.manual_seed(112);model=Contrastive();untrained=copy.deepcopy(model.encoder)
optimizer=torch.optim.Adam(model.parameters(),lr=.001)
g=torch.Generator().manual_seed(113);losses=[]
for epoch in range(80):
 total=0.;order=torch.randperm(len(xt),generator=g)
 for ids in order.split(128):
  a,b=augment(xt[ids],g),augment(xt[ids],g)
  loss=ntxent(model(a),model(b));optimizer.zero_grad();loss.backward();optimizer.step()
  total+=loss.item()*len(ids)
 losses.append(total/len(xt))
model.eval()
with torch.no_grad():
 feat=F.normalize(model.encoder(xt),dim=1).numpy()
 testfeat=F.normalize(model.encoder(xte),dim=1).numpy()
 rawfeat=F.normalize(untrained(xt),dim=1).numpy()
 rawtestfeat=F.normalize(untrained(xte),dim=1).numpy()
rng=np.random.default_rng(114)
initial=np.concatenate([rng.choice(np.where(y[train]==k)[0],5,replace=False) for k in range(10)])
def probe(features,testing,ids):
 clf=LogisticRegression(C=10,max_iter=1500).fit(features[ids],y[train][ids])
 return clf,float(clf.score(testing,yte))
cl,accuracy=probe(feat,testfeat,initial)
_,random_accuracy=probe(rawfeat,rawtestfeat,initial)
_,pixel_accuracy=probe(X[train],X[test],initial)
prototypes=np.stack([feat[initial[y[train][initial]==k]].mean(0) for k in range(10)])
prototype_pred=((testfeat[:,None]-prototypes[None])**2).sum(2).argmin(1)
prototype_accuracy=float((prototype_pred==yte).mean())
pool=np.setdiff1d(np.arange(len(train)),initial)
confidence=cl.predict_proba(feat[pool]);accepted=confidence.max(1)>=.8
pseudo=dict(threshold=.8,count=int(accepted.sum()),correct_fraction=float((cl.predict(feat[pool][accepted])==y[train][pool][accepted]).mean()) if accepted.any() else None)
active={};acquired={}
for policy in ['entropy','random']:
 ids=initial.copy();curve=[];round_ids=[];rg=np.random.default_rng(115)
 for round_index in range(6):
  classifier,score=probe(feat,testfeat,ids);curve.append([len(ids),score])
  if round_index==5:break
  remaining=np.setdiff1d(np.arange(len(train)),ids)
  probabilities=classifier.predict_proba(feat[remaining])
  entropy=-(probabilities*np.log(np.maximum(probabilities,1e-15))).sum(1)
  selected=remaining[np.argsort(-entropy,kind='stable')[:20]] if policy=='entropy' else rg.choice(remaining,20,replace=False)
  round_ids.append(selected);ids=np.r_[ids,selected]
 active[policy]=curve;acquired[policy]=np.array(round_ids)

# Exact differentiable inner update: three tasks y = a*x, each with one support point.
w=torch.tensor(0.,requires_grad=True);outer=[]
for slope in [-1.,1.,3.]:
 support_loss=.5*(w-slope)**2
 inner_grad=torch.autograd.grad(support_loss,w,create_graph=True)[0]
 adapted=w-.5*inner_grad
 outer.append(.5*(2*adapted-2*slope)**2)
meta_loss=torch.stack(outer).mean();meta_gradient=torch.autograd.grad(meta_loss,w)[0].item()

# Class-incremental labels: the encoder has seen every training image without labels.
class Classifier(nn.Module):
 def __init__(self,encoder):
  super().__init__();self.encoder=copy.deepcopy(encoder);self.head=nn.Linear(32,10)
 def forward(self,x): return self.head(self.encoder(x))
torch.manual_seed(116);stage_a=Classifier(model.encoder)
old=np.where(y[train]<5)[0];new=np.where(y[train]>=5)[0]
def fit_steps(net,primary,replay=None,seed=117):
 opt=torch.optim.Adam(net.parameters(),lr=.003);gen=np.random.default_rng(seed)
 net.train()
 for step in range(200):
  ids=gen.choice(primary,64 if replay is None else 32)
  if replay is not None:ids=np.r_[ids,gen.choice(replay,32)]
  loss=F.cross_entropy(net(xt[ids]),yt[ids]);opt.zero_grad();loss.backward();opt.step()
 net.eval()
def task_scores(net):
 with torch.no_grad(): pred=net(xte).argmax(1).numpy()
 return [float((pred[yte<5]==yte[yte<5]).mean()),float((pred[yte>=5]==yte[yte>=5]).mean())]
fit_steps(stage_a,old);continual={'after_A':task_scores(stage_a)}
replay_rng=np.random.default_rng(118)
buffer=np.concatenate([replay_rng.choice(np.where(y[train]==k)[0],16,replace=False) for k in range(5)])
for name,replay in [('new_only',None),('replay',buffer)]:
 net=copy.deepcopy(stage_a);fit_steps(net,new,replay,119);continual[name]=task_scores(net)
 torch.save(net.state_dict(),out/f'continual-{name}.pt')
torch.save(model.state_dict(),out/'contrastive.pt')

gv=torch.Generator().manual_seed(120)
chosen=np.array([np.flatnonzero(y[train]==k)[0] for k in range(10)])
images=xt[chosen];view1=augment(images,gv);view2=augment(images,gv)
fig,axs=plt.subplots(3,10,figsize=(13,4.8),gridspec_kw={'wspace':.03,'hspace':.15})
for row,items in enumerate([images,view1,view2]):
 for col,img in enumerate(items):
  axs[row,col].imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);axs[row,col].set_xticks([]);axs[row,col].set_yticks([])
  if row==0:axs[row,col].set_title(str(col))
 axs[row,0].set_ylabel(tr(['原图','视图 A','视图 B'][row],['Original','View A','View B'][row]))
fig.suptitle(tr('同一张图，两次独立变化：噪声 σ=0.08，遮挡概率 0.15','One image, two independent views: noise σ=0.08; masking probability 0.15'))
save(fig,'views')
with torch.no_grad():
 za,zb=model(view1),model(view2);similarity=(za@zb.T).numpy()
pca=PCA(n_components=2).fit(feat);coords=pca.transform(testfeat)
fig=plt.figure(figsize=(13,7.8));grid=fig.add_gridspec(2,2,width_ratios=[1,1.3],hspace=.4,wspace=.32)
ax=fig.add_subplot(grid[0,0]);ax.plot(np.arange(1,81),losses,color='#125f82',lw=2)
ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('平均 NT-Xent / nats','Mean NT-Xent / nats'),title=tr('A  标签未进入表示训练','A  Representation training sees no labels'))
ax=fig.add_subplot(grid[1,0]);im=ax.imshow(similarity,cmap='viridis',vmin=-1,vmax=1);ax.set(xlabel=tr('视图 B：样本编号','View B: sample index'),ylabel=tr('视图 A：样本编号','View A: sample index'),title=tr('B  对角线是同一原图的配对','B  Diagonal entries are positive pairs'))
fig.colorbar(im,ax=ax,fraction=.045,label=tr('余弦相似度','Cosine similarity'))
ax=fig.add_subplot(grid[:,1]);sc=ax.scatter(coords[:,0],coords[:,1],c=yte,cmap='tab10',s=23,alpha=.8,edgecolors='none')
ax.set(xlabel=tr('主成分 1','Principal component 1'),ylabel=tr('主成分 2','Principal component 2'),title=tr('C  测试表示的二维投影；颜色只用于读图','C  Test representations; labels color the plot only'))
fig.colorbar(sc,ax=ax,ticks=range(10),fraction=.045,label=tr('真实数字','True digit'));save(fig,'representation')
fig,(ax,bar)=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[1.5,1]},layout='constrained')
for policy,color,label in [('entropy','#b85d30',tr('熵选样','Entropy queries')),('random','#125f82',tr('随机选样','Random queries'))]:
 c=np.array(active[policy]);ax.plot(c[:,0],c[:,1],'-o',color=color,lw=2,label=label)
ax.set(xlabel=tr('累计人工标签数','Cumulative human labels'),ylabel=tr('测试准确率','Test accuracy'),ylim=(.5,1),title=tr('A  每轮新增 20 个标签','A  Twenty additional labels per round'));ax.legend()
names=[tr('像素 + 线性','Pixels + linear'),tr('随机表示 + 线性','Random + linear'),tr('对比表示 + 线性','Contrastive + linear'),tr('对比表示 + 原型','Contrastive + prototypes')]
vals=[pixel_accuracy,random_accuracy,accuracy,prototype_accuracy]
bar.barh(names,vals,color=['#a9b2b8','#a9b2b8','#125f82','#b85d30']);bar.set(xlim=(0,1.05),title=tr('B  相同的 50 个标签','B  The same 50 labels'),xlabel=tr('测试准确率','Test accuracy'))
for i,v in enumerate(vals):bar.text(v+.01,i,f'{v:.1%}',va='center',fontsize=10)
save(fig,'labels')
fig,(ax,table)=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.4,1]},layout='constrained')
names=['after_A','new_only','replay'];xx=np.arange(3)
ax.bar(xx-.18,[continual[n][0] for n in names],.36,label=tr('旧类 0–4','Old classes 0–4'),color='#125f82')
ax.bar(xx+.18,[continual[n][1] for n in names],.36,label=tr('新类 5–9','New classes 5–9'),color='#b85d30')
ax.set_xticks(xx,[tr('学完 A','After A'),tr('B：仅新样本','B: new only'),tr('B：加入回放','B: with replay')]);ax.set(ylim=(0,1.12),ylabel=tr('测试准确率','Test accuracy'),title=tr('A  学到新类后，旧知识还在吗？','A  Learning new classes: what survives?'));ax.legend(loc='upper left',fontsize=9)
matrix=np.array([continual[n] for n in names]);im=table.imshow(matrix,vmin=0,vmax=1,cmap='Blues',aspect='auto')
table.set_xticks([0,1],[tr('旧类','Old'),tr('新类','New')]);table.set_yticks(xx,[tr('A 后','After A'),tr('新样本','New only'),tr('80 张回放','80 replay images')]);table.set_title(tr('B  每种方式的实际结果','B  Measured task accuracies'))
for i in range(3):
 for j in range(2):table.text(j,i,f'{matrix[i,j]:.1%}',ha='center',va='center',color='white' if matrix[i,j]>.6 else '#152d3a',fontsize=14)
save(fig,'forgetting')
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__,sklearn=sklearn.__version__),
 splits=dict(train=len(train),validation=len(val),test=len(test)),seed=110,
 contrastive=dict(epochs=80,temperature=.2,batch_size=128,final_loss=losses[-1],encoder_parameters=sum(p.numel() for p in model.encoder.parameters()),projector_parameters=sum(p.numel() for p in model.projector.parameters())),
 probes=dict(contrastive=accuracy,random=random_accuracy,pixels=pixel_accuracy,prototype=prototype_accuracy),
 active=active,pseudo=pseudo,continual=continual,replay_count=len(buffer),
 meta=dict(gradient=meta_gradient,initial=0,inner_rate=.5,outer_rate=.1,updated=-.1*meta_gradient),
 hand=dict(cosine=float(np.dot([.6,.8],[0.,1.])),uniform_three_candidate_loss=float(np.log(3)),masked_mse=float(np.mean((np.array([.3,.6])-np.array([.2,.8]))**2)),prototype=np.mean([[0.,1.],[2.,1.]],axis=0).tolist()))
(out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train_indices=train,val_indices=val,test_indices=test,initial_labels=initial,
 features=feat,test_features=testfeat,pca_coordinates=coords,loss=losses,similarity=similarity,view1=view1.numpy(),view2=view2.numpy(),
 entropy_queries=acquired['entropy'],random_queries=acquired['random'],replay_indices=buffer)
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

运行后可以先打开样本接触表，确认增强保留了要识别的内容；再读相似度矩阵，检查配对关系有没有形成；随后比较相同标签预算下的分类结果；最后看新旧任务成绩如何变化。若要继续探索，一次改变一个决定最容易解释：减少遮挡、增加标签、给主动选样加入多样性，或者扩大回放缓冲区。每一种改变都对应本章的一条问题线索：让模型保留什么信息，让人回答什么问题，以及让新知识怎样与旧知识共存。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M11.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SimCLR](https://arxiv.org/abs/2002.05709)

   正负配对、投影头与增强设计。

   Primary paper; figures not copied
2. [UvA Tutorial 17: SimCLR](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial17/SimCLR.html)

   表示评估与经许可原图。

   MIT; copyright 2020 Phillip Lippe; original tutorial output figure only
3. [Bootstrap Your Own Latent](https://arxiv.org/abs/2006.07733)

   在线/目标网络、移动平均与停止梯度。

   Primary paper; figures not copied
4. [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)

   可见块编码与隐藏像素重建。

   Primary paper; figures not copied
5. [FixMatch](https://arxiv.org/abs/2001.07685)

   弱/强增强和置信度筛选伪标签。

   Primary paper; figures not copied
6. [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160)

   标注函数的覆盖、冲突与标签建模。

   Primary paper; figures not copied
7. [Prototypical Networks for Few-shot Learning](https://arxiv.org/abs/1703.05175)

   支持集原型与查询距离。

   Primary paper; figures not copied
8. [Model-Agnostic Meta-Learning](https://arxiv.org/abs/1703.03400)

   内层支持更新与外层查询目标。

   Primary paper; figures not copied
9. [Domain-Adversarial Training of Neural Networks](https://arxiv.org/abs/1505.07818)

   领域适应与梯度反转。

   Primary paper; figures not copied
10. [Experience Replay for Continual Learning](https://arxiv.org/abs/1811.11682)

    回放保存经验的机制；原论文实验为强化学习场景。

    Primary paper; our digit experiment is independently designed
11. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    数据说明与图像许可。

    CC BY 4.0; E. Alpaydin and C. Kaynak
