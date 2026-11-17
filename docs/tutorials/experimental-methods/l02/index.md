# CCK-8与MTT：颜色变化告诉了我们什么

Source: https://ml-biomat.com/tutorials/experimental-methods/l02/
Language: zh-CN

一孔颜色背后有细胞数量、代谢和材料背景。沿着显色反应、孔板对照与剂量曲线，学会计算并解释一个有明确含义的百分数。

## 1. 一孔颜色变浅，细胞究竟发生了什么

研究一种新水凝胶时，我们常希望先知道它与细胞相处得怎样。把细胞接触材料后的培养液加入显色试剂，过一段时间，某些孔变成较深的橙色，另一些孔颜色很浅。酶标仪再把颜色差别变成一列吸光度数值，这就是许多人第一次遇见CCK-8实验的样子。它操作方便，也容易让人立刻把颜色深浅理解成“活细胞多或少”。要把这组数用好，还需要补上颜色与细胞之间的几步联系。

CCK-8和MTT都借助细胞相关的还原过程生成有颜色的产物。还原可以先理解为一个分子获得电子；活跃的细胞代谢会不断转移电子，显色反应利用其中的一部分形成可检测信号。因此，一孔中的总颜色同时受到细胞数量、每个细胞的代谢状态、显色时间和实验环境影响。用一家餐馆作类比，总营业额既受顾客数量影响，也受每位顾客的消费额影响。只看营业额，需要了解人均消费是否稳定，才能估计顾客数量。

这一关系决定了实验适合怎样使用。比较同一细胞类型、相同培养阶段与显色条件下的材料处理，可以把相对代谢响应作为重要的初步表征；结合细胞计数、膜完整性染色或DNA复制测量，就能进一步分清数量变化、细胞状态变化和增殖变化。例如，处理后信号降到一半，可能有较少细胞留在孔中，也可能细胞仍在但单细胞代谢减弱。后一种情况同样具有生物学意义，只是需要用与实际读出相符的名称描述。

本篇从显色反应和酶标仪讲起，再设计一块包含匹配空白的实验板，最后分析三次独立实验。贯穿始终的问题是：一个看起来简单的百分数，怎样保留它真正代表的生物学含义？你会看到材料本身的颜色怎样把结果抬高，也会看到同一个剂量—响应曲线上，两种常被叫作“50%”的位置为什么并不重合。完整程序与图中的数值对应，可以逐步改动条件观察结果。

## 2. 从MTT到WST-8：把细胞过程接到一块微孔板上

1983年，Mosmann发表了适于比较细胞生长与存活相关响应的MTT比色方法。微孔板让许多平行条件能够在相近的操作流程中比较，比逐个观察和计数更便于扩大实验规模。它也把一个重要问题带到了台前：显色信号与细胞状态有关，要知道正在比较的是哪一种细胞过程。历史上还存在检测DNA合成的放射性胸腺嘧啶核苷掺入方法；两者都曾服务于增殖研究，但一个关注还原活动，一个关注DNA合成，读出的生物学环节各有侧重。

![MTT的微孔板比色思路与WST-8可溶性产物检测的原创示意。MTT结晶需要适当溶解，WST-8体系通过电子介体连接细胞相关还原过程。图示测量链，不把全部反应归于一种细胞器。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4cf820aa45750c4acfab1e82.svg?v=4cf820aa4575)

图 1MTT的微孔板比色思路与WST-8可溶性产物检测的原创示意。MTT结晶需要适当溶解，WST-8体系通过电子介体连接细胞相关还原过程。图示测量链，不把全部反应归于一种细胞器。

MTT属于四唑盐，细胞相关的还原过程使其转变成有色甲臜。这个名称可以先看作显色产物的类别，不必从完整化学名称背起。MTT甲臜溶解性较低，会形成结晶，因此通常需要增加溶解步骤，再测定溶液的吸光度。若结晶没有充分溶解，局部颗粒和不均匀颜色就会影响读数。这个环节把化学产物的物理性质与操作联系起来：同样数量的产物，分散在均匀溶液里和留成不规则结晶时，光学测量的条件并不相同。

CCK-8使用WST-8体系，借助电子介体把细胞相关的还原能力连接到可溶性甲臜的生成。电子介体可以理解为在反应伙伴之间传递电子的中间参与者。产物能留在培养液中，使显色后读数更直接。常见CCK-8读数波长为450 nm，MTT溶解产物常在570 nm附近测量；具体主波长、参比波长和流程应与使用的体系相对应。它们检测的仍是一个化学反应的光学结果，因此试剂选择也要结合样品颜色、材料组成和计划研究的细胞过程。

