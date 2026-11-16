# 听见结构：语音、声谱与音频学习

Source: https://ml-biomat.com/tutorials/machine-learning/m20/
Language: zh-CN

从一个音调到一句话，连接采样、声音事件、识别、合成和声源分离。

## 1. 一段声音，可以回答几种不同的问题？

听见门铃时，我们通常先判断发生了什么，再决定是否开门；在会议中，我们既要听清说了什么，也要分辨是谁在说话；听到一首歌，还会注意旋律、节拍与不同乐器。这些活动都从声音出发，却对应不同的机器学习任务。音频分类判断整段录音属于哪类，声音事件检测还要定位开始和结束，自动语音识别把声音转成文字，说话人分段回答“谁在什么时候说话”，语音合成则沿相反方向把文字变成可听的波形。先选定问题，才能确定需要什么标签和怎样评价答案。

麦克风记录的是随时间变化的信号，并不会直接给出“猫叫”“请左转”这样的语义。声音从声源经过房间反射、背景噪声和设备响应，到达录音系统后又被采样与量化。波形里的某个变化可能来自说话内容，也可能来自距离、音量或麦克风。一个能在同一房间识别训练录音的模型，换到另一个房间可能就失去依据。因此，音频学习既要理解信号表示，也要设计能够区分内容与录音条件的实验。

本章从可听、可画、可手算的合成声音开始。我们训练一个小型声谱分类器，比较保留时间结构与把时间平均掉的差别；再把两个频带分开的声音混合，用明确的频带规则恢复目标，并同时查看信噪比与试听结果。语音识别、合成和说话人分析沿这条信号处理主线展开，分别解释输入、输出、训练信号和评价方法。示例中的扫频声用于检验这些计算环节，不需要先掌握语言学，也能看清波形怎样变成学习任务。

## 2. 从空气振动到一列数字

模拟信号连续变化，数字录音则每隔固定时间取一次样本。采样率为 8000 Hz，意思是每秒记录 8000 个数；两秒单声道录音就有 16000 个样本。频率为 440 Hz 的正弦波每秒完成 440 次振动，而振幅描述信号摆动的大小。频率、采样率和振幅分别回答不同问题，不能互换。未经声压校准的数字振幅通常以相对满量程的数值表示，因此一段录音里的 0.5 不能直接解释成某个固定的声压或响度。

$$
t_n=\frac{n}{f_s},\qquad x[n]=A\sin(2\pi f_0t_n+\phi),\qquad N=f_sT
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5fb7428d211201250c2723f.svg) | 样本索引，从 0 开始的整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a7fe25f77889bee1430ff4c0.svg) | 每秒采样个数，单位 Hz，即 s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af73c71154f6f0e1e155cc73.svg) | 第 n 个样本的时间与录音时长，单位秒。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4137d12b0e3cd75eb27ad555.svg) | 数字样本及振幅，使用统一的相对振幅单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/36617854c069c6f283a50186.svg) | 正弦信号频率，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ea4606e878cd1dc5ff695b.svg) | 初始相位，弧度；三角函数角度无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/54c5f8946c55301722df6f6e.svg) | 样本总数，整数；这里假设时长与采样率乘积为整数。 |

每秒采 f_s 个数，两个样本之间就相隔 1/f_s 秒。把这个时间代入连续正弦，便得到数字序列。f_s=8000 Hz 时相邻样本间隔 0.125 ms，2 秒共有 16000 个样本。若 f₀=1000 Hz、A=1、φ=0，前五个样本为 0、√2/2、1、√2/2、0，每个周期有 8 个样本。2πf₀t 的单位相互抵消，表示已经转过多少相位。

采样定理说明，在带限等条件满足时，采样率应高于信号最高频率的两倍，才能从样本唯一恢复带内信号。若用 8000 Hz 采样，超过 4000 Hz 的成分会折叠到低频，产生混叠。把 5000 Hz 的余弦按这个速率取样，得到的样本与 3000 Hz 余弦相同；只看这些数字，已经无法知道原声是哪一种。降低采样率前，需要先用抗混叠滤波去掉将要超出新带宽的成分。单纯删掉一些样本，并不能完成正确的重采样。

这些限制在电话与录音技术的发展中一直很实际：传输和存储带宽有限，而人们又希望保留足够的信息辨认语音。数字信号处理把连续变化的声音转成可重复计算的对象，随后语音研究才得以系统比较不同特征和识别算法。今天的端到端网络可以直接接收波形，但采样率、带宽和量化仍决定它实际看到什么。把 16 kHz 音频误当成 8 kHz 播放，会同时改变时长和音高；在文件标签上改一个数字，并没有改变真实采样过程。

另一个容易忽略的问题是声道。立体声中的左右通道可能包含空间线索，两支麦克风的到达时间差也能帮助定位声源。直接取平均可得到单通道，却可能削弱反相成分并丢失空间信息。处理之前应明确任务是否需要这些线索，记录声道顺序和同步方式。对本章的单通道信号，我们只研究时间与频率结构，波形振幅使用统一的相对单位，播放文件还使用共同增益，方便比较处理前后的差别。

## 3. 声谱图让频率随着时间展开

整段傅里叶变换回答“有哪些频率”，却把这些成分出现的先后混在一起。短时傅里叶变换 STFT 先截取一个小窗口，在窗口内分析频率，再把窗口沿时间滑动。结果是一张复数矩阵：一轴是频率，一轴是窗口位置，每个元素同时包含幅值和相位。把幅值或功率映射为颜色，就得到声谱图。上升扫频形成向上倾斜的亮线，下降扫频形成向下倾斜的亮线；若只对时间取平均，两者的频率分布可以很相似，方向信息却被消掉了。

