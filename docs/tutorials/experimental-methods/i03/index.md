# 扫描电镜与能谱：形貌、电子与元素

Source: https://ml-biomat.com/tutorials/experimental-methods/i03/
Language: zh-CN

沿着电子束到达样品后产生的不同信号，读懂表面图像、元素谱与它们之间的空间关系。

## 表面的纹理、颗粒与元素，分别要怎样看

一张静电纺丝膜用肉眼看起来像薄薄的白纸，放到扫描电子显微镜下，却可能出现交织的细纤维、珠状缺陷和彼此连接的孔隙。骨修复材料表面长出一层沉积物以后，显微图像能够显示它的形状，配合能量色散X射线谱，还能检查沉积区域是否出现钙、磷等元素信号。这两种观察常在同一台仪器上完成，但回答的问题不同：扫描电子显微镜，也就是SEM，记录电子束扫描位置对应的信号；EDS则把检测到的X射线按能量分类。把两者放在一起，可以建立形貌与组成之间的空间联系。

SEM图像容易让人产生“像在看山脉”的感觉，因为边缘、朝向和探测器位置共同形成明显的明暗。这里的亮度并不等于表面高度，黑暗区域也不一定就是空洞。材料成分、荷电、倾斜与局部几何都能改变信号。初次读图时，可以先描述直接可见的结构：纤维有多宽，颗粒是否团聚，裂纹从哪里经过；再结合探测器类型与制样方式解释明暗。EDS补充的是元素相关证据，也需要从能谱、背景与采集条件出发，而不是看到软件给出的元素名称就结束判断。

本篇会先拆开电子束与样品的相互作用，再讨论生物和聚合物样品为什么需要特别准备，随后把图像标定、电子剂量与能谱计数连接起来。真实花粉SEM图像用于观察表面结构；另一个明确标记为教学构造的能谱用于研究相邻峰如何重叠。两组材料彼此独立，能谱不是对花粉成分的测量。这样的安排让你既能看到仪器面对真实样品时的细节，又能在已知答案的计算中理解分析步骤为什么有效。

## 扫描电子束怎样把表面变成一幅图

SEM用电子源产生电子束，再由电场与磁场控制它的能量、会聚和扫描位置。可以把扫描想成用一支极细的笔按行访问样品上的许多位置，只不过每到一个位置，仪器记录的不是颜料，而是样品发出的信号。探测器在这一时刻收集到的信号强弱决定对应像素的亮度。扫描坐标与信号记录同步，许多点就组成一幅图像。真空环境帮助电子在仪器中稳定传播，也影响哪些样品能够直接放入常规样品室。

20世纪中期，奥特利与剑桥的研究者把电子扫描、探测和显示技术逐步结合，相关工作推动Stereoscan在1965年进入系列化生产。这个发展过程说明，显微镜的能力不仅来自“把束斑做小”，还来自能否高效收集信号、稳定扫描和正确显示。今天仍然需要同时考虑这些环节：一个很小的探针若只有很少电子，图像可能噪声很大；增加束流能改善计数，却也可能改变探针尺寸并加重样品受照。图中将扫描装置与信号来源放在一起，帮助理解这些联系。

![原创扫描电子显微镜与信号来源示意。左图将扫描位置与探测器信号联系起来，也呈现1965年Stereoscan系列化生产这一历史节点；右图比较SE、BSE与X射线的来源。相互作用范围取决于样品与束能，图示不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/eb273a1637aba7c8e99c5880.svg?v=eb273a1637ab)

图 1原创扫描电子显微镜与信号来源示意。左图将扫描位置与探测器信号联系起来，也呈现1965年Stereoscan系列化生产这一历史节点；右图比较SE、BSE与X射线的来源。相互作用范围取决于样品与束能，图示不按比例。

