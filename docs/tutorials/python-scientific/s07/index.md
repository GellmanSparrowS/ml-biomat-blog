# 看清三维数据内部的结构

Source: https://ml-biomat.com/tutorials/python-scientific/s07/
Language: zh-CN

从空间采样到等值面、内部切片与体积测量，用PyVista把三维形状与可核对的几何量连接起来。

## 看见外表以后，怎样知道里面是什么

显微断层图像常常是一层层的灰度切片，模拟程序则可能在空间中的许多位置保存温度、浓度或位移。把这些数据画成三维外形，可以帮助我们判断方向、连通关系和内部位置；若还想测量体积，就需要知道外形怎样从数值生成。本节用PyVista完成这一过程：建立带毫米坐标的体数据，提取等值面，切开查看内部，再把计算出的体积和截面积与已知答案比较。

我们先构造一个椭球形的教学模型。它有确定的数学表达式，三条轴的长度也能直接计算，因此既能练习真实的三维操作，也能判断结果差多少。它可以帮助理解颗粒、孔洞或组织轮廓的处理过程。图中的数值来自这个解析模型，阈值表示我们选择的区域边界。处理实际成像数据时，阈值还需要与信号含义、背景和实验标定联系起来。

三维视图负责说明空间位置，二维切片负责精确读数，误差图负责判断离散后的结果。三者各有用处。旋转相机能够发现被挡住的一侧，却不会增加输入数据的空间分辨率；让表面看起来更光滑，也不会自动提高体积精度。把这些问题放在同一个例子里，才能知道每一步操作改变了什么。

## 先给空间中的每个位置一个数

“标量场”可以先理解为空间位置到一个数值的对应关系。例如房间每个位置都有一个温度，温度就是标量；同时记录风速的大小和方向，则需要向量。本节给每个位置计算一个无量纲指标q：先分别把三个坐标除以三个参考长度，平方后相加。这样，位置与原点的关系就被压缩成一个数，同时保留三个方向上不同的尺度。

$$
q(x,y,z)=\left(\frac{x}{a}\right)^2+\left(\frac{y}{b}\right)^2+\left(\frac{z}{c}\right)^2,\qquad q\leq\lambda
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eeaf78722a7e7f8494b85137.svg) | 相对中心的三个空间坐标，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | 参考半轴，依次为3、2、1 mm，均为正值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 标量场值，无量纲；相同q值的位置构成等值面。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 选定的正阈值，无量纲；内部满足q不大于该值。 |

每项先用长度除以长度，得到无量纲比例，再平方相加。平方使正负方向具有相同贡献，也使距离增加时贡献增大。代入(1.5, 1, 0.5) mm，可得q=(1.5/3)²+(1/2)²+(0.5/1)²=0.75，因此该点位于λ=1的内部。等值面上的半轴分别为a√λ、b√λ、c√λ；λ=0.5时最长半轴为3√0.5≈2.121320 mm。

参考长度取3、2、1 mm。在(3,0,0) mm处，只有第一项等于1，因此q为1；在(0,2,0)和(0,0,1) mm处也一样。连接所有q恰好为1的位置，就得到一个椭球表面。这三个参考长度是半轴，从中心量到两侧端点；完整的三个轴长分别为6、4、2 mm。它像一个沿不同方向拉伸的球，在最长轴方向需要移动更远，才能达到相同的指标。

等值面取q等于阈值λ，内部则定义为q不大于λ。把λ从1改成0.5，三个半轴都乘以0.5的平方根，整个椭球缩小；改成1.5，则一起放大。这里较小的q对应靠近中心的位置，所以“内部”位于阈值以下。读取别的标量场时，应重新确认哪一侧对应所研究的材料或区域，不能只凭颜色深浅判断内外。

阈值与网格分辨率是两种不同选择。前者改变我们定义的边界，后者改变用多少采样值描述同一个场。比较体积时必须把这两种变化分开，否则很容易把选取了更大区域造成的体积增加，误当成网格计算变得更准确。后面的图会在同一阈值下逐步加密采样，再分别比较三个阈值。

## 数组有几个数，空间就有几个格子吗

PyVista的ImageData把规则采样点与它们之间的连接关系组织在一起。建立它时，三个设置尤其重要：dimensions给出每个方向的点数，origin给出第一个点的位置，spacing给出相邻点的实际距离。单独一张数字表只能说明某处有一个值；加上这些空间信息，程序才能知道两个值相隔多少毫米，以及哪些点共同组成一个小立方单元。

$$
h=\frac{x_{\max}-x_{\min}}{N-1},\qquad x_i=x_{\min}+ih,\quad i=0,\ldots,N-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 相邻采样点的间距，单位mm；本例三个方向相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd27db42b5426d22e4e9954.svg) | 该方向的起点与终点坐标，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 每个方向的采样点数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 从0开始的点索引，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | 第i个采样点的坐标，单位mm。 |

N个点之间有N−1段间隔，因此总长度要除以间隔数。取起点−4 mm、终点4 mm、N=33，得到h=8/32=0.25 mm；第16号点的坐标为−4+16×0.25=0 mm。三个方向各有33个点，合计33³=35,937个点；每个方向32段，合计32³=32,768个体单元。