$$
X_{k,m}=\frac{1}{S_w}\sum_{n=0}^{N_w-1}x[n+mH]w[n]e^{-2\pi\mathrm{i}kn/N_w},\qquad S_w=\sum_{n=0}^{N_w-1}w[n],\qquad f_k=\frac{kf_s}{N_w}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0993be952e6f796d152c613.svg) | 输入样本，相对振幅单位；边界使用零填充。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c098f70b11f917194ff6ac69.svg) | Hann 窗权重及其和，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/166403f5e6eb7bbd6158cb63.svg) | 窗口长度与步长，以样本数计，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5657cfd582d156d8f6302a7.svg) | 窗内样本索引、频率格点索引和窗口索引，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f30e943e4d67119e11eb027d.svg) | 虚数单位，平方为 −1；复指数同时记录正弦与余弦投影。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | 第 m 帧第 k 个格点的复数谱，采用窗和归一，具有输入振幅单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/05efcb9156fe14780eed3c07.svg) | 采样率与第 k 格点频率，均为 Hz。 |

先乘窗口，再把这段信号投影到各个振荡基函数，得到局部频率组成。实信号只保留非负频率，所以 256 点窗口产生 129 个格点。8000/256=31.25 Hz 是相邻格点间距，第 16 格点为 500 Hz；H=64 对应每隔 8 ms 分析一次。代码在两端各补半个窗口，因此帧时间标记对应原信号中心；公式中的取样索引理解为补零后的数组。除以窗和使幅值尺度与窗口长度的变化分开。

窗口长度决定观察尺度。8000 Hz 采样下，256 点窗口覆盖 32 ms，频率格点间隔为 31.25 Hz；相邻窗口移动 64 点，对应 8 ms。更长窗口能更细地区分相近频率，但会把短暂变化摊到更长时段。更小步长增加时间上的采样密度，却不会自动缩短窗口本身。零填充可以让频谱曲线画得更密，不等于获得新的频率分辨能力。Hann 窗让边缘逐渐减弱，可减少硬切片造成的频谱泄漏，同时改变主瓣宽度，因此窗函数也参与这种取舍。

$$
D_{k,m}=20\log_{10}\frac{|X_{k,m}|}{A_{\rm ref}},\qquad P_{b,m}=\sum_k B_{b,k}|X_{k,m}|^2,\qquad \operatorname{mel}(f)=2595\log_{10}\left(1+\frac{f}{700\,\mathrm{Hz}}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | 复数 STFT 系数；绝对值为幅值，相对振幅单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/89d8b2e252400f4fafdbec52.svg) | 频率格点、时间帧与 Mel 频带的整数索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6cfa31659fe18d2711f8738c.svg) | 正的参考幅值，与 X 同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2171c3b4ff2a63fc599e89e0.svg) | 相对参考幅值的分贝值，单位 dB。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a1e55881cda008514a87fa9a.svg) | 第 b 个三角滤波器在格点 k 的无量纲权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b9733ff69a26642e8c62ed40.svg) | 频带聚合后的平方幅值，单位为相对振幅的平方。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3fc10fc0b5bd7fa3b82fd22f.svg) | 物理频率 f 以 Hz 计；Mel 是本式采用的 HTK 感知尺度坐标。 |

对数必须作用于无量纲比值，因此幅值先除以同单位参考。幅值比为 1/2 时是约 −6.02 dB，平方幅值比为 1/4 时用 10log₁₀ 也得到相同结果。Mel 频带把附近格点按三角权重汇总；例如两个格点的功率为 4 和 1，权重为 0.5 和 1，则频带值为 3。1000 Hz 对应约 1000 mel。代码将聚合功率设置数值下限后取自然对数作为网络特征，图中的分贝则使用十进对数，两种尺度用途不同。

分贝显示压缩了强弱差异，让较弱的谐波也能被看见，但必须说明参考值。幅值比使用 20 倍对数，功率比使用 10 倍对数；幅值减半约为 −6.02 dB。若每张声谱都各自按最大值归一化，颜色可以比较内部结构，却不能直接比较两段声音的绝对强弱。本章分类样例分别以各自峰值为参考，分离实验则共用一个参考值。两组图的图注和色条保留这一区别，读者可以据此判断哪些比较成立。

Mel 滤波器组进一步把线性频率上的功率汇总到一组感知尺度频带。低频处频带较密，高频处较疏；每个三角滤波器对附近频率加权求和，再取对数，形成常见的 log-Mel 输入。它保留了对语音有用的频谱轮廓，却不是无损表示：频带聚合丢掉细节，功率还丢掉相位。本章明确实现 32 个三角滤波器，连续三角形顶点为 1，在离散频率格点直接取样，不再把离散峰值归一或作面积归一。换用其他软件时，Mel 定义、归一化、窗长和参考值都应一起核对，不能只比较数组形状。