入射电子进入材料后会经历多次散射。二次电子通常指能量低于50 eV的被激发电子，由于能量低，能逃出样品的多来自靠近表面的区域。边缘或倾斜表面更容易让一部分二次电子逃逸，因此这类图像常有鲜明的表面纹理。背散射电子主要来自被散射后返回表面外的入射电子，能量范围较宽，信号通常对材料平均原子序数更敏感。在相似几何与探测条件下，含较高原子序数成分的区域常更亮；表面倾角、晶体取向和探测器位置也会参与形成对比。

另一条路径产生特征X射线。入射电子若使原子的内层电子离开原来的状态，较外层电子填补空位时，可以放出具有特定能量的X射线。不同元素的电子能级不同，因此这些能量提供元素识别线索。与此同时，电子在材料中减速还会形成连续X射线背景。EDS检测器并不是直接看到一个写着元素名字的粒子，而是测量许多X射线事件的能量，把它们累积到不同能道中，再从峰位与峰形识别可能的元素。

三类信号对应的空间范围不同。细小的电子束进入材料后会扩散，X射线的产生与逃逸区域可能明显大于表面成像的有效区域。因而一张轮廓清楚的纳米颗粒图，并不自动意味着同一像素的EDS信号只来自颗粒本身；下方基底、附近相和表面镀层也可能贡献。提高加速电压通常使电子进入更深区域，并帮助激发某些高能谱线；降低电压可以增强一些近表面信息，却可能无法有效激发所需谱线。仪器条件应由目标元素、样品尺寸与研究深度共同决定。

## 制样改变了什么，图像就应该怎样解释

金属块、干燥聚合物纤维和含水细胞不能采用完全相同的制样路线。常规高真空下，液态水会造成稳定性和真空问题，柔软的含水结构也可能在脱水过程中收缩或塌陷。生物样品常需要固定以尽量保留目标结构，再通过适当脱水与干燥方法准备观察。临界点干燥的思路是减少液—气界面移动时的毛细作用；冷冻电镜路线则通过低温保存状态，并结合专门转移与观察条件。哪条路线合适，要看研究关心的是干态表面、湿态结构还是某个处理后的形貌。

例如，冻干水凝胶里的孔洞可能受到冰晶生长与升华过程的影响。它们可以描述该冻干材料的形貌，但若要讨论水中原始网络的网孔尺度，还需要使用与湿态结构相匹配的方法。对于纤维膜，干燥本身可能较容易实现，但纤维断裂、压实和样品台上的粘接仍会改变局部形态。把制样状态写进对象名称，例如“冻干截面”“干态纤维表面”，比在图注末尾加一段泛泛的提醒更能帮助读者判断图像对应什么材料状态。

许多聚合物和生物样品导电性低，入射电子与离开样品的电子若不平衡，局部电荷会积累。荷电可能造成亮暗条带、突然闪亮、图像漂移或局部扭曲。建立样品到样品台的导电通路、采用合适的薄导电镀层、调整束流与入射能量，或者使用适当的低真空模式，都是围绕电荷平衡采取的措施。观察粉末时，松散颗粒若没有良好接触，可能比紧贴基底的部分更容易荷电。改变条件后同一区域的形貌是否稳定，是区分真实结构与成像伪影的一种实用检查。

镀层同时也是样品的一部分。薄金属层可以改善导电和信号，却会覆盖最细的纹理、增加表观尺寸，并在EDS中产生自己的元素峰。要分析金、铂或碳本身时，镀层、胶带与基底的选择尤其需要提前安排。若测量的是数十纳米宽的纤维，一个几纳米量级的覆盖层就可能带来可见偏差；若测量的是几十微米的孔径，同样厚度的影响又处于不同尺度。制样记录因此应与预计测量尺寸联系起来，而不是只记一句“喷金后观察”。

## 从真实花粉图像读出结构，再把像素换成长度

这幅SEM图像来自CDC公共卫生图像库，摄影者为Janice Carr，编号5609，属于公有领域图像。花粉表面的突起、沟槽与开口展示了SEM在观察复杂表面时的特点。原图保留了10 μm比例尺，我们没有改变局部纹理或填补结构。先沿着一个颗粒边缘观察亮度如何随朝向变化，再看看凹陷内部与周围是否采用同一种灰度。你会发现，形状可以通过多个线索识别，但把灰度直接转换成高度会忽略探测与几何关系。

