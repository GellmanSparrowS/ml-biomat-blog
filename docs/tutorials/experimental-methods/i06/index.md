# X射线衍射：从峰的位置到晶体结构

Source: https://ml-biomat.com/tutorials/experimental-methods/i06/
Language: zh-CN

把峰位、峰宽和峰面积分别连到原子周期、有序尺度与散射分配。

## 同样含有钙和磷，为什么还要看衍射

一种骨修复材料在溶液中形成了新的表面沉积，元素分析检测到钙和磷。接下来很自然的问题是：这些元素究竟怎样排列，形成了哪一种晶体，还是只形成了缺少长程有序的沉积？元素组成像一份食材清单，同样的食材可以有不同的组织方式，材料性能也可能随之改变。X射线衍射简称XRD，它利用原子排列对X射线的散射与干涉，把空间周期转化成特定角度上的强度变化。峰的位置、强度和宽度因此能够提供彼此不同的结构信息。

聚合物也经常需要这种观察。加热、冷却、拉伸或加入填料以后，有序区域的数量、排列方向和尺度可能改变，进而影响透明度、刚度和阻隔性能。XRD可以把这些变化变成可比较的图样，但图里一座更高的峰并不直接等于“结晶更多”，一座更宽的峰也不直接等于“颗粒更小”。先分清每一种曲线特征由什么产生，再选择适合的计算，才能让衍射图成为结构解释的一部分。

本篇从两列波为什么会互相增强讲起，逐步进入布拉格关系、粉末图样、峰宽和面积分解。你不需要先掌握晶体学，只需要愿意把“原子如何重复排列”与“探测器在什么方向收到较强信号”联系起来。后面的代码使用一组明确构造的教学峰，让峰位移动、尺寸展宽、仪器展宽和背景选择分别发生，观察它们怎样改变同一张图。这样能在分析真实数据之前，先建立每一步计算对应什么物理问题的直觉。

## 让波峰一起到达，原子排列就会留下方向信息

把两颗石子落在水面上，波纹相遇时有些位置起伏更大，有些位置却较平静。波的叠加取决于它们到达时的相位，也就是波形在一个周期中走到了哪里。X射线照到样品后，电子对入射辐射发生散射；许多原子发出的散射波在探测器处叠加。若原子之间有规律地重复排列，某些方向上的路程差恰好让波峰与波峰相遇，信号就得到增强。衍射图记录的正是这种方向选择性，而不是一张直接放大的原子照片。

1912年的晶体X射线衍射发现，把X射线的波动性质与晶体内部周期联系起来。随后布拉格父子的研究用一组平行晶面之间的路程差解释强散射方向，并通过角度测量研究晶体结构。这一历史转变很值得理解：人们不必直接看到每一个原子，也能利用波如何叠加来推断间距。图中的平行晶面是帮助计算的几何构造，散射实际来自材料中的电子；把它们想成一层层普通镜子可以帮助画图，却不能替代原子散射的物理机制。

![原创布拉格几何与早期测角思想示意。相邻平行面提供额外路程，整数波长条件形成增强；晶面是几何构造，图不按比例。历史联系为1912—1913年晶体衍射与结构测量的发展。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b7831d29765fee83e6492c52.svg?v=b7831d29765f)

图 1原创布拉格几何与早期测角思想示意。相邻平行面提供额外路程，整数波长条件形成增强；晶面是几何构造，图不按比例。历史联系为1912—1913年晶体衍射与结构测量的发展。

考虑来自相邻两层的散射波。较深一层的波在进入和离开时都多走一段路，两段合起来为两倍晶面间距乘以入射掠角的正弦。如果额外路程等于一个、两个或更多整波长，两列波就重新对齐，形成增强。这就是布拉格关系。这里的角度θ是射线与晶面的夹角，而常见粉末衍射图横坐标写的是入射束与衍射束之间的角度2θ。把这两个角度混淆，是计算晶面间距时最常见、也最容易通过画图发现的错误之一。

