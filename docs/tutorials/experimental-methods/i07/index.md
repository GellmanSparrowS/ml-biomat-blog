# 小角X射线散射：看见纳米尺度的集合结构

Source: https://ml-biomat.com/tutorials/experimental-methods/i07/
Language: zh-CN

从一瓶透明蛋白质溶液出发，读懂散射曲线、回转半径与拟合范围。

## 一瓶透明蛋白质溶液，里面的分子有没有抱成团

把一小瓶蛋白质溶液放在灯下，它可能像清水一样透明。透明只能说明可见光没有被大量散射到眼睛里，并不告诉我们蛋白质是各自舒展、两两结合，还是少数已经聚成较大的团簇。药物制剂的保存、酶在不同酸碱度下的形状变化、聚合物胶束的形成，都需要回答这种“看起来没有变化，内部究竟怎样”的问题。小角X射线散射，通常写作SAXS，让一束X射线穿过样品，测量它在原来前进方向附近偏转的微弱光。这里的“小角”描述探测方向，不表示研究对象很小；恰好相反，与原子间距产生的较大角度散射相比，靠近直射光的信号常常包含更大尺度的结构信息。

可以先想象在远处观察一群举着小灯的人。若每个人独立改变位置，远处收到的光强分布会随排列方式改变。X射线散射也来自许多散射单元的共同贡献，只是其中必须考虑波的相位，也就是不同波的起伏是否对齐。蛋白质里的电子、水里的电子都参与散射，我们最终需要提取的是蛋白质相对于周围溶液的差异。SAXS因此适合研究溶液中的分子整体尺寸、形状和集合状态，也适合研究凝胶中的密度起伏、纳米颗粒和胶束。它把整个被照射体积内的大量对象共同记录下来，得到的是统计平均信号，而不是给某一个分子拍下轮廓清楚的照片。

本节围绕一份公开的溶菌酶溶液数据展开。溶菌酶是一种能切断细菌细胞壁特定化学连接的蛋白质，鸡蛋清中就含有它，因此“透明液体里有一颗折叠起来的分子”并非遥远的场景。我们将读出真实散射曲线，解释为什么低角度曲线的下降速度能反映分子的分布尺度，再亲自改变拟合范围，观察同一份数据为何会给出略有差别的尺寸。学习的重点不是记住某个蛋白质的标准答案，而是建立一条清楚的测量链：样品和缓冲液怎样进入仪器，探测到的强度怎样成为曲线，曲线中的哪些特征又支持怎样的结构判断。

## 从金属为什么变硬，到溶液里的纳米结构

小角散射的发展与一个很具体的材料问题有关：某些铝铜合金经过放置或热处理后会变硬，普通显微观察却未必立即看出变化。Guinier在回忆中记述，1938年研究小角散射时，两位冶金研究者请他检查时效中的铝铜合金。他看到的异常散射帮助人们把力学性质变化与晶体内部很细小的组织联系起来。这段历史的意义在于，研究者没有要求所有结构变化都表现为清晰的大颗粒；他们转而追问，原子组成或电子密度的微小不均匀，能否通过波的干涉留下可测的痕迹。今天用SAXS研究蛋白质和聚合物，同样是在寻找肉眼看不见、但会影响功能的内部排列。

现代仪器的示意图把这个思想变成一条光路。狭缝或其他光学元件把入射光束整理得足够窄，光束经过装有样品的毛细管，绝大部分继续向前，少量光偏离原方向。探测器要分辨这种很小的偏角，样品与探测器之间常留出较长距离；一个挡光片遮住强烈的直射光，避免它淹没附近的弱散射。挡光片也带来实际后果：最接近零角度的一部分信号通常无法直接测得。因此，后面出现的“零角强度”往往是根据模型外推得到的量，而不是探测器中央某个像素的简单读数。

散射实验常把角度换成散射矢量大小q。这里不需要先掌握矢量代数，可以把q理解为一个把波长和角度合并起来的尺度坐标。波长越短，同一偏角对应的q越大；偏角越靠近直射方向，q越小。小q对较大范围的相对位置敏感，大q逐渐带出更细的内部信息，但“一个q对应一个独立尺寸”只是帮助定位数量级的直觉。只有真正周期性结构的峰，才适合直接把峰位换算为明确的重复距离。蛋白质的平滑曲线来自许多原子间距离的共同作用，需要整体分析。

