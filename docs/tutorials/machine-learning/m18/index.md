# 让生成器学会分布：GAN、DCGAN与WGAN

Source: https://ml-biomat.com/tutorials/machine-learning/m18/
Language: zh-CN

从八个小簇追踪对抗训练，再看卷积图像、条件控制与生成评价为什么需要不同证据。

## 没有逐张答案，怎样教模型画出合理的图

给模型一张模糊照片，希望它补出清楚的细节，问题很快会超过逐像素比较：同一种头发可以有不同的细丝排列，同一片草地可以有许多合理纹理。若把所有可能答案平均，结果往往平滑，却缺少真实图像的细节结构。生成模型面对的任务，是学会产生一组合理的结果，而不只是对某个输入给出一个平均答案。GAN提供了一种学习信号：让另一个网络不断比较真实样本和生成样本，把它发现的差异传回生成器。

可以想象两个人一起练习陶艺。一人制作杯子，另一人看大量成品后指出哪些结构显得不自然。制作者不需要拿到每一件作品唯一正确的逐点坐标，却需要从反馈中学到整体比例和局部细节。实际GAN使用可微计算传递这种反馈，判别器也会随着生成样本改变自己的判断标准。于是这不再是对一个固定答案集做普通回归，而是两个网络彼此影响的学习过程。它能用于纹理合成、图像翻译和数据分布建模；每个用途还需要说明哪些变化允许自由生成，哪些内容必须保留。

Goodfellow等人在2014年的工作提出了生成器与判别器的对抗训练框架。2015年的DCGAN把卷积结构系统地用于图像生成，2017年的WGAN与梯度惩罚方法则重新讨论了分布距离和训练信号。本章先在二维平面上观察这些问题，再进入真实手写图像。下面的GAN Lab分镜保留了原项目动画的六个时刻：绿色目标点围成圆环，紫色生成点随训练改变。点怎样移动、是否覆盖整圈，比单独的一条损失曲线更容易揭示生成过程。

![GAN Lab原动画的六帧分镜，按原始帧0、46、92、138、184、231排列；绿色是真实圆环样本，紫色是生成样本。原图作者：Minsuk Kahng、Nikhil Thorat、Duen Horng Chau、Fernanda B. Viégas、Martin Wattenberg；Apache 2.0。改编仅为静态抽帧与拼排，非本章八簇训练结果。](https://ml-biomat.com/static/tutorials/machine-learning/figures/52acca42d21e06223efc6fe8.png?v=52acca42d21e)

图 1GAN Lab原动画的六帧分镜，按原始帧0、46、92、138、184、231排列；绿色是真实圆环样本，紫色是生成样本。原图作者：Minsuk Kahng、Nikhil Thorat、Duen Horng Chau、Fernanda B. Viégas、Martin Wattenberg；Apache 2.0。改编仅为静态抽帧与拼排，非本章八簇训练结果。

## 生成器给样本，判别器给反馈

生成器读取一组简单随机数，例如两个标准正态坐标，再输出一个二维点；图像生成器则可以把较短的随机向量变成整张图。这组随机数叫潜变量，提供输出变化的来源。判别器读取一个样本，输出“来自真实数据”的概率。训练判别器时，真实点的目标是1，当前生成点的目标是0；训练生成器时，则希望生成点得到更高的真实概率。生成器并没有逐点配对的目标位置，它通过许多样本的共同分布接受约束。

$$
\min_\theta\max_\psi V=\mathbb E_{x\sim p_{\mathrm{data}}}[\log D_\psi(x)]+\mathbb E_{z\sim p_z}[\log(1-D_\psi(G_\theta(z)))]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eb1908cc8450efe542f213a3.svg) | 真实样本、潜随机向量、生成样本；二维实验x与z均为2维，坐标无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f979d55af01ef145a0c149e.svg) | 参数θ的生成器与参数ψ的判别器；D输出0到1之间的真实概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/39104b8057611a12e33da53c.svg) | 目标数据分布、标准正态潜分布，以及对应分布上的期望。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7786a72523421eab514da2ff.svg) | 对抗价值、自然对数、生成器最小化与判别器最大化方向；对数项以nats计。 |

判别器最大化真样本的logD和生成样本的log(1−D)，等价于最小化两项负对数。若D(real)=0.8、D(fake)=0.2，判别损失为−2ln0.8≈0.446287。最小化该式的生成器希望提升D(fake)。实际代码保留判别目标，生成目标采用下一式的非饱和形式。

判别器对一个真实点给出0.8，对一个生成点给出0.2，这一对样本的判别损失为约0.4463。如果两个输出都为0.5，损失约为1.3863。这个数字需要结合训练阶段理解：0.5可能意味着两种分布接近，也可能意味着判别器还没有学会区分。只有在理想化的分布匹配情形，最优判别器才在两种来源混合处无法区分。实际实验应同时看生成样本、覆盖和独立距离，而不是把判别准确率50%自动当成成功。

本章的目标分布有八个小簇，中心均匀放在半径2的圆周上，每个坐标再加入标准差0.08的独立高斯噪声。它比单个圆环多了一层结构：样本既要靠近正确位置，也要把质量分配给八个模式。二维生成器有两个64单元隐藏层，最后用平滑变换把输出限制在−3到3的显示区域。每个生成坐标都来自实际网络计算，训练和测试目标点用不同种子生成；测试集只参与观察结果。

## 交替更新：同一张计算图，两种梯度路径

