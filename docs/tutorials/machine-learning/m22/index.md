# 图神经网络：让关系进入计算

Source: https://ml-biomat.com/tutorials/machine-learning/m22/
Language: zh-CN

从一跳消息到 GCN、GraphSAGE、GAT 和几何等变性，亲手检查信息怎样沿边传播。

## 1. 拿掉连线，问题会变成什么

傍晚下雨，你想知道下一站公交是否会挤满。本站此刻的客流当然重要，但上游站点刚刚涌入的人、附近地铁临时停运的信息，也可能决定十分钟后的情况。如果把每个站点单独放进表格，只给模型看本站的数字，就丢掉了人会沿线路移动这个事实。图神经网络处理的正是这类问题：一个对象的判断，需要借助它与其他对象的关系。公交站、文章、账户或零件都可以成为节点；线路、引用、交易或接触则成为边。选择哪一种关系进入模型，比先挑选哪一种网络更重要。

这里的“图”是关系图，不是统计图表。把一条路线画得弯一些、把两个站点画得远一些，只要连线和属性没有改变，抽象图就仍然相同。也因此，图上节点没有天然的从左到右顺序：给车站重新编号，不应改变它的拥堵预测。普通表格模型把一行当作一个独立样本，图模型则把节点的特征和邻接关系一起作为输入。输出可以是每个节点的类别、某一对节点之间出现关系的概率，也可以是整张图的性质。这三种任务共用信息传播的方法，但训练标签的位置和评估划分不同。

本章先在几个节点之间传递一列数，再搭建一个可以完整运行的 GCN。我们使用明确生成规则的合成网络：两个群体内部连接较多，群体之间连接较少，节点自身的观测带有噪声。这样的设置让“关系能增加什么信息”变得可检查。随后再改变观察角度：如果邻居的意见并不一样重要，如果一张图不断长大，如果节点有空间坐标，消息应该怎样计算？GCN、GraphSAGE、GAT 和几何等变网络，就在这些具体问题里各有位置。

## 2. 从关系图到一张可计算的矩阵

假设三个站点 A、B、C 依次相连，A 与 C 没有直达线路。邻接矩阵就是一张“行节点能否接收到列节点消息”的表：A 行 B 列填 1，A 行 C 列填 0。无向图中两个方向相同，矩阵关于对角线对称；公交的单行路线则需要保留方向。节点特征另外放在矩阵 X 中，每一行对应一个站点，每一列对应一种观测，例如标准化后的客流、等待时间和降雨。边也可以有属性，例如行驶时间；给边加方向和属性，表达的是不同的交通事实，不能只凭画图好看随意设置。

