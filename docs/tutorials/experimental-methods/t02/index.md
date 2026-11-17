# 热重分析：质量变化中的组成与稳定性

Source: https://ml-biomat.com/tutorials/experimental-methods/t02/
Language: zh-CN

让每一份失重都有去向：从水分、残炭与灰分，到温度和时间共同决定的稳定性。

## 一块材料变轻以后，离开的究竟是什么

拿到一片含矿物颗粒的生物高分子薄膜，我们常会问三个看似简单的问题：它吸了多少水，里面有多少有机物，受热以后还能留下什么？称一次质量只能得到总数，就像称一个装满物品的行李箱，无法知道衣服、水瓶和金属配件各占多少。热重分析把称量变成连续观察：让样品经历规定的温度和气氛，同时记录质量如何改变。随着水分蒸发、有机物分解或炭被氧化，曲线上会出现下降区间与暂时平稳的台阶。实验的价值来自这些质量变化与实验条件之间的对应关系，而不只是终点剩下的一个百分数。

热重分析常缩写为 TGA，记录的质量轨迹称为 TG 曲线。它与上一节的差示扫描量热测量不同：DSC 关注热量如何进出样品，TGA 关注留在坩埚里的质量。冰熔化时吸收热量，水仍留在容器中，质量可以不变；水蒸发并离开容器时，质量才会下降。聚合物的玻璃化和熔融也可能没有明显失重，因此把一条平坦 TG 曲线解释成“材料内部没有变化”，就会漏掉结构重排。把热流与质量放在共同的温度轴上，才能区分吸热伴随挥发，还是仅发生相态变化。

对材料研究，TGA 可以帮助比较涂层的挥发组分、复合材料的有机与无机比例，以及同一配方在不同气氛中的失重过程。对生物相关样品，它可用于理解干燥支架中的水分、矿化材料中的有机基质，或药物晶体中的结晶水。这里的“水”还需要进一步区分：表面吸附水、孔隙中的水与进入晶体结构的水，结合环境不同，释放过程也可能不同。温区给出线索，确定化学身份则需要结合已知组成、反应计量以及逸出气体的红外或质谱信号。

阅读本节时，可以始终带着一个问题：天平看到的这份变化，是样品中原本就有的一份物质，还是加热过程中生成、随后又离开的一份产物？这一区别会决定聚合物含量、炭黑含量和灰分能否正确计算。我们将用一个已知配方的构造样品贯穿全章，让每一份质量都有明确去向；然后再用草酸钙一水合物说明，如何通过化学式与台阶高度互相核对。最后考察升温速率与保温时间，理解“开始失重的温度”为什么必须连同测量程序一起读。

## 连续称量的巧思：把天平放进一个可控制的环境

早期分析常把物质加热一段时间，冷却，取出称量，再继续加热。这样的做法能得到若干点，却会打断反应，还可能让样品在冷却和转移时重新吸水或接触空气。二十世纪早期 Honda 与 Saito 等人的热天平工作，把连续称量、受控加热与气氛联系起来。Saito 的早期论文讨论了不同气体、连续升温以及分段保温的作用。这段历史说明，热重仪的关键进步不仅是天平变得更灵敏，更是把“什么时候称、在什么环境中称”变成了可记录和比较的实验条件。

现代热重仪通常包括微量天平、样品坩埚、炉体、温度测量元件和气路。样品质量经支撑结构传到天平，炉体负责实施升温程序，气流则决定反应环境并带走逸出产物。图中的杠杆结构是原理示意，帮助我们看清这些功能如何连接；实际仪器也可采用不同的悬挂与反馈结构。氮气常用于观察热解，即供氧较少时的热分解；空气则能让某些炭质残余进一步氧化。两种气氛下出现不同轨迹，是化学环境改变了反应路径，不是同一条曲线被简单平移。

![原创原理图，联系 Honda、Saito 的早期连续热称量工作；不按比例，不复制历史装置。右图为构造样品的温度与气氛程序。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7260a32fd646502712f02582.svg?v=7260a32fd646)

图 1原创原理图，联系 Honda、Saito 的早期连续热称量工作；不按比例，不复制历史装置。右图为构造样品的温度与气氛程序。

天平同时受样品与周围气体影响。热气体密度变化会改变浮力，气流会带来机械作用，切换氮气和空气也可能造成读数瞬变。因此常用相同坩埚、气流、升温和换气程序记录空白，再处理相应背景。这个空白好比给厨房秤上的空碗去皮，但更复杂：碗周围的空气在整个实验中持续变化，所以背景是一条随时间变化的轨迹。我们保留空白原始记录，尤其查看气体切换附近，而不是把那里的短促尖峰立即解释为一种新组分。

装样也会改变曲线。较厚的一堆粉末可能内部升温较慢，逸出气体需要穿过较长路径；同样质量铺成薄层时，传热和传质条件会不同。坩埚材料、是否加盖、样品粒度、气流与温度程序都应围绕问题选择，并随结果记录。对易吸湿样品，称量到开始测试之间的等待时间也会改变初始状态。比较两种支架时，先规定它们是原样、恒湿平衡后，还是经过同一干燥处理，再谈含水量差异，才能让分母代表相同的物理对象。

## 从质量轨迹到失重速率：先看台阶，再看峰

