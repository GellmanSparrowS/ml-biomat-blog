# 接触角：一滴液体如何认识表面

Source: https://ml-biomat.com/tutorials/experimental-methods/p03/
Language: zh-CN

从水珠的轮廓理解润湿，分清界面平衡、接触线历史与图像误差。

## 同一滴水，为什么有时铺开，有时像珠子

雨水落在玻璃、蜡纸和叶片上，会留下很不一样的形状。有的水滴很快铺开，有的保持鼓起的轮廓，有的看上去很圆，却牢牢黏在原处。这些差别影响油墨能否连续铺展、涂层是否均匀、微流道能否顺利进液，也影响生物材料表面最初怎样接触水和含蛋白质的溶液。接触角实验把这种日常观察变成一个可以定义的几何量：在液体、固体和周围气体相遇的位置，液滴表面的切线与固体表面之间，沿液体内部测得的夹角。

这里最容易混淆的是角度究竟属于谁。它不是固体单独拥有的一枚标签，而是特定液体、固体表面、周围环境和测量过程共同形成的结果。把水换成另一种液体，清洗方式改变，表面在空气中放置一段时间，或把液滴从缓慢加液改成快速撞击，都可能改变观察到的形状。因此，“这个表面的接触角是多少”最好转化成更具体的问题：用什么液体，在怎样的表面状态下，液滴形成后多久，以哪一种运动或静置过程测量。

本节从一个已知形状的小液滴出发，解释角度与界面作用的关系，随后学习怎样从轮廓读取它。我们会看到，轮廓拟合可以非常稳定，但基线放错一点就能产生更大的系统偏差；也会看到，加液和抽液时的角度为何不同。最后再把表面粗糙、气体夹层和生物材料的吸水联系起来。这样，一张水滴照片就不只给出一个数字，而能帮助决定下一步该检查表面化学、结构还是液体与材料之间随时间发生的变化。

日常所说的亲水与疏水，通常用水接触角小于或大于90°来作初步描述。这里的“水”不能省略，因为同一表面可能不容易被水铺展，却容易被某种油润湿。接近90°的两个结果，也应结合实际测量波动阅读，而不是把89°与91°当成完全相反的材料类别。角度提供连续的几何信息，功能往往也连续变化；明确分界的名称有助于交流，却不应替代对原始轮廓和实验条件的理解。

## Young为什么把问题放在三种界面的交会处

1805年，Thomas Young发表了关于流体内聚作用的论文。图中保留了原文第66页的一段：他注意到，特定固体与液体的组合会形成相应的接触角，并把这种现象与液体表面的作用联系起来。那时没有今天的高速相机和自动拟合软件，研究者依靠液滴、毛细管和曲面形状建立理论。这个历史入口很有帮助，因为接触角的核心并不是相机有多精密，而是液体表面、固体表面与固液界面在接触线附近怎样共同决定几何形状。

表面张力可以从两种互相联系的角度理解。它表现为沿界面单位长度传递的拉力，也对应增加单位界面面积所需的自由能。想象把一个已经存在的界面拉大，需要付出能量；不同界面的代价不同，液体铺展时就会同时减少一种面积、增加另一些面积。对于平整、化学均一、刚性且处于理想平衡的固体表面，沿水平方向比较这些变化，得到Young关系。图中的箭头是单位接触线长度上的界面贡献示意，角度从液体一侧读取；不要把水滴外面的补角当成同一个量。

$$
\gamma_{SV}-\gamma_{SL}=\gamma_{LV}\cos\theta_Y
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ded793ad5550dae1b42621e0.svg) | 固体–气体界面自由能，mJ/m²，数值等于mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7b827ae0be883fb68e689fae.svg) | 固体–液体界面自由能，mJ/m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f3d1c4c2559796bb2ba336f.svg) | 液体–气体表面张力，mN/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d941e2f726e4aeecee316d62.svg) | 理想平整、化学均一刚性表面上的平衡角，从液体内部读取。 |

在适用的平衡条件下，沿表面比较界面贡献。差值36 mN/m除以72 mN/m为0.5，因此θY=60°。一组角度给出的是两种固体界面量的差。

如果固气界面与固液界面之间的自由能差为36 mN/m，而液气表面张力为72 mN/m，那么余弦值为0.5，理想角度是60°。这里的36不是固体表面自由能本身，而是两个界面量的差。只测一种液体的一个角度，提供的是这样一条关系，不能同时独立确定其中所有未知量。使用多种已知性质的探针液体，可以在选定的表面能模型下进一步分析，但模型如何分配极性和色散贡献，也应成为结果定义的一部分。

