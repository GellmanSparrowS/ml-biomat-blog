# 免疫荧光：让目标蛋白在细胞中显现

Source: https://ml-biomat.com/tutorials/experimental-methods/l05/
Language: zh-CN

从抗体识别到核胞质比，读懂真实细胞图像，并亲手检验背景、曝光与区域选择。

## 一枚细胞变亮之前，先问蛋白去了哪里

把细胞放在柔软的凝胶和坚硬的玻璃上，它们可能长得不一样：有的铺展，有的收拢，有的把调节基因活动的蛋白送进细胞核。显微镜能看见轮廓，却认不出某个蛋白。免疫荧光给这个问题加上了分子身份：用能够结合目标的抗体带路，再用荧光标记显示它所在的位置。于是，研究问题可以从“细胞好像变了”，推进到“这个蛋白在核内与核外的分布怎样改变”。位置很有用，因为细胞中的许多工作有固定场所。酶在一个区室中遇得到的伙伴，换到另一个区室后可能完全不同。

先把一幅荧光照片想成有地址的测量表。每个像素对应标本中的一小片区域，数值表示探测器记录到的信号；绿色和紫色是把数值展示给眼睛的颜色。抗体识别、染料发光、显微镜收光和屏幕显示，分别完成不同任务。细胞发出的光多，并不自动意味着目标蛋白多：更多抗体到达、曝光变长、材料自身发光，都能把照片推亮。因此，实验要同时回答两件事：这些信号来自什么，以及这些数值是在怎样的条件下得到的。弄清这条测量链，后面的对照和计算便有了共同目的。

本章用两个互相补充的例子来学习。真实的人类蛋白图谱图像展示细胞中波形蛋白的纤维状分布，让我们练习辨认通道和空间结构；一个可重复运行的构造图像实验则保持每枚细胞的目标总信号相同，只改变核内外分配，让我们追踪从像素到结论的每一步。前者提供真实细胞的复杂外观，后者给出已知答案，便于检查背景、分区和曝光怎样改变结果。它们各自回答清楚的问题，读者不需要预先学过免疫学或图像编程。

一开始就写下测量对象，可以省去许多后来无法解释的比较。想研究“进入细胞核”，通常需要每枚细胞的核内与胞质平均信号；想研究“单个细胞含量”，则需要整个细胞的积分信号和完整边界；想研究“蛋白形成斑点”，还要记录斑点数量、大小与检测尺度。这些量会对细胞变大作出不同反应。一个面积扩大而平均亮度不变的细胞，积分信号会增加；一个总量不变而蛋白集中到小区域的细胞，局部平均亮度会增加。先明确问题，才知道该画哪种区域、保存哪些原始数值。

## 抗体怎样把分子身份变成可见位置

抗体是一类蛋白质，可以把它想成有特定接触面的夹子。目标上被它识别的一小部分叫表位，可能是一段相邻的氨基酸，也可能由折叠后彼此靠近的几段组成。这个比喻有一个有用的细节：夹子能否扣上，既看接触面是否匹配，也看那一面有没有露出来。同一个蛋白在活细胞、固定细胞和被展开的蛋白溶液中，会呈现不同的表面。因此，一支抗体在一种实验中得到清楚结果，换到另一种制样条件后仍需要检查它实际识别的对象。

1941 年，Coons、Creech 和 Jones 把带有蒽基的荧光基团接到抗体相关蛋白上，检验它们是否仍保留特异识别。他们比较不同型的肺炎球菌，在可见光下都能找到的细菌，经过相应标记后呈现不同的荧光结果。原文还记录了一个直接推动方法改进的困难：组织自身的蓝色荧光会淹没这种标签。这个故事把两个问题同时摆出来了——给分子装灯，以及让这盏灯从背景中被认出来。今天选择染料、设置阴性对照和测量材料自发荧光，仍是在处理这两个问题。

![直接与间接标记的原创示意。星号代表荧光标签，不表示真实结合数量；科学史连接识别与背景两个问题。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fbb28ee22cf663401744d6d2.svg?v=fbb28ee22cf6)

图 1直接与间接标记的原创示意。星号代表荧光标签，不表示真实结合数量；科学史连接识别与背景两个问题。