$$
2d\sin\theta=n\lambda
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 相邻平行晶面间距，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 射线与晶面的夹角；图样横轴通常为2θ，计算时角度转换为弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 衍射级次，正整数；本例取1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X射线波长，nm；本例0.15406 nm。 |

相邻两层散射波额外路程为2d sinθ，等于整波长时相互增强。d=0.25 nm、n=1时，θ=arcsin(0.15406/0.5)≈17.946°，图中峰位2θ≈35.892°。

波长已知时，测到峰角度就可以计算相应的晶面间距。以0.15406 nm的X射线为例，0.25 nm间距的一阶增强出现在2θ约35.89°的位置。如果晶格均匀膨胀，间距增大，为保持路程差与波长匹配，θ就会减小，峰向低角移动。这一趋势在交互实验里可以直接看到。真实峰位变化还可能来自样品高度误差、仪器零点或温度等条件，所以判断晶格变化时，需要把几何标定与样品状态同时放在实验设计中。

## 为什么一堆随机小晶粒能形成一条可读的曲线

一块单晶的原子排列有相对统一的方向，旋转它时，不同晶面依次满足衍射条件。粉末样品则由许多晶粒组成，理想情况下它们取向足够分散，总有一部分晶粒以合适角度参与某个反射。满足同一晶面间距的散射在空间中形成一组方向，二维探测器可以记录成环，传统扫描探测器则沿角度逐步记录强度，最后形成强度—2θ曲线。粉末方法把方向丰富的晶粒集合变成容易比较的结构特征图，因此广泛用于材料鉴定。

晶体学中的晶面通常用三个整数标记，称为米勒指数，写作h、k、l。初学时可以先把它们理解为晶体中不同方向和间距的一组平行面标签。不同标签对应不同几何关系，但是否产生明显反射、强度有多大，还取决于晶胞内部原子的位置和散射能力。有些原子的散射波会在某个方向互相抵消，形成系统消光。因而仅知道晶胞边长还不足以预测所有峰高，结构中的原子种类与排列也参与决定图样。

理想随机粉末只是一个目标状态。片状颗粒容易平躺，针状颗粒容易沿某个方向排列，拉伸聚合物的晶区也可能形成择优取向。此时某些峰明显增强，另一些峰减弱，即使晶体总量没有同比例改变。薄膜、纤维和块体需要根据几何选择透射、反射或掠入射等配置。二维图样的环若变成弧或出现强度不均匀，往往直接提示方向分布。把取向信息保留下来，比为了得到一条简单曲线而忽略它更有研究价值。

制样还影响峰位与背景。反射几何下，样品表面高度与预定聚焦位置不一致，可能引起角度偏移；压实程度、颗粒大小和吸收会改变有效散射体积；样品托、溶剂和空气也可能贡献背景。对于含水生物材料，干燥或研磨本身可能改变结构，测量方式应保留研究所关注的状态。空样品托、已知标准物质和重复装样分别帮助检查不同环节。把它们放进测量流程，才能判断两条图样的差别发生在材料内部还是采集几何上。

测量设置需要兼顾角度范围、步长和计数时间。范围太窄可能漏掉区分晶相的关键反射；步长过大可能无法充分描述窄峰形状；计数时间短则使弱峰更难与随机波动分开。提高每一步计数可以降低相对随机噪声，却不会自动修正样品位移或仪器分辨率。先根据预期结构选择范围，再用标准样品和初步扫描检查峰宽与背景，是把测量资源用在关键问题上的一种直接方式。

## 峰位置给出间距，整套峰才逐渐约束结构

面对一条新图样，可以先找到稳定可重复的峰，记录位置和宽度，再计算一组晶面间距。接着结合样品可能包含的元素、处理过程和已知晶体结构，寻找能解释多条反射的候选相。开放晶体结构数据库中的结构文件能够支持计算参考图样，公开衍射分析软件则能把结构模型与实验曲线联系起来。参考图样应注明波长和计算条件，因为同一间距在不同波长下出现在不同2θ位置，直接把两个不同波长的角度表比较会产生混乱。

