# 表面张力：液滴、液面与界面能

Source: https://ml-biomat.com/tutorials/experimental-methods/p04/
Language: zh-CN

用薄板的力与悬滴的形状测量界面张力，再看表面年龄和浓度怎样改变读数。

## 一滴清洁剂，为什么能改变一大片水面

把清水滴到一片洁净塑料上，水往往聚成珠；加入少量表面活性剂后，同样体积的液体可能铺得更开。配制蛋白质药物时，研究者又会遇到另一个问题：摇晃产生的新鲜气液界面可能吸附蛋白质，影响它的构象与聚集。涂层能否均匀覆盖、乳液能否形成细小液滴、泡沫能否长期存在，都与界面有关。表面张力测量把这些看似不同的问题连接起来：在规定温度、组成和界面形成时间下，扩大一块液体表面，需要付出多少自由能？也可以换一种实验语言问：液体沿着接触线，给探针施加了多大的力？

液体内部的分子周围大多是同类邻居，界面附近的分子面对的环境不同。因此，让更多分子处于界面通常需要做功，液滴便倾向于减少表面积。固定体积的球体具有最小表面积，这解释了小水滴为什么接近球形。把表面想成一张会收缩的薄膜，有助于理解力的方向；但真实液面能够流动，界面上的分子也会持续交换，它与具有固定材料点的橡皮膜不同。表面张力的单位是牛顿每米，常写为毫牛顿每米；从能量角度看，它也等于每平方米需要的焦耳数。单位之间的等价来自做功等于力乘距离，而面积增加量等于边长乘移动距离。

日常说的表面张力通常指液体与气体之间的界面张力。油和水之间同样存在界面张力，只是两边都是液体，计算悬滴形状时必须使用两相密度之差。黏度则描述流动时内部摩擦的强弱：蜂蜜流得慢主要与黏度有关，液滴边界愿不愿意扩大与界面张力有关。两者能够同时影响液滴形成，却对应不同的测量量。一个液体具有较低表面张力，也并不自动意味着它能在任何固体上完全铺展；固液界面与固气界面的能量仍参与接触角的形成。本章用力和轮廓两条实验路线测量张力，再把时间与浓度放入同一张实验地图。

## 把水面的“干净程度”变成可以控制的变量

十九世纪末，Agnes Pockels在日常条件下研究水面。她在1891年发表于《Nature》的信中描述了一个长约70厘米、宽约5厘米、深约2厘米的长方形水槽：水加到槽口，一块可移动的横向薄片把水面分成不同区域。移动薄片时，受限区域的面积改变，表面污染物的拥挤程度也随之改变。她还利用轻巧的天平与小圆片研究水面作用力。这个设计的巧妙之处，是把“这盆水似乎不一样”拆成可以逐项改变的量：表面面积、表面物质和测力条件。图中的装置是根据这一实验思想绘制的原理示意，帮助理解变量之间的关系。

这段历史与今天的实验仍然相通。清洁过的容器、空气中的有机物、吸头上残留的清洗剂，都可能改变真正参与测量的表面。Pockels后续的讨论也重新检查了器具清洁与早期解释的关系。一个平滑、稳定的数字并不替代对界面状态的控制；如果痕量物质持续吸附，测到的表面张力就会随时间变化。对于蛋白质、脂质和聚合物溶液，界面本身还可能发生结构重排。研究者需要同时规定溶液怎样配制、界面何时生成、等待了多久，以及探针或液滴经历过怎样的接触过程。

![左：依据Pockels 1891年水槽与移动隔板实验思想绘制的原创示意，圆点代表表面物质。右：完全润湿薄板的弯月面与向下毛细力、向上浮力；几何与箭头不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/01c584f9b6060b3a365b1462.svg?v=01c584f9b606)

图 1左：依据Pockels 1891年水槽与移动隔板实验思想绘制的原创示意，圆点代表表面物质。右：完全润湿薄板的弯月面与向下毛细力、向上浮力；几何与箭头不按比例。

现代张力仪把这种变量控制与更灵敏的传感器结合起来。Wilhelmy板法将一片薄板悬挂在微量天平下，使板的下端接触并进入液体。液体沿着板的四周形成弯月面，表面张力在竖直方向上的分量会改变天平读数。悬滴法则从相机图像读取另一种结果：重力把液滴拉长，界面张力使轮廓保持紧凑，二者竞争决定外形。两种方法分别把界面性质编码进力和形状，因此它们的关键准备也不同。前者尤其关注探针周长、润湿状态与浮力，后者尤其关注图像尺度、密度差与轮廓质量。

## 从天平读数中分离毛细力和浮力

