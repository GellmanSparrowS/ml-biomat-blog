# 从一杯咖啡到科学机器学习：PINN、FNO与方程发现

Source: https://ml-biomat.com/tutorials/machine-learning/m29/
Language: zh-CN

把已知规律、观测数据和数值方法放在一起，分清求解、识别、算子学习与机制发现。

## 1. 一杯咖啡，能把哪些问题交给机器学习

把一杯热咖啡放在桌上，每分钟测一次温度，很快就能画出一条下降曲线。接下来可以问几个不同的问题：十分钟后还能有多热？换一个杯子，冷却速度会怎样变化？只测最初一分钟，能否同时判断杯子的保温能力和房间温度？这些问题都用到了数据，却需要不同的计算。已知冷却规律和参数时，我们向前计算温度；规律已知、参数未知时，我们从测量反推参数；连规律的形式也不清楚时，则需要比较能够解释观测的候选方程。

科学机器学习把这种问题结构带进学习过程。已知的部分可以是守恒关系、微分方程、几何对称性，也可以是一段能够求导的模拟程序。网络负责表示未知函数、补充缺少的机制，或加速许多重复求解。它像是在一张已有道路与河流的地图上补全细节：哪些地方已经有可靠信息，哪些地方需要数据决定，应该在建模前说清。这样选择网络和损失函数时，就有了比“换一个更大的模型”更具体的依据。

本章沿着三个问题展开：冷却曲线带我们理解数值求解、PINN与参数识别；一根首尾相接的导热环带我们理解FNO为什么学习的是函数之间的映射；带噪声的增长曲线则让SINDy从候选表达式中挑出方程。最后再用振子的能量检查提醒我们，连续方程、学习表示和离散求解各自承担什么工作。下面的图把这些输入输出并列，读后面的代码时可以不断回到这张图，确认当前学习的对象究竟是什么。

![从Fourier的波分解，到SINDy、PINN与FNO：各方法接收与学习的对象不同。曲线为机制示意；后续实验图展示实际计算。](https://ml-biomat.com/static/tutorials/machine-learning/figures/219900607e341e74b0f8a380.svg?v=219900607e34)

图 1从Fourier的波分解，到SINDy、PINN与FNO：各方法接收与学习的对象不同。曲线为机制示意；后续实验图展示实际计算。

## 2. 微分方程是在说明“现在怎样变化”

温度计给出的是某一时刻的温度，微分方程描述的是温度此刻变化得多快。咖啡比房间热得越多，向外散热通常越快；在一个简化的集中温度模型中，变化率与温差成正比。这里把杯中温度看成一个数，意味着忽略杯内不同位置的温度差；房间温度保持固定，冷却率也在这段实验中保持不变。它适合解释一条整体冷却曲线。如果研究的是厚物体内部各点的温度，则还需要空间坐标和热传导方程。

$$
\frac{dT}{dt}=-k(T-T_a),\qquad T(t)=T_a+(T_0-T_a)e^{-kt}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bfb18198bbe0d00a4b99f5f6.svg) | 当前、环境与初始温度，单位°C；相减后的温差也可用K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/46e85659ae7cce8ad65d8b6c.svg) | 时间以min计，正冷却率k以min⁻¹计；kt无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f970573b6ea0d9dd47cb0090.svg) | 温度变化率，单位°C/min；e是自然指数的底数。 |

先把温差记为θ=T−T_a，环境恒定时θ的变化率等于−kθ。指数函数求导后仍含自身，因此θ=(T_0−T_a)e^(−kt)满足方程与起点。T_0=80、T_a=20、k=0.35时，初始变化率为−21°C/min，一分钟后解析温度约62.28°C。

导数不必先理解成一个陌生符号。若当前每分钟大约下降21摄氏度，那么很短的0.1分钟内，先按下降2.1摄氏度估计，就得到一个新的温度；再用新温度重新估计下一小段的速度。这就是显式Euler方法的基本做法。它把一条连续变化的曲线拆成许多局部直线。步长越大，一步之内“速度近似不变”的假设越粗；缩小步长后，可以观察结果是否逐渐稳定，而不是只相信一次计算输出的小数位。

$$
T_{n+1}=T_n-hk(T_n-T_a),\qquad T_{n+1}-T_a=(1-hk)(T_n-T_a)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8d3557db3b53e7263582572.svg) | 步编号和该步温度；编号无量纲、温度°C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a70852daaf5fec5d910599d1.svg) | 时间步长min、冷却率min⁻¹、固定环境温度°C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e042d48fdfe39efc4daf9ad.svg) | 一步的温差放大因子，无量纲。 |

当前斜率乘步长给出温度增量。k=.5、h=2时因子为0，80°C一步变为20°C；k=.5、h=4时因子为−1，温度在80与−40°C间摆动。渐近衰减要求|1−hk|<1，即0<hk<2；单调不越过环境的条件更强，为0<hk≤1。

对这个冷却方程，数值稳定性还能直接算出来。每走一步，温差乘以一个固定因子：因子在0与1之间，温度单调靠近环境；因子在−1与0之间，温度会越过环境温度来回摆动，但幅度渐小；绝对值超过1，摆动反而越来越大。真实的咖啡并没有获得一台加热器，增加的温差来自离散算法。交互中可以改变冷却率与步长，比较同一物理模型的解析曲线、Euler和四阶Runge–Kutta结果。先理解这种数值误差，后面才容易判断网络在模仿什么。

## 计算器会让咖啡越来越热吗？

改变冷却率与步长，对照精确指数曲线。每个点都是实际离散更新；坐标范围随结果调整，保留越过环境温度或发散的点。

