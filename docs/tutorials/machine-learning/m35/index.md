# 点云怎样变形，密度怎样改变：Normalizing Flow

Source: https://ml-biomat.com/tutorials/machine-learning/m35/
Language: zh-CN

用概率质量守恒理解体积变化与Jacobian，从仿射耦合走到样条与连续流，并训练一个能采样、打分和逆向回算的模型。

## 1 把一团点拉成弯月，概率去了哪里

假设一台设备记录了两项传感器读数。它们常常沿一条弯曲带状区域共同变化：第一项升高时，第二项先降后升。只用平均值和协方差画一个椭圆，会把弯带中间许多很少出现的位置也当成常见状态。我们希望学到更贴近这条带子的概率分布，既能生成合理的新读数，也能计算某次观测落在怎样的密度区域。Normalizing Flow把这个任务转化为一个几何问题：能否通过一系列可逆变形，把复杂的数据云变回容易计算的高斯云？

想象一块印着点阵的弹性薄膜。把某个小方格拉大，格内点的数量没有改变，单位面积内的点却变稀了；把方格压小，密度就升高。概率也遵守这样的质量守恒：同一批可能结果被移动到另一个区域，所携带的概率质量不变，但它占据的长度、面积或高维体积会改变。Flow需要记录这种变化，所以它既移动点，也计算局部拉伸系数。这个系数正是后面Jacobian行列式的几何含义。

$$
x=f(z),\qquad p_X(x)=p_Z(z)\left|\frac{dz}{dx}\right|=\frac{p_Z(z)}{|f'(z)|},\qquad z=f^{-1}(x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/62ff9d7345c45d49c87a5d02.svg) | 基础变量、变换后的变量、可微可逆映射与逆函数；例子均用无量纲坐标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bd0b4ae4b916ebfc8fbea14f.svg) | 输入与输出概率密度，单位分别为输入和输出坐标单位的倒数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ad3f3fdb5413303f68fbd0.svg) | 局部斜率、逆变换斜率与绝对值；绝对值保留正的长度比例。 |

对应小区间携带同一概率：p_X(x)dx≈p_Z(z)dz。若x=2z+3，斜率为2，在x=3对应z=0，密度为1/(2√(2π))≈0.199471。若反向翻转坐标，斜率可为负，密度仍使用绝对值。

一维时已经能看清全部道理。令标准正态变量先放大两倍再向右平移3，得到的新分布中心在3，宽度变为原来的两倍。中心处密度从约0.398942降为0.199471，因为同样的概率质量现在占据两倍长度。平移只改变位置，放大才改变密度。这里说的是概率密度，不是“恰好等于3”的概率；连续变量落在一个精确点上的概率为0，落在一个小区间的概率才近似等于该处密度乘区间宽度。

## 2 从长度到面积：为什么要算行列式

二维变换可以同时旋转、剪切和拉伸，单看一根边的长度已经不够。Jacobian矩阵记录每个输出坐标对每个输入坐标的小变化有多敏感。把它作用在一个足够小的单位方格上，方格近似变成平行四边形；行列式的绝对值给出面积比。若横向放大2倍、纵向放大3倍，面积放大6倍，密度相应除以6。若只做剪切，形状看似倾斜，面积却可能保持不变，密度也就不需要因局部面积而修正。

$$
\log p_X(x)=\log p_Z(g(x))+\log|\det J_g(x)|,\qquad J_{g,ij}=\frac{\partial g_i}{\partial x_j},\qquad g=f^{-1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1948951fb2582b68d628dbcb.svg) | D维数据向量、D维潜向量、生成映射与归一化逆映射；本例D=2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bdd32a98db8b6d68e884c880.svg) | D×D Jacobian矩阵、输出坐标索引与输入坐标索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4628700cca9689c491f4e5e5.svg) | 行列式、绝对值、自然对数及两侧密度；在固定坐标单位下对数密度按nats计。 |

若生成方向横向放大2倍、纵向放大3倍，J_f行列式为6，J_g行列式为1/6，输出对数密度减少ln6。多层复合时Jacobian相乘，行列式也相乘，所以对数行列式逐层相加。绝对值只处理方向，不能把奇异矩阵变成可逆矩阵。

我们约定生成方向为从简单变量z到数据x的映射f，计算观测密度时使用逆映射g。拿到一个数据点，先通过g找回它对应的高斯坐标，再加上逆变换的对数体积修正。使用对数能把很多层的行列式乘积变成和，避免直接相乘导致极大或极小的数。同一过程如果改从生成方向写，修正项前面就变成负号；记住“被拉大的区域密度下降”，比孤立背一个正负号更可靠。

这种方法要求保留信息。若把二维点投影成一个数，很多不同点会挤到同一输出，便无法靠单一逆函数找回原位置。普通AE允许压缩到更低维，Flow的基本可逆层则保持维数。图像中的重新排列、棋盘拆分、通道交换可以改变张量外形，却要保留全部元素。可逆性还约束分布的形状：一个连续可逆映射不会把连通空间凭空撕成几块；实际模型可以把连接区域的密度压得很低，从而近似看似分离的多个簇。

## 3 留下半边作为参照，另一半就容易找回

一个任意深度网络，即使输入输出维数相同，也未必容易求逆，更未必容易计算大矩阵的行列式。2016年发布的Real NVP采用仿射耦合层：先把坐标分成两组，一组暂时不动，用它计算另一组的缩放和平移。逆向时，参照组仍然原封不动地在那里，因此能重新计算相同的缩放和平移，再做减法与除法。复杂神经网络只负责给出变换系数，网络本身不必可逆。

