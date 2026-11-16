# 看懂模型怎样判断：可解释性、归因与内部机制

Source: https://ml-biomat.com/tutorials/machine-learning/m25/
Language: zh-CN

从可读模型出发，逐步检查替换、背景、梯度与内部干预，让每种解释回答一个明确问题。

## 预测正确之后，还想知道什么

一台相机把手写数字认成3，我们可以继续问：它主要依赖右侧弧线，还是依赖背景里一块偶然的亮点？一个需求预测模型给出较高数值，我们也可能想知道，是某个输入把结果推高，还是模型把两个总是一起变化的特征混在了一起。可解释性围绕这些具体问题展开。它既可以帮助研究者理解模型，也可以发现数据处理错误、检查规则是否符合应用要求，并为后续测量和实验提供线索。

不同问题需要不同解释。总体解释总结模型在一群对象上的行为，局部解释说明某一个预测相对某个参照如何形成；输入归因分配输出差异，内部分析则检查神经元、表示和计算路径。一个重要性排名不能直接回答某位用户为何得到这个预测，一张局部热图也不能概括整套系统。本节先把解释对象、输出尺度、参照对象和预期用途说清，再选择计算方法，避免看到一幅漂亮图就把它当成所有问题的答案。

我们会实际训练两类模型：一类读取三个相关的表格特征，另一类识别8×8像素手写数字。表格实验能逐项检查替换、求平均与分配贡献；图像实验能查看梯度、路径积分、通道响应和遮挡后的输出。每幅图都对应明确计算，不把模型内的预测关系直接写成现实世界的干预效果。若要回答改变某项现实条件会怎样，还需接上因果设计与相应的数据。

## 先选择能直接读懂结构的模型

线性模型把每个特征乘以一个系数，再相加。固定其他输入时，某个特征增加一单位带来多少预测变化，可以直接由系数读出。这个说法同时要求明确特征单位、变换与相关关系：标准化后的“一单位”是一个标准差，取对数后的系数需要按对数尺度解释；两个几乎相同的输入则可能分担同一条预测信息。线性结构简单，解释仍需要把数据表示一起带上。

浅决策树可以沿一条路径复述预测，例如先判断某个输入是否超过阈值，再进入少量分支。树很深时，单条路径可能仍短，但整体规则已经难以一眼把握。广义可加模型GAM允许每个特征有自己的弯曲响应，再把这些响应相加，既能表达非线性，也保留逐项查看的结构。若两个特征联合产生额外作用，则要显式加入交互项，否则可加结构会遗漏这部分规律。

$$
\widehat y=\beta_0+\sum_{j=1}^p f_j(x_j)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/84b54b809e5e61516ae65a79.svg) | 预测结果与截距，均为结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b6f63c98dba7f777ad1c41c8.svg) | 特征索引、特征数、第j特征及其单变量响应函数；输入各有单位，函数值为结果单位。 |

线性模型令fj=βjxj，可加样条则用弯曲函数。截距1、f1(2)=4、f2(3)=9，预测14。只有求和时没有跨特征乘积；交互需要另加函数。

合成实验让第一特征产生线性作用、第二特征产生平方作用，并加入二者乘积；第三特征几乎复制第一特征，二者相关系数约0.996。600条记录训练、200条测试时，线性模型RMSE约0.947，浅树0.731，可加样条模型0.678，随机森林0.271。另一个带第一特征单调约束的提升树得到0.211。这里生成机制在固定其他输入时确实随第一特征增加，约束与问题结构一致；换一种机制，应重新判断这条约束是否合理。

![左：相关特征分布与一条离开常见组合的替换路径；中：12次置换的MSE增加均值±标准差；右：相同600/200划分下的五种模型RMSE。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d175d75b1e18842babf8591c.svg?v=d175d75b1e18)

图 1左：相关特征分布与一条离开常见组合的替换路径；中：12次置换的MSE增加均值±标准差；右：相同600/200划分下的五种模型RMSE。

单调约束规定方向，稀疏约束减少使用的变量，形状约束可以表达凸性或饱和等要求。它们把领域知识写进模型可取的函数集合，通常比事后给复杂模型配一段解释更直接。不过可读结构与预测误差仍要同时检查：少一条必要交互，解释可能很清楚，预测却偏离真实关系。模型选择因此需要围绕任务，在足够表达能力与可检查结构之间做具体比较。

## 打乱一列，与沿着一列移动

置换重要性先记录测试误差，再打乱某一列，把它与结果及其他特征的对应关系拆开，观察误差增加多少。它衡量的是已拟合模型对这列信息的依赖，并不重新训练模型。代码每项重复12次置换，显示均值与标准差。第一特征单独置换使MSE平均增加约3.760，相关副本约0.492；把两者用同一行置换一起打乱，增加约6.693。分开破坏与一起破坏的信息不同，贡献也不要求简单相加。

$$
I_j=\frac1n\sum_{i=1}^n\left[\ell(y_i,f(x_{i,-j},x_{\pi(i),j}))-\ell(y_i,f(x_i))\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3dc5dc5364d523cf7d193d6a.svg) | 对象索引、特征索引、测试对象数与随机行排列。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b17901c71506b5271de88ca7.svg) | 原输入、除第j列的其余输入、被重排的第j列、观测结果与固定预测模型。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f5298f54aa4c0df5bf3005a6.svg) | 损失与置换后平均损失增加；MSE时单位为结果单位平方。 |

如果原MSE为0.2，置换后为0.7，重要性为0.5。模型不重新拟合；联合置换使用同一行排列保留组内关系。图示12次排列的均值与标准差。

PDP选择一组特征取值，把所有对象的这一列依次替换成每个值，再平均预测；ICE保留每个对象各自的曲线。平均曲线可以平滑地概括趋势，个体曲线则显示不同背景下响应是否相同。本例第二特征会改变第一特征的作用斜率，所以多条ICE并不重合。看见曲线分叉时，可以继续检查交互，而不是仅用一条总体曲线描述每个人。

