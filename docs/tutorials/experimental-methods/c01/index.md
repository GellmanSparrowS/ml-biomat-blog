# 高效液相色谱：让混合物按时间分开

Source: https://ml-biomat.com/tutorials/experimental-methods/c01/
Language: zh-CN

把混合物分成可辨认的时间信号，再把峰面积变成有明确实验含义的浓度与质量。

## 一杯咖啡里，怎样只数咖啡因

咖啡有颜色、有气味，也含有许多溶解在水中的物质。若直接测它对紫外光的吸收，仪器接收到的是多种成分共同作用的结果；我们真正想知道的咖啡因，只占其中一部分。类似的问题也出现在材料研究中：一块聚合物泡过的水里，可能同时有释放的药物、残余小分子和降解产物；细胞培养液里则有营养物、代谢物和添加剂。要准确量出某一种物质，常常先要让它与其他物质分开，再安排合适的检测。

高效液相色谱，简称 HPLC，采用的办法是让混合物通过一根装有特殊填料的柱子。液体不断向前流，不同分子与填料接触、停留和离开的平均时间不同，原来一起进入的物质便陆续到达出口。检测器在那里连续记录信号，得到一张“谁在什么时候出来、出来了多少”的图。横轴是进样后的时间，纵轴是某种检测响应，例如紫外吸光度。色谱的核心是分离，检测器负责把经过它的物质转成可读信号，两者合作才形成完整分析。

可以想象一群人从同一地点穿过街区。有些人一路走过，有些人反复在商店停留，走到终点的时间便不同。色谱中的分子并没有目的，也不会主动选择商店；它们不断热运动，在流动液体和固定环境之间交换，停留概率取决于相互作用。这个区别十分重要：一次进入色谱柱的同一种分子并非整齐的一队，个体经历略有差别，到达时间会分散成一个峰。分离既要让不同成分平均到达时间不同，也要把每一组的时间分散控制得足够小。

本章沿着一次定量实验展开：先理解柱内发生什么，再决定如何使目标峰与邻居分开，随后把峰面积换成浓度，最后把浓度放回原来的研究问题。咖啡因是容易想象的对象，程序采用明确构造的数据来展示计算；同一条思路也适用于合成反应中的残余单体、材料浸提液中的添加剂，以及载药材料的释放实验。方法是否适合，首先取决于目标物能否在所选液体中稳定存在、能否得到合适分离，以及检测器对它是否有可用响应。

## 分子的一点偏好，怎样变成分钟级的差别

色谱中不断移动的液体称为流动相，留在柱内并与分子发生相互作用的环境称为固定相。固定相可以是颗粒表面的化学基团，也可以包含被固定的液相环境。一个分子在流动相中时容易随液体向前，在固定相附近停留时平均前进速度较低。这样的交换沿整根柱子反复发生，很小的分配差异便能积累为可测的时间差。决定效果的是两种环境怎样分别对待不同分子，而不是把柱子想成只按颗粒大小筛分的滤网。

这种把反复分配变成分离的思想，也解释了色谱的发展。马丁在 1952 年诺贝尔演讲中回顾，分配色谱把色谱与逆流萃取的思路连接起来。马丁和辛格的工作与蛋白质组成分析的需要相连：复杂混合物需要被分解成能够分别测量的组分。图中的柱内示意用两条分子带表示这种累计差异，现代仪器则用稳定泵送、精细填料和连续检测，让分配过程产生可重复的时间记录。科学问题推动了分离方法，分离能力又让更复杂的化学与生物问题变得可研究。

常见的反相色谱采用相对疏水的固定相，例如带有十八碳烷基链的 C18 表面，流动相通常含水与可混溶的有机溶剂。许多较疏水的分子在这样的条件下停留较久；提高有机相比例，常能使它们更容易被洗脱出来。这里的“较久”是相对于同一组条件说的。分子的电荷、氢键、芳香结构和固定相表面细节都会影响结果，两种同为 C18 的柱子也可能表现出不同选择性。目标物若非常亲水、带电或属于大分子，还可以考虑亲水作用、离子交换、体积排阻等分离机制。

电荷状态是一个值得先建立的基础。某些分子可以接受或释放质子，溶液酸碱度改变时，带电与不带电形式的比例也会改变。带电形式与水、固定相的作用往往不同，于是保留时间随 pH 改变。缓冲液用于让酸碱度保持在设定范围，浓度与盐种也参与分离。选择条件时，要同时考虑分子稳定性、固定相可承受的条件以及后续检测器的兼容性。例如连接质谱时，流动相中的不挥发盐与单纯紫外检测时具有不同的操作后果。

![原创柱内分配与现代液路示意。两条色带表示不同平均保留，连接马丁与辛格分配色谱发展的核心思想。右图把驱动液流、加入样品、分离和检测放在真实流向中；不按设备尺寸绘制。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d8de0e5b1d13ee0a55eefc06.svg?v=d8de0e5b1d13)

