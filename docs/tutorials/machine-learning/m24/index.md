# 强化学习：从试探到长期决策

Source: https://ml-biomat.com/tutorials/machine-learning/m24/
Language: zh-CN

从午餐选择和悬崖边的路线，理解 Bandit、MDP、Bellman、TD、SARSA 与 Q-learning。

## 先选午餐，还是先学会走路

第一次到陌生街区吃午饭，你可以去已经满意的店，也可以试一家没去过的店。熟悉的店提供较稳妥的收益，新店则提供可能影响以后选择的信息。如果只剩今天一顿饭，尝试的价值通常较小；如果将在这里住一年，早一点了解不同店铺就更有用。这个简单情境已经包含强化学习的一个核心问题：行动既会带来结果，也会改变以后能够获得的信息。推荐系统怎样安排探索、游戏角色怎样走到目标、仓库机器人怎样选择路线，都需要处理类似的取舍。

不过，选午餐与走路仍有一项关键差别。在最简单的多臂老虎机模型中，今天选择哪家店并不改变明天有哪些店可选，收益只与本次选项有关。走路时，向右一步会把你带到另一个位置，下一次能做什么随之改变；看似多绕两步的动作，也许能避开一段容易失足的窄路。前者适合学习探索与利用，后者要求把状态、转移、长期回报和策略一起建模。本章沿这条顺序，把一张小表格怎样学会决策算清楚，再用悬崖边走格子的实验比较 SARSA 和 Q-learning。

强化学习与监督学习的训练信号也不同。识别手写数字时，每张训练图片附有目标类别；学习走路时，环境通常只反馈这一步花了多少时间、是否到达终点、是否跌落，并没有逐步给出“正确动作”。学习者要从一串结果中判断前面的动作有多大贡献，这叫延迟信用分配。开始学习前最值得问的是：动作确实会影响后续状态吗，是否能获得可靠反馈，交互试错的成本有多大？这些问题决定任务需要哪种模型和实验环境。

![行动产生奖励和新状态，价值与策略再改变下一次选择。下方以TD（1988）与Q-learning（1992）的论文节点说明由预测进入控制的思路；这是根据算法定义绘制的概念图。](https://ml-biomat.com/static/tutorials/machine-learning/figures/63993347597fcb952a139c49.svg?v=63993347597f)

图 1行动产生奖励和新状态，价值与策略再改变下一次选择。下方以TD（1988）与Q-learning（1992）的论文节点说明由预测进入控制的思路；这是根据算法定义绘制的概念图。

## 探索的成本，与没有探索的成本

把四家餐馆想象成四个按钮，每次按下一个按钮便得到一个带噪声的分数。这里“臂”就是一个选项；分数的期望是它长期的平均质量，单次分数还会受到出餐速度、当天口味等偶然因素影响。对某个按钮已经观察到的分数取平均，就得到它的动作价值估计。这个估计可以逐次更新，不必把全部历史分数保存在内存里：新样本和旧平均值的差是本次信息，已经观察的次数越多，新样本的权重越小。

$$
\widehat q_{n+1}(a)=\widehat q_n(a)+\frac{R_{n+1}-\widehat q_n(a)}{n+1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 一个按钮或动作的编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1dcdc987095eab8d037d9299.svg) | 动作a被观察n次后的平均奖励估计，与奖励同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 该动作已有的观测次数，正整数；新动作首次观测直接初始化。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e9bd7eea834fbc463ff80d4e.svg) | 该动作新获得的第n+1次奖励，与平均奖励同单位。 |

把n个旧样本总和写成n乘旧平均，再加入一个新样本，除以n+1，展开就得到增量形式。前两次奖励为1和3，旧平均为2；第三次得到8，新平均为2+(8−2)/3=4，与(1+3+8)/3一致。

贪心策略每次选择目前平均分最高的按钮。问题在于，“目前最高”也可能只是“早期运气最好”：一个本来不错的按钮第一次给出低分，之后就再也没有机会改善评价。ε-greedy 给每次选择留出一小部分随机探索概率，剩余概率用于选择当前最好的按钮。例如 ε 为 0.1、共有四个按钮时，每个按钮至少得到 0.025 的选择概率；当前唯一最优按钮还得到其余 0.9，因此总概率是 0.925。探索不是必定改选其他按钮，随机步骤也可能再次选中当前最优项。

