# 坐标、矩阵与一把可靠的图像尺

Source: https://ml-biomat.com/tutorials/python-scientific/p10/
Language: zh-CN

用刻度尺建立像素尺度，沿残差理解最小二乘，再让矩阵转动整组坐标。

## 照片中的一百个像素，究竟有多长

给一根细纤维拍照后，我们很容易在图上数出它跨过了多少个像素。像素是图像中的采样位置，它还没有告诉我们纤维在现实中有多长。同一根纤维换一个放大倍数，可以占据完全不同的像素数；相机稍微转动，原来几乎水平的纤维还会变成斜线。要从照片获得可比较的长度，需要分别处理两件事：用已知尺度建立像素与毫米的联系，再把方向和坐标表达清楚。本章用一个小型标定实验把这两件事连接起来，学习矩阵乘法、向量长度和最小二乘。

设想把一把有刻度的标尺放进视野，在六个已知位置读取图像坐标。我们使用一组构造的教学记录：标尺位置依次为0、2、4、6、8、10 mm，对应像素读数为1、42、80、120、162、201 px。这些数接近一条直线，又保留了一点读数差异，便于把每一步算清楚。这里的0 mm是标尺选择的参考点，1 px是该点在图像读数中的位置；两个零点来自不同的坐标系统，没有理由天然重合。记录里的小差异则可以来自取整或定位过程，在本例中只作为已给定的读数偏离处理。

随后考虑一块在图像中横跨200 px、纵跨80 px的矩形区域。我们约定它的左下角是几何计算的原点，像素为正方形，横纵方向使用同一个尺度，并把纵轴转成向上的数学方向。这样，标定负责决定这块区域有几毫米宽，旋转负责决定各顶点在新位置的坐标。真实相机若有明显畸变，或横纵方向的尺度不同，应分别建立相应的标定关系；本章的计算对应视野内尺度一致的平面图像。

这条流程也适用于显微图像中的颗粒轮廓、拉伸照片中的标记点，以及扫描图上的尺寸测量。它把一个常见误会拆开了：图形在屏幕上转动，不等于物体变长；像素数字变成毫米，也不等于只换了坐标轴上的文字。前者需要保持距离的几何变换，后者需要具有单位的比例关系。把两步写成数组操作后，成百上千个点都能遵循同样的规则。

## 从“向右两步、向上一步”理解向量

先看一个最简单的点：从原点向右走2 mm，再向上走1 mm，就到达坐标为(2,1) mm的位置。这一对数可以写成向量，理解为一支从原点指向该点的箭头。箭头的两个分量分别记录水平和竖直位移，箭头本身的长度则是从起点直达终点的距离。两条直角边组成一个直角三角形，因而可以用勾股定理计算距离。分量的正负表示方向，平方之后再相加才得到与方向无关的长度。

$$
r=\|\mathbf v\|_2=\sqrt{x^2+y^2},\qquad \mathbf v=\begin{bmatrix}x\\y\end{bmatrix}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 箭头长度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/771507e21f2935d77160257f.svg) | 平面位移向量，两个分量均为mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | 水平与竖直位移，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ab7d58f94422b5ef65d1d1a3.svg) | 欧氏长度；下标2指平方和再开方的规则 |

对互相垂直、使用相同长度单位的两轴应用勾股定理。x=2 mm、y=1 mm时，r=√5 mm≈2.236 mm；转成(-1,2) mm后仍得到同一个长度。平方项为mm²，开平方恢复mm。

如果把整支箭头逆时针转90°，它会指向(-1,2) mm。新位置的横坐标为负，表示在原点左边；它并没有产生“负长度”。转动前后的距离都是根号5 mm，约2.236 mm。这个手算例子很适合检查程序：如果旋转后得到(1,-2)，方向转反了；如果得到(0,0)，则很可能把矩阵运算误写成了另一种操作。理解坐标的几何含义之后，几行数字就具有了可检验的物理意义。

在NumPy中，我们把多个点排成一个二维数组，每一行是一点，每一列是一种坐标分量。矩形的四个顶点因此构成形状为(4,2)的数组。这里的4表示点数，2表示每一点有两个分量；它与上一章“每一行是一轮实验”的数组外形相似，但两条轴的含义已经不同。对这个数组调用`np.linalg.norm(points, axis=1)`，就是在每行内部把两个分量合成一个长度，结果有四个数。省略轴参数会把整个数组合成一个数，回答的便不是逐个顶点离原点多远。

