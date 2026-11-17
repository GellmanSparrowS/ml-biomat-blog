# 扩散与渗透：分子怎样穿过材料

Source: https://ml-biomat.com/tutorials/experimental-methods/e05/
Language: zh-CN

把分子进入、内部运动与整体穿过分开测量，用浓度分布、时间滞后和荧光恢复读懂传输。

## 材料里面能走动，为什么还不一定穿得过去

一枚隐形眼镜既要保持形状，也要让氧气到达角膜；一层食品包装膜希望减少某些气体进入；细胞包埋在凝胶里以后，营养分子需要穿过材料才能抵达细胞。这些问题都涉及分子运动，但“在里面走得快”和“能够从一侧到另一侧”并不是同一个量。一个分子可能很愿意进入材料，却在内部移动缓慢；另一个分子在里面移动很快，却很少进入。扩散与渗透实验把这两个环节分开，使材料的通透性可以被解释，也能指导厚度、组成和界面设计。

扩散系数描述分子随机运动导致空间分布展开的快慢，常用长度平方除以时间作单位。渗透实验则通常把材料放在供体与接收体之间：供体一侧目标物较多，接收体一侧较少，连续测接收侧积累的量。它直接观察的是整个通道的净传输，包含进入材料、内部迁移和离开材料等步骤。两侧液体的混合、样品厚度和暴露面积也参与结果。因此，一条接收量曲线要变成材料参数，需要先交代装置怎样约束这些过程。

还需要区分“分子渗透”与“水的渗透”。如果两侧溶液组成不同，水可能因化学势差而移动，这通常称为渗透现象；若施加压力，液体整体穿过多孔材料，则还包含压差驱动流动。本节主要讨论没有显著整体流动时，目标溶质从浓度较高一侧向较低一侧的净传输。保持两侧液面和压力条件可比，是让这个实验定义成立的重要设计。实际研究若希望利用压力过滤或渗透压，就需要把水流量与溶质通量一起测量。

![原创科学史示意：Fick 的浓度梯度、Daynes 的穿膜过渡，以及 Axelrod 等的局部漂白恢复。图中几何和分子位置用于解释各方法测量对象，不复原某个历史装置的尺寸。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/aecb8f7d2d04df2cce8607a1.svg?v=aecb8f7d2d04)

图 1原创科学史示意：Fick 的浓度梯度、Daynes 的穿膜过渡，以及 Axelrod 等的局部漂白恢复。图中几何和分子位置用于解释各方法测量对象，不复原某个历史装置的尺寸。

这条研究线连接着几个不同年代的测量思想。Fick 在 1855 年讨论液体扩散，把浓度沿空间的变化与净通量联系起来；Daynes 在 1920 年研究气体通过橡胶膜时，关注建立传输过程所需的时间；到了 1976 年，Axelrod 等系统讨论荧光漂白后的恢复，用局部亮度变化研究分子运动。今天的膜实验、凝胶传输和细胞内动态测量沿用这些思想，却观察不同尺度。图中用原创示意把三种测量对象并列，便于在学习方程之前先认清各自究竟看到了什么。

## 许多无规则的小步，怎样形成有方向的净流动

在一个均匀液体里，单个分子不会知道哪里浓度更低。它受到周围分子的热运动影响，持续改变运动方向。若左侧分子比右侧多，某个短时间内从左向右跨过分界面的分子数，平均会大于反向跨过的数量。净传输由两边数量不对称产生，而不是因为每个分子都朝同一个方向行走。当两侧浓度相同，两个方向仍有交换，只是平均净量为零。这个图景能同时解释扩散的方向与平衡后的动态状态。

“梯度”可以先理解为单位距离上的变化。相同的浓度差如果分布在很短距离内，梯度更陡；如果隔着更长距离，梯度更缓。Fick 第一定律把净通量与这个梯度联系起来。通量按单位面积、单位时间计算，所以扩大暴露面积会增加总传输量，却不必改变单位面积上的材料行为。方程里的负号负责方向：当沿所选正方向浓度降低，浓度梯度为负，净通量便沿正方向。先确定坐标方向，再理解符号，公式就不再是一串需要硬记的字母。

$$
J=-D\frac{\mathrm{d}c}{\mathrm{d}x}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | 沿 x 正方向的净质量通量，μg cm^{-2} s^{-1}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 材料内扩散系数，cm²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 材料内目标物浓度，μg/cm³；1 cm³=1 mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 沿传输方向的位置，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/19c0c9a9adb9595e43d95dfa.svg) | 浓度对位置的变化率，μg/cm⁴。 |

在此稀溶质、恒定 D 的一维模型中，净量沿浓度下降方向。浓度在 0.05 cm 内由 50 降至 0 μg/cm³，梯度为 −1000 μg/cm⁴；D=10⁻⁶ cm²/s 给出 J=0.001 μg cm⁻² s⁻¹。

