# 用简单模型解释预测：回归、近邻与贝叶斯

Source: https://ml-biomat.com/tutorials/machine-learning/m04/
Language: zh-CN

读懂系数与残差，再为概率、计数和没有完整观察到的寿命选择合适模型。

## 从一个可解释的预测开始

如果一家商店想预测明天的用电量，一个有用的起点是把开门时长、气温和预计客流的贡献相加。它未必立刻得到最准确的预测，却能让人追问：营业时间多一小时，预测会改变多少？哪些天误差特别大？一个特征缺失时，程序究竟填了什么？简单模型的价值正在于此：它们把参数、预测和误差之间的关系放在看得见的位置。先建立这样的起点，再比较更复杂的方法，才能知道新增复杂度解决了哪个问题。

本章先学习连续数值预测，再转向类别与概率。线性回归、岭回归和Lasso共享一条加权求和的主线；逻辑回归把线性分数变成概率；近邻方法向相似样本询问答案；朴素贝叶斯根据各类别产生特征的可能性进行比较。最后，计数和事件发生时间会提醒我们：并不是所有目标都适合普通直线。泊松模型与生存分析分别处理非负计数和观察尚未结束的事件时间。

实验使用明确生成的小数据，以便知道哪些关系是预先设定的。回归数据有十个特征，其中两个高度相关，部分数值被随机遮去；分类数据是带噪声的两个月牙；计数由指数均值生成；部件寿命则与独立观察截止时间结合。每组实验都有不同用途，图中所说的预测改善只针对相应生成规则和拆分。读者可以修改噪声、相关程度和观察时间，检验结论随条件如何变化，而不是把示例的算法顺序当成固定排名。

## 一条线怎样决定自己应该经过哪里

线性回归把预测写成特征的加权和加上偏置。“线性”首先指对参数的依赖形式：即使输入中包含温度平方或两个特征的乘积，只要这些变换先被计算出来，模型仍然可以对它们的系数保持线性。一个系数表示在模型的其他输入保持不变时，相应输入增加一个单位带来的预测变化。这个解释描述模型内部的条件关系；当现实中两个特征总是一起变化时，单独改变其中一个可能离开已有数据覆盖的范围。

$$
\widehat y_i=b+\sum_{j=1}^p w_jx_{ij},\qquad r_i=y_i-\widehat y_i,\qquad\min_{b,\mathbf w}\sum_{i=1}^n r_i^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dbf1dc27226e2761db070ccb.svg) | 训练样本数、特征数与相应索引，无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29313d2a94e65ab63aa973ae.svg) | 第i个样本的第j个特征及权重；权重单位为响应单位/该特征单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e6ed5d7ae8fdea0b1ed63fdc.svg) | 观测、预测、截距与残差，均采用响应单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1e6e60d2bfa1e755c04f563b.svg) | p维权重向量，以及选择使平方残差总和最小的参数。 |

观测(2,4,6)若只拟合常数，预测均值4，残差(−2,0,2)，平方和8。常数改成3，平方和变为1+1+9=11；均值是这一问题的最小二乘解。

残差是观测减预测，它在散点图中表现为点到拟合线的竖直距离。最小二乘把每个残差平方后相加，寻找使总和最小的系数。平方防止正负误差抵消，同时使较大的误差承担更高代价。对于一个常数预测，最小二乘得到样本均值；对于一条直线，它在斜率和截距之间寻找共同最优位置。几何上，可以把所有观测组成一个长向量，拟合则是在特征列所张成的空间里寻找最接近它的投影。

使用平方误差并不要求每一组数据都严格服从高斯分布。把最小二乘进一步解释为某个概率模型的最大似然时，才需要说明独立高斯噪声等条件。若噪声方差随输入变化，均值关系仍然可以用线性模型描述，但系数标准误差与区间的计算需要相应处理。离群点会因平方而产生较大影响，因此拟合后要看残差图和原始记录，确定大误差来自真实的特殊情形、测量问题还是模型遗漏了结构。