![真实花粉扫描电子显微图，原图保留10 μm标尺。图像：CDC / Janice Carr，PHIL 5609，公有领域。表面纹理和明暗展示的是电子成像信号，未与右侧教学能谱关联。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bf1de67233fea46477c01428.svg?v=bf1de67233fe)

图 2真实花粉扫描电子显微图，原图保留10 μm标尺。图像：CDC / Janice Carr，PHIL 5609，公有领域。表面纹理和明暗展示的是电子成像信号，未与右侧教学能谱关联。

测量长度时，比例尺比图片上写的放大倍数更稳妥。图像在网页中缩小或放大以后，屏幕上的尺寸变化了，原来针对某种显示或输出条件的倍率不再能直接换算成实际长度。比例尺与图像一起等比例变化，仍然保持参照关系。若10 μm的比例尺在当前数字图像中横跨180个像素，每个像素约对应0.0556 μm。一条测得36像素宽的结构，表观宽度约2.0 μm。这里用180像素作为演算示例，正式分析应在所使用的原始文件上准确确定比例尺端点或读取校准元数据。

$$
p=\frac{L_b}{N_b},\qquad d=N_o p
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 当前图像的像素尺寸，μm/像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8508650ef567c89cbba636de.svg) | 标尺表示的实际长度，μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0a95fa5ddcb2300bb4c3a4e.svg) | 标尺覆盖的像素数，像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 对象沿测量线的长度，μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/94c0a2364daa8ec33aea23bd.svg) | 对象沿测量线覆盖的像素数，像素。 |

若10 μm标尺占180像素，则p=10/180=0.05556 μm/像素，36像素的对象长2 μm。标尺与图像必须经历相同缩放；倾斜表面的投影长度还需要结合几何解释。

纤维直径最好沿与纤维局部方向垂直的剖面测量。斜着跨过一条纤维，得到的线段会比真正的投影宽度更长。颗粒相互重叠时，投影面积也未必对应单颗粒完整轮廓。可以预先规定选点规则，在多个视野和独立样品上测量，并保存每个测量位置的标记图。随后展示分布，而不仅给出一个平均值。宽度分布可能揭示少量粗纤维、珠状缺陷或双峰结构，这些差异在一张“代表性图片”里很容易被忽略。

形貌分析还要处理图像本身的空间变换。样品倾斜会压缩某些方向的投影长度；自动漂移校正、拼接和重采样会改变像素坐标。对定量工作，应保留原始尺度与变换记录，检查标准样品的标定是否适用于当前条件。边缘增强滤波可以让轮廓看起来更清楚，也可能改变阈值边界；因此可用增强图辅助观看，而用经过明确验证的处理步骤完成测量。分析选择的好坏，最终体现在轮廓是否对应研究对象，而不是输出直方图是否平滑。

## 电子束也是一种处理：剂量与重复扫描

电子束把能量和电荷送入样品，所以成像本身也可能改变样品。聚合物、蛋白质和其他敏感材料可能出现收缩、熔融样变化、断裂或束致污染；同一区域反复扫描后变暗、变亮或出现矩形痕迹，应结合扫描历史检查。降低束流、减少驻留时间、先用低倍率寻找位置，再在需要的区域采集高分辨图，可以控制累计照射。具体条件需要由样品稳定性与目标信号确定，不能只照搬另一种材料的电压和扫描速度。

$$
N_e=\frac{It}{e},\qquad D=\frac{N_e}{A}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2244f89c20614334f7d67053.svg) | 入射电子总数，无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 束流，A；100 pA=10⁻¹⁰ A。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 在指定区域上的总照射时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 元电荷，1.602176634×10⁻¹⁹ C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 平均入射电子剂量，本例电子数/μm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 实际接受扫描的面积，μm²。 |

电流乘时间得到电荷，再除以每个电子的电荷得到电子数。100 pA照射1 s约有6.2415×10⁸个电子；均匀分布在100 μm²上约为6.2415×10⁶个电子/μm²。停留和重复扫描会改变局部剂量。

