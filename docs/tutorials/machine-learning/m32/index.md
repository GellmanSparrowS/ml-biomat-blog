# 按内容读取，按输入记忆：Transformer与Mamba

Source: https://ml-biomat.com/tutorials/machine-learning/m32/
Language: zh-CN

从查询、键和值的手算，走到真实注意力、选择性状态与长序列计算。

## 需要答案时，怎样找到相关的那条信息

桌上放着四张卡片，每张写有一个名字和一个数字。现在有人问“林对应的数字是多少”，你会先找名字，再读旁边的数字，而不是把四个数字求平均。长句理解、图像块之间的关系和历史记录查询，都包含类似的按内容读取问题。循环网络把过去压进不断更新的状态；注意力则允许当前位置对其他位置分配不同权重，直接读取与当前问题相关的内容。

本章沿着“读什么、怎么保存、计算花在哪里”展开。先用只有两个键的算例把查询、键和值算清楚，再把多头、位置、遮罩、残差和归一化组装成Transformer。随后转向状态空间模型，理解连续变化怎样变成递推，以及Mamba为什么让状态更新依赖当前输入。两条路线都有真实小实验：Transformer学习按键查值，选择性状态模型学习只记住带标记的输入，遇到干扰时保留已有记录。

这些实验把任务规则写得很明确，因此既能检查输出是否正确，也能查看注意力分配、步长和内部状态。它们使用不同任务，分别展示两种机制的计算过程。模型选择还需要考虑上下文长度、是否逐项生成、输入是否完整可见，以及所用实现如何管理内存。把这些条件与结构一起理解，比根据一个架构名称推断速度或能力更接近实际使用。

## 查询、键和值分别做什么

查询描述当前位置想找什么，键描述每条候选记录具有什么特征，值则是找到记录后准备读取的内容。查通讯录时，姓名可以帮助匹配，电话号码则是最终要拿走的信息；两者承担不同角色。在神经网络中，这些角色通常由不同的线性变换产生。同一输入向量可以分别投影成查询、键和值，让训练决定哪些特征适合匹配，哪些特征适合传递。

$$
Q=X_qW_Q,\qquad K=X_kW_K,\qquad V=X_kW_V
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0a9d9b45cd9e8a8dd4fd42b2.svg) | 查询侧与记录侧输入，行是位置、列是特征；数值已编码或缩放，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f6c42b12b9575cb1af3a039.svg) | 查询位置数、记录位置数、输入特征宽度，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d51101c07d06ef9d1ddeb5cb.svg) | 学习得到的查询、键和值投影；d_k为匹配维数，d_v为传递内容的维数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/977b500e71ce6d69074802af.svg) | 投影后的查询、键和值矩阵。 |

每行输入乘相应权重得到一种角色表示。若输入为(1,2)，查询投影取单位矩阵，查询仍为(1,2)；值投影取对角元素(2,0.5)，值成为(2,1)。自注意力中两侧输入相同，交叉注意力中来自不同序列。为突出角色，式中省略可选偏置；库的投影可以带偏置。

查询与键的点积越大，表示它们在当前特征坐标中越相合。点积会随特征维数及数值尺度变化，因此缩放点积注意力将它除以键维数的平方根，再用softmax转成非负、总和为1的读取权重。最后用这些权重对值向量求和。整个过程包含相似度计算、归一化和信息汇聚三个步骤，每一步都能够在一组很小的数字上重现。

$$
S=\frac{QK^\top}{\sqrt{d_k}}+M,\qquad \alpha_{ij}=\frac{e^{S_{ij}}}{\sum_{r=1}^{T_k}e^{S_{ir}}},\qquad O=\alpha V
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4121a43dfe038f5f051b9b6c.svg) | 匹配分数与加性遮罩；允许位置M为0，禁用位置为负无穷。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77898ba461afcb97a3e7f28.svg) | 键矩阵转置与键宽度；转置使每个查询能与每个键做点积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b80fa4f43252caaf216e9633.svg) | 查询行索引、一个键索引、归一化求和用的键索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86745df553e3e78b7038595d.svg) | 非负读取权重，每个有效查询行相加为1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/91b7cd3dd14a1a81bca61eb0.svg) | 读取后的输出与值矩阵，输出保留值的特征维度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/abaa4fa6da9379e7ead98f05.svg) | 自然指数底及维数平方根缩放；所有分数在本例无量纲。 |

若查询与键的各坐标近似独立、方差约为1，点积的方差随d_k增大，除以平方根有助于控制分数尺度。两键算例的分数(1/√2,0)给出权重(0.66976155,0.33023845)，乘值(2,0)、(0,4)后为(1.33952310,1.32095380)。实际计算常先减去每行最大分数再取指数，归一化结果不变而数值更稳定。

