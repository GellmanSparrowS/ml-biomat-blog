# 决策树与森林：让不同的规则共同判断

Source: https://ml-biomat.com/tutorials/machine-learning/m30/
Language: zh-CN

读懂一刀切分，再用真实树的差异、袋外记录和相关特征检验集成。

## 一次只问一个问题，为什么也能形成复杂判断

挑选水果时，人会依次观察大小、颜色和软硬：颜色偏青时再看硬度，颜色成熟时也许改看表皮损伤。决策树把这样的条件判断写成一个可以计算的结构。每个内部节点询问某个特征是否超过阈值，根据答案走向不同分支，最后在叶节点给出类别比例或平均响应。树不需要先把整个输入空间压成一条直线，它可以在不同区域采用不同规则，因此常常能自然表达阈值效应和特征之间的条件关系。

这种可读性会随树深迅速改变。一个两层树的规则可以逐条检查，一棵有上百个叶节点的树则很难靠肉眼理解，而且训练数据稍微变化，早期分裂就可能换成另一列特征。森林利用的正是这种变化：让许多树在不同数据和候选特征上成长，再合并预测。本章先把单次分裂算清楚，再讨论怎样限制一棵树、怎样制造有用的差异，以及为什么复制许多相同的树并不能带来同样收益。

教学图分成两个任务。两个月牙数据用于展示一棵深度为2的树及其特征空间分区；另一份1000条、9个特征的分类数据用于比较模型，其中一列是另一列的近似副本。所有方法共享750条训练记录与250条测试记录，既比较类别准确率，也保留概率对数损失和袋外结果。这样可以同时看到规则、计算过程和独立测试，而不会用一张漂亮的树图代替性能检验。

## 沿着树读一次预测，再看它切出了什么

从根节点出发，读取当前特征与阈值，例如第二个坐标是否小于某个数。符合条件走左侧，不符合走右侧，直到遇到叶节点。叶中的训练类别计数决定预测概率；若采用均匀权重，有80个正例、20个负例的叶便给出0.8的正类概率。回归树则通常输出叶中目标的平均值。树的输出在一个叶区域内保持不变，因此标准CART模型是一种分段常数近似，而不是每个叶里都拟合一条新的斜线。

