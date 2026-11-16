# 让噪声沿速度场走向数据：Flow Matching与Rectified Flow

Source: https://ml-biomat.com/tutorials/machine-learning/m41/
Language: zh-CN

区分训练线段与实际轨迹，用配对、Reflow和求解器解释生成速度与精度。

## 给一群点安排方向，让它们组成图案

想象一场无人机表演：开始时，许多光点散在空中，随后逐渐形成三片弯曲的风车叶片。若给每架无人机指定终点，再让它沿直线飞过去，任务似乎已经完成。但生成模型面临的情况略有不同：我们拥有许多目标图案中的位置样本，也能随机产生起点，却没有天然的一一配对。模型要学会的是，在某个时刻、某个位置，应该向哪里移动，才能让整群点的分布逐渐变成目标分布。

Flow Matching把这个问题组织成速度预测。先构造容易抽样的路径，在路径上随机挑一个位置和时刻，把该处应该采用的速度作为训练答案。网络学好后，从新的随机起点出发，反复查询速度并向前积分，就能生成新样本。这个思路适合图像、声音、轨迹等连续表示，也适合把一种分布转换为另一种分布。它把“怎样训练一个生成器”变成了一个有明确输入和数值标签的回归问题。

理解时需要同时看两幅画：一幅是训练时构造的路径，另一幅是模型实际积分得到的路径。训练线段可以笔直，学出的轨迹仍然会转弯；速度损失可以很低，最终分布仍可能漏掉一部分区域。本章用三叶风车点云把这些差别展开，并比较独立配对、小批次最优匹配、再次训练的Reflow和带叶片条件的生成。每一种方法都实际训练，轨迹与评价使用同一组新起点。

![八团高斯向双月分布变化的CFM与OT-CFM密度、速度和粒子对照。](https://ml-biomat.com/static/tutorials/machine-learning/figures/7c604f4a70ace0ff466d7153.png?v=7c604f4a70ac)

图 1TorchCFM原始动画的三个时刻，选取CFM与OT-CFM两列：各时刻自上而下为密度、速度场和粒子轨迹，展示八团高斯向双月分布的变化。Alexander Tong与TorchCFM贡献者，MIT许可；裁切并重新编排第0、55、110帧，原版权和许可随图保留。这是原教程实验。

## 一条路径怎样产生位置、时间与速度标签

最容易计算的路径，是连接起点与终点的直线。把生成时间规定为0到1，时间0位于噪声端，时间1位于数据端，中间位置就是两个端点的加权平均。这里的时间是一根控制生成进度的刻度，并非无人机真实飞行的秒数。若每次把整条线段走完都需要一个单位时间，速度就是终点减起点；这个向量同时给出方向与每单位生成时间走过的距离。

$$
x_t=(1-t)x_0+tx_1,\qquad u_t(x_0,x_1)=\frac{d x_t}{dt}=x_1-x_0,\qquad t\sim\mathcal U(0,1)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2337d07ffc05a0636ede060.svg) | 噪声端点、数据端点与中间位置，均为d维向量；本例d=2，坐标无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6cf8706468163f4cc00255a7.svg) | 归一化生成时间、0至1均匀分布、条件路径速度与对时间求导；速度单位为坐标/生成时间。 |

位置是两个端点的线性加权；求导时端点保持固定，因此−x₀+x₁就是速度。x₀=(0,0)、x₁=(2,1)、t=0.25时，位置为(0.5,0.25)，速度(2,1)。若把相同路程改成5秒物理运动，物理速度应为(0.4,0.2)/秒，不能把归一化时间直接当秒。

取起点(0,0)、终点(2,1)，四分之一时刻的位置为(0.5,0.25)，速度始终为(2,1)。因此训练样本很容易制造：抽取端点，抽取一个0到1之间的时间，直接算出位置和速度。无需先把前面四分之一的轨迹逐步模拟出来，也无需在训练时求解一个完整常微分方程。这正是“无需模拟的训练”在这里的具体含义；生成新样本时，仍需要求解网络定义的运动过程。

许多这样的线段一起运动，会在每个时刻形成一群点。这群点的概率分布随时间变化，叫概率路径。若起点服从标准高斯、终点来自训练数据，那么时间0和1的分布就已确定，中间分布由配对方式与插值规则共同决定。线性插值只是一个方便的选择；也可以用随时间变化的信号与噪声系数构造曲线路径。先把端点、路径与时间约定写清楚，才能知道网络真正拟合的量。

即使两个端点分布一样，中间分布也可能改变。设一维起点和终点都是独立标准高斯，取一半起点加一半终点，中间方差就是两个0.25之和，即0.5，比端点方差1更窄。若改成让每个终点等于自己的起点，整条路径都不动，方差便始终为1。这两个小实验拥有相同端点分布，却呈现不同的中途收缩；耦合所改变的不只是画面中的连线，还包括网络沿途要搬运的概率分布。

## 交叉路口只有一个速度，为什么还能搬运整群点

独立抽取起点和终点，会得到许多相互穿过的线段。若两条线在同一时刻经过相同位置，却要求两个不同方向，一个只接收位置和时间的网络无法同时返回两个答案。平方误差的最佳办法是返回条件平均：把所有在该时刻、该位置可能出现的路径速度，按其可能性加权。平均是针对当前位置形成的局部判断，不是对整个数据集只算一个总方向。

