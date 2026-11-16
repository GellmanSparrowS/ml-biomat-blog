# 让预测值得使用：不确定性、可靠性与隐私

Source: https://ml-biomat.com/tutorials/machine-learning/m39/
Language: zh-CN

从“有多大把握”走到“在哪些条件下仍能工作”，用实际概率、预测集合、扰动与分布变化检查模型。

## 1. 从“答对多少”走到“怎样使用答案”

同样是读出一张快递单上的数字，模型说“这是8，概率0.51”和“这是8，概率0.99”，后续操作可以很不一样：前者交给人重新看一眼，后者直接进入分拣流程。如果这两个概率与真实正确率没有对应关系，界面上的小数点再多也帮不了忙。模型还会遇到新的相机、倾斜的纸张和不同人的笔迹；这些变化是否影响结论，需要另做实验。可靠性因此关心一整条使用链：预测怎样表达把握，系统怎样处理含糊对象，哪些输入变化会让它出错，以及训练和发布过程中如何保护数据。

概率预测在深度学习之前已经用于天气预报。预报十次“降雨概率80%”，可以等待足够多类似预报，检查其中下雨的比例是否接近八成。这种把语言中的把握变成长期频率的思路，也适用于机器分类；只是分类任务还多了一层选择：我们常常只显示概率最大的那个答案。2017年Guo等人研究现代神经网络的校准问题，把一个容易被准确率掩盖的现象推到前台：模型更会分类，并不自动意味着输出的概率更贴近实际频率。理解这段方法史的关键，是把“排出最可能类别”和“给出可信概率”看作两个可分别测量的问题。

本章用公开的8×8手写数字完成一条连续实验。1797张图片随机分成900张训练、150张调温、150张共形校准和597张测试；每张图片只进入其中一组。训练集学习识别方法，调温集调整概率的陡峭程度，共形集决定预测集合阈值，测试集负责最后观察。除此之外，用已知生成过程的曲线区分两类不确定性，用两家虚拟客户端理解联邦更新，并用公开合成数值观察隐私噪声。这样，每种方法回答的对象都能对应到具体数据和计算。

## 2. 看不清的数据，与还没学会的模型

把同一支温度计放在相同环境中读数，多次结果可能仍有微小波动；增加训练样本能帮助估计波动范围，却不会消除这支仪器的测量噪声。另一种情况是模型只看过0到30摄氏度的记录，突然需要预测零下环境：这时的问题来自知识覆盖不足。前一种通常称为数据不确定性或偶然不确定性，后一种称为模型不确定性或认知不确定性。这种区分取决于输入信息和任务设定。如果增加一项原来没有记录的环境变量，一部分看似随机的波动可能变得可以解释，所以“数据噪声”也需要说明是在什么信息条件下定义的。

Kendall与Gal在2017年的研究中把这两类不确定性放到深度视觉模型的共同框架下。本章用更小的回归实验看它们的区别：在输入−3到3之间生成100个点，平均结果沿正弦曲线变化，噪声标准差为0.1加上输入绝对值的0.12倍。因此，中间区域比较平稳，两端更嘈杂。五个神经网络分别使用有放回抽样的训练点和不同初始参数，每个网络同时输出一个均值和一个正方差；通过高斯负对数似然训练，既学习曲线，也学习不同位置的波动大小。

$$
\widehat{\operatorname{Var}}(Y\mid x)=\frac1M\sum_{m=1}^M\sigma_m^2(x)+\frac1M\sum_{m=1}^M[\mu_m(x)-\bar\mu(x)]^2,\quad\bar\mu=\frac1M\sum_m\mu_m
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5eab15f1c4638adc5f25a660.svg) | 输入与结果随机变量；输入按特征计量，结果用y单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b0f36d3188e052b14d52a5a7.svg) | 模型索引、模型数、每模型预测均值与方差；后两者为y单位与y单位平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/53ee4b0d1216901fe0bb79f8.svg) | 集成平均预测与混合分布方差；分别为y单位与其平方。 |

把模型等权看作M个条件分布，用全方差公式分解。两模型均值1和3、噪声方差均为0.25，平均均值2，均值方差1，总方差1.25。这里分母M对应等权混合，非无偏样本方差估计。

这条公式可以想成五位观察者各自带来一个预测分布。即使五个人的中心判断相同，每个人认为结果本身仍会波动，混合后的分布就有宽度；如果他们的中心判断也不一样，混合分布会进一步变宽。第一项是各模型预测的噪声方差平均值，第二项是中心判断之间的差异。本例把五个网络等权混合，因此分母是五；这些网络组成了可计算的近似分布，并没有通过五次训练得到完整的贝叶斯后验。改变网络结构、先验约束或训练数据，都可能改变模型间的分歧。

![五个异方差回归网络分别输出均值与噪声方差，训练点100个。左图蓝带是均值±1.96倍总标准差；右图分开画模型均值分歧、平均预测噪声与已知生成噪声。竖线标出训练输入范围。](https://ml-biomat.com/static/tutorials/machine-learning/figures/33a94aa58c24e9d39457d433.svg?v=33a94aa58c24)

图 1五个异方差回归网络分别输出均值与噪声方差，训练点100个。左图蓝带是均值±1.96倍总标准差；右图分开画模型均值分歧、平均预测噪声与已知生成噪声。竖线标出训练输入范围。

读图时先找两条标出−3和3的竖线：线内有训练观测，线外只有模型延伸出来的预测。接近输入4处，平均预测噪声方差约1.70，模型均值方差约0.057；而按合成规则，该处真实噪声方差约0.34。几个网络把陌生区域的一部分失配记进了预测噪声，说明“模型给出的分解”和“生成过程中的真实分解”需要分别看。左侧均值加减1.96倍总标准差只是依据前两阶矩画出的带状摘要；混合分布的形状和外推误差会影响它的实际覆盖。下一步的共形方法将直接用独立残差校准覆盖，与这里回答的问题有所不同。

## 3. 让九成把握对应大约九成正确

神经网络最后通常先输出一组logit，也就是未经归一化的类别分数，再用softmax变成概率。若所有分数同时放大，最大的类别仍是原来那个，概率却会更接近0和1。本例有意把已经训练好的分数乘2.5，构造一个可控制的过度自信情形，然后只用150张调温图片拟合一个正数温度。这样能清楚地看到：概率发生改变时，分类能力是否真的改变。温度越大，分数差异被压缩，概率通常越平缓；它调节的是同一组类别分数的尺度。

$$
p_j(x;T)=\frac{\exp(z_j(x)/T)}{\sum_{k=1}^{K}\exp(z_k(x)/T)},\qquad T>0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39a8252b6cee9c681e60c71c.svg) | 输入、类别j的logit、类别数、目标类别与求和类别索引；logit为无量纲分数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a94cd21cc54c4257a0be4fe2.svg) | 正温度与类别概率，均无量纲。 |

