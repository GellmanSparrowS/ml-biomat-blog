# 降解实验：材料如何随时间改变

Source: https://ml-biomat.com/tutorials/experimental-methods/e03/
Language: zh-CN

沿着分子断链、质量流失与碳的去向，理解材料的结构变化和功能寿命。

## 材料什么时候失去作用，又什么时候真正离开

可吸收缝线需要在组织愈合期间维持拉力，随后逐渐被处理；组织工程支架要给细胞提供起初的支撑，又为新生组织腾出空间；可降解包装则面对堆肥、土壤或水体等不同环境。这些用途都与降解有关，关心的时间却不完全相同。一根缝线可能尚未明显变轻，已经失去很多承载能力；一片薄膜可能碎成小片，却仍以聚合物形式留在环境中。设计降解实验，首先要确定希望追踪的是化学连接、材料完整性、功能保持，还是物质最终去向。

把一条长项链剪成两段，是理解这件事的好起点。珠子总数没有减少，链的条数却从一条变成两条，平均每条链变短了。若短链仍留在原来的样品中，天平几乎看不出变化；等它们变得足够小、能够溶解并迁移出去，样品质量才开始下降。高分子降解中的断链、可溶片段生成和片段离开，常常按照不同的时间进程发生。因此，质量曲线与分子量曲线共同测量，会比只记录“剩下多少克”更早地揭示材料内部变化。

本章把几个常混在一起的词拆开使用。降解侧重化学结构或大分子连接的改变；侵蚀描述物质从材料中离开，表现为质量或尺寸减少；碎裂描述整体分成较小块；矿化则关注有机碳转成二氧化碳等无机产物的过程。在具体环境中，它们可能相互促进，也可能不同步。材料在酶液中失去质量，与在堆肥中完成生物转化，所测对象和证据都不同。把名称对应到实际测量，可以让研究问题更清楚。

一个完整的降解研究通常保留三条线索：样品本身的质量、形态和力学状态，内部链的尺寸或化学变化，以及进入外液或气相的产物。根据用途选择其中的关键指标，再安排取样时间和环境条件。本章用随机断链的教学模型解释为什么分子变短可以早于失重，用真实凝胶图像观察酶作用后的形态变化，并用碳核算说明矿化实验的分母。最后，代码把这些过程分别画出来，帮助你为自己的材料选对测量组合。

## 水、酶和扩散，怎样共同决定材料的变化

许多聚酯的主链含有酯键。水参与水解反应后，一个原有连接被拆开，产生新的链端，长链逐渐变成较短的片段。反应速度受温度、酸碱条件、链的化学结构和局部环境影响。蛋白质或某些多糖网络则可以被适合的酶切割。酶是具有催化功能的生物大分子，它需要接触能够识别的结构，才能促进相应反应。材料中有可切割的键，只说明存在一条可能路径；水或酶能否到达这些位置，同样决定实验中观察到的速度。

可以把材料看成一座建筑：水和酶是需要进入楼内的作用物，切割连接是发生在房间里的反应，生成片段则需要沿通道离开。若水很快进入整个样品，而反应相对慢，内部许多位置可能同时发生断链，形成体相降解。若作用物只能到达靠近表面的区域，或在进入深处之前已迅速反应，变化可能集中在外层，表现出表面侵蚀特征。这些模式不是固定贴在某种聚合物名字上的标签，还与尺寸、孔隙和环境有关。

一九九五年，Grizzi 等人比较了同一批聚乳酸制成的不同尺寸器件，研究水解过程中反应和扩散的关系。较大的样品内部可以积累酸性降解产物，使内部反应加快；较小结构更容易让产物向外扩散，行为因而不同。这个研究提醒我们，表面积更大并不总能推出“降解一定更快”。图中的大小样品示意把产物排出的路径画出来：几何尺寸既改变进入的距离，也改变反应产物能否积累，两个方向的影响需要一起考虑。

![原创机制与历史示意：一次主链断裂增加分子数量；不同尺寸改变产物扩散距离。1995 年 Grizzi 等的尺寸比较将聚乳酸降解与反应—扩散耦合联系起来，图中箭头用于说明过程，不表示实测通量。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d689fe09bb7d6fbf2850a903.svg?v=d689fe09bb7d)

