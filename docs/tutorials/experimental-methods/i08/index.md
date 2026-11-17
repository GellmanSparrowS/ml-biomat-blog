# 显微CT：把投影还原成三维结构

Source: https://ml-biomat.com/tutorials/experimental-methods/i08/
Language: zh-CN

用多方向投影恢复内部截面，再分清孔隙体积与贯通通路。

## 海绵里面的孔，是房间还是相通的走廊

拿起一块海绵，表面的小孔很容易看见，但水为什么能穿过整块材料，却不能只看表面回答。孔隙可能互相连接，也可能像封闭的房间一样藏在内部。组织工程支架、泡沫塑料、电池电极和骨组织都有类似的问题：内部空隙占多少体积，通道在什么方向贯通，承载的细梁有多厚，裂纹是否从表面延伸到了深处。把样品切开可以看到一个截面，但切的位置不同，答案就可能不同；切割还会破坏原来的三维关系。显微CT利用许多方向的X射线投影，在计算机中重建内部体积，使我们能沿任意方向观察这些空间联系。

CT是计算机断层成像的缩写。“断层”不意味着仪器真的把物体切成薄片，而是重建结果允许我们像翻阅一摞透明地图一样查看内部层面。普通X射线照片把一条射线路径上的贡献叠加到同一个位置，前后结构可能彼此遮挡；CT通过改变观察方向，取得许多不同的叠加关系，再求出哪些空间分布能够同时解释这些投影。显微CT把这套思想用于较小样品和更细的空间尺度，常见实验对象从骨小梁、昆虫和种子，到复合材料、微型零件和多孔支架。

本节用两个明确构造的教学对象贯穿原理。第一个是包含不同衰减区域的圆形截面，我们知道它的真实结构，可以检验投影和重建怎样改变图像。第二个是带有贯通通道、窄颈、侧向分支和封闭小孔的三维方块，用来比较孔隙率与连通性。前者帮助理解“怎样从叠影得到截面”，后者帮助理解“得到截面后怎样回答材料问题”。两组数据都由完整代码生成，图中展示的是对应计算结果，尺寸、灰度与分析条件可以逐一改变。

## 把叠在一起的影子分开，曾经比拍得更细更重要

早期X射线成像已经能看见骨骼和金属，但影像中不同深度的组织常常叠在一起。CT发展中的关键突破，是把“从不同方向测量”与“用计算恢复截面”结合起来。Cormack研究了由透射测量恢复内部衰减分布的问题，Hounsfield则推动了实际扫描设备的实现；两人因计算机辅助断层成像的发展共同获得1979年诺贝尔生理学或医学奖。这里值得理解的不是一台机器突然变得无所不能，而是测量目标发生了变化：研究者愿意花时间取得多方向信息，换取把深度重叠分开的能力。

图中左侧用平行射线、平移与改变方向说明早期逐线测量的思想，右侧则画出现代实验室显微CT常见的几何关系：X射线从小焦点向外发散，样品放在旋转台上，另一侧的平面探测器记录投影。图中只画侧视平面，真实光束还向纸面前后展开，形成锥束。小焦点和几何放大有助于观察细节，但放大越高，能够完整放入视野的样品范围通常越小。不同设备也可能采用平行束或其他扫描轨迹，因此分析软件需要知道实际几何，不能把所有投影都当成同一种相机照片。

一个直观练习是想象有两颗小珠子，恰好沿你的视线前后排列。只拍一张投影，两颗珠子可能重合成一个亮点；转到另一个角度，它们便分开了。对于复杂样品，情况更像同时解许多有关加法的题目：每条射线告诉你沿途总共减弱了多少，却没有直接标明每一小段分别贡献多少。足够丰富的方向约束了这些可能的分配。图像重建因此不是给照片增加立体阴影，而是根据成组的测量关系估计内部数值分布。

![原创原理示意，连接1970年代CT发展与现代实验室几何。A为逐线平移与多方向测量思想，B为发散锥束的侧视和旋转样品；不按比例，也不是历史设备复刻。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9c9e6c1faf81832ff3b2dd91.svg?v=9c9e6c1faf81)