所有分数同除正数，排序不变。二分类分数(2,0)，T=1时第一类概率约0.881；T=2时约0.731。独立调温集最小化负对数似然来选择T。

实际拟合得到温度约2.2075。597张测试图片的分类准确率在校准前后都是92.13%，改变最大概率的类别数为零；负对数似然则从约0.258降到0.195。负对数似然关注真实类别获得了多少概率，尤其会惩罚非常自信的错误，因此它能捕捉准确率没有显示的改善。温度参数从独立调温集获得，测试数据只用于观察；如果反复看测试结果来选择校准方案，就会把最终考场变成另一套训练材料。

$$
\operatorname{ECE}=\sum_{b=1}^B\frac{n_b}{N}\left|a_b-c_b\right|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/437425f90c982ec6174f0461.svg) | 置信箱索引、总箱数、箱内样本数与总测试样本数；均为计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f7a162fbcad799200a452030.svg) | 箱内正确率、平均最大预测概率与加权绝对差，均无量纲。 |

两个等大箱分别平均信心0.6/0.9、实际正确率0.5/0.8，则ECE=0.5×0.1+0.5×0.1=0.1。分箱规则与样本数会改变估计；空箱不参与加权。

可靠性图把最大预测概率落在相近范围的对象放进一箱，横轴是箱内平均信心，纵轴是箱内实际正确率。点落在对角线下方，表示模型说得比做得更有把握；上方则相反。这里用十个等宽箱，期望校准误差ECE从约0.0513降到0.0193。这个数适合与图一起读：同样的误差可能来自一个大箱的小偏差，也可能来自一个很小箱的大偏差；换一套分箱，数值也会变化。因此代码同时保留每箱人数、平均信心和正确率，让读者能看见平均数怎样形成。

![597张测试数字的最大类别概率校准图、置信度分布与选择性预测曲线。温度只在另外150张图片上拟合；右图的点旁数字是保留预测的概率门槛。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5fffb79cc50f90fef03e6402.svg?v=5fffb79cc50f)

图 2597张测试数字的最大类别概率校准图、置信度分布与选择性预测曲线。温度只在另外150张图片上拟合；右图的点旁数字是保留预测的概率门槛。

概率还会连接到工作量。若只接受最大概率至少0.9的预测，本次保留471张，占测试集78.89%，其中错误率约0.64%；其余126张转交复核。把门槛提高到0.99后，只保留308张，本次其中没有错误。这里的零来自这308个对象的实际计数，部署时仍要持续累积新对象的错误记录。实际阈值应结合误判代价、漏判代价和复核容量，在独立验证对象上确定；“概率越高越好”没有说明被拒绝的对象由谁处理。

![逻辑回归、SVC、保序和Sigmoid校准的可靠性曲线及概率直方图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/26cd6d1fa2a0abb04db43ef7.png?v=26cd6d1fa2a0)

图 3scikit-learn官方校准示例原图：二分类正类概率与实际正类比例的对应，下面的直方图显示概率分布。此图讨论正类概率，本章数字实验讨论最大类别概率与分类正确率。scikit-learn贡献者，BSD-3-Clause许可，未改编。

官方原图提供了另一个角度。它画的是二分类正类概率与正类实际比例，而本章数字图画的是十分类最大概率与分类正确率；两者的纵轴含义不同，读图前先确认正在校准哪个事件。Sigmoid校准拟合一个平滑映射，保序回归拟合单调的阶梯关系，温度缩放则保留多分类logit排序并只拟合一个尺度。独立校准数据较少时，参数少的映射较容易稳定；数据充足且失真形状复杂时，较灵活的映射有机会拟合更细的关系。它们共同需要一个与实际使用环境相符的校准样本。

## 4. 用一个集合表达哪些答案还值得保留

有时最有用的输出是一组候选。例如字迹含糊的快递单可以交给操作员“3或8”，连续量可以给出一段范围。共形预测把这种输出与一个有限样本的排序计算连接起来：先固定模型，再找一组没有参与拟合的校准对象，记录模型在真实答案上的不符合程度。新对象若要被视为同类情形，其真实答案的分数也应与这些校准分数放在一起比较。二十世纪末以来发展的共形方法，把统计覆盖问题转化为可交换分数的秩；Angelopoulos与Bates的教程展示了这一思路怎样接到多种现代预测模型后面。

$$
s_i=1-p_{y_i}(x_i),\quad k=\lceil(n+1)(1-\alpha)\rceil,\quad q=s_{(k)},\quad C(x)=\{j:1-p_j(x)\le q\}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d00d1d454d62db2557ded6e9.svg) | 共形校准对象索引、样本数、输入、真实标签与固定模型的类别j概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/82d95afabbbe1d8f61b7227b.svg) | 真实类别不符合度、升序第k分数与从1开始的秩；分数无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c82e35d09cd7e769da2ba9d9.svg) | 目标错误率、阈值、预测标签集合与类别索引；概率无量纲，集合大小为类别数。 |

n=150、α=0.1时k=136。本例q约0.4324，因此概率至少约0.5676的类别入选。若k=n+1，用q=∞。在模型固定、校准对象与新对象分数可交换时，新分数在n+1个位置的秩给出至少1−α的边际覆盖；并列采用≤使覆盖更保守。

本例的不符合度是“一减去真实类别概率”：真实类别概率越低，分数越大。150个共形校准分数排序后，目标错误率0.1对应第136个位置，而不是随手取某个软件默认的90%分位插值。多出来的那个位置留给新对象。若校准分数与新分数可交换，可以把新对象的秩想成在151个位置上均匀落点；取足够靠后的阈值，就把漏掉真实答案的概率控制在设定水平。这是对校准样本和新对象随机性的边际覆盖结论，并没有要求每一幅图片、每一个类别或每一种清晰度都有相同覆盖。

实际阈值约0.4324，等价于保留概率至少0.5676的类别。因为这个门槛高于一半，本次每个集合至多含一个类别：597张测试图片中有27张空集合，其余是单元素集合，平均大小约0.955；真实类别被包含的比例为90.45%。空集合在这里表达“没有任何类别达到这条统一门槛”。如果任务希望含糊图片得到多个候选，可以改用按类别概率累积构造的分数，再在独立校准集上重新确定阈值；分数选择影响集合效率，秩计算提供覆盖依据。