![三个独立测试样例的波形与线性频率声谱。每幅声谱各以自身峰值为 0 dB，窗长 256 点、步长 64 点、采样率 8000 Hz；斜线方向保留了上升与下降的区别。](https://ml-biomat.com/static/tutorials/machine-learning/figures/03ef8e1288fdaef097057029.svg?v=03ef8e1288fd)

图 1三个独立测试样例的波形与线性频率声谱。每幅声谱各以自身峰值为 0 dB，窗长 256 点、步长 64 点、采样率 8000 Hz；斜线方向保留了上升与下降的区别。

## 4. 从一段声音的类别，到事件发生的时间

整段分类可以把一张 log-Mel 声谱送入卷积网络，让局部卷积寻找谐波、频率斜率或短暂爆发，再汇总成类别概率。本章的三个类别是恒定音调、上升扫频和下降扫频。每条录音长 0.6 秒，频率、初相位和噪声各有变化；同一个录音条件组共享一个简单的设备增益与相邻采样响应。训练、验证、测试分别使用不同条件组，防止同一设备特征同时出现在训练和测试中。它模拟的是录音条件变化，而不是把合成条件编号称作真实说话人。

事件检测比分类多了时间定位。假如一段十秒录音里同时有说话和两次门铃，只给“含门铃”标签还不够。模型可以在每个短时帧输出多种事件的概率，再通过阈值、最短持续时间和相邻片段合并得到事件区间。多种声音能够重叠时，应使用独立的多标签输出，而不是强迫每帧只属于一个类别。只有整段标签的弱监督训练，还要解释怎样把局部证据汇总成整段判断；不能把训练时没给出的事件边界当作已有真值。

流式识别又带来延迟要求。一个模型若依赖未来两秒的声谱，在线系统就必须等待两秒才能输出对应判断。因果卷积、有限右侧上下文和分块注意力提供不同的精度与等待时间取舍。评价事件检测时，除了类别正确率，还要报告起止时间容差、漏报、误报和持续时长匹配方式。对警报监测，长时间录音中每小时误报次数可能比整段准确率更接近使用成本。把这些定义放进任务设计，才能知道该优化哪种错误。

## 5. 语音识别的难点，是声音与文字没有逐帧对齐

同一个“你好”，有人说得快，有人拖长最后一个音。训练语音识别时，常有整段录音和转写，却没有每个字精确对应哪几个声学帧的标注。早期隐马尔可夫模型系统把发音拆成状态，用状态转移描述时间延续，再把声学似然、发音词典和语言模型组合起来。这样的分工让对齐成为概率推断的一部分。后来神经网络逐步接替声学建模，端到端方法又进一步学习声音到符号序列的映射；对齐问题并没有消失，而是被写进了新的训练目标。

CTC 在每个输入帧上预测字符或子词，并加入一个特殊空白符。得到一条逐帧路径后，先合并相邻重复符号，再删除空白。例如 A、A、空白、A 会变成 AA；如果先删空白再合并，就会错误地只剩一个 A。训练时不要求选定唯一对齐，而是把所有能折叠成正确转写的路径概率加起来。输出顺序随输入时间单调前进，重复字符需要空白把它们隔开。实际训练用动态规划累加共享前缀，避免逐一枚举指数增长的路径。

$$
p(Y\mid X)=\sum_{\pi:\,\mathcal B(\pi)=Y}\prod_{t=1}^{T}p_t(\pi_t\mid X),\qquad \mathcal L_{\rm CTC}=-\log p(Y\mid X)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a28e27b5a4ff6fb1a8387994.svg) | 输入声学帧序列与目标符号序列；符号序列通常比帧序列短。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4130b90d370e23b5f3efe091.svg) | 声学帧总数与其索引，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4c7b7b1118bfe7ed2694035e.svg) | 包含空白符的逐帧路径，长度为 T；π_t 为该帧符号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bad201494f63e5f5cf85c962.svg) | 先合并连续重复、再删除空白的折叠操作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af9a87107fc3edc86391c888.svg) | 模型在给定完整声学输入后，对第 t 帧符号的概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1ac183623433bd322ce4dd9d.svg) | 转写序列的总概率和负自然对数损失；概率无量纲，损失以 nat 计。 |

路径内部按 CTC 的条件分解相乘，互斥路径再相加。三个帧对 A 的概率依次为 0.6、0.5、0.7，则 AA 只有 A—空白—A 一条路径，概率为 0.6×0.5×0.7=0.21。空序列概率为 0.4×0.5×0.3=0.06，剩余六条路径都得到 A，总概率为 0.73，对应损失 −ln(0.73)≈0.315。输入编码器可以利用时间上下文；帧输出的乘法分解不表示原始声音各帧互不相关。

逐帧挑最大概率的贪心路径，与最可能的完整转写也可能不同。示例只有三个帧和“空白、A”两个符号，所有八条路径都能列出来。逐帧贪心折叠成 AA，但所有折叠成 A 的路径概率之和为 0.73，高于 AA 的 0.21。第二帧有并列最大值，脚本固定选择排序在前的空白，因此贪心规则也完全明确。这个小例子说明，解码不仅是逐格选最大数；束搜索通过保留多个候选前缀，能够近似利用更多序列概率。

![三个帧的符号概率与全部八条路径汇总后的转写概率。第二帧并列时贪心规则取空白，产生 AA；按完整转写概率排序，A 的 0.73 最高。](https://ml-biomat.com/static/tutorials/machine-learning/figures/4888af10bfee2f2b781a897c.svg?v=4888af10bfee)

图 2三个帧的符号概率与全部八条路径汇总后的转写概率。第二帧并列时贪心规则取空白，产生 AA；按完整转写概率排序，A 的 0.73 最高。

## 八条声学路径，三个可能转写

调节三个帧输出 A 的概率，空白概率自动补足为 1。每条路径先合并连续重复，再删除空白。右侧把相同转写的路径概率相加，比较贪心选择与整个序列的选择。每帧并列时，贪心规则选择空白。

[Figure: 八条 CTC 路径和合并后的转写概率](https://ml-biomat.com/tutorials/machine-learning/m20/#M20-svg)

编码器—解码器识别器采用另一种组织方式：编码器把声学序列变成表示，解码器根据已经输出的文字和对声学表示的注意力继续生成。CTC 的帧输出条件分解与自回归解码器的文字历史依赖不同，因此它们在对齐、流式处理和语言约束上有不同特点。Whisper 的原始研究以大量多语种、多个任务的带转写音频训练这类系统，展示了训练数据范围对迁移的影响。使用这类模型时，应分别评价转写、翻译、时间戳和静音片段，避免把不同输出任务混成一个分数。

$$
\mathrm{WER}=\frac{S+D+I}{N_{\rm ref}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1e2e153d47e5fe74ff1b2e08.svg) | 把参考转写变成识别转写所需的最小编辑对齐中的替换、删除、插入词数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/28343a0bbc49a01e2b8450a5.svg) | 参考转写中的词数，正整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/506ac9a8622bbafd87956531.svg) | 词错误率，无量纲；乘 100 可写成百分比，插入很多时可以超过 1。 |

