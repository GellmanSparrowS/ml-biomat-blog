# 从雪花到图像：扩散、Score与条件生成

Source: https://ml-biomat.com/tutorials/machine-learning/m34/
Language: zh-CN

跟随真实去噪轨迹，比较DDPM、DDIM和引导强度，再走进潜空间。

## 从电视雪花点里画出一枚圆环

如果把一幅圆环图逐渐掺入随机雪花，先会看不清边缘，随后连圆环是否存在也难以判断。现在反过来：给机器一整幅雪花，再告诉它“画一个圆环”，它能否一步步整理出合理的轮廓？这正是扩散生成的基本任务。它适合为同一个条件提出多种候选，例如插画草图、语音片段或机器人可能采用的动作序列。条件决定要往哪一类结果靠近，起始噪声和采样过程提供变化；同一句要求可以产生不同答案。

这里有一个很容易混淆的地方。给一张已知照片加噪后再恢复，是图像复原问题；从独立噪声开始生成，则是在学习过许多样本后提出一张新图。生成时没有一张藏在雪花后面的“唯一正确照片”。把这个区别放在心里，后面就能理解：训练时为什么可以知道加入的噪声，生成时为什么又要依靠模型估计，以及为什么多次采样会得到不同结果。

2015年，Sohl-Dickstein等人把逐步破坏数据、再学习逆过程的想法写成生成模型，借用了非平衡热力学中的过程视角。2020年的DDPM把逐步去噪与预测噪声的训练方式组织得尤其有效。理解这段历史，可以从一个实际困难出发：直接把整幅随机图变成清晰图，映射很复杂；如果把任务拆成许多小幅修正，并告诉模型当前噪声有多大，每次修正就有了明确的工作范围。本章先观察二维点的方向，再训练一个真正生成8×8圆环与十字图的模型。

![上排：一张测试十字逐步加噪。下排：从独立噪声生成圆环。两行并非同一张图的正反恢复；底层像素数组保留原值，显示灰度固定在\[−1,1\]，超出部分仅在显示时饱和。](https://ml-biomat.com/static/tutorials/machine-learning/figures/c59b29fce54b373787c50757.svg?v=c59b29fce54b)

图 1上排：一张测试十字逐步加噪。下排：从独立噪声生成圆环。两行并非同一张图的正反恢复；底层像素数组保留原值，显示灰度固定在[−1,1]，超出部分仅在显示时饱和。

## 怎样加噪，才知道每一时刻发生了什么

图像进入计算机后，可以摊平成一串数。本章每幅图有64个像素，用−1表示背景、1表示实心笔画，边缘经过平均后可以取中间值。一次加噪先把原来的数缩小一点，再加一份独立的标准高斯噪声。“标准”表示均值为0、方差为1；噪声的正负不偏向某个方向。缩小系数和噪声系数使用平方根，是因为独立随机量相加时方差相加，而乘上一个系数会把方差乘上该系数的平方。

$$
x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t,\quad \alpha_t=1-\beta_t,\quad \bar\alpha_t=\prod_{j=1}^{t}\alpha_j,\qquad x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/afd3e05d1c68845d6dd89d64.svg) | 干净样本、前一步与当前样本，均为d维向量；图像d=64，点云d=2。坐标均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c290ee14e71a69efaf1d339d.svg) | 噪声时间编号1至T、总步数64与乘积索引；不是实际秒数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/590d661f97b5749e1a61c517.svg) | 单步噪声方差比例、单步信号方差保留比例和累计保留比例；均无量纲，初值ᾱ₀=1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d1c9e542a3bf09d0034a4de3.svg) | 独立标准正态d维向量；前者为单步噪声，后者为等价累计噪声。两个表达描述相同边缘分布。 |

展开递推后，独立噪声的方差相加为1−ᾱ_t，因此可以一步合成给定时间的样本。手算取x₀=1、ᾱ_t=0.64、ε=−0.5，得到0.8×1+0.6×(−0.5)=0.5。已知这次ε时可反算x₀=(0.5+0.3)/0.8=1；生成时ε未知，需要网络估计。

单步保留比例与累计保留比例要分开理解。一次只损失少量信号，连续做许多次也会把信号几乎抹掉。累计比例是沿途各步保留比例的乘积；与之相对的部分给出总噪声方差。把每一步展开，旧噪声会继续被缩小，新噪声不断加入。它们彼此独立，合起来仍然是高斯量，因此可以直接从原图和时间编号算出某个噪声水平的样本，不必真的走完前面所有步骤。训练中这个捷径会节省大量计算。

代码采用64步余弦调度：开始时较多保留图像，随后逐步降低信号比例，并把最后单步噪声比例截在0.999。实际累计信号比例到第64步约为5.93×10^{−7}，起点因此可以用标准高斯近似。调度器决定各噪声水平的安排，采样器决定如何从一个水平移动到另一个水平；这两个选择相关，却承担不同工作。图中的前向一行来自一张测试十字的真实逐步加噪路径，反向一行则从另一份独立噪声生成圆环，两行展示的是两种过程。

## 让网络学习一个能检查的目标：加入了多少噪声

训练时我们自己生成噪声，所以有准确的答案。先随机取一幅训练图，再随机取时间编号，按累计公式合成带噪图；网络接收带噪图、时间和类别，输出64个预测噪声值。把预测值与实际加入的噪声逐像素比较，便得到均方误差。随机取时间，让同一个网络同时见到“几乎清楚”“轮廓模糊”和“接近纯噪声”的情况。时间输入尤其重要：同一个灰色像素，在轻噪声与重噪声状态下承载的证据不同。