UCB 把探索安排得更有针对性。它在平均分上加一个“还值得了解多少”的奖励：一个按钮被试过的次数越少，奖励通常越大；随着总选择次数增长，很久没有尝试的按钮也会重新获得关注。这个额外项不是餐馆本身的收益，而是选动作时使用的乐观分数。在下面的实验里，四个按钮的真实均值固定为 0.2、0.5、0.8、1.0，观测噪声的标准差都是 1。我们知道这些均值，是因为亲手生成了教学环境；学习算法每次只看得到自己选中按钮的一个带噪声样本。

$$
A_t=\operatorname*{arg\,max}_{a}\left[\widehat q_t(a)+\sqrt{\frac{2\ln t}{N_t(a)}}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/697849e3b4a294a61c884ddf.svg) | 第t次选择的动作编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 总选择次数；自然对数中的t为无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 待比较的动作编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/92f660195cb755b8afcb07a1.svg) | 到当前时刻该动作的平均奖励估计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/10dc61f0abc250b5fa83fc7d.svg) | 该动作此前的被选择次数，必须大于零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | 自然对数；探索奖励按本实验标准化奖励尺度计算。 |

先把每个按钮各选一次，避免分母为零；之后比较平均分加探索奖励。t=100、N=4、平均分0.5时，探索奖励约为1.517，总分约为2.017。这个分数用于比较动作，环境给出的实际奖励仍来自该按钮原来的分布。

图中的累计伪遗憾，逐次加总“最优按钮的均值减去实际所选按钮的均值”。它把决策质量与当次随机噪声分开，因此即使一顿普通午餐碰巧得到很高评分，也不会被算成找到了更优选项。32 个随机种子、每次 400 次选择的实验中，贪心、ε-greedy 和 UCB 的平均累计伪遗憾约为 96.84、42.13 和 37.38。右侧保留每次运行的一个点，可以看到平均值背后不同的经历。换成随时间变化的按钮均值时，样本平均可能反应过慢，此时需要窗口、常数步长或其他适应变化的办法。

![四个均值固定的合成按钮，32个种子，每个400次选择。左图曲线为平均累计伪遗憾，阴影为种子间四分位范围；右图每个点对应一次独立运行。噪声标准差为1。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b67638f6970e9a72e8c02466.svg?v=b67638f6970e)

图 2四个均值固定的合成按钮，32个种子，每个400次选择。左图曲线为平均累计伪遗憾，阴影为种子间四分位范围；右图每个点对应一次独立运行。噪声标准差为1。

## 给连续决策一张可以计算的地图

当动作改变下一步的位置，就要引入状态。一个马尔可夫决策过程（MDP）包括状态、动作、转移规律、奖励规律和折扣因子。状态应包含预测下一步所需的信息：格子世界的位置足够描述本章环境，而移动机器人的位置往往还不够，还需要速度、电量和障碍物观测。所谓马尔可夫性，是说在给定当前状态和动作后，更早的历史不再提供额外的转移信息。如果只告诉模型“在走廊中央”，却没有告诉它正朝哪边运动，那么状态设计就可能遗漏重要信息。

策略是从状态到动作分布的规则。确定性策略可以是一张每格一个箭头的地图，随机策略则给向上、右、下、左分别分配概率。奖励描述每一步的偏好；回报把一段未来的奖励汇总起来。两者不能混为一谈：朝着终点走的一步可能立刻得到负奖励，因为它消耗时间，但仍然带来更好的长期结果。折扣因子 γ 决定较远奖励的权重，既能表达对延迟的偏好，也能在无限持续任务中帮助回报保持有限。本章走格子是到终点结束的任务，训练代码采用 γ=1，直接累计整段路的奖励。

$$
G_t=\sum_{k=0}^{T-t-1}\gamma^kR_{t+k+1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33cb70bd20d03f7b40d90d58.svg) | 从时刻t之后开始累计的折扣回报，与奖励同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 本回合终止时刻，按动作步计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 当前时刻，按动作步计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 距离当前时刻的非负整数步数，求和索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 折扣因子，无量纲；本实验回合任务取1，交互规划可调。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6780ac06aa49cd1f2d595b2a.svg) | 完成第t+k次动作后收到的奖励。 |

