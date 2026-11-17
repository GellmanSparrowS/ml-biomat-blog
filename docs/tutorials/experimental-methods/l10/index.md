# 划痕与Transwell：细胞怎样移动并穿过屏障

Source: https://ml-biomat.com/tutorials/experimental-methods/l10/
Language: zh-CN

把闭合面积、细胞轨迹、梯度与跨膜数量连起来，读懂迁移、铺展和增殖各自留下的证据。

## 一条空隙变窄，细胞究竟做了什么

皮肤受损后，周围细胞会重新排列、移动和增殖，逐步覆盖暴露区域。研究一种敷料或材料表面时，我们也会关心它是否有利于细胞进入空缺处。把长满细胞的平面中央留出一条空隙，再用显微镜连续拍摄，就能看见两侧细胞怎样接近。这个实验通常称为划痕或伤口愈合实验，图像直观，问题却可以问得很细：边缘前进得多快，细胞是否保持彼此连接，还是个别细胞先走进空隙，分裂与铺展分别发生在什么时候？

另一个常见问题是细胞能否穿过一个屏障。例如，免疫细胞是否会向某种可溶性信号聚集，或者细胞能否通过一层基质。Transwell把细胞与待测试环境放在多孔膜的两侧，最后统计通过膜的细胞。它像把一条平面道路换成带门的隔间：细胞既要能移动，还要到达孔口、通过孔道，并在被计数的位置留下来。这个结果与平面空隙闭合互相补充，因为它们包含不同的几何约束和观测终点。

两个实验都适合研究材料与细胞的相互作用，但先把“迁移”拆成可观察的行为会更容易理解。细胞把前缘伸出去、在表面建立黏附、牵引身体向前，再释放后方的连接。细胞骨架与黏附结构在这个过程中不断变化；周围细胞、基质排列和可溶信号又会影响方向。显微镜看到的覆盖面积由这些移动加上细胞形状和数量变化共同形成。我们因此从空隙、细胞轨迹和跨膜计数三个层次记录信息，让每个数值回答一个明确问题。

本节的完整例子会从构造显微像素分割空隙，计算闭合率，再追踪两组速度相同、方向分布不同的细胞，并检查跨膜实验的分母。真实开放论文图则让读者看到细胞边缘、形态和分裂带来的复杂变化。所有构造数据都有清楚设定的几何或运动条件，便于逐步核算。学习的重点是把一张“看上去闭合得更好”的图，转成有时间、空间、样品和行为定义的实验结果。

## 把移动放进一个可比较的装置

1962年Boyden发表了一种研究可溶性物质如何吸引白细胞的装置：两个室由滤膜隔开，一侧放细胞，另一侧放待测试溶液。这样的设计让化学环境与通过膜的细胞数量建立联系，也给不同溶液提供了可比较的几何条件。原始工作还通过改变抗体、抗原与血清的组合，追问真正产生吸引作用的成分。这段历史值得关注的地方，是把“细胞朝某处聚集”的现象分解成可操作的条件，而不是把观察到的移动直接归因于溶液中的某一个名字。

现代插入式培养装置沿用了两室与多孔膜的关系，结构、孔径和读出方式更加多样。膜上可以不加基质层，用于研究通过孔道的迁移；也可以覆盖一定组成的细胞外基质，使结果包含穿过基质与孔道的能力。细胞外基质是细胞周围提供支撑、黏附位置和信号的材料集合，体外涂层把其中一部分条件引入实验。把涂层组成、厚度、批次和孔径写进结果，能够说明细胞实际上面对了怎样的障碍。

![原创几何示意：平面细胞层与现代两室插入件；右图连接Boyden1962年的滤膜两室思路，并非历史装置复刻。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/569a99dd0517838ef746a758.svg?v=569a99dd0517)

图 1原创几何示意：平面细胞层与现代两室插入件；右图连接Boyden1962年的滤膜两室思路，并非历史装置复刻。

平面划痕实验把另一类几何条件固定下来：原先彼此接触的细胞层突然出现可进入的空间。边缘细胞获得了新的自由边界，附近细胞也可能改变排列与分裂。2004年Yarrow及合作者把这类实验扩展到多孔板，并比较不同成像方式能够读出什么信息。他们的真实图像同时展示正常闭合、迁移受影响、形态改变和分裂细胞增加，说明一张图里并不只有一条空隙宽度。实验向高通量发展时，保留能区分这些行为的信息，仍然是读图的核心。

形成空隙的方法会改变问题的起点。机械划过细胞层会移除细胞，也可能损伤底部涂层并留下碎片；使用可移除隔挡则可以在细胞长好后露出预留区域，减少刮擦带来的表面变化。两者对应不同的边缘状态，不能仅凭初始宽度相同就视为完全相同的刺激。研究材料表面时尤其要看划痕是否同时刮掉了目标涂层，否则细胞面对的可能是裸露基底。把起始图与表面情况保存下来，就给后面的闭合曲线提供了可解释的起点。

## 从像素面积到闭合速度，分母先讲清楚