把还原反应全部画进一颗线粒体里，会使机制显得过于简单。细胞中有多种参与电子转移的酶和还原性分子，培养状态与处理条件都可能改变它们的贡献。生物材料还会在细胞之外参与实验：还原性组分可能直接促使试剂显色，深色颗粒可能吸收或散射检测光，某些表面可能吸附试剂或产物。实验设计的任务，是把这些可测的材料贡献与细胞相关信号分开，并在需要时选择另一种生物学读出补充解释。

## 3. 酶标仪读取的是光，生物学解释从光以后开始

酶标仪让选定波长的光经过孔内液体，再测量到达探测器的光。液体中的显色产物吸收了一部分光，仪器通过样品与参考光强的比例计算吸光度。颜色越深，某些波长透过的光越少。吸光度本身没有“细胞数”的单位，只有先通过已知数量的细胞建立对应关系，才能在相近条件下把它换算成数量。这个对应关系应针对细胞类型、培养状态和反应时间检查，而不是把试剂盒名称当作通用的计数换算表。

$$
A=-\log_{10}\!\left(\frac{I}{I_0}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 通过孔内液体后测得的光强，单位与I₀相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 对应参考光强，光强比应为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以10为底的对数。 |

透过光为参考的50%时，A≈0.301。吸光度来自光强比的对数；样品与空白的吸光度可以相减，是在匹配条件下比较附加的吸收贡献。它本身没有细胞数单位。

微孔中的光程与液体体积、孔形和读数方式有关。加液体积不一致会同时改变反应物比例和光学条件；气泡则让光束遇到额外界面。把一块板中各孔的最终体积、混匀方式和读数前处理保持一致，有助于让差别更多地来自待比较的样品。对有浑浊颗粒的材料，可以记录参比波长响应并检查颗粒分布，但参比扣除的效果仍取决于材料在两个波长处的光学行为，不能简单假设所有背景都以相同方式变化。

显色时间也是实验条件，而不是最后等待的一段空白时间。较短时间内，产物可能近似稳定地积累，信号随时间增加；时间过长后，底物、细胞状态和检测范围都可能改变。若逐列加试剂，却在整块板加完后立刻同时读数，第一列和最后一列实际经历的显色时间就不同。多道移液、固定的加样顺序、适当的分批读数或经过验证的终止方式，都可以使计划中的时间与实际经历的时间更接近。

铺板数量与显色时间应当一起摸索。少量细胞配很短时间，信号可能接近背景；大量细胞配很长时间，响应可能进入弯曲区。图中稍后给出的数量—时间曲线展示了这一点。一个合适的工作区间应使目标数量范围内的差别能够稳定区分，同时保留一定上下余量。先做小范围细胞数量梯度，再用两个或多个显色时间比较，是建立这张实验“刻度尺”的直接方法。

三维水凝胶又多了一层空间问题。试剂需要从外部溶液进入网络，产物也要在适合读数的位置积累；凝胶厚度、孔隙结构与细胞分布都会影响这个过程。两个含有相同数量细胞的凝胶，如果一个很薄、另一个很厚，在相同短时间内可能形成不同的读数。可以先比较厚度与显色时间梯度，再结合切片或三维成像检查细胞分布。把薄层培养中建立的数量—信号关系用于三维样品前，需要让取样与传质条件也进入标定设计。

## 4. 为材料实验安排真正匹配的空白

设想一种有颜色的材料，浓度越高，培养液在450 nm处吸光越明显。如果所有处理孔都只减去“培养基加试剂”的同一个空白，高浓度材料自身的颜色仍会留在结果中。即使细胞相关信号正在下降，总吸光度也可能看起来下降得较少，甚至上升。解决这个问题要从实验板开始：每个材料浓度都设置没有细胞、其他组成和处理过程尽可能匹配的孔，用它测量材料与试剂在该条件下共同贡献的背景。

![构造的第一次独立实验：48个使用孔随机分布，圆圈标记无细胞匹配空白。右图保留原始含细胞信号、匹配空白与差值，显示材料浓度变化如何进入读数。灰色孔未使用。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6e0fcc6285ba1fc2a1a729b4.svg?v=6e0fcc6285ba)

图 2构造的第一次独立实验：48个使用孔随机分布，圆圈标记无细胞匹配空白。右图保留原始含细胞信号、匹配空白与差值，显示材料浓度变化如何进入读数。灰色孔未使用。

本例的细胞孔含有细胞、材料和显色试剂；对应空白孔含有相同材料浓度、培养液和试剂，但没有细胞。零材料浓度的细胞孔是本次实验的参照，零浓度的无细胞孔提供其背景。三类信息共同构成反算所需的分子和分母。若实验还涉及溶剂，参照孔也应包含与处理孔相匹配的溶剂条件；如果要确认体系能够检出明显的响应下降，可以安排已知能改变该读出的对照，并使其用途和处理条件明确。

匹配空白最直接处理的是可相加的背景。例如，一部分材料本身的光吸收可以在无细胞孔中测到，再从含细胞孔的响应中扣除。若材料吸附显色产物，情况就不再只是增加一个背景数值：同样生成的产物可能有不同的回收率。可以向含材料和不含材料的体系加入可比较的产物或信号标准，检查信号回收；也可以结合显微计数等另一种读出，判断材料与检测化学的相互作用。这样，每个额外对照都有一个具体要解决的问题。

排板还需要照顾位置。孔板边缘的蒸发和温度条件可能与中间不同，如果所有高浓度样品都放在一侧，位置变化就会与剂量变化混在一起。本例将48个使用孔随机安排在96孔板中，并保存每个孔的行列、条件与重复编号。实际实验可以采用随机化或平衡分块，同时根据所用细胞和培养时长控制边缘效应。颜色热图既帮助检查读数，也能让连续一行异常、局部异常或加样顺序相关的模式显现出来。

$$
R=100\,\frac{A_s-A_{bs}}{A_c-A_{bc}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 相对代谢响应，以%为单位表示的数值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33fe913a815d09d9b267ca3d.svg) | 处理细胞孔的平均吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f4621c2ce242814ee1f6cada.svg) | 与处理浓度匹配的无细胞孔平均吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | 同一次实验参照细胞孔的平均吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e60fe3eaa0f62628aab7f65.svg) | 参照条件的无细胞空白平均吸光度，无量纲。 |

