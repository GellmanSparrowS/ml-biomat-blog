# 让训练走稳：优化器、尺度与泛化

Source: https://ml-biomat.com/tutorials/machine-learning/m10/
Language: zh-CN

从一次能手算的更新，到真实网络的损失、梯度和学习率。

## 模型已经搭好，为什么还学不动

学骑自行车时，方向正确还不够：转把过猛会左右摇摆，动作太小又来不及纠正偏离。训练神经网络也有类似问题。损失告诉我们预测与目标相差多少，梯度给出局部变化方向，优化器则把这些信息转成参数更新。即使网络结构和数据完全相同，更新幅度、历史梯度的使用方式、初始参数的尺度，都可能让训练过程呈现很不一样的曲线。

本章围绕一个可观察的问题展开：用带噪声的数据学习一条弯曲关系，怎样让网络稳定地接近它，又保留对新观测的预测能力？我们先在可以看清全貌的二维地形上理解 SGD、动量和 Adam，再用真正的多层网络记录误差、梯度范数和学习率。二维地形帮助解释更新规则，真实网络的训练曲线则回答实验中发生了什么；两者承担不同的教学任务。

训练设置并不是一袋可以随意叠加的技巧。初始化影响信号怎样进入深层网络，归一化改变中间表示的尺度，正则化改变模型可以依赖哪些细节，超参数搜索决定如何比较这些选择。把它们放在同一个诊断流程里，才能回答“改了什么，为什么改，观察什么结果”。到章末，你将能够读懂一条训练曲线背后的计算，设计小规模对照，并保存足以继续训练或复现实验的状态。

## 从坡度到一步更新

假设损失是一张地形图，参数是地图上的坐标，目标是找到较低的位置。梯度指出当前位置上升最快的方向，因此取负梯度得到局部下降方向。学习率决定沿这个方向走多远。这种局部信息只描述当前位置附近的变化，步子很大时可能越过谷底，落到另一侧更高的位置。损失是否下降，需要由更新后的计算检验，不能仅凭“沿负梯度走”就推断任意步长都合适。

$$
\theta_{t+1}=\theta_t-\eta g_t,\quad g_t=\frac1B\sum_{j\in\mathcal B_t}\nabla_\theta\ell_j(\theta_t);\qquad F(x,y)=\tfrac12(x^2+25y^2)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/579b56236a900400be4c8491.svg) | 第t次更新前的P个模型参数，本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 正学习率，控制更新幅度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a8bc9a9919727860a99c5f29.svg) | 批平均梯度；∇表示对各参数求偏导组成的向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f55e53533c50f03e00925fd7.svg) | 批大小、当前批样本索引集合、一个样本索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b3f25829030c7309d95691ef.svg) | 样本j的损失；本章回归用无量纲目标的平方误差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/543e180ef21c4f915f1da00f.svg) | 另一个二维教学目标及其两个标量参数，与真实网络参数分开。 |

先把批内每个样本的梯度相加再除以批大小，得到用于本次更新的方向。二维目标的梯度为(x,25y)：在(3,1)处使用学习率0.07，下一点为(2.79,−0.75)，目标从17降到10.9233。曲率较大的纵向坐标会跨过谷底。

完整数据集上的平均损失可能包含数百万个样本，每次更新都遍历全部数据会很慢。小批量 SGD 用一组抽样观测的平均梯度近似总体梯度，在计算成本与估计波动之间折中。一个批次恰好含有较难的样本，损失会暂时升高；打乱样本顺序能避免始终按同一种顺序看到数据，却不会消除抽样噪声。比较训练曲线时，应明确画的是某个批次的损失，还是固定训练集、验证集上的完整平均值。

随机近似的研究为这种“用有噪声的局部观测逐步改善参数”的思路提供了早期基础。对今天的小批量训练而言，重要的是认识到更新方向本来就带有波动。因此，批大小、学习率和训练轮数需要一起看：同样的一轮，批越小，参数更新次数越多；同样的一百次更新，模型可能看过很不一样数量的样本。记录计算预算时同时保留轮数、批大小和样本数，会让实验之间更容易比较。

![二维解析目标F=(x²+25y²)/2上的60步轨迹，从(3,1)出发。SGD和动量步长0.07，动量系数0.6；Adam步长0.15。星号为极小点，灰线为同一组等高线；这三幅图展示更新规则，非真实网络损失面的降维。](https://ml-biomat.com/static/tutorials/machine-learning/figures/ebf547a245d4fd6a3b6fe4be.svg?v=ebf547a245d4)

图 1二维解析目标F=(x²+25y²)/2上的60步轨迹，从(3,1)出发。SGD和动量步长0.07，动量系数0.6；Adam步长0.15。星号为极小点，灰线为同一组等高线；这三幅图展示更新规则，非真实网络损失面的降维。

图中的谷地在纵向更陡。普通 SGD 在陡方向上容易来回跨越，而在平缓方向上前进较慢。这个例子可以手算：从坐标(3,1)出发，梯度为(3,25)，学习率0.07得到下一点(2.79,−0.75)。纵坐标变号，说明一步跨过了谷底；下一步梯度的纵向符号又会改变。等高线与轨迹放在一起，正好解释了这种来回摆动的来源。

## 记住过去的方向，再调整各坐标的步幅

动量法给优化器增加一个会逐渐遗忘的历史梯度累积量。如果某个方向上的梯度反复同向，累积会增强沿该方向的推进；如果梯度交替变号，前后贡献会部分抵消。可以把它想成推一辆有惯性的小车，不过计算中的“速度”是算法变量，和真实物体的速度单位没有关系。它保存的是更新方向的历史，因此恢复训练时，除了模型权重，还需要保存优化器的这个状态。

$$
v_t=\mu v_{t-1}+g_t,\qquad\theta_{t+1}=\theta_t-\eta v_t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c584295e8446c89497dad165.svg) | 当前和前一次的梯度累积，初始为零，与参数形状相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dab423e802bb7a0f16e23576.svg) | 历史保留系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/73bc71e9a241c8ca2cbf3b44.svg) | 当前批梯度、模型参数和正学习率；t为更新编号。 |

