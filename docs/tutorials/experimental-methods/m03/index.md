# 断裂实验：裂纹为什么向前走

Source: https://ml-biomat.com/tutorials/experimental-methods/m03/
Language: zh-CN

从一个小裂口走到能量释放率，读懂起裂、稳定扩展、柔度标定与凝胶撕裂。

## 一个小口子，为什么会改变整件材料的命运

一张没有缺口的塑料薄膜可能很难直接拉断，在边缘剪开一个小口后，却能沿着裂口轻松撕开。医用敷料、水凝胶贴片、柔性传感器和复合材料层板都会遇到类似问题：完整试样承受的最大拉力很高，是否意味着它在出现划伤以后仍然耐用？拉伸实验主要描述试样整体如何变形和失效，断裂实验则把注意力放在一个已经存在的裂纹上，研究它在什么条件下开始向前走，以及继续增长需要多少驱动力。两种实验相互补充，因为实际材料通常既要承担载荷，也要容忍一定程度的缺陷。

裂纹尖端把载荷重新分配到很小的区域。可以把它想成一支队伍被迫绕过道路中央的缺口：远处平均人流没有变化，缺口两端的通道却变得拥挤。材料内部发生的是应力重新分布，局部可能先出现链段拉伸、塑性变形、孔洞、纤维桥联或化学键断裂。尖端越尖锐，局部场通常越集中，但只看一个理论上无限大的尖端应力并不能直接预测整件试样何时断裂。我们还需要追问，裂纹向前推进一小步，周围材料能够提供多少能量，这一步又要消耗多少能量。

Griffith在1921年发表的研究，把裂纹扩展与弹性能量和新表面形成联系起来。1953年，Rivlin与Thomas进一步讨论橡胶的特征撕裂能，让这种能量思路进入大变形高分子材料。两段历史之间的联系很重要：玻璃与橡胶的变形方式差别很大，但都可以从“推进裂纹需要能量”出发组织实验。后来关于增韧水凝胶的研究又展示了网络桥联与周围耗散的作用。下图用原创原理图连接这些问题，不把玻璃的线弹性计算直接套给大变形凝胶。

![原创历史与机制示意：1921年Griffith裂纹能量思路、1953年Rivlin–Thomas橡胶撕裂能，以及网络桥联与周围耗散。均为原理图，非历史实验数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2a76eb0f17789687ad1ea6b8.svg?v=2a76eb0f1778)

图 1原创历史与机制示意：1921年Griffith裂纹能量思路、1953年Rivlin–Thomas橡胶撕裂能，以及网络桥联与周围耗散。均为原理图，非历史实验数据。

## 先分清能量的三个分母

机械功来自力与位移的共同作用。缓慢拉开一个线性弹簧，力从零逐渐增加，力–位移曲线下的三角形面积就是存入的弹性能。单位是焦耳，也可以用N·mm表示，后者除以一千才是焦耳。把这份功除以试样原始体积，得到单位体积的功或能量密度，常见单位是J/m³；把裂纹增长所对应的能量变化除以新增加的裂纹平面面积，则得到J/m²。拉伸曲线下面积、总断裂功与断裂能之间的差别，首先就藏在这个分母里。

$$
G=-\frac{\partial\Pi}{\partial A_c}=-\frac{1}{B}\frac{\partial\Pi}{\partial a},\qquad G\geq G_c
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 能量释放率，J/m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/51db0c676e18e6a142517806.svg) | 给定加载控制下的系统势能，J，含储能与外力功。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | 单个投影裂纹平面面积，m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 直裂纹前缘的出平面宽度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 单个前缘的裂纹长度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb6f84da03b8ec08dfd05485.svg) | 规定条件下的裂纹扩展阻力，J/m²。 |

准静态能量判据；投影裂纹面积已与产生两个表面的阻力定义配套。B=0.02 m、Δa=0.001 m、势能减少0.006 J时，G=300 J/m²。

能量释放率中的“率”指对裂纹面积的变化率，不是每秒释放多少能量。记号G表示裂纹平面增加一小块面积时，系统可提供多少机械能。这里裂纹面积按一个平面的投影面积计算，裂开后产生的上下两个自由表面已经包含在材料阻力的定义中，不能再随意多乘或少乘一个二。如果宽20 mm的裂纹前缘向前推进1 mm，新增裂纹平面面积就是20 mm²。对应可用能量减少0.006 J时，G就是300 J/m²。这个数把不同大小试样的能量变化放到了可比较的面积尺度上。

材料抵抗裂纹扩展的能量记作临界值或阻力。对于理想脆性断裂，它与形成新表面密切相关；对于增韧高分子，裂尖附近还可能消耗能量来拉出链段、打开可逆键、使颗粒周围空化或带动纤维桥联。因此，宏观测得的断裂阻力常常包含多种过程。研究它们时，既要观察裂纹，也要观察周围变形区域，不能只把所有能量都解释为断开主链化学键。不同速度、温度、含水状态和加载历史会改变这些过程参与的程度，实验条件也就成为结果含义的一部分。

