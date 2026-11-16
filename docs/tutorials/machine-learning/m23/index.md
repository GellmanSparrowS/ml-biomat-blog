# 从找得到到排得好：检索、排序与推荐

Source: https://ml-biomat.com/tutorials/machine-learning/m23/
Language: zh-CN

拆开查询词分数、搜索近似、交互反馈与时间评价，训练一套可检查的双阶段推荐实验。

## 找到一篇文章，与推荐下一部电影

自行车刹车出了问题，你输入“bike repair”，希望先看到维修说明，而不是一份城市骑行地图。晚上打开视频网站，平台却没有收到明确查询，只能根据已经看过的内容推测下一部作品。信息检索与推荐共享一个核心问题：从很多候选中挑出少数有用对象。二者可利用的信息不同，评价目标也要跟着改变；一个主要回应当前问题，一个还需要推断兴趣、场景与此刻的需求。

大量候选让系统通常分成召回和排序两步。召回先快速筛出几十、几百或几千个候选，排序再做更细的比较。可以把它想成图书馆先找到可能有关的书架，再逐本查看目录。第一步漏掉的书，第二步即使非常聪明也无从选择。因此本节分别观察候选召回率、最终前十名质量与搜索计算量，把“找得到”“排得好”和“算得动”放在三个清楚的位置。

我们从八条短文档开始，每一个词都能直接检查，再进入5000向量的近似检索，最后训练80位用户与140件物品的推荐模型。后两组数据按公开的生成规则构造，用户日志按时间分成初始训练、第二阶段训练和最终测试。这样的规模可以在普通CPU上完整运行，也能把物品何时上架、负样本从哪里来、每个指标的分母是谁展示清楚。复杂系统中的许多错误，正藏在这些看似朴素的定义里。

## 一个词为什么值得更多分

倒排索引把“文档中有哪些词”翻转为“这个词出现在哪些文档”。本例bike对应D1和D5，repair对应D1和D2，索引同时保存各词在文档里的次数。查询来了，系统可以先合并相关词的文档列表，不必逐字重读全部文章。与书末索引类似，它负责快速找到位置；究竟哪篇排第一，还需要评分规则。词元化、大小写归一、词形处理和中文分词决定索引中的基本单位，索引与查询必须采用一致规则。

TF-IDF结合两种直觉：某词在一篇文章里多次出现，往往说明它是主题；某词在所有文章里都出现，区分能力就弱。这里用词频乘以平滑逆文档频率，再把整个文档向量归一化，用余弦比较查询与文档。归一化使长短不同的文档可以按方向比较。一个罕见的型号可能很有帮助，普遍出现的“guide”则较弱；不过罕见拼写错误也会得到大权重，词频规则仍需要与文本清理配合。

$$
w_{td}=f_{td}\left[\log\frac{N+1}{n_t+1}+1\right],\quad \widehat{\mathbf w}_d=\frac{\mathbf w_d}{\|\mathbf w_d\|_2},\quad s(q,d)=\widehat{\mathbf w}_q^\mathsf T\widehat{\mathbf w}_d
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2d2478f98dd73335a812d415.svg) | 词、文档、查询、文档总数及含词t的文档数；计数无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec687a03bb96151ed8bf0df0.svg) | 词t在文档d中的次数、TF-IDF分量及全词表向量；无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/61d920a4595219981b16f6e7.svg) | 单位化向量、欧氏长度、转置与余弦分数；无量纲。零向量约定分数为零。 |

这是代码使用的平滑IDF形式。四篇文档中某词出现于一篇，则IDF=log(5/2)+1≈1.916；出现两次得到分量3.833，再与其他分量一起归一化。查询使用同一训练词表与IDF。

BM25进一步让词频收益逐渐饱和，并单独处理文档长度。把bike写十遍，不应得到写一次的十倍分；一本几百页的总目录也更容易偶然包含查询词。Okapi团队在1994年TREC-3报告中讨论词频、长度与检索评价，方法演进对应的就是这些实际问题。本节使用带正值平滑IDF的常见BM25形式，把每个词的贡献拆开显示；不同实现的IDF变体与词元化规则需要一起记录。

$$
s(q,d)=\sum_{t\in q}\log\left(1+\frac{N-n_t+0.5}{n_t+0.5}\right)\frac{f_{td}(k_1+1)}{f_{td}+k_1(1-b+bL_d/\overline L)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33640683d4255f503365a392.svg) | 查询、文档、唯一查询词、文档总数、含词文档数与文档词频；无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f1ad2a4a6689818aacf5aeda.svg) | 文档长度与全语料平均长度，单位为词元数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/067d6b2017776921657ed11d.svg) | 词频饱和参数、长度归一化强度与分数；均无量纲，k1>0，0≤b≤1。 |

分子增长而分母也增长，产生词频饱和。N=8、df=2、tf=1且b=0时，单词贡献log3.6≈1.281；两个同样条件的查询词给2.562。较长文档在b>0时分母变大。

