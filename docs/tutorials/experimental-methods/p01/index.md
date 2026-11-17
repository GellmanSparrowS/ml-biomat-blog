# 动态光散射：从布朗运动测量粒径

Source: https://ml-biomat.com/tutorials/experimental-methods/p01/
Language: zh-CN

从随机运动和闪烁光强，读懂水动力尺寸、少量聚集体与不同平均方式。

## 看不见颗粒，也能知道它在水里有多大

一瓶刚配好的蛋白质溶液看起来清澈，放置一段时间后却可能已经出现少量聚集体；一份纳米载体加入缓冲液后，肉眼仍看不出变化，它在液体中的运动却可能慢了下来。动态光散射，简称 DLS，正是利用这种运动测量颗粒大小。仪器用激光照射分散液，记录散射光如何随时间起伏，再从起伏的时间尺度推算扩散系数，最后换算为水动力直径。这个过程没有逐个拍下颗粒的轮廓，而是让许多颗粒的随机运动共同提供尺寸信息。

水动力直径可以先理解为一个关于阻力的等效尺寸：假如有一颗理想球，它在同样液体、同样温度下扩散得与目标颗粒一样快，这颗球的直径就是目标的水动力直径。颗粒表面的聚合物链、吸附层、溶剂化以及形状都会影响运动阻力，因此 DLS 的尺寸不必等于显微镜中干燥核心的宽度。像穿着蓬松外套穿过人群，外套会改变行动时需要让开的空间，但等效尺寸并不是给真实表面画出一条固定硬边界；柔软层与周围液体可能相互穿透，影响的是整体运动响应。

这个定义决定了 DLS 擅长回答什么。它适合比较分散状态是否改变、蛋白质是否出现较慢扩散组分、表面修饰后颗粒的水动力行为是否变化，以及一份较窄分布样品在不同批次间是否一致。对于长棒、片层或柔软网络，一个直径只能概括特定运动性质，形貌还需要成像等方法补充。对于正在沉降、强烈对流或快速反应的体系，记录中的变化包含了布朗扩散以外的运动。先说清测量对象，才知道该把哪个数字作为结果，而不是让软件报告中的最大字号替我们选择研究问题。

本节沿着仪器的推理链逐步走：为什么小颗粒扩散得快，为什么运动会使散射光闪烁，相关曲线又如何变成直径。随后我们故意在小颗粒中加入极少量较大的颗粒，看看“数量上很少”为什么仍可能在光学信号中非常显眼。最后讨论样品处理、液体黏度和浓度检验，并用完整程序从构造的光子计数开始重建相关曲线。读完后，应能把一个粒径值连同它的信号、环境与平均方式一起解释。

## 从花粉附近的微粒，到可以计算的随机运动

十九世纪，植物学家 Robert Brown 观察到悬浮在液体中的微小颗粒持续进行不规则运动。运动并不需要颗粒具有生命：周围液体的分子在热运动中不断交换动量，微粒受到的作用在短时间内并不完全抵消。到了二十世纪初，Einstein 与 Smoluchowski 把这种杂乱运动写成可检验的统计关系，Perrin 则用胶体实验把分子尺度的理论与显微镜下的观察联系起来。在其 1926 年诺贝尔演讲中，Perrin 特别讨论了颗粒位移和乳液分布。这段历史有趣之处在于，研究者没有追求预测每一次转弯，而是找到许多随机路径共同遵循的规律。

一颗粒子向左走与向右走都可能发生，直接平均带符号的位移，结果往往接近零；这并不意味着颗粒没有移动。把位移平方后再平均，就能保留运动范围，并让正负方向都贡献正数。二维平面中有横向和纵向两个方向，各自的平均平方位移与经过时间成正比，两者相加得到图中的直线规律。这里的扩散系数单位是面积除以时间，不是速度；布朗路径没有一条始终朝同一方向前进的轨道，所以把扩散系数解释成“每秒走了多少米”会丢掉随机运动的含义。

$$
\left\langle [x(t)-x(0)]^2+[y(t)-y(0)]^2\right\rangle=4Dt
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3b231539d50d3e8aaff9e854.svg) | 二维位置坐标，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 平移扩散系数，m²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0e6630a6cb958dd089f42cf.svg) | 许多独立位移的平均；此处模拟2048条路径。 |

各向同性、无漂移的二维布朗扩散中，每个方向贡献2Dt。D=6.1343277 μm²/s、t=0.3 s，二维平均平方位移7.36119 μm²；其平方根2.71 μm是位移尺度，不是总路程。

![原创数值示意，联系 Brown 的观察以及 Einstein、Smoluchowski、Perrin 的统计研究。不是历史实测轨迹。25 °C、黏度0.890 mPa·s；每种尺寸2048条二维路径，时间步0.001 s。实线为样本平均，虚线为理论4Dt。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4826c4c793da13735a4e26de.svg?v=4826c4c793da)

图 1原创数值示意，联系 Brown 的观察以及 Einstein、Smoluchowski、Perrin 的统计研究。不是历史实测轨迹。25 °C、黏度0.890 mPa·s；每种尺寸2048条二维路径，时间步0.001 s。实线为样本平均，虚线为理论4Dt。