![解析两键算例：从缩放分数到softmax权重，再到二维值向量的加权和。绿色箭头是输出，蓝橙箭头是两个值；全部为明确输入的计算结果。](https://ml-biomat.com/static/tutorials/machine-learning/figures/43b9122729f7fee1de42c1a7.svg?v=43b9122729f7)

图 1解析两键算例：从缩放分数到softmax权重，再到二维值向量的加权和。绿色箭头是输出，蓝橙箭头是两个值；全部为明确输入的计算结果。

取查询(1,0)，两个键分别为(1,0)与(0,1)，键维数为2。缩放后的分数约为0.7071与0，softmax给出约0.66976和0.33024。若两个值为(2,0)与(0,4)，输出便是两者的加权和，约为(1.33952,1.32095)。它既没有简单选出某一个值，也没有直接输出相似度，而是把匹配程度转换为对内容的读取比例。

自注意力让查询、键和值都来自同一序列，便于序列内部交流；交叉注意力则让查询来自一侧，键和值来自另一侧。例如翻译时，目标序列当前位置可以提出查询，读取源句编码器提供的表示。查询数与键数可以不同，得到的注意力矩阵也就不一定是正方形。先明确信息来自哪一侧，再看矩阵形状，就不容易把这些结构混在一起。

## 多个读取视角，还要知道哪些位置可以看

一个读取分配可能无法同时表达多种关系。多头注意力用不同投影形成多个特征子空间，各自完成匹配与汇聚，再把结果拼接并映射回模型宽度。可以把它理解成同一份资料上的几种阅读方式：有的关注局部相邻关系，有的关注某个内容特征。不过，每个头承担什么功能是学习结果，不能在训练前直接给它们贴上语法或语义标签。

$$
\operatorname{MHA}(X)=\operatorname{Concat}(O^{(1)},\ldots,O^{(H)})W_O
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9d6bf175b0b3d7c88137cd57.svg) | 注意力头数、一个头的编号，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/42d7a82f5a83ad83892f4fab.svg) | 第h个头按上一式得到的读取结果；上标为头编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be6eccd644d3a07b523f251f.svg) | 沿特征维拼接，得到T×(H d_v)矩阵。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff255aafe46114917e14e8ee.svg) | 输出投影，恢复模型宽度d。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d9aafadb2337f86876fc8070.svg) | 输入表示、序列长度、模型宽度、多头注意力运算，数值无量纲。 |

本章四头、模型宽度32，每头的键和值宽度为8，四个8维结果拼成32维，再经过32×32输出投影。头之间采用不同的可学习投影，因此读取权重可以不同；拼接保留各头结果的分量，随后由输出投影组合。

遮罩控制哪些连接在当前任务中可用。自回归生成第一个词时，还没有后面的词，因果遮罩便禁止当前位置读取未来；填充遮罩则排除为了凑齐批长度而加入的位置。通常在softmax之前把禁用位置的分数设成负无穷，使其归一化权重为零。若把一整行都遮掉，归一化就失去有效候选，因此数据与遮罩必须共同保证每个需要输出的位置至少有一个可读对象。

不同接口对布尔遮罩的含义可能不同。本章使用的`nn.MultiheadAttention`把True视为禁止读取。程序构造一段六位置输入，改变后三个位置的内容，再检查前三个位置的输出：在因果遮罩下，最大变化为零。这个干预直接检验信息是否按预期受限，而不是只看一张画成三角形的遮罩图。训练下一词预测时，还需要正确移位输入和目标，遮罩与标签对齐共同定义了预测问题。

注意力仅根据输入向量之间的关系计算，不会自动知道谁在前、谁在后。位置表示把顺序加入模型：可以给各位置一个可学习向量，也可以用确定的正弦、余弦函数表达不同尺度的位置变化。旋转位置编码则把成对特征按位置旋转，让查询与键的点积携带相对位置关系。本章小模型直接把五个可学习位置向量加到输入投影上，便于看到位置如何进入实际计算。

## 把读取、局部变换和直接路径组装起来

Transformer层不仅包含注意力。注意力在不同位置之间交换信息，逐位置前馈网络则对每个位置的特征做非线性变换，同一组前馈参数在各位置共享。残差连接把输入直接加回变换结果，LayerNorm控制每个位置内部的特征尺度。两类子层各自负责不同工作：先向其他位置取信息，再在当前位置加工表示，随后重复这个过程。

$$
U=X+\operatorname{MHA}(\operatorname{LN}_1(X)),\qquad Y=U+\operatorname{FFN}(\operatorname{LN}_2(U))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38f8e1d574419bbd047a3717.svg) | 层输入、中间表示、层输出，形状一致；批维在外层额外保留。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff86c7f353952f4d5c710806.svg) | 分别沿每个位置的特征维做LayerNorm，具有各自学习参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/917a676254468d25a9d8aefc.svg) | 跨位置进行多头信息读取。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7c72d18fd01e238477b7cb66.svg) | 逐位置共享的前馈网络；本例32→64→32，使用GELU激活。 |

两次相加都要求特征宽度相同。若某位置输入为(0.2,0.4)，第一子层输出为(0.1,−0.2)，则U=(0.3,0.2)；第二子层再输出(0.02,0.03)，得到Y=(0.32,0.23)。本式采用预归一化，原始参考结构图采用相加后归一化，两者应按各自顺序阅读。

![编码器—解码器Transformer原始组织：追踪输入与输出两条路径，注意解码器中的因果自注意力及跨侧读取。图：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola，Dive into Deep Learning，Fig.11.7.1，CC BY-SA 4.0，原图未改动。该图采用后归一化，本章代码采用预归一化。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2cfd9aab4c73a8836b3ab263.svg?v=2cfd9aab4c73)

图 2编码器—解码器Transformer原始组织：追踪输入与输出两条路径，注意解码器中的因果自注意力及跨侧读取。图：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola，Dive into Deep Learning，Fig.11.7.1，CC BY-SA 4.0，原图未改动。该图采用后归一化，本章代码采用预归一化。

图中的原始编码器—解码器结构来自2017年Transformer路线。编码器能够在完整源序列内部读取，适合形成输入表示；解码器的自注意力使用因果遮罩，再通过交叉注意力读取编码器输出。只保留编码器的模型适合整段理解或分类，只保留因果解码器的模型适合逐项生成。名称描述的是信息流与子层组织，而不是一个架构只能完成一种应用。

