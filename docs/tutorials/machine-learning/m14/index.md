# 从照片走向三维：相机、辐射场与点云

Source: https://ml-biomat.com/tutorials/machine-learning/m14/
Language: zh-CN

手算深度，沿射线看见颜色，再用PointNet式网络学习无序点集。

## 1. 一张照片缺少的，是沿视线方向的距离

伸出一根手指，先闭左眼，再闭右眼，手指会相对远处背景跳动。近物跳得明显，远物跳得较少，这个日常体验就是双目深度的重要线索。照片把三维世界压到平面上，同一条视线上的许多位置都可以投影到同一个像素。若想从照片测量距离、建立零件模型，或者换一个角度观看房间，就需要把相机、空间与图像之间的关系重新建立起来。三维视觉的学习，从认识这种信息缺失开始，比直接进入大型重建软件更容易掌握计算为什么成立。

本章涉及三种不同目标。几何重建关心物体在哪里、表面怎样连接；新视角合成关心从另一个相机位置会看到什么图像；点云学习关心一组空间采样点属于什么对象或部件。一个场景可以在已见过的方向上渲染得很逼真，却在少见视角下暴露错误形状；一组稀疏点云也可能足以识别椅子，却不足以精确制造它。先分清所需输出，才能选择坐标、表面、体密度或高斯基元等不同表示，并为结果设置合适的检查方式。

我们会先手算针孔投影与双目距离，再理解多视图如何联合求解相机与空间点。随后用一个明确定义的三维密度场沿射线累积颜色，查看遮挡和采样数量怎样改变像素；最后训练一个共享逐点网络，识别球面与立方体表面采样点，并验证打乱点的顺序不改变结果。NeRF、3D Gaussian Splatting 与 PointNet 的核心思想分别落在这些可检查的步骤中，模型名字因此对应具体的计算职责。

## 2. 相机是一个坐标转换器

描述空间点时，首先要说相对于哪里。世界坐标可以固定在桌面，相机坐标固定在镜头中心。相机移动后，同一个物体的世界坐标保持不变，相机坐标则改变。外参中的旋转和平移负责这次坐标转换；内参中的焦距和主点位置负责把相机坐标投到图像上。这里约定相机的正深度方向朝前，成像公式采用位于相机前方的虚拟像平面，因此不需要为倒立成像再额外写一个负号。使用其他软件时，应核对它的轴向与世界到相机、相机到世界的变换方向。

$$
p_c=Rp_w+t,\qquad u=f_x\frac{X_c}{Z_c}+c_x,\quad v=f_y\frac{Y_c}{Z_c}+c_y
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/544857d035238c222088f2be.svg) | 世界与相机坐标中的三维点列向量，单位m；pc=(Xc,Yc,Zc)ᵀ，Zc>0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3cafeb78b5a3fe4ab1afd21f.svg) | 3×3世界到相机的旋转矩阵，无量纲；3维平移向量，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d14b71953101044988436e00.svg) | 横纵焦距与主点坐标，全部以像素px表示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/487fcc1666d8aaba8b444887.svg) | 图像横纵坐标(px)与相机坐标分量(m)；此式暂不含镜头畸变。 |

先旋转、平移到相机坐标，再用相似三角形的坐标/深度比例投影。R为单位阵、t为零，点(0.3,0.15,3)m，fx=fy=800px，主点(320,240)px，得到u=800×0.3/3+320=400px，v=280px。同一视线上的(0.6,0.3,6)m也投到相同像素，说明单个投影缺少深度。

投影中除以深度，来自相似三角形。一个物体离相机越远，占据的视角越小，图像上的尺寸也越小。焦距以像素表示时，三维坐标之间的长度单位会在比值中相消，最终得到像素坐标。例如相机坐标为 (0.3,0.15,3) 米，焦距两个方向都是 800 像素，主点是 (320,240)，投影就落在 (400,280)。若把三维坐标全部换成毫米，只要三轴一致，结果仍然相同。把焦距的毫米值直接当像素值使用，则会混淆传感器尺度和图像采样尺度。

真实镜头还存在畸变。径向畸变让直线在图像边缘弯曲，切向畸变与镜头和成像平面的偏心有关。标定通过拍摄已知几何，例如不同姿态的棋盘格，寻找使投影点与观测角点尽量一致的内参与畸变参数。多个倾斜角度能提供比重复拍正面更多的几何约束。标定后改变焦距、裁切或图像分辨率，应相应更新参数。重投影误差是在图像坐标上比较预测和观测的距离，它告诉我们几何模型是否能解释这些角点，但还应检查视野覆盖与实际工作距离。