直接免疫荧光把染料接在识别目标的一抗上，识别与报告由同一支抗体完成。间接法先让一抗结合目标，再让带染料的二抗结合一抗。例如，一抗由兔来源抗体构成，就选择能够识别相应兔免疫球蛋白的二抗；“抗兔”说的是二抗识别谁，并不是样品必须来自兔。间接法让不同一抗共享报告工具，也可能增加每个目标附近的荧光标签数量。与此同时，它增加了一层结合过程，所以二抗对样品的结合和不同通道之间的交叉识别，也成为需要观察的对象。

抗体浓度的影响可以用一个简单平衡模型理解。设所有结合位点相同，游离抗体充足，系统已经达到平衡，浓度增加会提高位点被占据的比例，随后逐渐接近饱和。解离常数描述这条曲线的位置：浓度等于它时，一半位点被占据。这个理想模型帮助理解为什么把抗体再加十倍，特异信号未必也增加十倍。实际标本中还存在不同亲和力的接触、空间阻挡、扩散和洗涤过程，所以最佳工作浓度要从真实信号与背景的共同变化中选择，而不是只盯着哪张照片最亮。

$$
\theta=\frac{c}{K_d+c}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 结合位点占据比例，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 平衡时游离抗体浓度，nM |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | 解离常数，与浓度同单位，nM |

同一种互不协作的结合位点在平衡下，结合与解离平衡得到占据率。假设游离浓度已知且探针不明显耗尽。Kd 为 2 nM 时，c 为 2 nM 得 0.5，18 nM 得 0.9；图中使用这一参数。

## 保存现场，也给探针留出通路

固定的任务是尽可能保留取样时的细胞结构。可以把它理解为给正在工作的房间拍一张分子层面的快照，但固定剂本身会改变房间里的连接关系。交联型固定会形成新的化学连接，既能保留结构，也可能遮住表位；沉淀型处理会改变蛋白和膜的状态。选择时要同时观察目标信号与细胞形态，不能把一种条件得到的亮度直接当成另一种条件下的蛋白量。处理组和对照组若采用不同固定时间，那么后面的强度差便混合了生物变化与保存方式。

通透是为抗体打开到达细胞内部的路径。细胞膜像一道选择性很强的边界，而抗体是相对大的分子；检测核内目标时，探针必须跨过外部和内部障碍。通透太弱会出现“外面亮、里面暗”，通透过强又可能抽提出可溶性组分。观察细胞表面的目标时，保留膜的完整性反而可能是设计的一部分。对三维凝胶中的细胞，还要增加一层距离问题：从材料表面走到深处，比到达玻片上薄薄的一层细胞需要更多时间。沿深度衰减的染色，既可能涉及生物分布，也可能涉及探针到达和光传播。

封闭和洗涤围绕的是未被希望保留的结合。封闭液中的组分占据容易吸附蛋白的位置，降低后来抗体在那里停留的机会；洗涤把游离或较弱结合的组分带走。材料研究中，这一步尤其值得单独看，因为带电表面、疏水区域和多孔支架都可能吸附抗体。一个没有细胞的材料空白，与同样处理但不加一抗的样品，能够把材料发光与二抗相关信号分别显露出来。它们提供的是不同信息，不能因为两者都叫“阴性”就互相代替。

配制工作液时，把“稀释几倍”还原成具体体积会更稳妥。例如储备液浓度是每毫升 1 毫克，需要 500 微升、每毫升 2 微克的工作液，储备液占最终体积的五百分之一，即取 1 微升后补至 500 微升。这里说的是最终总体积，不是在 500 微升稀释液中再加入储备液。小到难以稳定移取的体积，可以先做中间稀释，再按相同守恒关系配制。记录储备浓度、最终体积和稀释液组成，比只记录一个比例更方便后来重现条件。

$$
C_sV_s=C_wV_f,\qquad V_s=\frac{C_wV_f}{C_s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | 储备液浓度，μg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 储备液加入体积，μL |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | 工作液目标浓度，μg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/4d13c340035341c4ed1de3a2.svg) | 最终总体积，μL |

稀释前后抗体质量守恒。体积使用同一单位时换算因子相消。1000 μg/mL 储备液配制 500 μL、2 μg/mL 工作液，需要 1 μL 储备液，补足最终体积。

