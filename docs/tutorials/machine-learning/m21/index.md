# 时间序列：站在过去，预测未来

Source: https://ml-biomat.com/tutorials/machine-learning/m21/
Language: zh-CN

从面包店备货到设备监测，把季节规律、深度预测与不确定性放在同一条时间轴上。

## 1. 预测的第一步，是站在正确的时间点上

面包店要决定明天烤多少面包，电网要安排下周供电，实验室想知道设备温度何时可能超过工作范围，这些问题都依赖时间序列。它们不仅关心下一次观测是多少，还关心提前多久作决定、当时能知道哪些信息，以及预测偏高或偏低会带来什么代价。今天收盘后做出的“今天销量预测”对早晨备货没有帮助。一个完整的预测问题，应先写清预测起点、预测步长和结果使用时刻，再选择模型。

时间索引也不是表格旁边的一列装饰。每天一条记录与工作日一条记录的“上一行”含义不同，时区与夏令时会影响小时数，重复时间戳可能来自补报或不同设备。缺测应与真实的零区分：商店没营业、营业但没卖出、数据接口断开，是三种不同情况。若使用插值补缺，要检查插值是否读取了预测时刻之后的值；居中的滑动平均也可能偷偷借用未来。先把观测何时产生、何时可获得理清，后面的训练与评估才有明确边界。

本章用一条规则公开的合成需求序列贯穿计算。它有缓慢上升的水平、每周和年度起伏、相关噪声，以及后期一次水平变化。先用“明天等于今天”和“下周等于上周”建立可解释基线，再比较平滑模型、ARIMA、滞后特征回归与小型 GRU。我们会保留模型实际失败的部分：在这里，包含季节结构的简单方法优于这个固定训练配置的 GRU，而原先校准的区间在水平变化后覆盖明显下降。这样的结果帮助我们理解模型究竟利用了什么，而不把复杂程度当作效果保证。

## 2. 今天、上周与慢慢变化的水平

朴素预测把最近一次观测延续到未来，适合先回答“变化是否真的可预测”。季节朴素预测则重复上一个完整季节：每天的数据有稳定周规律时，下周一参考上周一，而不是刚过去的星期日。若最近七天的数值依次为 1 到 7，那么接下来七天的季节朴素预测仍是 1 到 7。它不需要估计许多参数，却保留了任务中最明显的周期线索。一个新模型应在相同预测时点、相同步长上与它比较，才能看出额外计算带来了多少收益。