$$
L(\theta)=\mathbb E_{x_0,c,t,\epsilon}\!\left[\frac1d\left\|\epsilon-\epsilon_\theta\!\left(\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,t,c\right)\right\|_2^2\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ebaa51d428d62bfd4786339f.svg) | 可训练网络参数、输出d个噪声分量的网络与平均噪声均方误差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d1eb7bc324e541f723ab8009.svg) | 训练样本、类别条件（含空条件）、均匀抽取的时间1…64、独立标准正态噪声。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d04bd1bd8af9b2288f302d50.svg) | 对上述随机量求平均、坐标数、逐分量平方和、累计信号保留比例；误差无量纲。 |

若二维噪声是(1,−1)，预测是(0.5,−0.5)，平方误差平均为(0.25+0.25)/2=0.25。批训练再对样本平均。平方损失的最佳预测是给定带噪样本、时间与条件后的噪声条件均值，因此网络不必猜中每一次可能的原图与噪声组合。

本例把时间变成16对正弦与余弦数，再与像素、三维类别编码拼接，交给两个128单元的隐藏层。三类编码分别表示圆环、十字和空条件，总计37,568个可训练参数。小图可以这样摊平计算；高分辨率图像更常使用能在多个尺度交换信息的网络。U-Net先缩小空间尺寸以汇集大范围结构，再逐层恢复分辨率，并通过跳跃连接取回边缘细节。大尺度可以判断物体占据哪里，小尺度则负责纹理与轮廓；时间信息在多个层中调节当前应该修正的内容。

预测噪声后，可以从带噪图中扣除它，得到原图估计。DDPM再把这一估计与当前状态组合成下一步的均值，按规定方差补入随机扰动。最后一步的方差为零，输出落到图像端。公式里的“原图估计”在重噪声阶段可能很不准：累计信号平方根很小，除法会放大误差。本例把估计限制在训练像素范围−1到1；这是实际采样算法的一部分，阅读结果时应把它与网络预测一起考虑。

$$
\hat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\,\hat\epsilon}{\sqrt{\bar\alpha_t}},\quad \tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,\qquad \mu_t=\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}\hat x_0+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t,\qquad x_{t-1}=\mu_t+\sqrt{\tilde\beta_t}\,\xi
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a1eec75ae8541f9a02f11387.svg) | 预测噪声、由它反算的干净图估计和当前状态，均为d维；代码对x̂₀截取到[−1,1]后代入均值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4be26bade2781b22846fb0c8.svg) | 反向高斯均值d向量、每坐标后验方差和独立标准正态d向量；最后一步无随机项。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b36d1cab37b8c12e9f8817e7.svg) | 前式定义的单步与累计比例，及当前时间；所有坐标与方差在本章均无量纲。 |

在已知真实x₀时，高斯条件分布可由前向两步联合分布配方求得上述均值和方差；采样把未知x₀替换为网络估计。t=1时ᾱ₀=1，后验方差为0，第二项系数为0，第一项系数为1，故直接输出x̂₀。若ᾱ_t=0.64、x_t=0.5、ε̂=−0.5，估计仍为1。

## 二维箭头告诉我们，去噪为什么指向数据

先把图像放在一边，设数据是平面上的两团点。给每个点加噪后，两团点逐渐变宽并互相重叠。现在站在平面某个位置，想知道向哪里走会让该噪声水平下的概率密度增大。对数密度对位置的梯度就回答这个问题，通常叫score。这里的“分数”是一个方向向量，二维数据对应两个分量；它不是给图片打出的单个质量分，也不是类别概率。

$$
s_t(x)=\nabla_x\log p_t(x)\approx-\frac{\epsilon_\theta(x,t)}{\sqrt{1-\bar\alpha_t}},\qquad \nabla_x\log\mathcal N(x;\mu,vI)=\frac{\mu-x}{v}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/265f560b7424dae7e9bb959e.svg) | 时间t的边缘密度、其d维score和对每个位置分量求偏导的梯度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f5a4dcd34fbea73d591b6a1f.svg) | 无条件网络噪声预测和累计信号保留比例；有条件网络对应条件密度的score。 |
| ![Formula](https://ml-biomat.com/static/agent-math/317b5d2f052f838279d9fe18.svg) | 高斯均值d向量、每坐标方差、d×d单位矩阵和位置。score量纲为坐标单位的倒数；本例无量纲。 |

高斯对数密度含−||x−μ||²/(2v)，求导得(μ−x)/v。已知x₀=1、ᾱ=0.64时，条件加噪均值0.8、方差0.36，在x=0.5的score是0.3/0.36=0.833333。这个数是给定该x₀的条件score；数据边缘score要平均所有可能原样本的条件score。噪声均方误差学到的条件均值正好实现这一平均。

对一团已知均值的高斯分布，箭头指向均值，离均值越远，恢复方向越强，方差越大，箭头越缓。对两团高斯混合，某个位置可能同时属于两团的尾部，因此正确方向是按两团在该位置的相对可能性加权，而非始终奔向最近的中心。图中的橙色箭头按这个已知分布直接计算，蓝色箭头由另一个6,530参数的小网络学习得来。模型在三个时间点上的网格均方根误差分别为1.643、0.154和0.057；低噪声时梯度更陡，固定网格又包含低密度尾部，比较误差时要结合箭头尺度与密度背景阅读。

![三种噪声水平的二维score场：橙色为解析混合高斯方向，蓝色为实际学习方向，灰色背景为真实加噪密度。显示9×9组箭头，RMSE使用完整17×17网格，所有面板采用同一箭头尺度与色标。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0d73db9e485c1f3623f36cf6.svg?v=0d73db9e485c)

图 2三种噪声水平的二维score场：橙色为解析混合高斯方向，蓝色为实际学习方向，灰色背景为真实加噪密度。显示9×9组箭头，RMSE使用完整17×17网格，所有面板采用同一箭头尺度与色标。

2019年的多噪声水平score学习，让“先在宽松、平滑的分布上找方向，再逐步收紧”成为清楚的建模路线。随后基于随机微分方程的表述，把离散去噪与连续时间联系起来。随机微分方程描述每一步同时包含确定移动和随机扰动；相应的概率流常微分方程只保留确定速度，却可在精确score条件下产生相同的一系列边缘分布。相同分布并不要求每一条粒子轨迹相同，这一点也解释了后面为何可以更换采样路线。

$$
dx=f(x,t)\,dt+g(t)\,dW_t,\qquad dx=[f(x,t)-g(t)^2s_t(x)]\,dt+g(t)\,d\bar W_t\quad(dt<0),\qquad \frac{dx}{dt}=f(x,t)-\tfrac12g(t)^2s_t(x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d3e56d32773c66fd5e2759a0.svg) | 连续状态、连续噪声时间、d维漂移和标量扩散幅度；f单位为坐标/时间，g为坐标/√时间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/12a030d7b0da4d1bbf359805.svg) | 前向及反向布朗增量，独立坐标方差分别为dt与\|dt\|；反向式从大t向小t积分。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bb9ea1db401c1b448204586d.svg) | 精确边缘score、扩散幅度的平方及概率流ODE速度；相同边缘分布结论需要正确score与相应初始分布。 |

