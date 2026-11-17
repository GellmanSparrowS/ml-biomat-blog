# 光学与荧光显微镜：从光路到可信图像

Source: https://ml-biomat.com/tutorials/experimental-methods/i01/
Language: zh-CN

沿着样品、光路与像素理解显微成像，用真实细胞图像检验分辨率、强度与区域计数。

## 一张细胞照片，怎样变成一个可以回答的问题

把一小片透明水凝胶放到显微镜下，你可能看见一些圆点、细长的影子和若隐若现的边界。它们究竟是细胞、气泡、材料孔隙，还是落在盖玻片上的灰尘？如果细胞在一种材料上显得更亮、更大，究竟是它们长得更好，还是这一次曝光更长、焦点更准？光学显微镜把肉眼难以分辨的细节带到眼前，也把一系列判断交给观察者。本篇将从光如何经过样品讲起，逐步走到像素、分辨率、荧光强度和区域计数。读完以后，你应当能够为“细胞是否铺展开”“荧光标记分布在哪里”“两组样品是否真的有差别”选择合适的图像，而不是只挑一张漂亮照片。

先把“看见”分成三件事，会让后面的概念容易理解。检测，是判断有无信号；分辨，是把相邻的两个东西认作两个；测量，是把长度、面积、数量或亮度写成有单位、有定义的数。夜里很远的一盏灯可以被看见，却无法看清灯泡的形状，说明检测能力与空间分辨能力并不相同。显微镜里，一个比光学分辨尺度小得多的荧光分子也可能发出足够的光，让相机知道它在那里；图中的亮斑宽度却主要由光学系统决定。把这个亮斑的直径直接当成分子的直径，就把检测结果误读成了尺寸测量。

对生物材料研究而言，图像还需要与样品层级对应。一个培养孔里可以拍十个视野，一个视野里又可以测几十个细胞，但这些细胞共享培养液、材料配方与处理条件。研究材料批次差异时，独立制备的材料才构成主要重复；研究单个细胞形态分布时，细胞可以作为描述对象，同时保留它所属的视野和样品。采图之前确定“我要比较的是细胞、视野还是独立样品”，后面的统计图才会有清楚的分母。显微成像与实验设计从第一次选视野就已经连接在一起。

## 从胡克的观察到荧光标记：让透明结构产生对比

1665年出版的《显微图谱》把罗伯特·胡克观察到的微小结构带给了读者。书中的图像来自显微观察与细致绘图，这种工作方式提醒我们，显微技术的发展始终包含两个部分：让原本不易察觉的结构形成对比，以及把观察结果清楚地记录下来。早期复合显微镜用物镜形成放大的中间像，再由目镜进一步观察。今天的数字显微镜把中间像送到相机，记录方式改变了，照明、物镜、样品和观察平面之间的关系仍然决定图像里有什么。图中用简化光路并排展示了历史观察与现代荧光成像的联系。

![原创光路示意：左侧把早期复合显微镜的照明、样品与观察连接起来，右侧展示现代落射荧光成像如何按波长分开发射与激发。示意图不按比例绘制，也不是特定历史仪器的尺寸复原。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d104b2ad7afbf969ba73983b.svg?v=d104b2ad7afb)

图 1原创光路示意：左侧把早期复合显微镜的照明、样品与观察连接起来，右侧展示现代落射荧光成像如何按波长分开发射与激发。示意图不按比例绘制，也不是特定历史仪器的尺寸复原。

明场成像时，光穿过样品后进入物镜。若某处吸收或散射较强，到达相机的光就较少，那里通常显得较暗。染色组织因此可以呈现清晰结构，而活细胞往往含有大量水，吸收很弱，放在透明培养液中容易显得“没有东西”。细胞仍会改变光传播的速度和相位；可以把相位理解为两列波在同一时刻走到了各自起伏周期的什么位置。相差与微分干涉方法把这类较难直接看见的差别转换成强度变化，因而适合观察透明细胞。相差图上的光晕、微分干涉图上像浮雕的明暗，都与成像方式有关，不能直接当作细胞真实的高度地图。