$$
\hat y_{T+h\mid T}=y_T\quad\text{(naive)},\qquad \hat y_{T+h\mid T}=y_{T+h-m}\quad\text{(seasonal, }1\le h\le m\text{)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | 第 t 个时间步的观测，单位为需求量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 最后一个可见观测的时间索引，整数；预测起点为 T+1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 向未来预测的步数，正整数；本式季节形式限制在一个周期内。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 一个季节的时间步数，例如日数据的周周期 m=7。 |
| ![Formula](https://ml-biomat.com/static/agent-math/90cfee39269e6a786b411a86.svg) | 在已知截至 T 的信息时，对 T+h 的预测，单位为需求量。 |

朴素方法直接沿用最后观测；季节方法把目标日期向前移动一个周期，因此引用相同季节位置。若最后一周依次为 1、2、3、4、5、6、7，最后观测是 7，朴素的七个预测全为 7，季节预测为 1 到 7。超过一周期时继续循环最近周期的位置，不能直接引用未来尚未观测的值。这里的竖线表示信息截止时刻，不是除法。

指数平滑把过去压缩为持续更新的状态。简单指数平滑保留一个水平估计：新观测占一部分权重，上一时刻的水平占剩余权重。展开递推后，越久远的观测权重越小，因此得名“指数”。水平从 100 更新到观测 120，若平滑系数为 0.2，新水平是 104；它既没有完全忽略变化，也没有把一次波动全部当成新常态。系数越大，响应越快，噪声也更容易进入状态。Holt 的趋势扩展再估计每步变化，Holt–Winters 则加入周期位置上的季节状态。

$$
\begin{aligned}\ell_t&=\alpha(y_t-s_{t-m})+(1-\alpha)(\ell_{t-1}+b_{t-1}),\\ b_t&=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1},\\ s_t&=\gamma(y_t-\ell_t)+(1-\gamma)s_{t-m},\\ \hat y_{t+h\mid t}&=\ell_t+h b_t+s_{t+h-m},\quad 1\le h\le m.\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | 时刻 t 的观测，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a6fe2f82fa2e4afba3c32986.svg) | 更新后的局部水平，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d82478c4058da6c98fa79581.svg) | 每个时间步的趋势增量，需求量/步。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f0ee2fe79451c957263c10d2.svg) | 当前季节位置的加法偏移，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f49874ef6bc310341e9a984.svg) | 水平、趋势、季节的平滑权重，均在 0 到 1 之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1605fb5ff388cf936c72524e.svg) | 当前整数时间索引、周期步数、预测步长；本例一步一天，m=7。 |
| ![Formula](https://ml-biomat.com/static/agent-math/508f70b1421da086232be5bb.svg) | 未来观测的预测，需求量单位。 |

第一行先减去同季节位置的偏移，再把观测与上一水平加趋势作加权；第二行平滑水平的变化；第三行把去掉新水平后的剩余分配给季节。代码采用这里的分量更新形式。取上一水平 100、趋势 2、对应旧季节 5、新观测 110，权重依次为 0.2、0.1、0.3，则新水平为 102.6，新趋势为 2.06，新季节为 5.72。若下一天对应的季节偏移为 4，一步预测为 102.6+2.06+4=108.66。一步的趋势乘以步长才与水平具有相同量纲。

这些递推公式也保留了预测方法发展的实际背景。库存与生产计划需要反复更新成百上千条需求记录，而早期计算资源有限；把全部历史压缩成少量状态，可以让新观测到来时立即修正预测。Holt 对趋势、Winters 对季节的扩展，让这种更新方式适应更丰富的商业序列。后来状态空间表述又把原先的分量规则与概率建模接起来，使人们不仅能报出下一次数值，也能讨论误差如何向未来传播。方法的演变始终围绕同一个问题：保留哪些历史信息，才足以支撑下一次决定？

加法季节性用绝对幅度描述起伏，例如每到周末多售 20 份；乘法季节性用比例描述，例如周末多售 20%。当序列整体水平增长时，二者的预测会逐渐分开。ETS 把误差、趋势和季节成分放入状态空间形式，名称中的字母分别描述这些组成，既便于比较结构，也便于产生预测分布。本章代码采用固定系数的加法 Holt–Winters 分量更新，显式维护水平、趋势和七个季节位置，不自动搜索所有 ETS 形式。阅读代码时，可以直接追踪今天的观测怎样改变明天的状态。

趋势和季节只是有用的描述，不是每条曲线都必须具备的零件。短记录中的一个弯曲片段可能看起来像长期趋势，节假日的日期又可能每年变化。分解方法用于探索时，应说明平滑窗口和边界处理；用于实时预测时，要保证每个时刻的分量仅由当时可见数据估计。生成数据中的“真实趋势”可以直接画出来检查方法，但现实数据中同名分量通常是估计结果，不能把某一次分解当作唯一的物理原因。

## 3. ARIMA 与状态空间：从相邻时刻的关系入手

ARIMA 从自相关出发：今天相对常态的偏离，是否与昨天的偏离有关？AR 部分使用过去的序列值，MA 部分使用过去的预测创新，I 表示先差分再把预测累积回原尺度。这里的“移动平均”不是对最近几天观测做普通平均，而是对过去误差的加权组合。差分帮助去掉某些随时间移动的水平；季节差分则比较今天与上一个同季节位置。差分次数过多也会引入不必要的噪声结构，因此应检查序列与残差，而不是越多越好。

$$
d_t=y_t-y_{t-1},\qquad d_t=c+\phi d_{t-1}+\varepsilon_t,\qquad \hat y_{T+h\mid T}=y_T+\sum_{j=1}^{h}\hat d_{T+j\mid T}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | 第 t 步的需求观测，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea3b128d75d4d2dd987ffaf5.svg) | 相邻观测的差，需求量单位；时间间隔固定为一步。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 差分回归的常数项，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | 前一个差分的系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c56edde4f1d59f195d1ee.svg) | 均值为零的预测创新，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/766c1b88c51440c474b41780.svg) | 最后观测索引、预测步数、求和中的未来步数，均为整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be0c2f50f513b340b58e1769.svg) | 预测差分和累积后的预测需求，均为需求量单位。 |

ARIMA(1,1,0) 中的三个数字分别表示一个自回归滞后、一次差分、没有移动平均创新项。预测时把未来创新的条件均值设为零，递推差分后再加回最近观测。若最后需求是 10、最后差分是 2、c=0.5、φ=0.5，则下一差分为 1.5，再下一差分为 1.25；一步预测 11.5，两步预测 12.75。脚本以条件最小二乘估计常数和系数，不计算完整似然或自动选择季节阶数。

代码实现一个可手算的 ARIMA(1,1,0)：先对相邻观测作一次差分，再用常数项和前一个差分预测下一个差分，最后从最近观测累积回去。若过去每天恰好增加 1，预测就应继续增加 1；脚本用这个输入检查实现。它没有季节项，所以在强周规律的本章数据中输给季节朴素并不意外。完整的季节 ARIMA 可增加季节滞后、季节差分与季节误差项。选择阶数时，信息准则、残差自相关与真正的多步回测各自提供不同信息。