![左：八篇文档中bike与repair的BM25贡献；右：词法、四维LSA与RRF的名次。1为最好，同分按文档编号稳定排序。](https://ml-biomat.com/static/tutorials/machine-learning/figures/107bb99c57299e842c0dd242.svg?v=107bb99c5729)

图 1左：八篇文档中bike与repair的BM25贡献；右：词法、四维LSA与RRF的名次。1为最好，同分按文档编号稳定排序。

| ID | 内容 |
| --- | --- |
| D1 | bike repair wheel brake guide |
| D2 | bicycle maintenance tire repair workshop |
| D3 | bread baking flour yeast oven |
| D4 | sourdough bread starter fermentation guide |
| D5 | city bicycle route bike travel map |
| D6 | train travel ticket station guide |
| D7 | python data matrix vector tutorial |
| D8 | search vector index ranking retrieval |

## 拆开每个词的贡献

固定查询bike repair与八条文档，单独改变D1的重复和长度。倒排表与逐词评分随参数更新。

[Figure: BM25分词贡献与文档分数](https://ml-biomat.com/tutorials/machine-learning/m23/#M23-plot)

默认查询bike repair时，D1同时包含两个词，BM25约2.588；D2只包含repair，约1.294；D5只包含bike，而且多一个词，约1.197。交互可以给D1重复bike，也可以添加无关词，再改变饱和参数与长度参数。重复带来的增益和无关篇幅带来的惩罚会分开显示。把长度参数设为零，追加无关词便不再改变该文档分数；这比记住一个默认参数更容易理解它控制的究竟是什么。

## 用向量补充词面，再决定怎样融合

词法检索擅长精确名称、编号与明确术语，却可能漏掉换一种说法的内容。向量检索把查询与文档映射到同一空间，用内积、余弦或距离找邻居。本节先对TF-IDF矩阵做四维奇异值分解，得到可检查的潜在语义表示LSA。它利用文档中词的共同出现压缩表示，能够展示词法空间怎样变成低维空间；实际语义能力取决于语料结构，不会因为向量维数减少就自动理解所有同义词。

$$
A=U\Sigma V^\mathsf T,\quad z_d=\mathbf w_d^\mathsf T V_r,\quad s(q,d)=\frac{z_qz_d^\mathsf T}{\|z_q\|_2\|z_d\|_2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dfb718bce8fbf73a38d014f.svg) | 文档×词的TF-IDF矩阵与奇异值分解因子，所有分量无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be148765b8f86fb526625511.svg) | 保留维数、词数×r的右奇异向量矩阵、文档词向量及投影后的1×r文档/查询向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/13c6cae25092da1039650016.svg) | 余弦分数、欧氏范数与转置，无量纲。 |

投影把共同出现方向变成新坐标，再比较方向。二维例中zq=(1,0)、zd=(1,1)，余弦为1/√2≈0.707。代码用r=4，零投影时分数按零处理。

在这八条文档中，D1、D2、D5都与自行车有关，四维投影让它们在当前查询下得到较高相似度。但旅行指南也可能因共同词而靠近，低维压缩同时丢失了部分细节。现代稠密检索通常通过相关与不相关配对训练编码器，令有用的查询—文档关系在空间中靠近。它需要代表目标任务的训练对、合适的负样本，以及模型更新后同步更新的文档索引。保存旧向量却更换查询编码器，会让两边的坐标不再一致。

混合召回可以合并词法与稠密通道。直接相加分数，需要处理两个量纲不同、分布不同的评分尺度；倒数排名融合RRF改用各通道名次，以一个常数减缓第一名相对后面名次的优势。本例把BM25与LSA名次融合，固定常数60，并按文档编号稳定处理同分。这是一种方便的起点，最终比例和候选数量仍应在独立查询集上选择。精确型号查询与宽泛自然语言查询的最佳通道组合，可能并不相同。

$$
\operatorname{RRF}(d)=\sum_{j=1}^{J}\frac1{c+r_j(d)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fb244cdbf42016f7472d53.svg) | 文档、通道索引与通道总数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c246eec0bb985ee8582cbba.svg) | 文档在通道j的1起始名次、正平滑常数与融合分数，无量纲。 |

只用名次而非原始评分尺度。两个通道都第一、c=60时，分数2/61≈0.032787；两边都是第二则2/62≈0.032258。并列排名在本例按ID稳定确定。

向量召回分数也不是概率。内积0.8不等于80%相关，余弦为零只说明在当前表示和内积定义下正交。若向量已经单位化，余弦与内积产生相同排序；未归一化时，向量长度也参与评分。把归一化、距离类型与训练目标写进索引配置，可以解释为什么同一组向量换一种搜索器后排名发生变化，而不把差异误归于某种“智能程度”。

## 少看一些候选，要付出多少召回代价