如果某个位置进入的分子多于离开的分子，它附近的浓度会上升；反过来则会下降。将这个局部守恒关系与通量联系起来，就得到描述浓度随时间变化的扩散方程。图中的热图没有在每个位置安排不同材料，而是让同一材料内部的浓度随时间建立：左侧保持较高浓度，右侧保持接近零，最初内部没有目标物。早期主要在入口附近变化，后来影响逐步传到更深位置，最后形成近似直线的浓度分布。直线表示各位置的净通量相同，材料内部不再继续积累。

![同一理想平膜模型的空间—时间热图与浓度剖面。膜厚 0.5 mm，D=10⁻⁶ cm²/s，入口膜内浓度 50 μg/mL，出口为零；颜色尺与曲线纵轴采用相同浓度定义。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/73e00a2caef8dd291b50338e.svg?v=73e00a2caef8)

图 2同一理想平膜模型的空间—时间热图与浓度剖面。膜厚 0.5 mm，D=10⁻⁶ cm²/s，入口膜内浓度 50 μg/mL，出口为零；颜色尺与曲线纵轴采用相同浓度定义。

随机步行带来一个很有用的尺度关系：走到更远处所需时间大致随距离的平方增长。若材料内部的有效扩散系数不变，将目标距离增加一倍，扩散时间尺度会增加到约四倍。这里说的是过程的特征时间，不是保证每个分子都在同一时刻到达。对于凝胶中的细胞，这个关系解释了为什么把构件做厚一点，供给问题可能突然变得突出；对于检测装置，把传输距离缩短往往比单纯延长等待更直接。具体比例系数还由几何和边界条件决定。

$$
t_{\mathrm{diff}}\propto\frac{\ell^2}{D},\qquad \frac{t_2}{t_1}=\left(\frac{\ell_2}{\ell_1}\right)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a91f47f932c9f9cb2951264a.svg) | 所选几何与观察标准下的扩散特征时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dac4cdb34a25b3b90b51bf8b.svg) | 特征传输距离，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 保持不变的扩散系数，cm²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4a242ab8839381eab37575ed.svg) | 两种几何相似情况的相应特征时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/354ae30840963888785d34f6.svg) | 两种情况的特征距离，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d9c6c40f15e6a090e4bcafe4.svg) | 表示成正比；比例系数由几何和特征时间定义确定。 |

相同 D、几何相似且采用同一观察标准时，距离由 0.05 增至 0.10 cm，时间比为 4。这里的比例规律不指定所有分子的到达时刻。

扩散系数也与所追踪的对象有关。小染料、带标记蛋白质、自由离子和与网络结合的分子群体，可以有不同的运动方式。温度、溶剂黏度和网络结构改变时，有效扩散系数也可能改变。若材料中存在不同方向的通道，沿不同方向的扩散还可以不同。初学时先从均匀、各向同性、稀溶液和恒定扩散系数建立理解；随后用方向比较、浓度变化或时间变化实验，判断这些简化与实际样品之间的联系。

## 进入多少与走得多快，共同决定通透性

把一块干净材料放入含目标分子的液体，等待分配接近平衡后，材料内外的浓度未必相同。某些分子偏爱材料内部的环境，内部浓度会更高；另一些分子更喜欢外部水相，内部浓度会更低。分配系数就是在明确浓度定义和条件下，用材料内浓度除以外液浓度。若外液为 100 μg/mL，材料内部为 50 μg/mL，分配系数为 0.5。它描述“进入的程度”，扩散系数则描述进入之后的移动，两者在机制上有不同含义。

在均匀平膜、稳定浓度差、无反应且两侧界面分配迅速达到平衡的近似下，稳态浓度分布近似线性。此时把膜内外的分配关系代入 Fick 定律，就得到净通量与外液浓度差的关系。本节将包含膜厚的系数记为 P，其单位是长度除以时间；它等于扩散系数乘分配系数，再除以膜厚。文献中也常把不除厚度的乘积称为渗透率，气体研究还可能以压力差为驱动力，所以比较数值时要同时看定义和单位。

$$
K=\frac{c_{m,\mathrm{eq}}}{C_{b,\mathrm{eq}}},\qquad P=\frac{DK}{L},\qquad J_{\mathrm{ss}}=P(C_d-C_r),\qquad \dot M=AJ_{\mathrm{ss}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | 同一浓度基准下材料/外液平衡分配系数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/75f0936fa6794f04552ffae1.svg) | 平衡时材料内部浓度，μg/cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/11000e938578f6b9d3f45892.svg) | 对应平衡外液浓度，μg/cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 本节包含膜厚的通透系数，cm/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 膜内扩散系数，cm²/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 膜厚，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9ac89127e3910a4715ad8104.svg) | 稳态净质量通量，μg cm^{-2} s^{-1}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aad6f74707cc379dcf3f69f1.svg) | 供体与接收体外液浓度，μg/cm³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/12d771b3a5eff76e275bd9c0.svg) | 单位时间穿过的质量，μg/s；点表示对时间求变化率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 有效暴露面积，cm²。 |

