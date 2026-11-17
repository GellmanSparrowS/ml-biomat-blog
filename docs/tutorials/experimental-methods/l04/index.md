# EdU实验：追踪正在复制的DNA

Source: https://ml-biomat.com/tutorials/experimental-methods/l04/
Language: zh-CN

用一个有起止时间的分子标签，分清新 DNA 合成、阳性比例和细胞群体增长。

## 细胞变多之前，先看谁正在复制遗传信息

一种材料上第二天的细胞比第一天多，可能意味着细胞正在分裂；另一种材料上数量没有明显变化，也可能同时发生了分裂与流失。只比较终点数量，往往难以分清过程。EdU 实验把问题向前推进一步：在我们指定的一段时间内，哪些细胞合成了新的 DNA？DNA 是细胞保存遗传信息的长分子，细胞准备分裂时通常需要复制一套遗传信息。给新合成的部分留下可以检测的标记，就能从群体数量追踪到正在发生的分子过程。

EdU 是一种与胸苷结构相近的核苷类似物。可以把核苷理解为细胞制造 DNA 所需原料的一种组成形式；EdU 进入细胞后经过代谢转化，能够参与新 DNA 的合成。它带有一个可供后续化学反应识别的小基团，检测时再连接荧光分子。这个设计把“生物过程发生时留下标记”和“后来把标记显示出来”分成两个阶段，使研究者能够规定时间窗口，再观察哪些细胞核保存了这段时间里的合成记录。

这个时间窗口通常称为脉冲。持续半小时、两小时和一天的标记，对应的是不同问题：短时间观察更接近当时正在合成 DNA 的群体，较长时间则会纳入后来进入合成阶段的细胞。阳性比例因此必须与脉冲起止时间一起阅读。若两种材料使用了不同的标记时长，结果差别就同时包含了时间窗口的变化；即使标记时长相同，也需要结合细胞周期和起始状态来解释。

EdU 与活死染色可以形成有用的接续。绿色、膜完整的群体中，有些细胞正在合成 DNA，有些暂时没有；EdU 阴性并不等于死亡，EdU 阳性也不是已经完成一次分裂的证明。检测新 DNA 合成、观察分裂事件和统计最终细胞数，分别位于同一过程的不同位置。先明确自己想观察哪个位置，才能选择合适的标记窗口和后续读数，并把材料对细胞的影响说得具体。

## 一个很小的化学标签，连接了细胞生物学与点击反应

在 EdU 成为常用工具以前，研究者已经通过带标记的胸苷和 BrdU 等类似物研究 DNA 合成。BrdU 掺入后可以被相应抗体识别，但埋在双链 DNA 中的结构需要变得可接近，常见检测方法因此包含处理 DNA 结构的步骤。问题很自然：是否可以先放入一个更小的化学标签，后来再用小分子把它找出来，从而减少检测对结构的影响？这个问题把 DNA 复制实验与选择性连接分子的化学方法接到了一起。

2008 年，Salic 与 Mitchison 报道了使用 EdU 并通过荧光叠氮化物检测 DNA 合成的方法。EdU 上的末端炔基与叠氮基团在一价铜参与下形成稳定连接，这类反应属于点击化学。炔基可以先理解成分子上的一个小接头，荧光探针带着与它匹配的另一端；细胞先把带接头的原料放进 DNA，检测时再把发光部分接上。比喻中的接头对应真实的化学基团，反应仍依赖合适试剂、环境和可接近性。

![EdU 掺入与后续荧光点击检测是两个阶段。下方为构造周期的 G1、S、G2、M 区段，短脉冲能否标记取决于与 S 期的重叠；2008 年原研究提供这一方法的历史入口。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7988f32b1e97b11336e86df1.svg?v=7988f32b1e97)

图 1EdU 掺入与后续荧光点击检测是两个阶段。下方为构造周期的 G1、S、G2、M 区段，短脉冲能否标记取决于与 S 期的重叠；2008 年原研究提供这一方法的历史入口。

原研究用没有加入 EdU 的细胞和 DNA 合成受抑制的细胞进行比较，观察到相应的标记差异。这些对照把核内荧光与 EdU 掺入联系起来，而不只是展示一张明亮的细胞图。研究还展示了细胞与组织中的应用，以及脉冲之后一段时间再观察标记位置的思路。对今天的实验设计来说，历史中的关键仍然适用：小分子标签提供检测能力，合适的阴性和过程对照则确定这项能力在当前样本里具体读出了什么。

