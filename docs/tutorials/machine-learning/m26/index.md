# 让训练跑得明白：精度、内存、并行与恢复

Source: https://ml-biomat.com/tutorials/machine-learning/m26/
Language: zh-CN

先找到时间和内存花在哪里，再把一个正确的训练目标拆给更多计算资源。

## 训练慢，先找出谁在等待

一家餐馆想更快出餐，增加厨师可能有用，也可能只是让更多人站在灶台前等待：食材还没洗好，炉灶已经占满，或者打包台跟不上。训练神经网络也有这样的分工。数据要读取、解码和组成批次，模型要完成前向与反向计算，优化器要更新参数，多台设备之间还要交换信息。训练系统研究的就是这些环节如何配合。它直接决定同样的研究时间能尝试多少实验，以及一个模型是否能放进现有内存并稳定训练。

历史上的模型设计也受硬件约束影响。D2L讨论原始AlexNet时展示了因当时GPU内存有限而划分网络的安排；后来，数据并行成为扩大训练规模的常用起点。2020年的PyTorch Distributed论文进一步讨论了梯度分桶与计算通信重叠：数学上相同的梯度平均，执行顺序不同，设备等待时间也会不同。规模增长推动的并非只有更多参数，还包括对数据流、存储位置和通信时机更细的安排。理解这些安排，才能判断一项优化究竟改变了哪里。

$$
\mathcal T=\frac{n}{t},\qquad S_k=\frac{t_1}{t_k},\qquad \eta_k=\frac{S_k}{k}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6949af36f16986b61ff8e11.svg) | 吞吐量、完成的样本数和耗时；单位分别样本/秒、样本、秒。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2ffd5956fec03f6c157ead5e.svg) | k为设备数；t1、tk为同一工作量在1个和k个设备上的耗时，均为秒。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e5bf4c99d933c2bd4d88b49.svg) | 加速比和并行效率，均无量纲。 |

处理960个样本用了2秒，吞吐量480样本/秒。若相同工作量单设备用4秒、4设备用1.5秒，加速比约2.67，效率约0.667。比较时必须固定工作量；只把每设备批次保持不变会同时扩大总批次。

吞吐量描述单位时间完成多少样本，延迟描述一次请求或一次更新等多久；两者相关，却不等同。大批次可能提高吞吐量，同时让单个样本等待更久。比较训练速度时，应同时记录每步样本数、更新次数、精度、模型与设备设置。对GPU计时还要处理异步执行：CPU提交工作之后可能很快返回，而GPU仍在计算，使用相应同步或设备事件才能测量实际完成时间。第一次编译、内存分配和缓存预热也应与稳定运行阶段分开。

![真实CPU剖析与独立计时。上图为预热后3步Adam训练的分析器范围；左下按自身CPU时间列出算子；右下为SGD完整更新的12组计时，每组5次，横线取中位数。两部分的优化器与测量开销不同，不能把范围长度直接相加当作右下的速度。](https://ml-biomat.com/static/tutorials/machine-learning/figures/8ebf563822aa78bf1f133a93.svg?v=8ebf563822aa)

图 1真实CPU剖析与独立计时。上图为预热后3步Adam训练的分析器范围；左下按自身CPU时间列出算子；右下为SGD完整更新的12组计时，每组5次，横线取中位数。两部分的优化器与测量开销不同，不能把范围长度直接相加当作右下的速度。

本章使用54,147参数的小网络，在CPU上实际运行。图的上半部分来自分析器记录的三个训练步，能看到前向、损失、反向和Adam更新各占什么范围；右下则是另行计时的SGD完整更新，每组5次，共12组。分析器本身会增加开销，两部分不能直接相加或相除。这里的重点是先建立一份可读的成本分解，再检查改变精度、内存策略或并行方式后，结果与计算目标是否仍然一致。

## 把数据及时送到计算发生的地方

训练代码中的一行“取下一批数据”，背后可能包含许多工作。图像需要读取压缩文件、解码、裁剪并转为张量；文本需要分词、截断或补齐；表格需要解析字符串并转换类型。若这些步骤比一次模型计算还慢，加快矩阵乘法就无法消除等待。Dataset负责定义如何取得样本，DataLoader负责采样、组织批次和必要的并行读取；把这两层分开，可以分别判断数据准备与模型计算的成本。

批处理通常能减少重复调度，使一次矩阵运算处理更多样本。变长序列还有额外问题：把长度20与长度2000的文本放在同一批，补齐部分可能占去大多数计算。按长度分组、使用掩码，或者按有效token数而不是样本数组织批次，都能更准确地控制工作量。对应的损失也要按有效元素计数，否则两台设备虽然各有八条文本，却可能对总体目标贡献不同数量的token。数据组织与数学归约方式因此相互联系。

缓存适合重复使用而又不变化的结果，例如确定性的文件解码或固定分词。随机裁剪与颜色增强若在第一次读取后就固定缓存，后续轮次便失去原本的随机变化；训练集标准化参数也不能利用测试集来计算。多工作进程可以提前准备数据，但会增加进程启动、复制与调度成本，小型内存数据未必受益。在使用GPU时，页锁定内存和合适的异步传输能帮助主机与设备搬运重叠；它们的收益需要结合实际传输量与时间线判断。

程序把同一份768×32数值保存为CSV和NPY，并在预热后测量整份读取，再单独测量从内存复制96行的成本。CSV与NPY对照说明文本解析和二进制读取的差别；缓存项对应已经准备好数据之后取一个批次。三项的工作量标在图注中，不能把较小批次复制的时间直接当成一种文件格式的加速比。数据很小时，先把确定性准备移出训练循环，经常比增加读取进程更容易解释和维护。

## 拆开批次以后，怎样保持同一个训练目标

内存装不下一个大批次时，可以一次处理其中一部分，把梯度累积起来，最后只更新一次参数。这里最容易混淆的是“算了几次反向”和“更新了几次参数”。如果每个小批次都立刻执行optimizer.step，后一个小批次看到的参数已经改变，过程自然不同；梯度累积则让所有小批次对同一组参数求导。每次新大批次开始时清零梯度，中间只追加，全部完成后再更新，才对应我们想计算的全批次平均。

$$
B_{\rm eff}=RKA,\qquad \nabla_\theta L=\sum_{j=1}^{m}\frac{n_j}{N}\nabla_\theta L_j,\quad N=\sum_{j=1}^{m}n_j
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a3576044580388006267924f.svg) | 一次更新的有效样本数、数据并行副本数、每副本微批样本数、累积次数；无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa030f8ff794ca3a6b386c6.svg) | j为微批编号，m为微批数量，nj为第j批样本数，N为总数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eed48cd34399b8bb5c47bae6.svg) | θ为所有模型参数；L和Lj为整体及微批的样本平均损失，梯度对相同参数求导。本例交叉熵及参数均无量纲。 |