$$
q=\frac{4\pi\sin\theta}{\lambda}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 散射矢量大小，nm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 总散射角2θ的一半，数值三角函数用弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X射线波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

波长0.15 nm、总偏角1°时，半角0.5°给出q=0.731073 nm⁻¹。q统一角度和波长，供不同测量几何下比较。

本例波长约为0.15 nm。若射线总偏转角为1°，公式中的半角就是0.5°，算出的q约为0.731 nm⁻¹；如果把1°直接代入半角位置，结果会接近加倍。这种角度定义看似细小，却会把后面估计的长度整体带偏。q也常用Å⁻¹表示，而1 nm等于10 Å，所以0.1 Å⁻¹等于1 nm⁻¹。读入数据时先确认单位，比在拟合完成后凭经验判断“尺寸似乎合理”可靠得多。图中的两种排列则提醒我们，平均距离相同并不意味着内部形状相同，尺寸参数只是结构描述的开始。

![原创概念图。A把1930年代关注内部细小不均匀的历史问题与现代SAXS光路连接，角度夸大以便阅读，直射束止于挡光片。B以侧视符号比较均匀实心球和同一均方半径的分散单元，说明相同Rg不确定唯一结构。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0049c7988279d606fdb575d4.svg?v=0049c7988279)

图 1原创概念图。A把1930年代关注内部细小不均匀的历史问题与现代SAXS光路连接，角度夸大以便阅读，直射束止于挡光片。B以侧视符号比较均匀实心球和同一均方半径的分散单元，说明相同Rg不确定唯一结构。

## 先把水和容器量好，蛋白质的信号才会显出来

一份溶液测量包含蛋白质、缓冲液、毛细管及其他背景的共同贡献。缓冲液并不是纯水的另一个名字，它还可能含盐、酸碱缓冲组分、甘油或还原剂。这些物质会改变电子密度，也会改变蛋白质的相互作用。最有用的参照通常是与样品尽可能匹配、但不含目标蛋白质的溶液，例如同一次透析得到的外液，或尺寸排阻色谱实验中适当选择的缓冲液帧。只凭配方重新配一杯“差不多”的液体，微小浓度差也可能在相减后留下明显偏差，尤其在蛋白质本身散射较弱的高q区域。

实际处理还要考虑曝光时间、入射光强、透过率和探测器响应。先把这些条件归一到共同尺度，再用样品曲线减去适当缩放的缓冲液曲线，才能把差值解释为目标对象的散射。减法不会自动消除随机误差：两个有波动的读数相减，波动会共同进入结果。如果两个测量的误差独立，差值的方差等于两个方差之和；缩放背景时，其误差也随缩放系数一起变化。这解释了为什么很小的蛋白质差值，仍可能带着不小的误差条。

$$
I_p=I_s-aI_b,\qquad \sigma_p^2=\sigma_s^2+a^2\sigma_b^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/44d9fad31d63f36e8d73e778.svg) | 处理后的对象相对溶剂散射强度，共同强度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d3bc1f47b81d56c2b85373af.svg) | 归一后的溶液强度，与背景同尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c826a1b7cf2ddf4418889fa6.svg) | 匹配缓冲液的归一强度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 已确定的背景缩放系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b40cd07d2c7b2ebebd2a46c9.svg) | 差值、溶液和背景的标准误差，各自与强度同单位。 |

独立测量且缩放系数视为已知时，方差相加。1050±10减1000±10，a=1，得到50±14.142；此处±表示一个标准误差。若a也有不确定度，还需传播其贡献。

例如某个q位置，归一后的样品强度为1050，标准误差为10；匹配缓冲液强度为1000，标准误差为10，缩放系数为1。相减得到50，而标准误差约为14.14，不是零，也不是两个误差相减得到的零。信号与误差之比只有约3.54。若真实蛋白质贡献更小，随机波动完全可能让差值出现负数。负数在这里描述两次测量的差，并非“探测到了负的光子”。因此，不能为了画对数曲线而把所有负值改成很小的正数；应保留原表，并在线性坐标上检查它们的位置与误差。

样品准备还包括浓度、均一性和时间。测量一组浓度，可以观察曲线除以浓度后是否重合；若低q区域随浓度发生系统改变，分子间的吸引或排斥可能已经参与信号。把一次长曝光拆成多个短帧，则可以检查X射线照射过程中是否出现聚集或结构变化。离心或过滤适合解决某些尘埃和大颗粒问题，但也可能改变研究对象的组成，操作前应明确要研究的是完整分散体系还是其中的可溶部分。样品温度、缓冲液、浓度和曝光过程都属于实验条件，因为它们直接决定瓶子里存在什么。

