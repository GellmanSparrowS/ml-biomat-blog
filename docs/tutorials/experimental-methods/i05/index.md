# 原子力显微镜：用微小探针触摸表面

Source: https://ml-biomat.com/tutorials/experimental-methods/i05/
Language: zh-CN

让针尖形状、表面起伏和微小力各自有清楚的物理含义。

## 看起来一样光滑的表面，细胞为什么可能感到不同

两片透明聚合物薄膜，肉眼看起来都很平整，细胞却可能在上面呈现不同的铺展形态。除了化学组成，表面的细小起伏、局部软硬和分子吸附也可能参与其中。若想知道一条纳米尺度的沟槽有多深，或者一个水凝胶小区域在轻压时怎样变形，普通照片提供的信息还不够。原子力显微镜简称AFM，它把一个微小探针放在柔软悬臂末端，通过探针与表面之间的力，让悬臂发生可以检测的微小弯曲。沿表面扫描可以获得高度图，在固定位置靠近和离开则可以获得力曲线。

用手指摸过桌面，能够发现眼睛不容易看到的颗粒和划痕，这个经验有助于理解AFM。但手指有宽度，碰到柔软材料会把它压下去，移动太快还可能漏掉细小起伏；AFM也有相应问题。针尖形状影响横向轮廓，作用力影响软样品变形，反馈速度影响探针能否跟上地形。理解这些关系之后，AFM图像就不再只是漂亮的彩色山丘，而是一组与探针、样品和控制条件有关的高度与力数据。

本篇围绕两条研究路径展开：先用表面图像解释纳米起伏与粗糙度，再用力曲线理解局部压入和弹性模量。它们共享同一支悬臂，却需要不同的标定和分析。对于蛋白膜、细胞、水凝胶和涂层，AFM可以在合适的空气或液体环境下工作，这让样品状态的选择更灵活。观察前先明确需要的是干态表面形貌、水合状态高度，还是某一时间尺度下的局部力学响应，后续设置才能围绕同一个问题组织。

## 从读取电流，到读取一根微小弹簧的弯曲

1986年，比尼希、夸特和格伯提出的原子力显微镜，把扫描探针的思路从电流测量扩展到力测量。早期扫描隧道显微镜依靠探针与表面之间的隧道电流获得信息，对样品导电性有要求；AFM让表面相互作用推动悬臂弯曲，从而能研究许多不导电材料。原始装置使用带金刚石尖端的金属悬臂，并借助另一支隧道探针读取悬臂位移。这个历史细节说明，今天熟悉的激光读出并不是第一台AFM的全部构成，新的测量方法常常先借用已有工具解决最困难的读数问题。

现代AFM常用光杠杆读出：一束激光照在悬臂背面，反射到分区光电探测器上。悬臂稍微弯曲，反射角就变化，远处的光斑随之移动。仪器首先得到的是与光斑位置有关的电压信号，经灵敏度标定后才换算成悬臂末端位移。再把位移乘以悬臂弹簧常数，就得到力。这里有两次转换，一次回答“电压变化对应多少位移”，另一次回答“这样的位移对应多大力”。把两者分清，可以避免直接把软件里一条电压曲线当成已经标定的力曲线。

$$
d=S\Delta V,\qquad F=kd
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 悬臂末端偏转，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 反光杠杆位移灵敏度，m/V；本例50 nm/V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d734398b2cf2660032fdbf86.svg) | 扣除基线后的探测器电压变化，V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 悬臂弹性弯曲对应的力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 经过标定的悬臂弹簧常数，N/m。 |

先用灵敏度把电压换成位移，再按线性弹簧关系换成力。50 nm/V×0.10 V=5 nm；0.20 N/m×5×10⁻⁹ m=10⁻⁹ N=1 nN。符号方向依测量约定；这里比较力的大小。