$$
m_i=\sum_{j=1}^{N}A_{ij}x_j,\qquad \mathbf m=A\mathbf x
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 节点数，无量纲整数；本式先用每节点一个标量特征。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 接收节点与发送节点索引，取1至N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | N×N邻接矩阵；Aij=1表示j向i传递消息，否则为0，元素无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3e1f8a0b406959ab68838255.svg) | 节点j的标量信号及N维列向量；这里采用无量纲标准化观测。 |
| ![Formula](https://ml-biomat.com/static/agent-math/63d7401d5988a965f904b548.svg) | 邻居信号和及N维结果，单位与x相同。 |

每个Aij先充当开关，再求和，因此矩阵乘法恰好实现沿边收集。三节点链A—B—C没有自连接，输入(1,3,5)时输出(3,6,3)。给对角线加1后，B收到1+3+5=9；再除以包括自己在内的3个节点，均值为3。求和与平均是两个不同运算。

矩阵乘法在这里有非常朴素的含义：沿着有连接的位置，把邻居的数加起来。若 A、B、C 的信号分别是 1、3、5，B 收到 A 和 C 的和就是 6；把自己也纳入邻域后，三个数的平均为 3。可以把这一步想成开一次小型邻里会议，每个节点从允许参加的人那里收集意见。会议名单由图决定，怎样综合意见由聚合规则决定。这里还没有学习，只是在搬运和组合观测。真正的神经网络会学习如何把这些综合观测转换成对任务有用的新特征。

这个区别有助于理解图卷积的来历。图信号处理关心不规则网络上的信号如何变化；相连节点数值相近，相当于沿关系变化得较平缓。Kipf 与 Welling 在 ICLR 2017 的 GCN 工作中，把谱图卷积的局部近似整理成一种简洁的逐层传播规则，让节点特征与连接结构共同参与半监督分类。下面的 Distill 原图把信息从邻居汇集到中心节点的过程画了出来。阅读时先跟踪消息的来源，再看聚合后的向量去了哪里，比把每一个方框名称背下来更容易理解模型。

![Distill 图神经网络架构图，展示邻域聚合与节点更新。](https://ml-biomat.com/static/tutorials/machine-learning/figures/959cd188a1cbd110dea60bdb.png?v=959cd188a1cb)

图 1消息聚合的原始架构图：邻居表示经过聚合，再更新节点表示。图：Sanchez-Lengeling、Reif、Pearce 与 Wiltschko，A Gentle Introduction to Graph Neural Networks，Distill (2021)，https://distill.pub/2021/gnn-intro/，CC BY 4.0，原图未改动。

构图同时也是建模假设。按空间距离连边，表示近邻可能相关；按引用连边，表示文章存在知识联系；按同一账户发生的交易连边，表示这些记录共享参与者。这些关系并不自动等于“类别相同”。欺诈网络中的异常账户可能频繁连接正常账户，交通路网相邻站点的客流也可能一高一低。图的价值要通过与只看节点特征的基线比较来检验，还要查看边的方向、时间和含义。把预测时才会知道的边提前放入图中，会让模型得到现实任务中不可用的信息。

## 3. GCN：让邻居说话，也让热门节点少一点音量

直接求和有一个问题：一个有一百个邻居的节点，往往比只有两个邻居的节点得到大得多的数值，即使每条消息同样普通。GCN 给每条连接乘上由两端连接数决定的系数，并加入自连接，让节点保留自己的信息。这个系数同时考虑接收者和发送者，因此叫对称归一化。它与简单“除以自己邻居数”的平均并不完全相同；在连接数相等的图上两者一致，在连接数不等时，发送者的热门程度也会改变贡献。归一化后的数值通常保持在更便于后续网络处理的尺度。

$$
\widetilde A=A+I_N,\quad \widetilde D_{ii}=\sum_j\widetilde A_{ij},\quad \widehat A=\widetilde D^{-1/2}\widetilde A\widetilde D^{-1/2},\qquad H^{(\ell+1)}=\operatorname{ReLU}(\widehat A H^{(\ell)}W^{(\ell)})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e40cf74018a825ff1b5a7b89.svg) | 无向图的N×N邻接矩阵和单位矩阵；元素无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4fd6c496d6d7712a47e3912f.svg) | 加自连接后的邻接矩阵及度对角矩阵，N×N；度是邻居计数且包含自己。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c47342559dd71b1b19dfe153.svg) | 对称归一化传播矩阵，N×N；边i,j权重是1/√(di dj)，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fa29d7dba7af8c5436716754.svg) | 第ℓ层节点表示N×Fℓ、可学习权重Fℓ×Fℓ₊₁；标准化隐藏表示与权重均无量纲，H⁽⁰⁾=X。 |
| ![Formula](https://ml-biomat.com/static/agent-math/90d899d413b08675e0bedf96.svg) | 层索引、该层通道数、逐元素max(0,z)操作。分类输出层在代码中省略ReLU。 |

左乘传播矩阵汇集节点，右乘权重矩阵重组通道，形状依次为(N×N)(N×Fℓ)(Fℓ×Fℓ₊₁)。三节点链加入自连接后度为2、3、2，输入(1,3,5)，中点聚合值为1/√6+3/3+5/√6≈3.449，而简单邻域均值为3。两种结果的差别来自发送节点度的归一化。若所有度相等为d，系数就变为1/d。

传播矩阵负责“从哪里收集”，权重矩阵负责“怎样重组特征”。假设每个节点有 6 个输入数字，第一层输出 16 个数字，那么输入矩阵是节点数乘 6，权重矩阵是 6 乘 16，结果是节点数乘 16。权重在所有节点共享，所以不会为每个站点单独学习一套规则。ReLU 再把负数截成零，带来非线性。第二层重复邻居聚合，中心节点便间接获得两跳范围内的信息。层数增长时可见范围扩大，但“看得更远”与“分得更清楚”是两个需要分别验证的目标。

训练时，模型给每个节点输出各类别的分数，而损失只在有训练标签的节点上计算。标签不是每轮沿边抄过去的答案；被传播的是特征，以及由共享权重产生的隐藏表示。标签通过损失和梯度影响这些权重，再间接影响全图的预测。本章实验训练时可以看到整张图和所有节点特征，但只使用 20 个节点的标签更新参数。这叫传导式节点分类。若真正的使用场景是明年出现的新节点，则需要按时间或节点批次留出测试对象，并检查建图过程在那个时刻能获得什么。

### 邻域实验：图、矩阵与信号一起变化

每步用旧状态同时更新全部节点，始终包含自连接。改变参数从初始信号重新计算，单步按钮再向前传播一次。

[Figure: 左为节点关系及当前数值，右为传播矩阵，下为节点信号柱形图](https://ml-biomat.com/tutorials/machine-learning/m22/#M22-svg)

在交互中先选择“平均”，把第一个节点的信号调到 6，再单步传播。它的变化会进入相邻节点，第二次传播才继续到更远的位置。开启额外连线后，再观察新连接怎样改变邻域人数和平均值；选择“求和”则会看见连接较多的位置更容易积累较大的数。这个小实验把聚合本身拆出来，没有训练权重。它适合检查数据怎样流动，而完整代码会把相同的结构运算放进可学习的两层网络。

## 4. GraphSAGE 与 GAT：新邻居怎样加入，意见怎样加权

一座城市每天会出现新站点，一张交易网络每天会加入新账户。为每个固定节点单独记住一个向量，不容易处理这种增长。Hamilton、Ying 与 Leskovec 在 2017 年的 GraphSAGE 中，把重点放在学习一个可复用的邻域聚合函数，并通过采样控制计算量。以均值聚合版本为例，先平均选中的邻居特征，再把这个平均与节点自己的特征并排拼接，交给共享的线性层和激活函数。模型学的是如何加工一组局部观测，因此新节点只要有合适的特征和可用的邻居，也可以进入同一套计算。

$$
\overline h_i=\frac{1}{|S(i)|}\sum_{j\in S(i)}h_j,\qquad h_i'=\sigma\!\left(W[h_i\Vert\overline h_i]+b\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5681a4914647757834ffe88.svg) | 中心节点、邻居节点、抽样邻居集合和其大小；集合需非空，孤立节点另设零邻居向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2215da064eaf2b3b48181bd.svg) | F维节点列向量和F维邻居均值，采用无量纲隐藏特征。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8cf39fd79bbe48a27c6ceb26.svg) | 拼接操作，产生2F维向量；W为F′×2F，b为F′维，均为可学习无量纲参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/59ac27727155f13a2ca7aad9.svg) | 逐元素激活与更新后的F′维向量；本式是均值GraphSAGE的核心变换，完整变体还可归一化表示。 |

自己的信息与邻居的信息保留在拼接向量不同位置，权重便能学习二者的不同作用。设自己的标量为2，两个邻居为1、5，均值为3；拼接为(2,3)，取W=(2,−1)、b=0、ReLU，输出max(0,4−3)=1。若把自己也混入邻居平均，算出的量就属于另一种聚合规则。

采样为什么重要？若每个节点平均有 50 个邻居，直接展开两跳可能访问约 2500 条分支；每层只抽取 10 个邻居，就把展开规模控制在约 100 条分支。重复节点会让实际数量小于这个乘积，但计算增长的趋势很清楚。随机抽样带来不同批次的波动，热门节点、稀有关系和关键远邻也可能被遗漏。因此训练与评价要说明采样数量及随机性。归纳式能力来自共享的特征处理规则和合适的评估，不是给网络起了 GraphSAGE 这个名字就自动获得。

另一个问题是：邻居是否都值得同样重视？Veličković 等人的 GAT 在 2018 年把注意力放到图的局部邻域中。模型先根据中心节点和邻居的特征计算相容分数，再用 softmax 把分数转换成权重；权重非负且在当前邻域内加起来为 1。比如两个邻居的分数是 0 和自然对数 3，指数化后是 1 和 3，归一化后便得到 0.25 和 0.75。若对应消息为 2 和 6，聚合值就是 5。注意力让权重随特征和中心节点变化，而 GCN 的归一化主要由连接结构确定。

$$
\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_{k\in\mathcal N_i}\exp(e_{ik})},\qquad h_i'=\sigma\!\left(\sum_{j\in\mathcal N_i}\alpha_{ij}Wh_j\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d151193ddab5d9bfb3903d6d.svg) | 中心节点、邻居索引、求和索引及允许的邻域，可包含自己；集合按边掩码给定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff454cbb1c2c014f5d6a966e.svg) | 学习得到的相容分数与softmax权重，均无量纲；分数由i和j的变换后特征共同计算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eaaae4da4516a6e235e27303.svg) | 输入F维向量、F′×F权重、输出F′维向量及激活；此处是单头注意力，隐藏量无量纲。 |

指数把任意实数分数变为正数，除以总和让权重合计为1。数值实现可先减去邻域最大分数，结果不变且更稳定。两个分数0、ln3产生权重0.25、0.75；若Wh分别为2、6，激活前聚合为0.25×2+0.75×6=5。改变邻域成员也会改变分母，因此其余权重会随之重新归一化。

多个注意力头可以各自形成一套加权方式，再拼接或平均结果。它们有时捕捉不同关系，有时也学到相似模式，具体分工由训练决定。一个很大的注意力权重说明这次内部计算强调了某条消息；若想判断这条边是否真正改变最终预测，还要删边、替换特征或比较反事实输入。GCN 的计算简单，适合先建立结构基线；GraphSAGE 便于邻域采样和新节点处理；GAT 允许数据决定局部权重。选择时应比较同样的数据划分、计算预算和实际指标，而不是按名称的新旧排序。

## 5. 标签落在哪里，决定怎样训练和检验

节点分类问的是“这个对象属于哪一类”，所以每个被标注节点贡献一个分类损失。链接预测问的是“两个对象之间会不会出现关系”，常见做法是先得到两个节点的表示，再用点积或小网络计算配对分数。若两个二维表示分别是 (1,0) 和 (2,1)，点积为 2，经过 sigmoid 后得到约 0.881。这个数只有在相应训练目标、采样和校准条件下才可解释为预测概率。尤其要注意：做链接预测时，测试边不能同时作为消息传播的输入边，否则模型已经看到了要猜测的连接。

$$
z_{ij}=h_i^{\mathsf T}h_j,\qquad p_{ij}=\frac{1}{1+\exp(-z_{ij})}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 待评分的一对节点索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2a3e18970f6df1c85ae1bb61.svg) | 相同F维空间中的无量纲节点表示；本例采用对称点积评分。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd0fc75ca5b5a2073a0cec7.svg) | 配对logit、0至1间的sigmoid输出和转置符号；均无量纲。 |