第一式为前向SDE，第二式为反向SDE，第三式为共享边缘分布的确定性ODE。取标准正态平稳过程f=−x/2、g=1、s=−x：反向SDE漂移为+x/2，但dt为负；概率流速度则为0。每个粒子可以在ODE中静止，同时整个人群保持标准正态，说明分布相同不要求轨迹相同。

离散调度怎样靠近连续过程，可以用一个小时间步算出来。令时间间隔为0.01，单步噪声方差也为0.01，那么原信号乘数是√0.99≈0.994987，平均位移约为当前位置的−0.005013倍，噪声标准差为0.1。把平均位移除以时间间隔，就接近每单位时间−0.5倍位置的漂移；随机项的标准差则按时间间隔的平方根变化，对应公式中的布朗增量。逐步缩小时间间隔、同时匹配这些系数，才得到连续极限。有限的64步调度仍是一套离散规则，跨过多个水平的DDIM也需要按自身公式计算，不能仅凭都画着平滑轨迹就当成相同算法。

## 同一个模型，为什么可以走64步，也可以走16步

一次网络训练并没有规定生成时只能使用唯一的步数。DDIM从另一种保持训练边缘分布的过程构造出采样规则；当额外随机项设为零时，给定同一份起始噪声和条件，后续轨迹由模型确定。每一步先估计图像端，再按下一个噪声水平重新组合信号和残差。把时间表从64个水平缩成16个水平，就能减少网络调用，不过模型误差与数值跨步方式也会影响结果。

$$
\hat\epsilon_{\rm consistent}=\frac{x_t-\sqrt{\bar\alpha_t}\,\hat x_0}{\sqrt{1-\bar\alpha_t}},\qquad x_s=\sqrt{\bar\alpha_s}\,\hat x_0+\sqrt{1-\bar\alpha_s}\,\hat\epsilon_{\rm consistent},\qquad 0\le s<t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cae1ce632ae35c9c5529a926.svg) | 当前与下一选定时间编号，以及两时刻的d维状态；下一时间可跳过多个训练水平。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9fa7e35ea97ef40ec2c7748a.svg) | 截取后的原图估计，以及由当前状态与该估计重新计算的相容残差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3728c71b94ab6bc4fd00b2e9.svg) | 两个时间的累计信号比例；这是额外随机项η=0的DDIM更新，所有量无量纲。 |

若ᾱ_t=0.64、x_t=0.5、x̂₀=1，相容残差为−0.5。选下一个ᾱ_s=0.81，则x_s=0.9−0.5√0.19≈0.682055。终点s=0时ᾱ₀=1，直接得到x̂₀。较少步数减少网络调用，模型误差与跨步方式仍会改变输出。

本例的DDIM使用同一套训练权重、同一份64组起始噪声，对比64、16和8步。因为原图估计被截到像素范围，代码随后重新计算与该估计相容的残差，再进行组合；否则“估计图像加残差”已不等于当前状态。这个细节使公式、实现与画面对应起来。确定性只意味着相同输入可重复，不意味着任意少的步数都会产生同样的结果。

![每行固定显示最前12个生成样本，列之间交替请求圆环与十字；同列共享起始噪声。依次为DDPM64、DDIM64、DDIM16与DDIM8，均采用普通条件预测w=1。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f1fa337568cda4d40f2b5831.svg?v=f1fa337568cd)

图 3每行固定显示最前12个生成样本，列之间交替请求圆环与十字；同列共享起始噪声。依次为DDPM64、DDIM64、DDIM16与DDIM8，均采用普通条件预测w=1。

图中每一列使用相同起始噪声，行与行只改变采样方法或步数，并固定展示最前面的12幅结果。64步DDPM的轮廓较连贯；这个小模型的DDIM结果仍有缺口、杂点和形状偏差。独立形状分类器在64幅结果上的条件符合率分别为63/64、57/64、57/64和56/64。16步与64步DDIM在该指标上相同，画面却不逐像素相同。这样的对照可以帮助选择计算预算：先明确希望保留的性质，再测量减少步骤会损失哪些细节。

## 逐步查看真实生成的像素

每帧来自本章实际采样。更换算法仍使用同一组初始噪声；选择样本与像素，可以同时看到当前状态、当前估计的终点，以及最终输出。