可以用两组简单数值看清这个区别：固气与固液界面量分别为50和14，或者分别为80和44，二者的差都是36，因此搭配同一种液体会给出相同理想角度。一个角度并没有区分这两种组合。界面自由能常写成mJ/m²，与mN/m在数值上等价，因为能量等于力乘距离。把单位关系和未知量数量一起检查，能帮助判断某项表面能计算还需要多少额外测量或模型假定。

![左：Thomas Young，1805，An Essay on the Cohesion of Fluids，第66页局部，公有领域扫描，Wikimedia Commons存档。该段把特定固体–液体组合与接触角联系起来。右：原创Young界面贡献示意，从液体内部读取θ，图不按力的比例绘制。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/952b60635c811a6e8d40fd17.svg?v=952b60635c81)

图 1左：Thomas Young，1805，An Essay on the Cohesion of Fluids，第66页局部，公有领域扫描，Wikimedia Commons存档。该段把特定固体–液体组合与接触角联系起来。右：原创Young界面贡献示意，从液体内部读取θ，图不按力的比例绘制。

这个平衡图还解释了为什么“水滴越扁就一定越黏”过于简单。较小角度意味着在指定条件下液体更倾向于接触更多固体面积，但液滴移动时还要跨过接触线遇到的局部障碍。粗糙突起、化学斑块和吸附层都会让接触线暂时停住。宏观轮廓因此可能停留在一系列可观察状态，而不是每次都立即到达同一个理想平衡角。后面的前进角、后退角与滞后，正是把这种过程信息纳入测量的方法。

## 先看清接触的位置，再让软件去找轮廓

常见的座滴法把一小滴液体放在样品上，从侧面拍摄。背光使液滴轮廓与背景形成清晰反差，样品台调整到合适位置，相机应尽量平视接触区域。实验开始前，先确认镜头中的固体表面没有明显倾斜，左右接触点都可辨认，针头不会遮住主要轮廓。样品若弯曲、透明或有明显反光，真正的接触位置可能与视觉上最深的一条线不同。图像中的基线是用来表示固体表面的参考线，它应来自可解释的几何位置，而不是为了让结果更好看而自由移动。

液滴体积需要与样品和问题匹配。很小的液滴受重力形变较弱，却更容易受到蒸发、表面局部不均和像素分辨率的影响；较大的液滴覆盖更多区域，但重力可能让轮廓偏离简单球冠。球冠可以想象成从一个球上切下来的一顶帽子，在重力影响较小且液滴近似轴对称时，是很方便的几何模型。对于较明显的重力变形，可以采用包含重力和界面曲率的Young–Laplace形状拟合。模型选择取决于轮廓中的物理作用，而不是只看哪种拟合给出的残差最小。

重力与表面张力的相对作用可以用Bond数估计。它把重力造成的压力变化与曲率引起的界面压力尺度相比，数值越小，球冠近似越有几何依据。本例采用曲率半径作为特征长度，水与气体的密度差近似取1000 kg/m³，表面张力取72 mN/m，得到约0.0825。它说明在这个构造尺度下重力是较小的贡献，并不表示所有0.5 μL液滴都具有相同误差；液体性质、角度和选取的长度尺度仍需一起说明。