历史贡献每过一步乘以μ，因此较早的梯度逐渐减弱。若连续两步标量梯度都是2、μ=0.9、初始累积为0，则v依次为2、3.8；学习率0.1时对应更新幅度0.2、0.38。若第二步梯度变成−2，新的累积为−0.2，前后方向部分抵消。本章使用未乘(1−μ)的累积约定。

Adam 进一步分别记录梯度的一阶矩和二阶矩：前者反映近期方向，后者反映各坐标近期梯度平方的大小。用二阶矩的平方根调整更新，有助于处理不同参数坐标的尺度差异。Kingma 与 Ba 在2014年底公开论文，并在2015年 ICLR 发表这项工作；它面对的是有噪声、维度高、不同坐标行为差异明显的优化任务。理解这个背景后，默认参数就不再像一组需要死记的神秘数字。

$$
\begin{aligned}m_t&=\beta_1m_{t-1}+(1-\beta_1)g_t\\v_t&=\beta_2v_{t-1}+(1-\beta_2)g_t^{\odot2}\\\widehat m_t&=m_t/(1-\beta_1^t),\quad\widehat v_t=v_t/(1-\beta_2^t)\\\theta_{t+1}&=\theta_t-\eta\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6547e8510550e1844593df44.svg) | 梯度一阶矩、二阶原点矩的指数累积；此处v为平方梯度累积，与动量式的v约定不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d5c57a727bc90b1421a0594a.svg) | 两个历史保留系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a6cadede5ab9cb27f1e8004.svg) | 每个梯度分量分别平方，不是向量内积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/784f6a437e83ae47a34d6590.svg) | 从零初始化后经过偏差修正的矩估计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3ec959b931716b50d217ab86.svg) | 参数向量、学习率、从1开始的更新编号；幂t表示重复乘方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | 正稳定常数，防止除以零；平方根、除法均逐元素进行。 |

第一步g=2、β₁=0.9、β₂=0.999，得到m=0.2、v=0.004；除以0.1和0.001后分别为2和4。取η=0.1且ε远小于2，更新约0.1。二阶矩记录的是平方大小，没有先减均值，因此不等同于梯度方差。本文数据与参数均无量纲。

一阶矩和二阶矩最初都从零开始，最早几步会因此偏小，偏差修正项就是用来校正这一初始化影响。以第一步梯度2为例，取衰减系数0.9和0.999，一阶累积为0.2，二阶累积为0.004；修正后分别恢复为2和4，平方根为2。在忽略极小稳定项时，学习率0.1带来的更新幅度约为0.1，而普通 SGD 的幅度为0.2。这个算例展示了缩放机制，并不意味着所有坐标永远以相同步幅移动。

AdamW 把权重衰减从自适应梯度计算中分开。若直接把平方权重惩罚加入 Adam 的损失，它产生的梯度也会进入矩估计并受到各坐标缩放；AdamW 则单独执行权重收缩，再进行基于数据梯度的更新。Loshchilov 与 Hutter 的工作澄清了两者在自适应优化器中的区别。在普通 SGD 中，两种形式可以通过系数对应；在 Adam 中，不能只看参数名里都出现“weight decay”就认为运算完全相同。

$$
\theta_{t+1}=(1-\eta\lambda)\theta_t-\eta u_t,\qquad u_t=\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d7d3e8046bf6405ded6e3db6.svg) | 本次更新前、后的模型参数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ed54e1e1abcc42b8081bb761.svg) | 学习率、非负权重衰减强度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9614d82ed7278eec4d4b3690.svg) | 由数据损失梯度形成的Adam自适应方向。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dae8c74f82086ba6034ccff4.svg) | 上一式中的修正矩与稳定常数，均逐坐标使用。 |

先按1−ηλ收缩原权重，再减去自适应更新。标量θ=2、η=0.1、λ=0.01、u=0.5时，收缩后1.998，更新后1.948。若平方权重惩罚直接进入数据梯度，它也会影响矩估计，得到的通常是不同更新。

## 学习率不是从头到尾都要一样

训练刚开始时，参数、优化器的矩估计和中间表示都在快速变化。预热让学习率先从较小值逐步升高，给这些状态一个逐渐建立的过程。后期再降低学习率，可以减少在较好区域附近的来回摆动。预热不是每个任务都必须添加的步骤，它的作用应通过早期梯度和损失变化来观察。本章让 AdamW 使用五轮线性预热和随后余弦下降，把这个变化直接画在真实训练曲线旁边。

