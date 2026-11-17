# 细胞培养与计数：建立可比较的实验起点

Source: https://ml-biomat.com/tutorials/experimental-methods/l01/
Language: zh-CN

从计数室的一小格，连接细胞培养历史、取样精度与每孔接种数。

## 比较材料之前，先让细胞站在相近的起点

两块材料上培养一天后，一块看起来细胞更多，另一块更少。这个差异可能来自材料对细胞的作用，也可能在实验开始时就已经存在：第一块原本接种得更多，细胞在第二块上没有均匀分散，或两组使用了不同状态的细胞。细胞培养与计数因此是后续实验的起点。它们帮助我们知道放进去了什么、放进去多少，以及这些细胞当时处于什么状态。起点清楚，后面的颜色、荧光、蛋白和基因表达变化才容易与研究问题连接起来。

培养细胞可以理解为在体外为一个活的群体安排生活环境。培养基提供营养、盐和缓冲成分，容器或材料表面提供附着与空间条件，温度和气体环境影响代谢与酸碱平衡。细胞既消耗物质，也释放代谢产物和信号分子，还会改变周围环境。这与把一种稳定试剂分装到几个管子里不同：相同数量的细胞，在不同培养历史、密度和材料界面上，可能以不同方式继续生长。计数提供数量，培养记录则解释数量背后的生物状态。

本节从常见的哺乳动物细胞培养与计数出发，重点建立可以迁移的判断方法。贴壁细胞需要适合的表面，悬浮细胞主要分散在液体中；原代细胞直接来自组织，通常保留较多来源特征，连续细胞系则可以长期扩增并形成相对稳定的研究模型。具体培养基、温度、气体和传代方式应跟随所用细胞的已验证条件。先认清细胞身份与生长方式，再安排数量和空间，可以避免把一种细胞的习惯当成所有细胞的共同要求。

计数本身也需要先定义对象。完整细胞总数、膜完整细胞数、能够继续分裂的细胞数和最终附着在材料上的细胞数，是不同问题。台盼蓝等排斥染料利用膜通透性区分群体，给出的是特定染色时间内的膜完整状态；它与长期增殖能力、代谢水平和后续功能有关联，但不是同一个测量。若实验目标是按活细胞数量接种，就应明确采用的活性判定方法，并在后续适当时间检查细胞是否附着、恢复和保持所需形态。

## 细胞有培养历史，传一次代不等于分裂一次

培养容器里的细胞会增多，空间和营养条件也随之变化。将一部分细胞转移到新容器继续培养，称为传代。它既扩大可用细胞，也改变群体所处的密度和环境。一个“传代次数”只表示发生了多少次这样的转移，不直接告诉我们细胞经历了多少次数量倍增。例如一次按二分之一分配，恢复到原来数量需要一次理想倍增；一次只保留八分之一，恢复到原来数量则需要三次理想倍增。因此，传代编号与群体倍增数应分别理解。

![一次传代可对应不同倍增数：分配 1:2 与 1:8 的理想扩增示意。Hayflick 与 Moorhead 的研究引出培养历史这个变量。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/33996fc3b439932e86291175.svg?v=33996fc3b439)

图 1一次传代可对应不同倍增数：分配 1:2 与 1:8 的理想扩增示意。Hayflick 与 Moorhead 的研究引出培养历史这个变量。

1961 年，Hayflick 与 Moorhead 研究正常人二倍体细胞的连续培养，指出这类细胞的增殖能力存在有限范围。这项工作让“已经培养了多久、经历了多少扩增”成为解释细胞行为的重要变量。它不是为所有细胞规定一个相同的截止次数；不同细胞、培养条件和群体状态会影响观察结果。其方法上的启发在于：细胞会随培养历史改变，不能只因为瓶子标签相同，就默认不同时间取得的群体具有完全相同的生物特征。

群体倍增数用终点细胞数与起点细胞数的比值计算。数量增加四倍，相当于连续翻倍两次；增加八倍，相当于三次。对数只是把“乘了多少倍”改写成“相当于翻倍几次”的工具。若 48 小时内从两万个细胞增至八万个，净群体倍增数是二，对应平均倍增时间 24 小时。这里的“净”很重要，因为细胞可能同时分裂、死亡、脱落或在收集时丢失；仅凭两个总数，测到的是群体净变化，而不是逐个细胞完成分裂的次数。