4副本、每批8个样本、累积3次，更新看到了96个样本。若96个样本分成17、31、48条三批，其平均损失需按17/96、31/96、48/96加权；平均三个均值会让每条小批样本获得更大权重。

完整实验从相同参数出发，用前96个样本算一次平均交叉熵梯度，再分成17、31、48三个小批次。正确实现把每批损失求和后除以96，三个反向结果自然累加；错误对照则把三个小批次的均值等权平均。前者与全批梯度的最大差约7.45×10⁻⁹，属于浮点加法顺序产生的小差异；后者达到0.01188，因为每条样本的权重已被改变。均值听起来相同，分母不同却会直接改变优化目标。

这个等价关系依赖计算本身能够按样本相加。BatchNorm使用当前批次的均值和方差，把大批拆小会改变前向输出；跨样本对比损失的负例集合也会变小。Dropout等随机操作还需要考虑随机数对应关系。因而实验在梯度等价性部分关闭Dropout，使用没有BatchNorm的网络，把要检验的对象限定为样本平均损失及其归约。恢复实验再单独打开Dropout，检查随机状态是否被正确保存，两个问题各有对应的对照。

数据并行与梯度累积可以组合。四个副本每次各处理八个样本，累计三次才更新，有效批大小是96；若每个副本的最后一批不足八个，就应根据实际样本数或有效token数加权。在DDP中，累积的中间步骤可使用no_sync减少不必要的梯度同步，最后一步再触发聚合；前向也应位于相应上下文中。学习率调度和日志中的“step”最好明确是微批步还是优化器更新步，否则同一个训练配置会出现不同的时间尺度。

## 少存一些数，或者把一部分数重新算出来

浮点格式用有限位数表示数值，需要同时考虑能覆盖多大的范围，以及相邻数字之间有多细的间隔。FP16和BF16都占16位，但指数与有效数字的分配不同：BF16保留接近FP32的指数范围，尾数更短；FP16在相近数量级上通常更细，却更容易遇到很小梯度下溢或大数溢出。图中的实际类型转换能看出这种区别：1e−8转FP16成为0，转BF16仍保留近似值；1.001转BF16则可能直接舍入到1。

$$
\tilde L=sL,\qquad \tilde g=\nabla_\theta\tilde L=sg,\qquad g=\tilde g/s
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0e3d81b121b61d9889e7e249.svg) | 原损失、放大后的损失和正缩放因子s；s无量纲，真实训练可动态调整。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7a28a623c4c68e362e8f21c5.svg) | 参数、原梯度与放大梯度；梯度向量形状同参数，恢复后才用于更新或按原尺度裁剪。 |

1e−8直接转成FP16会变成0。先乘65536，转成FP16，再以FP32除回65536，实验得到约9.99717e−9。缩放扩大可表达的小梯度；若放大导致溢出，需要降低缩放因子并跳过该次无效更新。

自动混合精度不是把整个模型文件都改为半精度。autocast按算子选择计算类型，让适合低精度的矩阵运算使用低精度，而某些归约和损失继续使用更稳定的类型。FP16训练常配合梯度缩放，先放大损失，反向后再把梯度除回；做梯度裁剪前要先恢复原尺度。CPU上的BF16示例通常只需要autocast。本章实际使用CPU BF16运行前向与损失，反向在上下文之外执行，梯度相对FP32最大差约0.000817。

这台CPU上的BF16更新中位时间约10.48毫秒，FP32约0.60毫秒，重计算版本约1.19毫秒。低精度在这组硬件与小矩阵条件下更慢，说明数据类型名称本身并不决定速度；硬件指令、内核实现、矩阵大小与转换开销共同决定结果。这些数值来自一次测量，重新运行会随系统负载变化。用于判断正确性的梯度对照则回答另一个问题：精度变化究竟让数值偏离多少，后续训练效果需要在同样的数据划分下继续评价。

![左图统计前向保留供反向使用的非参数张量底层存储，按地址去重，含输入切片保留的完整数据存储，不是峰值进程内存。右上比较梯度差；DDP一行比较SGD更新后的参数差。右下为实际浮点类型转换。全部使用同一96样本与参数起点，重计算差为0。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5f46d9e0d932caf0d9b4dd35.svg?v=5f46d9e0d932)

图 2左图统计前向保留供反向使用的非参数张量底层存储，按地址去重，含输入切片保留的完整数据存储，不是峰值进程内存。右上比较梯度差；DDP一行比较SGD更新后的参数差。右下为实际浮点类型转换。全部使用同一96样本与参数起点，重计算差为0。

激活检查点处理的是反向传播需要保存的中间结果。普通前向把若干张量保留下来，反向时直接使用；检查点只保留必要入口，在反向经过该区域时重新计算中间量。因此它用额外计算换取较少的保留存储。代码把四层特征网络包进非重入checkpoint，同一批次梯度差为0，保留的非参数底层存储从302,212字节降到154,756字节。这个统计按存储地址去重，包含输入切片引用的完整底层数组，表示前向结束后的保留量；峰值内存、通信缓冲和优化器状态需要另外测量。

## 数据并行：每个副本计算一部分，再共同更新

数据并行给每个设备一份完整模型，分配不同的样本，让它们分别计算局部梯度。聚合之后，各设备拿到相同的全局梯度，再以相同优化器状态更新，所以参数副本继续一致。它很像几个人分别核算一份调查表的不同部分，最后把总和与总人数汇合，得到共同平均值。真正重要的是先把哪些量相加、在哪里除以数量说清楚，而不是先记住一个分布式接口名字。

$$
g=\frac1R\sum_{r=1}^{R}g_r,\qquad \theta_{\rm new}=\theta-\lambda g
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/50ec721002628c3a35b08389.svg) | R为等大批次的副本数，r为副本编号，gr为局部样本平均梯度，g为全批平均梯度；向量形状均与θ相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/70b0887f0d88757fc638b64a.svg) | 更新前后参数向量；λ为学习率，本章SGD对照取0.05，交互示例取0.1，均采用无量纲模型。 |

两份梯度[1,3]和[3,1]求和得[4,4]，除以2得[2,2]。若θ=[1,1]、学习率0.1，两台设备都更新为[0.8,0.8]。同参数起点、同聚合梯度、同优化器状态，才会保持副本同步。

![双GPU数据拆分、局部梯度计算、梯度聚合与参数更新的原始教学图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/09b6c97cf764f398a536944b.svg?v=09b6c97cf764)

图 3D2L图13.5.3：两台GPU分别计算局部梯度，再聚合并同步更新。原图未改动。来源：Dive into Deep Learning，Training on Multiple GPUs，CC BY-SA 4.0；图中的硬件用于说明数据流，本章运行的是两CPU进程。