第一步奖励乘1，第二步乘γ，第三步乘γ²，较远的奖励依次降权。奖励为−1、−1、10且γ=0.9时，回报为−1−0.9+8.1=6.2。若γ=1，则同一条轨迹回报为8；奖励没有变化，改变的是未来奖励如何汇总。

价值函数则给“处在这里、以后按某个策略行动”一个平均回报。状态价值 V 衡量当前位置，动作价值 Q 还把第一个动作指定下来。它们都是对未来随机性的期望，并不预言每一条实际路径。比如从同一个格子出发，有时探索动作会把学习者带到危险处，有时会一路顺利到达终点；价值函数把这些可能性按概率加权。因此，评价一个策略时，既可以问平均得分，也可以问失败概率和回报分布。业务若关心最坏情形，就需要把这种偏好明确放进目标或约束，而不能靠平均分替它作决定。

## 为什么长期问题能拆成一步

把一条路线的回报拆开，第一部分是下一步立即得到的奖励，第二部分是之后整段路线的折扣回报。第二部分与原问题具有相同结构，只是起点换到了下一个状态。这正是 Bellman 递推的出发点。它像规划一次多段火车旅行：若已经知道从每个中转站继续出发的最佳代价，就能比较先坐哪一班车。递推没有凭空消除未来，而是把未来浓缩在每个状态的价值中，让相邻状态交换信息。

$$
V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)\left[r(s,a,s')+\gamma V^*(s')\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 当前状态，例如格子位置。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | 可能的下一状态；求和遍历这些状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 当前可选动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0a36a87631d65297a8473b9.svg) | 从状态s采用最优策略的期望回报，与奖励同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/839101a417c5f6ac8aea5ab5.svg) | 给定状态与动作后的转移概率，各下一状态概率之和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ca32dc98c9920092714bd2f.svg) | 指定这次转移的期望即时奖励。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 无量纲折扣因子。 |

先对同一个动作可能导致的下一状态按概率加权，再比较不同动作。确定转移时，动作A给出−1并到达价值8的状态，动作B给出0.5并到达价值5的状态；γ=0.9时分别得到6.2和5，A更优。终止状态的后续价值设为0。

如果环境的转移概率和奖励已知，就可以直接计算这些平均值，这属于动态规划。策略评估固定“每个状态怎样选动作”，反复更新各状态的价值；策略改进再把动作换成当前看来更有利的选择。价值迭代则在每次更新里直接取最优动作。实现时要区分同步更新与原地更新：前者用上一轮整张表计算新表，便于观察价值一层层传播；后者可以立即利用本轮刚更新的数值，常常传播得更快。两种做法的中间轨迹不同，比较时应说明更新方式。

下面的交互实验使用已知的格子世界规则进行同步价值迭代。调节“动作偏移概率”会让本来想向右的动作有机会偏到上方或下方；靠近悬崖时，这种不确定性会改变安全路线的价值。每点一次“一轮更新”，所有格子同时用上一轮价值计算一次。把 γ 调为 0，可以检查算法是否只看即时奖励；继续提高 γ，远处终点和危险区域的影响才会逐步传播。这个实验强调的是已知模型的规划；后面的 Q-learning 则通过实际走到的转移更新表格。

## 亲手传播一张价值地图

先点一轮更新，观察即时奖励，再连续推进30轮。滑移概率表示本来打算执行的动作偏到两个垂直方向的总概率，两边各占一半。改变参数后，会按当前轮数重新计算整张价值表。

初始价值为0。