$$
\mathrm{PD}=\log_2\!\left(\frac{N_t}{N_0}\right),\qquad T_d=\frac{t}{\mathrm{PD}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39f01eb55d50f92c89f7cf5d.svg) | 起止测量间净群体倍增数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3d5bc3f33c6bf9779e0abdb9.svg) | 终点测得细胞数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 起点测得细胞数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/14ae3fefbbf822ee29c5d5c8.svg) | 以 2 为底的对数，把倍数转换为等效翻倍次数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 两次测量的时间间隔，h。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e6d3ee28e801518c3f5199bb.svg) | 该区间平均净倍增时间，h；适用于 PD>0。 |

N_0=20000、N_t=80000、t=48 h，数量比为 4，PD=2，T_d=24 h。只有生长阶段和计数定义相近时，倍增时间的比较才对应相近生物过程。

观察增长曲线时，刚接种后细胞可能需要恢复和附着，随后进入较快扩增阶段，密度或营养限制出现后又会放缓。只有在相近生长阶段比较倍增时间，数字才具有相近含义。半对数图将细胞数放在对数轴上，理想指数增长就会呈直线；曲线弯曲提示增长速率发生变化。研究材料对细胞的作用时，也要考虑不同材料上的附着延迟是否使两组在测量当天处于不同阶段，而不只比较一个最终细胞数。

保存低代次的主细胞库和工作细胞库，可以让不同实验从可追溯的起点开始。冻存恢复后要观察形态、数量变化和适应情况，再进入正式比较；如果突然出现与既往不同的生长或形态，先检查培养条件、身份和污染状态。一个清楚的记录可以包含细胞名称与标识、来源批次、传代或倍增历史、培养基及关键添加物、复苏时间和实验接种信息。这些字段是连接不同批次结果的生物学条件。

## 让环境变化和处理效应分得开

培养基中的颜色常来自酸碱指示成分，可以提示环境变化，却不能替代细胞状态的直接观察。细胞代谢会改变酸碱和营养，培养基的缓冲系统又与气体环境配合；更换容器、液体体积或长时间离开培养环境，都可能改变这些条件。血清和其他添加物还提供复杂的蛋白质与信号成分，批次变化可能影响附着和生长。比较材料时，应让两组使用相同或经过设计的培养条件，把有意改变的变量与日常操作造成的变化区分开。

细胞密度也是环境的一部分。贴壁细胞通常用单位面积细胞数描述接种密度，悬浮细胞常用单位体积细胞数；两者都需要同时知道实际面积或体积。显微镜下的“汇合度”是表面被细胞覆盖的程度，它受细胞大小、伸展和排列影响。相同细胞数在两种材料上，可能因铺展面积不同而呈现不同汇合度；同样百分之七十的覆盖，也未必意味着相同细胞数。因此，覆盖图像与细胞计数各自保留，才能区分数量与形态变化。

无菌操作的意义可以从实验变量理解：进入培养体系的其他生物会消耗营养、产生分泌物并改变细胞反应。工作时减少容器敞开时间、按规范使用相应防护和培养操作设备、将不同细胞与试剂清楚分开，都是为了维持所研究的体系。培养液看起来清澈，并不说明所有污染都不存在。支原体可以在没有明显浑浊时影响细胞生长和表达，因而需要适当的检测；常用抗生素也不能替代这一检查，更不能替代规范操作。

细胞身份与污染是两个独立问题。一个培养物可以没有检出支原体，却并非标签上写的细胞；也可以身份相符，却存在微生物污染。人源细胞常用短串联重复序列等方法进行身份比对，其作用类似比较一组遗传标识。显微形态则提供更频繁、直接的日常线索，但形态相似不足以确认身份。将身份记录、污染检测和日常形态观察结合起来，才能说明实验使用了哪一个生物对象，并追踪它是否发生了值得调查的改变。

材料还会改变细胞所在的局部环境。未充分平衡的材料可能改变培养液pH、吸收营养成分或释放小分子；疏水表面可能使接种液聚成一滴，导致细胞集中；多孔支架可能让细胞进入内部，使表面视野看起来较少。接种前记录材料状态，接种后检查空间分布与附着效率，可以将“没有看到”进一步分解为没有接种进去、没有保留下来、进入了更深处或真正减少。这个分解常常比直接增加检测指标更有帮助。

## 计数板的关键是一小格里有多少体积