图 1原创机制与历史示意：一次主链断裂增加分子数量；不同尺寸改变产物扩散距离。1995 年 Grizzi 等的尺寸比较将聚乳酸降解与反应—扩散耦合联系起来，图中箭头用于说明过程，不表示实测通量。

对于酶促降解，酶的尺寸、吸附和活性还会带来额外限制。多孔凝胶可能让酶更容易接近内部，致密网络则可能主要在外层受到作用。酶浓度常用质量浓度或活性单位表示，两者含义不同：同样一毫克不同批次酶制剂，催化活性未必相同。记录酶种类、活性定义、保存与更换条件，有助于解释实验之间的差异。还可以设置没有酶的相同缓冲液对照，分开观察水解、溶解和酶参与后的额外变化。

材料本身的历史也会留下影响。结晶区中的链排列较紧密，无定形区域更无序，水进入和链运动可能不同；加工过程改变结晶、取向和残余应力，灭菌过程也可能改变初始分子量。比较两种材料时，仅写出相同化学名称还不够，应同时记录牌号、分子量分布、结晶状态、尺寸与制备过程中的关键条件。对生物材料而言，降解研究的起点最好就是实际使用前的材料状态，这样功能变化的时间才有明确参照。

## 质量、链长和功能：三个互相补充的读数

称重最容易理解，也最容易混入别的变化。若要计算聚合物干质量损失，应将每个时间点样品按一致程序清洗、去除外部残留并干燥，再与初始干质量比较。湿凝胶的重量同时受到含水量变化影响，因而需要把湿质量变化单独命名。填料脱落、盐沉积、蛋白吸附和容器残留，也会改变天平读数。先列出样品中哪些物质可能进入或离开，再选择适当空白和组成校正，才能让质量差对应研究目标。

$$
L_m(t)=1-\frac{m_d(t)}{m_d(0)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/99da358d7cf8b7d2ecc3cb0b.svg) | 时间 t 的干质量损失比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/083a973ce5ea6d3e3795e784.svg) | 时间 t 按同一清洗、干燥条件测得的剩余干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce9c3374598b0bc90f891f70.svg) | 相同质量定义下的初始干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 浸泡或暴露时间，本例为 d。 |

用初始质量减剩余质量再除以初始质量，得到流失的比例。初始 100 mg、剩余 80 mg 给出 Lm=0.20，即 20%。盐、填料与残留液体应按研究对象校正。

一百毫克初始干样品在某个时点剩下八十毫克，干质量损失就是百分之二十，质量保持率为百分之八十。如果表面还留了十毫克盐，未校正的结果会把质量损失低估为百分之十；若清洗时丢掉了一块仍然未溶解的碎片，又会把可回收材料的损失混进侵蚀结果。对于容易碎裂的材料，可在取样时收集可见碎片和过滤截留物，并分别记录它们的去向。这样的分类能帮助判断材料是变成溶解片段，还是变成了更小的固体。

分子量测量关注链的大小。数均摩尔质量可以理解为总分子质量按分子条数平均；同样数量的重复单元被分成更多条链，平均值就会下降。下面用数均聚合度表示平均每条链包含多少重复单元，不必先处理摩尔这个计数单位。一百条各含一百个单元的链，共有一万个单元。若每条恰好切一次，总链数变成二百条，平均链长从一百降为五十，而重复单元总量仍然是一万个。

$$
\overline{N}_n=\frac{N_{\rm units}}{N_{\rm chains}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e1867b609e4ab077116615bd.svg) | 数均聚合度，即每条链平均含有的重复单元数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bf2c4bb71bb69b11da8c031e.svg) | 计入样本的重复单元总数，无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/67fcf314cf72502074519d11.svg) | 同一分子群体的链条数，无量纲计数。 |

把全部重复单元分给全部链条。1000 条各含 100 个单元的链共有 100000 个单元；若每条链各断一次而全部片段仍保留，链数增至 2000，平均链长降到 50，聚合物质量仍为初始值。

体积排阻色谱可以帮助观察可溶聚合物的分子量分布，但送进仪器的究竟是哪一部分，决定了结果的含义。若只分析残留固体溶解后的组分，已经进入外液的小片段就没有被计入；若只分析外液，看到的又主要是能够逃离材料的部分。网络材料还可能难以直接溶解，需要选择适合的化学分析、溶胶部分或其他结构指标。报告时写清楚分析对象，才能把“残余材料中的平均链长”与“全部产物的平均链长”区分开。

