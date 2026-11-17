# 活死染色：把细胞状态变成可读图像

Source: https://ml-biomat.com/tutorials/experimental-methods/l03/
Language: zh-CN

从染料进出细胞的机制，走向背景、串色、对象分类与三维材料里的空间判断。

## 一张绿色的细胞照片，究竟回答了什么问题

把细胞放到一块新制备的水凝胶上，第二天拍到许多绿色亮点，通常是一件令人高兴的事。但接下来仍有值得追问的细节：这些亮点对应多少个细胞，是否分布均匀，材料内部是否也有相似状态，红色细胞是在表面还是深处？活死染色的价值就在这里。它把细胞的一部分生理状态转成可以定位的光信号，使材料表面、孔隙和细胞群体不再只是一个平均读数。我们可以沿着图像找出状态变化出现在哪里，再把它与接种、运输和局部环境联系起来。

本节以哺乳动物细胞常用的 calcein AM 与乙锭同二聚体 EthD-1 双染为例。前者通过细胞内酯酶产生可保留的荧光产物，后者主要进入膜完整性受损的细胞并与核酸结合。名称虽然叫活死染色，实际观察的是酯酶活性、产物保留与膜通透性这几个具体性质。把这些性质说清楚，后面的颜色、阈值和百分比才有明确含义。细胞是否正在复制 DNA、是否能形成新群体、是否保持某项功能，则可以通过相应实验继续观察。

初学者很容易把“更亮”理解成“活得更好”。实际上，同样数量的细胞可能因为染料进入量、酶活性、细胞体积、曝光时间或观察深度不同而出现不同亮度。相反，细胞数减半与每个细胞亮度减半，都可能让整孔绿色信号减半。因此，实验开始前要确定想比较的是单细胞分类比例、单位面积的细胞数量、空间分布，还是整孔荧光强度。它们可以共同出现，但计算时各自使用的对象和分母应保留。

图像还有一个直接优势：它允许我们同时观察形态。一个细胞是否铺展、是否聚团、是否位于材料裂隙附近，常常给出下一步检查的线索。形态与染色共同描述状态，却不需要被压成同一个分数。例如某种表面上细胞保持绿色但明显圆缩，可以进一步检查附着与骨架组织；另一种材料上红色对象集中在中心，则值得检查中心区域的供养、染料到达和成像深度。先让空间信息帮助提出问题，再选择下一项实验。

## 让细胞自己完成一段发光反应

普通染料可以直接给物体着色，荧光前体则把一次化学变化变成可见信号。1966 年，Rotman 与 Papermaster 研究能在酶作用后产生荧光的酯类化合物，观察活细胞内荧光产物的积累，并将产物保留与细胞膜完整性联系起来。这项研究提供了一种巧妙的思路：让较容易进入细胞的前体先通过膜，再由胞内酶把它转成性质不同的产物，观察产物能否留在细胞内部。历史中的问题不是给所有细胞贴一张永久标签，而是借分子的进出研究细胞状态。

![从 1966 年的荧光酯研究读懂进入、酶转化与膜内保留。右图示意现代红色探针的膜通透性与核酸结合机制；为原理图，不是历史实验复刻。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/dde800e83cdc4181788a2fcd.svg?v=dde800e83cdc)

图 1从 1966 年的荧光酯研究读懂进入、酶转化与膜内保留。右图示意现代红色探针的膜通透性与核酸结合机制；为原理图，不是历史实验复刻。

calcein AM 延续了这样的测量逻辑。AM 基团帮助前体进入细胞，胞内酯酶切除相关基团后，形成带有较强绿色荧光、较难穿过完整细胞膜的 calcein。可以把它想成携带临时通行外衣的小包裹：进门后外衣被拆下，里面的发光物更容易留在房间中。这个比喻只帮助理解进入与保留；真实过程还受分子电荷、酶反应、运输和染色时间影响。绿色出现需要一串条件配合，所以它既与细胞数量有关，也与每个细胞的反应状态有关。

EthD-1 提供另一条信息。完整细胞膜通常阻止它进入；膜通透性明显增加后，它可以到达细胞内部，与核酸结合并产生较强红色荧光。核酸是包括 DNA 和 RNA 在内的一类分子，DNA 储存遗传信息，因此红色信号常与核区域相关。这里的颜色来自染料与光学通道，并非细胞死亡时天然变红。不同活死染色组合使用的染料、进入机制和检测波段可能不同，不能只凭包装上的绿色与红色就把条件完全互换。

