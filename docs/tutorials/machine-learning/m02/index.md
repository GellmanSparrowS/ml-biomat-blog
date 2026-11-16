# 让模型算得明白：线性代数、微积分与概率

Source: https://ml-biomat.com/tutorials/machine-learning/m02/
Language: zh-CN

形状与单位检查、空间变换、梯度步和概率代价，在四组小实验中连接起来。

## 数学是一套检查预测的方法

假设你要根据每天的气温、客流和营业时长预测用电量。数据表中有许多列，程序却需要把它们变成一个数；观察到预测偏高以后，又需要决定应调整哪一个参数、调整多少；即使平均预测不错，还需要表达不同日子的波动。这三个问题分别把我们带到线性代数、微积分和概率。它们并不是开课前必须通过的一道资格考试，而是随着问题出现逐步加入的工具。本章用同一条计算链说明这些工具怎样接起来：组织输入、得到预测、计算误差、调整参数，再检查数值是否可信。

读公式时可以先问三个问题：这个量描述什么，形状是什么，单位是什么。温度是摄氏度，一个月的温度记录是一列数；一百天、三个特征组成一张一百行三列的表。把整张表乘上三个权重，应该得到一百个预测，而不是一个无法解释的巨大矩阵。许多程序错误在运行之前就能被形状和单位检查发现。后面的每个实验都会给出具体尺寸与小算例，读者可以先用纸笔算出两三个数，再对照完整Python结果。

本章的图全部来自明确的几何构造或小规模计算：圆经过矩阵后如何改变，二维场保留少量成分后还剩什么，梯度更新为什么有时靠近最低点、有时越走越远，以及报告概率怎样影响预测代价。它们对应后续模型中的真实部件。线性模型使用矩阵乘法，主成分分析使用投影与分解，神经网络使用链式法则，概率分类使用对数损失。掌握这些连接，比提前记住一长串算法名称更能帮助你阅读代码。

## 从一列数到一次批量计算

只有大小的一个数叫标量；按顺序排列的一列数叫向量；按行列排列的数表叫矩阵。张量在编程中通常指更多维的数组，例如一批彩色图片可以按“图片数、高度、宽度、颜色通道”存成四维数组。每个轴都有含义，因此交换两个轴并不只是改变显示方式。把图片高度误当成批次数，程序可能仍能执行某种运算，却已经换了科学问题。写代码时先把各轴含义写清，再讨论如何广播、转置和压缩维度。

$$
\widehat{\mathbf y}=X\mathbf w+b\mathbf1_n,\qquad\widehat y_i=\sum_{j=1}^{p}X_{ij}w_j+b
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46833dd7644e5c60bb4525fe.svg) | n行p列输入矩阵；每行一个样本，每列一个特征，列单位可不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dbf1dc27226e2761db070ccb.svg) | 样本数、特征数、行索引与列索引，均为计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96db857c645773bf5928888e.svg) | p维权重及第j个权重；单位为输出单位除以第j列单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 标量偏置，与输出同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78cd82e74e7c5af5aa1274cd.svg) | n维全1向量，使偏置加到每个样本；无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/63a5ce02962df2a4e8d07d43.svg) | n维预测向量及第i个预测，单位与目标相同。 |

取X两行为(1,2)与(3,4)，w=(2,−1)、b=5，预测分别为2−2+5=5与6−4+5=7。矩阵尺寸(2,2)乘(2,)得到(2,)。

矩阵乘法中的求和是在特征轴上完成的。对于一个样本，三个特征各乘一个权重，再加在一起，得到一个预测；对一百个样本重复同一规则，就得到一百个预测。NumPy里的@表达这种矩阵乘法，星号则通常表示逐元素相乘。两者都可能不报错，因此不能用“程序跑完了”来判断是否做对。若X有100行3列，w有3个元素，X@w得到100个数；X*w得到100行3列，每个特征贡献仍然分开。先检查其中第一行，往往比盯着整张输出更有效。

