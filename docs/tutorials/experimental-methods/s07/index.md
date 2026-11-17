# X射线光电子能谱：读懂材料最外层

Source: https://ml-biomat.com/tutorials/experimental-methods/s07/
Language: zh-CN

从一滴水的铺展出发，读懂电子能量、表面深度、元素比例和化学环境。

## 一滴水为什么突然愿意铺开

同一片塑料，处理前滴上一滴水，水像小珠子一样缩成一团；经过等离子体处理后，水却铺得更开。称一称，两片材料几乎一样重；用手弯折，硬度也没有明显改变。变化可能集中在最外面的几纳米。这个厚度远小于一根头发的直径，却正是水、蛋白质、细胞和胶黏剂最先接触的位置。研究者想知道的事情很具体：表面是不是多了氧，氧与哪些原子连接，改变持续了多久，清洗以后还在不在？X 射线光电子能谱，简称 XPS，就是从这些表面原子发出的电子中读取化学信息的方法。

可以把材料想成一本很厚的书。称重得到整本书的质量，许多体相检测更像统计整本书的内容，XPS 则特别关注封面及附近的几页。封面换了一种涂层，整本书的重量未必明显变化，读者摸到的触感却已经不同。这个比喻帮助我们确定问题所在，但真实的 XPS 并没有一条整齐的“只读到第十页”的边界。越靠近外表面的原子通常贡献越大，深处的贡献逐渐减弱；所谓探测深度，是针对这种连续权重定义的尺度。

在生物材料研究中，XPS 常用于比较蛋白质吸附前后的氮信号、检验聚合物表面的含氧基团，或研究植入物表面的氧化层。在普通材料研究中，同样的思路用于胶接、涂层、腐蚀、催化剂和电子器件。问题应写成可观察的变化，例如“清洗后表面氮原子比例是否仍然提高”，而不是一句笼统的“测一下表面”。前一种问法会自然带出未处理样品、清洗对照和重复试样，也能帮助决定先扫哪些能量区域、是否需要改变测量角度。

读完本章，应能把一张横轴为结合能的图连接到三个不同层次的结论：有哪些可检测元素，各元素在检测范围内的相对比例如何，同一元素的电子环境是否发生变化。这三个层次对应不同的采集和分析步骤。元素比例、碳化学环境比例和涂层厚度虽然都可能由峰面积计算，却各自采用不同的分母与物理模型；先说清正在回答哪个问题，计算才有明确对象。

## 把电子带走，要付出多少能量

原子中的电子受到原子核和其他电子共同作用。要把一个原来处于束缚状态的电子带离，需要提供能量。XPS 用已知能量的 X 射线光子照射样品，其中一些光子把能量交给电子，电子随后逸出。仪器直接分析的是逸出电子的动能，也就是与运动相关的能量。既然入射光子的能量已知，把电子离开以后仍然带着的动能扣除，再处理仪器的能量参照，就能求出对应的结合能。它像一笔有明确收入和支出的账：光子提供预算，摆脱束缚消耗一部分，余下的表现为电子运动。

能谱常用电子伏特，写作 eV。它是能量单位，表示一个基本电荷通过一伏电势差所对应的能量；这里不需要先把所有数字换成极小的焦耳数，便可直接比较不同电子的能量。常用铝靶 Kα X 射线的光子能量约为 1486.6 eV。下面的例子选取一个结合能 284.8 eV 的教学峰，并把分析器功函数取为 4.5 eV，算得动能 1197.3 eV。功函数与能量零点有关，经过校准的仪器会处理这部分关系；实际使用已经输出的结合能轴时，应沿用仪器记录的校准和参照，避免再手动减一次。

