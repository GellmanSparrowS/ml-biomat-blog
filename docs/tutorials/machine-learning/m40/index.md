# 低谷里有多少概率：能量模型、Score Matching与采样

Source: https://ml-biomat.com/tutorials/machine-learning/m40/
Language: zh-CN

从能量差算到概率，再用真实训练与随机链区分模型形状、概率质量和采样覆盖。

## 画一张地形图，让样本知道哪里值得停留

挑选一把椅子时，我们会同时考虑承重、舒适、尺寸和外观，很难把所有要求写成一个唯一答案，却可以给不同方案一个比较分数。能量模型也采用类似思路：给每个候选样本计算一个能量值，合理样本处在较低的位置，较少出现的样本处在较高的位置。对图像，样本是整幅像素数组；对动作，样本可以是一段关节轨迹。网络先学会评价整个候选，随后通过搜索或随机采样提出新的候选。

把能量想象成地形，有助于理解下一步怎样移动：坡度给出下坡方向，低谷对应较高概率区域。不过，采样的任务包含“按概率出现”这层要求。若只让小球一直下坡，它会停在谷底附近，得到一组几乎相同的答案。随机扰动让粒子在低谷周围活动，也使它有机会越过山脊访问另一片区域。能量形状与探索过程共同决定最后能看到什么。

统计物理用能量和温度描述许多微观状态的相对出现机会，机器学习继承了这种把整体约束写成标量函数的办法。本章先把能量与概率的区别算清，再训练一个真实神经能量模型。数据包含四团大小不同的点；正确模型既要找到四个低谷，也要学会在它们之间分配概率。这个小问题足以看见配分函数、负样本、链的混合和score之间的关系。

![神经能量采样从随机像素逐步形成数字的迭代序列。](https://ml-biomat.com/static/tutorials/machine-learning/figures/1529524c00b765789b492048.svg?v=1529524c00b7)

图 1UvA Deep Learning Tutorials的原始神经能量模型采样输出：从随机像素初始化，沿图中迭代顺序逐渐形成数字结构。Phillip Lippe与教程贡献者，MIT许可，原始Notebook生成图，未改动。图像展示该教程的MNIST实验；本章随后单独训练二维模型来检查概率质量。

## 能量变成概率，还差一个总账

能量可以是正数，也可以是负数，不能直接拿它当概率。先取负号再做指数，便得到正的权重；能量越低，权重越大。随后要把所有可能状态的权重合起来，再用每个状态的权重除以这个总量。这个总量叫配分函数。离散状态使用求和，连续坐标使用积分。它保证的是总概率为1，而连续密度在某个位置可以大于1，因为真正的概率还需要乘上邻近区域的大小。

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},\qquad Z_\theta=\int e^{-E_\theta(u)}\,du
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/450ec5d073fe8ccb5c2ec2a1.svg) | 样本坐标、积分用的占位坐标和网络参数；本例x、u为二维无量纲向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c7a2d1fed05fbe504fca30c8.svg) | 标量无量纲能量、自然指数底、配分函数和密度；有量纲坐标下密度单位为坐标体积倒数。 |

积分把全部正权重合起来，所以密度再积分恰好等于1；离散状态把积分换成求和。能量0和ln2给出权重1与1/2，总和3/2，概率2/3与1/3。物理能量U若以焦耳计，须先除以k_B T成为无量纲E；k_B是玻尔兹曼常数，T是绝对温度。本例网络能量没有焦耳单位。

例如两个离散状态的能量分别为0与ln2，权重就是1与1/2，归一化后概率为2/3与1/3。若把两个能量都加上7，两个权重同时乘上e^{−7}，总量也乘上相同因子，最终概率不变。可见绝对能量零点可以移动，真正影响相对概率的是能量差。绘制不同模型的地形时，先减去各自最小能量可以方便看形状，但这些相对高度不能代替各自的归一化概率。

连续空间的困难来自状态数量。二维小网格可以把每个小格的权重加起来；若一幅图有数千个像素，每个像素又有许多可能取值，逐个枚举就会迅速失去可行性。灵活的能量网络让我们容易计算某个候选的分数，却没有自动给出整个空间的总账。后面的训练与采样方法，正是围绕怎样利用局部计算、同时处理这份全局归一化要求展开的。

低谷的深度与宽度还需要一起看。设两个互不重叠的小区域内能量近似不变，第一个区域能量为0、面积为1，第二个能量为ln2、面积为4。前者的总权重约为1，后者虽然位置更高，总权重却约为2，因此归一化后第二个区域占2/3的概率。地形图中最深的那个点无法独自回答“样本最常落在哪一片”。高维空间里，可容纳状态的体积同样重要；这也是看见几个漂亮的谷底以后，还要用积分或区域频率检查概率质量的原因。

物理图景中的温度提供了另一种理解。若真实能量差保持不变，提高温度会减小无量纲能量差，让不同状态的权重更接近；降低温度则更偏向低能量状态。机器学习通常把这个尺度吸收到网络输出中，本章固定这一约定，所以数值能量没有焦耳单位。若生成时另外将能量除以一个温度参数，就等于选择了一种新的概率分布。步长改变的是离散采样过程；温度改变的是目标权重，两者需要分别设置和说明。

## 训练为什么既要看真实样本，也要看模型自己相信的样本

最大似然希望真实数据获得较高概率。把能量概率代入负对数后，会出现两项：真实样本的能量，以及配分函数的对数。只降低真实样本能量还不够，因为网络可能把其他地方也一起降低，使总权重同步增加。对完整目标求参数梯度，会得到真实数据上的平均梯度减去模型分布上的平均梯度。这两部分常被叫作正相和负相。

$$
L(\theta)=\mathbb E_{p_{\rm data}}[E_\theta(x)]+\log Z_\theta,\qquad \nabla_\theta L=\mathbb E_{p_{\rm data}}[\nabla_\theta E_\theta(x)]-\mathbb E_{p_\theta}[\nabla_\theta E_\theta(x)]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a07fca8b0d4692ec528a5732.svg) | 平均负对数密度、自然对数和按下标分布取平均；固定坐标单位时L以nats计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a8443011abc65f8fca430718.svg) | 数据分布、当前模型分布、输入样本与参数向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cd215d0ce220d9e9827a8a4f.svg) | 标量能量、配分函数与对参数求梯度；梯度形状与参数相同。 |