程序确实启动两个本机CPU进程，通过Gloo建立进程组，每个进程处理48条数据。DDP在反向过程中同步局部平均梯度，两者各完成一次学习率0.05的SGD更新。最后两个参数副本的差为0，与单进程96条全批次更新的最大差约7.45×10⁻⁹。额外的整数向量all-reduce把[1,1]与[2,3]相加，两进程都得到[3,4]，提供一个容易手算的通信核对。这个实验验证的是同步与更新关系，没有把CPU进程当成两张GPU的速度测量。

DDP构造时会同步模型初始状态，并将梯度组织成桶。反向从后面的层逐渐得到梯度，一个桶就绪后可以先开始通信，同时继续计算其他层；桶过大可能延迟通信启动，桶过小又会增加启动次数。所有进程必须以一致顺序参与集合通信，一方提前结束、跳过某个分支或遇到未处理异常，其他进程便可能等待。分布式训练中的“卡住”因此常常与程序路径、数据数量和通信顺序有关，而不只是算力不足。

数据采样也要分工。多个副本若各自遍历完全相同的数据，只是重复计算；分布式采样器负责把样本分给各进程，跨轮次还需要更新随机打乱。验证集的最后部分若为了凑齐副本数而重复填充，计算准确率时应避免把重复样本当成新的观测。DDP主要解决副本同步，数据划分、有效损失分母和评价统计仍由训练程序决定。先用一个能够手算的小批次核对更新，再扩大任务，能更容易发现这些接口之间的错位。

## 模型太大时，哪些东西必须每台都保存

训练占用的存储不只有权重。每个参数可能还有梯度、Adam的一阶和二阶矩，以及用于稳定更新的FP32主权重；前向激活、临时工作区和通信缓冲再叠加上来。数据并行把完整状态复制到每台设备，增加设备数量不会自动缩小单份模型。ZeRO研究的出发点就是减少这种冗余：先分片优化器状态，再分片梯度，最后连参数也分片，让不同设备负责不同部分。

$$
M_{\rm DDP}=P(b_w+b_g+b_o),\quad M_1=P(b_w+b_g+b_o/R),\quad M_2=P(b_w+b_g/R+b_o/R),\quad M_3=P(b_w+b_g+b_o)/R
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6c04a51457034e5d812d0a8f.svg) | P为参数个数，R为分片设备数，均为无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7faaeb05f8055dcd7d9fc9c5.svg) | 每参数权重、梯度、主权重加优化器状态的字节数。本例分别2、2、12；12=4字节主权重+两个4字节Adam矩。 |
| ![Formula](https://ml-biomat.com/static/agent-math/392337d6f3490ca179980f20.svg) | 每设备的持久状态字节数，依次对应完整复制和ZeRO第1、2、3阶段；不含激活、暂存参数、通信缓冲与分配器开销。 |

P=1亿、R=4时，DDP为1.6 GB，三个分片阶段分别0.7、0.55、0.4 GB；GB按10⁹字节计。不同实现的梯度精度和主权重策略不同，应先确定bw、bg、bo再代入。

字节预算需要先说明实现约定。图中假定低精度参数2字节、梯度2字节、FP32主权重4字节、两份Adam矩共8字节，所以每参数总计16字节。对于1亿参数、4设备，完整复制每设备1.6 GB；依次分片后为0.7、0.55和0.4 GB。这是持久模型状态的解析预算。若采用FP32梯度、没有独立主权重，或使用不同优化器，就应该更改各项字节数，不能把“每参数16字节”当成所有训练程序的固定常数。

FSDP提供了把分片状态接入模型执行的方式。一个模块即将计算时，设备通过all-gather收齐该模块所需参数；局部反向产生的梯度通过reduce-scatter聚合并分回负责的设备，优化器只更新本设备持有的状态。需要时再为后续计算收集参数。分片降低持久存储，却会产生参数暂存与通信；提前预取下一个模块有机会隐藏等待，也会让更多参数同时驻留。模块划分的粒度因而决定了通信次数、峰值存储与可重叠程度。

下面的交互把同一组梯度与存储预算放在一起。每个进程的局部梯度按明确公式给出，逐步执行可以观察局部值、平均值与更新后权重；切换分片阶段则改变每设备负责的持久状态。它展示的是数据流和解析字节预算，真实设备上的临时峰值与通信时间需回到分析器测量。先确认一项优化省掉的是权重副本、优化器副本还是激活，才能判断它是否对准当前内存瓶颈。

## 一个梯度怎样在多个进程间形成共同更新

示意梯度由进程编号与参数编号生成：两者先各加1，相乘后除以10。所有权重初值为1，学习率0.1；假设各进程批次一样大。存储预算另按输入的真实参数规模计算，采用2字节权重、2字节梯度、12字节主权重及Adam状态。

[Figure: 一个梯度怎样在多个进程间形成共同更新](https://ml-biomat.com/tutorials/machine-learning/m26/#M26-plot)

手动推进只改变计算阶段；不同分片方式保持同一个数学更新，改变的是状态归属。每设备预算相等，激活与临时缓冲单独计算。

## 分张量、分网络阶段，还是分给不同专家

张量并行把一次较大的矩阵运算拆给多个设备。按输出列分割权重时，每台计算不同输出特征，结果按列拼起来；按输入维分割时，各台算的是同一输出的部分和，最后必须相加。这个区别决定了何时需要通信。注意框架中线性层权重常按“输出×输入”存储，讨论行列分片时应以实际矩阵乘法与布局为准。先在纸上写出输入、权重与输出形状，可以避免把存储轴名称误当成计算含义。

$$
X[W_1\ W_2]=[XW_1\ XW_2],\qquad [X_1\ X_2]\begin{bmatrix}V_1\\V_2\end{bmatrix}=X_1V_1+X_2V_2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5a413b9be6c9314d81d66a65.svg) | X为B×d输入；W1、W2分别为d×h1、d×h2的输出列分片。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3b1e83b6383456601d77026e.svg) | X1、X2为B×h1、B×h2的输入特征分片；V1、V2为h1×o、h2×o权重行分片。 |
| ![Formula](https://ml-biomat.com/static/agent-math/16c8746d45b4db3ecf180d6c.svg) | B为批大小，其余字母为特征维度，都是计数；方括号表示按所示轴拼接，加号为同形状张量逐元素求和。本例数值无量纲。 |

输入[2,3]、权重列[1,4]与[5,6]分别产生14和28，按列拼接得[14,28]。若后续求这两项乘1与2的和，两份部分结果为14和56，需要相加得70。列分片产生不同输出，行分片产生同一输出的部分和。

流水线并行则按层把模型分成阶段。一个微批经过第一阶段后送入第二阶段，第一阶段同时处理下一个微批，像装配线逐件流动。启动时后面的阶段还没收到输入，结束时前面的阶段已经没活可做，这些空闲时间称为气泡。增加微批数能提高理想利用率，但也改变调度与保留激活的需求。GPipe采用先完成一组前向、再做反向的安排，1F1B在预热后交替安排一次前向与一次反向，以改变中间存储和等待关系。

$$
U_{\rm forward}=\frac{m}{m+p-1},\qquad V_{\rm ring}\approx 2\frac{R-1}{R}G
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2ad69b22eb61d6cb4d522b0f.svg) | 理想前向流水线利用率、微批数、等耗时阶段数。U无量纲，模型只计一次前向、忽略通信且所有阶段时长相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3d589cb45d7033d3fb72f837.svg) | 环形all-reduce每进程发送的近似字节数、进程数与完整梯度消息字节数；不含接收量、协议头与延迟。 |