$$
E_B=h\nu-E_K-\Phi_{\mathrm{an}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dfd1267e50e10bbc94160d9b.svg) | 结合能，eV；以适当校准的费米能级为参照。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 普朗克常数，eV·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 入射光频率，s⁻¹；hν 为光子能量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d70c8f0e877cac0363c29de.svg) | 分析器测得电子动能，eV。 |
| ![Formula](https://ml-biomat.com/static/agent-math/83bfd7d1a50c8bb908a1db0d.svg) | 分析器功函数，eV。 |

能量守恒连接已知光子能量与测得动能。hν=1486.6 eV、EB=284.8 eV、Φan=4.5 eV，得到 EK=1197.3 eV。绝缘样品还需适当控制充电与参照；仪器已经校准的结合能轴按记录直接使用。

这段历史的关键并非只在于发现电子可以离开物质，而在于把电子能量测得足够精细。凯·西格巴恩在 1981 年诺贝尔演讲中回顾了自己从电子聚焦和能量分辨率研究走向电子能谱的过程。不同化学环境造成的细小位移，只有在仪器能够分开邻近能量时才变得可见；电子能谱因此进入化学分析，形成 ESCA，也就是“化学分析用电子能谱”这一名称。图中的装置关系将光源、样品、电子运动和能量分析连接起来：原子环境改变一小段能量，仪器把它变成可以比较的谱峰位置。

C 1s、O 1s 这样的标签由元素符号与电子轨道名称组成。C 表示碳，1s 表示参与发射的内层电子状态，并不是“第一个碳峰”。一个元素可以拥有多种可测轨道，某些轨道还会出现自旋与轨道运动耦合造成的成对谱线。同一个化学状态就可能有两个峰，因此判断化学种类时不能把曲线上每一个鼓包都当作一种新物质。含氧碳与只连碳、氢的碳通常处于不同电子环境，C 1s 峰会出现不同贡献；对于金属氧化物，还需结合多重态、卫星峰以及电子发射后其他电子的响应理解谱形。

![原创光电子示意与能量账本。深度曲线采用 L=2.5 nm 的指数模型，面积归一为 1；角度从表面法线起算。右图的功函数与结合能是教学值，三项相加为 1486.6 eV。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4856771c7e1a91653c78eef4.svg?v=4856771c7e1a)

图 1原创光电子示意与能量账本。深度曲线采用 L=2.5 nm 的指数模型，面积归一为 1；角度从表面法线起算。右图的功函数与结合能是教学值，三项相加为 1486.6 eV。

## 为什么照进去很深，读出来却很浅

X 射线能够进入样品内部相当深的位置，但产生的电子要穿过周围物质才能到达表面。沿途如果发生非弹性碰撞，电子会把部分能量交给材料，抵达探测器时就不再保留原来那条特征峰的能量。它们可能进入背景，或者根本没有逃出样品。于是，来自深处的完整特征信号比来自浅处的信号弱得多。决定 XPS 表面敏感性的关键是电子的逃逸过程，而不是简单地把 X 射线的穿透距离叫作测量深度。

先考虑一个平整、均匀的样品，并把电子沿路保持特征能量的概率近似写成指数衰减。若每前进相同距离都有相同比例的电子损失，那么剩余比例会不断相乘，最后得到指数函数。有效衰减长度 L 用来概括特定材料、电子能量与测量几何下的衰减；它与非弹性平均自由程有关，但还包含所采用应用模型中的弹性散射修正。一个长度值应与对应电子及分析用途一起使用，例如基底电子穿过覆盖层时，应选取这些电子在覆盖层中的相关长度。

$$
w(z,\theta)=\frac{\exp[-z/(L\cos\theta)]}{L\cos\theta}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a7d43466111bfe7c3c78ee.svg) | 归一化深度信号密度，nm⁻¹；从 0 到无穷深度积分为 1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 沿表面法线量取的深度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 该电子、材料与应用模型的有效衰减长度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 相对表面法线的发射角；三角函数计算使用弧度。 |

平整均匀样品的指数衰减近似：电子路径为 z/cosθ，归一化因子保证总贡献为 1。L=2.5 nm、θ=0、z=2.5 nm 时 w≈0.14715 nm⁻¹。实际弹性散射和粗糙形貌需采用相应模型。

角度也能改变看到的深浅。这里把发射角定义为电子方向与表面法线的夹角，法线就是垂直于表面的方向。垂直出射时，电子从深度 z 到表面走的路最短；向旁边倾斜后，同样深度要走更长的路，损失也更多。因而大角度检测会更偏重最表层。不同仪器有时从表面平面起算角度，阅读记录时应先看清定义。若把这两种定义混在一起，正弦与余弦会对调，厚度计算也会随之改变。

我们用“包含总特征信号 95% 的深度”描述一个具体探测范围。它并非最深电子的来源，而是把由表及里的贡献累加到 95% 时达到的位置。取 L=2.5 nm，沿法线检测得到约 7.49 nm；倾斜到 60° 时得到约 3.74 nm。最深的少量贡献仍然存在。这样理解后，“XPS 看几纳米”就成为可以讨论条件的陈述：电子能量、材料、表面形貌和几何改变，这个尺度也会改变。

$$
d_{95}=-L\cos\theta\ln(0.05)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5566087c3ff7062424a56fdd.svg) | 包含特征信号 95% 的深度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 有效衰减长度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 相对表面法线的发射角。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85eb3227c042f8ec4de535b2.svg) | 来自更深处的剩余信号比例，无量纲。 |

把归一化深度密度从表面积分至 d95，令累计贡献为 0.95。L=2.5 nm 时，法线方向 d95=7.48933 nm；60° 时为 3.74467 nm。ln 为自然对数，0.05 是信号比例。

