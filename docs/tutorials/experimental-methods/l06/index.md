# ELISA：把分子识别转化成浓度

Source: https://ml-biomat.com/tutorials/experimental-methods/l06/
Language: zh-CN

看懂显色、弯曲的标准曲线、稀释与加标，建立从一孔读数到研究结论的完整计算链。

## 一滴培养液，怎样告诉我们细胞发出了多少信号

把免疫细胞放到两种材料表面，一天后取出少量培养液，肉眼可能看不出差别。细胞却可能向周围释放不同数量的信号蛋白，招来其他细胞或改变邻近组织的活动。研究者想知道的不是培养液总体有多浑浊，而是其中某一种分子有多少。ELISA，也就是酶联免疫吸附测定，把抗体的识别能力和酶的放大能力连接起来：先把目标从复杂混合物中留住，再让留下来的酶制造可测量的颜色，最后通过已知浓度的标准品把颜色换算成浓度。

可以把这件事想成在许多不同形状的零件中寻找一种螺母。捕获工具负责挑中它，报告工具负责把“挑中了多少”变成容易读取的信号。二者分工非常重要。读板仪测到的是光学信号，不直接数蛋白分子；抗体决定哪些分子参与检测，酶、底物、反应时间和读数条件共同决定这些分子最终对应多深的颜色。标准曲线把这一整套过程校准到浓度尺度上。读懂一张 ELISA 数据表，实际上是在读懂这条从识别到校准的路线。

本章从常见的夹心法讲起，再建立一个完整的浓度计算例子。你会看到为什么标准曲线会弯曲、为什么同一份样品稀释后折算出的浓度可能反而升高，以及为什么漂亮的拟合线还需要独立质控来检查。真实发表的标准曲线图展示试剂批次之间的差异；可运行的构造数据则让每个数字都有明确的已知起点。两者结合后，读者可以把一孔颜色、一条曲线和一个生物学结论逐步连接起来。

先确定最终需要回答的量。例如每毫升培养液含有多少皮克目标蛋白，描述的是取样时液体中的浓度；培养液总体积乘上浓度，得到的是这段收集过程中留在液体中的总量。若要比较每枚细胞的分泌行为，还要考虑细胞数量及其随时间的变化、取样时间和培养液更换。这些分母不是在最后随便挑一个除数。预先说明比较的是每孔释放量、单位体积浓度，还是按细胞数量归一化的积累量，后面的采样设计才会与问题一致。

## 识别、洗涤与显色，各自承担哪一段工作

夹心法先在固体表面固定捕获抗体，再加入样品，让目标结合到表面。洗去没有留下的组分后，检测抗体结合目标上的另一个可及部位。检测抗体可以直接携带酶，也可以通过其他连接方式引入酶。最后加入底物，酶不断催化生成能够被光学系统读出的产物。这个结构像从两侧确认同一件物品的身份：两支抗体需要同时接触目标，不能互相挡住。对于很小、只有有限可及表位的分子，合适的检测构型可能不同。

竞争法提供了另一种路线。样品中的目标与带标记的分子，或与固定在表面的结合对象，竞争有限的识别机会。在常见竞争构型中，样品目标越多，最终留下的报告信号反而越少。因此，“颜色更深就是含量更高”并不是所有免疫测定共同遵循的规则。先画出谁被固定、谁携带报告酶、谁在洗涤后留下，信号方向便可以从分子关系中推出来。选择拟合函数之前，先知道这条曲线为什么向上或向下。

1971 年，Engvall 与 Perlmann 发表了以 ELISA 命名的免疫球蛋白定量工作，同年 van Weemen 与 Schuurs 发表了使用抗原—酶结合物的免疫分析。这些工作把酶的催化报告引入免疫识别，使少量被识别分子的存在能够转成不断积累的信号。下面画的是现代夹心法的原理，帮助理解这个连接思想。历史上的方法发展并非把现成的读板仪装上去便结束了：固定、分离未结合组分和保持报告反应可比较，都是把识别变成定量所需要解决的环节。

![现代夹心 ELISA 的原创原理图：固定捕获、靶标、检测与酶产物；上方连接 1971 年的两组酶免疫分析工作。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b4824536ff05ca44d77ad1e5.svg?v=b4824536ff05)

