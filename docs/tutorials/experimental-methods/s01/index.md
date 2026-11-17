# 红外光谱：从分子振动读懂材料

Source: https://ml-biomat.com/tutorials/experimental-methods/s01/
Language: zh-CN

从透明薄膜的分子振动出发，读懂光谱、ATR取样和定量标定；用真实聚合物光谱与完整计算练习，把每个峰放回实验条件中。

## 1. 两张透明薄膜，为什么会有不同的“指纹”

把一片保鲜膜和一片干燥后的水凝胶放在桌上，它们可能同样透明、柔软，肉眼很难说明其中的分子有什么不同。红外光谱提供了另一种观察办法：让一束包含许多波长的红外光与样品相遇，再比较哪些波长的光减少了。分子中的某些运动会吸收特定频段的光，仪器把这些变化排成一条曲线。曲线上一个较宽的隆起、一组相邻的尖峰，或某个频段几乎没有信号，都能帮助我们判断材料包含哪些化学结构，以及这些结构所处的环境是否发生变化。

这种方法很适合回答材料研究中的具体问题。例如，制备聚合物膜时，原料中的某类官能团是否还在；胶原蛋白涂层与空白基底的光谱有什么差别；一个吸水后的样品与干燥样品相比，哪些变化来自水、哪些变化值得进一步联系到聚合物链。这里的“官能团”可以先理解为分子中经常一起出现、具有相近化学行为的一小组原子，如羟基中的氧和氢。读谱的目标是把这些结构线索组合起来，而不是看见一个峰就给整份样品贴上名称。

红外检测经历过一个很朴素的起点。1800年，赫歇尔把阳光经过棱镜分开的光带与温度计放在一起比较，发现红光以外、眼睛看不见的位置仍有升温作用。这个实验把“看不见”与“测不到”区分开来。后来的红外光谱学进一步追问：不同物质会怎样改变这部分辐射？早期逐波长测量积累了大量物质的光谱，现代仪器则通过干涉测量和计算更快地得到整段光谱。图中的两套装置分别对应发现辐射和测量分子响应这两个问题。

![从赫歇尔的分光与测温思路，到FTIR干涉仪的基本光路。左图为历史实验原理示意，温度计高度不表示历史测量值；右图的移动镜改变光程差，样品信号由探测器记录。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/caaa0c4d4a1a2aed562cfd9e.svg?v=caaa0c4d4a1a)

图 1从赫歇尔的分光与测温思路，到FTIR干涉仪的基本光路。左图为历史实验原理示意，温度计高度不表示历史测量值；右图的移动镜改变光程差，样品信号由探测器记录。

在实验室中常见的名字是FTIR，即傅里叶变换红外光谱。FTIR描述仪器获取光谱的方式；ATR，即衰减全反射，描述光如何接触样品。它们可以同时出现，因此“ATR-FTIR”并不是两种互相竞争的仪器。理解这一区别很实用：同一台FTIR可以配透射或ATR附件，而同一种材料在不同取样方式下，峰的相对强度可能不同。后面比较光谱时，我们始终把“材料是什么”与“怎样测它”放在一起考虑。

## 2. 从弹簧的节奏，理解分子为什么吸光

原子在分子中并非静止不动。两个相连原子之间的距离可以围绕平衡位置轻微变化，几个原子之间的夹角也可以摆动。把一根化学键想象成连接两个小球的弹簧，能帮助我们抓住最初的规律：连接越难拉长，来回振动通常越快；参与运动的质量越大，节奏通常越慢。真实分子中的原子共享电子，振动遵循量子力学，弹簧图像用来解释这种恢复力与惯性的竞争。它尤其适合描述平衡位置附近的小幅运动。

光也有自己的频率，表示电场每秒重复变化多少次。红外光的电场如果能够与分子的某种振动耦合，且光子的能量与两个振动态之间的能量差相符，就可能被吸收。可以把这件事类比为按合适的节奏推动秋千，同时还要把力施加在能够推动秋千的方向上：节奏匹配和作用方式都需要合适。对于红外吸收，后一条件表现为振动过程中分子的电偶极矩发生变化。电偶极矩描述正、负电荷分布的分离程度；所以“键存在”本身，并不保证它在红外中产生很强的峰。

$$
\widetilde\nu=\frac{1}{\lambda},\qquad \widetilde\nu\,[\mathrm{cm}^{-1}]=\frac{10^4}{\lambda\,[\mu\mathrm m]},\qquad \Delta E=h c_0\widetilde\nu
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | 波数，单位cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 波长；第一式与波数采用一致长度单位，第二式使用μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | 一次吸收对应的能量差，单位J。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 普朗克常数，6.62607015×10⁻³⁴ J·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | 真空光速；波数用cm⁻¹时取2.99792458×10¹⁰ cm/s。 |

一厘米含10⁴微米，因此波长10 μm对应1000 cm⁻¹。该波数的光子能量约1.986×10⁻²⁰ J。能量式描述光子能量；产生吸收还需要满足分子跃迁的耦合条件。

光谱的横轴通常采用波数，而不是我们熟悉的波长。可以把波数理解为一厘米长度里能排下多少个波：波长越短，同样长度内排下的波越多，波数也越大。中红外常用的4000到400 cm⁻¹对应2.5到25 μm。这里的微米是千分之一毫米。许多红外图习惯把较大的波数放在左边，因此从左向右看，波长越来越长、单个光子的能量越来越低。读图前确认横轴方向，能避免把峰位移动的方向说反。