参考为“turn left at next street”，识别为“turn right at the next street”。left 被替换为 right，同时插入 the，参考共 5 个词，所以 WER=(1+0+1)/5=0.4。分母始终使用参考词数，不能为了插入了词就换成识别词数。多个句子的总体 WER 通常先合计编辑数和参考词数再相除，与逐句 WER 的简单平均不同；短句和长句由此具有不同权重。

词错误率 WER 先把参考转写与识别结果进行最小编辑对齐，再统计替换、删除和插入。中文若用字错误率 CER，则要说明分词或按字切分的规则。大小写、标点、数字写法是否归一，也会改变分数。跨说话人切分能测试新说话人的泛化，跨录音环境切分则测试设备和噪声变化；同一长录音切出的相邻片段应留在同一数据划分中。错误分析最好回到具体词句，区分专有名词、口音、噪声和时间截断造成的问题。

## 6. 从文字生成声音：发音、韵律与声码器

语音合成的输入是一段文字，但文字并没有逐项规定声音。多音字怎么读，缩写怎样展开，哪里停顿，哪个词需要重读，都会影响听感。文本前端可以先规范数字与符号，把文字转换为字符或音素，再由声学模型预测持续时长、基频、能量或 Mel 声谱等表示。同一句话的音素可以相同，停顿和重音却改变表达重点。韵律因此不是生成结束后的装饰，而是决定声学序列怎样随时间展开的组成部分。

Tacotron 2 的原始工作把字符到 Mel 声谱的序列预测，与由声谱生成波形的 WaveNet 声码器连接起来。前一部分决定每段声音的声学轮廓和对齐，后一部分补出可播放的细致波形。Mel 功率谱本身没有保存完整相位，不能简单把颜色反过来就还原原声；声码器学习的是满足条件的波形分布。其他合成系统可以显式预测音素时长，或用扩散与流等生成方式形成声学表示，但仍要处理文本、时间与波形之间的对应关系。

HiFi-GAN 则把波形生成与多种判别器结合，其中多周期判别器关注不同周期上的结构。人声的有声段包含重复的准周期模式，仅有平滑的平均频谱未必能保留自然的周期细节。训练中的对抗目标、特征匹配和频谱相关目标各自约束不同方面，生成器再把 Mel 条件上采样为高采样率波形。声码器评价应同时记录音质、速度和输入条件是否与训练一致：同一模型处理真实声谱和前级模型预测的声谱，可能面对不同的误差分布。

听评要给听者稳定的比较条件。短句内容、播放音量、耳机条件和排序会影响判断，随机排列与匿名样本有助于减少顺序偏差。平均意见分 MOS 汇总人的评分，但需要同时说明评分尺度、听者人数、语言经验和样本组成；两篇工作里的 MOS 不一定来自同一道考试。客观频谱距离或可懂度指标可以补充定位问题，却不能完全替代对自然度、发音正确性和韵律的听辨。多说话人系统还应把内容正确、音色相似与韵律控制分别评估。

## 7. 混合声里找目标，也要知道丢掉了什么

一个麦克风接收到的通常是多个声源叠加。降噪倾向于保留目标语音并压低干扰，声源分离则希望输出多个独立来源。若目标与干扰占据不同频带，一个频率掩码就能展示基本机制：把目标频带保留，其余频带压低，再逆变换回波形。本章目标包含 440 Hz 与 880 Hz 两个成分，干扰从 1300 Hz 向更高频移动，因此 1000 Hz 以下的掩码具有明确依据。现实中的两个人声常在同一频带重叠，单靠这个规则就无法分开。