$$
y_a=x_a,\quad y_b=x_b\odot e^{s(x_a)}+t(x_a),\qquad x_b=(y_b-t(y_a))\odot e^{-s(y_a)},\qquad \log|\det J|=\sum_j s_j(x_a)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64a9e92858a356da3c167f14.svg) | 输入与输出的两组坐标；a组保持不变，b组被变换。本章每组一个标量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9d0ae721d9a4bed70799a71d.svg) | 由参照组计算的对数尺度、平移和正尺度；形状与b组相同。s无量纲，t与被变换坐标同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a2f763450e66e0be3c61a7cf.svg) | 逐元素乘法、该层Jacobian，以及被变换组的分量索引。 |

取s=ln2、t(x_a)=3x_a，输入(0.5,1)变为(0.5,3.5)。Jacobian为[[1,0],[3,2]]，行列式2，对数修正ln2≈0.693147。逆变换使用保留下来的y_a重新算出系数，无需对系数网络求逆。代码默认执行该层的归一化方向，生成时反序调用inverse=True。

例如保留第一个坐标，把第二个坐标变成原来的两倍，再加上第一个坐标的三倍。输入(0.5,1)会变成(0.5,3.5)；逆向时先看到保留的0.5，再计算(3.5−1.5)/2，便找回1。Jacobian是对角线上为1和2的三角矩阵，行列式直接等于2。第二个输出也依赖第一个输入，这种交叉影响写在非对角位置，却不改变三角矩阵的行列式乘积规则。于是一个复杂系数网络可以参与弯曲变形，同时保留简单的密度计算。

![UvA原始checkerboard mask图：黑白格把变量分成保留组与变换组。Phillip Lippe，UvA Deep Learning Tutorials；原图未改动，MIT许可与版权文本随图保留。](https://ml-biomat.com/static/tutorials/machine-learning/figures/06a123405b6d85e5317668d5.svg?v=06a123405b6d)

图 1UvA原始checkerboard mask图：黑白格把变量分成保留组与变换组。Phillip Lippe，UvA Deep Learning Tutorials；原图未改动，MIT许可与版权文本随图保留。

一次耦合层只改变一组变量，所以要交换角色再继续。二维例子交替保留第一、第二坐标，图像则可像原图那样使用棋盘遮罩，让黑格提供参照、白格接受变换，下一层再反过来。这里的遮罩用于划分参与变换的变量，与PixelCNN遮住未来答案的因果遮罩用途不同。堆叠之后，每个变量都能影响其他变量，逆向计算则严格按相反层序逐层撤销。少撤销一层、层序写反，往往都能立刻从回算误差中看出来。

## 4 真正训练一个弯曲分布的可逆网络

实验从两个独立标准正态数出发，把第一个乘1.2，把第二个乘0.35后加上第一项平方产生的弯曲偏移。这样得到一条有厚度的“香蕉”形点云。因为生成规则已知，我们可以算出真实目标密度，并把它与网络学出的密度放在同一个色标下比较。4096个训练点、1024个验证点和2048个测试点分别使用独立种子生成；训练程序只使用前两组选择参数，测试组留到最后评价。

$$
x_1=1.2z_1,\quad x_2=0.35z_2+0.55(z_1^2-1),\quad z\sim\mathcal N(0,I_2),\qquad L(\theta)=-\frac1N\sum_{n=1}^N\log p_\theta(x^{(n)})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/de213b795d23890187cb5527.svg) | 两个独立标准正态坐标及弯曲后的两个坐标，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/03df122ca86d7ab9c1db3258.svg) | 零均值单位协方差二维高斯，以及本例的横向尺度、纵向厚度与弯曲系数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1172e770bf980becbada7547.svg) | 网络参数、训练点数、样本索引、第n个样本、平均负对数密度目标，按nats/点计。 |

生成Jacobian为[[1.2,0],[1.1z₁,0.35]]，行列式恒为0.42，因此真实密度等于对应标准高斯密度除以0.42。z=(0,0)对应x=(0,−0.55)，密度约0.378940。训练网络不使用这个解析密度作为标签，而只对训练点最大化自身密度；解析密度用于独立比较。

网络由八个仿射耦合层组成，每个系数网络包含两层32维tanh隐藏层，合计9488个参数。它沿数据到高斯的方向计算对数密度，以平均负对数密度作为损失。缩放的对数通过0.8乘tanh限制在−0.8到0.8之间，避免单层指数尺度过大。最后一个线性层从零开始，使初始耦合接近恒等映射；训练200轮后，验证损失选择第121轮权重。这个设计让模型先从平稳的坐标系统出发，再逐渐学会弯曲和压缩。

一次训练更新同时衡量两种作用。把数据点送到高斯中心附近，会提高基础分布给出的密度；把许多不同点压进很小的潜空间，又会通过Jacobian带来相应体积修正。两项必须一起算，才能得到原数据坐标中的正确密度。如果只奖励点靠近原点，网络会倾向把所有数据挤成一团，却没有学到原来不同区域各占多少概率。可逆结构和体积项把位置变化与密度变化联系起来，训练目标才真正对应所要拟合的分布。

![左：700个独立目标点（橙）与700个生成点（蓝）。中：已知生成规则的密度。右：训练后Flow的变量变换密度。两幅密度图共用范围和色标，坐标均无量纲。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3ef27629ad6f04d26cffa6cd.svg?v=3ef27629ad6f)