$$
\mu=\frac{m_1m_2}{m_1+m_2},\qquad \widetilde\nu=\frac{1}{2\pi c_0}\sqrt{\frac{k}{\mu}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 约化质量，单位kg，将两个原子的相对运动写成一个有效质量问题。 |
| ![Formula](https://ml-biomat.com/static/agent-math/57ad720e8c13de438f8f5ea6.svg) | 两个参与模型振动的原子质量，单位kg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 键的谐振恢复力常数，单位N/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | 真空光速，取cm/s后输出波数为cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | 模型振动波数，单位cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

对近似的碳—氢双原子模型，质量分别取12 u和1 u，1 u约1.66054×10⁻²⁷ kg，约化质量为0.923 u。取k=500 N/m，波数约3030 cm⁻¹。这是解释质量与刚度趋势的谐振模型；真实聚合物振动涉及多个原子与环境。

弹簧模型还能解释同位素实验为什么有用。同位素具有相同的化学元素身份，却有不同的原子质量。把氢换成较重的氘，连接两端的电荷结构可能只小幅改变，振动中参与运动的质量却明显增加，相应振动往往移向较低波数。研究者因此能够区分重叠的分子运动。另一方面，在蛋白质这样的大分子里，一种振动常由多个原子共同参与，不能把每个峰都分配给一根完全独立的弹簧。酰胺Ⅰ带主要与肽键中的羰基伸缩有关，其形状还受到不同肽键振动之间的耦合与局部环境影响。

峰为什么有宽有窄，也可以从分子处境来理解。一个干燥聚合物中的羟基可能参与强弱不同的氢键，同类化学键周围存在一系列略有差别的环境；许多稍有不同的吸收叠在一起，就形成较宽的带。峰变宽因而值得联系到环境分布，而不仅是仪器是否“清楚”。仪器分辨率、温度、分子运动和样品组成也会共同改变峰形。后面处理数据时，我们保留宽峰，并用局部放大图检查细节，正是为了避免把有意义的形状当成背景抹掉。

## 3. 仪器怎样把一束光变成一条曲线

先考虑透射测量。仪器记录没有待测样品时的参考光强，再记录光穿过样品后的光强。两者相除，得到某个波数处剩下多少比例的光，这个比例叫透过率。参考测量帮助我们消去光源本来就有的强弱分布，以及光路和探测器对不同波数的响应。它也解释了为什么背景要在合适的时间重新采集：如果房间湿度、光路中的二氧化碳或附件状态已经改变，较早的背景就不能充分描述现在的测量条件。

$$
T(\widetilde\nu)=\frac{I(\widetilde\nu)}{I_0(\widetilde\nu)},\qquad A(\widetilde\nu)=-\log_{10}T(\widetilde\nu)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 透过率分数，无量纲；50%写作0.5。 |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 穿过样品后的光强，单位与参考光强相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 参考光强，可用相同条件下的仪器信号单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | 波数，单位cm⁻¹，提醒每个频段分别取比。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以10为底的对数，作用于无量纲比值。 |

若参考强度为1000而样品强度为500，T=0.5，A=0.30103。相同的两层各透过一半，合起来T=0.25，A=0.60206，说明相乘的透过率经对数变为相加的吸光度。这里采用透射定义；ATR的相应显示值取反射信号与背景的比。

为什么还要把透过率变成吸光度？设想同样的两层材料叠起来，每层都让一半的光通过，最后剩下的是四分之一，而不是零。透过率是逐层相乘的，取负对数以后，两个相同薄层贡献的吸光度就能相加。这为定量计算带来方便。透过率50%对应吸光度约0.301，10%对应1，1%对应2；因此吸光度每增加1，探测器接收到的相对光强会减少到原来的十分之一。很高的峰并不意味着测量一定更精确，因为此时剩余光很少，杂散光和探测噪声的影响会更加明显。

FTIR中负责编码不同波长的装置是干涉仪。一个分束器把入射光分成两条光路，一条到固定镜，另一条到移动镜，然后让它们重新相遇。移动镜改变两条路的光程差；同一波长的两束光有时加强、有时抵消，不同波长的明暗变化节奏不同。探测器先记录随光程差变化的干涉图，计算再把叠加的不同节奏分开，得到光谱。这个过程与从一段合奏声中分析不同频率有相似之处：仪器记录的是混合信号，傅里叶变换提供分辨频率成分的语言。

这里有两项常被混淆的设置。增加扫描次数，主要是把多次测量平均，以减少不相关的随机噪声；若其他条件不变，理想情况下扫描次数增加到四倍，信噪比约提高到两倍。提高光谱分辨率，则需要获得更长范围的光程差信息，用来区分相隔很近的谱带。把导出的数据插值成更多点，并不会补出原来没有测到的分辨能力。选择设置时，先考虑要区分的是宽广的聚合物吸收带，还是相距很近的细小结构，再考虑允许的测量时间和样品稳定性。

原始文件中的纵轴同样需要确认。有的文件保存百分透过率，有的保存吸光度，还有的只导出经过归一化的强度。对已经是吸光度的数值再次取负对数，会改变峰形；把50%的透过率当作数值50而非0.5输入公式，则会得到错误的吸光度。一个很有效的自查是找出纵轴的物理意义，再用50%和0.301这组数检查变换方向。保存样品光谱、背景、单位和处理步骤，后续重画图时就能知道每一个数是怎样得到的。

## 4. ATR为什么方便，又为什么特别在意接触

透射要求光穿过样品。较厚的聚合物片可能使某些频段的光几乎全部被吸收，含水样品也容易产生很强的水吸收。ATR把样品放在高折射率晶体表面，让红外光从晶体内部斜着到达界面，再返回探测器。折射率描述光在介质中传播的性质，入射角则相对于界面法线定义。在合适的角度下，界面附近的电磁场会延伸到样品一侧，样品对这一场的响应改变返回的光。固体只需与晶体充分接触，就能取得有用的光谱，因此ATR特别适合薄膜、粉末及许多软材料。

![弹簧图像连接恢复力与质量，ATR图像连接界面与取样权重。右图按实数折射率近似计算强度衰减，入射角均为45°；标记的dₚ是振幅衰减长度，强度在该距离衰减到e⁻²。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e01929f224ca60da48d3543a.svg?v=e01929f224ca)

图 2弹簧图像连接恢复力与质量，ATR图像连接界面与取样权重。右图按实数折射率近似计算强度衰减，入射角均为45°；标记的dₚ是振幅衰减长度，强度在该距离衰减到e⁻²。

要理解接触为什么重要，可以想象把一支温度探头贴在物体表面：如果中间隔着空气缝隙，读数就不再充分反映物体本身。ATR中的机制是光学的，但同样对紧密接触敏感。压头帮助固体贴合晶体；粗糙度、粉末颗粒大小和软材料变形会改变实际接触状态。不同样品的所有峰一起增强时，首先应比较接触和取样条件，再讨论化学组成。清洁晶体后的空白复测也很有用，尤其是在相邻样品含有相似聚合物时，残留薄层容易带来看似合理的峰。

$$
d_p=\frac{\lambda}{2\pi n_1\sqrt{\sin^2\theta-(n_2/n_1)^2}},\qquad \frac{|E(z)|^2}{|E(0)|^2}=\exp\!\left(-\frac{2z}{d_p}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f34c990e19a62f93d18d883f.svg) | 振幅降至1/e的深度，单位μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 真空波长，单位μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c2652c58d15d116e3ef5414c.svg) | 晶体和样品的实数折射率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 晶体内相对界面法线的入射角；计算三角函数时采用弧度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 从界面向样品内部的距离，单位μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/74335d93aebe185d8164d835.svg) | 距离z处与界面处的电场振幅，单位相同，如V/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/579aca15d6b056589d293cd9.svg) | π是圆周率，exp是以自然常数e为底的指数函数。 |