$$
\mathrm{Bo}=\frac{\Delta\rho\,gR^2}{\gamma_{LV}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/76f8718fd930ba8aa9f1254c.svg) | Bond数，重力与表面张力作用的无量纲尺度比。 |
| ![Formula](https://ml-biomat.com/static/agent-math/988fbc7bbcda53116494bdef.svg) | 液体与周围气体的密度差，kg/m³，本例近似1000。 |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | 重力加速度，m/s²，本例9.81。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 本例选取的曲率半径，m；从mm换算。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f3d1c4c2559796bb2ba336f.svg) | 液气表面张力，N/m；72 mN/m等于0.072 N/m。 |

R=0.000777992 m时Bo≈0.08247。重力压力尺度ΔρgR除以曲率压力尺度γ/R得到该比值；使用其他特征长度时需写明定义。

表面清洁也不是一个没有细节的前处理词。溶剂残留、手指接触、表面处理后的存放时间和空气中的吸附物，都可能改变最外层化学环境。若研究等离子体处理后的聚合物，处理后立即测量与放置数天后测量回答的是不同时间点的问题。若研究细胞培养用材料，水滴在干燥表面上的行为与材料浸在培养液中的界面状态也不同。明确测量对象的准备和等待时间，可以把这些变化变成实验设计的一部分，而不是事后把所有差别归为误差。

一次测量还应同时保存时间与空间信息。液滴接触表面后，记录一段轮廓序列，可以分辨迅速铺展、缓慢吸水和蒸发等过程。不同位置的重复滴液描述表面不均匀，不同独立样品的重复描述制备差异；同一滴液体的许多视频帧则描述一个过程，不能自动当成许多独立样品。左右接触角也值得分别观察：明显不对称可能提示台面倾斜、方向性纹理、污染或接触线钉扎。平均值有用，但先理解左右差别，往往比立即把它们平均更能发现问题。

图像标定还有一个几何细节。若水平与竖直方向的像素对应不同物理长度，显示出来的圆会被拉成椭圆，直接用像素坐标算角度就会产生偏差。应分别确认两个方向的比例，并在拟合前转换到同一长度单位。例如一个像素代表5 μm时，20 μm的基线偏移只有四个像素，在整幅照片里可能不显眼，却足以改变角度约一度以上。这个例子说明，接触区域的清晰定位比给最终结果增加小数位更有价值。

## 从一顶球冠，读出角度、体积与基线偏差

先用几何关系建立一个可核对的例子。球冠的底面半径记为a，从固体表面到最高点的高度记为h。对理想球冠，接触角等于两倍的反正切h/a。这个关系来自圆的几何：高度与底面半径决定了半角对应的直角三角形，因此只要二者使用同一种长度单位，比例就与放大倍数无关。这里的a指液滴与表面相交处的半径，不是所有高度里最大的横向半径；角度大于90°的鼓起液滴尤其需要分清这两者。

$$
\theta=2\arctan(h/a),\qquad V=\frac{\pi h}{6}(3a^2+h^2)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 理想球冠接触角；反三角函数结果为弧度，显示时转为度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 从基线到液滴顶点的高度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 接触底面的半径，mm；不是鼓起液滴的最大横向半径。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 球冠体积，mm³；数值等于μL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |

圆的半角几何给出h/a，球冠积分给出体积。a=0.731073 mm、h=0.511903 mm恢复θ=70°和V=0.5 μL；采用近似轴对称且重力影响较小的球冠模型。

本节构造一个体积0.5 μL、接触角70°的球冠。由于1 μL等于1 mm³，计算可以统一使用毫米。它的曲率半径约为0.7780 mm，接触底面半径约为0.7311 mm，高度约为0.5119 mm；把高度与底面半径代回公式，可以恢复70°和0.5 μL。这些数值不是某种材料的实测性质，而是给轮廓算法提供一个已知答案。随后向轮廓坐标加入标准差为2 μm的独立随机扰动，用整个轮廓拟合圆，看看测量怎样偏离已知几何。

拟合得到的圆心和半径决定圆与基线的交点，也决定交点处切线的方向。默认结果约为70.029°，与设定角度很接近；若保持同一个拟合圆不变，只把基线向上移动20 μm，估计角度就降到约68.454°。这个操作没有改变液体，也没有重新拍摄，只改变了我们认定固体表面的位置。误差之所以明显，是因为接触角在轮廓与表面交会的位置定义，基线一移动，交点和切线都跟着变化。单纯增加轮廓点数不能自动修复这个几何错误。

$$
\theta_{\mathrm{fit}}=\arccos\left(\frac{b-y_c}{R}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e9dd721598f9326794077013.svg) | 由拟合圆与指定水平基线得到的角度；显示为度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 分析基线的竖直坐标，mm；真实表面设为0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/024420a1f4a1300a242618c4.svg) | 拟合圆心的竖直坐标，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 拟合圆的半径，mm。 |

圆的半径与切线垂直，因此交点的几何给出余弦。默认拟合基线b=0时约70.029°，同一圆改用b=0.020 mm时约68.454°。该式要求基线与圆存在相交。

四面板图分别展示轮廓与基线、拟合径向残差、基线偏移带来的角度变化，以及300次相同真值下的独立噪声模拟。最后一个面板中的角度标准差约为0.039°，远小于20 μm基线偏移造成的变化。它说明重复拟合可以很精密，却仍可能存在共同的系统偏差。真实测量还包括镜头像差、接触点识别、样品不均匀和模型形状误差，因此不能把这个理想模拟中的小标准差直接当作仪器总体准确度。把不同误差来源分别对应到可检查的图像环节，才能决定该改进什么。

![构造0.5 μL、70°球冠与2 μm坐标噪声。A比较真实和上移20 μm基线；B为径向残差；C改变同一拟合圆的分析基线；D为300次独立噪声模拟。精密重复与共同基线偏差在图中分开。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1e5b3a6982e51b1251685e97.svg?v=1e5b3a6982e5)