血细胞计数板是一块具有精确几何结构的玻璃计数室。它最早服务于血细胞计数，现在也用于多种细胞悬液。盖玻片与计数面之间形成已知深度，网格给出已知面积，二者相乘就是观察体积。以常见改良 Neubauer 计数室的一大格为例，面积为一平方毫米，深度为 0.1 毫米，体积为 0.1 立方毫米，也就是万分之一毫升。因此，数出这一格里的细胞，再乘一万，便换算为每毫升的数量。这个一万来自体积，不是需要脱离计数室结构记忆的常数。

![真实血细胞计数板及配套器具，Todd 摄影，CC BY-SA 2.0。原照片完整保留，外加双语说明；本组合图同按 CC BY-SA 2.0 分享。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/eace2793bedbbf7b5ada428d.svg?v=eace2793bedb)

图 2真实血细胞计数板及配套器具，Todd 摄影，CC BY-SA 2.0。原照片完整保留，外加双语说明；本组合图同按 CC BY-SA 2.0 分享。

![计数区域面积与计数室深度共同决定体积。绿色边计入、橙色边排除；图内细胞仅示意几何，不是右文四格的原始计数。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8aa59db209142e5f65ad5eff.svg?v=8aa59db20914)

图 3计数区域面积与计数室深度共同决定体积。绿色边计入、橙色边排除；图内细胞仅示意几何，不是右文四格的原始计数。

$$
V_s=Ah,\qquad C=\frac{d\sum_{i=1}^{n}N_i}{nV_s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 每个观察区域体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 每个观察区域面积，mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 计数室深度，mm；Ah 得到 mm³，除以 1000 转成 mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 原悬液的所定义细胞浓度，个/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 从原悬液到被计数混合液的总稀释倍数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 等体积观察区域数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | 第 i 个区域内所定义的细胞计数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 区域索引，从 1 到 n，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对各区域计数求和的运算。 |

先求总体积中的平均数量，再还原稀释。A=1 mm²、h=0.1 mm 给出 V_s=10⁻⁴ mL。四格膜完整细胞合计 308 个，d=2，因此 C=2×308/(4×10⁻⁴)=1.54×10⁶ 个/mL。

不同计数板或自动计数耗材的有效深度和区域可能不同，计算应使用实际观察体积。盖玻片没有正确就位、加样过多、气泡或液体没有均匀进入，都会破坏“所数区域对应已知体积”的前提。悬液应在取样前温和而充分混匀，因为细胞会沉降，也可能聚团；取样与装板之间拖得太久，顶部和底部的浓度就可能不同。检查两侧计数室或多个区域是否出现明显系统差异，有助于发现装样和混匀问题。

边界上的细胞要按统一规则归属，例如计入上边和左边，不计入下边和右边。这样相邻区域不会重复计算同一个细胞，也不会把所有边界细胞都漏掉。规则的价值在于一致性，具体使用哪一对相邻边可以按计数方案确定。观察时还要区分完整细胞、碎片、气泡和细胞团。若一个团里明显有多个细胞却被当成一个对象，计数就会偏低；若碎片被当作细胞，计数又会偏高。保留原始图像或计数记录，能让这些判断被复查。

染色往往同时稀释样品。将等体积细胞悬液和染液混合，测量混合液里的浓度后，要乘二才能还原原悬液。若此前还进行过其他稀释，所有步骤的倍数相乘。染色后等待时间也应一致，因为膜通透性和染料作用可能随时间改变。把“样品体积、加入体积、最后体积、计数时间”记在同一张记录中，就能把生物判定与浓度换算连起来，避免得到一个精确到很多位、却缺少正确稀释基准的数字。

以四个大格为例，未染色细胞分别为 72、81、76、79 个，染色细胞为 8、9、7、8 个。未染色平均每格 77 个，总平均每格 85 个；若染色造成两倍稀释，原悬液膜完整细胞浓度是每毫升 154 万个，总浓度是每毫升 170 万个。将全部四格的未染色数除以总数，膜完整比例约为百分之九十点六。浓度与比例回答不同问题：即使两份悬液的比例相同，它们每毫升可用于接种的细胞数也可能相差很大。

$$
f_v=\frac{N_v}{N_v+N_d},\qquad P_v=100f_v\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33fc340055a349697fda4777.svg) | 按膜完整标准分类的细胞比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a4913ae2411f1cd97def0a6b.svg) | 合并观察区域中膜完整的细胞数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/909a1770cd343bb9acb32947.svg) | 相同区域中染料进入的细胞数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/704f9911f7e55073fd93e910.svg) | 膜完整百分比，%。 |