对Z求导产生−∇E乘e^(−E)，再除以Z就成为模型分布平均，得到负号。两状态模型E(0)=0、E(1)=θ时，数据中状态1占0.8，θ=0时模型给0.5，梯度0.8−0.5=0.3；梯度下降把θ减小，让状态1能量下降、概率增加。

正相把真实样本附近的能量往下拉；负相则从模型当前分布取样，对它过度偏爱的区域施加反向调整。“负样本”因此不是人工标注的错误答案，也不必长得荒谬，它是模型自己正在给予概率的候选。如果负样本只来自某一个低谷，训练就难以知道其他低谷分走了多少概率。采样器的覆盖会直接进入参数更新，而不只是影响最后展示的几张生成图。

低维时可以把这个过程完整展开。本章的一种训练方式直接在48×48网格上累加权重，近似计算窗口内配分函数，因此正相与负相都能通过自动微分得到。另一种方式用持续运行的随机链近似负相。它们使用同一类网络、同一份训练数据，再用更密网格计算统一的验证指标。这样可以观察差别来自哪里，而不是用两套含义不同的训练损失直接比较高低。

## 下坡加随机步：Langevin与接受修正

Langevin采样每一步做两件事：沿负能量梯度移动，再加入高斯随机扰动。梯度告诉它哪个方向概率增大，噪声则保持探索。两部分的尺度要匹配：采用本章的约定，确定移动乘步长，噪声标准差取两倍步长的平方根。若任意改变噪声幅度而不改变其余部分，长期分布也会改变。把噪声关掉得到的是寻找低能量位置的优化过程，采样则需要保留合适的波动。

$$
x_{k+1}=x_k-h\nabla_xE_\theta(x_k)+\sqrt{2h}\,\xi_k,\qquad \xi_k\sim\mathcal N(0,I_d)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9338ef5dbb88926a09481bfd.svg) | 第k步d维位置、离散步索引和维度；本例d=2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9767612e4b8e0ed0506d92bf.svg) | 正步长、位置梯度、各步独立的标准高斯d向量和d阶单位阵；本例坐标与算法时间无量纲。 |

梯度漂移与噪声方差2h匹配。对E=x²/2，更新是(1−h)x+√(2h)ξ；平稳方差V满足V=(1−h)²V+2h，因此0<h<2时V=1/(1−h/2)。h=0.1给1.05263，而目标方差为1。取x=1、噪声ξ=0时，一步位置为0.9；有随机噪声时单步也可以向高能量移动。

连续时间的Langevin过程与目标密度有明确联系，有限步长的离散实现却会引入偏差。这个未经接受修正的版本通常称ULA。对标准高斯目标，能量梯度等于位置，离散更新是一种线性递推；步长越大，平稳方差会偏离目标。较大步长可以让粒子更快穿过空间，也可能把低谷附近的云团撑得过宽，甚至使迭代不稳定。步长既控制速度，也改变数值性质。

MALA在同样的Langevin提议后，加一个Metropolis–Hastings接受步骤。它同时比较能量变化和两个方向的提议概率，使目标密度成为理想精确计算下的平稳分布。提议若被拒绝，链保留原位置，这个重复位置也是一个有效采样状态。接受率很高可能只是步子很小；接受修正解决离散平稳分布的问题，有限时间内跨越多个低谷的速度仍需要另外检查。

$$
q(y\mid x)=\mathcal N\!\left(y;x-h\nabla E(x),2hI_d\right),\qquad A(x,y)=\min\!\left(1,\frac{e^{-E(y)}q(x\mid y)}{e^{-E(x)}q(y\mid x)}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/13679622cab1185145edc120.svg) | 当前状态、提议状态、步长、维度与单位阵；x和y均为d向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/73a565bd58b87235bebdcfa6.svg) | 正向与反向提议密度、均值m和协方差C的高斯密度在y处的值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b32948f4104447a4407a7661.svg) | 能量、位置梯度、0至1的接受概率和取较小值；配分函数在比值中消去。 |

用独立0至1均匀数与A比较，接受则移动，拒绝则重复原状态。E=x²/2、x=0、y=1、h=0.1时，能量差为0.5，正向与反向高斯指数成本为2.5和2.025，log接受比为−0.5+2.5−2.025=−0.025，接受概率约0.97531。梯度提议不对称，因此反向q不能省略。

为什么还要比较反方向？站在坡上时，下坡提议的均值会向谷底偏移，所以“从这里提议那里”和“从那里提议这里”一般不一样容易。若只看能量差，便会把这种提议本身的偏好再算一遍。接受比用反向密度补偿这份不对称，使两点之间的平衡概率流匹配。计算时可以在对数空间相减，避免极小概率相除；真正需要的只是两个位置的能量和梯度，归一化总量会消去。

## 短链、持续链，以及它们怎样改变训练

2000年前后的Contrastive Divergence工作为难以运行到平衡的模型提供了短链训练思路。CD-k从真实数据出发，运行k步当前模型的采样，再把结果作为负相近似。起点离数据近，少量步骤就能提供有用的局部变化信息；与此同时，短链分布仍依赖真实数据起点，通常不同于模型的平稳分布。CD更新一般也会停止对采样路径反向传播，把生成的负样本当作本次梯度估计中的固定输入。

$$
E_a(x)=\tfrac12ax^2,\qquad V_{\rm after}=(1-ha)^2V_{\rm data}+2h,\qquad a_{\rm CD1}=\frac{1-\sqrt{1-2h/V_{\rm data}}}{h}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dedaa4c24fe65cc4d1ba6815.svg) | 正精度参数、标量能量和一维位置；模型方差为1/a。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b2c3ec66990d565b9912ff10.svg) | ULA步长、零均值数据的方差和一次更新后方差；本例均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eba6a38c1ebd54119c5fb882.svg) | 令数据方差等于一步负样本方差的低精度根；要求1−2h/V_data非负。 |