[Figure: 温度与时间以及一步放大因子](https://ml-biomat.com/tutorials/machine-learning/m29/#M29-board)

RK4在一步内评估四次斜率，按1、2、2、1加权，再除以6。显示的放大因子针对完整步长；最后一步若不足h，则缩短到12min终点。

常微分方程只有一个独立变量，例如时间；偏微分方程还把位置等变量加入描述。实际软件中的自适应求解器会估计局部误差，自动调整步长，SciPy的solve_ivp就提供了这类接口。绝对容差决定接近零时允许多大的绝对误差，相对容差则按当前状态大小缩放要求。求解器容差与观测噪声是两件事：前者控制计算近似，后者描述测量起伏。把二者分开记录，才能知道继续加密计算是否还有实际价值。

## 3. PINN把一条曲线放进方程里检查

传统时间推进从起点逐步走向未来，PINN则先用神经网络表示整条待求曲线。给网络一个时刻，它输出该时刻的温度；自动微分再计算这条曲线的斜率，把斜率和温度一起代入冷却方程。若两边不平衡，就得到一个残差。训练通过许多位置的残差来调整曲线，同时满足初始条件或边界条件。Raissi等人的公开PINN工作把这种思路用于微分方程的解与参数发现，核心联系是网络的可微表示与已有的物理关系。

直接把摄氏度和分钟塞进损失，容易让不同项因数值尺度而失衡。这里先把温差除以初始温差60摄氏度，再把时间除以10分钟。新的状态u与时间τ都是无量纲量，冷却参数相应变为3.5。无量纲化并没有改变物理过程，而是换了一套适合比较的坐标。就像把不同货币换算到同一计价单位，先统一尺度，才能讨论哪个误差更大；若后续还加入数据误差、边界误差，也要说明它们采用什么尺度与权重。

$$
u_\theta(\tau)=1+\tau N_\theta(\tau),\qquad r_\theta=\frac{du_\theta}{d\tau}+\kappa u_\theta,\qquad L_r=\frac1{N_c}\sum_{i=1}^{N_c}r_\theta(\tau_i)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/72cc594dfb76298686ce40b5.svg) | τ=t/(10min)，u=(T−20°C)/(60°C)，均无量纲；θ表示网络参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c60c8d085d6caee0e9ac014b.svg) | 标量网络输出及无量纲冷却率κ=(10min)k=3.5。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4e82384609c5e54e34522cc1.svg) | 无量纲方程残差、残差均方、64个配点及其索引。 |

τ=0时u恒等于1。若某处u=.5、导数−1.6，则r=−1.6+3.5×.5=.15，残差平方=.0225。训练把许多位置的这种不平衡相加；自动微分需要保留导数计算图，随后才能继续对参数θ求导。

本例把网络输出写成“1加上τ乘以一个可学习函数”。当τ为零时，后半项自动消失，所以初始状态永远等于1，不需要用一个很大的惩罚系数去逼近它。这叫把条件直接写进表示。若改为只最小化方程残差而不约束初值，恒等于零的曲线也能满足冷却方程，却描述了完全不同的起点。方程、初始条件与边界条件共同确定问题，缺少其中一项时，损失下降也可能对应另一个解。

实际实验使用64个训练位置、两个24单元的隐藏层和1600次更新，并在另外200个位置检查残差。训练区间内，归一化温差的最大绝对误差约0.00259，折回温度约0.156摄氏度；把同一网络延伸到两倍时间，最大误差却约0.335。图中可直接看到训练范围以外的曲线重新上翘。这个现象说明怎样设计下一步检验：扩展残差采样区间、保留长时间观测，或选择时间推进表示，再比较同一时间范围内的误差。网络能在任意坐标上给出数值，准确性仍需要与实际约束覆盖的区域对应。

![左：同一冷却方程的解析与Euler结果，k=.35min⁻¹；中：PINN只在τ≤1训练，虚线外检查到τ=2；右：实际残差训练曲线。](https://ml-biomat.com/static/tutorials/machine-learning/figures/81ceae80a952aafa40c463f6.svg?v=81ceae80a952)

图 2左：同一冷却方程的解析与Euler结果，k=.35min⁻¹；中：PINN只在τ≤1训练，虚线外检查到τ=2；右：实际残差训练曲线。

## 4. 反问题：让观测告诉我们参数是多少

现在保留冷却规律，但把冷却率当成未知量。每试一个冷却率，模拟器都能产生一组预测温度；预测与测量之间的平方差，告诉我们这个参数是否合适。若模拟器的每一步都能求导，就可以把最终误差沿时间步向后传，直接计算参数增加一点会让误差如何变化。本例对原始参数使用softplus变换，保证冷却率为正，再通过一个步长0.05分钟的Euler模拟器优化参数。学习的对象只有一个标量，依然属于从数据识别动力系统。

$$
k=\log(1+e^a),\qquad L_{\rm obs}(a)=\frac1m\sum_{j=1}^m\left[T_h(t_j;k(a))-y_j\right]^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ecdfbca3a5b513951afdb7.svg) | 无约束原始参数a与正冷却率k；代码使用每分钟这一固定单位表示k的数值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa1443ee8179ae13c02ba6cb.svg) | 9次观测、观测编号、时间min和实测温度°C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4fae8c260301ef518f4a8217.svg) | 步长h=.05min的模拟器温度；观测均方损失单位°C²。 |

预测温度若比两次观测分别高1°C和低2°C，这两点的均方误差为(1²+2²)/2=2.5°C²。链式法则先经过各时间步，再经过k对a的导数；softplus导数为sigmoid(a)。指数内a是无量纲优化坐标，k的物理单位由选定的参数化单位承载。

构造数据使用真实冷却率0.35每分钟，在0到8分钟每隔一分钟观测一次，除精确已知的初始值外加入标准差0.4摄氏度的噪声。优化得到约0.35115每分钟。程序还在一个固定参数位置比较自动微分与中心差分，两者相对差约3.23×10⁻⁹。这检验的是离散模拟器的梯度计算：自动微分准确地对当前程序求导，程序自身的时间离散误差则仍由步长决定。改变步长再重新识别参数，可以观察数值近似是否正在影响估计。

参数能否被数据区分，比优化器能否继续降低损失更根本。若环境温度也未知，只观察最初一分钟时，较冷的房间与较小的冷却率可能产生相似曲线。图中的误差等值线因此形成细长的谷；观察到8分钟后，两种作用更容易分开，低误差区域也更集中。这叫可辨识性。增加同一时刻的重复测量主要帮助降低噪声，延长观察窗口或改变初始温度则可能提供新的辨识信息，实验设计应根据缺少的那种信息来调整。

![左：9次温度观测与估计参数对应的连续解，误差棒为0.4°C且初值精确；右两图：使用精确无噪目标比较不同观察窗的参数RMSE等值线，星号是真实参数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5fa0af0022b4e34a4899850c.svg?v=5fa0af0022b4)

图 3左：9次温度观测与估计参数对应的连续解，误差棒为0.4°C且初值精确；右两图：使用精确无噪目标比较不同观察窗的参数RMSE等值线，星号是真实参数。

