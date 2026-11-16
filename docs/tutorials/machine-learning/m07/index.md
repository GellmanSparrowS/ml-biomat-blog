# 让证据更新认识：贝叶斯、隐变量与高斯过程

Source: https://ml-biomat.com/tutorials/machine-learning/m07/
Language: zh-CN

从七次成功的手算后验，走到层次共享、消息传递与可检查的计算近似。

## 七次成功以后，知道了多少

一家新店接待了十位顾客，其中七位购买了商品。把购买率写成70%很容易，但如果下一天再来十人，会不会仍有七人购买？如果另一家店接待一千人、有七百人购买，两家店的70%是否同样可靠？这些问题要求模型同时表达估计值与证据多少。贝叶斯推断把尚未确定的成功率视为一个需要描述的不确定量，先写出可能范围，再让实际观测改变不同取值受到的支持。

先验表达观察这批数据之前对参数的认识；似然描述参数取某个值时，出现当前数据有多容易；后验把两者结合，得到看过数据后的分布。Bayes于1763年发表的遗稿由Price介绍，讨论由事件发生情况推断其未知机会的问题。今天的模型已经远超最初场景，但“从结果反推产生结果的概率机制”仍然是理解入口。更新并不是凭空增加确定性，而是把已有假设与新证据的关系算清楚。

$$
p(\theta\mid D)=\frac{p(D\mid\theta)p(\theta)}{p(D)},\qquad p(D)=\int p(D\mid\theta)p(\theta)\,d\theta
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f0f92154fe22663cdf94a902.svg) | 已观察的数据和未知参数；本节theta为无量纲成功概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e28cb8f34e18057679d10fca.svg) | 先验密度、似然和后验密度；密度单位由参数/观测单位决定，似然作为theta的函数无需对theta积分为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/10ef1a90ef491e62d41ffc76.svg) | 证据、对全部参数取值的积分及积分变量；离散参数用求和代替积分。 |

两候选theta=0.5与0.8，各有先验权重0.5。一次成功的加权似然为0.25和0.4，证据0.65，后验分别5/13和8/13。分母使所有候选的后验权重相加为1。

假设只考虑两枚候选硬币，正面率分别0.5和0.8，事先认为拿到两者的概率相同。观察一次正面后，第二枚更能解释结果，后验权重变成8/13，而非直接宣布它一定是第二枚。若允许成功率在0到1连续变化，后验就从两个权重变成一条密度曲线。曲线高的区域受到更多支持，曲线覆盖的宽度保留了有限观测带来的不确定性；一条具体概率取值在连续分布中的概率为零，区间面积才表示概率。

本节用十次试验中的七次成功贯穿解析计算、交互与采样实验。试验被建模为在给定同一成功率后相互独立、成功率在这段时间内不变。如果顾客来自不同渠道，或价格在试验过程中改变，这个共同成功率模型便需要增加相应结构。把这样的条件放进模型，比在结果后面加一句笼统提醒更有用：条件决定了哪些数据可以共同更新、哪些差异应另设变量。

## 一条可以手算的后验，也能预测下一批结果

Beta分布定义在0到1之间，适合表示未知成功率。两个正参数控制密度形状：两者相等时围绕0.5对称，第一项相对较大时偏向较高成功率。在二项观测模型下，Beta先验与似然相乘后仍属于Beta家族，成功数加到第一参数，失败数加到第二参数。这叫共轭，意思是更新后保留方便计算的分布形式；它让我们能先看清概率操作，再学习更复杂的计算方法。

$$
\theta\sim\operatorname{Beta}(a,b),\quad s\mid\theta\sim\operatorname{Binomial}(n,\theta),\quad\theta\mid s\sim\operatorname{Beta}(a+s,b+n-s),\quad\mathbb E[\theta\mid s]=\frac{a+s}{a+b+n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | 正的Beta先验形状参数，无量纲；可解释为更新中的先验等效计数，但不必对应实际历史样本。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c1d92ccdad2a809dfc0820ba.svg) | 试验总数、成功数与共同成功概率；0≤s≤n，给定theta时试验独立。 |
| ![Formula](https://ml-biomat.com/static/agent-math/479c4b5409f673fd67c54b6e.svg) | Beta分布、二项分布、期望和服从分布的记号；成功数为计数，概率无量纲。 |

Beta密度中theta与1−theta的幂次分别为a−1和b−1，似然贡献s与n−s，乘法让幂次相加。a=b=2，s=7、n=10得Beta(9,5)、均值9/14。两后验参数均大于1时，MAP为(9−1)/(9+5−2)=2/3。

先验Beta(2,2)更新七次成功、三次失败后成为Beta(9,5)。后验均值为9/14，约0.6429，最大后验位置MAP为8/12，约0.6667；原始比例则是0.7。三个数回答不同问题：均值平均了整个后验，MAP选择密度最高的位置，原始比例来自观测计数。这个后验的等尾95%区间约为0.386到0.861，表示在指定模型与先验下，参数落入该区间的后验概率为95%。

## 逐次加入证据，再看未来十次

蓝线为更新后的成功率密度，灰线为先验；右侧柱子表示未来十次的成功数概率。初始数据为七次成功、三次失败，可逐条增加或撤回。

[Figure: Beta后验与未来成功数分布](https://ml-biomat.com/tutorials/machine-learning/m07/#M07-plot)

下一批十次试验还包含另一层波动：即使成功率已经固定，每次成功与失败也有随机性。后验预测先对每个可能成功率计算未来结果的概率，再按照后验权重平均。代码得到未来成功数均值约6.429、方差约3.673。如果把未知成功率直接固定为后验均值，二项分布的方差只有约2.296；额外差异来自尚未消失的参数不确定性。图中两组柱具有相同均值，却以不同程度向两侧展开。

$$
P(K=k\mid D)=\int_0^1P(K=k\mid\theta)p(\theta\mid D)\,d\theta={m\choose k}\frac{B(a_*+k,b_*+m-k)}{B(a_*,b_*)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4c44806b2cfd835465c6e2b3.svg) | 未来成功数随机变量、可能成功数与未来试验数，k从0到m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/621c406e4bb4bb0dbf1ed09f.svg) | 已观察数据、成功概率与更新后的两个Beta形状参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/77b70a684b1e323b868811a4.svg) | Beta函数、从m次中选择k次成功位置的组合数与概率；结果为无量纲离散概率。 |