点积把两个表示的逐坐标乘积相加。输入(1,0)与(2,1)，得到z=2、p≈0.8808。交换i和j得分不变，因此这种解码器适合无向关系；有向或多类型关系可使用关系专属变换或顺序敏感网络。训练时使用怎样的负采样会改变分数解释，测试还应匹配实际候选集合。

没有记录到的边也不一定是真正的负例。一对人没有交互记录，可能因为还没有机会相遇；一个知识关系没有收录，可能只是数据库不完整。负采样要先说明候选集合，再从中抽取未观测配对，并说明这种标签约定。推荐任务通常还需要在真实候选池中评价排序，因为从百万对象里找出相关对象，比从一个正例和一个随机负例中二选一困难得多。动态图还应按时间切分：训练只能使用预测时刻以前的节点特征与边事件。

图分类则为整张图给出一个标签，例如判断一组零件的连接方案属于哪一种结构。节点数可变，输出长度却要固定，所以需要读出操作。求和保留规模信息，平均强调典型节点的状态，最大值强调是否存在某种强特征。两个节点的标量表示是 2 和 4，求和为 6，平均为 3；再加入两个完全相同的节点，平均仍为 3，求和变为 12。哪一种更合适，取决于目标是否随系统大小变化。不能把所有节点按编号直接拼接，然后期待模型天然忽略重新编号。