同一分类和计数范围内，分母包含两类计数。308 个未染色和 32 个染色细胞，得到 308/340=0.905882，即 90.59%。在两类共享相同稀释和体积时，这些因子相消。

## 数得更多、稀释重数，分别解决什么问题

只在一个很小视野里数几个细胞，就像只观察一小段街道来估计整座城市的人口，随机波动会比较大。在分散均匀、细胞近似独立进入计数体积的理想情况下，累计计入数量越多，相对随机波动越小：计入一百个时的理想尺度约为百分之十，四百个时约为百分之五。这个关系解释了为什么增加计数面积或重复装板能提高统计精度。它处理的是随机抽样波动，不能自动修正盖玻片深度错误、团聚漏计或全部样品都少乘了一个稀释倍数。

$$
\sigma_N=\sqrt{\mu},\qquad \mathrm{CV}\approx\frac{1}{\sqrt{N}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c80d13437e108b7ecd5e7468.svg) | 理想泊松计数的标准差，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 同一取样条件下的期望计数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 实际累计计数，用作期望计数的估计，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd8c772d1a9221850e1289c.svg) | 相对标准差，无量纲，乘 100% 写成百分比。 |

均匀悬液中近似独立抽样时，泊松分布的方差等于均值。计入 100 个时 CV≈0.10，400 个时≈0.05。此随机尺度不包含混匀、深度、稀释或分类的系统偏差。

重复性与准确性也应分开。一个设置错误的自动计数器可能每次都给出非常接近的值，却稳定地漏掉一类细胞；人工计数也可能因为两个人采用不同边界或形态规则而系统不同。检查自动图像中的识别边界、对象尺寸范围和染色分类，可以把算法输出对应回真实对象。对不同大小或不同处理状态的细胞，原先合适的参数未必仍然合适。选择计数方法时，比较完整过程的样品准备、识别规则和重复结果，比只比较仪器名称更有用。

![A 保留逐格原始计数；B 展示理想随机计数的相对标准差；C 用构造的拥挤漏计展示稀释系列怎样识别非比例响应。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c1fddad40e3ae34728429743.svg?v=c1fddad40e3a)

图 4A 保留逐格原始计数；B 展示理想随机计数的相对标准差；C 用构造的拥挤漏计展示稀释系列怎样识别非比例响应。

稀释系列提供另一种内部检查。同一均匀原液按不同已知比例稀释，理想测得浓度应按相同比例变化；乘回稀释倍数后，应得到相近的原液估计。若高浓度样品系统偏低，而适当稀释后估计上升，可能存在重叠、团聚或识别饱和。若低浓度样品偏高，则可以检查背景碎片和非细胞对象。NIST 研究团队在 2017 年将受控稀释、重复样品和统计分析结合，用于评价计数过程的精度与比例一致性。这个思路不需要先把某一种日常方法指定为绝对正确的参照。

稀释检查也依赖自己的实验条件。原液必须在取样时保持均匀，加入体积要准确，稀释不能明显改变细胞聚团或活性，否则浓度变化同时包含了处理变化。重复独立配制的稀释液，与对同一稀释液反复读数，能分别观察准备和读取两个层次的变异。实验中还可以记录随等待时间的读数变化，以检查沉降或染色时间的影响。把误差定位到具体步骤，下一次调整才有明确方向。

还有一种容易混淆的重复，是把同一瓶悬液数了四格，当成做了四次独立细胞培养。四格可以帮助估计这份悬液的计数波动，却共享同一瓶细胞的培养历史；四个独立培养批次则能呈现批次之间的生物变化。整理结果时，可以先在每个批次内汇总多格计数，再比较批次间差异。这样的层次也会延伸到后面的成像：同一孔拍十个视野，增加了空间采样，却没有自动变成十个独立培养实验。

将不同计数结果合并时，分母也要保留。例如一个区域观察了五十个细胞，另一个观察了五百个，直接平均两个活细胞百分比会让小样本与大样本占相同权重。若目标是这两个区域合在一起的细胞比例，应把活细胞计数相加，再除以总计数之和；若目标是比较两个独立样本各自的状态，则应先保留样本级结果，再按设计汇总。合并方式由问题决定，而不是哪一种操作最方便。