![200个月牙观测拟合的深度2分类树。每个节点包含阈值、Gini、样本数、类别分布和预测类；此小树用于解释结构。](https://ml-biomat.com/static/tutorials/machine-learning/figures/992e7057fe184c6ec8820528.svg?v=992e7057fe18)

图 1200个月牙观测拟合的深度2分类树。每个节点包含阈值、Gini、样本数、类别分布和预测类；此小树用于解释结构。

图中的每个节点同时给出条件、不纯度、样本数和类别分布。样本数说明这条规则由多少记录支持，类别分布说明它还保留多少混合。不要只看最后预测类别，因为两个都预测正类的叶，一个可能有51%的正例，另一个有98%。这些比例来自到达该叶的训练记录，叶很小时会有较大波动；纯叶的概率0或1也不意味着未来必然如此，后面的对数损失会显示这种极端概率的代价。

![左：同一小树的分段常数概率区域；右：六个回归观测的所有五个候选切分误差，3.5处最小。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d2f9951de906f5b979cbea70.svg?v=d2f9951de906)

图 2左：同一小树的分段常数概率区域；右：六个回归观测的所有五个候选切分误差，3.5处最小。

把节点对应到平面，会发现每次分裂都是沿某个坐标轴切一刀，叶区域因此呈矩形或若干轴向限制的交集。不同深度允许不同数量的矩形，能够逐步靠近弯曲边界。对单个特征做严格单调变换，数值阈值会改变，但排序保持，很多树分裂也会对应到相同记录；因此树通常不像距离模型那样依赖标准化。若把缺失、类别编码或浮点精度改变了，仍需检查实际实现如何处理这些情况。

CART每一步在当前节点内比较候选特征和阈值，选取带来最大局部改善的一刀，再递归处理子节点。这是贪心搜索：它不尝试所有可能的整棵树再寻找全局最优。早期看起来相近的两种选择，可能引导后续走向不同结构。于是树的可解释性不仅是把结果画出来，还包括承认规则来自特定样本与局部搜索，并通过重复拟合观察重要分裂是否稳定。

分段常数还决定了回归树的外推方式。若所有训练温度都低于40℃，输入45℃和60℃可能沿同一条最右分支到达同一个叶，给出相同预测。若任务需要延续一个随温度增长的物理趋势，可以加入有明确趋势结构的模型，或采用叶内带回归关系的方法，再用超出训练范围的数据检验。先看数据范围与叶规则，能提前发现这种选择是否符合实际用途。

## 怎样判断一刀切得好不好

分类节点里，两类各一半时最混合，几乎全是同一类时较纯。Gini不纯度可以理解为根据节点类别比例随机抽一个标签，它与另一个独立同分布标签不一致的概率。二分类各一半时为0.5，全部同类时为零。信息熵也衡量混合程度，但通过对数信息量计算。选择哪一种准则会改变具体分裂，二者共同要求的是：切分以后子节点加权平均的不纯度比父节点更低。

$$
G=1-\sum_{c=1}^Kp_c^2,\quad H=-\sum_{c=1}^Kp_c\log_2p_c,\quad\Delta I=I_P-\frac{n_L}{n_P}I_L-\frac{n_R}{n_P}I_R
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/162b3577db3a5ef438ec5a18.svg) | Gini不纯度与类别熵；G无量纲，H以bit为单位，0log0约定为0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/23101535a78b5a0b7f96efde.svg) | 类别数、类别索引与节点内类别比例；比例和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0f60d2a597bb8013e28d25d3.svg) | 父、左、右节点及其样本数；左右数目相加等于父节点。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc87fcda8a2145b3494ee548.svg) | 采用同一准则的不纯度和切分改善；分类均匀权重情形，改善与所用准则同单位。 |

父节点正负各5，G=0.5。切为左侧1正4负、右侧4正1负，两侧G均0.32，加权后仍0.32，改善0.18。熵则从1 bit降为约0.7219 bits，改善约0.2781 bits。

子节点一定要按样本比例加权。如果一刀切出一个只有两条记录的纯节点，剩下98条仍然混杂，简单平均两个节点会夸大那两条记录的贡献。按节点人数计算，才能比较整批样本的整体改善。信息增益就是父节点熵减去加权子节点熵；Gini减少则使用Gini值进行同样操作。若有样本权重，人数要替换为相应权重和，成本敏感学习也会因此改变树的生长方向。

回归目标没有类别比例，因此可以比较各节点相对于自身均值的平方残差。图2右侧使用六个输入位置，目标依次为1、1、2、6、7、7。阈值放在3.5时，左侧围绕4/3波动，右侧围绕20/3波动，两侧平方残差总和为4/3；其他候选阈值的误差更大。这一小例子说明回归树为何会把低值区和高值区分开，也说明所谓“方差减少”最终落实到哪些观测和哪些平方差。