$$
L_{\rm CFM}(\theta)=\mathbb E\!\left[\frac1d\|v_\theta(x_t,t)-u_t\|^2\right],\qquad v^*(x,t)=\mathbb E[u_t\mid x_t=x,t]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0438b4b9edaa3075aad08d79.svg) | 网络预测的d维速度、网络参数和平方误差下的最佳条件平均速度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d45451db65f0237ead2f8e9f.svg) | 对端点配对及时间求平均、条件路径速度、中间位置、时间、维度和逐分量平方和。 |
| ![Formula](https://ml-biomat.com/static/agent-math/32a003be033473682af6ff34.svg) | 按坐标平均的条件Flow Matching损失与“给定”条件；损失单位为速度的平方。 |

把速度写成条件均值加零均值残差，展开平方后交叉项平均为0，损失便分成网络对条件均值的误差和无法由当前输入解释的方差。两个等概率标签(2,0)、(0,2)的最佳预测为(1,1)，每坐标平均损失为1；非零最小损失来自标签差异。实际训练不同耦合的这个方差也不同。

例如同一位置有两种等概率速度(2,0)与(0,2)，它们的最佳平方误差预测是(1,1)。沿这个平均方向走的粒子，会在随后时刻再次查询速度，因而一般不会继续沿原来某条训练线段运动。训练标签记得自己配对的终点，网络只知道当前状态；这一区别解释了为什么“训练用直线”不能直接推出“生成只需一大步”。图中独立配对的线段大量交叉，实际积分轨迹则随位置与时间逐步改变方向。

这还解释了本章独立配对模型的一步结果为何挤向中心。在时间0，独立抽取的终点与给定起点无关，所以理想速度等于目标均值减去当前起点。若直接用一个长度为1的Euler步，起点与负起点相消，所有点都被送到目标均值附近。逐步积分则会持续利用中途位置提供的新信息，逐渐把人群分向不同叶片。OT与Reflow使端点依赖起点，时间0的条件平均因此不再被迫采用同一个目标均值。

![相同24组起终点分别独立连接与最小平方成本匹配；右图是另一组固定起点通过独立配对网络得到的真实ODE轨迹。空心点标起点，实心橙点标训练终点，坐标无量纲。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6520760d64d88220206599e6.svg?v=6520760d64d8)

图 2相同24组起终点分别独立连接与最小平方成本匹配；右图是另一组固定起点通过独立配对网络得到的真实ODE轨迹。空心点标起点，实心橙点标训练终点，坐标无量纲。

局部平均仍能产生正确概率路径，其原因可以从流入与流出理解。在一个很小的区域里，决定粒子数量怎样变化的是穿过边界的平均流量，而不是每个粒子的姓名。条件平均速度保持了这份平均流量，因此在精确学习及合适的解存在条件下，可以保持所构造路径的各时刻分布。光滑、具有唯一解的速度场不会让两条轨迹在同一时刻同一位置分叉；在平面投影中不同时刻经过同一点，则完全可能。

$$
\frac{\partial p_t(x)}{\partial t}+\nabla_x\!\cdot\!\big[p_t(x)v(x,t)\big]=0,\qquad \frac{dz_t}{dt}=v(z_t,t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/58d7f37513126ee9d3605676.svg) | 位置x处的概率密度、d维坐标和生成时间；密度单位为坐标体积的倒数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d210ccd5a1479c85e1b122f.svg) | 速度场、概率通量与散度（各坐标通量变化率之和）。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cd7dd1123c2b03722096ac5a.svg) | ODE实际轨迹、固定位置的时间偏导与沿轨迹的全导数。 |

小区域的概率减少量等于净流出量；局部平均速度保持通量，便保持各时刻分布。均匀密度在恒定速度场中平移时，区域内通量散度为0，密度不变。若速度随位置张开，流出大于流入，密度下降。ODE的唯一解条件用于区分同一时刻不能分叉与不同时刻可经过同一点。

![独立配对与小批次OT在t=0、0.5、1的实际粒子位置与网络速度场。蓝点为固定前500个生成粒子，淡橙点为固定300个测试目标；所有箭头使用同一缩放。](https://ml-biomat.com/static/tutorials/machine-learning/figures/7b31daddcdb44112c5739858.svg?v=7b31daddcdb4)

图 3独立配对与小批次OT在t=0、0.5、1的实际粒子位置与网络速度场。蓝点为固定前500个生成粒子，淡橙点为固定300个测试目标；所有箭头使用同一缩放。

## 先把起点和终点配得合理一些

配对方式叫耦合。两种耦合可以拥有完全相同的一组起点和终点，却让搬运路线截然不同。设两个起点是(−1,0)、(1,0)，终点按顺序是(1,1)、(−1,1)。按原顺序连接，两条路线交叉，平均平方距离为5；交换终点后，两条路线都竖直向上，平均平方距离降为1。两侧分布没有变化，变化的是谁和谁连接，以及沿途训练速度的复杂程度。

$$
\pi^*=\arg\min_{\pi\in S_B}\frac1B\sum_{i=1}^{B}\|a_i-b_{\pi(i)}\|^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8416f2a80d4385b5f4add97f.svg) | 批大小、样本索引、d维噪声起点与d维数据终点；训练B=128。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9f98c39eb3bed43f5aeaf29a.svg) | 所有B项排列、一个一对一匹配、成本最小的匹配与选择最小值位置的运算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/40ce8c99eb6c6b3590d8d679.svg) | 平方欧氏距离与批平均；成本单位为坐标的平方。 |