常见成像流程先在活细胞培养阶段加入 EdU，再固定、通透并完成点击检测。固定帮助保存结构，通透让检测试剂接近目标；荧光通常在后面的化学反应中出现。这样，“活细胞阶段的生物掺入”与“固定样本中的荧光显色”就有明确先后。原始方法也探索过其他样本条件，后来的试剂体系又改善了与某些荧光蛋白的兼容性。使用具体组合时，应按照其反应条件安排顺序，尤其关注既有荧光标记在含铜反应后的保留。

## 理解细胞周期，才知道一个阳性核代表哪段经历

把常见分裂周期看成一圈连续过程，会比把几个字母背下来容易。G1 阶段细胞生长并准备复制，S 阶段合成 DNA，G2 阶段继续准备，M 阶段完成有丝分裂和相关分配过程。并非所有细胞都持续绕圈，有些会退出活跃分裂状态，也有些在某一阶段停留较久。EdU 在常见增殖实验中主要标记脉冲期间进行 DNA 复制的细胞，因此它与 S 阶段密切相关，却保留的是一段经历，而不是拍照瞬间的阶段标签。

例如一个细胞在脉冲开始时正处于 S 阶段，结束时已经进入 G2，它仍然可以保留 EdU 标记。另一个细胞开始时还在 G1，但在两小时脉冲内进入 S，也会获得标记。若只按照拍照时的 DNA 总量或当前形态寻找 S 阶段细胞，这两种经历可能被不同地解释。将 EdU 信号与独立的 DNA 含量、时间记录结合，能看见“什么时候合成过”和“现在大约处在哪里”之间的关系。

为了理解脉冲长短，可以先看一个明确简化的相位模型：周期为二十四小时，S 阶段占八小时；追踪单位的起始相位均匀分布，其中四分之三参与周期，其余不进入 S。极短但可检出的标记窗口对应参与周期部分的八小时区段；增加两小时脉冲，就把将要进入 S 的另一段起始相位也纳入，覆盖长度变为十小时。因此总体理想覆盖比例是四分之三乘十除以二十四，即百分之三十一点二五。

$$
f_{\mathrm{cover}}=g\,\min\!\left(1,\frac{T_S+T_P}{T_C}\right),\qquad T_P>0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/12bf2f205cc2df4a17703941.svg) | 固定追踪单位中脉冲与 S 期发生任意重叠的理想比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | 参与该周期的追踪单位比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/79bf081bc99237d993a45dda.svg) | S 阶段时长，h。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0e53f812f5b4ea65a73be379.svg) | 正的标记脉冲时长，h；零脉冲没有实际掺入。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c671358096b31204cca6d4e0.svg) | 完整周期时长，h，且 0<T_S≤T_C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a05d6e83f4c2e8f52c235d7.svg) | 取两者较小值，使参与周期部分的覆盖率最多为 1。 |

假定起始相位均匀、阶段时长固定、分母不因分裂更新，并把任意短暂重叠视为可标记。g=0.75、T_S=8 h、T_C=24 h、T_P=2 h，得到 0.3125；脉冲 8 h 时为 0.50，16 h 时达到 0.75。实际检出还受信号阈值影响。

用一条传送带来想象这个模型会更直观。不同追踪单位最初站在传送带的不同位置，只有经过绿色区段时才会留下标签。短暂开放标记时，只来得及记录附近的一部分；开放更久，后面到达的单位也被纳入。这个图景解释了为什么累计标记比例可以增加，却不要求传送带转得更快。真实细胞群还存在进入、离开与分裂，模型把这些暂时固定，目的是先看清窗口本身的作用。

这里固定的是所追踪的单位，计算的是相位区间是否与 S 阶段相交，没有把脉冲期间分裂产生的新细胞重新加入分母。真实扩增群体的年龄分布、周期长短和分裂后的核数会更复杂，长脉冲还会增加这些过程的影响。这个模型的用途是看清时间窗口的几何关系：即使单个细胞的周期没有加快，延长脉冲也会提高阳性比例。若要从数据进一步估计周期长度，应采用与实际生长、取样和分母相符的模型，并增加相应时间点。

还有一些情形会改变“新 DNA 合成”与“群体增殖”的关系。细胞修复 DNA 时也可能发生局部合成，某些细胞会复制 DNA 却没有完成通常的细胞分裂，多核或不同倍性的细胞又使一个细胞核不一定等于一个细胞。研究对象处于这些情形时，应结合 DNA 含量、形态、分裂观察或相应过程标记解释 EdU。把所测对象说成“EdU 阳性核”，往往比直接称为“新增细胞”更准确，也为后面的比较保留了清楚的逻辑。

## 脉冲、浓度和对照，应围绕同一个问题安排