$$
\operatorname{SSE}(A)=\sum_{i\in A}(y_i-\overline y_A)^2,\quad\operatorname{gain}=\operatorname{SSE}(P)-\operatorname{SSE}(L)-\operatorname{SSE}(R)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/54be1efeb49676ff8c1329e5.svg) | 一个节点包含的样本集合，以及父、左、右样本集合。 |
| ![Formula](https://ml-biomat.com/static/agent-math/42ee64482fbba1d88dd2092a.svg) | 样本索引、目标和节点内目标均值，后两者同目标单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/74e6b44ae4fc5c77f51ba9ee.svg) | 节点平方残差和及减少量，单位为目标单位平方。 |

六个目标(1,1,2,6,7,7)的父均值4，SSE=44。前三个均值4/3、后三个20/3，各自SSE=2/3，总和4/3，减少128/3≈42.6667。

不纯度改善是训练目标，不是泛化成绩。若允许树不断分裂，每个叶最终可能只保留一个样本，训练不纯度降到零，却把测量噪声也写进规则。对连续特征，候选切分通常位于相邻不同值之间；唯一值很多的特征拥有更多尝试机会，这也会影响基于不纯度的特征重要性。后续解释时需要用独立数据上的置换结果与相关特征结构共同检查，而不是把训练中累计改善直接读成变量的真实作用大小。

多分类不纯度把所有类别比例一起计算，因此十种数字或多种故障也能采用同一框架。类别权重会改变这些比例及切分选择：提高稀少故障的权重，树会更加重视它们，但叶中的加权比例也随之改变。若希望输出部署总体中的事件概率，就要结合真实类别比例与校准数据评价，而不是把加权叶比例直接照搬为人群发生率。

## 树应该长到什么时候

最大深度限制从根到叶的提问次数，最小叶样本数要求每个最终规则有足够观测支持，最大叶数直接限制区域数量。这些是提前限制生长的办法。它们分别控制规则长度、局部样本量和总体复杂度，因此不能只看树深一个参数。某一分支可能很深却覆盖很少记录，另一棵较浅的树也可能因频繁切分而产生很多叶。读模型时应把结构与每个叶的支持样本一起看。

$$
R_\alpha(T)=R(T)+\alpha|\mathcal L(T)|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5a8a6e0c58abbfa6ec2dcd0.svg) | 候选树、叶节点集合和叶数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/586d0d3d830f3827601c2df2.svg) | 所有叶的样本加权训练不纯度；分类中采用相同的Gini或熵准则。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8e41357d56827d913d4f97e.svg) | 每叶复杂度惩罚与总目标；alpha非负，具有每叶不纯度单位。 |

大树训练风险0.10、有10个叶，小树风险0.16、有4个叶。alpha=0.005时目标分别0.15与0.18，大树较好；alpha=0.02时分别0.30与0.24，小树较好。

代价复杂度剪枝先考虑较大的树，再比较删除子树所增加的训练误差与减少的叶数。惩罚系数越大，保留每一个叶就越昂贵，树通常越小。本例只在训练数据内生成候选剪枝强度，再用三折训练侧验证选择，最终测试集始终留在外面。完整树有59个叶，选出的剪枝树有11个叶，测试准确率从85.6%提高到88.4%，对数损失从约5.19降到0.479。剪枝同时减少了部分过于自信的错误概率。

这里的改善并不要求剪枝总能提高成绩。如果训练数据很充足、真实边界复杂，过强剪枝会损失有用结构。验证选择的任务正是寻找当前数据下的取舍。候选剪枝路径来自开发数据时，内层最高分承担选择工作；最终独立测试用于评价选完之后的流程。若还需要比较整个选择流程的抽样变化，可以将这一步放入外层交叉验证，而不是反复用同一测试集改剪枝范围。

可以先用下面的互动练习一个更局部的选择：固定十个标签，改变切分阈值，并在Gini与熵之间切换。界面同时显示左右样本、两侧比例和加权改善。选择极靠边的阈值时，一个小节点可能很纯，总改善却有限；中间的一刀若把两类较好分开，总改善就更大。把这种数值直觉建立起来，再看一整棵树的许多分裂会容易得多。

## 这一次分裂，改善了多少

十个观测按特征值1到10排列，颜色表示真实类别。每个柱表示一个候选切分的加权不纯度改善。