取n₁=2.4、n₂=1.5、θ=45°，1000 cm⁻¹对应λ=10 μm，得到dₚ=2.005 μm。在z=dₚ处归一化强度为exp(−2)=0.1353。该场分布使用实数折射率近似，要求sinθ>n₂/n₁；吸收较强时需完整界面光学。

公式中的穿透深度是一种特定的衰减长度：场的振幅降到界面值的1/e时，离界面有多远。光强与振幅平方相关，所以在同一个距离上，归一化强度已经降到约0.135。它不像刀片那样把样品切成“测到”和“没测到”两层，较深位置的权重逐渐减小。采用图中折射率和45°入射角，1000 cm⁻¹处的振幅衰减长度约为2.01 μm，2000 cm⁻¹处约为1.00 μm。长波长部分对应更大的衰减长度，这会影响不同谱带之间的相对强度。

这一简化计算采用实数折射率和弱吸收附近的场分布，用于理解尺度与趋势。实际ATR记录的是反射信号；强吸收、折射率随波数明显变化或接近临界角时，需要用更完整的界面光学来解释峰形。因此，对ATR样品做定量时，应当用相同晶体、接触方法、温度和组成背景建立标定。把透射中的固定光程直接填成“2 μm”，并不等于已经完成ATR定量。对很薄的涂层，还要把基底光谱一起比较，因为场会同时受到涂层和基底的影响。

## 交互实验：ATR在样品里看得多深

保持晶体折射率2.4、样品折射率1.5，改变波数与入射角。左图显示界面向内的强度衰减，右图把当前波数放到整段深度曲线上。观察较长波长与较大入射角分别怎样改变取样权重。

