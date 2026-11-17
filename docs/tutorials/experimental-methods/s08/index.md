# ICP发射光谱：把元素的光变成可靠的含量

Source: https://ml-biomat.com/tutorials/experimental-methods/s08/
Language: zh-CN

从材料浸出与组成出发，理解氩等离子体、谱线分离、定量校准和元素质量账本。

## 一杯透明液体里，材料留下了什么？

把含钙的聚合物薄片放进缓冲液，几天后取出，液体看起来仍然清澈。钙可能已经进入溶液，薄片也可能只是在表面发生了变化。肉眼分不出这两种情形，称重又容易受到吸水、残余盐和干燥程度的影响。ICP发射光谱能沿着另一条路径回答问题：把一小部分液体送进高温氩等离子体，观察其中元素发出的特征光，再用已知浓度的标准液把光信号换算成含量。对生物材料研究来说，这让元素释放、无机填料组成、痕量金属残留和培养环境变化成为可以分别测量的问题。

“ICP”是电感耦合等离子体的英文缩写，描述产生高温光源的方式；“OES”表示光学发射光谱，“AES”强调原子发射，在这里指向同一类元素光谱测量。仪器记录的是特定波长附近的光，而溶液的毫克每升浓度来自校准。这个过程很像用一个具有已知刻度的接收器辨认不同乐器：音高帮助确定是谁在发声，响度还要经过比较才能说明有多少。元素谱线的波长对应电子能级差，光强则受到元素量、进样效率、等离子体状态和光路共同影响，因此这两个任务需要分开理解。

研究开始时，要把“多少”说完整。浸提液中的钙浓度，乘以这次收集的液体体积，得到该液体包含的钙质量；再除以放入的材料质量，可以得到每克材料在相应条件下释放的量。若把材料整体溶解并完全消解，再测钙，则回答材料原先含有多少钙。两次实验即便使用同一台仪器，分母、时间范围和制样过程也不同。后文的完整数值例子固定采用一种构造的低钙聚合物复合材料，测其干基总钙含量；开头的浸出问题用来说明研究用途，两者各自保留清楚的测量定义。

ICP-MS也会用到氩等离子体，但接下来的检测路径变了：它把离子送入真空系统，按质量与电荷之比区分并检测；ICP-OES则收集发出的光，按波长区分。这样的差别决定了需要处理的干扰，前者关注同质量或多原子离子的贡献，后者关注谱线重叠和光学背景。选择方法还取决于待测浓度、基体、元素、样品数量和已有条件。对于材料中多个主量或微量元素的组成，OES的多元素测量十分实用；当目标转向极低含量元素或同位素信息时，就需要评估相应的质谱方法。

发光之前，原来的分子结构已经历了强烈改变。因此，测得钙元素并不会直接告诉我们它原先属于磷酸钙、碳酸钙还是某种可溶盐；测得铬也不等于已经区分不同化学形态。材料的晶相可以结合衍射判断，官能团可以结合红外分析，元素在表面还是内部则要结合取样设计。把这些问题分别交给合适的证据，能让ICP结果在研究中发挥明确作用：它负责一个定义清楚的元素质量账本。

## 从火焰的颜色，到高温等离子体中的电子

1860年，基尔霍夫和本生发表了用光谱观察进行化学分析的研究。把盐送入火焰，肉眼看到的颜色只是一个粗略印象；让光经过狭缝和棱镜，不同颜色会沿不同方向展开，形成可区分的明线。原先混在一起的亮光由此变成了具有位置结构的信号。图中用原创光路示意展示这个思想：狭缝限定光束，分光元件把波长展开，观察者在不同位置寻找特征。现代仪器常用光栅和电子检测器，但“先把光分开，再比较各处强度”的逻辑仍然相通。

颜色可以帮助认元素，强度却容易受到周围物质影响。Greenfield、Jones和Berry在1964年的论文开头讨论过一个具体困难：火焰中的钙发射会受到磷和铝的抑制。样品并没有凭空少掉钙，改变的是元素进入发光状态的效率。这个问题促使他们研究高温等离子体作为光谱激发源，其中高频感应方式的持续放电不需要电极伸入光源。历史在这里提供了一条实用线索：分析方法的进步，常常起于“同样的元素量为何给出不同读数”，而今天的基体校正仍在处理这类问题。

![原创科学史与仪器原理示意。A：1860年光谱分析的分光思想，颜色和几何为说明用途。B：1964年论文讨论的钙受磷、铝抑制问题，柱高是概念示意。C：喷雾筛选、排液、同心炬管、外绕射频线圈及轴向/径向收光；两条光路表示可选方向，未按实物比例绘制。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/53f6d271f2fe27f3c7015e06.svg?v=53f6d271f2fe)

图 1原创科学史与仪器原理示意。A：1860年光谱分析的分光思想，颜色和几何为说明用途。B：1964年论文讨论的钙受磷、铝抑制问题，柱高是概念示意。C：喷雾筛选、排液、同心炬管、外绕射频线圈及轴向/径向收光；两条光路表示可选方向，未按实物比例绘制。

等离子体可以看成含有大量自由电子和离子的气体。线圈中的射频电流产生随时间变化的磁场，在气体中感应出电场；已有的带电粒子从中获得能量，通过碰撞把能量传给更多粒子，维持等离子体。点火提供起始带电粒子，后续能量主要由射频感应输入。氩气既承载样品，也参与维持放电。这里的“高温”不是把每个位置都视为温度相同的一只炉子，进样通道、外侧区域和观察位置存在差异，这也是气流、功率和观察位置会改变信号的原因。

样品首先经过雾化器成为许多液滴，雾室再筛掉较大的液滴，让较细的气溶胶进入等离子体。它很像喷雾之后再做一次按液滴行为的选择：吸入多少液体，并不等于多少液体都进入了有效发光区。细液滴先失去溶剂，残余物蒸发并形成原子，随后发生激发、电离等过程。一个原子或离子的电子获得能量后，可以处在较高能级；回到较低能级时释放光子。这个较低能级可以是基态，也可以仍是某个激发态，因此同一元素会出现多条谱线。