假设平膜均匀、界面分配迅速、外部液层影响小且无反应。D=10⁻⁶ cm²/s、K=0.5、L=0.05 cm 得到 P=10⁻⁵ cm/s；浓度差 100 μg/cm³、面积 1 cm² 给出 0.001 μg/s，即 3.6 μg/h。

取一个具体例子：膜厚 0.5 mm，也就是 0.05 cm；扩散系数为每秒一百万分之一平方厘米，分配系数为 0.5。计算得到 P 为每秒十万分之一厘米。供体浓度 100 μg/mL、接收侧接近零时，净通量为每平方厘米每秒 0.001 μg，也就是每平方厘米每小时 3.6 μg。暴露面积若为一平方厘米，总速率就是每小时 3.6 μg；面积增为两平方厘米，在其他条件相同时总速率加倍。这些数字都保留在示例的输出中，可逐步核对单位换算。

同一个通透系数可能来自不同组合。例如分配系数加倍而扩散系数减半，其乘积保持不变，稳态斜率就可能相同，但膜内储存量与建立稳态的过程会不同。这是为什么仅测后期一条直线，往往不足以同时确定“进入多少”和“走得多快”。可以另做平衡吸附或分配实验，或在适用条件下利用时间滞后获得扩散信息，再结合稳态通量求分配。每加一项独立测量，都在减少同一条曲线可能对应的不同机制。

外部液层也可以成为串联阻力。分子经过供体侧液层、材料本体和接收侧液层，稳定状态下各段通过的净量相同，总浓度差却分配在不同段上。增强混合后外部液层变薄，若总通量明显上升，说明此前有一部分驱动力消耗在液层中。材料很薄或很通透时，这种影响尤其容易显现。比较不同膜厚，并结合混合条件，可以判断测到的主要是材料内部路径，还是装置附近的传质过程。

## 把两间小室变成可以解释的实验

对多孔材料，“孔很多”并不直接等于某个分子容易穿过。通道是否彼此连通、实际路径是否弯曲、入口是否润湿以及孔壁是否吸附目标物，都会影响有效传输。显微图里一个很大的空隙，也可能是与另一侧不连通的局部空间。将结构成像与不同尺寸、不同表面性质的示踪分子比较，可以让这些问题分别显现。示踪物的选择因此应围绕实际需要运输的分子，而不是只挑一个最容易检测的染料。

一个基本扩散池由供体室、接收室和夹在中间的样品组成。真正参与传输的面积是开口暴露面积，不是裁下来的整片面积。密封边缘需要避免旁路：如果溶液沿夹具缝隙绕过材料，接收侧出现目标物并不能说明它穿过了材料本体。样品厚度应在与实验相近的水合和受力状态下测量，因为干膜厚度、自由溶胀厚度和被夹持后的厚度可能不同。对于柔软凝胶，还应检查夹持是否把它压薄或造成局部破损。

装样时排除贴在有效区域的气泡，让接收液真正接触整个表面。气泡可能减少润湿面积，也可能使局部传输路径发生变化。温度影响溶液和材料，因此需要给两侧足够时间接近设定状态，再定义实验起点。混合帮助每个室内浓度均匀，但不能让样品松动或产生压差驱动流。记录两侧体积、液位、实际暴露面积、样品方向和混合方式，能将几何与操作条件连接到后面的通量计算。

膜的完整性可以通过与研究对象合适的独立指标检查。致密膜关注裂纹和针孔，细胞屏障关注连续覆盖与屏障状态，组织样品还要考虑制备和保存的影响。电阻、示踪物通过或成像各自观察不同方面，选择取决于材料和研究目的。某个离子相关的电学指标变化，不一定与某个中性大分子的通量成简单比例。完整性检查的作用是识别研究定义之外的破损或旁路，同时保留样品本身真实的生物或材料差异。

分析流程沿用上一章的质量账本：接收侧取样后补液，需要把此前取走的目标物加回累计量，再除以面积，才得到累计单位面积传输量。接收液浓度应使用与实际介质匹配的标准曲线，并检查目标物在温育、过滤和容器中的稳定性与回收。供体侧也值得取适当样本，以确定浓度是否真的维持不变。实验结束时测供体残留、接收累计量以及材料内保留量，可以判断目标物是穿过了、仍储存在膜内，还是在处理过程中改变了所测形式。

