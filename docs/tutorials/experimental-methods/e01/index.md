# 溶胀实验：水如何进入高分子网络

Source: https://ml-biomat.com/tutorials/experimental-methods/e01/
Language: zh-CN

从干湿质量与分母定义出发，把吸水、尺寸变化、网络连接和生物材料的使用状态联系起来。

## 一片敷料吸进水以后，改变的不只是重量

把一片干燥水凝胶放进水里，它可能像海绵一样变大，却又与海绵有重要区别。海绵里的水主要占据肉眼可见或显微镜下可见的孔隙；许多水凝胶中的水还进入了高分子链之间，使原来卷曲的链段逐渐伸展。用于伤口敷料时，这个过程关系到吸收液体的能力；用于软骨替代材料时，它会改变尺寸和承载能力；用于细胞培养时，细胞接触到的软硬程度也可能随浸泡时间变化。溶胀实验就是把这些变化变成可比较的质量、体积和时间记录。

想象一个由许多橡皮筋连接起来的渔网。小水分子能钻进网中，网结又把长链连成整体，使它们不能像糖分子那样各自散开。这个比喻把两个过程分开了：溶剂进入材料叫吸收，材料因此增大叫溶胀；长链脱离整体并分散到液体中则是溶解。真实凝胶可能同时吸水、释放未连接的链，甚至发生化学降解，所以单看最后一次称重，往往还看不清过程中发生了什么。完整实验需要记录样品从哪一种状态出发，以及浸泡后哪些物质仍然留在里面。

日常语言中的“吸水十倍”尤其值得拆开。有人用湿样品质量除以干样品质量，有人用吸收的水除以干样品质量，还有人说的是体积变化。假设干材料为零点一克，吸水后的总质量为一克：前一种质量比为十，后一种吸水量比为九，水占湿样品的质量百分数则是百分之九十。三个答案都能描述同一块材料，却回答了三个不同问题。读论文时先找到分子和分母，比先比较数字大小更有帮助。

本章沿着一块凝胶的经历展开：先认识网络为什么吸水，再把称重结果转换成明确的比例，接着设计浸泡、取样和干燥过程，最后读懂时间曲线。计算例子使用可重复生成的教学数据，另有一幅公开论文中的真实实验图，可以对照观察理想曲线与实验中有限采样、误差条和材料差异的关系。学完以后，面对“这个配方吸水更多”的结论，你可以进一步判断它指的是何种状态、何种环境，以及这一变化对材料用途意味着什么。

## 水想进入，网络又把链拉回来

水分子和高分子链一直在热运动。对于适合吸水的聚合物，水与链混合后，可以形成更多可能的分子排列，同时发生氢键等相互作用。把水想成在许多房间之间走动的人，有助于理解混合倾向：当内部提供了可以进入的位置，分子会在内外交换，直到两边对水的“吸引程度”达到平衡。这里更准确的物理量叫化学势，它描述增加少量某种物质时体系自由能的变化。初学时可以先抓住方向：水的化学势存在差别，就有推动水迁移的原因。

网络并不会无限扩张。连接在一起的链被拉得更开时，可自由采取的卷曲姿态减少，网络因此产生回缩倾向。溶剂混合推动膨胀，链的弹性抵抗膨胀，两者共同决定最终尺寸。交联点可以是共价键，也可以来自离子结合、氢键、结晶区或蛋白质之间的可逆作用；它们稳定的时间尺度和环境不同。海藻酸盐凝胶在含有竞争离子的液体中可能改变连接状态，明胶的物理网络也会随温度变化，因此“放进水里”还需要说清楚水的温度和组成。

一九四三年，Flory 与 Rehner 把溶剂混合和交联网络弹性放在同一个统计力学框架中研究，讨论了硫化橡胶等网络的溶胀。这段历史的价值，是把肉眼看到的变大同看不见的链连接起来，而不是给任何凝胶套上一个固定换算表。现代水凝胶可以含有带电基团、蛋白质、多种交联方式和显著的结构不均匀性。理解这条历史线索后，就能知道为什么需要先检查网络种类和参考状态，再讨论由溶胀反推交联密度。

