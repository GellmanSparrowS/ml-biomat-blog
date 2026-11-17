# 凝胶分数：真正连成网络的有多少

Source: https://ml-biomat.com/tutorials/experimental-methods/e02/
Language: zh-CN

从连接、提取和质量守恒读懂凝胶分数，辨别填料、未提尽组分与网络结构各自的作用。

## 看起来成了胶，里面的链都连上了吗

把一种透明液体照光几分钟，它变成了可以夹起的小圆片。若要把圆片用作细胞支架，接下来会关心它在培养液里是否稳定、会释放多少可溶物、不同批次的连接程度是否一致。肉眼看到“成胶”回答了整体形态的问题，却没有告诉我们有多少聚合物真正留在网络中。凝胶分数实验把材料放进能够带走可溶组分的液体里，经过充分提取和干燥，再比较留下的干物质。它把一个模糊的形态判断变成有明确质量基准的实验问题。

可以把前驱液想成一桌散开的毛线。连接反应发生后，有些线被接进横跨桌面的网，有些只形成小团，还有些仍然游离。把整张网轻轻提起来，会带起与它相连的线；足够容易移动的小团和游离线，则有机会被合适的溶剂带走。实际提取比这个动作更慢，因为可溶链还要穿过网络和周围液体。网孔较小、链很长或样品较厚时，它们可能暂时困在里面。因此，提取后留得多，既可能来自网络比例高，也可能来自提取尚未充分。

这个实验与上一章的溶胀相互补充。溶胀关注网络留住了多少液体，凝胶分数关注原有干物质有多少在提取后留下。两种质量变化可以同时发生：一块样品在水中变重，是因为吸水；同一块样品重新干燥后变轻，则可能因为可溶组分离开。若把湿质量直接放进凝胶分数的分子，吸水量就会混入连接程度的测量。先分清干物质和水，再讨论网络、填料和提取物，后面的计算就有了清楚对象。

本章从“连通”这个直观概念开始，逐步进入干质量核算、提取终点、填料校正和结果解释。完整程序包含一组可手算的复合凝胶例子，也重新绘制了一篇开放论文中的真实凝胶分数与力学数据。你会看到，几乎所有质量都留在网络里，仍然可以对应相差很大的刚度。这个发现不是实验之间互相矛盾，而是说明网络的质量、连接方式和有效承载链各自提供了不同的信息。

## 从一根线到一张网：连通为何会突然出现

一根高分子链由许多重复单元连接而成，但链很长并不等于已经形成三维网络。要形成网络，需要不同链或不同分支之间建立连接，逐渐出现能够贯穿样品的连通结构。可以把每个节点看作分子片段，把连接看作化学键或稳定的物理联系。当连接很少时，只有许多小团；再增加少量关键连接，几个大团可能被接成一体。整体开始表现出凝胶特征的转变，与单个反应基团是否已经全部反应是两个问题。

一九四一年，Flory 用分子统计方法研究三维聚合物的成胶；随后 Stockmayer 在一九四三年及一九四四年的工作中进一步发展了分支聚合物的尺寸分布和成胶理论。科学史在这里帮助我们换一种看法：成胶不是每根链都同时“变硬”，而是连接关系改变以后，体系出现了跨越更大尺度的结构。下面的有限网格图增加同一批候选连接的出现概率，突出最大连通簇的变化，直观展示为什么连接多少和连接在哪里都重要。

![固定候选连线上的有限网格模拟，蓝色表示最大连通簇。节点等质量，图用于解释连通结构的出现，不将有限网格比例作为实验凝胶分数。历史注释对应 Flory 与 Stockmayer 的成胶研究。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1384b4cb998ba0d0373dc581.svg?v=1384b4cb998b)

图 1固定候选连线上的有限网格模拟，蓝色表示最大连通簇。节点等质量，图用于解释连通结构的出现，不将有限网格比例作为实验凝胶分数。历史注释对应 Flory 与 Stockmayer 的成胶研究。

