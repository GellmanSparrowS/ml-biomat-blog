# 提升树：每一步修正怎样成为强模型

Source: https://ml-biomat.com/tutorials/machine-learning/m31/
Language: zh-CN

从八个样本的权重变化，走到 XGBoost、LightGBM、CatBoost 的真实训练、排序与解释。

## 后一棵树，接着修正前面留下的问题

修改一篇文章时，第一遍整理结构，第二遍补充解释，第三遍处理还不顺的段落。每一轮都建立在已有结果上，而不是让几位作者各自写一篇再取平均。Boosting采用类似的逐步修正思想：先得到一个简单预测，再训练新的小模型，专门处理当前预测还没有解决的部分。最终结果是许多模型贡献的累加。与上一章的森林相比，它强调前后轮次的依赖，因此需要同时管理每一步的力度和总共走多少步。

本章沿着问题的发展进入方法。AdaBoost改变样本在下一轮中的权重，让当前困难的样本获得更多注意；梯度提升把“还需修正什么”写成损失对预测的负梯度，使同一框架能够处理回归、分类与排序；XGBoost、LightGBM和CatBoost则进一步处理正则化、计算资源和类别特征。理解这些联系后，几个软件名称就不再是互相替换的黑箱，而是不同统计假设与工程选择的组合。

五种实现都在1800条明确生成的分类记录上运行，训练1080条、验证360条、测试360条。输入有十个数值特征和一个四分类特征，后者由第一个数值特征的区间生成，因此提供另一种编码而没有额外的独立信息。另有一维回归实验显示新增树怎样修正残差，查询分组排序实验显示目标函数怎样改变。图中的时间与内存来自实际独立进程运行，数据、参数与所有输出都可由完整脚本重新产生。

## 难分的样本，怎样在下一轮变得更重要

AdaBoost从均匀样本权重开始，训练一个较简单的分类器，再计算它在当前权重下错了多少。错误率越低，这个分类器在最终组合中获得的权重越大；被它分错的样本则提高相对权重，促使下一轮关注这些位置。Freund与Schapire在1990年代的研究把乘法权重更新与提升联系起来，1997年的论文系统讨论了这一做法。它的关键不在于预先知道每个弱学习器有多好，而在于根据当前观察到的错误进行调整。

$$
\epsilon_m=\sum_{i=1}^nD_m(i)\mathbf1[h_m(x_i)\ne y_i],\quad \alpha_m=\frac{\eta}{2}\ln\frac{1-\epsilon_m}{\epsilon_m},\quad D_{m+1}(i)=\frac{D_m(i)e^{-\alpha_m y_i h_m(x_i)}}{Z_m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/37e7ea7e1e209c402bf2fd4c.svg) | 样本数、样本索引与提升轮次，均为计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/93bb4b0cd18cb095f786f05f.svg) | 输入特征向量、真实标签与本轮弱分类器输出；本式标签和输出均为−1或+1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/646aa1b9dab853028ed79067.svg) | 归一化样本权重与加权错误率，无量纲；权重和为1，本式要求错误率在0与1之间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c403c2cd2df430316dafa77f.svg) | 正的学习率与本轮投票系数，均无量纲；这是对称二分类记号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a5e38d0246c5845c201ae32e.svg) | 归一化分母、条件成立取1否则取0的指示函数、自然对数；Z为所有未归一化新权重之和。 |

八条等权记录错两条，错误率1/4。学习率1时，alpha=ln(3)/2≈0.5493。正确记录乘1/√3，错误记录乘√3；归一化后六条正确记录各1/12，两条错误记录各1/4，总和仍1。

假设八个样本最初各占1/8，一个弱分类器分错两个，加权错误率为1/4。按二分类的对称系数约定，它的投票系数约为0.5493；重新归一化后，每个错分点的权重变成1/4，六个正确点各为1/12。错分组与正确组的总权重各为一半。下一轮并没有获得新的原始数据，而是换了一种看待同一批数据的分布。样本权重像课堂练习中的时间分配，让遗漏的部分有机会被补上。

这种关注也会追逐错误标签和极端噪声。如果某个样本本身标错，反复提高它的权重可能让后续模型付出越来越大代价。需要检查高权重样本究竟代表稀少但重要的情形，还是标注与测量问题。学习率可以缩小每轮贡献，基础树深度也影响一轮能表达多少结构。代码使用scikit-learn的SAMME实现与单层树桩；下面的手算采用对称的二分类表达，两者的系数尺度约定不同，权重更新的相对作用可以对应起来。

## 一轮提升怎样重新分配注意力

八条记录初始权重均为1/8。改变树桩阈值、方向和学习率，观察错分记录的权重与总权重。橙色标出错分，蓝色标出正确。