更新判别器时，生成样本暂时作为固定输入。代码把它从生成器的计算图中分离，防止这一步顺手修改生成器；随后让判别器更好地区分真假。更新生成器时，判别器参数保持固定，但判别结果对输入的导数仍然需要保留。生成器先接收“怎样改变样本能提高评分”的方向，再把这个方向传回自己的参数。如果在这一阶段把整个判别计算都放入不求梯度的环境，学习信号也会被一起切断。冻结参数与切断输入梯度是两种不同的操作。

原始极小极大目标在判别器很自信时，可能给生成器很小的梯度。例如某个生成点被判为真实的概率只有0.01，原始饱和形式对判别logit的梯度幅值约0.01；常用的非饱和目标则约0.99。两种形式都希望提高生成样本的真实评分，但优化早期的推动力差别很大。本章使用非饱和生成器损失，判别器直接输出logit，再通过数值稳定的softplus计算损失，避免先构造接近0的概率再取对数。

$$
L_G^{\mathrm{sat}}=\log(1-\sigma(a)),\quad L_G^{\mathrm{NS}}=-\log\sigma(a),\qquad \frac{\partial L_G^{\mathrm{sat}}}{\partial a}=-\sigma(a),\quad\frac{\partial L_G^{\mathrm{NS}}}{\partial a}=\sigma(a)-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bc1be4a7792db09d517828f5.svg) | 判别器对单个生成点给出的logit及其sigmoid概率，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d90457f08ec556210aaeda7c.svg) | 生成器饱和与非饱和单样本损失，前者为负或零，后者非负，以nats计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96b9ee67af2db0b7893154ee.svg) | 对logit的导数，继续乘判别器输入导数与生成器参数导数后得到完整梯度。 |

令a=ln(0.01/0.99)，sigmoid(a)=0.01，两个导数分别为−0.01与−0.99。梯度下降都会提高a，但第二种推动更强。非饱和损失用softplus(−a)计算。这里比较的是同一logit处的局部导数，完整网络中的梯度还取决于后续链式法则。

交替过程也解释了为什么一条损失曲线不足以描述训练。判别器刚学会一种新线索，生成器损失可能上升；生成器堵住某个漏洞，判别器又要寻找新的线索。学习率、每轮双方的更新次数和网络容量共同决定两者追赶的速度。图中固定同一批潜变量，展示它们在不同训练时刻的位置。这样可以区分“画面随机换了一批点”与“同一组输入经过更新后的网络，确实移动到了不同位置”。

![固定128组潜变量在0、300、750、1500次生成更新后的输出；橙色是同一批独立目标点，蓝色是生成点。两行分别为GAN与WGAN-GP，同一坐标范围便于观察漂移、簇间过渡与覆盖变化。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2dc14858286451db77d8b613.svg?v=2dc148582864)

图 2固定128组潜变量在0、300、750、1500次生成更新后的输出；橙色是同一批独立目标点，蓝色是生成点。两行分别为GAN与WGAN-GP，同一坐标范围便于观察漂移、簇间过渡与覆盖变化。

## 跟踪同一组噪声的训练旅程

这里回放实际训练保存的快照，每格相隔50次生成器更新。蓝点始终对应同一批128个潜输入；橙点是独立目标样本。选择一个蓝点编号，可显示它从训练开始到当前时刻的轨迹。右侧统计使用全部2048个生成点。

[Figure: 实际GAN训练回放、选定点轨迹与模式计数](https://ml-biomat.com/tutorials/machine-learning/m18/#M18-board)

GAN背景显示真实概率。WGAN背景显示减去当前网格均值的critic评分，颜色刻度随该帧标明；减去常数不改变输入梯度。坐标无量纲，所有快照共享相同范围。

## 从真假概率转向搬运一堆沙子的距离

两堆沙子的位置不同，怎样衡量把一堆搬成另一堆要付出多少代价？如果每小份沙子的搬运距离就是成本，那么分布之间的位置差异会自然进入比较。Wasserstein距离采用这种质量搬运思路。最简单的例子是一份质量集中在0，另一份集中在2：搬运距离是2；把第二份移到0.5，距离变成0.5。即使两份质量从未重叠，距离也能连续反映它们靠近的程度。这给生成器提供了与“真假是否容易分开”不同的反馈视角。

$$
W_1(P,Q)=\sup_{\|f\|_{\mathrm{Lip}}\le1}\left(\mathbb E_{x\sim P}f(x)-\mathbb E_{y\sim Q}f(y)\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/775185e771e23c7dab6c1e19.svg) | 目标与生成分布、各自的样本；输入空间采用欧氏距离。 |
| ![Formula](https://ml-biomat.com/static/agent-math/299c0db7dbc479dcd70cb003.svg) | 实数评分函数，满足任意两点\|f(x)−f(y)\|≤\|\|x−y\|\|；输出不是概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/acf251e3efd8841b6a4a4236.svg) | 所有满足约束函数中的上确界、1阶Wasserstein距离、期望；距离单位随输入坐标。 |

若P全部在0、Q全部在2，取f(x)=−x，评分差为2；1-Lipschitz条件也限制任意可行差不超过2，所以距离为2。神经critic只在有限函数族和训练预算内近似这个优化。本章最小化critic损失E_fake f−E_real f加惩罚，生成器最小化−E_fake f。

WGAN用一个实数评分函数近似这个分布距离，通常称它为critic。它的输出不经过sigmoid，也不解释成概率。为了让评分差具有距离意义，需要限制评分随输入变化的速度：输入移动一个单位，评分变化不应超过一个单位，这就是1-Lipschitz条件。若没有约束，把所有评分乘以一千就能把差距放大一千倍，数值便失去固定尺度。原始WGAN使用权重截断来间接限制函数；WGAN-GP改为在真实点与生成点之间采样位置，对输入梯度的范数施加惩罚。

$$
\widetilde x=t x+(1-t)G_\theta(z),\quad t\sim U[0,1],\qquad L_{\mathrm{GP}}=\lambda\mathbb E\left[(\|\nabla_{\widetilde x}f(\widetilde x)\|_2-1)^2\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a9c35f5ab162afce2c2cd0f4.svg) | 真实点、生成点与二者之间的插值点，均为同维度向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/12d756cc228f0bd6288c2eee.svg) | 在0–1均匀抽取的插值系数，与坐标无关，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/188c73183abb00d191faa5b9.svg) | 评分对输入坐标的梯度向量及其欧氏范数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/629afdc2e987ccdb6c292fcd.svg) | 惩罚权重，本例10，以及加到critic目标上的惩罚。 |