原点的选择也要始终一致。矩形四个顶点到左下角的距离依次是0、10、约10.770、4 mm；若把原点改成矩形中心，这四个距离都会改变，而任意两顶点之间的距离保持不变。计算两点距离时，先用终点坐标减去起点坐标，再对所得位移向量求长度，就会自然消去共同的坐标原点。这也是图像测量常常先求两点之差的原因。

![原始蓝色矩形与红色旋转矩形、单位方向箭头和保持不变的四个距离。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8554335f5254083deae87940.svg?v=8554335f5254)

图 1同一矩形在标定后的毫米坐标中逆时针旋转30°。右上角画出旋转矩阵两列对应的单位方向；右下角逐个比较顶点到原点的距离。几何面板横纵等比例。

## 矩阵的两列，描述两根方向箭头怎样转动

一个平面方向可以由“向右一单位”和“向上一单位”这两根基本箭头组合出来。点(2,1)就是两根水平单位箭头，加上一根竖直单位箭头。旋转时，只要知道这两根基本箭头分别转到哪里，就能把原来的组合一起转过去。旋转矩阵的第一列记录水平单位箭头的新分量，第二列记录竖直单位箭头的新分量。矩阵乘法所做的，正是按原来两个分量给这两列加权，再相加。

$$
\theta=\frac{\pi\phi}{180},\qquad \begin{bmatrix}x^\prime\\y^\prime\end{bmatrix}=\underbrace{\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}}_{R}\begin{bmatrix}x\\y\end{bmatrix}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | 以度为数值单位的逆时针转角，如30 |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 同一转角的弧度数；弧度为无量纲角度单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/09ddc635f7b6cb67ae9fd772.svg) | 平角的度数，用于度与弧度换算 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 2×2旋转矩阵，各元素无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | 旋转前的坐标，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/2a3d1fd52a68a190a931ec53.svg) | 绕原点旋转后的坐标，mm；撇号标记新坐标 |
| ![Formula](https://ml-biomat.com/static/agent-math/5bc8e1a5d4bcca693b9f9dcf.svg) | 给出单位方向投影的正弦与余弦函数，函数值无量纲 |

矩阵第一列是水平单位方向旋转后的分量，第二列是竖直单位方向旋转后的分量。用原来的x、y加权相加，得到新坐标。30°对应π/6；(2,1) mm转成(2×0.866025−0.5,2×0.5+0.866025) mm≈(1.232051,1.866025) mm。

以30°为例，水平单位箭头转成约(0.866,0.500)，竖直单位箭头转成约(-0.500,0.866)。于是原点到(2,1)的箭头转到约(1.232,1.866) mm：新横坐标来自2乘0.866，再减去1乘0.500；新纵坐标来自2乘0.500，再加上1乘0.866。这两次乘加具有清楚的几何来源。三角函数所需的角度用弧度表达，`np.deg2rad(30)`把30°换成圆周率的六分之一；把30直接交给`np.sin`，程序会按30弧度计算，结果对应另一个旋转角。

公式通常把单个向量竖着写成列。我们的数据表却把每个点横着放在一行，所以批量计算写成`points @ R.T`。`R.T`交换矩阵的行与列，让每个数据行都得到公式里的两次乘加。形状检查是(4,2)乘(2,2)，中间两个2相同，输出仍是(4,2)。若单个点是一维数组`[2.,1.]`，则可直接写`R @ point`，返回长度为2的一维数组；NumPy的一维数组本身没有固定的行向量或列向量外形。

Python在3.5中加入了专门的`@`运算符，这个设计由2014年的PEP 465提出，解决的是科学程序里两种乘法长期共用一个符号的困扰。对NumPy数组，`*`表示对应位置逐个相乘，`@`表示沿相连的维度乘积求和。例如旋转矩阵中的一行包含两个权重，需要把两项贡献合起来，正适合使用`@`。程序最后还检查`R.T @ R`是否接近单位矩阵：逆向转回来应当恢复原坐标。浮点三角函数留下的极小舍入差异，用`np.allclose`比较更合适。

这里讨论的是坐标轴固定、图形主动转动。如果保持图形不动而把坐标轴逆时针转动，同一点的新坐标会对应相反方向的变换。拍照时还常遇到图像行号向下增加的约定，与数学纵轴向上相反；应先统一轴方向，再解释转角的正负。把原点画出来、在横纵轴标清正方向，并先检查一个90°例子，可以把这些不同约定分开，随后再处理任意角度。

## 把刻度尺读数变成带单位的直线

现在回到六条标定记录。标尺上每增加2 mm，像素读数大约增加40 px，因此一个自然的模型是“比例乘以长度，再加零点位置”。比例叫斜率，单位是px/mm；零点位置叫截距，单位是px。这两个量的作用不同：斜率决定尺子在图像里被放大多少，截距决定尺子的零刻度位于哪里。图像整体平移会改变截距，却不会改变每毫米包含多少像素。

$$
\widehat p_i=a s_i+b,\qquad r_i=p_i-\widehat p_i,\qquad s=\frac{p-b}{a},\qquad \Delta s=\frac{\Delta p}{a}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 标定记录编号，从1到6，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/98809785fc57c54ab2c96fe5.svg) | 已知标定位置或换算得到的位置，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e473ccb167494c193bb13372.svg) | 对应像素读数，px |
| ![Formula](https://ml-biomat.com/static/agent-math/68e840913b12a81fc785459a.svg) | 模型预测像素读数，px；帽号表示拟合值 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 像素尺度，即直线斜率，px/mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 标尺零点对应的像素位置，px |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 观测减去拟合的残差，px |
| ![Formula](https://ml-biomat.com/static/agent-math/d865353994b14d656a35dc2f.svg) | 两位置间的像素位移与物理位移，分别为px与mm；Δ表示差值 |

线性且尺度一致的标定中，a=20 px/mm、b=1 px时，4 mm处预测81 px；观测80 px，残差为−1 px。反算81 px得到(81−1)/20=4 mm。两个位置相减时共同截距抵消，200 px位移对应10 mm。

从第一条与最后一条记录可以算出斜率为20 px/mm、截距为1 px。这条线在本例中恰好也是使用所有记录的最小二乘解，但其他两点连线不一定给出同一结果。例如用0 mm和2 mm处的读数，会得到20.5 px/mm。选择哪两个点会影响答案，正说明我们需要一种利用全部记录的共同规则。六条记录对应的拟合读数为1、41、81、121、161、201 px，观测值减去拟合值后得到0、1、-1、-1、1、0 px。

这些差值叫残差。正残差表示该次读数位于拟合线的上方，负残差表示位于下方。残差与测量中不可直接知道的真实误差并不是同一个概念：残差以所选模型的拟合值为参照，可以从现有数据直接计算。把残差单独画出来尤其有用，因为纵坐标从原图的两百多像素缩小到几个像素，小差异便清楚可见。如果残差随长度持续弯曲，就值得检查线性关系、镜头畸变或读数方法；这种形状信息不会从一条看似很直的标定曲线自动显现。

获得20 px/mm的尺度后，200 px的位移对应10 mm，80 px对应4 mm。这里换算的是相对某个图像点的位移，所以两端读数相减时，1 px的共同截距已经抵消。若要把标尺上的某个绝对像素读数还原为标尺位置，则需要先减去截距，再除以斜率。例如81 px还原为4 mm。把位置与位移区分开，就能解释为什么完整的标定模型里有截距，而矩形边长的计算只用了斜率。

![带单位的标定直线、六个有正负号的残差及设计矩阵数据表。](https://ml-biomat.com/static/tutorials/python-scientific/figures/4c9884108de262cd3ea821c1.svg?v=4c9884108de2)

图 2六条构造的标定记录给出20 px/mm与1 px。完整读数与残差分别绘图，并与设计矩阵逐行对应；残差平方和为4 px²。

## 最小二乘从观测问题中长出来

十九世纪初的天文学和大地测量已经面对同一种困难：观测可以做很多次，却很难让所有读数同时精确符合少数几个未知参数。勒让德在1805年出版的彗星轨道研究中讨论了这种不完全吻合，并在附录中提出最小二乘方法，还将它用于法国子午线测量。方法的关键是为所有残差建立一个共同目标，让它们的平方和尽可能小。今天的显微标定与当时研究的具体对象相差很大，但“多条观测共同确定少数参数”的结构延续了下来。

$$
S(a,b)=\sum_{i=1}^{N}\left[p_i-(a s_i+b)\right]^2=\sum_{i=1}^{N}r_i^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 当前参数对应的残差平方和，px² |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | 待拟合斜率与截距，分别为px/mm和px |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 标定记录数，本例为6，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 从1到N的记录编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/494b59eedd3f44cca8cf919a.svg) | 第i条观测像素读数，px |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | 第i条已知标尺位置，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 第i条观测减拟合残差，px |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 依次把N项相加 |

采用同等权重，使S最小的参数为本例最小二乘解。六个残差0、1、−1、−1、1、0 px给出S=0+1+1+1+1+0=4 px²。平方保留偏离大小并避免正负抵消；标尺位置按足够准确的输入处理。

直接把正负残差相加会互相抵消：本例六个残差加起来是0 px，却仍有四个读数偏离拟合线。平方之后，每项贡献都非负，1 px和-1 px都贡献1 px²，最后得到4 px²。平方还会让较大的偏离受到更强的强调，例如3 px的偏离贡献9 px²。绝对值之和也能作为另一种目标，但对应不同的优化问题。最小二乘的名称明确告诉我们，这里选定的衡量标准是平方和。

下面的等高线图把斜率与截距作为两个坐标轴，每一组参数都能产生一条标定线，并据此算出一个残差平方和。同一条等高线上的参数组合具有相同的总平方偏离，向中心移动时这个数逐渐减小。长而倾斜的椭圆说明两种参数可以部分补偿：斜率略微提高时，降低截距能让中间区域的预测变化较小。选择较宽的标定范围，可以让比例与零点的作用更容易区分。

如果强制截距为0，参数只能沿图中截距为0的水平线变化。程序得到的斜率约20.136364 px/mm，残差平方和约5.909091 px²，超过自由拟合的4 px²。这里的差别来自我们对零点的约束，而不是程序忽然更不精确了。只有实验定义确实保证两套零点重合时，固定零截距才表达了合适的关系。本例对六条读数采用同等权重，并把已知标尺位置当作足够准确的输入；若读数精度明显不同，可以按各自的不确定度建立加权拟合，若横坐标本身也有显著误差，则需要同时处理两方向的误差结构。

![斜率与截距平面上的残差平方和等高线及两种模型的残差比较。](https://ml-biomat.com/static/tutorials/python-scientific/figures/91409af48bdc170394803433.svg?v=91409af48bdc)

图 3以本章数据演示勒让德1805年提出的平方和目标。等高线来自实际计算的残差平方和；固定零截距限制了参数选择，使平方和从4增至约5.909 px²。

## 把六条关系排成矩阵，让NumPy求解

一条直线只有斜率与截距两个未知量，我们却有六条记录。把每个长度与一个常数1排成一行，就得到形状为(6,2)的设计矩阵。第一列乘斜率，第二列乘截距，逐行相加后恰好得到六个预测像素读数。这里的1表示每条记录都包含同一个零点项；它不表示多测了一种物理量。设计矩阵的两列还具有不同单位，长度列为mm，常数列无量纲，各自乘上对应系数后统一得到px。

`np.column_stack([LENGTH, np.ones_like(LENGTH)])`负责构造这张表，`np.linalg.lstsq(design, PIXEL, rcond=None)`负责求解。返回值依次是系数、残差平方和数组、秩和奇异值。系数的顺序由我们放置列的顺序决定，本例先长度后常数，因此先得到斜率再得到截距。随后`design @ coefficients`生成拟合值，`PIXEL - predicted`生成每条残差。代码把这些物理量分开命名，读程序时便能从每个变量追溯到图中的位置。

秩可以先理解为设计矩阵提供了多少种独立的信息。本例的长度有多个不同值，长度列无法由常数列乘一个固定数字得到，因此秩为2，两个系数可以分别确定。假如所有标定记录都在同一个长度位置，重复读数可以帮助了解该点的波动，却无法单独辨认斜率和截距。`lstsq`即使在信息不足时也可能返回一组系数，返回的秩便提醒我们重新检查标定点的安排。奇异值进一步描述数值方向的尺度，本章保留输出供检查，不把它们当成两个具有相同物理单位的测量结果。

返回的残差数组还具有特定接口规则：当矩阵秩不足，或者记录数不大于未知数个数时，它会为空。空数组表示这个接口没有在该字段报告平方和，并不直接表示残差全为零。因此完整程序始终用已经算出的残差做一次`residual @ residual`。程序另写了一个基于中心化求和的标量计算，独立核对斜率与截距；读者可以先跟随前面的两点手算与六个残差，再逐步阅读这个核对函数，主计算仍由NumPy完成。

核对函数中的中心化，也可以从标定图理解。六个长度的平均值是5 mm，像素读数的平均值是101 px；先从每条记录减去这两个平均值，相当于把坐标原点移到数据中心。中心化的长度与像素偏移相乘再求和，得到1400 mm·px；长度偏移的平方和为70 mm²，二者相除便是20 px/mm。再用平均读数减去斜率乘平均长度，得到1 px的截距。这既解释了函数里的加减乘除，也表明标定点都挤在同一位置时，分母为什么会消失。

## 完整计算：标定、旋转和逐点检查

下面的程序将本章全部构造数据写在文件开头，可以直接运行。它先求标定系数，再把四个像素位移除以尺度得到毫米坐标，随后进行30°旋转。程序保存三组双面板或多面板科学图，以及包含标定值、残差、旋转矩阵、顶点坐标和距离的`summary.json`。绘图使用Matplotlib，数组计算使用NumPy，两者都在[P06](https://ml-biomat.com/tutorials/python-scientific/p06/)介绍的同一个Python环境中安装。

### 运行完整例子

中文图把en改成zh；使用已安装NumPy与Matplotlib的环境。

```
python main.py --output output --language en
```

### 标定与坐标变换的完整程序

LENGTH与PIXEL为六条构造记录；OUTLINE为相对图像原点的像素位移。scalar_fit独立核对系数，rotation生成旋转规则，main保存数值与科学图。

```
"""Calibrate a constructed microscope scale and rotate planar coordinates."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon

LENGTH = np.array([0, 2, 4, 6, 8, 10], dtype=float)  # mm
PIXEL = np.array([1, 42, 80, 120, 162, 201], dtype=float)  # px
OUTLINE = np.array([[0, 0], [200, 0], [200, 80], [0, 80]], dtype=float)
BLUE, RED, GREEN = '#246989', '#b95235', '#42816b'


def rotation(degrees):
    theta = np.deg2rad(degrees)
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


def scalar_fit(x, y):
    """Independent centered-sum line fit, used as an arithmetic check."""
    xbar = math.fsum(map(float, x)) / len(x)
    ybar = math.fsum(map(float, y)) / len(y)
    numerator = math.fsum((float(u)-xbar)*(float(v)-ybar) for u, v in zip(x, y))
    denominator = math.fsum((float(u)-xbar)**2 for u in x)
    slope = numerator / denominator
    return slope, ybar - slope*xbar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('output'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    design = np.column_stack([LENGTH, np.ones_like(LENGTH)])
    coefficients, returned_sse, rank, singular = np.linalg.lstsq(design, PIXEL, rcond=None)
    slope, intercept = coefficients
    predicted = design @ coefficients
    residual = PIXEL - predicted
    sse = float(residual @ residual)
    R = rotation(30)
    physical = OUTLINE / slope  # displacement from a chosen image origin, in mm
    rotated = physical @ R.T
    radii = np.linalg.norm(physical, axis=1)
    rotated_radii = np.linalg.norm(rotated, axis=1)
    point90 = rotation(90) @ np.array([2., 1.])
    constrained_slope = float(LENGTH @ PIXEL / (LENGTH @ LENGTH))
    constrained_residual = PIXEL - constrained_slope * LENGTH
    assert np.allclose(coefficients, [20, 1])
    assert np.allclose(coefficients, scalar_fit(LENGTH, PIXEL))
    assert np.allclose(residual, [0, 1, -1, -1, 1, 0]) and np.isclose(sse, 4)
    assert np.allclose(point90, [-1, 2])
    assert np.allclose(R.T @ R, np.eye(2))
    assert np.allclose(radii, rotated_radii)
    assert np.allclose(rotated, [[u*math.cos(math.pi/6)-v*math.sin(math.pi/6),
                                 u*math.sin(math.pi/6)+v*math.cos(math.pi/6)] for u, v in physical])
    zh = args.language == 'zh'
    tr = lambda z, e: z if zh else e
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    family = [f for f in ['Noto Sans CJK SC', 'Noto Sans SC', 'Microsoft YaHei', 'DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family': family if zh else ['DejaVu Sans', 'Arial'],
                         'font.size': 12, 'axes.titlesize': 14, 'axes.titleweight': 'bold',
                         'axes.spines.top': False, 'axes.spines.right': False, 'svg.fonttype': 'none',
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6', 'text.color': '#172b36'})
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=170, bbox_inches='tight')
        plt.close(fig)

    fig = plt.figure(figsize=(12.4, 7.7), layout='constrained')
    gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 1])
    ax = fig.add_subplot(gs[:, 0])
    for points, color, label in [(physical, BLUE, tr('标定后','Calibrated')), (rotated, RED, tr('逆时针30°','30° counterclockwise'))]:
        ax.add_patch(Polygon(points, facecolor=color, edgecolor=color, alpha=.15, lw=2))
        closed = np.vstack([points, points[0]])
        ax.plot(closed[:, 0], closed[:, 1], 'o-', color=color, lw=2, label=label)
    for i, (x, y) in enumerate(rotated):
        ax.annotate(str(i), (x, y), xytext=(6, 7), textcoords='offset points', color=RED, weight='bold')
    ax.axhline(0, color='#83949a', lw=.8); ax.axvline(0, color='#83949a', lw=.8)
    ax.set(xlim=(-4, 12), ylim=(-3, 11), aspect='equal', xlabel='x / mm', ylabel='y / mm', title=tr('a  长度不变，坐标改变','a  Coordinates change; lengths do not'))
    ax.legend(loc='upper left', fontsize=11); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[0, 1])
    basis = rotation(30)
    for v, color, label in [(np.array([1, 0]), BLUE, '(1, 0)'), (np.array([0, 1]), BLUE, '(0, 1)'), (basis[:, 0], RED, '(0.866, 0.500)'), (basis[:, 1], GREEN, '(-0.500, 0.866)')]:
        ax.annotate('', xy=v, xytext=(0, 0), arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': 2})
        ax.text(v[0]*1.08, v[1]*1.08, label, color=color, fontsize=10, ha='center')
    ax.set(xlim=(-.8, 1.45), ylim=(-.2, 1.35), aspect='equal', title=tr('b  矩阵的两列：单位方向转到哪里','b  Matrix columns: rotated unit directions'))
    ax.set_xlabel(tr('无量纲方向分量','Dimensionless direction components')); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[1, 1])
    pos = np.arange(4)
    ax.bar(pos-.17, radii, .34, color=BLUE, label=tr('旋转前','Before'))
    ax.bar(pos+.17, rotated_radii, .34, color=RED, alpha=.75, label=tr('旋转后','After'))
    ax.set(xticks=pos, xlabel=tr('顶点编号','Vertex index'), ylabel=tr('到原点距离 / mm','Distance to origin / mm'), title=tr('c  按行计算向量长度','c  Vector norms computed row by row'))
    ax.legend(); ax.grid(axis='y', alpha=.15)
    save(fig, 'coordinate-rotation')

    fig = plt.figure(figsize=(12.4, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1], width_ratios=[1.5, 1])
    ax = fig.add_subplot(gs[0, 0])
    xx = np.linspace(0, 10, 101)
    ax.plot(xx, slope*xx+intercept, color=BLUE, lw=2, label='p = 20s + 1')
    ax.scatter(LENGTH, PIXEL, color=RED, s=65, zorder=3, label=tr('构造的标定记录','Constructed calibration records'))
    ax.set(xlabel=tr('已知长度 s / mm','Known length s / mm'), ylabel='p / px', title=tr('a  像素读数：六条记录确定比例与零点','a  Six records determine scale and offset'))
    ax.legend(); ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[1, 0])
    ax.axhline(0, color='#83949a', lw=1)
    ax.vlines(LENGTH, 0, residual, color=BLUE, lw=3); ax.scatter(LENGTH, residual, color=BLUE, s=55)
    ax.set(xlabel=tr('已知长度 / mm','Known length / mm'), ylabel=tr('观测 − 拟合 / px','Observed − fitted / px'), ylim=(-1.7, 1.7), yticks=[-1,0,1], title=tr('b  残差放大后，1 px清楚可见','b  Residual view reveals 1 px differences'))
    ax.grid(alpha=.15)
    ax = fig.add_subplot(gs[:, 1]); ax.axis('off')
    table = ax.table(cellText=[[f'{s:.0f}', '1', f'{p:.0f}', str(round(float(r)))] for s,p,r in zip(LENGTH,PIXEL,residual)],
                     colLabels=['s / mm', '1', 'p / px', 'r / px'], loc='center', cellLoc='center', bbox=[.02,.22,.96,.60])
    table.auto_set_font_size(False); table.set_fontsize(13)
    for (i,j), cell in table.get_celld().items():
        cell.set_edgecolor('#d3dcdb'); cell.set_facecolor('#e6efee' if i==0 else '#fbfaf6')
    ax.text(.02,.94,tr('c  设计矩阵的每一行都对应一条记录','c  One design-matrix row per record'),fontsize=14,weight='bold')
    ax.text(.02,.10,tr('a = 20 px/mm；b = 1 px\n残差平方和 = 4 px²；rank = 2','a = 20 px/mm; b = 1 px\nSquared residual sum = 4 px²; rank = 2'),fontsize=14,linespacing=1.7)
    save(fig, 'calibration-residuals')

    fig = plt.figure(figsize=(12.4, 7.5), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[.2, 1], width_ratios=[1.2, 1])
    ax = fig.add_subplot(gs[0, :]); ax.axis('off')
    ax.text(0,.75,tr('1805：把互不完全吻合的观测，变成一个共同的求解问题','1805: reconciling observations through one shared objective'),fontsize=18,weight='bold')
    ax.text(0,.05,tr('勒让德的最小二乘思想，用本章构造的显微标定记录展示。','Legendre’s least-squares principle, illustrated with this chapter’s constructed calibration records.'),fontsize=12)
    ax = fig.add_subplot(gs[1, 0])
    aa, bb = np.meshgrid(np.linspace(19,21,301), np.linspace(-4,6,301))
    costs = np.sum((PIXEL[:,None,None] - aa[None]*LENGTH[:,None,None]-bb[None])**2, axis=0)
    contours = ax.contour(aa, bb, costs, levels=[5,10,20,40,80,160,320], cmap='viridis', linewidths=1.5)
    ax.clabel(contours, inline=True, fontsize=10, fmt='%g')
    ax.axhline(0, color=RED, linestyle=':', linewidth=1.2, alpha=.6)
    ax.scatter([slope,constrained_slope],[intercept,0],color=[BLUE,RED],s=[80,65],zorder=4)
    ax.annotate(tr('自由零点：(20, 1)','Free offset: (20, 1)'),(20,1),xytext=(19.05,4.5),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE)
    ax.annotate(tr('强制 b = 0','Force b = 0'),(constrained_slope,0),xytext=(20.25,-3),arrowprops={'arrowstyle':'->','color':RED},color=RED)
    ax.set(xlabel=tr('斜率 a / (px/mm)','Slope a / (px/mm)'), ylabel=tr('截距 b / px','Intercept b / px'), title=tr('a  等高线数字：残差平方和 / px²','a  Contour labels: squared residual sum / px²'))
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(LENGTH,residual,'o-',color=BLUE,label=tr('自由零点','Free offset'))
    ax.plot(LENGTH,constrained_residual,'s--',color=RED,label=tr('强制零点','Forced zero'))
    ax.axhline(0,color='#83949a',lw=1)
    ax.set(xlabel=tr('已知长度 / mm','Known length / mm'),ylabel=tr('残差 / px','Residual / px'),ylim=(-1.8,1.8),title=tr('b  改变模型，残差也随之改变','b  Changing the model changes the residuals'))
    ax.legend();ax.grid(alpha=.15)
    save(fig,'least-squares-history')
    summary = {'dataset':'Constructed microscope calibration', 'length_mm':LENGTH.tolist(),'pixel_px':PIXEL.tolist(),
               'slope_px_per_mm':float(slope),'intercept_px':float(intercept),'residual_px':residual.tolist(),'sse_px2':sse,
               'rank':int(rank),'singular_values':singular.tolist(),'returned_sse_px2':returned_sse.tolist(),
               'rotation_30':R.tolist(),'physical_vertices_mm':physical.tolist(),'rotated_vertices_mm':rotated.tolist(),
               'radii_before_mm':radii.tolist(),'radii_after_mm':rotated_radii.tolist(),'point_90_mm':point90.tolist(),
               'constrained_slope_px_per_mm':constrained_slope,'constrained_sse_px2':float(constrained_residual@constrained_residual)}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
```

运行结果中，斜率约为20.000000 px/mm，截距约为1.000000 px，四个旋转后顶点约为(0,0)、(8.660254,5.000000)、(6.660254,8.464102)、(-2.000000,3.464102) mm。第二个顶点由原来的(10,0) mm转来，其两个新分量分别是10乘30°的余弦和正弦。第三个顶点还包含原来4 mm竖直边的贡献，因此横坐标减少2 mm、纵坐标增加约3.464102 mm。逐点对照比单看一幅旋转图更容易发现转置或角度方向的问题。

程序同时比较旋转前后的四个向量长度，检查旋转矩阵反向相乘是否得到单位矩阵，并以标量三角计算重新生成全部顶点。这些检查分别对应距离、逆变换和逐点坐标三个不同方面。图中几何面板使用横纵等比例的坐标；如果一个方向被拉伸显示，即使数字正确，矩形与旋转角也会在视觉上变形。残差面板则刻意放大纵向读数差异，因为它呈现的是两个不同单位变量之间的关系，并不承担平面几何形状的展示任务。

可以先把旋转角改成90°，核对整块矩形落在原点的左上方，再把已知尺度记录全部改成原来的两倍，观察斜率如何随输入单位改变。后一种修改必须同时改清标尺单位或物理定义：如果只是把mm改写为cm，同一距离的数值应缩小到十分之一，而斜率以px/cm表示时增大十倍。单位和数值相互配合，才能让得到的实际长度保持一致。

读数输出中的小数位数还值得留意。求解器可能打印19.99999999999999，而不是整齐的20；两者的差异来自有限精度运算。图注按便于阅读的精度显示，数值文件保留计算结果，便于下一步继续运算。读图时关注可由标定数据支持的变化，不把长长的小数尾部当成额外的测量精度；本例原始读数以整数像素给出，显示更多小数主要用于逐步核对计算。

## 亲手调整一条标定记录，观察影响怎样传到几何图

交互实验使用同样的六条记录。选择一条记录并增加或减少它的像素读数，直线、六个残差、平方和与矩形的毫米尺寸会同时更新。右侧矩形仍然占据200×80 px，因此它在物理坐标里有多大，完全由当前拟合斜率决定。旋转角只改变朝向；图中同时显示旋转前后的轮廓，方便区分尺度变化与旋转变化。截距可以自由拟合，也可以勾选固定为0来比较两个模型。

### 标定误差怎样改变图像尺

调整一条标尺记录或转动矩形。图形坐标统一为毫米，像素轮廓固定为200×80 px。

[Figure: 标定曲线、残差和联动旋转矩形](https://ml-biomat.com/tutorials/python-scientific/p10/#P10-chart)

蓝色：自由或当前约束下的拟合；橙色：被修改记录与旋转后轮廓；灰色：未旋转轮廓。残差为观测减拟合。

先保持30°，把10 mm处的读数提高10 px。这个远离平均长度的位置会明显影响斜率，换算出的矩形宽度随之减小。接着把读数恢复，改动0 mm处的记录，比较截距与斜率怎样共同调整。每次只改一个读数，能把变化追溯到具体记录。再把旋转角设为0°与90°，观察同一套标定下的长度与残差保持不变，顶点坐标则随角度改变。

图像测量中的计算选择最终都要回到所测对象：以哪个点为原点，横纵轴朝哪里，标尺记录覆盖多大范围，零点是否经过独立校准，像素能否按统一尺度换算。NumPy让这些步骤对一整组坐标一起执行，矩阵也让规则表达得紧凑。理解每一列和每一次乘加之后，数组计算就能继续扩展到更多轮廓点、更多图像和重复的标定实验；下一章将转向包含名称、分类与缺失值的真实记录，学习怎样在表格中保留这些观测含义。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P10.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NumPy: numpy.linalg.lstsq](https://numpy.org/doc/2.4/reference/generated/numpy.linalg.lstsq.html)

   设计矩阵、秩与返回值规则

   BSD-3-Clause documentation; original example here
2. [NumPy: numpy.matmul](https://numpy.org/doc/2.4/reference/generated/numpy.matmul.html)

   矩阵乘法与形状匹配

   BSD-3-Clause documentation
3. [NumPy: numpy.linalg.norm](https://numpy.org/doc/2.4/reference/generated/numpy.linalg.norm.html)

   沿指定轴计算向量长度

   BSD-3-Clause documentation
4. [PEP 465: matrix multiplication operator](https://peps.python.org/pep-0465/)

   @运算符的设计背景

   Public domain PEP; factual reference
5. [Legendre, Nouvelles méthodes, 1805](https://doi.org/10.3931/e-rara-35115)

   最小二乘的原始观测问题与历史背景

   Public Domain Mark, ETH Library; no scans reproduced