能量对a的导数是x²/2，CD梯度为前后方差差的一半；令它为0后解二次式得到所示根。V_data=1、h=0.1给a≈1.055728、模型方差≈0.947214。这个固定点属于“从数据开始的一步ULA”更新，和真实最大似然精度1不同。

一个高斯算例可以把这种差别看得很清楚。真实数据方差为1，模型能量用一个可调精度乘位置平方的一半。采用步长0.1的一步ULA作为CD负样本时，令前后方差相同得到的精度约为1.05573，对应模型密度方差约0.94721。程序用20万个真实样本执行这一更新，输出方差约1.00075。有限一步样本看起来接近数据方差，模型定义的密度却已有偏移；这是采样步骤与训练固定点耦合的具体例子。

持续对比散度保留上一次的链状态，让下一次参数更新从已有候选继续走。本例的PCD20维护1,024个状态，每次取128个，走20步、步长0.02，再放回缓存，其中5%用新的高斯状态重启。这个重启有助于探索，也让实际负相成为一套明确的有限链近似。2019年的神经能量模型工作将样本缓存与梯度采样结合，用于更复杂的图像与轨迹；它背后的计算问题在这四个低谷上同样存在。

缓存中的状态也会随训练逐渐“变旧”，因为每次更新参数后，地形已经有所改变。持续链希望利用已有位置继续追踪新分布，效果取决于参数移动速度与链探索速度是否匹配。代码先固定当前网络生成负样本，再把这些坐标从采样计算图中分离，最后对它们的能量求参数梯度。这样对应公式中的“在当前模型分布下平均能量梯度”。若直接沿有限采样路径一起反向传播，会额外加入采样位置随参数变化的导数，得到另一种更新目标；它并非此处最大似然负相估计所要求的操作。

## 不先求总账，也能学习局部方向吗

对数密度对位置求梯度，配分函数会消失，因为它只依赖模型参数，不依赖当前样本位置。这个位置梯度叫score，对能量模型而言恰好等于负能量梯度。二维输入对应两个方向分量，图像输入对应每个像素的方向。这里要把两种求导分开：训练最大似然对参数求导时，配分函数不能丢；求样本移动方向时，才可以利用它对位置为常数的性质。

$$
s_\theta(x)=\nabla_x\log p_\theta(x)=-\nabla_xE_\theta(x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/323707e7bd0b4d5427a86d8d.svg) | score向量、d维样本与模型参数；score有d个分量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e3a619cc3dfeb4f60937fd04.svg) | 密度、无量纲能量、对位置求梯度和自然对数；有量纲坐标下score单位为坐标倒数。 |

log p=−E−logZ，对x求导时logZ是常数。标准高斯在x=2处score为−2，指向0；方差4的高斯在同一点score为−0.5，因为宽分布的相对密度变化更缓。score不是概率，向量长度也不直接给概率大小。

2005年的Score Matching进一步研究，能否直接让模型的方向场贴近真实数据的方向场。真实score未知，但在边界项消失等条件下，通过分部积分，可以把目标改写成只需要数据样本、模型score及其散度的形式。这个改写绕过了对配分函数的显式求值。若score来自一个标量能量的梯度，方向场自动满足相应的梯度结构；任意预测向量的网络则需要按所采用模型检查它与概率密度的联系。

$$
J(\theta)=\mathbb E_{p_{\rm data}}\!\left[\tfrac12\|s_\theta(x)\|^2+\nabla_x\cdot s_\theta(x)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7c451a648435d5ef8afa031d.svg) | 去掉与参数无关常数后的Score Matching目标与数据平均；J可为负。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7342c62a4d51a2e06ca208e9.svg) | d维score、模型参数、d维位置和分量平方和。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f356b92922d2e360cc410073.svg) | 散度，即各分量对同名坐标的偏导之和；与score平方同为坐标倒数平方单位。 |

从真实score与模型score的平方距离展开，交叉项经分部积分变成模型散度；需要足够光滑、可积且边界项消失。一维s=−ax、数据方差V时，J=a²V/2−a，求导得aV−1，最优a=1/V。V=4时a=0.25，无需先算Z。

去噪Score Matching提供了更容易制造标签的办法。给干净样本加一份已知高斯噪声，带噪样本相对于该干净样本的条件score可以直接算出，再用平方误差训练网络。最优条件平均对应的是加噪后平滑分布的score。2011年关于去噪与score matching联系的工作阐明了这条关系，后来多噪声水平的生成方法进一步利用它在不同平滑程度之间移动。

$$
\tilde x=x+\sigma\epsilon,\quad\epsilon\sim\mathcal N(0,I_d),\qquad L_{\rm DSM}=\mathbb E\!\left[\frac1d\left\|s_\theta(\tilde x)+\frac{\epsilon}{\sigma}\right\|^2\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/04e62bfffa527fbd0014154a.svg) | 干净样本、带噪样本、独立标准高斯噪声与维度；前三者为d维向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6166be0d8610833c0bef4930.svg) | 正噪声标准差、在带噪输入处预测的score和参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451a5c7f5f37caedca8b44d7.svg) | 去噪score平方损失、对数据和噪声平均、按坐标平均；单位为score平方。 |

高斯条件密度对带噪位置的梯度为−(x̃−x)/σ²=−ε/σ，标签已知。平方损失的最佳条件均值等于平滑边缘密度score。干净N(0,1)、σ=0.5给带噪N(0,1.25)，score为−0.8x̃。对单个x=1、ε=2，x̃=2、标签−4；网络平均多个可能干净来源后才得到边缘方向。

程序用20万个标准高斯样本加标准差0.5的噪声，带噪方差因此为1.25，真实score斜率为−0.8。只拟合一个线性斜率，就得到约−0.80221，与解析值相近。它比干净分布的斜率−1更缓，原因是加噪让分布变宽。这个算例同时说明，去噪标签可以训练出有意义的边缘方向，也说明固定噪声水平学到的是平滑密度，而非自动恢复了所有干净细节。