图 1现代夹心 ELISA 的原创原理图：固定捕获、靶标、检测与酶产物；上方连接 1971 年的两组酶免疫分析工作。

洗涤在这里相当于把没有通过识别步骤的报告工具带走。如果游离酶或带酶抗体留在孔里，它们同样能够催化显色，于是空白也变深。显色时间则决定了产物有多久可以积累。先加底物的孔若比后加的孔多反应几分钟，颜色差可能包含时间差。合理安排加液和终止的顺序，使各孔经历相近的反应时间，能让标准和样品共享同一把尺。使用何种底物、终止条件和读取波长，需要与具体测定体系对应，不能仅凭“ELISA”这个名称确定。

常见的颜色读数是吸光度，表示通过样品的光相对于参照光减少了多少。它是一个对数比值，没有长度或质量单位。对于给定光程和同一种显色产物，吸光度能够反映产物浓度；而产物浓度又取决于酶反应。这两层关系解释了为什么吸光度与目标蛋白浓度不一定成直线。即使光学读数处于良好范围，抗体结合的容量、检测过程和反应动力学也会让整条标准曲线发生弯曲。

$$
A=-\log_{10}\left(\frac{I}{I_0}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 吸光度，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | 穿过样品的光强，与参照同单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 参照光强，与透射光同单位 |

吸光度把透光比例转成对数尺度；相同波长和仪器条件下透光比例 0.1 对应 A=1，0.01 对应 A=2。其单位相消。吸光度对应显色产物，目标浓度通过整套测定的标准曲线获得。

## 在加样之前，把样品、标准与质控放到同一张地图上

标准品是一组已知目标浓度的样品，作用是建立浓度与读数的关系。零浓度标准仍含有相应稀释液和检测试剂，可以显示这套测定在没有目标时的基础信号。独立质控样品则用来检查通过标准曲线反算出的浓度是否稳定：它不参与拟合，而是像考试中的新题，用已经建立的曲线给出预测。若一组标准恰好共同配错了浓度，它们仍可能排成一条非常平滑的曲线；独立制备的质控更容易发现这类共同偏差。

标准梯度常用连续稀释配制，浓度相邻成固定倍数，便于覆盖较宽范围。例如每次取相同体积的上一管溶液与稀释液混合，就得到二倍稀释。每一步都要充分混匀再取下一份，否则误差会沿着后续梯度传递。标准与样品的基质也值得提前考虑。“基质”就是目标之外的那一整套环境，例如培养基、血清蛋白、盐、材料浸出组分。它们可能改变抗体结合、目标稳定性和报告反应，使相同目标浓度产生不同的读数。

复孔帮助观察同一样品重复加液与测量的分散。两个或三个复孔若差别很大，先回到孔位置、移液、气泡、洗涤和反应时间寻找原因。复孔一致，则说明这几次技术重复相近；它们仍来自同一份样品，不能代替独立培养或独立材料样品。板图应同时保存样品身份、稀释倍数、标准浓度和复孔关系。用空间位置把这些信息连起来，才容易看出边缘偏高、某一列异常或某次加液造成的规律。

收集培养上清时，时间也是样品的一部分。相同浓度可以来自较少细胞较长时间的积累，也可以来自较多细胞较短时间的积累。材料可能吸附目标蛋白，让液体中留下的量减少；目标还可能在培养或保存过程中降解。把“细胞释放到系统中的量”与“取样时液体中可被检测的量”区分开，便能安排相应补充实验，例如向无细胞材料体系加入已知目标，观察经过相同接触时间后的回收情况。这直接服务于材料—分子相互作用的解释。

样品若需要多级稀释，最终倍数来自每一级倍数相乘。先二倍、再四倍，进入检测孔前的样品就是原样的八分之一；若试剂流程还包含与标准完全相同的反应混合步骤，应按标准定义使用相应浓度尺度。记录“进入测定前”的样品稀释和测定本身的固定加液步骤，可以避免把同一个体积变化计算两次。浓度单位也要贯穿一致：皮克、纳克和微克之间相差千倍，显示小数位再多也补救不了单位跳转。

## 标准曲线为什么弯曲，怎样沿着它找回浓度

在低浓度端，信号接近空白，少量目标带来的变化容易与背景波动混在一起。进入中间范围后，浓度变化能带来明显的信号变化。更高浓度时，检测过程逐渐接近上限，曲线又变平。四参数逻辑斯蒂曲线用下平台、上平台、中点位置和陡峭程度描述这种形状，简称 4PL。它是用于校准的经验模型，而不是把整个抗体和酶反应都精确还原的化学方程。选择模型的关键，是它能否在工作范围内把已知浓度可靠地找回来。

本例设置下平台 0.05、上平台 2.05，中点浓度为每毫升 100 皮克，形状参数为 1.2。浓度正好在中点时，吸光度位于两平台之间的一半，也就是 1.05。公式中的浓度比把量纲消去，因此把浓度改用其他单位时，中点浓度也要一起换算。横轴采用对数刻度只是为了把多倍变化展开得更清楚；它不会把零浓度变成一个普通对数点。程序保留零浓度标准参与拟合，在主要对数曲线图中单独处理其显示。

$$
y=a+(d-a)\frac{c^b}{m^b+c^b}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 测定吸光度，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/0aa7bfcc5af82046a01fa888.svg) | 低与高平台吸光度，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 测定对应的目标浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 半幅响应对应浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 正的形状参数，无量纲 |

