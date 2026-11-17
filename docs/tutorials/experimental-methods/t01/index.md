# 差示扫描量热：材料吸热放热时发生了什么

Source: https://ml-biomat.com/tutorials/experimental-methods/t01/
Language: zh-CN

读懂热流中的台阶和峰，把热历史、升温速率与分子结构联系起来。

## 塑料为什么会变软，蛋白质为什么会展开？

把一块巧克力握在手里，它逐渐失去形状；给透明塑料片加热，它可能先变得容易弯曲，再发生更明显的形态变化；一份蛋白质溶液受热后，有时冷却回来仍然保持功能，有时却留下难以恢复的聚集物。这些现象都与能量和分子运动有关，但它们并不是同一种变化。差示扫描量热，简称 DSC，用可控的温度程序观察样品吸收或释放热量的过程。它帮助我们回答材料在什么温度范围发生变化、变化需要多少热，以及此前的加工和储存经历留下了怎样的影响。

对聚合物材料，DSC 常用于比较结晶程度、玻璃化转变、熔融和固化过程。一个可降解支架经过不同冷却方式后，化学组成可以相同，链段排列却不同，随后的力学响应与水分进入方式也可能改变。对生物大分子，DSC 可以观察蛋白质、核酸或脂质结构的热转变，比较缓冲条件和配方如何改变转变曲线。研究者关心的并不只是一个“耐热温度”，而是样品沿着温度变化路径经历了哪些过程，以及这些过程与使用条件有什么联系。

理解 DSC 可以从烧水开始。相同的小火，给不同质量的水升高同样温度，所需时间不同；水到达沸腾阶段，继续输入热量却主要用于状态改变。前一种热量支持温度上升，后一种热量支持相变。DSC 也需要区分这两类贡献，只是样品通常很少，温度程序更精确，并且用参比来比较热量差异。读曲线时，一段基线的高度、一个台阶和一个尖峰各有含义，不能都被叫作“吸热峰”以后再一起寻找峰顶。

本节先解释仪器如何把热交换转为曲线，再用一个明确构造的聚合物复合样品练习玻璃化温度、峰面积和质量归一化。随后把升温速率与真实公开的铟标定结果放在一起，认识测量条件对数值的影响。最后转向蛋白质展开，说明同样是吸热峰，为什么需要不同的样品准备和解释。整条路线围绕一个问题展开：曲线上的每一部分，究竟对应样品怎样的能量变化？

## 两只小容器，怎样测到微小的热量差

“差示”指样品与参比之间的比较，“扫描”指温度随时间按设定程序变化，“量热”指测量热交换。对于许多固体材料实验，样品放在小坩埚中，参比使用匹配的空坩埚。两边都要跟随同一温度程序，样品一侧却多了材料本身的热容量和转变热。通过比较两侧所需的热流，仪器把容器、炉体和背景中的共同贡献尽量减去，让样品的差异表现出来。蛋白质溶液实验常用液体样品池和匹配缓冲液参比，逻辑相同，具体结构和灵敏度有所不同。

1962 年，Watson 与 O’Neill 提交的差示微量量热仪专利提出了一种清楚的控制思路：一套反馈使样品和参比的平均温度跟随程序，另一套反馈调节两侧功率，让它们尽量保持相同温度。记录为补偿样品变化而需要的功率差，就能把热效应转为定量信号。这段仪器史值得放在原理中理解，因为它解释了为什么“测到两边温度不同”和“测到维持温度所需的功率不同”不是同一个读数，也解释了峰面积成为能量尺度的关键。

![原创仪器原理图。A 联系 Watson 与 O’Neill 于 1962 年提交的功率补偿方案；B 表示热流型 DSC 的另一种测量链条。图形不按比例，不复制专利图。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/64eeda46d96a2e34f6e82f53.svg?v=64eeda46d96a)

图 1原创仪器原理图。A 联系 Watson 与 O’Neill 于 1962 年提交的功率补偿方案；B 表示热流型 DSC 的另一种测量链条。图形不按比例，不复制专利图。

另一类常见实现是热流型 DSC。样品和参比通过已知热传导通路与共同热源交换能量，传感器测量两侧温差，再通过标定关系转换为热流差。功率补偿型与热流型的实现不同，但都需要温度标定、热流或焓标定和合适的基线处理。图中的两个原理示意帮助辨认测量链条，没有把不同仪器的内部结构画成同一套装置。使用仪器时，先确认输出究竟是毫瓦、瓦每克，还是已经转换成热容的量，后面的计算才有一致的起点。

热流是单位时间传递的能量，可以理解为“热量流动得多快”。本节把吸热画为向上、放热画为向下；其他软件可能采用相反方向，因此应读轴上的标注。一个 5 mg 样品在每分钟 10 K 的升温程序中，如果比热为每克每开尔文 1.5 J，单纯跟随升温就需要约 1.25 mW 的热流。这样的背景即使没有熔融、结晶或反应也会存在。转变发生时，附加的热效应叠在这个背景上，形成需要进一步分离的峰或台阶。