取Aₛ=0.54、Aᵦₛ=0.14、A꜀=0.84、Aᵦ꜀=0.04，得到100×0.40/0.80=50%。分母是同次实验中正的、可分辨的参照信号；扣除假定匹配空白能代表可相加背景。

用一组小数算一次就容易看清。处理孔吸光度为0.54，匹配材料空白为0.14；参照细胞孔为0.84，参照空白为0.04。处理组的细胞相关信号是0.40，参照组是0.80，相对响应为50%。如果处理孔也只减0.04，会得到62.5%。这12.5个百分点的差别完全来自背景处理，尚未涉及任何新的细胞机制。计算前把每一项对应到实验板里的实际孔，能很快发现遗漏了哪一种对照。

当细胞相关信号接近背景波动时，两个测量值相减可能出现小的负数。它表示差值落在零附近的噪声范围内，而不是出现负数量的细胞。先保留原始差值，检查匹配空白的散布和可分辨信号范围；直接把所有负值改成零，会让平均响应向上偏移，也会隐藏这一区域的测量精度。

## 5. 细胞数量、代谢和重复，怎样分别解释

在经过验证的近似线性区间，可以把信号拆成几个相乘的因素：细胞数量、平均单细胞反应速率和显色时间，再乘上把产物量换成吸光度的比例系数。这个简化关系的用途是帮助判断变量，而不是把复杂的细胞代谢压成一个恒定参数。如果某种处理让细胞数量减半，同时让剩余细胞的平均显色速率增加到两倍，总信号仍可能不变。若处理主要改变代谢而不是数量，结果也可以被描述为代谢响应变化，再安排与数量或膜完整性相关的实验继续追踪。

$$
S\approx\kappa N q t
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 扣除匹配空白后的吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | 参考单细胞活性下的信号比例系数，单位cell⁻¹·h⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 参与反应的细胞数量，单位cell。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 相对于参考状态的平均单细胞反应活性，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 显色时间，单位h。 |

在合适的线性工作区间，κ=4×10⁻⁵ cell⁻¹·h⁻¹、N=5000、q=1、t=2 h给出S=0.40。若N=2500而q=2，S仍为0.40。模型假定反应速率、传质和光学条件支持这一近似，用来分清数量与单细胞状态的共同影响。

活性、存活和增殖这些词需要联系到测量对象。膜完整性染色关注细胞膜能否阻挡某些染料；EdU实验关注一段时间内的DNA合成；计数关注可识别细胞的数量；CCK-8和MTT关注细胞相关的还原显色响应。把这些结果放在一起，可以提出更具体的解释。例如，细胞数变化不大、显色响应下降而膜完整性保持，提示应进一步关注代谢状态或检测化学；若数量、显色响应和膜完整性都改变，则有不同的证据组合需要解释。