设计材料比较时，可以先规定希望观察的阶段。例如接种后早期更关心附着与恢复，较晚时间再观察 DNA 合成，便能减少把附着延迟直接解释成复制变化的混淆。各组需要有可比较的起始数量、培养历史和密度，并记录材料面积与实际保留群体。检测时间点决定观察哪段培养经历，脉冲长度决定在那个时间点附近整合多久，两者应分别写清楚。只写“培养一天后做 EdU”还不足以说明标记覆盖的具体时间。

配液计算可以从数量守恒开始。若用十毫摩尔每升的储液配制五毫升、二十微摩尔每升的工作液，需要十微升储液，再补足到五毫升。将这份两倍浓度工作液与等体积原培养液混合，最终浓度为十微摩尔每升。这个例子解释稀释关系，实际浓度和时间应依据所用细胞及检测条件选择。将工作液浓度误当最终浓度，或把毫摩尔与微摩尔混用，都会让同一个名义方案变成不同暴露。

$$
C_sV_s=C_wV_w,\qquad C_f=\frac{C_wV_w+C_mV_m}{V_w+V_m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | 储液浓度，μmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | 从储液转移的体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | 配制的工作液浓度，μmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec72cf11e28fd771d0f29c76.svg) | 工作液体积，mL；第二式中指参与混合的体积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b4840a9faca02419281df787.svg) | 原培养液中 EdU 浓度，μmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d26d844b3e76efe75c6582e5.svg) | 参与混合的原培养液体积，mL。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c47656593144cdd6182f400.svg) | 混合后的最终浓度，μmol/L。 |

10 mmol/L=10000 μmol/L。配 5 mL、20 μmol/L 工作液需 V_s=20×5/10000=0.010 mL，即 10 μL。与等体积无 EdU 培养液混合，最终为 10 μmol/L。假定配液时无明显反应或吸附损失。

检查单位可以帮助判断配液是否合理。浓度乘体积给出物质的量，单纯加入溶剂时，这个量保持不变；两边统一使用毫升或微升，都可以得到同一结果。两倍工作液适合与原培养液等体积混合，但记录时应将它的浓度与细胞实际经历的最终浓度分开。这样后续复算能够直接对应到实验中的每一次转移。

脉冲结束同样需要一个明确时间定义。若先给第一组换液，半小时以后才轮到最后一组，实际脉冲就可能随操作顺序改变；对于较短标记，这种差别尤其明显。可以按小批次安排相同起止间隔，将不同组交错处理，并记录开始、结束和固定的时间。观察较大支架时，还要考虑外部换液与内部标记物清除之间的差别，让名义上的脉冲尽可能对应细胞实际经历的窗口。

没有加入 EdU、但经历同样固定和检测步骤的样本，可以给出非特异背景。已知具有复制活动的样本帮助确认掺入与检测链条能够工作；与研究问题相符的过程对照，则帮助判断信号变化是否来自 DNA 合成。材料本身的背景、荧光探针吸附、试剂进入深度和样本在处理中的保留，也需要通过适当对照观察。固定通透后细胞脱落较多时，即使剩余核的图像很好看，最终分母也已发生变化。

提高浓度或延长脉冲常常会让信号更容易看见，但 EdU 同时参与了细胞内的代谢与 DNA 过程。Ligasová 等对不同细胞的研究显示，掺入效率和后续细胞响应与细胞身份、浓度和暴露安排有关。一个实用做法是在代表性条件下比较几个标记窗口，同时检查信号分离、形态和后续数量变化，选择能够清楚回答当前问题的条件。需要长时间追踪时，更要把标记过程本身纳入实验条件，并保留未标记对照。

双脉冲实验进一步利用了时间结构。例如先用一种可区分的标记记录前一段合成，再在稍后窗口用另一种标记记录后续合成，可以比较持续、退出或新进入复制状态的群体。两种标记的检测相容性、交叉识别和顺序需要单独验证，不能只因为颜色不同就认为互不影响。刚开始学习时，先把一个脉冲、一个清楚的总核分母和一个固定观察时间做好，便已经能回答许多材料与细胞反应的问题。

## 先找到全部细胞核，再问哪些核带有新合成标记

EdU 图像的一个关键设计，是用独立的核染色建立全部对象。若只从 EdU 通道寻找细胞核，阴性核很容易消失在检测流程里，阳性比例就会被推高。可以先在总核通道定位核区域，再把同一组区域放到 EdU 通道中测量信号。核接触时要检查是否被连成一个对象，碎裂时要检查是否被重复计数，跨越图像边缘的对象则按预先确定的规则处理。对象分割应与原图叠加检查，而不是只看软件输出了多少行数字。

