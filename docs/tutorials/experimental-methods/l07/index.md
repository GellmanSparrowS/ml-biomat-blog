# Western blot：条带的身份、强度与比较

Source: https://ml-biomat.com/tutorials/experimental-methods/l07/
Language: zh-CN

沿着分离、转移、识别和成像，理解一条蛋白条带怎样成为有明确分母的测量。

## 一条深色条带，究竟告诉了我们什么

一种材料让细胞中的某个蛋白增加了，还是让它被切成了更小的片段？培养条件改变后，某个信号蛋白的总量没有变，它的修饰状态是否已经改变？这类问题不仅关心“有多少”，还关心“是什么大小、哪一种形式”。Western blot，通常称蛋白质免疫印迹，把两种能力放到一起：先通过凝胶把复杂蛋白混合物按迁移行为分开，再用抗体找出其中的目标。条带的位置提供表观大小信息，条带的信号在合适的工作范围内支持数量比较。

可以想象一群外形不同的人同时挤过一条布满障碍的通道。如果每个人身上受到的推动方式各不相同，最后的位置很难比较。常用的 SDS 聚丙烯酰胺凝胶电泳先尽量把蛋白展开，并让它们获得相对一致的电荷与质量关系，再利用凝胶网孔对不同长度分子的阻碍来分离。这个类比帮助理解分离方向，但蛋白并不是刚性的球，迁移也不是完美的称重过程。因此，我们通过同胶的分子质量标尺读出“表观分子质量”，再与目标的预期形式结合判断。

一条带的深浅则经过了另一串过程：裂解提取、加样、分离、转膜、抗体结合、报告反应和成像。任何一段变化，都可能改变最终亮度。要把处理组与对照组的条带差异解释成目标量差异，就要使这些环节具有可比较的条件，并用合适的参照检查进入每条泳道的样品量。参照并不是为了把图做得整齐，而是为了回答一个具体问题：这条带变强，究竟是目标在样品中的比例改变了，还是这一道整体进入了更多蛋白？

本章用一组已知真值的构造印迹图逐步完成计算，同时阅读真实发表的稀释系列。构造例子让处理组的目标相对于总蛋白增加两倍，并另外改变各泳道的加样量和转移比例。代码从实际生成的像素中积分，比较校正前后能否找回这个两倍关系。真实实验图则让我们看到不同蛋白和不同成像方式具有不同的定量范围。把图像外观、像素测量和生物学问题接在一起，条带就不再只是论文里一排深浅不同的方块。

## 把分离的位置保存下来，让抗体能够接近目标

电泳后的蛋白位于凝胶内部，而抗体需要到达这些位置才能识别目标。1979 年，Towbin、Staehelin 和 Gordon 报道了通过电场把蛋白从聚丙烯酰胺凝胶转移到硝酸纤维素膜上的方法。Towbin 后来回忆，他们研究核糖体蛋白的抗体时，希望利用已经分离好的蛋白图案来确定抗体识别谁，但致密凝胶妨碍抗体自由进出。把图案复制到更容易接近的表面，便让“分开”与“识别”两个步骤顺利衔接。

这个历史问题很容易用印章理解：我们希望保留各条带在平面上的相对位置，却把蛋白从厚厚的凝胶内部搬到膜上。实际转移依靠电场使带电蛋白沿垂直于凝胶平面的方向移动。膜放在迁移路径上，接收并保留蛋白。凝胶、膜和缓冲液之间需要良好接触；夹在中间的气泡会形成局部接触缺口，使某块区域转移不足。观察转膜后的整体蛋白分布，可以把这种空间缺口与“目标恰好在这里消失”区分开。

![1979年电转移思想的原创示意：凝胶完成分离，横向电场把空间图案转移到可供抗体接近的膜上。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1f0adfcfa6b7bfff659f51a9.svg?v=1f0adfcfa6b7)

图 11979年电转移思想的原创示意：凝胶完成分离，横向电场把空间图案转移到可供抗体接近的膜上。