单位也会随计算传播。若预测量是千瓦时，输入温度以摄氏度记录，那么温度权重的单位应是千瓦时每摄氏度；营业时长以小时记录时，其权重则是千瓦。不同列的单位可以不同，因为乘过各自权重以后都变成同一个输出单位。偏置也必须采用输出单位。标准化特征会改变权重的数值解释，却不会使模型凭空获得新的信息；它主要改变数值尺度与优化几何。保存训练均值和标准差，才能把未来数据放进同一个坐标系。

广播是批量计算的便利规则，也是初学者容易遇到的陷阱。长度为3的均值向量可以从100行3列的数据中逐行减去，因为最后一维对应三个特征。长度为100的预测若误写成100行1列，再减去长度为100的目标，有些数组规则会生成100乘100的差值表，而非100个残差。应当在关键步骤检查shape，并用一个含两行数据的小例子确认各维度对齐。这个习惯会直接延续到神经网络中的批次、时间步和通道维度。

## 矩阵改变空间，投影留下一个方向

把二维向量画成从原点出发的箭头，矩阵就可以理解为改变所有箭头的规则。有的矩阵旋转空间，有的沿一个方向拉长，有的把两个方向混合。与孤立地计算四个乘法相比，观察一个圆经过变换后成为怎样的椭圆，能同时看到所有方向受到的影响。图中的橙色标记跟随同一个点移动，使圆形本身的对称性不会掩盖旋转。所有坐标都采用无量纲教学尺度，重点是方向与相对长度。

![同一个单位圆依次经历SVD的方向变换、伸缩与方向变换；橙点跟踪同一输入点，最后一图与直接乘原矩阵一致。](https://ml-biomat.com/static/tutorials/machine-learning/figures/da342dfd16702f9d52730e51.svg?v=da342dfd1670)

图 1同一个单位圆依次经历SVD的方向变换、伸缩与方向变换；橙点跟踪同一输入点，最后一图与直接乘原矩阵一致。

内积计算两个向量在方向上的配合程度。若两个箭头正交，内积为零；若方向接近，正内积通常较大，但长度也会影响结果。投影则回答更具体的问题：沿着指定方向观察一个向量，能够看到多少？就像下午的影子把三维物体压到地面上，投影保留了某些方向的信息，舍弃了垂直方向的信息。这个比喻解释了为什么降维必然涉及取舍：被舍弃的部分可能是噪声，也可能含有某个预测任务需要的信号。

$$
\operatorname{proj}_{\mathbf u}(\mathbf x)=\frac{\mathbf u^\top\mathbf x}{\mathbf u^\top\mathbf u}\mathbf u,\qquad A\mathbf v=\lambda\mathbf v
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/99aba7f28d3cd80a9ab78b53.svg) | 同维向量；u为非零投影方向，采用相同的坐标尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9221822a6402f4d6cb9d08be.svg) | 转置；uᵀx是内积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/586e312e13336db7e2ba5c78.svg) | 沿指定方向的投影，单位与x相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 方阵线性变换；本章无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/67f20bb68a72f1c8979c3402.svg) | 非零特征向量及特征值；lambda是该方向的伸缩比例。 |

x=(3,2)、u=(1,0)时投影为(3,0)，丢弃垂直分量(0,2)。对于A=diag(2,1)，v=(1,0)满足Av=2v，因此lambda=2。

特征向量是变换中特别稳定的方向：经过方阵作用后，箭头仍沿原来的直线，只改变长度或正负方向；相应的比例叫特征值。并不是每个实矩阵都有完整的实特征向量组，矩阵也未必对称。数据分析中常见的协方差矩阵是对称半正定的，可以选择正交特征向量，并用非负特征值描述各方向的方差。这是主成分分析的几何基础：挑选变化最明显的方向，并明确记录舍弃了多少变化。

本章不把“方差大”直接等同于“对任务有用”。一个传感器很大的背景漂移可能贡献了主要方差，真正区分类别的小信号却藏在另一个方向。投影是否合适，要看重建、去噪、压缩还是预测中的哪一个目标。先对输入进行中心化，可以让方向表示围绕均值的变化；是否再除以各列标准差，则取决于原单位的大小是否应当影响比较。几何图帮助我们看见这项选择，而不是让降维成为一个默认按钮。

## 把复杂变化拆成一组可排序的成分

