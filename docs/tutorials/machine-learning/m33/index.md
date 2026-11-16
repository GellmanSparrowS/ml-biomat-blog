# 从压缩一张图到生成新图：AE与VAE

Source: https://ml-biomat.com/tutorials/machine-learning/m33/
Language: zh-CN

用同一批手写图，看懂瓶颈、去噪、重参数化与ELBO，再亲手走进训练出的潜空间。

## 把一幅画装进小纸条，再从纸条把它画回来

假设你只能给朋友传一张很小的纸条，却想让他重画一幅图。逐像素抄写太占地方，于是你可能写下“一个偏窄的圆环，上方缺一小口”。朋友需要理解这些描述，才能把图还原出来。自编码器把这样的合作变成两个一起训练的网络：编码器把图像压进较短的向量，解码器再从向量重建图像。这里没有人预先规定纸条上该写“圆环”还是“缺口”，网络通过重建误差自己形成一种通信方式。我们关心的是，这份短描述保留了哪些结构，又省略了哪些细节。

这个问题可以连接图像压缩、去噪、相似样本检索和表示学习。例如旧照片有零散噪点时，我们希望重建常见的笔画与轮廓，把偶然的污点舍弃；整理大量图像时，我们也希望用较短的表示比较它们。不过，能把见过的图像写成纸条，再画回来，并没有自动回答另一个问题：如果随手编一张纸条，能否画出合理的新图像？变分自编码器VAE把“纸条应当怎样分布”也纳入模型，从而连接表示、概率推断与生成。

自编码器沿用了神经网络通过误差学习内部表示的思路。Kingma与Welling在2013年提出的Auto-Encoding Variational Bayes，把神经网络作为近似推断器，配合可微的随机采样方法训练潜变量模型。它的关键变化不只是“增加噪声”，而是让编码器输出一个分布，并让这个分布参与明确的概率目标。先看公开教程中的容量曲线：潜向量维度改变时，重建误差随之变化。然后用同一批手写数字，把容量、去噪、分布和采样逐项拆开。

![原教程中CIFAR10自编码器的潜维度与重建误差曲线，展示容量变化；误差采用原教程定义，数值不与本章每像素MSE直接混比。Phillip Lippe，UvA Deep Learning Tutorials，Tutorial 9，代码单元\[11\]，MIT，未改动。这是AE实验。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5d80d19605c1eea7717ca3e7.svg?v=5d80d19605c1)

图 1原教程中CIFAR10自编码器的潜维度与重建误差曲线，展示容量变化；误差采用原教程定义，数值不与本章每像素MSE直接混比。Phillip Lippe，UvA Deep Learning Tutorials，Tutorial 9，代码单元[11]，MIT，未改动。这是AE实验。

## 瓶颈为什么能学到结构

本章图像有8×8个像素，把它摊开后就是64维输入。编码器先经过64个隐藏单元，再缩成2维或8维潜向量；解码器则从潜向量经过64个隐藏单元，输出64个重建强度。两端都由数据调整参数，中间的短向量构成瓶颈。若所有像素相互独立，压缩会损失许多信息；手写数字却有重复的背景、连续笔画和常见组合，因此较少坐标能够描述其中一部分规律。瓶颈迫使模型利用这些共同结构，而不是给每个像素保留一个独立的通道。

$$
z=f_\phi(x),\quad \widehat x=g_\theta(z),\qquad L_{\mathrm{AE}}=\frac1{ND}\sum_{i=1}^N\sum_{j=1}^D(\widehat x_{ij}-x_{ij})^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/388c1172af1c00ded90619da.svg) | 单张输入与重建，D=64个归一化像素，强度无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0fd0aa86c9a7c3e4aeec2bd1.svg) | d维潜向量、带参数φ的编码器、带参数θ的解码器；本例d=2或8。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b2819cff441cb2ca0dd46db7.svg) | 平均的图像数、每图像素数、图像索引与像素索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/630f78f925061226dc19efb8.svg) | 每图每像素平均平方误差，单位为归一化强度平方。 |

一个两像素输入(0.2,0.8)重建成(0.3,0.6)，平方误差为0.01与0.04，平均0.025。对本章图像需要累加64项，再对图像平均。编码器与解码器一起接收损失梯度；去噪时把f的输入替换成受扰动图像，公式里的目标x仍是干净图。

重建损失把“画得像”变成可优化的数字。逐像素平方误差会对大的强度偏差施加更大惩罚，而且能够直接反向传播。本例2维自编码器在测试集上的每像素均方误差为0.03650，8维时降为0.01451。接触表中，更多维度通常能保留更明确的笔画。可是较低像素误差和人眼判断并不完全一致：一条清晰笔画轻微平移，可能比一条位置正确但模糊的笔画得到更大误差。选择损失函数，实际上也在选择哪些差异值得模型认真处理。

从64个数变成2个数，是表示维度的压缩；要做真正的文件压缩，还要规定每个数用多少比特、如何量化、是否传输解码器以及怎样编码剩余误差。一个32位浮点数的存储成本不同于一个小整数，解码网络也占空间。因此本章把“维度更少”与“文件更小”分开计算。对比线性方法也有帮助：在线性编码器、线性解码器和平方损失等条件下，自编码器与主成分子空间密切相关；加入非线性后，它可以把弯曲的数据结构展开，但潜坐标不再天然具有唯一方向或可读名称。