覆盖层厚度可以用基底信号衰减来估计。先测裸基底的某条峰，再用相同条件测覆盖后的同一条峰，比较二者面积。均匀覆盖层越厚，保留下来的基底信号越少。在 L=2.5 nm 的模型中，2 nm 薄膜使法线方向的基底峰降到裸基底的约 44.9%，而在 60° 方向降到约 20.2%。把这个实验做成角度系列，就能检验信号变化是否符合均匀覆膜的预期。粗糙表面、孔洞和岛状覆盖会让不同位置的路径不一样，此时研究问题要改成覆盖率或结构分布，并选取相应的几何模型。

$$
r=\frac{I_{\mathrm{sub}}}{I_{\mathrm{bare}}}=\exp\!\left(-\frac{d}{L\cos\theta}\right),\qquad d=-L\cos\theta\ln r
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 覆盖后与裸基底峰面积之比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d414a7153e40c5c4b33cda1.svg) | 相同条件下覆盖后与裸基底的同一谱线净面积，单位相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 均匀覆盖层厚度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 基底电子在覆盖层中相应用途的衰减长度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 相对表面法线的发射角。 |

连续平整覆盖层、匹配采集与稳定基底条件下，用沿程损失解释基底信号变化。d=2 nm、L=2.5 nm、θ=0 时 r=0.449329；θ=60° 时 r=0.201897。反演厚度要求 0<r≤1。

## 改变观看角度，表面会显得多厚

厚度、角度与衰减长度共同决定基底峰能保留多少。图中深度贡献归一为 1；角度从表面法线量起。

[Figure: 覆盖层与信号深度交互图](https://ml-biomat.com/tutorials/experimental-methods/s07/#S07-plot)

## 真正的样品从哪里开始变得复杂

一片刚刚制成的薄膜，在包装、运输、镊子夹持、清洗和晾干中，外表面都可能发生变化。XPS 对几纳米内的成分很敏感，手指留下的有机物、清洗液中的盐、胶带转移的硅氧烷，也会成为可见信号。开始实验时，先确定究竟研究“制备完成后的表面”“经过清洗的表面”，还是“在溶液里使用后的表面”。这三个对象都值得研究，但它们不必具有相同组成。给样品规定一致的暴露、清洗与保存过程，是把表面状态固定下来的实验步骤。

常规 XPS 在高真空或超高真空环境中工作，一方面减少飞行电子与气体分子的碰撞，另一方面减缓残余气体覆盖样品表面。干燥聚合物与金属片较容易安排；含水凝胶、活细胞和挥发性样品需要专门考虑真空中的失水与结构变化。假如问题关乎水凝胶在水中的最外层，干燥后的表面化学与湿态界面应分别表述。冷冻转移、低温测量或近常压装置各有适合的条件，选择取决于要保留哪种状态，以及设备怎样实现电子传输和环境控制。

绝缘材料还有一个常见问题：电子离开后，局部积累正电，后来逸出的电子受到额外电势影响，测得动能降低，换算出的表观结合能升高。整体均匀带电时，各峰可能一起移动；不同区域的导电性、厚度或电接触不同，就会出现差分充电，谱峰被拉宽甚至变成多个肩部。电荷中和装置用低能电子等方式补偿表面电荷，样品固定与电接触同样重要。把某个碳峰全部移动到 284.8 eV 只能施加一个整体数值偏移，无法修复各区域移动量不同造成的谱形变化。

因此，能量参照要和样品化学一起考虑：所选参照峰属于什么物质，是否确实存在，是否在处理前后保持相同环境？对于富含官能团的聚合物，最高的碳峰未必就是可以任意固定的“污染碳”。先查看中和条件是否稳定、重复扫描是否整体漂移，再依据合适的参照和已知物质比较峰位，会比事后把每张图移到看起来一致的位置更有解释力。需要使用数值修正时，保留修正量和依据，便于把谱图与材料状态对应起来。

采集通常先做覆盖较大结合能范围的全谱，再对感兴趣元素做精细扫描。全谱回答是否存在碳、氧、氮或意外杂质；精细扫描回答某个峰内是否有可分辨的不同贡献。分析器通能决定电子通过分析器时的能量尺度，通常需要在计数效率与能量分辨率之间选择。较小步长会让横轴采样更密，却不会自动改善光源和分析器造成的实际展宽。若样品会被 X 射线照射改变，可以在同一区域重复短扫描，检查峰形和组成随时间的变化，再选择总剂量与测量位置。照射区域的大小也会影响结论：一条窄涂层与旁边裸露的基底可能同时进入检测范围。把光斑与样品特征尺寸比较，再测量几个位置，能够区分局部化学变化、覆盖不完整与不同结构平均后的组成。

## 峰有多大，先问它对什么敏感

全谱中氧峰比碳峰高，并不意味着氧原子一定比碳原子多。不同轨道吸收光子并发射电子的概率不同，电子在材料中的损失、分析器的传输效率也随能量变化。比较元素时，需要先对积分面积进行灵敏度校正。积分面积是峰相对于背景的总信号，把横轴每一小段的宽度乘上该处的信号，再加起来；它保留了峰宽变化时仍应计入的电子数，比只取最高点更适合定量。

相对灵敏度因子，简称 RSF，承担把不同元素响应换到可比尺度上的作用。它应与仪器、光源、分析模式以及选取的谱线一致。下面为了看清计算，给碳、氮、氧设置面积 5000、1200、9000，并采用教学因子 1.0、1.8、3.0。氧的原始面积占比约 59.2%，经校正后，三个相对量变为 5000、666.7、3000，氧的比例约为 34.6%。这些因子用来演示运算，实际样品应使用经过核对的仪器数据或参考材料确定的响应。

$$
x_i=\frac{A_i/S_i}{\sum_j A_j/S_j}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | 第 i 元素在所纳入可检测元素中的等效均匀原子分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/081841f943a2910bf49ac5b3.svg) | 扣除相应背景后的谱线净面积，所有元素采用一致计数与能量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6398be9a730b07210cb4c69e.svg) | 与光源、谱线和采集模式匹配的相对灵敏度因子，共同比例尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 元素编号；求和包括全部纳入定量的元素。 |