100 pA束流持续1 s，对应约6.24亿个入射电子。这个数看起来很大，但若电子分散到较大扫描面积，每单位面积受到的照射又不同。以100 μm²为例，平均面剂量约624万个电子/μm²；缩小到1 μm²、保持相同束流和总时间，平均面剂量就增加100倍。图像放大时扫描区域缩小，因此即使仪器面板上的束流没有变化，局部累计照射也可能显著增加。对敏感样品，记录电子束条件与扫描范围比只记录“拍了几张图”更有意义。

增加计数可以改善随机噪声，但需要付出剂量或时间。若背景很低，独立计数的相对标准差大致随总计数平方根的倒数减小：100个计数约有10%的相对波动，10000个约为1%。把噪声减半，需要约四倍计数，而不是两倍。实际谱峰位于连续背景之上，扣除背景后净峰面积的不确定性还包含背景估计的贡献。仪器的活时间与实际经过时间也不同，处理每个事件所需的时间会形成死时间；比较能谱强度时应使用合适的活时间与束流归一化。

## EDS能谱的峰位、峰面积与背景各自说明什么

能谱横轴是X射线能量，纵轴是某个能道中累积的事件数。峰位帮助识别可能的电子跃迁，峰面积与该跃迁产生并被检测到的X射线数量有关。一个元素可能有多组谱线，因此识别时应查看彼此相关的峰，而不是凭一个小突起自动命名。入射能量必须足以产生所需内层空位；即使元素存在，某条谱线也可能在当前条件下很弱。相邻元素谱线重叠、探测器逃逸峰与脉冲叠加等现象，都需要与候选元素一起检查。

元素定量比“峰高越大含量越多”多了几个环节。不同元素产生特征X射线的概率不同，X射线在样品中被吸收的程度不同，还可能引发其他元素的荧光；探测效率随能量变化，粗糙表面也会改变出射路径。标准样品与适当的基体校正把这些因素联系起来。NIST关于SEM/EDS定量的研究表明，高质量定量可以在明确的制样、标准与谱处理条件下实现。软件给出的质量百分数应与所用元素集合、归一化方式和样品几何一起阅读，不能把自动归一到100%的外观当成独立的质量检查。

$$
k_i=\frac{N_i/(t_iI_i)}{N_{i,s}/(t_{i,s}I_{i,s})}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e8755a0f9e8b8e36aada3a9f.svg) | 元素i在未知样品与标准样品之间的归一化强度比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 待分析元素的标记。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bf916434bdeeb6654028e556.svg) | 未知样品、标准样品的同一特征线净计数；背景已扣除。 |
| ![Formula](https://ml-biomat.com/static/agent-math/55fa88cba25de0f80f2ea93c.svg) | 对应采集的有效计数时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/70fd09737bb43bbcddb8e886.svg) | 对应采集束流，采用相同电流单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 下标s表示标准样品。 |

在同样的有效时间和束流下，未知样品6000计数、标准样品12000计数，k比为0.5。强度比先消除了照射量的差别；进一步获得组成，需要吸收、原子序数及荧光等基体修正，因此0.5不直接等于50%质量分数。

本篇用两个中心分别位于2.00和2.14 keV的教学峰演示重叠。它们称为峰1和峰2，不指定真实元素，净面积设为6000和3000计数。检测峰宽从80 eV增大到160 eV、240 eV时，两个峰越来越难用肉眼分开；总计数仍然可以保持相同。程序把已知峰形与背景组成一个联合模型，再用非负最小二乘估计两个面积和背景。已知中心与宽度让这个练习可控，真实分析则要通过校准、谱线组合和合适的物理模型确定这些信息。

![独立构造的教学能谱，两个峰位用于研究重叠，不指定元素。A改变能量分辨率；B同时拟合两个峰和背景；C检查按计数标准差缩放的残差；D展示无背景泊松计数的精度变化。完整代码生成这些数值。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5086be6e1869a29d7f24b11c.svg?v=5086be6e1869)

图 3独立构造的教学能谱，两个峰位用于研究重叠，不指定元素。A改变能量分辨率；B同时拟合两个峰和背景；C检查按计数标准差缩放的残差；D展示无背景泊松计数的精度变化。完整代码生成这些数值。

残差图把观测计数减去拟合计数，再除以近似计数标准差。若残差围绕零随机波动，说明当前模型能解释主要形状；若某个能量区间持续偏正或偏负，就可能漏掉一个峰、背景形状不对或峰宽设置不合适。拟合曲线贴近数据并不自动给出唯一元素组合，尤其当两个候选峰高度重叠时，面积之间会互相补偿。此时增加计数有助于降低随机噪声，改善能量分辨或引入其他谱线信息则帮助区分模型。两种改进针对不同原因，适合放在同一幅诊断图里理解。

$$
N_{\mathrm{net}}=N_g-\alpha N_b,\qquad \sigma_{\mathrm{net}}=\sqrt{N_g+\alpha^2N_b}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6468fae1cbb437ecfc0c3d51.svg) | 背景扣除后的净计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/20f373067c0c290e52601d71.svg) | 峰窗口的总计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0a95fa5ddcb2300bb4c3a4e.svg) | 独立背景窗口的计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 把背景窗口计数换算到峰窗口的面积或时间比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d4d550c712b8e8f75ec7484b.svg) | 净计数的标准差，计数单位。 |