从像素反过来构造射线，也可以按同一组几何关系逐步完成：先减去主点，再分别除以横纵焦距，得到虚拟像平面上的两个归一化坐标；补上朝前的第三分量1，就得到一个方向，再归一化为单位向量。用相机姿态把方向转回世界坐标，就能从相机中心出发采样。还要区分相机深度和射线距离：沿中心轴时二者相同，倾斜射线走过的路更长。代码的深度图显示沿射线的加权距离，因此不会把它直接叫作相机坐标的Z值。

## 3. 两条视线交会，距离才有了约束

两台相机观察同一点时，可以从两条视线的交会估计空间位置。对经过校正、光轴平行的双目系统，对应点通常被变换到同一图像行，横向位置差称为视差。相机中心之间的距离叫基线。基线越大或焦距越长，同样深度产生的视差通常越大；物体越远，视差越小。下面的关系来自两组三角形的差，是双目测距最常用的入门算例。实际噪声使两条射线未必精确相交，三角化便需要寻找最符合观测的位置。

$$
d=u_L-u_R=\frac{fB}{Z},\qquad Z=\frac{fB}{d}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d3a304cfd8c87c33bffa627c.svg) | 校正后左、右图同一点的横坐标和视差，px；本约定正常前方点d>0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/978f149e4d511c2397b7abd1.svg) | 共同水平焦距(px)、水平相机基线(m)与相机前方深度(m)。 |

左相机投影为fX/Z，右相机相对于同一点的横坐标是X−B；两式相减消去X，得到fB/Z。f=800px、B=0.12m、Z=3m时，d=32px；反算800×0.12/32=3m。若测成31px，深度约3.097m；测成33px约2.909m，因此视差的一个像素误差已经对应约9至10cm的距离变化。公式要求校正后的几何与已知基线。

对于没有校正的相机，两幅图中的对应点遵循极线约束。第一幅图的一个像素对应一条空间射线，这条射线投到第二幅图上成为一条极线，因此对应点的搜索从整个二维图像缩到一条线附近。极线约束提供的是几何可能性，具体匹配还需要纹理和局部特征。重复窗格、光滑墙面和反光表面会使对应关系变得含糊。相机之间只有旋转、几乎没有平移时，射线缺少足够的视差，空间距离也就难以稳定确定。

从运动恢复结构 SfM 同时估计多张照片的相机姿态与稀疏空间点。一个典型流程先提取并匹配图像特征，再用几何一致性排除错误匹配，选择合适的初始视图，逐步加入新相机并三角化新点，最后用光束法平差共同优化相机与点的位置。Schönberger 与 Frahm 在 2016 年的工作系统讨论了这种增量重建，并给出开源 COLMAP 实现。它回应的是大量无序照片中的匹配、可靠初始化和持续优化问题，而不是为每一张照片单独猜出一个深度图。

多视图立体在已知相机附近进一步估计稠密深度，再融合成点云或表面。相机覆盖不足的背面不会凭空获得同等观测约束，透明与反光区域也未必服从简单的外观一致性。单目 SfM 通常只有相对尺度：把场景和相机平移距离一起放大，投影可以保持不变。要得到米或毫米，需要已知基线、标尺、可靠位姿或其他尺度信息。下面的深度—视差曲线显示，远处物体的视差变化越来越小，同样一个像素的匹配误差便会引起更大的距离误差。