大分子与小分子的转移条件不完全相同。大分子可能较难从凝胶中出来，小分子可能更容易穿过某些膜或在特定条件下保留不足。凝胶组成、膜材料、孔径、转移时间和缓冲体系因此需要围绕目标范围选择。转移时间越长，并不意味着所有目标都越好。可以同时查看膜上的整体信号以及转移后凝胶中残留的蛋白，判断当前条件主要缺在哪一段。优化的对象是目标范围内的可比较转移，而不是追求一个脱离样品的统一时间。

转膜后，封闭减少抗体在无关表面的吸附，一抗识别目标，带报告标记的二抗或其他检测组件把结合位置转成信号。化学发光体系让酶催化产生光，荧光体系则需要相应激发光；它们的信号稳定性、通道安排和动态范围各有特点。膜上的蛋白位置是同一个空间底图，检测方式决定如何把这些位置变成数字。比较不同曝光或不同检测方法时，应回到原始信号与已验证的范围，而不是仅比较哪张展示图的背景更白。

## 从细胞到泳道：让加进去的样品有明确含义

裂解把细胞内部组分释放到溶液中，但不同蛋白的提取难度不同。膜相关蛋白、细胞骨架蛋白和容易溶解的胞质蛋白，对缓冲液和处理条件的响应可能不同。离心后取上清，得到的是这套条件下进入上清的蛋白部分；若目标主要留在沉淀中，只分析上清便会漏掉它。选择提取方式时，应先考虑目标所在的位置以及研究的问题，再检查相应部分是否被保存。材料表面上附着的细胞还可能难以完整回收，需要注意不同组的回收过程是否一致。

蛋白酶能够切断蛋白，磷酸酶能够去掉某些磷酸化修饰。细胞被打开后，原本分隔在不同位置的酶与底物有机会相遇，因此样品制备的时间、温度与保护条件会影响后来看到的形式。研究总蛋白与研究磷酸化形式，关心的保存对象并不完全一样。把取样时刻和处理顺序固定下来，能够减少操作过程中新增的变化。出现较小条带时，也应把真实加工、目标降解和抗体识别其他分子的可能性放到具体对照中区分。

常规变性电泳中，SDS 帮助展开蛋白并赋予负电荷；还原剂则用来处理二硫键，把某些通过二硫键连接的链分开。二者作用不同，是否使用还原条件取决于想观察的蛋白形式。加热也不是所有样品都越强越好，某些蛋白在不合适条件下会聚集或丢失可识别性。记录变性、还原和加热条件，才能把不同分子质量位置上的信号与制样状态联系起来。同一批比较样品应共享相应的处理方式。

上样前测总蛋白浓度，是把“加多少体积”换成“加多少蛋白”的一步。假设样品浓度为每微升 2 微克，计划上样 20 微克，就需要 10 微升样品。另一样品浓度每微升 1 微克，则需要 20 微升，再通过配制使最终缓冲条件和总体积相容。蛋白测定方法还要与裂解液中的去污剂、还原剂等组分兼容。标准液和样品环境差异较大时，测得的总浓度可能带着基质偏差，随后每条泳道的“相同上样量”也会受到影响。

$$
V=m/C
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 所取样品体积，μL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 计划上样的蛋白质量，μg |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 样品总蛋白质量浓度，μg/μL |

质量等于浓度乘体积，移项得到所需体积。20μg除以2μg/μL得到10μL。浓度应来自与裂解液兼容的定量；加入缓冲液后总装载体积再单独匹配。

相同总蛋白上样量定义了比较的分母，却不自动等于相同细胞数。如果处理让细胞明显增大或改变总体蛋白含量，每 20 微克总蛋白所代表的细胞数量可能不同。研究“目标占总体蛋白的比例”时，总蛋白归一化很直接；研究“每枚细胞有多少目标”时，还要保留细胞数量、提取体积和回收信息。一个实验可以保存多种原始量，但解释时应清楚说明当前比值代表哪一种生物学尺度。

## 读条带位置，也读整条泳道的上下文

分子质量标尺由一组已知大小的蛋白组成，与样品一起经历电泳。常用做法是在适用范围内，把标尺的分子质量取对数，与迁移距离建立近似关系。距离越大，通常对应越小的表观质量。对数刻度的一个特点是，100 到 50 与 50 到 25 都是减半，所以在理想的局部标定中会对应相等的距离间隔。本例用这个关系构造标尺：20、40、60 毫米分别对应 100、50、25 千道尔顿，便于直观核对计算。

