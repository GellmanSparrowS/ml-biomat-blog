# 一步一步生成：自回归模型与解码的选择

Source: https://ml-biomat.com/tutorials/machine-learning/m36/
Language: zh-CN

从下一字符的概率走到完整文本、像素与音频；训练一个LSTM，再比较采样、截断和束搜索。

## 1 从输入法的下一个字，到一整个对象的概率

手机输入“明天早上”后，候选栏可能出现“见”“出发”“开会”。候选会随已输入的内容变化，而且通常不只有一个合理答案。自回归模型把这种局部选择组织成一个完整的生成过程：读入已有部分，给下一项分配概率，选择一项接到末尾，再继续。这里的“一项”可以是汉字、英文子词、图像的像素，也可以是音频中的一个采样值。同一种概率结构因而能服务于文字补全、语音合成和图像生成；实际网络、数据表示和计算成本则各有不同。

理解这个过程，可以先想一棵不断分叉的路线树。第一处分叉决定走哪条路，第二处分叉的概率取决于刚才已经走过的路线。某条完整路线的概率，需要把沿途各个条件概率相乘。例如，三个连续选择分别得到0.6、0.5和0.8的概率，整条路径的概率就是0.24。后一项已经把前面的选择作为条件，因此这里并没有要求各项相互独立。把条件漏掉，才会把一条有语义联系的句子变成互不相关的抽签。

$$
p_\theta(x_1,\ldots,x_T\mid c)=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t},c)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2b4909437d46ae5fc3f3652f.svg) | 第t个离散符号、它之前的全部符号、完整序列长度；这里最后一个符号可为EOS。符号编号无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/16508da7a38cadb954c4d62f.svg) | 参数θ定义的概率分布、网络参数、可选条件，如已知提示；BOS作为起始约定。概率无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a9f0a3025c11269dd3099d4.svg) | 连乘符号与从1到T的步号；每个因子都是给定前缀后的下一项概率。 |

由p(a,b)=p(a)p(b|a)反复展开得到，不要求不同位置独立。三步条件概率0.6、0.5、0.8相乘为0.24。对所有完整可能结果求和得到1的前提，还包括模型最终会以概率1结束；实际采样另设最大长度，截断输出会单独记录结束状态。

我们还需要约定从哪里开始、在哪里结束。代码为每句添加BOS和EOS两个特殊符号：BOS启动预测，EOS表示句子完成。没有结束符，模型只能给固定长度的前缀打分，很难区分“这句话结束了”和“还有内容没写出来”。为把不同长度句子放进同一批张量，另设PAD补齐空位，PAD既不属于正文，也不进入损失。本章用一个能完整列出规则的微型语言做实验，让每一次生成都可以逐字检查。

## 2 为什么预测下一个字符就能学习整句话

概率的连乘很快会得到极小的数。即使每步都有0.5的概率，100步相乘也只有约十的负三十次方。计算时改用对数，乘法就变成加法；再加一个负号，模型给正确答案的概率越高，损失越小。这就是最大似然训练与交叉熵的联系。训练程序读到“the b”时，目标字符可以是“l”；损失只取出模型分给“l”的概率，却会通过softmax的归一化同时推动各个候选的分数调整。

$$
L=-\frac1N\sum_{i,t}m_{it}\log p_\theta(x_{it}\mid x_{i,<t}),\qquad N=\sum_{i,t}m_{it},\qquad \mathrm{PPL}=e^L
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3383ca973814618c495083d9.svg) | 句子编号、句内位置、正确目标符号及其前缀。批量logit形状为B×S×V，标签为B×S。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c22fe2a0468f908781365f1.svg) | 有效目标为1、PAD为0的掩码，以及有效目标总数；EOS计入。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a97c359088981a5c26ed4302.svg) | 每有效符号平均负对数似然，单位nats/符号；自然对数、自然指数底数，以及无量纲困惑度。 |

对概率连乘取对数得到逐位置求和，除以有效位置数得到可比较的平均值。三步路径概率0.24时，总负对数为1.427116，平均为0.475705，困惑度约1.609149。四个等概率选项给每步损失ln4，指数还原为4。PAD不应改变分母。

准备一行训练数据时，最容易出错的是错位关系。输入是BOS、t、h、e……，目标是t、h、e、空格……、EOS。每个位置的网络只能读取输入中该位置及其之前的内容，便能用已知前缀预测目标。真实句子为所有位置提供了正确历史，这种训练方式通常叫teacher forcing。它一次提供很多监督信号：一个有四十多个字符的句子，可以贡献四十多次有明确答案的下一字符预测，而不必等整句生成完才给一个总分。

困惑度把平均负对数似然再取指数，可理解为模型在预测时面对的有效选择数量。若每一步都在四个等概率选项间犹豫，困惑度就是4；若多数拼写几乎确定，只在少数词语边界需要选择，字符困惑度会很低。本例独立测试得到每字符0.159137 nats，困惑度1.172499。它反映的是这个微型字符语言的可预测性。比较两个困惑度时，应固定分词方式、测试文本、是否计入EOS以及平均分母；把字符模型和子词模型的数字直接并排，会把不同的计量单位混在一起。

## 3 同一条概率链，可以由不同网络实现