图左给出两个构造颗粒在相同 0.3 秒内的一条二维路径，图右则平均了每种尺寸的 2048 条独立路径。单条轨迹会偶然向某个方向走远，也可能多次折返；平均以后，80 nm 颗粒与 240 nm 颗粒的运动范围差异才稳定显现。虚线是理论平均，不是把某一条路径拉直。对于这里的水和温度，80 nm 颗粒的扩散系数约为 6.134 μm²/s，0.3 秒的二维平均平方位移约为 7.361 μm²。平方位移开方约为 2.71 μm，表示统计意义的位移尺度，并非颗粒实际曲折路径的总长度。

尺寸与扩散的联系由 Stokes–Einstein 关系给出。热运动的能量尺度与绝对温度有关，液体黏度和颗粒尺寸则决定运动阻力。相同温度与液体中，球的直径增大三倍，扩散系数降为三分之一；液体黏度增大一倍，扩散系数也减半。这个关系针对相应流体条件下的等效球阻力，稀释、接近平衡且主要进行布朗扩散的体系最容易解释。浓体系中的颗粒相互作用、黏弹性介质或复杂表面边界，会使“从扩散直接换算尺寸”需要额外物理模型。

$$
D=\frac{k_BT}{3\pi\eta d_H},\qquad d_H=\frac{k_BT}{3\pi\eta D}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 平移扩散系数，m²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2600a50cd45c9994bcd80b30.svg) | 玻尔兹曼常数，1.380649×10⁻²³ J/K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 分散介质动力黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3b6a97fbe00a64ed7f5753e9.svg) | 等效球水动力直径，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

热运动与球形Stokes阻力的关系；适用于相应连续流体与布朗扩散条件。T=298.15 K、η=0.000890 Pa·s、dH=80×10⁻⁹ m，D≈6.13433×10⁻¹² m²/s。同环境240 nm球的D为三分之一。

## 散射光为什么会闪烁：颗粒移动改变了波的叠加

历史图中的路径是为了说明统计原理，DLS 本身并不直接输出这些二维坐标。若要观察单个颗粒的运动，可以使用适合的显微追踪方法；若要快速评估许多纳米颗粒的整体扩散，散射相关测量更方便。两者都能联系到扩散，却有不同的检测权重、采样对象和空间分辨条件。因此把显微追踪得到的数量分布与 DLS 光强分布比较时，应先统一所讨论的物理量。认识这种区别，也能帮助我们为同一个样品选择真正互补的测量，而不是期待所有仪器给出相同的直方图。

激光提供具有稳定相位关系的入射光。许多颗粒把光散射到探测方向，这些光波到达探测器时会相互叠加：有些位置关系使波峰更容易重合，亮度增强；另一些关系使波峰与波谷部分抵消，亮度减弱。颗粒稍微移动，光程和相位就会改变，原先的明暗关系随之变化，探测器便记录到光强起伏。这个信号不像逐个颗粒穿过一束光时简单地亮一下、暗一下，而是许多散射波共同形成的干涉图样在不断改变。

想象隔着磨砂玻璃看许多反光点，单个点的位置难以分辨，整体亮暗图案却一直变化。变化得快，往往意味着散射结构忘记原来位置关系的速度快；变化得慢，则相关性保留得久。DLS 用自相关函数把这种“过了多久还像刚才”量化。它把一段光强记录与延迟后的同一记录配对相乘，再对许多时刻求平均。延迟很小时，较亮的时刻附近常仍较亮，乘积平均偏大；延迟足够长时，两个亮度近似独立，乘积平均趋近平均亮度的平方。

$$
g_2(\tau)=\frac{\langle I(t)I(t+\tau)\rangle}{\langle I\rangle^2}=1+\beta|g_1(\tau)|^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/60518fc66e22af7805986728.svg) | 归一化光强自相关，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b4a2d5741b5fa9e74f2c3b8.svg) | 探测光强或等时间窗光子数；分子与分母用同一单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/665d0053bb3deb2475f4a302.svg) | 记录时间与延迟时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0e6630a6cb958dd089f42cf.svg) | 在平稳记录上对许多起始时刻平均。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 由光学收集和模式平均决定的相干因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | 归一化电场相关，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | 复数幅值。 |

右侧为适用的高斯散射场统计下Siegert关系；本例两个独立模式给β=0.5。零延迟理想散射g1=1，g2=1.5；长延迟g1趋零，g2趋1。实际零延迟光子计数还含计数噪声，拟合时排除。

![构造80 nm球形颗粒散射，种子810，633 nm、90°、介质折射率1.333。两个独立复高斯模式与泊松计数，采样2 μs，共1048576点。显示前10 ms；用全记录计算相关，拟合延迟≤6 ms并排除零延迟。图D包括全部展示延迟。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/14690df7b74f4e6ccbd9b40d.svg?v=14690df7b74f)

图 2构造80 nm球形颗粒散射，种子810，633 nm、90°、介质折射率1.333。两个独立复高斯模式与泊松计数，采样2 μs，共1048576点。显示前10 ms；用全记录计算相关，拟合延迟≤6 ms并排除零延迟。图D包括全部展示延迟。

因此，本节归一化光强相关函数的长延迟基线约为一，而不是零。若软件画的是相关函数减一，基线才会在零；若画的是从光强相关换算出的电场相关，曲线定义又不同。图中显示的光子计数来自构造的两个独立光学模式，加入了光子到达的泊松波动，之后再由整段计数计算相关。上方只展示前十毫秒以便看清起伏，计算却使用完整约 2.10 秒记录。这个短记录是可重复的教学模型，不是给所有真实样品规定的采集时长。

