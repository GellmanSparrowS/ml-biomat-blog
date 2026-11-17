# 共聚焦显微镜：让三维样品一层层显现

Source: https://ml-biomat.com/tutorials/experimental-methods/i02/
Language: zh-CN

从针孔与光学切片理解三维测量，用真实组织堆栈探索深度、投影和体积。

## 细胞是在材料表面，还是已经走进了里面

假设你在一种多孔支架里培养细胞，荧光照片显示整个视野布满亮点。这个结果很容易让人产生“细胞已经填满支架”的印象，但一张二维图像可能同时混入表面、内部和底部的信号。要知道细胞究竟位于哪里，需要沿着深度观察。共聚焦显微镜擅长从一定厚度的样品中选取较薄的光学层，把不同深度分别记录下来，再组织成三维图像。它能帮助研究细胞进入水凝胶的距离、蛋白在组织中的分布、微球在材料内部的排列，也能用于具有适当反射信号的材料表面观察。

“光学切片”可以先类比成从一摞透明纸里看清某一张。若每张纸都画着图案，同时看过去，所有线条会叠在一起；选择性地记录其中一层，就更容易分辨那层的结构。共聚焦没有真的把组织切开，而是利用照明位置与检测孔的位置共同筛选光。被记录的一层仍然具有有限厚度，并非数学上厚度为零的平面。理解这一点后，就不会把相邻两张图里出现同一个细胞当成两个细胞，也不会把层间距直接当成仪器的轴向分辨率。

三维数据带来的主要价值，是保留位置关系。一个红色对象与一个绿色对象在投影图里重叠，可能处在不同深度；一个看似断开的管状结构，在另一层可能继续延伸。读图时需要把二维观察习惯扩展到三个方向：在水平面辨认轮廓，沿深度追踪连续性，再用垂直切面检查空间关系。本篇会用真实的小鼠肾组织共聚焦数据展示这种读法，并用可以移动的切片帮助你理解，为什么一幅漂亮的最大强度投影不能代替原始图像堆栈。

## 针孔为什么能挑选深度：从明斯基的双重聚焦说起

明斯基的显微装置专利于1957年提出申请、1961年获得授权，其中把点照明、扫描和针孔检测联系起来。这个构想与研究神经组织等复杂生物结构的需要有关：不同深度的信号叠加，使真正想观察的位置难以辨认。历史上的装置通过移动样品，让一个小光点逐处扫描，再把探测器信号按相同位置组织成图像。今天常见的激光扫描共聚焦显微镜通常让扫描光束移动，样品保持相对稳定；光源、探测器和数字记录技术的改进，使这套空间选择原理变得更适合日常成像。

![原创针孔检测示意。绿色焦平面信号在针孔处会聚，另一深度的红色虚线信号有较大部分被孔外遮挡。历史联系来自明斯基1957年申请、1961年授权的扫描显微装置；图示讲解共轭检测原理，不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7f6fd63dc5b562f3627e1011.svg?v=7f6fd63dc5b5)

图 1原创针孔检测示意。绿色焦平面信号在针孔处会聚，另一深度的红色虚线信号有较大部分被孔外遮挡。历史联系来自明斯基1957年申请、1961年授权的扫描显微装置；图示讲解共轭检测原理，不按比例。

先看图中的绿色光路。来自焦平面上某一点的光，经过检测光学系统后，在与样品点对应的另一个平面形成较紧集的光斑。如果把针孔放在这个位置，较多的光可以穿过去，到达探测器。来自焦平面上方或下方的光，在针孔平面上通常没有聚成同样小的光斑，一部分会落在孔外被挡住。照明焦点与检测系统所选择的位置互相对应，这就是“共聚焦”名字背后的核心关系。针孔筛选的是光在空间中的分布，不是根据颜色猜测它来自哪一层。