图 1原创原理示意，连接1970年代CT发展与现代实验室几何。A为逐线平移与多方向测量思想，B为发散锥束的侧视和旋转样品；不按比例，也不是历史设备复刻。

## 探测器先看到光变弱，随后才得到内部灰度

X射线穿过物体时，一部分光子因吸收或散射离开原来的探测路径。在射线能量单一、窄束近似合适的情形下，同一种材料越厚，透过的强度按指数规律下降。线性衰减系数描述单位长度使射线减弱的程度，它的单位是长度的倒数。这个量与材料组成、密度和X射线能量有关，因此图像中某处更亮，首先表示在指定条件下重建的衰减更高；要进一步换成矿物密度或某种组分含量，需要相应标准和校准，而不是把灰度直接叫作质量。

$$
I=I_0e^{-\mu L},\qquad p=-\ln(I/I_0)=\mu L
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f9665f604056f523b647279.svg) | 透过强度与入射强度，使用同一探测单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 均匀材料的线性衰减系数，mm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 射线路径长度，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 负对数透过率，亦为本例路径衰减积分，无量纲。 |

单能窄束、均匀材料且已完成背景归一时，μ=0.4 mm⁻¹、L=2 mm给出I/I0=0.449329、p=0.8。非均匀路径用各小段μΔL相加。

例如均匀材料的衰减系数为0.4 mm⁻¹，射线穿过2 mm后，透过强度约为入射强度的44.93%。取透过率的负自然对数得到0.8，恰好等于衰减系数与厚度的乘积。若沿途有多种材料，就把每一段的“衰减系数乘长度”相加。对数这一步把沿路径连续相乘的透过比例转换成可以相加的量，正好适合后续重建。于是一个探测器读数经过处理后，成为一条射线路径上的衰减积分，而不是那个探测器像素正前方某一个小点的密度。

真正的探测器还存在暗信号和像素响应差异。关闭或遮挡射线时的读数帮助估计暗场；没有样品时的照射记录提供平场，用来观察同一束光在不同探测位置的响应。样品图先扣暗场，再除以同样扣暗场的平场，才能得到较合理的透过率。若某个像素一直偏亮或偏暗，它会在一连串投影里留下固定位置的异常；重建把这种固定误差绕旋转轴传播，可能形成环状伪影。这个例子把仪器校准与图像里的具体形状联系起来，也说明漂亮的三维渲染不能替代对投影质量的检查。

$$
T=\frac{S-D}{F-D},\qquad p=-\ln T
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 校正后透过率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 有样品时同一探测像素的读数，共同探测单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 同条件暗场读数，与S同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 无样品平场读数，与S同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 该射线的负对数透过率，无量纲。 |

例如S=510、D=10、F=1010，则T=500/1000=0.5，p=0.693147。要求F>D且扣暗后的读数处于有效动态范围；时间、响应和曝光条件应匹配。

实际实验室光源通常具有一段能量分布。较低能量的X射线往往先被衰减，穿过厚材料后，剩余光束的平均能量提高，称为束硬化。若仍用最简单的单能模型解释，均匀材料的中心和边缘可能出现不同灰度，形成杯状变化。合适的滤片、能量条件、标准样品与重建校正共同帮助处理这类问题。校正量应通过截面、灰度剖面和已知对象来选择；把校正一律推到最大，可能引入新的结构偏差。准备扫描时先知道要比较的是形状、孔隙还是密度，才能决定哪些校准最关键。

## 从正弦图到截面：方向越少，条纹越容易留下来

把每个方向的一维投影并排排列，会得到一张称为正弦图的图。名字来自一个小对象在旋转测量中留下的轨迹：它投影到探测器上的位置随角度变化，常呈现类似正弦波的曲线。正弦图的一个轴是探测位置，另一个轴是方向，亮暗表示该路径的衰减积分。它不是样品的截面，也不是把很多照片简单压在一起；它保留的是重建所需的测量关系。识别这种坐标，能帮助我们在看到投影数据时避免把条带误认成样品里的纤维或层片。