先把面积除以响应因子，再将可比信号归一化。面积 C/N/O=5000/1200/9000，教学因子=1/1.8/3 时，氧分数=0.346154，乘 100 得 34.6154 at.%。分层样品的结果带有表面权重，氢通常不在该分母内。

这个百分比的分母是被纳入分析、具有可用峰信号的元素总量。常规 XPS 的元素分析通常不直接计入氢和氦，因此“碳占 60 at.%”不能自动理解成材料全部原子中有 60% 是碳。若样品在探测范围内存在明显分层，按均匀模型得到的数值应理解为带有表面权重的等效组成。比如一层很薄的富氧膜覆盖在碳基底上，测得氧比例既与覆盖层的化学组成有关，也与膜厚、基底贡献和检测角度有关。

![构造全谱与灵敏度校正。峰位用于元素区域示意，所列 RSF 为教学因子。相同峰面积在校正前后给出不同百分比；校正后氧占所纳入元素的约 34.6%。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3219f567e94e6cfd782a35ea.svg?v=3219f567e94e)

图 2构造全谱与灵敏度校正。峰位用于元素区域示意，所列 RSF 为教学因子。相同峰面积在校正前后给出不同百分比；校正后氧占所纳入元素的约 34.6%。

比较处理前后的数据时，除了平均值，还要问平均了什么。一个位置连续扫三次，主要反映该位置的计数波动、稳定性与照射过程；同一块样品测三个位置，可以发现横向不均匀；独立制备三块样品，则更接近制备过程的重复性。图中最后一个面板采用明确构造的三块试样数值，用散点保留每个样品，再显示均值和样本标准差。误差线因此有清楚的对象，读者能够区分“这块样品测得稳定”和“这个制备方法得到的材料稳定”。

同一元素内部的化学环境比例使用另一种分母。若 C 1s 被合理分为几种碳环境，它们来自相同轨道，某个分量面积除以总 C 1s 面积，可以描述检测范围内该类碳环境的加权比例。它与氧元素的原子百分比不是同一个量：一个羧基含一个羧基碳和两个氧，而一个醚氧可能连接两个碳；仅凭一个含氧碳分量的面积，无法直接按一对一关系换成氧原子数。将元素组成和化学环境分析一起比较，反而能够检查所提化学模型是否协调。

## 分峰是一项化学解释，不是绘画比赛

一条宽峰可以由多个环境共同贡献，也可能受到仪器展宽、无序结构、卫星过程或充电影响。分峰就是为这些贡献建立模型，再问模型能否解释观测数据。开始之前，应先根据分子结构、处理反应、参考物质和其他谱区提出候选。假如研究一片含酯基的聚合物，碳骨架、连接氧的碳以及羰基相关环境可以成为有化学依据的起点；如果每遇到一个小起伏就加一条峰，模型虽然更贴近噪声，化学解释却会越来越随意。

背景是这个问题的一部分。非弹性损失产生的电子会构成随能量变化的连续信号，简单直线有时只适用于很窄、变化平缓的局部范围。Shirley 与 Tougaard 背景采用不同的物理或经验关系，适合的选择要结合谱形、能量窗口和分析目的。背景终点选在哪里、是否包含邻近峰，都会影响最后面积。把扣背景后的曲线单独保存，并查看背景在峰两侧是否合理，比只保留软件输出的一行百分数更容易发现问题。

