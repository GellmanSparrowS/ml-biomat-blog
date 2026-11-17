# 凝胶电泳：在一块胶里分开生物大分子

Source: https://ml-biomat.com/tutorials/experimental-methods/c04/
Language: zh-CN

读懂一张胶图中的位置、亮度和分子状态，让每条带都有合适的参照。

## 一条亮带里，藏着几个不同的问题

把一种酶装进水凝胶，希望它在几天内缓慢释放，首先需要知道释放出来的究竟是什么。溶液里测到蛋白质，可能意味着完整的酶离开了材料，也可能意味着酶已经断成小片段。另一个实验中，你从细胞里纯化一种蛋白质，得到了一管透明液体；肉眼无法看出其中是一个主要成分，还是许多大小相近的分子。凝胶电泳把这种看不见的差别变成空间上的条带：让带电分子在电场推动下穿过含水的高分子网络，迁移快的走得远，慢的留在后面。随后通过染色或荧光检测，把不同位置的分子群显示出来。胶像一张分子旅行的合影，记录的是许多分子的集体分布，而非单个分子的照片。

这张合影可以回答三类问题。条带出现的位置帮助估计分子大小；条带的数量与分布揭示样品中可分辨的组分；经过校准的条带信号则可用于估计某个组分的量。这三件事需要不同的参照。大小参照是同一块胶上已知大小的标记物，定量参照是已知上样质量的同一种蛋白质，身份参照则可能来自抗体识别、质谱或核酸测序。假如两个不同蛋白质恰好走到同一位置，它们会叠成一条带，因此“只有一条带”描述的是这套分离条件下的图像。研究者接下来选择何种验证，取决于想把结论推进到大小、纯度、身份还是功能。

核酸实验也有类似的需求。PCR 是把一段选定 DNA 大量复制的方法，研究者常用胶图检查扩增产物是否集中在预期长度，以及是否存在额外产物。这里的长度常用碱基对 bp 表示，一千个碱基对是 1 kb；蛋白质大小则常用千道尔顿 kDa 表示。DNA 长度和蛋白质质量属于不同的尺子，不能拿同一种标记直接互换。我们会从电场为什么能推动分子讲起，再读一张构造的蛋白质荧光胶图：已知大小的标记物、已知上样质量的标准和未知样品同时出现，使“位置”和“亮度”各有自己的校准依据。

## 从液体中移动的界面，到一块能筛分分子的胶

电泳最初并不依赖今天常见的凝胶板。蒂塞利乌斯在 1937 年研究血清蛋白时，观察的是溶液中随电场移动的界面。蛋白质浓度改变了光的折射，因而可以用光学方法追踪这些界面。他采用平扁的 U 形液体通道，并将装置维持在约 4°C，以减小热对流对分离的干扰。这个问题很直观：如果水本身不断翻动，分子即使有不同的电泳速度，也会被液流重新混在一起。图中的历史原理示意把光学观察和冷却放在一起，是因为分离不只需要一种驱动力，还要设法抑制会抹平差异的运动。

![原创历史原理与现代凝胶示意。左图根据蒂塞利乌斯 1937 年论文解释冷却、光学界面与 U 形液体通道；不是原装置的尺寸复原。右图区分 SDS 作用与二硫键还原。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a4791d351ae3415b4285710e.svg?v=a4791d351ae3)

图 1原创历史原理与现代凝胶示意。左图根据蒂塞利乌斯 1937 年论文解释冷却、光学界面与 U 形液体通道；不是原装置的尺寸复原。右图区分 SDS 作用与二硫键还原。

凝胶提供了另一种组织空间的方法。它含有大量水，同时由连续网络限制大尺度流动；溶解在水中的分子仍能移动，但穿过网络时会遇到与自身大小、形状有关的阻碍。可以把它想成一片细密的灌木丛：同样受到向前的牵引，不同长度和姿态的物体穿行难度不同。这个比喻只用于理解阻力，真正的分子在热运动中不断改变构象，网络孔径也有分布，并不是整齐的金属筛孔。琼脂糖和聚丙烯酰胺是两类常见凝胶材料；调整组成可以改变可分离的尺度窗口，因此选胶首先是选择要看清哪一段分子大小。

电场来自两端电势的差别。带负电的分子受到朝向正极的驱动力，在液体阻力作用下很快进入近似稳定的平均迁移状态。用“电泳迁移率”把这种响应概括起来，就能把电场与平均速度联系起来。这里用速度与迁移率的大小，方向另行说明；真实装置中电场可能在不同区域变化，所以下式是均匀场、固定温度与缓冲条件下的局部模型。它解释了为什么电压、通道长度和运行时间必须一起记录，也提醒我们，面板上的电压数值本身并不等于分子感受到的场强。

$$
E=\frac{V}{L},\qquad v=\mu E,\qquad d=vt
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 平均场强大小，V/m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 电极间电压大小，V。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 对应电压的通道长度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 平均迁移速度大小，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | 固定条件下有效电泳迁移率大小，m²/(V·s)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 在指定方向上的迁移距离，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 运行时间，s。 |

均匀场、近似恒温且迁移率保持不变时，速度与场强成比例。V=100 V、L=0.10 m、μ=2×10⁻⁸ m²/(V·s)、t=1800 s，E=1000 V/m、v=20 μm/s、d=36 mm。