## 曲线起点怎样给出一个分子的分布尺度

现在观察低q区域。偏角很小时，同一颗粒内部各处散射的波彼此相差还不大，强度随q的下降可以用一个简单的指数形式近似。这就是Guinier近似。取强度的自然对数后，指数下降变成一条直线，横轴选q的平方，斜率与回转半径的平方成正比。自然对数可以理解为把“相乘的变化”改写为“相加的变化”的刻度；本节不要求手算对数，只需要知道，若近似成立，选定区域里的点应接近直线，而直线越陡，代表的分布尺度越大。

$$
I(q)\simeq I(0)e^{-q^2R_g^2/3},\qquad \ln I(q)=b+mq^2,\quad R_g=\sqrt{-3m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 散射矢量大小，nm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a9c085d6657ea9c3c169083b.svg) | 指定q处强度及模型外推的零角强度，沿用共同强度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/742acc50d5d386b6c8461bed.svg) | 散射对比度分布的回转半径，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 所选强度单位下ln I(0)的数值截距。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | ln I对q²的斜率，nm²。 |

小q近似使初始曲线主要反映均方尺度。真实曲线在0.087–0.8 nm⁻¹窗口的加权拟合斜率约−0.588695 nm²，因此Rg=1.328942 nm。对数拟合使用相对误差σI/I的一阶近似。

回转半径Rg这个名字容易让人想到一颗球绕着中心转，其实这里描述的是散射对比度如何分布在中心周围。对于内部对比度均匀的对象，可以把它分成许多小块，计算每块到中心的距离平方，求平均后再开平方。远离中心的小块因为距离被平方而更有影响。均匀实心球的Rg约为其几何半径的0.775倍；一根细长杆、一条柔性链和一颗球，即使具有相同Rg，也可能拥有很不一样的最大长度与外形。把Rg直接叫“颗粒半径”会抹掉这种区别。

$$
R_g^2=\frac{\sum_j w_j r_j^2}{\sum_j w_j},\qquad R_{g,\mathrm{sphere}}=\sqrt{\frac35}\,R
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/742acc50d5d386b6c8461bed.svg) | 同号散射对比度对象的回转半径，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 散射小单元的编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f6264b954f8fef8d9872def7.svg) | 第j单元相对于溶剂的散射权重，共同单位；本均匀对象例各处同号。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ac93bfc1786051ffd5b120d4.svg) | 第j单元距对比度加权中心的距离，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 均匀实心球的几何半径，nm。 |

先平均距离平方，再开方。均匀球的体积积分得到3R²/5；本例Rg=1.328942 nm对应等效均匀球半径1.715656 nm。真实对象形状需由更多信息描述。

本节对归档溶菌酶曲线选取q从0.087到0.8 nm⁻¹的区域，并对正强度点进行加权对数线性拟合。权重使用归档标准误差传播到对数后的近似：相对误差越小的点，权重越大。得到斜率约为−0.5887 nm²，因此Rg约为1.329 nm；外推的零角强度约为11.64，沿用归档强度单位。若仅为建立几何直觉，把这一Rg换成均匀实心球的等效半径，会得到约1.72 nm。这个换算给出一个体积均匀球的比较尺度，并没有把真实溶菌酶的表面凹凸变成球面。

近似适用到哪里，需要结合结果再检查。常见紧凑颗粒使用qRg小于约1.3的区域作为起点，细长或内部不均匀对象可能需要更小的上限。这并不是一条保证所有数据都正确的开关：低q曲线看起来直，也可能仍包含相互作用或少量大颗粒的影响。本例上限乘以拟合Rg约为1.063，满足常用的初步尺度检查；接下来还应观察残差、上下限变化和独立样品条件。最前几个点虽然误差较大，仍保留在完整图中，使读者能看见靠近挡光片处的信息质量。

## 在真实曲线上练习：同一个名字下面，保留完整测量条件