重复也有不同层次。同一次铺板中三个相同条件的孔，主要帮助估计加液、孔间状态和读数的技术变化。另一天独立准备细胞与处理条件，再完整做一次实验，才提供另一层实验间变化的信息。是否独立取决于具体制备过程，而不仅是文件里是否写了不同日期。本例把三次独立构造实验作为统计单位，每次实验中的三个技术孔先求均值，再做匹配空白扣除和参照归一化，最后比较三次实验的结果。

归一化以后，每次实验的零剂量参照都恰好等于100%，这是公式的定义造成的。它并不意味着原始参照孔没有波动；原始孔的差异保留在吸光度表中，并参与了其他剂量的分母。图中画出的误差条是三个独立实验结果的样本标准差，用来描述这三次结果的散布。把九个技术孔直接当成九个独立实验，会把孔之间共享的培养与处理条件忽略掉，使不确定性的表达偏离实验结构。

![四个互相衔接的问题：A为简化的数量—时间响应模型；B展示数量减半、单细胞活性加倍时信号相同；C比较三次独立构造实验与共同空白分析；D以三次独立实验均值和日间样本标准差展示剂量曲线。零剂量参与计算，在对数图D中未显示。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d8465560aa87dac2a3953147.svg?v=d8465560aa87)

图 3四个互相衔接的问题：A为简化的数量—时间响应模型；B展示数量减半、单细胞活性加倍时信号相同；C比较三次独立构造实验与共同空白分析；D以三次独立实验均值和日间样本标准差展示剂量曲线。零剂量参与计算，在对数图D中未显示。

在最高的50 μg/mL材料浓度处，本例经过匹配空白校正后的平均相对代谢响应约为21.45%，只减共同空白则得到约37.46%。三条独立实验曲线同时展示了实验间差别，比只画一根平均柱更容易判断结果是否一致。这里所有细胞与吸光度数据均为构造例子，生成规则明确保存。它把背景带来的影响单独放大，让读者先掌握分析逻辑，再把同样的表格结构用于自己的真实实验。

## 6. 剂量—响应曲线上的两个“50%”

把材料浓度放在横轴、相对响应放在纵轴，常会看到一条先较平缓、随后下降、再逐渐接近低平台的曲线。浓度跨越较大范围时，对数横轴能把低浓度部分展开；零浓度无法放在对数轴上，因此它仍参与参照与拟合，但在对数图中另行说明或不显示。曲线拟合的价值是概括变化范围与位置，让不同条件下的响应能够按明确定义比较，而不是自动给每条曲线贴上同一种机制解释。

$$
y(c)=L+\frac{U-L}{1+(c/K)^h},\qquad y(K)=\frac{U+L}{2},\qquad c_{y=50}=K\left(\frac{U-50}{50-L}\right)^{1/h}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 材料暴露浓度，本例单位μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/014d06406569aa2ddd6cfa41.svg) | 该浓度下拟合的相对响应，以%为单位表示的数值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/00d614107d5e3a57ff52ec95.svg) | 拟合上平台与下平台，与y使用相同的百分数尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 拟合动态范围中点浓度，单位μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 控制曲线陡峭程度的正坡度参数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6b482d895dca66782c68edea.svg) | 响应达到参照50%的浓度，单位μg/mL；存在条件为L<50<U。 |

本例拟合U≈99.81、L≈16.03、K≈7.86、h≈1.442。动态范围中点响应约57.92%，而y=50对应浓度约10.25 μg/mL。式中50表示响应尺度上的50%；浓度比c/K无量纲，才能取幂。

四参数模型用上平台、下平台、动态范围中点的浓度和坡度描述曲线。令浓度等于中点参数时，分母中的浓度比等于1，响应自然位于上下平台的平均值。若上平台为100%、下平台为20%，这个中点就是60%，并不是50%。这段很简单的代数解释能避免一种常见误读：软件给出的半最大参数，可能指拟合动态范围走过一半的位置；“相对未处理对照降到50%”则指纵轴达到50的位置。

在本例拟合中，上平台约99.81%，下平台约16.03%，动态范围中点浓度约7.86 μg/mL，而达到对照50%响应的浓度约10.25 μg/mL。图中两条水平线分别标记这两种定义。报告结果时，可以直接写清“拟合动态范围中点浓度”或“相对参照降至50%的浓度”，让数字的含义随名称一起交代。如果实验剂量尚未覆盖下平台，就应增加适合的浓度范围或选择更符合已有数据的问题，避免让没有被观察的远端曲线主导参数。