## 多看一些面积，会怎样改变计数结果？

这里每格为 10⁻⁴ mL。调整累计计数、格数和稀释倍数，比较原液浓度与理想随机波动。“面积加倍”采用相同密度的理想比较，同时增加面积与预计计数；它不是新的实测结果。

[Figure: 累计计数与理想相对抽样标准差的关系](https://ml-biomat.com/tutorials/experimental-methods/l01/#L01-lab)

交互图把取样面积与浓度换算分开。保持理想细胞密度不变时，增加观察面积会让预计计入的数量增加，推算浓度保持相同，而相对抽样波动减小。改变稀释倍数则是在同一个计数结果上，改变它与原液之间的换算关系。先分别试这两种操作，再组合起来，就能看清“数得更多”和“原液更浓”为什么是两个不同的判断。

## 从每毫升多少个，走到每孔真正放进去多少个

计数之后，接种就是一个浓度与体积的守恒计算。假设希望每孔一万个膜完整细胞，每孔加一百微升，则工作悬液需要每毫升十万个。前面得到的原液浓度是每毫升 154 万个，所以只需取一定体积原液，再加入培养基稀释。若计划十二孔，并为移液损耗准备百分之十余量，总工作液体积为 1.32 毫升，所需原液约 85.7 微升，培养基约 1.234 毫升。余量增加的是可分配的总量，不应改变目标浓度或每孔目标数。

$$
C_w=\frac{N_w}{V_w},\qquad V_f=n_wV_w(1+r),\qquad C_sV_s=C_wV_f,\qquad V_m=V_f-V_s
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | 目标工作悬液浓度，个/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/324c7d23fe8b6b2221fa0192.svg) | 每孔目标细胞数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec72cf11e28fd771d0f29c76.svg) | 每孔分配体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d13c340035341c4ed1de3a2.svg) | 准备的最终工作液体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b794cb38c00fee5cea77f6d.svg) | 计划孔数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 额外准备比例，无量纲；10% 写成 0.1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | 原液膜完整细胞浓度，个/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 此配液公式中的原液取样体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d26d844b3e76efe75c6582e5.svg) | 加入培养基体积，mL。 |

守恒假设配液期间细胞数不显著变化且均匀分散。每孔 10⁴ 个、0.1 mL、12 孔、10% 余量给出 C_w=10⁵ 个/mL，V_f=1.32 mL。C_s=1.54×10⁶ 时，V_s=0.085714 mL=85.714 μL，V_m=1.234286 mL。此处 V_s 指取样体积，与 E1 的格体积按各公式定义区分。

换算时始终保留单位：一毫升等于一千微升，一百微升就是 0.1 毫升；每毫升细胞数乘毫升体积，得到的才是细胞数。如果所需原液体积小到现有移液工具难以准确操作，可以先做一次已记录倍数的中间稀释，再完成配液。这样调整的是操作路径，目标细胞数与最终浓度保持相同；计数误差与移液误差也能分别追踪。

配好以后还要让每孔获得相近的样本。细胞在分装过程中可能沉降，若从第一孔到最后一孔始终不再温和混匀，各孔数量就可能沿操作顺序变化。吸头残留、分装速度和气泡也会影响小体积操作。较多孔时可以按合理批次混匀和分装，并检查开始与结束时的代表性样本。对于贴壁培养，接种后移动培养板的方式可能使细胞聚在中心或边缘；先观察实际分布，再决定后续成像的位置和数量。

培养板本身也有空间结构。边缘孔与中央孔可能经历不同蒸发和温度变化，若把所有对照都放在一边、所有处理都放在另一边，位置效应就与处理效应重合。图中的构造热图展示了这种混杂，旁边的布局将处理分散到多个位置。实际设计可以采用随机化或按行列分块，并让必要对照覆盖不同区域。成像时同样需要预先规定视野选择方式，避免只拍细胞最密、最整齐或最符合预期的区域。

![A、B 从普通轴与半对数轴阅读构造增长曲线；C 为构造的位置效应，D 将处理随机分散到孔位。图中的随机布局未强制每个边缘位置数量相等。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0b601f1731a6074a7a3a8edc.svg?v=0b601f1731a6)