![左：已知焦距800px和基线0.12m时的深度—视差关系，3m对应32px。右：测试集中的球面与立方体表面点云，每份64点，颜色表示归一化z坐标；坐标已居中并以最远点距离缩放。](https://ml-biomat.com/static/tutorials/machine-learning/figures/da3d6d5dca5686c78a589553.svg?v=da3d6d5dca56)

图 1左：已知焦距800px和基线0.12m时的深度—视差关系，3m对应32px。右：测试集中的球面与立方体表面点云，每份64点，颜色表示归一化z坐标；坐标已居中并以最远点距离缩放。

## 4. 点、面和场，各自保留什么信息

点云把观察到的位置记录成一组坐标，常附带颜色、法向或强度。它简单直接，适合激光扫描和多视图重建，但点之间没有默认连线，采样密度也可能不均匀。网格额外给出顶点如何组成三角形，因此便于计算表面法向、面积与渲染；连接错了，几何外形也会改变。体素把空间切成规则小格，便于使用三维卷积，但分辨率每个方向翻倍，格子数量会增加八倍。表示选择同时决定能保存的细节和需要承担的计算量。

隐式表示不逐个列出所有表面点，而是提供一个可查询函数。占据函数回答某位置在物体内部的概率；有符号距离函数回答离表面有多远，并用正负区分两侧；表面对应距离为零的集合。连续坐标可以在任意位置查询，但提取网格还需要在空间中采样并找出零等值面。辐射场又换了一种问题：在某个位置，体密度是多少，沿某个方向看过去会得到什么颜色？它以生成图像为目标，不必一开始就显式给出干净的三角网格。

不同“密度”不要混用。NeRF 体渲染中的密度描述沿长度累积的不透明程度，常用单位是长度的倒数；它不是材料质量密度，也不是点云中每立方米采了多少个点。一个射线样本的密度乘以所代表的区间长度，才形成无量纲的光学厚度。这个单位关系直接决定如何把“这里有多少遮挡”转换成透明度，也解释了为什么改变场景尺度时，密度和距离需要协调变化。

是否保留绝对尺寸，也取决于任务。点云居中和缩放可以让分类器专注形状，但会消去位置和大小；同形状的桌面模型与真实建筑因此可能得到相近输入。如果目标是质量、长度或空间放置位置，应保留被移除的尺度与平移信息，并在输出时恢复或将其作为额外特征。标准化不是无条件改善数据，而是主动决定哪些变化应该被忽略。这个决定应与预期不变性和最终测量单位一起记录。

## 5. NeRF：沿一条射线，把颜色逐层累积

想象透过几层有颜色的薄纱看白色背景。第一层贡献一部分颜色，剩余光量才继续到第二层，再到第三层。前面的层越不透明，后面的颜色对最终结果影响越小。体渲染把一条相机射线分成多个区间，在各区间查询密度和颜色，用由近到远的累积把它们合成为一个像素。这个过程同时体现几何位置、遮挡顺序和局部外观，不是把沿线所有颜色直接求平均。

$$
r(t)=o+t\,d,\quad \alpha_i=1-e^{-\sigma_i\Delta_i},\quad T_i=\prod_{j<i}(1-\alpha_j),\qquad C=\sum_{i=1}^{N}T_i\alpha_i c_i+T_{N+1}c_{\rm bg}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c183f0b2cce72055896ed3cf.svg) | 射线位置、相机中心(长度单位)、单位方向向量(无量纲)、沿射线的距离(长度单位)；d此处是向量，不是视差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aff3de4d1287f50ac8efc600.svg) | 由近到远的区间索引、前方区间索引、区间总数、区间长度；Δi与t使用同一长度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29c3a8316806774aaf842d39.svg) | 区间内近似常数的体密度(长度⁻¹)、不透明度和到达该区间的透射率(均无量纲)；T1=1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e6e788e985849507bdb7d611.svg) | 局部、背景和最终RGB三维列向量，本例为0至1的归一化颜色。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4d72c41288befef4e73ce70f.svg) | 穿过所有区间后的剩余透射率；各Tiαi与它相加为1。 |

均匀区间中透射率按指数衰减，密度与长度的乘积无量纲，1减透射率就是该区间截获的比例。Δ=1长度单位、σ=ln2/长度单位时，α=0.5。两层α均0.5，权重依次0.5、0.25，背景0.25，合计1。红(1,0,0)在蓝(0,0,1)前、白背景时，颜色为(0.75,0.25,0.5)。换采样数量时应改变Δ，保持积分区间一致，而不是让每个新样本继续沿用旧透明度。

令第一层红色、第二层蓝色，两层不透明度都为 0.5，背景为白色。红色先贡献 0.5，蓝色只接收到剩余的 0.5，所以贡献 0.25，白色背景贡献最后的 0.25。RGB 结果是 (0.75,0.25,0.50)；交换前后顺序则变成 (0.50,0.25,0.75)。两层的颜色和不透明度完全相同，顺序却改变画面。在交互中逐层前进，可以同时看到透射率、当前层权重和累积颜色，直接检查每一步的量如何守恒。

### 射线实验：逐层合成一个像素