相关函数中的相干因子描述光学收集与模式平均如何影响起始幅度。本例两个等强独立模式的理想幅度为 0.5，有限记录拟合得到约 0.489；它不是样品中一半颗粒发生了运动。光子计数在零延迟还有额外的计数噪声贡献，因此程序从非零延迟开始拟合。实际仪器还可能出现探测器余脉冲、背景散射和漂移，应结合相应记录检查短延迟与长延迟区域。把幅度、基线和衰减时间分开阅读，能避免将所有相关曲线差异都归结为粒径变化。

## 从衰减时间走到直径，中间有哪些换算

对于稀释、单一尺寸、近似球形且主要进行平移布朗扩散的颗粒，电场相关随延迟时间呈指数衰减。衰减率不仅取决于扩散系数，还取决于观察几何：激光波长、液体折射率和接收散射光的角度共同决定散射矢量的大小。可以把它理解为仪器用某种空间尺度观察位置变化；相同颗粒换一个角度，相关衰减时间会改变，但只要正确代入几何参数，推算出的扩散系数应保持相应一致性。直接比较两个仪器曲线的横向位置而忽略角度，会把光学条件误读成颗粒变化。

$$
g_1(\tau)=e^{-\Gamma\tau},\qquad\Gamma=Dq^2,\qquad q=\frac{4\pi n}{\lambda_0}\sin\frac{\theta}{2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | 单一扩散组分的电场相关，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 延迟时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | 电场相关衰减率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 平移扩散系数，m²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 散射矢量大小，m⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 液体在激光波长处的折射率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | 真空激光波长，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 入射与散射方向夹角；正弦计算使用弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率。 |

稀释单一尺寸、平移布朗扩散模型。633 nm、n=1.333、θ=90°给q≈1.8712×10⁷ m⁻¹。80 nm模型D≈6.13433×10⁻¹² m²/s，Γ≈2148 s⁻¹；光强超额相关按exp(−2Γτ)衰减，不能漏掉因子2。

本例使用真空波长 633 nm、液体折射率 1.333、散射角九十度和温度 25 °C，得到散射矢量大小约 1.8712×10⁷ m⁻¹。程序先对由光子记录计算的光强相关曲线拟合，再把衰减率除以散射矢量的平方得到扩散系数，最后用正确黏度换算直径。已知模型直径为 80 nm，本次有限记录得到约 80.90 nm。两者的差别让我们看到采样波动如何进入结果；增加记录并比较重复测量，才可以研究估计的稳定程度，而不是把拟合器给出的许多小数位当成实际精度。

为什么光强相关公式的指数里有一个二，而电场相关里没有？探测器直接记录的是光强，在适用的散射统计条件下，超出基线的光强相关与电场相关的平方相联系。电场指数平方以后，指数中的衰减率就乘了二。如果把光强相关当成电场相关直接代入，会把扩散系数与直径换算错一个因子。这个细节看起来只是公式前的小数字，却对应测量对象的根本区别。阅读导出的相关文件时，应先确定软件输出的到底是哪种函数，再决定使用什么模型。

拟合残差也值得看。残差是数据减去拟合曲线，连续朝同一方向偏离可能提示单指数没有描述完整结构，也可能来自背景或漂移。相关曲线上相邻延迟点由同一批光子配对形成，误差通常相关，因此普通最小二乘给出的形式误差不等同于独立样品间的不确定性。我们在这里把拟合用于重建已知构造模型，并保留残差图；真实研究中还应比较重复记录、不同装样和合理的拟合区间，让误差分析对应实际重复层级。

## 为什么千分之一的大颗粒，会占去很多散射光

如果每个人都用同样响亮的声音说话，听到的声音比例也许接近人数比例；若有人拿着扩音器，少数人也能很显眼。小颗粒的散射存在类似的不均衡。在颗粒远小于波长、形状和光学性质满足 Rayleigh 近似时，同种均匀球的单颗粒散射强度与直径的六次方成正比。直径增大三倍，单颗粒贡献便增加到 729 倍。这个高次方关系只在相应近似下使用；尺寸接近波长时，角度与光学结构会让散射更复杂，不能继续把六次方当成任意粒径的通用规则。

$$
w_i=\frac{N_i d_i^6}{\sum_jN_jd_j^6},\qquad g_1(\tau)=\sum_iw_i e^{-\Gamma_i\tau}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | 第i组对散射光强的比例，无量纲，各组和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2e48d6441cb55e92796c4f28.svg) | 第i或j组颗粒数量，或使用同一基准的数量比例。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c3bf1aa96ca6a8b183630c1e.svg) | 相应均匀球直径，使用相同长度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 组分求和编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | 混合物电场相关，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7cb77d3624bf5ffc46257fb9.svg) | 第i组衰减率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 延迟时间，s。 |

同光学对比均匀球的Rayleigh近似，单次散射且组分独立扩散。10与30 nm数量比例0.999、0.001，较大组的光强比例为0.001×729/(0.999+0.001×729)=0.421875。此六次方权重不延伸为大颗粒的通用散射模型。

构造混合物中，99.9% 的颗粒直径为 10 nm，只有 0.1% 为 30 nm，且两类球具有相同光学对比。较大颗粒虽然数量仅占千分之一，却贡献约 42.19% 的散射强度。按数量计算的平均直径只有 10.02 nm；按光强做算术平均得到 18.44 nm；由初始相关衰减得到的 z 平均直径则约为 13.91 nm。这三个值都来自同一个明确模型，差别来自平均方式。报告粒径时写清“数量均值”“分布峰位置”还是“z 平均”，比只写一个含义不明的平均粒径更容易比较。

