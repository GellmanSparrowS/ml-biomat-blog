# 压缩实验：柔软材料承重时发生什么

Source: https://ml-biomat.com/tutorials/experimental-methods/m02/
Language: zh-CN

从接触和侧向膨胀出发，理解软材料的非线性承载、端面约束与排液时间。

## 一块软材料，为什么有时承重、有时塌下去

把手指按在湿海绵上，刚按下去时能感到明显的反抗，停一会儿，水慢慢流出，手指又能继续向下。换成橡皮擦，同样的动作也会让它变矮，但侧面往外鼓起，几乎看不到液体离开。两种材料都可以被叫作“软”，承重的过程却很不同。研究软骨替代材料、细胞培养水凝胶或缓冲泡沫时，压缩实验要把这种触觉经验拆成可以比较的记录：施加了多大的力，试样缩短了多少，用了多长时间，以及受力时允许它向哪里变形或排水。

压缩机的基本动作很朴素。两个压板夹住试样，其中一个缓慢靠近，力传感器记录试样的反力。由这两列数据可以计算压缩刚度，但机器并不知道夹在中间的是完整圆柱、歪斜小块，还是已经失水的薄片。试样形状、压板摩擦和接触起点会一起进入曲线。实验的第一步因此是明确问题。如果要比较两种凝胶配方的初始柔软程度，就要保持尺寸、含水状态和加载速度可比；如果要评价缓冲垫在大变形下能否支撑载荷，则应关注工作应变、回弹和重复压缩后的变化，而不只取开头一小段斜率。

关节软骨把这个问题推进得更深。它由固体骨架与间隙中的水组成，承载时两者会相互作用。1980年，Mow、Kuei、Lai和Armstrong发表了关于软骨压缩蠕变与应力松弛的双相理论和实验研究。“双相”在这里指固体基质与流体两部分，提醒我们：一条随时间下降的力曲线，可能包含水流动带来的贡献。下图把这个历史上的建模转变放在压板边界条件旁边。理解材料内部有两部分还不够，还需要知道流体出口在哪里，以及固体侧面是否能自由移动。

![原创示意：自由侧向变形、端面摩擦鼓肚、刚性约束和1980年双相软骨研究所强调的固体–流体共同承载。图中形状用于比较边界，非某项实验照片。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fbccf525e25cebab95614013.svg?v=fbccf525e25c)

图 1原创示意：自由侧向变形、端面摩擦鼓肚、刚性约束和1980年双相软骨研究所强调的固体–流体共同承载。图中形状用于比较边界，非某项实验照片。

## 从压板位移到材料应变，中间隔着一个接触点

先把试样想成一枚小圆柱。原始高度是两张平整端面之间的距离，原始面积是垂直于加载方向的圆面积。压缩工程应变表示高度减少的比例：高2 mm的圆柱缩短0.2 mm，应变就是0.1，也可以显示成10%。本节把压缩量与压应力都记成正数，方便直接阅读加载曲线；这与把拉伸记为正、压缩记为负的连续介质约定只是符号选择不同。比较软件输出时先查看定义，避免把负号变化误读成材料反向受力。

$$
\varepsilon_c=\frac{H_0-H}{H_0},\qquad\lambda=\frac{H}{H_0}=1-\varepsilon_c,\qquad P=\frac{F}{A_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1953a63a6cc4d667632db12b.svg) | 压缩工程应变，无量纲，压缩取正。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f510273c694c65128635cc0b.svg) | 原始高度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 当前高度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 轴向高度比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 名义压应力，N/mm²；乘1000换算为kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 轴向压缩反力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 原始截面积，mm²。 |

H0=2 mm、H=1.8 mm给出εc=0.1、λ=0.9；力除以垂直受力方向面积得到平均名义应力。

压板刚开始移动时，试样可能还没有接触上压板。即使已经接触，表面的少量凸起也可能先被压平，然后整张端面才逐渐承载。因此，平台走过的距离不能从第一行数据起全部算作材料压缩。本例让真正的接触发生在平台闭合0.06 mm处。对2 mm高的试样，这段空行程已经相当于3%应变，足以改写整个初始斜率。把“力第一次大于零”当作接触点也不稳妥，因为传感器有基线偏移和噪声，液体表面还可能出现毛细作用。更实用的办法是保留接触前记录，估计基线，再结合曲线形状与端面图像确认接触区间。