![网络示意：自由与基底固定的溶胀。网格是原理图，蓝色小圆表示水；历史注释连接 1943 年的混合与弹性理论。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/708c40f16b8ada426ff6a630.svg?v=708c40f16b8a)

图 1网络示意：自由与基底固定的溶胀。网格是原理图，蓝色小圆表示水；历史注释连接 1943 年的混合与弹性理论。

带电网络还多了一层原因。固定在链上的电荷需要附近的可移动离子维持电中性，凝胶内部和外部的离子组成因而可能不同，产生额外的渗透作用。向外液加盐通常会减弱某些离子凝胶的溶胀驱动力，但具体变化还取决于离子价态、结合反应和酸碱条件。把这些影响想成“盐让水变重”会走错方向：关键是离子的分布和它们与网络的相互作用。同一个配方在纯水、生理盐水和细胞培养基中的结果，可能对应三个不同的平衡状态。

网络的边界同样重要。一块自由漂浮的均匀凝胶可以向三个方向扩张；如果底面粘在玻璃上，平面内的扩张受到限制，厚度和内部应力就会以另一种方式变化。图中的网格把这件事画出来：相同的吸水倾向遇到不同的固定方式，得到的形状并不相同。研究细胞在凝胶表面的行为时，这个区别非常实际，因为培养用的薄胶往往固定在基底上，而称量用的样品却可能是自由圆片。比较两者，需要把边界条件一起带进解释。

## 从天平读数走到含水量和体积

先为质量取清楚的名字。干燥后属于网络材料的质量记作干质量，去掉表面游离液体后的湿样品质量记作湿质量。两者之差对应样品保留的液体质量，前提是浸泡期间没有未计入的材料流失或溶质沉积。用湿质量除以干质量，得到每克干材料对应多少克湿样品；减去一，就得到每克干材料吸收多少克液体。比值中的克相互约去，因此它是无量纲的，写成克每克则可以帮助读者记住分母。

$$
Q_m=\frac{m_w}{m_d},\qquad q=\frac{m_w-m_d}{m_d}=Q_m-1,\qquad w_w=\frac{m_w-m_d}{m_w}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f827cd558a9b7c38c0686e49.svg) | 湿质量与干质量之比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | 去除外部液体后的湿样品质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | 作为基准的干聚合物质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 保留液体质量与干质量之比，无量纲，常写 g/g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e5b197dd107c875b96b8f1b.svg) | 水在湿样品中的质量分数，无量纲；乘 100 得百分数。 |

干质量 0.10 g、湿质量 1.00 g 时，Qm=10，q=9，ww=0.90。质量差表示液体质量，条件是干物质组成与材料流失已纳入质量核算。

公式中的含水质量分数使用湿样品作为分母，取值在零与一之间。干质量零点一克、湿质量一克时，九成湿质量来自水，剩余一成来自聚合物。若把百分数写成百分之九百，那说的是“水质量相对干材料质量”的百分比，而不是水在湿样品中所占的比例。错误常发生在把表头“溶胀率”照抄过来，却没有同时抄下定义。保存原始干湿质量，可以在以后用同一组数据重新计算不同定义，避免只剩一个无法追溯的百分数。

质量比与体积比之间需要密度这座桥。密度表示单位体积中有多少质量，所以质量除以密度得到体积。如果干聚合物密度比水高，同样质量的聚合物占据的体积更小，湿体积与干体积之比就可能大于湿质量与干质量之比。下面的换算假设聚合物和溶剂体积近似可加，干质量确实对应聚合物，且所用密度适合当前温度和组成。含大量无机填料、闭孔或强烈体积收缩的体系，需要分别处理这些额外组成。

$$
Q_V=\frac{m_d/\rho_p+(m_w-m_d)/\rho_s}{m_d/\rho_p}=1+\frac{\rho_p}{\rho_s}(Q_m-1),\qquad \phi_p=\frac{1}{Q_V}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0c8e72b6b5d491a201d0a4d9.svg) | 湿体积与干聚合物体积之比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | 干聚合物质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | 湿样品质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e04e40ff4b2959cf46147e6c.svg) | 干聚合物密度，g/cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/72df456d8963cb97ca755642.svg) | 溶剂密度，g/cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f827cd558a9b7c38c0686e49.svg) | 湿干质量比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/68346d656e91e3fc34903833.svg) | 湿样品中的聚合物体积分数，无量纲。 |