以通道长度 10 cm、电压 100 V 为例，平均场强为 1000 V/m。如果某组分在此条件下的有效迁移率是 2×10⁻⁸ m²/(V·s)，平均速度就是 20 μm/s，30 min 走过 36 mm。这是展示单位如何连接的计算，并非所有蛋白质的通用迁移率。把电压加倍，在迁移率保持不变的模型里会使速度加倍；但电流也会发热，温度又会影响缓冲液和迁移过程。条带弯成笑脸、变宽或不同泳道走得不一致时，应回到热量分布、缓冲条件和上样差异去寻找原因，而不是把弯曲条带当作一种新的分子大小。

## 先决定保留什么结构，再选择怎样跑胶

DNA 的磷酸骨架通常带负电，较长的链同时拥有更多电荷和更大的运动阻力。凝胶提供额外的尺寸筛分，使不同长度的线性片段得以分离。蛋白质则更复杂：组成它的氨基酸不同，表面正负电荷的数量和位置也不同，而且电荷会随 pH 改变。两个质量相同的蛋白质，可以因为形状和电荷不同而在天然电泳中迁移到不同位置。“天然”表示尽量保留原有结构的实验条件，具体复合物能否保持完整，还取决于缓冲液、稀释、运行时间以及结合本身的稳定性。若研究的是一个蛋白质复合物有没有解离，这些条件就是实验问题的一部分。

SDS 是十二烷基硫酸钠，一种带负电的表面活性剂。它与许多蛋白质结合并促进展开，使原来复杂的形状与电荷差异减小，大小于是成为迁移的重要决定因素。SDS-PAGE 中的 PAGE 指聚丙烯酰胺凝胶电泳。把不同蛋白质想成换上近似统一装备的参赛者，有助于理解为什么可以建立大小标尺；实际结合并不对每种蛋白质都完全相同，糖基化等修饰或特殊组成会改变表观迁移。因此胶图给出的是与所选标准比较得到的表观大小，若要追踪修饰或精确质量，可把这一结果与质谱连接起来。

展开与切断共价连接又是两件事。两个蛋白质亚基可以由二硫键连接，即两个硫原子之间形成的共价键；SDS 帮助改变折叠和非共价相互作用，而还原剂用于把二硫键拆开。设两个各为 40 kDa 的亚基只由一个二硫键相连，非还原 SDS 条件下可能出现约 80 kDa 的组分，还原后则集中到约 40 kDa。还原后的亮带包含原先两个亚基的总量，并不是凭空消失一半。这种成对设计把化学处理变成一个问题：连接是否依赖二硫键？若材料又通过其他共价键交联，解释就需要把那些连接也纳入分子结构。

![原创分子状态示意，不是实验结果。A 假定两个 40 kDa 亚基仅由二硫键连接，用非还原与还原 SDS 条件检验连接；B 比较同长度 DNA 的构象，说明线性标记需要匹配比较对象。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5ceb37c8b7043952d6934066.svg?v=5ceb37c8b704)

图 2原创分子状态示意，不是实验结果。A 假定两个 40 kDa 亚基仅由二硫键连接，用非还原与还原 SDS 条件检验连接；B 比较同长度 DNA 的构象，说明线性标记需要匹配比较对象。

高分辨 SDS 胶的历史也与具体生物学问题紧密相连。拉姆利在 1970 年发表的工作研究 T4 噬菌体头部组装过程中的结构蛋白切割；参与这一研究时期的 Jonathan King 后来回顾，能够分清复杂混合物中的蛋白条带，使研究者得以结合遗传突变去寻找缺失或改变的结构组分。这里重要的是比较逻辑：一个改变明确的生物学条件，配上一套能够显示组分变化的分离方法。今天比较材料处理前后的蛋白片段、还原前后的连接或纯化不同步骤的样品，也沿用这种把实验干预与条带变化对应起来的思路。

## 把样品、标记和对照放在同一张图上

一块胶能讲清楚多少事情，往往在上样前就已决定。研究蛋白质纯化时，可把起始液、流穿液、洗涤液和洗脱液按流程排在相邻泳道；研究释放时，可把原始蛋白、材料空白和不同时间点的释放液一起比较。泳道是样品从一个加样孔出发形成的纵向区域，每一道对应一个明确样品。若比较组成，常希望按相同总蛋白量上样；若比较每单位原始培养液的产量，则可能需要按相同原始体积的等效量上样。这两种归一化回答不同问题，应把取样量和稀释关系写进记录，避免用漂亮的等亮条带掩盖真正的产量差别。

标记物应覆盖目标所在的大小区间，而不是只在远处提供几个数字。凝胶浓度较高通常形成更紧密的筛分环境，有利于某些较小分子的分离，却可能使较大的分子难以进入或挤在上方。梯度胶让组成沿迁移方向变化，可以覆盖较宽范围，但校准关系也要由实际标记确认。对于 DNA，先确认比较对象是线性片段还是环状质粒；同样长度的开环、超螺旋和线性 DNA 因形状不同而改变迁移。拿未切开的质粒直接对照线性 DNA 标记，可能把形状差别误读成长度差别。设计一次合适的线性化处理，常比给错误尺子增加小数位更有帮助。

