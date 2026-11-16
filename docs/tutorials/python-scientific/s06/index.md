# 沿着轨迹分析分子的变化

Source: https://ml-biomat.com/tutorials/python-scientific/s06/
Language: zh-CN

用泛素的实际模拟轨迹分开整体转动与内部变化，在结构、时间曲线和残基波动之间逐项核对。

## 分子在动，形状也在变吗

把一团柔软的绳结放进水里，它可以整体漂走，也可以一边转动、一边让末端摆动。两张照片里同一个点的位置相差很大，并不一定意味着绳结被拉开了。分析蛋白质的分子动力学轨迹时，我们也会遇到这个问题：原子坐标一直变化，其中有多少来自整条分子的移动，有多少来自内部形状的调整？本节用 MDAnalysis 读取一段泛素轨迹，把这两类变化拆开，画出整体结构差异、分子尺寸和各残基的波动。完成后，你能从一串坐标文件得到有明确对象、单位、参考和时间范围的分析结果。

蛋白质是由氨基酸残基连接而成的长链。“残基”指一个氨基酸进入链以后保留下来的结构单元，每个通常都有一个叫作 Cα 的骨架碳原子。把相邻残基的 Cα 连起来，就得到一条简化链迹，适合观察骨架怎样弯曲；氨基酸侧链、氢原子和周围水分子则包含更多局部细节。本例的泛素有 76 个残基，模型中蛋白质共有 1231 个原子。我们用 76 个 Cα 比较形状，用全部蛋白质原子的质量计算尺寸。这两种选择回答的问题不同，后面的图会一直保留它们的名称。

这种从结构转向运动的提问有很具体的历史背景。1977 年，McCammon、Gelin 和 Karplus 研究牛胰蛋白酶抑制剂 BPTI，把经验势能给出的原子受力接入运动方程，讨论平均结构周围的波动。一个已经折叠的蛋白质仍然具有丰富的内部运动，因而一张结构图需要和一段随时间变化的坐标记录配合阅读。下面的图用本例泛素的实际轨迹呈现这个问题：灰色第一帧保持不动，蓝色链迹在相同视角下变化，橙色点标出末端 Gly76。下方再把两个位置的运动变成带单位的曲线，使“看起来在动”变成可以比较的量。

![1977年BPTI研究把折叠结构中的原子波动作为计算对象。图中使用本例泛素的配准后轨迹来观察同类问题：相同尺度的三个时刻，以及Gly76和Ile23到自身全窗口平均位置的距离；这些距离均由三维坐标计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0f8825838981170aac40d7da.svg?v=0f8825838981)

图 11977年BPTI研究把折叠结构中的原子波动作为计算对象。图中使用本例泛素的配准后轨迹来观察同类问题：相同尺度的三个时刻，以及Gly76和Ile23到自身全窗口平均位置的距离；这些距离均由三维坐标计算。

这里的动画帧来自经典分子动力学计算。原子的位置由指定分子模型和数值积分产生，和显微镜逐帧拍摄有不同的数据身份。起始蛋白质来自 PDB 1UBQ，使用 AMBER99SB-ILDN 蛋白质参数、TIP3P 水、各 17 个钠离子与氯离子，温度和压力控制目标分别为 300 K 与 1 bar。分析关注这一模型在 0–1000 ps 内的构象变化；如果研究目标转为成键反应、质子转移或很慢的构象转换，需要在模型和时间尺度上重新作相应安排。

## 先把原子身份和时间放进同一个对象

一个轨迹文件最重要的内容，是每一帧按同样顺序排列的原子坐标；它往往没有足够的信息告诉你每个原子叫什么、属于哪个残基、质量是多少。拓扑文件负责补充这张身份表。MDAnalysis 的 `Universe` 把两者接在一起：`reference.tpr` 提供原子身份、质量和连接信息，`ubiquitin-5ps.xtc` 提供随时间变化的坐标与模拟盒。本例虽然沿用了 TPR 的文件名，形状比较的参考明确选轨迹第一帧，不使用 TPR 中保存的最小化坐标。一个文件能同时包含多类信息，计算时仍要说清到底取了哪一部分。

整套体系有 18869 个原子，其中包括蛋白质、水和离子。`u.select_atoms('protein')` 返回一个 `AtomGroup`，可以把它理解为沿着身份表选中的一组行；`'protein and name CA'` 再把范围缩到蛋白质内名为 CA 的原子。这里的 CA 是 Cα 原子名称，选区中的 protein 条件还说明它属于蛋白质。原子组保留与原轨迹的对应关系，所以切换帧以后，这些原子的坐标也会更新。程序检查总原子数、蛋白质原子数、Cα 数和残基编号，确认后才开始比较。

把 `u.trajectory[20]` 理解为“把读取位置转到第 21 张照片”会很直观。数组从 0 开始编号，本例第 20 号帧对应 100 ps。`for ts in u.trajectory` 则依次改变这个读取位置，`ts.time` 给出当前帧的物理时间。保存坐标时使用 `.copy()`，让数组成为这一时刻独立的一份数值；否则，围绕当前帧管理数据的阅读器可能在后续读取中更新底层缓冲区。遍历完成后阅读器也可能回到第一帧，因此需要长期保留的时间和值应在循环内明确收集。

长度与时间要在入口处统一。MDAnalysis 默认把本例坐标读成 Å，1 Å 等于 0.1 nm；程序在进入分析数组时除以 10，所有图中的长度都用 nm。时间读成 ps，1000 ps 等于 1 ns。本例从原先每 1 ps 保存的轨迹中每隔 5 帧取一帧，保留 0、5、10，一直到 1000 ps，共 201 帧。生成动力学时的积分步长是 0.002 ps，也就是 2 fs；保存间隔 5 ps 对应 2500 个积分步。只保留这些照片并没有把模拟的积分步长改成 5 ps，却让更快的运动无法从这份子集中恢复。研究振动频率时要另外准备时间分辨率相称的输出。