本章程序构造三个位置已知、面积分别为 6500、2200、1300 的高斯分量，加上线性背景，再按设定计数时间加入泊松噪声。高斯线形与线性背景在这里是完整声明的教学条件，用来让读者知道正确答案和误差来源。程序同时拟合分量面积、共同宽度和背景参数，并与只放两个分量的模型比较。它没有从一张未知材料谱中自动发现三个官能团，而是在已知条件下检验“漏掉一个真实贡献”会留下怎样的残差。

![构造 C 1s 区域，三个真实教学面积为 6500、2200、1300 counts·s⁻¹·eV；共同高斯宽度 σ=0.48 eV，逐点计数时间 0.4 s。上图为观测与拟合，下图为观测减拟合的残差；两个分量模型遗漏一个已知贡献。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0a73f21c61cbff3c7998cbb2.svg?v=0a73f21c61cb)

图 3构造 C 1s 区域，三个真实教学面积为 6500、2200、1300 counts·s⁻¹·eV；共同高斯宽度 σ=0.48 eV，逐点计数时间 0.4 s。上图为观测与拟合，下图为观测减拟合的残差；两个分量模型遗漏一个已知贡献。

残差是每个能量点的观测值减去模型值。三个分量模型的残差主要围绕零起伏，两个分量模型则在遗漏贡献附近留下连贯的结构。连贯残差提示模型中仍有未解释的信息，但下一步既可以检查化学组分，也可以检查背景、充电和峰形。实际分析中，不同峰的位置差、宽度、双峰面积比等约束应来自相应物理关系；把参数任意放开，通常会产生多个外观近似却含义不同的解。对于具有复杂多重态的过渡金属谱区，先研究合适参考谱与专门模型，会比直接套用本章的高斯组合更有效。

不确定度也应沿着推理链理解。增加计数时间能减小相对计数波动，拟合会更稳定；它不会自动确定正确的背景形式或能量参照。可以把同一数据在几组合理背景终点、峰宽约束下重新分析，观察目标比例改变多少，再与独立样品的变化比较。若处理前后差别比这些分析选择造成的变化还小，应优先改善样品设计和测量条件，让需要回答的化学差异进入清楚可辨的范围。这样安排实验，得到的是更有分辨力的证据，而不仅是更多小数位。

### 从表面权重到峰拟合的完整 XPS 教学实验

构造数据均在脚本中定义，固定随机种子输出四组图、原始与处理后的表格以及数值摘要。