例如，光学灵敏度为50 nm/V时，扣除基线后的0.10 V信号对应5 nm悬臂位移；若弹簧常数为0.20 N/m，力就是1.0 nN。这里的灵敏度必须采用“位移除以电压”的定义，有些软件显示的却是它的倒数，单位为V/nm。把单位写进每一步乘法，可以立即发现是否需要取倒数。压在足够硬的参照表面上时，接触后的位移主要体现悬臂弯曲，因此可帮助标定光学灵敏度；实际还需要检查倾角、接触稳定性和所用方法的适用条件。

弹簧常数可以通过热噪声、参考悬臂或其他经过验证的方法标定。热噪声法利用悬臂在热运动下的微小振动与刚度之间的关系，分析时需要考虑振动模式、探测带宽和读出方式。这里不把某一个仪器菜单当成通用步骤，而是关注标定所建立的对应关系。若更换悬臂、改变激光在悬臂上的位置或更换介质，需要检查哪些标定量随之改变。这样保存下来的力曲线，才有一条从探测器信号到物理单位的完整路径。

![原创AFM读出示意。左侧联系1986年装置中的金刚石探针、金属悬臂与隧道读出；右侧展示常用激光光杠杆和反馈思想。间距放大用于说明，不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f4de354299db92442251a46d.svg?v=f4de354299db)

图 1原创AFM读出示意。左侧联系1986年装置中的金刚石探针、金属悬臂与隧道读出；右侧展示常用激光光杠杆和反馈思想。间距放大用于说明，不按比例。

弹簧常数描述悬臂抗弯曲的程度，单位是N/m。较软的悬臂在相同力下弯得更多，适合探测较小的力；较硬的悬臂能适应更大的作用力，但微小力对应的位移更难分辨。实际选择还涉及热噪声、液体阻尼、共振频率和测量速度。生物样品常需要兼顾温和接触与稳定读出，硬质涂层则可能需要不同范围的悬臂。厂家标称值可以帮助选型，定量力测量还需要对实际使用的悬臂与环境进行合适标定。

压电扫描器把电压变化转成很小的位置变化，让探针或样品在横向和竖向移动。扫描时，反馈控制不断比较当前相互作用与目标值，再调整竖向位置。这像沿着山路行驶时不断修正车身高度：记录为了保持指定状态而做出的调整，就能描绘地形。但若控制反应太慢，陡峭边缘后会出现拖尾；若反应过强，又可能振荡。高度通道与误差信号放在一起观察，比只看高度彩色图更容易发现跟踪是否可靠。

## 怎样扫描，决定怎样接触样品

接触模式让探针持续接近或接触表面，并通过维持悬臂偏转来控制作用。它的概念直接，适合许多稳定表面，但横向拖动会产生摩擦，可能移动弱吸附分子或使柔软结构变形。动态模式则让悬臂振动，根据振幅、频率或相位等量的变化进行控制。常说的轻敲模式利用间歇接触来减少持续横向拖拽，不过合适的作用强度仍取决于振幅、设定值、探针和介质。模式名称帮助分类，真正决定样品经历什么的是具体相互作用条件。

测量蛋白吸附层时，基底应足够稳定，样品固定方式应保留待观察结构。空气中干燥可能让蛋白层收缩，液体中观察则需要考虑缓冲液、温度、漂移以及探针在液体里的运动。水凝胶表面也可能在交换溶液后逐渐溶胀，因此开始扫描前的平衡过程会影响高度与力学结果。把同一位置在不同时间的变化看成材料响应，前提是排除扫描器漂移和探针推动造成的位移。环境条件并非附在结尾的背景信息，它们是样品状态的一部分。

扫描范围、像素数和扫描速度需要一起选择。一个1 μm宽的视野记录512个采样位置，横向采样间隔约2 nm；但2 nm像素不意味着能分辨2 nm宽的对象，因为针尖和反馈也限制可见细节。扩大视野可以看见分布和代表性，小视野则适合检查局部形状。先获得稳定的大范围图，再选择有明确理由的小范围区域，能减少只展示最好看位置的偏差。比较不同样品时，尽量使用相近的扫描尺度和处理规则，否则粗糙度差异可能同时包含取样尺度变化。