同一轮实验还需要统一等待时间和样品姿态。玻片局部干燥会让溶质浓缩，边缘可能突然变得特别亮；一个样品先染完后等待很久，另一个立刻观察，也可能经历不同程度的光照和储存变化。安排足够体积覆盖标本、相同的洗涤方式和一致的成像顺序，都是在保护比较的共同条件。对容易脱落的细胞，保存处理前后的全视野记录也很有帮助：最后留下来的细胞是否代表开始时的群体，需要从这些图像中判断。

## 让对照回答具体的问题

一张清楚的图像可以来自清楚的目标，也可以来自稳定的错误结合。检查身份时，最有说服力的办法之一是改变目标本身：例如降低目标表达后，原来的特定空间信号是否相应减弱。另一个办法是用识别不同表位的独立抗体，查看它们是否给出相符的位置变化；还可以用独立检测方式检验目标的存在。选择哪一种取决于样品与研究问题。它们共同的思路是为“这是这个蛋白”增加一条不完全依赖同一识别试剂的证据链。

不加一抗的对照回答的是另一件事：在一抗缺席时，二抗、样品和成像系统会留下什么信号。若这张图很暗，说明这部分背景较低；它没有直接检查一抗会不会结合别的蛋白。未染色样品显示材料、细胞和固定处理带来的自发荧光。已知能出现目标信号的阳性样品则帮助检查整条检测链是否工作。如果所有样品都暗，可以先从阳性样品判断是研究对象变了，还是试剂、表位可及性与显微镜设置出了问题。

做多颜色标记时，每个通道都需要知道自己在看谁。一个强绿色染料的发射尾部可能进入另一个检测窗口；两个来自相同宿主的一抗，也可能被同一种二抗同时识别。只含一种标记的样品可以检查光学串色，按抗体宿主和识别对象安排的对照可以检查免疫试剂交叉结合。这两种交叉现象发生在不同位置，解决办法也不同。前者涉及激发、滤光和采集顺序，后者涉及试剂配对、直接标记或专门的多重染色策略。

下面的真实图像来自人类蛋白图谱，靶标是波形蛋白 VIM，细胞为 ASC52telo，使用的抗体编号为 HPA001762。合并图中的绿色是目标信号，红色显示微管参考结构，蓝色显示细胞核。先单独看绿色图，再回到合并图，就容易看见围绕核区、沿细胞长轴延伸的纤维样结构。红色线条也很鲜明，但颜色鲜明并不能改变它的通道身份。对初学者而言，这一步比一开始计算复杂系数更重要：先从图例确认每个通道的对象，再描述它的空间关系。

![真实 ASC52telo 免疫荧光图。绿：VIM，红：微管，蓝：核；抗体 HPA001762，图像 582878。Human Protein Atlas v26，CC BY 4.0，原图并列添加标题，未从展示图进行蛋白定量。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6e71a572376a74f458c575cb.svg?v=6e71a572376a)

图 2真实 ASC52telo 免疫荧光图。绿：VIM，红：微管，蓝：核；抗体 HPA001762，图像 582878。Human Protein Atlas v26，CC BY 4.0，原图并列添加标题，未从展示图进行蛋白定量。

图谱在 2017 年发表的亚细胞蛋白地图把这样的单细胞观察扩展到上万种蛋白，使“蛋白在哪里”成为可以系统检索的问题。本例保留公开图像的展示形式，用于学习位置与通道，而数值定量使用后面的已知像素数据。原始科研图像若要比较强度，应保留探测器数值、位深、曝光和空间标定；展示用压缩图经过的缩放和显示变换，则属于另一层信息。学习时把这两种用途分清，就能既利用公开图像的丰富形态，又正确组织自己的定量测量。

## 从亮度到位置：先扣背景，再确定分母

核内与胞质的比较从划定区域开始。核染色帮助找到核边界；整个细胞的边界还需要合适的轮廓标记、明场信息或经过检查的分割方法。胞质区域等于细胞区域去掉细胞核，而不是随意在核旁画一个圈。拥挤细胞的环形区域可能混入邻居，细胞突起也可能被一个小圆圈漏掉。如果研究目标本身用于定义区域，弱信号的细胞更容易被排除，最终的平均值就偏向强信号细胞。尽量用独立通道确定位置，再在目标通道读取数值，可以减少这种相互牵扯。