归一化位置也有不同约定。原图在残差相加后归一化，本章代码采用先归一化再进入子层的形式，并在最后再做一次归一化。阅读实现时应沿着运算顺序检查，而不是把“Add & Norm”当成位置无关的固定标签。两层小Transformer中，每层含四个注意力头，模型宽度32，前馈中间宽度64；注意力和前馈子层的输出都回到32维，才能与残差输入相加。

词元也并不专指自然语言的词。文本可以先按子词编码，再查嵌入表；图像可以分块、展平并线性投影；连续传感器记录可以把一个时间点的多个特征映射到同一模型宽度。它们共同提供一串向量，但采样间隔、位置含义和可见范围不同。本章每张键值卡直接编码成九维向量：四个键位置、四个值位置和一个查询标记，五张卡构成一条短序列。

## 另一条路线：维护一份会随输入变化的状态

如果每到一个新时刻，都重新查看全部历史，序列越长，读取的对象就越多。状态空间模型采用另一种组织方式：用一组状态概括过去，新输入到来后更新状态，再从状态读出结果。这种思路长期用于描述动态系统，例如一个容器的温度既受到当前加热影响，也保留过去积累的热量。模型把“内部怎样演化”与“外部看到什么”分开，让状态成为连接过去与当前的中介。

$$
\frac{dh(\tau)}{d\tau}=Ah(\tau)+Bx(\tau),\qquad y(\tau)=Ch(\tau)+Dx(\tau)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3c5718e2fe3ba865d1d37f34.svg) | 连续时间和N维内部状态；时间按模型指定单位计，状态在本章无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0a00dcb6659783089cd167c8.svg) | 此简化系统的标量输入与输出，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bb28ee8729a7fb3a1da437ba.svg) | 状态演化与输入作用系数，时间量纲为每单位时间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c37fb19f512eb0eb645bd7a8.svg) | 从状态读取输出的系数、直接输入项系数，本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dc6e3fa635830d5dca115967.svg) | 状态相对连续时间的变化率。 |

输入通过B改变内部状态，A决定状态自身怎样演化，再由C读取，D允许输入直接影响输出。标量例A=−1、B=1、C=1、D=0时，当前状态0.8、输入−0.5给出瞬时变化率−1.3每单位时间。变化率不是下一状态；还需要对选定时间间隔积分。

连续方程需要离散成计算机上的逐步更新。以状态按自身值衰减、同时受到输入推动的标量系统为例，如果一个时间间隔内输入保持不变，可以精确求出该步旧状态的保留系数和新输入的贡献。衰减率取−1、输入系数取1、间隔取ln2时，旧状态恰好保留一半，输入也贡献一半。旧状态0.8、当前输入−0.5，就得到新状态0.15。这个算例把连续变化、采样间隔与递推系数连在了一起。

$$
h_t=e^{a\Delta}h_{t-1}+\frac{e^{a\Delta}-1}{a}\,b x_t\quad(a\ne0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6d3079853305e3d7d1266f42.svg) | 离散间隔末端与起点的标量状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | 上一式标量情况下的状态率、输入系数，均为每单位时间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/101bc29506fa7eee5de512cf.svg) | 间隔长度及离散时间编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f8abeca1e21f2ff4458a26ea.svg) | 在该间隔内保持常值的标量输入，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a6477ba1148f635d5b79627.svg) | 旧状态的保留倍率和积分后的输入贡献系数，均无量纲。 |

常值输入下求解线性微分方程得到这一精确离散式。a=−1、b=1、Δ=ln2时，两项系数均为0.5，故0.8与−0.5得到0.15。若a趋近0，输入系数趋近bΔ；可以使用该极限处理零衰减率。

当状态更新矩阵和输入、读出规则不随时间改变时，模型具有线性时不变结构。把递推展开，能够看见过去各次输入以不同衰减权重叠加到当前输出，也可以转写成一类序列卷积。对于固定规则的动态响应，这种结构很自然；如果某些词需要记住、某些干扰需要跳过，更新规则就需要能够根据内容做选择。这个问题把状态空间模型与本章开头的“查到相关信息”联系起来。

状态维数决定了内部可用的记录空间，衰减率决定不同分量保留信息的时间尺度。许多神经状态空间设计使用具有结构的矩阵，使较大的状态仍能高效计算。对角形式让各状态坐标按不同速率衰减，输入投影和输出投影再把它们组合起来。它与一个标量移动平均有共同的递推思想，但多尺度状态与可学习投影提供了更丰富的表示方式。

## 选择性状态：当前内容决定怎样更新

Gu与Dao在2023年提出的Mamba，让部分状态空间参数成为当前输入的函数。直观地说，同一条状态通路不必对所有输入采用相同的保存和写入策略：遇到重要标记时可以更新，遇到干扰时可以更多保留旧内容。选择性来自输入影响离散步长、输入写入与状态读出；当这些量随内容变化，整体模型也就不再是固定核的线性卷积。