![90个相同测试样本，三条完整预处理—回归流程的残差。横纵轴使用生成响应单位，色标为未遮挡的原始特征x₀；零线帮助观察系统偏差。](https://ml-biomat.com/static/tutorials/machine-learning/figures/ff3290b1c9ff49dca42b650f.svg?v=ff3290b1c9ff)

图 190个相同测试样本，三条完整预处理—回归流程的残差。横纵轴使用生成响应单位，色标为未遮挡的原始特征x₀；零线帮助观察系统偏差。

本例300条记录中210条用于训练，90条用于测试。生成均值为20加上三个有效特征的线性贡献，另有标准差1.4的独立高斯噪声；十列中随机遮去147个数值。普通最小二乘、岭回归和Lasso的测试RMSE分别约1.439、1.414和1.386。图中横轴是预测，纵轴是残差，颜色显示第一个原始特征。如果残差随预测呈曲线，说明均值关系可能遗漏非线性；如果像喇叭一样展开，说明波动随输入变化。一个总误差数值无法代替这些结构信息。

## 让相似的解释少一些相互争抢

当两列特征几乎相同，很多系数组合都能得到相近的预测。例如两支温度计读数接近，把第一支的系数增加一点、第二支减少一点，总预测几乎不变。于是数据的轻微扰动就可能让系数大幅变化。岭回归给系数平方和增加惩罚，让过大的相互抵消变得昂贵，倾向于用较平缓的组合分担贡献。它通常不会把系数精确压到零，而是连续收缩它们，改善某些病态或高方差问题中的稳定性。

$$
J_{\rm Ridge}=\sum_i r_i^2+\alpha_R\sum_j w_j^2,\qquad J_{\rm Lasso}=\frac1{2n}\sum_i r_i^2+\alpha_L\sum_j|w_j|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/479702a85ff3aefeab1ac2f7.svg) | 本章scikit-learn两种回归的目标约定；截距不受惩罚，目标单位均为响应单位平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/864236b792cc24b490570b22.svg) | 沿用残差、权重、样本数及索引；此处特征已标准化，权重使用响应单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e6bedf18d4ad0c1bae9a982.svg) | 非负惩罚强度；此尺度下alpha_R无量纲，alpha_L具有响应单位，二者数值不直接比较。 |

若平方残差和10、n=5、w=(2,−1)，岭alpha_R=1时目标10+5=15；Lasso alpha_L=1时目标10/10+3=4。两目标缩放不同，不能仅比较15和4决定优劣。

Lasso把惩罚改成系数绝对值之和，使一部分系数可以恰好变为零。Tibshirani在1996年的论文中把收缩与变量选择放进同一个问题：模型既要保留有用的拟合能力，也要形成更紧凑的表示。理解零系数时，应看到它取决于特征集合、缩放与惩罚强度。高度相关的一组变量中，某一个被选中而另一个变成零，并不证明后者在现实中没有作用；它可能只是提供了非常相近的信息。