正向与反向扫描是一组很有用的内部检查。如果地形真实且跟踪稳定，两者应在适当配准后给出相容的结构；若边缘拖尾方向随着扫描方向反转，就需要检查反馈、速度和探针状态。图中突然出现一条横向跳变，可能是暂时失去接触、污染粘附或行偏移。相同形状反复复制在许多不同对象上，可能提示双针尖或污染针尖。旋转扫描方向、降低速度、重新测量标准表面等操作，能够把样品结构与仪器轨迹逐步区分。

## 探针有宽度，测得的山也会变宽

针尖并不是没有尺寸的数学点。当它从一座小凸起旁经过时，侧面已经先碰到凸起，悬臂便开始抬高。因此，记录到的横向轮廓比真实凸起更宽。这个现象常被称为针尖卷积，不过从几何上说，它更接近形态学膨胀：在所有可能接触位置中，探针必须升到足够高，才能避免与表面相互穿入。它与普通光学模糊的平均运算不同。把这个区别讲清，才能理解为什么用一种简单平滑滤波并不能自动恢复真实颗粒形状。

为了看清关系，本篇构造一个高10 nm、宽20 nm的理想台阶，并用截面为抛物线的针尖扫描。针尖参数R越大，底部越钝，测得的边缘越向两侧扩展；台阶顶部高度在这个刚性几何模型中保持不变。若在一半高度处测量宽度，R为20 nm时，结果约为48.28 nm，明显大于真实20 nm。这个例子解释了为什么AFM测到的纳米颗粒横向直径常需要考虑针尖形状，而高度在适当条件下可能更接近原对象的竖向尺寸。

$$
w_{1/2}=w+2\sqrt{RH}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/facda8feca2f934f536e87e0.svg) | 测得轮廓在台阶一半高度处的宽度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 理想矩形台阶的真实宽度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 抛物线针尖顶点曲率半径参数，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 台阶高度，nm。 |

针尖截面距顶点横向s处的高度为s²/(2R)。在半高位置，每侧扩展s满足s²/(2R)=H/2，所以s=√(RH)。两侧相加得到公式。w=20、R=20、H=10 nm时，表观半高宽48.284 nm。模型为刚性几何、无粘附且完整跟踪。

![构造教学表面。A对同一矩形台阶改变抛物线针尖参数；B、C显示加入倾斜及平面调平后的高度，色标分别列出；D以同一位置的剖面和Sq比较处理前后变化。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/675e9f3a1ace7af99317d7bf.svg?v=675e9f3a1ace)

图 2构造教学表面。A对同一矩形台阶改变抛物线针尖参数；B、C显示加入倾斜及平面调平后的高度，色标分别列出；D以同一位置的剖面和Sq比较处理前后变化。

高度也会受到真实相互作用影响。柔软颗粒被压扁后，测得高度降低；表面覆着聚合物刷或吸附层时，探针可能在不同作用力下进入不同深度；凹坑太窄时，针尖无法到达底部，测得深度会偏浅。因而“高度总是准确”同样不合适。可以改变作用条件，比较高度是否稳定，并使用已知高度或形状的标准样品检查扫描器和针尖。对宽度要求很高的研究，探针表征、形状重建以及与其他显微方法的比较都会变得重要。

交互实验把针尖参数、台阶高度和真实宽度交给读者。图中同时显示真实台阶与预测测量轮廓，数字给出一半高度处的表观宽度。先固定高度，把R增大，观察横向扩展；再固定R，提高台阶高度，观察针尖侧面如何更早接触对象。这个模型忽略弹性变形、粘附和反馈延迟，目的在于单独看清几何贡献。把几何贡献与下一节的力学贡献区分开，是理解软材料AFM图像的重要一步。

## 针尖变钝，台阶会变宽多少

刚性矩形台阶与抛物线针尖的几何模型。灰色为真实轮廓，绿色为预测测量轮廓；虚线标出一半高度。