4个微批通过3个等时阶段，需要4+3−1=6个时间槽，每阶段工作4槽，利用率2/3。另一个独立例子中，4进程归约200 MB梯度，每进程发送约300 MB；它描述通信量，不直接给出耗时。

![两种解析图。左图按每参数2字节权重、2字节梯度、12字节主权重及Adam状态，计算1亿参数、4设备的持久状态预算；激活与临时缓冲另计。右图是4微批、3等时阶段的理想前向调度，格内数字是微批编号，不是实测多GPU时间线。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b1fb97ebe1a0f48fd49ee039.svg?v=b1fb97ebe1a0)

图 4两种解析图。左图按每参数2字节权重、2字节梯度、12字节主权重及Adam状态，计算1亿参数、4设备的持久状态预算；激活与临时缓冲另计。右图是4微批、3等时阶段的理想前向调度，格内数字是微批编号，不是实测多GPU时间线。

图中四个微批通过三个等时阶段，前向需要六个时间槽，每个阶段实际工作四槽，利用率为三分之二。这个小图只计算前向并忽略通信；完整训练还包括反向、阶段时长差异和调度约束。旁边的环形all-reduce公式同样是通信量模型：四进程归约200 MB梯度，每进程约发送300 MB，不等于“需要多少毫秒”。实际耗时还取决于带宽、启动延迟、拓扑，以及这段通信有多少被计算覆盖。

专家并行利用的则是模型的条件计算结构。一个token经路由器选中少数专家，只发送到这些专家所在设备；专家完成计算后，再把结果送回原序列位置。Switch Transformer所代表的稀疏专家路线让总参数量与每个token激活的参数量有所分离。代价在于token搬运和负载分配：若大多数token都选择同一个专家，其设备会变成瓶颈；专家容量、辅助平衡目标以及溢出token的处理方式，都会影响实际训练目标与效率。

这些并行方式可以沿不同设备维度组合。张量并行频繁交换层内结果，适合通信较快的设备组；数据并行或参数分片可以在另一维处理不同批次与状态；流水线再把网络阶段分开。组合时还要核对有效批大小：参与同一个样本张量计算的设备不能再次计入数据并行副本数。一个八设备系统若每四台合作处理一个模型分片组，只有两个数据并行副本。设备总数、模型分片数和独立样本副本数，各自回答不同的问题。

## 保存权重，不等于保存了训练过程

读书时记住当前页码，便能从那里继续；训练的“页码”却不止一个。除了模型参数，Adam积累的矩、学习率调度器位置、混合精度缩放器、随机数状态和数据采样位置，都可能影响下一步。只加载权重仍能进行推理，也能开始新的训练，但如果目标是接着原过程往下走，就需要恢复这些决定下一步的状态。保存时最好放在完整优化器更新结束之后；若选择在梯度累积中途保存，已累积梯度和微批进度也要一起记录。

本章用带Dropout的网络完成12次Adam更新，在第6次更新后保存模型、优化器、随机数状态和已完成步数。随后一条路径继续训练，另一条路径重新建立网络并加载完整检查点，再从相同随机状态开始。后六次损失与最终参数的差都为0。对照组只恢复模型权重，同时仍恢复相同随机数状态，以单独观察丢失Adam状态的影响；最终参数最大差约0.02484，曲线也开始分开。这里“只恢复权重”后损失较低并不改变对照目的：它已经是一条不同的优化轨迹。

![左图在第6次Adam更新后保存：完整状态恢复曲线与不中断训练重合；只恢复权重的对照保留相同随机数状态，但丢弃Adam状态，后续轨迹分开。右图是预热后的数据操作计时：CSV与NPY读取全部768×32数据，缓存项只复制当前96行，分别对应准备整份数据与取一个训练批次。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5a1a66e2d8e26b920fb43545.svg?v=5a1a66e2d8e2)

图 5左图在第6次Adam更新后保存：完整状态恢复曲线与不中断训练重合；只恢复权重的对照保留相同随机数状态，但丢弃Adam状态，后续轨迹分开。右图是预热后的数据操作计时：CSV与NPY读取全部768×32数据，缓存项只复制当前96行，分别对应准备整份数据与取一个训练批次。

多进程恢复还需要共享一个一致的进度点。各进程保存的分片属于同一更新版本，重新启动时要让模型、优化器与数据分配对应起来。若设备数量变化，分片检查点可能需要重新分配，采样器也会产生新的划分方式。工程上可先写临时文件，确认所需分片齐全，再更新一个描述完整版本的清单；恢复时按清单选择已完成版本。通信超时与故障处理也应让所有进程明确结束或一起重启，避免某一方继续使用过期状态。

检查点频率是一项成本取舍。频繁保存会消耗带宽与存储，间隔过长则会在中断后重算更多工作。可以测量单次保存耗时，再结合可接受的重算步数安排间隔。还应实际进行一次“保存—重启—下一步”的核对，比只确认文件存在更有信息。激活检查点与训练检查点虽然英文都叫checkpoint，作用不同：前者在一次反向过程中重新计算中间量，后者把训练状态写到持久存储，供进程重新启动后恢复。

## 在PyTorch、JAX与Keras中寻找同一个计算

切换框架时，最值得保留的是训练目标、参数状态和数据布局。PyTorch的常见写法让参数保存在Module中，loss.backward把梯度写到参数的grad字段，再由优化器更新。JAX常把参数作为函数输入，用value_and_grad同时返回损失与梯度，再显式产生更新后的参数结构；随机数也通常通过显式键传递。两种写法的外观不同，仍可以用同一个两样本模型检查它们是否在算相同的平均损失。

