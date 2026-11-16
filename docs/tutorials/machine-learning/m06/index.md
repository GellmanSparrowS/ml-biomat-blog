# 寻找没有标签的结构：从PCA到聚类与异常

Source: https://ml-biomat.com/tutorials/machine-learning/m06/
Language: zh-CN

用真实数字图像、形状对照与误报记录，检查压缩、分组和二维地图保留了什么。

## 没有答案标签，也可以提出清楚的问题

把手机相册中的照片整理成几组，看起来像一件很自然的事：同一个人的照片放在一起，旅行照片按地点分开，再找出几张模糊或重复的图片。但“相似”其实有许多含义。一张海边合影可以因为人物相同而靠近室内肖像，也可以因为蓝色背景而靠近天空照片。无监督学习面对的正是这种处境：数据已经存在，却没有一列标准答案规定应该怎样组织它们。算法需要一个可计算的目标，而读者需要先决定希望保留哪一种关系。

本节把四种目标放在同一条理解线上。降维用更少的数字描述对象，聚类把对象组成若干组，密度估计描述哪些区域更常出现，异常检测则为值得检查的记录安排优先级。它们可以连接使用，但输出并不相同。一张二维地图给出坐标，聚类给出组号，密度给出单位体积内的概率集中程度，异常分数给出某种定义下的不寻常程度。先说清最终要浏览、压缩还是报警，后面的距离、参数和评价指标才有依据。

主要实验使用 scikit-learn 随库提供的1797幅八乘八手写数字图像，原数据来自 UCI 的 Optical Recognition of Handwritten Digits，由 E. Alpaydin 与 C. Kaynak 的相关工作整理，数据采用 CC BY 4.0 许可。每幅图像变成64个像素值，除以16后落在0到1之间。实验另外生成月牙、椭圆和正常与异常观测，以便把已知的生成机制与算法结果对照。数字标签只用于分层划分和最后给地图着色，PCA、t-SNE、UMAP的拟合不读取这些标签。

## 相似性从量尺开始

想象用价格和重量整理商品。两件商品相差100元、0.1千克，把原始数值直接平方相加，价格差几乎决定了全部距离；若价格改成以万元记录，结论又会改变。物品本身没有变化，变化的是量尺。标准化先减去训练样本的均值，再除以训练样本的标准差，把差异表达为“偏离常见值多少个标准差”。这样可以减少数值尺度的支配，但也意味着把每一列的典型波动放到相近地位，这仍然是一项建模选择。

$$
z_j=\frac{x_j-\mu_j}{s_j},\quad d(z,v)=\sqrt{\sum_{j=1}^{d_f}(z_j-v_j)^2},\quad \operatorname{cos}(a,b)=\frac{a^\mathsf Tb}{\|a\|_2\|b\|_2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/212957f061a4837e3688ae41.svg) | 第j个原始特征、训练均值、正训练标准差与特征索引；前三者具有相同特征单位，零方差列需另行处理。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f0a4b57a130481b83378460b.svg) | 标准化特征向量、另一个标准化向量、特征数与欧氏距离；标准化后的坐标和距离无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/de4a4793c577391ef6bbe08e.svg) | 非零且同维的向量、欧氏长度、转置与余弦相似度；相似度无量纲，两向量使用相同坐标单位约定。 |

价格120元、重量12千克，训练均值分别100元与10千克、标准差20元与2千克，标准化后为(1,1)，到均值的标准化距离√2。向量(1,0)与(2,0)的欧氏距离为1、余弦为1：长度不同但方向相同。

欧氏距离适合把各坐标差异看作可以累积的几何位移。余弦相似度关注方向：两篇文章的词频向量即使长度不同，只要各词比例相近，方向也可能相近。曼哈顿距离把各坐标绝对差相加，马氏距离进一步利用协方差，对高度相关的变化作不同处理。选择时应把数值关系翻译回问题：总购买量重要，还是购买比例重要；两项高度相关的测量是否反复表达了同一件事。零向量的余弦方向没有定义，需要事先规定处理方式。

本节数字图像的64个坐标都是同一量纲的灰度，统一除以16便能保留像素间相对差异。若对每个像素分别标准化，原本几乎总是黑色的边缘像素会因微小波动被放大，图像距离也随之变化。图像平移一格还可能产生较大像素距离，尽管人仍看见同一个数字。这说明原始像素是一种具体表示；以后换成神经网络特征时，也应重新检查哪些变换被保留、哪些被忽略。距离从来与表示方式共同工作。

维度增多时，许多互不相关的噪声坐标会累积到距离中，使真正有用的差异不再突出。解决方法包括删去无信息特征、按任务选择特征权重，或先学习较低维的表示。这里的“先”也涉及评估顺序：若要处理未来数据，均值、尺度和降维方向都在训练集上学习，再应用于新对象；若只是浏览当前固定收藏，则可以明确把整个收藏作为描述对象。两种任务各有合理流程，关键是对应最终用途。