[Figure: 针尖展宽模型](https://ml-biomat.com/tutorials/experimental-methods/i05/#I05-plot)

## 粗糙度是相对于哪一个平面、哪一种尺度的起伏

AFM高度图记录的是一个区域内的数值场。颜色只是把高度换成视觉表达，同一组数据使用不同色标会呈现不同的山丘感。定量比较应读取高度单位、色标范围和横向尺度，并确认是否经过调平。样品稍微倾斜，整个视野就会从一边到另一边逐渐升高；这段宏观斜坡会增加高度离散程度，却未必是研究者所说的表面粗糙。最简单的平面调平是在数据中拟合一个平面，再从每个位置减去该平面的高度。

图中的教学表面由两个平滑周期起伏组成，随后人为加入倾斜平面。原始图把真实起伏与整体斜坡叠在一起，调平后更容易比较局部变化。处理的理由来自已知几何，而不是希望把图变得更好看。真实样品中，长波起伏可能本来就是结构的一部分；若使用过高阶多项式或逐行强力调平，可能把它一起删除。大颗粒占据视野一侧时，也会拉偏全图拟合平面，适合根据目标选择基底区域或掩膜，并保留处理前后的剖面对照。

$$
\bar z=\frac1N\sum_{i=1}^N z_i,\qquad S_q=\sqrt{\frac1N\sum_{i=1}^N(z_i-\bar z)^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | 第i个采样位置的高度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 在所选区域内的采样点索引，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 所选区域的有效采样点数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c0542cabaa03a20baa1420d.svg) | 所选区域的平均高度，nm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d2cee8f616536ae9f81ee93c.svg) | 该区域相对平均面的均方根高度起伏，nm。 |

对等面积像素求平均。−1、1、−1、1 nm四个高度的均值为0，偏差平方平均为1 nm²，开平方得到1 nm。这个分母N用于定义所测表面的面积统计；调平、掩膜和扫描范围必须一致。

均方根粗糙度Sq先求每个高度相对于平均高度的偏差，再把偏差平方、平均，最后开平方。平方让正负起伏都贡献正值，也让较大的峰谷影响更明显；开平方则把单位从nm²恢复为nm。高度为−1、1、−1、1 nm的一组点，平均为0，Sq就是1 nm。若给所有点同时加上100 nm，起伏没有改变，Sq仍为1 nm；若增加一个真实斜坡，各位置相对平均值的差异变大，Sq则会改变。这说明粗糙度与整体零点不同，却与去除的背景有关。

相同Sq并不意味着相同表面。一片由细密小起伏组成的表面，与一片由宽缓波纹组成的表面，可以具有相同高度离散程度，却给细胞、液滴或粘附界面带来不同空间结构。剖面、二维高度图和相关长度能够补充Sq；相关长度可以初步理解为表面高度相似性沿横向保持多远。扫描尺度也必须相配：在100 nm与100 μm视野得到的统计覆盖不同波长范围。描述表面时，把高度幅度与横向组织同时交代，通常比只列一个粗糙度数字更能说明材料差别。

## 从靠近与离开的一条曲线，读出压入和粘附

力曲线测量暂时停止横向扫描，让探针在某一位置靠近样品、接触、压入，再离开。仪器记录扫描器位置与悬臂偏转。靠近前的基线帮助判断零点与漂移，接触后的上升段反映悬臂弯曲与样品变形，回撤时若探针被表面吸住，可能出现负向力并在脱离时跳回。靠近曲线和回撤曲线之间的差异，可以来自粘附、黏弹性、液体阻力或分子拉伸；先辨认每个阶段发生了什么，再选择相应模型，才能让曲线参数具有明确含义。

扫描器向样品前进的距离，并不全部变成压入深度。一部分移动使悬臂弯曲，另一部分才使样品变形；还需要确定开始接触的位置。若把扫描器位移直接当作压入量，或者把接触点选得过早、过晚，模量都会发生偏移。探针半径、悬臂弹簧常数和光学灵敏度分别控制不同转换环节，也都需要与实际测量一致。用同一套曲线比较几种合理接触点和拟合区间，观察参数如何变化，可以看出结果主要受材料响应还是处理选择影响。

