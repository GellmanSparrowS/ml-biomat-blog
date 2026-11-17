# 流式细胞术：逐个细胞读出多维信息

Source: https://ml-biomat.com/tutorials/experimental-methods/l09/
Language: zh-CN

从光脉冲、串色和门控出发，把群体分布、比例与绝对数量连接起来。

## 平均值相同，两瓶细胞可以很不一样

把一种荧光标记的材料加入培养细胞后，整孔读数增加了一倍，这件事可以有几种完全不同的解释：每个细胞都稍微变亮，少数细胞变得特别亮，或者一部分细胞死亡后更容易黏附荧光物质。想象统计一个班的身高，只知道平均数，仍然看不见个体之间的差异。流式细胞术把悬浮液中的对象依次送过检测区，为每次通过记录一组信号，因此能够把“这瓶样品有多亮”继续拆成“哪些事件亮、亮到什么程度、同时带有什么特征”。这正是它在免疫细胞分类、材料与细胞相互作用、蛋白表达和细胞状态研究中的用途。

这里先使用“事件”这个词，因为仪器检测到一次脉冲，并不自动意味着检测到一个完整活细胞。碎片、两颗贴在一起的细胞、计数微球，以及材料颗粒本身，都可能触发记录。检测器没有提前知道对象的身份；它提供的是散射、荧光和时间等数字，研究者需要结合样品、染色和控制实验逐步确定分析对象。经过这一过程后，才能把某一组事件解释为活单细胞，进一步讨论它们的表型。表型指在当前测量中能够观察到的特征组合，例如同时表达两个蛋白，或某种探针信号升高。

可以把一份流式文件看成一张很长的表。每一行是一件被记录的事件，每一列是一个通道：可能是向前散射的积分信号，也可能是某个波段的荧光。两列作散点图时，一行就成为一个点；改变横纵轴，仍然是在从不同角度观察同一批行。图上的点颜色往往用来表示密度或选中的群体，并不等于细胞本身发出的颜色。理解这个表格结构以后，门控也就不神秘了：在图上圈出区域，相当于给符合条件的行加一个可追溯的选择标记。

本章用两个普通标记X和Y建立一个透明的例子。它们可以代表研究中的两种待测分子，但这里不替它们指定某种真实细胞身份。完整程序构造12000个事件，让读者知道每一步加入了什么信号、噪声和异常，再把事件写成标准FCS文件并重新读取。另有一幅来自真实研究的多通道分布图，用来观察实验数据的重叠和复杂性。两类图承担不同任务：构造模型便于核对计算，真实分布帮助我们理解同一类细胞内部仍然存在的差异。

## 一颗细胞经过光束，留下怎样的脉冲

悬浮液进入仪器后，液流聚焦让对象尽量沿着可重复的路径通过光束。流体像一条逐渐收窄的通道，帮助队伍经过同一个观察位置；这幅图景强调路径控制，并不保证对象之间绝不会相遇。样品太浓、细胞黏连或流动不稳定，都可能使一次检测窗口里出现多个对象。检测到的光经过光学元件分配到不同探测器，随后转成随时间变化的电信号。对于一个事件，信号先升高再降低，形成脉冲，仪器把它的面积、高度和宽度等特征保存下来。

前向散射FSC收集接近入射方向的散射光，侧向散射SSC收集另一方向的散射光。在同类细胞和固定光学条件下，它们常能帮助区分尺寸与内部结构不同的群体，但散射还受到折射率、形状和检测角度影响。于是FSC并不是一把已经标成微米的尺，SSC也不是直接数出细胞内有多少颗粒。研究材料摄取时尤其要留意：颗粒附着、折射率改变或细胞收缩，都可能改变散射。把散射图与显微图像、制样过程和荧光标记一起阅读，才能给群体赋予合适的解释。

脉冲的高度是最高点，面积是整个通过过程的信号累积，宽度描述持续时间。两个相邻细胞经过时，可能形成一个更宽的脉冲，面积明显增加，而最高点没有同比增加。因此面积和高度的关系能够帮助识别成对事件。右图让两个高斯形脉冲相邻出现：总面积约为单脉冲的两倍，高度却仍接近单脉冲。这是一个便于理解的几何模型，真实仪器的宽度定义、电子增益和记录单位各有约定，门的位置应从相应样品的脉冲分布确定，而不是照搬某条固定斜线。

$$
A=\int s(t)\,dt,\qquad H=\max_t s(t),\qquad W_{\mathrm{eq}}=A/H
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | 扣基线的脉冲信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过光束的时间，本图用μs。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 脉冲积分面积，此模拟中为a.u.·μs。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 脉冲最大高度，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/19536a0d407aa5450fc4a393.svg) | 面积除以高度定义的等效宽度，μs；H须大于0。 |

面积累积整个通过过程，高度只取最高点。峰高1a.u.、时间标准差2μs的高斯脉冲，积分约5.0133a.u.·μs，等效宽度约5.0133μs；两个相邻同形脉冲的总面积约10.0265。仪器报告的W未必采用A/H定义，且A、H可能有各自电子缩放；主例的FSC-A/H门使用已归一化的构造坐标。

![从检测到分选的原创原理图与脉冲几何。右图为构造信号，面积以a.u.·μs计；宽脉冲的面积增加，不要求高度同倍增加。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8254fe2016afe0e8b78ec845.svg?v=8254fe2016af)

图 1从检测到分选的原创原理图与脉冲几何。右图为构造信号，面积以a.u.·μs计；宽脉冲的面积增加，不要求高度同倍增加。

这一测量思路有一段很有启发性的历史。20世纪60年代，逐颗检测与液滴偏转技术结合，使研究者可以按照测得的性质把对象真正分开；随后，荧光标记又把分选依据连接到细胞分子。Herzenberg团队的历史回顾描述了荧光检测、液滴形成和带电偏转之间的配合。这里画的是原理示意，关键是“先识别，再在正确时刻分开”这条因果链。今天，分析型流式仪主要形成数据表，分选型仪器还能够回收特定群体。图上画了门，表示已在数据中选择事件；实际获得一管被选细胞，则还需要分选装置及相应的回收验证。