图 1原创柱内分配与现代液路示意。两条色带表示不同平均保留，连接马丁与辛格分配色谱发展的核心思想。右图把驱动液流、加入样品、分离和检测放在真实流向中；不按设备尺寸绘制。

现代 HPLC 的液路可以顺着流向读：溶剂经过脱气、混合与泵送，进样阀把一定体积样品加入流动相，样品经过柱子后到达检测器，再流向收集或废液位置。泵提供推动液体穿过细颗粒床所需的压力；压力本身并不是区分分子的原因。更小颗粒能够缩短某些传质路径，但也会增加流动阻力。把泵、柱子和检测器看作各司其职的部件，能够避免一个常见误解：换成更高压力的设备，并不会自动让两个相互作用几乎一样的分子分开。

## 峰在哪里，和峰有多宽一样重要

保留时间是从进样到目标峰最大值的时间。它包含分子随流动相通过系统的时间，以及由于保留而增加的时间。用一种在所选条件下基本不被保留、又能适当检测的标记，可以估计死时间或空隙时间 t₀。把目标的保留时间减去 t₀，再除以 t₀，得到保留因子 k。这样就把单纯“过柱需要多久”与“额外停留了多少”区分开。实际标记和测量位置需要与所研究的柱体积对应，最先出现的任意小峰并不天然就是可靠的死时间标记。

$$
k=\frac{t_R-t_0}{t_0},\qquad t_R=t_0(1+k)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 等度条件下的保留因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0dfa193aee7778fd0c1a71af.svg) | 目标峰保留时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a15f4e949d9181049b209fc5.svg) | 合适未保留标记的空隙时间，min。 |

把额外保留时间按未保留流动时间归一化。tR=4 min、t₀=1 min，得到 k=3。梯度中流动相改变，保留不能由一个恒定 k 完整描述。

若 t₀=1 min，一种物质在 4 min 到达，则 k=3。它的总时间相当于未保留流动时间的四倍，其中三倍是与保留有关的额外时间。第二种物质若 k=3.36，则在 4.36 min 到达，两个 k 的比值为 1.12，称为这对组分的选择性。选择性描述固定相和流动相区分两个成分的程度。若二者的 k 完全相同，延长等待只能让它们一起更晚出现；改变能区分二者的相互作用，才会产生新的平均时间差。

同一种分子的到达时间会分散，因为它们走过的流路、扩散经历和固定相交换过程不同。色谱峰因而有宽度。两个峰中心相差 0.3 min，若各自非常窄，可以分得清；若各宽 1 min，就会明显叠在一起。分离度把中心间隔与峰宽放进同一个比例，比较的是“间隔相对于散开程度有多大”。计算时先说明使用基线宽度还是半高宽度，两套公式的系数不同，不能混用。

$$
R_s=\frac{2(t_{R,2}-t_{R,1})}{w_1+w_2},\qquad \alpha=\frac{k_2}{k_1}\quad(k_2\geq k_1>0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c29ea71c312c1c2bf08acd27.svg) | 两峰分离度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/43bdb088cbae6d3907fc9e8b.svg) | 较早与较晚峰的保留时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8959dc68ce37371df41f244e.svg) | 两峰的基线宽度，min；本章高斯模型采用 4σ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 选择性，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d62ad609310d0b90a08f3cae.svg) | 两组分等度保留因子，无量纲。 |

中心间隔相对平均基线宽度衡量分开程度。tR=4 与 4.36 min、w=0.32 与 0.3488 min，Rs≈1.07656；k=3 与 3.36，α=1.12。峰拖尾或面积差异明显时还需检查具体积分干扰。

理论塔板数 N 是描述峰相对宽窄的常用量。它不是柱子里真的有几千块隔板，而是从分离理论发展出来的效率尺度。对于近似高斯的峰，保留时间除以标准差，再平方，得到 N。高斯峰在平均值两边逐渐降低，标准差描述这一时间分布的宽度。若保留时间相同而峰宽减半，N 会变成四倍。对应的分离度在其他条件相同下大约提高两倍，因此追求柱效会有收益，但它与改变化学选择性是不同的改进方向。

$$
N=\left(\frac{t_R}{\sigma_t}\right)^2=16\left(\frac{t_R}{w}\right)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 理论塔板数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0dfa193aee7778fd0c1a71af.svg) | 保留时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/87de164e10556b3dda44460d.svg) | 高斯到达时间分布的标准差，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 高斯峰基线宽度，取 4σt，min。 |

在近似高斯、适当等度条件下，以峰宽相对于时间尺度描述效率。tR=4 min、σt=0.08 min 得 N=2500；宽度减半而时间不变时 N=10000。真实系统的额外展宽也会进入观察到的峰宽。

![构造等度高斯峰，每个分量面积为 1，t₀=1 min、k₁=3。A 与 B 只改变 N，A 与 C 只改变选择性。分离度采用基线宽度 4σ；热图白线为 Rs=1.5。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/de307cbaaf8878785ad258e2.svg?v=de307cbaaf88)