光线从左向右穿过红、蓝、绿三层，后方为白色背景。每次只处理一层，未处理部分暂按白背景显示；调节透明度和顺序会重新计算当前步骤。

[Figure: 三层颜色的入射透射率、颜色权重与合成像素](https://ml-biomat.com/tutorials/machine-learning/m14/#M14-svg)

Mildenhall 等人在 2020 年的 NeRF 工作中，用一个神经网络表示连续辐射场：输入空间位置和观察方向，输出密度与依赖方向的颜色。相机像素对应一条射线，网络沿线接受查询，再经过可微体渲染得到像素；预测图像与真实照片之间的误差，通过这条计算链更新网络参数。位置编码把坐标扩展成多频率信号，帮助网络表达细节；更密集地采样重要区域，则把计算集中到可能影响像素的位置。方向相关颜色用于表达视角变化带来的外观差异，例如一定程度的高光变化。

本章先把“场是什么”与“怎样学习场”拆开。代码直接规定两个三维高斯形状的密度团及其颜色，从三个相机方向渲染，不进行 NeRF 拟合。这样得到的图像与射线深度可以逐项对照已知场，并检查增加采样数量时数值误差怎样下降。进一步学习 NeRF 时，需要把这个已知函数替换成可训练网络，使用训练视图提供像素损失，把留出的相机视图用于评价。已见视图的拟合、新视图的图像质量，以及几何尺寸准确性，应分别检查。

![已知三维密度场的三个相机视图，每射线96个中点采样](https://ml-biomat.com/static/tutorials/machine-learning/figures/3ab6736d7ed799c5f9075181.svg?v=3ab6736d7ed7)

图 2已知三维密度场的三个相机视图，每射线96个中点采样。上：归一化RGB合成；下：用Tiαi加权的射线距离除以总不透明度，表示条件加权距离；总不透明度小于0.05的射线隐藏。密度场由两个有色高斯团组成，图像为数值渲染，并非训练得到的NeRF重建。

渲染图中柔和的边缘来自我们规定的连续密度分布。高斯团的密度向外平滑衰减，所以边缘处透明度逐渐降低，更多白色背景透过来；这与训练不足造成的模糊是不同机制。增加射线样本会更准确地积分同一个柔和场，不会把它变成硬边球面。若希望验证硬表面的重建，应另行规定尖锐表面或有符号距离作为真值，再检查采样与网络是否能恢复该边界。区分目标场本身的性质与数值误差，是解释图像的重要一步。

## 6. 3D Gaussian Splatting：把场景写成可投影的椭球

体渲染沿每条射线查询许多位置，空区域也可能消耗计算。Kerbl 等人在 2023 年的 3D Gaussian Splatting 中，采用一组显式三维高斯基元表示场景，每个基元具有中心、方向与尺度、透明度，以及表示方向相关外观的参数。高斯的协方差决定椭球沿哪些方向伸展；球形只需要相同尺度，细长表面片则可以用各向异性椭球更紧凑地表示。相机改变时，基元投影到像平面上形成二维椭圆状覆盖，再按可见性和前后关系混合颜色。

$$
g(x)=\exp\!\left[-\tfrac12(x-\mu)^{\mathsf T}\Sigma^{-1}(x-\mu)\right],\qquad \Sigma_{\rm image}\approx J R\Sigma R^{\mathsf T}J^{\mathsf T}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/313be2bc3b1ea3e88ce189b7.svg) | 三维查询位置、中心(长度单位)、对称正定3×3协方差矩阵(长度²)；二维算例采用对应2维版本。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a9e111e418e432fd154a819b.svg) | 未乘透明度的高斯形状权重，无量纲；没有概率密度的归一化常数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1921007cc69f5e372ba69af9.svg) | 世界到相机旋转3×3(无量纲)、投影在中心附近的2×3雅可比(px/长度)、近似二维投影协方差2×2(px²)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b5661152420d3e399df6a285.svg) | 转置与矩阵逆；二次型把位移按各方向尺度衡量，得到无量纲指数。 |

二维中心为零，Σ=diag(1,1)时，x=(2,0)得到g=exp(−2)≈0.1353。改为Σ=diag(4,1)，横向标准差为2，得到g=exp(−0.5)≈0.6065。投影协方差先经旋转改变坐标系，再用局部线性投影J把长度变化映成像素变化；因此输出单位为px²。这个局部近似解释高斯椭球怎样形成图像椭圆，实际渲染还要处理透明度、深度排序和像素覆盖。

