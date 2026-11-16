# 把记忆留到最后：RNN、LSTM与GRU

Source: https://ml-biomat.com/tutorials/machine-learning/m15/
Language: zh-CN

沿着一条序列追踪状态与梯度，再亲手打开循环网络的记忆门。

## 读到最后，还记得开头吗

一句“这家店的环境很好，但我不会再来了”，如果只看前半句，很容易判断错说话者的态度。语音、天气记录和设备振动也有相同的特点：当前观测的意义往往依赖之前发生了什么。把每个时间点独立交给普通分类器，会丢掉顺序和上下文；把整段内容一次拼成固定长度向量，又难以适应长短不同的记录。循环神经网络的出发点，是让模型一边接收新信息，一边维护一份可以更新的内部状态。

这份状态有点像阅读时的便笺。它不必逐字保存已经看到的全部内容，却需要留下对当前任务有用的线索。问题在于，便笺会不断被新信息修改：几十个无关读数之后，开头那条关键记录还能否影响答案？本章先把循环网络沿时间展开，理解梯度怎样跨越许多步，再进入 LSTM 和 GRU 的门机制。最后用一个明确的小实验检验它们：只在序列第一项给出要记住的正负号，后面不断出现干扰，读完后再回答第一项是什么。

这个合成任务的好处是答案由生成规则直接决定，记忆距离也可以单独改变。我们能够比较模型在训练长度和更长序列上的行为，查看一个记忆单元的门值，而不必同时处理分词、语言知识和复杂语音信号。到章末，你应能区分细胞状态与隐藏状态，解释 teacher forcing 为什么改变训练时的输入，并根据任务是否能看见未来，选择单向、双向或序列到序列的组织方式。

## 同一套参数，沿时间使用多次

普通 RNN 每读入一个新向量，就把它与上一时刻的隐藏状态一起变换，得到新的隐藏状态。将循环画成一个环很节省空间，却容易让人以为网络在执行一种特殊运算。把它沿时间展开，就会看见一条熟悉的计算链：第一步处理第一项，第二步处理第二项和第一步留下的状态，第三步再接着计算。每一步都使用同一组参数，因此模型学习的是更新规则，长度增加时主要增加计算次数，而不是重新增加一套参数。

$$
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间步，离散索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | 当前输入，含d个特征；本例为标准化数值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85eedc5e4cf9b6744741f60b.svg) | 当前和前一隐藏状态，m为隐藏宽度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/157ea1323b2c054eafb68cee.svg) | 输入与状态的权重矩阵，本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/10da1fa641a861563af1756d.svg) | 偏置向量，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cbf403b7976b754f4c306eac.svg) | 逐元素双曲正切，将每个输入映射到−1与1之间。 |

先分别变换输入和旧状态，使它们具有相同的m维形状，再相加并经过非线性。标量例中W_x=1、W_h=0.5、b=0、h_0=0，输入依次为1、0，得到h_1≈0.7616、h_2≈0.3634。批处理时库把批维加在外面；本章batch_first=True对应输入形状[批大小,时间长度,特征数]。

例如把所有量暂时缩成标量，输入权重取 1，状态权重取 0.5，偏置为零，初始状态为零。第一次输入 1，状态约为 tanh(1)＝0.7616；第二次输入零，状态约为 tanh(0.5×0.7616)＝0.3634。第二步虽然没有新信号，仍然能够携带过去的信息；同时，这个值比上一时刻小，提醒我们“存在状态”并不等于“能够长久保存状态”。在真正的向量状态中，不同分量可以记录不同线索，更新规则也由数据学习。

输出位置决定了任务形式。整段序列分类可以从最终状态读出一个类别，例如判断一段声音是否含有某个事件；逐步预测会在每个时刻读出结果，例如给每个词标注词性；序列生成则把当前输出变成下一步的部分输入。它们可以共享同一种循环单元，但训练目标、损失位置和可使用的信息不同。实际代码中应先确定这些对象，再决定网络层数，否则很容易把“最后一个时间步的状态”误当成所有任务通用的答案。

## 长序列为什么难训练

时间反向传播，简称 BPTT，就是把上一章的反向传播应用到展开后的循环计算图。最后一步的误差若要影响第一步使用的参数，梯度必须经过中间许多次状态变换。为了看清这个过程，先想象一条只有线性状态更新的标量链，每一步把旧状态乘以同一个数。如果这个倍率略小于 1，连续相乘会迅速缩小；略大于 1，则会迅速放大。真实 RNN 还包含非线性导数与矩阵方向，但这种乘积结构已经解释了长距离训练的核心困难。

