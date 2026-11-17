# Zeta电位：颗粒周围的电与运动

Source: https://ml-biomat.com/tutorials/experimental-methods/p02/
Language: zh-CN

沿着相位、速度和迁移率，认识盐、滑移面与分散液中的界面电性。

## 为什么一瓶分散液，换一种水就开始结团？

设想你把一种蛋白质包覆的纳米颗粒分散在水里，刚制备时液体均匀，换成含盐缓冲液后却渐渐出现絮状物。显微镜可以帮助寻找团块，动态光散射可以追踪尺寸变化，而Zeta电位测量要追问更靠近颗粒表面的事情：周围液体中的离子怎样组织起来，颗粒在电场里怎样移动，这种运动透露出怎样的界面状态。这里的“界面”就是两种物质相接的区域，例如固体颗粒与水的交界处。它虽然很薄，却能改变颗粒相遇时是容易贴住，还是保持一定距离。

这个问题也出现在更熟悉的事物里。颜料需要均匀分散，才能形成一致的颜色；水处理希望微小悬浮物聚成容易沉降的团块；蛋白质药物制剂则希望在储存期间维持合适的分散状态。结团本身没有统一的好坏，关键在于它是否符合使用目的。测量表面电性可以帮助选择酸碱度、盐的种类和添加剂，但研究者最后关心的仍是实际功能，例如涂层是否均匀、颗粒能否稳定输送、蛋白质是否保持活性。因而这章会把电位读数与粒径、外观和时间联系起来，而不把一个数字当作所有性能的替身。

Zeta写成希腊字母ζ，读作“泽塔”。电位可以先理解为与电荷所处位置有关的能量标尺，单位是伏；毫伏是千分之一伏。两个位置之间的电位差，决定单位正电荷从一个位置移到另一个位置时电势能怎样变化。仪器显示负电位，并不意味着颗粒含有“负的能量”；它表示相对于选定的远处液体，界面附近的电位更低。正负号还会影响颗粒在电场中的运动方向，因此在读数之前，必须知道仪器和模型怎样规定方向与参考零点。

最容易混在一起的三个量是表面电荷、表面电位和ζ电位。电荷回答表面多出或少了多少带电基团；表面电位描述紧靠材料表面的位置；ζ电位则与颗粒运动时液体发生相对滑动的位置有关。它们彼此联系，却需要不同的信息才能互相换算。给颗粒包上一层亲水聚合物，可能同时改变离子分布和流动边界，即使核心材料没有改变，也会改变测得的迁移率。本章先沿着运动这一条可观察的线索建立解释，再回到盐、酸碱度和材料设计。

## 颗粒带着怎样的一圈液体一起走？

许多表面遇水后会产生电荷。例如，一个酸性基团释放氢离子后，留下带负电的基团；某些碱性基团结合氢离子后，会带正电。离子也可以吸附在表面，改变原有的电荷分布。水里的正负离子不断热运动，同时受到电场影响：负表面附近通常更容易出现正离子，负离子相对减少。电荷吸引使反号离子靠近，热运动又使它们倾向于分散，两种作用达到统计平衡后，就形成由表面电荷和周围离子共同组成的电双层。

“双层”这个名字容易让人想到两张边界整齐的薄膜。较靠近表面的区域确实可能存在较紧密的吸附，但再往外的离子分布通常逐渐变化，像人口从城市中心向外围逐步稀疏，并没有一圈固定离子站在准确的外边缘。这个类比用来说明分布的连续性：离子仍在交换位置，平均浓度才形成稳定轮廓。电位也随距离逐渐接近远处液体的数值。不同盐浓度下，接近零的快慢不同，后面会用一条可计算的曲线来观察这件事。

当颗粒移动时，紧邻表面的部分液体和吸附物会随它一起运动，较远处液体则与它产生相对运动。对于能用清晰边界近似的颗粒，可以画出一个滑移面，也叫剪切面；ζ电位取这个位置相对于远处液体的电位差。把它想成穿着外套穿过人群：人群接触到的边界与身体表面并不重合。这个比喻解释了为何包覆层会影响读数，但真实的聚合物层可以让水和离子穿行，它并非不透水的外套。对软颗粒、渗透性凝胶和浓厚刷层，流动发生在一段区域中，硬球的单一滑移面模型需要进一步扩展。

电泳的早期研究常借显微镜观察颗粒移动，再把位移和经过的时间换成速度。1931年Henry关于颗粒电泳的研究把颗粒尺寸与电双层范围的关系带入迁移率换算，说明同样的运动不能脱离几何和介质来解释。图中的装置是这一观察原理的示意：电场由正端指向负端，负迁移率颗粒沿相反方向运动。右边则把表面与滑移面画在同一条电位曲线上。科学史中的这一步仍体现在现代仪器的软件中：先从光信号提取运动，再选择物理模型计算电位。

![A为早期显微电泳观察原理的原创示意，联系Henry1931年的研究，不是某台历史装置复原。B为25°C、1mmol/L离子强度、表面电位−15mV的平面低电位模型；滑移面外移改变读取位置。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2ed30ebdd50c63e266bf5b78.svg?v=2ed30ebdd50c)

图 1A为早期显微电泳观察原理的原创示意，联系Henry1931年的研究，不是某台历史装置复原。B为25°C、1mmol/L离子强度、表面电位−15mV的平面低电位模型；滑移面外移改变读取位置。

看右图时，可以先固定表面电位，再把滑移面向外移动。读到的ζ绝对值会变小，表面本身并不需要变成电中性。这提醒我们关注两个不同的变化：表面的化学基团是否改变，以及包覆层、吸附层是否改变了流动边界。若一种纳米载体接触蛋白质溶液后ζ发生变化，后续可比较吸附前后的粒径、蛋白质含量和介质组成，把“界面改变”进一步落实到可以检验的结构解释上。