几何测量同样需要适合软材料的工具。用卡尺夹紧凝胶，会在读数之前先把它压薄；用刀切割时，倾斜的端面会让一侧先接触，产生看似柔软的起始段。可以在浴液中用标定图像测量宽度，用平行切割工具准备端面，并记录每个试样自己的尺寸。圆柱直径进入面积时要平方，因此直径多估计5%，面积会多估计约10.25%，同一力换算出的应力就会偏低约9.3%。这种误差是整条曲线一起缩放，重复采集更多力点并不会把它平均掉。

样品高度也决定同一平台速度意味着什么。平台每分钟移动0.2 mm，对2 mm高的样品相当于每分钟10%工程应变，对4 mm高的样品则是5%。比较材料时应写出位移速度和对应应变速率，并说明是否在压缩过程中保持该速度。薄试样能减少某些失稳，却让接触误差、表面不平整和机器变形占据更大的比例；高试样减轻端面影响时，又可能倾斜或弯曲。高度与直径的选择要服务于材料和夹具条件，不能把一种硬质材料的推荐比例直接搬到易变形凝胶上。

## 侧面能不能鼓出来，决定了压缩的含义

“不可压缩”容易让人误以为材料根本压不动。它实际说的是体积变化很小，而不是形状不变。一个体积近似守恒的圆柱，高度减少20%以后，当前高度变成原来的0.8倍，面积就要增至原来的1.25倍才能装下同样体积；圆形截面的半径增加到原来的约1.118倍。压板允许端面滑动时，整个圆柱可以比较均匀地变矮变宽。把它放进刚性套筒里，阻止侧向扩张，同样的高度变化就要求更大的体积压缩或其他内部过程，测出的力自然会改变。

端面摩擦介于自由滑动与完全侧向约束之间。与压板接触的材料向外移动受到阻碍，中间区域却仍能扩张，于是侧面出现鼓肚。此时内部各处的应变和应力不再一样，简单地用力除以原始面积仍然可以得到平均名义应力，却不能把这条曲线当成均匀单轴响应。拍摄侧面轮廓有时比再增加一位小数更有帮助。润滑能改变滑动条件，但润滑剂与凝胶的相容性、是否渗入、是否在加载时被挤走，都要一起考虑。一个开始很滑的界面，并不保证全过程都保持相同摩擦状态。

$$
M=\frac{E(1-\nu)}{(1+\nu)(1-2\nu)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 横向应变完全为零时的约束压缩模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 自由单轴小变形杨氏模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 泊松比，无量纲，本比较取0≤ν<0.5。 |

各向同性线弹性、两个横向应变为零。E=60 kPa、ν=0.45给出M=227.586 kPa。侧壁额外限制横向扩张，产生侧向应力。

泊松比描述小变形时轴向变化与横向变化的联系。对于各向同性线弹性材料，自由侧向变形时的压缩模量是杨氏模量；横向应变被完全限制为零时，对应的是约束压缩模量。取杨氏模量60 kPa、泊松比0.45，后者约为227.6 kPa，已经接近前者的3.8倍。这里没有换材料，只是换了边界条件。泊松比越来越接近0.5时，理想约束模量急剧增加，反映近似体积守恒的材料越来越难在侧向封死的情况下继续缩短。式子中的极限也告诉我们，不能把0.5直接代进分母后继续当普通有限数计算。

自由压缩、约束压缩和压痕各自回答不同问题。自由压缩适合观察整体形状变化，约束压缩便于研究受限侧向变形与排液，而球形压痕主要探查接触附近的一片区域。三者都可能报告以kPa为单位的数值，但反演模型、受力体积与边界条件不同。对空间不均匀的生物组织，表面一小块的压痕模量与整体圆柱的压缩响应更有可能互相补充。选方法时先画出力和位移发生在哪里，再决定应该把哪一个数称作材料参数。

![左：各向同性线弹性材料在完全侧向约束下的模量；右：均匀恒体积圆柱压缩时的面积与半径变化。两个面板分别说明边界和几何，不是同一个泊松比随应变变化模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a8f389e4cab5e5e0d2f48975.svg?v=a8f389e4cab5)

图 2左：各向同性线弹性材料在完全侧向约束下的模量；右：均匀恒体积圆柱压缩时的面积与半径变化。两个面板分别说明边界和几何，不是同一个泊松比随应变变化模型。

## 曲线变陡，可以来自形状变化

在很小的应变范围内，许多软材料的应力可以近似随应变成正比，直线斜率给出初始模量。把这条直线一直延伸到40%压缩就未必合适。压缩过程中高度缩短、面积增大，链段与网络的变形也不断改变，曲线可以逐渐变陡。本节用不可压缩Neo-Hookean模型构造一个完全可复算的例子。这个模型用一个剪切模量控制弹性响应，允许较大形状变化，并在小变形时回到线弹性关系。它适合帮助我们分清“曲线弯曲”与“已经损伤”这两个不同判断。

$$
P=\mu(\lambda^{-2}-\lambda),\qquad E_0=3\mu,\qquad \sigma_c=\lambda P
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 名义压应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 剪切模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 当前高度/原始高度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | 小应变初始杨氏模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/23ed93a4937fe7721e1ddcf7.svg) | 当前面积上的真压应力，kPa。 |

