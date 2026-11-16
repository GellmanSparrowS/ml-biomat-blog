# 从动作价值到策略更新：深度强化学习

Source: https://ml-biomat.com/tutorials/machine-learning/m37/
Language: zh-CN

在同一个随机走廊中运行DQN与PPO，理解回放、优势、裁剪和连续控制。

## 1. 当状态多到放不进一张表

送货车在路口选择方向，恒温设备调整功率，游戏角色决定下一步移动，这些任务都要考虑动作之后还会发生什么。上一章可以把每个状态与动作的价值写进表格；如果状态换成摄像头画面、关节角度或一长串传感器读数，逐格存储就变得困难。深度强化学习用神经网络把观测映射成价值或动作分布，让相似情形共享计算。但网络也把许多预测联系起来：修正一个状态的价值，可能改变其他状态，因此训练数据、目标值和更新幅度需要一起设计。

本章使用一条七格走廊。快递员从一至五格随机出发，目标随机在零或六格；走到另一个端点算失败。每次选择向左或向右，环境有百分之十概率把动作翻转，最多行动二十步。抵达目标奖励一，错误端点奖励负一，普通移动奖励负零点零二。输入包含位置、目标与剩余时间，分别回答“我在哪里”“要去哪里”和“还来得及走多久”。这个小任务能把学习过程完全展开，也能通过已知转移规则精确计算基线。

价值学习先估计每个动作未来的回报，再选择较好的动作；策略学习直接输出动作的概率，并用经历过的回报调整它；Actor–Critic 同时学习行动者和评价者。OpenAI 的二〇一八年教学图适合定位这些选择，但一棵分类树无法表现所有交叉关系：PPO 也有价值网络，SAC 同时使用随机策略与离策略数据，模型式方法还能把规划与策略训练结合。理解每个模块学什么、数据从哪里来，比记忆一个算法名字所在的树枝更有用。

![强化学习方法的历史教学分类图](https://ml-biomat.com/static/tutorials/machine-learning/figures/5c9c021ec1436eb5c55aaa9b.svg?v=5c9c021ec143)

图 1OpenAI《Spinning Up》2018教学关系图，原图保留英文。以学习策略、价值或模型理解算法；本章补充这些模块的交叉组合。原页：https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html；MIT许可：https://raw.githubusercontent.com/openai/spinningup/master/LICENSE。

## 2. DQN：让网络学习动作价值

DQN 的输入是一份状态表示，输出是每个离散动作的价值。本例输入十个数，输出向左和向右两个数；输出较大者是当前贪心选择。Mnih 等人在二〇一三年的 Atari 工作中将图像表示学习与 Q-learning 联系起来，让卷积网络从画面估计未来奖励。这里改用小型全连接网络，把计算重点放在目标构造和数据组织上：一次观察到的奖励，加上下一状态的估计价值，组成当前动作的学习目标。

$$
y_i=r_i+\gamma(1-d_i)\max_{a'}Q_{\bar\theta}(s'_i,a'),\quad\mathcal L=\frac1B\sum_{i=1}^{B}\ell(Q_\theta(s_i,a_i)-y_i),\quad\ell(e)=\begin{cases}e^2/2&|e|\le1\\|e|-1/2&|e|>1\end{cases}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/91ddd31201411affadf62bd0.svg) | 第i条转移的状态、执行动作、奖励、下一状态与终止标记。d为0或1；本例奖励为无量纲任务分。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0d9eb9fa4d1c85e9b3562044.svg) | 小批次样本数、样本索引与下一状态候选动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/25466d762a2d1f840409be64.svg) | 在线网络与目标网络参数；目标计算停止梯度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 动作价值；本例网络输入10维、输出2维，按动作选出标量，与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/05fe78b5b68e2122cf068260.svg) | 折扣系数与目标值；代码γ=0.97，目标与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b50fd96b3413648e1f224a9f.svg) | 平均回归损失、阈值为1的Huber型损失与预测减目标的误差；这里全部任务量无量纲。 |

目标把眼前奖励与尚未结束时的未来价值相加，网络只更新本条记录实际动作对应的输出。假设奖励1、γ=0.9、下一状态最大值2、尚未终止，则目标2.8；当前预测2，误差−0.8，损失0.32。若真正终止，目标改为1，不接下一状态的价值。分段损失在小误差附近像平方损失，大误差时斜率不再随误差绝对值增长。

如果预测和目标都由正在快速变化的同一个网络产生，更新会追逐一个不断移动的参照。目标网络保存一份较慢更新的参数，计算目标时停止梯度；本例每一百二十八次环境交互复制一次在线网络。经验回放则保存状态、动作、奖励、下一状态和是否真正结束，再随机抽取小批次，减少相邻轨迹样本的强相关，并重复利用已经付出交互成本的数据。这两项设计处理不同问题：一个减缓目标漂移，一个改变训练样本的时间组织。

回放池中的动作可能来自较早的探索策略，Q-learning 的目标却使用下一状态的最大价值，因此属于离策略学习。它不要求记录中的每个动作都是当前最优选择，但数据仍应覆盖需要学习的状态和动作。过小的回放池容易遗忘，过旧的数据也可能跟不上变化的环境。优先回放可以更常抽取大误差样本，但抽样分布随之改变，需要相应的重要性权重与覆盖检查；简单的均匀回放是理解这些取舍的清楚起点。

结束标记直接决定是否保留未来价值。本例的二十步是任务本身的截止时间，输入中包含剩余步数，因此到时是真正终止，后续价值为零。若只是训练程序为了收集固定长度数据而截断轨迹，环境本身还能继续，就应使用末状态价值续接，而不是把它当成死亡。PPO 的三十二步采样窗口会跨越若干个回合，也可能在一个未结束回合中停止；代码保留每步的下一状态价值，正是为区分这两种情况。

## 3. Double 与 Dueling 分别改变了哪里

从一组带误差的估计中挑最大值，容易把正误差也挑出来。假设所有动作真实价值都是零，但估计各有独立的零均值噪声，单个估计平均仍是零，最大值的平均却会大于零。动作越多，可被选中的偶然高值也越多。Double DQN 将“挑哪个动作”和“给这个动作打多少分”分开：在线网络选动作，目标网络评价该动作。两者并非完全独立，因此它减少哪一部分偏差取决于误差的相关结构，并不会让所有估计自动变成精确值。

$$
a^*=\arg\max_a Q_\theta(s',a),\qquad y_{\rm Double}=r+\gamma(1-d)Q_{\bar\theta}(s',a^*)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/65d5791718d5cb558a50141f.svg) | 下一状态、候选动作与在线网络选出的动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6141b2d51d1b502b926964cf.svg) | 在线与目标动作价值网络及参数；各输出一个动作对应的标量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/57afd3dd2741fa5223bfcb35.svg) | 当前奖励、折扣、真正终止标记与Double目标；奖励/目标使用相同的无量纲任务尺度。 |