先在空气中称量干板，再把这个重量从后续读数中扣除，称为去皮。去皮后的读数仍然包含两项：接触线处的毛细力，以及浸入液体的板体受到的浮力。本例把向下的力规定为正，完全润湿时毛细力向下，浮力向上。假设薄板宽10毫米、厚0.1毫米，接触线绕板一周，其周长是两个宽度加两个厚度，等于20.2毫米。不能只取板的宽度，因为前后两个宽面和两条窄边都与液体相接。板越薄，窄边贡献越小，但它仍然有清楚的几何含义。

$$
F_{\mathrm{tare}}=\gamma P\cos\theta-\Delta\rho\,gwtz,\qquad P=2(w+t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b01fb8392b6a8aa7cb7333fd.svg) | 扣除干板重量后的竖直力，N；向下为正。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 液体界面张力，N/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 润湿周长，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 板与液体的接触角，从液体内读取。 |
| ![Formula](https://ml-biomat.com/static/agent-math/988fbc7bbcda53116494bdef.svg) | 液体与空气密度差，kg/m³，本例近似1000。 |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | 重力加速度，9.81 m/s²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 板宽，m；本例0.010。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 板厚，m；本例0.0001。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 浸入深度，m。 |

静态、规则截面和固定接触角条件下，竖直毛细力减去浮力。γ=0.050 N/m、θ=0、z=0给出F=0.00101 N；z=0.005 m时为0.00096095 N。

如果表面张力为50毫牛顿每米，接触角为零，刚接触水面时的毛细力是1.01毫牛顿。把板再浸入5毫米，排开的液体体积等于宽、厚、深度三者相乘，浮力达到0.04905毫牛顿，去皮后的向下读数便降为0.96095毫牛顿。将后一数字直接除以周长，会得到偏低的张力。更清楚的处理是记录多个浸入深度，画出力随深度的直线，再把直线外推到零深度。斜率主要反映浮力，截距给出毛细力。示例加入小幅测量噪声，得到约1.01048毫牛顿截距，对应50.02385毫牛顿每米。

![构造观测：A以零深度截距分离浮力；B固定真实张力为50 mN/m，显示误用零接触角带来的系统变化。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/226dd950f0d9ab8c29e821f2.svg?v=226dd950f0d9)

图 2构造观测：A以零深度截距分离浮力；B固定真实张力为50 mN/m，显示误用零接触角带来的系统变化。

接触角决定毛细力有多少投影到竖直方向。图中的板表面若具有30度接触角，而计算时仍假定完全润湿，原本50毫牛顿每米的张力会被读成约43.30毫牛顿每米。仪器测量的是力，接触角假设来自探针与液体的实际相互作用，二者需要配合。铂板常用于形成良好润湿的测量条件，但使用之前仍应按照材料与仪器要求清洁、检查并稳定温度。若蛋白质吸附改变了板面，连续测量中的接触角也可能改变。此时，随时间漂移的力既可能来自液面吸附，也可能包含探针表面变化，换用独立探针或轮廓法对照能够帮助分辨。

实验记录应保存原始力、浸入深度、时间和温度，而不只保存最终张力。气泡附着会改变排液体积，容器壁太近可能影响弯月面，液位漂移会改变实际浸入深度。测量低浓度表面活性剂时，容器、探针与空气接触处的吸附还可能消耗一部分溶质。保持相同容器尺寸、液体体积和等待程序，能够让样品之间的比较对应同一实验问题。检查线性残差也有具体作用：若力随深度明显弯曲，简单的固定接触角与固定周长模型就需要重新检查。

## 让液滴轮廓告诉我们界面的力量

从针头缓慢悬挂一滴液体，相机得到的首先是一条明暗边界。要把边界变成张力，需要理解弯曲界面两侧为什么存在压力差。界面张力沿表面拉拽，而曲面上不同位置的拉力方向并不平行；它们合起来形成指向曲率中心的作用。液滴内部必须具有相应压力，才能与这一作用平衡。Young–Laplace关系把这种平衡写成两个相互垂直方向曲率的贡献。球面两个方向的曲率半径相同，圆柱面则有一个方向近似平直，因此仅凭一个横截面的弯曲程度判断全部压力会遗漏信息。

$$
\Delta p=\gamma\left(\frac{1}{R_1}+\frac{1}{R_2}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/388b34d468326c8df9f49910.svg) | 界面两侧压力差，Pa；球滴内压减外压。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 界面张力，N/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9cac43c0b77042679a064ee0.svg) | 第一主曲率半径，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/99a0a123eddd37514ed7e5ce.svg) | 与第一方向垂直的第二主曲率半径，m。 |