[Figure: ATR强度衰减与波数相关深度曲线](https://ml-biomat.com/tutorials/experimental-methods/s01/#S01-plot)

曲线采用实数折射率近似。振幅衰减长度与固定厚度的透射光程含义不同；图中的归一化强度是计算得到的取样权重示意。

交互图中先保持角度不动，把波数从1000调到2000，观察整条强度曲线怎样靠近表面，再保持波数不动改变角度。它把取样深度变成一条连续的权重曲线，而不只是一个数字。若要比较两个样品的表面涂层，这种变化可以帮助提出具体问题：现有测量更偏重靠近界面的区域，还是包含较多基底贡献？随后再结合涂层厚度和光学性质决定怎样取样，而不是单靠一个峰高完成判断。

## 5. 读一份真实聚合物光谱：先看全貌，再看局部

下面的实测示例来自OpenSpecy公开提供的“土壤中LDPE”光谱。LDPE是低密度聚乙烯，其链结构以碳和氢为主，日常薄膜中很常见。样品包含土壤背景，正适合练习把聚合物线索与混合样品的其他贡献放在一起考虑。文件保存了1798个信号值及波数范围；图中保留发布的数值，以“原文件信号”标记纵轴，不把未完整注明的响应单位改写为浓度。我们用它学习谱带组合与平滑的影响，下一部分再用测量定义明确的受控透射例子建立浓度标定。

![OpenSpecy公开的土壤中LDPE实测光谱（CC BY 4.0），本图重新绘制。纵轴保留原文件响应数值，色带指示碳氢伸缩及亚甲基弯曲、摇摆相关区域。局部图和残差展示平滑窗口改变峰形的方式。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/33757242d691789946ec7992.svg?v=33757242d691)

图 3OpenSpecy公开的土壤中LDPE实测光谱（CC BY 4.0），本图重新绘制。纵轴保留原文件响应数值，色带指示碳氢伸缩及亚甲基弯曲、摇摆相关区域。局部图和残差展示平滑窗口改变峰形的方式。

读这张图时，先沿横轴浏览较宽的区域。羟基相关的伸缩振动通常分布在约3000至3600 cm⁻¹附近，氢键使其位置和宽度有所变化；碳氢伸缩常出现在约2800至3000 cm⁻¹。更低波数区包含许多伸缩、弯曲和耦合运动，组合起来具有较强的辨识性，因此常被称为指纹区。本例在约2915与2848 cm⁻¹处有明显的碳氢伸缩相关峰，较低波数的亚甲基弯曲和摇摆区提供进一步线索。图中色带帮助定位这些区域；土壤背景的其他贡献要与聚乙烯的多条谱带一起比较。把多个谱带、样品的已知化学组成以及相同取样方式的参考谱放在一起，判断才会逐步收敛。

在生物材料中，水尤其需要认真对待。水的羟基吸收很强，弯曲振动又与蛋白质酰胺Ⅰ带所在区域相邻；一个湿蛋白样品的变化，可能同时包含水含量和蛋白质环境的变化。把样品干燥可以改变水贡献，却也可能改变蛋白质构象和氢键。实验设计因此应先确定要研究的是湿态材料、干态材料，还是吸水过程本身，再让对照与其保持一致。这样，样品处理就成为研究问题的一部分，而不是测量前随意做的一项准备。

图中原始曲线旁边有一条轻度平滑后的曲线。平滑像是在一小段数据里概括共同趋势，能够减少快速起伏，也会改变真实的窄结构。这里采用Savitzky–Golay方法：在一个移动窗口里拟合低阶多项式，取窗口中央的拟合值。11点窗口对应的实际波数跨度由采样间隔决定，不能只看“11”就判断处理强弱。局部放大图把11点和41点窗口放在同一坐标上，较大的窗口已经明显改变峰形；右下角画出原始值减平滑值，让被去掉的结构直接可见。

如果残差里出现沿峰两侧成组的正负结构，说明处理改变了有规律的形状，不能把它全部称为噪声。另一个常见问题是先把每条曲线最高点归一化到1，再比较峰强。这样做很适合比较谱形，却同时消去了总体强度信息。若问题是“哪个样品吸收更多”，就需要回到原来的尺度，并检查样品厚度、接触和参考信号。数据处理的每一步都应当对应一个明确任务：平滑解决随机起伏，基线处理估计背景，归一化强调相对形状，它们解决的是不同问题。

## 6. 从一个峰到一个数：怎样建立可解释的定量

设想我们在固定厚度的透射样品中研究一种吸收组分。浓度越大，光经过的同样距离内通常会遇到更多吸收单元。在组分状态、光程和仪器响应保持合适的条件下，吸光度与浓度近似成正比，这就是比尔—朗伯关系的实用起点。它允许我们用已知浓度的标准样品建立关系，再把未知样品放到同一标尺上。这里的关键不只是“拟合出一条直线”，而是标准样品与未知样品具有可比较的取样和化学环境。

$$
A=\varepsilon c\ell
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选定波数处的吸光度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 摩尔吸光系数，单位L·mol⁻¹·cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 吸收组分浓度，单位mol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dac4cdb34a25b3b90b51bf8b.svg) | 透射光程长度，单位cm。 |

若ε=120 L·mol⁻¹·cm⁻¹，光程0.005 cm，浓度0.650 mol/L，峰中心A=0.390。这是本例构造谱带的峰高关系；假设光程与吸收组分状态固定、光学响应适于线性标定。ATR需要在自己的取样条件下建立关系。

实际谱带有宽度，最高的单个点容易受到噪声、采样位置或分辨率影响。另一个选择是对固定波数区间内的谱带求面积。可以把积分理解为把曲线下方切成很多很窄的竖条，再把每条的高度乘宽度相加。求面积前先估计基线：本例选择远离中心谱带的两侧区间，用这些点拟合一条直线，作为缓慢变化的背景。随后在1660至1800 cm⁻¹的固定窗口内，对减去基线的信号做梯形积分。峰面积有cm⁻¹的单位，因为吸光度无量纲，而横轴宽度有波数单位。

$$
Q=\int_{\widetilde\nu_a}^{\widetilde\nu_b}[A(\widetilde\nu)-B(\widetilde\nu)]\,d\widetilde\nu,\qquad Q=mc+b,\qquad \widehat c=\frac{Q_u-b}{m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30efb430554daf87861b0459.svg) | 标准与未知样品的基线校正峰面积，单位cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f148cd39757f2803a55c933b.svg) | 积分窗口的低、高波数端点，本例为1660与1800 cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5ef648b1dc468d185ae3f4f4.svg) | 测得吸光度与估计基线，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c5a2c12967ff8ea7b23cc316.svg) | 一个很小的波数间隔，单位cm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 面积—浓度校准斜率，单位cm⁻¹·L/mol。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 拟合截距，单位cm⁻¹；区别于每条光谱的基线B。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa86a0645aeb94c36638b99e.svg) | 标准浓度与未知样品估计浓度，单位mol/L。 |

程序在升序波数网格上做梯形积分，拟合得到m≈27.088、b≈−0.00506。未知样品的积分结果代入反算，得到约0.6468 mol/L。固定窗口、固定基线规则及可比取样使标准与未知样品落在同一标尺。

![构造的透射标定实验：六个浓度，各含三次独立随机噪声实现。先用两侧浅黄色区间估计基线，再在固定窗口求面积。未知浓度估计为约0.647 mol/L；残差与透过率曲线帮助检查定量关系及其测量条件。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6018f81661a1d27a1776305a.svg?v=6018f81661a1)

图 4构造的透射标定实验：六个浓度，各含三次独立随机噪声实现。先用两侧浅黄色区间估计基线，再在固定窗口求面积。未知浓度估计为约0.647 mol/L；残差与透过率曲线帮助检查定量关系及其测量条件。