$$
L(w)=\frac{(w\cdot1-2)^2+(w\cdot2-4)^2}{2},\qquad \left.\frac{dL}{dw}\right|_{w=1}=-5,\qquad w_{\rm new}=1-0.1(-5)=1.5
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/623266ad2e97a6418b22b401.svg) | 标量线性模型权重、更新后权重与两样本平均平方误差，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b215ca6388be117e2b4987b8.svg) | 输入为1、2，目标为2、4，学习率0.1；dL/dw为损失对权重的导数。 |

在w=1时，两个预测误差为−1和−2，平均平方误差为2.5；导数是两项“误差×输入×2”再平均，得到−5。三种框架只要使用相同均值、形状和更新规则，应计算同一答案。

在JAX中，grad把标量函数转换为梯度函数，vmap把针对单样本的计算映射到批次，jit把可追踪的计算编译执行。首次调用可能需要编译，后续调用复用编译结果，因此计时时要区分两者，并等待异步结果真正完成。涉及设备布局时，Mesh描述设备组成，PartitionSpec描述数组轴沿哪些设备轴分片；没有分片的设备轴可能持有复制数据。一个批次轴分片、特征轴复制的数组，表达的是与数据并行相近的信息分工，布局转换则可能引入通信。

Keras提供fit这样的高层训练入口，也允许覆盖train_step。使用TensorFlow后端时，可在GradientTape中计算前向与损失，再求梯度并交给优化器；training=True决定Dropout等层采用训练行为。tf.distribute.MirroredStrategy维护同步数据并行副本，MultiWorkerMirroredStrategy把这种安排扩展到多机。Keras还支持其他后端，因此“用了Keras”并不能单独说明底层执行与分布式策略。比较实现时，应明确后端、损失归约、随机行为和数据类型。

| 需要表达的事情 | PyTorch | JAX | Keras / TensorFlow |
| --- | --- | --- | --- |
| 计算导数 | autograd与backward | grad / value_and_grad | GradientTape |
| 组织批量运算 | 张量批次维与DataLoader | 数组批次维与vmap | tf.data与批次张量 |
| 编译计算 | torch.compile | jit | tf.function与相应编译设置 |
| 多设备布局 | DDP、FSDP、DeviceMesh | Mesh与分片规格 | distribute.Strategy |

这些对应关系用于寻找同一层职责，并不表示接口可以逐字替换。比如改变均值与求和归约、把标量目标广播到错误维度，或忘记切换训练模式，即使用同一优化器名称也会产生不同更新。本章运行的是PyTorch完整实验，JAX与Keras/TF部分依据各自官方接口讲解同一计算与布局含义。移植时可以先复现上面的2.5损失、−5梯度和1.5新权重，再增加批处理、编译和分布式功能，让每一步变化都有清楚的参照。

## 完整实验：先核对，再测量，再扩大

程序生成768条32维输入，以固定线性教师加噪声产生三类标签。前576条用于随机训练批次，后192条评价；网络有四层128宽隐藏表示和三类输出。训练恢复实验只进行12次更新，测试准确率为133/192，约69.27%，用于确认这是一段实际学习过程。梯度等价性与两进程DDP对照则固定前96条样本，避免把抽样差异混入系统比较。每个CPU进程使用两线程，软件版本与运行设备保存在数值摘要中。

### 完整CPU实验：训练等价性、两进程DDP、性能与恢复

从终端执行此完整文件，--output指定输出目录，--language选择语言。首次运行完成全部测量；加入--render-only用同一份测量生成另一语言图。程序会启动两个本机CPU进程完成Gloo梯度同步，并保存真实分析器范围、随机训练检查点、权重和数据。