$$
\Delta E=E_{\mathrm{upper}}-E_{\mathrm{lower}}=h\nu=\frac{hc_0}{\lambda_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | 单个光子的能量或能级差，J；也可换算为eV |
| ![Formula](https://ml-biomat.com/static/agent-math/d8ddb0fdc5f500d4eb915283.svg) | 跃迁的较高、较低能级能量，J |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 普朗克常数6.62607015×10⁻³⁴ J·s |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 光的频率，s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | 真空光速299792458 m/s；下标0表示真空 |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | 真空波长，m；400 nm=400×10⁻⁹ m |

电子降到较低能级时，能量差由一个光子带走。真空中频率等于光速除以波长，因此两个表达相同。400 nm对应4.9661×10⁻¹⁹ J，除以每电子伏特的1.602176634×10⁻¹⁹ J，得到3.09960496 eV。空气波长须先按折射率换算，光强不由本式单独给出。

公式把光的波长与单个光子的能量联系起来。波长越短，一个光子携带的能量越大，但光子能量大并不等于样品浓度高；浓度校准主要利用选定谱线的信号大小。以真空波长400 nm为例，计算得到每个光子约3.100 eV。纳米是十亿分之一米，电子伏特则是适合描述原子能量变化的单位。线表有时列空气波长，精密换算时要区分介质；本章光谱横轴使用NIST钙线表中的空气波长，光子算例则明确采用真空波长，避免把两种定义混在一起。

谱线名称中的罗马数字也有特定含义。Ca I表示中性钙原子，Ca II表示失去一个电子的钙离子。这里的II是光谱命名中的第二个电离阶段，不能按日常化学式的写法理解成“二价钙”。更重要的是，这个标记描述在等离子体中发光的粒子，而不是测量前材料里的钙以什么化学形态存在。高温激发把元素从原来的结构中释放出来，为稳定比较元素量创造条件，也改变了我们能够直接读取的信息种类。

## 先定义样品，再决定怎样把它送进仪器

透明液体也可能含有肉眼看不见的颗粒，尤其在研究纳米材料或缓慢溶解的无机填料时。若要测操作定义下的溶解态元素，过滤顺序就很关键。例如EPA 200.7采用先通过0.45 μm滤膜、再酸化的定义。这个孔径是实验操作的边界，细小纳米颗粒仍可能通过。若先加酸，部分原本应留在颗粒中的元素可能提前溶出，最终结果回答的已经是另一个问题。实验记录因此需要保存滤膜孔径、过滤与酸化顺序、取样时间和体积，保证不同组之间比较的是同一种分数。

如果关注悬浮颗粒和溶液共同包含的可回收元素，需要采用相应提取或消解过程。方法中的“总可回收”有具体操作含义，并不自动等于任何难溶晶体中的全部元素都已释放。聚合物、组织、陶瓷和含硅矿物的分解难度差别很大；消解方案应与材料组成和目标元素匹配，并通过适合的参考材料或其他回收证据验证。观察到液体澄清只能说明大颗粒减少，不能代替对完整释放的验证。在比较材料组成时，这一步决定所测到的是总量还是某种可提取量。

后面的教学样品设为干燥后的低钙复合材料，称取0.2500 g，本算例假定钙已完整进入消解液，最终定容至50.00 mL。这里“定容”指溶解和转移完成后，把整个溶液补到规定总体积，而不是简单地加入50 mL液体。随后取消解液的一部分，再作10倍稀释用于进样。干基质量、消解总体积和再次稀释的倍数分别保存，才能把仪器的mg/L读数换回材料的mg/kg。若改用吸水后的试样质量，分母会包含水，结果应明确写为相应的湿基或原样基准。

处理痕量元素时，容器和试剂也是样品的一部分。水、酸、滤膜、离心管和取样工具可能引入待测元素，较高浓度样品还会在进样管路中留下残留。方法空白应经历与样品相同的关键制备步骤，用来观察这些额外贡献；校准空白主要用于建立标准系列的零点和相应酸基体。两者的任务不同。谱线背景扣除、校准截距和方法空白也不能当成三个可以机械相减的同义量：一个单独的污染空白更应触发污染来源排查和相关样品复核，而不是自动从所有样品中减去同一个数。

把液体稀释有时比复杂校正更有效，因为盐含量、酸度和黏度下降后，雾化和传输更接近标准液。但目标元素也同时变稀，低浓度测量会更依赖空白和噪声。选择稀释倍数像调节显微镜的视野：需要让待测对象进入适合观察的范围，又要保留足够信号。可以先用适当稀释的少量样品估计浓度，再检查标准范围、目标信号和基体表现；最终报告使用实际执行的全部体积与倍数，而不是只写一个印象中的“大约稀释十倍”。

## 找到钙的谱线，还要知道旁边是谁

光谱仪把不同波长的光分到不同检测位置，但每条谱线都有宽度。粒子运动、发光环境和仪器分辨能力共同影响观测到的形状；即使真实跃迁很窄，有限的光学分辨率也会让它在图上占据一段范围。两条靠得近的线因此可能堆在一起，如同隔墙听到两个人同时说话。峰顶升高既可能来自更多目标元素，也可能来自邻近谱线的尾部。选线时需要同时考虑目标线的灵敏度、附近元素、背景、基体浓度和当前仪器的实际分辨能力。

本章以Ca II的317.9332 nm空气波长作为目标中心。NIST表中还列有其他钙线，例如Ca II的393.36614 nm和Ca I的422.6727 nm；这些事实波长帮助确认位置，表中相对强度则来自特定资料条件，不能直接替代本仪器的浓度校准。图里添加的邻峰明确是构造的干扰峰，不指定为某个真实元素跃迁。这样可以单独考察“距离变近会怎样”，而不会把教学设定误认成一组已经确认的实际谱线归属。

![构造谱线与实际拟合输出。目标中心为NIST所列Ca II空气波长317.9332 nm；另一条为模拟干扰峰，间距0.018 nm，共同半高全宽0.014 nm。噪声标准差20 a.u.；残差带为±40 a.u.。D中条件数针对扣去常数/线性背景并归一化后的两列峰形，体现系数对噪声的敏感性。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fb370970c0d2272c17d1ceef.svg?v=fb370970c0d2)

图 2构造谱线与实际拟合输出。目标中心为NIST所列Ca II空气波长317.9332 nm；另一条为模拟干扰峰，间距0.018 nm，共同半高全宽0.014 nm。噪声标准差20 a.u.；残差带为±40 a.u.。D中条件数针对扣去常数/线性背景并归一化后的两列峰形，体现系数对噪声的敏感性。

测量窗口里还存在连续背景。一个直观处理办法是在目标峰两侧选择没有其他谱线的区域，用这些区域估计背景，再读取目标峰的贡献。两侧背景点本身也要检查：若把另一个元素的峰误当成背景，扣除量就会过大，目标浓度反而被低估。谱线重叠通常让信号变高，错误背景点却可能让结果变低，这说明不能只凭偏差的方向猜测原因。观察完整窗口、比较可用的另一条谱线，并检查样品稀释后是否给出一致回算值，往往比盯着一个峰顶更有判断力。

$$
y_i=A\,g_i+B\,h_i+b_0+b_1x_i+\varepsilon_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 波长采样点编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i点的观测信号，a.u.（任意但一致的信号单位） |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | 目标峰和干扰峰的峰高，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/4c96cf679f9702a712ef0a78.svg) | 给定位置、宽度的两条峰形，中心归一为1，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | 目标中心处的线性背景，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/86ef2a91a3da50f97dc73bcd.svg) | 背景随波长变化的斜率，a.u./nm |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | 相对于目标中心的波长偏移，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/df6c5ac19bbf29886eee1c95.svg) | 第i点随机噪声，a.u. |

在探测器线性范围内，不同光贡献相加。本例取A=7680、B=4608、b₀=250、b₁=800；目标中心x=0，g=1，邻峰尾部h约0.01022，平均信号约7977.1 a.u.。固定峰位和线宽后作最小二乘；两形状完全相同只确定A+B，分别估计需要独立信息。

图中的模型把观测写成目标峰、干扰峰、缓慢变化的背景和随机噪声之和。两个峰形在各自中心取值为1，因此系数表示峰高，单位与信号相同。实际软件也可以采用面积或其他线形定义，只要标准和样品的处理一致。这里先固定峰位置和宽度，让拟合只决定各项贡献，方便看清一个重要问题：当两个峰形几乎相同时，给目标峰多分一些、给干扰峰少分一些，仍可能得到几乎相同的总曲线。残差很小，不能单独保证每个分量都分得准确。

交互实验用一个条件数来显示这种噪声放大：先从两条峰形中去掉常数和线性背景可以解释的部分，再把剩余的两列形状归一到相同长度，比较它们的相似程度。条件数接近1时，两个方向较容易区分；峰逐渐重合时，系数对很小的噪声也会变得敏感。完全重合的两条线只提供总贡献，当前窗口无法分别确定两个峰高。此时要换用干扰更少的谱线、提高可用分辨能力，或加入来自其他测量的独立信息。界面会显示这一变化，而不会在任何重叠程度下都给出一个看似精确的浓度。

同一台ICP还可能沿等离子体轴向或从侧面径向观察。轴向通常穿过较长的发光路径，既可能得到更强的目标信号，也可能收集更多背景和基体影响；径向观察的区域和路径不同，在某些高基体样品中更合适。它们是观察同一类光源的不同几何方式。强谱线在高浓度下还可能出现自吸收，部分光在离开光源前再次被吸收，使信号与浓度的关系弯曲。选线、视角和稀释因此要共同服务于一个目标：让标准和样品处于可比较的响应范围。

## 从仪器读数，走回一克材料