异构图保留节点和边的类型：作者、文章、会议是三类节点，“撰写”和“发表于”是不同关系。关系专属的变换矩阵可以分别处理各类消息，再汇总到目标节点。知识图谱把事实写成“主体—关系—客体”，例如“文章—引用—文章”，方向和关系名都参与评分。动态图则额外记录事件时间，用时间窗口、递归状态或时间编码区分“刚刚发生”和“很久以前”。这几种扩展都从同一个问题出发：边上的哪些信息会改变消息含义，就应在表示和计算中保留下来。

## 6. 一个完整实验：关系能把噪声中的群体找出来吗

下面的代码生成 120 个节点，分成两个各 60 个节点的群体。同群体连边概率为 0.18，跨群体为 0.015，最终固定样本有 648 条无向边。每个节点有 6 个带标准正态噪声的特征，前两个特征按类别加上 −0.25 或 0.25，因此仅凭自身观测很难判断类别。每类随机选 10 个训练标签、10 个验证标签，剩下的 40 个作为测试标签。图的展示位置只为帮助读图生成，不进入模型；图上左右两群的位置也没有作为分类线索传给模型。

![社区网络与前两维特征散点图对照。](https://ml-biomat.com/static/tutorials/machine-learning/figures/83f371dce4e38162e2ae5503.svg?v=83f371dce4e3)

图 2合成图的两种视角。左：120个节点、648条边，颜色为生成类别，黑圈为20个训练标签，绘图坐标不输入模型。右：前两个输入特征高度重叠；关系与单点特征提供不同信息。

GCN 和 MLP 都使用 6→16→2 的无偏置线性层、ReLU 和 0.2 的 dropout，共有相同数量的可学习权重。GCN 在两层前各进行一次图聚合，MLP 只看节点自身的数字。两者都训练 150 轮，用验证交叉熵最低的那一轮保存参数，再计算测试准确率。重复 5 个初始化种子，图和标签划分保持固定，这样观察到的是训练初始化的波动；若要估计换一张图或换一组标签的波动，需要另加数据种子和划分种子的实验。

### 完整 Python：GCN 对照、传播图与对称性检查

使用 NumPy、PyTorch、Matplotlib。运行 main.py --output output --language zh，或把语言换为 en。固定图和划分，训练五次同参数量的 GCN/MLP，保留验证损失最低的检查点，写出数据、summary.json 与三组图。

```
"""A transductive graph experiment with reproducible ablations and symmetries."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


def dataset():
    rng = np.random.default_rng(2026)
    labels = np.repeat(np.arange(2), 60)
    p = np.where(labels[:, None] == labels[None, :], .18, .015)
    upper = np.triu(rng.random((120, 120)) < p, 1)
    adjacency = (upper | upper.T).astype(np.float32)
    features = rng.normal(0, 1, (120, 6)).astype(np.float32)
    features[:, :2] += (2 * labels[:, None] - 1) * .25
    train, valid, test = [], [], []
    for c in range(2):
        order = rng.permutation(np.where(labels == c)[0])
        train.extend(order[:10]); valid.extend(order[10:20]); test.extend(order[20:])
    a = adjacency + np.eye(120, dtype=np.float32)
    inv = 1 / np.sqrt(a.sum(1))
    normalized = inv[:, None] * a * inv[None, :]
    return adjacency, normalized, features, labels, train, valid, test


class NodeModel(nn.Module):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.first = nn.Linear(6, 16, bias=False)
        self.last = nn.Linear(16, 2, bias=False)

    def forward(self, x, a):
        hidden = torch.relu(self.first(a @ x if self.graph else x))
        hidden = nn.functional.dropout(hidden, .2, self.training)
        return self.last(a @ hidden if self.graph else hidden)


def fit(kind, seed, a, x, y, train, valid, test):
    torch.manual_seed(seed)
    model = NodeModel(kind == 'GCN')
    optimizer = torch.optim.Adam(model.parameters(), lr=.02, weight_decay=5e-4)
    trace, best_loss, best = [], float('inf'), None
    for epoch in range(150):
        model.train(); optimizer.zero_grad()
        logits = model(x, a)
        loss = nn.functional.cross_entropy(logits[train], y[train])
        loss.backward(); optimizer.step()
        model.eval()
        with torch.no_grad():
            logits = model(x, a)
            val = nn.functional.cross_entropy(logits[valid], y[valid]).item()
            trace.append([loss.item(), val])
            if val < best_loss:
                best_loss, best = val, copy.deepcopy(model.state_dict())
    model.load_state_dict(best); model.eval()
    with torch.no_grad():
        logits = model(x, a)
        accuracy = (logits[test].argmax(1) == y[test]).float().mean().item()
    return model, np.asarray(trace), accuracy, logits.detach().numpy()


def vectors(points):
    difference = points[None, :, :] - points[:, None, :]
    weights = np.exp(-np.square(difference).sum(-1))
    return (weights[:, :, None] * difference).sum(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': 'Microsoft YaHei' if zh else 'Arial',
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none'})
    def label(ch, en): return ch if zh else en
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
    adjacency, normalized, features, labels, train, valid, test = dataset()
    a, x, y = torch.tensor(normalized), torch.tensor(features), torch.tensor(labels)
    results, traces, scores, models = {}, {}, {}, {}
    for kind in ['MLP', 'GCN']:
        traces[kind], scores[kind] = [], []
        for seed in range(5):
            model, trace, score, logits = fit(kind, seed, a, x, y, train, valid, test)
            traces[kind].append(trace); scores[kind].append(score)
            if seed == 0: models[kind] = (model, logits)
        results[kind] = {'test_accuracy': scores[kind], 'mean_accuracy': float(np.mean(scores[kind]))}
    permutation = torch.tensor(np.random.default_rng(17).permutation(120))
    with torch.no_grad():
        shifted = models['GCN'][0](x[permutation], a[permutation][:, permutation])
        original = models['GCN'][0](x, a)[permutation]
        permutation_error = float((shifted-original).abs().max())
    points = np.array([[0., 0.], [1., .1], [.2, .8], [1.2, 1.]])
    theta = .7
    rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotation_error = float(np.max(np.abs(vectors(points @ rotation.T) - vectors(points) @ rotation.T)))
    assert permutation_error < 2e-6
    assert rotation_error < 1e-12
    results.update({'nodes': 120, 'edges': int(adjacency.sum()/2), 'split_sizes': [20, 20, 80],
                    'permutation_max_error': permutation_error, 'rotation_max_error': rotation_error})
    (args.output/'summary.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    np.savez(args.output/'data.npz', adjacency=adjacency, features=features, labels=labels,
             train=train, valid=valid, test=test, GCN_trace=np.array(traces['GCN']),
             MLP_trace=np.array(traces['MLP']), GCN_scores=scores['GCN'], MLP_scores=scores['MLP'])

    colors = np.array(['#176b91', '#bb554d'])[labels]
    rng = np.random.default_rng(71)
    xy = rng.normal(0, .32, (120, 2)); xy[:, 0] += (labels*2-1)*.8
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={'width_ratios':[1.25, 1]})
    for i, j in zip(*np.where(np.triu(adjacency, 1))):
        axs[0].plot(xy[[i,j],0], xy[[i,j],1], color='#b4c0c9', lw=.45, alpha=.35, zorder=0)
    axs[0].scatter(*xy.T, c=colors, s=24)
    axs[0].scatter(*xy[train].T, facecolors='none', edgecolors='black', s=85, linewidths=1.2)
    axs[0].set(title=label('关系图：黑圈为20个训练标签', 'Graph: rings mark 20 training labels'), aspect='equal')
    axs[0].axis('off')
    axs[1].scatter(features[:,0], features[:,1], c=colors, s=28, alpha=.7)
    axs[1].set(xlabel=label('节点特征1（无量纲）','Node feature 1 (dimensionless)'),
               ylabel=label('节点特征2（无量纲）','Node feature 2 (dimensionless)'),
               title=label('仅看特征，两个类别重叠','Features alone overlap'))
    fig.tight_layout(); save(fig, 'data')

    fig = plt.figure(figsize=(12, 7)); gs=fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax = fig.add_subplot(gs[:,0])
    for kind, c in [('MLP','#bb554d'), ('GCN','#176b91')]:
        values = np.asarray(traces[kind])[:,:,1]
        ax.plot(np.arange(1,151), np.mean(values,0), color=c, label=kind)
        ax.fill_between(np.arange(1,151), *np.quantile(values,[.25,.75],axis=0), color=c, alpha=.15)
    ax.set(xlabel=label('训练轮数','Epoch'), ylabel=label('验证交叉熵','Validation cross-entropy'),
           title=label('5次初始化：均值与四分位带','5 initializations: mean and interquartile band'))
    ax.legend()
    ax=fig.add_subplot(gs[0,1])
    for k, kind in enumerate(['MLP','GCN']):
        vals=scores[kind];ax.scatter(k+np.linspace(-.12,.12,5),vals,c=['#bb554d','#176b91'][k],s=50)
        ax.hlines(np.mean(vals),k-.25,k+.25,color=['#bb554d','#176b91'][k])
    ax.set(xticks=[0,1],xticklabels=['MLP','GCN'],ylim=(0,1.05),ylabel=label('测试准确率','Test accuracy'))
    ax=fig.add_subplot(gs[1,1]); logits=models['GCN'][1]
    pred=logits.argmax(1); confusion=np.zeros((2,2),int)
    for t in test: confusion[labels[t],pred[t]]+=1
    ax.imshow(confusion,cmap='Blues',vmin=0,vmax=40)
    for i in range(2):
        for j in range(2): ax.text(j,i,str(confusion[i,j]),ha='center',va='center',color='white' if confusion[i,j]>20 else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xlabel=label('预测类别','Predicted class'),
           ylabel=label('真实类别','True class'),title=label('GCN种子0：80个测试节点','GCN seed 0: 80 test nodes'))
    fig.tight_layout();save(fig,'results')

    n=36; ring=np.eye(n)
    for i in range(n): ring[i,(i-1)%n]=ring[i,(i+1)%n]=1
    ring/=3; signal=np.zeros(n); signal[:6]=1
    sequence=[signal.copy()]
    for _ in range(60): sequence.append(ring@sequence[-1])
    sequence=np.array(sequence)
    fig,axs=plt.subplots(1,3,figsize=(13,4),gridspec_kw={'width_ratios':[1.3,1,.9]})
    im=axs[0].imshow(sequence,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    axs[0].set(xlabel=label('环上节点编号','Node on a ring'),ylabel=label('平均传播次数','Averaging steps'),title=label('扩散信息，也磨平差别','Information spreads; contrast fades'))
    fig.colorbar(im,ax=axs[0],label=label('节点信号（无量纲）','Node signal (dimensionless)'))
    axs[1].semilogy(np.var(sequence,axis=1),color='#176b91')
    axs[1].set(xlabel=label('传播次数','Propagation steps'),ylabel=label('节点间方差','Variance across nodes'))
    v=vectors(points); rotated=points@rotation.T; vr=vectors(rotated)
    axs[2].quiver(*points.T,*v.T,color='#176b91',angles='xy',scale_units='xy',scale=1,label=label('原坐标','Original'))
    axs[2].quiver(*rotated.T,*vr.T,color='#bb554d',angles='xy',scale_units='xy',scale=1,label=label('旋转0.7 rad','Rotated 0.7 rad'))
    axs[2].scatter(*points.T,color='#176b91',s=12);axs[2].scatter(*rotated.T,color='#bb554d',s=12)
    axs[2].set(xlim=(-.7,1.6),ylim=(-.2,1.8),aspect='equal',xlabel='x',ylabel='y',title=label('向量随几何旋转','Vectors rotate with geometry'))
    axs[2].legend(fontsize=8)
    fig.tight_layout();save(fig,'structure')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
```

实际运行中，GCN 的五次测试准确率为 0.9875、0.9750、0.9750、0.9750、0.9750，平均 0.9775；MLP 的平均值为 0.4950。差别与生成机制一致：群体内密集连接提供了单个节点噪声特征之外的信息。图中的验证损失曲线帮助理解选取检查点的过程，散点保留五次运行各自的结果，混淆矩阵则展示种子 0 的 80 个测试节点如何分类。这里的高分对应这张具有明显同配结构的合成图。把跨群体连接概率提高，或让相邻节点更常属于不同类别，就会改变聚合带来的帮助。

![验证损失、测试准确率散点和测试混淆矩阵组成的多面板图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6807880f814f70a71d64fba2.svg?v=6807880f814f)

图 3实际运行结果。左：五次初始化的验证交叉熵均值与四分位带；右上：各次最优验证检查点的测试准确率，横线是均值；右下：GCN种子0在80个测试节点上的混淆矩阵。图和标签划分固定。

代码还有两项与准确率不同的检查。首先打乱节点编号，同时重排特征行和邻接矩阵的行列，比较预测在相同重排后的差值；最大绝对差约为 9.54×10⁻⁷，来自浮点运算次序。其次对一个由距离加权的向量消息做旋转，检查输出箭头是否一起旋转，误差约为 2.22×10⁻¹⁶。前一项检查普通 GCN 的节点置换性质，后一项检查单独构造的几何算子。它们回答的是结构一致性问题，与分类准确率分别提供不同证据。

## 7. 编号可以改变，物理对象不应跟着改变

给节点重新编号，好比给书架上的书重新贴索引号码。节点输出也应按同样顺序重排，这叫置换等变；若输出是整张图的一个数，则应保持不变，叫置换不变。平均、求和这类聚合不依赖邻居排列顺序，共享权重又不依赖节点名字，因此可以形成这种结构性质。训练时随机打乱编号有助于发现程序错误，但更直接的做法是从计算形式保证，并在代码中做一次数值对照。把节点编号当作连续特征输入，往往会重新引入与任务无关的顺序。

$$
f(PX,PAP^{\mathsf T})=P f(X,A)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/08b9af13817a89a808fad482.svg) | N×F节点特征矩阵与N×N邻接矩阵。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d12beb7c65071b9de7ea3da.svg) | N×N置换矩阵及转置，每行每列恰有一个1；无量纲，只重新排列索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 输出N×C节点分数的图模型；C为类别数，分数无量纲。 |