图 2左：700个独立目标点（橙）与700个生成点（蓝）。中：已知生成规则的密度。右：训练后Flow的变量变换密度。两幅密度图共用范围和色标，坐标均无量纲。

在同一批独立测试点上，单高斯拟合的平均负对数密度为2.883696 nats，Flow为1.964784，真实生成分布自身为1.961473。目标密度这一项表示真实分布给这批具体点的平均分数，帮助判断网络已经接近到什么程度；有限样本分数也会随测试点变化。图中散点显示实际抽样，密度面板则来自变量变换公式，二者是不同的计算。只看散点容易忽略细小质量偏差，只看密度又可能没发现采样方向的层序错误，因此需要一起检查。

![标准高斯坐标中的同一张网格，依次经过0、2、4、8个真实逆向耦合层；橙点为相同160个潜样本的变换结果。网格线随变换弯曲，交点保持一一对应。](https://ml-biomat.com/static/tutorials/machine-learning/figures/921bdfe5ead3dc47fdb47682.svg?v=921bdfe5ead3)

图 3标准高斯坐标中的同一张网格，依次经过0、2、4、8个真实逆向耦合层；橙点为相同160个潜样本的变换结果。网格线随变换弯曲，交点保持一一对应。

本例把2048个测试点归一化后再生成回来，最大坐标误差约1.91×10⁻⁶。正反向对数行列式相加的最大误差约4.17×10⁻⁷。在选定二维点处，另用自动微分展开完整Jacobian，再算行列式，与各层累加结果相差约3.3×10⁻¹⁶。这些检查对应三个不同问题：位置能否找回、体积修正能否抵消、简化公式是否与完整导数一致。它们把“网络结构理论上可逆”落实到了实际程序的数值结果。

## 沿真实可逆层移动一张网格

网格与样本来自训练后的八层Flow。选定高斯起点，逐层生成并同时查看面积比、密度和逆向恢复误差。每一步使用实际网络权重；前进与后退都可单步操作。

[Figure: 潜空间与变换后网格的对应，含面积与密度](https://ml-biomat.com/tutorials/machine-learning/m35/#M35-board)

蓝线为同一张网格，橙点为固定160组潜样本，红点为选定起点及其变换；红虚线依次连接各层输出坐标。坐标无量纲；两图采用相同的每单位长度比例。面积比由Jacobian计算，密度为起始高斯密度除以该面积比。

## 5 自回归Flow：哪一个方向能够并行

耦合层通过暂时保留一组变量获得容易的逆运算，自回归Flow则让第i个变量的变换参数依赖前面的变量。这样Jacobian同样具有三角结构，但计算速度会随依赖方向而改变。2017年的Masked Autoregressive Flow，简称MAF，适合密度估计：给定完整数据向量后，各个位置需要的前缀都已经知道，遮罩网络可以一次算出各维的均值和尺度，再同时得到所有潜变量。生成数据时，后面的均值与尺度却要等待前面生成出的数据坐标。

$$
z_i=\frac{x_i-\mu_i(x_{<i})}{\sigma_i(x_{<i})},\qquad \sigma_i>0,\qquad \log|\det J_{x\to z}|=-\sum_{i=1}^{D}\log\sigma_i(x_{<i})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/49176a361325b6b62d8f3501.svg) | 第i个数据坐标、潜坐标、前面所有数据坐标与总维度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc1454c20c7160593f31559a.svg) | 由数据前缀预测的平移与正尺度；μ与x同单位，σ把数据单位映射到潜变量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/67575451a8129bb2d625dc8b.svg) | 从数据到潜变量的三角Jacobian、自然对数与行列式。 |

MAF在给定完整x时并行算各维参数。若二维σ=(2,3)，逆向体积比为1/6，对数修正−ln6。生成时x_i=μ_i(x_<i)+σ_i(x_<i)z_i，需要先得到前面的x。IAF改让生成系数依赖z_<i，使已知z的生成方向能够并行。

Inverse Autoregressive Flow，简称IAF，把便于并行的方向放在生成一侧：已抽好的整组潜变量作为输入，第i个数据坐标的系数依赖前面的潜变量。因为所有潜变量同时已知，生成可以一次计算；若只有数据点而要反求潜变量，则需要按顺序恢复。名字里的“逆”提醒我们关注哪一侧作为系数网络的输入，不能仅凭“自回归”三个字就断言采样一定慢。比较实现时，应分别询问一次密度计算和一次生成各需要多少轮网络调用。

用三个数可以看到依赖差别。设生成规则为x₁=z₁，x₂=z₂+0.5z₁，x₃=z₃+z₁z₂；给定整个z向量，三个式子的右侧全部已知。给定x时，则先恢复z₁，再恢复z₂，最后才能恢复z₃。这种依赖顺序与上一章字符生成相似，但这里每一步是连续坐标的可逆变换，并且同时记录密度。耦合层、MAF和IAF可以在表达灵活性、网络调用次数和主要使用方向之间做不同取舍；样条变换还能进一步改变每个坐标内部的形状。

## 6 把直线缩放换成柔软的单调曲线

仿射变换在固定参照变量后，只会对另一坐标做直线式缩放和平移。若希望同一坐标在一处被压缩、另一处被拉伸，可以换成保持单调的非线性曲线。Neural Spline Flows在2019年采用单调有理二次样条：先设置一串顺序一致的输入与输出结点，再给结点指定正的导数，在相邻结点之间连接平滑曲线。输入始终向右走，输出也始终向右走，因此不会出现两个输入挤到同一输出的折返。