最直观的重建办法叫反投影：把一条射线的测量值沿原来的路径“涂回去”，再把各个方向的结果相加。真正的结构位置会得到许多方向的共同支持，因此逐渐显出来；但每条路径也把数值涂到了本来没有对象的地方，于是简单相加会产生模糊的光晕。滤波反投影在涂回去之前调整投影中不同空间变化的贡献，补偿这种模糊。这里的滤波不是任意美化图像，而是重建数学的一部分；同时，强调快速变化也会影响噪声，因此实际算法常在边缘清晰度与噪声之间选择适合任务的处理方式。

六面板图把这几个步骤放在一起。左上角是已知截面，中央为它的解析投影，右上角是未滤波反投影；下排分别用12个方向和180个方向进行滤波重建，并画出较密方向重建减去真值的差异。教学例没有加入探测噪声，因此12方向图中的明显条纹主要展示角度采样不足。180方向的结果更接近原对象，但边缘仍受到离散网格、插值与有限采样的影响。差异图使用正负颜色显示高估和低估，比只看一个平滑的灰度图更容易判断误差集中在哪里。

![构造教学截面的解析投影与实际代码重建。A、D、E及差异F以mm⁻¹表示衰减；正弦图B和未滤波反投影C为无量纲。12方向与180方向使用同一几何和滤波，未加入探测噪声；差异图显示有限采样和插值的影响。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3a4e567da503b3d3d3a75b49.svg?v=3a4e567da503)

图 2构造教学截面的解析投影与实际代码重建。A、D、E及差异F以mm⁻¹表示衰减；正弦图B和未滤波反投影C为无量纲。12方向与180方向使用同一几何和滤波，未加入探测噪声；差异图显示有限采样和插值的影响。

本例在同一128×128网格上比较重建与真值，180方向的均方根误差约为0.050 mm⁻¹，12方向约为0.212 mm⁻¹。均方根误差先把每个像素的差平方，再求平均和开方，因此较大的局部误差会受到更强惩罚；数值与衰减系数同单位。这个比较说明在固定对象与算法下增加方向的作用，但不能直接当成所有仪器都应使用180方向的建议。所需方向数还受目标细节、视野、探测采样和噪声影响。实际扫描应围绕要量的最小结构进行设计，再用重建结果和标准对象检验是否达到要求。

## 体素有多小，与真正能分清多细，是两件相连的事

重建体积由许多小格子组成，每个格子叫体素，可以理解为三维像素。体素间距告诉我们数值在空间中多密地排列，却不单独决定仪器能分辨的细节。光源焦点、探测器模糊、机械稳定性、样品运动和重建滤波都会把边界扩散到多个体素。把同一张模糊照片放大到更多像素，不会自动找回原来丢失的细线；同样，把重建网格设得很小，也需要测量本身提供相应信息。分辨率可以用边缘响应、细线或其他合适标准对象来评价，报告时把体素间距与这种实际表现分别说明。

在材料与生物样品之间，这个区别格外重要。骨矿物与周围介质之间往往有较明显的衰减差异，细骨小梁较容易显现；含水软组织或水凝胶与水的衰减可能接近，内部边界就不容易区分。造影剂或染色可提高某些组分的对比度，但扩散不均、组织收缩和化学处理也可能改变样品。若研究的是湿态孔道，干燥后更清楚的图像未必保留原来的孔径；若研究的是金属填料，强衰减又可能带来明显条纹。样品状态与成像条件要服务于同一个研究问题。

扫描时间同样有空间代价。为了获得更多光子而延长曝光，能够改善某些随机波动，却也增加样品缓慢移动、失水或温度变化的机会。夹持方式需要足够稳定，同时避免压坏软材料或挡住主要视野。样品旋转到任何角度都应有足够透射并落在适当视野中；一个方向看起来尺寸合适，转到另一面可能会被截断。记录投影数、角度范围、曝光、滤片、源与样品距离及重建条件，目的都是让最后的三维数值能够对应到实际测量，而不是只保存一张很有立体感的截图。

体素单位的错误还会被三维计算放大。若把三个方向都为10 μm的间距误写成20 μm，单个体素体积就增加到原来的八倍，而不是两倍。孔隙率这种共同体积相除的比值可能保持不变，绝对孔隙体积、表面积和孔径却会受到不同影响。因此，检查一个看似正常的百分数，并不能替代单位检查。重采样到另一套网格时，也应同时更新空间间距；插值让数组尺寸发生变化，却不意味着样品在物理上膨胀或收缩。