![每列是同一张测试图，上到下为原图、2维AE、8维AE、β=1 VAE的均值编码重建、含噪输入、8维去噪AE。所有图统一显示0–1强度。数据：E. Alpaydin、C. Kaynak，UCI手写数字，CC BY 4.0；重建均为实际模型输出。](https://ml-biomat.com/static/tutorials/machine-learning/figures/4914f770856e8732fd10f87b.svg?v=4914f770856e)

图 2每列是同一张测试图，上到下为原图、2维AE、8维AE、β=1 VAE的均值编码重建、含噪输入、8维去噪AE。所有图统一显示0–1强度。数据：E. Alpaydin、C. Kaynak，UCI手写数字，CC BY 4.0；重建均为实际模型输出。

## 去噪时，为什么输入和答案不一样

普通自编码器把输入本身作为重建目标；去噪自编码器则把被扰动的图像作为输入，把原来的干净图作为答案。训练时我们知道噪声是怎样加进去的，所以不需要给每个像素重新人工标注。模型必须根据残留结构猜回被破坏的内容：一条连续笔画中间少了一个亮点，可以借助周围位置恢复；完全孤立的噪点则未必属于真实笔画。这样的目标把“压缩后重画”变成“从不完整的观察恢复规律”，也解释了为什么输入噪声的类型需要符合实际问题。

实验给像素加上标准差0.25的高斯噪声，再截到0–1范围。普通8维自编码器读取含噪测试图时，重建相对干净图的均方误差为0.03672；用相同8维瓶颈训练的去噪模型降到0.02164。读取干净图时，普通模型的误差为0.01451，去噪模型为0.01632。它们各自适应了不同输入条件：去噪训练更愿意把偏离常见结构的细节拉回去，这对噪声有帮助，却可能略去一部分真实的小差异。

这也给异常检测一个具体的思考入口。若只用正常样本训练，某些异常可能难以重建，产生较大误差；但一个容量很强的模型也可能把异常重建得很好，普通样本中罕见的写法则可能误差很大。实际设计应先说明“异常”指哪种变化，再用对应异常和正常样本设定评价。重建误差提供的是模型对某类结构的适应程度，不能直接把最高误差的图都叫作错误数据。去噪、压缩和异常发现使用了相近的组件，却依赖不同的训练输入、目标和判定方式。

## VAE的短纸条是一团可能性

普通自编码器为一张图输出一个确定的坐标。VAE的编码器输出均值和方差，描述这张图可能对应哪些潜坐标。想象纸条不再写“位置恰好在这里”，而是圈出一小片区域；解码器要在这片区域内都能生成与输入相容的内容。均值决定区域中心，标准差决定各方向的宽度。我们采用两个潜坐标、对角高斯分布，因此每张图需要两个均值和两个对数方差。对角假设让条件分布的两个坐标独立，便于计算；不同输入的均值集合仍然可以形成复杂、相关的整体分布。

$$
q_\phi(z\mid x)=\mathcal N(\mu_\phi(x),\operatorname{diag}(e^{\ell_\phi(x)})),\quad p(z)=\mathcal N(0,I),\quad p_\theta(x\mid z)=\mathcal N(g_\theta(z),\sigma_x^2 I)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6b767d33fc65203af063da4c.svg) | 近似后验、潜变量先验、图像观察分布；概率密度随变量单位而改变。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3045d5c77821c1da3694cbe4.svg) | 每张图输出的均值与对数方差向量；d=2，潜坐标无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0363af670b35ceb835b1520.svg) | 多元高斯分布、把向量放在对角线的操作、对应维度的单位矩阵；先验I为d×d，观察分布I为D×D。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f7d87e6f03dbedd326be8ece.svg) | 解码器输出的D=64个条件均值、观察噪声标准差，本例σ_x=0.25。 |

若某潜坐标μ=0.5、ℓ=ln0.25，则方差0.25、标准差0.5；图像像素的观察方差却是0.25²=0.0625。两种方差属于不同空间：编码方差由输入决定，观察方差在本例固定。先验给生成过程提供起点；q利用已经看到的图像近似反向推断。

生成模型还指定一个先验：在没有看到任何图像之前，潜坐标从标准正态分布抽取。然后解码器给出图像的条件分布。本章用固定标准差0.25的高斯观察模型，网络输出64个像素的条件均值。编码器近似回答“看到这张图之后，哪些潜坐标比较可能”，解码器回答“给定潜坐标，图像怎样分布”。这两个方向分别对应推断与生成。编码器的输出分布记作q，是因为它在近似真实后验p；我们可以很快计算q，却通常不能精确求出后验所需的积分。

图中展示的是解码分布的均值图像。完整的观察模型还会在每个均值周围加入标准差0.25的像素噪声；这种高斯分布允许强度超出0–1，显示时若截断，就改变了显示值的分布。因此这里用均值图册观察学到的笔画结构，并在概率计算中保持原来的高斯定义。对真正的二值图可以使用伯努利观察分布，对连续颜色也可以选择更合适的分布族。网络输出看起来是一张图，背后究竟表示样本、均值还是概率参数，需要始终说清楚。