同时重排特征行以及邻接矩阵行列，相当于换编号。输出左边重新计算，右边只是把原输出换同样编号，二者应一致。若节点输出为(2,5,7)，交换前两个节点后应得到(5,2,7)。图级求和读出再把这些数相加，两种编号都为14，因此得到置换不变输出。浮点加法顺序变化可造成微小数值误差。

空间几何还有另一组变化。把一个分子或机械结构整体旋转，它的质量等标量性质保持不变，受力方向等向量性质则应该随坐标系旋转。普通 GCN 处理的是一般特征，直接把 x、y、z 坐标塞进输入，并不会自动得到旋转等变性。一个简单的构造是：用两点距离决定消息强度，用两点位移决定消息方向。距离不随旋转改变，位移随旋转改变，因此所有位移的加权和也会正确旋转。下面的公式把这种逻辑写成可检验的运算，长度先用同一尺度归一化。

$$
v_i=\sum_j\exp\!\left(-\|r_j-r_i\|^2\right)(r_j-r_i),\qquad v_i(Rr)=R\,v_i(r)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f69e9a731c172316bf6e0e05.svg) | 节点索引及位置向量，位置已除以参考长度，故坐标无量纲；代码使用二维，构造同样适用于三维。 |
| ![Formula](https://ml-biomat.com/static/agent-math/247c126e566140ca1dceb95f.svg) | 欧氏距离及聚合向量；本例均以归一化坐标为单位，j=i项为零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2d823743d6fb81798bf85e6a.svg) | 满足RᵀR=I、detR=1的旋转矩阵、所有节点位置的集合及旋转后的集合；vᵢ(Rr)表示用新坐标重新计算。 |

旋转保持距离，所以指数权重不变；位移变成R(rj−ri)，公共的R可以移到求和外，便得到等变关系。两个点(0,0)、(1,0)时，第一点收到(e⁻¹,0)≈(0.3679,0)；逆时针旋转90度后，消息变成(0,0.3679)。这是一个精确设计的向量算子，代码单独验证它，没有把它冒充为经过训练的三维网络。

Geiger 与 Smidt 在 2022 年介绍的 e3nn，把标量、向量及更一般的几何张量放入统一的可学习等变运算框架。实际三维模型可使用球谐函数、张量积和与距离相关的网络，让方向信息在各层保持一致的变换规律。本章的小向量算子保留了其中最易手算的一部分：几何量应怎样随坐标变化。若任务需要区分镜像结构，还要区分旋转和反射的要求；若边由距离阈值建立，旋转后应使用同一阈值和数值精度规则，避免构图误差破坏预期对称性。

## 8. 传播得远，也要保留值得区分的差别

反复平均会发生什么？想象环形水槽里有一小段染料，每一步都让当前位置与左右邻居混合。开始时信号局限于少量节点，随后逐渐扩散，邻居之间的差别也越来越小。图中的热图用 36 个节点和纯平均传播展示这个过程：横轴是节点位置，纵轴是传播次数，颜色表示信号；旁边的方差曲线量化节点差别如何下降。这是过平滑的一种清楚机制。实际网络还包含权重、非线性、残差和归一化，因此应把这种实验当作分析传播的起点，再测量训练模型各层表示的变化。

![传播次数与节点的信号热图、方差曲线以及旋转前后向量箭头。](https://ml-biomat.com/static/tutorials/machine-learning/figures/a23458fece8310d79f688f2f.svg?v=a23458fece83)

图 4左与中：36节点环上纯平均传播，初始6节点信号为1，其余为0；信号扩散、节点间方差下降。右：独立的距离加权向量算子在旋转0.7 rad后方向一起旋转。两组计算用于分析结构性质，与训练分类指标分开。

另一个问题是表达能力。假设所有节点最初的特征都相同，而且每个节点都有两个邻居，那么普通局部消息传递会在每一层收到相同的邻居多重集合。一个六节点环与两个三节点环，可以因此给所有节点产生相同表示；求和或平均读出也可能分不出这两张同样有六个节点的图。这个例子说明，局部聚合掌握的信息有明确边界。加入能反映整体结构的位置编码、使用更高阶关系或针对任务设计子结构特征，都在为模型补充原有消息无法区分的内容。

过挤压则关注另一件事：许多远处节点的信息经过少数连接，被压进固定宽度的向量。增加层数虽然扩大了可见范围，也可能让这条信息通道更加拥挤。改进连边、残差路径、全局注意力或层次化读出，各自改变的是不同的信息瓶颈；代价也可能体现为计算量或构图假设。一个实用的研究顺序是先定义关系和预测时刻，再建立 MLP 与浅层 GCN 的对照，检查标签划分与错误节点，最后用明确的失败模式推动模型升级。这样每增加一个模块，都能回答它解决了哪一种具体困难。

你可以用现有代码继续做一个小研究：保持特征、标签划分和优化参数不变，只改变跨群体连边概率，重复生成多个图，再观察 GCN 相对 MLP 的增益怎样变化。每次同时记录平均节点度、同类相连比例和测试结果，就能把“图有帮助”拆成可解释的条件。再做一次删边实验，比较随机删边与删除跨群体边的效果，会发现边的数量和边携带的信息不是同一个概念。由此得到的不是某个网络名称的胜负，而是关系表示为什么适合当前问题的证据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M22.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [A Gentle Introduction to Graph Neural Networks](https://distill.pub/2021/gnn-intro/)

   关系表示、消息传递可视化及本章采用的原图。

   Original diagrams and text CC BY 4.0; selected original GCN image unmodified.
2. [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)

   GCN传播规则、半监督节点分类与谱图解释。
3. [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216)

   GraphSAGE聚合与邻居采样。
4. [Graph Attention Networks](https://arxiv.org/abs/1710.10903)

   基于局部特征的注意力权重。
5. [e3nn: Euclidean Neural Networks](https://arxiv.org/abs/2207.09453)

   几何张量与欧氏等变网络框架。