本式描述向上增长的四参数校准曲线，浓度非负、d大于a，m和b为正。a=0.05、d=2.05、m=100、b=1.2 时，c=100 给出 y=1.05。比值中的浓度幂具有相同单位，最后相消；它是经验校准关系。

计算未知样品时，先从纵轴的吸光度走到曲线，再向横轴找浓度。公式的反函数把这个图上操作写成可以重复执行的计算。例如吸光度 1.05 对应每毫升 100 皮克；若这是原样八倍稀释后的样品，原样浓度便是每毫升 800 皮克。稀释倍数乘在反算得到的浓度上。直接把吸光度乘八再代入曲线，相当于假设这条弯曲关系能够按直线缩放，会把读数送到完全不同的位置，甚至超过曲线的上平台。

$$
c=m\left(\frac{y-a}{d-y}\right)^{1/b},\qquad C_0=Dc
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 由读数反算的稀释样品浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 半幅响应浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 未知样品吸光度，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/0aa7bfcc5af82046a01fa888.svg) | 校准低、高平台，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 曲线形状参数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/8e1f255f71ebe5898eee968b.svg) | 折算原样浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 测定前累计样品稀释倍数，无量纲 |

先将 4PL 移项反解，再按浓度守恒恢复稀释。反函数适用于 a<y<d，样品须位于已检查的工作区间。y=1.05 对应 c=100；八倍稀释给 C0=800。示例拟合原始吸光度，a包含基础响应，不再额外扣一次空白。

拟合时，每个标准点都带有测量分散。如果高信号的波动通常更大，让所有点具有相同权重，可能使高信号区域主导拟合。加权拟合按误差大小调整各点的影响，权重需要来自适合该测定的误差模型或充分的重复数据。本例的数据由明确给定的噪声模型生成，因此程序用这个已知标准差进行加权。实际实验中，仅凭两个复孔估计复杂的误差规律通常不稳妥，可以通过多轮标准和质控数据检查适合的权重与模型。

空白处理也要前后一致。本例直接拟合原始读数，让低平台包含基础响应；另一种流程可以先从标准与样品同时减去同一个空白估计，再拟合校正后的曲线。两种表示都需要与相应的反函数配套。只给样品扣空白，或者拟合原始曲线后又重复扣一次空白，都会把样品相对于曲线的位置移走。保留原始与校正后的两列数值，可以让这些操作清楚可追踪。

![实际代码输出的构造标准曲线、残差、固定读数偏差反算的浓度区间和板图。A的零标准参与拟合但不置于对数横轴；D空白灰区为未使用孔。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9c12f8261a00fc550644acd5.svg?v=9c12f8261a00)

图 2实际代码输出的构造标准曲线、残差、固定读数偏差反算的浓度区间和板图。A的零标准参与拟合但不置于对数横轴；D空白灰区为未使用孔。

看图时，先检查标准点是否覆盖目标样品所在的区间，再看残差，也就是每个读数减去拟合值后的差。残差若在某段持续为正、另一段持续为负，可能提示模型形状不合适；个别孤立异常则需要结合孔位和操作记录排查。4PL 在对数浓度尺度上具有对称形状，某些测定需要允许不对称的五参数模型。增加参数的目的应当是改善独立浓度预测，而不是让线条更贴近每一个训练点。用独立低、中、高质控检查反算偏差，比只报一个接近一的拟合优度更能反映定量表现。