起点a=[(−1,0),(1,0)]、终点b=[(1,1),(−1,1)]给出成本矩阵[[5,1],[1,5]]。按顺序平均成本5，交换终点平均成本1。线性指派算法保留每个端点恰好一次，在该批中找到最小成本；批匹配与完整分布的全局最优传输是不同尺度的问题。

本例的OT版本在每批128个起点与128个数据点之间计算所有平方距离，再求一对一匹配，使这批点的总成本最小。每个终点仍使用一次，保持了该批的经验分布。图中的24点示意，平均平方距离从2.846降到0.627。这里优化的是小批次中的配对；换一批点，匹配也会变化，不能把它理解为已经求得两个完整连续分布之间的全局最优搬运。

2022年的Flow Matching工作把概率路径与速度回归联系起来，随后的小批次最优传输方法进一步研究怎样通过配对改善学习。这个发展顺序对应两个不同问题：先获得可计算的训练目标，再改善目标所包含的路线。比较时还要留意，独立配对与OT配对的速度标签分布不同，所以它们的验证速度误差不能直接当作同一把生成质量尺。本章会另外比较真实积分后的分布与路径弯曲程度。

## Rectified Flow：让已经学会的路线再直一些

Rectified Flow也从直线插值与速度回归出发，尤其关心由此得到的确定性配对，以及怎样进一步拉直生成路线。2022年的相关工作提出Reflow：先用一个已训练的速度场，从新起点积分到终点；保存这些实际起终点，再用它们之间的直线训练第二个速度场。第一次训练使用的是任意配对，第二次则继承了第一个模型已经形成的对应关系。

$$
z_1=\Phi_{v^{(k)}}(z_0),\qquad \tilde x_t=(1-t)z_0+tz_1,\qquad \tilde u=z_1-z_0,\qquad v^{(k+1)}\leftarrow\operatorname{Fit}(\tilde x_t,t,\tilde u)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5c9c71a539128c2c36e4ac1.svg) | Reflow轮次、教师速度场与下一轮学生速度场；与ODE内部时间不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fc15703225552a6ecf429650.svg) | 把教师ODE从0积到1的映射、随机起点和教师生成终点。 |
| ![Formula](https://ml-biomat.com/static/agent-math/515cff3ac5beb1aca8f634b1.svg) | 新直线训练位置、新速度标签、生成时间和按前述平方目标训练的操作；形状均为d维。 |

若教师把z₀=(−1,0)送到z₁=(0,2)，第二轮t=0.5的训练位置为(−0.5,1)，速度标签(1,2)。学生学习教师起终点的直连关系，而非教师沿途每一处弯曲速度。数值教师终点与学习误差都会影响下一轮分布；本例保留全部教师配对用于检查。

这个过程可以类比重新设计通勤路线。第一轮先让人群找到能到达目的地的路线；第二轮记录实际出发地与到达地，再尝试在保持这种对应的基础上减少绕行。它与直接把教师终点回归成一个一步网络仍有区别：Reflow继续学习带时间输入的速度场，生成时仍可以选择多步积分。若想得到直接一步映射，还可在这些起终点对上进行专门蒸馏。

实验从独立配对模型出发，用64步Heun生成2,048组训练起终点和512组验证起终点，再训练一个新网络。平均轨迹长度减去直线弦长，从约0.3965降到0.00133，路线明显变直；一步Euler生成的投影分布距离从0.5739降到0.0852。不过Reflow细步结果与真实测试分布的距离为0.0791，教师为0.0729。它学的是教师形成的端点分布，因此路线更直与更接近真实数据是两个需要分别测量的目标。

![前三个无条件模型在一步Euler、四步Euler、八步Heun和128步RK4参考下的前500个固定输出。各行起点相同，坐标范围统一；参考解是模型自己的数值解。](https://ml-biomat.com/static/tutorials/machine-learning/figures/a3c8ac8f96eef50cf0547b1d.svg?v=a3c8ac8f96ee)

图 4前三个无条件模型在一步Euler、四步Euler、八步Heun和128步RK4参考下的前500个固定输出。各行起点相同，坐标范围统一；参考解是模型自己的数值解。

## 用几次速度查询，换来多准确的一段运动

网络给出的是某一时刻的速度，求解器负责把速度积成位置。Euler方法先查当前速度，再按步长向前走；如果路途中速度改变，这一步就会偏离真实解。Heun方法先做一次Euler预测，在预测终点再查一次速度，取起终两次速度的平均来修正。经典RK4进一步在两个中间位置和终点取值，用四次查询组合出一小步。每步的精度与每步的计算代价因此同时变化。

$$
x_{n+1}^{\rm Euler}=x_n+h\,v(x_n,t_n),\qquad \tilde x=x_n+h\,v(x_n,t_n),\qquad x_{n+1}^{\rm Heun}=x_n+\frac h2\big[v(x_n,t_n)+v(\tilde x,t_n+h)\big]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/880884186ce6b52872048e8b.svg) | 求解步索引、步长、当前生成时间与d维状态；均匀N步时h=1/N、t_n=nh。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca42b4fdc1565280331cdddb.svg) | Euler临时预测、速度网络和更新后的状态；h乘速度得到坐标增量。 |