## 两种颜色进入同一个通道，怎样把贡献分开

给抗体连接荧光分子，可以让它结合的对象在适当激发下发光。一个荧光分子的发射通常覆盖一段波长，而检测通道也接收一段波长，两者不会天然一一对应。假设X主要被第一通道检测，但其中一部分光也进入第二通道，那么一个只带X的细胞，也可能在Y的图上变亮。它像两个麦克风都收到了同一位说话人的声音：第二路有声音，并不足以说明第二个人开口。补偿要解决的是各路信号中线性混合的贡献，而不是根据我们希望得到的细胞比例去调整图形。

用单染控制可以测量这种混合。只加入X染料，比较阳性和相匹配阴性群体在两个探测器中的变化，次通道变化除以主通道变化，就得到一个串色系数。阳性和阴性应具有相近的自发荧光背景，使用的荧光分子、串联染料状态和仪器设置也要与正式实验对应。太暗的阳性群体使斜率难以准确估计，饱和的信号则破坏线性关系。图C保留散点，让斜率的来源清楚可见；单染控制的作用是确定信号怎样混合，它与决定正式样品阳性边界的任务不同。

本例把两个方向的串色同时保留下来：X信号的25%进入第二通道，Y信号的5%进入第一通道。先处理已知的固定电子基线，再解两个联立方程。例如真实贡献为X=1000、Y=200时，观测到的扣基线信号为1010和450。第二通道的450包含了X贡献的250，不能全部归给Y；同时第一通道也含有Y贡献的10，所以简单地各减一次而不考虑相互关系，会留下误差。矩阵只是把这组联立方程整齐地写在一起，程序使用线性方程求解器恢复两个贡献。

$$
\begin{bmatrix}y_1\\y_2\end{bmatrix}=\begin{bmatrix}1&b\\a&1\end{bmatrix}\begin{bmatrix}x_X\\x_Y\end{bmatrix},\qquad x_X=\frac{y_1-by_2}{1-ab},\quad x_Y=\frac{y_2-ay_1}{1-ab}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/759961a30d68d6c3c8e3b71a.svg) | 两个探测器扣除已知固定基线后的线性信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/710ad7c128e0717b76d57b53.svg) | 待估计的X和Y主通道贡献，a.u.；各来源以自身主通道为单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | X进入第二通道的串色系数，通道单位统一后为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Y进入第一通道的串色系数，同样为无量纲。 |

采用线性、未饱和响应，串色矩阵的行是探测器、列是来源，且1−ab不为0。a=0.25、b=0.05，真实(1000,200)产生(1010,450)，联立求解恢复(1000,200)。实际含噪数据恢复的是估计值，不会消除噪声。基线处理使用控制和仪器定义，并非把每种细胞的自发荧光都视为同一个常数。

扣基线和补偿后，一些弱信号会变成负数。荧光分子当然没有发出负的光，负值反映的是相对于背景的估计以及测量波动。把这些值全部改成零，会把分布挤在边界上，也会改变均值、分位数和门附近的事件数。补偿能校正平均串色关系，却不会使光子统计和探测噪声消失；一个很亮的标记还可能使其他通道的阴性分布变宽。图D保留这个宽度与零以下的事件，帮助我们把“中心位置校正正确”与“阴阳群体是否容易分开”区分开来。

![构造事件的原始混合、补偿后分布、单染斜率与阴性噪声。A、B均用同一asinh尺度；虚线标出200a.u.的阈值。D是按各直方图积分为1归一的密度，保留负值；所有数值均来自完整示例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a28286835d3e9b6c65e3bdf4.svg?v=a28286835d3e)

图 2构造事件的原始混合、补偿后分布、单染斜率与阴性噪声。A、B均用同一asinh尺度；虚线标出200a.u.的阈值。D是按各直方图积分为1归一的密度，保留负值；所有数值均来自完整示例。

普通对数不能显示零和负数，因此流式分析常使用零附近较平缓、较大信号处类似对数的坐标变换。本例采用asinh变换，参数c决定零附近多宽的一段被展开。改变c像换一张地图的刻度，不会使同一个细胞真的多出蛋白。如果阳性阈值原来为200，显示时也要把200按同一规则变换，才能保持门选中的事件不变。线性补偿应在这种非线性显示之前完成，因为先把各个数弯曲再相减，与先分开贡献再换刻度，一般得不到相同结果。

$$
u=\operatorname{asinh}(x/c),\qquad u_g=\operatorname{asinh}(x_g/c)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 补偿后的信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 正的显示尺度参数，与x同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4620fefc72ebf96810ce9f34.svg) | 变换坐标，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dfae5713ceb32386a507bad7.svg) | 信号原尺度上的门阈值，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c20f9bf1d88cc73e738ac44.svg) | 同一门在显示坐标上的位置，无量纲。 |

asinh在零附近保留正负两侧，在大数值处压缩范围；它是单调变换，点与门同时变化时成员不变。xg=200、c=50得到ug≈2.09471；c=100则ug≈1.44364。补偿应先在线性尺度完成。本例先变换再补偿会得到Y坐标约1.99350，而正确顺序为2.09471。

## 沿着一条有分母的路线，找到目标群体

分析可以先看时间轴。若某一段时间里散射整体突然下降，可能与气泡、流动变化或样品供应状态有关，后续所有荧光分群都值得结合这一变化检查。程序在45至48秒之间构造了一个明确的信号异常，用它展示时间质量控制：保留异常前后稳定区间，再继续分析。真实实验中，时间门应依据采集记录和信号形态确定；一个随刺激逐渐变化的生物过程，也可能在时间轴上留下趋势。保留原始时间列，能帮助区分采集问题与研究对象本来就随时间改变的情况。