图 2构造等度高斯峰，每个分量面积为 1，t₀=1 min、k₁=3。A 与 B 只改变 N，A 与 C 只改变选择性。分离度采用基线宽度 4σ；热图白线为 Rs=1.5。

图中三个色谱图把两条路线并排比较。第一种条件采用 N=2500、选择性 1.12；第二种只把 N 提高到 10000，峰中心不变而变窄；第三种保持 N=2500，把选择性提高到 1.30，两个峰中心拉开。热图把这些组合扩展成连续范围，白线表示模型中的分离度 1.5。对于面积相近、近似对称的高斯峰，这常对应良好分离；若一个峰比另一个大很多，或者明显拖尾，能否可靠积分还要直接检查小峰受到的干扰。

流速也影响峰宽。流得很慢时，分子有较长时间沿柱方向扩散；流得很快时，在不同环境之间交换可能跟不上整体流动。不同路径造成的分散也同时存在，因此效率与流速之间通常有一个有利范围。把流速加倍，保留时间往往缩短，但峰宽、压力和检测采样也随之改变，结果未必是分离度提高。交互图选择独立改变柱效与选择性，让这两个概念先变得清楚；真实方法开发再把它们连接到柱长、颗粒、溶剂、pH 和温度等可操作条件。

## 让峰变窄，还是让峰离远一些

固定第一组分 k=3，比较柱效、选择性与时间尺度。空隙时间在此只缩放整个模型，不预测真实流速对柱效的影响。

[Figure: 两组分色谱交互图](https://ml-biomat.com/tutorials/experimental-methods/c01/#C01-plot)

## 让样品以合适的状态进入柱子

色谱图从进样开始，样品的定量故事却更早开始。取样是否均匀，目标物是否完全溶解，是否吸附在容器或滤膜上，保存期间是否氧化或分解，都会改变最后进入仪器的量。浑浊样品通常需要适当澄清，以减少颗粒进入细小液路；所选离心、过滤或萃取步骤又必须与目标物性质匹配。例如，一个疏水小分子可能留在过滤材料上，一种药物可能随沉淀蛋白一起损失。前处理既要保护分离系统，也要把目标物带到一个可追踪的溶液中。

样品溶剂与初始流动相的关系同样影响峰形。若进样液在反相条件下具有很强的洗脱能力，而且体积较大，目标物可能在柱头尚未形成窄带便向前移动，出现展宽、分裂或前伸。把浓度提高而保持较小进样体积，与把稀溶液大量注入柱子，并不总是等效。样品量过大还可能超过固定相的线性容量，导致保留和峰形随浓度改变。用不同进样量检查峰位、形状和面积是否按预期变化，可以判断定量是否处在合适区间。

等度洗脱在一次运行中保持流动相组成不变，适合保留范围不太宽的样品，也便于建立直观的 k 与 N 关系。梯度洗脱则逐渐改变溶剂组成，例如在反相色谱中增加有机相比例，让较强保留的成分随后出来。梯度中同一分子的保留能力随时间变化，不能把它当成始终具有一个固定 k 的等度实验。梯度结束后，柱子还需要回到初始组成并充分平衡，下一次进样才有可比起点。

泵开始改变比例，不等于柱入口立即收到新溶剂。混合器、管路和进样系统之间存在体积，新组成需要随流动通过这些空间。若梯度延迟体积为 0.75 mL、流速为 0.50 mL/min，到达延迟就是 1.5 min。两台仪器运行相同的泵程序，却可能把不同时间的梯度送到柱头，因此方法转移需要比较实际梯度到达和系统体积。图中的两条梯度曲线保留相同斜率，只改变到达时间，帮助把这个问题与柱内分离区分开。

检测器必须对目标物有合适响应。紫外检测适合能在所选波长吸收的物质，二极管阵列检测器可以同时记录一段波长范围；荧光检测适合天然发光或经过合适标记的目标。示差折光等检测方式可用于一些缺少强紫外吸收的物质，但对流动相变化有不同要求。连接质谱可以增加质量与碎片信息。选择一个方便的波长不是定量的终点：还要确认溶剂背景、目标响应、邻近杂质和实际浓度是否支持所需灵敏度。

## 从一个峰，到原样里有多少物质

确定目标峰时，先在相同条件下测量已知标准物，比较保留时间。向样品中加入少量标准物，观察对应峰如何增加，也能帮助定位。若两个不同物质恰好一起流出，它们会形成共洗脱，检测器可能只给出一个外观整齐的峰。比较峰前、峰顶与峰后的光谱，改变分离条件，或增加质谱信息，都是进一步判断的办法。保留时间提供条件依赖的身份线索，多个彼此协调的观测会使归属更扎实。

峰面积需要先确定基线，也就是目标物没有经过时检测器应有的信号。若基线缓慢漂移，可以用目标峰附近、没有其他成分的时间段估计背景，再对目标区域积分。积分窗口太窄会丢失峰两侧的信号，太宽则可能把邻峰和基线误差算进去。图中的窗口变化实验显示，窄窗口虽然把最高的部分包住了，仍会遗漏相当多的面积。对于拖尾峰和重叠峰，积分规则应提前确定并对同批样品一致使用，再检查规则是否在所有浓度下都合适。

外标法为同一种目标物配制一系列已知浓度，在相同进样量和检测条件下测峰面积，建立浓度与响应关系。程序采用六个浓度水平、每个水平三个构造重复值，拟合线性校准。斜率表示每增加一个浓度单位，面积平均增加多少；截距记录零浓度附近的偏置。是否保留截距、是否加权，应由空白、误差结构和残差共同判断，不能只为了让直线穿过原点而强制截距为零。样品最好落在已经验证的校准范围内，过高时进行准确稀释后再测。

$$
A=mc+b,\qquad c_{\mathrm{original}}=D\frac{A_{\mathrm{unknown}}-b}{m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/88c650b4e9eb956a41e222a9.svg) | 校准或未知样目标峰面积，mAU·min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 校准斜率，(mAU·min)/(μg/mL)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 仪器瓶内目标浓度，μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 校准截距，mAU·min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 原样至进样溶液的总体稀释因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994c7009d659d06ee37650ec.svg) | 原始溶液浓度，μg/mL。 |

