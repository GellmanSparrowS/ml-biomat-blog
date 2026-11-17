# 核磁共振：从核自旋到分子结构

Source: https://ml-biomat.com/tutorials/experimental-methods/s06/
Language: zh-CN

以真实乙醇峰表为线索，把自旋、化学位移、耦合、时间信号与积分连接起来，再走向聚合物和蛋白质。

## 一杯透明溶液里，分子怎样连接？

两瓶透明液体看起来没有差别，里面的分子却可能完全不同；同一种聚合物在反应前后也可能保持透明，只是少量侧基发生了变化。红外能够帮助寻找某些化学键，色谱能够把混合物分开，而核磁共振会进一步利用原子核周围的磁环境，提供化学位置、相邻关系和相对数量的信息。它的名字常让人想到医院里的磁共振成像。两者共享核自旋与磁共振的物理基础，只是这里主要关注分子内部的化学差别，而不是人体不同位置的图像。

核磁共振简称 NMR。常见的氢谱主要观察氢原子核，也就是质子；碳谱常观察碳的同位素 ¹³C。不是每一种原子核都能以相同方式参与这项测量，核的自旋性质与天然丰度会影响信号。初学时可以先把谱图当成一个分子环境的“频道表”：不同环境在不同位置出现响应，相互作用让某些频道分裂成一组线，合适条件下的面积又提供相对数量。接下来要做的，是理解这些图像特征如何从真实测量产生。

我们用乙醇作为贯穿例子。乙醇含有一个甲基、一个亚甲基和一个羟基，也就是常写的 CH₃、CH₂ 和 OH。它足够简单，能把化学环境、峰的分裂和积分连在一起；它又足够真实，包含溶剂交换与参照条件等问题。本篇读取 BMRB 的公开乙醇条目，展示实际存储的峰表和积分，再另行构造时间信号来学习傅里叶变换。公开数据与教学模型各自负责一个问题，不把重画的理想曲线当成数据库原始谱线。

学习路线从磁场中的核自旋出发，经过化学位移、耦合和时间信号，走到样品准备与定量条件。最后再讨论蛋白质、聚合物和多维谱。掌握这些层次后，你不必先背完所有官能团的位移表，也能判断一张谱图提供了什么信息、哪些设置影响了比较，以及下一项实验应当补充哪一种连接关系。

## 磁场建立差别，射频脉冲让差别变得可测

自旋是原子核的一种量子性质，并不是一个小球按经典方式绕自身轴旋转。某些核同时具有磁矩，因而会与外加磁场相互作用。对自旋为二分之一的核，磁场使两种自旋能级分开；热平衡下，较低能级上的核略多一些。数量差通常只占很小一部分，却在大量原子核共同参与时形成可测的净磁化。把样品放进磁体，并不意味着所有核都整齐朝向同一个方向。

从整体磁化的角度看，可以用陀螺进动帮助理解：一个倾斜的陀螺会绕竖直方向转动，磁化在磁场中也有相应的进动频率。这个类比描述整体运动关系，不替代自旋的量子解释。与进动相匹配的射频磁场能够改变磁化方向，短脉冲使其产生横向分量；横向磁化随时间转动，在接收线圈中感应出电信号。仪器测得的是大量核共同形成的响应，而不是逐个拍摄原子核。

$$
\nu_0=\frac{\gamma}{2\pi}B_0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/73e82b44155602b2e23ac25f.svg) | 拉莫尔共振频率，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 旋磁比，rad·s⁻¹·T⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5926b97aed9157f3038e191c.svg) | 静磁场强度，T。 |

磁矩与磁场相互作用确定主要进动尺度。质子的 γ/(2π) 约为 42.577 MHz/T，9.4 T 给出约 400.2238 MHz；化学环境带来的小修正形成位移。

![原创核感应功能示意连接磁场、样品、射频线圈与感应接收，说明 1946 年工作的核心物理关系。右图用质子旋磁比近似展示频率随磁场变化；图中 9.4 T 对应 400.22 MHz，不包含具体样品的电子屏蔽修正。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6292576e832fb458fb430f98.svg?v=6292576e832f)

图 1原创核感应功能示意连接磁场、样品、射频线圈与感应接收，说明 1946 年工作的核心物理关系。右图用质子旋磁比近似展示频率随磁场变化；图中 9.4 T 对应 400.22 MHz，不包含具体样品的电子屏蔽修正。

1946 年，Bloch 及其合作者、Purcell 及其合作者分别发表了在凝聚态物质中观察核磁响应的工作。两条路线分别强调核感应与共振吸收，却指向共同的物理机制。后来发现同一种核在不同化合物中的共振位置略有差别，这让一项关于核磁矩的物理测量变成了识别化学环境的工具。1966 年 Ernst 与 Anderson 的傅里叶变换磁共振工作，又把脉冲后的时间信号与整段频谱联系起来，改变了获取光谱的方式。

常说的“400 MHz 核磁”通常是按该磁场下的质子共振频率命名，不是说所有核都在 400 MHz 响应。质子的频率与磁场近似按 42.577 MHz/T 的比例增长，所以 9.4 T 对应约 400.22 MHz；同一磁体上的 ¹³C 有不同的旋磁比，因此工作频率也不同。较高磁场可增加以赫兹表示的化学位移间隔，但实际可分辨程度仍取决于线宽、样品和采集条件。