公开数据库SASBDB中的SASDAC2记录由Darja Ruskule提交，样品是乙酸钠缓冲液中的鸡源溶菌酶，页面给出的缓冲液浓度为40 mmol/L、pH为3.8。下载文件包含2168行q、强度和误差数据，q使用nm⁻¹。它已经经过溶液与背景的处理，因此本节从散射曲线开始分析，并不把它描述成探测器的原始像素。数据库页面报告的Guinier回转半径为1.5 nm，而本节明确指定窗口和权重的简化拟合约为1.329 nm。两个数的差别正好提供一个值得追查的分析问题，而不是把自己的结果强行调到页面数字。

第一幅数据图保留整个q范围的走势，低角区是较高的强度，高角区逐渐接近较弱的信号。第二个面板把低q数据转换为Guinier坐标，填实的点进入本节拟合，空心点提供相邻区域的参照。第三个面板显示“观测减预测，再除以该点归档误差”的残差：若连续一段都在零线上方或下方，说明偏差有方向，不能只用一个很高的相关系数把它盖过去。第四个面板逐步改变拟合上限，展示Rg怎样随窗口移动。这样，拟合得到的尺寸就与实际选择过程放在同一张图里。

误差条还有一个需要仔细理解的地方。对数误差近似要求相对误差不要过大，因此最初那些强度与误差相当的点，虽然保留下来，却几乎不影响加权拟合。完整代码另外在原强度坐标中用同一个指数近似做非线性加权拟合，便于比较坐标变换的影响。两种方法使用同一组点和同一组归档误差；它们并不是两次独立实验。真正独立的支持来自重新制备样品、改变浓度或曝光条件、以及其他测量方法。把计算中的交叉检查和实验中的独立重复分清，才能正确理解一致性有多大分量。

![真实数据：Darja Ruskule，SASBDB SASDAC2，依数据库自由复用政策署名。A展示正强度的全范围对数图；B保留拟合内外点；C使用归档误差标准化残差；D比较拟合上限。最初点的大误差在图中可见，模型窗口不是数据库页面的原始分析设置。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6cbcad191bfb6388979fca12.svg?v=6cbcad191bfb)

图 2真实数据：Darja Ruskule，SASBDB SASDAC2，依数据库自由复用政策署名。A展示正强度的全范围对数图；B保留拟合内外点；C使用归档误差标准化残差；D比较拟合上限。最初点的大误差在图中可见，模型窗口不是数据库页面的原始分析设置。

如果研究问题是“某种处理是否使蛋白质展开”，最有价值的设计并不是各测一条曲线后比较一个Rg。先保证处理前后缓冲液匹配，再比较多个浓度和照射帧，随后观察Rg、整体曲线形状以及可能的柔性变化。一个明显增大的Rg既可能来自单分子展开，也可能来自分子聚集；两者对生物功能的含义很不同。尺寸排阻色谱联用SAXS可以沿洗脱过程观察不同大小组分，配合浓度检测和质量信息，把这些解释逐步分开。实验设计提供区分机制的条件，数学拟合则负责把条件下的信号说清楚。

## 尺寸之外：紧凑、柔性、聚集与背景留下不同线索

把两条曲线的横轴都乘以各自Rg，再把纵轴强度除以各自零角强度，可以先消去整体尺度和强弱差别。进一步乘上横轴的平方，就得到常用的无量纲Kratky表示。它把原来被低角度高强度压住的形状差异凸显出来。图中均匀球与理想高斯链具有相同的Rg，但曲线不同：球模型表现出衰减和振荡，理想链在相应范围趋向另一种走势。真实蛋白质的结构、柔性和内部电子密度更复杂，因此图形比较要和样品状态、可测q范围及误差一起阅读，而不是把所有有峰的曲线都判成“折叠正常”。

这种表示中的每一个量都有明确角色。qRg是无量纲横坐标，表示观察尺度相对于对象大小；强度比I(q)/I(0)也是无量纲，表示相对于零角度的散射下降；二者组合后的纵坐标不再带长度或强度单位。代码中的球模型和高斯链模型用于展示几何后果，与旁边真实溶菌酶高q数据分别标注。高q面板使用线性坐标，保留负值和误差条，能看见在弱信号区，背景处理与随机波动的重要性。把这两类图放在一起，是为了学会同时看结构模式和测量质量，而不是用理想曲线替代实验曲线。

![A为同一Rg下的均匀球与理想高斯链教学模型，纵横轴均无量纲。B为SASDAC2实际高q数据，线性坐标保留负强度。两面板分别帮助判断形状差异与弱信号质量。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/49c17feecfd3bc88aff2324c.svg?v=49c17feecfd3)