双染可以把观察对象暂时分成绿单阳、红单阳、双阳和双阴四类。“阳性”表示信号超过预先确定的判定标准。绿单阳符合酯酶产物生成并保留、红色探针进入较少的状态；红单阳提示膜通透性增加而绿色信号较低。双阳可能涉及状态转变、残留产物、对象重叠或通道串色；双阴则可以来自信号较弱、染色不足、深处衰减或并非细胞的对象。保留四类及原始图像，有助于把这些原因进一步分开。

常规这种双染需要在适当染色窗口内观察活体样本。固定和通透处理会改变膜性质，并可能使非共价保留的染料移动；如果先完成固定再按同样方法染色，测到的膜通透性就已包含处理本身的影响。需要固定后继续分析时，可以选用为相应目的设计并验证的可固定探针，并按其反应机制解释结果。把样本处理顺序与测量性质连起来，就能明白为什么某个流程中的染色条件不能随意移到另一个流程。

## 先准备几幅能解释颜色的对照图

第一次在一种新材料上使用染料时，可以先观察没有细胞、没有染料的材料。某些高分子、交联产物、表面处理成分或培养液本身会发光，这称为自发荧光。再观察没有细胞但加入染料的材料，可以检查染料是否吸附在表面或聚集在孔隙。两种图像回答不同问题：前者给出材料原有背景，后者还包括材料与染料相互作用。若只用空玻璃作背景，就可能漏掉材料特有的光学表现。

细胞对照则帮助建立染色响应。状态良好的未处理细胞提供常见的绿色范围，经过适当验证的膜受损对照帮助确认红色探针能够进入并被检测。单独加入绿色探针或红色探针的单染对照，可以检查一个染料在另一通道是否产生信号。对照应使用与实验样本相近的细胞、材料、染色时间和成像设置，因为这些条件共同决定背景与响应。它们不是实验结束后补上的装饰，而是用来解释每一个信号从哪里来的具体比较。

三维材料尤其需要考虑染料和光的到达。染料从外液进入支架需要时间，内部细胞不一定与表面细胞同时接触到相同浓度；荧光从深处传到探测器，又会受到吸收、散射和光学系统的影响。绿色较弱既可能来自细胞状态，也可能来自这两段传输。可以比较不同深度的响应、检查染色时间变化，并使用适合的深度成像与光学对照。表面一张清晰照片，描述的是那个观察层面的细胞，而不是自动代表整个支架。

处理样本时还要留意细胞是否被选择性丢失。膜受损或附着较弱的细胞可能更容易进入上清、在换液时被带走；如果只拍洗涤后仍留在材料上的细胞，分母就变成了保留群体。需要评价整个处理体系时，可以把上清、附着群体和必要的收集步骤纳入设计，并记录它们怎样汇总。这个问题与图像本身的清晰程度无关，却可能显著改变最后的活细胞比例。

## 相机保存的是数字，颜色只是读图方式

荧光显微镜用特定波段的光激发染料，再通过滤光系统收集发射光。相机或探测器把光信号转成像素数值，软件随后给这些数值分配绿色、红色或其他显示颜色。本节的合并图用绿色和紫红色显示两个通道，使它们更容易区分；改变显示配色不改变原始信号。原始通道应分别保存，并保留曝光、增益、光源设置、像素尺寸和深度位置。用于展示的合并图，则帮助读者理解空间对应关系。

![构造图像的两个原始通道、合并显示与逐对象信号。像素尺寸为 1 μm；已知中心区域用于提取强度，四类对象全部保留，虚线阈值为 40 a.u.。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cbf6ad79350502f5ea29ee76.svg?v=cbf6ad793505)

图 2构造图像的两个原始通道、合并显示与逐对象信号。像素尺寸为 1 μm；已知中心区域用于提取强度，四类对象全部保留，虚线阈值为 40 a.u.。

曝光过低会使弱信号淹没在噪声里，过高则可能使像素达到探测器上限。达到上限以后，更强的光仍显示同一个最大值，这叫饱和。饱和区丢失了强度差异，事后调暗显示也无法恢复。比较强度时，应在有代表性的强弱样本上选择共同的有效采集范围，检查原始像素分布，并避免对每张图单独自动调整后再凭视觉比较亮度。显示对比度可以改善阅读，但定量分析应回到保留原始数值的数据。