荧光提供了另一种对比来源。某些分子吸收激发光以后，经过很短的时间放出发射光；常见荧光标记的发射波长比激发波长长。1852年，斯托克斯对荧光现象的研究使这种光谱变化成为可以系统讨论的问题。现代荧光显微镜利用波长差异把强烈的激发光与较弱的发射光分开：激发滤光片选择入射波段，二向色镜改变特定波段的传播方向，发射滤光片再清除残留的激发光。物镜既可以把激发光送到样品，又把一部分向各方向发出的荧光收集回来。因此，一块滤光片的选择不仅影响照片颜色，还直接影响背景有多高、两个通道是否串色。

标记让图像具有生物学选择性。例如，能结合DNA的染料常用于显示细胞核，带荧光的抗体可以帮助寻找目标蛋白，荧光微球可以显示水凝胶内部的运动。但是，显示“哪里有荧光”与显示“哪里有目标分子”之间，还隔着标记是否特异、染料是否进入样品、未结合染料是否洗去等实验环节。材料本身也可能发光，尤其在不同激发波段下表现不同。将不加染料的材料、不含目标的合适对照和单通道标记样品放在同一套成像条件下观察，可以把这些来源逐一辨认出来，随后再讨论细胞或蛋白的分布。

## 放大、分辨与采样，为什么是三个不同的旋钮

物镜上常能看见“60×/1.30”这样的标记。前面的数字表示放大倍率，后面的数字通常是数值孔径。倍率决定样品的像在探测器上有多大；数值孔径描述物镜能接受多宽的光锥。把物镜想成接雨水的漏斗有助于形成直觉：开口方向覆盖得更宽，就能收集更多方向来的光。光学系统的数值孔径还包含物镜与样品之间介质的折射率，因此高数值孔径物镜常与特定浸液一起设计。空气物镜、水浸物镜和油浸物镜需要各自合适的使用条件，随意把一种液体换成另一种，会改变实际光路和像差。

$$
\mathrm{NA}=n\sin\alpha
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/94fc28e088e9b56db129dfa6.svg) | 数值孔径，无量纲；此处指物方数值孔径。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 物镜与样品间介质的折射率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 被收集光锥的半角；代入三角函数时以弧度表示，或使用明确的角度模式。 |

例如n=1.515、半角约59.1°时，数值孔径约1.30。半角是光锥从中心轴到边缘的角度，所以不能把整个张角直接代入。介质和几何角度共同决定收集能力。

光有波动性，一个理想点光源经过有限大小的光学孔径后，也会形成有宽度的亮斑，称为点扩散函数，简称PSF。可以把一个复杂的荧光样品看作许多小光源的集合，每个小光源都贡献一份扩散开的亮斑；这些亮斑相加，形成最终图像。两个光源距离较远时，峰之间有明显凹谷；距离逐渐缩小时，亮斑重叠，识别两个对象就越来越困难。瑞利判据给出一种常用的横向分辨尺度，用来讨论理想衍射受限系统中两个等亮点源的区分。它不是所有样品都共有的一条硬边界，因为信噪比、亮度差和具体的识别方法也会影响判断。

$$
d_{\mathrm R}=\frac{0.61\lambda}{\mathrm{NA}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5044dd543be62338ea7d9e03.svg) | 理想横向瑞利分辨尺度；与波长采用相同长度单位，如μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 真空中的荧光发射波长，这里取0.520 μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/94fc28e088e9b56db129dfa6.svg) | 物方数值孔径，无量纲，这里取1.30。 |

0.61×0.520÷1.30=0.244 μm。公式描述理想圆孔、衍射受限条件下两个等亮点源的瑞利判据，系数来自艾里图样的空间结构；波长更短或孔径更大时，亮斑尺度减小。

以发射波长520 nm、数值孔径1.30为例，瑞利尺度约为244 nm，也就是0.244 μm。把相机图像再放大四倍，两个原本混在一起的亮斑会一起变大，并不会自动出现新的谷底。真正改善这类光学分辨，需要改变有效孔径、波长、像差或成像方法。图中的两点源比较使用高斯函数近似PSF的中心部分，便于计算与观察；真实圆孔产生的艾里图样还包含旁瓣。因此曲线用于解释重叠机制，数值分辨尺度仍按照明确写出的瑞利公式单独计算。

![教学计算与模拟。A：两点源相距0.30 μm时，较高数值孔径形成更窄的高斯中心剖面。B：光学曲线相同，采样过稀仍会漏掉谷底。C：比较纯光子噪声与含背景、读出噪声的信噪比。D：固定种子生成一万次平均计数为100的泊松曝光。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/376bb54dd7955f4f51ae6d03.svg?v=376bb54dd795)

