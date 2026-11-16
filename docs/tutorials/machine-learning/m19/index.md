# 图像与文字怎样会合：多模态对齐与融合

Source: https://ml-biomat.com/tutorials/machine-learning/m19/
Language: zh-CN

从配对检索走向视觉问答，检查每种模态究竟提供了什么信息。

## 1. 用一句话寻找图片，为什么需要两种表示？

在相册里输入“窗边的一只黑猫”，我们希望系统找到符合这句话的图片，即使文件名没有这些词。视频会议中的字幕要把声音与画面对应起来，机器人则可能同时使用摄像头、触觉和语言指令。这些任务都需要连接不同模态：它们记录世界的方式不同，像素、词语、声波或传感器读数没有天然统一的坐标。多模态学习要建立可用于比较、互补或推理的关系，而不是把几种文件放进同一个文件夹就算完成融合。

图文检索提供了一个清楚的入口。图像编码器把像素变成向量，文本编码器把词语变成另一个向量，训练使对应的图文在共享空间里更接近。之后，文字可以寻找图片，图片也可以寻找描述。这里的“接近”是为任务学出的关系：两张图片的颜色可以差很多，却都对应“骑自行车的人”；两句话用词不同，也可能描述同一个场景。向量应当保留哪些差别，取决于训练配对和评价目标。

本章先解释配对数据与对比目标，再把检索接到融合、视觉问答和图像描述。完整实验使用九种颜色与形状组合，训练小型图像编码器和两词文本编码器，所有图片由代码生成。我们将删除颜色、替换描述或把图像置空，观察模型还保留什么能力。这个实验让读者检查跨模态计算本身；涉及大型视觉语言模型时，再明确连接模块、训练信号和生成输出分别承担什么作用。

## 2. 配对数据告诉模型什么才是“同一件事”

一张图片配一句描述，是一种弱于逐像素标注、又比完全无标签更丰富的监督。描述往往只提到场景中的部分内容，例如“孩子在踢球”没有说出衣服颜色，也没有给出球的位置。训练不能把未提及的物体都当作不存在。反过来，网页旁边的文字也可能是在评论、讲背景或引用别处内容，未必准确描述图片。构造数据集时，应检查图片与文字的关联单位、重复记录和错配比例，再决定把什么作为正例。

视频与音频还要处理同步。画面帧每秒几十张，声音每秒有几千到几万个样本，字幕又是长短不一的句子；三者不应按相同数组下标硬配。可以给每种模态保留时间戳，再按事件窗口、片段或对齐模型建立对应。若说话声比嘴部动作晚了半秒，模型可能学习到错误的同步关系。多个传感器同样需要统一时钟、空间标定和延迟定义；数据是否配对正确，先于网络是否足够复杂。

早期多传感器融合常依赖共同物理坐标，把不同测量汇入同一个状态估计；图像描述与跨媒体检索则推动了语义层面的连接。CLIP 的 2021 年工作把大规模图文配对、两个编码器和批内对比目标结合起来，并用文字描述类别，实现无需为每个新数据集重新训练分类头的迁移方式。它将“图片应该归到哪个固定编号”改成“图片与哪些语言概念匹配”，由此使检索与分类可以共享同一套表示。