这种筛选改变了信号与背景的组成。宽场显微镜可以同时收集较大区域的光，薄样品中往往高效而明亮；厚荧光样品里的离焦信号也会进入图像，形成雾状背景。共聚焦拒绝其中一部分离焦光，使某个深度的结构更容易辨认。针孔缩小时，光学层通常变薄，但能通过的有效光也减少；针孔开大时，信号增加，同时更多离焦光被接受。因此，针孔大小需要与样品亮度、厚度和测量目的配合，而不是一律调到最小。

仪器常以艾里单位描述针孔大小。一个艾里单位与指定波长和光学放大条件下的艾里斑直径相关，便于不同设置之间讨论针孔的相对尺度。它不是固定的微米数，也不等同于样品内的切片厚度。多通道成像时，各通道波长不同，同一个物理针孔对它们对应的艾里单位也可能不同。要比较通道的空间分布，应检查实际光学层厚度、通道配准和信号范围，而不只是看软件里是否都写着同一个针孔数字。

## 从一张图到一个体积：像素、体素与层间距

二维图像里的小方格叫像素。把不同深度的图像按顺序排列后，每个位置对应一个有体积的小格子，称为体素。一个三维数组需要明确轴顺序，否则程序可能把颜色通道当成深度。本篇原始文件包含16个深度、3个通道，每个平面512×512像素；程序整理成“深度、通道、纵向、横向”的顺序。原始标定给出横向间距1.24 μm、层间距1.25 μm。虽然这两种间距很接近，光学分辨率仍可能在横向和轴向不同，体素形状与PSF形状描述的是两件事。

$$
z_k=z_0+k\Delta z,\qquad H_{\mathrm{centers}}=(N_z-1)\Delta z
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/216c15b93ccea50c6180bd15.svg) | 第k层中心的深度坐标，μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b72465f81bed2e150afe1243.svg) | 第一层中心的参考坐标，μm，本例设为0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 从0开始的层索引，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d6e29d9ed67cc12345806818.svg) | 相邻层中心间距，μm，本例1.25 μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | 记录的层数，无量纲整数，本例16。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dbbb3310c3c3b526400e3f5f.svg) | 首末层中心之间的距离，μm。 |

第15层的坐标是0+15×1.25=18.75 μm。16层包含15个中心间隔；按体素格子计算的总厚度则为16×1.25=20 μm。定义不同，计算用途也不同。

这里把第一层中心定义为深度零。第15层中心就在18.75 μm处，因为从第0层到第15层一共跨过15个间隔。另一方面，把16层分别视为厚1.25 μm的采样格子，它们覆盖的体素厚度是20 μm。前者是首末采样中心之间的距离，后者是格子体积计算所用的总厚度，二者都可以有用，关键是保持定义一致。对于同一堆栈，不能在长度图里使用前者，又在体积计算时不加说明地把层数当成间隔数。

层间距需要根据你想保留的轴向信息选择。若一个细胞内部结构在深度方向变化很快，每隔很远才拍一张，就像只翻一本书中的每十页，容易跳过重要部分。把层间距设得很小可以增加采样密度，但不会让光学层自动变薄；它可能记录许多彼此高度相似的图像，并增加曝光与采集时间。可以用亚分辨荧光微球测量轴向PSF，再结合仪器给出的采样建议与具体分析目标安排间距。正式比较时，应保留原始层间距，而不是只交付一个经过插值、看起来更平滑的三维模型。

图中的四张真实切片使用相同灰度映射和相同空间尺度。你可以沿着某个较亮的轮廓追踪：它在第0层怎样出现，到第5层是否移动、扩大或分裂，再到第15层如何变化。每张图的深度坐标来自同一个参考面，所以这些变化描述的是空间位置，不是时间过程。三维堆栈通常需要逐层采集，活样品若在采集过程中运动，空间变化与时间变化可能混在一起；这时要把堆栈采集时间与生物过程的速度一起考虑。

![真实小鼠肾组织共聚焦图像，第二通道的第0、5、10、15层。所有图采用同一显示范围0—3000数字量与物理标定。数据：Genevieve Buckley / Monash Micro Imaging，经scikit-image分发，CC0。亮度变化需要结合组织分布、光学传播与采集条件解释。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d46745da3d9883f9652f502f.svg?v=d46745da3d98)