图 2教学计算与模拟。A：两点源相距0.30 μm时，较高数值孔径形成更窄的高斯中心剖面。B：光学曲线相同，采样过稀仍会漏掉谷底。C：比较纯光子噪声与含背景、读出噪声的信噪比。D：固定种子生成一万次平均计数为100的泊松曝光。

光学系统给出细节以后，相机还必须把它记录下来。相机上的一个像素可能宽6.5 μm，经60倍总放大后，对应样品中约0.108 μm。样品平面的像素尺寸越大，同一段细节能落入的像素越少，就像用大方格纸描一条细弯线，转折容易被跳过去。这里用分辨尺度的一半作为易于操作的采样检查值：0.244 μm的一半约0.122 μm，所以0.108 μm像素能够覆盖这一要求。严格的采样设计还应根据成像模式的空间频率支持、相机耦合倍率与像素合并方式确定，实际实验可以用荧光微球或标定样品检查PSF与像素尺度。

$$
p_{\mathrm s}=\frac{p_{\mathrm c}}{M},\qquad p_{\mathrm s}\lesssim\frac{d_{\mathrm R}}2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4a7ed4ea54cfbe1740080f73.svg) | 样品平面的像素间距，μm/像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/410307030b95e045f504bfeb.svg) | 相机传感器的像素间距，μm/像素。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 从样品到相机的总横向放大倍率，无量纲，包含相机转接光学。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5044dd543be62338ea7d9e03.svg) | 所采用的横向分辨尺度，μm。 |

6.5 μm除以60，得到0.1083 μm/像素。此处以至少两个像素覆盖一个分辨尺度作为简明采样检查；它不是对全部成像模式的完整频域采样规定。像素合并与转接倍率改变后需重新计算。

分辨率与像素尺寸的区别会影响最普通的长度测量。假设一条纤维在图像里宽五个像素，像素间距为0.20 μm，直接相乘得到1.0 μm，这是图像上的表观宽度。若纤维本身接近PSF宽度，边缘已经受到明显模糊，这个数就需要结合成像模型解释。对几十微米大小的细胞测投影面积，同样的模糊可能只占较小比例；对数百纳米的纤维测直径，则成为主要误差来源。选择物镜与测量指标时，先把预计对象尺寸和成像尺度放到同一张尺子上，通常比拍完后反复更换阈值更有效。

## 从样品准备开始保护你想观察的结构

活细胞、固定细胞和切片组织需要不同的准备路径。活细胞成像关心形态变化、运动和短时间响应，温度、培养液、气体环境以及照明剂量都会影响观察过程。固定样品更适合稳定地记录某个时刻的结构，也方便多次染色和长时间采集，但固定、透化、脱水及封片都可能改变形态或分子分布。选择准备方法时，可以先写出希望保留的对象：是细胞膜的连续性、细胞骨架的形状，还是某种可溶性蛋白的位置？随后选择能保留这一对象、又能让标记进入目标位置的条件，并让比较组经历一致的处理。

透明材料也会改变光路。水凝胶、培养液、盖玻片与浸液的折射率如果不匹配，来自不同深度的光可能无法在同一位置准确会聚，图像会随着深度增加而变模糊。样品越厚，散射和离焦光也越值得关注。对薄层细胞，宽场荧光成像通常能高效采集；对三维培养结构，观察某一层时常需要共聚焦等具有光学切片能力的方法。先检查样品厚度、关注的深度和物镜工作距离，再决定仪器模式，可以避免把“深处看不清”误认为“深处没有细胞”。

盖玻片并非可随意替换的透明支架。有些高数值孔径物镜针对特定盖玻片厚度进行校正；偏离设计条件会引入像差。培养皿底部的材料和厚度也会影响可用物镜。测量前应把物镜标记、浸液、样品容器和相机连接方式一起记录，必要时用带已知刻度的载物台测微尺校准尺寸。图像文件里保留物理像素大小，比在导出图片上手画一条比例尺可靠，因为裁剪、重采样和排版时，比例尺需要随图像保持正确关系。

选视野同样属于实验准备。若总是寻找“细胞长得最好”的区域，最终图像会偏向局部最理想的状态。可以在事先规定的网格位置采样，或按照明确的随机规则选择视野，并记录是否排除边缘、气泡或明显制备损伤。排除标准应针对成像失败或样品不可用的原因，而不是针对观察结果是否符合预期。比较不同材料时，优先使用相同物镜、曝光、照明和处理流程；如果亮度范围差异很大，需要改变采集设置，就应保留每次设置，并设计能把信号带回同一计量尺度的标定。

