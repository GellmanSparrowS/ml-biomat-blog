# 拉曼光谱：散射光里的分子指纹

Source: https://ml-biomat.com/tutorials/experimental-methods/s02/
Language: zh-CN

从一粒透明颗粒出发，理解光如何交换振动能量，再用完整光谱分析分辨峰、背景与仪器效应。

## 一粒看不见成分的颗粒，怎样告诉我们它是什么

在显微镜下，一粒透明塑料碎片、一小块盐晶体和一团干燥蛋白质都可能只是边缘明亮的小东西。它们的形状可以相似，内部的化学键却不同。拉曼光谱把一束颜色很纯的光照到样品上，收集向其他方向散开的微弱光，再寻找其中发生了颜色变化的部分。颜色变化对应光与分子交换的能量；把这些能量变化排列出来，就得到一张与分子振动有关的图谱。研究水凝胶时可以用它比较不同区域的组成，研究骨组织时可以观察矿物与有机组分的谱带，研究聚合物时可以追踪取向、结晶或化学反应带来的变化。同一台显微拉曼仪既能看见一个位置，又能询问那个位置包含怎样的分子结构。

“分子指纹”这个比喻很方便，但要想象的是一整组线索，而不是一个峰对应一个唯一身份。钢琴上相同的音可以出现在许多曲子里，识别歌曲需要一段旋律。类似地，很多有机物都含有碳氢键，相关谱带会出现在相近区域；混合物还会让不同成分的峰重叠。实际判断会同时比较几个峰的位置、形状和相对强度，并检查测量条件。若一根纤维旋转后某个峰变强，变化可能来自分子取向和光的偏振关系；若同一点照射一会儿后背景下降，变化也可能来自荧光漂白。先知道仪器测量的过程，才能把这些现象分开。

本篇围绕一个具体任务展开：在宽阔的背景上分辨两条靠近的拉曼峰，并比较它们的面积。这个任务会遇到初学者最常见的三个问题：横坐标为什么使用 cm⁻¹，而不是激光的颜色；为什么肉眼看起来更高的峰不一定包含更多拉曼信号；为什么增加激光功率有时让结果更清楚，有时却把样品和探测器一起推离了正常工作范围。后面的图、计算和交互都围绕这三个问题。用于数值练习的光谱由明确的峰形、背景和随机计数噪声构造，真值保存在输出文件中，因此可以检查每一步处理究竟改善了什么，又改变了什么。

开始实验前，研究问题还要落实为“测哪里”。一张透明薄膜的表面、厚度方向和夹杂颗粒可能具有不同组成；一块组织的矿化区与周围软组织也会给出不同信号。单点光谱回答所选光斑附近的情况，面扫描把许多点按位置组织起来。把十次重复照射同一位置当作十个独立样品，会混淆仪器重复性与材料本身的差异。合适的设计通常先用几个低功率试测点了解背景和稳定性，再在独立制备的样品中选择有明确规则的位置。这样得到的差别才有机会连接到材料制备或生物状态。

## 从两块滤光片到现代光谱仪：先把稀少的光找出来

1928 年，C. V. Raman 与 K. S. Krishnan 在液体散射研究中辨认出了与入射光颜色不同的散射成分。理解这个发现，不必先从获奖名单开始，可以从一个光学筛选问题开始：如果一束紫光照进液体，收集到的光大部分仍然是紫色，怎样看见混在其中的另一种颜色？早期实验通过滤光选择入射光，再用另一块滤光片抑制原来的颜色。这里的关键不是光变得很亮，而是原本淹没微弱信号的强光被有选择地挡住。下图重新画出这个思想，并把它与现代仪器的功能联系起来；图示说明光路角色，不按历史装置的尺寸复原。

![早期滤光思想与现代仪器功能的原创示意。上图突出从强散射中筛选不同颜色的光；下图说明像素计数如何经过标定成为光谱。光路为功能示意，未复原历史装置尺寸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f23efeb7364d26a4414fc51a.svg?v=f23efeb7364d)

图 1早期滤光思想与现代仪器功能的原创示意。上图突出从强散射中筛选不同颜色的光；下图说明像素计数如何经过标定成为光谱。光路为功能示意，未复原历史装置尺寸。

现代显微拉曼仪通常用激光提供窄波段入射光，用物镜把它聚焦到样品，同时收集返回的散射光。滤光器先抑制与激光同频的强烈瑞利散射，光栅再把剩余光按波长分开，探测器记录不同位置接收到的信号。可以把光栅想成一把把不同音高分到不同位置的“光学梳子”，但它分开的实际物理量是波长。探测器最初得到的是像素和计数；软件通过波长标定把像素位置换成波长，再结合激光波长换成拉曼位移。因此，横坐标准确和纵坐标准确是两个不同的标定任务。