状态空间模型换了一个观察角度：我们看到的是带噪观测，背后还有一个随时间变化但不能直接测到的状态。以设备温度为例，真实温度逐步变化，传感器再叠加测量误差。预测步骤先根据状态转移估计下一状态和不确定性，更新步骤再根据新观测与预测的差修正状态。在线卡尔曼滤波在同一时刻只使用过去和当前数据；平滑则允许利用后续观测回看过去，二者用于预测回测时不能互换。

$$
\begin{aligned}\mu_t^-&=\mu_{t-1},& P_t^-&=P_{t-1}+q,\\ K_t&=\frac{P_t^-}{P_t^-+r},&\mu_t&=\mu_t^-+K_t(y_t-\mu_t^-),\\ P_t&=(1-K_t)P_t^-.\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9d131aa3749f8c85574efde6.svg) | 观测更新之前、之后的隐藏水平估计，观测量单位；上标 − 表示预测阶段。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | 当前观测，观测量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b59daee6fd36fad95fe4813a.svg) | 更新之前、之后的状态误差方差，观测量单位的平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4d4462a83beb571480a8e07.svg) | 每步过程噪声方差与测量噪声方差，观测量单位的平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b4090df4ac7ee2164e33cf0b.svg) | 卡尔曼增益，0 到 1 之间的无量纲观测权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 离散时间步索引。 |

这是隐藏水平按随机游走变化、观测直接测量该水平的标量线性高斯模型。预测不改变水平均值，却增加过程方差；更新按状态和测量各自的不确定性分配权重。若预测水平 10、预测方差 4、测量方差 9、新观测 13，则增益为 4/13，更新水平为 10+3×4/13≈10.923，更新方差为 36/13≈2.769。测量越精确，r 越小，观测获得越大权重。这里是机制算例，与后面的六模型比较分开。

这个框架也解释了缺测怎么处理：没有新测量时，可以继续执行状态预测，但跳过观测更新，不确定性随之变化。多个传感器可以通过不同观测方程共享同一潜在状态；趋势和季节也可以写进状态向量。状态空间并不与神经网络互斥，转移或观测映射也可以学习。关键问题仍是哪些量会随时间演化、哪些噪声来自过程、哪些噪声来自测量，以及这些假设是否与预测任务一致。

## 4. 回测要重演当时能做出的决定

随机打乱时间序列再切分，会让模型在训练时见到测试时点之后的模式。滚动起点回测则不断把日历推进：在某个起点，只使用它之前的历史，预测接下来的若干步，等待对应真值后计算误差，再进入下一个起点。扩展窗口保留全部过去，滑动窗口只保留最近一段历史。前者利用更多样本，后者可能更快适应机制变化。无论哪种，预处理、特征选择与参数估计都应遵守同一时间边界。

一步预测与七步预测也不是同一道题。递归策略训练下一步模型，再把预测结果接回输入，逐步走到未来；它共享一套规则，但早期误差会进入后续步骤。直接策略一次预测每个未来步长，可以使用多个输出头或一个向量输出；它避免把自己的前一步预测当真值，却需要从数据学会各步长的关系。本章 Ridge 使用递归预测，GRU 一次输出七个数。误差图按步长分开，帮助看清模型在哪个时间距离上开始失去优势。

外生变量的可获得时间尤其重要。日历、已安排的促销与预先设定的价格，可以在预测起点知道；下周的实际温度和未来故障记录通常还不知道。使用天气预报作为输入，应保存当时发布的天气预报版本，而不是用事后实测温度替代。若外生变量本身也要预测，其误差应进入整个系统的评价。本章回归使用历史滞后、已知日历周期和时间位置，没有把未来需求或未来真实噪声放入特征。

四个时间段承担不同职责：日索引 0–499 用于训练；500–599 选择 GRU 检查点；600–699 校准区间；700 以后用于测试。测试每七天发出一次七日预测，共 28 个起点和 196 个预测值，最后四天没有形成完整预测窗，因此不纳入这次统计。Ridge 与 GRU 的权重在测试期间固定，输入可以更新到当时最新观测；平滑状态与 ARIMA 参数则根据各起点之前的历史更新。比较的是这组明确部署方式，若要比较其他更新频率，应另做相同协议的实验。

![上：900 天合成需求及四个连续时间段，虚线标记日索引 820 的水平变化。下：去掉已知生成趋势后的局部观测与已知季节分量；这些真实分量来自生成规则，未提供给预测器。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b6ed27ad1adf72c51c661309.svg?v=b6ed27ad1adf)