## 完整实验：把能量地形与概率质量都画出来

目标包含四个均值在(±1.2,±1.2)的高斯团，每个方向标准差0.32，混合权重依次为0.55、0.25、0.15和0.05。训练、验证、测试分别有4,096、1,024和1,024点，使用独立种子。网络把两个坐标送入两层32单元的双曲正切隐藏层，输出一个标量，再加上坐标平方和的一半，共1,185个参数。这个二次项让远处能量上升，隐藏层的有界输出则提供局部起伏。

![左：已知目标的相对能量三维地形，减去窗口内最小值；中、右：两个真实训练模型的窗口归一化密度，使用独立概率密度色标。橙点是150个固定测试样本。坐标无量纲。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6ccb0520d5762eb5a96998c5.svg?v=6ccb0520d576)

图 2左：已知目标的相对能量三维地形，减去窗口内最小值；中、右：两个真实训练模型的窗口归一化密度，使用独立概率密度色标。橙点是150个固定测试样本。坐标无量纲。

GridMLE与PCD20各训练2,000次更新，分别选中第2,000与第600次的验证最优权重。网格方法在[−4,4]²窗口内计算积分；评价使用160×160中点网格，并再用240×240复核。把窗口扩到[−6,6]²后，两模型的对数配分函数变化约为1.72×10^{−5}与6.29×10^{−5}。这些检查帮助判断当前窗口与网格对这次低维实验是否足够细，也明确了所报告负对数密度的计算范围。

$$
\widehat Z_W=\Delta A\sum_{j=1}^{G^2}e^{-E_\theta(u_j)},\quad\log\widehat Z_W=\log\Delta A+\operatorname{logsumexp}_j[-E_\theta(u_j)],\quad\Delta A=(8/G)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/40325612353eae0022304974.svg) | 积分窗口[−4,4]²、每轴网格数、格点索引和二维中点坐标。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eb70ebc658c338a54a648e45.svg) | 窗口配分函数的中点近似、每个格子的面积和网络能量；Z具有面积单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/61ac3ada8b31d719b9cbd211.svg) | 先指数求和再取自然对数的稳定运算与自然对数。 |

小格内权重近似为中点权重乘面积，累加得到积分。G=48有2304格，每格面积1/36；若整个窗口能量都为0，近似Z=2304/36=64，恰等于窗口面积，归一化密度1/64。logsumexp先减去最大输入再计算，避免直接指数溢出；窗口积分与无限空间积分须区分。

测试窗口负对数密度分别约1.7951与1.9903。GridMLE在四象限分配的质量约为0.5471、0.2518、0.1542和0.0469，PCD20则约为0.6831、0.2004、0.0943和0.0222。两模型都画出了四个低谷，后者却给第一团分配了过多质量。由于高斯尾部会轻微越过坐标轴，程序用高斯分布函数精确计算目标象限概率，再比较质量，而不是把混合权重直接当成完全相同的象限概率。

![左：固定验证集的窗口负对数密度与训练更新。中：已知目标象限质量及两个模型的网格积分质量。右：GridMLE能量下512条MALA链运行1000步后的最终位置，步长0.03；最终点云与模型积分质量分别解释。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e0878cda1776d1373d4fbab3.svg?v=e0878cda1776)

图 3左：固定验证集的窗口负对数密度与训练更新。中：已知目标象限质量及两个模型的网格积分质量。右：GridMLE能量下512条MALA链运行1000步后的最终位置，步长0.03；最终点云与模型积分质量分别解释。

这里的网格积分只适合低维检查。若每个维度取48个点，二维需要2,304个位置，十维就需要48的十次方个位置。高维方法因此依赖采样、结构假设或其他训练目标。本章保留低维网格，是为了能够分别检查模型与采样器，而非把枚举作为一般图像模型的训练办法。完整代码还保存真实目标梯度与有限差分的核对、原始点、网络权重、全部链轨迹和概率质量。

### 完整Python：能量训练、积分与随机链诊断

依赖NumPy、PyTorch和Matplotlib。运行python main.py --output results --language zh，真实训练两套能量网络，并保存原始数据、全部链轨迹、权重、数值摘要和四组科学图。