这组数据是明确构造的透射实验：六个浓度，每个浓度有三次独立加入随机噪声的测量，真实谱带中心为1730 cm⁻¹，峰宽和背景形式保持一致。程序得到的校准斜率约为27.09 cm⁻¹每mol/L，未知样品估计约0.647 mol/L，与生成数据时设定的0.650 mol/L接近。这里的接近让我们检查面积提取与反算流程是否正确。把同样流程用于实际测量时，应当用真正独立制备或重复取样的标准样品估计变异，而不是把同一条曲线复制三遍当作三次实验。

观察残差图，比只看决定系数更有帮助。残差是每次测得的面积减去直线预测面积；如果高浓度一端持续向下偏离，就应检查吸收过强、化学状态变化或响应饱和。如果散布随浓度明显扩大，拟合时可能需要考虑不同点的精度差异。如果三个重复值在某一浓度全部偏向同一边，还应回到配液和样品制备。一个很高的决定系数能够说明数据总体沿直线排列，却不能替代这些针对具体误差来源的检查。

误差也会在反算浓度时传递。直线的斜率越小，同样大小的面积波动会对应越大的浓度波动；未知样品远离标准范围时，直线外推又把没有实际检查过的关系带入结论。实际工作中可以把未知样品调整到标定范围内，再连同稀释倍数报告原始样品浓度。对于重叠谱带，先明确所选面积代表的是整个混合区，还是经过额外模型分离出的某个组分；这一步决定了最终的数字应该叫什么，而不只是小数点保留几位。

## 7. 把读谱、处理和核对放进一个完整程序

下面的程序包含本篇图像与数据处理的完整过程。它首先读取随示例附带的土壤中LDPE光谱，将波数按升序整理后进行平滑，再按红外领域常见的高波数在左的方式绘图。计算时的数组顺序和展示时的坐标方向可以不同：积分使用升序波数，图像则反转坐标轴。把这两件事分开很重要，否则直接对倒序横轴积分，可能只因坐标方向而得到负面积。

程序的第二部分生成标定光谱、估计每条曲线的基线、计算面积并拟合直线。输出文件不仅包含图，还保留原始构造光谱、基线、各浓度的面积、残差和计算摘要。这样读者既能从图上看变化，也能回到表格核对某个点。随机种子固定为26，因此重复运行会得到相同的教学结果；如果主动更换种子，就相当于再做一轮相同条件下、随机波动不同的模拟测量。

### 完整例子：实测读谱与受控标定

下载包附带LDPE-in-soil原始文件及其CC BY 4.0许可。运行后输出四组图、处理后的光谱、标定表格、完整构造光谱与summary.json。