背景扣除为什么要乘面积，可以从像素相加理解。假如一个区域有 100 个像素，每个像素都带着 25 个单位的均匀背景，那么总信号里有 2500 个单位来自背景。积分强度扣除的是这 2500；平均强度则直接减去每像素的 25。核胞质比使用两边的平均值，避免把区域大小混进亮度比较。例如核内平均读数 145、胞质 85、背景 25，扣除后分别为 120 和 60，比值为 2。直接用原始值相除只有约 1.71，背景把两者往相似的方向拉近了。

$$
F_{\rm corr}=F_{\rm sum}-n b,\qquad R_{N/C}=\frac{\overline I_N-b}{\overline I_C-b}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0339704ab48f75ba65258899.svg) | 扣背景后的区域积分强度，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/52a6793f1c59e6ada83931d9.svg) | 原始区域积分强度，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 区域像素数量，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 每像素背景平均值，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/e43c47c5dbb086eb37f5d1ac.svg) | 核胞质平均强度比，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/2b58c6da2c0388feb3f570fa.svg) | 核区域原始平均强度，a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/adf60fadcfb41b6537595116.svg) | 胞质区域原始平均强度，a.u. |

各像素均匀背景相加为 n 倍背景；比值比较扣除后的平均值。假设两区域背景相同、未饱和、胞质校正信号大于零。145、85 和背景 25 得 (145−25)/(85−25)=2；原始比值约 1.706。

核胞质比解决的是相对富集，并不等同于“有多少百分比的蛋白在核内”。后者还需要核与胞质的面积或体积、光学采样方式以及相应的积分信号。在二维图像中，一个核区域很小而平均亮度很高的细胞，核内积分信号仍可能小于大片胞质的积分信号。厚度变化又会影响每个像素累积的光量。研究问题若涉及细胞整体分配，可以在一致的三维采集和分割条件下比较各区室积分；若关注薄层单细胞的定位变化，则清楚定义的平均强度比常常更容易直接解释。

构造实验中，每枚细胞的目标积分信号固定为 10000 个单位，一组主要分布在胞质，另一组更集中到核内。代码先建立独立的几何区域，再按照这个总量分配信号，随后加入背景与噪声，最后从生成的原始图像读回区域平均值。图中的每个点对应一枚细胞，因此你可以同时看到群体差异和个体分散。总信号图接近不变而核胞质比明显改变，直接说明“移动位置”和“增加总量”是两个可以分开的问题。

![程序实际生成并读取像素的构造实验。蓝色为核，橙色为胞质；每点一枚细胞，积分总量接近相同而核胞质比改变。空间标定为 1 μm/像素。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/447f20f02a215c709bcfc204.svg?v=447f20f02a21)

图 3程序实际生成并读取像素的构造实验。蓝色为核，橙色为胞质；每点一枚细胞，积分总量接近相同而核胞质比改变。空间标定为 1 μm/像素。

选择汇总方式也需要保留实验层级。同一培养孔中的几十枚细胞共享培养、染色和成像条件，它们帮助描述这一孔的细胞分布；不同培养批次或独立处理样本则回答结果能否在新的实验中重现。可以先在每个独立样本内计算中位数，再比较样本之间的变化，同时展示细胞分布。把每枚细胞都当作完全独立的实验，会让数据量看上去很大，却没有增加独立处理的次数。记录细胞编号、视野、孔和批次，使这些层级在后来的分析中仍然可见。

## 漂亮图像与可比较图像需要哪些共同条件

曝光相当于收光的时间窗口。在线性范围内，同一个区域收光时间加倍，信号大致随之增加；当探测器达到上限，再强的信号也被记录成同一个最大值。此时高峰被截平，位置比值也会改变。设核内与胞质真实信号为 120 和 60，背景为 25，探测器上限为 255。曝光加倍后，核内本应达到 290，却只能记作 255；胞质仍是 170。再扣除加倍后的背景 50，得到 205 与 120，比值约 1.71。照片可能更鲜艳，测量却丢失了两处原本的差异。