图 5A、B 从普通轴与半对数轴阅读构造增长曲线；C 为构造的位置效应，D 将处理随机分散到孔位。图中的随机布局未强制每个边缘位置数量相等。

“接种了一万个”仍然需要与“附着了多少”区分。对材料表面，可以在适当时间测上清中未附着细胞、观察表面分布，或通过经过验证的收集方法估计附着群体。三维支架中细胞可能进入内部，表面二维图像应与深度信息或整体回收结合。若两种材料的初始保留率不同，后期数量差异就同时包含接种保留与后续增殖。增加一个接种后早期的基线测量，往往能把这两个阶段清楚分开。

## 让数量、状态与后续实验自然衔接

完整示例从四格原始计数计算浓度、膜完整比例和配液体积，再画出随机计数尺度、稀释系列诊断、增长曲线与培养板布局。所有模拟曲线都明确标为构造示例，计数板照片则展示真实器具。程序导出的计数表保留每一格的未染色、染色与总数，便于读者从原始记录重算。数值检查分别验证观察体积、活细胞浓度、接种守恒与群体倍增关系，使“每孔多少个”可以回溯到“实际数了哪些细胞”。

### 从原始计数到可比较的接种

完整示例导出逐格 CSV、计数与配液结果及五幅图。增长和位置效应为明确标注的构造示例，照片及授权说明随代码提供。