B函数是Beta密度的归一化积分，乘上未来二项似然后幂次增加，积分给出两个B函数之比。若后验Beta(9,5)，未来十次成功均值10×9/14≈6.429；方差为10×9×5×24/(14²×15)≈3.673。固定theta=9/14则方差10×9/14×5/14≈2.296。

![左：先验与后验，阴影为等尾95%后验区间；中：完整后验预测与固定后验均值的二项预测；右：成功比例相同、样本量不同的后验。](https://ml-biomat.com/static/tutorials/machine-learning/figures/939ce313c8e00963b9b7c05e.svg?v=939ce313c8e0)

图 1左：先验与后验，阴影为等尾95%后验区间；中：完整后验预测与固定后验均值的二项预测；右：成功比例相同、样本量不同的后验。

共轭并不限定于硬币。正态观测与合适的正态先验、泊松计数与Gamma先验，也能形成易于更新的模型。选择先验时，可以先模拟它允许怎样的观测：如果某个先验意味着一家小店常常出现远超实际接待能力的客流，就应调整模型和单位。先验预测把参数假设翻译回可理解的结果，后验预测则检查加入数据后能否再现关心的现象。这两步帮助读者把概率曲线与实际问题保持连接。

## 小店能从其他店学到什么

四家店分别观察了5、20、50和200位顾客，购买人数为4、10、30和110。第一家的观测比例最高，却只有五条记录。全部店铺合并成一个购买率会抹掉真实差异，各店完全分开又让小样本估计剧烈波动。层次模型在两者之间建立联系：每家店有自己的成功率，这些成功率共同来自一个总体分布；总体分布本身的均值和集中程度也由数据更新。

$$
\mu\sim\operatorname{Uniform}(0,1),\quad\kappa\sim\operatorname{Exponential}(\text{rate}=0.1),\quad\theta_g\mid\mu,\kappa\sim\operatorname{Beta}(\kappa\mu,\kappa(1-\mu)),\quad Y_g\mid\theta_g\sim\operatorname{Binomial}(n_g,\theta_g)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d2455474f43efb98735a21bd.svg) | 群组索引、该组试验数、成功数与成功概率；群组数据给定各自theta后独立。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e1b9bd30207e04217b3c892c.svg) | 总体成功率均值与正集中程度，均无量纲；kappa越大，群组概率通常越接近mu。 |
| ![Formula](https://ml-biomat.com/static/agent-math/698aabd843434d4c0d576e20.svg) | 均匀分布、指数分布与率参数；这里率0.1对应均值10。 |

给定mu=0.6、kappa=10，五次中四次成功的组后验均值为(4+6)/(5+10)=2/3；二百次中一百一十次成功则为116/210≈0.5524。实际层次实验还对mu和kappa的后验积分，因此结果与固定这两个值的手算不同。

给定总体均值与集中程度，一家店的后验均值可以看作自身观测比例与总体均值的加权平均。样本少时，总体信息占较大权重；样本多时，该店数据占较大权重。这个过程称为部分汇聚。它并不是把所有店机械推到0.5，而是让共同总体与各店记录相互提供信息。如果某些店面向完全不同的人群，可以加入地区、渠道等解释变量，或建立多个总体，使共享关系与实际业务结构一致。

![左：四家店的观测比例、独立Beta(1,1)后验均值和层次积分后验均值；虚线为总体均值后验平均。右：总体均值与集中程度的联合后验网格质量，纵轴为对数尺度。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b91b4456da9a9f47afa82e6d.svg?v=b91b4456da9a)

图 2左：四家店的观测比例、独立Beta(1,1)后验均值和层次积分后验均值；虚线为总体均值后验平均。右：总体均值与集中程度的联合后验网格质量，纵轴为对数尺度。

代码对总体均值和集中程度做二维网格积分，保留超参数的不确定性，再计算各店的后验均值。结果约为0.635、0.531、0.593和0.552；第一家从观测的0.8向总体信息靠近，第四家因200条记录而变化很小。总体均值的后验平均约0.572。图右侧显示的是超参数网格上的概率质量，集中程度采用对数网格，计算中包含相应的积分权重；否则把网格点简单等权相加，会改变原本声明的先验。

这里的总体均值先验在0到1均匀，集中程度采用均值10的指数先验，数值积分覆盖明确的有限范围。边缘网格质量很小，为进一步加密和扩展网格提供了检查依据。另一种做法是先估计一个超参数值再固定，称为经验贝叶斯；它计算更方便，但条件化于这个值，未把超参数的不确定性继续传递给各店。本例特意使用积分，让读者看到层次结构与计算近似是两件可以分别讨论的事。

## 看不见的状态，也可以逐步传递证据

一台设备是否处于易报警状态，不能直接观察，只能看到每个时刻有没有报警。隐马尔可夫模型HMM用隐藏状态表示内部工况，用发射概率描述状态如何产生观测，用转移概率描述状态如何延续和改变。图模型把这些关系画成节点与箭头：时间方向连接隐藏状态，每个隐藏状态再连接本时刻的观测。箭头首先规定概率分解；给定当前状态后，当前观测不再需要直接依赖其他时刻的状态。

![隐藏状态链与层次群组模型并排对照](https://ml-biomat.com/static/tutorials/machine-learning/figures/844d5bc7c2382c111cf7962f.svg?v=844d5bc7c238)

图 3两种概率结构的原创示意：HMM通过时间相邻状态共享信息，层次模型通过总体参数连接群组。箭头规定条件分布，灰色为已观察量；每个Y群组计数还条件于已知样本数。

条件独立并不意味着观察到的信号彼此毫无关系。持续的隐藏工况会让相邻报警相关，而一旦知道本时刻状态，该时刻报警的发射机制就可以单独计算。层次店铺模型也有类似区别：给定总体参数，各店概率按模型独立生成；把未知总体参数积分掉后，各店的数据会通过共同总体相互影响。读图时，可以用手遮住一个隐藏节点，想一想还剩哪些共同信息，再把它揭开。图中的连接说明计算如何分解，是否能解释为实际干预关系，需要另行建立因果模型。

$$
p(z_{1:T},y_{1:T})=\pi_{z_1}b_{z_1}(y_1)\prod_{t=2}^TA_{z_{t-1},z_t}b_{z_t}(y_t),\quad\alpha_t(j)=b_j(y_t)\sum_i\alpha_{t-1}(i)A_{ij}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b4ca40e89600686579ed8a15.svg) | 序列长度、时刻、隐藏状态、观测和前后状态索引；本例状态与报警观测均取0/1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ba3ba85084bcd9e08182feb4.svg) | 初始状态概率、从i到j的转移概率、状态j下产生观测y的发射概率；相应离散分布均归一化。 |
| ![Formula](https://ml-biomat.com/static/agent-math/41f2ee49482a5b9573a1dae6.svg) | 观测截至t并处于j的联合概率，以及依次相乘；所有量无量纲。本式alpha未归一化，代码逐步缩放以避免下溢。 |

初始概率(0.6,0.4)，无报警的发射概率(0.85,0.2)，第一步联合量(0.51,0.08)，其和0.59为首条观测概率。除以0.59后状态1概率0.135593。后续先对前一状态求和，避免重复列举共享的路径前缀。

本例只有状态0与状态1。状态1的报警概率为0.8，状态0为0.15；从状态0留在原状态的概率为0.9，从状态1留在原状态的概率为0.8。初始状态1概率为0.4。第一条观测没有报警，因此状态0贡献0.6乘0.85，状态1贡献0.4乘0.2，归一化后状态1概率约0.1356。每来一条观测，先按转移矩阵预测下一状态，再乘上该状态产生观测的概率，最后归一化。

这就是前向消息：用一个短向量汇总此前所有观测对当前状态的影响。过滤只使用截至当前的数据，适合实时判断；平滑还把后续观测通过后向消息传回来，适合事后重建。八条报警观测为0、0、1、1、1、0、1、0。在第三时刻，过滤给状态1约0.460，看到后续连续报警后的平滑概率约0.797。两者不同来自可用信息不同，实时系统不能在当时使用尚未出现的未来观测。

全序列最可能的状态路径与逐时刻最大后验状态也有区别。前者要求一整条路径的联合概率最大，通常用Viterbi动态规划；后者逐位置选择后验最大者，可能产生不同路径。代码为八时刻、两状态枚举全部256条路径，独立核对前向算法给出的观测似然，二者差约4.3×10⁻¹⁹。长序列无需枚举所有路径，消息传递复用相同的中间量，正是概率图结构带来的计算收益。

## EM在猜归属和改参数之间迭代

前面的HMM转移和发射概率已经给定。如果这些参数也未知，观测记录又没有对应的真实状态，就需要同时处理隐藏变量与模型参数。高斯混合中的组分归属也面临同样问题。直接给每个点猜一个固定类别，再当成真实标签拟合，会把不确定的归属过早锁死。EM在当前模型下计算柔性的归属概率，然后把它们当作权重更新参数，使不同可能归属都能影响下一次拟合。

$$
q_i(k)=p(z_i=k\mid x_i,\vartheta^{\rm old}),\quad N_k=\sum_iq_i(k),\quad\mu_k^{\rm new}=\frac{\sum_iq_i(k)x_i}{N_k}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c3662d65405121157c505c41.svg) | 观测索引、组分索引、观测值与隐藏归属。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0fc2bc6be6dda63561ac5f5.svg) | 当前参数下的归属责任度、旧模型参数集合与组分有效计数；q无量纲、对k相加为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/64800a1b919238f0694d679d.svg) | 更新后的组分均值，与观测同单位；要求N_k>0。 |