$$
\log_{10}\!\left(\frac{M}{1\,\mathrm{kDa}}\right)=\alpha-\beta d
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 标尺估计的表观分子质量，kDa |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 从相同原点测得的迁移距离，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 拟合截距，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | 正的距离系数，mm的负一次方 |

在标尺近似对数线性的胶段内拟合。构造例中20、40、60mm分别对应100、50、25kDa，β=0.0150515/mm、α=2.30103，40mm得到50kDa。除以1kDa使对数自变量无量纲；真实标尺按其校准段使用。

读到接近预期分子质量的条带，是身份判断的一条线索。糖基化、剪切、异构体、聚集和异常迁移都可能改变位置；抗体也可能识别其他大小相近的蛋白。可以使用目标降低或缺失的样品、已知表达目标的阳性样品，或识别不同表位的独立抗体，检查指定条带随目标变化的关系。对磷酸化抗体，还可结合能够改变相应修饰的处理与总蛋白检测。每种对照都围绕要确定的身份或形式提供信息。

因此，保存完整膜图很有价值。只截取预期位置附近的一小条，容易让上方的聚集信号、下方的降解片段或其他明显条带退出视野。分析前先看整条泳道，再明确积分哪一个峰、为什么选它。构造图中在目标下方保留了另一条较弱信号，它提醒我们：有颜色的位置并不都自动属于同一个定量对象。示例只积分事先指定的目标峰，并把另一个峰留在完整图中，让选择可以被直接看见。

条带的弯曲、拖尾和宽度也提供实验信息。加样过多、样品盐分或分离过程不均匀，可能让峰变宽或泳道变形；相邻条带挤在一起时，积分范围会影响包含的信号。选择合适的凝胶范围与上样量，让目标在局部分离得清楚，比事后用一个越来越精细的框切开重叠条带更可靠。预染标尺可以方便观察运行和转移，但染料修饰也会影响迁移，因此应结合适合该体系的标尺说明来理解大小估计。

## 从像素加法到归一化倍数

一张膜图可以看成二维数字表。一个条带占据许多像素，积分信号就是把选定区域的像素读数相加。背景同样占据这些像素，因此扣背景时需要考虑区域面积。若 400 个像素的原始总和为 12000，每像素背景为 20，那么背景总量为 8000，条带净积分为 4000。把背景只减一次，会把大部分背景仍留在条带数值里。图像软件中的“平均值”和“积分值”代表不同量，使用时先确认当前输出的是哪一个。

$$
S=\sum_{j=1}^{n}I_j-nB
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 扣背景后的区域积分，读数单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/2182e4a63941864596054a3f.svg) | 区域第j像素的原始读数，读数单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 区域像素编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 区域像素数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 该区域代表性背景的每像素平均读数 |

求和包含条带和区域内背景，因此需扣掉每个像素的背景贡献。400像素总读数12000，背景20，净积分4000。例中使用未截顶、线性响应的数字图像；复杂背景需以空间匹配方法估计。

背景怎样选，取决于它在膜上的空间变化。均匀背景可以用附近没有条带的区域估计；如果背景沿泳道缓慢变化，可以通过目标上下的区域或适合的局部方法估计。选择区域时不要把邻近弱条带当成纯背景，也不要为了让各组更接近而分别调整规则。代码在目标峰上下取对称的局部区域，估计该峰附近的背景；总蛋白通道使用相邻空白带，并显式处理构造图中已知的横向缓慢梯度。每一步都能从保存的数组中检查。

积分框应完整覆盖指定峰，并以一致规则处理各泳道。框太小会截掉宽条带的尾部，框太大则把更多背景波动或邻近峰加进去。对相似条带，可使用一致宽度和边界规则；对形状差异明显的峰，需要检查固定框是否仍捕获了同一物理对象。查看泳道的纵向强度曲线很有帮助：条带变成峰，背景变成基线，积分区域对应峰下的一段面积。曲线能够显示一张小缩略图中不容易看出的截顶与拖尾。