早期的有限阶语言模型，把最近几个词的出现次数整理成条件概率表。窗口变长后，需要统计的组合急剧增加，很多组合在训练语料中根本没有出现。神经网络把离散符号映射为向量，让不同上下文共享参数。递归网络进一步用隐藏状态概括历史：每读入一个字符，就把旧状态和新字符合成一个新状态。原图中的横向连线表示这份记忆如何向前传递，向上的连线则把记忆转成下一项预测；“自回归”说的是概率如何分解，“递归网络”说的是如何计算其中的条件概率。

![D2L原图：隐藏状态概括已观察历史，并逐步产生下一项分布。作者Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola；原图未改动，CC BY-SA 4.0。图中的时间索引约定与正文输入后预测下一项的约定相差一次平移。](https://ml-biomat.com/static/tutorials/machine-learning/figures/8f8b1d923892258a19beb0e8.svg?v=8f8b1d923892)

图 1D2L原图：隐藏状态概括已观察历史，并逐步产生下一项分布。作者Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola；原图未改动，CC BY-SA 4.0。图中的时间索引约定与正文输入后预测下一项的约定相差一次平移。

普通RNN反复使用非线性变换，较远信息在多次更新中可能逐渐减弱。1997年的LSTM引入门控制的信息通路，使网络能够分别学习写入、保留和读出。本章采用单层LSTM：每个字符先查表得到24维向量，再更新64维隐藏状态和64维细胞状态，最后输出28个候选分数。读完“the blue robot”后，模型保留下来的内容可以帮助下一步进入动词，而不必把整个前缀逐字重新输入。生成时缓存这两个状态，只需处理新加进来的字符。

$$
(h_t,c_t)=\operatorname{LSTM}(e(x_t),h_{t-1},c_{t-1}),\qquad a_t=W_oh_t+b_o,\quad p(x_{t+1}=j\mid x_{\le t})=\operatorname{softmax}(a_t)_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0f31d9accd033224b859ce5.svg) | 当前字符的24维嵌入、64维隐藏状态、64维细胞状态，都是学习得到的无量纲向量；此处c_t为状态，不是E1的外部条件。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fd8f947de5568504529202fd.svg) | 输出矩阵28×64、偏置28维、logit向量28维；j索引候选字符。 |
| ![Formula](https://ml-biomat.com/static/agent-math/efda7fd2544be4b97cf94699.svg) | 已经读入的步号、截至该步的全部输入，以及沿候选维度归一化的指数函数。 |

输入字符先进入递归状态，当前状态预测后一个字符，因而没有读入目标。可手算的两类输出a=(ln3,0)经softmax变为(3/4,1/4)。本例参数数目是28×24+4×64×(24+64+2)+28×64+28=25532；LSTM的两组偏置都计入。

因果Transformer采用另一种历史组织方式。每个位置产生查询、键和值，查询只与当前位置及左侧位置的键比较；右侧位置被遮罩，所以无法提前读取答案。训练时所有真实输入已经给出，各位置的注意力运算可以并行进行。RNN和LSTM仍有沿时间传递状态的计算依赖，即使库允许一次传入整段张量，也不等于每个时间点都独立计算。生成时三者都要等待刚选择的新符号，才能确定下一步的条件分布。Transformer的键值缓存减少重复计算，但不会消除这种概率依赖；一次输出多个符号需要额外的算法设计。

$$
A=\operatorname{softmax}_{\mathrm{row}}\!\left(\frac{QK^\top}{\sqrt d}+M\right),\qquad M_{ij}=\begin{cases}0&j\le i\\-\infty&j>i\end{cases},\qquad H=AV
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d62be4b9e5e1132c2311be54.svg) | 同一层各位置的查询、键和值；Q、K形状S×d，V形状S×d_v，特征无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7f6c855c878161720ea2bf9f.svg) | S×S因果掩码、S×S注意力权重、S×d_v混合输出；每行A和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33b315fab1d16e258b12531b.svg) | 查询位置、键位置、序列长度、查询键维度、值维度与转置符号。 |

右侧分数加−∞后指数为0，故被屏蔽位置不贡献输出。若第二个输入位置可见两项，未屏蔽分数为(ln3,0)，它们的权重为(0.75,0.25)；第三位置无论分数多大都为0。输入已经右移，所以允许读取当前位置输入仍然只是在预测下一符号。

把一整句送入本例LSTM，与逐字符送入并缓存状态，最终得到的所有logit最大差约为3.8×10⁻⁶，来自浮点计算路径。这给“同一条件概率的两种执行方式”一个可检查的数值对应。若逐步计算时忘记传回状态，每一步看到的就只剩当前字符；若把双向LSTM直接用于下一字符训练，反向通路又可能读到目标后的内容。前者丢失历史，后者改变了可用信息，两种错误都可以产生形状正确却含义错误的程序。

## 4 像素和声音，也能按顺序接龙

图像通常同时呈现在眼前，建模时却可以约定一个顺序：从第一行左端开始，逐行读到右下角。2016年的PixelRNN与PixelCNN把这种分解用于像素生成。预测第25个灰度像素时，前24个像素属于已知历史；第25个及其之后的原始像素都要遮住。卷积的权重乘上固定遮罩，就能在训练时阻止模型从近邻窗口偷看当前答案。彩色图像还需要规定R、G、B通道的顺序，或采用另行设计的联合通道分布。