质量变化还可能朝上。比如某些金属粉末与氧气反应，氧进入固体产物，天平便记录增重；如果氧化与挥发同时发生，读数是两者的净结果，甚至可能暂时接近平坦。因而失重少不总意味着反应少，增重也不应先被当成仪器错误。把气氛、可能反应和空白放在一起检查，就能决定下一步是核对氧化物形成，还是排查浮力与气流背景。对于同时存在增重和失重的过程，先保留带符号的质量轨迹，比强行把所有事件都转换成向上的“分解峰”更便于理解。

为了比较不同装样量，常把初始质量设为百分之百。假设独立称得初始质量为 10 mg，某时刻还剩 9.2 mg，剩余比例就是百分之九十二，之前已损失百分之八。这种归一化把毫克变成比例，但没有消除初始状态的差异。若另一个人先把样品干燥后再称重，他的百分之百就对应不同对象。因此报告“残余百分之二十”时，应说明是相对于原始湿样、干样，还是有机组分。归一化不是一种自动统一实验的操作，它只是把选择好的分母写进计算。

$$
w(t)=\frac{m(t)}{m_0},\qquad L_{a\to b}=\frac{m(t_a)-m(t_b)}{m_0}\times100\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/270613e026ede7b90829cf4d.svg) | 时刻 t 的剩余质量比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | 校正背景后的样品质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 规定初始状态下的样品质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | 时间与所选阶段起止时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3b6a7273a3af8b17fc5a7bab.svg) | 该阶段相对于初始质量的失重百分数，%。 |

共同分母使各阶段成为同一份初始质量的组成账目。m0=10 mg、阶段质量从10降至9.2 mg，失重8%，剩余比例0.92。各台阶若改用不同分母，百分数不能直接相加。

构造样品初始为 10 mg，先在氮气中以每分钟十摄氏度升到 600 °C，然后保温，并在第七十分钟改用空气。初始组成设为水 0.8 mg、聚合物 6 mg、炭黑 1.2 mg、稳定无机组分 2 mg。图中低温后约剩 9.2 mg，氮气热解后约剩 3.8 mg，空气阶段结束约剩 2 mg。计算得到的四项比例约为 8.01%、53.99%、18.00% 和 20.00%；微小偏差来自构造噪声与有限的台阶区间。现在先把它们叫作低温失重、氮气热解失重、空气阶段失重和最终残余，随后再讨论化学归属。

TG 曲线下降最陡的位置，意味着单位时间内失去的质量最多。将质量对时间求导，就得到质量变化速率；本节再加一个负号，让失重峰朝上，便于阅读。这条曲线常称 DTG。不同软件可能采用相反的符号，纵轴也可能是毫克每分钟、百分比每分钟或百分比每摄氏度，所以读峰前先读单位。恒速升温阶段可以借助升温速率在时间导数与温度导数之间换算；保温时温度不变，样品却仍能失重，这时以时间表示过程尤其清楚。

$$
r_t=-\frac{1}{m_0}\frac{dm}{dt},\qquad r_T=-\frac{1}{m_0}\frac{dm}{dT},\qquad r_t=\beta r_T,\quad\beta=\frac{dT}{dt}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d2410ee324d5f3cc2de959fa.svg) | 按初始质量归一化的失重速率，min⁻¹；乘100可写为%/min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78c3388d05455d424532a900.svg) | 按温度归一化的失重速率，K⁻¹或°C⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a358ffe402fdf3c4c31be5d.svg) | 当前质量与初始质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 温度，°C或K；温差使用同一单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 升温速率，K/min或°C/min。 |

链式法则把每度的变化乘以每分钟升高度数，得到每分钟的变化。10 mg样品以0.2 mg/min失重时，rt=0.02 min⁻¹，即2%/min；β=10 K/min时rT=0.002 K⁻¹，即0.2%/K。保温β=0时继续使用时间导数，不能除以零求温度导数。

![构造数据，种子720，初始10 mg。百分数均以独立给定的初始质量归一化。空白采用同一程序；DTG 加负号使失重朝上。局部多项式三阶，窗口7、21、61点，采样0.05 min，覆盖0.3、1.0、3.0 min。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1c40380d920c0c4baa4fd7ac.svg?v=1c40380d920c)

图 2构造数据，种子720，初始10 mg。百分数均以独立给定的初始质量归一化。空白采用同一程序；DTG 加负号使失重朝上。局部多项式三阶，窗口7、21、61点，采样0.05 min，覆盖0.3、1.0、3.0 min。

求导会放大相邻点的小差别，因此原始质量看起来很平滑，DTG 却可能布满细小起伏。例子比较了三个 Savitzky–Golay 局部多项式窗口，覆盖约 0.3、1.0 和 3.0 分钟。较短窗口保留更多波动，较长窗口会把换气后的尖锐转折摊宽，甚至在转折两侧产生过冲。选择窗口时，应同时看原始质量、采样间隔与待解释事件的持续时间，保留能稳定复现的主要特征。峰的个数不是组分的自动计数器：多个反应可能重叠成一个峰，同一种物质也可能连续经历脱水、断链和氧化。

## 残炭会让组成分析拐一个弯