还有一种经常被忽略的情况是部分体积效应：一个体素里同时包含固体和孔隙，重建灰度会落在两者之间。边界体素究竟算哪一类，就与分割规则有关。对于很粗的梁，这些混合体素只占表面附近的一小部分；对于仅有几个体素宽的细梁或窄通道，它们可能占据大半体积。于是同样的阈值改变，在粗结构上只稍微移动边界，却可能让细通道突然断开。这也是为什么孔隙率变化不大时，连通性仍可能发生很大的变化。

## 先定义研究区域，再数孔隙和寻找通路

计算孔隙率之前，先确定分母是什么。若把样品外部的空气也算进研究区域，孔隙率会随着裁剪框大小变化，材料本身却没有改变。研究区域应对应明确的样品体积，例如支架内部某个固定大小的区域、骨组织的某一解剖区域，或去除外部空气后的整体样品包络。随后根据灰度或更合适的分割方法，把每个体素归为孔隙、固体或其他组分。孔隙率是孔隙体积除以研究区域总体积；在等体素网格中，共同体素体积在比值里消去，便可以用体素数的比值计算。

$$
V_v=\Delta x\Delta y\Delta z,\qquad \phi=\frac{V_p}{V_{\mathrm{ROI}}}=\frac{N_p}{N_{\mathrm{ROI}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1b2d60b2f55270f4079ede68.svg) | 单个体素体积，mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec9221cb3cb38bb1f2a7546d.svg) | 三个方向体素间距，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | 孔隙率，无量纲；乘100得到百分比。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0aab7bc1436cffc0257cb238.svg) | 孔隙体积与研究区域总体积，mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a0a1fa56c4155ae51682658e.svg) | 孔隙与研究区域体素数，无量纲计数。 |

等体素网格使共同体积约去。间距0.01 mm给出体素体积10⁻⁶ mm³；3213/48³=0.0290527，即2.90527%。绝对孔隙体积0.003213 mm³。

教学方块有48×48×48个体素，三个方向间距均为0.01 mm，单体素体积为0.000001 mm³，总体积为0.110592 mm³。采用指定模糊条件和灰度阈值128时，有3213个体素归为孔隙，因此孔隙体积为0.003213 mm³，孔隙率约为2.905%。原始构造几何的孔隙率约为3.266%，二者的差别来自模糊、噪声、灰度量化和阈值选择。这里保留已知真值，让我们可以看到图像分析究竟恢复了什么，而不是把任何一次分割都当成材料的唯一真实边界。

连通性提出另一个问题：这些孔隙体素之间有没有连续路线？本节采用六邻域定义，即一个体素只与共享面的上、下、左、右、前、后六个邻居相连，单纯在棱或角上碰到不算。程序给每个独立孔隙团簇编号，再找出同时接触z方向两端面的团簇。把这些贯通团簇的体积除以全部孔隙体积，得到本节使用的贯通孔隙比例。分母与孔隙率不同，前者只问孔隙内部有多少参与指定方向的贯通，后者问整个研究区域有多少是孔隙。

$$
f_{\mathrm{span},z}=\frac{V_{\mathrm{pore\ clusters\ touching\ both}\ z\mathrm{\ faces}}}{V_p}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eaef2a2f98497936fa9a3119.svg) | 指定z方向贯通孔隙比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ebf93f58e7d2b4164904cc55.svg) | 按六邻域同时接触z两端面的孔隙团簇总体积，mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcf999839bc2e4b6bb4754e8.svg) | 研究区域内全部孔隙体积，mm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 指定的体积轴，方向标签。 |

按共享面连接体素，再识别同时接触两端的团簇。默认条件下3003/3213=0.9346405，即93.464%；本指标描述几何贯通，不包含流体黏度或通道水力阻力。

默认条件下，贯通孔隙比例约为93.46%，剩下的孔隙属于未连接两端的部分。这个比例并不等于流体渗透率：同样贯通的通路，窄颈尺寸、弯曲程度和表面作用不同，流动阻力仍会不同。图中的窄颈正好帮助区分这些概念。绿色区域代表按当前分割连接z两端的孔隙，橙色代表其他孔隙；随着模糊加大或阈值改变，一小段连接可能消失，使贯通比例从接近一突然变成零。曲线的跳变不是材料在交互时真的断裂了，而是图像与分割条件改变了我们恢复出的通路。