[Figure: 节点分裂与不纯度改善](https://ml-biomat.com/tutorials/machine-learning/m30/#M30-plot)

## 重新抽取数据，让不稳定的树彼此补充

Bootstrap从n条训练记录中有放回抽取n次，有些记录被抽中多次，有些一次没有。每一次抽样都会改变树看到的经验分布，进而改变它的分裂。Bagging把这种抽样应用于许多个基础学习器，回归时平均预测，分类时可以投票或平均类别概率。本例的软件实现对树的类别概率取平均。若单棵树对样本扰动敏感，而这些变化并不完全同步，平均就有机会减少波动。

$$
P(\text{record omitted})=\left(1-\frac1n\right)^n\approx e^{-1},\quad\mathbb E[N_{\rm OOB}]=B\left(1-\frac1n\right)^n
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7650612bb33f7ec603d9bbfb.svg) | 原训练记录数与独立bootstrap树数，均为计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c44375a21549caa3f590b2e2.svg) | 某一训练记录没有参与拟合的树数，单位为棵。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4f4d0e8dc3cc1608cce6e48f.svg) | 概率、期望与自然指数底数；近似在n较大时成立。 |

每次抽取未选中指定记录的概率1−1/n，n次有放回独立抽取相乘得到该式。n=750、B=120时，期望约44.116棵；一棵树约使用63.2%的不同训练记录。

Breiman在1996年的Bagging工作和2001年的随机森林研究，围绕一个看似矛盾的现象展开：单个学习器的不稳定性，有时正是组合后能够改善的原因。如果每次抽样都得到完全相同的预测，平均一百次仍然是原来的预测；如果不同树的偏差方向部分抵消，集体结果才会更稳定。它像几位测量者各自读数后取平均，但要特别留意他们是否共享同一把偏掉的尺子。共同误差不会因为人数增加而消失。

$$
\operatorname{Var}\!\left(\frac1B\sum_{b=1}^B Z_b\right)=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ed376fee9c98c195228f7c6.svg) | 基础预测器数量、索引与同一输入的随机预测，Z单位为响应单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0b55f8c2ddff1b47486bb264.svg) | 每个预测相同的方差与每对预测相同的相关系数；方差为响应单位平方，相关无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | 对规定的数据/模型随机性计算方差；这是等方差等相关的教学模型。 |

sigma²=1、B=10时，若rho=0，平均方差为0.1；rho=0.3则为0.37。B增加到100，后者为0.307，继续增加树无法消掉共同的0.3项。

这个方差式子在各预测具有相同方差、各对具有相同相关系数的简化条件下，把“增加树数”和“减少相关性”分开。树数增大只能压低可平均掉的那一部分，相关性留下一个下限。现实树之间不必满足完全相同的关系，但这个分解提供清楚的设计方向。Bagging通常对高方差的深树比较有效；如果基础模型本来就非常稳定，重复抽样和平均的收益可能很小。

本例训练120棵Bagging树，独立测试准确率为89.2%，高于单棵未剪枝树的85.6%。袋外估计为92.0%，与独立测试并不相等，因为它们使用不同的评估样本与不同数量的参与树。平均概率也没有保证所有指标都改善到同样程度：Bagging的测试对数损失约0.653，仍高于剪枝树的0.479。比较时保留这些不同结果，才能判断增加树数解决了分类边界还是概率输出中的问题。

森林内部不同树的预测分散程度，反映给定数据下抽样和特征随机化带来的变化。未来观测本身的噪声、重新采集整批训练数据的变化以及输入分布迁移，是另外的随机性。若目标是给出有指定覆盖率的预测区间，应明确区间针对哪一种随机性，再采用相应的校准或概率方法。直接画出树预测的几个分位数，可以描述森林成员差异，但需要额外步骤才能回答未来观测落在哪个范围。

## 为什么每个节点还要少看几列特征

即使每棵树抽到了不同样本，某个强特征仍可能反复赢得根节点分裂，使许多树形成相似结构。随机森林在每个节点再随机挑选一部分候选特征，只在其中寻找最好的切分。这样一些树暂时看不到最强特征，被迫利用其他信息，降低彼此的相似性。随机性不是目的本身：候选特征太少也会使每棵树变弱。因此需要同时观察单树表现、树之间的错误相关程度以及最终森林的表现。