背景扣除也需要对应测量对象。若一个细胞区域包含一百个像素，像素强度之和为一万二千，邻近无细胞背景平均每像素为二十，那么背景贡献约为两千，校正后的总信号为一万。这是“每像素背景乘像素数”的体积式思路：区域越大，累计的背景也越多。不同区域背景不均匀时，可以使用有依据的局部估计或平场校正，并保留处理前后图像，检查真实细胞结构有没有被一起削去。

$$
F_{\mathrm{corr}}=\sum_{j=1}^{n_p} I_j-n_p\bar B,\qquad \bar I_{\mathrm{corr}}=\frac{F_{\mathrm{corr}}}{n_p}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e75ccac71f13631e1c7c90f9.svg) | 对象区域的扣背景总强度，a.u.（任意强度单位）。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2182e4a63941864596054a3f.svg) | 第 j 个像素的原始强度，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 像素索引，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4773c6daf0d996bad65e1235.svg) | 对象区域的像素数，无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9744967524d2194c13c2ad4e.svg) | 相同采集条件下每像素平均背景，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a7fd434c3ba79d2fe36f71b7.svg) | 对象区域的扣背景平均像素强度，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对对象区域内像素求和。 |

背景近似均匀且加性时，将每像素背景乘区域像素数后扣除。100 个像素总强度 12000、平均背景 20，校正总强度为 10000，校正平均强度为 100。

两个荧光通道还可能存在串色。绿色染料的部分发射光落入红色检测窗口时，一个绿色细胞也会在红色通道出现信号。单染对照可以估计这种贡献，在探测器响应近似线性且没有饱和时进行相应校正。以简单单向串色模型为例，绿色校正信号一百、串入系数为 0.4，红色通道会额外增加四十；若真实红色信号为五，测得四十五可能超过红色阈值。减去估计的绿色贡献后，才能判断这是否属于真正的双阳对象。

$$
G=G_{\mathrm{obs}}-B_G,\qquad R=R_{\mathrm{obs}}-B_R-\alpha G
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8602e0bdcf66b1b2ee9fa0fc.svg) | 扣背景、并对红色校正单向串色后的平均信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9a32cfa1933f9b284de73c20.svg) | 对象区域在绿色和红色通道的原始平均信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/50bcf82ce5fdf10817b8563e.svg) | 对应通道的平均背景，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 绿色向红色通道的串入系数，无量纲，在同一检测设置下由单染对照估计。 |

此例假设信号线性、未饱和，且红色向绿色的串入可忽略。扣背景绿色 100、真实红色 5、α=0.4 时，扣背景但未校正串色的红色为 45；减去 40 后回到 5。两个方向都有串色时需对应的双向模型。

本节程序生成一幅有明确真值的教学图像，保存两个含背景与噪声的原始通道，以及已知细胞位置附近的测量区域。随后从每个区域提取像素平均值，扣除已知背景并校正串色，形成逐对象信号表。这里有意把区域位置作为已知条件，以便集中检查信号处理；实际图像还需通过独立核标记、细胞边界或经过检查的分割方法定位对象。将定位与分类分成两步，可以看清误差发生在“找到了几个对象”还是“把对象分成哪一类”。

## 从图像走向百分比，最重要的是分母

一个绿色细胞铺展得很大，另一个细胞只形成小亮点，两者在绿色像素面积上差异很大，却各自只对应一个细胞。因此，绿色面积除以红绿总面积，通常测量的是染色区域的面积比例，而不是细胞数比例。若研究问题需要细胞比例，应先建立逐细胞对象，再测量各自信号。相邻细胞接触时可能被分成同一个对象，单个细胞的碎片又可能被分成多个；把识别轮廓叠加回原图检查，能直接发现这些情况。

构造示例中共有一百二十个已定位对象。按校正信号和阈值分类，绿单阳八十四个，红单阳二十四个，双阳六个，双阴六个。绿单阳占全部对象百分之七十，所有红阳对象占百分之二十五，另有百分之五双阴。如果只在两个单阳类别之间计算，得到八十四除以一百零八，约百分之七十七点八；这是“已分为两个单阳类别的对象中，绿单阳的比例”，与全体对象的百分之七十含义不同。把四类原始计数列出来，两个结果之间的区别便一目了然。