[Figure: 真实标签、树桩预测与归一化权重](https://ml-biomat.com/tutorials/machine-learning/m31/#M31-plot)

互动固定八个标签，让你选择树桩的阈值、方向和更新力度。上方显示这一轮的错误，下方显示更新前后的样本权重。错误率为一半时，投票系数为零，这个分类器没有提供优于随机方向的判断；错误率超过一半时，负系数相当于反向采用该规则，实际训练程序可以选择翻转或拒绝它。观察权重总和始终为一，能够检查归一化是否正确，而不必把指数更新当作难以解释的技巧。

## 从追着错误跑，到沿损失的下降方向修正

回归问题没有“分错或分对”这样简单的标签，因此需要更一般的修正目标。对于平方损失，当前观测减预测的残差正好指向应该补上的量：预测少了2，就希望下一步加一点正值；预测多了1，就希望加一点负值。训练一棵回归树拟合这些残差，再把它的部分预测加回原模型，就得到最直观的梯度提升。初始预测通常选使损失最小的常数，平方损失下就是训练目标均值。

$$
r_{im}=-\left.\frac{\partial\ell(y_i,F)}{\partial F}\right|_{F=F_{m-1}(x_i)},\qquad F_m(x)=F_{m-1}(x)+\eta h_m(x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93519422cf83110abebee704.svg) | 观测索引、轮次、任意输入、观测输入与目标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4a689e31890fc97c95f6af0b.svg) | 前后两轮的原始预测函数与拟合负梯度的小树；分类时F是分数，不是概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8338dc4c5daca5f09e7fb996.svg) | 单条损失、负梯度伪残差和正学习率；本章数值例全部无量纲。 |

平方损失取(y−F)²/2，对F求导为F−y，负梯度就是y−F。目标(2,5)、原预测(3,3)得到残差(−1,2)；小树若恰好拟合它们，学习率0.1使新预测为(2.9,3.2)。逻辑损失的负梯度为y−p，但更新仍加在原始分数上。

![同一百个合成观测上的平方损失提升：初始均值、第一棵残差树、缩小后的贡献，以及一轮、十轮、六十轮的预测。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2bf5158be5727ee8f2b5e120.svg?v=2bf5158be572)

图 1同一百个合成观测上的平方损失提升：初始均值、第一棵残差树、缩小后的贡献，以及一轮、十轮、六十轮的预测。

图中的真实关系由正弦与线性项组成，再加入标准差0.18的高斯噪声。第一幅显示初始均值，第二幅显示残差和拟合它的小树，第三幅只显示要加入的15%贡献。下排比较累加1、10和60棵深度2树后的曲线。每棵树本身是分段常数，很多小贡献相加后可以逼近平滑关系。残差总和在初始均值处约为零，这个简单恒等式也成为完整脚本的数值检查。

对其他可微损失，需要拟合负梯度，而不一定是原始响应残差。二分类对数损失作用于原始分数时，负梯度是标签减当前概率，但累加的新树作用在原始分数上，随后才通过sigmoid得到概率。若把这个修正直接加到概率上，就换了优化问题。Friedman在2001年的梯度提升工作把提升解释为函数空间里的逐步优化，使损失选择、基础学习器和每步搜索可以在一个框架中讨论。

学习率小，会让每一步更谨慎，通常需要更多轮；树深控制一轮能够表达的交互结构；行采样和列采样则为学习加入随机性。它们需要联合考虑，不能把树数当成独立的“精度旋钮”。早停使用验证损失选择有用的轮次，即使训练损失仍在下降，也可以停止继续追逐训练细节。验证集承担了选择工作，最终测试因此保留到模型和停止位置确定之后。

![五个固定配置的训练与验证对数损失。AdaBoost固定使用400轮，验证曲线仅用于观察；GBDT、XGBoost、LightGBM和CatBoost按验证损失选择轮数。测试记录用于最后评价。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f4152ecc381969571176c33b.svg?v=f4152ecc3819)

图 2五个固定配置的训练与验证对数损失。AdaBoost固定使用400轮，验证曲线仅用于观察；GBDT、XGBoost、LightGBM和CatBoost按验证损失选择轮数。测试记录用于最后评价。

AdaBoost曲线在约40轮后出现了一个值得仔细读的现象：训练与验证的对数损失一起升高。图中统计的是软件输出概率的对数损失，AdaBoost的加权分类更新与指数损失解释则针对另一种量。本章使用的scikit-learn实现先把各棵树的加权投票除以总权重，再把归一化分数转换为概率；新增树既改变投票，也改变这个分母。分类边界与概率的信心因此可以朝不同方向变化。这里保留400轮的实际输出，读者可以同时检查分类准确率和概率损失，看到同一模型回答“分到哪类”与“概率报得多准”时表现的差别。

## XGBoost：把一轮修正写成可快速比较的目标

XGBoost对每个观测计算当前损失的一阶和二阶导数。一阶项指出修正方向，二阶项描述局部弯曲程度；再加上叶数和叶权重的正则项，就能为候选树结构计算近似目标。把落在同一个叶里的梯度和曲率分别相加，叶的最佳分数可以写成一个简单分式。于是比较一次分裂时，不必对所有可能叶值重新做完整优化，而能用左右子节点的统计量快速计算收益。

$$
G_j=\sum_{i\in I_j}g_i,\quad H_j=\sum_{i\in I_j}h_i,\quad \widetilde L=\sum_{j=1}^J\left[G_jw_j+\frac12(H_j+\lambda)w_j^2\right]+\gamma J,\quad w_j^*=-\frac{G_j}{H_j+\lambda}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7e0420234890d636d2d9da42.svg) | 叶索引、叶数、落入该叶的观测集合及观测索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c1606c14eceb60340c079e42.svg) | 损失对当前原始分数的一阶和二阶导数，以及叶内各自的总和；此处h_i为二阶导数，与上一式的小树h_m不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e33da962e40c68b8cfe7df9d.svg) | 叶的新分数、非负L2惩罚、非负每叶惩罚和二阶近似目标；无量纲分类损失，要求H_j+lambda>0。 |