样品的盐、溶剂和体积也会改变出发条件。盐离子参与导电，过多的盐可造成局部电场和发热差异；上样体积很大，会让样品从一个宽区域出发，邻近组分更难分开。许多不连续蛋白电泳体系设有浓缩区域，利用不同离子的迁移行为把起始样品压缩成较窄区域，然后进入分离区域。这类似先把赛跑者整理到同一条起跑线上，再比较速度，但实现它的是缓冲离子的运动和酸碱平衡。更换缓冲体系、凝胶和电极溶液时，要把它们当成一套相互配合的化学系统，而非可以随意拼接的耗材。

运行结束还只是得到分离后的分子分布。不同染料对蛋白质或核酸的结合方式不同，检测的线性范围、背景和灵敏度也不同。荧光成像记录的是发射光所产生的探测器信号；透射扫描中深色染带降低透过光强，进一步定量时可能需要光密度转换。两者不能直接套用相同的灰度减法。本章的完整例子特指线性荧光响应：同一种蛋白质、相同染色条件、尚未饱和的检测器。这样的定义让每一步计算都有明确对象，也使读者知道把方法搬到自己的仪器时，首先应核对哪一段测量关系。

## 先读位置：把迁移距离变成有参照的大小

图中每一个亮带都是由二维高斯分布构造的教学信号，加入固定随机种子的噪声与缓慢变化的背景。它不是实测胶图，但保留了定量分析需要处理的关键结构：标记泳道有五个已知大小的条带，后面依次是空白、20 ng、40 ng、80 ng 标准和未知样品。未知泳道中有一个约 40 kDa 的主带和一个约 25 kDa 的次带。主带的大小与上样质量是两个不同变量；我们故意把“40 kDa”和“40 ng”同时放在图里，是为了练习区分一个分子有多大，以及这一道里有多少这种分子。

![全部为构造荧光数据，固定种子 640。L 为 100、70、40、25、15 kDa 标记；标准上样量为 0、20、40、80 ng，U 中主带 55 ng、次带 12 ng。虚线为起点与参考前沿；位置与亮度分别校准。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0206ebf1eb5c2e434e9d5183.svg?v=0206ebf1eb5c)

图 3全部为构造荧光数据，固定种子 640。L 为 100、70、40、25、15 kDa 标记；标准上样量为 0、20、40、80 ng，U 中主带 55 ng、次带 12 ng。虚线为起点与参考前沿；位置与亮度分别校准。

迁移距离从同一个起点测量，通常取分离区起始线到条带中心的距离。再除以起点到指定参考前沿的距离，得到无量纲的相对迁移距离 Rf。参考前沿并非一种已知大小的蛋白质，而是帮助描述这次运行进度的位置。若所有距离都使用像素，除法会消去像素单位，因此不必先把照片换算成毫米。胶图歪斜时，应先确定正确的泳道方向；标记与样品横向位置差异明显且存在弯曲时，局部标记或重复标记比强行使用全图统一的水平线更合理。

$$
R_f=\frac{d_{\mathrm{band}}}{d_{\mathrm{front}}},\qquad \log_{10}\!\left(\frac{M}{1\,\mathrm{kDa}}\right)=a+bR_f
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2fefa7f4702f6dc2c446e8bb.svg) | 相对迁移距离，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/02a6a84c4c5d4eb323805b4f.svg) | 共同起点至带中心的距离，pixel 或 mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2abe6535cfb35c678786bb92.svg) | 同一起点至指定参考前沿的距离，与分子同单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 按标记物校准的表观蛋白质质量，kDa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | 所选线性范围内经验校准的截距与斜率，均无量纲。 |

距离比消去图像缩放；质量先除以 1 kDa 再取对数。构造模型 a=2.1、b=−1.25，M=40 kDa 给出 Rf≈0.398352。实际由带噪声的标记中心重新拟合，在目标附近插值。

为什么大小要取对数？在选定凝胶的一段有效范围内，蛋白质质量的对数与相对迁移距离常能用直线近似，这是一种由标准物确定的经验校准。图的纵轴写成 log₁₀(M/kDa)，表示先把质量除以 1 kDa 得到数值，再取以 10 为底的对数。把 100 kDa、10 kDa 和 1 kDa 放在这把尺子上，它们对应 2、1 和 0。例子的构造关系是截距 2.1、斜率 −1.25，40 kDa 对应 Rf 约 0.398。程序从带噪声图像中重新定位标记中心，再拟合这条关系，未知主带的反算结果约为 40 kDa。

读大小时值得停下来检查标记点是否沿着一条直线分布。最上方的大分子可能挤在一起，最下方的组分也可能接近前沿，使线性近似变差。此时可缩小校准范围，使用包围目标的标记，或选择更适合的胶；把直线延长到没有标准支持的区域，得到的数字会越来越依赖假定。条带很宽时，中心位置本身也有不确定性。可以比较峰顶、强度加权中心或拟合中心是否一致，并查看重复胶中的位置变化。这样，最终的“约 40 kDa”来自一组可观察的参照关系，而不是从图片上目测一个似乎熟悉的位置。

## 再读亮度：背景、面积和饱和共同决定定量