## 让校准秩变成可见的区间

左侧九个校准绝对残差固定不动；右侧十个教学对象显示预测区间与真实结果。降低目标错误率会扩宽区间；增加新数据偏移只移动右侧真实结果。交互中的有限样本覆盖直接计数，理论边际覆盖来自重复抽样中的可交换性。

[Figure: 校准分数排序与新样本预测区间](https://ml-biomat.com/tutorials/machine-learning/m39/#M39-plot)

交互把相同的秩逻辑放到回归残差上。九个校准绝对残差从小到大排列，目标错误率0.2时取第八个残差0.6，预测区间宽度就是1.2。改变右边新对象的结果偏移，会使更多真实点离开区间，左边的旧校准残差却保持不动。这个操作同时说明了两件事：覆盖可以通过“落在区间内的点数”直接数出来，而旧环境的排序关系需要新环境仍满足相应的可交换性。想让范围适应新的噪声水平，应收集相符的校准对象或采用有明确假设的加权、分组等扩展。

## 5. 换一台相机，原来的把握还在吗

数据分布变化可以发生在不同环节。输入外观改变，标签比例改变，或相同输入与结果之间的关系改变，需要不同的检查方法。把所有变化都称为“OOD”容易漏掉关键条件：医院换了扫描仪，既可能改变像素统计，也可能改变哪些人进入数据库；一类过去少见的病变变多，又会改变类别比例。先写清训练环境、预期使用环境与变化机制，才能选择重新校准、重加权、补采样或重新训练。若变化已影响真实标签的定义，也需要重新整理任务本身。

本例把597张测试图像旋转30°，保持8×8画布，使用线性插值并用零填充边缘。这个操作同时改变方向、局部像素和边缘内容，是一个具体的图像变化测试。沿用原来的模型、温度和共形阈值后，分类准确率降到49.08%，预测集合覆盖降到41.54%。这不是给旧集合再加一个固定百分比就能修复的问题：校准分数来自原图，而新输入已经系统地离开了原来的条件。图中同时列出集合大小，帮助判断模型是在变得含糊，还是仍然对错误类别给出很高概率。

![原图与旋转30°后的预测集合覆盖和大小；右侧按训练集墨迹阈值划分测试图像。所有情形沿用同一个共形阈值，虚线表示设定的90%边际覆盖目标。](https://ml-biomat.com/static/tutorials/machine-learning/figures/58eb67c7a269a31b84011b98.svg?v=58eb67c7a269)

图 4原图与旋转30°后的预测集合覆盖和大小；右侧按训练集墨迹阈值划分测试图像。所有情形沿用同一个共形阈值，虚线表示设定的90%边际覆盖目标。

还可以把“一减最大类别概率”当作异常分数，区分原图与旋转图。本次两组的AUROC约0.844，说明这个简单分数具有区分能力，却仍存在重叠。确定告警阈值还需要指定允许的误报率，再检查会漏掉哪些变化。一个检测器对旋转敏感，并不意味着它也能识别错误标签、陌生类别或轻微模糊；这些变化进入不同的测试组。保留正常对象与变化对象的成对关系，也有助于直接观察某个对象怎样从正确、低信心变成错误、高信心。

## 6. 随机噪声与朝着错误方向的扰动

随机抖动通常没有特定目标，对抗扰动则选择最容易增加损失的方向。Goodfellow等人的FGSM方法用一阶近似给出一个非常直观的计算：把输入看作64个可微坐标，求损失对每个像素的梯度，再把每个像素朝损失增加的方向移动相同幅度。即使每个坐标变化不大，许多坐标合起来也可能明显改变最终分数。这段历史提醒我们，高维模型的可靠性不能只靠肉眼判断“两张图看起来差不多”，还需要明确允许怎样改变输入以及用什么方式寻找变化。

$$
x_{\rm adv}=\operatorname{clip}_{[0,1]}\!\left(x+\epsilon\operatorname{sign}\nabla_x\ell(f_\theta(x),y)\right),\quad\|x_{\rm adv}-x\|_\infty\le\epsilon
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a1941f9cd259ed6c94c9c2b7.svg) | 原输入、扰动输入、固定模型参数、预测模型与真实标签。本例输入为64维0–1像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/51e7596ee37a2ca79a5c442d.svg) | 交叉熵损失、对输入求梯度与逐元素取符号；损失无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d2e0462cdaf8f016404392f2.svg) | 像素扰动上限、裁切到合法范围与最大绝对分量范数；ε为归一化像素单位。 |

像素(0.2,0.95)、梯度符号(+1,+1)、ε=0.1，得到(0.3,1.0)，真实变化(0.1,0.05)。对梯度线性近似，逐坐标取同号端点使允许方盒内损失增加最大。

扰动预算0.1指的是归一化到0至1之后，每个像素最多改变0.1。公式最后的裁切保留合法像素范围，真实差值图用−0.1到0.1的色标显示，所以视觉上放大的红蓝颜色并没有被当作原图强度。标准训练模型在原图上的准确率约92.13%，预算0.1的FGSM输入下约51.42%。第二个模型每个训练批次同时学习干净样本和预算0.1的FGSM样本，两部分交叉熵各占一半；对抗训练模型在干净测试图片上的准确率约91.12%，在预算0.1的新攻击下约70.35%；测试时分别针对两个模型重新计算梯度。

![同一8×8数字的原图、FGSM扰动图与实际像素差，颜色范围分别为0–1与−0.1到0.1。右图对每个模型分别重新求梯度，比较相同扰动预算下的白盒FGSM准确率。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d87c3f6a1d1a641334f0cb84.svg?v=d87c3f6a1d1a)

图 5同一8×8数字的原图、FGSM扰动图与实际像素差，颜色范围分别为0–1与−0.1到0.1。右图对每个模型分别重新求梯度，比较相同扰动预算下的白盒FGSM准确率。

这一步“重新计算”很要紧：对标准模型构造的攻击输入，换到另一个模型上可能已经不是同样有效的方向。比较防护方法时，应给每个方法相同的扰动集合、同类攻击计算预算，并进一步检查多步攻击和不同初值下的结果。当前曲线显示的是一次FGSM测试，不是对整个扰动盒中所有输入求出的最坏情形。经过认证的鲁棒半径回答的是另一个计算问题，例如用可证明的界或随机平滑条件建立保证；使用时需要同时说明所保护的距离度量和适用概率。

