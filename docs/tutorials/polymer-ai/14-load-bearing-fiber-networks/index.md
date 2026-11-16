# 纤维网络的承载机制：取向、拉伸与弯曲

Source: https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/
Language: zh-CN

[下载代码合集 ↓](https://ml-biomat.com/static/tutorials/polymer-ai/polymer-ai-notebooks.zip)

从生物纤维的排列到图像中的力学线索

杨云浩 · 复旦大学 · 高分子与生物大分子教程

拿起一块织物，沿着经线拉与斜着拉，手上的感觉常常不同。同样多的线，换一种排列和连接方式，就能改变变形的难易。身体中的许多支撑结构也与纤维有关：肌腱需要传递拉力，血管壁需要随压力变化，皮肤需要在日常活动中伸展。本节从这些现象出发，认识胶原的层级结构，再把一张纤维图像转成可计算的方向信息。我们将训练一个小型卷积神经网络，让它同时估计排列和指定加载下的响应，并与图像测量及物理近似逐项比较。

## 01从三条分子链，到能够传力的纤维

[《高分子网络与凝胶：交联、贯通和弹性》](https://ml-biomat.com/tutorials/polymer-ai/13-networks-and-gels/)用柔性链组成的网络解释含水凝胶，并区分“存在贯通路径”与“能够抵抗指定变形”。换成纤维以后，还要考虑弯曲。一根细竹条沿长轴拉伸很费力，从侧面推却容易弯，这两种受力调用了不同的变形方式。网络中某段纤维会主要伸长还是主要弯曲，与它的方向、周围连接和加载方式有关。因此，从图像走向力学预测时，我们要逐步记录纤维在哪里、朝哪边、与谁相连，再检查模型是否保留了这些信息。

胶原提供了一个重要的生物例子。它是细胞外基质中的主要结构蛋白之一，细胞外基质可以想象成细胞周围共同建造和维护的环境，其中有纤维、含水的高分子以及多种结合分子。细胞通过与这个环境连接来感受和施加力，组织的形状也与它的结构有关。这里讨论的胶原纤维属于细胞外的支撑系统；细胞内部另有由肌动蛋白、微管等组成的骨架，两者通过细胞表面的连接共同参与力的传递。

以能够形成纤维的胶原为例，首先要看三条多肽链怎样组织成三股螺旋。可以借用三股绳的形象：每股都有自己的局部形状，三股之间还存在更高一级的缠绕关系。胶原的具体分子几何由序列、键的构型和链间相互作用共同确定，三股绳帮助我们看清层级，但不会替代这些化学细节。三股螺旋也有别于前面蛋白质章节中的α螺旋，辨认结构时需要保留这个区别。

20世纪中叶，研究者已经能从衍射图样中获得胶原的结构约束，却还需要提出能够满足这些约束的分子模型。[Ramachandran与Kartha在1954年提出胶原结构模型](https://doi.org/10.1038/174269c0)，并在[1955年继续修订三链结构](https://doi.org/10.1038/176593a0)。这段历史适合与今天的结构学习放在一起理解：观测提供可以检查的线索，模型把线索组织成空间关系，再回到观测判断哪些关系成立。随着约束增加，结构模型也会细化。

1954—1955 · 从胶原结构模型走向层级理解

[Figure: 胶原链、原纤维与网络的原创层级示意。历史起点为Ramachandran与Kartha的早期结构模型；线条展示组织关系，各层级的长度和粗细采用不同示意比例。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-collagen)

[Figure: 胶原链、原纤维与网络的原创层级示意。历史起点为Ramachandran与Kartha的早期结构模型；线条展示组织关系，各层级的长度和粗细采用不同示意比例。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-collagen)

**图1** 胶原链、原纤维与网络的原创层级示意。历史起点为Ramachandran与Kartha的早期结构模型；线条展示组织关系，各层级的长度和粗细采用不同示意比例。

分子继续聚集，可以形成更粗的原纤维，原纤维又参与组织更高一级的纤维结构。走到组织尺度，纤维之间的位置、方向、连接和周围含水环境共同决定力怎样传递。可以把这条路线看成从“绳股怎样组成绳子”走到“绳子怎样织成网”。若研究的是分子稳定性，三股螺旋及其相互作用很重要；若研究一小片网络怎样受力，首先需要的是纤维几何、连接处的约束和每段纤维的力学性质。

不同层级还对应不同的测量。分子结构实验提供局部构象信息，显微图像可以显示纤维分布，加载实验则记录力与变形。一张二维图中两根亮线相交，可能是真实连接，也可能是不同深度的投影重叠。要把图像转换成承载网络，可以借助三维成像、交联标记或其他结构证据确定交点性质。在本节的受控计算中，交点明确设为焊接，这使连接的含义能够直接进入求解。

生物网络还会随制备状态和受力状态改变。弯曲或起伏的纤维受到拉伸时，可能先变直，随后才明显伸长；细胞也会在较长时间里改建周围结构。因此，“这张图对应怎样的样品状态”与“图上有多少纤维”同样重要。我们先研究一个较清楚的起点：平面内的直纤维、固定的连接和小变形。等这些关系被逐项理解，便能继续加入起伏、三维组织或随时间变化的连接。

## 02把“朝哪边排列”变成可测量的数

先在纸上画几根平行线。沿任意一根从左端走到右端，与从右端走到左端，看到的是同一根纤维。因此，描述这种结构时，0度和180度应当代表同一个方向。如果直接对普通角度求平均，两根分别朝向1度和179度的线会得到90度，恰好指向与它们几乎垂直的位置。问题来自角度的表示方式，而非计算器的算术：我们的数据需要尊重纤维没有指定头尾这一事实。

解决办法是先把角度乘2，再计算正弦与余弦。相差180度的两根纤维，二倍角相差360度，在圆上回到同一点。用一对数q_{x}、q_{y}保存平均结果，就可以绕开角度跨越边界的麻烦。若各段长度不同，还可以让长段占较多权重：这里问的是网络总长度如何分配到不同方向，而非图中画出了多少条编号不同的线。

先解决一根纤维有两个等价朝向的问题

qx=ΣLa cos(2θa)/ΣLa，qy=ΣLa sin(2θa)/ΣLa；S2=√(qx²+qy²)。La是平面内第a段纤维长度，θa是相对于水平轴的无头尾方向。二倍角使相差180度的方向相同。

下标a遍历所有纤维段，L_{a}是第a段长度，θ_{a}是它相对于水平轴的方向。分子将每段长度乘相应的方向分量后相加，分母除以总长度，因此q的两个分量都没有单位。S_{2}是这对分量形成的向量长度，范围从0到1。所有纤维平行时，它们在二倍角圆上指向同一处，平均后长度仍为1；方向互相抵消时，平均向量就会缩短。

可以亲手算一个例子。两段长度相等的纤维，一段水平，另一段与水平成45度。它们的二倍角向量分别是(1,0)与(0,1)，平均得到q=(0.5,0.5)，所以S_{2}=√0.5，约为0.707。把向量q的方向角除以2，得到主要排列方向22.5度。这一方向落在两根线之间，符合几何直觉；当q恰好为0时，主要方向没有唯一值，应保留方向分布本身。

S_{2}也会丢失信息。若一半长度水平、一半竖直，两组二倍角向量为(1,0)与(−1,0)，相加为0；均匀分布在平面各方向的纤维，同样得到0。前者具有清楚的两组正交排列，后者各方向等价。要区分它们，可以继续查看完整角度分布，或加入四倍角的正弦、余弦统计。用少数数字概括结构时，理解哪些差别被平均掉了，是选择AI输入的重要一步。

排列与熵之间还有一段有意思的科学史。[Onsager在1949年讨论细长胶体的形状与相互作用](https://doi.org/10.1111/j.1749-6632.1949.tb27296.x)，其中包括棒状粒子的取向。想象在桌上移动几根细棒：方向杂乱时，每根棒周围需要避让的区域较大；较为平行时，一些位置安排反而更容易实现。平行排列减少了方向选择，却可能增加位置安排的余地，两种熵的变化需要一起计入。这帮助我们理解，出现有序方向也可以来自总体自由能的降低。

1949 · 有序排列怎样与熵联系起来

[Figure: 细棒取向与位置安排的原创示意。位置和方向自由度共同进入统计描述；图中棒的位置用于解释几何关系。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-onsager)

[Figure: 细棒取向与位置安排的原创示意。位置和方向自由度共同进入统计描述；图中棒的位置用于解释几何关系。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-onsager)

**图2** 细棒取向与位置安排的原创示意。位置和方向自由度共同进入统计描述；图中棒的位置用于解释几何关系。

Onsager的研究讨论可重新安排的粒子体系，本节焊接纤维网的方向则由生成时的几何确定。两者共享“需要描述取向”的问题，而形成取向的机制不同。对数据建模也要作同样区分：测得方向分布，解决的是结构表征；解释这个分布怎样产生，还需要浓度、流动、相互作用或加工过程等信息。[《从分子到样品：制备、加工与层级结构》](https://ml-biomat.com/tutorials/polymer-ai/15-processing-and-hierarchy/)会进一步把制备过程接到这些可观察的结构上。

现在把手绘的线换成显微图像。图像由像素亮度组成，并没有直接告诉我们每根纤维的中心线在哪里。一个有用的线索是：沿亮纤维前进时，亮度变化通常较慢；横穿纤维边缘时，亮度变化较快。把水平方向的亮度变化记为I_{x}，竖直方向记为I_{y}，再对邻近像素的乘积作平滑平均，就得到下面的结构张量。这里的I表示图像亮度，稍后梁公式中的截面二次矩也使用字母I，两者由所在问题区分。

沿纤维走与横穿纤维，亮度变化的程度不同

图像结构张量J由局部亮度梯度Ix、Iy的乘积加权平均组成。λ1≥λ2≥0为两个特征值，局部方向一致性c=(λ1−λ2)/(λ1+λ2)，分母为0的空白位置不取方向。较小特征值的特征向量沿亮度变化较慢的方向。

尖括号表示在一个小邻域内加权平均，离中心近的像素权重较大。矩阵J整理了横向、纵向变化及两者共同变化的程度。特征向量可以理解为这个矩阵选出的两条主要方向，特征值则描述沿这些方向的变化强弱。较小特征值对应亮度变化较慢的方向，因而可用来估计纤维走向。两特征值接近时，局部没有突出的单一方向；差别较大时，方向线索更明确。

例如某个小区域得到J=diag(9,1)，表示沿水平的亮度变化较强、沿竖直较弱，于是估计纤维接近竖直。方向一致性c=(9−1)/(9+1)=0.8。若两个特征值均为5，c=0，局部可能包含交叉纹理或其他近乎各向同性的图案。完全空白处两个值都接近0，程序根据梯度能量筛掉这些像素，避免让没有可见结构的位置影响方向统计。

[Rezakhaniha等人在2012年发表的研究](https://doi.org/10.1007/s10237-011-0325-z)把胶原纤维的起伏和取向测量与动脉外膜结构联系起来。他们对离体兔颈总动脉进行荧光标记和共聚焦成像，并比较完整与切开状态下的组织。样品的状态会影响观测到的方向分布，这说明方向统计需要与制样和力学状态一起记录。图像分析因此不仅是把亮线描出来，还要让测量结果对应一个明确的实验对象。

2012 · 胶原成像把排列与样品状态联系起来

[Figure: 按Rezakhaniha等人的研究问题绘制的原创概念图：组织状态、显微测量、方向统计。曲线与柱形用于解释流程，实验纤连蛋白图像见下方实测分析。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-measurement)

[Figure: 按Rezakhaniha等人的研究问题绘制的原创概念图：组织状态、显微测量、方向统计。曲线与柱形用于解释流程，实验纤连蛋白图像见下方实测分析。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-measurement)

**图3** 按Rezakhaniha等人的研究问题绘制的原创概念图：组织状态、显微测量、方向统计。曲线与柱形用于解释流程，实验纤连蛋白图像见下方实测分析。

下面使用另一种细胞外基质蛋白——纤连蛋白——的公开实验图像。图像由[Arafat等人的2025年纤维追踪比较研究](https://doi.org/10.1371/journal.pone.0320006)提供。纤连蛋白与胶原的分子结构和生物作用各有特点，这里选择它，是为了实际演示如何从具有背景、交叉和亮度变化的纤维图像读取方向。原始观测、计算方向、方向叠加和分布图并排展示，便于判断算法究竟读取了哪些可见线索。

一张实验图像 · 四种观察方式

![A｜作者提供的纤连蛋白荧光图像。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/3964827db1aed03eab078334.svg)

A｜作者提供的纤连蛋白荧光图像。

![B｜所选像素的局部方向，角度按无头尾方向标示。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/70f0ec1f767def5344d9ad32.svg)

B｜所选像素的局部方向，角度按无头尾方向标示。

![C｜将估计方向叠加在观测上，短线沿局部纤维排列。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/a1824bb2aa14e95264d61cba.svg)

C｜将估计方向叠加在观测上，短线沿局部纤维排列。

![D｜按梯度能量加权的方向分布；不同方向的柱高之和为1。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/7d7cf91b026bd0a391f52839.svg)

D｜按梯度能量加权的方向分布；不同方向的柱高之和为1。

**图4** 原始图像：Youssef Arafat、Cristina Cuesta-Apausa、Esther Castellano、Constantino Carlos Reyes-Aldasoro，2025年纤维追踪研究的作者数据；[原文以CC BY发表](https://doi.org/10.1371/journal.pone.0320006)。方向图、叠加图与分布由本页代码计算。分析排除边缘与右下标注，采用1像素梯度平滑和3像素张量平滑，筛选条件见正文。

程序先将RGB图像转为亮度，再用1像素尺度的高斯平滑抑制细小波动，用3像素尺度平均梯度乘积。分析区域避开10像素边缘和右下方标注；在区域内保留梯度能量不低于第60百分位、且c至少为0.2的位置。最后约35.17%的全图像素参与统计。这样得到的是具有较明确方向线索的位置所组成的图像测量，其数值会随平滑尺度和选点条件变化。

对所选像素按梯度能量加权，本次取向向量约为(−0.0337,0.6485)，方向分布偏向右上方。这里的权重与前面精确几何中的长度权重不同：亮而清晰的边缘会提供更多梯度信号，所以两种测量即使使用相同二倍角表达式，也在汇总不同对象。后面的受控数据同时保留精确线段和含噪图像，便能检查成像与估计带来的偏差。

## 03纤维可以伸长，也可以弯曲

方向明确之后，还需要回答力怎样传递。把一根细杆沿长度拉开，主要改变各小段的长度；从侧面推弯它，则让杆的一侧较伸长、另一侧较压缩。后一种变形与截面上材料离中性轴的距离有关：材料分布得越远，抵抗弯曲的能力通常越强。我们用细梁模型将这两项贡献分别计算，再把所有纤维段连接成网络。

细长结构可以通过拉长，也可以通过弯曲来变形

细梁的轴向能Us=(EA/2)∫(du平行/ds)²ds，弯曲能Ub=(EI/2)∫(d²v/ds²)²ds。s为沿初始纤维的长度坐标，u平行为轴向位移，v为横向位移；E为杨氏模量，A为截面积，I为截面二次矩。这里采用小变形Euler–Bernoulli梁，忽略剪切变形。

s表示沿初始纤维的长度坐标，u_{∥}是轴向位移，v是横向位移。第一个导数du_{∥}/ds表示相邻位置的轴向位移差除以距离，也就是小应变；二阶导数d²v/ds²描述斜率沿长度怎样改变，在小变形下对应曲率变化。平方使伸长与压缩、向上与向下弯曲都消耗正能量。积分则把沿纤维各小段的贡献累加起来，作用与把很多很短的段逐段求和相同。

E是杨氏模量，单位为力除以面积；A是截面积，因此EA具有力的单位。I是截面二次矩，单位为长度的四次方，所以EI具有力乘长度平方的单位。轴向应变没有单位，乘EA再沿长度积分得到能量；曲率具有长度倒数的单位，平方后乘EI并积分，同样得到力乘长度。按单位逐项检查，可以帮助理解为什么两个能量式中分别出现EA和EI。

一个容易计算的情况，是把梁的一端位置和转角固定，另一端自由转动，再在自由端施加力。这就是悬臂梁。横着推与沿轴向拉会得到下面两种位移关系。横向式中的L³意味着，在其他条件相同时，长度加倍会使横向位移增至8倍；轴向位移则只增至2倍。因此，同样材质的细长结构，经常表现出容易弯曲、较难拉长的差别。

拉同一根细杆与横向掰弯它，需要不同的力

长度L的悬臂梁，一端位移与转角固定、另一端施加横向力且自由转动时，端位移δ垂直=FL³/(3EI)；相应轴向受力位移δ平行=FL/(EA)。两式均为小变形线性关系。

F为施加的力，L为梁长，δ_{⊥}和δ_{∥}分别为横向与轴向端位移。取一个教学算例：长度单位为ℓ₀，力单位为F₀，设L=ℓ₀、EA=F₀、EI=0.0005F₀ℓ₀²，并施加F=10^{−5}F₀。轴向位移为10^{−5}ℓ₀，横向位移约为0.006667ℓ₀，两者相差约667倍。这个差别来自给定的细梁参数和边界条件，程序也用同一个解析结果核对梁单元。

在网络中，一根原始纤维被交点分成多个梁段。每个节点有三个自由度：水平位移、竖直位移和转角。焊接意味着相接的梁段共享这些节点变量，交点处可以传递力，也可以传递弯矩；若连接允许自由转动，就要修改转角约束。程序将每段的局部伸长与弯曲关系转换到统一坐标系，再把同一节点受到的贡献相加。自由节点达到平衡时，合力和合力矩都为0。

边界条件决定我们到底在测什么。本例在边长为ℓ₀的正方形内生成纤维，纤维与正方形边界相交的端点按指定单轴应变移动，边界转角固定为0；内部节点则自由平移和转动。所有边界节点都遵循同一条位移规则。这样，当加载方向改变时，定义仍然清楚，也便于同时旋转样品和加载来检查计算。

同一张纤维图，需要配上明确的加载条件

边界节点位移uB=ε[n·(rB−r0)]n，边界转角ψB=0。r0是正方形中心，n是单轴加载方向的单位向量，ε为给定小应变；内部节点的二维平移与转角自由调整。

r_{B}是边界节点的初始位置，r₀是正方形中心，n是加载方向的单位向量，ε为小应变。点积n·(r_{B}−r₀)量出该节点沿加载方向离中心多远，再乘ε得到它沿该方向应移动的距离。水平加载时n=(1,0)，于是水平位移为ε(x−x₀)、竖直位移为0。ε取0.001时，左右两侧相对分开的距离为0.001ℓ₀。

边界确定以后，让内部节点调整到总能量最低的位置。在线性模型中，应变增大一倍，位移也增大一倍，能量随之增至4倍。因而可以用一个系数C概括这套加载下的二次能量响应，再除以EAℓ₀得到没有单位的数c_{C}，作为学习模型的目标。这里的C具有能量单位；把二维网络结果联系到三维实验模量时，还需要样品体积、厚度和相应加载定义。

二维框架的能量响应，按自己的单位报告

网络能量响应系数C=2Umin/ε²；无量纲响应cC=C/(EAℓ0)。Umin是给定边界后的最低总能量，ε为无量纲应变，EA为轴向刚性尺度，ℓ0为长度单位。C具有能量单位。

例如，ε=0.001时求得U_{min}=2×10^{−6}EAℓ₀，代入得到C=4EAℓ₀，故c_{C}=4。若把ε改为0.0005，同一个线性系统的能量降到5×10^{−7}EAℓ₀，算出的C仍为4EAℓ₀。这说明C提取的是当前结构与边界条件下的响应尺度，而非一次任选加载幅度的能量。后面的图和误差都用EAℓ₀作为C的单位。

还可以先做一个更简单的方向实验：让所有点都跟随均匀单轴应变，不允许内部另外调整，暂时只计轴向能量。方向为θ的纤维承受的轴向应变为εcos²(θ−α)，其中α是加载角度；能量与应变平方成正比，于是出现cos⁴(θ−α)。下面按总纤维长度归一化，显示这个四次投影的平均值D。它把“方向怎样参与承载”单独拿出来，完整网络的弯曲与内部调整仍由后面的梁计算处理。

方向相同的纤维，换个方向拉会怎样？

二倍角分量 q**(1.00, 0.00)**排列统计 S₂**1.000**轴向能量投影 D**1.000**

[Figure: 水平平行纤维受水平加载，方向投影为1](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#fiber-network)

平行纤维与加载同向，cos⁴投影的长度平均为1。

**图5** 等总长度、均匀单轴应变下的轴向能量投影，D=ΣL cos⁴(θ−α)/ΣL。绿色为纤维方向，棕色箭头为加载方向；相交线用于表示方向族。连续变化展示准静态角度扫描，可暂停；关闭脚本时保留平行排列的静态图。

平行纤维沿自身方向加载时D=1，转为垂直加载时D=0。两组等长正交纤维沿其中一组加载，D=(1+0)/2=0.5；将加载转过45度，两组各自贡献cos⁴45°=0.25，平均仍为0.25。两种情况下S_{2}都为0，承载投影却会改变。这正好接回前面的统计问题：二倍角概括了部分排列特征，而四倍角或更完整的几何信息还会影响力学。

对完整网络，也可以构造一个物理参照：让所有节点都按边界的均匀位移规则移动，并将节点转角设为0，再计算伸长和弯曲总能量。这组试探位移满足边界条件，因此最低能量不会高于它，得到的C就是一个上界。内部节点能调整得越充分，精确解与这个上界之间可能相差越多。这个参照既能检查求解结果，也能作为容易计算的结构特征。

## 04让图像模型读出排列与加载响应

前面已有两条计算路线：从精确几何求解力学，或从像素梯度估计方向。现在让AI直接读图，学习哪些局部图样与取向、承载有关。一张48×48像素图像包含2304个亮度值；把它按固定顺序铺成一行仍能保存数值，但模型还需要知道哪些位置在图上相邻。**卷积神经网络**直接利用这种空间关系：用一个小窗口扫过图像，在不同位置重复同一组计算。像拿一个小放大镜逐处查看，某些窗口会响应边缘，另一些会响应交叉或不同方向的线段；这些局部结果再组合成整张图的预测。

[LeCun、Bottou、Bengio与Haffner在1998年的论文](https://doi.org/10.1109/5.726791)中系统讨论了基于梯度学习的文档识别，其中卷积网络把局部连接、共享权重和逐层表示结合起来。手写数字的笔画与显微图中的纤维具有不同含义，却都包含位置相邻的图像线索。同一类局部计算可以在图像不同位置重复使用，训练则决定哪些组合有助于当前任务。

1998 · 从文档识别认识卷积与共享权重

[Figure: LeCun等人的卷积学习思路与本节图像任务的原创示意。历史研究面向文档识别，右侧为本节构建的取向和加载响应分支。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-ai)

[Figure: LeCun等人的卷积学习思路与本节图像任务的原创示意。历史研究面向文档识别，右侧为本节构建的取向和加载响应分支。](https://ml-biomat.com/tutorials/polymer-ai/14-load-bearing-fiber-networks/#history-ai)

**图6** LeCun等人的卷积学习思路与本节图像任务的原创示意。历史研究面向文档识别，右侧为本节构建的取向和加载响应分支。

先只看第一层。取一个3×3的小窗口，给九个位置各配一个权重，将亮度乘权重后相加，再加偏置，得到一个输出。窗口向右或向下移动时，继续使用同一组权重。这就是权重共享：模型学习“怎样识别一种局部模式”，无需为图中每个位置分别学习一套规则。实际第一层有8组窗口权重，产生8张特征图。

卷积将局部邻域变成可学习的图像特征

第一层单通道图像卷积：za(i,j)=ba+ΣrΣs Wa(r,s)I(i+r,j+s)，r和s各取−1、0、1；ha=max(0,za)。I为像素亮度，Wa为第a个3×3滤波器的训练权重，ba为偏置。

i、j是窗口中心的像素位置，r、s各取−1、0、1，标出相邻位置；W_{a}是第a组权重，b_{a}是偏置。假设一个窗口三列亮度分别为0、0.5、1，三行相同，权重每行设为(−1,0,1)，偏置为0，则加权和为3。把亮暗左右交换后得到−3。ReLU函数取输入与0的较大值，所以两者输出分别为3和0。训练中的权重由数据调整，这个手算窗口只帮助我们看清计算过程。

本例连续使用三层卷积，每层后接ReLU和2×2平均池化。平均池化把相邻四个值取平均，图像边长依次从48变为24、12和6，通道数依次为8、12和16。最终得到6×6×16=576个数，再转换为64维表示。局部窗口在更深层间接覆盖原图更大的范围，模型因而有机会组合线段和交叉关系；能学到多少，仍要回到新网络的预测结果来评价。

这64个数分成两个输出分支。取向分支输出q的两个分量，若向量长度超过1，就按比例缩回单位圆内，使输出符合取向定义。力学分支还接收加载方向的二倍角分量cos2α、sin2α，因为相同图像在不同加载下可能有不同响应。它输出一个经过softplus变换的非负值，用来预测对数响应t。把加载条件明确接入，模型才能学习“这张网在这次加载下怎样响应”。

一个图像表示，服务于取向和加载响应两个输出

取向与响应共同训练：t=ln(1+cC)，L=(1/2n)Σ||q̂a−qa||²+(1/n)Σ(t̂a−ta)²。n是当前样本数，取向有两个分量，因此第一项按2n平均。标签来自精确几何与独立梁计算，两个输出分别评价。

先用C除以EAℓ₀，再取ln(1+c_{C})，保证对数中的数没有单位。c_{C}=0时t=0，c_{C}=1时t≈0.693，c_{C}=3时t≈1.386；对数让较大的响应被适度压缩。损失函数中n为当前样本数，帽号表示预测，第一项对两个取向分量及所有样本求平均，第二项对对数响应误差求平均。二者相加参与训练，最终仍分别报告两项任务的误差。

一个模型共有41935个可训练参数。程序用三个不同初始化分别训练，种子固定为14、24和34，每次最多80轮，用验证集选择保留的轮次。训练样本分批进入模型，Adam根据损失的梯度更新参数。取向输出对三个模型求平均；响应先平均三个对数输出，再用指数还原。平均的位置会影响结果，因而代码保留完整定义，方便从保存的参数复算预测。

旋转提供了一项有明确预期的检查。把网络和加载方向一起转过90度，物理能量应保持不变，取向q则因二倍角表示而变成−q。训练时随机使用0、90、180和270度旋转，同步修改加载输入与取向标签。测试时还可以对四种旋转分别预测，将取向转回原坐标后求平均，同时平均对数响应。这个操作使四种直角旋转得到一致结果，也让“旋转应怎样影响输出”成为模型设计的一部分。

为了看清学习方法带来的作用，本例安排了几种输入清楚的参照。最简单的回归只用纤维总长度、条数和总长度的平方；图像特征回归从同一幅含噪图像提取亮度、梯度能量及相对于加载方向的二倍角和四倍角统计。另一个几何特征回归使用精确节点、梁段、连接度及方向信息，并加入仿射能量上界。最后还直接报告这个物理上界与精确解的差别。

图像特征回归与CNN面对的是同样的观察图像，可以用来比较手工定义特征与学习图像表示。几何回归和物理上界拥有精确线段与连接，输入更充分，它们帮助回答“若结构已经测清，还能做到什么程度”。所有回归的标准化都使用训练集统计，正则化强度从固定候选中由验证集选择。把数据来源与模型一起报告，才容易判断误差差别来自观察信息、特征设计，还是学习方法。

## 05运行代码，再用结果选择下一步

下面的完整程序生成240个母网络，每个由6到10根平面直纤维组成。方向分布包含较分散和较集中的情况，纤维裁切在正方形内，相交位置形成焊接节点；过短的梁段被排除，以保持数值条件稳定。每个母网络生成两种模糊与噪声程度的48×48图像，再分别进行水平和竖直加载，因此共有480幅观察图像、960条图像与加载记录。

同一个母网络的四条记录共享精确几何，所以它们一起进入训练、验证或测试集合。三组母网络数量为144、48和48，对应576、192和192条记录。这样的分组让测试真正面对新网络，避免把同一张网的另一幅噪声图或另一种加载当成独立新对象。所有测试母网络的标签都由梁平衡计算给出，CNN训练时只读取指定图像与加载输入。

代码还会下载前面展示的纤连蛋白实验图像，核对固定版本文件的校验值，执行结构张量分析，并生成四幅实验图和六幅受控学习结果图。第一次运行需要联网取得该图像，后续使用本地缓存；数据生成、力学求解、模型训练和绘图均在下面展开。运行所需的库列在代码栏，输出目录保存样本、模型参数、预测及可再次使用的图件。

完整Python例子 · NumPy · SciPy · PyTorch · scikit-learn · Matplotlib · Pillow · requests[下载代码](https://ml-biomat.com/static/tutorials/polymer-ai/assets/cc5fbe9520a205fa0a3ea24e.py)

```python
"""Read fiber orientation and predict a controlled frame response from images.

Dependencies: numpy, scipy, torch, scikit-learn, matplotlib, Pillow, requests.
Simulation uses fixed EA=1 and EI=.0005, length unit l0=1, small strain .001.
All crossings are welded and all boundary rotations are fixed.
Real fibronectin image: Arafat et al., PLOS ONE (2025), doi:10.1371/journal.pone.0320006.
The author-provided TIFF is downloaded once and SHA256 checked.
Experimental image analysis is separate from simulated mechanical learning.
"""
from pathlib import Path
import os,copy,json,hashlib
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from scipy.ndimage import gaussian_filter,sobel
import torch
from torch import nn
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from PIL import Image
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
OUT=Path('fiber_outputs')
torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)

def beam(xa,xb,EA=1.,EI=.0005):
    d=xb-xa;L=float(np.linalg.norm(d));c,s=d/L
    local=np.zeros((6,6));local[np.ix_([0,3],[0,3])]=EA/L*np.array([[1,-1],[-1,1]])
    ids=[1,2,4,5]
    local[np.ix_(ids,ids)]=EI/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
    R=np.array([[c,s,0],[-s,c,0],[0,0,1.]])
    T=np.zeros((6,6));T[:3,:3]=R;T[3:,3:]=R
    return T.T@local@T

def stiffness_matrix(x,edges,EA=1.,EI=.0005):
    K=np.zeros((3*len(x),3*len(x)))
    for i,j in edges:
        ids=np.r_[np.arange(3*i,3*i+3),np.arange(3*j,3*j+3)]
        K[np.ix_(ids,ids)]+=beam(x[i],x[j],EA,EI)
    return K

def response(x,edges,boundary,direction,epsilon=.001,EA=1.,EI=.0005):
    x=np.array(x);n=np.array(direction);K=stiffness_matrix(x,edges,EA,EI)
    fixed=np.array([d for i in boundary for d in [3*i,3*i+1,3*i+2]])
    free=np.setdiff1d(np.arange(len(K)),fixed);u=np.zeros(len(K))
    affine=epsilon*np.outer((x-.5)@n,n)
    u.reshape(-1,3)[boundary,:2]=affine[boundary]
    if len(free):u[free]=np.linalg.solve(K[np.ix_(free,free)],-K[np.ix_(free,fixed)]@u[fixed])
    force=K@u;energy=float(.5*u@force)
    residual=float(max(abs(force[free]),default=0));assert residual<1e-7
    return dict(response=2*energy/epsilon**2,energy=energy,displacement=u.reshape(-1,3).tolist(),residual=residual)

def geometry(rng):
    while True:
        count=int(rng.integers(6,11));mean=rng.uniform(0,np.pi);concentration=float(rng.choice([0.,1.,3.,7.]))
        angles=(rng.vonmises(2*mean,concentration,count)/2)%np.pi
        segments=[]
        for a in angles:
            direction=np.array([np.cos(a),np.sin(a)]);normal=np.array([-direction[1],direction[0]])
            point=np.array([.5,.5])+rng.uniform(-.36,.36)*normal
            hits=[]
            for axis in [0,1]:
                if abs(direction[axis])<1e-10:continue
                for side in [0.,1.]:
                    t=(side-point[axis])/direction[axis];q=point+t*direction
                    if -1e-10<=q[1-axis]<=1+1e-10:hits.append((t,q))
            hits.sort(key=lambda z:z[0]);segments.append(np.array([hits[0][1],hits[-1][1]]))
        nodes=[];boundary=[];locations=[[] for _ in segments]
        for i,seg in enumerate(segments):
            for t,point in [(0.,seg[0]),(1.,seg[1])]:
                k=len(nodes);nodes.append(point);boundary.append(k);locations[i].append((t,k))
        for i in range(count):
            for j in range(i+1,count):
                a,b=segments[i];c,d=segments[j];matrix=np.column_stack([b-a,-(d-c)])
                if abs(np.linalg.det(matrix))<1e-9:continue
                t,s=np.linalg.solve(matrix,c-a)
                if 1e-9<t<1-1e-9 and 1e-9<s<1-1e-9:
                    k=len(nodes);nodes.append(a+t*(b-a));locations[i].append((t,k));locations[j].append((s,k))
        x=np.array(nodes);edges=[]
        for loc in locations:
            loc.sort();edges.extend((a[1],b[1]) for a,b in zip(loc[:-1],loc[1:]))
        edges=np.array(edges);length=np.linalg.norm(x[edges[:,1]]-x[edges[:,0]],axis=1)
        if length.min()<.008:continue
        n=(x[edges[:,1]]-x[edges[:,0]])/length[:,None]
        q=np.sum(length[:,None]*np.c_[n[:,0]**2-n[:,1]**2,2*n[:,0]*n[:,1]],axis=0)/length.sum()
        return dict(x=x.tolist(),edges=edges.tolist(),boundary=boundary,segments=np.array(segments).tolist(),
                    fiber_count=count,mean_angle=mean,concentration=concentration,length=float(length.sum()),q=q.tolist())

def render(g,rng,variant=0,noise_override=None):
    side=48;yy,xx=np.mgrid[:side,:side];xx=xx/(side-1);yy=1-yy/(side-1)
    points=np.stack([xx,yy],axis=-1);signal=np.zeros((side,side))
    for start,end in np.array(g['segments']):
        d=end-start;t=np.clip(np.sum((points-start)*d,axis=-1)/(d@d),0,1)
        distance=np.linalg.norm(points-(start+t[...,None]*d),axis=-1)
        signal=np.maximum(signal,np.exp(-.5*(distance/.009)**2))
    blur=.35 if variant==0 else .7;noise=.035 if variant==0 else .08
    if noise_override is not None:noise=noise_override
    observed=.08+.8*gaussian_filter(signal,blur)+rng.normal(0,noise,signal.shape)
    return np.clip(observed,0,1).astype(np.float32),signal>.5

def orientation(image):
    smooth=gaussian_filter(image.astype(float),.8)
    gx=sobel(smooth,axis=1)/8;gy=-sobel(smooth,axis=0)/8
    gx=gx[2:-2,2:-2];gy=gy[2:-2,2:-2]
    xx=float(np.sum(gx*gx));yy=float(np.sum(gy*gy));xy=float(np.sum(gx*gy))
    return np.array([yy-xx,-2*xy])/(xx+yy+1e-12)

def generate():
    rng=np.random.default_rng(1414);parents=[];images=[];rows=[]
    for i in range(240):
        g=geometry(rng);g['group']=i;g['split']='test' if i%5==0 else 'validation' if i%5==1 else 'train'
        loads=[response(g['x'],g['edges'],g['boundary'],n) for n in [[1.,0.],[0.,1.]]]
        g['loading_results']=loads;parents.append(g)
        for variant in range(2):
            observed,mask=render(g,rng,variant);image_index=len(images);images.append(observed)
            q=orientation(observed)
            for axis in [0,1]:
                rows.append(dict(group=i,split=g['split'],variant=variant,image_index=image_index,
                    loading=[1.,0.] if axis==0 else [0.,1.],response=loads[axis]['response'],
                    q_true=g['q'],q_image=q.tolist()))
    return parents,np.array(images),rows


def descriptors(g,loading):
    x=np.array(g['x']);edges=np.array(g['edges']);d=x[edges[:,1]]-x[edges[:,0]]
    length=np.linalg.norm(d,axis=1);angle=np.arctan2(d[:,1],d[:,0])-np.arctan2(loading[1],loading[0])
    degree=np.bincount(edges.ravel(),minlength=len(x))
    moments=[float(np.sum(length*f(m*angle))/length.sum()) for m in [2,4] for f in [np.cos,np.sin]]
    affine=np.zeros((len(x),3));n=np.array(loading);affine[:,:2]=np.outer((x-.5)@n,n)
    v=affine.ravel();upper=float(v@stiffness_matrix(x,edges)@v)
    count=[g['length'],g['fiber_count'],g['length']**2]
    rich=count+[len(x),len(edges),float(length.mean()),float(length.std()),float(degree.max()),float(degree.mean()),float(degree.std())]+moments+[upper]
    return count,rich

def image_descriptors(image,loading):
    a=gaussian_filter(image.astype(float),.8);gx=sobel(a,1)[2:-2,2:-2]/8;gy=-sobel(a,0)[2:-2,2:-2]/8
    weight=gx*gx+gy*gy;total=weight.sum()+1e-12
    theta=np.arctan2(gy,gx)+np.pi/2-np.arctan2(loading[1],loading[0])
    moments=[float(np.sum(weight*f(m*theta))/total) for m in [2,4] for f in [np.cos,np.sin]]
    density=float(image.mean());spread=float(image.std())
    return [density,spread,float(weight.mean()),*moments,*[density*v for v in moments],density*density]

class ImageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),
            nn.Conv2d(8,12,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),
            nn.Conv2d(12,16,3,padding=1),nn.ReLU(),nn.AvgPool2d(2))
        self.shared=nn.Sequential(nn.Flatten(),nn.Linear(16*6*6,64),nn.ReLU())
        self.qhead=nn.Linear(64,2)
        self.response=nn.Sequential(nn.Linear(66,32),nn.ReLU(),nn.Linear(32,1))
    def forward(self,image,loading):
        h=self.shared(self.conv(image));q=self.qhead(h)
        q=q/torch.linalg.vector_norm(q,dim=1,keepdim=True).clamp(min=1)
        value=torch.nn.functional.softplus(self.response(torch.cat([h,loading],dim=1)))
        return torch.cat([q,value],dim=1)

def metrics(rows,pred,ids):
    pred=np.asarray(pred,dtype=float)
    y=np.array([rows[i]['response'] for i in ids]);value=np.expm1(pred[ids,2]);q=np.array([rows[i]['q_true'] for i in ids])
    return dict(RMSE=float(np.mean((value-y)**2)**.5),MAE=float(np.mean(abs(value-y))),
                log_RMSE=float(np.mean((pred[ids,2]-np.log1p(y))**2)**.5),q_component_RMSE=float(np.mean((pred[ids,:2]-q)**2)**.5))

def infer(model,images,loads,symmetrized=False):
    predictions=[]
    with torch.no_grad():
        for start in range(0,len(images),64):
            batch=images[start:start+64];v=loads[start:start+64];values=[]
            for k in range(4 if symmetrized else 1):
                sign=(-1)**k
                result=model(torch.rot90(batch,k,[2,3]),sign*v)
                result[:,:2]*=sign;values.append(result)
            predictions.append(torch.stack(values).mean(0).numpy())
    return np.concatenate(predictions)

def main():
    OUT.mkdir(exist_ok=True)
    parents,images,rows=generate();bygroup={g['group']:g for g in parents}
    ids={s:np.array([i for i,r in enumerate(rows) if r['split']==s]) for s in ['train','validation','test']}
    arrays=[descriptors(bygroup[r['group']],r['loading']) for r in rows]
    features={'counts':np.array([a[0] for a in arrays]),'geometry_graph':np.array([a[1] for a in arrays])}
    features['image_features']=np.array([image_descriptors(images[r['image_index']],r['loading']) for r in rows])
    target=np.array([[*r['q_true'],np.log1p(r['response'])] for r in rows])
    observed=np.array([r['q_image'] for r in rows]);result={'baselines':{},'cnn':{},'split_counts':{k:len(v) for k,v in ids.items()}}
    for name,X in features.items():
        scale=StandardScaler().fit(X[ids['train']]);Z=scale.transform(X);best=None;candidates=[]
        for alpha in [.01,.1,1.,10.,100.]:
            model=Ridge(alpha=alpha).fit(Z[ids['train']],target[ids['train'],2])
            pred=np.maximum(0,model.predict(Z));loss=float(np.mean((pred[ids['validation']]-target[ids['validation'],2])**2))
            candidates.append(dict(alpha=alpha,validation_loss=loss))
            if best is None or loss<best[0]:best=(loss,model,alpha,pred)
        p=np.c_[observed,best[3]]
        result['baselines'][name]=dict(predictions=p.tolist(),scores={s:metrics(rows,p,j) for s,j in ids.items()},
            alpha=best[2],scaler_mean=scale.mean_.tolist(),scaler_scale=scale.scale_.tolist(),
            coef=best[1].coef_.tolist(),intercept=float(best[1].intercept_),validation_candidates=candidates)
    # Direct affine trial energy is an upper bound and uses only input geometry.
    p=np.c_[observed,np.log1p(features['geometry_graph'][:,-1])]
    result['baselines']['affine_upper_bound']=dict(predictions=p.tolist(),scores={s:metrics(rows,p,j) for s,j in ids.items()})
    t=torch.tensor(target,dtype=torch.float32)
    im=torch.tensor(images[[r['image_index'] for r in rows],None],dtype=torch.float32)
    loading=torch.tensor([[r['loading'][0]**2-r['loading'][1]**2,2*r['loading'][0]*r['loading'][1]] for r in rows])
    def lossfn(p,y):return torch.mean((p[:,:2]-y[:,:2])**2)+torch.mean((p[:,2]-y[:,2])**2)
    saved=[];raws=[];sym=[]
    noisy=[]
    for i,image in enumerate(images):
        g=parents[i//2];image2,_=render(g,np.random.default_rng(4141+i),variant=1,noise_override=.16);noisy.append(image2)
    noisy=torch.tensor(np.array(noisy)[[r['image_index'] for r in rows],None],dtype=torch.float32)
    noisy_preds=[];rotated=[]
    for seed in [14,24,34]:
        torch.manual_seed(seed);model=ImageModel();optimizer=torch.optim.Adam(model.parameters(),lr=.001)
        rng=np.random.default_rng(1415);bestloss=float('inf');wait=0;history=[]
        for epoch in range(1,81):
            model.train();order=rng.permutation(ids['train'])
            for start in range(0,len(order),64):
                ix=order[start:start+64];k=int(rng.integers(0,4));sgn=(-1)**k
                batch=torch.rot90(im[ix],k,[2,3]);truth=t[ix].clone();truth[:,:2]*=sgn
                optimizer.zero_grad();loss=lossfn(model(batch,sgn*loading[ix]),truth);loss.backward();optimizer.step()
            model.eval()
            with torch.no_grad():
                vl=float(lossfn(model(im[ids['validation']],loading[ids['validation']]),t[ids['validation']]))
                tl=float(lossfn(model(im[ids['train']],loading[ids['train']]),t[ids['train']]))
            history.append(dict(epoch=epoch,train=tl,validation=vl))
            if vl<bestloss-1e-7:bestloss=vl;bestepoch=epoch;weights=copy.deepcopy(model.state_dict());wait=0
            else:wait+=1
            if wait>=12:break
        model.load_state_dict(weights);model.eval()
        raw=infer(model,im,loading);s=infer(model,im,loading,True)
        rot=infer(model,torch.rot90(im,1,[2,3]),-loading);rot[:,:2]*=-1
        raws.append(raw);sym.append(s);rotated.append(rot);noisy_preds.append(infer(model,noisy,loading,True))
        saved.append(dict(seed=seed,best_epoch=bestepoch,history=history,parameters=sum(p.numel() for p in model.parameters()),
                          state_dict={k:v.numpy().tolist() for k,v in weights.items()}))
        print('seed',seed,'best epoch',bestepoch,'validation loss',bestloss,flush=True)
    avg=np.mean(raws,axis=0);sy=np.mean(sym,axis=0);noise=np.mean(noisy_preds,axis=0);rot=np.mean(rotated,axis=0)
    result['cnn']=dict(seeds=saved,raw_predictions=avg.tolist(),symmetrized_predictions=sy.tolist(),
        noisy_predictions=noise.tolist(),rotated_back_predictions=rot.tolist(),
        scores_raw={s:metrics(rows,avg,j) for s,j in ids.items()},
        scores_symmetrized={s:metrics(rows,sy,j) for s,j in ids.items()},
        scores_noisy_test=metrics(rows,noise,ids['test']),
        rotation_raw_q_RMSE=float(np.mean((rot[ids['test'],:2]-avg[ids['test'],:2])**2)**.5),
        rotation_raw_response_MAE=float(np.mean(abs(np.expm1(rot[ids['test'],2])-np.expm1(avg[ids['test'],2])))))
    result['orientation_baseline_test_RMSE']=float(np.mean((observed[ids['test']]-target[ids['test'],:2])**2)**.5)
    result['scope']='Generated 2D Euler-Bernoulli frames; prescribed affine boundary strain; C=2U/epsilon^2 in EA*l0 units.'
    result['parents']=parents
    result['generator_seed']=1414
    result['experimental_image']=experimental_analysis()
    make_plots(parents,images,rows,result,OUT)
    for i,row in enumerate(rows):
        row['cnn_prediction']=result['cnn']['symmetrized_predictions'][i]
        row['baseline_predictions']={name:m['predictions'][i] for name,m in result['baselines'].items()}
    (OUT/'samples.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    np.save(OUT/'images.npy',images)
    print(json.dumps({'baselines':{k:v['scores']['test'] for k,v in result['baselines'].items()},
          'raw':result['cnn']['scores_raw']['test'],'symmetrized':result['cnn']['scores_symmetrized']['test'],
          'noise':result['cnn']['scores_noisy_test'],'orientation_baseline':result['orientation_baseline_test_RMSE']},indent=2))


def make_plots(parents,images,rows,r,out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
        'text.color':'#29433a','axes.labelcolor':'#29433a','svg.hashsalt':'L14-fibers','axes.titlepad':15,
        'figure.facecolor':'#fffdf8','savefig.facecolor':'#fffdf8'})
    out.mkdir(exist_ok=True);test=np.array([i for i,x in enumerate(rows) if x['split']=='test'])
    row=rows[test[0]];g=parents[row['group']];x=np.array(g['x']);edges=np.array(g['edges'])
    cnn=np.array(r['cnn']['symmetrized_predictions']);base=np.array(r['baselines']['image_features']['predictions'])
    names=['counts','image_features','cnn','geometry_graph','affine_upper_bound']
    labels=['Fiber / length counts','Measured image features','Image CNN + four rotations','Known geometry / graph','Affine physical upper bound']
    def draw(ax,key):
        if key=='observation':
            ax.axis('off');ax.set_title('A  Known geometry and an imperfect image')
            left=ax.inset_axes([.02,.12,.45,.77]);right=ax.inset_axes([.53,.12,.45,.77])
            left.add_collection(LineCollection(x[edges],colors='#43816b',linewidths=1.7));left.scatter(x[:,0],x[:,1],s=7,c='#ae8053')
            left.set(xlim=(0,1),ylim=(0,1),aspect='equal',title='Explicit welded crossings');left.axis('off')
            right.imshow(images[row['image_index']],cmap='gray',vmin=0,vmax=1,extent=(0,1,0,1));right.set_title('48 x 48 observed pixels');right.axis('off')
            ax.text(.5,.02,'First held-out parent; two imaging variants stay in the same group',ha='center',transform=ax.transAxes,fontsize=8)
        elif key=='orientation':
            ax.axis('off');ax.set_title('B  Direction is an axis, without an arrowhead')
            polar=ax.inset_axes([.02,.16,.43,.7],projection='polar');vec=ax.inset_axes([.58,.18,.38,.64])
            d=x[edges[:,1]]-x[edges[:,0]];length=np.linalg.norm(d,axis=1);theta=np.arctan2(d[:,1],d[:,0])%np.pi
            bins=np.linspace(0,np.pi,19);hist,_=np.histogram(theta,bins=bins,weights=length);hist/=hist.sum();centers=(bins[:-1]+bins[1:])/2
            polar.bar(np.r_[centers,centers+np.pi],np.tile(hist,2),width=np.pi/18*.9,color='#8eb19c')
            polar.set_yticks([]);polar.tick_params(labelsize=8);polar.set_title('Length-weighted directions',fontsize=9)
            for q,c,label in [(g['q'],'#ae8053','Geometry'),(row['q_image'],'#6589a2','Structure tensor'),(cnn[test[0],:2],'#267b69','Image CNN')]:
                vec.quiver(0,0,q[0],q[1],angles='xy',scale_units='xy',scale=1,color=c,width=.012,label=label)
            circle=np.linspace(0,2*np.pi,100);vec.plot(np.cos(circle),np.sin(circle),':',c='#c8c8bd')
            vec.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),aspect='equal',xlabel='q_x')
            vec.text(.03,.97,'q_y',ha='left',va='top',transform=vec.transAxes,fontsize=9)
            vec.legend(fontsize=7,loc='upper center',bbox_to_anchor=(.5,-.17));vec.grid(alpha=.15)
        elif key=='deformation':
            ax.set_title('C  Internal nodes translate and rotate')
            ax.add_collection(LineCollection(x[edges],colors='#c9cec3',linewidths=1))
            u=np.array(g['loading_results'][0]['displacement']);curves=[];amp=80
            for a,b in edges:
                d=x[b]-x[a];L=np.linalg.norm(d);t=d/L;normal=np.array([-t[1],t[0]])
                s=np.linspace(0,1,15);axial=(1-s)*(u[a,:2]@t)+s*(u[b,:2]@t)
                bend=(1-3*s*s+2*s**3)*(u[a,:2]@normal)+L*(s-2*s*s+s**3)*u[a,2]+(3*s*s-2*s**3)*(u[b,:2]@normal)+L*(-s*s+s**3)*u[b,2]
                curves.append(x[a]+s[:,None]*d+amp*(axial[:,None]*t+bend[:,None]*normal))
            ax.add_collection(LineCollection(curves,colors='#397d67',linewidths=1.6))
            boundary=g['boundary'];moved=x+amp*u[:,:2];ax.scatter(moved[boundary,0],moved[boundary,1],s=18,c='#ae8053',label='Prescribed boundary nodes')
            ax.set(xlim=(-.1,1.1),ylim=(-.1,1.1),aspect='equal',xlabel='x / l0',ylabel='y / l0')
            ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.13));ax.text(.5,.98,'x-directed affine boundary strain; displacements x 80',ha='center',va='top',transform=ax.transAxes,fontsize=8)
        elif key=='prediction':
            truth=np.array([rows[i]['response'] for i in test])
            ax.scatter(truth,np.expm1(base[test,2]),s=19,c='#c29a6e',alpha=.55,label='Measured image features')
            ax.scatter(truth,np.expm1(cnn[test,2]),s=19,c='#397e69',alpha=.55,label='Image CNN + four rotations')
            limit=max(truth.max(),np.expm1(cnn[test,2]).max());ax.plot([0,limit],[0,limit],':',color='#8c8f7b')
            ax.set(xlabel='Independent beam solution / (EA l0)',ylabel='Prediction / (EA l0)',title='D  Response on 48 unseen parent networks')
            ax.legend(fontsize=8);ax.grid(alpha=.12)
        elif key=='scores':
            vals=[r['cnn']['scores_symmetrized']['test']['RMSE'] if n=='cnn' else r['baselines'][n]['scores']['test']['RMSE'] for n in names]
            ax.barh(range(5),vals,color=['#bcc3b2','#b89b77','#448c73','#6b91aa','#91b0a0']);ax.set_yticks(range(5),labels,fontsize=8);ax.invert_yaxis()
            for i,v in enumerate(vals):ax.text(v+.025,i,f'{v:.3f}',va='center',fontsize=9)
            ax.set(xlim=(0,max(vals)*1.17),xlabel='Response RMSE / (EA l0)',title='E  Compare models with their input information')
            ax.grid(axis='x',alpha=.12)
        elif key=='checks':
            ax.axis('off');ax.set_title('F  Noise and a joint 90-degree rotation')
            left=ax.inset_axes([.13,.18,.38,.66]);right=ax.inset_axes([.67,.18,.29,.66])
            vals=[r['orientation_baseline_test_RMSE'],r['cnn']['scores_symmetrized']['test']['q_component_RMSE'],r['cnn']['scores_noisy_test']['q_component_RMSE']]
            left.bar(range(3),vals,color=['#6b91aa','#448c73','#bc986b']);left.set_xticks(range(3),['Tensor','CNN','CNN\nmore noise'],fontsize=8)
            left.set_ylabel('q-component RMSE');left.grid(axis='y',alpha=.12)
            right.bar([0,1],[r['cnn']['rotation_raw_response_MAE'],0],color=['#9aaea0','#397e69'])
            right.set_xticks([0,1],['Raw','Four-rotation\naverage'],fontsize=8);right.set_ylabel('Prediction change / (EA l0)')
            right.text(1,0,'0 by symmetry',ha='center',va='bottom',rotation=90,fontsize=8)
            ax.text(.5,.02,'Orientation uses q = <cos(2theta), sin(2theta)>; response rotation moves loading too.',ha='center',transform=ax.transAxes,fontsize=8)
    keys=['observation','orientation','deformation','prediction','scores','checks']
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.8,5.4),layout='constrained');draw(ax,key)
        fig.savefig(out/(key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(15.6,16.2),layout='constrained')
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(out/'fiber_learning.png',dpi=160);fig.savefig(out/'fiber_learning.svg',metadata={'Date':None});plt.close(fig)


def tensor(image,roi=None):
    smooth=gaussian_filter(image.astype(float),1.)
    gx=sobel(smooth,axis=1)/8;gy=-sobel(smooth,axis=0)/8
    xx=gaussian_filter(gx*gx,3);yy=gaussian_filter(gy*gy,3);xy=gaussian_filter(gx*gy,3)
    energy=xx+yy;difference=np.sqrt((xx-yy)**2+4*xy*xy)
    coherency=difference/(energy+1e-15)
    theta=(.5*np.arctan2(-2*xy,yy-xx))%np.pi
    valid=np.zeros_like(image,dtype=bool);valid[10:-10,10:-10]=True
    if roi is not None:valid&=roi
    threshold=np.percentile(energy[valid],60)
    valid&=(energy>=threshold)&(coherency>=.2)
    q=np.array([np.sum(energy[valid]*np.cos(2*theta[valid])),np.sum(energy[valid]*np.sin(2*theta[valid]))])/np.sum(energy[valid])
    return dict(theta=theta,coherency=coherency,energy=energy,valid=valid,q=q,threshold=threshold)

def experimental_analysis():
    path=OUT/'Fluorescent_Fibronectin.tif'
    url='https://raw.githubusercontent.com/youssefarafat/Trace_Ridges/ab919e66a0f65b10b6aeb51d7510aedc8e0200dc/Fluorescent_Fibronectin.tif'
    if not path.exists():
        response=requests.get(url,timeout=40);response.raise_for_status();path.write_bytes(response.content)
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='d9107c136570141d3fe55c9ad8ef4dbf71ffb27e9abbe2bda2efed65be2bc18a'
    img=Image.open(path);raw=np.array(img)
    assert raw.ndim==3 and raw.shape[2]==3,raw.shape
    original=(raw.astype(float)@np.array([.299,.587,.114]))/np.iinfo(raw.dtype).max
    roi=np.ones(original.shape,dtype=bool);roi[-70:,-230:]=False
    data=tensor(original,roi);rotated=tensor(np.rot90(original),np.rot90(roi))
    error=float(np.max(abs(data['q']+rotated['q'])))
    assert error<1e-12
    e=data['energy'];coh=data['coherency'];theta=data['theta'];v=data['valid']
    # Independently recover the local director as the smaller-eigenvalue eigenvector.
    smooth=gaussian_filter(original,1);gx=sobel(smooth,1)/8;gy=-sobel(smooth,0)/8
    xx=gaussian_filter(gx*gx,3);yy=gaussian_filter(gy*gy,3);xy=gaussian_filter(gx*gy,3)
    points=np.argwhere(v)[::401];maxerr=0
    for row,col in points:
        _,vec=np.linalg.eigh([[xx[row,col],xy[row,col]],[xy[row,col],yy[row,col]]])
        n=vec[:,0];q=np.array([n[0]**2-n[1]**2,2*n[0]*n[1]])
        target=np.array([np.cos(2*theta[row,col]),np.sin(2*theta[row,col])])
        maxerr=max(maxerr,float(np.max(abs(q-target))))
    assert maxerr<1e-12
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'L14-fibronectin','font.size':10,'figure.facecolor':'#fffdf8','savefig.facecolor':'#fffdf8'})
    def draw(ax,key):
        if key=='source':
            ax.imshow(original,cmap='gray');ax.set_title('A  Author-provided fibronectin image');ax.axis('off')
        elif key=='directions':
            show=np.where(v,theta*180/np.pi,np.nan)
            im=ax.imshow(show,cmap='twilight',vmin=0,vmax=180)
            ax.figure.colorbar(im,ax=ax,label='Local direction / degrees',shrink=.7)
            ax.set_title('B  Selected local fiber directions');ax.axis('off')
        elif key=='overlay':
            ax.imshow(original,cmap='gray',alpha=.65)
            sy,sx=np.mgrid[20:raw.shape[0]-20:32,20:raw.shape[1]-20:32];ok=v[sy,sx];angle=theta[sy,sx]
            xxp=sx[ok];yyp=sy[ok];tt=angle[ok]
            ax.quiver(xxp,yyp,np.cos(tt),-np.sin(tt),angles='xy',scale_units='xy',scale=.06,color='#d9b46d',width=.003,headwidth=0,headlength=0,headaxislength=0,pivot='mid')
            ax.set_title('C  Local directions over the observation');ax.axis('off')
        else:
            bins=np.linspace(0,np.pi,37);hist,_=np.histogram(theta[v],bins=bins,weights=e[v]);hist/=hist.sum()
            ax.bar((bins[:-1]+bins[1:])*90/np.pi,hist,width=4.5,color='#488b76')
            ax.set(xlabel='Unoriented direction / degrees',ylabel='Gradient-energy weighted fraction',title='D  Image orientation distribution')
    keys=['source','directions','overlay','distribution']
    for key in keys:
        fig,ax=plt.subplots(figsize=(6,5.5),layout='constrained');draw(ax,key)
        fig.savefig(OUT/('experimental_'+key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(10,9),layout='constrained')
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(OUT/'experimental_orientation.png',dpi=150);fig.savefig(OUT/'experimental_orientation.svg',metadata={'Date':None});plt.close(fig)
    report=dict(source='https://raw.githubusercontent.com/youssefarafat/Trace_Ridges/ab919e66a0f65b10b6aeb51d7510aedc8e0200dc/Fluorescent_Fibronectin.tif',
        commit='ab919e66a0f65b10b6aeb51d7510aedc8e0200dc',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        authors='Youssef Arafat, Cristina Cuesta-Apausa, Esther Castellano, Constantino Carlos Reyes-Aldasoro',
        paper='https://doi.org/10.1371/journal.pone.0320006',year=2025,
        image_credit='Author-provided fluorescent fibronectin image from the original study; analysis reproduced with attribution.',
        article_license='CC BY',
        shape=list(raw.shape),dtype=str(raw.dtype),frames=getattr(img,'n_frames',1),
        grayscale_conversion='RGB luminance .299R+.587G+.114B, divided by255; source unchanged',
        excluded_annotation_rectangle_xy=[raw.shape[1]-230,raw.shape[0]-70,raw.shape[1],raw.shape[0]],
        roi_rotation='The exclusion mask is rotated together with the image.',
        gray_range=[int(raw.min()),int(raw.max())],q=data['q'].tolist(),selected_fraction=float(v.mean()),
        gradient_smoothing_pixels=1,tensor_smoothing_pixels=3,coherency_minimum=.2,energy_percentile=60,
        joint_image_rotation_q_max_error=error,independent_eigenvector_max_error=maxerr,independent_points=len(points),
        scope='Experimental image direction statistics and rotation consistency; synthetic frame mechanics is a separate controlled task.',passed=True)
    return report


if __name__=='__main__':main()
```

本次实际运行输出

```
seed 14 best epoch 80 validation loss 0.03153904527425766
seed 24 best epoch 80 validation loss 0.035696081817150116
seed 34 best epoch 78 validation loss 0.024649973958730698
{
  "baselines": {
    "counts": {
      "RMSE": 2.184109706028288,
      "MAE": 1.6633560434004035,
      "log_RMSE": 0.5796652485604395,
      "q_component_RMSE": 0.054425075431559666
    },
    "geometry_graph": {
      "RMSE": 0.3501040830902298,
      "MAE": 0.2587263696719076,
      "log_RMSE": 0.07921421075909235,
      "q_component_RMSE": 0.054425075431559666
    },
    "image_features": {
      "RMSE": 0.5406790104401736,
      "MAE": 0.4050663988981846,
      "log_RMSE": 0.13428835744137654,
      "q_component_RMSE": 0.054425075431559666
    },
    "affine_upper_bound": {
      "RMSE": 0.25185043255758677,
      "MAE": 0.20799889695623808,
      "log_RMSE": 0.07637942942534165,
      "q_component_RMSE": 0.054425075431559666
    }
  },
  "raw": {
    "RMSE": 0.4729237470985272,
    "MAE": 0.3423421384715237,
    "log_RMSE": 0.131414948785789,
    "q_component_RMSE": 0.07320922186943177
  },
  "symmetrized": {
    "RMSE": 0.45988866865746236,
    "MAE": 0.3292228551667617,
    "log_RMSE": 0.128078960424268,
    "q_component_RMSE": 0.07022957296014173
  },
  "noise": {
    "RMSE": 0.4771642361895034,
    "MAE": 0.3980660329185934,
    "log_RMSE": 0.1709621562184005,
    "q_component_RMSE": 0.08348743179595684
  },
  "orientation_baseline": 0.054425075431559666
}
```

A图先把同一个留出母网络的精确几何和观察图像放在一起。左图的交点、梁段与边界位置由生成过程明确记录；右图经过模糊和噪声，局部交叉与邻近线条可能更难分辨。看见这种差别，就能理解为什么“有一张照片”和“知道完整网络”是不同的数据条件，也能理解为何需要在含噪观察上评价图像方法。

B图展示长度加权方向分布，并把几何标签、结构张量估计和CNN预测放到q平面中。方向分布在相差180度的位置重复，反映纤维无头尾的定义。q平面中的点越靠近圆周，二倍角平均的长度越大；点接近中心时，需要进一步查看分布，判断是方向分散还是多组方向互相抵消。比较三个点的位置，则能直观看到两种图像估计偏离几何标签的程度。

C图显示给定加载后的梁网络。节点之间的曲线由梁的横向位移和转角重建，因而能够显示弯曲，位移放大80倍以便观察。求解仍使用0.001的小应变，图中放大的轮廓用于看清内部调整。与所有节点均匀移动的试探相比，内部自由度会重新分配伸长与弯曲能量，网络也由此找到较低的总能量状态。

一次运行 · 六幅结果图

![A｜同一个母网络的精确连接几何与48×48含噪观察图像。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/427c38e3df3811279d511af2.svg)

A｜同一个母网络的精确连接几何与48×48含噪观察图像。

![B｜长度加权的纤维方向分布，与几何、结构张量和图像CNN得到的二维取向向量。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/56aa4f64aa6511500738379a.svg)

B｜长度加权的纤维方向分布，与几何、结构张量和图像CNN得到的二维取向向量。

![C｜给定单轴边界应变后，内部节点的平移和转角；位移放大80倍显示。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/fd49eb4f89dd807f03dc7480.svg)

C｜给定单轴边界应变后，内部节点的平移和转角；位移放大80倍显示。

![D｜48个留出母网络上的192条加载图像：直接梁解与两种图像预测。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/ff4f4d700f7d124b008df75f.svg)

D｜48个留出母网络上的192条加载图像：直接梁解与两种图像预测。

![E｜按实际输入信息比较能量响应系数的均方根误差。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/22e4441b752618aece063db1.svg)

E｜按实际输入信息比较能量响应系数的均方根误差。

![F｜取向误差、成像噪声与网络和加载一起旋转90度后的预测一致性。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/9f2a6106fdc88593d36637e4.svg)

F｜取向误差、成像噪声与网络和加载一起旋转90度后的预测一致性。

**图7** 240个母网络，每个包含两种成像变体及两个正交加载，共960条记录；按母网络划分为144/48/48个训练、验证和测试对象。交叉处焊接，边界位移随指定单轴应变变化，边界转角为0。目标C=2U/ε²，图中以EAℓ₀为单位；实验纤连蛋白图像另作取向分析。

[矢量组图SVG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/1267d60dc9bc8ee6bd85cd2b.svg)[高清组图PNG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/e2bc31a3a739aa9905d6adc0.png)[完整样本JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/9c55045c3356ffd5d997c84d.json)[模型与结果JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/0b3fe9f7f2b07b7fa9478b88.json)

D图比较192条测试记录的预测和精确力学响应，横轴来自梁求解，纵轴来自图像方法，落在对角线附近表示两者接近。图像特征回归的RMSE为0.5407EAℓ₀，经过四种旋转平均的CNN为0.4599EAℓ₀。RMSE是误差平方的平均再开平方，会突出较大的偏差；对应MAE分别为0.4051与0.3292EAℓ₀，表示平均绝对偏差。本次受控任务中，CNN从图像学习的表示改善了这两项响应误差。

E图把五种方法放在一起。计数回归、图像特征回归、旋转平均CNN、精确几何回归及仿射物理上界的RMSE依次约为2.1841、0.5407、0.4599、0.3501和0.2519EAℓ₀。图中同时标明输入条件，便于把结果与已有信息联系起来：只统计总量会丢失大量方向与连接差别，图像保留了空间线索，而精确几何还能支持直接的物理近似。

物理上界在本例中与精确解较接近，也与这里的网络和边界有关。许多长纤维直接连接到受规定应变的边缘，均匀试探位移已经能够描述部分变形。若研究内部自由调整更明显、连接更稀疏或初始起伏更强的网络，可以重新检查上界与精确解的距离，再决定需要怎样的学习模型。这个比较把AI放回研究流程：先利用已有的可计算关系，再评估学习能补充哪些结构信息。

F图的取向任务给出了另一种排序。按q的两个分量计算RMSE，结构张量为0.0544，原始CNN为0.0732，旋转平均CNN为0.0702。这个合成成像条件下，沿亮度梯度估计方向的简单方法更准确。因此，若当前研究只需要取向，可以优先使用结构张量；若还要学习包含连接和加载效应的响应，CNN的另一分支提供了额外功能。两个任务分别评价，才能保留这种有用差别。

增加观察噪声后，旋转平均CNN的响应RMSE为0.4772EAℓ₀，取向分量RMSE为0.0835。原始CNN在网络与加载共同旋转90度时，响应预测的平均绝对变化为0.1255EAℓ₀；四种旋转平均则按构造保持这组旋转下的一致性。前者检查成像质量变化，后者检查坐标变换。它们各自对应明确的研究条件，比单独观察训练损失更能说明模型会怎样被使用。

实验纤连蛋白图像的检查也回到测量定义。把图像和排除标注的区域一起旋转90度，q应变成−q，本次计算在浮点精度内满足这一关系。这个检查确认坐标与方向计算配合正确；若要进一步衡量实验图上的方向准确度，可以标注一批局部纤维方向，并在相同区域比较。若希望预测实验材料的承载，还要取得对应样品的连接证据、几何尺寸、纤维参数和力学加载数据，建立成对的结构与响应记录。

从三股螺旋到纤维网络，再到图像中的方向和一次加载响应，我们不断选择与问题相符的尺度。AI沿着这条路线接收观测，物理定义则规定输出的含义，并提供解析算例、能量上界和旋转关系来检验结果。[《从分子到样品：制备、加工与层级结构》](https://ml-biomat.com/tutorials/polymer-ai/15-processing-and-hierarchy/)将把视线移到样品形成的过程：同样的分子，经过怎样的浓度变化、流动和加工，才会产生不同的排列与层级结构；这些过程记录又怎样帮助模型提出可实行的制备方案。

## 资料与延伸阅读

Ramachandran与Kartha，1954，[Structure of Collagen](https://doi.org/10.1038/174269c0)；1955，[Structure of Collagen](https://doi.org/10.1038/176593a0)。两篇早期论文用于连接衍射约束、分子模型与胶原层级结构；历史图为按概念关系绘制的原创示意。

Onsager，1949，[The Effects of Shape on the Interaction of Colloidal Particles](https://doi.org/10.1111/j.1749-6632.1949.tb27296.x)；Rezakhaniha等，2012，[Experimental investigation of collagen waviness and orientation in the arterial adventitia using confocal laser scanning microscopy](https://doi.org/10.1007/s10237-011-0325-z)。前者提供取向与位置自由度的历史线索，后者把胶原图像测量接到具体组织与样品状态。

LeCun等，1998，[Gradient-Based Learning Applied to Document Recognition](https://doi.org/10.1109/5.726791)；Arafat等，2025，[Fibre tracing in biomedical images: An objective comparison between seven algorithms](https://doi.org/10.1371/journal.pone.0320006)。实验图像来自后者的作者数据仓库；六幅学习结果图来自本页代码的受控梁网络计算，参数、样本与预测可在结果区下载。