功能测量则回到材料为什么被使用。缝线可以追踪断裂力，承重支架可以追踪压缩模量或疲劳性能，屏障膜可以追踪完整性与渗透。每次力学测量应尽量保持含水、温度和加载条件一致，因为这些因素本身就会改变响应。某些材料早期链长下降但质量保持，承载性能可能已经发生变化；另一些材料吸水变软后又因结晶或结构重排出现不同趋势。把功能曲线与质量、链长放在同一时间轴上，才能看出实际使用窗口。

## 让时间点、对照和环境组成一个实验

初始可溶物的洗脱可以通过前处理对照识别。一组使用充分提取并重新平衡的材料，另一组保留实际制备后状态，再比较早期外液组成和干质量变化。如果差异主要集中在最初阶段，就可以进一步检查残留添加剂或未连网聚合物的贡献。前处理本身也可能改变材料结构，因此应保留两组起始状态的测量，而不是默认洗过以后只减少了某一种成分。

先确定环境与用途的关系。研究植入材料的水解，可以选择有明确酸碱度和离子组成的水溶液；研究蛋白网络被酶作用后的变化，需要定义酶及其活性；研究堆肥中的生物转化，则需要相应的接种物、温湿度和气体交换。实验条件应直接回答设定的问题。把一个高温水解实验得到的时间原样换成体内存留时间，会跳过温度、酶、传质和组织反应等变化；更有用的做法是先建立相同机制下的比较，再用目标环境验证关键时间段。

取样常常是破坏性的：干燥会改变水凝胶，色谱需要溶解材料，拉伸可能拉断样品。因此，可以为每个时点预留独立样品，并把制备批次分散到不同时间组，而不是把第一批全用于早期、第二批全用于晚期。初始时点也应有真实测量，用来确认制备与预处理后的状态。若希望连续观察同一份样品，可选择不会明显改变状态的成像或尺寸测量，再与独立样品的破坏性分析对应。

时间点应围绕变化过程安排。早期可能先出现可溶物洗脱或吸水，中期发生明显断链，后期才大量失重。只在开始和结束称量，会把这些过程压成一个百分数。可以先用少量样品做较密的探索性观察，找到链长、形态或力学变化开始加快的区间，再在正式比较中增加这些区间的取样。对于很慢的过程，还应留出足够长的观察窗口；对于很快的酶促过程，取样和终止反应所需时间也要纳入记录。

外液更换会改变实验。保留同一份液体有利于累积产物和进行物质核算，却可能造成酸性产物积累、酶失活或营养耗尽；定期换液能维持某些外部条件，却会带走产物并改变反馈。两种设计都可以回答具体问题，但应记录换液时间、体积及采样比例。对于会自催化的聚酯，外液酸碱度与材料内部酸碱度也未必相同，因此稳定的浴液读数不能自动说明样品内部环境完全不变。

加速实验应保留机制检查。升温可以缩短等待时间，但跨越玻璃化转变、改变结晶或使酶失活，都可能改变控制过程。可以比较多个温度下的形态、产物和分子量变化是否具有一致顺序，再讨论温度依赖。单一高温曲线即使十分平滑，也不能独自确定另一种环境的寿命。对于材料筛选，加速条件很适合在明确范围内比较配方；对于使用寿命，则需要把目标条件下的观测接入同一个证据链。

## 把链剪短，为什么天平还没有明显变化

理解平均值时，还要记住链长是一种分布。两份材料即使具有相同数均长度，也可能一份包含许多短链和少量很长的链，另一份则集中在较窄范围。它们的可溶比例、缠结和承载表现可能不同。程序保留每一种长度的片段数量，并把数量转换成相应质量比例，所以既能看平均值，也能查看小片段逐渐积累的过程。分布图把单一平均数遮住的信息重新展开。

教学模型从很多条相同长度的线性链出发，每条含一百个重复单元。各个连接以相同的固定速率独立发生切割，随着时间增加，已切断的连接比例逐渐上升。这里先把重复单元当作质量相同的珠子，忽略真实水解中链端组成的微小质量变化，使注意力集中在“条数增加”和“物质离开”这两个过程。模型可以精确计算不同长度片段的期望数量，无需把随机噪声误当成机制。