可用能量还与外部加载方式有关。保持载荷时，裂纹增长让结构变软，加载点通常继续移动，外界会继续做功；保持开口不动时，外界在这段增长中不再做功，结构释放的是已经存储的能量。计算时使用系统势能，把储能与外力功放在同一个账本里。两种控制方式可以在某一瞬间给出相同的G，但裂纹再前进以后，G的变化趋势可能相反。这正是后面交互实验要展示的内容，也是为什么“达到起裂条件”与“立刻一路断到底”不是同一个判断。

## 把裂纹、载荷和开口放进同一幅图

本节先研究双悬臂梁试样。把两根细长梁沿界面连接，在一端留出裂纹，再把上下两臂向相反方向拉开，就像打开一本粘住的书。裂纹长度从加载线量到裂尖，每一臂承受大小为P的力，两臂加载点之间的相对距离变化称为开口位移。注意P不是上下两股力的数值之和；测力与位移是一对配套量。若把单臂力换成两倍，却仍使用总开口，能量和柔度计算都会失去原来的定义。

![理想双悬臂梁的配套定义：P为每臂载荷，δ为两臂加载点之间的相对开口，a从加载线量到裂尖。右图阴影为固定裂纹长度下的弹性储能。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/77ae929802934ba5783741c4.svg?v=77ae92980293)

图 2理想双悬臂梁的配套定义：P为每臂载荷，δ为两臂加载点之间的相对开口，a从加载线量到裂尖。右图阴影为固定裂纹长度下的弹性储能。

双悬臂梁特别适合说明界面或层间张开，但并不是所有材料都适合制成这种形状。硬质块体可采用紧凑拉伸或缺口弯曲试样，薄橡胶和凝胶常用缺口条带或撕裂试样。选择几何时要让裂纹沿目标区域稳定、可观察地增长，并让所采用的分析关系对应实际边界。NASA关于复杂烧蚀材料的研究曾讨论裂纹偏离中面的情况，这说明即使一种夹具在某类复合材料中很成熟，换成另一种组织结构后，裂纹路径仍需要重新检查。

缺口与裂纹也要区分。锯切或模具留下的缺口通常有有限圆角，尖端附近的应力集中与真正锐利裂纹不同。实验会根据材料采用刀片引入尖锐裂口、疲劳预裂或受控预扩展等办法，并记录起始裂纹状态。对凝胶，刀片可能挤压或撕伤邻近区域；对层合材料，脱模薄膜末端可能留下与自然扩展裂尖不同的树脂区。比较材料时，起裂方式应保持一致，并把起裂阻力与充分扩展后的阻力分别记录。这样可以辨认初始制样影响，而不把它误写成整个传播过程的材料特性。

裂纹长度通常需要图像测量。应在试样平面内标定像素尺寸，把加载点、裂尖和长度方向说清，并让图像时间与力、位移同步。表面看到的一条裂纹未必代表整个宽度内的裂纹前缘，前缘可能弯曲，内部也可能先走。可以比较两侧图像，结合断面标记或适合材料的内部观察。裂纹突然跳跃时，低帧率会把多步增长压缩成一次事件，影响起裂时刻和传播速度的判断。采样频率应由预期裂纹运动速度决定，而不只由数据文件大小决定。

## 裂纹越长，结构越软：用柔度测能量

柔度是位移除以力，可以理解为结构有多容易被打开。对于相同材料和臂厚的双悬臂梁，裂纹越长，自由弯曲的梁段越长，相同力造成的开口就越大。我们可以在几个已知裂纹长度下，用尚未推动裂纹的低载荷测量开口–力斜率，得到柔度与裂纹长度的关系。之后再把这条关系的斜率与实际载荷联系起来，计算能量释放率。这里求导不是为了增加数学复杂度，而是在问：裂纹多走一点，结构柔度会多增加多少。

$$
C(a)=\frac{\delta}{P},\qquad G=\frac{P^2}{2B}\frac{dC}{da}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 试样开口柔度，mm/N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 裂纹长度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 加载点相对开口，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 每一侧载荷的大小，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 能量释放率，N/mm；乘1000转为J/m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 裂纹前缘宽度，mm。 |

线弹性、相同加载几何与裂纹路径；导数衡量裂纹增加导致的柔度增加。P=78.881 N、B=20 mm、dC/da=0.00192857 N⁻¹得到G=0.3 N/mm。

对细长、线弹性、小挠度的理想双悬臂梁，梁弯曲给出柔度随裂纹长度三次方增加的关系。每臂厚度也以三次方进入分母，所以臂厚测量与裂纹长度同样重要。取梁模量70 GPa、宽20 mm、每臂厚2 mm、裂纹长30 mm，柔度约为0.01929 mm/N。若界面阻力规定为300 J/m²，起裂载荷约78.88 N，对应相对开口约1.521 mm。单臂只移动总开口的一半，且远小于30 mm自由梁长，这有助于判断小挠度近似是否合适。