这幅图的节点质量相同，最大连通簇的节点比例可以作为理解网络比例的练习；真实高分子链的长度和质量不同，实验称量对应的是质量比例。有限网格也会出现多个较大的团块，不能把其中最大的一团直接当作任何材料的标准凝胶分数。图要说明的是连通概念，称量实验则通过规定的提取条件分离可提取和残留部分。把两者联系起来时，需要考虑链的溶解能力、扩散速度、物理缠结和连接的稳定性。

即使一条链连进网络，它也不一定承担同样多的弹性负载。一端连接、另一端自由的悬挂链，会增加网络质量，却未必像两端都接在有效网络上的链那样传递应力。形成局部小环的连接，也可能消耗反应基团而没有增加远距离连通。可以把它想成桥上的钢索：接在两端支座之间的索与只挂在一个支座上的索，质量相同，承载作用却不同。因此，凝胶分数、反应转化率和力学模量需要分别测量，再共同解释。

物理凝胶还提醒我们，网络存在于具体条件下。明胶在适当温度下形成的连接，可能在升温时解开；离子交联的多糖网络可能受到盐组成影响。如果提取液把这些连接主动拆开，测到的残留比例就包含网络解体过程。对于稳定共价网络，通常希望选用能溶解可溶链、又尽量保持网络连接的条件；对于可逆网络，则应把温度、离子环境和观察时间直接写进研究问题，描述在这些条件下保留下来的结构。

## 先算干物质，再决定分母里放什么

最简单的情况是样品只含一种聚合物，提取前后都能得到可靠的干质量。提取后的干质量除以提取前的干质量，就是以初始干聚合物为基准的凝胶分数。若初始为一百毫克，充分提取后留下八十毫克，则凝胶分数为百分之八十，其余百分之二十是这一操作条件下被提取的部分。先做这个简单算例，可以看到百分数的物理含义：每一百份初始干物质中，有多少份在规定提取后留了下来。

$$
G=\frac{m_r}{m_0},\qquad S=\frac{m_0-m_r}{m_0}=1-G
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 以初始干聚合物为基准的凝胶质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 同一基准下的可提取质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 提取前干聚合物质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | 充分提取后保留的干聚合物质量，mg。 |

两者采用同一初始质量作分母。m0=100 mg、mr=80 mg 时，G=0.80、S=0.20；乘 100 后分别为 80% 与 20%。假设提取过程中网络保持研究定义下的稳定状态，其他质量贡献已校正。

“溶胶分数”通常表示与凝胶分数互补的可溶部分，但互补关系需要相同的质量基准。若把质量损失除以提取后的质量，一百减八十再除以八十，会得到百分之二十五；这与以初始质量为分母的百分之二十不同，二者不能直接与同一个凝胶分数相加。最稳妥的办法是先写出物质去向：初始聚合物等于残留网络聚合物加已提取聚合物，再在等式两侧除以同一个初始质量。公式由质量守恒得到，而不是靠记忆分母位置。

实际生物材料常含无机颗粒、纤维、颜料或药物。假设一百毫克复合材料包含二十毫克不溶填料和八十毫克聚合物，其中百分之八十的聚合物属于网络。那么网络聚合物为六十四毫克，可溶聚合物为十六毫克，充分提取后的总干残留为八十四毫克。直接报告百分之八十四，描述的是复合材料的总残留比例；若研究聚合物连网比例，应在分子和分母中分别扣除对应填料，得到六十四除以八十，即百分之八十。

$$
G_p=\frac{m_r-m_{f,r}}{m_0-m_{f,0}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9c807c118e583214a0e1035b.svg) | 扣除填料后的聚合物凝胶质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 复合材料提取前的总干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | 复合材料提取后的总干残留，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f3258e9a04f243f0185368.svg) | 提取前填料干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/761a14a6eca3d939d07aa69e.svg) | 提取后残留填料干质量，mg。 |

分子只留下网络聚合物，分母只留下初始聚合物。100 mg 初始总质量、84 mg 残留和前后各 20 mg 填料给出 Gp=(84−20)/(100−20)=0.80。填料若流失，两端需要各自测量。

![构造质量账本：100 mg 复合材料包含 64 mg 网络聚合物、16 mg 可溶聚合物和 20 mg 不溶填料。充分提取后总残留 84%，聚合物凝胶分数 80%。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c50baf2285aef444a74f8caa.svg?v=c50baf2285ae)