图 1上：900 天合成需求及四个连续时间段，虚线标记日索引 820 的水平变化。下：去掉已知生成趋势后的局部观测与已知季节分量；这些真实分量来自生成规则，未提供给预测器。

## 5. 深度预测：学习跨时间复用的表示

神经预测把一段历史变成内部表示，再生成未来。GRU 用门控状态积累信息，时间卷积在多个局部窗口中寻找模式，Transformer 则让不同时间位置通过注意力交换信息。把一段时间切成 patch，可以减少很长序列的计算长度，同时保留片段内部结构。它们都需要知道顺序，可以加入位置、日历和采样间隔等信息。输入形状通常是批次×历史长度×变量数，输出是批次×预测步长×目标数；把这些维度写清，比只说“用了 Transformer”更能说明实际做了什么。

本章的小 GRU 接收最近 28 天的单变量序列，隐藏维度为 16，最后一个隐藏状态通过线性层一次输出七天。标准化只使用训练段的均值与标准差，所有后续窗口沿用这两个数。它能从训练窗口学习重复形状，但训练段之外的水平增长与后期跳变要求进一步外推。测试中这个配置的误差高于季节基线，提示我们检查输入是否保留了合适的水平和季节信息、是否需要局部归一化或更新模型，以及训练样本数量是否支持当前参数量。增加网络深度不是这些问题的共同答案。

时间序列基础模型试图从大量不同序列中学习可迁移规律。Chronos 的 2024 年论文把经过缩放和量化的数值序列转成可由语言模型式结构处理的 token，并通过生成得到预测分布；TimesFM 的原始工作则使用适合时间序列片段的解码器式预训练设计。它们的共同目标是让新序列从跨数据集经验中获益。实际选用时仍应核对输入频率、上下文长度、多变量与外生变量支持方式，以及模型训练数据和本次评价数据是否重叠。

多个序列一起训练，还会引入“共享什么”的选择。同一家连锁店的多个门店可能共享周末模式，却有不同规模；不同设备可能共享动力学，但传感器单位和噪声不同。全局模型可以借助对象标识、静态属性和归一化来学习共同规律，再保留对象差异。评估时既要看已有对象未来时段，也要根据应用需要留出全新对象。只有这样，才能区分模型学会了时间演化，还是记住了某个对象的典型水平。

## 6. 未来有波动，预测也应表达范围

一个点预测把可能的未来压缩成一个数字。面包店若只按平均销量备货，就没有表达缺货和剩余的不同成本。分位数预测给出更丰富的信息：0.9 分位数对应一个希望约 90% 观测落在其下方的位置，适合某些偏向避免缺货的决策。分位数损失对高估和低估施加不同权重，让模型学习这个位置。多个分位数组成区间后，还要检查它们是否顺序一致，避免较低分位数反而高于较高分位数。

$$
e=y-q_\tau,\qquad L_\tau(y,q_\tau)=\begin{cases}\tau e,&e\ge0,\\(\tau-1)e,&e<0.\end{cases}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 实际观测，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c744d28123c834669893c23a.svg) | 模型预测的 τ 分位数，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 分位数水平，0 到 1 之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 真值减预测值，正值表示低估，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/827f570a764047d02167b369.svg) | 分位数损失，需求量单位。 |

当 τ=0.9，低估的每单位误差乘 0.9，高估的每单位误差乘 0.1，因此最优位置会比中位数更高。预测为 10 时，真值 12 的损失为 1.8，真值 8 的损失为 0.2；两种误差绝对值相同，但代价不同。若真值连续分布，期望损失在预测位置两侧的概率权重平衡时达到最小，对应 τ 分位数。损失不需要先假设未来服从正态分布。

区间评价同时关注覆盖率和宽度。把区间无限放宽，几乎什么都能覆盖，却无法支持精细决策；区间过窄则频繁漏掉真实值。可以统计真值落入区间的比例、平均区间宽度，以及对漏出部分施加额外惩罚的区间分数。还应按预测步长、对象类别和运行条件分组查看：总体覆盖接近 90%，并不说明远期预测或稀有状态也同样可靠。时间相关与机制变化会影响校准残差是否适用于未来，必须用后续数据检验。

$$
\mathrm{coverage}=\frac1n\sum_{i=1}^n\mathbf1\{L_i\le y_i\le U_i\},\qquad \mathrm{width}=\frac1n\sum_{i=1}^n(U_i-L_i)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | 评价的预测个数及其索引，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第 i 个预测对应的实际需求，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8a3f22d38c60047b8702b4f2.svg) | 预测区间下界与上界，需求量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2ac1b98030d2dc2b2acb75cd.svg) | 括号内条件成立时为 1，否则为 0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e7e43dea1f17851acba633c1.svg) | 被区间覆盖的比例，0 到 1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4121a5409ac039446013e23.svg) | 平均区间宽度，需求量单位。 |