$$
C=\frac{8a^3}{EBh^3},\qquad G=\frac{12P^2a^2}{EB^2h^3}=\frac{3P\delta}{2Ba}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 理想双悬臂梁柔度，mm/N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 加载线至裂尖距离，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 梁材料杨氏模量，N/mm²=MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 出平面宽度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 每一臂的厚度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 能量释放率，N/mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 每臂载荷大小，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 试样加载点间相对开口，mm。 |

细长线弹性梁、小挠度，忽略根部转动和剪切贡献。E=70000、B=20、h=2、a=30时C=0.0192857 mm/N；G=0.3 N/mm时P=78.881 N，δ=1.52128 mm。

真实测量可能还包含夹具和机架的变形。本例在试样柔度之外加上0.003 mm/N的固定系统柔度，再给标定数据加入少量噪声。拟合时同时识别裂纹长度的立方项和常数项，能把这两种贡献分开。常数系统柔度对裂纹长度的导数为零，因此在正确的柔度导数法中不会直接进入G；但若把横梁总位移误当试样开口，塞进理想梁的简化公式，就会高估能量。程序将两种分析并排画出，让“位移测在哪里”成为可见的数值差异。

这种理想梁关系还有明确的进一步改进方向。根部并非绝对固支时会发生转动，较短厚梁中剪切变形也会增加开口；连接块、铰链和胶层厚度则可能改变有效加载位置与局部柔度。可以采用与试样相符的修正梁理论、独立柔度标定或数值标定。选择哪一种，应由几何和可测量量决定。若材料已经发生明显塑性，加载与卸载路径不同，线性弹簧储能关系就需要替换为适合该行为的断裂分析，而不是只给同一个式子增加更多拟合参数。

![构造标定与传播记录：柔度对裂纹长度、力与开口、同步裂纹位置及传播G。橙线展示误用横梁位移导致的偏差；绿色虚线为指定300 J/m²阻力。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/beeda05611429bedae010f45.svg?v=beeda0561142)

图 3构造标定与传播记录：柔度对裂纹长度、力与开口、同步裂纹位置及传播G。橙线展示误用横梁位移导致的偏差；绿色虚线为指定300 J/m²阻力。

## 起裂以后，是停住还是继续走

构造的双悬臂梁记录在起裂前近似是一条直线：裂纹长度保持30 mm，开口增加使力增加。达到规定阻力后，裂纹开始增长。若逐渐增加开口，较长的自由梁段会变软，维持扩展所需的力反而可以下降。因此，力曲线峰值之后向下走，并不意味着实验已经结束。将同步裂纹长度放在旁边，就能看到力下降与裂纹持续前进同时发生。单独报告峰值载荷，会丢掉传播阶段以及由它得到的阻力信息。

把起裂瞬间的载荷保持不变，理想梁模型中的G随裂纹长度平方增加；裂纹向前一点，驱动力反而更大。若阻力保持常数，这种趋势会促进继续增长。改为保持起裂开口不变，载荷会随着结构变软而下降，G则随裂纹长度四次方的倒数降低，增长容易停止。两条曲线在起裂点相交，之后朝相反方向变化。所谓稳定性因此同时涉及材料阻力、试样几何和机器控制，不能只靠材料名字判断。实际机器的有限刚度与控制响应，也会影响实验处在两种理想控制之间的什么位置。

![左：相同起裂状态下保持载荷与保持开口的能量趋势。右：宽大薄板中央裂纹半长与临界应力的关系，材料参数为指定教学值。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5cac95b8c9fada828ab4810a.svg?v=5cac95b8c9fa)

图 4左：相同起裂状态下保持载荷与保持开口的能量趋势。右：宽大薄板中央裂纹半长与临界应力的关系，材料参数为指定教学值。

材料阻力也可能随着裂纹扩展而上升，形成阻力曲线，常称R曲线。例如裂纹后方逐渐形成更多纤维桥联，或尖端周围的耗散区在一段距离内发展。此时起裂值、某一扩展量下的阻力和稳定平台值可能不同，应该对应各自的裂纹增量。把它们全部称作“断裂韧性”而不说明取值位置，会让本来合理的结果难以比较。对不同尺寸试样，还要检查耗散区和桥联区是否受到边界限制，以及扩展距离是否足以形成所讨论的阶段。

$$
K_I=Y\sigma\sqrt{\pi a},\qquad G=\frac{K_I^2}{E^{\prime}},\qquad E^{\prime}=\begin{cases}E&\text{plane stress}\\ E/(1-\nu^2)&\text{plane strain}\end{cases}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd6693efed951c5ba12757b7.svg) | 模式I应力强度因子，Pa·√m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ab4817775494786b06f0b9ce.svg) | 与裂纹和试样几何匹配的无量纲修正系数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 远场拉应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 本例中央裂纹半长，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 能量释放率，J/m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | 平面状态对应的有效弹性模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 杨氏模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 泊松比，无量纲。 |