这是把本轮损失在旧预测附近展开到二阶，丢掉与新树无关的常数。固定树结构后，对每个叶的w求导并令零，得到最优叶值。G=−3、H=2、lambda=1时w=1，叶二次项为−1.5；若gamma=0.2，一个叶对应的目标增量为−1.3。

这不是把所有模型都简化成同一个二次函数，而是在当前预测附近为下一轮建立局部近似。对于平方损失，二阶结构本来就是精确的；对于其他损失，步长和正则化帮助控制局部近似的使用范围。叶权重惩罚抑制过大的修正，最小子节点权重限制证据过少的分裂，分裂收益阈值要求新分支带来足够改善。每个参数都作用于某一个具体环节，调参时应先理解它改变的对象。

稀疏特征与缺失值也进入树的构造。某个分裂遇到缺失时，模型可以学习把它送向哪一侧；这条默认路径根据训练目标选择。未出现的稀疏条目如何解释，取决于输入矩阵与missing参数，数值零和缺失不能随意互换。本例为了让类别编码的差异更清楚，将类别在训练侧独热编码，并保留完整数值矩阵；当前XGBoost也支持其他类别处理路径，选择哪一种应写进实验，而不是把独热编码说成它唯一的能力。

代码采用hist建树方式，它把连续值归入有限桶，在桶内累积统计量。直方图并不是LightGBM独有的现代实现特征，因此比较软件时要看实际设置。本次XGBoost以最多400轮、深度3、学习率0.05运行，并根据验证损失选择159轮，测试准确率约91.11%、对数损失约0.241。数值说明的是这组配置，下一步可以在相同开发预算下比较深度、正则与采样，而不是从单次结果推出软件的普遍高下。

缺失值的默认方向也能用一个小例子理解。假设“最近一次购买金额”缺失可能意味着没有购买记录，也可能意味着系统没有采集该字段；把两者统一填成零，便把“真实花了零元”混在其中。支持缺失值分支的树在训练时比较把缺失记录送向左侧或右侧的损失，保存较好的方向供预测使用。这个方向依赖训练数据中的缺失机制。上线后若采集流程改变，大量记录突然缺失，模型虽然仍能给出数值，输入所表达的事件已经变化，因而需要按缺失模式检查表现。

## LightGBM：把分裂统计压进直方图，再选择最值得长的叶

连续特征可能有成千上万个不同值，逐个扫描候选阈值会带来较大开销。直方图方法先把值分到较少的桶，累加每个桶的梯度、曲率和计数，再通过累计和比较切分。一个父节点拆成两个子节点以后，已知父直方图和一个子节点直方图，另一个可以相减得到。桶数越少，统计与存储通常越省，但阈值分辨率也越粗；这是一项可测量的精度与资源取舍。