![左：七个具体模型在相同250条测试记录上的准确率；右：每节点候选特征数变化时的单树平均准确率、森林准确率与实测错误相关。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6dd49c5424040a8a9f11b95b.svg?v=6dd49c542404)

图 3左：七个具体模型在相同250条测试记录上的准确率；右：每节点候选特征数变化时的单树平均准确率、森林准确率与实测错误相关。

本例把每个节点可看的特征数设为1、3和9。单树平均准确率约为79.7%、84.9%和85.2%，而树间错误指示的平均相关系数约为0.224、0.323和0.431。森林准确率分别为91.6%、92.0%和88.8%。中间设置在这一拆分上兼顾了单树能力与差异。图里的错误相关系数是对250条测试记录实际计算的教学诊断，与Breiman论文中专门定义的理论强度和相关量不同；两者共享的是考察能力与相关性共同作用的思路。

增加森林中的树数主要降低平均预测的蒙特卡洛波动，通常不像无限加深单棵树那样不断增加局部拟合能力，但仍消耗内存和预测时间。每个节点候选特征数、叶样本数、抽样比例和最大深度会改变基础树本身。可以先固定这些设置，观察树数增加时袋外分数与预测稳定性是否趋于平缓，再决定继续增加树是否值得。对时间或分组数据，验证方式仍需遵守部署结构，森林的随机抽样不会自动处理样本依赖。

森林中的单个路径可以说明某棵树怎样判断，却不能用一棵“代表树”替代整个集成的计算。解释一个样本时，可以查看它在不同树中到达的叶概率、局部贡献或条件响应；解释全局行为时，再研究特征重要性、部分依赖和错误分组。把解释对象说清楚，才能让读者知道图里展示的是某个基础学习器、平均预测，还是整个数据总体上的关系。

## 没被某棵树抽中的记录，可以做什么

一条训练记录没有进入某棵树的bootstrap样本，就叫该树的袋外记录。预测这条记录时，只使用没有见过它的那些树，再把所有记录的袋外预测汇总成评分。这样可以在保留训练数据利用率的同时，得到一个内部评估信号。本例750条训练记录、120棵树，每条记录平均有44.04棵袋外树，与理论期望44.12接近。图中显示完整分布，而不是假设每条记录恰好有同样多的验证树。

![左：同一森林的不纯度重要性与测试置换准确率下降，两者定义不同；误差线为十次置换标准差。右：120次bootstrap中每条记录的袋外树数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e5adc235783763f61e57301d.svg?v=e5adc2357837)

图 4左：同一森林的不纯度重要性与测试置换准确率下降，两者定义不同；误差线为十次置换标准差。右：120次bootstrap中每条记录的袋外树数。

袋外估计的隔离单位是记录。如果同一对象的近似副本仍在其他训练行中，某条记录虽被留出，其对象信息仍可能被树看到；这正是评估章的分组问题。因此袋外分数适合作为符合独立记录假设的内部诊断，部署到新对象或未来时间时，应保留对应的外部切分。反复根据袋外分数选择大量设置，也会把它变成调参依据，最后仍需对选定流程做独立检查。

不纯度重要性把某列参与分裂时带来的训练不纯度减少累计起来，再归一化。它计算方便，却可能偏向可选阈值很多的特征，并把相关变量的贡献分散。置换重要性则在指定评价数据上打乱一列，观察分数下降，回答当前模型在这个分布下有多依赖该列。它不需要重新训练，但打乱会破坏特征之间的关系，因此在高度相关的数据中需要仔细定义要扰动什么。

本例x₈是x₀加上很小噪声得到的副本。分别打乱x₀和x₈，准确率平均只下降0.6和0.36个百分点，因为另一列仍提供相近信息；把两列用同一个行置换一起打乱，平均下降10.24个百分点。这个差别不表示两个小数相加算错，而是说明“单列可替代性”和“整组信息贡献”是不同问题。重要性图的列必须配合相关结构和扰动定义阅读，后续解释章节会进一步展开这种背景依赖。