各向同性线弹性、模式I、裂尖小尺度非线性区。宽大薄板Y=1、E=3 GPa、Gc=500 J/m²、a=1 mm时临界应力21.851 MPa；a=4 mm时10.925 MPa。

对满足线弹性断裂条件的材料，另一种常用描述是应力强度因子。它把远场应力、裂纹大小和几何效应组织成裂尖场的幅度，单位通常是MPa·√m。以宽大薄板中央裂纹为例，半长1 mm、杨氏模量3 GPa、临界能量500 J/m²时，临界远场应力约21.85 MPa；半长变为4 mm，临界应力降为约10.93 MPa。裂纹长度增加四倍，承受的临界应力减半。这里的a是半长，不是整条裂纹长度，且采用薄板平面应力条件；换成厚试样的平面应变关系时，弹性换算也要随之改变。

## 柔软水凝胶怎样测断裂能

大变形凝胶的裂尖附近往往远远超出线性小应变范围，直接套用玻璃或金属的应力强度公式容易失去对应的物理场景。宽而短的纯剪切条带提供了另一条直观路线：准备同批材料的无缺口和有缺口试样，保持相同初始夹持高度。先由有缺口试样确定裂纹开始扩展时的伸长比，再在无缺口试样的加载曲线上计算达到同样伸长比所储存的能量密度。足够宽、裂纹远离边缘和夹具影响的理想几何中，能量密度乘初始高度，就得到能量释放率。

$$
W(\lambda_c)=\int_1^{\lambda_c}S(\lambda)\,d\lambda,\qquad G_c=H_0W(\lambda_c)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | 无缺口弹性条带单位原始体积储能，J/m³=Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 当前夹持高度/原始高度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c67cedfd9e1a287c0f930fba.svg) | 对应缺口试样起裂的伸长比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 以原始截面积定义的名义拉应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb6f84da03b8ec08dfd05485.svg) | 纯剪切几何中的起裂能量，J/m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f510273c694c65128635cc0b.svg) | 初始夹持高度，m。 |

足够宽的弹性纯剪切条带，裂尖远离夹具和边缘。教学Neo-Hookean平面应变条带μ=10 kPa、λc=2给出W=11250 J/m³；H0=0.01 m得到112.5 J/m²。

为什么高度会出现？把裂纹向前推进一小段，裂纹后方一条原本受拉的材料带会卸载。它的体积与初始夹持高度、试样厚度和裂纹增量成正比；新裂纹面积则只包含厚度与裂纹增量。两者相除以后留下高度。因此，这个关系来自明确的卸载区域几何，并非任何缺口拉伸都能使用的通式。“纯剪切”是这种宽条带实验的传统名称，远离裂尖的宏观变形可以理解为拉伸方向伸长、宽度方向近似受限、厚度方向相应收缩，不能把它误画成两个平面相互滑动的简单剪切。

本例另设一个完全弹性的不可压缩Neo-Hookean宽条带，剪切模量为10 kPa，初始高度10 mm，规定在伸长比2时起裂。程序对无缺口试样的名义应力–伸长比曲线积分，得到11.25 kPa的储能密度，也就是11250 J/m³；乘0.01 m高度后，断裂能为112.5 J/m²。积分横轴是无量纲伸长比，名义应力使用原始截面积，所以它们组成与原始体积对应的功。若把百分应变直接作为积分横轴而不除以100，结果会多出一百倍。

增韧凝胶可以通过多种机制提高裂纹扩展所需能量。Sun等人在2012年的双网络水凝胶研究中，把共价网络的桥联和离子网络的解缔耗散联系起来。这给实验设计一个很具体的启发：除了测一次断裂，还可以比较加载卸载滞后、恢复时间和再次加载的响应，观察耗散机制是否恢复。大滞后材料的加载功包含已经消耗的能量，不能自动全部当作可释放的弹性储能；分析时需说明采用的测量定义、加载历史和相应能量方法。图中的纯弹性示例把这一步先分开，便于读者看清积分和几何的基本关系。

![独立纯弹性凝胶条带示例：无缺口名义应力曲线的积分给出储能密度，再乘初始高度10 mm，得到缺口试样在指定临界伸长比2时的112.5 J/m²。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b5698c33c0addd7c5e2e0628.svg?v=b5698c33c0ad)

图 5独立纯弹性凝胶条带示例：无缺口名义应力曲线的积分给出储能密度，再乘初始高度10 mm，得到缺口试样在指定临界伸长比2时的112.5 J/m²。

## 把原始信号、裂纹图像和计算连起来

完整程序先构造九个裂纹长度的柔度标定，拟合立方系数与固定系统柔度，再生成随开口增长的稳定裂纹路径。观测力、开口与裂纹长度分别加入固定随机种子的噪声，保留在同一张数据表中。计算G时使用拟合柔度的导数，并与规定的300 J/m²传播阻力比较。程序还故意保留一次把横梁位移当试样开口的分析，让读者看到偏差在起裂附近最明显，随后随试样本身柔度增加而减弱。这种对照直接对应实验中的位移来源选择。