接着在FSC和SSC上选择候选细胞事件，减少明显碎片的影响，再在脉冲面积与高度之间选择单事件区域。本例为了让计算透明，使用矩形散射门和面积/高度的窄带；两列已按构造模型归一到可比较的尺度。对于实际样品，激活后的细胞可能变大，组织消化后的群体可能很分散，过紧的散射门会把研究中真正改变的细胞提前排除。可以把最后找到的目标事件重新投回上游散射图，这种回看能够检查它们是否聚集在门边缘，或某一亚群是否已经被最初的选择丢失。

脉冲单细胞门也需要与样品形态配合。细胞成对时的排列方向不同，某一种FSC宽度或面积关系未必能够识别所有组合；必要时可结合SSC脉冲、其他单细胞证据及显微检查。随后使用死亡染料选择符合研究目的的活细胞。完整膜通常排斥某些核酸染料，而膜受损事件更容易染亮；若后续要固定和透化，应在适当步骤使用可固定的活死染料，保存固定前的膜状态信息。死亡染料阴性描述的是所选指标下的状态，不等同于已经证明所有细胞功能均正常。

![同一12000事件的门控路径。A标出构造的不稳定区段；B至E依次使用前一父群；F显示全量计数。散点为可读性抽取显示，数量由完整数组计算，脉冲坐标采用本例的归一化尺度。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/686b55be423f4e4bda3196fe.svg?v=686b55be423f)

图 3同一12000事件的门控路径。A标出构造的不稳定区段；B至E依次使用前一父群；F显示全量计数。散点为可读性抽取显示，数量由完整数组计算，脉冲坐标采用本例的归一化尺度。

每一步选择都有一个父群体，也就是这一关之前允许进入的事件。假设10000个总事件中，得到6000个活单细胞，其中3000个X阳性，而X与Y双阳性为900个。900除以3000得到30%，回答X阳性群体中有多少同时Y阳性；900除以6000得到15%，回答活单细胞中有多少双阳性；900除以10000得到9%，则以全部采集事件为分母。三个数字可以同时正确，它们讨论的是不同群体。绘图和导出结果时，同时保留数量、父群体和百分比，读者便能沿着选择路径复原结论。

$$
p_{G\mid P}=N_G/N_P,\qquad p_{G\mid A}=\prod_{j=1}^{m}\frac{N_j}{N_{j-1}}=N_G/N_A
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5d37ecc8a3cfa64f17cb687e.svg) | 子群、其指定父群，以及全部事件。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ca1407bb5d26b15142bac1d.svg) | 相应群体的事件数，计数；分母须非零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e030e3c0b33e809fab494344.svg) | 相对于父群或全部事件的比例，无量纲；乘100成为%。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5a4fe308f7124fa593b4bb53.svg) | 嵌套门的层级编号与总层数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5595bec7d02a56853e57f907.svg) | 第j级及前一级保留的事件数；N0=NA，Nm=NG。 |

每个子群包含于父群时，逐级比例相乘，中间计数会约去。10000全部→6000活单细胞→3000X阳性→900双阳性，得到0.6×0.5×0.3=0.09。900/3000=30%与900/6000=15%使用不同父群。重叠而非嵌套的门不能套用同一乘积链。

完整模拟中的数量会与这个简单算例不同，因为散射、染色和噪声都有连续分布。它从12000个事件出发，留下11700个稳定事件、10530个候选细胞、9754个单事件和8792个活事件，最后得到866个双阳性事件。双阳性占活事件约9.85%，占全部事件约7.22%。程序输出每一步的布尔选择，表示每一行是否通过该门；后续检查可以直接回到具体事件，而不必只依赖屏幕上一个已经四舍五入的百分数。

## 阳性边界怎样获得实验依据

一个群体是否阳性，通常需要围绕研究问题建立控制。未染色样品帮助观察样品本身的自发荧光以及仪器背景；单染样品帮助确定串色；荧光减一控制，也叫FMO，则包含正式面板中的其他染色，唯独省去正在判断的那个标记。这样，缺少Y染色的样品仍然保留X等其他染料带来的分布展宽，更接近正式面板里Y阴性事件所处的测量环境。把FMO与完整染色并排，可以判断门附近的信号是否超出了其他标记共同形成的背景分布。

FMO没有加入待测抗体，因此它也不会告诉我们这支抗体会不会非特异地黏在细胞上。验证抗体识别对象，需要合适的生物阴性、阳性或阻断等控制。例如比较已知不表达目标的细胞与表达目标的细胞，可以检验信号是否随目标出现；研究材料处理时，还应检查材料是否自身发光、是否吸附抗体、是否改变细胞自发荧光。控制各自回答不同问题，组合起来才形成可信的判别依据。把一种控制当作所有误差的总开关，容易错过恰好与处理条件相关的变化。

阳性并不总对应两座分得很开的山峰。有些分子连续表达，分布从低到高平缓延伸，划一条线就会把连续变化转成两个类别。此时可同时报告完整分布、中位荧光以及预先定义阈值下的比例，让读者看到结论是否依赖边界的一点移动。抗体用量也值得滴定：增加用量可能提高特异信号，也可能抬高背景，最佳条件取决于分离程度和研究目标。检测增益、染料组合、固定条件与批次保持可比较，才适合把不同样品的亮度放到同一张图上讨论。

下面的交互让同一批240个构造事件在不同补偿和显示条件下出现。X到Y的真实串色为25%，Y到X为5%；正确补偿时，Y阳性占50%，双阳性占25%。点击跳过X到Y补偿，会让部分X单阳性事件被读成Y阳性。再改变显示尺度，散点位置和门线一起移动，而事件比例应保持不变。最后提高Y阈值，观察究竟是哪一群事件穿过了边界。这个练习把三件常被混在一起的事情拆开：信号混合的校正、坐标的显示方式和分析者选择的阈值。

## 交互实验：串色、门阈值与显示尺度

240个构造事件保持不变。先调整X到Y补偿，再改变Y阈值；最后只调显示尺度，检验比例是否保持。X阳性阈值固定为400a.u.，两个百分比均以240事件为分母。方向键可调整滑块，图形可横向滚动。