质量除以密度得到体积；在体积近似可加条件下相加。Qm=10、ρp=1.2 g/cm³、ρs=1.0 g/cm³ 时，QV=11.8，φp≈0.08475。

![同一教学样品的质量组成和三个比值。干聚合物 0.10 g、内部水 0.90 g，体积比采用给定密度换算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9fa9cbb613e9bfe68ada9a45.svg?v=9fa9cbb613e9)

图 2同一教学样品的质量组成和三个比值。干聚合物 0.10 g、内部水 0.90 g，体积比采用给定密度换算。

取聚合物密度为每立方厘米一点二克、水为每立方厘米一克，上述样品的干聚合物体积约为零点零八三三立方厘米，水体积为零点九立方厘米，总体积约为零点九八三三立方厘米。两者相除得到体积比十一点八，聚合物体积分数约为零点零八四七五。这里的体积分数描述聚合物在湿材料总体积中占多少，与质量分数零点一不同。链间距离、溶剂迁移和某些网络模型常与体积分数相关，所以不能把质量分数直接代替进去。

如果材料均匀、自由并且各个方向等比例伸展，长度伸长倍数是体积比的立方根：长、宽、高各乘一个相同倍数，三个倍数相乘才得到体积变化。体积比十一点八对应长度约为原来的二点二七七倍。这个计算的参考是干态，而许多凝胶在制备完成时就含有大量水；从制备态到平衡态的伸长，应使用两种状态的体积之比。对于固定在玻璃上的薄层，三个方向的伸长本来就不相同，更适合分别测量厚度和面内尺寸。

$$
\lambda=\left(\frac{V}{V_0}\right)^{1/3},\qquad \lambda_{\mathrm{dry}}=Q_V^{1/3}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 相对于所选参考状态的等向长度伸长倍数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 当前体积，cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | 参考状态体积，cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2b72c1ebdf16f54dc902b630.svg) | 以干态为参考的等向伸长倍数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c8e72b6b5d491a201d0a4d9.svg) | 湿体积与干聚合物体积之比，无量纲。 |

等向自由溶胀时，三个长度方向各乘 λ，体积乘 λ³。QV=11.8 给出相对于干态的 λ≈2.277；基底固定的情况应分别处理方向。

## 把浸泡和称重设计成一条完整证据链

实验开始前先确定要比较什么。若研究敷料吸收渗液的表现，可以关注规定时间内的吸液量和受压后的保液量；若研究细胞培养基底，就应考虑培养温度、液体组成以及材料是否固定；若研究交联网络，则需要把可溶组分先充分提取出来，或同步测量它的损失。目标一旦明确，样品尺寸、浸泡体积、取样时间和参考质量才有共同依据。不同目标得到的“溶胀能力”并不需要排成一个唯一的性能排行榜。

每份独立样品应有自己的编号和干质量。裁切尺寸影响水走到内部的距离，边缘缺口又可能加快进入或造成碎片脱落，因此记录厚度和直径很有价值。样品间干质量不必完全相等，但应先逐份归一化，再计算组内平均值。把三个湿质量先相加，再除以三个干质量之和，会得到按干质量加权的总体比值；它与每份样品比值的普通平均回答的统计问题不同。代码保留每一份样品的称重轨迹，便于看出异常来自哪一份。

浸泡液应足以维持研究设定的外部环境。样品释放盐、酸、未反应单体或可溶聚合物时，小体积外液的组成会随时间改变，进一步影响溶胀。容器加盖可以减少蒸发，温度稳定可以减少平衡状态和迁移速率的漂移。若更换外液，应记录体积、时间和操作方式；若保留同一份外液，也应说明这一设计。对离子或酸碱敏感的凝胶，测量浸泡前后的酸碱度或电导率，常能解释只看质量时难以理解的差异。

取出湿样品后，表面挂着的液滴不是网络内部的水。轻触吸水纸、固定沥液时间或使用其他经过比较的去液方法，都应保持接触方式和持续时间一致。用力挤压会把内部液体挤出，等太久又会让样品蒸发变轻。可以先对几份同类样品比较操作重复性，选择在可控时间内稳定的步骤。天平称量容器的空重也要记录；如果样品连同玻璃片一起称量，就必须扣除玻璃本身及可能残留在其上的外部液体。