```
"""Neural energies, positive/negative phases, and honest sampling diagnostics."""
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
centers=np.array([[-1.2,-1.2],[1.2,-1.2],[1.2,1.2],[-1.2,1.2]]);weights=np.array([.55,.25,.15,.05]);sigma=.32;variance=sigma*sigma
signs=np.array([[-1,-1],[1,-1],[1,1],[-1,1]]);quadrant_weights=np.array([sum(w*math.prod(.5*(1+math.erf(float(sign[j]*mu[j])/(sigma*math.sqrt(2)))) for j in range(2)) for w,mu in zip(weights,centers)) for sign in signs])
def sample_data(n,seed):
 r=np.random.default_rng(seed);labels=r.choice(4,n,p=weights);return (centers[labels]+r.normal(0,sigma,(n,2))).astype('float32'),labels
def true_energy_gradient(x):
 delta=x[:,None]-centers[None];logterms=np.log(weights)[None]-np.sum(delta*delta,2)/(2*variance)-math.log(2*math.pi*variance);maximum=logterms.max(1,keepdims=True);responsibility=np.exp(logterms-maximum);total=responsibility.sum(1,keepdims=True);e=-maximum[:,0]-np.log(total[:,0]);responsibility/=total;gradient=(responsibility[:,:,None]*delta).sum(1)/variance;return e,gradient
train,train_labels=sample_data(4096,400);valid,valid_labels=sample_data(1024,401);test,test_labels=sample_data(1024,402);xt=torch.tensor(train)
class Energy(nn.Module):
 def __init__(self):
  super().__init__();self.net=nn.Sequential(nn.Linear(2,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))
 def forward(self,x):return self.net(x).flatten()+.5*x.square().sum(1)
def midpoint_grid(limit,n):
 a=-limit+(np.arange(n)+.5)*(2*limit/n);xx,yy=np.meshgrid(a,a);return np.c_[xx.ravel(),yy.ravel()].astype('float32'),(2*limit/n)**2
grid_train,cell_train=midpoint_grid(4,48);grid_eval,cell_eval=midpoint_grid(4,160);gt=torch.tensor(grid_train);ge=torch.tensor(grid_eval)
def logZ(m,g,cell):return torch.logsumexp(-m(g),0)+math.log(cell)
def langevin_torch(m,x,steps,h,rng):
 for _ in range(steps):
  x=x.detach().requires_grad_(True);gradient=torch.autograd.grad(m(x).sum(),x)[0];x=(x-h*gradient+math.sqrt(2*h)*torch.randn(x.shape,generator=rng)).detach()
 return x
models={};histories={};training={}
for name,seed in [('GridMLE',403),('PCD20',404)]:
 torch.manual_seed(seed);m=Energy();opt=torch.optim.Adam(m.parameters(),lr=.001);rng=torch.Generator().manual_seed(seed+100);buffer=1.5*torch.randn((1024,2),generator=rng);history=[];best=float('inf');best_state=None
 for step in range(1,2001):
  idx=torch.randint(len(xt),(128,),generator=rng);positive=m(xt[idx]);negative_mean=0.
  if name=='GridMLE':loss=positive.mean()+logZ(m,gt,cell_train)
  else:
   ids=torch.randperm(len(buffer),generator=rng)[:128];negative=buffer[ids].clone();restart=torch.rand((128,),generator=rng)<.05;negative[restart]=1.5*torch.randn((int(restart.sum()),2),generator=rng);negative=langevin_torch(m,negative,20,.02,rng);buffer[ids]=negative;negative_energy=m(negative.detach());negative_mean=negative_energy.mean().item();loss=positive.mean()-negative_energy.mean()
  opt.zero_grad();loss.backward();opt.step()
  if step%100==0:
   with torch.no_grad():z=logZ(m,ge,cell_eval);validation_nll=(m(torch.tensor(valid)).mean()+z).item()
   history.append([step,loss.item(),validation_nll,positive.mean().item(),negative_mean])
   if validation_nll<best:best=validation_nll;best_step=step;best_state=copy.deepcopy(m.state_dict())
 m.load_state_dict(best_state);m.eval();models[name]=m;histories[name]=history;training[name]=dict(updates=2000,best_step=best_step,validation_window_nll=best,parameters=sum(p.numel() for p in m.parameters()),seed=seed);torch.save(dict(model=m.state_dict(),best_step=best_step),out/f'{name.lower()}.pt')
def model_eg(m,x):
 a=torch.tensor(x,dtype=torch.float32,requires_grad=True);e=m(a);g=torch.autograd.grad(e.sum(),a)[0];return e.detach().numpy().astype('float64'),g.detach().numpy().astype('float64')
def quadrants(x):return np.where(x[:,1]<0,np.where(x[:,0]<0,0,1),np.where(x[:,0]>0,2,3))
def chain(eg,h,steps,initial,seed,method='ULA',record_every=10):
 rng=np.random.default_rng(seed);x=np.array(initial,dtype='float64');path=[x.copy()];accepted=0;switches=np.zeros(len(x),dtype=int);counts=np.zeros(4,dtype='int64');occupancies=[];e,g=eg(x)
 for step in range(1,steps+1):
  proposal=x-h*g+math.sqrt(2*h)*rng.normal(size=x.shape);pe,pg=eg(proposal)
  if method=='MALA':
   forward=np.sum((proposal-x+h*g)**2,1)/(4*h);backward=np.sum((x-proposal+h*pg)**2,1)/(4*h);logratio=-pe+e+forward-backward;accept=np.log(rng.uniform(size=len(x)))<np.minimum(0,logratio)
  else:accept=np.ones(len(x),dtype=bool)
  previous=quadrants(x);x[accept]=proposal[accept];e[accept]=pe[accept];g[accept]=pg[accept];accepted+=int(accept.sum());switches+=(previous!=quadrants(x))
  if step>steps//2:counts+=np.bincount(quadrants(x),minlength=4)
  if step%record_every==0:path.append(x.copy());occupancies.append(np.bincount(quadrants(x),minlength=4)/len(x))
 return x,np.array(path),dict(acceptance=accepted/(steps*len(x)),final_weights=(np.bincount(quadrants(x),minlength=4)/len(x)).tolist(),second_half_weights=(counts/counts.sum()).tolist(),total_variation=float(.5*np.abs(counts/counts.sum()-quadrant_weights).sum()),chains_ever_switched=float((switches>0).mean()),mean_switches=float(switches.mean()),steps=steps,h=h,method=method),np.array(occupancies)
initials=dict(one=np.repeat(centers[:1],128,axis=0),spread=centers[np.arange(128)%4].copy());runs={};paths={};occupancies={}
for name,h,initial,method in [('small_one',.005,'one','ULA'),('small_spread',.005,'spread','ULA'),('medium_spread',.04,'spread','ULA'),('large_spread',.16,'spread','ULA'),('mala_spread',.16,'spread','MALA')]:
 x,path,stat,occ=chain(true_energy_gradient,h,2000,initials[initial],405,method);runs[name]=stat;paths[name]=path;occupancies[name]=occ
model_stats={};densities={};neural_paths={};neural_samples={};initial_rng=np.random.default_rng(406);neural_initial=initial_rng.normal(0,1.5,(512,2))
for name,m in models.items():
 with torch.no_grad():eg=m(ge).numpy().astype('float64');z=logZ(m,ge,cell_eval).item();density=np.exp(-eg-z);test_nll=float(m(torch.tensor(test)).mean()+z)
 density_weights=np.array([density[quadrants(grid_eval)==c].sum()*cell_eval for c in range(4)]);densities[name]=dict(energy=eg,density=density)
 x,path,stat,_=chain(lambda a:model_eg(m,a),.03,1000,neural_initial,407,'MALA',20);neural_paths[name]=path;neural_samples[name]=x
 extended,extended_cell=midpoint_grid(6,240)
 with torch.no_grad():extended_logz=logZ(m,torch.tensor(extended),extended_cell).item();fine,fc=midpoint_grid(4,240);fine_logz=logZ(m,torch.tensor(fine),fc).item()
 stat['TV_from_model_quadrature']=float(.5*np.abs(np.array(stat['second_half_weights'])-density_weights).sum())
 model_stats[name]=dict(window_test_nll=test_nll,logZ_window=z,normalization_sum=float(density.sum()*cell_eval),quadrant_mass=density_weights.tolist(),quadrant_mass_TV=float(.5*np.abs(density_weights-quadrant_weights).sum()),window_logZ_refinement=abs(fine_logz-z),extended_logZ_difference=extended_logz-z,sampling=stat)
# Analytic CD1 fixed point for a Gaussian energy, and sampled denoising-score regression.
r=np.random.default_rng(408);clean=r.normal(size=200000);eps=r.normal(size=len(clean));noise_sigma=.5;noisy=clean+noise_sigma*eps;dsm_a=float(np.dot(noisy,eps/noise_sigma)/np.dot(noisy,noisy));h=.1;cd_precision=(1-math.sqrt(1-2*h))/h;cd_step=(1-h*cd_precision)*clean+math.sqrt(2*h)*r.normal(size=len(clean));gpoints=np.array([[.3,.7],[-.2,-1.1],[1.3,.9]]);analytic=true_energy_gradient(gpoints)[1];finite=np.empty_like(analytic)
for j in range(2):
 offset=np.zeros_like(gpoints);offset[:,j]=1e-5;finite[:,j]=(true_energy_gradient(gpoints+offset)[0]-true_energy_gradient(gpoints-offset)[0])/(2e-5)
single=np.array([[.5,-.25]]);neural_energy,neural_grad=model_eg(models['GridMLE'],single)
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=1024,weights=weights.tolist(),quadrant_weights=quadrant_weights.tolist(),sigma=sigma,seeds=[400,401,402]),training=training,models=model_stats,known_target_chains=runs,score_matching=dict(noise_sigma=noise_sigma,fit_precision=dsm_a,true_smoothed_precision=.8,samples=len(clean)),hand=dict(two_state_probability=[2/3,1/3],probability_ratio=2.,constant_shift=7.,cd1_precision=cd_precision,cd1_model_variance=1/cd_precision,cd1_actual_step_variance=float(cd_step.var()),true_gradient_max_error=float(np.max(np.abs(analytic-finite))),neural_probe_energy=float(neural_energy[0]),neural_probe_gradient=neural_grad[0].tolist()),domain=dict(training_window=[-4,4],training_grid=48,evaluation_grid=160,refinement_grid=240,extended_window=[-6,6]))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,train_labels=train_labels,validation=valid,test=test,grid=grid_eval,true_density=np.exp(-true_energy_gradient(grid_eval)[0]),clean_score_samples=clean,noisy_score_samples=noisy,score_noise=eps,cd1_samples=cd_step,neural_initial=neural_initial,**{n+'_history':np.array(v) for n,v in histories.items()},**{n+'_energy':d['energy'] for n,d in densities.items()},**{n+'_density':d['density'] for n,d in densities.items()},**{n+'_samples':v for n,v in neural_samples.items()},**{n+'_chain':v for n,v in paths.items()},**{n+'_occupancy':v for n,v in occupancies.items()},**{n+'_neural_chain':v for n,v in neural_paths.items()})
lab_grid,lab_cell=midpoint_grid(4,60);known_e=true_energy_gradient(lab_grid)[0];learned_e=model_eg(models['GridMLE'],lab_grid)[0];lab=dict(centers=centers.tolist(),weights=weights.tolist(),variance=variance,grid=lab_grid.tolist(),cell=lab_cell,quadrant_weights=quadrant_weights.tolist(),learned_quadrant_weights=model_stats['GridMLE']['quadrant_mass'],energies={'True':known_e.tolist(),'Learned':learned_e.tolist()},logZ={'True':0.,'Learned':model_stats['GridMLE']['logZ_window']},network={k:v.detach().numpy().tolist() for k,v in models['GridMLE'].state_dict().items()});(out/'lab-data.json').write_text(json.dumps(lab,separators=(',',':')),encoding='utf-8')
fig=plt.figure(figsize=(13,4.8),layout='constrained');ax=fig.add_subplot(131,projection='3d');small,_=midpoint_grid(3,70);truee=true_energy_gradient(small)[0];xx=small[:,0].reshape(70,70);yy=small[:,1].reshape(70,70);ax.plot_surface(xx,yy,(truee-truee.min()).reshape(70,70),cmap='viridis',linewidth=0,rasterized=True);ax.set(xlabel='x1',ylabel='x2',zlabel='',title=tr('A  已知目标：相对能量','A  Target: relative energy'));ax.view_init(35,-55)
for j,name in enumerate(['GridMLE','PCD20']):
 ax=fig.add_subplot(1,3,j+2);im=ax.imshow(densities[name]['density'].reshape(160,160),origin='lower',extent=(-4,4,-4,4),cmap='YlGnBu',vmin=0,vmax=1);ax.scatter(test[:150,0],test[:150,1],s=3,color='#b96f3b',alpha=.35);ax.set(xlabel='x1',ylabel='x2',title=name+tr('：窗口归一化密度',': window-normalized density'));fig.colorbar(im,ax=ax,label=tr('每单位面积密度','Density per unit area'),shrink=.65)
save(fig,'landscape')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
for name,color in [('GridMLE','#125f82'),('PCD20','#bf7139')]:
 hh=np.array(histories[name]);axs[0].plot(hh[:,0],hh[:,2],label=name,color=color)
axs[0].set(xlabel=tr('参数更新次数','Parameter updates'),ylabel=tr('验证窗口负对数密度','Validation window NLL'),title=tr('A  统一验证尺度','A  Shared validation measure'));axs[0].legend(fontsize=9)
ind=np.arange(4);axs[1].bar(ind-.25,quadrant_weights,.25,label=tr('目标','Target'),color='#526b59');axs[1].bar(ind,model_stats['GridMLE']['quadrant_mass'],.25,label='GridMLE',color='#125f82');axs[1].bar(ind+.25,model_stats['PCD20']['quadrant_mass'],.25,label='PCD20',color='#bf7139');axs[1].set(xticks=ind,xlabel=tr('象限类别','Quadrant class'),ylabel=tr('概率质量','Probability mass'),title=tr('B  网格积分得到的质量','B  Mass from quadrature'));axs[1].legend(fontsize=8)
axs[2].scatter(*neural_samples['GridMLE'].T,s=5,alpha=.45,color='#125f82');axs[2].set(xlim=(-4,4),ylim=(-4,4),xlabel='x1',ylabel='x2',title=tr('C  GridMLE的512条MALA终点','C  512 MALA endpoints for GridMLE'));axs[2].set_aspect('equal');save(fig,'learning')
labels={'small_one':tr('ULA h=0.005，单谷起点','ULA h=0.005, one valley'),'small_spread':tr('ULA h=0.005，四谷均分','ULA h=0.005, spread'),'medium_spread':tr('ULA h=0.04，四谷均分','ULA h=0.04, spread'),'large_spread':tr('ULA h=0.16，四谷均分','ULA h=0.16, spread'),'mala_spread':tr('MALA h=0.16，四谷均分','MALA h=0.16, spread')}
fig,axs=plt.subplots(2,3,figsize=(13,7.4),layout='constrained');names=list(runs)
for ax,name in zip(axs.flat,names):
 pp=paths[name];ax.plot(pp[:,0,0],pp[:,0,1],lw=.8,color='#bf7139',alpha=.8);ax.scatter(*pp[-1].T,s=6,color='#125f82',alpha=.6);ax.scatter(*centers.T,marker='+',color='#111',s=55);ax.set(xlim=(-4,4),ylim=(-4,4),xlabel='x1',ylabel='x2',title=f"{labels[name]}\nTV={runs[name]['total_variation']:.3f}");ax.set_aspect('equal')
axs[1,2].axis('off');axs[1,2].bar(np.arange(4),quadrant_weights,color=['#125f82','#bf7139','#63864b','#755c8b']);axs[1,2].axis('on');axs[1,2].set(xticks=range(4),xlabel=tr('象限类别','Quadrant class'),ylabel=tr('真实概率质量','True mass'),title=tr('已知目标：0.55 / 0.25 / 0.15 / 0.05','Known target: 0.55 / 0.25 / 0.15 / 0.05'));save(fig,'mixing')
fig,axs=plt.subplots(1,3,figsize=(13,4.2),layout='constrained')
for name,color in [('small_one','#125f82'),('small_spread','#bf7139'),('mala_spread','#63864b')]:
 occ=occupancies[name];axs[0].plot(np.arange(1,len(occ)+1)*10,occ[:,0],label=labels[name],color=color)
axs[0].axhline(quadrant_weights[0],color='#333',ls='--');axs[0].set(xlabel=tr('采样步数','Sampling steps'),ylabel=tr('最重象限的链比例','Fraction of chains in heaviest quadrant'),title=tr('A  初始化影响多久','A  Persistence of initialization'));axs[0].legend(fontsize=8)
for name,color in [('small_spread','#bf7139'),('mala_spread','#63864b')]:
 values=paths[name][:,0,0].copy();values-=values.mean();denom=np.dot(values,values);corr=[np.dot(values[:len(values)-lag],values[lag:])/denom if denom else float('nan') for lag in range(41)];axs[1].plot(np.arange(41)*10,corr,color=color,label=labels[name])
axs[1].set(xlabel=tr('间隔 / 采样步','Lag / sampling steps'),ylabel=tr('首链x1自相关','First-chain x1 autocorrelation'),title=tr('B  相邻样本的依赖','B  Dependence of successive samples'));axs[1].legend(fontsize=8)
q=np.linspace(-3,3,200);axs[2].plot(q,-q,label=tr('干净N(0,1) score','Clean N(0,1) score'),color='#bf7139');axs[2].plot(q,-.8*q,label=tr('加噪真实score','True noisy score'),color='#333');axs[2].plot(q,-dsm_a*q,'--',label=tr('DSM回归','DSM regression'),color='#125f82');axs[2].set(xlabel='x',ylabel='score',title=tr('C  去噪学习的是平滑密度','C  Denoising learns a smoothed density'));axs[2].legend(fontsize=8);save(fig,'diagnostics');print(json.dumps(summary,indent=2))
```

