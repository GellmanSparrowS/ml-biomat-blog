# 分数可信么：评估、泛化与实验设计

Source: https://ml-biomat.com/tutorials/machine-learning/m03/
Language: zh-CN

从熟悉对象的满分，到罕见事件的零检出，重新设计能回答实际问题的测试。

## 考试成绩，要和将来的工作相对应

一个辨认零件缺陷的模型，在测试图片上得到99%的准确率，看起来已经很可靠。可是，如果同一零件连续拍了六张照片，其中五张进入训练、一张进入测试，模型可能认出了零件表面的独特纹路，而没有学会区分缺陷。将来面对全新的零件，原来的分数便回答不了最重要的问题。模型评估首先要确定“新”究竟意味着什么：同一对象的新记录、新对象、未来时间，还是另一台设备和另一座城市。这比选择一个听起来专业的指标更早一步。

训练集用于确定模型参数，验证集用于选择预处理、算法和参数设置，测试集用于检查已经确定的工作流程。它们的区别不只在文件名，更在于哪些结果能够影响决策。看过测试错误后改了特征，这批测试数据就参与了开发；继续开发完全合理，但后续评估需要新的独立数据。一个清楚的实验设计应能画出信息流：每次拟合看到了哪些观测，每项选择根据什么结果，最后哪一组结果承担整体检验。

本章从两个明确生成的实验展开。第一个给120个对象各生成六条相近记录，并随机给对象分配类别，用来检验记住对象身份怎样抬高分数。第二个生成2400条相互独立的罕见事件记录，用来比较概率、阈值、错误成本与实验不确定性。两组数据承担不同问题，不能把第一组的分组效应和第二组的分类指标混成一个结果。所有生成规则、拆分索引与逐样本输出都包含在完整代码中，便于重新计算。

## 按行、按对象和按时间，实际上在问三个问题

随机切分适合样本近似独立、未来数据来自类似总体的情形。分层随机切分会尽量保留各类别比例，使小类别不至于偶然消失，但它仍然是按行切分。若多行来自同一个人、同一块样品或同一段视频，分层并不会阻止对象信息跨集合流动。分组切分要求整个对象一起进入训练或测试；若实际应用关心新的机构，分组单位还应提升到机构。组的定义应来自预测用途和数据产生过程，而不是哪个切法分数更高。