[Figure: diagram](https://ml-biomat.com/tutorials/experimental-methods/l09/#L09-lab)

## 比例之外，还要知道采到了多少

如果两份样品的目标群体都占10%，它们仍可能含有很不一样的目标细胞总数。一份样品有十万个活细胞，另一份只有一万个，百分比相同并不抵消数量差别。研究材料毒性时尤其需要把存活总量与幸存者中的表型比例一起读：某个亚群比例升高，可能来自该群增加，也可能来自其他群减少。流式文件中的总事件数通常由采集时间、停止条件和样品浓度共同决定，因此“采到了两万行”本身没有提供原样的体积尺度。

计数珠为数量引入一个已知参照。向确定体积的原样加入已知数量的微球，充分混匀后，在同一次采集中分别识别目标细胞和微球。若二者以相同采集份额进入仪器，细胞事件数与珠事件数的比值，就等于整管中两者数量的比值；未知采集份额因此消去。将这个比例乘上加入的珠总数，再除以所取原样体积，就得到原样的目标浓度。额外加入的染色缓冲液会同时稀释珠和细胞，使用这个比值时不必把它误当成原样体积。

$$
C_{\mathrm{cell}}=\frac{n_{\mathrm{cell}}}{n_b}\frac{C_bV_b}{V_s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cc5689fe165be4f85d6d561b.svg) | 所取原样中目标细胞浓度，cells/μL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/914da3c1b6e03f18548e56ec.svg) | 同一采集区间内目标细胞和珠的事件数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a2c7455873446449e6636a4.svg) | 加入前计数珠悬液浓度，beads/μL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4c2fa541a1b8466dacbc3550.svg) | 加入珠悬液的体积，μL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 参与混合的原样体积，μL。 |

细胞和珠均匀混合且具有一致有效采集份额时，事件数比消去未知采集体积。6000个细胞事件、1000个珠事件，Cb=1000beads/μL、Vb=20μL、Vs=100μL，得到1200cells/μL。所有量对应珠加入时的样品；预先稀释的原始材料还需相应稀释因子，先前制样损失另由回收测量确定。

例如加入20μL、每μL含1000颗珠的悬液，珠总数为20000；原样取100μL，采到6000个目标事件和1000个珠事件，计算得到1200个目标细胞/μL。若采集时间加倍且两类事件都加倍，浓度仍相同。这个消去关系需要珠和细胞均匀悬浮、正确识别，且加入参照后没有发生不同程度的损失。把珠漏在触发阈值以下，会使珠计数偏低、推算细胞浓度偏高；混合后再洗涤，则可能改变两者比例。计数得到的是参照加入时对应样品中的浓度，先前消化或转移丢失的细胞需要通过另外的回收记录追踪。

另一条获得绝对浓度的路径，是使用经过校准的体积采集系统，将目标事件数除以实际分析体积，并处理稀释及损失关系。无论采用哪条路径，都应把目标门的定义与体积定义保留下来。计数珠本身并不属于活单细胞门，要建立独立珠门，在一致的采集区间比较两类事件。若研究只要求群体比例，珠不是每个实验都必加的项目；若结论涉及每毫升有多少目标细胞，体积或已知参照就是计算链中需要补上的信息。

![三个独立算例：同一900事件采用不同分母、稀有群体的泊松计数近似，以及固定珠/细胞比例下采集量改变而浓度保持1200cells/μL。它们讲解数量定义，不是新的生物实验。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bb2360d9b6718e391dcd9bfb.svg?v=bb2360d9b671)

图 4三个独立算例：同一900事件采用不同分母、稀有群体的泊松计数近似，以及固定珠/细胞比例下采集量改变而浓度保持1200cells/μL。它们讲解数量定义，不是新的生物实验。

多采集事件还能减少抽样起伏。在独立抽样且分类正确的简单模型中，比例的标准误差同时取决于比例和父群体数量。1000个父群体事件中有25%阳性，标准误差约为1.37个百分点；这并不是不同培养批次之间的误差条。对于稀有群体，目标事件数尤其关键：平均采到25个目标时，泊松计数近似给出约20%的相对波动，采到100个时约10%。若目标比例稳定，要把预期目标数从25提高到100，总采集量约需增加到四倍，才能把这一相对波动减半。采集计划因而应围绕目标群体的预期数量安排；向已有很多事件的大群体再增加一些记录，对稀有群体的精度未必有明显帮助。因此增加总采集量可以改善稀有群体的计数精度，而补偿、门控和制样偏差仍须由相应控制来处理。

$$
\operatorname{SE}(\hat p)\simeq\sqrt{\frac{\hat p(1-\hat p)}{N}},\qquad\operatorname{CV}_{\mathrm{rare}}\simeq\frac{1}{\sqrt{k}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8e2a7a0b6724724df048ccba.svg) | 观察到的阳性比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 对应父群体的事件数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e7a5ba0e6907d996a32a35b0.svg) | 独立二项抽样近似的比例标准误差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 稀有群体的目标事件数，采用泊松计数近似。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1e15735a378a68af881e41dc.svg) | 稀有计数的近似相对标准差，无量纲。 |

此处把分类规则固定，讨论抽样起伏，不包括独立制样差异。p=0.25、N=1000得到SE≈0.01369，即1.37个百分点。稀有目标k=25时CV≈20%，k=100时≈10%。零或极少事件时不能套用这个相对误差表达式，比例接近0或1时需采用适合稀少计数的区间估计。

## 从真实分布中，看见群体内部的变化

真实实验很少像四个整齐点团那样简单。下面的公开研究图把CD4阳性与CD8阳性T细胞在多个通道上的分布排列起来：每一行是一种信号，同一行中的红蓝曲线代表两群已被识别的细胞。沿着一行比较，可以看到哪些标记的分布明显分开，哪些仍大量重叠。横轴已经经过显示变换，0.6不是“60%的细胞”，也不是可以直接跨不同抗体比较的蛋白分子数；曲线高度主要帮助观察分布形状，不能拿两个峰顶的高度直接推断两群细胞总数的比例。