```
"""Constructed XPS experiments: surface weighting, composition and peak models."""
from pathlib import Path
import argparse, json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Arc

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';T=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
        'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold',
        'axes.labelcolor':'#243c49','text.color':'#243c49','axes.edgecolor':'#8da0a6',
        'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','svg.fonttype':'path'})
    blue,green,red,gold='#286488','#008b7b','#dc604d','#c39227'
    def save(fig,name):
        fig.tight_layout(pad=1.6)
        for ext in ['svg','png']:fig.savefig(out/f'{name}-{args.language}.{ext}',dpi=155,bbox_inches='tight')
        plt.close(fig)
    def gaussian(x,mu,sigma):return np.exp(-.5*((x-mu)/sigma)**2)/(sigma*np.sqrt(2*np.pi))

    fig,ax=plt.subplots(1,3,figsize=(14,4.8),gridspec_kw={'width_ratios':[1.1,1,1]})
    a=ax[0];a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    a.add_patch(Rectangle((.5,.5),9,3.8,color='#dbe5e7'));a.plot([.5,9.5],[4.3,4.3],color=blue,lw=2)
    a.annotate(T('X 射线','X-rays'),xy=(4.3,4.2),xytext=(.6,8.8),arrowprops={'arrowstyle':'->','color':gold,'lw':3},fontsize=13)
    a.add_patch(FancyArrowPatch((4.4,3.8),(7.1,8.3),arrowstyle='->',mutation_scale=15,color=green,lw=3))
    a.text(7.5,7.5,T('电子\n至分析器','Electron\nto analyzer'),fontsize=9,ha='left')
    a.plot([4.4,4.4],[3.8,9],ls=':',color='#7b929a');a.text(4.4,9.4,T('表面法线','Surface normal'),fontsize=10,ha='center')
    a.add_patch(Arc((4.4,3.8),4,4,theta1=58,theta2=90,color=blue));a.text(4.8,6.1,r'$\theta$')
    a.plot([2,2.7,2.2,3.1],[1.5,2.3,2.9,3.6],color=red,lw=2);a.text(.8,.8,T('碰撞损能 → 背景','Energy loss → background'),fontsize=10)
    a.set_title(T('A  从光子到电子','A  From photon to electron'),loc='left')
    z=np.linspace(0,15,400);L=2.5
    for angle,c in [(0,green),(60,blue)]:
        weight=np.exp(-z/(L*np.cos(np.deg2rad(angle))))/(L*np.cos(np.deg2rad(angle)))
        ax[1].plot(z,weight,color=c,label=f'{angle}°')
    ax[1].set(xlabel=T('深度 / nm','Depth / nm'),ylabel=T('归一化信号权重 / 每 nm','Normalized signal weight / per nm'))
    ax[1].legend(title=T('相对法线角度','Angle from normal'));ax[1].set_title(T('B  表面贡献更大','B  Surface-weighted signal'),loc='left')
    ax[2].barh([0,1,2],[284.8,4.5,1197.3],color=[blue,gold,green]);ax[2].set_yticks([0,1,2],[T('结合能','Binding energy'),T('分析器功函数','Analyzer work function'),T('测得动能','Measured kinetic energy')]);ax[2].set_xlabel('eV');ax[2].set_xlim(0,1400)
    for y,v in enumerate([284.8,4.5,1197.3]):ax[2].text(v+25,y,str(v),va='center',fontsize=10)
    ax[2].set_title(T('C  1486.6 eV 的能量账本','C  A 1486.6 eV energy budget'),loc='left')
    save(fig,'photoemission')

    e=np.linspace(0,800,4001);areas=np.array([5000.,1200.,9000.]);rsf=np.array([1.,1.8,3.]);centers=[284.8,400,532];labels=['C 1s','N 1s','O 1s']
    base=50+.035*e;survey=base+sum(a*gaussian(e,m,2.2) for a,m in zip(areas,centers));fractions=(areas/rsf)/sum(areas/rsf)
    fig,ax=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.55,1]})
    ax[0].plot(e,survey,color=blue);ax[0].invert_xaxis();ax[0].set(xlabel=T('结合能 / eV','Binding energy / eV'),ylabel=T('教学信号 / counts s⁻¹','Teaching signal / counts per second'))
    for m,l in zip(centers,labels):ax[0].annotate(l,(m,np.interp(m,e,survey)),xytext=(m+40,np.interp(m,e,survey)+100),arrowprops={'arrowstyle':'-','color':blue})
    ax[0].set_ylim(0,2100);ax[0].set_title(T('A  全谱先找到元素','A  Survey identifies elements'),loc='left')
    x=np.arange(3);ax[1].bar(x-.18,areas/areas.sum()*100,.36,label=T('直接按面积','Raw area fraction'),color=gold);ax[1].bar(x+.18,fractions*100,.36,label=T('灵敏度校正后','Sensitivity-corrected'),color=green);ax[1].set_xticks(x,labels);ax[1].set_ylabel('%');ax[1].set_ylim(0,80);ax[1].legend(fontsize=9);ax[1].set_title(T('B  不同元素的响应不同','B  Unequal elemental response'),loc='left')
    save(fig,'composition');np.savetxt(out/'survey.csv',np.c_[e,survey,base],delimiter=',',header='binding_energy_eV,signal_counts_per_s,background_counts_per_s',comments='')
    np.savetxt(out/'composition.csv',np.c_[areas,rsf,fractions],delimiter=',',header='area_counts_per_s_eV,teaching_RSF,atomic_fraction',comments='')

    rng=np.random.default_rng(570);x=np.linspace(282,292,501);mu=np.array([284.8,286.4,288.8]);trueA=np.array([6500,2200,1300]);sigma=.48;dwell=.4
    baseline=110+3*(x-282);true=baseline+sum(a*gaussian(x,m,sigma) for a,m in zip(trueA,mu));observed=rng.poisson(true*dwell)/dwell
    def model(x,a,b,c,w,p,q):return p+q*(x-282)+sum(A*gaussian(x,m,w) for A,m in zip([a,b,c],mu))
    p,cov=curve_fit(model,x,observed,p0=[6000,2000,1000,.5,100,2],sigma=np.sqrt(np.maximum(observed*dwell,1))/dwell,absolute_sigma=True,bounds=([0,0,0,.2,0,-10],[20000,20000,20000,1.2,500,20]))
    def incomplete(x,a,b,w,p,q):return p+q*(x-282)+a*gaussian(x,mu[0],w)+b*gaussian(x,mu[1],w)
    q,_=curve_fit(incomplete,x,observed,p0=[6500,2200,.5,100,2],bounds=([0,0,.2,0,-10],[20000,20000,1.2,1500,100]))
    fitted=model(x,*p);wrong=incomplete(x,*q);fitbase=p[4]+p[5]*(x-282)
    fig,ax=plt.subplots(2,2,figsize=(12,7.4),gridspec_kw={'height_ratios':[2,1]})
    for col,(fit,title) in enumerate([(fitted,T('A  三个已知教学环境','A  Three specified teaching environments')),(wrong,T('B  漏掉一个环境','B  One environment omitted'))]):
        ax[0,col].plot(x,observed,color='#9aa9ac',lw=.8,label=T('计数噪声数据','Count-noise data'));ax[0,col].plot(x,fit,color=green if col==0 else red,lw=2,label=T('拟合','Fit'));ax[0,col].set_title(title,loc='left');ax[0,col].legend(fontsize=9)
        ax[1,col].axhline(0,color='#8b9b9e',lw=1);ax[1,col].plot(x,observed-fit,color=blue if col==0 else red,lw=.9);ax[1,col].set_xlabel(T('结合能 / eV','Binding energy / eV'));ax[1,col].set_ylabel(T('残差 / counts s⁻¹','Residual / counts per second'))
        for row in [0,1]:ax[row,col].invert_xaxis()
    for a,m,c in zip(p[:3],mu,[blue,gold,red]):ax[0,0].fill_between(x,fitbase,fitbase+a*gaussian(x,m,p[3]),color=c,alpha=.2)
    ax[0,0].set_ylabel(T('信号 / counts s⁻¹','Signal / counts per second'));save(fig,'peak-model')
    np.savetxt(out/'carbon_region.csv',np.c_[x,observed,baseline,fitted,wrong,observed-fitted],delimiter=',',header='binding_energy_eV,observed_counts_per_s,true_background,three_component_fit,two_component_fit,residual',comments='')

    fig,ax=plt.subplots(1,3,figsize=(14,4.8));d=np.linspace(0,10,300)
    for ang,c in [(0,green),(30,gold),(60,blue)]:ax[0].plot(d,np.exp(-d/(L*np.cos(np.deg2rad(ang)))),color=c,label=f'{ang}°')
    ax[0].legend();ax[0].set(xlabel=T('均匀覆盖层厚度 / nm','Uniform overlayer thickness / nm'),ylabel=T('基底峰 / 裸基底峰','Substrate peak / bare-substrate peak'));ax[0].set_title(T('A  倾斜使基底更难看见','A  Tilt suppresses the substrate'),loc='left')
    xx=np.linspace(281,290,700);normal=gaussian(xx,284.8,.45);uniform=gaussian(xx,286.3,.45);differential=.6*gaussian(xx,284.8,.45)+.4*gaussian(xx,286.3,.45)
    ax[1].plot(xx,normal,color=green,label=T('无偏移','Unshifted'));ax[1].plot(xx,uniform,color=gold,label=T('整体 +1.5 eV','Uniform +1.5 eV'));ax[1].plot(xx,differential,color=red,label=T('不同区域带电不同','Differential charging'));ax[1].invert_xaxis();ax[1].set(xlabel=T('表观结合能 / eV','Apparent binding energy / eV'),ylabel=T('等面积信号 / 每 eV','Equal-area signal / per eV'));ax[1].legend(fontsize=8);ax[1].set_title(T('B  电势也会移动峰','B  Potential also shifts peaks'),loc='left')
    samples=np.array([8.,9.,7.,18.,20.,17.]);ax[2].scatter([0,0,0,1,1,1],samples,color=[blue]*3+[green]*3,s=45);ax[2].errorbar([0,1],[samples[:3].mean(),samples[3:].mean()],yerr=[samples[:3].std(ddof=1),samples[3:].std(ddof=1)],fmt='_',ms=22,color='#243c49',capsize=5);ax[2].set_xticks([0,1],[T('处理前','Before'),T('处理后','After')]);ax[2].set(xlim=(-.5,1.5),ylim=(0,25),ylabel=T('氧原子百分比 / at.%','Oxygen atomic percentage / at.%'));ax[2].set_title(T('C  三个独立试样','C  Three independent specimens'),loc='left');save(fig,'decisions')
    summary={'example_kinetic_energy_eV':1486.6-284.8-4.5,'information_depth_95_normal_nm':-L*np.log(.05),'information_depth_95_60deg_nm':-L*.5*np.log(.05),'substrate_ratio_2nm_normal':float(np.exp(-2/L)),'substrate_ratio_2nm_60deg':float(np.exp(-2/(L*.5))),'oxygen_atomic_fraction':float(fractions[2]),'fitted_oxygenated_carbon_fraction':float(sum(p[1:3])/sum(p[:3])),'true_oxygenated_carbon_fraction':.35,'fit_rms_counts_per_s':float(np.sqrt(np.mean((observed-fitted)**2))),'incomplete_fit_rms_counts_per_s':float(np.sqrt(np.mean((observed-wrong)**2))),'teaching_data':True}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
```