$$
\dot Q_{\mathrm{base}}=m c_p\beta,\qquad \beta=\frac{dT}{dt}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8988d245a3957f245c21d13b.svg) | 没有转变热时的样品升温热流，W。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 样品质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3dd37e60d36899a1d25331ba.svg) | 定压比热容，J/(g·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 升温速率，K/s；摄氏温差与开尔文温差数值相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 温度；求变化率可使用 K 或 °C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |

每克升高一度所需热量乘以质量和每秒升高度数，得到每秒能量。m=0.005 g、cp=1.5 J/(g·K)、β=10/60 K/s，热流为 0.00125 W，即 1.25 mW。此式描述无转变热且近似均温的升温背景。

这里使用的比热，是单位质量样品升高单位温度所需的热量；整个样品的热容量还要乘以质量。摄氏温差与开尔文温差数值相同，所以每分钟 10 °C 与每分钟 10 K 表示同样的升温速率，但涉及绝对温度的热力学关系必须使用开尔文。这个小小的单位区分经常决定计算能否复现。另一个重要区分是炉体程序温度与样品实际温度：样品、坩埚和传感器之间的热传递需要时间，升温越快，这种响应滞后越值得检查。

## 台阶和峰，讲的是不同的分子故事

聚合物可以有排列较规整的晶区，也可以有缺乏长程规则排列的无定形区域。玻璃化转变主要涉及无定形部分的链段运动：低温下，一些较大范围的局部运动来不及在观察时间内发生；升温后，这些运动逐渐能够响应实验的时间尺度。材料因此可能从较硬的玻璃态进入更柔顺的状态，比热也随之改变。在 DSC 中，这通常表现为基线台阶。它不是所有分子同时从固体变成液体，所以不宜把玻璃化温度当成与纯物质熔点完全同类的常数。

本例用一个平滑台阶描述玻璃化过程，台阶中点为 60 °C，比热增加量为每克每开尔文 0.35 J。读这个温度时，我们明确选择台阶中点；实际报告中也可能使用外推起点、拐点或其他规定方法，它们未必给出相同数值。若样品在玻璃态放置了较长时间，还可能在台阶附近出现焓松弛的恢复峰。这个附加吸热与材料此前如何储存有关，并不意味着那里一定存在一小块晶体熔融。比较首次扫描、受控冷却后的复扫和不同扫描速率，有助于把这些贡献区分开。

熔融对应晶体有序结构的破坏，需要吸收热量；结晶则在适当条件下建立更有序的结构，通常释放热量。某些聚合物冷却得很快，链段来不及充分排列，随后重新加热时却获得了足够的活动能力，于是在熔融之前先结晶。这个发生在升温过程中的放热事件称为冷结晶，其中“冷”不是说样品正在降温。若只看较高温度的熔融面积，就会把扫描途中新形成的晶体也算进样品最初的晶体量。

峰顶、起点和面积也承担不同任务。峰顶描述所选条件下热流变化最强的温度，外推起点用几何方法描述事件开始的温度位置，面积则累计这段过程的能量。聚合物晶体的尺寸、完善程度和重排过程可能让熔融峰变宽，甚至出现肩峰。两个峰也可能来自重结晶和再熔融的叠加，因此不能仅凭峰的数量就断言存在两种化学组分。对疑问最有效的回应通常是改变热历史、升温速率或配合结构测量，而不是立刻给每个肩峰命名。

生物体系又提供另一种故事。蛋白质展开改变了分子内部接触与溶剂相互作用，可能形成明显的吸热峰；脂质膜也可以发生链有序程度改变的转变。它们和聚合物熔融一样会交换热量，却不因此拥有相同的分子机制。DSC 的价值正在于统一测量能量变化，同时要求解释者根据样品组成和实验过程提出合适的结构问题。读曲线的第一步是辨认能量贡献，下一步才是结合其他证据判断其分子来源。

## 样品的过去，和升温的速度，都进入测量

一小片材料进入坩埚以前，已经经历过加工、冷却、拉伸、储存和吸水。首次升温保留了这些经历对当前状态的影响，因此适合回答“收到的样品是什么状态”。若将材料充分熔融，再按照共同程序冷却并复扫，就可以比较共同热历史下的行为。第二次扫描并不会自动比第一次更真实，它回答的是另一个问题。对于发生降解、交联或不可逆化学变化的样品，第一次升温甚至改变了材料组成，不能把复扫简单称为去除历史后的同一材料。

称量和装样决定热量如何归一化，也影响热传递。样品应能代表要比较的材料，质量记录要与实际进入仪器的那一份对应。薄片尽量与坩埚形成适当接触，过厚或堆积不均的样品可能产生内部温差。坩埚材质、盖子、密封方式和气氛应根据目标过程选择：挥发组分需要考虑逸出与压力，氧化研究需要明确气体条件，吸湿材料需要记录含水状态。空白坩埚与装样坩埚之间的匹配也影响启动阶段和基线。

温度与热量需要分别建立量值联系。熔融温度已知的参考物质可以检验温度轴；已知转变焓、准确质量和适当积分方法可以检验热量尺度。铟常用于这类标定，NIST 的公开报告进一步展示了不同名义升温速率下的估计结果。图中重绘的是报告表 4 的模型后验均值及 95% 可信区间，零速率位置的 28.58 J/g 是外推的平衡值，并不是仪器在不升温的情况下完成了一条熔融扫描。保留这种数据定义，才能正确理解误差棒和横轴。

![A 是构造的 8 s 一阶热响应模型，完整转变热保持约 45 J/g。B 依据 Fortin 等的 NIST SP 260-242 表 4 重绘公开数值：点为后验均值，误差棒为原表 95% 可信区间，零速率点为外推结果。NIST 政府研究数据，保留署名与原始数值。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d0c1ed9bd123bf05770fa4ac.svg?v=d0c1ed9bd123)

图 2A 是构造的 8 s 一阶热响应模型，完整转变热保持约 45 J/g。B 依据 Fortin 等的 NIST SP 260-242 表 4 重绘公开数值：点为后验均值，误差棒为原表 95% 可信区间，零速率点为外推结果。NIST 政府研究数据，保留署名与原始数值。

这个滞后模型在完整积分时保留孤立事件的总热量：能量只是向稍后的时间重新分布，并没有消失。如果积分窗口过窄，延迟的峰尾会被漏掉，尤其可能使快速扫描的面积显得较小。实际检查时，应先比较足够覆盖完整响应的区间，再判断面积变化是否反映材料差异；同时，扩大区间也可能包含邻近事件或更不确定的背景。合适的边界需要由曲线回到可信基线的位置及附近过程共同支持，把积分边界画在原始曲线上，读者便能直接检查这一选择。

升温速率改变的是观察过程中的时间安排。更快升温时，同样的温度区间用时更短，单位时间需要交换的热量往往更大，峰看起来也更高；与此同时，样品跟随程序的滞后可能更加明显。本例为一个积分热量 45 J/g 的构造熔融峰加入 8 s 一阶响应，升温速率分别为每分钟 5、10 和 20 °C，得到峰顶约 165.65、166.25 和 167.25 °C。三个峰位置不同，完整积分后却都接近 45 J/g。这是把热响应效应单独拿出来观察的模型，实际材料还可能随速率改变结晶或反应路径。

实际比较可以从一组共同条件开始，再针对问题改变一个因素。若怀疑峰移动来自热滞后，比较较小样品量和较慢扫描；若怀疑冷结晶受前期冷却影响，比较明确规定的冷却程序；若出现意外吸热，检查前后质量和含水状态。不同因素的比较需要保留原始曲线，而不是只保存自动输出的温度。这样，热历史、传热和材料转变各自改变了什么，就能够沿着实验记录逐一判断。

## 从毫瓦曲线算到每克热量与结晶比例

本节的聚合物例子使用一个假想复合样品，质量 5 mg，聚合物质量分数为 0.8，另有 0.2 的惰性填料。程序以每分钟 10 °C 从 20 °C 升至 200 °C，构造了 60 °C 附近的玻璃化台阶、110 °C 附近的冷结晶放热和 165 °C 附近的熔融吸热。设定的冷结晶热量为每克复合样品 20 J，熔融热量为每克复合样品 45 J。这些数值用于解释分析步骤，不对应某一种已测量的商业聚合物。

![全部为构造的假想复合样品，随机种子 710，质量 5 mg、升温速率 10 °C/min、聚合物质量分数 0.8。吸热向上。A 保留比热背景，B 拟合玻璃化台阶中点，C 标出积分区间，D 分别展示不同质量基准的计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1717459391c225bc80740751.svg?v=1717459391c2)

图 3全部为构造的假想复合样品，随机种子 710，质量 5 mg、升温速率 10 °C/min、聚合物质量分数 0.8。吸热向上。A 保留比热背景，B 拟合玻璃化台阶中点，C 标出积分区间，D 分别展示不同质量基准的计算。

程序先减去构造的仪器背景，然后在玻璃化附近拟合比热台阶，得到中点约 60.005 °C、比热增量约每克每开尔文 0.3505 J。较高温度的峰分析使用转变两侧选定区间拟合局部线性基线，再对冷结晶和熔融区域分别积分。由于图的横轴是温度，面积的单位是毫瓦乘温度；必须除以升温速率，才能把温度间隔换成时间间隔，再将功率乘时间转为热量。最后除以样品质量，得到便于不同样品比较的每克焓变。

$$
\Delta h=\frac{1}{m}\int_{t_a}^{t_b}[\dot Q(t)-\dot Q_0(t)]\,dt=\frac{1}{m\beta}\int_{T_a}^{T_b}[\dot Q(T)-\dot Q_0(T)]\,dT
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a7f92a6abd1defda3a545b43.svg) | 按样品质量归一化的转变焓，J/g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 实际用于归一化的样品质量，g。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cee984b0ecbc9ab32f893bae.svg) | 已校正仪器背景的样品热流，W。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fd724bd870304f04c8bb030e.svg) | 无该转变时估计的样品热流基线，W。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | 时间与积分起止时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/536ddb365f804465fe425907.svg) | 温度及对应积分边界，°C 或 K；使用一致的温差单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 恒定升温速率，K/s。 |