![逐层生长先展开同一层的节点，树形相对均衡。Microsoft / LightGBM 官方原图，MIT 许可，未改动。](https://ml-biomat.com/static/tutorials/machine-learning/figures/dcf2230660f312997cedae6d.png?v=dcf2230660f3)

图 3逐层生长先展开同一层的节点，树形相对均衡。Microsoft / LightGBM 官方原图，MIT 许可，未改动。

![按叶生长选择当前改善最大的叶，不要求各分支同深；深度与叶数约束因此各有作用。Microsoft / LightGBM 官方原图，MIT 许可，未改动。](https://ml-biomat.com/static/tutorials/machine-learning/figures/4bf21a9a4d94fadbc76331d0.png?v=4bf21a9a4d94)

图 4按叶生长选择当前改善最大的叶，不要求各分支同深；深度与叶数约束因此各有作用。Microsoft / LightGBM 官方原图，MIT 许可，未改动。

官方原图把两种生长次序放在一起。按层生长依次扩展某一深度的节点；按叶生长每次寻找预期损失下降最大的叶，可能连续深入某一条分支。固定叶数时，后者能把计算集中到更需要细分的区域，也可能在小样本上形成很深的局部规则。LightGBM因此同时提供num_leaves、max_depth和叶内最小数据量等约束。本例把叶数限制为8、深度限制为3，让结构规模保持明确，并不把两种生长策略画成一种永远优于另一种的关系。

LightGBM的研究还包括梯度相关的采样和互斥特征打包。GOSS优先保留大梯度样本，再从小梯度样本中抽取一部分并调整权重，让需要较大修正的记录获得更多计算；EFB尝试把很少同时非零的稀疏特征组合起来，减少有效列数。它们分别处理行与列的计算成本，不等同于普通均匀子采样。软件版本、boosting设置和数据特点会决定具体启用的路径；本例采用普通GBDT配置，图中的运行结果没有额外声称开启GOSS。

对于类别特征，LightGBM可以依据训练目标相关的统计量组织类别，再寻找类别集合之间的切分，避免把类别号码当作天然连续大小。本例将四个类别声明为pandas类别列，训练和验证使用相同类别词表，词表由训练侧确定。验证选择135轮，测试准确率约91.11%、对数损失约0.248。小数据上的计时会受调用和系统调度影响，因此图中同时给出资源定义，读者可以增加数据规模、重复运行，再研究何时实现差异开始占主导。

按叶生长的偏好可以通过计算预算看清：若当前一个叶分裂能减少损失十个单位，另一个只能减少一个单位，允许再增加一个叶时会优先选择前者。下一轮仍重新比较所有可分裂叶，因此某条分支可能连续加深。逐层生长则更接近给同层分支安排相同的扩展机会。样本很少的深叶更容易围绕个别记录形成细规则，最小叶样本数和最小二阶导数和控制的正是这种局部证据不足；它们与学习率缩小整棵树贡献的作用并不相同。

## CatBoost：类别统计怎样避免偷看自己的答案

用每个类别的平均目标替换类别名称，看起来能把文字变成有用数字，却容易泄漏。若某个类别只出现一次，直接用它的目标均值编码，该样本便把自己的答案带进输入。即使类别出现多次，同一个标签参与自身统计，也会让训练阶段的编码比未来样本更了解结果。CatBoost的有序目标统计按照某种顺序，只使用当前样本之前已经出现的同类记录，并加入先验平滑，使当前标签不直接进入自己的统计值。

$$
c_i=\frac{\sum_{j\in P_i}y_j+a p_0}{|P_i|+a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8491503cb3d88ee63e629414.svg) | 当前记录、较早记录索引、排列中位于i之前且类别相同的记录集合及其大小，集合不包含i。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2568d99f80750234e016f162.svg) | 二值目标、先验正类率、正的先验等效样本数与平滑类别编码；目标与比例无量纲。 |

同一类别依次出现目标1、0、1，先验0.5、a=1。第一条没有前序记录，编码0.5；第二条用第一条得到(1+0.5)/2=0.75；第三条用前两条得到(1+0+0.5)/3=0.5。当前目标从未参与自己的编码。这是有序目标统计的简化示例；CatBoost使用多种统计及排列。

假设同一类别按顺序出现三个标签1、0、1，先验均值0.5、先验强度1，则三个位置的教学编码依次为0.5、0.75和0.5。第一个位置没有之前的同类样本，只能使用先验；第二个位置可使用第一个标签；第三个位置看到前两个标签。整组均值2/3则包含了每个样本自己的结果，与这个过程不同。实际CatBoost具有多种统计类型与组合策略，这个小算例解释的是顺序排除自身标签和先验平滑的机制。

有序提升与有序类别统计相关，但处理的对象不同。前者用相应前缀模型计算样本的修正信号，减轻训练预测依赖自身目标带来的偏移；后者处理类别特征如何变成数值。代码显式选择Ordered模式，并把四分类列交给CatBoost，one_hot_max_size设为2，使该列走类别统计路径。常见对称树在同一深度使用相同分裂规则，便于规则化结构和预测计算；CatBoost也提供其他生长策略，示例参数决定这里实际使用什么。

本次CatBoost根据验证选择219棵深度3树，测试准确率92.5%、对数损失约0.230。Ordered设置在这次CPU实验中花费的时间明显高于另外几种配置，这是一项值得保留的实际取舍。若数据量更大、类别更多或使用不同生长模式，计算与精度关系会变化。类别处理便利并不免除时间切分：随机顺序中的“之前”不是现实时间中的过去，预测未来时仍要按真实日期控制训练、统计与验证的可用信息。

## 比较的单位，是完整工作流程

五个实现使用同一份训练、验证和测试索引，最大轮数都为400。AdaBoost使用深度1树桩和学习率0.1，固定保留全部400轮作为基线；它的验证曲线用于观察训练过程，没有参与选择轮数。其余分类提升树使用深度3和学习率0.05；LightGBM叶数上限为8，CatBoost使用Ordered。GBDT完整拟合400轮后在验证曲线上选择174轮，XGBoost、LightGBM和CatBoost使用验证损失与25轮耐心值选择轮数。这个设计统一了数据和一部分计算上限，也保留了各方法清楚的具体配置。若要做面向最优性能的算法比较，还应给每个实现相同的调参试验数或墙钟预算，而不把默认参数数量当成公平预算。

![同一360条测试记录上的准确率、对数损失，以及实际独立进程的拟合和曲线计算耗时、峰值常驻内存。资源测量包含指定的软件环境；中英文各自实际运行。](https://ml-biomat.com/static/tutorials/machine-learning/figures/dfe9dbea5c152d504c105fb2.svg?v=dfe9dbea5c15)

图 5同一360条测试记录上的准确率、对数损失，以及实际独立进程的拟合和曲线计算耗时、峰值常驻内存。资源测量包含指定的软件环境；中英文各自实际运行。

五个测试准确率依次约为84.72%、91.39%、91.11%、91.11%和92.5%；对应模型为AdaBoost、GBDT、XGBoost、LightGBM、CatBoost。几条强基线只相差少数样本，因此结果应连同概率损失和计算成本一起阅读。不同实现的类别编码使用相同原始信息。独热编码和LightGBM的类别词表均由训练记录确定；CatBoost接收原始类别字符串，其类别统计从训练记录学习。本例A、B、C、D四类都出现在训练集中。若类别具有真实时间顺序，或者同一用户有多条记录，拆分协议需要升级，不能沿用这里的独立生成行假设。

资源图的时间包含拟合、验证曲线计算和测试预测，不包含Python导入；内存是每个独立工作进程的峰值常驻内存，包含导入库和运行时。每个实现单独启动进程，避免先前模型残留改变后一个模型的基线。两个语言版本各自真实运行，因此短时计数可能稍有差别；它们不是多次重复后的性能排名。若研究部署成本，应进一步报告多次重复的中位训练时间、固定批量的预测吞吐与模型大小，明确线程数和硬件条件。

早停也是超参数选择。测试标签不能进入eval_set，类别统计不能使用测试目标，缺失填补和词表学习也应在训练侧完成。最终决定好轮数后，可以按预先定义的方案合并训练与验证重新拟合，再在保留测试上检查；也可以保留这里的训练模型以便直接对应验证曲线。两种方案都需要把实际训练数据范围记录下来，才能解释为什么某次最终模型与开发阶段的数值略有不同。

验证曲线也会有噪声，尤其当验证集只有少数正例时。第135轮优于第134轮，可能只对应几条记录概率的小幅移动。可以先规定耐心轮数和主要指标，再观察较宽的一段曲线是否平稳；如果反复按照测试分数改变这些规则，测试集就逐渐成了新的验证集。对于昂贵模型，保存每轮验证曲线还便于检查训练是否过早停止，或是否继续消耗许多轮却只获得极小改善。确定候选后，再用另一组独立记录或按部署方式重新划分的数据检查表现。

## 换一个目标，树仍然累加，修正信号却会改变

回归、分类与排序共享累加树的表示，但损失定义了每一轮应修正什么。平方回归追踪数值误差，分类对数损失追踪概率与标签之间的偏差，排序则关心同一查询内部候选的相对顺序。把不同查询的候选混成普通分类行，会丢失竞争集合；同一个查询的候选也应整体进入训练或测试。本例另生成80个查询，每个8个候选，60个查询训练、20个新查询测试，真正使用XGBRanker进行学习。

排序相关等级为0到3，依据明确的潜在效用加噪声后分配。NDCG先把相关等级换成增益，再让靠后位置的增益打折，最后除以同一查询中最理想顺序的得分。高相关候选放在前面，读者较早看到有用结果，分数就更高；把最相关候选埋到末尾，即使列表包含相同物品，也会损失分数。本例评价前5位，每个查询单独计算，再对20个测试查询取平均，得到约0.961。查询组之间的整体分数平移不会改变组内排序，因此原始分数不应直接解释为跨查询相同尺度的相关概率。排序树的更新关注同一查询内候选之间的相对顺序：把高相关候选放在低相关候选之后会产生需要修正的比较，NDCG相关的权重让影响列表质量的交换获得相应关注。树用特征拟合这些更新信号，逐轮改变候选的分数。这里报告的@5明确规定评价截止位置；训练过程使用代码中的rank:ndcg目标。曝光、比较样本与反馈来源决定了哪些偏好进入这些更新。

$$
\operatorname{DCG@K}=\sum_{r=1}^{K}\frac{2^{g_r}-1}{\log_2(r+1)},\qquad \operatorname{NDCG@K}=\frac{\operatorname{DCG@K}}{\operatorname{IDCG@K}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f10a207433df574f151b37b.svg) | 保留的排名位置数与从1开始的位置索引，均为无量纲计数；K不超过该查询候选数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3f8ef56587f0ba25bd66e77f.svg) | 第r位候选的相关等级与指数增益；本例等级为0、1、2、3，对应增益0、1、3、7，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/80e2f3a4c89172264f530f4a.svg) | 以2为底的对数折扣，第一位为1，第二位约1.585；分母越大，较后位置的贡献越小。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cecbf47d4b809626cad8fea7.svg) | 折损累计增益、将同一查询候选按相关等级降序排好所得的理想增益，以及二者的比值；均无量纲。理想增益为0时，本例评价约定NDCG为0。 |