本节三个方向都从−4 mm延伸到4 mm。每个方向取33个点，意味着32个间隔，所以间距为0.25 mm。空间中共有35937个点、32768个小立方单元。点和单元数量不同，正如一条线段上5个刻度点之间只有4段。若误把点数当成间隔数，计算区域的终点就会偏移，后面的几何尺寸也会随之改变。

数据放在`point_data`里，表示q在每个采样点上的取值。`cell_data`则为每个单元保存一个值，常见于单元平均量或分区标签。两种存储对应不同的物理定义。本节直接从`grid.points`取得真实坐标，再计算q，因此每个数与其位置逐一对应。若从一个三维NumPy数组导入数值，还需要核对轴的顺序与展平顺序；只要数组长度相同，程序就可能接收，空间方向却未必正确。

可以先检查几个容易手算的位置：中心q为0，三个参考半轴端点q为1，坐标(1.5,1,0.5) mm的三项各为0.25，合计0.75。这样既能检查毫米单位，也能检查坐标与数值是否错位。对实际数据，还应确认层间距是否等于平面像素间距；三个方向的间距可以不同，立体显示应按各自的物理长度安排比例。

## 八个角点之间，表面究竟从哪里穿过

1987年，Lorensen与Cline发表Marching Cubes方法，面对的是如何从三维医学成像采样值构造可观察的表面。算法逐个处理由八个角点围成的小单元，比较角点值与给定阈值，在跨越阈值的边上寻找交点，再用三角面连接这些交点。2019年介绍PyVista的论文则展示了如何通过Python接口使用VTK的三维绘图与网格分析能力。本节显式选择`method='marching_cubes'`，把这一算法实际用到前面的采样场上。

![一个实际Marching Cubes单元及其边上线性插值。左图的两个三角面由原生算法从八个角点值生成；右图比较同一条边的线性近似与已知解析场，显示交点从0.7071 mm移至0.6667 mm的原因。颜色区分阈值两侧，坐标轴使用物理长度。](https://ml-biomat.com/static/tutorials/python-scientific/figures/e5a7d8ba9a44788ae6c68817.svg?v=e5a7d8ba9a44)

图 1一个实际Marching Cubes单元及其边上线性插值。左图的两个三角面由原生算法从八个角点值生成；右图比较同一条边的线性近似与已知解析场，显示交点从0.7071 mm移至0.6667 mm的原因。颜色区分阈值两侧，坐标轴使用物理长度。

左图取自本节的一个真实网格单元。蓝色角点的q小于1，橙色角点的q大于1；跨过两种状态的边上会出现边界交点。局部面片由实际运行的算法生成。这里的数字不是空间坐标，而是各角点的q值；坐标轴另用毫米标明。三角面的顶点通常位于单元边的中间，因此表面能够比直接堆叠整块立方体更细致地表达边界位置。

$$
\eta=\frac{\lambda-q_0}{q_1-q_0},\qquad \mathbf r_* =\mathbf r_0+\eta(\mathbf r_1-\mathbf r_0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ff4c8bab0ec6e039de68ecf.svg) | 边上两个端点的标量值，无量纲，且彼此不同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 位于两个端点值之间的阈值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 从第一个端点走到交点所占的边长比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27dee343dec5fb058859f85.svg) | 两个端点的位置向量，每个分量的单位为mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a0037efc1d28fcdd3514849d.svg) | 线性插值得到的交点位置向量，单位mm。 |

线性变化表示沿边走过相同比例的路程，标量也完成相同比例的变化。在图中的竖直边上，q₀=0.75、q₁=1.5、λ=1，因此η=0.25/0.75=1/3。z坐标从0.5 mm开始，增加(1/3)×0.5 mm，交点为2/3 mm。该边的解析场满足q=0.5+(z/mm)²，因此真实交点为√0.5 mm≈0.707107 mm。两者相差约0.040440 mm，正是这条边上的线性近似误差。

右图把一条边单独展开。沿这条边，x固定为1.5 mm、y固定为1 mm，z从0.5 mm增加到1 mm，q从0.75增加到1.5。假设边上数值按直线变化，达到q=1需要走完整变化的三分之一，所以交点位于z约0.6667 mm。已知解析场给出的真实位置约为0.7071 mm。两个结果之间的距离，直接显示了只利用端点并做线性插值时留下的近似。

把网格加密后，端点间距离缩短，弯曲关系在更小范围内更接近直线，边界通常也更接近解析位置。另一方面，复杂场可能包含很薄的结构或一个单元内多次变化；采样点没有捕捉到的变化，需要通过更密的采样或更合适的数据模型来描述。对当前平滑、单一且凸的椭球，局部插值误差可以清楚追踪，适合建立这层直觉。

## 切开体数据，与切开表面，得到的东西不同