![左：7×7图像按行扫描，蓝色24个位置可见，橙色第25项是当前目标。右：核宽3、膨胀1/2/4的实际依赖图，最上方节点覆盖15个输入位置；横轴为相对当前输入的偏移。](https://ml-biomat.com/static/tutorials/machine-learning/figures/fc7decbd66c1b59f70da1b22.svg?v=fc7decbd66c1)

图 2左：7×7图像按行扫描，蓝色24个位置可见，橙色第25项是当前目标。右：核宽3、膨胀1/2/4的实际依赖图，最上方节点覆盖15个输入位置；横轴为相对当前输入的偏移。

第一层的A型遮罩排除中心原始像素，后续B型遮罩可以读取中心位置的隐藏特征，因为该特征已经只由允许的历史构成。这一层层保持因果性的要求，比“把图片右边涂黑”更精确。简单堆叠遮罩卷积还可能遗漏部分上方历史，形成感受野盲区；门控PixelCNN用分开的垂直与水平信息流改善覆盖。本例代码直接构造5×5的A型遮罩，把当前及后续像素统一加100，指定位置的卷积输出仍完全不变，能验证可见范围确实被限制。

同年的WaveNet把下一项换成音频采样值。声音每秒包含成千上万个采样点，网络既要尊重时间顺序，又要看到足够长的历史。因果卷积只向左取输入，膨胀卷积则把取样间隔逐层增大。图中用核宽3、膨胀率1、2、4的三层网络，让最上方输出接触到连续15个输入位置；这组小尺寸是为手算而设计，原始WaveNet使用更深的膨胀层堆叠。原模型还将波形幅值量化为类别，用类似字符预测的softmax输出下一采样值的分布，并通过额外条件控制说话人或文本内容。

$$
R=1+\sum_{\ell=1}^{L}(k_\ell-1)d_\ell
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/626b40094bfad3228e2e2b06.svg) | 感受野的输入位置跨度与卷积层数；各层步幅均为1，只有向左的因果填充。 |
| ![Formula](https://ml-biomat.com/static/agent-math/58668167964505b55812b3b7.svg) | 第ℓ层核宽、膨胀间隔与层编号；均以离散位置计数，无物理单位。 |

一层宽k的卷积最远向左跨(k−1)d个位置，逐层叠加这些跨度并包含当前位置。k=3、d=1,2,4时R=1+2+4+8=15。这里所有偏移0到14都能由组合得到，所以跨度内没有缺口；任意膨胀组合未必有这一性质。

因果卷积在训练时可以同时计算一整段波形上各位置的损失，生成时却仍需逐个产生采样值。这解释了为什么“训练很并行”和“逐步生成很慢”可以同时成立。本章只计算小型因果卷积的依赖关系：改动输入位置16及之后的数值，前16个输出保持不变。若要把这种结构用于实时语音，除了预测质量，还要测量每秒能够生成多少采样点、缓存需要多少内存，以及播放前需要等待多久。

## 5 温度和候选截断，怎样改变生成的选择

训练完成后，权重决定一组候选分数；解码策略决定如何从分数中做选择。贪心法每一步都取最大概率候选，因此同一个前缀总会得到同一个续写。直接采样则保留概率中的不确定性。温度作用在softmax之前：降低温度会放大分数差异，提高温度会让较低分的候选得到更多机会。温度并不会重新训练模型，也不会补充训练数据里没有的知识；它改变的是已有候选之间的相对权重。

$$
q_j(\tau)=\frac{e^{a_j/\tau}}{\sum_{r\in\mathcal V}e^{a_r/\tau}},\qquad \widetilde q_j=\frac{q_j\,\mathbf1[j\in S]}{\sum_{r\in S}q_r}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/22cadef85af9a199f278e8e7.svg) | 候选j的logit、正温度和允许候选集合；生成时排除PAD/BOS，保留EOS。均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/105a65b28864b4c6dc4b2901.svg) | 温度调整后的概率、top-k或top-p保留集合，以及重新归一化后的抽样概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/788d26357b24a3227edc7280.svg) | 候选索引、求和索引与指示函数；保留时为1，否则为0。 |

取logit为ln(0.6)、ln(0.25)、ln(0.1)、ln(0.05)，温度1还原这四个概率；温度2使概率正比于它们的平方根。top-p=0.8按降序累计，保留0.6和0.25再除以0.85。稳定实现先减去最大logit，它只消去分子分母共同的因子。

top-k先保留概率最高的k项，top-p则按累计概率选择一个可变大小的候选集合。若四项概率为0.60、0.25、0.10和0.05，top-k=2保留前两项，归一化后分别为0.705882和0.294118。top-p=0.8也保留前两项，因为第一项尚未达到0.8，加入第二项后累计质量为0.85。达到或跨过阈值的那一项必须留下；若把它也删掉，候选集合实际包含的概率质量就低于设定值。一个高度确定的拼写位置可能只保留一个字符，而选择新单词时可能留下多个。

2019年提出的nucleus sampling围绕这一可变候选集合展开，研究了高似然解码与自然文本多样性之间的差异。这里可以用更小的语言直接观察同一问题：模型几乎确定“robo”后接“t”，却需要在“the ”后选择颜色。固定k会在两种位置都保留相同数量的候选，累计质量阈值则随分布的集中程度调整。下面的交互读取训练模型在五个真实前缀后的分数；点击候选分支，还可以查看追加该字符后下一步的分布。图中的变化来自条件与概率运算，而非预设动画。

## 走进一个真实前缀的分叉口

