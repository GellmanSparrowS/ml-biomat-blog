# 透射电镜：电子穿过薄片以后

Source: https://ml-biomat.com/tutorials/experimental-methods/i04/
Language: zh-CN

从一颗黑点出发，理解薄样品、投影、衍射和颗粒尺寸之间的关系。

## 一颗黑点，是颗粒、空腔，还是两件东西的重叠

把含有纳米颗粒的水滴放到透射电镜样品网上，得到的图像里常常出现许多深色小圆点。研究者希望知道它们有多大、是否团聚、内部有没有空腔，以及晶体怎样排列。这些问题看起来都可以用一张放大的照片回答，实际却对应不同的信息：颗粒轮廓来自成像对比，空腔涉及沿电子束方向的物质分布，晶体排列则需要理解电子衍射。一颗圆点为什么发黑，是进入这些问题的起点。透射电子显微镜通常简称TEM，它让电子穿过足够薄的样品，再把携带了样品信息的电子形成图像或衍射图样。

生活中可以借助影子理解透射观察。两片树叶前后错开，投到墙上的影子可能连成一片；只看影子，难以判断它们是否真的相接。TEM也把沿束流方向分布的结构投影到二维画面上，不过电子还会发生散射和波的干涉，明暗关系比普通影子丰富。这个比喻帮助我们记住投影的几何含义，却不把所有电子图像简化成黑白剪影。本篇将先解释电子怎样成像，再把制样、颗粒统计和衍射联系起来，最后通过倾转实验观察同一组三维对象为何能产生不同的二维关系。

在生物材料研究中，这种观察可以连接几个尺度。无机纳米填料的尺寸影响它们在聚合物中的分散，脂质囊泡的膜结构关系到包载方式，细胞超薄切片则呈现细胞器与材料附近的局部结构。要让图像回答问题，首先需要决定观察的是干燥颗粒、树脂包埋的截面，还是保留水合环境的冷冻薄层。它们都可以进入TEM，却经过不同的准备过程，也保留着不同的样品状态。把目标结构与制样路线对应起来，往往比先选择最高倍率更有帮助。

## 电子为什么能成为一束可以成像的波

光学显微镜用玻璃透镜改变光的传播方向，电子显微镜则利用电场和磁场控制带电电子。电压使电子获得动能，磁透镜把不同位置出发的电子重新会聚，后续透镜系统再将像放大。1931年，鲁斯卡与克诺尔的早期装置展示了串联磁透镜形成放大像的可能性；当时的倍率远低于现代电镜，但它回答了一个关键工程问题：电子束也能够完成多级成像。后来改进电子源、透镜、真空和稳定性，才逐渐把这个原理变成能观察细小结构的仪器。

电子同时具有波的性质，波长与动量有关。可以把波长理解为波形重复一次所对应的空间长度：更短的波长为辨认更细的结构提供条件。提高加速电压会提高电子动量，并缩短波长。在200 kV下，电子波长约为2.508 pm，也就是0.002508 nm。这个数字远小于可见光波长，但仪器分辨率还取决于透镜像差、机械与电气稳定性、探测器、样品厚度和电子束损伤。波长给出一项物理条件，最终图像质量由整条成像链共同决定。

$$
\lambda=\frac{h}{\sqrt{2m_e e V\left(1+\frac{eV}{2m_ec^2}\right)}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 电子波长，m；1 pm=10⁻¹² m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 普朗克常数，6.62607015×10⁻³⁴ J·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/250412b4badc287fd481e758.svg) | 电子静止质量，约9.1093837×10⁻³¹ kg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 元电荷，1.602176634×10⁻¹⁹ C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 加速电压，V；200 kV=200000 V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 真空光速，299792458 m/s。 |

电荷乘电压给出动能；分母为包含相对论修正的电子动量，波长等于普朗克常数除以动量。代入200000 V得到约2.507934×10⁻¹² m，即2.508 pm。初始动能相对加速能量可忽略。