## 会在谷底活动，与会访问所有低谷，是两回事

先对完全已知的真实能量采样，可以把模型误差暂时拿掉。128条链都从最重低谷出发，使用0.005步长走2,000步，后半段仍有约95.5%的状态留在该象限，而目标约为55.0%。把初始链均匀放进四个低谷，相同步长下最重象限的占比又只有约27.9%。两种初始化得到不同结果，说明这些有限链仍记得出发位置；只看每个低谷内部的散点云，容易错过这种整体偏差。

![在完全已知目标能量下，比较五套初始化、步长和采样方法。每幅展示128条链运行2000步的最终点及第一条链轨迹；标题TV由后半程全部状态计算。最后一幅显示精确目标象限质量，顺序为左下、右下、右上、左上。](https://ml-biomat.com/static/tutorials/machine-learning/figures/29b85106c833d9ea9e3a5e7d.svg?v=29b85106c833)

图 4在完全已知目标能量下，比较五套初始化、步长和采样方法。每幅展示128条链运行2000步的最终点及第一条链轨迹；标题TV由后半程全部状态计算。最后一幅显示精确目标象限质量，顺序为左下、右下、右上、左上。

步长增到0.16后，ULA的链频繁换象限，平均每条约切换168次，但象限质量总变差距离仍约0.229。MALA用同样步长接受约43.2%的提议，消除了该提议机制的平稳分布偏差，有限2,000步的质量距离却约0.256，因为跨谷探索仍慢。较频繁移动、较高接受率、最终画面像四团点，各自回答的问题不同。这里的总变差是四个象限概率差的绝对值之和的一半，度量的是这四个区域的质量误差。

对学出的GridMLE能量，网格质量与目标的距离只有约0.006；但从512组新高斯起点运行1,000步MALA后，链的后半段质量与该模型网格质量的距离仍约0.099。模型已经给出了较合理的四团权重，采样器还没有充分体现它。图中的轨迹、象限占比与自相关因此要一起看：同一低谷中的连续坐标可以很快失去局部相关，链仍可能很少访问其他低谷。增加独立初始化、检查跨区域往返，再比较较长运行的分布，是具体可执行的诊断步骤。

![左：128条链在最重象限的即时占比与目标概率。中：第一条链x₁坐标的自相关，每10步记录一次，横轴换算为实际步数；采用完整中心化平方和作分母。右：20万点去噪score回归，与干净及带噪高斯的解析score对照。](https://ml-biomat.com/static/tutorials/machine-learning/figures/76c3d19e8a3609bd73e0acbe.svg?v=76c3d19e8a36)

图 5左：128条链在最重象限的即时占比与目标概率。中：第一条链x₁坐标的自相关，每10步记录一次，横轴换算为实际步数；采用完整中心化平方和作分母。右：20万点去噪score回归，与干净及带噪高斯的解析score对照。

## 让链自己走：能量相同，探索结果为何不同

16条链使用固定种子4001，浏览器逐步执行完整ULA或MALA。可以切换已知目标与真实训练的GridMLE能量；背景能量与密度各有独立含义。改变模型、步长或初始化会重新开始。

[Figure: 能量或密度背景、16条随机链和象限质量](https://ml-biomat.com/tutorials/machine-learning/m40/#M40-board)

蓝点为当前16个位置，红线为第一条链走过的轨迹。右侧灰柱表示该能量的目标象限质量，蓝柱累计每一步的16个状态（包括拒绝后重复的状态）；它们包含起步阶段。坐标超出背景窗口时自动扩轴，概率统计保留全部位置。

## 从分类分数到扩散方向，哪些信息能够共用

一个分类器输出每个类别的logit，也可以写成输入与类别的联合能量：取该类别logit的负值。给定输入后，对有限类别归一化，就回到熟悉的softmax。若把类别边缘化，还可得到关于输入的一个非归一化分数。2019年的Joint Energy-based Model工作沿着这一联系把分类与生成训练放在一起，但单靠分类正确并不会自动确定输入密度。

$$
E(x,y)=-f_y(x),\qquad p(y\mid x)=\frac{e^{f_y(x)}}{\sum_c e^{f_c(x)}},\qquad E_{\rm input}(x)=-\log\sum_c e^{f_c(x)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fefe874b2667ea8d6da93133.svg) | 输入向量、类别标签和对全部类别求和的索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/091ca0487396554a405569c6.svg) | 对应类别的无量纲logit与输入—类别联合能量；C类分类器输出C个logit。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3092e09750f999904d9eddf5.svg) | 给定输入的类别概率、对类别边缘化后的输入能量和自然对数。 |

联合权重为exp(f_y)，固定x对类别求和就得到softmax；同一总和也提供输入的未归一化权重。logit(2,0)给概率0.880797与0.119203，输入能量约−2.126928。都加10后类别概率不变，输入能量变成−12.126928，因此分类训练不能单独确定输入密度。

原因可以用两个数字说明。类别logit为(2,0)时，第一类概率约0.881；对同一个输入同时加10，变成(12,10)，类别概率完全相同，输入对应的边缘能量却降低10。若这个共同偏移随输入变化，分类损失无法识别它，输入之间的相对密度却会改变。要把分类器用作生成模型，就需要针对输入分布增加相应训练信号，而不能只把已有softmax分数换个名字。

扩散与能量模型也通过score相连。固定能量给出一个固定分布的方向场，扩散通常学习多个噪声水平上的方向，并沿着时间变化生成样本。能量相加还对应概率权重相乘，适合表达多个条件同时满足的倾向，例如动作接近目标且避开障碍。真正使用时，要分别检查能量是否描述了目标、训练是否覆盖了关键区域、采样是否充分探索。四个低谷里的每一项检查，都能迁移到更高维的候选设计问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M40.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [UvA Deep Learning Tutorials: Deep Energy-Based Models](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial8/Deep_Energy_Models.html)

   能量、负相、持续采样与原始生成迭代图。

   MIT, Copyright 2020 Phillip Lippe; original notebook output; external attributed figures excluded
2. [Estimation of Non-Normalized Statistical Models by Score Matching](https://jmlr.org/papers/v6/hyvarinen05a.html)

   2005年Score Matching目标及分部积分条件。

   Primary paper reference; no copied figures
3. [A Connection Between Score Matching and Denoising Autoencoders](https://www-labs.iro.umontreal.ca/~vincentp/Publications/DenoisingScoreMatching_NeuralComp2011.pdf)

   2011年高斯去噪与平滑密度score的联系。

   Author-hosted primary paper; no copied figures
4. [Training Products of Experts by Minimizing Contrastive Divergence](https://www.cs.toronto.edu/~hinton/absps/tr00-004.pdf)

   短链Contrastive Divergence的训练思路。

   Author-hosted technical report; no copied figures
5. [Implicit Generation and Generalization in Energy-Based Models](https://arxiv.org/html/1903.08689v2)

   神经能量模型、Langevin负样本和样本缓存。

   Primary paper reference; independent experiment
6. [Exponential Convergence of Langevin Distributions and Their Discrete Approximations](https://stat.duke.edu/~scs/Courses/Stat376/Papers/ConvergeRates/GeneralState/RobertsTweedie1996.pdf)

   连续Langevin、离散近似与Metropolis修正。

   Primary paper reference; no copied figures
7. [Your Classifier is Secretly an Energy Based Model and You Should Treat it Like One](https://arxiv.org/abs/1912.03263)

   分类logit与联合能量的联系。

   Primary paper reference; no copied figures