一个峰与某候选相接近，只是开始。不同晶体可能共享相似间距，多相混合又会让峰互相重叠。更有说服力的判断来自多条峰的位置关系、应当出现却缺失的反射、相对强度趋势以及元素信息。对于骨样矿物沉积，可以把XRD的有序结构信息与元素分析、红外中的化学基团信息联系起来；对于聚合物填料，可以把基体宽散射与无机相反射分开考虑。每种测量提供不同约束，组合起来才能逐渐收窄结构解释。

$$
q=\frac{4\pi\sin\theta}{\lambda},\qquad q_{n=1}=\frac{2\pi}{d}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 散射矢量大小，nm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 散射角2θ的一半。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X射线波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 一阶布拉格反射对应的晶面间距，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 布拉格反射级次，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

把一阶布拉格关系代入q定义，得到q=2π/d。d=0.25 nm对应q≈25.133 nm⁻¹。不同波长的同一结构周期可以用q坐标比较。

散射矢量大小q提供另一种横坐标，它把波长与角度合并成一个与空间尺度直接关联的量。对于一阶布拉格反射，q等于2π除以间距，因此间距越大，q越小。使用q坐标便于比较不同波长的测量，也为后面的小角散射建立联系。q不是颗粒直径的直接倒数：只有在明确知道某个峰来自怎样的周期或模型时，才能把它换成相应长度。这里先把它理解为描述散射空间频率的一把尺子。

峰位精确到许多小数并不保证间距同样准确。角度零点、样品位移、波长分布、峰重叠和背景都会影响峰中心的估计。多条峰共同变化时，可以比较偏移是否符合统一的晶格变化，还是更像某一种仪器几何误差。对温度或湿度响应材料，最好保持测量几何一致，记录达到目标状态的时间，并用相应参照检查仪器稳定性。这样获得的峰位变化才有明确的物理解释，而不是只在两条曲线上画一支箭头。

## 峰为什么变宽：有限周期、应变和仪器一起参与

如果一列原子无限长、排列完美，满足条件的散射方向可以非常集中。真实有序区域只有有限个重复周期，允许显著增强的角度范围就会变宽。代码中的第一幅干涉曲线只改变共同参与叠加的周期数：十个周期的峰较宽，八十个周期的峰较窄。可以把它想成合唱中能够保持同一节拍的人数与持续范围：有序配合延续得越长，对相位偏离的选择就越严格。这个比喻帮助理解有限尺寸如何影响峰宽，实际计算仍来自散射波的叠加。

![教学计算。A改变相干叠加的重复周期数，显示有限有序长度与峰宽的关系；B为纯尺寸高斯峰加已知仪器展宽，比较未修正和修正后的尺寸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cbf1d946e2cf75aa50c0b7a9.svg?v=cbf1d946e2cf)

图 2教学计算。A改变相干叠加的重复周期数，显示有限有序长度与峰宽的关系；B为纯尺寸高斯峰加已知仪器展宽，比较未修正和修正后的尺寸。

谢乐关系把一项经过适当处理的尺寸展宽换算成相干衍射尺度。这个尺度指晶体中能够维持相关周期排列的长度，不一定等于显微镜下完整颗粒的外形尺寸。一个颗粒包含多个晶粒，或者内部缺陷打断有序排列时，两者可以明显不同。公式中的形状因子与晶体形状、峰宽定义等有关，常用近似值0.9适合入门计算，但不是对所有样品固定不变的自然常数。先说明使用了哪个峰、哪种宽度和哪些修正，再解释得到的长度。

