# 疲劳实验：反复加载怎样留下损伤

Source: https://ml-biomat.com/tutorials/experimental-methods/m04/
Language: zh-CN

读懂循环载荷、寿命离散、未失效试样和裂纹增长，把反复使用变成可分析的历史。

## 一次没有压坏，为什么反复使用后会坏

把回形针轻轻掰一下，它可能还能恢复原来的样子；反复向两边弯折，同一个位置却会逐渐变软，最后断开。鞋底、关节软骨替代材料、柔性导线和植入器件每天也在经历重复载荷。一次拉伸实验能告诉我们材料在不断增大的载荷下怎样失效，疲劳实验则问另一件事：每一次都没有达到单次破坏条件，重复许多次以后，材料是否仍能保持功能。这里的“疲劳”指材料结构在循环作用下发生演化，并不是材料像人一样因为劳累而需要休息。

循环失效可以从表面微小缺陷开始，也可能涉及孔隙、界面脱粘、局部塑性或高分子网络的损伤。某些阶段外观变化很少，裂纹却已经缓慢增长；最后剩下的承载部分不足，才出现一次明显断裂。因此，疲劳研究有两条互相联系的路线。一条从完整试样出发，记录某种循环条件下到达规定失效状态的次数；另一条从可测量裂纹出发，记录每一批循环使裂纹增加多少。前者常用于寿命比较，后者帮助理解已有缺陷怎样发展，两个结果不能不加区分地放在同一个坐标轴上。

十九世纪铁路车轴的失效推动了疲劳实验的发展。Wöhler在1858至1870年间发表了一系列系统试验，把重复应力与承受的循环次数联系起来。旋转弯曲特别适合说明这个问题：外部弯曲载荷方向可以保持不变，但车轴表面的某一点转到上方和下方时，会轮流处在受拉与受压区域。材料点经历的是循环应力，而不是一份静止不变的载荷。下图用原理示意把旋转与应力波形连起来，这也是为什么分析疲劳时，应跟着材料点的受力历史走，而不只看机器外力是否换向。

![原创旋转弯曲原理图：固定方向弯曲载荷下，旋转材料点交替受拉压。右侧应力为示意值，非Wöhler历史数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/299c53a0123933c12686ce7b.svg?v=299c53a01239)

图 1原创旋转弯曲原理图：固定方向弯曲载荷下，旋转材料点交替受拉压。右侧应力为示意值，非Wöhler历史数据。

## 一个循环必须说清最大值、最小值和速度

先看一条简单的正弦应力曲线。最大应力与最小应力的中点是平均应力，两者差值的一半是应力幅；最大值减最小值则是应力范围。幅与范围相差二倍，名称相近却不能混用。若循环从10 MPa升到100 MPa再回到10 MPa，平均应力为55 MPa，应力幅45 MPa，应力范围90 MPa，最小值与最大值之比为0.1。这个比值通常记作R，帮助读者迅速判断循环是否一直在拉伸，以及最低载荷相对于最高载荷有多大。

$$
\sigma_m=\frac{\sigma_{\max}+\sigma_{\min}}{2},\quad\sigma_a=\frac{\sigma_{\max}-\sigma_{\min}}{2},\quad\Delta\sigma=2\sigma_a,\quad R=\frac{\sigma_{\min}}{\sigma_{\max}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5269b242adb1189076e77772.svg) | 平均应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1e1d1d71588c211f946d0524.svg) | 应力幅，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b70db1f8af3fa7ce2b6c46bd.svg) | 一个循环的最大应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/36459aa93561f626acf00ff1.svg) | 一个循环的最小应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2073bb3222b4607f026726c2.svg) | 应力范围，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 应力比，无量纲，最大值非零。 |

10至100 MPa循环给出平均55、幅45、范围90 MPa，R=0.1。相同最大值而最低值不同会同时改变幅和平均值。

同样的最大应力并不代表同样的循环。把最低值从10 MPa提高到50 MPa，最高值仍是100 MPa，应力幅却从45 MPa变成25 MPa，平均应力从55 MPa变成75 MPa。裂纹的张开程度、闭合过程和循环塑性都可能随之改变。比较疲劳曲线时，应力比、控制方式和波形应一起记录。完全反向循环的R为负一，从零到正拉力的循环R为零，而拉–拉循环常有正R。对于压缩试验，应先说明正负号约定，再使用比例，避免把符号看似相同的数当成相同受力状态。