磁体周围的强静磁场持续存在，样品送入前应遵守仪器区对金属物件、植入器械和样品容器的要求。对数据理解来说，更直接的问题是样品所在体积内磁场是否足够均匀。不同位置若经历不同磁场，同一种化学环境也会产生一组不同频率，原本窄的线就被展宽。匀场操作正是调整这种空间差异，让谱线宽度尽量反映分子与实验本身，而不是容器和磁场分布造成的额外影响。

## 化学位移：为什么横轴用 ppm，而且从右向左增加？

正式采集前，样品应在合适溶剂中均匀溶解，装入洁净且尺寸合适的核磁管，并达到稳定温度。未溶颗粒、气泡和不均匀的液柱会扰动局部磁场，既影响匀场，也影响重复性。氘代溶剂减少大量普通溶剂氢带来的背景，并可提供磁场锁定所需的氘信号，但锁定与位移参照是两项任务：前者帮助保持磁场稳定，后者定义化学位移坐标。溶剂本身仍可能有残余氢、水或杂质峰，分析时应识别这些响应，而不是把每条额外线都归给目标分子。

原子核并不是孤立地感受外磁场。周围电子在磁场中的响应会改变核实际经历的局部磁环境，不同化学结构因此产生不同共振位置。与氧相邻的乙醇 CH₂ 和较远的 CH₃ 有不同环境，氢谱位置也随之分开。化学位移是相对于参照信号的频率差，再除以参照频率并以百万分之一表示。这样，同一种环境在不同磁场仪器上的数据就更容易放在同一坐标上比较。

$$
\delta=10^6\frac{\nu-\nu_{\mathrm{ref}}}{\nu_{\mathrm{ref}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 化学位移的 ppm 数值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 目标共振频率，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a066baf94a113b7f4f0c8e7.svg) | 相应参照频率，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/93f6f3a1cafe345159e21225.svg) | 将频率比换为百万分之一的数值因子。 |

先比较目标与参照，再按磁场相关频率尺度归一化。400 MHz 上 1 ppm=400 Hz，600 MHz 上 1 ppm=600 Hz；同样 2 ppm 分别对应 800 与 1200 Hz。溶剂、温度与参照条件需一致或明确记录。

在 400 MHz 仪器上，1 ppm 对应 400 Hz；在 600 MHz 仪器上，1 ppm 对应 600 Hz。因此相差 2 ppm 的两个环境，在前者相差 800 Hz，在后者相差 1200 Hz。ppm 间隔近似保持，而赫兹间隔增大。传统 NMR 图把较高化学位移放在左侧，你会看到横轴从左到右逐渐减小。这个方向是谱图约定，读图时先看刻度，不把左移和右移简单等同于一般坐标图上的增减方向。

参照点同样属于实验。水溶液常使用 DSS 等参照，有机溶剂中常见 TMS；也可以依据合适的残余溶剂信号或仪器参照方案建立坐标。不同溶剂、温度、酸碱条件或分子相互作用会改变位移，因此数据库中的一个数值需要和对应条件一起读取。本篇乙醇条目 bmse000297 记录的样品为 D₂O 中 100 mM 乙醇，温度 298 K，pH 7.4，以 DSS 为参照，在约 400 MHz 条件下测量。

![真实公开记录 BMRB bmse000297，DOI 10.13018/BMSE000297；Madison Metabolomics Consortium。A、B 保留七条跃迁线的记录位置与高度，C 保留峰组积分，面积比约 1.4978。原条目条件为 D₂O 中 100 mM、298 K、pH 7.4、DSS 参照。峰表竖线不表示实测线宽；数据按 BMRB 公共领域政策使用。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9b50621df6c75fef0a4e602f.svg?v=9b50621df6c7)

图 2真实公开记录 BMRB bmse000297，DOI 10.13018/BMSE000297；Madison Metabolomics Consortium。A、B 保留七条跃迁线的记录位置与高度，C 保留峰组积分，面积比约 1.4978。原条目条件为 D₂O 中 100 mM、298 K、pH 7.4、DSS 参照。峰表竖线不表示实测线宽；数据按 BMRB 公共领域政策使用。

该条目的归属表把 CH₂ 氢放在约 3.645 ppm，把 CH₃ 氢放在约 1.175 ppm；其一维峰组记录使用约 3.641 ppm 和 1.170 ppm。归属表、峰组中心与每条分裂线是不同层次的记录，不必期待它们的末位完全相同。图中保留数据库给出的七条分裂线位置和高度，以竖线显示它们；同时展示两组实际记录的积分。竖线图没有提供连续峰形或线宽，所以后面的时间信号模型会明确另行设定这些量。

乙醇有六个氢，为什么例子的主要积分只对应五个？因为 OH 上的氢容易与溶剂交换，在 D₂O 中可以被氘替换，其 ¹H 响应也会受到交换条件影响。这里观察的是在该样品与实验条件下可见、可归属的氢，不是把分子式中的每个氢机械对应到一条谱线。蛋白质中的可交换氢也有类似问题，这使溶剂选择不仅影响谱图背景，还会改变你实际观察到哪些原子。