对dx/dt=x，x₀=1，整段h=1，Euler得到2；Heun先预测2，再用速度1与2的平均，得到2.5。真实值e≈2.71828。RK4在每一步另外评估两个半步状态，使用1:2:2:1权重组合四个速度；本章代码逐项实现，16次查询可分配为Euler16、Heun8或RK4四步。

一个能手算的例子是速度等于当前位置，初始位置为1。从时间0走到1，解析终点为自然常数e≈2.71828。Euler一步给出2，四步给出2.44141，十六步得到2.63793，六十四步得到2.69734。速度场在这个例子里完全正确，误差全部来自有限步长。因此评估生成模型时，应该先区分网络定义的运动是否合适，再检查求解器是否把这段运动算得足够准。

本章把每个网络的128步RK4结果作为数值参考，并用256步再次检查稳定性。相同16次网络查询，可以用于16步Euler、8步Heun或4步RK4。对独立配对模型，这三种结果相对参考终点的均方根误差约为0.06495、0.00473与0.000624。它们使用同一个网络，所以差别来自积分方法与步长；若更换网络，不能直接把轨迹误差混在一起比较。

![左：各模型对自身参考终点的RMSE。中：对同一独立测试集的32方向投影W1。圆、方、三角分别为Euler、Heun、RK4，横轴为实际网络调用次数。右：1024条参考轨迹的平均路径长减弦长。](https://ml-biomat.com/static/tutorials/machine-learning/figures/79ba9037b749a0fbb564c5cf.svg?v=79ba9037b749)

图 5左：各模型对自身参考终点的RMSE。中：对同一独立测试集的32方向投影W1。圆、方、三角分别为Euler、Heun、RK4，横轴为实际网络调用次数。右：1024条参考轨迹的平均路径长减弦长。

另一张图比较的是生成分布与独立测试分布的距离。它不会因为求解器更准确就必然单调下降：OT模型四步Euler的投影距离约0.0590，细步参考约0.0623，这次较粗的数值误差恰好把有限样本指标推向更小的值。选择算法时应同时看数值误差、样本分布与图形覆盖。速度网络调用次数也比“用了几步”更适合比较不同求解器的主要计算量。

## 跟随一个粒子，同时观察整群分布

播放的是实际128步RK4轨迹，每8步显示一帧，共17帧。箭头来自同一网络在该时刻的实际预测；右侧用相同坐标范围对照三种模型。

[Figure: 粒子、速度场及实际积分轨迹](https://ml-biomat.com/tutorials/machine-learning/m41/#M41-board)

蓝点为前128个固定起点的当前状态，红点为所选粒子，红线为它已经走过的轨迹。灰虚线直接连接该粒子的实际起终点，用于比较绕行；它不是原始训练配对。淡橙线标已知目标叶片中心线，箭头按固定尺度显示。

## 与连续Flow、扩散放在同一张地图上

连续Normalizing Flow描述的是由速度场和常微分方程构成的可逆连续变换。Flow Matching描述的是怎样训练这个速度场。二者可以同时出现在同一个模型上：用Flow Matching学到速度，用ODE生成样本，若还想计算密度，就沿轨迹累计速度场的散度。训练速度回归时可以不计算散度，求某个生成点的对数密度时则需要补上这一步。把模型结构与训练目标分开，名称之间的关系就清楚了。

2018年的Neural ODE把网络层之间的变化写成连续动力学，并为连续Flow提供了可训练的计算途径。若用最大似然直接训练这类模型，通常需要在训练循环里积分状态和密度变化；Flow Matching后来把训练监督移到可直接抽样的条件路径上。网络仍然定义一段连续运动，变化的是获得训练信号的方法。因此“训练时省去求解器”与“采样时使用求解器”可以同时成立，也解释了为什么这条路线受到关注。

$$
\frac{d\log p_t(z_t)}{dt}=-\nabla_z\cdot v_\theta(z_t,t)=-\sum_{i=1}^{d}\frac{\partial v_{\theta,i}}{\partial z_i}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f254dc7dba41b1b4a8f26790.svg) | 实际ODE轨迹、轨迹位置处密度、自然对数与沿轨迹求导；固定坐标单位下对数密度按nats计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a6396b974572ca759bf6ac3d.svg) | 速度的第i个分量、第i个位置分量、索引、维度与散度；散度单位为生成时间倒数。 |

二维速度v=(0.5z₁,0.5z₂)的散度为1。时间1内每个方向放大e^0.5，面积放大e，对数密度下降1，密度乘e^(−1)，概率质量保持。Flow Matching训练损失不需要这个散度，但计算CNF密度需要沿轨迹积它。生成样本的分布评价与密度计算各自回答不同问题。

扩散的概率流ODE也定义一个速度场，不过它通常从噪声过程及score推导速度。若直接用可抽样的条件路径监督速度，就可以从Flow Matching角度训练。两者共享许多连续概率路径与采样工具，区别常出现在路径如何选择、网络预测什么量、以及损失怎样加权。对某条固定路径，噪声预测、干净样本预测和速度预测还可能通过已知系数互相转换；训练权重与数值条件仍会随参数化变化。

方向约定也要明确。本章时间0是噪声、时间1是数据；扩散章节的离散时间则从干净数据0开始，噪声随编号增大。比较两章时，先把时间轴翻到同一方向，再比较速度或score的符号。仅凭一条箭头朝左还是朝右判断公式不同，容易把坐标约定当成方法差异。这里的速度是在整个样本空间中移动，若样本本身是一段机器人动作，它的生成时间又与动作内部的物理时间不同。