校准系列相当于给光信号建立一把刻度尺。我们配制0、0.25、0.50、1.00和2.00 mg/L五个钙水平，各构造三次进样读数，用它们拟合一条带截距的直线。标准溶液应有可追溯的浓度，配液体积和酸度要与设计相符；由同一支原液配出的标准具有共同的来源误差，重复进样只能告诉我们短期读数的散布。检查液若来自独立来源，就能帮助发现校准原液或配液过程中的共同偏差，这一点比单纯增加同一瓶标准的重复次数更有信息。

$$
S=a c+b,\qquad \widehat c=\frac{S_{\mathrm{sample}}-b}{a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 标准的净谱线信号，a.u.；光谱背景已按同一流程处理 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 标准元素浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 校准斜率，a.u.每mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 校准截距，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5e0d97dd9bcf99758f72c2f.svg) | 与标准同样处理的样品信号，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/70e13ece2487a9b7956f0a74.svg) | 回算的进样液浓度，mg/L；帽号表示估计值 |

在线性范围与可比响应条件下，先减去零点再按斜率换单位。理想a=12000、b=150、Ssample=9750，得到0.800 mg/L。实际构造观测拟合a≈12002.666、b≈142.092，三次未知液读数平均得到0.8005197 mg/L。方法空白承担制样污染诊断，不再机械减一次同一截距。

直线斜率表示每增加1 mg/L会增加多少信号，截距表示该校准处理流程在零浓度时的响应。样品信号减去截距后再除以斜率，就像先把尺子的起点对齐，再按每格长度读数。本例实际运行得到斜率约12002.67 a.u.每mg/L、截距约142.09 a.u.，未知液三次进样的平均回算浓度约0.80052 mg/L。这个结果来自明确标识的构造观测，不是实验室采集的数据；它保留了随机噪声，所以不会恰好等于设定的0.80000。

![构造的五水平校准与低钙复合材料算例，各标准三次进样，误差为固定随机噪声。未知液三次读数的均值回算约0.80052 mg/L。C假定钙完整进入50.00 mL消解液，原样干质量0.2500 g，另稀释10倍，得到约1601.04 mg/kg。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fa6ec1500a1bca5f3e412c74.svg?v=fa6ec1500a1b)

图 3构造的五水平校准与低钙复合材料算例，各标准三次进样，误差为固定随机噪声。未知液三次读数的均值回算约0.80052 mg/L。C假定钙完整进入50.00 mL消解液，原样干质量0.2500 g，另稀释10倍，得到约1601.04 mg/kg。

拟合完成后，先看每个标准点的残差，也就是观测减去拟合。若中间水平总偏低而两端总偏高，可能存在弯曲；若高浓度散布明显更大，就要考虑误差大小随浓度变化以及相应的加权拟合。相关系数很高也可能掩盖低浓度处的重要偏差，因为高浓度点支配了整体变化范围。本例绘出全部十五个点和残差，让读者把校准看成一组可以诊断的测量关系，而不是只接受软件给出的一个漂亮指标。未知液也应处于验证过的范围内，超过上限时优先稀释后重测。

$$
w=\frac{\widehat c\,D\,V}{m_s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 原干基材料的元素含量，mg/kg |
| ![Formula](https://ml-biomat.com/static/agent-math/70e13ece2487a9b7956f0a74.svg) | 最终进样液的回算浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 从消解液到进样液的总稀释倍数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 全部原消解液的定容体积，L |
| ![Formula](https://ml-biomat.com/static/agent-math/e9ba2f332f9416cc47936a32.svg) | 该消解液对应的原样干质量，kg |

假定元素完整释放且转移，浓度乘体积得到元素质量，再除以样品质量。0.800×10×0.05000/0.0002500=1600 mg/kg=0.16%质量分数。程序用带噪声的回算浓度得到约1601.04 mg/kg。浸提实验采用其实际收集体积和取样账本，结果应命名为相应浸出量。

理想算例中的0.800 mg/L是最后进样液的浓度，乘10得到原消解液的8.00 mg/L；乘0.05000 L得到整瓶消解液中的0.400 mg钙；再除以0.0002500 kg材料，就得到1600 mg/kg，也就是质量分数0.16%。这适合本例的低钙复合材料设定，并不是纯磷酸钙材料的典型组成。把实际运行的0.80052代入同样的体积账本，会得到约1601.04 mg/kg。中间的钙质量很有用：它能帮助发现把毫升误当升、把克误当千克或把稀释倍数用两次造成的千倍偏差。

若研究对象换成浸出液，最后一步的意义也随之变化。一次完整收集的20.0 mL液体若含0.800 mg/L钙，其中就是0.0160 mg钙；若对应0.2500 g材料，则是0.0640 mg/g材料的该次浸出量。连续取样并补加新液时，之前取走的元素也要进入累计账本；单次终点浓度乘当前体积会漏掉已经带走的部分。把时间、取样体积和补液情况连同浓度保存，才能区分释放速度、累计释放量和剩余材料组成，而不让同一个mg/L数字承担三个不同结论。

## 样品让信号变暗时，内标和标准加入怎样工作

溶液中的其他成分统称为基体。酸度、盐含量、黏度和表面张力会影响雾化、液滴筛选和传输；进入等离子体后的组成变化还可能影响激发或电离。设想标准液中0.800 mg/L钙产生9600 a.u.背景扣除信号，而某个样品基体让整个传输效率降到80%，同样的钙只得到7680 a.u.。直接使用原来的外标斜率12000回算，就会读成0.640 mg/L。重复进样可以十分稳定地得到这个偏低结果，因此“重复得很好”和“量得准确”是两个需要分别检验的性质。

内标法给所有标准、空白和样品加入相同浓度的另一种元素，利用它的响应追踪共同变化。假设内标原本为5000 a.u.，样品中也同步降至4000 a.u.，两者都降为80%，目标信号除以内标信号时这个共同因子就会相消。适合的内标应在样品中原有含量足够低或得到妥善处理，所选谱线也要避开干扰，并在实际基体中验证其变化与目标元素足够一致。名称里有“内标”并不会自动使任何元素都成为合格的参照。

$$
c_{\mathrm{IS}}=\frac{S_A}{a}\frac{S_{I,\mathrm{ref}}}{S_I}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0c96901b8b2ce501d0ff987.svg) | 理想共同响应模型下的内标校正浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/fbfc0f565ed61fb4e844ec2b.svg) | 扣除相应背景和截距后的目标信号，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 标准条件下目标的校准斜率，a.u.每mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/39e7b1a43cfe84d51c42ad59.svg) | 样品中内标的净信号，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/562b42e43fdbcfd6045d461a.svg) | 相同加入浓度下，参考条件中内标的净信号，a.u. |

目标与内标都乘以同一个传输因子时，比值恢复该因子。7680/12000×5000/4000=0.800 mg/L；未经校正是0.640 mg/L。本式是已处理零点后的理想示例，实际可直接校准信号比值。目标特有的干扰和制样损失需分别检验。

![精确定义的教学模型。共同响应降至80%时，外标得到0.640 mg/L，理想内标校正得到0.800 mg/L。标准加入保持终体积和基体一致。检查液序列后四份另有目标元素特有的8%抑制，内标校正后仍为真实值的92%；消解后加标检验后续响应。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e0e756fdb3d1c56093c05d04.svg?v=e0e756fdb3d1)

图 4精确定义的教学模型。共同响应降至80%时，外标得到0.640 mg/L，理想内标校正得到0.800 mg/L。标准加入保持终体积和基体一致。检查液序列后四份另有目标元素特有的8%抑制，内标校正后仍为真实值的92%；消解后加标检验后续响应。

图中前十二份检查液只发生共同响应下降，内标比值能够追踪并校正。最后四份额外加入了目标元素独有的8%抑制，内标仍按原来方式变化，校正结果就停在真实值的92%。这能帮助判断校正的适用边界：它处理的是两条通道共同经历的乘性变化。某条谱线多出来的光、制样时未释放的元素、管壁上已经损失的目标物，都需要相应的证据和处理步骤。可在不同稀释倍数下比较结果，检查其他谱线，并把制样回收验证与进样响应验证分别安排。