图 2真实小鼠肾组织共聚焦图像，第二通道的第0、5、10、15层。所有图采用同一显示范围0—3000数字量与物理标定。数据：Genevieve Buckley / Monash Micro Imaging，经scikit-image分发，CC0。亮度变化需要结合组织分布、光学传播与采集条件解释。

## 扫描速度、光子数和样品状态怎样一起决定设置

激光扫描系统逐点收集信号，每个点停留多久称为像素驻留时间。驻留时间增加，通常能收集更多光子；图像更大、平均次数更多或通道依次采集，也会延长总时间。可以先用一个简化乘法估算成本：一幅512×512像素图，每个像素2 μs，重复平均两次，理想扫描时间约1.05 s。若16层、3个通道全部顺序采集，就约50.3 s。实际设备还需要回扫、调焦、通道切换与读出时间，因此这个乘法用于理解主要贡献，而不是替代仪器实际记录的时间戳。

$$
t_{\mathrm{frame}}\approx N_xN_y\tau N_a,\qquad t_{\mathrm{stack}}\approx t_{\mathrm{frame}}N_zN_c
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9726e175d28ec5900e7f53a8.svg) | 单平面、单通道的理想扫描时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1146e9e5c5b8032680acc2c1.svg) | 横纵像素数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 每次扫描的像素驻留时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/41233129fdcf45a3b022217c.svg) | 每个位置重复平均的次数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34b25718fdbd7276f8f56589.svg) | 整个堆栈的理想顺序扫描时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | 深度层数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bfeaf6f059c8ef7165e8b680.svg) | 全部顺序采集时的通道数，无量纲整数。 |

512×512×2×10⁻⁶×2=1.048576 s；再乘16层和3通道，约50.33 s。公式忽略回扫、移动和切换开销；同时探测通道不按相同方式乘以通道数，实际时间应读取采集记录。

这个时间预算会影响生物解释。若一个细胞结构在几十秒内明显移动，完整堆栈就不是同一瞬间的三维快照。可以减少无关的视野范围、降低不必要的层数，或选择更适合快速成像的扫描方式，让测量速度与问题匹配。转盘共聚焦利用多个针孔同时采集不同位置，适合一些需要较快采集的活细胞实验；其针孔结构、样品散射与通道设置又带来不同的取舍。选择系统时应问“需要多快地记录哪些空间信息”，而不是单看一幅静态图能有多细腻。

平均可以降低随机波动，却也会重复照射样品。荧光分子可能发生光漂白，活细胞也可能因照明而改变状态，因此高激光功率与长驻留时间并不总能带来更有用的数据。可以先在具有代表性的样品上寻找未饱和且足够辨认目标的设置，再观察短时间重复采集时信号和形态是否稳定。检测器增益改变的是电子信号的放大，不会凭空增加已经进入系统的光子。比较实验组时，应把激光功率、增益、驻留时间、平均方式和针孔条件作为一组相互关联的设置保留下来。

三维样品的装载需要让目标结构保持原来的形态。直接压紧盖玻片可能把软水凝胶或组织压扁，导致观察到的高度变化来自制样。适当的间隔支撑、合适的样品腔与足够的物镜工作距离，可以给样品留出空间。折射率不匹配会使深处的PSF发生变化；散射与吸收又会让深层信号衰减。若深处图像更暗，应同时考虑标记分布、光传播和探测条件，必要时采用具有已知分布的荧光参照或反向观察来辨别原因，而不是直接把亮度衰减解释为细胞数量下降。