## 随机抽样怎样接上梯度

训练时需要从编码分布抽一个潜向量，再送进解码器。但“让随机数发生器按新的均值和方差抽样”这个描述，没有直接给出样本如何随网络参数变化的计算路径。重参数化把随机性搬到一个固定标准分布里：先抽标准正态噪声，再用编码器输出的均值和标准差对它平移、缩放。对这一条已经抽到的噪声，后续运算都是普通的可微计算。这样既保留抽样的分布，也让梯度能沿着明确的算术关系回到编码器。

$$
\epsilon\sim\mathcal N(0,I),\quad z=\mu+e^{\ell/2}\odot\epsilon,\qquad \frac{\partial z_j}{\partial\mu_j}=1,\quad \frac{\partial z_j}{\partial\ell_j}=\frac12e^{\ell_j/2}\epsilon_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bc4dcdd816066dd3105937e5.svg) | 标准正态噪声、编码均值、对数方差、采样潜向量，形状相同，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a13c037afb4db6c1b0350d96.svg) | 逐坐标相乘与潜坐标索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/006e9cdbaf8f19396a4bac5d.svg) | 保持本次噪声固定时的局部偏导，其他坐标互不直接影响。 |

μ=0.5、ℓ=ln0.25、ε=−0.4，得到z=0.5+0.5×(−0.4)=0.3；对μ导数为1，对ℓ导数为0.5×0.5×(−0.4)=−0.1。代码用float64独立核对。随机性来自ε，网络参数控制的是可微的平移与缩放，因此导数能继续传回编码器。

例如均值0.5、标准差0.5，抽到噪声−0.4，就得到潜坐标0.3。保持这次噪声不变，均值增加0.01，坐标也增加0.01；标准差增加0.01，坐标减少0.004。代码让网络输出对数方差，指数变换保证方差为正，也把原本受正数约束的量变成可以自由取值的网络输出。此时坐标对对数方差的导数为−0.1。这个导数由手算得到，再用自动微分核对，能够看见“随机节点后面仍然能求梯度”具体是什么意思。

每次抽样得到的梯度带有随机波动，训练通过不同批次和不同噪声平均这些信息。这里每张训练图每次使用一个潜样本，验证时为每张图使用固定的8组噪声，减少选模型时由抽样带来的额外波动；测试统计使用32组独立噪声，报告采样重建误差。另一个常见展示方式是直接把均值送进解码器，这能得到稳定的重建图，但它不是对整个编码分布的期望重建。非线性解码器下，“先平均再解码”和“先解码再平均”一般不同。

## 重建与KL：为什么目标里需要两笔账

如果只要求重建准确，编码器可以把不同图像放到很远、很窄的小区域里，解码器各自记住这些区域的内容。从先验随机抽点时，却可能落在没有学好的空隙。VAE的训练目标因此同时处理两件事：由编码分布抽到的潜变量，应当能解释输入；这个编码分布也要与指定先验保持联系。后一项用KL散度衡量。它比较的是概率分布，不是简单比较两组均值：均值相同但宽度不同的两个高斯分布，也会产生正的KL。

$$
D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))=\frac12\sum_{j=1}^d\left(\mu_j^2+e^{\ell_j}-1-\ell_j\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d030412d4e039867037a4f93.svg) | 从q到p的KL散度，非负，使用自然对数时单位nats；方向不可随意互换。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f45e9410864d7d0b4efbf507.svg) | 第j维编码均值、对数方差与方差；潜坐标无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/002d92ae8202f23d5abc8977.svg) | 潜维度、求和索引与标准正态先验；公式依赖对角高斯q和此先验。 |

一维μ=0.5、方差0.25时，KL=0.5×(0.25+0.25−1−ln0.25)≈0.443147。当μ=0、方差1时每项为0。这个解析式把高斯密度比的对数对q取期望后得到，平方项的期望同时包含均值平方和方差，因此不能只惩罚均值偏离零。

两项相加并不是随意拼接的损失。把联合分布分成先验与条件分布，再引入编码分布，可以把对数证据拆成一个可优化的下界和一个非负的后验差距。这个下界叫ELBO。提高ELBO会同时考虑解释图像的能力与推断分布的代价；真实后验越接近编码分布，下界与对数证据之间的距离越小。这里的“变分”指用一族可计算的分布去近似难求的后验，而不是说模型只是对普通自编码器做了一点随机修改。

$$
\log p_\theta(x)=\mathcal L(x)+D_{\mathrm{KL}}(q_\phi(z\mid x)\|p_\theta(z\mid x)),\quad \mathcal L(x)=\mathbb E_q[\log p_\theta(x\mid z)]-D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e74e6aa040ce200228f3796.svg) | 图像的边缘概率密度与真实潜变量后验；前者由潜变量积分获得。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7ab77ec4103bb054ed229d53.svg) | 单图ELBO及按编码分布q对潜变量取期望。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78b2e3cdb94abade6dd35efa.svg) | KL散度、自然对数、生成模型参数与编码器参数；本式各对数项以nats计。 |