## 完整实验：风车的形状、覆盖与真实训练

风车有三片叶片，每片沿半径0.4到2展开，角度在叶片基准角上再增加半径的0.8倍，最后给两个坐标加入标准差0.07的独立噪声。训练集4,096点，验证与测试各1,024点，三套种子独立。坐标均无量纲。三个无条件速度网络都使用两个96单元的隐藏层，共9,890个参数；条件网络额外接收三维叶片编码，共10,178个参数。独立配对、OT与条件模型各训练4,000次，Reflow训练3,000次。

生成评价使用同一组1,024个新高斯起点。把生成点与测试点投影到32个均匀方向，每个方向分别排序后计算平均绝对差，再对方向平均，得到投影Wasserstein-1距离。它把比较变成许多一维搬运问题，数值越小表示这些投影越接近。另一个指标把点投到已知叶片中心线，检查距离小于0.21的比例，并把三片叶片各分六段，统计有至少五个合格点的区域。前者检查整体位置分布，后者把局部漏覆盖显式展示出来。

$$
\widehat{SW}_1=\frac1K\sum_{k=1}^{K}\frac1N\sum_{i=1}^{N}\left|\operatorname{sort}(Xq_k)_i-\operatorname{sort}(Yq_k)_i\right|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fea5eb7b1530bbb810b9d5d2.svg) | N×d生成点矩阵与独立测试点矩阵、每组点数1024和维度2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8e00274d63d818bbde8ebcc7.svg) | 第k个d维单位投影方向、方向数32与方向索引；二维角度在[0,π)均匀取值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7d9c626d72a72106966cdb1f.svg) | 每个投影内独立排序、排序索引、绝对值与有限方向投影W1估计；单位为坐标单位。 |

一维等权样本[0,2]与[1,3]排序后对应距离都为1，平均W1为1。二维先投影成一维，再对方向平均。相同指标可来自不同局部缺陷，所以本例同时查看曲线距离、18区段覆盖与散点图。

细步参考下，独立配对、OT与Reflow的投影距离分别约0.0729、0.0623和0.0791，靠近中心线的比例约68.7%、76.9%和65.1%。三者都覆盖18个统计区段，但分布厚度与局部位置仍不同；“覆盖全部区段”并不等于每个区段都已学得同样好。完整程序保存所有终点、完整参考轨迹、教师配对、训练记录与权重，因而可以用别的阈值重新检查，而不必依赖一张经过挑选的散点图。

验证集也与各自的训练目标对应。OT验证使用与训练相同的128点匹配规则；Reflow验证使用另一组独立的教师起终点。每个模型依据自己的固定验证误差选择权重，生成后再与同一份独立测试分布比较。这样，配对构造、模型选择与最终分布评价各有清楚的位置，读者可以循着程序检查每一个数是在哪一步得到的。

### 完整Python：训练速度、Reflow与求解器比较

运行python main.py --output results --language zh。依赖NumPy、SciPy、PyTorch与Matplotlib；所有数据由规则生成。四个网络真实训练，保存全部输出、教师配对、参考轨迹、权重和科学图。