划痕图像的第一步通常是划定尚未被细胞覆盖的区域。图像处理中，这个区域可以表示为一个只有“属于空隙”与“不属于空隙”两种值的掩膜。统计其中像素数，再乘每个像素代表的面积，就得到物理面积。这里容易漏掉一个平方：若像素边长为2微米，一个像素覆盖4平方微米，而不是2平方微米。相机与物镜组合决定这一标定，图片显示得更大并不会改变原始像素对应的真实长度。

$$
A=n_p s_xs_y
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 分割空隙面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/4773c6daf0d996bad65e1235.svg) | 空隙内像素数量，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/45e9f2faccf8bb8a3297984f.svg) | 每个像素横、纵向边长，μm |

每个像素面积是横边乘纵边，总面积再乘像素数。60000像素、横纵边均2μm，面积240000μm²。空间标定来自实际采集设置；本例像素为正方形。

每个视野先记录自己的初始空隙面积，再比较后续剩余面积，得到闭合百分比。比如初始面积为240000平方微米，24小时后剩96000平方微米，已覆盖的部分为144000，闭合60%。这个百分比把不同视野的面积尺度归一化，但并没有消除起始形状的全部影响。宽200微米与宽800微米的两条空隙，即使边缘以同样速度前进，相同时间内闭合百分比仍会不同。保留初始面积和宽度分布，能够解释这些几何差异。

$$
C(t)=100\%\,\frac{A_0-A(t)}{A_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4e857df82e09ece3691e350.svg) | 时刻t的空隙闭合率，% |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从起始图像计算的时间，h |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 同一视野起始空隙面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/fb60620bc9b2f7378081e24b.svg) | 时刻t剩余空隙面积，μm² |

先取减少的面积，再除以自己的初始面积。240000减96000等于144000，除240000得到60%。初始与后续图像需对应同一视野和一致的空隙定义。

当空隙近似是一条长矩形，两边以相似速度向内前进，可以从宽度变化估计单侧边缘的平均速度。为什么要除以2？因为总宽度的减少来自左、右两边共同推进。初始宽400微米，24小时后宽160微米，左右总共推进240微米；每边平均推进120微米，再除24小时，得到5微米每小时。这个速度描述细胞层边缘，而一个细胞的轨迹可能弯曲、停顿或横向移动，两者具有不同的测量对象。