## 一组线不等于一组不同分子

同一组中的几个氢为什么有时只给一个化学位移？除了化学对称性，分子运动也会影响环境的时间平均。如果几个位置在测量所敏感的时间尺度上迅速互换，仪器可能观察到它们的平均响应；降低温度后交换变慢，谱形又可能分开或展宽。因此峰数不仅由静态结构图决定，还与分子运动和实验温度有关。做变温实验时，要同时注意溶解度、酸碱平衡、交换和仪器温度校准，才能把谱形变化联系到具体运动过程。

乙醇的 CH₃ 常表现为三重峰，CH₂ 常表现为四重峰。这些分裂主要来自通过化学键传递的核自旋耦合：邻近自旋的不同状态，使目标核的跃迁频率出现多个允许位置。对于简单的一阶情形，与 n 个等价自旋二分之一邻核耦合，会形成 n+1 条线。CH₃ 旁有两个 CH₂ 氢，因而出现三条；CH₂ 旁有三个 CH₃ 氢，因而出现四条。这里数的是满足相应等价条件的耦合邻核，而不是所有空间上靠近的原子。

三重峰常接近 1∶2∶1 的强度分布，四重峰接近 1∶3∶3∶1，因为不同邻核状态组合出现的数目不同。它像把几次两种结果的组合按总结果分类，中间类别的组合更多。这个组合直觉帮助解释线条强弱，却不是所有复杂谱形的通用算法。若化学位移间隔以赫兹表示时与耦合常数接近，自旋之间的强耦合效应可能改变线形与相对强度，简单的 n+1 图像就需要更完整的自旋体系分析。

耦合常数通常记作 J，单位为 Hz。对同一个分子与相同环境，它通常不会随磁场像化学位移的赫兹间隔那样成比例增长。因此一组约 7.1 Hz 的分裂，在 400 MHz 上约为 0.0178 ppm，在 600 MHz 上约为 0.0118 ppm。更高磁场会使以 ppm 画出的耦合间隔看起来更窄，同时把不同化学环境在赫兹上的差异拉开。比较不同仪器谱图时，先确定正在比较 ppm、Hz，还是峰的物理线宽。

积分应覆盖整组分裂线。CH₃ 的三条线合在一起对应三个氢，CH₂ 的四条线合在一起对应两个氢，所以合适定量条件下两组面积约为 3∶2。峰数与氢数由此分开：三条线并不意味着三个不同氢环境，四条线也不意味着该组有四个氢。公开乙醇条目记录的两组积分为 180.16 和 120.28，比例约为 1.498，接近 3/2；这个例子把化学结构、分裂机制和面积信息连接起来。

## 先听到随时间衰减的合奏，再分开其中的频率

记录时间的长短与相邻采样点的间隔控制不同问题。较长记录帮助区分靠近的频率，较短采样间隔则允许覆盖更宽的频率范围。若接收窗口放置不合适，窗口外的响应可能折回到错误位置，形成频率混叠；这像电影里的车轮看起来反向旋转，是有限采样带来的错觉。选择谱宽时应把目标峰、参照和必要的空白区域一起放进来，随后再扩大目标区域查看，而不是在采集时只围住一个看起来最重要的峰。

脉冲之后，接收线圈记录一段随时间振荡并衰减的信号，称为自由感应衰减，简称 FID。不同共振环境像不同音高的乐器同时发声，仪器最先记录的是它们叠加的“合奏”。傅里叶变换把这段时间信号分解到频率轴上，得到熟悉的谱峰。这里的声音只是帮助理解频率分解的类比，实际检测的是射频电信号。接收系统通常先与参考频率混频，因此数据中的振荡常表示相对于载频的偏移，而不是直接以几百兆赫逐点画在屏幕上。

$$
s(t)=\sum_j A_j\exp\!\left(-\frac{t}{T_{2,j}^{*}}\right)\exp\!\left[i(2\pi f_jt+\phi_j)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | 复数 FID，相对信号单位；实部与虚部为两个接收分量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 脉冲后的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 共振分量编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb2c27f1e1ca2cb88caf17da.svg) | 第 j 分量初始振幅，与 s 同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/819a2589289afcba11f6e5ce.svg) | 有效横向衰减时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea0efbb08d1d6502e2a12fed.svg) | 相对于接收载频的频率偏移，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d417405b726871d27d560b21.svg) | 初始相位，rad。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 虚数单位，i²=−1；把正交接收分量合写。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

各环境的旋转、衰减响应相加。A=1、f=10 Hz、相位 0、T₂*=0.20 s 时，t=0.10 s 完成一周期，复信号为约 0.6065。模型假设独立指数分量；复杂交换与强耦合需相应扩展。

式中的复数表示法把两个相差四分之一周期的接收分量写在一起，便于同时保留幅度与相位。理解实部像余弦、虚部像正弦，就能先使用这个工具，而不必把它当成一个额外的神秘物理量。每个分量的频率决定峰的位置，衰减快慢影响峰宽，相位影响变换后吸收型与色散型成分如何混合。把相位调好，是为了让积分针对合适的吸收型线形，而不是把峰左右两侧的正负畸变一起误算进去。