![左图将前12个对象的六条记录排列在一起，蓝色显示测试行及测试对象的全部行；分组切分让两者一致。右图比较20次拆分的真实测试准确率。](https://ml-biomat.com/static/tutorials/machine-learning/figures/14806b8c1be262ccc0dca74d.svg?v=14806b8c1be2)

图 1左图将前12个对象的六条记录排列在一起，蓝色显示测试行及测试对象的全部行；分组切分让两者一致。右图比较20次拆分的真实测试准确率。

图中的每个对象有八维固定特征，六条记录只添加很小的扰动，类别则独立随机分配给对象。最近邻模型在20次按行随机切分中平均准确率为100%，因为测试记录几乎总能找到同一对象的训练近邻；按对象留出后的平均准确率为44.5%。新对象的类别与特征之间没有设定可学习关系，因此后者围绕机会水平波动，有限对象与有限重复并不要求均值恰好50%。这个对照揭示了两种评估目标的差异：识别熟悉对象与概括到新对象，是两件不同的事。

时间切分把过去用于训练、未来用于评估。预测明天销量时，随机打乱日期会让未来趋势进入训练，得到与实际部署不同的知识条件。滚动评估可以让训练窗口逐渐增长，或保持固定长度以追踪近期状态。若目标包含未来七天的总量，靠近切分边界的样本标签会覆盖相同日期，还需要留出间隔；时间间隔应对应标签窗口和信息延迟。仅仅把日期列删掉，不能消除已经混入其他列的未来信息。

泄漏也会发生在预处理。先用全部数据挑选最相关的特征，再进行交叉验证，验证标签已经影响了特征选择；先计算全体均值进行缺失填补，也让未来样本参与了变换估计。Pipeline把这些需要学习的步骤与模型放在一起，在每个训练折中重新拟合。对于严格已知的物理单位换算，规则可以预先固定；对于由数据估计的尺度、编码和筛选，则应追踪它们各自看到了哪些样本。

## 轮流考试，也需要另一层检验选择过程

K折交叉验证把开发数据分成K份，每次用其中一份验证、其余份训练，轮流得到K个分数。它让不同样本都有机会承担验证角色，并使参数选择不只依赖一次偶然拆分。各折训练集高度重叠，因此这些分数不是K次完全独立的实验；直接用普通独立样本公式给它们计算极窄的置信区间，会夸大精度。交叉验证的主要价值是组织拟合与比较，分数的统计解释仍取决于拆分结构。

如果尝试很多组参数，再报告其中最高的验证分数，就把选择中的幸运波动也计入成绩。Cawley与Talbot在2010年的研究专门分析了这种模型选择过拟合：不仅训练目标会被过度优化，有限数据上的验证准则也会。解决办法是让外层评估整个选择流程，内层负责选参数。每个外层训练集都重新执行内层搜索，再到完全未参与该次选择的外层测试折上评分。嵌套交叉验证因此回答“这套选择方法面对新数据如何表现”，而不是只评价一个事后固定的参数。

本例在1440条训练记录中进行三折内层搜索，比较逻辑回归的四个正则化设置；四折外层评估得到的平均精确率分别约0.134、0.242、0.170、0.217。这些值变化较明显，说明罕见事件与有限样本会让比较不稳定。另有480条验证记录专门选择行动阈值，最后480条测试记录检查固定模型与固定阈值。本章用于阈值和消融实验的逻辑回归事先固定正则化参数C=1；嵌套搜索另外展示完整参数选择流程。两套计算共享训练数据，嵌套搜索的最优模型没有替换阈值实验中的固定模型。因此，外层分数评价参数选择流程，480条测试记录评价这里固定的模型与决策规则。

分组或时间问题的内外层都要延续相应约束，不能只把最外层分好组，内层又让同一对象跨折。若计算预算有限，可以先用较小的预设搜索范围和少量合理模型，再扩大有希望的区域；预算、候选集合和主要指标应在比较前写清。重复查看一个小验证集并不断提出新方案，本质上也在增加搜索规模。保存失败配置和选择规则，能够让最后的结论对应真实完成的实验。

## 指标衡量的，是你愿意怎样计算错误

回归预测一个连续数值。平均绝对误差与目标同单位，容易解释成平均偏离多少；均方根误差也回到原单位，却更重视大偏差。若四次误差为1、1、1、9，平均绝对误差为3，均方根误差约4.58，两者不同来自对最后一次大错误的处理。R平方则把模型平方误差与测试集合内的均值基线比较，可以为负，表示该模型在这组测试数据上不如这一常数基准。接近零的真实值会使百分比误差非常不稳定，选择指标时应考虑数据的零点是否有实际意义。

$$
\operatorname{MAE}=\frac1n\sum_i|y_i-\widehat y_i|,\quad\operatorname{RMSE}=\sqrt{\frac1n\sum_i(y_i-\widehat y_i)^2},\quad R^2=1-\frac{\sum_i(y_i-\widehat y_i)^2}{\sum_i(y_i-\overline y)^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | 测试样本数与样本索引，计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc34a3022c550d4606408025.svg) | 观测、预测与测试观测均值，采用相同的目标单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6db5824810b0dc847a6952b1.svg) | 平均绝对误差与均方根误差，单位与目标相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/12373d1e32275b1b5a25ca4b.svg) | 无量纲相对平方误差指标；式子要求测试目标并非常数。 |

误差1、1、1、9的绝对值平均为3，平方平均为21，因此RMSE=√21≈4.58。若残差平方和12、测试均值基准平方和8，则R²=1−12/8=−0.5。

分类需要区分四类结果。真正例是实际有事件且发出警报；假正例是没有事件却发出警报；假负例是实际有事件却漏掉；真负例是正确保持安静。精确率回答“发出的警报有多少是真的”，召回率回答“实际事件找回了多少”，两者分母不同。F1用调和平均同时关注它们，却没有包含真负例，也没有自动对应某种成本。宏平均让每一类权重相同，微平均把各类计数合并，样本加权平均则遵循类别频率；多分类比较应明确采用哪一种。