$$
N=N_{G}+N_{R}+N_{GR}+N_{0},\qquad p_G=\frac{N_G}{N},\qquad p_{R+}=\frac{N_R+N_{GR}}{N},\qquad p_{G\mid\mathrm{single}}=\frac{N_G}{N_G+N_R}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 全部已定位并纳入分析的对象数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0356a29120b1d61c171a4944.svg) | 绿单阳对象数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/682d716020f3a5d1a3665231.svg) | 红单阳对象数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4e18d96696d9fb378aec36d4.svg) | 双阳对象数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 双阴对象数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0d6a3f0d3a47869a3a5eb7ae.svg) | 绿单阳占全部对象比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc86242e9123e8782d45a318.svg) | 红阳占全部对象比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0489dadaffb1d9203979c6a0.svg) | 仅在两个单阳类别中计算的绿单阳比例，无量纲。 |

84、24、6、6 个对象共 120 个；p_G=70%，p_R+=25%。只保留两个单阳类别时，84/108=77.78%，因此需同时报告分类范围与排除类别。每个对象仅归入四类中的一类。

阈值不应随着希望得到的结论逐张调节。可以根据阴性和单染对照、背景分布以及代表性样本确定判定方法，再以一致的规则应用于比较对象。对于亮度和背景随位置变化的图像，分割方法可能需要局部信息，但其选择和参数也要经过验证。观察阈值在合理范围内变化时，结果是否稳定，有助于判断结论是来自清晰分离的群体，还是大量对象恰好堆在边界附近。图中的阈值敏感性曲线保留同一个总对象分母，让这种变化容易看清。

![四类计数、阈值敏感性、构造深度衰减与整体强度的不同来源。A、B 使用同一分母 120；C 的系数是教学参数；D 区分细胞数与单细胞亮度。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/45ea6288345eae7703139a31.svg?v=45ea6288345e)

图 3四类计数、阈值敏感性、构造深度衰减与整体强度的不同来源。A、B 使用同一分母 120；C 的系数是教学参数；D 区分细胞数与单细胞亮度。

不同视野的汇总方式也会影响数字。如果第一个视野有八十个绿单阳和一百个总对象，第二个有五个绿单阳和十个总对象，简单平均两个百分比得到百分之六十五；合并计数则得到八十五除以一百一十，约百分之七十七点三。前者是两个视野比例的等权平均，后者是这些已观察对象的合并比例。若两个视野属于同一孔，应先说明希望描述视野分布还是整个采样群体；比较独立培养孔或批次时，再保留相应的独立重复层次。

比例还应与绝对数量一起阅读。材料甲保留了九十个绿单阳和十个红单阳，材料乙只保留九个绿单阳和一个红单阳，两者单阳群体中的绿色比例同为百分之九十，但可供后续研究的细胞数量相差十倍。如果问题关注材料的细胞承载或保留能力，可以同时报告单位面积或单位体积的对象数，并给出所用面积、深度和有效观察范围。这样一个漂亮的百分比就不会遮住群体大幅减少这一变化。

观察对象较少时，分类比例还会有较大的随机波动。应保留每个视野和每个独立样本的计数，结合实验设计汇总，而不是只给一个汇总百分数。若一个材料上细胞集中成团，来自相同团块的细胞也可能共享局部环境；增加同一团块内的细胞数，与增加独立位置或独立培养样本提供的信息不同。安排跨区域的采样，能够同时观察总体趋势与局部不均匀性。

## 细胞没有改变，双阳为什么突然变多？

四个圆代表信号相同的四组构造细胞，圆内数字为对象数，共 120 个。调整单向串色和共同分类阈值，打开或关闭校正，比较同一群体的判定。这里的分组信号是无噪声示例；正文代码另有含噪声的逐像素图像。

[Figure: 绿色和红色信号及四类对象计数](https://ml-biomat.com/tutorials/experimental-methods/l03/#L03-lab)

## 看见深处、保留数量，才能读懂材料上的状态

三维支架里的图像可以按深度分层观察。一个简化的衰减模型假设信号随光程增加按指数下降，说明即使细胞本身不变，深处仍可能显得更暗。指数的含义是每经过相同厚度，剩余光再乘同一个比例。在构造例子中，绿色有效衰减系数为每微米 0.006，红色为每微米 0.003；到二百微米深处时，分别剩约百分之三十和百分之五十五。两通道衰减不同，便会改变相同细胞在二维信号图上的位置。

$$
I(z)=I_0\exp(-\mu z),\qquad f(z)=\frac{I(z)}{I_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51a5b62ee59924de23f8e7a8.svg) | 深度 z 的测得信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 零深度参照信号，a.u.。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | 观察深度，μm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 简化模型的有效衰减系数，μm⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | 以自然常数 e 为底的指数函数，输入 μz 无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c2298a29bae4706e73396095.svg) | 相对参照保留的信号比例，无量纲。 |