奇异值分解把一个矩阵写成三个变换依次作用：先改变输入方向，再沿正交方向伸缩，最后改变输出方向。它适用于长方形矩阵，因此比只讨论方阵的特征分解更适合数据表。图1中展示的就是这个过程，单位圆经历方向改变、非均匀伸缩和最后的方向改变，得到与直接乘原矩阵相同的椭圆。奇异值告诉我们每个独立方向被放大多少，并按从大到小排列。

$$
A=U\Sigma V^\top,\qquad A_r=\sum_{k=1}^{r}\sigma_k\mathbf u_k\mathbf v_k^\top
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | m×n实矩阵；元素单位由原数据定义。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b5ab03b659ab43ca500f4c01.svg) | 行数、列数、保留秩与成分索引；1≤r≤min(m,n)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/181c6fbfc16569597629ec4d.svg) | 约化形式分别为m×s和n×s正交列矩阵，其中s=min(m,n)，方向无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1fbad29a1619c9468255aa67.svg) | s×s对角矩阵及其非负降序对角值；奇异值继承A的数值单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/45b9cfc916d4ca94324ea100.svg) | U和V的第k列，以及保留r项的近似矩阵；近似单位与A相同。 |

若A=diag(3,1)，可取U=V=单位矩阵，奇异值为3和1。只保留第一项得到diag(3,0)，Frobenius误差为1，相对误差为1/√10≈0.3162。

如果只保留最大的几个奇异值及其对应方向，就得到低秩近似。把一张灰度图片看成矩阵，秩一成分可以理解为一列纵向变化与一行横向变化的外积；若干这种简单条纹叠加起来，便能描述更复杂的二维结构。这里的图像是由两个平滑峰和一组斜向波纹计算出来的标量场，不是照片。我们知道它的生成规则，因此可以把重建差异和原始结构逐项对照，避免把肉眼觉得平滑直接当成压缩成功。

![由两个高斯峰和斜向波纹构成的96×96无量纲标量场。各图共用色标；下方分别显示奇异值衰减和不同秩的相对Frobenius误差。](https://ml-biomat.com/static/tutorials/machine-learning/figures/dea478089d23dd30e55610ad.svg?v=dea478089d23)

图 2由两个高斯峰和斜向波纹构成的96×96无量纲标量场。各图共用色标；下方分别显示奇异值衰减和不同秩的相对Frobenius误差。

上排使用相同色标比较原场与不同秩的重建，下排显示奇异值衰减和相对误差。相对误差把所有像素差的平方相加、开平方，再除以原场的同类长度，因此它无量纲，也能跨不同幅值进行比较。保留更多成分会减少重建误差；当小奇异值已经接近浮点精度时，继续保留它们对可见结构几乎没有影响。对于固定秩，截断SVD在平方重建误差意义下具有最优性，但这个结论谈的是重建目标，并不自动决定分类准确率。

分解还可以揭示数值不稳定：如果某个方向的奇异值非常小，沿这个方向的输入变化几乎不会改变输出。反过来从输出求输入时，就需要除以一个很小的数，测量噪声也随之放大。这解释了为什么实际回归通常使用稳定的最小二乘求解器或正则化，而不是手工对矩阵求逆。条件数用最大与最小非零奇异值的比值描述一种放大风险；它是分析线性问题的工具，不是对所有模型通用的质量评分。

## 导数衡量一次小调整会带来什么

调节水龙头时，我们关心旋钮再转一点，流量会增加多少。导数表达的正是局部变化率：在某个位置附近，输入的小变化与输出变化之比。曲线很陡时，同样的旋钮调整会产生较大的输出变化；曲线平缓时，输出改变较小。若输入与输出有物理单位，导数的单位是输出单位除以输入单位。机器学习把旋钮换成模型参数，把输出换成误差，于是导数帮助我们决定下一次调整的方向。

$$
\frac{df}{dx}=\lim_{h\to0}\frac{f(x+h)-f(x)}h,\qquad\frac{dL}{dw}=\frac{dL}{d\widehat y}\frac{d\widehat y}{dw}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a580622b14a1c16add55735.svg) | 输入、输入扰动与输出函数；h与x同单位，导数单位为f单位/x单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af71e757095127e67ae46646.svg) | 考察扰动趋近零时差商的极限，要求相应导数存在。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0af214a4fb74136f9c2fe407.svg) | 损失、标量参数与中间预测；链式法则沿可微依赖关系相乘。 |