坡度参数描述过渡区有多陡，但它并不单独确定细胞内发生了什么。材料分散、释放过程、细胞群体差异以及检测化学都可能改变观测到的曲线形状。比较不同材料时，还应把接触时间、浓度单位、细胞类型、直接接触或浸提处理方式一起写清。例如，相同的质量浓度对不同粒径颗粒可能对应不同的表面积；这些信息决定两条曲线究竟在比较什么实验条件。

横轴浓度还要对应实际接触阶段。把10 μL、浓度100 μg/mL的材料悬液加入90 μL培养液，混合后的材料浓度是10 μg/mL，因为材料总量分布在100 μL里。随后加入检测液又会改变读数阶段的体积，但材料暴露阶段的剂量定义应当保持清楚。若材料会沉降或吸附在孔底，名义加入浓度和细胞附近实际经历的条件还会有差别；记录混匀、分散与接触几何，有助于解释不同实验之间的曲线变化。

## 7. 从孔板原始读数到可复查的图

完整程序生成三次独立实验，每次含八个材料浓度，每个浓度有三个细胞孔与三个匹配空白孔，共144条孔级记录。它保存孔位、材料浓度、孔类型、重复编号和原始吸光度，随后按实验和剂量分组。先对技术孔求均值，再扣除对应空白、除以本次实验的参照信号，得到每次实验的剂量曲线。最后汇总三条曲线，并拟合平均响应。这样的数据结构保留了实验层级，后续检查不必猜测某个数来自哪一次实验。

输出的热图对应第一次实验，剂量图对应三次实验的汇总；数据表同时保留校正前后两种结果。程序中的细胞数量—显色时间曲线和两组相同信号示意，使用另外注明的简化模型解释工作区间与数量—代谢混合影响，没有把这些示意当作实际细胞测量。计算摘要给出背景校正的手算例子、最高剂量响应以及两种半响应浓度，方便从图、表和公式三处相互核对。

### 完整例子：从144个孔级读数到三次实验的剂量曲线

程序生成明确标注的教学数据，输出孔级CSV、独立实验汇总、三组图和计算摘要。先校正每次实验，再汇总重复；中英文只改变图像文字。