图 3A为同一Rg下的均匀球与理想高斯链教学模型，纵横轴均无量纲。B为SASDAC2实际高q数据，线性坐标保留负强度。两面板分别帮助判断形状差异与弱信号质量。

进一步分析还可以求距离分布P(r)，它把不同散射单元之间的距离贡献汇总起来，帮助理解对象是较紧凑还是较伸长。由于测量只覆盖有限q范围，而且带有噪声，从曲线到距离分布需要平滑和最大尺寸等选择。可以把这理解为凭有限的回声重建房间：回声包含空间信息，但必须考虑记录带宽和噪声，不能随意补出所有细节。选择最大尺寸时，应检查分布末端是否自然回到零、拟合是否稳定，以及改变范围后形状是否合理。仅仅为了使另一种Rg与Guinier结果相同而调整参数，会把独立检查变成相互迎合。

对聚合物凝胶和胶束，研究者还会遇到相关峰、界面散射和不同组分的对比度。一个峰可能来自对象之间的平均排列，而不是单个对象的直径；盐浓度变化既可能改变粒子尺寸，也可能改变粒子之间的相互作用。读图时可以依次提出三个问题：样品中有什么对象，它们内部怎样分布，它们彼此怎样排列。SAXS曲线把三者叠在同一个信号里，浓度系列、对比度变化和互补实验则帮助逐一分解。问题问得具体，拟合模型才有选择依据。

为什么少量大颗粒值得留意？在足够低的q处，同一对象内部的散射贡献能够近似同相相加，先相加的是波的振幅，强度再与振幅的平方有关。因此，相同组成下，一个体积更大的紧凑对象，其单颗粒低角度贡献可以增长得比体积本身更快。由很多小分子组成的聚集体，即使颗粒数很少，也可能明显影响低q曲线。这里还要分清“固定颗粒数”与“固定总蛋白质量”：把同样总量的蛋白质聚成更大的对象，会同时减少对象数目，整体变化需要把两者一起计算。实验中保留浓度信息并观察洗脱过程，正是为了把散射强弱、对象数量与单个对象大小连起来，而不是仅凭曲线更高就判断样品更多。

## 亲手移动拟合窗口，观察结论如何跟着证据变化

下面的交互实验使用同一份公开曲线中的低q数据。下限控制从哪里开始纳入点，上限控制在哪个q停止；蓝点参与拟合，其他点仍留在图中。试着先保持下限不变，只把上限从0.4逐渐增加到1.2 nm⁻¹，观察直线、Rg以及q上限乘Rg的变化。较宽窗口提供更多点，却可能越过近似适用的区域；较窄窗口更接近小角极限，却可能让斜率对噪声和局部起伏更敏感。这个权衡来自信息本身，不能用“点越多越好”或“直线越短越安全”解决。

然后把下限向右移动，检查低q点的影响。若某些数据看起来碍眼，先问它们对应的误差、挡光片附近的几何、背景和样品状态是什么，再决定怎样处理。交互中每次改变窗口都会重新计算点数和拟合结果，因此你可以直接看到，一次貌似微小的删点动作怎样改变结构参数。所有范围外的数据继续显示，便于把局部拟合放回完整曲线中。实验记录应同时保存范围、单位、误差处理和结果；只留下一个带许多小数的Rg，会丢掉重现计算所需的关键信息。

## 真实曲线：移动Guinier拟合窗口

数据为Darja Ruskule提交的SASBDB SASDAC2。蓝点参与加权拟合，空心点保留上下文；调整范围后同时阅读Rg、点数和qmax Rg。