令x=3、y=5、预测为wx，损失为(wx−y)²。w=2时预测6，dL/d预测=2，d预测/dw=3，所以dL/dw=6。直接展开损失再求导也得到6。

一个模型往往有很多参数。偏导数每次只考察其中一个参数变化，其余参数暂时保持不动；把所有偏导按参数顺序排起来，便得到梯度向量。在通常的欧氏距离下，梯度指向函数局部增加最快的方向，负梯度指向局部下降最快的方向。这里的“最快”是针对同样大小的极小位移而言，不能直接推出走很大一步也会下降。如果地形弯曲明显，局部坡度只适合指导附近的一步。

预测通常由好几层计算组成，因此还需要链式法则。先用参数得到预测，再用预测得到损失，参数对损失的影响就是沿这条计算链逐段传递变化率。例子中，预测为参数乘输入，损失为预测与观测之差的平方；一个因子来自平方函数的斜率，另一个因子来自预测对参数的斜率。神经网络的反向传播把这个规则系统地应用于许多层，并在分支处把不同路径的贡献相加。自动微分节省了手算，却仍需要正确的计算图和目标函数。

有限差分提供了一个独立检查：稍微增大与减小参数，重新计算损失，用两个结果的差除以两次扰动之间的距离，近似得到导数。本章在二维二次函数上同时计算解析梯度与中心差分，二者应当接近。扰动并非越小越好；过小会使两个浮点数相减时有效数字大量丢失，过大又不再代表局部斜率。用几种扰动尺度检查一致性，比只选择一个极小数更有说服力。

## 沿坡下降：为什么步长决定成败

有了梯度，就可以反复向负梯度方向移动。学习率决定每一步走多远。本章使用一个在两个方向弯曲程度不同的碗形目标：第二个方向比第一个方向陡八倍。小步长比较稳，却需要更多次更新；适中的步长可能在陡方向来回摆动，但幅度逐渐缩小；过大的步长则让每一次越过谷底的距离都更大，最终发散。图中同一组初始参数和三种步长，使这些现象可以在轨迹与损失曲线上同时核对。

$$
L(\mathbf w)=\tfrac12(w_1^2+kw_2^2),\quad\nabla L=(w_1,kw_2)^\top,\quad\mathbf w_{t+1}=\mathbf w_t-\eta\nabla L(\mathbf w_t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cb4681a1a45ee2509bf3d35c.svg) | 二维参数及其两个分量，本教学例子无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7677415a903353266414162c.svg) | 二次目标及正曲率参数；k>0时目标严格凸，本例k=8。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c12ab9487a4458e174c3e1d.svg) | 由两个偏导组成的梯度，与参数同形状。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a75429b238a0ac5516db3841.svg) | 更新次数与正学习率；本例均无量纲。 |

起点(2,2)、k=8时梯度(2,16)，eta=0.1给出新点(1.8,0.4)，新损失0.5(3.24+1.28)=2.26。此二次函数的稳定步长范围为0<eta<2/max(1,k)，k=8时上限0.25。

![相同起点(2,2)、目标0.5(w₁²+8w₂²)，比较25次梯度更新。左图固定视野，发散轨迹离开视野；右图对数纵轴显示全部损失。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f0eecd338adc27ff014dce18.svg?v=f0eecd338adc)

图 3相同起点(2,2)、目标0.5(w₁²+8w₂²)，比较25次梯度更新。左图固定视野，发散轨迹离开视野；右图对数纵轴显示全部损失。

凸函数提供一种重要的几何保证：任意两点之间的函数图像不会高于连接两点函数值的直线；对可微凸函数，找到梯度为零的点就找到了全局最小值。二次碗是典型例子。非凸目标可能有多个谷地、鞍点和平坦区，因此局部梯度信息不能独自判断全局最优位置。这个区别帮助我们理解算法能保证什么，而无需把所有现实模型都想象成崎岖山脉。即使在凸问题中，糟糕的尺度和步长仍会使数值迭代很慢。