## 相机记录的是光子形成的信号，亮度比较需要共同尺度

数字图像可以理解成一张二维表格，每个位置存放一个数。对于荧光相机，这个数来自光子在探测器中产生的电荷，再经过放大、偏置和数字化得到。常说的“16位图像”意味着数值可用的编码范围更大，并不保证每幅图都具有同样多的有效细节。若信号太强，探测器或数字化范围达到上限，继续增加光子也不会记录成更大的数，这就是饱和。饱和区域内部的真实强度关系已经丢失；把显示亮度调暗只能改变屏幕上的外观，无法把这些关系恢复出来。

即使光源平均亮度不变，相同时间内到达探测器的光子数仍会有波动。在常见的独立光子计数近似下，平均收集100个信号电子时，光子统计引起的标准差约为10个，理想信噪比约为10；平均收集400个时，标准差约20个，信噪比约20。信号增加四倍，信噪比通常只增加两倍，这解释了为什么一味延长曝光会逐渐付出更大的时间和光照代价。真实相机还包含背景光、暗信号和读出噪声，因此要把这些来源放进同一个噪声预算中。

$$
\mathrm{SNR}=\frac{S}{\sqrt{S+B+\sigma_{\mathrm r}^{2}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae03e7fd82fc9511ad569820.svg) | 信噪比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 单个像素在一次曝光中的平均信号电子计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 同一像素与曝光中的平均背景电子计数，假设服从独立泊松统计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/091162969f7c9d3f6f679061.svg) | 读出噪声的标准差，以电子计数表示；平方后是方差。 |

光子计数的泊松方差等于平均计数，独立噪声的方差相加，再开平方得到总标准差。S=100、B=100、读出噪声标准差=3时，100/√209≈6.917。背景均值视为已准确估计；有限背景估计、暗电流与像素间相关需要按实验另加。

本篇的例子设信号为100个电子、背景为100个电子、读出噪声标准差为3个电子，得到信噪比约6.92。这个计算把背景平均值看作已经通过足够准确的独立估计扣除，但背景的随机波动仍然存在。若只用很少几个像素估计背景，背景估计本身还会增加额外不确定性。改善信噪比可以通过增加有效信号，也可以通过降低自发荧光、杂散光和非特异标记来减少背景；后者有时比提高激发功率更适合活细胞。相机增益会改变数字值的比例，不能像增加实际检测到的光子那样改善光子统计。

屏幕上的颜色与原始信号也要分开。将一张灰度图显示成绿色，只是在数字值与显示颜色之间建立映射；将对比度范围从0—1000改为0—500，会让同一批数显得更亮。展示时可以选择便于辨认结构的映射，定量时仍应使用原始数值，并保存采用的显示范围。背景扣除后，一个细胞区域的积分信号等于区域内像素值之和减去同等面积的背景贡献。区域面积越大，背景贡献越多；因此总荧光与单位面积平均荧光回答的是不同的问题，比较前需要先说明究竟关心分子总量、局部浓度还是细胞大小。

## 用真实图像走一遍：从像素到区域，而不是直接跳到细胞结论

下面的图像来自David Root与CellProfiler公开的细胞DNA荧光数据，通过scikit-image分发，使用CC0许可。原始图像为512×512像素，保存为灰度TIFF。本篇保留它的数字值，用相同显示范围展示原图和分割结果，再把阈值变化带来的影响画出来。这个示例没有为原始图像补造显微镜倍率或物理像素大小，因此横纵坐标使用像素，区域面积也使用像素数。实际实验要报告微米或平方微米时，应从原始采集元数据或独立标定取得换算比例。

![真实DNA荧光图像与分析。原图：David Root / CellProfiler，经scikit-image分发，CC0。A、B使用相同显示范围；绿色轮廓对应平滑后阈值45、面积至少40像素的连通区域。C保留原始灰度分布。D显示区域数随阈值变化。坐标使用像素，不推定缺失的物理标定。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/431f5047400f4db8213b46e8.svg?v=431f5047400f)