图 2构造质量账本：100 mg 复合材料包含 64 mg 网络聚合物、16 mg 可溶聚合物和 20 mg 不溶填料。充分提取后总残留 84%，聚合物凝胶分数 80%。

这里必须区分提取前填料和提取后填料。若颗粒也会脱落、溶解或发生反应，不能把同一个填料质量自动从两端扣除。可以通过已知配方、灰分测量、热重分析或元素分析确定各阶段的填料贡献，并检查这些方法是否还包含其他不挥发残留。装在网袋、筛网或容器里提取的样品，也应扣除载体自身质量。让每一项质量对应一种明确物质，比把计算式增加很多符号更有用。

初始干质量也值得认真选择。有些前驱体系含盐、光引发剂和小分子添加剂，它们本来就不属于高分子网络；以总配方固体为分母时，得到的是总固体残留，而不是纯粹的聚合物凝胶分数。如果研究制备过程中聚合物的利用程度，可以使用进入反应的干聚合物量作为基准，并独立核对转移损失。比较不同配方时，应保持分母定义一致，尤其避免一种材料扣除了添加剂、另一种却把所有固体都算进去。

## 提取条件决定哪些物质能够离开

选溶剂首先要回答它能否溶解目标可溶组分。水适合许多亲水聚合物，却不能自动提取所有未连接的疏水链；一种溶剂能溶解原料，也不代表它在当前温度下能迅速穿过成胶后的材料。可以先用未交联聚合物做溶解对照，再用已知稳定的网络检查条件是否会造成化学断裂或显著侵蚀。这样，实验的“洗掉”步骤就有了可验证的作用对象，而不是把所有在浸泡后减少的质量都归给未反应链。

样品厚度影响可溶链走到外液的路程。薄片、粉碎颗粒和完整块体即使化学组成相同，达到提取终点的时间也可能不同。切碎有助于缩短路径，但可能产生难以回收的网络碎屑；使用筛网保留碎屑时，又要检查细小颗粒是否穿过筛孔。适度搅动可以减少样品周围停滞液层的影响，剧烈搅动则可能让柔软网络机械破碎。因此，尺寸、支撑方式和搅动强度都应服务于分离可溶物这一目标。

换新溶剂能够降低外液中已提取物的浓度，让更多可溶链继续向外迁移。连续萃取装置通过反复接触较新的溶剂提高提取效率，简单的分次浸泡也能做到类似的浓度更新。选择哪一种方式取决于材料稳定性、溶剂和实验规模。升温通常会加快某些迁移过程，却也可能改变物理连接或加速化学反应；提取条件不能只按“越强越充分”选择。更好的目标是找到可溶物已充分移出、网络性质仍符合研究定义的操作窗口。

判断终点需要连续证据。可以比较多轮提取后的干残留是否趋于稳定，检查后续提取液中的聚合物信号是否接近空白，或者结合两种办法。反复干燥同一块样品可能改变结构，因而也可以使用独立样品完成不同提取时长。若残留质量长期持续下降，应检查网络降解、颗粒脱落和溶剂不相容等过程，而不是只把更长时间对应的更低数值当成“更准确”。终点判断应与实际材料的稳定性一起建立。

空白和回收检查能把操作损失与材料差异分开。空容器、空网袋经过相同浸泡和干燥步骤，可以显示载体自身是否留下残留或损失质量；已知质量的可溶聚合物经过同样回收步骤，可以估计提取液蒸干、转移和分析造成的损失。若要分析残留单体或光引发剂，色谱等方法能进一步给出化学身份。总质量测量告诉我们有多少物质离开，组成分析则告诉我们离开的是什么，两者组合更适合解释后续细胞实验。

## 洗一次和洗六次，测到的为什么不同

用一个可手算的模型观察提取过程。仍取一百毫克复合材料，其中网络聚合物六十四毫克、填料二十毫克、可溶聚合物十六毫克。假设每轮提取都带走当前剩余可溶物的百分之七十，而网络和填料保持不变。第一轮剩下四点八毫克可溶物，第二轮剩下一点四四毫克，第三轮只剩零点四三二毫克。每次去掉的是“当前剩余量”的固定比例，所以剩余量按几何级数减少，而不是每轮都减去同样的毫克数。