$$
\begin{aligned}\Delta_t&=\operatorname{softplus}(W_\Delta u_t+b_\Delta),\quad B_t=W_Bu_t,\quad C_t=W_Cu_t\\h_{t,d,n}&=e^{\Delta_{t,d}A_{d,n}}h_{t-1,d,n}+\Delta_{t,d}B_{t,n}u_{t,d}\\r_{t,d}&=\sum_{n=1}^{N}C_{t,n}h_{t,d,n}+D_du_{t,d}\\\widehat y_t&=w^\top\bigl(r_t\odot\operatorname{SiLU}(z_t)\bigr)+b\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a5625d1805920ff4c88bdfe6.svg) | 内部输入与输出门控分支，均由当前及因果局部输入计算；D_c=24。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81b6682fe1ae279c3c2db014.svg) | 按通道计算的正步长；softplus为log(1+exp(v))，实际使用稳定实现。 |
| ![Formula](https://ml-biomat.com/static/agent-math/097f23240656e0a867b67f4a.svg) | 输入到步长的学习投影和偏置。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9f0713f1222e82c96ccfea98.svg) | 输入相关的写入与读出投影；N=4，每个时刻在内部通道间共享这些N维系数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/39ac8b0cf04d2c77169a6e71.svg) | 负衰减率及内部状态；代码将每个率参数化为负指数，初始状态为零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/76a6dc77e0a5431e539a549a.svg) | 时间、内部通道、状态坐标索引；D_d为直接输入系数，r_t为读出后的通道向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a62ffa9a018e73196692c19b.svg) | 最终线性读出权重、偏置、标量预测与逐元素乘法。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2650f19e6d80d3aec856bd07.svg) | 平滑门控激活，σ为sigmoid；本例输入、状态与模型时间均使用归一化数值。 |

给定一个坐标A=−1、Δ=0.2、旧h=0.8、B=0.5、u=−1，新状态为exp(−0.2)×0.8−0.1≈0.554985。状态项采用指数转移，输入项采用ΔBu；它不同于前一式的精确积分输入系数。B、C与Δ随输入变化，赋予模型按内容更新的能力。每次扫描的状态形状为批大小×24×4。

本章的CPU示例保留这一核心计算。输入先分成两路，一路经过短的因果逐通道卷积与SiLU，另一条用作输出门控；再从当前表示计算正步长、写入系数和读出系数。每个内部通道有四个状态坐标，负的衰减率保证在正步长下旧状态乘数处于零到一之间。程序采用与参考选择性扫描形式一致的指数状态转移和步长乘输入写入项，完整循环逐时刻列在代码中，便于查看每次状态变化。

这里要区分连续系统的精确离散化与实现中使用的写入近似。前一节的标量例子把常值输入在整个间隔内的作用精确积分；本章选择性扫描则使用步长乘写入系数的形式。两者保留了相同的“旧状态传递加新内容”结构，但输入项的数值规则不同。将公式与实现逐项对应后，才能解释改变步长为什么会同时改变遗忘和写入。

Mamba还重视扫描过程怎样在硬件上执行。给定每一步的系数，连续两次仿射状态更新可以合成为一次，而这种组合满足结合律，因此能够组织成并行扫描。正式实现会进一步安排显存读写和融合运算。本章使用显式CPU循环展示数值机制，训练时保留反向传播所需状态；推断新观测时，则可以继续更新已有状态，而无需保存整张历史注意力矩阵。

## 两个实际实验：按内容读取与按标记保存

第一个任务每条序列含四张键值卡和最后一张查询卡。四个键各出现一次，值从四个类别中随机生成，查询指定其中一个键，模型预测它对应的值。训练、验证、测试分别独立生成1000、300、400条序列。两层Transformer实际训练50轮，按验证交叉熵选择参数；不读取查询、只回答四张卡中最常见值的规则作为参照。

第二个任务每条序列含16个数值与标记，数值在−1到1均匀采样，首项始终有标记，后续标记独立以0.2概率出现。每一步的目标都是最近一次带标记的数值。训练、验证、测试分别为800、240、320条序列，选择性模型训练70轮，以逐步均方误差学习何时写入、何时保持。两个实验的目标不同，图中分别使用各自损失，并保留清楚的样本数与生成种子。

### 完整Python：内容检索与选择性状态扫描

依赖NumPy、Matplotlib、PyTorch。运行python main.py --output results --language zh，训练两种小模型并产生五组SVG、模型参数、summary.json和原始轨迹。CPU双线程；无大模型下载。选择性核心逐步实现因果卷积、输入相关步长/写入/读出与输出门控。

```
"""Attention retrieval and a CPU selective state-space teaching model.

The selective recurrence follows the mathematical form documented by Gu & Dao
and the state-spaces/mamba reference implementation. This compact implementation
uses ordinary PyTorch operations so each state is inspectable on CPU.
"""
from pathlib import Path
import argparse,copy,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn

def retrieval_data(n,seed):
    rng=np.random.default_rng(seed);x=np.zeros((n,5,9),dtype=np.float32);target=np.zeros(n,dtype=np.int64);slots=[]
    for b in range(n):
        keys=rng.permutation(4);values=rng.integers(0,4,4);chosen=int(rng.integers(4))
        for t,(key,value) in enumerate(zip(keys,values)):x[b,t,key]=1;x[b,t,4+value]=1
        x[b,4,keys[chosen]]=1;x[b,4,8]=1;target[b]=values[chosen];slots.append(chosen)
    return torch.tensor(x),torch.tensor(target),np.array(slots)

class AttentionBlock(nn.Module):
    def __init__(self):
        super().__init__();self.norm1=nn.LayerNorm(32);self.attention=nn.MultiheadAttention(32,4,batch_first=True,dropout=0)
        self.norm2=nn.LayerNorm(32);self.ff=nn.Sequential(nn.Linear(32,64),nn.GELU(),nn.Linear(64,32))
    def forward(self,x,mask=None,weights=False):
        z=self.norm1(x);a,w=self.attention(z,z,z,attn_mask=mask,need_weights=weights,average_attn_weights=False)
        x=x+a;return x+self.ff(self.norm2(x)),w

class TinyTransformer(nn.Module):
    def __init__(self):
        super().__init__();self.embed=nn.Linear(9,32);self.position=nn.Parameter(torch.randn(1,5,32)*.02)
        self.blocks=nn.ModuleList([AttentionBlock(),AttentionBlock()]);self.norm=nn.LayerNorm(32);self.head=nn.Linear(32,4)
    def forward(self,x,weights=False):
        x=self.embed(x)+self.position;all_weights=[]
        for block in self.blocks:x,w=block(x,weights=weights);all_weights.append(w)
        logits=self.head(self.norm(x[:,-1]));return (logits,all_weights) if weights else logits

def memory_data(n,seed,length=16):
    rng=np.random.default_rng(seed);values=rng.uniform(-1,1,(n,length));marks=rng.random((n,length))<.2;marks[:,0]=True
    targets=np.zeros_like(values);last=np.zeros(n)
    for t in range(length):last=np.where(marks[:,t],values[:,t],last);targets[:,t]=last
    x=np.stack([values,marks],-1).astype('float32');return torch.tensor(x),torch.tensor(targets,dtype=torch.float32)

class SelectiveMemory(nn.Module):
    def __init__(self,width=24,state_size=4):
        super().__init__();self.width=width;self.state_size=state_size
        self.input=nn.Linear(2,2*width);self.local=nn.Conv1d(width,width,3,padding=2,groups=width)
        self.delta=nn.Linear(width,width);nn.init.constant_(self.delta.bias,-2)
        self.B=nn.Linear(width,state_size,bias=False);self.C=nn.Linear(width,state_size,bias=False)
        self.log_rates=nn.Parameter(torch.log(torch.arange(1,state_size+1,dtype=torch.float32)).repeat(width,1))
        self.direct=nn.Parameter(torch.ones(width));self.readout=nn.Linear(width,1)
    def forward(self,x,trace=False):
        u,z=self.input(x).chunk(2,-1);length=x.shape[1]
        u=nn.functional.silu(self.local(u.transpose(1,2))[...,:length].transpose(1,2))
        dt=nn.functional.softplus(self.delta(u));B=self.B(u);C=self.C(u);A=-torch.exp(self.log_rates)
        h=x.new_zeros(x.shape[0],self.width,self.state_size);outputs=[];states=[]
        for t in range(length):
            decay=torch.exp(dt[:,t,:,None]*A[None])
            write=dt[:,t,:,None]*B[:,t,None,:]*u[:,t,:,None]
            h=decay*h+write
            y=(h*C[:,t,None,:]).sum(-1)+self.direct*u[:,t]
            outputs.append(self.readout(y*nn.functional.silu(z[:,t])).squeeze(-1))
            if trace:states.append(h)
        result=torch.stack(outputs,1)
        return (result,dt,torch.stack(states,1)) if trace else result

def fit(model,train_x,train_y,val_x,val_y,classification,epochs,seed):
    optimizer=torch.optim.Adam(model.parameters(),lr=.003);generator=torch.Generator().manual_seed(seed)
    criterion=nn.CrossEntropyLoss() if classification else nn.MSELoss();history=[];best=float('inf');saved=None;best_epoch=0
    for epoch in range(1,epochs+1):
        model.train()
        for ix in torch.randperm(len(train_x),generator=generator).split(64):
            optimizer.zero_grad(set_to_none=True);loss=criterion(model(train_x[ix]),train_y[ix]);loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(),1.0);optimizer.step()
        model.eval()
        with torch.no_grad():tl=float(criterion(model(train_x),train_y));vl=float(criterion(model(val_x),val_y))
        history.append([epoch,tl,vl])
        if vl<best:best=vl;best_epoch=epoch;saved=copy.deepcopy(model.state_dict())
    model.load_state_dict(saved);model.eval();return np.array(history),best_epoch

def run(output,language):
    output.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    tx,ty,_=retrieval_data(1000,320);vx,vy,_=retrieval_data(300,321);ex,ey,slots=retrieval_data(400,322)
    torch.manual_seed(323);transformer=TinyTransformer();attention_history,attention_best=fit(transformer,tx,ty,vx,vy,True,50,324)
    with torch.no_grad():logits,weights=transformer(ex,weights=True);accuracy=float((logits.argmax(-1)==ey).float().mean())
    query_blind=ex[:,:4,4:8].sum(1).argmax(-1);baseline=float((query_blind==ey).float().mean())
    mx,my=memory_data(800,325);mv,mvy=memory_data(240,326);me,mey=memory_data(320,327)
    torch.manual_seed(328);selective=SelectiveMemory();memory_history,memory_best=fit(selective,mx,my,mv,mvy,False,70,329)
    with torch.no_grad():memory_pred,dt,states=selective(me,trace=True)
    memory_mse=float(nn.functional.mse_loss(memory_pred,mey));last_mse=float(nn.functional.mse_loss(memory_pred[:,-1],mey[:,-1]))
    torch.save(transformer.state_dict(),output/'transformer.pt');torch.save(selective.state_dict(),output/'selective-memory.pt')
    # Exact QKV example; compare direct calculation with the library operation.
    q=torch.tensor([[1.,0.]],dtype=torch.float64);k=torch.eye(2,dtype=torch.float64);v=torch.tensor([[2.,0.],[0.,4.]],dtype=torch.float64)
    scores=q@k.T/math.sqrt(2);alpha=torch.softmax(scores,dim=-1);manual=alpha@v
    official=nn.functional.scaled_dot_product_attention(q[None,None],k[None,None],v[None,None])[0,0]
    qkv_error=float((manual-official).abs().max());assert qkv_error<1e-12
    # Changing future tokens cannot change earlier outputs under a causal mask.
    torch.manual_seed(330);block=AttentionBlock().eval();sequence=torch.randn(1,6,32);changed=sequence.clone();changed[:,3:]+=10*torch.randn(1,3,32)
    mask=torch.triu(torch.ones(6,6,dtype=torch.bool),diagonal=1)
    with torch.no_grad():a,_=block(sequence,mask);b,_=block(changed,mask);causal_error=float((a[:,:3]-b[:,:3]).abs().max())
    assert causal_error<1e-6
    # A diagonal scan independently evaluated in two equivalent arrangements.
    A=np.array([-.5,-1.]);deltas=np.array([.1,.2,.05]);inputs=np.array([1.,-2.,.3]);B=np.array([.6,-.4]);h=np.zeros(2);trace=[]
    for delta,value in zip(deltas,inputs):h=np.exp(delta*A)*h+delta*B*value;trace.append(h.copy())
    # Expanded closed form: each earlier write is multiplied by later decays.
    expanded=sum(deltas[t]*B*inputs[t]*np.exp(A*deltas[t+1:].sum()) for t in range(3))
    scan_error=float(np.abs(h-expanded).max());assert scan_error<1e-12

    fig=plt.figure(figsize=(12,4.3),layout='constrained');gs=fig.add_gridspec(1,3,width_ratios=[1,1,1.3])
    ax=fig.add_subplot(gs[0,0]);ax.bar([0,1],scores.numpy().ravel(),color=['#0072B2','#D58500']);ax.set(xticks=[0,1],xticklabels=['K1','K2'],ylabel=tr('缩放点积分数','Scaled dot-product score'))
    ax=fig.add_subplot(gs[0,1]);ax.bar([0,1],alpha.numpy().ravel(),color=['#0072B2','#D58500']);ax.set(xticks=[0,1],xticklabels=['K1','K2'],ylim=(0,1),ylabel=tr('归一化读取权重','Normalized reading weight'))
    ax=fig.add_subplot(gs[0,2]);ax.arrow(0,0,2,0,color='#0072B2',width=.025,length_includes_head=True);ax.arrow(0,0,0,4,color='#D58500',width=.025,length_includes_head=True);ax.arrow(0,0,float(manual[0,0]),float(manual[0,1]),color='#008675',width=.035,length_includes_head=True)
    ax.text(2,.2,'V1');ax.text(.1,3.8,'V2');ax.text(float(manual[0,0]),float(manual[0,1])+.15,tr('加权输出','Weighted output'));ax.set(xlim=(-.2,2.8),ylim=(-.2,4.3),xlabel=tr('特征维1','Feature dimension1'),ylabel=tr('特征维2','Feature dimension2'))
    fig.savefig(output/f'qkv-{language}.svg');plt.close(fig)
    # Actual second-layer head maps for the first held-out retrieval example.
    retrieval_sample=next(i for i in range(len(ex)) if len(set(ex[i,:4,4:8].argmax(1).tolist()))==4)
    head_maps=weights[-1][retrieval_sample].numpy();key_ids=ex[retrieval_sample,:4,:4].argmax(1).numpy();value_ids=ex[retrieval_sample,:4,4:8].argmax(1).numpy();query=int(ex[retrieval_sample,4,:4].argmax())
    labels=[f'K{k}:V{v}' for k,v in zip(key_ids,value_ids)]+[f'Q:K{query}']
    fig,axes=plt.subplots(1,4,figsize=(13,3.8),layout='constrained')
    for j,ax in enumerate(axes):
        im=ax.imshow(head_maps[j],vmin=0,vmax=1,cmap='viridis');ax.set(xticks=range(5),xticklabels=labels,yticks=range(5),yticklabels=labels,title=tr(f'头{j}',f'Head{j}'))
        ax.tick_params(axis='x',labelrotation=55);ax.add_patch(plt.Rectangle((-.5,3.5),5,1,fill=False,edgecolor='#D58500',lw=2))
    fig.colorbar(im,ax=list(axes),shrink=.6,label=tr('注意力权重','Attention weight'));fig.savefig(output/f'attention-{language}.svg');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.3),layout='constrained')
    for ax,history,title in [(axes[0],attention_history,tr('键值检索：Transformer','Key-value retrieval: Transformer')),(axes[1],memory_history,tr('最近标记值：选择性状态','Last marked value: selective state'))]:
        ax.semilogy(history[:,0],history[:,1],label=tr('训练','Training'),color='#0072B2');ax.semilogy(history[:,0],history[:,2],label=tr('验证','Validation'),color='#D58500');ax.set(title=title,xlabel=tr('训练轮数','Epoch'),ylabel=tr('交叉熵' if ax is axes[0] else '均方误差','Cross entropy' if ax is axes[0] else 'MSE'));ax.legend()
    fig.savefig(output/f'learning-{language}.svg');plt.close(fig)
    # Inspect a learned memory trajectory, not a manually prescribed gate plot.
    sample=0;time=np.arange(1,17);marked=np.flatnonzero(me[sample,:,1].numpy())
    fig=plt.figure(figsize=(12,6.3),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.6,1])
    ax=fig.add_subplot(gs[0,:]);ax.plot(time,me[sample,:,0],'.-',color='#9aa5ab',label=tr('当前输入值','Current input value'));ax.step(time,mey[sample],where='post',color='#273e47',lw=2,label=tr('最近标记值目标','Last-marked-value target'));ax.plot(time,memory_pred[sample],'o-',color='#0072B2',ms=4,label=tr('模型读出','Model readout'));ax.scatter(time[marked],me[sample,marked,0],s=90,facecolors='none',edgecolors='#D58500',linewidths=2,label=tr('有标记的输入','Marked inputs'));ax.set(xlabel=tr('时间步','Time step'),ylabel=tr('数值（无量纲）','Value (dimensionless)'));ax.legend(ncol=2,fontsize=9)
    ax=fig.add_subplot(gs[1,0]);im=ax.imshow(dt[sample].T,aspect='auto',origin='lower',cmap='magma');ax.set(xlabel=tr('时间索引0–15','Time index0–15'),ylabel=tr('内部通道0–23','Internal channel0–23'));fig.colorbar(im,ax=ax,label=tr('学习得到的步长Δ','Learned step sizeΔ'))
    ax=fig.add_subplot(gs[1,1]);ax.plot(time,states[sample,:,0,:].numpy());ax.set(xlabel=tr('时间步','Time step'),ylabel=tr('通道0的四维状态','Four state coordinates, channel0'));ax.legend([f'n={i}' for i in range(4)],fontsize=8,ncol=2)
    fig.savefig(output/f'memory-{language}.svg');plt.close(fig)
    lengths=np.array([16,32,64,128,256,512,1024,2048]);attention_entries=4*lengths**2;kv_entries=2*32*lengths;state_entries=np.full_like(lengths,24*4)
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.3),layout='constrained')
    axes[0].loglog(lengths,attention_entries,'o-',label=tr('4头注意力分数','Four-head attention scores'),color='#0072B2');axes[0].loglog(lengths,24*4*lengths,'o-',label=tr('选择性状态逐步展开','Unrolled selective states'),color='#D58500');axes[0].set(xlabel=tr('序列长度T','Sequence lengthT'),ylabel=tr('指定数组的标量数','Scalars in the specified array'));axes[0].legend(fontsize=9)
    axes[1].loglog(lengths,kv_entries*4/1024,'o-',label=tr('单层KV缓存，d=32','One-layer KV cache,d=32'),color='#0072B2');axes[1].loglog(lengths,state_entries*4/1024,'o-',label=tr('24×4递推状态','24×4 recurrent state'),color='#D58500');axes[1].set(xlabel=tr('已读长度T','Observed lengthT'),ylabel=tr('float32状态存储（KiB）','float32 state storage(KiB)'));axes[1].legend(fontsize=9)
    fig.savefig(output/f'complexity-{language}.svg');plt.close(fig)
    summary={'retrieval':{'train':1000,'validation':300,'test':400,'accuracy':accuracy,'query_blind_majority_accuracy':baseline,'best_epoch':attention_best,'parameter_count':sum(p.numel() for p in transformer.parameters()),'sample_index':retrieval_sample,'sample_query_key':query,'sample_correct_slot':int(slots[retrieval_sample]),'sample_values':value_ids.tolist(),'sample_prediction':int(logits[retrieval_sample].argmax()),'sample_target':int(ey[retrieval_sample])},'memory':{'train':800,'validation':240,'test':320,'length':16,'test_mse_all_steps':memory_mse,'test_mse_last_step':last_mse,'best_epoch':memory_best,'parameter_count':sum(p.numel() for p in selective.parameters())},'hand_attention':{'weights':alpha.numpy().tolist(),'output':manual.numpy().tolist(),'library_max_error':qkv_error},'causal_prefix_max_error':causal_error,'scan_expansion_max_error':scan_error,'scan_final_state':h.tolist(),'torch_version':torch.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez(output/'experiment.npz',attention_history=attention_history,memory_history=memory_history,head_maps=head_maps,memory_input=me.numpy(),memory_target=mey.numpy(),memory_prediction=memory_pred.numpy(),delta=dt.numpy(),states=states.numpy(),retrieval_test=ex.numpy(),retrieval_target=ey.numpy());print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![两个独立任务的实际训练与验证曲线：左为键值检索交叉熵，右为最近标记值的逐步均方误差。纵轴采用对数尺度，样本数与训练预算见正文。](https://ml-biomat.com/static/tutorials/machine-learning/figures/c21b09d764c7d2746ba6e248.svg?v=c21b09d764c7)

图 3两个独立任务的实际训练与验证曲线：左为键值检索交叉熵，右为最近标记值的逐步均方误差。纵轴采用对数尺度，样本数与训练预算见正文。

检索模型在400条测试序列上的准确率为100%，忽略查询的多数值规则为53.5%。模型共有17764个参数。注意力图选择一条四个值互不相同的测试序列，避免多个相同答案掩盖读取位置；图中展示第二层四个头的实际权重，橙框标出最后查询位置的一行。不同头可以采用不同读取分配，最终答案由残差、前馈和分类头共同形成。

![已训练Transformer第二层的四头注意力。选择首条四个值互不相同的测试样本；横轴是被读取记录，纵轴是发出查询的位置，橙框为最后查询行。各头共用0–1色标。](https://ml-biomat.com/static/tutorials/machine-learning/figures/ae84aede960e71b54d93b83c.svg?v=ae84aede960e)

图 4已训练Transformer第二层的四头注意力。选择首条四个值互不相同的测试样本；横轴是被读取记录，纵轴是发出查询的位置，橙框为最后查询行。各头共用0–1色标。

选择性模型共有1177个参数，在测试序列全部时间步上的均方误差约0.000552，最后一步约0.001074。轨迹图把当前输入、最近标记值目标和模型读出放在同一时间轴上。圆圈标记需要写入的观测，灰色干扰仍持续出现，模型输出则跟随目标的分段变化。下方展示实际学习到的步长，以及一个内部通道的四个状态坐标，使输出变化能够与内部更新一起检查。

这条示例的最后一段没有新标记，目标应保持水平，而模型读出在末端出现了可见漂移。这个局部现象与较小的整体均方误差同时存在，说明平均指标还需要配合时间位置来读。可以进一步按“距离最近一次标记经过了多少步”分组，检查误差是否随保存间隔变化；再通过改变干扰数值，区分状态保留与当前读出对误差的影响。实际轨迹因此既是结果展示，也为下一项实验提供了具体问题。

![真实选择性模型的测试样本轨迹：当前值、标记位置、目标与模型输出共用时间轴。下方为24个内部通道的学习步长及通道0的四维状态。标记决定任务要求何时更新，门控参数由模型学习。](https://ml-biomat.com/static/tutorials/machine-learning/figures/330e7edfadc1d4b14b9c5239.svg?v=330e7edfadc1)

图 5真实选择性模型的测试样本轨迹：当前值、标记位置、目标与模型输出共用时间轴。下方为24个内部通道的学习步长及通道0的四维状态。标记决定任务要求何时更新，门控参数由模型学习。

程序还做了三个独立数值核对。两键注意力的手算加权和与库函数一致；改变未来输入后，因果遮罩保护的前三个输出不变；一条两维状态递推与展开后的各次写入加权和相差约2.78×10⁻¹⁷。最后一项直接验证了“早期写入还要乘以后续保留系数”的解释。把小规模计算核对与训练结果并列，可以同时看清实现规则和学习行为。

## 转动查询，观察信息从哪里流入

四个键位于四个方向，值向量分别为(2,0)、(0,4)、(−2,0)、(0,−4)。拖动左图查询箭头或使用滑块，中间读取权重与右侧输出同步变化。开启因果遮罩时，将查询视为位置1，只允许读取位置0和1；后两条记录的权重变为零。

[Figure: 查询方向、四个注意力权重与值向量输出](https://ml-biomat.com/tutorials/machine-learning/m32/#M32-plot)

键顺序K1=(1,0)、K2=(0,1)、K3=(−1,0)、K4=(0,−1)，点积分数除以√2。所有特征无量纲；绿色箭头表示加权输出，灰色条表示被遮罩的记录。

## 长序列的代价，来自保存和计算什么

普通完整自注意力需要考虑位置两两之间的匹配，长度翻倍时，这部分配对数量增加到四倍。生成过程中，KV缓存保存过去位置的键和值，避免每产生一个新词都重新计算它们；新查询仍需要读取已有缓存。状态空间递推则把过去压进固定形状状态，单次更新的核心状态大小不随已读长度增加。两种方式保留历史的形式不同，也因此呈现不同的计算与存储结构。

$$
N_{\mathrm{score}}=H T^2,\qquad N_{\mathrm{KV}}=2Td,\qquad N_{\mathrm{state}}=D_cN
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d35c4e2939f2a170dba0b27.svg) | 序列长度、注意力头数、所有头合计的模型宽度；单层、单样本计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/92daac7d5ea84ad4363336d6.svg) | 显式完整自注意力分数矩阵中的标量数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/568d04f23698088cf4fe07e0.svg) | 普通多头注意力的键和值缓存标量数；系数2对应两种缓存。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3af6a2de19c1f1d50afa0ea7.svg) | 递推内部通道数、每通道状态宽度、当前核心状态标量数。 |

H=4、T=512时分数矩阵有1048576个数；d=32时KV缓存为32768个数，float32占128KiB。D_c=24、N=4给出96个当前状态数，float32占0.375KiB。这里计指定数组，不包括权重、卷积缓存与其他中间量；训练时保留T步状态会引入额外的T因子。

![解析数组规模，非运行时间测量。左计完整注意力分数及训练时逐步展开的状态数；右比较普通单层KV缓存与本例当前递推核心状态的float32存储。卷积缓存、模型权重和其他中间量另计。](https://ml-biomat.com/static/tutorials/machine-learning/figures/abc07bb3bce4195b7c3e1f91.svg?v=abc07bb3bce4)

图 6解析数组规模，非运行时间测量。左计完整注意力分数及训练时逐步展开的状态数；右比较普通单层KV缓存与本例当前递推核心状态的float32存储。卷积缓存、模型权重和其他中间量另计。

图左计数的是指定数组的标量数，右侧按float32的每个数4字节换算。四个注意力头、长度512时，完整分数矩阵包含1048576个数；模型宽度32的单层KV缓存包含32768个数，即128KiB。本章24通道、每通道4维的递推核心只保留96个状态数，另有短卷积所需缓存与模型权重。图明确区分了逐步展开的训练状态和只保留当前状态的推断情形。

实际实现还会改变内存使用。融合注意力算法可以按块计算，避免长期存下完整分数矩阵；稀疏或局部注意力改变参与配对的位置；分组查询注意力减少KV头数，进而改变缓存常数。对角状态更新的显式Python循环易于阅读，而优化后的扫描内核会有不同运行效率。比较部署方案时，记录序列长度、批大小、精度、是否缓存和真实硬件上的测量，才能把数学规模与实际速度接起来。

回到应用问题，完整输入上的内容匹配、逐项生成时反复访问远处细节、连续信号的状态跟踪，要求并不相同。注意力提供按内容重新分配读取权重的方式，选择性状态模型提供按输入更新压缩记录的方式，也可以组合成混合结构。理解它们之后，新的架构名称可以拆回本章的问题：输入被怎样表示，历史怎样保存，当前输出怎样读取，以及哪项实验能显示这些机制是否适合任务。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M32.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

   Transformer原始研究与方法史。

   Primary research link; no paper figure copied
2. [Dive into Deep Learning — The Transformer Architecture](https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html)

   原结构图、编码器解码器与掩码。

   CC BY-SA4.0 text/figures
3. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)

   输入相关状态参数与扫描设计。

   Primary research link; no paper figure copied
4. [state-spaces/mamba — reference implementation](https://github.com/state-spaces/mamba)

   选择性递推、因果卷积与门控的官方实现。

   Apache2.0 repository code; no GPU extension bundled
5. [PyTorch — MultiheadAttention](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)

   本例接口形状、逐头权重与布尔掩码约定。