先逐项判断真值是否落在上下界之间，再对 0/1 结果取平均，就得到实际覆盖率。四个区间覆盖了三个真值时，覆盖率为 0.75。区间 [8,12] 与 [0,20] 都能覆盖真值 10，但宽度分别为 4 与 20，二者提供的信息量不同。脚本的固定半宽约为 2.993，所以所有区间宽度约 5.986；比较变化前后覆盖率时，宽度保持相同。

代码用独立校准段中 Ridge 的绝对预测误差，选择按有限样本秩修正的约 90% 分位数作为固定半宽，得到预测值上下各约 2.993 的区间。这里是透明易查的残差区间构造，不假设时间序列残差自动满足可交换性。测试的实际覆盖率为 0.6429：变化前为 0.9167，变化后降到 0.2105。固定区间没有随新的水平偏差变宽，读者能在时间轴上看到漏出的观测集中在哪里。区间应当随着可获得的新证据重新校准，并与重新训练或状态更新分开记录。

## 7. 完整实验：六种预测器站在相同的日历上

合成序列的基础水平从 40 起，每天增加 0.018；周起伏振幅为 5，年度起伏振幅为 3。随机噪声由前一天噪声的 0.6 倍加上标准差 1.5 的新扰动组成，日索引 820 起额外增加 6。所有数值使用统一的需求量单位，时间步为一天。我们保留这些生成分量用于解释，但预测器只收到当时可见的总观测和规定的日历特征，并没有直接获得真实趋势、真实噪声或未来变化点。

### 六种时序预测器与按时间校准的区间

固定随机种子生成 900 天需求，按时间训练、选择与校准，输出真实测试误差、分步长误差和变化前后覆盖率。依赖 NumPy、PyTorch、scikit-learn 和 Matplotlib，CPU 两线程。