在验证的线性范围内先反演进样浓度，再乘稀释因子。m=6、b=0.8、A=78.8、D=4 时，进样浓度 13 μg/mL，原液浓度 52 μg/mL。程序由带噪声校准与真实积分计算邻近结果。

![固定随机种子的构造定量实验。未知样真实浓度 13 μg/mL，校准每个水平三个重复。填色为指定目标峰积分区域；残差为校准面积减拟合面积。右下图比较不同窗口回收的目标面积比例，揭示峰翼的贡献。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5411acd08951789e92f3eb24.svg?v=5411acd08951)

图 3固定随机种子的构造定量实验。未知样真实浓度 13 μg/mL，校准每个水平三个重复。填色为指定目标峰积分区域；残差为校准面积减拟合面积。右下图比较不同窗口回收的目标面积比例，揭示峰翼的贡献。

教学数据把真实关系设为面积约等于 6 倍浓度再加 0.8，浓度单位为 μg/mL，面积单位为 mAU·min；mAU 是千分之一吸光度单位。未知样的目标峰来自 13 μg/mL 的构造溶液，积分和校准会得到接近这个值的结果。如果这是原样经过四倍稀释后的溶液，原样浓度约为 52 μg/mL。这里的“四倍”是最终体积除以取用原样体积，而不是额外加入液体的体积比。把一次取样、定容与进一步稀释逐项串起来，才能把仪器瓶里的浓度正确换回研究对象。

若需要报告一块材料中的含量，还要继续乘以提取液体积，再除以被提取材料的质量。例如某溶液对应原始提取液浓度 52 μg/mL，提取液总体积为 10 mL，目标物总量就是 520 μg；若来自 0.20 g 材料，则为 2600 μg/g，也就是 2.6 mg/g。每一步单位都能相互抵消或保留下来，因此单位检查也是推理检查。对于多个峰的样品，某个峰占总面积的 90% 只是该检测条件下的面积比例；不同物质响应不同，不能直接把它当成质量纯度。

内标法是在标准与样品中加入已知量的另一种合适物质，用目标峰面积与内标峰面积之比建立校准。当进样体积整体偏大或偏小时，两者信号一起变化，比例可以减少这类误差。内标应稳定、原样中没有或可区分，并与目标及杂质分开。若想跟踪萃取损失，还必须在相关前处理步骤之前加入，而且它与目标物的回收行为需要匹配；在萃取结束后才加入，只能帮助之后的步骤。加标回收则直接加入已知目标物，比较测得增加量与加入量，是另一个问题，二者的名称和目的应区分清楚。

## 一条漂亮的直线，还需要哪些搭档

校准线很直，说明这些标准点在所测范围内与所用模型相符。原样经过提取后有没有损失、目标峰是否共洗脱、样品在自动进样器里是否降解，则需要其他证据。把质量检查放到各个步骤，会比只看一个相关系数更有效：溶剂空白观察系统背景，处理空白检查器皿与试剂，较高浓度样品之后的空白检查残留带入，独立配制的检查样检验校准后的测量表现。它们各自回答不同问题，出现变化时也便于定位。

回收率是一个直观的前处理检查。对两份可比样品，一份保持原样，另一份在提取前加入已知目标物，两者测得量之差再除以加入量，得到这次加标对应的回收比例。假如加进去 10 μg，最后只比原样多测到 8.5 μg，回收率为 85%。这个数字说明在所测浓度、基质与处理条件下，增加的目标物有多少成为可测信号。改变容器、萃取条件或过滤材料后重复比较，可以把损失转化成具体可改进的步骤。