![图像与文字分别编码，训练匹配对角线，使用时与候选描述比较。](https://ml-biomat.com/static/tutorials/machine-learning/figures/308a3ca4503f1c7a07803916.png?v=308a3ca4503f)

图 1CLIP 官方图：左侧为图文批内对比训练，右侧为文字类别编码与新图匹配。原图未修改。OpenAI / Alec Radford 等，2021，CLIP 仓库，MIT；Copyright (c) 2021 OpenAI。

图中的左侧对应训练：一批图片与一批文字形成两两相似度矩阵，原始配对位于对角线上。右侧对应使用：先把候选类别写成描述，再编码成文字向量，与新图片比较。训练目标和使用流程因此相连，但不完全相同。候选标签、提示句和评价数据仍由具体任务定义；当所有正确类别都被排除在候选集合外，系统仍会选出其中最相似的一项。检索系统需要让“相对更像”与“实际符合要求”各有对应的判断步骤。

## 3. 对比学习把一批配对变成许多个比较

两个编码器原先产生的向量可能具有不同尺度。先分别除以自身长度，就能用单位向量的点积表示余弦相似度，把比较集中到方向。假如图像向量是 (3,4)，归一化后为 (0.6,0.8)；文字向量是 (0,2)，归一化后为 (0,1)，两者相似度为 0.8。这个数描述当前表示里的方向接近程度，不直接等于“描述正确的概率”。学习过程会改变向量方向，使需要匹配的图文更容易被检索到。

$$
u_i=\frac{f_\theta(I_i)}{\|f_\theta(I_i)\|_2},\quad v_j=\frac{g_\phi(T_j)}{\|g_\phi(T_j)\|_2},\quad s_{ij}=u_i^\mathsf Tv_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1fcdf58caca1138f7dbea3ab.svg) | 第 i 张图像与第 j 条文字；图像输入为通道×高×宽，文字为 token 索引序列。 |
| ![Formula](https://ml-biomat.com/static/agent-math/474d65e369924067d1723f94.svg) | 图像与文本编码器，参数分别为 θ 与 φ；输出均为 d 维向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ab7d58f94422b5ef65d1d1a3.svg) | 向量各分量平方和的平方根，即欧几里得长度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7545db240f9c712bc65dd786.svg) | 归一化后的单位向量，形状 d，数值无物理单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/77ea99ae0a08426e8a150aa9.svg) | 图文余弦相似度与转置符号；s 在 −1 到 1 之间，无量纲。 |

归一化把两向量的长度都变为 1，点积于是只由夹角决定。图像向量 (3,4) 长度为 5，文字向量 (0,2) 长度为 2，归一化后点积为 0.6×0+0.8×1=0.8。完整批次的图像与文字矩阵都为 B×d，图文相似度矩阵因此为 B×B。计算时给零附近的长度设置数值下限，避免除零；本章模型输出均通过非零向量归一化检查。

在含有 B 对图文的批次里，每张图都与 B 条文字比较，每条文字也与 B 张图比较。把相似度除以温度，再经过 softmax，得到在当前候选集合内的归一化分数。图像到文字的交叉熵希望正确配对在该行占较大权重，文字到图像则对列做同样的事，两个方向取平均。一次训练因而不仅告诉模型“这一对相配”，也告诉它当前这批其他候选怎样与这一对区分。

$$
\begin{aligned}p_{ij}^{I\to T}&=\frac{e^{s_{ij}/\tau}}{\sum_{k=1}^{B}e^{s_{ik}/\tau}},\quad p_{ij}^{T\to I}=\frac{e^{s_{ij}/\tau}}{\sum_{k=1}^{B}e^{s_{kj}/\tau}},\\ \mathcal L&=-\frac1{2B}\sum_{i=1}^{B}\left[\log p_{ii}^{I\to T}+\log p_{ii}^{T\to I}\right].\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/90f0f365b8310a24e7aef8d8.svg) | 批次配对个数与图像、文字、求和候选索引；整数，对角线为正配对。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5a76efbbccbee7d654438e30.svg) | 图像 i 与文字 j 的无量纲余弦相似度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 正温度，无量纲；本实验固定为 0.12。 |
| ![Formula](https://ml-biomat.com/static/agent-math/09e083d7d5ed203c25a70d38.svg) | 分别沿文字候选行、图像候选列归一化的分数，均为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a37d71725f7b516cbb9cf38.svg) | 两个检索方向平均的负对数损失；log 使用自然对数，损失以 nat 计。 |

正确配对的分数进入对数，概率越接近 1，损失越接近零。若 B=2，相似度矩阵为对角线 1、非对角线 0，τ=1，则每个正确项的归一化分数都是 e/(e+1)≈0.731，双向平均损失为 −ln(0.731)≈0.313。除以 2B 是对两个方向、B 个样本共同取平均。稳定实现先减去每行最大 logit 再做指数，交叉熵函数已包含这类数值处理。

温度调节分数的尖锐程度。较小温度会放大相似度差异，让最高项占据更多权重；较大温度让分布更平缓。改变温度并不改变同一组相似度的排序，却会改变损失和梯度。候选集合也会改变归一化分数：三个分数为 1、0、−1 时，第一项的 softmax 约为 0.665；去掉最后一项，第一项就变为约 0.731，尽管前两项原分数完全没动。因此展示检索分数时，应把候选数量、温度和筛选规则一起说明。

批内其他配对不一定都是真负例。两张图片可能同样是一只黑猫，两段描述也可能表达相同含义；硬把其中一个配对当正例、其余语义相同项当负例，会给模型互相冲突的目标。可用多个正例、去重或根据语义关系调整采样。本章每批从九种类别中各取一张图，并各配唯一的颜色—形状描述，使批内九条描述各有明确差别；测试时同一描述对应十二张图片，则把这十二张都当作有效检索结果。

文本表示也决定了哪些差别能进入学习。两个词嵌入取平均，足以处理本章角色明确的颜色—形状描述，却会丢失词序：把“狗追猫”与“猫追狗”只按词袋平均，结果相同。上下文编码器可以表达角色关系，训练配对仍需奖励这种区分。图像全局向量也可能保留“有狗、有猫”，却没有保留谁在追谁。困难负例可以只改变关系、保留熟悉物体，让模型必须利用关系信息才能完成匹配。

## 方向、温度与候选集合怎样改变分数

图像向量沿单位圆移动，三个文字候选分别指向 0°、90° 和 180°。点积给出真实余弦相似度，右侧按温度归一化。移除候选 C 时，其余相似度不变，归一化分数却会变化。这里的向量是可手算的二维例子。

[Figure: 单位向量、余弦相似度与候选集合归一化分数](https://ml-biomat.com/tutorials/machine-learning/m19/#M19-svg)

## 4. 共享向量适合检索，但检索还要定义正确答案

双编码器的一个实用优点是可以提前计算候选库。十万张图片各保存一个向量，用户输入新文字时，只需编码这句话并查找邻近向量。精确点积在规模不大时容易实现，大规模索引可使用近似最近邻方法缩短查询时间。近似索引的速度、内存与召回之间存在取舍，应分别评价编码器的语义排序和索引本身是否找回正确近邻，否则无法判断错误来自表示还是检索工程。

$$
\mathrm{Recall@}K=\frac1Q\sum_{q=1}^{Q}\mathbf1\left\{\operatorname{TopK}(q)\cap P_q\ne\varnothing\right\}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1dd54bf48f8df143cf906dae.svg) | 查询总数与查询索引，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 保留的最高排名候选个数，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9de5b2fc3f1abf86192ff2a0.svg) | 查询 q 返回的前 K 个候选的标识集合。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c9c67b23ff454476a93a644.svg) | 查询 q 的有效正例集合，按任务语义定义。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3d32668ccce2a39a546eee99.svg) | 集合交集、空集与指示函数；有交集时该查询计 1，否则计 0。 |