在线网络负责选，目标网络负责评价。下一状态在线输出(4,3)、目标输出(2,5)，在线会选第一个动作，目标给它2分。奖励1、γ=0.9时，Double目标为2.8；普通DQN直接取目标网络最大值5，得到5.5。目标网络对另一个动作给了更高值，并不会改变Double本次已经选定的动作。

图中的五万次噪声算例专门展示选择效应：两个候选时，同一组估计取最大值的均值约零点五六八；二十个候选时约一点八六五。用独立第二组噪声评价所选动作，均值则接近零。这是一个可重复的统计机制实验，独立性是它的设定；实际 Double DQN 的两个网络共享训练历史，应通过真实环境回报与价值误差判断效果。二〇一五年的 Double DQN 工作正是把表格方法中的这种分工推广到深度价值网络。

Dueling 改变的是网络输出结构。它把“当前状态整体有多好”和“某个动作相对其他动作有多好”分成两个分支，再组合成动作价值。比如车已处在畅通道路上，整体前景不错，而稍向左或稍向右的差别很小；共享状态价值可以减少每个动作都重新学习同一事实的负担。为了让分解有明确约定，常从优势分支中减去各动作的平均值。Dueling 可以与 Double DQN 同时使用，一个改变目标选择，一个改变表示结构。

$$
Q(s,a)=V(s)+A(s,a)-\frac1m\sum_{j=1}^{m}A(s,a_j)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/09e33249fb2a44b3a16b695b.svg) | 状态、查询动作与第j个离散动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f441d5a733f02391d4cb1a7.svg) | 状态分支输出的一个标量，与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/07378df13b4f41d9096644ef.svg) | 优势分支对动作a的输出；完整分支有m个数，与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5d562bcaafa96061616f6969.svg) | 动作数、动作索引与组合动作价值；本例m=2，各任务量无量纲。 |

减去动作平均值后，优势分支只表达相对差别，V承担该状态各动作价值的均值。V=2、优势为(−1,1)时，Q=(1,3)。若给两个优势同时加5，得到(4,6)，平均值也增加5，因此Q仍为(1,3)。这消除了同一常数在两个分支间任意搬移的一种不明确性，且不改变贪心动作选择。

## 4. 直接调整动作概率：REINFORCE 与基线

策略网络不一定先给动作估值，也可以直接输出概率。对左右两个动作，它先输出两个 logits，再用 softmax 转成总和为一的概率，按这个分布采样动作。一次回合得到好结果，就增加其中有益动作出现的可能；得到差结果，则向相反方向更新。REINFORCE 通过“动作的对数概率梯度乘回报”把这一直觉写成可计算形式。它不需要对环境求导：道路如何翻转动作、游戏怎样产生奖励，可以当作可采样的外部过程。

$$
\nabla_\theta J=\mathbb E_{\tau\sim\pi_\theta}\!\left[\sum_{t=0}^{T-1}\nabla_\theta\log\pi_\theta(a_t\mid s_t)\big(G_t-b(s_t)\big)\right],\qquad G_t=\sum_{k=t}^{T-1}r_k
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8f5ed8b1adff646d1cbe95e.svg) | 策略参数、有限回合未折扣期望回报与参数梯度；回报采用无量纲任务分。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d530b1794a9754a597787ed8.svg) | 策略动作概率、按当前策略采样的完整轨迹与期望。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7ea051e99f790acbb94bb2ce.svg) | 当前步、未来步、回合长度、状态、动作与第k步奖励。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d5033980c206f50bdff43e45.svg) | 当前步开始的实际未折扣回报与只依赖状态的基线；二者同尺度，策略更新时视为固定权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c6218d94f5cfc1cfe45060d.svg) | 自然对数；动作概率无量纲。 |

轨迹概率中的环境转移不依赖策略参数，对数将各步策略概率的乘积变成求和；过去奖励对当前采样动作的期望贡献可去掉，留下未来回报。本式采用未折扣有限回合以突出推导；后面的GAE使用明确给定的折扣。二动作策略用一个logit表示向右概率0.25，实际采样向右时，该动作对数概率对logit的导数为1−0.25=0.75。优势为2，则这条样本提供1.5的梯度上升信号。

整段回报有很大随机性。一次正确转向可能恰好被环境翻转而失败，错误动作也可能碰巧接近目标，因此单条经历的评价容易摇摆。基线衡量在同一状态通常能取得多少回报，动作得到的回报减去基线，就是相对表现。基线若只依赖状态、不依赖本次采样动作，其期望梯度贡献为零：所有动作概率的总和始终是一，对这个总和求导得到零。这个性质允许减少估计方差，同时保留期望更新方向。

例如某状态通常得到三分，一次动作后得到五分，它的相对信号是正二；若得到一分则为负二。即便两个原始回报都为正，后者仍可提示减少该动作概率。基线常由一个价值网络学习，也可以用简单平均作入门对照。训练策略时应将回报或优势视为固定权重，停止穿过它们的梯度；否则优化目标会额外推动评价器去改变分数，而不是只改变动作概率。完整代码中的 PPO 同样保留了这一分工。