$$
\mathrm{Recovery}=\frac{q_{\mathrm{spiked}}-q_{\mathrm{unspiked}}}{q_{\mathrm{added}}}\times100\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/da2911810e849da2f484a127.svg) | 加标回收百分比，%。 |
| ![Formula](https://ml-biomat.com/static/agent-math/340607043a312e60188e2839.svg) | 加标样测得目标物量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/17a361682607930130ab2ca5.svg) | 对应未加标样测得量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2ed64c2d28a6fe11e9f25433.svg) | 相关处理前已知加入量，μg。 |

相减去掉原有目标物，再比较新增信号与已知加入量。多测到 8.5 μg、加入 10 μg，回收率 85%。样品和终体积需可比，并明确加标发生在什么步骤。

精密度与回收率应一起理解。三次结果都接近 85%，说明损失比较稳定；三次分别为 60%、85%、105%，则提示过程波动或干扰需要处理。稳定偏差与随机波动对研究有不同影响。若原样中的目标物被包在复杂材料内部，外加标准物也未必经历完全相同的释放或结合过程，可以进一步安排不同加入时点、不同提取次数或合适参考材料，把校正策略建立在与原样更接近的行为上。

程序中的校准残差图保留每个重复值与拟合线的差，而不是只给出一条线。若低浓度点在一侧、高浓度点在另一侧，可能需要检查线性范围或模型形式；若误差随浓度增长，可能需要研究加权拟合。对一批真实样品，还可以把保留时间、检查样浓度和压力随进样顺序画出来，寻找渐变或突变。这样的图常能区分柱子状态逐步改变、溶剂问题和某一次进样异常，让分析回到可解释的实验过程。

正式测量前，可以用标准混合物检查关键峰对的分离、保留行为和面积重复性。检查对象应围绕任务确定：主成分旁边的微量杂质，与两种含量接近的成分，需要的分离表现并不一样。检查结果改变时，依次比较溶剂配制、漏液、温度、柱状态与进样设置；一次改变多个条件，可能得到更漂亮的图，却难以理解改善来自哪里。把空白、标准、检查样、未知样和定期检查排成合理序列，便能把整批测量组织成连贯比较。还要区分同一瓶反复进样、独立前处理和独立试样，它们分别检验不同层次的重复性。

### 完整分离、积分、校准与取样质量平衡

固定随机种子生成明确标记的教学数据，保存所有图、校准重复值、未知色谱图和释放取样表。

```
"""Reproducible constructed HPLC separation, calibration and sampling examples."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','text.color':'#243c49','axes.labelcolor':'#243c49','axes.edgecolor':'#8ea1a8','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','svg.fonttype':'path'})
 blue,green,red,gold='#286488','#008b7b','#dc604d','#c39227';rng=np.random.default_rng(610)
 def save(fig,n):
  fig.tight_layout(pad=1.6)
  for ext in ['svg','png']:fig.savefig(out/f'{n}-{a.language}.{ext}',dpi=155,bbox_inches='tight')
  plt.close(fig)
 def g(t,mu,s):return np.exp(-.5*((t-mu)/s)**2)/(s*np.sqrt(2*np.pi))
 fig,ax=plt.subplots(1,2,figsize=(13,5),gridspec_kw={'width_ratios':[1,1.55]});x=ax[0];x.set(xlim=(0,10),ylim=(0,10));x.axis('off')
 x.add_patch(Rectangle((3,1.1),3,7.7,fill=False,lw=2,color=blue))
 for yy in np.arange(1.6,8.6,.55):
  for xx in [3.45,4.25,5.05,5.65]:x.add_patch(Circle((xx,yy),.13,color='#b9c9cb'))
 for yy,c,label in [(6.5,gold,T('停留较久','More retained')),(3.1,green,T('前进较快','Faster migration'))]:x.add_patch(Rectangle((3.1,yy),2.8,.55,color=c,alpha=.65));x.text(6.4,yy+.27,label,va='center',fontsize=10)
 x.annotate('',xy=(4.5,9),xytext=(4.5,10),arrowprops={'arrowstyle':'->','color':blue,'lw':2});x.annotate('',xy=(4.5,.15),xytext=(4.5,1),arrowprops={'arrowstyle':'->','color':blue,'lw':2});x.text(.1,.15,T('流动相不断向下移动','Mobile phase keeps moving'),fontsize=10);x.set_title(T('A  分配差异累积为分离','A  Repeated partition creates separation'),loc='left')
 x=ax[1];x.set(xlim=(0,14),ylim=(0,10));x.axis('off');items=[(.3,6.5,2,1.4,T('溶剂瓶','Solvents')), (3.3,6.5,2,1.4,T('泵与混合','Pump / mix')), (6.3,6.5,2,1.4,T('定量进样','Injection')), (6.3,2.8,2,1.4,T('色谱柱','Column')), (10,2.8,2.7,1.4,T('检测器','Detector'))]
 for xx,yy,w,h,label in items:x.add_patch(Rectangle((xx,yy),w,h,facecolor='#e6eeee',edgecolor=blue,lw=1.7));x.text(xx+w/2,yy+h/2,label,ha='center',va='center')
 for start,end in [((2.3,7.2),(3.3,7.2)),((5.3,7.2),(6.3,7.2)),((7.3,6.5),(7.3,4.2)),((8.3,3.5),(10,3.5)),((12.7,3.5),(13.7,3.5))]:x.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=14,color=green,lw=2))
 x.text(10,1.2,T('固定波长下的信号随时间记录','Signal recorded over time at a fixed wavelength'),fontsize=10,ha='center');x.text(1,2.2,T('分离发生在柱内\n检测发生在出口','Separation inside the column\nDetection after the column'),fontsize=12,color=green);x.set_title(T('B  用稳定流动读取时间顺序','B  Controlled flow reveals elution order'),loc='left');save(fig,'instrument')

 t=np.linspace(0,10,4001);t0=1.;k1=3.;alpha=1.12;N=2500.
 def peaks(N,alpha):
  tr=np.array([t0*(1+k1),t0*(1+alpha*k1)]);s=tr/np.sqrt(N);ys=np.array([g(t,m,w) for m,w in zip(tr,s)]);rs=(tr[1]-tr[0])/(2*sum(s));return tr,s,ys,rs
 fig,ax=plt.subplots(2,2,figsize=(12,7.6));records=[]
 for axis,(n,al,label) in zip(ax.flat[:3],[(2500,1.12,T('A  原条件','A  Initial conditions')),(10000,1.12,T('B  柱效提高四倍','B  Fourfold plate count')),(2500,1.30,T('C  改变选择性','C  Change selectivity'))]):
  tr,s,y,rs=peaks(n,al);axis.plot(t,y.sum(axis=0),color=blue,lw=2);axis.fill_between(t,0,y[0],alpha=.2,color=green);axis.fill_between(t,0,y[1],alpha=.2,color=gold);axis.set(xlim=(3.4,5.6),xlabel=T('时间 / min','Time / min'),ylabel=T('归一化信号 / 每 min','Normalized signal / per min'));axis.set_title(label+f' · Rs={rs:.2f}',loc='left');records.append([n,al,*tr,*s,rs])
 ns=np.linspace(1000,12000,100);als=np.linspace(1.01,1.4,100);nn,aa=np.meshgrid(ns,als);rsgrid=3*(aa-1)*np.sqrt(nn)/(2*(4+1+3*aa));im=ax[1,1].pcolormesh(ns,als,rsgrid,shading='auto',cmap='viridis');ax[1,1].contour(ns,als,rsgrid,levels=[1.5],colors=['white'],linewidths=1.5);ax[1,1].set(xlabel=T('理论塔板数 N','Theoretical plates N'),ylabel=T('选择性 α','Selectivity α'));ax[1,1].set_title(T('D  两种改进各有作用','D  Two distinct routes to separation'),loc='left');fig.colorbar(im,ax=ax[1,1],label='Rs');save(fig,'resolution');np.savetxt(out/'separation_cases.csv',records,delimiter=',',header='N,alpha,tR1_min,tR2_min,sigma1_min,sigma2_min,Rs',comments='')

 concentrations=np.repeat([0,2,5,10,20,40],3);calarea=6*concentrations+.8+rng.normal(0,.6,len(concentrations));slope,intercept=np.polyfit(concentrations,calarea,1)
 trace_t=np.linspace(4,7,1501);baseline=2+.3*(trace_t-4);truearea=6*13+.8;trace=baseline+truearea*g(trace_t,5.2,.12)+40*g(trace_t,6.25,.14)+rng.normal(0,.3,len(trace_t));baseline_mask=(trace_t<4.5)|(trace_t>6.85);bp=np.polyfit(trace_t[baseline_mask],trace[baseline_mask],1);estimated_base=np.polyval(bp,trace_t);region=(trace_t>=4.65)&(trace_t<=5.7);area=np.trapezoid((trace-estimated_base)[region],trace_t[region]);conc=(area-intercept)/slope;stock=conc*4
 fig,ax=plt.subplots(2,2,figsize=(12,7.5));ax[0,0].plot(trace_t,trace,color=blue,label=T('进样信号','Injected signal'));ax[0,0].plot(trace_t,estimated_base,color=gold,label=T('估计基线','Estimated baseline'));ax[0,0].fill_between(trace_t[region],estimated_base[region],trace[region],alpha=.25,color=green);ax[0,0].set(xlabel=T('时间 / min','Time / min'),ylabel='mAU');ax[0,0].legend(fontsize=9);ax[0,0].set_title(T('A  面积包括整个目标峰','A  Integrate the target peak'),loc='left')
 ax[0,1].scatter(concentrations,calarea,color=blue,s=22);xx=np.linspace(0,42,100);ax[0,1].plot(xx,slope*xx+intercept,color=green);ax[0,1].scatter([conc],[area],color=red,marker='D',s=55,label=T('未知样','Unknown'));ax[0,1].legend();ax[0,1].set(xlabel=T('浓度 / μg mL⁻¹','Concentration / micrograms per mL'),ylabel=T('峰面积 / mAU·min','Peak area / mAU min'));ax[0,1].set_title(T('B  同一目标物的校准','B  Analyte-specific calibration'),loc='left')
 ax[1,0].axhline(0,color='#8da0a8');ax[1,0].scatter(concentrations,calarea-(slope*concentrations+intercept),color=blue,s=25);ax[1,0].set(xlabel=T('浓度 / μg mL⁻¹','Concentration / micrograms per mL'),ylabel=T('面积残差 / mAU·min','Area residual / mAU min'));ax[1,0].set_title(T('C  校准残差保留误差信息','C  Calibration residuals reveal error'),loc='left')
 windows=[.12,.24,.36,.48,.6];captured=[]
 for half in windows:
  sel=np.abs(trace_t-5.2)<=half;captured.append(np.trapezoid((trace-estimated_base)[sel],trace_t[sel])/truearea*100)
 ax[1,1].plot(windows,captured,'o-',color=green);ax[1,1].axhline(100,color='#8da0a8',ls=':');ax[1,1].set(xlabel=T('积分窗口半宽 / min','Integration half-width / min'),ylabel=T('目标面积回收 / %','Target area recovered / %'),ylim=(60,105));ax[1,1].set_title(T('D  太窄的窗口遗漏峰翼','D  Narrow windows lose peak tails'),loc='left');save(fig,'quantification')
 np.savetxt(out/'calibration.csv',np.c_[concentrations,calarea,calarea-(slope*concentrations+intercept)],delimiter=',',header='concentration_ug_per_mL,area_mAU_min,residual_mAU_min',comments='');np.savetxt(out/'unknown_chromatogram.csv',np.c_[trace_t,trace,estimated_base],delimiter=',',header='time_min,signal_mAU,estimated_baseline_mAU',comments='')

 fig,ax=plt.subplots(1,3,figsize=(14,4.7));tt=np.linspace(0,16,500);program=np.clip(10+8*tt,10,90);arrival=np.clip(10+8*(tt-1.5),10,90);ax[0].plot(tt,program,color=blue,label=T('泵设定','Pump program'));ax[0].plot(tt,arrival,color=green,label=T('到达柱入口','At column inlet'));ax[0].set(xlabel=T('时间 / min','Time / min'),ylabel=T('有机相 B / %','Organic B / %'));ax[0].legend(fontsize=9);ax[0].set_title(T('A  梯度有到达延迟','A  Gradients have a delay'),loc='left')
 spikes=[0,5,10,20];recovered=np.array(spikes)*.85;ax[1].plot(spikes,spikes,ls=':',color='#8da0a8',label='100%');ax[1].plot(spikes,recovered,'o-',color=green,label='85%');ax[1].set(xlabel=T('提取前加入 / μg','Spike before extraction / micrograms'),ylabel=T('测得增加量 / μg','Measured increase / micrograms'));ax[1].legend();ax[1].set_title(T('B  加标追踪样品回收','B  Spikes track recovery'),loc='left')
 c=np.array([2.,5.,8.]);V=10.;v=1.;cumulative=V*c+v*np.r_[0,np.cumsum(c[:-1])];ax[2].plot([1,2,3],V*c,'o-',color=gold,label=T('当前容器内','Currently in vessel'));ax[2].plot([1,2,3],cumulative,'o-',color=green,label=T('累计释放','Cumulative released'));ax[2].set(xlabel=T('取样序号','Sampling event'),ylabel=T('目标物质量 / μg','Analyte mass / micrograms'));ax[2].set_xticks([1,2,3]);ax[2].legend(fontsize=9);ax[2].set_title(T('C  已取走的质量也要算','C  Include previously removed mass'),loc='left');save(fig,'method-decisions');np.savetxt(out/'release_sampling.csv',np.c_[c,V*c,cumulative],delimiter=',',header='concentration_ug_per_mL,current_mass_ug,cumulative_mass_ug',comments='')
 _,_,_,rs=peaks(2500,1.12)
 summary={'retention_factor_example':3.,'initial_resolution':float(rs),'fourfold_N_resolution':float(peaks(10000,1.12)[3]),'changed_selectivity_resolution':float(peaks(2500,1.3)[3]),'calibration_slope':float(slope),'calibration_intercept':float(intercept),'unknown_area_mAU_min':float(area),'unknown_diluted_ug_per_mL':float(conc),'unknown_original_ug_per_mL':float(stock),'dwell_delay_min':.75/.5,'spike_recovery_fraction':.85,'cumulative_release_final_ug':float(cumulative[-1]),'constructed_data':True}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
```

## 当浓度进入一个材料实验

载药材料的释放实验很好地说明，得到可靠浓度以后，仍需要一个与实验设计一致的质量账本。设材料浸在 10 mL 液体中，每次取走 1 mL 检测，再补回 1 mL 不含药物的新液体。到第三次取样前，容器中剩余的药物量等于当前浓度乘以 10 mL，但之前两次取走的药物已经离开容器。累计释放量应把它们加回来。漏掉这部分，会让释放较早、取样较频繁的实验尤其容易低估总量。

$$
M_n=Vc_n+v\sum_{i=1}^{n-1}c_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | 第 n 次取样前的累计释放量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 每次补液恢复后的容器总体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31eea81269f83b010cbeea2c.svg) | 相应取样前均匀液体中的浓度，μg/mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 每次取走的固定体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | 取样序号，无量纲；求和只包含先前取样。 |