## 从看见运动，到读懂光的相位

速度是位移除以时间，电泳迁移率则把速度再除以电场强度。这样做的原因是：在线性响应范围内，把推动颗粒的电场加倍，平均电泳速度也加倍；除去电场后得到的系数，才方便比较不同测量设置。电场强度的单位是伏每米，描述电位在空间中变化的快慢。理想均匀场中，两电极的电压差除以间距就是场强；实际样品池的弯曲通道和电极几何要通过仪器的场强标定来处理。只记下施加多少伏，还不足以比较两种池子的运动条件。

$$
\mu_e=\frac{v_e}{E},\qquad v_{\mathrm{obs}}=\mu_eE+v_b,\qquad E=\frac{\Delta V}{L}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30854555fd9f63edbc653606.svg) | 电泳迁移率，m²/(V·s)，保留正负号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/faaaf4cbacd278edd00b6bef.svg) | 颗粒相对于液体的电泳速度，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 沿选定方向的电场强度，V/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/446a2b5c06840d79dbea4391.svg) | 实验观察到的平均速度，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0b1d31d4957d48699797e34.svg) | 与电场无关的恒定背景液流速度，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d734398b2cf2660032fdbf86.svg) | 按电场方向定义的电压下降，V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 均匀场近似中的电极间距，m。 |

线性响应、稳态速度，并以液体为电泳参考。理想10V跨越0.01m得到1000V/m；μe=−1.949911×10⁻⁸m²/(V·s)，ve=−19.49911μm/s。加入3μm/s恒定背景流，观测−16.49911μm/s。弯曲或非均匀样品池使用其场强校准。

颗粒同时也在做布朗运动。对单颗粒观察来说，随机位移会叠加在定向移动上，短时间看去可能忽左忽右；通过足够多的颗粒或时间记录，可以估计平均漂移速度。光学电泳仪不必逐个追踪可见颗粒，而是收集许多颗粒散射的光。颗粒移动会改变散射光相对于参考光的相位，也可以表现为微小频率偏移。可以把相位看成钟表指针在一圈中的位置：两只钟同速时相对角度保持不变，转速略有差别时，相对角度会逐渐积累。

相位分析光散射，简称PALS，利用这种累积来测量微小运动。把每个时刻的相位差画出来，平均斜率便与速度有关。一个完整周期相当于二π弧度，仪器原始角度经常被限制在一圈内；相位展开就是把跳回起点的记录接成连续变化。它要求相邻采样之间的变化和噪声足以被正确辨认。本章构造一个已知光学投影系数的复信号，加上随机噪声，再进行展开和直线拟合，让这一处理过程变得可见。

$$
\phi(t)=\phi_0+q_{\parallel}v_{\mathrm{obs}}t,\qquad v_{\mathrm{obs}}=\frac{1}{q_{\parallel}}\frac{d\phi}{dt}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/05b88f36b3fde196e67c87eb.svg) | 展开相位与初始相位，rad。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a08ebf776281e4521428c39.svg) | 散射矢量沿速度方向的带符号投影系数，m⁻¹；由光学几何规定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/446a2b5c06840d79dbea4391.svg) | 该方向观测速度，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fe11c3232bceca2eab4e659c.svg) | 相位对时间的斜率，rad/s。 |

恒定速度的光学相位模型，相位符号与参考光约定一致。q∥=3×10⁶m⁻¹、vobs=−16.49911μm/s时，斜率−49.49733rad/s，0.25s内变化−12.37433rad。实际构造记录对复信号加噪声后展开，再拟合斜率。

图中的六个电场包含三个大小和两个方向。对于设定为−25mV的模型颗粒，迁移率约为−1.950×10⁻⁸m²/(V·s)。在1000V/m电场下，相对于液体的电泳速度约为−19.50μm/s。例子另加入始终朝同一方向的3μm/s背景流，所以仪器观察到约−16.50μm/s；电场反向时则观察到约22.50μm/s。把所有观测速度对电场作图，直线斜率恢复迁移率，截距恢复恒定背景流。这里保留正负方向，才能把两种运动分开。

![构造信号，种子820；ζ=−25mV，黏度0.89mPa·s、相对介电常数78.4，恒定流3μm/s，光学投影系数3×10⁶m⁻¹。A显示两个方向的相位，B用六个场强拟合，C保留相位残差。D另加0.5×10⁻⁸m²/(V·s)的电渗迁移贡献，展示正反电场不能自动去除的项。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b647d40b11be10e52f4fe254.svg?v=b647d40b11be)

图 2构造信号，种子820；ζ=−25mV，黏度0.89mPa·s、相对介电常数78.4，恒定流3μm/s，光学投影系数3×10⁶m⁻¹。A显示两个方向的相位，B用六个场强拟合，C保留相位残差。D另加0.5×10⁻⁸m²/(V·s)的电渗迁移贡献，展示正反电场不能自动去除的项。

还有一种液流会随电场一起反向。样品池壁也有电双层，外加电场能够推动壁面附近液体，形成电渗流；封闭池内还会出现回流。若某处液体速度本身正比于电场，简单地把正反电场的结果平均，得到的斜率仍包含这部分液流。图D专门展示这个差别。真实仪器可以利用特定观测位置、池体设计，或利用颗粒响应和液流建立时间不同的快速反向测量来处理它。因而“用了交变电场”与“已正确校正电渗流”之间，需要一套明确的测量方法来连接。

## 迁移率怎样成为毫伏，模型又怎样进入结果？

运动受到电作用推动，也受到液体黏性阻力。黏度越大，同样的界面电性和电场通常产生越慢的运动；介质的介电性质则决定电场和电荷之间怎样相互作用。因此，从迁移率换算ζ，需要知道测量温度下的动力黏度和介电常数。动力黏度以Pa·s计，水在25°C附近约为0.00089Pa·s，也就是0.89mPa·s。相对介电常数是与真空相比的无量纲倍数，而公式里的绝对介电常数还要乘上真空介电常数，单位为F/m。少写这一项会让数值完全失去物理意义。