![White等（2021）图2，CC BY 4.0，完整转载并在图外增加标题。红色CD4阳性、蓝色CD8阳性T细胞；每行比较一个参数。横轴为变换坐标，峰高不能直接当作群体数量。数据来自原论文所述EQAPOL研究。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ce2422d48d86af11cd3f4192.svg?v=ce2422d48d86)

图 5White等（2021）图2，CC BY 4.0，完整转载并在图外增加标题。红色CD4阳性、蓝色CD8阳性T细胞；每行比较一个参数。横轴为变换坐标，峰高不能直接当作群体数量。数据来自原论文所述EQAPOL研究。

这种排列适合提出更具体的问题。如果两个群体在某个功能标记上的主峰位置接近，但其中一群多出高信号尾部，整群中位数可能变化很小，而尾部比例已经发生变化。相反，所有细胞都轻微右移时，固定阈值下的阳性比例可能变化不明显，中位数却能显示整体移动。选择何种汇总，取决于希望描述的是群体组成、整群表达位置，还是少数强响应者。先看分布，再选与研究问题对应的数字，比把所有通道都压成同一种柱状图更容易保留生物意义。

还要区分荧光信号与目标数量之间的距离。抗体结合位点、染色饱和程度、荧光分子亮度、检测效率及细胞自发荧光，都可能影响读数。同一种标记在可比较条件下的变化可以很有价值；若要进一步解释为每细胞多少分子，则需要合适的定量校准与结合模型。对荧光材料而言，表面吸附与内部摄取都可能让细胞相关信号增强，可以通过成像、合适的表面淬灭或去除处理来区分位置。流式给出高通量的个体分布，空间位置的信息则由与其互补的实验继续补充。

实验重复的单位也应回到实际设计。一个样品里测得一万个细胞，并不等于做了一万次独立培养；它们共享培养环境、材料处理和制样步骤。比较处理组时，通常先为每个独立样品保留一个或一组预定指标，再在样品层面比较，同时展示代表性分布与门控。这样，事件层面的丰富信息用于刻画样品内部差异，独立制样之间的变化用于回答处理效果是否稳定，两种层级各自发挥作用。

## 让每个结果都能回到事件表

完整程序先构造散射、脉冲和荧光事件，加入已知串色、固定基线及噪声，再用FlowIO写入FCS并读取。FCS既包含事件数组，也包含通道名称、记录方式和时间尺度等元数据；正式文件中的增益与存储尺度需要按其定义处理，不能把所有二进制数一概当成已经适合分析的线性荧光。这里生成的是明确指定的线性浮点数据，并检查读回后事件数、通道顺序和数值一致性。FlowKit文档把未补偿、补偿后和显示变换后的数据区分为不同状态，这种区分同样贯穿本例。

程序中的混合矩阵约定“行是探测器、列是荧光来源”，并把约定连同系数写成独立表。其他软件导出的矩阵可能采用转置排列，因此接入实验文件时，先用已知单染事件核对方向比直接复制一张数字表更可靠。读取FCS不会自动判断某份信号是否已经补偿；需要查看采集设置、元数据和分析记录，避免把同一个校正应用两次。显示参数、门坐标所在的尺度及父子关系也要一起保存，否则相同门坐标放到另一种变换下，就可能选中不同事件。

### 从FCS事件到补偿、门控和数量结果

完整离线示例，固定随机种子909。生成并读回12000×8的FCS，再由读回值执行补偿和门控；输出逐事件CSV、控制、门数量、NPZ和图。FlowIO 1.4.0作为带BSD许可的原版小型依赖随包附带，外部依赖为NumPy、Matplotlib及Pillow。