$$
\operatorname{ICE}_i(z)=f(z,x_{i,-j}),\qquad\operatorname{PDP}_j(z)=\frac1n\sum_{i=1}^n\operatorname{ICE}_i(z)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/800926673aeb9732053f2892.svg) | 对象索引、目标特征、对象数、目标特征的替换值与其余固定特征。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c6cd6629068802ef2c19ba9d.svg) | 模型、对象响应曲线与平均响应曲线；输出均为预测结果单位。 |

先替换再预测。三人的某网格点预测为2、4、9，PDP为5，而ICE保留这三个差别。强相关输入的替换可能远离常见组合。

![左：30条ICE和200测试对象的PDP；右：按各自标明方法居中的PDP与十区间ALE。纵轴是模型预测及其居中变化，不是现实干预效应。](https://ml-biomat.com/static/tutorials/machine-learning/figures/407181b9508e5d3a42e3faa0.svg?v=407181b9508e)

图 2左：30条ICE和200测试对象的PDP；右：按各自标明方法居中的PDP与十区间ALE。纵轴是模型预测及其居中变化，不是现实干预效应。

强相关特征给替换操作带来一个具体问题。训练数据中第一、第三特征几乎相等，PDP却会把第一特征改成很大，同时保留第三特征很小，生成少见组合。ALE把第一特征划成局部区间，只对本来落在某区间的对象计算上下端点差，再逐段累加并居中，减少远离实际联合分布的替换。代码使用十个分位区间。它仍然总结模型的局部变化，区间太稀疏、分箱太粗或存在复杂交互时，也应结合样本分布阅读。

## 用附近的简单模型解释一个预测

2016年的LIME研究把局部解释组织成一个容易操作的过程：围绕待解释对象产生邻近样本，向原模型查询结果，再让一个简单模型重点拟合附近行为。可以把它想成在弯曲地面上铺一小块平板；范围很小时，平板能描述局部坡度，范围扩大后，远处的起伏也会影响它的位置。邻域如何定义、哪些扰动可行、距离权重和简单模型复杂度，都会影响最终解释。

$$
\widehat g=\arg\min_{g(z)=\beta_0+\beta^\mathsf Tz}\sum_{i=1}^m w_i[f(z_i)-g(z_i)]^2+\lambda\|\beta\|_2^2,\quad w_i=\exp\!\left(-\frac{\|z_i-x\|_2^2}{2h^2}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0755ee100528064ed2d0b6e8.svg) | 目标三维输入、邻近扰动、扰动数与邻域宽度；本例输入均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b26922014466083f7794284.svg) | 原预测模型、局部线性模型、截距与三维斜率；输出为结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c34d4f71d9fb2cd0d844aa97.svg) | 距离权重、非负惩罚系数、欧氏范数与最小化参数。 |

距离为零权重1，距离等于h时权重e^-1/2≈0.607。600个扰动用h=0.2或0.8，λ=0.01；比较拟合误差与五个种子的系数差异。

本例对一个随机森林预测进行实际加权线性拟合，每次取600个独立高斯扰动，比较0.2与0.8两种邻域宽度，各重复五个种子。原模型在该点预测约−1.664；窄邻域的局部模型在该点预测约−1.54到−1.55，宽邻域约−0.97到−1.00。窄邻域的加权拟合优度约0.836到0.863，宽邻域约0.798到0.807。解释旁边给出这些数，可以看到近似究竟拟合得多好，而不只看系数的正负。

本例的独立扰动也会打破第一、第三特征的相关关系，因此它明确回答的是该扰动邻域下的局部响应。对于只能取合法组合的数据，可以在可行集合内抽样、使用条件生成模型或直接解释有实际意义的特征组。局部斜率是附近变化率，贡献值则需要额外说明从哪里变化到哪里；把一个系数直接写成“这项造成了多少结果”，会跳过这段参照关系。

## 把预测差额分给特征，先说清参照

Shapley值来自合作分配问题：几位成员一起产生一笔收益，如何分配各自贡献？放到模型解释中，把特征看成成员，逐步加入特征时带来的预测变化看成边际收益，再对所有加入顺序求平均。交互项因而可以由参与者共同分担。计算开始前，要定义一个特征缺席时如何填补，以及“空集合”对应的参考预测；不同定义会形成不同的分配问题。

$$
\phi_j=\sum_{S\subseteq F\setminus\{j\}}\frac{|S|!(p-|S|-1)!}{p!}[v(S\cup\{j\})-v(S)],\qquad v(\varnothing)+\sum_{j=1}^{p}\phi_j=f(x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c2050a20f8e050868e23ea7a.svg) | 全体特征集合、特征数、目标特征、先加入的特征子集、集合大小与阶乘。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81e802bf30a81f3d8c26bb91.svg) | 固定集合S特征并按所选背景补齐后的平均输出、空集合参考与目标预测，结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b14779b70d4b2a8a3695f4f.svg) | 第j特征的分配贡献、并集、去掉元素与子集关系；贡献同输出单位。 |

权重对应全部加入顺序中某集合先出现的比例。f=x1+2x2+x1x2，从(0,0)到(2,3)，x1先/后贡献2/8，平均5；x2先/后6/12，平均9，总和14。

## 两种加入顺序，怎样分配同一项交互

公开模型f(x)=x₁+2x₂+x₁x₂。x为目标，b为参照。两条折线分别先加入x₁或x₂；Shapley贡献平均两种顺序的增量。