一个直观算例是把高斯的横向标准差从 1 增到 2，同时保持纵向标准差为 1。在距离中心横向 2、纵向 0 的位置，未乘透明度的高斯权重由 exp(−2)≈0.135 增到 exp(−0.5)≈0.607，说明覆盖范围沿横向变宽。三维到二维的投影则还要考虑相机旋转以及透视投影在中心附近的局部变化，协方差不能简单删掉第三行第三列。靠近相机的相同基元往往覆盖更多像素，视角改变也会改变投影椭圆的方向与大小。

训练使用可微渲染把图像误差传回高斯中心、形状、透明度和颜色参数，并在优化过程中调整基元数量与分布，例如对需要更多细节的位置分裂或增密，对贡献很小的基元删减。NeRF 的常见表述是“按位置查询网络”，3DGS 的常见表述是“投影并混合显式基元”，二者都需要相机和多视图信息。它们得到的漂亮外观并不自动等于可用于力学网格的封闭表面；若研究目标是尺寸、法向或拓扑，应把这些几何量单独提取并与观测比较。

## 7. PointNet：一袋没有顺序的点怎样进入网络

一张点云可以先列出最高的点，也可以先列出最靠左的点，物体本身没有改变。直接把所有坐标按顺序拼成很长的向量，会让网络把排列误认为形状。Qi 等人在 2017 年发表的 PointNet 让每个点经过同一组网络，再用对输入顺序不敏感的最大值操作汇总。可以把它想成向所有点询问同一组问题，每个问题保留全体点中最强的回应；点的到达顺序不影响这些最强回应。由此得到固定长度的全局表示，再完成对象分类。

$$
h_i=\phi(p_i),\quad z_k=\max_{1\le i\le N}h_{ik},\qquad \widehat y=\psi(z)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/64ce1240f88a388826694962.svg) | 第i个三维点列向量、点索引及点数；代码N=64，坐标居中并缩放为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3ee18f897c9f94e3975aff0c.svg) | 所有点共享的神经网络、F维点特征与其第k分量；代码F=64，隐藏量无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3da56523af656a4dda677791.svg) | 通道索引、该通道的点集最大值、F维全局表示；不同通道的最大值可由不同点贡献。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ae4dec2f081c6c8cbdad8485.svg) | 分类头与类别分数向量；代码输出2个无量纲logit，再取最大分数对应类别。 |

三个点的二维隐藏特征为(1,4)、(3,2)、(2,5)，逐通道最大值为z=(3,5)。任意交换三个点的顺序，z都不变；共享φ保证每个点的处理规则也不变。整个对象分类因此具备置换不变性。逐点分割可把z与每个hi拼接再分类，输出随点序相同重排。最大值运算本身没有约束旋转后的坐标怎样变化，旋转性质需要另外设计。

若任务是给每个点分配部件类别，模型还要保留局部逐点特征，并把全局表示复制回每个点，与局部信息拼接，再输出逐点标签。整个物体是什么，可以帮助解释某个局部点属于椅背还是椅腿。原始 PointNet 还包含输入与特征对齐模块；本章的小网络保留共享逐点变换和最大值汇总这条核心路径，使用训练数据中的随机旋转来增加方向变化。置换不变来自计算结构，旋转不变则是另一种要求，不能因为使用了最大值汇总就认为也自动满足。

实验生成球面与立方体表面的点云，每份包含 64 个点。每份点云经过随机正交旋转、减去点均值，再按最远点距离缩放，使输入处于可比较的尺度；训练、验证、测试分别有 160、40、60 份。网络把每点 3 个坐标变成 32 再变成 64 个特征，逐通道取最大值后，用一个小分类头输出两类分数。训练 80 轮，验证损失最低的是第 64 轮；测试准确率为 58/60，即 0.9667。重新排列测试点的顺序后，输出最大绝对差为 0。

### 完整 Python：几何、体渲染与点云分类

运行 main.py --output output --language zh，或用en生成英文图。脚本使用NumPy、PyTorch、Matplotlib，在CPU训练小型共享逐点网络，并独立渲染已知三维场。保存点云、预测、射线图像与summary.json；不下载权重。