假设只有两件候选，等级为3和1。把等级1放第一、等级3放第二，则DCG@2=1+7/log2(3)≈5.4165；理想顺序给IDCG@2=7+1/log2(3)≈7.6309，所以NDCG@2≈0.7098。理想顺序本身得1。完整实验先将等级变成增益，再把增益传给ndcg_score，按20个测试查询平均得到NDCG@5约0.961。

![一个测试观测的主要 XGBoost 特征贡献，单位为原始对数几率。完整输出中全部特征贡献与基线之和等于原始分数，转换后得到概率约0.1732。](https://ml-biomat.com/static/tutorials/machine-learning/figures/a8b85ab6f502573b9bb2ba9f.svg?v=a8b85ab6f502)

图 6一个测试观测的主要 XGBoost 特征贡献，单位为原始对数几率。完整输出中全部特征贡献与基线之和等于原始分数，转换后得到概率约0.1732。

$$
z=\phi_0+\sum_{j=1}^d\phi_j,\qquad p=\frac{1}{1+e^{-z}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a78d8c046bf3647434fdc286.svg) | 编码后特征数、特征索引、基线与各特征对原始分数的贡献；贡献与基线均为无量纲对数几率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/464baf38a8828b3364b642c3.svg) | 原始二分类分数、正类概率和自然指数底数；本式对应逻辑链接。 |