假设两个窗口独立且满足泊松计数统计，扣除数值时，方差仍相加。1200个总计数减去200个等效背景计数，净计数1000，标准差√1400≈37.4，相对标准差约3.74%。若背景参数来自同一联合拟合，应使用拟合的协方差描述相关性。

## 改变峰宽与计数，观察哪些问题能靠多测一会儿解决

交互实验固定两个教学峰的位置，让你改变检测峰宽、第二个峰的相对面积和计数时间。曲线显示期望计数，不额外加入随机抖动，所以可以直接看到峰形重叠的变化。延长时间会把信号整体抬高，并改善预计计数精度，却不会让探测器的峰宽变小。减小第二个峰的面积后，它可能只表现为主峰一侧的肩部；这种形状说明，判断小峰需要看整个谱形和其他证据，而不是要求每个成分都长出一个独立尖峰。

## 改变分辨率，两个元素峰会发生什么

这是一组构造的教学谱，不对应花粉成分。保持峰位2.00与2.14 keV，调整探测器峰宽、第二峰面积比与计数时间。曲线显示期望计数；比较峰顶高度与总面积的变化。

[Figure: 双峰期望能谱](https://ml-biomat.com/tutorials/experimental-methods/i03/#I03-plot)

峰1的相对计数标准差按无背景理想值估算；重叠峰和背景使实际面积估计更困难。分辨率改善与延长采集时间解决的是不同问题。

完整代码生成原创SEM信号示意，展示随包附带的CDC花粉图，并独立构造一份带泊松计数噪声的教学EDS谱。程序保存每个能道的期望计数、模拟观测、拟合值与标准化残差，也输出已知无噪声模型的恢复结果，便于检查算法是否能在理想情况下找回6000与3000的峰面积。真实图片与模拟谱在文件和图注中都明确区分。你可以先改变峰宽，再改变计数规模，比较哪一种变化改善峰的区分，哪一种主要改善面积估计的随机稳定性。

### 完整Python：真实SEM图与能谱重叠实验

附带公开图像；教学谱采用固定随机种子。输出CSV、拟合参数、残差及三个双语图。

```
"""SEM/EDS: signal origins, a public-domain SEM image, and peak overlap.

Image: CDC/Janice Carr, PHIL 5609, public domain.
Spectra are constructed teaching data, not an analysis of the pollen image.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from PIL import Image
from scipy.optimize import nnls
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,6),layout='constrained')
    ax=axes[0];ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off');ax.set_title(tr('A  扫描位置与探测器信号配对','A  Pair scanning position with detector signal'))
    ax.add_patch(Rectangle((3.8,3.5),2.4,5.5,fc='#e2e8e5',ec=gray));ax.text(5,8.5,tr('电子源','Electron source'),ha='center')
    for y in [6.8,5,3.8]:ax.add_patch(Ellipse((5,y),2,.45,fc='#bfd4dc',ec=blue))
    ax.plot([5,5],[8,2.5],color=blue,lw=2);ax.text(6.7,6.6,tr('透镜与光阑','Lenses and apertures'));ax.text(6.7,4.7,tr('扫描线圈','Scan coils'))
    ax.add_patch(Rectangle((2,1.5),6,.8,fc='#c7b5a1'));ax.text(5,1.8,tr('样品台','Specimen stage'),ha='center')
    ax.add_patch(Rectangle((.5,3),1.6,1,fc='#c8e1d8',ec=green));ax.text(.3,4.3,tr('SE探测器','SE detector'))
    ax.annotate('',(1.4,3.4),(5,2.5),arrowprops={'arrowstyle':'->','lw':2,'color':green})
    ax.text(.3,.3,tr('1965：Stereoscan走向系列化生产\n扫描坐标决定像素位置，信号决定亮度','1965: Stereoscan enters series production\nScan coordinates locate pixels; signals set brightness'),fontsize=10)
    ax=axes[1];ax.set(xlim=(-4,4),ylim=(-4,4));ax.axis('off');ax.set_title(tr('B  同一束电子产生不同信号','B  One incident beam, several signals'))
    ax.add_patch(Rectangle((-4,-4),8,4,fc='#e6dfd1'));ax.plot([-4,4],[0,0],color=gray,lw=2)
    ax.add_patch(Ellipse((0,-1.6),3.5,3.1,fc='#abc6d0',alpha=.55));ax.add_patch(Ellipse((0,-.15),1.1,.3,fc=green,alpha=.6))
    ax.annotate('',(0,0),(0,3.6),arrowprops={'arrowstyle':'->','color':blue,'lw':3});ax.text(.2,2.8,tr('入射电子','Incident electrons'))
    ax.annotate('',(-2.8,1.6),(-.2,-.1),arrowprops={'arrowstyle':'->','color':green,'lw':2});ax.text(-3.9,2,tr('SE：近表面','SE: near surface'))
    ax.annotate('',(2.8,1.4),(.1,-1),arrowprops={'arrowstyle':'->','color':blue,'lw':2});ax.text(1.7,1.9,tr('BSE：散射返回','BSE: returning electrons'))
    ax.plot([.2,.6,1,1.4,1.8,2.2,2.6],[ -2,-1.9,-1.5,-1.6,-1.2,-1.3,-.9],color=red,lw=2);ax.text(1.4,-2.5,tr('X射线：元素信息','X-rays: elemental information'))
    ax.text(-3.8,-3.7,tr('范围取决于能量与材料；示意不按比例','Ranges depend on energy and material; not to scale'),fontsize=10)
    save(fig,'signals')
    photo=np.asarray(Image.open(Path(__file__).parent/'data/pollen-cdc5609.jpg'))
    fig,ax=plt.subplots(figsize=(10,7.5),layout='constrained');ax.imshow(photo,cmap='gray');ax.axis('off');ax.set_title(tr('真实SEM：花粉表面的纹理与几何','Real SEM: texture and geometry of pollen surfaces'))
    fig.text(.5,.01,'CDC / Janice Carr · PHIL 5609 · Public domain · wwwn.cdc.gov/phil',ha='center',fontsize=10)
    save(fig,'pollen')
    energy=np.arange(1.6,2.5001,.005);centers=np.array([2.00,2.14]);areas=np.array([6000.,3000.])
    def basis(fwhm):
        sigma=fwhm/np.sqrt(8*np.log(2))
        g=np.exp(-.5*((energy[:,None]-centers)/sigma)**2)
        return g/g.sum(axis=0)
    fwhm=.16;G=basis(fwhm);background=8.;expectation=G@areas+background
    rng=np.random.default_rng(1703);counts=rng.poisson(expectation)
    design=np.column_stack([G,np.ones(len(energy))]);coef,_=nnls(design,counts);fit=design@coef
    exact,_=nnls(design,expectation)
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for width,color in [(.08,green),(.16,red),(.24,blue)]:axes[0,0].plot(energy,basis(width)@areas+background,color=color,label=f'FWHM {width*1000:.0f} eV',lw=2)
    axes[0,0].set(xlabel=tr('能量 / keV','Energy / keV'),ylabel=tr('期望计数 / 能道','Expected counts / channel'),title=tr('A  分辨率改变峰的重叠','A  Resolution changes peak overlap'));axes[0,0].legend(frameon=False)
    axes[0,1].step(energy,counts,where='mid',color=gray,lw=1,label=tr('教学计数','Teaching counts'));axes[0,1].plot(energy,fit,color=red,lw=2,label=tr('固定峰位联合拟合','Joint fit with fixed centers'))
    for i,color in enumerate([green,blue]):axes[0,1].plot(energy,G[:,i]*coef[i],ls='--',color=color,label=f'Peak {i+1}')
    axes[0,1].set(xlabel=tr('能量 / keV','Energy / keV'),ylabel=tr('计数 / 能道','Counts / channel'),title=tr('B  同时处理峰与背景','B  Fit peaks and background together'));axes[0,1].legend(frameon=False,fontsize=9)
    residual=(counts-fit)/np.sqrt(np.maximum(fit,1));axes[1,0].plot(energy,residual,color=green,lw=1);axes[1,0].axhline(0,color=gray);axes[1,0].axhspan(-2,2,color=gray,alpha=.12)
    axes[1,0].set(xlabel=tr('能量 / keV','Energy / keV'),ylabel=tr('计数残差 / √拟合计数','Count residual / √fitted count'),title=tr('C  残差检验模型遗漏','C  Residuals reveal model mismatch'))
    n=np.logspace(1,5,100);axes[1,1].loglog(n,100/np.sqrt(n),color=blue,lw=2)
    axes[1,1].set(xlabel=tr('无背景的净计数','Net counts without background'),ylabel=tr('泊松相对标准差 / %','Poisson relative SD / %'),title=tr('D  计数增加四倍，相对噪声减半','D  Four times the counts halves relative noise'))
    save(fig,'eds')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['energy_keV','expected_counts','observed_teaching_counts','fitted_counts','standardized_residual']);w.writerows(zip(energy,expectation,counts,fit,residual))
    summary={'energy_channels':len(energy),'peak_separation_keV':.14,'noiseless_area1':float(exact[0]),'noiseless_area2':float(exact[1]),'noiseless_background':float(exact[2]),'fitted_area1':float(coef[0]),'fitted_area2':float(coef[1]),'fitted_background':float(coef[2]),'electron_count_100pA_1s':100e-12/1.602176634e-19,'scale_um_per_px_10um_180px':10/180,'poisson_relative_sd_10000':.01,'image_shape':list(photo.shape),'data_origin':'Real public-domain CDC SEM image; EDS spectrum independently constructed, not measured from that image.'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

固定随机种子运行后，两个峰的拟合面积约为6257.8与3076.7计数，每能道背景约7.16计数。它们与设定值的差异来自此次泊松抽样；把观测数据换成无噪声期望值，同一算法恢复6000、3000与8。这个比较把程序能否正确求解与一次实验中的随机波动分开，便于理解实际测量为什么需要误差估计。

## 让形貌与组成围绕同一个材料问题展开

把纤维直径统计做成一个具体实验，会发现选图方式与画线方式同样重要。可以先在低倍率图上划分网格，按预先设定的间隔选取视野，再在每个视野沿垂直于纤维轴线的方向测量。交叉处、断裂端和明显扁塌的位置需要有统一的处理规则，因为在那里画出的宽度与完整圆柱纤维的直径含义不同。测量线也不能只挑最细、最清楚的纤维；否则几百次画线仍可能围绕少数容易观察的对象重复。把原始测量线保留在图像副本中，别人就能理解每一个数字是怎样得到的。

若三块独立制备的纤维膜，每块取五个视野、每个视野量二十根纤维，得到三百个直径数字，并不等于有三百次独立材料制备。一个视野内的纤维共享加工条件，来自同一块膜的不同视野也可能相关。适合先画出每块膜各自的直径分布，再比较独立样品之间是否一致。对于偏斜的直径分布，中位数、四分位间距和完整分布图可以相互补充；一个平均值容易掩盖少量粗纤维。这样的统计设计让“纤维变细了”变成可以追溯到取样区域、对象数量和独立批次的陈述。

截面观察还会带来新的几何问题。一根斜切的圆柱在截面上看起来像椭圆，长轴受切割角度影响，直接把它当直径会偏大。多孔支架被机械切割后，边缘可能受压、拉裂或产生碎屑；经过离子束制备的截面则需要考虑加工造成的损伤层。观察到孔口被堵住时，可以比较不同位置、不同方向和不同制样路线，判断它在原材料中是否普遍存在。这些对照把“怎样看到”与“看到了什么”连起来，也解释了为什么一张清晰截面往往需要配合完整的样品几何信息。

研究材料表面沉积时，可以先用较低倍率记录分布，再在具有代表性的区域观察细节，并对沉积物、裸露基底和空白对照分别采集能谱。这样才能区分基底本来的元素、处理带来的变化和制样引入的信号。元素面分布图应与原始谱和计数信息配合：每个像素计数很少时，自动拉伸颜色可能把很弱的波动显示成鲜明斑块；不同元素各自采用最大值归一化时，颜色同样鲜艳也不意味着含量接近。

对于钙磷沉积，EDS可以帮助确认相关元素信号及其空间分布；晶相、化学键与有机成分则可由XRD、红外或其他合适方法补充。对于纤维膜，SEM直径与孔隙形貌可以与力学性能、润湿行为和细胞实验联系，但这些联系需要来自同批样品的测量。把每张图、每条谱和每个定量表连到明确的样品编号与处理条件，能够让微观观察成为研究证据的一部分，而不是独立于实验主线的装饰。

读完本篇后，可以尝试解释这样一组结果：某区域在背散射图里较亮，EDS中又出现明显金峰，但样品曾经喷金。亮度可能同时包含形貌、镀层和样品组成的贡献，下一步应通过制样记录、对照区域与合适的分析条件把它们分开。再看另一种情况：提高计数时间后，小峰的波动减小了，却仍然与主峰连在一起。这正是计数精度与能量分辨率不同的表现。把信号来源、样品状态和计算定义联系起来，SEM与EDS就能各自发挥清楚的作用。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [CDC PHIL 5609 — pollen SEM](https://wwwn.cdc.gov/phil/Details.aspx?pid=5609)

   真实图像身份、标尺和公有领域许可。

   Public domain; CDC / Janice Carr.
2. [JEOL — secondary electron](https://www.jeol.com/words/semterms/20121024.070758.php)

   二次电子能量及表面信号。
3. [JEOL — backscattered electron](https://www.jeol.com/words/semterms/20121024.072858.php)

   背散射电子、原子序数及形貌对比。
4. [University of Cambridge — Stereoscan](https://www-g.eng.cam.ac.uk/125/1950-1975/sem2.html)

   扫描电子显微镜的工程发展与1965年系列化生产。

   Historical institutional reference; diagram original.
5. [MyScope — SEM image artefacts](https://myscope.training/SEM_Image_artefacts_and_trouble_shooting)

   充电、漂移、污染与电子束损伤。

   Site educational text CC BY-SA 4.0 unless otherwise stated; linked reading.
6. [Newbury & Ritchie — quantitative SEM/SDD-EDS](https://link.springer.com/article/10.1007/s10853-014-8685-2)

   基于标准的元素定量、峰干扰、计数与基体修正。

   Open-access article CC BY 4.0; linked reading.