$$
h_t=a h_{t-1},\qquad \frac{\partial h_T}{\partial h_0}=\prod_{t=1}^{T}a=a^T
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e707e5d250917043d81b6e.svg) | 简化标量链的当前状态、初始状态，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 每一步固定的状态倍率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | 当前时间索引、总步数，均为整数；此处T为指数中的步数，不是转置符号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e1008907cad09e198dabfbc2.svg) | 终点状态相对初始状态的局部变化率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eddaa20e15661440b4bf8d78.svg) | 把各时间步的局部导数连乘。 |

链式法则让每一步的倍率连乘。0.8的20次方约0.01153，1.2的20次方约38.34；前者缩小远程信号，后者放大它。这条式子对应无输入、无非线性的标量模型。真实RNN需要乘相应的雅可比矩阵，图中用标量链单独展示连乘机制。

每步倍率为 0.8，跨越 20 步后只剩约 0.0115；每步倍率为 1.2，同样跨越 20 步会变成约 38.34。前一种情况下，远处误差难以显著改变早期参数；后一种情况下，一次更新可能过大。梯度裁剪处理的是过大的梯度：当整体梯度范数超过指定阈值，就按同一比例缩小所有分量，保留方向。它有助于控制更新幅度，却不会把已经很小的远程信号重新放大。较长任务还可用截断 BPTT 控制图的长度，代价是截断位置之前的梯度联系不再保留。