有限体积会改变长期驱动力。供体只有有限目标物时，随着传输它的浓度下降；接收侧若不断积累，浓度又会上升，两边的差逐渐变小。即使膜性质完全不变，曲线也会弯向平台。示例把一个 2 mL、初始 100 μg/mL 的供体与一个 10 mL 空白接收体连接起来，在忽略膜储存的两室模型中，最终两边浓度相同，但接收侧质量更大，因为它的体积更大。这个平台由守恒和体积决定，不需要假设膜突然失效。

## 从后期斜率和时间滞后拆出两个信息

刚开始实验时，膜内部还没有建立稳定的浓度分布。入口已经有分子进入，出口的通量却需要随内部浓度传播逐渐增加。经过这个过渡阶段后，若边界条件保持，累计接收量会接近一条直线。把后期直线向时间轴延长，与时间轴相交的位置称为时间滞后。它不是“第一个分子到达”的时间，也不是仪器第一次检出信号的时间，而是整个过渡过程相对于后期稳定速率形成的几何截距。

$$
M(t)\simeq AJ_{\mathrm{ss}}(t-t_{\mathrm{lag}}),\qquad t_{\mathrm{lag}}=\frac{L^2}{6D},\qquad D=\frac{L^2}{6t_{\mathrm{lag}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46f382af9057c20a2d8676c0.svg) | 累计穿过膜到达接收侧的质量，μg。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 有效暴露面积，cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9ac89127e3910a4715ad8104.svg) | 稳态通量，μg cm^{-2} s^{-1}。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 实验时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f8ee0947ec3a7b9f620bb565.svg) | 稳态直线外推到时间轴的截距，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 均匀平膜厚度，cm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | 浓度无关的膜内扩散系数，cm²/s。 |

适用于初始无目标物、入口浓度固定、出口接近零的平膜。L=0.05 cm、D=10⁻⁶ cm²/s 给出 416.667 s，即 6.944 min。线性表达式用于后期外推；早期累计量使用完整过渡解。

在均匀平膜、初始无目标物、恒定扩散系数、入口固定浓度和出口接近零的模型中，滞后与厚度平方成正比，与扩散系数成反比。前面的 0.5 mm 膜给出约 416.7 s，即 6.94 min 的时间滞后。厚度加倍以后，稳态通量减半，而滞后增加到四倍。这两个变化分别来自路程对稳定梯度和对建立过程的影响。把它们同时画出来，能比单独报告一个通透系数提供更多结构线索。

![构造数据四联图：稳态直线与滞后、拟合起点敏感性、厚度系列和有限体积效应。D 是另一个忽略膜储存的两室模型，用于展示外部浓度差变化；A—C 保留固定边界平膜的内部过渡。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1b8555dd5e947a34b497e08f.svg?v=1b8555dd5e94)

图 3构造数据四联图：稳态直线与滞后、拟合起点敏感性、厚度系列和有限体积效应。D 是另一个忽略膜储存的两室模型，用于展示外部浓度差变化；A—C 保留固定边界平膜的内部过渡。

拟合窗口需要从曲线和残差中选择。若把尚在建立浓度分布的早期点也拟合成直线，斜率与截距会一起偏移。示例逐步推迟拟合起点，观察估计滞后是否稳定；合适时间窗内参数趋于一致，提供了一个可检查的依据。若继续延长到供体耗竭、接收侧积累或膜溶胀明显的阶段，后期也可能偏离原模型。于是，最长的拟合区间并不自动拥有最清楚的物理含义，关键是区间内的实验条件能否维持对应假设。

装置本身也会带来时间响应。管路死体积、检测器响应和充分混合所需时间，都可能增加看起来像“膜滞后”的延迟。可以利用不含待测膜的装置对照、已知传输特性的参照物或独立响应测试，量化这些贡献。气体膜研究和液体扩散池的驱动力、单位与检测方式不同，但都遵循这一逻辑：先理解测量链条中的时间，再把剩余的传输过程归到材料上。这样得到的参数更容易用于厚度改变或装置改变后的预测。

## 厚度、扩散与分配，各自留下什么特征

固定供体浓度 100 μg/mL、接收侧零浓度、面积 1 cm²。曲线采用完整平膜过渡解，虚线为稳态后期外推。