`grid.contour([1.0], scalars='q', method='marching_cubes')`提取q等于1的表面，输出对象是PolyData，包含表面顶点与连接它们的三角面。方括号很有用：一个只含1.0的列表明确指定这个阈值；直接传整数1，则表示让接口自动选择一个等值面。得到表面以后，内部采样值仍保存在原来的ImageData中，表面只是同一份数据的一种几何表达。

现在在z=0.5 mm处放一张水平切片。对原始体数据调用`slice`，得到的是带q值的二维平面网格，可以用颜色显示内部数值；对椭球表面调用同样的切片操作，得到的是表面与平面的交线。这条交线围住截面，但它本身不是填满的截面。左图用填充的橙色多边形标明切片位置，右图把同一条边界与解析椭圆放到等比例坐标里比较。

![同一解析教学场的两种观察方式。左侧是真实VTK渲染，透明椭球中橙色区域位于z₀=0.5 mm；右侧对原始体网格切片，并在共享物理坐标中叠加网格交线与解析边界。色标表示无量纲q值；透明度改变可见性，长度与面积由几何坐标决定。](https://ml-biomat.com/static/tutorials/python-scientific/figures/a7a5cc76fab95b15416ba681.svg?v=a7a5cc76fab9)

图 2同一解析教学场的两种观察方式。左侧是真实VTK渲染，透明椭球中橙色区域位于z₀=0.5 mm；右侧对原始体网格切片，并在共享物理坐标中叠加网格交线与解析边界。色标表示无量纲q值；透明度改变可见性，长度与面积由几何坐标决定。

切片需要位置与方向两项信息。origin在这里给出平面经过的点(0,0,0.5) mm，normal=(0,0,1)给出垂直于平面的方向，因此切片平行于xy平面。法向量像插在纸面上的一支垂直箭头，它描述纸面朝向；把纸沿箭头移动，可以观察不同高度。斜向切片也遵循同样原则，只需更换法向量与经过的点。

三维图可以告诉我们切片在物体哪一层，读截面宽度时则使用右侧二维图。二维横纵轴都以毫米表示并保持相同比例，椭圆的长短轴才能直观比较。右图颜色来自切片网格上的q值，橙线来自表面交线，白色虚线来自解析公式；它们各自对应明确的对象。改变颜色映射只改变显示方式，改变阈值才会移动边界。

## 体积和截面积，要有可以核对的答案

在阈值λ下，椭球的三个半轴分别是原参考半轴乘以λ的平方根。把一个单位球沿三方向拉伸，体积会依次乘上三个长度比例，因此椭球体积含有三个半轴的乘积。固定一个高度后，把该高度贡献的平方项移到右边，剩下的二维关系是一个椭圆。这样能得到体积与截面积的解析答案，作为离散网格测量的参照。

$$
V_\lambda=\frac{4\pi abc}{3}\lambda^{3/2},\qquad A_\lambda(z_0)=\pi ab\max\!\left[\lambda-\left(\frac{z_0}{c}\right)^2,0\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2a5cff4651c7a5c7f4a2bf9b.svg) | 阈值λ所定义椭球的解析体积，单位mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f957e27f053a9767e0816a17.svg) | 高度z₀处的解析截面积，单位mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | 参考半轴3、2、1 mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | 正阈值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b72465f81bed2e150afe1243.svg) | 水平切片相对中心的高度，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约为3.141593，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/61b9dc3596ef4f553078d1bb.svg) | 取u与0中较大的值；此处使不相交平面的截面积为0。 |

球体体积按三个方向的伸长比例相乘，因此椭球体积含abc与λ的3/2次方。固定z₀后，剩余两项之和为λ−(z₀/c)²，截面的两个半轴都乘以这一余量的平方根，面积则乘以余量本身。λ=1时V=4π×3×2×1/3=8π≈25.132741 mm³；z₀=0.5 mm时A=π×3×2×(1−0.25)=4.5π≈14.137167 mm²。

λ为1时，体积是8π mm³，约25.132741 mm³。在z=0.5 mm处，剩余指标为0.75，截面两个半轴约为2.598076 mm和1.732051 mm，面积为4.5π mm²，约14.137167 mm²。切片移到z=1 mm时，截面收缩为顶点，面积为零；继续向上移，就没有与椭球相交的截面。程序和交互都保留这种空截面的状态。

网格体积通过封闭的三角表面计算。代码先检查没有开放边，再读取`surface.volume`，并用每个三角面与原点组成的有向四面体体积之和独立核对。封闭性有实际意义：若切掉一半表面又没有补上切口，剩余面片就不再完整围住一个区域。给网格测量体积前，还应检查是否有自交、重复面或不一致的面方向；这些问题会影响所围区域的定义。

$$
V_h=\frac{1}{6}\left|\sum_{j=1}^{M}\mathbf p_j\cdot(\mathbf q_j\times\mathbf r_j)\right|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eea286090480eac2f8dfd8fa.svg) | 闭合、朝向一致的三角网格所围体积，单位mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 三角面总数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 三角面的编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9c8b8a36b95f4c9f91eaff7d.svg) | 第j个三角面的三个顶点相对原点的位置向量，单位mm；这里的粗体q是位置向量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fc15a27a41ba825be39eec62.svg) | 叉乘与点乘；三个向量的混合积给出带符号的平行六面体体积。 |