累计量等于当前容器内量加先前取走量。V=10 mL、v=1 mL、c₁/c₂/c₃=2/5/8 μg/mL，M₃=80+2+5=87 μg。假设充分混合、等体积无目标物补液，并按定义处理降解或其他损失。

若前三次测得浓度依次为 2、5、8 μg/mL，第三次取样前容器内有 80 μg，前两次共取走 2+5=7 μg，累计为 87 μg。这个简单相加依赖几个清楚条件：每次混合充分、取样体积已知、补回液不含目标物、总体积恢复到 10 mL，并且所计目标物没有在液相中明显降解或被其他过程消耗。若药物会降解，可以把目标物与降解物的色谱分析结合起来，建立更完整的物质去向，而不是把所有浓度下降都解释为释放变慢。

![三个明确条件的教学计算。梯度延迟为 0.75 mL / 0.50 mL/min=1.5 min；加标回收模型为 85%；释放容器维持 10 mL，每次取走 1 mL 后补入不含目标物的液体，第三次取样前累计释放 87 μg。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fccfdac9ed2e08f6b6a13944.svg?v=fccfdac9ed2e)

图 4三个明确条件的教学计算。梯度延迟为 0.75 mL / 0.50 mL/min=1.5 min；加标回收模型为 85%；释放容器维持 10 mL，每次取走 1 mL 后补入不含目标物的液体，第三次取样前累计释放 87 μg。