均匀、自由侧向变形、不可压缩Neo-Hookean固体；面积A=A0/λ。μ=20、λ=0.8给出P=15.25、E0=60、σc=12.2 kPa。

把剪切模量设为20 kPa，初始杨氏模量就是60 kPa。压缩20%时，当前高度比是0.8，代入模型得到名义压应力15.25 kPa；若把初始直线直接外推，只会得到12 kPa。半径3 mm的圆柱原始面积约28.274 mm²，因此前者对应约0.431 N。这个换算中特别要留意kPa与N/mm²：1 kPa等于0.001 N/mm²。忘记这一千倍的换算，绘图程序照样会画出光滑曲线，物理量却已经完全错位。

同一个受力状态还可以报告当前面积上的真应力。均匀、体积守恒的压缩中，当前面积比原始面积大，所以真压应力反而比名义压应力小。上述20%压缩的例子给出12.2 kPa，而不是15.25 kPa。这个方向与均匀拉伸时真应力高于工程应力的情况正好相反，原因都在分母面积。程序把两条曲线放在同一张图中，保留相同的力与变形，只改变应力定义，便于看到这不是两份相互矛盾的实验结果。

拟合时，本例同时寻找剪切模量、接触位置与力基线，使预测力尽量接近构造的含噪记录。三个参数承担不同职责：模量主要控制承载水平，接触位置左右移动压缩起点，基线则整体上下移动力。保留接触前的观测能帮助识别基线，覆盖足够的应变范围能帮助区分模量与接触点。若只留下很窄的一小段曲线，多个参数组合可能给出几乎相同的拟合。此时应增加独立几何或接触证据，而不是单凭曲线重合得漂亮就接受每个参数。

![构造记录与完整拟合：接触前基线、接触点、力残差，以及同一不可压缩Neo-Hookean响应的初始切线和两种应力定义。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/da287a9665214a048bc44d79.svg?v=da287a966521)

图 3构造记录与完整拟合：接触前基线、接触点、力残差，以及同一不可压缩Neo-Hookean响应的初始切线和两种应力定义。

## 压住以后力变小，水去了哪里

含水网络被快速压缩时，水来不及立刻穿过孔隙离开，内部压力可以分担一部分外力。保持位移后，压力逐渐向排液边界释放，传感器读到的力随之下降。这个过程像一座有排水通道的蓄水区：通道越长，内部压力调整通常越慢。这里的类比只帮助理解空间迁移，真实软组织还包含网络弹性、渗透率变化、纤维方向和分子松弛。为了把一个机制讲清楚，下面规定一个一维压力扩散模型，单独研究排液距离怎样改变时间尺度。

$$
\frac{\partial p}{\partial t}=D\frac{\partial^2p}{\partial z^2},\qquad p(0,t)=p(H,t)=0,\qquad\tau_1=\frac{H^2}{\pi^2D}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 相对浴液的超额压力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从规定初态起的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 固定压力扩散系数，mm²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 层内轴向位置，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 两端排液层厚，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f59c766cfefc407124903879.svg) | 最慢空间模态的衰减时间尺度，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

一维、固定D、两端零超额压力，初始内部p=10 kPa。H=2 mm、D=0.01 mm²/s得到τ1=40.528 s；H=4 mm时162.114 s。压力曲率驱动时间变化。

模型中的薄层厚2 mm，两端与浴液相通，超额压力在两端保持为零；内部起始压力为10 kPa，压力扩散系数设为0.01 mm²/s。超额压力是相对于浴液压力多出的部分，因此边界为零并不是说那里没有绝对压力。方程表达的意思是：压力分布弯曲越明显，局部压力随时间变化越快。刚开始时，表面附近先下降，内部仍然较高；随后整个分布逐渐变平并接近零。图中的多条空间曲线把这件事展开，比单看一条总力下降曲线更容易理解“排液”发生在试样内部什么位置。