同样厚度使剩余信号乘同一比例，形成指数衰减。此均匀有效模型用于说明深度效应；μ=0.006 μm⁻¹、z=200 μm，f=e⁻¹·²≈0.301；μ=0.003 时 f≈0.549。

深度堆栈还带来重复计数问题。一个细胞可能出现在相邻的多个光学切片中，若逐层计数后直接相加，就会把同一个细胞重复纳入。可以根据三维对象连接规则识别完整对象，或采用明确的分层取样方法；最大强度投影有助于展示空间轮廓，却可能把前后重叠细胞叠在一起。选择三维计数、分层比例或投影面积时，应让分析对象与准备回答的问题相匹配。

图中的长度也要经过空间标定。一个像素代表多少微米取决于物镜、相机与采集设置，图像在文档中放大或缩小并不会改变这个原始关系。只有知道像素对应的实际长度，才可以把细胞计数换成单位面积密度，或比较不同深度与材料尺寸。比例尺应跟随图像缩放，而不能从另一张不同倍率的照片里直接复制。

真实显微成像中的衰减包含照明、发射收集、散射和光学结构等因素，这个简化式用来理解方向与尺度。要对实际材料作深度比较，可以记录分层强度与对象数量，检查染料到达情况，并用合适参照评估深度响应。对每层分别自动拉亮，能让展示更清楚，却会隐藏层与层之间的原始信号差异；因此应将显示调整与数值比较区分，并在图注交代观察层面、深度范围和比例尺。

时间同样会改变观察。持续激发可能造成光漂白，使染料逐渐失去发光能力；成像过程还可能影响活细胞状态。若按固定顺序观察一整块板，前后样本的染色等待时间可能不同。可以通过交错或随机化观察顺序、记录染色到拍摄的间隔、减少不必要照射，并检查时间依赖性来控制这些因素。需要追踪同一个细胞时，则应明确测量本身给它带来的光照与染料暴露。

真实研究也提醒我们保留不同测量层次。Sazonova 等在 2022 年比较了代谢读数、calcein/EthD-1 信号、流式细胞分析和蛋白检测。原图中的绿色信号以对照归一化，测量的是整孔荧光，而不是图像逐细胞计数；加入抑制特定死亡过程的处理后，红色信号和绿色信号并没有按同样方式恢复。把两者并列，才能看到细胞死亡减少与细胞群体扩增恢复是不同问题。原图其余测量进一步帮助研究者解释这些差别。

![Sazonova 等（2022）图 2，CC BY 4.0，完整转载。a 为 MTS、b 为双染整孔信号、c 为流式分类、d 为蛋白检测；a、c 有 5 次重复，b 有 6 次，点与均值±标准差按原图保留。Contr 为对照，Cis 为顺铂，Q-VD 为所用半胱天冬酶抑制剂。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5a4e200f980785839602728b.svg?v=5a4e200f9807)

图 4Sazonova 等（2022）图 2，CC BY 4.0，完整转载。a 为 MTS、b 为双染整孔信号、c 为流式分类、d 为蛋白检测；a、c 有 5 次重复，b 有 6 次，点与均值±标准差按原图保留。Contr 为对照，Cis 为顺铂，Q-VD 为所用半胱天冬酶抑制剂。

读这幅图时，可以先只比较 b 面板：左侧看绿色通道，右侧看红色通道，再检查共同的组别名称与各自纵轴。每个点表示原研究的一次重复，线与误差线表示均值和标准差，两个通道均有六次重复。随后再转到 a、c 面板，观察不同测量是否讲述同一部分变化。图中的红色信号可以低于平均背景，这反映了该研究的归一化与背景基准，不能当成“负的死亡细胞数”。把坐标定义读清楚，复杂图也可以逐层理解。

## 让每一个分类都能回到原图