这里采用检索研究常见的“每个查询是否至少命中一个正例”定义。四个查询中有三个的前五项包含有效正例，Recall@5 就是 3/4=0.75。本实验每条文字有十二张满足颜色与形状的测试图片，返回其中任何一张都算命中。这个定义不同于“找回正例个数/全部正例个数”的集合召回率，因此要连同正例关系一起说明。

Recall@K 要先定义每个查询的正例集合。若问题是“找这张照片对应的原始说明”，可能只有一条正确记录；若问题是“找红色圆形”，许多图片都符合。本章的文字到图片评价采用后一种语义定义，每条文字有十二张有效测试图片，只要前 K 项中至少出现一张就算该查询命中。九个文字查询的命中率与一百零八个图片查询的命中率，分母不同；把两个方向分别报告，可以看出查询难度与库结构的差别。

文本提示也构成输入的一部分。“猫”“一张猫的照片”和“猫的医学插图”会给文本编码器不同上下文。可以预先确定若干提示模板并组合它们的表示，但模板选择与验证应在测试前完成。所谓零样本迁移通常指没有用目标任务的带标签训练集拟合该分类器，并不是模型没有见过相关语言或视觉概念。本章的小模型在九种组合上训练，再评价这些组合的新图片，因此称为配对检索实验，不把它描述成开放世界的零样本识别。

检索还能作为生成系统的一个环节。先从图像库、视频片段或文档图表中找出候选，再让更昂贵的联合模型逐对精排，最后生成带证据的回答。双编码器擅长把库提前编码，交叉编码器则可以在每个候选与问题之间进行细粒度交互，两者的计算位置不同。要提高一条完整链的质量，应记录正确材料有没有进入候选、精排是否保留它、最终回答是否使用了其中内容，而不是只看最后一句话是否流畅。

## 5. 融合让模态在计算过程中互相提问

检索让两个向量可比较，融合则让不同模态共同决定输出。早期融合把已对齐的特征拼接后交给共同模型；后期融合分别计算预测，再按权重组合；中间融合则让各自编码的特征在网络内部交换信息。前两种方式容易作为基线，但拼接必须处理维度与尺度，后期组合也可能错过需要局部图文对应的关系。问题若是“左边那个杯子是什么颜色”，一句话与整张图各压成一个全局向量，可能不足以保留所需的位置关系。