如果直接把氮气中的失重叫“聚合物含量”，本例会得到约百分之五十四，比实际百分之六十少了一截。原因是模型中聚合物热解后有十分之一质量成为炭，留在坩埚里。这 0.6 mg 新生炭与原有 1.2 mg 炭黑一起，在空气阶段被消耗，形成约百分之十八的失重。于是把空气阶段的全部失重都当成原有炭黑，又会把炭黑含量算高。曲线中的每个台阶都是真实的质量账目，但账目名称需要反应路径支撑，不能仅凭“先掉的算聚合物，后掉的算炭黑”来分配。

如果独立对照已经给出了聚合物在相同条件下的残炭比例，就可以把账目解开。设聚合物原质量为一整份，其中九成进入挥发产物，一成留下；测得的 5.4 mg 热解失重就对应原聚合物的九成，因此原质量为 6 mg。空气阶段失去 1.8 mg，再扣除聚合物贡献的 0.6 mg 炭，得到原有炭黑 1.2 mg。这里的残炭比例不是从同一条曲线随意调出来的参数，它需要适合该配方与程序的独立信息；填料、交联和气氛都可能改变残炭行为。

$$
m_p=\frac{\Delta m_{\mathrm{py}}}{1-y},\qquad m_c=\Delta m_{\mathrm{ox}}-y m_p
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/63b17c0ff2d1bd233aeb8ba3.svg) | 初始聚合物质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b5b59c6334e2c66dd05e12e.svg) | 归属于聚合物挥发产物的热解失重，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 相同条件下聚合物残炭质量除以初始聚合物质量，无量纲；由独立信息给定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/da91b33ee64dd3e861a37f01.svg) | 原有炭黑或模型中原有可燃炭质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc150985325e893d423793e2.svg) | 充分氧化时新生炭与原有炭共同失去的质量，mg。 |

假定热解损失来自聚合物挥发部分，原有炭在热解阶段保留，氧化阶段炭充分消耗且无其他失重或增重。Δmpy=5.4 mg、y=0.1得mp=6 mg；Δmox=1.8 mg减去0.6 mg新生炭，得mc=1.2 mg。

![构造质量平衡：聚合物60%、水8%、原有炭黑12%、稳定无机组分20%。聚合物残炭比例0.1时产生6%新生炭。右侧保持两段失重54%和18%不变，展示不同独立残炭假设对应的组成。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4b5b2fada23f1597eba4795e.svg?v=4b5b2fada23f)

图 3构造质量平衡：聚合物60%、水8%、原有炭黑12%、稳定无机组分20%。聚合物残炭比例0.1时产生6%新生炭。右侧保持两段失重54%和18%不变，展示不同独立残炭假设对应的组成。

图右把残炭比例从零逐渐提高，同时保持测到的两段失重不变。你会发现推算的聚合物含量随之增加，原有炭黑含量降低。这不是计算矛盾，而是两段质量变化不足以同时确定所有未知量。在本例的简单质量平衡中，为保证推算炭黑非负，残炭比例最高为四分之一；这个数学边界并不是某种材料的已知残炭率。它告诉我们下一项有价值的实验是什么：测量未加炭黑的对应聚合物，或用能够识别残余物的另一种方法，补上区分原有炭与新生炭的信息。

最终残余也需要顺着反应来命名。本例特意把 2 mg 无机组分设为全程稳定，所以空气阶段充分结束后，它可以对应原有无机含量。实际材料中的碳酸盐可能释放二氧化碳，金属可能吸氧增重，某些无机化合物也会挥发或发生反应，终点残余就可能是转化后的产物。另一个容易忽略的变化是质量基准：2 mg 占初始 10 mg 的百分之二十，却占去掉水后 9.2 mg 的约百分之二十一点七四。两者都可以有用，只要名字和分母保持一致。

## 同一个残余，可能装着哪些物质？

构造配方固定为水8%、聚合物60%、原有炭黑12%、稳定无机物20%。改变聚合物残炭比例和空气阶段的完成程度，查看误把氧化失重全算为炭黑、把最终残余全算为无机物时的差别。