精确搜索逐一计算查询与全部向量的距离，答案明确，适合作为核对基准。候选达到百万级时，可以用近似最近邻ANN减少扫描。本节实现一种透明的倒排文件索引IVF：先用k-means把数据库分成64个区域，查询时找最近的若干区域，只对区域内向量计算精确距离。这里的倒排项变成“区域对应哪些向量”，与词索引的组织思路相通。漏掉的邻居主要来自没有打开的区域。

![64区IVF的候选距离计算量—精确邻居召回曲线，标注为探查区数；右侧展示区域大小。另有每查询64次中心比较，未计入横轴。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2faac80751066154bb5b5b8e.svg?v=2faac8075106)

图 264区IVF的候选距离计算量—精确邻居召回曲线，标注为探查区数；右侧展示区域大小。另有每查询64次中心比较，未计入横轴。

代码用5000个16维向量和100条查询做实际对照。只探查一个区域时，平均计算约80.54个候选距离，精确前十邻居的召回率为0.253；探查8个区域时约626.76次、召回0.753；探查32个区域时约2507.13次、召回0.992。全部64区扫描5000向量时召回为1。这里横轴统计候选距离次数，另有固定的64次中心比较；它直接反映搜索工作量，运行时延还受实现、硬件和批量大小影响。

分区大小并不完全相同，因此相同探查数也会扫描不同数量。图的第二面板展示这个分布，提示系统应观察尾部时延与最慢查询。HNSW沿多层邻居图逐步靠近目标，增加搜索宽度可以换取更高召回；产品量化PQ把子向量编码为短码，以减少存储和距离计算成本，同时引入近似误差。IVF、图搜索与量化可以组合，但每增加一种近似，都应重新对照精确邻居，分别记录召回、存储与查询成本。

Faiss的官方教程先用精确平面索引说明数据库、查询、返回编号与距离，再进入更复杂索引。这种顺序很实用：先固定表示，判断近似搜索是否忠实找到它的邻居；随后用相关性标注判断这些邻居是否真的有用。ANN的Recall@10比较的是精确向量邻居，推荐Recall@10比较的是相关物品或未来交互，两种分母不同。把它们分开，才能定位问题出在索引近似，还是出在表示与任务不匹配。

## 用户—物品矩阵里，空白意味着什么

评分是一种明确反馈，点击、观看、收藏和购买则常作为隐式反馈。用户没有点击某件物品，可能是不喜欢，也可能从未见过、没有时间、已经在其他地方购买。矩阵里的空白因此不应直接填成“讨厌”。协同过滤利用共同交互模式：如果两件物品经常被同一批用户选择，它们可能有可利用的关联。本例先计算物品交互列的余弦相似度，对每个候选保留十个最相似物品，再累加用户历史中的邻居证据。

矩阵分解为每个用户和物品分别学习一个低维向量，内积形成匹配分数。它把稀疏表格里的规律分配到共享参数中：用户看过的几件物品都在某个潜在方向上有较大值，学习便可能把用户向量推向那个方向。潜在方向未必对应人类命名的“喜剧”“运动”等单一类别，旋转整套坐标也可能保留同样内积。解释向量时，应通过邻居与预测行为理解其作用，而不是直接给每个维度起一个未经检验的标签。

![用户—物品矩阵与两个低秩因子矩阵。](https://ml-biomat.com/static/tutorials/machine-learning/figures/071458d92fa3e4202726569b.svg?v=071458d92fa3)

图 3矩阵分解原图：用户因子与物品因子相乘重建评分。Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, Dive into Deep Learning, Fig. 21.3.1, CC BY-SA 4.0. 原图未改编，原页见延伸阅读；此图保留CC BY-SA 4.0许可。

$$
\widehat R_{ui}=\mathbf p_u^\mathsf T\mathbf q_i,\qquad\widehat R=PQ^\mathsf T
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d572cf609be8ae51ebaa6bac.svg) | 用户、物品索引与潜在维数，计数无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c59c6d3c83a1823c744de5b.svg) | 用户数×k、物品数×k的因子矩阵及其中k维向量；分量是学习坐标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b0822334e5c350d432390490.svg) | 单个匹配分数、完整分数矩阵与转置。本例分数无量纲，不作为评分星级。 |

同维坐标相乘求和，使用户与物品共享结构。p=(1,2)、q=(3,1)给分5；换成q=(0,1)得2。代码因子维数12，使用排名损失训练。

显式评分与隐式排序采用不同训练目标。若要预测用户给出的星级，可以在已知评分条目上拟合平方误差，并加入用户与物品的偏置项，分别描述打分宽严与普遍受欢迎程度。若目标是挑出下一件可能交互的物品，更关心的是候选之间的相对顺序。一个模型可能星级均方误差较低，却把最值得推荐的少数物品排得较差；选择损失前，应先决定最终页面如何使用它的输出。