[Figure: 两种加入顺序与特征贡献](https://ml-biomat.com/tutorials/machine-learning/m25/#M25-plot)

交互使用一个完全公开的二特征函数。输入为(2,3)、参照为(0,0)时，预测为14，两个Shapley贡献为5和9；乘积项6被两种加入顺序平均分配。把参照换成(1,1)，参考预测变成4，同一输出14的差额变成10，两项贡献为3和7。对象和模型都没有改变，解释改变的是比较起点。这也说明，贡献较大不等于这个特征在所有人群中都更重要。

![左：80背景样本、三特征全部集合的Shapley逐步求和；中：30个测试对象的贡献与特征值；右：两个邻域宽度、五种子局部斜率均值±标准差。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d19cdc16ffb3702fbe2f86a1.svg?v=d19cdc16ffb3)

图 3左：80背景样本、三特征全部集合的Shapley逐步求和；中：30个测试对象的贡献与特征值；右：两个邻域宽度、五种子局部斜率均值±标准差。

随机森林实验枚举三个特征的全部八个集合，用80个训练背景样本补齐缺席特征，得到精确的边际背景Shapley值。某测试对象的参考预测约0.380，三项贡献约−1.368、−0.287、−0.389，相加得到−1.664。若背景改成第一特征为正的训练对象，参考升至约2.118，贡献也随之改变。这里的精确是对所选模型、有限背景与集合定义而言；背景保留未替换列之间的关系，替换列与其余列之间的相关则被拆开。

![SHAP蜂群图中每行一个特征，点的左右与颜色表示贡献和取值。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0fcd149c9226bcf9c4a73868.png?v=0fcd149c9226)

图 4SHAP官方Adult/XGBoost蜂群原图，横轴为默认原始log-odds贡献，颜色为特征值。Scott Lundberg及SHAP贡献者，MIT许可，未改编。

SHAP项目原始蜂群图展示一种紧凑读法：每行一个特征，每个点一个对象，横向位置是贡献，颜色是原始特征值，点的堆叠反映分布。所选Adult/XGBoost示例默认解释原始边际分数，即二分类log-odds，横轴不是概率百分点。我们的三特征实验解释回归结果单位，两个图的尺度不同。相关特征若改用条件背景，信息分配还会改变，模型未直接读取的一列也可能因携带相关信息得到条件归因。

## 热图里，亮的是敏感度还是贡献

图像归因先选定一个标量输出。这里解释“数字3”的分类logit，随后问每个像素对这个数有什么作用。Saliency计算输出对像素的梯度，表示当前位置的微小改变会带来多大变化；取绝对值后只保留敏感程度，方向信息已经去掉。梯度很小也可能是模型在该位置已经饱和，因此局部斜率与从一幅参照图走到当前图的累计变化，是两个不同问题。

$$
S_j(x)=\frac{\partial f_c(x)}{\partial x_j}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/116d3ff8ca8fc9844612c124.svg) | 64维归一化像素输入、像素索引与目标类别索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff7ec1afdc831fd8806819cc.svg) | 目标类别logit、局部梯度与偏导；梯度为logit/归一化强度单位。 |

梯度2表示足够小的像素增量0.01带来约0.02的logit变化，其他输入固定。显示|S|时正负方向被合并，图中明确标记绝对值。

Integrated Gradients在参照图与当前图之间走一条路径，沿途累计梯度，再乘以各像素的总变化。2017年的相关研究把敏感性、实现不变性等性质纳入方法设计。完整性提供一个可检查的求和关系：各像素贡献相加，应接近两端输出之差。参照可以是全黑图、均值图或其他有任务含义的对象，选择它也在定义比较问题；路径穿过的中间图像是否合理，同样值得查看。

$$
\operatorname{IG}_j(x;b)=(x_j-b_j)\int_0^1\frac{\partial f_c(b+\alpha(x-b))}{\partial x_j}\,d\alpha,\qquad\sum_j\operatorname{IG}_j=f_c(x)-f_c(b)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/228d8035641ba5e338c3a919.svg) | 64维目标与基线图像、像素索引与目标类别；像素强度归一化到0–1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d8e619ffa58db67bebadc631.svg) | 0到1路径位置、目标logit、像素贡献、偏导与路径积分；贡献为logit单位。 |

链式法则沿路径积分给出端点输出差。f=2x1+3x2，从零到(1,2)，贡献为2与6，和8。CNN用128点中点积分，求和偏差反映数值积分误差。

![同一个真实数字3的输入、绝对梯度、黑色基线IG、均值基线IG与第二卷积层取正部前/后的Grad-CAM。解释目标为类别3的logit；两幅IG共用色标范围，Grad-CAM缩放到0–1。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2884696d0c6133169712d5f5.svg?v=2884696d0c61)

图 5同一个真实数字3的输入、绝对梯度、黑色基线IG、均值基线IG与第二卷积层取正部前/后的Grad-CAM。解释目标为类别3的logit；两幅IG共用色标范围，Grad-CAM缩放到0–1。

代码用1257张数字图训练小型卷积网络，在540张留出图上准确率约0.963。选择的数字3，其目标logit约7.050，全黑参照约−2.817，两端差约9.868；128点中点积分得到贡献和约9.870，数值误差约0.0023。换成训练均值图作为参照，贡献分布随之改变。两幅IG图采用相同颜色范围，红色与蓝色保留贡献方向；Saliency与Grad-CAM使用各自标注的尺度，不能只按亮度横向比较。

Grad-CAM把目标输出对卷积特征图的梯度在空间上平均，作为通道权重，再组合特征图并保留正向部分。它提供所选层上的区域定位，空间精细程度受该层分辨率影响；把小特征图插值到原图尺寸，并不会增加新的定位信息。本例第二卷积层仍是8×8，所以可以直接展示。它与输入梯度、路径贡献分别回答不同尺度的问题，图注需要写清目标类别、层、归一化与颜色含义。