## PCA保留的是变化，压缩损失可以算出来

用一根直线代表一片散点云，最直观的办法是让点到直线的垂直距离尽可能小。Pearson在1901年讨论最贴近空间点集的直线和平面，已经把这种几何问题写进统计研究。PCA延续了这个思路：先把点云移到均值处，再寻找彼此垂直、能够保留最多变化的方向。第一方向沿点云最伸展的方向，第二方向在与第一方向垂直的条件下保留剩余变化。这里的“重要”由方差定义，尚未涉及哪种差异对分类或研究问题最有用。

$$
z_i=V_k^\mathsf T(x_i-\mu),\quad\widehat x_i=\mu+V_kz_i,\quad E_k=\frac1n\sum_{i=1}^n\|x_i-\widehat x_i\|_2^2,\quad V_k^\mathsf TV_k=I_k
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10d2411af09e9ba80eb7f88b.svg) | 观测数、索引、原始特征维度和保留分量数，k不超过原始维度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e00cb86ad595f6fecb8e7e9d.svg) | d_f维原始向量、训练均值与重建向量；本例为统一缩放后的无量纲像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c271bce45296621ac9590a40.svg) | d_f×k正交列方向矩阵、k维投影坐标与k×k单位矩阵；方向无量纲，坐标与输入同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc49eec661d93602ca36b4ac.svg) | 每条观测的总平方重建误差平均值与欧氏长度；E为输入单位平方。图像报告的每像素MSE再除以64。 |

中心为零时，点(2,1)沿水平单位向量(1,0)投影得到坐标2、重建(2,0)、平方误差1。原平方长度5分成保留长度平方4与残差平方1。正交性使交叉项为零，因此保留方差最大时重建平方误差最小。

投影像把立体物体照出影子。换一个照射方向，影子可以保留物体的长轴，也可能把长轴压成一小点。对于正交投影，原向量可以分成沿保留方向的部分和垂直残差，两部分平方长度相加等于原平方长度。因此，总变化固定时，最大化保留的方差与最小化重建平方误差是同一件事。交互中五个点的总均方长度为2.56，投到水平轴会留下2、丢掉0.56；转动方向，可以直接看到这两部分此消彼长。

## 把点云投到一条线上

蓝点为五个中心化观测，橙点为正交投影，连接线表示重建残差。拖动角度或选中一个点，比较保留方差、丢失方差和该点的残差。坐标均无量纲。