图 2构造0.5 μL、70°球冠与2 μm坐标噪声。A比较真实和上移20 μm基线；B为径向残差；C改变同一拟合圆的分析基线；D为300次独立噪声模拟。精密重复与共同基线偏差在图中分开。

## 加液与抽液，让接触线的记忆显现出来

在许多表面上，缓慢向液滴加液时，接触线不会立刻向外移动。它可能暂时钉在原处，底面半径近似不变，而液滴高度和接触角逐渐增加；达到某个范围后，接触线开始前进，新增液体主要扩大接触面积。反过来抽液时，接触线也可能先保持不动，让角度下降，然后才向内后退。前进过程中的代表角度称为前进角，后退过程中的代表角度称为后退角，二者之差称为接触角滞后。它记录了液滴经历过什么，因此比一张静止照片包含更多过程信息。

图中的教学模型把前进阈值设为100°、后退阈值设为70°。起点是一滴0.5 μL、角度85°的液滴，加液到2 μL，再抽液到0.15 μL。在接触线被钉住的阶段，程序保持底面半径不变，根据球冠体积关系重新求角度；达到规定阈值后，程序保持角度，让底面半径改变。这样生成的两条路径不是同一条曲线倒着走，而是形成一段回线。它没有尝试预测某种真实表面的钉扎能量，而是用明确规则展示“同一体积下，形状仍可能取决于此前过程”。

前进角与后退角的测量需要留意加液速率、针头位置和接触线是否真的移动。体积增加但接触线仍固定时，记录的是钉扎阶段中的某个角度；把它直接称为稳定前进角，会混淆过程位置。速度较高时，黏性流动和动态效应也参与形状。比较不同材料时，应采用可对应的过程定义，并保存体积或时间序列，让接触线运动与角度变化能够一起检查。倾斜台上的前后缘角度和液滴滑落行为提供另一类信息，其条件也需要与座滴加液实验区分。

日常的叶片和花瓣提供很好的直觉。有些表面上的水滴既鼓起又容易滚落，另一些表面上的水滴同样鼓起，却不容易移动。较大静态接触角描述的是某一时刻的外形，移动还涉及接触线被不同位置阻碍的程度。因此，设计自清洁或低黏附表面时，常同时关心前进、后退和滑落过程；设计需要稳定液滴定位的微阵列时，较强钉扎反而可能有用。实验指标的价值来自它与实际功能的对应，而不是角度越大或越小就普遍越好。

## 粗糙表面上，水到底接触了多少固体

表面纹理会改变液体真正接触的面积，也可能让气体留在凹陷中。Wenzel状态描述液体充分进入粗糙纹理的情形：相同投影面积下，实际固液接触面积更大。用实际面积与投影面积之比表示粗糙度因子，便能写出一种理想化关系。对于原本较易被该液体润湿的表面，增加真实接触面积会使表观角度进一步减小；对于另一侧的理想情形，趋势相反。这个模型依赖液体确实跟随纹理接触，不能只凭表面有粗糙度就自动套用。

Cassie–Baxter类型的复合接触则考虑液滴底下有不同组分。最常见的教学图是固体顶端与困在纹理中的气体共同接触液体：液滴只在一部分投影面积上碰到固体，其余位置跨过气体。图中两种局部状态使用同样的纹理，却有不同接触方式。外观上一个较大的角度，可能来自材料化学、粗糙纹理、复合接触或它们的共同作用。若需要区分机制，应增加表面形貌、压力或浸润过程的观察，而不是把一个角度反算成唯一微观结构。

$$
\cos\theta_W=r\cos\theta_Y,\qquad \cos\theta_{CB}=f_s(1+\cos\theta_Y)-1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4c6f875f1bc533cb7355276e.svg) | 理想充分填充粗糙纹理的表观接触角。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f985068e4f235683ab2c6131.svg) | 固体与气体复合接触的简化表观角。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d941e2f726e4aeecee316d62.svg) | 同种材料理想平整表面的Young角。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 实际固体面积与投影面积之比，无量纲且不小于1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9112d329658776a27244df88.svg) | 投影接触区内与固体接触的面积分数，无量纲，0至1。 |

两个式子对应不同接触状态。θY=60°、r=1.5给出θW=41.410°；θY=110°、fs=0.2给出θCB=150.274°。余弦右侧需处于−1至1，状态假定需由实验支持。