资源比较也应落实到具体结构。预测一条记录需要在各树中沿路径走到叶，树数与路径长度共同影响操作数，保存的节点和阈值则占用内存。相同树数下，较大的最小叶样本数常会减少节点；只比较树数无法说明两个森林具有相同成本。实际选择时可记录模型文件大小、批量预测耗时和独立测试表现，并使用重复计时减少系统调度的影响。

## 更随机的树、直接投票与再学一次组合规则

Extra Trees进一步随机化候选切分阈值，再在这些随机候选中选择较好的分裂。常见实现默认使用整个训练集而不做bootstrap，所以增加随机性的来源与普通随机森林不同。随机阈值能减少搜索和树间相似性，也可能降低单树精度；具体收益要看数据中的结构。这里120棵Extra Trees测试准确率为92.4%，比随机森林的92.0%多答对一条记录；对数损失却分别约0.369和0.241。一个小的准确率差异并不决定所有预测用途。

投票组合可以混合不同模型家族。硬投票合并类别决定，软投票平均概率；若概率尺度或校准差别很大，简单平均未必合适。Stacking则让第二层模型学习如何组合第一层输出，关键是第二层训练样本必须来自第一层未见过该样本时的预测。代码使用三折折外预测训练逻辑回归组合器，再把基础模型拟合于全部训练数据，用于最终测试。直接把基础模型的训练集内预测交给第二层，会让组合器学习到过于乐观的输入。

本例把逻辑回归、15近邻和80棵随机森林作为三种基础模型。软投票测试准确率为89.6%，Stacking为92.0%；后者的对数损失约0.234。它们共享基础模型集合，却采用不同组合规则，结果说明“多放几个模型”与“学习如何组合”有不同作用。所有设置都在同一独立测试集上一次性比较，接下来若按这些结果继续选择和修改组合，应把这一比较视为开发信息，再安排新的最终评估。

### 完整实验：从单树到森林、投票与Stacking

需要NumPy、Matplotlib、scikit-learn。运行python main.py --output results --language zh，得到四组图、summary.json和保存所有输入与拆分的experiment_data.npz。