```
"""Flow cytometry: constructed events, FCS round trip, compensation and gates.

The event cloud is simulated. The separately reproduced Figure 2 from White
et al. (2021) contains published experimental distributions; see NOTICE.txt.
Run offline: python main.py --output results --language en
"""
from pathlib import Path
import argparse, csv, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from PIL import Image

# Unmodified BSD-3-Clause FlowIO is bundled for portable FCS reading/writing.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'data' / 'vendor'))
import flowio

BLUE='#186e83'; AMBER='#cd803f'; PURPLE='#8160a1'; GREEN='#3c8a6a'
MATRIX=np.array([[1., .05], [.25, 1.]])  # rows: detectors; columns: fluorophores
BACKGROUND=np.array([80., 100.])

def compensate(measured, matrix=MATRIX, background=BACKGROUND):
    """Solve the linear signal mixture before applying a display transform."""
    return np.linalg.solve(matrix, (np.asarray(measured)-background).T).T

def gate_events(events, corrected):
    time,area,height,width,side,dead=events[:,:6].T
    stable=(time<45)|(time>=48)
    cells=stable&(area>50)&(area<300)&(side>20)&(side<140)
    singlets=cells&(area/height>.85)&(area/height<1.15)
    live=singlets&(dead<200)
    positive=live&(corrected[:,0]>200)&(corrected[:,1]>200)
    return dict(all=np.ones(len(events),dtype=bool),stable=stable,cells=cells,singlets=singlets,live=live,double_positive=positive)

def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):
        fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    def table(name,header,rows):
        with(out/name).open('w',newline='',encoding='utf8')as f:
            writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)
    rng=np.random.default_rng(909);N=12000
    kinds=np.repeat(['debris','doublet','dead','live'],[1200,800,1000,9000]);rng.shuffle(kinds)
    time=np.arange(N)/100.;height=rng.lognormal(np.log(100),.17,N);side=rng.normal(60,13,N)
    height[kinds=='debris']=rng.uniform(15,35,(kinds=='debris').sum());side[kinds=='debris']=rng.uniform(5,18,(kinds=='debris').sum())
    width=rng.normal(1,.035,N);width[kinds=='doublet']=rng.normal(1.8,.06,(kinds=='doublet').sum())
    area=height*width;artifact=(time>=45)&(time<48);area[artifact]*=.45
    viability=rng.normal(50,15,N);viability[kinds=='dead']=rng.lognormal(np.log(900),.25,(kinds=='dead').sum())
    phenotype=rng.choice(4,N,p=[.35,.35,.20,.10]);truth=rng.exponential(12,(N,2))+15
    for channel,groups in [(0,[1,3]),(1,[2,3])]:
        mask=np.isin(phenotype,groups);truth[mask,channel]=rng.lognormal(np.log(800),.3,mask.sum())
    truth[kinds=='debris']*=.1;truth[kinds=='dead']+=500
    ideal=truth@MATRIX.T;measured=ideal+BACKGROUND+rng.normal(size=(N,2))*(18+.5*np.sqrt(ideal))
    original=np.column_stack([time,area,height,width,side,viability,measured])
    labels=['Time','FSC-A','FSC-H','FSC-W','SSC-A','Viability-A','FL1-A','FL2-A']
    with(out/'constructed-events.fcs').open('wb')as handle:
        flowio.create_fcs(handle,original.ravel().tolist(),labels,metadata_dict={'timestep':'1','comment':'Constructed teaching events; linear signals; external compensation matrix'})
    fcs=flowio.FlowData(out/'constructed-events.fcs');events=fcs.as_array(preprocess=True)
    assert fcs.event_count==N and fcs.channel_count==8 and fcs.pnn_labels==labels
    assert np.allclose(events,original,rtol=1e-6,atol=1e-5)
    corrected=compensate(events[:,6:8]);gates=gate_events(events,corrected);live=gates['live']
    table('events.csv',labels+['X_compensated','Y_compensated','simulated_kind','selected_double_positive'],[list(row)+list(c)+[kind,int(gates['double_positive'][i])]for i,(row,c,kind)in enumerate(zip(events,corrected,kinds))])
    table('gate_counts.csv',['gate','parent','events','percent_parent','percent_all'],[[name,'none'if j==0 else list(gates)[j-1],int(mask.sum()),100*mask.sum()/(N if j==0 else list(gates.values())[j-1].sum()),100*mask.mean()]for j,(name,mask)in enumerate(gates.items())])
    table('mixing_matrix.csv',['detector','X_coefficient','Y_coefficient'],[['FL1-A',1,.05],['FL2-A',.25,1]])
    np.savez_compressed(out/'flow_data.npz',events=events,corrected=corrected,truth=truth,kind=kinds,**{f'gate_{k}':v for k,v in gates.items()})
    # Independent single-stain controls estimate spillover on a linear scale.
    negative=BACKGROUND+rng.normal(0,12,(1000,2));controls=[];estimates=[]
    for ch in [0,1]:
        x=np.zeros((1000,2));x[:,ch]=rng.lognormal(np.log(1800),.28,1000)
        y=x@MATRIX.T+BACKGROUND+rng.normal(0,15,(1000,2));controls.append(y)
        delta=np.median(y,axis=0)-np.median(negative,axis=0);estimates.append(delta[1-ch]/delta[ch])
    table('single_stain_controls.csv',['control','FL1_A','FL2_A'],[[name,*row]for name,data in zip(['unstained','X_only','Y_only'],[negative,*controls])for row in data])
    # Same X-positive control gives the Y-FMO spreading example, after compensation.
    fmo=compensate(controls[0]);unstained=compensate(negative)
    cofactor=50.;transform=lambda x:np.arcsinh(x/cofactor)
    t=np.linspace(-15,15,1201);pulse=np.exp(-t*t/(2*2**2));double=np.exp(-(t-3)**2/8)+np.exp(-(t+3)**2/8)
    fig,axs=plt.subplots(1,2,figsize=(12,5.6));ax=axs[0];ax.set(xlim=(0,10),ylim=(0,9));ax.axis('off')
    ax.add_patch(Polygon([[3,8],[7,8],[5.7,5],[5.7,3],[4.3,3],[4.3,5]],closed=True,fc=BLUE,alpha=.12))
    ax.plot([5,5],[8,3],color=BLUE,lw=1)
    for y in [7.5,6.5,5.5,4.5,3.5]:ax.add_patch(Circle((5,y),.18,fc=BLUE))
    ax.annotate('',xy=(6.4,4.5),xytext=(1,4.5),arrowprops={'arrowstyle':'->','color':AMBER,'lw':2})
    ax.text(.8,5,T('激光','Laser'),color=AMBER);ax.text(7,4.5,T('散射与荧光\n成为同一行记录','Scatter and fluorescence\nbecome one event row'),fontsize=10,va='center')
    for x,y in [(5,2.6),(4.5,1.8),(4,1),(5.5,1.8),(6,1)]:ax.add_patch(Circle((x,y),.16,fc=PURPLE if x<5 else GREEN))
    ax.text(.3,8.7,T('1960年代：从逐个检测到按信号分选','1960s: from individual detection to signal-based sorting'),fontsize=11)
    ax.text(.3,.1,T('原创原理图；分选需另有液滴识别与偏转。','Original principle; sorting adds timed droplet deflection.'),fontsize=9)
    ax=axs[1];ax.plot(t,pulse,color=BLUE,label=T('一个高斯脉冲','One Gaussian pulse'));ax.plot(t,double,color=AMBER,label=T('相邻两脉冲','Two adjacent pulses'));ax.fill_between(t,0,pulse,color=BLUE,alpha=.12)
    ax.set(xlabel=T('经过光束的时间 / μs','Transit time / μs'),ylabel=T('扣基线信号 / a.u.','Baseline-corrected signal / a.u.'),title=T('高度接近，积分面积明显不同','Similar height, different integrated area'));ax.legend(frameon=False,fontsize=9);fig.tight_layout();save(fig,'history-pulses')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8.7));sample=np.flatnonzero(live)[::3]
    for ax,data,title in [(axs[0,0],events[:,6:8]-BACKGROUND,T('A  扣基线后仍混有串色','A  Baseline subtraction leaves spillover')),(axs[0,1],corrected,T('B  线性补偿后，再用asinh显示','B  Linear compensation, then asinh display'))]:
        v=transform(data[sample]);ax.scatter(v[:,0],v[:,1],s=3,alpha=.22,color=BLUE,rasterized=True);ax.axvline(transform(200),color=AMBER,ls='--');ax.axhline(transform(200),color=AMBER,ls='--');ax.set(xlim=(-2,5),ylim=(-2,5),xlabel='asinh(detector 1 / 50)' if ax is axs[0,0] else 'asinh(X / 50)',ylabel='asinh(detector 2 / 50)' if ax is axs[0,0] else 'asinh(Y / 50)',title=title)
    ax=axs[1,0];ax.scatter(controls[0][:,0]-80,controls[0][:,1]-100,s=3,alpha=.2,color=AMBER);xx=np.array([0,4500]);ax.plot(xx,.25*xx,color=BLUE);ax.set(xlabel=T('X单染：主通道 / a.u.','X-only: primary detector / a.u.'),ylabel=T('次通道 / a.u.','Secondary detector / a.u.'),title=T('C  单染斜率给出串色比例','C  Single stain estimates spillover'))
    ax=axs[1,1];bins=np.linspace(-70,70,50);ax.hist(unstained[:,1],bins=bins,density=True,histtype='step',lw=2,color=GREEN,label=T('未染色对照','Unstained'));ax.hist(fmo[:,1],bins=bins,density=True,histtype='step',lw=2,color=PURPLE,label=T('X单染，Y缺失','X stained, Y omitted'));ax.axvline(0,color='gray',lw=.7);ax.set(xlabel=T('补偿Y / a.u.','Compensated Y / a.u.'),ylabel=T('概率密度 / (a.u.)⁻¹','Probability density / (a.u.)⁻¹'),title=T('D  负值保留，噪声仍存在','D  Retain negative values and noise'));ax.legend(frameon=False,fontsize=9)
    fig.tight_layout();save(fig,'compensation')
    fig,axs=plt.subplots(2,3,figsize=(13,8.1));idx=np.arange(0,N,4)
    axs[0,0].scatter(events[idx,0],events[idx,1],s=2,color=BLUE,alpha=.2);axs[0,0].axvspan(45,48,color=AMBER,alpha=.2);axs[0,0].set(xlabel=T('采集时间 / s','Acquisition time / s'),ylabel='FSC-A / a.u.',title=T('A  先检查时间稳定性','A  Check stability over time'))
    ids=np.flatnonzero(gates['stable'])[::3];axs[0,1].scatter(events[ids,1],events[ids,4],s=2,color=BLUE,alpha=.2);axs[0,1].add_patch(Rectangle((50,20),250,120,fill=False,ec=AMBER,lw=1.5));axs[0,1].set(xlabel='FSC-A / a.u.',ylabel='SSC-A / a.u.',title=T('B  散射门定义候选事件','B  Scatter gate defines candidates'))
    ids=np.flatnonzero(gates['cells'])[::3];axs[0,2].scatter(events[ids,2],events[ids,1],s=2,color=BLUE,alpha=.2);xx=np.array([40,200]);axs[0,2].plot(xx,.85*xx,color=AMBER);axs[0,2].plot(xx,1.15*xx,color=AMBER);axs[0,2].set(xlabel='FSC-H / a.u.',ylabel='FSC-A / a.u.',title=T('C  单事件脉冲几何','C  Singlet pulse geometry'))
    ids=np.flatnonzero(gates['singlets']);axs[1,0].hist(events[ids,5],bins=np.linspace(0,1600,70),color=BLUE,alpha=.7);axs[1,0].axvline(200,color=AMBER);axs[1,0].set(xlabel=T('死亡染料 / a.u.','Viability-dye signal / a.u.'),ylabel=T('事件数','Events'),title=T('D  选定存活状态','D  Select the live population'))
    axs[1,1].scatter(transform(corrected[sample,0]),transform(corrected[sample,1]),s=2,alpha=.2,color=BLUE);axs[1,1].axvline(transform(200),color=AMBER);axs[1,1].axhline(transform(200),color=AMBER);axs[1,1].set(xlabel='asinh(X / 50)',ylabel='asinh(Y / 50)',title=T('E  活单细胞中读取表型','E  Phenotype within live singlets'))
    names=[T(z,e)for z,e in [('全部','All'),('稳定','Stable'),('候选','Cells'),('单细胞','Singlets'),('活细胞','Live'),('双阳性','X+Y+')]];counts=[int(v.sum())for v in gates.values()];axs[1,2].barh(np.arange(6),counts,color=[BLUE]*5+[AMBER]);axs[1,2].set_yticks(np.arange(6),names);axs[1,2].invert_yaxis();axs[1,2].set(xlabel=T('通过事件数','Passing events'),title=T('F  每一步保留数量与分母','F  Preserve counts and denominators'))
    for i,c in enumerate(counts):axs[1,2].text(c+100,i,str(c),va='center',fontsize=9)
    axs[1,2].set_xlim(0,15000);fig.tight_layout();save(fig,'gating')
    fig,axs=plt.subplots(1,3,figsize=(13,4.7));denoms=[10000,6000,3000];numerator=900
    axs[0].bar(T(['全部事件','活单细胞','X阳性'],['All events','Live singlets','X-positive']),[100*numerator/d for d in denoms],color=[BLUE,GREEN,AMBER]);axs[0].set(ylabel=T('同一900事件所占比例 / %','Fraction of the same 900 events / %'),title=T('A  分母改变，问题改变','A  Denominators change the question'))
    k=np.logspace(0,4,200);axs[1].loglog(k,100/np.sqrt(k),color=PURPLE);axs[1].scatter([25,100,400],[20,10,5],color=AMBER);axs[1].set(xlabel=T('稀有目标事件数 k','Rare-target count k'),ylabel=T('泊松计数近似CV / %','Poisson counting CV / %'),title=T('B  多采集改善抽样精度','B  More events improve sampling precision'))
    beads=np.array([500,1000,2000]);cells=6*beads;concentration=cells/beads*1000*20/100
    axs[2].plot(beads,concentration,'o-',color=GREEN);axs[2].set(xlabel=T('采到的计数珠数','Acquired bead events'),ylabel=T('原样目标浓度 / cells μL⁻¹','Original target concentration / cells μL⁻¹'),ylim=(0,1600),title=T('C  采集份额消去','C  Sampling fraction cancels'));fig.tight_layout();save(fig,'counts')
    fig,ax=plt.subplots(figsize=(13,8.2));ax.imshow(Image.open(Path(__file__).resolve().parent/'flowkit2021-figure2.webp').convert('RGB'));ax.axis('off');ax.set_title(T('真实测量分布：在同一标记内比较两群细胞','Measured distributions: compare two populations within each marker'),fontsize=12);fig.text(.5,.015,T('White等，2021，图2；CC BY 4.0，完整转载。原图横轴是变换坐标。','White et al., 2021, Figure 2; CC BY 4.0, reproduced in full. Original x-axis shows transformed coordinates.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,1]);save(fig,'published')
    exact=compensate(np.array([[1010.,450.]])+BACKGROUND)
    wrong=compensate(transform(np.array([[1010.,450.]])),background=np.zeros(2))
    summary={'fcs':{'events':fcs.event_count,'channels':fcs.channel_count,'maximum_absolute_roundtrip_error':float(abs(events-original).max())},'compensation':{'example_X':float(exact[0,0]),'example_Y':float(exact[0,1]),'estimated_X_to_Y':float(estimates[0]),'estimated_Y_to_X':float(estimates[1]),'negative_Y_live_events':int((corrected[live,1]<0).sum()),'transform_then_compensate_Y':float(wrong[0,1]),'compensate_then_transform_Y':float(transform(exact)[0,1])},'pulse':{'single_area':float(np.trapezoid(pulse,t)),'double_area':float(np.trapezoid(double,t)),'area_ratio':float(np.trapezoid(double,t)/np.trapezoid(pulse,t))},'gates':dict(zip(gates,counts)),'fractions':{'double_positive_percent_live':100*counts[-1]/counts[-2],'double_positive_percent_all':100*counts[-1]/N},'counting':{'conditional_percent':900/3000*100,'all_percent':900/10000*100,'bead_based_cells_per_uL':6000/1000*1000*20/100,'binomial_se_at_p025_N1000':float(np.sqrt(.25*.75/1000)),'rare_cv_at25':1/np.sqrt(25),'rare_cv_at100':1/np.sqrt(100)}}
    assert np.allclose(exact,[[1000,200]])
    assert abs(estimates[0]-.25)<.01 and abs(estimates[1]-.05)<.01
    assert summary['compensation']['negative_Y_live_events']>0
    assert all(a>=b for a,b in zip(counts,counts[1:]))
    assert abs(summary['pulse']['area_ratio']-2)<1e-7
    assert not np.isclose(wrong[0,1],transform(exact)[0,1])
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf8');print(json.dumps(summary,allow_nan=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

输出包括构造FCS、逐事件表、补偿控制表、门控数量表和所有图。逐事件文件保留已补偿X、Y以及最终是否入选，便于从双阳性事件回查其时间、散射和活死信号。图像下采样用于保持散点可读，所有计数则使用完整事件集。这个区别在大文件分析中很实用：屏幕上显示两千个点，不应悄悄把统计分母也改成两千。正式研究可沿用这条记录链，将模拟数据入口替换为具有明确通道和实验控制的样品，再根据样品定义相应门。

从采样到报告，流式结果最清楚的表达通常包含对象、状态和分母。例如“在时间稳定、候选散射、单事件及活细胞条件下，X与Y双阳性占活单细胞的比例”，就比“阳性率升高”多交代了关键的测量含义。若同时提供独立样品的结果、相应分布、控制和绝对计数依据，读者可以判断变化来自群体组成、信号位置还是数量。流式细胞术的价值也在这里：把一瓶混合样品拆成可关联的个体记录，让研究问题逐步落到具体细胞及其共同特征上。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L09.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Herzenberg et al. (2002). The History and Future of the Fluorescence Activated Cell Sorter and Flow Cytometry](https://herzenberglab.stanford.edu/sites/g/files/sbiybj27506/files/media/file/lah490.pdf)

   检测、荧光标记与液滴偏转结合的历史。

   Historical reference; no artwork reproduced.
2. [Cossarizza et al. (2019). Guidelines for the use of flow cytometry and cell sorting in immunological studies, second edition](https://pmc.ncbi.nlm.nih.gov/articles/PMC7350392/)

   单染控制、FMO、活死染色、双事件脉冲几何及分析定义。
3. [FlowKit tutorial 1: Sample class](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part01-sample-class.html)

   FCS元数据、预处理及raw/comp/xform状态的区分。
4. [FlowKit tutorial 2: transforms and Matrix](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part02-transforms-module-matrix-class.html)

   补偿与显示变换、负值及坐标尺度。
5. [FlowKit tutorial 3: GatingStrategy and GatingResults](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part03-gating-strategy-and-gating-results-classes.html)

   层级门与相对父群/全量统计的区别。
6. [FlowIO API and source](https://flowio.readthedocs.io/en/latest/api.html)

   使用FlowIO写入与读取FCS，核对通道与预处理含义。

   FlowIO 1.4.0 source bundled under BSD-3-Clause; full license included.
7. [CountBright Plus Absolute Counting Beads User Guide, MAN0018850 B.0](https://documents.thermofisher.com/TFS-Assets/LSG/manuals/MAN0018850_CountBrightPlus_UG.pdf)

   珠/细胞比例、原样体积、混匀和加珠后损失条件。
8. [White et al. (2021). FlowKit: A Python Toolkit for Integrated Manual and Automated Cytometry Analysis Workflows](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.768541/full)

   真实CD4/CD8多通道分布（图2）及事件与门信息的组织。

   Figure 2: CC BY 4.0, credited and reproduced in full; code license separately BSD-3-Clause.