标准加入法换了一种比较方式：从同一份未知液取等体积小份，在不同容器中加入不同已知量的目标元素，最后都补到相同总体积。这样，各瓶原样贡献相同，基体也尽量一致，只让加入的目标浓度改变。把信号对终体积中的新增浓度作图，向左延长至零信号的位置，就能估计这套终体积中原样贡献了多少。若每份原液又被最终配液稀释了一次，得到原液浓度时还要恢复这个已知倍数，不能把横截距直接当成最初消解液的浓度。

$$
S=q(c_x+c_{\mathrm{add}}),\qquad c_x=\frac{\beta}{q},\qquad c_{\mathrm{add},0}=-\frac{\beta}{q}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 扣除相应背景后的标准加入信号，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 该恒定样品基体中的响应斜率，a.u.每mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/9c54bbce30583a2aa825733e.svg) | 各瓶相同终体积中原样带来的浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/3f452a9afb83108541dff1a7.svg) | 各瓶终体积中新加入的已知浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 对新增浓度拟合的纵轴截距，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/edbf9de74fec745b1752934a.svg) | 拟合直线在零信号处的横轴截距，mg/L |

等体积原样、相同终体积、线性且共同基体响应，使斜率和原样贡献受到同一因子影响。q=9600、β=7680时cx=0.800 mg/L，横截距−0.800 mg/L。这个cx属于最终混合体积；恢复初始原液时再应用终体积与原样小份体积之比。未消除的加性谱线会改变β并偏移结果。

教学图让固定终体积中的原样贡献为0.800 mg/L，新增浓度为0、0.400、0.800和1.200 mg/L，样品基体把斜率压低至9600 a.u.每mg/L。拟合截距为7680 a.u.，截距除以斜率仍为0.800，因此横截距是−0.800 mg/L。计算成立的原因是同一个响应因子同时乘在原样和新加的元素上。若存在一条额外谱线或未处理的背景偏移，它会改变截距，却不以相同方式改变加标斜率；标准加入也会把这部分光错误计入原样。做标准加入之前，谱线与背景的检查依然是必要步骤。

加标回收可以把这种检验变得更直接。在同样的终体积基准上，样品原有0.800 mg/L，再加0.500 mg/L，理想读数增加0.500。若外标结果从0.640升到1.040，实际增加0.400，回收率就是80%。消解后加入的可溶标准检验了后续响应，却没有经历原始材料的分解；完整方法的回收还要通过合适的制样验证来评价。比较这些不同层次的检查，可以把“低了20%”进一步定位到光谱、进样、基体或制样环节，而不是只给结果乘一个经验修正数。

$$
R=\frac{c_{\mathrm{spiked}}-c_{\mathrm{native}}}{c_{\mathrm{added}}}\times100\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 加标回收率，% |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa442cea385f1c181f3e880.svg) | 加标样品测得浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/e6504e8fba3cf3faca91399c.svg) | 未加标样品在同一终体积基准上的测得浓度，mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/e077c72fdd39aab03ec09b0c.svg) | 按同一终体积计算的加入浓度，mg/L |

加标前后差值应等于加入量，因此取二者之比。外标结果1.040与0.640 mg/L，加入0.500 mg/L，得到80%；共同响应被正确校正时增量为0.500，得到100%。消解后加入的标准检验后续过程，原始材料释放过程另以适合证据评价。

## 小信号、参考材料与可信的误差范围

接近零浓度时，读数不会完全静止。检测器、背景估计和进样过程都会带来散布，因此要先问“零附近会波动多大”，再讨论一个小信号是否可以稳定识别。这里构造十次校准空白读数，用样本标准差描述信号噪声，再用校准斜率把信号单位换成浓度单位。若先把负的回算浓度全部改成零，会人为压窄这种散布；保留原始低端读数有助于正确估计噪声。这与最终结果表如何注明低于报告限的样品，是两个不同的数据处理阶段。