这个两端排液模型的最慢指数衰减时间尺度约为40.53 s。把厚度加倍到4 mm，其余条件不变，时间尺度变成约162.11 s，正好乘四。长度平方关系来自空间上的扩散过程，而不是把材料分子都变慢了四倍。图中用扩散系数乘时间再除以厚度平方，两个厚度的平均压力曲线便重合。做真实实验时，若改变尺寸能显著改变松弛时间，就可以据此设计后续实验，把流体迁移与主要由局部网络过程控制的松弛区分得更清楚。

平均压力的积分可理解为先把薄层切成许多等厚小片，再将各片压力相加取平均；因此它与中央位置的最高压力并不相同。

$$
\bar p(t)=\frac{1}{H}\int_0^H p(z,t)\,dz,\qquad F(t)=A_0\left[\sigma_s+\bar p(t)\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/541ba1aae0dc9ef838f71ad2.svg) | 层内平均超额压力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 层厚，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 位置，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 局部超额压力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 总压缩力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 固定承载面积，mm²；使用kPa时另乘0.001换算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb8516549f964d260f28c111.svg) | 教学模型规定的固定固体承载应力，5 kPa。 |

面积28.274 mm²，初始平均压力10 kPa时F=0.424115 N；压力消退后F=0.141372 N。固体项与压力初态独立规定，展示载荷分担。

为了把压力连到力，教学模型另外规定一个保持5 kPa的固体承载部分，再把平均超额压力加上去，乘以28.274 mm²面积。起始总力约0.424 N，压力充分消退后趋近0.141 N。这个固体项与压力初态是明确给定的，便于逐项核算载荷分担；完整软骨双相模型还会联立固体变形、流体运动与相应边界条件。尤其要看清排液方向：本例是上下两端排液，而不透水压板之间的自由圆柱往往主要从侧面排液，此时时间尺度关联的是径向路径，不能把试样高度直接塞进同一个公式。

![规定的一维两端排液模型：空间压力分布、厚度效应、无量纲时间重合及固定固体应力与压力的载荷分担。散点为加入噪声的构造力记录。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4a5472b86cdd68762f7dc95f.svg?v=4a5472b86cdd)

图 4规定的一维两端排液模型：空间压力分布、厚度效应、无量纲时间重合及固定固体应力与压力的载荷分担。散点为加入噪声的构造力记录。

## 让实验条件和材料问题对得上

对水凝胶和组织，含水状态是力学状态的一部分。试样从浴液中拿出来后，表面蒸发会改变尺寸和聚合物浓度；换成不同盐浓度的液体，又可能改变溶胀。应先在选定介质和温度下达到可重复的状态，再记录取样、平衡与测试之间的时间关系。浴液测试能减少蒸发，也会引入力传感器或夹具浸没造成的浮力、液面作用和温度漂移。空载基线应在相同浸没条件下取得，避免用空气中的归零去解释液体里的毫牛级变化。

力传感器的选择要与试样匹配。一个能压硬塑料的大量程传感器，可能无法清楚分辨软凝胶接触初期的微小力。先用尺寸和预计应力估计载荷范围，再选择分辨率与容量合适的传感器，并设置合理的位移或载荷终止条件。机器记录的采样频率也要覆盖最快的阶段。如果整个接触过程只有几帧数据，后续拟合再精细也难以找回没有记录的起点。反过来，在缓慢平衡阶段密集保存相邻点，只会得到许多高度相关的数值，并不等于增加了独立试样数量。

预压和循环预处理会改变你正在测量的对象。少量预压有助于建立稳定接触，但把预压后的高度当成原始高度，就相当于采用了新的参考状态，需要把它写清。某些网络经过第一圈大变形后会软化，泡沫孔结构也可能留下残余变形；此时第二圈与第一圈的差别本身就是材料信息。可以分别展示初次加载、后续循环和卸载后的恢复时间，避免把所有曲线混在一起平均成一条看似平滑的响应。若研究的是实际使用前经过预处理的材料，就让实验历史对应这种使用状态。