两个观测0和2，对某组责任度0.75和0.25，有效计数为1，加权均值(0.75×0+0.25×2)/1=0.5。E步更新软归属，M步更新参数；组分方差和比例也使用这些权重。

E步计算隐变量的条件分布，M步最大化在这份分布下的完整数据对数似然平均。高斯混合的M步因此变成加权均值、加权方差和组分比例更新。HMM的E步使用前后向消息估计各时刻状态及相邻状态对的概率，M步再按期望计数更新转移与发射概率，这一经典训练过程常称Baum–Welch。两类模型共享思路，但隐变量之间的依赖不同，所以E步所需计算也不同。

![左和中：300点高斯混合EM拟合及逐轮对数似然；右：同一八时刻观测下的HMM过滤与平滑，横轴每时刻下方写出报警观测。](https://ml-biomat.com/static/tutorials/machine-learning/figures/75521470417585818d8068a8.svg?v=755214704175)

图 4左和中：300点高斯混合EM拟合及逐轮对数似然；右：同一八时刻观测下的HMM过滤与平滑，横轴每时刻下方写出报警观测。

代码实际对300个合成一维观测运行20轮高斯混合EM。训练对数似然由约−685.0升到−550.7，两个组分均值约−2.054与1.805。曲线检查每次更新是否改善目标，也显示后期变化趋小。EM得到的是一次初始化下的参数优化结果；它没有像完整后验那样保留所有参数不确定性，多个局部最优还需要不同初始化比较。贝叶斯、EM、HMM不是互相排斥的算法名称：前者是推断框架，中间是优化方法，后者是概率模型结构。

## 抽了很多次，也可能只在原地挪动

高维后验经常难以直接积分。1953年Metropolis、Rosenbluth与Teller等人的计算工作把按概率访问状态的思想用于统计物理，后来成为广泛使用的马尔可夫链蒙特卡洛方法基础。一次随机游走提出新状态，再根据目标密度的相对大小决定接受还是保留旧状态。经过合适的运行与检查，访问记录可以用来近似后验平均、区间和预测；相邻记录彼此相关，不能简单按独立样本理解。

$$
a(\theta,\theta^{\prime})=\min\!\left(1,\frac{\widetilde p(\theta^{\prime})q(\theta\mid\theta^{\prime})}{\widetilde p(\theta)q(\theta^{\prime}\mid\theta)}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/12d2ba147169a3af41c53b5f.svg) | 当前参数状态与候选状态；本例在无量纲logit坐标中提出变化。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96d59c36164b7f8b52db2b2b.svg) | 目标的未归一化密度、提议条件密度与接受概率；比例抵消相同归一化常数，接受概率无量纲。 |