二维梯度(3,4)范数为5，未加权惩罚(5−1)²=16；λ=10时贡献160。梯度(0.6,0.8)范数为1，惩罚为0。代码对输入求导时保留计算图，因为随后还要对这项梯度范数求参数导数。该惩罚作用于抽样插值位置，是可实现的局部约束。

本例每次生成器更新前做五次critic更新，梯度惩罚权重为10。惩罚只在本轮抽到的插值位置计算，约束的是评分函数的局部变化；它不直接要求生成点落进某个目标小簇。1500次生成器更新后，这次WGAN-GP只有约5.62%的点进入规定邻域，达到覆盖阈值的模式为2个；普通GAN为约46.39%，覆盖8个。WGAN-GP花了7500次critic更新，普通GAN为1500次。这个对照把目标函数、优化进度和计算预算同时摆出来，不能由方法名称预先决定哪条曲线应该更好。

读WGAN轨迹时，先看点群是否仍在移动，再看质量是否集中在少数方向。梯度惩罚下降，说明抽样位置的梯度范数更接近要求；它与分布已经匹配是不同的测量。较小的学习率、更多训练步骤、更合适的critic容量或不同约束，都可以成为后续有针对性的实验，但要沿用同一组覆盖和距离指标观察。这里保留固定终点和整段轨迹，让训练中的振荡与偏移成为可以检查的现象，而不是只选某张看起来最接近目标的截图。

## DCGAN怎样从小网格长出一张图

二维点只需要两个输出，图像却包含相邻像素之间的结构。DCGAN把卷积带来的局部连接和参数共享用于对抗模型：生成器逐层扩大空间尺寸，判别器则通过步幅卷积逐层压缩图像。本章的小型卷积生成器把8维噪声投影为32通道的2×2网格，再扩成16通道4×4，最后得到单通道8×8图像。隐藏层使用批归一化与ReLU，输出使用tanh；真实图像也缩放到−1到1，使判别器接收一致的强度范围。

$$
n_{\mathrm{out}}=(n_{\mathrm{in}}-1)s-2p+k+o
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/08d7b5c10397ef3b8b7b5c3b.svg) | 某个空间方向上的输入与输出网格长度，单位为像素位置数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/afe7915b50d7cb6d0c9a6acf.svg) | 步幅、每侧填充、核大小、output_padding；本式膨胀率1，o用于选择输出尺寸。 |

n_in=2、s=2、p=1、k=4、o=0时输出为4；再从4得到8。覆盖次数实验不填充：4格输入、步幅2、核3输出9格，核4输出10格。大小公式描述网格尺寸；像素数值由所有重叠的核贡献相加，不能从尺寸推断图像已经被正确恢复。

转置卷积可以理解为让小网格上的每个数，在大网格上贡献一块带权图案，重叠位置把贡献相加。它不是先前卷积的一般逆运算：多个输入可能在卷积中得到同样输出，转置矩阵并不能自动找回丢失的信息。核宽3、步幅2时，某些位置被覆盖一次，另一些两次；二维相乘后就会出现1、2、4的交错覆盖。下面把输入和核都设为1，直接画出覆盖次数。核宽4、步幅2使内部覆盖更均匀，但边界仍不同，学习到的权重也仍会影响实际纹理。