$$
m_{s,n}=m_{s,0}(1-f)^n,\qquad m_{r,n}=m_g+m_f+m_{s,n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ed6a8b77d464f557e04c458b.svg) | 第 n 轮后仍困在样品中的可溶物质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4485401618153fae76741122.svg) | 初始可溶物质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 每轮去除当前可溶物的比例，无量纲，0≤f≤1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 提取循环次数，非负整数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c08b19480f6f40dc311e3c0.svg) | 第 n 轮后的总干残留，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/821fabcbaa0d572d6a4846c5.svg) | 保持不变的网络聚合物质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/554f701c791c97b491f4dfff.svg) | 保持不变的填料质量，mg。 |

教学模型令每次保留相同比例的可溶物。ms,0=16 mg、f=0.7 时，一轮后 4.8 mg，三轮后 0.432 mg；加上 64 mg 网络和 20 mg 填料，三轮总残留为 84.432 mg。

第一轮后的总残留为八十八点八毫克，未扣填料的残留比例是百分之八十八点八。扣除二十毫克填料后，再除以八十毫克初始聚合物，得到百分之八十六，仍高于真正连网的百分之八十。到第三轮，这个校正后比例降为百分之八十点五四。这里有两个独立偏差：填料把总残留抬高，尚未提完的可溶物又让聚合物残留继续偏高。只完成其中一种校正，不能消除另一种原因。

![构造的分次提取诊断：总残留与填料校正、每轮提取量、去除比例敏感性、独立样品结果。三份样品的点展示实际计算值，横线为均值。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f6e0308e2b15403d7f0adbaa.svg?v=f6e0308e2b15)

图 3构造的分次提取诊断：总残留与填料校正、每轮提取量、去除比例敏感性、独立样品结果。三份样品的点展示实际计算值，横线为均值。

图中的每轮提取量逐渐减小，说明后续换液提供的信息与最初不同。第一轮主要显示容易移出的部分，后几轮更接近判断提取是否充分。模型中的每轮去除比例是教学设定，真实过程会受到溶剂质量、链尺寸、网络阻碍和时间影响。若后续一轮提取量突然明显增加，应该回看温度、换液、样品破损或化学变化，而不是机械地用同一个指数解释所有数据。保留每份提取液的编号，可以把异常和具体操作阶段对应起来。

交互实验让你同时改变每轮去除比例、循环次数和填料比例。网络在聚合物中所占的真实比例固定为百分之八十。先保持填料比例不变，只增加循环次数，观察校正后结果如何接近八十；再保持提取充分，改变填料比例，观察总残留比例为何跟着变。两条曲线把配方组成和提取效率的影响分开。研究不同复合材料时，这种分离尤其有用，因为填料含量常常正是配方变化的一部分。

## 提取效率与填料，各自改变了什么

初始复合材料 100 mg，聚合物真实凝胶分数固定为 80%。改变提取轮数、每轮去除比例和填料含量，观察两种残留比例。

[Figure: 提取轮数与残留质量比例](https://ml-biomat.com/tutorials/experimental-methods/e02/#E02-plot)

提取结束后，还可以做质量闭合检查。若初始总质量一百毫克，最终残留八十四毫克，收集并分析到的提取物为十五点二毫克，两者合计九十九点二毫克，对初始质量的回收率为百分之九十九点二。这个结果提示还有零点八毫克的转移、回收或测量差异需要解释。若合计超过初始质量，应检查残余溶剂、盐沉积和容器扣重。质量闭合把样品与提取液连成同一个账本，有助于判断质量变化是否已被主要环节捕捉。

$$
R_m=\frac{m_r+\sum_{i=1}^{N}m_{e,i}}{m_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e11a2e26f9ec9e2808fc57d6.svg) | 质量回收率，无量纲，乘 100 为百分数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | 最终总干残留质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb04031f2872bf6b1f089faf.svg) | 第 i 份提取液中回收到的目标干物质质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 与这些物质类别一致的初始总干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 提取液编号，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 提取液份数，无量纲整数；求和符号表示全部相加。 |