$$
\operatorname{precision}=\frac{TP}{TP+FP},\quad\operatorname{recall}=\frac{TP}{TP+FN},\quad F_1=\frac{2TP}{2TP+FP+FN}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c6fbc7d3eeff17e6d411272.svg) | 真正例、假正例、假负例与真负例的样本计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5da11f9b5e39e563d6d0093a.svg) | 精确率、召回率与F1，范围0到1；相应分母为0时需规定处理方式。 |

TP=14、FP=58、FN=17时，精确率14/72≈0.1944，召回率14/31≈0.4516，F1=28/103≈0.2718。72是警报数，31是实际事件数。

排序任务关心有限位置里的有用结果，例如读者只会查看前十条搜索结果。Precision@k查看前k条中相关结果的比例，Recall@k查看找回了所有相关结果中的多少。NDCG让靠前的相关结果贡献更大，并按理想排序归一化：同样找到三条有用结果，把最有用的放在第一位与放在第十位，得分不同。计算之前还需定义哪些候选被检索、哪些相关标签能够观察到；未点击的项目可能从未曝光，直接视为负例会混入展示机制。

$$
\operatorname{DCG}@k=\sum_{r=1}^k\frac{2^{g_r}-1}{\log_2(r+1)},\qquad\operatorname{NDCG}@k=\frac{\operatorname{DCG}@k}{\operatorname{IDCG}@k}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/542032cf3c2e3bf464d7b459.svg) | 考虑的前k个位置与从1开始的位置索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/57b0453fa50cc773dbe10a6f.svg) | 第r个结果的非负分级相关性；本式使用指数增益约定，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cecbf47d4b809626cad8fea7.svg) | 折损累计增益、同一候选标签下的理想最大值及归一结果；IDCG为0时另定无相关结果的协议。 |
| ![Formula](https://ml-biomat.com/static/agent-math/14ae3fefbbf822ee29c5d5c8.svg) | 以2为底的对数，位置越靠后折损越大。 |

相关等级按(0,1)排列，DCG@2=1/log₂3≈0.6309；理想顺序(1,0)的IDCG为1，故NDCG约0.6309。换成理想顺序就得到1。

ROC-AUC和平均精确率AP使用连续分数，考察多个阈值下的排序行为。ROC横轴是假正例占所有负例的比例，负例很多时，较小的比例仍可能对应大量误报；精确率—召回率曲线直接展示警报中真事件所占比例。AP按召回率增加对精确率加权，和把PR曲线用梯形面积积分的数值定义并不完全相同。本例测试集正例比例约6.46%，ROC-AUC约0.763、AP约0.175。它们回答不同问题，不能只因一个数看起来更大就选它报告。

## 93.5%的准确率，为什么一个事件也没找到

第二个实验的480条测试记录中，31条为正例。把所有记录都判为负例，准确率已经达到93.54%。拟合的逻辑回归在默认0.5阈值下恰好也把全部测试记录判为负例，漏掉31次事件；这个结果清楚地说明，默认阈值与当前用途并不匹配。模型仍然给不同记录赋予不同概率，排序具有一定信息，因此可以在验证集上选择更符合行动代价的阈值，而不是把准确率高直接等同于检测有效。

$$
C(t)=c_{FP}FP(t)+c_{FN}FN(t),\qquad t^*=\frac{c_{FP}}{c_{FP}+c_{FN}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/621165602b9172491c95f47c.svg) | 行动阈值与总错误成本；分数≥t判正。成本使用自定成本单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31d949ea1f6e1748f611c952.svg) | 给定阈值下误报与漏报数量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bab89fdc9fbcb80ac2f93ac8.svg) | 每次误报与漏报的正成本，单位为成本/次。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a7778e03e3c5bdd4653d82c.svg) | 校准概率、固定成本和零正确决策成本条件下的理论最优阈值；并非本例验证搜索阈值。 |

误报58、漏报17，成本分别1和10时总成本228。理论阈值为1/11≈0.0909，来自比较行动成本(1−p)cFP与不行动成本pcFN；本例经验验证选择0.14。