```
"""FTIR: measured OpenSpecy LDPE-in-soil spectrum and a constructed calibration.

Run: python main.py --output output --language en
The bundled LDPE-in-soil signal retains its published ordinate; acquisition units were
not fully documented in that ASP file. Calibration data below are a controlled simulation.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

BLUE, RED, GOLD, GREY = '#12687b', '#be6047', '#a87d22', '#71828c'


def configure():
    plt.rcParams.update({'font.family': 'sans-serif',
        'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
        'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
        'axes.spines.top': False, 'axes.spines.right': False,
        'svg.fonttype': 'none', 'axes.unicode_minus': False,
        'savefig.facecolor': 'white', 'axes.edgecolor': '#c6d0d5'})


def penetration(wavenumber_cm, angle_deg, n_crystal=2.4, n_sample=1.5):
    """Amplitude 1/e depth in micrometres, nonabsorbing-index approximation."""
    term = np.sin(np.deg2rad(angle_deg))**2 - (n_sample/n_crystal)**2
    if np.any(term <= 0):
        raise ValueError('Use an angle above the critical angle.')
    wavelength_um = 10000 / np.asarray(wavenumber_cm)
    return wavelength_um / (2*np.pi*n_crystal*np.sqrt(term))


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    configure()
    tr = lambda zh, en: zh if language == 'zh' else en
    def save(fig, name):
        fig.savefig(output/f'{name}-{language}.svg', bbox_inches='tight')
        plt.close(fig)
    def arrow(ax, x1, y1, x2, y2, color=BLUE, lw=2):
        ax.annotate('', (x2,y2), (x1,y1), arrowprops={'arrowstyle':'->','color':color,'lw':lw})

    # A history/optics diagram, not a reconstructed historical measurement.
    fig, axes = plt.subplots(1, 2, figsize=(12.8,5.3), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0,10), ylim=(0,7)); ax.axis('off')
    ax=axes[0]
    ax.set_title(tr('A  从“看不见”到可测量：赫歇尔，1800','A  Making invisible radiation measurable: Herschel, 1800'),loc='left',pad=20)
    arrow(ax,.3,4.5,3.2,4.5,GOLD)
    ax.add_patch(Polygon([[3,3.7],[3.8,5.4],[4.6,3.7]],fc='#dceaf0',ec=BLUE))
    for j,col in enumerate(['#7164a0','#3b8fa5','#5d9c61','#c1a23f','#bd5c47']):
        ax.plot([4.1,7.1],[4.4,5.8-j*.5],color=col,lw=4)
    ax.plot([4.1,7.1],[4.4,2.8],color=RED,lw=2,ls='--')
    ax.text(.3,5,tr('阳光','Sunlight'),color=GOLD)
    ax.text(2.8,3.1,tr('棱镜分光','Prism'),color=BLUE)
    ax.text(7.3,5.7,tr('可见光','Visible light'),va='center')
    ax.text(7.3,3.8,tr('红光','Red light'),va='center')
    ax.text(7.3,2.8,tr('红外区域','Infrared'),va='center',color=RED)
    for j in range(3):
        x=6.8+j*.65; y=1.3
        ax.add_patch(Circle((x,y),.18,fc=RED,ec='none'))
        ax.add_patch(Rectangle((x-.06,y),.12,.9,fc='#f1d7cf',ec=GREY))
        ax.plot([x,x],[y,y+.35+j*.15],color=RED,lw=3)
    ax.text(.3,1.2,tr('温度计比较不同位置的升温\n图示的是实验思路，不是历史数据','Thermometers compare heating at different positions\nConceptual reconstruction, not historical data'),fontsize=10,va='center')
    ax=axes[1]
    ax.set_title(tr('B  FTIR：改变光程差，记录干涉信号','B  FTIR: vary path difference and record interference'),loc='left',pad=20)
    arrow(ax,.3,3.8,3.6,3.8,GOLD)
    ax.plot([3.5,4.2],[3.4,4.2],color=GREY,lw=5)
    arrow(ax,3.85,3.8,3.85,6,BLUE);arrow(ax,4.05,6,4.05,3.8,RED)
    ax.plot([3.1,4.8],[6.2,6.2],color=GREY,lw=5)
    arrow(ax,4.2,3.8,7.6,3.8,BLUE);arrow(ax,7.6,3.6,4.2,3.6,RED)
    ax.plot([7.8,7.8],[3.1,4.5],color=GREY,lw=5)
    arrow(ax,7.6,5,8.7,5,GREY)
    arrow(ax,3.9,3.5,3.9,1.5,RED)
    ax.add_patch(Rectangle((3.3,1.35),1.3,.45,fc='#b6d6d1',ec=BLUE))
    ax.add_patch(Rectangle((3.2,.3),1.5,.6,fc='#e7edf0',ec=GREY))
    arrow(ax,3.9,1.3,3.9,.9,RED)
    labels=[(.3,4.3,'红外源','IR source'),(.4,2.8,'分束器','Beam splitter'),(4.9,6.1,'固定镜','Fixed mirror'),(6.3,5.5,'移动镜','Moving mirror'),(5,1.5,'样品或ATR附件','Sample / ATR accessory'),(5,.55,'探测器','Detector')]
    for x,y,z,e in labels:ax.text(x,y,tr(z,e),fontsize=10)
    save(fig,'history-optics')

    fig=plt.figure(figsize=(12.8,6.8),layout='constrained')
    gs=fig.add_gridspec(2,2,width_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
    ax.set_title(tr('A  键：弹性恢复力与运动质量','A  A bond: restoring force and moving masses'),loc='left')
    for x,r,col,label in [(2,.65,BLUE,'C'),(8,.45,RED,'H')]:
        ax.add_patch(Circle((x,2.6),r,fc=col));ax.text(x,2.6,label,color='white',ha='center',va='center',fontsize=17)
    x=np.linspace(2.7,7.5,120);ax.plot(x,2.6+.23*np.sin(np.linspace(0,16*np.pi,120)),color=GREY,lw=2)
    arrow(ax,1.3,1.3,2.5,1.3);arrow(ax,8.8,1.3,7.6,1.3,RED)
    ax.text(5,.2,tr('运动时电荷分布的变化决定红外活性','Changing charge distribution determines IR activity'),ha='center',fontsize=10)
    ax=fig.add_subplot(gs[1,0]);ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
    ax.set_title(tr('B  ATR：在界面附近取样','B  ATR: sampling near an interface'),loc='left')
    ax.add_patch(Rectangle((.4,.4),9,2,fc='#dceaf0',ec='none'))
    ax.add_patch(Rectangle((.4,2.4),9,1.5,fc='#dcece3',ec='none'))
    arrow(ax,1,.6,4,2.4,GOLD);arrow(ax,4,2.4,7,.6,GOLD)
    ax.plot([4,4],[.5,4.3],ls='--',color=GREY,lw=1)
    ax.text(.7,3.3,tr('样品 n2 = 1.5','Sample n2 = 1.5'),fontsize=10)
    ax.text(.7,.1,tr('晶体 n1 = 2.4','Crystal n1 = 2.4'),fontsize=10)
    for z in np.linspace(.05,1.3,16):ax.plot([3,5],[2.4+z]*2,color=RED,alpha=float(np.exp(-z*2)),lw=3)
    ax.text(5.5,3,tr('强度随距离衰减','Intensity decays with distance'),fontsize=10)
    ax=fig.add_subplot(gs[:,1]);z=np.linspace(0,8,300)
    for wn,col in [(1000,BLUE),(2000,RED),(3000,GOLD)]:
        dp=float(penetration(wn,45));ax.plot(z,np.exp(-2*z/dp),color=col,lw=2.5,label=f'{wn} cm$^{-1}$; dp={dp:.2f} μm')
    ax.set(xlabel=tr('距晶体表面的距离 / μm','Distance from crystal surface / μm'),ylabel=tr('归一化强度 |E/E0|²','Normalized intensity |E/E0|²'),title=tr('C  同一入射角下，波长改变取样权重','C  Wavelength changes the depth weighting'),ylim=(0,1.04))
    ax.legend(fontsize=10);ax.grid(alpha=.18)
    save(fig,'vibration-atr')

    asp=np.loadtxt(Path(__file__).parent/'data/openspecy-ldpe-soil.asp')
    assert len(asp)-6 == int(asp[0])
    raw=np.c_[np.linspace(asp[1],asp[2],int(asp[0])),asp[6:]]
    raw=raw[np.argsort(raw[:,0])];wn,signal=raw.T
    smooth=savgol_filter(signal,11,2)
    fig=plt.figure(figsize=(12.8,8.0),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,:]);ax.plot(wn,signal,color=GREY,lw=1.5,label=tr('公开LDPE光谱原始数值','Published LDPE-in-soil values'));ax.plot(wn,smooth,color=BLUE,lw=1,label=tr('11点二阶平滑','11-point quadratic smoothing'))
    for lo,hi,txt,col in [(2800,3000,'C–H',RED),(1350,1500,'CH2',GOLD),(680,780,'CH2',BLUE)]:
        ax.axvspan(lo,hi,color=col,alpha=.08);ax.text((lo+hi)/2,.59,txt,color=col,ha='center',fontsize=10)
    ax.set(xlim=(4000,650),ylim=(0,.64),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('原文件信号 / 相对单位','Original-file signal / relative units'),title=tr('A  土壤中LDPE的实测光谱（OpenSpecy）','A  A published measured spectrum: LDPE-in-soil (OpenSpecy)'))
    ax.legend(loc='upper right',bbox_to_anchor=(1,.84),fontsize=10)
    ax=fig.add_subplot(gs[1,0]);keep=(wn>=2800)&(wn<=3000)
    ax.plot(wn[keep],signal[keep],'.-',color=GREY,label=tr('原数值','Original'))
    for window,col in [(11,BLUE),(41,RED)]:ax.plot(wn[keep],savgol_filter(signal,window,2)[keep],color=col,label=tr(f'{window}点窗口',f'{window}-point window'))
    ax.set(xlim=(3000,2800),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('相对信号','Relative signal'),title=tr('B  窗口变大，也会改变峰形','B  Wider smoothing changes the peak shape'));ax.legend(fontsize=9)
    ax=fig.add_subplot(gs[1,1]);ax.plot(wn,signal-smooth,color=RED,lw=1);ax.axhline(0,color=GREY,lw=1)
    ax.set(xlim=(4000,650),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('原始值 − 平滑值','Original − smoothed'),title=tr('C  检查被平滑去掉的结构','C  Inspect what smoothing removes'))
    save(fig,'ldpe-measured')

    rng=np.random.default_rng(26)
    x=np.linspace(1580,1880,601);g=np.exp(-.5*((x-1730)/18)**2)
    c=np.repeat(np.arange(6)*.2,3)
    base=.025+.00002*(x-1730)
    y=.6*c[:,None]*g+base+rng.normal(0,.003,(len(c),len(x)))
    anchors=(x<1620)|(x>1840);band=(x>=1660)&(x<=1800)
    baselines=np.array([np.polyval(np.polyfit(x[anchors],row[anchors],1),x) for row in y])
    corrected=y-baselines
    # Integrating a fixed window is less sensitive to a single noisy maximum.
    areas=np.trapezoid(corrected[:,band],x[band],axis=1)
    slope,intercept,r,p,se=linregress(c,areas)
    unknown_c=.65
    unknown=.6*unknown_c*g+base+rng.normal(0,.003,len(x))
    unknown_base=np.polyval(np.polyfit(x[anchors],unknown[anchors],1),x)
    unknown_area=float(np.trapezoid((unknown-unknown_base)[band],x[band]))
    recovered=(unknown_area-intercept)/slope
    residual=areas-(intercept+slope*c)
    # Repeated calibration specimens are independent simulated measurements.
    fig,axs=plt.subplots(2,2,figsize=(12.8,8.4),layout='constrained')
    ax=axs[0,0]
    for i,col in [(0,GREY),(9,BLUE),(15,RED)]:ax.plot(x,y[i],color=col,label=f'c = {c[i]:.1f} mol/L')
    ax.fill_between(x,0,.7,where=anchors,color=GOLD,alpha=.10)
    ax.set(xlim=(1880,1580),ylim=(0,.7),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('吸光度','Absorbance'),title=tr('A  构造实验：共同的背景与不同浓度','A  Constructed experiment: background and concentration'));ax.legend(fontsize=9)
    ax=axs[0,1];ax.scatter(c,areas,color=BLUE,s=22,label=tr('独立重复测量','Independent simulated repeats'));ax.plot([0,1],[intercept,intercept+slope],color=BLUE,lw=1.4)
    ax.scatter([recovered],[unknown_area],marker='D',s=55,color=RED,label=tr(f'未知样品估计：{recovered:.3f} mol/L',f'Unknown estimate: {recovered:.3f} mol/L'))
    ax.set(xlabel=tr('浓度 / mol/L','Concentration / mol/L'),ylabel=tr('校正后的峰面积 / cm$^{-1}$','Corrected band area / cm$^{-1}$'),title=tr('B  固定窗口的面积校准','B  Calibration using a fixed integration window'));ax.legend(fontsize=9)
    ax=axs[1,0];ax.scatter(c,residual,color=RED,s=26);ax.axhline(0,color=GREY,lw=1)
    ax.set(xlabel=tr('浓度 / mol/L','Concentration / mol/L'),ylabel=tr('面积残差 / cm$^{-1}$','Area residual / cm$^{-1}$'),title=tr('C  残差揭示直线遗漏了什么','C  Residuals inspect what the line misses'))
    ax=axs[1,1];absorb=np.linspace(0,3,200);ax.plot(absorb,100*10**(-absorb),color=BLUE,lw=2.4)
    ax.scatter([0,.30103,1,2],[100,50,10,1],color=RED,zorder=4)
    ax.set(xlabel=tr('吸光度 A','Absorbance A'),ylabel=tr('透过率 / %','Transmittance / %'),title=tr('D  高吸光度意味着探测器收到更少光','D  High absorbance leaves less light at the detector'));ax.grid(alpha=.15)
    save(fig,'calibration')
    np.savetxt(output/'ldpe-processed.csv',np.c_[wn,signal,smooth,signal-smooth],delimiter=',',header='wavenumber_cm-1,published_signal,smoothed_signal,residual',comments='')
    np.savetxt(output/'calibration.csv',np.c_[c,areas,residual],delimiter=',',header='concentration_mol_L,band_area_cm-1,residual_cm-1',comments='')
    np.savez_compressed(output/'spectra.npz',wavenumber_cm=x,absorbance=y,baseline=baselines,unknown=unknown)
    summary={'data_origin':'Measured LDPE-in-soil: OpenSpecy CC BY 4.0; calibration: constructed with seed 26',
        'ldpe_rows':int(len(wn)), 'ldpe_max_wavenumber_cm':float(wn.max()),
        'absorbance_at_half_transmission':float(-np.log10(.5)),
        'penetration_um_1000_45':float(penetration(1000,45)),
        'penetration_ratio_1000_to_2000':float(penetration(1000,45)/penetration(2000,45)),
        'calibration':{'slope':float(slope),'intercept':float(intercept),'r_squared':float(r*r),
        'unknown_true_mol_L':unknown_c,'unknown_estimated_mol_L':float(recovered),
        'residual_sd_cm-1':float(np.std(residual,ddof=2))}}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    assert len(wn)==1798 and np.all(np.diff(wn)>0)
    assert abs(recovered-unknown_c)<.01
    assert abs(summary['penetration_ratio_1000_to_2000']-2)<1e-12
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args()
    main(args.output,args.language)
```