![构造三维方块：通道、窄颈、侧枝及独立孔。A、B为y索引20的截面，统计来自完整48³体积。绿色为连接z两端的孔隙；曲线比较模糊标准差σ为0.5、1、1.5体素时，阈值改变对体积分数和贯通比例的不同影响。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0e8eb458546464f79b5eea85.svg?v=0e8eb4585464)

图 3构造三维方块：通道、窄颈、侧枝及独立孔。A、B为y索引20的截面，统计来自完整48³体积。绿色为连接z两端的孔隙；曲线比较模糊标准差σ为0.5、1、1.5体素时，阈值改变对体积分数和贯通比例的不同影响。

## 移动阈值，看一条窄颈怎样决定整个通路

下面的交互使用同一个三维教学方块，提供三种已知模糊程度，并允许改变灰度阈值和观察切片。灰度越低越接近孔隙；阈值提高时，更多边界体素会被纳入孔隙。左图显示截面灰度，右图显示按当前条件得到的孔隙分类，体积分数与贯通比例由整个三维体积计算，而不是只数眼前这一张切片。先把模糊程度设为较小值，沿z方向浏览窄颈附近，再逐步增加模糊，观察结构在图像中怎样逐渐变得难分。

保持模糊条件不变时，缓慢移动阈值，会发现孔隙率通常连续地变化，贯通比例却可能突然跳变。原因是通路依赖最薄弱的连接：只要一个狭窄位置被判为固体，上下两段很大的孔隙就会分开。这个现象对真实支架分析很重要，因为研究者可能只报告一个稳定的总体孔隙率，却没有检查决定运输的窄颈是否已接近分辨极限。可以把相邻阈值下的截面和通路结果放在一起，找出结论敏感的位置，再决定是否需要更高分辨率扫描、互补测量或更明确的分割依据。

## 三维孔隙：阈值怎样改变贯通

构造教学体积48³，体素间距0.01 mm。灰度小于阈值判为孔隙；绿色连接z两端，橙色为其他孔隙。统计使用全部体积，切片只改变观察位置。

如果比较两种支架，不宜分别调阈值直到两张三维图都看起来最好。先在相同扫描与重建条件下确认灰度尺度可比较，再依据标准、相分布和局部边界选择分析规则；若材料成分导致灰度本来不同，则需要各自有物理依据的校准。最后把规则变化对结果的影响一起检查。这样做的收获是，图像中的差别能够逐步对应到材料结构，而不是来自两次不同的显示偏好。显示亮度和颜色可以帮助观察，测量使用的原始灰度、研究区域与分割规则则应清楚保留。

## 完整例子：让几何真值、重建与三维统计彼此核对

完整Python例子分为两个相互衔接的实验。二维部分直接计算圆形区域对射线路径的贡献，生成各方向的投影，再用滤波反投影恢复截面；因为投影来自解析几何，方向采样不足造成的条纹容易单独观察。三维部分建立带窄颈和孤立孔的体积，施加指定高斯模糊和固定种子的轻微噪声，量化成灰度后进行分割和六邻域连通分析。两部分各自保存数组，避免把二维投影例子误认为后面三维方块的真实扫描重建。

输出既包括图，也包括可以重新计算的数值。投影数组保存方向和探测坐标，体积数组保存灰度、构造孔隙真值及体素间距；表格列出不同模糊和阈值下的孔隙率、贯通比例和团簇数量。数值摘要还检验已知厚度平板的透过率、圆盘中心的解析路径积分与体素体积。这些检查分别对应物理衰减、投影几何和三维单位换算，使一个错误不容易被后面的漂亮图片掩盖。程序中所有长度单位一致，换用实际数据时同样应先确认单位和坐标，再进入统计。