$$
A=\operatorname{softmax}_{\rm rows}\!\left(\frac{QK^\mathsf T}{\sqrt{d_k}}\right),\qquad O=AV
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 查询矩阵，n_q×d_k；例子中来自文字表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 键矩阵，n_v×d_k；例子中来自图像区域。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 值矩阵，n_v×d_v；与键对应的区域内容表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b9e52f7fbff1603ac8625d14.svg) | 查询数量、视觉位置数量、键维度和值维度，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f1efaf107177724d3c2807e7.svg) | 逐行归一化的注意力权重 n_q×n_v，以及汇总输出 n_q×d_v。 |
| ![Formula](https://ml-biomat.com/static/agent-math/17c6a1d9c8dc7a1a58d9ebfd.svg) | 缩放因子与转置；神经表示和权重均无指定物理单位。 |

查询先与每个键比较，再用对应权重读取值。一个查询对两个区域的 logit 为 ln3 和 0 时，softmax 权重为 0.75 和 0.25；若对应值为 (2,0) 与 (0,4)，输出就是 (1.5,1)。缩放因子控制维度增加时点积的典型尺度。多个头可以并行读取不同关系，但每个头仍遵循这套矩阵形状；交叉注意力与自注意力的关键差别是查询和键值来自不同序列。

交叉注意力把一侧的查询与另一侧的键和值连接起来。以一个文字查询为例，它可对多个图像区域算权重，再加权读取这些区域的表示。问“颜色”时，查询应把注意力分配到目标物体；问“有几个”时，模型需要保留多个实例及其关系。权重是计算中的信息汇总系数，不能单凭一张注意力热图就认定模型的完整推理原因。可以进一步遮挡高权重区域、替换物体或改变问题，检查输出是否按预期变化。

视觉语言模型通常把视觉编码器、连接模块和语言生成模型组合起来。BLIP-2 用可学习查询构成的连接模块，从冻结视觉编码器读出与语言有关的信息，再与冻结语言模型衔接，分阶段学习跨模态表示和生成关系。Flamingo 的工作则研究如何在预训练视觉与语言模型之间加入连接，使图像或视频能够与文字交错输入。这些设计回应同一个成本问题：已有模型各自掌握大量知识，怎样训练一个合适的接口，让它们能够交换信息？

冻结底座并不表示所有计算都免费。视觉编码仍要处理像素，语言生成仍需逐步输出 token；可训练参数少与推理耗时低是不同指标。图像分辨率、视觉 token 数、连接模块的压缩方式以及上下文长度，都影响保留的细节和计算量。阅读一个 VLM 方案时，应画出像素经过哪些表示、在哪里转成语言模型可接收的向量、哪些参数更新、哪些损失参与训练，输入输出的对应关系就会比模型名称更清楚。

## 6. 描述、问答与音视频，需要不同的证据

图像描述根据图片生成一段文字，训练常以参考描述作为目标，让模型逐词预测；视觉问答还给出一个问题，答案必须回应问题指定的信息。一张桌上有两个杯子的图片，可以被描述成“桌上放着杯子”，却不能用这句话正确回答“有几个杯子”。同一张图也可能有多个合理描述，因此纯粹比较词面重合会漏掉同义表达，同时可能奖励听起来相似但事实错误的句子。评价应同时检查对象、属性、数量和关系是否与图像一致。

$$
p(y_{1:L}\mid I,q)=\prod_{t=1}^{L}p(y_t\mid y_{<t},I,q),\qquad \mathcal L_{\rm gen}=-\sum_{t=1}^{L}\log p(y_t\mid y_{<t},I,q)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8c4a7d4e66f9edd248c8f073.svg) | 图像输入与问题文本；图像描述任务可以省略问题。 |
| ![Formula](https://ml-biomat.com/static/agent-math/01e84314ba118beefe8bc70f.svg) | 第 t 个答案 token 与它之前的答案前缀。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc947ed58e2957c8badfe9da.svg) | 答案长度（包含训练定义的结束符）及 token 位置，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 以图像、问题和已有前缀为条件的 token 概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8fdd277f9908d04b494d21d3.svg) | 整句负自然对数似然，nat；训练也可按有效 token 数取平均。 |

链式分解把一整句的概率写成逐步条件概率。若正确的两个输出 token 概率分别为 0.8 与 0.5，序列概率是 0.4，负对数损失约为 0.916。训练时常把真实前缀交给模型，生成时则使用已经生成的前缀，二者的输入分布可能不同。损失要求模型复现监督答案；是否真正依据图像，还需配合遮挡、问题单模态基线和逐项事实评价。

文档问答尤其依赖视觉前处理。把整页缩成小方图可以保留版面，却可能抹掉单个字母；分块裁剪能保留细节，但会增加视觉 token，并需要保存每块的位置。某些问题应先定位区域、提取文字，再解释其中数字，而不是把整页当一幅普通场景图。答案若同时给出对应区域或页内位置，读者就能核对模型引用的证据。这样的输出要求应提前影响分辨率、裁剪和标注方式。

有些错误来自语言先验过强。例如训练数据中“香蕉是什么颜色”经常回答黄色，模型可能在没有看清图片时沿用这个常见答案。可以用改变颜色的图像、遮掉关键区域的图像以及图文互相矛盾的组合做受控测试。每次只改变一项，观察答案是否随视觉证据变化，再与只输入问题的基线比较。若问题需要读图表数值，还要保留单位、坐标和误差范围；如果图片分辨率已经丢失细小文字，后续语言生成不能从不存在的像素中恢复可靠读数。

音视频理解增加了时间关系。画面中的开门动作可能早于关门声，人物说话的口型应与相应音频片段对齐，事件检索还要返回开始和结束时间。模型可以先分别编码帧、短音频段与文字，再用时间位置和跨模态注意力连接它们。抽帧间隔太大可能漏掉短事件，把音频整体平均也可能丢掉先后顺序。视频字幕、事件描述、声音来源定位和情绪判断分别需要不同粒度的监督，不能只用整段主题标签替代所有任务。

## 7. 完整实验：颜色与形状怎样在两个空间里会合

代码生成红、绿、蓝三种颜色与圆、方、三角三种形状的九个组合。每种组合分别生成 32 张训练图、8 张验证图和 12 张测试图，位置、大小、亮度、背景与像素噪声变化，三组随机种子独立。图像分辨率为 28×28，图像编码器有两层卷积，最后输出 24 维向量；文本使用颜色与形状两个词的可训练嵌入，平均后经线性层得到同样维度。两侧向量都归一化，温度固定为 0.12。

![每种颜色—形状组合的一张独立测试图，真实像素为 28×28。位置、大小、亮度与噪声由独立种子生成。](https://ml-biomat.com/static/tutorials/machine-learning/figures/c8d0d5cce54f14362f471a56.svg?v=c8d0d5cce54f)

图 2每种颜色—形状组合的一张独立测试图，真实像素为 28×28。位置、大小、亮度与噪声由独立种子生成。

### 可从头运行的图文对比与缺失信息实验

小型卷积图像编码器与两词文本编码器从头训练，不下载大型权重。输出双向语义检索、矛盾颜色描述与消融结果，保存图、数组和 summary.json。

```
"""Small paired image-text experiment with explicit candidate sets and ablations."""
import argparse,copy,json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as PolygonPath
from sklearn.decomposition import PCA

torch.set_num_threads(2)
COLORS=np.array([[.85,.2,.18],[.18,.65,.3],[.15,.35,.85]])
CAPTIONS=['red circle','red square','red triangle','green circle','green square','green triangle','blue circle','blue square','blue triangle']
TOKENS=torch.tensor([[c,s+3]for c in range(3)for s in range(3)])

def dataset(perclass,seed):
    rng=np.random.default_rng(seed);images=[];labels=[];yy,xx=np.mgrid[:28,:28]
    for c in range(9):
        color,shape=divmod(c,3)
        for _ in range(perclass):
            cx,cy=rng.uniform(12,16,2);rad=rng.uniform(6,9)
            if shape==0:mask=(xx-cx)**2+(yy-cy)**2<=rad**2
            elif shape==1:mask=(abs(xx-cx)<=rad)&(abs(yy-cy)<=rad)
            else:mask=PolygonPath([[cx,cy-rad],[cx-rad,cy+rad],[cx+rad,cy+rad]]).contains_points(np.c_[xx.ravel(),yy.ravel()]).reshape(28,28)
            im=np.ones((28,28,3))*rng.uniform(.03,.15);im[mask]=COLORS[color]*rng.uniform(.8,1.1);im=np.clip(im+rng.normal(0,.025,im.shape),0,1)
            images.append(im.transpose(2,0,1));labels.append(c)
    return torch.tensor(np.array(images),dtype=torch.float32),np.array(labels)

class PairModel(nn.Module):
    def __init__(self):
        super().__init__();self.image=nn.Sequential(nn.Conv2d(3,12,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(12,24,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d((4,4)),nn.Flatten(),nn.Linear(384,24))
        self.words=nn.Embedding(6,24);self.text=nn.Linear(24,24,bias=False)
    def encode_image(self,x):return nn.functional.normalize(self.image(x),dim=1)
    def encode_text(self,t):return nn.functional.normalize(self.text(self.words(t).mean(1)),dim=1)
    def forward(self,x,t):return self.encode_image(x)@self.encode_text(t).T/.12

def recall_at(similarity,querylabels,candidatelabels,k):
    top=np.argsort(-similarity,axis=1)[:,:k]
    return float(np.mean(np.any(candidatelabels[top]==querylabels[:,None],axis=1)))

def run(out,language):
    out.mkdir(parents=True,exist_ok=True);zh=language=='zh';text=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
    save=lambda fig,name:(fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight'),fig.savefig(out/f'{name}-{language}.png',dpi=140,bbox_inches='tight'),plt.close(fig))
    torch.manual_seed(19);train,ytrain=dataset(32,19);valid,yvalid=dataset(8,119);test,ytest=dataset(12,219)
    model=PairModel();optimizer=torch.optim.Adam(model.parameters(),lr=.002);trace=[];best=float('inf');selected=0
    for step in range(1,301):
        model.train();idx=torch.arange(9)*32+torch.randint(32,(9,));optimizer.zero_grad();logits=model(train[idx],TOKENS);target=torch.arange(9)
        loss=(nn.functional.cross_entropy(logits,target)+nn.functional.cross_entropy(logits.T,target))/2;loss.backward();optimizer.step()
        if step%5==0:
            model.eval()
            with torch.no_grad():vl=nn.functional.cross_entropy(model(valid,TOKENS),torch.tensor(yvalid)).item()
            trace.append([step,loss.item(),vl])
            if vl<best:best=vl;weights=copy.deepcopy(model.state_dict());selected=step
    model.load_state_dict(weights);model.eval()
    torch.save(model.state_dict(),out/'paired-model.pt')
    (out/'model.json').write_text(json.dumps({'class':'PairModel','image_shape':[3,28,28],'embedding_dimensions':24,'vocabulary':['red','green','blue','circle','square','triangle'],'tokens':TOKENS.tolist(),'captions':CAPTIONS,'temperature':.12,'selected_step':selected},indent=2),encoding='utf-8')
    reloaded=PairModel();reloaded.load_state_dict(torch.load(out/'paired-model.pt',weights_only=True));reloaded.eval()
    with torch.no_grad():reload_error=float((model(test,TOKENS)-reloaded(test,TOKENS)).abs().max())
    with torch.no_grad():
        iz=model.encode_image(test).numpy();tz=model.encode_text(TOKENS).numpy();sim=iz@tz.T
        gray=test.mean(1,keepdim=True).repeat(1,3,1,1);gray_sim=(model.encode_image(gray)@model.encode_text(TOKENS).T).numpy()
        missing_sim=(model.encode_image(torch.zeros_like(test))@model.encode_text(TOKENS).T).numpy()
        shapeonly=model.encode_text(TOKENS[:3,1:]).numpy();shape_sim=(iz@shapeonly.T)[:,np.arange(9)%3]
    pred=sim.argmax(1);i2t=recall_at(sim,ytest,np.arange(9),1);t2i=recall_at(sim.T,np.arange(9),ytest,1)
    gray_pred=gray_sim.argmax(1);shape_pred=shape_sim.argmax(1)
    mean_sim=np.array([sim[ytest==k].mean(0)for k in range(9)])
    image_means=np.array([iz[ytest==k].mean(0)for k in range(9)]);pca=PCA(2);project=pca.fit_transform(np.r_[image_means,tz]);scores=(sim/.12);probs=np.exp(scores-scores.max(1,keepdims=True));probs/=probs.sum(1,keepdims=True)
    # Removing a candidate changes normalized scores but not remaining cosine similarities.
    hand=np.array([1,0,-1]);soft=np.exp(hand);soft/=soft.sum();soft_subset=np.exp(hand[:2]);soft_subset/=soft_subset.sum()
    summary={'train_images':len(train),'validation_images':len(valid),'test_images':len(test),'candidate_captions':9,'selected_step':selected,'i2t_recall1':i2t,'t2i_recall1':t2i,'i2t_recall3':recall_at(sim,ytest,np.arange(9),3),'gray_exact_accuracy':float(np.mean(gray_pred==ytest)),'gray_shape_accuracy':float(np.mean(gray_pred%3==ytest%3)),'missing_image_accuracy':float(np.mean(missing_sim.argmax(1)==ytest)),'shape_only_exact_accuracy':float(np.mean(shape_pred==ytest)),'shape_only_shape_accuracy':float(np.mean(shape_pred%3==ytest%3)),'image_norm_error':float(abs(np.linalg.norm(iz,axis=1)-1).max()),'text_norm_error':float(abs(np.linalg.norm(tz,axis=1)-1).max()),'paired_mean_cosine':float(np.mean(sim[np.arange(len(test)),ytest])),'pca_explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'hand_probabilities':soft.tolist(),'hand_subset_probabilities':soft_subset.tolist(),'semantic_positives_per_text_query':12,'embedding_dimensions':24}
    summary['contradictory_color_mean_cosine']=float(np.mean(sim[np.arange(len(test)),(ytest+3)%9]))
    summary['reload_logits_error']=reload_error
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'data.npz',test_images=test.numpy(),test_labels=ytest,image_embeddings=iz,text_embeddings=tz,similarity=sim,gray_similarity=gray_sim,shape_only_similarity=shape_sim,zero_image_similarity=missing_sim,trace=trace,pca=project)
    assert summary['image_norm_error']<1e-6;assert summary['text_norm_error']<1e-6
    labels=[z for z in CAPTIONS];zhlabels=[c+s for c in ['红色','绿色','蓝色']for s in ['圆形','方形','三角形']];names=zhlabels if zh else labels
    fig,axs=plt.subplots(3,3,figsize=(8,8),layout='constrained')
    for k,ax in enumerate(axs.flat):ax.imshow(test[k*12].permute(1,2,0));ax.set_title(names[k]);ax.set(xticks=[],yticks=[])
    save(fig,'pairs')
    fig,axs=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.4,1]},layout='constrained')
    im=axs[0].imshow(mean_sim,cmap='RdBu_r',vmin=-1,vmax=1);axs[0].set(xticks=range(9),yticks=range(9),xticklabels=names,yticklabels=names,xlabel=text('文字候选','Text candidate'),ylabel=text('真实图像类别','True image class'));axs[0].tick_params(axis='x',labelrotation=60);fig.colorbar(im,ax=axs[0],label=text('余弦相似度','Cosine similarity'))
    tr=np.array(trace);axs[1].plot(tr[:,0],tr[:,1],label=text('训练：双向','Train: symmetric'),color='#176b91');axs[1].plot(tr[:,0],tr[:,2],label=text('验证：图检索文','Validation: image to text'),color='#bd554c');axs[1].set(xlabel=text('优化步数','Optimization step'),ylabel=text('交叉熵','Cross entropy'));axs[1].legend();save(fig,'alignment')
    fig,axs=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1,1.15]},layout='constrained');marks=['o','s','^']
    for k in range(9):
        color=COLORS[k//3];v,w=project[k],project[9+k];axs[0].plot([v[0],w[0]],[v[1],w[1]],color=color,alpha=.5);axs[0].scatter(*v,c=[color],marker=marks[k%3],s=70);axs[0].scatter(*w,facecolors='none',edgecolors=[color],marker=marks[k%3],s=110)
    axs[0].set(xlabel=text('主成分 1','Principal component 1'),ylabel=text('主成分 2','Principal component 2'),title=text('实心：图像均值；空心：文本','Filled: mean image; open: text'))
    lab=[text('完整图文','Full pair'),text('灰度图像','Grayscale'),text('仅形状文字','Shape-only text'),text('全零图像','Zero image')];exact=[i2t,summary['gray_exact_accuracy'],summary['shape_only_exact_accuracy'],summary['missing_image_accuracy']];shape=[float(np.mean(pred%3==ytest%3)),summary['gray_shape_accuracy'],summary['shape_only_shape_accuracy'],float(np.mean(missing_sim.argmax(1)%3==ytest%3))]
    yy=np.arange(4);axs[1].barh(yy-.17,exact,height=.3,color='#176b91',label=text('颜色+形状均正确','Color and shape correct'));axs[1].barh(yy+.17,shape,height=.3,color='#bc8440',label=text('形状正确','Shape correct'));axs[1].set(yticks=yy,yticklabels=lab,xlim=(0,1.05),xlabel=text('正确率','Accuracy'));axs[1].invert_yaxis();axs[1].legend(loc='lower right',fontsize=9);save(fig,'ablation')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();run(args.output,args.language)
```

程序同时保存 paired-model.pt 与 model.json，包含所选权重、词表、架构说明与温度。重新建立 PairModel 并加载权重后，对同一批图文计算的logit最大差为0；data.npz还保存仅形状文字与全零图像的完整得分矩阵，方便逐样本比较。

每个优化步从九类中各选一张图，使用对称交叉熵训练，共进行 300 步，并以验证集图像到文字的交叉熵选择检查点。固定种子的实际结果中，108 个图片查询的 Recall@1 与九个文字查询的 Recall@1 都为 1.0。匹配描述的平均余弦相似度为 0.9591；只把颜色换成另一种、保留形状不变后，平均相似度降到 0.2416。后一个比较专门检验颜色是否参与匹配，而不是只报告九分类整体高分。

![左：108 张测试图按真实类别分组后的平均余弦相似度；右：训练的双向交叉熵与验证的图像到文字交叉熵，两个目标方向在图例中区分。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b854ed093396f44153af1373.svg?v=b854ed093396)

图 3左：108 张测试图按真实类别分组后的平均余弦相似度；右：训练的双向交叉熵与验证的图像到文字交叉熵，两个目标方向在图例中区分。

图像变成灰度后，形状正确率仍为 1.0，颜色与形状同时正确的比例降为 1/3。文字只保留形状词时也是如此；代码把同一形状的分数复制到三个颜色候选，明确按候选顺序处理并列。全零图像的联合正确率为 1/9。缺失信息没有通过模型凭空补回，剩余形状线索却仍能工作。图中的二维投影只保留前两个主成分，解释约 52.8% 的变化；相近位置用于辅助观察，真正检索仍使用完整 24 维向量。

![左：图像类均值与文本向量共同作 PCA，前两成分解释约 52.8% 方差，实心/空心标记对应两个模态；右：固定模型在缺失颜色、缺失文字颜色词和全零图像条件下的实测正确率。](https://ml-biomat.com/static/tutorials/machine-learning/figures/574629a8bef616fe043069b8.svg?v=574629a8bef6)

图 4左：图像类均值与文本向量共同作 PCA，前两成分解释约 52.8% 方差，实心/空心标记对应两个模态；右：固定模型在缺失颜色、缺失文字颜色词和全零图像条件下的实测正确率。

训练与检索时的矩阵形状也有区别。每批训练是九张图片对九条唯一描述，形成方阵；测试是一百零八张图片对九条描述，形成矩形矩阵。行方向回答图片找文字，列方向回答文字找图片。若把只认对角线的一一匹配规则直接搬到测试矩阵，就会错误惩罚每条描述对应的其他有效图片。代码因此把类别关系与向量一起保存，按语义正例集合评价。维度检查在这里直接关系到指标是否回答了正确问题。

这些消融按固定模型执行，没有在每种缺失条件下重新训练。因此，它们回答的是当前编码器对输入变化的反应，而不是经过专门适配后的最高性能。若应用经常缺失某种模态，可以在训练中加入模态丢弃、显式缺失标记或可用性门控，再用相同缺失模式评价。灰度、模糊、遮挡与完全缺失也应分别测试，因为它们保留的信息不同；把所有退化输入都叫“噪声”，会掩盖具体该改哪一步。

## 8. 让评价检查模态的贡献与互相矛盾的证据

输入消融与重新训练回答不同问题。从训练好的多模态模型中删掉文字，是检查这个具体模型失去文字后的反应；另训练一个计算资源相当的纯图像模型，则是在问图像单独能把任务做到什么程度。两项比较都值得做，却不应都含糊标成“无文字”。更完整的研究可以交叉比较训练条件与可用模态，固定评价样本，并说明参数量或计算量差异，从而区分信息互补、模型容量与训练预算带来的收益。

一个多模态系统可能在表面上接收很多输入，却主要依赖其中一种。只输入文字、只输入图像、随机打乱配对、替换不相关区域和删除关键区域，可以构成一组有解释力的基线。打乱配对后性能若几乎不变，就应检查标签是否已经能从单一模态猜出，或是否存在数据泄漏。对需要互补信息的任务，还可以选择每种单独模态都无法确定答案、两者结合才能确定的样本，让融合的收益对应到任务结构。

偏差检查同样需要具体维度。图文数据可能把某些职业与外观、某些物体与特定背景频繁绑定；模型因而利用了相关性，却没有学到预期属性。按场景、语言、对象组合或拍摄条件分组查看错误，再改变背景但保留物体，能够帮助定位依赖。评价数据应按原始图片或视频去重与分组，避免同一内容的不同裁剪、字幕版本或压缩副本跨越训练和测试。组合泛化还需要留出未见过的属性组合，不能用见过组合的新图片代替。

最后，按输出任务保存合适的证据。检索保留查询、候选库和排序；问答保留问题、图片与逐项答案判定；描述检查语义覆盖和事实一致；音视频定位记录时间容差与同步方式。测量延迟、内存和缺失模态时的行为，能把模型质量与实际使用连接起来。多模态学习的价值在于让互补线索共同支持判断：共享空间解决怎样比较，融合解决怎样交换信息，任务评价则检验这些信息是否真正进入了答案。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M19.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [CLIP official repository and original diagram](https://github.com/openai/CLIP)

   原作者图文编码和零样本分类示例；原图按 MIT 采用。

   MIT; Copyright (c) 2021 OpenAI; https://raw.githubusercontent.com/openai/CLIP/main/LICENSE
2. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)

   图文对比目标与迁移评估的原始论文。
3. [BLIP-2](https://arxiv.org/abs/2301.12597)

   冻结视觉、语言模型与查询连接模块。
4. [Flamingo](https://arxiv.org/abs/2204.14198)

   交错图文、视频与少样本视觉语言任务。