多通道图像还需要区分串色与真实共定位。某种染料的发射谱较宽时，它的光可能同时进入两个检测窗口；这时一个只有单一标记的样品也会在两个通道里发亮。单染对照可以直接测出这种现象，未染对照则帮助辨认材料或组织的自发荧光。顺序激发能减少一些由同时照明引起的混合，但若发射窗口本身重叠，顺序扫描并不会自动消除所有串色。对于距离比较，多色荧光微球还能检查不同波长的图像是否准确叠合。把这些检查与生物标记实验一起安排，通常比在最终合并图上猜测颜色来源更容易解释。

## 三维数据怎样压成一张图，以及压缩时丢掉了什么

最大强度投影在每个横向位置上，选取所有深度中最大的那个数。这种显示方式能把分散在不同深度的亮结构集中到一张图中，适合快速浏览荧光网络或寻找稀疏目标。平均投影则把同一横向位置上的所有层求平均，更接近描述整段深度里的平均信号。两者都保留横向位置，却不再告诉你被选中的信号来自哪一层。最大投影里相邻甚至相交的结构，在三维空间中可能相隔数微米，因此涉及接触、共定位或连通性的问题，需要回到切片或正交视图。

$$
P_{\max}(x,y)=\max_k I(x,y,k),\qquad P_{\mathrm{mean}}(x,y)=\frac1{N_z}\sum_{k=0}^{N_z-1}I(x,y,k)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dea8a18a2088323ea180fbb9.svg) | 第k层、横向位置(x,y)的原始强度，数字量；位置可用像素索引或标定坐标表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | 图像平面的横纵位置；本篇图像坐标用μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 深度层索引，从0开始，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | 参与投影的层数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/842117f33e02cf9f7b56a727.svg) | 最大强度投影，数字量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/36b205260ddb2b37d4ffbb56.svg) | 平均强度投影，数字量。 |

四层强度10、20、100、30的最大投影为100，平均投影为40。max选一个最大值，求和再除以层数得到平均值；两种操作都移除了该位置的深度分布。

一个简单例子能说明差别：某个横向位置的四层强度分别为10、20、100和30，最大投影等于100，平均投影等于40。若再增加一层很亮的结构，最大投影可能明显升高，却仍然只显示一个数。最大投影也容易保留孤立的噪声高值；平均投影会把只占很少层的细结构稀释。选择投影方式时，先决定要展示结构的可见性、整体平均强度还是特定深度的分布，再选相应的表达。相同数据使用不同投影得到不同亮度，并不意味着样品发生了改变。

![同一真实堆栈的不同读法。A、B在共同显示范围下比较最大与平均投影；C保留三个通道沿深度的平均信号，通道间数值不直接换算成分子数量比；D固定分析体积，显示第二通道超过阈值的体素比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3993ba2b3c47743fd449e3bf.svg?v=3993ba2b3c47)

图 3同一真实堆栈的不同读法。A、B在共同显示范围下比较最大与平均投影；C保留三个通道沿深度的平均信号，通道间数值不直接换算成分子数量比；D固定分析体积，显示第二通道超过阈值的体素比例。

图中最大投影与平均投影采用相同显示范围，所以亮度差异直接反映投影规则。深度曲线则分别计算三个通道在每一层的平均数字量。通道的染料、探测效率和采集设置可能不同，因此曲线适合观察各自随深度的变化，跨通道的绝对数值不能简单解释为不同分子的数量比。若某个通道在深处降低，可以检查同一结构的形态、背景与标定信号，再判断是生物分布还是光学衰减。曲线把空间变化集中呈现出来，切片则保留变化发生在哪里，两种图相互补充。

三维渲染会进一步把体素变成表面、透明云或彩色体积。这些表示能让空间关系更直观，但其外观受到阈值、透明度和插值的影响。一个平滑表面可能来自显示算法对离散数据的连接，不能据此推断仪器记录到了同样平滑的边界。呈现组织或支架的三维结构时，可以同时提供一张整体渲染、带物理坐标的正交切片和用于生成表面的分割规则。这样读者既能获得直观印象，也能回到原始信号检查边界与空隙。