## 5. Actor–Critic 与 GAE：在等待回报和及时更新之间

Actor 负责动作分布，Critic 估计状态价值。两者可以拥有独立网络，也可以共享特征提取层、分别输出策略与价值。本例共享两个三十二维隐藏层，上面接两个动作 logits 和一个价值标量。Critic 用经历得到的目标训练，Actor 用相对价值信号调整概率。A2C 通常从多个环境同步收集短轨迹，再合并更新；同步描述数据与参数更新的组织方式，并不意味着每个环境经历相同的状态。

等完整回合结束再计算回报，能利用实际奖励，却可能需要等待很久；只看一步 TD 误差更新更及时，却更依赖当前价值估计。GAE 将之后的一串 TD 误差按几何权重累加，让参数 λ 控制传播距离。较小 λ 更重视附近的误差，较大 λ 让较远奖励影响前面的动作。二〇一五年的 GAE 工作把这种优势估计与策略优化联系起来，使价值网络承担减少梯度噪声的角色，而不只是输出一个额外统计量。

$$
\delta_t=r_t+\gamma(1-d_t)V(s_{t+1})-V(s_t),\qquad\hat A_t=\delta_t+\gamma\lambda(1-d_t)\hat A_{t+1},\qquad\hat A_T=0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | 当前转移索引与采样窗口长度；从T−1向0递推。 |
| ![Formula](https://ml-biomat.com/static/agent-math/053bcaf18fe5f8c8317c15a6.svg) | 当前/下一状态、奖励与真正终止标记，终止为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5a9105ba2001ee110accdf47.svg) | 采样时的状态价值、TD误差与GAE优势，均与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2b94ab8bc94736dd0f6657df.svg) | 折扣与优势传播系数，通常在0至1；代码分别0.97和0.95。 |

一步误差衡量奖励加续接价值相对当前估计的差，再把下一步优势折减后向前传。奖励(0,0,1)、V=(0.2,0.3,0.4)、终止在最后，γ=0.9、λ=0.8，得到δ=(0.07,0.06,0.6)，优势(0.42424,0.492,0.6)。窗口末尾的优势设为零，不意味着末状态价值为零；未终止时，最后一个δ仍包括下一状态V。真正终止则通过d同时切断价值与后续优势。

三步算例的奖励是零、零、一，三个状态价值是零点二、零点三、零点四，最后真正终止。取折扣零点九、λ 为零点八，TD 误差分别为零点零七、零点零六、零点六；从后往前累加得到优势零点六、零点四九二和零点四二四二四。终点奖励因此能影响之前动作，同时价值估计又提供了局部修正。代码将优势加回旧价值作为价值回归目标，并把策略使用的优势按整批均值与标准差归一化。

归一化改善数值尺度，却也改变同一有限批次中不同样本的相对权重，因此应记录具体做法。若在每个很小的小批次独立归一化，和在整个采样批次统一归一化，训练过程可能不同。批次边界同样重要：真正终止处切断后续优势，不能把重置后的新回合奖励加回旧回合；采样窗口结束但回合还在继续时，则使用末状态价值。把这些索引画成时间顺序，往往比仅背下 GAE 公式更能避免实现错误。

## 6. PPO 为什么限制一个动作概率变化的收益

一次采样给出的优势只反映旧策略附近的经历。如果拿同一批数据反复大幅更新，策略可能已经走到这些样本无法代表的位置。TRPO 用新旧策略之间的平均 KL 距离约束更新幅度，并借助局部近似求解；PPO 则提供更便于一阶优化的做法。二〇一七年的 PPO-Clip 使用新旧动作概率之比，在代理目标中削去继续向某一方向过度变化的收益，从而支持对一批新轨迹进行多轮小批次更新。

$$
\rho_i(\theta)=\frac{\pi_\theta(a_i\mid s_i)}{\pi_{\rm old}(a_i\mid s_i)},\qquad L_{\rm clip}=\frac1B\sum_{i=1}^{B}\min\!\left(\rho_i\hat A_i,\operatorname{clip}(\rho_i,1-\epsilon,1+\epsilon)\hat A_i\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8bd9750df1a9d94604e32c16.svg) | 采样记录索引、批次大小、采样状态和实际动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fa5000290880458fe08d11fc.svg) | 当前策略、采样时固定的旧策略与当前参数；概率都对应同一记录动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b7986769e3dcf2f5576a7fd9.svg) | 新旧概率比与裁剪宽度，均无量纲；代码ε=0.2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9f0b4490f9c43d63aee296ca.svg) | 固定优势估计；代码按整个采样批次归一化后无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d9944c7c9378cf7deef406a6.svg) | 待最大化的代理目标、区间截断和取两项较小值；代码最小化其负值。 |

比值衡量同一动作概率相对采样时变化多少。优势2、ρ=1.5、ε=.2时，取min(3,2.4)=2.4；优势−2、ρ=.5时，取min(−1,−1.6)=−1.6。若优势为正但ρ低于下界，目标仍继续惩罚概率减小；若优势为负且ρ高于上界，也继续惩罚变坏，因此不能只把ρ裁剪后直接乘优势。裁剪的是这条样本的优化激励，不是所有网络输出的硬约束。

优势为正二、旧动作概率为零点四、新概率为零点六时，概率比是一点五。若裁剪宽度为零点二，未裁剪贡献为三，裁剪后的贡献为二点四，目标取较小者，因此不再奖励继续把这一动作概率推高。优势为负二、概率比为零点五时，目标取负一点六，而不是负一；这限制了“过度降低一个差动作概率”带来的额外收益。正负优势的两边不同，交互把它们放在同一坐标中，可以直接查看取最小值后哪一段变平。

裁剪发生在优化目标中，并不会把网络真正输出的所有概率比硬性锁在区间里。共享参数还会同时改变其他动作和状态，因此更新后仍要检查 KL、裁剪比例、策略熵与评价回报。KL 过大时可以提前结束当前批次更新；熵快速降到很低，则提示策略正在接近确定选择。它们是诊断量，与最终任务回报各有用途。本例记录采样动作上的平均旧对数概率减新对数概率，作为有限样本 KL 估计；数值可能因采样而略为负。