一个三角面与原点可以组成四面体，它的体积是相应平行六面体的六分之一。逐面保持一致朝向并累加带符号的贡献，内部重复部分会抵消，留下闭合边界的体积。三个顶点为(1,0,0)、(0,1,0)、(0,0,1) mm时，混合积为1 mm³，四面体体积为1/6 mm³。本例将这一独立求和与VTK给出的体积比较，默认网格两者均为24.597686 mm³。

截面积则由有序边界点计算。对当前单一凸椭圆，可以绕中心按极角排列交点，再用多边形面积公式求面积。若截面有多个分离区域、孔洞或凹陷，就需要保留各条交线原有的连接关系，分别处理外边界与孔洞。本节的排序函数对应凸截面这一明确条件，便于看清几何对象与测量算法如何配合。

$$
A_h=\frac12\left|\sum_{i=1}^{K}(x_i y_{i+1}-y_i x_{i+1})\right|,\qquad (x_{K+1},y_{K+1})=(x_1,y_1)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/31940250be2dad706c01f020.svg) | 切片边界围成的多边形面积，单位mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 按边界顺序排列的顶点数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 边界顶点的编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0628201b1fcd40d880b250aa.svg) | 第i个顶点的平面坐标，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bb35f800746b473b95c8a4f8.svg) | 重复第一个顶点以闭合最后一条边，单位mm。 |

相邻两点与原点构成小三角形，每项是其带符号面积的两倍；沿边界求和得到整个多边形的面积。以(0,0)、(3,0)、(3,2)、(0,2) mm组成的矩形为例，两项非零贡献各为6 mm²，最终面积为(6+6)/2=6 mm²。本章切片是单一凸多边形，角度排序可以给出连续的边界次序。带孔或相互分离的截面需要分别处理边界及其方向。

## 用加密采样判断几何结果是否稳定

固定λ为1，每个方向分别取17、33和65个点，间距依次为0.5、0.25和0.125 mm。三次计算使用相同区域、相同解析场和相同提面方法，只有采样间距改变。得到的体积约为22.987597、24.597686和24.999078 mm³，逐步接近25.132741 mm³。与直接比较渲染图片相比，这组数更清楚地揭示了分辨率的作用。

$$
e_V=100\frac{|V_h-V_\lambda|}{V_\lambda}\%,\qquad e_A=100\frac{|A_h-A_\lambda|}{A_\lambda}\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/02db18e605a00a9e29f6ccd1.svg) | 体积与截面积的相对误差，以百分数表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2ad35a603be4d743d1325439.svg) | 间距为h的网格测得的体积和截面积，单位分别为mm³与mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/161ce06a736c5e1390bbed5e.svg) | 同一阈值、同一切片位置的解析体积与截面积，单位分别为mm³与mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 采样间距，单位mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | 绝对值，保留偏差的大小。 |

先求网格值与参考值的差，再除以参考值，使不同尺寸的对象能够比较。默认体积误差为100×|24.597686−25.132741|/25.132741≈2.129%；默认面积误差约0.500%。面积为0的空切片没有可用的相对误差分母，此时页面显示面积0以及“空截面”，并保留绝对面积值。误差图的面积比较固定在z₀=0.5 mm，三个阈值下的解析面积均大于0。

相应体积误差约为8.535%、2.129%和0.532%。在这组平滑模型与网格上，间距减半后，误差约缩小到四分之一。截面积也接近解析答案，但它是不同的几何量，误差大小无需与体积完全相同。图中分别绘出两者，使我们能够看到一张切片的面积看起来已经很准确时，整个三维边界仍可能留下更明显的累计误差。