![构造的 480 核图像：独立总核通道建立分母，EdU 通道提供脉冲记录，逐核信号与 DNA 信号共同展示。像素尺寸 1 μm；已知中心区域用于强度提取，不是全核体积估计。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d27826dd6f0133bae227b6c9.svg?v=d27826dd6f01)

图 2构造的 480 核图像：独立总核通道建立分母，EdU 通道提供脉冲记录，逐核信号与 DNA 信号共同展示。像素尺寸 1 μm；已知中心区域用于强度提取，不是全核体积估计。

背景、曝光和阈值的处理与一般荧光图像相通，但这里有一个特殊的生物原因会产生弱信号：细胞可能只在脉冲的末端短暂进入 S 阶段，获得较少标记。另一些细胞在整个窗口内持续合成，信号就更强。若把阈值设得很高，得到的比例会更偏向充分标记的群体；若设得过低，又可能纳入背景。阴性对照和阈值敏感性分析共同帮助区分这两种情况，并说明所报告阳性比例对应何种检测条件。

构造示例共有四百八十个核，其中三百六十个参与理想周期。两小时脉冲与 S 阶段发生任意重叠的核有一百五十个，占百分之三十一点二五。程序让 EdU 信号与实际重叠时间成比例，再生成含背景和噪声的核图像，从已知区域提取像素均值。即使没有噪声，检测阈值也会排除一些仅短暂重叠的弱标记核；示例中按理想信号阈值检出一百四十二个。这个差别把“发生了掺入”与“在当前条件下被检出”具体地联系起来。

$$
\mathrm{LI}=\frac{N_{\mathrm{EdU+}}}{N_{\mathrm{nuclei}}},\qquad P_{\mathrm{EdU+}}=100\,\mathrm{LI}\%
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ce82b781069415402958ad88.svg) | 标记指数，即规定脉冲和阈值下的阳性核比例，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/45b530b2ed4744ea22fcc10d.svg) | 独立定位的核中超过 EdU 判定阈值的核数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7c6bf26a946440e4ff236342.svg) | 同一采样范围内纳入分析的全部核数，个。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c71d463a060ff611b7e505ed.svg) | EdU 阳性核百分比，%。 |

分母由独立总核通道建立。200 个核中 60 个阳性，LI=0.30，即 30%；另一组 100 个核中 40 个阳性，比例 40%，但阳性核数为 40。示例的几何掺入数与图像检出数分别保留。

计算核内信号时，平均强度与总强度也有不同含义。一个核面积较大，在每像素亮度相同的情况下会有更高的总强度；若研究目标是比较单位区域的标记，平均强度更直接，若关注整个核内的累积信号，则需要保留面积与总量。示例用小的已知核中心区域测平均强度，目的是让阈值与时间重叠容易对应；这组区域并不用于估计完整细胞核体积。实际分析应按问题选择区域并保持定义一致。

报告结果时，可以同时给出总核数、阳性核数和阳性比例。条件甲有二百个总核，其中六十个阳性，比例为百分之三十；条件乙有一百个总核，其中四十个阳性，比例为百分之四十。乙的阳性比例较高，但阳性数量仍比甲少。若研究问题是材料支持的复制活跃群体规模，数量与面积密度提供了必要补充；若问题是现有群体中处于标记窗口内的比例，则需要保留相应分母。两种表达可以共同展示。

每个材料样本可以拍摄多个预先规定的视野，以观察空间差异；同一样本内的视野共享培养和处理条件，汇总时应保留样本层次。三维支架还要记录观察深度、试剂可达性与核是否在相邻切片中重复出现。最大强度投影可以帮助展示标记分布，三维对象计数则需要相应的空间连接规则。把同一孔的许多核当成许多独立培养实验，会高估实验重复提供的信息。

## 改变时间窗口，再看一张真正的实验图

交互实验将周期、S 阶段和脉冲放在同一条时间关系中。参与周期比例保持不变时，延长脉冲会覆盖更多起始相位；延长 S 阶段，也会使更多单位在给定窗口内获得标记。两种变化都可以提高阳性比例，但对应的生物过程不同。因此，单个阳性比例一般不能同时确定参与周期比例、S 阶段长度和整个周期长度。通过时间系列、独立总量或其他周期信息，才能逐步将这些因素分开。

## 只把脉冲延长，阳性比例会怎样变化？

固定周期为 24 h，S 期从相位 8 h 开始。绿色条表示 S 阶段，橙色条表示可能与它重叠的起始相位。调整脉冲、S 期与参与周期比例，观察同一个比例为什么可能来自不同条件。