轨迹还经过完整分子重建和蛋白质居中处理。周期性边界可以想象为一块向各方向重复铺开的空间：从一边离开的原子，在相邻的等价盒子里仍属于同一个分子。若直接把跨边界的原子当成彼此相隔一个盒长，分子尺寸和结构拟合都会出问题。本例输入已经把蛋白质连回完整形状；换用自己的轨迹时，应先根据盒向量和分子连接重建完整分子，再做下面的几何分析。把一个分子画完整、追踪它穿过许多盒子的扩散，以及移除整体旋转，是不同的操作，要按研究问题选择。

## 让同一个分子在同一把尺子下比较

如果拿两张透明薄膜分别描出分子的骨架，直接重叠时可能到处错开。先把它们的中心移到一起，再转动其中一张，通常能让大部分骨架靠得更近。计算机中的刚体配准做的就是这个动作，只是它处理三维坐标，而且把“尽量靠近”写成一个明确的最小化目标。刚体二字意味着同一帧里所有原子接受同一次平移和旋转，原子之间的距离保持不变；程序不会为了追求较小误差而把某个残基单独拉向参考。

本节固定用 76 个 Cα、相同的原子顺序和相等的权重，把每一帧配准到第一帧。对坐标先求三个方向各自的平均，得到几何中心；减掉这个中心即可移除平移。再求使平方偏差总和最小的三维旋转。你可以把平方偏差理解为各个配对点之间距离的平方：距离越大的点，对目标的贡献越大。这里用几何中心，是因为每个 Cα 贡献相同；以后选择质量加权拟合时，中心和误差中的权重也必须一起改成质量对应的定义。

完整代码调用 `AlignTraj` 实际执行配准。为了把数据关系看得清楚，它先用 `Merge(ca)` 建立只含这 76 个原子的对象，再用 `load_new` 接入形状为“201 帧 × 76 原子 × 3 坐标”的数组。参考对象保存第一帧坐标，移动对象保存所有帧。这样只需要在内存中处理骨架；水和离子的坐标仍留在原轨迹里，计算全蛋白质尺寸时仍能使用完整身份和质量。

配准的实际效果要同时看数字和结构。1000 ps 时，未配准的 Cα 均方根偏差为 0.362319 nm；只移除平移后是 0.345529 nm；进一步移除整体旋转后为 0.107340 nm。它们由同一批原子、同一个时刻和同一个参考得到。三者的差别说明，直接坐标差异中有相当一部分来自整体朝向。配准后的剩余差异则保留了这组 Cα 相对第一帧的形状变化。若蛋白质由两个相对转动的结构域组成，选择全蛋白质还是一个结构域作为拟合区，会改变观察内部运动的坐标系，需要与研究目标保持一致。

![三种坐标处理共享第一帧与76个Cα。下左为1231个蛋白质原子的质量加权Rg；下右灰色为第一帧，橙色为1000 ps未配准链迹，蓝色为同一帧配准后链迹。坐标轴为固定三维坐标系的x、z投影。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f365017ae4634f27175aec70.svg?v=f365017ae463)

图 2三种坐标处理共享第一帧与76个Cα。下左为1231个蛋白质原子的质量加权Rg；下右灰色为第一帧，橙色为1000 ps未配准链迹，蓝色为同一帧配准后链迹。坐标轴为固定三维坐标系的x、z投影。

## 一个结构差异数值是怎样算出来的

RMSD 是 root mean square deviation 的缩写，中文常称均方根偏差。三个英文词已经给出运算顺序：先把每对对应原子的距离平方，再对原子求平均，最后开平方。平方避免正负方向互相抵消，平均让不同数量的原子有一致的计量口径，开平方把结果从面积单位还原为长度单位。这里“对应”十分重要：第一个数组的第 15 个 Cα 必须和参考的同一个残基比较，原子数相等而顺序不同仍会得到错误的结构差异。