![输入4×4全1、卷积核全1、步幅2、无填充的转置卷积输出。每个数字是实际覆盖次数。核3产生9×9输出，核4产生10×10输出；内部与边界的覆盖差别均保留。](https://ml-biomat.com/static/tutorials/machine-learning/figures/542e97c3ddfe5fc7bd8fdbea.svg?v=542e97c3ddfe)

图 3输入4×4全1、卷积核全1、步幅2、无填充的转置卷积输出。每个数字是实际覆盖次数。核3产生9×9输出，核4产生10×10输出；内部与边界的覆盖差别均保留。

这正是2016年Distill关于格纹伪影的分析所强调的结构问题。把上采样与普通卷积分开，例如先按确定规则扩大网格，再学习卷积，可以改变重叠方式。选择结构时先问空间尺寸怎样变化、每个位置收到多少贡献，再看训练出的图像，能够把“看起来有格子”追溯到具体计算。本章没有把二维全连接生成器换个名字叫DCGAN，而是另外训练了真实的转置卷积网络，使用1437张训练图、1200次双方更新，并保留360张图用于展示独立样本形态。

![上：20张未参加训练的手写图。下：小型DCGAN训练1200次后，对固定60组8维噪声的全部输出，统一0–1灰度。图像数据：E. Alpaydin、C. Kaynak，UCI，CC BY 4.0。生成图来自实际训练模型。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e843859bd205768d8000b334.svg?v=e843859bd205)

图 4上：20张未参加训练的手写图。下：小型DCGAN训练1200次后，对固定60组8维噪声的全部输出，统一0–1灰度。图像数据：E. Alpaydin、C. Kaynak，UCI，CC BY 4.0。生成图来自实际训练模型。

生成接触表使用训练前固定的60组噪声，按原顺序全部展示。可以观察笔画是否连贯、不同样本是否过于相像，以及有没有难以归类的形态。这个8×8任务让卷积生成过程在CPU上完整跑起来，模型输出与高分辨率图像的用途不同；若要生成更大图像，空间层级、数据量和判别器的观察范围也必须随之调整。生成阶段通常只运行生成器，判别器主要承担训练反馈，因此训练成本与单张采样成本也要分别记录。

## 指定想要什么：条件GAN与图像翻译

无条件生成器自己决定产生哪个模式；条件GAN把类别、文字或另一张图作为额外输入。2014年的条件GAN工作把条件同时送给生成器和判别器：生成器需要满足要求，判别器也要判断样本与要求是否相容。如果只让判别器看图，生成器可能画出合理的猫，却忽略“画一只狗”的指令。条件提供了新的可用信息，因此不能把条件模型与完全不知道类别的模型当成同一输入任务比较。

本章用八维独热向量指定二维簇编号，两个网络都读取这个条件。为了进一步连接成对图像翻译，实验还加入权重10的L1项，让生成坐标接近同类别的实际训练点；图中明确标成“cGAN + L1”。这里每个条件对应一小团高斯点，而噪声与具体训练点没有一一对应关系，因此L1部分偏向该簇的中心。评估时按簇编号循环提出请求，每类各256次，因此请求本身均匀；覆盖统计检查生成结果是否真的到达这些要求的位置。结果条件匹配率达到100%，约99.95%的点落入规定邻域，八个簇都有覆盖；与此同时，需要继续检查簇内变化是否被压得过小。指定类别、准确到达中心和恢复完整随机分布，是三个可以分别测量的目标。

$$
L_{G,c}=\mathbb E_{z,c}[-\log D(G(z,c),c)]+\lambda_1\mathbb E_{(c,y),z}\left[\frac1{d_y}\sum_{j=1}^{d_y}|G(z,c)_j-y_j|\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1fc699f40396eab4db38187a.svg) | 已知条件、独立随机潜变量、与条件配对的目标；本例c为8维独热簇编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/efc2ea22e3846678963a6b11.svg) | 条件生成器输出与同时读取条件的判别器。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e10654059f4b3a972139ef46.svg) | 输出坐标数、本坐标索引与L1权重；二维例d_y=2，λ₁=10。 |

条件指定某簇，目标坐标(2,0)，生成坐标(1.8,0.1)，平均L1误差(0.2+0.1)/2=0.15，加权后为1.5。另加对抗项，要求输出符合该条件下的真实分布。若z与y的细小噪声独立，L1倾向条件中位数，可能压缩类内变化；因此单独测量生成方差。

pix2pix把这个思路用于成对图像：输入可以是边缘图，目标是与它对应的照片；生成器常采用带跳跃连接的编码器—解码器，把空间位置的信息传给输出。PatchGAN判别器对多个局部区域评分，帮助学习局部纹理；L1项则维持与配对目标的大尺度一致。对抗项与重建项解决的要求不同。若一个灰度场景存在多种合理颜色，而每个输入只给出一张彩色答案，强重建项可能鼓励平均或常见颜色；加入随机潜变量也不保证模型一定使用它，仍要在同一条件下改变噪声、实际观察输出变化。

## 画得像、种类全、变化足，要分开检查

模式崩溃最直观的表现，是不同随机输入反复落到少数类型。一个模型可能画出很像样的“8”，却几乎从不画其他数字。只挑几张漂亮样本会掩盖这个问题；只看总体均值也可能看不见。我们的二维任务可以把评价定义得很具体：生成点距离最近中心小于0.24，记为有效；某个模式至少包含全部2048个生成点的1%，才算达到覆盖阈值。这样，离中心很远的过渡点不会被简单归类后混进高质量覆盖统计。

![上：最终点分布与对应评分场，散点显示128个生成点；GAN色标是概率，WGAN色标是critic实数评分，条件模型使用已知类别与L1项。下：全部2048个生成点在0.24半径内的模式计数，虚线为均匀分配256点。](https://ml-biomat.com/static/tutorials/machine-learning/figures/84d13c387685eb81f6bc16b2.svg?v=84d13c387685)

图 5上：最终点分布与对应评分场，散点显示128个生成点；GAN色标是概率，WGAN色标是critic实数评分，条件模型使用已知类别与L1项。下：全部2048个生成点在0.24半径内的模式计数，虚线为均匀分配256点。

覆盖计数仍然不能表示簇内方差是否正确。条件模型即使把每类所有噪声都映射到同一个中心，也可以在类别和有效比例上拿到很高的成绩，却失去目标中的细小随机变化。程序因此另外记录条件模型的类内标准差，并保留全部生成坐标。这次按类别和坐标平均方差后再开方，得到0.02458，小于目标的0.08；强L1项使输出更集中在簇中心，同时压缩了簇内变化。普通GAN虽然覆盖八个模式，有效比例却只有46.39%，说明不少点还留在小簇之间或周围。把模式数、有效比例与类内变化并排读，能够避免用一个好看的指标替代整个生成任务。

另一个测量把真实点和生成点投影到许多方向，分别排序，再计算对应位置的平均距离。在一维、等权样本下，排序配对给出经验Wasserstein距离；对32个方向平均，就得到这里的投影距离。它同时感受到位置变化和质量分配，且不需要借助正在训练的判别器。方向有限时仍可能遗漏某些结构，因此它与模式覆盖共同使用。图中也保留生成器损失，但普通GAN的负对数概率与WGAN的负critic评分不是同一种量，不按曲线高低直接排名。

$$
\widehat W_{\mathrm{proj}}=\frac1{Kn}\sum_{k=1}^K\sum_{i=1}^n|a^{(k)}_{(i)}-b^{(k)}_{(i)}|,\qquad a^{(k)}_i=u_k^{\mathsf T}x_i,\quad b^{(k)}_i=u_k^{\mathsf T}\widehat x_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e57eec8d96fb9b979a8d1b6.svg) | 第i个目标与生成点、第k个单位投影方向；本例为二维。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3d0b0bef87f72567316ddce8.svg) | 投影坐标与从小到大排序后的第i个值；排序分别在两组样本中进行。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f1d1453c5268cc78383f2e6a.svg) | 投影方向数32、每组样本数2048、有限方向平均经验距离；单位与坐标一致。 |