[Figure: 脉冲与 S 阶段的相位覆盖及比例曲线](https://ml-biomat.com/tutorials/experimental-methods/l04/#L04-lab)

![A 为均匀相位、固定分母模型；B 比较任意掺入和阈值检出；C 为理想追踪稀释；D 用相同图同时保留总数、阳性数和比例。所有数据为构造例子。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f983d783a263102ef80df290.svg?v=f983d783a263)

图 3A 为均匀相位、固定分母模型；B 比较任意掺入和阈值检出；C 为理想追踪稀释；D 用相同图同时保留总数、阳性数和比例。所有数据为构造例子。

脉冲结束后换成不含 EdU 的培养条件，再在不同时间观察，称为追踪或追赶实验。最初标记过的 DNA 可以随细胞经历保留、分配和稀释。若理想情况下标记稳定、细胞对称分裂，且没有新的标记加入，每次分裂后每个后代细胞分得的平均标记量约为原来的一半。两次分裂后约为四分之一，四次后约为十六分之一。随着信号接近检测阈值，原先的标记群体可能逐渐难以识别，因此追踪结果应与信号分布一起阅读。

$$
\bar L_k=\frac{\bar L_0}{2^k},\qquad f_k=\frac{\bar L_k}{\bar L_0}=2^{-k}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7cb7ac0bb1fc44085ece8589.svg) | 经历 k 次理想对称分裂后，每个后代细胞的平均标记量，任意标记量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/45e8eecb99b23d5d75f6affe.svg) | 追踪开始时每个初始细胞的平均标记量，同上单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 分裂次数，无量纲非负整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e86f759b6e0ce297b6383e26.svg) | 每个后代细胞保留的平均标记比例，无量纲。 |

假设标记稳定、分配对称、无新增标记和其他损失，细胞数每次翻倍，平均标记分到两份。两次分裂为 25%，四次为 6.25%。此关系描述每个后代的平均量，不把每个核内的空间分配规定为完全相同。

追踪过程中也可以同时观察标记群体的位置。原先在材料外层合成过 DNA 的细胞，后来可能迁移到内部；同一个位置的阳性比例变化就同时包含数量、迁移和信号稀释。若需要区分这些过程，可以增加空间配准、重复成像或明确的分区统计，并将时间点上的总核数一起保留。这样追踪曲线与空间图会互相解释，而不会把所有标记减少都归到一个原因上。

真实实验图可以帮助我们理解另一个层次：相同外液浓度不一定给不同细胞带来相同的掺入信号。Ligasová 等在 2015 年的图 2 中比较了不同细胞的 EdU 浓度响应，并研究了胸苷共存时的变化。A 面板使用八小时标记，以各条件中标记最强的百分之五细胞核的平均信号描述掺入，并相对较高浓度的结果归一化；B 面板使用两小时标记，采用标记最强的百分之三十核进行比较。这里的纵轴是经过定义的信号比例，不是全体细胞的阳性率。

![Ligasová 等（2015）图 2，CC BY 4.0，完整转载。A：8 h 标记，最强 5% 核平均信号相对 50 μM 结果；B：2 h 标记，最强 30% 核的共加胸苷/单加 EdU 信号比。误差线为 SEM，均有三次重复。这里的百分比是信号归一化结果。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/946238abe8a645d10285ed02.svg?v=946238abe8a6)

图 4Ligasová 等（2015）图 2，CC BY 4.0，完整转载。A：8 h 标记，最强 5% 核平均信号相对 50 μM 结果；B：2 h 标记，最强 30% 核的共加胸苷/单加 EdU 信号比。误差线为 SEM，均有三次重复。这里的百分比是信号归一化结果。

读图时先看横轴浓度，再比较各细胞曲线出现明显信号的范围。曲线的差别说明原料运输、代谢转化与掺入效率会参与最终读数。B 面板进一步展示，加入另一种相关底物后，EdU 的信号响应也会变化。图中的误差线是均值的标准误，描述重复实验均值估计的波动；它与用标准差表示单次结果分散程度的含义不同。这样的真实例子提醒我们把浓度、时间、对象选择与归一化基准同时读入图中。

这一观察也能转回材料研究。如果材料改变了细胞密度、营养可用性或局部环境，EdU 信号可能同时反映复制过程和标记的进入与利用。设计对照时，可以检查细胞是否在可比较条件下暴露于标记、成像区域是否代表样本、标记后的细胞数量是否保留。这样安排之后，EdU 便能作为一条有明确时间含义的证据，与材料上的附着、群体增长和功能观察相互连接。

## 从逐核记录，回到材料改变了哪一段过程

完整程序保存总核与 EdU 原始图像、核区域标签、逐核信号及汇总。读者可以从某个核的位置出发，找到其脉冲与 S 阶段重叠时间，再查看构造的掺入强度、从像素提取的强度和最后判定。代码另外画出脉冲覆盖、阈值敏感性、追踪稀释与数量分母比较。图像中的位置和信号来自明确的教学构造，真实研究图则单独注明实验条件，让模型与观测各自承担解释作用。