$$
v_{\rm edge}=\frac{w_0-w_t}{2t}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/457582f1a6cb86d77424cc8c.svg) | 单侧边缘平均推进速度，μm/h |
| ![Formula](https://ml-biomat.com/static/agent-math/9aa2b69e898db5e9d56207e0.svg) | 起始平均空隙宽度，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/49296f174f7d0afdfa8fd6c8.svg) | 时刻t平均空隙宽度，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 观察时间，h |

适用于近似平行且两侧相似推进的边界。两侧各贡献一半宽度减少；400降至160μm用24h，单边速度240/(2×24)=5μm/h。边界速度与单个细胞路径速度分开定义。

实际划痕常常弯曲且宽窄不一。可以在沿空隙方向的一系列位置测局部宽度，或者在固定视野内直接统计面积；选择取决于边缘形状与研究问题。一个伸入空隙的细长突起会明显改变某处最窄宽度，却只占很小面积；几颗孤立细胞可能先进入中央，又没有形成连续覆盖。读者应在掩膜上看到这些对象如何处理：是否把突起算进边界、孤立细胞是否扣去、碎片如何识别。定义清楚后，同一规则贯穿所有条件与时间点。

![代码实际输出的构造图像与分割轮廓，像素2μm；下方比较闭合真值、初始宽度与阈值敏感性。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4ff4c06e514fa47b00d813c5.svg?v=4ff4c06e514f)

图 2代码实际输出的构造图像与分割轮廓，像素2μm；下方比较闭合真值、初始宽度与阈值敏感性。

本节图像为已知几何构造：每像素2微米，视野高600微米，初始空隙平均宽400微米，两边各以5微米每小时推进。程序对带纹理和噪声的图像平滑后分割，再保留最大的相连空隙区域，输出轮廓叠加图和闭合曲线。阈值敏感性图显示，把判断亮暗的界限略作改变会怎样影响结果。真实相差不大的两组，如果结论随着合理的小幅边界调整反复变号，就应优先检查分割定义和成像条件，再增加数值的小数位。

## 同样闭合60%，可能经历不同的细胞过程

细胞层覆盖空隙可以通过多条路径发生。原有细胞向中央迁移，细胞身体铺展开占据更大面积，附近细胞分裂后增加覆盖者，都能让未覆盖面积变小。想把这些贡献分开，可以在同一时间序列中观察细胞核位置、细胞轮廓和分裂事件。核位置方便追踪身体的大致移动，轮廓显示铺展，分裂事件说明数量变化；三个读数结合起来，就能解释为什么同一闭合曲线背后会出现不同的细胞行为。

选择观察窗口也有作用。较短窗口中能够直接追踪起始细胞的移动；较长窗口可能让更多分裂、死亡和脱落累积进结果。缩短时间并不自动排除增殖，需要看这类细胞在当前条件下何时发生分裂。降低血清或使用抑制增殖的处理会改变细胞环境，也可能改变迁移、黏附和存活，因此相关对照应同时记录这些行为。把增殖标记、细胞计数与时间序列接到同一问题上，能把“为了控制某个过程而采取的处理”本身也纳入测量。

另一个常见混淆来自细胞数量。两组起始细胞层如果密度不同，边缘可供参与的细胞数、彼此接触状态和营养条件都会变化。比较材料时，黏附效率不同可能在正式划痕之前就造成这些差异。先确认起始汇合程度和活细胞数量，再解释后续移动，可以区分材料帮助细胞留在表面与帮助细胞移动的作用。汇合是细胞覆盖表面的程度，不等同于所有细胞具有相同的状态；时间零的图像是这一差别的直接记录。

## 交互实验：同样闭合，不同细胞移动

改变初始宽度、时间、原有细胞移动速度与额外覆盖前缘速度。空隙边缘由两种速度相加推进；箭头只跟随原有细胞移动。额外覆盖是铺展或新增覆盖的示意速度，不是细胞分裂速率。

[Figure: 空隙几何、细胞移动与闭合曲线](https://ml-biomat.com/tutorials/experimental-methods/l10/#L10-lab)

交互实验用一个明确的几何模型展示信息缺口。单侧前缘推进分为“原有细胞移动”与“铺展或新增细胞带来的额外覆盖”两部分，单位都是微米每小时。它们相加决定空隙缩小，但图中跟随原有细胞的箭头只由移动速度决定。把5加0改成2加3，24小时的闭合率保持60%，箭头却变短。额外覆盖参数是一个示意性的前缘速度，不是细胞分裂速率；它让我们看清，需要再增加哪一种观测，才能区分两种相同面积结果。

## 穿过多孔膜：信号、孔道和计数位置

Transwell的上室放入一定数量的细胞，下室放入待测试溶液，两侧通过多孔膜交换可溶性物质。所谓浓度梯度，就是位置不同，信号浓度不同；细胞可能根据这种空间差异偏向某个方向移动。开始时下室较浓，不代表整个观察期间梯度都保持不变。扩散会重新分配分子，细胞会消耗或释放信号，膜和涂层还可能吸附它们。两室体积、接触面积、时间和分子性质共同决定细胞实际经历的环境。

图中的两室交换模型把这个过程先简化为两杯充分混匀的液体。上室0.1毫升起初没有信号，下室0.6毫升起初为10纳克每毫升，总量为6纳克。交换会让两侧浓度接近总量除总体积，约8.571纳克每毫升。程序记录每个时刻的上、下室浓度，并检查总体质量始终为6纳克。这里的曲线用于解释梯度会随时间改变，真实装置中靠近膜的局部浓度需要由对应几何、传质条件或实测示踪建立。

如果下室加入信号后通过的细胞变多，可以进一步设置上下室都没有信号、上下室相同浓度、只有下室以及只有上室有信号等条件。均匀信号可能让细胞整体更活跃，却没有同样的方向梯度；方向偏向梯度的现象称为趋化，非定向的运动活跃程度改变常称为趋动。比较这些条件，把方向作用与速度或活性作用逐步分开。细胞还能沿固定在表面的配体差异移动，那涉及表面信息，应与溶液中的浓度梯度分别设计。

两室交换速度在模型中用导通系数g表示：浓度差乘g，给出单位时间转移的质量。上室因此增加，下室同时减少；同一份转移质量在小体积中造成的浓度变化更大，所以两室体积都进入浓度差的衰减速度。设g为0.02毫升每小时，下面的关系给出3小时后的浓度差约4.966纳克每毫升。这个参数属于本节构造模型，真实膜的值需要由实际传质测量建立。

$$
\Delta c(t)=\Delta c_0\exp\!\left[-g\left(\frac{1}{V_u}+\frac{1}{V_l}\right)t\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6f8ef384ada27708b9205032.svg) | 下室减上室的体积平均浓度差，ng/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/d3f36c525113c3e9bd33a306.svg) | 起始浓度差，ng/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | 两室交换导通系数，mL/h |
| ![Formula](https://ml-biomat.com/static/agent-math/424f1a1571bd30409c6a3740.svg) | 上、下室体积，mL |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 交换时间，h |

两室充分混匀、体积恒定，无额外产生或损失，并假设转移速率为g乘浓度差。两室相反的质量变化使差值按指数衰减。g=0.02、Vu=0.1、Vl=0.6、初始差10时，3h后差10exp(−0.7)约4.966ng/mL；指数无量纲。

![构造的两室体积平均浓度与跨膜计数。每点为一个独立插入件，橙线为3个计数的均值；所有条件输入50000活细胞。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b519f155fdddab8a72f0c474.svg?v=b519f155fddd)

图 3构造的两室体积平均浓度与跨膜计数。每点为一个独立插入件，橙线为3个计数的均值；所有条件输入50000活细胞。

孔径也在参与筛选。孔太小，细胞与细胞核的变形可能成为主要障碍；孔太大，重力沉降和非主动穿过会改变读数。上样细胞过多则可能遮挡孔口或在表面形成拥挤层。检查合适的细胞数、时间和孔径范围，比照搬某个细胞系的参数更有意义。培养时是否出现膜下气泡、两室液面和体积是否一致，也会改变接触与流动条件。对材料涂层的研究还需确认涂层覆盖均匀，避免把局部缺口造成的易通过路径解释为整体材料作用。

终点计数必须说明数的是哪里。贴壁细胞通过后可能停在膜的下表面，需要清除上表面尚未通过的细胞，再观察下表面；非贴壁细胞则可能进入下室液体。只数下表面或只数下室，回答的都是一个明确位置的回收数量。若按接种活细胞数作分母，600个通过细胞除以50000个输入细胞，得到1.2%。若比较相同条件的涂层与未涂层膜，180除以600得到30%，这描述涂层相对于基线迁移的通过比例，两种百分比的分母不同。

$$
P_{\rm input}=100\%\frac{N_{\rm crossed}}{N_{\rm input}},\qquad P_{\rm coating}=100\%\frac{\overline N_{\rm coated}}{\overline N_{\rm uncoated}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/455d2073f7b2c579e45d7588.svg) | 通过细胞占输入活细胞的比例，% |
| ![Formula](https://ml-biomat.com/static/agent-math/88d4394861a8d67deaa914e2.svg) | 按规定回收位置统计的通过细胞数 |
| ![Formula](https://ml-biomat.com/static/agent-math/05257314088d7512596a9f14.svg) | 接种活细胞数 |
| ![Formula](https://ml-biomat.com/static/agent-math/7a63829e7be0525729a1c9d4.svg) | 涂层相对未涂层的通过比例，% |
| ![Formula](https://ml-biomat.com/static/agent-math/7a5c20b532080055cc6f5c74.svg) | 匹配条件下独立涂层与未涂层插入件平均通过数 |

输入归一化：600/50000=1.2%。涂层相对通过：180/600=30%。两种分母分别代表进入实验的活细胞与无额外涂层时的迁移基线；体积、时间、孔径与计数位置匹配。

## 走得快、走得直与朝同一方向，是三件事

时间序列可以为每个细胞建立一串位置坐标。相邻两帧之间的直线距离相加，得到记录到的路径长度；再除总时间，得到平均路径速度。起点到终点的直线距离称为净位移长度，它忽略了途中绕路。就像人在公园走了一圈，计步路线很长，回到出发点后净位移却接近零。把路径长度与净位移同时保留，能区分移动活跃而不断改变方向的细胞，与持续朝一个方向前进的细胞。

$$
L=\sum_{j=1}^{m}\sqrt{(x_j-x_{j-1})^2+(y_j-y_{j-1})^2},\qquad v=L/(t_m-t_0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 相邻采样点连线的总路径，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 相邻位置段的编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 位置段数量，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/96477b2fe2e7ddc7328f97cc.svg) | 第j个位置坐标，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 记录轨迹的平均路径速度，μm/h |
| ![Formula](https://ml-biomat.com/static/agent-math/af01f97a1ec46052fc2a4305.svg) | 末次与首次采样时刻，h |

每段用勾股定理求长度，再相加。坐标(0,0)、(3,4)、(6,4)的两段为5和3μm，路径8μm；历时2h，速度4μm/h。采样间隔改变会改变记录到的弯曲细节。

用净位移长度除路径长度，得到轨迹直线性，取值在0到1之间。一条一直朝左的直线轨迹与一直朝右的直线轨迹都接近1，因此直线性本身没有告诉我们细胞朝哪边走。若把预期梯度方向定义为正x轴，可以把净位移投影到x方向，再除路径长度，得到有正负的前向迁移指数。正值表示沿梯度方向净前进，负值表示相反方向，接近零则表示在该方向上没有明显净推进。

$$
D=\frac{\sqrt{(x_m-x_0)^2+(y_m-y_0)^2}}{L},\qquad \mathrm{FMI}_x=\frac{x_m-x_0}{L}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 轨迹直线性，无量纲，0至1 |
| ![Formula](https://ml-biomat.com/static/agent-math/eb985d0dd107c86347098e80.svg) | 沿预定正x方向的前向迁移指数，无量纲，−1至1 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c267702472a95afa49a186f.svg) | 轨迹终点坐标，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/640d1781cec644e3d742caf9.svg) | 轨迹起点坐标，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 同一轨迹的总路径长度，μm，需大于0 |

净位移长度除路径给直线性；x位移除路径保留方向符号。前例净位移√52，D约0.901，FMIx=6/8=0.75。静止轨迹路径为0时单独记录静止，不对零作除法。

考虑三个位置，起点为零，第一小时到达横向3、纵向4微米，第二小时到达横向6、纵向4微米。第一段距离由勾股定理得到5，第二段为3，总路径8微米，平均速度4微米每小时；净位移为根号52，约7.211微米，直线性约0.901，沿x的前向指数是6除8，等于0.75。每个数字都从同一条轨迹产生，却强调不同特点。对一群细胞，先计算每条轨迹的指标，再查看分布和独立实验之间的变化。

![代码实际输出的20条/组构造轨迹。两组按0.5h采样速度均20μm/h；方向偏向与稀疏采样分别改变不同指标。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d6d53b9024ca11fafcc4f8b9.svg?v=d6d53b9024ca)

图 4代码实际输出的20条/组构造轨迹。两组按0.5h采样速度均20μm/h；方向偏向与稀疏采样分别改变不同指标。

构造例的两组细胞每半小时都走10微米，所以按这个采样间隔计算，平均速度同为20微米每小时。第一组方向均匀变化，第二组方向集中在正x附近，轨迹图和前向指数便明显不同。如果每隔两小时才拍一次，细胞在两次拍摄之间的弯曲路线被一条直线代替，估计路径会缩短；频繁转弯的一组通常受影响更大。图中的采样比较让读者看见，时间分辨率与空间标定一样，都属于速度定义的一部分。

追踪还需要处理视野漂移、细胞分裂和离开画面的情况。可以用固定背景结构校正载物台漂移，否则所有细胞同时移动的假象会进入轨迹；分裂后是终止母细胞轨迹还是转为谱系记录，需要事先确定。只选择一直留在画面中的细胞可能偏向移动较慢者，保留离开视野的记录与适当观察区域有助于判断这种选择。一个实验中的几十条轨迹描述该实验的细胞分布，跨实验重复则提供不同培养与处理批次的稳定性信息。

## 让图像保留足够的生物学信息

下面的真实图显示，划痕实验中的“变化”可以有多种样子。A呈现同一类细胞边缘移动的时间序列，B展示从0到24小时空隙逐步改变，D则并排显示不同表型。边缘是否连续、细胞是否拉长、是否出现大量圆形分裂细胞，都是面积数字之外的线索。读图时先找到原始比例尺和时间，再比较同一尺度下的空间变化，最后才把图像与某一组数值指标对应。这样既保留整体图案，也让定量有可见对象。

![Yarrow等2004年图1，CC BY2.0完整转载。A为BS-C-1时间序列，B为0–24h，D为不同表型；原图比例尺A20μm、B/D100μm、C底部500μm。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7dd7e3fcd0eb95ee8ca22ac0.svg?v=7dd7e3fcd0eb)

图 5Yarrow等2004年图1，CC BY2.0完整转载。A为BS-C-1时间序列，B为0–24h，D为不同表型；原图比例尺A20μm、B/D100μm、C底部500μm。

拍摄时需要在时间点之间返回同一视野，尽量保持焦点、照明和成像参数一致。若一个时间点拍摄中央、另一个时间点拍摄更窄的一端，面积变化会混入位置变化。自动载物台可以保存坐标，人工拍摄也可以使用不会伤害细胞的定位标记与固定取景规则。材料表面的散射、颜色和自发荧光可能改变细胞与空隙的对比，必要时选择适合的成像方式或附加通道。选用更高倍物镜时，还要检查视野是否仍包含足够的完整边界。

跨膜计数同样需要覆盖空间差异。中心与边缘的细胞分布可能不同，预先规定多个位置或扫描整张膜，可以减少只挑密集区域带来的偏差。每个视野是同一插入件中的一部分，先汇总到插入件，再比较独立重复；几个视野不自动成为几个独立实验。细胞聚团时，一个亮斑可能包含多个核，染色强度也可能随处理变化。确定计数对象、保留代表性图像与分割叠加，能够把“数量变化”与“染得更亮”区分开。

研究材料释放物时，可以把条件培养液加入相关室；研究材料接触效应时，则要明确细胞接触的是涂层、薄膜还是浸提后的基底。这两条路线回答不同的问题。若某种处理同时降低活细胞数与通过数，结合起始输入、终点存活和轨迹观察，可以选择进一步研究毒性、黏附或迁移过程。把这些测量安排成围绕同一个生物问题的组合，比只增加一个闭合百分比更能解释材料发挥作用的位置。

## 完整例子：面积、轨迹与跨膜计数一起读

完整程序输出五组图形和可逐项检查的数据。划痕部分保存原始构造图像、真实空隙和实际分割掩膜，并导出逐时刻面积；轨迹部分保存每个细胞的坐标、时刻和组别；跨膜部分保存每张独立构造膜的通过数与输入细胞数，同时输出两室交换的质量平衡。真实发表图单独保留原始标注，便于对照阅读。读者运行后得到的图就是本节展示的计算输出，修改参数可以继续追问几何与测量规则怎样改变结果。

### 完整 Python：图像分割、轨迹与跨膜分母

完整导出图像数组、空隙掩膜、逐细胞轨迹、逐插入件计数、两室质量平衡与双语图。

```
"""Offline constructed scratch, tracking and Transwell examples with a licensed measured figure."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
from scipy.ndimage import gaussian_filter,label
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def metrics(track,dt):
    track=np.asarray(track,dtype=float)
    if track.ndim!=2 or track.shape[1]!=2 or len(track)<2 or not np.isfinite(track).all() or not np.isfinite(dt) or dt<=0:
        raise ValueError('Provide at least two finite x/y positions and a positive sampling interval.')
    length=float(np.linalg.norm(np.diff(track,axis=0),axis=1).sum());displacement=track[-1]-track[0]
    stationary=length==0
    return {'path_um':length,'speed_um_per_h':float(length/((len(track)-1)*dt)),'stationary':stationary,'directness':None if stationary else float(np.linalg.norm(displacement)/length),'fmi_x':None if stationary else float(displacement[0]/length)}

def population_metrics(tracks,dt):
    values=[metrics(track,dt) for track in tracks]
    directional=[value['fmi_x'] for value in values if not value['stationary']]
    return {'mean_fmi_x':float(np.mean(directional)) if directional else None,'mean_speed_um_h':float(np.mean([value['speed_um_per_h'] for value in values])),'stationary_fraction':float(np.mean([value['stationary'] for value in values])),'directional_track_count':len(directional)}
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda a,b:a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(1010);px=2.;yy,xx=np.mgrid[:300,:480];x=xx*px;y=yy*px;center=480+12*np.sin(y/60);times=np.array([0,6,12,18,24]);images=[];masks=[];truth_masks=[];areas=[]
    for t in times:
        width=400-10*t;gap=abs(x-center)<width/2;raw=np.where(gap,30.,120.)+rng.normal(0,5,gap.shape)+8*np.sin(x/13)*np.cos(y/17)*(~gap);raw=gaussian_filter(raw,.7)
        candidate=gaussian_filter(raw,1)<75;labs,n=label(candidate);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=labs==np.argmax(sizes)
        images.append(raw);masks.append(mask);truth_masks.append(gap);areas.append(mask.sum()*px**2)
    areas=np.array(areas);closure=100*(1-areas/areas[0]);np.savez_compressed(out/'scratch_images.npz',time_h=times,image=np.array(images),segmented_gap=np.array(masks),known_gap=np.array(truth_masks),pixel_um=px)
    with(out/'closure.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['time_h','segmented_area_um2','closure_percent','ideal_width_um']);w.writerows(zip(times,areas,closure,400-10*times))
    tracksets={};trackrows=[]
    for name in ['random','directed']:
        tracks=[]
        for j in range(20):
            angle=rng.uniform(-np.pi,np.pi,24)if name=='random'else rng.normal(0,.35,24)
            step=10*np.column_stack([np.cos(angle),np.sin(angle)]);track=np.vstack([np.zeros(2),np.cumsum(step,axis=0)]);tracks.append(track)
            for k,(tx,ty)in enumerate(track):trackrows.append([name,j+1,k*.5,tx,ty])
        tracksets[name]=tracks
    with(out/'tracks.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['group','cell_id','time_h','x_um','y_um']);w.writerows(trackrows)
    counts={'no_cue':[180,200,220],'lower_cue':[540,600,660],'uniform_cue':[360,400,440],'upper_cue':[135,150,165],'coated_lower_cue':[150,180,210]}
    with(out/'transwell_counts.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['condition','independent_insert','whole_membrane_count','input_cells']);w.writerows([k,i+1,v,50000]for k,vals in counts.items()for i,v in enumerate(vals))
    t=np.linspace(0,12,121);vu=.1;vl=.6;k=.02;equilibrium=10*vl/(vu+vl);decay=np.exp(-k*(1/vu+1/vl)*t);cu=equilibrium*(1-decay);cl=equilibrium+(10-equilibrium)*decay
    with(out/'gradient.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['time_h','upper_ng_ml','lower_ng_ml','total_ng']);w.writerows(zip(t,cu,cl,vu*cu+vl*cl))
    fig,ax=plt.subplots(1,2,figsize=(11,5.3))
    for a in ax:a.axis('off');a.set(xlim=(0,10),ylim=(0,7))
    ax[0].add_patch(Rectangle((.5,1.1),9,4,fc=BLUE,alpha=.1));ax[0].add_patch(Rectangle((4,1.1),2,4,fc='#faf9f5'))
    for j in range(4):
        for i in range(3):
            for shift in[0,6]:ax[0].add_patch(Circle((1+i*.8+shift,1.6+j*.9),.28,fc=BLUE,alpha=.7))
    ax[0].annotate('',xy=(4.7,3),xytext=(3.1,3),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[0].annotate('',xy=(5.3,3),xytext=(6.9,3),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[0].text(5,6,T('同一平面：空隙如何闭合','One plane: how a gap closes'),ha='center',fontsize=12);ax[0].text(5,.3,T('迁移、铺展与增殖共同改变覆盖面积','Migration, spreading and division change coverage'),ha='center',fontsize=9)
    ax[1].add_patch(Rectangle((1,1),8,4.7,fill=False,ec=BLUE,lw=2));ax[1].add_patch(Rectangle((2.2,3),5.6,3,fill=False,ec=PURPLE,lw=2));
    for i in range(6):ax[1].plot([2.2+i*.95,2.7+i*.95],[3,3],color=PURPLE,lw=4)
    for xx0 in[3,4.4,6,7]:ax[1].add_patch(Circle((xx0,3.6),.22,fc=BLUE))
    for xx0 in[2,3,4,5,6,7,8]:ax[1].add_patch(Circle((xx0,1.8),.07,fc=AMBER))
    ax[1].annotate('',xy=(5,2.3),xytext=(5,3.6),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[1].text(5,6.6,T('1962 Boyden：用膜连接两个室','1962 Boyden: two compartments and a membrane'),ha='center',fontsize=12);ax[1].text(5,.3,T('现代插入式装置原创示意，非历史原件','Original modern-insert schematic, not the historical apparatus'),ha='center',fontsize=9);fig.tight_layout();save(fig,'history')
    fig,ax=plt.subplots(2,3,figsize=(12,7.7))
    for j,idx in enumerate([0,2,4]):
        a=ax[0,j];a.imshow(images[idx],cmap='gray',vmin=20,vmax=140,extent=[0,960,600,0]);a.contour(x,y,masks[idx],levels=[.5],colors=[AMBER],linewidths=.7);a.set(title=f'{times[idx]} h',xlabel='x / μm',ylabel='y / μm')
    ax[1,0].plot(times,closure,'o-',color=BLUE);ax[1,0].plot(times,100*10*times/400,'--',color=AMBER);ax[1,0].set(xlabel=T('时间 / h','Time / h'),ylabel=T('空隙闭合 / %','Gap closure / %'),title=T('A  分割值与几何真值','A  Segmentation and geometric truth'))
    width=np.linspace(200,800,100);ax[1,1].plot(width,np.minimum(100,100*240/width),color=PURPLE);ax[1,1].set(xlabel=T('初始宽度 / μm','Initial width / μm'),ylabel=T('24小时闭合 / %','Closure at24 h / %'),title=T('B  同一边缘速度，起始宽度不同','B  Same edge speed, different initial widths'))
    th=np.arange(50,101,5);sensitivity=[]
    for q in th:
        aa=[(gaussian_filter(im,1)<q).sum()*px**2 for im in[images[0],images[-1]]];sensitivity.append(100*(1-aa[1]/aa[0]))
    ax[1,2].plot(th,sensitivity,'o-',color=GREEN);ax[1,2].axhline(60,color='gray',ls='--');ax[1,2].set(xlabel=T('分割阈值 / a.u.','Segmentation threshold / a.u.'),ylabel=T('24小时闭合 / %','Closure at24 h / %'),title=T('C  边界判断的敏感性','C  Sensitivity to boundary definition'));fig.tight_layout();save(fig,'scratch')
    fig,ax=plt.subplots(2,2,figsize=(11,8.7))
    for j,name in enumerate(['random','directed']):
        a=ax[0,j]
        for track in tracksets[name]:a.plot(track[:,0],track[:,1],alpha=.6,lw=1.2,color=BLUE if j==0 else AMBER);a.scatter(*track[-1],s=8,color=PURPLE)
        a.set_aspect('equal');a.set(xlim=(-130,260),ylim=(-140,140),xlabel='x / μm',ylabel='y / μm',title=T('A  无偏方向，步长相同','A  Unbiased headings, equal step length')if j==0 else T('B  方向偏向正x，步长仍相同','B  Headings biased toward+x, same steps'));a.axhline(0,color='gray',lw=.5);a.axvline(0,color='gray',lw=.5)
    for j,name in enumerate(['random','directed']):
        ms=[metrics(q,.5)for q in tracksets[name]];ax[1,0].scatter(np.full(20,j),[m['fmi_x']for m in ms],color=BLUE if j==0 else AMBER,alpha=.65)
        for stride,col in[(1,BLUE),(4,AMBER)]:ax[1,1].scatter(j+(.12 if stride==4 else-.12),np.mean([metrics(q[::stride],.5*stride)['speed_um_per_h']for q in tracksets[name]]),color=col,s=60)
    for a in ax[1]:a.set_xticks([0,1],[T('随机方向','Random'),T('定向','Directed')]);a.grid(alpha=.15)
    ax[1,0].set(ylabel=T('沿x前向迁移指数','Forward migration index along x'),title=T('C  方向性由投影位移体现','C  Projected displacement measures bias'))
    ax[1,1].set(ylabel=T('估计平均速度 / μm/h','Estimated mean speed / μm/h'),title=T('D  蓝：0.5h采样；橙：2h采样','D  Blue:0.5h sampling; orange:2h'));fig.tight_layout();save(fig,'tracks')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));ax[0].plot(t,cu,color=BLUE,label=T('上室','Upper'));ax[0].plot(t,cl,color=AMBER,label=T('下室','Lower'));ax[0].set(xlabel=T('时间 / h','Time / h'),ylabel=T('体积平均浓度 / ng/mL','Volume-averaged concentration / ng/mL'),title=T('A  两室交换的构造模型','A  Constructed two-compartment exchange'));ax[0].legend()
    labels=[T('无信号','No cue'),T('下室信号','Lower cue'),T('均匀信号','Uniform cue'),T('上室信号','Upper cue'),T('涂层+下室','Coated+lower')]
    for i,(name,values)in enumerate(counts.items()):ax[1].scatter(np.full(3,i),values,color=BLUE);ax[1].plot([i-.15,i+.15],[np.mean(values)]*2,color=AMBER,lw=3)
    ax[1].set_xticks(range(5),labels,rotation=20,ha='right');ax[1].set(ylabel=T('每张膜通过的细胞数','Crossed cells per membrane'),title=T('B  构造计数：每点是独立插入件','B  Constructed counts: each dot is an insert'))
    for a in ax:a.grid(alpha=.15)
    fig.tight_layout();save(fig,'transwell')
    fig,ax=plt.subplots(figsize=(11,10));ax.imshow(Image.open(Path(__file__).resolve().parent/'yarrow2004-figure1.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实划痕实验：闭合之外还有形态与分裂信息','Measured scratch assay: closure, morphology and division'),fontsize=12);fig.text(.5,.015,T('Yarrow等2004，图1；CC BY2.0，完整转载。\n原图比例尺：A20μm；B、D100μm；C底部500μm。','Yarrow et al.2004,Fig1; CC BY2.0, reproduced in full.\nOriginal scale bars:A20μm;B/D100μm;Cbottom500μm.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.07,1,1]);save(fig,'published')
    simple=metrics(np.array([[0.,0.],[3.,4.],[6.,4.]]),1)
    stationary=metrics(np.zeros((3,2)),1)
    assert stationary['speed_um_per_h']==0 and stationary['directness'] is None and stationary['fmi_x'] is None
    summary={'geometry':{'initial_area_um2':400*600,'final_area_um2':160*600,'closure_percent':60,'one_edge_speed_um_h':(400-160)/(2*24),'equivalent_area_from_60000_pixels_um2':60000*2**2},'tracking':simple,'stationary_tracking':stationary,'stationary_population':population_metrics([np.zeros((3,2))],1),'transwell':{'migration_percent':600/50000*100,'coated_to_uncoated_percent':180/600*100,'initial_total_ng':.6*10,'final_total_ng':float(vu*cu[-1]+vl*cl[-1]),'equilibrium_ng_ml':equilibrium},'segmentation':{'initial_area_um2':float(areas[0]),'final_closure_percent':float(closure[-1])},'populations':{name:population_metrics(tracks,.5) for name,tracks in tracksets.items()}}
    assert abs(closure[-1]-60)<.15
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf8');print(json.dumps(summary,allow_nan=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

可以先把初始空隙宽度加倍，保持边缘速度不变，检查24小时闭合率怎样下降；再改变图像阈值，观察轮廓而不仅是百分比。随后让轨迹采样间隔变大，比较路径速度与净位移变化。最后分别改变跨膜输入量、未涂层通过数和涂层通过数，核对两种分母回答的研究问题。每次保留原始输入和最终计算，就能找出变化来自细胞行为设定、采样几何还是分析规则。

如果目标是评价材料是否支持组织覆盖，可以重点报告起始密度、闭合时间序列、边缘结构以及存活与增殖信息；如果目标是研究趋化，则让方向梯度对照与轨迹方向性进入主线；如果目标是研究穿过基质，则保留涂层定义和配对的未涂层迁移结果。三种问题可以彼此连接，但各自的主要读数应清楚。最终，实验不只是给出“更多”或“更快”，而是展示细胞在怎样的环境与几何条件下，以什么方式改变了位置和覆盖。

闭合曲线接近100%时，还要保留时间信息。两组都在终点完全闭合，可能是一组较早达到，另一组稍晚才赶上。比较多个时间点或明确的到达时间，能保留这种差别；边缘接触以后，原先“两边向内推进”的几何关系也发生变化。若把接触后的平段继续拟合成恒定速度，会把后期无法继续缩窄的几何约束混入速度估计。选择尚未闭合且边界可清楚辨认的区间，并说明拟合对象，可以让曲线与实际图像保持对应。

保存结果时，可以用同一张记录表把培养批次、插入件、视野和细胞轨迹连接起来。三个插入件各拍五个视野，得到十五幅图，实验重复仍首先是三个独立插入件。不同日期独立准备的细胞提供另一层变化；若从同一孔反复拍摄，则数据之间共享起始状态。保留这些层次既便于选择统计模型，也便于回到某个异常图像查清原因。数字越多，越需要清楚它们共享了哪些实验条件。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L10.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Boyden (1962): The chemotactic effect of mixtures of antibody and antigen on polymorphonuclear leucocytes](https://pmc.ncbi.nlm.nih.gov/articles/PMC2137509/)

   滤膜分隔两室的原始研究及变量设计。

   Historical technical reference; original figure not reproduced
2. [Yarrow et al. (2004): A high-throughput cell migration assay using scratch wound healing](https://pmc.ncbi.nlm.nih.gov/articles/PMC521074/)

   真实闭合、形态与分裂图像；不同图像读出比较。

   CC BY 2.0; Fig. 1 reproduced in full.
3. [Justus et al. (2023): Transwell In Vitro Cell Migration and Invasion Assays](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335869/)

   贴壁与非贴壁细胞回收、膜表面计数和实验条件。
4. [Corning: Assay Methods—Cell Invasion Assay](https://www.corning.com/catalog/cls/documents/protocols/protocol_DL_031_Cell_Invasion_Assay.pdf)

   涂层与未涂层配对、独立插入件及通过比例分母。
5. [ibidi: Chemotaxis and Migration Tool 2.0 manual](https://ibidi.com/img/cms/products/software/chemotaxis_tool/Manual_ChemotaxisTool_2_0_eng.pdf)

   轨迹标定、路径距离、直线性与前向迁移指数定义。
6. [ImageJ: Analyze menu](https://imagej.net/ij/docs/menus/analyze.html)

   空间标定、面积与区域保存。