[Figure: 生成过程的像素图、轨迹和固定样本组](https://ml-biomat.com/tutorials/machine-learning/m34/#M34-board)

红框标记所选像素；下方曲线保留原始数值，灰度图只把[−1,1]映射到白黑，范围外显示饱和。最下方八幅图展示该步骤全部保留样本，环与十字请求交替。动画初始暂停，可用键盘调整各项。

## 把“请画圆环”变成可调节的方向

条件生成需要把要求送入模型。本章用类别编码，文本模型则可以使用语句的向量表示。Classifier-free guidance的办法是在训练时偶尔把条件拿掉，让同一个网络既会回答“通常怎样去噪”，也会回答“已知要求时怎样去噪”。本例每个训练样本有15%的机会改用空条件。采样时分别计算这两个预测，它们的差提供条件带来的方向变化，再用一个系数调节变化幅度。

$$
\hat\epsilon_w=\epsilon_\theta(x_t,t,\varnothing)+w\,[\epsilon_\theta(x_t,t,c)-\epsilon_\theta(x_t,t,\varnothing)]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/79c9cb0224e7f17ab5f2c8e1.svg) | 带噪状态、时间、请求的类别或其他条件，以及空条件编码。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2475ae267775357fa1147f48.svg) | 同一网络的噪声预测、组合后的d维预测和无量纲引导系数；w=0无条件，w=1普通条件。 |

一个分量的无条件预测为0.2，条件预测为−0.1。w=3时组合为0.2+3(−0.1−0.2)=−0.7。这个线性外推可增强条件差异；其结果仍是噪声预测，需要再经采样更新形成图像。本例w>0实际调用网络两次，w=0只调用一次。

这里采用的系数约定是：0对应无条件预测，1对应普通条件预测，3把条件差放大三倍。不同文章或软件可能把“普通条件预测”记作零引导，因此阅读参数时应同时看公式。较强引导往往使结果更服从要求，也可能收窄同类样本的变化，或放大模型在某些位置的误差。这个权衡可以直接观察，不必把一个更大的数字自动理解为更好的生成。