$$
\Delta\nu_{1/2}=\frac{1}{\pi T_2^{*}},\qquad \Delta\nu_{\mathrm{window}}=\frac{1}{\pi T_2^{*}}+L_B
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/411288fdedf35db5f14fc88d.svg) | 理想洛伦兹吸收线的半高全宽，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/72f68daae778569b46b086fb.svg) | 指数横向衰减时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d4f59fee1d2180f7d0e23a22.svg) | 指数加窗后的半高全宽，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5a55bb6d12cadf2847f816c2.svg) | 指数窗 exp(−πLBt) 对应的额外展宽，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

指数衰减的傅里叶变换给出洛伦兹线，两个指数衰减率相加。T₂*=0.20 s 对应 1.59155 Hz；再加入 3 Hz 展宽后为 4.59155 Hz。有限记录、相位和其他线形贡献会改变实际观测。

![单独构造的乙醇式一阶自旋教学模型：3∶2 总面积、7.1 Hz 耦合、T₂*=0.20 s。A 是 FID 实部；B 是相同数据的频谱；C 比较额外 3 Hz 指数展宽；D 比较两种实际记录时长而保持相同补零长度。该模型不是 BMRB 原始时域数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/13036fb4ad5e53eb3ab55dd0.svg?v=13036fb4ad5e)

图 3单独构造的乙醇式一阶自旋教学模型：3∶2 总面积、7.1 Hz 耦合、T₂*=0.20 s。A 是 FID 实部；B 是相同数据的频谱；C 比较额外 3 Hz 指数展宽；D 比较两种实际记录时长而保持相同补零长度。该模型不是 BMRB 原始时域数据。

横向衰减时间 T₂* 包含分子弛豫与磁场不均匀等效应。理想指数衰减产生洛伦兹线形，T₂*=0.20 s 时半高全宽约为 1.59 Hz；衰减越快，频率峰越宽。采集持续时间还决定原始频率网格：记录 2 s 时基本间隔约 0.5 Hz，记录 0.25 s 时约 4 Hz。向时间数据末尾补零会让变换后的曲线插值更密，却没有增加实际观察时间，也不会凭空提供新的频率分辨信息。

窗函数则主动改变时间数据的权重。给 FID 乘一个逐渐衰减的指数，会减弱后段噪声的影响，同时使有效衰减更快、谱线更宽。它是一项可解释的信噪比与分辨率交换。代码同时展示未经加窗和加入展宽的结果，并放大两条靠近的教学谱线，使这一交换直接可见。若一味追求光滑，两个原本能区分的组分可能合到一起；若过度强调后段信号，噪声和截断波纹也会被放大。

## 让两条邻近谱线分开

两个教学环境的化学位移固定相差 0.020 ppm，面积相同。改变质子工作频率、有效横向衰减时间及处理时的额外展宽，观察赫兹尺度上的峰宽与间隔。模型采用理想洛伦兹线，不加入耦合和噪声。

浅色曲线为两个组分，深色为总和。总面积保持一致；图中标出的半高全宽是每个单独组分的宽度，不能把混合峰包络的宽度直接代入单峰公式。

交互实验把两条等面积谱线的间隔与 T₂*、额外指数展宽放在同一张图里。改变磁场时，固定 ppm 间隔对应的赫兹间隔随之变化；改变 T₂* 时，峰宽按照相应关系变化。图上的谷深帮助观察两条线何时还能分开，但它不代替真实实验中的噪声、采样、相位与复杂耦合分析。这个小实验回答的是一个明确问题：为什么更高磁场、较长相干寿命和较温和的处理，会对区分邻近频率产生不同作用。

## 积分成为数量之前，要让核有时间恢复

峰高与面积需要特别分开。同样数量的信号若分散到更宽的频率范围，峰会变矮，但完整面积可以保持不变。两个等面积洛伦兹峰中，线宽加倍的那一个峰高约减半；如果直接比较高度，就会误判为数量减少。积分把整段频率响应加起来，因此更接近核数，但前提是范围覆盖充分、基线正确且信号没有重叠。数据库分别储存高度和积分，正是因为这两个量回答不同问题；本篇真实峰表图也保留了这种区别。

一次脉冲改变了磁化，下一次脉冲到来前，纵向磁化会逐渐恢复。这个恢复过程通常由 T₁ 描述，与控制横向相干衰减的 T₂ 或 T₂* 是不同概念。如果重复太快，一些环境尚未恢复就被再次激发，信号会受到压低；不同环境的 T₁ 不同，压低比例也不同。于是即使谱峰位置完全正确、形状也很好看，积分比例仍可能偏离实际核数。定量 NMR 的关键之一，就是让采集条件对所比较的信号给出可比响应。

$$
\frac{M_z(T_R)}{M_0}=1-\exp\!\left(-\frac{T_R}{T_1}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6e0da5546ff4ab95a469ed95.svg) | 完全饱和后经过 TR 的纵向磁化，与 M₀ 同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | 平衡纵向磁化，磁化单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2d2c1f807c495a8c8c5b65ee.svg) | 理想模型的恢复或重复时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d3e6eda1d26b8ec9a05d7509.svg) | 纵向恢复时间常数，s。 |

磁化与平衡值的差按指数减小。TR=T₁ 时恢复 63.212%；TR=5T₁ 时恢复 99.326%。实际序列的翻转角与采集、延迟共同决定重复激发响应。