$$
\xi=\frac{x-x_0}{w},\quad s=\frac hw,\qquad f(x)=y_0+\frac{h\left[s\xi^2+d_0\xi(1-\xi)\right]}{s+(d_0+d_1-2s)\xi(1-\xi)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b578ba9b754822a716ede6.svg) | 当前样条段左端输入/输出结点、输入区间宽与输出区间高，w、h严格为正。 |
| ![Formula](https://ml-biomat.com/static/agent-math/17bae4178ce5e4537b485569.svg) | 段内输入、映射到0–1的局部坐标、该段割线斜率h/w。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fe5457fb4e7b4cb7078ce6c0.svg) | 左右端点的正导数与输出值；导数单位为输出坐标单位/输入坐标单位。本例均无量纲。 |

在本例区间x∈[−1,0]，y∈[−2,0.5]，w=1、h=2.5、d₀=0.5、d₁=2。取x=−0.5，ξ=0.5，分母为1.875，分子为1.875，所以f(x)=−1；用商法则可得该处导数10/3。正反向代码都使用同一组结点与端点导数，逆向在对应输出区间内解二次方程。

公式看起来比缩放加平移长，是因为它同时满足几个边界条件：经过左右两个结点，在两端具有指定斜率，并且在区间内部保持单调。分子和分母都是局部坐标的二次多项式，反过来给定输出时，整理后仍是一个可解析求解的二次方程。代码采用避免相近数相减的根式，并单独处理退化成一次方程的情况。正的区间宽度、高度和端点导数，使曲线能够柔软变形而保持可逆。

结点也规定了局部计算的顺序。正向给定输入时，先找到它位于哪两个输入结点之间，再使用这一段的宽度、高度与导数。逆向给定输出时，则在输出结点中定位区间。两种查找使用不同的横轴，找到的却是同一段对应关系。区间之外接上恒等直线，使远处的点也有定义；两端斜率设为1，让样条与直线尾部在连接处平滑衔接。这些边界约定直接影响尾部密度和逆向结果，属于完整变换的一部分。

![预设五结点有理二次样条：曲线、正导数、5000个变换后样本的直方图与解析变量变换密度。范围外接恒等尾部；端点导数为1。该图单独说明样条机制。](https://ml-biomat.com/static/tutorials/machine-learning/figures/02b750664c68fd44ee7702bd.svg?v=02b750664c68)

图 4预设五结点有理二次样条：曲线、正导数、5000个变换后样本的直方图与解析变量变换密度。范围外接恒等尾部；端点导数为1。该图单独说明样条机制。

图中使用五个预先指定的结点来单独展示样条机制，并没有把它冒充另一项训练结果。左图画出曲线与结点，中图显示各处斜率始终为正，右图把5000个高斯样本通过曲线后的直方图与变量变换密度叠在一起。曲线拉得陡的地方，原来的概率质量分散到更宽范围；压得平的地方，输出密度升高。1401个测试位置的正反向最大误差约1.1×10⁻¹⁵，有限差分导数与解析导数最大差约4.5×10⁻¹⁰，验证了逆解和局部伸缩的对应。

实际的神经样条Flow会让条件网络输出各段宽度、高度和导数，再用softmax或softplus等变换保证它们满足正性要求。样条既可放进耦合层，也可放进自回归结构，因而它描述的是“单个坐标怎样变换”，不与前两种条件依赖方式互相排斥。图像像素是离散整数，还要处理离散与连续之间的关系：常见做法在每个整数格内加入均匀噪声，再训练连续密度；原离散像素值的概率对应一个小格内的密度积分，而不是格中心的单点密度。

## 7 很多小步接起来，就走到连续Flow

离散Flow把变换分成若干可逆层；连续Normalizing Flow则给每个位置规定一个随时间变化的速度场，让点沿常微分方程移动。只要速度场满足保证解存在唯一的适当条件，知道终点和完整动力学，就能向后积分找回起点。点云在流动中同样遵守概率质量守恒，密度变化取决于周围的小体积正在膨胀还是收缩。这个局部膨胀率由速度场Jacobian的迹，也就是散度给出。

$$
\frac{dx_t}{dt}=v_\theta(x_t,t),\qquad \frac{d\log p_t(x_t)}{dt}=-\operatorname{tr}\!\left(\frac{\partial v_\theta}{\partial x_t}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9afa3cb39c93766ce5e0d003.svg) | 时间t的D维坐标、连续时间、D维速度场与其参数；本例时间与坐标均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea03d1e0f61a4a14eff275ea.svg) | 沿移动轨迹的密度，以及沿该轨迹取的全导数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d1bdb262be05fb4f5450d327.svg) | D×D速度Jacobian与其对角线之和；散度单位为时间的倒数。 |

取v=(0.4x₁,−0.2x₂)，Jacobian迹为0.2，故时间1内对数密度下降0.2。坐标解析变化为x₁(1)=e^0.4x₁(0)、x₂(1)=e^(−0.2)x₂(0)，面积比e^0.2，与密度因子e^(−0.2)相抵。一般神经速度场需要数值积分，并同时累积密度变化。

把时间缩短到一个很小的步长，可以将局部变换近似为“原坐标加速度乘步长”。它的Jacobian接近单位矩阵加速度Jacobian乘步长，体积比的一阶变化由对角线之和决定。这解释了为什么离散层需要行列式，而连续密度方程出现迹。2018年的FFJORD进一步用随机迹估计降低高维计算成本；二维小例子则可以直接求完整迹，把空间变化与对数密度变化都清楚地算出来。