公式中的相对论修正并不是为了使计算显得复杂。在TEM常用电压下，电子速度已达到光速的显著比例，用低速物体的动量关系会产生可见偏差。若只想理解趋势，可以先观察代码生成的电压—波长曲线：电压升高，波长缩短；若要标定衍射间距，就需要使用对应电压的准确波长。这里把从概念到数值的两步分开，是为了让每个计算都有明确用途。读者可以先掌握“电子作为波被样品散射”，再逐渐进入透镜与衍射的细节。

![原创电子光学与制样概念图。A联系1931年磁透镜多级成像；B显示明场光阑选择近轴透射电子，离轴电子被挡住；C说明20世纪80年代玻璃化制样使含水结构能够进入低温真空观察。均为非按比例原理图。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0718b66f69c0fcf5ee95c6b1.svg?v=0718b66f69c0)

图 1原创电子光学与制样概念图。A联系1931年磁透镜多级成像；B显示明场光阑选择近轴透射电子，离轴电子被挡住；C说明20世纪80年代玻璃化制样使含水结构能够进入低温真空观察。均为非按比例原理图。

透过样品的电子并不都沿原方向前进。有的偏转较小，有的偏转较大，还有的把部分能量交给样品。明场成像主要选择靠近光轴的透射束，散射出去较多的位置可能显得较暗；暗场成像则选择某一散射束，让符合相应条件的区域变亮。光阑像一道可以选择通行方向的门，改变它的位置与大小就改变哪些电子参与成像。因此，讨论一个区域“更黑”时，要同时知道成像模式、光阑、厚度和材料组成，而不是把灰度直接读作一种化学成分的含量。

## 先把样品变得可透过，再决定保留哪一种结构

电子穿过物质时会不断与原子相互作用，样品过厚就会增加多重散射，并使结构信息更难解释。TEM需要电子可透过的区域，合适厚度随材料组成、电压和观察目标变化。对树脂包埋的生物超薄切片，几十纳米至约百纳米是一类常见尺度；对致密金属或高分辨晶格成像，要求可能不同。把“薄”看作与电子传播有关的条件，比记住一个对所有材料通用的厚度数字更准确。制样过程中还要考虑支撑膜、样品网、污染和局部厚度不均匀。

分散颗粒常通过滴加到支撑膜上观察。溶剂蒸发后，颗粒会受到液流、毛细作用和表面相互作用影响，可能聚集在液滴边缘，形成与原悬浮液不同的空间分布。若问题是溶液中颗粒是否团聚，应把干燥图像与水合状态测量联系起来，例如动态光散射或冷冻TEM；若问题是无机核的形状，干燥TEM又能提供直接轮廓信息。稀释、清洗和分散步骤也会改变观察对象，记录它们能够解释为什么同一种材料在不同样品网上表现不同。

组织和细胞通常需要固定、脱水、包埋、超薄切片与对比增强。固定让部分分子结构在后续处理时保持位置，树脂提供切削支撑，超薄切片让电子能够穿过，含较重元素的染色剂则增强某些结构与背景的散射差异。每一步都服务于具体困难，同时也可能引入收缩、抽提、压缩或沉淀。看到一条深色膜状边界时，要把它理解为在这条制样路线和成像条件下呈现的结构，而不是把每个黑色像素看成未经处理的原始分子分布。

负染色采用另一种思路：在小颗粒或大分子周围形成电子散射较强的背景，使轮廓更容易辨认。它适合快速观察外形和样品均一性，但干燥、铺展和染色剂分布会影响轮廓。冷冻TEM则把含水薄层快速冷却，使水形成没有长程晶格排列的玻璃态冰，随后在低温下观察。大冰晶的生长可能推动和重排样品，玻璃化的价值在于尽量保留水合结构。20世纪80年代玻璃化方法的发展，解决了真空环境与含水生物样品之间长期存在的一项矛盾，也成为后来冷冻电镜结构研究的重要基础。