```
"""Camera geometry, volume compositing, and a PointNet-style classifier."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


def clouds(count, seed):
    rng=np.random.default_rng(seed);points=[];labels=np.arange(count)%2
    for label in labels:
        if label==0:
            p=rng.normal(size=(64,3));p/=np.linalg.norm(p,axis=1,keepdims=True)
        else:
            p=rng.uniform(-1,1,(64,3));axes=rng.integers(0,3,64)
            p[np.arange(64),axes]=rng.choice([-1,1],64)
        rotation,_=np.linalg.qr(rng.normal(size=(3,3)))
        p=p@rotation;p-=p.mean(0);p/=np.linalg.norm(p,axis=1).max()
        points.append(p)
    return np.array(points,dtype=np.float32),labels


class PointModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.point=nn.Sequential(nn.Linear(3,32),nn.ReLU(),nn.Linear(32,64),nn.ReLU())
        self.readout=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,2))
    def forward(self,x):
        return self.readout(self.point(x).amax(dim=1))


def scene(points):
    centers=np.array([[-.35,0,0],[.35,.12,.08]])
    sizes=np.array([.23,.19]);colors=np.array([[.82,.25,.18],[.12,.42,.75]])
    components=16*np.exp(-.5*np.square((points[...,None,:]-centers)/sizes[:,None]).sum(-1))
    sigma=components.sum(-1)
    color=(components[...,None]*colors).sum(-2)/(sigma[...,None]+1e-15)
    return sigma,color


def render(angle, samples, resolution=48):
    origin=np.array([2.8*np.cos(angle),1.,2.8*np.sin(angle)])
    forward=-origin/np.linalg.norm(origin)
    right=np.cross(forward,[0,1,0]);right/=np.linalg.norm(right)
    up=np.cross(right,forward)
    q=(np.arange(resolution)+.5-resolution/2)/(resolution/2)
    xx,yy=np.meshgrid(q,-q)
    direction=1.8*forward+xx[...,None]*right+yy[...,None]*up
    direction/=np.linalg.norm(direction,axis=-1,keepdims=True)
    edges=np.linspace(1,5,samples+1);t=(edges[:-1]+edges[1:])/2;delta=np.diff(edges)
    points=origin+direction[:,:,None,:]*t[None,None,:,None]
    sigma,color=scene(points);alpha=-np.expm1(-sigma*delta)
    trans=np.concatenate([np.ones((*alpha.shape[:2],1)),np.cumprod(1-alpha,axis=-1)[...,:-1]],axis=-1)
    weights=trans*alpha;remaining=np.prod(1-alpha,axis=-1)
    rgb=(weights[...,None]*color).sum(-2)+remaining[...,None]
    opacity=weights.sum(-1)
    depth=(weights*t).sum(-1)/(opacity+1e-12)
    conservation=float(np.max(np.abs(opacity+remaining-1)))
    return rgb,depth,opacity,conservation


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def txt(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    torch.manual_seed(14)
    tx,ty=clouds(160,10);vx,vy=clouds(40,20);ex,ey=clouds(60,30)
    tx,ty,vx,vy=map(torch.tensor,[tx,ty,vx,vy]);model=PointModel()
    optimizer=torch.optim.Adam(model.parameters(),lr=.003);history=[];best=float('inf')
    for epoch in range(80):
        model.train();losses=[]
        for ids in torch.randperm(160).split(20):
            optimizer.zero_grad();loss=nn.functional.cross_entropy(model(tx[ids]),ty[ids])
            loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad():val=nn.functional.cross_entropy(model(vx),vy).item()
        history.append([np.mean(losses),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    with torch.no_grad():
        test=torch.tensor(ex);logits=model(test);prediction=logits.argmax(1).numpy()
        permutation=torch.tensor(np.random.default_rng(17).permutation(64))
        permutation_error=float((model(test[:,permutation])-logits).abs().max())
    angles=[0,.8,1.6];renders=[render(a,96) for a in angles]
    reference=render(.8,256)[0];sample_counts=[8,16,32,64,96]
    errors=[float(np.sqrt(np.mean((render(.8,n)[0]-reference)**2))) for n in sample_counts]
    conservation=max(r[3] for r in renders)
    focal,baseline,depth=800.,.12,3.
    disparity=focal*baseline/depth
    recovered=focal*baseline/disparity
    # Front-to-back red and blue layers, both with opacity one half.
    red=np.array([1.,0,0]);blue=np.array([0.,0,1]);white=np.ones(3)
    red_first=.5*red+.5*.5*blue+.25*white
    blue_first=.5*blue+.5*.5*red+.25*white
    summary={'test_pointclouds':60,'test_accuracy':float(np.mean(prediction==ey)),
             'permutation_max_error':permutation_error,'selected_epoch':int(np.argmin(np.array(history)[:,1])+1),
             'compositing_conservation_error':conservation,'stereo_disparity_px':disparity,
             'recovered_depth_m':recovered,'sample_counts':sample_counts,'rgb_rmse_to_256_samples':errors,
             'red_front_rgb':red_first.tolist(),'blue_front_rgb':blue_first.tolist()}
    assert permutation_error<1e-6 and conservation<1e-12
    assert abs(recovered-3)<1e-12
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',test_clouds=ex,test_labels=ey,prediction=prediction,history=history,
             view_rgb=np.array([r[0] for r in renders]),view_depth=np.array([r[1] for r in renders]),
             view_opacity=np.array([r[2] for r in renders]),samples=sample_counts,rmse=errors)
    fig=plt.figure(figsize=(12,4.3));gs=fig.add_gridspec(1,3,width_ratios=[1.1,1,1])
    ax=fig.add_subplot(gs[0]);zs=np.linspace(.8,8,150);ds=focal*baseline/zs
    ax.plot(zs,ds,color='#176b91');ax.scatter([3],[32],color='#bb554d',zorder=3)
    ax.annotate('3 m → 32 px',(3,32),xytext=(3.4,65),arrowprops={'arrowstyle':'->'})
    ax.set(xlabel=txt('深度 / m','Depth / m'),ylabel=txt('视差 / px','Disparity / px'),title=txt('固定焦距800 px，基线0.12 m','Focal length 800 px; baseline 0.12 m'))
    for k in range(2):
        ax=fig.add_subplot(gs[k+1],projection='3d');p=ex[k]
        ax.scatter(*p.T,c=p[:,2],cmap='viridis',s=15,vmin=-1,vmax=1)
        ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1),xlabel='x',ylabel='y',zlabel='z',title=txt(['球面点集','立方体表面点集'][k],['Sphere points','Cube-surface points'][k]))
        ax.set_box_aspect((1,1,1));ax.view_init(22,35)
        ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_zticks([-1,0,1])
    fig.tight_layout();save(fig,'geometry')
    fig,axs=plt.subplots(2,3,figsize=(12,7))
    for j,angle in enumerate(angles):
        rgb,dep,opacity,_=renders[j]
        axs[0,j].imshow(rgb);axs[0,j].set_title(txt(f'相机方位 {angle:.1f} rad',f'Camera azimuth {angle:.1f} rad'))
        masked=np.ma.masked_where(opacity<.05,dep)
        im=axs[1,j].imshow(masked,cmap='viridis',vmin=2,vmax=4)
        axs[1,j].set_title(txt('条件加权射线距离 / 单位长度','Conditional ray distance / length units'))
        for i in range(2):axs[i,j].set_xticks([]);axs[i,j].set_yticks([])
    fig.colorbar(im,ax=axs[1,:],shrink=.65,label=txt('射线距离','Ray distance'))
    save(fig,'views')
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,3,width_ratios=[1.3,1,1])
    ax=fig.add_subplot(gs[:,0]);hist=np.array(history)
    ax.plot(np.arange(1,81),hist[:,0],label=txt('训练','Training'),color='#176b91')
    ax.plot(np.arange(1,81),hist[:,1],label=txt('验证','Validation'),color='#bb554d')
    ax.set(xlabel=txt('轮数','Epoch'),ylabel=txt('交叉熵','Cross-entropy'),title=txt('共享逐点网络与最大值读出','Shared point network and max readout'));ax.legend()
    ax=fig.add_subplot(gs[0,1]);conf=np.zeros((2,2),int)
    for y,p in zip(ey,prediction):conf[y,p]+=1
    ax.imshow(conf,cmap='Blues',vmin=0,vmax=30)
    for i in range(2):
        for j in range(2):ax.text(j,i,str(conf[i,j]),ha='center',va='center',color='white' if conf[i,j]>15 else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xlabel=txt('预测类别','Predicted class'),ylabel=txt('真实类别','True class'))
    ax=fig.add_subplot(gs[1,1]);ax.semilogy(sample_counts,errors,'o-',color='#176b91')
    ax.set(xlabel=txt('每射线采样数','Samples per ray'),ylabel='RGB RMSE',title=txt('对照256采样','Reference: 256 samples'))
    ax=fig.add_subplot(gs[0,2]);ax.imshow(np.tile(red_first,(30,30,1)));ax.set_title(txt('红在前，蓝在后','Red in front of blue'));ax.axis('off')
    ax=fig.add_subplot(gs[1,2]);ax.imshow(np.tile(blue_first,(30,30,1)));ax.set_title(txt('蓝在前，红在后','Blue in front of red'));ax.axis('off')
    fig.tight_layout();save(fig,'results')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

代码同时保存体渲染和点云分类的数据。渲染中每射线使用 8、16、32、64、96 个中点采样，与 256 个采样的结果比较，RGB 均方根差从约 0.00558 降到 0.0000175。所有射线上的颜色权重加剩余背景透射率，与 1 的最大差约为 1.55×10⁻¹⁵。点云图展示的是模型真实输入，混淆矩阵展示 60 份测试点云的结果，颜色块则把前后顺序改变时的两层合成算例单独画出。它们分别检查学习效果、数值积分和遮挡逻辑。

![左：共享逐点网络的训练与验证交叉熵；中上：60份测试点云的混淆矩阵，类别0球面、1立方体；中下：射线采样与256采样参考的RGB均方根差；右：两层透明度均0.5、白背景时，红蓝顺序改变得到的RGB色块](https://ml-biomat.com/static/tutorials/machine-learning/figures/fbef665715974bcbf9ffa70f.svg?v=fbef66571597)

图 3左：共享逐点网络的训练与验证交叉熵；中上：60份测试点云的混淆矩阵，类别0球面、1立方体；中下：射线采样与256采样参考的RGB均方根差；右：两层透明度均0.5、白背景时，红蓝顺序改变得到的RGB色块。

最大值读出还带来一个可手算的特点：重复加入一个已经存在的点，不会改变任何通道的最大值。这个性质适合把输入看作形状采样，而不适合直接从重复点数量推断物体质量。若点的数量本身携带信息，求和或额外计数特征可能更合适。最大值的各通道也可能由少量不同点贡献，因此可以记录这些贡献点在空间中的位置，观察模型依赖的轮廓区域。这样的可视化比只画一个分类概率，更接近网络究竟从点云中读取了什么。

## 8. 让模型回答几何问题，也回答观测覆盖的问题

三维任务的评价需要尊重相机与对象的分组。新视角合成应留出相机位置，检查训练视角之间的插值，也检查视角覆盖较弱的位置；同一对象的相近扫描不能随意分到点云训练和测试两侧。几何重建可以比较点到面的距离、法向一致性和已知尺寸；图像合成可以比较像素误差、结构相似性或感知差异。场景尺度是否经过对齐、背景是否参与评分、遮挡和不可见区域如何处理，都直接决定数字的含义。

点云采样还会改变观察到的形状。稀疏点集可能漏掉细腿或孔洞，遮挡会让某一侧完全没有观测，异常远点可能主导最大值通道。除了整体准确率，可以逐渐减少点数、加入少量离群点或裁去一个方向的点，观察错误来自哪一种变化。局部邻域方法和图网络能够进一步利用点与点之间的关系；等变网络则把坐标变换规律直接放入计算中。这些扩展各自处理具体困难，应该围绕采样与任务性质来选择。

可以从本章延伸一个完整的小项目：拍摄带有已知标尺的静态对象，先检查标定与相机覆盖，再恢复稀疏点和姿态，用一部分视图训练场景表示，保留另一些视图评价，同时测量几个已知长度。把相机分布、图像误差和长度误差放在同一报告中，就能判断模型在哪些位置看得清、在哪些位置主要依赖插值。三维学习的价值，体现在这些空间关系能够被计算、检验，并用于下一步的测量或交互。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M14.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

   针孔、内外参和标定。
2. [Structure-from-Motion Revisited](https://demuc.de/papers/schoenberger2016sfm.pdf)

   增量SfM与COLMAP的原始论文。
3. [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934)

   连续辐射场、可微渲染与训练。
4. [Nerfstudio — Nerfacto](https://docs.nerf.studio/nerfology/methods/nerfacto.html)

   射线采样、相机细化与工程管线；原管线图在线阅读。
5. [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)

   高斯基元、各向异性协方差与可见性渲染。
6. [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://arxiv.org/abs/1612.00593)

   共享逐点映射、对称聚合与局部全局表示。
