# 从经验到行动：离线学习、预测控制与多智能体

Source: https://ml-biomat.com/tutorials/machine-learning/m38/
Language: zh-CN

让历史数据、运动模型与伙伴信息各尽其用，理解一个决策怎样走出模拟环境。

## 一辆小车，需要的不只是一张奖励表

想象一辆在图书馆送书的小车。你已经收集了工作人员驾驶它的记录，希望它先学会沿通道前进；小车启动后，还得根据当前位置及时刹车；遇到另一辆车时，两者又必须协调，才能通过狭窄入口。这三个问题都属于“怎样选择行动”，但可用信息很不一样。驾驶记录告诉它过去做过什么，运动模型告诉它某个动作可能带来什么变化，伙伴的信息则决定它应该与谁配合。选择算法之前，先认清这些信息从哪里来，往往比先选择一个复杂网络更有帮助。

前面的强化学习课程把智能体放进一个可以反复试验的环境：行动、观察奖励，再更新策略。现在我们把这条循环拆开。有时只有历史数据，不能在学习过程中追加试验；有时可以先用动力学计算未来；有时环境中还有同时学习的伙伴。离线强化学习、模型式强化学习和多智能体强化学习分别抓住了这些变化，它们也可以组合。例如，先用离线示范训练机械臂，再用学习到的动力学规划动作，最后与移动平台联合工作。这里的分类依据是信息与交互方式，并非互相排斥的模型名单。

本章安排三个能完整算清的小实验。第一张实验台只有两个状态和两个动作，用来追踪数据空白怎样影响价值；第二张实验台是一辆具有位置和速度的小车，用来比较事先安排与持续反馈；第三张实验台让两个智能体共同选择动作，用来判断奖励应该怎样归因。小环境的意义是让每个数字都有落点：我们知道真实规则，能检查计算过程，也能看清把方法搬到机器人时还要增加哪些观测、约束和数据。

## 从示范学习，到处理数据中没有出现的动作

行为克隆把驾驶记录当成监督学习数据：输入是当时看到的道路，标签是示范者的方向盘动作。对于离散动作，可以让模型输出一组概率，再增大示范动作的概率；连续动作则可以预测位置、速度或力矩目标，用相应的回归损失训练。这里不必先给每个示范动作打奖励分。它适合把已有技能快速转为可执行策略，但训练数据的观测范围决定了它主要练习过哪些情况。一个总在道路中央驾驶的专家，可能很少留下“已经偏到路边后怎样回正”的记录。

$$
\mathcal L_{\rm BC}(\theta)=-\frac1N\sum_{i=1}^{N}\log\pi_\theta(a_i\mid o_i)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | N为记录条数，i为记录编号，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0edfd5e80a775cd134ebe2cf.svg) | 第i条观测与示范动作；本例均为整数类别。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a14a05c17a6f753c12e01c4a.svg) | 带参数θ的动作条件概率；概率无量纲，本例每个状态有两个logit。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3fd1ba0c6b5f2dff6c6bb973.svg) | BC平均负自然对数似然，无量纲；log为自然对数。 |

一次示范选择动作0，模型给它0.8概率，这条损失是−ln(0.8)=0.2231；给0.2时损失升到1.6094。平均后每条示范都能贡献梯度，模型学的是“看到这个观测时示范怎样做”。

这也解释了DAgger为什么要让学习中的策略亲自产生观测，再请专家标注这些新观测该采取的动作。把新记录加入旧数据后，下一轮训练就会更多覆盖模型自己容易遇到的位置。专家查询改变了数据采集过程，因此DAgger需要继续与环境和专家交互；纯离线行为克隆则只处理已经收集的示范。收集机械臂数据时，同样要保留失败前后的恢复动作、动作执行时间、相机与关节传感器的时间对应，以及目标物体的不同姿态。示范的“好”既涉及动作质量，也涉及状态覆盖。

离线强化学习进一步利用奖励，在固定记录里寻找更高回报的策略。麻烦出现在价值更新要比较所有动作，而数据只为其中一部分动作提供证据。假设在状态s0执行动作0会到s1，奖励0；在s1执行动作0会结束，奖励1。我们保存100次这样的两步示范，共200条转移，折扣0.9，所以这条路线从s0出发的真实价值是0.9。动作1从未出现，价值表却把它初始化为3。普通离线Q学习会反复相信这个没有被样本纠正的3，甚至把s0的已记录动作也推高到2.7。