若可信规律只描述了部分过程，可以保留已知项，再用一个小网络表示未知的修正。例如主散热项已知，但外部热源随时间变化，混合模型可以把两者分开写出。2020年的Universal Differential Equations工作系统讨论了把可学习结构嵌入微分方程的方式。修正项的输入、单位和允许变化的范围都应明确；若网络自由度过大，它可能同时吸收传感器偏差、错误参数和遗漏机制。比较不同实验条件下的修正是否一致，能帮助判断它学到的是什么。

## 5. FNO学习的是“给一整条初始曲线，返回一整条终态曲线”

一杯咖啡只用一个温度就能近似表示，导热环却需要描述各个位置。设某处初始较热、另一处较冷，热会从温度高的位置向周围扩散，尖锐的起伏逐渐变平。Fourier在1822年的《热的解析理论》中，把热传导与三角级数联系起来：复杂形状可以分解成不同频率的波，每个波怎样衰减就能分别计算。这种表示把一条看似复杂的曲线，变成一组有明确意义的幅度。图里的衰减因子显示，越细密的空间起伏，消退得越快。

$$
\partial_t u=\nu\partial_{xx}u,\quad u(x+1,t)=u(x,t),\qquad \widehat u_k(t)=\widehat u_k(0)e^{-\nu(2\pi k)^2t}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fbbaf8b0fdd040f786401509.svg) | 本热环实验中的位置、时间、相对场值与扩散系数均已无量纲化，ν=.01。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3fbb79a4d0c9ef0232fdb904.svg) | 对时间的一阶偏导与对位置的二阶偏导。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e785b1453f8f37fb139bdad4.svg) | 整数空间频率编号、该频率复幅度、圆周率；此处k不是冷却率。 |

正弦或余弦对x求两次导数会乘−(2πk)²，所以每个幅度服从独立的指数衰减。t=1时第1模式乘约.673825，第2模式乘约.206153；k=0时乘1，平均值保持不变。周期边界让环首尾连接，网格不重复采样同一个端点。

若只求一次终态，成熟的数值方法通常已经很合适。若要对许多初始温度分布重复计算，例如在设计优化中反复比较不同输入，就可以学习“初始函数到终态函数”的映射。2020年提出、随后发表的Fourier Neural Operator把一部分可学习变换放在频率空间中。PINN接收一个坐标，输出一个解的数值；这里的FNO接收整条初始曲线，输出相应的整条终态曲线。训练集因此应按独立函数划分，同一条曲线上的不同网格点共同属于一个样本。

$$
v_{\ell+1}(x)=\sigma\!\left(W_\ell v_\ell(x)+\mathcal F^{-1}\!\left[R_\ell(k)\mathcal F[v_\ell](k)\right](x)+b_\ell\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f3f6b3ec1592328a300359e.svg) | 第ℓ层的12通道场、层编号与无量纲位置；批张量形状B×12×N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4d9fbc783e21ae17b2cff8a.svg) | 逐点12×12实矩阵、12维偏置与GELU非线性，位置间共享。 |
| ![Formula](https://ml-biomat.com/static/agent-math/edcf1fc5bb0656f0573915de.svg) | 实输入FFT、对应逆变换和每个保留频率的12×12复通道矩阵；保留k=0…5，其余谱分支系数为0。 |

若只看单通道某个频率，输入幅度2乘权重.5得到1，逆变换把各频率重新叠回空间。实际代码还包含多通道混合、逐点项与非线性。N从32变64时同一组频率权重仍可使用；能否准确处理变化后的输入函数，需要独立数据检验。

本章真正训练了一个两层的小型FNO。输入先提升到12个特征通道，每层把特征做快速Fourier变换，在前6个频率位置上学习通道混合，再变回空间；并行的逐点线性变换保留局部信息，二者相加后经过GELU。频率权重是复数，因为一个波的幅度和相位都要表达；最终输出仍是实数场。保留少数频率让全局变化的处理较紧凑，逐点项与非线性也会参与构造更细的结构，因此不能把整个网络简单等同于一次低通滤波。

训练使用96条初始函数，24条验证函数选择权重，最后24条独立函数评价。所有函数由常数项与第1到4阶正弦、余弦组成，目标终态由热方程的精确频率衰减生成。网络在32点网格训练，第580次更新取得最低验证误差；独立函数的平均相对L2误差约0.00612。计算时，先把一条曲线上的逐点误差平方相加并开方，再除以真实曲线各点平方和的平方根，最后对24条曲线取平均。将同一批独立函数改在64点网格采样，误差仍约0.00612。这里检验的是同一物理参数、同一类输入函数下的分辨率变化；要研究更高频输入、不同扩散系数或新边界，还应把相应条件加入训练和独立测试设计。

![同一个FNO在32与64点网格预测同一批24个独立函数；误差图共用对称色标。右上是训练/验证MSE，右下为精确热方程衰减，浅色覆盖输入含有的1–4阶模式。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2298d03e4336f4cc441854dc.svg?v=2298d03e4336)

图 4同一个FNO在32与64点网格预测同一批24个独立函数；误差图共用对称色标。右上是训练/验证MSE，右下为精确热方程衰减，浅色覆盖输入含有的1–4阶模式。

## 6. 已经知道的守恒关系，可以直接参与表示

周期导热环没有向外输送热量，因此平均温度应保持不变。普通FNO并不会自动精确满足这一点：本例原始输出的平均值误差约9.54×10⁻⁴。我们可以先减去预测场的平均值，再加回输入场的平均值，得到满足该离散守恒关系的输出。这个操作相当于把整条曲线上下平移到正确的平均高度，保留其空间起伏；由于真实目标也有这个平均值，在相同均方误差度量下，它消除了与常数方向有关的误差分量。

$$
\widetilde u_j=\widehat u_j-\overline{\widehat u}+\overline{u_0},\qquad \overline u=\frac1N\sum_{j=1}^N u_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2bba91d3946a6152c4300f05.svg) | 第j个网格位置的原始预测、投影预测与初始场；场值无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f4e94f360946e2a19f19f355.svg) | 均匀网格的算术平均、网格点数和索引；本例N=32或64。 |

若预测为(1,3)、初始均值为1.5，预测均值是2，投影结果为(.5,2.5)，新均值正好1.5。这里的“帽子”表示预测，与上一节Fourier系数的帽子按语境区分。非均匀网格需要按单元权重计算积分平均。