```
"""Train flow-matching velocity fields and compare actual ODE trajectories.
All data follow the explicit pinwheel rule below. No downloads are required.
"""
from pathlib import Path
import argparse,json,math,copy,platform,time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
def pinwheel(n,seed):
 r=np.random.default_rng(seed);labels=np.arange(n)%3;r.shuffle(labels);radius=r.uniform(.4,2,n);angle=labels*2*np.pi/3+.8*radius;points=np.c_[radius*np.cos(angle),radius*np.sin(angle)]+r.normal(0,.07,(n,2));return points.astype('float32'),labels
train,labels=pinwheel(4096,410);valid,valid_labels=pinwheel(1024,411);test,test_labels=pinwheel(1024,412);xt=torch.tensor(train);yt=torch.tensor(labels)
class Velocity(nn.Module):
 def __init__(self,conditional=False):
  super().__init__();self.conditional=conditional;self.net=nn.Sequential(nn.Linear(3+(3 if conditional else 0),96),nn.SiLU(),nn.Linear(96,96),nn.SiLU(),nn.Linear(96,2))
 def forward(self,x,t,c=None):
  if isinstance(t,(float,int)):t=torch.full((len(x),1),float(t))
  else:t=t.reshape(-1,1)
  parts=[x,t]
  if self.conditional:parts.append(F.one_hot(c,3).float())
  return self.net(torch.cat(parts,1))
def couple(a,b,kind):
 if kind!='OT':return b
 cost=torch.cdist(a,b).square().numpy();_,j=linear_sum_assignment(cost);return b[j]
@torch.no_grad()
def integrate(model,initial,steps,method='heun',condition=None,record=False):
 x=initial.clone();h=1/steps;path=[x.numpy().copy()] if record else []
 for i in range(steps):
  t=i*h;k1=model(x,t,condition)
  if method=='euler':x=x+h*k1
  elif method=='heun':x=x+h*(k1+model(x+h*k1,t+h,condition))/2
  else:
   k2=model(x+h*k1/2,t+h/2,condition);k3=model(x+h*k2/2,t+h/2,condition);k4=model(x+h*k3,t+h,condition);x=x+h*(k1+2*k2+2*k3+k4)/6
  if record:path.append(x.numpy().copy())
 return x.numpy(),np.array(path)
histories={};training={};models={}
def fit(name,seed,steps=4000,paired=None):
 conditional=name=='Conditional';torch.manual_seed(seed);m=Velocity(conditional);opt=torch.optim.Adam(m.parameters(),lr=.001);rng=torch.Generator().manual_seed(seed+100);vrng=torch.Generator().manual_seed(seed+200)
 if paired is None:
  va=torch.randn((1024,2),generator=vrng);vb=torch.tensor(valid);vc=torch.tensor(valid_labels)
  if name=='OT':vb=torch.cat([couple(va[i:i+128],vb[i:i+128],name) for i in range(0,1024,128)])
 else:va,vb=paired[2:];vc=None
 vt=torch.rand((len(va),1),generator=vrng);vx=(1-vt)*va+vt*vb;vu=vb-va;best=float('inf');best_state=None;history=[];started=time.perf_counter()
 for step in range(1,steps+1):
  if paired is None:
   idx=torch.randint(len(xt),(128,),generator=rng);a=torch.randn((128,2),generator=rng);b=couple(a,xt[idx],name);c=yt[idx] if conditional else None
  else:
   idx=torch.randint(len(paired[0]),(128,),generator=rng);a,b=paired[0][idx],paired[1][idx];c=None
  t=torch.rand((128,1),generator=rng);x=(1-t)*a+t*b;u=b-a;loss=F.mse_loss(m(x,t,c),u);opt.zero_grad();loss.backward();opt.step()
  if step%200==0:
   with torch.no_grad():vl=F.mse_loss(m(vx,vt,vc),vu).item()
   history.append([step,loss.item(),vl])
   if vl<best:best=vl;best_step=step;best_state=copy.deepcopy(m.state_dict())
 m.load_state_dict(best_state);m.eval();models[name]=m;histories[name]=history;training[name]=dict(parameters=sum(p.numel() for p in m.parameters()),updates=steps,best_step=best_step,validation_velocity_mse=best,seconds=time.perf_counter()-started,seed=seed);torch.save(dict(model=m.state_dict(),conditional=conditional,best_step=best_step),out/f'{name.lower()}.pt');return m
fit('Independent',414);fit('OT',415)
teacher_rng=torch.Generator().manual_seed(416);teacher_train=torch.randn((2048,2),generator=teacher_rng);teacher_valid=torch.randn((512,2),generator=teacher_rng);teacher_b,_=integrate(models['Independent'],teacher_train,64,'heun');teacher_vb,_=integrate(models['Independent'],teacher_valid,64,'heun');fit('Reflow',417,3000,(teacher_train,torch.tensor(teacher_b),teacher_valid,torch.tensor(teacher_vb)));fit('Conditional',418)
evalrng=torch.Generator().manual_seed(413);initial=torch.randn((1024,2),generator=evalrng);requests=torch.arange(1024)%3
rr=np.linspace(.4,2,240);curve=np.concatenate([np.c_[rr*np.cos(c*2*np.pi/3+.8*rr),rr*np.sin(c*2*np.pi/3+.8*rr)] for c in range(3)]);curve_labels=np.repeat(np.arange(3),len(rr));curve_bins=np.tile(np.minimum((np.arange(len(rr))*6/len(rr)).astype(int),5),3)
angles=np.arange(32)*np.pi/32;directions=np.c_[np.cos(angles),np.sin(angles)]
def assess(x):
 distance=((x[:,None]-curve[None])**2).sum(2);nearest=distance.argmin(1);d=np.sqrt(distance[np.arange(len(x)),nearest]);cl=curve_labels[nearest];inside=d<.21;counts=np.bincount((cl*6+curve_bins[nearest])[inside],minlength=18);sw=float(np.abs(np.sort(x@directions.T,axis=0)-np.sort(test@directions.T,axis=0)).mean());return dict(sliced_w1=sw,mean_curve_distance=float(d.mean()),near_curve_fraction=float(inside.mean()),covered_bins=int((counts>=5).sum()),bin_counts=counts.tolist(),arm_counts=np.bincount(cl,minlength=3).tolist())
settings=[('Euler1','euler',1),('Euler4','euler',4),('Euler16','euler',16),('Heun8','heun',8),('RK4x4','rk4',4),('Heun32','heun',32)]
metrics={};outputs={};paths={};replay={};axis=np.linspace(-2.5,2.5,11);gx,gy=np.meshgrid(axis,axis);grid=np.c_[gx.ravel(),gy.ravel()].astype('float32')
for name,m in models.items():
 c=requests if name=='Conditional' else None;reference,reference_path=integrate(m,initial,128,'rk4',c,True);paths[name]=reference_path;outputs[name+'_reference']=reference;metrics[name]={}
 for label,method,n in settings:
  value,_=integrate(m,initial,n,method,c);stat=assess(value);stat.update(endpoint_rmse=float(np.sqrt(np.mean((value-reference)**2))),calls=n*dict(euler=1,heun=2,rk4=4)[method]);metrics[name][label]=stat;outputs[name+'_'+label]=value
 stat=assess(reference);refined,_=integrate(m,initial,256,'rk4',c);stat['refinement_rmse']=float(np.sqrt(np.mean((refined-reference)**2)));stat['calls']=512;chords=np.linalg.norm(reference_path[-1]-reference_path[0],axis=1);lengths=np.linalg.norm(np.diff(reference_path,axis=0),axis=2).sum(0);stat['mean_path_excess']=float(np.mean(lengths-chords));stat['mean_path_length']=float(lengths.mean());stat['mean_chord_length']=float(chords.mean())
 if c is not None:stat['condition_agreement']=float((curve_labels[((reference[:,None]-curve[None])**2).sum(2).argmin(1)]==requests.numpy()).mean())
 metrics[name]['Reference']=stat
 if name!='Conditional':
  time_indices=np.arange(0,129,8);fields=[]
  with torch.no_grad():
   for k in time_indices:fields.append(m(torch.tensor(grid),k/128).numpy().tolist())
  replay[name]=dict(times=(time_indices/128).tolist(),points=reference_path[time_indices,:128].tolist(),velocity=fields,solver='RK4, 128 steps')
# Exact two-by-two assignment, one hand interpolation, and a known ODE isolate calculation.
hand_a=np.array([[-1.,0.],[1.,0.]]);hand_b=np.array([[1.,1.],[-1.,1.]]);cost=((hand_a[:,None]-hand_b[None])**2).sum(2);row,col=linear_sum_assignment(cost);ode=[]
for n in [1,4,16,64]:
 x=1.;h=1/n
 for _ in range(n):x+=h*x
 ode.append(dict(steps=n,value=x,error=abs(x-math.e)))
pairrng=np.random.default_rng(419);pair_a=pairrng.normal(size=(24,2));pair_b=train[:24];_,pair_j=linear_sum_assignment(((pair_a[:,None]-pair_b[None])**2).sum(2));pair_ot=pair_b[pair_j]
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(train=4096,validation=1024,test=1024,seeds=[410,411,412],noise=.07),training=training,metrics=metrics,reflow=dict(train_pairs=2048,validation_pairs=512,teacher='Independent',teacher_solver='Heun64',teacher_calls_per_pair=128),hand=dict(interpolated=[.5,.25],velocity=[2.,1.],independent_cost=float(cost.diagonal().mean()),optimal_cost=float(cost[row,col].mean()),optimal_permutation=col.tolist(),euler_exp=ode),display_pairs=dict(independent_mean_cost=float(np.mean(np.sum((pair_b-pair_a)**2,1))),ot_mean_cost=float(np.mean(np.sum((pair_ot-pair_a)**2,1)))))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'replay.json').write_text(json.dumps(dict(models=replay,grid=grid.tolist(),target=test[:400].tolist(),curves=[curve[i*240:(i+1)*240:8].tolist() for i in range(3)]),separators=(',',':')),encoding='utf-8');np.savez_compressed(out/'experiment.npz',train=train,train_labels=labels,validation=valid,validation_labels=valid_labels,test=test,test_labels=test_labels,initial_noise=initial.numpy(),requested_classes=requests.numpy(),teacher_train_start=teacher_train.numpy(),teacher_train_end=teacher_b,teacher_validation_start=teacher_valid.numpy(),teacher_validation_end=teacher_vb,grid=grid,pair_a=pair_a,pair_b=pair_b,pair_ot=pair_ot,**outputs,**{name+'_trajectory':v for name,v in paths.items()},**{name+'_history':np.array(v) for name,v in histories.items()})
colors=['#176b8a','#bd6d3a','#63864b']
fig,axs=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
for ax,b,title in zip(axs[:2],[pair_b,pair_ot],[tr('A  独立配对','A  Independent pairs'),tr('B  小批次最短平方距离配对','B  Minibatch squared-cost assignment')]):
 for a,z in zip(pair_a,b):ax.plot([a[0],z[0]],[a[1],z[1]],color='#647e87',alpha=.4,lw=.8)
 ax.scatter(*pair_a.T,s=26,facecolors='none',edgecolors='#125f82',label=tr('噪声起点','Noise start'));ax.scatter(*b.T,s=24,c='#bf7139',label=tr('数据终点','Data end'));ax.set_title(title);ax.legend(fontsize=8)
for i in range(24):axs[2].plot(paths['Independent'][:,i,0],paths['Independent'][:,i,1],color=colors[i%3],alpha=.7,lw=1)
axs[2].scatter(*initial[:24].numpy().T,s=20,facecolors='none',edgecolors='#125f82');axs[2].set_title(tr('C  学到的ODE轨迹','C  Learned ODE trajectories'))
for ax in axs:ax.set(xlabel='x1',ylabel='x2',xlim=(-4,4),ylim=(-4,4));ax.set_aspect('equal')
save(fig,'couplings')
fig,axs=plt.subplots(2,3,figsize=(13,8),layout='constrained')
for row,name in enumerate(['Independent','OT']):
 for col,k in enumerate([0,64,128]):
  ax=axs[row,col];pts=paths[name][k];ax.scatter(pts[:500,0],pts[:500,1],s=5,color='#176b8a',alpha=.5);ax.scatter(test[:300,0],test[:300,1],s=3,color='#bf7139',alpha=.15)
  with torch.no_grad():v=models[name](torch.tensor(grid),k/128).numpy()
  ax.quiver(grid[:,0],grid[:,1],v[:,0],v[:,1],angles='xy',scale_units='xy',scale=8,width=.003,color='#314c59');ax.set(xlim=(-3,3),ylim=(-3,3),xlabel='x1',ylabel='x2',title=f'{name}, t={k/128:.1f}');ax.set_aspect('equal')
save(fig,'velocity')
fig,axs=plt.subplots(3,4,figsize=(13,10),layout='constrained')
for row,name in enumerate(['Independent','OT','Reflow']):
 for col,key in enumerate(['Euler1','Euler4','Heun8','reference']):
  v=outputs[name+'_'+key];ax=axs[row,col];ax.scatter(*v[:500].T,s=5,alpha=.55,color='#176b8a');ax.set(xlabel='x1',ylabel='x2',xlim=(-3,3),ylim=(-3,3),title=f'{name} / {key}');ax.set_aspect('equal')
save(fig,'samples')
fig,axs=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
for j,name in enumerate(['Independent','OT','Reflow']):
 for label,method,n in settings:
  z=metrics[name][label];axs[0].scatter(z['calls'],z['endpoint_rmse'],color=colors[j],marker=dict(euler='o',heun='s',rk4='^')[method]);axs[1].scatter(z['calls'],z['sliced_w1'],color=colors[j],marker=dict(euler='o',heun='s',rk4='^')[method])
 axs[0].plot([],[],color=colors[j],label=name);axs[2].bar(j,metrics[name]['Reference']['mean_path_excess'],color=colors[j])
axs[0].set(xscale='log',yscale='log',xlabel=tr('速度网络调用次数','Velocity-network calls'),ylabel=tr('终点对参考解RMSE','Endpoint RMSE vs reference'),title=tr('A  同一模型的数值误差','A  Numerical error within each model'));axs[0].legend(fontsize=8);axs[1].set(xscale='log',xlabel=tr('速度网络调用次数','Velocity-network calls'),ylabel=tr('32方向投影W1','32-direction sliced W1'),title=tr('B  与独立测试分布比较','B  Difference from held-out distribution'));axs[2].set(xticks=range(3),xticklabels=['Independent','OT','Reflow'],ylabel=tr('平均路径长减弦长','Mean path length minus chord'),title=tr('C  积分路径弯曲程度','C  Curvature of integrated paths'));save(fig,'diagnostics')
fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained');conditional=outputs['Conditional_reference'];req=requests.numpy()
for c,ax in enumerate(axs):
 ax.scatter(*test[test_labels==c].T,s=7,color='#bf7139',alpha=.4,label=tr('测试目标','Test target'));ax.scatter(*conditional[req==c].T,s=7,color='#176b8a',alpha=.6,label=tr('按类别生成','Conditional samples'));ax.set(xlim=(-2.5,2.5),ylim=(-2.5,2.5),xlabel='x1',ylabel='x2',title=tr('请求叶片 ','Requested arm ')+str(c));ax.set_aspect('equal');ax.legend(fontsize=9)
save(fig,'conditions');print(json.dumps(summary,indent=2))
```