![使用未遮挡训练特征计算的系数路径，与图1的缺失数据评价相区分。每条线对应一列特征，两个模型alpha的误差缩放约定不同。](https://ml-biomat.com/static/tutorials/machine-learning/figures/7e4028d6a57da495507166e2.svg?v=7e4028d6a57d)

图 2使用未遮挡训练特征计算的系数路径，与图1的缺失数据评价相区分。每条线对应一列特征，两个模型alpha的误差缩放约定不同。

图中每条曲线是一列特征的系数，横轴增加惩罚强度。为清楚观察相关特征，系数路径使用训练样本中未遮挡的十列生成值，而前一幅测试残差图使用实际遮挡后的数据与缺失处理流程；二者用途明确区分。岭惩罚抑制的是系数向量整体的L2范数；当两列特征高度相关时，解释同一部分响应的权重会在它们之间重新分配，所以某个系数可以先增大再减小，图中的x₀就显示了这种变化。Lasso路径还会出现精确的零。两个软件模型对平方误差采用不同缩放约定，因此同样的alpha数字不表示相同惩罚强度，图的横轴用于理解各自变化，不能逐点比较数字大小。

正式比较中的缺失指示列使输入从十列增加到二十列。训练侧五折验证选择岭alpha=10、Lasso alpha=0.1；Lasso保留七个非零系数，其中包含三个缺失指示项。这些指示项在当前随机缺失生成器中没有设定真实预测作用，非零值反映有限样本拟合与所选惩罚的结果。把“被模型选中”与“已发现机制”分开，才能正确使用稀疏模型。若需要解释稳定性，可重复拆分，记录每列被选择的频率，而不是只展示一次漂亮的稀疏系数表。

## 模型前面的步骤，也是需要学习的一部分

特征工程把原始记录变成更适合问题的输入。对于一年中的日期，直接使用1到365会使年末与年初相距很远；正弦和余弦编码可以表达周期。对于类别名称，随意赋予1、2、3会引入不存在的距离或顺序，独热编码更适合无序类别。对于温度与湿度共同影响的过程，交互项能够让一个特征的作用随另一个变化。每一种变换都加入了结构假设，因此应从问题和观测机制出发，再通过训练侧比较检验。

缺失值不等于零。若传感器没有读数，把它填成零可能制造一场从未发生的低温事件。本例使用训练中位数填补，再增加“原来是否缺失”的指示列，让模型区分实际接近中位数与因为没有观测而被填成中位数。中位数是一个具体基线，它没有恢复丢失的测量值；若缺失依赖设备状态或目标，缺失机制本身也值得建模。测试中出现训练未见的新缺失类型时，应检查预处理对列数与类别的处理是否一致。

Pipeline把填补、缩放和拟合绑定成一个对象。交叉验证每次只在训练折估计中位数、均值与标准差，再变换验证折，避免未来信息影响预处理。对岭回归和Lasso，缩放尤其重要，因为惩罚直接作用于系数：输入换一个单位，表示同一作用所需的系数大小也改变；未缩放时，这可能使某些列获得意外的惩罚优势。对近邻方法，缩放则改变距离，因此会直接改变哪些样本被当作邻居。

如果要把标准化模型的系数换回原单位，可以用标准化系数除以训练标准差，并相应调整截距。转换后的预测应与原Pipeline逐条一致，这是一个很好的复核。包含交互、多项式或缺失指示时，每个系数的对象也应写清：它可能对应“温度平方”或“温度缺失”，并不是原始温度本身。解释模型之前先生成最终特征名称，比只打印一串浮点数更能避免误读。

## 从连续分数到类别概率

把普通线性回归直接用于0/1标签，预测可能小于零或大于一。逻辑回归保留线性分数，却用S形函数把它映射到零和一之间。分数为零时概率为0.5，分数很大时概率接近一，很小时接近零。它优化的是伯努利概率模型的对数损失，因此名称里虽然有“回归”，常见用途却是分类。模型输出概率以后，行动阈值仍需根据任务设置；默认0.5只是一种特定选择。

$$
z=b+\mathbf w^\top\mathbf x,\quad p=\frac1{1+e^{-z}},\quad\log\frac p{1-p}=z,\quad\ell=-y\log p-(1-y)\log(1-p)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6645a980453d409ae0c7963.svg) | 输入特征向量、同维权重、偏置与线性分数；此式中分数无量纲，权重单位相应抵消输入单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/537df2def454b5181de4f6e6.svg) | 正类概率与0/1标签；p在0到1之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d733275f6c334d150d24653e.svg) | 单样本伯努利负对数似然、自然指数底数与自然对数；损失以nat表示。 |

z=0时p=0.5；z=ln3时p=0.75，几率为3。若y=1，损失−ln0.75≈0.2877；若y=0，同样的预测损失−ln0.25≈1.3863。

逻辑回归的线性关系发生在对数几率上。几率是事件概率除以不发生概率；一个系数增加一单位输入时，几率会乘上该系数的指数，而不是让概率始终增加同样多。接近0.5时，S形曲线比较陡，同样的分数变化造成较大概率变化；接近0或1时，变化较缓。多分类可以使用softmax把多个分数一起归一化，输出所有类别的概率。类别之间的相对分数，而不是某个分数的绝对零点，决定概率。