调度器还可以按固定间隔衰减，或在验证指标长期没有改善时调整。固定调度只依赖训练进度，指标驱动调度需要事先定义监测对象、改善阈值和等待长度。无论采用哪一种，都要明确调度的时间单位是批次还是训练轮；把原本每轮更新的调度器放进每个批次，会使学习率过早下降。恢复训练也需要恢复调度进度，否则同一组权重接下来的更新规则会改变。

寻找学习率时，可以先选几个相差数倍的候选，在相同训练片段上观察。过大时，损失常出现持续放大或频繁剧烈震荡；过小时，训练损失长期缓慢变化。还要结合梯度看：如果梯度本身几乎为零，单纯放大学习率可能只是掩盖激活饱和或计算图断开的原因。先弄清更新量小是因为步长小，还是因为可用梯度小，能减少盲目试参。

## 让信号穿过深层网络

把一个信号连续乘以很小的数，它会迅速变弱；反复乘以很大的数，则可能迅速放大。多层网络中的权重和激活导数也会不断改变信号尺度。所有权重都设成同一个值，还会让同一层的神经元得到相同的更新，难以学出不同特征。随机初始化打破这种对称性，而合适的方差让信息在进入深层网络时保持可用尺度。对于 ReLU 网络，Kaiming 初始化把输入连接数和激活截断的影响一起纳入方差选择。

$$
\operatorname{Var}(W_{ij})\approx\frac{2}{n_{\mathrm{in}}}\qquad\text{(ReLU, fan-in initialization)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33a5218183f1f6f9bd612ba0.svg) | 从输入连接j到输出单元i的初始权重，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | 随机初始化分布的方差，即标准差的平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/58e3dd04ac34d0fb80ebff55.svg) | 每个输出单元的输入连接数；卷积层还包含核的空间位置与输入通道。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31dfd422ce48f185cc9b8c28.svg) | 在独立、近似对称输入与相关尺度假设下使用的初始化尺度。 |

求和使方差随输入连接数增加，ReLU截掉负半轴，又改变信号的二阶矩，因此该尺度用2/n_in补偿。n_in=64时，方差为0.03125，标准差约0.17678。它给出初始化分布，不要求每个网络层实测标准差都恰好等于1；训练后权重也会改变。

![左：1024个64维输入通过十层随机ReLU网络的激活标准差，纵轴为对数尺度。右：一个2×3输入矩阵分别经过BatchNorm与LayerNorm，图内保留数值；关闭可学习仿射项，使用当前输入统计。色标分别标明原始值和归一化值。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f847ff2849d242fba263fccf.svg?v=f847ff2849d2)

图 2左：1024个64维输入通过十层随机ReLU网络的激活标准差，纵轴为对数尺度。右：一个2×3输入矩阵分别经过BatchNorm与LayerNorm，图内保留数值；关闭可学习仿射项，使用当前输入统计。色标分别标明原始值和归一化值。

图左让同一批随机输入通过十层未经训练的 ReLU 网络。权重标准差0.02时，输出标准差逐层缩小到约3.00×10⁻¹⁰；取0.5时则增大到约2.86×10⁴；本例Kaiming初始化下，末层约为0.873。这里直接测的是前向激活尺度，梯度还取决于损失、反向路径和激活导数。将这些分开观察，才能避免把“输出幅度正常”当成训练一定顺利的充分条件。

BatchNorm 与 LayerNorm 都包含减去均值、除以标准差的操作，关键区别在于统计哪些数。对本章二维的“样本×特征”矩阵，BatchNorm 按特征列跨样本计算，LayerNorm 按每个样本的特征行计算。图中两行输入分别为(1,2,3)和(7,8,9)：按列处理后，两行分别接近全−1与全1；按行处理后，两行都约为(−1.225,0,1.225)。统计轴的选择改变了模型保留哪些相对差异。

$$
\mu=\frac1K\sum_{k=1}^K a_k,\quad s^2=\frac1K\sum_{k=1}^K(a_k-\mu)^2,\quad z_k=\gamma\frac{a_k-\mu}{\sqrt{s^2+\epsilon}}+\delta
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/25b7529c6c6e8acf6c9d1467.svg) | 被一起统计的K个激活及其索引；BatchNorm和LayerNorm选取的集合不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/db147e2c758c6819e9100826.svg) | 该组均值和使用除数K的方差；激活按本例无量纲处理。 |
| ![Formula](https://ml-biomat.com/static/agent-math/216c15b93ccea50c6180bd15.svg) | 归一化并可学习缩放后的激活。 |
| ![Formula](https://ml-biomat.com/static/agent-math/935db6a7235228a2cbcc207a.svg) | 可学习的缩放和偏移；图中关闭此仿射变换，等效γ=1、δ=0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | 小正稳定项，与方差相加。 |

对一行(1,2,3)，均值2、方差2/3，忽略微小ε后得到(−1.224745,0,1.224745)。对第一列(1,7)，均值4、方差9，得到(−1,1)。图用ε=10⁻⁵，因而末位略有差异。训练用批内统计与保存的运行统计是不同对象，库的运行方差更新约定需随实现核对。

实际 BatchNorm 通常在训练时更新运行均值与方差，在评价时使用保存的统计量；LayerNorm 按当前样本计算，不依赖其他样本组成。小批量、序列长度变化和训练评价模式切换，都会影响如何使用这些层。残差连接则提供另一种改善信息传递的结构：让一个模块学习对输入的增量，输出为输入加上这个增量。当输入与输出形状相同，直接路径可以把已有表示传下去，梯度也有一条较直接的回路；形状变化时需要投影或相应匹配。

## 训练误差下降之后，还要看新数据

网络可以把有限观测中的偶然噪声也拟合进去。正则化的作用，是改变哪些拟合方式更容易被学习过程选中。权重衰减倾向于压缩参数幅度，Dropout 在训练时随机屏蔽部分激活，使预测不总是依赖同一组内部通路，数据增强则把任务允许的变化带进训练样本。三者作用的位置不同，也不会对所有数据产生同样结果。选择时应先明确任务里什么变化应当保持答案不变。

$$
\widetilde h_j=\frac{r_jh_j}{1-p},\qquad r_j\sim\operatorname{Bernoulli}(1-p),\qquad\mathbb E[\widetilde h_j\mid h_j]=h_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cdb0bc656b138d5994913397.svg) | 第j个原激活、训练时Dropout输出，形状相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cea5cff4355d5a0ddba5f6a5.svg) | 丢弃概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ac93bfc1786051ffd5b120d4.svg) | 取1表示保留、取0表示丢弃的随机掩码。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1b610de9cb237fff7dda30ae.svg) | 以概率1−p取1的分布。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5042ed00f6677baad4f282ea.svg) | 固定原激活后，对随机掩码取平均。 |