干燥过程决定分母的含义。烘干、真空干燥和冷冻干燥会带来不同的温度与结构历史，应选择适合材料稳定性的方式，并通过间隔称量检查质量是否达到稳定。缓冲盐和其他不挥发溶质会留在干样品中，不能自动当作聚合物。需要聚合物干质量时，可设置充分换液去盐、空白残留测量或独立组成分析，并检查这一处理有没有同时溶掉网络。把“干到恒重”与“只剩聚合物”分开理解，是准确称量的关键一步。

## 快慢、平衡和厚度，分别告诉我们什么

安排时间点时，还应考虑操作本身需要多久。若逐份取出、去液、称量、放回，一组样品的实际浸泡时间可能相差数分钟；对于快速吸水薄膜，这个差别已经足以改变比较。可以错开起始时间，逐份记录真实时间戳，或在每个时点使用独立样品。独立样品避免反复操作影响后续轨迹，连续称量同一份样品则能保留个体的完整变化，两种设计分别适合不同问题。

一条典型溶胀曲线开始上升较快，随后逐渐接近平台。开始时内外状态相差大，表层又最先接触液体；随着水进入，迁移的距离增加，驱动力也会改变。平台表示在当前观察时间和测量精度下质量变化变小。判断平衡时，可以预先设定相邻几次称量的相对变化阈值和时间间隔，而不是只规定所有材料都浸泡一天。若缓慢降解正在增加吸水空间，或者可溶物仍在释放，曲线可能持续变化，此时应同时观察干质量与材料形态。

为了练习从数据读出两个信息，代码使用一个单指数接近平衡的模型：最终能达到多少，以及以多快的速度接近它。模型从初始质量比三出发，接近平衡质量比十，时间参数为四十五分钟。这个时间参数表示变化完成约百分之六十三点二所需的时间；它不是达到完全平衡的时刻。经过三倍时间参数，约完成百分之九十五的变化。这种近似适合描述单一主导时间过程的曲线形状，也能作为比较样品的经验指标。

$$
Q_m(t)=Q_0+(Q_\infty-Q_0)\left(1-e^{-t/\tau}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38da52f1cae2f9d507f1a8ad.svg) | 时间 t 时的模型湿干质量比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/60aeca77be2527e34462d75b.svg) | 初始质量比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dc1bd1301b77fa0c9082a354.svg) | 模型长期极限质量比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过的时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 单指数时间参数，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底数，约 2.71828，无量纲。 |

此经验模型表示剩余变化量以固定相对速率减少。Q0=3、Q∞=10、τ=45 min 时，t=45 min 的比值约为 7.42484，完成总变化的 63.212%。

![构造的三份样品从原始湿质量、逐样品归一化走到拟合和残差；误差条为样品间 SD。右下图单独改变模型时间参数以解释厚度平方标度。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7566013739e5108c09cb6cbc.svg?v=7566013739e5)

图 3构造的三份样品从原始湿质量、逐样品归一化走到拟合和残差；误差条为样品间 SD。右下图单独改变模型时间参数以解释厚度平方标度。

图中先展示三份样品的原始湿质量，再展示逐份归一化后的平均值和样品间标准差。误差条来自三份独立样品在同一时间点的比值差异，而不是天平说明书上的精度，也不是同一读数重复保存三次得到的差异。拟合使用每个时间点的平均比值，残差图则检查观测值与拟合曲线之差有没有明显趋势。若早期全部在曲线上方、后期全部在下方，单一时间参数可能把两个不同过程挤在了一起，应增加机制检查和相应时间点。

厚度实验很适合检验迁移的作用。对于扩散或某些孔弹性控制的过程，在几何形状和边界条件相似、有效迁移系数近似不变时，特征时间随迁移长度的平方变化。直观上，分子的热运动反复改变方向，走到两倍远处平均需要更长的探索过程，时间因而可增加到四倍。图中把一毫米样品的时间参数设为四十五分钟，二毫米样品则为一百八十分钟。这个关系帮助安排采样，并不意味着任意凝胶只要厚两倍就必定慢四倍。