[Figure: 正交投影与方差分解](https://ml-biomat.com/tutorials/machine-learning/m06/#M06-plot)

数字实验将1347幅图像用于学习PCA方向，另外450幅只用于重建检查。保留两个分量时，测试像素均方误差约0.05277；十个分量降至0.01954，二十个降至0.00837，四十个降至0.000919。图中每一列始终是同一幅留出图像，从上到下增加分量，读者能看出哪些笔画先回来。所有图采用同一灰度范围，因此“看起来更清楚”与数值误差有可比较的尺度。

![六幅留出数字沿列排列，从原图逐步增加PCA重建分量；右侧是450幅留出图像的像素均方误差及训练累计方差比例。图像灰度范围固定0到1。数据：UCI Optical Recognition of Handwritten Digits，CC BY 4.0；本图为计算结果。](https://ml-biomat.com/static/tutorials/machine-learning/figures/46444a9210e2d30448fb8ac3.svg?v=46444a9210e2)

图 1六幅留出数字沿列排列，从原图逐步增加PCA重建分量；右侧是450幅留出图像的像素均方误差及训练累计方差比例。图像灰度范围固定0到1。数据：UCI Optical Recognition of Handwritten Digits，CC BY 4.0；本图为计算结果。

保留64个分量后，重建误差接近浮点舍入量级，这是完整正交基能够表达原空间的结果。与此同时，二十个分量已经保留约89.6%的训练方差，却仍可能丢失区分两个相似数字的一小段笔画。压缩任务关心重建质量，分类任务则要进一步测量预测效果。累计方差比例是读图工具，不是通用的“足够好”标准。若噪声恰好具有很大方差，PCA也会优先保留它；低方差但有判别力的方向需要借助监督目标或领域知识识别。

## 一组的含义，由聚类规则决定

k-means把每个点交给最近的中心，再把每组中心移到组内均值，两步交替进行。固定中心时，最近中心使每个点的平方距离最小；固定分组时，算术均值使组内平方偏差和最小。这解释了为什么更新通常让目标下降，也解释了它偏爱围绕中心展开的紧凑组。初始中心不同可能走向不同局部解，所以代码使用多次初始化。组数增加会让训练距离继续减小，选择组数还需要稳定性、解释用途或其他评价，不能只追求最小训练误差。

$$
J=\sum_{i=1}^n\|x_i-c_{g_i}\|_2^2,\qquad c_k=\frac1{|A_k|}\sum_{i\in A_k}x_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43f2ec92374b1c86b9b64c3e.svg) | 样本数、索引与d_f维特征向量；特征已按相同尺度约定处理。 |
| ![Formula](https://ml-biomat.com/static/agent-math/14399b8dddaeab27160ff5ed.svg) | 组数、组索引、样本所属组号、组中心、该组样本集合与非零样本数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/614eb99191286bb013cad6c9.svg) | 总平方距离目标与欧氏长度；目标为特征单位平方，标准化数据时无量纲。 |

一维点(0,2,8,10)分成前后两组时，中心分别1与9，总平方距离1+1+1+1=4。全部放一组中心5，总平方距离25+9+9+25=68。增加组数可以降低训练目标，因此还需要选择复杂度的依据。

月牙数据把这一偏好显示得很直接。两条弯曲月牙各自连贯，但同一月牙的两端离自己的均值很远；k-means容易从中间划出几何上紧凑的区域。层次聚类则从单个对象开始反复合并，树状图记录整个过程。单连接比较两组之间最近的点，容易顺着细长链条连接；完全连接比较最远点，更强调一组的最大跨度；Ward方法选择使组内平方误差增加最少的合并。这里没有统一的“最近”，每种连接准则都规定了不同的组间关系。

DBSCAN换了一个问题：哪些点周围有足够多的邻居，密集区域能否连续连接。给定半径和最小样本数，邻域内数量足够的点成为核心点；邻近核心点但自身邻居不够的点可以作为边界点，远离这些区域的点标为噪声。代码中的最小样本数包含点自身。核心点之间沿密集邻域传递连接，因此可以找到弯曲形状，也不要求事先给出组数。不同区域密度差异很大时，一个统一半径可能同时把稀疏组打散、把稠密组附近的区域连在一起。

![相同500点月牙与500点椭圆数据分别经过三种算法。颜色表示算法分组，灰色为DBSCAN噪声；ARI用生成标签评价分组一致性，噪声数同时显示。](https://ml-biomat.com/static/tutorials/machine-learning/figures/16fa5cad3235b0cab2b43db4.svg?v=16fa5cad3235)

图 2相同500点月牙与500点椭圆数据分别经过三种算法。颜色表示算法分组，灰色为DBSCAN噪声；ARI用生成标签评价分组一致性，噪声数同时显示。

500点月牙实验中，固定参数的DBSCAN恢复两条生成月牙，调整兰德指数ARI为1；k-means与两组分GMM分别约0.257和0.523。椭圆数据上，GMM约0.921、k-means约0.906，而DBSCAN将31点记为噪声。这些分数使用了合成数据保存的生成标签，ARI按点对是否同组比较，并校正随机一致性；组号交换不会影响结果。现实资料没有标签时，可以比较重采样后的分组一致性，并检查边界对象，而不是把一个内部指标自动解释成自然类别的证据。

![多种聚类算法在不同形状数据上的分组对照](https://ml-biomat.com/static/tutorials/machine-learning/figures/f9722ff1d6f26abfb41607ed.png?v=f9722ff1d6f2)

图 3scikit-learn开发者的原始算法—形状对照图，BSD-3-Clause许可，未改动。按行比较同一数据，按列比较同一算法；原图使用英文算法名称，时间标注属于原示例。

官方算法对照图把更多形状放在一起，适合先按行观察“同一批点被怎样分组”，再按列观察“同一规则偏爱什么形状”。图中额外算法提供方法全景，本节实际实验聚焦k-means、GMM和DBSCAN，并另用六个点完整展示层次合并。把原图当作提出问题的地图，再回到本节保留的输入和参数，就能区分算法结构的影响与某一次参数选择的影响。

轮廓系数也是常见的内部检查：比较一点到本组其他点的平均距离，与它到最近其他组的平均距离。若两者为2和5，差3除以较大距离5得到0.6，说明这个点在当前距离下更贴近本组。它偏好组内紧凑、组间分离的几何结构，因此弯曲月牙可能在视觉上连贯，却未获得很高轮廓系数。比较算法时，应把指标偏好的几何形状也纳入解释。重采样检查还要处理组号任意交换的问题，可以比较点对共组关系，而不直接比较数字编号。

## 高斯混合给出柔性的归属，也给出密度

两种人群在测量空间中重叠时，把边界附近的对象硬分到某一组会丢掉信息。高斯混合模型把总体描述成若干椭圆形概率分布的加权和：每个组分有中心、协方差和混合比例。中心描述典型位置，协方差描述伸展方向及尺度，比例描述从该组分抽取记录的机会。一个对象可以以不同概率关联各组分，这种“责任度”是观察到该对象后，对其潜在组分归属的条件概率。

$$
p(x)=\sum_{k=1}^K\pi_k\mathcal N(x\mid\mu_k,\Sigma_k),\qquad r_{ik}=\frac{\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)}{\sum_{h=1}^K\pi_h\mathcal N(x_i\mid\mu_h,\Sigma_h)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/27509148373c8c6129efab02.svg) | 组分数、两个组分索引、观测索引、任意d_f维向量与观测向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/324d4eda86e7dc8a4081a48b.svg) | 非负混合比例（和为1）、d_f维均值、d_f×d_f正定协方差；均值同输入单位，协方差含对应单位乘积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/42db73e94c2e691a2004355e.svg) | 高斯概率密度、混合密度与组分责任度；密度单位为特征体积的倒数，责任度为无量纲条件概率。 |

两个组分比例0.4与0.6，在某点的密度0.2与0.1，加权密度为0.08与0.06，总密度0.14；责任度分别4/7与3/7。若两密度同时缩小一千倍，总密度也缩小一千倍，责任度却不变。

责任度的分母把所有组分的加权密度相加，再把每一项归一化，因此各组分责任度之和为1。这里有两个容易混淆的量：总体密度描述这个位置是否常见，责任度描述在这些候选组分之间怎样分配归属。一个离所有组分都很远的点，仍可能以接近1的责任度归属于其中相对最近的一组；同时它的总体密度非常小。做异常检查时，应查看密度或单独设计的异常分数，而不能把最大责任度当作“这个观测很正常”的概率。

参数通过EM交替估计：在当前参数下计算各点责任度，再用这些软权重更新组分比例、均值和协方差。协方差约束影响模型能力：球形只保留一个尺度，对角形式忽略坐标相关，完整矩阵允许椭圆旋转。组分过多会追逐少数点，协方差也可能缩得极小；多次初始化与协方差正则化帮助计算，组分选择则需要独立评价。本例以375点拟合、125点检查，比较一到五个组分的BIC和留出平均对数密度。

![左：两组分高斯混合的密度等高图；中：375点训练BIC与125点测试平均对数密度；右：六点完全连接树状图，其纵轴为组间最远距离。](https://ml-biomat.com/static/tutorials/machine-learning/figures/eb1ec73fc18ed0163f6e93b9.svg?v=eb1ec73fc18e)

图 4左：两组分高斯混合的密度等高图；中：375点训练BIC与125点测试平均对数密度；右：六点完全连接树状图，其纵轴为组间最远距离。

BIC把训练对数似然与参数数量的惩罚结合，值越小越好；本例在两个组分处最小，与生成过程一致，留出平均对数密度也在附近达到较高水平。它选择的是给定高斯混合家族中的近似复杂度，一个形状复杂的真实人群可能需要几个高斯组分才能描述。右侧六点树状图的纵轴则是完全连接距离，最后两大组在距离2.4处合并。把两种图并排看，能区分概率密度模型与基于距离的合并记录，各自回答不同的问题。

## 二维地图要检查邻居，不能只看岛屿

卷起一张纸以后，纸上沿表面相邻的点仍然相邻，但隔着空气直线距离很近的两点可能位于不同层。流形学习借用这种直觉：高维观测可能由少数连续因素控制，局部邻居能提供关于低维结构的线索。照片中的视角、姿态和光照，便可能让同一对象沿着连续的变化路径移动。有限数据、噪声、缺测和不合适的距离都可能影响这条路径，所以降维前理解原始表示，往往比不断调整地图颜色更有价值。

van der Maaten与Hinton在2008年的t-SNE论文中处理了把高维邻域挤进二维的拥挤问题。方法把高维点间邻近关系转换为概率，再调整二维坐标，使二维的邻近概率与之协调；低维使用长尾分布，让许多非邻居有空间分开。perplexity控制邻域尺度的有效大小，不能直接当作最终每点恰有几个邻居。优化尤其重视高维近邻在地图上的安排，因此不同岛屿之间的空白距离、岛屿面积和朝向没有统一的原空间度量解释。

UMAP先依据局部距离尺度建立带权近邻图，再优化低维图的连接关系。n_neighbors改变构图时考虑的邻域范围，min_dist影响低维点能够聚得多紧。相同样本可以因此呈现松散云团或紧密岛屿，但原始对象并没有随之变成不同物种。UMAP提供对新样本的transform路径；本节采用的标准scikit-learn t-SNE主要对当前样本集联合嵌入。需要持续加入新对象的系统，应把新样本映射方式和地图稳定性纳入选择。

![相同900幅数字的四张无监督地图，颜色为拟合后加入的数字标签。T为十近邻trustworthiness，overlap为十近邻平均重合比例；坐标方向和尺度由各嵌入决定。数据：UCI，CC BY 4.0。](https://ml-biomat.com/static/tutorials/machine-learning/figures/40c589e6f87a1ee91be00779.svg?v=40c589e6f87a)

图 5相同900幅数字的四张无监督地图，颜色为拟合后加入的数字标签。T为十近邻trustworthiness，overlap为十近邻平均重合比例；坐标方向和尺度由各嵌入决定。数据：UCI，CC BY 4.0。

四张地图使用相同900幅图像：二维PCA、perplexity为10和50的t-SNE，以及15邻居的UMAP。原空间十近邻与二维十近邻的平均重合比例分别约0.182、0.616、0.628和0.555。另一指标trustworthiness考察二维引入的“假近邻”在原空间究竟排得多远，其值分别约0.825、0.988、0.989和0.987。高trustworthiness与十近邻完全重合不是同一要求：把原本第11近的点挪到第10近，和把一个极远点挪过来，应受到不同程度的惩罚。

$$
O_k=\frac1n\sum_{i=1}^n\frac{|N_i^{\rm original}\cap N_i^{\rm map}|}{k},\quad T_k=1-\frac{2}{nk(2n-3k-1)}\sum_{i=1}^n\sum_{j\in U_i}(r_i(j)-k)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0dc800785ec2d81e6ae9f15e.svg) | 点数、两个点索引与邻居数，排除点自身；trustworthiness使用k<n/2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a08c10878c94c7d88df99a60.svg) | 原空间和地图的k近邻集合，以及地图引入但原空间k近邻中没有的点集合。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d6f0c06dc4fba168d372c430.svg) | j在i原空间近邻中的名次（最近为1）、平均近邻重合比例与trustworthiness；均为无量纲。 |