保留水并不意味着样品在测量时仍像培养皿里一样活动。玻璃化把结构固定在冷冻状态，薄层厚度、气液界面、吸附取向和辐照仍会影响数据。对于柔软囊泡，可以比较不同区域的冰厚和囊泡轮廓；对于蛋白颗粒，可以检查取向分布与聚集情况。研究目标如果只是确认无机颗粒的晶格，复杂的冷冻路线未必最合适；目标若是观察水合膜结构，制样方式就成为核心条件。方法选择从所需信息出发，能够使后面的图像解释更清楚。

## 灰度承载着厚度、散射与取向的信息

电子束既提供信息，也向样品传递能量。聚合物和生物样品可能发生化学键断裂、质量损失、收缩或气泡形成；某些无机材料也会受到原子位移、加热或污染沉积影响。因此，一块区域在反复对焦后出现的细节变化，可能来自观察过程本身。可以在邻近区域完成部分对焦，在目标区域采用预定曝光，再比较首帧与后续帧的轮廓或衍射变化。这样的安排让图像的采集顺序成为理解结构稳定性的一部分，而不是只关心最后保存的那张最清晰照片。

降低曝光又会减少电子计数，使随机波动更明显。探测器把电子事件转换成数字图像，其效率、像素大小、读出方式和饱和范围影响最终信号。将总曝光分成短帧有时能够帮助校正漂移，但校正后的清晰度仍需要依靠原始信号支持。对于同一结构，可以比较早期帧与累积帧：前者剂量较低但噪声较大，后者计数较多却可能包含更多辐照变化。这个取舍解释了为什么“多照一会儿”既可能改善观察，也可能改变被观察的对象。

对于一些非晶薄样品，在相近成像条件下，更厚或散射更强的区域会把更多电子移出明场接收范围，因而可能更暗。这通常称为质量—厚度对比，其中“质量”指沿电子束路径累积的物质及其散射性质，并不是把每个像素放到天平上称重。厚度增加、元素组成改变和染色差异都可能改变信号。一个实心球的中心穿透路径较长，边缘较短，可能形成由边缘到中心的灰度变化；空心壳的路径分布又不同。这些趋势可用于提出结构解释，随后通过倾转、厚度信息或其他测量检验。

晶体还会产生强烈的取向依赖。原子排列具有重复周期，散射电子波在某些方向相互增强，形成衍射束。轻微倾转样品，就可能使某些晶粒进入或离开强衍射条件，从而显著改变明场图像的亮度。这解释了为什么相同组成的两个晶粒也可以一明一暗。对于薄片中的弯曲条纹、晶界或缺陷，衍射对比本身就是有用信号；对于单纯颗粒轮廓测量，则需要意识到局部对比变化可能影响阈值分割。

高分辨TEM中的晶格条纹还涉及透射波与散射波的相位干涉。相位可以先理解为波形进行到哪个位置：两个波峰同时到达时可能增强，波峰与波谷相遇时可能抵消。透镜离焦和像差会改变这些波的相对关系，所以亮点或暗点不总能直接一一对应某种原子。确认原子排列需要结合成像条件、晶体取向和适当的图像模拟。入门时先学会准确描述“图中出现某间距的周期条纹”，再根据衍射与结构知识判断它可能对应哪些晶面。

图像处理也会影响这种判断。提高对比度可以帮助看见较弱的结构，但饱和会丢失强度差别；平滑减少高频噪声，也可能抹去细小间隙；锐化让边缘突出，却可能在边界两侧产生人工明暗带。原始图像应与展示版本同时保存，尺寸测量基于具有明确标定和处理记录的数据。若改变平滑程度后颗粒直径明显变化，说明边界位置尚依赖处理选择，应回到信噪比、标尺和分割规则本身，而不是继续调整到看起来最整齐的结果。

## 把样品转一点，二维重叠就可能分开