$$
\operatorname{RMSD}(t)=\sqrt{\frac{1}{N}\sum_{i=1}^{N}\left\|\widetilde{\mathbf r}_i(t)-\mathbf r_i^{\mathrm{ref}}\right\|^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c28bb395211208bbd75d07f3.svg) | 时刻 t 的均方根结构偏差，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 所选帧的时间，ps |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 参与比较的原子数；本例为 76，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 按相同顺序配对的原子编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/53ed5a9277e7e49f9cb02e14.svg) | 按指定方法处理后，第 i 个 Cα 的三维坐标向量，nm；可选未配准、去平移或刚体拟合 |
| ![Formula](https://ml-biomat.com/static/agent-math/7d91d2ea07ecd57330855b66.svg) | 第一帧中对应 Cα 的参考坐标，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/2ee49bcacdf21c726bb6de10.svg) | 向量三个分量的平方和；这里单位为 nm² |
| ![Formula](https://ml-biomat.com/static/agent-math/c1a69b9e26498e8da33b4b57.svg) | 把 1 到 N 号原子的平方距离相加 |

以两个配对点的教学算例说明运算：若处理后两个点到各自参考点的距离分别为 0.1 和 0.3 nm，平方平均为 (0.01+0.09)/2=0.05 nm²，开根号得到 0.223607 nm。这里权重相等。实际轨迹有 76 个 Cα，1000 ps 刚体拟合后得到 0.107340 nm；对三种坐标版本分别代入同一式子，就得到三条 RMSD 曲线。

公式中的坐标可以是原始坐标，也可以是去平移或完成刚体拟合以后的坐标，只要把处理方法说清。图中三条曲线共享纵轴，是为了直接比较这三种定义。在整个 201 帧子集上，未配准 RMSD 的平均为 0.506850 nm，配准后的平均为 0.147892 nm。平均值把一段曲线压缩成一个数，方便报告这一窗口的总体尺度；时间曲线则保留了变化发生的顺序。例如大约 650–700 ps 的拟合 RMSD 高于前面不少时段，读者可以回到对应帧观察是哪些区域发生了位置调整。

RMSD 不是一个普遍的“好坏分数”。它相对于选定参考测量几何差异：改用另一帧、另一组原子或另一种权重，回答的问题也随之改变。一个末端的大幅移动可能抬高全蛋白质 RMSD，而较小的局部变化也可能对结合口袋很重要。因此解释曲线时应接着看残基位置和具体距离。若要判断某种状态被充分采样，可以比较多个时间窗、独立轨迹和与研究问题直接相关的观测量；曲线出现一段平坦区域，说明的是这一几何指标在该时段内变化较小。

示例还用 NumPy 的奇异值分解独立求一次最佳旋转，与 MDAnalysis 的 QCP 计算比较。两条路线分别组织矩阵分解和旋转求解，但采用同样的配对点与相等权重。本次全部帧的两种 RMSD 最大差约为 6.7×10⁻¹⁵ nm；把配准后实际存储的单精度坐标再代回公式，最大差约为 4.0×10⁻⁸ nm。后一个量来自坐标表示的精度尺度，比图中 0.1 nm 左右的结构变化小很多。检查相同定义的不同实现，可以帮助定位单位、权重或原子顺序上的错误。

## 回转半径：质量离中心有多远

如果希望知道蛋白质整体是否变得更松散，可以计算回转半径 Rg。想象把分子各处的质量按离中心的距离排列：质量越多、距离越远，对 Rg 的贡献就越大。它使用全部蛋白质原子的质量，并先求质量中心。一个氧原子和一个氢原子在相同距离处的贡献不同，这与前面让每个 Cα 等权参与拟合的定义形成了清楚的区别。质量不是画图时随手附上的属性，而是这项物理量所需要的输入。

$$
M=\sum_{i=1}^{N_p}m_i,\qquad \mathbf r_{\mathrm{cm}}=\frac{\sum_{i=1}^{N_p}m_i\mathbf r_i}{M},\qquad R_g=\sqrt{\frac{\sum_{i=1}^{N_p}m_i\|\mathbf r_i-\mathbf r_{\mathrm{cm}}\|^2}{M}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 所选蛋白质原子的总质量，u |
| ![Formula](https://ml-biomat.com/static/agent-math/5a9c1aa4dbcfe2c2217b3e46.svg) | 全部蛋白质原子数，本例为 1231，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 蛋白质原子编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/929c2a5e3b92ad47814e45bb.svg) | 第 i 个原子的质量，u；本例读取 TPR |
| ![Formula](https://ml-biomat.com/static/agent-math/1dd29f54f8cb4b9a864140cf.svg) | 当前帧第 i 个原子的坐标向量，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/fe1efa6a514c38eeec0bd835.svg) | 当前帧蛋白质质量中心的坐标，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/742acc50d5d386b6c8461bed.svg) | 质量加权回转半径，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/de714f948b8aa66300ec4bd3.svg) | 三维向量各分量平方之和，nm² |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对所选的全部蛋白质原子求和 |

取一维教学例子：两个质点质量为 1 u 和 3 u，位置为 0 nm 和 2 nm。总质量 4 u，质量中心为 (1×0+3×2)/4=1.5 nm。加权平方距离为 [1×(0−1.5)²+3×(2−1.5)²]/4=0.75 nm²，所以 Rg=0.866025 nm。将两点一起平移或旋转不改变此值。实际数据用 1231 个原子在三维中做同样运算，第一帧为 1.180766 nm。

这 201 帧的平均 Rg 为 1.190952 nm，第一帧为 1.180766 nm。图中 Rg 曲线的纵轴放大了约 1.18–1.21 nm 的变化范围，便于观察分子的尺寸调整；看图时应读刻度，不能把曲线在面板里的高度直接理解为分子膨胀了几倍。Rg 是所有质量到质量中心距离的均方根，不是最远原子距离，也不是把蛋白质包起来的球半径。一个细长结构和一个较均匀的团块可以具有接近的 Rg，所以形状判断还需要结构图或其他方向性指标。

平移和旋转不会改变 Rg。把所有原子一起平移时，质量中心平移相同距离，相对位置保持不变；一起旋转时，到中心的距离保持不变。因而本节直接在完整蛋白质的每一帧上计算 Rg，无需先执行 Cα 配准。这也是检查程序的一个好机会：对同一个分子施加任意刚体变换后，算得的 Rg 应在数值精度范围内相同。与之相对，如果周期性边界把分子分成两块，它们的普通坐标距离可能改变，这时就需要先恢复分子的完整几何。

代码里的 `protein.radius_of_gyration()` 使用 TPR 拓扑提供的质量。它后面紧接一个独立计算：取出所有蛋白质坐标，以质量加权求中心，再平均平方距离并开根号。两者在每一帧上相符，最大差小于 10⁻¹⁵ nm。拓扑中的蛋白质总质量约为 8564.922 u，u 是原子质量单位；在 Rg 的分子和分母中，质量单位相消，最终只留下 nm。将来改用 PDB 等不一定保存全部质量信息的格式时，先确认元素与质量的赋值，再使用这一物理量。

## 沿着残基编号找出局部活动

RMSD 的横轴是时间，每一帧把许多原子的差异汇总起来。RMSF 则把问题转过来：固定一个原子，看它在一段时间里围绕自己的平均位置怎样波动。F 来自 fluctuation，即波动。每个残基得到一个数以后，横轴就变成残基编号，能够比较骨架不同位置的活动幅度。求平均位置以前先对齐各帧，可以减少整条分子转动对局部活动的混入。本节用拟合后的 RMSF 比较局部活动：所有帧采用相同的第一帧配准规则，再在所选窗口内部重新计算每个 Cα 的平均位置。图和交互中还保留未配准与去平移两组结果，便于观察整体运动对坐标波动的贡献。每一组都使用自身坐标在当前窗口内的平均位置。

$$
\overline{\mathbf r}_i=\frac{1}{K}\sum_{k=1}^{K}\widetilde{\mathbf r}_i(t_k),\qquad \operatorname{RMSF}_i=\sqrt{\frac{1}{K}\sum_{k=1}^{K}\|\widetilde{\mathbf r}_i(t_k)-\overline{\mathbf r}_i\|^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 选定 Cα 原子的编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 当前统计窗口内的保存帧数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 窗口中第几个保存帧，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c9b48d61e70baede492433d.svg) | 第 k 个保存帧的时间，ps |
| ![Formula](https://ml-biomat.com/static/agent-math/2af86cc6a230c44cc20e877d.svg) | 采用指定坐标处理后的 Cα 位置，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1de2e76d7a6a0433c4e77.svg) | 该原子在所选时间窗内的平均坐标，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/b8ef4d276aebf957b6e970a4.svg) | 该原子相对自身窗口平均位置的均方根波动，nm |
| ![Formula](https://ml-biomat.com/static/agent-math/de714f948b8aa66300ec4bd3.svg) | 三维坐标差的分量平方和，nm² |
| ![Formula](https://ml-biomat.com/static/agent-math/0dfcceb73a3665cd8b838c11.svg) | 把所选窗口中所有帧的量相加 |

设一个点在三个保存时刻的一维位置为 0、0.2、0.4 nm，另外两维都为零。平均位置为 0.2 nm，三个平方偏差为 0.04、0、0.04 nm²，所以 RMSF=√(0.08/3)=0.163299 nm。三维数据先加总三个方向的平方偏差，再按帧平均。实际 Gly76 在 201 帧全窗口的拟合后 RMSF 为 0.487722 nm；在 41 帧的 0–200 ps 窗口中为 0.313331 nm，使用的是该短窗口自己的平均位置。

算式中的平均对象是平方距离，因此 RMSF 不等于把到平均位置的距离直接求平均，也不等于把整条 RMSD 时间曲线平均一下。前者仍在比较同一个原子随时间的变化，后者已经先把许多原子混在同一个数中。RMSF 使用窗口内的帧数作为分母，是在描述这些记录围绕其平均位置的波动幅度；它不是均值的标准误。轨迹相邻帧通常相关，如果需要给长期平均量估计统计不确定性，还要处理这种时间相关性，而不是把 201 张连续照片当成 201 次独立实验。

![配准规则固定后，三个时间窗产生各自的平均位置和RMSF；图例括号内为帧数。下左比较全窗口未配准与配准结果。右侧平均链迹按全窗口拟合后RMSF着色，色标范围0–0.55 nm。](https://ml-biomat.com/static/tutorials/python-scientific/figures/b7573871091ff9dff2de9f38.svg?v=b7573871091f)

图 3配准规则固定后，三个时间窗产生各自的平均位置和RMSF；图例括号内为帧数。下左比较全窗口未配准与配准结果。右侧平均链迹按全窗口拟合后RMSF着色，色标范围0–0.55 nm。

图中末端 Gly76 在全窗口的拟合后 RMSF 为 0.487722 nm，高于大部分内部残基。把窗口改为 0–200 ps，它变成 0.313331 nm；改为 800–1000 ps，则是 0.396427 nm。两个短窗口都包含两端点，因而各有 41 帧。窗口改变以后，参与计算的坐标和平均位置都改变了；全窗口还可能包含不同时间段平均位置之间的移动。因此不能把两个短窗口的 RMSF 简单平均，就期待得到全窗口值。这个例子也说明，“第 76 位的波动是多少”需要同时附上配准方法、采样间隔和统计时间窗。

右侧结构图将全窗口 RMSF 映射为颜色，并使用全窗口的平均坐标描出骨架。它便于定位峰值属于末端还是内部区域；平均坐标是一种统计表达，可能没有任何单帧恰好取到这个形状。下方交互可以随时切回实际帧，把平均量和真实构象对应起来。若从晶体结构里读到 B 因子，也应先保留它的实验含义：晶体精修中的位置分布与无序、模型因素等共同影响该参数；这里的 RMSF 则来自指定分子模型和有限时间段的轨迹统计，两者需要在适当模型下建立比较关系。

## 完整程序：从读取到结果表和组图

下载包包含程序、拓扑和 201 帧轨迹子集。安装 MDAnalysis、NumPy 与 Matplotlib 后，在解压目录运行下面的命令；`--output` 指定结果目录，`--language` 决定图中文字。输入文件由脚本相对位置定位，因此把整个目录移动到另一台电脑时仍能找到它们。结果包括按时间排列的 `timeseries.csv`、按窗口与残基排列的 `rmsf.csv`、数值摘要和三幅组图。CSV 中列名直接保留 nm、ps，便于接到 pandas 后继续分组或与其他轨迹比较。

### 安装与运行

在解压后的示例目录运行；中文图需要系统中安装 Noto Sans CJK SC、Noto Sans SC、Microsoft YaHei 或 SimHei 字体之一。

```
python -m pip install MDAnalysis numpy matplotlib
python main.py --output results --language en
python main.py --output results-zh --language zh
```

`analyze` 负责科学计算，`plot_figures` 读取同一份结果绘图。前者先逐帧收集 Cα 坐标与全蛋白质 Rg，再建立三个坐标版本，随后在三个时间窗里调用 `RMSF`。`rms.RMSF` 本身不会替你配准，所以拟合后的数组先进入新的内存轨迹，再计算波动。每个步骤的输出在下一步都有明确用途：坐标用于拟合和结构图，时间用于窗口筛选，RMSF 数组同时用于曲线和结构颜色。这样更换绘图风格不会改变科学定义。

### 完整轨迹分析与绘图程序

读取实际 TPR/XTC，运行配准、回转半径和三个窗口的 RMSF，保存表格、数值摘要与三幅组图。

```
"""Read a real ubiquitin trajectory; separate rigid-body motion and fluctuations."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import align, rms
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.collections import LineCollection

BLUE, ORANGE, GREEN = '#176480', '#bd5b28', '#2e8071'
MODES = ('raw', 'centered', 'fitted')
WINDOWS = {'all': (0, 1000), 'early': (0, 200), 'late': (800, 1000)}


def available_plot_fonts():
    choices = ['Noto Sans CJK SC', 'Noto Sans SC', 'Microsoft YaHei',
               'SimHei', 'DejaVu Sans']
    installed = {f.name for f in font_manager.fontManager.ttflist}
    return [x for x in choices if x in installed]


def rigid_fit_svd(mobile, reference):
    """Independent equal-weight proper rotation, using row-vector coordinates."""
    x = mobile - mobile.mean(axis=0)
    y = reference - reference.mean(axis=0)
    left, _, right = np.linalg.svd(x.T @ y)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(left @ right)
    fitted = x @ (left @ correction @ right) + reference.mean(axis=0)
    return fitted


def analyze(output):
    source = Path(__file__).resolve().parent / 'data'
    # XTC readers save an offset index next to the trajectory. Keep it in output.
    cache = output / 'trajectory-cache'
    cache.mkdir(exist_ok=True)
    trajectory = cache / 'ubiquitin-5ps.xtc'
    shutil.copyfile(source / trajectory.name, trajectory)
    u = mda.Universe(str(source / 'reference.tpr'), str(trajectory))
    protein = u.select_atoms('protein')
    ca = u.select_atoms('protein and name CA')
    assert len(u.atoms) == 18869 and len(protein) == 1231 and len(ca) == 76
    assert np.array_equal(ca.resids, np.arange(1, 77))
    times, coordinates, rg, rg_direct = [], [], [], []
    masses = protein.masses.astype(float)
    for ts in u.trajectory:
        times.append(float(ts.time))
        coordinates.append(ca.positions.astype(float).copy() / 10)
        rg.append(float(protein.radius_of_gyration()) / 10)
        xyz = protein.positions.astype(float) / 10
        com = np.average(xyz, axis=0, weights=masses)
        rg_direct.append(float(np.sqrt(np.average(
            np.sum((xyz - com) ** 2, axis=1), weights=masses))))
    times = np.asarray(times)
    raw = np.asarray(coordinates)
    assert np.allclose(times, np.arange(201) * 5, atol=1e-6)
    reference = raw[0]
    centered = raw - raw.mean(axis=1, keepdims=True) + reference.mean(axis=0)
    # A small in-memory Universe has the same 76 atom identities and 201 frames.
    mobile = mda.Merge(ca)
    mobile.load_new((raw * 10).astype(np.float32), order='fac', dt=5)
    ref = mda.Merge(ca)
    ref.atoms.positions = reference * 10
    align.AlignTraj(mobile, ref, select='all', weights=None,
                    in_memory=True).run()
    fitted = np.array([mobile.atoms.positions.copy().astype(float) / 10
                       for _ in mobile.trajectory])
    xyz_by_mode = {'raw': raw, 'centered': centered, 'fitted': fitted}
    rmsd = {key: np.sqrt(np.mean(np.sum((a-reference)**2, axis=2), axis=1))
            for key, a in xyz_by_mode.items()}
    qcp = np.array([rms.rmsd(x, reference, center=True, superposition=True)
                    for x in raw])
    independent = np.array([rigid_fit_svd(x, reference) for x in raw])
    svd_rmsd = np.sqrt(np.mean(np.sum((independent-reference)**2, axis=2), axis=1))
    # The exact identity frame can give a tiny QCP roundoff, so compare at 1e-6 nm.
    assert np.max(np.abs(qcp-svd_rmsd)) < 1e-6
    assert np.max(np.abs(rmsd['fitted']-svd_rmsd)) < 1e-6
    assert np.max(np.abs(np.array(rg)-rg_direct)) < 1e-12
    windows, rmsf_error = {}, []
    for key, (start, end) in WINDOWS.items():
        indices = np.flatnonzero((times >= start) & (times <= end))
        record = {'start_ps': start, 'end_ps': end, 'frames': len(indices),
                  'rmsf_nm': {}, 'mean_nm': {}, 'rg_mean_nm': float(np.mean(np.array(rg)[indices]))}
        for mode, xyz in xyz_by_mode.items():
            mem = mda.Merge(ca)
            mem.load_new((xyz*10).astype(np.float32), order='fac', dt=5)
            result = rms.RMSF(mem.atoms).run(start=int(indices[0]), stop=int(indices[-1])+1)
            fluct = result.results.rmsf / 10
            direct = np.sqrt(np.mean(np.sum((xyz[indices]-xyz[indices].mean(axis=0))**2,
                                           axis=2), axis=0))
            rmsf_error.append(float(np.max(np.abs(fluct-direct))))
            record['rmsf_nm'][mode] = fluct.tolist()
            record['mean_nm'][mode] = xyz[indices].mean(axis=0).tolist()
        windows[key] = record
    assert max(rmsf_error) < 1e-6
    summary = {
        'frames': len(times), 'atoms': len(u.atoms), 'protein_atoms': len(protein),
        'CA_atoms': len(ca), 'sampling_ps': 5, 'duration_ps': float(times[-1]-times[0]),
        'protein_mass_u': float(masses.sum()),
        'rg_mean_nm': float(np.mean(rg)), 'rg_first_nm': rg[0],
        'rmsd_last_nm': {key: float(v[-1]) for key,v in rmsd.items()},
        'rmsd_mean_nm': {key: float(np.mean(v)) for key,v in rmsd.items()},
        'rmsf_76_nm': {key: value['rmsf_nm']['fitted'][75] for key,value in windows.items()},
        'rmsf_peak_residue': int(np.argmax(windows['all']['rmsf_nm']['fitted'])+1),
        'checks': {'QCP_SVD_max_nm': float(np.max(np.abs(qcp-svd_rmsd))),
                   'AlignTraj_SVD_max_nm': float(np.max(np.abs(rmsd['fitted']-svd_rmsd))),
                   'Rg_max_nm': float(np.max(np.abs(np.array(rg)-rg_direct))),
                   'RMSF_max_nm': max(rmsf_error)},
        'versions': {'MDAnalysis': mda.__version__, 'numpy': np.__version__,
                     'matplotlib': matplotlib.__version__},
        'input_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (source/'reference.tpr', source/'ubiquitin-5ps.xtc')}
    }
    lab = {'times_ps': times.tolist(), 'resids': ca.resids.tolist(),
           'resnames': ca.resnames.tolist(), 'xyz_nm': {k:v.tolist() for k,v in xyz_by_mode.items()},
           'rmsd_nm': {k:v.tolist() for k,v in rmsd.items()}, 'rg_nm': rg,
           'windows': windows, 'reference_nm': reference.tolist()}
    for name, obj in [('summary',summary),('lab-data',lab)]:
        (output/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    with (output/'timeseries.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['time_ps','RMSD_raw_nm','RMSD_centered_nm','RMSD_fitted_nm','Rg_nm'])
        w.writerows(zip(times,*[rmsd[k] for k in MODES],rg))
    with (output/'rmsf.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['window','mode','resid','resname','RMSF_nm'])
        for window, record in windows.items():
            for mode in MODES:
                w.writerows((window,mode,int(i),str(n),float(v)) for i,n,v in
                            zip(ca.resids,ca.resnames,record['rmsf_nm'][mode]))
    return lab, summary


def plot_figures(d, summary, output, language):
    zh = language == 'zh'
    def t(a,b): return a if zh else b
    plt.rcParams.update({'font.family':available_plot_fonts() if zh else ['DejaVu Sans'],
        'font.size':13,'axes.titlesize':16,'axes.labelsize':13,'xtick.labelsize':12,
        'ytick.labelsize':12,'axes.spines.top':False,'axes.spines.right':False,
        'svg.fonttype':'none','figure.facecolor':'#fffefb','axes.facecolor':'#fffefb'})
    time=np.array(d['times_ps']); ref=np.array(d['reference_nm']); ref-=ref.mean(axis=0)
    raw=np.array(d['xyz_nm']['raw']); fit=np.array(d['xyz_nm']['fitted'])
    labels=[t('未配准','Unfitted'),t('去平移','Translation removed'),t('去平移与旋转','Rigid-body fitted')]
    colors=[ORANGE,'#887494',BLUE]
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight')
        fig.savefig(output/f'{name}-{language}.png',dpi=150,bbox_inches='tight'); plt.close(fig)
    def clean(ax): ax.grid(alpha=.16); ax.set_axisbelow(True)
    fig=plt.figure(figsize=(14,8.5),layout='constrained')
    grid=fig.add_gridspec(2,2,height_ratios=[1.3,1])
    a=fig.add_subplot(grid[0,:]); b=fig.add_subplot(grid[1,0]); c=fig.add_subplot(grid[1,1])
    for mode,label,color in zip(MODES,labels,colors): a.plot(time,d['rmsd_nm'][mode],color=color,lw=1.8,label=label)
    a.set(xlabel=t('时间 / ps','Time / ps'),ylabel=t('Cα RMSD / nm','Cα RMSD / nm'),
          title=t('A  同一个第一帧参考，三种坐标处理','A  One first-frame reference, three coordinate treatments'))
    a.legend(loc='upper left',ncol=3,fontsize=12); a.set_ylim(bottom=0); clean(a)
    b.plot(time,d['rg_nm'],color=GREEN,lw=1.5); b.set(xlabel=t('时间 / ps','Time / ps'),ylabel='Rg / nm',
          title=t('B  1231个蛋白质原子的质量分布','B  Mass distribution of 1231 protein atoms')); clean(b)
    c.plot(ref[:,0],ref[:,2],color='#a6acaf',lw=2,label=t('第一帧','First frame'))
    for arr,color,label in [(raw[-1]-np.array(d['reference_nm']).mean(axis=0),ORANGE,t('1000 ps：未配准','1000 ps: unfitted')),
                             (fit[-1]-np.array(d['reference_nm']).mean(axis=0),BLUE,t('1000 ps：配准后','1000 ps: fitted'))]:
        c.plot(arr[:,0],arr[:,2],color=color,lw=1.5,alpha=.85,label=label)
    c.set(xlabel='x / nm',ylabel='z / nm',title=t('C  固定视角的Cα链迹','C  Cα traces in one fixed projection'))
    c.set_aspect('equal'); clean(c)
    save(fig,'global-motion')
    fig=plt.figure(figsize=(14,9),layout='constrained'); g=fig.add_gridspec(2,2,width_ratios=[1.25,1])
    a=fig.add_subplot(g[0,0]); b=fig.add_subplot(g[1,0]); c=fig.add_subplot(g[:,1]); res=np.arange(1,77)
    for key,col in [('all',BLUE),('early',GREEN),('late',ORANGE)]:
        r=d['windows'][key]; a.plot(res,r['rmsf_nm']['fitted'],lw=2,color=col,label=f"{r['start_ps']}–{r['end_ps']} ps ({r['frames']})")
    a.set(title=t('A  固定配准后，时间窗决定平均位置','A  A fixed alignment, different averaging windows'),xlabel=t('残基编号','Residue number'),ylabel='Cα RMSF / nm'); a.legend(fontsize=11);clean(a)
    for mode,col,label in [('raw',ORANGE,labels[0]),('fitted',BLUE,labels[2])]:
        b.plot(res,d['windows']['all']['rmsf_nm'][mode],color=col,lw=2,label=label)
    b.set(title=t('B  0–1000 ps：整体转动也会增大坐标波动','B  Global rotation also enlarges positional fluctuations'),xlabel=t('残基编号','Residue number'),ylabel='Cα RMSF / nm');b.legend(fontsize=11);clean(b)
    mean=np.array(d['windows']['all']['mean_nm']['fitted']); mean-=mean.mean(axis=0)
    fluct=np.array(d['windows']['all']['rmsf_nm']['fitted']); pts=mean[:,[0,2]]
    lc=LineCollection(np.stack([pts[:-1],pts[1:]],axis=1),cmap='viridis',norm=plt.Normalize(0,.55),linewidth=4)
    lc.set_array((fluct[:-1]+fluct[1:])/2); c.add_collection(lc);c.scatter(pts[:,0],pts[:,1],c=fluct,cmap='viridis',vmin=0,vmax=.55,s=24,zorder=3)
    for i,offset in [(0,(-20,-24)),(75,(8,8))]: c.annotate(f'{i+1} {d["resnames"][i]}',pts[i],xytext=offset,textcoords='offset points',fontsize=12)
    c.annotate('9 THR',pts[8],xytext=(1.05,1.15),textcoords='data',fontsize=12,
               arrowprops={'arrowstyle':'-','color':'#666'},bbox={'facecolor':'#fffefb','edgecolor':'none','pad':2})
    c.autoscale(); c.margins(.2);c.set_aspect('equal');c.set(xlabel='x / nm',ylabel='z / nm',title=t('C  全窗口平均构象及局部波动','C  Full-window mean and local fluctuations'))
    fig.colorbar(lc,ax=c,orientation='horizontal',pad=.09,label='Cα RMSF / nm',ticks=[0,.1,.2,.3,.4,.5]);clean(c)
    save(fig,'local-fluctuations')
    fig=plt.figure(figsize=(14,8.5),layout='constrained');g=fig.add_gridspec(2,3,height_ratios=[1.4,1])
    for j,frame in enumerate([0,100,200]):
        ax=fig.add_subplot(g[0,j]);p=fit[frame]-np.array(d['reference_nm']).mean(axis=0)
        ax.plot(ref[:,0],ref[:,2],color='#b5b8b9',lw=2,label=t('0 ps','0 ps'))
        ax.plot(p[:,0],p[:,2],color=BLUE,lw=2);ax.scatter(*p[75,[0,2]],color=ORANGE,s=65,zorder=4)
        ax.annotate('Gly76',p[75,[0,2]],xytext=(8,6),textcoords='offset points',fontsize=12)
        ax.set(xlabel='x / nm',ylabel='z / nm',title=f'{time[frame]:.0f} ps',xlim=(-2.2,2.2),ylim=(-2,2.8));ax.set_aspect('equal');clean(ax)
    a=fig.add_subplot(g[1,:2]); mean=np.array(d['windows']['all']['mean_nm']['fitted'])
    for idx,col in [(22,BLUE),(75,ORANGE)]:
        a.plot(time,np.linalg.norm(fit[:,idx]-mean[idx],axis=1),color=col,lw=1.7,label=f'{d["resnames"][idx]}{idx+1}')
    a.set(xlabel=t('时间 / ps','Time / ps'),ylabel=t('距自身平均位置 / nm','Distance from own mean / nm'),title=t('局部波动：相同时间里，两个位置怎样移动','Local fluctuations at two positions over the same time'));a.legend(ncol=2,fontsize=12);clean(a)
    b=fig.add_subplot(g[1,2]); b.axis('off')
    b.text(0,1,t('从折叠结构到原子运动','From folded structure\nto atomic motion'),va='top',fontsize=17,color=BLUE)
    b.text(0,.70,t('1977 · McCammon、Gelin、Karplus\nBPTI的经验势能与运动方程\n追踪平均结构周围的波动。\n\n上方：本例泛素的201帧子集\n灰色参考保持不动，\n橙色端点显示Gly76的位置。',
        '1977 · McCammon, Gelin, Karplus\nAn empirical potential and equations\nof motion for BPTI revealed\nfluctuations about an average.\n\nAbove: the present ubiquitin subset\nThe gray reference stays fixed;\norange tracks the position of Gly76.'),va='top',fontsize=13,linespacing=1.6)
    save(fig,'fluctuation-history')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('results'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    data,summary=analyze(args.output)
    plot_figures(data,summary,args.output,args.language)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
```

程序把 XTC 复制到结果目录中的缓存位置再读取，因为轨迹阅读器会在旁边保存帧偏移索引，以便快速跳转。分析结果和索引都留在输出目录，输入数据可以保持原样。运行结束时打印的摘要可以与图中的具体数值对照，例如 201 帧、76 个 Cα 和末帧拟合 RMSD。独立检查分别使用 SVD 配准、直接质量加权距离和先求均值再求偏差的两遍 RMSF 计算；这些检查针对数学定义，帮助发现数据排列和单位转换问题。

处理更大体系时，可以先逐帧计算不需要整段坐标的量，例如 Rg 和指定距离，把表格逐行写出。只有在需要反复操作完整坐标集合时才加载内存。本例的 Cα 数组很小，保留全部 201 帧便于教学和交互；全体系的水和离子没有必要随之复制成多套内存数组。面对另一个蛋白质，首先更新数据身份、原子选择和编号检查，再决定拟合区与时间窗，原有计算函数则可以继续使用。

## 沿着同一帧，在结构和曲线之间来回查看

下面的实验把时间帧、坐标处理和 RMSF 时间窗分开控制。移动时间滑块时，结构、RMSD 与 Rg 上的游标、所选残基的位置同步更新；切换坐标处理时，可以看到同一帧整体朝向的变化以及 RMSD 数值的变化；切换窗口时，残基曲线、结构颜色和局部距离曲线一起更新。灰色链迹固定为第一帧，结构视图可以转动，但转动视角只改变投影，所有数值仍使用三维坐标。

### 轨迹、配准与时间窗

比较同一时刻的三种坐标处理，再把一个残基的波动追踪到结构里。播放从当前帧逐步推进，可随时暂停；进入页面时保持静止。

[Figure: 当前帧结构与所选残基轨迹](https://ml-biomat.com/tutorials/python-scientific/s06/#S06-structure)

灰色为第一帧；链颜色为当前窗口RMSF。橙点为当前残基，橙色细线为它在窗口中的轨迹。u、v是正交投影坐标，单位nm。

[Figure: 三种RMSD与Rg时间曲线](https://ml-biomat.com/tutorials/python-scientific/s06/#S06-times)

当前坐标处理用粗线，游标标记同一帧；淡绿色为RMSF统计窗口。Rg使用全部蛋白质原子质量，保持相同。

[Figure: 逐残基RMSF与选择位置](https://ml-biomat.com/tutorials/python-scientific/s06/#S06-fluctuation)

橙色位置与结构里的同一个Cα对应；切换时间窗同时改变曲线、结构颜色与窗口平均位置。

[Figure: 所选残基到窗口平均位置的距离](https://ml-biomat.com/tutorials/python-scientific/s06/#S06-local)

曲线保留全部时刻，绿色区域内的帧参与当前RMSF计算；距离来自三维坐标。

可以先选择 1000 ps，依次查看未配准、去平移和刚体拟合，确认 Rg 保持相同，再观察末端位置和 RMSD 的差异。接着保留刚体拟合，选择第 76 位并切换三个时间窗：彩色链段提示这个位置在统计图中的含义，局部曲线显示它到当前窗口平均位置的三维距离。最后改选第 23 位，比较末端和内部位置的运动尺度。所有视图共享 Python 实际算出的坐标与统计量，页面在本地切换这些结果；保存的轨迹和完整程序可以重新生成它们。把观察落到具体原子、时间、参考和单位上，轨迹中的变化就能成为下一步研究可以继续追问的问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [MDAnalysis: trajectories](https://userguide.mdanalysis.org/stable/trajectories/trajectories.html)

   Universe、动态坐标、帧迭代与坐标副本。

   MDAnalysis User Guide repository: LGPL-2.1; methodological reference.
2. [MDAnalysis: RMSF tutorial](https://userguide.mdanalysis.org/stable/examples/analysis/alignment_and_rms/rmsf.html)

   先配准再计算RMSF的官方示例。

   MDAnalysis User Guide repository: LGPL-2.1; methodological reference.
3. [MDAnalysis 2.11: RMS quantities](https://docs.mdanalysis.org/stable/documentation_pages/analysis/rms.html)

   RMSD、RMSF、权重与结果属性。

   MDAnalysis package LGPL-3.0-or-later; component terms retained.
4. [MDAnalysis 2.11: alignment](https://docs.mdanalysis.org/stable/documentation_pages/analysis/align.html)

   AlignTraj与内存轨迹的坐标处理。

   MDAnalysis package LGPL-3.0-or-later; API reference.
5. [MDAnalysis 2.11: atom groups](https://docs.mdanalysis.org/stable/documentation_pages/core/groups.html)

   原子选择、质量中心与回转半径。

   MDAnalysis package LGPL-3.0-or-later; API reference.
6. [McCammon, Gelin & Karplus (1977), Dynamics of folded proteins](https://doi.org/10.1038/267585a0)

   BPTI中平均结构周围原子运动的历史研究。

   Primary scientific reference; publisher copyright.
7. [PDB 1UBQ: ubiquitin](https://www.rcsb.org/structure/1UBQ)

   轨迹起始蛋白质的公开结构身份。

   PDB archive data: CC0 1.0; https://www.rcsb.org/pages/policies
8. [Vijay-Kumar, Bugg & Cook (1987), Structure of ubiquitin refined at 1.8 Å resolution](https://doi.org/10.1016/0022-2836%2887%2990679-6)

   1UBQ的原始结构研究。

   Primary scientific reference; publisher copyright.
9. [GROMACS introductory tutorial](https://tutorials.gromacs.org/docs/md-intro-tutorial.html)

   模拟准备、动力学与后处理的开放操作背景。

   Public tutorial; consult its stated terms for reuse.
10. [MDAnalysis licensing](https://github.com/MDAnalysis/mdanalysis/blob/develop/LICENSE)

    软件包与组件许可。

    LGPL-3.0-or-later package; component licenses as listed.