[Figure: 穿膜累计量与稳态外推](https://ml-biomat.com/tutorials/experimental-methods/e05/#E05-plot)

## 不等分子穿过整块材料，也能观察局部运动

荧光漂白恢复实验选择另一条观察路径。先让一小片区域中的荧光分子变暗，再用较弱的光观察这片区域怎样重新变亮。变亮通常来自周围未漂白分子进入，同时暗分子离开；它不要求原来被漂白的每个分子重新发光。1976 年 Axelrod 等建立的分析把恢复过程与分子运动、流动和可动群体联系起来。对于凝胶和细胞环境，这种局部方法可以在不建立整个样品的宏观浓度差时，观察某个空间尺度上的动态。

首先需要三个亮度：漂白前、漂白刚结束时和充分恢复后的平台。恢复了多少占最初损失亮度的比例，可以作为适用模型中的可动比例。若归一化漂白前亮度为 1，漂白后降为 0.2，平台回到 0.8，那么最初损失 0.8，恢复 0.6，可动比例为 0.75。这个比例依赖观察时长与测量模型：在当前时间窗内没有恢复的群体，可能真正固定，也可能只是交换很慢。延长时间或改变漂白区域大小，可以进一步区分这些情况。

$$
f_{\mathrm{mob}}=\frac{I_{\infty}-I_0}{I_{\mathrm{pre}}-I_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43f47e963875c759940d11ea.svg) | 按此恢复模型估计的可动比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c59d25a349209f75166a8a12.svg) | 充分恢复的平台亮度，已作一致背景与采集漂白校正，任意一致强度单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | 漂白刚结束时的亮度，与其余亮度采用同一单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1056405dcb44d58478d34a61.svg) | 漂白前亮度，与其余亮度采用同一单位。 |

用实际恢复的亮度除以最初损失的亮度。Ipre=1、I0=0.2、I∞=0.8，得到 0.6/0.8=0.75。观察时长足以确定相应平台，且光漂白与背景等已按测量模型处理。

漂白区域越大，周围分子填补这个区域通常需要越久。示例采用理想二维高斯漂白模型，把中心亮度的恢复与区域尺度相连；图中半径从 5 μm 增为 10 μm，达到相同恢复比例的时间增加四倍。它展示距离平方关系如何出现在显微实验中。若改变区域尺度后时间不按这个趋势变化，就可以进一步考察结合与解离、整体流动或不均匀结构的作用。具体扩散系数的计算应采用与漂白光斑、成像维度和实际观测区域匹配的模型。

![构造的理想二维高斯漂白图像与中心亮度曲线，统一颜色尺度 0—1，标尺 5 μm。默认扩散系数 1 μm²/s、半径 5 μm、可动比例 0.75；曲线比较区域大小与可动比例，图像不作为显微实测。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c3eab5f75c9573031ee97361.svg?v=c3eab5f75c95)

图 4构造的理想二维高斯漂白图像与中心亮度曲线，统一颜色尺度 0—1，标尺 5 μm。默认扩散系数 1 μm²/s、半径 5 μm、可动比例 0.75；曲线比较区域大小与可动比例，图像不作为显微实测。

实际图像需要校正背景、采集过程中的持续光漂白和样品漂移。一个未受强漂白的参考区域可以帮助观察整体亮度是否下降；背景区域帮助扣除相机和介质的信号。漂白脉冲持续期间分子也可能移动，若把结束后的亮度分布误当成最初设定的锐利边界，拟合就会改变。恢复曲线还可能受可逆暗态、标记物与材料结合以及光照改变局部环境的影响。先检查原始图像和空间分布，再解释一条平均亮度曲线，能保留这些重要线索。

局部恢复与整膜通量是互补的信息。局部运动快，可能说明分子在水通道内移动容易；若材料入口分配很低，整体穿膜量仍可以很小。反过来，材料中保留了大量目标物，也可能伴随较慢的局部运动。将分配、局部扩散与宏观渗透放在一起，便能区分进入、移动和通过三个环节。对于会被细胞消耗或会与网络反应的分子，还需要增加反应或消耗的测量，才能把输运与去向联系起来。

## 用完整计算连接空间图像和接收量曲线

参数对几何误差的敏感程度也不同。直接由稳态斜率、面积和外液浓度差计算本节定义的 P 时，不需要再输入膜厚；由时间滞后反推扩散系数时，膜厚却以平方进入计算。若把厚度高估百分之十，其他输入不变，推算的扩散系数就会高估约百分之二十一。对于易溶胀样品，这个差别说明为什么厚度测量应与传输实验处在相近状态，并记录不同位置的厚度变化，而不是只使用制样模具的名义尺寸。

分配实验也需要明确所测分子群体。材料内的总目标物可以包括能够移动的分子，以及结合在较固定位置的分子。如果直接把总吸入量代入只描述可动溶质的模型，推算的扩散系数就会改变含义。将吸入过程与转移到空白介质后的释放一起测量，可以观察可逆性和缓慢交换，再用局部荧光运动补充信息。这些观察帮助判断一个简单的溶解—扩散描述是否足够，或是否需要明确加入储存与结合过程。