```
"""A constructed CCK-8 plate experiment: matched blanks and independent days.

All assay values are simulated for teaching; no biological measurements are
claimed. Each of three days has its own response, and each condition has three
technical wells. Output includes raw well-level data and day-level summaries.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,FancyArrowPatch

BLUE,RED,GOLD,GREY='#12687b','#be6047','#b18a35','#758893'

def response(dose,bottom,top,half,hill):
    return bottom+(top-bottom)/(1+(np.asarray(dose)/half)**hill)

def blank_correct(sample,sample_blank,control,control_blank):
    denominator=np.asarray(control)-np.asarray(control_blank)
    if np.any(denominator<=0):raise ValueError('A positive control signal is required.')
    return 100*(np.asarray(sample)-np.asarray(sample_blank))/denominator

def run(out,lang):
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
        'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#b8c9cf',
        'svg.fonttype':'none','axes.unicode_minus':False,'savefig.facecolor':'white'})
    t=lambda z,e:z if lang=='zh' else e
    def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
    def arrow(ax,start,end):ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=16,lw=2,color=BLUE))
    rng=np.random.default_rng(83)
    doses=np.array([0,.5,1,2,5,10,20,50.])
    records=[];day_ratios=[];naive_ratios=[];means_by_day=[]
    for day in range(3):
        top_signal=.8*(1+.06*(day-1));half=8*(1+.12*(day-1))
        expected=response(doses,15,100,half,1.4)/100
        blank=.04+.0025*doses
        sample=top_signal*expected[:,None]+blank[:,None]+rng.normal(0,.012,(8,3))
        acellular=blank[:,None]+rng.normal(0,.004,(8,3))
        sample_mean=sample.mean(axis=1);blank_mean=acellular.mean(axis=1)
        ratios=blank_correct(sample_mean,blank_mean,sample_mean[0],blank_mean[0])
        naive=100*(sample_mean-blank_mean[0])/(sample_mean[0]-blank_mean[0])
        day_ratios.append(ratios);naive_ratios.append(naive);means_by_day.append((sample_mean,blank_mean))
        positions=rng.choice(96,size=48,replace=False);cursor=0
        for i,dose in enumerate(doses):
            for kind,array in [('cells',sample),('matched_blank',acellular)]:
                for rep in range(3):
                    pos=int(positions[cursor]);cursor+=1
                    records.append({'day':day+1,'well':chr(65+pos//12)+str(pos%12+1),
                        'row':pos//12,'column':pos%12,'dose_ug_ml':dose,'kind':kind,
                        'technical_replicate':rep+1,'absorbance':float(array[i,rep])})
    ratios=np.array(day_ratios);naive=np.array(naive_ratios)
    mean=ratios.mean(axis=0);sd=ratios.std(axis=0,ddof=1)
    parameters,covariance=curve_fit(response,doses,mean,p0=[15,100,8,1.4],
        bounds=([0,90,.01,.2],[50,110,100,4]),maxfev=10000)
    bottom,top,half,hill=parameters
    absolute_50=half*((top-50)/(50-bottom))**(1/hill) if bottom<50<top else None
    dense=np.geomspace(.2,80,300)

    fig,axs=plt.subplots(1,2,figsize=(12.7,5.4),layout='constrained')
    for ax in axs:ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off')
    ax=axs[0];ax.set_title(t('A  MTT：1983年的微孔板比色思路','A  MTT: a microplate color assay in 1983'),loc='left',pad=20)
    ax.add_patch(Circle((2,4.5),1.1,fc='#d9e9e3',ec=BLUE,lw=2));ax.text(2,4.5,t('细胞内\n还原过程','Cellular\nreduction'),ha='center',va='center')
    arrow(ax,(3.2,4.5),(4.7,4.5));ax.text(3.8,5,t('MTT','MTT'),ha='center')
    for x,y in [(5.4,4.6),(5.9,4.2),(6.3,4.7),(5.4,4.0)]:ax.plot(x,y,marker='D',ms=14,color='#765080')
    ax.text(5.9,3.1,t('不溶性甲臜结晶','Insoluble formazan crystals'),ha='center',fontsize=10)
    arrow(ax,(6.8,4.5),(8.3,4.5));ax.add_patch(Rectangle((8.4,3.5),1,2,fc='#baa1c7',ec=GREY));ax.text(8.9,2.7,t('溶解后读数','Dissolve, then read'),ha='center',fontsize=10)
    ax.text(.4,.9,t('把大量平行样品放进一块板里比较\n颜色产生的速度仍与细胞状态有关','Compare many parallel specimens in one plate\nColor production still depends on cellular state'),fontsize=11)
    ax=axs[1];ax.set_title(t('B  WST-8：把产物留在溶液里','B  WST-8: keep the product in solution'),loc='left',pad=20)
    ax.add_patch(Circle((2,4.5),1.1,fc='#d9e9e3',ec=BLUE,lw=2));ax.text(2,4.5,t('细胞还原力','Cellular\nreducing power'),ha='center',va='center')
    arrow(ax,(3.2,4.5),(4.5,4.5));ax.text(4.8,5.4,t('电子介体','Electron mediator'),ha='center',fontsize=10)
    ax.add_patch(Circle((5,4.5),.42,fc=GOLD));arrow(ax,(5.6,4.5),(7.2,4.5))
    ax.add_patch(Rectangle((7.3,3.5),1.5,2,fc='#e8b66c',ec=GREY));ax.text(8,2.7,t('可溶性甲臜','Soluble formazan'),ha='center',fontsize=10)
    ax.text(.4,.9,t('CCK-8通常在450 nm读取\n示意图关注测量链，不表示反应位置的全部细节','CCK-8 is commonly read at 450 nm\nA measurement-chain diagram, not every reaction site'),fontsize=11)
    save(fig,'history-chemistry')

    fig,axs=plt.subplots(1,2,figsize=(12.7,5.8),layout='constrained')
    plate=np.full((8,12),np.nan);kinds={}
    for rec in records:
        if rec['day']==1:plate[rec['row'],rec['column']]=rec['absorbance'];kinds[(rec['row'],rec['column'])]=rec['kind']
    cmap=plt.colormaps['YlOrBr'].copy();cmap.set_bad('#edf1f3')
    im=axs[0].imshow(plate,cmap=cmap,vmin=0,vmax=.9,aspect='equal')
    for (r,c),kind in kinds.items():
        if kind=='matched_blank':axs[0].plot(c,r,marker='o',ms=4,mfc='none',mec=BLUE)
    axs[0].set(xticks=np.arange(12),xticklabels=np.arange(1,13),yticks=np.arange(8),yticklabels=list('ABCDEFGH'),title=t('A  第一次实验的48个随机排布读数','A  Forty-eight randomized wells on day 1'))
    fig.colorbar(im,ax=axs[0],shrink=.7,label=t('吸光度','Absorbance'))
    axs[0].text(.5,-.16,t('圆圈：无细胞匹配空白；灰格：未使用','Circles: matched cell-free blanks; grey: unused'),ha='center',transform=axs[0].transAxes,fontsize=10)
    ax=axs[1]
    a,b=means_by_day[0]
    ax.plot(doses,a,'o-',color=RED,label=t('细胞 + 材料 + 试剂','Cells + material + reagent'))
    ax.plot(doses,b,'o-',color=GOLD,label=t('材料 + 试剂，无细胞','Material + reagent, no cells'))
    ax.plot(doses,a-b,'o-',color=BLUE,label=t('相减后的细胞相关信号','Cell-associated difference'))
    ax.set(xlabel=t('材料浓度 / μg·mL$^{-1}$','Material concentration / μg/mL'),ylabel=t('吸光度','Absorbance'),title=t('B  匹配空白随材料浓度改变','B  Matched blanks change with material dose'));ax.legend(fontsize=9);ax.grid(alpha=.13)
    save(fig,'plate-controls')

    fig,axs=plt.subplots(2,2,figsize=(12.7,8.1),layout='constrained')
    ax=axs[0,0];n=np.linspace(0,20000,200)
    for time,col in [(1,BLUE),(2,RED),(4,GOLD)]:
        signal=1.5*(1-np.exp(-.00004*n*time/1.5))
        ax.plot(n,signal,color=col,label=f'{time} h')
    ax.set(xlabel=t('每孔细胞数','Cells per well'),ylabel=t('构造的校正吸光度','Constructed corrected absorbance'),title=t('A  铺板数量与孵育时间共同影响响应','A  Cell number and incubation time act together'));ax.legend()
    ax=axs[0,1];xx=np.linspace(0,4,200)
    ax.plot(xx,.2*xx,color=BLUE,label=t('数量×单细胞活性：1×1','Number × per-cell activity: 1 × 1'))
    ax.plot(xx,.2*xx,color=RED,ls='--',lw=3,label=t('数量×单细胞活性：0.5×2','Number × per-cell activity: 0.5 × 2'))
    ax.set(xlabel=t('显色时间 / h','Color-development time / h'),ylabel=t('理想线性吸光度','Ideal linear absorbance'),title=t('B  不同细胞数量可能给出相同信号','B  Different cell counts can give the same signal'));ax.legend(fontsize=9)
    ax=axs[1,0]
    for day,col in enumerate([BLUE,RED,GOLD]):ax.plot(doses,ratios[day],'.-',color=col,alpha=.9,label=t(f'独立实验 {day+1}',f'Independent day {day+1}'))
    ax.plot(doses,naive.mean(0),'s--',color=GREY,label=t('只减共同空白','Common blank only'))
    ax.set(xlabel=t('浓度 / μg·mL$^{-1}$','Concentration / μg/mL'),ylabel=t('相对代谢响应 / %','Relative metabolic response / %'),title=t('C  每次实验先校正，再比较重复','C  Correct each day before comparing repeats'));ax.legend(fontsize=9)
    ax=axs[1,1]
    ax.errorbar(doses[1:],mean[1:],yerr=sd[1:],fmt='o',color=BLUE,capsize=4,label=t('日均值 ± 日间SD，n=3','Day means ± between-day SD, n=3'))
    ax.plot(dense,response(dense,*parameters),color=BLUE,lw=2)
    midpoint=(top+bottom)/2
    ax.axhline(midpoint,color=GOLD,ls=':',label=t('拟合动态范围的中点','Halfway through fitted dynamic range'))
    ax.axhline(50,color=RED,ls='--',label=t('对照信号的50%','50% of control signal'))
    ax.set(xscale='log',xlabel=t('浓度 / μg·mL$^{-1}$（对数轴）','Concentration / μg/mL (log axis)'),ylabel=t('相对代谢响应 / %','Relative metabolic response / %'),title=t('D  两种“50%”对应不同浓度','D  Two meanings of “50%” give different concentrations'));ax.legend(fontsize=8)
    save(fig,'response-diagnostics')

    with (out/'well-data.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    np.savetxt(out/'day-summary.csv',np.c_[doses,ratios.T,mean,sd,naive.mean(0)],delimiter=',',
        header='dose_ug_ml,day1_percent,day2_percent,day3_percent,mean_percent,between_day_sd,common_blank_only_percent',comments='')
    summary={'origin':'Constructed teaching data, seed 83; 3 independent days × 8 doses × 2 well types × 3 technical wells',
        'well_count':len(records),'independent_days':3,'technical_wells_per_condition':3,
        'worked_example_corrected_percent':float(blank_correct(.54,.14,.84,.04)),
        'worked_example_common_blank_percent':100*(.54-.04)/(.84-.04),
        'corrected_high_dose_percent':float(mean[-1]),'common_blank_high_dose_percent':float(naive.mean(0)[-1]),
        'fitted':{'bottom_percent':float(bottom),'top_percent':float(top),'half_dynamic_range_ug_ml':float(half),'hill':float(hill),'absolute_50_control_ug_ml':float(absolute_50)},
        'known_true_half_dynamic_range_ug_ml':8.0,'control_percent_each_day':ratios[:,0].tolist()}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    assert len(records)==144 and np.allclose(ratios[:,0],100)
    assert np.isclose(summary['worked_example_corrected_percent'],50,atol=1e-12)
    assert 6<half<10 and absolute_50>half
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

可以先把材料背景随浓度增加的系数改成零，观察共同空白与匹配空白两条分析结果怎样靠近；再恢复背景，增加无细胞空白的测量噪声，观察校正后的散布如何改变。这样的改动把“需要空白”变成一个可计算的原因。若把技术孔数量增加，而独立实验次数仍保持三个，图中估计的仍是三个独立实验之间的变化。技术重复改善每次实验内部的估计，独立重复则帮助了解结果跨制备条件的变化，两者承担不同作用。

## 交互实验：相同颜色，可以来自多少种细胞状态

把参照细胞相关吸光度设为0.80，培养液与试剂共同背景设为0.04。在这个线性教学模型中，独立改变细胞数量、单细胞活性与材料附加背景，比较直接读出的相对信号和匹配空白校正后的响应。

[Figure: 细胞数量、校正和未匹配空白响应的比较及数量活性关系图](https://ml-biomat.com/tutorials/experimental-methods/l02/#L02-plot)

右图颜色表示数量与活性的乘积，虚线上的不同组合都给出100%的校正响应。模型把材料作用写成可相加背景；产物吸附或传质改变需要另行检查回收与反应条件。

## 8. 把一个百分数写成清楚的实验结论

一个完整的结果可以这样组织：说明细胞类型与材料处理方式，给出接触和显色时间，描述匹配空白与参照，最后报告相对代谢响应及独立实验次数。若同时做了细胞计数或活死染色，就把这些结果用于解释显色变化的来源。例如，在细胞计数基本一致的条件下观察到代谢响应改变，研究重点便会转向单细胞状态与检测体系；若细胞数也发生变化，则继续分析增殖、脱落或死亡等不同过程。

对生物材料而言，样品参与检测的方式与细胞本身同样值得认真设计。直接接触可能同时改变细胞黏附和光学路径，浸提液可能带入可溶性组分，颗粒可能随混匀与沉降改变读数。把这些条件记录在实验设计和数据表中，就能在结果异常时定位下一步：补一个浓度匹配空白、做一次信号回收比较，或增加一种直接观察细胞的测量。每一步补充都围绕一个明确问题，而不是不断增加没有解释用途的对照名称。

读懂CCK-8和MTT，意味着能沿着细胞状态、电子转移、显色产物、光学读数和归一化计算这条路径来回追踪。颜色提供了便于比较的入口，严谨的空白和重复设计让比较站得住，互补实验则帮助把信号变化解释成更具体的生物学过程。接下来学习活死染色时，我们会从每孔汇总信号走向单个细胞图像，看见另一种观察细胞状态的尺度。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Mosmann (1983): Rapid colorimetric assay for cellular growth and survival](https://pubmed.ncbi.nlm.nih.gov/6606682/)

   MTT微孔板比色方法的历史论文与摘要。
2. [Assay Guidance Manual: Cell Viability Assays](https://www.ncbi.nlm.nih.gov/sites/books/NBK144065/?report=classic)

   四唑盐显色、代谢读出、干扰与实验设计。
3. [Dojindo: Cell Counting Kit-8 product manual](https://www.dojindo.com/manual/CK04/)

   WST-8、电子介体、读数波长与条件优化。
4. [Dojindo: Measuring Cell Viability / Cytotoxicity](https://www.dojindo.com/products/pdf/Protocol/Cell_Counting_Kit-8.pdf)

   材料颜色、无细胞背景与检测干扰的具体处理思路。
5. [GraphPad: Relative versus absolute IC50](https://www.graphpad.com/guides/prism/latest/curve-fitting/reg_50_of_what__relative_vs_absolu.htm)

   拟合动态范围中点与参照50%响应的区别。
6. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   有边界的非线性拟合参数与残差定义。
7. [Cell Viability Assays for 3D Cellular Constructs](https://pubmed.ncbi.nlm.nih.gov/37142936/)

   三维细胞体系中活性测量的进一步阅读入口。
8. [Huyck et al. (2012): XTT measurements in three-dimensional matrices](https://pmc.ncbi.nlm.nih.gov/articles/PMC3419859/)

   三维基质中验证工作区间与细胞可达性的实验案例；该论文使用XTT。