功率乘时间给出热量；恒速升温时 dt=dT/β。一个面积 0.0375 W·K 的吸热事件，m=0.005 g、β=1/6 K/s，得到 45 J/g。若积分轴用分钟或功率用毫瓦，应先换单位。

本例输出的熔融热量约为 45.03 J/g，冷结晶热量约为 19.74 J/g。它们与设定值的差别来自噪声、有限积分窗口，以及峰尾对所选基线区间的影响。基线不是画在峰下面的一根装饰线，而是对“没有该转变时应有多少热流”的估计。仅仅把一个 40 °C 宽积分区间的基线整体错移 0.01 mW，在本例质量和速率下，就会使焓变相差 0.48 J/g。比较很小的样品差异时，这个尺度比图上的视觉接近程度更有意义。

计算初始结晶比例还需要两次澄清。首先，熔融时消耗的热量包括最初已有晶体和扫描中新增晶体的贡献，所以在适用的近似下应减去冷结晶热量的正值幅度。其次，这里的峰面积已经按整个复合样品质量归一化，而我们希望得到聚合物部分内部的结晶比例，就要再除以聚合物质量分数。填料不参与这些峰、相应转变可分离且参考熔融焓合适时，才与这个质量平衡相符。不同晶型、显著重排或反应重叠，需要相应的结构与基线分析。