$$
\tau\propto\frac{L^2}{D},\qquad \frac{\tau_2}{\tau_1}=\left(\frac{L_2}{L_1}\right)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7a8cd924f632d8dad8901100.svg) | 相似几何条件下的特征时间及两份样品的特征时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8e40a7acd8098e65ecb98265.svg) | 迁移距离及其两份样品的取值，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 有效迁移系数，m²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d9c6c40f15e6a090e4bcafe4.svg) | 表示成正比，具体几何系数由边界条件决定。 |

在几何、边界和 D 保持可比的扩散或相应孔弹性标度下，长度翻倍使时间增至四倍。教学曲线的 1 mm 与 2 mm 样品分别使用 45 min 和 180 min；本式不单独确定 D。

若材料有致密表皮、各向异性结构或明显的网络松弛，厚度与时间之间可能出现不同关系。薄片两面都接触水，与底面被玻璃封住的情况，也有不同的有效迁移距离和数值系数。要从拟合时间反推出扩散系数，应选用与形状、边界和耦合力学相符的解；本章将平方标度用于解释趋势，把具体扩散系数的测量留给扩散与渗透实验。这样，经验拟合负责概括曲线，物理模型负责连接材料内部过程，两者各有清楚的位置。

## 让误差显形，再看真实材料

天平显示的最后一位数字，也要结合样品大小理解。同样一毫克的质量误差，对十毫克干样品和一百毫克干样品有不同的相对影响。检查天平状态、避免气流和静电、缩短暴露空气的时间，有助于稳定读数；增加独立样品则帮助了解材料本身的差异。把称量重复性与样品间差异分别测量，才能判断接下来应改进操作还是改进制备的一致性。

称量中的小偏差可以沿着比值放大。干质量只有零点一克的样品，若表面多挂了二十毫克液体，质量比会从十变成十点二；若干燥后多留下十毫克盐，而湿质量仍是一克，用这个偏大的分母计算就只剩约九点零九。两个错误方向相反，有时还会碰巧互相抵消，所以结果“看起来合理”并不足以确认步骤正确。图中分别改变表面液体和残留盐，让分子、分母的作用独立显现。

![构造的称量偏差：表面液体增加湿质量，残留盐增加干质量。两图分别改变一种偏差，虚线表示没有偏差时的质量比十。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7b2518c5639462b3a2b6a6fc.svg?v=7b2518c56394)

图 4构造的称量偏差：表面液体增加湿质量，残留盐增加干质量。两图分别改变一种偏差，虚线表示没有偏差时的质量比十。

下面的交互实验保留同一块零点一克干聚合物和零点九克内部水，只改变称量时残留的表面液体与干燥后残留的盐。拖动滑块时，真正的网络含水状态不变，计算出的质量比却会变化。尝试找出一种两类偏差恰好抵消、显示值接近十的组合，再分别把其中一项归零，就能看到补偿现象。实际研究中，与其寻找“正确数字”，更有效的是通过空白、标准化去液和组成测量，让每个读数都对应明确物质。

## 改变称量偏差，观察同一块凝胶

内部始终有 0.10 g 聚合物与 0.90 g 水。分别改变外部液体和干燥残留盐，比较表观质量比与真实值。