频率告诉我们每秒有多少个完整循环。五赫兹意味着每秒五圈，一百万圈约需要55.6小时；换成一百赫兹，钟表时间会大幅缩短，但材料内部过程未必保持相同。高分子在每圈中耗散的能量可能变成热，频率提高后散热来不及，试样温度就会上升。含水网络还可能来不及排液或恢复，腐蚀介质中的化学过程则依赖实际停留时间。加速测试应同时观察温度、波形跟踪和材料响应，确认改变频率后仍然在研究同一种主导过程。

机器控制的是力、位移或局部应变中的某一个量，其余量是响应。力控制下，材料变软可能使变形逐渐增大；位移控制下，同样的软化会让峰值力下降。两种曲线变化都可能是损伤的表现，也可能包含可恢复的网络重排，因此要结合卸载后的残余变形和恢复过程判断。图中的滞后环表示加载与卸载走了不同路径，环面积对应一圈内的机械能损失。它能提示耗散和发热，却不是“这一圈已经消耗了多少总寿命”的直接刻度。

![左：最大应力100 MPa相同、R不同的两种循环。右：独立构造滞后环说明每圈耗散；该环不是S–N或Paris数据的材料模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/18ac63835a12ceb078f31cbd.svg?v=18ac63835a12)

图 2左：最大应力100 MPa相同、R不同的两种循环。右：独立构造滞后环说明每圈耗散；该环不是S–N或Paris数据的材料模型。

## 寿命曲线上的箭头，也是实验结果

应力–寿命曲线常简称S–N曲线。让多个独立试样分别在几个应力水平下循环，记录到达预定失效条件时的循环次数，再把应力与次数画在一起。横轴通常使用对数，因为寿命可能跨越几千到几百万圈。对数坐标每前进一格代表相同倍数，不是增加相同次数，所以图上看似相近的两个点，实际寿命可能相差很大。失效条件也要在测试前确定：完全断开、刚度下降某一比例、裂纹达到某一长度，或者器件输出偏离规定范围，得到的是不同定义的寿命。

$$
N_{50}=N_{\mathrm{ref}}\left(\frac{\sigma_a}{\sigma_{\mathrm{ref}}}\right)^{-b},\qquad\log_{10}N\sim\mathcal N\!\left(\log_{10}N_{50},s^2\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8e84b28fc356c74bc8262265.svg) | 指定应力幅下的中位失效循环数，cycles。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0d389c9b3256376faa184ef9.svg) | 参考应力幅下中位寿命，本例10⁶ cycles。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1e1d1d71588c211f946d0524.svg) | 应力幅，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1a95f2b7007feac96d8dcf4f.svg) | 参考应力幅，本例100 MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 应力–寿命幂指数，本例5，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 单个试样失效循环数，cycles，取数值计算对数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | log10寿命的标准差，本例0.16，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0e378265ddb70b5dadd36830.svg) | 正态分布记号，参数为均值与方差。 |

同一载荷比、波形和环境下的教学幂律及对数正态离散。125 MPa给出N50=327680圈；一百万圈停机而未断的试样提供N>10⁶的信息。

本节规定一条教学关系：100 MPa应力幅对应一百万圈的中位寿命，应力幅提高时寿命按五次方下降。125 MPa对应327680圈，150 MPa约对应131687圈。这里的中位数表示同样条件下，寿命分布有一半在它之前、一半在它之后，不是每一根试样都必须恰好在那里断裂。程序在对数寿命上加入随机离散，构造24个独立试样，再统一在一百万圈处停机。这样，较低应力下的一些试样会在停机时仍然完好，形成疲劳实验中常见的未失效记录。

这类记录称为右删失或runout。它提供的信息是寿命超过已经经历的次数，而不是寿命恰好等于停机次数。图中用向右箭头表示这个方向。如果把所有箭头都当成一百万圈时的断裂点，会把长寿命压短；如果把它们删掉，只保留已经断开的试样，又会优先留下较短寿命。两种做法都丢掉了原始观察的含义。数据表因此需要同时保存观测循环数与是否发生失效的标记，让后续分析能够区分“看到了断裂”与“到这里还没有断裂”。

本例用最大似然估计处理这两种观察。对已经失效的试样，模型评价这个寿命附近出现失效的可能性；对未失效试样，模型评价活过停机次数的可能性。程序采用对数寿命近似正态分布，搜索最能解释全部记录的曲线位置、斜率与离散程度。图中的浅色区域是拟合寿命分布的10%至90%分位范围，描述试样之间的分散，不是拟合中位曲线的置信区间。理解这一区别后，读者就能看出误差带究竟在表达材料离散性，还是表达我们对曲线位置掌握得有多准。

![构造24个独立试样，10⁶圈停机。向右箭头为未失效记录；带为拟合寿命分布10–90%分位，不是参数置信区间。右图显示100 MPa条件下的生存概率尾部。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d3a0e9b6a1aca6ed7b506589.svg?v=d3a0e9b6a1ac)