一维目标(0,2)、生成(1,3)，排序后平均距离为(|0−1|+|2−3|)/2=1。二维时先沿一个方向投影再做同样计算，最后对方向平均。这里方向均匀覆盖0到π；目标点和生成点使用相同数量。这个独立指标与神经critic的评分差属于不同估计过程。

![每50次生成器更新记录一次有效比例、32方向投影距离和生成器损失。测试目标集与评估噪声固定。WGAN每个生成步骤使用五次critic更新，其余一次；两种生成损失定义不同。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6a93060c47af23baa12d49d0.svg?v=6a93060c47af)

图 6每50次生成器更新记录一次有效比例、32方向投影距离和生成器损失。测试目标集与评估噪声固定。WGAN每个生成步骤使用五次critic更新，其余一次；两种生成损失定义不同。

图像研究中常用FID在固定特征空间比较均值与协方差。它把特征分布近似成高斯，再计算两个高斯之间的距离；特征提取网络、预处理与样本数都会进入评价条件。本章有一个能手算的提醒：半径2圆周上的八个等权中心，与只保留四个轴向中心的分布，均值都是零，协方差都是2倍单位矩阵。仅比较这两项会得到相同的高斯近似，尽管后者缺了四个模式。代码核对了协方差相同，因此样本图、覆盖、重复和分布指标各有需要回答的问题。

## 完整实验：同时保留样本、梯度和预算

二维实验固定4096个训练点、2048个独立测试点，三种模型各进行1500次生成器更新。普通GAN与条件模型每次配一次判别更新，WGAN-GP配五次；二维模型都使用64单元的两个隐藏层和相同的平滑输出范围。条件模型额外获得簇标签与配对L1训练信号，学习率和目标在代码中分别列明。图像实验单独训练卷积模型，噪声维数、图像划分和生成接触表的固定随机输入也全部保存。这样可以追溯每项结果使用了哪些信息与计算。

### 完整Python：四种真实对抗训练实验

运行python main.py --output results --language zh。依赖NumPy、Matplotlib、scikit-learn与PyTorch，不下载模型权重。程序训练GAN、WGAN-GP、cGAN+L1和小型DCGAN，输出五幅SVG、summary.json、完整数据、权重与每50步的回放数据。