设想两个半径均为12 nm的球，它们的中心沿横向相差16 nm，沿深度相差50 nm。真实中心距离约52.5 nm，两个球实际上相互分离；沿初始电子束方向观察，深度被压到同一平面，中心只相差16 nm，两个半径相加却有24 nm，因此投影轮廓重叠。此时把重叠图像直接称为“颗粒融合”，就把二维关系误当成三维关系。这个例子只用球的几何便能说明问题，不需要预先掌握电子波的数学描述。

$$
x^{\prime}=x\cos\theta+z\sin\theta,\qquad y^{\prime}=y
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eeaf78722a7e7f8494b85137.svg) | 样品原坐标，nm；z为初始束流方向的深度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ded7fb3f94b5eed0963dc345.svg) | 倾转后投影平面上的坐标，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 围绕y轴的倾转角；计算三角函数时用弧度。 |

旋转把横向和深度分量重新组合，再舍去沿新束流方向的分量。两中心横向相差16 nm、深度相差50 nm，在60°时投影间距为16×0.5+50×0.866025≈51.30 nm；三维距离仍为√(16²+50²)≈52.50 nm。

![同一对半径12 nm的教学球体，在0°、30°和60°倾转后的投影。三维中心距约52.5 nm保持不变；投影中心距随角度改变。颜色用于区分对象，不表示元素或真实TEM强度。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/33fb06c37aa2aec50715d225.svg?v=33fb06c37aa2)

图 2同一对半径12 nm的教学球体，在0°、30°和60°倾转后的投影。三维中心距约52.5 nm保持不变；投影中心距随角度改变。颜色用于区分对象，不表示元素或真实TEM强度。

倾转相当于换一个方向看同一组三维点。围绕纵向轴旋转时，原来的横向位置与深度位置会共同决定新的横向投影。对本篇两个球，倾转30°后中心投影间距约38.9 nm，倾转60°后约51.3 nm，重叠便消失。若真实对象通过颈部连接，连接在多个适当方向上应表现出相容的几何关系。两三个视角已经能帮助检验简单的投影解释，而完整三维重建需要更多角度、图像配准和合适的重建模型。

电子断层成像把一系列倾转投影组合起来恢复三维结构。可以把它想成围绕一件物体收集许多影子，再寻找能同时产生这些影子的内部形状。实验中，样品杆和几何遮挡通常限制可达角度，缺失的角度形成所谓“缺失楔”，使某些方向的信息较弱，重建对象可能沿特定方向拉长。倾转还增加电子穿过样品的有效路径长度，并累积辐照剂量。三维重建的质量因此与角度覆盖、样品厚度、漂移校正和剂量安排共同有关。

交互实验保留两个球的真实三维位置，允许你调整倾角和深度间距。左侧展示二维投影，数值同时给出真实中心距离、投影中心距离以及轮廓是否重叠。先把深度间距设为零，再增加深度间距，比较在0°观察时两种情况有多相似；随后转动视角，观察差异如何出现。这里的颜色只帮助区分两个教学对象，不代表元素或电子密度；图形展示的是投影几何，而完整TEM强度还包含前面讨论的散射与干涉。

## 转动两个球，看见隐藏的深度

半径12 nm，横向中心距16 nm。颜色帮助跟踪对象；展示投影几何。