基线−1、两项贡献0.5与−0.2，相加得到z=−0.7，再转换得p≈0.3318。把贡献分别转换为概率后相加不满足这个关系。实际测试例的z≈−1.56295，p≈0.17322；全部贡献求和与原始分数的差约2.38×10⁻⁷。

XGBoost还可以为一个预测输出加性特征贡献。图中展示同一个测试样本的主要贡献，单位是原始对数几率分数；所有特征贡献加上基线，得到约−1.563，经sigmoid变成正类概率约0.1732。代码使用与早停预测相同的迭代范围，并检查贡献总和与原始分数之差，约为2.4×10的负7次方，符合浮点计算精度。只画最大的几个条形是为了阅读，完整相加时仍包括未画出的较小项。

贡献解释的是当前模型相对于其解释背景的分数分解，正贡献不等于该特征在现实中具有正向因果效应。独热列可以按原类别变量汇总，但相关输入与不同背景定义仍会影响解释。图中的零线表示贡献方向，整体概率还取决于基线和其他所有项。把这层关系讲清以后，解释图才有机会帮助定位某个预测由哪些输入驱动，而不是变成给模型结果附上一张看似有道理的彩色条形图。

### 完整实验：五种提升、残差、排序与特征贡献

使用NumPy、pandas、Matplotlib、scikit-learn、XGBoost、LightGBM和CatBoost。运行python main.py --output results --language zh。五种分类器分别在独立进程运行；输出包含原始数组、训练曲线、数值摘要和本节全部原创图。