在理想完全饱和后的单指数恢复模型中，等待一个 T₁ 只恢复约 63.2%，等待五个 T₁ 恢复约 99.3%。若两个信号的 T₁ 分别为 1 s 和 3 s，重复间隔只有 1 s，它们的恢复比例约为 0.632 和 0.283，面积比会受到很大影响。实际脉冲序列中的翻转角、采集时间和等待时间共同决定恢复状态，不能只盯着一个参数名字。对于需要较高准确度的比较，应测量相关 T₁ 或验证延长重复间隔后积分比是否已经稳定。

$$
c_x=c_r\,\frac{I_x/n_x}{I_r/n_r}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8fb2d8dc0b2a5dd5e304e5a9.svg) | 目标物与定量标准浓度，相同单位，本例 mmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c884cfbe6a36b0e2dde4337.svg) | 目标峰组与标准峰组的积分，同一积分尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa2459b6287126e02028e14.svg) | 每个目标或标准分子对所选峰组贡献的核数，无量纲。 |

先把面积除以每分子核数，得到与分子数量成比例的响应，再与已知标准比较。Ix=120、nx=3、Ir=80、nr=2、cr=5 mmol/L 时 cx=5 mmol/L。要求响应可比、恢复适当、峰无混淆且标准纯度已处理。

加入已知浓度的定量标准，可以把核数归一化后的积分比换成浓度比。例如目标峰积分 120、每分子贡献三个氢；标准峰积分 80、每分子贡献两个氢，两者除以核数后都为 40。若标准浓度为 5 mmol/L，则目标浓度也是 5 mmol/L。标准需要与样品相容、稳定、纯度明确，而且峰不要与目标重叠。用于确定零 ppm 的位移参照，与用于确定物质数量的定量标准承担不同任务，即使某种物质有时能够同时承担两者，也应把两种用途分清。

![理想完全饱和后恢复的教学模型。两个环境的 T₁ 分别为 1 s 和 3 s，真实核数比为 3/2；短重复间隔使恢复速度不同转化成积分比偏差。曲线采用相同激发与检测效率，展示定量采集为何要考虑恢复时间。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/506c4d636d4fac88d377b368.svg?v=506c4d636d4f)

图 4理想完全饱和后恢复的教学模型。两个环境的 T₁ 分别为 1 s 和 3 s，真实核数比为 3/2；短重复间隔使恢复速度不同转化成积分比偏差。曲线采用相同激发与检测效率，展示定量采集为何要考虑恢复时间。

积分范围和基线也会改变结果。范围过窄会漏掉峰尾，过宽又可能纳入邻峰或基线偏移；对一组谱图，保持一致的峰组定义与处理方式很重要。溶剂抑制可以帮助观察被强溶剂峰遮盖的区域，但也可能影响附近目标峰。普通去耦碳谱的峰强还会受到弛豫和核 Overhauser 效应等因素影响，因此不能直接沿用常规氢谱的计数习惯。定量目标应当在采集之前确定，再选择合适的脉冲、延迟和处理条件。

### 读取真实峰表，构造 FID 并检验处理与定量条件

程序从所附 NMR-STAR 原文读取峰位置、高度与积分，另行建立明确标记的时间信号和恢复模型，输出全部图与表。