$$
p(t)=1-e^{-kt},\qquad \overline{N}_n(t)=\frac{N_0}{1+(N_0-1)p(t)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9b836c2bf1155191ac0f8ab3.svg) | 一根初始主链键到时间 t 已被切断的概率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 各键独立、同速断裂模型中的速率常数，d^{-1}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 暴露时间，d。 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | 每条初始线性链的重复单元数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9197ac85a3550d73ddda69d0.svg) | 计入全部片段的总体数均聚合度，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数函数的底数，无量纲。 |

N0 个单元有 N0−1 根连接键，每次切断使片段数加一。大量相同初始链的平均片段数为 1+(N0−1)p。N0=100、p=0.1 时平均产生 10.9 个片段，数均聚合度为 100/10.9=9.174。该模型不包含自催化或位置差异。

模型还规定，长度不超过八个单元的片段可以立即进入外液，较长片段暂时保留。这个阈值是用于解释分离过程的教学设定，不是所有聚合物共享的溶解界限。真实溶解与迁移会受到化学结构、温度和相互作用影响，也需要时间。先采用明确阈值，可以直接看到断链已经制造了很多小分子，而其中只有一部分达到离开条件；改变阈值则能显示相同断链速率为什么可能产生不同失重曲线。

![构造的独立断链模型及单独的球体表面侵蚀模型。A 的平均链长均相对初始长度 100 归一化；B 按长度类别计质量；C 只改变最大可溶长度；D 只改变初始半径。各图帮助区分分子、质量、溶解与几何效应。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e0bac4b0f9a01fef1b6cd68c.svg?v=e0bac4b0f9a0)

图 2构造的独立断链模型及单独的球体表面侵蚀模型。A 的平均链长均相对初始长度 100 归一化；B 按长度类别计质量；C 只改变最大可溶长度；D 只改变初始半径。各图帮助区分分子、质量、溶解与几何效应。

当每个连接被切断的概率为零点一时，一条初始长度一百的链平均产生十点九个片段，全部片段的数均长度约为九点一七四；初始数均长度为一百，因此平均链长只剩约百分之九点一七。与此同时，按八单元阈值计算，材料仍保留约百分之七十四点三八的重复单元质量。两条曲线差别很大，却来自同一个质量守恒模型。它说明断链测量与失重测量各自捕捉不同环节，早期质量稳定也可以伴随显著的分子变化。

图中还区分全部片段和残留片段的平均长度。短片段先离开后，留在固体里的分子群体被筛选过，平均长度会高于把所有片段都包括进去的结果。这种选择效应提醒我们，在不同时间点只分析“还能取出来的固体”，可能逐渐改变被测对象。交互实验可以调节断链速率、观察时间和溶解阈值，比较质量保持与平均链长。尝试保持断链速率不变，只改变阈值，就能看到化学变化相似而失重不同的情况。

## 断链与溶解分别控制了什么

初始链长固定为 100。每根连接键独立断裂，长度不超过阈值的片段立即进入溶液。改变断键概率与可溶长度，比较全部片段的数均链长和剩余聚合物质量。

[Figure: 片段质量分布](https://ml-biomat.com/tutorials/experimental-methods/e03/#E03-plot)

右下角另画了一个独立的理想球体表面侵蚀模型：表面以固定速度向中心退缩，密度保持不变，质量随半径的三次方变化。初始半径一毫米，表面每天退缩零点零零五毫米，一百天后半径剩一半，质量则只剩八分之一。它与前面的体相随机断链模型有不同假设，用来解释几何如何影响侵蚀曲线。实际材料接近哪一种情况，应结合截面形态、内部化学变化和尺寸依赖来判断。

$$
\frac{m(t)}{m(0)}=\left[\max\left(1-\frac{vt}{R_0},0\right)\right]^3
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | 侵蚀时间 t 时的球体质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4357fcfe49d6a8dd7d2c3424.svg) | 球体初始质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 表面向内退缩的恒定速度，mm d^{-1}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 侵蚀时间，d。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31e316fb976f1ca84f57e4cb.svg) | 球体初始半径，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8228983b74c5db73c259fc11.svg) | 取两个数中的较大者，避免半径小于零。 |