同样质量的蛋白质若集中成窄带，峰顶可能比宽带更亮。因此定量通常对一个包含整条带的区域积分，把区域内所有像素的信号相加，再扣掉背景。这像计算一座小山的体积，既要看高度，也要看底面覆盖了多大范围。ROI 是感兴趣区域的简称，图中用绿色框圈出目标条带，蓝色框选在它附近、没有明显条带的位置。邻近背景能反映局部染色和照明状况；若背景沿图像变化，就不宜从遥远角落取一个数字扣遍整张胶。区域还应避开邻近泳道和次带，避免把别的组分一起算进去。

$$
S=\sum_{p=1}^{N}(I_p-\bar B)=\sum_{p=1}^{N}I_p-N\bar B
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 背景扣除后的积分信号，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 所选区域的像素编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 积分区域像素数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/44d9fad31d63f36e8d73e778.svg) | 第 p 个像素的荧光计数，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9744967524d2194c13c2ad4e.svg) | 目标位置估计的每像素平均背景，counts。 |

线性荧光响应中，相加收集整条带的信号，再去掉同一区域应有的背景。N=1107、原始总计数 240000、背景 100，净积分为 129300 counts；每像素背景误差 2 会带来 2214 counts 的积分误差。

本例积分框包含 41×27，也就是 1107 个像素。假设这一区域总计数为 240,000，背景平均为每像素 100 counts，背景贡献就是 110,700 counts，净积分为 129,300 counts。背景只估错每像素 2 counts，净积分就会改变 2214 counts；对于很弱的条带，这可能已经是明显比例。程序在条带上下取两个背景小区，因构造背景随行号近似线性变化，对称取样有助于估计条带位置的背景。数据文件同时保存净积分和背景均值，便于区分信号变化究竟来自条带还是背景。

![A、B、D 来自同一构造图像；每个标准一个泳道。C 是独立的连续二维高斯削顶模型，背景 100 counts、最大值 4095，已按曝光时间校正；曲线偏离直线显示丢失计数。D 改变积分区半高，背景与标定保持一致。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/df3740a6064f7e085231103d.svg?v=df3740a6064f)

图 4A、B、D 来自同一构造图像；每个标准一个泳道。C 是独立的连续二维高斯削顶模型，背景 100 counts、最大值 4095，已按曝光时间校正；曲线偏离直线显示丢失计数。D 改变积分区半高，背景与标定保持一致。

净积分仍然是探测器计数，需要已知上样质量的同一种蛋白质来建立质量标尺。程序用空白和三个标准拟合直线，再由未知主带的净积分反算，得到接近 55 ng 的上样质量。若这道样品取自一份稀释液，还要用上样体积换算该溶液浓度，再乘以相应稀释倍数。比如 55 ng 来自 5 μL 上样，浓度就是 11 ng/μL；若上样前进行了两倍稀释，原液对应 22 ng/μL。这里的体积是实际进入泳道的样品体积；若加入上样缓冲液后总体积增加，必须明确浓度究竟指混合前还是混合后的溶液。

$$
S=km+b_0,\qquad \hat m=\frac{S-b_0}{k},\qquad c=\frac{\hat m}{V_s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 净积分信号，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 同一蛋白质、固定曝光和染色条件下的校准斜率，counts/ng。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 标准实际进入泳道的质量，ng。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | 校准截距，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f35e2a884154f04380ef47f1.svg) | 未知样品进入泳道的估计质量，ng。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 对应上样溶液的浓度，ng/μL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 与该质量对应的上样体积，μL。 |

同一种蛋白质在线性范围内以已知质量建立信号标尺。若 k=2200 counts/ng、b₀=500 counts、S=121500 counts，则 m̂=55 ng；Vₛ=5 μL 时 c=11 ng/μL。两倍稀释的原液为 22 ng/μL。实际代码由图像重新估计斜率与截距。

相同质量的不同蛋白质未必染得同样亮，因为染料结合与氨基酸组成等因素有关。若用主带积分除以整道所有条带的积分，得到的是所选检测条件下的信号占比。只有进一步采用相同质量响应等条件，才能把它解释成质量占比。例子特意给主带 55 ng、次带 12 ng，并为两者设定相同响应，因此主带质量比例为 55/67，约 82.1%。真实纯化样品可先报告主要条带的信号比例，再用合适标准、其他检测或质量平衡完善组分定量。若胶底还有小分子片段跑出了成像区域，分母也要相应重新考虑。

曝光过长会产生另一个容易被忽略的问题：检测器达到最大值后，继续增加光子也无法提高像素数值。图中的 12 位探测器示意采用最大值 4095，亮带中心会被削成平顶，按线性关系反算的质量因此偏低。降低显示亮度只能改变观看效果，已经截断的计数不会回来。交互中可以改变上样质量、曝光时间和背景，观察同一个二维高斯条带何时开始削顶，以及曝光校正之后还剩多少偏差。这里采用连续高斯积分的解析模型，避免把某个任意阈值误当作检测器的真实响应曲线。

交互采用一个可以算清楚的形状：条带从中心向四周平滑降低，截平后损失的主要是中心区域。把被记录的净积分除以理想净积分，就得到保留下来的信号比例，再乘以真实质量得到表观质量。下式把这个二维高斯模型的积分结果写出来；它假定背景恒定、积分区覆盖整个条带，因而适合解释削顶本身，与前面有限像素框中的背景估计是两个层次的问题。