```
"""Real BMRB peak records and separate NMR time-domain teaching models.
python main.py --output results --language en
Data: BMRB bmse000297, DOI 10.13018/BMSE000297, public-domain archive.
The generated FIDs are simulations; they are not the deposited raw experiment.
"""
from pathlib import Path
import argparse,json,re,shlex
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#263d49','axes.labelcolor':'#263d49','axes.edgecolor':'#9bacb1','svg.fonttype':'path'})
blue,teal,coral,gold,gray='#265f85','#078579','#d6604d','#bb9033','#84969b'
def save(f,n):
 for item in f.findobj(matplotlib.text.Text):
  value=item.get_text()
  for old,new in [('₂',r'$_2$'),('₃',r'$_3$'),('₁',r'$_1$'),('⁻¹',r'$^{-1}$')]:value=value.replace(old,new)
  item.set_text(value)
 f.savefig(out/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{a.language}.png',dpi=155,bbox_inches='tight');plt.close(f)
def title(ax,l,z,e):ax.set_title(l+'  '+tr(z,e),loc='left',weight='bold',pad=14)

text=(Path(__file__).parent/'data'/'bmse000297.str').read_text(encoding='utf8')
frame=text.split('save_spectral_peak_1H',1)[1].split('\nsave_',1)[0]
def table(category):
 for content in re.findall(r'loop_\s*(.*?)\s*stop_',frame,re.S):
  tokens=shlex.split(content);n=0
  while n<len(tokens) and tokens[n].startswith('_'):n+=1
  columns=tokens[:n]
  if columns and columns[0].startswith(category+'.'):
   assert (len(tokens)-n)%n==0
   return [dict(zip(columns,tokens[i:i+n])) for i in range(n,len(tokens),n)]
 raise ValueError(category)
pos={r['_Spectral_transition_char.Spectral_transition_ID']:float(r['_Spectral_transition_char.Chem_shift_val']) for r in table('_Spectral_transition_char')}
height={r['_Spectral_transition_general_char.Spectral_transition_ID']:float(r['_Spectral_transition_general_char.Intensity_val']) for r in table('_Spectral_transition_general_char')}
areas={r['_Peak_general_char.Peak_ID']:float(r['_Peak_general_char.Intensity_val']) for r in table('_Peak_general_char')}
lines=np.array([[pos[k],height[k]] for k in pos]);actual_ratio=areas['2']/areas['1']

fig,axs=plt.subplots(1,2,figsize=(11.6,5.2));ax=axs[0];ax.set_xlim(0,10);ax.set_ylim(0,7);ax.axis('off')
ax.add_patch(Rectangle((.2,.5),1.4,5.9,fc='#dce5e8',ec=gray));ax.add_patch(Rectangle((8.4,.5),1.4,5.9,fc='#dce5e8',ec=gray));ax.text(.9,3.4,'N',ha='center',fontsize=20);ax.text(9.1,3.4,'S',ha='center',fontsize=20)
for y in [1.6,3.4,5.2]:ax.annotate('',xy=(8.1,y),xytext=(1.9,y),arrowprops={'arrowstyle':'->','color':gray,'lw':1})
ax.add_patch(Rectangle((4.65,1.2),.7,4.8,fc='#e9f4f2',ec=teal,lw=2));ax.text(5,6.3,tr('样品管','Sample tube'),ha='center',fontsize=10)
for y in np.linspace(2.4,4.7,5):ax.add_patch(Ellipse((5,y),2,.35,fill=False,ec=blue,lw=1.8))
ax.plot([6,7,7],[3.5,3.5,.6],color=blue,lw=2);ax.text(6.3,.25,tr('射频脉冲 / 感应接收','RF pulse / induction receiver'),ha='center',fontsize=9)
title(ax,'A','核感应的实验关系','Nuclear-induction experiment')
ax=axs[1];B=np.linspace(0,12,100);ax.plot(B,42.577*B,color=teal,lw=3);ax.scatter([9.4],[42.577*9.4],color=coral,s=55,zorder=3);ax.annotate('9.4 T → 400.22 MHz',(9.4,42.577*9.4),xytext=(3,460),arrowprops={'arrowstyle':'->','color':gray},fontsize=10);ax.set(xlabel=tr('磁场 / T','Magnetic field / T'),ylabel=tr('质子共振频率 / MHz','Proton resonance frequency / MHz'),xlim=(0,12),ylim=(0,540));title(ax,'B','磁场决定主要频率尺度','Field sets the principal frequency scale')
fig.text(.5,.01,tr('1946 年凝聚态核磁研究连接磁场、射频与感应信号。原创功能示意，非历史设备复原。','The 1946 condensed-matter experiments connected field, radiofrequency and induction. Original functional schematic, not a historical reconstruction.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'induction')

fig,axs=plt.subplots(1,3,figsize=(12.2,4.5),gridspec_kw={'width_ratios':[1,1,.9]})
for ax,mask,lim,z,e in [(axs[0],lines[:,0]>2,(3.70,3.58),'CH$_2$：四条分裂线','CH$_2$: four split lines'),(axs[1],lines[:,0]<2,(1.23,1.10),'CH$_3$：三条分裂线','CH$_3$: three split lines')]:
 v=lines[mask];ax.vlines(v[:,0],0,v[:,1],color=blue if mask[0] else teal,lw=3);ax.scatter(v[:,0],v[:,1],s=22,color=blue if mask[0] else teal);ax.set(xlim=lim,ylim=(0,36),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('记录的峰高 / 原条目单位','Deposited peak height / entry units'));title(ax,'A' if ax is axs[0] else 'B',z,e)
axs[2].bar([0,1],[areas['1'],areas['2']],color=[blue,teal],width=.6);axs[2].set(xticks=[0,1],xticklabels=['CH$_2$','CH$_3$'],ylabel=tr('记录的峰组积分 / 原条目单位','Deposited group integral / entry units'),ylim=(0,220));axs[2].text(0,areas['1']+4,f"{areas['1']:.2f}",ha='center');axs[2].text(1,areas['2']+4,f"{areas['2']:.2f}",ha='center');title(axs[2],'C',f'面积比 {actual_ratio:.4f}',f'Area ratio {actual_ratio:.4f}')
fig.text(.5,.01,tr('真实峰表：BMRB bmse000297 · D$_2$O，100 mM，298 K，pH 7.4，DSS 参照。竖线不表示实测线宽。','Real peak records: BMRB bmse000297 · D$_2$O, 100 mM, 298 K, pH 7.4, DSS reference. Sticks do not specify measured linewidth.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'ethanol')

# Construct a first-order ethanol-like FID with known areas and relaxation.
mhz=400.;carrier=2.4;j=7.1;dt=1/4000;N=8192;t=np.arange(N)*dt
freq=np.r_[((1.170-carrier)*mhz)+j*np.array([-1,0,1]),((3.641-carrier)*mhz)+j*np.array([-1.5,-.5,.5,1.5])]
amplitude=np.r_[3*np.array([1,2,1])/4,2*np.array([1,3,3,1])/8];T2=.2
fid=np.sum(amplitude[:,None]*np.exp(2j*np.pi*freq[:,None]*t[None,:])*np.exp(-t[None,:]/T2),axis=0)
rng=np.random.default_rng(560);noisy=fid+.015*(rng.normal(size=N)+1j*rng.normal(size=N))
def fft(data,lb=0):
 v=data.copy()*np.exp(-np.pi*lb*t[:len(data)]);v[0]*=.5
 f=np.fft.fftshift(np.fft.fftfreq(32768,dt));s=2*dt*np.fft.fftshift(np.fft.fft(v,n=32768)).real
 return f/mhz+carrier,s
ppm,spectrum=fft(noisy);_,broadened=fft(noisy,3);_,ideal=fft(fid)
group=lambda low,high:np.trapezoid(ideal[(ppm>=low)&(ppm<=high)],x=ppm[(ppm>=low)&(ppm<=high)]*mhz)
simratio=group(.8,1.5)/group(3.3,4.0)
fig,axs=plt.subplots(2,2,figsize=(11.6,7.7))
mask=t<.06;axs[0,0].plot(t[mask]*1000,noisy.real[mask],color=blue,lw=.9);axs[0,0].set(xlabel=tr('脉冲后时间 / ms','Time after pulse / ms'),ylabel=tr('FID 实部 / 相对单位','Real FID / relative units'));title(axs[0,0],'A','先记录时间合奏','Record the time-domain ensemble')
axs[0,1].plot(ppm,spectrum,color=teal,lw=1);axs[0,1].set(xlim=(4.1,.7),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));title(axs[0,1],'B','傅里叶变换分开频率','Fourier transform separates frequencies')
axs[1,0].plot(ppm,spectrum,color=teal,label=tr('不加窗','Unweighted'));axs[1,0].plot(ppm,broadened,color=coral,label=tr('额外展宽 3 Hz','Additional 3 Hz broadening'));axs[1,0].set(xlim=(1.23,1.11),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));axs[1,0].legend(frameon=False,fontsize=9);title(axs[1,0],'C','光滑与分辨率一起改变','Smoothing changes resolution')
shortN=1000;_,short=fft(fid[:shortN]);axs[1,1].plot(ppm,ideal,color=teal,label=tr('2.048 s 记录','2.048 s acquisition'));axs[1,1].plot(ppm,short,color=gold,label=tr('0.250 s 记录，同样补零','0.250 s, same zero filling'));axs[1,1].set(xlim=(1.23,1.11),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));axs[1,1].legend(frameon=False,fontsize=9);title(axs[1,1],'D','补零没有延长观察时间','Zero filling does not extend observation')
fig.tight_layout();save(fig,'processing')

TR=np.linspace(.01,18,400);rec1=1-np.exp(-TR/1);rec3=1-np.exp(-TR/3);biased=1.5*rec1/rec3
fig,axs=plt.subplots(1,2,figsize=(11.6,4.7));axs[0].plot(TR,rec1,color=teal,label='T$_1$ = 1 s');axs[0].plot(TR,rec3,color=blue,label='T$_1$ = 3 s');axs[0].axhline(1-np.exp(-5),color=gray,ls=':',label='99.326%');axs[0].set(xlabel=tr('重复间隔 / s','Repetition interval / s'),ylabel=tr('恢复磁化 / 平衡磁化','Recovered / equilibrium magnetization'),ylim=(0,1.05));axs[0].legend(frameon=False,fontsize=9);title(axs[0],'A','不同环境恢复速度不同','Environments recover at different rates')
axs[1].plot(TR,biased,color=coral,lw=3);axs[1].axhline(1.5,color=gray,ls='--',label=tr('真实核数比 3/2','True nucleus-count ratio 3/2'));axs[1].set(xlabel=tr('重复间隔 / s','Repetition interval / s'),ylabel=tr('受恢复影响的积分比','Recovery-biased integral ratio'));axs[1].legend(frameon=False,fontsize=9);title(axs[1],'B','位置正确，面积仍可偏差','Correct positions can accompany biased areas')
fig.tight_layout();save(fig,'recovery')
np.savetxt(out/'deposited_transitions.csv',lines,delimiter=',',header='chemical_shift_ppm,deposited_height',comments='')
np.savetxt(out/'deposited_integrals.csv',np.array([[3.641,areas['1'],2],[1.170,areas['2'],3]]),delimiter=',',header='group_shift_ppm,deposited_integral,assigned_proton_count',comments='')
np.savetxt(out/'simulated_fid.csv',np.column_stack([t,noisy.real,noisy.imag]),delimiter=',',header='time_s,real,imaginary',comments='')
np.savetxt(out/'simulated_spectra.csv',np.column_stack([ppm,spectrum,broadened,short]),delimiter=',',header='chemical_shift_ppm,unweighted,broadened_3Hz,short_record',comments='')
summary={'proton_frequency_at_9_4T_MHz':42.577*9.4,'deposited_transition_count':len(lines),'deposited_area_ratio':actual_ratio,'simulated_area_ratio':float(simratio),'linewidth_T2star_02_Hz':1/(np.pi*.2),'recovery_at_5T1':float(1-np.exp(-5)),'biased_ratio_TR1':float(1.5*(1-np.exp(-1))/(1-np.exp(-1/3))),'example_concentration_mM':5*(120/3)/(80/2),'raw_frequency_spacing_Hz':1/(N*dt),'data_kind':{'peak_records':'real BMRB bmse000297 data','FID_and_recovery':'constructed teaching models'}}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

完整程序离线读取所附 BMRB NMR-STAR 文件，提取真实峰表与积分，并另外生成可控的 FID、窗函数比较和恢复偏差图。它保留原始数据库文件，也导出便于检查的表格。公开数据中的高度、积分和化学位移分别读取，不把高度当成面积；构造信号的线宽、噪声与采样长度则写在代码中。这样你可以沿着每一个数字回到它对应的数据层次，并通过改变一个条件检查其后果。

## 从乙醇走向聚合物和蛋白质

观察核种也可以跟着问题改变。含氟材料中的 ¹⁹F、磷酸基团中的 ³¹P，都可能提供比拥挤氢谱更直接的线索；相应溶剂、频率窗口、参照与定量条件也要重新确定。选择一个较少受其他组分干扰的核种，有时比在复杂氢谱中强行分开所有峰更有效。它仍然需要清楚的化学归属，而不是把一个新峰自动当成某种特定反应产物。

以侧基改性为例，若未反应官能团的特征峰逐渐减小，而一组稳定骨架峰始终保留，可以先分别除以各自每单元贡献的核数，再比较反应前后的归一化比例。这样做把溶液浓度变化与化学转化尽量分开。若反应同时改变了溶解性，或目标峰与产物峰重叠，这条计算路线就需要额外的分离或归属信息。真正有用的转化率应告诉读者选了哪组信号、按几个核归一化、哪些样品组分进入了测量，而不仅是一个百分数。

对聚合物，NMR 常用来比较单体组成、侧基转化、端基或局部排列。选择不重叠且归属清楚的信号后，可以把积分除以每个重复单元贡献的核数，再讨论组分比例。端基法估算链长时，端基信号通常远弱于重复单元信号，低含量杂质或基线误差就可能被放大；同时还要知道每条链的端基数与化学完整性。材料是否完全溶解也决定了溶液谱代表整个样品，还是其中较易溶解的一部分。

大分子在溶液中转动较慢，许多响应可能变宽并相互重叠。增加一条频率维度，可以把原本挤在同一横轴上的关系展开。COSY 等实验利用耦合建立氢之间的连接线索，HSQC 把直接相连的氢与某些异核响应联系起来，而 NOE 相关实验可以提供空间接近的信息。这些实验传递的是不同物理关系，不是任意两个峰在二维图上相交就说明两个原子相连。选择哪一种二维或多维实验，应从想知道的连接类型出发。

蛋白质结构研究进一步把许多归属、距离或取向约束与分子几何结合起来。最后展示的一组 NMR 结构反映数据与结构计算允许的构象范围，其离散程度还会受到约束数量和方法影响，不能直接把每个模型当成按时间顺序拍摄的分子运动。研究动力学通常要结合专门的弛豫、交换或其他时间敏感实验。结构与运动都能借助 NMR 研究，但它们需要不同的观测与模型。

固体中的分子运动与各向异性相互作用又不同，常需魔角旋转及相应脉冲方法来处理谱线展宽。能否溶解、是否要保留材料原来的固态组织、关注化学组成还是局部运动，都会影响选择溶液或固体 NMR。读完一张谱，最值得留下的是明确的归属关系与数量定义：哪些核产生信号，参照和条件是什么，积分代表多少个核，哪些连接由哪一种实验支持。这样的记录能把谱峰真正转化成分子结构与材料变化的证据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [BMRB: Ethanol bmse000297](https://bmrb.io/metabolomics/mol_summary/show_data.php?id=bmse000297)

   真实乙醇峰表、归属、积分与样品条件。

   Public-domain archive data; DOI 10.13018/BMSE000297; Madison Metabolomics Consortium.
2. [BMRB: About and distribution policy](https://bmrb.io/bmrb/)

   公共领域数据政策与数据库引用。

   Archive data public domain; BMRB states shared wwPDB usage policy.
3. [Oxford NMR: Classic NMR Papers](https://nmr.chem.ox.ac.uk/classic-nmr-papers)

   1946 核磁、化学位移与 1966 傅里叶变换的原文索引。

   Historical bibliography; original figures.
4. [UCSB NMR: Chemical Shift Referencing](https://nmr.chem.ucsb.edu/protocols/refppm.html)

   位移定义、参照与条件记录。
5. [Oxford NMR: Quantitative NMR Spectroscopy](https://nmr.chem.ox.ac.uk/sites/g/files/vzsiac2831/files/nmrchem/documents/media/quantitative_nmr.pdf)

   恢复时间、积分、相位与定量标准。
6. [Oxford NMR: Processing Techniques](https://nmr.chem.ox.ac.uk/sites/g/files/vzsiac2831/files/nmrchem/documents/media/processing-techniques.pdf)

   指数加窗的信噪比与展宽交换。

   Copyright author; technical reference, no source figures reproduced.
7. [Iowa State CIF: NMR Coupling Constants](https://www.cif.iastate.edu/nmr/nmr-tutorials/couplingconstants)

   不同键连接的耦合范围与 Hz 单位。