```
"""Five real boosting implementations; isolated worker resource measurements."""
from pathlib import Path
import argparse,json,sys,subprocess,time,os,ctypes
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,log_loss,ndcg_score
from xgboost import XGBClassifier,XGBRanker,DMatrix
from lightgbm import LGBMClassifier,early_stopping,log_evaluation
from catboost import CatBoostClassifier

def peak_rss_mb():
    if os.name=='nt':
        class Counters(ctypes.Structure):
            _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
        c=Counters();c.cb=ctypes.sizeof(c);handle=ctypes.windll.kernel32.GetCurrentProcess;handle.restype=ctypes.c_void_p
        fun=ctypes.windll.psapi.GetProcessMemoryInfo;fun.argtypes=[ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_ulong];fun.restype=ctypes.c_int
        if not fun(handle(),ctypes.byref(c),c.cb):raise OSError('Process memory counter failed')
        return c.PeakWorkingSetSize/1024**2
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform=='darwin' else 1024)

def worker(name,datafile,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);a=np.load(datafile);X=a['X'];cat=a['category'];y=a['y'];tr=a['train'];va=a['validation'];te=a['test']
    enc=OneHotEncoder(handle_unknown='ignore',sparse_output=False).fit(cat[tr,None]);Z=np.c_[X,enc.transform(cat[:,None])]
    frame=pd.DataFrame(X,columns=[f'x{j}' for j in range(X.shape[1])]);frame['category']=cat
    lframe=frame.copy();dtype=pd.CategoricalDtype(categories=sorted(np.unique(cat[tr])));lframe['category']=lframe['category'].astype(dtype)
    curves={};start=time.perf_counter()
    if name=='AdaBoost':
        model=AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),n_estimators=400,learning_rate=.1,random_state=31);model.fit(Z[tr],y[tr]);prob=model.predict_proba(Z[te]);rounds=len(model.estimators_)
        curves={'train':[log_loss(y[tr],p) for p in model.staged_predict_proba(Z[tr])],'validation':[log_loss(y[va],p) for p in model.staged_predict_proba(Z[va])]}
    elif name=='GBDT':
        model=GradientBoostingClassifier(n_estimators=400,learning_rate=.05,max_depth=3,random_state=31);model.fit(Z[tr],y[tr]);vcur=[log_loss(y[va],p) for p in model.staged_predict_proba(Z[va])];rounds=int(np.argmin(vcur))+1
        curves={'train':[log_loss(y[tr],p) for p in model.staged_predict_proba(Z[tr])],'validation':vcur};prob=next(p for i,p in enumerate(model.staged_predict_proba(Z[te]),1) if i==rounds)
    elif name=='XGBoost':
        model=XGBClassifier(n_estimators=400,max_depth=3,learning_rate=.05,subsample=.85,colsample_bytree=.85,tree_method='hist',n_jobs=2,random_state=31,eval_metric='logloss',early_stopping_rounds=25,reg_lambda=1.)
        model.fit(Z[tr],y[tr],eval_set=[(Z[tr],y[tr]),(Z[va],y[va])],verbose=False);prob=model.predict_proba(Z[te]);rounds=model.best_iteration+1;ev=model.evals_result();curves={'train':ev['validation_0']['logloss'],'validation':ev['validation_1']['logloss']}
    elif name=='LightGBM':
        model=LGBMClassifier(n_estimators=400,max_depth=3,num_leaves=8,learning_rate=.05,n_jobs=2,random_state=31,verbosity=-1)
        xt=lframe.iloc[tr];yt=y[tr];xv=lframe.iloc[va];yv=y[va]
        model.fit(xt,yt,eval_X=(xt,xv),eval_y=(yt,yv),eval_names=['train','validation'],eval_metric='binary_logloss',callbacks=[early_stopping(25,verbose=False),log_evaluation(0)]);prob=model.predict_proba(lframe.iloc[te]);rounds=model.best_iteration_;curves={'train':model.evals_result_['train']['binary_logloss'],'validation':model.evals_result_['validation']['binary_logloss']}
    else:
        model=CatBoostClassifier(iterations=400,depth=3,learning_rate=.05,loss_function='Logloss',random_seed=31,thread_count=2,verbose=False,allow_writing_files=False,boosting_type='Ordered',one_hot_max_size=2)
        model.fit(frame.iloc[tr],y[tr],cat_features=['category'],eval_set=(frame.iloc[va],y[va]),early_stopping_rounds=25,use_best_model=True);prob=model.predict_proba(frame.iloc[te]);rounds=model.tree_count_;ev=model.get_evals_result();curves={'train':ev['learn']['Logloss'],'validation':ev['validation']['Logloss']}
    elapsed=time.perf_counter()-start;peak=peak_rss_mb();result={'name':name,'test_accuracy':float(accuracy_score(y[te],prob.argmax(1))),'test_log_loss':float(log_loss(y[te],prob)),'selected_rounds':int(rounds),'fit_and_curve_seconds':elapsed,'worker_peak_rss_mb':peak,'curves':curves}
    if name=='XGBoost':
        booster=model.get_booster();dm=DMatrix(Z[te[:1]]);contrib=booster.predict(dm,pred_contribs=True,iteration_range=(0,rounds))[0];margin=float(booster.predict(dm,output_margin=True,iteration_range=(0,rounds))[0]);result['contribution_sum_error']=float(abs(contrib.sum()-margin));result['example_margin']=margin;result['example_probability']=float(prob[0,1]);result['contributions']=contrib.tolist();result['feature_names']=[f'x{j}' for j in range(X.shape[1])]+enc.get_feature_names_out(['category']).tolist()+['bias'];model.save_model(out/'model.ubj')
    (out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf8');np.save(out/'test_probability.npy',prob)

def main(output,language):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(31)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
    def t(z,e):return z if zh else e
    def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
    X,y=make_classification(n_samples=1800,n_features=10,n_informative=5,n_redundant=2,class_sep=1.,flip_y=.03,random_state=31)
    category=np.array(['A','B','C','D'])[np.digitize(X[:,0],[-.7,0,.7])];idx=np.arange(1800);tr,tmp=train_test_split(idx,test_size=.4,stratify=y,random_state=31);va,te=train_test_split(tmp,test_size=.5,stratify=y[tmp],random_state=31)
    datafile=out/'classification_data.npz';np.savez(datafile,X=X,category=category,y=y,train=tr,validation=va,test=te)
    results={}
    for name in ['AdaBoost','GBDT','XGBoost','LightGBM','CatBoost']:
        dest=out/'workers'/name;run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',name,'--data',str(datafile),'--output',str(dest)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(f'{name} failed:\n{run.stderr}')
        results[name]=json.loads((dest/'summary.json').read_text())
    # Gradient boosting for a known continuous relationship, exposing component trees.
    xr=np.sort(rng.uniform(-2,2,100));yr=np.sin(2*xr)+.25*xr+rng.normal(0,.18,100);reg=GradientBoostingRegressor(n_estimators=60,learning_rate=.15,max_depth=2,random_state=31).fit(xr[:,None],yr);grid=np.linspace(-2,2,300);staged=list(reg.staged_predict(grid[:,None]));initial=float(yr.mean());first=reg.estimators_[0,0].predict(grid[:,None]);residual=yr-initial
    fig=plt.figure(figsize=(12,6),layout='constrained');gs=fig.add_gridspec(2,3)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(xr,yr,s=12,color='#167d87');ax.axhline(initial,color='#d48745');ax.set(title=t('初始常数预测','Initial constant prediction'),xlabel='x',ylabel='y')
    ax=fig.add_subplot(gs[0,1]);ax.scatter(xr,residual,s=12,color='#167d87');ax.plot(grid,first,color='#d48745');ax.axhline(0,color='#a3b7c1',lw=.7);ax.set(title=t('第一棵树拟合残差','First tree fits residuals'),xlabel='x',ylabel=t('残差','Residual'))
    ax=fig.add_subplot(gs[0,2]);ax.plot(grid,.15*first,color='#d48745');ax.set(title=t('加入15%的树贡献','Add 15% of the tree contribution'),xlabel='x',ylabel=t('新增预测','Added prediction'))
    for ax,n in zip([fig.add_subplot(gs[1,j]) for j in range(3)],[1,10,60]):ax.scatter(xr,yr,s=9,color='#9bb1bd');ax.plot(grid,np.sin(2*grid)+.25*grid,'--',color='#263d4b');ax.plot(grid,staged[n-1],color='#167d87');ax.set(title=f'{n} '+t('棵树','trees'),xlabel='x',ylabel='y')
    save(fig,'residual_steps')
    fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');colors=['#9b6b89','#b78a44','#167d87','#5275a3','#7648a0']
    for (name,r),color in zip(results.items(),colors):
        axs[0].plot(np.arange(1,len(r['curves']['validation'])+1),r['curves']['validation'],label=name,color=color);axs[1].plot(np.arange(1,len(r['curves']['train'])+1),r['curves']['train'],label=name,color=color)
    axs[0].set(title=t('验证集概率对数损失','Validation probability log loss'),xlabel=t('树数','Tree count'),ylabel=t('对数损失（nat）','Log loss (nats)'));axs[1].set(title=t('训练集概率对数损失','Training probability log loss'),xlabel=t('树数','Tree count'),ylabel=t('对数损失（nat）','Log loss (nats)'));axs[0].legend();save(fig,'curves')
    fig,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained');names=list(results)
    for ax,key,label in zip(axs.ravel(),['test_accuracy','test_log_loss','fit_and_curve_seconds','worker_peak_rss_mb'],[t('测试准确率','Test accuracy'),t('测试对数损失（nat）','Test log loss (nats)'),t('拟合与曲线计算时间（秒）','Fit and curve-computation time (s)'),t('独立进程峰值RSS（MiB）','Isolated-process peak RSS (MiB)')]):
        values=[results[n][key] for n in names];ax.barh(names,values,color=colors);ax.set(xlabel=label);ax.invert_yaxis();ax.set_xlim(0,max(values)*1.18)
        for i,v in enumerate(values):ax.text(v,i,f' {v:.3f}' if key!='worker_peak_rss_mb' else f' {v:.1f}',va='center',fontsize=10)
    save(fig,'comparison')
    r=results['XGBoost'];con=np.array(r['contributions']);order=np.argsort(np.abs(con[:-1]))[::-1][:7];fig,ax=plt.subplots(figsize=(9,4.6),layout='constrained');ax.barh(np.arange(len(order)),con[order],color=np.where(con[order]>=0,'#d48745','#167d87'));ax.set_yticks(np.arange(len(order)),np.array(r['feature_names'])[order]);ax.axvline(0,color='#7d97a4');ax.set(xlabel=t('原始分数贡献（log-odds）','Raw-score contribution (log odds)'),title=t('同一个测试样本：贡献相加得到原始分数','One test observation: contributions add to the raw score'));ax.invert_yaxis();save(fig,'contributions')
    # Query-disjoint ranking: each query contains eight candidates, relevance0..3.
    qx=rng.normal(size=(80,8,4));utility=2*qx[:,:,0]-qx[:,:,1]+.4*rng.normal(size=(80,8));rel=np.empty((80,8),int)
    for q in range(80):rel[q,np.argsort(utility[q])]=np.repeat(np.arange(4),2)
    ranker=XGBRanker(n_estimators=60,max_depth=3,learning_rate=.1,objective='rank:ndcg',tree_method='hist',n_jobs=2,random_state=31)
    ranker.fit(qx[:60].reshape(-1,4),rel[:60].ravel(),qid=np.repeat(np.arange(60),8));rs=ranker.predict(qx[60:].reshape(-1,4)).reshape(20,8);ranking=float(ndcg_score(2**rel[60:]-1,rs,k=5))
    summary={'train_n':len(tr),'validation_n':len(va),'test_n':len(te),'numeric_features':10,'categories':4,'models':{n:{k:v for k,v in r.items() if k not in ['curves','contributions','feature_names']} for n,r in results.items()},'regression_initial_residual_sum':float(residual.sum()),'xgb_contribution_sum_error':results['XGBoost']['contribution_sum_error'],'ranking_train_queries':60,'ranking_test_queries':20,'ranking_candidates_per_query':8,'ranking_ndcg5':ranking}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'regression_ranking_data.npz',x=xr,y=yr,rank_X=qx,rank_relevance=rel,rank_prediction=rs)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');ap.add_argument('--worker');ap.add_argument('--data');a=ap.parse_args()
    if a.worker:worker(a.worker,a.data,a.output)
    else:main(a.output,a.language)
```