[Figure: 真实与表观质量比](https://ml-biomat.com/tutorials/experimental-methods/e01/#E01-plot)

真实研究的曲线提供了另一层观察。Subramani 等人研究了固定在基底上的聚丙烯酰胺凝胶，在不同浸泡时间测量溶胀，并与力学变化相联系。下图保留原论文的坐标、数据点和误差条，可以看到不同配方的时间响应并不相同；某些材料的变化在较早时段更明显，另一些则相对稳定。原图中的纵轴是该论文定义的体积溶胀比，读它时应回到湿干质量和密度换算，而不是把数值直接当成含水质量百分数。

![真实实验原图：Subramani 等（2020），图 4，Frontiers in Materials，DOI 10.3389/fmats.2020.00212，CC BY 4.0。A 为较长时间尺度，B 为较短时间尺度，纵轴为原文体积溶胀比，误差条为 SD。原图科学内容未改变，新增中英文外标题与署名；原图标签保留英文。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4e9de513b39ccb8fb60ad068.svg?v=4e9de513b39c)

图 5真实实验原图：Subramani 等（2020），图 4，Frontiers in Materials，DOI 10.3389/fmats.2020.00212，CC BY 4.0。A 为较长时间尺度，B 为较短时间尺度，纵轴为原文体积溶胀比，误差条为 SD。原图科学内容未改变，新增中英文外标题与署名；原图标签保留英文。

把这幅真实实验图与前面的教学曲线并排理解，还能学会一个实用的阅读顺序：先看横轴时间跨度，再看纵轴的参考状态，然后看每个点代表多少独立样品，最后比较配方间的差异。误差条有重叠时，不能仅凭肉眼把差异划成“存在”或“不存在”；应结合完整数据、实验重复和针对研究问题的统计比较。对于细胞培养应用，尤其值得把溶胀曲线和同一状态下的力学测量对应起来，确认细胞接触时的尺寸与软硬程度。

## 把一组质量数据整理成可以继续研究的结果

还有一个容易混淆的结构尺度：网络模型中的网孔尺寸描述链段和连接之间的统计尺度，干燥显微图里看到的大孔则可能受到冻干、相分离或制样影响。二者可以共同研究，却不能只凭名称相似就直接对应。若希望知道蛋白质能否穿过湿网络，可以把溶胀测量与示踪分子的扩散、吸附及尺寸信息结合起来；这些实验比单独放大一幅干态孔洞照片更接近分子的真实运动环境。

完整程序保留了从质量到结论的中间步骤。它为三份样品设置各自的干质量，在一组固定时间点生成带有小幅称量波动的教学湿质量；随后逐样品计算湿干质量比，得到平均值和样品间标准差，再拟合平衡质量比与时间参数。导出的表格既含原始湿质量，也含平均比值、标准差和拟合值，读者可以重新作图或更换拟合范围。代码固定随机种子，所以重新运行得到的是同一组教学记录，便于核对手算结果。

### 完整 Python：溶胀质量核算、拟合与误差诊断

执行后导出原始质量、归一化结果、拟合参数及本章五幅图。公开原图和许可说明随示例打包，运行无需联网。

```
"""Mass/volume swelling and a constructed time series; includes a licensed published figure."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def uptake(t,initial,equilibrium,time_scale):
    return initial+(equilibrium-initial)*(1-np.exp(-np.asarray(t)/time_scale))

def ratios(dry,wet,rho_polymer=1.2,rho_water=1.):
    mass=wet/dry
    volume=1+rho_polymer/rho_water*(mass-1)
    return {'mass_ratio':mass,'water_per_dry':mass-1,'water_fraction':1-1/mass,
            'volume_ratio':volume,'polymer_volume_fraction':1/volume,'isotropic_stretch':volume**(1/3)}

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    result=ratios(.1,1.)
    rng=np.random.default_rng(101)
    times=np.array([0,5,10,20,30,45,60,90,120,180,240.])
    dry=np.array([.098,.102,.100]);truth=uptake(times,3,10,45)
    wet=dry[:,None]*truth+rng.normal(0,.003,(3,len(times)))
    observed=wet/dry[:,None];mean=observed.mean(0);sd=observed.std(0,ddof=1)
    fit,cov=curve_fit(lambda t,qinf,tau:uptake(t,3,qinf,tau),times,mean,p0=[9,40],bounds=([3,1],[20,1000]))
    prediction=uptake(times,3,*fit);smooth=np.linspace(0,240,400)
    np.savetxt(output/'swelling.csv',np.column_stack([times,*wet,mean,sd,prediction]),delimiter=',',header='time_min,wet_g_1,wet_g_2,wet_g_3,mean_mass_ratio,sd_mass_ratio,fitted_ratio',comments='')
    np.savetxt(output/'dry_masses.csv',dry,delimiter=',',header='dry_mass_g',comments='')
    fig,ax=plt.subplots(1,3,figsize=(12,4.4));nodes=np.array([[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]],float)
    for k,stretch in enumerate([1,1.65,1.65]):
        a=ax[k];a.set_aspect('equal');a.axis('off');coords=nodes*stretch
        if k==2:coords[:,0]=nodes[:,0]
        for i,j in [(0,1),(1,2),(3,4),(4,5),(6,7),(7,8),(0,3),(3,6),(1,4),(4,7),(2,5),(5,8)]:
            a.plot(coords[[i,j],0],coords[[i,j],1],color='#186e83',lw=3)
        a.scatter(*coords.T,s=35,color='#cd803f',zorder=3)
        for x,y in [(0.5,.5),(1.5,.5),(.5,1.5),(1.5,1.5)]:a.add_patch(Circle((x*(stretch if k<2 else 1),y*stretch),.12,color='#a2cdd9'))
        if k==2:a.plot([-.3,2.3],[-.15,-.15],color='#707c82',lw=7)
        a.set(xlim=(-.5,3.8),ylim=(-.6,3.8));a.set_title(tr(['A  制备时的网络','B  自由溶胀','C  底面固定'][k],['A  As-prepared network','B  Free swelling','C  Substrate constraint'][k]),loc='left')
    fig.text(.5,.01,tr('1943：Flory 与 Rehner 将溶剂混合与网络弹性放进同一理论。','1943: Flory and Rehner joined solvent mixing with network elasticity.'),ha='center');save(fig,'network')
    fig,ax=plt.subplots(1,2,figsize=(11,4.5));ax[0].bar(tr(['干聚合物','水'],['Dry polymer','Water']),[.1,.9],color=['#cd803f','#186e83']);ax[0].set(ylabel=tr('质量 / g','Mass / g'),title=tr('A  湿样品 1.00 g 的组成','A  Composition of a 1.00 g wet specimen'))
    labels=tr(['湿 / 干质量','吸水 / 干质量','湿 / 干体积'],['Wet / dry mass','Water / dry mass','Wet / dry volume']);ax[1].barh(labels,[10,9,11.8],color=['#186e83','#3c8a6a','#8160a1']);ax[1].set(xlabel=tr('比值 / 无量纲','Ratio / dimensionless'),title=tr('B  三个分母明确的量','B  Three explicitly defined ratios'),xlim=(0,14))
    for i,v in enumerate([10,9,11.8]):ax[1].text(v+.15,i,f'{v:g}',va='center')
    fig.tight_layout();save(fig,'ratios')
    fig,ax=plt.subplots(2,2,figsize=(11,7.3));ax=ax.ravel()
    for i in range(3):ax[0].plot(times,wet[i],'.-',alpha=.7,label=f'{i+1}: {dry[i]:.3f} g')
    ax[0].set(title=tr('A  三份样品的原始湿质量','A  Raw wet masses of three specimens'),ylabel=tr('湿质量 / g','Wet mass / g'));ax[0].legend(fontsize=9)
    ax[1].errorbar(times,mean,yerr=sd,fmt='o',ms=4,label=tr('均值 ± 样品间 SD','Mean ± between-specimen SD'));ax[1].plot(smooth,uptake(smooth,3,*fit),label=tr('单指数拟合','Single-exponential fit'));ax[1].set(title=tr('B  先逐样品归一化，再汇总','B  Normalize each specimen before averaging'),ylabel=tr('湿 / 干质量比','Wet / dry mass ratio'));ax[1].legend(fontsize=9)
    ax[2].axhline(0,color='#707c82',lw=.8);ax[2].plot(times,mean-prediction,'o-');ax[2].set(title=tr('C  残差检查','C  Residual inspection'),ylabel=tr('观测值 − 拟合值','Observed − fitted'))
    for h in [.5,1,2]:ax[3].plot(smooth,uptake(smooth,3,10,45*h*h),label=f'{h:g} mm')
    ax[3].set(title=tr('D  固定几何假设下的厚度效应','D  Thickness effect under fixed geometry'),ylabel=tr('模型质量比','Model mass ratio'));ax[3].legend()
    for a in ax:a.set_xlabel(tr('时间 / min','Time / min'))
    fig.tight_layout();save(fig,'kinetics')
    fig,ax=plt.subplots(1,2,figsize=(11,4.5));film=np.linspace(0,.05,100);salt=np.linspace(0,.02,100)
    ax[0].plot(film*1000,(1+film)/.1);ax[0].set(xlabel=tr('残留表面液体 / mg','Residual surface liquid / mg'),ylabel=tr('计算质量比','Calculated mass ratio'),title=tr('A  表面液体抬高分子','A  Surface liquid raises the numerator'))
    ax[1].plot(salt*1000,1/(.1+salt),color='#cd803f');ax[1].set(xlabel=tr('干燥后残留盐 / mg','Salt remaining after drying / mg'),ylabel=tr('计算质量比','Calculated mass ratio'),title=tr('B  残留盐抬高分母','B  Residual salt raises the denominator'))
    for a in ax:a.axhline(10,color='#707c82',ls='--');a.grid(alpha=.15)
    fig.tight_layout();save(fig,'artifacts')
    from PIL import Image
    published=np.asarray(Image.open(Path(__file__).with_name('subramani2020-figure4.webp')))
    fig,ax=plt.subplots(figsize=(11,4.8));ax.imshow(published);ax.axis('off');ax.set_title(tr('真实实验：固定在基底上的凝胶随时间溶胀','Published measurements: swelling of substrate-attached gels'),pad=14)
    fig.text(.5,.015,'Subramani et al. (2020), Figure 4 · Frontiers in Materials · CC BY 4.0',ha='center',fontsize=9);save(fig,'published')
    summary={'worked_example':result,'fit':{'equilibrium_mass_ratio':float(fit[0]),'time_scale_min':float(fit[1])},'checks':{'initial_ratio':float(uptake(0,3,10,45)),'one_time_scale_fraction':float((uptake(45,3,10,45)-3)/7),'fourfold_time_scale_at_double_thickness':4.,'surface_20mg_ratio':10.2,'salt_10mg_ratio':1/.11}}
    assert abs(result['volume_ratio']-11.8)<1e-12
    assert abs(result['water_fraction']-.9)<1e-12
    assert abs(summary['checks']['one_time_scale_fraction']-(1-np.exp(-1)))<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

第一次运行时，可以先核对三个容易手算的结果：湿干质量比为十、水的质量分数为零点九、使用给定密度后的体积比为十一点八。确认这些换算后，再观察拟合参数是否接近生成数据时的设定。接着把最晚几个时间点删去重新拟合，会发现只记录早期上升段时，最终平台与时间参数更容易相互补偿。这说明增加更早的采样可以改善快速过程的分辨，而延长观察则帮助确定平台；两种改进针对不同的信息缺口。

写结果时，可以围绕一个明确问题组织证据。例如比较两种敷料，可先展示独立样品的吸液时间曲线，再报告规定时间的吸液量、平衡状态以及受压保液表现；比较培养基底，则需要把固定方式、培养环境、尺寸变化和力学状态连接起来。图题写清质量比或体积比的定义，表格保留干湿质量和样品编号，正文解释变化为何影响实际用途。读者就能从一条曲线继续走向材料选择，而不只是记住一个较大的吸水数字。

溶胀还自然引出下一项实验：如果一块材料在浸泡后变得更轻，究竟是原有水被移走，还是一部分高分子没有真正连成网络而被提取出去？凝胶分数测量把注意力转向提取前后的干物质，并与本章的含水量形成互补。先知道留下多少网络，再讨论这些网络吸收多少水，会让交联、溶解和降解之间的关系清楚得多，也为后续的释放和扩散研究建立可靠的质量基准。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Subramani et al. (2020). The Influence of Swelling on Elastic Properties of Polyacrylamide Hydrogels](https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2020.00212/full)

   体积换算、基底约束与真实溶胀曲线；原图 4 获许可复用。

   CC BY 4.0; Figure 4 credited in caption and bundled notice.
2. [Flory and Rehner (1943). Statistical Mechanics of Cross-Linked Polymer Networks II. Swelling](https://doi.org/10.1063/1.1723792)

   混合与网络弹性理论的历史原始文献。
3. [Sheth et al. Measurement of Hydrogel Swelling Ratio and Mesh Size](https://bio-protocol.org/exchange/minidetail?id=4024598&type=30)

   识别制备态、湿态、干态三个参考状态及持续降解问题。

   CC BY as stated for the extracted research method; no figure reused.
4. [Sheth et al. (2019). Predicting Drug Release From Degradable Hydrogels Using Fluorescence Correlation Spectroscopy and Mathematical Modeling](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00410/full)

   将网络溶胀与分子迁移和降解联系起来。
5. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   有界非线性拟合接口与参数意义。