$$
D\approx\frac{K\lambda}{\beta_s\cos\theta},\qquad \beta_s=\sqrt{\beta_o^2-\beta_i^2}\quad\text{(Gaussian profiles)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 由尺寸展宽估计的相干衍射尺度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 与形状和峰宽定义有关的因子，无量纲；教学例取0.9。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X射线波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/adf8cfc447681bea28281828.svg) | 归属于样品尺寸贡献的2θ半高全宽，弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/714bfb9affa05813acb8606a.svg) | 观测峰的2θ半高全宽，弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/58e8ca623882ae98a67c5493.svg) | 同条件下仪器高斯峰宽，弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 峰位2θ的一半，计算余弦时使用弧度。 |

平方相减只用于本例高斯卷积，且样品展宽被设为纯尺寸贡献。0.303117°观测宽度与0.12°仪器宽度给出0.278352°样品宽度，换成弧度后得到30 nm。直接用观测宽度约得27.55 nm。

用本篇的数值走一遍：间距0.25 nm对应峰位35.8919°，设定相干尺度30 nm时，样品尺寸贡献的半高宽约0.27835°。若仪器高斯半高宽为0.12°，观测宽度约0.30312°。直接把这个较大的宽度代入谢乐关系，会得到约27.55 nm；先按高斯卷积关系扣除仪器贡献，再换成弧度，则恢复30 nm。差别来自已经明确加入的仪器展宽。把这些中间数值列出来，可以检查单位转换和峰宽定义，也能说明标准样品为什么是计算的一部分。

仪器本身会使峰变宽，包括光学几何、波长分布和探测系统的影响。可以测量适合的标准样品，建立对应条件下的仪器峰形，再从观测峰形中分离样品贡献。本篇用两个高斯峰宽的平方相加来演示这一过程，因为高斯卷积具有这样的关系；洛伦兹峰或混合峰形需要不同处理。若观测宽度已经接近仪器宽度，扣除后的小差别会对误差非常敏感，尺寸估计也随之不稳定。图中的曲线直观显示，直接把观测宽度代入会低估设定的相干尺度。

微观应变也会展宽。不同位置的晶面间距略有差别，就像许多中心稍有偏移的小峰叠在一起，最终形成更宽的整体峰。堆垛层错、各向异性尺寸和多相重叠还会带来更复杂的形状。利用多条反射及其角度依赖，可以进一步区分尺寸与应变贡献；这需要适合材料的模型和足够数据。单个宽峰提供的是有限信息，把它直接换成一个看似精确的粒径，容易掩盖尚未分开的物理贡献。

单位检查能避免一个很大的数值错误。常见图样横坐标用度，谢乐关系中的峰宽却要用弧度，而且宽度是2θ轴上的宽度。把0.3°直接写成0.3 rad，会产生约57倍的差别。θ仍然是峰位置的一半，不是峰宽的一半。实际计算时，先在图上标出峰中心、半高位置与两个半高交点，再把相应宽度转换单位。一个简单示意往往比记住变量名称更能防止角度混用。

## 峰面积、宽散射和背景，为什么需要一起解释

半结晶聚合物的图样常同时包含较窄反射和宽散射。较窄反射与有序区域有关，宽散射则包含无序结构的贡献；仪器和样品环境还会增加背景。要比较处理前后的有序程度，可以在明确角度范围与分解模型下，估计晶体峰面积占两类样品散射面积的比例。这个操作看似只是积分，实际上首先要决定哪些信号属于样品、如何表示宽散射以及怎样处理重叠峰。不同定义得到的指数可以用于各自一致的比较，但需要与质量结晶度等其他量区分。

$$
X_A=\frac{A_c}{A_c+A_a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/61f0812c0240edef2566362b.svg) | 在指定模型与扫描范围下的晶体峰面积指数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | 扣除背景后归属于晶体峰的总积分强度，共同强度×角度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/97cabe215ef9775c31d616d7.svg) | 同范围内归属于宽散射成分的积分强度，与Ac同单位。 |

50000/(50000+35000)=0.588235，即58.82%。等角度网格上求和时，共同角度步长在比值中消去。该量由背景、分解和取向等条件定义；与质量结晶度的换算需要适合材料的校准和散射模型。