激光的发展让这种微弱信号更容易测量，显微镜与阵列探测器又使空间定位和整段光谱采集成为常见操作。不过，仪器各部分的效率并不随波长保持不变：滤光片在某段透过得多一些，光栅和探测器又可能在另一段响应更高。因此，两个相距很远的峰，其原始计数比同时包含样品信息和仪器响应。NIST 的拉曼相对强度标准针对的正是这类响应校正问题。用硅等参照材料检查一个峰的位置，可以帮助核对横坐标；它不等于已经校正了全谱的相对强度。

观察弱光也意味着认真对待背景。样品荧光常形成缓慢变化的宽背景，玻璃基底和培养液可能贡献自己的谱带，探测器暗电流会随条件变化，偶发宇宙射线事件则可能产生孤立尖峰。它们看起来都属于“多出来的信号”，来源却不同。测量空白基底有助于识别基底峰，重复短曝光有助于识别偶发尖峰，暗信号记录帮助了解探测器本身，改变激发波长则可能显著改变荧光。把所有背景都交给同一个平滑按钮，往往会把不同问题混在一起。

## 光交换了一点能量，横坐标就记下这一点差别

把两个相连的原子想成由弹簧连接的小球，可以理解振动：原子会围绕平衡位置运动，键的伸缩和角度的变化具有各自特征。真正的分子由许多原子组成，一个振动模式往往包含多个原子协同运动。分子也不能任意连续地吸收或交出振动能量；量子描述把这些能量组织成允许的状态。拉曼散射中，入射光和离开光之间的能量差，恰好对应分子振动状态发生的变化。图中的虚能级是一种描述散射过程的中间状态表示，不是分子先停留一会儿的稳定电子能级。

![三种散射的能量收支。v 是振动态编号，0 和 1 分别表示图中的低、高振动态。等长的向上箭头表示相同入射光能量；斯托克斯过程给分子留下振动能量，反斯托克斯过程取走原有振动能量。虚线表示散射过程中的虚能级，不是稳定的电子激发态。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/506521438fbac5ff485b62e2.svg?v=506521438fba)

图 2三种散射的能量收支。v 是振动态编号，0 和 1 分别表示图中的低、高振动态。等长的向上箭头表示相同入射光能量；斯托克斯过程给分子留下振动能量，反斯托克斯过程取走原有振动能量。虚线表示散射过程中的虚能级，不是稳定的电子激发态。

瑞利散射前后，分子的振动状态没有改变，光也保留原来的能量。斯托克斯散射把一部分光能量留给分子，离开的光能量较低、波长较长。反斯托克斯散射则要求分子原先已经处在较高振动态，它把能量交给光，离开的光波长较短。在通常的室温条件下，多数分子占据较低振动态，因此许多常规拉曼测量主要分析斯托克斯一侧。温度升高会改变振动态的占据比例；若要利用两侧强度比测温，还要处理仪器响应以及其他激发条件，不能直接把任意两个原始峰高相除。

$$
\Delta\widetilde{\nu}=10^7\left(\frac{1}{\lambda_0}-\frac{1}{\lambda_s}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/888f64c1ee46a39652337b29.svg) | 拉曼位移，cm⁻¹；本式斯托克斯侧为正。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | 激光波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1a4fc1363bf176a12e0b860f.svg) | 散射光波长，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7d87fc730958fc67a28c903c.svg) | 将 nm⁻¹ 换算为 cm⁻¹ 的数值因子；1 cm = 10⁷ nm。 |

能量差与倒数波长的差成正比，所以先取倒数再相减。532 nm 激发下，1000 cm⁻¹ 位移对应约 561.89 nm 散射光；位移为零时散射波长与激光相同。

这里的倒数波长叫作波数。若波长用厘米表示，波数就是每厘米包含多少个波长，所以单位是 cm⁻¹。实验常把激光波长写成纳米，为了保持同一单位，需要乘上换算因子。用 532 nm 激光测到 1000 cm⁻¹ 的斯托克斯位移，散射波长约为 561.89 nm；换成 785 nm 激光，同样的振动对应约 851.87 nm。散射光的绝对颜色变了，能量差对应的位移仍然相同。也正因为如此，不同激发波长的光谱可以在统一的位移轴上比较峰位。相同的位移并不自动保证强度可直接比较，因为激发效率与仪器响应仍然可能改变。