2009年的BPR研究把隐式推荐写成成对排序：对用户u，已交互物品i应倾向于排在一个未交互候选j之前。训练单位因此是三元组，而不是孤立的“喜欢/不喜欢”标签。本节从训练期可用的120件物品中，为每条正交互抽取一个该用户训练期未交互的候选，优化分数差的逻辑损失。抽到的候选只是学习中的比较对象，未来可能成为正交互；抽样只使用当时可见的训练历史，避免提前利用未来记录。

$$
\mathcal L=\frac1{|\mathcal D|}\sum_{(u,i,j)\in\mathcal D}\log\left[1+\exp\bigl(-(s_{ui}-s_{uj})\bigr)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7648b83134fd7aeb0e573c5d.svg) | 抽样三元组集合、三元组数、用户、已交互物品与抽样比较物品。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dfee1a8dc0a4351aaa28654d.svg) | 两物品的无量纲匹配分数与平均成对逻辑损失。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e3f3d7dde4cc9b7b4cb6c489.svg) | 自然对数与指数；实现用稳定softplus。 |

正物品比比较物品高2分时损失log(1+e^-2)≈0.127；低2分时约2.127。代码每轮重新抽样，只排除训练正例，Adam另用权重衰减0.001。

均匀负采样覆盖宽，热门负采样更常遇到大家会看见的对象，困难负采样则选择模型容易混淆的候选。后者能提供更强训练信号，也更可能采到潜在喜欢的物品，需要结合任务判断。批内负样本通过其他样本的正物品节省计算，同一物品重复出现时还要处理假负例。若用采样后的softmax近似全目录概率，采样分布会影响归一化，可能需要相应校正；抽样策略本身就是模型设计的一部分。

## 把内容接入双塔，再给候选精排

只有物品ID的矩阵分解，在新物品第一次出现时缺少互动证据。双塔保留可快速检索的内积结构，同时把用户特征和物品特征分别送入两个编码网络。物品塔可以读取类别、文字或图像，用户塔可以读取历史聚合与当前情境；两边输出相同维数向量。物品向量可以预先计算，查询时只运行用户塔并搜索索引。若把每个用户—物品组合都交给一个大型联合模型，表达能力可能更强，却难以对整个目录预先缓存。

本例物品各有八维单位化内容特征，用户偏好也用八维向量生成。交互概率同时受偏好匹配与物品曝光权重影响，每人每天选一件此前未选的物品。前16天产生1280条交互，用于训练BPR矩阵分解和双塔；双塔用户输入是这16件历史物品特征的平均值。第17至20天的320条交互专门训练第二阶段排序器；第21至24天的320条记录作为最终测试，此时新增20件物品，形成65条冷物品测试交互。

![左：前24位用户的训练交互，橙线右侧为后来上架物品；中：真实BPR与双塔训练损失；右：未来四天完整目录的前十名评价。](https://ml-biomat.com/static/tutorials/machine-learning/figures/253bb1c9f113b0c9b297b558.svg?v=253bb1c9f113)

图 4左：前24位用户的训练交互，橙线右侧为后来上架物品；中：真实BPR与双塔训练损失；右：未来四天完整目录的前十名评价。

两个模型各训练160轮，均采用成对损失。完整目录测试中，双塔Recall@10约0.359、NDCG@10约0.307，BPR矩阵分解分别约0.225和0.171。直接用历史平均内容与物品内容内积的简单基线，Recall@10约0.369，略高于双塔。生成偏好本来就是内容内积，因此这个基线与数据机制很契合；增加网络并没有在本次样本中带来额外收益。训练损失下降与测试前十名改善，需要分别观察。

学习排序可以使用更多候选特征。代码真正训练XGBoost的LambdaMART排序器，把同一用户的候选放在同一query group，特征包含双塔分数、矩阵分解分数、内容相似度和训练热度。它从第二阶段交互中学习哪些比较更有利于NDCG，随后只重排双塔召回的30个候选。这30个候选的未来交互召回率约0.703，限定了排序器能够找到的范围；重排后前十Recall约0.350、NDCG约0.293，比直接双塔略低，提示这一阶段的特征、样本与目标需要继续改进。

## 冷启动与曝光，会怎样改变学习到的兴趣

新增物品没有训练交互，纯ID模型与邻居模型在本次实验的冷物品Recall@10均为零；使用内容的双塔约0.600，简单内容基线约0.631，重排后约0.446。这里的分母是65条冷物品测试交互，排名仍在完整可用目录中进行。冷启动也可能发生在新用户、全新类别或新地区。内容特征能为某些新对象提供相似性，真正超出已有特征范围的新类别，则需要新的测量、探索与反馈。

![左：完整目录排序中的冷物品召回，分母65条测试交互；右：120件已有物品的生成曝光权重与训练交互数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5b6fdc8bc3e1f9b345902e70.svg?v=5b6fdc8bc3e1)

图 5左：完整目录排序中的冷物品召回，分母65条测试交互；右：120件已有物品的生成曝光权重与训练交互数。

曝光偏差来自“有机会看见”与“看见后愿意选择”两层机制。某件物品被放在首页，交互更容易增长；训练器若只看点击，可能把位置优势学成偏好，再继续扩大曝光。代码用明确曝光权重生成日志，图里可以看到曝光与训练交互的关系，同时还有用户兴趣造成的分散。现实日志应保留展示、位置、候选集合、时间与行为结果，才能区分没有展示、展示未点击和点击后不满意等情况。

随机探索可以为较少曝光的候选创造可比较机会。在分配概率已知且目标策略有支持的日志中，逆倾向加权可帮助评价另一策略；极小概率会带来高方差，需要检查权重与有效样本量。把未曝光记录随意补成负例，或者用一个估计概率就声称已经消除偏差，都会改变问题的统计含义。更实际的做法是先明确要优化点击、完成观看、满意度还是长期留存，再设计能够测到该目标的记录与实验。

## 让指标对应真正要展示的那一页

Recall@K问前K个候选找回了多少相关物品；NDCG还关心它们排在什么位置，并允许多级相关性。代码最终测试中每人有四条未来交互，先排除训练期和第二阶段已经见过的物品，再对全部剩余目录排序。二值相关性让每次命中增益为1，越靠后折扣越大。用少量采样负例替代完整目录会让排名任务变容易，也改变指标定义，因此不同候选协议的数值应分开记录。

$$
\operatorname{Recall@K}=\frac{|L_K\cap G|}{|G|},\quad\operatorname{DCG@K}=\sum_{r=1}^K\frac{2^{g_r}-1}{\log_2(r+1)},\quad\operatorname{NDCG@K}=\frac{\operatorname{DCG@K}}{\operatorname{IDCG@K}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ab6865610db5ec65193b681b.svg) | 显示个数、前K物品集合、相关物品集合、集合大小与交集，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6b3a844b884853058429fba8.svg) | 1起始排名与该位置相关性等级；代码为0/1未来交互。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0bc5c9a3a33a40b20fdb7f5.svg) | 折损增益、同一相关集合的理想折损增益、归一化增益与2为底对数，无量纲。 |