PPO 的策略仍主要依据当前策略新采集的轨迹更新。保存一批旧概率、做四轮更新，与从任意久以前的回放池持续抽样不同。代码在每轮收集十六个环境各三十二步，共五百一十二条转移，固定旧动作对数概率与优势，再分成一百二十八条的小批次更新四轮。新的收集轮开始时，使用更新后的策略。这样读者能把“环境样本”“优化步数”和“数据重复使用次数”对应起来，而不会把它们都叫作一个训练轮数。

## 交互：PPO削去了哪一边的更新收益

选择同一动作的新旧概率、优势与裁剪宽度。图上同时显示正负优势的代理目标，圆点标记当前样本；另一动作概率自动补足为一。把正优势动作的概率降低，或把负优势动作的概率提高，查看目标为何仍会继续变差。

[Figure: PPO正负优势目标曲线、当前样本与裁剪贡献](https://ml-biomat.com/tutorials/machine-learning/m37/#M37-svg)

纵轴随参数自动调整并标出数值。这里计算单条样本对代理目标的贡献，网络更新还会同时影响其他状态与动作；平坦段不等于整个网络梯度必为零。

## 7. 连续动作：DDPG、TD3 与 SAC

方向只有左右两个时，可以直接比较两个 Q 值；机械臂关节力矩或阀门开度连续变化，无法把每一种取值都列成输出。DDPG 用 Actor 直接给出连续动作，再让 Critic 评价这个动作。由于 Critic 对动作可求导，Actor 可以沿着提高预测价值的方向更新。经验回放与目标网络仍保留，行为阶段通常在 Actor 输出上加入噪声探索。动作应按实际上下界缩放，传给环境的力矩单位与网络内部归一化坐标要区分清楚。

$$
\nabla_\theta J_\mu\approx\mathbb E_{s\sim\mathcal D}\left[\left.\nabla_a Q_\phi(s,a)\right|_{a=\mu_\theta(s)}\nabla_\theta\mu_\theta(s)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a22dfd6872fc5c2e8a1f6913.svg) | 状态与回放池的状态采样分布。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bab5907dbf1b11459409f0e7.svg) | 确定性Actor及其参数；输出m维连续动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e46ee6754305e295e1862db5.svg) | Critic及参数；输入状态与m维动作，输出标量价值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb0c8a1ff671b47f0377effc.svg) | 价值对动作的梯度、Actor参数雅可比与Actor优化目标；乘积给参数更新方向。 |

链式法则把“动作怎样改变价值”和“参数怎样改变动作”连接起来。固定状态下令Q(a)=−(a−0.5)²、μθ=θ，当前θ=0，则价值对动作导数为1；步长0.1更新后动作变0.1，价值从−0.25变−0.16。本例动作坐标无量纲；实际力矩等动作需要记录归一化映射，梯度会随坐标尺度变化。优化Actor时冻结Critic参数，但仍保留从Critic输出传回动作的导数。

假如 Critic 在某个动作附近误画出一个尖峰，Actor 会努力走向那个峰，即使环境回报并没有相应提高。TD3 用两个 Critic 的较小预测构造目标，降低偶然高估的影响；对目标动作加入受限噪声并裁剪到合法范围，减少对狭窄尖峰的依赖；Actor 和目标网络更新得比 Critic 慢，让评价器先得到更多修正。这三个设计分别处理估计偏差、动作附近的平滑性和更新节奏，应分别通过对照检验，而不是当作一串不可拆分的名字。

SAC 学习随机策略，并把熵纳入目标。熵较高表示策略保留了更多动作选择，训练目标在环境回报与这种多样性之间取舍；温度系数控制二者的相对权重，有些实现通过目标熵自动调节温度。它同样使用回放数据和双 Critic，构造包含下一动作对数概率的软价值目标。SAC 与 TD3 的联系在于都处理连续控制中的价值估计与策略更新，区别则包括随机策略、熵目标和相应的优化形式。

$$
y_{\rm SAC}=r+\gamma(1-d)\left[\min_{j=1,2}Q_{\bar\phi_j}(s',a')-\alpha\log\pi_\theta(a'\mid s')\right],\quad a'\sim\pi_\theta(\cdot\mid s'),\qquad\mathcal L_\pi=\mathbb E\left[\alpha\log\pi_\theta(a\mid s)-\min_jQ_{\phi_j}(s,a)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/44beed4c16cc97bd1f78b2ae.svg) | 奖励、折扣、真正终止标记、当前/下一状态与相应策略采样动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e7af4ff6d55320bb687c795.svg) | 两个当前Critic及其目标副本，j=1或2，价值与回报同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a14a05c17a6f753c12e01c4a.svg) | 随机策略与参数；连续动作时使用归一化动作坐标的概率密度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a95c2d3c3aa75e4332e4f3fd.svg) | 正的温度系数、软价值目标与待最小化的策略损失；α把对数概率项换到奖励尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f66e75ac05c3b7325c622f41.svg) | Critic与目标参数，以及对回放状态和策略动作的期望。 |

较小Critic估计与熵项一起构成下一状态的软价值。奖励1、γ=.9、未终止、两个目标值2和3、α=.2、下一动作对数密度−.7，目标为1+.9×(2+.14)=2.926。策略最小化损失时倾向提高价值，同时保留由温度控制的分布宽度。连续分布的微分熵可为负，且随动作单位变化；tanh等变换需修正密度。此式对应常用双Q连续SAC，离散动作版本会相应改写动作期望。

连续策略常先采样高斯变量，再用 tanh 压到有限区间。这个变换改变了概率密度，计算对数概率时需要雅可比修正，不能直接拿变换前的高斯密度代替。还应区分三种看起来都像“加噪声”的操作：DDPG 行为噪声帮助采集新动作，TD3 目标平滑噪声用于构造训练目标，SAC 的随机性属于所学习的策略分布。它们作用的位置和评价方式不同。部署评价可使用策略均值或继续采样，但必须在结果中说明选择。