训练数据受到污染又是另一条路径。代码随机选择900个训练标签中的90个，把类别编号循环加一，再以相同初始化和训练规则拟合第三个模型；随后仍在干净测试图像上评价。这个模型的干净测试准确率为92.80%，原模型为92.13%；本次有限样本中，标签污染没有降低整体准确率。进一步比较可以增加随机种子并检查具体类别和目标对象，把训练数据质量与某一次总体分数分开观察。现实中的投毒可能选择特定对象或植入触发图案，评价时需要同时记录干净性能、目标对象的错误变化和污染比例。数据版本、标签审查、重复样本与异常更新检查，都对应这些具体入口；单靠在输入图片上加噪声，处理不了训练标签已经被改动的问题。

## 7. 平均表现怎样落到不同人和不同对象身上

全体对象的准确率可能很好，某一组却持续承担更多错误。本章按训练集平均像素强度的中位数，把测试图像分成较少墨迹与较多墨迹两组；阈值在看测试结果前固定。两组分别有280和317张，覆盖率约91.79%与89.27%。这是图像质量分层，帮助看清总体90.45%的覆盖由哪些对象组成。组的定义、人数和实际任务含义要一起报告：数字图像的亮度分层回答不了招聘、借贷或服务分配中的群体公平问题。

$$
\operatorname{TPR}_g=\frac{TP_g}{TP_g+FN_g},\qquad\operatorname{FPR}_g=\frac{FP_g}{FP_g+TN_g}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/983459c66fab7d802fbf231f.svg) | 组索引与该组真正例、假负例、假正例、真负例计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/852109845d67c334953178b1.svg) | 真实正例中的检出率与真实负例中的误报率，均无量纲；各分母须非零。 |

某组20个真实正例中识别16个，80个真实负例中误报8个，则TPR=0.8、FPR=0.1。另一组须按自己的真实正负例计数作分母，不能拿组总人数代替。

在一个有明确正类的二分类决策中，人口统计均等比较各组被选中的比例；机会均等比较真实正例中的检出率；等化赔率同时比较检出率和误报率。三者分母不同，表达的目标也不同。例如两组真实正例比例不同，即使它们的检出率和误报率一样，最终被选中的比例仍可能不同。选择指标应从决策的后果出发：谁承担漏判损失，谁承担误报损失，标签本身怎样形成，以及需要满足哪些制度要求。把多个指标同时列出，可以帮助发现张力，但不会自动替代对任务目标的判断。

分组评价还需要看到小样本的不稳定。十个人里多错一个，错误率就跳十个百分点；把相互交叉的属性拆得很细，可能产生许多这样的小组。可以同时提供样本数、区间与跨时间结果，并在标签获取有偏时检查缺失机制。数据治理由此进入模型流程：明确哪些数据可以用于哪个目标，保留标签与版本的变更关系，落实访问和保留规则，并为撤回或纠错建立更新路径。这些工作让“同一套评价”在模型迭代后仍有可比较的含义，也为隐私方法确定需要保护的记录单位。

## 8. 少让一条记录左右发布结果

一个统计量只包含平均值，也可能暴露个体。例如已经知道九十九个人的数据，再知道一百个人的精确总和，就能推回最后一人。差分隐私因此不只看输出是否带姓名，而是比较两份仅相差一条记录的数据：观察同一个发布结果时，两种世界的概率应保持接近。Dwork与Roth的专著把这个要求写成可组合的数学定义，使“保护程度”能跟随机机制和多次发布放在一起计算。本章采用固定人数、替换一条记录的相邻关系，先把保护单位说清楚。

$$
\Pr[\mathcal M(D)\in S]\le e^\epsilon\Pr[\mathcal M(D^\prime)\in S]+\delta
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a5e0799435269c7929f194f6.svg) | 相邻数据集，本章约定固定人数且仅替换一条记录。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be63aeac331eaa36afb23131.svg) | 随机发布机制、任意输出事件集合及对机制随机性的概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24a3eb098ec2e963fece6ef7.svg) | 非负无量纲隐私参数：概率比的指数界与加性松弛。 |

这条不等式要对所有相邻数据和输出事件成立。ε=ln2、δ=0时，一侧某事件概率0.1，另一侧至多0.2；交换相邻数据也须满足。δ是概率界的加性项，不能直接解释为个人泄露概率。

对于预先限制在0到1之间的100个数，替换一条记录最多让总和改变1，让均值改变0.01。这个最大变化叫敏感度；Laplace机制按敏感度与隐私参数的比值添加噪声。噪声不是任意选一个看起来够乱的量，而是由输入边界、记录数、相邻关系和目标参数共同决定。若把数据边界从0到1改为0到100，敏感度也扩大一百倍；若边界本身来自未经保护的私有数据探索，这一步也需要纳入发布机制的分析。

$$
\widetilde\mu=\frac1n\sum_{i=1}^{n}\operatorname{clip}_{[a,b]}(x_i)+Z,\quad\Delta=\frac{b-a}{n},\quad Z\sim\operatorname{Laplace}(0,\Delta/\epsilon)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/50f030f03bd74cf6533e1194.svg) | 固定记录数、索引、单个数值及预先确定的公开截断下上界；数值与边界同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/574b08031328fb735714c7c3.svg) | 发布均值、替换一条记录的最大均值变化与随机噪声；均为原数值单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d75420bd21d22fb2849de561.svg) | 无量纲隐私参数与位置0、尺度Δ/ε的Laplace分布；尺度为数值单位。 |

n=100、边界[0,1]时Δ=0.01。ε=0.5给噪声尺度0.02、标准差√2×0.02≈0.02828。单条记录最多改变b−a，求均值再除n，所以这一步确定噪声大小。

左侧实验用公开合成数据，在每个参数下抽取10000次噪声。隐私参数0.5对应理论RMSE约0.02828，模拟结果约0.02874；参数0.1时理论RMSE增到约0.1414。更小的参数收紧相邻数据输出概率的关系，也让数值发布更嘈杂。这里使用公开固定种子是为了复现噪声分布图；真正处理私有数据的发布机制，需要未公开的安全随机性、正确的敏感度和累计预算。把噪声种子与私有精确统计量一起公开，会改变观察者实际能够获得的信息。

![左、中：公开合成数据的Laplace噪声分布与每条件10000次抽样RMSE；右：两个不同分布客户端的FedAvg，横轴为通信轮数，各曲线每轮本地更新次数不同。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d02679e515dce22a2eed8ceb.svg?v=d02679e515dc)