$$
\Delta E=h c\,\Delta\widetilde{\nu}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | 分子获得的振动能量，J；这里描述斯托克斯过程。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 普朗克常数，6.62607015 × 10⁻³⁴ J·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 真空光速，此处用 2.99792458 × 10¹⁰ cm·s⁻¹，与 cm⁻¹ 配套。 |
| ![Formula](https://ml-biomat.com/static/agent-math/888f64c1ee46a39652337b29.svg) | 拉曼位移，cm⁻¹。 |

光子的能量等于普朗克常数乘频率，频率等于光速乘波数，因此两束光的能量差满足本式。1000 cm⁻¹ 对应 1.98645 × 10⁻²⁰ J，约 0.123984 eV；1 eV = 1.602176634 × 10⁻¹⁹ J。

还需要解释一件容易被忽略的事：为什么有的振动在红外光谱里明显，在拉曼里却弱？光的电场会使分子的电子云略微变形，电子云有多容易被改变，用极化率描述。如果某个振动过程会改变这种“容易变形的程度”，它就可能具有拉曼活性。红外吸收则与振动过程中偶极矩的变化有关。偶极矩描述正负电荷分布的不对称程度，这和极化率是不同性质。因此两种方法会从不同角度观察分子振动。对某些具有特定对称性的分子，选择规则更加严格；对复杂生物样品，实际价值往往在于把两种光谱作为互补证据。

这种互补性也解释了拉曼常用于含水体系的原因：水在很多常用拉曼指纹区域中的干扰方式，与红外吸收中的强水吸收不同，研究者有时更容易观察溶液或水合材料中的目标谱带。实际选择仍取决于浓度、荧光、基底、目标振动和采样深度。例如，透明水凝胶中的聚合物信号可能很弱，增加采集时间和优化聚焦会有帮助；若材料含有强荧光杂质，先改变激发条件可能比继续累加背景更有效。先识别问题的来源，仪器参数才有明确调整方向。

## 测量条件怎样进入光谱：功率、时间、焦点与样品

激光功率和曝光时间都能增加收到的光子数，但它们在样品上留下的作用不同。更大的功率把能量更快地集中到小区域，可能提高局部温度；更长的曝光则延长了受照时间，可能让光漂白、氧化或其他慢变化累积。用一个较低功率连续采集数条短光谱，可以观察峰位、峰形和背景是否随时间稳定，再决定是否延长总采集时间。若同一点的谱形持续改变，应先把这个变化作为实验现象研究：它可能显示样品正在受光影响，而不是仪器尚未“采够”。

计数中的随机起伏可以用抛硬币的类比理解。观察次数很少时，正反面的比例变化较大；观察次数增多后，比例更稳定。光子到达也具有统计起伏，在独立计数的理想近似下，计数标准差约等于平均计数的平方根。因此把曝光时间增加四倍，信号计数约增加四倍，而计数噪声约增加两倍，信噪比约提高两倍。背景光也参与这种起伏。即使之后数学上减去背景的平均值，背景在探测时引入的随机波动仍然留在数据里；一条看起来已经“贴着零线”的谱，不一定具有更好的实际信息质量。

$$
\mathrm{SNR}=\frac{S}{\sqrt{S+B+\sigma_r^2}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae03e7fd82fc9511ad569820.svg) | 信噪比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 目标信号的平均电子计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 同一采样通道或所选积分范围内的平均背景电子计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/91fd8c3471f776b7aee7c26b.svg) | 相同读出范围的读出噪声标准差，以电子计数表示。 |

独立泊松计数的方差等于平均计数，独立噪声的方差相加，再开平方得到总标准差。这里假设背景均值已知，未加入独立背景估计的不确定度。S=200、B=800、读出噪声忽略时，信噪比为 6.3246；交互采用读出标准差 5，得到 6.2470。

假设选定峰区域中拉曼信号产生 200 个计数，背景产生 800 个计数，其他噪声暂时忽略，则信噪比约为 6.32。让信号和背景都随曝光时间增加四倍，会得到 800 和 3200 个计数，信噪比约为 12.65。这个计算解释了长曝光的收益，也让我们看见另一条改善路线：如果能通过改变激发波长或样品条件降低背景，就可能在相同总照射量下获得更清楚的峰。下面的交互把峰计数、背景计数和探测器上限放在同一张图里；它采用教学计数模型，读数单位对应模型中的电子计数，而不是某一型号仪器的真实设置。

## 调节采集条件，观察信噪比与削顶

保持样品组成不变，改变功率、曝光时间和荧光背景。模型在峰顶产生每秒 40 × 功率系数的信号电子，背景产生每秒 160 × 背景系数 × 功率系数的电子，读出噪声标准差为 5 个电子。虚线表示理想信号，实线表示计数上限为 3000 时的记录；到达上限后峰顶会被削平。