取h=1、p=0.25，输出以0.75概率为4/3，以0.25概率为0，平均为1。期望保持不变不意味着每次前向结果相同。PyTorch的这一约定在评价模式直接输出原激活；无需再次乘保留概率。

Dropout 的训练输出通常对保留的激活进行反向缩放。丢弃概率0.25时，保留概率为0.75，保留下来的值除以0.75，因此平均值保持原尺度。本章对十万个值为1的输入实际采样，平均输出约1.00279；进入评价模式后，同一层直接返回输入。一次训练前向与一次评价前向的差异来自模式定义，而不是模型参数被修改了。比较训练和验证误差时，也应注意训练损失是否是在启用 Dropout 的状态下记录的。

数据增强需要保护目标含义。识别普通物体时，小幅裁剪或亮度变化常保留类别；识别数字时，随意旋转可能把某些符号变成别的符号；计量图像中改变颜色或尺寸还可能改变要预测的物理量。应把增强理解成对“哪些变换不影响标签”的明确假设，并检查增强后的样本。测试集则按照预先定义的评价流程处理，避免用训练时的随机变化无意改变比较条件。

## 同一网络的四条训练记录

完整程序用正弦函数与线性项组成一个已知的均值关系，再加入标准差0.2的高斯噪声。训练、验证、测试分别独立生成96、240和400个观测。四个模型使用相同的网络初始参数与批次顺序：SGD和动量学习率为0.03，Adam为0.01，AdamW峰值为0.01并使用0.01的权重衰减及预热、余弦调度。每种配置训练160轮，按自己的验证误差选择保存参数。

### 完整Python：优化、激活尺度与验证搜索

依赖NumPy、Matplotlib、PyTorch；运行python main.py --output results --language zh。程序产生五组SVG、数值摘要、数据轨迹与四个模型参数文件。所有模型固定种子，使用CPU双线程；小批量损失反向传播之后先测梯度再更新，绘图数据可在experiment.npz及summary.json中重新读取。