## 稀释与加标，让样品自己检验这把尺

如果同一份样品稀释两倍、四倍、八倍后，反算并折回原样的浓度接近一致，说明在这些条件下样品与标准的对应关系较为一致。这里的“稀释线性”描述的是校准后的浓度，不要求原始吸光度按稀释倍数成比例变化。相反，若越稀释，折算浓度越高，可以考虑某种干扰也随稀释减弱。先查看样品读数是否落在可靠范围，再结合回收实验检查基质，比直接把最高值当成真值更容易找到原因。

构造例子把原样浓度固定在每毫升 800 皮克，同时设置一种随稀释减弱的抑制：未稀释时只有六成有效响应，八倍稀释时达到九成五。校准模型本身完全正确，样品却因为响应改变而被读成较低浓度。没有噪声时，未稀释样品折算为 480，八倍稀释为 760，十六倍稀释为 780。这个例子把两个经常混在一起的问题拆开了：曲线算得正确，与样品是否像标准那样响应，是两项需要分别检查的条件。

## 同一份样品，稀释后为何得到不同的浓度？

校准曲线固定为正文的 4PL。构造的基质效应使有效浓度乘以“1−抑制强度/稀释倍数”。先反算浓度，再乘稀释倍数；调整吸光度偏差，观察曲线平坦区域的敏感性。

[Figure: 标准曲线、有效浓度和加入读数偏差后的反算位置](https://ml-biomat.com/tutorials/experimental-methods/l06/#L06-lab)

加标回收则向样品中加入已知量的目标，查看测得的增加量是否接近加入量。假设未加标样品为每毫升 40 皮克，按照最终体积加入相当于每毫升 25 皮克的目标，测得加标样品为 62。检测到的增加量是 22，回收率为百分之八十八。分子里减去原有的 40，是因为我们只想追踪新加入的那一部分。配制时要让未加标对照经历相同的体积变化，或者把原有浓度按最终体积修正，否则“加标造成的稀释”也会混进回收计算。

$$
\mathrm{Recovery}=100\%\,\frac{C_{\rm spiked}-C_{\rm unspiked}}{C_{\rm added}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/da2911810e849da2f484a127.svg) | 加标回收率，% |
| ![Formula](https://ml-biomat.com/static/agent-math/855aac15c18924e953f833e0.svg) | 加标后测得浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/b1bbfaaddb07df7e6f4b2bd5.svg) | 匹配最终体积的未加标浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/556105106ab656f403037742.svg) | 加入目标对最终体积的浓度贡献，pg/mL |

减去原有部分只保留新加入目标的测得增量，再与已知加入量比较。62−40=22，加入25，回收率88%。未加标对照与加标样品具有相同体积变化；各浓度使用相同稀释尺度。

![构造的基质抑制随稀释减弱，原样真值800pg/mL。橙色误差条为3个技术复孔的样本SD；右图为40、65、62pg/mL的加标回收例子。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f6e9be4ab0cc7f6b56db2734.svg?v=f6e9be4ab0cc)

图 3构造的基质抑制随稀释减弱，原样真值800pg/mL。橙色误差条为3个技术复孔的样本SD；右图为40、65、62pg/mL的加标回收例子。

加标位置会改变这个实验回答的问题。在已经制备好的培养上清中加入目标，主要检查检测阶段的基质响应；在材料接触或样品提取之前加入，则还把吸附、提取和保存损失包含进来。两者都很有用，但应按研究步骤解释。加入的纯化标准与样品中的天然目标也可能在结合伙伴、修饰或片段状态上不同，因此可以把加标回收与自然样品的稀释一致性结合起来。多个方向的检验能够把具体问题定位到取样、前处理或测定阶段。

稀释也有代价。它减弱干扰的同时，把目标浓度推向低端；过度稀释后，信号又会接近背景，浓度不确定性增加。交互中可以固定原样浓度，只增加稀释倍数，观察测量点如何沿曲线移动。再加入一个很小的吸光度偏差，比较中间段与平台附近折算结果的变化。这使“选择合适稀释度”成为一个有证据的平衡：把基质效应降到可接受水平，同时让目标落在经质控确认的工作区间。

## 误差条、批次变化与真正可比较的结果

相同的吸光度误差，在曲线不同位置会造成不同的浓度误差。曲线很陡时，纵向移动一点只对应较小的横向移动；平台附近，纵向的一点差异却可能对应很宽的浓度范围。本例中点的局部斜率为每单位浓度 0.006 吸光度，0.02 的读数变化约对应每毫升 3.33 皮克。这个局部估计解释了为什么不能把所有读数的可靠程度视为相同。图中直接用反函数计算相同上下偏差对应的浓度区间，让这个几何关系更直观。

复孔精密度可以用标准差和变异系数描述。标准差表示一组结果围绕平均值的分散大小，变异系数把它除以平均值，方便比较不同浓度尺度。例如三个反算浓度为 98、100、102，平均值是 100，样本标准差是 2，变异系数为百分之二。它描述这三个结果彼此有多接近，并不检查它们是否一起偏离真实浓度。若三孔都来自同一份配错的标准液，它们可以非常一致而共同偏低。

$$
\overline C=\frac{1}{n}\sum_{i=1}^{n}C_i,\quad s=\sqrt{\frac{\sum_{i=1}^{n}(C_i-\overline C)^2}{n-1}},\quad \mathrm{CV}=100\%\,\frac{s}{\overline C}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd0d870dfc8efaf0a79af99d.svg) | 复孔浓度平均值，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/971aeb8f6c70c0afe2138963.svg) | 第i个复孔反算浓度，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 复孔编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 复孔数量，至少2，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 样本标准差，pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd8c772d1a9221850e1289c.svg) | 变异系数，% |