材料浸提实验则需要区分“释放到指定介质中的量”和“材料内原来存在的总量”。温度、介质、时间、材料表面积和液体体积都会改变提取结果。用 HPLC 比较不同配方时，应让这些条件对应同一个研究问题。若目标是残余单体含量，选择能够充分提取并经过回收验证的方法；若目标是使用过程中可迁移的小分子，则按相关接触条件设计浸提。相同的峰面积，可以服务于不同问题，含量名称应准确对应实验定义。

分析测量与制备收集共享分离原理，却有不同重点。分析进样用少量物质判断组成或浓度；制备实验希望拿到可供后续使用的目标物，因此还要考虑载样量、收集区间、回收质量与溶剂去除。只收峰的中间一段可能提高纯度，同时减少回收量；收完整条带则可能带入邻近杂质。如果目的是纯化一种肽或添加剂，可再用适当分析条件检验收集物，并把实际回收质量与最初载入量比较。此时色谱图指导的是一次物质分离，而不仅是一个含量数值。

完成一次分析后，把样品准备、分离条件、检测波长、校准范围、积分规则和质量检查连接成一段可以重做的描述。保留原始色谱图以及处理后的面积表，让浓度有可追踪的依据。下一次需要改进时，先判断问题发生在进入仪器之前、柱内分离、出口检测还是换算回原样的步骤。HPLC 的价值就在于把复杂混合物拆成时间上可辨的组分，再把这些组分接回明确的化学、生物或材料问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Martin: The development of partition chromatography](https://www.nobelprize.org/uploads/2018/06/martin-lecture.pdf)

   分配色谱与逆流萃取的原始历史叙述。
2. [Thermo Fisher: HPLC basics](https://www.thermofisher.com/dk/en/home/industrial/chromatography/chromatography-learning-center/liquid-chromatography-information/hplc-basics.html?erpType=Global_E1)

   液路部件、流动相、固定相及检测记录。
3. [Agilent: Essentials of good HPLC method development](https://www.agilent.com/cs/library/slidepresentation/public/essentials_of_good_hplc_method_development_july_27_2022.pdf)

   分离度、柱效、选择性、流速与梯度延迟。
4. [Agilent: A guide to HPLC column selection](https://www.agilent.com/cs/library/eseminars/public/how-do-i-choose-a-guide-to-hplc-column-selection.pdf)

   固定相选择、颗粒尺寸与系统体积。
5. [JASCO: Qualitative and quantitative HPLC analysis](https://www.jasco-global.com/principle/principles-of-hplc-5-qualitative-and-quantitative-analysis/)

   保留时间、加标定位、外标与内标。
6. [Shimadzu: Quantitation error factors in sample preparation](https://www.shimadzu.com/an/service-support/technical-support/liquid-chromatography/essential_knowledge/error.html)

   容器吸附、稳定性、提取与回收实验。