```
"""Optimization, activation scale, and normalization experiments on CPU."""
from pathlib import Path
import argparse,copy,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn

def data(n,seed):
    rng=np.random.default_rng(seed);x=rng.uniform(-3,3,(n,1)).astype('float32')
    clean=np.sin(1.7*x)+.15*x
    y=clean+rng.normal(0,.2,x.shape).astype('float32')
    return torch.from_numpy(x),torch.from_numpy(y)

def network():return nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))

def continuation_check(output, train):
    """An epoch-boundary checkpoint with optimizer, schedule, and two RNG states."""
    def make():
        return nn.Sequential(nn.Linear(1,16),nn.ReLU(),nn.Dropout(.25),nn.Linear(16,1))
    schedule={'base_lr':.01,'total_epochs':5,'minimum_fraction':.1}
    def update(model,opt,batch_rng,epoch,config):
        rate=config['base_lr']*(config['minimum_fraction']+(1-config['minimum_fraction'])*
             (1+math.cos(math.pi*epoch/config['total_epochs']))/2)
        for group in opt.param_groups:group['lr']=rate
        indices=torch.randperm(len(train[0]),generator=batch_rng)
        model.train();losses=[]
        for batch in indices.split(32):
            opt.zero_grad(set_to_none=True)
            loss=nn.functional.mse_loss(model(train[0][batch]),train[1][batch])
            loss.backward();opt.step();losses.append(loss.detach().clone())
        return indices,torch.stack(losses).mean(),rate
    torch.manual_seed(190);model=make();opt=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=.01)
    batch_rng=torch.Generator().manual_seed(191)
    for epoch in [1,2]:update(model,opt,batch_rng,epoch,schedule)
    torch.save({'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':2,
                'schedule':schedule,'batch_rng':batch_rng.get_state(),
                'torch_rng':torch.get_rng_state()},output/'continuation.pt')
    original_indices,original_loss,rate=update(model,opt,batch_rng,3,schedule)
    saved=torch.load(output/'continuation.pt',weights_only=True)
    restored=make();restored.load_state_dict(saved['model'])
    restored_opt=torch.optim.AdamW(restored.parameters(),lr=.01,weight_decay=.01)
    restored_opt.load_state_dict(saved['optimizer'])
    restored_rng=torch.Generator();restored_rng.set_state(saved['batch_rng'])
    # Restore global RNG after constructing the new network, before dropout runs.
    torch.set_rng_state(saved['torch_rng'])
    indices,loss,restored_rate=update(restored,restored_opt,restored_rng,saved['epoch']+1,saved['schedule'])
    error=max((p-q).abs().max().item() for p,q in zip(model.parameters(),restored.parameters()))
    result={'saved_epoch':2,'next_epoch':3,'learning_rate':rate,'restored_learning_rate':restored_rate,
            'batch_match':bool(torch.equal(original_indices,indices)),
            'loss_error':abs(original_loss.item()-loss.item()),'parameter_max_error':error,
            'optimizer_step':int(next(iter(restored_opt.state.values()))['step'].item())}
    assert result['batch_match'] and error==0 and result['loss_error']==0
    return result

def fit(kind,lr,decay,train,val,epochs=160):
    torch.manual_seed(101);model=network()
    if kind=='SGD':opt=torch.optim.SGD(model.parameters(),lr=lr)
    elif kind=='Momentum':opt=torch.optim.SGD(model.parameters(),lr=lr,momentum=.9)
    elif kind=='Adam':opt=torch.optim.Adam(model.parameters(),lr=lr,weight_decay=decay)
    else:opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=decay)
    generator=torch.Generator().manual_seed(102);hist=[];best=float('inf');state=None;epoch_best=0
    for epoch in range(1,epochs+1):
        # AdamW alone demonstrates warmup followed by cosine decay.
        scale=min(epoch/5,1)*(0.1+0.9*(1+math.cos(math.pi*max(epoch-5,0)/max(epochs-5,1)))/2) if kind=='AdamW' else 1
        for group in opt.param_groups:group['lr']=lr*scale
        norms=[];model.train()
        for ix in torch.randperm(len(train[0]),generator=generator).split(32):
            opt.zero_grad(set_to_none=True);loss=nn.functional.mse_loss(model(train[0][ix]),train[1][ix]);loss.backward()
            norm=torch.sqrt(sum(p.grad.square().sum() for p in model.parameters())).item();norms.append(norm)
            assert math.isfinite(norm);opt.step()
        model.eval()
        with torch.no_grad():tl=nn.functional.mse_loss(model(train[0]),train[1]).item();vl=nn.functional.mse_loss(model(val[0]),val[1]).item()
        hist.append([epoch,tl,vl,float(np.mean(norms)),lr*scale])
        if vl<best:best=vl;state=copy.deepcopy(model.state_dict());epoch_best=epoch
    model.load_state_dict(state);return model,np.array(hist),best,epoch_best

def run(output,language):
    output.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    train=data(96,103);val=data(240,104);test=data(400,105);grid=torch.linspace(-3,3,400)[:,None]
    configurations={'SGD':(.03,0),'Momentum':(.03,0),'Adam':(.01,0),'AdamW':(.01,.01)}
    models={};histories={};metrics={};colors=['#0072B2','#D58500','#008675','#98558b']
    for name,(lr,decay) in configurations.items():
        model,h,best,epoch=fit(name,lr,decay,train,val);models[name]=model;histories[name]=h
        with torch.no_grad():mse=nn.functional.mse_loss(model(test[0]),test[1]).item()
        metrics[name]={'learning_rate':lr,'weight_decay':decay,'best_epoch':epoch,'validation_mse':best,'test_mse':mse}
        torch.save(model.state_dict(),output/f'{name}.pt')
    fig=plt.figure(figsize=(12,8),layout='constrained');gs=fig.add_gridspec(2,2)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(train[0],train[1],s=12,alpha=.5,color='#89939b',label=tr('训练观测 n=96','Training observations n=96'))
    ax.plot(grid,torch.sin(1.7*grid)+.15*grid,color='#25333d',lw=2,ls='--',label=tr('生成均值','Generating mean'))
    for (name,model),color in zip(models.items(),colors):
        with torch.no_grad():ax.plot(grid,model(grid),color=color,label=name)
    ax.set(xlabel=tr('输入 x（无量纲）','Input x (dimensionless)'),ylabel=tr('目标 y（无量纲）','Target y (dimensionless)'));ax.legend(fontsize=8,ncol=2)
    ax=fig.add_subplot(gs[0,1])
    for (name,h),color in zip(histories.items(),colors):ax.semilogy(h[:,0],h[:,2],color=color,label=name)
    ax.axhline(.2**2,color='#89939b',ls=':',label=tr('噪声方差 0.04','Noise variance 0.04'));ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('验证均方误差','Validation MSE'));ax.legend(fontsize=8)
    ax=fig.add_subplot(gs[1,0])
    for (name,h),color in zip(histories.items(),colors):ax.semilogy(h[:,0],h[:,3],color=color,label=name)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('批梯度范数的轮内平均','Epoch mean of batch gradient norm'))
    ax=fig.add_subplot(gs[1,1])
    for (name,h),color in zip(histories.items(),colors):ax.plot(h[:,0],h[:,4],color=color,label=name)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('学习率','Learning rate'));ax.legend(fontsize=8)
    fig.savefig(output/f'training-{language}.svg');plt.close(fig)

    paths={}
    for name in ['SGD','Momentum','Adam']:
        p=torch.tensor([3.,1.],requires_grad=True)
        opt=torch.optim.SGD([p],lr=.07,momentum=.6 if name=='Momentum' else 0) if name!='Adam' else torch.optim.Adam([p],lr=.15)
        path=[p.detach().numpy().copy()]
        for _ in range(60):opt.zero_grad();(.5*(p[0]**2+25*p[1]**2)).backward();opt.step();path.append(p.detach().numpy().copy())
        paths[name]=np.array(path)
    xx,yy=np.meshgrid(np.linspace(-.5,3.5,180),np.linspace(-1.1,1.2,140));zz=.5*(xx**2+25*yy**2)
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    for ax,((name,path),color) in zip(axes,zip(paths.items(),colors)):
        ax.contour(xx,yy,zz,levels=[.05,.2,.5,1,2,4,8,16],colors='#ccd4db',linewidths=.8);ax.plot(path[:,0],path[:,1],'-o',color=color,ms=2);ax.scatter([0],[0],marker='*',s=80,color='#263b43')
        ax.set(title=name,xlabel=tr('参数 x','Parameter x'),ylabel=tr('参数 y','Parameter y'),xlim=(-.5,3.5),ylim=(-1.1,1.2))
    fig.savefig(output/f'terrain-{language}.svg');plt.close(fig)

    # Feed the same random vectors through ten untrained ReLU layers.
    torch.manual_seed(106);initial=torch.randn(1024,64);activation={}
    for scheme in ['small','large','kaiming']:
        torch.manual_seed(107);h=initial.clone();stds=[]
        for _ in range(10):
            w=torch.empty(64,64)
            if scheme=='kaiming':nn.init.kaiming_normal_(w,nonlinearity='relu')
            else:nn.init.normal_(w,std=.02 if scheme=='small' else .5)
            h=torch.relu(h@w.T);stds.append(float(h.std()))
        activation[scheme]=stds
    matrix=torch.tensor([[1.,2.,3.],[7.,8.,9.]])
    bn=nn.BatchNorm1d(3,affine=False,track_running_stats=False);ln=nn.LayerNorm(3,elementwise_affine=False)
    bn_values=bn(matrix).detach().numpy();ln_values=ln(matrix).detach().numpy()
    fig=plt.figure(figsize=(12,4.5),layout='constrained');gs=fig.add_gridspec(1,4,width_ratios=[1.8,1,1,1])
    ax=fig.add_subplot(gs[0,0])
    for (name,values),color in zip(activation.items(),colors):ax.semilogy(range(1,11),values,'-o',label=tr({'small':'小权重','large':'大权重','kaiming':'Kaiming'}[name],name),color=color)
    ax.set(xlabel=tr('层数','Layer index'),ylabel=tr('ReLU输出标准差','Standard deviation of ReLU outputs'));ax.legend(fontsize=8)
    for j,(name,a) in enumerate([('Input',matrix.numpy()),('BatchNorm',bn_values),('LayerNorm',ln_values)]):
        ax=fig.add_subplot(gs[0,j+1]);im=ax.imshow(a,cmap='RdBu_r',vmin=-2 if j else 0,vmax=2 if j else 9)
        for r in range(2):
            for c in range(3):ax.text(c,r,f'{a[r,c]:.2f}',ha='center',va='center',color='white' if (j==0 and a[r,c]>6) or (j>0 and abs(a[r,c])>1) else '#182a34',fontsize=10)
        ax.set(title=tr('原始输入',name) if j==0 else name,xticks=[0,1,2],xticklabels=[1,2,3],yticks=[0,1],yticklabels=[1,2],xlabel=tr('特征','Feature'),ylabel=tr('样本','Sample'))
        fig.colorbar(im,ax=ax,shrink=.5)
    fig.savefig(output/f'scale-{language}.svg');plt.close(fig)

    # A transparent, validation-only hyperparameter grid. Test data are untouched.
    rates=[.001,.003,.01];decays=[0,.01,.1];search=np.zeros((3,3))
    for row,decay in enumerate(decays):
        for col,lr in enumerate(rates):_,_,score,_=fit('AdamW',lr,decay,train,val,epochs=60);search[row,col]=score
    fig,ax=plt.subplots(figsize=(7.2,4.8),layout='constrained');im=ax.imshow(search,cmap='viridis_r')
    for r in range(3):
        for c in range(3):ax.text(c,r,f'{search[r,c]:.4f}',ha='center',va='center',color='white' if search[r,c]>.15 else '#152e32')
    ax.set(xticks=range(3),xticklabels=rates,yticks=range(3),yticklabels=decays,xlabel=tr('峰值学习率','Peak learning rate'),ylabel=tr('AdamW权重衰减','AdamW weight decay'))
    fig.colorbar(im,ax=ax,label=tr('最佳验证均方误差（60轮预算）','Best validation MSE (60-epoch budget)'))
    fig.savefig(output/f'search-{language}.svg');plt.close(fig)
    # Reproduce two concrete failures with a separate, matched short budget.
    failure_traces={}
    for rate in [.03,1.0]:
        torch.manual_seed(101);model=network();opt=torch.optim.SGD(model.parameters(),lr=rate);losses=[]
        for step in range(30):
            opt.zero_grad();loss=nn.functional.mse_loss(model(train[0]),train[1]);value=float(loss.detach());losses.append(value)
            if not math.isfinite(value) or value>1e10:break
            loss.backward();opt.step()
        failure_traces[str(rate)]=losses
    rng=np.random.default_rng(109);permutation=rng.permutation(len(train[0]))
    _,_,clean_score,_=fit('Adam',.01,0,train,val,epochs=80)
    _,_,shuffled_score,_=fit('Adam',.01,0,(train[0],train[1][permutation]),val,epochs=80)
    fig,axes=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
    for rate,losses in failure_traces.items():axes[0].semilogy(np.arange(len(losses)),losses,'-o',ms=3,label=tr('学习率 ','rate ')+rate)
    axes[0].set(xlabel=tr('完整批更新步数','Full-batch update'),ylabel=tr('训练均方误差','Training MSE'));axes[0].legend()
    axes[1].bar([0,1],[clean_score,shuffled_score],color=['#0072B2','#D58500'],width=.55)
    axes[1].set(xticks=[0,1],xticklabels=[tr('对应正确','Aligned targets'),tr('打乱标签','Shuffled targets')],ylabel=tr('最佳验证均方误差','Best validation MSE'))
    for j,v in enumerate([clean_score,shuffled_score]):axes[1].text(j,v,f'{v:.4f}',ha='center',va='bottom')
    fig.savefig(output/f'diagnostics-{language}.svg');plt.close(fig)
    # Deterministic dropout probe: inverted dropout preserves expectation.
    torch.manual_seed(108);drop=nn.Dropout(.25);probe=drop(torch.ones(100000));drop.eval();eval_equal=bool(torch.equal(drop(torch.ones(20)),torch.ones(20)))
    summary={'train_n':96,'validation_n':240,'test_n':400,'noise_std':.2,'epochs':160,'models':metrics,'quadratic_final':{k:float(.5*(v[-1,0]**2+25*v[-1,1]**2)) for k,v in paths.items()},'activation_std':activation,'batchnorm':bn_values.tolist(),'layernorm':ln_values.tolist(),'dropout_training_mean':float(probe.mean()),'dropout_eval_identity':eval_equal,'search_validation_mse':search.tolist(),'failure_traces':failure_traces,'label_diagnostic':{'epochs':80,'aligned_validation_mse':clean_score,'shuffled_validation_mse':shuffled_score},'torch_version':torch.__version__,'numpy_version':np.__version__}
    summary['continuation']=continuation_check(output,train)
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',train_x=train[0].numpy(),train_y=train[1].numpy(),validation_x=val[0].numpy(),validation_y=val[1].numpy(),search=search,**{f'history_{k}':v for k,v in histories.items()},**{f'path_{k}':v for k,v in paths.items()})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![实际神经网络的四个配置：拟合曲线、验证误差、批梯度范数的轮内平均、实际学习率。训练96、验证240、测试400个独立合成观测，噪声标准差0.2。所有模型从相同参数和批次顺序开始；AdamW另外使用衰减与调度，具体设置见正文。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f6414f720ecde96e6bda9daf.svg?v=f6414f720ecd)

图 3实际神经网络的四个配置：拟合曲线、验证误差、批梯度范数的轮内平均、实际学习率。训练96、验证240、测试400个独立合成观测，噪声标准差0.2。所有模型从相同参数和批次顺序开始；AdamW另外使用衰减与调度，具体设置见正文。

这次运行的测试均方误差依次为0.05125、0.04457、0.04346和0.04724。四条曲线都学到了主要的弯曲趋势，Adam在这里的测试误差最小；AdamW所用的正则化和调度并没有让它自动成为最优。图中噪声方差0.04是生成过程的一个参照：即使准确知道无噪声均值，对独立噪声观测仍会出现误差。有限测试集上的误差可以在这个参照附近波动，它也不等同于每次训练都能达到的固定下限。

下方梯度图记录每轮各批梯度范数的平均值，学习率图记录真正传给优化器的数值。把这两者和验证曲线联系起来，可以发现更新规则与误差变化的对应关系。若想单独研究 AdamW 的衰减作用，下一步应固定其余设置，只改变衰减；若想比较调度，保持优化器与峰值学习率相同。这组示例给出四个明确配置的实际行为，也展示了怎样把一个复杂比较拆成可解释的单因素实验。

![九个AdamW配置，每个训练60轮、按同一验证集记录最佳均方误差。热图值来自实际训练，训练种子与数据保持一致；测试数据未参与搜索。](https://ml-biomat.com/static/tutorials/machine-learning/figures/291821e30eef20fd70e4936a.svg?v=291821e30eef)

图 4九个AdamW配置，每个训练60轮、按同一验证集记录最佳均方误差。热图值来自实际训练，训练种子与数据保持一致；测试数据未参与搜索。

九格热图再用60轮预算比较 AdamW 的三个学习率与三个衰减系数。每格只用验证集选择最低误差，测试集不参与搜索。0.001的学习率在该预算内下降较慢，验证误差约0.195到0.200；0.003和0.01得到约0.054的结果。相邻格子差距很小时，可以对入围设置重复几个随机种子，而不是只追逐第四位小数。热图的价值是揭示参数区域的整体行为，让下一轮搜索有明确方向。

## 在同一条谷地里选择更新规则

目标为(x²+25y²)/2，始终从(3,1)出发。调节学习率与动量，再逐步观察轨迹。提高步长时，陡方向可能反复跨越谷底，甚至离开当前视窗；数值读出仍显示实际计算。Adam使用0.9和0.999的矩系数，只有动量法使用下方的动量系数。

[Figure: 带等高线的优化轨迹](https://ml-biomat.com/tutorials/machine-learning/m10/#M10-plot)

横纵轴是两个无量纲参数，灰色椭圆为同一损失水平，圆点为逐次计算的参数。参数绝对值超过10¹²时停止展开，保留此前数值以便观察发散。

## 把调参变成有次序的实验

超参数是训练前或训练过程中由外部规则指定的选择，例如网络宽度、学习率、批大小和衰减系数。网格搜索适合查看少数参数的规则组合；随机搜索在较多维度中能探索更多不同取值，尤其当只有少数参数强烈影响结果时。贝叶斯优化则用已有试验拟合“参数到验证表现”的代理模型，再根据预期收益与不确定性选择下一次试验。它把试验结果用于后续决策，适合单次训练成本较高的搜索。

例如，代理模型可能认为某一区域的误差较低、预测很确定，另一区域的平均预测稍差，却还存在获得更好结果的较大可能。采集规则把这两种信息组合，决定继续精修已知区域，还是花一次训练预算探索未知区域。完成新试验后，把真实的验证误差加入记录，再更新代理模型。代理模型的输入是超参数配置，输出是对验证表现及其不确定性的预测；最终用于回答任务的仍是实际训练得到的模型。这个区分有助于理解为什么搜索算法也有自己的模型和决策规则。

AutoML 把数据预处理、模型选择、搜索和资源分配组织成自动流程。自动化仍需要一项清楚的评价任务：样本如何划分，指标衡量什么，哪些特征在预测时可用，计算预算是多少。搜索越多，越容易挑中对固定验证集偶然有利的配置，因此最终需要保留未参与这些选择的测试数据。对于同一对象多条记录或时间相关数据，搜索内部也要沿用合适的分组或时间划分。

训练异常时，可以从最早出现异常的量往前查。先看输入和标签的数值、单位及对应关系，再让网络拟合一小批样本，验证损失函数和梯度是否连通；随后检查各层激活、梯度范数与实际学习率。若训练误差都降不下去，应先处理计算、优化或表示问题；若训练误差持续下降而验证误差上升，则研究数据量、正则化、划分和分布差异。每次只改变一项主要因素，保存曲线和配置，便能看清修复是否确实作用于原问题。

![两个单因素故障实验。左：同初始参数、同完整训练批次，只改变SGD学习率；高学习率达到预设损失阈值后停止。右：Adam相同80轮预算，分别使用正确对应和固定随机打乱的训练标签；验证标签保持正确。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0b73bdbf13e571a44d9d34c0.svg?v=0b73bdbf13e5)

图 5两个单因素故障实验。左：同初始参数、同完整训练批次，只改变SGD学习率；高学习率达到预设损失阈值后停止。右：Adam相同80轮预算，分别使用正确对应和固定随机打乱的训练标签；验证标签保持正确。

程序还保留了两个实际故障。把同一网络的完整批SGD学习率从0.03改到1.0，训练误差从约0.546迅速增大，六次更新后超过4×10¹²，程序在预设数值阈值处停止展开。另一项实验打乱训练标签与输入的对应关系，保持Adam的80轮预算不变：正确对应时最佳验证误差约0.04978，打乱后约0.46365。前者应从更新幅度查起，后者应先修复样本与标签关系；继续添加网络层无法替代这两项具体修复。

浮点精度也属于训练机制的一部分。指数、平方与连乘可能产生溢出或下溢，稳定的损失函数会把某些运算重新组织，避免先得到极端概率再取对数。混合精度通过较低精度计算节省资源，同时保留部分更高精度累积；梯度缩放则用于减少某些低精度格式的小梯度下溢。出现非有限值时，记录它最早发生在哪个运算，使用稳定实现、检查尺度，再决定是否需要提高精度。模型权重、优化器状态、调度进度、数据划分与随机状态一起保存，下一次实验就有了可复用的起点。

程序最后安排了一个可逐项检查的续训实验：带Dropout的小网络每轮随机排列全部96个样本，分为三个32样本批次，完成两轮后保存模型、AdamW状态、轮数、余弦调度配置、批次生成器状态与PyTorch随机状态。未中断分支继续第三轮；另一分支重新建立网络和优化器，再从文件恢复全部状态后执行同一轮。两边选中的批次完全相同，学习率均为0.00410942，损失差与更新后参数最大差均为0。Dropout用到的全局随机状态要在重新建立网络之后恢复，因为网络初始化本身也消耗随机数。这个小实验在轮边界保存；若要从一轮中间继续，还需要保存该轮排列和已经处理的位置。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M10.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning — Momentum](https://d2l.ai/chapter_optimization/momentum.html)

   累积梯度与二维曲率的解释。
2. [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)

   原始算法、偏差修正与方法史。
3. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)

   AdamW与损失惩罚的区别。
4. [PyTorch — AdamW](https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html)

   运行代码所用优化器定义。
5. [Batch Normalization](https://arxiv.org/abs/1502.03167)

   批统计归一化的原始研究。
6. [Layer Normalization](https://arxiv.org/abs/1607.06450)

   按样本特征计算统计量的设计。
7. [Random Search for Hyper-Parameter Optimization](https://www.jmlr.org/papers/v13/bergstra12a.html)

   搜索空间与预算比较。
8. [Practical Bayesian Optimization of Machine Learning Algorithms](https://arxiv.org/abs/1206.2944)

   代理模型和搜索决策的原始研究。
9. [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

   残差路径的原始研究。