样本标准差使用n−1以估计重复测量分散；CV再按正平均值归一化。98、100、102 的均值100、平方偏差和8、s=√(8/2)=2，因此CV=2%。它描述复孔精密度，独立样品与批次分散另行保留。

真实的批次差异可以比孔内分散更大。Feng 等人在 2019 年的研究中比较了不同批次试剂的标准曲线。下面图 A 显示同一标示浓度在不同批次对应不同的吸光度，图 B 展示批次内部和批次之间的变化。图 A 的误差条是标准差，各批次包含的曲线数量不同。沿固定吸光度画一条水平线，就能看见它与不同曲线交点的浓度不一样。这说明长期比较需要有贯穿各批次的共同质控，把“样品改变”与“测量标尺改变”区分开。

![Feng等2019年图2，CC BY4.0，完整转载。A为不同试剂批次标准曲线均值±SD，批次1–5分别28、19、8、4、9条；B比较批次1与5的单条曲线。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2061c20b4566f61a36dac64c.svg?v=2061c20b4566)

图 4Feng等2019年图2，CC BY4.0，完整转载。A为不同试剂批次标准曲线均值±SD，批次1–5分别28、19、8、4、9条；B比较批次1与5的单条曲线。

共同质控可以来自充分混匀后分装保存的一批样品，每次测定取一份，减少重复冻融带来的额外变化。若更换试剂批次，安排一组跨批次重复样品，有助于检查变化是整体平移、比例变化，还是某一浓度段特别明显。研究组别也应尽可能分布在不同板上，而不是把所有对照放在一板、所有处理放在另一板。这样的安排让板间变化有机会被识别，不会与处理效应完全重合。

低于可靠定量范围的样品，需要保留其测量信息和范围身份。它可能有可识别信号，但反算浓度分散过大；“能看见变化”与“能给出稳定浓度”是不同的能力。通过低浓度样品的偏差和精密度建立下限，通过高浓度样品与稀释回收建立上限，才能把曲线上的一段确认为工作区间。计算机可以对很远的曲线外侧继续给出数字，但实验设计应把样品调整回有标准和质控支撑的位置。

## 把完整计算链跑一遍，再解释生物学差异

完整程序先生成有重复孔的标准数据，再拟合曲线，随后分析同一原样的稀释系列。它导出标准表、稀释结果、示例板图和摘要，并把实际计算出的残差、误差传播和基质效应画出来。运行后可以从八倍稀释那一行开始，依次查看原始吸光度、反算的孔内浓度与折回原样的浓度。独立数值检查包含中点、反函数、稀释守恒、回收率和复孔变异系数，让每一步都能通过简单手算核对。