![左：480条测试记录的概率分布；中：480条验证记录上的成本曲线与选定阈值0.14；右：测试集精确率—召回率曲线，虚线为正例比例。](https://ml-biomat.com/static/tutorials/machine-learning/figures/733df77ea8e4ef223f5be2a1.svg?v=733df77ea8e4)

图 2左：480条测试记录的概率分布；中：480条验证记录上的成本曲线与选定阈值0.14；右：测试集精确率—召回率曲线，虚线为正例比例。

我们给一次误报计1个成本单位，一次漏报计10个成本单位，在验证集上搜索阈值，得到0.14。将这个阈值固定后用于测试集，得到14次检出、17次漏报和58次误报，总成本为228；默认阈值的成本是310。阈值降低改善了这个具体成本目标，同时需要处理更多警报。读者应该把检出率、警报数量与成本并排看，而不是只保留下降的那个数字。若每个警报都需要人工复核，58次误报还对应明确的工作量。

当概率已校准、错误成本固定、正确决策成本为零时，可以通过比较“采取行动”和“不采取行动”的期望代价得到一个理论阈值。实际模型可能存在校准误差，验证集选择则直接依据观察到的成本曲线。两种路径都需要说明成本来自哪里，以及部署时的事件比例是否变化。若事件比例下降，即使条件识别能力相近，警报中的真事件比例也可能下降。校准、分布变化与阈值更新在可靠性章节会进一步展开。

## 把阈值变成一张成本账本

20条固定记录，颜色表示真实类别；虚线右侧触发警报。单位：概率无量纲、矩阵为记录数、成本为教学成本单位。

[Figure: 分数、混淆矩阵与成本](https://ml-biomat.com/tutorials/machine-learning/m03/#M03-plot)

互动提供20条固定分数与真实标签。移动阈值时，分数没有被重新训练，改变的是哪些记录触发行动；调整漏报成本时，混淆矩阵不变，成本账本改变。把这两种作用分开以后，读者就能辨认“模型变好了”和“同一个模型采用了不同决策规则”之间的区别。没有发出警报时，精确率的分母为零，界面显示未定义；这比强行给出一个漂亮的零或一，更准确地表达当前决策发生了什么。

## 训练很好、验证很差，下一步该补数据还是改模型

学习曲线比较不同训练样本数量下的训练表现与验证表现。若样本很少时训练分数很高，验证分数低，增加样本后两者逐渐靠近，数据可能正在减轻模型对偶然样本的依赖。若两条曲线都停在较低水平，继续收集同类数据的收益可能有限，应检查特征表达、模型形式和标签质量。曲线不是自动诊断书，但它能把“多训练一点试试”转化为更具体的下一步实验。

![1440条开发记录上，逻辑回归与决策树的学习曲线。每个点为三个折的均值，阴影为一个折间标准差；两者使用相同拆分与AP指标。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3cc0c36f1919fdfb63d9d4f3.svg?v=3cc0c36f1919)

图 31440条开发记录上，逻辑回归与决策树的学习曲线。每个点为三个折的均值，阴影为一个折间标准差；两者使用相同拆分与AP指标。

本例比较逻辑回归与未限制深度的决策树，使用相同的三个训练侧验证折，纵轴都是AP。树可以在训练数据上得到很高分数，而验证表现与训练表现之间存在明显距离；逻辑回归的表达方式更受限制，训练分数不会同样接近一。阴影表示三个折之间的一个标准差，展示拆分波动，并不是95%置信区间。随着样本量变化，各折中的正例数量也变化，因此曲线上的起伏需要结合罕见事件样本数理解。

偏差与方差给这种现象提供更系统的语言。对于平方损失，在固定输入位置上，把许多不同训练集得到的预测平均起来，它与真实条件均值之间的偏离形成偏差；各次预测围绕这个平均预测的波动形成方差；观测自身的随机性形成不可约噪声。这个分解依赖损失与随机性定义，不能把一条训练—验证差距直接当成测得的“方差”。更复杂的模型通常降低某些表达偏差，也可能增加对数据的敏感性；正则化、集成和更多数据分别从不同环节改变取舍。

消融实验用来检验一个具体部件的贡献，例如移除一组特征、关闭一种数据增强或换掉一个网络模块。除被考察因素外，拆分、训练预算、指标和选择流程尽量保持一致；必要时为两个方案分别调参，并说明预算如何分配。本例把完整12维输入与只保留前3维的模型比较，重新拟合两个模型，再在相同测试记录上计算逐样本Brier损失差。这个消融检查的是保留特征集合的预测作用，不把某一列的作用解释成因果效应。

## 差多少、稳不稳，和是否过了一条检验线

单次得分由训练样本、测试样本和随机训练过程共同影响。报告均值之前，应明确重复了哪一个环节：只换随机初始化、重新抽训练集，还是重新抽测试对象，它们反映的不确定性不同。本例固定已经拟合的两个模型，对480条测试记录成对重抽样2000次；每次同一组索引同时用于完整模型与删减模型，保留两个预测之间的对应关系。由此得到的是给定这两个拟合模型时，测试样本抽样带来的差异波动。

$$
B=\frac1n\sum_i(p_i-y_i)^2,\qquad\overline d=\frac1n\sum_i\left[(p_i^{\rm reduced}-y_i)^2-(p_i^{\rm full}-y_i)^2\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | 测试记录数与索引；相关对象应成组重抽样。 |
| ![Formula](https://ml-biomat.com/static/agent-math/043e1e9a3c94510bfcdeec48.svg) | 预测正例概率与0/1真实标签，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8d1edb3e2ede488762ecd888.svg) | Brier平均平方概率误差与删减减完整模型的配对平均差，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d9b761f767dac28327d36769.svg) | 使用3个特征和12个特征的两次独立拟合，测试样本一一对应。 |

对真实正例，两个模型概率0.4和0.7，对应损失0.36和0.09，删减减完整为0.27；对真实负例需分别平方其预测概率。配对重抽样保持两个模型使用同一批索引。

![左：固定两个已拟合模型，对测试记录成对重抽样2000次的Brier差；橙线是百分位区间。右：四个明确构造的教学p值与Holm调整，和左侧真实计算分开。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5816fe7441731e58c72f9f6c.svg?v=5816fe744173)

图 4左：固定两个已拟合模型，对测试记录成对重抽样2000次的Brier差；橙线是百分位区间。右：四个明确构造的教学p值与Holm调整，和左侧真实计算分开。

删减模型减完整模型的平均Brier损失差约0.00347，百分位bootstrap区间约为0.000046到0.00715，正值表示完整模型的概率预测损失较小。这是概率质量上的差异。两个模型在0.5阈值下却都没有检出正例，因此分类决定完全一致，配对分类检验没有不一致样本可比较，代码返回p=1。不同指标出现这样的组合并不矛盾：预测概率已经变化，尚未越过固定行动阈值。检验之前必须先明确要比较哪一种结果。

效应量直接描述变化多大，例如每一千条记录减少多少次漏报、平均损失降低多少；置信区间表达指定抽样流程的精度；p值则衡量在给定零假设与检验条件下，观察到当前或更极端统计量的概率。它不是“零假设为真的概率”，也不衡量变化是否值得实际采用。若数据按对象相关，重抽样也应以对象为单位；如果希望涵盖重新训练的不确定性，需要在重复流程中重新拟合，而不是只重排固定预测。

同时检查许多模型、指标和子群体，会增加偶然出现小p值的机会。图中的四个教学p值为0.001、0.018、0.04和0.3，Holm方法排序后按剩余比较数逐步调整，得到0.004、0.054、0.08和0.3。它控制一组检验中至少一次错误拒绝的概率，适合需要控制家族错误率的场景；探索大量候选时，也可以根据目标采用控制错误发现率的方法。先确定主要比较，再把探索结果连同比较范围保存，能让统计判断与研究问题保持一致。

## 为什么有限样本有机会支持对未来的判断

统计学习理论把实践中的担心写成一个问题：训练误差与同分布新样本的平均误差，究竟能相差多少？PAC框架把要求分成两个旋钮，一个是允许多大的误差，另一个是允许多小概率的失败。与Valiant在1984年提出的可学习性研究相联系，这种表达不要求每次抽样都完美，而是讨论在明确条件下，以高概率得到足够准确的规则。计算效率也是可学习性的重要部分；拥有某种存在性保证，并不等于已经有可执行的快速训练算法。

$$
R(h)\le\widehat R_n(h)+\sqrt{\frac{\ln(2|\mathcal H|/\delta)}{2n}}\qquad\text{for all }h\in\mathcal H
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/233c3fbb57e116ed8a26799e.svg) | 一个分类规则、预先固定的有限候选集合与其规则数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/23a91d1904bf8a4deea703bf.svg) | 同分布总体上的期望0/1损失与n个独立同分布样本上的平均0/1损失，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33a17c452e0b6e09211ac3be.svg) | 样本数与0到1之间的失败概率；不等式以至少1−delta的概率对所有候选同时成立。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | 自然对数；该式由有界损失的Hoeffding界与并集界得到。 |

候选数100、n=1000、delta=0.05时，附加项√(ln4000/2000)≈0.0644。一个模型的偏离概率可用集中不等式控制，再把所有候选失败概率相加，便得到对整个搜索集合同时有效的界。

有限候选集合的界展示了三个方向：独立样本越多，训练与真实误差差距的上界越小；候选规则越多，选择偶然好结果的空间越大；要求更高置信度，上界就需要更宽。若候选规则有100条，样本数1000，失败概率0.05，这个界的附加项约0.0644。它通常比实际观察到的差距宽，因为它要同时覆盖所有候选与许多可能的数据分布。这个式子依赖独立同分布和有界损失，不会自动覆盖前面存在对象泄漏的拆分。

连续参数模型拥有无穷多个候选，单纯数规则就失去作用。VC维转而考察一个分类器家族能在多少个精心选择的点上实现所有二元标记方式。实数轴上的单阈值分类器可以打散一个点，却不能打散两个按顺序排列的点的所有标记；平面上的直线可以打散三个不共线点，但无法打散任意四点布局。这个概念描述家族的表达能力，与参数个数相关却不总是相等。它把“模型很灵活”的直觉变成可以分析的数学对象。

理论界与实际评估各自承担工作。界解释样本量、复杂度和置信要求怎样相互制约；分组测试、时间测试、成本曲线与错误分析则检查当前任务中的具体表现。完整实验把这些层次连接起来：先写清新样本是什么，再确定拆分；先确定行动目标，再选指标和阈值；最后用重复与配对比较说明差异的大小和波动。按这个顺序，评估不会只剩一个排行榜上的数字，而会成为选择下一次实验的依据。

### 完整评估实验：拆分、阈值、学习曲线与配对比较

依赖NumPy、SciPy、scikit-learn、Matplotlib。运行python main.py --output results --language zh。生成器、所有拆分、拟合、bootstrap及图像都在代码内；summary.json与experiment_data.npz保留数值。

```
"""Evaluation protocols, thresholds and repeated comparisons on known generators."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split,GroupShuffleSplit,StratifiedKFold,GridSearchCV,cross_val_score,learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,average_precision_score,roc_auc_score,precision_recall_curve,confusion_matrix
from scipy.stats import binomtest

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(33)
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
 # Object identity has no relation to its assigned class, but repeated views reveal identity.
 identities=rng.normal(0,3,(120,8));labels=rng.integers(0,2,120);groups=np.repeat(np.arange(120),6)
 Xg=identities[groups]+rng.normal(0,.12,(720,8));yg=labels[groups];random_scores=[];group_scores=[];split_examples=[]
 for seed in range(20):
  tr,te=train_test_split(np.arange(720),test_size=.25,random_state=seed,stratify=yg)
  gt,ge=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed).split(Xg,yg,groups))
  for dest,a,b in [(random_scores,tr,te),(group_scores,gt,ge)]:
   m=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=1));m.fit(Xg[a],yg[a]);dest.append(accuracy_score(yg[b],m.predict(Xg[b])))
  if seed==0:split_examples=[te,ge]
 fig=plt.figure(figsize=(11,5),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.3,1]);ax=fig.add_subplot(gs[0,0]);matrix=np.zeros((4,72));
 for k,idx in enumerate(split_examples):
  matrix[k*2]=np.isin(np.arange(72),idx);matrix[k*2+1]=np.isin(groups[:72],groups[idx])
 ax.imshow(matrix,aspect='auto',cmap='Blues',vmin=0,vmax=1);ax.set_yticks(range(4),[t('随机：测试行','Random: test rows'),t('随机：测试对象的全部行','Random: rows of test objects'),t('分组：测试行','Grouped: test rows'),t('分组：测试对象的全部行','Grouped: rows of test objects')]);ax.set(xlabel=t('前12个对象，每个6行','First 12 objects, six rows each'));ax.set_xticks(np.arange(2.5,72,6),np.arange(12));
 for x in np.arange(5.5,72,6):ax.axvline(x,color='white',lw=1)
 ax=fig.add_subplot(gs[0,1]);ax.boxplot([random_scores,group_scores],tick_labels=[t('随机行','Random rows'),t('新对象','New objects')],showmeans=True);ax.set(ylim=(0,1.05),ylabel=t('测试准确率','Test accuracy'));ax.grid(axis='y',alpha=.2);save(fig,'splits')
 # A distinct independent-row rare-event classification experiment.
 X,y=make_classification(n_samples=2400,n_features=12,n_informative=5,n_redundant=2,weights=[.94,.06],flip_y=.01,class_sep=1.,random_state=33)
 idx=np.arange(len(y));tr,tmp=train_test_split(idx,test_size=.4,stratify=y,random_state=33);va,te=train_test_split(tmp,test_size=.5,stratify=y[tmp],random_state=33)
 model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000));model.fit(X[tr],y[tr]);pv=model.predict_proba(X[va])[:,1];pt=model.predict_proba(X[te])[:,1]
 thresholds=np.linspace(0,1,201);fn_cost=10
 def counts(a,b,q):tn,fp,fn,tp=confusion_matrix(a,b>=q,labels=[0,1]).ravel();return {'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'cost':int(fp+fn_cost*fn)}
 costs=[counts(y[va],pv,q)['cost'] for q in thresholds];qstar=float(thresholds[np.argmin(costs)]);test_default=counts(y[te],pt,.5);test_selected=counts(y[te],pt,qstar)
 precision,recall,_=precision_recall_curve(y[te],pt)
 fig,axs=plt.subplots(1,3,figsize=(12,3.8),layout='constrained');axs[0].hist([pt[y[te]==0],pt[y[te]==1]],bins=np.linspace(0,1,21),stacked=True,color=['#167d87','#d48745'],label=['0','1']);axs[0].axvline(qstar,color='#523e67',ls='--');axs[0].set(xlabel=t('测试预测概率','Test predicted probability'),ylabel=t('样本数','Observations'));axs[0].legend(title=t('真实类别','True class'))
 axs[1].plot(thresholds,costs,color='#167d87');axs[1].axvline(qstar,color='#d48745',ls='--');axs[1].set(xlabel=t('候选阈值','Candidate threshold'),ylabel=t('验证集成本：FP+10FN','Validation cost: FP+10FN'))
 axs[2].plot(recall,precision,color='#167d87');axs[2].axhline(y[te].mean(),ls='--',color='#9aabb4');axs[2].set(xlabel=t('召回率','Recall'),ylabel=t('精确率','Precision'),xlim=(0,1),ylim=(0,1.02));save(fig,'threshold')
 # Nested tuning estimates the entire selection procedure on training data only.
 inner=StratifiedKFold(3,shuffle=True,random_state=34);outer=StratifiedKFold(4,shuffle=True,random_state=35)
 search=GridSearchCV(make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)),{'logisticregression__C':[.01,.1,1,10]},cv=inner,scoring='average_precision',n_jobs=1)
 nested=cross_val_score(search,X[tr],y[tr],cv=outer,scoring='average_precision');search.fit(X[tr],y[tr])
 sizes=np.array([.15,.3,.5,.75,1]);curves={};fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,(name,est) in zip(axs,[('Logistic',make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))),('Tree',DecisionTreeClassifier(random_state=33))]):
  ns,train,valid=learning_curve(est,X[tr],y[tr],cv=inner,train_sizes=sizes,scoring='average_precision',shuffle=True,random_state=33,n_jobs=1)
  for vals,label,col in [(train,t('训练','Train'),'#d48745'),(valid,t('验证','Validation'),'#167d87')]:
   ax.plot(ns,vals.mean(1),'o-',label=label,color=col);ax.fill_between(ns,vals.mean(1)-vals.std(1),vals.mean(1)+vals.std(1),alpha=.15,color=col)
  ax.set(title=name,xlabel=t('每折训练样本数','Training observations per fold'),ylabel=t('平均精确率 AP','Average precision'),ylim=(0,1.02));ax.legend();curves[name]={'sizes':ns.tolist(),'train':train.tolist(),'validation':valid.tolist()}
 save(fig,'learning')
 # Paired test-object bootstrap, conditional on the fitted models.
 ablated=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000));ablated.fit(X[tr,:3],y[tr]);pa=ablated.predict_proba(X[te,:3])[:,1]
 full_loss=(pt-y[te])**2;abl_loss=(pa-y[te])**2;dif=abl_loss-full_loss;boot=[]
 for _ in range(2000):b=rng.integers(0,len(te),len(te));boot.append(dif[b].mean())
 ci=np.quantile(boot,[.025,.975]);b=int(np.sum((pt>=.5)==y[te]) - np.sum(((pt>=.5)==y[te])&((pa>=.5)==y[te])))
 c=int(np.sum((pa>=.5)==y[te]) - np.sum(((pt>=.5)==y[te])&((pa>=.5)==y[te])))
 pvalue=float(binomtest(b,b+c,.5).pvalue) if b+c else 1.
 rawp=np.array([.001,.018,.04,.3]);order=np.argsort(rawp);adj_sorted=np.maximum.accumulate(rawp[order]*(len(rawp)-np.arange(len(rawp))));holm=np.empty_like(rawp);holm[order]=np.minimum(adj_sorted,1)
 fig,axs=plt.subplots(1,2,figsize=(11,3.8),layout='constrained');axs[0].hist(boot,bins=35,color='#167d87',alpha=.85);axs[0].axvline(0,color='#6a7783',ls='--');axs[0].axvline(ci[0],color='#d48745');axs[0].axvline(ci[1],color='#d48745');axs[0].set(xlabel=t('删减模型−完整模型：Brier差','Reduced minus full model: Brier difference'),ylabel=t('重抽样次数','Bootstrap replicates'))
 axs[1].plot(np.arange(1,5),rawp,'o-',label=t('原始p值（教学示例）','Raw p-values (illustration)'),color='#167d87');axs[1].plot(np.arange(1,5),holm,'s-',label='Holm',color='#d48745');axs[1].axhline(.05,color='#6a7783',ls='--');axs[1].set(xlabel=t('检验编号','Test index'),ylabel='p',xticks=[1,2,3,4],ylim=(0,.35));axs[1].legend();save(fig,'uncertainty')
 summary={'group_random_accuracy_mean':float(np.mean(random_scores)),'group_heldout_accuracy_mean':float(np.mean(group_scores)),'train_n':len(tr),'validation_n':len(va),'test_n':len(te),'test_positive_n':int(y[te].sum()),'threshold':qstar,'default':test_default,'selected':test_selected,'always_negative_accuracy':float(1-y[te].mean()),'test_roc_auc':float(roc_auc_score(y[te],pt)),'test_average_precision':float(average_precision_score(y[te],pt)),'nested_average_precision':nested.tolist(),'best_inner_ap':float(search.best_score_),'brier_difference':float(dif.mean()),'brier_bootstrap95':ci.tolist(),'mcnemar_discordant':[b,c],'mcnemar_exact_p':pvalue,'holm_p':holm.tolist(),'learning_curves':curves}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,y=y,train=tr,validation=va,test=te,probability=pt,ablated_probability=pa,group_X=Xg,group_y=yg,groups=groups,bootstrap=np.array(boot))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [scikit-learn — Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

   分组、分层与时间切分。

   BSD-3-Clause
2. [scikit-learn — Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

   分类、回归与排序指标的精确定义。

   BSD-3-Clause
3. [Cawley & Talbot (2010), Over-fitting in Model Selection](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf)

   模型选择过程自身的过拟合。
4. [MIT — Learnability and VC Dimension](https://gradml.mit.edu/supervised/learnability_and_vc/)

   PAC、有限候选和VC维的推导。
5. [Columbia — Introduction to PAC Learning](https://www.cs.columbia.edu/~aho/cs3261/Lectures/L22-Introduction_to_PAC_Learning.html)

   可学习性的历史问题与计算效率。