某点两组十近邻有六个相同，该点重合比例0.6；对全部点平均得到O。若六个点各取一邻居，只有一个地图新邻居在原空间排第三，则惩罚和为3−1=2，归一化系数为1/24，T=11/12。名次更远的假近邻扣分更多。

这些结果支持一个具体判断：在本次像素距离、样本集合和参数下，非线性地图保留的局部邻域多于二维PCA。进一步检查可以选中一个点，回看原图及两种空间里的邻居，并改变随机种子、邻域尺度或样本子集。若分组结论只在某一个漂亮视角出现，就应回到原始特征检验相应差异。若目的是压缩后重建，前面的PCA误差仍是更直接的评价；地图好看、邻域可靠、重建准确分别对应不同目标。

## 异常分数最终要变成多少次检查

设备在正常运行时形成一片稳定的数据区域，之后一条新记录偏离这片区域，可以触发检查。这是新颖性检测：训练数据主要代表正常状态，评价对象是未来记录。离群值检测则允许当前资料中混有少量异常，试图从这批资料中识别偏离主体的点。二者对训练资料的假设不同。例如，新出现的一整团异常可能在自身内部很密集，若与正常资料一起做局部密度比较，结论会与只根据历史正常数据判断不同。

Isolation Forest通过随机选择特征和切分位置把点逐步隔离，容易被较少切分独立分出的对象获得更高异常程度。LOF比较一个对象及其近邻的局部可达密度，适合关注“比周围邻居稀疏多少”。本节把LOF设置为novelty模式，在400条正常记录上拟合；新的200条正常校准记录用于设定阈值，之后才评价200条正常与40条异常测试记录。分数统一取为越大越异常，但两种模型的数值尺度不同，各自在自己的校准分数上确定阈值。