本篇构造三个晶体峰和一个宽散射成分，并加入常数背景。三个峰的总面积系数为50000，宽成分为35000，因而教学模型的峰面积指数为50000除以85000，约58.82%。这里每个峰形在相同角度网格上归一化，系数对应相同扫描范围内的总计数贡献。程序先联合拟合这些成分，再检查背景假定改变时的指数变化。已知峰形让练习容易检验；真实聚合物中的宽散射、织构和吸收等因素需要依据实际体系建立分析方案。

![构造教学图样，三个窄峰与一个宽成分共同拟合，不指定真实晶相。A为观测与拟合；B为模型分解；C为标准化残差；D保持观测不变，改变背景假定后重新拟合面积指数。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8d658c4a3b93388c91609125.svg?v=8d658c4a3b93)

图 3构造教学图样，三个窄峰与一个宽成分共同拟合，不指定真实晶相。A为观测与拟合；B为模型分解；C为标准化残差；D保持观测不变，改变背景假定后重新拟合面积指数。

对于同一组计数，先扣掉很高的背景再拟合，可能把宽散射成分削弱，进而抬高晶体峰面积比例；背景偏低则可能把多余信号分配给宽成分。图中保持观测不变，只改变固定背景，展示这种分配如何影响结果。更复杂的背景不一定更正确，因为它也可能吸收真实的宽峰。适合依据空样品托、相邻角度范围和物理模型确定背景形式，再检查结果对合理选择是否稳定。这样获得的指数变化，才能与材料处理带来的变化放在同一尺度上比较。

峰高和峰面积也不能混用。在总散射贡献相同的教学模型里，峰变宽以后，峰顶会降低，但面积保持不变。因此，一条较矮的峰可以仅仅意味着更宽的分布，而不一定意味着有序区域减少。反过来，择优取向可以让某个峰很高，却未必增加整个样品的晶体质量分数。比较处理前后曲线时，可以先统一测量和归一化规则，同时看位置、面积、宽度与二维取向信息，避免用一个视觉特征替代多个物理问题。

残差是观测曲线减去模型曲线后剩下的部分。若残差在某段角度持续同号，可能意味着背景形状不合适、漏掉反射、峰宽不匹配或存在未考虑的相。拟合软件给出很小的整体误差时，也要检查局部系统偏差。全谱精修通过结构与仪器模型同时解释大量数据，是进一步研究的工具；它的参数需要有物理含义，并与采集范围和质量相匹配。让模型复杂度随着问题与证据增长，比一开始释放所有参数更容易理解每一步为什么改善解释。

## 把晶格膨胀与尺寸变化分开观察

交互实验围绕一个间距0.25 nm的教学反射展开。你可以改变晶格间距的相对变化、相干尺度以及仪器高斯峰宽。图中同时显示样品本征峰和加入仪器展宽后的观测峰，二者采用相同面积归一化。增大间距会移动峰中心，减小相干尺度会让峰变宽，提高仪器宽度也会让峰变宽。前一种变化主要涉及周期位置，后两种变化则可能在外观上相似，需要借助标定分开。数字区给出直接代入观测宽度和扣除已知仪器宽度后的尺寸，便于比较。

## 同一个峰，位置与宽度各由什么改变

波长0.15406 nm、初始间距0.25 nm、形状因子0.9。绿色为纯尺寸峰，蓝色为加入仪器高斯展宽后的峰；二者面积相同。