## 条件决定去哪一片区域，评价决定是否到得合适

在条件实验中，网络还收到请求的叶片编号。训练时，目标数据点的叶片类别作为条件，噪声起点仍独立抽取；生成时改变类别编码，同一噪声就能被送往不同叶片。条件模型细步生成的叶片符合率为99.8%，靠近中心线的比例约90.0%。这些数字描述本章三类几何点的结果。若条件换成文字、音频提示或初始姿态，条件编码与评价规则也需要随任务改变。

![三个请求叶片下的实际条件生成（蓝）与对应独立测试点（橙）。生成起点为同一评价噪声组中指定该类别的子集；每组约341点，采用128步RK4。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e2030bc5c6d607309abbc48e.svg?v=e2030bc5c6d6)

图 6三个请求叶片下的实际条件生成（蓝）与对应独立测试点（橙）。生成起点为同一评价噪声组中指定该类别的子集；每组约341点，采用128步RK4。

将一段动作作为样本时，位置向量可以由所有时刻的关节角拼接而成，速度网络输出的是整个候选动作在生成过程中的变化率。它与某个关节真实运动的角速度不同：前者沿生成时间改变一个完整方案，后者沿物理时间描述方案内部的运动。这样的模型能提出多种动作候选，随后还要检查碰撞、关节范围、接触条件与终点误差，判断方案能否执行。