$$
a_k^c=\frac1{HW}\sum_{u=1}^H\sum_{v=1}^W\frac{\partial f_c}{\partial A_{uv}^{k}},\qquad L^c=\operatorname{ReLU}\left(\sum_k a_k^c A^k\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bbf4a4beafe43aaa65bd08ff.svg) | 通道与两个空间索引，以及特征图高和宽；本例12通道、H=W=8。 |
| ![Formula](https://ml-biomat.com/static/agent-math/796902c1169abecbf44f6ae3.svg) | 第k通道特征图、其位置值与目标类别logit。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a2e2166451f4791f36f639a.svg) | 平均梯度通道权重、目标定位图、取正部与偏导。原始加权图为logit尺度，再按最大值归一化显示。 |

两通道在某位置值3和2、平均梯度0.5和−0.2时，正部为max(0,1.5−0.4)=1.1。空间平均产生通道权重，不提供独立像素贡献求和性质。

本次图中，标准Grad-CAM恰好全部为零，所以同时展示取正部之前的有符号结果。这个网络在卷积后把所有位置展开，再用位置各异的全连接权重分类；Grad-CAM的空间平均将这些权重合并，得到的加权图在当前输入上全为负，取正部后便归零。与此同时，完整模型仍能给类别3较高logit。读这组图可以准确定位信息消失的计算步骤，也能看出区域定位图与原模型完整决策之间的区别。

## 从像素走向概念，再观察内部表示

像素归因很细，但人常想问“竖直笔画是否重要”这类问题。2018年的TCAV研究用概念样本与对照样本在内部表示中训练一个分隔方向，再计算目标输出沿这个方向的导数。概念不由一个词自动确定，而由实际提供的样本集合定义。选择哪一层、怎样准备对照、概念与其他属性是否混杂，都影响方向所代表的内容；重复背景抽样与统计比较是完整研究设计的一部分。

$$
D_{C,c}(x)=\nabla_a f_c(a(x))^\mathsf T v_C,\qquad T_{C,c}=\frac1{|X_c|}\sum_{x\in X_c}\mathbf1\{D_{C,c}(x)>0\}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1a03a158faf24bccc3e775cf.svg) | 所选层展开激活、本例512维单位概念方向与对激活的梯度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b1800e2eb9f630f21ac87ec4.svg) | 概念对比、目标类别、该类别评价样本集合及样本数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7cf069fe502feb6e16e478e5.svg) | 方向导数、正导数比例与指示函数；比例无量纲，导数依激活坐标尺度。 |

若四个导数为0.2、−0.1、0.4、0.3，比例为3/4。方向由概念与对照样本训练，单次方向的比例不是统计显著性检验；完整TCAV研究可重复对照拟合。

![上排为真实生成的概念探针输入，三幅竖线与三幅横线；下排为第一层通道2平均激活最大的六幅训练数字，标签与激活同时列出。](https://ml-biomat.com/static/tutorials/machine-learning/figures/33c1cbb628059de0e2de01df.svg?v=33c1cbb62805)

图 6上排为真实生成的概念探针输入，三幅竖线与三幅横线；下排为第一层通道2平均激活最大的六幅训练数字，标签与激活同时列出。

本例构造60幅带噪竖线和60幅带噪横线，在第一卷积层表示上训练线性概念探针，保留30幅检查，探针准确率为1。随后查看真实测试数字：类别1、3、7沿“竖线相对横线”方向的正导数比例分别为1、1、0。这组结果描述受控样本集定义的方向，以及模型沿该方向的敏感性。若继续研究自然笔画概念，应补充不同书写风格、对照概念、重复拟合与跨样本评价，检查方向是否稳定。

![四种不同球类组合的优化刺激图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6bfaf9eb5121d82f51f687e7.png?v=6bfaf9eb5121)

图 7Distill原图：多样性优化展示GoogLeNet mixed5a通道9对多种球类外观的响应。Chris Olah、Alexander Mordvintsev、Ludwig Schubert，Feature Visualization，2017，CC BY 4.0，未改编。

特征可视化的结果也可能很朴素。这里通道2的优化刺激几乎是一幅全亮图，其高激活训练样本则包含较密的笔画。与其强行为它起一个复杂语义名字，不如直接检查它对亮度、边缘、位置等变化的响应。优化目标、像素范围和正则化共同决定能找到什么刺激；增加平滑惩罚会减少细碎纹理，加入多样性项则可以寻找不同但同样高响应的输入。每次改变目标后，都可以再用真实样本检查提出的解释。实际训练图中，平均亮度与通道2平均激活的相关系数约0.986，这支持进一步检查亮度响应：保留笔画几何，只改变亮度，再记录通道变化。

特征可视化换了提问方式：固定网络，修改输入，让某个通道尽可能活跃。Distill的2017年示例展示，同一通道可能被多种外观激活，加入多样性目标能看到单张优化图遗漏的侧面。本节也真正优化了一个8×8输入，最大化第一层通道2的平均激活，同时限制像素范围，并加入幅值与相邻像素差的惩罚。生成图是模型刺激，不是拍摄到的真实数字；旁边的高激活训练样本提供另一种观察该通道的方法。

## 让解释经受一次真正的改变

机制可解释性继续追问信息怎样沿内部计算路径流动。一个神经元与某概念相关，可以提示研究方向；把它置零、替换成另一输入的激活或修补一段表示，再观察后续输出，能够直接测试它在该模型计算中的作用。多义神经元可能同时响应几类结构，某个概念也可能分散在许多单元中，因此分析单位可以是通道、方向、特征组或相互连接的小回路。确定这些单位，需要结合响应与干预结果。

![左：同一图像按归因或随机顺序归零后的目标logit；中：优化出的通道2刺激；右：单个竖线—横线概念方向在各真实测试类别中的正导数比例。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5f1908f09ac5ef3ed23ca416.svg?v=5f1908f09ac5)

图 8左：同一图像按归因或随机顺序归零后的目标logit；中：优化出的通道2刺激；右：单个竖线—横线概念方向在各真实测试类别中的正导数比例。

代码把训练网络第一层的通道2置零，测试准确率从约0.963降到0.954。对全部测试图而言，类别3的logit平均反而升高约0.902，说明这个通道对不同输出的作用方向并不相同。另一个检查按IG绝对贡献顺序把当前数字图的像素归零，与固定随机顺序比较：前四个高归因像素移除后，目标logit从7.050降到约0.408，随机顺序前四像素在此图上没有改变输出。归零后的图逐渐偏离自然数字分布，所以这里评价的是明确的黑色替换操作。

反事实解释寻找能让模型达到指定输出的可行输入变化。一个简单评分为第一特征加第二特征的两倍，当前输入(1,1)得3；若第一特征不可改变，达到阈值5需要把第二特征至少提高到2。代码保留这一不可变条件并核对结果。实际应用还应约束类别合法性、变化成本、时间顺序及特征间关系，再判断变化能否实施。模型输出跨过阈值，与现实采取行动后的结果，仍由不同证据支持。

$$
x^*=\arg\min_{x^\prime\in\mathcal F}d(x^\prime,x)\quad\text{subject to}\quad f(x^\prime)\ge t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/05020bbd252fb20e2fd1e79c.svg) | 原输入、候选修改与选出的修改，输入各有实际单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f70e518ff66c4f1b7d5b06.svg) | 满足不可变与合法性条件的集合、变化成本、固定预测模型、目标阈值与最小化选择。 |