![构造同光学对比均匀球，10与30 nm，数量比例99.9%与0.1%。采用Rayleigh六次方权重。PDI为衰减率的归一化方差；C用无噪声电场相关的对数做二阶局部展开，展示截断误差，不是仪器性能数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/37c031afb6a950685fae3080.svg?v=37c031afb6a9)

图 3构造同光学对比均匀球，10与30 nm，数量比例99.9%与0.1%。采用Rayleigh六次方权重。PDI为衰减率的归一化方差；C用无噪声电场相关的对数做二阶局部展开，展示截断误差，不是仪器性能数据。

z 平均来自衰减率的光强加权平均，再经扩散关系换算为尺寸。在相同环境的球形模型下，它对应直径的光强调和平均，而不是直径本身的光强算术平均。累积量分析还用相关函数偏离单指数的程度估计衰减率分布的相对方差，得到 DLS 的多分散性指数 PDI。这里的 PDI 与体积排阻色谱中摩尔质量分布的分散系数不是同一个定义，也不是“有多少颗粒不合格”的比例。它提供整体分布宽度的信息，却不会自动告诉我们有几个独立粒径群。

$$
\begin{aligned}\bar\Gamma&=\sum_iw_i\Gamma_i,\quad\mu_2=\sum_iw_i(\Gamma_i-\bar\Gamma)^2\\\mathrm{PDI}&=\frac{\mu_2}{\bar\Gamma^2},\quad d_z=\left(\sum_i\frac{w_i}{d_i}\right)^{-1}\\\ln g_1(\tau)&\simeq-\bar\Gamma\tau+\frac{\mu_2\tau^2}{2}\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a3181f4c55adf168086b94ad.svg) | 光强加权平均衰减率及各组衰减率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | 各组光强比例，无量纲，和为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a21f07d3948532bb6aa91995.svg) | 衰减率分布方差，s⁻²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/018a3249e5c08bf1bcdc9076.svg) | DLS多分散性指数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8ce6179638f66a34b72be421.svg) | z平均直径与各组水动力直径，统一长度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7af7845460cf4b819947dd4b.svg) | 电场相关（无量纲）与延迟时间（s）。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 组分编号。 |

各组使用相同介质、温度与几何；尺寸调和平均来自Γ与1/d成正比。10/30 nm例子得到dz=13.9130 nm、PDI≈0.20983；数量均值10.02 nm，光强算术均值18.4375 nm。末式为小延迟二阶累积量展开，较长延迟需考虑高阶项；并非把任意混合物恢复为两个真实峰。

图中的混合曲线很平滑，但与具有相同初始衰减率的单指数仍有差别。若用有限阶展开拟合不同延迟区间，得到的平均值也会变化，因为展开忽略了更高阶项。多指数分布反演试图恢复更多尺寸信息，然而相近的指数衰减可以互相补偿，小噪声就可能造成明显的峰形变化。软件画出两个尖峰时，应检查它们在重复记录和合理分析设置下是否稳定，并结合成像、分离或其他证据解释。把一个宽峰任意拆成许多峰，并不会凭空增加测量中的信息。

## 极少量大颗粒与一个输入框，会怎样改变粒径？

构造10与30 nm同光学对比均匀球，25 °C、633 nm、90°。先改变较大颗粒的数量比例，再分别改变真实黏度与用于换算的输入黏度。曲线使用真实黏度；报告直径使用输入黏度。