图 3构造24个独立试样，10⁶圈停机。向右箭头为未失效记录；带为拟合寿命分布10–90%分位，不是参数置信区间。右图显示100 MPa条件下的生存概率尾部。

## 不等它断开，直接跟踪裂纹每圈走多远

寿命包含裂纹形成和后续增长等多个阶段。如果试样已经有一条能观察的裂纹，就可以单独研究增长过程。先记录裂纹长度，施加一批循环，再重新测量，长度增量除以循环增量就是平均每圈扩展量。这个数可能很小，远小于单帧图像能辨认的距离，因此常常需要累积足够的循环后再测。测量窗口太短，定位误差占主导；窗口太长，驱动力已经明显变化，又会把一个弯曲过程平均成粗糙的直线。窗口应与图像分辨率和增长速度共同选择。

$$
\frac{da}{dN}=C(\Delta K)^m,\qquad\Delta K=Y\Delta\sigma\sqrt{\pi a},\qquad N_p=\int_{a_0}^{a_f}\frac{da}{C[Y\Delta\sigma\sqrt{\pi a}]^m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 本例中央裂纹半长，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 累计循环数，cycles。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Paris系数；本例m=3时单位为m/cycle/(MPa·√m)³，取10⁻¹⁰。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Paris增长指数，本例3，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1b568e0bb351fe2c942a6f22.svg) | 模式I应力强度范围，MPa·√m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ab4817775494786b06f0b9ce.svg) | 几何系数，本例宽大板取1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2073bb3222b4607f026726c2.svg) | 远场应力范围，本例60 MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5a9c1aa4dbcfe2c2217b3e46.svg) | 从初始到规定终点的传播循环数，cycles。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6301e767c6538ae4707f3d93.svg) | 初始半长，本例0.001 m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa14f1964a62cdb086a276be.svg) | 规定终点半长，本例0.006 m。 |

中段长裂纹线弹性教学模型，保持工况，忽略阈值与失稳段。积分把每段长度除以当地增长率再相加。数值求解与m=3解析积分独立核对。

Paris与Erdogan在1963年的研究讨论了裂纹扩展规律与数据范围，今天常用的Paris关系把每圈扩展速率与应力强度因子范围联系起来。在许多线弹性长裂纹的中段数据中，双对数图上可以出现近似直线，斜率是指数，位置由系数决定。系数的单位随指数和应力强度单位而变化，因此把以毫米为长度单位的一组系数直接用于以米计算的程序，会产生严重错误。靠近阈值的缓慢增长、短裂纹以及接近快速失稳的阶段，都需要与各自过程相符的描述，不能仅把同一条中段直线无限延长。

本例规定指数为三，系数为每圈每三次方MPa·√m对应一乘十的负十次方米，并取应力范围60 MPa、几何系数为一。中央裂纹的半长从1 mm开始，计算到预先规定的6 mm终点。由于裂纹变长会使应力强度范围增大，即使外部应力范围不变，增长也会逐渐加快。程序同时用解析积分与数值微分方程求解，核对两条路径的一致性。这个终点是为了比较传播寿命而选定的长度，不是由断裂韧性自动求出的最终破坏尺寸。

改变初始缺陷就能改变到同一终点的循环数。将初始半长从1 mm增到2 mm，省掉的不只是最前面1 mm的长度，还省掉了原本增长很慢的早期阶段，因此传播寿命会显著缩短。这让裂纹检测与寿命模型建立了直接联系：能够识别多小的缺陷，决定模型从哪个状态开始计算。真实结构中，几何系数通常随裂纹与部件尺寸之比改变，载荷比、残余应力和裂纹闭合也会影响增长。把这些条件与拟合数据配对，才能让模型服务于同一种裂纹和环境。

![构造Paris中段数据、初始裂纹对传播的影响、Miner份额及传播寿命敏感性。6 mm是规定比较终点，非由韧性自动确定的失稳尺寸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2aeabdf938b35bb5e7c78b13.svg?v=2aeabdf938b3)

图 4构造Paris中段数据、初始裂纹对传播的影响、Miner份额及传播寿命敏感性。6 mm是规定比较终点，非由韧性自动确定的失稳尺寸。

## 不同大小的循环，能否直接相加

实际使用很少只包含一种固定振幅。走路、跑步和偶尔跳跃给鞋底带来不同载荷；柔性器件也会经历小幅日常弯曲与少量大幅折叠。最简单的线性累积办法是，把某一应力水平实际经历的次数除以该水平对应的参考寿命，作为一个损伤份额，再把各份额相加。这就是常见的Miner累积思路。它像把不同工况折算成同一本账里的份额，便于初步比较载荷谱，但账本里的数字是模型指标，不是显微镜下能够直接数出的断键百分比。