最终交付一项显微CT研究时，最有解释力的组合通常包括样品位置明确的截面、合适的三维视图、量化定义和支持结论的比较。三维视图帮助人们理解通道怎样分布，截面帮助检查边界是否可信，统计回答孔隙和连通发生了多大变化。若要进一步解释支架为什么更容易被水浸润，还需要考察材料表面与液体的相互作用；孔道提供空间路线，表面润湿决定液体进入这些路线时的界面条件。接触角实验正好把这个问题转化为可以观察和计算的液滴形状。

比较实验还需要把样品与观察区域分开计数。同一块支架里裁出十个小立方体，可以帮助描述内部不均匀，却不能自动等同于十块独立制备的支架。若研究不同工艺的影响，应保留独立样品之间的变化，并说明每个样品的区域怎样选取。对于加载前后扫描，还要先把两个体积配准到共同位置，检查是否比较了同一条梁或同一个孔。颜色、透明度和观察方向可以帮助展示这些对应关系，但一张渲染图中某个细梁消失，也可能只是显示设置遮住了它；返回原截面和数值掩膜，才能确定结构是否改变。

### 完整Python：投影重建与三维孔隙连通

从已知几何生成投影，比较方向采样，再对独立构造体积分析灰度、孔隙和贯通通路，保存全部数组与敏感性表。