两件相关物品出现在前三名的第一和第三位，Recall@3=1，DCG=1+1/2=1.5，理想DCG=1+1/log2(3)≈1.631，NDCG≈0.920。本例每用户四条未来交互，按用户平均。

相关性标注也要对应查询的实际任务。维修查询中，直接介绍刹车调整的文章可以得到高等级，一般保养指南得到中等级，城市骑行路线即使包含bike也可能只得低等级。评分者需要共同的判断说明，含糊查询可以保留多个意图。推荐中的购买、完整观看和一次误触点击也不是同一等级的证据。先把相关性含义说清楚，再讨论排名指标，才能知道指标改善究竟替读者解决了什么问题。

时间切分使训练者只使用测试时刻之前的信息，但离线回放仍来自既有曝光机制。推荐一个过去没展示过的物品，日志中通常没有它在那次情境下会怎样的结果；直接把所有未发生点击当成零，评价的是特定观察协议。在线随机实验可以比较真实展示后的结果，应以用户或合适的稳定单位分组，并考虑观察窗、星期周期与跨用户影响。平均点击率之外，还可以同时看目录覆盖、重复推荐、新物品表现和用户留存，让局部排序增益与整体体验对应起来。

目录管理也影响评价与实际展示。物品下架后应从可用候选中排除，内容更新后可能需要重新生成向量，新物品则需要进入索引。若只取十个邻居再过滤库存，删除几件后页面可能凑不满十件；扩大候选范围或采用支持过滤的索引可以处理这种关系。保留编码器版本、目录快照、可用条件与索引构建时间，能够还原一次检索结果，也让离线评价与实际页面面对同一候选范围。

### 完整实验：BM25、IVF、BPR、双塔与LambdaMART

运行python main.py --output results --language zh。无需下载数据，八条原创文档与模拟日志均由代码保存；输出四组原创图、模型权重、时间划分与指标摘要。