### 从脉冲重叠生成核图像，再计算检出结果

完整示例导出两个原始图像数组、核区域、逐核 CSV、四幅图及汇总。固定种子构造数据；公开实验图和许可随包提供。

```
"""EdU pulse coverage, nuclear image measurements and labeling decisions."""
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


def pulse_overlap(phase,duration,s_start=8.,s_end=16.,cycle=24.):
    phase=np.asarray(phase);overlap=np.zeros_like(phase,dtype=float)
    for k in range(int(np.ceil(duration/cycle))+2):overlap+=np.maximum(0,np.minimum(phase+duration,s_end+k*cycle)-np.maximum(phase,s_start+k*cycle))
    return overlap

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(404);n=480;cycling=360;phase=(np.arange(cycling)+.5)*24/cycling;overlap=np.r_[pulse_overlap(phase,2),np.zeros(n-cycling)];true_signal=60*overlap;ideal_labeled=overlap>0;ideal_detected=true_signal>=15
    final_phase=np.r_[(phase+2)%24,np.zeros(n-cycling)];dna=np.where(final_phase<8,2,np.where(final_phase<16,2+(final_phase-8)/4,4));order=rng.permutation(n);true_signal=true_signal[order];dna=dna[order];overlap=overlap[order];ideal_labeled=ideal_labeled[order];ideal_detected=ideal_detected[order]
    positions=np.array([(15+24*x,15+24*y) for y in range(20) for x in range(24)],float)+rng.uniform(-2,2,(n,2));yy,xx=np.mgrid[:490,:590];nuclei=np.full(xx.shape,20.);edu=np.full(xx.shape,20.);labels=np.zeros(xx.shape,int)
    for i,((x,y),signal,d) in enumerate(zip(positions,true_signal,dna)):
        kern=np.exp(-((xx-x)**2+(yy-y)**2)/(2*3.4**2));nuclei+=d*35*kern;edu+=signal*kern;labels[(xx-x)**2+(yy-y)**2<2**2]=i+1
    nuclei+=rng.normal(0,1,nuclei.shape);edu+=rng.normal(0,1,edu.shape);measured=np.array([edu[labels==i+1].mean()-20 for i in range(n)]);measured_dna=np.array([nuclei[labels==i+1].mean()-20 for i in range(n)])/35
    detected=measured>=15;np.savetxt(output/'nuclei.csv',np.column_stack([np.arange(1,n+1),overlap,dna,true_signal,measured,detected.astype(int)]),delimiter=',',header='nucleus,overlap_h,relative_DNA_content,true_EdU_au,measured_EdU_au,positive',comments='');np.savez_compressed(output/'nuclear_images.npz',nuclei_raw=nuclei,edu_raw=edu,roi_labels=labels,pixel_um=1.)
    fig,ax=plt.subplots(2,1,figsize=(10.8,7.4));a=ax[0];a.axis('off');a.set(xlim=(0,10),ylim=(0,3));a.text(.4,2.65,tr('活细胞：掺入小标签','Live cells: incorporate a small tag'),fontsize=12);a.text(5.6,2.65,tr('检测阶段：连接荧光标记','Detection: attach a fluorescent reporter'),fontsize=12)
    for left in [.6,5.9]:
        a.plot([left,left+3],[1.15,1.15],color='#186e83',lw=3);a.plot([left,left+3],[1.75,1.75],color='#186e83',lw=3)
        for x in np.linspace(left+.2,left+2.8,7):a.plot([x,x],[1.15,1.75],color='#91bac7',lw=2);a.scatter([x,x],[1.15,1.75],color='#186e83',s=32)
        a.scatter([left+1.5],[1.75],color='#cd803f',s=80,zorder=5)
    a.plot([2.1,2.1],[1.75,2.15],color='#cd803f',lw=2);a.text(2.1,2.28,'EdU',color='#aa6529',ha='center',fontsize=10);a.add_patch(FancyArrowPatch((3.9,1.45),(5.4,1.45),arrowstyle='->',mutation_scale=22));a.text(4.65,1.95,'Cu(I)',ha='center',fontsize=10);a.plot([7.4,7.4,8.05],[1.75,2.1,2.1],color='#8160a1',lw=2);a.scatter([8.05],[2.1],marker='*',s=230,color='#8160a1');a.text(5,.35,tr('DNA 梯形为核苷位置示意；星号为后来连接的荧光探针。','DNA ladder depicts nucleotide positions; the star marks the reporter attached later.'),ha='center',fontsize=10);a.text(5,.05,tr('2008 年 Salic 与 Mitchison：将 DNA 掺入与小分子点击检测相连接。','Salic and Mitchison, 2008: connect DNA incorporation with small-molecule click detection.'),ha='center',fontsize=10)
    a=ax[1];stages=[(0,8,'G1'),(8,8,'S'),(16,6,'G2'),(22,2,'M')];colors=['#b9d8e2','#3c8a6a','#d8c7e5','#d6aa81']
    for (start,width,name),c in zip(stages,colors):a.barh(1.25,width,left=start,height=.3,color=c);a.text(start+width/2,1.25,name,ha='center',va='center')
    for y,start,over in [(.8,6,0),(.5,9,2),(.2,15,1)]:
        a.barh(y,2,left=start,height=.15,color='#e2c5a9')
        if over:a.barh(y,over,left=max(start,8),height=.15,color='#3c8a6a')
        a.text(start+2.4,y,tr(f'2 h 脉冲；重叠 {over} h',f'2 h pulse; overlap {over} h'),fontsize=10,va='center')
    a.set(xlim=(0,24),ylim=(0,1.65),yticks=[],xlabel=tr('构造周期中的位置 / h','Position in a constructed cycle / h'));fig.tight_layout();save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8));a=ax[0,0];a.imshow(nuclei,cmap='Blues_r',origin='lower',vmin=20,vmax=160,extent=[0,590,0,490]);a.set_title(tr('A  全部核：独立建立分母','A  All nuclei establish the denominator'));a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[0,1];a.imshow(edu,cmap='magma',origin='lower',vmin=20,vmax=145,extent=[0,590,0,490]);a.set_title(tr('B  EdU：记录脉冲内的掺入','B  EdU records incorporation during the pulse'));a.plot([430,530],[35,35],color='white',lw=3);a.text(480,50,'100 μm',color='white',ha='center',fontsize=9);a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,0];a.scatter(measured_dna,measured,c=np.where(detected,'#8160a1','#8aa0a8'),s=12,alpha=.65);a.axhline(15,color='#cd803f',ls='--');a.set(xlabel=tr('相对 DNA 信号','Relative DNA signal'),ylabel=tr('核内 EdU 均值 / a.u.','Mean nuclear EdU / a.u.'),title=tr('C  脉冲末端的 DNA 与 EdU','C  DNA and EdU at the end of the pulse'))
    a=ax[1,1];a.hist(measured,bins=40,color='#186e83');a.axvline(15,color='#cd803f',ls='--');a.set(xlabel=tr('扣背景核内 EdU / a.u.','Background-corrected nuclear EdU / a.u.'),ylabel=tr('核数','Nuclei'),title=tr('D  阈值与短暂进入 S 期的弱信号','D  Threshold and weak signal from brief S-phase overlap'));fig.suptitle(tr('固定相位群体的构造图像；每个核定位区域已知','Constructed fixed-cohort images; nuclear measurement regions are known'),fontsize=11);fig.tight_layout();save(fig,'nuclei')
    fig,ax=plt.subplots(2,2,figsize=(11.2,7.5));duration=np.linspace(.05,20,200)
    for fraction in [.5,.75,1.]:ax[0,0].plot(duration,100*fraction*np.minimum(1,(8+duration)/24),label=f'g={fraction}')
    ax[0,0].set(xlabel=tr('脉冲长度 / h','Pulse duration / h'),ylabel=tr('几何覆盖比例 / %','Geometric coverage / %'),title=tr('A  固定追踪单位的相位覆盖模型','A  Phase coverage of fixed tracking units'));ax[0,0].legend(fontsize=9)
    qs=np.linspace(1,125,125);ax[0,1].plot(qs,[100*np.mean(measured>=q) for q in qs]);ax[0,1].axhline(31.25,ls=':',color='#8160a1',label=tr('有任意掺入的比例','Any-incorporation fraction'));ax[0,1].axvline(15,ls='--',color='#cd803f');ax[0,1].set(xlabel=tr('判定阈值 / a.u.','Decision threshold / a.u.'),ylabel=tr('检出阳性比例 / %','Detected positive fraction / %'),title=tr('B  掺入与检出之间的差别','B  Incorporation versus detection'));ax[0,1].legend(fontsize=8)
    divisions=np.arange(5);ax[1,0].plot(divisions,100/2.**divisions,'o-');ax[1,0].set(xticks=divisions,xlabel=tr('理想对称分裂次数','Ideal symmetric divisions'),ylabel=tr('每个后代细胞的平均标记 / %','Mean label per descendant / %'),title=tr('C  脉冲后追踪中的标记稀释','C  Label dilution during a chase'))
    ax[1,1].bar([tr('条件甲','Condition A'),tr('条件乙','Condition B')],[200,100],label=tr('总核数','Total nuclei'),color='#b9d8e2');ax[1,1].bar([tr('条件甲','Condition A'),tr('条件乙','Condition B')],[60,40],label=tr('EdU 阳性核','EdU-positive nuclei'),color='#8160a1');ax[1,1].text(0,210,'30%',ha='center');ax[1,1].text(1,110,'40%',ha='center');ax[1,1].set(ylabel=tr('核数','Nuclei'),ylim=(0,270),title=tr('D  阳性比例与阳性数量同时阅读','D  Read positive fraction and count together'));ax[1,1].legend(fontsize=8);fig.tight_layout();save(fig,'pulse')
    fig,ax=plt.subplots(figsize=(8.2,12.5));ax.imshow(plt.imread(Path(__file__).with_name('ligasova2015-figure2.png')));ax.axis('off');ax.set_title(tr('真实实验：浓度、细胞身份与竞争底物改变掺入信号','Measured example: concentration and competing substrate affect labeling'),fontsize=11);fig.text(.5,.06,tr('Ligasová 等，2015，图 2，CC BY 4.0；均值±SEM。\nA 为 8 h，B 为 2 h 标记；见正文的信号定义。','Ligasová et al., 2015, Fig. 2, CC BY 4.0; mean ± SEM.\nA uses 8 h; B uses 2 h; signal definitions in text.'),ha='center',fontsize=9);save(fig,'published')
    summary={'cohort':{'total':n,'cycling':cycling,'any_incorporation':int(ideal_labeled.sum()),'ideal_detected':int(ideal_detected.sum()),'observed_detected':int(detected.sum()),'any_percent':float(ideal_labeled.mean()*100),'observed_percent':float(detected.mean()*100)},'geometry':{'two_hour_fraction':.75*(8+2)/24,'eight_hour_fraction':.75*(8+8)/24,'sixteen_hour_fraction':.75},'dilution':{'stock_10mM_to_5ml_20uM_ul':10.,'final_after_equal_mix_uM':10.},'chase':{'two_division_fraction':.25,'four_division_fraction':.0625},'comparison':{'a_fraction':.3,'b_fraction':.4,'a_positive':60,'b_positive':40}}
    assert ideal_labeled.sum()==150 and ideal_detected.sum()==142 and abs(pulse_overlap(np.array([6.,7.,8.,15.,16.]),2)-np.array([0.,1.,2.,1.,0.])).max()<1e-10
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

可以先将脉冲由两小时改成四小时，观察几何覆盖与检出比例如何变化；再固定脉冲，只提高阈值，检查弱标记核怎样退出阳性集合。随后改变参与周期的比例，比较它与延长 S 阶段造成的曲线差异。每次修改时同时保留总核数和阳性数，可以避免只关注百分比。对实际数据，逐核表与原图叠加检查也帮助发现分割、脱落、背景和边缘处理引入的问题。

最后形成的解释应能够说清楚：在什么培养阶段、什么时间窗口内，有多少已观察核显示了新 DNA 合成标记，信号怎样判定，以及结果与总体细胞数量和空间分布如何对应。若材料组的阳性比例变化，可以进一步观察周期推进、群体增长或特定功能；若比例相近而总核数相差很大，则先检查起始保留与后续流失。EdU 把一个笼统的“细胞长得怎样”，拆成了能够按时间和对象继续研究的问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Salic and Mitchison (2008): A chemical method for fast and sensitive detection of DNA synthesis in vivo](https://salic.med.harvard.edu/sites/salic.med.harvard.edu/files/publications/Salic_2008_Proc%20Natl%20Acad%20Sci%20U%20S%20A.pdf)

   EdU 掺入与点击检测的原始方法、对照和追踪实例。
2. [Thermo Fisher: Click-iT EdU Imaging Cell Proliferation Protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/click-it-edu-imaging-protocol.html)

   标记、固定通透、检测和额外染色的先后关系。
3. [Thermo Fisher: Click-iT Plus EdU Cell Proliferation Imaging Kits Protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/click-it-plus-edu-imaging-protocol.html)

   含铜检测条件与荧光蛋白兼容性的具体体系。
4. [Ligasová et al. (2015): A Fatal Combination: A Thymidylate Synthase Inhibitor with DNA Damaging Activity](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0117459)

   不同细胞的掺入响应、底物竞争和标记条件；完整转载图 2。

   CC BY 4.0; Figure 2 reproduced intact with attribution and outer teaching title.
5. [ImageJ: Principles of Scientific Imaging](https://imagej.net/imaging/principles)

   原始数值、分割检查和阈值方法。