[Figure: 真实SAXS数据的Guinier拟合](https://ml-biomat.com/tutorials/experimental-methods/i07/#I07-plot)

## 完整计算：把曲线、误差和选择一起保存

下面的完整Python例子直接读取随例子提供的SASDAC2文件，不需要再次联网。文件前四行是说明，随后2168行是数据，末尾还有其他文本，因此读取时明确指定数据行数。程序保留原始q、归档强度与误差三列，另外导出本次拟合的选择标记和预测值。这样，任何一个拟合点都能返回原始表格核对，范围外和负强度数据也没有消失。程序还输出窗口敏感性表，便于把不同选择下的Rg画成连续曲线，而不是只保存最符合期待的一次结果。

计算中的一项检查使用没有噪声的已知Guinier曲线：预先设定Rg为1.5 nm、零角强度为10，再让同一拟合函数恢复这两个数。这个检查验证公式、单位和实现是否一致；真实溶菌酶数据则展示实际曲线与简化模型之间的差别。两种任务分开放置，可以避免把“程序能找回自己生成的参数”误当成“蛋白质结构已经确认”。执行结果同时给出线性化与原强度拟合、低q窗口和高q弱信号图，形成一份能继续分析的记录。

完成这组练习后，可以回到最初的透明小瓶。SAXS让我们把“分子有没有变化”拆成可测的问题：低角区的分布尺度怎样改变，整体形状是否保持，是否出现大对象的贡献，结果是否随浓度和照射时间变化。它尤其适合把溶液状态下的生物分子与材料纳米结构放在同一种测量语言里。下一步若需要知道一个多孔支架中孔隙在三维空间怎样连接，就要换一种保留空间位置的方法；小角散射提供整体统计，X射线微米CT则通过许多方向的投影重建体积，这正是下一节要建立的联系。

### 完整Python：公开溶菌酶曲线与Guinier窗口

读取随包提供的真实曲线，进行两种加权拟合、窗口敏感性检查和模型形状比较，并保存原数据、选择标记与结果。

```
"""Read the openly reusable SASBDB SASDAC2 profile and teach SAXS inference.

python main.py --output results --language en
Data credit: Darja Ruskule, SASBDB SASDAC2 (lysozyme in sodium acetate).
https://www.sasbdb.org/data/SASDAC2/ ; https://www.sasbdb.org/about/
The archive permits unrestricted reuse with attribution. The archived profile
is processed solution-minus-buffer intensity, not a raw detector exposure.
"""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from scipy.optimize import curve_fit

def fit_guinier(q, intensity, sigma, lo=.087, hi=.8):
    m=(q>=lo)&(q<=hi)&(intensity>0)&(sigma>0)
    x=q[m]**2; y=np.log(intensity[m]); weights=intensity[m]/sigma[m]
    X=np.column_stack([np.ones(m.sum()),x])
    coeff=np.linalg.lstsq(X*weights[:,None],y*weights,rcond=None)[0]
    rg=np.sqrt(-3*coeff[1]) if coeff[1]<0 else np.nan
    return {'rg_nm':float(rg),'i0':float(np.exp(coeff[0])),
            'points':int(m.sum()),'slope_nm2':float(coeff[1]),
            'intercept':float(coeff[0]),'qmax_rg':float(hi*rg)},m

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
        'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#18344a',
        'text.color':'#18344a','axes.edgecolor':'#8295a2','svg.fonttype':'none',
        'savefig.facecolor':'#fbfcfc','figure.facecolor':'#fbfcfc'})
    blue='#186c94';green='#188777';orange='#d27839';gray='#a1abb2'
    def save(fig,name):
        fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(out/f'{name}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(fig)
    # The historical ATSAS file has four header lines, 2168 rows, then a footer.
    data=np.loadtxt(Path(__file__).parent/'data'/'SASDAC2.dat',skiprows=4,max_rows=2168)
    q,I,sigma=data.T
    result,mask=fit_guinier(q,I,sigma)
    nonlinear,_=curve_fit(lambda x,i0,rg:i0*np.exp(-x*x*rg*rg/3),q[mask],I[mask],
                         sigma=sigma[mask],p0=[12,1.4],absolute_sigma=True)
    windows=np.arange(.4,1.201,.025)
    sensitivity=np.array([fit_guinier(q,I,sigma,hi=h)[0]['rg_nm'] for h in windows])
    testq=np.linspace(.1,.8,80);testI=10*np.exp(-testq**2*1.5**2/3)
    reference,_=fit_guinier(testq,testI,np.ones(80)*.1)
    summary={**result,'nonlinear_rg_nm':float(nonlinear[1]),'nonlinear_i0':float(nonlinear[0]),
       'rows':len(q),'nonpositive_rows':int(np.sum(I<=0)),
       'noiseless_rg_nm':reference['rg_nm'],'noiseless_i0':reference['i0'],
       'q_for_1deg_invnm':float(4*np.pi*np.sin(np.deg2rad(.5))/.15),
       'equivalent_sphere_radius_nm':float(np.sqrt(5/3)*result['rg_nm']),
       'intensity_units':'archived intensity units; absolute calibration not asserted',
       'data_credit':'Darja Ruskule; SASBDB SASDAC2'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    predicted=result['i0']*np.exp(-q*q*result['rg_nm']**2/3)
    np.savetxt(out/'data.csv',np.column_stack([q,I,sigma,mask.astype(int),predicted]),delimiter=',',
         header='q_invnm,intensity,reported_sigma,guinier_selected,guinier_prediction',comments='')
    np.savetxt(out/'window_sensitivity.csv',np.column_stack([windows,sensitivity]),delimiter=',',
         header='qmax_invnm,rg_nm',comments='')
    # Original apparatus illustration; not a replica of a historical camera.
    fig,axs=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1.55,1]})
    a=axs[0];a.set_xlim(0,10);a.set_ylim(-2,2);a.axis('off')
    a.plot([.3,8.45],[0,0],color=blue,lw=2)
    for x in [1.5,2.4]:
        a.add_patch(Rectangle((x,-.8),.16,.72,color=gray));a.add_patch(Rectangle((x,.08),.16,.72,color=gray))
    a.add_patch(Rectangle((3.8,-.6),.3,1.2,facecolor='#b5dddb',edgecolor=green))
    a.plot([8.8,8.8],[-1.8,1.8],color=blue,lw=5)
    a.add_patch(Rectangle((8.45,-.18),.3,.36,color='#394d5c'))
    for s in [-1,1]:a.plot([4,8.8],[0,s*1.3],color=orange,lw=2)
    for x,y,z,e in [(1.9,1.25,'准直狭缝','Collimation'),(4,-1.2,'溶液样品','Solution'),(8.4,-.7,'挡光片','Beamstop'),(8.7,1.6,'探测器','Detector')]:a.text(x,y,tr(z,e),ha='center',fontsize=10)
    a.annotate('',xy=(8.8,-1.65),xytext=(4,-1.65),arrowprops={'arrowstyle':'<->','color':blue})
    a.text(6.3,-1.95,tr('较长距离：分开很小的角度','Long distance resolves small angles'),ha='center',fontsize=10)
    a.set_title(tr('A  1930年代的小角问题 → 现代几何','A  A 1930s question → modern geometry'),loc='left')
    b=axs[1];b.set_xlim(-3,3);b.set_ylim(-2.1,2.1);b.set_aspect('equal');b.axis('off')
    b.add_patch(Circle((-1.5,0),1,facecolor='#b5dddb',edgecolor=green))
    theta=np.linspace(0,2*np.pi,10,endpoint=False)
    b.scatter(1.5+.775*np.cos(theta),.775*np.sin(theta),s=35,color=orange)
    b.plot([-1.5,-.5],[0,0],color=green);b.text(-1.5,-1.45,tr('均匀实心圆球','Uniform solid sphere'),ha='center',fontsize=10)
    b.text(1.5,-1.45,tr('分散散射单元','Separated scatterers'),ha='center',fontsize=10)
    b.set_title(tr('B  相同均方距离，不同内部排列','B  Same mean-square distance, different structure'),loc='left',fontsize=11)
    save(fig,'geometry')
    fig,ax=plt.subplots(2,2,figsize=(12,9));a,b,c,d=ax.ravel()
    positive=I>0
    a.errorbar(q[positive][::8],I[positive][::8],yerr=sigma[positive][::8],fmt='.',ms=3,lw=.5,color=blue,alpha=.65)
    a.set_yscale('log');a.set_ylim(.01,30);a.set_xlabel('q / nm⁻¹');a.set_ylabel(tr('归档强度','Archived intensity'))
    a.set_title(tr('A  真实溶菌酶溶液曲线','A  Measured lysozyme solution profile'),loc='left')
    a.text(.97,.96,tr('非正强度见下一幅线性坐标图','Nonpositive intensities shown on linear axis next'),transform=a.transAxes,ha='right',va='top',fontsize=9)
    low=(q<=1.2)&positive
    b.errorbar(q[low]**2,np.log(I[low]),yerr=sigma[low]/I[low],fmt='o',ms=2,mfc='white',mec=gray,color=gray,lw=.5,alpha=.6)
    b.scatter(q[mask]**2,np.log(I[mask]),s=8,color=blue)
    x=np.linspace(0,.8**2,100);b.plot(x,result['intercept']+result['slope_nm2']*x,color=orange,lw=2)
    b.set_ylim(1.65,2.7);b.set_xlabel('q² / nm⁻²');b.set_ylabel('ln I');b.set_title(tr('B  Guinier区域：实心点参与拟合','B  Guinier region: filled points fitted'),loc='left')
    c.scatter(q[mask],(I[mask]-predicted[mask])/sigma[mask],s=10,color=blue)
    c.axhline(0,color=gray);c.set_xlabel('q / nm⁻¹');c.set_ylabel(tr('(观测−预测) / σ','(Observed − predicted) / σ'))
    c.set_title(tr('C  以归档误差为单位的残差','C  Residuals in reported-error units'),loc='left')
    d.plot(windows,sensitivity,color=green,lw=2);d.axvline(.8,color=orange,ls='--')
    d.axhline(1.5,color=gray,ls=':',label=tr('归档页面报告值1.5 nm','Entry-reported value 1.5 nm'))
    d.set_xlabel('qmax / nm⁻¹');d.set_ylabel('Rg / nm');d.set_title(tr('D  改变上限，检查估计稳定性','D  Change upper bound; inspect stability'),loc='left');d.legend(fontsize=9)
    fig.suptitle(tr('真实数据：Darja Ruskule · SASBDB SASDAC2','Measured data: Darja Ruskule · SASBDB SASDAC2'),fontsize=13)
    fig.tight_layout();save(fig,'guinier')
    fig,axs=plt.subplots(1,2,figsize=(12,4.8));a,b=axs
    x=np.linspace(.001,7,900);u=np.sqrt(5/3)*x
    sphere=(3*(np.sin(u)-u*np.cos(u))/u**3)**2
    chain=2*(np.exp(-x*x)-1+x*x)/x**4
    a.plot(x,x*x*sphere,color=green,label=tr('均匀圆球模型','Uniform sphere model'))
    a.plot(x,x*x*chain,color=orange,label=tr('理想高斯链模型','Ideal Gaussian-chain model'))
    a.set_xlabel('q Rg');a.set_ylabel('(q Rg)² I(q) / I(0)');a.legend();a.set_title(tr('A  同一Rg下的模型形状','A  Model shapes at the same Rg'),loc='left')
    high=np.unique(np.r_[np.flatnonzero(q>4.5)[::3],np.flatnonzero((q>4.5)&(I<=0))])
    b.errorbar(q[high],I[high],yerr=sigma[high],fmt='.',color=blue,lw=.5,alpha=.65)
    b.axhline(0,color=gray);b.set_xlabel('q / nm⁻¹');b.set_ylabel(tr('归档强度，线性坐标','Archived intensity, linear scale'))
    b.set_title(tr('B  高q端：负值也属于测量结果','B  High q: negative values remain data'),loc='left')
    fig.tight_layout();save(fig,'shape')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
```

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SASBDB SASDAC2 — Lysozyme in sodium acetate](https://www.sasbdb.org/data/SASDAC2/)

   真实曲线、样品条件与数据库报告尺寸；数据提交者Darja Ruskule。

   SASBDB unrestricted reuse policy; attribution required by community guidance.
2. [SASBDB — About and data-use policy](https://www.sasbdb.org/about/)

   数据复用条件与结构数据库背景。

   Data and models free of copyright restrictions, with original-author attribution requested.
3. [BioXTAS RAW — Guinier analysis](https://bioxtas-raw.readthedocs.io/en/latest/saxs/saxs_guinier.html)

   低q窗口、误差、聚集和拟合质量。

   Public technical reference; no figure reproduced.
4. [SSRL — SAXS data analysis primer](https://www-ssrl.slac.stanford.edu/smb-saxs/content/data-analysis-primer)

   缓冲液匹配、曲线与结构问题的联系。

   Public facility educational reference; no figure reproduced.
5. [Trewhella et al. — 2017 biomolecular SAS reporting guidelines](https://journals.iucr.org/d/issues/2017/09/00/jc5010/index.html)

   Guinier范围、残差、P(r)与结构解释的证据。

   Open scientific reference; no paper figure reproduced.
6. [André Guinier — Personal reminiscences](https://www.iucr.org/what-we-do/publications/books/Fifty-Years-of-X-ray-Diffraction/guinier)

   1938年铝铜合金时效与小角散射的历史联系。

   Historical primary account; original explanatory illustration used.