Henry关系还包含一个与κa有关的函数。a是颗粒半径，κ的倒数是电双层的一个特征长度，因此κa比较的是颗粒大小与离子屏蔽范围。电双层相对于颗粒很厚时，Hückel极限给出函数值1；相对很薄且符合相应电动学条件时，Smoluchowski极限给出1.5。同样的迁移率代入这两个换算方式，会得到不同的ζ。中间区域需要使用适合的函数或更完整的模型，而不是凭水溶液这个名称自动选择某一个常数。

$$
\mu_e=\frac{2\varepsilon\zeta f(\kappa a)}{3\eta},\quad\varepsilon=\varepsilon_0\varepsilon_r,\qquad\zeta_{\mathrm{Smol}}=\frac{\eta\mu_e}{\varepsilon}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30854555fd9f63edbc653606.svg) | 电泳迁移率，m²/(V·s)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/35264eff6bf21304fbf59624.svg) | ζ电位以及Smoluchowski换算值，V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 动力黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 液体绝对介电常数，F/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 真空介电常数，本例8.8541878128×10⁻¹²F/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f1d4e2d001f572c0acb3f119.svg) | 液体相对介电常数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | Debye长度的倒数，m⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 颗粒半径，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c38ceecfc9d2ffb270e214f3.svg) | Henry函数，无量纲；Hückel极限为1，Smoluchowski极限为1.5。 |

Henry经典关系使用相应稀分散刚性颗粒与低电位近似，模型需考虑双电层尺度、松弛和表面导电条件。右式由f=1.5得到。μe=−4.5×10⁻⁸、η=0.00089Pa·s、εr=78.4，右式ζ=−0.05769494V；f=1则−0.08654241V。标准物质保留其报告的Smoluchowski约定与舍入认证值。

以−4.5×10⁻⁸m²/(V·s)为例，使用25°C、黏度0.89mPa·s、相对介电常数78.4，Smoluchowski换算得到约−57.69mV。如果改用Hückel极限，则得到约−86.54mV，绝对值相差一半。这两个数字不是样品突然发生了变化，而是同一个迁移率经过了两个不同的模型。后面的标准物质例子按照其报告采用的Smoluchowski关系，保留认证结果−58mV。把迁移率与模型名称一起报告，读者才能追溯这个数值从哪里进入物理解释。

Henry的经典处理针对相应的稀分散、刚性颗粒和低电位近似，忽略某些双电层松弛和表面导电效应。电位较大、表面导电明显或颗粒柔软时，应选择包含这些物理过程的处理。这个条件也解释了为什么不要把ζ换算成一个简单的“每颗粒带多少电子”。电场作用的不只是一个孤立电荷点，还涉及周围离子和液体的共同运动。若研究目标是表面基团的数量，可结合酸碱滴定、表面化学分析或吸附测量，让不同实验各自回答明确的问题。

读软件结果时，最好沿着输入和输出走一遍：介质组成决定该用什么黏度与介电参数，温度改变这些参数，颗粒半径和离子强度帮助选择模型，光学记录给出迁移率，再进行电位换算。设定值与样品条件一致，计算才具有清楚的含义。若两台仪器报告不同ζ，先比较迁移率和这些输入，有时差别会在换算环节被找到；若迁移率已经不同，就继续检查样品制备、场强、池壁流动以及测量时间。

## 盐改变的是电作用的空间范围

往水里加入氯化钠，会增加能够重新分布的正负离子。负表面吸引正离子后，远处看到的电作用受到更强屏蔽。为描述这种变化，常用Debye长度：在一个简化的低电位模型中，距离增加一个Debye长度，电位幅度缩小到原来的约37%。它是衰减尺度，不是一层液体的硬边界。对于相同温度和介电性质的稀电解质溶液，这个长度与离子强度平方根的倒数成正比，所以浓度增加一百倍，衰减长度缩短十倍。

离子强度与“加了多少盐”相关，但要把每种离子的浓度和电荷数都算进去。钠离子带一个基本正电荷，氯离子带一个基本负电荷；平方后它们对离子强度都作正贡献。二价离子在相同摩尔浓度下有更大的权重，而且还可能发生特异吸附或桥联，因此更换盐种类时既改变屏蔽，也可能改变表面化学。缓冲液中的所有主要离子同样参与计算。电导率测量有助于检查溶液是否一致，但不同离子移动能力不同，电导率与离子强度并非可以无条件互换的同一个量。

$$
I=\frac12\sum_i c_i z_i^2,\qquad\lambda_D=\kappa^{-1}=\sqrt{\frac{\varepsilon k_BT}{2e^2N_A\,1000I}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 离子强度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29928b2adca455a1420619c0.svg) | 第i类离子的摩尔浓度，mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | 第i类离子的电荷数，如Na⁺为+1、Ca²⁺为+2，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 各离子种类的编号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e0a253a79b8148f73aac3fcc.svg) | Debye长度(m)及其倒数(m⁻¹)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 液体绝对介电常数，F/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2600a50cd45c9994bcd80b30.svg) | 玻尔兹曼常数，1.380649×10⁻²³J/K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 基本电荷量，1.602176634×10⁻¹⁹C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/160ee348aa1d6f945e161c12.svg) | 阿伏伽德罗常数，6.02214076×10²³mol⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/11e3e740ee2e42f3954f5b75.svg) | 将mol/L换成mol/m³的单位换算因子，L/m³。 |

理想稀电解质、连续介质的Debye屏蔽尺度。1mmol/L NaCl有相同浓度的Na⁺与Cl⁻，I=0.001mol/L；T=298.15K、εr=78.4给λD≈9.61370nm。I增加100倍，λD减小10倍。代码输入mmol/L，其数值已等于mol/m³，因此不会再乘1000。