这些方法适合的条件也不同。DQN 的有限动作最大值容易算，PPO 可处理离散或连续策略且数据流程直接，DDPG、TD3 和 SAC 则重视回放复用与连续动作优化。高维动作、稀疏奖励、接触动力学和有限真实试验预算，会改变选择。下一章将进一步把离线数据、环境模型、控制方法和机器人观测接进来；本章的实际训练比较集中在同一个离散走廊，连续方法的计算通过公式和明确动作例子展开。

## 8. 同一环境、同一交互预算，观察两种学习路线

完整实验分别训练 DQN 与 PPO，使用三十七、一百三十七和二百三十七三个种子，每次训练六千一百四十四次环境交互。DQN 的回放池最多三千条，从第一百二十八条后开始，每四次交互抽取六十四条无放回样本更新；探索概率在前半预算由一降到零点零五。PPO 则采用前述十六环境、三十二步采样与四轮更新。两者隐藏层都为三十二维，但梯度更新次数不同，因此相同交互预算不等于相同计算成本。

### 同一随机走廊中的DQN与PPO完整实验

包含环境、网络、回放、目标更新、GAE、PPO裁剪、独立评价、精确策略递推和模型保存重载。

```
"""DQN and PPO on the same finite-horizon stochastic courier task."""
import argparse,copy,json,math
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2)
GAMMA=.97;HORIZON=20

class Courier:
 """Position1..5, target0or6; other endpoint is failure; action flips withp=.1."""
 def __init__(self,seed,n=1):self.rng=np.random.default_rng(seed);self.n=n;self.reset(np.arange(n))
 def reset(self,indices):
  if not hasattr(self,'position'):self.position=np.zeros(self.n,dtype=int);self.goal=np.zeros(self.n,dtype=int);self.remaining=np.zeros(self.n,dtype=int)
  self.position[indices]=self.rng.integers(1,6,len(indices));self.goal[indices]=self.rng.integers(0,2,len(indices))*6;self.remaining[indices]=HORIZON
 def observe(self):return np.column_stack([np.eye(7)[self.position],np.eye(2)[self.goal//6],self.remaining/HORIZON]).astype('float32')
 def step(self,actions):
  actual=np.asarray(actions,dtype=int)^(self.rng.random(self.n)<.1);self.position+=2*actual-1;self.remaining-=1
  reached=self.position==self.goal;wrong=(self.position==0)|(self.position==6);done=wrong|(self.remaining==0);reward=np.where(reached,1,np.where(wrong,-1,-.02)).astype('float32');next_observation=self.observe();return next_observation,reward,done,reached

class QNet(nn.Module):
 def __init__(self):super().__init__();self.net=nn.Sequential(nn.Linear(10,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2))
 def forward(self,x):return self.net(x)
class ActorCritic(nn.Module):
 def __init__(self):super().__init__();self.body=nn.Sequential(nn.Linear(10,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh());self.policy=nn.Linear(32,2);self.value=nn.Linear(32,1)
 def forward(self,x):h=self.body(x);return self.policy(h),self.value(h).squeeze(-1)

def evaluate(model,kind,seed=9001,episodes=100):
 returns=[];success=[];lengths=[]
 for episode in range(episodes):
  env=Courier(seed+episode);total=0
  for t in range(HORIZON):
   with torch.no_grad():out=model(torch.from_numpy(env.observe()));logits=out[0]if kind=='PPO'else out;action=logits.argmax(-1).numpy()
   obs,reward,done,reached=env.step(action);total+=float(reward[0])
   if done[0]:break
  returns.append(total);success.append(bool(reached[0]));lengths.append(t+1)
 return {'mean_return':float(np.mean(returns)),'success_rate':float(np.mean(success)),'mean_length':float(np.mean(lengths)),'returns':returns}

def exact_policy_value(toward_goal):
 values=np.zeros((2,7));success=np.zeros((2,7))
 for remaining in range(1,HORIZON+1):
  new=np.zeros_like(values);new_success=np.zeros_like(success)
  for target_index,goal in enumerate([0,6]):
   for position in range(1,6):
    right_probability=(.9 if goal==6 else .1)if toward_goal else .5
    for delta,probability in [(-1,1-right_probability),(1,right_probability)]:
     nxt=position+delta;end=nxt in (0,6);reward=1 if nxt==goal else -1 if end else -.02
     new[target_index,position]+=probability*(reward+(0 if end else values[target_index,nxt]))
     new_success[target_index,position]+=probability*((nxt==goal)+(0 if end else success[target_index,nxt]))
  values,success=new,new_success
 return float(values[:,1:6].mean()),float(success[:,1:6].mean())

def train_dqn(seed,steps=6144):
 torch.manual_seed(seed);rng=np.random.default_rng(seed+1);env=Courier(seed+2);net=QNet();target=copy.deepcopy(net).eval();opt=torch.optim.Adam(net.parameters(),lr=.003);buffer=[];curve=[];losses=[];obs=env.observe()[0]
 for step in range(1,steps+1):
  epsilon=max(.05,1-.95*step/(steps/2))
  with torch.no_grad():action=int(net(torch.from_numpy(obs)).argmax())
  if rng.random()<epsilon:action=int(rng.integers(2))
  nxt,reward,done,reached=env.step([action]);buffer.append((obs.copy(),action,float(reward[0]),nxt[0].copy(),bool(done[0])))
  if len(buffer)>3000:buffer.pop(0)
  obs=nxt[0]
  if done[0]:env.reset(np.array([0]));obs=env.observe()[0]
  if len(buffer)>=128 and step%4==0:
   batch=[buffer[i]for i in rng.choice(len(buffer),64,replace=False)];s,a,r,ns,d=map(np.array,zip(*batch));s=torch.tensor(s);ns=torch.tensor(ns);a=torch.tensor(a);r=torch.tensor(r,dtype=torch.float32);d=torch.tensor(d,dtype=torch.float32)
   with torch.no_grad():y=r+GAMMA*(1-d)*target(ns).max(1).values
   prediction=net(s).gather(1,a[:,None]).squeeze(1);loss=nn.functional.smooth_l1_loss(prediction,y);opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(net.parameters(),1);opt.step();losses.append(float(loss.detach()))
  if step%128==0:target.load_state_dict(net.state_dict())
  if step%512==0:curve.append([step,evaluate(net,'DQN',9001,100)['mean_return']])
 return net,curve,losses

def gae(rewards,values,next_values,dones,gamma,lam):
 advantages=np.zeros_like(rewards);last=np.zeros(rewards.shape[1],dtype=np.float32)
 for t in range(len(rewards)-1,-1,-1):
  mask=1-dones[t];delta=rewards[t]+gamma*mask*next_values[t]-values[t];last=delta+gamma*lam*mask*last;advantages[t]=last
 return advantages

def train_ppo(seed,steps=6144):
 torch.manual_seed(seed);rng=np.random.default_rng(seed+1);env=Courier(seed+2,16);net=ActorCritic();opt=torch.optim.Adam(net.parameters(),lr=.006);curve=[];diagnostics=[];horizon=32
 for update in range(steps//(16*horizon)):
  storage=[]
  for _ in range(horizon):
   obs=env.observe()
   with torch.no_grad():logits,value=net(torch.from_numpy(obs));dist=Categorical(logits=logits);action=dist.sample();oldlog=dist.log_prob(action)
   nxt,reward,done,reached=env.step(action.numpy())
   with torch.no_grad():nv=net(torch.from_numpy(nxt))[1]
   storage.append((obs,action.numpy(),oldlog.numpy(),value.numpy(),reward,done.astype('float32'),nv.numpy()));env.reset(np.flatnonzero(done))
  obs,act,oldlog,values,rewards,dones,nextvalues=[np.array(x)for x in zip(*storage)];adv=gae(rewards,values,nextvalues,dones,GAMMA,.95);returns=adv+values
  obs=torch.tensor(obs.reshape(-1,10));act=torch.tensor(act.ravel());oldlog=torch.tensor(oldlog.ravel());returns=torch.tensor(returns.ravel());adv=torch.tensor(adv.ravel());adv=(adv-adv.mean())/(adv.std(unbiased=False)+1e-8)
  for epoch in range(4):
   for ids in np.array_split(rng.permutation(len(obs)),4):
    logits,v=net(obs[ids]);dist=Categorical(logits=logits);ratio=(dist.log_prob(act[ids])-oldlog[ids]).exp();objective=torch.minimum(ratio*adv[ids],ratio.clamp(.8,1.2)*adv[ids]);vloss=(v-returns[ids]).square().mean();loss=-objective.mean()+.5*vloss-.01*dist.entropy().mean();opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(net.parameters(),.5);opt.step()
  with torch.no_grad():logits,_=net(obs);dist=Categorical(logits=logits);ratio=(dist.log_prob(act)-oldlog).exp();diagnostics.append([float(((ratio<.8)|(ratio>1.2)).float().mean()),float((oldlog-dist.log_prob(act)).mean()),float(dist.entropy().mean())])
  curve.append([(update+1)*16*horizon,evaluate(net,'PPO',9001,100)['mean_return']])
 return net,curve,diagnostics

def run(out,language):
 out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if language=='zh'else e;plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');fig.savefig(out/f'{n}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
 seeds=[37,137,237];curves={};scores={};models={};diag=[]
 for kind,train in [('DQN',train_dqn),('PPO',train_ppo)]:
  curves[kind]=[];scores[kind]=[]
  for seed in seeds:
   net,curve,detail=train(seed);curves[kind].append(curve);scores[kind].append(evaluate(net,kind,19001,500))
   if seed==37:models[kind]=net
   if kind=='PPO':diag.append(detail)
  print(kind,[x['mean_return']for x in scores[kind]],flush=True)
 # Positive max bias with independent zero-mean estimation noise.
 rng=np.random.default_rng(3700);action_counts=[2,5,10,20];bias=[];spread=[]
 for k in action_counts:
  online=rng.normal(size=(50000,k));independent=rng.normal(size=(50000,k));selected=online.argmax(1);maxima=online.max(1);double=independent[np.arange(len(online)),selected];bias.append([maxima.mean(),double.mean()]);spread.append([maxima.std()/math.sqrt(len(maxima)),double.std()/math.sqrt(len(double))])
 hand=gae(np.array([[0],[0],[1]],dtype='float32'),np.array([[.2],[.3],[.4]],dtype='float32'),np.array([[.3],[.4],[0]],dtype='float32'),np.array([[0],[0],[1]],dtype='float32'),.9,.8).ravel()
 torch.save({kind:model.state_dict()for kind,model in models.items()},out/'policies.pt');loaded=torch.load(out/'policies.pt',weights_only=True);probe=torch.eye(10);reload_errors={}
 for kind,cls in [('DQN',QNet),('PPO',ActorCritic)]:
  fresh=cls();fresh.load_state_dict(loaded[kind]);before=models[kind](probe);after=fresh(probe)
  if kind=='PPO':before,after=before[0],after[0]
  reload_errors[kind]=float((before-after).abs().max().detach())
 oracle_value,oracle_success=exact_policy_value(True);random_value,random_success=exact_policy_value(False)
 summary={'seeds':seeds,'steps_per_seed':6144,'evaluation_episodes_per_seed':500,'gamma':GAMMA,'finite_horizon':20,'slip_probability':.1,'exact_toward_goal_return':oracle_value,'exact_toward_goal_success':oracle_success,'exact_random_return':random_value,'exact_random_success':random_success,'evaluation':{kind:{'seed_mean_returns':[s['mean_return']for s in values],'seed_success_rates':[s['success_rate']for s in values],'mean_return':float(np.mean([s['mean_return']for s in values]))}for kind,values in scores.items()},'gae_hand':hand.tolist(),'dqn_hand_target':1+.9*5,'double_dqn_hand_target':1+.9*2,'dueling_hand_q':[1,3],'ppo_positive_clipped':min(1.5*2,1.2*2),'ppo_negative_clipped':min(.5*(-2),.8*(-2)),'max_bias':np.array(bias).tolist(),'action_counts':action_counts,'reload_errors':reload_errors}
 (out/'evaluation.json').write_text(json.dumps(scores,indent=2),encoding='utf-8')
 (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'configuration.json').write_text(json.dumps({'environment':'finite-horizon courier','observation':'onehotposition7,onehotgoal2,remaining/20','actions':['left','right'],'reward':'goal+1,wrong endpoint-1,otherwise-0.02','architecture':'10-32tanh-32tanh;Q2 or policy2/value1','saved_seed':37,'steps':6144,'evaluation_seed':19001},indent=2),encoding='utf-8');np.savez_compressed(out/'data.npz',dqn_curves=curves['DQN'],ppo_curves=curves['PPO'],ppo_diagnostics=diag,bias=bias,bias_standard_error=spread,gae=hand)
 fig,axs=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
 for kind,color in [('DQN','#176b91'),('PPO','#bc6945')]:
  data=np.array(curves[kind]);x=data[0,:,0];vals=data[:,:,1];axs[0].plot(x,vals.mean(0),label=kind,color=color);axs[0].fill_between(x,vals.min(0),vals.max(0),color=color,alpha=.15)
  means=[s['mean_return']for s in scores[kind]];axs[1].scatter(np.full(3,0 if kind=='DQN' else 1)+np.array([-.1,0,.1]),means,color=color,s=60,label=kind)
 axs[0].axhline(oracle_value,color='#267c6a',ls=':',label=tr('朝目标策略精确期望','Exact toward-goal expectation'));axs[0].axhline(random_value,color='#999',ls='--',label=tr('随机策略精确期望','Exact random expectation'));axs[0].set(xlabel=tr('环境交互步数 / 每个种子','Environment steps / seed'),ylabel=tr('贪心评价回报','Greedy evaluation return'),title=tr('3个种子：均值与最小—最大范围','3 seeds: mean and min–max range'));axs[0].legend(fontsize=8);axs[1].set(xticks=[0,1],xticklabels=['DQN','PPO'],ylabel=tr('独立500回合的平均回报','Mean return over 500 independent episodes'),title=tr('固定最终预算，不挑最好检查点','Fixed final budget; no best-checkpoint selection'));save(fig,'learning')
 fig,axs=plt.subplots(2,2,figsize=(11,4.8),layout='constrained')
 for row,kind in enumerate(['DQN','PPO']):
  for col,goal in enumerate([0,6]):
   ax=axs[row,col];positions=np.arange(1,6);obs=np.column_stack([np.eye(7)[positions],np.tile(np.eye(2)[goal//6],(5,1)),np.ones(5)]).astype('float32')
   with torch.no_grad():res=models[kind](torch.tensor(obs));values=res[0].softmax(-1).numpy()if kind=='PPO'else res.numpy()
   im=ax.imshow(values.T,aspect='auto',cmap='viridis',vmin=0 if kind=='PPO'else -1.1,vmax=1 if kind=='PPO'else 1.1);ax.set(xticks=range(5),xticklabels=positions,yticks=[0,1],yticklabels=tr('向左|向右','Left|Right').split('|'),xlabel=tr('初始位置','Starting position'),title=f'{kind} / '+tr('目标','target')+f'={goal}')
   for i in range(2):
    for j in range(5):ax.text(j,i,f'{values[j,i]:.2f}',ha='center',va='center',color='white'if values[j,i]<(values.max()+values.min())/2 else'#102f43')
   fig.colorbar(im,ax=ax,ticks=[0,.5,1]if kind=='PPO'else[-1,0,1],label=tr('概率'if kind=='PPO'else'Q值','Probability'if kind=='PPO'else'Q value'))
 save(fig,'policy')
 fig,axs=plt.subplots(1,3,figsize=(12,3.6),layout='constrained');bias=np.array(bias);spread=np.array(spread)
 for j,label,color in [(0,tr('同一估计取最大','Max of one estimate'),'#bc6945'),(1,tr('独立估计评价所选动作','Independent evaluation'),'#176b91')]:axs[0].errorbar(action_counts,bias[:,j],yerr=1.96*spread[:,j],fmt='o-',label=label,color=color)
 axs[0].axhline(0,color='#888',ls='--');axs[0].set(xticks=action_counts,xlabel=tr('候选动作数','Number of actions'),ylabel=tr('真实值0时的平均估计','Mean estimate when true values are 0'),title=tr('50000次噪声算例','50000 noise experiments'));axs[0].legend(fontsize=7)
 ratio=np.linspace(.3,1.7,200)
 for adv,color in [(2,'#176b91'),(-2,'#bc6945')]:axs[1].plot(ratio,np.minimum(ratio*adv,np.clip(ratio,.8,1.2)*adv),label=f'A={adv}',color=color)
 axs[1].axvspan(.8,1.2,color='#d9e4e9',alpha=.6);axs[1].set(xlabel=tr('新旧策略概率比','New/old probability ratio'),ylabel=tr('单样本代理目标','Single-sample surrogate'),title='PPO-Clip');axs[1].legend()
 axs[2].bar(range(3),hand,color='#267c6a');axs[2].set(xticks=range(3),xticklabels=['t=0','t=1','t=2'],ylabel=tr('优势估计','Advantage estimate'),title=tr('GAE手算：γ=.9，λ=.8','GAE example: γ=.9, λ=.8'));save(fig,'mechanisms');print(json.dumps(summary,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();run(args.output,args.language)
```