比较原始候选质量与截断后的抽样分布。前缀与下一层五个分支都来自训练出的LSTM；点击下方字符按钮，观察追加它后概率怎样改变。单次抽样使用固定种子，不会自动改变前缀。

[Figure: 实际下一字符概率及累计质量](https://ml-biomat.com/tutorials/machine-learning/m36/#M36-board)

蓝色为温度调整后、截断前的概率；橙色为保留并重新归一化后的概率。右图按蓝色概率递减累计，竖线标记实际保留项数。显示概率最高的12项，计算始终使用全部26个允许候选。

抽样截断还涉及一个容易忽略的计量差别：模型原本给某字符的概率，与截断后实际用于抽样的概率可以不同。评价原模型似然时应使用原始softmax；解释某次抽样为何选中一个字符时，应查看经过温度、截断和重新归一化的分布。代码的测试交叉熵保留28类完整分布，生成时排除PAD和BOS，再做采样。图和交互明确显示的是生成阶段的候选分布。

## 6 搜索一整句，与随机写一句有什么不同

贪心法容易在局部较好的岔路上过早定下来。假设第一步A、B的概率为0.6和0.4，走A之后最好续接概率是0.5，走B之后最好续接概率是0.9，那么两条最佳完整路径的概率分别为0.30和0.36。保留B这条暂时落后的分支，才可能找到更高概率的结尾。束搜索每一步保留若干个候选前缀，扩展它们，再按累计分数筛选；束宽控制了同时保留多少条路线，也决定要付出多少次预测和状态存储。

$$
s(y)=\sum_{t=1}^{n}\log p(y_t\mid y_{<t},c),\qquad s_\alpha(y)=\frac{s(y)}{((5+n)/6)^\alpha}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f10d7d17cd9a5f667bc1a22d.svg) | 生成续写、其中第t项、之前的续写，以及固定前缀条件。 |
| ![Formula](https://ml-biomat.com/static/agent-math/00fa1a2d18f9f99092a11597.svg) | 生成步数，含EOS但不含已给前缀，以及累计模型对数概率，单位nats。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a8b88596ffec78c08c189d1.svg) | 长度归一化指数，本例0.7；变换后的排序分数；5与6为这项规则选定的常数。 |

若n=1，分母为1；n=7且α=1时分母为2，因此原始分数−4变为−2。这会相对提高较长候选的排序。本例α=0退回原始对数概率。束宽4表示每轮保留四条候选，不表示最后一定找到了全局最优句子。

完整句子还有长短差别。连续加上负的对数概率，会让长句的原始分数越来越小。代码提供一个明确的长度归一化规则，并把EOS计入长度；所有候选使用同一规则比较。已经生成EOS的候选直接保留，不再接字符。我们的束宽为4、长度指数为0.7，得到“the green robot finds the key near the river.”，累计对数概率约−6.446799，归一化分数约−1.441288。这个分数用于当前搜索规则的排序；它经过长度变换，已经不是某句话的对数概率。

束搜索适合在已有模型下寻找高分候选，例如受约束的转写或翻译；随机采样更适合需要多个不同方案的场合。增加束宽可以探索更多路线，但有限束仍可能在早期剪掉最终最好的路径。长度归一化也会改变偏好，所以需要用实际任务评价，而不能只看搜索分数。对固定前缀反复执行确定性束搜索，仍会得到相同答案；若目标是为同一提示提供一组不同设计，需要另外安排多样性或采样机制。

## 7 真实训练：看懂低困惑度背后的选择和错误

本章语料由一个公开写在代码里的组合规则产生：六种颜色、四个角色、三个动作、五件物品、四个地点，组合成1440句“the … near the ….”。完整句子不重复，随机分为1008句训练、216句验证和216句测试。每个词都出现在训练语言中，测试考察的是没有用于训练的完整组合。语料是合成的微型语言，因此可以用完整规则检查拼写与句法，还能准确判断生成句子是否与训练句子重合。

LSTM共有25532个参数，用Adam学习80轮，每批最多64句，学习率0.004，梯度范数裁剪为1；按验证损失选出的权重来自第80轮。下方左图显示训练与验证损失的变化，中图检查每种解码设置生成100句时有多少符合完整语法，右图数这些结果包含多少不同字符串。测试集下一字符准确率约91.60%，不是100%，因为颜色、角色等位置本来就有多个合理选择。一个概率模型可以为这些选项分配合理概率，而不必在每个词语分叉处猜中测试句恰好选择的那条路。

![相同LSTM的训练与验证损失，以及六种策略各100次完整生成的语法有效率和不同字符串数。种子363到462；不同字符串数包括无效拼写。虚线标出验证选择的第80轮。](https://ml-biomat.com/static/tutorials/machine-learning/figures/64c59c7baafba1d4fd606931.svg?v=64c59c7baafb)

图 3相同LSTM的训练与验证损失，以及六种策略各100次完整生成的语法有效率和不同字符串数。种子363到462；不同字符串数包括无效拼写。虚线标出验证选择的第80轮。

在同一模型下，温度0.7得到100句有效句子和96种不同字符串；温度1.0得到99句有效句子和95种字符串；温度1.3得到86句有效句子和97种字符串。贪心生成100次只有一种字符串，而top-p=0.9得到100句有效句子和95种字符串。不同字符串数把拼错的句子也算进去，所以要与语法有效率一起读。这个例子很适合揭示一项指标的具体含义：多出两种字符串，可能只是多出了两个错误，而不是多出了两个有用的想法。

![每种策略按固定种子顺序最先生成的两个字符串。保留拼写错误和重复；温度1.3第二行展示条件偏离后继续生成的具体结果。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3d14965aa7323a86ae346ef6.svg?v=3d14965aa732)

图 4每种策略按固定种子顺序最先生成的两个字符串。保留拼写错误和重复；温度1.3第二行展示条件偏离后继续生成的具体结果。

图中保留了各策略最先生成的两个字符串。温度1.3的第二句出现“the cube narrie fox …”，错误首先把物品放到了颜色所在的位置，后续又形成不属于词表的拼写。生成过程中，这个错误会进入下一步的条件；训练时该位置通常看到的却是合乎规则的真实前缀。这就是误差累积的具体路径。查看逐字符概率热图，可以区分模型本来就不确定的词语边界，以及应该集中于一个字符的词内拼写位置，再决定改进数据、模型还是解码策略。

![对给定完整示例逐字符输入，显示实际模型的下一字符概率。每列总和约1，图中省去PAD/BOS两行；空格写作space，横轴下划线表示已输入空格。颜色范围0–1一致。](https://ml-biomat.com/static/tutorials/machine-learning/figures/eb84b10863e5a735df399b26.svg?v=eb84b10863e5)

图 5对给定完整示例逐字符输入，显示实际模型的下一字符概率。每列总和约1，图中省去PAD/BOS两行；空格写作space，横轴下划线表示已输入空格。颜色范围0–1一致。

生成字符串还帮助区分“学到可组合的规律”和“只给出一个固定答案”。贪心结果没有出现在训练句子中，却符合相同的组合语法，这与模型复用词语和句法位置模式的行为相符。留出集似然考察更多未参与训练的组合，采样统计则观察模型沿自己所选路径运行的结果。把这两类信息放在一起，比单独展示一句漂亮的生成文本，或只报告平均准确率，更能说明模型实际怎样使用学到的概率。

## 8 从条件续写到可复核的完整实验

条件生成可以从一段已知前缀开始。代码先读入“the blue robot ”，再继续预测动作、物品和地点；20次top-p=0.9采样全部保留了该前缀，也都符合语法。更一般的条件还可以是译文所对应的原文、说话人编号，或一幅用于描述的图像。它们需要作为额外输入进入每一步条件概率；模型怎样读取条件、条件在训练中是否出现，决定了它能控制哪些属性。把一句要求附在提示后面，也需要模型学过相应的条件关系才会产生稳定效果。

评价序列时，应先明确要完成的任务。概率估计看留出数据的负对数似然，转写看词或字符错误率，结构化输出看格式与字段是否符合规则，开放式生成还要检查内容、重复和多样性。本例同时保存每个字符的抽样概率、完整字符串、结束状态和训练句重合情况。生成文本中约七成与训练句重合，与训练集覆盖整个有限语言的70%这一事实相呼应；在组合数量固定的微型语言里，重合本身不足以解释模型采用了什么内部策略，还要结合留出组合上的概率和行为观察。

### 完整Python：字符LSTM、六种解码策略和束搜索

运行python main.py --output results --language zh。依赖NumPy、Matplotlib与PyTorch，语料全部由本程序生成，不下载权重。训练、生成、概率热图、因果检验和全部输出在同一文件中。

```
"""A character-level LSTM language model trained on a fully specified grammar.
All sequences, split indices, weights, generated strings, and figures are saved.
"""
from pathlib import Path
import argparse, json, math, itertools, copy, platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['en','zh'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
colors=['blue','red','gold','green','pink','white'];agents=['robot','pilot','otter','fox'];verbs=['carries','finds','moves'];objects=['cube','book','ball','key','bag'];places=['river','tower','garden','bridge']
sentences=[f'the {c} {a} {v} the {o} near the {r}.' for c,a,v,o,r in itertools.product(colors,agents,verbs,objects,places)]
vocab=['<pad>','<bos>','<eos>']+sorted(set(''.join(sentences)));stoi={s:i for i,s in enumerate(vocab)};V=len(vocab)
encoded=[[1]+[stoi[c] for c in s]+[2] for s in sentences];length=max(map(len,encoded));data=torch.zeros(len(encoded),length,dtype=torch.long)
for i,row in enumerate(encoded):data[i,:len(row)]=torch.tensor(row)
perm=np.random.default_rng(360).permutation(len(data));train_ids,val_ids,test_ids=perm[:1008],perm[1008:1224],perm[1224:]
class CharacterLSTM(nn.Module):
 def __init__(self):
  super().__init__();self.embedding=nn.Embedding(V,24,padding_idx=0);self.lstm=nn.LSTM(24,64,batch_first=True);self.head=nn.Linear(64,V)
 def forward(self,x,state=None):
  h,state=self.lstm(self.embedding(x),state);return self.head(h),state
torch.manual_seed(361);model=CharacterLSTM();optimizer=torch.optim.Adam(model.parameters(),lr=.004);order_rng=torch.Generator().manual_seed(362)
def evaluation(indices):
 model.eval();total=0.;tokens=0;correct=0
 with torch.no_grad():
  for idx in np.array_split(indices,max(1,math.ceil(len(indices)/128))):
   x=data[idx,:-1];y=data[idx,1:];logits,_=model(x);mask=y!=0;total+=F.cross_entropy(logits.reshape(-1,V),y.reshape(-1),ignore_index=0,reduction='sum').item();tokens+=mask.sum().item();correct+=((logits.argmax(-1)==y)&mask).sum().item()
 return dict(nll=total/tokens,perplexity=math.exp(total/tokens),accuracy=correct/tokens,tokens=tokens)
history=[];best=float('inf');best_epoch=0;best_state=None
for epoch in range(1,81):
 model.train();order=torch.randperm(len(train_ids),generator=order_rng);total=0.;count=0
 for part in order.split(64):
  idx=train_ids[part];x=data[idx,:-1];y=data[idx,1:];logits,_=model(x);loss=F.cross_entropy(logits.reshape(-1,V),y.reshape(-1),ignore_index=0);optimizer.zero_grad();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1);optimizer.step();n=(y!=0).sum().item();total+=loss.item()*n;count+=n
 valid=evaluation(val_ids);history.append([epoch,total/count,valid['nll']])
 if valid['nll']<best:best=valid['nll'];best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
model.load_state_dict(best_state);model.eval();test_metrics=evaluation(test_ids)
torch.save(dict(model=model.state_dict(),vocab=vocab,epoch=best_epoch),out/'character-lstm.pt')
def distribution(logits,temperature=1.,top_k=0,top_p=1.):
 logits=logits.astype('float64').copy()/temperature;logits[:2]=-np.inf;logits-=np.max(logits);probs=np.exp(logits);probs/=probs.sum();order=np.argsort(-probs,kind='stable');keep=np.ones(len(probs),dtype=bool)
 if top_k>0:keep[:]=False;keep[order[:top_k]]=True
 if top_p<1:
  # Keep the token that first reaches or crosses the requested cumulative mass.
  n=np.searchsorted(np.cumsum(probs[order]),top_p,side='left')+1;nucleus=np.zeros(len(probs),dtype=bool);nucleus[order[:n]]=True;keep&=nucleus
 probs*=keep;return probs/probs.sum()
@torch.no_grad()
def prefix_state(prefix):return model(torch.tensor([[1]+[stoi[c] for c in prefix]]))
@torch.no_grad()
def sample(prefix='',mode='sample',temperature=1.,top_k=0,top_p=1.,seed=0,max_new=80):
 logits,state=prefix_state(prefix);rng=np.random.default_rng(seed);text=prefix;trace=[];ended=False
 for _ in range(max_new):
  raw=logits[0,-1].numpy();prob=distribution(raw,temperature,top_k,top_p);token=int(prob.argmax()) if mode=='greedy' else int(rng.choice(V,p=prob));trace.append(dict(token=vocab[token],probability=float(prob[token])))
  if token==2:ended=True;break
  text+=vocab[token];logits,state=model(torch.tensor([[token]]),state)
 return dict(text=text,ended=ended,trace=trace)
@torch.no_grad()
def beam_search(prefix='',width=4,alpha=.7,max_new=80):
 logits,state=prefix_state(prefix);beams=[dict(text=prefix,score=0.,length=0,ended=False,logits=logits,state=state)]
 def rank(b):return b['score']/(((5+b['length'])/6)**alpha)
 for _ in range(max_new):
  candidates=[]
  for b in beams:
   if b['ended']:candidates.append(b);continue
   # Raw log probabilities retain the model's normalization, including special tokens.
   lp=F.log_softmax(b['logits'][0,-1],dim=-1);lp[:2]=-torch.inf
   for token in torch.topk(lp,width).indices.tolist():
    ended=token==2;new_logits,new_state=(b['logits'],b['state']) if ended else model(torch.tensor([[token]]),b['state'])
    candidates.append(dict(text=b['text']+('' if ended else vocab[token]),score=b['score']+lp[token].item(),length=b['length']+1,ended=ended,logits=new_logits,state=new_state))
  beams=sorted(candidates,key=rank,reverse=True)[:width]
  if all(b['ended'] for b in beams):break
 best=sorted(beams,key=rank,reverse=True)[0];return {k:best[k] for k in ['text','score','length','ended']}|dict(normalized_score=rank(best))
settings={'greedy':dict(mode='greedy'),'T0.7':dict(temperature=.7),'T1.0':dict(temperature=1.),'T1.3':dict(temperature=1.3),'top-k5':dict(top_k=5),'top-p0.9':dict(top_p=.9)}
generation={};metrics={};valid_set=set(sentences);training_set={sentences[i] for i in train_ids}
for name,options in settings.items():
 rows=[sample(seed=363+i,**options) for i in range(100)];generation[name]=rows;strings=[r['text'] for r in rows]
 metrics[name]=dict(valid=sum(s in valid_set for s in strings)/100,unique=len(set(strings)),ended=sum(r['ended'] for r in rows)/100,training_overlap=sum(s in training_set for s in strings)/100)
beam=beam_search();conditioned=[sample(prefix='the blue robot ',seed=463+i,top_p=.9) for i in range(20)]
# A small tree of actual next-character distributions for the browser explorer.
prefixes=['the ','the blue ','the blue robot ','the blue robot carries the ','the blue robot carries the book near the ']
lab_nodes=[]
for prefix in prefixes:
 logits,_=prefix_state(prefix);raw=logits[0,-1].numpy();options=[]
 for token in np.argsort(-distribution(raw))[:5]:
  if token<3:continue
  child,_=prefix_state(prefix+vocab[token]);options.append(dict(token=int(token),prefix=prefix+vocab[token],logits=child[0,-1].numpy().tolist()))
 lab_nodes.append(dict(prefix=prefix,logits=raw.tolist(),children=options))
(out/'decoding.json').write_text(json.dumps(dict(vocab=vocab,nodes=lab_nodes),ensure_ascii=False,separators=(',',':')),encoding='utf-8')
# Compare teacher-forced and cached sequential evaluation of identical known tokens.
with torch.no_grad():
 seq=data[test_ids[:1],:-1];whole,_=model(seq);parts=[];state=None
 for t in range(seq.shape[1]):
  pred,state=model(seq[:,t:t+1],state);parts.append(pred)
 sequential_error=float((whole-torch.cat(parts,1)).abs().max())
 # A causal dilated convolution reads only positions at or before its input index.
 torch.manual_seed(364);signal=torch.randn(1,1,32);altered=signal.clone();altered[:,:,16:]+=10
 def causal(x):
  for dilation in [1,2,4]:x=F.conv1d(F.pad(x,(2*dilation,0)),torch.tensor([[[.2,.3,.5]]]),dilation=dilation)
  return x
 causal_error=float((causal(signal)[:,:,:16]-causal(altered)[:,:,:16]).abs().max())
 mask=torch.ones(1,1,5,5);mask[:,:,3:]=0;mask[:,:,2,2:]=0
 img=torch.arange(49,dtype=torch.float32).reshape(1,1,7,7);changed=img.clone();changed.flatten()[24:]+=100
 pixel_error=float((F.conv2d(img,mask,padding=2)[0,0,3,3]-F.conv2d(changed,mask,padding=2)[0,0,3,3]).abs())
hand_p=np.array([.6,.25,.1,.05]);hand_k=hand_p.copy();hand_k[2:]=0;hand_k/=hand_k.sum();chain=.6*.5*.8
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(sentences=len(sentences),train=len(train_ids),validation=len(val_ids),test=len(test_ids),vocabulary=V,max_padded_length=length,seed=360),training=dict(epochs=80,best_epoch=best_epoch,parameters=sum(p.numel() for p in model.parameters()),embedding=24,hidden=64,lr=.004,batch=64),test=test_metrics,generation=metrics,beam=beam,conditioned=dict(count=20,valid=sum(r['text'] in valid_set for r in conditioned)/20,prefix_preserved=all(r['text'].startswith('the blue robot ') for r in conditioned)),hand=dict(chain_probability=chain,chain_nll=-math.log(chain),chain_perplexity=chain**(-1/3),top_k_first=float(hand_k[0]),top_p_count=int(np.searchsorted(np.cumsum(hand_p),.8)+1),receptive_field=1+2*(1+2+4),sequential_logit_max_error=sequential_error,causal_future_error=causal_error,pixel_future_error=pixel_error))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'generations.json').write_text(json.dumps(dict(unconditional=generation,beam=beam,conditioned=conditioned),ensure_ascii=False,indent=2),encoding='utf-8');(out/'corpus.json').write_text(json.dumps(dict(sentences=sentences,vocab=vocab,train_indices=train_ids.tolist(),validation_indices=val_ids.tolist(),test_indices=test_ids.tolist()),indent=2),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',encoded=data.numpy(),train_indices=train_ids,validation_indices=val_ids,test_indices=test_ids,history=history,mask=mask.numpy())
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,1],label=tr('训练','Train'),color='#125f82');axs[0].plot(h[:,0],h[:,2],label=tr('验证','Validation'),color='#bf7139');axs[0].axvline(best_epoch,color='#555',ls=':',lw=1);axs[0].set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('每字符负对数似然 / nats','NLL per character / nats'),title=tr('A  从字符规则到新组合','A  Learning unseen combinations'));axs[0].legend()
names=list(metrics);xs=np.arange(len(names));axs[1].bar(xs,[metrics[n]['valid'] for n in names],color='#125f82');axs[1].set_xticks(xs,names,rotation=35,ha='right');axs[1].set(ylim=(0,1.07),ylabel=tr('合乎语法的生成比例','Grammar-valid fraction'),title=tr('B  每种策略100次生成','B  100 generations per strategy'))
axs[2].bar(xs,[metrics[n]['unique'] for n in names],color='#bf7139');axs[2].set_xticks(xs,names,rotation=35,ha='right');axs[2].set(ylim=(0,105),ylabel=tr('不同完整字符串数','Distinct complete strings'),title=tr('C  同一模型的不同选择','C  Choices from the same model'));save(fig,'learning')
# A teacher-forced probability strip makes uncertain boundaries and certain spelling visible.
chosen='the blue robot carries the book near the river.';ids=torch.tensor([[1]+[stoi[c] for c in chosen]])
with torch.no_grad():prob=model(ids)[0].softmax(-1)[0].numpy().T
fig,ax=plt.subplots(figsize=(14,6),layout='constrained');im=ax.imshow(prob[2:,:],aspect='auto',vmin=0,vmax=1,cmap='YlGnBu');ax.set_yticks(range(V-2),[('EOS' if v=='<eos>' else 'space' if v==' ' else v) for v in vocab[2:]]);ax.set_xticks(np.arange(0,len(chosen)+1,2),['BOS' if i==0 else ('_' if chosen[i-1]==' ' else chosen[i-1]) for i in range(0,len(chosen)+1,2)]);ax.set(xlabel=tr('读入的当前字符（预测下一字符）','Current input character (predicting the following character)'),ylabel=tr('候选下一字符','Candidate next character'),title=tr('真实模型的条件概率：词内集中，选择词语时分散','Actual conditional probabilities: concentrated spelling, uncertain word choices'));fig.colorbar(im,ax=ax,label=tr('预测概率','Predicted probability'));save(fig,'probabilities')
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained');raster=np.arange(49).reshape(7,7);ax=axs[0];state=np.where(raster<24,1,np.where(raster==24,2,0));ax.imshow(state,cmap=matplotlib.colors.ListedColormap(['#e9e4d9','#71a6b8','#bd713f']),vmin=0,vmax=2)
for row in range(7):
 for col in range(7):ax.text(col,row,str(raster[row,col]+1),ha='center',va='center',fontsize=10)
ax.set(title=tr('A  预测第25个像素：只读蓝色历史','A  Predict pixel 25 using only blue history'),xlabel=tr('图像列：从左到右','Column: left to right'),ylabel=tr('图像行：从上到下','Row: top to bottom'))
ax=axs[1];offsets={0}
for row,d in enumerate([4,2,1]):
 new={i-j*d for i in offsets for j in range(3)}
 for i in offsets:
  for j in range(3):ax.plot([i,i-j*d],[3-row,2-row],color='#8ca8b4',lw=1)
 for i in new:ax.scatter(i,2-row,s=30,color='#125f82')
 offsets=new
ax.scatter(0,3,c='#bd713f',s=65);ax.set(xticks=range(-14,1,2),yticks=range(4),yticklabels=[tr('输入','Input'),'d=1','d=2','d=4'],xlabel=tr('相对当前输入的位置','Position relative to current input'),title=tr('B  核3、膨胀1/2/4覆盖15个位置','B  Kernel 3, dilation 1/2/4 spans 15 positions'));save(fig,'causality')
fig,ax=plt.subplots(figsize=(13,7.4));ax.axis('off');lines=[]
for name in ['greedy','T0.7','T1.0','T1.3','top-k5','top-p0.9']:
 lines.append((name,generation[name][0]['text'],generation[name][1]['text']))
for i,(name,a,b) in enumerate(lines):
 y=.96-i*.15;ax.text(0,y,name,color='#125f82',weight='bold',fontsize=13,transform=ax.transAxes);ax.text(.13,y,a,fontsize=11,transform=ax.transAxes);ax.text(.13,y-.05,b,fontsize=11,transform=ax.transAxes)
ax.set_title(tr('每种策略最先生成的两个字符串：保留实际拼写','The first two generated strings per strategy: actual spelling retained'),loc='left',pad=18);save(fig,'samples')
print(json.dumps(summary,indent=2))
```

运行后可从corpus.json复核句子与划分，从generations.json逐字查看全部输出，从experiment.npz读取编码和训练曲线。character-lstm.pt保存词表、网络权重和所选轮数，decoding.json保存交互使用的实际前缀分数。一个很有信息量的扩展，是固定模型和100个采样种子，只改变温度或累计概率阈值，再并排统计有效率、不同有效句子数、结束长度与词语频率。这样每项变化都对应一个明确操作，也能逐渐看清：模型学到的概率、搜索规则和最后采用的评价标准，各自决定了生成结果的哪一部分。

这条思路也能把前面出现的方法联系起来。LSTM与因果Transformer都可以实现自回归分布，VAE可以采用自回归解码器，图像模型还可以预测离散编码而不是直接预测像素。这些选择分别回答概率怎样分解、对象怎样表示、条件怎样计算的问题。把它们放在合适的层次上，便能理解“生成模型”为何是一个广泛目标，而自回归是构造和抽样联合分布的一种具体方式。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M36.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning: Working with Sequences](https://d2l.ai/chapter_recurrent-neural-networks/sequence.html)

   条件分解、递归状态原图。

   CC BY-SA 4.0; original image retained unchanged
2. [Long Short-Term Memory](https://doi.org/10.1162/neco.1997.9.8.1735)

   1997年门控记忆机制原论文。

   Primary paper; no figure copied
3. [Long Short-Term Memory — author-hosted full text](https://people.idsia.ch/~juergen/lstm1997-2024head.pdf)

   1997年原始论文的作者免费全文镜像。

   Primary paper; no figure copied
4. [PyTorch LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

   状态张量、权重与两组偏置。

   Official API reference; independent code
5. [Pixel Recurrent Neural Networks](https://arxiv.org/abs/1601.06759)

   像素自回归与PixelRNN/PixelCNN。

   Primary paper; no figure copied
6. [Conditional Image Generation with PixelCNN Decoders](https://arxiv.org/html/1606.05328v2)

   遮罩、盲区、条件生成和双信息流。

   Primary paper; no figure copied
7. [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/html/1609.03499v2)

   因果膨胀卷积与训练/生成计算顺序。

   Primary paper; independently constructed dependency diagram
8. [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)

   Nucleus sampling的候选质量截断。

   Primary paper; no figure copied
9. [Dive into Deep Learning: Beam Search](https://d2l.ai/chapter_recurrent-modern/beam-search.html)

   候选扩展与束宽的计算意义。

   CC BY-SA 4.0 reference; independent worked example
10. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

    因果注意力与位置并行。

    Primary paper; no figure copied
11. [Google Neural Machine Translation](https://arxiv.org/abs/1609.08144)

    长度归一化搜索分数形式。

    Primary paper; no figure copied