![实际代码产生的构造像素、积分边界、泳道剖面和定量。泳道1–3是对照，4–6真实靶标比例为2倍；第二条弱带保留在全幅图中。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9d80a55d136c637ccc04d9d8.svg?v=9d80a55d136c)

图 2实际代码产生的构造像素、积分边界、泳道剖面和定量。泳道1–3是对照，4–6真实靶标比例为2倍；第二条弱带保留在全幅图中。

归一化的下一步，是把目标净信号除以同一泳道的参照信号，再与对照组比较。例如对照目标信号 10000、总蛋白信号 100000；处理组目标 24000、总蛋白 120000。只看目标会得到 2.4 倍，而按总蛋白校正后是 2 倍。这样做依赖目标和参照在相应工作范围内按样品量响应，且参照能反映想校正的共同变化。若目标转移行为特别不同，或参照自身发生生物学变化，一个除法不会自动消除所有差异。

$$
R_i=T_i/P_i,\qquad F_i=R_i/\overline{R}_{\rm control}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/df8767aa6cc94e0af05ed184.svg) | 第i个样品的靶标与总蛋白积分比，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样品编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/d337cf254934852ef394972a.svg) | 靶标条带扣背景积分，读数单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/0cabdc5951d269a0b202838f.svg) | 该泳道总蛋白扣背景积分，同一约定读数尺度 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b2693d2330ea11c23fe03a6.svg) | 相对对照均值的倍数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/56cda88a0249301c9488c9fc.svg) | 对照样品各自Ri的算术均值，无量纲 |

每条泳道先除自身总蛋白，再与对照比值均值比较。对照10000/100000=0.1，处理24000/120000=0.2，倍数为2；直接比较靶标得到2.4。两种信号均处于已检查的响应区间，总蛋白作为分母对应每单位回收总蛋白的靶标量。

构造图中六条泳道的目标真值按组分别为一倍和两倍，加样与转移则在各道变化。直接比较目标峰会出现额外起伏，按总蛋白通道校正后，两组关系更接近已知真值。每条泳道仍保留独立数值，不把处理组先合并成一条代表性条带。实际研究中，来自独立培养或独立样品的泳道用于比较生物变化；同一样品重复上样帮助检查技术重复。保存样品与膜的对应关系，才能在后续汇总中维持这一区分。

## 条带越深，为什么反而越难比较

最深的条带未必提供最多的定量信息。信号与目标量在一段范围内可以近似成比例，但超过范围后会逐渐变平。原因可能来自上样与膜容量、抗体可及性、报告反应，也可能来自探测器截顶。后者很容易理解：探测器只能记到某个最大值，两倍输入都达到上限时，像素看起来便一样深。缩短曝光有助于检查探测器截顶；如果改变曝光后，上样稀释系列仍不按比例响应，则应继续检查检测链更前面的环节。

因此，先用代表性混合样品做一组上样梯度，可以同时检查目标与参照的响应范围。某个丰富的管家蛋白可能在很低的总上样量下已经接近平台，而低丰度目标仍需要更多样品才看得清楚。管家蛋白指维持细胞基本功能的一类常用参照候选，它的名称不保证在所有处理条件下保持恒定。选择参照时，既要检查它的生物稳定性，也要检查它的信号是否处于可比较区间。总蛋白染色提供另一种分母，但同样需要核对背景、线性和样品构成。

真实稀释实验把这些差异展示得很清楚。Taylor 等人的图中，同一组样品包含加入的 ADH 与内源 GAPDH，上方和下方条带分别对应这两个对象；不同面板采用数字成像和胶片检测。沿着上样量减半的方向阅读，可以看到两个对象的信号并不是在所有位置都同步减半。曲线上的误差条为四张膜的平均值标准误，反映这组重复均值的估计分散。图的用途是帮助识别工作范围，而不是把其中某个上样量直接搬到其他蛋白或仪器。

![Taylor等2013年图3，完整转载，Creative Commons Attribution。ADH与GAPDH稀释系列使用数字成像或胶片；曲线误差条为4张膜的SEM。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/eddee5c5c95f89217149f4da.svg?v=eddee5c5c95f)