最常见的入门模型之一是球形压头的赫兹接触。它描述一个球压入均匀、各向同性、线弹性的厚样品，在小变形、接触范围相对球半径较小且粘附贡献可忽略的条件下，力怎样随压入深度增长。直观上，压得越深，接触区域越大，同时需要变形的材料也更多，所以力不是简单与压入深度成正比。模型给出的关系是力正比于压入深度的3/2次方；压入深度增加到原来的四倍，所需力增加到八倍。这个增长规律是接触几何与弹性变形共同作用的结果。

$$
F=\frac{4E}{3(1-\nu^2)}\sqrt{R}\,\delta^{3/2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 压入力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 样品杨氏模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | 样品泊松比，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 球形压头半径，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 扣除悬臂弯曲并确定接触零点后的样品压入深度，m。 |

假设探针相对样品足够刚硬，样品为厚、均匀、各向同性线弹性体，接触变形小且粘附可忽略。E=20000 Pa、ν=0.45、R=10⁻⁶ m、δ=50×10⁻⁹ m时，F≈3.73846×10⁻¹⁰ N，即0.374 nN。

本篇用半径1 μm的球形探针、20 kPa弹性模量和0.45泊松比构造力曲线，压入深度为2—100 nm。泊松比描述材料沿压缩方向变短时横向鼓出的程度，接近0.5表示体积变化较小。压入50 nm时，模型给出约0.374 nN的力。程序加入固定种子的微小噪声，再拟合同一模型，同时画出残差和假定探针半径变化时的模量。半径估计越大，同样的力曲线所需模量越小，这说明漂亮的拟合曲线也依赖准确的几何标定。

![构造赫兹接触数据，球半径1 μm、样品模量20 kPa、泊松比0.45。A显示带噪声数据及拟合；B显示残差；C保持曲线相同，改变拟合时假定的探针半径，揭示几何标定与模量之间的关系。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/51d92f6e56440a75f7af3f11.svg?v=51d92f6e5644)

图 3构造赫兹接触数据，球半径1 μm、样品模量20 kPa、泊松比0.45。A显示带噪声数据及拟合；B显示残差；C保持曲线相同，改变拟合时假定的探针半径，揭示几何标定与模量之间的关系。

对薄涂层，压入过深会受到下方硬基底影响；对细胞，局部厚度、细胞骨架、液体流动与测量速度都可能参与响应；对黏弹性凝胶，不同加载速度可能得到不同的表观模量。可以通过改变压入范围、加载速度、探针尺寸或测量位置，判断哪个因素控制结果。此时报告“在给定探针、环境和加载条件下拟合得到的局部模量”，便把数值与它回答的问题自然连接起来。AFM力学图上的每个颜色像素都来自这样的曲线与模型，不是直接拍到的一种固有颜色。

## 让几何、调平和接触模型各自接受检验

力曲线里的粘附也可以成为研究对象。回撤时最明显的负向力常被用来描述拉脱力，但它会受到接触时间、加载历史、探针表面化学、湿度或液体组成影响。空气中形成的微小液桥可以增加吸引，液体中的电荷屏蔽与聚合物链连接又会带来不同响应。若要比较蛋白层与裸基底的相互作用，可以使用相同探针条件、相近接触时间和多个位置重复，并检查探针是否在测量过程中吸附了物质。这样的对照让粘附差异与具体界面过程联系起来。

完整代码把三类问题分开计算。第一部分改变针尖参数，观察横向轮廓展宽；第二部分给已知表面加入倾斜，再用平面拟合恢复起伏；第三部分从指定弹性参数生成力曲线，加入噪声后重新拟合。输出包括双语图、原始与调平后的高度数组、逐点力曲线表格和计算摘要。由于教学数据的真实值已知，可以检验方法在自身条件下是否恢复正确参数，再讨论真实实验多出的接触点、粘附、漂移和异质性问题。

### 完整Python：针尖展宽、平面调平与压入拟合

明确给出教学表面与接触参数，导出数据、拟合残差、数值摘要和三个双语图。

```
"""AFM teaching models: probe broadening, levelling and Hertz indentation.

All arrays are constructed teaching data. No experimental surface or cell is claimed.
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def hertz(delta,E,R,nu):return 4/3*E/(1-nu**2)*np.sqrt(R)*delta**1.5
def broadening(x,radius,height=10,width=20):
    distance=np.maximum(np.abs(x)-width/2,0)
    return np.maximum(height-distance**2/(2*radius),0)

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
    ax=axes[0];ax.set_title(tr('A  1986：用悬臂弯曲读取微小力','A  1986: cantilever bending senses force'))
    ax.add_patch(Rectangle((1,3.8),6,.15,fc='#d6b664'));ax.add_patch(Rectangle((.8,3),.5,2,fc=gray));ax.add_patch(Polygon([[6.5,3.8],[7,3.8],[6.75,3]],fc=blue));ax.add_patch(Rectangle((1,1.5),8,.4,fc='#c8d6ca'))
    ax.add_patch(Polygon([[6.4,6.5],[7.1,6.5],[6.75,4.3]],fc=red));ax.text(6.75,7,tr('STM读取悬臂位移','STM reads cantilever displacement'),ha='center',fontsize=10)
    ax.text(3.5,4.4,tr('金属悬臂','Metal cantilever'),ha='center');ax.text(7.2,2.9,tr('金刚石探针','Diamond tip'),fontsize=10);ax.text(4.7,.8,tr('压电位置控制','Piezo position control'),ha='center');ax.annotate('',(6.75,3),(6.75,2),arrowprops={'arrowstyle':'<->','color':green})
    ax=axes[1];ax.set_title(tr('B  常用光杠杆读出与反馈','B  Common optical-lever readout and feedback'))
    ax.add_patch(Rectangle((1,3.8),6,.15,fc=gray));ax.add_patch(Polygon([[6.4,3.8],[7,3.8],[6.7,2.9]],fc=blue));ax.add_patch(Rectangle((1,1.7),8,.3,fc='#c8d6ca'))
    ax.plot([2,6.5,8.8],[7,3.95,6.8],color=red,lw=2);ax.text(1.6,7.4,tr('激光','Laser'));ax.add_patch(Rectangle((8.2,6.5),1.2,.6,fc='#d5e5eb',ec=blue));ax.text(7.1,7.5,tr('分区探测器','Split detector'),fontsize=10)
    ax.text(3,5,tr('悬臂弯曲 → 光斑移动','Bending → spot displacement'),ha='center',fontsize=10);ax.text(5,.6,tr('反馈调节z位置，使相互作用接近设定值','Feedback changes z to maintain the interaction setpoint'),ha='center',fontsize=10)
    save(fig,'principle')
    x=np.linspace(-80,80,801);truth=np.where(np.abs(x)<=10,10.,0.)
    grid=np.linspace(-250,250,129);X,Y=np.meshgrid(grid,grid);surface=2*np.cos(2*np.pi*X/500)+np.cos(4*np.pi*Y/500);plane=.025*X-.015*Y+7;raw=surface+plane
    design=np.column_stack([X.ravel(),Y.ravel(),np.ones(X.size)]);coef=np.linalg.lstsq(design,raw.ravel(),rcond=None)[0];level=raw-(design@coef).reshape(X.shape)
    sq=lambda a:float(np.sqrt(np.mean((a-a.mean())**2)))
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained');ax=axes[0,0];ax.fill_between(x,truth,color=gray,alpha=.3,label=tr('真实台阶','True step'))
    for radius,color in [(5,green),(20,red),(60,blue)]:ax.plot(x,broadening(x,radius),color=color,lw=2,label=f'R={radius} nm')
    ax.set(xlabel='x / nm',ylabel=tr('高度 / nm','Height / nm'),title=tr('A  更钝的针尖使横向轮廓更宽','A  Blunter probes broaden lateral outlines'));ax.legend(frameon=False,fontsize=9)
    for ax,a,title in [(axes[0,1],raw,tr('B  原始高度：表面加倾斜','B  Raw height: surface plus tilt')),(axes[1,0],level,tr('C  减去拟合平面','C  Subtract a fitted plane'))]:
        im=ax.imshow(a,extent=(-250,250,-250,250),origin='lower',cmap='cividis');ax.set(xlabel='x / nm',ylabel='y / nm',title=title);cb=fig.colorbar(im,ax=ax,shrink=.8);cb.set_label(tr('高度 / nm','Height / nm'))
    axes[1,1].plot(grid,raw[64],color=red,label=tr('原始剖面','Raw profile'));axes[1,1].plot(grid,level[64],color=green,label=tr('调平后剖面','Levelled profile'));axes[1,1].set(xlabel='x / nm',ylabel=tr('高度 / nm','Height / nm'),title=tr('D  倾斜改变粗糙度统计','D  Tilt changes roughness statistics'));axes[1,1].legend(frameon=False);axes[1,1].text(.04,.06,f'Sq: {sq(raw):.3f} → {sq(level):.3f} nm',transform=axes[1,1].transAxes)
    save(fig,'topography')
    delta_nm=np.linspace(2,100,100);delta=delta_nm*1e-9;E=20e3;R=1e-6;nu=.45;clean=hertz(delta,E,R,nu);rng=np.random.default_rng(1705);observed=clean+rng.normal(0,8e-12,len(delta));basis=hertz(delta,1,R,nu);Efit=np.dot(basis,observed)/np.dot(basis,basis);fit=basis*Efit
    fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
    axes[0].scatter(delta_nm,observed*1e9,s=12,color=gray,label=tr('构造观测数据','Constructed observations'));axes[0].plot(delta_nm,fit*1e9,color=green,lw=2,label=tr('赫兹拟合','Hertz fit'));axes[0].set(xlabel=tr('压入深度 / nm','Indentation / nm'),ylabel=tr('力 / nN','Force / nN'),title=tr('A  球形探针弹性接触','A  Spherical elastic contact'));axes[0].legend(frameon=False,fontsize=9)
    axes[1].plot(delta_nm,(observed-fit)*1e12,color=blue);axes[1].axhline(0,color=gray);axes[1].set(xlabel=tr('压入深度 / nm','Indentation / nm'),ylabel=tr('残差 / pN','Residual / pN'),title=tr('B  检查拟合剩余结构','B  Inspect remaining structure'))
    assumed=np.linspace(.5,2,100);estimates=Efit*np.sqrt(1/assumed);axes[2].plot(assumed,estimates/1000,color=red,lw=2);axes[2].axvline(1,color=gray,ls='--');axes[2].set(xlabel=tr('假定探针半径 / μm','Assumed probe radius / μm'),ylabel=tr('拟合模量 / kPa','Fitted modulus / kPa'),title=tr('C  半径标定影响模量','C  Radius calibration changes modulus'))
    save(fig,'force')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['indentation_nm','true_force_nN','constructed_observation_nN','fitted_force_nN','residual_pN']);w.writerows(zip(delta_nm,clean*1e9,observed*1e9,fit*1e9,(observed-fit)*1e12))
    np.savez_compressed(output/'topography.npz',x_nm=grid,raw_nm=raw,levelled_nm=level,true_nm=surface)
    exact=np.dot(basis,clean)/np.dot(basis,basis)
    summary={'force_02Npm_5nm_nN':1.,'width_halfheight_R20_H10_W20_nm':20+2*np.sqrt(20*10),'sq_raw_nm':sq(raw),'sq_levelled_nm':sq(level),'sq_true_nm':sq(surface),'hertz_force_50nm_nN':float(hertz(50e-9,E,R,nu)*1e9),'fitted_E_kPa':float(Efit/1000),'noiseless_E_kPa':float(exact/1000),'plane_slope_x':float(coef[0]),'plane_slope_y':float(coef[1]),'data_origin':'Constructed AFM geometry, surface and indentation teaching data.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

实际运行得到的Sq由调平前4.528 nm降至1.587 nm，后者与已知教学表面一致；恢复的平面斜率分别为0.025和−0.015。带噪声力曲线拟合得到约20.003 kPa，无噪声曲线则恢复20 kPa。这些数值分别检验背景扣除和接触模型计算，与曲线看起来是否平滑是不同的判断。

一个完整的表面研究可以从低倍率光学图定位开始，用AFM检查选定区域的高度，再根据问题增加力曲线或不同环境下的重复测量。对于蛋白吸附层，可以同时关注覆盖区域、厚度和局部相互作用；对于水凝胶，可以把表面起伏与压入响应放在同一位置比较；对于涂层，可以把纳米形貌与润湿、粘附或宏观力学联系起来。每一步保留原始信号、标定、样品状态和分析定义，微小探针获得的信息就能融入更完整的材料与生物研究。

## 把一块水凝胶的表面图与力学图连起来

若探针状态可能变化，可以在整组测量前后检查同一稳定参照表面。参照响应的变化有助于发现污染或标定漂移，避免把这类变化归入水凝胶本身的差异。

设想要比较两种交联程度的水凝胶，问题是较高交联是否同时改变表面起伏和局部抗压响应。可以先让两组样品在同样溶液与温度下达到相近的平衡状态，再用光学图记录测量区域。高度图采用相同扫描尺度、接近的探针作用条件和明确的调平规则；力曲线则使用已标定的球形探针，在多个位置采用相同加载程序。两类测量各自保留原始数据，随后按位置联系起来。这样得到的比较同时包含结构与响应，而不会把颜色深浅直接等同于材料软硬。

若第二组表面Sq更大、拟合模量也更高，还需要看这些变化发生在哪个层级。可能每块样品都呈现相近趋势，也可能只是少数颗粒状区域同时粗糙且较硬。把力曲线位置叠加到高度图上，区分基体、凸起和边界，能够帮助形成更具体的问题。若凸起只有几十纳米厚，较深压入可能同时感受到基体；若凸起会被探针推动，前后高度图则可能显示位置变化。空间对应和测量前后比较，使一个平均趋势逐渐变成对局部结构的解释。

最后的图可以由同一尺度的高度图、代表性力曲线、各样品的参数分布和几条关键剖面组成。高度色标与模量色标采用不同单位，保留比例尺，并说明每个分布来自多少独立样品和多少测量位置。代表性曲线应展示基线、接触区间和拟合范围，让读者看到模量从哪里来；参数分布则显示材料是否均匀。完成这样的组合后，AFM既能回答“表面是什么样”，也能回答“在这些条件下局部怎样响应”，两者共同服务于交联结构与材料性能之间的研究问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Binnig, Quate & Gerber — Atomic Force Microscope (1986)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.56.930)

   原子力显微镜原始论文与早期读出构想。

   Primary paper; original explanatory figure here.
2. [APS Physics — AFM landmark](https://physics.aps.org/articles/v5/106)

   1986年装置、金属悬臂、隧道读出与后来的光学读出。

   Publisher historical account; no image reused.
3. [Gwyddion — Tip Convolution Artefacts](https://gwyddion.net/documentation/user-guide-en/tip-convolution-artefacts.html)

   针尖形状、形态学膨胀与重建。

   Guide GPL v2+ or GFDL v1.2+; linked reference, figures original.
4. [Gwyddion — Data Levelling and Background Subtraction](https://gwyddion.net/documentation/user-guide-en/leveling-and-background.html)

   平面、多项式与掩膜调平的物理后果。

   Guide GPL v2+ or GFDL v1.2+; linked reference.
5. [Gwyddion — Statistical Analysis](https://gwyddion.net/documentation/user-guide-en/statistical-analysis.html)

   面积粗糙度、统计量和尺度解释。

   Guide GPL v2+ or GFDL v1.2+; linked reference.
6. [JPK / Bruker — A practical guide to AFM force spectroscopy](https://www.bruker.com/en/products-and-solutions/microscopes/bioafm/resource-library/a-practical-guide-to-afm-force-spectroscopy-and-data-analysis/_jcr_content/root/sections/section/sectionpar/twocolumns/contentpar-2/calltoaction.download-asset.pdf/primaryButton/jpk-tech-force-spectroscopy.14-2.pdf)

   靠近回撤、位移到力转换、标定与相互作用。