这个例子说明，统一曝光与检查饱和需要一起做。只统一曝光，仍可能让最亮处理组达到上限；只逐张调整到“看起来不错”，又改变了比较尺度。可以先用预实验找到能够覆盖预期强度范围的采集条件，随后固定条件获取比较数据。展示时，同一比较中的图像使用一致的亮度映射，并保留显示范围。若为了观察某个结构另做增强展示，可以把它作为结构图说明其用途，定量仍从保留原始数值的图像进行。

下面的交互实验把核内与胞质真实信号固定住，让你改变曝光、背景和核区域混入胞质的比例。先在正常曝光下增加背景，比较扣除前后；再把曝光提高到使柱顶截平，观察背景扣除为什么救不回已经丢掉的峰值；最后让核区域稍微越过边界，看看核胞质比怎样下降。三个操作分别发生在采集、校正和分割环节，却都可能在最终表格中表现为同一个比值变化。沿着原始信号往回追，才知道应该改哪一步。

## 同一个蛋白分布，为何测出不同的比值？

核内与胞质真实平均信号固定为 120 和 60，探测器上限 255。改变曝光与背景，再尝试把少量胞质混进核区域，沿着原始读数追踪比值变化。

[Figure: 核与胞质的期望信号、实际读数和背景](https://ml-biomat.com/tutorials/experimental-methods/l05/#L05-lab)

![四种测量诊断：位点占据、特异信号与背景之比、曝光饱和、核边界混入胞质。各曲线来自正文明确给出的教学模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f66c538ebe9cf339bc8fed05.svg?v=f66c538ebe9c)

图 4四种测量诊断：位点占据、特异信号与背景之比、曝光饱和、核边界混入胞质。各曲线来自正文明确给出的教学模型。

两种蛋白的颜色重合时，还会遇到“共定位”的问题。可以把两通道同一像素的数值配成一对，考察它们是否一起升高或降低。皮尔逊相关系数衡量这种同步变化，先减去各通道自己的平均值，再比较共同变化与各自波动的大小。若第二通道永远是第一通道的两倍，相关系数为 1，即使两者亮度并不相等。共同出现在一个光学分辨区域内，提供的是空间共现信息；要研究分子直接结合，还需要能够探查更短距离或相互作用的实验设计。

$$
r=\frac{\sum_{i=1}^{m}(x_i-\overline x)(y_i-\overline y)}{\sqrt{\sum_{i=1}^{m}(x_i-\overline x)^2\sum_{i=1}^{m}(y_i-\overline y)^2}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 皮尔逊相关系数，无量纲，范围 −1 至 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 被分析的配对像素数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 配对像素编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/0628201b1fcd40d880b250aa.svg) | 同一位置的两通道像素强度，各通道 a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/8f4280576ddf56a5d99f652b.svg) | 所选区域各通道的平均强度，各通道 a.u. |

先居中再比较共同变化，分母用各自波动大小归一化；两通道都须具有非零方差。x 为 1、2、3、4，y 为 2、4、6、8 时，分子为 10，分母为 10，r=1。它表示像素强度同步变化，不是分子数比例。

计算共定位时，空白区域、相邻像素相关、通道错位和细胞三维形状都会影响结果。一个大面积黑背景可以让许多像素同时很暗，改变整幅图的统计关系；两个上下分开的结构在投影图上也可能重叠。选定与问题相关的区域，检查单通道对照与空间配准，并在需要时分析三维数据，能让系数对应明确的空间问题。对于只关心核转位的实验，核胞质比通常已经直接对应问题，不必因为软件能输出更多系数就把每一个都算一遍。

## 运行完整例子，再把设计带回自己的样品

完整程序输出四组图、每枚构造细胞的测量表、保存原始像素和区域标签的数组，以及数值摘要。运行时可以先打开核胞质比分布图，再沿着表格中的细胞编号回到对应区域，检查这个比值由哪两组像素计算出来。代码把几何区域直接作为已知标签，目的是让背景和读数过程透明；实际图像中，这些标签需要由分割获得，并逐视野检查。把分割单独当作一个有输出可检查的步骤，比把它藏在最终平均值后面更容易发现问题。

### 完整 Python：从原始像素计算蛋白定位

离线运行，导出 40 枚构造细胞的原始数组、区域标签、逐细胞表和四组实际图像。公开图谱图像随示例打包。