![九次实际网格提取的体积与截面积误差。两张图使用双对数坐标，面积比较固定在z₀=0.5 mm；下方表格列出每个分辨率与阈值对应的实际三角面数、体积和误差。网格间距每减半，默认阈值下的体积误差约缩小为四分之一。](https://ml-biomat.com/static/tutorials/python-scientific/figures/65d1ecfb2717e16ad0a72574.svg?v=65d1ecfb2717)

图 3九次实际网格提取的体积与截面积误差。两张图使用双对数坐标，面积比较固定在z₀=0.5 mm；下方表格列出每个分辨率与阈值对应的实际三角面数、体积和误差。网格间距每减半，默认阈值下的体积误差约缩小为四分之一。

误差图还比较了三个阈值。较小阈值对应较小的椭球，同样0.5 mm的间距对它而言更粗，因此相对误差更大。提取规则保持不变，采样尺度相对于物体尺寸的比例却发生了变化。描述分辨率时，同时给出网格间距与所研究结构的大小，比只说用了多少个点更有解释力。

加密也会增加数据量。每个方向的间隔数加倍，体单元数量会变为八倍；表面三角形数量则取决于边界怎样穿过网格。表格记录了实际面数，便于把精度与计算负担一起比较。实际体数据没有解析答案时，可以保持处理条件一致，逐步改变分辨率，观察目标量是否稳定，并结合成像分辨率与测量不确定度决定需要的精度。

## 完整程序：保存几何，也保存测量依据

下面的程序使用PyVista实际生成九张三角网格：三个阈值分别配三种分辨率。每张网格都计算封闭体积，并在六个高度生成真实切片交线。默认三维图由VTK离屏渲染，二维图与误差图由Matplotlib生成。离屏表示图像直接写入文件，便于重复生成同样的视图；在桌面交互分析中，也可以用Plotter打开可旋转窗口。

### 完整示例：从体数据生成网格、切片、量测与科学图

运行python main.py --output outputs --language zh生成中文图与全部数据；把zh改为en生成英文图。需要NumPy、PyVista与Matplotlib，PyVista安装时会带入VTK。程序逐一保存9个网格的顶点、面和6个高度的切片，默认条件为N=33、λ=1、z₀=0.5 mm。运行结果包括真实VTK渲染图、三组科学图、可重新读取的VTI/VTP几何文件以及数值摘要。

```
"""Extract, slice, measure, and render an analytical ellipsoid field with PyVista."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import pyvista as pv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib import font_manager
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

AXES = np.array([3., 2., 1.])  # mm: reference semiaxes at q = 1
RESOLUTIONS = [17, 33, 65]
LEVELS = [.5, 1., 1.5]
SLICE_Z = [0., .25, .5, .75, 1., 1.25]  # mm


def scalar_field(points):
    return np.sum((points / AXES)**2, axis=1)


def create_grid(n):
    spacing = 8. / (n - 1)
    grid = pv.ImageData(dimensions=(n, n, n), spacing=(spacing,)*3, origin=(-4.,)*3)
    grid.point_data['q'] = scalar_field(grid.points)
    return grid


def polygon_slice(surface, z):
    """Use VTK to cut the surface, then order this convex ellipse's boundary."""
    cut = surface.slice(normal=(0, 0, 1), origin=(0, 0, z))
    if cut.n_points < 3:
        return np.empty((0, 2)), 0.
    points = np.unique(cut.points[:, :2], axis=0).astype(float)
    center = points.mean(axis=0)
    order = np.argsort(np.arctan2(points[:, 1]-center[1], points[:, 0]-center[0]))
    points = points[order]
    area = abs(np.dot(points[:, 0], np.roll(points[:, 1], -1))
               - np.dot(points[:, 1], np.roll(points[:, 0], -1))) / 2
    return points, float(area)


def analytic_volume(level):
    return 4 * math.pi * np.prod(AXES) * level**1.5 / 3


def analytic_area(level, z):
    return math.pi * AXES[0] * AXES[1] * max(level-(z/AXES[2])**2, 0.)


def triangle_volume(surface):
    """Independent signed tetrahedron sum for a consistently oriented closed mesh."""
    faces = surface.faces.reshape(-1, 4)[:, 1:]
    a, b, c = (surface.points[faces[:, i]].astype(float) for i in range(3))
    return abs(float(np.sum(np.einsum('ij,ij->i', a, np.cross(b, c))) / 6))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    tr = lambda z, e: z if args.language == 'zh' else e
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ['Noto Sans CJK SC','Noto Sans SC',
        'Microsoft YaHei','SimHei','DejaVu Sans'] if f in fonts], 'font.size': 12,
        'svg.fonttype':'none', 'axes.spines.top':False, 'axes.spines.right':False, 'grid.alpha':.16})
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)

    records, mesh_bank, surfaces = [], {}, {}
    for n in RESOLUTIONS:
        grid = create_grid(n)
        for level in LEVELS:
            # A one-item list requests this value; integer 1 would request one automatic contour.
            surface = grid.contour([level], scalars='q', method='marching_cubes').triangulate()
            assert surface.n_open_edges == 0
            assert surface.is_all_triangles
            volume = float(surface.volume)
            independent = triangle_volume(surface)
            assert math.isclose(volume, independent, rel_tol=2e-7, abs_tol=2e-7)
            slices = []
            for z in SLICE_Z:
                poly, area = polygon_slice(surface, z)
                slices.append({'z':z, 'points':poly.tolist(), 'area':area,
                               'exact_area':float(analytic_area(level, z))})
            mid = slices[2]
            key = f'{n}-{level:g}'
            mesh_bank[key] = {'n':n, 'level':level, 'spacing':8/(n-1),
                'points':surface.points.tolist(), 'faces':surface.faces.reshape(-1,4)[:,1:].tolist(),
                'volume':volume, 'exact_volume':float(analytic_volume(level)), 'slices':slices}
            surfaces[key] = surface
            records.append({'n':n,'level':level,'spacing_mm':8/(n-1),'points':surface.n_points,
                'triangles':surface.n_cells,'open_edges':surface.n_open_edges,'volume_mm3':volume,
                'independent_volume_mm3':independent,'exact_volume_mm3':float(analytic_volume(level)),
                'volume_error_percent':100*abs(volume/analytic_volume(level)-1),
                'slice_area_mm2':mid['area'],'exact_slice_area_mm2':mid['exact_area'],
                'slice_error_percent':100*abs(mid['area']/mid['exact_area']-1)})
    (args.output/'mesh-bank.json').write_text(json.dumps(mesh_bank,separators=(',',':')),encoding='utf-8')
    columns=list(records[0]);np.savetxt(args.output/'convergence.csv',
        [[row[k] for k in columns] for row in records],delimiter=',',header=','.join(columns),comments='')
    default=surfaces['33-1']; default_grid=create_grid(33)
    default.save(args.output/'ellipsoid.vtp');default_grid.save(args.output/'scalar-grid.vti')
    field_plane=default_grid.slice(normal='z',origin=(0,0,.5)).triangulate()
    field_plane.save(args.output/'field-slice.vtp')
    cut_points, cut_area=polygon_slice(default,.5)

    # Render the actual VTK geometry; physical coordinates are in millimeters.
    plotter=pv.Plotter(off_screen=True,window_size=(1100,850))
    plotter.set_background('white')
    plotter.add_mesh(default,color='#477f9b',opacity=.25,smooth_shading=False)
    loop=np.column_stack([cut_points,np.full(len(cut_points),.5)])
    disk=pv.PolyData(loop,np.r_[len(loop),np.arange(len(loop))]).triangulate()
    plotter.add_mesh(disk,color='#c8753c',opacity=.85)
    plotter.add_mesh(pv.lines_from_points(loop,close=True),color='#8f451d',line_width=4)
    # Coordinate rulers sit outside the object; each tick keeps its physical position.
    ruler_origin=np.array([-3.6,-2.6,-1.4])
    label_points=[];label_text=[]
    for axis,end,ticks in [(0,3.6,[-3,0,3]),(1,2.6,[-2,0,2]),(2,1.4,[-1,0,1])]:
        endpoint=ruler_origin.copy();endpoint[axis]=end
        plotter.add_mesh(pv.Line(ruler_origin,endpoint),color='#617780',line_width=1.4)
        for tick in ticks:
            location=ruler_origin.copy();location[axis]=tick
            label_points.append(location);label_text.append(str(tick))
        middle=ruler_origin.copy();middle[axis]=(ruler_origin[axis]+end)/2
        middle[(axis+1)%3]+= .35 if axis==2 else (-1.0 if axis==0 else -.55)
        label_points.append(middle);label_text.append(['x / mm','y / mm','z / mm'][axis])
    plotter.add_point_labels(np.array(label_points),label_text,font_size=23,text_color='#263b46',
        show_points=False,shape=None,always_visible=True)
    plotter.camera_position=[(7,-10,6),(0,0,0),(0,0,1)]
    plotter.enable_parallel_projection()
    plotter.camera.zoom(.85)
    plotter.show(screenshot=args.output/'native-surface.png')

    fig,axes=plt.subplots(1,2,figsize=(13,6.2),layout='constrained',gridspec_kw={'width_ratios':[1.05,1]})
    axes[0].imshow(plt.imread(args.output/'native-surface.png'));axes[0].axis('off')
    axes[0].set_title(tr('A  等值面与内部切片的位置','A  Surface and internal slice position'))
    xy=field_plane.points[:,:2];tri=field_plane.faces.reshape(-1,4)[:,1:]
    colored=axes[1].tripcolor(mtri.Triangulation(xy[:,0],xy[:,1],tri),field_plane['q'],
        shading='gouraud',cmap='cividis',vmin=0,vmax=7)
    close=np.vstack([cut_points,cut_points[0]])
    axes[1].plot(close[:,0],close[:,1],color='#e98a43',lw=2.4,label=tr('网格切片边界','Mesh intersection'))
    theta=np.linspace(0,2*np.pi,501);radius=np.sqrt(.75)
    axes[1].plot(3*radius*np.cos(theta),2*radius*np.sin(theta),'--',color='white',lw=1.6,label=tr('解析边界','Analytical boundary'))
    axes[1].set(xlim=(-4,4),ylim=(-4,4),aspect='equal',xlabel='x / mm',ylabel='y / mm',
        title=tr('B  在z = 0.5 mm处读内部数值','B  Read values at z = 0.5 mm'))
    axes[1].legend(loc='upper right',fontsize=10)
    fig.colorbar(colored,ax=axes[1],shrink=.8,label=tr('标量q / 无量纲','Scalar q / dimensionless'))
    fig.suptitle(tr('同一体数据：N = 33，等值面q = 1','One volume dataset: N = 33, isosurface q = 1'),fontsize=16)
    save(fig,'surface-and-slice')

    # A real marching-cubes cell, plus one edge where interpolation is hand-checkable.
    cell=pv.ImageData(dimensions=(2,2,2),spacing=(.5,.5,.5),origin=(1.5,1.,.5))
    cell['q']=scalar_field(cell.points)
    patch=cell.contour([1.],scalars='q',method='marching_cubes').triangulate()
    fig=plt.figure(figsize=(12.6,6.8),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.1,1])
    ax=fig.add_subplot(gs[0],projection='3d')
    pts=cell.points
    for i in range(8):
        for j in range(i):
            if np.count_nonzero(np.abs(pts[i]-pts[j])>1e-10)==1:
                ax.plot(*np.array([pts[i],pts[j]]).T,color='#899ba6',lw=1.2)
    faces=patch.faces.reshape(-1,4)[:,1:]
    ax.add_collection3d(Poly3DCollection(patch.points[faces],facecolors='#72a7bc',edgecolors='#28658c',alpha=.65,lw=1.5))
    ax.scatter(*pts.T,c=np.where(cell['q']<1,'#28658c','#c26835'),s=48,depthshade=False)
    for point,q in zip(pts,cell['q']):ax.text(*(point+np.array([.015,.015,.025])),f'{q:.3f}',fontsize=10)
    ax.set(xlabel='x / mm',ylabel='y / mm',zlabel='z / mm',xticks=[1.5,2],yticks=[1,1.5],zticks=[.5,1],
        title=tr('A  八个采样值决定局部三角面','A  Eight samples define a local patch'))
    ax.set_box_aspect((1,1,1));ax.view_init(elev=23,azim=-63)
    ax=fig.add_subplot(gs[1]);zz=np.linspace(.5,1,200)
    ax.plot(zz,.5+zz**2,color='#28658c',lw=2.5,label=tr('解析场：q = 0.5 + (z/mm)²','Known field: q = 0.5 + (z/mm)²'))
    ax.plot([.5,1],[.75,1.5],'o--',color='#c26835',lw=2,label=tr('边上的线性插值','Linear interpolation on edge'))
    ax.axhline(1,color='#677b86',lw=1.2)
    ax.scatter([2/3,np.sqrt(.5)],[1,1],s=65,c=['#c26835','#28658c'],zorder=4)
    ax.annotate('0.6667 mm',(2/3,1),xytext=(.51,1.15),arrowprops={'arrowstyle':'->','color':'#c26835'},color='#a65329')
    ax.annotate('0.7071 mm',(np.sqrt(.5),1),xytext=(.74,.85),arrowprops={'arrowstyle':'->','color':'#28658c'},color='#28658c')
    ax.set(xlabel='z / mm',ylabel=tr('标量q / 无量纲','Scalar q / dimensionless'),
        title=tr('B  同一条边：交点怎样确定','B  One edge: locating the crossing'))
    ax.legend(loc='upper left',fontsize=10);ax.grid(True)
    fig.suptitle(tr('1987年Marching Cubes：从相邻采样值构造边界','Marching Cubes, 1987: constructing a boundary from neighboring samples'),fontsize=15)
    save(fig,'history-interpolation')

    fig=plt.figure(figsize=(12.8,8.5),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.25,1])
    axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1])]
    for level,color in zip(LEVELS,['#28658c','#2b8a74','#c26835']):
        group=[r for r in records if r['level']==level]
        for ax,key in zip(axs,['volume_error_percent','slice_error_percent']):
            ax.loglog([r['spacing_mm'] for r in group],[r[key] for r in group],'o-',color=color,lw=2,label=f'λ = {level:g}')
    for ax,title in zip(axs,[tr('A  封闭网格体积误差','A  Enclosed mesh volume error'),tr('B  z = 0.5 mm处的面积误差','B  Area error at z = 0.5 mm')]):
        ax.set(title=title,xlabel=tr('网格间距 / mm','Grid spacing / mm'),ylabel=tr('相对误差 / %','Relative error / %'))
        ax.set_xticks([.125,.25,.5],labels=['0.125','0.25','0.5']);ax.minorticks_off();ax.legend();ax.grid(True)
    ax=fig.add_subplot(gs[1,:]);ax.axis('off')
    labels=['N','h / mm','λ',tr('三角面数','Triangles'),'V / mm³',tr('体积误差 / %','Volume error / %')]
    rows=[[r['n'],f"{r['spacing_mm']:.3f}",f"{r['level']:g}",r['triangles'],f"{r['volume_mm3']:.5f}",f"{r['volume_error_percent']:.3f}"] for r in records]
    table=ax.table(cellText=rows,colLabels=labels,loc='center',cellLoc='center',bbox=[0,.0,1,.96])
    table.auto_set_font_size(False);table.set_fontsize(11)
    for (i,j),cell in table.get_celld().items():cell.set_facecolor('#eaf1f4' if i==0 else 'white');cell.set_edgecolor('#d2dfe5')
    fig.suptitle(tr('固定解析场，仅改变采样间距；参考答案由椭球公式给出',
        'One analytical field, different sample spacings; ellipsoid formulas provide the reference'),fontsize=15)
    save(fig,'convergence')

    baseline=next(row for row in records if row['n']==33 and row['level']==1)
    summary={'pyvista_version':pv.__version__,'vtk_version':pv.vtk_version_info._asdict(),
        'reference_semiaxes_mm':AXES.tolist(),'reference_volume_mm3':float(analytic_volume(1)),
        'reference_area_z05_mm2':float(analytic_area(1,.5)),'default':baseline,'records':records,
        'single_cell_triangles':patch.n_cells,'edge_linear_crossing_mm':2/3,
        'edge_exact_crossing_mm':float(np.sqrt(.5)),
        'field_slice_points':field_plane.n_points,'field_slice_triangles':field_plane.n_cells}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
```

输出中的`scalar-grid.vti`保存规则网格与q值，`ellipsoid.vtp`保存默认等值面，`field-slice.vtp`保存带数值的二维切片。它们都是可以重新读入PyVista的几何数据。`convergence.csv`保存九组结果，`summary.json`保存关键数值，`mesh-bank.json`保存供页面查看的顶点、三角面与切片。这些对象各有用途，图片负责阅读，网格和表格负责继续计算。

阅读代码时，可以先跟随create_grid、contour和slice三步，再查看体积与面积的核对函数。默认N=33、λ=1的网格有1054个顶点、2104个三角面，体积约24.597686 mm³；z=0.5 mm处的截面积约14.066500 mm²。这里的差异来自离散几何，解析参照仍然分别是25.132741 mm³和14.137167 mm²。保留数值表，便能追踪图形变化究竟来自哪一个设置。

图中的表面采用实际三角面显示，没有通过移动顶点的几何平滑来改写边界。渲染中的光照与透明度帮助看清位置，测量始终作用于同一张网格。若以后加入简化面数、平滑或修补操作，应同时保存处理前后的几何量，判断这些操作是否改变了研究关注的体积、孔径或连通关系。

## 把阈值、切片高度和网格间距分开试一遍

先保持默认阈值与分辨率，移动切片高度。三维视图中的橙色截面会向上移动，二维交线逐渐收缩，截面积随之降低；整个椭球体积保持不变。页面读取完整程序预先生成的真实网格与切片，三维显示由Plotly完成。旋转视角用于观察这些几何对象，相应二维图始终保留原来的毫米比例。

## 实验：同一个体数据，三个相互校对的视图

先移动切片，观察其位置与面积怎样同时改变；再固定高度，仅改变分辨率或阈值。三维网格和6个高度的交线均来自完整Python程序实际运行的PyVista结果。蓝色虚线给出解析截面，面积图的实线给出连续解析解，圆点对应6次原生切片。

### 三维位置：蓝色为等值面，橙色为切片

拖动三维图旋转；观察方向菜单也可用键盘操作。浅橙色平面表示切片高度，即使它已移到物体外部。三维坐标保持物理比例，下面的平面图以相同毫米尺度读取两个方向。

### 截面几何：网格与解析边界

[Figure: 等比例XY切片及解析边界](https://ml-biomat.com/tutorials/python-scientific/s07/#S07-section-svg)

### 截面积怎样随高度改变

[Figure: 解析面积曲线与6个实际网格切片的面积](https://ml-biomat.com/tutorials/python-scientific/s07/#S07-area-svg)

接着固定切片高度0.5 mm，只改变分辨率。解析椭圆与解析体积保持不变，网格边界、面数及误差更新。最后改变阈值，注意这次连解析答案也会变化，因为我们选择了另一个区域。把切片升到1.25 mm，三个可选椭球都位于它下方，截面为空；页面仍显示完整表面和体积，并把截面积记为零。

把表面不透明度提高可以体验遮挡：外表面更清楚，内部截面更难看见；降低不透明度或切换顶部视角，又能找到截面的位置。二维图提供稳定的读数依据，避免依赖三维投影猜测长度。完成这些比较后，处理真实体数据就有了一条可检查的路径：确认数值与空间坐标的对应关系，定义要提取的区域，再用切片和几何量核对三维显示。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [PyVista: Creating a Uniform Grid](https://docs.pyvista.org/examples/00-load/create_uniform_grid.html)

   点、单元、维度、原点与间距的对象定义。

   PyVista documentation and software: MIT; original example and figures here.
2. [PyVista: Contouring](https://docs.pyvista.org/examples/01-filter/contouring.html)

   从三维标量场提取等值面。

   MIT
3. [PyVista: DataSetFilters.contour](https://docs.pyvista.org/api/core/_autosummary/pyvista.datasetfilters.contour)

   等值列表、轮廓数量与marching_cubes方法参数。

   MIT
4. [PyVista: Slicing](https://docs.pyvista.org/examples/01-filter/slice.html)

   用法向与平面位置生成切片。

   MIT
5. [PyVista: PolyData.volume](https://docs.pyvista.org/api/core/_autosummary/pyvista.polydata.volume)

   由闭合三角网格测量体积。

   MIT
6. [Lorensen & Cline (1987), Marching Cubes: A High Resolution 3D Surface Construction Algorithm](https://graphics.stanford.edu/courses/cs348a-20-winter/Papers/Marching_Cubes.pdf)

   医学体数据中的等值面构造问题及边上线性插值方法。

   Original paper consulted for historical and technical facts; no paper figures reproduced.
7. [Sullivan & Kaszynski (2019), PyVista: 3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK)](https://joss.theoj.org/papers/10.21105/joss.01450)

   PyVista与VTK之间的接口关系及公开发表时间。

   JOSS article CC BY 4.0; software MIT.