f=x1+2x2，原点(1,1)，固定x1=1且只能增加x2，阈值5；按第二坐标变化量最小化，最小修改(1,2)，分数5。

解释评价要回到用途。忠实性检查解释所强调的部分是否确实影响模型；稳定性比较相似输入、背景样本和随机种子下的解释；完整性检查贡献求和；可理解性则需要面向使用者检验。2018年的显著图合理性检查研究强调，视觉相似的边缘图可能来自不同机制，可以通过随机化模型参数或标签训练来检验解释是否响应模型变化。本节的邻域重复、背景替换、积分误差和遮挡实验分别检查其中具体一项。

比较解释时还应固定模型版本与输出坐标。一个方法解释概率，另一个解释logit，贡献大小本来就不在同一尺度；一个使用全体训练背景，另一个只比较高需求对象，回答的参考问题也不同。评价表可以并列记录目标类别、参照样本、扰动方式、随机种子与实际误差，再比较解释是否帮助完成既定任务。这样，方法之间的差异就能追溯到明确选择，而不被简化为哪张图颜色更集中。

### 完整实验：表格解释、CNN归因、概念与通道干预

运行python main.py --output results --language zh。表格与概念图为明确生成数据；手写数字取自scikit-learn内置UCI Optical Digits数据。输出六组原创图、训练CNN权重、原始数组与指标；核心解释计算均直接展示。