[Figure: 残炭与氧化完成比例的质量账目](https://ml-biomat.com/tutorials/experimental-methods/t02/#T02-plot)

交互实验中，原有聚合物、炭黑和无机组分比例固定，只改变聚合物残炭比例、空气阶段消耗掉的炭比例和装样量。先让空气反应充分完成，再逐渐减少完成比例，你会看到最终残余开始包含尚未烧尽的炭。此时即使横轴已经走到“结束”，它也不再等于原有无机组分。改变装样量则只按比例改变本模型的毫克读数，百分数保持不变；真实实验若随装样量改变出现不同百分数，就值得检查热传递、气体交换和反应是否完成。

## 用化学式核对台阶：一份结晶水的去向

在进入计量计算前，还要确认样品是否适合用单一化学式描述。粉末中若混有另一种盐或吸附的液体，同一份总失重就会包含多项贡献。可以先比较不同批次的固体结构与初始含水状态，再选择已知组成的对照。这里的顺序很实用：化学式提供预期比例，实验检验实际比例是否符合；若不符合，就查找额外组分、反应重叠或过程未完成的证据。把公式当成可检查的质量模型，远比看到一个接近整数的水合数后立即命名化合物更有解释力。

草酸钙一水合物是理解分步失重的好例子。它的化学式写作 CaC₂O₄·H₂O，点号后的水属于晶体组成，并不是样品表面随意沾上的一滴水。在合适的实验条件下，可以依次观察脱去水、草酸盐转成碳酸盐，以及碳酸盐转成氧化物的过程。伴随释放的气体分别涉及水、一氧化碳和二氧化碳。先写清固体产物与逸出物，再用原子量计算每一份质量，便能把曲线上看似抽象的台阶与具体化学反应连接起来。

本例采用钙 40.078、碳 12.011、氧 15.999、氢 1.008 的近似原子量，得到一水合物的式量 146.111 g/mol。每摩尔其中含 18.015 g 水，所以完全脱去这一份水，预期损失约百分之十二点三三。随后释放一摩尔 CO 和一摩尔 CO₂，对最初水合物质量的比例约为百分之十九点一七和三十点一二，最终 CaO 约占百分之三十八点三八。这里所有百分数都用最初质量作分母，四份相加为百分之百；若逐步改用上一台阶作分母，各段百分数就不再能直接相加。

![草酸钙一水合物的计量质量模型。所有台阶以初始水合物质量计；采用图示近似原子量。曲线形状与转变温度为构造值，非实测数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ff730a4a117fb63e5c39e3c2.svg?v=ff730a4a117f)

图 4草酸钙一水合物的计量质量模型。所有台阶以初始水合物质量计；采用图示近似原子量。曲线形状与转变温度为构造值，非实测数据。

反过来也能根据失水比例估计结晶水数量。先把水合物想成“已知质量的无水部分，加上若干份水”，测得的水比例同时影响分子中的水质量与总质量，所以不能只把百分数乘上无水式量后就结束。把总质量关系解出来，便得到下面的表达式。代入约百分之十二点三三的失水比例与无水草酸钙式量 128.096 g/mol，可得到一份水。这样的计算有明确化学前提：选定失重区间主要对应水，初始固体组成已知，并且脱水与其他分解能够分开。

$$
f_w=\frac{n_w M_w}{M_a+n_w M_w},\qquad n_w=\frac{f_w M_a}{M_w(1-f_w)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/40240877de058d73b2fe4254.svg) | 初始水合物中水的质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b794cb38c00fee5cea77f6d.svg) | 每个无水化学式单位对应的水分子数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | 水的摩尔质量，此处18.015 g/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/acae10568b66868832f17363.svg) | 无水化学式单位的摩尔质量，此处128.096 g/mol。 |

水的质量同时进入分子和总质量分母；解质量分数关系得到水合数。fw=18.015/146.111≈0.1232967，代入得nw=1。要求选定失重是该水合物的水，并与其他挥发或分解贡献分开。

图中的台阶高度来自上述计量，曲线形状和转变温度则是构造模型。真实草酸钙实验中，样品质量、坩埚、气氛、升温速率和判定起始温度的方法都会影响读到的温区。公开的多实验室比较研究专门考察了这些操作差异，提醒我们先统一测量定义，再比较数值。对于成分未知的生物矿化样品，同样大小的低温失重还可能混有吸附水或残留溶剂；通过不同湿度预处理、逸出气体分析与固体结构测量，可以逐步区分这些贡献，让计量推断有对应的化学对象。

## 为什么快一点加热，材料看起来会更耐热

常见热稳定性指标包括失去初始质量百分之五时的温度，以及 DTG 主峰所在温度。它们便于比较同一程序下的样品，但都包含“经历了多长时间”的信息。设想两份相同材料同时开始升温，一份每分钟升五度，另一份每分钟升二十度。快升温的样品到达某一温度时，已在此前温区停留的时间更短，即使反应规律完全相同，累计分解也可能较少，因此它往往要到更高温度才达到相同转化比例。仪器与样品的温度滞后还可能进一步改变表观位置。

为了单独看清时间效应，我们用一个只有一步反应的一阶模型：每一瞬间的反应速度与尚未转化的比例成正比，温度通过 Arrhenius 关系改变速率常数。“一阶”在这里描述数学形式，不是说现实聚合物只经过一种化学反应；模型中的转化比例也针对选定反应的总质量变化，不能把含有永久灰分的整块样品直接当成百分之百可失去的质量。活化能描述速率对温度的敏感性，它与量热实验测得的反应热属于不同物理量。

$$
\alpha=\frac{m_s-m(t)}{m_s-m_f},\qquad\frac{d\alpha}{dt}=k(T)(1-\alpha),\qquad k(T)=A\exp\!\left(-\frac{E_a}{RT}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 选定反应已完成比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f38b34c4861f4340ecef52cd.svg) | 该反应开始与完全结束时的质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | 时刻t对应质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fc90edd0d6c7e9e5eceaaa94.svg) | 温度T下的一阶速率常数，min⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 指前因子，本例10¹⁰ min⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fc22571629d5ee46df4d11e5.svg) | Arrhenius活化能，本例140000 J/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 气体常数8.314462618 J/(mol·K)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |

单步一阶模型中速率与未转化比例成正比；mf必须对应完整反应终点。300 °C即573.15 K时k≈0.00174261 min⁻¹。初始α=0等温60 min时α=1−exp(−k×60)≈0.09928，即9.93%。模型参数固定，未包含多步反应与扩散控制。

![构造单步一阶动力学，A=10¹⁰ min⁻¹、Ea=140 kJ/mol。左图仅改变升温速率；右图为300 °C等温反应。不包含传热滞后或扩散过程。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0a3c040dd0bd01084facb8c9.svg?v=0a3c040dd0bd)