[Figure: 格子世界价值和策略地图](https://ml-biomat.com/tutorials/machine-learning/m24/#M24-lab)

终止格子的后续价值为0。此处使用已知转移规则计算期望，是动态规划；Python实验中的学习者则只从实际经历的一步更新Q表。

## 从一次旅程的结局，到下一次预测

在许多任务里，转移规律并没有事先给出。学习者可以完成一整回合后，把实际回报当成价值的训练目标，这就是 Monte Carlo 思路。它使用的是走完之后看到的结果，目标中没有尚未兑现的价值预测，但一条长路径可能包含许多随机事件，回报的波动也会较大。若任务很长，等待整段结束还会延迟更新。这里自然出现一个问题：能否在每走一步之后，便利用新增的信息改善刚才的判断？

时序差分（TD）学习用“即时奖励加下一状态的当前价值”代替整段尚未观察到的回报，目标与旧预测之差就是 TD 误差。它一边使用价值估计，一边更新价值估计，这种用已有预测帮助构造目标的方式叫自举。Sutton 在 1988 年的论文中系统讨论了相邻时刻预测之间的差异怎样驱动学习。理解这段历史的重点是问题如何改变：从等待结局后纠错，变成利用中途新得到的一次预测纠错。网络多大并不是这个思想成立的前提，一张数值表就能展示它。

$$
V(s)\leftarrow V(s)+\alpha\left[r+\gamma(1-d)V(s')-V(s)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 当前状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | 本次实际到达的下一状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 本次即时奖励，与价值同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 学习步长，0到1之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 无量纲折扣因子。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 真正终止时为1，否则为0；计算步数上限不自动设为终止。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 当前状态价值表，与奖励同单位。 |

方括号是一次TD误差：新的单步目标减旧预测。取旧值2、奖励1、下一价值4、γ=0.9、α=0.2且未终止，目标4.6，更新后2.52。若该步终止，目标为1，更新后为1.8。

如果某格旧价值为 2，下一步奖励为 1，下一格价值为 4，γ=0.9，那么本次目标是 4.6，TD 误差是 2.6。使用步长 0.2 后，旧值向目标移动五分之一，变成 2.52。步长控制信息吸收的速度，折扣控制未来奖励的权重，两者在公式中都像系数，承担的职责却不同。到达真正的终止状态时，未来部分取零；如果只是因为演示的最大步数而暂停，环境任务本身仍可能继续，此时不应把暂停机械地当作终止。本章代码把达到终点与达到运行步数上限分开处理。

## SARSA 与 Q-learning 学的是什么

从预测进入控制，只需要让价值表区分不同动作，并让新的价值反过来影响选动作。SARSA 的名字对应一条五元经验：当前状态、当前动作、奖励、下一状态、下一动作。它用下一步实际会按当前策略选择的动作价值构造目标。因此，当策略保留探索概率时，SARSA 评估的也包括这些探索动作带来的风险。这里的 on-policy 指学习的目标策略与收集经验的行为策略一致；它描述的是数据和目标的关系，而不是算法是否实时运行。

$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma(1-d)Q(s',a')-Q(s,a)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 当前状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | 本次实际到达的下一状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 本次即时奖励，与价值同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 学习步长，0到1之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 无量纲折扣因子。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 真正终止时为1，否则为0；计算步数上限不自动设为终止。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 当前动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/36b400f98b136a84c0280fc3.svg) | 下一状态按当前行为策略实际选出的动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 状态动作价值表，每项与奖励同单位。 |

SARSA沿实际策略选择的下一动作计算目标。若旧Q为2、奖励1、下一次选中动作的Q为1、γ=0.9、α=0.2，目标为1.9，新Q为1.98；即便下一状态另一个动作的Q为4，这次SARSA更新仍使用已经选中的动作。

Q-learning 在下一状态直接选取最大的动作价值构造目标，即使收集经验时仍然使用 ε-greedy。它学习的是后续采用贪心选择时的目标，而行为中仍可能含有随机动作，所以属于 off-policy。Watkins 与 Dayan 在 1992 年的论文中给出了表格情形的收敛结果；理论讨论需要持续访问状态动作和合适的学习率条件。本章固定步长、有限回合的实验展示学习行为，我们直接检查得到的路径和回报，而不把一条趋稳曲线当成收敛定理的验证。

$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma(1-d)\max_bQ(s',b)-Q(s,a)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 当前状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | 本次实际到达的下一状态。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 本次即时奖励，与价值同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 学习步长，0到1之间，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 无量纲折扣因子。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 真正终止时为1，否则为0；计算步数上限不自动设为终止。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 当前动作。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 下一状态全部可选动作的遍历索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 状态动作价值表，与奖励同单位。 |

Q-learning用下一状态最大的动作价值构造目标。沿用上例，若最大Q为4，则目标4.6，新Q为2.52；实际随后是否随机选了其他动作，不改变这一次更新的目标。到达终点时未来项为零。

悬崖任务让两种目标的差别变得直观：底行中央十个格子是悬崖，跌入后得到 −100 并回到起点，其余每步奖励为 −1，到达右下角终点结束。贪心执行时，贴着悬崖上方走可以缩短路径；保留探索时，一次随机向下却可能付出很大代价。Q-learning 可以学到一条很短的贪心路线，而 SARSA 往往会把探索风险算进价值，留出距离。评价时必须区分“训练期间含探索的行为回报”和“训练后关闭探索的贪心路线”，否则同一张图很容易被读成互相矛盾的结论。

## 把目标、路径和回报放在同一实验里

完整程序同时运行按钮选择和悬崖走格子。走格子部分使用 8 个随机种子，每个算法各训练 500 回合，ε=0.1，步长为 0.5。平局时随机选取一个最大值动作，避免全零初始化时总是偏向数组里的第一个方向。环境函数只负责给出下一状态、奖励和是否到终点，学习函数则负责更新价值；这种分离使同一个环境能够支持 SARSA、Q-learning 和不同的策略。代码中的手算断言检查了一次悬崖转移、一次到达终点和一次 TD 更新，便于先确定规则正确再解释训练曲线。

### 完整实验：按钮探索与悬崖边控制

依赖NumPy和Matplotlib。保存为main.py，运行python main.py --output results --language zh；改为en得到英文图。函数transition定义环境，learn完成实际TD控制，bandit比较探索方式。输出summary.json和NPZ保存数据，三幅SVG由同一轮计算生成。

```
"""Tabular reinforcement learning: bandits and the cliff-walking task.

Run: python main.py --output results --language en
Requires NumPy and Matplotlib. All data are synthetic and generated here.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BLUE, RED, GOLD = '#176b91', '#b04743', '#c18a28'
START, GOAL, ROWS, COLS = 36, 47, 4, 12
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def transition(state, action):
    row, col = divmod(int(state), COLS)
    dr, dc = MOVES[int(action)]
    row, col = np.clip(row + dr, 0, ROWS-1), np.clip(col + dc, 0, COLS-1)
    next_state = int(row * COLS + col)
    if row == 3 and 0 < col < 11:
        return START, -100., False
    return next_state, -1., next_state == GOAL


def choose(q, rng, epsilon):
    if rng.random() < epsilon:
        return int(rng.integers(len(q)))
    ties = np.flatnonzero(np.isclose(q, q.max(), rtol=0, atol=1e-12))
    return int(rng.choice(ties))


def learn(method, seed, episodes=500, epsilon=.1, alpha=.5, gamma=1.):
    rng = np.random.default_rng(seed)
    q = np.zeros((ROWS * COLS, 4))
    returns, falls, lengths = [], [], []
    for _ in range(episodes):
        state = START
        action = choose(q[state], rng, epsilon)
        total, dropped = 0., 0
        for step in range(600):
            nxt, reward, done = transition(state, action)
            next_action = choose(q[nxt], rng, epsilon)
            future = q[nxt].max() if method == 'Q-learning' else q[nxt, next_action]
            target = reward if done else reward + gamma * future
            q[state, action] += alpha * (target - q[state, action])
            total += reward
            dropped += int(reward == -100)
            state, action = nxt, next_action
            if done:
                break
        returns.append(total); falls.append(dropped); lengths.append(step + 1)
    return q, np.array(returns), np.array(falls), np.array(lengths)


def greedy_route(q):
    state, path, total = START, [START], 0.
    for _ in range(100):
        state, reward, done = transition(state, int(q[state].argmax()))
        path.append(state); total += reward
        if done:
            return path, total, True
    return path, total, False


def bandit(method, seed, steps=400):
    means = np.array([.2, .5, .8, 1.])
    rng = np.random.default_rng(seed)
    q, counts = np.zeros(4), np.zeros(4, dtype=int)
    gaps = []
    for t in range(steps):
        if method == 'UCB':
            action = t if t < 4 else int(np.argmax(q + np.sqrt(2*np.log(t+1)/counts)))
        else:
            action = choose(q, rng, .1 if method == 'epsilon' else 0.)
        reward = means[action] + rng.normal(0, 1)
        counts[action] += 1
        q[action] += (reward - q[action]) / counts[action]
        gaps.append(means.max()-means[action])
    return np.cumsum(gaps), counts


def configure(language):
    plt.rcParams.update({'font.family':'sans-serif', 'font.sans-serif':['Microsoft YaHei','Arial'],
                         'font.size':11, 'axes.spines.top':False, 'axes.spines.right':False,
                         'svg.fonttype':'none', 'pdf.fonttype':42, 'axes.unicode_minus':False,
                         'figure.facecolor':'white', 'axes.facecolor':'white'})


def loop_figure(out, zh):
    fig, ax = plt.subplots(figsize=(11, 4.5)); ax.set(xlim=(0,11), ylim=(0,4.5)); ax.axis('off')
    boxes=[(1,2.0,3,1.2,'学习者：选择动作\n策略与价值估计' if zh else 'Agent: choose action\nPolicy and value estimates',BLUE),
           (7,2.0,3,1.2,'环境：回应动作\n位置变化与奖励' if zh else 'Environment: respond\nNew position and reward',RED)]
    for x,y,w,h,label,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.12',facecolor=color,edgecolor='none'))
        ax.text(x+w/2,y+h/2,label,color='white',ha='center',va='center',fontsize=13,linespacing=1.6)
    ax.add_patch(FancyArrowPatch((4.2,2.9),(6.8,2.9),arrowstyle='-|>',mutation_scale=18,color=BLUE,lw=2))
    ax.add_patch(FancyArrowPatch((6.8,2.25),(4.2,2.25),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2))
    ax.text(5.5,3.18,'动作 a(t)' if zh else 'Action a(t)',ha='center')
    ax.text(5.5,1.8,'奖励 r(t+1)，状态 s(t+1)' if zh else 'Reward r(t+1), state s(t+1)',ha='center')
    for x,year,text in [(1.1,'规划 / Planning','已知转移，计算价值' if zh else 'Known transitions → values'),(4.3,'1988 · TD','由下一次预测更新' if zh else 'Learn from the next prediction'),(7.5,'1992 · Q-learning','由经验改进动作价值' if zh else 'Improve action values from experience')]:
        ax.text(x,.9,year,color=BLUE,fontweight='bold');ax.text(x,.42,text,fontsize=10)
    fig.tight_layout();fig.savefig(out/f'loop-{lang(zh)}.svg');fig.savefig(out/f'loop-{lang(zh)}.png',dpi=150);plt.close(fig)


def lang(zh):
    return 'zh' if zh else 'en'


def make_figures(out, zh, runs, routes, bandits):
    fig, axes = plt.subplots(1,2,figsize=(11,4.4),gridspec_kw={'width_ratios':[1.45,1]})
    for method,color,label in [('greedy',GOLD,'贪心' if zh else 'Greedy'),('epsilon',RED,'ε=0.1'),('UCB',BLUE,'UCB')]:
        regrets=np.stack([x[0] for x in bandits[method]])
        axes[0].plot(np.arange(1,401),regrets.mean(0),color=color,label=label,lw=2)
        lo,hi=np.quantile(regrets,[.25,.75],axis=0);axes[0].fill_between(np.arange(1,401),lo,hi,color=color,alpha=.12)
        x={'greedy':0,'epsilon':1,'UCB':2}[method]
        axes[1].scatter(np.full(len(regrets),x)+np.linspace(-.12,.12,len(regrets)),regrets[:,-1],c=color,alpha=.65,s=24)
    axes[0].set(xlabel='选择次数' if zh else 'Number of choices',ylabel='累计伪遗憾（奖励单位）' if zh else 'Cumulative pseudo-regret (reward units)');axes[0].legend(frameon=False)
    axes[1].set(xticks=[0,1,2],xticklabels=['贪心' if zh else 'Greedy','ε=0.1','UCB'],ylabel='第400步的累计伪遗憾' if zh else 'Pseudo-regret after 400 choices')
    fig.tight_layout();fig.savefig(out/f'bandits-{lang(zh)}.svg');fig.savefig(out/f'bandits-{lang(zh)}.png',dpi=150);plt.close(fig)
    fig=plt.figure(figsize=(12,7.4));gs=fig.add_gridspec(2,2,height_ratios=[1,1.4],hspace=.5,wspace=.3)
    for j,(method,color) in enumerate([('Q-learning',BLUE),('SARSA',RED)]):
        ax=fig.add_subplot(gs[0,j]);ax.set(xlim=(-.5,11.5),ylim=(3.5,-.5),aspect='equal',xticks=range(12),yticks=range(4))
        for row in range(4):
            for col in range(12):
                face='#efc9c7' if row==3 and 0<col<11 else '#f1f4f5'
                ax.add_patch(Rectangle((col-.48,row-.48),.96,.96,facecolor=face,edgecolor='white'))
        path=routes[method][0];pos=np.array([divmod(s,12) for s in path]);ax.plot(pos[:,1],pos[:,0],color=color,lw=2.3,marker='o',ms=3)
        ax.text(0,3,'S',ha='center',va='center',fontweight='bold');ax.text(11,3,'G',ha='center',va='center',fontweight='bold')
        ax.set_title(method+' · '+('种子0的贪心路径' if zh else 'greedy route, seed 0'));ax.set_xlabel('列' if zh else 'Column');ax.set_ylabel('行' if zh else 'Row')
    ax=fig.add_subplot(gs[1,0]);bx=fig.add_subplot(gs[1,1])
    for j,(method,color) in enumerate([('Q-learning',BLUE),('SARSA',RED)]):
        returns=np.stack([x[1] for x in runs[method]])
        blocks=returns.reshape(len(returns),25,20).mean(2)
        lo,hi=np.quantile(blocks,[.25,.75],axis=0)
        ax.plot(np.arange(20,501,20),blocks.mean(0),color=color,lw=2,label=method)
        ax.fill_between(np.arange(20,501,20),lo,hi,color=color,alpha=.15)
        scores=returns[:,-100:].mean(1);bx.scatter(j+np.linspace(-.12,.12,len(scores)),scores,c=color,s=35)
        bx.plot([j-.2,j+.2],[scores.mean()]*2,color=color,lw=2)
    ax.set(xlabel='训练回合（20回合分组）' if zh else 'Training episode (20-episode blocks)',ylabel='平均未折扣回报' if zh else 'Mean undiscounted return');ax.legend(frameon=False)
    bx.set(xticks=[0,1],xticklabels=['Q-learning','SARSA'],ylabel='末100回合平均回报' if zh else 'Mean return, last 100 episodes')
    fig.savefig(out/f'cliff-{lang(zh)}.svg',bbox_inches='tight');fig.savefig(out/f'cliff-{lang(zh)}.png',dpi=150,bbox_inches='tight');plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh';configure(args.language)
    assert transition(START,1)==(START,-100.,False)
    assert transition(35,2)==(GOAL,-1.,True)
    assert abs(2+.2*(1+.9*4-2)-2.52)<1e-12
    runs={m:[learn(m,s) for s in range(8)] for m in ['Q-learning','SARSA']}
    routes={m:greedy_route(runs[m][0][0]) for m in runs}
    bandits={m:[bandit(m,s) for s in range(32)] for m in ['greedy','epsilon','UCB']}
    summary={'seeds':list(range(8)),'episodes':500,'epsilon':.1,'alpha':.5,'gamma':1.,'max_steps':600,'hand_update':2.52,'algorithms':{}}
    for m,results in runs.items():
        summary['algorithms'][m]={'last100_mean_return':float(np.mean([r[1][-100:].mean() for r in results])),
          'last100_falls_per_episode':float(np.mean([r[2][-100:].mean() for r in results])),
          'greedy_seed0_return':routes[m][1],'greedy_seed0_reached_goal':routes[m][2],'greedy_seed0_steps':len(routes[m][0])-1,
          'capped_episodes':int(sum((r[3]==600).sum() for r in results))}
        np.savez(args.output/f'{m.replace("-","")}-data.npz',returns=np.stack([r[1] for r in results]),q=np.stack([r[0] for r in results]),falls=np.stack([r[2] for r in results]))
    summary['bandit_final_pseudoregret']={m:float(np.mean([r[0][-1] for r in xs])) for m,xs in bandits.items()}
    loop_figure(args.output,zh);make_figures(args.output,zh,runs,routes,bandits)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

上排显示种子 0 的训练后贪心路径：Q-learning 用 13 步到达终点，SARSA 用 17 步。下排左侧把训练期间的回报每 20 回合分组，曲线是 8 个种子的平均值，阴影为种子之间的四分位范围。右侧则让每个种子的末 100 回合平均回报各占一个点，短横线标出均值。Q-learning 和 SARSA 在这个设置下的末段平均回报分别约为 −49.66 和 −27.06；相应每回合平均跌落次数约为 0.330 和 0.045。较短的贪心路径与较差的探索行为回报可以同时成立，因为它们评价的是不同策略。

![上排为种子0的训练后贪心路径，下排为持续ε=0.1探索的训练回报。两种算法各8个种子、500回合；阴影为种子间四分位范围，右下点为末100回合均值。路径与训练曲线对应不同评价策略。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6975afc92dc9b0633cbb27de.svg?v=6975afc92dc9)

图 3上排为种子0的训练后贪心路径，下排为持续ε=0.1探索的训练回报。两种算法各8个种子、500回合；阴影为种子间四分位范围，右下点为末100回合均值。路径与训练曲线对应不同评价策略。

每个算法在全部 4000 个训练回合中都出现过一次触及 600 步上限的回合，代码保存了这个计数。回报曲线按实际收集的步数统计，末段比较仍采用相同回合窗口；若比较样本效率，还应进一步以环境交互次数作为横轴，因为不同策略走完一回合需要的步数不同。把 ε 改成 0 后重新训练，会改变探索数据的覆盖；只在训练结束后把执行策略改成贪心，则保留原有训练数据。这个小修改非常适合检查你是否真正区分了行为策略、学习目标与评价策略。

## 从格子世界带走的实验习惯

奖励设计决定学习者努力优化什么。若给机器人“每接近目标一米就加分”，需要检查来回移动是否能够重复获取奖励；若只惩罚耗时，却没有表达碰撞代价，最快路线可能并非期望路线。稠密奖励可以帮助学习，但也可能改变任务偏好。基于势函数的奖励塑形提供一种有条件保持策略排序的构造：为状态设置一个势，额外奖励取下一状态折扣势与当前势的差。把这种额外奖励沿轨迹相加，中间项会抵消；相应结论仍依赖折扣和终止状态的处理是否一致。

评价的最小单位也要与问题匹配。按钮实验的一次运行包含 400 次选择，走格子的一次运行包含 500 回合；随机种子代表独立重复的随机选择过程。将同一条学习曲线上的 500 个回合当作 500 次独立实验，会低估训练轨迹的相关性。比较算法时应固定环境、训练预算、评价方式和调参规则，再报告种子间分布。用于挑参数的环境回合和最后报告效果的评价回合也应分开。面对真实系统，先在可检查的仿真和已有数据中确认奖励、状态与动作定义，再逐渐扩大交互范围。

还可以做一个完全手算的小实验：把到终点之前的一条路线写成三个状态，最后一步奖励为10，前两步奖励为0，所有价值先设为0。Monte Carlo在走完整条路线后，立刻把同一回报按折扣分配给沿途状态；单步TD先让靠近终点的状态得到信息，再靠后续访问把信息传向起点。若改用已知转移的同步价值迭代，奖励信息每一轮同样只能向前传播有限距离。把这三种传播方式画在同一张纸上，就能清楚区分“经验是否已走完”“是否使用当前预测”和“是否知道完整转移规律”这三个独立问题。

读到这里，你应能把一个连续决策任务写成状态、动作、奖励和转移，说明价值为何能递推，手算一次 TD、SARSA 或 Q-learning 更新，并从路径与回报图里判断它们各自在优化什么。接下来的深度强化学习会用神经网络替换价值表，并加入回放、目标网络或策略梯度。表格实验中建立的习惯仍然保留：先把任务说清楚，把目标算清楚，再让每条训练曲线对应真实收集到的经验。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M24.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning — Q-Learning](https://d2l.ai/chapter_reinforcement-learning/qlearning.html)

   探索、动作价值与表格实现。

   CC BY-SA 4.0 (book text and original figures)
2. [Gymnasium — Cliff Walking](https://gymnasium.farama.org/environments/toy_text/cliff_walking/)

   悬崖环境的位置、动作、奖励和终止规则。
3. [Sutton (1988), Learning to predict by the methods of temporal differences](https://link.springer.com/article/10.1007/BF00115009)

   相邻时刻预测差异的学习方法与历史背景。

   Original paper reference
4. [Watkins and Dayan (1992), Q-learning](https://link.springer.com/article/10.1007/BF00992698)

   Q-learning的表格收敛条件与动态规划联系。

   Original paper reference