机械平衡的曲面上，两方向曲率贡献相加。单个球形界面γ=0.050 N/m、R1=R2=0.001 m时，压力差100 Pa。悬滴沿高度还满足静水压变化。

当球形界面的半径为1毫米、张力为50毫牛顿每米时，内外压力差为100帕。这里讨论的是一个液体–气体界面；肥皂泡薄膜具有内外两个界面，需要分别考虑，不能把两种对象混用。悬滴从下端向上，液体静压逐渐降低，局部曲率也随之改变。程序沿界面弧长逐点积分，把顶点附近近似圆形的轮廓延伸到更高位置，再调整张力和顶点曲率半径，使计算边界贴近观测边界。图中展示液滴下段，因为这一区域直接体现曲率与重力竞争，而针头附近还涉及具体的附着几何。

![轴对称Young–Laplace模型的悬滴下段，规定张力50 mN/m与3 μm标准差径向噪声。左为轮廓和拟合；右为径向残差。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fc217f57883ac2f46bb1f3c3.svg?v=fc217f57883a)

图 3轴对称Young–Laplace模型的悬滴下段，规定张力50 mN/m与3 μm标准差径向噪声。左为轮廓和拟合；右为径向残差。

示例规定真实张力为50毫牛顿每米、底端顶点半径为1毫米，并给轮廓坐标加入3微米量级的噪声。拟合得到张力约50.955毫牛顿每米，顶点半径约1.00059毫米，径向残差的均方根约2.56微米。两个参数对轮廓的影响并不完全独立：顶点半径控制局部曲率，张力控制重力沿高度造成多大形变。若液滴很小、几乎是球形，重力造成的变化很弱，许多张力值都可能与近似圆形轮廓相容。选择具有适当重力变形的稳定液滴，通常比单纯追求更小、更圆的液滴更有利于参数识别。

图像中的毫米尺度是计算的一部分。像素尺寸设置错误，会同时改变曲率与重力长度尺度；相机未水平放置、液滴轴线倾斜或液滴仍在振荡，也会破坏轴对称静态模型。实验时可用已知尺寸校准图像尺度，检查左右轮廓的一致性，等待运动衰减，并测定实验温度下两相密度。油中水滴使用水与油的密度差，空气中水滴常近似使用水的密度。分析结果连同残差随高度的分布一起观察：随机小幅波动与一侧持续偏离所指向的问题不同，后者更值得检查照明、边缘提取和轴线定位。

形状拟合还可以用一个简单的数量级检查来理解。曲率压力大约随张力除以液滴半径变化，而沿液滴高度的重力压力大约随密度差、重力加速度和高度的乘积变化。液滴尺寸增大时，重力相对于曲率作用增强，因此形状逐渐偏离球面。这个尺度关系也说明，知道图像中液滴有多少像素还不够，必须知道每个像素对应多长。液滴尺寸过大又可能接近脱落，轮廓在拍摄期间变化，所以应在可识别形变与稳定悬挂之间选择适合的范围。左右边界都能清晰辨认、底端顶点完整入镜、针头附近没有遮挡，是轮廓进入拟合前应直接检查的图像条件。

## 同一瓶溶液，也会有不同年龄的表面

表面活性剂分子往往包含亲水部分与疏水部分，在气液界面或油水界面上排列能够降低自由能。新鲜界面刚形成时，界面上的分子分布与长时间放置后的分布不同。分子需要从体相移动到界面，随后吸附、重新取向，某些大分子还会缓慢展开或形成相互作用网络。于是，表面张力不仅取决于配方，也取决于表面年龄。这里的年龄从这块界面生成时开始计时，与整瓶溶液放置了多久是两个变量。把一瓶放置一夜的溶液吹成新气泡，新气泡仍然只有刚形成的年龄。

$$
\gamma(a)=\gamma_{\infty}+(\gamma_0-\gamma_{\infty})e^{-a/\tau_r}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 表面年龄，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/326221aa7409b4a62fda0814.svg) | 该年龄的张力，mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/97e4157d29a2b15aac854b6c.svg) | 初始张力，72 mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd2b4bb24d7b7e6ed71658d9.svg) | 长期极限，35 mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7f4562fee555940b00253509.svg) | 规定的弛豫时间，2 s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然对数的底，无量纲。 |

指定指数弛豫教学模型，差值每经过τr缩小至原来的1/e。a=2 s时γ=48.61154 mN/m；具体吸附体系需由其动力学确定时间规律。