图A给出25°C水介质中的计算值：离子强度为0.1、1、10和100mmol/L时，Debye长度依次约30.40、9.61、3.04和0.96nm。图C把半径一起画进去，同样1mmol/L的溶液，对半径1nm的对象和半径1000nm的对象，κa相差一千倍。色图里的等值线是尺度提示，不是仪器精度的合格线；靠近哪一种理论极限，还要结合需要的准确度和其他模型条件判断。这个图也说明，单靠某一个盐浓度阈值无法替所有纳米颗粒选择换算方式。

![理想电解质、固定水介电参数、25°C计算。A的Debye长度按离子强度平方根倒数变化；B固定表面电位−15mV，虚线滑移面距表面1nm；C显示κa而非仪器准确度，等值线1和100是尺度参照。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5773ad179757792ed2b5272d.svg?v=5773ad179757)

图 3理想电解质、固定水介电参数、25°C计算。A的Debye长度按离子强度平方根倒数变化；B固定表面电位−15mV，虚线滑移面距表面1nm；C显示κa而非仪器准确度，等值线1和100是尺度参照。

为了单独观察屏蔽，先取一个平面、低电位模型，并固定表面电位为−15mV。让滑移面位于表面外1nm，在1mmol/L时读到约−13.52mV，在100mmol/L时读到约−5.30mV。表面电位没有改变，读数已经接近零，原因是沿途的电位衰减更快。这个模型把问题拆得很清楚：保持表面条件，改变屏蔽长度，再在同一个位置读取电位。实际表面还会发生电荷调节，盐和酸碱度可能同时改变基团解离，因此实验中的曲线可以比这幅图更复杂。