图 3真实DNA荧光图像与分析。原图：David Root / CellProfiler，经scikit-image分发，CC0。A、B使用相同显示范围；绿色轮廓对应平滑后阈值45、面积至少40像素的连通区域。C保留原始灰度分布。D显示区域数随阈值变化。坐标使用像素，不推定缺失的物理标定。

计算先用标准差为0.8像素的高斯滤波轻度平滑图像，再把大于45的像素归为前景，最后保留面积至少40像素的连通区域。高斯滤波相当于让附近像素按距离共同参与估计，可减小细小波动，也会改变边缘与相邻对象之间的连接。阈值把连续灰度转换成“保留或不保留”的决定；连通区域则把相接的前景像素组成一组。三个步骤各自有明确作用，所以应分别检查：平滑是否抹去了细节，阈值是否截掉暗核，面积筛选是否删除了真实的小对象。

两个相邻细胞核一旦在二值图里接触，就可能被算成一个区域；一个亮度不均的核也可能被切成几块。因此，输出中的“连通区域数”保持这个名称，不直接改写为细胞总数。右下图把阈值从20扫到100，让你观察参数改变时区域数是否稳定。较低阈值可能把相邻区域连成大片，较高阈值又可能只留下亮核的一部分。一个平坦区间能提示结果对阈值较不敏感，但仍要把轮廓叠回原图，逐一检查代表性的密集、稀疏、明亮和暗弱区域，确定这些区域对应什么生物对象。

若研究目标是正式计数，下一步可以加入人工标注的校验视野，或利用距离变换与分水岭把接触的核分开。距离变换记录前景像素离边界有多远，核的内部常形成较高的“山峰”；从这些中心向外分配像素，可以帮助划分接触对象。中心点过多会把一个核切碎，过少又会合并多个核，所以方法选择仍然要回到实际图像。定量结果应保留逐对象面积、平均亮度和所属样品编号，这样异常对象可以被定位回原图，组间比较也能够按照真实的实验层级展开。

## 亲手改变孔径和像素尺寸，再运行完整分析

交互区固定发射波长为520 nm，把两个点源放在同一条横线上。调节数值孔径，会改变点扩散函数的宽度；调节点源间距，会改变两个峰的重叠程度；调节样品平面像素间距，则会改变相机能记录多少个采样点。请先预测哪个操作能让谷底变清楚，再看曲线和采样点如何变化。界面同时显示瑞利尺度与每个分辨尺度对应的像素数，帮助你把视觉印象和数量联系起来。这里只模拟横向中心剖面，真实实验还需要检查轴向分辨、像差、噪声和样品运动。

## 两点源显微实验

改变光学孔径、点源间距与相机采样，观察同一测量链中不同环节的作用。横轴是样品平面的横向位置；曲线是教学用高斯PSF叠加，圆点是相机采样。