```
"""Chronological forecasts, rolling horizons, and held-out interval calibration."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
HORIZON=7


def seasonal_naive(history, horizon=7, period=7):
    return np.asarray([history[-period+(h%period)] for h in range(horizon)])


def generate():
    rng=np.random.default_rng(21);t=np.arange(900);noise=np.zeros(900)
    for i in range(1,900):noise[i]=.6*noise[i-1]+rng.normal(0,1.5)
    trend=40+.018*t;season=5*np.sin(2*np.pi*t/7)+3*np.sin(2*np.pi*t/365)
    shift=6*(t>=820)
    return trend+season+noise+shift,trend,season,noise


def features(history,t):
    return np.r_[history[-28:],t/900,np.sin(2*np.pi*t/7),np.cos(2*np.pi*t/7),
                 np.sin(2*np.pi*t/365),np.cos(2*np.pi*t/365)]


def holt_winters(history,horizon=7):
    alpha,beta,gamma=.25,.03,.2;m=7
    level=np.mean(history[:m]);trend=(np.mean(history[m:2*m])-level)/m
    season=history[:m]-level
    for t in range(m,len(history)):
        old_level=level;slot=t%m;old_season=season[slot]
        level=alpha*(history[t]-old_season)+(1-alpha)*(level+trend)
        trend=beta*(level-old_level)+(1-beta)*trend
        season[slot]=gamma*(history[t]-level)+(1-gamma)*old_season
    return np.array([level+h*trend+season[(len(history)+h-1)%m] for h in range(1,horizon+1)])


def arima110(history,horizon=7):
    differenced=np.diff(history)
    # Conditional least squares for an AR(1) model of first differences.
    design=np.column_stack([np.ones(len(differenced)-1),differenced[:-1]])
    constant,phi=np.linalg.lstsq(design,differenced[1:],rcond=None)[0]
    value=history[-1];delta=differenced[-1];out=[]
    for _ in range(horizon):
        delta=constant+phi*delta;value+=delta;out.append(value)
    return np.asarray(out)


class DirectGRU(nn.Module):
    def __init__(self):
        super().__init__();self.recurrent=nn.GRU(1,16,batch_first=True);self.output=nn.Linear(16,7)
    def forward(self,x):
        _,hidden=self.recurrent(x);return self.output(hidden[-1])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def text(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    y,trend,season,noise=generate();torch.manual_seed(21)
    train_end,selection_end,calibration_end=500,600,700
    train_ids=np.arange(28,train_end)
    xx=np.array([features(y[:i],i) for i in train_ids]);yy=y[train_ids]
    scaler=StandardScaler().fit(xx);ridge=Ridge(alpha=10).fit(scaler.transform(xx),yy)
    mean,std=y[:train_end].mean(),y[:train_end].std()
    def windows(origins):
        a=np.array([(y[o-28:o]-mean)/std for o in origins],dtype=np.float32)[:,:,None]
        b=np.array([(y[o:o+7]-mean)/std for o in origins],dtype=np.float32)
        return torch.tensor(a),torch.tensor(b)
    train_origins=np.arange(28,train_end-6);select_origins=np.arange(train_end,selection_end-6,7)
    tx,ty=windows(train_origins);vx,vy=windows(select_origins)
    model=DirectGRU();optimizer=torch.optim.Adam(model.parameters(),lr=.005)
    trace=[];best=float('inf')
    for epoch in range(45):
        model.train();losses=[]
        for ids in torch.randperm(len(tx)).split(64):
            optimizer.zero_grad();loss=nn.functional.mse_loss(model(tx[ids]),ty[ids]);loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad():val=nn.functional.mse_loss(model(vx),vy).item()
        trace.append([float(np.mean(losses)),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    methods=['Naive','Seasonal naive','Holt-Winters','ARIMA(1,1,0)','Ridge','GRU']
    def forecast(origin,method):
        history=y[:origin].copy()
        if method=='Naive':return np.full(7,history[-1])
        if method=='Seasonal naive':return seasonal_naive(history)
        if method=='Holt-Winters':return holt_winters(history)
        if method=='ARIMA(1,1,0)':return arima110(history)
        if method=='Ridge':
            out=[]
            for t in range(origin,origin+7):
                prediction=float(ridge.predict(scaler.transform(features(history,t)[None]))[0]);out.append(prediction);history=np.r_[history,prediction]
            return np.array(out)
        with torch.no_grad():return model(torch.tensor(((history[-28:]-mean)/std).astype(np.float32))[None,:,None]).numpy()[0]*std+mean
    calibration_origins=np.arange(selection_end,calibration_end-6,7)
    test_origins=np.arange(calibration_end,len(y)-6,7)
    target=np.array([y[o:o+7] for o in test_origins]);predictions={m:np.array([forecast(o,m) for o in test_origins]) for m in methods}
    calibration_error=np.abs(np.array([forecast(o,'Ridge')-y[o:o+7] for o in calibration_origins])).ravel()
    rank=min(len(calibration_error),int(np.ceil((len(calibration_error)+1)*.9)))
    radius=float(np.sort(calibration_error)[rank-1])
    lower=predictions['Ridge']-radius;upper=predictions['Ridge']+radius
    covered=(target>=lower)&(target<=upper)
    times=test_origins[:,None]+np.arange(7)[None]
    before=times<820;after=~before
    summary={'test_origins':len(test_origins),'forecast_horizon':7,'test_forecasts':target.size,
             'mae':{m:float(np.mean(np.abs(predictions[m]-target))) for m in methods},
             'mae_by_horizon':{m:np.mean(np.abs(predictions[m]-target),axis=0).tolist() for m in methods},
             'ridge_interval_radius':radius,'coverage':float(covered.mean()),
             'coverage_before_shift':float(covered[before].mean()),'coverage_after_shift':float(covered[after].mean()),
             'gru_selected_epoch':int(np.argmin(np.array(trace)[:,1])+1),
             'latest_training_target':int(train_origins[-1]+6),'first_selection_origin':int(select_origins[0]),
             'latest_calibration_target':int(calibration_origins[-1]+6),'first_test_origin':int(test_origins[0]),
             'seasonal_hand_forecast':seasonal_naive(np.tile(np.arange(1,8),3)).tolist(),
             'arima_constant_increment_forecast':arima110(np.arange(30,dtype=float)).tolist()}
    assert summary['latest_training_target']<summary['first_selection_origin']
    assert summary['latest_calibration_target']<summary['first_test_origin']
    assert np.allclose(arima110(np.arange(30,dtype=float)),np.arange(30,37))
    assert np.array_equal(forecast(700,'Seasonal naive'),y[693:700])
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',series=y,trend=trend,season=season,noise=noise,
             train_trace=trace,test_origins=test_origins,targets=target,interval_lower=lower,
             interval_upper=upper,calibration_errors=calibration_error,**{m.replace(' ','_'):p for m,p in predictions.items()})
    colors=['#8c9196','#b38b31','#328679','#8d64a6','#176b91','#bd554c']
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,1,height_ratios=[2,1]);ax=fig.add_subplot(gs[0])
    ax.plot(y,color='#476170',lw=.8)
    for a,b,c,l in [(0,500,'#d9e9ef',text('训练','Train')),(500,600,'#f6e9ca',text('模型选择','Selection')),(600,700,'#e3dfed',text('区间校准','Calibration')),(700,900,'#e0eadc',text('测试','Test'))]:
        ax.axvspan(a,b,color=c,alpha=.5);ax.text((a+b)/2,75,l,ha='center')
    ax.axvline(820,color='#bd554c',ls='--');ax.set(xlabel=text('日索引','Day index'),ylabel=text('需求 / 量单位','Demand / quantity units'),ylim=(25,80))
    ax=fig.add_subplot(gs[1]);start=80;ax.plot(np.arange(start,start+56),y[start:start+56]-trend[start:start+56],color='#176b91',label=text('去已知趋势的观测','Observation minus known trend'))
    ax.plot(np.arange(start,start+56),season[start:start+56],color='#bd554c',label=text('生成的季节分量','Generated seasonal component'))
    ax.set(xlabel=text('日索引','Day index'),ylabel=text('偏离 / 量单位','Deviation / quantity units'));ax.legend(ncol=2,fontsize=9)
    fig.tight_layout();save(fig,'timeline')
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,2,width_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,0]);ax.plot(times.ravel(),target.ravel(),color='#333',lw=1,label=text('真实观测','Observed'))
    ax.plot(times.ravel(),predictions['Ridge'].ravel(),color='#176b91',lw=1,label='Ridge')
    ax.fill_between(times.ravel(),lower.ravel(),upper.ravel(),color='#176b91',alpha=.15,label=text('校准区间','Calibrated interval'))
    ax.axvline(820,color='#bd554c',ls='--');ax.set(xlabel=text('日索引','Day index'),ylabel=text('需求','Demand'));ax.legend(ncol=3,fontsize=8)
    ax=fig.add_subplot(gs[1,0]);errors=np.abs(predictions['Ridge']-target)
    im=ax.imshow(errors.T,aspect='auto',origin='lower',cmap='magma',extent=[test_origins[0]-3.5,test_origins[-1]+3.5,.5,7.5])
    ax.set(xlabel=text('滚动预测起点（日）','Rolling origin (day)'),ylabel=text('预测步长（日）','Horizon (days)'),yticks=range(1,8));fig.colorbar(im,ax=ax,label=text('绝对误差','Absolute error'))
    ax=fig.add_subplot(gs[:,1]);
    method_labels={'Naive':text('朴素','Naive'),'Seasonal naive':text('季节朴素','Seasonal naive')}
    for m,c in zip(methods,colors):ax.plot(range(1,8),summary['mae_by_horizon'][m],'o-',label=method_labels.get(m,m),color=c,ms=4)
    ax.set(xlabel=text('预测步长（日）','Horizon (days)'),ylabel=text('MAE / 量单位','MAE / quantity units'),xticks=range(1,8));ax.legend(fontsize=9)
    fig.tight_layout();save(fig,'backtest')
    fig,axs=plt.subplots(1,3,figsize=(12,3.8),gridspec_kw={'width_ratios':[1.2,1,1]})
    trace=np.array(trace);axs[0].plot(range(1,46),trace[:,0],label=text('训练','Train'),color='#176b91');axs[0].plot(range(1,46),trace[:,1],label=text('选择窗口','Selection window'),color='#bd554c')
    axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('标准化均方误差','Standardized MSE'),title='GRU');axs[0].legend()
    axs[1].hist(calibration_error,bins=15,color='#176b91',alpha=.8);axs[1].axvline(radius,color='#bd554c',ls='--')
    axs[1].set(xlabel=text('校准绝对残差','Calibration absolute residual'),ylabel=text('预测数','Forecast count'),title=text(f'区间半宽 {radius:.2f}',f'Interval radius {radius:.2f}'))
    vals=[summary['coverage_before_shift'],summary['coverage_after_shift']]
    axs[2].bar([0,1],vals,color=['#176b91','#bd554c']);axs[2].axhline(.9,color='#888',ls='--')
    axs[2].set(xticks=[0,1],xticklabels=[text('变化前','Before shift'),text('变化后','After shift')],ylim=(0,1),ylabel=text('区间覆盖率','Interval coverage'))
    fig.tight_layout();save(fig,'uncertainty')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

196 个测试预测值上的平均绝对误差依次为：朴素 4.9229，季节朴素 1.9687，固定系数加法 Holt–Winters 1.8597，非季节 ARIMA(1,1,0) 4.7632，Ridge 2.6424，GRU 5.8398。误差单位与需求相同。Holt–Winters 在这组设置中得分最低，强周规律使季节朴素也成为有竞争力的基线。ARIMA 的这个简化配置没有季节项，GRU 的固定训练与输入方式也未能适应后段水平；这些结果回答具体配置下的问题，并为接下来该改什么提供方向。

![28 个测试起点各预测七天。左上为 Ridge 预测、真值与固定校准区间，左下为起点×步长的绝对误差，右侧为六种方法按步长的 MAE。每个起点相隔七天，因此步长也对应固定周内位置。](https://ml-biomat.com/static/tutorials/machine-learning/figures/99e87635127eb606ab998222.svg?v=99e87635127e)

图 228 个测试起点各预测七天。左上为 Ridge 预测、真值与固定校准区间，左下为起点×步长的绝对误差，右侧为六种方法按步长的 MAE。每个起点相隔七天，因此步长也对应固定周内位置。

阅读图时先看预测起点和步长，再看颜色。左上将每次七日预测接成一条时间曲线，阴影是校准区间；左下把每个起点、每个步长的绝对误差展开成热图；右侧分别统计未来第一天到第七天的 MAE。测试起点每次相隔七天，因此各步长对应固定的周内位置，曲线起伏也与季节相位有关。不要把它误读为“误差必然随步长单调增加”。把起点改为每天移动，则会在各步长中混合更多不同的周内位置。

![GRU 训练与选择误差、98 个校准残差及区间半宽、水平变化前后的实际覆盖率。90% 是目标水平，柱高为测试观测统计；两者分别表示设定与结果。](https://ml-biomat.com/static/tutorials/machine-learning/figures/9aca71cdbe2ec8d5e86fbf80.svg?v=9aca71cdbe2e)

图 3GRU 训练与选择误差、98 个校准残差及区间半宽、水平变化前后的实际覆盖率。90% 是目标水平，柱高为测试观测统计；两者分别表示设定与结果。

代码中的简单检查也有明确含义。严格递增的 0 到 29 输入给 ARIMA(1,1,0)，应延续为 30 到 36；重复三次的 1 到 7 输入给季节朴素，应再次给出 1 到 7。训练最后一个目标索引为 499，模型选择第一个起点是 500；校准最后一个目标是 697，测试第一个起点是 700。这些边界检查与最终误差一起保存，使“没有使用未来”可以对应到实际窗口，而不只是一句原则。

## 把预测起点推到变化的前后

这条可手算的序列由基础水平 20、每周偏移 [0,2,4,3,1,−1,−2]、线性趋势和第 42 天的水平变化组成。每次预测只读起点之前的观测。先隐藏未来作出预测，再显示真值，比较季节朴素如何在一周后适应变化。

[Figure: 预测起点、历史窗口、预测和可显示的真值](https://ml-biomat.com/tutorials/machine-learning/m21/#M21-svg)

## 8. 当邻站影响你，当规律本身发生变化

时间序列经常同时具有空间结构。上游道路的拥堵会影响下游路段，相邻气象站共享天气过程，多台设备可能受到同一供电波动影响。可以先用滞后的邻站观测作为外生特征，再用图网络聚合空间关系、用时间模型描述演化。若邻站数据有传输延迟，应使用预测时实际收到的版本。对多门店、多层级需求，独立预测还可能出现总量与各分项之和不一致，需要协调预测，使输出符合业务或守恒约束。

异常点和变化点也应分开。一次传感器尖峰可能是瞬时错误，一段持续抬高的均值则可能表示运行机制变了。异常检测可以比较当前观测与只用过去建立的预测区间；变化点检测关心均值、方差或动态参数是否持续改变。在线累计残差、窗口分布比较和离线分段各有不同延迟与假设。检测到变化后，合理动作可能是核对传感器、缩短训练窗口、更新状态或重训模型，具体取决于变化来自测量系统还是被观察对象。

一次好的时序研究，最终应交付可重放的预测档案：每次何时发出预测、使用哪个模型版本、历史截止在哪里、预测了哪些时点、区间怎样校准、真值何时补齐。将误差与预测步长、季节位置和变化条件联系起来，才能判断模型应继续使用还是需要调整。时间序列学习的核心不是找一条最贴合已有曲线的线，而是让每一次面向未来的计算，都站在当时真正拥有的信息上。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M21.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Forecasting: Principles and Practice — forecasting tools](https://otexts.com/fpp3/toolbox.html)

   朴素方法与滚动预测起点的开放教材。
2. [Forecasting: Principles and Practice — exponential smoothing](https://otexts.com/fpp3/exponential-smoothing.html)

   平滑、趋势、季节与状态空间形式。
3. [Forecasting: Principles and Practice — ARIMA](https://otexts.com/fpp3/arima.html)

   差分、创新与季节 ARIMA。
4. [Chronos: Learning the Language of Time Series](https://arxiv.org/abs/2403.07815)

   缩放、量化与概率预测的原始论文。
5. [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688)

   TimesFM 原始论文的分块解码器设计。