$$
\hat S_{k,m}=M_{k,m}X_{k,m},\qquad \hat s=\operatorname{ISTFT}(\hat S),\qquad \mathrm{SNR}=10\log_{10}\frac{\sum_n s[n]^2}{\sum_n(\hat s[n]-s[n])^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | 混合信号的复数谱，振幅单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/60e1d12d4350594a5b98bbbc.svg) | 频率或时频掩码，无量纲；本例在 1000 Hz 以下为 1，其余为 0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b162864974e72484bd9eaf9d.svg) | 估计目标的复数谱，振幅单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ecbd8a3ba1b2757fa6521b98.svg) | 频率格点、帧和样本索引，均为整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ef3728d51aa7279137439047.svg) | 匹配分析窗与重叠权重的逆短时傅里叶变换。 |
| ![Formula](https://ml-biomat.com/static/agent-math/72e299742b02f1bf993be8a6.svg) | 已知目标与估计波形，振幅单位；需对齐时间和采样率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33105f45313029a217dc86e7.svg) | 目标能量与误差能量比的分贝值，dB。 |

掩码为零的格点被压低，为一的格点保留混合谱系数。逆变换后按窗重叠相加，再除以对应窗平方和，恢复时域信号。目标能量为 100、误差能量为 10 时，SNR 为 10 dB；误差降到 1，则为 20 dB。分子分母具有相同平方振幅单位，取比后无量纲。本例按已知波形计算，既惩罚残留干扰也惩罚目标丢失；它不是带最优缩放的 SI-SDR 指标。

学习型分离模型可以预测时频掩码、复数谱或直接预测时域波形。训练需要说明参考声源怎样得到；如果输出多个声源，而它们的编号没有固定含义，可以在各个输出与参考的排列中选最小损失，避免“正确分开但顺序交换”受到错误惩罚。使用混合信号相位重建的掩码方法较直观，却受相位误差影响；直接预测复数或波形的方法会承担更多重建任务。多麦克风系统还可利用到达时间和空间协方差，将空间滤波与学习表示结合。

音乐也需要适合其结构的表示。固定频率间隔的 STFT 便于信号计算，常数 Q 变换按近似对数频率组织格点，更贴近音程；色度图把不同八度的相同音级汇总，适合某些和声分析，却丢失八度信息。节拍与起音关心能量何时变化，旋律与多音高估计关心哪些基频同时存在。若研究乐器分离，不能只用总体音量误差评价，还要检查其他声部残留、目标声部丢失和新产生的伪影。选择表示时，应保留任务需要的差别。

下面三段音频都长两秒、采样率 8000 Hz，采用共同增益写成 16 位单声道 WAV。第一段是具有平滑包络的双频目标声，第二段叠加扫频干扰与白噪声，第三段保留 1000 Hz 以下频带后重建。先听干扰从哪里出现，再对照声谱中被保留和被压低的区域。共同增益保留了处理前后的振幅关系；比较时可以把播放器音量保持一致，再查看数值指标解释听到的差别。

目标声：440 Hz 与 880 Hz 的合成成分，8000 Hz，2 秒。

目标声音频

混合声：目标声、从 1300 Hz 上升的干扰与白噪声，共用播放增益。

混合声音频

频带估计：保留 1000 Hz 以下的 STFT 系数，再用重叠相加重建。

频带估计音频

![上：0.80–0.84 秒波形局部，共用振幅轴；下：两秒完整声谱，共用分贝参考。目标频率为 440 与 880 Hz，干扰在 1300 Hz 以上；频带掩码同时保留了目标带内噪声。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b394ca90fe458c21abf5da09.svg?v=b394ca90fe45)

图 3上：0.80–0.84 秒波形局部，共用振幅轴；下：两秒完整声谱，共用分贝参考。目标频率为 440 与 880 Hz，干扰在 1300 Hz 以上；频带掩码同时保留了目标带内噪声。

## 8. 完整实验，以及说话人表示的下一步

代码逐项实现采样、Hann 窗 STFT、32 频带 Mel 汇总、卷积分类、频率掩码、逆变换和一个可枚举的 CTC 算例。分类数据按录音条件组划分为 120 条训练、36 条验证、48 条测试。网络有两层小卷积和一个分类头，以验证交叉熵选择检查点；另一条基线先对 log-Mel 沿时间求平均，再训练逻辑回归。两个方法使用相同划分，差别对应一个明确问题：把时间顺序丢掉之后，是否还能可靠判断扫频方向？

### 从波形到分类、分离与 CTC 概率

只生成短合成音频，不下载模型权重。代码保存可试听 WAV、全部数值、四组双语图和 summary.json，CPU 使用两线程。

```
"""Generated audio: time-frequency analysis, classification, masks, and exact CTC."""
import argparse,copy,itertools,json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
FS=8000;NFFT=256;HOP=64;DURATION=.6

def stft(x,nfft=NFFT,hop=HOP):
    window=np.hanning(nfft+1)[:-1]
    padded=np.pad(x,(nfft//2,nfft//2+(-len(x))%hop))
    frames=np.lib.stride_tricks.sliding_window_view(padded,nfft)[::hop]
    return np.fft.rfft(frames*window,axis=1).T/window.sum()

def istft(z,length,nfft=NFFT,hop=HOP):
    window=np.hanning(nfft+1)[:-1];frames=np.fft.irfft(z.T,n=nfft,axis=1)*window.sum()
    out=np.zeros((len(frames)-1)*hop+nfft);weight=np.zeros_like(out)
    for i,frame in enumerate(frames):
        out[i*hop:i*hop+nfft]+=frame*window;weight[i*hop:i*hop+nfft]+=window**2
    out=np.divide(out,weight,out=np.zeros_like(out),where=weight>1e-12)
    return out[nfft//2:nfft//2+length]

def mel_filters(count=32):
    hz=np.fft.rfftfreq(NFFT,1/FS)
    mel=lambda x:2595*np.log10(1+x/700)
    points=700*(10**(np.linspace(mel(0),mel(FS/2),count+2)/2595)-1)
    filters=[]
    for left,mid,right in zip(points[:-2],points[1:-1],points[2:]):
        filters.append(np.maximum(0,np.minimum((hz-left)/(mid-left),(right-hz)/(right-mid))))
    return np.array(filters),points[1:-1]

BANK,CENTERS=mel_filters()
def feature(x):return np.log(np.maximum(BANK@abs(stft(x))**2,1e-8)).astype(np.float32)

def dataset(groups,snr=None):
    signals=[];labels=[];groupids=[]
    time=np.arange(int(FS*DURATION))/FS
    for group in groups:
        profile=np.random.default_rng(2000+group);echo=profile.uniform(-.25,.25);gain=profile.uniform(.7,1.3)
        for label in range(3):
            for repeat in range(4):
                rng=np.random.default_rng(10000+group*100+label*10+repeat)
                low=rng.uniform(300,600);high=rng.uniform(1200,1700);phase=rng.uniform(0,2*np.pi)
                if label==0:f0=f1=rng.uniform(650,950)
                elif label==1:f0,f1=low,high
                else:f0,f1=high,low
                phase_t=2*np.pi*(f0*time+(f1-f0)/(2*DURATION)*time**2)+phase
                clean=np.sin(phase_t)*np.sin(np.pi*time/DURATION)**2
                clean=gain*(clean+echo*np.r_[0,clean[:-1]])
                level=rng.uniform(5,25) if snr is None else snr
                noise=np.random.default_rng(90000+group*100+label*10+repeat).normal(size=len(clean))
                noise*=np.sqrt(np.mean(clean**2)/(10**(level/10)*np.mean(noise**2)))
                signals.append(clean+noise);labels.append(label);groupids.append(group)
    return np.array(signals),np.array(labels),np.array(groupids)

class AudioCNN(nn.Module):
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d((4,4)),nn.Flatten(),nn.Linear(256,3))
    def forward(self,x):return self.net(x)

def collapse(path):
    return ''.join(c for i,c in enumerate(path) if c!='_' and (i==0 or c!=path[i-1]))

def edit_distance(ref,hyp):
    d=np.zeros((len(ref)+1,len(hyp)+1),int);d[:,0]=np.arange(len(ref)+1);d[0,:]=np.arange(len(hyp)+1)
    for i in range(1,len(ref)+1):
        for j in range(1,len(hyp)+1):d[i,j]=min(d[i-1,j]+1,d[i,j-1]+1,d[i-1,j-1]+(ref[i-1]!=hyp[j-1]))
    return int(d[-1,-1])

def run(out,language):
    out.mkdir(parents=True,exist_ok=True);zh=language=='zh';text=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
    save=lambda fig,name:(fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight'),fig.savefig(out/f'{name}-{language}.png',dpi=140,bbox_inches='tight'),plt.close(fig))
    waves,y,g=dataset(range(17));features=np.array([feature(w) for w in waves]);train=g<10;valid=(g>=10)&(g<13);test=g>=13
    mean=features[train].mean();std=features[train].std();inputs=torch.tensor((features-mean)/std)[:,None];targets=torch.tensor(y)
    torch.manual_seed(20);model=AudioCNN();optimizer=torch.optim.Adam(model.parameters(),lr=.002);trace=[];best=float('inf');selected=0
    trainids=np.flatnonzero(train)
    for epoch in range(35):
        model.train();order=torch.randperm(len(trainids));total=0
        for ids in order.split(24):
            ix=trainids[ids.numpy()];optimizer.zero_grad();loss=nn.functional.cross_entropy(model(inputs[ix]),targets[ix]);loss.backward();optimizer.step();total+=loss.item()*len(ix)
        model.eval()
        with torch.no_grad():vl=nn.functional.cross_entropy(model(inputs[valid]),targets[valid]).item()
        trace.append((total/train.sum(),vl))
        if vl<best:best=vl;weights=copy.deepcopy(model.state_dict());selected=epoch+1
    model.load_state_dict(weights);model.eval()
    torch.save({'model':model.state_dict(),'mean':float(mean),'std':float(std)},out/'audio-model.pt')
    (out/'model.json').write_text(json.dumps({'class':'AudioCNN','classes':['steady','rising','falling'],'sample_rate_hz':FS,'window_samples':NFFT,'hop_samples':HOP,'mel_filters':32,'selected_epoch':selected,'mean':float(mean),'std':float(std)},indent=2),encoding='utf-8')
    saved=torch.load(out/'audio-model.pt',weights_only=True);reloaded=AudioCNN();reloaded.load_state_dict(saved['model']);reloaded.eval()
    restored_inputs=torch.tensor((features[test]-saved['mean'])/saved['std'])[:,None]
    with torch.no_grad():reload_error=float((model(inputs[test])-reloaded(restored_inputs)).abs().max())
    with torch.no_grad():prob=model(inputs[test]).softmax(1).numpy()
    pred=prob.argmax(1);cm=confusion_matrix(y[test],pred,labels=range(3))
    baseline=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000));baseline.fit(features[train].mean(2),y[train]);baseline_accuracy=float(baseline.score(features[test].mean(2),y[test]))
    levels=[20,5,-5];noise_acc=[]
    for level in levels:
        ww,yy,_=dataset(range(13,17),level);ff=np.array([feature(w) for w in ww]);xx=torch.tensor((ff-mean)/std)[:,None]
        with torch.no_grad():pp=model(xx).argmax(1).numpy()
        noise_acc.append(float(np.mean(pp==yy)))
    t=np.arange(2*FS)/FS;envelope=np.sin(np.pi*t/2)**2
    clean=envelope*(.65*np.sin(2*np.pi*440*t)+.2*np.sin(2*np.pi*880*t));interference=.65*envelope*np.sin(2*np.pi*(1300*t+250*t*t))
    noise=np.random.default_rng(77).normal(0,.12,len(t));mixture=clean+interference+noise
    z=stft(mixture);freq=np.fft.rfftfreq(NFFT,1/FS);mask=(freq<=1000).astype(float)[:,None]
    estimate=istft(z*mask,len(t));reconstructed=istft(z,len(t));reconstruction_error=float(abs(reconstructed-mixture).max())
    snr=lambda estimate:float(10*np.log10(np.sum(clean**2)/np.sum((estimate-clean)**2)))
    shared_gain=.85/max(np.max(abs(x)) for x in [clean,mixture,estimate])
    for name,w in [('clean',clean),('mixture',mixture),('filtered',estimate)]:wavfile.write(out/(name+'.wav'),FS,np.int16(np.clip(w*shared_gain,-1,1)*32767))
    ctc_prob=np.array([[.4,.6],[.5,.5],[.3,.7]]);sequences={}
    for path in itertools.product(range(2),repeat=3):
        output=collapse(''.join('_A'[k] for k in path));p=float(np.prod([ctc_prob[i,k] for i,k in enumerate(path)]));sequences[output]=sequences.get(output,0)+p
    greedy=collapse(''.join('_A'[k] for k in ctc_prob.argmax(1)))
    ref='turn left at next street'.split();hyp='turn right at the next street'.split();ed=edit_distance(ref,hyp)
    summary={'sample_rate_hz':FS,'window_samples':NFFT,'hop_samples':HOP,'frequency_bin_hz':FS/NFFT,'split_clips':[int(train.sum()),int(valid.sum()),int(test.sum())],'group_overlap':len(set(g[train])&set(g[test])),'selected_epoch':selected,'cnn_test_accuracy':float(np.mean(pred==y[test])),'time_averaged_baseline_accuracy':baseline_accuracy,'confusion_matrix':cm.tolist(),'noise_levels_db':levels,'noise_accuracy':noise_acc,'stft_reconstruction_max_error':reconstruction_error,'input_snr_db':snr(mixture),'filtered_snr_db':snr(estimate),'ctc_sequence_probabilities':sequences,'ctc_greedy_output':greedy,'wer_edit_distance':ed,'wer_reference_words':len(ref),'wer':ed/len(ref),'audio_duration_seconds':len(t)/FS,'audio_shared_gain':float(shared_gain)}
    summary['reload_logits_error']=reload_error
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez_compressed(out/'data.npz',waveforms=waves,labels=y,groups=g,features=features,probabilities=prob,trace=trace,clean=clean,mixture=mixture,estimate=estimate,ctc_prob=ctc_prob)
    assert reconstruction_error<1e-10;assert abs(sum(sequences.values())-1)<1e-12;assert abs(sequences['AA']-.21)<1e-12;assert ed==2
    names=[text('恒定音调','Steady tone'),text('上升扫频','Rising sweep'),text('下降扫频','Falling sweep')]
    fig,axs=plt.subplots(2,3,figsize=(12,5.6),gridspec_kw={'height_ratios':[.7,1.4]},layout='constrained')
    for c in range(3):
        idx=np.flatnonzero((y==c)&test)[0];wave=waves[idx];spec=stft(wave);db=20*np.log10(np.maximum(abs(spec),1e-8)/np.max(abs(spec)))
        axs[0,c].plot(np.arange(len(wave))/FS,wave,lw=.35,color='#4d6575');axs[0,c].set(title=names[c],xlabel=text('时间 / s','Time / s'),ylabel=text('振幅','Amplitude'))
        im=axs[1,c].pcolormesh(np.arange(spec.shape[1])*HOP/FS,freq,db,cmap='magma',vmin=-65,vmax=0,shading='auto',rasterized=True);axs[1,c].set(ylim=(0,2500),xlabel=text('时间 / s','Time / s'),ylabel=text('频率 / Hz','Frequency / Hz'))
    fig.colorbar(im,ax=axs[1,:],label=text('相对峰值 / dB','Relative to each peak / dB'));save(fig,'representations')
    fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained');tr=np.array(trace)
    axs[0].plot(np.arange(1,36),tr[:,0],label=text('训练','Train'),color='#176b91');axs[0].plot(np.arange(1,36),tr[:,1],label=text('验证','Validation'),color='#bc5549');axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('交叉熵','Cross entropy'));axs[0].legend()
    im=axs[1].imshow(cm,cmap='Blues',vmin=0,vmax=16);axs[1].set(xticks=range(3),yticks=range(3),xticklabels=names,yticklabels=names,xlabel=text('预测类别','Predicted'),ylabel=text('实际类别','True'));axs[1].tick_params(axis='x',labelrotation=25)
    for i in range(3):
        for j in range(3):axs[1].text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if cm[i,j]>8 else '#18384d')
    axs[2].plot(levels,noise_acc,'o-',color='#176b91');axs[2].axhline(1/3,color='#8e9ba3',ls='--',label=text('随机机会 1/3','Chance 1/3'));axs[2].set(xticks=levels,ylim=(0,1.05),xlabel=text('输入信噪比 / dB','Input SNR / dB'),ylabel=text('正确率','Accuracy'));axs[2].legend();save(fig,'classification')
    fig,axs=plt.subplots(2,3,figsize=(12,5.8),layout='constrained');refamp=max(abs(stft(w)).max() for w in [clean,mixture,estimate])
    for j,(name,w)in enumerate([(text('目标声','Target'),clean),(text('混合声','Mixture'),mixture),(text('频带估计','Band estimate'),estimate)]):
        segment=(t>=.8)&(t<.84)
        axs[0,j].plot(t[segment],w[segment],lw=.8,color=['#176b91','#8c6e99','#2b897a'][j]);axs[0,j].set(title=name,xlabel=text('时间 / s','Time / s'),ylabel=text('振幅','Amplitude'),ylim=(-1.5,1.5))
        zz=stft(w);im=axs[1,j].pcolormesh(np.arange(zz.shape[1])*HOP/FS,freq,20*np.log10(np.maximum(abs(zz),1e-8)/refamp),vmin=-65,vmax=0,cmap='magma',shading='auto',rasterized=True);axs[1,j].set(xlabel=text('时间 / s','Time / s'),ylabel=text('频率 / Hz','Frequency / Hz'),ylim=(0,2500))
    fig.colorbar(im,ax=axs[1,:],label=text('共享参考 / dB','Shared reference / dB'));save(fig,'separation')
    fig,axs=plt.subplots(1,2,figsize=(10,3.2),layout='constrained');im=axs[0].imshow(ctc_prob.T,cmap='Blues',vmin=0,vmax=1,aspect='auto')
    axs[0].set(xticks=range(3),xticklabels=[1,2,3],yticks=[0,1],yticklabels=[text('空白','Blank'),'A'],xlabel=text('声学帧','Acoustic frame'),title=text('每帧输出概率','Frame probabilities'))
    for i in range(3):
        for j in range(2):axs[0].text(i,j,f'{ctc_prob[i,j]:.1f}',ha='center',va='center',color='white' if ctc_prob[i,j]>.55 else '#18384d')
    axs[1].bar([text('空序列','Empty'),'A','AA'],[sequences[''],sequences['A'],sequences['AA']],color=['#9daab1','#176b91','#bf7444']);axs[1].set(ylim=(0,1),ylabel=text('所有路径求和后的概率','Probability summed over paths'),title=text('最可能的路径不等于最可能的转写','Best path differs from best transcript'));save(fig,'ctc')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

audio-model.pt保存所选CNN权重及训练集的均值、标准差，model.json记录采样和特征设置。用保存的归一化参数处理测试特征，重新建立AudioCNN加载权重后，logit最大差为0；这让后续推理沿用训练时相同的输入尺度。

固定随机种子的这次运行中，卷积网络在 48 条测试录音上全部分类正确，时间平均基线正确率为 0.6875。保持测试信号生成参数不变，分别以 20、5 和 −5 dB 信噪比加入噪声，网络正确率为 1.0、1.0 和 0.3333。较低噪声下的高分与强噪声下的下降应一起阅读：训练噪声范围为 5–25 dB，−5 dB 已经改变了输入条件。这个受控实验让我们直接看到模型依赖的声谱线条何时被噪声淹没。

![左：实际训练与验证交叉熵；中：48 条独立条件组测试样例的计数混淆矩阵；右：相同测试信号参数下改变加噪信噪比的正确率。虚线是三类均衡任务的随机机会水平。](https://ml-biomat.com/static/tutorials/machine-learning/figures/eb77389ef8e9332c2babda5b.svg?v=eb77389ef8e9)

图 4左：实际训练与验证交叉熵；中：48 条独立条件组测试样例的计数混淆矩阵；右：相同测试信号参数下改变加噪信噪比的正确率。虚线是三类均衡任务的随机机会水平。

分离实验的输入信噪比约为 −0.329 dB，频带估计后约为 13.869 dB。该数值使用已知目标波形作为参考，按逐样本误差能量计算；它回答这个频带分离算例里目标恢复到什么程度。STFT 不加掩码后逆变换的最大误差约为 6.66×10⁻¹⁶，说明窗口与重叠重建衔接正确。脚本还验证 CTC 所有输出概率之和为 1，并计算一个含一次替换和一次插入的转写例子，其 WER 为 2/5=0.4。

进一步处理真实语音时，自监督表示可以利用大量没有转写的录音。wav2vec 2.0 在潜在声学表示中遮蔽片段，再通过对比任务学习恢复相应的量化目标，之后用带转写样本适配语音识别。说话人表示则强调同一个人在不同句子中的稳定特征，可以用嵌入距离做验证，或把一段长录音中的片段聚类。说话人识别问“这个人是谁”，说话人验证问“是否同一个人”，分段还要恢复发言时间并处理重叠语音；三者的标签和错误统计不同。

说话人分段常把语音活动检测、局部嵌入提取、聚类和时间边界修正连接起来。评价时需要说明是否计入重叠说话、边界周围是否允许时间容差，以及漏检语音、误检语音和说话人混淆分别有多少。按人划分数据、按录音来源去重，再保存采样率、前处理和模型版本，能让这些结果真正对应新的声音条件。至此，波形、声谱、文字和身份表示已经连接起来；选择下一种模型时，先问它保留了什么信息，又需要怎样的参考答案，任务就会清楚得多。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M20.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [librosa — Using display.specshow](https://librosa.org/doc-playground/main/auto_examples/plot_display.html)

   时间、频率和分贝参考的可视化讲解。
2. [SciPy STFT documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html)

   窗、边界、幅值尺度与逆变换条件。
3. [Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)

   CTC 原始论文：对齐求和与训练目标。
4. [Sequence Modeling With CTC](https://distill.pub/2017/ctc/)

   CTC 折叠、动态规划与解码的开放图解。
5. [SpeechBrain — Speech Recognition From Scratch](https://speechbrain.readthedocs.io/en/latest/tutorials/tasks/speech-recognition-from-scratch.html)

   从声学输入到编码解码、束搜索的开源训练流程。
6. [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)

   Whisper 的原始多语种、多任务研究。
7. [Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions](https://arxiv.org/abs/1712.05884)

   Tacotron 2 的声学表示与声码器分工。
8. [HiFi-GAN](https://arxiv.org/abs/2010.05646)

   波形生成与周期结构的原始研究。
9. [wav2vec 2.0](https://arxiv.org/abs/2006.11477)

   遮蔽潜在表示与对比预训练。