训练曲线每五百一十二次交互使用同一组一百个评价回合，最终固定使用训练结束的模型，在另外五百个回合上评价。每个评价回合拥有独立确定的随机种子，使不同模型从相同初始条件和逐步随机数出发；评价不再使用 DQN 的探索概率，PPO 也取最大概率动作。三个训练种子最终都学会朝目标选择，两种方法在这批评价条件下都得到平均未折扣回报约零点九零八四、成功率百分之九十八。相同结果来自相同最终贪心行为和共用评价条件。

![三种训练种子，每种6144步交互。左图每点100个固定贪心评价回合，阴影为训练种子最小—最大范围；右图为另外500个回合的最终均值。水平线由已知环境规则精确递推。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0f03f4c0a80333b89145b3ad.svg?v=0f03f4c0a803)

图 2三种训练种子，每种6144步交互。左图每点100个固定贪心评价回合，阴影为训练种子最小—最大范围；右图为另外500个回合的最终均值。水平线由已知环境规则精确递推。

环境规则已知，因此还可以从零剩余步数开始逐层递推，精确计算二十步策略的期望。始终选择目标方向的策略期望回报约零点八九八七四，成功概率约百分之九十七点五；均匀随机策略期望回报约负零点一一三二四。五百回合样本均值高于前一个期望，是有限随机样本的波动。训练使用折扣零点九七，图上的评价则累计未折扣奖励，两种数值不应混为同一个价值。图中还展示网络在不同位置与目标下输出的 Q 值或动作概率。