$$
A=\kappa mt,\quad H=C_{\max}-B,\quad \hat m_{\mathrm{clip}}=m\begin{cases}1,&A\le H,\\ \dfrac{H}{A}\left[1+\ln\!\left(\dfrac{A}{H}\right)\right],&A>H.\end{cases}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 无背景的理想峰顶计数，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | 峰顶响应系数，20 counts/(ng·s)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 真实上样质量，ng。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 曝光时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 背景之上可记录的信号余量，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/139d2bc88abb1cc4b4d82e6b.svg) | 探测器最大值，4095 counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 恒定每像素背景，counts。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c6ce7831fa820eaf1c2509a4.svg) | 积分并按曝光校正后，用理想线性关系反算的表观质量，ng。 |

对连续二维高斯带，把中心超过 H 的部分截平，再在整个平面积分，得到第二支中的保留比例；ln 表示自然对数。m=100 ng、t=4 s、B=100，A=8000、H=3995，表观质量约 84.61 ng。背景恒定、无其他噪声，积分区完整覆盖条带。

## 一条带何时会被曝光截平

改变质量、曝光与背景。教学模型为连续二维高斯荧光带，峰高系数 20 counts/(ng·s)，最大值 4095。积分后除以曝光时间；先观察正常线性区，再找出削顶后的质量低估。