[Figure: 点源强度曲线与采样点](https://ml-biomat.com/tutorials/experimental-methods/i01/#I01-plot)

完整程序把本篇的三幅图重新生成：第一幅是原创光路示意，第二幅是分辨与光子统计的教学计算，第三幅使用随下载包附带的真实显微图像。程序会输出阈值扫描表、原始与处理数组，以及含分辨尺度、像素尺寸、信噪比和区域计数的摘要。你可以先只改变阈值或平滑参数中的一个，比较叠加轮廓与扫描曲线的变化；理解单个参数以后，再讨论组合调整。这样每次改动都对应一个可解释的问题，而不是把处理流程当作寻找最好看结果的黑箱。

### 完整Python：光学尺度、光子统计与真实图像分析

下载包附带CC0原始TIFF；程序离线读取，输出三幅图、数据数组、阈值扫描表与数值摘要。

```
"""Optical microscopy: resolution, photon statistics and a real CC0 image.

The microscopy data are mitosis.tif, David Root / CellProfiler, CC0.
The analytical point-spread profiles and photon experiment are teaching models.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, FancyArrowPatch


def style():
    plt.rcParams.update({'font.family': 'sans-serif',
        'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
        'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': '#243b45', 'text.color': '#243b45',
        'axes.edgecolor': '#849398', 'axes.titleweight': 'bold',
        'font.size': 11, 'savefig.facecolor': '#faf9f5', 'figure.facecolor': '#faf9f5'})


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    style()
    zh = language == 'zh'
    def tr(a, b): return a if zh else b
    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        fig.savefig(output / f'{name}-{language}.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
    blue, green, red, gray = '#3473a8', '#168477', '#bb6046', '#69787e'

    # Original explanatory drawing: the optical geometry is schematic.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0, 10), ylim=(0, 10)); ax.axis('off')
    a = axes[0]
    a.set_title(tr('A  从照明到观察：早期复合显微镜', 'A  Illumination and viewing: a compound microscope'))
    a.add_patch(Rectangle((4.55, 4), .9, 4.5, color='#ded4bd'))
    a.add_patch(Ellipse((5, 8.2), 1.2, .3, fc='#d7e8ed', ec=blue))
    a.add_patch(Ellipse((5, 4.3), 1.2, .3, fc='#d7e8ed', ec=blue))
    a.plot([3, 7], [2.8, 2.8], color=gray, lw=5)
    a.add_patch(Ellipse((5, 2.9), .6, .15, color=red))
    a.add_patch(Ellipse((1.5, 2.8), .7, .7, color='#e8af58'))
    a.annotate('', (4.8, 2.9), (1.9, 2.9), arrowprops={'arrowstyle':'->','color':'#c58c37','lw':2})
    a.annotate('', (5, 8.9), (5, 3.1), arrowprops={'arrowstyle':'->','color':green,'lw':2})
    for x, y, label in [(6,8.2,tr('目镜','Eyepiece')),(6,4.3,tr('物镜','Objective')),
        (6,2.4,tr('样品','Specimen')),(.3,1.7,tr('照明','Illumination'))]:
        a.text(x,y,label,fontsize=10)
    a.text(.3,.3,tr('1665：《显微图谱》把观察与绘图联系起来\n图示说明光路，并非历史仪器的尺寸复原',
        '1665: Micrographia connects observation and illustration\nOptical schematic; not a dimensional reconstruction'),fontsize=10)
    a = axes[1]
    a.set_title(tr('B  荧光显微镜：分开激发光与发射光','B  Fluorescence: separate excitation and emission'))
    a.plot([.8,5,5],[6.8,6.8,2.7],color=blue,lw=3)
    a.plot([5.25,5.25],[2.7,9],color=green,lw=3)
    a.plot([4.3,5.7],[6.1,7.5],color=gray,lw=4)
    a.add_patch(Ellipse((5.1,4.3),1.7,.45,fc='#d7e8ed',ec=blue))
    a.add_patch(Rectangle((4.6,8.7),1.2,.7,fc='#dde5e3',ec=gray))
    a.add_patch(Ellipse((5.1,2.5),2,.35,fc='#d5a190'))
    a.add_patch(Rectangle((2.4,6.1),.15,1.4,fc=blue,alpha=.5))
    a.add_patch(Rectangle((4.6,7.9),1.2,.12,fc=green,alpha=.6))
    a.text(.2,7.4,tr('激发光','Excitation'),color=blue)
    a.text(6.2,6.7,tr('二向色镜','Dichroic mirror'))
    a.text(6.2,4.2,tr('物镜','Objective'))
    a.text(6.2,2.4,tr('荧光样品','Fluorescent specimen'))
    a.text(6.2,8.1,tr('发射滤光片','Emission filter'))
    a.text(6.2,9,tr('相机','Camera'))
    a.text(.3,.3,tr('蓝色：激发路径；绿色：被收集的发射路径\n只有一小部分各向发射的光进入物镜',
        'Blue: excitation path; green: collected emission\nOnly a fraction of emitted light enters the objective'),fontsize=10)
    save(fig, 'optics')

    wavelength_um, na, camera_pixel_um, magnification = .520, 1.3, 6.5, 60
    rayleigh_um = .61 * wavelength_um / na
    sampling_um = camera_pixel_um / magnification
    x = np.linspace(-1,1,1001)
    sigma = .21 * wavelength_um / na
    sep = .30
    profiles = {}
    fig, axes = plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for aperture, color in [(.65, red),(1.3,green)]:
        s=.21*wavelength_um/aperture
        y=np.exp(-.5*((x-sep/2)/s)**2)+np.exp(-.5*((x+sep/2)/s)**2)
        profiles[str(aperture)]=y
        axes[0,0].plot(x,y,lw=2.4,color=color,label=f'NA={aperture:.2f}')
    axes[0,0].set(xlim=(-.7,.7),xlabel=tr('横向位置 / μm','Lateral position / μm'),ylabel=tr('相对强度','Relative intensity'),title=tr('A  两个点源相距 0.30 μm','A  Two emitters separated by 0.30 μm'))
    axes[0,0].legend(frameon=False)
    fine=profiles['1.3']
    axes[0,1].plot(x,fine,color=gray,lw=1.5,label=tr('连续模型','Continuous model'))
    for pitch,marker,color in [(.1083,'o',green),(.325,'s',red)]:
        xp=np.arange(-.65,.66,pitch)
        yp=np.exp(-.5*((xp-sep/2)/sigma)**2)+np.exp(-.5*((xp+sep/2)/sigma)**2)
        axes[0,1].plot(xp,yp,marker=marker,color=color,ls='--',label=f'{pitch:.3f} μm / pixel')
    axes[0,1].set(xlim=(-.7,.7),xlabel=tr('横向位置 / μm','Lateral position / μm'),ylabel=tr('相对强度','Relative intensity'),title=tr('B  采样太稀会丢掉峰间结构','B  Coarse sampling loses the valley'))
    axes[0,1].legend(frameon=False,fontsize=9)
    photons=np.logspace(0,4,180)
    axes[1,0].loglog(photons,np.sqrt(photons),color=green,lw=2.4,label=tr('纯光子噪声','Photon noise only'))
    axes[1,0].loglog(photons,photons/np.sqrt(photons+100+3**2),color=blue,lw=2.4,label=tr('背景100电子，读出噪声3电子','Background 100; read noise SD 3 electrons'))
    axes[1,0].set(xlabel=tr('平均信号电子数','Mean signal electrons'),ylabel='SNR',title=tr('C  多收集光子怎样改善信噪比','C  How collected photons improve SNR'))
    axes[1,0].legend(frameon=False,fontsize=9)
    rng=np.random.default_rng(612)
    counts=rng.poisson(100,10000)
    axes[1,1].hist(counts,bins=np.arange(60,141,2),color=blue,alpha=.8)
    axes[1,1].axvline(100,color=red,ls='--')
    axes[1,1].set(xlabel=tr('一次曝光的光子数','Photon count in one exposure'),ylabel=tr('模拟次数','Number of simulations'),title=tr('D  同样亮的光源仍会波动','D  A constant source still fluctuates'))
    save(fig,'resolution')

    image=np.asarray(Image.open(Path(__file__).parent/'data/mitosis.tif')).astype(float)
    if image.shape != (512,512): raise ValueError(f'Unexpected image shape {image.shape}')
    smooth=ndimage.gaussian_filter(image,.8)
    threshold=45
    def objects(t):
        mask=smooth>t
        labels,n=ndimage.label(mask)
        sizes=np.bincount(labels.ravel())
        keep=sizes>=40;keep[0]=False
        return keep[labels],int(np.sum(keep))
    mask,nobjects=objects(threshold)
    thresholds=np.arange(20,101,5)
    values=np.array([objects(t)[1] for t in thresholds])
    fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
    axes[0,0].imshow(image,cmap='gray',vmin=0,vmax=180)
    axes[0,0].set(title=tr('A  真实DNA荧光图像 / CC0','A  Real DNA fluorescence image / CC0'),xlabel=tr('x / 像素','x / pixel'),ylabel=tr('y / 像素','y / pixel'))
    axes[0,1].imshow(image,cmap='gray',vmin=0,vmax=180)
    axes[0,1].contour(mask,levels=[.5],colors=[green],linewidths=.6)
    axes[0,1].set(title=tr(f'B  阈值45：{nobjects}个连通区域',f'B  Threshold 45: {nobjects} connected regions'),xlabel=tr('x / 像素','x / pixel'),ylabel=tr('y / 像素','y / pixel'))
    axes[1,0].hist(image.ravel(),bins=np.arange(257),color=gray)
    axes[1,0].set(yscale='log',xlabel=tr('原始灰度 / 数字量','Raw intensity / digital number'),ylabel=tr('像素数','Pixel count'),title=tr('C  保留原始灰度分布','C  Preserve the raw intensity distribution'))
    axes[1,0].axvline(threshold,color=red,ls='--')
    axes[1,1].plot(thresholds,values,'o-',color=green,lw=2)
    axes[1,1].axvline(threshold,color=red,ls='--')
    axes[1,1].set(xlabel=tr('分割阈值 / 数字量','Segmentation threshold / digital number'),ylabel=tr('面积≥40像素的区域数','Regions with area ≥40 pixels'),title=tr('D  参数敏感性：区域数不等于真细胞数','D  Sensitivity: regions are not ground-truth cells'))
    save(fig,'measurement')
    np.savez_compressed(output/'image_analysis.npz',raw=image,smoothed=smooth,mask=mask)
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['threshold_digital_number','connected_regions_area_ge40px']);w.writerows(zip(thresholds,values))
    summary={'rayleigh_um':rayleigh_um,'sample_pixel_um':sampling_um,
        'snr_100_signal_100_background_3_read':100/np.sqrt(209),
        'image_height_px':image.shape[0],'image_width_px':image.shape[1],
        'connected_regions_threshold45':nobjects,'mask_fraction_threshold45':float(mask.mean()),
        'poisson_sample_mean':float(counts.mean()),'poisson_sample_sd':float(counts.std(ddof=1)),
        'data_origin':'Real microscopy: David Root / CellProfiler, CC0; point profiles and photon draws: constructed teaching models'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='zh')
    args=parser.parse_args();main(args.output,args.language)
```

## 把一组照片组织成一次有说服力的测量

现在回到开头的水凝胶。若问题是细胞是否更容易铺展，先选择能清楚显示细胞边缘的成像方式，保证各组像素尺度一致，再定义投影面积、长宽比或圆度等指标。若问题是某种蛋白是否增加，就需要合适的标记对照、未饱和的强度范围与一致的背景处理，并明确按单细胞、单位面积还是总样品量比较。若问题是细胞是否进入材料内部，一张表面照片提供的信息就不够，应采集与深度有关的数据，并检查深层信号衰减。仪器设置随着问题变化，图像的解释也随之改变。

一个容易执行的成像记录，应能回答样品如何制备、在哪些位置采图、光怎样照进去、相机怎样记录、像素如何换算成尺寸、数值怎样处理。把原始图、处理后的数值表和用于展示的图分别保存，能让它们各自完成自己的任务。原始图保留测量信息，数值表承载比较，展示图帮助读者理解结构与分析位置。裁剪可以突出细节，但要保留足够的整体视野；同一指标的比较图宜使用共同尺度，并说明误差条代表样品间变化、细胞间变化还是测量不确定性。

最后可以用一个具体练习检验理解：两组细胞在同一材料上培养，B组照片比A组亮两倍，而B组曝光也恰好长两倍。若探测器工作在线性范围，背景与光漂白影响得到控制，这个结果首先说明记录到的数字量与曝光时间共同变化；应把曝光和背景处理纳入比较，再讨论标记量。若B组同时出现大片饱和区域，就需要重新采集适当曝光的图像。这个判断不需要复杂数学，它依靠的是整条测量链：样品产生光，光学系统收集光，相机编码信号，分析方法把信号转成与研究问题对应的量。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Nikon MicroscopyU — Numerical Aperture](https://www.microscopyu.com/microscopy-basics/numerical-aperture)

   理解光锥、折射率与数值孔径。
2. [Nikon MicroscopyU — Introduction to Fluorescence Microscopy](https://www.microscopyu.com/techniques/fluorescence/introduction-to-fluorescence-microscopy)

   激发与发射分离、滤光片及斯托克斯历史。
3. [Introduction to Bioimage Analysis — Blur & the PSF](https://bioimagebook.github.io/chapters/3-fluorescence/2-formation_spatial/formation_spatial.html)

   继续学习点扩散函数及其对测量的影响。

   Book original content CC BY 4.0; linked reading.
4. [Introduction to Bioimage Analysis — From photons to pixels](https://bioimagebook.github.io/chapters/3-fluorescence/1-formation_overview/formation_overview.html)

   连接光子、探测器和数字像素。

   Book original content CC BY 4.0; linked reading.
5. [scikit-image — human_mitosis dataset](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.human_mitosis)

   真实图像的身份与CC0许可。

   Image copyright David Root, CC0.
6. [scikit-image — Segment human cells in mitosis](https://scikit-image.org/docs/stable/auto_examples/applications/plot_human_mitosis.html)

   观察阈值、接触细胞核与计数之间的关系。
7. [Robert Hooke — Micrographia, 1665 / Wellcome Collection](https://wellcomecollection.org/works/apmaw56u)

   查阅历史原著，理解观察与绘图的联系。

   Digitized work marked Public Domain by Wellcome Collection.