### 完整 Python：校准、反算、稀释与质控图

离线生成明确标记的构造数据，执行加权4PL拟合，输出逐孔CSV、摘要和实际图形；真实发表图随包提供。

```
"""Offline ELISA calibration, matrix effects and dilution experiment."""
from pathlib import Path
import argparse,csv,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';GREEN='#3c8a6a';PURPLE='#8160a1'
PARAMS=(.05,2.05,100.,1.2)
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def fourpl(c,a=.05,d=2.05,m=100.,b=1.2):
    c=np.asarray(c,dtype=float);return a+(d-a)*c**b/(m**b+c**b)
def inverse(y,a=.05,d=2.05,m=100.,b=1.2):
    y=np.asarray(y,dtype=float)
    with np.errstate(invalid='ignore',divide='ignore'):return m*((y-a)/(d-y))**(1/b)
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(606);levels=np.array([0,6.25,12.5,25,50,100,200,400,800,1600]);x=np.repeat(levels,3)
    sigma=.006+.008*fourpl(x);raw=fourpl(x)+rng.normal(0,sigma)
    fit,cov=curve_fit(fourpl,x,raw,p0=PARAMS,sigma=sigma,absolute_sigma=True,bounds=([0,1,1,.3],[.3,4,1000,3]),maxfev=10000)
    with (out/'standards.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['concentration_pg_ml','replicate','absorbance','constructed_noise_sd']);w.writerows(zip(x,np.tile([1,2,3],len(levels)),raw,sigma))
    dilutions=np.array([1,2,4,8,16,32]);original=800.;effective=original/dilutions*(1-.4/dilutions)
    sample_signal=fourpl(effective);sample_raw=sample_signal[:,None]+rng.normal(0,.01,(len(dilutions),3));back=inverse(sample_raw,*fit)*dilutions[:,None]
    with (out/'dilutions.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['dilution','replicate','true_original_pg_ml','matrix_fraction','absorbance','estimated_original_pg_ml'])
        for i,dil in enumerate(dilutions):
            for j in range(3):w.writerow([dil,j+1,original,1-.4/dil,sample_raw[i,j],back[i,j]])
    fig,ax=plt.subplots(figsize=(11,5));ax.set(xlim=(0,12),ylim=(0,6));ax.axis('off')
    for x0,stage in [(1.5,0),(5.5,1),(9.5,2)]:
        ax.add_patch(Rectangle((x0-1,1),2,.15,fc=BLUE));ax.plot([x0,x0,x0-.5,x0,x0+.5],[1.1,2,2.5,2,2.5],color=BLUE,lw=4)
        if stage>=1:ax.add_patch(Ellipse((x0,2.65),1,.6,fc=AMBER))
        if stage>=2:
            ax.plot([x0,x0,x0-.4,x0,x0+.4],[2.95,3.5,4,3.5,4],color=PURPLE,lw=4);ax.add_patch(Ellipse((x0+.55,4.2),.8,.55,fc=GREEN));ax.text(x0+.55,4.2,'E',ha='center',va='center',color='white')
            ax.scatter([x0+.4,x0+.8,x0+1.2],[4.9,5.2,4.8],color='#d7ac3f',s=70)
    for a,b in [(2.8,4.1),(6.8,8.1)]:ax.annotate('',xy=(b,2.5),xytext=(a,2.5),arrowprops={'arrowstyle':'->','lw':1.5})
    for x0,label in [(1.5,T('固定捕获抗体','Immobilized capture')),(5.5,T('结合样品中的靶标','Bind sample target')),(9.5,T('检测抗体、酶与产物','Detector, enzyme and product'))]:ax.text(x0,.45,label,ha='center',fontsize=10)
    fig.text(.5,.94,T('1971：Engvall–Perlmann 与 van Weemen–Schuurs 的酶免疫分析工作','1971: enzyme immunoassay work by Engvall–Perlmann and van Weemen–Schuurs'),ha='center',fontsize=12)
    fig.text(.5,.015,T('现代夹心法的原创示意；酶 E 把分子识别转成可积累的颜色信号。','Original modern sandwich schematic: enzyme E converts recognition into accumulating color.'),ha='center',fontsize=10);save(fig,'history')
    grid=np.geomspace(2,3000,300);fig,ax=plt.subplots(2,2,figsize=(11,8.4))
    ax[0,0].scatter(x[x>0],raw[x>0],s=18,color=BLUE,label=T('构造标准复孔','Constructed standard wells'));ax[0,0].semilogx(grid,fourpl(grid,*fit),color=AMBER,label='4PL');ax[0,0].legend(fontsize=8);ax[0,0].set(xlabel=T('浓度 / pg/mL','Concentration / pg/mL'),ylabel=T('吸光度','Absorbance'),title=T('A  信号随浓度上升后逐渐变平','A  Response approaches a plateau'))
    ax[0,1].scatter(x,raw-fourpl(x,*fit),color=PURPLE,s=20);ax[0,1].set_xscale('symlog',linthresh=5);ax[0,1].axhline(0,color='grey',lw=1);ax[0,1].set(xlabel=T('浓度 / pg/mL','Concentration / pg/mL'),ylabel=T('实测构造值 − 拟合值','Constructed observation − fit'),title=T('B  残差保留误差的方向','B  Residuals retain error direction'))
    y=fourpl(grid);low=inverse(y-.02);high=inverse(y+.02);ax[1,0].semilogx(grid,100*(high-low)/(2*grid),color=GREEN);ax[1,0].set(xlabel=T('真实浓度 / pg/mL','True concentration / pg/mL'),ylabel=T('±0.02 信号误差对应的半宽 / %','Concentration half-width from ±0.02 signal / %'),title=T('C  同样的信号误差，不同的浓度误差','C  Equal signal error, unequal concentration error'),ylim=(0,50))
    plate=np.full((8,12),np.nan);plate_levels=np.array([0,12.5,25,50,100,200,400,800]);plate[:,:2]=fourpl(plate_levels)[:,None]+rng.normal(0,.01,(8,2));plate[:6,3:6]=sample_raw;plate[6:,3:6]=fourpl([50,300])[:,None]+rng.normal(0,.01,(2,3))
    plate_cmap=plt.get_cmap('cividis').copy();plate_cmap.set_bad('#e1e5e6')
    im=ax[1,1].imshow(plate,cmap=plate_cmap,vmin=0,vmax=2);ax[1,1].set_xticks(range(12),range(1,13));ax[1,1].set_yticks(range(8),list('ABCDEFGH'));ax[1,1].set_title(T('D  示例板：标准、稀释系列、质控','D  Example plate: standards, dilution series, QC'));fig.colorbar(im,ax=ax[1,1],label=T('吸光度','Absorbance'),fraction=.04)
    fig.tight_layout();save(fig,'calibration')
    np.savetxt(out/'plate.csv',plate,delimiter=',',header='constructed demonstration plate; NaN unused')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));ideal=inverse(sample_signal)*dilutions
    ax[0].plot(dilutions,ideal,'o-',color=BLUE,label=T('无噪声、含基质效应','Noiseless, matrix effect'));ax[0].errorbar(dilutions,back.mean(axis=1),yerr=back.std(axis=1,ddof=1),fmt='s',color=AMBER,label=T('拟合反算，3 复孔均值 ± SD','Fitted inversion, mean ± SD of 3 wells'));ax[0].axhline(800,color=GREEN,ls='--',label=T('真实原样浓度','True original concentration'));ax[0].set_xscale('log',base=2);ax[0].set_xticks(dilutions,dilutions);ax[0].set(xlabel=T('稀释倍数','Dilution factor'),ylabel=T('折算原样浓度 / pg/mL','Back-corrected concentration / pg/mL'),title=T('A  稀释减弱构造的基质抑制','A  Dilution reduces constructed matrix suppression'));ax[0].legend(fontsize=8)
    ax[1].bar([0,1,2],[40,65,62],color=[BLUE,GREEN,AMBER]);ax[1].set_xticks([0,1,2],[T('未加标','Unspiked'),T('理论加标后','Expected spiked'),T('测得加标后','Measured spiked')]);ax[1].set(ylabel=T('浓度 / pg/mL','Concentration / pg/mL'),title=T('B  加入 25，测得增加 22：回收 88%','B  Add 25, recover 22: 88% recovery'));fig.tight_layout();save(fig,'matrix')
    fig,ax=plt.subplots(figsize=(8.2,12.6));ax.imshow(Image.open(Path(__file__).resolve().parent/'feng2019-figure2.png'));ax.axis('off');ax.set_title(T('真实实验：试剂批次改变标准曲线','Measured experiment: lot-dependent standard curves'),fontsize=12)
    fig.text(.5,.012,T('Feng 等，2019，图 2；CC BY 4.0。\nA：均值 ± SD；批次 1–5 的曲线数分别为 28、19、8、4、9。','Feng et al., 2019, Fig. 2; CC BY 4.0.\nA: mean ± SD; lots 1–5 contain 28, 19, 8, 4, 9 curves.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.07,1,1]);save(fig,'published')
    assert np.isclose(fourpl(100),1.05) and np.isclose(inverse(1.05),100)
    assert np.allclose(ideal,800*(1-.4/dilutions))
    cv=np.std([98,100,102],ddof=1)/100*100
    summary={'model':{'midpoint_signal':float(fourpl(100)),'inverse_midpoint':float(inverse(1.05)),'midpoint_slope':2*1.2/(4*100),'midpoint_delta_c_for_002':.02/(2*1.2/(4*100))},'dilution':{'no_matrix_original':float(inverse(fourpl(100))*8),'one_matrix':float(ideal[0]),'eight_matrix':float(ideal[3]),'sixteen_matrix':float(ideal[4])},'spike':{'recovery_percent':(62-40)/25*100},'precision':{'cv_percent':float(cv)},'fit':{'a':float(fit[0]),'d':float(fit[1]),'m':float(fit[2]),'b':float(fit[3]),'sample_eightfold_mean':float(back[3].mean())}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

练习时可以把基质抑制设为零，看不同稀释度是否回到同一个原样浓度；随后只增加读数噪声，观察低端与高端怎样变得不稳定；再改变标准曲线中点，比较同一信号对应的浓度。这样每次只改变一个测量环节，结果也能对应一个清楚原因。示例中的板图标明未使用的孔，不把它们填成零浓度；零读数、零标准和没有测量是三个不同状态，在表格中保留这种区别会让后续处理更可靠。

还可以用一个具体例子检查归一化的意义。两孔都测得每毫升 800 皮克，一孔培养液为 1 毫升，另一孔为 2 毫升，液体中目标总量便分别为 800 和 1600 皮克。若后一孔细胞数也恰好是前一孔的两倍，按终点细胞数计算的积累量又可能相同。随着细胞在收集期内增殖或死亡，终点数量也会偏离整段时间的平均数量。把浓度、体积、时长和细胞数分别保存，比只留下一个最终归一化数字更容易解释这些情况。

回到材料与细胞研究，最终解释可以沿着一条完整链条展开：在明确的培养时间和体积中取样，检查材料对目标的吸附及基质影响，使用同板标准与独立质控获得浓度，再按照问题选择总量或细胞相关分母。将各独立样品的数值、复孔精密度和必要的稀释回收信息放在一起，读者便能理解差异来自哪一个实验对象。ELISA 的价值由此显现：它把分子识别转化为可比较的测量，让一滴原本看不出区别的液体提供具体的研究证据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Engvall & Perlmann (1971): Quantitative assay of immunoglobulin G](https://pubmed.ncbi.nlm.nih.gov/5135623/)

   1971年ELISA原始发表的作者、标题与年份。
2. [van Weemen & Schuurs (1971): Immunoassay using antigen-enzyme conjugates](https://pubmed.ncbi.nlm.nih.gov/11945853/)

   同年抗原—酶结合物的免疫分析工作。
3. [Cox et al.: Immunoassay Methods, Assay Guidance Manual](https://www.ncbi.nlm.nih.gov/sites/books/NBK92434/)

   检测构型、独立质控、模型选择和加权校准。
4. [Thermo Fisher: Spike-and-recovery and linearity-of-dilution assessment](https://documents.thermofisher.com/TFS-Assets/LSG/Application-Notes/TR0058-Spike-and-Recovery.pdf)

   基质响应、加标位置与校准浓度尺度的稀释检验。
5. [Feng et al. (2019): A computational solution to improve biomarker reproducibility during long-term projects](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0209060)

   真实标准曲线批次差异与跨板共同质控；图2。

   CC BY 4.0; Fig. 2 reproduced without cropping
6. [SciPy: scipy.optimize.curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   sigma权重、参数约束与非线性拟合接口。