运行后可以做两项有针对性的改动。先把平滑窗口从11改成较大的奇数，观察局部峰高、峰宽和残差共同怎样变化；再把标定数据的噪声增大，观察浓度估计和残差散布怎样变化。修改窗口时应让它小于数据点数，并保持多项式阶数小于窗口长度。比较结果时始终保留原始曲线与相同坐标范围，使视觉差异对应真实的数据处理差异，而不是纵轴自动缩放造成的印象。

## 8. 带着光谱回到材料问题

现在回到开头的透明薄膜。第一步不是急着检索一个峰，而是确认样品状态与取样方式：干膜还是湿膜，透射还是ATR，是否具有可比的厚度或接触条件。第二步检查背景、纵轴单位和原始曲线，再用整段谱带组合比较候选结构。第三步才围绕研究问题提取峰位、峰形、面积或谱带比值，并把处理过程与对照保持一致。这样的顺序使每一个数字都能回到光怎样经过样品、分子怎样响应这一条具体因果链上。

如果研究的是水凝胶表面的蛋白质吸附，可以先比较空白基底、处理后的基底和蛋白质参考样品，再查看相关谱带是否与预期一致，同时考虑水与基底的贡献。若研究的是聚合反应中某类官能团的消耗，就应关注对应谱带随时间的变化，并用稳定的取样或适当内部参考减少光程变化的影响。峰的出现或变化由此成为回答问题的一部分；其解释还要与样品组成、反应路径和其他测量相互衔接。