把留在样品和进入各份提取液的质量相加，再与初始质量比较。84 mg 残留与合计 15.2 mg 提取物，对 100 mg 初始质量的回收率为 99.2%。

## 同样的凝胶分数，为什么可以有不同的刚度

还有一种情况是整块样品的平均值掩盖了空间差异。光交联材料可能因光在厚度方向衰减、表面氧气或组分分布不均而形成不同的连接程度。整体凝胶分数较高，并不排除表层和内部的力学状态不同。可以比较不同厚度、照射方向或切片区域，并结合空间分辨的光谱或力学测量。此时需要改进的是制备均匀性，而不只是继续提高平均残留比例。

凝胶分数接近百分之百，意味着按当前提取定义，几乎全部初始聚合物都留在残余网络中。它没有直接规定相邻连接点之间的链长，也没有规定每单位湿体积里有多少聚合物。两张网都可以把所有绳子连起来，一张网结疏、另一张网结密；它们的总连网质量相似，承载响应却不同。溶胀又会改变湿网络的体积和链间距离，所以解释力学性质时，应同时考虑聚合物浓度、网络结构、含水状态和加载时间尺度。

真实材料中的这种差别很容易通过开放数据看到。Velasco-Rodriguez 等人的研究比较了改性明胶、改性透明质酸及其混合网络，表中同时报告凝胶分数和弹性模量。下面把其中两组量重新画出来：横向误差线保留原表报告的误差数值，右图将每种配方的凝胶分数与模量配对。可以看到，凝胶分数相近的点并不挤在同一个模量值上。阅读时应把点看成不同配方，而不是同一配方连续提高交联程度的轨迹。

![真实公开数据重绘自 Velasco-Rodriguez 等（2021），表 1，International Journal of Molecular Sciences 22:6758，DOI 10.3390/ijms22136758，CC BY 4.0。保留原表凝胶分数、模量及所报告误差数值；原表未明确标注误差类型，故不另命名。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/72cdec58cdfaff0e1ec8569d.svg?v=72cdec58cdfa)

图 4真实公开数据重绘自 Velasco-Rodriguez 等（2021），表 1，International Journal of Molecular Sciences 22:6758，DOI 10.3390/ijms22136758，CC BY 4.0。保留原表凝胶分数、模量及所报告误差数值；原表未明确标注误差类型，故不另命名。

图中的误差值来自原论文表格，本章保持其原有数值，不把没有明确注明的误差类型另行命名。自己的实验则应明确写出误差条代表标准差、标准误还是某种置信区间，并说明独立样品数。比如三个独立样品的凝胶分数分别略高、略低于八十，可以先展示三个点，再给出平均值和样品间标准差。把同一块材料重复称三次反映的是称量重复性，与三次独立制备的批次差异不是同一层级的信息。

凝胶分数与生物相容性的关系也需要经过中间步骤。较多可提取物可能意味着有未连入网络的聚合物、添加剂或反应副产物，但它们对细胞的作用取决于具体成分、浓度和暴露条件。通过色谱、光谱或适合目标组分的定量方法，可以确定提取物身份；再把提取液用于有明确对照的细胞实验，才形成从制备到生物响应的解释链。单纯追求更高的凝胶分数，可能忽略网络太致密、传质太慢或力学环境不合适等其他设计要求。

同样，反应基团消耗得多，也可能产生更多局部环或悬挂结构，而不成比例地提高有效连接。可以用光谱跟踪反应转化，用提取衡量不溶网络质量，用溶胀探查含水状态，用流变或力学实验测量承载响应。若这几种结果共同改变，研究者就有更完整的证据；若它们变化方向不同，差异本身可能指出网络结构正在改变。选择后续实验时，关键是找出当前哪一层信息尚未测到，而不是让一种指标承担全部解释。

## 让质量核算帮助你改进下一批材料