密度恒定且始终保持球形时，质量与半径的三次方成正比。R0=1 mm、v=0.005 mm/d、t=100 d 后半径为初始的一半，剩余质量为 0.5³=12.5%。

## 真实图像与碳去向，把“降解”说得更具体

Yin 等人比较了两种不同孔结构的明胶衍生凝胶在胶原酶环境中的变化。下图同时提供质量变化、宏观照片和显微图，可以观察材料形态如何随时间演化。阅读这幅图时，一个重要细节来自实验方法：作者称量的是去掉表面液体后的溶胀样品，所以图中的质量变化属于湿质量变化。本章保留原图，并把这一测量定义写清楚，使图像证据和称量对象对应起来，而不是将其直接改名为干聚合物质量损失。

![真实显微图和曲线完整转载自 Yin 等（2023），Figure 4，Frontiers in Soft Matter，DOI 10.3389/frsfm.2022.1101680，CC BY 4.0。原图内容不变，新增外部标题与署名。原文质量指标采用湿质量，图中的下降须结合形态与含水变化理解。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7d9f431c5c67025e5072b349.svg?v=7d9f431c5c67)

图 3真实显微图和曲线完整转载自 Yin 等（2023），Figure 4，Frontiers in Soft Matter，DOI 10.3389/frsfm.2022.1101680，CC BY 4.0。原图内容不变，新增外部标题与署名。原文质量指标采用湿质量，图中的下降须结合形态与含水变化理解。

宏观照片帮助判断整体是否完整，显微图帮助观察局部孔壁和表面变化，质量曲线则提供总体数量信息。三者放在一起，比单独挑选一张变化最大的照片更容易理解材料经历了什么。比较不同时间点时，还应留意比例尺、视野位置和样品是否来自同一观察方式。孔洞变大可能与侵蚀有关，也可能受到溶胀、塌陷或制样过程影响；结合湿态图像、干质量和组成分析，可以逐步分辨这些原因。

若问题转向环境中的生物转化，就需要追踪碳。微生物可以把部分材料碳转成二氧化碳，同时把一部分纳入自身生物量，还有一部分以溶解有机物或固体残留存在。样品从眼前消失，并不意味着这些碳已经全部矿化。呼吸测量通过二氧化碳生成或氧消耗追踪生物活动，实验中设置只含接种物、不含测试材料的空白，用来扣除微生物自身及培养基产生的背景信号。参考物则帮助检查实验系统是否正常工作。

以二氧化碳核算为例，假设初始材料一百毫克，其中碳占一半，那么初始碳为五十毫克。一个碳原子进入一个二氧化碳分子后，还结合了两个氧原子；用近似摩尔质量十二与四十四换算，全部碳变成二氧化碳时对应约一百八十三点三三毫克。若测得总二氧化碳八十毫克，接种物空白为十四毫克，归于样品的净量为六十六毫克，对应约百分之三十六的碳矿化。分母来自初始碳，而不是初始材料总质量。

$$
B=\frac{m_{\mathrm{CO_2,test}}-m_{\mathrm{CO_2,blank}}}{m_0w_C(44/12)}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 样品碳转化为二氧化碳的比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1ea936ecb6fb60952e0e8269.svg) | 测试体系累积收集的二氧化碳质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/827ffe18301532ffcc19ff8f.svg) | 对应接种物空白产生的二氧化碳质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | 初始待测材料干质量，mg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/76b6ff745138a626e7b2b375.svg) | 材料初始碳质量分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bd59755da4d9bf50091317ae.svg) | CO₂ 与碳的摩尔质量之比，单位相消。 |

每 12 mg 碳完全氧化对应约 44 mg 二氧化碳。100 mg 材料含碳 50%，理论 CO₂ 为 183.333 mg；测试得到 80 mg、空白 14 mg 时净值为 66 mg，B=36%。需采用能收集相应碳去向的实验系统。

![构造的碳守恒示例。左图将初始 50 mg 碳分配到固体、溶解物、生物量和二氧化碳；右图的纵轴则为 CO₂ 本身的质量。扣除接种物空白后，66 mg CO₂ 对应 18 mg 碳，矿化比例为 36%。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/41a4ff014e01f8f1bd84e161.svg?v=41a4ff014e01)