处理实测图像时，裂尖定义要前后一致。裂纹张开形成的阴影、白化区的边界、表面纹理变化和真正失去连接的位置可能并不重合。应先在几帧清晰图像中确认判据，再将相同判据用于整段记录；遇到看不清的区间，保留时间范围并补充另一视角或更合适的成像方式。长度求导会放大逐帧定位噪声，因此估计裂纹速度时要说明所用时间窗口。对本节的能量计算，准确配对同一时刻的力与裂纹长度，往往比把每一帧都标到很多小数更重要。

运行结果中，传播阶段估计G的均值约为297.22 J/m²，接近规定的300 J/m²；差别来自柔度标定和各测量通道加入的噪声。若在起裂点使用未修正的横梁位移，得到的却是约346.67 J/m²。这一对照说明，系统偏差可以明显大于曲线上的随机抖动。凝胶积分的数值结果约112.4999 J/m²，与直接积分表达式给出的112.5 J/m²一致。前一项检查测量定义，后一项检查积分与单位，它们检验的是不同环节。

误差传播也能用简单比例先估计。理想梁的G与载荷平方成正比，所以载荷统一高估1%，G约高估2.01%；固定其他量时，裂纹长度高估1%也会产生相同的平方效应。臂厚位于三次方分母，厚度高估1%会让G降低约2.94%。这些比例不是把全部不确定度简单相加的规则，而是帮助确定哪些量值得优先测准。若同一把标尺同时进入多个尺寸，误差还会相关；重复使用同一错误标定，不会产生相互抵消的独立误差。

裂纹前缘的宽度也需要与面积定义一致。界面沿斜面或曲折路径分离时，显微镜看到的真实新表面积可能大于投影面积；本节的G仍以推进方向的投影裂纹面积归一化。若研究目标是比较表面粗糙化造成的增韧，可以另行测量真实面积并说明它与投影面积的关系。保留这两个定义，才能把宏观抗裂性能与微观断面结构联系起来，而不在计算中悄悄更换分母。

### 完整Python：柔度标定、裂纹扩展和凝胶能量

保存力、开口、裂纹位置与能量计算，比较控制方式及系统柔度。