## 把表面化学变成下一步实验

回到最初那滴水。假设处理后的聚合物确实出现较高氧比例，并且 C 1s 的含氧环境贡献增加。现在可以提出更有针对性的问题：变化是否集中于表面；放置一周后，氧信号和润湿行为是否一起变化；水洗后是否仍保留；材料的粗糙程度是否也改变？角度系列帮助讨论深度分布，时间系列追踪表面重排或污染，清洗对照区分较弱附着与稳定保留的组分，形貌测量则检查几何因素。每项实验都连接到一种具体解释，研究因此从“有一张谱”走向“知道接下来该比较什么”。

![三种不同诊断的教学模型。A：均匀薄膜的基底信号衰减，L=2.5 nm。B：等面积单一环境受到均匀或差分充电，肩部可以来自电势分布。C：每组三个独立试样的构造氧比例，横线为均值，误差线为样本标准差。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9b90c90d9f792c4a4f51f7f8.svg?v=9b90c90d9f79)

图 4三种不同诊断的教学模型。A：均匀薄膜的基底信号衰减，L=2.5 nm。B：等面积单一环境受到均匀或差分充电，肩部可以来自电势分布。C：每组三个独立试样的构造氧比例，横线为均值，误差线为样本标准差。

蛋白质吸附提供另一个自然例子。对于本来几乎不含氮的基底，吸附后出现 N 1s 信号，可以支持表面出现含氮物质这一判断。接着比较仅经过缓冲液的基底、完整蛋白溶液处理的基底以及相同清洗条件，就能讨论信号来自盐、添加剂还是蛋白相关覆盖。若想知道蛋白是否仍保持活性，需要把表面化学与结合实验、酶活或细胞反应对应起来；这些测量分别读出组成和功能，联合后能解释为什么某些表面吸附很多蛋白，却未必产生预期的生物响应。