[Figure: 衍射峰位置与宽度](https://ml-biomat.com/tutorials/experimental-methods/i06/#I06-plot)

先把仪器宽度设小，改变相干尺度，建立峰宽与尺寸的关系；再固定样品，把仪器宽度增大，观察未经修正的结果怎样偏离。最后改变间距，检查峰向哪一侧移动，并把计算的θ与横坐标2θ对应起来。这里采用高斯峰与指定形状因子，练习范围内每一项变化都有明确来源。真实测量可以沿用这种逐项检查的思路，再加入材料所需的应变、取向和多相模型。

## 从一条曲线走向一套可解释的结构判断

曲线归一化也会改变视觉重点。把每条曲线最高峰缩放到相同高度，适合比较位置，却移除了该峰原本的绝对高度差；按总面积缩放强调所选范围内的相对分配，按曝光时间归一则保留另一种计数关系。样品量、吸收或照射体积改变时，每秒计数也不自动等于单位质量散射。保留原始计数并说明绘图变换，才能区分材料变化与展示方式。固定种子运行中，面积指数拟合约59.05%，无噪声期望值则恢复设定的58.82%，二者展示了正确模型下的计数波动。

如果要比较三种冷却速度下的聚合物，可以先保持样品厚度、测量几何和角度范围一致，分别观察反射位置、宽度、取向与面积分解。较慢冷却可能改变有序区域的形成过程，但具体趋势需要由材料体系与数据决定。再把这些结构量与同批样品的热分析、力学或光学性能联系起来，能够检验哪一种结构变化最接近性能变化。每种冷却条件使用独立制备样品，并把重复装样与独立制备区分，可以同时观察测量重现性与材料制备差异。

多相材料中的全谱分析还需要注意参数之间的补偿。某一相的含量、择优取向参数、背景与峰宽有时都能改变相似角度范围的强度，软件可能用其中一个参数去弥补另一个模型缺口。先从已知组成与简单峰形出发，逐步加入有物理理由的自由度，并检查参数是否稳定、是否出现不合理值，有助于保持解释清楚。一个很低的拟合误差只有与合理结构、合适参照和可解释残差相联系时，才真正帮助回答研究问题。

完整程序生成布拉格几何示意、有限周期干涉曲线，以及带噪声教学图样的联合拟合与背景敏感性图。数据表保存每个角度的期望计数、构造观测、拟合值和标准化残差，计算摘要保存峰位、峰宽、尺寸与面积指数。你可以改变峰之间的距离，观察重叠如何增加；也可以让宽散射的形状偏离拟合模型，检查残差是否出现连续结构。这样既能学习计算，也能练习从计算留下的问题反推模型需要补充什么。

### 完整Python：衍射峰位、展宽和面积分解

生成确定的物理几何与固定种子教学计数，保存逐角度表格、拟合残差和数值摘要。

```
"""XRD teaching model: Bragg geometry, coherent domains and profile fitting.

Patterns are constructed, with no claimed identity as a measured material.
Peak areas use normalized discrete basis functions over this scan range.
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
from scipy.optimize import nnls
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def peak_properties(d=.25,D=30.,instrument=.12,wavelength=.15406):
    theta=np.arcsin(wavelength/(2*d));center=np.rad2deg(2*theta)
    beta=np.rad2deg(.9*wavelength/(D*np.cos(theta)))
    observed=np.hypot(beta,instrument)
    naive=.9*wavelength/(np.deg2rad(observed)*np.cos(theta))
    return center,beta,observed,naive

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    ax=axes[0];ax.set(xlim=(-5,5),ylim=(-3.8,4.5));ax.set_aspect('equal');ax.axis('off');ax.set_title(tr('A  布拉格几何：比较两条路程','A  Bragg geometry: compare two paths'))
    for y in [0,-1.6,-3.2]:
        ax.plot([-4.8,4.8],[y,y],color=gray,lw=1)
        ax.scatter(np.linspace(-4.5,4.5,10),np.full(10,y),s=23,color=gray)
    for y,col in [(0,green),(-1.6,blue)]:
        ax.annotate('',(0,y),(-4,y+2.8),arrowprops={'arrowstyle':'->','color':col,'lw':2});ax.annotate('',(4,y+2.8),(0,y),arrowprops={'arrowstyle':'->','color':col,'lw':2})
    ax.annotate('',(4.5,0),(4.5,-1.6),arrowprops={'arrowstyle':'<->','color':red});ax.text(4.65,-.8,'d',color=red);ax.text(-2.4,.25,'θ',color=green);ax.text(1.9,.25,'θ',color=green)
    ax.text(0,3.9,tr('额外路程：2d sinθ = nλ','Extra path: 2d sinθ = nλ'),ha='center',fontsize=13)
    ax.text(0,-3.75,tr('原子面为几何构造；电子散射形成干涉','Planes are a geometrical construction; scattering interferes'),ha='center',fontsize=9)
    ax=axes[1];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(tr('B  1912—1913：角度变成结构信息','B  1912–1913: angle becomes structure'))
    ax.plot([1,5,9],[6,2,6],color=blue,lw=3);ax.scatter([5],[2],s=400,marker='D',color=green);ax.text(.5,6.6,tr('X射线','X-rays'));ax.text(4.3,1,tr('晶体','Crystal'));ax.text(8,6.6,tr('探测器','Detector'))
    ax.add_patch(Arc((5,2),5,5,theta1=45,theta2=135,color=red,lw=1.5));ax.text(5,5,tr('扫描散射方向','Scan scattering direction'),ha='center')
    ax.text(5,.1,tr('晶体周期 → 峰位置；内部排列 → 强度','Crystal periodicity → positions; arrangement → intensities'),ha='center',fontsize=10)
    save(fig,'bragg')
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    phase=np.linspace(-.7,.7,2001)
    for N,col in [(10,green),(30,red),(80,blue)]:
        amplitude=np.sum(np.exp(1j*np.outer(phase,np.arange(N))),axis=1)/N
        axes[0].plot(phase,np.abs(amplitude)**2,color=col,label=f'N={N}',lw=2)
    axes[0].set(xlabel=tr('相邻周期相位偏离 / rad','Phase offset per repeat / rad'),ylabel=tr('归一化干涉强度','Normalized interference intensity'),title=tr('A  有序周期越多，峰越窄','A  More coherent repeats, narrower peaks'));axes[0].legend(frameon=False)
    sizes=np.linspace(5,120,200);widths=np.array([peak_properties(D=d)[2] for d in sizes]);naive=np.array([peak_properties(D=d)[3] for d in sizes]);axes[1].plot(sizes,naive,color=red,lw=2,label=tr('直接用观测宽度','Using observed width'));axes[1].plot(sizes,sizes,color=green,ls='--',label=tr('扣除已知仪器高斯宽度','Known Gaussian instrument correction'));axes[1].set(xlabel=tr('设定相干尺寸 / nm','Specified coherent size / nm'),ylabel=tr('估计尺寸 / nm','Estimated size / nm'),title=tr('B  仪器展宽需要标定','B  Instrument broadening needs calibration'));axes[1].legend(frameon=False,fontsize=9)
    save(fig,'coherence')
    angle=np.linspace(10,70,3001);ds=np.array([.4,.25,.2]);centers=np.array([peak_properties(d=d)[0] for d in ds]);widths=np.array([peak_properties(d=d)[2] for d in ds])
    def g(center,width):
        v=np.exp(-4*np.log(2)*((angle-center)/width)**2);return v/v.sum()
    crystalline=np.column_stack([g(c,w) for c,w in zip(centers,widths)]);amorphous=g(23,9);design=np.column_stack([crystalline,amorphous,np.ones(len(angle))]);truth=np.array([16000.,22000.,12000.,35000.,12.]);expected=design@truth;rng=np.random.default_rng(1706);observed=rng.poisson(expected);coef,_=nnls(design,observed);fit=design@coef;residual=(observed-fit)/np.sqrt(np.maximum(fit,1))
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    axes[0,0].plot(angle,observed,color=gray,lw=.7,label=tr('构造观测','Constructed observation'));axes[0,0].plot(angle,fit,color=green,lw=1.5,label=tr('已知峰形联合拟合','Joint fit with known shapes'));axes[0,0].set(xlabel='2θ / °',ylabel=tr('计数 / 步','Counts / step'),title=tr('A  完整扫描与拟合','A  Full scan and profile fit'));axes[0,0].legend(frameon=False,fontsize=9)
    axes[0,1].plot(angle,crystalline@coef[:3],color=blue,label=tr('晶体峰贡献','Crystalline peaks'));axes[0,1].plot(angle,amorphous*coef[3],color=red,label=tr('宽散射贡献','Broad contribution'));axes[0,1].axhline(coef[4],color=gray,label=tr('常数背景','Constant background'));axes[0,1].set(xlabel='2θ / °',ylabel=tr('计数 / 步','Counts / step'),title=tr('B  区分峰、宽散射与背景','B  Peaks, broad scattering and background'));axes[0,1].legend(frameon=False,fontsize=9)
    axes[1,0].plot(angle,residual,color=green,lw=.6);axes[1,0].axhline(0,color=gray);axes[1,0].set(xlabel='2θ / °',ylabel=tr('标准化残差','Standardized residual'),title=tr('C  检查未解释的角度结构','C  Inspect unexplained angular structure'))
    choices=np.linspace(8,16,80);indices=[]
    for bg in choices:
        a,_=nnls(design[:,:4],observed-bg);indices.append(a[:3].sum()/a[:4].sum())
    axes[1,1].plot(choices,np.array(indices)*100,color=red,lw=2);axes[1,1].axvline(12,color=gray,ls='--');axes[1,1].set(xlabel=tr('固定背景 / 计数每步','Fixed background / counts per step'),ylabel=tr('模型峰面积指数 / %','Model peak-area index / %'),title=tr('D  背景选择改变面积分解','D  Background changes the area decomposition'))
    save(fig,'profile')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['two_theta_deg','expected_counts','constructed_counts','fitted_counts','standardized_residual']);w.writerows(zip(angle,expected,observed,fit,residual))
    center,beta,bobs,naive=peak_properties();exact,_=nnls(design,expected)
    summary={'center_d025_deg':center,'size_fwhm_D30_deg':beta,'observed_fwhm_deg':bobs,'uncorrected_size_nm':naive,'corrected_size_nm':.9*.15406/(np.deg2rad(np.sqrt(bobs*bobs-.12**2))*np.cos(np.deg2rad(center/2))),'true_area_index':50000/85000,'fitted_area_index':float(coef[:3].sum()/coef[:4].sum()),'noiseless_area_index':float(exact[:3].sum()/exact[:4].sum()),'q_d025_invnm':2*np.pi/.25,'peak_positions_deg':centers.tolist(),'data_origin':'Constructed teaching pattern, not an experimental phase or crystallinity measurement.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

回到最初的钙磷沉积问题，一次有组织的分析会把元素组成、多个衍射反射、样品状态以及适合的化学结构信息联系起来。对于聚合物，则可以把热处理历史、二维取向、峰形变化和力学性能放在同一条研究线上。XRD的价值在于让原子尺度的周期排列以角度和强度的形式出现；读懂这些信号的形成过程，才能从“这张图有几个峰”进一步走向“哪些结构变化解释了材料行为”。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [IUCr — Scope, potential and applications of X-ray analysis](https://www.iucr.org/education/pamphlets/2)

   从散射与成像类比进入结构测量。

   Public educational reference; figures original.
2. [IUCr — Calculation of structure factors](https://www.iucr.org/education/pamphlets/3)

   相位叠加、原子排列与反射强度。

   Public educational reference; figures original.
3. [Nobel Foundation — 1915 presentation speech](https://www.nobelprize.org/prizes/physics/1915/ceremony-speech/)

   布拉格平行面解释与早期晶体结构分析。

   Historical primary record; no historical image reproduced.
4. [NIST — SRM 1979 diffraction line-profile standard](https://www.nist.gov/publications/certification-standard-reference-material-1979-powder-diffraction-line-profile-standard)

   相干尺寸、微应变、层错和峰形标定。

   Government research reference.
5. [NIST SRM 1979 certification paper](https://nvlpubs.nist.gov/nistpubs/jres/125/jres.125.020.pdf)

   深入阅读标准材料的峰形与背景处理。

   Government research publication; figures not reused.