![左：线性速度场下(1,1)到时间1的解析轨迹。右：RK4使用1、2、4、8、16步后的实际终点最大绝对误差，双对数坐标；比较对象是解析终点。](https://ml-biomat.com/static/tutorials/machine-learning/figures/c206a9d51bc6e1de4ffec4d6.svg?v=c206a9d51bc6)

图 5左：线性速度场下(1,1)到时间1的解析轨迹。右：RK4使用1、2、4、8、16步后的实际终点最大绝对误差，双对数坐标；比较对象是解析终点。

代码选择横向按0.4倍当前位置增长、纵向按−0.2倍当前位置变化的速度场。从(1,1)出发，时间1的解析终点约为(1.491825,0.818731)。面积放大为原来的exp(0.2)，沿轨迹的对数密度因此下降0.2。用RK4积分，一步的终点最大误差约9.14×10⁻⁵，十六步降至1.90×10⁻⁹。理论动力学的可逆性与数值求解精度是两个需要分别检查的对象；选步长、容差和积分器时，要把计算成本与坐标、密度误差一起记录。

## 8 用密度发现变化，也要认识概率质量的位置

当正常数据的分布已学好，可以把低密度位置作为需要检查的观测。这里在验证集的对数密度下侧5%位置确定阈值，随后冻结阈值。独立正常测试点中约4.98%被标记，把另一组独立点整体向上移动1.5后，约97.66%被标记。这个结果对应一种明确的变化：整条弯带相对于训练位置发生了竖直偏移。阈值不是从测试异常里挑出的，因而可以同时读到正常点的标记比例与这一特定变化的检出比例。

![左：训练/验证平均负对数密度，虚线为真实分布在验证点上的分数。中：正常测试与竖直偏移点的分数直方图，阈值由验证集固定。右：64维高斯的半径密度（蓝，左轴）与相对原点的点密度（橙，右轴）。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f09d18ac566ff3086a3d06a5.svg?v=f09d18ac566f)

图 6左：训练/验证平均负对数密度，虚线为真实分布在验证点上的分数。中：正常测试与竖直偏移点的分数直方图，阈值由验证集固定。右：64维高斯的半径密度（蓝，左轴）与相对原点的点密度（橙，右轴）。

密度与概率质量仍有区别。图中64维标准高斯在原点的点密度最高，但大多数样本的半径接近8，因为远离原点处有极多方向和空间位置。最右图的蓝线统计“半径落在某个小区间”的概率密度，橙色虚线则表示单点密度相对原点怎样下降；它们回答不同问题。若某项业务关注的是类别含义、失效风险或违规组合，还需要定义与这些对象对应的评价数据。低密度分数首先衡量相对于所学坐标分布的稀少程度，具体研究任务再决定这种稀少程度如何进入判断。

### 完整Python：训练Real NVP、样条变换和连续流

运行python main.py --output results --language zh。依赖NumPy、Matplotlib和PyTorch。数据全部由显式规则生成；网络实际训练，样条与线性ODE为独立机制计算。输出权重、原始点、密度、网格和五幅SVG。

```
"""Eight affine coupling layers learn a known curved density.
Also compute rational-quadratic splines and a continuous linear flow.
"""
from pathlib import Path
import argparse,json,math,copy,platform
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
def banana(n,seed):
 z=np.random.default_rng(seed).normal(size=(n,2));return np.c_[1.2*z[:,0],.35*z[:,1]+.55*(z[:,0]**2-1)].astype('float32')
def true_logp(x):
 z=np.c_[x[:,0]/1.2,(x[:,1]-.55*((x[:,0]/1.2)**2-1))/.35];return -.5*(z*z).sum(1)-math.log(2*math.pi)-math.log(.42)
train,valid,test=banana(4096,350),banana(1024,351),banana(2048,352);xt=torch.tensor(train);xv=torch.tensor(valid);xe=torch.tensor(test)
class Coupling(nn.Module):
 def __init__(self,keep):
  super().__init__();self.keep=keep;self.change=1-keep;self.net=nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2));nn.init.zeros_(self.net[-1].weight);nn.init.zeros_(self.net[-1].bias)
 def forward(self,x,inverse=False):
  coeff=self.net(x[:,self.keep:self.keep+1]);s=.8*torch.tanh(coeff[:,0]);t=coeff[:,1];y=x.clone()
  if inverse:y[:,self.change]=x[:,self.change]*torch.exp(s)+t;ld=s
  else:y[:,self.change]=(x[:,self.change]-t)*torch.exp(-s);ld=-s
  return y,ld
class Flow(nn.Module):
 def __init__(self):super().__init__();self.layers=nn.ModuleList([Coupling(i%2) for i in range(8)])
 def forward(self,x,inverse=False):
  ld=x.new_zeros(len(x));layers=reversed(self.layers) if inverse else self.layers
  for layer in layers:x,delta=layer(x,inverse);ld=ld+delta
  return x,ld
 def logp(self,x):
  z,ld=self(x);return -.5*(z*z).sum(1)-math.log(2*math.pi)+ld
torch.manual_seed(355);model=Flow();optimizer=torch.optim.Adam(model.parameters(),lr=.001);rng=torch.Generator().manual_seed(356);history=[];best=float('inf');best_state=None;best_epoch=0
for epoch in range(1,201):
 order=torch.randperm(len(xt),generator=rng);total=0.
 for idx in order.split(256):
  loss=-model.logp(xt[idx]).mean();optimizer.zero_grad();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),5);optimizer.step();total+=loss.item()*len(idx)
 with torch.no_grad():val=-model.logp(xv).mean().item()
 history.append([epoch,total/len(xt),val])
 if val<best:best=val;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch
model.load_state_dict(best_state);model.eval();torch.save(dict(model=model.state_dict(),best_epoch=best_epoch),out/'realnvp.pt')
with torch.no_grad():
 test_lp=model.logp(xe).numpy();val_lp=model.logp(xv).numpy();latents=np.random.default_rng(357).normal(size=(2048,2)).astype('float32');generated=model(torch.tensor(latents),True)[0].numpy();encoded,forward_ld=model(xe);restored,inverse_ld=model(encoded,True);roundtrip=float((restored-xe).abs().max());logdet_cancel=float((forward_ld+inverse_ld).abs().max())
mean=train.mean(0);cov=np.cov(train.T);inv_cov=np.linalg.inv(cov)
def gaussian_logp(x):return -.5*np.einsum('ni,ij,nj->n',x-mean,inv_cov,x-mean)-math.log(2*math.pi)-.5*np.linalg.slogdet(cov)[1]
anomalies=banana(2048,353);anomalies[:,1]+=1.5;threshold=float(np.quantile(val_lp,.05))
with torch.no_grad():anomaly_lp=model.logp(torch.tensor(anomalies)).numpy()
# Verify the learned triangular Jacobian against a full autograd Jacobian.
double_model=copy.deepcopy(model).double();point=torch.tensor([.4,-.2],dtype=torch.float64,requires_grad=True)
jac=torch.autograd.functional.jacobian(lambda x:double_model(x[None])[0][0],point);jac_logdet=torch.linalg.slogdet(jac)[1].item();analytic_ld=double_model(point[None])[1].item()
# One-dimensional rational-quadratic spline, identity tails and endpoint derivatives one.
xknots=np.array([-3.,-1.,0.,1.,3.]);yknots=np.array([-3.,-2.,.5,2.,3.]);derivatives=np.array([1.,.5,2.,.5,1.])
def spline(values,inverse=False):
 values=np.asarray(values,dtype=float);bins=np.clip(np.searchsorted(yknots if inverse else xknots,values,side='right')-1,0,len(xknots)-2);x0=xknots[bins];y0=yknots[bins];w=np.diff(xknots)[bins];h=np.diff(yknots)[bins];delta=h/w;d0=derivatives[bins];d1=derivatives[bins+1]
 if inverse:
  rel=values-y0;a=rel*(d0+d1-2*delta)+h*(delta-d0);b=h*d0-rel*(d0+d1-2*delta);c=-delta*rel;disc=np.maximum(b*b-4*a*c,0);linear=np.abs(a)<1e-12;xi=np.zeros_like(values);np.divide(2*c,-b-np.sqrt(disc),out=xi,where=~linear);np.divide(-c,b,out=xi,where=linear);result=x0+w*xi
 else:xi=(values-x0)/w;den=delta+(d0+d1-2*delta)*xi*(1-xi);result=y0+h*(delta*xi*xi+d0*xi*(1-xi))/den
 den=delta+(d0+d1-2*delta)*xi*(1-xi);deriv=delta**2*(d1*xi**2+2*delta*xi*(1-xi)+d0*(1-xi)**2)/den**2;outside=(values<=-3)|(values>=3);result=np.where(outside,values,result);deriv=np.where(outside,1,deriv)
 return result,(-np.log(deriv) if inverse else np.log(deriv))
sx=np.linspace(-3.5,3.5,1401);sy,sld=spline(sx);sback,_=spline(sy,True);finite=(spline(sx+1e-5)[0]-spline(sx-1e-5)[0])/2e-5
interior=np.min(np.abs(sx[:,None]-xknots[None]),axis=1)>.001;spline_derivative_error=float(np.max(np.abs(finite[interior]-np.exp(sld[interior]))));spline_inverse_error=float(np.max(np.abs(sx-sback)))
sz=np.random.default_rng(358).normal(size=5000);sgen=spline(sz)[0];grid1=np.linspace(-4,4,1000);latent1,invld=spline(grid1,True);spline_pdf=np.exp(-.5*latent1**2)/math.sqrt(2*math.pi)*np.exp(invld)
# A continuous flow with analytic solution and a separately implemented RK4 solver.
A=np.diag([.4,-.2]);z0=np.array([1.,1.]);exact=z0*np.exp(np.diag(A));ode=[]
def rhs(state):return A@state
for n in [1,2,4,8,16]:
 x=z0.copy();dt=1/n
 for _ in range(n):
  k1=rhs(x);k2=rhs(x+.5*dt*k1);k3=rhs(x+.5*dt*k2);k4=rhs(x+dt*k3);x+=dt*(k1+2*k2+2*k3+k4)/6
 ode.append(dict(steps=n,x=x.tolist(),max_error=float(np.max(np.abs(x-exact))),logdensity_change=-float(np.trace(A))))
# Layer-by-layer grids and samples are computed by the actual learned inverse.
lines=[]
for fixed in np.linspace(-2,2,9):
 t=np.linspace(-2,2,41);lines.extend([np.c_[np.full(len(t),fixed),t],np.c_[t,np.full(len(t),fixed)]])
gridlines=np.array(lines).astype('float32');frames=[];cur=torch.tensor(gridlines.reshape(-1,2));points=torch.tensor(latents[:160]);probe=torch.tensor([[.5,-.5]],dtype=torch.float32);ld_probe=0.
with torch.no_grad():
 for layer_index,layer in enumerate([None]+list(reversed(model.layers))):
  if layer is not None:cur,_=layer(cur,True);points,_=layer(points,True);probe,dl=layer(probe,True);ld_probe+=dl.item()
  frames.append(dict(layer=layer_index,grid=cur.reshape(gridlines.shape).numpy().tolist(),points=points.numpy().tolist(),probe=probe[0].tolist(),probe_logdet=ld_probe))
hand_spline_y,hand_spline_ld=spline(np.array([-.5]));weights=[]
for layer in model.layers:
 weights.append(dict(keep=layer.keep,layers=[dict(weight=m.weight.detach().numpy().tolist(),bias=m.bias.detach().numpy().tolist()) for m in layer.net if isinstance(m,nn.Linear)]))
(out/'flow-lab.json').write_text(json.dumps(dict(frames=frames,weights=weights),separators=(',',':')),encoding='utf-8')
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=2048,seed=[350,351,352],true_logdet=math.log(.42)),training=dict(epochs=200,best_epoch=best_epoch,parameters=sum(p.numel() for p in model.parameters()),layers=8,batch=256,lr=.001,scale_bound=.8),density=dict(flow_test_nll=float(-test_lp.mean()),gaussian_test_nll=float(-gaussian_logp(test).mean()),true_test_nll=float(-true_logp(test).mean()),roundtrip_max_error=roundtrip,logdet_cancel_error=logdet_cancel,jacobian_logdet=jac_logdet,analytic_logdet=analytic_ld,jacobian_error=abs(jac_logdet-analytic_ld)),anomaly=dict(logdensity_threshold=threshold,false_positive=float((test_lp<threshold).mean()),shifted_detection=float((anomaly_lp<threshold).mean()),vertical_shift=1.5),spline=dict(inverse_max_error=spline_inverse_error,derivative_max_error=spline_derivative_error,min_derivative=float(np.exp(sld).min())),ode=ode,hand=dict(affine_scale=2,affine_point_density=1/(2*math.sqrt(2*math.pi)),coupling_logdet=math.log(2),spline_midpoint=float(hand_spline_y[0]),spline_midpoint_derivative=float(np.exp(hand_spline_ld[0])),ode_logdensity_change=-.2,ode_final_x1=float(exact[0]),ode_final_x2=float(exact[1])))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,validation=valid,test=test,latents=latents,generated=generated,encoded=encoded.numpy(),test_logdensity=test_lp,anomalies=anomalies,anomaly_logdensity=anomaly_lp,history=history,spline_x=sx,spline_y=sy,spline_logderivative=sld,spline_generated=sgen,ode=np.array([[r['steps'],r['max_error']] for r in ode]))
# Density is shown on one common coordinate grid and color scale.
gx,gy=np.meshgrid(np.linspace(-4,4,180),np.linspace(-2,5,160));mesh=np.c_[gx.ravel(),gy.ravel()].astype('float32')
with torch.no_grad():density=np.exp(model.logp(torch.tensor(mesh)).numpy()).reshape(gx.shape)
true_density=np.exp(true_logp(mesh)).reshape(gx.shape);fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
axs[0].scatter(test[:700,0],test[:700,1],s=5,alpha=.5,color='#b97d43');axs[0].scatter(generated[:700,0],generated[:700,1],s=4,alpha=.4,color='#125f82');axs[0].set_title(tr('A  目标与生成：各700点','A  Target and generated: 700 each'))
for ax,img,title in zip(axs[1:],[true_density,density],[tr('B  已知目标密度','B  Known target density'),tr('C  可逆网络密度','C  Learned flow density')]):
 im=ax.pcolormesh(gx,gy,img,vmin=0,vmax=max(true_density.max(),density.max()),cmap='YlGnBu',shading='auto',rasterized=True);ax.set_title(title);fig.colorbar(im,ax=ax,label=tr('每单位面积概率密度','Density per unit area'))
for ax in axs:ax.set(xlim=(-4,4),ylim=(-2,5),xlabel='x1',ylabel='x2');ax.set_aspect('equal')
save(fig,'density')
fig,axs=plt.subplots(1,4,figsize=(14,4),layout='constrained')
for ax,i in zip(axs,[0,2,4,8]):
 frame=frames[i]
 for line in frame['grid']:line=np.array(line);ax.plot(line[:,0],line[:,1],color='#125f82',lw=.7,alpha=.8)
 pt=np.array(frame['points']);ax.scatter(pt[:,0],pt[:,1],s=3,color='#c17a3a',alpha=.5);ax.set(xlim=(-5,5),ylim=(-3,7),xlabel=tr('坐标1','Coordinate 1'),ylabel=tr('坐标2','Coordinate 2'),title=tr('逆向层数 ','Inverse layers ')+str(i));ax.set_aspect('equal')
save(fig,'grids')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');axs[0].plot(sx,sy,color='#125f82');axs[0].scatter(xknots,yknots,color='#bf7139',s=30);axs[0].plot(sx,sx,ls=':',color='#8c9698');axs[0].set(xlabel='z',ylabel='x = f(z)',title=tr('A  单调有理二次样条','A  Monotone rational-quadratic spline'))
axs[1].plot(sx,np.exp(sld),color='#bf7139');axs[1].axhline(0,color='#777',lw=.7);axs[1].set(xlabel='z',ylabel="f'(z)",title=tr('B  每处斜率保持为正','B  Positive slope throughout'))
axs[2].hist(sgen,bins=70,density=True,color='#8fb9c1',alpha=.7,label=tr('5000个样本','5,000 samples'));axs[2].plot(grid1,spline_pdf,color='#125f82',label=tr('变量变换密度','Change-of-variables density'));axs[2].set(xlabel='x',ylabel=tr('概率密度','Density'),title=tr('C  拉伸改变密度','C  Stretching changes density'));axs[2].legend(fontsize=9);save(fig,'spline')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,1],label=tr('训练','Train'));axs[0].plot(h[:,0],h[:,2],label=tr('验证','Validation'));axs[0].axhline(-true_logp(valid).mean(),ls=':',color='#555',label=tr('目标本身','True density'));axs[0].set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('负对数密度 / nats','Negative log density / nats'),title=tr('A  最大似然训练','A  Maximum-likelihood training'));axs[0].legend(fontsize=9)
axs[1].hist(-test_lp,bins=np.histogram_bin_edges(np.r_[-test_lp,-anomaly_lp],bins=45),density=True,alpha=.55,label=tr('目标测试集','Target test'),color='#125f82');axs[1].hist(-anomaly_lp,bins=np.histogram_bin_edges(np.r_[-test_lp,-anomaly_lp],bins=45),density=True,alpha=.45,label=tr('向上移1.5','Shifted upward 1.5'),color='#bf7139');axs[1].axvline(-threshold,ls='--',color='#222');axs[1].set(xlabel=tr('负对数密度分数','Negative log-density score'),ylabel=tr('直方图密度','Histogram density'),title=tr('B  用验证集确定阈值','B  Threshold set on validation'));axs[1].legend(fontsize=9)
r=np.linspace(.001,13,600);log_shell=(64-1)*np.log(r)-.5*r*r-(64/2-1)*math.log(2)-math.lgamma(64/2);axs[2].plot(r,np.exp(log_shell),color='#125f82',label=tr('半径概率密度','Radius density'));axs[2].set(xlabel=tr('64维标准高斯半径','Radius in a 64D standard normal'),ylabel=tr('半径概率密度','Radial density'),title=tr('C  概率质量聚集在一圈','C  Probability mass occupies a shell'));ax2=axs[2].twinx();ax2.plot(r,np.exp(-.5*r*r),ls='--',color='#bf7139');ax2.set_ylabel(tr('相对原点的点密度','Point density relative to origin'),color='#bf7139');save(fig,'diagnostics')
fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');times=np.linspace(0,1,101);path=z0[None]*np.exp(times[:,None]*np.diag(A));axs[0].plot(path[:,0],path[:,1],color='#125f82',lw=3);axs[0].scatter([1,exact[0]],[1,exact[1]],c=['#bf7139','#125f82'],s=60);axs[0].set(xlabel='x1',ylabel='x2',title=tr('A  dx/dt = diag(0.4, −0.2)x','A  dx/dt = diag(0.4, -0.2)x'));axs[0].set_aspect('equal');axs[1].loglog([x['steps'] for x in ode],[x['max_error'] for x in ode],'o-',color='#125f82');axs[1].set(xlabel=tr('RK4步数','RK4 steps'),ylabel=tr('相对解析终点的最大绝对误差','Maximum absolute endpoint error'),title=tr('B  连续可逆性与数值误差','B  Continuous invertibility and numerical error'));save(fig,'ode')
print(json.dumps(summary,indent=2))
```

完整脚本保存训练、验证、测试点，2048个生成点，逐层网格，模型权重，以及样条和ODE的计算结果。可以先固定模型，在交互中改变高斯起点并逐层查看它的去向，再比较生成空间中的密度与局部面积比。进一步改变传感器单位时，密度数值也会随坐标体积的单位改变，阈值需要与预处理保持一致。Flow的价值正在于把这些关系放在同一套可计算的框架内：样本怎样移动、密度怎样修正、逆向怎样恢复，都能沿着实际变换逐步检查。

由此也能理解它与其他生成方法的关系。VAE在边缘密度难以直接计算时，引入推断分布并优化下界；GAN通过对抗目标学习生成样本；基本Flow选择等维可逆映射，让密度可以通过体积变化求出。这些设计决定了评价与生成时可直接取得哪些量。比较方法时，可以从实际应用需要抽样、打分、控制条件还是恢复潜变量出发，再判断哪种结构最适合承担相应计算。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M35.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Density Estimation Using Real NVP](https://arxiv.org/html/1605.08803v3)

   变量变换、仿射耦合与逐层可逆性。

   Primary paper; no copied figures
2. [UvA Tutorial 11: Normalizing Flows for Image Modeling](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial11/NF_image_modeling.html)

   原始棋盘遮罩图、去量化与图像Flow结构。

   MIT; original notebook cell33 execution14 mask output only
3. [Masked Autoregressive Flow for Density Estimation](https://arxiv.org/html/1705.07057v4)

   MAF与IAF的依赖方向和计算差别。

   Primary paper; no copied figures
4. [Improved Variational Inference with Inverse Autoregressive Flow](https://arxiv.org/abs/1606.04934)

   已知潜变量时并行生成的IAF。

   Primary paper; no copied figures
5. [Neural Spline Flows](https://arxiv.org/html/1906.04032v2)

   有理二次样条、解析导数与二次方程逆解。

   Primary paper; independent numerical construction
6. [FFJORD](https://arxiv.org/abs/1810.01367)

   连续Flow、散度与迹估计。

   Primary paper; no copied figures
7. [Do Deep Generative Models Know What They Don’t Know?](https://arxiv.org/abs/1810.09136)

   密度与分布外检测的区别。

   Primary paper; own analytic Gaussian-shell illustration