$$
s_B=\sqrt{\frac{\sum_{j=1}^{n}(B_j-\overline B)^2}{n-1}},\qquad c_{3s}=\frac{3s_B}{a},\qquad c_{10s}=\frac{10s_B}{a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f990247057bfe614e52c27c.svg) | 第j次校准空白信号，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/23c2accd18c3dd312fe92883.svg) | 这些空白信号的算术平均，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/a685ea95c60540ff028f8ac9.svg) | 观测编号和观测总数，无量纲；本例n=10 |
| ![Formula](https://ml-biomat.com/static/agent-math/284686c1a37c7859ac406591.svg) | 空白信号的样本标准差，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 校准斜率，a.u.每mg/L |
| ![Formula](https://ml-biomat.com/static/agent-math/65d71ecfdd9bf632552deabc.svg) | 三倍与十倍噪声对应的浓度尺度，mg/L |

离均差平方取平均再开方描述散布；离均差之和为零，只有n−1个可自由变化的量，因此分母用n−1。sB≈11.0629、a≈12002.666，得到0.00276511与0.00921703 mg/L。这是简化的仪器噪声换算，正式方法检出限与定量下限还需完整制样、多批空白和低浓度偏差/精密度验证。

本例空白信号标准差约11.063 a.u.，三倍标准差除以斜率得到约0.002765 mg/L，十倍则约0.009217 mg/L。这两个数描述当前简化噪声模型下的浓度尺度。完整方法的检出能力还要纳入制样污染、低浓度回收、不同批次和日期的变化；EPA的更新方法检出限程序把加标样品与方法空白的多批结果一起纳入。定量下限也需要用低浓度样品验证偏差和精密度。若最终进样液再稀释十倍，原样基准的低端能力也会变差，本例质量换算因子为2000 L/kg，不能只引用仪器溶液端的一个数字。

参考材料提供另一种检验。NIST SRM 1643f是一种含痕量元素的水参考材料，其证书列出了钙、镁、锶、锌等元素的认证值。这里选取四项真实证书数值重新绘图：钙29.430 mg/L、镁7.454 mg/L、锶0.314 mg/L、锌0.0744 mg/L。它们跨越不同浓度范围，一条固定的配液路线未必让所有元素都落在最佳测量区间。例如钙若使用本章0至2 mg/L的校准范围，就需要相应稀释；更稀的元素在同一倍数下则可能逼近低端，测量方案应按元素分别检查。

![依据NIST SRM 1643f证书质量浓度列原创绘图，μg/L除以1000换为mg/L。误差线为证书扩展不确定度，约95%覆盖，各元素覆盖因子在右图标明；不是本章采集的测量重复。左图采用对数横轴，右图显示扩展不确定度相对各自浓度的百分数。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/321f10d72f0cde11f18fe7c4.svg?v=321f10d72f0c)

图 5依据NIST SRM 1643f证书质量浓度列原创绘图，μg/L除以1000换为mg/L。误差线为证书扩展不确定度，约95%覆盖，各元素覆盖因子在右图标明；不是本章采集的测量重复。左图采用对数横轴，右图显示扩展不确定度相对各自浓度的百分数。

证书给出的误差范围也有明确含义。四项扩展不确定度分别为0.330、0.060、0.019和0.0017 mg/L，对应覆盖因子分别为2.1、2.0、2.2和2.1，覆盖概率约95%。它们综合了赋值和相关测量过程的信息，不能当作本章做了几次重复进样所得的标准差。图右把扩展不确定度除以相应浓度，得到相对大小，锶约为6.05%。这样既保留了不同元素的实际浓度差异，也能看出证书范围相对于各自数值有多宽；用一个统一百分比套在所有元素上会丢掉这些差别。

证书同时给出质量分数和质量浓度，两列的单位分别是每千克溶液和每升溶液，数值通过溶液密度关联。这里明确使用质量浓度列，并把μg/L除以1000换成mg/L。参考材料的用途也要和待测过程对应：水溶液参考材料很适合检验溶液测量与稀释过程，而材料完全消解是否成功，需要与样品基体和元素结合方式相适应的证据。将参考材料、独立检查液、方法空白、平行制样和加标安排在同一分析序列中，可以分别观察量值、污染、样品不均匀性和基体响应。

长序列中还要留意随时间的漂移。检查液在序列前、中、后的位置可以帮助判断一个变化来自样品还是仪器状态；高浓度样品之后的冲洗空白则有助于观察携带污染。发现检查液偏移后，回看受影响的时间段、谱线、内标和进样状态，再安排相应样品的复核。这样处理，最终的浓度就与一个有边界的实验序列相连。读者看到的不只是小数点后几位，而是这些位数分别得到哪些测量环节的支持。

## 亲手改变分辨率，再完成整个计算

下面的交互把真实浓度固定为0.800 mg/L，让你改变目标线与模拟邻峰的距离、观测半高全宽、邻峰强度，以及两种元素共同经历的基体响应。半高全宽是峰高一半处左右两点的间距，数值越大表示峰越宽。先保持其他条件不变，把峰间距逐渐减小，观察原始光谱、联合拟合、条件数和浓度估计如何一起变化。再恢复足够大的间距，单独把基体响应从1降到0.8，比较外标与内标结果，就能把光谱分离问题和共同传输问题分开体会。

## 交互实验：光谱分开了，浓度就一定准确吗？

已知钙浓度固定为0.800 mg/L，目标线的空气波长为317.9332 nm。先移动邻峰，再改变峰宽，比较光谱、残差和浓度估计；之后单独改变共同基体响应，观察外标和内标校正怎样分开。右下角误差线表示两倍模型标准误差，所有曲线使用同一组固定噪声。

[Figure: 联动的ICP光谱、拟合残差和三种浓度读数](https://ml-biomat.com/tutorials/experimental-methods/s08/#S08-plot)

| 读取方式 | 浓度 / mg L⁻¹ | 当前假设下处理了什么 |
| --- | --- | --- |
| 直接读取目标中心 |  | 已知背景已扣除；邻峰贡献仍在。 |
| 联合分峰后用外标 |  | 按已知峰形分离；基体响应仍会改变结果。 |
| 联合分峰并作内标校正 |  | 再消除两条通道完全共享的响应因子。 |

本实验的两个峰采用高斯线形，位置和宽度已知；背景为直线，逐点独立噪声标准差为20 a.u.。条件数针对去除常数及线性背景、再归一化后的两条峰形。两峰完全重合时，总曲线仍能拟合，单独的钙贡献却无法从这个窗口分离；此时停止显示各自浓度。内标通道在本模型中准确追踪共同响应，实际实验需要检验这种一致性。

界面给出的浓度误差尺度来自一个具体假设：两个峰的位置、宽度和线形已经正确给定，逐点噪声标准差为20 a.u.。显示的两倍模型标准误差用于比较条件变化，不包含真实实验中的谱线归属错误、错误背景形式或制样损失。当峰完全重合时，拟合总曲线仍可以很好看，但只有总峰贡献能够确定，界面会停止报告各自浓度。这个状态值得亲自试一次，因为它说明“图线贴得很好”和“问题的信息足够”有何区别。

完整Python例子从构造校准、生成光谱、联合拟合、残差检查开始，再做未知液回算、质量换算、标准加入和质量控制图，最后读取随例子附带的四元素证书数据绘图。随机数固定，因此重新运行会得到相同的观测与结果；中文和英文只改变文字，不改变数值。输出同时保留原始构造读数、拟合值和残差的表格，便于逐点核对。证书表与模拟观测分别保存，文件中的数据身份也保持明确。

### 完整例子：从光谱与校准到材料含量

离线运行，输出五幅对应语言图、校准/光谱/检查液/证书数值表和summary.json。光谱、校准与质控均为明确的教学构造；四元素表来自NIST证书质量浓度列。

```
"""ICP-OES: reproducible teaching models and actual NIST certificate values.

All spectra, calibration observations and QC sequences are constructed examples.
The four SRM rows are certified numerical facts, not measurements made here.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Ellipse, FancyArrowPatch

BLUE, GREEN, ORANGE, PURPLE = '#236d96', '#18877d', '#d57b39', '#8863a4'


def fixed_noise(n, seed=804):
    """Specified LCG + Box-Muller, shared exactly with the browser laboratory."""
    out = []
    while len(out) < n:
        seed = (1664525 * seed + 1013904223) & 0xffffffff
        u = (seed + .5) / 4294967296
        seed = (1664525 * seed + 1013904223) & 0xffffffff
        v = (seed + .5) / 4294967296
        out.extend([np.sqrt(-2*np.log(u))*np.cos(2*np.pi*v),
                    np.sqrt(-2*np.log(u))*np.sin(2*np.pi*v)])
    return np.array(out[:n])


def spectral_model(separation=.018, width=.014, interference=.6, matrix=.8):
    x = np.linspace(-.06, .06, 241)
    sigma = width / np.sqrt(8*np.log(2))
    g = np.exp(-.5*(x/sigma)**2)
    h = np.exp(-.5*((x-separation)/sigma)**2)
    baseline = 250 + 800*x
    y = baseline + matrix*12000*.8*(g+interference*h) + 20*fixed_noise(len(x))
    bg = np.column_stack([np.ones(len(x)), x])
    gp = g-bg@np.linalg.lstsq(bg, g, rcond=None)[0]
    hp = h-bg@np.linalg.lstsq(bg, h, rcond=None)[0]
    rho = float(gp@hp/np.sqrt((gp@gp)*(hp@hp)))
    identifiable = abs(rho) < 1-1e-12
    condition = np.sqrt((1+abs(rho))/(1-abs(rho))) if identifiable else None
    design = np.column_stack([g, h, np.ones(len(x)), x])
    if identifiable:
        coef = np.linalg.lstsq(design, y, rcond=None)[0]
        se = 20*np.sqrt(np.linalg.inv(design.T@design)[0, 0])/(12000*matrix)
        external, corrected = coef[0]/12000, coef[0]/(12000*matrix)
    else:
        combined = np.column_stack([g, np.ones(len(x)), x])
        c = np.linalg.lstsq(combined, y, rcond=None)[0]
        coef = np.array([c[0], 0, c[1], c[2]])
        external = corrected = se = None
    fit = design@coef
    return {'x':x, 'y':y, 'fit':fit, 'g':g, 'h':h, 'baseline':baseline,
            'coef':coef, 'identifiable':identifiable,
            'condition':float(condition) if identifiable else None,
            'external_mg_L':float(external) if identifiable else None,
            'corrected_mg_L':float(corrected) if identifiable else None,
            'standard_error_mg_L':float(se) if identifiable else None,
            'residual_rms':float(np.sqrt(np.mean((y-fit)**2))),
            'center_naive_mg_L':float((y[120]-baseline[120])/12000)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--language', choices=['zh','en'], default='en')
    args = parser.parse_args()
    out, lang = args.output, args.language
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],
                         'font.size':11, 'axes.spines.top':False,
                         'axes.spines.right':False, 'svg.fonttype':'none',
                         'axes.labelcolor':'#293c49','text.color':'#293c49',
                         'axes.titleweight':'bold','figure.facecolor':'#fffdf9'})
    def t(zh,en): return zh if lang=='zh' else en
    def save(fig,name):
        fig.savefig(out/f'{name}-{lang}.svg', bbox_inches='tight')
        fig.savefig(out/f'{name}-{lang}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
    def csvsave(name, header, rows):
        with (out/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.writer(f); w.writerow(header); w.writerows(rows)

    # 1: original historical/mechanistic drawing, not a copied historical apparatus.
    fig=plt.figure(figsize=(14,10),layout='constrained')
    gs=fig.add_gridspec(2,2,height_ratios=[1,1.7])
    ax=fig.add_subplot(gs[0,0]); ax.set(xlim=(0,10),ylim=(0,5)); ax.axis('off')
    ax.set_title(t('A  从火焰颜色到可分辨谱线','A  From flame colour to resolved lines'),loc='left')
    ax.add_patch(Polygon([[.8,1],[1.3,3.3],[1.8,1]],color=ORANGE,alpha=.8))
    ax.add_patch(Rectangle((.8,.6),1,.4,color='#8a949d'))
    ax.add_patch(Rectangle((3,.7),.15,1.18,color='#293c49'))
    ax.add_patch(Rectangle((3,2.12),.15,1.28,color='#293c49'))
    ax.add_patch(Polygon([[5,1],[5.7,3.2],[6.4,1]],facecolor='#cae8ec',edgecolor=BLUE))
    ax.plot([1.4,5.5],[2,2],color=ORANGE,lw=2)
    for yy,col in [(1.2,PURPLE),(2,GREEN),(2.8,ORANGE)]:
        ax.plot([5.5,8.6],[2,yy],color=col,lw=2); ax.plot([8.7,8.7],[yy-.2,yy+.2],color=col,lw=3)
    ax.text(.4,.1,t('火焰','Flame')); ax.text(2.5,.1,t('狭缝','Slit')); ax.text(5,.1,t('棱镜','Prism'))
    ax.text(.3,4,t('1860：基尔霍夫与本生的光谱分析','1860: Kirchhoff and Bunsen — spectral analysis'),fontsize=11)
    ax=fig.add_subplot(gs[0,1]); ax.set(xlim=(0,10),ylim=(0,5)); ax.axis('off')
    ax.set_title(t('B  1964年的问题：同样的钙，为什么变暗？','B  The 1964 question: why does calcium look dimmer?'),loc='left')
    for xpos,height,label in [(2,2.1,t('钙溶液','Calcium solution')),(6,1.1,t('钙 + 磷 / 铝','Calcium + P / Al'))]:
        ax.add_patch(Rectangle((xpos,.8),1,height,color=ORANGE,alpha=.7))
        ax.text(xpos+.5,.4,label,ha='center',fontsize=10)
    ax.text(.3,4,t('火焰中的化学干扰 → 探索高温感应等离子体','Chemical interference in flames → induction plasma'),fontsize=11)
    ax.text(.3,3.2,t('概念图；柱高不是历史测量数据','Conceptual illustration; bar heights are not historical data'),fontsize=10,color='#687782')
    ax=fig.add_subplot(gs[1,:]); ax.set(xlim=(0,16),ylim=(0,6)); ax.axis('off')
    ax.set_title(t('C  一滴样品怎样成为元素的光','C  How a droplet becomes elemental light'),loc='left')
    ax.add_patch(Rectangle((.35,1.4),1.15,1.4,facecolor='#ecf5f7',edgecolor=BLUE,lw=1.5))
    ax.add_patch(Rectangle((.38,1.43),1.09,.7,facecolor='#99d0dc',alpha=.7))
    ax.plot([.92,.92,2.0,2.0],[1.7,3.2,3.2,2.9],color=BLUE,lw=2)
    ax.text(.9,1.05,t('样品瓶','Sample'),ha='center')
    ax.add_patch(Polygon([[1.85,2.6],[2.7,2.8],[1.85,3]],facecolor='#bedae6',edgecolor=BLUE))
    ax.text(2.2,3.65,t('雾化器','Nebulizer'),ha='center')
    ax.annotate(t('氩气','Argon'),xy=(1.9,2.65),xytext=(1.6,2.05),arrowprops={'arrowstyle':'->','color':GREEN},fontsize=10)
    ax.add_patch(Polygon([[2.8,1.9],[3.4,1.6],[5.8,1.6],[6.3,2.2],[6.3,3.5],[3.2,3.5],[2.8,3.1]],facecolor='#eef5f7',edgecolor=BLUE,lw=1.5))
    ax.text(4.5,3.85,t('雾室：筛去大液滴','Spray chamber: remove large drops'),ha='center',fontsize=11)
    ax.scatter([3,3.3,3.5,3.8,4.1,4.5,5,5.5,5.9],[2.8,2.7,2.95,2.8,2.9,2.82,2.86,2.87,2.9],s=[30,20,12,8,6,5,4,4,3],color=BLUE)
    ax.scatter([3.4,4.2,4.6],[2.3,2.05,1.85],s=[45,70,55],color=BLUE,alpha=.65)
    ax.plot([4.6,4.6],[1.6,.95],color=BLUE,lw=2)
    ax.annotate('',xy=(4.6,.65),xytext=(4.6,1.3),arrowprops={'arrowstyle':'->','color':BLUE})
    ax.text(4.65,.35,t('大液滴与废液','Large drops / drain'),ha='center',fontsize=10)
    ax.plot([6.3,7.5],[2.9,2.9],color=BLUE,lw=3)
    for height,start,end in [(1.8,7.4,11.1),(1.25,7.6,10.5),(.45,7.4,10.0)]:
        ax.plot([start,end],[2.9-height/2]*2,color='#8dafbf',lw=2)
        ax.plot([start,end],[2.9+height/2]*2,color='#8dafbf',lw=2)
    for xcoil in [8.3,8.65,9,9.35]:
        ax.add_patch(Ellipse((xcoil,2.9),.28,2.1,facecolor='none',edgecolor=ORANGE,lw=2.8))
    ax.add_patch(Ellipse((10.5,2.9),2.4,1.05,facecolor=PURPLE,alpha=.22))
    ax.add_patch(Ellipse((10.3,2.9),1.8,.6,facecolor=ORANGE,alpha=.24))
    ax.annotate('',xy=(10.7,2.9),xytext=(6.6,2.9),arrowprops={'arrowstyle':'->','color':BLUE,'lw':1.8})
    ax.annotate('',xy=(9.8,3.62),xytext=(7.5,3.62),arrowprops={'arrowstyle':'->','color':GREEN,'lw':1.5})
    ax.text(7.7,4.25,t('石英同心炬管','Concentric quartz torch'),ha='center',fontsize=11)
    ax.text(8.8,1.35,t('外绕射频线圈','External RF coil'),ha='center',color=ORANGE,fontsize=11)
    ax.text(8.9,.85,t('中心：样品气溶胶','Centre: sample aerosol'),ha='center',fontsize=10)
    ax.text(10.8,1.65,t('氩等离子体','Argon plasma'),ha='center',fontsize=11)
    ax.annotate('',xy=(13.5,2.9),xytext=(11.7,2.9),arrowprops={'arrowstyle':'->','color':PURPLE,'lw':2})
    ax.text(12.8,2.45,t('轴向看光','Axial light'),ha='center',color=PURPLE,fontsize=10)
    ax.annotate('',xy=(10.8,4.75),xytext=(10.8,3.45),arrowprops={'arrowstyle':'->','color':GREEN,'lw':2})
    ax.text(11.05,4.05,t('径向看光','Radial light'),color=GREEN,fontsize=10)
    ax.plot([10.8,13.4],[4.75,4.75],color=GREEN,lw=1.5,ls='--')
    ax.plot([13.5,13.5],[2.9,4.75],color=PURPLE,lw=1.5,ls='--')
    ax.add_patch(Rectangle((13.5,4.15),2.2,1.2,facecolor='#f0edf5',edgecolor=PURPLE))
    ax.text(14.6,4.75,t('分光光学系统\n与检测器','Spectrometer\nand detector'),ha='center',va='center',fontsize=11)
    ax.text(.3,5.25,t('原理剖面示意；两条光路表示可选择的观察方向','Functional cross-section; two light paths represent alternative viewing directions'),fontsize=11)
    ax.text(12.5,.45,t('去溶剂 → 原子化 → 激发 / 电离','Desolvation → atoms → excitation / ionization'),ha='center',fontsize=10)
    save(fig,'light-path')

    # 2: spectral overlap and identifiability. Line centre is NIST air wavelength.
    sp=spectral_model()
    fig,axs=plt.subplots(2,2,figsize=(13,8.5),layout='constrained')
    ax=axs[0,0]; xx=317.9332+sp['x']
    ax.plot(xx,sp['y'],color='#86939c',lw=1,label=t('构造观测','Constructed observations'))
    ax.plot(xx,sp['fit'],color=BLUE,lw=2,label=t('联合拟合','Joint fit'))
    ax.set(title=t('A  两条谱线与背景','A  Two lines and a background'),ylabel=t('信号 / a.u.','Signal / a.u.'))
    ax.legend(fontsize=9);ax.ticklabel_format(useOffset=False,axis='x')
    ax=axs[1,0]
    ax.plot(xx,sp['coef'][0]*sp['g'],color=GREEN,label=t('Ca II 分量','Ca II component'))
    ax.plot(xx,sp['coef'][1]*sp['h'],color=ORANGE,label=t('模拟干扰峰','Constructed interference'))
    ax.plot(xx,sp['coef'][2]+sp['coef'][3]*sp['x'],color=PURPLE,label=t('拟合背景','Fitted background'))
    ax.set(xlabel=t('空气波长 / nm','Air wavelength / nm'),ylabel=t('信号 / a.u.','Signal / a.u.'),title=t('B  分开核对每一项','B  Inspect each contribution'))
    ax.legend(fontsize=9);ax.ticklabel_format(useOffset=False,axis='x')
    ax=axs[0,1];ax.plot(sp['x'],sp['y']-sp['fit'],color=BLUE,lw=1)
    ax.axhspan(-40,40,color=BLUE,alpha=.08);ax.axhline(0,color='#9eaaaf',lw=1)
    ax.set(xlabel=t('距钙线中心 / nm','Offset from calcium line / nm'),ylabel=t('观测 − 拟合 / a.u.','Observed − fitted / a.u.'),title=t('C  小残差仍需配合可辨识性','C  Small residuals need an identifiability check'))
    sep=np.linspace(.00015,.04,160)
    cond=np.array([spectral_model(separation=s)['condition'] for s in sep])
    ax=axs[1,1];ax.semilogy(sep/.014,cond,color=PURPLE,lw=2)
    ax.axvline(.018/.014,color=ORANGE,ls='--',label=t('当前示例','Current example'))
    ax.set(xlabel=t('峰间距 / 半高全宽','Separation / FWHM'),ylabel=t('投影后条件数 κ','Projected condition number κ'),title=t('D  靠近时噪声被放大','D  Approaching lines amplify noise'));ax.legend(fontsize=9)
    save(fig,'spectral-separation')
    csvsave('spectrum.csv',['air_wavelength_nm','constructed_signal','fitted_signal','residual'],zip(xx,sp['y'],sp['fit'],sp['y']-sp['fit']))

    # 3: calibrations and the complete solid-to-solution calculation.
    rng=np.random.default_rng(805)
    cx=np.repeat([0,.25,.5,1,2],3)
    cy=150+12000*cx+rng.normal(0,30,len(cx))
    slope,intercept=np.polyfit(cx,cy,1)
    uy=150+12000*.8+rng.normal(0,18,3)
    uc=(uy-intercept)/slope
    c=float(uc.mean()); mass=c*10*.05000/.0002500
    residual=cy-(slope*cx+intercept)
    blank=150+12*fixed_noise(10,808)
    sd=float(np.std(blank,ddof=1)); lod=3*sd/slope;loq=10*sd/slope
    fig=plt.figure(figsize=(13,8.6),layout='constrained');gs=fig.add_gridspec(2,2)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(cx,cy,color=BLUE,s=25)
    ax.plot([0,2],[intercept,intercept+2*slope],color=BLUE,lw=1)
    ax.scatter([c],[uy.mean()],color=ORANGE,s=70,zorder=4,label=t('未知液，三次进样均值','Unknown, mean of three injections'))
    ax.set(xlabel=t('标准浓度 / mg L⁻¹','Standard concentration / mg L⁻¹'),ylabel=t('净谱线信号 / a.u.','Net line signal / a.u.'),title=t('A  五个水平，各三次观测','A  Five levels, three observations each'));ax.legend(fontsize=9)
    ax=fig.add_subplot(gs[1,0]);ax.scatter(cx,residual,color=GREEN,s=25);ax.axhline(0,color='#85949c',lw=1)
    ax.set(xlabel=t('标准浓度 / mg L⁻¹','Standard concentration / mg L⁻¹'),ylabel=t('校准残差 / a.u.','Calibration residual / a.u.'),title=t('B  检查弯曲与低端散布','B  Look for curvature and low-end scatter'))
    ax=fig.add_subplot(gs[:,1]);ax.axis('off')
    steps=[t('干基复合材料 0.2500 g','Dry composite specimen: 0.2500 g'),t('完整消解，定容至 50.00 mL','Complete digestion; make to 50.00 mL'),t('消解液再稀释 10 倍','Dilute digest a further tenfold'),t(f'进样液测得 {c:.4f} mg/L',f'Measured solution: {c:.4f} mg/L'),t(f'样品总钙 {mass:.1f} mg/kg',f'Total Ca in specimen: {mass:.1f} mg/kg')]
    for j,label in enumerate(steps):
        y=.88-j*.18;ax.text(.5,y,label,ha='center',va='center',transform=ax.transAxes,fontsize=13,bbox={'boxstyle':'round,pad=.6','fc':'#e9f1f4','ec':'none'})
        if j<4: ax.annotate('',xy=(.5,y-.12),xytext=(.5,y-.05),xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':BLUE})
    ax.set_title(t('C  保存体积与质量，才能回到材料','C  Retain volumes and mass to return to the material'),loc='left')
    save(fig,'calibration-mass')
    csvsave('calibration.csv',['concentration_mg_L','constructed_signal','fitted_signal','residual'],zip(cx,cy,slope*cx+intercept,residual))
    csvsave('unknown.csv',['injection','constructed_signal','concentration_mg_L'],zip(range(1,4),uy,uc))

    # 4: matrix physics and QC. The values here are exact constructed relationships.
    added=np.array([0,.4,.8,1.2]); add_signal=.8*12000*(.8+added)
    add_slope,add_intercept=np.polyfit(added,add_signal,1)
    seq=np.arange(1,17);gain=1-.15*(seq-1)/15
    # Deliberate response mismatch in the last four solutions illustrates limits.
    target_response=gain.copy(); target_response[-4:]*=.92
    fig,axs=plt.subplots(2,2,figsize=(13,8.4),layout='constrained')
    ax=axs[0,0];labels=[t('真实','True'),t('外标','External'),t('内标比值','Internal ratio')]
    ax.bar(labels,[.8,.64,.8],color=[GREEN,ORANGE,BLUE]);ax.set(ylim=(0,1),ylabel=t('浓度 / mg L⁻¹','Concentration / mg L⁻¹'),title=t('A  两条通道共同降为 80%','A  Both channels fall to 80%'))
    ax=axs[0,1];ax.plot(added,add_signal,'o-',color=GREEN);ax.plot([-.8,0],[0,add_intercept],color=GREEN,ls='--');ax.axhline(0,color='#9da7ac',lw=1);ax.axvline(-.8,color=ORANGE,ls=':')
    ax.set(xlabel=t('终体积中加入的钙 / mg L⁻¹','Added calcium in final volume / mg L⁻¹'),ylabel=t('背景扣除信号 / a.u.','Background-corrected signal / a.u.'),title=t('B  标准加入：横截距 −0.800','B  Standard additions: intercept −0.800'))
    ax=axs[1,0];ax.plot(seq,target_response,'o-',color=ORANGE,label=t('外标','External'));ax.plot(seq,target_response/gain,'o-',color=BLUE,label=t('内标校正','Internal correction'));ax.axhline(1,color=GREEN,ls=':')
    ax.axvspan(12.5,16.5,color=PURPLE,alpha=.07);ax.set(xlabel=t('检查液顺序','Check solution sequence'),ylabel=t('测得浓度 / 已知浓度','Measured / known concentration'),ylim=(.7,1.05),title=t('C  最后四份：目标元素额外抑制 8%','C  Last four: extra 8% analyte suppression'));ax.legend(fontsize=9)
    ax=axs[1,1];ax.axis('off');ax.set_title(t('D  校正需要追踪同一种变化','D  Correction must track the same change'),loc='left')
    text=t('共同雾化 / 传输变化\n目标信号 ÷ 内标信号 → 可抵消\n\n额外谱线、消解损失、不同响应\n需要换线、验证制样或改变基体\n\n消解后加标：0.50 mg/L\n外标增量：0.40 mg/L → 回收率 80%',
           'Shared nebulization / transport change\nAnalyte ÷ internal signal → cancels\n\nExtra lines, digestion losses, unequal response\nChange line, validate preparation or matrix\n\nPost-digestion spike: 0.50 mg/L\nExternal increment: 0.40 mg/L → 80% recovery')
    ax.text(.03,.9,text,va='top',linespacing=1.7,fontsize=12,transform=ax.transAxes)
    save(fig,'matrix-quality')
    csvsave('standard_additions.csv',['added_mg_L','constructed_signal'],zip(added,add_signal))
    csvsave('quality_control.csv',['sequence','shared_gain','external_ratio','internal_corrected_ratio'],zip(seq,gain,target_response,target_response/gain))

    # 5: actual NIST certificate values, with element-specific expanded uncertainty.
    with (Path(__file__).parent/'data'/'srm1643f.csv').open(encoding='utf-8') as f:
        cert=list(csv.DictReader(f))
    names=[r['element'] for r in cert]
    values=np.array([float(r['concentration_ug_L'])/1000 for r in cert])
    uncertainty=np.array([float(r['expanded_uncertainty_ug_L'])/1000 for r in cert])
    factors=np.array([float(r['coverage_factor']) for r in cert])
    fig,axs=plt.subplots(1,2,figsize=(13,5.5),layout='constrained');yp=np.arange(4)
    ax=axs[0];ax.errorbar(values,yp,xerr=uncertainty,fmt='o',color=BLUE,capsize=5,ms=7)
    ax.set(xscale='log',yticks=yp,yticklabels=names,xlabel=t('认证质量浓度 / mg L⁻¹（对数轴）','Certified mass concentration / mg L⁻¹ (log scale)'),title=t('A  NIST SRM 1643f 的四个元素','A  Four elements in NIST SRM 1643f'))
    ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
    ax=axs[1];ax.barh(yp,100*uncertainty/values,color=[BLUE,GREEN,PURPLE,ORANGE]);ax.set(yticks=yp,yticklabels=names,xlabel=t('相对扩展不确定度 / %','Relative expanded uncertainty / %'),title=t('B  误差线各有自己的覆盖因子','B  Each interval has its own coverage factor'));ax.invert_yaxis()
    for i,(u,v,k) in enumerate(zip(uncertainty,values,factors)):
        ax.text(100*u/v+.1,i,f'{100*u/v:.2f}%   k={k:.1f}',va='center',fontsize=10)
    ax.set_xlim(0,8.5)
    fig.suptitle(t('证书值与约 95% 扩展不确定度；不是本例的实测重复','Certificate values and ≈95% expanded uncertainty; not replicate measurements in this example'),fontsize=12)
    save(fig,'certified-reference')
    csvsave('certificate_mg_L.csv',['element','concentration_mg_L','expanded_uncertainty_mg_L','k'],zip(names,values,uncertainty,factors))
    summary={'photon_400nm_eV':6.62607015e-34*299792458/(400e-9)/1.602176634e-19,
             'ideal_mass_mg_kg':.8*10*.05000/.0002500,
             'calibration':{'slope':float(slope),'intercept':float(intercept)},
             'unknown_mg_L':c,'sample_Ca_mg_kg':mass,
             'blank_signal_sd':sd,'noise_scale_3s_mg_L':lod,'noise_scale_10s_mg_L':loq,
             'standard_addition_native_mg_L':float(add_intercept/add_slope),
             'post_digest_external_recovery_percent':(.8*1.3-.8*.8)/.5*100,
             'shared_matrix_external_mg_L':.64,'shared_matrix_internal_mg_L':.8,
             'certificate_Ca_mg_L':float(values[0]),'certificate_Sr_relative_U_percent':float(100*uncertainty[2]/values[2]),
             'spectral_default':{k:v for k,v in sp.items() if not isinstance(v,np.ndarray)},
             'model_labels':{'calibration':'constructed','spectra':'constructed','quality_control':'constructed','certificate':'NIST certified facts'}}
    assert abs(summary['ideal_mass_mg_kg']-1600)<1e-9
    assert abs(summary['standard_addition_native_mg_L']-.8)<1e-12
    assert abs(summary['post_digest_external_recovery_percent']-80)<1e-10
    assert spectral_model(separation=0)['identifiable'] is False
    assert .78<c<.82 and 1500<mass<1700
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
```

把例子用于自己的实验时，首先替换已知浓度与实际观测，并检查信号究竟是峰高、积分面积还是仪器已处理过的浓度。随后确认背景和截距各处理一次，写入实际称样量、定容体积和所有稀释步骤，再用独立检查液与适合的回收证据评价结果。若两条可用谱线给出的浓度不一致，优先查看完整光谱窗口、背景位置、稀释一致性和样品基体。这样的分析过程能够把一杯液体中的光，稳妥地连接到材料研究真正关心的元素量、释放行为和组成变化。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [EPA SW-846 Method 6010D, Revision 5 (2018)](https://www.epa.gov/sites/default/files/2015-12/documents/6010d.pdf)

   理解雾化、光谱背景、基体干扰、方法空白和质量控制。
2. [EPA Method 200.7, Revision 4.4](https://www.epa.gov/sites/default/files/2015-08/documents/method_200-7_rev_4-4_1994.pdf)

   操作定义下的溶解态、总可回收元素与标准加入条件。
3. [Kirchhoff and Bunsen (1860): Chemical Analysis by Observation of Spectra](https://www.chemteam.info/Chem-History/Kirchhoff-Bunsen-1860.html)

   原文英文节选中的狭缝、棱镜与元素特征谱线。

   Historical technical reference; no web image or extended quotation reused.
4. [Greenfield, Jones and Berry (1964), Analyst 89, 713–720](https://masspec.scripps.edu/learn/ms/pdf/1964_GreenfieldS.pdf)

   钙发射的磷/铝抑制问题与高频感应等离子体的早期研究。

   Historical article hosted by an institutional repository; cited as a technical reference. Chapter diagrams are original.
5. [NIST Handbook: Strong Lines of Calcium](https://physics.nist.gov/PhysRefData/Handbook/Tables/calciumtable2.htm)

   核对Ca I和Ca II的空气波长，区分线位置与浓度校准。

   Three factual wavelength entries cited; no database compilation or figure reproduced.
6. [NIST SRM 1643f: Trace Elements in Water, Certificate](https://tsapps.nist.gov/srmext/certificates/1643f.pdf)

   四元素真实质量浓度、扩展不确定度、覆盖因子和浓度/质量分数区别。

   Four non-SRD certificate facts transcribed with attribution under NIST non-SRD data policy; original replot; μg/L converted to mg/L.
7. [EPA: Method Detection Limit Procedure, Revision 2](https://www.epa.gov/sites/default/files/2016-12/documents/mdl-procedure_rev2_12-13-2016.pdf)

   方法检出限如何纳入完整制样、加标与方法空白的多批变化。
8. [NIST: Copyright, Fair Use and Licensing Statements](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)

   认证数值再绘的署名、修改说明与非SRD数据使用条款。

   Rights reference; non-SRD terms are not generalized to all SRD databases.