[Figure: 两个球的投影](https://ml-biomat.com/tutorials/experimental-methods/i04/#I04-plot)

## 衍射图不是另一张照片，它记录空间周期

在成像模式下，图像位置对应样品中的位置；切换到衍射模式后，图样位置主要对应散射方向。重复排列的原子会在满足相位配合的方向产生增强的散射信号，形成斑点或环。单个取向较一致的晶体常出现离散斑点，许多不同取向的小晶粒可能组成环，无序材料则常表现为较宽的弥散散射。这里的“常”对应不同结构的典型表现，真实图样还受样品厚度、织构和选区范围影响，判断时需要结合实际采集区域。

选区电子衍射用位于像平面的选区光阑限定参与分析的样品区域，再让透镜系统把衍射平面投到探测器上。这样可以把某个区域的形貌与其晶体信息联系起来。衍射环离中心越远，意味着散射角越大；在小角近似下，较大的环半径对应较小的晶面间距。这个关系乍看与直接观察的尺寸相反，因为衍射图表示的是空间周期的倒数尺度。先分清“样品坐标”与“散射坐标”，就不容易把环直径误读成颗粒直径。

$$
rd\approx L\lambda,\qquad d\approx\frac{L\lambda}{r}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 从透射斑点中心到衍射环的半径，本例mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 晶面间距，本例nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 经过标准样品标定的有效相机长度，本例mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 对应加速电压的电子波长，本例nm。 |

这是小散射角下的相机常数关系。L与r采用同一长度单位，d与λ采用同一单位即可。200 kV时λ≈0.002507934 nm，L=500 mm，d=0.25 nm，对应r≈5.015868 mm。

以200 kV电子、500 mm有效相机长度为例，0.25 nm晶面间距对应约5.016 mm的环半径。实际仪器中的相机长度是经过透镜系统形成的有效几何量，需要用已知间距的标准样品标定；它不只是拿尺量出的样品到相机距离。一个环或一组条纹通常只能提供候选间距，晶相鉴定还应比较多条反射的相对位置、允许出现的反射和元素组成。若样品有多相重叠，先记录选区位置和各环，再结合其他信息逐步区分，比只凭一条接近的间距命名材料更可靠。

颗粒尺寸、晶粒尺寸和相干衍射尺寸也需要分别理解。一个外形完整的颗粒可能包含多个不同取向的晶粒；一个晶粒内部的缺陷又可能缩短保持相干散射的尺度。TEM轮廓测得的是投影几何，衍射峰宽反映的则与周期排列的范围及其他展宽机制有关。把两种数值放到同一张表里比较时，先写清定义，差异便可能成为理解内部结构的线索，而不是急着选择一个作为“正确尺寸”。

## 从颗粒轮廓到一份能够解释的尺寸分布

一个不完全圆形的轮廓可以用多种长度描述。最长距离强调伸长方向，短轴描述横向宽度，等效圆直径则把实际投影面积换成面积相同的圆的直径。最后一种定义适合把复杂轮廓压缩成一个可比较数字，但会舍去形状差异。两颗等效圆直径相同的颗粒仍可能分别是圆盘和细杆，因此需要根据研究问题同时保留长宽比或形状图。先说明用哪一种直径，再讨论平均值，能够让不同方法之间的比较更有意义。

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 已标定的颗粒投影面积，nm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | 具有相同面积的圆的直径，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约3.14159265，无量纲。 |

圆面积等于π乘半径平方，反过来先求半径，再乘2得到直径。面积314.159 nm²对应约20 nm；这个数描述等面积圆，不恢复轮廓的长宽比或三维体积。

测量之前先确认像素标定、边界规则以及接触颗粒如何处理。如果一个对象恰好被图像边缘截断，面积会偏小；若两个对象重叠成一个区域，面积又可能偏大。可以预先规定边界截断对象不进入单颗粒面积统计，并单独记录团聚比例；对于难以可靠分开的重叠对象，转向更稀疏区域或补充倾转观察。选择规则应在不同样品中保持一致，避免某一组只测孤立颗粒、另一组却把聚集体整体算作颗粒。

本篇构造十个直径为18、19、20、20、21、22、23、25、27、35 nm的颗粒，每个颗粒在数目平均中只投一票，得到23.0 nm。若按投影面积加权，大颗粒的权重随直径平方增加，平均值就会升高。两种平均不是互相矛盾的答案，它们分别强调“一颗随机选中的颗粒”与“随机选中的投影面积更可能来自什么尺寸”。与动态光散射等方法比较时，还需要进一步区分强度权重、水合层和反演模型，不能只把软件显示的平均直径并排摆放。

![全部由完整代码生成的教学计算。A为包含相对论修正的电子波长；B为200 kV、500 mm有效相机长度下的衍射环几何；C、D来自同一组十个指定颗粒，比较数目分布与不同加权平均。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b5e48817c855158ba3910ccb.svg?v=b5e48817c855)

图 3全部由完整代码生成的教学计算。A为包含相对论修正的电子波长；B为200 kV、500 mm有效相机长度下的衍射环几何；C、D来自同一组十个指定颗粒，比较数目分布与不同加权平均。

颗粒很多也要注意取样层级。一张图里测量数百颗颗粒，能够描述该视野内的分布；不同样品网、不同制备批次和不同区域的变化，则需要通过相应重复来观察。适合先用低倍率确定位置，再按预定规则选视野，保留分散区域与聚集区域的比例。报告中同时呈现代表性图像、测量规则、对象数量和独立样品数量，读者才能看清统计结论覆盖的是哪一级变化。对纳米材料而言，少量大颗粒或聚集体可能影响后续用途，完整分布往往比单一平均值更有价值。

## 用一套可重复计算把图像、几何和结构联系起来

完整程序生成三个双语图：电子成像与玻璃化概念图、同一对球在三个倾角下的投影，以及电压—波长、衍射环和尺寸统计组成的四联图。所有几何与颗粒尺寸都是明确给定的教学数据，程序把原始直径、投影面积和面积权重保存到表格。你可以改变球的深度间距，看看二维轮廓怎样变化；也可以把35 nm的大颗粒改成25 nm，观察数目平均和面积加权平均分别改变多少。这样可以把抽象定义转化为看得见的数值后果。

### 完整Python：投影、衍射环与尺寸分布

所有教学对象在代码中明确定义；保存双语图、逐颗粒表格和可复核数值。

```
"""TEM teaching experiment: projection ambiguity, calibration and diffraction.

All images and particle coordinates here are constructed teaching models.
Projection maps describe geometry, not a full coherent electron-optical simulation.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse,Circle

def wavelength(voltage):
    h,e,m,c=6.62607015e-34,1.602176634e-19,9.1093837139e-31,299792458.
    return h/np.sqrt(2*m*e*voltage*(1+e*voltage/(2*m*c*c)))

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(13,6),layout='constrained')
    for ax in axes:ax.axis('off');ax.set(xlim=(-3,3),ylim=(0,10))
    ax=axes[0];ax.set_title(tr('A  1931：磁透镜形成放大像','A  1931: magnetic-lens magnification'),fontsize=12)
    for y,label in [(8.8,tr('薄样品','Thin specimen')),(6.4,tr('物镜','Objective lens')),(3.8,tr('投影系统','Projector system')),(1,tr('探测器','Detector'))]:
        ax.add_patch(Rectangle((-1.4,y-.12),2.8,.24,fc=gray if y>8 else '#a9c6d1',ec=gray));ax.text(0,y+.4,label,ha='center')
    for dx in [-.9,0,.9]:ax.plot([.5,dx,-.5*1.4/2.4],[8.8,6.4,5],color=blue,lw=1.5)
    for dx in [-1,0,1]:ax.plot([-.5*1.4/2.4,dx,.5*1.4/2.4*2.8/1.2],[5,3.8,1],color=blue,lw=1.5)
    ax.text(0,.1,tr('原创电子光路概念图；不按比例','Original electron-optical concept; not to scale'),ha='center',fontsize=9)
    ax=axes[1];ax.set_title(tr('B  选择电子，改变图像对比','B  Select electrons, change contrast'),fontsize=12)
    ax.add_patch(Rectangle((-2,7),4,.3,fc='#ccbda9'));ax.text(0,8,tr('薄片散射电子','Thin section scatters electrons'),ha='center')
    ax.annotate('',(0,2),(0,7),arrowprops={'arrowstyle':'->','color':green,'lw':2})
    for end in [-1.14,1.14]:ax.annotate('',(end,4.15),(0,7),arrowprops={'arrowstyle':'->','color':red,'lw':2})
    ax.add_patch(Rectangle((-2.7,3.9),2.2,.25,fc=gray));ax.add_patch(Rectangle((.5,3.9),2.2,.25,fc=gray));ax.text(0,4.6,tr('物镜光阑','Objective aperture'),ha='center')
    ax.text(0,.7,tr('明场：主要接收近轴透射束\n散射、厚度和取向共同影响明暗','Bright field: mainly near-axis electrons\nScattering, thickness and orientation matter'),ha='center',fontsize=10)
    ax=axes[2];ax.set_title(tr('C  玻璃态冰保留水合环境','C  Vitreous ice preserves hydration'),fontsize=12)
    ax.add_patch(Rectangle((-2.5,4),5,2,fc='#dce8ec',ec=blue));rng=np.random.default_rng(44)
    for x,y in rng.uniform([-2.3,4.2],[2.3,5.8],(35,2)):ax.add_patch(Circle((x,y),.05,color=blue,alpha=.5))
    for x,y in [(-1.4,5.3),(.1,4.7),(1.5,5.2)]:ax.add_patch(Ellipse((x,y),.8,.45,angle=x*40,fc=green))
    ax.text(0,7.3,tr('20世纪80年代：玻璃化制样发展','1980s: development of vitrification'),ha='center',fontsize=10)
    ax.text(0,2.5,tr('无规则排列的水分子\n避免大冰晶重排样品','Disordered water arrangement\nAvoid large ice crystals rearranging specimens'),ha='center',fontsize=10)
    save(fig,'principle')
    pts=np.array([[-8.,0.,-25.],[8.,0.,25.]])
    def project(angle):
        a=np.deg2rad(angle);return np.column_stack([pts[:,0]*np.cos(a)+pts[:,2]*np.sin(a),pts[:,1]])
    fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
    for ax,angle in zip(axes,[0,30,60]):
        pr=project(angle)
        for i,(x,y) in enumerate(pr):ax.add_patch(Circle((x,y),12,fc=[green,red][i],alpha=.65,ec='white'))
        sep=np.linalg.norm(pr[1]-pr[0]);ax.set(xlim=(-50,50),ylim=(-35,35),xlabel=tr('投影位置 / nm','Projected position / nm'),ylabel='y / nm',title=tr(f'倾转 {angle}°：中心距 {sep:.1f} nm',f'Tilt {angle}°: centers {sep:.1f} nm'));ax.set_aspect('equal');ax.axhline(0,color=gray,lw=.6,ls=':')
    fig.suptitle(tr('相同的两个球：重叠随观察方向改变','The same two spheres: overlap changes with viewing angle'),fontsize=15)
    save(fig,'projection')
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    voltage=np.linspace(60,300,300);lam=wavelength(voltage*1000)*1e12
    axes[0,0].plot(voltage,lam,color=blue,lw=2);axes[0,0].set(xlabel=tr('加速电压 / kV','Accelerating voltage / kV'),ylabel=tr('电子波长 / pm','Electron wavelength / pm'),title=tr('A  波长很短，成像仍受透镜与样品影响','A  Short wavelength is only one ingredient'))
    ds=np.array([.2,.25,.35]);camera_mm=500.;lam_nm=wavelength(200e3)*1e9;rings=camera_mm*lam_nm/ds
    ax=axes[0,1]
    for r,d,col in zip(rings,ds,[green,blue,red]):ax.add_patch(Circle((0,0),r,fill=False,lw=2,color=col,label=f'd = {d:.2f} nm'))
    ax.plot(0,0,'o',color=gray);ax.set(xlim=(-7.5,7.5),ylim=(-7.5,7.5),xlabel=tr('屏上位置 / mm','Screen position / mm'),ylabel=tr('屏上位置 / mm','Screen position / mm'),title=tr('B  晶面间距越小，衍射环越外','B  Smaller spacings give outer rings'));ax.set_aspect('equal');ax.legend(frameon=False,fontsize=9,loc='upper left')
    diam=np.array([18,19,20,20,21,22,23,25,27,35.]);weights=diam**2
    edges=np.arange(15,41,5);axes[1,0].hist(diam,bins=edges,color=green,alpha=.8,edgecolor='white');axes[1,0].set(xlabel=tr('等效圆直径 / nm','Equivalent-circle diameter / nm'),ylabel=tr('颗粒数','Particle count'),title=tr('C  数目分布保留大颗粒尾部','C  Number distribution retains the large tail'))
    definitions=[tr('数目平均','Number mean'),tr('面积加权平均','Area-weighted mean')];means=[diam.mean(),np.average(diam,weights=weights)]
    axes[1,1].bar(definitions,means,color=[green,red],width=.55)
    for i,v in enumerate(means):axes[1,1].text(i,v+.6,f'{v:.2f} nm',ha='center')
    axes[1,1].set(ylabel=tr('平均直径 / nm','Mean diameter / nm'),ylim=(0,33),title=tr('D  权重改变，回答的问题也改变','D  Different weights answer different questions'))
    save(fig,'measurement')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['particle','diameter_nm','projected_area_nm2','area_weight']);w.writerows((i+1,d,np.pi*d*d/4,weights[i]/weights.sum()) for i,d in enumerate(diam))
    summary={'wavelength_200kV_pm':float(wavelength(200e3)*1e12),'ring_radius_d025_nm_mm':float(camera_mm*lam_nm/.25),'projected_separation_0_nm':float(np.linalg.norm(project(0)[1]-project(0)[0])),'projected_separation_60_nm':float(np.linalg.norm(project(60)[1]-project(60)[0])),'true_center_distance_nm':float(np.linalg.norm(pts[1]-pts[0])),'number_mean_nm':float(diam.mean()),'area_weighted_mean_nm':float(np.average(diam,weights=weights)),'diameter_from_area_314159_nm2':float(2*np.sqrt(314.1592653589793/np.pi)),'data_origin':'Constructed geometric and numerical teaching examples; no experimental TEM image claimed.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

使用TEM研究一个新体系时，可以先写出希望得到的量：是无机核的投影尺寸、囊泡膜的形态，还是某个局部晶体的晶面间距。随后选择保留该信息的制样路线，确定成像与衍射条件，并把所需对照安排进去。若发现异常，沿着样品状态、投影关系、散射机制和处理步骤逐层追查。透射电镜最有用的地方，是让细微结构获得可观察、可测量的表达；理解这些表达怎样形成，才能把一幅清晰图像转化成关于材料和生物结构的清楚认识。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Ernst Ruska — Nobel lecture](https://www.nobelprize.org/uploads/2018/06/ruska-lecture.pdf)

   早期磁透镜与1931年多级电子成像。

   Historical primary source; original diagram here.
2. [JEOL Bionote — TEM specimen preparation](https://www.jeol.com/applications/pdf/others/1462_en.pdf)

   超薄切片、负染色、冷冻观察与断层成像。
3. [JEOL — wavelength of electron](https://www.jeol.com/words/emterms/20121023.071258.php)

   相对论波长公式与200 kV标准数值。
4. [JEOL — selected-area diffraction](https://www.jeol.com/words/emterms/20121023.052558.php)

   选区光阑、像平面和衍射模式。
5. [EMBL — Jacques Dubochet and vitrification](https://www.embl.org/news/science/jacques-dubochet-awarded-nobel-prize-for-chemistry/)

   玻璃化发展的历史及含水样品观察。

   Institutional historical reference; original illustration.
6. [Royal Swedish Academy of Sciences — cryo-EM scientific background](https://www.nobelprize.org/uploads/2018/06/advanced-chemistryprize2017-1.pdf)

   冷冻电镜发展、辐照与三维结构的背景。

   Public scientific background; no figures reused.