把log p(x,z)减去log q(z|x)，对q取期望，再用p(x,z)=p(z|x)p(x)，就得到第一项恒等分解；再用p(x,z)=p(x|z)p(z)，得到第二式。后验KL非负，所以ELBO不超过log证据。若log p(x)=−10、后验KL=0.4，则ELBO=−10.4。这个后验差距不同于训练中可直接计算的q到先验KL。

在固定方差的高斯观察模型下，负对数似然由平方误差加常数组成，因而能够精确说明重建项为什么长成现在的样子。代码把64个像素的平方误差先求和，再除以观察方差的两倍，最后加上每张图的KL。训练时可以省去与参数无关的高斯常数；报告负ELBO时再把常数放回。由于连续概率密度可以大于1，负对数密度可以为负，所以本例β=1的测试负ELBO约−5.780 nats/图并不矛盾。它仍然是同一个明确观察模型下的变分量，不能与换了强度单位或观察分布的数字直接混比。

$$
-\log p_\theta(x\mid z)=\frac{\|x-g_\theta(z)\|^2}{2\sigma_x^2}+\frac D2\log(2\pi\sigma_x^2)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e0f43653f7f49b1558e89534.svg) | 观察图像与解码均值，D=64个无量纲像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2900fc90c210213243c6ecbf.svg) | 固定观察标准差和像素总数；不是潜变量标准差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/35d95492a0d8700f5a67bf76.svg) | 64个像素残差平方之和、圆周率、自然对数。 |

若每像素MSE为0.04，平方误差总和64×0.04=2.56，除以2×0.25²得到20.48。高斯常数约−29.91077 nats，所以条件负对数密度约−9.43077 nats。对编码采样求平均并加上KL，才得到负ELBO；显示均值重建的MSE不能直接代替这项采样期望。

## 调信息容量，也给生成过程一个条件

β-VAE把KL项乘以一个权重，以便研究表示的信息约束和重建之间的取舍。本例β从0.2增到1再到4时，平均KL从6.433降到3.763、1.857 nats/图；采样重建均方误差从0.03727升到0.03978、0.04818。图上横轴对应编码分布偏离先验的程度，纵轴对应失去的像素精度，两者来自同一次实际训练。β=1对应前面推导的标准ELBO；改变β后得到的是加权目标，不能把不同β的训练损失直接当作相同的证据下界比较。

![左：三个β模型在360张测试图上的平均KL与采样重建MSE，每张图32组潜噪声。右：相同8维瓶颈普通AE与去噪AE，分别读取干净和固定含噪测试图，目标始终为干净图。不同训练目标的取舍在同一划分上观察。](https://ml-biomat.com/static/tutorials/machine-learning/figures/28de6f08bce1300ba20cb2a4.svg?v=28de6f08bce1)

图 3左：三个β模型在360张测试图上的平均KL与采样重建MSE，每张图32组潜噪声。右：相同8维瓶颈普通AE与去噪AE，分别读取干净和固定含噪测试图，目标始终为干净图。不同训练目标的取舍在同一划分上观察。

把KL压得很小，还可能出现后验坍塌：许多输入都得到接近先验的编码分布，解码器不再从潜变量读取足够信息。如果解码器另有很强的条件输入，绕开潜变量就更容易。诊断时可以看每维KL、不同输入均值的变化、改变潜变量后输出是否变化，以及打乱潜变量是否影响重建。本例β=4仍有约1.857 nats的平均KL，两个均值坐标的方差约为0.82和0.83，因此不能只因图像变模糊就称它完全坍塌。逐渐增加KL权重、控制解码器能力或调整信息容量，都可以改变这条训练路径。

条件VAE把一个已知要求交给编码器和解码器。本例用十维独热向量表示数字类别，编码器读取图像与类别，解码器读取潜变量与类别。这样，类别主要由条件指定，潜变量可以描述同一数字的笔画风格和其他变化。图中每列固定类别，每行使用相同的潜坐标；横向看条件改变了什么，纵向看潜变量改变了什么。2015年的深度条件生成模型工作把这种思路用于结构化输出；它也可以连接文本条件、属性条件或已知观测条件，只要明确条件在训练和生成时都怎样获得。

$$
J_\beta(x,c)=\mathbb E_{q_\phi(z\mid x,c)}[-\log p_\theta(x\mid z,c)]+\beta D_{\mathrm{KL}}(q_\phi(z\mid x,c)\|p(z))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43372e0cb627109b8d74aa73.svg) | 图像、已知条件、潜变量；本例c为10维独热类别向量，z为2维。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d98f95086ed3b254f57f2ade.svg) | 条件编码分布、条件解码分布、标准正态先验；本例先验不依赖c。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c56eaa2a890eaf09a14e9f38.svg) | KL权重、单图加权训练目标、潜变量期望；β无量纲，目标以nats计。 |

去掉c便得到本章无条件β-VAE目标。若期望重建负对数密度为−9.4、KL为3.8，β=1时目标−5.6；β=4时目标5.8。改变β改变了优化取舍。条件c=数字3时，编码器输入为64+10维，解码器输入为2+10维；训练和采样都提供类别，随机z再控制同类内部变化。