图 6左、中：公开合成数据的Laplace噪声分布与每条件10000次抽样RMSE；右：两个不同分布客户端的FedAvg，横轴为通信轮数，各曲线每轮本地更新次数不同。

多次发布还会累积信息。同一份数据上分别使用0.5、0.5的纯差分隐私机制，基本组合给出总参数至多1，且加性松弛仍为零；更精细的会计方法可以结合采样和机制形式计算训练预算。DP-SGD把这个思想接到梯度训练中：逐样本计算梯度，按给定范数上限裁切，再给聚合梯度加入高斯噪声，并用采样率、噪声乘子和训练步数进行隐私会计。普通梯度裁切只约束优化更新；缺少逐样本敏感度控制、随机噪声和会计，就没有完成这套机制。

这些参数需要和研究目标一起设计。保护一条访问记录与保护一个人的全部访问，使用的是不同相邻关系；训练轮数增加也会改变累计信息。差分隐私给出了相邻数据的输出分布关系，数据治理则规定谁能访问原始数据、保留多久和怎样处理授权变化。二者接在不同位置：前者约束发布机制，后者管理数据使用流程。把两者的对象写清楚，比把“脱敏”“加密”“隐私训练”当作同一个标签更容易落实到代码和系统。

## 9. 数据留在各处，模型怎样一起学习

手机上的输入习惯、医院里的图像和工厂的传感器数据，常常天然分散在不同地点。McMahan等人在2017年介绍的FedAvg把训练组织成通信轮次：服务器发出当前参数，客户端在本地数据上更新若干步，再把更新后的参数按样本数加权平均。这个安排把通信与计算放到可调的关系里；本地多算几步，可以减少达到某个进度所需的通信，但客户端面对的数据不同时，也会向各自的局部目标走得更远。

$$
\theta^{(r+1)}=\sum_{k=1}^K\frac{n_k}{\sum_{j=1}^K n_j}\,\theta_k^{(r,E)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/397338c685aa99b36ec9a948.svg) | 通信轮次、客户端数、客户端索引与求和索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c5b6a59ed4dd1d73983aa22d.svg) | 客户端k记录数与该轮本地梯度更新步数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c5f24bbc7db331cc86546496.svg) | 聚合后的参数向量与客户端从共同起点出发更新E步后的向量；各参数保持模型自身单位。 |

两个同样大小客户端把参数(1,0)与(3,2)传回，平均为(2,1)。若每轮仅一步、相同步长、全批量梯度与按记录数加权，平均局部梯度等于全体梯度；多步时各客户端后续梯度在不同位置计算。

代码建立两个各有100条记录的客户端。第一组输入集中在−2附近，结果额外偏移−1；第二组输入集中在2附近，结果额外偏移+1。每个客户端都拟合一条直线，但由于输入位置与偏移同时变化，两家偏好的参数并不完全一致。图中比较每轮本地更新1、5、20步，总共通信40轮，横轴特意标为通信轮数：20步曲线每轮做了更多计算，并没有与1步曲线使用相同梯度计算量。合并数据的最小二乘结果提供统一的比较目标。

本地仅一步时，按人数平均局部全批量梯度等于直接计算合并数据梯度；实际参数最大差约4.4×10⁻¹⁶，处在浮点舍入量级。40轮后的全体MSE约0.19923，与合并数据最优值约0.19923相近；每轮20步时约0.21753。较多本地步数在这个异质数据例子中产生了客户端漂移。合并最优斜率约2.452也值得注意：生成式中对输入的系数是2，但分组偏移与输入位置相关，一条没有组标记的合并直线会把一部分组差异吸收进斜率。优化结果与生成机制参数因此需要按各自模型解释。

本地存储解决了原始记录的直接汇集方式，传出的更新仍然可能携带数据的信息。安全聚合通过协议让服务器看到聚合值，差分隐私则约束发布结果对相邻数据的敏感程度；两者可以组合，保护对象和参与方假设需要分别说明。本章在一个进程里模拟两家客户端，关注参数怎样更新以及何时偏离合并目标。把这个计算迁移到真实系统，还要处理客户端掉线、通信压缩、参与比例和模型版本同步，这些条件都会影响实际每轮参与了哪些数据。

完整脚本将本章的五组原始实验图、固定数据划分、训练权重和数值摘要放在同一输出目录。读代码时可以顺着信息流检查：训练只接触训练记录，温度只看调温记录，集合阈值只用共形记录；变化测试复用已经固定的模型；不同防护模型分别生成自己的攻击；隐私图与联邦图使用独立的公开合成数据。将这些边界写成可运行流程，便能同时保留预测的实用性和每个指标的实际含义。

### 从概率校准到联邦优化的完整CPU实验

脚本生成全部原始实验图、固定划分、模型权重与数值摘要。公开数字与合成数据分别处理；隐私部分是固定公开种子的噪声分布模拟。