$$
D=\sum_i\frac{n_i}{N_i}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Miner线性累积指标，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 载荷水平或载荷块编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ac70a528e41a9bd73952b00.svg) | 第i水平实际施加循环数，cycles。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | 同一水平的参考恒幅寿命，cycles。 |

相同定义的参考寿命与工况；线性相加本身不含顺序效应。10万圈/327680圈 + 20万圈/100万圈 = 0.5051758。D=1是选定模型中的名义终点，不是通用实测断键比例。

使用本节规定的寿命曲线，在125 MPa下经历十万圈，对应份额约0.3052；在100 MPa下经历二十万圈，对应0.2；相加得到约0.5052。若只按这个线性模型计算，交换两个载荷块的先后次序，结果完全相同。真实材料却可能记住先后顺序：大载荷造成的塑性区、残余应力、网络软化或裂纹闭合状态，会改变后面的增长。这个差别给出了检验模型的直接实验：设计相同次数和振幅、顺序相反的两组载荷，看响应是否相同，而不是先把模型相加结果当成已经测到的损伤。

不规则载荷还需要先定义如何计数。一个波形里可能有大循环包着小循环，简单数过零点会漏掉许多具有实际幅值的往返。雨流计数是一类把复杂历史分解成循环范围与平均值的方法，常用于建立载荷谱；它解决的是计数问题，后续仍需要与相应的材料疲劳关系结合。保存原始时间序列非常重要，因为只留下直方图会丢掉顺序和停留时间。若材料对休息恢复或持续载荷敏感，这些被丢掉的信息恰好可能影响结果。

高分子和含水材料尤其值得同时保留循环数与钟表时间。三十万圈在五赫兹下约为16.67小时，在另一频率下可能经历不同的温度积累、排液和恢复。若插入长时间停机，材料状态还可能在没有新循环时继续变化。把实验分成载荷块、保持段与恢复段，并同步记录温度和峰谷值，可以让这种历史被后续分析使用。用一个平均频率概括全部过程，往往不足以解释为什么两组相同循环数的样品表现不同。

## 在真实水凝胶研究中，怎样看待“没有增长”

下面是一张真实研究图，来自Lin等人的抗疲劳断裂PVA水凝胶论文。图中保留了原始循环数、能量标注和比例尺：在所示载荷条件下，对比第10圈与第30000圈的缺口图像，可以观察裂口位置是否发生可辨认变化。大图比例尺为5 mm，局部图为1 mm。照片让“重复很多次后裂纹怎样变化”成为具体可看的证据，也提醒我们，材料耐一次撕裂与耐反复裂纹扩展需要分别测量。

![Lin等，Anti-fatigue-fracture hydrogels，arXiv:1812.06403v1（2018），图3H裁切，CC BY 4.0。90 min干态退火后溶胀PVA凝胶，原图G=1000 J/m²，比较N=10与30000；保留原始5 mm和1 mm比例尺及标注。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f37caf9733caf78c81022ae3.svg?v=f37caf9733ca)

图 5Lin等，Anti-fatigue-fracture hydrogels，arXiv:1812.06403v1（2018），图3H裁切，CC BY 4.0。90 min干态退火后溶胀PVA凝胶，原图G=1000 J/m²，比较N=10与30000；保留原始5 mm和1 mm比例尺及标注。

判断没有可辨认增长时，观察分辨率和循环窗口必须一起出现。假设长度定位只能可靠区分20 μm，经过1000圈后没有辨认出位移，那么这个窗口对应的平均增长分辨能力约为每圈20 nm。这个算术示例解释了为什么每圈增长可以小于单帧像素尺寸：实验积累的是很多圈后的总位移。若要更敏感，可以提高定位精度或延长观察窗口，同时检查加载条件是否保持稳定。有限窗口内未辨认到增长，是一个带着长度和时间尺度的观察结果。

在凝胶疲劳研究中，载荷循环可能先改变无缺口试样的应力–伸长曲线，使网络逐渐达到较稳定的循环状态；缺口试样的驱动力计算也应与相应状态匹配。只用第一圈的能量去代表几千圈后的状态，可能遗漏软化或结构重排。实验可以保存若干代表循环、周期性拍摄裂纹，并跟踪峰值力、残余伸长和环境温度。把这些信号并列之后，就能分清整体变软、裂纹扩展与仪器漂移各自在什么时候出现，为解释材料机制提供更多约束。