$$
\mathcal L(Q)=\frac{1}{2N}\sum_i\left[Q(s_i,a_i)-y_i\right]^2+\frac{\alpha}{N}\sum_i\left[\log\sum_a e^{Q(s_i,a)}-Q(s_i,a_i)\right],\qquad y_i=r_i+\gamma(1-d_i)\max_{a'}\bar Q(s_i',a')
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f7947c05c98be410cc3d116.svg) | N条转移的编号、当前状态、数据动作、奖励、下一状态、终止标记；d为0或1。本例奖励归一化为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/462b3a536c9dc2f497facce9.svg) | Q为2×2动作价值表，横线表示冻结的目标表，y为固定目标，均以折扣奖励计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6dad6f354c6551df5aab8c6b.svg) | 求和与最大值遍历可选动作；γ=0.9为无量纲折扣。 |
| ![Formula](https://ml-biomat.com/static/agent-math/12a26ef968e68bff378e02ae.svg) | α为相对保守惩罚权重，本例取0或1；L是标量目标。log和e表示自然对数及指数；Q在已归一化的奖励尺度下进入指数。 |

若某状态Q为[1,3]且数据只选动作0，额外惩罚为ln(e¹+e³)−1≈2.1269；改成[1,0]后约0.3133。优化因此倾向压低数据外动作相对于记录动作的高度。终止样本d=1时目标直接等于奖励，避免把终止状态继续接长。

2020年的CQL研究把这种数据外动作的高估放到了训练目标中处理。上式采用离散动作的log-sum-exp版本：一边拟合记录中的转移，一边压低候选动作相对于记录动作的过高估计。运行1000次更新后，普通Q在两个状态都选择未记录动作；CQL选择有记录的动作，贪心行为克隆也如此。若未记录动作实际奖励为−2，三者从s0出发的折扣回报分别为−2、0.9、0.9。给普通Q补上每个状态各5条动作1、奖励−2的记录，它也能选回正确路线，说明改变信息覆盖本身就有力量。

![固定数据为何留下不同答案。上排给出价值表及原始数据覆盖；下排的Q、CQL与贪心BC都仅用相同的200条记录训练，再在两个只改变未记录动作奖励的世界中评价。补齐动作的Q多用了10条奖励−2的转移，只在上排展示。共享色标−4到4，格内数值保留实际输出。](https://ml-biomat.com/static/tutorials/machine-learning/figures/641244fec01a6ed4f617ca0d.svg?v=641244fec01a)

图 1固定数据为何留下不同答案。上排给出价值表及原始数据覆盖；下排的Q、CQL与贪心BC都仅用相同的200条记录训练，再在两个只改变未记录动作奖励的世界中评价。补齐动作的Q多用了10条奖励−2的转移，只在上排展示。共享色标−4到4，格内数值保留实际输出。

再把未记录动作的真实奖励改成+2，原来的200条数据仍然完全相同。普通Q这次碰巧得到2，CQL与克隆仍得到0.9。这两个世界说明：没有被观察的动作收益需要新证据来区分，算法中的保守倾向只是选择方式。还要读清图中的具体数值：这次有限步优化得到的CQL已记录动作值约0.920和1.010，略高于真实0.9和1；“保守”描述的是目标设计，不能把图中每一个格子都读成严格下界。实验采用特意设置的乐观初始化，用来放大未经支持的动作价值如何影响更新。

## 先预测下一步，为什么能帮助选动作

骑自行车的人不必每次刹车都等到撞上障碍物才知道结果。他会利用速度、距离和对刹车效果的经验，提前判断能否停下。模型式决策把这份预测能力明确写出来：输入当前状态和动作，输出下一状态，以及需要时的奖励和终止概率。模型可以是已知物理关系，也可以从数据拟合。预测结果随后进入规划器，比较一串候选动作的后果。与直接学习动作价值相比，动力学模型提供了更细的中间解释：究竟是速度预测错了，还是代价权重让控制器愿意走得更快。

$$
x_{t+1}=Ax_t+Bu_t,\qquad x_t=\begin{bmatrix}p_t\\v_t\end{bmatrix},\quad A=\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},\quad B=\begin{bmatrix}\tfrac12\Delta t^2\\\Delta t\end{bmatrix}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0da4b4e06aa18f369f7ff17.svg) | t为离散步编号；Δt=0.2秒为主实验时间间隔。 |
| ![Formula](https://ml-biomat.com/static/agent-math/80c07f2de91d2a3f9cb14a45.svg) | x为2×1状态列向量，p是位置（m），v是速度（m/s）。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06f429a3f1595f2f96e26ad6.svg) | u是该步恒定加速度（m/s²）；A为2×2转移矩阵，B为2×1控制矩阵。非对角A项单位秒，B两行单位分别秒²和秒。 |

速度每秒变化u，持续Δt后增量就是uΔt；位置包含原速度走过的距离和匀加速增加的一半距离。由p=1 m、v=0.5 m/s、u=−1 m/s²出发，0.2 s后p=1+0.1−0.02=1.08 m，v=0.3 m/s。

我们的运动模型只有位置和速度两个状态。每0.2秒选择一个加速度，并假定这一小段内加速度保持不变，就能由匀加速运动得到上式。若只把位置给模型，同一位置上的小车可能正在前进，也可能正在后退，下一步自然不同；加入速度后，状态才包含这项必要信息。输入数据的每一列都要有明确含义。位置的米与速度的米每秒不能因为放进同一个数组就忽略单位，矩阵中的时间系数正是负责把它们换成可以相加的量。

为了模拟系统辨识，我们随机生成200组位置、速度和加速度，位置在−2到2米，速度和加速度分别在−1到1的相应单位内。真实模型算出下一状态，再给位置和速度各加标准差0.01的测量噪声，单位分别为米和米每秒。前150组用于最小二乘拟合，后50组只评价。得到的控制系数约为0.02076和0.20225，对应真值0.02和0.2；测试误差相对无噪声真值计算，位置RMSE约0.00115米、速度约0.00191米每秒。这个评价检验的是一步动力学预测。

![从150条带噪转移估计动力学。左图每格是估计系数减真实系数，p、v、u以1 m、1 m/s、1 m/s²为参考尺度，时间间隔0.2秒；右图在位置—速度平面展示实际运动轨迹，星号是静止目标。50条独立输入上的无噪声真值误差另在正文列出。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b962a3a71dcdeab2b130ff5c.svg?v=b962a3a71dcd)

图 2从150条带噪转移估计动力学。左图每格是估计系数减真实系数，p、v、u以1 m、1 m/s、1 m/s²为参考尺度，时间间隔0.2秒；右图在位置—速度平面展示实际运动轨迹，星号是静止目标。50条独立输入上的无噪声真值误差另在正文列出。

长计划会把一步预测反复送回模型，微小误差便有机会累积。如果训练数据的加速度只在−1到1之间，却让规划器搜索加速度10，得到的漂亮轨迹首先是在外推模型。模型集成可以让多个拟合器表达不同预测，规划器据此避开分歧大的区域；缩短想象轨迹并频繁接入真实观测，则减少了误差积累的时间。DreamerV3所代表的世界模型路线把观测压缩到潜在状态，在学习模型的想象轨迹中训练行为。这里我们保留可直接读懂的两维物理状态，从而看清“先预测、再决策”的共同结构。

## LQR给出反馈规律，MPC把约束放进计划

只看离目标的距离，会使小车在接近目标时仍保持较大速度，随后冲过去。控制代价因此同时考虑位置误差、速度和使用加速度的开销。线性二次调节器LQR研究的正是线性动力学配合二次代价：偏离越大，惩罚按平方增长；动作越大，执行开销也越高。这种形式的可贵之处在于，动态规划可以求出一个线性反馈规律。每次读到位置和速度，把它们乘以反馈增益，就得到当前动作，不必现场列举很长的动作树。

$$
P=Q+A^TPA-A^TPB(R+B^TPB)^{-1}B^TPA,\qquad K=(R+B^TPB)^{-1}B^TPA,\qquad u_t=-Kx_t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03989545ad94aaeaa348c0bf.svg) | 线性动力学矩阵、状态和动作，形状依次2×2、2×1、2×1和标量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb70477a5508a528bdcbf292.svg) | 状态代价矩阵diag(1,0.1)和动作代价矩阵[0.1]，形状2×2与1×1；数值是在1 m、1 m/s、1 m/s²参考尺度下的权重。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2afee757440eae1fd37defb2.svg) | P为无限时域价值的2×2对称矩阵；K为1×2反馈增益；T表示转置，−1表示矩阵求逆。归一化代价无量纲。 |