![两模型均仅用400条正常记录拟合，再用200条正常记录设阈值。蓝点为200条正常测试记录，绿色叉为40条生成异常；黑线为阈值。右侧改变正常校准分位数，显示误报与检出的共同变化。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5413b7f378c95a5cdc565203.svg?v=5413b7f378c9)

图 6两模型均仅用400条正常记录拟合，再用200条正常记录设阈值。蓝点为200条正常测试记录，绿色叉为40条生成异常；黑线为阈值。右侧改变正常校准分位数，显示误报与检出的共同变化。

阈值取正常校准分数的第95百分位。实际测试中，Isolation Forest检出40条异常，同时误报13条正常记录；LOF同样检出40条异常、误报12条正常记录。若每次误报检查成本为1、漏掉异常的成本为20，两者本次成本为13和12。校准集上的5%尾部选择不意味着任何未来环境恰好误报5%，这里新的正常测试误报比例分别是6.5%和6%。图中改变阈值后，检查工作量和检出比例一起变化，实际使用者可以据此安排复核能力。

实验异常由中心在(3.3,−3.3)附近的另一高斯分布生成，与正常区域分得较开。若把异常移向正常云团、改变正常噪声或增加新的正常工况，检出和误报都会改变。需要记录的不只是一个“异常率”，还包括异常种类、正常状态覆盖范围和人工复核结果。罕见也可能意味着有价值的新现象：异常分数适合把记录送入检查队列，最终的错误、故障或发现，需要结合原始对象及后续验证确定。