某些参数还有可行范围，例如概率不能为负，几个混合比例必须加起来等于一。约束优化会在降低目标的同时保持这些条件。投影梯度先走普通梯度步，再把结果放回可行集合；若约束只是一维非负，负数可直接截到零，而复杂集合需要相应的投影算法。正则化则把偏好写进目标，例如惩罚过大的权重。这两种做法相关，但并不意味着可以随意把每个参数截断后声称得到同一个优化问题。

## 一步一步走向谷底

起点(2,2)，所有量无量纲。轨迹与损失来自同一次计算；改变参数会重置起点。

[Figure: 一步一步走向谷底](https://ml-biomat.com/tutorials/machine-learning/m02/#M02-plot)

互动中可以改变学习率和第二方向的曲率，再单步观察更新。初始点固定为(2,2)，当曲率为8、学习率为0.1时，一步之后应到达(1.8,0.4)，目标从18降到2.26。这个小例子同时检查了梯度、步长、坐标顺序和损失定义。把学习率提高到0.3再重复，会看到陡方向的误差放大。变化来自实际递推式，而非预设动画；任何时候都可以复位到同一个起点继续比较。

## 一次结果与一组可能结果

明天是否下雨只有一个实际结果，但今天的预测可以表达许多可能天气中下雨所占的概率。概率介于零与一之间，完整互斥结果的概率加起来为一。随机变量则把每种结果对应到一个数，例如下雨记为1、不下雨记为0。期望按概率加权求平均，因此可以是某次观测永远不会取到的数；一枚硬币的平均正面次数可以是0.7，单次抛掷却仍只有0和1。方差进一步描述结果围绕期望的分散程度。

$$
\mathbb E[X]=\sum_i p_i x_i=\mu,\quad\operatorname{Var}(X)=\sum_i p_i(x_i-\mu)^2,\quad P(A\mid B)=\frac{P(A\cap B)}{P(B)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0021244cb2867b2bc1498b5a.svg) | 离散随机变量、可能取值与取值索引；x_i使用所测量量的单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29d8041678f9875c2bfdd4ae.svg) | 第i种结果的概率与期望；概率非负且总和为1，期望与X同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | 方差，单位为X单位的平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/69e39a892cb662e81faeb8af.svg) | 两个事件、概率、同时发生与条件；要求P(B)>0，概率无量纲。 |

X取0、1、2，概率0.2、0.5、0.3，则均值1.1，方差0.2×1.21+0.5×0.01+0.3×0.81=0.49。若雨天概率0.5，雨天且拥堵概率0.3，给定雨天的拥堵概率为0.6。

条件概率表示已知额外信息后，应该在哪一个群体中计算比例。若在100个晴天中有20天交通拥堵，而在100个雨天中有60天拥堵，那么已知下雨时应使用雨天组的比例，而不是把两组混合的总体比例。条件改变了比较集合，不一定表示因果干预。雨天与拥堵有关，可能同时涉及出行方式、能见度和道路管理。独立性则表示知道一个事件不会改变另一个事件的概率，它比“相关系数为零”更强；非线性关系可能在零相关下仍然存在。

似然把概率模型反过来用于比较参数。观察十次抛掷，其中七次正面以后，结果已经固定，我们考察哪个候选正面概率让这批结果更容易出现。若假设各次独立且共享同一个概率，整段观测的概率可由每次的概率相乘得到。最大似然会选择0.7。这里0.7是参数估计，不是“参数为0.7的概率”；若想给参数本身安排概率分布，需要再引入先验与贝叶斯更新。