为清楚分离时间因素，示例指定一条由72逐渐降到35毫牛顿每米的指数曲线，时间尺度为2秒。2秒时张力约48.61毫牛顿每米，因为初始与长期值之间的差还剩约36.8%。这条曲线是演示用的弛豫模型，参数并未代表某一种指定蛋白质或清洁剂的实测吸附常数。实际吸附可受扩散、能垒、界面占据和分子构象共同控制，因而可能出现多个时间阶段。理解示例时应关注可检验的关系：在相同配方与温度下，改变观察年龄可以改变所读取的力，也可以改变形成液滴时的界面形状。

最大气泡压力法适合观察不断生成的新界面。气体从浸没的毛细管中鼓出，气泡曲率先增加到一个特征状态，再继续长大；当界面近似半球、曲率半径等于管口半径时，曲率压力达到相应最大值。总压力还包括毛细管浸入深度造成的液柱压力，因此必须扣除该项后才能与表面张力联系。改变气泡形成速度，可以访问不同表面年龄。其时间定义通常与气泡形成到达到最大压力的阶段有关，不能直接用整次气泡脱落周期替代。把动态曲线与板法、悬滴法比较时，应先匹配各自真正观察的界面年龄。

时间曲线还影响取样方式。若每次测量都把同一表面反复拉起或压缩，上一轮操作可能已经改变界面面积和分子排列；下一轮读数便不再具有相同初始条件。需要比较新鲜界面时，应规定如何重新形成界面；需要研究老化时，则应尽量减少观察过程对界面的扰动。蛋白质体系尤其值得同时记录缓冲液、盐浓度和温度，因为这些条件会改变分子的电荷状态、分子间作用与构象稳定性。重复实验的对象应是经过完整制备和等待程序的独立界面，连续读取同一表面的多个时间点则描述这一界面的演化过程。

## 浓度曲线的转折，怎样联系到分子聚集

逐步增加表面活性剂浓度，界面吸附往往使表面张力下降。达到一定范围后，继续加入的分子更容易形成胶束等聚集体，张力曲线的下降趋势可能转为较平缓的平台。胶束可想象成把疏水部分藏在内部、亲水部分朝向水的动态聚集体；分子仍在聚集体与溶液之间交换。临界胶束浓度常通过性质随浓度变化的转折估计，表面张力只是其中一种性质。温度、盐浓度、表面活性剂组成都会影响这一转折，因此一个数值必须与配方和条件一起阅读。

$$
\gamma(c)=\gamma_p+k\min\!\left[\log_{10}(c/c_*),0\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/482cc0189b34e0e766508729.svg) | 浓度c处的张力，mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 表面活性剂浓度，mmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/71a1a028a21bc2c5b0e55c55.svg) | 转折浓度，mmol/L；本例1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ea68d49e66db4eeec415924.svg) | 平台张力，35 mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 低浓度段每十倍浓度的斜率，本例−18.5 mN/m。 |

仅对无量纲比值c/c*取对数。浓度低于转折时下降，高于转折时为平台。c=0.1 mmol/L得到53.5 mN/m；构造含噪数据拟合c*≈0.98855 mmol/L。

横轴采用浓度的对数，是因为实验常跨越多个数量级。0.01、0.1、1和10毫摩尔每升在对数轴上等距，而在线性轴上前两个点几乎挤在一起。示例规定平台为35毫牛顿每米，转折浓度为1毫摩尔每升，转折之前每增加十倍浓度，张力下降18.5毫牛顿每米。因此0.1毫摩尔每升对应53.5毫牛顿每米，0.01毫摩尔每升对应72。程序在一系列候选转折位置上拟合下降段与平台，比较残差平方和，含噪数据得到约0.98855毫摩尔每升。转折位置附近的代价曲线展示哪些候选与数据更相容，避免只看到一个精确到很多位的小数。

![A为指定指数时间曲线；B与C为构造浓度系列及转折搜索；D根据IAPWS参考关系计算纯水温度曲线。前三图是教学模型，D是公开物性参考计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b3e6243fe5ddc35ba044662d.svg?v=b3e6243fe5dd)

图 4A为指定指数时间曲线；B与C为构造浓度系列及转折搜索；D根据IAPWS参考关系计算纯水温度曲线。前三图是教学模型，D是公开物性参考计算。

测量浓度系列时，低浓度样品尤其容易受到痕量杂质与容器吸附影响。配液顺序、体积误差和母液浓度都可能移动横轴；等待时间不一致又会移动纵轴。如果浓度越高的样品恰好等待越久，就把两个变量混在了一起。对于混合表面活性剂或蛋白质体系，曲线可能具有宽转变、多个过程或持续的界面重排，分段直线适合描述清晰转折的数据，不应把每一个平台都自动命名为某种单一聚集机制。增加独立的散射、荧光探针或其他聚集信息，可以把经验转折与分子结构更紧密地联系。