```
"""Reliability experiments with separate fit, temperature, conformal and test sets."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.ndimage import rotate
from scipy.special import softmax
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss,roc_auc_score
import torch
from torch import nn
from torch.nn import functional as F
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def bins(prob,y):
 conf=prob.max(1);correct=prob.argmax(1)==y;edges=np.linspace(0,1,11);rows=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  mask=(conf>=lo)&(conf<(hi if hi<1 else hi+1e-9));n=int(mask.sum())
  if n:rows.append({'n':n,'confidence':float(conf[mask].mean()),'accuracy':float(correct[mask].mean())})
 return rows,float(sum(r['n']*abs(r['confidence']-r['accuracy']) for r in rows)/len(y))
class Classifier(nn.Module):
 def __init__(self):super().__init__();self.net=nn.Sequential(nn.Linear(64,48),nn.ReLU(),nn.Linear(48,10))
 def forward(self,x):return self.net(x)
def fgsm(model,x,y,epsilon):
 xx=x.clone().detach().requires_grad_(True);loss=F.cross_entropy(model(xx),y);g=torch.autograd.grad(loss,xx)[0];return (xx+epsilon*g.sign()).clamp(0,1).detach()
def train_classifier(x,y,adversarial=False):
 torch.manual_seed(39);m=Classifier();opt=torch.optim.Adam(m.parameters(),lr=.005)
 for epoch in range(30):
  order=torch.randperm(len(x))
  for ids in order.split(128):
   xx=x[ids];yy=y[ids];loss=F.cross_entropy(m(xx),yy)
   if adversarial:adv=fgsm(m,xx,yy,.1);loss=.5*(loss+F.cross_entropy(m(adv),yy))
   opt.zero_grad();loss.backward();opt.step()
 m.eval();return m
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);z=language=='zh';L=lambda a,b:a if z else b;rng=np.random.default_rng(39);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if z else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 # Five independently initialized/bootstrap heteroscedastic Gaussian regressors.
 rx=rng.uniform(-3,3,100);true_sd=.1+.12*abs(rx);ry=np.sin(1.5*rx)+rng.normal(size=100)*true_sd;grid=np.linspace(-5,5,240);means=[];vars=[]
 for seed in range(5):
  torch.manual_seed(390+seed);model=nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2));opt=torch.optim.Adam(model.parameters(),lr=.01);ii=np.random.default_rng(seed).choice(100,100,replace=True);xx=torch.tensor(rx[ii,None],dtype=torch.float32);yy=torch.tensor(ry[ii],dtype=torch.float32)
  for _ in range(350):mu,lv=model(xx).unbind(1);lv=lv.clamp(-6,2);loss=.5*((yy-mu).square()*torch.exp(-lv)+lv).mean();opt.zero_grad();loss.backward();opt.step()
  with torch.no_grad():a=model(torch.tensor(grid[:,None],dtype=torch.float32));means.append(a[:,0].numpy());vars.append(torch.exp(a[:,1].clamp(-6,2)).numpy())
  torch.save(model.state_dict(),out/f'uncertainty-model-{seed}.pt')
 means=np.array(means);vars=np.array(vars);mean=means.mean(0);alea=vars.mean(0);epis=means.var(0);total=alea+epis
 fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained');axs[0].fill_between(grid,mean-1.96*np.sqrt(total),mean+1.96*np.sqrt(total),color='#d2e6ec',label=L('均值±1.96总标准差','Mean ±1.96 total SD'));axs[0].plot(grid,mean,color='#247b94',label=L('集成均值','Ensemble mean'));axs[0].plot(grid,np.sin(1.5*grid),'--',color='#d97b36',label=L('生成均值','Generating mean'));axs[0].scatter(rx,ry,s=14,color='#293f4c',alpha=.6);axs[0].set(xlabel='x',ylabel='y',title=L('100训练点；训练范围[-3,3]','100 training points; training range[-3,3]'));axs[0].legend(fontsize=8)
 axs[1].plot(grid,alea,label=L('平均预测噪声方差','Mean predicted noise variance'));axs[1].plot(grid,epis,label=L('模型均值方差','Variance of model means'));axs[1].plot(grid,(.1+.12*abs(grid))**2,':',label=L('已知生成噪声方差','Known generating noise variance'));axs[1].set(xlabel='x',ylabel=L('y单位平方','Squared y units'));axs[1].legend(fontsize=8)
 for ax in axs:
  for edge in [-3,3]:ax.axvline(edge,color='#8399a5',ls=':')
 save(fig,'uncertainty')
 data=load_digits();X=data.data/16;y=data.target;ids=np.arange(len(y));train,rest=train_test_split(ids,train_size=900,random_state=39);cal,test=train_test_split(rest,train_size=300,random_state=39);tune,conf=train_test_split(cal,train_size=150,random_state=39);tx=torch.tensor(X[train],dtype=torch.float32);ty=torch.tensor(y[train]);testx=torch.tensor(X[test],dtype=torch.float32);testy=torch.tensor(y[test]);model=train_classifier(tx,ty)
 # Explicitly sharpen by2.5 to create a controlled overconfidence example.
 all_logits=model(torch.tensor(X,dtype=torch.float32)).detach()*2.5;logT=torch.tensor(0.,requires_grad=True);opt=torch.optim.LBFGS([logT],lr=.2,max_iter=80,line_search_fn='strong_wolfe');tune_y=torch.tensor(y[tune])
 def closure():opt.zero_grad();loss=F.cross_entropy(all_logits[tune]/logT.exp(),tune_y);loss.backward();return loss
 opt.step(closure);temperature=float(logT.exp().detach());raw=softmax(all_logits[test].numpy(),axis=1);prob=softmax(all_logits[test].numpy()/temperature,axis=1);cp=softmax(all_logits[conf].numpy()/temperature,axis=1);alpha=.1;k=int(np.ceil((len(conf)+1)*(1-alpha)));scores=1-cp[np.arange(len(conf)),y[conf]];q=float(np.sort(scores)[k-1]);sets=prob>=1-q;coverage=float(sets[np.arange(len(test)),y[test]].mean());setsize=float(sets.sum(1).mean());rawbins,rawece=bins(raw,y[test]);calbins,calece=bins(prob,y[test]);selection=[]
 for threshold in [.5,.7,.9,.95,.99]:
  accept=prob.max(1)>=threshold;selection.append({'threshold':threshold,'retained':int(accept.sum()),'fraction':float(accept.mean()),'error':float(np.mean(prob[accept].argmax(1)!=y[test][accept])) if accept.any() else None})
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained');axs[0].plot([0,1],[0,1],':',color='#8d9da6')
 for name,rows,c in [(L('原始分数×2.5','Raw logits×2.5'),rawbins,'#d97b36'),(L('温度校准','Temperature'),calbins,'#247b94')]:axs[0].plot([r['confidence'] for r in rows],[r['accuracy'] for r in rows],'o-',label=name,color=c)
 axs[0].set(xlabel=L('分箱平均最大概率','Mean maximum probability in bin'),ylabel=L('该箱分类正确率','Classification accuracy in bin'),title=L('10个等宽置信箱','10 equal-width confidence bins'));axs[0].legend(fontsize=8);axs[1].hist(raw.max(1),bins=np.linspace(0,1,11),alpha=.5,color='#d97b36',label=L('原始分数×2.5','Raw logits×2.5'));axs[1].hist(prob.max(1),bins=np.linspace(0,1,11),alpha=.5,color='#247b94',label=L('温度校准','Temperature'));axs[1].set(xlabel=L('最大预测概率','Maximum predicted probability'),ylabel=L('测试对象数','Test records'));axs[1].legend(fontsize=8);axs[2].plot([a['fraction'] for a in selection],[a['error'] for a in selection],'o-',color='#247b94')
 for a in selection:axs[2].annotate(str(a['threshold']),(a['fraction'],a['error']),xytext=(3,3),textcoords='offset points')
 axs[2].set(xlabel=L('保留预测比例','Fraction retained'),ylabel=L('保留对象中的错误率','Error among retained records'),title=L('阈值改变工作量与错误','Threshold changes workload and errors'));save(fig,'calibration')
 shifted=np.array([rotate(im,30,reshape=False,order=1,mode='constant',cval=0) for im in data.images[test]/16]);shiftx=torch.tensor(shifted.reshape(-1,64),dtype=torch.float32);sp=softmax(model(shiftx).detach().numpy()*2.5/temperature,axis=1);ssets=sp>=1-q;shiftcover=float(ssets[np.arange(len(test)),y[test]].mean());shiftacc=float(np.mean(sp.argmax(1)==y[test]));oodauc=float(roc_auc_score(np.r_[np.zeros(len(test)),np.ones(len(test))],np.r_[1-prob.max(1),1-sp.max(1)]));groups={};ink_cut=float(np.median(X[train].mean(1)))
 for g,mask in [('Lower ink',X[test].mean(1)<ink_cut),('Higher ink',X[test].mean(1)>=ink_cut)]:groups[g]={'n':int(mask.sum()),'accuracy':float(np.mean(prob[mask].argmax(1)==y[test][mask])),'coverage':float(sets[mask][np.arange(mask.sum()),y[test][mask]].mean()),'mean_set_size':float(sets[mask].sum(1).mean())}
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].bar([L('原图','Original'),L('旋转30°','Rotated30°')],[coverage,shiftcover],color=['#247b94','#d97b36']);axs[0].axhline(.9,ls='--',color='#263c49');axs[0].set(ylim=(0,1),ylabel=L('真实标签落入集合的比例','Fraction of true labels in prediction set'),title=L('同一共形阈值','Same conformal threshold'));axs[1].hist(sets.sum(1),bins=np.arange(-.5,2.5),alpha=.6,color='#247b94',label=L('原图','Original'));axs[1].hist(ssets.sum(1),bins=np.arange(-.5,2.5),alpha=.6,color='#d97b36',label=L('旋转30°','Rotated30°'));axs[1].set(xlabel=L('集合类别数','Prediction-set size'),ylabel=L('测试对象数','Test records'),xticks=[0,1],xlim=(-.5,1.5));axs[1].legend(fontsize=8);ix=np.arange(2);axs[2].bar(ix-.16,[g['accuracy'] for g in groups.values()],width=.3,label=L('准确率','Accuracy'));axs[2].bar(ix+.16,[g['coverage'] for g in groups.values()],width=.3,label=L('覆盖率','Coverage'));axs[2].set(xticks=ix,xticklabels=[f'{L("较少墨迹" if k=="Lower ink" else "较多墨迹",k)}\nn={v["n"]}' for k,v in groups.items()],ylim=(0,1),title=L('按训练亮度阈值分组','Groups from a training-set ink threshold'));axs[2].legend(fontsize=8);save(fig,'coverage_shift')
 # Separate trained models and fresh white-box attacks for each defense.
 robust=train_classifier(tx,ty,adversarial=True);poison_labels=ty.clone();pi=rng.choice(900,90,replace=False);poison_labels[pi]=(poison_labels[pi]+1)%10;poison=train_classifier(tx,poison_labels);attacks={};adversarial_examples={}
 for name,net in [('Standard',model),('Adversarial training',robust)]:
  vals=[]
  for eps in [0,.05,.1,.2]:
   adv=fgsm(net,testx,testy,eps);vals.append(float((net(adv).argmax(1)==testy).float().mean()));
   if eps==.1:adversarial_examples[name]=adv
  attacks[name]=vals
 changed=np.flatnonzero((model(testx).argmax(1)==testy).detach().numpy()&(model(adversarial_examples['Standard']).argmax(1)!=testy).detach().numpy());pick=int(changed[0]);original=testx[pick].reshape(8,8).numpy();adv=adversarial_examples['Standard'][pick].reshape(8,8).numpy();fig=plt.figure(figsize=(13,5),layout='constrained');gs=fig.add_gridspec(2,4,width_ratios=[1,1,1,2]);axs=[fig.add_subplot(gs[:,i]) for i in range(4)];titles=[L(f'原图：真实{int(testy[pick])}，预测{int(model(testx[pick:pick+1]).argmax(1)[0])}',f'Original: true {int(testy[pick])}, predicted {int(model(testx[pick:pick+1]).argmax(1)[0])}'),L(f'FGSM ε=0.1：预测{int(model(adversarial_examples["Standard"][pick:pick+1]).argmax(1)[0])}',f'FGSM ε=0.1: predicted {int(model(adversarial_examples["Standard"][pick:pick+1]).argmax(1)[0])}'),L('像素变化（真实尺度）','Pixel change (actual scale)')]
 for ax,arr,title,cmap in zip(axs[:3],[original,adv,adv-original],titles,['gray','gray','coolwarm']):im=ax.imshow(arr,cmap=cmap,vmin=-.1 if cmap=='coolwarm' else 0,vmax=.1 if cmap=='coolwarm' else 1);ax.set_title(title,fontsize=10);ax.set_xticks([]);ax.set_yticks([]);fig.colorbar(im,ax=ax,shrink=.55)
 for name,vals in attacks.items():axs[3].plot([0,.05,.1,.2],vals,'o-',label=L('标准训练' if name=='Standard' else '对抗训练',name))
 axs[3].set(xlabel=L('L∞扰动上限','L∞ perturbation budget'),ylabel=L('相应模型的FGSM准确率','FGSM accuracy for the attacked model'),ylim=(0,1));axs[3].legend(fontsize=8);save(fig,'robustness')
 # Public synthetic-data simulation of Laplace accuracy; fixed seed is for the teaching plot.
 bounded=rng.uniform(0,1,100);sensitivity=.01;epsilons=np.array([.1,.2,.5,1.]);dp=[];noises=[]
 for eps in epsilons:
  noise=rng.laplace(0,sensitivity/eps,10000);noises.append(noise);dp.append({'epsilon':float(eps),'scale':float(sensitivity/eps),'theoretical_rmse':float(np.sqrt(2)*sensitivity/eps),'empirical_rmse':float(np.sqrt(np.mean(noise**2)))})
 # Federated full-batch linear regression, two equally sized heterogeneous clients.
 clients=[]
 for center,offset in [(-2.,-1.),(2.,1.)]:
  cx=rng.normal(center,.8,100);cy=2*cx+offset+rng.normal(0,.2,100);clients.append((np.c_[cx,np.ones(100)],cy))
 FX=np.vstack([a for a,b in clients]);FY=np.concatenate([b for a,b in clients]);optimal=np.linalg.lstsq(FX,FY,rcond=None)[0];fed={};fweights={};lr=.03
 for steps in [1,5,20]:
  w=np.zeros(2);trace=[]
  for _ in range(40):
   local=[]
   for cx,cy in clients:
    v=w.copy()
    for _ in range(steps):v-=lr*2*cx.T@(cx@v-cy)/len(cy)
    local.append(v)
   w=np.mean(local,axis=0);trace.append(float(np.mean((FX@w-FY)**2)))
  fed[str(steps)]=trace;fweights[str(steps)]=w.tolist()
 central=np.zeros(2)
 for _ in range(40):central-=lr*2*FX.T@(FX@central-FY)/len(FY)
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');axs[0].hist(noises[0],bins=70,density=True,alpha=.5,label='ε=0.1');axs[0].hist(noises[2],bins=70,density=True,alpha=.6,label='ε=0.5');axs[0].set(xlabel=L('发布均值减去原均值','Released mean minus original mean'),ylabel=L('密度','Density'),title=L('公开模拟；每条件10000次噪声','Public simulation;10,000 noise draws each'));axs[0].legend();axs[1].plot(epsilons,[d['theoretical_rmse'] for d in dp],'o-',label=L('理论RMSE','Theoretical RMSE'));axs[1].plot(epsilons,[d['empirical_rmse'] for d in dp],'x',label=L('模拟RMSE','Simulated RMSE'));axs[1].set(xlabel='ε',ylabel=L('均值单位的RMSE','RMSE in mean units'));axs[1].legend(fontsize=8)
 for steps,trace in fed.items():axs[2].plot(range(1,41),trace,label=f'{L("本地步数","Local steps")}={steps}')
 axs[2].axhline(np.mean((FX@optimal-FY)**2),color='#8299a5',ls=':',label=L('合并数据最小二乘','Pooled least-squares optimum'));axs[2].set(xlabel=L('通信轮数','Communication round'),ylabel=L('全体数据MSE','Pooled-data MSE'),yscale='log');axs[2].legend(fontsize=7);save(fig,'privacy_federation')
 acc=float(np.mean(prob.argmax(1)==y[test]));summary={'n_total':len(y),'n_train':len(train),'n_temperature':len(tune),'n_conformal':len(conf),'n_test':len(test),'split_intersection':sum(len(set(a)&set(b)) for i,a in enumerate([train,tune,conf,test]) for b in [train,tune,conf,test][i+1:]),'temperature':temperature,'sharpening_factor':2.5,'accuracy':acc,'raw_nll':float(log_loss(y[test],raw)),'temperature_nll':float(log_loss(y[test],prob)),'raw_ece':rawece,'temperature_ece':calece,'argmax_change_count':int(np.sum(raw.argmax(1)!=prob.argmax(1))),'conformal_rank':k,'conformal_threshold':q,'coverage':coverage,'mean_set_size':setsize,'empty_set_count':int(np.sum(sets.sum(1)==0)),'shift_accuracy':shiftacc,'shift_coverage':shiftcover,'shift_mean_set_size':float(ssets.sum(1).mean()),'ood_uncertainty_auroc':oodauc,'groups':groups,'selection':selection,'attacks':attacks,'poison_count':len(pi),'poison_clean_accuracy':float((poison(testx).argmax(1)==testy).float().mean()),'attack_max_linf':float(torch.max(abs(adversarial_examples['Standard']-testx))),'laplace_sensitivity':sensitivity,'privacy_accuracy':dp,'basic_two_release_epsilon':1.,'basic_two_release_delta':0.,'fedavg_E1_centralized_max_error':float(np.max(abs(np.array(fweights['1'])-central))),'fed_weights':fweights,'pooled_optimal_weights':optimal.tolist(),'pooled_optimal_mse':float(np.mean((FX@optimal-FY)**2)),'fed_final_mse':{k:v[-1] for k,v in fed.items()},'uncertainty_at_zero':{'aleatoric':float(alea[np.argmin(abs(grid))]),'epistemic':float(epis[np.argmin(abs(grid))])},'uncertainty_at_four':{'aleatoric':float(alea[np.argmin(abs(grid-4))]),'epistemic':float(epis[np.argmin(abs(grid-4))])}}
 for name,net in [('standard',model),('adversarial',robust),('poisoned',poison)]:torch.save(net.state_dict(),out/f'{name}-classifier.pt')
 np.savez_compressed(out/'experiment_data.npz',train_indices=train,temperature_indices=tune,conformal_indices=conf,test_indices=test,raw_probabilities=raw,calibrated_probabilities=prob,conformal_scores=scores,prediction_sets=sets,shifted_images=shifted,shifted_probabilities=sp,test_labels=y[test],regression_x=rx,regression_y=ry,regression_grid=grid,ensemble_means=means,ensemble_variances=vars,adversarial_example=adv,original_example=original,poison_indices=pi,client_X=FX,client_y=FY);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M39.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Guo et al. (2017), On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)

   温度缩放与概率校准。

   Primary technical reference; linked, not reproduced
2. [Angelopoulos & Bates, A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511)

   有限样本预测集合、秩与覆盖条件。

   Primary technical reference; linked, not reproduced
3. [Kendall & Gal (2017), What Uncertainties Do We Need in Bayesian Deep Learning?](https://arxiv.org/abs/1703.04977)

   数据与模型不确定性的区分。

   Primary technical reference; linked, not reproduced
4. [Goodfellow et al., Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572)

   FGSM线性近似及对抗训练。

   Primary technical reference; linked, not reproduced
5. [Fairlearn: common fairness metrics](https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html)

   人口统计均等、机会均等与等化赔率的分母。

   Primary technical reference; linked, not reproduced
6. [Dwork & Roth (2014), The Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)

   Laplace机制、敏感度与组合。

   Primary technical reference; linked, not reproduced
7. [Opacus FAQ](https://opacus.ai/docs/faq)

   逐样本梯度裁切、噪声、会计与安全随机数。

   Primary technical reference; linked, not reproduced
8. [McMahan et al. (2017), Communication-Efficient Learning of Deep Networks from Decentralized Data](https://proceedings.mlr.press/v54/mcmahan17a.html)

   FedAvg本地更新与通信。

   Primary technical reference; linked, not reproduced
9. [scikit-learn: Probability calibration curves](https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html)

   原图中的SVC与两种校准。

   BSD-3-Clause; original figure reused
10. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    数字数据与原始任务。

    CC BY 4.0; digit data