![相同两个月牙生成器与拆分；背景为实际模型的正类概率，实线为0.5边界，点为180个测试观测。kNN边界较灵活，但其有限投票概率需要另行评价。](https://ml-biomat.com/static/tutorials/machine-learning/figures/9d3fc23bda0cf438288ca8e1.svg?v=9d3fc23bda0c)

图 3相同两个月牙生成器与拆分；背景为实际模型的正类概率，实线为0.5边界，点为180个测试观测。kNN边界较灵活，但其有限投票概率需要另行评价。

图中使用相同420个训练点和180个测试点比较三种分类器。两个月牙的关系是非线性的，普通逻辑回归只能给出线性分界，本次测试准确率为86.67%。这不说明所有线性模型都会失败：加入合适的非线性特征，可以让线性参数模型表达弯曲边界；也可以使用核方法或神经网络自动组织更丰富的表示。关键是分清“线性参数”与“原始坐标里的直线”，并把新增特征的选择放在训练侧进行。

概率输出还要检查校准：报告0.8的样本，长期来看是否约有80%为正例？逻辑回归使用概率损失，常能提供有用的概率起点，但特征遗漏、正则化、抽样比例与分布变化都会影响校准。分类准确率只关心阈值或最大类别，而对数损失会惩罚自信错误。接下来近邻方法的结果正好说明这两种评价为什么可以给出不同排序。

## 询问邻居，或者比较每一类怎样产生特征

k近邻先保存训练样本，预测新点时找到距离最近的k个邻居，再由他们投票或平均。分类输出可以用邻居中的类别比例表示，回归则平均邻居目标。k小的时候能追随局部结构，也更容易受一个噪声点影响；k大时更平滑，却可能跨过不同群体的边界。距离加权让更近的样本贡献更大，但距离本身仍需要有意义。在高维空间里，很多无关维度会共同影响距离，因此特征选择、缩放和降维会显著改变近邻。

本例选择k=15，测试准确率达到93.89%，高于普通逻辑回归；对数损失却约0.719，差于逻辑回归的0.286。原因之一是有限邻居投票会给出精确的0或1概率，一旦这些自信判断出错，对数惩罚非常大。库在计算时使用数值裁剪来保持有限结果。这个实验提示：想获得更多正确类别，可以检查近邻；想把概率用于风险或成本计算，还应检查平滑、校准和验证结果。准确率的改善与概率质量的改善需要分别检验。

$$
P(Y=c\mid\mathbf x)=\frac{\pi_c\prod_{j=1}^p q_j(x_j\mid c)}{\sum_{a=1}^{K}\pi_a\prod_{j=1}^p q_j(x_j\mid a)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f7fab13bb77748ab95824423.svg) | 类别随机变量、候选类别、归一化求和类别与总类别数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9de4251bb30f6f1c6ecb6e56.svg) | 特征向量、其第j项、特征数与特征索引；此处p是维度，不是上一式的概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce006fb0b9eacb74e0eab1c1.svg) | 类别先验概率与给定类别的单特征概率或密度；连续密度具有特征单位的倒数，归一化后消去。 |
| ![Formula](https://ml-biomat.com/static/agent-math/40622fb44b3838693d5fff08.svg) | 给定特征后的类别概率，无量纲；乘积来自条件独立假设。 |

两类先验各0.5。某两个二值特征在类1下出现概率0.8、0.6，在类0下为0.2、0.3，则未归一分数0.24与0.03，类1后验为0.24/0.27≈0.8889。

朴素贝叶斯采取另一条路线：先估计每类有多常见，再估计在该类别下各个特征出现的可能性，把这些证据结合起来比较类别。它的“朴素”假设是给定类别后，各特征条件独立，这使高维联合分布变成许多一维分布的乘积。GaussianNB为连续特征使用类内高斯分布；MultinomialNB常用于非负词计数；BernoulliNB适合有无某特征的二值记录。输入分布与模型假设相配，比函数名称是否熟悉更重要。

给两个高度相关的词分别计入证据，朴素贝叶斯可能把相近信息重复计算，从而形成过于自信的概率；类别判断有时仍然不错。文本计数中还需要平滑，避免某个类别在训练中没见过一个词，就把整篇文档的似然乘成零。图中的GaussianNB在月牙数据上得到86.67%的准确率、约0.298的对数损失。月牙并不满足类内独立高斯形状，因此这幅比较同时展示了模型假设怎样成为边界形状。

## 目标是计数时，均值也需要合适的形状

一天到店人数是非负整数，机器每小时的故障次数也是计数。普通线性预测可能给出负均值，而广义线性模型把三个部分分开：响应服从哪种分布，输入如何形成线性预测子，以及通过什么连接函数把均值与预测子联系起来。普通高斯线性回归使用恒等连接，伯努利逻辑回归使用logit连接，泊松回归常使用对数连接。改变响应类型，不必放弃线性组合的清楚结构。

$$
Y\mid x\sim\operatorname{Poisson}(\mu),\qquad\log\mu=\beta_0+\beta_1x,\qquad\mu=e^{\beta_0+\beta_1x}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae046271dd751e178814d5e7.svg) | 每个固定观察窗的非负整数计数，以及无量纲输入。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 条件平均计数，严格为正；此处计数视为无量纲数量，观察窗固定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/134310dd50a86cb19a5b5082.svg) | 对数均值的截距与斜率；本例输入无量纲，二者无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c1afb732f9f6f9c82d604b05.svg) | 按指定泊松分布产生观测；给定输入时方差也等于mu。 |