32点测试网格上，投影后的均方误差从约5.38×10⁻⁶变为3.87×10⁻⁶，平均值守恒误差降到浮点舍入量级。这个改善有清楚的前提：周期边界、无源热方程与均匀网格。如果边界正在散热、系统存在热源，或网格单元大小不同，就要分别采用通量平衡、源项平衡或加权积分。把“物理约束”写成一个口号没有帮助，必须先说明守恒的量、它在哪个范围成立，以及离散数据怎样计算这个量。

对无摩擦振子，另一个有用结构是能量。Hamiltonian方法用一个能量函数产生运动方向，2019年的Hamiltonian Neural Networks进一步让网络学习这个函数。连续时间下，由相反的交叉导数产生的两项变化可以抵消，形成能量守恒。真正运行时，还要用离散积分器推进时间；一个连续方程具有守恒结构，并不意味着任意离散算法都会逐步精确守恒。下面不训练网络，而是固定同一个已知振子，只改变积分规则，单独观察这一层影响。

$$
H(q,p)=\tfrac12(q^2+p^2),\quad \dot q=p,\quad\dot p=-q,\qquad p_{n+1}=p_n-hq_n,\quad q_{n+1}=q_n+hp_{n+1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a28ff85d15b897481636239.svg) | 无量纲位置、动量与能量；质量与刚度已缩放为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5034fd939bf7fc7f74b7be0b.svg) | 对无量纲时间的导数、步编号、步长h=.1。 |

连续能量导数为q·p+p·(−q)=0。辛Euler从(q,p)=(1,0)出发，先算p_new=−.1，再算q_new=.99，能量为(.99²+.1²)/2=.49505。显式Euler则用旧动量更新位置，得到(1,−.1)，能量=.505。两种离散更新已经在第一步产生不同的能量误差。

![同一无量纲振子、h=.1、400步，比较显式Euler与辛Euler。右侧小图放大辛Euler的能量振荡；虚线为初始能量0.5。](https://ml-biomat.com/static/tutorials/machine-learning/figures/612c90b044de7d980e4cd8ea.svg?v=612c90b044de)

图 5同一无量纲振子、h=.1、400步，比较显式Euler与辛Euler。右侧小图放大辛Euler的能量振荡；虚线为初始能量0.5。

图中显式Euler的轨迹不断向外盘旋，初始0.5的能量在400步后增加到约26.76。辛Euler先更新动量，再使用新动量更新位置，轨迹保持在原轨道附近；能量在约0.476到0.526之间振荡。辛积分保持的是相空间的几何结构，这里的能量有界波动也能从放大图看见。学习动力学时，可以分别检验连续向量场、一步预测和长时间轨迹，从而定位误差是在模型中出现，还是在推进过程中积累。

## 7. 从曲线发现方程：先决定允许哪些表达式

如果连变化规律也未知，可以先提出一个候选表达式库，例如常数、状态本身、状态平方与状态立方，再寻找少数能够解释导数的项。2016年Brunton、Proctor和Kutz提出的SINDy把这种任务组织成稀疏回归。它的吸引力在于输出直接是一条可以阅读、分析和继续求解的方程：一次项意味着随状态成比例变化，二次项可以表达随状态增大而增强的限制作用。发现过程仍依赖候选库；库中没有的机制，不会因为回归求解得很精确就自动出现。

$$
\dot{\boldsymbol u}\approx\Theta(\boldsymbol u)\boldsymbol\xi,\qquad \Theta(u_i)=(1,u_i,u_i^2,u_i^3)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/100f8a1637ae5388f5005717.svg) | 跨三条轨迹收集的无量纲状态、估计导数min⁻¹与样本索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/82770301c5be3fcb36b932c8.svg) | 每行4个候选项的设计矩阵与4维稀疏系数；由于u无量纲，各系数单位min⁻¹。 |

u=.5时一行是(1,.5,.25,.125)，乘系数(0,1.2,−.8,0)得到导数.4min⁻¹。阈值回归先最小二乘，再删去小系数，在剩余列上重新拟合。本例阈值.08对应当前变量与候选列的尺度，实际输入导数来自带噪测量的局部多项式估计。

本例用三条不同初始状态的增长曲线训练，真实规律包含1.2u与−0.8u²两项，状态u无量纲、时间以分钟计。每0.02分钟采样，并加入标准差0.002的状态噪声。直接用相邻测量之差除以时间间隔，虽然形式简单，却会放大噪声；两次独立测量的误差都进入分子，分母越小，导数起伏可能越大。程序因此在21点窗口中拟合三次局部多项式，再从多项式取得导数，并去掉边缘10个点，减少单侧窗口对回归的影响。

回归先拟合全部候选项，再删去绝对系数小于0.08的项，并在保留项上重新拟合，重复这一过程。本例最终得到约1.19949u−0.79938u²，常数项与三次项被删去。原始差分的导数均方根误差约0.0725，平滑求导后约0.00958。阈值的含义随变量单位与候选列缩放改变：若把状态换成另一套单位，同一个数字不再表示同样的筛选力度。更大的候选库还会产生相关列，实际选取时需要比较多个阈值，并查看独立轨迹是否稳定支持相同的项。