```
"""Measure and verify CPU training: accumulation, real DDP, precision and recovery."""
import argparse
import copy
import json
import platform
import time
import uuid
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


class Net(nn.Module):
    def __init__(self, dropout=0.):
        super().__init__()
        self.features=nn.Sequential(nn.Linear(32,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU())
        self.head=nn.Linear(128,3)

    def forward(self,x,recompute=False):
        hidden=checkpoint(self.features,x,use_reentrant=False) if recompute else self.features(x)
        return self.head(hidden)


def make_data():
    generator=torch.Generator().manual_seed(26)
    x=torch.randn(768,32,generator=generator)
    teacher=torch.randn(32,3,generator=generator)
    y=(x@teacher+.25*torch.randn(768,3,generator=generator)).argmax(1)
    return x,y


def new_model(dropout=0.):
    torch.manual_seed(260)
    return Net(dropout)


def flatten(model,grad=False):
    return torch.cat([(p.grad if grad else p).detach().flatten()for p in model.parameters()])


def max_error(a,b):return float((a-b).abs().max())


def gradient_experiments(x,y):
    full=new_model();F.cross_entropy(full(x[:96]),y[:96]).backward();reference=flatten(full,True)
    accumulated=new_model();wrong=new_model();offset=0
    for size in [17,31,48]:
        xb,yb=x[offset:offset+size],y[offset:offset+size]
        (F.cross_entropy(accumulated(xb),yb,reduction='sum')/96).backward()
        (F.cross_entropy(wrong(xb),yb)/3).backward();offset+=size
    bf=new_model()
    with torch.autocast('cpu',dtype=torch.bfloat16):loss=F.cross_entropy(bf(x[:96]),y[:96])
    loss.backward()
    result={'accumulation_gradient_error':max_error(reference,flatten(accumulated,True)),
        'unweighted_microbatch_error':max_error(reference,flatten(wrong,True)),
        'bf16_gradient_error':max_error(reference,flatten(bf,True))}
    opt=torch.optim.SGD(full.parameters(),lr=.05);opt.step()
    return result,flatten(full),reference


def ddp_worker(rank,init_method,output):
    torch.set_num_threads(2)
    dist.init_process_group('gloo',rank=rank,world_size=2,init_method=init_method)
    try:
        x,y=make_data();model=DistributedDataParallel(new_model())
        optimizer=torch.optim.SGD(model.parameters(),lr=.05)
        sl=slice(rank*48,(rank+1)*48)
        optimizer.zero_grad();F.cross_entropy(model(x[sl]),y[sl]).backward();optimizer.step()
        total=torch.tensor([rank+1.,2.*rank+1.]);dist.all_reduce(total)
        torch.save({'parameters':flatten(model.module),'reduction':total},Path(output)/f'ddp-rank{rank}.pt')
    finally:dist.destroy_process_group()


def retained_storage(x,y,recompute):
    model=new_model();saved={};parameter_pointers={p.untyped_storage().data_ptr()for p in model.parameters()}
    def pack(tensor):
        storage=tensor.untyped_storage();ptr=storage.data_ptr()
        if ptr not in parameter_pointers:saved[ptr]=storage.nbytes()
        return tensor
    with torch.autograd.graph.saved_tensors_hooks(pack,lambda t:t):
        loss=F.cross_entropy(model(x[:96],recompute=recompute),y[:96])
    retained=sum(saved.values());loss.backward()
    return retained,flatten(model,True)


def train_steps(model,optimizer,x,y,start,end):
    losses=[]
    for _ in range(start,end):
        index=torch.randperm(576)[:96]
        optimizer.zero_grad();loss=F.cross_entropy(model(x[index]),y[index]);loss.backward();optimizer.step();losses.append(float(loss.detach()))
    return losses


def recovery(x,y,out):
    model=new_model(.2);optimizer=torch.optim.Adam(model.parameters(),lr=.003)
    torch.manual_seed(2026)
    first=train_steps(model,optimizer,x,y,0,6)
    checkpoint_data={'model':copy.deepcopy(model.state_dict()),'optimizer':copy.deepcopy(optimizer.state_dict()),
        'rng_state':torch.get_rng_state(),'completed_updates':6,'architecture':{'inputs':32,'hidden':128,'hidden_layers':4,'outputs':3,'dropout':.2},'learning_rate':.003}
    torch.save(checkpoint_data,out/'training-checkpoint.pt')
    later=train_steps(model,optimizer,x,y,6,12);reference=flatten(model)
    saved=torch.load(out/'training-checkpoint.pt',weights_only=True)
    restored=Net(.2);restored.load_state_dict(saved['model']);restored_opt=torch.optim.Adam(restored.parameters(),lr=.003);restored_opt.load_state_dict(saved['optimizer'])
    torch.set_rng_state(saved['rng_state']);restored_loss=train_steps(restored,restored_opt,x,y,6,12)
    weights_only=Net(.2);weights_only.load_state_dict(saved['model']);fresh_opt=torch.optim.Adam(weights_only.parameters(),lr=.003)
    torch.set_rng_state(saved['rng_state']);weights_loss=train_steps(weights_only,fresh_opt,x,y,6,12)
    model.eval()
    with torch.no_grad():test_accuracy=float((model(x[576:]).argmax(1)==y[576:]).float().mean())
    torch.save(model.state_dict(),out/'trained-model.pt')
    return {'resume_parameter_error':max_error(reference,flatten(restored)),'weights_only_parameter_error':max_error(reference,flatten(weights_only)),
        'resume_loss_error':float(np.max(abs(np.array(later)-restored_loss))),'test_accuracy':test_accuracy},np.array(first+later),np.array(first+restored_loss),np.array(first+weights_loss)


def measure(function,repeats=12,inner=5):
    for _ in range(3):function()
    values=[]
    for _ in range(repeats):
        start=time.perf_counter()
        for _ in range(inner):function()
        values.append((time.perf_counter()-start)*1000/inner)
    return np.array(values)


def timings(x,y,out):
    np.savetxt(out/'features.csv',x.numpy(),delimiter=',',fmt='%.9g');np.save(out/'features.npy',x.numpy())
    paths={'Parse CSV':lambda:np.loadtxt(out/'features.csv',delimiter=',',dtype=np.float32),
           'Read NPY':lambda:np.load(out/'features.npy'),
           'Cached rows':lambda:x[:96].clone()}
    data={k:measure(fn,inner=3)for k,fn in paths.items()}
    steps={}
    for name,amp,recompute in [('FP32',False,False),('CPU BF16',True,False),('Recompute',False,True)]:
        model=new_model();optimizer=torch.optim.SGD(model.parameters(),lr=.05)
        def step():
            optimizer.zero_grad()
            with torch.autocast('cpu',dtype=torch.bfloat16,enabled=amp):loss=F.cross_entropy(model(x[:96],recompute=recompute),y[:96])
            loss.backward();optimizer.step()
        steps[name]=measure(step)
    return data,steps


def profile(x,y,out):
    model=new_model();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for _ in range(3):
        opt.zero_grad();F.cross_entropy(model(x[:96]),y[:96]).backward();opt.step()
    with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],record_shapes=True) as prof:
        for _ in range(3):
            opt.zero_grad()
            with torch.profiler.record_function('forward'):prediction=model(x[:96])
            with torch.profiler.record_function('loss'):loss=F.cross_entropy(prediction,y[:96])
            with torch.profiler.record_function('backward'):loss.backward()
            with torch.profiler.record_function('optimizer'):opt.step()
    events=[{'name':e.name,'start_us':e.time_range.start,'duration_us':e.time_range.end-e.time_range.start}for e in prof.events()if e.name in ['forward','loss','backward','optimizer']]
    start=events[0]['start_us']
    for e in events:e['start_us']-=start
    operators=sorted([{'name':e.key,'self_cpu_us':e.self_cpu_time_total,'calls':e.count}for e in prof.key_averages()if e.key.startswith('aten::')],key=lambda e:e['self_cpu_us'],reverse=True)
    (out/'profile.json').write_text(json.dumps({'events':events,'operators':operators},indent=2),encoding='utf-8')
    trace=[{'name':e['name'],'cat':'training','ph':'X','ts':e['start_us'],'dur':e['duration_us'],'pid':0,'tid':0}for e in events]
    (out/'trace.json').write_text(json.dumps({'traceEvents':trace}),encoding='utf-8')
    return events,operators


def draw(out,lang,summary,data_timing,step_timing,events,operators,curves):
    zh=lang=='zh';plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    colors=['#266d86','#dd8b38','#8a63a2','#4c9276']
    def save(fig,name):
        fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight',facecolor='white');fig.savefig(out/f'{name}-{lang}.png',dpi=155,bbox_inches='tight',facecolor='white');plt.close(fig)
    fig=plt.figure(figsize=(12.7,8.1),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[.85,1])
    ax=fig.add_subplot(gs[0,:]);stages=['forward','loss','backward','optimizer'];names=['前向','损失','反向','参数更新']if zh else['Forward','Loss','Backward','Optimizer']
    for j,e in enumerate(events):
        i=stages.index(e['name']);ax.broken_barh([(e['start_us']/1000,e['duration_us']/1000)],(j//4-.28,.56),facecolors=colors[i])
    for i,n in enumerate(names):ax.plot([],[],lw=7,color=colors[i],label=n)
    ax.set_yticks([0,1,2],['1','2','3']);ax.invert_yaxis();ax.set_ylabel('训练步'if zh else'Training step');ax.set_xlabel('从首个前向开始 / ms'if zh else'Time from first forward / ms');ax.legend(ncols=4,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.26));ax.set_title('CPU 实际分析器范围（包含测量开销）'if zh else'Actual CPU profiler ranges (including measurement overhead)',pad=42)
    ax=fig.add_subplot(gs[1,0]);top=operators[:7];ax.barh(range(len(top)),[o['self_cpu_us']/1000 for o in top],color=colors[0]);ax.set_yticks(range(len(top)),[o['name'] for o in top]);ax.invert_yaxis();ax.set_xlabel('三步累计自身 CPU 时间 / ms'if zh else'Self CPU time across three steps / ms')
    ax=fig.add_subplot(gs[1,1]);labels=['FP32','CPU BF16','重计算'if zh else'Recompute']
    for i,(name,v)in enumerate(step_timing.items()):ax.scatter(np.full(len(v),i)+np.linspace(-.08,.08,len(v)),v,color=colors[i],s=18,alpha=.7);ax.plot([i-.2,i+.2],[np.median(v)]*2,color='#243749',lw=2)
    ax.set_xticks(range(3),labels);ax.set_ylabel('每次更新 / ms'if zh else'Milliseconds per update');ax.set_title('12组计时，每组5次更新'if zh else'12 timing groups, five updates each')
    save(fig,'profile')
    fig=plt.figure(figsize=(12.4,6.6),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1,1.35]);ax=fig.add_subplot(gs[:,0])
    bars=[summary['saved_storage_plain_bytes']/1024,summary['saved_storage_checkpoint_bytes']/1024]
    ax.bar([0,1],bars,color=colors[:2],width=.6);ax.set_xticks([0,1],['普通前向','激活重计算']if zh else['Normal forward','Checkpointed']);ax.set_ylabel('保留的非参数张量存储 / KiB'if zh else'Retained non-parameter storage / KiB');ax.set_title('同一96样本前向，按存储地址去重'if zh else'Same 96 examples; unique storage addresses')
    for i,v in enumerate(bars):ax.text(i,v+4,f'{v:.1f}',ha='center')
    ax.set_ylim(0,max(bars)*1.18)
    ax=fig.add_subplot(gs[0,1]);gradkeys=['accumulation_gradient_error','unweighted_microbatch_error','bf16_gradient_error','checkpoint_gradient_error','ddp_update_error'];labels=['加权累积','等权平均小批','BF16','重计算','两进程 DDP']if zh else['Weighted accumulation','Unweighted microbatches','BF16','Recompute','Two-process DDP']
    vals=[summary[k]for k in gradkeys];ax.barh(range(5),np.maximum(vals,1e-10),color=[colors[0],colors[1],colors[2],colors[0],colors[0]]);ax.set_xscale('log');ax.set_yticks(range(5),labels);ax.invert_yaxis();ax.set_xlabel('最大绝对差（0显示在1e-10）'if zh else'Max absolute difference (zero drawn at 1e-10)')
    for i,v in enumerate(vals):ax.text(max(v,1e-10)*1.25,i,f'{v:.2g}',va='center',fontsize=9)
    ax.set_xlim(7e-11,max(vals)*20)
    ax=fig.add_subplot(gs[1,1]);v=np.array([1e-8,1e-5,.1,1.001,1000.1],dtype=np.float32);bf=torch.tensor(v).bfloat16().float().numpy();fp=torch.tensor(v).half().float().numpy();table=[[f'{n:g}',f'{p:.7g}',f'{b:.7g}']for n,p,b in zip(v,fp,bf)];ax.axis('off');t=ax.table(cellText=table,colLabels=['FP32','FP16','BF16'],loc='center',cellLoc='center');t.auto_set_font_size(False);t.set_fontsize(11);t.scale(1,1.7);ax.set_title('真实类型转换：范围与精度是两件事'if zh else'Actual conversions: range and precision differ')
    save(fig,'memory')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5),layout='constrained')
    names=['不中断','完整恢复','只恢复权重']if zh else['Uninterrupted','Full recovery','Weights only']
    for i,c in enumerate(curves):axes[0].plot(np.arange(1,13),c,label=names[i],color=colors[i],lw=2,ls=['-','--',':'][i],marker='o',ms=3)
    axes[0].axvline(6.5,color='gray',ls=':');axes[0].set_xlabel('参数更新次数'if zh else'Optimizer updates');axes[0].set_ylabel('抽样批次交叉熵'if zh else'Sampled-batch cross-entropy');axes[0].legend(frameon=False);axes[0].set_xticks([1,3,6,9,12])
    for i,(name,v)in enumerate(data_timing.items()):axes[1].scatter(np.full(len(v),i)+np.linspace(-.08,.08,len(v)),v,color=colors[i],s=18,alpha=.7);axes[1].plot([i-.2,i+.2],[np.median(v)]*2,color='#243749',lw=2)
    axes[1].set_yscale('log');axes[1].set_xticks([0,1,2],['CSV全量解析','NPY全量读取','缓存96行复制']if zh else['Parse all CSV','Read all NPY','Copy 96 cached rows']);axes[1].tick_params(axis='x',labelsize=9);axes[1].set_ylabel('每次操作 / ms（对数轴）'if zh else'Milliseconds per operation (log scale)');axes[1].set_title('预热后的读取与解析成本'if zh else'Warm-cache reading and parsing costs')
    save(fig,'recovery')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.4),layout='constrained')
    n=1e8;devices=4;memory=np.array([[2,2,12],[2,2,12/devices],[2,2/devices,12/devices],[2/devices,2/devices,12/devices]])*n/1e9
    base=np.zeros(4)
    for j,label in enumerate(['参数','梯度','主权重 + Adam 状态']if zh else['Parameters','Gradients','Master weights + Adam state']):axes[0].bar(range(4),memory[:,j],bottom=base,color=colors[j],label=label);base+=memory[:,j]
    axes[0].set_xticks(range(4),['DDP','ZeRO-1','ZeRO-2','ZeRO-3']);axes[0].set_ylabel('每设备持久状态 / GB'if zh else'Persistent state per device / GB');axes[0].legend(frameon=False,fontsize=9);axes[0].set_title('解析预算：1亿参数、4设备、混合精度'if zh else'Analytical budget: 100M parameters, four devices')
    stages,micro=3,4
    for stage in range(stages):
        for mb in range(micro):
            axes[1].broken_barh([(stage+mb,1)],(stage-.32,.64),facecolors=colors[mb]);axes[1].text(stage+mb+.5,stage,str(mb+1),ha='center',va='center',color='white')
    axes[1].set_yticks(range(stages),['阶段1','阶段2','阶段3']if zh else['Stage 1','Stage 2','Stage 3']);axes[1].invert_yaxis();axes[1].set_xticks(range(7));axes[1].set_xlim(0,6);axes[1].set_xlabel('理想化前向时间槽（等时阶段）'if zh else'Idealized forward slots (equal stage times)');axes[1].set_title('4个微批，3阶段：利用率4/6'if zh else'Four microbatches, three stages: utilization 4/6')
    save(fig,'parallel')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='en');parser.add_argument('--render-only',action='store_true',help='Render another language from already measured outputs');args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if args.render_only:
        summary=json.loads((out/'summary.json').read_text());stored=np.load(out/'data.npz');pr=json.loads((out/'profile.json').read_text())
        data_timing={k:stored['data_'+k.replace(' ','_')]for k in ['Parse CSV','Read NPY','Cached rows']};step_timing={k:stored['step_'+k.replace(' ','_')]for k in ['FP32','CPU BF16','Recompute']}
        curves=[stored[k]for k in ['loss_full','loss_restored','loss_weights_only']]
        draw(out,args.language,summary,data_timing,step_timing,pr['events'],pr['operators'],curves);return
    x,y=make_data();summary,reference_update,reference_gradient=gradient_experiments(x,y)
    rendezvous=out/('rendezvous-'+uuid.uuid4().hex)
    mp.spawn(ddp_worker,args=(rendezvous.as_uri(),str(out)),nprocs=2,join=True)
    ranks=[torch.load(out/f'ddp-rank{k}.pt',weights_only=True)for k in range(2)]
    summary.update({'ddp_update_error':max_error(reference_update,ranks[0]['parameters']),'ddp_replica_error':max_error(ranks[0]['parameters'],ranks[1]['parameters']),'all_reduce_hand':ranks[0]['reduction'].tolist()})
    if rendezvous.exists():rendezvous.unlink()
    plain,plain_gradient=retained_storage(x,y,False);saved,checkpoint_gradient=retained_storage(x,y,True)
    summary.update({'saved_storage_plain_bytes':plain,'saved_storage_checkpoint_bytes':saved,'checkpoint_gradient_error':max_error(plain_gradient,checkpoint_gradient)})
    recovery_summary,*curves=recovery(x,y,out);summary.update(recovery_summary)
    data_timing,step_timing=timings(x,y,out);events,operators=profile(x,y,out)
    summary.update({'parameter_count':sum(p.numel()for p in new_model().parameters()),'timing_median_ms':{k:float(np.median(v))for k,v in step_timing.items()},'data_median_ms':{k:float(np.median(v))for k,v in data_timing.items()},'fp16_tiny':float(torch.tensor(1e-8).half()),'scaled_fp16_recovered':float((torch.tensor(1e-8)*65536).half().float()/65536),'bf16_tiny':float(torch.tensor(1e-8).bfloat16()),'memory_budget_gb':[1.6,.7,.55,.4],'pipeline_forward_utilization':4/6,'effective_batch_hand':4*8*3,
        'environment':{'device':'CPU','threads_per_process':2,'ddp_processes':2,'backend':'gloo','torch':str(torch.__version__),'numpy':np.__version__,'python':platform.python_version(),'os':platform.system()}})
    np.savez(out/'data.npz',features=x.numpy(),labels=y.numpy(),loss_full=curves[0],loss_restored=curves[1],loss_weights_only=curves[2],**{'step_'+k.replace(' ','_'):v for k,v in step_timing.items()},**{'data_'+k.replace(' ','_'):v for k,v in data_timing.items()})
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    draw(out,args.language,summary,data_timing,step_timing,events,operators,curves)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

运行首先完成真实测量，随后保存summary.json、原始时间样本、分析器范围、模型权重和训练检查点。另一语言的图使用--render-only读取这同一份结果，保持时间线与数值一致。profile.json包含阶段时间与算子自身时间，trace.json按常见时间线格式保存三个训练步的范围，便于逐段查看。存储预算和理想流水线图则从公开的假设直接计算，与实际CPU测量分别标注。

扩展到更大的模型时，可以沿用这套检查顺序：先确认单设备梯度与数据分母，再检查累积和同步后的更新，接着测量时间与峰值内存，最后选择需要的分片和并行。保存与恢复也应随最小实验一起建立。这样，一项优化带来的变化能够被准确归为更少的等待、更少的持久状态、更多的重计算，或不同的数值误差，而训练所要学习的目标始终清楚。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M26.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning: Training on Multiple GPUs](https://d2l.ai/chapter_computational-performance/multiple-gpus.html)

   §13.5.1—13.5.4及图13.5.3：划分方式、批次拆分、梯度聚合。

   D2L original figure CC BY-SA4.0; full notice included.
2. [PyTorch Distributed design note](https://docs.pytorch.org/docs/2.15/notes/ddp.html)

   Internal Design：初始广播、梯度桶、异步all-reduce、优化器一致性。
3. [PyTorch Distributed: Experiences on Accelerating Data Parallel Training](https://arxiv.org/abs/2006.15704)

   2020年原论文摘要：分桶、计算通信重叠与同步跳过。
4. [PyTorch Automatic Mixed Precision](https://docs.pytorch.org/docs/2.15/amp.html)

   CPU训练、BF16、autocast范围及操作类型列表。
5. [PyTorch activation checkpointing](https://docs.pytorch.org/docs/2.15/checkpoint.html)

   非重入checkpoint、保存随机数状态与重计算行为。
6. [PyTorch data loading](https://docs.pytorch.org/docs/2.15/data.html)

   Dataset/DataLoader、批处理、工作进程和分布式采样接口。
7. [Getting Started with FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

   参数all-gather、梯度reduce-scatter、分片优化器与预取段。
8. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054)

   摘要与方法的冗余状态分片思想，图中按明确字节假设独立计算。
9. [PyTorch Tensor Parallel tutorial](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html)

   ColwiseParallel/RowwiseParallel、通信布局与FSDP组合。
10. [PyTorch Pipeline Parallel tutorial](https://docs.pytorch.org/tutorials/intermediate/pipelining_tutorial.html)

    阶段划分、微批、GPipe与1F1B调度。
11. [Switch Transformers](https://arxiv.org/abs/2101.03961)

    2021原论文摘要：稀疏专家路由、通信与负载。
12. [JAX: grad and vmap](https://docs.jax.dev/en/latest/101/transformations.html)

    grad、value_and_grad、vmap与jit组合、首次编译。
13. [JAX: Distributed arrays and automatic parallelization](https://docs.jax.dev/en/latest/201/sharding.html)

    Mesh、NamedSharding、PartitionSpec和复制/分片/未归约数组。
14. [Keras: Customizing fit with TensorFlow](https://keras.io/guides/custom_train_step_in_tensorflow/)

    train_step、GradientTape、训练模式和优化器更新。
15. [TensorFlow: Distributed training](https://www.tensorflow.org/guide/distributed_training)

    MirroredStrategy及同步/异步数据并行。
16. [D2L full figure license](https://github.com/d2l-ai/d2l-en/blob/master/LICENSE)

    原图署名与CC BY-SA 4.0许可。

    CC BY-SA4.0