例如理想平整表面的角度为60°、粗糙度因子为1.5时，Wenzel关系给出约41.41°。另一个例子中，平整表面角度为110°，固体接触面积分数为0.2，固体与气体复合接触的简化关系给出约150.27°。这两个数对应不同假定，不是同一个样品的两种任意算法。若公式右侧超出余弦允许的范围，说明所假定的有限角度状态不能按这个简单形式继续求解，应回到铺展或状态转变的问题。计算应帮助检查物理图像，而不是用截断数值掩盖不合适的状态假定。

![规定阈值的教学模型：前进100°、后退70°，接触线钉扎时保持底面半径，运动时保持对应角度。下排比较完全填充与固体–气体复合接触的局部纹理，示意不按比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a0ce1c6c1c33d64c2638de7f.svg?v=a0ce1c6c1c33)

图 3规定阈值的教学模型：前进100°、后退70°，接触线钉扎时保持底面半径，运动时保持对应角度。下排比较完全填充与固体–气体复合接触的局部纹理，示意不按比例。

生物材料还可能在测量期间吸水、溶胀或释放小分子。水滴高度下降，既可能来自接触线向外铺展，也可能来自液体进入材料，或向空气蒸发；三者可以同时发生。观察底面半径、高度、体积与时间，比只画接触角随时间下降更能区分过程。对于长期浸液使用的材料，可以根据问题选择浸没条件下的气泡法或其他界面表征，并明确角度从哪一相读取。干态水接触角为表面提供一种可比较的起点，蛋白质吸附与细胞行为则还需要各自的实验来连接。

例如两种聚合物薄膜在空气中的水接触角接近，但进入含蛋白质溶液后，可能形成不同的吸附层。细胞随后接触的是这个不断变化的界面，而不只是最初干燥薄膜上的化学基团。要把润湿与细胞黏附连接起来，可以先记录表面处理和水接触角，再在相同浸泡条件下测量蛋白质吸附量与保留状态，最后比较细胞实验。这样每一步都有对应的对象和时间，避免把某一个“最佳角度”当成所有生物材料通用的设计目标。

## 把基线移动一点，看看“材料性质”会不会跟着变

下面的交互实验使用理想球冠，允许改变真实接触角、液滴体积和分析基线偏移。实线是同一个几何模型的液滴轮廓，水平参考线表示真实表面，另一条线表示分析时采用的基线。先把偏移设为零，改变体积：在这个忽略重力的模型中，液滴整体放大或缩小，而接触角保持设定值。随后固定真实角度和体积，移动分析基线，观察估计角度怎样改变。这个对比把真实形状变化与图像解释变化分开，让基线的作用可以直接看到。

再比较较小和较大的液滴。相同的绝对基线偏移，对尺寸较小的液滴占更大比例，因此往往带来更明显的角度变化。换句话说，像素尺寸、放大倍数和液滴大小共同决定接触点附近的几何精度。交互还显示球冠底面半径与高度，便于把角度变化连回实际长度。若真实实验中的液滴已经因重力明显变扁，或左右轮廓显著不对称，应选择符合该状态的分析模型；交互中的球冠关系则保留为一个容易核对的几何基准。

## 球冠与基线：角度改变来自哪里

理想球冠，忽略重力。绿色为真实表面，紫色为分析基线；负偏移时，圆模型交点向真实轮廓下方外推。改变体积与改变基线，比较两者对角度的不同作用。