图 5构造单步一阶动力学，A=10¹⁰ min⁻¹、Ea=140 kJ/mol。左图仅改变升温速率；右图为300 °C等温反应。不包含传热滞后或扩散过程。

模型取指前因子每分钟一百亿、活化能 140 kJ/mol。升温速率分别为 5、10、20 °C/min 时，反应达到百分之五转化的温度约为 340.78、355.61、371.15 °C。三条曲线并没有换材料，也没有改变活化能，只改变了时钟走过每个温区的速度。另一方面，在 300 °C 保持六十分钟，模型已转化约百分之九点九三；保持六小时则约百分之四十六点六零。一个比扫描中百分之五转化温度低得多的温度，仍然可以在足够长时间内积累明显变化。

因此，围绕短时加工的问题，可以比较接近加工气氛与时间尺度的实验；围绕长期储存或服役的问题，则需要覆盖目标时间与温度的保温数据，并检查反应路径是否保持一致。多升温速率实验有助于识别动力学差异，但重叠反应、扩散限制和氧气供应变化会使简单单步模型失去对应对象。实际研究中，应先确认基线、质量变化区间、气氛和最终转化定义，再选用相应动力学方法。这样得到的“更稳定”才有明确场景：是在同一热程序下更晚失重，还是在指定温度和时长后保留了更多质量。

## 把一条热重曲线整理成可以追问的结果

起始温度也要有操作定义。用初始基线与失重区切线的交点定义外推起始温度，和读取累计失重达到百分之五时的温度，使用的是不同几何规则。少量水或残留溶剂可能先消耗掉百分之五，却不对应聚合物主链的大规模分解。比较主链稳定性时，可以先规定干燥状态，或者明确针对选定反应阶段定义转化；比较实际使用中的挥发损失时，则可能需要保留原样水分。先说明所关心的损失是什么，再选择指标，才能避免不同文章中同名温度实际回答不同问题。

下面的完整程序从已知质量组成出发，构造原始读数、空坩埚背景、三种导数平滑结果和气氛切换过程。它输出逐点时间、温度、质量及导数，同时保存台阶区间的平均值与组成计算。程序还单独生成水合物计量图和一阶动力学图，让“多少质量”“发生什么反应”“经历多久”各自对应清楚的计算。所有构造曲线都保留生成条件，你可以改变一个条件后观察影响，而不会把数值模型误认为某种真实材料的实测性能。

### 完整热重、残炭计量与时间效应分析

输出原始/空白/校正质量、三种导数、水合物计量、升温与等温动力学，以及五幅双语图。