红外最有价值的地方，是把我们看不见的分子运动转变成可比较的实验信号。学会读它，不需要一开始就背完整张峰位表，而需要逐步掌握三件事：哪些运动可能与光耦合，仪器和取样怎样改变观察到的信号，以及处理后的数字到底代表什么。接着学习拉曼光谱时，这套思路仍然适用；不同之处在于，拉曼观察的是光散射过程中能量的变化，分子运动与光耦合的规则也随之改变。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [ESA: Space infrared astronomy comes of age](https://www.esa.int/Science_Exploration/Space_Science/Exploring_space/Space_infrared_astronomy_comes_of_age)

   赫歇尔发现红外辐射的历史背景。
2. [OpenSpecy: package tutorial](https://www.openspecy.org/pkgdown/articles/sop.html)

   开放光谱文件与预处理工作流程。

   CC BY 4.0
3. [OpenSpecy: LDPE-in-soil example data](https://github.com/wincowgerDEV/OpenSpecy-package/blob/main/inst/extdata/ftir_ldpe_soil.asp)

   本篇重新绘制与处理的实测LDPE-in-soil数据；官方library-builder教程将该样品明确标为土壤中LDPE，原文件保存在示例包中。

   OpenSpecy contributors; CC BY 4.0; replotted and smoothed. https://github.com/wincowgerDEV/OpenSpecy-package/blob/main/LICENSE.md
4. [OpenSpecy: Build a Mini Reference Library](https://www.openspecy.org/pkgdown/articles/library-builder.html)

   公开示例光谱的材料标签、文件对应与参考库组织。

   CC BY 4.0
5. [Chemistry LibreTexts: The Harmonic Oscillator and Infrared Spectra](https://chem.libretexts.org/Courses/University_of_California_Davis/UCD_Chem_110A%3A_Physical_Chemistry__I/UCD_Chem_110A%3A_Physical_Chemistry_I_%28Larsen%29/Text/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor/5.05%3A_The_Harmonic_Oscillator_and_Infrared_Spectra)

   谐振子、跃迁与红外活性的理论延伸。
6. [Shimadzu: ATR penetration depth](https://www.shimadzu.co.uk/service-support/technical-support/ftir/faq/atr.html)

   波长、角度与折射率对ATR深度尺度的影响。
7. [Bruker: Attenuated Total Reflectance](https://www.bruker.com/en/products-and-solutions/infrared-and-raman/ft-ir-routine-spectrometer/what-is-ft-ir-spectroscopy/atr-attenuated-total-reflectance.html)

   ATR取样几何、界面场与固体接触。
8. [Coblentz Society: Attenuated Total Reflection Spectroscopy](https://www.coblentz.org/field-guide/chapter9/)

   进一步理解ATR反射、折射率色散和强吸收下的峰形。
9. [SciPy: savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

   平滑窗口、多项式阶数及边界处理。