图 4构造的碳守恒示例。左图将初始 50 mg 碳分配到固体、溶解物、生物量和二氧化碳；右图的纵轴则为 CO₂ 本身的质量。扣除接种物空白后，66 mg CO₂ 对应 18 mg 碳，矿化比例为 36%。

图中的碳账本把五十毫克初始碳分到残余固体、溶解有机物、生物量和二氧化碳四个去向，数字是构造的守恒例子。真正的矿化实验需要适合环境的装置、空白、回收与时间条件；OECD 的好氧水相测试提供了这类测量的规范思路，而堆肥或其他介质需要对应方法。把测量环境写进结论，例如在指定温度和接种条件下的碳转化曲线，能让“降解快慢”具有可以复核的实际含义。

## 从一条下降曲线走向材料的使用窗口

样品破碎到无法夹持时，应把“无法完成该力学测量”与“测得零强度”区别记录；低于称量检出水平的残留，也应按检测范围表达。可以补充适合碎片或小质量样品的观察方法，并保留失去完整形态的时间。这样的记录能够说明功能终点何时到来，同时避免在图上填入并未测得的零值。研究结论会更贴近样品实际经历的过程。

程序输出每个时间点的质量保持率、全部片段的数均长度和残留片段的数均长度，并画出片段尺寸分布、溶解阈值敏感性及独立的球体表面侵蚀例子。计算首先检查重复单元总量守恒，再核对一个容易手算的片段数量关系。公开凝胶图与许可说明也随示例提供，运行时直接读取本地文件。这样，数值模型、原始公开图像和碳核算分别承担自己的解释任务，读者可以逐项复核，而不会把它们误当作同一批材料的实验结果。

### 完整 Python：断链分布、质量流失与碳去向

示例导出不同分子群体的平均链长、残留质量、四幅图与数值汇总；真实公开图像及许可说明随示例提供。