图 3Taylor等2013年图3，完整转载，Creative Commons Attribution。ADH与GAPDH稀释系列使用数字成像或胶片；曲线误差条为4张膜的SEM。

交互实验专门隔离探测器截顶这一环节。两条构造峰的真实目标量相差两倍，峰形相同，背景已知。开始时曝光适中，积分比值接近二；提高曝光后，强峰先被截平，测得倍数下降。再把两条泳道同时减少上样量，观察比例关系怎样恢复。屏幕中保留未截断的虚线曲线，让你看见消失的那部分信号在哪里。这个实验把“缩短曝光”与“减少上样”作为可比较的操作，同时说明它只模拟了检测上限这一种机制。

## 交互实验：多曝光会不会改变倍数

两条构造条带的真实目标量始终相差2倍。调整曝光和共同上样量，观察原始轮廓在255读数处截顶，随后比较扣背景积分。背景也随曝光增长；虚线表示不受检测上限影响的响应。

[Figure: 双条带原始强度轮廓](https://ml-biomat.com/tutorials/experimental-methods/l07/#L07-lab)

![构造的标尺、成像截顶、测得倍数与背景误差诊断。D在同一400像素区域比较弱、强净积分的敏感性。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0f280524f689118bf6e6393d.svg?v=0f280524f689)

图 4构造的标尺、成像截顶、测得倍数与背景误差诊断。D在同一400像素区域比较弱、强净积分的敏感性。

另一个常见问题是弱条带的背景敏感性。相同的每像素背景误差，乘以积分区域的像素数后会形成相同的总误差，但它占弱条带净信号的比例更大。图中使用相同的 400 像素区域，比较净积分 800 与 8000 的条带：背景每像素高估一个单位，就分别损失一半与百分之五的净信号。这样的检查能帮助判断某个很大的倍数变化是否主要由接近背景的小分母造成，并指向增加有效信号或改善背景估计的具体方向。

## 把完整膜图、逐泳道数值与研究问题放在一起

完整程序输出构造靶标图、总蛋白图、各泳道的净积分与归一化表，以及独立的大小标定、背景和饱和诊断。原始数组保留所有像素，读者可以把积分区域向上或向下移动，查看是否混入另一个峰；也可以改变背景估计位置，比较不同规则怎样影响弱信号。图中的构造数据与真实发表图分开标注，程序不从压缩的论文展示图中推测原始定量值。这样，形态阅读与数值复现各自有清楚的依据。

### 完整 Python：从条带像素到归一化倍数

运行后导出完整构造像素、逐泳道CSV、摘要和图形；真实发表图在离线资料包内。

```
"""Offline western-blot pixels, lane normalization and dynamic-range exercise."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';GREEN='#3c8a6a';PURPLE='#8160a1'
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def integrated(signal=80.,exposure=1.,ceiling=255.):
    y=np.arange(-20,21);profile=signal*np.exp(-.5*(y/4)**2)
    return float((np.minimum(ceiling,exposure*(profile+20))-exposure*20).sum())
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(707);yy,xx=np.mgrid[:240,:400];base=20+.025*yy+.01*xx
    target=base.copy();total=base.copy();loads=np.array([1,.8,1.2,1,.8,1.2]);transfers=np.array([1,.9,1.1,.85,1.05,.95]);amount=np.array([1,1,1,2,2,2]);centers=45+60*np.arange(6)
    for i,cx in enumerate(centers):
        shape_x=np.exp(-.5*((xx-cx)/8)**2);factor=loads[i]*transfers[i]
        target+=80*amount[i]*factor*shape_x*np.exp(-.5*((yy-95)/4)**2)
        target+=7*factor*shape_x*np.exp(-.5*((yy-165)/4)**2)
        for y0,a in zip([50,80,110,145,180,210],[18,30,20,26,16,22]):total+=a*factor*shape_x*np.exp(-.5*((yy-y0)/4)**2)
    target+=rng.normal(0,.4,target.shape);total+=rng.normal(0,.4,total.shape);rows=[]
    for i,cx in enumerate(centers):
        mask=(abs(xx-cx)<=16)&(abs(yy-95)<=15)
        bgmask=(abs(xx-cx)<=16)&(((yy>=65)&(yy<=75))|((yy>=115)&(yy<=125)))
        bg=target[bgmask].mean();signal=float(target[mask].sum()-mask.sum()*bg)
        lane=(abs(xx-cx)<=16)&(yy>=30)&(yy<=225)
        side=(abs(xx-(cx+26))<=2)&(yy>=30)&(yy<=225)
        # Correct the known linear x-gradient between adjacent background strip and lane center.
        total_bg=float(total[side].mean()-.01*26)
        total_signal=float(total[lane].sum()-lane.sum()*total_bg)
        rows.append([i+1,'control' if i<3 else 'treated',loads[i],transfers[i],amount[i],signal,total_signal,signal/total_signal])
    with (out/'lanes.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['lane','group','relative_load','relative_transfer','true_target_per_total','target_integral_au','total_protein_integral_au','target_over_total']);w.writerows(rows)
    np.savez_compressed(out/'blots.npz',target=target,total_protein=total,background_plane=base)
    ratio=np.array([r[-1] for r in rows]);normalized=ratio/ratio[:3].mean();rawratio=np.array([r[-3] for r in rows]);rawratio/=rawratio[:3].mean()
    fig,ax=plt.subplots(figsize=(11,5.1));ax.axis('off');ax.set(xlim=(0,12),ylim=(0,7))
    for x0,col,label in [(1.5,BLUE,T('分离后的凝胶','Separated gel')),(6,PURPLE,T('接收蛋白的膜','Receiving membrane'))]:
        ax.add_patch(Rectangle((x0,1.2),2.2,4.7,fc=col,alpha=.13,ec=col))
        for j in range(3):
            for y in [2+j*.3,3.2+j*.2,4.8-j*.3]:ax.plot([x0+.3+j*.55,x0+.7+j*.55],[y,y],color=col,lw=4)
        ax.text(x0+1.1,.6,label,ha='center')
    ax.annotate('',xy=(5.7,3.5),xytext=(4,3.5),arrowprops={'arrowstyle':'->','lw':2});ax.text(4.8,4.1,T('横向电场','Transverse field'),ha='center')
    ax.text(9.8,4.4,T('保留分离位置\n让抗体接近蛋白','Preserve separation\nMake proteins accessible'),ha='center',linespacing=1.7)
    ax.text(6,6.6,T('1979：Towbin、Staehelin、Gordon 的电转移方法','1979: electrophoretic transfer by Towbin, Staehelin and Gordon'),ha='center',fontsize=12)
    fig.text(.5,.02,T('原创示意：条带间的位置关系在转移后保留；不是历史仪器照片。','Original schematic: relative band positions survive transfer; not a historical apparatus photograph.'),ha='center',fontsize=9);save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8.4))
    for a,img,title in [(ax[0,0],target,T('A  构造靶标通道','A  Constructed target channel')),(ax[0,1],total,T('B  构造总蛋白通道','B  Constructed total-protein channel'))]:
        a.imshow(img,cmap='gray_r',vmin=15,vmax=200);a.set_title(title);a.set_xticks(centers,range(1,7));a.set_xlabel(T('泳道','Lane'));a.set_yticks([50,95,165,210]);a.set_ylabel(T('纵向位置 / 像素','Vertical position / pixel'))
    for cx in centers:ax[0,0].add_patch(Rectangle((cx-16,80),32,30,fill=False,ec=AMBER,lw=.8))
    profile=target[:,centers[0]-16:centers[0]+17].mean(axis=1);ax[1,0].plot(np.arange(240),profile,color=BLUE);ax[1,0].axvspan(80,110,color=AMBER,alpha=.25);ax[1,0].set(xlabel=T('纵向位置 / 像素','Vertical position / pixel'),ylabel=T('泳道横向平均读数 / a.u.','Lane-width mean signal / a.u.'),title=T('C  积分区域只覆盖指定的靶标峰','C  Integration isolates the selected target peak'))
    ax[1,1].bar(np.arange(6)-.18,rawratio,.35,color=BLUE,label=T('只比较靶标','Target only'));ax[1,1].bar(np.arange(6)+.18,normalized,.35,color=AMBER,label=T('总蛋白归一化','Total-protein normalized'));ax[1,1].set_xticks(range(6),range(1,7));ax[1,1].set(xlabel=T('泳道1–3对照，4–6处理','Lanes1–3control;4–6treated'),ylabel=T('相对各自对照均值','Relative to corresponding control mean'),title=T('D  相同真实倍数，不同加样与转移','D  Shared true fold change, variable loading'));ax[1,1].legend(fontsize=8);fig.tight_layout();save(fig,'pixels')
    fig,ax=plt.subplots(2,2,figsize=(11,8.2));masses=np.array([100,100/np.sqrt(2),50,50/np.sqrt(2),25]);dist=np.array([20,30,40,50,60]);coef=np.polyfit(dist,np.log10(masses),1)
    ax[0,0].plot(dist,masses,'o-',color=BLUE);ax[0,0].set_yscale('log');ax[0,0].set_yticks([25,50,100],[25,50,100]);ax[0,0].set(xlabel=T('迁移距离 / mm','Migration distance / mm'),ylabel=T('表观分子质量 / kDa','Apparent molecular mass / kDa'),title=T('A  构造标尺：对数质量与距离','A  Constructed ladder: log mass and distance'))
    load=np.geomspace(.05,6,100)
    for e,col in [(1,BLUE),(3,AMBER)]:ax[0,1].plot(load,[integrated(80*v,e) for v in load],color=col,label=T(f'曝光{e}倍',f'{e}× exposure'))
    ax[0,1].set(xlabel=T('相对目标量','Relative target amount'),ylabel=T('积分读数 / a.u.','Integrated signal / a.u.'),title=T('B  截顶后信号不再按量增长','B  Clipping breaks proportional response'));ax[0,1].legend(fontsize=8)
    exposures=np.linspace(.2,4,100);fold=[integrated(160,e)/integrated(80,e) for e in exposures]
    ax[1,0].plot(exposures,fold,color=PURPLE);ax[1,0].axhline(2,color=GREEN,ls='--');ax[1,0].set(xlabel=T('曝光倍数','Exposure multiplier'),ylabel=T('测得倍数变化','Measured fold change'),title=T('C  真值2倍在饱和时被压低','C  Saturation compresses a true twofold change'))
    errors=np.linspace(-2,2,50);ax[1,1].plot(errors,100*(800-400*errors)/800,color=BLUE,label=T('弱条带：总净信号800','Weak band: net integral800'));ax[1,1].plot(errors,100*(8000-400*errors)/8000,color=AMBER,label=T('强条带：总净信号8000','Strong band: net integral8000'));ax[1,1].set(xlabel=T('每像素背景高估值 / a.u.','Background overestimate per pixel / a.u.'),ylabel=T('保留下来的净信号 / %','Retained net signal / %'),title=T('D  同一400像素区域的背景敏感性','D  Background sensitivity in400pixels'));ax[1,1].legend(fontsize=8)
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(10,9));ax.imshow(Image.open(Path(__file__).resolve().parent/'taylor2013-figure3.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实稀释系列：目标与参照各有工作范围','Measured dilution series: target and reference have distinct ranges'),fontsize=12);fig.text(.5,.015,T('Taylor等，2013，图3；Creative Commons Attribution。\n上、下条带分别为ADH、GAPDH；曲线误差条为4张膜的SEM。','Taylor et al.,2013,Fig.3; Creative Commons Attribution.\nUpper/lower bands: ADH/GAPDH; curve error bars: SEM from4blots.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'published')
    assert np.isclose(integrated(160)/integrated(80),2)
    summary={'mass':{'load_volume_ul':20/2,'ladder_midpoint_kDa':float(10**np.polyval(coef,40))},'background':{'corrected_integral':12000-400*20},'normalization':{'raw_ratio':24000/10000,'normalized_fold':(24000/120000)/(10000/100000)},'dynamic':{'linear_fold':integrated(160)/integrated(80),'exposure_three_fold':integrated(160,3)/integrated(80,3)},'pixels':{'mean_control':float(normalized[:3].mean()),'mean_treated':float(normalized[3:].mean()),'individual_normalized':normalized.tolist()}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

第一次运行先核对一个简单结果：只改变两组目标比例为一与二时，校正后能否找回两倍。随后加入不同的加样量，看未经归一化的波动；再把参照也设置为随处理改变，观察一个不稳定分母会怎样改变答案。研究磷酸化时还可以思考两个分母：磷酸化目标除以总目标，描述该目标的相对修饰信号；总目标除以总蛋白，描述目标在总体样品中的相对含量。两种比值对应不同问题，最好把构成它们的原始量一起保留。

正式比较时，可把完整膜图作为空间记录，把选定条带、标尺和积分范围作为分析记录，再把各独立样品的归一化数值放到同一张统计图中。不同膜之间若需要比较，可以安排共同参照样品连接测量尺度，同时保留各膜自己的对照。最终叙述从样品与目标形式开始，说明条带身份如何确认、哪个范围用于比较、分母代表什么，再解释组间变化。这样的一条证据链既保留了蛋白印迹特有的大小信息，也让深浅比较成为清楚的数量问题。

还可以把不同样品的共同参照放进每一张膜，理解跨膜比较为什么多了一层关系。假设同一份混合裂解液分别出现在两次实验中，第一次靶标与总蛋白比值为0.10，第二次为0.08；同一个待比较样品在第二张膜上得到0.16，除以当张膜共同参照就是2。直接把0.16与第一张膜的0.10相比会得到1.6，混入了两次测量尺度的差异。共同参照应有足够的同批分装并经过保存稳定性检查，各组样品在不同膜之间均衡安排。它连接的是测量尺度，组内独立样品之间的真实差异仍然保留。

膜上的黑白关系也需要先问清。数字发光图的原始读数通常随检测到的光增加而增大，软件可以把高读数显示成白色，也可以反转显示成黑色；改变显示配色并不改变原始数组。扫描胶片的灰度则还经过胶片曝光、显影和扫描仪响应，较黑处可能对应较小的像素值。将图片简单反色只改了数值方向，未恢复所有环节的线性关系。读者若在不同软件中得到相反的强度顺序，应先核对数据定义，再谈背景扣除。把定量数组与用来排版的显示图分开保存，可以让图像直观与计算含义同时清楚。

条带形状本身也能帮助定位问题。两侧较强而中间较弱，可能需要检查转移接触和局部气泡；一整条泳道弯曲或扩散，则要把注意力移到加样、盐分和电泳条件。所有样品都在同一高度出现狭窄污点，与只有某一生物处理出现额外完整条带，对实验判断的意义不同。先保留全膜及相邻背景，再用对应的操作记录缩小原因，比只查看裁剪后的一条横线更有效。这些观察最后应回到一个可检验的调整，例如重做相同样品的较低上样量、改变转移条件，或换用识别不同表位的抗体核对身份。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Towbin, Staehelin & Gordon (1979): Electrophoretic transfer of proteins](https://doi.org/10.1073/pnas.76.9.4350)

   电转移原始发表记录。
2. [Towbin (1988): Citation Classic retrospective](https://garfield.library.upenn.edu/classics1988/A1988M295200001.pdf)

   作者回顾抗体接近凝胶蛋白的困难与电转移思路。
3. [Taylor et al. (2013): A Defined Methodology for Reliable Quantification of Western Blot Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC3840294/)

   稀释系列、数字与胶片成像、总蛋白归一化；真实图3。

   Creative Commons Attribution, version not stated by article; Fig. 3 reproduced
4. [Thermo Fisher: Western blot sample preparation](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-gel-electrophoresis-information/western-blot-protocols/western-blot-sample-preparation.html)

   提取条件、蛋白保护和定量兼容性。
5. [Thermo Fisher: Total protein normalization](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-gel-electrophoresis-western-blot/protein-gel-electrophoresis-western-blot-imaging-analysis/total-protein-normalization.html)

   总蛋白分母及响应范围检查。
6. [Uhlén et al. (2016): A proposal for validation of antibodies](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335836/)

   按具体实验应用建立抗体身份证据。
7. [ImageJ: Analyze menu and gel analysis](https://imagej.net/ij/docs/menus/analyze.html#gels)

   泳道剖面、像素积分与区域保留。