[Figure: 高斯带曝光与削顶交互图](https://ml-biomat.com/tutorials/experimental-methods/c04/#C04-plot)

选择曝光时，可以同时观察强带与弱带。曝光缩短能保护强带不被截平，但弱带会更接近背景波动。一组不同曝光的图像，可以帮助寻找净积分随曝光近似成比例、反算质量也相对稳定的区间。标准与未知样品要使用一致的响应定义；需要跨曝光比较时，用实际线性关系支持校正。检查原始像素最大值和积分值，比只看经过显示调节的图像更容易发现隐藏在亮带中心的饱和。

## 让一张胶图成为下一步实验的依据

下面的完整程序从生成原始二维计数开始，保留未经显示调节的数组，然后逐步完成标记定位、大小校准、局部背景扣除和质量反算。保存的原始图像数组用于复算，泳道曲线用于查看主带与次带，校准表则保留每道标准的已知质量和实际测得的积分。图中第四个定量面板改变积分区域的高度：区域太窄会截掉条带两侧，逐渐放宽后估计值接近平台。平台说明主要信号已被包括；继续放大到覆盖邻近条带，又会引入新的组分。这种敏感性检查比只展示最终一个数字更能帮助确定合理的分析范围。

### 完整胶图、大小校准和条带定量例子

生成明示的构造二维荧光数据，保存原始数组，输出两种校准、背景分析与削顶诊断。

```
"""Constructed electrophoresis images and quantitative diagnostics; no network needed."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Ellipse

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):
  f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 def text(ax,x,y,z,e,**kw):ax.text(x,y,T(z,e),**kw)
 def arrow(ax,x1,y1,x2,y2,col=B):ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'->','color':col,'lw':2})
 # Original historical mechanism, not an image of an actual historical experiment.
 f,axes=plt.subplots(1,2,figsize=(13.4,5.3),layout='constrained')
 for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
 ax=axes[0];ax.set_title(T('A  1937：追踪溶液中的移动界面','A  1937: Follow a boundary in solution'),loc='left')
 ax.plot([2,2,2.4,6.6,7,7],[6.5,2,1.5,1.5,2,6.5],color='#9ac0cd',lw=30,solid_capstyle='butt');ax.plot([2,2,2.4,6.6,7,7],[6.5,2,1.5,1.5,2,6.5],color=B,lw=1)
 for y in [3.6,4.2,4.8]:ax.plot([1.62,2.38],[y,y],color=R,lw=3)
 arrow(ax,.3,4.2,3.8,4.2,G);text(ax,.15,5.1,'折射率梯度 → 光学界面','Refractive gradient → optical boundary',fontsize=10)
 text(ax,4.2,6.1,'缓冲液','Buffer',ha='center');text(ax,2,7,'−', '−',ha='center',fontsize=20);text(ax,7,7,'+', '+',ha='center',fontsize=20)
 text(ax,.3,.25,'蒂塞利乌斯：冷却至约 4°C，减小热对流\n原理图；溶液中没有凝胶筛网','Tiselius: about 4°C to suppress convection\nPrinciple diagram; no gel sieve in the liquid',fontsize=10)
 ax=axes[1];ax.set_title(T('B  现代凝胶：电驱动 + 分子筛','B  Modern gels: Electric drive + molecular sieve'),loc='left')
 ax.add_patch(Rectangle((1.6,1.4),5.8,5.3,facecolor='#e2edf0',edgecolor=B))
 for x in np.arange(1.8,7.5,.6):ax.plot([x,x],[1.4,6.7],color='#bfd3da',lw=.6)
 for y in np.arange(1.6,6.7,.5):ax.plot([1.6,7.4],[y,y],color='#bfd3da',lw=.6)
 for x in [2.7,4.5,6.3]:ax.add_patch(Rectangle((x-.45,6.2),.9,.5,fc='#fcfbf7',ec=B))
 for x,y in [(2.7,4.9),(2.7,3),(4.5,4.4),(4.5,2.1),(6.3,3.7)]:ax.plot([x-.4,x+.4],[y,y],lw=8,color=R)
 arrow(ax,8.4,6.3,8.4,2);text(ax,8.7,4,'向正极','Toward +',rotation=90,va='center')
 text(ax,1.8,.25,'SDS 改变蛋白质的电荷与形状\n还原剂另行切断二硫键','SDS changes protein charge and shape\nA reducing agent separately breaks disulfides',fontsize=10)
 save(f,'history-mechanism')
 # Constructed raw fluorescence image: all lanes share detector and dye response.
 rng=np.random.default_rng(640);yy,xx=np.mgrid[:360,:390];origin,front=25.,335.;xs=np.array([45,105,165,225,285,345]);masses=np.array([100,70,40,25,15.]);rf=(2.1-np.log10(masses))/1.25;ys=origin+(front-origin)*rf
 center=lambda m:origin+(front-origin)*(2.1-np.log10(m))/1.25
 raw=100+.03*yy+np.zeros_like(xx,dtype=float)
 def band(x,y,ng):return 20*ng*np.exp(-.5*((xx-x)/6)**2-.5*((yy-y)/3)**2)
 for y in ys:raw+=band(xs[0],y,35)
 loads=np.array([0,20,40,80,55.])
 for x,m in zip(xs[1:],loads):raw+=band(x,center(40),m)
 raw+=band(xs[-1],center(25),12);raw=np.round(np.maximum(0,raw+rng.normal(0,3,raw.shape))).astype(np.uint16)
 yc=int(round(center(40)));xhalf=20;yhalf=13
 def measure(x,y):
  cy=int(round(y));roi=raw[cy-yhalf:cy+yhalf+1,int(x)-xhalf:int(x)+xhalf+1].astype(float)
  strips=np.concatenate([raw[cy-24:cy-17,int(x)-xhalf:int(x)+xhalf+1].ravel(),raw[cy+18:cy+25,int(x)-xhalf:int(x)+xhalf+1].ravel()]);bg=float(strips.mean())
  return float(roi.sum()-roi.size*bg),bg
 results=np.array([measure(x,center(40)) for x in xs[1:]]);coef=np.polyfit(loads[:4],results[:4,0],1);estimate=(results[-1,0]-coef[1])/coef[0]
 # Locate ladder maxima from local profiles, then estimate size in the same gel.
 detected=[]
 for y in ys:
  profile=raw[:,25:66].mean(axis=1);window=np.arange(int(y)-6,int(y)+7);detected.append(window[np.argmax(profile[window])])
 detected=np.array(detected);fit=np.polyfit((detected-origin)/(front-origin),np.log10(masses),1)
 uprofile=raw[:,325:366].mean(axis=1);win=np.arange(yc-8,yc+9);uy=int(win[np.argmax(uprofile[win])]);mass_est=10**np.polyval(fit,(uy-origin)/(front-origin))
 f=plt.figure(figsize=(13.6,7.5),layout='constrained');gs=f.add_gridspec(2,2,width_ratios=[1.1,1]);ax=f.add_subplot(gs[:,0]);im=ax.imshow(raw,cmap='magma',vmin=90,vmax=1800,origin='upper');ax.set_xticks(xs,['L','0','20','40','80','U']);ax.xaxis.tick_top();ax.set_xlabel(T('标准 / ng；U = 未知样品','Standards / ng; U = unknown'));ax.xaxis.set_label_position('top');ax.set_ylabel(T('图像行 / pixel','Image row / pixel'));ax.set_title(T('A  构造的原始荧光图','A  Constructed raw fluorescence image'),loc='left',pad=48)
 ax.axhline(origin,color='white',lw=.8,ls='--');ax.axhline(front,color='white',lw=.8,ls='--');ax.add_patch(Rectangle((325,yc-yhalf),41,27,fc='none',ec='#76dccb',lw=1.6));f.colorbar(im,ax=ax,shrink=.7,label=T('探测器计数','Detector counts'))
 ax=f.add_subplot(gs[0,1]);dx=(detected-origin)/(front-origin);ax.scatter(dx,np.log10(masses),c=B);grid=np.linspace(0,.85,100);ax.plot(grid,np.polyval(fit,grid),color=B);ax.scatter((uy-origin)/(front-origin),np.log10(mass_est),c=R,zorder=4);ax.annotate(f'U: {mass_est:.1f} kDa',((uy-origin)/(front-origin),np.log10(mass_est)),xytext=(.5,1.85),arrowprops={'arrowstyle':'->','color':R});ax.set(xlabel=T('相对迁移距离 Rf','Relative migration Rf'),ylabel='log₁₀(M / kDa)',title=T('B  同一块胶的大小校准','B  Size calibration on the same gel'))
 ax=f.add_subplot(gs[1,1]);ax.plot(np.arange(360),uprofile,color=R);ax.axvspan(yc-13,yc+13,color=G,alpha=.18);ax.axvline(center(25),color=B,ls=':');ax.set(xlabel=T('图像行 / pixel','Image row / pixel'),ylabel=T('泳道平均计数','Lane-mean counts'),title=T('C  未知泳道：40 kDa 主带与 25 kDa 次带','C  Unknown lane: 40 kDa major, 25 kDa minor'))
 save(f,'gel-size')
 # Analytic integration of a clipped two-dimensional Gaussian band.
 def apparent(m,t,bg):
  amp=20*np.asarray(m)*t;cap=4095-bg;ratio=np.ones_like(amp,dtype=float);mask=amp>cap;ratio[mask]=cap/amp[mask]*(1+np.log(amp[mask]/cap));return np.asarray(m)*ratio
 f,ax=plt.subplots(2,2,figsize=(13.6,8),layout='constrained')
 crop=raw[yc-27:yc+28,320:371];ax[0,0].imshow(crop,cmap='magma',vmin=90,vmax=1800,extent=(320,371,yc+28,yc-27));ax[0,0].add_patch(Rectangle((325,yc-13),41,27,fc='none',ec=G,lw=2));
 for y in [yc-24,yc+18]:ax[0,0].add_patch(Rectangle((325,y),41,7,fc='none',ec=B,lw=2))
 ax[0,0].set(xlabel=T('图像列 / pixel','Image column / pixel'),ylabel=T('图像行 / pixel','Image row / pixel'),title=T('A  绿色积分区；蓝色背景区','A  Green integration; blue background'))
 ax[0,1].scatter(loads[:4],results[:4,0]/1000,c=B);ax[0,1].plot([0,85],np.polyval(coef,[0,85])/1000,color=B);ax[0,1].scatter(estimate,results[-1,0]/1000,c=R);ax[0,1].annotate(f'U = {estimate:.2f} ng',(estimate,results[-1,0]/1000),xytext=(12,155),arrowprops={'arrowstyle':'->','color':R});ax[0,1].set(xlabel=T('同一蛋白质的上样质量 / ng','Loaded mass of the same protein / ng'),ylabel=T('净积分 / 10³ counts','Net integral / 10³ counts'),title=T('B  背景扣除后反算质量','B  Infer mass after background subtraction'))
 ml=np.linspace(0,200,201)
 for t,c in [(1,B),(4,R),(8,Y)]:ax[1,0].plot(ml,apparent(ml,t,100),c=c,label=f'{t} s')
 ax[1,0].plot(ml,ml,'--',c='#6f7883',label=T('理想线性','Ideal linear'));ax[1,0].legend();ax[1,0].set(xlabel=T('真实上样质量 / ng','True loaded mass / ng'),ylabel=T('按曝光校正的表观质量 / ng','Exposure-corrected apparent mass / ng'),title=T('C  12 位探测器削顶造成低估','C  Clipping by a 12-bit detector causes underestimation'))
 widths=np.arange(2,23);integ=[]
 for w in widths:integ.append((raw[yc-w:yc+w+1,325:366].astype(float).sum()-(2*w+1)*41*results[-1,1]-coef[1])/coef[0])
 ax[1,1].plot(widths,integ,c=G);ax[1,1].axhline(55,c=R,ls='--');ax[1,1].set(xlabel=T('积分区域半高 / pixel','Integration half-height / pixel'),ylabel=T('未知样品估计质量 / ng','Estimated unknown mass / ng'),title=T('D  积分区太窄会漏掉带的两侧','D  A narrow region misses band tails'))
 save(f,'quantitation')
 f,axs=plt.subplots(1,2,figsize=(13.6,5.6),layout='constrained')
 for ax in axs:ax.set(xlim=(0,10),ylim=(0,9));ax.axis('off')
 ax=axs[0];ax.set_title(T('A  二硫键连接的两个 40 kDa 亚基','A  Two 40 kDa subunits joined by a disulfide'),loc='left')
 for x in [2,7]:ax.add_patch(Circle((x,7),.8,fc='#b9dbe3',ec=B));text(ax,x,7,'40','40',ha='center',va='center')
 ax.plot([2.8,6.2],[7,7],c=Y,lw=3);text(ax,4.5,7.3,'S—S','S—S',ha='center');arrow(ax,2.5,5.6,2.5,4.7);arrow(ax,7,5.6,7,4.7)
 for x,label,y in [(2.5,T('非还原 SDS','Nonreducing SDS'),3.9),(7,T('还原 SDS','Reducing SDS'),2.1)]:
  ax.add_patch(Rectangle((x-.75,1.2),1.5,3.4,fc='#e2edf0',ec=B));ax.plot([x-.5,x+.5],[y,y],lw=9,color=R);text(ax,x,.6,label,label,ha='center',fontsize=10)
 text(ax,.2,3.9,'80 kDa','80 kDa',fontsize=10);text(ax,8,2.1,'40 kDa','40 kDa',fontsize=10);text(ax,.3,8.2,'构造关系示意；假定亚基无其他共价交联','Constructed relationship; no other covalent crosslinks',fontsize=9)
 ax=axs[1];ax.set_title(T('B  同样长度的 DNA 可以有不同形状','B  DNA of equal length can have different shapes'),loc='left')
 ax.add_patch(Ellipse((2,6.7),2.4,1.4,fill=False,ec=B,lw=2));text(ax,2,5.4,'开环','Open circular',ha='center')
 x=np.linspace(0,2*np.pi,200);ax.plot(6.8+1.2*np.cos(x),6.7+.35*np.sin(3*x),c=R,lw=2);text(ax,6.8,5.4,'超螺旋','Supercoiled',ha='center')
 ax.plot([1,8],[3.4,3.4],color=G,lw=2);text(ax,4.5,2.5,'线性化后再与线性标记比较','Linearize before comparison with a linear ladder',ha='center',fontsize=10)
 text(ax,.4,.6,'形状改变摩擦与穿孔方式\n迁移快慢还取决于胶和实验条件','Conformation changes drag and pore passage\nMigration also depends on gel and run conditions',fontsize=10)
 save(f,'molecular-forms')
 np.savez_compressed(a.output/'constructed_gel.npz',raw_counts=raw,lane_centers=xs,origin=origin,front=front)
 np.savetxt(a.output/'ladder.csv',np.c_[masses,detected,(detected-origin)/(front-origin)],delimiter=',',header='mass_kDa,image_row_px,Rf',comments='')
 np.savetxt(a.output/'quantitation.csv',np.c_[loads,results],delimiter=',',header='true_mass_ng,net_integral_counts,background_counts_per_pixel',comments='')
 np.savetxt(a.output/'unknown_profile.csv',np.c_[np.arange(360),uprofile],delimiter=',',header='image_row_px,mean_counts',comments='')
 summary={'estimated_mass_kDa':float(mass_est),'estimated_load_ng':float(estimate),'calibration_slope_counts_per_ng':float(coef[0]),'calibration_intercept_counts':float(coef[1]),'image_max_counts':int(raw.max()),'ideal_Rf_40kDa':float((2.1-np.log10(40))/1.25),'field_V_per_m':1000.,'speed_um_per_s':20.,'distance_30min_mm':36.,'clipped_100ng_4s_apparent_ng':float(apparent(100.,4.,100.)),'target_mass_fraction_equal_response':55/67,'roi_pixels':41*27,'unknown_background_counts_per_pixel':float(results[-1,1])}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

如果把程序用于自己的荧光胶图，先替换原始数组，并核对像素位深、零点、饱和值以及是否已做过相机背景校正。随后把标记大小、泳道位置、起始线和前沿位置改成实际记录；用已有标准检验大小拟合的范围，再选择与未知条带相匹配的定量标准。自动检测峰的位置仍需要回到图像核对，因为气泡、灰尘或局部染色缺陷也可能形成亮点。保留全图、记录裁切范围与泳道对应关系，可以让另一个人顺着同一套分析看懂结果，而不必猜测被截掉的区域原来是什么。

回到开头的酶释放问题，若释放液的主带位置与原始酶相近，并且主带质量随时间增加，下一步可把它与催化活性测量连接，询问释放出来的分子是否仍能工作；若低大小条带逐渐增加，则可以设计保存条件、蛋白酶抑制或材料相互作用的比较，寻找片段出现的原因。不同材料应包含材料空白，因为溶出的组分可能影响背景、染色或上样条件。研究纯化时，还可把各组分的浓度乘以总体积，估算每一步回收的量，再比较目标带是否在提高纯度的同时大量损失。这样，胶图中的一条带会自然地引出一个能检验的实验决定。

重复也要围绕这个决定安排。同一张图重复圈选，主要反映分析方法的敏感性；同一样品重复上样，增加了上样和运行差异；不同批次的蛋白制备或独立材料样品，才进一步包含制备与生物学差异。把这些重复混在一起算一个标准差，会让误差条失去清晰含义。对准备继续用于结合实验的蛋白质，可以先用电泳核对组分和降解，再以尺寸排阻检查溶液中的聚集状态，最后进入等温滴定量热或表面结合测量。每种方法观察的对象不同，连在一起才形成从样品是什么、状态如何，到它怎样参与研究过程的完整线索。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Tiselius (1937): Electrophoresis of serum globulin](https://pmc.ncbi.nlm.nih.gov/articles/PMC1267100/)

   1937 年原文第 1464–1465 页：U 形液体通道、4°C 冷却与光学界面。
2. [King (2022): Using T4 genetics and Laemmli’s development of high-resolution SDS gel electrophoresis](https://pmc.ncbi.nlm.nih.gov/articles/PMC9576892/)

   参与者回顾高分辨凝胶与 T4 结构蛋白研究。

   CC BY 4.0 article; historical reference only, no article artwork reproduced.
3. [Thermo Fisher: Overview of electrophoresis](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-electrophoresis.html)

   天然与 SDS 条件、孔径、浓缩及凝胶选择。
4. [Bio-Rad: A Guide to Polyacrylamide Gel Electrophoresis and Detection](https://www.bio-rad.com/webroot/web/pdf/lsr/literature/Bulletin_6040A.pdf)

   场强与焦耳热、同胶大小校准、染色响应和定量。
5. [QIAGEN: DNA analysis using analytical gels](https://www.qiagen.com/en-gb/knowledge-and-support/knowledge-hub/bench-guide/dna/analysing-dna/dna-analysis-using-analytical-gels)

   DNA 构象、凝胶浓度、样品与缓冲液条件。
6. [ImageJ: Analyze menu and gel analysis](https://imagej.net/ij/docs/menus/analyze.html)

   原始灰度、泳道曲线、区域积分与背景。