下面的示例计算一个初始不含目标物的平膜，在固定入口浓度与零出口浓度下怎样建立分布。程序导出位置—时间浓度数组、构造的接收质量观测、拟合参数以及四幅图。空间热图和累计接收量来自同一组参数，因此可以在图间追踪过程：先看入口附近逐渐变亮，再看出口通量逐渐接近稳定，最后看累计曲线接近直线。计算还检查长时间结果与独立稳态表达式一致，以及初始累计接收量为零。

### 完整 Python：平膜浓度场、时间滞后与局部恢复

代码导出浓度数组、构造接收量、拟合结果与四幅图。完整平膜解接受零时刻与后期稳态两种独立条件检查。

```
"""Planar diffusion, steady permeation, time-lag analysis and idealized FRAP."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch,Circle

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def permeated(time,D=1e-6,L=.05,K=.5,C=100.,area=1.):
    t=np.atleast_1d(time).astype(float);n=np.arange(1,201)[:,None]
    correction=np.sum((-1.)**n/n**2*np.exp(-D*n*n*np.pi**2*t[None,:]/L**2),axis=0)
    q=area*D*K*C/L*(t-L**2/(6*D)-2*L**2/(np.pi**2*D)*correction)
    return np.where(t==0,0,np.maximum(q,0))

def profile(x,time,D=1e-6,L=.05,K=.5,C=100.):
    x=np.asarray(x);n=np.arange(1,201)[:,None]
    if time==0:return np.where(x==0,K*C,0.)
    return K*C*(1-x/L-2/np.pi*np.sum(np.sin(n*np.pi*x/L)/n*np.exp(-D*n*n*np.pi**2*time/L**2),axis=0))

def frap_center(time,D=1.,radius=5.,mobile=.75,depth=.8):
    return 1-depth*((1-mobile)+mobile*radius**2/(radius**2+4*D*np.asarray(time)))

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.2))
    for a in ax:a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    ax[0].add_patch(Rectangle((1,2),8,6,facecolor='#e2eef0'));rng=np.random.default_rng(505)
    ax[0].scatter(rng.uniform(1.5,4.8,40),rng.uniform(2.5,7.5,40),s=12,color='#186e83');ax[0].scatter(rng.uniform(5.2,8.5,12),rng.uniform(2.5,7.5,12),s=12,color='#186e83');ax[0].add_patch(FancyArrowPatch((3,1.5),(7,1.5),arrowstyle='->',mutation_scale=17,color='#cd803f'));ax[0].set_title(tr('1855 · Fick：浓度梯度与通量','1855 · Fick: gradient and flux'));ax[0].text(5,.5,tr('从高浓度到低浓度的净传输','Net transfer from high to low concentration'),ha='center',fontsize=9)
    ax[1].add_patch(Rectangle((1,2),3.5,6,facecolor='#a2cdd9'));ax[1].add_patch(Rectangle((5.5,2),3.5,6,facecolor='#e2eef0'));ax[1].add_patch(Rectangle((4.5,2),1,6,facecolor='#8160a1'));ax[1].text(2.6,5,tr('供体','Donor'),ha='center');ax[1].text(7.3,5,tr('接收体','Receiver'),ha='center');ax[1].add_patch(FancyArrowPatch((3,1.5),(7,1.5),arrowstyle='->',mutation_scale=17,color='#cd803f'));ax[1].set_title(tr('1920 · Daynes：穿膜的时间滞后','1920 · Daynes: permeation time lag'));ax[1].text(5,.5,tr('膜内先建立浓度分布','A concentration profile develops in the membrane'),ha='center',fontsize=8.5)
    ax[2].add_patch(Rectangle((1,2),8,6,facecolor='#3c8a6a'));ax[2].add_patch(Circle((5,5),1.4,color='#123d36'));ax[2].add_patch(FancyArrowPatch((2,5),(4,5),arrowstyle='->',mutation_scale=17,color='white'));ax[2].add_patch(FancyArrowPatch((8,5),(6,5),arrowstyle='->',mutation_scale=17,color='white'));ax[2].set_title(tr('1976 · Axelrod 等：漂白后的恢复','1976 · Axelrod et al.: recovery after bleaching'));ax[2].text(5,1,tr('跟随明亮分子进入暗区','Follow bright molecules entering a bleached region'),ha='center',fontsize=9);fig.tight_layout();save(fig,'history')
    x=np.linspace(0,.05,201);times=np.linspace(0,1800,181);field=np.array([profile(x,t) for t in times]);fig,ax=plt.subplots(1,2,figsize=(11,4.8));im=ax[0].imshow(field,origin='lower',aspect='auto',extent=(0,.5,0,30),cmap='cividis',vmin=0,vmax=50);fig.colorbar(im,ax=ax[0],label=tr('膜内浓度 / μg mL⁻¹','Membrane concentration / μg mL⁻¹'));ax[0].set(xlabel=tr('膜内位置 / mm','Position in membrane / mm'),ylabel=tr('时间 / min','Time / min'),title=tr('A  浓度如何逐渐建立','A  Development of concentration'))
    for t in [30,120,600,1800]:ax[1].plot(x*10,profile(x,t),label=f'{t/60:g} min')
    ax[1].plot(x*10,50*(1-x/.05),'--',color='#8f979a',label=tr('稳态','Steady state'));ax[1].set(xlabel=tr('膜内位置 / mm','Position in membrane / mm'),ylabel=tr('浓度 / μg mL⁻¹','Concentration / μg mL⁻¹'),title=tr('B  从弯曲分布到稳定梯度','B  Curved profiles approach a stable gradient'));ax[1].legend(fontsize=9);fig.tight_layout();save(fig,'profiles')
    t=np.linspace(0,7200,121);q=permeated(t);noisy=q+rng.normal(0,.01,len(t));mask=t>=2400;slope,intercept=np.polyfit(t[mask],noisy[mask],1);lag=-intercept/slope;dfit=.05**2/(6*lag);pfit=slope/100
    np.savetxt(output/'permeation.csv',np.column_stack([t,t/60,q,noisy]),delimiter=',',header='time_s,time_min,ideal_received_ug,constructed_observed_ug',comments='');np.savez(output/'profiles.npz',position_cm=x,time_s=times,concentration_ug_ml=field)
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.3));ax=ax.ravel();ax[0].plot(t/60,noisy,'.',ms=3,label=tr('构造观测','Constructed observations'));ax[0].plot(t/60,slope*t+intercept,label=tr('40 min 后拟合','Fit after 40 min'));ax[0].scatter([lag/60],[0],color='#cd803f',zorder=5);ax[0].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('A  稳态斜率与时间轴截距','A  Steady slope and time-axis intercept'));ax[0].legend(fontsize=8)
    starts=np.arange(120,4201,120);fits=[]
    for start in starts:
        m=t>=start;ss,ii=np.polyfit(t[m],noisy[m],1);fits.append(-ii/ss/60)
    ax[1].plot(starts/60,fits);ax[1].axhline(.05**2/6e-6/60,color='#cd803f',ls='--');ax[1].set(xlabel=tr('拟合开始时间 / min','Fit start time / min'),ylabel=tr('估计滞后 / min','Estimated lag / min'),title=tr('B  拟合窗口的敏感性','B  Sensitivity to fitting window'))
    for L in [.025,.05,.1]:ax[2].plot(t/60,permeated(t,L=L),label=f'{L*10:g} mm')
    ax[2].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('C  厚度改变速率与滞后','C  Thickness changes rate and lag'));ax[2].legend(fontsize=9)
    finite_t=np.linspace(0,48*3600,300);qfinite=(100*2*10/12)*(-np.expm1(-1e-5*(1/2+1/10)*finite_t));ax[3].plot(finite_t/3600,qfinite,label=tr('有限供体与接收体','Finite donor and receiver'));ax[3].plot(finite_t/3600,.001*finite_t,'--',label=tr('恒定驱动力外推','Constant-driving-force extrapolation'));ax[3].axhline(200,color='#8f979a',ls=':');ax[3].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('D  有限容积改变长期驱动力','D  Finite volumes change long-term driving force'));ax[3].legend(fontsize=8);fig.tight_layout();save(fig,'analysis')
    grid=np.linspace(-15,15,181);xx,yy=np.meshgrid(grid,grid);r2=xx**2+yy**2;fig=plt.figure(figsize=(11,7));gs=fig.add_gridspec(2,3,height_ratios=[1,1.1]);axs=[fig.add_subplot(gs[0,j]) for j in range(3)]
    for a,tm in zip(axs,[0,5,30]):
        intensity=1-.8*(.25*np.exp(-r2/25)+.75*25/(25+4*tm)*np.exp(-r2/(25+4*tm)));a.imshow(intensity,origin='lower',extent=(-15,15,-15,15),cmap='viridis',vmin=0,vmax=1);a.plot([5,10],[-12,-12],color='#17333a',lw=3);a.text(7.5,-10,'5 μm',ha='center',color='#17333a',fontsize=8);a.set_title(f'{tm} s');a.set_xticks([]);a.set_yticks([])
    a=fig.add_subplot(gs[1,:]);ft=np.linspace(0,120,241)
    for radius,mobile in [(5,.75),(10,.75),(5,1)]:a.plot(ft,frap_center(ft,radius=radius,mobile=mobile),label=tr(f'半径 {radius} μm，可动比例 {mobile:.2f}',f'Radius {radius} μm, mobile fraction {mobile:.2f}'))
    a.set(xlabel=tr('漂白后时间 / s','Time after bleaching / s'),ylabel=tr('中心归一化亮度','Normalized central brightness'),title=tr('理想二维高斯漂白模型：空间扩散与可动比例','Ideal 2D Gaussian-bleach model: spreading and mobile fraction'));a.legend(fontsize=9);fig.tight_layout();save(fig,'frap')
    summary={'nominal':{'D_cm2_s':1e-6,'partition':.5,'thickness_cm':.05,'P_cm_s':1e-5,'steady_flux_ug_cm2_h':3.6,'lag_s':.05**2/6e-6,'lag_min':.05**2/6e-6/60},'fit':{'slope_ug_s':float(slope),'lag_s':float(lag),'D_cm2_s':float(dfit),'P_cm_s':float(pfit)},'scaling':{'double_thickness_flux_ratio':.5,'double_thickness_lag_ratio':4,'double_distance_time_ratio':4},'frap':{'prebleach':1,'immediate':float(frap_center(0)),'plateau':.8,'mobile_fraction':.75,'half_recovery_s':6.25,'at_half_recovery':float(frap_center(6.25))},'finite_bath':{'initial_mass_ug':200,'equilibrium_received_ug':100*2*10/12},'checks':{'q_at_zero':float(permeated([0])[0]),'late_mass_ug':float(permeated([7200])[0]),'late_linear_ug':.001*(7200-.05**2/6e-6)}}
    assert abs(summary['checks']['late_mass_ug']-summary['checks']['late_linear_ug'])<1e-9;assert abs(frap_center(6.25)-.5)<1e-12;assert np.all(field>=-1e-9)
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

图中的两室有限体积模型与固定边界平膜模型分别展示不同实验条件，前者忽略膜内储存并采用已建立的传输关系，后者保留膜内浓度建立过程。将它们分开，可以清楚看到曲线弯曲究竟来自材料内部过渡，还是来自外部驱动力变化。荧光恢复示例同样标为理想模型图像，不把计算亮度当作显微实测。实际数据分析可以沿用相应的量与单位，再根据所用装置、几何和观测方式选择匹配的模型。

尝试先只改变膜厚，再只改变分配系数，最后只改变扩散系数。厚度同时改变稳态斜率和时间滞后；分配系数在此线性模型中缩放传输量，却不改变浓度建立的时间尺度；扩散系数同时影响移动快慢和最终通量。这个三步比较帮助辨认不同参数在数据中留下的特征。若实际实验只测到其中一个特征，就可以据此决定增加分配测量、延长过渡期采样，或补充局部运动观察。

面向研究决策，最终报告应保留分子身份、材料状态、厚度面积、温度介质、浓度边界与参数定义。这样，一项通透性结果才能被用于不同厚度的设计、不同载体的比较，或细胞供给距离的判断。后面的细胞实验将从建立可比较的起点开始：即使材料传输性质相同，初始细胞数量、活性与空间分布不同，也会产生不同消耗和不同观察结果。把传输和生物状态都变成可测的量，两部分研究才能自然接起来。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Fick (1855). On liquid diffusion](https://doi.org/10.1080/14786445508641925)

   液体扩散与浓度梯度的历史原始论文。
2. [Daynes (1920). The process of diffusion through a rubber membrane](https://doi.org/10.1098/rspa.1920.0034)

   橡胶膜气体传输与时间滞后方法的历史工作。

   Historical reference; no assets reproduced.
3. [Imperial College London ReCoDe: Time Lag Analysis, A Theoretical Foundation](https://raw.githubusercontent.com/ImperialCollegeLondon/ReCoDe-permeation-analysis-app/main/docs/02-Theoretical-Background.md)

   边界条件、稳态外推、单位和时间滞后分析。
4. [COMSOL: Diffusion Equation](https://www.comsol.com/multiphysics/diffusion-equation)

   Fick 定律、局部守恒与恒定扩散系数条件。
5. [COMSOL: Diffusion Length and Timescales](https://www.comsol.com/multiphysics/diffusion-length-and-time-scales)

   距离平方与扩散时间尺度的联系。
6. [Axelrod et al. (1976). Mobility measurement by analysis of fluorescence photobleaching recovery kinetics](https://pubmed.ncbi.nlm.nih.gov/786399/)

   漂白恢复测量分子运动和可动群体的原始工作。

   Original abstract reference; no images reproduced.
7. [FDA (2022 draft). In Vitro Permeation Test Studies for Topical Drug Products Submitted in ANDAs](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/in-vitro-permeation-test-studies-topical-drug-products-submitted-andas)

   扩散池、屏障完整性、接收液与取样的实验设计。

   Official draft guidance; technical reading, with no assets reproduced.