![左：十次独立试验、七次成功的相对对数似然；中：二元熵；右：真实成功概率0.7时报告不同概率的交叉熵。自然对数给出nat单位。](https://ml-biomat.com/static/tutorials/machine-learning/figures/36067de63748c272189ae184.svg?v=36067de63748)

图 4左：十次独立试验、七次成功的相对对数似然；中：二元熵；右：真实成功概率0.7时报告不同概率的交叉熵。自然对数给出nat单位。

对数把独立观测概率的乘积变成求和，既简化求导，也避免很多小概率连乘后变成计算机里的零。图中第一幅画的是相对对数似然，最高点被平移到零，这样不改变哪个参数最优，却更容易比较曲线形状。独立同分布是假设的一部分，时间序列或同一受试者的重复记录可能不满足它。建立概率模型前，应检查样本之间怎样关联，而不是因为数组有很多行就把每一行都当成新的独立证据。

## 从通信中的信息，到预测中的对数代价

1948年，Claude Shannon研究通信时，把一个问题放在中心：消息有多种可能，接收者平均需要得到多少信息，才能知道实际发生了哪一种？如果结果几乎总是相同，消息不太令人意外；如果几个结果同样可能，就需要更多信息区分。这个问题导出熵。图4中第二幅展示二元概率的熵：在概率0或1附近，不确定性小；两种结果各占一半时，不确定性最大。这里讨论的是统计不确定性，与消息内容是否有趣并不是同一个概念。

$$
H(p)=-\sum_i p_i\ln p_i,\quad H(p,q)=-\sum_i p_i\ln q_i,\quad D_{\rm KL}(p\|q)=H(p,q)-H(p)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/89e5019371c0d604f379329e.svg) | 定义在相同离散结果上的真实与报告概率，非负且各自归一；p_i>0处要求q_i>0以得到有限值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 结果索引，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d3dd181217f9d250008c256f.svg) | 熵、交叉熵和KL散度，采用自然对数时单位nat；0ln0约定为0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | 自然对数；输入概率无量纲。 |

p=(0.5,0.5)时熵为ln2≈0.6931nat。报告q=(0.9,0.1)，交叉熵≈1.2040nat，额外代价KL≈0.5108nat。若q=p，额外代价为0。

交叉熵把真实分布提供的结果，用另一套报告概率来计价。如果真实正面比例为0.7，却一直报告0.99，那么少量反面出现时会受到很高的对数惩罚。图中的交叉熵在报告概率与真实比例一致时最低；高出真实熵的部分就是KL散度。它衡量采用另一套概率所付出的额外对数代价，方向有意义：交换两套分布一般不会得到相同数值，因此不能把它当成普通欧氏距离。若真实可能出现的结果被模型赋予零概率，这个额外代价会发散。

自然对数对应nat，以2为底的对数对应bit。改变底数会按固定比例缩放熵和交叉熵，不改变最优报告概率。实际分类训练中，真实标签常写成只有一个位置为1的向量，交叉熵便只留下真实类别概率的负对数。这解释了为什么模型把正确类别概率从0.1提高到0.9会显著降低损失，也解释了为什么一个自信的错误比一个犹豫的错误受到更重惩罚。类别准确率只看最大概率的位置，交叉熵还关心整套概率是否合理。

$$
\log\sum_{j=1}^{K}e^{z_j}=a+\log\sum_{j=1}^{K}e^{z_j-a},\quad a=\max_jz_j,\quad q_i=e^{z_i-\operatorname{logsumexp}(\mathbf z)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5bf4e2ea8de2808c57b6a731.svg) | 类别数与类别索引，计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6f1f5acc2895e75bc4d32d09.svg) | 原始分数、K维分数向量和最大分数；均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | 第i类归一化概率，非负且全部之和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6bdb4529d9344276682d4249.svg) | 稳定计算指数和的自然对数，输出为无量纲对数尺度。 |

分数(1000,1001,999)减最大值后为(−1,0,−2)，指数约(0.3679,1,0.1353)，除以总和1.5032，得到(0.2447,0.6652,0.0900)。

最后还要把数学等式变成稳定的计算。若几个分数是1000、1001和999，直接先求指数会溢出；把它们同时减去最大值，指数只需要作用于−1、0、−2，再归一化，就能得到相同概率。代码使用logsumexp完成相应的对数归一化，结果约为0.2447、0.6652、0.0900，总和为一。这个处理没有改变模型，也没有近似掉一个类别，它利用等式消去了共同的巨大尺度。数值稳定性往往来自重新组织正确的公式，而非换用更大的数据类型。

### 完整实验：分解、差分、优化与概率