把“现在的二次代价+下一步的二次价值”对动作求最小，会得到线性反馈及Riccati方程。本实验求得K=[2.41456,2.32640]；p=1、v=0时未限幅建议u=−2.41456 m/s²，执行器上限为1时实际取−1。限幅后的控制器已改变原本无约束最优解。

为了让各项代价能直接相加，我们用1米、1米每秒和1米每二次方秒作参考尺度，并给位置、速度、动作的平方分别赋权1、0.1、0.1。增大位置权重意味着更急于回到目标，增大动作权重意味着更珍惜执行器输出。这里的无限时域LQR使用未折扣代价，求解要求相应的稳定化条件；本例双积分器可控，状态权重正定，动作权重也为正。代码利用离散Riccati方程算出增益，再把动作限制到±1。限幅很实用，但已经改变了无约束LQR所优化的问题。

模型预测控制MPC把动作界限直接写进每一次优化。它以当前测得的状态为起点，预测未来12步，也就是2.4秒，选择一串都满足加速度上限的动作。计划算完后，只执行第一步；0.2秒后取得新位置和速度，再更新整份计划。类似边走边看导航，当前路线有规划，实际情况变化后又允许重新计算。本例的线性模型让所有预测状态都是动作序列的线性函数，二次代价可以转成带上下界的最小二乘问题，SciPy即可完成求解。

$$
\min_{u_0,\ldots,u_{H-1}}\left[\sum_{j=1}^{H-1}x_j^TQx_j+x_H^TPx_H+\sum_{j=0}^{H-1}u_j^TRu_j\right]\quad\text{subject to }x_{j+1}=\hat A x_j+\hat B u_j,\ |u_j|\le u_{\max}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b81cfed776f3a3c36f7417e8.svg) | H为预测步数，本例12；j为相对当前时刻的步编号；x0为刚测得的状态，xj与uj为预测状态和计划动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd2b2a01b5fbeeae983157e.svg) | 帽子表示由150条训练转移估计的模型；Q、R为状态与动作权重，P为该估计模型的Riccati终端权重。矩阵形状和归一化单位同前。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1a5a77c2df23d512bac667fd.svg) | 最大加速度1 m/s²；T为转置，竖线为绝对值。 |

预测状态都是待选动作的线性函数，因此二次代价可写成有界最小二乘，本例直接求解整个动作序列。初始状态的代价对本次选动作是常数，故省去。若H=1，就只需比较下一状态的终端代价与这一次动作代价；找到计划后只执行第一项，再测量、再求解。

![相同的8秒运动、相同的3秒时刻速度扰动。上图显示位置，中图显示实际加速度及±1 m/s²界限，下图比较逐步归一化代价总和。MPC每0.2秒重新测量和规划；初始计划持续执行的对照完全不知道中途扰动。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5e9c715ecd6bb18389d72784.svg?v=5e9c715ecd6b)

图 3相同的8秒运动、相同的3秒时刻速度扰动。上图显示位置，中图显示实际加速度及±1 m/s²界限，下图比较逐步归一化代价总和。MPC每0.2秒重新测量和规划；初始计划持续执行的对照完全不知道中途扰动。

图中小车初始位置为1.5米、速度为0，总共运行8秒，在第3秒突然增加0.7米每秒的速度。事先安排40步再持续执行的方案没有反馈，位置逐渐偏离，累计代价约110.41；限幅LQR约13.89274，使用辨识模型的MPC约13.89256。这两种反馈方案在本实验中表现非常接近，主要差别来自能否接收扰动后的状态。MPC的结构优势是可把多步动作、状态边界和更一般的预测模型放在同一个规划问题中；具体收益取决于约束、模型和计算预算。

下面把连续加速度改成三个可选档位，使整棵短计划树可以逐条枚举。时间间隔取0.5秒，末状态位置和速度权重为2和0.5，中间状态权重为1和0.1，动作权重为0.1。增加预测步数会增加候选计划，也会改变提前刹车的时机。每按一次“执行一步”，只落实当前最优计划的第一项，然后根据新状态重新规划；第三步后的速度扰动能让你看见计划如何改写。

## 每走一步，重算接下来的路

调整初始状态与规划长度，再逐步执行。第三步后注入指定的速度扰动。图中灰线是代价紧随最优解的五条计划；未执行的未来随测量更新。