## 从一张地图走回原始对象

完整代码保留了原始数组、训练与测试索引、四张嵌入坐标和各实验摘要。先看PCA重建图库：选一幅图，找出在低秩重建中消失的笔画，再核对它的误差。随后比较同一个对象的原空间近邻和投影近邻，观察地图有没有把视觉相似但像素位置不同的数字拆开。聚类实验则可以固定生成数据、改变半径或组数，检查哪些点最先改变归属。这样的阅读顺序让图像、数值和算法操作始终指向同一批对象。

### 完整实验：数字压缩、邻域地图、聚类与异常

需要NumPy、SciPy、Matplotlib、scikit-learn和umap-learn。运行python main.py --output results --language zh。数字随scikit-learn提供，无需额外下载；输出五组科学图、experiment_data.npz与summary.json。

```
"""Unsupervised structure: actual compression, neighborhoods, density and novelty."""
from pathlib import Path
import argparse,json,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.cluster.hierarchy import linkage,dendrogram
from sklearn.datasets import load_digits,make_moons
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans,DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE,trustworthiness
from sklearn.neighbors import NearestNeighbors,LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import adjusted_rand_score,confusion_matrix
from umap import UMAP

COL=['#237b94','#d87430','#609b6d','#a268a6','#c7a22b','#465db0','#b95159','#7f8e37','#6e8290','#d38aab']
def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'white','axes.titleweight':'bold','axes.unicode_minus':False})
 rng=np.random.default_rng(6)
 def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 d=load_digits();X=d.data/16;y=d.target;it,ie=train_test_split(np.arange(len(X)),test_size=.25,stratify=y,random_state=6)
 ranks=[2,5,10,20,40,64];errors=[];ratios=[];recons={}
 for k in ranks:
  p=PCA(n_components=k,svd_solver='full').fit(X[it]);rec=p.inverse_transform(p.transform(X[ie]));errors.append(float(np.mean((rec-X[ie])**2)));ratios.append(float(p.explained_variance_ratio_.sum()));recons[k]=rec
 # Every image is reconstructed from a training-only basis; common grayscale limits.
 fig=plt.figure(figsize=(14.2,9.2),layout='constrained')
 outer=fig.add_gridspec(1,2,width_ratios=[1.85,1],wspace=.17)
 gs=outer[0].subgridspec(6,6,hspace=.08,wspace=.06)
 curves=outer[1].subgridspec(2,1,hspace=.20)
 for row,k in enumerate([None,2,5,10,20,40]):
  for c in range(6):
   ax=fig.add_subplot(gs[row,c]);ax.imshow(X[ie[c]].reshape(8,8) if k is None else recons[k][c].reshape(8,8),cmap='gray',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
   if c==0:ax.set_ylabel(T('原图','Original') if k is None else f'k={k}',rotation=0,labelpad=27,va='center')
   if row==0:ax.set_title(str(y[ie[c]]))
 ax=fig.add_subplot(curves[0]);ax.plot(ranks,errors,'o-',color=COL[0]);ax.set(xlabel=T('保留分量数','Retained components'),ylabel=T('测试像素均方误差','Test pixel MSE'),title=T('450幅留出图像','450 held-out images'));ax.grid(alpha=.18)
 ax=fig.add_subplot(curves[1]);ax.plot(ranks,ratios,'s-',color=COL[1]);ax.set(xlabel=T('保留分量数','Retained components'),ylabel=T('训练累计方差比例','Training cumulative variance'),ylim=(0,1.05));ax.grid(alpha=.18);save(fig,'compression')
 # Labels are used for display after the unsupervised embeddings are fitted.
 subset=it[:900];A=X[subset];p2=PCA(2,svd_solver='full').fit_transform(A)
 embeddings={'PCA':p2,'t-SNE p=10':TSNE(perplexity=10,random_state=6,max_iter=800,init='pca',learning_rate='auto').fit_transform(A),'t-SNE p=50':TSNE(perplexity=50,random_state=6,max_iter=800,init='pca',learning_rate='auto').fit_transform(A),'UMAP n=15':UMAP(n_neighbors=15,min_dist=.15,random_state=6,n_jobs=1,n_epochs=300).fit_transform(A)}
 def neighbors(data):
  raw=NearestNeighbors(n_neighbors=11).fit(data).kneighbors(data,return_distance=False)
  return np.array([row[row!=i][:10] for i,row in enumerate(raw)])
 nbr=neighbors(A);quality={}
 fig,axs=plt.subplots(2,2,figsize=(12,10),layout='constrained')
 for ax,(name,Z) in zip(axs.flat,embeddings.items()):
  en=neighbors(Z);overlap=float(np.mean([len(set(a)&set(b))/10 for a,b in zip(nbr,en)]));tr=float(trustworthiness(A,Z,n_neighbors=10));quality[name]={'trustworthiness10':tr,'neighbor_overlap10':overlap}
  sc=ax.scatter(Z[:,0],Z[:,1],c=y[subset],s=10,cmap=ListedColormap(COL),vmin=-.5,vmax=9.5,alpha=.8);ax.set(title=f'{name} | T={tr:.3f}, overlap={overlap:.3f}',xlabel=T('嵌入坐标1（任意单位）','Embedding coordinate 1 (arbitrary units)'),ylabel=T('嵌入坐标2','Embedding coordinate 2'));ax.set_xticks([]);ax.set_yticks([])
 cb=fig.colorbar(sc,ax=axs,ticks=range(10),shrink=.75);cb.set_label(T('真实数字标签（拟合未使用）','Digit label (unused during fitting)'));save(fig,'neighborhoods')
 moon,ym=make_moons(500,noise=.07,random_state=6)
 e0=rng.multivariate_normal([-2,0],[[1.2,.7],[.7,.6]],250);e1=rng.multivariate_normal([2,0],[[.6,-.45],[-.45,1.2]],250);ell=np.vstack([e0,e1]);ye=np.repeat([0,1],250);cluster_scores={};fig,axs=plt.subplots(2,3,figsize=(13,8),layout='constrained')
 for row,(name,D,Y) in enumerate([('moons',moon,ym),('ellipses',ell,ye)]):
  for col,(n,model) in enumerate([('k-means',KMeans(2,n_init=20,random_state=6)),('GMM',GaussianMixture(2,n_init=5,random_state=6)),('DBSCAN',DBSCAN(eps=.19 if row==0 else .4,min_samples=8))]):
   labels=model.fit_predict(D);ari=float(adjusted_rand_score(Y,labels));noise=int((labels==-1).sum());cluster_scores[f'{name}/{n}']={'ari':ari,'noise':noise,'clusters':len(set(labels)-{-1})};ax=axs[row,col];colors=[('#acb5bc' if a==-1 else COL[a%len(COL)]) for a in labels];ax.scatter(*D.T,c=colors,s=13,alpha=.8);ax.set(title=f'{n} | ARI={ari:.3f}, noise={noise}',xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'));ax.set_aspect('equal',adjustable='datalim')
 save(fig,'cluster_shapes')
 gt,ge=train_test_split(np.arange(500),test_size=.25,random_state=6);gm=GaussianMixture(2,n_init=10,random_state=6).fit(ell[gt]);xx,yy=np.meshgrid(np.linspace(-6,6,180),np.linspace(-4,4,150));grid=np.c_[xx.ravel(),yy.ravel()];density=np.exp(gm.score_samples(grid)).reshape(xx.shape);bics=[];ll=[]
 for k in range(1,6):
  q=GaussianMixture(k,n_init=10,random_state=6).fit(ell[gt]);bics.append(float(q.bic(ell[gt])));ll.append(float(q.score(ell[ge])))
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');im=axs[0].contourf(xx,yy,density,levels=12,cmap='Blues');axs[0].scatter(*ell[gt].T,s=4,color='#293d4b',alpha=.35);fig.colorbar(im,ax=axs[0],label=T('概率密度','Probability density'));axs[0].set(title=T('GMM：密度不等于组分概率','GMM: density versus membership'),xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'))
 axs[1].plot(range(1,6),bics,'o-',color=COL[0]);axs[1].set(xlabel=T('组分数','Components'),ylabel='BIC',title=T('训练拟合与复杂度','Training fit and complexity'));ax2=axs[1].twinx();ax2.plot(range(1,6),ll,'s--',color=COL[1]);ax2.set_ylabel(T('测试平均对数密度','Test mean log density'),color=COL[1]);axs[1].set_xticks(range(1,6))
 small=np.array([[0,0],[.2,.1],[.5,0],[2,0],[2.1,.2],[2.4,0]]);Z=linkage(small,method='complete');dendrogram(Z,labels=list('ABCDEF'),ax=axs[2],color_threshold=1);axs[2].set(ylabel=T('完全连接距离','Complete-link distance'),title=T('六点的逐步合并','Six observations merge'));save(fig,'density_hierarchy')
 # Training and threshold selection see only normal observations.
 train=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],400);cal=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],200);normal=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],200)
 anomaly=rng.normal(loc=[3.3,-3.3],scale=.6,size=(40,2));test=np.vstack([normal,anomaly]);truth=np.r_[np.zeros(200,dtype=int),np.ones(40,dtype=int)];novel={};models=[('Isolation Forest',IsolationForest(n_estimators=150,random_state=6,n_jobs=1)),('LOF novelty',LocalOutlierFactor(n_neighbors=20,novelty=True))]
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained')
 for ax,(name,model) in zip(axs[:2],models):
  model.fit(train);cs=-model.score_samples(cal);score=-model.score_samples(test);threshold=float(np.quantile(cs,.95));pred=(score>threshold).astype(int);tn,fp,fn,tp=confusion_matrix(truth,pred).ravel();novel[name]={'threshold':threshold,'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'cost_fp1_fn20':int(fp+20*fn)};field=-model.score_samples(grid).reshape(xx.shape);im=ax.contourf(xx,yy,field,levels=16,cmap='YlOrRd');ax.contour(xx,yy,field,levels=[threshold],colors=['#263744'],linewidths=1.5);ax.scatter(*normal.T,s=8,c=COL[0],alpha=.7);ax.scatter(*anomaly.T,s=15,c=COL[2],marker='x');fig.colorbar(im,ax=ax,label=T('异常分数（越大越异常）','Anomaly score (higher is more unusual)'));ax.set(title=f'{name} | FP={fp}, FN={fn}',xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'))
  fr=[];rec=[]
  for quantile in np.linspace(.8,.995,40):
   p=score>np.quantile(cs,quantile);fr.append(float(p[:200].mean()));rec.append(float(p[200:].mean()))
  axs[2].plot(fr,rec,'o-',ms=3,label=name)
 axs[2].set(xlabel=T('正常测试样本误报比例','False-positive fraction on normal test data'),ylabel=T('异常测试样本检出比例','Detected fraction of anomalous test data'),ylim=(0,1.05),title=T('阈值改变检查工作量','Thresholds alter review workload'));axs[2].legend(fontsize=9);axs[2].grid(alpha=.2);save(fig,'novelty')
 summary={'digits_n':len(X),'train_n':len(it),'test_n':len(ie),'pixel_features':64,'map_n':len(subset),'pca_ranks':ranks,'pca_test_mse':errors,'pca_train_variance_fraction':ratios,'neighborhoods':quality,'clusters':cluster_scores,'gmm_bic':bics,'gmm_test_mean_log_density':ll,'gmm_best_bic_components':int(np.argmin(bics)+1),'gmm_responsibility_sum_max_error':float(abs(gm.predict_proba(ell[ge]).sum(1)-1).max()),'novelty_train_normal':len(train),'novelty_calibration_normal':len(cal),'novelty_test_normal':len(normal),'novelty_test_anomaly':len(anomaly),'novelty':novel,'hierarchy_final_complete_distance':float(Z[-1,2])}
 np.savez_compressed(out/'experiment_data.npz',digits=X,labels=y,train_indices=it,test_indices=ie,map_indices=subset,moons=moon,moon_labels=ym,ellipses=ell,ellipse_labels=ye,novelty_train=train,novelty_calibration=cal,novelty_test=test,novelty_truth=truth,**{f'map_{j}':v for j,v in enumerate(embeddings.values())});(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

开展新的无监督分析时，可以先写一段简短的数据说明：对象是什么，哪些坐标表达相似性，单位如何处理，结果用于浏览、压缩、分组还是报警。接着确定与目标相符的检查：重建误差对应压缩，邻域保留对应地图，重采样一致性与领域检查对应分组，误报和漏报成本对应报警。即使没有现成标签，也可以逐步补充小规模人工检查或后续观测，让探索结果变成能够继续验证的研究问题，而不必让一张二维图承担全部结论。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Pearson (1901), On Lines and Planes of Closest Fit](https://zenodo.org/records/1430636)

   从点到直线的距离理解降维历史。
2. [UCI — Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   手写数字数据及许可。

   CC BY 4.0
3. [scikit-learn — Decomposing signals in components](https://scikit-learn.org/stable/modules/decomposition.html)

   PCA、中心化、SVD与重建。

   BSD-3-Clause
4. [scikit-learn — Comparing clustering algorithms](https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html)

   算法形状对照原图与开放示例。

   BSD-3-Clause
5. [scikit-learn — Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html)

   责任度、协方差、EM和BIC。

   BSD-3-Clause
6. [van der Maaten & Hinton (2008), Visualizing Data using t-SNE](https://www.jmlr.org/papers/v9/vandermaaten08a.html)

   邻域概率与拥挤问题。
7. [UMAP — How UMAP Works](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html)

   局部尺度、近邻图和低维布局。

   BSD-3-Clause project
8. [UMAP — Basic Parameters](https://umap-learn.readthedocs.io/en/latest/parameters.html)

   邻居数与最小距离参数。

   BSD-3-Clause project
9. [scikit-learn — Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)

   LOF新颖性模式与异常检测目标。

   BSD-3-Clause