对称提议使两个q抵消，候选与当前密度比为0.4时，以概率0.4接受。比值大于1则接受。把theta变为u=log(theta/(1−theta))后，Jacobian为theta(1−theta)；Beta(9,5)的u空间密度因此正比于theta⁹(1−theta)⁵，代码据此计算。

本例故意选择已经知道解析答案的Beta(9,5)，便于核对采样器。代码在成功率的logit坐标中随机游走，并在目标密度里加入变量变换的Jacobian，避免把坐标变化误当成同一个密度。四条链从分散位置出发，丢弃前500步，再保留各4000步。步长0.7时，链的后验均值约0.6420，与解析均值0.6429接近；接受率约64%到65%，各链仍有自相关，因此有效样本量小于4000。

![每行是四条链，保留各4000步；上排步长0.7，下排0.03。轨迹每五步显示一次，ESS仍使用全部保留记录。中列为滞后自相关，右列叠加解析Beta后验。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6cb490c5c169c951822d5ed5.svg?v=6cb490c5c169)

图 5每行是四条链，保留各4000步；上排步长0.7，下排0.03。轨迹每五步显示一次，ESS仍使用全部保留记录。中列为滞后自相关，右列叠加解析Beta后验。

把步长改成0.03后，接受率升到约97%到99%，轨迹却移动缓慢。最小单链有效样本量从约573降至约4.6，经典split R-hat从约1.001升至1.224。高接受率只说明提出的变化容易接受，细小步子可能需要很久才能穿过整个后验区域。图中轨迹、自相关和直方图一起显示这个问题；直方图有一团像样的形状，并不能替代链间一致性和探索速度的检查。

$$
N_{\rm eff}\approx\frac{N}{1+2\sum_{\ell\ge1}\rho_\ell},\qquad\widehat R=\sqrt{\frac{\frac{n-1}{n}W+\frac Bn}{W}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/baccfdf2f10c579a84f14ad8.svg) | 一条链的保留样本数、某个估计量的有效样本量、滞后自相关及滞后；计数与相关无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c061b232f898f9c6c2805a73.svg) | 每条分割链的样本数、链内样本方差平均、n乘各链均值的样本方差、经典split R-hat；W与B均为参数单位平方，R-hat无量纲。 |

若一千个样本的滞后相关为0.8的连续幂，相关和为4，ESS约1000/(1+8)=111。估计均值的蒙特卡洛误差应按这些有效信息计算，不能把一千条相关记录都当独立。代码将每条链一分为二后比较W与B；现代秩诊断在正文另行说明。

这里透明实现了经典split R-hat及基于正自相关对的单链ESS，适合检查计算含义。实际复杂模型通常采用秩标准化、折叠R-hat以及bulk与tail ESS，分别检查整体分布和尾部量，并结合采样器特有诊断，例如HMC的发散。R-hat接近1说明当前检查未发现明显链间差异，仍需考虑各链是否共同漏掉一个模式。增加运行长度之前，应检查参数化、尺度与模型几何；机械稀疏保存通常只会丢掉可用于平均的信息。

## 用一个容易计算的分布靠近后验

变分推断把积分问题转成优化：选择一族方便计算的分布，再调整其中参数，使它靠近目标后验。最常见的平均场近似把不同潜变量写成相互独立的因子，计算与存储因此简化。代价也很具体：若目标后验沿倾斜方向伸展，独立因子只能用坐标轴对齐的形状近似。优化器即使准确解决了给定目标，也无法创造近似家族中原本没有的相关结构。

$$
\operatorname{ELBO}(q)=\mathbb E_q[\log p(D,\theta)-\log q(\theta)],\quad\log p(D)=\operatorname{ELBO}(q)+D_{\rm KL}(q\|p(\theta\mid D))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3afa9187688d4f19a6e3b0a9.svg) | 观测、潜变量/参数、近似分布与模型概率或密度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a33fdd5fe38628007d233099.svg) | 近似分布下的期望、自然对数、KL散度和证据下界；对数比与KL以nat计，使用一致的底层测度。 |

证据对q固定，KL非负，因此最大化ELBO等价于减小该KL。二维高斯协方差对角为1、相关0.9时，精度矩阵对角为1/(1−0.9²)，最优独立反向KL近似方差为0.19；目标边缘方差仍为1。实际优化KL约0.83037nat。

代码把目标设为均值(1,−1)、两个边缘方差均为1、相关系数0.9的二维高斯，再实际优化反向KL下的独立高斯近似。均值被恢复到约(1,−1)，两项近似方差却约为0.19。这可以从目标精度矩阵的对角项求倒数核对。图左的长椭圆和较紧的轴对齐轮廓说明近似怎样避开目标低密度区域；图右则直接显示边缘分布被压窄。这个结果来自明确的目标分布和近似家族，而非所有变分方法的固定表现。

![左：相关高斯目标的等密度线与反向KL下独立高斯近似；右：第一维边缘密度。真实边缘方差1，近似约0.19，展示这个近似家族的相关结构损失。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3e994d52b8e0e80b1bcf54e4.svg?v=3e994d52b8e0)