学习Boosting可以沿着一条可核对的路线继续：先手算一次权重更新，再追踪一轮负梯度与新增树，接着观察验证损失选择了哪一轮，最后对一个实际预测把所有贡献加回去。算法、软件和任务的区别都会落到这条路线中的不同位置。面对新数据时，先确定响应类型、类别结构和部署切分，再给候选实现分配明确的比较预算，结果就能指导下一步研究。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M31.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Freund & Schapire (1997), A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting](https://www.schapire.net/papers/FreundSc95.pdf)

   乘法权重与AdaBoost的研究背景。
2. [Friedman (2001), Greedy Function Approximation: A Gradient Boosting Machine](https://www.cmi.ac.in/~madhavan/courses/dmml2025/literature/Friedman-Gradient-Boosting-Machine-2001.pdf)

   函数空间中的梯度提升。
3. [XGBoost — Introduction to Boosted Trees](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)

   二阶展开、叶值与正则化。

   Apache-2.0 project; technical reference
4. [LightGBM — Features](https://lightgbm.readthedocs.io/en/stable/Features.html)

   直方图、按叶生长与两幅原始树结构图。

   MIT; Microsoft and LightGBM developers
5. [LightGBM (2017)](https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html)

   GOSS与EFB的原论文。
6. [CatBoost — Transforming categorical features to numerical features](https://catboost.ai/docs/en/concepts/algorithm-main-stages_cat-to-numberic)

   类别统计与先验。
7. [CatBoost: unbiased boosting with categorical features](https://arxiv.org/abs/1706.09516)

   有序提升与类别处理的区别。
8. [LightGBM license](https://github.com/microsoft/LightGBM/blob/master/LICENSE)

   原图的完整MIT许可。

   MIT