将凝胶分数接回溶胀实验时，也要更新干质量基准。假设原始干聚合物一百毫克，提取后留下八十毫克网络，随后湿质量为八百毫克。用原始一百毫克作分母，湿干比为八；用实际剩余网络八十毫克作分母，湿干比为十。前者描述相对初始投入的湿质量，后者描述当前网络的含水状态。保存提取前后两个干质量，就能让这两种结果各自回答明确的问题。

完整代码从一个明确的质量组成开始，计算每轮提取后留下的网络、填料和可溶物，再分别输出原始残留比例与聚合物校正比例。它还为三份独立样品设置不同的初始质量，演示先逐样品扣除填料、再计算平均值的方法。另一个表格保存公开论文中的真实数值，程序直接读取并重新绘图。这样，构造数据负责解释计算机制，公开实验数据负责展示真实配方之间的关系，两者在文件和图注中都有清楚身份。

### 完整 Python：提取终点、填料校正与公开数据重绘

程序导出各轮提取账本、逐样品校正表、四幅图和数值汇总；公开数据表与 CC BY 许可说明随示例提供。

```
"""Gel fraction: extraction mass balance, filler correction, and published network properties."""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def extraction(cycles,removal=.7,initial=100.,filler=20.,gel_fraction=.8):
    polymer=initial-filler;network=polymer*gel_fraction;sol=polymer-network
    trapped=sol*(1-removal)**np.asarray(cycles)
    residual=network+filler+trapped
    return residual,100*residual/initial,100*(residual-filler)/polymer,trapped

def connected_components(n,edges):
    parent=list(range(n))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,j in edges:parent[find(i)]=find(j)
    groups={}
    for i in range(n):groups.setdefault(find(i),[]).append(i)
    return sorted(groups.values(),key=len,reverse=True)

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(202);coords=np.array([(i%6,i//6) for i in range(36)]);edges=[(i,j) for i in range(36) for j in range(i+1,36) if np.abs(coords[i]-coords[j]).sum()==1];scores=rng.random(len(edges));sizes=[]
    fig,ax=plt.subplots(1,3,figsize=(12,4.5))
    for a,p in zip(ax,[.2,.5,.85]):
        active=[e for e,s in zip(edges,scores) if s<p];groups=connected_components(36,active);largest=set(groups[0]);sizes.append(len(largest))
        for i,j in active:a.plot(coords[[i,j],0],coords[[i,j],1],color='#186e83' if i in largest else '#c4cbd0',lw=2)
        a.scatter(*coords.T,c=['#186e83' if i in largest else '#cd803f' for i in range(36)],s=36,zorder=4);a.set_aspect('equal');a.axis('off');a.set_title(tr(f'连接概率 {p:.2f}\n最大连通簇 {len(largest)}/36',f'Bond probability {p:.2f}\nLargest connected cluster {len(largest)}/36'))
    fig.text(.5,.02,tr('1941–1943：Flory 与 Stockmayer 将成胶理解为分支连接的统计问题。','1941–1943: Flory and Stockmayer treated gelation as a statistical connectivity problem.'),ha='center',fontsize=10);save(fig,'connectivity')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));names=tr(['提取前','充分提取后'],['Before extraction','After complete extraction'])
    ax[0].bar(names,[64,64],label=tr('网络聚合物','Network polymer'),color='#186e83');ax[0].bar(names,[16,0],bottom=[64,64],label=tr('可溶聚合物','Soluble polymer'),color='#cd803f');ax[0].bar(names,[20,20],bottom=[80,64],label=tr('不溶填料','Insoluble filler'),color='#8160a1');ax[0].set(ylabel=tr('干质量 / mg','Dry mass / mg'),title=tr('A  100 mg 复合材料的质量去向','A  Mass accounting for a 100 mg composite'));ax[0].legend(fontsize=9)
    ax[1].barh(tr(['原始残留比','聚合物凝胶分数'],['Raw residue fraction','Polymer gel fraction']),[84,80],color=['#8160a1','#186e83']);ax[1].set(xlim=(0,105),xlabel=tr('质量分数 / %','Mass fraction / %'),title=tr('B  分子和分母同时扣除填料','B  Remove filler from numerator and denominator'))
    for i,v in enumerate([84,80]):ax[1].text(v+1,i,str(v),va='center')
    fig.tight_layout();save(fig,'accounting')
    cycles=np.arange(7);residual,raw,corrected,trapped=extraction(cycles);removed=np.r_[0,-np.diff(trapped)];np.savetxt(output/'extraction.csv',np.column_stack([cycles,residual,raw,corrected,trapped,removed]),delimiter=',',header='cycle,residual_mg,raw_percent,polymer_corrected_percent,trapped_sol_mg,removed_this_cycle_mg',comments='')
    specimen_initial=np.array([100.,120.,90.]);specimen_filler=.2*specimen_initial;specimen_final=.8*(specimen_initial-specimen_filler)+specimen_filler+np.array([.3,-.2,.1]);measured=100*(specimen_final-specimen_filler)/(specimen_initial-specimen_filler)
    np.savetxt(output/'specimens.csv',np.column_stack([specimen_initial,specimen_filler,specimen_final,measured]),delimiter=',',header='initial_mg,filler_mg,extracted_dry_mg,polymer_gel_percent',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11,7));ax=ax.ravel();ax[0].plot(cycles,raw,'o-',label=tr('未扣填料','Filler uncorrected'));ax[0].plot(cycles,corrected,'s-',label=tr('扣除填料','Filler corrected'));ax[0].axhline(80,color='#707c82',ls='--');ax[0].set(ylabel=tr('残留分数 / %','Remaining fraction / %'),title=tr('A  提取不足与填料是两个偏差','A  Incomplete extraction and filler are distinct biases'));ax[0].legend(fontsize=9)
    ax[1].bar(cycles[1:],removed[1:],color='#cd803f');ax[1].set(ylabel=tr('本次提取物 / mg','Mass extracted in this wash / mg'),title=tr('B  每一次换液带走多少','B  Material removed by each wash'))
    for f in [.3,.5,.7,.9]:ax[2].plot(cycles,extraction(cycles,f)[2],'.-',label=f'{f:.1f}')
    ax[2].axhline(80,color='#707c82',ls='--');ax[2].set(ylabel=tr('校正后残留分数 / %','Corrected remaining fraction / %'),title=tr('C  每次去除比例改变终点接近速度','C  Removal fraction controls endpoint approach'));ax[2].legend(title=tr('每次去除比例','Removal per wash'),fontsize=9)
    ax[3].plot(np.arange(1,4),measured,'o',ms=8);ax[3].axhline(measured.mean(),color='#cd803f');ax[3].set(xticks=[1,2,3],ylim=(78,82),xlabel=tr('独立样品编号','Independent specimen'),ylabel=tr('聚合物凝胶分数 / %','Polymer gel fraction / %'),title=tr('D  先逐样品校正，再汇总','D  Correct individual specimens before averaging'))
    for a in ax[:3]:a.set_xlabel(tr('提取循环次数','Extraction cycle'))
    fig.tight_layout();save(fig,'extraction')
    with Path(__file__).with_name('published_table.csv').open(encoding='utf8') as f:rows=list(csv.DictReader(f))
    g=np.array([float(r['gel_percent']) for r in rows]);ge=np.array([float(r['gel_error']) for r in rows]);m=np.array([float(r['modulus_kPa']) for r in rows]);me=np.array([float(r['modulus_error']) for r in rows]);labels=[r['formulation'] for r in rows]
    fig,ax=plt.subplots(1,2,figsize=(12,6.8),gridspec_kw={'width_ratios':[1.3,1]});y=np.arange(len(rows));ax[0].errorbar(g,y,xerr=ge,fmt='o',capsize=3,color='#186e83');ax[0].set(yticks=y,yticklabels=labels,xlim=(55,109),xlabel=tr('凝胶分数 / %','Gel fraction / %'),title=tr('A  公开表格中的凝胶分数','A  Gel fractions from a published table'));ax[0].invert_yaxis()
    colors=['#186e83']*3+['#cd803f']*3+['#8160a1']*6
    for i in range(len(rows)):ax[1].errorbar(g[i],m[i],xerr=ge[i],yerr=me[i],fmt='o',color=colors[i],alpha=.8,capsize=2)
    ax[1].set(xlabel=tr('凝胶分数 / %','Gel fraction / %'),ylabel=tr('弹性模量 / kPa','Elastic modulus / kPa'),title=tr('B  质量连入网络与刚度并非一一对应','B  Network mass and stiffness are not one-to-one'))
    ax[1].text(.04,.96,tr('蓝：HAMA\n橙：GelMA\n紫：混合网络','Blue: HAMA\nOrange: GelMA\nPurple: mixed networks'),transform=ax[1].transAxes,va='top',fontsize=10)
    fig.suptitle('Velasco-Rodriguez et al. (2021), Table 1 · CC BY 4.0',fontsize=11);fig.tight_layout();save(fig,'published')
    summary={'worked_example':{'network_mg':64.,'raw_fraction_percent':84.,'polymer_fraction_percent':80.,'sol_fraction_percent':20.,'closure_percent':99.2},'extraction':{'cycle1_corrected_percent':float(corrected[1]),'cycle3_corrected_percent':float(corrected[3]),'cycle6_trapped_mg':float(trapped[6])},'specimens':{'mean_percent':float(measured.mean()),'sd_percent':float(measured.std(ddof=1))},'published':{'rows':len(rows),'hama_modulus_ratio':m[2]/m[0]},'connectivity':{'largest_cluster_sizes':sizes}}
    assert abs(corrected[1]-86)<1e-12;assert abs(corrected[3]-80.54)<1e-12;assert abs(residual[-1]+sum(removed)-100)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

运行后可以先核对第一轮的百分之八十六和第三轮的百分之八十点五四，再检查各轮提取物与最终残留相加是否回到初始一百毫克。随后把每轮去除比例从零点七改成零点三，观察达到相同终点误差需要多少轮；或者把填料比例改大，比较未校正和校正结果之间的差距。这个练习帮助确定实际实验最需要增加哪类信息：延长提取、测定填料、提高回收，还是增加独立样品。

记录结果时，应把样品编号、初始干质量、最终干残留、提取条件和组成校正放在同一条数据链中。对于柔软凝胶，照片可帮助说明提取后是否仍保持完整；对于颗粒复合材料，提取液中的浑浊和沉降物值得单独检查；对于可降解网络，随时间持续损失质量应与独立降解实验相互参照。这些观察不是额外的装饰，而是帮助解释为什么一份质量差代表可溶链移出，另一份却可能包含网络破碎。

下一章将把时间本身变成研究变量，观察材料在环境中如何逐渐降解。凝胶分数实验希望在定义好的提取过程中识别初始网络与可溶部分；降解实验则关注连接或主链随时间改变以后，质量、分子量、结构和功能如何演化。先把起始网络比例弄清楚，就能更有把握地判断后续质量减少来自原有可溶物的早期流失，还是材料在环境作用下形成了新的可溶片段。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [IUPAC Gold Book: gel fraction](https://goldbook.iupac.org/terms/view/GT07551)

   网络质量分数的术语定义。

   Definition reference; no assets reproduced.
2. [Stockmayer (1943). Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers](https://doi.org/10.1063/1.1723803)

   成胶与分支尺寸分布的历史原始论文。
3. [Kovac and Fixman (2017). Walter H. Stockmayer, National Academy of Sciences Biographical Memoir](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf)

   核对 Flory 1941 与 Stockmayer 1943–1944 的研究关系。

   Historical reference; no photographs or text reproduced.
4. [Hiroki et al. (2011). Biodegradability of Blend Hydrogels Based on Carboxymethyl Cellulose and Carboxymethyl Starch](https://www.jstage.jst.go.jp/article/tmrsj/36/3/36_397/_pdf)

   原始实验中的提取、干质量与溶胀定义。
5. [Velasco-Rodriguez et al. (2021). Hybrid Methacrylated Gelatin and Hyaluronic Acid Hydrogel Scaffolds](https://www.mdpi.com/1422-0067/22/13/6758)

   真实网络凝胶分数与模量数据，以及提取程序。

   CC BY 4.0; Table 1 data transcribed and plotted with attribution.