图 6左：相关高斯目标的等密度线与反向KL下独立高斯近似；右：第一维边缘密度。真实边缘方差1，近似约0.19，展示这个近似家族的相关结构损失。

ELBO把拟合质量与近似分布的熵联系起来，增加它等价于在固定模型下减小相应KL差异。优化曲线平稳说明数值目标不再明显改善，后验近似质量还需要检查：与小规模MCMC或解析结果对照，扩展近似家族，或考察后验预测中真正关心的量。变分推断便于较大模型快速近似，MCMC便于通过采样探索更复杂形状，两者可以在同一工作流中分工，而不必只按运行速度选一个名字。

## 高斯过程把不确定性画在整条函数上

回归时，未知对象可以是一条函数，而不只是一个成功率。高斯过程规定：在任意有限输入位置上，函数值共同服从多元高斯分布。均值函数描述中心趋势，核函数描述不同位置的函数值如何共同变化。RBF核让相近输入的函数值强相关，长度尺度决定多远仍算“相近”。因此，在一个位置观察到响应，会通过核把信息传给附近位置；离数据很远时，预测逐渐回到先验行为。

$$
k(x,x^{\prime})=\sigma_f^2\exp\!\left[-\frac{(x-x^{\prime})^2}{2\ell^2}\right],\quad m_*=k_*^\mathsf T(K+\sigma_n^2I)^{-1}y,\quad s_*^2=k_{**}-k_*^\mathsf T(K+\sigma_n^2I)^{-1}k_*
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/91cb5b808cf3e88540c9e610.svg) | 一维输入位置、另一位置、正长度尺度与先验函数方差；ell同输入单位，函数方差为响应单位平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78bbd28daaaf026101b6a87f.svg) | 观测数、n×n训练核协方差矩阵、n×n单位矩阵与n维观测向量；本式先验均值为0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24a4d93ed15072671e37c951.svg) | 训练函数值与测试函数值的n维协方差向量、测试先验方差与独立同方差高斯观测噪声方差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ac644bcc73563be6034d1268.svg) | 测试潜在函数的条件均值与方差、转置与矩阵逆；均值同响应单位，方差为响应单位平方。实际库使用稳定线性代数。 |

单个同位置观测y=1，K=k*=k**=1，噪声方差0.25，均值1/1.25=0.8，潜在方差1−1/1.25=0.2。未来观测还加独立噪声，方差0.45。多观测公式来自联合高斯分布的条件化。

本节六个观测由正弦函数加标准差0.15的高斯噪声生成，比较长度尺度0.4、1.2和3.0，核幅度固定为1，不在这六点上重新优化超参数。短长度尺度允许更快变化，两个观测之间也可能保留较大不确定性；长长度尺度偏好平缓变化，影响范围更远。长度1.2时，输入0处潜在函数标准差约0.113，到输入4处增至约0.970。这是指定核与观测位置共同产生的结果。

![同一六个含噪观测，RBF长度尺度分别0.4、1.2和3。蓝带是潜在函数、浅橙带是未来观测的逐点95%区间，点线是生成函数sin(x)。核幅度1，观测噪声标准差0.15，超参数固定。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3026f415312b78236873c2c8.svg?v=3026f415312b)

图 7同一六个含噪观测，RBF长度尺度分别0.4、1.2和3。蓝带是潜在函数、浅橙带是未来观测的逐点95%区间，点线是生成函数sin(x)。核幅度1，观测噪声标准差0.15，超参数固定。

蓝色带表示潜在函数的逐点95%后验区间，浅橙色带还加入未来一次观测的噪声方差，因此更宽。对于一个可手算例子，先验函数方差1，在同一位置观察到数值1、噪声方差0.25，后验均值为0.8、潜在函数方差0.2；未来观测方差再加0.25，得到0.45。把“函数已经知道多少”和“下一次测量还会波动多少”分开，才能正确解释阴影。逐点95%也不同于整条曲线同时落入带中的概率为95%。