反卷积则尝试根据PSF模型，把扩散开的信号重新分配到更可能的来源位置。它与改变显示对比度不同，因为它对图像形成过程作出了数学假设。若PSF与真实仪器、波长或成像深度不匹配，或者原图已经饱和、采样过稀，结果可能出现边缘振铃或不稳定的细节。实际使用时保留原始堆栈，说明PSF如何获得与停止计算的规则，并用已知结构或微球检查恢复效果。对于本篇的入门问题，先把真实切片、投影和物理标定读清楚，再引入反卷积，能够更容易识别计算究竟改善了什么。

## 体积不是把二维面积随意乘一个厚度

从三维图像计算体积，最直接的做法是先确定哪些体素属于目标，再把这些体素的物理体积加起来。每个体素的体积等于横向间距、纵向间距和层间距的乘积。本例中，一个体素约为1.922 μm³。若有1000个体素被纳入同一目标，分割体积约为1922 μm³。这个数的含义由分割规则决定：如果规则只是通道2强度大于1000，那么结果叫“超过该阈值的信号体积”；要把它解释为细胞、管腔或特定蛋白结构的体积，还需验证阈值对应的对象。

$$
V=N_{\mathrm{mask}}\Delta x\Delta y\Delta z,\qquad f=\frac{N_{\mathrm{mask}}}{N_{\mathrm{ROI}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 被选中体素的总体积，μm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa0d04a4648049d3ba42d047.svg) | 满足固定分割规则的体素数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec9221cb3cb38bb1f2a7546d.svg) | 三个方向的体素间距，μm；本例依次1.24、1.24、1.25。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 入选体素占分析区域的比例，无量纲；乘100得到百分比。 |
| ![Formula](https://ml-biomat.com/static/agent-math/87d0002d8eeb12cf9a4e12cc.svg) | 固定分析区域中的全部体素数，无量纲整数；ROI表示感兴趣区域。 |

一个体素体积为1.24×1.24×1.25=1.922 μm³，1000个体素对应1922 μm³。此处默认规则相同、体素大小均匀且分母固定。超过强度阈值的信号体积与具体生物对象体积的关系需要由分割校验确定。

程序把阈值从500扫到2000，绘出符合条件的体素占整个分析体积的比例。阈值升高时，入选体素只能减少或保持不变，这提供了一条简单但有力的计算检查。曲线若出现反向增加，就应检查是否混用了不同掩膜、是否改变了分析区域，或是否在每个阈值下又进行了不同处理。这里的分母始终是同一通道、同一16层视野中的全部体素。若研究需要只分析组织内部，应先建立固定的组织掩膜，再以该掩膜内的体素作为分母，并清楚地区分“视野占比”与“组织内部占比”。

处在图像边界的对象可能被截断。若你想比较完整细胞体积，边界截断对象需要按预先规定的规则处理；若想计算某个固定空间窗口内的总体信号占比，边界内的部分体素仍可以参与。两种问题有不同的分析单位，不宜套用同一套删除规则。相邻细胞在三维中接触时，简单连通区域也可能把它们合成一个对象；需要对象级计数时，可以结合核标记、三维距离变换和人工校验建立分割，而不把总信号体积直接除以一个假定的“平均细胞体积”。

重复与误差同样应保持空间层级。16张切片属于同一个组织堆栈，增加层数增加了空间采样，并没有增加16个独立组织样本。可以对多个独立样品各自计算体积分数，再比较样品间分布；也可以描述一个样品内部沿深度的变化，但要保持“内部空间差异”这一名称。对于阈值带来的不确定性，可以报告合理阈值区间内结果如何变化，并展示代表性边界叠图。这样的信息直接告诉读者哪些结构稳定、哪些细节对处理更敏感。

## 拖动真实切片，再把整个分析重新算一遍

交互区使用同一份真实肾组织数据中的第二通道。移动深度滑块，会在16个原始采样平面之间切换；切换到最大投影或平均投影，会看到沿深度压缩以后形成的图像。所有视图采用相同的显示映射，避免自动调节对比度掩盖信号变化。图像为便于页面浏览进行了显示缩小，数值摘要仍由完整512×512像素平面计算。先寻找一个明亮轮廓，观察它在哪些层出现，再比较投影里它与周围结构的关系，通常就能理解二维重叠与三维位置之间的区别。

## 逐层浏览真实共聚焦堆栈

第二通道，固定0—3000数字量显示范围。浏览图缩小为256×256像素；原始数值与均值来自512×512平面。数据：Genevieve Buckley / Monash Micro Imaging，CC0。

![真实肾组织共聚焦图像](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5766842ea164cc2bb0927907.png?v=5766842ea164)

视野宽度635 μm；灰度显示。

完整Python程序离线读取随包附带的原始TIFF，验证页面数量和数组形状，按“深度、通道、纵向、横向”整理数据。随后生成原理图、四层切片图和投影诊断图，导出每层的平均信号与阈值占比，并保存投影数组。程序中的体素体积、首末层中心距离和理想扫描时间都可以手算核对。你可以先把第二通道换成另一通道，再检查它的深度变化；也可以改变固定阈值，观察体积分数曲线，而不改变原始数组或给不同层分别自动拉伸灰度。

### 完整Python：真实堆栈的切片、投影与体积

读取随下载包附带的CC0 TIFF，保留三维轴顺序与物理尺寸，输出图像、逐层表格和计算摘要。

```
"""Confocal microscopy: real optical sections, projections and 3D sampling.

The bundled kidney TIFF is CC0, acquired by Genevieve Buckley,
Monash Micro Imaging (2018), and distributed by scikit-image.
Axes are (z, channel, y, x); spatial steps are 1.25, 1.24, 1.24 um.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from PIL import Image,ImageSequence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse,Rectangle

def load_stack():
    with Image.open(Path(__file__).parent/'data/kidney.tif') as im:
        pages=np.stack([np.asarray(page).astype(np.uint16) for page in ImageSequence.Iterator(im)])
    if pages.shape!=(48,512,512):raise ValueError(f'Unexpected TIFF dimensions {pages.shape}')
    return pages.reshape(16,3,512,512)

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'],'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'font.size':11,'axes.titleweight':'bold','text.color':'#243b45','axes.labelcolor':'#243b45','figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5'})
    zh=language=='zh';tr=lambda a,b:a if zh else b
    green,blue,red,gray='#168477','#3574a8','#bd624b','#73848a'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(11,6),layout='constrained');ax.set(xlim=(0,12),ylim=(0,7));ax.axis('off')
    ax.set_title(tr('从点照明到针孔检测：共轭平面之间的空间筛选','From point illumination to pinhole detection: spatial selection'))
    for x in [1,2,3]:ax.plot([x,x],[1,4.3],color='#c6d2ce',lw=8,alpha=.65)
    ax.text(.7,5,tr('样品的不同深度','Different specimen depths'))
    ax.add_patch(Ellipse((4.4,2.7),.35,4.3,fc='#d8e8ef',ec=blue))
    ax.text(3.8,5.1,tr('检测光学','Detection optics'))
    for y in [.8,4.6]:
        ax.plot([2,4.4,7.5],[2.7,y,2.7],color=green,lw=2)
        defocused_end=2.7+(2.7-y)*(7.5-6.65)/(6.65-4.4)
        ax.plot([1,4.4,6.65,7.5],[2.7,y,2.7,defocused_end],color=red,lw=1.4,ls='--')
    ax.add_patch(Rectangle((7.4,.3),.25,2.15,fc=gray));ax.add_patch(Rectangle((7.4,2.95),.25,2.2,fc=gray))
    ax.text(6.6,5.4,tr('针孔所在平面','Pinhole plane'))
    ax.add_patch(Rectangle((9,2.1),1.3,1.2,fc='#dde7e3',ec=gray))
    ax.annotate('',(9,2.7),(7.7,2.7),arrowprops={'arrowstyle':'->','color':green,'lw':2})
    ax.text(8.7,3.7,tr('探测器','Detector'));ax.text(8.5,1.5,tr('焦平面光通过\n离焦光大部分被挡住','In-focus light passes\nMuch defocused light is blocked'))
    ax.scatter([2,1],[2.7,2.7],color=[green,red],s=80,zorder=10)
    ax.text(.8,.2,tr('绿色：焦平面；红色虚线：另一深度。光线为原理示意，不按比例。','Green: focal plane; red dashes: another depth. Schematic rays, not to scale.'),fontsize=10)
    ax.text(.8,6.2,tr('1957年申请，1961年授权：明斯基的扫描与双重聚焦构想','Filed 1957, granted 1961: Minsky’s scanning and double-focusing concept'),fontsize=11)
    save(fig,'pinhole')
    stack=load_stack();dz,dy,dx=1.25,1.24,1.24
    volume=stack[:,1].astype(float);z=np.arange(16)*dz
    vmax=3000;extent=[0,512*dx,512*dy,0]
    fig,axes=plt.subplots(2,2,figsize=(10,9),layout='constrained')
    for ax,i in zip(axes.ravel(),[0,5,10,15]):
        im=ax.imshow(volume[i],cmap='magma',vmin=0,vmax=vmax,extent=extent)
        ax.set(xlabel='x / μm',ylabel='y / μm',title=tr(f'层 {i}：z={z[i]:.2f} μm',f'Slice {i}: z={z[i]:.2f} μm'))
    cb=fig.colorbar(im,ax=axes,shrink=.7);cb.set_label(tr('原始数字量，共同显示范围','Raw digital number, common display range'))
    save(fig,'sections')
    projection_max=volume.max(axis=0);projection_mean=volume.mean(axis=0)
    fractions=(volume>1000).mean(axis=(1,2));means=volume.mean(axis=(1,2))
    thresholds=np.arange(500,2001,100);vf=np.array([(volume>t).mean() for t in thresholds])
    fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
    axes[0,0].imshow(projection_max,cmap='magma',vmin=0,vmax=vmax,extent=extent)
    axes[0,0].set(xlabel='x / μm',ylabel='y / μm',title=tr('A  最大强度投影：保留沿z最亮值','A  Maximum projection: brightest value along z'))
    axes[0,1].imshow(projection_mean,cmap='magma',vmin=0,vmax=vmax,extent=extent)
    axes[0,1].set(xlabel='x / μm',ylabel='y / μm',title=tr('B  平均投影：沿z平均信号','B  Mean projection: average signal along z'))
    for c,color in enumerate([blue,green,red]):
        axes[1,0].plot(z,stack[:,c].mean(axis=(1,2)),'o-',color=color,label=tr(f'通道{c+1}',f'Channel {c+1}'))
    axes[1,0].set(xlabel='z / μm',ylabel=tr('平面平均数字量','Plane-mean digital number'),title=tr('C  各通道沿深度的强度变化','C  Intensity across depth in each channel'));axes[1,0].legend(frameon=False)
    axes[1,1].plot(thresholds,vf*100,'o-',color=green)
    axes[1,1].set(xlabel=tr('阈值 / 数字量','Threshold / digital number'),ylabel=tr('超过阈值的体素比例 / %','Voxels above threshold / %'),title=tr('D  分割结果依赖阈值','D  Segmented fraction depends on threshold'))
    save(fig,'projections')
    nz,nc,ny,nx=stack.shape
    voxel_volume=dx*dy*dz;selected=int(np.count_nonzero(volume>1000))
    summary={'shape_zcyx':[nz,nc,ny,nx],'voxel_volume_um3':voxel_volume,'first_last_center_distance_um':(nz-1)*dz,'voxel_extent_z_um':nz*dz,'threshold':1000,'selected_voxels':selected,'selected_volume_um3':selected*voxel_volume,'selected_fraction':selected/volume.size,'nominal_frame_s':512*512*2e-6*2,'nominal_three_channel_stack_s':512*512*2e-6*2*16*3,'max_projection_mean':float(projection_max.mean()),'mean_projection_mean':float(projection_mean.mean()),'slice_mean_values':means.tolist(),'data_origin':'Real CC0 kidney confocal image, Genevieve Buckley / Monash Micro Imaging, via scikit-image'}
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['slice_index','z_um','channel2_mean_digital_number','fraction_above1000']);w.writerows(zip(np.arange(nz),z,means,fractions))
    np.savez_compressed(output/'projections.npz',maximum=projection_max,mean=projection_mean,z_um=z)
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k!='slice_mean_values'},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

## 围绕三维问题组织采集与呈现

当问题是细胞进入材料的深度时，应先确定材料表面或其他可重复识别的参考面，再用统一坐标计算细胞位置。样品若倾斜，简单使用仪器的z坐标可能把表面高度变化混入侵入深度，可以通过表面标记或几何拟合建立相对深度。若问题是孔隙内是否形成连通的细胞网络，就需要覆盖足够大的体积，并检查切片间是否存在漏采或运动。若问题是两个蛋白是否在同一区域富集，则要关注通道串色、色差、标记特异性及分析尺度，不能只以合并图出现黄色作为分子相互作用的证据。

一份清楚的结果可以把整体与细节放在同一条叙述中：先用概览说明样品与取样位置，再以统一尺度的切片显示深度关系，随后给出与问题直接对应的分布或体积指标。记录应包含物镜、波长、针孔、扫描设置、层间距、堆栈范围、物理像素大小和处理规则。保留原始堆栈使读者或合作者能够重新选择切面，而不仅得到一张已经压平的投影。空间信息一旦在展示阶段被丢弃，单靠文字很难把它补回来。

选择堆栈起止位置时，先用低剂量预览确认目标从哪里出现、在哪里消失，再在两端留出与分析相适应的余量。若最后一层仍有大量目标信号，体积或最大深度可能受到采集窗口截断；扩大扫描范围和更换分析问题是两种不同处理。观察多个样品时使用一致的边界定义，能让深度分布具有可比较的参照。

可以用两个判断练习结束本篇。第一，层间距从1 μm改为0.2 μm后，三维表面看起来更平滑，是否说明光学轴向分辨率提高了五倍？采样确实变密，但光学PSF需要独立检查。第二，两个通道在最大投影中大量重合，是否说明它们在每一层都位于同一位置？逐层浏览和正交视图能够回答这个空间问题。把采样、光学选择和显示方式分开理解以后，共聚焦就从“拍三维彩图的仪器”变成了一个能够围绕位置、结构和时间设计的测量工具。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Minsky — US3013467A, Microscopy apparatus](https://patents.google.com/patent/US3013467A/en)

   历史扫描与双重聚焦构想；申请和授权年份。

   Historical primary source; original explanatory figure here.
2. [Nikon MicroscopyU — Introductory Confocal Concepts](https://www.microscopyu.com/techniques/confocal/introductory-confocal-concepts)

   针孔、点扫描、共轭焦点与发展历史。
3. [Nikon MicroscopyU — Specimen Preparation and Imaging](https://www.microscopyu.com/techniques/confocal/specimen-preparation-and-imaging)

   三维样品装载、物镜工作距离与折射率问题。
4. [Nikon MicroscopyU — Critical Aspects of Confocal Microscopy](https://www.microscopyu.com/techniques/confocal/critical-aspects-of-confocal-microscopy)

   采集设置、光漂白与多通道设计。
5. [Introduction to Bioimage Analysis — Microscopes & detectors](https://bioimagebook.github.io/chapters/3-fluorescence/4-microscope_types/microscope_types.html)

   比较宽场、点扫描和转盘的成像取舍。

   Book original content CC BY 4.0; linked reading.
6. [scikit-image — kidney dataset](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.kidney)

   原始图像、通道与物理间距的公开说明及CC0许可。

   Image: Genevieve Buckley / Monash Micro Imaging, 2018, CC0.