依赖NumPy、SciPy、Matplotlib。运行python main.py --output results --language zh，生成四幅图、全部输入场与summary.json；所有数据均由代码中的明确规则生成。

```
"""Small, reproducible experiments in geometry, approximation and optimization."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import logsumexp, xlogy

def main(output, language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
    def t(a,b):return a if zh else b
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    # A complete two-dimensional SVD: rotation/reflection, stretch, rotation.
    A=np.array([[2.,1.],[0.,1.]])
    U,s,Vt=np.linalg.svd(A);theta=np.linspace(0,2*np.pi,401);circle=np.array([np.cos(theta),np.sin(theta)])
    fig,axes=plt.subplots(1,4,figsize=(12,3.2),layout='constrained')
    arrays=[circle,Vt@circle,np.diag(s)@Vt@circle,A@circle]
    titles=[t('单位圆','Unit circle'),'Vᵀ x','Σ Vᵀ x','U Σ Vᵀ x = A x']
    for ax,points,title in zip(axes,arrays,titles):
        ax.plot(*points,color='#167d87',lw=2);ax.scatter(*points[:,0],color='#d48745',s=30,zorder=3)
        ax.axhline(0,color='#b8c7ce',lw=.7);ax.axvline(0,color='#b8c7ce',lw=.7)
        ax.set(xlim=(-2.8,2.8),ylim=(-2.8,2.8),aspect='equal',title=title,xlabel='x₁',ylabel='x₂')
    save(fig,'geometry')
    # Original analytic image, with structure known exactly; no downloaded image.
    x=np.linspace(-1,1,96);xx,yy=np.meshgrid(x,x)
    img=np.exp(-((xx+.35)**2+(yy-.2)**2)/.11)+.6*np.exp(-((xx-.35)**2+(yy+.3)**2)/.09)+.22*np.cos(11*(xx+yy))*np.exp(-xx**2-yy**2)
    u,sv,vt=np.linalg.svd(img,full_matrices=False);ranks=[1,2,4,12];errs=[]
    fig=plt.figure(figsize=(13,6.0),layout='constrained');gs=fig.add_gridspec(2,5,height_ratios=[1,1.1]);field_axes=[]
    for j,(rank,title) in enumerate([(96,t('原始场','Original field'))]+[(r,f'r={r}') for r in ranks]):
        approx=img if rank==96 else (u[:,:rank]*sv[:rank])@vt[:rank]
        ax=fig.add_subplot(gs[0,j]);field_axes.append(ax);field_image=ax.imshow(approx,cmap='magma',vmin=img.min(),vmax=img.max(),origin='lower',extent=[-1,1,-1,1]);ax.set(title=title);ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1])
        if rank!=96:errs.append(float(np.linalg.norm(img-approx)/np.linalg.norm(img)))
    fig.colorbar(field_image,ax=field_axes,location='right',shrink=.85,pad=.025,label=t('场幅值（无量纲）','Field amplitude (dimensionless)'))
    ax=fig.add_subplot(gs[1,:3]);ax.semilogy(np.arange(1,21),sv[:20],'o-',color='#167d87');ax.set(xlabel=t('奇异值序号','Singular-value index'),ylabel=t('奇异值（场幅值单位）','Singular value (field units)'));ax.grid(alpha=.2)
    ax=fig.add_subplot(gs[1,3:]);ax.bar([str(r) for r in ranks],errs,color='#d48745');ax.set(xlabel=t('保留秩 r','Retained rank r'),ylabel=t('相对重建误差','Relative reconstruction error'));save(fig,'svd')
    H=np.diag([1.,8.]);start=np.array([2.,2.]);trajectories={}
    fig,(ax,lossax)=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');g=np.linspace(-2.4,2.4,200);gx,gy=np.meshgrid(g,g);ax.contour(gx,gy,.5*(gx**2+8*gy**2),levels=[.1,.5,1,2,4,8,16],colors='#cad8de')
    for eta,col in [(.05,'#167d87'),(.22,'#d48745'),(.3,'#8b557c')]:
        w=start.copy();path=[w.copy()]
        for _ in range(25):w=w-eta*(H@w);path.append(w.copy())
        path=np.array(path);loss=.5*np.sum(path*(path@H),axis=1);trajectories[str(eta)]={'path':path.tolist(),'loss':loss.tolist()}
        ax.plot(*path.T,'o-',ms=2,color=col,label=f'η={eta}');lossax.semilogy(loss,color=col,label=f'η={eta}')
    ax.set(xlim=(-2.4,2.4),ylim=(-2.4,2.4),xlabel='w₁',ylabel='w₂',title=t('同一碗形目标，三种步长','One quadratic objective, three step sizes'));ax.legend()
    lossax.set(xlabel=t('更新次数','Update'),ylabel=t('目标函数（无量纲）','Objective (dimensionless)'));lossax.grid(alpha=.2);lossax.legend();save(fig,'gradients')
    q=np.linspace(.001,.999,500);p=.7;entropy=-(xlogy(q,q)+xlogy(1-q,1-q));ce=-(p*np.log(q)+(1-p)*np.log1p(-q));loglike=7*np.log(q)+3*np.log1p(-q)
    fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
    axes[0].plot(q,loglike-loglike.max(),color='#167d87');axes[0].axvline(.7,color='#d48745',ls='--');axes[0].set(xlabel=t('候选正面概率 q','Candidate success probability q'),ylabel=t('相对对数似然','Relative log likelihood'),title=t('10次中7次正面','Seven successes in ten trials'))
    axes[1].plot(q,entropy,color='#167d87');axes[1].set(xlabel='q',ylabel=t('熵（nat）','Entropy (nats)'),title=t('不确定性在中间最大','Uncertainty peaks in the middle'))
    axes[2].plot(q,ce,label=t('交叉熵','Cross entropy'),color='#167d87');hp=-(p*np.log(p)+(1-p)*np.log1p(-p));axes[2].axhline(hp,color='#d48745',label='H(p)');axes[2].set(xlabel=t('报告概率 q','Reported probability q'),ylabel='nat',title=t('真实比例 p=0.7','True proportion p=0.7'));axes[2].legend();save(fig,'probability')
    f=lambda v:.5*v@H@v;eps=1e-6;fd=np.array([(f(start+eps*np.eye(2)[i])-f(start-eps*np.eye(2)[i]))/(2*eps) for i in range(2)])
    logits=np.array([1000.,1001.,999.]);probs=np.exp(logits-logsumexp(logits))
    summary={'matrix_reconstruction_error':float(np.linalg.norm(A-U@np.diag(s)@Vt)),'singular_values':s.tolist(),'image_rank_errors':dict(zip(map(str,ranks),errs)),'analytic_gradient':(H@start).tolist(),'finite_difference_gradient':fd.tolist(),'gradient_max_error':float(np.max(np.abs(fd-H@start))),'one_step_eta_0_1':(start-.1*H@start).tolist(),'one_step_loss':f(start-.1*H@start),'stable_probabilities':probs.tolist(),'stable_probability_sum':float(probs.sum()),'entropy_p_0_7_nats':hp,'trajectories':trajectories}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(output/'experiment_data.npz',A=A,image=img,singular_values=sv,q=q,cross_entropy=ce)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

运行完整例子后，可以选择一个量反向追踪：例如一幅图上的点如何从矩阵乘法得到，一步损失如何由坐标计算，一组概率如何经过稳定归一化。再把其中一个输入改成手算方便的数，核对输出是否按预期改变。后续章节会把这些部件组合成更大的模型，但检查方式仍然相同：先确认对象、形状和单位，再核对一条可计算的关系，最后观察整个实验是否回答最初提出的问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning — Linear Algebra](https://d2l.ai/chapter_preliminaries/linear-algebra.html)

   矩阵、形状与范数。

   CC BY-SA 4.0
2. [Dive into Deep Learning — Calculus](https://d2l.ai/chapter_preliminaries/calculus.html)

   偏导、梯度与链式法则。

   CC BY-SA 4.0
3. [NumPy — Singular Value Decomposition](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)

   约化分解尺寸与重建。

   NumPy documentation
4. [SciPy — logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html)

   稳定对数归一化。

   SciPy documentation
5. [Shannon (1948), A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

   熵的通信问题背景与原始论证。