$$
\gamma=B\Theta^{\mu}(1+b\Theta),\qquad\Theta=1-T/T_c
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 纯水–水蒸气平衡参考张力，mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | IAPWS系数，235.8 mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4098ceb27149a2b9e1dfa022.svg) | 由临界温度定义的无量纲温度变量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 指数1.256，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 系数−0.625，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 绝对温度，K。 |
| ![Formula](https://ml-biomat.com/static/agent-math/588edc03ab9f438e1d5b1f2e.svg) | 水的临界温度，647.096 K。 |

IAPWS参考关系适用于三相点至临界点间的水–水蒸气平衡。20°C换成293.15 K，得到72.73614 mN/m。图示采用1至90°C范围。

纯水参考也需要规定温度。图中的水曲线按照IAPWS给出的水–水蒸气平衡参考关系计算，20摄氏度约为72.736毫牛顿每米。它是公开参考公式的计算结果，用来理解温度趋势与检验单位换算；实验中的水样还受到纯度、气氛、界面年龄和仪器状态影响。公式中的温度必须换成开尔文，20摄氏度对应293.15开尔文，不能把20直接代入绝对温度比值。参考曲线随升温下降，也说明比较两份只差少量张力的样品时，温度稳定和记录十分重要。

## 交互实验：把三个误差来源分开

下面的薄板使用与计算示例相同的宽度、厚度和液体密度。表面张力按照给定的时间曲线变化，三个控制量分别是表面年龄、浸入深度与接触角。先保持完全润湿和零浸入深度，改变年龄，观察张力下降怎样变成测力读数下降。再固定年龄，把板浸得更深：液体本身的指定张力没有改变，但浮力抵消了一部分向下作用。最后改变接触角，比较“直接用力除以周长”的结果与按已知条件校正后的结果。三个操作分别对应界面演化、体积排液和几何投影。

## 交互：年龄、浮力与润湿

改变一个变量，观察真实张力、测力值与直接除周长的结果。模型采用10 mm宽、0.1 mm厚的板。

[Figure: 力与深度关系](https://ml-biomat.com/tutorials/experimental-methods/p04/#P04-plot)

把年龄设为2秒、深度设为零、角度设为零时，张力约48.61毫牛顿每米，读数约0.982毫牛顿。增加深度到5毫米后，读数降低0.04905毫牛顿，但校正后的张力不变。再把接触角设为30度，毛细力还会乘上约0.866，说明两种几何因素可以同时存在。交互图中能够显示校正值，是因为模型明确知道这些输入；真实实验需要通过探针润湿、几何测量或独立实验建立相应条件。这个区别也给出了准备实验的顺序：先确定哪些变量能够控制和测量，再决定用哪条公式从信号反推出材料性质。

还可以把实验改成一个判断题：如果两个样品在零深度时读数不同，但深度曲线的斜率相同，哪些原因仍然可能存在？表面张力差和接触角差都能改变截距，因此需要控制润湿状态来分开。如果斜率也改变，应检查密度、板的实际截面、附着气泡和深度标定。把曲线的不同特征与不同物理因素对应起来，能够避免对每一次读数变化都给出同一个分子解释。对于新配方，先观察空白溶剂，再测加入单一组分的样品，最后比较完整配方，有助于找出哪一步真正改变了界面行为。

## 完整分析：让力、轮廓和浓度结果互相解释

完整程序生成三组构造观测：薄板随浸入深度变化的力、悬滴下段轮廓，以及表面张力随浓度变化的数据。它分别采用直线外推、Young–Laplace轮廓拟合和转折搜索，再把原始数据、拟合值与结果保存为表格。固定随机种子使相同环境下重复执行能够得到一致的教学结果，而输入数据中的噪声仍然保留在图里。读程序时，可以沿着“物理模型产生预测—观测与预测相减—调整参数减小差异”的顺序理解，不需要先掌握优化算法的全部数学推导。

### 完整Python：测力、液滴与浓度转折

执行三个独立拟合，保存观测和结果，并计算IAPWS水参考。

```
"""Surface-tension measurements: plate forces, pendant shape and surface age.
All measured-looking points are constructed teaching observations.
Water reference: IAPWS R1-76(2014), https://iapws.org/technical-guidance/release/Surf-H2O
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

def water_tension(temperature_c):
    tau=1-(np.asarray(temperature_c)+273.15)/647.096
    return 235.8*tau**1.256*(1-.625*tau)

def plate(gamma_mNm,theta_deg,depth_mm):
    width=.010;thickness=.0001;perimeter=2*(width+thickness)
    capillary=(gamma_mNm/1000)*perimeter*np.cos(np.deg2rad(theta_deg))
    buoyancy=1000*9.81*width*thickness*(np.asarray(depth_mm)/1000)
    return (capillary-buoyancy)*1000

def pendant(z_mm,gamma_mNm=50.,apex_radius_mm=1.):
    """Axisymmetric pendant interface: z upward from bottom apex, arc length s.
    dr/ds=cos(phi), dz/ds=sin(phi). Pressure decreases upward, giving
    dphi/ds=2/b-(Delta_rho*g/gamma)*z-sin(phi)/r.
    All numerical lengths here are mm; coefficient converts SI to mm^-2.
    """
    b=apex_radius_mm;k=1000*9.81/(gamma_mNm/1000)*1e-6;eps=1e-5
    def fun(s,y):
        r,z,phi=y
        return [np.cos(phi),np.sin(phi),2/b-k*z-np.sin(phi)/max(r,1e-10)]
    zmax=float(np.max(z_mm))+.01
    def stop(s,y):return y[1]-zmax
    stop.terminal=True;stop.direction=1
    sol=solve_ivp(fun,[eps,6*b],[eps,eps*eps/(2*b),eps/b],events=stop,max_step=.01,rtol=1e-8,atol=1e-10)
    return np.interp(z_mm,sol.y[1],sol.y[0])

def dynamic(age_s):return 35+37*np.exp(-np.asarray(age_s)/2)

def breakpoint_fit(logc,y):
    knots=np.linspace(-.5,.5,401);loss=[];coeffs=[]
    for k in knots:
        X=np.column_stack([np.ones(len(logc)),np.minimum(logc-k,0)])
        coeff=np.linalg.lstsq(X,y,rcond=None)[0];loss.append(np.sum((X@coeff-y)**2));coeffs.append(coeff)
    j=int(np.argmin(loss));return knots[j],coeffs[j],knots,np.asarray(loss)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if args.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839'
    def save(f,n):f.savefig(out/f'{n}-{args.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1804);depth=np.linspace(0,5,31);forces=plate(50,0,depth)+rng.normal(0,.003,len(depth));coeff=np.polyfit(depth,forces,1)
    fitted_gamma=coeff[1]/.0202
    z=np.linspace(.08,1.6,70);r=pendant(z);r_obs=r+rng.normal(0,.003,len(z))
    fit=least_squares(lambda p:pendant(z,p[0],p[1])-r_obs,[48,1.02],bounds=([20,.8],[90,1.2]),xtol=1e-10,ftol=1e-10,gtol=1e-10)
    gamma_fit,b_fit=fit.x;pred=pendant(z,gamma_fit,b_fit)
    logc=np.linspace(-2,1,45);c=10**logc;gamma_true=35-18.5*np.minimum(logc,0);gamma_obs=gamma_true+rng.normal(0,.3,len(c));k,bc,knots,loss=breakpoint_fit(logc,gamma_obs)
    noiseless_k,*_=breakpoint_fit(logc,gamma_true)
    summary={'plate_gamma_fit_mNm':float(fitted_gamma),'plate_intercept_mN':float(coeff[1]),'plate_slope_mN_per_mm':float(coeff[0]),
       'plate_force_50_zero_mN':float(plate(50,0,0)),'plate_force_50_5mm_mN':float(plate(50,0,5)),
       'plate_30deg_naive_mNm':float(50*np.cos(np.pi/6)),
       'pendant_gamma_fit_mNm':float(gamma_fit),'pendant_apex_radius_fit_mm':float(b_fit),
       'pendant_residual_rms_um':float(np.sqrt(np.mean((r_obs-pred)**2))*1000),
       'cmc_fit_mM':float(10**k),'cmc_noiseless_mM':float(10**noiseless_k),
       'surface_age_2s_mNm':float(dynamic(2)),'water20_mNm':float(water_tension(20)),
       'data_kind':'Constructed plate/drop/surfactant observations; IAPWS water reference calculation'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(out/'data.csv',np.column_stack([depth,forces,np.polyval(coeff,depth)]),delimiter=',',header='depth_mm,force_mN,fit_mN',comments='')
    np.savetxt(out/'pendant.csv',np.column_stack([z,r_obs,pred]),delimiter=',',header='height_above_bottom_mm,observed_radius_mm,fitted_radius_mm',comments='')
    np.savetxt(out/'concentration.csv',np.column_stack([c,gamma_obs,gamma_true]),delimiter=',',header='concentration_mM,observed_tension_mNm,specified_tension_mNm',comments='')
    fig,axs=plt.subplots(1,2,figsize=(12,4.7));a,b=axs
    a.set_xlim(0,10);a.set_ylim(0,5);a.axis('off');a.add_patch(Rectangle((.5,.8),9,3,facecolor='#d2e9eb',edgecolor=blue,lw=2));a.add_patch(Rectangle((6,.8),.22,3,color=orange))
    for x in np.linspace(1,5.5,9):a.scatter(x,2.2+.45*np.sin(x*2),s=35,color=green)
    a.annotate('',xy=(4.8,4.2),xytext=(6.1,4.2),arrowprops={'arrowstyle':'->','color':orange,'lw':2});a.text(5,4.65,tr('移动隔板，压缩受限表面','Move a barrier; compress a confined surface'),ha='center',fontsize=10)
    a.plot([2.5,2.5],[2.5,4.1],color='#455b6b');a.add_patch(Circle((2.5,2.5),.25,facecolor='white',edgecolor=blue));a.text(5,.3,tr('Pockels：控制面积与表面污染','Pockels: area and surface contamination'),ha='center',fontsize=10);a.set_title(tr('A  1891年的表面研究思想','A  Surface experiments reported in 1891'),loc='left')
    b.set_xlim(-3,3);b.set_ylim(-2.4,2.3);b.axis('off')
    for sign in [-1,1]:
        xx=np.linspace(.3,3,150);yy=.5*np.exp(-((xx-.3)/.35)**.5)
        b.fill_between(sign*xx,-2.4,yy,color='#d2e9eb');b.plot(sign*xx,yy,color=blue)
    b.add_patch(Rectangle((-.3,-1),.6,2.6,facecolor='#b0bdc5',edgecolor='#455b6b'));b.plot([0,0],[1.6,2.2],color='#455b6b')
    for x in [-.3,.3]:b.annotate('',xy=(x,-.65),xytext=(x,.45),arrowprops={'arrowstyle':'->','color':orange,'lw':2})
    b.annotate('',xy=(0,.15),xytext=(0,-1.5),arrowprops={'arrowstyle':'->','color':green,'lw':2});b.text(.7,-.65,tr('毛细力\n向下','Capillary force\ndownward'),fontsize=10);b.text(.4,-1.7,tr('浮力向上','Buoyancy upward'),fontsize=10);b.set_title(tr('B  Wilhelmy板：读出界面力','B  Wilhelmy plate: read interfacial force'),loc='left',fontsize=11);save(fig,'principle')
    fig,axs=plt.subplots(1,2,figsize=(12,4.8));a,b=axs
    a.scatter(depth,forces,color=blue,s=25,label=tr('构造观测','Constructed observations'));a.plot(depth,np.polyval(coeff,depth),color=orange,label=tr('线性拟合','Linear fit'));a.set_xlabel(tr('浸入深度 / mm','Immersion depth / mm'));a.set_ylabel(tr('扣除干板重量的力 / mN','Force after dry-weight tare / mN'));a.legend();a.set_title(tr('A  零深度截距分离浮力','A  Zero-depth intercept separates buoyancy'),loc='left')
    theta=np.linspace(0,70,200);b.plot(theta,50*np.cos(np.deg2rad(theta)),color=orange);b.axhline(50,color=green,ls='--',label=tr('规定真实张力50 mN/m','Specified true tension 50 mN/m'));b.set_xlabel(tr('实际接触角 / °','Actual contact angle / °'));b.set_ylabel(tr('假定完全润湿得到的张力 / mN/m','Tension inferred assuming complete wetting / mN/m'));b.legend(fontsize=9);b.set_title(tr('B  把接触角误当作零','B  Incorrectly treating contact angle as zero'),loc='left');fig.tight_layout();save(fig,'plate')
    fig,axs=plt.subplots(1,2,figsize=(11.5,5.5));a,b=axs
    zfull=np.linspace(0,1.8,240);rfull=pendant(zfull,gamma_fit,b_fit)
    for sign in [-1,1]:a.scatter(sign*r_obs,z,color=blue,s=13);a.plot(sign*rfull,zfull,color=orange,lw=2)
    a.set_aspect('equal');a.set_xlabel(tr('径向位置 / mm','Radial position / mm'));a.set_ylabel(tr('距底端顶点的高度 / mm','Height above bottom apex / mm'));a.set_title(tr('A  Young–Laplace：悬滴下段轮廓','A  Young–Laplace: lower pendant profile'),loc='left',fontsize=11)
    b.scatter(z,(r_obs-pred)*1000,s=20,color=blue);b.axhline(0,color='#a1abb2');b.set_xlabel(tr('距底端顶点的高度 / mm','Height above bottom apex / mm'));b.set_ylabel(tr('径向残差 / μm','Radial residual / μm'));b.set_title(tr('B  同时估计张力与顶点半径','B  Fit tension and apex radius together'),loc='left');fig.tight_layout();save(fig,'pendant')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8.7));a,b,d,e=axs.ravel();time=np.logspace(-2,2,200)
    a.semilogx(time,dynamic(time),color=blue);a.axhline(35,color=green,ls='--');a.set_xlabel(tr('表面年龄 / s','Surface age / s'));a.set_ylabel('γ / mN/m');a.set_title(tr('A  规定的动态吸附教学曲线','A  Prescribed dynamic teaching curve'),loc='left')
    b.semilogx(c,gamma_obs,'o',color=blue,ms=4);b.semilogx(c,bc[0]+bc[1]*np.minimum(logc-k,0),color=orange);b.axvline(10**k,color=green,ls='--');b.set_xlabel(tr('浓度 / mmol/L','Concentration / mmol/L'));b.set_ylabel('γ / mN/m');b.set_title(tr('B  转折与平台，构造数据','B  Break and plateau, constructed data'),loc='left')
    d.plot(10**knots,loss,color=orange);d.set_xlabel(tr('候选转折浓度 / mmol/L','Candidate break concentration / mmol/L'));d.set_ylabel(tr('残差平方和 / (mN/m)²','Residual sum of squares / (mN/m)²'));d.set_title(tr('C  检查转折选择的代价','C  Inspect the cost of breakpoint choices'),loc='left')
    temp=np.linspace(1,90,100);e.plot(temp,water_tension(temp),color=green);e.scatter([20],[water_tension(20)],color=orange);e.set_xlabel(tr('温度 / °C','Temperature / °C'));e.set_ylabel('γ / mN/m');e.set_title(tr('D  IAPWS纯水–水蒸气参考计算','D  IAPWS water–vapor reference calculation'),loc='left',fontsize=11);fig.tight_layout();save(fig,'dynamic')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

计算中还保留了无噪声的浓度系列，用来核对转折搜索能否恢复规定的1毫摩尔每升。薄板零深度与5毫米深度的结果则可直接用排液体积手算，作为独立的单位检查。这样的核对把算法误差与观测噪声分开，也让图中的小数有可追踪的物理起点。

三种分析共同说明了测量定义的重要性。薄板曲线的截距对应接触线作用，悬滴轮廓对应密度差与曲率的静态平衡，浓度转折对应指定配方下性质变化的位置。研究一份蛋白质溶液时，可先用动态张力观察界面建立的时间过程，再在匹配年龄下比较配方；若关注蛋白质最终吸附了多少、吸附层是否含水或发生重排，则需要直接观察界面层的实验。这样，张力测量就成为连接溶液配方、界面动力学与后续吸附研究的一步，而每一条曲线都能回答一个明确的物理问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Agnes Pockels historical correspondence archive](https://www.uni-kiel.de/anorg/lagaly/group/klausSchiver/pockels.pdf)

   阅读所收1891年原信，理解水槽、隔板、圆片与清洁控制。

   Historical facts paraphrased; no archive figures reproduced.
2. [KRÜSS — Surface tension](https://www.kruss-scientific.com/en/know-how/glossary/surface-tension)

   力、界面能与温度、年龄的关系。
3. [KRÜSS — Wilhelmy plate method](https://www.kruss-scientific.com/en/know-how/glossary/wilhelmy-plate-method)

   润湿周长、接触角与测力。
4. [KRÜSS — Pendant drop](https://www.kruss-scientific.com/en/know-how/glossary/pendant-drop)

   密度差、轮廓与Young–Laplace分析。
5. [KRÜSS — Surface age](https://www.kruss-scientific.com/en/know-how/glossary/surface-age)

   新界面的时间定义。
6. [KRÜSS — Bubble pressure tensiometer](https://www.kruss-scientific.com/en/know-how/glossary/bubble-pressure-tensiometer)

   最大气泡压力与动态测量。
7. [KRÜSS — Critical micelle concentration](https://www.kruss-scientific.com/en/know-how/glossary/critical-micelle-concentration-cmc-and-surfactant-concentration)

   浓度转折的测量含义。
8. [IAPWS — Revised Release on Surface Tension of Ordinary Water Substance](https://iapws.org/technical-guidance/release/Surf-H2O)

   纯水–水蒸气参考公式、参数和适用温区。