水浴与湿度控制也关系到裂纹观察本身。薄凝胶的边缘在空气中失水时，局部应力和尺寸都可能改变；长时间疲劳测试又比短时拉伸更容易受到蒸发影响。固定浸没状态、温度与介质，并检查标记或显影材料是否改变表面，是把图像变化归到材料响应的重要步骤。对透明样品，可以用适合的照明、表面纹理或局部标记改善裂尖可见度，但需要让这些处理在比较组之间保持一致。

## 从完整记录计算寿命与裂纹增长

程序生成的数值记录与研究照片分开保存。数值部分使用固定随机种子，构造24个试样的应力–寿命数据，明确标出失效与停机未失效；随后比较包含删失信息的拟合与只使用失效点的拟合。另一部分构造Paris中段增长数据，拟合指数和系数，再独立求解从已知初始裂纹到规定终点的传播。图中的寿命分位带、增长速率和线性损伤份额都来自这些计算，读者可以通过导出的表格重新画图，而不必从图片反推数字。

替换成实测文件时，先检查循环计数是否连续，以及停机后重新开始的计数有没有归零。若机器分段保存文件，同一个试样的第二段不能被误当成一个新试样。失效标记应对应预先定义的判据，异常停机、夹具滑移和试样断裂应分别记录。测量中断时已经经历的循环仍然是有效历史，只是后续是否继续以及怎样计入分析，需要与中断原因对应。保留这层记录，比在最后拟合时试图凭曲线外观猜测状态更可靠。

### 完整Python：删失寿命、Paris增长与载荷块

数值记录全部为构造数据；实际论文照片以独立许可文件随示例提供。