[Figure: 球冠真实与分析基线比较](https://ml-biomat.com/tutorials/experimental-methods/p03/#P03-plot)

## 完整例子：保存轮廓，而不只保存一个角度

完整Python例子首先根据给定体积和角度生成球冠轮廓，加入固定种子的坐标噪声，再用最小二乘拟合圆。最小二乘让所有轮廓点共同约束圆的位置与大小，避免只依赖最高点和两个接触点；随后仍需要基线确定接触角。程序导出轮廓坐标、径向残差和基线敏感性表，并重复生成300组独立噪声，展示在固定几何与固定误差模型下的拟合波动。这样，轮廓拟合、基线选择和重复性分别保留了可检查的证据。

第二部分实现规定阈值的加液—抽液模型，保存体积、角度与底面半径的完整路径。代码中的100°和70°是模型输入，30°滞后由二者相减得到；它们用于说明钉扎过程，不是从前一组70°静态轮廓中推断出来的材料参数。第三部分则计算两个理想粗糙接触例子，并把模型的接触状态画出来。将这些关系分开保存，可以清楚回答每一个数是设定的、拟合的还是根据物理假定算出的。

整理重复结果时，也应保留样品之间与样品内部的区别。标准差描述所观察重复值的分散，均值的不确定度则还取决于独立重复数量和共同误差。反复处理同一张图片可以检验算法对操作的敏感性，却不会增加独立样品数，也不会发现所有表面污染问题。将原图、轮廓、基线位置和样品编号联系起来，后续就能判断异常值来自图像识别、局部表面还是制备差异，并针对相应环节补充实验。

在实际研究中，可以把同样的记录思路用于一组表面处理实验：保持探针液体和测量过程一致，观察不同样品位置的轮廓，比较前进与后退行为，再结合表面形貌或化学分析判断处理改变了什么。接触角很适合提供界面状态的快速线索，但其解释依赖液体本身的性质。若液体中加入表面活性剂、蛋白质或其他溶质，液气表面张力也会随浓度与时间变化。下一节将把注意力从液滴与固体的相遇，转向液体界面自身的张力，理解它怎样通过力与形状被测量出来。

### 完整Python：球冠轮廓、基线与接触角滞后

生成指定球冠与噪声，拟合圆并改变基线，重复300次检查波动，再计算规定钉扎阈值下的加液—抽液路径。

```
"""Contact-angle geometry, contour fitting and an explicit pinning model.
All droplet observations are constructed teaching data. Historical excerpt:
Thomas Young (1805), An Essay on the Cohesion of Fluids, p. 66; public domain.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import brentq
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc,Rectangle

def cap(volume_ul,angle_deg):
    theta=np.deg2rad(angle_deg);R=(3*volume_ul/(np.pi*(1-np.cos(theta))**2*(2+np.cos(theta))))**(1/3)
    return R,R*np.sin(theta),R*(1-np.cos(theta))

def contour(volume_ul,angle_deg,n=180):
    R,a,h=cap(volume_ul,angle_deg);u=np.linspace(-np.deg2rad(angle_deg),np.deg2rad(angle_deg),n)
    return R*np.sin(u),R*np.cos(u)-R*np.cos(np.deg2rad(angle_deg))

def circle_fit(x,y):
    b=np.linalg.lstsq(np.column_stack([2*x,2*y,np.ones(len(x))]),x*x+y*y,rcond=None)[0]
    return b[0],b[1],np.sqrt(b[2]+b[0]**2+b[1]**2)

def apparent_angle(R,cy,baseline):return float(np.rad2deg(np.arccos(np.clip((baseline-cy)/R,-1,1))))

def pinned_volume(a,theta):
    t=np.deg2rad(theta);h=a*np.tan(t/2);return np.pi*h*(3*a*a+h*h)/6

def hysteresis():
    Vup=np.linspace(.5,2,101);Vdown=np.linspace(2,.15,151);initial_a=cap(.5,85)[1]
    up_angles=[];up_a=[]
    for v in Vup:
        if v<=pinned_volume(initial_a,100):theta=brentq(lambda t:pinned_volume(initial_a,t)-v,1,179);a=initial_a
        else:theta=100;a=cap(v,theta)[1]
        up_angles.append(theta);up_a.append(a)
    final_a=up_a[-1];down_angles=[];down_a=[]
    for v in Vdown:
        if v>=pinned_volume(final_a,70):theta=brentq(lambda t:pinned_volume(final_a,t)-v,1,179);a=final_a
        else:theta=70;a=cap(v,theta)[1]
        down_angles.append(theta);down_a.append(a)
    return np.r_[Vup,Vdown],np.r_[up_angles,down_angles],np.r_[up_a,down_a],len(Vup)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if args.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839'
    def save(f,n):f.savefig(out/f'{n}-{args.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    volume=.5;angle=70.;R,a,h=cap(volume,angle);x,y=contour(volume,angle)
    rng=np.random.default_rng(1803);xn=x+rng.normal(0,.002,len(x));yn=y+rng.normal(0,.002,len(y))
    cx,cy,rf=circle_fit(xn,yn);fitted=apparent_angle(rf,cy,0)
    residual=np.sqrt((xn-cx)**2+(yn-cy)**2)-rf
    offsets=np.linspace(-.03,.03,121);sensitivity=np.array([apparent_angle(rf,cy,b) for b in offsets])
    monte=[]
    for k in range(300):
        ccx,ccy,rr=circle_fit(x+rng.normal(0,.002,len(x)),y+rng.normal(0,.002,len(y)));monte.append(apparent_angle(rr,ccy,0))
    vols,angles,radii,split=hysteresis()
    summary={'specified_angle_deg':angle,'fitted_angle_deg':fitted,'cap_radius_mm':float(R),'base_radius_mm':float(a),'height_mm':float(h),
       'recovered_volume_ul':float(np.pi*h*(3*a*a+h*h)/6),'height_base_angle_deg':float(np.rad2deg(2*np.arctan(h/a))),
       'baseline_plus20um_angle_deg':apparent_angle(rf,cy,.02),'monte_carlo_sd_deg':float(np.std(monte,ddof=1)),
       'young_angle_deg':float(np.rad2deg(np.arccos(36/72))),'wenzel_60_r15_deg':float(np.rad2deg(np.arccos(1.5*np.cos(np.deg2rad(60))))),
       'cassie_110_f02_deg':float(np.rad2deg(np.arccos(.2*(1+np.cos(np.deg2rad(110)))-1))),
       'hysteresis_deg':30,'bond_R':float(1000*9.81*(R*.001)**2/.072),
       'data_kind':'Constructed spherical-cap observations and prescribed pinning model'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(out/'data.csv',np.column_stack([xn,yn,residual]),delimiter=',',header='x_mm,y_mm,radial_residual_mm',comments='')
    np.savetxt(out/'hysteresis.csv',np.column_stack([vols,angles,radii]),delimiter=',',header='volume_ul,angle_deg,base_radius_mm',comments='')
    np.savetxt(out/'baseline_sensitivity.csv',np.column_stack([offsets,sensitivity]),delimiter=',',header='baseline_mm,angle_deg',comments='')
    fig,axs=plt.subplots(1,2,figsize=(12,5),gridspec_kw={'width_ratios':[1.1,1]});left,right=axs
    left.imshow(Image.open(Path(__file__).parent/'data/young1805-excerpt.png'));left.axis('off');left.set_title(tr('A  Young，1805年原文第66页','A  Young, 1805, original page 66'),loc='left')
    xx,yy=contour(.5,60);aa=cap(.5,60)[1];right.fill_between(xx,yy,0,color='#c8e4e7');right.plot(xx,yy,color=blue,lw=2);right.axhline(0,color='#576d7b')
    px=aa
    right.annotate('',xy=(px+.35,0),xytext=(px,0),arrowprops={'arrowstyle':'->','color':orange,'lw':2});right.text(px+.12,-.1,'γSV',color=orange)
    right.annotate('',xy=(px-.35,0),xytext=(px,0),arrowprops={'arrowstyle':'->','color':green,'lw':2});right.text(px-.37,-.1,'γSL',color=green)
    right.annotate('',xy=(px-.2,.346),xytext=(px,0),arrowprops={'arrowstyle':'->','color':blue,'lw':2});right.text(px-.14,.38,'γLV',color=blue)
    right.add_patch(Arc((px,0),.35,.35,theta1=120,theta2=180,color=orange,lw=2));right.text(px-.23,.09,'θ')
    right.set_aspect('equal');right.set_xlim(-.9,1.15);right.set_ylim(-.22,.85);right.axis('off');right.set_title(tr('B  在液体一侧读角度','B  Read the angle through the liquid'),loc='left');save(fig,'history')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8.7));p1,p2,p3,p4=axs.ravel()
    p1.scatter(xn,yn,s=7,color=blue,label=tr('构造轮廓点','Constructed contour points'));tt=np.linspace(-np.deg2rad(fitted),np.deg2rad(fitted),300);p1.plot(cx+rf*np.sin(tt),cy+rf*np.cos(tt),color=orange,label=tr('圆拟合','Circle fit'))
    p1.axhline(0,color=green,label=tr('真实基线','True baseline'));p1.axhline(.02,color='#a14e6d',ls='--',label=tr('上移20 μm','Raised by 20 μm'));p1.set_aspect('equal');p1.set_xlabel('x / mm');p1.set_ylabel('y / mm');p1.legend(fontsize=8);p1.set_title(tr('A  轮廓与基线','A  Contour and baseline'),loc='left')
    p2.scatter(np.arange(len(residual)),residual*1000,s=9,color=blue);p2.axhline(0,color='#a1abb2');p2.set_xlabel(tr('轮廓点索引','Contour index'));p2.set_ylabel(tr('径向残差 / μm','Radial residual / μm'));p2.set_title(tr('B  模型与观测的差','B  Model-to-observation differences'),loc='left')
    p3.plot(offsets*1000,sensitivity,color=orange);p3.axhline(70,color=green,ls=':');p3.axvline(0,color='#a1abb2');p3.set_xlabel(tr('基线偏移 / μm','Baseline offset / μm'));p3.set_ylabel(tr('测得接触角 / °','Estimated angle / °'));p3.set_title(tr('C  基线误差的系统影响','C  Systematic effect of baseline error'),loc='left')
    p4.hist(monte,bins=20,color=blue,alpha=.8);p4.axvline(70,color=orange);p4.set_xlabel(tr('重复噪声模拟的角度 / °','Angles across repeated noise simulations / °'));p4.set_ylabel(tr('次数','Count'));p4.set_title(tr('D  300次固定真值重复','D  300 repeats at fixed true geometry'),loc='left')
    fig.tight_layout();save(fig,'measurement')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8));p1,p2,p3,p4=axs.ravel()
    for v,t,aa,col,lab in [(vols[:split],angles[:split],radii[:split],blue,tr('加液','Add liquid')),(vols[split:],angles[split:],radii[split:],orange,tr('抽液','Withdraw liquid'))]:
        p1.plot(v,t,color=col,label=lab);p2.plot(v,aa,color=col,label=lab)
    p1.set_ylabel(tr('角度 / °','Angle / °'));p2.set_ylabel(tr('接触底面半径 / mm','Contact-base radius / mm'))
    for p in [p1,p2]:p.set_xlabel(tr('体积 / μL','Volume / μL'));p.legend()
    p1.set_title(tr('A  规定阈值的钉扎模型','A  Pinning model with prescribed thresholds'),loc='left');p2.set_title(tr('B  角度变化时接触线可不移动','B  The contact line can remain fixed'),loc='left')
    for p,title,filled in [(p3,tr('C  Wenzel：液体填满纹理','C  Wenzel: liquid fills texture'),True),(p4,tr('D  Cassie：纹理间保留气体','D  Cassie: gas remains in the texture'),False)]:
        p.set_xlim(0,6);p.set_ylim(-.3,1.6);p.axis('off');p.add_patch(Rectangle((0,-.3),6,.3,color='#576d7b'))
        if filled:p.add_patch(Rectangle((0,0),6,1.1,color='#c8e4e7'))
        else:p.add_patch(Rectangle((0,.65),6,.45,color='#c8e4e7'))
        for start in np.arange(.3,6,1.2):p.add_patch(Rectangle((start,0),.5,.65,color='#576d7b'))
        p.plot([0,6],[1.1,1.1],color=blue,lw=2);p.set_title(title,loc='left');p.text(3,1.3,tr('局部接触状态示意，非整滴轮廓','Local contact states, not whole-drop outlines'),ha='center',fontsize=9)
    fig.tight_layout();save(fig,'hysteresis')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Thomas Young — An Essay on the Cohesion of Fluids (1805)](https://upload.wikimedia.org/wikipedia/commons/8/85/Thomas_Young-An_Essay_on_the_Cohesion_of_Fluids.pdf)

   第65–66页原文与历史接触角概念。

   Public domain; p. 66 excerpt reproduced.
2. [Wikimedia Commons — Young paper rights and bibliographic record](https://commons.wikimedia.org/wiki/File:Thomas_Young-An_Essay_on_the_Cohesion_of_Fluids.pdf)

   原文作者、年代与公有领域声明。

   Public Domain Mark 1.0 for the historical scan.
3. [KRÜSS — Contact angle and measurement methods](https://www.kruss-scientific.com/en/know-how/glossary/contact-angle)

   角度定义、座滴与其他测量方式。

   Public manufacturer reference; no illustration copied.
4. [KRÜSS — Young equation](https://www.kruss-scientific.com/en/know-how/glossary/youngs-equation)

   理想平衡与界面量的关系。

   Public manufacturer reference; no illustration copied.
5. [KRÜSS — Hysteresis of contact angle](https://www.kruss-scientific.com/en/know-how/glossary/hysteresis-of-the-contact-angle)

   前进、后退、钉扎与动态测量。

   Public manufacturer reference; original model used.
6. [KRÜSS — Young–Laplace fit](https://www.kruss-scientific.com/en/know-how/glossary/young-laplace-fit)

   曲率、重力与轮廓模型选择。

   Public manufacturer reference; no illustration copied.
7. [KRÜSS — Surface roughness and wetting](https://www.kruss-scientific.com/en/know-how/glossary/roughness)

   Wenzel与Cassie–Baxter状态及面积定义。

   Public manufacturer reference; original diagrams used.
8. [KRÜSS — Height-width method](https://www.kruss-scientific.com/en/know-how/glossary/height-width-method)

   球冠几何与真实液滴偏离圆弧时的处理。

   Public manufacturer reference; no code copied.