beta0=0.5、beta1=0.8时，x=0给出均值exp0.5≈1.649；x增加1，均值乘exp0.8≈2.226。每一条实际计数仍是整数，平均值可以不是整数。

![等长观察窗中的泊松计数：测试点、已知生成均值、泊松GLM和OLS预测。响应为每窗计数，输入无量纲；所有曲线使用相同输入范围。](https://ml-biomat.com/static/tutorials/machine-learning/figures/eede639630cf5628226ac32a.svg?v=eede639630cf)

图 4等长观察窗中的泊松计数：测试点、已知生成均值、泊松GLM和OLS预测。响应为每窗计数，输入无量纲；所有曲线使用相同输入范围。

本例400个输入对应等长观察窗，生成的平均计数为exp(0.5+0.8x)，再从泊松分布抽取实际计数。训练300条后，模型估计截距约0.449、斜率约0.757；它们接近生成值但不完全相等，因为样本有限且计数有波动。图中把测试计数、真实均值、泊松预测和普通直线放在一起，能够看到正均值与曲线形状怎样影响拟合。泊松模型在给定输入下把方差设为均值，若实际波动远大于均值，应检查遗漏因素、过度离散或考虑更合适的分布。

观察时长不同的计数不能直接公平比较。记录两小时的故障数自然可能多于记录半小时的故障数，即使单位时间风险相同。可以通过暴露量处理，把期望计数写成观察时长乘单位时间率；在对数连接里，观察时长的对数作为已知偏置项进入。实现时要区分“把时长当作自由特征”和“按理论固定暴露量系数为一”，两者表达的模型不同。本例统一观察窗长度，正是为了先隔离连接函数的作用。

## 还没看到故障，提供了什么信息

测试80个部件的寿命时，有些在观察结束前损坏，有些仍在运行。后者的寿命不是零，也不是等于观察时长，更不是永远不会损坏；我们知道的只是它至少活到了某个时刻。这叫右删失。每个样本因此需要两个字段：实际观察到的持续时间，以及该时刻是否真的发生事件。把删失样本直接删掉，会过度保留较早发生的事件；把观察截止时间当故障时间，又会人为制造一批过早故障。

Kaplan与Meier在1958年研究的不完整观察问题，正是怎样在这种情况下估计“到某个时间仍未发生事件”的比例。乘积极限估计在每个事件时刻查看风险集：当时仍在观察、且此前没有事件的样本有多少，其中发生事件的有多少。先算这一小步的存活比例，再把各步乘起来。删失不会让曲线当场下降，但会让它离开后续风险集。这种逐步更新能把一个看似抽象的生存函数拆成一张可以手算的账表。

$$
\widehat S(t)=\prod_{t_j\le t}\left(1-\frac{d_j}{n_j}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/00cba27d47f7255c4c5fcff0.svg) | 到时刻t仍未发生事件的估计概率；t以小时表示，概率无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7de582841847008ad5e72738.svg) | 不同事件时刻与其索引，只在发生事件时引入乘积因子。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9eb35de5f12a2aa16d422828.svg) | 时刻t_j的事件数与该时刻之前仍在风险集的观察数；采用计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eddaa20e15661440b4bf8d78.svg) | 把各事件时刻的条件存活比例相乘；依赖合适的独立删失条件。 |

四个观察终点2、3、4、5小时，3小时为删失，其余为事件。2小时因子3/4；3小时不下降但移走一个风险对象；4小时因子1/2，累计3/8；5小时最后事件使生存估计降为0。

![左侧为前12个部件的实际观察时间线；圆点为故障，竖线为删失。右侧80个部件的Kaplan–Meier曲线与平均寿命10小时的生成关系对照，短竖线标记删失。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b8cd0f9fa69b5338c487889c.svg?v=b8cd0f9fa69b)

图 5左侧为前12个部件的实际观察时间线；圆点为故障，竖线为删失。右侧80个部件的Kaplan–Meier曲线与平均寿命10小时的生成关系对照，短竖线标记删失。