![上：条件VAE，每列类别c固定，三行分别使用z=(−1,0)、(0,0)、(1,0)。下：无条件β=1 VAE从标准正态先验抽取的60个潜变量，种子339，按原顺序全部显示。图中显示解码均值，未加入观察噪声。](https://ml-biomat.com/static/tutorials/machine-learning/figures/dbd8506fe4bf13900467e59e.svg?v=dbd8506fe4bf)

图 4上：条件VAE，每列类别c固定，三行分别使用z=(−1,0)、(0,0)、(1,0)。下：无条件β=1 VAE从标准正态先验抽取的60个潜变量，种子339，按原顺序全部显示。图中显示解码均值，未加入观察噪声。

增加条件信息改变了任务。本例条件VAE的均值重建误差为0.02575，比无条件VAE的0.03809低；前者已经知道真实类别，不需要仅从两个潜坐标传递全部信息。条件生成时也必须提供类别，而无条件生成从先验出发即可。比较两种模型时，把这些输入列清楚，比只比较一个误差数字更能说明效果来自哪里。独热条件是可计算的开关，并不自动把每个潜坐标解释为某种独立风格；可解释因素需要额外的定义、数据或检验。

## 在潜空间散步，观察生成模型真正学了什么

普通AE的二维编码可以形成弯曲、分散的区域；VAE则在KL约束下把编码分布与标准正态先验联系起来。图中的散点是编码均值，虚线圆提示先验的坐标尺度；二维标准正态的“半径1”并不等于一维正态的68%区间，因为圆内概率涉及两个坐标共同变化。旁边的图册固定一张规则网格，逐点解码，能看见输出如何随着坐标连续改变。某些相邻位置形成平滑的笔画变化，也有位置出现类别难辨的平均形态，这些都属于模型实际学到的空间结构。

![左：360张测试图的AE编码与VAE均值，颜色为真实数字，只用于展示；VAE虚线圆半径1、2提示先验尺度。右：z₁、z₂从−2.5至2.5、间隔0.5的121个解码均值。两个散点图使用各自坐标范围，不把AE与VAE轴值直接等同。](https://ml-biomat.com/static/tutorials/machine-learning/figures/546014f417231acc65e3ecbe.svg?v=546014f41723)

图 5左：360张测试图的AE编码与VAE均值，颜色为真实数字，只用于展示；VAE虚线圆半径1、2提示先验尺度。右：z₁、z₂从−2.5至2.5、间隔0.5的121个解码均值。两个散点图使用各自坐标范围，不把AE与VAE轴值直接等同。

## 拖动坐标，运行真正的解码器

左图的浅色点是部分训练图的编码均值，圆环标记半径1与2。拖动黑点或用坐标滑块，右图立即计算β=1模型的64个像素均值。点击一个像素读取其数值；“先验抽样”使用固定随机序列，便于复现；超出当前坐标时，平面和滑块范围自动等比例扩大。

[Figure: 真实VAE潜空间与解码像素](https://ml-biomat.com/tutorials/machine-learning/m33/#M33-board)

显示条件均值，不额外加入观察噪声。两维标准正态半径1、2圆内概率分别约39.3%、86.5%。潜变量坐标与像素强度均无量纲。

两个编码之间的直线插值，是观察局部连续性的简单工具；从先验抽样，则是在检查生成分布。它们取点方式不同。高维标准正态的大部分质量集中在一定半径附近，两点直线插值的中段可能更靠近中心，未必经过典型的抽样区域。生成评价因此需要同时看样本外观、重复程度、类别或结构覆盖、与训练样本的相似性以及概率目标。接触表展示固定种子的全部60个先验抽样均值，没有挑选最好看的几张；它能让读者看见输出的多样性和模糊程度，但类别覆盖还应由独立定义的判读或分类评估来统计。

交互直接载入本章训练出的β=1解码器参数。拖动潜平面的点，浏览器会执行2→64→64的网络计算，更新8×8图像，而不是切换预存图片。坐标(0,0)时64个输出强度之和约为20.30716；这个数与Python解码结果对应。选择一个像素，还能看到它的预测均值。这里操作的是一个已经训练好的概率模型的均值函数，既能帮助理解潜变量怎样影响输出，也能把公式、代码和可见图像连成同一件事。

## 完整实验：固定划分，分别检查重建与生成

程序使用1797张公开手写数字图，种子330与331产生分层划分：1077张训练、360张验证、360张测试。七个模型各训练100轮：2维和8维AE、8维去噪AE、三个β的2维VAE，以及一个2维条件VAE。每个模型根据自身验证目标保存最佳参数。去噪模型验证时使用固定噪声图，VAE验证时使用固定的8组潜噪声，测试则使用另外32组。这样，图中每个结果都能追溯到同一个数据划分，同时保留不同方法各自真正优化的目标。

### 完整Python：七个模型与真实潜空间

运行python main.py --output results --language zh，依赖NumPy、Matplotlib、scikit-learn和PyTorch。数据随sklearn提供，程序训练全部七个模型并保存四组SVG、summary.json、experiment.npz、解码器参数JSON与权重。观察标准差固定0.25；重建MSE、采样MSE、KL和负ELBO分别记录。

```
"""Actual AE, denoising AE, beta-VAE, and conditional VAE on bundled digits."""
from pathlib import Path
import argparse,copy,json,platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
d=load_digits();x=(d.data/16).astype('float32');y=d.target
train,other=train_test_split(np.arange(len(y)),test_size=720,random_state=330,stratify=y)
val,test=train_test_split(other,test_size=360,random_state=331,stratify=y[other])
xt,xv,xe=[torch.tensor(x[i]) for i in [train,val,test]];yt,yv,ye=[torch.tensor(y[i]) for i in [train,val,test]]
class AE(nn.Module):
 def __init__(self,latent):
  super().__init__();self.encoder=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,latent));self.decoder=nn.Sequential(nn.Linear(latent,64),nn.ReLU(),nn.Linear(64,64),nn.Sigmoid())
 def forward(self,x):return self.decoder(self.encoder(x))
class VAE(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;c=10 if conditional else 0
  self.encoder=nn.Sequential(nn.Linear(64+c,64),nn.ReLU());self.mu=nn.Linear(64,2);self.logvar=nn.Linear(64,2)
  self.decoder=nn.Sequential(nn.Linear(2+c,64),nn.ReLU(),nn.Linear(64,64),nn.Sigmoid())
 def condition(self,v,y):return torch.cat([v,F.one_hot(y,10).float()],1) if self.conditional else v
 def encode(self,x,y):
  h=self.encoder(self.condition(x,y));return self.mu(h),self.logvar(h)
 def decode(self,z,y):return self.decoder(self.condition(z,y))
 def forward(self,x,y,eps):
  mu,lv=self.encode(x,y);z=mu+torch.exp(.5*lv)*eps;return self.decode(z,y),mu,lv
def kl(mu,lv):return .5*(mu.square()+lv.exp()-1-lv).sum(1)
sigma=.25;models={};histories={};metrics={}
noisegen=torch.Generator().manual_seed(332)
noisy_test=(xe+.25*torch.randn(xe.shape,generator=noisegen)).clamp(0,1)
fixed_val_noise=(xv+.25*torch.randn(xv.shape,generator=noisegen)).clamp(0,1)
for name,latent,denoise in [('ae2',2,False),('ae8',8,False),('denoise8',8,True)]:
 torch.manual_seed(333);model=AE(latent);opt=torch.optim.Adam(model.parameters(),lr=.003);gen=torch.Generator().manual_seed(334);best=1e9;history=[]
 for epoch in range(100):
  model.train()
  for ids in torch.randperm(len(xt),generator=gen).split(64):
   inp=xt[ids]
   if denoise:inp=(inp+.25*torch.randn(inp.shape,generator=gen)).clamp(0,1)
   loss=F.mse_loss(model(inp),xt[ids]);opt.zero_grad();loss.backward();opt.step()
  model.eval()
  with torch.no_grad():vl=F.mse_loss(model(fixed_val_noise if denoise else xv),xv).item()
  history.append(vl)
  if vl<best:best=vl;beststate=copy.deepcopy(model.state_dict());bestepoch=epoch+1
 model.load_state_dict(beststate);models[name]=model;histories[name]=history
 with torch.no_grad():metrics[name]=dict(clean_mse=F.mse_loss(model(xe),xe).item(),noisy_mse=F.mse_loss(model(noisy_test),xe).item(),best_epoch=bestepoch,parameters=sum(p.numel() for p in model.parameters()))
for name,beta,condition in [('vae02',.2,False),('vae1',1.,False),('vae4',4.,False),('conditional',1.,True)]:
 torch.manual_seed(335);model=VAE(condition);opt=torch.optim.Adam(model.parameters(),lr=.003);gen=torch.Generator().manual_seed(336);history=[];best=1e9
 vg=torch.Generator().manual_seed(337);valeps=torch.randn((8,len(xv),2),generator=vg)
 for epoch in range(100):
  model.train()
  for ids in torch.randperm(len(xt),generator=gen).split(64):
   recon,mu,lv=model(xt[ids],yt[ids],torch.randn((len(ids),2),generator=gen))
   distortion=(recon-xt[ids]).square().sum(1)/(2*sigma*sigma)
   loss=(distortion+beta*kl(mu,lv)).mean();opt.zero_grad();loss.backward();opt.step()
  model.eval()
  with torch.no_grad():
   mu,lv=model.encode(xv,yv);pred=torch.stack([model.decode(mu+(.5*lv).exp()*eps,yv) for eps in valeps]);dist=(pred-xv).square().sum(2).mean(0)/(2*sigma*sigma);vl=(dist+beta*kl(mu,lv)).mean().item()
  history.append(vl)
  if vl<best:best=vl;beststate=copy.deepcopy(model.state_dict());bestepoch=epoch+1
 model.load_state_dict(beststate);models[name]=model;histories[name]=history
 with torch.no_grad():
  mu,lv=model.encode(xe,ye);meanrec=model.decode(mu,ye)
  eg=torch.Generator().manual_seed(338);eps=torch.randn((32,len(xe),2),generator=eg)
  pred=torch.stack([model.decode(mu+(.5*lv).exp()*e,ye) for e in eps]);expectedmse=(pred-xe).square().mean().item();k=kl(mu,lv).mean().item()
  constant=64*.5*np.log(2*np.pi*sigma*sigma)
  metrics[name]=dict(beta=beta,mean_reconstruction_mse=F.mse_loss(meanrec,xe).item(),sampled_reconstruction_mse=expectedmse,kl_nats=k,negative_elbo_nats=expectedmse*64/(2*sigma*sigma)+constant+k,mu_variance=mu.var(0,unbiased=False).tolist(),best_epoch=bestepoch,parameters=sum(p.numel() for p in model.parameters()))
for name,model in models.items():torch.save(model.state_dict(),out/f'{name}.pt')
chosen=np.array([np.flatnonzero(y[test]==k)[0] for k in range(10)])
with torch.no_grad():
 mu,lv=models['vae1'].encode(xe,ye);vae_rec=models['vae1'].decode(mu,ye)
 rows=[xe[chosen],models['ae2'](xe[chosen]),models['ae8'](xe[chosen]),vae_rec[chosen],noisy_test[chosen],models['denoise8'](noisy_test[chosen])]
fig,axs=plt.subplots(6,10,figsize=(13,8.6),gridspec_kw={'wspace':.04,'hspace':.2})
labels=tr(['原图','AE：2维','AE：8维','VAE：均值重建','含噪输入','去噪AE：8维'],['Original','AE: 2D','AE: 8D','VAE: mean code','Noisy input','Denoising AE: 8D'])
for r,row in enumerate(rows):
 for c,img in enumerate(row):
  axs[r,c].imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);axs[r,c].set_xticks([]);axs[r,c].set_yticks([])
  if r==0:axs[r,c].set_title(str(c))
 axs[r,0].set_ylabel(labels[r],fontsize=10)
fig.suptitle(tr('同一测试图：容量、随机潜变量与去噪目标','The same test images: capacity, stochastic codes, and denoising'),y=.97);save(fig,'reconstruction')
with torch.no_grad():
 az=models['ae2'].encoder(xe).numpy();vz=mu.numpy();vg=np.linspace(-2.5,2.5,11)
 grid=np.array([[a,b] for b in vg[::-1] for a in vg],dtype='float32');decoded=models['vae1'].decode(torch.tensor(grid),torch.zeros(len(grid),dtype=torch.long)).numpy()
mosaic=np.zeros((88,88))
for i,img in enumerate(decoded):mosaic[(i//11)*8:(i//11+1)*8,(i%11)*8:(i%11+1)*8]=img.reshape(8,8)
fig=plt.figure(figsize=(13,7));gs=fig.add_gridspec(2,2,width_ratios=[1,1.2],hspace=.5,wspace=.32)
for i,(arr,title) in enumerate([(az,tr('A  AE 的确定性坐标','A  Deterministic AE coordinates')),(vz,tr('B  VAE 的编码均值','B  VAE encoder means'))]):
 ax=fig.add_subplot(gs[i,0]);sc=ax.scatter(arr[:,0],arr[:,1],c=y[test],cmap='tab10',s=9,alpha=.7);ax.set(xlabel=r'$z_1$' if i==0 else r'$\mu_1$',ylabel=r'$z_2$' if i==0 else r'$\mu_2$',title=title)
 fig.colorbar(sc,ax=ax,ticks=range(10),fraction=.04,pad=.03,label=tr('数字','Digit'))
 if i==1:
  ax.set_aspect('equal',adjustable='box')
  for radius in [1,2]:ax.add_patch(plt.Circle((0,0),radius,fill=False,color='#6c767c',ls='--',lw=.8))
ax=fig.add_subplot(gs[:,1]);ax.imshow(mosaic,cmap='gray_r',vmin=0,vmax=1,extent=[-2.75,2.75,-2.75,2.75]);ax.set(xlabel=r'$z_1$',ylabel=r'$z_2$',title=tr('C  β=1：解码均值图册，网格间距 0.5','C  β=1 decoder-mean atlas; grid spacing 0.5'));save(fig,'latent')
fig,(ax,bar)=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
colors=['#125f82','#b85d30','#658248']
for name,color in zip(['vae02','vae1','vae4'],colors):
 m=metrics[name];ax.scatter(m['kl_nats'],m['sampled_reconstruction_mse'],s=110,color=color);ax.annotate('β='+str(m['beta']),(m['kl_nats'],m['sampled_reconstruction_mse']),xytext=(8,7),textcoords='offset points',fontsize=11)
ax.set(xlabel=tr('平均 KL / nats 每图','Mean KL / nats per image'),ylabel=tr('采样重建均方误差 / 像素','Sampled reconstruction MSE / pixel'),title=tr('A  信息约束与重建的实际取舍','A  Measured information–distortion tradeoff'));ax.margins(.25)
names=['ae8','denoise8'];xx=np.arange(2);bar.bar(xx-.17,[metrics[n]['clean_mse'] for n in names],.34,color='#125f82',label=tr('干净输入','Clean input'));bar.bar(xx+.17,[metrics[n]['noisy_mse'] for n in names],.34,color='#b85d30',label=tr('含噪输入','Noisy input'));bar.set_xticks(xx,[tr('普通 AE','Ordinary AE'),tr('去噪 AE','Denoising AE')]);bar.set(ylabel=tr('对干净图的均方误差 / 像素','MSE against clean images / pixel'),title=tr('B  相同8维瓶颈，不同训练目标','B  Same 8D bottleneck, different objectives'));bar.legend();save(fig,'tradeoff')
gen=torch.Generator().manual_seed(339);prior=torch.randn((60,2),generator=gen)
with torch.no_grad():
 samples=models['vae1'].decode(prior,torch.zeros(60,dtype=torch.long)).numpy()
 positions=torch.tensor([[-1.,0.],[0.,0.],[1.,0.]])
 cond=np.stack([models['conditional'].decode(positions,torch.full((3,),k)).numpy() for k in range(10)])
fig=plt.figure(figsize=(13,8));gs=fig.add_gridspec(2,1,height_ratios=[1,1.2],hspace=.32)
top=gs[0].subgridspec(3,10,wspace=.03,hspace=.06)
for k in range(10):
 for j in range(3):
  ax=fig.add_subplot(top[j,k]);ax.imshow(cond[k,j].reshape(8,8),cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
  if j==0:ax.set_title('c='+str(k))
  if k==0:ax.set_ylabel(f'z1={j-1}, z2=0',fontsize=9)
bottom=gs[1].subgridspec(5,12,wspace=.03,hspace=.06)
for i,img in enumerate(samples):
 ax=fig.add_subplot(bottom[i//12,i%12]);ax.imshow(img.reshape(8,8),cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('无条件先验抽样','Unconditional prior draws'),loc='left',fontsize=11)
fig.suptitle(tr('条件控制与随机变化：显示解码分布均值','Conditional control and random variation: decoder means'),y=.98);save(fig,'generation')
with torch.no_grad():
 means=models['vae1'].encode(xt,yt)[0].numpy()
 probes={str(pair):models['vae1'].decode(torch.tensor([pair],dtype=torch.float32),torch.tensor([0]))[0].tolist() for pair in [[0,0],[1,-1],[-2,2]]}
weights={k:v.detach().numpy().tolist() for k,v in models['vae1'].decoder.state_dict().items()}
(out/'decoder.json').write_text(json.dumps(dict(weights=weights,means=means[::7].tolist(),labels=y[train][::7].tolist(),probes=probes)),encoding='utf-8')
mu_hand=torch.tensor([.5],dtype=torch.float64,requires_grad=True);lv_hand=torch.tensor([np.log(.25)],dtype=torch.float64,requires_grad=True);eps_hand=torch.tensor([-.4],dtype=torch.float64);z_hand=mu_hand+(.5*lv_hand).exp()*eps_hand
grad_mu,grad_lv=torch.autograd.grad(z_hand.sum(),[mu_hand,lv_hand]);kl_hand=kl(mu_hand.reshape(1,1),lv_hand.reshape(1,1)).item()
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),splits=dict(train=len(train),validation=len(val),test=len(test)),seed=330,epochs=100,sigma=sigma,metrics=metrics,
 hand=dict(z=z_hand.item(),dz_dmu=grad_mu.item(),dz_dlogvar=grad_lv.item(),kl=kl_hand,normal_constant_per_image=float(64*.5*np.log(2*np.pi*sigma*sigma))),
 decoder_checks={str(k):dict(sum=float(np.sum(v)),pixel0=v[0]) for k,v in probes.items()})
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train_indices=train,val_indices=val,test_indices=test,chosen_test_indices=chosen,reconstruction=np.stack([r.numpy() for r in rows]),ae_latents=az,vae_means=vz,grid=grid,decoded=decoded,prior=prior.numpy(),samples=samples,conditional=cond,**{n+'_history':h for n,h in histories.items()})
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

代码保存图像接触表、潜坐标、先验抽样点、条件输出、训练曲线和各模型参数。阅读时可以先重算一个高斯KL，再检查一次重参数化导数，最后对照图像观察这两项怎样影响学习。进一步实验可以只改变潜维度、观察噪声、β或条件信息中的一项。每次都分别记录重建、采样和表示变化：一张图画得更像、一个潜空间更规整、一个生成集合更丰富，是相互联系但各有定义的目标。把这些目标说清楚，自编码器与VAE的用途才会变得具体。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M33.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Auto-Encoding Variational Bayes](https://arxiv.org/html/1312.6114v11)

   §2.2–2.4：ELBO、重参数化；附录B高斯KL、附录C高斯解码器。

   Primary paper; no figure copied
2. [UvA Tutorial 9: Deep Autoencoders](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial9/AE_CIFAR10.html)

   编码瓶颈与潜维度原始实验图。

   MIT; copyright 2020 Phillip Lippe; license included
3. [PyTorch examples: VAE](https://github.com/pytorch/examples/tree/main/vae)

   均值/对数方差、采样与KL的官方代码结构；本章另选Gaussian观察模型。

   BSD-3-Clause code; independent teaching implementation
4. [Understanding disentangling in beta-VAE](https://arxiv.org/abs/1804.03599)

   信息容量与重建的取舍。

   Primary paper; no figure copied
5. [Learning Structured Output Representation using Deep Conditional Generative Models](https://proceedings.neurips.cc/paper/2015/hash/8d55a249e6baa5c06772297520da2051-Abstract.html)

   条件潜变量模型与结构化输出。

   Primary paper; no figure copied
6. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   图像数据定义。

   CC BY 4.0; E. Alpaydin and C. Kaynak