![解析计算的两种时间传递。左：线性标量链的梯度倍率，纵轴为对数尺度；右：固定遗忘门、无新写入时的状态保留比例。两图分别隔离连乘机制和直接细胞通路。](https://ml-biomat.com/static/tutorials/machine-learning/figures/60cae506d9b36eecb7abd02d.svg?v=60cae506d9b3)

图 1解析计算的两种时间传递。左：线性标量链的梯度倍率，纵轴为对数尺度；右：固定遗忘门、无新写入时的状态保留比例。两图分别隔离连乘机制和直接细胞通路。

Hochreiter 与 Schmidhuber 在 1997 年提出的 LSTM，针对的正是跨较长间隔学习依赖关系的问题。后来常用的 LSTM 形式加入遗忘门，让状态既能保存，也能主动更新或清空。这段历史能帮助理解结构选择：门让模型通过训练决定信息怎样写入、保留和读出。读结构图时，最值得注意的是贯穿时间的状态路径，以及新信息通过什么操作加入这条路径。

## LSTM：保存、写入和读出分开控制

LSTM 保留两个相关但不同的状态。细胞状态承担持续存储，隐藏状态是当前向其他层提供的可见输出。可以把它们理解成笔记本中的记录与此刻读给别人听的内容：记录仍然存在，并不意味着每一步都要完整读出来。遗忘门控制旧记录保留多少，输入门控制候选新记录写入多少，输出门控制当前状态向外显露多少。这些门的数值由当前输入和上一隐藏状态共同计算，通常在零到一之间连续变化，具有可微性。

$$
\begin{aligned}q_t&=\sigma(W_qx_t+U_qh_{t-1}+b_q),\quad q\in\{f,i,o\}\\g_t&=\tanh(W_gx_t+U_gh_{t-1}+b_g)\\c_t&=f_t\odot c_{t-1}+i_t\odot g_t\\h_t&=o_t\odot\tanh(c_t)\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cbf32d76af4802a50139ab94.svg) | 遗忘门、输入门、输出门，各分量在0与1之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/71d6ab9eefc849614ba23b2b.svg) | 表示三组门分别使用相同形式、不同参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fa9a7f586b22317620a37f.svg) | 候选写入内容，各分量在−1与1之间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce050e1043335673a387a783.svg) | 当前、前一细胞状态，数值不限于0到1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85eedc5e4cf9b6744741f60b.svg) | 当前、前一隐藏状态，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | 当前d维输入，t为时间索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e343378f53f518c611668c8b.svg) | 输入与隐藏状态的权重矩阵，每组单独学习。 |
| ![Formula](https://ml-biomat.com/static/agent-math/20040137dd3a5d5109d96d6f.svg) | 偏置；库中输入、状态两组偏置可相加得到这里的合并偏置。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8baa8c92c5b738f80358844d.svg) | sigmoid逐元素映射到0–1；⊙表示对应位置相乘。 |

门和候选内容先由输入与旧隐藏状态计算，随后按坐标更新细胞状态。以一个坐标为例，f=0.9、i=0.2、g=−0.5、旧c=0.8得到新c=0.62；o=0.7时新h≈0.38579。若固定f、停止写入，初始状态沿直接通路每步乘f，因此0.99跨20步保留约0.81791。

![LSTM的信息通路。顶部横向线承载细胞状态，三个门分别控制保留、写入和读出。图：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola，《Dive into Deep Learning》LSTM章节，CC BY-SA 4.0；保留原图英文符号。](https://ml-biomat.com/static/tutorials/machine-learning/figures/645861d6b929b1753537861a.svg?v=645861d6b929)

图 2LSTM的信息通路。顶部横向线承载细胞状态，三个门分别控制保留、写入和读出。图：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola，《Dive into Deep Learning》LSTM章节，CC BY-SA 4.0；保留原图英文符号。

图中圆圈里的逐元素乘法很关键。一个门值为 0.9，表示对应分量的旧状态先保留九成；每个状态分量可使用不同的门值，一些信息保留得更多，另一些更新更快。假设旧细胞状态为 0.8，遗忘门为 0.9，输入门为 0.2，候选内容为 −0.5，则新状态为 0.9×0.8＋0.2×(−0.5)＝0.62。再取输出门 0.7，隐藏状态约为 0.7×tanh(0.62)＝0.3858。这个小算例把保存、改写与读出分成了三个可检查的步骤。

细胞状态中的加法提供了一条比每步都整体重新变换更直接的通路。如果没有新写入，并把遗忘门固定为 0.99，旧内容跨越 20 步后仍保留约 81.8%；固定为 0.9 时则约为 12.2%。这里算的是固定门值下的直接状态通路，完整网络的梯度还包含门本身依赖输入和隐藏状态的其他路径。因此，LSTM 提供的是可学习的长程传递机制，实际能记住什么，要由训练任务和得到的门值来说明。

在代码层面，同一个 LSTM 单元可以一次计算四组线性变换，随后分别得到输入门、遗忘门、候选内容和输出门。PyTorch 把这四组参数按固定顺序拼在一起，以提高计算效率。本章的实验不仅调用 `nn.LSTM`，还逐时间步拆开它的权重、重算门值与状态，再与模块输出比较。这让结构图、公式、库接口和实际数值之间建立了逐项对应关系。

## GRU与不同长度的序列

GRU 用更新门和重置门组织记忆，不再单独保留一份细胞状态。按本章采用的约定，更新门接近 1 时更多保留旧隐藏状态，接近零时更多采用候选状态；重置门决定生成候选内容时应保留多少旧信息。Cho 等人在 2014 年的编码器—解码器工作中使用了这种门控结构。它提供了另一种参数更紧凑的状态更新方式，尤其适合把长程保留与当前改写放在同一个隐藏向量中理解。

$$
\begin{aligned}q_t&=\sigma(W_{iq}x_t+b_{iq}+W_{hq}h_{t-1}+b_{hq}),\quad q\in\{r,z\}\\n_t&=\tanh\!\left(W_{in}x_t+b_{in}+r_t\odot(W_{hn}h_{t-1}+b_{hn})\right)\\h_t&=z_t\odot h_{t-1}+(1-z_t)\odot n_t\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/daeea55e3bce10b0e01fed9a.svg) | 重置门、更新门，无量纲；本约定z越大，旧状态保留越多。 |
| ![Formula](https://ml-biomat.com/static/agent-math/20763ce29d53551efab2dad5.svg) | 候选、当前和前一隐藏状态，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | 当前输入，d为特征数，t为时间索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af3bd10bd01b7d3e9dff7bb5.svg) | 输入权重；下标i表示输入分支，q表示r或z。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5cb27e871bec5f048d93edee.svg) | 隐藏状态权重，h下标表示隐藏分支。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ba36451946e90d34511793eb.svg) | 各分支偏置，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/88e066a5cc36eb5e43345466.svg) | sigmoid、双曲正切、逐元素乘法和逐元素的互补权重。 |

公式采用PyTorch的重置位置：先完成隐藏分支的线性变换，再乘重置门。新状态是旧状态与候选的逐元素加权平均。旧状态0.8、候选−0.5、z=0.75给出0.475。两项权重相加为1，但门随当前输入与旧状态变化，因此整体更新仍是非线性的。

如果旧状态为 0.8，候选状态为 −0.5，更新门为 0.75，新状态就是 0.75×0.8＋0.25×(−0.5)＝0.475。与 LSTM 的例子对照，可以看出 GRU 的加权混合把两部分合在同一个状态中。不同教材或库可能用相反含义命名更新门，还可能把重置操作放在线性变换之前或之后。本章公式采用 PyTorch 的实现位置，阅读其他代码时应逐项核对，特别是隐藏向量乘矩阵与门的逐元素乘法通常不能任意交换顺序。

实际数据中的序列长短不同，常见做法是在批内补齐到同一长度，同时记录每个样本的有效长度。补零是存储安排，不自动告诉网络“这部分不算内容”。若直接取补齐后的最后一步，得到的可能是模型读过多个零之后的状态；逐步损失也可能把填充符当成真实目标。可以使用打包序列让循环层按有效长度工作，或按有效位置提取状态、用掩码计算损失。对于三条长度为 3、5、2 的记录，真正需要评价的时间点总数是 10，而不是补齐后的 15。

$$
L=\frac{\sum_{n=1}^{N}\sum_{t=1}^{T_{\max}}m_{nt}\ell_{nt}}{\sum_{n=1}^{N}\sum_{t=1}^{T_{\max}}m_{nt}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 按有效位置平均的损失；交叉熵使用自然对数时单位为nats。 |
| ![Formula](https://ml-biomat.com/static/agent-math/26a66e1ac1aef97aededc3dd.svg) | 批内序列数、序列编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af6c1eaa3efa8ef9f3aba00b.svg) | 补齐后的最大长度、位置编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6868759f6c37deff85b7865b.svg) | 有效位置为1、填充位置为0的掩码，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a9d0be830f91fed383b9b28.svg) | 该位置的预测损失，例如目标符号负对数概率。 |

分子只累加有效位置的误差，分母数出这些位置。三条长度3、5、2的序列共有10个有效位置；若它们的损失总和为4，平均为0.4。除以补齐后的15会低估每个真实位置的平均误差。批内至少有一个有效位置时才使用此平均。

多层循环网络把一层产生的状态序列作为下一层的输入，用深度增加逐步表示的复杂性。双向网络则分别从前向后、从后向前读取完整序列，再组合两个方向的状态。离线句子分析可以利用这种双侧上下文；实时告警和下一时刻预测在决策时还没有未来数据，必须相应限制信息流。这是由任务可见信息决定的结构选择。序列长度、方向数和层数进入张量形状后，也需要与初始状态及最终读出保持一致。

## 用实际实验测量记忆距离

完整程序生成两通道序列。第一通道的第一项为随机的 +1 或 −1，后面的值是标准差 0.3 的独立高斯干扰；第二通道只在第一步取 1，告诉模型哪一项需要记住。任务是在读完后判断首项的符号。训练集包含 800 条长度为 16 的序列，验证集包含另行生成的 300 条同长度序列。测试时分别生成长度为 8、16、32、64 的 500 条新序列，观察改变记忆距离以后的行为。

RNN、LSTM 和 GRU 都使用 16 维隐藏状态，相同的训练轮数、批大小与优化设置，并按各自验证损失选择参数。它们的参数总数分别为 337、1297 和 977，因此这是一组同隐藏宽度的教学比较。门结构需要额外参数，具体应用中还可以继续控制参数预算或计算时间。程序还画出一条 64 步样本在不同读取位置的预测，用来区分“最终答错”与“信息在什么时候改变”这两个问题。

### 完整Python：训练三种记忆单元并拆解LSTM门值

依赖NumPy、Matplotlib、PyTorch。运行python main.py --output results --language zh生成三组SVG、summary.json、原始轨迹与三个模型参数。程序使用CPU双线程和固定随机种子；训练集与验证集分别生成，按验证损失选参数，再测试四种长度。

```
"""Remember a marked first observation with RNN, LSTM, and GRU.

Synthetic task: the first channel starts with a random sign; subsequent values
are distractors. The second channel marks the first observation. Predict its sign
after the whole sequence. CPU training and all plots are self-contained.
"""
from pathlib import Path
import argparse,copy,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn


def make_data(n,length,seed):
    rng=np.random.default_rng(seed)
    labels=rng.integers(0,2,n)
    x=np.zeros((n,length,2),dtype=np.float32)
    x[:,:,0]=rng.normal(0,.3,(n,length))
    x[:,0,0]=2*labels-1
    x[:,0,1]=1
    return torch.from_numpy(x),torch.tensor(labels,dtype=torch.float32)


class Remember(nn.Module):
    def __init__(self,kind):
        super().__init__()
        self.recurrent=getattr(nn,kind)(2,16,batch_first=True)
        self.readout=nn.Linear(16,1)
    def forward(self,x):
        output,_=self.recurrent(x)
        return self.readout(output[:,-1,:]).squeeze(-1)


def run(output,language):
    output.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    train_x,train_y=make_data(800,16,151)
    val_x,val_y=make_data(300,16,152)
    models={};histories={};metrics={};colors={'RNN':'#0072B2','LSTM':'#D58500','GRU':'#008675'}
    lengths=[8,16,32,64]
    for kind in ['RNN','LSTM','GRU']:
        torch.manual_seed(153)
        model=Remember(kind);opt=torch.optim.Adam(model.parameters(),lr=.01)
        criterion=nn.BCEWithLogitsLoss();history=[];best=float('inf');best_state=None;best_epoch=0
        generator=torch.Generator().manual_seed(154)
        for epoch in range(1,81):
            model.train();order=torch.randperm(len(train_x),generator=generator)
            for indices in order.split(100):
                opt.zero_grad(set_to_none=True)
                loss=criterion(model(train_x[indices]),train_y[indices])
                loss.backward();nn.utils.clip_grad_norm_(model.parameters(),max_norm=1.0);opt.step()
            model.eval()
            with torch.no_grad():
                vl=criterion(model(val_x),val_y).item()
                tl=criterion(model(train_x),train_y).item()
            history.append([epoch,tl,vl])
            if vl<best:best=vl;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
        model.load_state_dict(best_state);model.eval();models[kind]=model;histories[kind]=np.array(history)
        accuracies=[]
        with torch.no_grad():
            for length in lengths:
                tx,ty=make_data(500,length,160+length)
                accuracies.append(float(((model(tx)>=0)==ty.bool()).float().mean()))
        metrics[kind]={'parameters':sum(p.numel() for p in model.parameters()),'best_epoch':best_epoch,
                       'validation_loss':best,'test_accuracy_by_length':dict(zip(map(str,lengths),accuracies))}
        torch.save(model.state_dict(),output/f'{kind}.pt')

    # Exact single-cell arithmetic with controlled gates, independent of training.
    f,i,o,g,c_prev=.9,.2,.7,-.5,.8
    c=f*c_prev+i*g;h=o*np.tanh(c)
    assert abs(c-.62)<1e-12
    # PyTorch LSTM gate order: input, forget, candidate, output.
    sample,_=make_data(1,16,999)
    cell=models['LSTM'].recurrent;H=torch.zeros(1,16);C=torch.zeros(1,16);trace=[]
    with torch.no_grad():
        for t in range(16):
            pre=sample[:,t]@cell.weight_ih_l0.T+cell.bias_ih_l0+H@cell.weight_hh_l0.T+cell.bias_hh_l0
            ip,fp,gp,op=pre.chunk(4,dim=1)
            I,F,G,O=torch.sigmoid(ip),torch.sigmoid(fp),torch.tanh(gp),torch.sigmoid(op)
            C=F*C+I*G;H=O*torch.tanh(C)
            trace.append(np.stack([F[0].numpy(),I[0].numpy(),O[0].numpy(),C[0].numpy()]))
        full,_=cell(sample)
        manual_error=float(torch.max(torch.abs(full[:,-1,:]-H)))
    assert manual_error<1e-6
    trace=np.stack(trace)
    # Choose the unit with greatest absolute terminal cell value; selection is explicit.
    unit=int(np.argmax(np.abs(trace[-1,3])))
    # Hold the same first signs fixed while reading every prefix of a 64-step set.
    # Removing distractor amplitudes isolates learned state dynamics from noise.
    diagnostic_x,diagnostic_y=make_data(500,64,4242)
    diagnostic_zero=diagnostic_x.clone();diagnostic_zero[:,1:,0]=0
    prefix_diagnostics={}
    with torch.no_grad():
        for kind,model in models.items():
            for condition,dx in [('noise',diagnostic_x),('zero_suffix',diagnostic_zero)]:
                hidden,_=model.recurrent(dx)
                predictions=model.readout(hidden).squeeze(-1)>=0
                accuracy=(predictions==diagnostic_y[:,None].bool()).float().mean(0)
                prefix_diagnostics[f'{kind}_{condition}']=accuracy.numpy().tolist()

    fig=plt.figure(figsize=(12,7),layout='constrained');gs=fig.add_gridspec(2,3)
    ax=fig.add_subplot(gs[0,:2])
    for kind in models:ax.plot(histories[kind][:,0],histories[kind][:,2],color=colors[kind],label=kind)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('验证交叉熵','Validation cross entropy'));ax.legend()
    ax=fig.add_subplot(gs[0,2])
    for kind in models:ax.plot(lengths,[metrics[kind]['test_accuracy_by_length'][str(t)] for t in lengths],'-o',color=colors[kind],label=kind)
    ax.axvline(16,color='#66737a',ls='--',lw=1);ax.axhline(.5,color='#8c989f',ls=':',lw=1)
    ax.set(xticks=lengths,ylim=(0,1.03),xlabel=tr('测试序列长度','Test sequence length'),ylabel=tr('准确率','Accuracy'))
    ax=fig.add_subplot(gs[1,:])
    probe,probe_y=make_data(1,64,999)
    with torch.no_grad():
        for kind,model in models.items():
            hidden,_=model.recurrent(probe)
            prob=torch.sigmoid(model.readout(hidden)).numpy().ravel()
            correct=prob if int(probe_y[0])==1 else 1-prob
            ax.plot(np.arange(1,65),correct,color=colors[kind],label=kind)
    ax.axvline(16,color='#66737a',ls='--',lw=1)
    ax.set(xticks=[1,8,16,32,48,64],ylim=(0,1.03),xlabel=tr('读到的时间步（离散索引）','Observed time steps (discrete index)'),ylabel=tr('真实首项类别的读出概率','Readout probability of the true first class'));ax.legend(ncol=3)
    fig.savefig(output/f'recall-{language}.svg');plt.close(fig)

    fig=plt.figure(figsize=(12,5.4),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(trace[:,:,unit].T,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    # Show gate rows only because cell state is not constrained to [0,1].
    ax.clear();im=ax.imshow(trace[:,:3,unit].T,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    ax.set(yticks=[0,1,2],yticklabels=[tr('遗忘门 f','Forget f'),tr('输入门 i','Input i'),tr('输出门 o','Output o')],
           xticks=[0,3,7,11,15],xticklabels=[1,4,8,12,16],xlabel=tr('时间步','Time step'))
    fig.colorbar(im,ax=ax,label=tr('门值（0–1）','Gate value (0–1)'),shrink=.7)
    ax=fig.add_subplot(gs[0,1]);ax.plot(np.arange(1,17),trace[:,3,unit],'-o',color=colors['LSTM'])
    ax.set(xlabel=tr('时间步','Time step'),ylabel=tr(f'细胞状态（单元{unit}）',f'Cell state (unit {unit})'))
    fig.savefig(output/f'gates-{language}.svg');plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained')
    steps=np.arange(0,41)
    for gain in [.8,1,1.2]:axes[0].semilogy(steps,gain**steps,label=f'a={gain}')
    axes[0].set(xlabel=tr('跨越步数','Number of steps'),ylabel=tr('简化线性链的梯度倍率','Gradient multiplier in a linear chain'));axes[0].legend()
    for keep in [.5,.9,.99]:axes[1].plot(steps,keep**steps,label=f'f={keep}')
    axes[1].set(xlabel=tr('跨越步数','Number of steps'),ylabel=tr('固定门、无新写入时保留比例','Retained fraction: fixed gate, no new input'));axes[1].legend()
    fig.savefig(output/f'memory-{language}.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,4.3),layout='constrained')
    keys=list(prefix_diagnostics)
    im=ax.imshow(np.array([prefix_diagnostics[k] for k in keys]),aspect='auto',cmap='viridis',vmin=0,vmax=1)
    labels=[k.replace('_zero_suffix',tr('：后续全零',': zero suffix')).replace('_noise',tr('：有干扰',': distractors')) for k in keys]
    ax.set(yticks=range(6),yticklabels=labels,xticks=[0,7,15,23,31,39,47,55,63],xticklabels=[1,8,16,24,32,40,48,56,64],xlabel=tr('同一组序列的前缀长度','Prefix length of the same sequence set'))
    ax.axvline(15,color='white',ls='--',lw=1)
    fig.colorbar(im,ax=ax,label=tr('500条序列的分类准确率','Classification accuracy over 500 sequences'),shrink=.8)
    fig.savefig(output/f'prefix-{language}.svg');plt.close(fig)
    summary={'train_size':800,'validation_size':300,'test_per_length':500,'training_length':16,
             'epochs':80,'hidden_size':16,'models':metrics,'manual_cell':{'f':f,'i':i,'o':o,'g':g,'c_previous':c_prev,'c':c,'h':float(h)},
             'manual_lstm_vs_module_error':manual_error,'plotted_unit':unit,
             'linear_gradient_20':{'0.8':.8**20,'1.2':1.2**20},'prefix_diagnostics':prefix_diagnostics,'torch_version':torch.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',sample=sample.numpy(),trace=trace,**{f'history_{k}':v for k,v in histories.items()})
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'))
    p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![上排比较验证损失和各长度的测试准确率；每个测试长度含500条新序列。虚线标出训练长度16，下排跟踪一条64步样本的真实首项类别读出概率。固定隐藏宽度16，RNN/LSTM/GRU参数数分别为337/1297/977；数据由明确的合成任务生成。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e27425bc2407f535dbefc6cb.svg?v=e27425bc2407)

图 3上排比较验证损失和各长度的测试准确率；每个测试长度含500条新序列。虚线标出训练长度16，下排跟踪一条64步样本的真实首项类别读出概率。固定隐藏宽度16，RNN/LSTM/GRU参数数分别为337/1297/977；数据由明确的合成任务生成。

在这次固定配置下，三个模型对长度为 8 和 16 的测试集都达到 100% 准确率。长度延长到 32 时，RNN 的准确率降到 0%，延长到 64 时为 16.2%；LSTM 与 GRU 在这两个测试长度上都为 100%。这里出现的零准确率不是图中漏画的数据，也不等同于随机猜测：模型对该测试分布发生了系统性反转。下方的逐步读出曲线帮助检查状态演化如何改变最终答案，使我们看见训练长度之外的行为可以与同长度测试很不一样。

这组结果的解释应与任务条件放在一起：信号只在开头出现，后面都是干扰，训练长度固定为 16，门控模型具有更多参数。我们因此学到一种实验设计方法：改变需要保存信息的间隔，保持生成规则和标签定义清楚，再检查状态与读出。把这种设计迁移到真实语音或文本时，可以改成控制前后线索的距离、插入无关片段，或比较不同长度分组。模型是否真正利用了需要的上下文，就能通过具体干预来研究。

![固定500条64步序列，分别在每个前缀末端读出；seed=4242。每种模型比较原始高斯干扰与后续值全部置零，首项和标签保持相同。共享色标为准确率，虚线标出训练终点16；RNN的交替颜色显示终止位置依赖。](https://ml-biomat.com/static/tutorials/machine-learning/figures/4d2e2ca7b73a4921031fe73a.svg?v=4d2e2ca7b73a)

图 4固定500条64步序列，分别在每个前缀末端读出；seed=4242。每种模型比较原始高斯干扰与后续值全部置零，首项和标签保持相同。共享色标为准确率，虚线标出训练终点16；RNN的交替颜色显示终止位置依赖。

进一步固定同一组500条64步序列，在每个前缀结束处读出答案，RNN在第15、16、17步的准确率依次为0%、100%、0%。把首项之后的干扰全部改成零，这三个结果仍相同，较长前缀中的反复变化也仍然存在。由此可以把现象定位得更具体：这个模型学到了依赖终止时刻的状态与读出动力学，而不是简单地随着时间越来越记不住。训练只要求第16步给出正确答案，并没有约束每个中间位置的读出。逐步检查同一批序列，把长度依赖与不同测试样本带来的变化分开了。

![实际训练LSTM的门值与细胞状态：展示样本seed=999、长度16中终点细胞状态绝对值最大的单元1。左侧门值共用0–1色标，右侧细胞状态独立标度。图中值来自逐步拆解保存的模型参数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/622c278ed837d12cc8e17df9.svg?v=622c278ed837)

图 5实际训练LSTM的门值与细胞状态：展示样本seed=999、长度16中终点细胞状态绝对值最大的单元1。左侧门值共用0–1色标，右侧细胞状态独立标度。图中值来自逐步拆解保存的模型参数。

门值图选择了这条示例中终点细胞状态绝对值最大的单元，并把选择规则写在图注里。三个门都用相同的零到一色标，细胞状态单独画曲线，因为它并不受零到一区间约束。逐步手算与 `nn.LSTM` 的最终隐藏状态最大差约为 5.96×10⁻⁸，符合本实验32位浮点计算的数值精度。观察一个单元能帮助理解机制；同时，任务信息通常分散在多个单元中，检查整组状态和输出会给出更完整的图景。

## 从一个答案走向一段输出

分类任务在读完后给出一个答案；翻译、摘要和语音转写往往需要输出另一段长度不同的序列。编码器—解码器把这项工作分成两个相连的过程：编码器读取输入并形成上下文表示，解码器根据上下文和已经产生的输出，逐项预测后续内容。早期的固定向量上下文要求把整段输入压进有限状态，长序列会增加保存细节的压力；注意力机制随后提供了按需读取多个输入位置的办法。理解这个困难，比直接记住“编码器加解码器”更容易连接到下一章。

$$
p(y_{1:T}\mid x)=\prod_{t=1}^{T}p(y_t\mid y_{<t},c(x))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 完整输入序列，长度可以与输出不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9969bc836ef1d3ea36f836a1.svg) | 完整目标序列、当前目标、此前目标前缀；离散符号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/db8506bdb7f13a6e716f3e71.svg) | 输出长度及当前位置，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a51c780ea99335cf8cbecb3.svg) | 编码器提供的上下文，可为向量或状态序列。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c93668eb0c4447eecb479c8.svg) | 概率、给定条件、逐步概率相乘；概率无量纲。 |

联合概率按条件概率的链式规则拆开，每一步都要看此前输出。若三个目标词在正确前缀下的概率为0.8、0.7、0.9，整段概率为0.504。Teacher forcing用真实前缀计算训练概率；自由生成时，前缀由模型已经生成的词构成。

训练时已经知道正确目标，因此可以把正确的前一个词送给解码器，这叫 teacher forcing。若目标序列是“红 蓝 结束”，解码器的输入依次为“开始 红 蓝”，需要预测的标签则为“红 蓝 结束”。输入与标签相差一个位置是关键，不能让当前目标直接进入预测自己的那一步。推断时没有正确目标可用，模型会把自己刚产生的词送回下一步。如果前面预测错了，后续条件也随之改变，因此训练损失和自由生成的序列质量需要分别观察。

相同组织方式也适用于连续值。时间序列预测可以输出未来若干步的实数，用误差损失训练；语音转写把声音帧映射成文本符号，需要处理声音与文字在时间上的不同节奏；文本生成则从开始标记或提示词出发逐步产生后续词元。输出类型决定读出层、损失和评价指标。回归误差、逐词准确率和整句生成质量回答不同问题，选择模型时应同时明确输入能看到多长、输出要预测什么以及何时作出决策。

## 把三个门交给你控制

这个标量实验把门值固定，起始细胞状态为0.8，在指定时间步写入候选内容−0.5，其余时间不写入。改变遗忘门观察保存速度，改变输入门观察写入量，再把输出门调到零：蓝色记忆仍可存在，橙色读出却消失。图由下方公式逐步计算。

[Figure: 细胞状态与隐藏读出随时间变化](https://ml-biomat.com/tutorials/machine-learning/m15/#M15-plot)

蓝线：细胞状态c；橙线：隐藏状态h；虚线：写入时刻。时间为离散步数，状态为无量纲。直接保留比例只计算固定遗忘门对初始内容的作用。

## 带着时间结构检查一个新任务

面对新的序列数据，可以先画一条时间轴，标出输入何时出现、目标何时可知、预测何时必须完成。然后确定有效长度与采样间隔，检查是否把同一对象相邻片段分到了训练和测试两侧。如果预测未来，训练数据应来自预测时实际已经可见的过去；如果分析一段已录制的声音，双向上下文可以成为合理输入。把这些条件说清楚，网络结构与数据划分才会围绕同一任务工作。

随后建立一个能解释的基线，例如最近一次观测、移动平均或简单线性状态模型，再比较循环网络带来的变化。检查长度分组、错误位置和干扰条件，比只报告全体平均分更有助于理解记忆机制。保存模型时，词表、归一化规则、填充标记、隐藏状态初始化与读出方式也要一起保留。若连续处理同一条长记录，可以明确地传递状态；若开始一条新的独立记录，就应按任务定义重新初始化，避免把上一条记录的信息带进新样本。

LSTM 和 GRU 给我们提供了可学习的状态管理方法：信息怎样保留，怎样改写，怎样对当前输出可见。注意力会进一步改变读取历史信息的方式，状态空间模型则从另一条路径研究长序列的递推和计算效率。它们都可以回到本章的同一组问题来理解：模型能访问什么信息，怎样跨时间传递它，计算代价怎样随长度增长，以及实验中如何证明所需的依赖关系确实被利用。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M15.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning — Long Short-Term Memory](https://d2l.ai/chapter_recurrent-modern/lstm.html)

   结构推导、历史与授权原图。

   CC BY-SA 4.0 text/figures; code Apache 2.0
2. [Dive into Deep Learning — Gated Recurrent Units](https://d2l.ai/chapter_recurrent-modern/gru.html)

   GRU机制与约定比较。

   CC BY-SA 4.0
3. [Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078)

   Cho等，2014；门控编码器—解码器的原始研究。

   Linked as primary research; no figure copied
4. [PyTorch — LSTM](https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html)

   门的拼接次序、参数与状态形状。

   PyTorch documentation; technical reference
5. [PyTorch — GRU](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GRU.html)

   本章重置门实现位置。

   PyTorch documentation; technical reference
6. [Dive into Deep Learning — Sequence to Sequence Learning](https://d2l.ai/chapter_recurrent-modern/seq2seq.html)

   编码器—解码器、填充掩码与teacher forcing。

   CC BY-SA 4.0