[Figure: 每走一步，重算接下来的路](https://ml-biomat.com/tutorials/machine-learning/m38/#M38-plot)

步长0.5秒；动作只选−上限、0、+上限。末状态权重(2,0.5)，中间状态权重(1,0.1)，动作权重0.1；手动单步，无自动播放。

## 伙伴也在学习，环境就会跟着改变

两个人抬桌子时，一方前进而另一方后退，通常比一起向任何一边移动都糟糕。多智能体合作也面临这种协调：一个动作是否好，要结合伙伴的动作判断。若把伙伴当成固定环境，每个人都在更新策略时，自己过去积累的经验便可能对应一位“旧伙伴”。这就是多智能体学习中的非平稳性之一。训练时可以集中使用全局状态与所有动作，执行时再让每个智能体依自己的观测行动，这种安排常称为集中训练、分散执行。

2017年的MADDPG研究让critic在训练时看到其他智能体的动作，帮助它区分环境变化与伙伴选择；actor执行时仍可只使用本地信息。2018年的QMIX从价值分解出发，让各智能体的局部价值通过单调混合器组成团队价值。单调性使各自提高局部价值的选择与混合价值的贪心选择相容，但也限制了可表达的联合价值形式。一个必须“一方左、另一方右”才高分的任务，可能需要比简单可加价值更丰富的交互表示。集中训练具体集中哪些信息，要写进数据和模型接口。

$$
J(p,q)=(1-p)(1-q)-p(1-q)-(1-p)q+3pq,\qquad A^A(a,b)=G(a,b)-\sum_{a'}\pi_A(a')G(a',b)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3c86914474b1db6c13af3d27.svg) | 智能体A、B选择动作1的概率，均在0到1之间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/395b9a6193444ab3c59e86ee.svg) | J为期望共同奖励；G为2×2奖励表[[1,−1],[−1,3]]；a、b为本次双方动作，a′遍历A的备选动作。奖励归一化无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/202deea885e03a4e37720ce6.svg) | πA为A当前动作概率；上标A标记智能体，A^A是该智能体的反事实优势，采用奖励单位。 |

四项依次是四种联合动作的概率乘奖励。p=q=0.5时J=(1−1−1+3)/4=0.5。若B实际选1，固定B后A的平均奖励是0.5×(−1)+0.5×3=1；A也选1获得优势3−1=2。换成A选0，优势是−1−1=−2。

我们采用一张最小合作奖励表：两者都选0得1，都选1得3，意见不一致得−1。策略各用一个Bernoulli概率表示，所以整个联合分布只需四种情况就能算完。当双方选择1的概率都为0.5时，期望奖励是0.5；若一方选择1的概率升到0.8，另一方仍为0.5，期望奖励升到0.8。但如果伙伴几乎总选0，盲目提高自己选择1的概率反而会增加冲突。高回报动作与当前伙伴策略之间的联系，可以在这样的小表里直接看到。

竞争任务又有另一种逻辑。石头剪刀布中，固定出石头会被固定出布的对手利用；对三种动作各取三分之一，才能让任何固定对手都没有系统优势。评估竞争策略时，应当面对一组历史对手或明确的对手分布，而不只看它是否胜过训练中的最后一个伙伴。自博弈可以不断生成新对手，历史策略池则保留旧版本，减轻策略在循环中遗忘曾经会应对的风格。合作的共同回报与竞争的可利用性，是不同的评价目标。

环境的行动时序也会改变问题。PettingZoo的Parallel接口适合把各智能体同一时刻的动作一起提交；AEC接口逐个处理智能体回合，也能在正确的更新规则下表达同时行动。石头剪刀布若错误地让第二位玩家先看见第一位玩家已经出的手势，就变成了另一个游戏。观测、合法动作掩码、每个智能体的终止标记，以及是否能读到伙伴当轮动作，都应与任务规则一致。多智能体数据多的不只是一个维度，还包括“谁在何时知道什么”。

## 共同成功以后，怎样知道谁帮上了忙

团队只收到一个总奖励时，直接把同一奖励交给所有智能体更新策略是可行起点，却会让个人学习信号混入伙伴的随机选择。例如自己这次做得不错，但伙伴失误导致总奖励低，自己的正确动作也可能被压低。反事实信用分配试着提出更细的问题：保持伙伴这次的动作不变，如果只换掉我的动作，结果会怎样？COMA把这个问题写成对本智能体备选动作的概率平均，用集中critic估计联合动作价值，再减去这份反事实平均。

$$
g_A=(a-p)\,[G(a,b)-b_A(b)],\qquad b_A(b)=\sum_{a'}\pi_A(a')G(a',b)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f45b7f6b64a4cd71bdeb9bdb.svg) | gA为对A的Bernoulli logit的单样本策略梯度；a取0或1，p为选择1的概率。a−p是对数概率对logit的导数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d8ac0f4ccf5d1edfd23ff034.svg) | G是共同奖励，b是B已选动作，bA是固定b后按A当前概率平均的奖励基线；求和遍历A备选动作。基线在策略梯度计算时停止求导。 |

在均匀策略下逐一枚举四种联合动作，不用基线时gA依次为−0.5、0.5、−0.5、1.5，均值0.25、方差0.6875；使用反事实基线后变为−0.5、1、−0.5、1，均值仍为0.25、方差0.5625。方差减少来自这个具体奖励表和当前概率。

本例直接知道四格真实奖励，因此反事实基线能精确计算，不需要另训critic。当双方概率都是0.5时，原始奖励梯度与带基线梯度的均值同为0.25，方差却从0.6875变为0.5625。均值保持的原因是：对自己的动作求期望时，对数概率导数的平均为0；只依赖伙伴动作的基线因此消去。实现中基线要停止求导，否则自动微分会把它对策略参数的依赖也加入更新，得到另一个目标的梯度。这个小细节正好能连接策略梯度公式和实际代码。

![合作奖励、信用分配与学习曲线放在同一页。上方梯度均值和方差由四种联合动作精确枚举；下方为4个种子、每次32个动作对、180次更新的真实训练。实线是种子均值，色带是最小到最大值；纵轴是当前策略在奖励表上的精确期望值。](https://ml-biomat.com/static/tutorials/machine-learning/figures/9641389b1e92c8e21d437a0c.svg?v=9641389b1e92)

图 4合作奖励、信用分配与学习曲线放在同一页。上方梯度均值和方差由四种联合动作精确枚举；下方为4个种子、每次32个动作对、180次更新的真实训练。实线是种子均值，色带是最小到最大值；纵轴是当前策略在奖励表上的精确期望值。

实际训练给两个Bernoulli策略各一个可学习logit，每次抽取32组同步动作，使用Adam更新180次，比较四个随机种子。两种方法都学会更频繁地选择高分的联合动作。最后原始奖励策略的期望回报约2.893到2.899，反事实基线策略约2.874到2.886，均接近上限3；这次最终数值并未因加入基线而更高。上面的精确方差结论针对均匀策略的一次梯度，下面的训练还受到策略变化、有限批次与Adam自适应步长影响，二者回答的是不同问题。

这份比较也给出了选择实验指标的办法。如果研究的是信用分配，就同时看梯度信号的均值、方差与团队学习过程；如果研究的是分散执行，就检查每个actor在部署时真正得到哪些观测；如果研究的是合作鲁棒性，就改变伙伴策略再评价。把整场表现压成一个最终分数，很容易漏掉方法究竟改善了哪一步。这里保留每个种子的完整曲线，色带表示最小到最大值，读者可以看到变异大小，而不是把一条平滑均值误读成每次训练都会经过的路线。

## 从完整状态走向相机、延迟与真实执行器

模拟器可以直接给出精确位置、速度和接触力，真实机器人通常得到的是相机图像、编码器读数和有延迟的传感器输出。单张图像可能无法判断物体正向左还是向右运动；同样的关节位置，也可能伴随不同速度和负载。部分可观测问题需要利用观测历史，把不确定性带进状态估计。堆叠连续帧、使用循环网络、显式估计速度，或维护一份隐藏状态概率分布，都在补充当前观测缺少的信息。选择哪一种取决于缺失的是运动趋势、遮挡目标还是未知物理参数。

$$
b_{t+1}(s')=\eta\,O(o_{t+1}\mid s')\sum_s P(s'\mid s,a_t)b_t(s)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6287735b28999d9ded38a578.svg) | b为对隐藏状态的概率分布；s、s′分别遍历当前和下一隐藏状态。概率无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f29fa5b53beed1a41e25d98a.svg) | a为已执行动作，o为新观测；P为状态转移概率，O为该状态产生观测的概率。此式采用观测仅依赖新状态的模型。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2092c6227405ee2600312c46.svg) | η为使所有新状态概率之和为1的归一化系数；t为时间步；求和合并旧状态的不确定性。 |

先依据动力学预测，再用新观测校正。假设静止目标在左/右的先验各0.5，传感器报告“左”在真左时概率0.8、真右时0.2；未归一化结果是0.4和0.1，乘η=2得到后验0.8和0.2。下一次动作可以利用这种不确定性，而不必把一次读数当作完全可靠的位置。

动作接口同样要具体。网络输出0.5可以表示0.5牛米的关节力矩，也可以表示归一化区间中间偏上的目标位置；两者接到执行器后完全不同。部署前要把动作尺度、坐标系、控制频率和低层伺服方式对应好。若高层策略每秒更新10次，而电机控制器每秒更新1000次，中间的插值与保持规则就参与了系统动力学。延迟可通过把上一些动作与观测时间戳放进状态表示来建模，接触与摩擦变化则可能要求非线性或分段模型。

仿真迁移的关键是让训练中遇到的变化与真实变化对得上。2017年的视觉域随机化工作通过改变模拟画面的外观帮助目标定位迁移；对于控制，还可以围绕质量、摩擦、传感器噪声和动作延迟设计动力学随机化。随机范围应覆盖可解释的设备变化，例如负载增加如何改变同一力矩带来的加速度，而不是任意扩大所有参数。系统辨识提供另一条路径：用真实转移拟合参数，再在这个模型附近训练或规划。二者可以结合，以测量确定中心，以不确定性决定变化范围。

约束也应拥有自己的位置。给碰撞一个负奖励，会让算法在“收益很大时是否值得碰撞”之间权衡；把关节角度、速度或力矩写成硬约束，则直接限制候选动作集合。MPC可以在规划中处理这些约束，执行层也可检查命令边界并采用既定的停止动作。状态约束是否能保持，进一步取决于模型误差、扰动范围和优化问题是否可行。工程上要明确约束量的单位、测量方式和恢复步骤，这些都能转成具体的测试场景。

## 没有重新运行策略，怎样评价它可能做到什么

离线策略评价希望利用旧策略采集的数据，估计新策略的回报。最直观的方法是重要性采样：新策略更容易产生的轨迹，在平均时增加权重；更不容易产生的轨迹则降低权重。这个比例沿时间步相乘，是因为一条轨迹的动作选择概率由各步条件概率组成。若新策略会执行某个动作，而旧策略在对应历史下从不执行它，数据中就没有可用于重新加权的那部分经验。前面两个世界共享同一份数据的例子，在这里表现为覆盖条件。

$$
\hat V_{\rm IS}=\frac1N\sum_{i=1}^N w_iG_i,\qquad w_i=\prod_{t=0}^{T_i-1}\frac{\pi(a_{it}\mid h_{it})}{\beta(a_{it}\mid h_{it})}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e855114b6328e693859ab863.svg) | N为独立回合数，i为回合编号，t为步编号，Ti为该回合长度，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6dd7ff37e2727fe45f4771fd.svg) | Gi为回合折扣回报；wi为无量纲重要性权重；V帽是目标策略价值估计，单位同奖励。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d634b295bfd681b8684a500f.svg) | π为待评价策略，β为数据采集策略；a为已执行动作，h为当时可用的完整历史或足够状态。分母必须对目标策略会用到的动作保持正概率。 |

某两步轨迹的目标/采集概率分别为0.8/0.5、0.6/0.3，权重为3.2。若两条轨迹回报2和1、权重3.2和0.4，普通IS估计为(3.2×2+0.4×1)/2=3.4；自归一化版本改除权重总和3.6，得到1.8889。两种有限样本估计的偏差与方差不同。

轨迹越长，许多个概率比相乘越容易产生极大或极小权重，少数回合便可能主导估计。自归一化权重、逐决策估计和混合估计试着管理这份波动。另一条路线是拟合价值评价FQE：把待评价策略固定下来，用它对下一步动作取期望，再拟合这份策略的Bellman目标；这里评价的是指定策略，不能悄悄换成最大化所有动作。模型式评价则先拟合转移和奖励，再在模型中运行策略。它们各自依赖行为概率、价值函数或动力学拟合的质量。

实际数据应按完整回合、设备或时间段划分训练与评价，避免把同一次操作的相邻帧分到两边。还应保存行为策略版本、动作概率（能够取得时）、奖励定义、自然终止与时间截断，以及观测到动作之间的延迟。Minari这样的数据接口能够组织和遍历回合，具体的数据加载器、字段转换及适用的数据许可仍需对应所选数据集。先查看数据是否覆盖计划研究的状态和动作，再决定采用行为克隆、保守价值学习还是继续采集，通常能把实验问题确定得更扎实。

如果一次新策略评价要估计的是“在新的负载下能否安全完成搬运”，仅更换策略权重还不够，负载已经改变了环境。应该分别安排同环境策略比较、负载变化试验与观测噪声试验，记录成功率、任务用时和约束触发情况。这样可以明确是策略改进、动力学适应还是传感器处理带来了变化。本章的真实规则全都公开，因此能够直接运行策略得到真值，再用这些真值理解离线估计需要哪些信息；真实任务则用可取得的独立运行逐步校准估计过程。

## 把三个实验放到同一套可重复流程中

完整程序依次生成离线记录、拟合动力学并运行控制器、训练合作策略，最后保存全部图和数值。离线Q与CQL都用Adam、学习率0.03、1000次更新，每20步复制目标表；行为克隆用同样学习率训练300次。控制部分固定随机种子38，辨识模型只使用前150组转移，剩余50组不参与拟合。合作实验使用38、138、238、338四个种子，学习率0.04。各实验的评价量分别是折扣回报、归一化控制代价和单次共同奖励，阅读时要保留这种量纲与任务的差别。

### 完整实验：离线动作覆盖、受扰运动与协作信用

只需NumPy、SciPy、PyTorch和Matplotlib。使用--output指定输出目录、--language选择图内语言；summary.json保存数值，data.npz保存曲线和轨迹，models.npz保存价值表、BC概率、辨识矩阵与反馈增益。所有数据按代码规则生成。

```
"""Offline learning, receding-horizon control, and cooperative credit assignment.

All environments and datasets are generated here. No external weights or data.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import solve_discrete_are, block_diag
from scipy.optimize import lsq_linear

torch.set_num_threads(2)
COLORS = ['#256d85', '#e58f38', '#8a5a9e', '#4c9571']


def offline_fit(alpha, covered=False):
    # Repeated rows are repeated observations, not independent environments.
    s = torch.tensor([0, 1] * 100)
    a = torch.zeros(200, dtype=torch.long)
    reward = torch.tensor([0., 1.] * 100)
    nxt = torch.ones(200, dtype=torch.long)
    done = torch.tensor([0., 1.] * 100)
    if covered:
        s = torch.cat((s, torch.tensor([0, 1] * 5)))
        a = torch.cat((a, torch.ones(10, dtype=torch.long)))
        reward = torch.cat((reward, -2 * torch.ones(10)))
        nxt = torch.cat((nxt, torch.zeros(10, dtype=torch.long)))
        done = torch.cat((done, torch.ones(10)))
    q = torch.nn.Parameter(torch.tensor([[0., 3.], [0., 3.]]))
    target = q.detach().clone()
    optimizer = torch.optim.Adam([q], lr=.03)
    curve = []
    for step in range(1000):
        y = reward + .9 * (1-done) * target[nxt].max(dim=1).values
        error = .5 * (q[s, a]-y).square().mean()
        penalty = (torch.logsumexp(q[s], dim=1)-q[s, a]).mean()
        loss = error + alpha * penalty
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        if (step+1) % 20 == 0:
            target = q.detach().clone()
            curve.append(q.detach().numpy().copy())
    logits = torch.nn.Parameter(torch.zeros(2, 2))
    opt_bc = torch.optim.Adam([logits], lr=.03)
    for _ in range(300):
        loss = torch.nn.functional.cross_entropy(logits[s], a)
        opt_bc.zero_grad(); loss.backward(); opt_bc.step()
    return q.detach().numpy(), np.array(curve), logits.detach().softmax(1).numpy()


def rollout_table(q, unobserved_reward):
    state, value = 0, 0.
    for t in range(2):
        action = int(np.argmax(q[state]))
        if action == 1:
            return value + .9**t * unobserved_reward
        if state == 1:
            return value + .9**t
        state = 1
    return value


def mpc_plan(A, B, Q, R, P, x, horizon=12, limit=1.):
    # Stack x_1,...,x_H = S x_0 + T [u_0,...,u_(H-1)].
    n = len(x)
    S = np.vstack([np.linalg.matrix_power(A, i+1) for i in range(horizon)])
    T = np.zeros((n*horizon, horizon))
    for i in range(horizon):
        for j in range(i+1):
            T[n*i:n*(i+1), j] = (np.linalg.matrix_power(A, i-j) @ B).ravel()
    weights = block_diag(*([Q]*(horizon-1)+[P]))
    L = np.linalg.cholesky(weights).T
    design = np.vstack((L @ T, np.sqrt(R[0, 0])*np.eye(horizon)))
    rhs = np.r_[-L @ S @ x, np.zeros(horizon)]
    result = lsq_linear(design, rhs, bounds=(-limit, limit), tol=1e-10)
    assert result.success
    return result.x


def control_experiment():
    rng = np.random.default_rng(38)
    dt = .2
    A = np.array([[1., dt], [0., 1.]])
    B = np.array([[.5*dt*dt], [dt]])
    features = rng.uniform([-2., -1., -1.], [2., 1., 1.], size=(200, 3))
    exact = features[:, :2] @ A.T + features[:, 2:] @ B.T
    measured = exact + rng.normal(0., .01, exact.shape)
    fit = np.linalg.lstsq(features[:150], measured[:150], rcond=None)[0].T
    Ah, Bh = fit[:, :2], fit[:, 2:]
    test_error = features[150:] @ fit.T - exact[150:]
    Q, R = np.diag([1., .1]), np.array([[.1]])
    P = solve_discrete_are(A, B, Q, R)
    Ph = solve_discrete_are(Ah, Bh, Q, R)
    K = np.linalg.solve(R+B.T@P@B, B.T@P@A)
    outputs = {}
    initial = np.array([1.5, 0.])
    initial_plan = mpc_plan(A, B, Q, R, P, initial, horizon=40)
    for name in ['Open loop', 'LQR clipped', 'Learned MPC']:
        x = initial.copy(); states = [x.copy()]; actions = []; cost = 0.
        for t in range(40):
            if name == 'Open loop':
                u = initial_plan[t]
            elif name == 'LQR clipped':
                u = float(np.clip((-K@x).item(), -1., 1.))
            else:
                u = mpc_plan(Ah, Bh, Q, R, Ph, x)[0]
            cost += float(x@Q@x + R[0, 0]*u*u)
            x = A@x + B[:, 0]*u
            if t == 14:
                x[1] += .7
            actions.append(u); states.append(x.copy())
        outputs[name] = {'states': np.array(states), 'actions': np.array(actions), 'cost': cost}
    return A, B, Ah, Bh, K, outputs, np.sqrt(np.mean(test_error**2, axis=0))


PAYOFF = np.array([[1., -1.], [-1., 3.]])


def credit_statistics(p=.5, q=.5):
    pa, pb = np.array([1-p, p]), np.array([1-q, q])
    probability = pa[:, None]*pb[None, :]
    baseline = pa @ PAYOFF
    score = np.array([-p, 1-p])[:, None]
    shared = score * PAYOFF
    counterfactual = score * (PAYOFF-baseline[None, :])
    result = []
    for gradient in [shared, counterfactual]:
        mean = float((probability*gradient).sum())
        variance = float((probability*(gradient-mean)**2).sum())
        result.append([mean, variance])
    return np.array(result)


def cooperative_train(seed, counterfactual):
    torch.manual_seed(seed)
    logits = torch.nn.Parameter(torch.zeros(2))
    optimizer = torch.optim.Adam([logits], lr=.04)
    payoff = torch.tensor(PAYOFF, dtype=torch.float32)
    curves = []
    for _ in range(180):
        probs = torch.sigmoid(logits)
        distribution = torch.distributions.Bernoulli(probs=probs)
        actions = distribution.sample((32,)).long()
        rewards = payoff[actions[:, 0], actions[:, 1]]
        advantages = rewards[:, None].expand(-1, 2).clone()
        if counterfactual:
            weights = torch.stack((1-probs, probs), dim=1).detach()
            b0 = (weights[0, :, None]*payoff[:, actions[:, 1]]).sum(0)
            b1 = (weights[1, None, :]*payoff[actions[:, 0], :]).sum(1)
            advantages -= torch.stack((b0, b1), dim=1)
        loss = -(distribution.log_prob(actions.float())*advantages.detach()).sum(1).mean()
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        p, q = torch.sigmoid(logits).detach().numpy()
        expected = np.array([1-p, p]) @ PAYOFF @ np.array([1-q, q])
        curves.append([float(p), float(q), float(expected)])
    return np.array(curves)


def draw(out, language, q_values, control, curves, statistics, model):
    zh = language == 'zh'
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
                         'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig, name):
        fig.savefig(out/f'{name}-{language}.svg', bbox_inches='tight', facecolor='white')
        fig.savefig(out/f'{name}-{language}.png', dpi=155, bbox_inches='tight', facecolor='white')
        plt.close(fig)
    fig = plt.figure(figsize=(12.8, 6.7), layout='constrained')
    grid = fig.add_gridspec(2, 4, height_ratios=[1, .8])
    names = ['离线 Q','CQL α=1','补齐动作后的 Q'] if zh else ['Offline Q','CQL α=1','Q with action coverage']
    for i, (name, q) in enumerate(zip(names, q_values)):
        ax = fig.add_subplot(grid[0, i]); im = ax.imshow(q, vmin=-4, vmax=4, cmap='RdBu')
        for row in range(2):
            for col in range(2):
                ax.text(col, row, f'{q[row,col]:.2f}', ha='center', va='center', color='white' if abs(q[row,col])>2.5 else '#172838')
        ax.set_xticks([0,1],['a0','a1']); ax.set_yticks([0,1],['s0','s1']); ax.set_title(name)
    fig.colorbar(im, ax=fig.axes, shrink=.75, label='Q（折扣奖励）' if zh else 'Q (discounted reward)', ticks=[-4,0,4])
    ax = fig.add_subplot(grid[0, 3]); counts = np.array([[100,0],[100,0]])
    ax.imshow(counts, cmap='Blues',vmin=0,vmax=100)
    for i in range(2):
        for j in range(2): ax.text(j,i,str(counts[i,j]),ha='center',va='center',color='white' if j==0 else '#172838')
    ax.set_xticks([0,1],['a0','a1']);ax.set_yticks([0,1],['s0','s1']);ax.set_title('原始数据次数' if zh else 'Original transition counts')
    ax = fig.add_subplot(grid[1,:]); rows = ['未知动作奖励 −2','未知动作奖励 +2'] if zh else ['Unobserved action reward −2','Unobserved action reward +2']
    values = np.array([[rollout_table(q,-2),rollout_table(q,2)] for q in q_values[:2]]+[[.9,.9]])
    labels = names[:2]+(['行为克隆（贪心）'] if zh else ['Behavior cloning (greedy)'])
    for i in range(3):ax.bar(np.arange(2)+(i-1)*.2, values[i],width=.19,label=labels[i],color=COLORS[i])
    ax.axhline(0,color='#687b88',lw=.7);ax.set_xticks([0,1],rows);ax.set_ylabel('真实折扣回报' if zh else 'True discounted return');ax.legend(ncols=4,loc='lower center',bbox_to_anchor=(.5,1.04),frameon=False)
    save(fig,'offline')
    fig, axes = plt.subplots(3,1,figsize=(12,8.6),layout='constrained',height_ratios=[1.4,1,.8])
    names_zh={'Open loop':'初始计划持续执行','LQR clipped':'限幅 LQR 反馈','Learned MPC':'学习模型 + MPC'}
    for i,(name,result) in enumerate(control.items()):
        label=names_zh[name] if zh else name
        axes[0].plot(np.arange(41)*.2,result['states'][:,0],label=label,color=COLORS[i],lw=2.1)
        axes[1].step(np.arange(40)*.2,result['actions'],where='post',color=COLORS[i],lw=1.7)
    for ax in axes[:2]:ax.axvline(3,color='#c74f48',ls='--',lw=1.2);ax.grid(alpha=.14)
    axes[0].set_ylabel('位置 / m' if zh else 'Position / m');axes[0].legend(ncols=3,frameon=False);axes[0].set_title('3 s 时速度突然增加 0.7 m/s' if zh else 'Velocity impulse +0.7 m/s at t = 3 s')
    axes[1].set_ylabel('加速度 / (m/s²)' if zh else 'Acceleration / (m/s²)');axes[1].axhline(1,ls=':',color='gray');axes[1].axhline(-1,ls=':',color='gray');axes[1].set_xlabel('时间 / s' if zh else 'Time / s')
    names=list(control);costs=[control[n]['cost'] for n in names]
    axes[2].barh(range(3), costs,color=COLORS[:3]);axes[2].set_yticks(range(3),[names_zh[n] if zh else n for n in names]);axes[2].invert_yaxis();axes[2].set_xlabel('40 步累积代价（归一化）' if zh else '40-step accumulated cost (normalized)')
    for i,c in enumerate(costs):axes[2].text(c+.3,i,f'{c:.2f}',va='center')
    axes[2].set_xlim(0,max(costs)*1.15)
    save(fig,'control')
    fig=plt.figure(figsize=(12.4,7.4),layout='constrained');gs=fig.add_gridspec(2,3,height_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(PAYOFF,cmap='RdBu',vmin=-3,vmax=3)
    for i in range(2):
        for j in range(2):ax.text(j,i,str(int(PAYOFF[i,j])),ha='center',va='center',fontsize=23,color='white' if PAYOFF[i,j]==3 else '#172838')
    ax.set_xticks([0,1],['0','1']);ax.set_yticks([0,1],['0','1']);ax.set_xlabel('智能体 B 动作' if zh else 'Agent B action');ax.set_ylabel('智能体 A 动作' if zh else 'Agent A action');ax.set_title('共同奖励矩阵' if zh else 'Shared reward matrix');fig.colorbar(im,ax=ax,shrink=.8,ticks=[-3,0,3])
    ax=fig.add_subplot(gs[0,1:]);bar_names=['共同奖励','反事实基线'] if zh else ['Shared reward','Counterfactual baseline']
    for i in range(2):ax.bar(np.arange(2)+(i-.5)*.3,statistics[:,i],.28,color=COLORS[i],label=['梯度均值','梯度方差'][i] if zh else ['Gradient mean','Gradient variance'][i])
    ax.set_xticks([0,1],bar_names);ax.set_ylim(0,.9);ax.legend(frameon=False,ncols=2,loc='upper center');ax.set_title('两方均以 0.5 概率选择动作 1' if zh else 'Both agents choose action 1 with probability 0.5');ax.set_ylabel('精确枚举值' if zh else 'Exact enumeration')
    for i in range(2):
        for j in range(2):ax.text(j+(i-.5)*.3,statistics[j,i]+.015,f'{statistics[j,i]:.4f}',ha='center',fontsize=10)
    ax=fig.add_subplot(gs[1,:])
    for i,c in enumerate(curves):
        y=c[:,:,2];ax.plot(np.arange(1,181),y.mean(0),color=COLORS[i],label=bar_names[i]);ax.fill_between(np.arange(1,181),y.min(0),y.max(0),color=COLORS[i],alpha=.17)
    ax.axhline(3,color='gray',ls=':',label='最优共同奖励' if zh else 'Optimal shared reward');ax.set_xlabel('更新次数（每次 32 次同步决策）' if zh else 'Updates (32 simultaneous decisions each)');ax.set_ylabel('策略的精确期望奖励' if zh else 'Exact expected policy reward');ax.legend(ncols=3,frameon=False)
    save(fig,'cooperation')
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.9),layout='constrained')
    A,B,Ah,Bh=model
    true=np.column_stack((A,B));estimated=np.column_stack((Ah,Bh))
    error=estimated-true;lim=np.max(abs(error))
    im=axes[0].imshow(error,cmap='RdBu',vmin=-lim,vmax=lim)
    for i in range(2):
        for j in range(3):axes[0].text(j,i,f'{error[i,j]:+.4f}',ha='center',va='center',color='white' if abs(error[i,j])>.65*lim else '#172838')
    axes[0].set_xticks(range(3),['p','v','u']);axes[0].set_yticks(range(2),['下一步 p','下一步 v'] if zh else ['p next','v next']);axes[0].set_title('归一化模型系数误差' if zh else 'Normalized model-coefficient error');fig.colorbar(im,ax=axes[0],shrink=.8,label='无量纲' if zh else 'Dimensionless')
    for i,(name,result) in enumerate(control.items()):axes[1].plot(result['states'][:,0],result['states'][:,1],color=COLORS[i],label=names_zh[name] if zh else name)
    axes[1].scatter([0],[0],s=70,marker='*',c='#172838');axes[1].set_xlabel('位置 / m' if zh else 'Position / m');axes[1].set_ylabel('速度 / (m/s)' if zh else 'Velocity / (m/s)');axes[1].legend(frameon=False,fontsize=9);axes[1].set_title('同一扰动下的状态轨迹' if zh else 'State trajectories under the same impulse')
    save(fig,'identification')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    q0,c0,bc=offline_fit(0);qc,cc,_=offline_fit(1);qcov,ccov,_=offline_fit(0,True)
    A,B,Ah,Bh,K,control,error=control_experiment()
    curves=np.array([[cooperative_train(seed,mode)for seed in [38,138,238,338]]for mode in [False,True]])
    statistics=credit_statistics()
    summary={'offline_q':q0.tolist(),'cql_q':qc.tolist(),'covered_q':qcov.tolist(),'bc_probabilities':bc.tolist(),
             'bad_world_returns':[rollout_table(q,-2) for q in [q0,qc,qcov]],'good_world_returns_original_data':[rollout_table(q,2) for q in [q0,qc]],
             'A_true':A.tolist(),'B_true':B.tolist(),'A_fit':Ah.tolist(),'B_fit':Bh.tolist(),'lqr_gain':K.tolist(),'heldout_model_rmse':error.tolist(),
             'control_costs':{k:v['cost']for k,v in control.items()},'max_abs_action':max(float(abs(v['actions']).max())for v in control.values()),
             'credit_mean':statistics[:,0].tolist(),'credit_variance':statistics[:,1].tolist(),'cooperation_final_return':curves[:,:,-1,2].tolist(),
             'one_step_state':(A@np.array([1.,.5])+B[:,0]*-1).tolist(),'discounted_demonstration_return':.9,
             'importance_weight_hand':(.8/.5)*(.6/.3),'is_hand_return':((.8/.5)*(.6/.3)*2+.4*1)/2}
    np.savez(out/'data.npz',offline_q=q0,cql_q=qc,covered_q=qcov,bc=bc,q_curve=c0,cql_curve=cc,covered_curve=ccov,cooperation=curves,
             **{k.replace(' ','_')+'_'+vname:v for k,result in control.items()for vname,v in result.items()})
    np.savez(out/'models.npz',offline_q=q0,cql_q=qc,bc_probabilities=bc,A_fit=Ah,B_fit=Bh,lqr_gain=K)
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    draw(out,args.language,[q0,qc,qcov],control,curves,statistics,(A,B,Ah,Bh))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

运行后，summary.json可以逐项核对正文中的数值，data.npz保留价值更新曲线、每步状态与动作，以及所有合作训练种子。models.npz保存离线价值表、克隆概率、动力学矩阵与反馈增益，能够直接用于同规则下的推理。改变实验时可以先问一个具体问题：增加少量动作1记录能否消除高估；把模型训练中的加速度范围缩小后，规划表现怎样变化；把伙伴的一个概率固定下来，自己的策略会如何调整。每次改变一个信息条件，图中的变化便容易与原因对应。

进一步进入机器人或多智能体平台时，继续沿用这条顺序：明确观测和动作含义，检查数据覆盖，确定动力学与奖励，再选择评价过程。离线数据让经验得以积累，预测模型让未来可以比较，反馈让行动能够适应变化，信用分配让合作中每个参与者得到更具体的学习信号。理解这些环节怎样连接，便能根据任务需要组合方法，而不必把一个算法名字当作整套决策系统。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M38.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Conservative Q-Learning for Offline Reinforcement Learning](https://arxiv.org/abs/2006.04779)

   原论文第2—4页、式4及附录实现段：分布偏移、log-sum-exp和估计条件。
2. [imitation: Behavioral Cloning and DAgger](https://imitation.readthedocs.io/en/latest/algorithms/dagger.html)

   官方算法说明、专家查询与数据聚合；同站BC的监督训练接口。
3. [Minari: Basic Usage](https://minari.farama.org/content/basic_usage/)

   回合抽样、iterate_episodes和数据加载责任。
4. [Underactuated Robotics: LQR](https://underactuated.mit.edu/lqr.html)

   离散时间Riccati方程、反馈增益与二次代价。
5. [Underactuated Robotics: Trajectory Optimization](https://underactuated.mit.edu/trajopt.html)

   轨迹优化问题与Model Predictive Control段。
6. [DreamerV3: Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104)

   摘要中的学习世界模型与想象中的行为学习；未复现该大规模模型。
7. [Counterfactual Multi-Agent Policy Gradients](https://arxiv.org/html/1705.08926v3)

   方法第4节：集中critic、其他动作固定时的反事实基线。
8. [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275)

   摘要：非平稳性与训练时使用其他智能体信息。
9. [QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485)

   摘要：单调混合与分散贪心执行的一致性。
10. [PettingZoo: AEC and Parallel API](https://pettingzoo.farama.org/api/parallel/)

    Parallel API及AEC API的行动时序、有效动作与终止处理。
11. [Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907)

    摘要：视觉外观随机化与目标定位任务。
12. [Empirical Study of Off-Policy Policy Evaluation](https://arxiv.org/abs/1911.06854)

    PDF第4页方法分类、第13页权重定义与长时域讨论。