$$
\psi(x)=\psi_0\exp\left(-\frac{x}{\lambda_D}\right),\qquad\zeta=\psi(\delta)=\psi_0\exp\left(-\frac{\delta}{\lambda_D}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f24b70e332dca9c1dbcbb320.svg) | 位置x与表面处的电位，统一使用V或mV。 |
| ![Formula](https://ml-biomat.com/static/agent-math/74f5bfc58ab11608a49c92ee.svg) | 距表面的距离与滑移面位置，统一长度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ae336c0d5d10c0c71e8df08c.svg) | Debye长度，与x及δ同一长度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/00f4c72c0a43d6a0501d3d63.svg) | 滑移面相对于远处液体的电位，与ψ同一电位单位。 |

固定表面电位、平面、低电位的线性化模型，远处电位为0；忽略特异吸附和电荷调节。ψ0=−15mV、δ=1nm，I=1mmol/L时ζ=−13.51813mV，100mmol/L时−5.30085mV。模型展示屏蔽和读取位置，不是实际材料的酸碱滴定预测。

下面的交互把离子强度、滑移面位置和表面电位分别交给你。先保持表面电位不变，观察两种方式如何让ζ的绝对值减小；再把表面电位改成正值，检查曲线是否保留同样的空间规律。图中显示到40nm，在低盐条件下曲线仍可能没有完全回到零，这正说明屏蔽具有较长的尾部。这里计算的是明确设定的平面电位剖面，不把ζ变化自动解释成表面电荷消失，也不把滑块产生的结果当成某种真实材料的酸碱滴定曲线。

## 同一表面，为什么读到不同的ζ？

平面低电位模型，25°C，固定相对介电常数78.4。改变盐的离子强度、滑移面距表面的距离与表面电位，观察电位剖面及滑移面读数。κa另按100nm半径计算，只作尺度参照。

[Figure: 电位随表面距离变化的曲线](https://ml-biomat.com/tutorials/experimental-methods/p02/#P02-plot)

## 把酸碱度、吸附与分散稳定性连成实验

改变pH可以改变表面酸碱基团的解离状态。随着pH扫描，ζ可能从正变负，穿过零的位置叫等电点，表示在所测介质和方法下电泳迁移率接近零。零电荷点则针对表面净电荷，两者在存在特异离子吸附等情况时可以不同。对于蛋白质或蛋白质包覆颗粒，表面还有正负电荷斑块、构象变化和吸附层变化，平均电位接近零并不等于每个区域都没有电荷。理解这一点后，测量曲线的用途就从“寻找一个神奇的pH”变成“寻找界面状态如何随条件改变”。

一个可比较的pH实验需要照顾滴定过程中悄悄改变的其他因素。加入酸碱会改变体积和离子组成，局部高浓度还可能先让蛋白质变性或颗粒聚集。可以制备独立的pH样品，维持相近的背景电解质；也可以逐步滴定并记录每一步添加量、平衡时间和电导率，同时比较升pH与降pH路径。两条路径不重合时，要检查是否发生不可逆吸附、聚集或结构变化。若某个pH下大团块沉降，光学测量可能主要读取仍悬浮的部分，所以同步记录外观和粒径能帮助识别样品群体发生了变化。

1940年代发展的DLVO理论把电双层排斥和范德华吸引放在同一个颗粒相互作用框架中。可以把两颗粒靠近的过程想成越过一段地形：排斥形成需要跨越的能垒，吸引使贴近后的状态更有利；盐改变排斥作用的范围，热运动则不断提供相遇机会。这个图景解释了为什么许多带电分散液加盐后更容易聚集。ζ为界面电动学提供信息，真正的能垒还取决于颗粒几何、距离、介质和表面条件，储存时间也决定多少次相遇最终累积成可见变化。

亲水聚合物和蛋白质包覆还会引入另一条稳定路径。两颗粒靠近时，表面链层被挤压、重叠，链的可用构象和局部溶剂状态发生变化，可以产生空间位阻稳定作用。这时较小的ζ绝对值与稳定分散可以同时出现。相反，吸附物覆盖不均匀或一条链连接两颗粒时，也可能促进桥联。因而研究配方时，可以将ζ作为电性这一维，与粒径随时间的变化、浊度、沉降和功能检测并列。这样每个读数都对应一个机制，配方优劣也回到具体使用条件下判断。

上机前先让样品和分散介质达到设定温度，记录pH、配方、颗粒浓度与电导率。需要稀释时，优先使用与样品液相条件相匹配的介质，并检查稀释是否改变吸附平衡；直接加入纯水可能把要研究的状态改掉。浓度过低时散射信号弱，过高时多重散射和相互作用增加，可以用一组保持介质组成的浓度系列寻找稳定读数区间。样品池的清洁、透光窗口、气泡和电极状态都会影响信号，连续记录的相位斜率若逐渐变化，就检查温度、聚集以及电极附近的反应，而不是只取最后显示的平均数。

场强也可以成为诊断变量。在温度和样品状态稳定的线性范围，迁移率应在合理场强变化下保持一致；若增加电场后读数系统改变，焦耳热、极化和液流都值得检查。具体电压需要结合样品池几何、导电性与仪器方法选择。实验设计中同时安排独立制样、不同取样和同一份样品的重复测量，才能分辨配方差异、取样差异与仪器短期波动。每次只改变一个科学因素，并保留相应的对照，最终得到的曲线才会告诉你该调整哪一步。

## 让真实参考数据和完整计算帮助判断读数

标准物质提供了一个可以共同检查测量系统的对象。NIST与JRC发布的胶体二氧化硅SRM1992/ERM-FD305，在规定的硼酸盐缓冲液和25°C条件下具有认证迁移率−4.5×10⁻⁸m²/(V·s)，扩展不确定度为0.4×10⁻⁸m²/(V·s)，覆盖因子k为2。认证报告用指定介质参数将迁移率换算成ζ，得到−58±5mV。这里的两个认证量有明确的计算联系，不能把它们看作两次互不相关的独立测量来相互验证。

图中重绘了报告表E1.1的15组被接受数据，每组有六个独立取样的平均值，而每个取样在原研究中又测量了五次。六个取样来自三个安瓿，分三天测量，因而同时涉及取样和跨日测量因素。15组来自12个实验室，其中同一实验室提供了四种仪器或样品池组合。因此图上的点首先代表取样均值，不是90次独立制备，更不是90个实验室。金色点显示每组内部差异，蓝色横线是六个取样均值的一个样本标准差。背景色带则对应认证值的扩展不确定度，二者定义不同。图形把取样均值的组内分散、组间差别和参考值范围放到同一个坐标里，便于逐层阅读。

![真实数据重绘：Ramaye等，NIST SP260-208，表E1.1及表11–12。15组数据来自12个实验室，每组六个取样均值；金点为取样均值，蓝线为均值±1样本标准差，色带为认证迁移率±扩展不确定度(k=2)。L11a–d为同一实验室的不同配置。B是报告的不确定度分量，不是各实验室误差棒。仅转录数值事实并重新绘图。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7cf4b39b73c66ac0a41a6d68.svg?v=7cf4b39b73c6)

图 4真实数据重绘：Ramaye等，NIST SP260-208，表E1.1及表11–12。15组数据来自12个实验室，每组六个取样均值；金点为取样均值，蓝线为均值±1样本标准差，色带为认证迁移率±扩展不确定度(k=2)。L11a–d为同一实验室的不同配置。B是报告的不确定度分量，不是各实验室误差棒。仅转录数值事实并重新绘图。

这些公开数值保留到原表的小数位后，计算得到各组均值的平均约为−4.53478，单位为10⁻⁸m²/(V·s)。认证报告还包含均匀性、运输和储存稳定性研究，所以不能直接用这90个数的离散程度代替完整认证不确定度。右图展示的四个相对标准不确定度分量分别为1.39%、3.40%、0.42%和1.80%。在所用独立分量合成近似下，先平方相加再开平方，最后乘覆盖因子；这与把所有百分数直接相加有不同的统计含义。用印出的四个舍入值计算约为8.22%，原报告基于其完整计算给出8.3%，两者的小差别保留为舍入效应。

$$
u_{c,\mathrm{rel}}=\sqrt{u_{\mathrm{char,rel}}^2+u_{\mathrm{bb,rel}}^2+u_{\mathrm{sts,rel}}^2+u_{\mathrm{lts,rel}}^2},\qquad U_{\mathrm{rel}}=k u_{c,\mathrm{rel}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7ee35732f6e138b09fc67bda.svg) | 合成相对标准不确定度，用比例或%一致表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ad4038a42317ce1bbc0c4683.svg) | 赋值研究的相对标准不确定度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/81fd171c2ddcdbf497fb6c1f.svg) | 安瓿间不均匀性的相对标准不确定度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/520c56af957880e974d91b05.svg) | 短期和长期稳定性的相对标准不确定度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2a2c9da525563eccc6f917ad.svg) | 扩展相对不确定度，与各u使用同一表示方式。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 覆盖因子，无量纲，本例2。 |

在相应独立分量合成近似下使用平方和。印出的1.39%、3.40%、0.42%、1.80%得到uc,rel≈4.112%、k=2时Urel≈8.224%；报告保留其完整计算的8.3%。认证迁移率不确定度舍入为0.4×10⁻⁸m²/(V·s)。图中各组±1SD与这里的扩展不确定度定义不同。

本章的完整Python例子沿两条路径展开。第一条使用随机种子820生成六段带噪声的复光学信号，展开相位，拟合速度，再由场—速度直线分离迁移率与恒定漂移。运行结果恢复约−25.005mV和3.0003μm/s，与设定的−25mV及3μm/s相符；残差图保留噪声，让读者检查直线假设。第二条读取随代码打包的真实迁移率数据，重算各组均值和标准差，并与认证值及不确定度分量一起作图。构造信号和真实数据分别标清，前者解释算法，后者展示研究数据的层次。