```
"""TGA mass accounting, derivatives, hydrate stoichiometry and rate effects.

All traces are constructed teaching models, not measurements of a real specimen.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.special import expit
from scipy.signal import savgol_filter
from scipy.integrate import cumulative_trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True)
P.add_argument('--language',choices=['zh','en'],default='en');args=P.parse_args()
OUT=args.output;OUT.mkdir(parents=True,exist_ok=True);ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],
 'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none',
 'axes.labelcolor':'#20333e','text.color':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(fig,name):
 for ext in ['svg','png']:fig.savefig(OUT/f'{name}-{args.language}.{ext}',dpi=145,bbox_inches='tight')
 plt.close(fig)
def csv(name,headers,cols):np.savetxt(OUT/name,np.column_stack(cols),delimiter=',',header=','.join(headers),comments='',fmt='%.10g')
def frac(x,center,width):
 a=expit((x-center)/width);a0=expit((x[0]-center)/width)
 return (a-a0)/(1-a0)

rng=np.random.default_rng(720)
t=np.arange(0,95.0001,.05);T=np.minimum(25+10*t,600)
water=frac(T,95,12);pyro=frac(T,350,18)
burn=np.where(t>=70,1-np.exp(-.5*np.maximum(t-70,0)),0)
true=10-.8*water-5.4*pyro-1.8*burn
blank=.028+.00008*(T-25)+.00012*t+.025*np.exp(-np.maximum(t-70,0)/.25)*(t>=70)
raw=true+blank+rng.normal(0,.0015,t.size)
blank_record=blank+rng.normal(0,.001,t.size);corrected=raw-blank_record
m0=10.0 # Independent initial mass, mg; every percentage uses this denominator.
plateau=lambda mask:float(np.mean(corrected[mask]))
dry=plateau((T>=180)&(T<=220));inert=plateau((t>=60)&(t<=68));ash=plateau(t>=90)
losses=np.array([m0-dry,dry-inert,inert-ash,ash])/m0*100
dtg={w:-savgol_filter(corrected,w,3,deriv=1,delta=.05)/m0*100 for w in [7,21,61]}
polymer=(dry-inert)/.9;carbon=inert-ash-.1*polymer
csv('tga_scan.csv',['time_min','temperature_C','true_mass_mg','raw_mass_mg','blank_mass_mg','corrected_mass_mg','dtg_window7_percent_per_min','dtg_window21_percent_per_min','dtg_window61_percent_per_min'],[t,T,true,raw,blank_record,corrected,dtg[7],dtg[21],dtg[61]])

# Figure 1: original explanatory apparatus, not a historical reconstruction.
fig,axs=plt.subplots(1,2,figsize=(12,4.9),gridspec_kw={'width_ratios':[1.1,1]},layout='constrained')
a=axs[0];a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
a.add_patch(Rectangle((3.7,1.1),3.2,3.6,fill=False,ec=R,lw=3))
a.add_patch(Rectangle((4,1.4),2.6,3,fill=False,ec=R,lw=1,ls='--'))
a.plot([2,7.5],[6.4,6.4],color=K,lw=3)
a.add_patch(Polygon([[4.4,5.9],[5,6.4],[5.6,5.9]],color=K))
a.plot([2.4,2.4],[6.4,5.3],color=K);a.add_patch(Rectangle((1.7,4.9),1.4,.4,color=B))
a.plot([5.3,5.3],[6.4,3.6],color=K,lw=1.5)
a.add_patch(Polygon([[4.7,3.6],[4.9,3.2],[5.7,3.2],[5.9,3.6]],fc=Y,ec=K))
a.annotate('',xy=(4.2,2.1),xytext=(2.1,2.1),arrowprops={'arrowstyle':'->','color':G,'lw':2})
a.annotate('',xy=(8.4,4.2),xytext=(6.7,4.2),arrowprops={'arrowstyle':'->','color':G,'lw':2})
a.text(1.9,1.4,L('受控气体入口','Controlled gas'),color=G,ha='center')
a.text(8,4.7,L('排出气体','Evolved gas'),color=G,ha='center')
a.text(2.4,7,L('质量读数','Mass readout'),ha='center')
a.text(5.3,2.7,L('坩埚与样品','Pan + specimen'),ha='center',fontsize=9)
a.text(7.2,2.5,L('炉体','Furnace'),color=R)
a.text(5,.25,L('连续称量：把“加热后再称”变为一条轨迹\n原理示意；联系 Honda 与 Saito 的早期热天平工作','Continuous weighing replaces interrupted heat–cool–weigh cycles\nPrinciple diagram; early thermobalance work of Honda and Saito'),ha='center',fontsize=9)
a.set_title(L('A  质量、温度、气氛同时记录','A  Mass, temperature and atmosphere'))
a=axs[1];a.plot(t,T,color=R,lw=2);a.set(xlabel=L('时间 / min','Time / min'),ylabel=L('程序温度 / °C','Programmed temperature / °C'),ylim=(0,670))
a.axvspan(0,70,color=B,alpha=.08);a.axvspan(70,95,color=G,alpha=.12)
a.axvline(70,color=G,ls='--');a.text(25,110,L('氮气','Nitrogen'),color=B);a.text(79,110,L('空气','Air'),color=G)
a.annotate(L('600 °C 保温','600 °C hold'),xy=(65,600),xytext=(38,470),arrowprops={'arrowstyle':'->','color':K})
a.set_title(L('B  构造样品的实验程序','B  Program for the teaching specimen'));save(fig,'balance-history')

fig,axs=plt.subplots(2,2,figsize=(12,8.4),layout='constrained')
a=axs[0,0];a.plot(t,100*raw/m0,color=Y,lw=1,label=L('原始','Raw'));a.plot(t,100*corrected/m0,color=B,lw=1.2,label=L('减去空坩埚','Blank corrected'))
a.axvline(70,color=G,ls='--');a.set(xlabel=L('时间 / min','Time / min'),ylabel=L('剩余质量 / 初始质量 %','Remaining mass / initial mass %'),title=L('A  同时保留原始与校正轨迹','A  Preserve raw and corrected traces'));a.legend(frameon=False)
a=axs[0,1];a.plot(t,blank_record,color=Y,lw=1);a.axvline(70,color=G,ls='--');a.set(xlim=(66,75),xlabel=L('时间 / min','Time / min'),ylabel=L('空坩埅读数 / mg','Empty-pan reading / mg'),title=L('B  换气也会推动天平读数','B  A gas switch also moves the balance'))
a=axs[1,0]
for w,c in [(7,'#a8b8bf'),(21,B),(61,R)]:a.plot(t,dtg[w],color=c,lw=1,label=L(f'{(w-1)*.05:.1f} min 窗口',f'{(w-1)*.05:.1f} min window'))
a.set(xlim=(66,78),xlabel=L('时间 / min','Time / min'),ylabel=L('失重速率 / % 初始质量·min⁻¹','Mass-loss rate / % initial mass min⁻¹'),title=L('C  导数放大噪声，平滑改变尖锐转折','C  Derivatives amplify noise; smoothing changes corners'));a.legend(frameon=False,fontsize=9)
a=axs[1,1];labels=L(['低温失重','氮气热解','空气中失重','最终残余'],['Low-T loss','N₂ pyrolysis','Air-stage loss','Final residue'])
a.bar(labels,losses,color=[B,R,K,Y]);a.set(ylabel=L('初始质量的百分比 / %','Percent of initial mass / %'),ylim=(0,65),title=L('D  先得到操作定义的四份质量','D  Four operationally defined mass fractions'))
for i,v in enumerate(losses):a.text(i,v+1,f'{v:.2f}',ha='center')
save(fig,'mass-derivative')

y=np.linspace(0,.25,151);inferred_poly=54/(1-y);inferred_carbon=18-y*inferred_poly
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0];parts=[(8,B,L('水 8','Water 8')),(54,R,L('挥发产物 54','Volatile products 54')),(6,'#bfa5a0',L('新生成炭 6','New char 6')),(12,K,L('原有炭黑 12','Added carbon 12')),(20,Y,L('矿物残余 20','Mineral residue 20'))]
left=0
for value,c,label in parts:a.barh(.5,value,left=left,color=c,height=.35);a.text(left+value/2,.76,label,rotation=45,ha='left',fontsize=9);left+=value
a.set(xlim=(0,105),ylim=(0,1.65),yticks=[],xlabel=L('初始质量的百分比 / %','Percent of initial mass / %'),title=L('A  60% 聚合物留下了 6% 炭','A  60% polymer leaves 6% char'))
a.annotate(L('空气阶段一起烧掉：18%','Consumed together in air: 18%'),xy=(70,.30),xytext=(43,.06),arrowprops={'arrowstyle':'->','color':K},fontsize=9)
a=axs[1];a.plot(y,inferred_poly,color=R,lw=2,label=L('推算聚合物','Inferred polymer'));a.plot(y,inferred_carbon,color=K,lw=2,label=L('推算原有炭黑','Inferred added carbon'));a.axvline(.1,color=B,ls='--');a.scatter([.1,.1],[60,12],c=[R,K]);a.set(xlabel=L('独立给定的聚合物残炭比例 y','Independently specified polymer char yield y'),ylabel=L('初始样品质量的百分比 / %','Percent of initial specimen mass / %'),ylim=(0,76),title=L('B  相同失重分配，可有不同原始组成','B  Same stage losses, different original compositions'));a.legend(frameon=False)
save(fig,'char-composition')

# Stoichiometry uses rounded standard atomic weights, g/mol.
Ca,C,O,H=40.078,12.011,15.999,1.008
MW=Ca+2*C+5*O+2*H;waterMW=2*H+O;coMW=C+O;co2MW=C+2*O;oxideMW=Ca+O
stoich=np.array([waterMW,coMW,co2MW,oxideMW])/MW*100
Th=np.linspace(25,900,1751)
hm=100-stoich[0]*frac(Th,170,12)-stoich[1]*frac(Th,500,18)-stoich[2]*frac(Th,750,22)
csv('hydrate.csv',['temperature_C','constructed_remaining_percent'],[Th,hm])
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0];a.plot(Th,hm,color=B,lw=2);a.set(xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('初始质量的百分比 / %','Percent of initial mass / %'),ylim=(30,105),title=L('A  化学计量规定台阶高度','A  Stoichiometry fixes step heights'))
for x,z,lab in [(220,91,'H₂O'),(560,72,'CO'),(810,48,'CO₂')]:a.text(x,z,lab,color=R)
a.text(75,40,L('曲线为构造模型，转变温度并非测量结果','Constructed curve; transition temperatures are not measurements'),fontsize=8)
a=axs[1];a.axis('off');a.set(xlim=(0,1),ylim=(0,1));a.set_title(L('B  从反应式核对每一份质量','B  Account for every portion by reaction'))
for yy,formula,note,c in [(.86,'CaC₂O₄·H₂O',f'{MW:.3f} g/mol',K),(.64,'CaC₂O₄',L(f'失水 {stoich[0]:.3f}%',f'Water loss {stoich[0]:.3f}%'),B),(.42,'CaCO₃',L(f'释放 CO：{stoich[1]:.3f}%',f'CO loss: {stoich[1]:.3f}%'),R),(.20,'CaO',L(f'释放 CO₂：{stoich[2]:.3f}%；余 {stoich[3]:.3f}%',f'CO₂ loss: {stoich[2]:.3f}%; residue {stoich[3]:.3f}%'),Y)]:
 a.text(.06,yy,formula,fontsize=17,color=c,va='center');a.text(.06,yy-.07,note,fontsize=10)
 if yy>.2:a.annotate('',xy=(.82,yy-.14),xytext=(.82,yy),arrowprops={'arrowstyle':'->','color':K})
save(fig,'hydrate-stoichiometry')

Ea=140000.;Af=1e10;Rg=8.314462618
Tk=np.linspace(298.15,923.15,6251);Tc=Tk-273.15;k=Af*np.exp(-Ea/(Rg*Tk))
rates={};metrics={}
for rate in [5,10,20]:
 hazard=cumulative_trapezoid(k/rate,Tk,initial=0);alpha=-np.expm1(-hazard);rates[rate]=alpha
 metrics[str(rate)]={'T5_C':float(np.interp(.05,alpha,Tc)),'peak_C':float(Tc[np.argmax(k*(1-alpha))])}
ti=np.linspace(0,360,721);ki=Af*np.exp(-Ea/(Rg*573.15));ai=-np.expm1(-ki*ti)
csv('kinetics.csv',['temperature_C','conversion_5Kmin','conversion_10Kmin','conversion_20Kmin'],[Tc,rates[5],rates[10],rates[20]])
csv('isothermal.csv',['time_min','conversion_at300C'],[ti,ai])
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0]
for rate,c in [(5,B),(10,R),(20,G)]:a.plot(Tc,100*(1-rates[rate]),color=c,lw=2,label=f'{rate} °C/min')
a.set(xlim=(300,520),ylim=(0,105),xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('未反应份额 / %','Unreacted fraction / %'),title=L('A  同一动力学，快扫曲线更靠右','A  Same kinetics; faster ramps shift right'));a.legend(frameon=False)
a=axs[1];a.plot(ti,100*ai,color=B,lw=2);a.scatter([60,360],100*(-np.expm1(-ki*np.array([60,360]))),color=R);a.set(xlabel=L('在 300 °C 保持的时间 / min','Hold time at 300 °C / min'),ylabel=L('转化比例 / %','Converted fraction / %'),title=L('B  较低温度也会累积反应','B  A lower temperature still accumulates reaction'));a.text(15,100*ai[-1]*.73,L('单步一阶构造模型\nA = 10¹⁰ min⁻¹，Eₐ = 140 kJ/mol','Constructed single-step first-order model\nA = 10¹⁰ min⁻¹; Eₐ = 140 kJ/mol'),fontsize=9)
save(fig,'rate-and-hold')

summary={'data_kind':'constructed teaching datasets','seed':720,'initial_mass_mg':m0,
 'dry_plateau_mg':dry,'inert_plateau_mg':inert,'final_plateau_mg':ash,
 'water_loss_percent':float(losses[0]),'pyrolysis_loss_percent':float(losses[1]),'air_loss_percent':float(losses[2]),'residue_percent':float(losses[3]),
 'char_corrected_polymer_percent':float(polymer/m0*100),'char_corrected_added_carbon_percent':float(carbon/m0*100),
 'ideal_dry_basis_residue_percent':2/9.2*100,'hydrate_water_loss_percent':float(stoich[0]),'hydrate_total_mass_percent':float(stoich.sum()),
 'hydrate_formula_mass_g_per_mol':MW,'hydrate_water_number':float((stoich[0]/100)*(MW-waterMW)/(waterMW*(1-stoich[0]/100))),
 'T5_5Kmin_C':metrics['5']['T5_C'],'T5_10Kmin_C':metrics['10']['T5_C'],'T5_20Kmin_C':metrics['20']['T5_C'],
 'isothermal_rate_at300C_per_min':float(ki),'isothermal_60min_conversion_percent':float(-np.expm1(-ki*60)*100),'isothermal_360min_conversion_percent':float(ai[-1]*100),
 'char_ambiguity_upper_y':18/(54+18)}
assert abs(sum(losses)-100)<1e-12
assert abs(polymer-6)<.03 and abs(carbon-1.2)<.03
assert abs(stoich.sum()-100)<1e-12 and abs(summary['hydrate_water_number']-1)<1e-12
assert metrics['5']['T5_C']<metrics['10']['T5_C']<metrics['20']['T5_C']
assert np.all(np.diff(ai)>=0)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

输出文件中的时间与温度两列都应保留：升温段可用温度寻找事件，保温和换气段则需要时间区分先后，二者共同描述完整实验。

阅读输出时，先用原始轨迹检查异常，再看空白是否出现同一时刻的变化；随后在相对平稳、化学意义明确的区间取台阶平均值，最后计算比例。平均多个点可以减小部分随机波动，但相邻点可能相关，且共同受到同一次装样和基线误差影响，因此它们不是多份独立样品。若要比较两种配方，应安排独立取样和重复实验，报告样品间差异；若主要问题是台阶边界选择，就改变区间并观察结果是否稳定。这两种检验针对不同的不确定性，值得分别保留。

对于一份含水、含矿物的生物高分子支架，一个清楚的研究结论可以依次交代初始状态、温度与气氛程序、低温失重、热解残余和氧化后残余，再说明组成换算采用的化学信息。如果残炭比例未知，下一步就选择合适的聚合物对照；如果疑似有结晶水，就核对失重计量与逸出气体；如果目的是加工稳定性，就在相应停留时间下增加保温测试。这样的安排让每个实验都回答一个具体问题，也让 TGA 从“材料烧完还剩多少”发展成理解组成、反应和时间尺度的一套方法。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/T02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Saito: A New Method of Studying Thermal Decomposition of Substances](https://www.jstage.jst.go.jp/article/pjab1912/2/2/2_2_58/_pdf/-char/en)

   连续称量、气氛与保温的早期历史。
2. [Sircar: Composition Analysis of Rubber by Thermogravimetry, TA083](https://www.tainstruments.com/pdf/literature/TA083.pdf)

   橡胶组成、残炭与炭黑的区分。
3. [NETZSCH: TGA Measurements by Means of the BeFlat Correction](https://analyzing-testing.netzsch.com/en-AU/application-literature/tga-measurements-by-means-of-the-beflat-correction/)

   浮力、气流与匹配空白。
4. [NETZSCH: TGA Measurements on Calcium Oxalate Monohydrate](https://analyzing-testing.netzsch.com/en/application-literature/tga-measurements-on-calcium-oxalate-monohydrate)

   草酸钙的分步固体与气体产物。
5. [Suzanne et al.: A Round-Robin Study on Decomposition of Calcium Oxalate Monohydrate by Thermogravimetry](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=935144)

   质量、坩埚、起始定义与实验室间比较。
6. [NETZSCH Kinetics Neo: Master Plot Verification](https://kinetics.netzsch.com/en/learn/master-plot)

   Arrhenius形式与单步反应的条件。
7. [NETZSCH Kinetics Neo: Conversion for Incomplete Measured Data](https://kinetics.netzsch.com/en/learn/how-to-calculate-conversion-for-incomplete-measured-data)

   转化比例与完整质量变化的定义。
8. [TA Instruments: High Resolution Thermogravimetric Analysis, TA023](https://www.tainstruments.com/pdf/literature/TA023.pdf)

   装样、速率和保温对分离的影响。