```
"""Fracture analysis: elastic DCB compliance and a separate pure-shear gel model.
All records are constructed with specified mechanics and a fixed random seed.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Ellipse

E=70000.;B=20.;h=2.;a0=30.;Gc=.3
def compliance(a):return 8*np.asarray(a)**3/(E*B*h**3)
def release(P,a):return 12*np.asarray(P)**2*np.asarray(a)**2/(E*B**2*h**3)
def force_critical(a):return np.sqrt(Gc*E*B**2*h**3/(12*np.asarray(a)**2))
def gel_stress(lam,mu=10.):return mu*(np.asarray(lam,dtype=float)-np.asarray(lam,dtype=float)**-3)
def gel_energy(lam,mu=10.):return .5*mu*(np.asarray(lam,dtype=float)**2+np.asarray(lam,dtype=float)**-2-2)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');v=p.parse_args();o=v.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if v.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{v.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{v.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1903);acal=np.linspace(25,65,9);Csys=.003;Cobs=(compliance(acal)+Csys)*(1+rng.normal(0,.007,len(acal)));kfit,cfit=np.linalg.lstsq(np.c_[acal**3,np.ones_like(acal)],Cobs,rcond=None)[0]
    d0=float(force_critical(a0)*compliance(a0));delta=np.linspace(.05,8,400);crack=np.maximum(a0,(3*E*h**3*delta**2/(16*Gc))**.25);force=delta/compliance(crack);stage=delta+Csys*force
    Pobs=force+rng.normal(0,.15,len(force));dobs=delta+rng.normal(0,.003,len(delta));aobs=crack+rng.normal(0,.12,len(crack));Gobs=Pobs**2/(2*B)*3*kfit*aobs**2*1000;Gexact=release(force,crack)*1000
    post=delta>=d0;Gmean=float(np.mean(Gobs[post]));naive=3*force*stage/(2*B*crack)*1000
    lam=np.linspace(1,2.5,601);sig=gel_stress(lam);critical=lam<=2;Wnum=float(np.trapezoid(sig[critical],lam[critical]));Ggel=Wnum*10
    summary={'analytic_C30_mm_N':float(compliance(30)),'analytic_Pinit_N':float(force_critical(30)),'analytic_delta_init_mm':d0,'specified_Gc_J_m2':300.,'fitted_compliance_cubic_mm_m2N':float(kfit),'fitted_system_compliance_mm_N':float(cfit),'mean_propagation_G_J_m2':Gmean,'naive_G_at_initiation_J_m2':float(3*force_critical(a0)*(d0+Csys*force_critical(a0))/(2*B*a0)*1000),'gel_energy_density_at_lambda2_kPa':float(gel_energy(2)),'gel_G_exact_J_m2':112.5,'gel_G_numeric_J_m2':Ggel,'critical_stress_a1mm_MPa':float(np.sqrt(500*3e9/(np.pi*.001))/1e6),'critical_stress_a4mm_MPa':float(np.sqrt(500*3e9/(np.pi*.004))/1e6)}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[delta,stage,Pobs,dobs,aobs,Gobs,Gexact,naive],delimiter=',',header='specimen_opening_mm,stage_travel_mm,observed_load_N,observed_opening_mm,observed_crack_mm,estimated_G_J_m2,exact_G_J_m2,uncorrected_stage_G_J_m2',comments='');np.savetxt(o/'compliance.csv',np.c_[acal,Cobs,compliance(acal)+Csys,kfit*acal**3+cfit],delimiter=',',header='crack_mm,observed_total_compliance_mm_N,true_total_compliance_mm_N,fitted_total_compliance_mm_N',comments='');np.savetxt(o/'gel.csv',np.c_[lam,sig,gel_energy(lam),gel_energy(lam)*10],delimiter=',',header='stretch,nominal_stress_kPa,stored_energy_kPa,pure_shear_G_J_m2',comments='')
    f,ax=plt.subplots(1,3,figsize=(13,4.7))
    for x in ax:x.set(xlim=(0,10),ylim=(0,9));x.axis('off')
    ax[0].add_patch(Rectangle((1,2),8,5,facecolor='#d6e8ef',edgecolor=blue,lw=2));ax[0].plot([3,7],[4.5,4.5],color='#233f51',lw=3)
    for xx in [2,5,8]:
        ax[0].annotate('',(xx,8),(xx,7),arrowprops={'arrowstyle':'->','color':orange});ax[0].annotate('',(xx,1),(xx,2),arrowprops={'arrowstyle':'->','color':orange})
    ax[0].text(5,.2,tr('1921  Griffith：裂纹与能量','1921  Griffith: cracks and energy'),ha='center',fontsize=10);ax[0].set_title(tr('a  小缺口改变破坏载荷','a  A flaw changes failure load'),fontsize=12)
    ax[1].add_patch(Rectangle((1,2),8,5,facecolor='#d0e9e2',edgecolor=green,lw=2));ax[1].add_patch(Polygon([(1,4),(5,4.5),(1,5)],facecolor='white'));ax[1].plot([1,5,1],[4,4.5,5],color='#233f51',lw=2);ax[1].text(5,.2,tr('1953  Rivlin–Thomas：撕裂能','1953  Rivlin–Thomas: tearing energy'),ha='center',fontsize=10);ax[1].set_title(tr('b  大变形橡胶也能算能量','b  Energy for large rubber deformation'),fontsize=11)
    for xx in np.linspace(1.5,8.5,6):
        yy=np.linspace(2,7,100);ax[2].plot(xx+.15*np.sin(yy*5),yy,color=green,lw=1.6)
    for yy in [3,4,5,6]:ax[2].plot([1.5,8.5],[yy,yy],color=blue,alpha=.6)
    ax[2].add_patch(Polygon([(1,4),(5,4.5),(1,5)],facecolor='#fbfcfc'));ax[2].plot([1,5,1],[4,4.5,5],color='#233f51',lw=2);ax[2].add_patch(Ellipse((5.7,4.5),3.2,4,facecolor=orange,alpha=.13,edgecolor=orange));ax[2].text(5,.2,tr('网络桥联与周围耗散','Network bridging and surrounding dissipation'),ha='center',fontsize=10);ax[2].set_title(tr('c  裂尖附近不只产生新表面','c  More than new surfaces at a tip'),fontsize=11);f.tight_layout();save(f,'history')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));x=ax[0];x.set(xlim=(0,11),ylim=(-3.5,3.5));x.axis('off');s=np.linspace(0,7,120);bend=(7-s)**2*(14+s)/686
    x.fill_between(s,.15+bend,.7+bend,color=blue,alpha=.3);x.fill_between(s,-.15-bend,-.7-bend,color=blue,alpha=.3);x.add_patch(Rectangle((7,-.7),3,1.4,facecolor='#d0e9e2',edgecolor=green));x.plot([0,7],[.15,-.0],color='#657f8d',ls='--');x.plot([0,7],[-.15,0],color='#657f8d',ls='--')
    for sign in [-1,1]:
        x.annotate('',(0,sign*3),(0,sign*1.7),arrowprops={'arrowstyle':'->','color':orange});x.text(.2,sign*2.5,'P',color=orange)
    x.annotate('',(0,-2.5),(7,-2.5),arrowprops={'arrowstyle':'<->','color':'#18344a'});x.text(3.5,-2.9,'a',ha='center');x.annotate('',(.5,1.15),(.5,-1.15),arrowprops={'arrowstyle':'<->'});x.text(.8,0,'δ',va='center');x.text(8.5,1.4,tr('每臂厚 h；出平面宽 B','Arm thickness h; out-of-plane width B'),ha='center',fontsize=9);x.set_title(tr('a  双悬臂梁：P 是每一侧的力','a  DCB: P is the force on each arm'),fontsize=12)
    xx=np.linspace(0,d0,100);yy=xx/compliance(a0);ax[1].fill_between(xx,0,yy,color=blue,alpha=.2);ax[1].plot(xx,yy,color=blue);ax[1].text(.45,12,tr('储能 = 三角形面积','Stored energy = triangular area'));ax[1].set(xlabel=tr('相对开口 δ / mm','Relative opening δ / mm'),ylabel=tr('载荷 P / N','Load P / N'),title=tr('b  裂纹不增长时，梁像弹簧','b  Before growth, the beams act as a spring'));f.tight_layout();save(f,'geometry')
    f,ax=plt.subplots(2,2,figsize=(12,8));fine=np.linspace(25,65,150);ax[0,0].scatter(acal,Cobs,color=orange,label=tr('构造观测','Constructed observations'));ax[0,0].plot(fine,kfit*fine**3+cfit,color=blue,label=tr('立方项 + 系统柔度','Cubic term + system compliance'));ax[0,0].set(xlabel=tr('裂纹长度 a / mm','Crack length a / mm'),ylabel=tr('总柔度 / mm/N','Total compliance / mm/N'),title=tr('a  标定裂纹与柔度','a  Calibrate crack length and compliance'));ax[0,0].legend(fontsize=9)
    ax[0,1].plot(delta,Pobs,color=blue,lw=1,label=tr('构造力观测','Constructed force observations'));ax[0,1].axvline(d0,color=orange,ls='--',label=tr('起裂','Initiation'));ax[0,1].set(xlabel=tr('试样开口 / mm','Specimen opening / mm'),ylabel=tr('载荷 / N','Load / N'),title=tr('b  力下降时裂纹仍在增长','b  Crack growth accompanies falling load'));ax[0,1].legend(fontsize=9)
    ax[1,0].plot(delta,aobs,color=green,lw=1);ax[1,0].axvline(d0,color=orange,ls='--');ax[1,0].set(xlabel=tr('试样开口 / mm','Specimen opening / mm'),ylabel=tr('裂纹长度 / mm','Crack length / mm'),title=tr('c  与力同步的裂纹记录','c  Crack record synchronised with load'))
    ax[1,1].scatter(aobs[post]-a0,Gobs[post],s=8,color=blue,alpha=.45,label=tr('柔度导数法','Compliance derivative'));ax[1,1].plot(crack[post]-a0,naive[post],color=orange,label=tr('误用横梁位移','Uncorrected stage travel'));ax[1,1].axhline(300,color=green,ls='--',label=tr('规定阻力','Specified resistance'));ax[1,1].set(xlabel=tr('裂纹增量 / mm','Crack extension / mm'),ylabel='G / J m⁻²',title=tr('d  稳定扩展的能量分析','d  Energy during stable propagation'));ax[1,1].legend(fontsize=9);f.tight_layout();save(f,'analysis')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));aa=np.linspace(20,75,250);Pc=force_critical(a0);Gload=release(Pc,aa)*1000;Gdisp=release(d0/compliance(aa),aa)*1000;ax[0].plot(aa,Gload,color=orange,label=tr('保持起裂载荷','Hold initiation load'));ax[0].plot(aa,Gdisp,color=blue,label=tr('保持起裂开口','Hold initiation opening'));ax[0].axhline(300,color=green,ls='--',label=tr('阻力300 J/m²','Resistance 300 J/m²'));ax[0].scatter([30],[300],color='#18344a');ax[0].set(xlim=(25,60),ylim=(0,1300),xlabel=tr('裂纹长度 / mm','Crack length / mm'),ylabel='G / J m⁻²',title=tr('a  加载控制决定增长趋势','a  Loading control changes the trend'));ax[0].legend(fontsize=9)
    flaw=np.linspace(.1,5,250);sc=np.sqrt(500*3e9/(np.pi*flaw/1000))/1e6;ax[1].plot(flaw,sc,color=purple);ax[1].scatter([1,4],np.sqrt(500*3e9/(np.pi*np.array([.001,.004])))/1e6,color=orange);ax[1].set(xlabel=tr('中心裂纹半长 a / mm','Centre-crack half-length a / mm'),ylabel=tr('临界远场应力 / MPa','Critical remote stress / MPa'),title=tr('b  E=3 GPa，Gc=500 J/m²，Y=1','b  E=3 GPa, Gc=500 J/m², Y=1'));f.tight_layout();save(f,'stability')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));ax[0].plot(lam,sig,color=green);ax[0].fill_between(lam[critical],0,sig[critical],color=green,alpha=.25);ax[0].axvline(2,color=orange,ls='--');ax[0].set(xlabel=tr('伸长比 λ','Stretch λ'),ylabel=tr('名义拉应力 / kPa','Nominal tensile stress / kPa'),title=tr('a  无缺口纯剪切条带的储能','a  Stored energy in an unnotched strip'));ax[0].text(1.12,2,'W(2) = 11.25 kPa')
    ax[1].plot(lam,gel_energy(lam)*10,color=blue);ax[1].axhline(112.5,color=orange,ls='--');ax[1].scatter([2],[112.5],color=orange);ax[1].set(xlabel=tr('缺口试样临界伸长比 λc','Critical stretch of notched strip λc'),ylabel=tr('能量释放率 / J m⁻²','Energy release rate / J m⁻²'),title=tr('b  H₀=10 mm，G=H₀W','b  H₀=10 mm, G=H₀W'));f.tight_layout();save(f,'gel')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

交互区将理想双悬臂梁的材料和尺寸固定，只改变裂纹长度、控制方式及所施加的载荷或开口。先把状态设在30 mm裂纹的起裂点，再选择保持载荷，观察裂纹变长后驱动力如何上升；随后保持同一初始开口，再作相同操作。图中同时显示G与规定阻力，数值给出对应载荷和开口。这里是在比较假定裂纹位置下的平衡驱动力，不是自动模拟一次真实的快速断裂，所以可以从容地逐点观察控制条件怎样改变能量关系。

## 交互：同一起裂点，两种控制方式

固定E=70 GPa、B=20 mm、每臂h=2 mm；G阻力=300 J/m²。载荷和开口输入分别用于所选控制方式。

[Figure: 能量释放率与裂纹长度](https://ml-biomat.com/tutorials/experimental-methods/m03/#M03-plot)

## 让断裂结果回答实际的耐损伤问题

准备实验时，先决定要研究材料内部开裂、两层材料脱粘，还是表面附着层剥离。它们都涉及裂纹，却可能有不同的裂纹路径和加载模式。张开型称为模式I，面内相对滑动为模式II，沿裂纹前缘方向的反向错动为模式III；实际结构可能混合出现。报告中把试样几何、受力方向和观察到的破坏位置放在一起，可以避免把界面强度、胶层内部断裂和基底破坏混成一个参数。显微断面或表面残留物有时正是区分这些路径的关键证据。

对生物材料，含水状态、加载速度和取样方向同样重要。纤维组织沿纤维与横穿纤维的开裂可能不同，干燥会同时改变尺寸与分子运动，等待时间又可能让可逆网络恢复。应让实验环境和历史对应预期使用场景，并记录裂纹扩展过程，而不是只留下断开后的照片。独立试样之间的离散性应与同一试样连续传播得到的多个数据点分开。后一类点能够描述一条阻力曲线，却不能代替独立制备或独立生物样本的重复。

最后把强度、刚度和耐裂纹扩展能力放回各自的位置。高模量材料可能很脆，伸长很多的材料也可能对缺口敏感；提高一次撕裂的能量，还需要进一步检查循环载荷下的裂纹增长。一个可解释的断裂结果应给出起始裂纹、载荷与位移定义、增长判据、分析几何、能量或应力强度单位，以及阻力取自起裂还是传播阶段。这样，数值才能帮助选择敷料边缘设计、比较网络增韧机制，或判断复合材料界面怎样抵抗已有缺陷的扩展。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Griffith — The phenomena of rupture and flow in solids (1921)](https://doi.org/10.1098/rsta.1921.0006)

   裂纹能量思路的历史文献身份。
2. [Rivlin and Thomas — Rupture of rubber I (1953)](https://imechanica.egr.uh.edu/sites/default/files/1953%20Rupture%20of%20rubber%20characteristic%20energy%20for%20tearing.pdf)

   原文前六页的撕裂能、几何和起裂判据。

   Research reading; no figures or data reused.
3. [Bower — Energy methods in fracture mechanics](https://solidmechanics.org/Text/Chapter9_4/Chapter9_4.php)

   势能、柔度导数及G与K的关系。

   Author textbook reference; original calculations and figures here.
4. [NASA — Mode-I fracture toughness with the nDCB test](https://www.nasa.gov/centers-and-facilities/nesc/mode-i-fracture-toughness-of-complex-materials-with-the-ndcb-test/)

   复杂材料中裂纹路径与传播测量的选择。

   Official technical account; no images reused.
5. [Macon — J-integral analysis of tapered double-cantilever beams](https://ntrs.nasa.gov/api/citations/20060026038/downloads/20060026038.pdf)

   原文梁柔度、根部转动、预裂和非线性分析。

   NASA-hosted technical paper; no figures or data reused.
6. [Sun et al. — Highly stretchable and tough hydrogels (2012)](https://www.nature.com/articles/nature11409)

   原始研究摘要中的共价网络桥联与离子网络耗散机制。

   Publisher abstract consulted; no figures or data reused.