图中寿命由平均10小时的指数分布生成，观察截止时间独立地在2到18小时之间均匀抽取。实际得到50次事件和30次删失，左侧显示前12个部件的时间线，右侧把估计生存曲线与真实生成曲线比较。独立删失使仍被观察的风险集能够代表相应时间的目标人群；如果越接近故障的设备越容易失去记录，删失机制会改变这种代表性，需要根据设备状态建模或重新设计记录方式。

生存概率是“到时刻t还未发生事件”的概率，危险率则描述已经活到t的条件下，接下来极短时间发生事件的速率，单位是时间的倒数。危险率不是某个时间点的发生概率。若要同时使用温度、负载等特征，可以进一步学习Cox比例风险模型或加速失效时间模型：前者比较危险率的倍数关系，后者描述时间尺度怎样被拉长或缩短。使用时需检查比例风险或相应分布假设，并按时间窗评价预测，而不是把删失数据直接交给普通回归。

## 亲手维护一个风险集

勾选表示事件，取消表示删失。四个部件从0小时开始观察；风险集计数与生存曲线同步更新。

[Figure: 风险集与生存概率](https://ml-biomat.com/tutorials/machine-learning/m04/#M04-plot)

| 时间（小时） | 风险集 | 事件数 | 生存概率 |
| --- | --- | --- | --- |

互动把四个部件的观察时间固定为2、3、4、5小时，你可以改变每个终点是事件还是删失，观察风险集、每步存活比例和最终曲线一起变化。默认第3小时为删失时，第2小时从四个样本中发生一次事件，存活比例变成3/4；第4小时风险集只剩两个，再发生一次事件，累计存活变成3/8。这个过程让“没有完整寿命也能提供信息”成为可检查的计算，而不是一句需要背下来的定义。

## 用预测问题选择起点，再读懂它为什么出错

对于连续响应，可以先用线性回归建立系数与残差的基线，再根据相关性、维度和稳定性比较岭与Lasso；对于分类，可以用逻辑回归检查线性分数，用近邻检查局部几何，用朴素贝叶斯检查简化的类内生成假设。计数和带删失的时间则要求先改变目标模型。这些选择不是从简单到高级的一条排行榜，而是把不同假设放到同一问题里接受检验。最合适的起点应当让你容易发现下一步需要改什么。

### 完整例子：六类基础模型与删失计算

依赖NumPy、Matplotlib、scikit-learn。运行python main.py --output results --language zh。所有生成规则、Pipeline、训练侧搜索、测试结果和五组图在同一脚本内；KM另有四点手算数据。

```
"""Interpretable baseline models and explicit censoring on seeded teaching data."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split,GridSearchCV,KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression,Ridge,Lasso,LogisticRegression,PoissonRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error,accuracy_score,log_loss

def kaplan_meier(duration,event):
 times=np.unique(duration[event]);survival=1.;ys=[];risk=[];deaths=[]
 for tm in times:
  n=int(np.sum(duration>=tm));d=int(np.sum((duration==tm)&event));survival*=1-d/n;ys.append(survival);risk.append(n);deaths.append(d)
 return np.r_[0,times],np.r_[1,ys],risk,deaths

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(44);zh=language=='zh'
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
 # Regression: a known mean relation with correlated measurements and missing values.
 X=rng.normal(size=(300,10));X[:,1]=X[:,0]+rng.normal(0,.08,300);truth=np.array([2.,0.,-1.5,1.,0.,0.,0.,0.,0.,0.]);y=20+X@truth+rng.normal(0,1.4,300)
 missing=rng.random(X.shape)<.06;Xm=X.copy();Xm[missing]=np.nan;tr,te=train_test_split(np.arange(300),test_size=.3,random_state=44)
 cv=KFold(5,shuffle=True,random_state=44);results={};fits={}
 for name,est,grid in [('OLS',LinearRegression(),None),('Ridge',Ridge(),{'ridge__alpha':[.01,.1,1,10,100]}),('Lasso',Lasso(max_iter=10000),{'lasso__alpha':[.001,.01,.05,.1,.3]})]:
  pipe=make_pipeline(SimpleImputer(strategy='median',add_indicator=True),StandardScaler(),est)
  fitted=GridSearchCV(pipe,grid,cv=cv,scoring='neg_mean_squared_error') if grid else pipe;fitted.fit(Xm[tr],y[tr]);pred=fitted.predict(Xm[te]);best=fitted.best_estimator_ if grid else fitted
  results[name]={'test_rmse':float(np.sqrt(mean_squared_error(y[te],pred))),'selected':fitted.best_params_ if grid else {},'coefficients':best[-1].coef_.tolist(),'nonzero_coefficients':int(np.sum(np.abs(best[-1].coef_)>1e-9))};fits[name]=(best,pred)
 fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
 for ax,(name,(m,pred)) in zip(axs,fits.items()):
  ax.scatter(pred,y[te]-pred,c=X[te,0],cmap='viridis',s=19,alpha=.8);ax.axhline(0,color='#d48745');ax.set(title=f'{name}: RMSE={results[name]["test_rmse"]:.3f}',xlabel=t('预测响应','Predicted response'),ylabel=t('观测−预测','Observed minus predicted'));ax.set_ylim(-5.5,5.5)
 fig.colorbar(axs[0].collections[0],ax=axs,shrink=.8,label=t('特征x₀（无量纲）','Feature x₀ (dimensionless)'));save(fig,'residuals')
 clean=StandardScaler().fit_transform(X[tr]);alphas=np.logspace(-3,2,60);paths={};fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,(name,cls) in zip(axs,[('Ridge',Ridge),('Lasso',Lasso)]):
  coefs=np.array([cls(alpha=a,max_iter=10000).fit(clean,y[tr]).coef_ for a in alphas]);paths[name]=coefs
  for j in range(10):ax.semilogx(alphas,coefs[:,j],label=f'x{j}',lw=2 if j<4 else .8,alpha=1 if j<4 else .5)
  ax.set(title=name,xlabel=t('惩罚参数 alpha（各模型约定不同）','Penalty alpha (model conventions differ)'),ylabel=t('标准化特征的系数','Coefficient of standardized feature'));ax.axhline(0,color='#b0c2cb',lw=.7)
 axs[1].legend(ncol=2,fontsize=9);save(fig,'regularization')
 # Identical held-out moon observations for three basic classifiers.
 Xc,yc=make_moons(n_samples=600,noise=.25,random_state=44);ct,ce=train_test_split(np.arange(600),test_size=.3,stratify=yc,random_state=44)
 gx,gy=np.meshgrid(np.linspace(-1.8,2.8,230),np.linspace(-1.3,1.9,160));grid=np.c_[gx.ravel(),gy.ravel()];class_results={};fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
 for ax,(name,clf) in zip(axs,[('Logistic',LogisticRegression()),('kNN k=15',KNeighborsClassifier(n_neighbors=15)),('Gaussian NB',GaussianNB())]):
  pipe=make_pipeline(StandardScaler(),clf);pipe.fit(Xc[ct],yc[ct]);prob=pipe.predict_proba(Xc[ce])[:,1];field=pipe.predict_proba(grid)[:,1].reshape(gx.shape);ax.contourf(gx,gy,field,levels=np.linspace(0,1,11),cmap='RdBu_r',alpha=.6);ax.contour(gx,gy,field,levels=[.5],colors='#243b49',linewidths=1.2);ax.scatter(*Xc[ce].T,c=yc[ce],cmap='RdBu_r',edgecolor='white',linewidths=.4,s=17);ax.set(title=name,xlabel='x₀',ylabel='x₁');class_results[name]={'accuracy':float(accuracy_score(yc[ce],prob>=.5)),'log_loss':float(log_loss(yc[ce],np.c_[1-prob,prob]))}
 fig.colorbar(axs[0].collections[0],ax=axs,shrink=.8,label=t('正类预测概率','Predicted positive probability'));save(fig,'classification')
 # Poisson response: expected count exp(0.5+0.8*x), one equal exposure unit each.
 xp=rng.uniform(-2,2,400);mu=np.exp(.5+.8*xp);yp=rng.poisson(mu);pr,pe=train_test_split(np.arange(400),test_size=.25,random_state=44)
 pm=PoissonRegressor(alpha=0,max_iter=1000).fit(xp[pr,None],yp[pr]);lm=LinearRegression().fit(xp[pr,None],yp[pr]);xx=np.linspace(-2,2,250)
 fig,ax=plt.subplots(figsize=(8,4),layout='constrained');ax.scatter(xp[pe],yp[pe],alpha=.5,s=20,color='#536e80',label=t('测试计数','Test counts'));ax.plot(xx,np.exp(.5+.8*xx),'--',color='#111827',label=t('生成均值','Generating mean'));ax.plot(xx,pm.predict(xx[:,None]),color='#167d87',lw=2,label='Poisson GLM');ax.plot(xx,lm.predict(xx[:,None]),color='#d48745',label='OLS');ax.set(xlabel=t('无量纲输入','Dimensionless input'),ylabel=t('每个等长观察窗的计数','Count per equal observation window'));ax.legend();save(fig,'poisson')
 # Independent right censoring of exponential lifetimes, time unit: hours.
 lifetime=rng.exponential(10,80);censor=rng.uniform(2,18,80);duration=np.minimum(lifetime,censor);event=lifetime<=censor;tm,surv,risk,deaths=kaplan_meier(duration,event);truegrid=np.linspace(0,20,200)
 fig=plt.figure(figsize=(11,4.5),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1,1.25]);ax=fig.add_subplot(gs[0,0]);
 for i in range(12):ax.plot([0,duration[i]],[i,i],color='#96aeb8');ax.scatter(duration[i],i,marker='o' if event[i] else '|',s=60,color='#d48745' if event[i] else '#167d87')
 ax.set(xlabel=t('观察时间（小时）','Observed time (hours)'),ylabel=t('前12个部件','First 12 components'),title=t('圆点：事件；竖线：删失','Circle: event; tick: censoring'));ax=fig.add_subplot(gs[0,1]);ax.step(np.r_[tm,duration.max()],np.r_[surv,surv[-1]],where='post',color='#167d87',lw=2,label='Kaplan–Meier');ax.plot(truegrid,np.exp(-truegrid/10),'--',color='#34495e',label=t('生成生存函数','Generating survival'))
 censor_surv=np.array([surv[np.searchsorted(tm,d,side='right')-1] for d in duration[~event]]);ax.scatter(duration[~event],censor_surv,marker='|',color='#167d87',label=t('删失','Censored'));ax.set(xlabel=t('时间（小时）','Time (hours)'),ylabel=t('生存概率 S(t)','Survival probability S(t)'),ylim=(0,1.03));ax.legend();save(fig,'survival')
 hand_t=np.array([2.,3.,4.,5.]);hand_e=np.array([1,0,1,1],dtype=bool);ht,hs,_,_=kaplan_meier(hand_t,hand_e)
 summary={'regression_train':len(tr),'regression_test':len(te),'regression':results,'missing_cells':int(missing.sum()),'classification_train':len(ct),'classification_test':len(ce),'classification':class_results,'poisson_intercept':float(pm.intercept_),'poisson_slope':float(pm.coef_[0]),'survival_n':len(duration),'events':int(event.sum()),'censored':int((~event).sum()),'km_hand_times':ht.tolist(),'km_hand_survival':hs.tolist()}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,X_missing=Xm,y=y,train=tr,test=te,X_class=Xc,y_class=yc,class_train=ct,class_test=ce,lifetime=lifetime,censor=censor,duration=duration,event=event,poisson_x=xp,poisson_y=yp)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

完整代码把生成器、缺失处理、交叉验证、预测和画图放在同一个可运行例子中。可以先增加两个特征的相关程度，观察系数路径是否更不稳定；再增大月牙噪声，比较分类准确率与对数损失是否同向变化；最后缩短观察截止时间，看看删失增多怎样改变生存曲线尾部。每次只改一个主要因素，保留原拆分与随机种子，结果便能围绕明确的问题展开，而不是变成不断更换模型名字的试错。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [scikit-learn — Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)

   最小二乘、正则化、逻辑回归与GLM。

   BSD-3-Clause
2. [scikit-learn — Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)

   邻居、度量与维度影响。

   BSD-3-Clause
3. [scikit-learn — Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

   条件独立与不同特征分布。

   BSD-3-Clause
4. [Tibshirani (1996), Regression Shrinkage and Selection via the Lasso](https://www2.stat.duke.edu/courses/Spring06/sta395/tibshirani.pdf)

   收缩与变量选择的原始研究。
5. [Kaplan & Meier (1958), Nonparametric Estimation from Incomplete Observations](https://web.stanford.edu/~lutian/coursepdf/KMpaper.pdf)

   不完整观察与乘积极限估计。