```
"""Constructed random-chain scission, dry-mass retention, and carbon accounting."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def fragment_distribution(probability,length=100):
    """Expected fragment counts per initial linear chain; independent identical bond cuts."""
    p=float(probability);l=np.arange(1,length+1);counts=np.empty(length)
    counts[:-1]=((length-l[:-1]-1)*p*p+2*p)*(1-p)**(l[:-1]-1)
    counts[-1]=(1-p)**(length-1)
    return l,counts

def response(time,rate=.003,cutoff=8,length=100):
    probability=1-np.exp(-rate*time);l,c=fragment_distribution(probability,length)
    keep=l>cutoff;mass=np.sum(l[keep]*c[keep]);number=np.sum(c[keep])
    return {'cut_probability':float(probability),'remaining_mass_percent':float(100*mass/length),'all_DP':float(length/c.sum()),'retained_DP':float(mass/number) if number>0 else 0.}

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.6))
    for a in ax:a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
    for row,(cut,title) in enumerate([(False,tr('链尚未切断','Uncut chain')),(True,tr('切一次：链数加一','One cut adds one chain'))]):
        xx=np.linspace(1,9,12);yy=np.full(12,6-row*3,dtype=float)
        for i in range(11):
            if cut and i==5:continue
            ax[0].plot(xx[i:i+2],yy[i:i+2],color='#186e83',lw=3)
        ax[0].scatter(xx,yy,color='#186e83',s=30);ax[0].text(5,4.8-row*3,title,ha='center',fontsize=10)
    ax[0].set_title(tr('A  断链先改变分子数量','A  Scission first changes molecule count'))
    for a,r,label in [(ax[1],2.2,tr('内部产物较难排出','Products retained in the interior')),(ax[2],.9,tr('较短的扩散路径','Shorter diffusion paths'))]:
        a.add_patch(Circle((5,4.4),r,color='#a2cdd9'));a.add_patch(Circle((5,4.4),r*.48,color='#cd803f',alpha=.75))
        for ang in [0,np.pi/2,np.pi,3*np.pi/2]:
            start=(5+r*.65*np.cos(ang),4.4+r*.65*np.sin(ang));end=(5+(r+1.1)*np.cos(ang),4.4+(r+1.1)*np.sin(ang));a.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=12,color='#186e83'))
        a.text(5,1.1,label,ha='center',fontsize=9)
    ax[1].set_title(tr('B  大尺度样品','B  Larger specimen'));ax[2].set_title(tr('C  小尺度样品','C  Smaller specimen'))
    fig.text(.5,.02,tr('1995：Grizzi 等通过不同尺寸的聚乳酸器件研究反应与扩散的耦合。','1995: Grizzi and colleagues investigated reaction–diffusion coupling across PLA device sizes.'),ha='center',fontsize=10);save(fig,'mechanism')
    time=np.linspace(0,120,241);records=[response(t) for t in time];remaining=np.array([r['remaining_mass_percent'] for r in records]);all_dp=np.array([r['all_DP'] for r in records]);ret_dp=np.array([r['retained_DP'] for r in records]);np.savetxt(output/'degradation.csv',np.column_stack([time,remaining,all_dp,ret_dp]),delimiter=',',header='time_day,remaining_mass_percent,all_fragments_number_average_DP,retained_fragments_number_average_DP',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11.6,7.3));ax=ax.ravel();ax[0].plot(time,remaining,label=tr('剩余聚合物质量','Remaining polymer mass'));ax[0].plot(time,all_dp,label=tr('全部片段的平均链长','Mean length of all fragments'));ax[0].plot(time,ret_dp,label=tr('仅残留片段的平均链长','Mean length of retained fragments'));ax[0].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('相对初始值 / %','Relative to initial value / %'),title=tr('A  质量与平均链长分开变化','A  Mass and mean chain length change differently'));ax[0].legend(fontsize=8)
    for t in [10,30,90]:
        l,c=fragment_distribution(1-np.exp(-.003*t));ax[1].plot(l,l*c/100,label=f'{t} d')
    ax[1].axvspan(1,8,color='#cd803f',alpha=.12);ax[1].set(xscale='log',xlabel=tr('片段长度 / 重复单元数','Fragment length / repeat units'),ylabel=tr('初始质量的比例 / 每种长度','Initial mass fraction / length class'),title=tr('B  短片段到达可溶范围','B  Short fragments enter the soluble range'));ax[1].legend(fontsize=9)
    for threshold in [4,8,12]:ax[2].plot(time,[response(t,cutoff=threshold)['remaining_mass_percent'] for t in time],label=f'{threshold}')
    ax[2].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('剩余聚合物质量 / %','Remaining polymer mass / %'),title=tr('C  改变溶解阈值，不改变断链速率','C  Change solubility threshold, keep scission rate'));ax[2].legend(title=tr('最大可溶长度','Maximum soluble length'),fontsize=9)
    for radius in [.5,1,2]:ax[3].plot(time,100*np.maximum(1-.005*time/radius,0)**3,label=f'{radius:g} mm')
    ax[3].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('剩余质量 / %','Remaining mass / %'),title=tr('D  独立的球体表面侵蚀模型','D  Separate spherical surface-erosion model'));ax[3].legend(title=tr('初始半径','Initial radius'),fontsize=9)
    fig.tight_layout();save(fig,'kinetics')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));labels=tr(['剩余固体','溶解有机物','生物量','二氧化碳中的碳'],['Remaining solid','Dissolved organics','Biomass','Carbon in CO₂']);values=[10,15,7,18]
    left=0
    for label,value,color in zip(labels,values,['#186e83','#cd803f','#8160a1','#3c8a6a']):ax[0].barh([0],value,left=left,label=label,color=color);left+=value
    ax[0].set(xlabel=tr('碳质量 / mg','Carbon mass / mg'),yticks=[],xlim=(0,50),title=tr('A  50 mg 初始碳的四条去向','A  Four destinations for 50 mg initial carbon'));ax[0].legend(loc='upper center',bbox_to_anchor=(.5,-.15),fontsize=9,ncol=2)
    ax[1].bar(tr(['测得总量','接种物空白','样品净贡献','理论完全转化'],['Measured total','Inoculum blank','Net specimen','Theoretical total']),[80,14,66,50*44/12],color=['#8160a1','#a8b4b9','#3c8a6a','#186e83']);ax[1].tick_params(axis='x',labelrotation=20);ax[1].set(ylabel=tr('CO₂ 质量 / mg','CO₂ mass / mg'),title=tr('B  扣空白后矿化比例为 36%','B  Blank-corrected mineralization is 36%'));fig.tight_layout();save(fig,'carbon')
    from PIL import Image
    img=np.asarray(Image.open(Path(__file__).with_name('yin2023-figure4.webp')));fig,ax=plt.subplots(figsize=(11,8));ax.imshow(img);ax.axis('off');ax.set_title(tr('真实研究：酶作用下的凝胶形态与湿质量变化','Published study: gel morphology and wet-mass change under enzyme exposure'),fontsize=12,pad=12);fig.text(.5,.015,'Yin et al. (2023), Figure 4 · Frontiers in Soft Matter · CC BY 4.0',ha='center',fontsize=9);save(fig,'published')
    l,c=fragment_distribution(.1);r30=response(30);summary={'worked_example':{'initial_dry_mg':100,'remaining_dry_mg':80,'mass_loss_percent':20,'one_cut_DP_ratio':.5,'one_cut_retained_mass_percent':100},'distribution':{'mass_conserved_units':float(np.sum(l*c)),'expected_fragment_count':float(c.sum()),'mean_DP_at_p_point1':float(100/c.sum()),'retained_mass_at_p_point1_percent':float(np.sum(l[8:]*c[8:]))},'at_day30':r30,'carbon':{'theoretical_CO2_mg':50*44/12,'net_CO2_mg':66,'mineralized_percent':36},'surface':{'radius1_day100_percent':100*(1-.005*100)**3}}
    assert abs(sum(l*c)-100)<1e-10;assert abs(sum(c)-10.9)<1e-10;assert abs(summary['surface']['radius1_day100_percent']-12.5)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

可以先改变模型中的断链速率，观察横向时间尺度如何移动；再只改变可溶阈值，观察失重变化而全部片段平均链长保持相同；最后比较不同半径的表面侵蚀曲线。每次只改一个条件，能够看清它控制的是化学、分离还是几何环节。若用真实数据拟合参数，应先确定测得的是哪个群体的分子量、哪一种质量以及哪一种边界条件，再选择模型，避免用多个自由参数把不同过程都揉成一条看似贴合的曲线。

降解结果的实际意义，常常落在两个时间之间：材料开始失去需要的功能，以及材料完成所需的结构或物质转化。对支架来说，还要把组织形成速度放进考虑；对释放载体来说，网络变化会同时影响分子迁移与释放；对环境材料来说，则要区分碎片形成、溶解和最终碳去向。报告可以以这些问题为主线，展示质量、结构和功能的对应关系，让“第几天变化多少”继续服务于材料选择和下一轮实验设计。

下一章讨论释放实验。一个分子离开载体，可能是自己沿浓度梯度扩散出去，也可能是网络溶胀后通道变宽，或者载体降解后原先困住的分子被释放出来。这里建立的质量基准、时间记录和外液更换意识，会直接用于释放量核算。把载体的变化与载荷的去向分别测量，再把它们连接起来，就能解释为什么两种看起来相似的释放曲线，背后可能有不同的材料过程。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Grizzi et al. (1995). Hydrolytic degradation of devices based on poly(DL-lactic acid) size-dependence](https://pubmed.ncbi.nlm.nih.gov/7772670/)

   尺寸、自催化与反应—扩散的历史实验。

   Abstract reference; no figures reproduced.
2. [Höglund et al. (2012). Crucial Differences in the Hydrolytic Degradation between Industrial Polylactide and Laboratory-Scale Poly(L-lactide)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3359772/)

   分子量变化与质量流失分离，以及温度、形态和介质的影响。
3. [Tsuji et al. (2011). Synthesis and Hydrolytic Degradation of Substituted Poly(DL-Lactic Acid)s](https://www.mdpi.com/1996-1944/4/8/1384)

   水解实验中的分子量测量与样品定义。
4. [Yin et al. (2023). Physical properties and cellular responses of gelatin methacryloyl bulk hydrogels and highly ordered porous hydrogels](https://www.frontiersin.org/journals/soft-matter/articles/10.3389/frsfm.2022.1101680/full)

   酶作用、孔结构、真实显微图与湿质量指标。

   CC BY 4.0; Figure 4 reproduced with attribution.
5. [OECD (1992). Test No. 301: Ready Biodegradability](https://www.oecd.org/en/publications/test-no-301-ready-biodegradability_9789264070349-en.html)

   好氧筛选中的空白、参考物与 CO₂、耗氧及溶解碳测量。

   Official method reference; no assets reproduced.