```
"""Inspectable lexical retrieval, IVF, BPR, two towers and chronological reranking."""
from pathlib import Path
import argparse,json,re
from collections import Counter,defaultdict
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from threadpoolctl import threadpool_limits
from xgboost import XGBRanker
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
DOCS=['bike repair wheel brake guide','bicycle maintenance tire repair workshop','bread baking flour yeast oven','sourdough bread starter fermentation guide','city bicycle route bike travel map','train travel ticket station guide','python data matrix vector tutorial','search vector index ranking retrieval']
def tokens(s):return re.findall('[a-z]+',s.lower())
def bm25(docs,query,k1=1.2,b=.75):
 cs=[Counter(tokens(d)) for d in docs];length=np.array([sum(c.values()) for c in cs]);N=len(docs);score=np.zeros(N);parts={}
 for t in sorted(set(tokens(query))):
  tf=np.array([c[t] for c in cs]);df=np.count_nonzero(tf);idf=np.log(1+(N-df+.5)/(df+.5));v=idf*tf*(k1+1)/(tf+k1*(1-b+b*length/length.mean()));score+=v;parts[t]=v
 return score,parts
def metrics(scores,truth,k=10):
 order=np.argsort(-scores,axis=1,kind='stable')[:,:k];hit=np.take_along_axis(truth,order,axis=1);den=truth.sum(1);rec=hit.sum(1)/np.maximum(den,1);discount=1/np.log2(np.arange(k)+2);ideal=np.array([discount[:min(int(n),k)].sum() for n in den]);ndcg=(hit*discount).sum(1)/np.maximum(ideal,1e-12);return {'recall':float(rec[den>0].mean()),'ndcg':float(ndcg[den>0].mean()),'coverage':float(len(np.unique(order))/scores.shape[1])},order
class MF(nn.Module):
 def __init__(self,nuser,nitem):
  super().__init__();self.u=nn.Embedding(nuser,12);self.v=nn.Embedding(nitem,12);nn.init.normal_(self.u.weight,std=.1);nn.init.normal_(self.v.weight,std=.1)
 def all_scores(self,uf,it):return self.u.weight@self.v.weight.T
class Towers(nn.Module):
 def __init__(self):
  super().__init__();self.u=nn.Sequential(nn.Linear(8,24),nn.Tanh(),nn.Linear(24,12));self.v=nn.Sequential(nn.Linear(8,24),nn.Tanh(),nn.Linear(24,12))
 def all_scores(self,uf,it):return self.u(uf)@self.v(it).T
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';L=lambda a,b:a if zh else b;rng=np.random.default_rng(23);torch.manual_seed(23);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 postings=defaultdict(list)
 for i,doc in enumerate(DOCS):
  for term,tf in Counter(tokens(doc)).items():postings[term].append([i,tf])
 lexical,parts=bm25(DOCS,'bike repair');vec=TfidfVectorizer();A=vec.fit_transform(DOCS).toarray();q=vec.transform(['bike repair']).toarray()[0];cos=A@q;U,S,Vt=np.linalg.svd(A,full_matrices=False);latent=A@Vt[:4].T;ql=q@Vt[:4].T;dense=latent@ql/np.maximum(np.linalg.norm(latent,axis=1)*np.linalg.norm(ql),1e-12)
 ranks1=np.argsort(np.argsort(-lexical,kind='stable'),kind='stable')+1;ranks2=np.argsort(np.argsort(-dense,kind='stable'),kind='stable')+1;rrf=1/(60+ranks1)+1/(60+ranks2)
 fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained');terms=list(parts);base=np.zeros(8)
 for t in terms:axs[0].barh(np.arange(8),parts[t],left=base,label=t);base+=parts[t]
 axs[0].set(yticks=range(8),yticklabels=[f'D{i+1}' for i in range(8)],xlabel='BM25',title=L('查询 bike repair：逐词贡献','Query bike repair: term contributions'));axs[0].invert_yaxis();axs[0].legend();im=axs[1].imshow(np.c_[ranks1,np.argsort(np.argsort(-cos))+1,ranks2,np.argsort(np.argsort(-rrf))+1],cmap='Blues_r',vmin=1,vmax=8);axs[1].set(yticks=range(8),yticklabels=[f'D{i+1}' for i in range(8)],xticks=range(4),xticklabels=['BM25','TF-IDF','LSA','RRF'],title=L('同一语料的排名（1最好）','Ranks on the same corpus (1 is best)'))
 for i in range(8):
  for j,v in enumerate([ranks1[i],(np.argsort(np.argsort(-cos))+1)[i],ranks2[i],(np.argsort(np.argsort(-rrf))+1)[i]]):axs[1].text(j,i,str(v),ha='center',va='center',color='white' if v<=3 else '#20394a')
 save(fig,'lexical')
 # IVF uses Euclidean partitions; exact top10 provides retrieval ground truth.
 xb=rng.normal(size=(5000,16));xq=rng.normal(size=(100,16));km=KMeans(64,n_init=3,random_state=23).fit(xb);exact=np.argsort(((xq[:,None]-xb[None])**2).sum(2),axis=1)[:,:10];centers=np.argsort(((xq[:,None]-km.cluster_centers_[None])**2).sum(2),axis=1);trade=[]
 for probe in [1,2,4,8,16,32,64]:
  recalls=[];cost=[]
  for qi in range(100):
   ids=np.flatnonzero(np.isin(km.labels_,centers[qi,:probe]));chosen=ids[np.argsort(((xb[ids]-xq[qi])**2).sum(1))[:10]];recalls.append(len(set(chosen)&set(exact[qi]))/10);cost.append(len(ids))
  trade.append({'nprobe':probe,'recall10':float(np.mean(recalls)),'distance_evaluations':float(np.mean(cost))})
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot([d['distance_evaluations'] for d in trade],[d['recall10'] for d in trade],'o-',color='#247b94')
 for d in trade:axs[0].annotate(str(d['nprobe']),(d['distance_evaluations'],d['recall10']),xytext=(4,5),textcoords='offset points')
 axs[0].set(xlabel=L('每查询候选向量距离计算数','Candidate-vector distances per query'),ylabel='Recall@10',ylim=(0,1.06),title=L('5000向量，100查询，64分区','5,000 vectors, 100 queries, 64 cells'));axs[1].hist(np.bincount(km.labels_),bins=15,color='#d97b36');axs[1].set(xlabel=L('每分区向量数','Vectors per cell'),ylabel=L('分区数','Number of cells'),title=L('相同nprobe也会扫描不同数量','The same nprobe can scan different counts'));save(fig,'ivf')
 # Known synthetic preference plus exposure generates chronological unique interactions.
 nu,ni,warm=80,140,120;item=rng.normal(size=(ni,8));item/=np.linalg.norm(item,axis=1,keepdims=True);preference=rng.normal(size=(nu,8));preference/=np.linalg.norm(preference,axis=1,keepdims=True);utility=preference@item.T;exposure=np.linspace(1.5,.5,ni);log=[];seen=np.zeros((nu,ni),bool)
 for day in range(24):
  available=warm if day<20 else ni
  for u in range(nu):
   prob=np.exp(5*utility[u,:available])*exposure[:available];prob[seen[u,:available]]=0;prob/=prob.sum();i=int(rng.choice(available,p=prob));seen[u,i]=True;log.append((u,i,day))
 log=np.array(log);train=np.zeros((nu,ni),bool);stage2=train.copy();test=train.copy()
 for u,i,t in log:(train if t<16 else stage2 if t<20 else test)[u,i]=True
 uf=train@item/16;uft=torch.tensor(uf,dtype=torch.float32);it=torch.tensor(item,dtype=torch.float32);users,pos=np.where(train);users_t=torch.tensor(users);pos_t=torch.tensor(pos);available_neg=[np.flatnonzero(~train[u,:warm]) for u in range(nu)];models={};traces={};rawscores={}
 for name,model in [('BPR-MF',MF(nu,ni)),('Two-tower',Towers())]:
  opt=torch.optim.Adam(model.parameters(),lr=.025,weight_decay=.001);losses=[]
  for epoch in range(160):
   neg=torch.tensor([rng.choice(available_neg[u]) for u in users]);scores=model.all_scores(uft,it);loss=F.softplus(-(scores[users_t,pos_t]-scores[users_t,neg])).mean();opt.zero_grad();loss.backward();opt.step();losses.append(float(loss.detach()))
  models[name]=model;traces[name]=losses;rawscores[name]=model.all_scores(uft,it).detach().numpy();torch.save(model.state_dict(),out/(name.lower().replace('-','_')+'.pt'))
 popularity=train.sum(0);norm=train/np.maximum(np.sqrt(train.sum(0)),1);sim=norm.T@norm;np.fill_diagonal(sim,0);keep=np.zeros_like(sim,bool);top=np.argsort(-sim,axis=0,kind='stable')[:10];np.put_along_axis(keep,top,True,axis=0);sim*=keep;rawscores['Item-kNN']=train@sim;rawscores['Popularity']=np.tile(popularity,(nu,1));rawscores['Content']=uf@item.T
 def features(u,ids):return np.c_[rawscores['Two-tower'][u,ids],rawscores['BPR-MF'][u,ids],rawscores['Content'][u,ids],np.log1p(popularity[ids])]
 xx=[];yy=[];qid=[]
 for u in range(nu):
  ids=np.flatnonzero(~train[u,:warm]);xx.append(features(u,ids));yy.extend(stage2[u,ids].astype(int));qid.extend([u]*len(ids))
 ranker=XGBRanker(n_estimators=100,max_depth=3,learning_rate=.05,objective='rank:ndcg',tree_method='hist',n_jobs=1,random_state=23,lambdarank_num_pair_per_sample=10);ranker.fit(np.vstack(xx),np.array(yy),qid=np.array(qid));ranker.save_model(out/'reranker.json')
 history=train|stage2;results={};rankings={};candidate_recall=[];rerank=np.full((nu,ni),-1e12)
 for name,s in rawscores.items():
  masked=s.copy();masked[history]=-1e12;results[name],rankings[name]=metrics(masked,test)
 for u in range(nu):
  s=rawscores['Two-tower'][u].copy();s[history[u]]=-1e12;ids=np.argsort(-s,kind='stable')[:30];candidate_recall.append(test[u,ids].sum()/4);rerank[u,ids]=ranker.predict(features(u,ids))
 results['Tower+rerank'],rankings['Tower+rerank']=metrics(rerank,test);cold={}
 for name,ranking in rankings.items():cold[name]=float(sum(test[u,ranking[u][ranking[u]>=warm]].sum() for u in range(nu))/test[:,warm:].sum())
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].imshow(train[:24],aspect='auto',cmap='Blues',interpolation='nearest');axs[0].axvline(warm-.5,color='#d97b36');axs[0].set(xlabel=L('物品ID','Item ID'),ylabel=L('用户ID（前24人）','User ID (first 24)'),title=L('前16天的交互矩阵','First 16 days: interaction matrix'))
 for name,loss in traces.items():axs[1].plot(loss,label=name)
 axs[1].set(xlabel=L('训练轮数','Training epoch'),ylabel=L('成对softplus损失','Pairwise softplus loss'));axs[1].legend(fontsize=9);names=list(results);ix=np.arange(len(names));axs[2].barh(ix-.16,[results[n]['recall'] for n in names],height=.3,label='Recall@10');axs[2].barh(ix+.16,[results[n]['ndcg'] for n in names],height=.3,label='NDCG@10');axs[2].set(yticks=ix,yticklabels=names,xlabel=L('后四天，全候选评价','Last four days, full eligible catalog'));axs[2].legend(fontsize=8);save(fig,'recommendation')
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].barh(names,[cold[n] for n in names],color='#247b94');axs[0].set(xlabel=L('冷启动交互Recall@10','Cold-item interaction Recall@10'),title=L('20件物品从第21天才可见','20 items become available on day 21'));axs[1].scatter(exposure[:warm],popularity[:warm],color='#d97b36',s=28,alpha=.7);axs[1].set(xlabel=L('生成曝光权重','Generating exposure weight'),ylabel=L('训练交互次数','Training interaction count'),title=L('点击同时受偏好与曝光影响','Interactions mix preference and exposure'));save(fig,'cold_exposure')
 summary={'documents':DOCS,'query':'bike repair','bm25_scores':lexical.tolist(),'tfidf_scores':cos.tolist(),'lsa_scores':dense.tolist(),'rrf_scores':rrf.tolist(),'lexical_order':np.argsort(-lexical,kind='stable').tolist(),'ivf':trade,'users':nu,'items':ni,'warm_items':warm,'log_count':len(log),'train_count':int(train.sum()),'stage2_count':int(stage2.sum()),'test_count':int(test.sum()),'cold_test_count':int(test[:,warm:].sum()),'train_test_overlap':int((train&test).sum()),'results':results,'cold_recall':cold,'candidate_recall30':float(np.mean(candidate_recall)),'loss_initial':{k:v[0] for k,v in traces.items()},'loss_final':{k:v[-1] for k,v in traces.items()},'train_last_day':int(log[log[:,2]<16,2].max()),'test_first_day':int(log[log[:,2]>=20,2].min())}
 summary.update({'postings':dict(postings),'item_neighbors':10,'ivf_full_recall':trade[-1]['recall10'],'ivf_full_distance_count':trade[-1]['distance_evaluations']})
 np.savez_compressed(out/'experiment_data.npz',log=log,item_features=item,user_preferences=preference,exposure=exposure,train=train,stage2=stage2,test=test,user_features=uf,ivf_database=xb,ivf_queries=xq,ivf_labels=km.labels_,ivf_centers=km.cluster_centers_,exact_neighbors=exact,**{k.replace('-','_').replace('+','_'):v for k,v in rawscores.items()});(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

完整代码输出原始文档、倒排表、所有时间戳、交互矩阵、内容特征、模型权重、实际排名指标和图的数组。可以先修改一个查询，检查词分数；再改变IVF探查数，观察邻居召回；最后改变曝光或新增物品比例，重新训练并比较冷启动结果。每次只改变一个问题，便能沿着索引、表示、采样、召回和排序找到影响来自哪里。一个可靠的检索推荐系统，正是由这些可检查的环节连接起来的。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M23.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Robertson et al., Okapi at TREC-3 (1994)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/okapi_trec3.pdf)

   词频、长度与检索评价的原始问题。

   Primary paper; no figure copied
2. [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/)

   倒排、词权重、向量空间与检索评价。

   Authors’ public text; reference
3. [Faiss — Getting started](https://github.com/facebookresearch/faiss/wiki/Getting-started)

   精确向量搜索接口及近似索引的核对基准。

   MIT project
4. [Dive into Deep Learning — Matrix Factorization](https://d2l.ai/chapter_recommender-systems/mf.html)

   因子模型原图与观察评分拟合。

   Figure CC BY-SA 4.0, unmodified
5. [Rendle et al. (2009), Bayesian Personalized Ranking](https://proceedings.mlr.press/r7/rendle09a.html)

   隐式反馈三元组与成对排序。

   Primary reference
6. [TensorFlow Recommenders — Basic retrieval](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

   查询塔、物品塔与召回—排序分工。

   Official tutorial; independent PyTorch experiment
7. [XGBoost — Learning to rank](https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.html)

   query group、LambdaMART与位置偏差。

   Apache-2.0 project