```
"""Counting-volume arithmetic, sampling variation and comparable culture starts."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(1010);live=np.array([72,81,76,79]);dead=np.array([8,9,7,8]);dilution=2;volume=1e-4;live_c=live.mean()*dilution/volume;total_c=(live+dead).mean()*dilution/volume;viability=100*live.sum()/(live+dead).sum()
    np.savetxt(output/'counts.csv',np.column_stack([np.arange(1,5),live,dead,live+dead]),delimiter=',',header='square,membrane_intact_count,stained_count,total_count',comments='',fmt='%d')
    fig,ax=plt.subplots(1,2,figsize=(11.3,4.4))
    for a in ax:a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
    for a,ratio in zip(ax,[2,8]):
        a.add_patch(Rectangle((.5,3),2,2,facecolor='#a2cdd9'));a.text(1.5,4,tr('起始细胞','Starting cells'),ha='center',va='center',fontsize=9);a.add_patch(FancyArrowPatch((2.8,4),(5,4),arrowstyle='->',mutation_scale=20));a.add_patch(Rectangle((5.5,2),4,4,facecolor='#a2cdd9'));a.text(7.5,4,tr(f'扩增 {ratio} 倍',f'{ratio}-fold expansion'),ha='center',va='center');a.set_title(tr(f'一次传代，分配比例 1:{ratio}',f'One passage, split ratio 1:{ratio}'));a.text(5,1,tr(f'理想净群体倍增数：{np.log2(ratio):g}',f'Ideal net population doublings: {np.log2(ratio):g}'),ha='center');
    fig.text(.5,.01,tr('1961 年 Hayflick 与 Moorhead 的有限增殖研究，让培养历史成为生物学变量。','Hayflick and Moorhead’s 1961 finite-proliferation work made culture history a biological variable.'),ha='center',fontsize=10);save(fig,'history')
    fig,ax=plt.subplots(1,2,figsize=(10.6,4.8));a=ax[0]
    for z in np.linspace(0,1,5):a.axvline(z,color='#a6b8bf');a.axhline(z,color='#a6b8bf')
    pos=rng.uniform(.03,.97,(45,2));a.scatter(pos[:,0],pos[:,1],s=40,facecolor='#a2cdd9',edgecolor='#186e83');a.scatter([.2,.66,.84],[.3,.57,.8],s=45,color='#8160a1');a.set(xlim=(-.1,1.1),ylim=(-.1,1.1),aspect='equal',xlabel=tr('宽度 / mm','Width / mm'),ylabel=tr('高度 / mm','Height / mm'),title=tr('A  一大格面积为 1 mm²','A  One large square has area 1 mm²'))
    a.plot([0,1],[1,1],color='#3c8a6a',lw=3);a.plot([0,0],[0,1],color='#3c8a6a',lw=3);a.plot([0,1],[0,0],color='#cd803f',lw=3);a.plot([1,1],[0,1],color='#cd803f',lw=3)
    a=ax[1];a.axis('off');a.add_patch(Rectangle((.1,.35),.8,.2,facecolor='#c9e3e9',edgecolor='#186e83'));a.plot([.05,.95],[.57,.57],color='#8160a1',lw=5);a.text(.5,.7,tr('盖玻片固定深度：0.1 mm','Coverslip fixes depth: 0.1 mm'),ha='center',fontsize=11);a.text(.5,.2,'1 mm × 1 mm × 0.1 mm\n= 0.1 mm³ = 10⁻⁴ mL',ha='center',fontsize=14);a.set_title(tr('B  从面积到已知体积','B  From area to a known volume'));fig.tight_layout();save(fig,'chamber')
    fig,ax=plt.subplots(1,3,figsize=(12,4.4));ax[0].bar(np.arange(1,5),live,label=tr('未染色','Unstained'));ax[0].bar(np.arange(1,5),dead,bottom=live,label=tr('染色','Stained'));ax[0].set(xlabel=tr('计数大格','Counting square'),ylabel=tr('细胞计数','Cell count'),title=tr('A  四格的原始计数','A  Raw counts in four squares'));ax[0].legend(fontsize=9)
    events=np.array([25,100,400,1600]);ax[1].plot(events,100/np.sqrt(events),'o-');ax[1].set(xscale='log',xlabel=tr('累计计入的细胞数','Total counted cells'),ylabel=tr('理想相对标准差 / %','Ideal relative SD / %'),title=tr('B  随机计数的不确定性尺度','B  Scale of random counting uncertainty'))
    fraction=np.array([.1,.25,.5,1]);truth=1.7e6*fraction;biased=truth/(1+truth/3e6);ax[2].plot(fraction,truth/1e6,'o-',label=tr('成比例响应','Proportional response'));ax[2].plot(fraction,biased/1e6,'s-',label=tr('构造的高密度漏计','Constructed crowding undercount'));ax[2].set(xlabel=tr('原液所占体积分数','Stock fraction in dilution'),ylabel=tr('计数浓度 / 10⁶ mL⁻¹','Counted concentration / 10⁶ mL⁻¹'),title=tr('C  稀释检验响应是否成比例','C  Dilution tests proportionality'));ax[2].legend(fontsize=8);fig.tight_layout();save(fig,'counting')
    t=np.linspace(0,120,241);exp=20000*2**(t/24);logistic=200000/(1+9*np.exp(np.log(2)*(-t)/24));fig,ax=plt.subplots(2,2,figsize=(11.2,7.2));ax=ax.ravel();ax[0].plot(t,exp,label=tr('持续指数增长','Continued exponential growth'));ax[0].plot(t,logistic,label=tr('构造的容量受限增长','Constructed capacity-limited growth'));ax[0].set(xlabel=tr('培养时间 / h','Culture time / h'),ylabel=tr('细胞数','Cell number'),title=tr('A  同一起点，不同后期条件','A  Same start, different later conditions'));ax[0].legend(fontsize=8)
    ax[1].semilogy([0,24,48,72],[20000,40000,80000,160000],'o-');ax[1].set(xlabel=tr('培养时间 / h','Culture time / h'),ylabel=tr('细胞数（对数轴）','Cell number (log scale)'),title=tr('B  等时间倍增在半对数图上成直线','B  Equal-time doubling gives a straight semilog line'))
    plate=np.ones((8,12));plate[[0,-1],:]=1.15;plate[:,[0,-1]]=1.15;plate+=rng.normal(0,.025,plate.shape);im=ax[2].imshow(plate,cmap='cividis',vmin=.9,vmax=1.2);fig.colorbar(im,ax=ax[2],label=tr('相对读数','Relative readout'));ax[2].set(xticks=range(12),xticklabels=range(1,13),yticks=range(8),yticklabels=list('ABCDEFGH'),title=tr('C  构造的板边位置效应','C  Constructed plate-edge position effect'))
    treatments=np.tile(np.arange(4),24);rng.shuffle(treatments);layout=treatments.reshape(8,12);ax[3].imshow(layout,cmap=plt.colormaps['Set2'].resampled(4),vmin=-.5,vmax=3.5)
    for row in range(8):
        for col in range(12):ax[3].text(col,row,'ABCD'[layout[row,col]],ha='center',va='center',fontsize=8)
    ax[3].set(xticks=range(12),xticklabels=range(1,13),yticks=range(8),yticklabels=list('ABCDEFGH'),title=tr('D  处理组分散到不同位置','D  Treatments distributed across positions'));fig.tight_layout();save(fig,'culture')
    from PIL import Image
    fig,ax=plt.subplots(figsize=(9,5.9));ax.imshow(Image.open(Path(__file__).with_name('hemocytometer-todd.jpg')));ax.axis('off');ax.set_title(tr('真实计数板：精确体积来自玻璃结构与盖玻片','A real counting chamber: geometry and coverslip define volume'),fontsize=12,pad=10);fig.text(.5,.01,'Todd · Hemocytometer · Wikimedia Commons · CC BY-SA 2.0',ha='center',fontsize=9);save(fig,'instrument')
    final_volume=12*.1*1.1;stock_volume=final_volume*1e5/live_c;summary={'counting':{'volume_per_square_ml':volume,'mean_live_per_square':float(live.mean()),'live_concentration_ml':float(live_c),'total_concentration_ml':float(total_c),'viability_percent':float(viability),'live_cells_in_2ml':float(live_c*2)},'seeding':{'target_per_well':10000,'final_volume_ml':final_volume,'stock_volume_ul':float(stock_volume*1000),'medium_volume_ml':float(final_volume-stock_volume)},'growth':{'initial_cells':20000,'cells_at_48h':80000,'doublings':2,'doubling_time_h':24},'sampling':{'relative_sd_100':.1,'relative_sd_400':.05},'dilution':{'true_stock_ml':1700000,'crowded_stock_measured_ml':float(biased[-1])}}
    assert abs(live_c-1540000)<1e-8;assert abs(stock_volume*live_c-final_volume*1e5)<1e-8;assert abs(np.log2(80000/20000)-2)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

可以先把稀释倍数由二改为四，观察推算原液浓度怎样变化；然后固定原液浓度，只改变目标接种数，检查需要的原液体积。再比较相同总计数分布在不同格子的情况：均值可能相同，空间差异却提示混匀或装样状态不同。对于实际实验，保留独立培养批次、材料编号和孔位，再将后续活死染色、代谢读数或DNA合成结果接到这些编号上，便能从共同起点追踪不同层次的细胞反应。

本节最终形成的结果不只是一个细胞浓度，而是一个有定义的实验起点：细胞身份清楚、培养状态可比较、数量和膜完整状态已测、材料上的实际分布得到观察。后面的活死染色会把细胞状态放回空间图像中，DNA 合成实验则观察哪个群体正在复制遗传物质。不同方法回答不同问题，但都受益于这里建立的数量、时间与空间记录。将这些记录放在同一条实验逻辑里，材料和生物之间的关系才会逐步清楚。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [ATCC: Animal Cell Culture Guide](https://www.atcc.org/resources/culture-guides/animal-cell-culture-guide)

   细胞培养、倍增、计数室几何与计数准备。
2. [ATCC: Cell Line Authentication Test Recommendations](https://www.atcc.org/resources/technical-documents/cell-line-authentication-test-recommendations)

   身份检测与日常形态、培养记录的互补关系。
3. [ATCC: Mycoplasma Contamination](https://www.atcc.org/the-science/authentication/mycoplasma-contamination)

   清澈外观与常用抗生素不能替代支原体检测。
4. [Thermo Fisher: Manually Counting Cells in a Hemocytometer](https://www.thermofisher.com/us/en/home/references/gibco-cell-culture-basics/cell-culture-protocols/counting-cells-in-a-hemacytometer.html)

   观察体积、稀释与原液浓度换算。
5. [Sarkar et al. (2017): Evaluating the quality of a cell counting measurement process via a dilution series experimental design](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=921053)

   独立稀释、重复测量、比例响应与精度评价。
6. [Hayflick and Moorhead (1961): The serial cultivation of human diploid cell strains](https://doi.org/10.1016/0014-4827%2861%2990192-6)

   正常二倍体细胞有限增殖能力的历史研究。
7. [Hayflick: Citation Classic retrospective](https://garfield.library.upenn.edu/classics1978/A1978FC39200002.pdf)

   原作者回顾有限细胞培养研究的科学背景。
8. [Todd: Hemocytometer photograph](https://commons.wikimedia.org/wiki/File:Hemocytometer.jpg)

   真实计数器具照片与作者、许可记录。

   CC BY-SA 2.0 photograph by Todd; composed figure also CC BY-SA 2.0.