```
"""Original parallel-beam CT and porous-volume teaching experiment.
Run: python main.py --output results --language en
All specimens and signals in this example are constructed, with known geometry.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

def make_volume(sigma=1.0):
    z,y,x=np.indices((48,48,48));radius=np.where((z>=22)&(z<=25),1.2,4.)
    channel=(x-16)**2+(y-20)**2<=radius**2
    branch=(y-20)**2+(z-12)**2<=3**2
    isolated=(x-35)**2+(y-35)**2+(z-35)**2<=4**2
    pores=channel|branch|isolated
    field=ndimage.gaussian_filter((~pores).astype(float),sigma=sigma,mode='nearest')
    field+=np.random.default_rng(1708).normal(0,.015,field.shape)
    return np.rint(np.clip(field,0,1)*255).astype(np.uint8),pores

def metrics(gray,threshold=128):
    pore=gray<threshold
    labels,n=ndimage.label(pore,structure=ndimage.generate_binary_structure(3,1))
    connected=np.intersect1d(np.unique(labels[0]),np.unique(labels[-1]));connected=connected[connected>0]
    spans=np.isin(labels,connected);count=int(pore.sum())
    return {'pore_voxels':count,'porosity':float(pore.mean()),'components':int(n),
       'spanning_fraction':float(spans.sum()/count) if count else 0.,
       'pore_volume_mm3':count*.01**3},spans

def project(detector,angles,circles):
    result=np.zeros((len(detector),len(angles)))
    for cx,cy,r,mu in circles:
        distances=detector[:,None]-cx*np.cos(angles)-cy*np.sin(angles)
        result+=2*mu*np.sqrt(np.maximum(r*r-distances**2,0))
    return result

def reconstruct(sino,detector,angles,X,Y,filtered=True):
    if filtered:
        nfft=2**int(np.ceil(np.log2(len(detector)*2)))
        frequency=np.fft.rfftfreq(nfft,d=detector[1]-detector[0])
        filtered_sino=np.fft.irfft(np.fft.rfft(sino,n=nfft,axis=0)*2*np.abs(frequency[:,None]),n=nfft,axis=0)[:len(detector)]
    else:filtered_sino=sino
    recon=np.zeros(X.shape)
    for k,theta in enumerate(angles):
        recon+=np.interp((X*np.cos(theta)+Y*np.sin(theta)).ravel(),detector,filtered_sino[:,k],left=0,right=0).reshape(X.shape)
    return recon*np.pi/(2*len(angles))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if args.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    def save(f,n):
        f.savefig(out/f'{n}-{args.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    blue='#186c94';orange='#d27839';green='#188777'
    coord=(np.arange(128)-63.5)*.01;X,Y=np.meshgrid(coord,coord)
    circles=[(0,0,.45,1),(-.16,.08,.12,-.8),(.2,-.12,.08,.6)]
    truth=np.zeros(X.shape)
    for cx,cy,r,mu in circles:truth+=mu*((X-cx)**2+(Y-cy)**2<=r*r)
    detector=(np.arange(256)-127.5)*.01;angles=np.arange(180)*np.pi/180
    sino=project(detector,angles,circles)
    full=reconstruct(sino,detector,angles,X,Y);sparse=reconstruct(sino[:,::15],detector,angles[::15],X,Y)
    back=reconstruct(sino,detector,angles,X,Y,False)
    gray,pores=make_volume(1.);stats,spans=metrics(gray)
    series=[]
    for sigma in [.5,1.,1.5]:
        g,_=make_volume(sigma)
        for t in range(50,206,5):series.append([sigma,t,*[metrics(g,t)[0][k] for k in ['porosity','spanning_fraction','components']]])
    np.savetxt(out/'data.csv',series,delimiter=',',header='blur_sigma_voxels,threshold_uint8,porosity,spanning_fraction,components',comments='')
    np.savez_compressed(out/'volume.npz',gray=gray,truth_pores=pores,voxel_spacing_mm=.01)
    np.savez_compressed(out/'tomography.npz',truth=truth,sinogram=sino,angles_rad=angles,detector_mm=detector,reconstruction=full)
    summary={**stats,'truth_porosity':float(pores.mean()),'fbp_rmse_180':float(np.sqrt(np.mean((full-truth)**2))),
       'fbp_rmse_12':float(np.sqrt(np.mean((sparse-truth)**2))),
       'slab_transmission':float(np.exp(-.4*2)),'slab_log_projection':.8,
       'voxel_volume_mm3':.01**3,'roi_volume_mm3':(48*.01)**3,
       'analytic_disk_center_projection':float(project(np.array([0.]),np.array([0.]),[(0,0,.45,1)])[0,0]),
       'specimen':'Constructed teaching geometries; not a measured CT scan'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    fig,axs=plt.subplots(1,2,figsize=(12,4.7));a,b=axs
    a.set_xlim(-1,8);a.set_ylim(-2,2);a.axis('off');a.add_patch(Circle((3,0),1,facecolor='#cee3e7',edgecolor=blue))
    for yy in [-.65,0,.65]:a.annotate('',xy=(6.5,yy),xytext=(0,yy),arrowprops={'arrowstyle':'->','color':blue})
    a.add_patch(Rectangle((6.5,-1),.3,2,color=orange));a.text(3,1.4,tr('平移 + 改变方向','Translate + change direction'),ha='center')
    a.text(3,-1.45,tr('早期逐线测量的思想','Early line-by-line acquisition'),ha='center');a.set_title(tr('A  从叠影到断层：1970年代','A  From superposition to sections: 1970s'),loc='left')
    b.set_xlim(-1,8);b.set_ylim(-2,2);b.axis('off');b.scatter([0],[0],s=80,color=orange)
    b.add_patch(Circle((3,0),.7,facecolor='#cee3e7',edgecolor=blue));b.plot([6.7,6.7],[-1.7,1.7],lw=5,color=blue)
    for yy in np.linspace(-1.5,1.5,7):b.plot([0,6.7],[0,yy],color=orange,lw=1,alpha=.65)
    b.annotate('',xy=(3.7,.8),xytext=(2.3,.8),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=-.5','color':green})
    b.text(3,-1.35,tr('样品旋转','Rotating sample'),ha='center');b.set_title(tr('B  实验室锥束几何的侧视','B  Side view of laboratory cone-beam geometry'),loc='left',fontsize=11)
    save(fig,'geometry')
    fig,ax=plt.subplots(2,3,figsize=(13,8));extent=[-.64,.64,-.64,.64]
    items=[(truth,'A  已知衰减分布','A  Known attenuation'),(sino,'B  多角度投影：正弦图','B  Angular projections: sinogram'),(back,'C  未滤波反投影','C  Unfiltered backprojection'),(sparse,'D  12方向滤波重建','D  FBP: 12 directions'),(full,'E  180方向滤波重建','E  FBP: 180 directions'),(full-truth,'F  重建减真值','F  Reconstruction minus truth')]
    for k,(a,(arr,z,e)) in enumerate(zip(ax.ravel(),items)):
        if k==1:im=a.imshow(arr,extent=[0,180,detector[-1],detector[0]],aspect='auto',cmap='magma');a.set_xlabel(tr('方向 / °','Direction / °'));a.set_ylabel(tr('探测位置 / mm','Detector coordinate / mm'))
        else:
            kw={'cmap':'coolwarm','vmin':-.25,'vmax':.25} if k==5 else {'cmap':'gray','vmin':0,'vmax':float(back.max()) if k==2 else 1.6}
            im=a.imshow(arr,extent=extent,origin='lower',**kw);a.set_xlabel('x / mm');a.set_ylabel('y / mm')
        a.set_title(tr(z,e),loc='left',fontsize=11)
        cb=fig.colorbar(im,ax=a,shrink=.7);cb.set_label('1' if k in [1,2] else 'mm⁻¹')
    fig.tight_layout();save(fig,'reconstruction')
    fig,ax=plt.subplots(2,2,figsize=(11,9));a,b,c,d=ax.ravel()
    a.imshow(gray[:,20,:],origin='lower',extent=[0,.48,0,.48],cmap='gray',vmin=0,vmax=255);a.set_title(tr('A  y=20截面：窄颈与分支','A  Section y=20: throat and branch'),loc='left');a.set_xlabel('x / mm');a.set_ylabel('z / mm')
    colors=np.zeros(gray.shape+(3,));colors[gray<128]=[.82,.47,.22];colors[spans]=[.09,.53,.47]
    b.imshow(colors[:,20,:],origin='lower',extent=[0,.48,0,.48]);b.set_title(tr('B  绿色孔隙连接z两端','B  Green pores connect both z faces'),loc='left');b.set_xlabel('x / mm');b.set_ylabel('z / mm')
    series=np.asarray(series)
    for sig,color in zip([.5,1,1.5],[blue,green,orange]):
        r=series[series[:,0]==sig];c.plot(r[:,1],r[:,2]*100,color=color,label=f'σ={sig:g} voxel');d.plot(r[:,1],r[:,3],color=color,label=f'σ={sig:g} voxel')
    c.axhline(pores.mean()*100,color='#a1abb2',ls=':',label=tr('构造真值','Constructed truth'));c.set_xlabel(tr('灰度阈值','Gray threshold'));c.set_ylabel(tr('孔隙率 / %','Porosity / %'));c.legend(fontsize=9);c.set_title(tr('C  体积分数随分割变化','C  Volume fraction changes with segmentation'),loc='left')
    d.set_xlabel(tr('灰度阈值','Gray threshold'));d.set_ylabel(tr('贯通孔隙 / 全部孔隙','Spanning pore volume / all pore volume'));d.set_ylim(-.03,1.03);d.legend(fontsize=9);d.set_title(tr('D  窄颈连接可突然改变','D  Throat connectivity can change abruptly'),loc='left')
    fig.tight_layout();save(fig,'porosity')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [scikit-image — Radon transform example](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html)

   投影、正弦图、滤波反投影与离散重建。

   BSD-licensed open-source project; independent original implementation and figures here.
2. [ASTRA Toolbox — 2D geometries](https://astra-toolbox.com/docs/geom2d.html)

   平行束、扇束、探测间距与空间坐标定义。

   Public technical reference; no code or figure copied.
3. [Bruker — Overview of NRecon, method note MCT-62](https://www.bruker.com/content/dam/bruker/int/en/resources/bbio/pci-community/microct-notes/MN062_NRecon%20overview.pdf)

   投影与截面、束硬化、环状伪影及校正条件。

   Public manufacturer manual; figures not reproduced.
4. [IBSI — Image processing](https://ibsi.readthedocs.io/en/latest/02_Image_processing.html)

   体素、空间间距、插值与研究区域定义。

   Public technical reference; no image reproduced.
5. [Nobel Foundation — 1979 CT development perspective](https://www.nobelprize.org/prizes/medicine/1979/perspectives/?print=1)

   早期断层设备、多方向测量与Hounsfield和Cormack的历史。

   Historical institutional account; original illustration used.
6. [Kak and Slaney — Principles of Computerized Tomographic Imaging](https://www.slaney.org/pct/pct-toc.html)

   继续阅读射线积分、重建和采样。

   Authors permit personal use of electronic book; link only, no book pages or figures reused.