```
"""Antibody binding, nuclear localization and image measurement: offline example."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Ellipse,FancyArrowPatch
from PIL import Image

BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text).replace('ASC52 telo', 'ASC52telo')


def response(exposure=1.,background=25.,contamination=0.):
    nucleus=(1-contamination)*120+contamination*60
    n=min(255,exposure*(nucleus+background));c=min(255,exposure*(60+background))
    return (n-exposure*background)/(c-exposure*background)

def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,5.2))
    for ax,indirect in zip(axes,[False,True]):
        ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
        ax.add_patch(Ellipse((5,1.8),3,1,fc=BLUE,ec='none'))
        ax.text(5,.8,T('靶蛋白与可及的表位','Target and accessible epitope'),ha='center')
        ax.plot([5,5,4,5,6],[2.3,3.8,4.8,3.8,4.8],color=AMBER,lw=5)
        if indirect:
            for x in [4.,6.]:
                ax.plot([x,x,x-.6,x,x+.6],[4.8,5.8,6.4,5.8,6.4],color=PURPLE,lw=4)
                ax.scatter([x-.6,x+.6],[6.4,6.4],s=100,marker='*',color=GREEN)
            ax.text(5,7.2,T('间接：一抗识别，带标二抗报告','Indirect: primary recognition, labeled secondary'),ha='center',fontsize=10)
        else:
            ax.scatter([4,6],[4.8,4.8],s=150,marker='*',color=GREEN)
            ax.text(5,6.8,T('直接：识别与发光位于同一抗体','Direct: recognition and label on one antibody'),ha='center',fontsize=10)
            ax.text(5,5.8,T('1941：Coons、Creech、Jones\n荧光化学与特异识别相遇','1941: Coons, Creech and Jones\nFluorescent chemistry meets specific recognition'),ha='center',fontsize=10)
    fig.text(.5,.015,T('原创原理示意；星号代表荧光团，数量不代表真实标记度。','Original mechanism schematic; stars are fluorophores, not measured labeling stoichiometry.'),ha='center',fontsize=9)
    save(fig,'history')
    # Constructed raw images: masks define geometry independently of protein intensity.
    rng=np.random.default_rng(505);yy,xx=np.mgrid[:220,:345]
    cells=np.zeros(xx.shape,int);nuclei=np.zeros(xx.shape,int);truth=np.zeros(xx.shape,float)
    rows=[]
    for i in range(40):
        cy=25+(i//8)*42;cx=25+(i%8)*42
        cell=(xx-cx)**2+(yy-cy)**2<=18**2;nuc=(xx-cx)**2+(yy-cy)**2<=8**2;cyto=cell&~nuc
        ratio=(.6 if i<20 else 2.)*np.exp(rng.normal(0,.12))
        total=10000.;c=total/(cyto.sum()+ratio*nuc.sum());n=c*ratio
        cells[cell]=i+1;nuclei[nuc]=i+1;truth[cyto]=c;truth[nuc]=n
        rows.append([i+1,'control' if i<20 else 'stimulated',ratio,total,int(nuc.sum()),int(cyto.sum())])
    raw=25+truth+rng.normal(0,.8,xx.shape);background=float(raw[cells==0].mean())
    result=[]
    for row in rows:
        i=row[0];nmask=nuclei==i;cmask=(cells==i)&~nmask
        n=raw[nmask].mean()-background;c=raw[cmask].mean()-background
        result.append(row+[float(n),float(c),float(n/c),float((raw[cells==i]-background).sum())])
    with (out/'localization.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['cell_id','group','true_NC_ratio','true_total_au','nuclear_pixels','cytoplasmic_pixels','nuclear_mean_au','cytoplasmic_mean_au','measured_NC_ratio','corrected_total_au']);w.writerows(result)
    np.savez_compressed(out/'images.npz',raw=raw,cell_masks=cells,nuclear_masks=nuclei,true_signal=truth)
    fig,ax=plt.subplots(2,2,figsize=(11,8.2))
    im=ax[0,0].imshow(raw,cmap='magma',vmin=25,vmax=55);ax[0,0].set_title(T('A  构造靶蛋白通道：原始数值','A  Constructed target channel: raw values'))
    ax[0,0].plot([20,70],[200,200],color='white',lw=3);ax[0,0].text(45,191,'50 μm',ha='center',color='white',fontsize=9)
    fig.colorbar(im,ax=ax[0,0],label=T('强度 / a.u.','Intensity / a.u.'),fraction=.035)
    masks=np.zeros((*raw.shape,3));masks[cells>0]=[.8,.5,.24];masks[nuclei>0]=[.18,.5,.65]
    ax[0,1].imshow(masks);ax[0,1].set_title(T('B  独立区域：核（蓝）与胞质（橙）','B  Independent masks: nucleus and cytoplasm'))
    for a in ax[0]:a.axis('off')
    ratios=np.array([r[-2] for r in result]);totals=np.array([r[-1] for r in result])
    for j,colour in enumerate([BLUE,AMBER]):
        indices=np.arange(j*20,(j+1)*20);jitter=np.linspace(-.15,.15,20)
        ax[1,0].scatter(j+jitter,ratios[indices],color=colour,alpha=.8)
        ax[1,1].scatter(j+jitter,totals[indices],color=colour,alpha=.8)
    for a in ax[1]:a.set_xticks([0,1],[T('对照','Control'),T('刺激','Stimulated')]);a.grid(axis='y',alpha=.2)
    ax[1,0].set(ylabel=T('核 / 胞质平均强度比','Nuclear / cytoplasmic mean ratio'),title=T('C  每个点是一枚构造细胞','C  Each point is one constructed cell'))
    ax[1,1].set(ylabel=T('扣背景积分强度 / a.u.','Background-corrected integrated intensity / a.u.'),title=T('D  总量相近，位置改变','D  Similar total, different location'),ylim=(9500,10500))
    fig.tight_layout();save(fig,'localization')
    fig,ax=plt.subplots(2,2,figsize=(11,8.2));c=np.geomspace(.05,100,200);bound=c/(2+c);background_curve=8+.8*c
    ax[0,0].semilogx(c,bound,color=BLUE);ax[0,0].set(xlabel=T('游离抗体浓度 / nM','Free antibody concentration / nM'),ylabel=T('结合占据率','Bound fraction'),title=T('A  单一位点平衡模型，Kd = 2 nM','A  One-site equilibrium model, Kd = 2 nM'))
    ax[0,1].semilogx(c,100*bound/background_curve,color=GREEN);ax[0,1].set(xlabel=T('抗体浓度 / nM','Antibody concentration / nM'),ylabel=T('特异信号 / 背景','Specific signal / background'),title=T('B  背景也随浓度上升的例子','B  Example with concentration-dependent background'))
    exposure=np.linspace(.2,4,200);ax[1,0].plot(exposure,[response(e) for e in exposure],color=AMBER);ax[1,0].axhline(2,color=BLUE,ls='--');ax[1,0].set(xlabel=T('曝光倍数','Exposure multiplier'),ylabel=T('测得核 / 胞质比','Measured N/C ratio'),title=T('C  饱和把真实比值 2 压向 1','C  Clipping compresses a true ratio of 2'))
    q=np.linspace(0,.5,100);ax[1,1].plot(q,[response(contamination=v) for v in q],color=PURPLE);ax[1,1].set(xlabel=T('核区域中混入的胞质比例','Cytoplasm fraction in nuclear region'),ylabel=T('测得核 / 胞质比','Measured N/C ratio'),title=T('D  区域边界也是测量条件','D  Region boundaries affect measurement'))
    for a in ax.flat:a.grid(alpha=.2)
    fig.tight_layout();save(fig,'diagnostics')
    here=Path(__file__).resolve().parent
    fig,ax=plt.subplots(1,2,figsize=(11,6.2))
    for a,name,title in zip(ax,['hpa-vim-asc.jpg','hpa-vim-asc-green.jpg'],[T('A  三通道合并','A  Three-channel merge'),T('B  靶蛋白 VIM：绿色通道','B  Target VIM: green channel')]):
        a.imshow(Image.open(here/name));a.axis('off');a.set_title(title)
    fig.text(.5,.06,T('ASC52telo；HPA001762；绿：VIM，红：微管，蓝：细胞核。\nHuman Protein Atlas v26，图像 582878；CC BY 4.0。','ASC52telo; HPA001762; green: VIM, red: microtubules, blue: nuclei.\nHuman Protein Atlas v26, image 582878; CC BY 4.0.'),ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.14,1,1]);save(fig,'published')
    assert response()==2 and response(4)==1
    assert np.isclose(response(2),205/120)
    summary={'binding':{'half':2/(2+2),'ninety_percent':18/(2+18)},'dilution':{'stock_ul':2*500/1000},'ratios':{'corrected':response(),'raw':145/85,'clipped_two':response(2),'clipped_four':response(4),'contamination_quarter':response(contamination=.25)},'constructed':{'cells':40,'estimated_background':background,'control_median':float(np.median(ratios[:20])),'stimulated_median':float(np.median(ratios[20:])),'mean_total':float(totals.mean())},'correlation':{'proportional':float(np.corrcoef([1,2,3,4],[2,4,6,8])[0,1])}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

第一次练习可以保持噪声和总量不变，只改变核内外分配；第二次把背景提高，比较原始比值与校正比值；第三次降低探测器上限，观察强信号先在哪里失真。程序还画出一个单一位点结合曲线和一个背景随抗体浓度升高的教学情景，帮助理解浓度优化为什么要观察信号与背景的共同变化。图谱图像随示例一同提供，运行不需要联网；它保留真实结构供辨认，代码生成的构造图像则承担数值检查。

还有一个适合材料研究的练习：保持总信号和核内分配不变，只让胞质区域扩大。同样的胞质信号分散到更多像素，平均值会降低，核胞质比便可能上升，而核内积分信号所占比例并没有改变。材料改变细胞铺展时，这个几何效应尤其值得检查。把面积、分区积分和平均强度一起保存，就能区分分子移动与几何稀释；若问题关注局部可用浓度，平均强度变化本身也可以成为有用的观察对象。

把这套思路带到材料表面培养的细胞时，可以先明确目标蛋白与定位问题，再围绕样品建立三个层次的比较：没有细胞的材料帮助识别基底信号，染色对照帮助检查试剂路径，独立培养样本帮助比较生物变化。预实验用于选择固定通透条件、抗体工作浓度和成像范围；正式比较保持这些条件一致，并保存全视野与独立通道。最后把定位图、单细胞分布和样本层级的汇总放在一起，读者便能从看到的结构追到测量的数值，再理解为什么这个变化与研究问题有关。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Coons, Creech & Jones (1941): Immunological Properties of an Antibody Containing a Fluorescent Group](https://www.ebm-journal.org/journals/experimental-biology-and-medicine/articles/10.3181/00379727-47-13084p/pdf)

   荧光抗体的早期特异识别和组织背景问题。
2. [Abcam: Immunocytochemistry protocol](https://www.abcam.com/en-us/technical-resources/protocols/icc-protocol)

   固定、表位保存和通透条件的选择。
3. [Thermo Fisher: Application Verification Testing for Immunofluorescence](https://www.thermofisher.com/us/en/home/life-science/antibodies/antibodies-learning-center/antibodies-resource-library/antibody-application-testing-protocols/immunofluorescence-protocol-adherent-suspension-application-testing.html)

   按检测链设计未染色与无一抗对照。
4. [Uhlén et al. (2016): A proposal for validation of antibodies](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335836/)

   与应用条件匹配的抗体身份验证。
5. [Human Protein Atlas v26: VIM subcellular localization](https://v26.proteinatlas.org/ENSG00000026025-VIM/subcellular)

   ASC52telo、HPA001762、图像 582878 的真实空间结构和通道身份。

   CC BY 4.0; images credited to Human Protein Atlas
6. [Thul et al. (2017): A subcellular map of the human proteome](https://doi.org/10.1126/science.aal3321)

   亚细胞蛋白地图的原始发表；配合图谱历史页阅读。
7. [ImageJ: Colocalization Analysis](https://imagej.net/imaging/colocalization-analysis)

   相关与共现、图像质量、区域和空间配准。
8. [Human Protein Atlas: Licence and citation](https://www.proteinatlas.org/about/licence)

   公开图谱图片的许可和具体图像署名。

   CC BY 4.0 for HPA copyrighted content, with stated third-party exceptions