```
"""Train ordinary GAN, WGAN-GP, a conditional GAN, and a tiny image DCGAN.
Synthetic mixture samples are generated here; images are sklearn's UCI digits.
"""
from pathlib import Path
import argparse,json,platform,copy,time
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
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none','axes.titleweight':'bold'})
def save(fig,name):fig.savefig(out/f'{name}-{a.language}.svg',bbox_inches='tight');plt.close(fig)
angles=np.arange(8)*np.pi/4;centers=np.c_[2*np.cos(angles),2*np.sin(angles)].astype('float32')
def mixture(n,seed):
 r=np.random.default_rng(seed);labels=r.integers(0,8,n);return (centers[labels]+r.normal(0,.08,(n,2))).astype('float32'),labels
train,labels=mixture(4096,180);test,testlabels=mixture(2048,181);xt=torch.tensor(train);lab=torch.tensor(labels)
zg=torch.Generator().manual_seed(182);fixed=torch.randn((2048,2),generator=zg);tracez=fixed[:128]
class Generator(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(10 if conditional else 2,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU(),nn.Linear(64,2))
 def forward(self,z,c=None):return 3*torch.tanh(self.net(torch.cat([z,F.one_hot(c,8).float()],1) if self.conditional else z)/3)
class Critic(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(10 if conditional else 2,64),nn.LeakyReLU(.2),nn.Linear(64,64),nn.LeakyReLU(.2),nn.Linear(64,1))
 def forward(self,x,c=None):return self.net(torch.cat([x,F.one_hot(c,8).float()],1) if self.conditional else x).squeeze(1)
def measures(fake):
 dist=np.linalg.norm(fake[:,None]-centers[None],axis=2);nearest=dist.argmin(1);valid=dist.min(1)<.24;counts=np.bincount(nearest[valid],minlength=8);prob=counts/max(1,counts.sum())
 directions=np.c_[np.cos(np.linspace(0,np.pi,32,endpoint=False)),np.sin(np.linspace(0,np.pi,32,endpoint=False))]
 sliced=float(np.mean(np.abs(np.sort(fake@directions.T,axis=0)-np.sort(test@directions.T,axis=0))))
 return dict(valid_fraction=float(valid.mean()),covered_modes=int((counts>=.01*len(fake)).sum()),mode_counts=counts.tolist(),mode_entropy=float(-(prob[prob>0]*np.log(prob[prob>0])).sum()),sliced_w1=sliced)
gridx=np.linspace(-3,3,31);gx,gy=np.meshgrid(gridx,gridx);grid=torch.tensor(np.c_[gx.ravel(),gy.ravel()],dtype=torch.float32)
models={};metrics={};histories={};snapshots={};times={};final_samples={}
for name in ['gan','wgan','conditional']:
 start=time.perf_counter();cond=name=='conditional';torch.manual_seed(183);g=Generator(cond);d=Critic(cond)
 lr=.0002 if name in ['wgan','conditional'] else .0005;betas=(0.,.9) if name=='wgan' else (.5,.9)
 go=torch.optim.Adam(g.parameters(),lr=lr,betas=betas);do=torch.optim.Adam(d.parameters(),lr=lr,betas=betas);rng=torch.Generator().manual_seed(184);history=[];frames=[]
 def snapshot(step):
  with torch.no_grad():
   c=torch.arange(len(fixed))%8 if cond else None;fake=g(fixed,c).numpy();m=measures(fake)
   values=d(grid,torch.zeros(len(grid),dtype=torch.long) if cond else None)
   if name!='wgan':values=values.sigmoid()
   frames.append(dict(step=step,samples=fake[:128].tolist(),field=values.numpy().reshape(31,31).tolist(),metrics=m));return m
 snapshot(0)
 for step in range(1,1501):
  ncritic=5 if name=='wgan' else 1
  for _ in range(ncritic):
   ids=torch.randint(len(xt),(128,),generator=rng);real=xt[ids];c=lab[ids] if cond else None
   fake=g(torch.randn((128,2),generator=rng),c).detach()
   if name=='wgan':
    t=torch.rand((128,1),generator=rng);mix=(t*real+(1-t)*fake).requires_grad_();s=d(mix);grad=torch.autograd.grad(s.sum(),mix,create_graph=True)[0];penalty=(grad.norm(dim=1)-1).square().mean();dl=d(fake).mean()-d(real).mean()+10*penalty
   else:dl=F.softplus(-d(real,c)).mean()+F.softplus(d(fake,c)).mean();penalty=torch.tensor(0.)
   do.zero_grad();dl.backward();do.step()
  for par in d.parameters():par.requires_grad_(False)
  pair_ids=torch.randint(len(xt),(128,),generator=rng) if cond else None
  c=lab[pair_ids] if cond else None;fake=g(torch.randn((128,2),generator=rng),c)
  gl=-d(fake).mean() if name=='wgan' else F.softplus(-d(fake,c)).mean()
  if cond:gl=gl+10*F.l1_loss(fake,xt[pair_ids])
  go.zero_grad();gl.backward();go.step()
  for par in d.parameters():par.requires_grad_(True)
  if step%50==0:
   m=snapshot(step);history.append([step,dl.item(),gl.item(),penalty.item(),m['valid_fraction'],m['sliced_w1']])
 with torch.no_grad():
  c=torch.arange(len(fixed))%8 if cond else None;fake=g(fixed,c).numpy();metrics[name]=measures(fake);final_samples[name]=fake.copy()
  if cond:
   metrics[name]['condition_match']=float((np.linalg.norm(fake[:,None]-centers[None],axis=2).argmin(1)==c.numpy()).mean())
   metrics[name]['within_class_std']=float(np.sqrt(np.mean([np.var(fake[c.numpy()==k],axis=0).mean() for k in range(8)])))
   metrics[name]['paired_l1_weight']=10
 metrics[name].update(generator_updates=1500,critic_updates=1500*(5 if name=='wgan' else 1),generator_parameters=sum(p.numel() for p in g.parameters()),critic_parameters=sum(p.numel() for p in d.parameters()),final_gradient_penalty=history[-1][3])
 models[name]=(g,d);histories[name]=np.array(history);snapshots[name]=frames;times[name]=time.perf_counter()-start
 torch.save(dict(generator=g.state_dict(),critic=d.state_dict()),out/f'{name}.pt')

# Tiny DCGAN: latent8 -> (32,2,2) -> (16,4,4) -> (1,8,8).
digits=load_digits();images=torch.tensor((digits.images/8-1).astype('float32'))[:,None]
image_train,image_test=train_test_split(np.arange(len(images)),test_size=360,stratify=digits.target,random_state=185)
class ImageGenerator(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(8,128),nn.Unflatten(1,(32,2,2)),nn.BatchNorm2d(32),nn.ReLU(),nn.ConvTranspose2d(32,16,4,2,1,bias=False),nn.BatchNorm2d(16),nn.ReLU(),nn.ConvTranspose2d(16,1,4,2,1),nn.Tanh())
 def forward(self,z):return self.net(z)
class ImageDiscriminator(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Conv2d(1,16,4,2,1),nn.LeakyReLU(.2),nn.Conv2d(16,32,4,2,1),nn.LeakyReLU(.2),nn.Flatten(),nn.Linear(128,1))
 def forward(self,x):return self.net(x).squeeze(1)
torch.manual_seed(186);ig=ImageGenerator();idd=ImageDiscriminator();igo=torch.optim.Adam(ig.parameters(),lr=.0002,betas=(.5,.999));ido=torch.optim.Adam(idd.parameters(),lr=.0002,betas=(.5,.999));rng=torch.Generator().manual_seed(187);igfixed=torch.randn((60,8),generator=rng);image_history=[]
for step in range(1,1201):
 ids=torch.randint(len(image_train),(64,),generator=rng);real=images[image_train[ids]];fake=ig(torch.randn((64,8),generator=rng)).detach();dl=F.softplus(-idd(real)).mean()+F.softplus(idd(fake)).mean();ido.zero_grad();dl.backward();ido.step()
 for par in idd.parameters():par.requires_grad_(False)
 fake=ig(torch.randn((64,8),generator=rng));gl=F.softplus(-idd(fake)).mean();igo.zero_grad();gl.backward();igo.step()
 for par in idd.parameters():par.requires_grad_(True)
 if step%50==0:image_history.append([step,dl.item(),gl.item()])
ig.eval()
with torch.no_grad(): generated=((ig(igfixed)+1)/2).numpy()[:,0]
torch.save(dict(generator=ig.state_dict(),discriminator=idd.state_dict()),out/'dcgan.pt')
# A transposed convolution with all-one input/kernel makes overlap counts explicit.
overlap3=F.conv_transpose2d(torch.ones(1,1,4,4),torch.ones(1,1,3,3),stride=2).numpy()[0,0]
overlap4=F.conv_transpose2d(torch.ones(1,1,4,4),torch.ones(1,1,4,4),stride=2).numpy()[0,0]
fig,axs=plt.subplots(2,3,figsize=(12,7.6),layout='constrained')
for col,name in enumerate(['gan','wgan','conditional']):
 fake=np.array(snapshots[name][-1]['samples']);field=np.array(snapshots[name][-1]['field']);ax=axs[0,col]
 if name!='conditional':im=ax.contourf(gx,gy,field,levels=15,cmap='PuBuGn',alpha=.5);fig.colorbar(im,ax=ax,fraction=.045,label=tr('评分','Score') if name=='wgan' else 'P(real)')
 ax.scatter(test[:300,0],test[:300,1],s=6,c='#ba783f',alpha=.45,label=tr('目标','Target'));ax.scatter(fake[:,0],fake[:,1],s=8,c='#125f82',label=tr('生成','Generated'));ax.set(xlim=(-3,3),ylim=(-3,3),xlabel='x1',ylabel='x2',title='cGAN + L1' if name=='conditional' else name.upper());ax.set_aspect('equal');ax.legend(fontsize=8)
 axs[1,col].bar(np.arange(8),metrics[name]['mode_counts'],color='#125f82');axs[1,col].axhline(2048/8,color='#b85d30',ls='--',label=tr('均匀期望','Uniform expectation'));axs[1,col].set(xlabel=tr('模式编号','Mode index'),ylabel=tr('有效生成点数','Valid generated count'),title=tr('覆盖 ','Coverage ')+f"{metrics[name]['covered_modes']}/8; "+tr('有效 ','valid ')+f"{metrics[name]['valid_fraction']:.1%}");axs[1,col].set_xticks(range(8))
save(fig,'distribution')
fig,axs=plt.subplots(2,4,figsize=(13,6.8),layout='constrained')
for row,name in enumerate(['gan','wgan']):
 for col,step in enumerate([0,300,750,1500]):
  frame=snapshots[name][step//50];fake=np.array(frame['samples']);ax=axs[row,col];ax.scatter(test[:300,0],test[:300,1],s=4,c='#b87941',alpha=.4);ax.scatter(fake[:,0],fake[:,1],s=7,c='#125f82');ax.set(xlim=(-3,3),ylim=(-3,3),title=f'{name.upper()} / {step}',xlabel='x1',ylabel='x2');ax.set_aspect('equal')
save(fig,'training')
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for name,color in [('gan','#125f82'),('wgan','#b85d30'),('conditional','#658248')]:
 h=histories[name];label='cGAN + L1' if name=='conditional' else name;axs[0].plot(h[:,0],h[:,4],color=color,label=label);axs[1].plot(h[:,0],h[:,5],color=color,label=label)
axs[0].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('有效样本比例','Valid fraction'),ylim=(0,1),title=tr('A  落在目标邻域内','A  Within target neighborhoods'));axs[0].legend(fontsize=9)
axs[1].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('32方向平均投影W1','Mean projected W1, 32 directions'),title=tr('B  同时观察位置与质量分配','B  Position and mass distribution'))
for name,color in [('gan','#125f82'),('wgan','#b85d30')]:
 h=histories[name];axs[2].plot(h[:,0],h[:,2],color=color,label=name)
axs[2].set(xlabel=tr('生成器更新数','Generator updates'),ylabel=tr('各自定义的G损失','G loss under its own objective'),title=tr('C  两种损失具有不同含义','C  Losses have different meanings'));axs[2].legend(fontsize=9);save(fig,'metrics')
fig=plt.figure(figsize=(13,8));gs=fig.add_gridspec(2,1,height_ratios=[1,1.25],hspace=.27)
top=gs[0].subgridspec(2,10,wspace=.05,hspace=.1)
for i in range(20):
 ax=fig.add_subplot(top[i//10,i%10]);ax.imshow((images[image_test[i],0]+1)/2,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('独立保留图像','Held-out images'),loc='left',fontsize=12)
bottom=gs[1].subgridspec(5,12,wspace=.04,hspace=.08)
for i,img in enumerate(generated):
 ax=fig.add_subplot(bottom[i//12,i%12]);ax.imshow(img,cmap='gray_r',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
 if i==0:ax.set_title(tr('DCGAN：固定60个噪声，1200次更新','DCGAN: 60 fixed inputs after 1,200 updates'),loc='left',fontsize=12)
save(fig,'dcgan')
fig,axs=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
for ax,img,k in zip(axs,[overlap3,overlap4],[3,4]):
 im=ax.imshow(img,vmin=0,vmax=4,cmap='YlGnBu');ax.set_title(f'kernel={k}, stride=2');ax.set(xlabel=tr('输出列','Output column'),ylabel=tr('输出行','Output row'));fig.colorbar(im,ax=ax,ticks=range(5),label=tr('覆盖次数','Overlap count'))
 for r in range(len(img)):
  for c in range(len(img)):ax.text(c,r,int(img[r,c]),ha='center',va='center',fontsize=9,color='white' if img[r,c]>2 else '#152d3a')
save(fig,'overlap')
logit=torch.tensor(np.log(.01/.99),dtype=torch.float64,requires_grad=True);saturating=F.logsigmoid(-logit);nonsaturating=F.softplus(-logit)
gsat=torch.autograd.grad(saturating,logit,retain_graph=True)[0].item();gnon=torch.autograd.grad(nonsaturating,logit)[0].item()
moment_error=float(np.max(np.abs(np.cov(centers.T,bias=True)-np.cov(centers[::2].T,bias=True))))
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,test=2048,modes=8,radius=2,std=.08,valid_radius=.24,generator_bound=3),metrics=metrics,
 dcgan=dict(train=len(image_train),test=len(image_test),updates=1200,generated=60,generator_parameters=sum(p.numel() for p in ig.parameters()),discriminator_parameters=sum(p.numel() for p in idd.parameters())),
 hand=dict(discriminator_loss=float(-2*np.log(.8)),saturating_gradient=gsat,nonsaturating_gradient=gnon,gradient_norm=float(np.linalg.norm([3,4])),gradient_penalty=float((np.linalg.norm([3,4])-1)**2),transpose_size_k3=int(overlap3.shape[0]),transpose_size_k4=int(overlap4.shape[0]),eight_vs_four_covariance_error=moment_error),runtime_seconds=times)
(out/'replay.json').write_text(json.dumps(dict(centers=centers.tolist(),real=test[:160].tolist(),grid=gridx.tolist(),models={n:snapshots[n] for n in ['gan','wgan']}),separators=(',',':')),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',train=train,test=test,labels=labels,fixed_latents=fixed.numpy(),conditional_requests=np.arange(len(fixed))%8,image_train_indices=image_train,image_test_indices=image_test,generated_images=generated,image_history=image_history,overlap3=overlap3,overlap4=overlap4,**{n+'_final':v for n,v in final_samples.items()},**{n+'_history':h for n,h in histories.items()})
with np.load(out/'experiment.npz') as saved:
 summary['saved_data']={}
 for name in ['gan','wgan','conditional']:
  restored=saved[name+'_final'];recomputed=measures(restored)
  summary['saved_data'][name]=dict(rows=len(restored),coordinate_max_error=float(np.max(np.abs(restored-final_samples[name]))),valid_error=abs(recomputed['valid_fraction']-metrics[name]['valid_fraction']),mode_counts_match=recomputed['mode_counts']==metrics[name]['mode_counts'],sliced_w1_error=abs(recomputed['sliced_w1']-metrics[name]['sliced_w1']))
 requests=saved['conditional_requests'];restored=saved['conditional_final'];std=float(np.sqrt(np.mean([np.var(restored[requests==k],axis=0).mean() for k in range(8)])))
 summary['saved_data']['conditional'].update(request_counts=np.bincount(requests,minlength=8).tolist(),within_class_std_error=abs(std-metrics['conditional']['within_class_std']))
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

检查代码时，先跟随一次判别更新中的detach，再跟随一次生成更新中穿过固定判别器的梯度；随后用0.01概率手算两种生成损失的梯度，最后看覆盖次数图怎样对应转置卷积。运行结果同时保存模型、每50步的实际快照、评价曲线和完整数据。若要改变训练配比或损失权重，沿用同一批固定噪声与测试点最容易看清变化。生成任务中的学习信号、图像结构和评价定义在这里彼此相连，任何一项改变都应在对应的可见结果中留下痕迹。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M18.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661)

   原始对抗目标、最优判别器与生成器学习。

   Primary paper; no figure copied
2. [GAN Lab](https://poloclub.github.io/ganlab/)

   二维训练动态原动画与开源实现。

   Apache 2.0; license retained; repository root has no NOTICE file
3. [DCGAN](https://arxiv.org/abs/1511.06434)

   卷积生成器与判别器的结构。

   Primary paper; no figure copied
4. [Wasserstein GAN](https://arxiv.org/abs/1701.07875)

   分布距离与Lipschitz critic。

   Primary paper; no figure copied
5. [Improved Training of Wasserstein GANs](https://arxiv.org/abs/1704.00028)

   输入梯度惩罚。

   Primary paper; no figure copied
6. [Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784)

   条件同时进入两侧网络。

   Primary paper; no figure copied
7. [Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)

   pix2pix、PatchGAN与配对L1。

   Primary paper; no figure copied
8. [Deconvolution and Checkerboard Artifacts](https://distill.pub/2016/deconv-checkerboard/)

   不均匀重叠的机制；本章图由实际卷积另绘。

   CC BY 4.0 reference; original images not copied
9. [GANs Trained by a Two Time-Scale Update Rule](https://arxiv.org/abs/1706.08500)

   两侧更新速度与FID定义。

   Primary paper; no figure copied
10. [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

    图像数据与许可。

    CC BY 4.0; E. Alpaydin and C. Kaynak