```
"""Explain actual fitted models through complementary, inspectable calculations."""
from pathlib import Path
import argparse,json,itertools,math
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression,Ridge,LogisticRegression
from sklearn.preprocessing import SplineTransformer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def exact_shap(model,x,background):
 p=len(x);values={}
 for mask in range(1<<p):
  X=background.copy()
  for j in range(p):
   if mask&(1<<j):X[:,j]=x[j]
  values[mask]=float(model.predict(X).mean())
 phi=np.zeros(p)
 for j in range(p):
  for mask in range(1<<p):
   if mask&(1<<j):continue
   k=mask.bit_count();weight=math.factorial(k)*math.factorial(p-k-1)/math.factorial(p);phi[j]+=weight*(values[mask|(1<<j)]-values[mask])
 return phi,values[0],values[(1<<p)-1]
class CNN(nn.Module):
 def __init__(self):super().__init__();self.c1=nn.Conv2d(1,8,3,padding=1);self.c2=nn.Conv2d(8,12,3,padding=1);self.fc=nn.Linear(12*64,10)
 def from_first(self,a):b=F.relu(self.c2(a));return self.fc(b.flatten(1)),b
 def forward(self,x):a=F.relu(self.c1(x));o,b=self.from_first(a);return o,a,b
def ig(model,x,base,target,steps=128):
 # Midpoint quadrature, explicitly retaining the chosen baseline and target logit.
 alphas=(torch.arange(steps,dtype=x.dtype)+.5)/steps;path=(base+alphas[:,None,None,None]*(x-base)).requires_grad_(True);logit=model(path)[0][:,target];g=torch.autograd.grad(logit.sum(),path)[0];return (x-base)*g.mean(0,keepdim=True)
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);z=language=='zh';L=lambda a,b:a if z else b;rng=np.random.default_rng(25);torch.manual_seed(25);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if z else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 X=rng.uniform(-1.5,1.5,(800,3));X[:,2]=X[:,0]+rng.normal(0,.08,800);y=2*X[:,0]+X[:,1]**2+.8*X[:,0]*X[:,1]+rng.normal(0,.15,800);tr,te=train_test_split(np.arange(800),test_size=.25,random_state=25);xt,yt=X[tr],y[tr];xe,ye=X[te],y[te]
 models={'Linear':LinearRegression(),'Tree':DecisionTreeRegressor(max_depth=3,random_state=25),'GAM':make_pipeline(SplineTransformer(n_knots=6,degree=3),Ridge(alpha=1)),'Monotonic':HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=9,monotonic_cst=[1,0,0],random_state=25),'Forest':RandomForestRegressor(n_estimators=120,max_depth=7,min_samples_leaf=4,n_jobs=1,random_state=25)}
 rmse={}
 for k,m in models.items():m.fit(xt,yt);rmse[k]=float(np.sqrt(np.mean((m.predict(xe)-ye)**2)))
 rf=models['Forest'];base_mse=np.mean((rf.predict(xe)-ye)**2);perm=[]
 for cols in [[0],[1],[2],[0,2]]:
  reps=[]
  for _ in range(12):xx=xe.copy();order=rng.permutation(len(xx));xx[:,cols]=xx[order][:,cols];reps.append(float(np.mean((rf.predict(xx)-ye)**2)-base_mse))
  perm.append({'features':cols,'mean':float(np.mean(reps)),'std':float(np.std(reps,ddof=1))})
 grid=np.linspace(-1.4,1.4,60);ice=[]
 for row in xe[:30]:xx=np.tile(row,(60,1));xx[:,0]=grid;ice.append(rf.predict(xx))
 pdp=np.array([rf.predict(np.c_[np.full(len(xe),v),xe[:,1:]]).mean() for v in grid]);edges=np.quantile(xt[:,0],np.linspace(0,1,11));delta=[];counts=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  sel=(xt[:,0]>=lo)&(xt[:,0]<(hi if hi<edges[-1] else hi+1e-9));low=xt[sel].copy();high=low.copy();low[:,0]=lo;high[:,0]=hi;delta.append(float(np.mean(rf.predict(high)-rf.predict(low))));counts.append(int(sel.sum()))
 ale=np.cumsum(delta)-np.array(delta)/2;ale-=np.average(ale,weights=counts)
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].scatter(xt[:,0],xt[:,2],s=7,alpha=.25,color='#247b94');axs[0].plot([-1.3,1.3],[1,1],'o--',color='#d97b36');axs[0].set(xlabel='x0',ylabel='x2',title=L('相关特征与人工替换','Correlated features and replacement'));axs[1].barh(['x0','x1','x2','x0+x2'],[v['mean'] for v in perm],xerr=[v['std'] for v in perm],color='#247b94');axs[1].set(xlabel=L('置换后的MSE增加','MSE increase after permutation'),title=L('12次置换的均值与标准差','Mean and SD over 12 permutations'));axs[2].barh(list(rmse),list(rmse.values()),color='#d97b36');axs[2].set(xlabel='RMSE',title=L('同一200点测试集','Same 200-record test set'));save(fig,'global_models')
 fig,axs=plt.subplots(1,2,figsize=(11,4.7),layout='constrained');axs[0].plot(grid,np.array(ice).T,color='#9abac5',alpha=.45,linewidth=.7);axs[0].plot(grid,pdp,color='#d97b36',lw=3,label='PDP');axs[0].set(xlabel='x0',ylabel=L('预测结果','Predicted outcome'),title=L('30条ICE与200点PDP','30 ICE curves and 200-record PDP'));axs[0].legend();axs[1].plot(grid,pdp-pdp.mean(),label=L('PDP减去网格均值','PDP minus grid mean'));axs[1].plot((edges[1:]+edges[:-1])/2,ale,'o-',label=L('ALE按样本数居中','ALE centered by bin counts'));axs[1].set(xlabel='x0',ylabel=L('居中后的模型效应','Centered model effect'),title=L('替换全体，或只做局部差分','Global replacement or local differences'));axs[1].legend(fontsize=8);save(fig,'dependence')
 bg=xt[:80];shaps=np.array([exact_shap(rf,row,bg)[0] for row in xe[:30]]);x=xe[0];phi,base,pred=exact_shap(rf,x,bg);altphi,altbase,_=exact_shap(rf,x,xt[xt[:,0]>0][:80]);lime=[]
 for width in [.2,.8]:
  for seed in range(5):
   rg=np.random.default_rng(seed);near=x+rg.normal(size=(600,3))*width;dist=np.sum(((near-x)/width)**2,axis=1);weights=np.exp(-dist/2);lm=Ridge(alpha=.01).fit(near,rf.predict(near),sample_weight=weights);approx=lm.predict(near);target=rf.predict(near);r2=1-np.sum(weights*(target-approx)**2)/np.sum(weights*(target-np.average(target,weights=weights))**2);lime.append({'width':width,'seed':seed,'coefficients':lm.coef_.tolist(),'point_prediction':float(lm.predict(x[None])[0]),'weighted_r2':float(r2)})
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');vals=[base,*phi];bottom=0
 for i,v in enumerate(vals):axs[0].bar(i,v,bottom=bottom,color='#247b94' if v>=0 else '#d97b36');bottom+=v
 axs[0].axhline(pred,color='#20394a',ls='--');axs[0].set(xticks=range(4),xticklabels=['Base','x0','x1','x2'],ylabel=L('模型结果单位','Model outcome units'),title=L('精确三特征Shapley求和','Exact three-feature Shapley sum'))
 for j in range(3):axs[1].scatter(shaps[:,j],j+rng.uniform(-.14,.14,30),c=xe[:30,j],cmap='coolwarm',vmin=-1.5,vmax=1.5,s=24)
 axs[1].axvline(0,color='#b6c5cc');axs[1].set(yticks=range(3),yticklabels=['x0','x1','x2'],xlabel=L('Shapley贡献','Shapley contribution'),title=L('30个测试对象；颜色为特征值','30 test records; color is feature value'));fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-1.5,1.5),cmap='coolwarm'),ax=axs[1],label=L('特征值','Feature value'),shrink=.65)
 for w,c in [(.2,'#247b94'),(.8,'#d97b36')]:cs=np.array([a['coefficients'] for a in lime if a['width']==w]);axs[2].errorbar(range(3),cs.mean(0),yerr=cs.std(0,ddof=1),fmt='o-',color=c,label=f'width={w}')
 axs[2].set(xticks=range(3),xticklabels=['x0','x1','x2'],ylabel=L('局部线性斜率','Local linear slope'),title=L('5个邻域种子的均值与标准差','Mean and SD over 5 neighborhood seeds'));axs[2].legend();save(fig,'local_attribution')
 digits=load_digits();images=digits.images[:,None]/16;labels=digits.target;it,ie=train_test_split(np.arange(len(labels)),test_size=.3,stratify=labels,random_state=25);trainx=torch.tensor(images[it],dtype=torch.float32);trainy=torch.tensor(labels[it]);testx=torch.tensor(images[ie],dtype=torch.float32);model=CNN();optimizer=torch.optim.Adam(model.parameters(),lr=.003);trace=[]
 for epoch in range(35):
  order=torch.randperm(len(it));total=0
  for idx in order.split(128):logits=model(trainx[idx])[0];loss=F.cross_entropy(logits,trainy[idx]);optimizer.zero_grad();loss.backward();optimizer.step();total+=float(loss.detach())*len(idx)
  trace.append(total/len(it))
 model.eval();predicted=model(testx)[0].argmax(1).detach().numpy();acc=float(np.mean(predicted==labels[ie]));selected=int(np.flatnonzero((labels[ie]==3)&(predicted==3))[0]);image=testx[selected:selected+1].clone();target=3;xin=image.clone().requires_grad_(True);logits,a,b=model(xin);grad=torch.autograd.grad(logits[0,target],xin,retain_graph=True)[0];bggrad=torch.autograd.grad(logits[0,target],b)[0];cam_signed=(bggrad.mean((2,3),keepdim=True)*b).sum(1).detach().numpy()[0];cam=np.maximum(cam_signed,0);cam/=max(cam.max(),1e-12);zero=torch.zeros_like(image);meanbase=trainx.mean(0,keepdim=True);attr=ig(model,image,zero,target);attrmean=ig(model,image,meanbase,target);logit=float(model(image)[0][0,target].detach());base_logit=float(model(zero)[0][0,target].detach());igerr=float(attr.sum().detach())-(logit-base_logit)
 # Compare attribution-ranked deletion with a fixed random deletion schedule.
 order_ig=np.argsort(-np.abs(attr.detach().numpy().ravel()));order_random=np.random.default_rng(250).permutation(64);delete={}
 for name,order in [('IG',order_ig),('Random',order_random)]:
  vals=[]
  for n in range(0,65,4):xx=image.clone();xx.view(-1)[torch.tensor(order[:n].copy())]=0;vals.append(float(model(xx)[0][0,target].detach()))
  delete[name]=vals
 fig,axs=plt.subplots(2,3,figsize=(11,7.4),layout='constrained');maps=[image.numpy()[0,0],abs(grad.detach().numpy()[0,0]),attr.detach().numpy()[0,0],attrmean.detach().numpy()[0,0],cam_signed,cam];titles=[L('真实输入：3','Observed input: 3'),'|Saliency|',L('IG：黑色基线','IG: black baseline'),L('IG：均值基线','IG: mean baseline'),L('Grad-CAM：取正部之前','Grad-CAM: before positive-part step'),L('Grad-CAM：取正部之后','Grad-CAM: after positive-part step')]
 for j,(ax,arr,title) in enumerate(zip(axs.flat,maps,titles)):
  vmax=1 if j==5 else max(max(abs(maps[2]).max(),abs(maps[3]).max()) if j in [2,3] else abs(arr).max(),1e-8);im=ax.imshow(arr,cmap='coolwarm' if j in [2,3,4] else 'gray' if j==0 else 'magma',vmin=-vmax if j in [2,3,4] else 0,vmax=vmax);ax.set_title(title,fontsize=11);ax.set_xticks([]);ax.set_yticks([]);fig.colorbar(im,ax=ax,shrink=.6)
 save(fig,'image_attribution')
 # A controlled concept direction: synthetic central vertical versus horizontal strokes.
 concept=[];cl=[]
 for c in [0,1]:
  for _ in range(60):
   xx=rng.uniform(0,.1,(8,8));pos=int(rng.integers(2,6));xx[:,pos]=.9 if c else xx[:,pos]
   if c==0:xx[pos,:]=.9
   concept.append(xx);cl.append(c)
 concept=torch.tensor(np.array(concept)[:,None],dtype=torch.float32);activation=model(concept)[1].detach().flatten(1).numpy();ct,ce=train_test_split(np.arange(120),test_size=.25,stratify=cl,random_state=25);probe=LogisticRegression(C=1,max_iter=2000).fit(activation[ct],np.array(cl)[ct]);cav=probe.coef_[0];cav/=np.linalg.norm(cav);probeacc=float(probe.score(activation[ce],np.array(cl)[ce]));tcav={}
 for k in [1,3,7]:
  sub=testx[labels[ie]==k];first=model(sub)[1].detach().requires_grad_(True);score=model.from_first(first)[0][:,k];direction=(torch.autograd.grad(score.sum(),first)[0].flatten(1).detach().numpy()*cav).sum(1);tcav[str(k)]={'n':len(sub),'positive_fraction':float(np.mean(direction>0)),'mean_directional_derivative':float(direction.mean())}
 # Input optimization maximizes one learned channel with L2 and total-variation regularization.
 vis=torch.tensor(rng.uniform(.2,.8,(1,1,8,8)),dtype=torch.float32,requires_grad=True);vo=torch.optim.Adam([vis],lr=.04);channel=2
 for _ in range(100):
  acts=model(vis)[1];tv=(vis[:,:,:,1:]-vis[:,:,:,:-1]).square().mean()+(vis[:,:,1:]-vis[:,:,:-1]).square().mean();loss=-acts[:,channel].mean()+.03*vis.square().mean()+.1*tv;vo.zero_grad();loss.backward();vo.step()
  with torch.no_grad():vis.clamp_(0,1)
 # Intervention on a trained internal channel: zero channel2 in conv1 before the rest of the network.
 first=model(testx)[1].detach();ablated=first.clone();ablated[:,channel]=0;ablacc=float(np.mean(model.from_first(ablated)[0].argmax(1).detach().numpy()==labels[ie]));activation_drop=float((model.from_first(first)[0][:,3]-model.from_first(ablated)[0][:,3]).mean().detach())
 fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
 for name,vals in delete.items():axs[0].plot(range(0,65,4),vals,'o-',label=name)
 axs[0].set(xlabel=L('归零像素数','Pixels set to zero'),ylabel=L('数字3的logit','Digit-3 logit'),title=L('同一图像、同一黑色替换','Same image and black replacement'));axs[0].legend();vim=axs[1].imshow(vis.detach().numpy()[0,0],cmap='gray',vmin=0,vmax=1);axs[1].set_title(L('通道2偏好的亮度模式','Channel-2 brightness preference'));axs[1].set_xticks([]);axs[1].set_yticks([])
 for spine in axs[1].spines.values():spine.set_visible(True);spine.set_color('#8fa5b1')
 fig.colorbar(vim,ax=axs[1],shrink=.6,label=L('归一化强度','Normalized intensity'));axs[2].bar(list(tcav),[v['positive_fraction'] for v in tcav.values()],color='#247b94');axs[2].set(ylim=(0,1.05),xlabel=L('测试真实类别','True test class'),ylabel=L('概念方向导数为正的比例','Fraction with positive concept derivative'),title=L('竖线相对横线的方向','Vertical-versus-horizontal direction'));save(fig,'interventions_concepts')
 train_acts=model(trainx)[1][:,channel].mean((1,2)).detach().numpy();top6=np.argsort(-train_acts)[:6];fig,axs=plt.subplots(2,6,figsize=(12,4.8),layout='constrained')
 for j,k in enumerate([60,61,62,0,1,2]):axs[0,j].imshow(concept[k,0],cmap='gray',vmin=0,vmax=1);axs[0,j].set_title(L('竖线','Vertical') if k>=60 else L('横线','Horizontal'))
 for j,k in enumerate(top6):axs[1,j].imshow(trainx[k,0],cmap='gray',vmin=0,vmax=1);axs[1,j].set_title(f'label={int(trainy[k])}, a={train_acts[k]:.2f}',fontsize=9)
 for ax in axs.flat:ax.set_xticks([]);ax.set_yticks([])
 fig.suptitle(L('上：合成概念样本；下：通道2平均激活最高的训练图','Top: synthetic concept examples; bottom: training images with highest channel-2 mean activation'));save(fig,'concept_examples')
 # Transparent feasible counterfactual for a two-feature score, with x1 immutable.
 original=np.array([1.,1.]);threshold=5.;changed=original.copy();changed[1]=(threshold-original[0])/2;cf_score=float(changed[0]+2*changed[1])
 summary={'tabular_train_n':len(tr),'tabular_test_n':len(te),'feature_correlation':float(np.corrcoef(X[:,0],X[:,2])[0,1]),'rmse':rmse,'permutation':perm,'shap_point':x.tolist(),'shap_values':phi.tolist(),'shap_base':base,'shap_prediction':pred,'shap_additivity_error':float(base+phi.sum()-pred),'shap_alternative_values':altphi.tolist(),'shap_alternative_base':altbase,'lime':lime,'digits_train_n':len(it),'digits_test_n':len(ie),'digits_accuracy':acc,'selected_test_index':selected,'selected_original_index':int(ie[selected]),'target_logit':logit,'black_baseline_logit':base_logit,'ig_sum':float(attr.sum().detach()),'ig_completeness_error':igerr,'concept_probe_accuracy':probeacc,'concept_direction':tcav,'ablated_channel':channel,'ablated_accuracy':ablacc,'class3_mean_logit_drop_after_ablation':activation_drop,'counterfactual_original_score':3.,'counterfactual_new_score':cf_score,'counterfactual_immutable_error':float(changed[0]-original[0]),'deletion':delete}
 constrained_x=np.tile(x,(60,1));constrained_x[:,0]=grid;summary['monotonic_violation']=float(max(0,-np.min(np.diff(models['Monotonic'].predict(constrained_x)))));summary['ale_weighted_mean']=float(np.average(ale,weights=counts));summary['gradcam_signed_range']=[float(cam_signed.min()),float(cam_signed.max())];summary['gradcam_positive_max']=float(cam.max());summary['channel2_brightness_correlation']=float(np.corrcoef(trainx.mean((1,2,3)).numpy(),train_acts)[0,1])
 torch.save(model.state_dict(),out/'digits-cnn.pt');np.savez_compressed(out/'experiment_data.npz',X=X,y=y,train_indices=tr,test_indices=te,pdp_grid=grid,pdp=pdp,ale_edges=edges,ale=ale,shap=shaps,digits_train_indices=it,digits_test_indices=ie,image=image.numpy(),gradient=grad.detach().numpy(),ig=attr.detach().numpy(),ig_mean=attrmean.detach().numpy(),gradcam=cam,concept_images=concept.numpy(),concept_labels=np.array(cl),cav=cav,optimized_stimulus=vis.detach().numpy(),loss_trace=trace);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

开始新的解释任务时，先写一句清楚的问题：解释哪个模型的哪个输出，对哪个对象、相对哪种参照，要帮助做什么判断。随后选择一个与问题匹配的方法，再用另一种计算或干预检查它。这样，模型解释就从一幅附在预测旁边的插图，变成能够发现问题、提出假设并指导下一步实验的研究工具。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M25.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Christoph Molnar — Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/)

   解释目标与方法组织。

   CC BY-NC-SA book; linked, no figure copied
2. [Ribeiro et al. (2016), Why Should I Trust You?](https://arxiv.org/abs/1602.04938)

   局部代理模型的原始问题。

   Primary reference
3. [SHAP — Beeswarm example and TreeExplainer](https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/plots/beeswarm.html)

   原图、背景样本与贡献分布。

   MIT, unmodified figure
4. [SHAP — TreeExplainer output scale](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html)

   XGBoost默认raw输出为log-odds。

   MIT documentation
5. [Sundararajan et al. (2017), Axiomatic Attribution for Deep Networks](https://proceedings.mlr.press/v70/sundararajan17a.html)

   IG、参照与归因性质。

   Primary reference
6. [Captum — Integrated Gradients](https://captum.ai/docs/extension/integrated_gradients)

   目标、基线与求和误差。

   Official technical reference
7. [Selvaraju et al., Grad-CAM](https://arxiv.org/abs/1610.02391)

   卷积层梯度定位，ICCV2017及后续版本。

   Primary reference
8. [Kim et al. (2018), TCAV](https://proceedings.mlr.press/v80/kim18d.html)

   概念方向与敏感性。

   Primary reference
9. [Olah, Mordvintsev & Schubert (2017), Feature Visualization](https://distill.pub/2017/feature-visualization/)

   优化刺激、多样性与原图。

   CC BY4.0, unmodified figure
10. [Adebayo et al., Sanity Checks for Saliency Maps](https://arxiv.org/abs/1810.03292)

    参数/标签随机化与解释评价。

    Primary reference
11. [UCI — Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    8×8数字数据，scikit-learn内置原始测试子集重新划分。

    CC BY4.0