深度分析还可以通过离子溅射逐层去除材料。这个操作改变的是样品本身，因此必须同时考虑元素的优先去除、氧化物还原、聚合物断链和混层等效应。若目标是保留有机物原有化学状态，可先研究角分辨方案或合适团簇离子条件，再用参考材料检查处理前后变化。厚度、组成和化学态不是同一条轴上的三个名称：有时需要独立厚度信息，有时需要截面结构，有时需要更稳定的表面参照。把这些需要写成下一项测量，就能让 XPS 与其他方法形成清楚的合作关系。

整理结果时，把元素全谱、相关精细谱、背景与分量、残差和样品重复情况放在能够互相核对的位置。正文交代样品状态、光源、分析条件、发射角定义、充电处理和能量参照，并说明比例的分母。读者于是可以沿着同一条路线重建推理：光子激发电子，电子逃逸形成表面权重，能量位置提示电子环境，积分经过合适校正变成组成，最后由对照实验把组成变化连接到材料用途。这条路线既适用于一片塑料，也适用于覆盖蛋白的传感器和经过氧化的金属。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Introduction to X-ray photoelectron spectroscopy](https://mmrc.caltech.edu/XPS%20Info/Practical%20Guides%20to%20XPS/Intro%20to%20XPS.pdf)

   光电子能量关系、仪器、化学位移与表面敏感性。
2. [Practical guides: First steps in planning, conducting and reporting XPS](https://mmrc.caltech.edu/XPS%20Info/XPS%20practical%20guide.pdf)

   问题设计、样品状态、处理和结果记录。
3. [XPS guide: Charge neutralization and binding energy referencing](https://mmrc.caltech.edu/XPS%20Info/Practical%20Guides%20to%20XPS/XPS%20guide%20charge%20neutralization.pdf)

   绝缘样品充电、差分充电与参照条件。
4. [Practical guides: Quantitative XPS](https://ywcmatsci.yale.edu/sites/default/files/files/Practical%20guides%20for%20x-ray%20photoelectron%20spectroscopy%20-%20Quantitative%20XPS.pdf)

   灵敏度因子、背景、原子比例与薄膜定量。
5. [NIST: Inelastic mean free paths, effective attenuation lengths and information depths](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=929257)

   区分平均自由程、有效衰减长度与信息深度。
6. [Kai Siegbahn: Electron spectroscopy for atoms, molecules and condensed matter](https://wiki.epfl.ch/mep/documents/MEP%5B09-10%5D_DOWNLOAD/siegbahn_nobellecture.pdf)

   1981 年诺贝尔演讲：电子聚焦、分辨率与化学分析。
7. [Thermo Fisher: XPS quick guide](https://documents.thermofisher.com/TFS-Assets/MSD/Flyers/xps-quick-guide-fl0163.pdf)

   光源、电子分析器与常见表面研究应用。