```
"""Inspect CART, bootstrap diversity and honest stacking on seeded data."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification,make_moons
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.ensemble import BaggingClassifier,RandomForestClassifier,ExtraTreesClassifier,VotingClassifier,StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.metrics import accuracy_score,log_loss
from sklearn.inspection import permutation_importance

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(30)
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
 Xm,ym=make_moons(n_samples=200,noise=.22,random_state=30);small=DecisionTreeClassifier(max_depth=2,random_state=30).fit(Xm,ym)
 fig,ax=plt.subplots(figsize=(12,5.6),layout='constrained');annotations=plot_tree(small,feature_names=['x₀','x₁'],class_names=['0','1'],filled=True,rounded=True,fontsize=11,ax=ax)
 if zh:
  for annotation in annotations:annotation.set_text(annotation.get_text().replace('gini','基尼').replace('samples','样本数').replace('value','类别计数').replace('True','是').replace('False','否').replace('class','预测类'))
 save(fig,'tree')
 gx,gy=np.meshgrid(np.linspace(-1.7,2.7,160),np.linspace(-1.2,1.7,140));grid=np.c_[gx.ravel(),gy.ravel()];fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');axs[0].contourf(gx,gy,small.predict_proba(grid)[:,1].reshape(gx.shape),levels=np.linspace(0,1,11),cmap='RdBu_r',alpha=.6);axs[0].scatter(*Xm.T,c=ym,cmap='RdBu_r',s=15,edgecolor='white',lw=.3);axs[0].set(xlabel='x₀',ylabel='x₁',title=t('深度2分类树的矩形区域','Rectangular regions of a depth 2 tree'))
 xr=np.arange(1,7);yr=np.array([1.,1.,2.,6.,7.,7.]);cuts=np.arange(1.5,6,1);loss=[]
 for cut in cuts:
  left=yr[xr<=cut];right=yr[xr>cut];loss.append(float(np.sum((left-left.mean())**2)+np.sum((right-right.mean())**2)))
 axs[1].plot(cuts,loss,'o-',color='#167d87');axs[1].set(xlabel=t('回归树候选阈值','Regression-tree candidate threshold'),ylabel=t('两侧平方残差和','Within-child squared-error sum'),xticks=cuts);axs[1].axvline(3.5,color='#d48745',ls='--');fig.colorbar(axs[0].collections[0],ax=axs[0],shrink=.8,label=t('正类概率','Positive probability'));save(fig,'splits')
 X,y=make_classification(n_samples=1000,n_features=8,n_informative=4,n_redundant=2,n_clusters_per_class=2,class_sep=1.,flip_y=.04,shuffle=False,random_state=30);X=np.c_[X,X[:,0]+rng.normal(0,.03,len(X))];tr,te=train_test_split(np.arange(1000),test_size=.25,stratify=y,random_state=30)
 cv=StratifiedKFold(3,shuffle=True,random_state=30);full=DecisionTreeClassifier(random_state=30).fit(X[tr],y[tr]);alphas=full.cost_complexity_pruning_path(X[tr],y[tr]).ccp_alphas;subset=np.unique(np.quantile(alphas,np.linspace(0,.9,12)))
 search=GridSearchCV(DecisionTreeClassifier(random_state=30),{'ccp_alpha':subset},cv=cv,scoring='accuracy');search.fit(X[tr],y[tr]);pruned=search.best_estimator_
 base=[('lr',make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500))),('knn',make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=15))),('rf',RandomForestClassifier(n_estimators=80,max_features=3,random_state=30,n_jobs=1))]
 models={'Tree':full,'Pruned tree':pruned,'Bagging':BaggingClassifier(estimator=DecisionTreeClassifier(),n_estimators=120,oob_score=True,random_state=30,n_jobs=1),'Random forest':RandomForestClassifier(n_estimators=120,max_features=3,oob_score=True,random_state=30,n_jobs=1),'Extra Trees':ExtraTreesClassifier(n_estimators=120,max_features=3,random_state=30,n_jobs=1),'Soft vote':VotingClassifier(estimators=base,voting='soft',n_jobs=1),'Stacking':StackingClassifier(estimators=base,final_estimator=LogisticRegression(),cv=cv,n_jobs=1)}
 results={}
 for name,m in models.items():
  m.fit(X[tr],y[tr]);p=m.predict_proba(X[te]);results[name]={'test_accuracy':float(accuracy_score(y[te],p.argmax(1))),'test_log_loss':float(log_loss(y[te],p)),'oob_accuracy':float(m.oob_score_) if hasattr(m,'oob_score_') else None}
 diversity=[]
 for mf in [1,3,9]:
  rf=RandomForestClassifier(n_estimators=120,max_features=mf,oob_score=True,random_state=30,n_jobs=1).fit(X[tr],y[tr]);errs=np.array([e.predict(X[te])!=y[te] for e in rf.estimators_],dtype=float);cc=np.corrcoef(errs);pair=float(cc[np.triu_indices_from(cc,1)].mean());diversity.append({'max_features':mf,'mean_tree_accuracy':float(1-errs.mean()),'error_correlation':pair,'forest_accuracy':float(rf.score(X[te],y[te])),'oob_accuracy':float(rf.oob_score_)})
 fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');positions=np.arange(len(results));axs[0].barh(positions,[r['test_accuracy'] for r in results.values()],color=['#a1b7c3','#a1b7c3','#167d87','#167d87','#167d87','#d48745','#d48745']);axs[0].set_yticks(positions,list(results));axs[0].set(xlim=(0,1.03),xlabel=t('独立测试准确率','Held-out accuracy'));axs[0].invert_yaxis()
 for key,label,col in [('mean_tree_accuracy',t('单树平均准确率','Mean individual accuracy'),'#d48745'),('forest_accuracy',t('森林准确率','Forest accuracy'),'#167d87'),('error_correlation',t('树错误相关系数','Tree-error correlation'),'#795e86')]:axs[1].plot([d['max_features'] for d in diversity],[d[key] for d in diversity],'o-',label=label,color=col)
 axs[1].set(xlabel=t('每个节点候选特征数','Candidate features per node'),ylabel=t('无量纲','Dimensionless'),xticks=[1,3,9],ylim=(0,1));axs[1].legend();save(fig,'ensemble')
 rf=models['Random forest'];perm=permutation_importance(rf,X[te],y[te],n_repeats=10,random_state=30,scoring='accuracy',n_jobs=1);joint=[]
 for _ in range(10):xp=X[te].copy();order=rng.permutation(len(te));xp[:,[0,8]]=xp[order][:,[0,8]];joint.append(rf.score(X[te],y[te])-rf.score(xp,y[te]))
 oob=np.zeros(len(tr),int)
 for sample in models['Bagging'].estimators_samples_:oob+=~np.isin(np.arange(len(tr)),sample)
 fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');j=np.arange(9);axs[0].bar(j-.2,rf.feature_importances_,.4,label=t('不纯度贡献','Impurity contribution'),color='#167d87');axs[0].bar(j+.2,perm.importances_mean,.4,yerr=perm.importances_std,label=t('测试置换准确率下降','Test permutation accuracy drop'),color='#d48745');axs[0].set(xlabel=t('特征编号（x₈近似复制x₀）','Feature index (x₈ nearly copies x₀)'),ylabel=t('各自定义的无量纲量','Dimensionless, different definitions'),xticks=j);axs[0].legend(fontsize=9)
 axs[1].hist(oob,bins=np.arange(oob.min()-.5,oob.max()+1.5,2),color='#167d87');expected=120*(1-1/len(tr))**len(tr);axs[1].axvline(expected,color='#d48745',ls='--',label=t('理论期望','Expected count'));axs[1].set(xlabel=t('一条训练记录的袋外树数','OOB trees for a training observation'),ylabel=t('训练记录数','Training observations'));axs[1].legend();save(fig,'importance')
 summary={'train_n':len(tr),'test_n':len(te),'features':X.shape[1],'models':results,'pruning_alpha':float(search.best_params_['ccp_alpha']),'full_leaves':int(full.get_n_leaves()),'pruned_leaves':int(pruned.get_n_leaves()),'diversity':diversity,'mean_oob_trees':float(oob.mean()),'expected_oob_trees':expected,'joint_x0_x8_permutation_drop':float(np.mean(joint)),'individual_x0_drop':float(perm.importances_mean[0]),'individual_x8_drop':float(perm.importances_mean[8]),'regression_split_losses':loss,'best_regression_split':float(cuts[np.argmin(loss)]),'best_regression_sse':min(loss)}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,y=y,train=tr,test=te,moon_X=Xm,moon_y=ym,oob_counts=oob,permutation_drops=perm.importances,regression_x=xr,regression_y=yr)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

完成本章后，可以按三个问题组织下一轮实验：规则是否过于细碎，就检查剪枝与叶样本数；树之间是否过于相似，就改变特征采样与数据抽样；解释是否受相关变量影响，就比较单列与成组扰动。每一次改动都对应可读的结构和可计算的结果。树与森林的优势因此不只是一次调用得到较高分数，还在于它们为复杂表格关系提供了许多能够检查的中间环节。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M30.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [scikit-learn — Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

   CART准则、节点约束和剪枝。

   BSD-3-Clause
2. [scikit-learn — Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)

   Bagging、随机森林、Extra Trees与折外Stacking。

   BSD-3-Clause
3. [Breiman (2001), Random Forests](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf)

   树强度、相关性与袋外估计的研究背景。