![从带噪状态估计导数、选择候选项，再从新初值u₀=.8检验0–8min轨迹；训练曲线仅覆盖0–4min，虚线标记这一时间边界。](https://ml-biomat.com/static/tutorials/machine-learning/figures/344b5869058845aecb6ff413.svg?v=344b58690588)

图 6从带噪状态估计导数、选择候选项，再从新初值u₀=.8检验0–8min轨迹；训练曲线仅覆盖0–4min，虚线标记这一时间边界。

训练曲线只覆盖0到4分钟，随后用初始状态0.8重新求解识别方程，检查到8分钟；最大状态误差约0.000520。这个检验同时改变了初值和时间范围，结果可以与导数拟合误差一起读。符号回归还可以采用表达式树搜索，让加、乘、指数等运算构成更灵活的候选；搜索空间越大，越需要用复杂度、量纲和独立数据筛选。一个短公式便于解释，但它是否描述了正确机制，要看它在相关实验条件改变后还能保留哪些预测能力。

## 8. 完整实验：从数值基线走到可检查的学习模型

下面的程序把本章五组计算放在同一个入口中。运行后得到PINN权重、FNO权重、所有构造数据、训练记录、独立预测和科学图。冷却例子先给解析基线，再检查网络和模拟器；算子例子按函数划分数据，并在同一批测试函数上比较两种网格；方程发现例子保留原始噪声、平滑导数和最终系数，能够逐步追查一个错误项从哪里进入。固定随机种子让图里的具体数值可以重现，代码中的数据生成规则也让实验条件完整可见。

### 完整Python：五组可复现实验

使用NumPy、SciPy和PyTorch实际计算。summary.json保存数值，experiment.npz保存数据与预测，pinn.pt和fno.pt保存权重。

```
"""Cooling, a small Fourier neural operator, and sparse equation discovery.

All data are constructed from the equations stated in the chapter.
The program writes only to the selected output directory.
"""
from pathlib import Path
import argparse
import copy
import json

import numpy as np
import torch
from torch import nn
from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
torch.manual_seed(2901)
rng = np.random.default_rng(2901)
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=Path('results'))
parser.add_argument('--language', choices=['zh', 'en'], default='en')
args = parser.parse_args()
out = args.output
out.mkdir(parents=True, exist_ok=True)
zh = args.language == 'zh'


def tr(chinese, english):
    return chinese if zh else english


plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
    'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
    'svg.fonttype': 'none', 'figure.facecolor': '#faf9f5',
    'axes.facecolor': '#faf9f5',
})


def save(fig, name):
    fig.savefig(out / f'{name}-{args.language}.svg', bbox_inches='tight')
    fig.savefig(out / f'{name}-{args.language}.png', dpi=130, bbox_inches='tight')
    plt.close(fig)


def euler_cooling(k, step, stop=12.0):
    time, temperature = [0.0], [80.0]
    while time[-1] < stop - 1e-12:
        dt = min(step, stop - time[-1])
        temperature.append(temperature[-1] - dt * k * (temperature[-1] - 20))
        time.append(time[-1] + dt)
    return np.array(time), np.array(temperature)


# A forward PINN: tau=t/10, u=(T-20)/60, du/dtau + 3.5*u=0.
net = nn.Sequential(nn.Linear(1, 24), nn.Tanh(), nn.Linear(24, 24),
                    nn.Tanh(), nn.Linear(24, 1)).double()
optimizer = torch.optim.Adam(net.parameters(), lr=.003)
collocation = torch.linspace(0, 1, 64, dtype=torch.float64)[:, None]
trace = []
for iteration in range(1600):
    tau = collocation.clone().requires_grad_(True)
    u = 1 + tau * net(tau)  # The initial condition is exact for any parameters.
    derivative = torch.autograd.grad(u.sum(), tau, create_graph=True)[0]
    residual = derivative + 3.5 * u
    loss = residual.square().mean()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if iteration % 40 == 0:
        trace.append([iteration, loss.item()])
grid = torch.linspace(0, 2, 401, dtype=torch.float64)[:, None]
with torch.no_grad():
    pinn = (1 + grid * net(grid)).numpy().ravel()
tau = grid.numpy().ravel()
exact = np.exp(-3.5 * tau)
test_tau = torch.tensor(np.linspace(.0025, .9975, 200)[:, None], requires_grad=True)
test_u = 1 + test_tau * net(test_tau)
test_derivative = torch.autograd.grad(test_u.sum(), test_tau)[0]
pinn_residual = (test_derivative + 3.5 * test_u).detach().numpy().ravel()
torch.save(net.state_dict(), out / 'pinn.pt')

# A differentiable numerical simulator estimates k from noisy observations.
obs_time = np.arange(0, 8.01, 1.0)
obs = 20 + 60 * np.exp(-.35 * obs_time) + rng.normal(0, .4, len(obs_time))
obs[0] = 80  # Initial condition is measured exactly in this constructed example.
dt = .05
obs_indices = torch.tensor(np.rint(obs_time / dt).astype(int))


def simulator(k):
    temperatures = [torch.tensor(80., dtype=torch.float64)]
    for _ in range(int(8 / dt)):
        temperatures.append(temperatures[-1] - dt * k * (temperatures[-1] - 20))
    return torch.stack(temperatures)[obs_indices]


probe_k = torch.tensor(.25, dtype=torch.float64, requires_grad=True)
probe_loss = (simulator(probe_k) - torch.tensor(obs)).square().mean()
automatic_gradient = torch.autograd.grad(probe_loss, probe_k)[0].item()
eps = 1e-5
with torch.no_grad():
    finite_gradient = (((simulator(torch.tensor(.25 + eps, dtype=torch.float64)) - torch.tensor(obs)).square().mean()
                       - (simulator(torch.tensor(.25 - eps, dtype=torch.float64)) - torch.tensor(obs)).square().mean()) / (2 * eps)).item()
raw_k = torch.tensor(-1.5, dtype=torch.float64, requires_grad=True)
inverse_optimizer = torch.optim.Adam([raw_k], lr=.04)
inverse_trace = []
for iteration in range(350):
    k = nn.functional.softplus(raw_k)
    inverse_loss = (simulator(k) - torch.tensor(obs)).square().mean()
    inverse_optimizer.zero_grad()
    inverse_loss.backward()
    inverse_optimizer.step()
    if iteration % 10 == 0:
        inverse_trace.append([iteration, k.item(), inverse_loss.item()])
estimated_k = nn.functional.softplus(raw_k).item()

# A genuine two-block FNO maps an initial periodic field to its field at time1.
nu = .01


def fields(coefficients, resolution, final=False):
    x = np.arange(resolution) / resolution
    result = np.repeat(coefficients[:, :1], resolution, axis=1)
    for mode in range(1, 5):
        amplitude = np.exp(-nu * (2 * np.pi * mode) ** 2) if final else 1.
        result += amplitude * (
            coefficients[:, 2 * mode - 1:2 * mode] * np.cos(2 * np.pi * mode * x)
            + coefficients[:, 2 * mode:2 * mode + 1] * np.sin(2 * np.pi * mode * x))
    return result.astype('float32')


coefficients = rng.normal(0, .45, (144, 9))
coefficients[:, 0] = rng.uniform(-.5, .5, 144)
train_x = torch.tensor(fields(coefficients[:96], 32))[:, None]
train_y = torch.tensor(fields(coefficients[:96], 32, True))[:, None]
valid_x = torch.tensor(fields(coefficients[96:120], 32))[:, None]
valid_y = torch.tensor(fields(coefficients[96:120], 32, True))[:, None]


class SpectralLayer(nn.Module):
    def __init__(self, width, modes):
        super().__init__()
        self.modes = modes
        self.weights = nn.Parameter(torch.randn(width, width, modes, dtype=torch.cfloat) / width)

    def forward(self, values):
        transformed = torch.fft.rfft(values, dim=-1)
        result = torch.zeros(values.shape[0], values.shape[1], transformed.shape[-1],
                             dtype=torch.cfloat, device=values.device)
        result[:, :, :self.modes] = torch.einsum(
            'bik,iok->bok', transformed[:, :, :self.modes], self.weights)
        return torch.fft.irfft(result, n=values.shape[-1], dim=-1)


class SmallFNO(nn.Module):
    def __init__(self):
        super().__init__()
        self.lift = nn.Conv1d(1, 12, 1)
        self.spectral = nn.ModuleList([SpectralLayer(12, 6) for _ in range(2)])
        self.local = nn.ModuleList([nn.Conv1d(12, 12, 1) for _ in range(2)])
        self.readout = nn.Conv1d(12, 1, 1)

    def forward(self, values):
        hidden = self.lift(values)
        for spectral, local in zip(self.spectral, self.local):
            hidden = nn.functional.gelu(spectral(hidden) + local(hidden))
        return self.readout(hidden)


torch.manual_seed(2902)
fno = SmallFNO()
fno_optimizer = torch.optim.Adam(fno.parameters(), lr=.003)
fno_rng = torch.Generator().manual_seed(2903)
best_validation, best_state, best_step = float('inf'), None, None
fno_trace = []
for iteration in range(601):
    indices = torch.randint(96, (32,), generator=fno_rng)
    loss = (fno(train_x[indices]) - train_y[indices]).square().mean()
    fno_optimizer.zero_grad()
    loss.backward()
    fno_optimizer.step()
    if iteration % 20 == 0:
        with torch.no_grad():
            validation = (fno(valid_x) - valid_y).square().mean().item()
        fno_trace.append([iteration, loss.item(), validation])
        if validation < best_validation:
            best_validation = validation
            best_state = copy.deepcopy(fno.state_dict())
            best_step = iteration
fno.load_state_dict(best_state)
torch.save(fno.state_dict(), out / 'fno.pt')
operator_results = {}
operator_arrays = {}
for resolution in [32, 64]:
    inputs = fields(coefficients[120:], resolution)
    targets = fields(coefficients[120:], resolution, True)
    with torch.no_grad():
        prediction = fno(torch.tensor(inputs)[:, None]).numpy()[:, 0]
    conserved = prediction - prediction.mean(1, keepdims=True) + inputs.mean(1, keepdims=True)
    relative = np.linalg.norm(prediction - targets, axis=1) / np.linalg.norm(targets, axis=1)
    operator_results[str(resolution)] = {
        'mean_relative_l2': float(relative.mean()),
        'mse': float(np.mean((prediction - targets) ** 2)),
        'projected_mse': float(np.mean((conserved - targets) ** 2)),
        'mean_conservation_error': float(np.mean(np.abs(prediction.mean(1) - inputs.mean(1)))),
        'projected_conservation_max_error': float(np.max(np.abs(conserved.mean(1) - inputs.mean(1)))),
        'identity_mse': float(np.mean((inputs - targets) ** 2)),
    }
    operator_arrays.update({f'input_{resolution}': inputs, f'target_{resolution}': targets,
                            f'prediction_{resolution}': prediction, f'projected_{resolution}': conserved})

# Sparse identification uses smoothed numerical derivatives, not known derivatives.
time = np.arange(0, 4.001, .02)


def logistic(t, initial):
    capacity = 1.2 / .8
    return capacity / (1 + (capacity / initial - 1) * np.exp(-1.2 * t))


clean = np.array([logistic(time, initial) for initial in [.2, .5, 1.]])
noisy = clean + rng.normal(0, .002, clean.shape)
smooth = savgol_filter(noisy, 21, 3, axis=1)
estimated_derivatives = savgol_filter(noisy, 21, 3, deriv=1, delta=.02, axis=1)
raw_derivatives = np.gradient(noisy, .02, axis=1)
states = smooth[:, 10:-10].ravel()
derivatives = estimated_derivatives[:, 10:-10].ravel()
library = np.stack([np.ones_like(states), states, states**2, states**3], axis=1)
coefficients_sindy = np.linalg.lstsq(library, derivatives, rcond=None)[0]
for _ in range(8):
    active = np.abs(coefficients_sindy) >= .08
    coefficients_sindy[~active] = 0
    coefficients_sindy[active] = np.linalg.lstsq(library[:, active], derivatives, rcond=None)[0]
rollout_time = np.linspace(0, 8, 401)
identified = solve_ivp(lambda t, x: sum(c * x**i for i, c in enumerate(coefficients_sindy)),
                       [0, 8], [.8], t_eval=rollout_time, rtol=1e-9, atol=1e-11).y[0]
true_derivative = 1.2 * clean - .8 * clean**2

# Same oscillator, different integrators: geometry changes long-time energy.
position = {'euler': [1.], 'symplectic': [1.]}
momentum = {'euler': [0.], 'symplectic': [0.]}
for _ in range(400):
    x, v = position['euler'][-1], momentum['euler'][-1]
    position['euler'].append(x + .1 * v)
    momentum['euler'].append(v - .1 * x)
    x, v = position['symplectic'][-1], momentum['symplectic'][-1]
    new_v = v - .1 * x
    momentum['symplectic'].append(new_v)
    position['symplectic'].append(x + .1 * new_v)
energy = {key: .5 * (np.array(position[key])**2 + np.array(momentum[key])**2) for key in position}

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
t = np.linspace(0, 12, 401)
axes[0].plot(t, 20 + 60 * np.exp(-.35 * t), color='#183a4c', label=tr('解析解', 'Analytic'))
for step, color in [(1, '#267b7d'), (6, '#bd653f')]:
    et, ey = euler_cooling(.35, step)
    axes[0].plot(et, ey, 'o--', color=color, label=f'Euler h={step}')
axes[0].axhline(20, color='#aaa', lw=.8)
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('温度 / °C', 'Temperature / °C'), title=tr('A  步长改变数值行为', 'A  Step size changes dynamics'))
axes[0].legend(fontsize=8)
axes[1].plot(tau, exact, color='#183a4c', label=tr('解析解', 'Analytic'))
axes[1].plot(tau, pinn, color='#267b7d', label='PINN')
axes[1].axvline(1, color='#bd653f', ls='--')
axes[1].set(xlabel=tr('无量纲时间 τ', 'Dimensionless time τ'), ylabel=tr('无量纲温差 u', 'Dimensionless excess u'), title=tr('B  训练区间与外推', 'B  Training interval and extrapolation'))
axes[1].legend(fontsize=8)
axes[2].semilogy(np.array(trace)[:, 0], np.array(trace)[:, 1], color='#267b7d')
axes[2].set(xlabel=tr('更新次数', 'Updates'), ylabel=tr('残差均方', 'Mean squared residual'), title=tr('C  自动微分形成约束', 'C  Autodifferentiated constraint'))
save(fig, 'cooling')

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
axes[0].errorbar(obs_time, obs, yerr=np.r_[0, np.repeat(.4, len(obs_time)-1)], fmt='o', color='#bd653f', label=tr('观测 ±1σ', 'Observations ±1σ'))
axes[0].plot(t, 20 + 60 * np.exp(-estimated_k * t), color='#267b7d', label=tr('估计参数的连续解', 'Continuous curve at fitted k'))
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('温度 / °C', 'Temperature / °C'), title=tr('A  可微求解器识别参数', 'A  Identify a simulator parameter'))
axes[0].legend(fontsize=8)
kk, ambient = np.meshgrid(np.linspace(.15, .6, 101), np.linspace(5, 35, 101))
for ax, stop in zip(axes[1:], [1, 8]):
    sample_t = np.linspace(0, stop, 9)
    target = 20 + 60 * np.exp(-.35 * sample_t)
    predicted = ambient[..., None] + (80 - ambient[..., None]) * np.exp(-kk[..., None] * sample_t)
    rmse = np.sqrt(np.mean((predicted - target)**2, axis=-1))
    contours = ax.contour(kk, ambient, rmse, levels=[.2, .5, 1, 2, 4, 8], cmap='viridis')
    ax.clabel(contours, fontsize=8)
    ax.plot(.35, 20, '*', color='#bd653f', ms=11)
    ax.set(xlabel=tr('冷却率 k / min$^{-1}$', 'Rate k / min$^{-1}$'), ylabel=tr('环境温度 / °C', 'Ambient / °C'), title=tr(f'0–{stop} min：温度RMSE等值线', f'0–{stop} min: temperature-RMSE contours'))
save(fig, 'inverse')

fig, axes = plt.subplots(2, 3, figsize=(13.5, 7), layout='constrained')
error_limit = max(float(np.max(np.abs(operator_arrays[f'prediction_{n}'] - operator_arrays[f'target_{n}']))) for n in [32, 64])
for column, resolution in enumerate([32, 64]):
    x = np.arange(resolution) / resolution
    for values, label, color in [(operator_arrays[f'input_{resolution}'][0], tr('初始', 'Initial'), '#aaa'),
                                 (operator_arrays[f'target_{resolution}'][0], tr('真实终态', 'Exact final'), '#183a4c'),
                                 (operator_arrays[f'prediction_{resolution}'][0], 'FNO', '#bd653f')]:
        axes[0, column].plot(x, values, label=label, color=color)
    axes[0, column].set(xlabel='x / L', ylabel=tr('场值', 'Field value'), title=f'N={resolution}')
    axes[0, column].legend(fontsize=8)
    error = operator_arrays[f'prediction_{resolution}'] - operator_arrays[f'target_{resolution}']
    im = axes[1, column].imshow(error, aspect='auto', extent=[0, 1, 24, 0], cmap='RdBu_r', vmin=-error_limit, vmax=error_limit)
    axes[1, column].set(xlabel='x / L', ylabel=tr('独立函数编号', 'Held-out function'), title=tr('全部24个函数的误差', 'Errors for all 24 held-out functions'))
    fig.colorbar(im, ax=axes[1, column], label=tr('预测−真实', 'Predicted−exact'))
ft = np.array(fno_trace)
axes[0, 2].semilogy(ft[:, 0], ft[:, 1], label=tr('训练批次', 'Training batch'), color='#267b7d')
axes[0, 2].semilogy(ft[:, 0], ft[:, 2], label=tr('验证函数', 'Validation functions'), color='#bd653f')
axes[0, 2].set(xlabel=tr('更新次数', 'Updates'), ylabel='MSE', title=tr('按验证函数选择权重', 'Select by validation functions'))
axes[0, 2].legend(fontsize=8)
modes = np.arange(0, 9)
axes[1, 2].semilogy(modes, np.exp(-nu * (2 * np.pi * modes)**2), 'o-', color='#267b7d')
axes[1, 2].axvspan(.5, 4.5, color='#267b7d', alpha=.1)
axes[1, 2].set(xlabel=tr('Fourier模式 k', 'Fourier mode k'), ylabel=tr('精确衰减因子', 'Exact attenuation'), title=tr('高频更快消退', 'High frequencies decay faster'))
save(fig, 'operator')

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), layout='constrained')
axes[0].plot(time, true_derivative[0], color='#183a4c', label=tr('真实导数', 'Exact derivative'))
axes[0].plot(time, raw_derivatives[0], color='#bbb', alpha=.6, label=tr('直接差分', 'Finite difference'))
axes[0].plot(time, estimated_derivatives[0], color='#bd653f', label=tr('局部多项式导数', 'Local-polynomial derivative'))
axes[0].set(xlabel=tr('时间 / min', 'Time / min'), ylabel='du/dt / min$^{-1}$', title=tr('A  求导会放大噪声', 'A  Differentiation amplifies noise'))
axes[0].legend(fontsize=8)
axes[1].bar(np.arange(4) - .18, [0, 1.2, -.8, 0], .36, label=tr('真实', 'True'), color='#183a4c')
axes[1].bar(np.arange(4) + .18, coefficients_sindy, .36, label=tr('识别', 'Identified'), color='#bd653f')
axes[1].set(xticks=np.arange(4), xticklabels=['1', 'u', 'u²', 'u³'], ylabel=tr('系数 / min$^{-1}$', 'Coefficient / min$^{-1}$'), title=tr('B  从候选库选择表达式', 'B  Select terms from a library'))
axes[1].legend(fontsize=8)
axes[2].plot(rollout_time, logistic(rollout_time, .8), color='#183a4c', label=tr('真实', 'True'))
axes[2].plot(rollout_time, identified, '--', color='#bd653f', label='SINDy')
axes[2].axvline(4, color='#aaa', ls=':')
axes[2].set(xlabel=tr('时间 / min', 'Time / min'), ylabel=tr('无量纲状态 u', 'Dimensionless state u'), title=tr('C  新初值与更长时间', 'C  New initial state and longer time'))
axes[2].legend(fontsize=8)
save(fig, 'discovery')

fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
for key, color in [('euler', '#bd653f'), ('symplectic', '#267b7d')]:
    label = tr('显式Euler', 'Explicit Euler') if key == 'euler' else tr('辛Euler', 'Symplectic Euler')
    axes[0].plot(position[key], momentum[key], color=color, label=label)
    axes[1].plot(np.arange(401)*.1, energy[key], color=color, label=label)
axes[0].set(xlabel='q', ylabel='p', title=tr('相平面轨迹', 'Phase-space trajectory'))
axes[0].set_aspect('equal')
axes[0].legend(fontsize=8)
axes[1].axhline(.5, color='#aaa', ls='--')
axes[1].set(xlabel=tr('无量纲时间', 'Dimensionless time'), ylabel=tr('能量 H', 'Energy H'), title=tr('离散更新改变长期能量', 'Discrete updates change long-time energy'))
axes[1].legend(fontsize=8)
inset = axes[1].inset_axes([.13, .42, .48, .43])
inset.plot(np.arange(401)*.1, energy['symplectic'], color='#267b7d', lw=.8)
inset.axhline(.5, color='#aaa', ls='--', lw=.7)
inset.set(ylim=(.47, .53), title=tr('辛Euler：能量放大', 'Symplectic energy: zoom'))
inset.tick_params(labelsize=7)
inset.title.set_fontsize(8)
save(fig, 'structure')

summary = {
    'pinn': {'inside_max_abs_error': float(np.max(np.abs(pinn[tau <= 1] - exact[tau <= 1]))),
             'outside_max_abs_error': float(np.max(np.abs(pinn[tau > 1] - exact[tau > 1]))),
             'independent_residual_rmse': float(np.sqrt(np.mean(pinn_residual**2))),
             'initial_condition_error': abs(float(pinn[0])-1), 'updates':1600},
    'inverse': {'true_k':.35, 'estimated_k':estimated_k, 'step':dt,
                'automatic_gradient':automatic_gradient, 'finite_gradient':finite_gradient,
                'gradient_relative_error':abs(automatic_gradient-finite_gradient)/abs(automatic_gradient)},
    'operator': {'train_functions':96, 'validation_functions':24, 'test_functions':24,
                 'selected_step':best_step, 'resolutions':operator_results},
    'sindy': {'coefficients':coefficients_sindy.tolist(), 'active_terms':int(np.count_nonzero(coefficients_sindy)),
              'derivative_rmse_raw':float(np.sqrt(np.mean((raw_derivatives[:,10:-10]-true_derivative[:,10:-10])**2))),
              'derivative_rmse_smooth':float(np.sqrt(np.mean((estimated_derivatives[:,10:-10]-true_derivative[:,10:-10])**2))),
              'heldout_rollout_max_error':float(np.max(np.abs(identified-logistic(rollout_time,.8))))},
    'structure':{'euler_final_energy':float(energy['euler'][-1]),
                 'symplectic_energy_min':float(energy['symplectic'].min()),
                 'symplectic_energy_max':float(energy['symplectic'].max())},
    'hand':{'euler_k05_h2_final':float(euler_cooling(.5,2)[1][-1]),
            'euler_k05_h4_final':float(euler_cooling(.5,4)[1][-1]),
            'heat_mode1_factor':float(np.exp(-.01*(2*np.pi)**2))}
}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
np.savez_compressed(out/'experiment.npz',tau=tau,pinn=pinn,exact=exact,
                    collocation=collocation.numpy(),pinn_trace=trace,pinn_test_residual=pinn_residual,
                    obs_time=obs_time,observations=obs,inverse_trace=inverse_trace,
                    operator_coefficients=coefficients,fno_trace=fno_trace,
                    sindy_time=time,sindy_clean=clean,sindy_noisy=noisy,
                    sindy_derivatives=estimated_derivatives,sindy_coefficients=coefficients_sindy,
                    rollout_time=rollout_time,identified_rollout=identified,
                    euler_energy=energy['euler'],symplectic_energy=energy['symplectic'],**operator_arrays)
print(json.dumps(summary,indent=2))
```

第一次阅读代码时，可以先跟随simulator中的温度列表：每个新值由前一个值和冷却率计算得到，最终观测误差沿这条链求导。然后查看SpectralLayer，注意网格长度由当前输入决定，而频率通道权重不随网格长度重建；这解释了32点训练后怎样在64点输入上计算。最后读候选库与阈值回归循环，手动改变某个候选项或噪声水平，观察方程项、导数误差和长时间轨迹是否一起变化。每一部分都能连接到前面一幅具体的图。

选用科学机器学习方法时，先列出已有信息和待求对象会更清楚。已知方程只需少量求解，可以从成熟数值方法开始；许多相关条件要反复求解，可以评估算子代理的训练成本与后续计算收益；需要识别少量参数，可以让观测通过可微模拟器约束它们；未知机制希望写成可读表达式，可以从有物理含义的候选库开始。无论选哪条路线，都把单位、边界、数据划分和误差定义放在模型旁边，结果才容易被下一位研究者继续使用。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M29.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Physics Informed Deep Learning](https://maziarraissi.github.io/PINNs/)

   连续时间残差、初边值与参数发现。
2. [Fourier Neural Operator for Parametric PDEs](https://arxiv.org/abs/2010.08895)

   原始算子学习论文与历史。
3. [NeuralOperator: Fourier Neural Operators](https://neuraloperator.github.io/dev/theory_guide/fno.html)

   频率层、局部项与分辨率变化。
4. [Discovering governing equations by sparse identification](https://arxiv.org/abs/1509.03580)

   稀疏候选库与方程发现。
5. [PySINDy documentation](https://pysindy.readthedocs.io/en/stable/)

   系统辨识与可扩展实现。
6. [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)

   独立轨迹求解与误差容差。
7. [Hamiltonian Neural Networks](https://arxiv.org/abs/1906.01563)

   可学习Hamiltonian与连续守恒。
8. [Fourier, Théorie analytique de la chaleur (1822)](https://www.e-rara.ch/zut/content/titleinfo/6187666)

   热传导与Fourier表示的原始专著。

   Historical work linked; no scanned image reproduced
9. [Universal Differential Equations for Scientific Machine Learning](https://arxiv.org/abs/2001.04385)

   把可学习结构嵌入已知动力学。

   Primary paper
10. [PySINDy STLSQ](https://pysindy.readthedocs.io/en/latest/generated/pysindy.optimizers.STLSQ.html)

    阈值回归、列缩放与重拟合。

    Official documentation