回到开始的光点表演，生成模型学到的是如何组织一群候选，而不是给每个点永久编号。端点配对决定训练路径，条件平均形成可查询的速度场，求解器把速度积成实际轨迹，评价再检查最终分布。抓住这四个环节，就能读懂为什么直线训练仍可能得到弯曲生成，为什么Reflow有助于减少步数，以及为什么更快、更直和更接近目标要分别用数据回答。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M41.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Flow Matching for Generative Modeling](https://arxiv.org/html/2210.02747v2)

   概率路径、条件速度与边缘速度回归。

   Primary paper; independent experiment
2. [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/html/2209.03003v1)

   直线插值、ODE配对、Reflow与轨迹性质。

   Primary paper; independent experiment
3. [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482)

   小批次耦合和OT-CFM。

   Primary paper; independent experiment
4. [TorchCFM](https://github.com/atong01/conditional-flow-matching)

   原始密度、速度与轨迹动画，明确由仓库教程生成。

   MIT Copyright2023AlexanderTong; cropped original frames and license retained
5. [Flow Matching Guide and Code](https://github.com/facebookresearch/flow_matching)

   连续与离散Flow Matching的进一步学习入口。

   CC BY-NC repository; linked reference only, no code/figure reuse
6. [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366)

   连续动力学网络与密度变化。

   Primary paper; no copied figures
7. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/html/2011.13456v2)

   概率流ODE与扩散的联系。

   Primary paper; no copied figures