![公开高斯过程例图：观测、预测曲线与逐点后验区间](https://ml-biomat.com/static/tutorials/machine-learning/figures/f259c98ddd7e8398023b3604.png?v=f259c98ddd7e)

图 8scikit-learn开发者的原始含噪高斯过程示例图，BSD-3-Clause许可，未改动。其函数为x sin(x)，与本节实验不同；按原例代码，阴影对应条件于拟合模型的潜在函数逐点区间。

官方例图使用另一个函数与噪声设置，能帮助比较观测附近和远离观测的形状。其图例写作confidence interval；按该例的RBF核、训练噪声alpha和predict返回的标准差，这里将阴影理解为固定拟合模型下的潜在函数逐点后验区间。具体代码决定区间含义。若改用包含WhiteKernel的预测协方差，或对核超参数积分，需要相应调整解释；不能仅凭阴影的颜色或“95%”字样判断。

### 完整实验：解析后验、层次积分、HMM、EM、采样、变分与GP

需要NumPy、SciPy、Matplotlib与scikit-learn。运行python main.py --output results --language zh。无需下载数据；输出六组原创图、原始数组与summary.json。解析概率、全路径枚举和单观测GP为不同计算提供独立核对。

```
"""Bayesian updates, hierarchy, exact messages, sampling, variational inference and GP."""
from pathlib import Path
import argparse,json,itertools
import numpy as np
from scipy.stats import beta,betabinom,binom,norm,multivariate_normal
from scipy.special import betaln,logsumexp,expit
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def hmm(observations,A,B,pi):
 n=len(observations);forward=np.zeros((n,2));scale=np.zeros(n);forward[0]=pi*B[:,observations[0]];scale[0]=forward[0].sum();forward[0]/=scale[0]
 for t in range(1,n):forward[t]=(forward[t-1]@A)*B[:,observations[t]];scale[t]=forward[t].sum();forward[t]/=scale[t]
 backward=np.ones((n,2))
 for t in range(n-2,-1,-1):backward[t]=A@(B[:,observations[t+1]]*backward[t+1])/scale[t+1]
 smooth=forward*backward;smooth/=smooth.sum(1,keepdims=True)
 return forward,smooth,float(np.prod(scale))

def ess_one(x):
 x=x-x.mean();n=len(x);f=np.fft.rfft(x,n=2*n);ac=np.fft.irfft(f*f.conj())[:n];ac/=ac[0];positive=0.;last=np.inf
 for lag in range(1,n-1,2):
  pair=ac[lag]+ac[lag+1]
  if pair<=0:break
  pair=min(pair,last);positive+=pair;last=pair
 return float(n/(1+2*positive)),ac

def sample_beta(step,seed,draws=4000,burn=500):
 rng=np.random.default_rng(seed);chains=[];rates=[]
 def logtarget(u):return 9*(-np.logaddexp(0,-u))+5*(-np.logaddexp(0,u)) # Beta(9,5) plus logit Jacobian
 for start in [-2,-.7,.7,2]:
  u=start;lp=logtarget(u);vals=[];accepted=0
  for t in range(draws+burn):
   v=u+rng.normal(scale=step);lv=logtarget(v)
   if np.log(rng.random())<lv-lp:u=v;lp=lv;accepted+=1
   if t>=burn:vals.append(expit(u))
  chains.append(vals);rates.append(accepted/(draws+burn))
 chains=np.array(chains);split=np.concatenate([chains[:,:draws//2],chains[:,draws//2:]]);n=split.shape[1];W=np.var(split,axis=1,ddof=1).mean();B=n*np.var(split.mean(1),ddof=1);rhat=np.sqrt(((n-1)/n*W+B/n)/W);esses=[ess_one(c)[0] for c in chains]
 return chains,{'step':step,'mean':float(chains.mean()),'acceptance':rates,'classical_split_rhat':float(rhat),'per_chain_ess':esses,'minimum_chain_ess':min(esses)}

def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';T=lambda z,e:z if zh else e;rng=np.random.default_rng(7)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
 def save(fig,n):fig.savefig(out/f'{n}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 a,b=9,5;grid=np.linspace(.001,.999,1000);k=np.arange(11);pred=betabinom.pmf(k,10,a,b);plug=binom.pmf(k,10,a/(a+b));ci=beta.ppf([.025,.975],a,b)
 fig,axs=plt.subplots(1,3,figsize=(14,4.3),layout='constrained');axs[0].plot(grid,beta.pdf(grid,2,2),label=T('先验 Beta(2,2)','Prior Beta(2,2)'),color='#83949e');axs[0].plot(grid,beta.pdf(grid,a,b),label=T('后验 Beta(9,5)','Posterior Beta(9,5)'),color='#237b94');axs[0].fill_between(grid,0,beta.pdf(grid,a,b),where=(grid>=ci[0])&(grid<=ci[1]),alpha=.17,color='#237b94');axs[0].set(xlabel=T('成功概率','Success probability'),ylabel=T('概率密度','Density'));axs[0].legend(fontsize=9)
 axs[1].bar(k-.18,pred,width=.36,color='#237b94',label=T('后验预测','Posterior predictive'));axs[1].bar(k+.18,plug,width=.36,color='#d87430',label=T('固定均值概率','Fixed mean probability'));axs[1].set(xlabel=T('未来10次的成功数','Successes in ten future trials'),ylabel=T('概率','Probability'));axs[1].legend(fontsize=9)
 for n in [10,40,200]:axs[2].plot(grid,beta.pdf(grid,2+.7*n,2+.3*n),label=f'n={n}')
 axs[2].set(xlabel=T('成功概率','Success probability'),ylabel=T('后验密度','Posterior density'),title=T('成功比例均为70%','Same observed success fraction: 70%'));axs[2].legend();save(fig,'update_predictive')
 # Integrate uncertain population mean and concentration on a quadrature grid.
 ns=np.array([5,20,50,200]);success=np.array([4,10,30,110]);mu=np.linspace(.002,.998,240);kappa=np.geomspace(.05,150,220);M,K=np.meshgrid(mu,kappa);aa=M*K;bb=(1-M)*K;logw=-K/10+np.log(K) # Exp(mean=10) prior and log-kappa Jacobian; mu uniform
 for n,s in zip(ns,success):logw+=betaln(s+aa,n-s+bb)-betaln(aa,bb)
 weights=np.exp(logw-logsumexp(logw));hiermean=np.array([np.sum(weights*(s+aa)/(n+K)) for n,s in zip(ns,success)]);independent=(success+1)/(ns+2);population_mu=float(np.sum(weights*M));edge_mass=float(weights[:3].sum()+weights[-3:].sum()+weights[:,:3].sum()+weights[:,-3:].sum())
 fig,axs=plt.subplots(1,2,figsize=(12,4.7),layout='constrained');xs=np.arange(4);axs[0].plot(xs,success/ns,'o--',label=T('观测比例','Observed fraction'),color='#d87430');axs[0].plot(xs,independent,'s--',label=T('各自Beta(1,1)','Separate Beta(1,1)'),color='#83949e');axs[0].plot(xs,hiermean,'o-',label=T('层次后验均值','Hierarchical posterior mean'),color='#237b94');axs[0].axhline(population_mu,ls=':',color='#237b94');axs[0].set(xticks=xs,xticklabels=[f'{i+1} (n={n})' for i,n in enumerate(ns)],xlabel=T('群组与样本量','Group and sample count'),ylabel=T('成功概率估计','Estimated success probability'),ylim=(.35,.9));axs[0].legend(fontsize=9)
 im=axs[1].pcolormesh(mu,kappa,weights,shading='auto',cmap='Blues',rasterized=True);axs[1].set(yscale='log',xlabel=T('总体均值','Population mean'),ylabel=T('集中程度 kappa','Concentration kappa'),title=T('超参数联合后验网格质量','Hyperparameter joint posterior grid mass'));fig.colorbar(im,ax=axs[1],label=T('网格概率质量','Grid probability mass'));save(fig,'hierarchy')
 # Transparent EM for a one-dimensional Gaussian mixture.
 latent=rng.random(300)>.4;data=rng.normal(np.where(latent,2.,-2.),np.where(latent,1.,.7));means=np.array([-1.,1.]);variances=np.ones(2);mix=np.ones(2)/2;history=[]
 for iteration in range(21):
  logjoint=np.array([np.log(mix[j])+norm.logpdf(data,means[j],np.sqrt(variances[j])) for j in range(2)]).T;den=logsumexp(logjoint,axis=1);history.append(float(den.sum()));resp=np.exp(logjoint-den[:,None]);mass=resp.sum(0)
  if iteration<20:mix=mass/len(data);means=(resp*data[:,None]).sum(0)/mass;variances=np.maximum((resp*(data[:,None]-means)**2).sum(0)/mass,1e-6)
 obs=np.array([0,0,1,1,1,0,1,0]);A=np.array([[.9,.1],[.2,.8]]);B=np.array([[.85,.15],[.2,.8]]);pi=np.array([.6,.4]);filtered,smoothed,likelihood=hmm(obs,A,B,pi);brute=0.;pathbest=None;maxprob=-1
 for path in itertools.product(range(2),repeat=len(obs)):
  prob=pi[path[0]]*B[path[0],obs[0]]
  for t in range(1,len(obs)):prob*=A[path[t-1],path[t]]*B[path[t],obs[t]]
  brute+=prob
  if prob>maxprob:maxprob=prob;pathbest=path
 fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained');u=np.linspace(-5,5,500);axs[0].hist(data,bins=30,density=True,color='#d8e3e8');axs[0].plot(u,sum(mix[j]*norm.pdf(u,means[j],np.sqrt(variances[j])) for j in range(2)),color='#237b94');axs[0].set(xlabel=T('观测值','Observation'),ylabel=T('密度','Density'),title=T('EM拟合混合密度','EM mixture fit'));axs[1].plot(range(21),history,'o-',ms=3,color='#237b94');axs[1].set(xlabel=T('EM更新次数','EM updates'),ylabel=T('训练对数似然','Training log likelihood'));axs[2].plot(range(1,9),filtered[:,1],'o-',label=T('过滤：截至当前','Filtering: observations so far'));axs[2].plot(range(1,9),smoothed[:,1],'s--',label=T('平滑：完整序列','Smoothing: full sequence'));axs[2].set(xticks=range(1,9),xticklabels=[f'{i+1}\n{o}' for i,o in enumerate(obs)],xlabel=T('时刻 / 报警观测','Time / observed alarm'),ylabel=T('状态1的后验概率','Posterior probability of state 1'),ylim=(0,1));axs[2].legend(fontsize=8);save(fig,'latent_messages')
 good,gd=sample_beta(.7,7);slow,sd=sample_beta(.03,17);fig,axs=plt.subplots(2,3,figsize=(14,8),layout='constrained')
 for row,(chains,dg) in enumerate([(good,gd),(slow,sd)]):
  for i,c in enumerate(chains):axs[row,0].plot(c[::5],lw=.6,alpha=.7,label=str(i+1))
  axs[row,0].set(xlabel=T('每5步显示一次','Displayed every fifth draw'),ylabel=T('成功概率','Success probability'),title=f'step={dg["step"]}, split R-hat={dg["classical_split_rhat"]:.3f}')
  for c in chains:axs[row,1].plot(ess_one(c)[1][:100],alpha=.8)
  axs[row,1].set(xlabel=T('滞后步数','Lag'),ylabel=T('自相关','Autocorrelation'),title=f'min ESS={dg["minimum_chain_ess"]:.0f}')
  axs[row,2].hist(chains.ravel(),bins=45,density=True,alpha=.6,color='#237b94');axs[row,2].plot(grid,beta.pdf(grid,a,b),color='#d87430');axs[row,2].set(xlabel=T('成功概率','Success probability'),ylabel=T('密度','Density'),title=T('采样与解析后验','Samples and analytic posterior'))
 save(fig,'sampling')
 # Actual optimization of reverse KL for an independent Gaussian approximation.
 target_mean=np.array([1.,-1.]);cov=np.array([[1,.9],[.9,1.]]);precision=np.linalg.inv(cov)
 def kl(p):
  delta=p[:2]-target_mean;v=np.exp(2*p[2:]);return .5*(np.dot(np.diag(precision),v)+delta@precision@delta-2+np.linalg.slogdet(cov)[1]-np.log(v).sum())
 fit=minimize(kl,[0,0,0,0],method='BFGS');qm=fit.x[:2];qv=np.exp(2*fit.x[2:]);gx,gy=np.meshgrid(np.linspace(-2,4,160),np.linspace(-4,2,160));pts=np.dstack([gx,gy]);fig,axs=plt.subplots(1,2,figsize=(11,4.6),layout='constrained');axs[0].contour(gx,gy,multivariate_normal.pdf(pts,target_mean,cov),levels=[.02,.08,.2],colors=['#d87430']);axs[0].contour(gx,gy,multivariate_normal.pdf(pts,qm,np.diag(qv)),levels=[.02,.08,.2],colors=['#237b94'],linestyles='--');axs[0].set(xlabel='theta 1',ylabel='theta 2',title=T('橙：目标；蓝虚线：独立近似','Orange: target; blue dashed: independent approximation'));axs[0].set_aspect('equal');u=np.linspace(-2,4,500);axs[1].plot(u,norm.pdf(u,1,1),label=T('目标边缘','Target marginal'),color='#d87430');axs[1].plot(u,norm.pdf(u,qm[0],np.sqrt(qv[0])),label=T('变分边缘','Variational marginal'),color='#237b94');axs[1].set(xlabel='theta 1',ylabel=T('概率密度','Density'));axs[1].legend();save(fig,'variational')
 xx=np.array([-2,-1.6,-.5,.2,.7,1.8])[:,None];yy=np.sin(xx[:,0])+rng.normal(0,.15,len(xx));query=np.linspace(-4,4,400)[:,None];gps={};fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained')
 for ax,length in zip(axs,[.4,1.2,3.]):
  gp=GaussianProcessRegressor(kernel=RBF(length,length_scale_bounds='fixed'),alpha=.15**2,optimizer=None).fit(xx,yy);mean,std=gp.predict(query,return_std=True);obs_std=np.sqrt(std**2+.15**2);ax.fill_between(query[:,0],mean-1.96*obs_std,mean+1.96*obs_std,color='#d87430',alpha=.15,label=T('未来观测95%区间','Future-observation 95% interval'));ax.fill_between(query[:,0],mean-1.96*std,mean+1.96*std,color='#237b94',alpha=.25,label=T('潜在函数95%区间','Latent-function 95% interval'));ax.plot(query,mean,color='#237b94');ax.scatter(xx,yy,c='#263744',s=24);ax.plot(query,np.sin(query),':',color='#83949e');ax.set(title=f'RBF length={length}',xlabel=T('输入x（无量纲）','Input x (unitless)'),ylabel=T('响应（无量纲）','Response (unitless)'),ylim=(-2.8,2.8));gps[str(length)]={'latent_std_at_zero':float(gp.predict([[0]],return_std=True)[1][0]),'latent_std_at_four':float(gp.predict([[4]],return_std=True)[1][0])}
 axs[1].legend(fontsize=8,loc='upper center');save(fig,'gaussian_process')
 one=GaussianProcessRegressor(kernel=RBF(1,length_scale_bounds='fixed'),alpha=.25,optimizer=None).fit([[0]],[1]);one_m,one_s=one.predict([[0]],return_std=True)
 summary={'prior_alpha':2,'prior_beta':2,'successes':7,'failures':3,'posterior_alpha':a,'posterior_beta':b,'posterior_mean':a/(a+b),'posterior_map':(a-1)/(a+b-2),'posterior_ci95':ci.tolist(),'predictive_mean':float(betabinom.mean(10,a,b)),'predictive_variance':float(betabinom.var(10,a,b)),'predictive_mass_sum':float(pred.sum()),'hierarchical_group_means':hiermean.tolist(),'hierarchical_population_mean':population_mu,'hyper_grid_edge_mass':edge_mass,'em_final_means':means.tolist(),'em_log_likelihood':history,'em_min_improvement':float(np.diff(history).min()),'hmm_likelihood':likelihood,'hmm_brute_likelihood':brute,'hmm_likelihood_error':abs(likelihood-brute),'hmm_filtered':filtered[:,1].tolist(),'hmm_smoothed':smoothed[:,1].tolist(),'hmm_most_probable_path':list(pathbest),'mcmc_good':gd,'mcmc_slow':sd,'variational_mean':qm.tolist(),'variational_variances':qv.tolist(),'variational_kl':float(fit.fun),'variational_optimizer_success':bool(fit.success),'gp':gps,'gp_one_observation_mean':float(one_m[0]),'gp_one_observation_latent_variance':float(one_s[0]**2)}
 np.savez_compressed(out/'experiment_data.npz',beta_grid=grid,predictive=pred,hierarchy_mu=mu,hierarchy_kappa=kappa,hierarchy_weights=weights,em_data=data,hmm_observations=obs,hmm_transitions=A,hmm_emissions=B,good_chains=good,slow_chains=slow,gp_x=xx,gp_y=yy);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

这套实验形成一条可复查的路线：先用Beta更新建立解析答案，再用层次积分共享信息，用HMM消息处理时间依赖，用EM估计隐变量模型参数，随后检查采样与变分近似，最后把后验传播到函数预测。新问题也可以按同样顺序组织：说明观测如何产生，写出未知量及共享关系，选择计算方法，并把后验预测带回实际对象检查。概率模型的价值在于让每一步的不确定性有清楚的来源与计算位置。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Bayes (1763), An Essay towards Solving a Problem in the Doctrine of Chances](https://www.jstor.org/stable/105741)

   由观测推断未知机会的历史问题。

   Historical reference
2. [PyMC — General API quickstart](https://www.pymc.io/projects/examples/en/latest/introductory/api_quickstart.html)

   模型定义、先验、采样与预测的现代工作流。

   MIT example project; reference
3. [Gelman et al., Bayesian Workflow](https://arxiv.org/abs/2011.01808)

   把模型检查与计算检查纳入推断。
4. [Stan — Latent Discrete Parameters](https://mc-stan.org/docs/stan-users-guide/latent-discrete.html)

   HMM与前向边缘化。
5. [hmmlearn — Tutorial](https://hmmlearn.readthedocs.io/en/latest/tutorial.html)

   隐藏状态、发射、解码与EM。

   BSD-3-Clause project
6. [Metropolis et al. (1953), Equation of State Calculations by Fast Computing Machines](https://www.osti.gov/biblio/4390578)

   概率状态访问与蒙特卡洛计算背景。

   Primary bibliographic reference
7. [Stan — Posterior Analysis](https://mc-stan.org/docs/reference-manual/analysis.html)

   split R-hat、秩标准化、ESS与采样误差。
8. [Blei, Kucukelbir & McAuliffe (2017), Variational Inference: A Review for Statisticians](https://www.cs.columbia.edu/~blei/papers/BleiKucukelbirMcAuliffe2017.pdf)

   ELBO、平均场与近似家族。
9. [scikit-learn — Gaussian Processes regression: basic introductory example](https://scikit-learn.org/stable/auto_examples/gaussian_process/plot_gpr_noisy_targets.html)

   原始公开GP图、核与训练噪声。

   BSD-3-Clause