代码还计算盐浓度对应的Debye长度、固定表面电位时的空间剖面，以及两种Henry极限的换算差异。输出的CSV保存场强与速度、相位记录的选定配对、屏蔽长度和参考数据统计；压缩数组保留全部相位与残差，便于更换拟合时间窗进行比较。若想继续探索，可以把背景流改为与电场成正比，观察为什么截距校正不再解决问题；也可以增大噪声，缩短记录时间，检查速度斜率的稳定程度。每一次修改都对应一个可解释的测量环节。

### 从相位到迁移率，再读真实标准物质数据

完整运行复信号生成、相位展开、速度和迁移率拟合、介质屏蔽计算、真实取样均值统计及不确定度合成，离线输出全部图与数据。

```
"""Zeta potential: from constructed optical phase to mobility and conversion.
Real reference-material aliquot means are bundled in data/mobility.csv.
Run offline: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json,csv as csvlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#20333e','axes.labelcolor':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(f,n):
 for e in ['svg','png']:f.savefig(O/f'{n}-{args.language}.{e}',dpi=145,bbox_inches='tight')
 plt.close(f)
def csv(n,heads,cols):np.savetxt(O/n,np.column_stack(cols),delimiter=',',header=','.join(heads),comments='',fmt='%.10g')
eps0=8.8541878128e-12;epsr=78.4;eps=eps0*epsr;eta=.00089;T=298.15;kb=1.380649e-23;e=1.602176634e-19;NA=6.02214076e23
def debye(I_mM):return np.sqrt(eps*kb*T/(2*e**2*NA*np.asarray(I_mM)))
rng=np.random.default_rng(820);zeta=-.025;mu=eps*zeta/eta;vbg=3e-6;q=3e6
fields=np.array([-1500,-1000,-500,500,1000,1500.]);t=np.linspace(0,.25,501);fitted=[];phases=[];residuals=[]
for E in fields:
 velocity=mu*E+vbg;phase=.4+q*velocity*t
 signal=np.exp(1j*phase)+.035*(rng.normal(size=t.size)+1j*rng.normal(size=t.size))
 unwrapped=np.unwrap(np.angle(signal));coef=np.polyfit(t,unwrapped,1);fit=np.polyval(coef,t)
 fitted.append(coef[0]/q);phases.append(unwrapped);residuals.append(unwrapped-fit)
fitted=np.array(fitted);phases=np.array(phases);residuals=np.array(residuals)
mf,bf=np.polyfit(fields,fitted,1);zf=mf*eta/eps
np.savez_compressed(O/'phase_records.npz',time_s=t,fields_V_m=fields,phase_rad=phases,phase_residual_rad=residuals)
csv('field_velocity.csv',['field_V_m','true_velocity_m_s','fitted_velocity_m_s'],[fields,mu*fields+vbg,fitted])
csv('phase_pair.csv',['time_s','phase_minus1000_rad','phase_plus1000_rad'],[t,phases[1],phases[4]])

# A historical principle illustration, not a reconstruction of a named apparatus.
fig,axs=plt.subplots(1,2,figsize=(12.8,5.4),layout='constrained',gridspec_kw={'width_ratios':[1.1,1]})
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off');ax.set_title(L('A  从显微观察到迁移率','A  From microscope observation to mobility'),loc='left')
ax.add_patch(Rectangle((.7,2),8.6,2.4,facecolor='#e6f1f2',edgecolor=B,lw=2))
for x,sign in [(1,'+'),(9,'−')]:ax.plot([x,x],[2.2,4.2],color=R,lw=5);ax.text(x,4.65,sign,ha='center',fontsize=22)
ax.annotate('',xy=(7.6,3.8),xytext=(2.4,3.8),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.text(5,4.05,L('电场 E','Electric field E'),ha='center',color=R)
for x in [3.8,4.5,5.2]:ax.add_patch(Circle((x,2.9),.16,color=B))
ax.annotate('',xy=(2.4,2.9),xytext=(3.4,2.9),arrowprops={'arrowstyle':'->','color':B,'lw':2});ax.text(5.6,2.85,L('负迁移率颗粒','Negative-mobility particles'),fontsize=10)
ax.plot([4.1,4.1],[5.1,6],color=K,lw=9);ax.plot([3.5,4.7],[5.1,5.1],color=K,lw=3);ax.plot([4.1,4.1],[4.4,5.05],color=K,ls=':');ax.text(4.7,5.6,L('显微镜观察位移','Microscope observes displacement'),fontsize=10)
ax.text(.8,1.35,L('1931 · Henry 将颗粒曲率与双电层尺度\n接入迁移率—电位的关系。','1931 · Henry links particle curvature and\ndouble-layer extent to mobility conversion.'),va='center',fontsize=11)
ax.text(.8,.4,L('原理示意；电极方向与符号明确','Principle illustration; explicit field and sign'),fontsize=10,color='#61717b')
ax=axs[1];x=np.linspace(0,25,400);lam=debye(1)*1e9;psi=-15*np.exp(-x/lam);slip=1.;ax.plot(x,psi,color=B,lw=2.5);ax.fill_between(x,psi,0,color=B,alpha=.08);ax.axvline(slip,color=R,ls='--');ax.scatter([0,slip],[-15,-15*np.exp(-slip/lam)],color=[B,R],zorder=5);ax.axhline(0,color=K,lw=.7)
ax.annotate(L('表面电位 −15 mV','Surface potential −15 mV'),(0,-15),(7,-14.3),arrowprops={'arrowstyle':'->','color':B},color=B)
ax.annotate(L('滑移面处 ζ','ζ at slipping plane'),(slip,-15*np.exp(-slip/lam)),(9,-10.2),arrowprops={'arrowstyle':'->','color':R},color=R)
ax.text(9,-.8,L('远处液体取零电位','Bulk liquid sets zero potential'),fontsize=10)
ax.set(xlabel=L('距表面距离 / nm','Distance from surface / nm'),ylabel=L('电位 / mV','Potential / mV'),title=L('B  运动的边界决定读哪个电位','B  The motion boundary defines which potential'),ylim=(-17,1))
save(fig,'history-interface')

fig,axs=plt.subplots(2,2,figsize=(12.8,9),layout='constrained')
for j,c in [(1,B),(4,R)]:axs[0,0].plot(t,phases[j],color=c,lw=1.2,label=f'E = {fields[j]:.0f} V/m')
axs[0,0].set(xlabel=L('时间 / s','Time / s'),ylabel=L('展开相位 / rad','Unwrapped phase / rad'),title=L('A  构造的光学相位记录','A  Constructed optical phase records'));axs[0,0].legend(frameon=False)
axs[0,1].scatter(fields,fitted*1e6,color=B,s=45,zorder=3);ef=np.linspace(-1600,1600,100);axs[0,1].plot(ef,(mf*ef+bf)*1e6,color=B);axs[0,1].axhline(0,color=K,lw=.7);axs[0,1].axvline(0,color=K,lw=.7);axs[0,1].set(xlabel=L('电场 / V m⁻¹','Electric field / V m⁻¹'),ylabel=L('观测速度 / μm s⁻¹','Observed velocity / μm s⁻¹'),title=L('B  斜率给迁移率，截距给恒定漂移','B  Slope gives mobility; intercept gives drift'));axs[0,1].text(.06,.06,f'μ = {mf/1e-8:.5f} × 10⁻⁸ m²/(V s)\n'+L('漂移','Drift')+f' = {bf*1e6:.4f} μm/s',transform=axs[0,1].transAxes,fontsize=10,bbox={'fc':'#fcfbf7','ec':'none'})
for j,c in [(1,B),(4,R)]:axs[1,0].plot(t,residuals[j],color=c,alpha=.7,lw=.8)
axs[1,0].set(xlabel=L('时间 / s','Time / s'),ylabel=L('相位拟合残差 / rad','Phase-fit residual / rad'),title=L('C  残差揭示记录是否偏离直线','C  Residuals test the straight-line model'))
eo=.5e-8;vals=[mu,mu+eo];labels=L(['恒定背景流已扣除','还存在随电场反向的液流'],['Constant background removed','Field-dependent flow remains']);axs[1,1].barh([1,0],np.array(vals)/1e-8,color=[B,R],height=.55);axs[1,1].set_yticks([1,0],labels);axs[1,1].set(xlim=(-2.2,0),xlabel=L('从场—速度斜率得到的量 / 10⁻⁸ m² V⁻¹ s⁻¹','Field–velocity slope / 10⁻⁸ m² V⁻¹ s⁻¹'),title=L('D  反向电场不会自动消除电渗流','D  Polarity reversal alone does not remove EOF'));axs[1,1].tick_params(axis='y',labelsize=9)
for y,v in zip([1,0],vals):axs[1,1].text(v/1e-8+.05,y,f'{v/1e-8:.4f}',va='center',color='white',fontweight='bold')
save(fig,'phase-to-mobility')

Is=np.logspace(-1,2,200);lams=debye(Is)*1e9;x=np.linspace(0,40,401)
csv('screening.csv',['ionic_strength_mM','Debye_length_nm','zeta_at1nm_mV'],[Is,lams,-15*np.exp(-1/lams)])
fig,axs=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
axs[0].loglog(Is,lams,color=B,lw=2.5)
for ii in [.1,1,10,100]:axs[0].scatter(ii,debye(ii)*1e9,color=R);axs[0].annotate(f'{debye(ii)*1e9:.2f}',(ii,debye(ii)*1e9),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
axs[0].set(xlabel=L('离子强度 / mmol L⁻¹','Ionic strength / mmol L⁻¹'),ylabel=L('Debye长度 / nm','Debye length / nm'),title=L('A  浓度百倍，长度缩短十倍','A  100× concentration gives 10× shorter range'),ylim=(.7,55))
for ii,c in zip([.1,1,10,100],[B,G,Y,R]):
 la=debye(ii)*1e9;axs[1].plot(x,-15*np.exp(-x/la),color=c,label=f'{ii:g} mM')
axs[1].axvline(1,color=K,ls='--',lw=1);axs[1].set(xlabel=L('距表面距离 / nm','Distance from surface / nm'),ylabel=L('电位 / mV','Potential / mV'),title=L('B  固定表面电位的平面模型','B  Planar model at fixed surface potential'),ylim=(-16,1));axs[1].legend(frameon=False,fontsize=9)
aa=np.logspace(0,3,180);kap=aa[:,None]/lams[None,:];im=axs[2].pcolormesh(Is,aa,np.log10(kap),cmap='viridis',shading='auto',vmin=-1.5,vmax=3);cs=axs[2].contour(Is,aa,kap,levels=[1,100],colors='white',linewidths=1.4);axs[2].clabel(cs,fmt={1:'κa = 1',100:'κa = 100'},fontsize=9,manual=[(20,2.15),(5,430)]);axs[2].set(xscale='log',yscale='log',xlabel=L('离子强度 / mmol L⁻¹','Ionic strength / mmol L⁻¹'),ylabel=L('颗粒半径 a / nm','Particle radius a / nm'),title=L('C  模型选择还取决于颗粒半径','C  Model choice also depends on radius'));fig.colorbar(im,ax=axs[2],label='log₁₀(κa)',shrink=.8)
save(fig,'salt-and-scale')

with (Path(__file__).parent/'data/mobility.csv').open(encoding='utf8') as f:rows=list(csvlib.DictReader(f))
names=[r['dataset'] for r in rows];data=np.array([[float(r[f'r{i}']) for i in range(1,7)] for r in rows]);means=data.mean(axis=1);sd=data.std(axis=1,ddof=1);components=np.array([1.39,3.40,.42,1.80]);urel=2*np.linalg.norm(components)
csv('reference_summary.csv',['dataset_index','mean_mobility_1e8','SD_of_six_aliquot_means_1e8'],[np.arange(len(names)),means,sd])
fig,axs=plt.subplots(1,2,figsize=(12.8,7.2),layout='constrained',gridspec_kw={'width_ratios':[1.3,1]});ax=axs[0];yy=np.arange(len(names));ax.axvspan(-4.9,-4.1,color=B,alpha=.1,label=L('认证值 ± U（k=2）','Certified value ± U (k=2)'));ax.axvline(-4.5,color=B,ls='--');ax.errorbar(means,yy,xerr=sd,fmt='o',color=B,ecolor=B,capsize=3,ms=4,label=L('均值 ± 1 SD','Mean ± 1 SD'))
for k in yy:ax.scatter(data[k],k+np.linspace(-.14,.14,6),s=13,color=Y,alpha=.8)
ax.set(yticks=yy,yticklabels=names,xlabel=L('迁移率 / 10⁻⁸ m² V⁻¹ s⁻¹','Mobility / 10⁻⁸ m² V⁻¹ s⁻¹'),title=L('A  真实测量：15组，每组6个取样均值','A  Measured: 15 datasets, six aliquot means each'));ax.invert_yaxis();ax.legend(frameon=False,fontsize=9,loc='lower right')
ax=axs[1];lab=L(['赋值研究','安瓿之间','短期稳定性','长期稳定性'],['Characterization','Between ampoules','Short-term stability','Long-term stability']);ax.barh(np.arange(4),components,color=[B,R,Y,G],height=.5);ax.set_yticks(np.arange(4),lab);ax.set(xlim=(0,4.4),ylim=(-1,5.8),xlabel=L('相对标准不确定度 / %','Relative standard uncertainty / %'),title=L('B  重复性以外的不确定度','B  Uncertainty beyond repeatability'))
for j,v in enumerate(components):ax.text(v+.08,j,f'{v:.2f}%',va='center')
ax.text(.1,4.3,L('认证迁移率：−4.5 ± 0.4\n单位：10⁻⁸ m²/(V s)，k = 2','Certified mobility: −4.5 ± 0.4\nUnit: 10⁻⁸ m²/(V s), k = 2'),fontsize=11,color=B)
ax.text(.1,5.25,L('由迁移率换算：ζ = −58 ± 5 mV','Converted from mobility: ζ = −58 ± 5 mV'),fontsize=11,color=K)
save(fig,'reference-and-uncertainty')

summary={'seed':820,'true_mobility_m2_Vs':mu,'fitted_mobility_m2_Vs':mf,'fitted_zeta_mV':zf*1000,'fitted_constant_drift_um_s':bf*1e6,'EOF_apparent_mobility_m2_Vs':mu+.5e-8,'Debye_length_at1mM_nm':float(debye(1)*1e9),'Debye_ratio_1_to100mM':float(debye(1)/debye(100)),'planar_zeta_at1mM_mV':float(-15*np.exp(-1/(debye(1)*1e9))),'planar_zeta_at100mM_mV':float(-15*np.exp(-1/(debye(100)*1e9))),'reference_dataset_count':len(names),'reference_aliquot_count':int(data.size),'mean_of_reference_dataset_means_1e8':float(means.mean()),'reference_Smoluchowski_mV':-4.5e-8*eta/eps*1000,'reference_Huckel_mV':-4.5e-8*3*eta/(2*eps)*1000,'expanded_relative_from_rounded_components_percent':float(urel),'phase_residual_RMS_rad':float(np.sqrt(np.mean(residuals**2)))}
(O/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

当你需要比较两种颗粒配方，可以从一个清楚的问题开始：包覆是否改变了界面电性，盐是否改变了作用范围，还是储存过程中出现了聚集。把相同介质条件下的迁移率、换算模型、ζ及其重复分布写清楚，再把它们与粒径和时间变化对照，就能把一行毫伏读数变成关于材料界面的实验判断。读者也能沿着相位、运动、模型和条件重新走过这条计算链，理解结果为何成立。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Ramaye et al.: NIST SP260-208, Certification of SRM1992/ERM-FD305](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-208.pdf)

   迁移率认证、真实取样均值、扩展不确定度和换算约定。

   Numerical values from Tables E1.1, 11 and 12 of the joint NIST/JRC report, transcribed and plotted with attribution; original artwork and prose are not reproduced.
2. [Malvern: Zeta Potential, An Introduction](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104zetapotentialintroduction)

   界面离子、酸碱度与空间位阻稳定。
3. [IUPAC Gold Book: Electrokinetic Potential](https://goldbook.iupac.org/terms/view/E01968)

   滑移面与电动电位的定义。
4. [Clogston & Vermilya: NCL Method PCC-2, Measuring Zeta Potential of Nanoparticles](https://dctd.cancer.gov/drug-discovery-development/assays/nano/ncl-methods-pcc2.pdf)

   样品、测量池、浓度、相位诊断及报告条件。
5. [Malvern: Measuring Zeta Potential Using PALS](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104phaseanalysislightscattering)

   相位斜率如何给出速度。
6. [Malvern: M3-PALS and Electro-osmosis](https://www.malvernpanalytical.com/en/learn/knowledge-center/application-notes/an101104zetapotentialm3-pals)

   电渗流、观测位置和场反向的动态作用。
7. [Royal Society Archives: Henry (1931) Cataphoresis Paper, RR43/57](https://makingscience.royalsociety.org/items/rr_43_57/referees-report-by-frederick-alexander-lindemann-on-a-paper-the-cataphoresis-of-suspended-particles-part-ithe-equation-of-cataphoresis-by-d-c-henry)

   Henry1931年工作的历史记录。