```
"""Fatigue teaching: censored stress-life data and a separate Paris growth model.
The bundled photograph is actual CC BY 4.0 research; see data/NOTICE.txt.
All numerical records generated here are constructed, not that paper's data.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Arc

def life(stress):return 1e6*(np.asarray(stress)/100.)**-5
def growth_life(a0=.001,af=.006,ds=60.,C=1e-10):
    return 2*(a0**-.5-af**-.5)/(C*(ds*np.sqrt(np.pi))**3)
def growth(n,a0=.001,ds=60.,C=1e-10,af=.006):
    ne=np.minimum(np.asarray(n),growth_life(a0,af,ds,C));return (a0**-.5-.5*C*(ds*np.sqrt(np.pi))**3*ne)**-2

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1904);S=np.repeat([80.,90.,105.,125.,150.,180.],4);true_log=np.log10(life(S))+rng.normal(0,.16,len(S));stop=1e6;Ntrue=10**true_log;failed=Ntrue<=stop;Nobs=np.minimum(Ntrue,stop);x=np.log10(S/100);y=np.log10(Nobs)
    def objective(q):
        mu=q[0]-q[1]*x;sd=np.exp(q[2]);z=(y-mu)/sd
        return -np.sum(np.where(failed,norm.logpdf(z)-np.log(sd),norm.logsf(z)))
    fit=minimize(objective,[6,5,np.log(.16)],method='L-BFGS-B',bounds=[(4,8),(1,10),(np.log(.03),np.log(.7))]);assert fit.success,fit.message
    intercept,m,logsd=fit.x;sd=float(np.exp(logsd));ols=np.polyfit(x[failed],y[failed],1)
    DK=np.geomspace(3.5,12,36);rate=1e-10*DK**3*10**rng.normal(0,.08,len(DK));mp,cp=np.polyfit(np.log10(DK),np.log10(rate),1);Cfit=10**cp
    nend=growth_life();nn=np.linspace(0,nend,401);aa=growth(nn);ode=solve_ivp(lambda n,v:[1e-10*(60*np.sqrt(np.pi*v[0]))**3],(0,nend),[.001],rtol=1e-10,atol=1e-13,dense_output=True);ode_error=float(np.max(abs(ode.sol(nn)[0]-aa)))
    blocks=np.array([100000.,200000.]);levels=np.array([125.,100.]);damage=blocks/life(levels)
    summary={'specimens':len(S),'failures':int(failed.sum()),'runouts':int((~failed).sum()),'fit_intercept_log10N':float(intercept),'fit_stress_exponent':float(m),'fit_log10_scatter':sd,'failures_only_intercept':float(ols[1]),'fit_median_life_at100':float(10**intercept),'specified_median_life_at125':float(life(125)),'specified_damage_sum':float(damage.sum()),'hours_300000cycles_at5Hz':300000/5/3600,'paris_fit_C':float(Cfit),'paris_fit_m':float(mp),'growth_cycles_1to6mm':float(nend),'growth_cycles_2to6mm':float(growth_life(.002)),'ode_max_error_m':ode_error,'growth_at_start_m_cycle':float(1e-10*(60*np.sqrt(np.pi*.001))**3),'stress_amplitude_100_10_MPa':45.,'mean_stress_100_10_MPa':55.,'stress_ratio_100_10':.1}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[S,Nobs,failed.astype(int)],delimiter=',',header='stress_amplitude_MPa,observed_cycles,failure_observed_1',comments='');np.savetxt(o/'growth.csv',np.c_[nn,aa*1000,60*np.sqrt(np.pi*aa),1e-10*(60*np.sqrt(np.pi*aa))**3],delimiter=',',header='cycles,crack_half_length_mm,delta_K_MPa_sqrt_m,da_dN_m_cycle',comments='');np.savetxt(o/'paris.csv',np.c_[DK,rate],delimiter=',',header='delta_K_MPa_sqrt_m,growth_rate_m_cycle',comments='');np.savetxt(o/'blocks.csv',np.c_[levels,blocks,life(levels),damage],delimiter=',',header='stress_amplitude_MPa,applied_cycles,median_constant_amplitude_life,miner_fraction',comments='')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));ax[0].set(xlim=(0,10),ylim=(0,7));ax[0].axis('off');ax[0].add_patch(Rectangle((1,3),8,.55,facecolor='#c5d6df',edgecolor=B));
    for xx in [2,8]:ax[0].add_patch(Rectangle((xx-.3,2.6),.6,1.4,facecolor='#6e8593'))
    ax[0].annotate('',(5,3.7),(5,5.7),arrowprops={'arrowstyle':'->','color':O,'lw':2});ax[0].text(5,6,tr('固定方向弯曲载荷','Bending load in a fixed direction'),ha='center');ax[0].add_patch(Arc((5,3.3),2,2,theta1=30,theta2=320,color=G,lw=2));ax[0].annotate('',(5.9,3.8),(5.8,4.1),arrowprops={'arrowstyle':'->','color':G});ax[0].scatter([4],[3.5],s=55,color=O);ax[0].text(5,1.3,tr('表面一点随转动交替受拉、受压','One surface point alternates tension and compression'),ha='center',fontsize=10);ax[0].text(5,.4,tr('Wöhler：1858–1870年的系统试验','Wöhler: systematic tests, 1858–1870'),ha='center',fontsize=10);ax[0].set_title(tr('a  旋转弯曲的历史问题','a  The historical rotating-bending question'),fontsize=12)
    theta=np.linspace(0,2*np.pi,250);ax[1].plot(theta/(2*np.pi),100*np.cos(theta),color=B);ax[1].axhline(0,color='#8a9ca7',ls='--');ax[1].set(xlabel=tr('一圈中的转数','Fraction of one revolution'),ylabel=tr('归一示例应力 / MPa','Illustrative stress / MPa'),title=tr('b  外力不换向，材料点仍经历循环','b  A rotating point still sees a stress cycle'));f.tight_layout();save(f,'history')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));t=np.linspace(0,2,501)
    for r,c in [(.1,B),(.5,O)]:mean=100*(1+r)/2;amp=100*(1-r)/2;ax[0].plot(t,mean+amp*np.sin(2*np.pi*t),color=c,label=f'R={r}')
    ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / MPa','Stress / MPa'),title=tr('a  相同最大应力，不同循环','a  Same maximum stress, different cycles'));ax[0].legend()
    eps=.03*np.sin(theta);sig=3*np.sin(theta)+.8*np.cos(theta);ax[1].plot(eps*100,sig,color=G);ax[1].fill(eps*100,sig,color=G,alpha=.18);ax[1].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('b  示意滞后环：每圈消耗能量','b  Illustrative hysteresis: energy lost per cycle'));ax[1].text(0,0,tr('面积有能量含义','Area has an energy meaning'),ha='center',fontsize=10);f.tight_layout();save(f,'waveform')
    f,ax=plt.subplots(1,2,figsize=(12,4.9));ss=np.linspace(75,185,180);mu=intercept-m*np.log10(ss/100);med=10**mu;lo=10**(mu+norm.ppf(.1)*sd);hi=10**(mu+norm.ppf(.9)*sd);ax[0].fill_betweenx(ss,lo,hi,color=B,alpha=.15,label=tr('拟合寿命分布10–90%分位','Fitted life distribution 10–90% quantiles'));ax[0].plot(med,ss,color=B,label=tr('包含未失效试样','Includes runouts'));ax[0].plot(10**np.polyval(ols,np.log10(ss/100)),ss,color=O,ls='--',label=tr('仅拟合失效点','Fit failures only'));ax[0].scatter(Nobs[failed],S[failed],color='#163b51',s=25)
    for nx,sy in zip(Nobs[~failed],S[~failed]):ax[0].annotate('',(nx*1.7,sy),(nx,sy),arrowprops={'arrowstyle':'->','color':G});ax[0].scatter([nx],[sy],facecolors='none',edgecolors=G,s=30)
    ax[0].set(xscale='log',xlabel=tr('观测循环数 / cycles','Observed cycles'),ylabel=tr('应力幅 / MPa','Stress amplitude / MPa'),title=tr('a  箭头表示达到停机上限仍未失效','a  Arrows mark survival to the test limit'));ax[0].legend(fontsize=8,loc='lower left')
    yy=np.linspace(4.7,7,500);pdf=norm.pdf(yy,intercept,sd);ax[1].plot(yy,pdf,color=B);ax[1].fill_between(yy,0,pdf,where=yy>=6,color=G,alpha=.3,label=tr('寿命超过10⁶的概率','Probability of life above 10⁶'));ax[1].axvline(6,color=O,ls='--');ax[1].set(xlabel='log₁₀(N)',ylabel=tr('对数寿命概率密度','Density of log life'),title=tr('b  100 MPa下的分布与删失','b  Distribution and censoring at 100 MPa'));ax[1].legend(fontsize=9);f.tight_layout();save(f,'life')
    f,ax=plt.subplots(2,2,figsize=(12,8));ax[0,0].loglog(DK,rate,'o',color=B,ms=4,label=tr('构造增长数据','Constructed growth data'));ax[0,0].loglog(DK,Cfit*DK**mp,color=O,label=f'm={mp:.3f}');ax[0,0].set(xlabel='ΔK / MPa √m',ylabel='da/dN / m cycle⁻¹',title=tr('a  Paris中段关系','a  Paris-regime relation'));ax[0,0].legend(fontsize=9)
    for start,c in [(.001,B),(.002,O)]:ns=np.linspace(0,growth_life(start),300);ax[0,1].plot(ns,growth(ns,start)*1000,color=c,label=f'a₀={start*1000:g} mm')
    ax[0,1].set(xlabel=tr('循环数','Cycles'),ylabel=tr('裂纹半长 / mm','Crack half-length / mm'),title=tr('b  从已知裂纹到规定6 mm终点','b  Known crack to a specified 6 mm endpoint'));ax[0,1].legend()
    ax[1,0].bar([0,1],damage,color=[B,O]);ax[1,0].set(xticks=[0,1],xticklabels=['125 MPa\n100,000 cycles','100 MPa\n200,000 cycles'],ylabel=tr('线性损伤份额','Linear damage fraction'),title=tr('c  Miner相加，不包含先后次序','c  Miner addition omits sequence effects'));ax[1,0].text(.5,.28,f'D={damage.sum():.4f}',ha='center')
    aa0=np.linspace(.0005,.0025,150);ax[1,1].plot(aa0*1000,[growth_life(q) for q in aa0],color=P);ax[1,1].set(xlabel=tr('初始裂纹半长 / mm','Initial crack half-length / mm'),ylabel=tr('到6 mm的循环数','Cycles to 6 mm'),title=tr('d  初始缺陷改变传播寿命','d  Initial defect changes propagation life'));f.tight_layout();save(f,'growth')
    img=plt.imread(Path(__file__).resolve().parent/'data/lin2018-fig3h.png');f,ax=plt.subplots(figsize=(12,5.3));ax.imshow(img);ax.axis('off');ax.set_title(tr('真实研究图：PVA凝胶在循环载荷下的缺口观测','Actual research figure: a PVA-gel notch under repeated loading'),loc='left',pad=18,fontsize=14);f.text(.5,.03,tr('Lin等，arXiv:1812.06403v1，图3H裁切，CC BY 4.0；保留原始标注与比例尺。','Lin et al., arXiv:1812.06403v1, cropped Fig. 3H, CC BY 4.0; original labels and scale bars retained.'),ha='center',fontsize=10);f.tight_layout(rect=[0,.06,1,1]);save(f,'published')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

读运行结果时，可以先数清楚样本，再看拟合数字。本例二十四个试样中，十五个达到失效判据，九个在一百万次循环时仍然工作。包含这九条生存信息的拟合，在一百兆帕应力幅下给出约一百零九万次的中位寿命；只拟合失效点时，对应数值约为九十二万次。这个差别来自同一批观测怎样进入计算，而不是换了一种材料。中位数意味着模型中一半试样的寿命高于这个数值，另一半低于它；它不等于每个试样都能达到的最低寿命，更不等于已经实际观察到所有试样都坚持了一百零九万次。

再把增长计算与寿命拟合分开核对。设定初始裂纹半长为一毫米时，到六毫米终点需要约三十一万一千次循环；初始半长改成两毫米后，约十五万七千次就到达同一终点。两者所用应力范围、增长系数和终点完全相同，差别只在起点。程序同时用解析积分与逐步数值求解计算这条曲线，两种结果在指定精度内一致。这样的交叉检查可以发现长度单位和积分方向错误，却没有替代实验对增长规律适用区间的判断。

若实际记录比模型曲线更早加速，应回到同步观测寻找原因。裂纹变长后剩余截面可能明显缩小，几何修正系数也可能随之改变；表面温度升高、环境吸液以及裂纹面的闭合，同样会改变驱动力或材料响应。把这些变化按循环位置标在图上，比直接给增长公式再加一个自由参数更容易看清问题。下一轮实验可以据此增加裂纹成像的时间密度、记录温度，或改用适合当前试样几何的驱动力计算。

交互区固定Paris中段系数和六毫米终点，让读者改变初始裂纹半长、应力范围与已经经历的循环数。增大应力范围时，增长曲线会更早变陡；增大初始缺陷时，到终点所需的循环数会减少。界面在规定终点停止计算，显示的是这一段传播所需的循环数和当前长度。这里没有把成核阶段、阈值区或快速失稳阶段隐藏进一个寿命数字，读者可以清楚看到模型从哪里开始、在哪里结束，以及哪些实验输入决定了它的结果。

## 交互：初始裂纹与传播循环数

固定C=10⁻¹⁰、m=3、Y=1；使用MPa、m和cycles。计算在半长6 mm处停止。

[Figure: 裂纹半长随循环数变化](https://ml-biomat.com/tutorials/experimental-methods/m04/#M04-plot)

## 把“能循环多久”变成一个完整的研究问题

选择疲劳实验时，先确定要保持的功能和失效判据。结构支架可能关注刚度与裂纹，柔性电极可能关注电阻，敷料可能关注边缘裂口和粘附保持。机械循环与功能信号同步记录，能够发现功能退化是否早于肉眼可见断裂。随后选择对应的载荷范围、平均水平、频率、波形和环境，再决定使用完整试样寿命还是已有裂纹增长路线。这样得到的循环数有具体用途，而不是一份脱离使用条件的耐久性排名。

统计比较需要多个独立试样，并尽量覆盖有信息的应力范围。所有试样都很快断裂时，可以了解高载荷区，却难以确定长寿命区；所有试样都达到停机上限时，可以说明这段观察内的生存情况，却难以确定曲线斜率。根据初步结果调整后续水平，保留未失效记录，并区分批次与个体差异，可以更有效地使用漫长的机时。显微断面、温度记录和循环曲线则帮助检查不同水平下是否出现了不同失效机制。

最终应同时展示载荷定义、失效定义、独立试样数、停机上限与未失效点，以及分析所覆盖的范围。若采用裂纹增长模型，还要给出裂纹几何、长度单位、拟合区间与传播终点。科学问题也会随结果向前推进：一次撕裂能很高而循环裂纹仍增长时，可以研究耗散机制在重复使用中如何变化；寿命离散很大时，可以检查初始缺陷与加工批次。疲劳实验的价值就在于把“反复使用后会怎样”拆成可观察的历史，而不只留下一个断开的时刻。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Deutsche Biographie — August Wöhler](https://www.deutsche-biographie.de/sfz26909.html?language=en)

   核对铁路车轴试验与1858–1870年论文时间线。

   Biographical reference; original diagram here.
2. [Instron — Dynamic fatigue testing](https://instron.com/en/resources/test-types/dynamic-test/)

   动态机架、载荷、应变测量与波形控制。

   Official technical reference; no images reused.
3. [NIST — Censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm)

   停机未失效与右删失记录的含义。

   Official statistical handbook; original example here.
4. [NIST — Maximum likelihood with censored reliability data](https://www.itl.nist.gov/div898/handbook/apr/section4/apr413.htm)

   失效标记、生存概率与寿命分布估计。

   Official statistical reference; no example data reused.
5. [JCSS — Fatigue models for metallic structures](https://www.jcss-lc.org/publications/jcsspmc/JCSS-3-12-Fatigue.pdf)

   S–N、Miner累积和长裂纹增长模型。
6. [Paris and Erdogan — A critical analysis of crack propagation laws (1963)](https://doi.org/10.1115/1.3656900)

   原始研究摘要中的规律检验与数据范围。

   Publisher indexed abstract consulted; no figures reused.
7. [Lin et al. — Anti-fatigue-fracture hydrogels](https://arxiv.org/abs/1812.06403v1)

   真实PVA缺口照片及含水状态、循环观测与检测尺度。

   CC BY 4.0, confirmed by arXiv license link. Fig. 3H cropped; attribution and change notice in data/NOTICE.txt.