![种子37模型在剩余20步时的实际输出。上排为DQN动作价值，下排为PPO动作概率；两种量分开色标，同一类共用尺度。](https://ml-biomat.com/static/tutorials/machine-learning/figures/bb7797494b70b4ecfd854763.svg?v=bb7797494b70)

图 3种子37模型在剩余20步时的实际输出。上排为DQN动作价值，下排为PPO动作概率；两种量分开色标，同一类共用尺度。

Q 值图中有一个输出约一点零五，高于这个任务可获得的最大奖励一。它是函数逼近产生的价值误差，说明选对动作与估值准确是两个不同目标；网络仍可凭借左右价值的相对大小做出正确选择。PPO 面板则是概率，始终处在零至一之间并逐位置相加为一。把两种输出使用不同色标，能避免把“数值较大”误读为同一种置信程度。

机制图将三种可以独立检查的计算放在一起：最大值选择的噪声偏差、PPO 正负优势的裁剪曲线、三步 GAE 的实际结果。它们帮助解释训练部件，却不代替环境中的算法比较。程序保存两种模型的种子三十七权重、网络与环境配置、逐回合评价结果和绘图数据，并重新建立网络读取权重，确认输出差为零。这样读者既能重新训练，也能检查已经保存的策略数值。

![左：独立零均值高斯噪声的50000次选择实验，误差条为均值±1.96标准误；中：裁剪宽度0.2的单样本PPO目标；右：三步GAE手算。三者分别说明机制。](https://ml-biomat.com/static/tutorials/machine-learning/figures/692093718ce81236aabe2b3a.svg?v=692093718ce8)

图 4左：独立零均值高斯噪声的50000次选择实验，误差条为均值±1.96标准误；中：裁剪宽度0.2的单样本PPO目标；右：三步GAE手算。三者分别说明机制。

## 9. 把探索、样本效率与稳定评价分开看

强化学习的训练曲线混合了学习、探索和环境随机性。DQN 的随机动作可能使训练回报偏低，却帮助发现更好的路线；PPO 的熵也影响采样行为。评价时应明确是否保留这些随机性，训练过程中用来观察曲线的环境种子与最终报告的种子应分开。若反复挑选曲线最高的检查点，评价数据就参与了选择，最终应再用独立回合检查。这里固定最终交互预算，展示三个种子的结果及训练期间的范围，不把一次最好回合当作方法能力。

样本效率回答“多少次环境交互后学会”，计算效率回答“消耗多少时间和设备资源”，二者不能互相代替。回放方法可以重复使用样本，却增加优化工作；并行环境提高采集速度，也可能改变数据相关性和更新节奏。比较应同时记录环境步数、优化步数、回放比、网络大小和实际用时。三条训练曲线最后重合，表示这些种子在这个任务上得到相同行为，并没有估计真实部署环境的一切变化；可进一步改变动作翻转概率、目标分布或时间限制，研究策略如何适应。

奖励设计也决定学到的行为。增加移动惩罚可能鼓励快些结束，若惩罚过大甚至会改变是否值得冒险到达目标；给每次靠近目标额外奖励，需要检查是否出现来回移动获取奖励的路径。除了平均回报，还应记录成功、失败类型、耗时和约束违反次数。把这些量与实际任务联系起来，才能判断网络究竟学会了什么。神经网络扩展了表示能力，而清楚的状态、奖励、数据和评价约定，让这种能力成为可以继续研究的决策方法。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M37.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Spinning Up — Algorithm Taxonomy](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html)

   方法之间的学习对象与数据关系。
2. [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)

   像素表示与深度动作价值的早期工作。
3. [CleanRL — DQN](https://docs.cleanrl.dev/rl-algorithms/dqn/)

   目标网络、回放与实现参数。
4. [Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461)

   选择与评价分离。
5. [Dueling Network Architectures](https://arxiv.org/abs/1511.06581)

   状态与动作优势分支。
6. [Spinning Up — Policy Optimization](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)

   轨迹概率、对数导数与策略梯度。
7. [Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438)

   价值基线与优势传播。
8. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)

   裁剪代理目标与多轮更新。
9. [Spinning Up — PPO Implementation](https://raw.githubusercontent.com/openai/spinningup/master/spinup/algos/pytorch/ppo/ppo.py)

   读取PPOBuffer的终止、窗口续接与GAE计算。
10. [Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)

    正负优势裁剪与TRPO联系。
11. [Spinning Up — DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)

    连续动作最大值与可微Actor。
12. [Spinning Up — TD3](https://spinningup.openai.com/en/latest/algorithms/td3.html)

    双Critic、延迟更新与目标平滑。
13. [Spinning Up — SAC](https://spinningup.openai.com/en/latest/algorithms/sac.html)

    熵正则与软价值。