![16步DDIM、相同起始噪声，依次使用引导系数0、1、3。偶数索引请求环，奇数索引请求十字；第一行无条件采样，因此请求不进入其计算。](https://ml-biomat.com/static/tutorials/machine-learning/figures/98e0dbf406e665362e0b963d.svg?v=98e0dbf406e6)

图 416步DDIM、相同起始噪声，依次使用引导系数0、1、3。偶数索引请求环，奇数索引请求十字；第一行无条件采样，因此请求不进入其计算。

在相同16步DDIM与相同噪声下，系数0、1、3得到的类别符合率为36/64、57/64和64/64，同类像素方差的均值依次约为0.1063、0.0985和0.0777。方差下降说明像素变化减少；噪点同样能抬高方差，所以它需要与样本图一起读。用于统计类别的逻辑回归只在生成完成后工作，既不参与去噪网络训练，也不向采样器提供梯度。这里的引导来自同一去噪器的两次预测，这也正是名称中“无分类器”的含义。

条件丢弃只改变网络接收到的信息，并不删掉训练图，也不把噪声标签改成零。一次128幅图的训练批，平均约19.2幅使用空条件；实际数目随随机抽样变化。这些图仍保留各自的圆环或十字结构，因此空条件分支学习两类数据混合后的去噪规律。普通条件分支则利用类别缩小可能答案的范围。两次预测差很小时，强引导的改动也小；差很大时，线性外推可能把预测推到训练中较少见的位置。另一种以条件预测为起点的约定，会把本章系数3写成额外引导系数2；比较实验参数时换算清楚，就能在相同更新上比较。

## 先压缩再生成：潜空间里反复去噪

一张512×512彩色图包含786,432个数，如果每一步都在这个尺寸上运行网络，计算代价很高。潜扩散先用图像编码器保存结构和外观信息，再在较小的潜张量上学习去噪，最后由解码器恢复图像。假设编码器输出64×64×4张量，元素数就降到16,384，是输入的1/48。这个比例描述所选张量形状，并不是文件压缩率；编码器的计算与信息损失也需要计入系统。

$$
z_0=E(x),\qquad z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon,\qquad \hat x=D(\hat z_0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0c30339c653b4a1e34212ca7.svg) | 输入图像、编码器与干净潜张量；示意形状为512×512×3到64×64×4。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86b07ee12f031d15e41b128c.svg) | 与潜张量同形状的带噪状态和标准高斯噪声，以及累计保留比例。 |
| ![Formula](https://ml-biomat.com/static/agent-math/faf0419082fed59255822f01.svg) | 采样所得潜变量、解码器与输出图像；潜变量按训练时约定缩放，无物理单位。 |

示意形状含512×512×3=786432个像素分量，潜张量含64×64×4=16384个数，数量减少48倍。编码器与解码器仍消耗计算，并决定保留哪些视觉信息。训练去噪网络前需要固定潜表示及其缩放约定；生成从潜噪声开始，重复更新后才解码。

2021年提出、2022年发表的潜扩散工作，把视觉压缩与扩散生成连接起来。它与VAE章节共享编码器和解码器的思想，但生成阶段在潜空间学习一个更灵活的分布。文本条件可通过交叉注意力进入去噪器：空间位置提供查询，文本向量提供键和值，让不同位置选择与自身相关的词语信息。时间条件回答“当前有多嘈杂”，文本条件回答“希望出现什么”，二者承担不同作用。

![文本条件进入潜空间去噪器，潜变量反复更新后通过图像解码器。](https://ml-biomat.com/static/tutorials/machine-learning/figures/3530f39960d397cb515c4c57.svg?v=3530f39960d3)

图 5潜扩散的条件、循环与解码位置。根据Polo Club of Data Science的Diffusion Explainer架构组件改编，MIT许可；原版权文本随图保留。重新绘制中英文标签并加入示意张量尺寸，本章实验使用像素空间。

图中最值得留意的是循环的位置：潜变量反复更新，图像解码通常在末端进行。本章实际训练的是像素空间的小网络，因而可以直接逐像素追踪每一步；潜扩散则把同样的过程放到了压缩表示中。若压缩阶段丢失细小文字或精确几何关系，后续生成需要面对这层表示限制。需要研究高分辨率生成时，可以分别评价压缩重建质量、潜空间生成质量和文本条件符合程度，找出误差在哪一段形成。

压缩质量可以先独立测量：拿一张未参与训练的图，只经过编码器和解码器，中间完全不做扩散，再比较输入与重建。如果细字已经变模糊，这部分误差属于表示与解码阶段。随后再让扩散生成潜变量，检查生成图是否增加了形状或纹理偏差。两个阶段的误差也未必简单相加，因为解码器是非线性的：某些潜坐标的小变化会明显移动边缘，另一些只改变柔和的色调。潜变量的缩放同样影响噪声水平；把潜值放大两倍却仍加入方差1的噪声，会提高信号相对强度，改变去噪器所见的任务。复用模型时，需要连同编码器、缩放因子和解码器一起保留这个约定。

## 把图、数字和完整程序放在同一个实验里

数据全部由几何规则生成：圆环的半径和位置变化，十字的角度、长度和笔画粗细变化。先在32×32网格画图，再按4×4区域平均成8×8图，保留灰度边缘。训练、验证、测试分别有3,072、512、512幅，使用独立随机种子，两个类别各占一半。模型训练5,000次更新，每批128幅；每250次在固定带噪验证样本上比较，最终选中第5,000次的权重。验证与测试噪声均方误差分别约为0.1746和0.1798。

评价生成图时，程序同时保存全部64幅输出、请求标签、每种设置的参数和前8幅图的完整轨迹。形状分类器在独立干净测试集上的正确率为100%，生成结果的符合率反映它识别出的形状。最近训练图的像素距离衡量相似程度，同类方差描述变化，网络调用次数表示主要采样工作量。类别正确的图仍可能有破损边缘，靠近训练图也可能只是几何规则限制了形状空间；把这些量与完整样本并排看，才能知道指标在回答哪个问题。

![左：固定验证噪声上的训练检查点误差。中：每种方法64幅图的类别符合率。右：同类像素方差，旁边标出实际去噪器调用次数；每次调用并行处理64幅图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/8688acc673c2179dde604619.svg?v=8688acc673c2)

图 6左：固定验证噪声上的训练检查点误差。中：每种方法64幅图的类别符合率。右：同类像素方差，旁边标出实际去噪器调用次数；每次调用并行处理64幅图。

完整程序先训练图像去噪器并生成六组结果，再训练二维score网络，输出权重、数组、轨迹和五幅科学图。训练时随机抽取单个噪声水平，生成时才沿时间表反复调用网络。阅读代码可以顺着这两条路线走：先找到带噪样本与噪声标签如何形成，再找到预测如何被采样器转成下一状态。更改步数、引导强度或数据几何后，保留同一组起始噪声，就能把新的变化与这里的结果逐列比较。

### 完整Python：噪声预测、六组采样与二维Score

运行python main.py --output results --language zh。使用NumPy、PyTorch、scikit-learn与Matplotlib；无需下载数据或模型。两组网络都真实训练，所有几何规则、权重、种子、输出与轨迹均保存在结果目录。

```
"""Learn diffusion scores on points, then train a conditional image denoiser.
Images are original antialiased ring/cross shapes generated by explicit geometry.
"""
from pathlib import Path
import argparse,json,math,copy,platform,time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.linear_model import LogisticRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
T=64;times=torch.arange(T+1,dtype=torch.float64);schedule=torch.cos((times/T+.008)/1.008*math.pi/2).square();schedule/=schedule[0].clone();beta=(1-schedule[1:]/schedule[:-1]).clamp(max=.999).float();alpha=1-beta;abar=torch.cat([torch.ones(1),torch.cumprod(alpha,0)])
class Denoiser(nn.Module):
 def __init__(self,dim,hidden,conditional):
  super().__init__();self.conditional=conditional;self.register_buffer('frequencies',torch.exp(-math.log(10000)*torch.arange(16)/16));self.net=nn.Sequential(nn.Linear(dim+32+(3 if conditional else 0),hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,dim))
 def forward(self,x,t,c=None):
  phase=t[:,None]*self.frequencies[None];parts=[x,phase.sin(),phase.cos()]
  if self.conditional:parts.append(F.one_hot(c,3).float())
  return self.net(torch.cat(parts,1))
def noised(x,t,eps):return abar[t,None].sqrt()*x+(1-abar[t,None]).sqrt()*eps
def glyphs(n,seed):
 rng=np.random.default_rng(seed);labels=np.arange(n)%2;rng.shuffle(labels);grid=(np.arange(32)+.5)/4-.5;xx,yy=np.meshgrid(grid,grid);result=[]
 for c in labels:
  dx=xx-(3.5+rng.uniform(-.45,.45));dy=yy-(3.5+rng.uniform(-.45,.45));width=rng.uniform(.45,.7)
  if c==0:ink=np.abs(np.sqrt(dx*dx+dy*dy)-rng.uniform(1.8,2.5))<width/2
  else:
   angle=rng.uniform(-.35,.35);u=dx*np.cos(angle)+dy*np.sin(angle);v=-dx*np.sin(angle)+dy*np.cos(angle);length=rng.uniform(2.2,2.8);ink=((np.abs(u)<width/2)&(np.abs(v)<length))|((np.abs(v)<width/2)&(np.abs(u)<length))
  result.append(ink.reshape(8,4,8,4).mean((1,3)).reshape(-1)*2-1)
 return np.array(result,dtype='float32'),labels
train,train_y=glyphs(3072,340);valid,valid_y=glyphs(512,341);test,test_y=glyphs(512,342);xt=torch.tensor(train);yt=torch.tensor(train_y)
torch.manual_seed(343);image_model=Denoiser(64,128,True);opt=torch.optim.Adam(image_model.parameters(),lr=.001);rng=torch.Generator().manual_seed(344);vrng=torch.Generator().manual_seed(345);vt=torch.randint(1,T+1,(len(valid),),generator=vrng);ve=torch.randn((len(valid),64),generator=vrng);vx=noised(torch.tensor(valid),vt,ve);history=[];best=float('inf');best_state=None;best_step=0;start=time.perf_counter()
for step in range(1,5001):
 idx=torch.randint(len(xt),(128,),generator=rng);t=torch.randint(1,T+1,(128,),generator=rng);eps=torch.randn((128,64),generator=rng);x=noised(xt[idx],t,eps);c=yt[idx].clone();c[torch.rand(128,generator=rng)<.15]=2;prediction=image_model(x,t,c);loss=F.mse_loss(prediction,eps);opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(image_model.parameters(),1);opt.step()
 if step%250==0:
  with torch.no_grad():vl=F.mse_loss(image_model(vx,vt,torch.tensor(valid_y)),ve).item()
  history.append([step,loss.item(),vl])
  if vl<best:best=vl;best_step=step;best_state=copy.deepcopy(image_model.state_dict())
image_model.load_state_dict(best_state);image_model.eval();training_seconds=time.perf_counter()-start;torch.save(dict(model=image_model.state_dict(),beta=beta,best_step=best_step),out/'image-denoiser.pt')
te=torch.randn((len(test),64),generator=vrng);tt=torch.randint(1,T+1,(len(test),),generator=vrng)
with torch.no_grad():test_mse=F.mse_loss(image_model(noised(torch.tensor(test),tt,te),tt,torch.tensor(test_y)),te).item()
# A classifier measures one aspect of shape fidelity, separately from denoiser training.
classifier=LogisticRegression(C=1,max_iter=1000).fit(train,train_y);classifier_test=float((classifier.predict(test)==test_y).mean())
sample_rng=torch.Generator().manual_seed(346);initial=torch.randn((64,64),generator=sample_rng);requests=torch.arange(64)%2
@torch.no_grad()
def guided(x,t,c,weight):
 null=torch.full_like(c,2);unconditional=image_model(x,t,null)
 if weight==0:return unconditional
 conditional=image_model(x,t,c);return unconditional+weight*(conditional-unconditional)
@torch.no_grad()
def generate(method='ddpm',steps=64,weight=1.,seed=347):
 x=initial.clone();rng=torch.Generator().manual_seed(seed);path=[dict(t=T,x=x[:8].numpy().tolist())];predicted=[]
 levels=list(range(T,0,-1)) if method=='ddpm' else np.linspace(T,1,steps,dtype=int).tolist()
 for i,level in enumerate(levels):
  t=torch.full((len(x),),level,dtype=torch.long);noise=guided(x,t,requests,weight);x0=((x-(1-abar[level]).sqrt()*noise)/abar[level].sqrt()).clamp(-1,1)
  predicted.append(dict(t=level,x0=x0[:8].numpy().tolist()))
  if method=='ddpm':
   prev=level-1;variance=beta[level-1]*(1-abar[prev])/(1-abar[level]);mean=abar[prev].sqrt()*beta[level-1]/(1-abar[level])*x0+alpha[level-1].sqrt()*(1-abar[prev])/(1-abar[level])*x;x=mean+(variance.sqrt()*torch.randn(x.shape,generator=rng) if prev>0 else 0)
  else:
   prev=levels[i+1] if i+1<len(levels) else 0
   # Recompute residual noise after clipping x0, keeping the decomposition consistent.
   noise=(x-abar[level].sqrt()*x0)/(1-abar[level]).sqrt();x=abar[prev].sqrt()*x0+(1-abar[prev]).sqrt()*noise
  path.append(dict(t=int(prev),x=x[:8].numpy().tolist()))
 return x.numpy(),path,predicted
settings=[('DDPM64',dict(method='ddpm',steps=64,weight=1)),('DDIM64',dict(method='ddim',steps=64,weight=1)),('DDIM16',dict(method='ddim',steps=16,weight=1)),('DDIM8',dict(method='ddim',steps=8,weight=1)),('CFG0',dict(method='ddim',steps=16,weight=0)),('CFG3',dict(method='ddim',steps=16,weight=3))]
outputs={};metrics={};replays={};requests_np=requests.numpy()
for name,setting in settings:
 started=time.perf_counter();generated,path,predicted=generate(**setting);seconds=time.perf_counter()-started;outputs[name]=generated;replays[name]=dict(settings=setting,path=path,predicted=predicted)
 prediction=classifier.predict(generated);distance=((generated[:,None]-train[None])**2).mean(2).min(1)
 metrics[name]=dict(condition_match=float((prediction==requests_np).mean()),predicted_ring_fraction=float((prediction==0).mean()),nearest_training_mse=float(distance.mean()),mean_pixel_variance=float(np.mean([np.var(generated[requests_np==c],axis=0).mean() for c in [0,1]])),denoiser_calls=setting['steps']*(1 if setting['weight']==0 else 2),seconds=seconds)
# A genuine forward Markov path, distinct from the direct marginal sampling used in training.
forward_rng=torch.Generator().manual_seed(348);forward=[torch.tensor(test[0])];current=forward[0]
for t in range(1,T+1):current=alpha[t-1].sqrt()*current+beta[t-1].sqrt()*torch.randn(64,generator=forward_rng);forward.append(current)
forward=torch.stack(forward).numpy()
# Learn the same epsilon objective for a two-Gaussian point mixture.
r=np.random.default_rng(349);point_labels=r.integers(0,2,4096);point_centers=np.array([[-1.,0.],[1.,0.]],dtype='float32');point_data=(point_centers[point_labels]+r.normal(0,.25,(4096,2))).astype('float32');point_tensor=torch.tensor(point_data)
torch.manual_seed(350);point_model=Denoiser(2,64,False);po=torch.optim.Adam(point_model.parameters(),lr=.002);prng=torch.Generator().manual_seed(351)
for step in range(2000):
 idx=torch.randint(4096,(256,),generator=prng);t=torch.randint(1,T+1,(256,),generator=prng);eps=torch.randn((256,2),generator=prng);loss=F.mse_loss(point_model(noised(point_tensor[idx],t,eps),t),eps);po.zero_grad();loss.backward();po.step()
torch.save(dict(model=point_model.state_dict(),beta=beta),out/'point-denoiser.pt')
axis=np.linspace(-2.5,2.5,17);gx,gy=np.meshgrid(axis,axis);grid=np.c_[gx.ravel(),gy.ravel()].astype('float32');fields=[]
for t in [8,32,56]:
 b=abar[t].item();means=point_centers*math.sqrt(b);variance=b*.25**2+(1-b);diff=means[None]-grid[:,None];lp=-np.sum(diff**2,axis=2)/(2*variance);prob=np.exp(lp-lp.max(1,keepdims=True));prob/=prob.sum(1,keepdims=True);truth=(prob[:,:,None]*diff).sum(1)/variance
 with torch.no_grad():learned=(-point_model(torch.tensor(grid),torch.full((len(grid),),t))/(1-abar[t]).sqrt()).numpy()
 fields.append(dict(t=t,score=learned.tolist(),truth=truth.tolist(),density=(np.exp(lp).mean(1)/(2*math.pi*variance)).tolist(),rmse=float(np.sqrt(np.mean((learned-truth)**2))),variance=variance))
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=3072,validation=512,test=512,image_shape=[8,8],classes=['ring','cross'],seeds=[340,341,342]),training=dict(steps=5000,best_step=best_step,parameters=sum(p.numel() for p in image_model.parameters()),batch=128,lr=.001,condition_dropout=.15,validation_noise_mse=best,test_noise_mse=test_mse,seconds=training_seconds),schedule=dict(T=T,alpha_bar_T=abar[-1].item(),beta_first=beta[0].item(),beta_last=beta[-1].item()),classifier=dict(test_accuracy=classifier_test,role='post-hoc shape-class evaluation; never used to guide generation'),generation=metrics,point_score=dict(parameters=sum(p.numel() for p in point_model.parameters()),steps=2000,grid_rmse={str(f['t']):f['rmse'] for f in fields}),hand=dict(noised_scalar=math.sqrt(.64)*1+math.sqrt(.36)*(-.5),recovered_scalar=(.5-math.sqrt(.36)*(-.5))/math.sqrt(.64),conditional_gaussian_score=-(-.5)/math.sqrt(.36),guidance_unconditional=.2,guidance_conditional=-.1,guidance_weight3=.2+3*(-.1-.2)))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'replay.json').write_text(json.dumps(dict(forward=forward.tolist(),forward_class=int(test_y[0]),alpha_bar=abar.tolist(),models=replays,requested_classes=requests_np[:8].tolist()),separators=(',',':')),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train=train,train_labels=train_y,validation=valid,validation_labels=valid_y,test=test,test_labels=test_y,initial_noise=initial.numpy(),requested_classes=requests_np,beta=beta.numpy(),alpha_bar=abar.numpy(),history=history,forward_path=forward,point_train=point_data,point_grid=grid,point_scores=np.array([f['score'] for f in fields]),point_truth=np.array([f['truth'] for f in fields]),**{name:values for name,values in outputs.items()})
def image_axis(ax,img):ax.imshow((np.array(img).reshape(8,8)+1)/2,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
fig,axs=plt.subplots(2,7,figsize=(13,4.8),layout='constrained');levels=[0,8,16,32,48,56,64]
for j,t in enumerate(levels):image_axis(axs[0,j],forward[t]);axs[0,j].set_title(f't={t}')
path=replays['DDPM64']['path'];levels_reverse=[64,56,48,32,16,8,0]
for j,t in enumerate(levels_reverse):image_axis(axs[1,j],next(f for f in path if f['t']==t)['x'][0]);axs[1,j].set_title(f't={t}')
axs[0,0].set_ylabel(tr('十字：前向加噪','Corruption (cross)'),fontsize=11);axs[1,0].set_ylabel(tr('圆环：独立生成','Generation (ring)'),fontsize=11);save(fig,'noise-path')
fig,axs=plt.subplots(4,12,figsize=(13,5.8),layout='constrained')
for row,name in enumerate(['DDPM64','DDIM64','DDIM16','DDIM8']):
 for col in range(12):
  image_axis(axs[row,col],outputs[name][col])
  if row==0:axs[row,col].set_title(tr('环','Ring') if col%2==0 else tr('十字','Cross'),fontsize=9)
 axs[row,0].set_ylabel(name,fontsize=11)
save(fig,'samplers')
fig,axs=plt.subplots(3,12,figsize=(13,4.8),layout='constrained')
for row,name in enumerate(['CFG0','DDIM16','CFG3']):
 for col in range(12):image_axis(axs[row,col],outputs[name][col])
 axs[row,0].set_ylabel(['w=0','w=1','w=3'][row],fontsize=12)
save(fig,'guidance')
fig,axs=plt.subplots(1,3,figsize=(13,4.2),layout='constrained');arrow_ids=np.arange(len(grid)).reshape(17,17)[::2,::2].ravel();maximum=max(max(f['density']) for f in fields)
for ax,f in zip(axs,fields):
 truth=np.array(f['truth']);score=np.array(f['score']);im=ax.contourf(gx,gy,np.array(f['density']).reshape(17,17),levels=np.linspace(0,maximum,15),cmap='Greys',alpha=.25);ax.quiver(grid[arrow_ids,0],grid[arrow_ids,1],truth[arrow_ids,0],truth[arrow_ids,1],color='#c18a57',angles='xy',scale_units='xy',scale=15,width=.004);ax.quiver(grid[arrow_ids,0],grid[arrow_ids,1],score[arrow_ids,0],score[arrow_ids,1],color='#125f82',angles='xy',scale_units='xy',scale=15,width=.003);ax.set(xlabel='x1',ylabel='x2',title=f"t={f['t']}; RMSE={f['rmse']:.3f}",xlim=(-2.7,2.7),ylim=(-2.7,2.7));ax.set_aspect('equal')
fig.colorbar(im,ax=axs,label=tr('加噪后的目标密度','Noisy target density'),fraction=.022,pad=.02)
save(fig,'score')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,2],color='#125f82');axs[0].set(xlabel=tr('参数更新数','Parameter updates'),ylabel=tr('固定验证噪声MSE','Fixed validation noise MSE'),title=tr('A  噪声预测学习','A  Learning noise prediction'))
names=list(metrics);pos=np.arange(len(names));axs[1].bar(pos,[metrics[n]['condition_match'] for n in names],color='#125f82');axs[1].set_xticks(pos,names,rotation=35,ha='right');axs[1].set(ylim=(0,1.06),ylabel=tr('后验分类器与请求一致率','Post-hoc classifier / request agreement'),title=tr('B  每设置64张图','B  64 images per setting'))
axs[2].scatter([metrics[n]['denoiser_calls'] for n in names],[metrics[n]['mean_pixel_variance'] for n in names],c=['#125f82']*4+['#bf7139','#648454'],s=45)
for n in names:axs[2].annotate(n,(metrics[n]['denoiser_calls'],metrics[n]['mean_pixel_variance']),xytext=(3,4),textcoords='offset points',fontsize=8)
axs[2].set(xlabel=tr('每批采样去噪器调用次数','Denoiser calls per sampling batch'),ylabel=tr('按请求分组的平均像素方差','Mean pixel variance within request groups'),title=tr('C  计算量与输出变化','C  Computation and output variation'));save(fig,'metrics')
print(json.dumps(summary,indent=2))
```

## 从图像走向声音与动作，评价也要随对象改变

图像之外，扩散也可以处理一段音频的波形、频谱或压缩表示。相邻采样点之间的相位与时间结构决定声音是否连贯，因此除了频谱外观，还应听取结果，检查时长、噪声、语言内容或条件符合程度。对一段机器人的轨迹，每个时间位置可包含多个关节角或空间坐标；去噪网络一次预测整段序列的修正，能够表达多种绕障路线。此时要把关节范围、速度、碰撞和终点误差纳入评价，画面平滑只回答了其中一部分问题。

三个对象有共同的计算结构：明确表示的数据维度，给定噪声过程，学习与时间有关的预测，再用采样器产生候选。它们也有各自的尺度。像素在本章被归一化为无量纲数，音频可能使用归一化振幅，轨迹中的位置、角度和时间则需要一致的单位与标准化约定。不同量直接混在同一个均方误差里，会让数值较大的量占据更高权重；合理的表示与损失设计应让真正重要的偏差被看见。

选择模型时，可以把问题收敛到三个可操作的判断：训练目标是否与希望修正的量一致，采样预算是否足以得到合格候选，评价是否覆盖条件与多样性。本章的圆环与十字让每一次预测都能展开成64个数；二维score又把同一思想变成可见的方向场。沿着这两种视角继续读图像、语音或动作生成论文，时间条件、噪声调度、引导和采样器就都有了可以计算的含义。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M34.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585)

   逐步破坏数据与学习逆过程的2015年工作。

   Primary paper; no copied figures
2. [Denoising Diffusion Probabilistic Models](https://arxiv.org/html/2006.11239v2)

   前向边缘、噪声目标与反向高斯采样。

   Primary paper; independent experiment
3. [Denoising Diffusion Implicit Models](https://arxiv.org/html/2010.02502v4)

   保持边缘的过程族、确定性采样与减少步数。

   Primary paper; independent experiment
4. [Generative Modeling by Estimating Gradients of the Data Distribution](https://arxiv.org/abs/1907.05600)

   2019年多噪声水平score学习。

   Primary paper; own analytic mixture figure
5. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/html/2011.13456v2)

   反向SDE、概率流ODE与时间方向。

   Primary paper; no copied figures
6. [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)

   联合有/无条件训练与引导系数约定。

   Primary paper; independent experiment
7. [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752)

   潜编码、感知压缩与交叉注意力。

   Primary paper; no copied figures
8. [Diffusion Explainer](https://poloclub.github.io/diffusion-explainer/)

   条件、潜去噪循环与图像解码的架构组件。

   MIT, Copyright 2022 Polo Club of Data Science; adapted diagram; license retained