[Figure: 混合物相关曲线与黏度换算](https://ml-biomat.com/tutorials/experimental-methods/p01/#P01-plot)

交互实验将较大颗粒的数量比例与真实、输入黏度分开。先保持两种黏度一致，增加少量 30 nm 颗粒，观察相关尾部、z 平均和 PDI 怎样一起变化；再固定颗粒组成，只改软件输入的黏度，你会看到相关曲线保持原样，报告直径却发生变化。前一种变化来自散射对象，后一种来自换算条件。能够区分这两类原因，是把粒径趋势用于材料或生物研究时最重要的基本功之一。

## 样品与液体，也是测量模型的一部分

在生物介质中，还有一个很实际的问题：光并不知道哪一种成分是研究目标。血清蛋白、胶束、培养基中的颗粒以及加入的载体都可能贡献散射。分别测量介质空白很重要，但两条光强相关曲线通常不能像两份质量那样直接相减，因为混合信号的归一化和电场到光强的关系带有非线性，组分之间还可能发生吸附。若要追踪载体自身的变化，可以结合适当分离、标记成像或多种对照，确定观察到的慢组分是否与载体相关，而不是仅根据一个新增峰给它命名。

温度改变时，液体黏度常有明显变化。NIST 公开操作指南列出的纯水黏度，在 20、25 和 37 °C 时分别为 1.002、0.890 和 0.692 mPa·s。图中假想颗粒始终保持 80 nm，物理扩散根据各温度和正确黏度计算；如果换算时温度填对，却一直使用 25 °C 的黏度，20 °C 时会得到约 90.07 nm，37 °C 时得到约 62.20 nm。一个看似显著的热响应尺寸变化，就这样由错误输入产生。实际温度响应材料可能确实收缩或膨胀，先处理液体性质才能把真正结构变化分出来。

![A保留Hackley与Clogston的NIST SP1200-6第9页纯水黏度数值。B为据此计算的80 nm不变颗粒模型：温度正确，黏度误设为固定0.890 mPa·s。C为水动力等效的概念示意，不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8b6dedd881120be010d49bfb.svg?v=8b6dedd88112)

图 4A保留Hackley与Clogston的NIST SP1200-6第9页纯水黏度数值。B为据此计算的80 nm不变颗粒模型：温度正确，黏度误设为固定0.890 mPa·s。C为水动力等效的概念示意，不按比例。

折射率也有两个不同角色。液体折射率参与散射矢量计算，影响由衰减率得到的扩散系数；颗粒自身的折射率则主要在把光强分布换算成体积或数量分布时进入光学模型。后者的换算还需要形状、吸收与组成假设，因此点击“数量分布”并不等于仪器重新逐个数了颗粒。对于含蛋白质、糖或较高盐浓度的介质，不能总把所有液体参数默认成纯水。测量温度达到平衡后，还应确认溶液没有明显对流、蒸发或沉降，使记录对应相对稳定的分散状态。

灰尘和偶发大颗粒会显著影响散射，所以洁净比色皿、盖好样品、检查气泡并测量分散介质空白都很有价值。但过滤不是一个只会改善结果、不会改变样品的按钮。滤膜可能吸附蛋白质，截留本来就属于研究对象的聚集体，也可能改变柔软颗粒。若问题是原样中是否存在聚集，过滤前后应当作为不同样品状态比较；若目标是单分散组分，则说明分离处理后测量的对象。用过程回收率、浓度检查或成像核对处理效果，比仅凭过滤后曲线更漂亮判断成功更可靠。

浓度太低时目标散射弱，背景和少数杂质更容易占据主导；浓度太高时多重散射与颗粒间相互作用又会改变表观扩散。可以用组成匹配的介质做一组稀释，观察粒径、相关质量与计数率是否在合理区间保持一致。单纯加纯水可能同时改变盐浓度、酸碱度和吸附平衡，使颗粒本身发生变化。对蛋白质或可逆自组装体系，稀释还可能改变结合平衡；此时浓度依赖本身就是科学信息，应设计相应研究，而不是只挑一个最接近预期的尺寸作为答案。

## 保留相关曲线，让粒径结果可以被解释

合适的参考颗粒可以检查仪器与操作是否工作正常。选择时要看参考值对应的是哪种测量、什么分散介质和温度，按相应条件比较平均值与重复性；标称“百纳米”并不意味着任何介质、任何平均方式都必须得到恰好一百。参考样品的储存和聚集状态也需要关注。DLS 的尺寸换算有物理关系作为基础，参考物的作用是检验实际光学、温控、样品池和分析链条是否共同给出预期响应，而不是用一个任意校正系数把每份未知样品都调到满意的大小。

完整程序首先模拟二维布朗路径，验证平均平方位移；随后构造两个独立散射模式的复电场，转换为光强，再生成泊松光子计数。它从整段计数计算相关函数，排除零延迟计数尖峰后拟合单指数，输出直径、幅度、基线和残差。另一个确定性模型比较两种粒径的数量、体积与光强权重，并展示累积量截断区间的影响。最后读取随程序附带的公开水黏度表，计算错误输入造成的尺寸偏差。两类数据在图注和输出中分别说明：黏度是公开物性数值，颗粒轨迹和光子记录是构造模型。

### 从布朗轨迹和光子记录重建粒径

完整执行随机轨迹、复场与光子计数、相关计算、拟合、混合权重、拟合窗诊断及黏度偏差，输出全部图与数据。

```
"""DLS: Brownian motion, photon correlation, mixtures and solvent inputs.

All particle traces are constructed. Bundled water viscosities are published
NIST SP1200-6 values, retained with attribution in data/README.txt.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#20333e','axes.labelcolor':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(f,n):
 for e in ['svg','png']:f.savefig(O/f'{n}-{args.language}.{e}',dpi=145,bbox_inches='tight')
 plt.close(f)
def csv(n,heads,cols):np.savetxt(O/n,np.column_stack(cols),delimiter=',',header=','.join(heads),comments='',fmt='%.10g')
kB=1.380649e-23;TK=298.15;eta=.000890;nmed=1.333;wave=633e-9;theta=np.pi/2
q=4*np.pi*nmed/wave*np.sin(theta/2)
def diffusion(d_nm,visc=eta,T=TK):return kB*T/(3*np.pi*visc*d_nm*1e-9)
def diameter(D,visc=eta,T=TK):return kB*T/(3*np.pi*visc*D)*1e9
rng=np.random.default_rng(810);D80=diffusion(80);D240=diffusion(240)
dtpath=.001;tp=np.arange(301)*dtpath
paths={};msds={}
for d in [80,240]:
 step=rng.normal(size=(2048,300,2))*np.sqrt(2*diffusion(d)*dtpath)*1e6
 xy=np.concatenate([np.zeros((2048,1,2)),np.cumsum(step,axis=1)],axis=1);paths[d]=xy[:3];msds[d]=np.mean(np.sum(xy*xy,axis=2),axis=0)
csv('brownian_msd.csv',['time_s','msd80_um2','theory80_um2','msd240_um2','theory240_um2'],[tp,msds[80],4*D80*tp*1e12,msds[240],4*D240*tp*1e12])
fig,axs=plt.subplots(1,2,figsize=(12,5.2),layout='constrained')
a=axs[0]
for d,c in [(80,B),(240,R)]:
 xy=paths[d][0];a.plot(xy[:,0],xy[:,1],color=c,lw=1.3,label=f'{d} nm');a.scatter(*xy[-1],color=c,s=35)
a.scatter(0,0,color=K,marker='x',s=55);a.set(aspect='equal',xlabel=L('x 位移 / μm','x displacement / μm'),ylabel=L('y 位移 / μm','y displacement / μm'),title=L('A  相同 0.3 s，不同扩散尺度','A  Same 0.3 s, different diffusion scales'));a.legend(frameon=False)
a=axs[1]
for d,c in [(80,B),(240,R)]:a.plot(tp,msds[d],color=c,lw=2,label=L(f'{d} nm：2048 条轨迹',f'{d} nm: 2048 paths'));a.plot(tp,4*diffusion(d)*tp*1e12,color=c,ls='--',lw=1)
a.set(xlabel=L('经过时间 / s','Elapsed time / s'),ylabel=L('二维平均平方位移 / μm²','Two-dimensional mean squared displacement / μm²'),title=L('B  杂乱路径可以有清楚的统计规律','B  Irregular paths have a statistical law'));a.legend(frameon=False,fontsize=9)
fig.suptitle(L('从 Brown 的观察，到 Einstein、Smoluchowski 与 Perrin 的定量研究\n原创数值示意；不是历史测量轨迹','From Brown’s observations to Einstein, Smoluchowski and Perrin\nOriginal numerical illustration, not historical measured trajectories'),fontsize=11);save(fig,'brownian-history')

# Two independent complex Gaussian optical modes give coherence factor 1/2.
# Poisson counts model photon detection; the zero-lag shot-noise spike is excluded.
N=1048576;dt=2e-6;burn=8192;Gamma=D80*q*q;a=np.exp(-Gamma*dt);intensity=np.zeros(N)
for _ in range(2):
 noise=(rng.normal(size=N+burn)+1j*rng.normal(size=N+burn))*np.sqrt((1-a*a)/2)
 field=lfilter([1],[1,-a],noise)[burn:];intensity+=np.abs(field)**2/2
counts=rng.poisson(.8*intensity).astype(np.int16);center=counts-counts.mean();pad=1<<(2*N-1).bit_length()
fft=np.fft.rfft(center,pad);cov=np.fft.irfft(fft*np.conj(fft),pad)[:6001]/(N-np.arange(6001))
lags=np.unique(np.geomspace(1,6000,250).astype(int));tau=lags*dt;g2=1+cov[lags]/counts.mean()**2
def mono(t,beta,rate,base):return base+beta*np.exp(-2*rate*t)
mask=tau<=.006;fit,_=curve_fit(mono,tau[mask],g2[mask],p0=[.5,Gamma,1],bounds=([.05,1,.9],[1.5,1e6,1.1]),maxfev=20000)
beta_fit,rate_fit,base_fit=fit;dfit=diameter(rate_fit/q**2);fitted=mono(tau,*fit)
np.savez_compressed(O/'photon_counts.npz',counts=counts,bin_seconds=dt,diameter_nm=80,seed=810)
csv('correlation.csv',['delay_s','g2_from_counts','single_exponential_fit','fit_residual'],[tau,g2,fitted,g2-fitted])
block=25;preview=counts[:5000].reshape(-1,block).sum(axis=1);tprev=(np.arange(preview.size)+.5)*block*dt
csv('photon_preview.csv',['time_s','counts_per50us'],[tprev,preview])
fig,axs=plt.subplots(2,2,figsize=(12,8.6),layout='constrained')
ax=axs[0,0];ax.axis('off');ax.set(xlim=(0,10),ylim=(0,7));ax.set_title(L('A  接收一个方向的散射波动','A  Collect fluctuations in one direction'))
ax.add_patch(Rectangle((.3,2.4),1.8,1.2,fc=R,alpha=.8));ax.text(1.2,3,L('激光','Laser'),ha='center',va='center',color='white');ax.add_patch(Rectangle((4,1.7),2,2.7,fc='#d9e9e8',ec=B));ax.text(5,1.1,L('样品池','Cuvette'),ha='center');ax.annotate('',xy=(4.8,3),xytext=(2.1,3),arrowprops={'arrowstyle':'->','lw':2,'color':R});ax.plot([5,8.8],[3,3],ls='--',color='#8d9ba3');ax.annotate('',xy=(5,5.6),xytext=(5,3),arrowprops={'arrowstyle':'->','lw':2,'color':B});ax.add_patch(Rectangle((4,5.7),2,1,fc=B));ax.text(5,6.2,L('探测器','Detector'),ha='center',va='center',color='white');ax.text(5.4,3.5,'90°',color=B);ax.text(7.3,2,L('干涉随位置改变\n记录光子数随时间变化','Positions change interference\nRecord photons versus time'),ha='center',fontsize=9)
ax=axs[0,1];ax.plot(tprev*1e3,preview,color=B,lw=1);ax.set(xlabel=L('记录时间 / ms','Acquisition time / ms'),ylabel=L('每 50 μs 的光子数','Photons per 50 μs'),title=L('B  同一构造记录的前 10 ms','B  First 10 ms of the constructed record'))
ax=axs[1,0];ax.semilogx(tau*1e6,g2,'o',ms=3,color='#9bb9c0',label=L('由光子记录计算','Computed from photon record'));ax.semilogx(tau*1e6,fitted,color=R,lw=2,label=L(f'拟合直径 {dfit:.2f} nm',f'Fitted diameter {dfit:.2f} nm'));ax.set(xlabel=L('延迟时间 τ / μs','Delay time τ / μs'),ylabel='g₂(τ)',title=L('C  相关曲线衰减到约 1','C  Correlation decays toward about 1'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,1];ax.semilogx(tau*1e6,g2-fitted,color=B);ax.axhline(0,color=K,lw=.8);ax.set(xlabel=L('延迟时间 τ / μs','Delay time τ / μs'),ylabel=L('数据 − 拟合','Data − fit'),title=L('D  残差保留有限采样的起伏','D  Residuals retain finite-record fluctuations'));save(fig,'photon-correlation')

# Ideal Rayleigh mixture: homogeneous spheres of the same optical contrast.
ds=np.array([10.,30.]);num=np.array([.999,.001]);w=num*ds**6;w/=w.sum();rates=np.array([diffusion(d)*q*q for d in ds]);meanrate=np.dot(w,rates);variance=np.dot(w,(rates-meanrate)**2);PDI=variance/meanrate**2;z=diameter(meanrate/q**2)
tmix=np.geomspace(1e-7,.003,450);g1=np.exp(-tmix[:,None]*rates)@w;gmix=1+.5*g1*g1
cuts=np.array([.15,.3,.6,1.,1.5]);winz=[];winp=[]
for cut in cuts:
 m=tmix*meanrate<=cut;coef=np.polyfit(tmix[m]*meanrate,np.log(g1[m]),2);gr=-coef[1]*meanrate;mu2=2*coef[0]*meanrate**2;winz.append(diameter(gr/q**2));winp.append(mu2/gr**2)
csv('mixture.csv',['delay_s','field_correlation','intensity_correlation','matched_first_cumulant_g2'],[tmix,g1,gmix,1+.5*np.exp(-2*meanrate*tmix)])
csv('cumulant_window.csv',['maximum_scaled_delay','fitted_z_nm','fitted_PDI'],[cuts,winz,winp])
fig,axs=plt.subplots(2,2,figsize=(12,8.2),layout='constrained')
ax=axs[0,0];weightings=[num,num*ds**3/(num*ds**3).sum(),w];lab=L(['数量','体积','光强'],['Number','Volume','Intensity'])
for i,ww in enumerate(weightings):ax.barh(i,100*ww[0],color=B);ax.barh(i,100*ww[1],left=100*ww[0],color=R);ax.text(101,i,f'{100*ww[1]:.2f}%',va='center',fontsize=9)
ax.set(yticks=range(3),yticklabels=lab,xlim=(0,122),ylim=(-.5,3.1),xlabel=L('各类比例 / %','Fraction on each basis / %'),title=L('A  30 nm 颗粒只占数量的 0.1%','A  30 nm particles are only 0.1% by number'));ax.text(1,2.73,L('蓝：10 nm；红：30 nm','Blue: 10 nm; red: 30 nm'),fontsize=9)
ax=axs[0,1];ax.semilogx(tmix*1e6,gmix,color=B,lw=2,label=L('双粒径混合物','Two-size mixture'));ax.semilogx(tmix*1e6,1+.5*np.exp(-2*meanrate*tmix),color=R,ls='--',label=L('同一初始衰减率的单指数','Single exponential, same initial rate'));ax.set(xlabel=L('延迟时间 / μs','Delay time / μs'),ylabel='g₂(τ)',title=L('B  一条平滑曲线里可以藏着混合物','B  A smooth curve can conceal a mixture'));ax.legend(frameon=False,fontsize=8)
ax=axs[1,0];ax.plot(cuts,winz,'o-',color=B);ax.axhline(z,color=R,ls='--',label=L('精确初始矩','Exact initial moment'));ax.set(xlabel=L('拟合窗上限 Γ̄τ','Fit-window upper limit Γ̄τ'),ylabel=L('二阶展开给出的直径 / nm','Diameter from second-order expansion / nm'),title=L('C  截断展开依赖拟合区间','C  Truncated expansion depends on its window'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,1];means=[np.dot(num,ds),z,np.dot(w,ds)];ax.bar(L(['数量均值','z 均值','光强算术均值'],['Number mean','z-average','Intensity arithmetic']),means,color=[G,B,R]);ax.set(ylabel=L('直径 / nm','Diameter / nm'),ylim=(0,24),title=L('D  三个“平均”回答不同问题','D  Three averages answer different questions'))
for j,v in enumerate(means):ax.text(j,v+.5,f'{v:.3f}',ha='center')
save(fig,'mixture-weighting')

tab=np.genfromtxt(Path(__file__).parent/'data/water_viscosity.csv',delimiter=',',names=True);temps=tab['temperature_C'];viscosities=tab['viscosity_mPa_s'];dapp=80*viscosities/.890
csv('viscosity_bias.csv',['temperature_C','published_viscosity_mPa_s','true_diameter_nm','inferred_with_fixed0890_nm'],[temps,viscosities,np.full(3,80),dapp])
fig,axs=plt.subplots(1,3,figsize=(14,4.8),gridspec_kw={'width_ratios':[1,1.1,1]},layout='constrained')
ax=axs[0];ax.plot(temps,viscosities,'o-',color=B);ax.set(xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('水的黏度 / mPa·s','Water viscosity / mPa·s'),title=L('A  公开的水黏度数值','A  Published water viscosities'));ax.text(20.2,.72,'NIST SP1200-6, p.9',fontsize=9)
ax=axs[1];ax.plot(temps,dapp,'o-',color=R,label=L('误用固定 0.890 mPa·s','Fixed0.890 mPa·s input'));ax.axhline(80,color=B,ls='--',label=L('正确黏度：80 nm','Correct viscosity:80 nm'));ax.set(xlabel=L('真实温度 / °C','Actual temperature / °C'),ylabel=L('推算直径 / nm','Inferred diameter / nm'),ylim=(55,100),title=L('B  颗粒没变，错误输入制造变化','B  Wrong inputs create a size change'));ax.legend(frameon=False,fontsize=8)
ax=axs[2];ax.set(xlim=(-1.6,1.6),ylim=(-1.7,1.7),aspect='equal');ax.axis('off');ax.add_patch(Circle((0,.25),1.05,fc='#d9e9e8',ec=B,ls='--',lw=2));ax.add_patch(Circle((0,.25),.65,fc=Y,ec=K));ax.text(0,.25,L('核心','Core'),ha='center',va='center');ax.text(0,-1.18,L('溶剂化与表面层影响阻力\n水动力等效边界不是硬壳','Solvation and surface layers affect drag\nHydrodynamic equivalence is not a rigid shell'),ha='center',fontsize=9);ax.set_title(L('C  扩散测的是带环境的颗粒','C  Diffusion includes the environment'));save(fig,'viscosity-measurand')
summary={'data_kind':'constructed particle traces; published water-viscosity values','seed':810,'temperature_K':TK,'viscosity_Pa_s':eta,'q_per_m':float(q),'diffusion80_m2_per_s':float(D80),'diffusion240_m2_per_s':float(D240),'diffusion_size_ratio':float(D80/D240),'two_dimensional_msd80_at03s_um2':float(4*D80*.3*1e12),'photon_record_seconds':N*dt,'photon_mean_count_per_bin':float(counts.mean()),'fitted_diameter_nm':float(dfit),'fitted_coherence':float(beta_fit),'fitted_baseline':float(base_fit),'mixture_large_number_percent':.1,'mixture_large_intensity_percent':float(w[1]*100),'mixture_number_mean_nm':float(np.dot(num,ds)),'mixture_z_average_nm':float(z),'mixture_intensity_arithmetic_nm':float(np.dot(w,ds)),'mixture_PDI':float(PDI),'wrong_viscosity_diameter_at20C_nm':float(dapp[0]),'wrong_viscosity_diameter_at37C_nm':float(dapp[-1]),'published_water_viscosity25_mPa_s':float(viscosities[1])}
assert abs(D80/D240-3)<1e-12
assert abs(w[1]-.421875)<1e-12
assert abs(z-320/23)<1e-10
assert abs(summary['mixture_number_mean_nm']-10.02)<1e-12
assert 74<dfit<86 and .9<base_fit<1.1
assert abs(dapp[-1]-80*.692/.890)<1e-12
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))
```

程序保留完整光子计数压缩文件、相关数据表、混合物结果和逐点输出，便于从任何一个图返回原来的计算。与真实实验衔接时，首先确认导出文件的函数定义和时间单位，保留原始记录，再替换相应读入部分；不要把减过一的相关函数再次按未减基线的形式拟合。对重复数据，应区分同一池连续测量、重新装样以及独立制备批次。前者主要检验短时重复性，后两者逐渐加入操作与制备变异，回答的研究问题不同。

一份清楚的结果应把分散介质、浓度、温度、黏度、散射角与波长连同 z 平均、PDI、重复次数和变异一起交代，并提供相应相关曲线。当蛋白质样品出现缓慢衰减尾部时，可进一步比较新鲜与储存样品、适当分离后的组分及独立形貌信息；当表面修饰后粒径变化时，可检查聚集与溶剂化层变化分别有什么证据。DLS 提供的是运动中的颗粒信息。把它放回样品所处的液体环境，并与其他测量各自的定义对应起来，才能让一个纳米数值成为可以推动研究的结论。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Perrin: Nobel Lecture, Discontinuous Structure of Matter (1926)](https://www.nobelprize.org/prizes/physics/1926/perrin/lecture/)

   布朗运动、位移统计与胶体实验的历史。
2. [Hackley & Clogston: NIST SP1200-6, Batch-Mode DLS (2015)](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1200-6.pdf)

   样品、浓度、介质参数、报告要求及第9页水黏度。

   Published numerical water-property facts retained with attribution; no source artwork reproduced.
3. [Malvern: Dynamic Light Scattering, An Introduction](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104dynamiclightscatteringintroduction)

   干涉、相关、光学几何与水动力等效。
4. [Mailer, Clegg & Pusey: Particle Sizing by DLS, Non-linear Cumulant Analysis](https://arxiv.org/pdf/1504.06502)

   衰减率矩、截断区间与反演问题。
5. [Malvern: Dynamic Light Scattering, Common Terms Defined](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp111214dlstermsdefined)

   调和z平均与PDI定义。
6. [Malvern: Cumulants and Distribution Algorithms](https://www.malvernpanalytical.com/en/learn/knowledge-center/faqs/faq160705cumulantsnnls)

   分布峰与累积量结果的区别。