完整示例输出双通道原始数组、对象区域标签、逐对象信号表和分类汇总。图像包含固定随机种子的背景噪声与不同细胞信号，因此运行后可以逐步复查：哪些像素属于一个对象，平均强度怎样算出，背景扣了多少，绿色贡献怎样从红色通道中减去，以及最终对象落在哪个阈值区域。图中保留双阳和双阴，避免在计算前把难解释对象悄悄丢掉。原研究图作为另外一个真实测量例子，与这些构造数据清楚分开。

### 双通道图像、逐对象信号与分类

固定种子构造原始图像，从已知区域测量像素强度，输出 NPZ、CSV、四图及分类摘要。真实研究图与许可随示例提供。

```
"""Constructed two-channel cell images: background, spillover and denominators."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,FancyArrowPatch,Rectangle

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(303);classes=np.repeat(np.arange(4),[84,24,6,6]);rng.shuffle(classes)
    xy=np.array([(18+25*x,18+25*y) for y in range(10) for x in range(12)],float)+rng.uniform(-3,3,(120,2))
    green=np.choose(classes,[100,5,70,5])+rng.normal(0,4,120);red=np.choose(classes,[5,100,70,5])+rng.normal(0,3,120);alpha=.15;bg=np.array([25.,20.]);gobs=green+bg[0];robs=red+alpha*green+bg[1]
    gc=gobs-bg[0];rc=robs-bg[1]-alpha*gc;threshold=40.;gp=gc>=threshold;rp=rc>=threshold
    counts=np.array([np.sum(gp&~rp),np.sum(~gp&rp),np.sum(gp&rp),np.sum(~gp&~rp)]);assert list(counts)==[84,24,6,6]
    yy,xx=np.mgrid[:270,:320];G=np.full(xx.shape,bg[0]);R=np.full(xx.shape,bg[1]);labels=np.zeros(xx.shape,int)
    for i,((x,y),g,r) in enumerate(zip(xy,green,red)):
        kernel=np.exp(-((xx-x)**2+(yy-y)**2)/(2*4**2));G+=g*kernel;R+=(r+alpha*g)*kernel;labels[(xx-x)**2+(yy-y)**2<=2**2]=i+1
    G+=rng.normal(0,1.2,G.shape);R+=rng.normal(0,1.2,R.shape)
    np.savez_compressed(output/'constructed_channels.npz',green_raw=G,red_raw=R,roi_labels=labels,pixel_um=1.,class_truth=classes,centers_xy=xy)
    gobs=np.array([G[labels==i+1].mean() for i in range(120)]);robs=np.array([R[labels==i+1].mean() for i in range(120)])
    gc=gobs-bg[0];rc=robs-bg[1]-alpha*gc;gp=gc>=threshold;rp=rc>=threshold
    counts=np.array([np.sum(gp&~rp),np.sum(~gp&rp),np.sum(gp&rp),np.sum(~gp&~rp)]);assert list(counts)==[84,24,6,6]
    np.savetxt(output/'cell_signals.csv',np.column_stack([np.arange(1,121),classes,gobs,robs,gc,rc]),delimiter=',',header='id,constructed_class,green_observed_au,red_observed_au,green_corrected_au,red_unmixed_au',comments='')
    fig,ax=plt.subplots(1,2,figsize=(11.5,4.7))
    for a in ax:a.set(xlim=(0,10),ylim=(0,7));a.axis('off')
    a=ax[0];a.add_patch(Circle((6,3.5),2,facecolor='#d9eee5',edgecolor='#3c8a6a',lw=3));a.text(6,4.1,tr('胞内酯酶','Intracellular esterase'),ha='center');a.text(6,3,tr('发光产物保留','Fluorescent product retained'),ha='center',fontsize=10);a.text(1.7,4.7,tr('可进入的前体','Permeant precursor'),ha='center');a.add_patch(FancyArrowPatch((2.5,3.5),(5,3.5),arrowstyle='->',mutation_scale=18));a.set_title(tr('A  进入 → 转化 → 保留','A  Entry → conversion → retention'));a.text(5,.4,tr('1966：Rotman 与 Papermaster\n用荧光酯研究细胞膜与产物保留。','1966: Rotman and Papermaster\nconnect fluorogenic esters to membrane retention.'),ha='center',fontsize=10)
    a=ax[1];a.add_patch(Circle((6,3.5),2,facecolor='#f0e2ed',edgecolor='#8160a1',lw=3,ls='--'));a.add_patch(Circle((6,3.5),.8,facecolor='#cd803f',alpha=.6));a.text(6,3.5,tr('核酸','Nucleic acids'),ha='center');a.text(1.8,4.7,tr('膜受损后可进入','Entry after membrane damage'),ha='center',fontsize=10);a.add_patch(FancyArrowPatch((2.5,3.5),(5,3.5),arrowstyle='->',mutation_scale=18));a.set_title(tr('B  进入 → 核酸结合 → 发光','B  Entry → nucleic-acid binding → fluorescence'));a.text(5,.4,tr('现代双参数染色：\n酯酶活性与膜通透性分别提供信息。','Modern two-parameter staining:\nesterase activity and permeability provide distinct information.'),ha='center',fontsize=10);fig.tight_layout();save(fig,'mechanism')
    fig,ax=plt.subplots(2,2,figsize=(10.8,8));rgb=np.zeros((*G.shape,3));rgb[:,:,1]=np.clip((G-bg[0])/120,0,1);rgb[:,:,0]=np.clip((R-bg[1])/120,0,1);rgb[:,:,2]=rgb[:,:,0]*.65
    for a,im,title,cmap in [(ax[0,0],G,tr('A  原始绿色通道','A  Raw green channel'),'viridis'),(ax[0,1],R,tr('B  原始红色通道','B  Raw red channel'),'magma')]:
        image=a.imshow(im,cmap=cmap,vmin=0,vmax=160,origin='lower',extent=[0,320,0,270]);fig.colorbar(image,ax=a,label=tr('强度 / a.u.','Intensity / a.u.'));a.set_title(title);a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,0];a.imshow(rgb,origin='lower',extent=[0,320,0,270]);a.plot([240,290],[22,22],color='white',lw=3);a.text(265,32,'50 μm',color='white',ha='center',fontsize=9);a.set_title(tr('C  合并显示；紫红色帮助区分通道','C  Composite; magenta distinguishes the red channel'));a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,1];palette=['#3c8a6a','#cd803f','#8160a1','#7c8990'];
    for k,name in enumerate([tr('绿单阳','Green only'),tr('红单阳','Red only'),tr('双阳','Double positive'),tr('双阴','Double negative')]):a.scatter(gc[classes==k],rc[classes==k],s=23,color=palette[k],label=name)
    a.axvline(40,c='#89989d',ls='--');a.axhline(40,c='#89989d',ls='--');a.set(xlabel=tr('扣背景绿色 / a.u.','Background-corrected green / a.u.'),ylabel=tr('校正串色红色 / a.u.','Unmixed red / a.u.'),title=tr('D  每个对象保留两个信号','D  Retain both signals per object'));a.legend(fontsize=8);fig.suptitle(tr('构造的双通道教学图像；从已知对象区域提取像素均值','Constructed two-channel images; mean pixel signals extracted from known object regions'),fontsize=11);fig.tight_layout();save(fig,'channels')
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.5));names=[tr('绿单阳','Green only'),tr('红单阳','Red only'),tr('双阳','Double +'),tr('双阴','Double −')];ax[0,0].bar(names,counts,color=palette);ax[0,0].set(ylabel=tr('对象数','Object count'),title=tr('A  保留四类与共同分母 120','A  Preserve four classes and denominator 120'))
    thresholds=np.linspace(20,115,96);single=[np.sum((gc>=q)&~rp)/120*100 for q in thresholds];ax[0,1].plot(thresholds,single);ax[0,1].axvline(40,c='#cd803f',ls='--');ax[0,1].set(xlabel=tr('绿色阈值 / a.u.','Green threshold / a.u.'),ylabel=tr('绿单阳占全部对象 / %','Green-only fraction of all objects / %'),title=tr('B  阈值敏感性保留分母','B  Threshold sensitivity with fixed denominator'))
    z=np.linspace(0,400,201);ax[1,0].plot(z,100*np.exp(-.006*z),label=tr('绿色 μ=0.006 μm⁻¹','Green μ=0.006 μm⁻¹'));ax[1,0].plot(z,100*np.exp(-.003*z),label=tr('红色 μ=0.003 μm⁻¹','Red μ=0.003 μm⁻¹'));ax[1,0].set(xlabel=tr('深度 / μm','Depth / μm'),ylabel=tr('保留强度 / %','Retained intensity / %'),title=tr('C  构造的深度衰减','C  Constructed depth attenuation'));ax[1,0].legend(fontsize=8)
    ax[1,1].bar([tr('100 个 × 100','100 cells × 100'),tr('100 个 × 50','100 cells × 50'),tr('50 个 × 100','50 cells × 100')],[10000,5000,5000],color=['#186e83','#cd803f','#8160a1']);ax[1,1].set(ylabel=tr('总荧光 / a.u.','Total fluorescence / a.u.'),title=tr('D  一样的总强度有不同原因','D  Equal total intensity can have different causes'));fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(9.2,10.5));ax.imshow(plt.imread(Path(__file__).with_name('sazonova2022-figure2.jpg')));ax.axis('off');ax.set_title(tr('真实实验：信号降低可以包含增殖停滞与细胞死亡','Measured example: reduced signal can combine growth arrest and death'),fontsize=12);fig.text(.5,.03,tr('Sazonova 等，2022，图 2，CC BY 4.0。完整原图；a、c 为 N=5，b 为 N=6，均值±标准差。','Sazonova et al., 2022, Fig. 2, CC BY 4.0. Complete original; a,c N=5; b N=6; mean ± SD.'),ha='center',fontsize=9);save(fig,'published')
    summary={'classification':{'green_only':84,'red_only':24,'double_positive':6,'double_negative':6,'total':120,'green_only_all_percent':70.,'red_positive_all_percent':25.,'resolved_viability_percent':84/108*100},'background':{'corrected_sum_example':12000-100*20},'spillover':{'green':100.,'red_true':5.,'red_measured_at_04':45.,'red_unmixed_at_04':5.},'depth':{'green_200_fraction':float(np.exp(-1.2)),'red_200_fraction':float(np.exp(-.6))},'pooling':{'pooled_percent':85/110*100,'equal_field_average_percent':65.},'sampling':{'ideal_se_fraction':float(np.sqrt(.7*.3/120))}}
    assert sum(counts)==120 and abs(rc+alpha*gc+bg[1]-robs).max()<1e-10 and 84/120==.7
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

可以先提高绿色阈值，观察哪些对象最先改变分类；再增加绿色向红色的串入系数，比较校正前后双阳数量。若改变背景但仍使用旧背景值扣除，整个群体会在信号图上移动；若只是改变显示配色，数值分类应保持相同。这样逐次改变一个条件，可以把图像处理中的“看起来变化了”与“原始测量或判定变化了”区分开。对真实图像，保存分析规则、对象轮廓和原始通道，也是在给未来的复查保留入口。

一份清楚的活死染色结果，应能说明观察的是哪类细胞、处于何种材料与时间点、使用什么探针和分类规则、观察了哪些空间区域，以及计数分母怎样形成。随后可以按问题接上其他实验：想知道绿色群体是否正在增加，观察 DNA 合成或长期数量变化；想理解圆缩，观察骨架与附着；想追踪死亡过程，结合相应分子标志与时间信息。染色图因此成为研究逻辑中的一个可定位、可计数的环节，而不是只用来证明材料上“有绿色”的配图。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Rotman and Papermaster (1966): Membrane properties of living mammalian cells as studied by enzymatic hydrolysis of fluorogenic esters](https://doi.org/10.1073/pnas.55.1.134)

   荧光前体、酶转化与细胞膜保留的原始历史研究；原文首页已读。
2. [Thermo Fisher: Molecular Probes Handbook, Section 15.3](https://www.thermofisher.com/us/en/home/references/molecular-probes-the-handbook/assays-for-cell-viability-proliferation-and-function/viability-and-cytotoxicity-assay-kits-for-diverse-cell-types.html)

   calcein AM 与 EthD-1 的两条检测原理及使用对象。
3. [Thermo Fisher: LIVE/DEAD Viability/Cytotoxicity Kit for mammalian cells protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/live-dead-viability-cytotoxicity-kit-for-mammalian-cells.html)

   染色时间、背景与固定兼容性需要按探针定义。
4. [ImageJ: Principles of Scientific Imaging](https://imagej.net/imaging/principles)

   像素数据、原始图像保存、均匀照明及阈值分割。
5. [Sazonova et al. (2022): Drug toxicity assessment: cell proliferation versus cell death](https://pmc.ncbi.nlm.nih.gov/articles/PMC9568594/)

   真实图 2 与方法说明，比较整体信号、细胞状态及增殖变化。

   CC BY 4.0; Figure 2 reproduced intact with attribution and added outer teaching title.