[Figure: 采集参数与拉曼峰计数](https://ml-biomat.com/tutorials/experimental-methods/s02/#S02-plot)

先把曝光增加四倍，再把背景减半。对比两种改动怎样影响信噪比和峰形。这里的信噪比计算对应峰顶一个采样通道；绘图未添加随机起伏，以便直接看见计数上限的影响。

焦点与采样体积同样重要。显微镜上看起来“已经看见样品”，并不意味着拉曼焦点正好落在目标相中。薄膜上方的覆盖层、下方的玻璃以及倾斜表面都可能改变收集比例。测量粗糙或多孔材料时，应保存光学图、测量位置和聚焦规则；对比两组样品时，让物镜、偏振配置和采集几何保持一致。若研究本来就关心取向，应有意控制并扫描偏振方向，把取向变化变成实验变量。把一个有物理意义的变量控制住，比事后用归一化把所有谱线拉到同样高更可靠。

空间扫描还引入分辨率与时间之间的取舍。把网格间距设得很小，会产生更多数据点，却不会自动缩小光斑。相邻像素的采样区域可能高度重叠，长时间扫描中的漂移也会把位置与时间混在一起。可以先用较疏的网格找出区域差异，再对局部做更细的扫描；同时在扫描前后重复一个参照位置，检查仪器和样品是否稳定。记录空间步长、物镜、光斑相关条件、每点曝光和重复次数，能让后续的化学分布图具有可理解的空间含义。

## 从原始计数到峰面积：每一步都保留可检查的痕迹

本篇的数值实验含有三条构造谱带：两条相邻谱带位于 1000 和 1040 cm⁻¹，第三条较宽谱带位于 1450 cm⁻¹。它们叠加在一个缓慢弯曲的背景上，并加入固定随机种子的计数噪声。这些位置和宽度用于演示分辨与定量，不指定真实材料的化学归属。程序保留原始谱、已知真值、估计背景和拟合结果，读者可以在同一个文件里核对它们。这样的练习特别适合认识预处理：如果只看处理后的漂亮曲线，很难知道小峰是否被增强、压低，甚至被算法创造出来。

![构造教学光谱的完整处理。A 对比两种背景选区；B 显示相邻峰的贡献；C 检查残差；D 将估计面积比与已知真值 0.6 对照。所有面板来自同一次程序运行，峰位不指定真实材料的化学归属。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/598e7c5cd0d217e699175958.svg?v=598e7c5cd0d2)

图 3构造教学光谱的完整处理。A 对比两种背景选区；B 显示相邻峰的贡献；C 检查残差；D 将估计面积比与已知真值 0.6 对照。所有面板来自同一次程序运行，峰位不指定真实材料的化学归属。

图中第一步先用事先指定的无峰区估计二次多项式背景。选择无峰区意味着已经对哪些位置主要包含背景作了判断，实际实验里应借助空白、参照谱和重复测量，而不是凭曲线平滑就假定那里没有信号。把基线视为一条缓慢起伏的道路，峰是路面上的山丘：想知道山丘本身有多高，需要先估计道路的海拔。若把山坡也选进“道路”采样点，道路就会被抬高，山丘面积随之减少。程序还提供故意过宽的背景选区，展示同一条原始谱如何因选区变化得到不同面积比。

背景扣除之后，程序在一个局部窗口内同时拟合两条高斯峰。高斯形状在这里是一个已知的教学模型：中心控制峰的位置，宽度控制展开程度，面积控制总信号。两条峰越靠近，各自贡献越容易互相补偿，因此“拟合曲线贴得很好”与“两个峰的参数都确定得很好”不是一回事。检查残差时，要观察剩余误差是否围绕零随机分布，还是在某个位置连续偏高或偏低。成片的结构性残差会提示背景或峰形没有描述好；偶发尖点则需要回看原始曝光，而不是随意增加一条峰去吸收它。

$$
I(x)=\frac{A}{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eebf2869a2c97592f992b0eb.svg) | 横坐标为 x 时的模型峰强度，计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 拉曼位移，cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 整个模型峰的积分面积，计数·cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 峰中心，cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 高斯宽度参数，cm⁻¹；等于对应归一化高斯分布的标准差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | 自然指数函数；其括号中的比值无量纲。 |

前面的归一化因子使全峰积分等于 A，宽度增大时峰高相应减小。两条教学峰面积为 6000 和 3600 计数·cm⁻¹，面积比为 0.6；宽度分别为 9 和 14 cm⁻¹，峰高比约为 0.386。实验峰形需结合具体展宽机制选择。

峰高与峰面积回答不同问题。同样的总信号摊在更宽的范围里，峰就会更矮，因此峰高下降可能来自展宽，而不是组分变少。示例中两条相邻峰的设定面积分别为 6000 和 3600 计数·cm⁻¹，面积比为 0.6；它们的宽度不同，峰高比就不会等于 0.6。若用积分比较实验样品，还要固定基线规则、积分窗口、曝光、功率及响应校正；若用内部参照峰做比值，则要说明参照峰为什么在所比较条件下可以稳定代表采样量。归一化是把结果表达为相对量，应当知道分母是什么以及它是否改变。

统计上的重复也要分层。相同样品同一点的重复采集可以评估短期测量波动；一个样品上的不同位置能够显示空间异质性；独立制备的样品才支持对制备过程差异的讨论。程序的重复噪声模拟主要演示第一层，并不把它当作材料批次差异。画图时可同时呈现每个独立样品的汇总值与样品内部位置分布，让读者看见差异来自哪里。这样比把所有像素合并成一个巨大样本量更接近实际实验问题，也能帮助决定下一次应该多测几个位置，还是多制备几份样品。

## 完整计算：同时看拟合结果与处理选择的影响

下面的程序会生成原始光谱、两种背景估计、双峰拟合、计数与信噪比的关系以及能级和光路示意。运行后，数据以 CSV 保存，关键数值进入 summary.json，图像以可放大的 SVG 保存。代码从清楚的参数开始，再按背景估计、局部拟合和结果汇总的顺序组织，因此可以直接把构造光谱替换成自己导出的两列数据。替换时先检查横坐标单位、排序方向和采样间距；对非等间距数据做数值积分时，必须使用实际横坐标，不能把所有点默认当作相同间距。

### 构造光谱、估计背景并比较双峰面积

完整程序使用 NumPy、SciPy 和 Matplotlib，输出四组图、可检查的 CSV 和计算摘要。无需在线数据；固定种子保留教学谱的可复现性。

```
"""Raman measurement and processing with explicitly constructed teaching data.

Run: python main.py --output output --language en
No experimental material or chemical identity is assigned to the model bands.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from scipy.optimize import curve_fit

BLUE, TEAL, ORANGE, INK = '#245ca6', '#087f80', '#ce6b35', '#233446'


def band(x, area, center, sigma):
    """Area-normalized Gaussian; x, center and sigma are in cm^-1."""
    return area / (sigma * np.sqrt(2 * np.pi)) * np.exp(-.5 * ((x-center)/sigma)**2)


def two_bands(x, a1, c1, w1, a2, c2, w2):
    return band(x, a1, c1, w1) + band(x, a2, c2, w2)


def signal_to_noise(power, time, background=1):
    signal = 40 * power * time
    baseline = 160 * background * power * time
    return signal / np.sqrt(signal + baseline + 25)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    zh = language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif':
        ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'], 'font.size': 11,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': INK, 'text.color': INK, 'svg.fonttype': 'none',
        'axes.unicode_minus': False, 'figure.facecolor': '#fbfaf6',
        'axes.facecolor': '#fbfaf6', 'savefig.facecolor': '#fbfaf6'})
    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        fig.savefig(output / f'{name}-{language}.png', bbox_inches='tight', dpi=140)
        plt.close(fig)
    def arrow(ax, a, b, color=INK):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=14,
                     lw=2, color=color))

    # Figure 1: an original conceptual comparison of optical functions.
    fig, axes = plt.subplots(2, 1, figsize=(11.8, 7.2), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0, 11), ylim=(-.4, 3.4)); ax.axis('off')
    ax=axes[0]; ax.set_title(tr('1928：选择入射颜色，抑制强背景',
        '1928: Select incident color and reject the dominant light'), loc='left', pad=12)
    ax.add_patch(Circle((.8,1.25),.22,color='#dfae56'))
    for angle in np.arange(0,2*np.pi,.52):
        ax.plot([.8+.3*np.cos(angle),.8+.48*np.cos(angle)],
                [1.25+.3*np.sin(angle),1.25+.48*np.sin(angle)],color='#dfae56')
    for dy,color in [(-.08,BLUE),(0,'#7850a2'),(.08,TEAL)]:arrow(ax,(1.3,1.25+dy),(2.35,1.25+dy),color)
    ax.add_patch(Rectangle((2.45,.8),.15,.9,facecolor='#7850a2',alpha=.7))
    arrow(ax,(2.65,1.25),(4.05,1.25),'#7850a2')
    ax.add_patch(Rectangle((4.1,.65),.8,1.2,facecolor='#e1efef',edgecolor=INK))
    for sx,sy in [(4.3,.85),(4.6,1.15),(4.3,1.5),(4.65,1.65)]:ax.add_patch(Circle((sx,sy),.04,color=TEAL))
    arrow(ax,(4.5,1.3),(4.5,2.25),'#7850a2')
    arrow(ax,(4.65,1.3),(4.65,2.25),TEAL)
    ax.add_patch(Rectangle((4.1,2.3),.9,.12,facecolor=TEAL,alpha=.6))
    arrow(ax,(4.65,2.5),(4.65,3.1),TEAL)
    ax.text(.8,.35,tr('光源','Light source'),ha='center',fontsize=10)
    ax.text(2.5,.35,tr('选色滤光片','Incident filter'),ha='center',fontsize=10)
    ax.text(4.5,.35,tr('液体样品','Liquid specimen'),ha='center',fontsize=10)
    ax.text(5.2,2.35,tr('抑制原色，观察弱散射','Reject original color; observe shifted light'),fontsize=10,color=TEAL)
    ax.text(6.1,1.25,tr('入射与收集方向分开\n先选光，再辨认变化',
        'Separate illumination and collection\nSelect light before comparing its color'),fontsize=12,linespacing=1.8)
    ax=axes[1];ax.set_title(tr('现代：聚焦、滤光、分光、计数','Modern: Focus, reject, disperse and count'),loc='left',pad=12)
    ax.add_patch(Rectangle((.35,1.6),1.1,.6,facecolor='#e8eff2',edgecolor=INK))
    ax.text(.9,1.9,tr('激光','Laser'),ha='center',va='center')
    arrow(ax,(1.5,1.9),(3.7,1.9),BLUE)
    ax.plot([3.7,4.15],[2.1,1.65],color=INK,lw=3)
    arrow(ax,(3.92,1.7),(3.92,.9),BLUE)
    ax.add_patch(Rectangle((3.55,.65),.8,.25,facecolor='#d5e2e8',edgecolor=INK))
    ax.plot([3.55,3.75,4.15,4.35],[.65,.42,.42,.65],color=INK)
    ax.add_patch(Rectangle((3.5,.05),1,.12,facecolor=TEAL))
    arrow(ax,(4.15,.3),(4.15,2.48),TEAL)
    ax.plot([3.95,4.35],[2.35,2.75],color=INK,lw=2)
    arrow(ax,(4.35,2.55),(5.65,2.55),TEAL)
    ax.add_patch(Rectangle((5.75,2.1),.15,.9,facecolor=TEAL,alpha=.65))
    arrow(ax,(6,2.55),(7.8,2.55),TEAL)
    ax.plot([8,8.3],[2.15,2.95],color=INK,lw=4)
    for k in range(5):ax.plot([7.96+.06*k,8.08+.06*k],[2.17+.15*k,2.15+.15*k],color='#8895a5')
    for y,col in [(2.,ORANGE),(2.5,TEAL),(3.,BLUE)]:arrow(ax,(8.35,2.55),(9.85,y),col)
    ax.add_patch(Rectangle((9.9,1.75),.24,1.5,facecolor='#e8eff2',edgecolor=INK))
    for y in np.linspace(1.8,3.2,11):ax.plot([9.9,10.14],[y,y],color='#8b98a5',lw=.7)
    ax.text(3.35,.65,tr('物镜','Objective'),ha='right',fontsize=10)
    ax.text(3.98,-.2,tr('样品','Specimen'),ha='center',fontsize=10)
    ax.text(5.82,1.7,tr('瑞利抑制','Rayleigh rejection'),ha='center',fontsize=10)
    ax.text(8.1,1.7,tr('光栅','Grating'),ha='center',fontsize=10)
    ax.text(10.02,1.3,tr('像素阵列','Pixel array'),ha='center',fontsize=10)
    ax.text(7.3,.5,tr('像素 → 波长 → 拉曼位移','Pixels → wavelength → Raman shift'),ha='center')
    save(fig,'optics')

    # Figure 2: energy bookkeeping, not a molecular potential-energy curve.
    fig,axes=plt.subplots(1,3,figsize=(11.8,4.5),layout='constrained')
    for ax,name,start,end in zip(axes,[tr('瑞利','Rayleigh'),tr('斯托克斯','Stokes'),tr('反斯托克斯','Anti-Stokes')],[0,0,1],[0,1,0]):
        ax.set(xlim=(0,3),ylim=(-.5,4.9));ax.axis('off');ax.set_title(name)
        for y in [0,1]:ax.plot([.2,2.8],[y,y],color=INK,lw=1.6)
        virtual=3+start
        ax.plot([.2,2.8],[virtual,virtual],color='#8b93a0',ls='--',lw=1.4)
        arrow(ax,(.85,start),(.85,virtual),BLUE);arrow(ax,(2.1,virtual),(2.1,end),TEAL)
        ax.text(1.5,virtual+.28,tr('虚能级（过程表示）','Virtual level (process representation)'),ha='center',fontsize=9)
        ax.text(2.7,-.32,'v = 0',ha='right',fontsize=9)
        ax.text(2.7,1.16,'v = 1',ha='right',fontsize=9)
        ax.text(.4,2.05,tr('入射','In'),color=BLUE);ax.text(2.25,2.05,tr('散射','Out'),color=TEAL)
    save(fig,'energy')

    # Independent photon counts; all generating parameters remain inspectable.
    rng=np.random.default_rng(248)
    x=np.arange(600.,1801.)
    base=110+.035*(x-600)+.000045*(x-1200)**2
    truth=two_bands(x,6000,1000,9,3600,1040,14)+band(x,12000,1450,28)
    raw=rng.poisson(base+truth).astype(float)
    anchors=(x<950)|((x>1120)&(x<1320))|(x>1560)
    contaminated=anchors|((x>1380)&(x<1520))
    fit_base=lambda m:np.polyval(np.polyfit((x[m]-1200)/600,raw[m],2),(x-1200)/600)
    good,bad=fit_base(anchors),fit_base(contaminated)
    region=(x>=950)&(x<=1120)
    def fit(background):
        return curve_fit(two_bands,x[region],(raw-background)[region],
           p0=[6000,1000,9,3600,1040,14],
           bounds=([0,990,3,0,1025,3],[20000,1010,25,20000,1055,35]),maxfev=20000)[0]
    params,biased=fit(good),fit(bad)
    model=two_bands(x[region],*params)
    residual=(raw-good)[region]-model
    np.savetxt(output/'spectrum.csv',np.column_stack([x,raw,base,truth,good,bad]),delimiter=',',
       header='shift_cm-1,raw_counts,true_background,true_bands,estimated_background,contaminated_background',comments='')
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    ax=axes[0,0];ax.plot(x,raw,color='#8895a5',lw=.7,label=tr('原始计数','Raw counts'))
    ax.plot(x,good,color=TEAL,lw=2,label=tr('无峰区估计','Clean anchors'))
    ax.plot(x,bad,color=ORANGE,lw=2,label=tr('含峰区估计','Contaminated anchors'))
    ax.set(title=tr('A · 原始信号与两种基线','A · Raw signal and two baselines'),ylabel=tr('计数','Counts'));ax.legend(fontsize=9)
    ax=axes[0,1];ax.plot(x[region],(raw-good)[region],'.',ms=3,color='#8a95a5',label=tr('扣除基线','Corrected'))
    ax.plot(x[region],model,color=INK,label=tr('双峰拟合','Two-band fit'))
    ax.fill_between(x[region],band(x[region],*params[:3]),alpha=.2,color=BLUE)
    ax.fill_between(x[region],band(x[region],*params[3:]),alpha=.2,color=TEAL)
    ax.set(title=tr('B · 相邻峰分别贡献多少','B · Contributions of neighboring bands'),ylabel=tr('计数','Counts'));ax.legend(fontsize=9)
    ax=axes[1,0];ax.plot(x[region],residual,color=BLUE,lw=.9);ax.axhline(0,color=INK,lw=1)
    ax.set(title=tr('C · 残差保留处理线索','C · Residuals retain diagnostic evidence'),ylabel=tr('数据 − 拟合 / 计数','Data − fit / counts'))
    ax=axes[1,1];ratios=[.6,params[3]/params[0],biased[3]/biased[0]]
    ax.bar([0,1,2],ratios,color=['#8b98a5',TEAL,ORANGE],width=.55)
    ax.axhline(.6,color=INK,ls='--',lw=1)
    ax.set(xticks=[0,1,2],xticklabels=[tr('真值','Truth'),tr('无峰区','Clean anchors'),tr('含峰区','Contaminated')],
       ylabel=tr('第二峰面积 / 第一峰面积','Second / first band area'),title=tr('D · 基线选择改变面积比','D · Baseline choice changes the area ratio'),ylim=(0,max(.9,max(ratios)*1.2)))
    for i,v in enumerate(ratios):ax.text(i,v+.025,f'{v:.3f}',ha='center')
    for ax in [axes[0,0],axes[0,1],axes[1,0]]:ax.set_xlabel(tr('拉曼位移 / cm$^{-1}$','Raman shift / cm$^{-1}$'))
    save(fig,'processing')

    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained')
    t=np.linspace(.1,20,300)
    for b,color in [(1,BLUE),(.25,TEAL)]:axes[0].plot(t,signal_to_noise(1,t,b),color=color,label=tr('背景系数','Background factor')+f' {b:g}')
    axes[0].set(xlabel=tr('曝光时间 / s','Exposure time / s'),ylabel=tr('信噪比','Signal-to-noise ratio'),title=tr('A · 收集更久或降低背景','A · Collect longer or reduce background'));axes[0].legend()
    power=np.linspace(.1,5,150);time=np.linspace(.1,20,180);pp,tt=np.meshgrid(power,time)
    im=axes[1].pcolormesh(pp,tt,signal_to_noise(pp,tt),shading='auto',cmap='viridis')
    cs=axes[1].contour(pp,tt,200*pp*tt,levels=[3000],colors='white',linewidths=1.8)
    axes[1].clabel(cs,fmt={3000:tr('计数上限','Count limit')},fontsize=9)
    axes[1].set(xlabel=tr('功率系数','Power factor'),ylabel=tr('曝光时间 / s','Exposure time / s'),title=tr('B · 先确认线性记录范围','B · Identify the linear recording range'))
    fig.colorbar(im,ax=axes[1],label=tr('理想信噪比','Ideal signal-to-noise ratio'))
    save(fig,'acquisition')
    summary={'data_kind':'constructed teaching spectrum','seed':248,
      'stokes_532_nm':1/(1/532-1000/1e7),'stokes_785_nm':1/(1/785-1000/1e7),
      'energy_1000_eV':6.62607015e-34*299792458*1000*100/1.602176634e-19,
      'true_area_ratio':.6,'fitted_area_ratio':float(params[3]/params[0]),
      'contaminated_area_ratio':float(biased[3]/biased[0]),'parameters':params.tolist(),
      'snr_example_without_read_noise':float(200/np.sqrt(1000)),
      'lab_snr_default':float(signal_to_noise(1,5)),
      'residual_rms':float(np.sqrt(np.mean(residual**2)))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

程序把拟合中心与宽度限制在具有物理意义的范围内，避免算法为了贴合噪声把一个峰挪到远处或赋予负宽度。约束应来自仪器分辨率、已知峰区域和实验目的，而不是为了让两组样品恰好得到预期差异。程序也保存残差，使用固定的无峰区规则进行背景估计，并把故意包含宽峰的错误选区作为对照。读者可以把宽峰从 1450 cm⁻¹ 逐渐移向背景选区，再观察估计基线与面积比如何变化。这种修改直接检验了预处理的假设，比单纯尝试几十种滤波参数再选择最好看的曲线更能说明问题。

![同一计数模型中的曝光收益与记录上限。左图比较背景系数为 1 和 0.25 时的理想信噪比；右图白线以上的条件使峰顶总计数超过 3000。颜色显示未削顶前的计数模型，白线标出它与实际记录开始分离的位置。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/218ba19bb4267a10c14b6050.svg?v=218ba19bb426)

图 4同一计数模型中的曝光收益与记录上限。左图比较背景系数为 1 和 0.25 时的理想信噪比；右图白线以上的条件使峰顶总计数超过 3000。颜色显示未削顶前的计数模型，白线标出它与实际记录开始分离的位置。

图中的功率—时间图采用同一组计数规则计算，颜色表示信噪比，边界表示选定探测器计数上限。对于处于线性响应范围且样品稳定的区域，提高总光子数会改善计数精度；到达上限后，记录峰形会被削平，继续曝光并不会恢复丢失的峰顶信息。真实仪器的计数上限、读出噪声、暗电流与增益设置有关，教学模型中的数字用于理解关系。把自己的仪器参数代入之前，应先从仪器说明、暗场和线性范围测试确定这些量，再比较同一采集任务的不同配置。

处理完成后，最值得保存的不是单独一张最终曲线，而是原始数据、采集条件、参照与空白、处理参数和用于形成结论的汇总结果。这里的保存关系就像一张有刻度的实验地图：最终的峰面积指向一个积分窗口，窗口指向背景扣除后的谱，背景又指向具体的估计规则。后续若发现某个波段存在基底干扰，可以沿这条关系重新计算，而不必猜测最早的操作。图像的可追溯性也使不同研究者能够比较各自的处理选择，把争论落实到数据和物理解释上。

## 把谱图放回研究问题：一张图需要哪些相互支持的线索

假设正在研究一种含蛋白质的水凝胶，想知道经过处理后是否出现成分重新分布。比较原始光谱时，先确定各位置的曝光、功率和聚焦条件一致，再查看相关谱带是否共同变化。若只看到所有峰同时放大，采样体积或聚焦变化就是需要优先检查的因素；若某组峰相对另一组稳定峰系统变化，才更接近成分比例变化的证据。随后把峰面积比画成空间图，并与明场图、样品几何或另一种化学表征对应，就能判断信号差异是否跟真实结构位置一致。研究结论来自这些线索的相互支持。

对于聚合物薄膜，峰位与峰宽的变化也可能包含应力、温度或有序程度的信息。把这些信息用于定量，需要针对同一材料、同一光学配置建立与控制变量的关系，例如在已知温度下测量峰位随温度的变化，再讨论未知状态。把其他材料的经验系数直接套过来，会丢掉化学结构和相态对响应的影响。若拉伸后峰强度发生变化，可以增加不同偏振方向的测量，分辨分子取向与浓度变化；若峰位随照射时间漂移，可以把功率序列和时间序列分开设计，寻找激光加热的贡献。

增强拉曼、共振拉曼和相干拉曼拓展了可研究的问题，但它们各自引入新的信号形成机制。表面增强拉曼利用金属纳米结构附近的局域场等效应提高某些分子的信号，分子与热点的距离、吸附方式及热点分布会影响强度。此时，一条很强的峰并不只由溶液总体浓度决定。理解普通拉曼中的采样量、响应和背景后，再进入这些方法，就能清楚地提出校准问题：增强发生在哪里，哪些分子真正被观察到，参照与目标经历了怎样的局部环境。

读完一张拉曼图，可以依次回答四个具体问题：横坐标对应什么能量差，纵坐标经历了哪些校正，峰的变化指向哪一种物理或化学解释，以及哪一个补充测量能区分仍然并存的解释。若两条峰重叠严重，可以考虑提高分辨能力、测量参照组分或联合另一种光谱；若空间分布很不均匀，则应增加有设计的空间采样。拉曼的价值正是在保留分子信息的同时，把这些信息带到微小位置。知道信号怎样形成，也就知道怎样把一次测量变成有方向的研究。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [C. V. Raman and the Raman Effect — ACS](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html)

   早期滤光实验、Raman 与 Krishnan 的历史背景。
2. [Raja and Barron: Raman Spectroscopy](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Physical_Methods_in_Chemistry_and_Nano_Science_%28Barron%29/04%3A_Chemical_Speciation/4.03%3A_Raman_Spectroscopy)

   散射能级、选择规则和表面增强拉曼的延伸阅读。

   CC BY 4.0 page; cited as open reading.
3. [NIST: Raman Intensity Calibration With Glass Luminescence Standards](https://www.nist.gov/publications/raman-intensity-calibration-glass-luminescence-standards)

   理解波长相关仪器响应与相对强度标定。
4. [RamanSPy: Preprocessing](https://ramanspy.readthedocs.io/en/latest/preprocessing.html)

   基线、去尖峰、平滑和归一化的公开软件入口。
5. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   非线性最小二乘参数、边界与拟合协方差说明。