$$
X_c=\frac{\Delta h_m-\Delta h_{cc}}{w_p\Delta h_m^\circ}\times100\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9452df3acfb36a01b9d75cca.svg) | 聚合物部分的初始结晶质量比例，%。 |
| ![Formula](https://ml-biomat.com/static/agent-math/45af6b60faf81f9352c1a2a6.svg) | 熔融热量的正值，按整个复合样品质量计，J/g 样品。 |
| ![Formula](https://ml-biomat.com/static/agent-math/428a3c64b2d849b0d41d859f.svg) | 冷结晶放热的正值幅度，J/g 样品。 |
| ![Formula](https://ml-biomat.com/static/agent-math/59c3b11c729fa3704eef4875.svg) | 样品中聚合物质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/37c105232a9ed6408e184706.svg) | 适合该聚合物和晶型的完全结晶参考熔融焓，J/g 聚合物。 |

先扣扫描期间新结晶贡献，再换成每克聚合物，最后与完全结晶参考量比较。假想模型设 Δhm=45、Δhcc=20 J/g 样品，wp=0.8、参考100 J/g 聚合物，得31.25%。填料无重叠转变，热事件可分离，参考量与结构相符。

这里还要分清两种基线：仪器空白描述测量系统和容器产生的偏移，转变基线描述样品在没有所积分事件时的热容量贡献。减去前者，并不会自动减去后者。本例高温区的比热近似线性，因而适合用局部直线估计；若样品熔融前后的比热明显不同，就需要相应的基线构造。比较几种有物理依据的基线，并记录积分改变多少，可以把计算敏感性与所用假设直接联系起来。

为了让分母清楚，本例把完全结晶参考聚合物的熔融焓设为 100 J/g 聚合物。用理想输入值计算，先用 45 减去 20，得到每克复合样品中最初晶体的 25 J，再除以 0.8，得到每克聚合物的 31.25 J，最后与 100 J/g 参考值相比，得出 31.25%。使用实际数值处理结果得到约 31.62%。图中的三根柱依次展示只取熔融、扣除冷结晶、再按聚合物质量归一化的差别；每一步改变的都是一个明确的物理定义。

下面的交互让读者改变样品质量、升温速率和基线偏移。理想材料的熔融焓保持不变，样品更重或升温更快时，毫瓦峰会更高；正确完成质量和时间换算后，结果仍应接近同一个每克热量。再加入小基线偏移，可以看到同样的仪器偏差对不同质量和扫描速率的影响不同。这个实验把“峰大”与“材料每克需要更多热量”分开，也让积分的单位换算具有直接可见的结果。

## 峰变高，是否意味着每克热量变多？

固定熔融焓 45 J/g、峰中心 165 °C、宽度参数 5 °C。积分区间 145–185 °C。改变质量与速率，再改变估计基线相对真实基线的偏移；正偏移表示基线估计偏高。

[Figure: 质量速率与基线对热流和积分的影响](https://ml-biomat.com/tutorials/experimental-methods/t01/#T01-plot)

## 蛋白质的吸热峰，怎样与展开比例联系起来

测量蛋白质溶液时，水和缓冲组分的热容量远大于少量蛋白质的差异信号，因此样品与参比缓冲液的匹配尤为重要。透析后的外液或合适的色谱流出缓冲液，可以帮助建立组成相近的参比。蛋白质浓度、有效池体积和分子量决定如何把总热量转换为每摩尔蛋白质的焓变。若样品发生吸附、沉淀或聚集，实际参与扫描的分子状态也会变化。因此，溶液澄清程度、重复扫描和扫描后样品状态都可以为热曲线提供必要的背景。

先考虑一个可逆、达到平衡的两态模型：每个蛋白质处于折叠态或展开态，展开焓在所考察温区近似不变，两态热容差设为零。温度升高时，展开态所占比例逐渐增加。模型中点温度为 60 °C，在这里两态比例各一半。这个模型的作用是把“结构群体随温度变化”与“测到额外热容量”明确连接；真实蛋白质可能有多个结构域、中间态或聚集过程，需要根据实验特征调整描述。

$$
K(T)=\exp\!\left[-\frac{\Delta H}{R}\left(\frac{1}{T}-\frac{1}{T_m}\right)\right],\qquad f_U(T)=\frac{K(T)}{1+K(T)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5287b9b7382426f155625e11.svg) | 展开态与折叠态的平衡比例之比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | 模型中近似恒定的摩尔展开焓，J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 气体常数，8.314462618 J/(mol·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d02c1a55a2052315ebe68af2.svg) | 两态等比例时的模型中点温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/38d847ee4f90227f3c1be623.svg) | 展开态分子比例，无量纲。 |

可逆、达到平衡的两态模型，ΔH在温区内不变、两态热容差设为零；由 van’t Hoff 关系以中点为参照得到比例。T=Tm=333.15 K 时指数为零，K=1，展开比例0.5。模型不把聚集或中间态并入这个比例。

每升高一点温度，如果有一批分子从折叠态转为展开态，就需要额外提供相应的展开热。因此，展开比例随温度变化最快的区域会出现热容峰。峰下面按温度积分，累计的是这些分子完成展开所需的热量。本例设定每摩尔展开焓为 200 kJ，在 20 至 100 °C 区间积分得到约 199.90 kJ/mol；稍小的数值是因为有限温区两端尚有极少比例没有完成从一个极限到另一个极限的变化。

$$
C_{p,\mathrm{ex}}=\Delta H\frac{df_U}{dT}=\frac{\Delta H^2}{RT^2}f_U(1-f_U),\qquad \Delta H_{\mathrm{cal}}=\int_{T_a}^{T_b}C_{p,\mathrm{ex}}\,dT
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/496ef11b49251e78d3f0c9e2.svg) | 扣除状态热容基线后的过量摩尔热容，J/(mol·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | 两态模型的摩尔展开焓，J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9fd90fe44c80ea5fc0ca6d2e.svg) | 展开比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/536ddb365f804465fe425907.svg) | 绝对温度及积分边界，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 气体常数，J/(mol·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7fbff5e5f098490dbfa519f3.svg) | 在所选温区积分得到的量热焓，J/mol。 |

每升高一度时新展开的分子比例乘以每摩尔展开热，给出额外热容。ΔH=200000 J/mol、Tm=333.15 K、中点 fU=0.5，额外热容约10.84 kJ/(mol·K)。20–100 °C 积分约199.90 kJ/mol，有限边界略未覆盖全部转变。

![构造的可逆两态蛋白质模型，中点温度 333.15 K，展开焓 200 kJ/mol，两态热容差设为零。右侧虚线仅表示 20% 分子恢复后的复扫幅度，不对应特定聚集反应模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/62a25ed03ba65684185832af.svg?v=62a25ed03ba6)

图 4构造的可逆两态蛋白质模型，中点温度 333.15 K，展开焓 200 kJ/mol，两态热容差设为零。右侧虚线仅表示 20% 分子恢复后的复扫幅度，不对应特定聚集反应模型。

复扫能把“受热发生过变化”和“冷却后恢复了什么”联系起来。若样品冷却后充分回到原来的状态，重复扫描可以再次出现相近的转变热；若只有部分分子恢复，峰面积可能减小。图中的虚线简单表示只有 20% 分子恢复时的示意热容，并没有据此拟合一种具体聚集机制。相似的复扫曲线是恢复性的证据，进一步检查扫描速率和浓度依赖，才能判断所用平衡模型是否适合。某些过程即使看起来可重复，也可能在快速扫描中偏离平衡。

峰的位置和峰的面积需要一起读。改变缓冲液后，转变温度可能提高，而热量、峰宽或复扫恢复程度也同时改变；这些信息对应不同方面的行为。配方研究还要考虑使用温度下的长期变化、活性保持和聚集速率，不能把一次升温中的峰顶直接当作保存寿命。DSC 在这里提供的是一条具体温度路径上的热响应，结合结构、活性和粒径测量，能把配方比较转成更清楚的机制问题。

## 把完整计算用于一项材料或配方比较

完整程序输出四组图、聚合物扫描的逐点数据、不同升温速率下的峰位置与积分结果，以及蛋白质的展开比例和过量热容。铟数据保存在随例子提供的表格中，程序直接读取并重绘公开报告中的估计值和区间。构造数据与真实公开统计结果采用清楚的图注区分：前者用来逐项控制变量、检验计算，后者展示实际计量研究如何报告速率与不确定度。运行所需的数据已经随代码提供，分析过程可以离线重复。

### 完整热流、结晶分析与蛋白质展开计算

执行基线处理、台阶拟合、积分与质量归一化，比较升温速率和公开铟数据，输出所有图和逐点结果。

```
"""DSC: constructed heat-flow analysis plus published NIST indium estimates."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.special import expit
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

def gaussian(x,center,width):return np.exp(-.5*((x-center)/width)**2)/(width*np.sqrt(2*np.pi))
def cp_model(t,a,b,step,tg,width):return a+b*(t-20)+step*expit((t-tg)/width)
def lagged_peak(t,rate,mass_mg=5,heat=45,tau=8):
 beta=rate/60;ideal=mass_mg*beta*heat*gaussian(t,165,5);alpha=np.exp(-(t[1]-t[0])/beta/tau);return ideal,lfilter([1-alpha],[1,-alpha],ideal)
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);T=lambda z,e:z if a.language=='zh' else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 t=np.linspace(20,200,3601);mass=.005;beta=10/60;cp=cp_model(t,1.2,.002,.35,60,1.5);instrument=.03+.0001*t;baseline=1000*mass*beta*cp;cc=-20*gaussian(t,110,7);melt=45*gaussian(t,165,5);rng=np.random.default_rng(710);raw=instrument+baseline+1000*mass*beta*(cc+melt)+rng.normal(0,.002,len(t));corrected=raw-instrument
 mask=(t>=40)&(t<=80);params,_=curve_fit(cp_model,t[mask],corrected[mask]/(1000*mass*beta),p0=[1.2,.002,.35,60,1.5]);estimated_cp=cp_model(t,*params)
 # Local baselines use transition-free sidebands. The ideal heat-capacity trend is linear well above Tg.
 side=((t>=85)&(t<=90))|((t>=132)&(t<=138))|((t>=140)&(t<=145))|((t>=185)&(t<=195));poly=np.polyfit(t[side],corrected[side],1);local=np.polyval(poly,t);excess=corrected-local
 mcc=(t>=90)&(t<=132);mm=(t>=145)&(t<=185);hcc=-np.trapezoid(excess[mcc],t[mcc])/(1000*mass*beta);hm=np.trapezoid(excess[mm],t[mm])/(1000*mass*beta);xc=(hm-hcc)/(.8*100)*100
 f,axes=plt.subplots(1,2,figsize=(13.7,5.4),layout='constrained')
 for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
 ax=axes[0];ax.set_title(T('A  1962：分别调节功率，保持两侧等温','A  1962: Adjust power to equalize temperatures'),loc='left');ax.add_patch(Rectangle((.7,1.8),8.6,5,fc='#edf0ee',ec='#7e929d'))
 for x,label,col in [(1.5,T('样品','Sample'),R),(6,T('参比','Reference'),B)]:
  ax.add_patch(Rectangle((x,4),2.5,1.3,fc='#e0e7e8',ec=col));ax.text(x+1.25,4.65,label,ha='center');ax.plot([x+.2,x+.6,x+1,x+1.4,x+1.8,x+2.2],[3,3.5,3,3.5,3,3.5],c=col,lw=2);ax.annotate('',xy=(x+1.25,4),xytext=(x+1.25,3.55),arrowprops={'arrowstyle':'->','color':col});ax.text(x+1.25,2.4,T('独立加热器','Separate heater'),ha='center',fontsize=10)
 ax.text(5,6.1,T('温度反馈 → 差分功率','Temperature feedback → differential power'),ha='center',fontsize=11);ax.text(5,.6,T('Watson 与 O’Neill 的功率补偿思想\n原创原理图，非专利图复制','Watson and O’Neill: power-compensation concept\nOriginal schematic, not a patent-figure reproduction'),ha='center',fontsize=10)
 ax=axes[1];ax.set_title(T('B  另一种实现：共同热源与热流通路','B  Another implementation: shared source and heat paths'),loc='left');ax.add_patch(Rectangle((1,1.8),8,1,fc='#ead4ba',ec=Y));ax.text(5,2.3,T('受程序控制的热源','Programmed heat source'),ha='center')
 for x,label,col in [(1.5,T('样品','Sample'),R),(6,T('参比','Reference'),B)]:
  ax.add_patch(Rectangle((x,4.2),2.5,1.3,fc='#e0e7e8',ec=col));ax.text(x+1.25,4.85,label,ha='center');ax.annotate('',xy=(x+1.25,4.2),xytext=(x+1.25,2.9),arrowprops={'arrowstyle':'->','color':col,'lw':3})
 ax.text(5,6.4,T('测量温差，经标定得到热流差','Measure temperature difference; calibrate to heat flow'),ha='center',fontsize=10);ax.text(5,.6,T('热流型 DSC：原理示意，尺寸不按比例','Heat-flux DSC: principle schematic, not to scale'),ha='center',fontsize=10);save(f,'instrument-history')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.4),layout='constrained');ax=axes[0,0];ax.plot(t,raw,c=B,label=T('原始构造信号','Constructed raw signal'));ax.plot(t,baseline+instrument,c='#6b7f8a',ls='--',label=T('无转变热的基线','Baseline without transition heat'));ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('热流 / mW；吸热向上','Heat flow / mW; endothermic up'),title=T('A  台阶、放热峰与吸热峰','A  Step, exotherm and endotherm'));ax.legend(fontsize=9)
 ax=axes[0,1];ax.scatter(t[mask][::8],corrected[mask][::8]/(1000*mass*beta),s=8,c=Y,label=T('表观比热','Apparent specific heat'));ax.plot(t[mask],estimated_cp[mask],c=B,label=T('台阶拟合','Step fit'));ax.axvline(params[3],c=R,ls='--');ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('比热 / J/(g·K)','Specific heat / J/(g·K)'),title=T(f'B  玻璃化台阶中点 {params[3]:.2f} °C',f'B  Glass-step midpoint {params[3]:.2f} °C'));ax.legend(fontsize=9)
 ax=axes[1,0];ax.plot(t,excess,c=B);ax.fill_between(t,0,excess,where=mcc,color=G,alpha=.3,label=T(f'冷结晶 {hcc:.2f} J/g',f'Cold crystallization {hcc:.2f} J/g'));ax.fill_between(t,0,excess,where=mm,color=R,alpha=.3,label=T(f'熔融 {hm:.2f} J/g',f'Melting {hm:.2f} J/g'));ax.set(xlim=(80,195),xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('扣基线热流 / mW','Baseline-subtracted heat flow / mW'),title=T('C  积分面积需除以升温速率','C  Temperature-axis area needs the heating rate'));ax.legend(fontsize=9)
 ax=axes[1,1];labels=[T('熔融直接比值','Melting alone'),T('扣冷结晶，样品基准','Subtract cold\ncrystallization'),T('再按聚合物质量归一','Polymer-mass\nnormalization')];vals=[hm/100*100,(hm-hcc)/100*100,xc];ax.bar(range(3),vals,color=[R,Y,B],width=.58);ax.set_xticks(range(3),labels,fontsize=9);ax.set(ylabel=T('计算结果 / %','Calculated result / %'),ylim=(0,65),title=T('D  分母改变，物理含义也改变','D  The denominator changes the meaning'))
 for i,v in enumerate(vals):ax.text(i,v+1,f'{v:.2f}%',ha='center',fontsize=10)
 save(f,'heat-flow-analysis')
 nist=np.genfromtxt(Path(__file__).parent/'data/nist_indium_table4.csv',delimiter=',',names=True);f,axes=plt.subplots(1,2,figsize=(13.7,5.5),layout='constrained');rate_rows=[]
 for rate,col in [(5,G),(10,B),(20,R)]:
  ideal,measured=lagged_peak(t,rate);peak=float(t[np.argmax(measured)]);heat=float(np.trapezoid(measured,t)/(1000*mass*(rate/60)));rate_rows.append([rate,peak,heat]);axes[0].plot(t,measured,c=col,label=T(f'{rate} °C/min；峰 {peak:.2f} °C',f'{rate} °C/min; peak {peak:.2f} °C'))
 axes[0].set(xlim=(145,190),xlabel=T('程序温度 / °C','Program temperature / °C'),ylabel=T('转变热流 / mW','Transition heat flow / mW'),title=T('A  构造模型：8 s 热响应滞后','A  Constructed model: 8-second thermal response'));axes[0].legend(fontsize=9)
 ax=axes[1];mean=nist['posterior_mean_J_per_g'];ax.errorbar(nist['heating_rate_C_per_min'],mean,yerr=[mean-nist['lower95_J_per_g'],nist['upper95_J_per_g']-mean],fmt='o',color=B,capsize=4);ax.axhline(28.58,c=G,ls=':',label=T('零速率外推 28.58 J/g','Zero-rate extrapolation: 28.58 J/g'));ax.set(xlabel=T('名义升温速率 / °C/min','Nominal heating rate / °C/min'),ylabel=T('熔融焓估计 / J/g','Estimated fusion enthalpy / J/g'),title=T('B  真实公开结果：NIST 铟标准物质','B  Published results: NIST indium reference material'));ax.legend(fontsize=9,loc='upper left');ax.text(.25,.05,T('表 4 后验均值与 95% 可信区间\n不是五条原始扫描的峰面积','Table 4 posterior means and 95% credible intervals\nNot peak areas from five individual scans'),transform=ax.transAxes,fontsize=9);save(f,'scan-rate-calibration')
 pt=np.linspace(20,100,1601);kel=pt+273.15;H=200000.;Tm=333.15;gas=8.31446261815324;frac=expit(-H/gas*(1/kel-1/Tm));cex=H**2/(gas*kel**2)*frac*(1-frac)/1000;integral=np.trapezoid(cex,pt)
 f,axes=plt.subplots(1,2,figsize=(13.7,5.4),layout='constrained');ax=axes[0];ax.plot(pt,frac,c=B,label=T('展开比例','Unfolded fraction'));ax.axvline(60,c='#71818b',ls=':');ax.axhline(.5,c='#71818b',ls=':');ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('展开分子比例','Fraction unfolded'),title=T('A  构造的可逆两态平衡','A  Constructed reversible two-state equilibrium'));ax.legend(fontsize=10)
 ax=axes[1];ax.plot(pt,cex,c=R,label=T('首次扫描 / 完全恢复后的复扫','First scan / rescan after full recovery'));ax.plot(pt,.2*cex,c=B,ls='--',label=T('仅 20% 分子恢复的复扫示意','Illustrative rescan with only 20% recovered'));ax.fill_between(pt,0,cex,color=R,alpha=.1);ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('过量摩尔热容 / kJ/(mol·K)','Excess molar heat capacity / kJ/(mol·K)'),title=T('B  面积计热，复扫考察恢复','B  Area measures heat; rescanning probes recovery'));ax.legend(fontsize=8);ax.text(.04,.65,T(f'20–100 °C 积分：{integral:.2f} kJ/mol\n参数 ΔH=200 kJ/mol；ΔCp=0',f'Integral, 20–100 °C: {integral:.2f} kJ/mol\nModel ΔH=200 kJ/mol; ΔCp=0'),transform=ax.transAxes,fontsize=9);save(f,'protein-unfolding')
 np.savetxt(a.output/'polymer_scan.csv',np.c_[t,(t-20)/beta,raw,instrument,corrected,baseline,local,excess],delimiter=',',header='temperature_C,time_s,raw_mW,instrument_mW,corrected_mW,true_cp_baseline_mW,fitted_local_baseline_mW,excess_mW',comments='');np.savetxt(a.output/'scan_rate.csv',rate_rows,delimiter=',',header='rate_C_per_min,peak_temperature_C,integrated_heat_J_per_g',comments='');np.savetxt(a.output/'protein.csv',np.c_[pt,frac,cex,.2*cex],delimiter=',',header='temperature_C,unfolded_fraction,excess_Cp_kJ_per_mol_K,rescan20percent_kJ_per_mol_K',comments='')
 summary={'glass_midpoint_C':float(params[3]),'specific_heat_step_J_per_g_K':float(params[2]),'melting_heat_J_per_g_sample':float(hm),'cold_crystallization_heat_J_per_g_sample':float(hcc),'initial_polymer_crystallinity_percent':float(xc),'ideal_initial_polymer_crystallinity_percent':31.25,'baseline_offset_heat_error_J_per_g':.01/1000*40/beta/mass,'protein_unfolded_fraction_at_60C':float(frac[np.argmin(abs(pt-60))]),'protein_integrated_heat_kJ_per_mol':float(integral),'nist_zero_rate_enthalpy_J_per_g':float(mean[0]),'rate_peak_temperatures_C':[row[1] for row in rate_rows],'rate_integrals_J_per_g':[row[2] for row in rate_rows]};(a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
```

第一次运行后，可以先只检查单位。把 5 mg 换成 0.005 g，把每分钟 10 K 换成每秒六分之一 K，确认毫瓦积分转成焦耳时还有千分之一的换算。然后改变基线区间，查看冷结晶热量和结晶比例如何变化。这个步骤比增加拟合小数位更有助于理解结果。最后比较速率诊断中的三条曲线：它们峰高和峰温不同，但经过正确换算的积分接近一致，说明图形外观与累计热量是两个可以分别检查的量。

若目标是比较不同冷却条件下的可降解材料，可以把首次升温保留为实际加工状态的测量，再增加统一热历史的复扫，结合质量分数和结晶峰解释差异。若目标是筛选蛋白质缓冲液，应同时查看转变曲线、复扫恢复和浓度或速率变化，并把最有希望的条件接到活性与储存实验中。若主要问题是加热时样品是否失去水、溶剂或分解产物，下一节的热重分析会直接跟踪质量，为 DSC 中的热事件增加另一条证据线。

一份可复查的 DSC 结果应让读者找到样品质量和状态、坩埚与气氛、温度程序、使用哪次扫描、吸放热方向、基线与积分边界，以及最终归一化的分母。玻璃化温度说明采用的判定方法，结晶比例说明参考熔融焓和聚合物质量基准，蛋白质焓变说明浓度与摩尔换算。把这些定义与曲线放在一起，材料的热行为才从一个孤立峰值变成能够连接加工、结构和应用的问题答案。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/T01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Watson & O’Neill: Differential microcalorimeter, US3263484A](https://patents.google.com/patent/US3263484A/en)

   功率补偿反馈与历史。
2. [TA Instruments: Interpreting Unexpected Events and Transitions in DSC Results, TA039](https://www.tainstruments.com/pdf/literature/TA039.pdf)

   水分、松弛、热历史和基线。
3. [TA Instruments: DSC and MDSC Online Training, Applications](https://www.tainstruments.com/wp-content/uploads/2020-DSC-Online-Training-Part-2-1.pdf)

   峰面积、冷结晶和晶体重排。
4. [TA Instruments: Determination of Polymer Crystallinity by DSC, TA123](https://www.tainstruments.com/applications-notes/thermal-analysis-application-brief-determination-of-polymer-crystallinity-by-dsc/)

   热流原理与共同热历史比较。
5. [Malvern: DSC Theory and Practice](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp140701-dsc-theory-and-practice)

   匹配缓冲、展开热容、复扫与速率依赖。
6. [Fortin et al. (2024): NIST SP260-242, Indium SRM2232a](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-242.pdf)

   表4的公开铟标定估计和可信区间。

   NIST-authored U.S. government research; Table 4 numeric values redrawn with credit, no third-party artwork reused.
7. [NIST: Copyrights and Disclaimers](https://www.nist.gov/copyrights-disclaimers)

   公开政府研究数据的复制与署名规则。