重复性要分层理解。同一试样连续压三次，能告诉我们循环效应和仪器重复性，却无法代替三个独立制备试样。来自同一组织块的多个切片，又可能比不同个体之间更相似。设计图表时保留试样层级，展示每个独立试样的曲线或提取参数，并解释误差条来自哪些对象。比较配方时，尺寸、批次、测量顺序和操作者造成的系统差异值得提前安排，而不是等到均值不同以后才猜测原因。合理的实验布局往往比增加一个复杂拟合模型更能提高结论的清晰度。

## 把接触、弹性和排液分别算清楚

下面的完整程序包含两组独立的教学记录。第一组从已知接触点和Neo-Hookean响应生成力数据，加入固定随机种子的测量噪声，再同时拟合接触位置、剪切模量与基线。输出保留平台位移、观测力、拟合力及残差，读者可以从最原始的一层重新检查。第二组从规定的一维压力模型生成时间序列，叠加固定固体载荷，并根据带噪总力估计扩散系数。两组模型分别解释大变形几何和排液时间，不把它们拼成一份声称来自真实组织的实验。

程序中的压力级数把空间分布分成不同波长的成分，短波成分消失得快，长波成分留下得久。读者第一次使用时不必先掌握级数推导，可以先核对三个容易检查的条件：两端压力始终为零，平均压力随时间下降，厚度加倍让相同衰减程度出现得更晚。起始时刻内部压力直接设为10 kPa，避免用有限项数近似一个边界突变时产生的小偏差。导出的空间数组保留位置、时刻与压力，既能重画曲线，也能检查数值与图例是否一致。

本次运行把设定为20 kPa的剪切模量恢复为约20.006 kPa，接触位置为约0.06013 mm，力残差的均方根约1.99 mN，与加入的2 mN噪声量级一致。排液记录则把设定的0.01 mm²/s恢复为约0.009996 mm²/s。这里可以比较已知输入与拟合输出，因为数据是按明确模型构造的；换成实测文件后，这种核对要由独立校准、重复试样与边界检查共同承担。残差变小并不自动回答接触是否正确，模量数值接近预期也不能替代对原始曲线和试样形状的观察。

观察试样的过程也应与数值记录同步。力突然下降并伴随可见裂口，与保持阶段平缓的排液下降有不同含义；试样向一旁滑动、压板碰到容器、界面夹住气泡，也可能改变曲线。同步图像不必复杂，但应能对应时间，并带有可信的长度标定。给事件加上标记时保留原始数据，方便之后核对。随手删掉一段“不好看”的曲线，会同时删掉判断它来自材料还是仪器的线索。对于透明凝胶，还可以从侧面观察接触面积、内部裂纹与压缩不均匀区域，把力的变化和空间变化接起来。

### 完整Python：接触反演、压缩几何与排液

运行两组独立教学模型，保存原始记录、拟合、压力场和四幅双语图。

```
"""Compression geometry, contact identification and a specified drainage model.
All numerical records are constructed teaching examples, not tissue measurements.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def nominal(e,mu=20.):
    lam=1-np.asarray(e)
    return mu*(lam**-2-lam)

def pressure_mean(t,H=2.,D=.01,p0=10.):
    t=np.asarray(t,dtype=float);n=np.arange(1,400,2,dtype=float)
    y=8*p0/np.pi**2*np.sum(np.exp(-np.outer(t.ravel(),n*n)*np.pi**2*D/H**2)/(n*n),axis=1)
    return np.where(t.ravel()==0,p0,y).reshape(t.shape)

def pressure_field(z,t,H=2.,D=.01,p0=10.):
    z=np.asarray(z);n=np.arange(1,400,2,dtype=float)
    if t==0:return np.where((z>0)&(z<H),p0,0.)
    return 4*p0/np.pi*np.sum(np.sin(np.outer(z,n)*np.pi/H)*np.exp(-n*n*np.pi**2*D*t/H**2)/n,axis=1)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1902);R=3.;H=2.;A=np.pi*R*R;u=np.linspace(-.1,.8,241);contact=.06;baseline=.0015
    model=lambda v:nominal(np.maximum(u-v[1],0)/H,v[0])*A/1000+v[2]
    force=model([20,contact,baseline])+rng.normal(0,.002,len(u))
    fit=least_squares(lambda v:model(v)-force,[18,.04,0],bounds=([1,-.05,-.02],[100,.15,.02])).x;pred=model(fit)
    t=np.linspace(0,300,301);pmean=pressure_mean(t);F=(5+pmean)*A/1000;Fobs=F+rng.normal(0,.0005,len(t))
    Dfit=float(np.exp(least_squares(lambda q:((5+pressure_mean(t,D=np.exp(q[0])))*A/1000-Fobs),[np.log(.02)]).x[0]))
    summary={'fit_mu_kPa':float(fit[0]),'fit_contact_mm':float(fit[1]),'fit_baseline_N':float(fit[2]),'residual_rms_mN':float(np.sqrt(np.mean((pred-force)**2))*1000),'nominal_at_20pct_kPa':float(nominal(.2)),'true_at_20pct_kPa':float(.8*nominal(.2)),'force_at_20pct_N':float(nominal(.2)*A/1000),'free_modulus_kPa':60.,'confined_modulus_nu045_kPa':60*.55/(1.45*.1),'tau_H2_s':4/(np.pi**2*.01),'tau_H4_s':16/(np.pi**2*.01),'fit_diffusivity_mm2_s':Dfit,'initial_force_N':float(15*A/1000),'equilibrium_force_N':float(5*A/1000),'mean_pressure_40s_kPa':float(pressure_mean(40.))}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[u,force,pred,force-pred],delimiter=',',header='stage_closure_mm,observed_force_N,fitted_force_N,residual_N',comments='');np.savetxt(o/'drainage.csv',np.c_[t,pmean,F,Fobs],delimiter=',',header='time_s,mean_excess_pressure_kPa,model_force_N,observed_force_N',comments='')
    z=np.linspace(0,H,201);times=np.array([0,2,10,40,100,300]);fields=np.array([pressure_field(z,tt) for tt in times]);np.savez(o/'pressure_fields.npz',z_mm=z,time_s=times,pressure_kPa=fields)
    f,ax=plt.subplots(2,2,figsize=(12,8));labels=[tr('a  自由侧向膨胀','a  Free lateral expansion'),tr('b  端面摩擦与鼓肚','b  End friction and barrelling'),tr('c  刚性侧壁约束','c  Rigid lateral confinement'),tr('d  1980：固体网络与流体共同承载','d  1980: solid network and fluid support')]
    for i,x in enumerate(ax.flat):
        x.set(xlim=(0,10),ylim=(0,7));x.axis('off');x.set_title(labels[i],loc='left',fontweight='bold',fontsize=12)
        if i<3:
            for yy in [1,5]:x.add_patch(Rectangle((1,yy),8,.45,facecolor='#8b9ca7'))
            if i==1:
                yy=np.linspace(1.45,5,80);left=3-.8*np.sin(np.pi*(yy-1.45)/3.55);right=7+.8*np.sin(np.pi*(yy-1.45)/3.55);x.fill(np.r_[left,right[::-1]],np.r_[yy,yy[::-1]],color=G,alpha=.28);x.plot(left,yy,color=G);x.plot(right,yy,color=G)
            else:x.add_patch(Rectangle((2.7 if i==0 else 3,1.45),4.6 if i==0 else 4,3.55,facecolor='#d0e9e4',edgecolor=G,lw=2))
            if i==2:
                for xx in [2.5,7]:x.add_patch(Rectangle((xx,1),.5,4.4,facecolor='#526b7a'))
            x.annotate('',(5,5.5),(5,6.6),arrowprops={'arrowstyle':'->','color':O,'lw':2})
            x.text(5,.3,[tr('侧面自由；端面滑动','Free sides; sliding ends'),tr('端部受阻；中部更宽','Restrained ends; wider middle'),tr('横向应变为零','Zero lateral strain')][i],ha='center')
        else:
            for xx in np.linspace(2,8,5):x.plot([xx,xx],[1.7,5.3],color=G,lw=2)
            for yy in np.linspace(1.7,5.3,4):x.plot([2,8],[yy,yy],color=G,lw=2)
            for xx in np.linspace(2.6,7.4,4):
                for yy in [2.3,3.5,4.7]:x.scatter(xx,yy,s=70,color=B,alpha=.55)
            x.annotate('',(8.9,3.5),(7.8,3.5),arrowprops={'arrowstyle':'->','color':B,'lw':2});x.text(5,.5,tr('Mow、Kuei、Lai、Armstrong：双相力学','Mow, Kuei, Lai, Armstrong: biphasic mechanics'),ha='center',fontsize=10)
    f.tight_layout();save(f,'geometry')
    f,ax=plt.subplots(2,2,figsize=(12,8));ax[0,0].scatter(u,force,s=9,color=B,alpha=.55,label=tr('构造观测','Constructed observations'));ax[0,0].plot(u,pred,color=O,label=tr('接触点与材料联合拟合','Joint contact/material fit'));ax[0,0].axvline(contact,color=G,ls='--');ax[0,0].set(xlabel=tr('平台闭合位移 / mm','Stage closure / mm'),ylabel=tr('力 / N','Force / N'),title=tr('a  先找到接触，再计算压缩','a  Find contact before compression'));ax[0,0].legend(fontsize=9)
    ax[0,1].scatter(u,(force-pred)*1000,s=9,color=B);ax[0,1].axhline(0,color='#82939c');ax[0,1].set(xlabel=tr('平台闭合位移 / mm','Stage closure / mm'),ylabel=tr('残差 / mN','Residual / mN'),title=tr('b  剩下的是怎样的误差','b  What remains after fitting'))
    e=np.linspace(0,.4,201);ax[1,0].plot(e*100,nominal(e),color=B,label='Neo-Hookean');ax[1,0].plot(e*100,60*e,color=G,ls='--',label=tr('初始切线 E₀=60 kPa','Initial tangent E₀=60 kPa'));ax[1,0].scatter([20],[15.25],color=O);ax[1,0].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('名义压应力 / kPa','Nominal compression stress / kPa'),title=tr('c  弯曲曲线仍可完全弹性','c  A curved response can be elastic'));ax[1,0].legend(fontsize=9)
    ax[1,1].plot(e*100,nominal(e),label=tr('原始面积','Original area'),color=B);ax[1,1].plot(e*100,(1-e)*nominal(e),label=tr('当前面积','Current area'),color=O);ax[1,1].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('压应力 / kPa','Compression stress / kPa'),title=tr('d  分母面积改变数值','d  Area definition changes the value'));ax[1,1].legend();f.tight_layout();save(f,'contact')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));nu=np.linspace(0,.49,200);M=60*(1-nu)/((1+nu)*(1-2*nu));ax[0].plot(nu,M,color=P);ax[0].axhline(60,color=G,ls='--',label=tr('自由压缩 E=60 kPa','Free compression E=60 kPa'));ax[0].scatter([.45],[60*.55/(1.45*.1)],color=O);ax[0].set(xlabel=tr('泊松比 ν','Poisson ratio ν'),ylabel=tr('约束压缩模量 / kPa','Constrained modulus / kPa'),title=tr('a  同一材料，不同侧向约束','a  Same material, different constraint'));ax[0].legend()
    ax[1].plot(e*100,1/(1-e),color=B,label=tr('面积 / 原始面积','Area / original area'));ax[1].plot(e*100,1/np.sqrt(1-e),color=O,label=tr('半径 / 原始半径','Radius / original radius'));ax[1].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('几何比值','Geometric ratio'),title=tr('b  不可压缩指体积守恒','b  Incompressible means constant volume'));ax[1].legend();f.tight_layout();save(f,'constraint')
    f,ax=plt.subplots(2,2,figsize=(12,8));colors=plt.cm.viridis(np.linspace(.05,.85,5))
    for tt,c in zip([2,10,40,100,300],colors):ax[0,0].plot(z,pressure_field(z,tt),color=c,label=f'{tt} s')
    ax[0,0].set(xlabel=tr('层内位置 / mm','Position in layer / mm'),ylabel=tr('超额压力 / kPa','Excess pressure / kPa'),title=tr('a  两端排液的压力分布','a  Pressure with two drained faces'));ax[0,0].legend(ncol=2,fontsize=9)
    for hh,c in [(2,B),(4,O)]:ax[0,1].plot(t,pressure_mean(t,H=hh),color=c,label=f'H={hh} mm')
    ax[0,1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('平均超额压力 / kPa','Mean excess pressure / kPa'),title=tr('b  厚度翻倍，时间尺度乘四','b  Double thickness, four times the scale'));ax[0,1].legend()
    for hh,c,st in [(2,B,'-'),(4,O,'--')]:ax[1,0].plot(t*.01/hh**2,pressure_mean(t,H=hh)/10,color=c,ls=st,label=f'H={hh} mm')
    ax[1,0].set(xlim=(0,.5),xlabel='Dt / H²',ylabel=tr('平均压力 / 初始压力','Mean / initial pressure'),title=tr('c  用排液长度归一化','c  Scale time by drainage length'));ax[1,0].legend()
    ax[1,1].fill_between(t,0,np.full_like(t,5*A/1000),color=G,alpha=.35,label=tr('指定固体部分','Specified solid contribution'));ax[1,1].fill_between(t,5*A/1000,F,color=B,alpha=.3,label=tr('压力部分','Pressure contribution'));ax[1,1].plot(t,F,color=B);ax[1,1].scatter(t[::10],Fobs[::10],s=12,color=O,label=tr('构造观测','Constructed observations'));ax[1,1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('合力 / N','Total force / N'),title=tr('d  一个明确规定的载荷分担模型','d  A specified load-sharing model'));ax[1,1].legend(fontsize=9);f.tight_layout();save(f,'drainage')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

交互区让厚度、扩散系数和观察时刻各自独立变化。先固定扩散系数，把厚度从2 mm调到4 mm，再寻找相同平均压力出现的时间；随后恢复厚度，只改变扩散系数，比较两种操作怎样改变曲线。颜色条展示当前层内压力，折线展示平均压力的时间过程，数值同时给出对应合力。初始压力、面积和固体项保持不变，因此这些对照只检验排液长度与迁移速率，不会偷偷混入更换材料强度或试样面积的影响。

## 交互：排液路径与时间

两端排液；初始压力10 kPa、固体项5 kPa、半径3 mm。改变厚度，观察相同压力衰减需要多久。

[Figure: 平均压力时间曲线和当前空间分布](https://ml-biomat.com/tutorials/experimental-methods/m02/#M02-plot)

## 从一条压缩曲线走向可解释的材料比较

如果两份凝胶的初始斜率不同，先沿着数据产生的链条寻找原因：它们是否有相同含水状态，接触点是否可靠，尺寸是否逐个测量，端面滑动是否一致，以及采用了哪个拟合区间。曲线只在大应变处分开时，可以进一步比较工作应力、卸载恢复与侧面形状；力在保持阶段的下降不同，则应把加载时长、排液路径和试样尺寸放在同一张记录表中。这样，每一种曲线差异都有相应的物理问题和补充观察，而不是全部被压缩进一个“更硬”的形容词。

压缩还常常与显微观察、吸水测量和组织结构分析一起工作。孔隙在受压时闭合，可以改变应力曲线；纤维取向会让不同方向表现不同；溶胀程度改变后，网络浓度和原始尺寸也一起变化。把加载方向标在取样图上，把测试前后的形貌与同一试样对应起来，可以让力学参数回到材料结构中。对于需要承受日常反复载荷的支架，单次压缩给出初始响应，后续的循环、疲劳与恢复实验则回答它在使用过程中如何演化。

一个完整的压缩结果应让读者重建受力场景：试样是什么形状，参考高度和面积怎样取得，压板怎样接触，侧面和液体能否移动，加载和等待各持续多久，最终提取的是初始切线、某一应变下的割线、工作应力还是平衡响应。把这些定义与曲线放在一起，数值便有了清楚的用途。软材料承重并不是一个固定常数在起作用，而是材料、几何、边界和时间共同形成的过程；压缩实验的价值，就在于把这些因素逐个变成能够观察、改变和计算的对象。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Mow et al. — Biphasic creep and stress relaxation (1980)](https://pubmed.ncbi.nlm.nih.gov/7382457/)

   核实1980年双相软骨压缩研究的作者、题目与日期。
2. [CellScale — Compression testing methods for soft materials and biomaterials](https://cellscale.com/applications/testing-methods/compression/)

   圆柱、球体与压痕的几何和低力测量实例。

   Copyright CellScale; technical reading only, no data or figures reused.
3. [DoITPoMS — Compression, friction and barrelling](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.7:_Compression_Testing_-_Practical_Basics_Friction_and_Barrelling)

   端面摩擦、鼓肚和均匀应力假设。

   CC BY-NC-SA reference consulted; no figures or text adapted.
4. [Lakes — Meaning of Poisson ratio](https://lakeslab.ep.wisc.edu/PoissonIntro2.html)

   自由与完全约束压缩模量的关系。

   University teaching reference; original derivation and diagrams here.
5. [Sandia LAMÉ manual — Neo-Hookean model](https://www.sandia.gov/files/sierra/SM_LAME_5_24/main/models/neo_hookean.html)

   有限变形弹性、单轴应力与小应变极限。

   Official technical reference; no figures reused.
