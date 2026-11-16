# 让蛋白质序列与结构相互对应

Source: https://ml-biomat.com/tutorials/python-scientific/s05/
Language: zh-CN

以真实晶体结构的内部缺口为线索，建立从序列位置到坐标、距离和结构比较的完整对应。

## 序列里的第 64 个氨基酸，为什么在结构里找不到

一条蛋白质序列有 89 个字母，读入它的结构后却只找到 87 个代表主链位置的碳原子，这并不罕见。若把序列字母与坐标列表按行拼接，前面看起来一切正常，到了内部缺口之后，后面的字母就会整体错位。这样的错误会进一步影响突变标注、距离计算和接触图：计算本身可以顺利运行，标注却已经指向了另一个残基。本节用 Biopython 处理一个真实的公开晶体结构，建立从完整沉积序列到已观察坐标的对应表，再沿同一张表绘制结构、查看缺口、计算距离，并比较同一种蛋白质的不同晶体学拷贝。

所用结构是 PDB 1BRS，Buckle、Schreiber 和 Fersht 于 1994 年研究的 barnase–barstar 复合物，X 射线衍射数据分辨率为 2.00 Å。Barnase 是一种切割 RNA 的酶，barstar 通过与它结合来抑制其作用；原研究使用的 barstar 带有 C40A、C82A 替换。本节始终使用该条目沉积的序列。文件中 A、B、C 是 barnase 的三个晶体学拷贝，D、E、F 是 barstar 的三个拷贝。它们使一个常被忽略的问题变得很具体：同一种沉积序列，在不同拷贝中可以有不同的坐标覆盖范围。

这里的学习目标从数据对应关系出发。读完后，你应能够从一条序列位置追到结构中的原子，并在没有坐标时保留这个位置；能够解释图上的断线、距离矩阵中的空白行，以及某个接触计数采用了哪些条件。Biopython 提供读取、组织和比较生物数据的对象，NumPy 负责坐标运算，Matplotlib 负责把对应关系画出来。把这几个环节连在一起，比单独记住某个文件读取函数更便于处理自己的蛋白质数据。

还需要区分结构文件中的链数与一个生物复合物的组成。晶体的不对称单元可以包含多个分子拷贝，它们用于描述晶体里的一组独立坐标；生物学组装体则回答这些分子怎样组成具有功能的复合物。不能看到文件里有六条蛋白链，就自动把研究对象称为六聚体。本节分别分析六条链内部的序列和 Cα，保留它们各自的标识。研究 barnase 与 barstar 的结合界面时，再选择相应组装体和跨链配对，会得到另一套明确的数据对象。

## 字母、残基与 Cα：先确定每个对象是什么

蛋白质可以从一串连接起来的氨基酸理解。氨基酸连入链以后，留下的组成单元称为残基；序列中的一个字母通常表示一个残基类型，而不是一个原子。例如 A 表示丙氨酸，G 表示甘氨酸，E 表示谷氨酸，N 表示天冬酰胺。每个残基又包含多个原子。Cα 是主链上的中心碳，连接氨基侧、羰基侧和侧链环境；用每个残基的一个 Cα 描绘整条链，可以把数百个原子的模型压缩成容易阅读的骨架。原子名 `CA` 在这个蛋白质语境中表示 Cα，不能单看两个字母就把它理解为钙元素。

完整的沉积聚合物序列和坐标文件里出现的残基，承担不同的信息任务。前者说明实验所研究的链按什么顺序组成，后者列出该结构模型中建立了哪些原子位置。晶体衍射提供的是许多分子共同形成的散射信息，研究者根据电子密度和化学约束建立模型。有些区域的密度不够清楚，可能没有建入相应坐标；同一序列中的这些位置仍然保留。就像有完整的街道地址簿，却只有部分门牌的现场照片，缺照片不等于地址从名册中消失。这里把两类信息分别读取，再用明确的位置编号连接。

Biopython 的 `Seq` 保存序列，`SeqRecord` 在序列外再加上编号、描述和注释。FASTA 文件则是一种简洁的文字形式：以 `>` 开头的一行给出记录标识和描述，后面的字母组成序列，换行只是排版，不会新建另一条链。程序生成六条记录，编号为 `1BRS_A` 到 `1BRS_F`，并用 `SeqIO.write()` 写出、`SeqIO.parse()` 读回。编号保留链的身份，字母保留沉积的完整顺序，因此 D 链的 FASTA 仍长 89，而不是被坐标覆盖范围缩成 87。

![1BRS 六条链的 Cα 坐标覆盖，以及 barstar 内部 64 E、65 N 的放大对照。灰色部分超出该链完整序列，不属于缺坐标位置。](https://ml-biomat.com/static/tutorials/python-scientific/figures/b5b84dbfb9e329013ccac8da.svg?v=b5b84dbfb9e3)

图 11BRS 六条链的 Cα 坐标覆盖，以及 barstar 内部 64 E、65 N 的放大对照。灰色部分超出该链完整序列，不属于缺坐标位置。

上图先按完整序列位置排开六条链。A、C 缺少第 1、2 位的 Cα 坐标；D 缺少第 64、65 位；E 还额外缺少第 1 位；B 和 F 的 Cα 覆盖完整。放大 D、E、F 的内部片段，可以看到第 64 位 E 和第 65 位 N 仍保留字母，但 D、E 的相应格子用橙色表示无坐标。覆盖率可以把这种情况压缩成一个数，不过缺口位置也需要保留：末端缺两个残基，与中间缺两个残基，对后续连接和标注的影响不同。

$$
f_{\mathrm{CA}}=\frac{N_{\mathrm{CA}}}{L}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a49fa40efbf0c96a3ae9ae8f.svg) | 所选链的 Cα 坐标覆盖率，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/d11a0dfd93acda6605806f9c.svg) | 具有所选 Cα 坐标的不同序列位置数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 完整沉积聚合物序列的长度，残基数，无量纲整数 |

D 链完整序列长 89，具有 Cα 坐标的位置有 87，所以覆盖率为 87/89≈0.977528，即 97.75%。分子数与原子总数不进入这里的分母；每个序列位置最多计算一个选定 Cα。

## 连接两张表，用位置标识而不是列表行号

本节使用 PDBx/mmCIF 文件。它把不同类别的信息组织成带名称的字段，`_entity_poly.pdbx_seq_one_letter_code_can` 给出聚合物序列，`_struct_asym` 把各链实例对应到聚合物实体，`_atom_site` 则包含原子坐标和身份字段。实体可以理解为“这种分子是什么”，链实例则表示文件里的“哪一个拷贝”：A、B、C 共享一个 barnase 实体，D、E、F 共享一个 barstar 实体。先建立实体到序列、链到实体的两个字典，就能为每条链取得正确的完整序列。

原子表中的 `label_seq_id` 指向该聚合物实体的序列位置，`label_asym_id` 指明链实例，因此二者组合起来，能够找到这份条目中的一个聚合物位置。文件还保留 `auth_seq_id` 与 `auth_asym_id`，用于作者采用的编号体系；插入码也有独立字段。作者编号可以延续完整蛋白的编号，带有缺口或插入位置，未必从 1 开始，也未必等于标准序列位置。本例多数已观察位置的两套数字一致，但代码仍把它们分别保存，以便同一种方法处理编号更复杂的结构。

D 链提供了一个直接的反例。它在序列位置 63 之后，下一条有 Cα 坐标的记录位于 66。若只把有坐标的残基压成列表，从 1 开始数，列表第 64 行已经是序列位置 66 的 G，而序列第 64 位应当是 E。把 Python 的第 63 个索引拿去读取这个压缩列表，会得到错误的氨基酸身份。程序的处理方式是先遍历完整序列的 1–89 位，再查找该位置是否存在坐标：有就写入三维位置和原子属性，没有就保留空值。这样的对应表仍有 89 行，后续数组中的空缺也出现在真正的 64、65 位。

`MMCIFParser` 另外把文件组织成“结构—模型—链—残基—原子”的层次。这里明确设置 `auth_chains=False` 和 `auth_residues=False`，使用标准链标识和序列位置访问聚合物残基。文件模型编号从 1 开始，解析后的第一个模型用 Python 索引 0 取得，这两种编号也需要区分。代码再从原始字段读取 Cα 的十进制坐标，与解析器对象中的坐标核对。两条读取路径分别帮助我们检查字段身份与结构层次；本例最大差约为 3.7×10⁻⁶ Å，来自解析器坐标的浮点精度差异。

原子序号、残基位置和模型编号也不要混为一列。一个残基包含多个原子，所以原子记录的流水号增长得远比序列位置快；一个文件又可能包含多个模型，各模型可以重复使用相同链与残基标识。用于访问某个原子的完整地址，应包含模型、链、残基位置和原子名，并在需要时加入插入码及替代位置。程序先固定第一个模型和聚合物链，再筛选名为 CA 的原子，避免把别的分子类型混入骨架。把每一层选择写清楚以后，同一条规则才能稳定地用于下一份文件。

## 把三维位置变成可检查的距离与接触

每个已观察的 Cα 有三个坐标 x、y、z，单位为 Å；1 Å 等于 0.1 nm。它们表示该原子在结构坐标系中的位置，整体平移或转动这套坐标不会改变内部距离。两个点的距离，是三个方向差值平方和的平方根，也就是三维空间里的勾股定理。平方使正负方向的位移都贡献正的长度量，再开平方把单位从 Å² 变回 Å。先用一对具体坐标手算，再推广到所有原子对，能够帮助检查数组广播的方向和结果单位。

$$
d_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 同一条链中两个序列位置的编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/6061515e1359986403f43ece.svg) | 位置 i 的 Cα 三维直角坐标，Å；位置 j 的同名量含义相同 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | 两个 Cα 的欧氏距离，Å |

D:63 的坐标为 (34.404,25.607,−7.294) Å，D:66 为 (32.590,30.124,−6.906) Å。三个差值为 1.814、−4.517、−0.388 Å，平方相加再开根号，得到 4.883076 Å。只有两端都有坐标时才计算该距离；缺坐标的位置保持空值。

D 链位置 62 与 63 的 Cα 距离约为 3.774 Å；位置 63 与 66 的距离约为 4.883 Å。后一对在压缩坐标列表中相邻，但序列中间隔着两个缺坐标位置。距离不算特别大，也不能因此把它们画成一段已观察到的连续主链。结构图保留完整位置数组，用空值使连线在缺口处断开。矩阵中，某个残基没有坐标时，与它有关的整行和整列距离都保持空缺；把这些空值填成 0，会把“尚无位置可算”错误地变成“所有原子与它重合”。

![D 链的固定方向正交投影、完整序列坐标下的距离矩阵，以及三个 barstar 拷贝的 Cα B 因子。缺坐标位置在各图中一致留空。](https://ml-biomat.com/static/tutorials/python-scientific/figures/a8e00ced58017846099f9008.svg?v=a8e00ced5801)

图 2D 链的固定方向正交投影、完整序列坐标下的距离矩阵，以及三个 barstar 拷贝的 Cα B 因子。缺坐标位置在各图中一致留空。

距离矩阵给出了所有已知位置之间的数值，还可以按一个明确规则生成接触图。本节把 Cα 间距离不超过 8 Å、且序列位置至少相差 4 的残基对称为接触。距离阈值是本次分析的几何定义，序列间隔条件则排除紧邻主链的局部连接，让折叠后相互靠近的链段更突出。矩阵关于对角线对称，统计时只取上三角，每对残基计算一次；满足相同规则的 D 链得到 177 对接触。改成其他阈值后，结果应随条件一起保存，读者才能复算对应计数。

$$
C=\sum_{1\leq i<j\leq L}\mathbf{1}\!\left[d_{ij}\leq r_c\ \mathrm{and}\ |i-j|\geq s\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 满足条件的不同残基对数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/47a94dd73f392576cd118ab0.svg) | 对链中每个不重复的有序编号对求和，i |
| ![Formula](https://ml-biomat.com/static/agent-math/c97f2f705aae6fe904ed2b60.svg) | L 为完整序列长度，i、j 为序列位置，均为无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/22ebe45a4378fbd0f4467250.svg) | 指示函数：两端坐标存在且括号条件满足时为 1，其余为 0 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | 位置 i 与 j 的 Cα 距离，Å |
| ![Formula](https://ml-biomat.com/static/agent-math/35f9cc01c0330718f02f18d2.svg) | 接触距离阈值，默认 8 Å |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 最小序列位置间隔，默认 4，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/bdbedbda53a69f23422a688c.svg) | 两个序列位置之差的绝对值，无量纲 |

D:63 与 D:66 相距 4.883 Å，满足 8 Å 的距离条件，但位置差为 3，小于默认间隔 4，因此这对不计入。对所有有坐标且 i

这类 Cα 接触描述的是粗略空间邻近。若研究氢键，需要进一步检查供体、受体、距离和方向；若研究两种蛋白的界面，应明确跨链原子选择，常常需要使用侧链重原子的最短距离。本节的图只统计单条链内部的 Cα 对。图中同时展示的 B 因子来自晶体模型的原子位移参数，单位为 Å²，与热运动、静态无序和精修模型有关。它可以帮助阅读同一结构中的局部差异，但不是逐残基的测量误差条，也不是一段分子动力学轨迹。灰色缺口与 B 因子曲线的断点共同提醒我们，数值始终附着于实际建立了坐标的原子。

投影图只是三维坐标的一种观察方式。把一串珠子放到桌上拍照，前后重叠的珠子可能看起来挨在一起，转动相机后又分开；照片里的距离因此会随视角变化。这里的 u、v 是旋转后坐标在屏幕平面上的两个分量，第三个分量只影响前后关系。真正的点间距离仍用原始三个坐标分量计算。接触矩阵和距离曲线为投影提供了数值参照：即使屏幕上的两个点重合，只要三维间距超过阈值，矩阵仍不会把它们标成接触。

## 同一条序列的不同拷贝，要先对齐再比较

蛋白质序列与三维结构在科学史上逐步成为两类可以相互连接的证据。Sanger 在 1958 年的诺贝尔演讲中回顾胰岛素研究，说明如何由片段推断氨基酸的排列顺序。知道一种蛋白含有哪些氨基酸，以及知道它们按什么顺序排列，已经是不同层次的信息。Kendrew 等人在 1960 年发表的肌红蛋白 2 Å 结构研究，则把蛋白质的空间排列带入原子模型。到 1971 年，PDB 以最初的 7 个结构建立公共档案，序列、身份字段和坐标逐渐成为可以共同保存、比较与复用的数据。

1BRS 的 D、E、F 链让这两类信息在一份现代文件里交汇。三条链的沉积序列相同，坐标覆盖和局部构象却不完全一致。它们位于晶体坐标系的不同位置，直接相减会把整体平移和旋转也算成构象变化。比较之前，需要先确定对应的残基，再寻找一个整体旋转和平移，让共同原子的平方偏差和尽可能小。Biopython 的 `Superimposer` 完成这个刚体对齐；“刚体”表示整条链一起转动，不在对齐过程中拉长某一段或改变内部距离。

![同一位置在序列表与坐标列表中的对应，以及 D/F 共同 87 个 Cα 对齐后的结构。图中的 64、65 位坐标属于 F 链。](https://ml-biomat.com/static/tutorials/python-scientific/figures/5d36299d5f49cbeb2544a2ed.svg?v=5d36299d5f49)

图 3同一位置在序列表与坐标列表中的对应，以及 D/F 共同 87 个 Cα 对齐后的结构。图中的 64、65 位坐标属于 F 链。

程序以 D 链为参考，选择 D、F 都有坐标的 87 个 Cα，按相同序列位置一一配对，再把 F 对齐到 D。图中绿色的 F 链在 64、65 位仍有坐标，蓝色的 D 链保持断开。F 链的这两个位置可以帮助理解缺口位于怎样的结构区域，但它们仍属于 F 这个拷贝；把它们写进 D 链会成为另一次结构建模操作，需要另行记录。对齐后的共同原子均方根偏差 RMSD 约为 0.244 Å，计算范围是这 87 个对应 Cα，不能把这个平均量理解为每个残基都相差同样距离。

$$
\mathrm{RMSD}=\sqrt{\frac{1}{N}\sum_{k=1}^{N}\left\|\mathbf{x}_k-\left(\mathbf{y}_k R+\mathbf{t}\right)\right\|^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b17228ca39adc15eff866b18.svg) | 刚体对齐后的均方根位置偏差，Å |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 参与对齐与比较的共同 Cα 数，本例为 87，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 所选对应原子对的索引，从 1 到 N，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/7f1258f7427282b1fcec9cc5.svg) | 参考链 D 中第 k 个选定 Cα 的坐标行向量，Å |
| ![Formula](https://ml-biomat.com/static/agent-math/7821703b8b24f2cff25e51f4.svg) | 待对齐链 F 中对应 Cα 的坐标行向量，Å |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 对 F 施加的 3×3 刚体旋转矩阵，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/37323ddd9fc7a290f4c2ada8.svg) | 旋转后施加的平移行向量，Å |
| ![Formula](https://ml-biomat.com/static/agent-math/a26a4df582a01989203b6838.svg) | 三维向量的欧氏长度；平方后单位为 Å² |
| ![Formula](https://ml-biomat.com/static/agent-math/610b8056963a095c3539df1f.svg) | 对所选的 N 对原子求和 |

Superimposer 选择使平方偏差和最小的 R 和 t。D/F 的 87 对共同 Cα 计算得到 RMSD=0.243970 Å，对应平均平方偏差约 0.0595214 Å²。为理解开方，可设两对原子的对齐后距离分别为 0.1 和 0.3 Å，则 RMSD=√[(0.01+0.09)/2]≈0.223607 Å。

RMSD 的解释依赖选择了哪些原子。若把柔性末端排除、改用整个骨架或加入侧链，结果就会变化；对齐前应同时保存选择条件和参考结构。本例的 2.00 Å 衍射分辨率描述数据能够分辨的整体空间细节尺度，0.244 Å 则描述两个已建立模型在指定原子集合上的相对偏差，它们并不是同一种误差量。D、E、F 也是同一个晶体条目里的拷贝，不应把三条曲线直接当作三次独立溶液实验。这样理解以后，结构比较得到的数值就与它实际回答的问题一致。

## 完整程序：让序列位置贯穿每一步计算

`read_chains()` 首先读取实体序列和链标识，再逐行寻找第一个模型中的聚合物 Cα。它保留标准位置、作者编号、插入码、替代位置标识、占有率、坐标和 B 因子。一个原子若有多个替代位置，程序按较高占有率选取；相同占有率时保留文件中先出现的记录。本例的 Cα 对应关系通过解析器坐标再次核对。遇到新的结构类型时，还需要检查修饰残基和多种替代构象的处理规则，因为一个一字母序列符号未必足以表达全部化学细节。

随后程序沿完整序列生成残基列表，而不是只沿已观察残基生成列表。坐标数组保持“序列长度 × 3”的形状，空位用 `NaN` 表达；计算所有两点差值时，广播得到“序列长度 × 序列长度 × 3”，沿最后一个坐标轴求长度，就得到距离矩阵。`contacts()` 同时应用距离与序列间隔条件，并只返回上三角索引。这里的数组索引从 0 开始，写回残基位置时加 1，确保图、表和原始字段采用相同的序列坐标。

### 完整序列映射、距离与刚体对齐程序

使用随例子提供的公开 mmCIF 文件，完整保留序列位置，并生成 FASTA、残基表、数值结果与科学图。

```
"""Connect deposited protein sequences to observed alpha-carbon coordinates.

Public input: PDB 1BRS (CC0), Buckle, Schreiber and Fersht (1994),
doi:10.1021/bi00196a004. Run: python main.py --output results --language en
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import seq1
from Bio.PDB import MMCIFParser, Superimposer
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

BLUE,ORANGE,GREEN,INK='#235b89','#bf5635','#177d72','#192b3a'
INPUT=Path(__file__).resolve().parent/'data'/'1BRS.cif'


def available_plot_fonts():
    choices=['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans']
    installed={font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]


def read_chains(path):
    data=MMCIF2Dict(str(path))
    sequence={entity:''.join(text.split()) for entity,text in zip(
        data['_entity_poly.entity_id'],data['_entity_poly.pdbx_seq_one_letter_code_can'])}
    chains={chain:{'id':chain,'entity':entity,'sequence':sequence[entity],
        'protein':'barnase' if entity=='1' else 'barstar', 'residues':[]}
        for chain,entity in zip(data['_struct_asym.id'],data['_struct_asym.entity_id']) if entity in sequence}
    parser=MMCIFParser(QUIET=True,auth_chains=False,auth_residues=False)
    structure=parser.get_structure('1BRS',str(path))
    selected={}
    count=len(data['_atom_site.id'])
    for row in range(count):
        get=lambda name:data['_atom_site.'+name][row]
        if get('pdbx_PDB_model_num')!='1' or get('label_atom_id')!='CA': continue
        chain,position=get('label_asym_id'),get('label_seq_id')
        if chain not in chains or position in ('.','?'): continue
        position=int(position)
        candidate={'position':position,'resname':get('label_comp_id'),
            'letter':seq1(get('label_comp_id')),'author_chain':get('auth_asym_id'),
            'author_number':get('auth_seq_id'),'insertion_code':get('pdbx_PDB_ins_code'),
            'altloc':get('label_alt_id'),'occupancy':float(get('occupancy')),
            'xyz_A':[float(get('Cartn_'+axis)) for axis in 'xyz'],
            'bfactor_A2':float(get('B_iso_or_equiv'))}
        key=(chain,position)
        if key not in selected or candidate['occupancy']>selected[key]['occupancy']:
            selected[key]=candidate
    maximum_error=0.
    for chain,record in chains.items():
        for position,letter in enumerate(record['sequence'],1):
            observed=selected.get((chain,position))
            if observed:
                assert observed['letter']==letter
                atom=structure[0][chain][position]['CA']
                maximum_error=max(maximum_error,float(np.max(np.abs(atom.coord-np.array(observed['xyz_A'])))))
            record['residues'].append(observed or {'position':position,'letter':letter,'xyz_A':None,'bfactor_A2':None})
        record['observed_count']=sum(r['xyz_A'] is not None for r in record['residues'])
        record['missing']=[r['position'] for r in record['residues'] if r['xyz_A'] is None]
        xyz=np.array([r['xyz_A'] if r['xyz_A'] is not None else [np.nan]*3 for r in record['residues']])
        record['xyz']=xyz
        record['distances']=np.linalg.norm(xyz[:,None,:]-xyz[None,:,:],axis=-1)
    assert maximum_error<1e-5  # Parser coordinates are float32; mmCIF decimals are read as float64.
    return chains,structure,maximum_error


def contacts(record,cutoff=8.,separation=4):
    n=len(record['sequence']);positions=np.arange(1,n+1)
    mask=(record['distances']<=cutoff)&(np.abs(positions[:,None]-positions[None,:])>=separation)
    return np.argwhere(np.triu(mask,1))


def projection(xyz):
    # One fixed orthographic view, shared by each pair of overlaid structures.
    a,b=np.deg2rad([35.,25.])
    rz=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    rx=np.array([[1,0,0],[0,np.cos(b),-np.sin(b)],[0,np.sin(b),np.cos(b)]])
    return xyz@rz.T@rx.T


def draw_trace(ax,xyz,color=BLUE,lw=1.8):
    p=projection(xyz)
    # NaN positions break the drawn trace at a missing coordinate.
    ax.plot(p[:,0],p[:,1],color=color,lw=lw)
    ax.set_aspect('equal');ax.set_xlabel('u / Å');ax.set_ylabel('v / Å')


def compare_copies(chains,structure):
    common=[i for i in range(1,90) if i not in chains['D']['missing']]
    fixed=[structure[0]['D'][i]['CA'] for i in common]
    moving=[structure[0]['F'][i]['CA'] for i in common]
    fit=Superimposer();fit.set_atoms(fixed,moving)
    rot,tran=fit.rotran
    transformed=chains['F']['xyz']@rot+tran
    delta=np.linalg.norm(chains['D']['xyz']-transformed,axis=1)
    rms=float(np.sqrt(np.nanmean(delta**2)))
    assert abs(rms-fit.rms)<1e-5
    return {'common_positions':common,'rotation':rot.tolist(),'translation_A':tran.tolist(),
            'rmsd_A':rms,'F_aligned_xyz_A':transformed.tolist(),
            'residue_deviation_A':[None if np.isnan(x) else float(x) for x in delta]}


def make_figures(chains,comparison,out,language):
    zh=language=='zh';tr=lambda cn,en:cn if zh else en
    plt.rcParams.update({'font.family':available_plot_fonts() if zh else ['DejaVu Sans'],
        'font.size':13,'axes.titlesize':15,'axes.labelsize':14,'svg.fonttype':'path',
        'figure.facecolor':'#faf9f6','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        for ext in ('svg','png'):fig.savefig(out/f'{name}-{language}.{ext}',dpi=165,bbox_inches='tight')
        plt.close(fig)
    fig=plt.figure(figsize=(13,7.5),layout='constrained')
    gs=fig.add_gridspec(2,1,height_ratios=[1,.85])
    ax=fig.add_subplot(gs[0]);arr=np.full((6,110),np.nan)
    for row,record in enumerate(chains.values()):
        arr[row,:len(record['sequence'])]=1
        arr[row,np.array(record['missing'],dtype=int)-1]=0
    cm=ListedColormap([ORANGE,BLUE]);cm.set_bad('#e7e9e9')
    ax.imshow(arr,aspect='auto',interpolation='nearest',cmap=cm,vmin=0,vmax=1,extent=[.5,110.5,5.5,-.5])
    ax.set_yticks(range(6),[f"{r['id']} · {r['protein']}  {r['observed_count']}/{len(r['sequence'])}" for r in chains.values()])
    ax.set_xlabel(tr('沉积序列位置 label_seq_id','Deposited sequence position label_seq_id'))
    ax.set_title(tr('蓝：有 Cα 坐标；橙：缺少坐标；灰：超出该链序列','Blue: Cα present; orange: absent; gray: beyond this chain'))
    ax=fig.add_subplot(gs[1]);ax.set_xlim(59.5,70.5);ax.set_ylim(-.7,2.6)
    for row,chain in enumerate(['D','E','F']):
        r=chains[chain]
        for pos in range(60,71):
            missing=pos in r['missing']
            ax.add_patch(plt.Rectangle((pos-.46,row-.32),.92,.64,facecolor=ORANGE if missing else BLUE))
            ax.text(pos,row,r['sequence'][pos-1],color='white',ha='center',va='center',fontsize=16,weight='bold')
    ax.set_yticks(range(3),['D','E','F']);ax.set_xticks(range(60,71));ax.set_xlabel(tr('序列位置；字母仍保留在缺坐标的位置','Sequence position; letters remain at positions without coordinates'))
    ax.set_title(tr('放大内部缺口：64 E 与 65 N','Internal-gap detail: 64 E and 65 N'))
    save(fig,'sequence-coverage')

    r=chains['D'];fig=plt.figure(figsize=(13,9),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.25,.65])
    ax=fig.add_subplot(gs[0,0]);draw_trace(ax,r['xyz']);p=projection(r['xyz'])
    values=np.array([x['bfactor_A2'] for x in r['residues']],dtype=float)
    dots=ax.scatter(p[:,0],p[:,1],c=values,cmap='viridis',vmin=0,vmax=70,s=25,zorder=3)
    for pos in (63,66):ax.scatter(*p[pos-1,:2],s=80,facecolor=ORANGE,edgecolor='white',zorder=5);ax.annotate(str(pos),p[pos-1,:2],xytext=(6,6),textcoords='offset points')
    ax.set_title(tr('D 链：Cα 轨迹与晶体模型 B 因子','Chain D: Cα trace and crystallographic B factor'))
    fig.colorbar(dots,ax=ax,shrink=.65,label='B / Å²')
    ax=fig.add_subplot(gs[0,1]);distance=np.ma.masked_invalid(r['distances']);cmap=plt.get_cmap('magma_r').copy();cmap.set_bad('#cbd3d8')
    im=ax.imshow(distance,origin='lower',extent=[.5,89.5,.5,89.5],cmap=cmap,vmin=0,vmax=45,interpolation='nearest')
    ax.set_xlabel(tr('序列位置 j','Sequence position j'));ax.set_ylabel(tr('序列位置 i','Sequence position i'))
    ax.set_title(tr('两点的真实三维距离','Actual three-dimensional point distance'))
    fig.colorbar(im,ax=ax,shrink=.65,label='d / Å')
    ax=fig.add_subplot(gs[1,:]);positions=np.arange(1,90)
    for chain,color in [('D',BLUE),('E',ORANGE),('F',GREEN)]:
        ax.plot(positions,[x['bfactor_A2'] for x in chains[chain]['residues']],color=color,lw=1.8,label=chain)
    ax.axvspan(63.5,65.5,color='#dbe1e5',alpha=.7);ax.set_xlabel(tr('barstar 序列位置','Barstar sequence position'));ax.set_ylabel('Cα B / Å²');ax.legend(ncol=3);ax.grid(alpha=.16)
    save(fig,'structure-and-distance')

    fig=plt.figure(figsize=(13,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[.62,1])
    ax=fig.add_subplot(gs[0,:]);ax.axis('off')
    columns=['label_seq_id',tr('序列字母','Sequence letter'),tr('D 链有 Cα？','Cα in D?'),tr('坐标列表行号（从 1 开始）','Coordinate-list row (one-based)')]
    cell=[]
    observed=[x['position'] for x in r['residues'] if x['xyz_A'] is not None]
    for pos in range(62,68):cell.append([pos,r['sequence'][pos-1],tr('有','Yes') if pos in observed else tr('缺少','Absent'),observed.index(pos)+1 if pos in observed else '—'])
    table=ax.table(cellText=cell,colLabels=columns,cellLoc='center',bbox=[0,.03,1,.94],colWidths=[.19,.18,.18,.45]);table.auto_set_font_size(False);table.set_fontsize(13)
    for (i,j),c in table.get_celld().items():
        c.set_edgecolor('#d4dde2')
        if i==0:c.set_facecolor('#dce9ee')
        elif i in (3,4):c.set_facecolor('#f5dfd7')
    ax=fig.add_subplot(gs[1,0]);fxyz=np.array(comparison['F_aligned_xyz_A']);draw_trace(ax,r['xyz'],BLUE);draw_trace(ax,fxyz,GREEN,lw=1.3)
    p=projection(fxyz)
    for pos in (64,65):ax.scatter(*p[pos-1,:2],color=ORANGE,s=90,zorder=8);ax.annotate(f'F:{pos}',p[pos-1,:2],xytext=(7,7 if pos==64 else -17),textcoords='offset points',color=ORANGE)
    ax.set_title(tr('D（蓝）与对齐后的 F（绿）','D (blue) and aligned F (green)'))
    ax=fig.add_subplot(gs[1,1]);ax.axis('off')
    lines=[(tr('序列位置 ↔ 空间坐标','Sequence positions ↔ coordinates'),15),
           (tr('1958 · Sanger：胰岛素序列','1958 · Sanger: insulin sequence'),14),
           (tr('1960 · Kendrew 等：肌红蛋白结构','1960 · Kendrew: myoglobin structure'),14),
           (tr('1971 · PDB：初始收录 7 个结构','1971 · PDB: seven initial structures'),14),
           (tr('1BRS D/F：沉积序列相同','1BRS D/F: same deposited sequence'),14),
           (tr(f'D/F：87 个共同 Cα；RMSD {comparison["rmsd_A"]:.3f} Å',f'D/F: 87 common Cα; RMSD {comparison["rmsd_A"]:.3f} Å'),14),
           (tr('橙色 64/65：F 链有坐标，D 链空缺','F:64/65 have coordinates; D:64/65 absent'),14)]
    for k,(text,size) in enumerate(lines):ax.text(0,.97-k*.135,text,fontsize=size,va='top',color=INK,weight='bold' if k==0 else 'normal')
    save(fig,'mapping-and-history')


def clean(value):
    if isinstance(value,np.ndarray):return clean(value.tolist())
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,list):return [clean(v) for v in value]
    if isinstance(value,float) and not np.isfinite(value):return None
    return value


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('results'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    chains,structure,coordinate_error=read_chains(INPUT)
    records=[SeqRecord(Seq(r['sequence']),id='1BRS_'+r['id'],description=r['protein']+' deposited polymer sequence') for r in chains.values()]
    fasta=args.output/'deposited-sequences.fasta';SeqIO.write(records,fasta,'fasta')
    reread=SeqIO.to_dict(SeqIO.parse(fasta,'fasta'));assert all(str(reread[r.id].seq)==str(r.seq) for r in records)
    fields=['chain','position','letter','observed_CA','author_chain','author_number','insertion_code','bfactor_A2','x_A','y_A','z_A']
    with (args.output/'residue-map.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields);writer.writeheader()
        for chain,record in chains.items():
            for r in record['residues']:
                row={k:r.get(k) for k in fields};row.update(chain=chain,observed_CA=r['xyz_A'] is not None)
                for axis,v in zip('xyz',r['xyz_A'] or [None]*3):row[axis+'_A']=v
                writer.writerow(row)
    comparison=compare_copies(chains,structure)
    summary={'pdb_id':'1BRS','source_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        'parser_coordinate_max_difference_A':coordinate_error,
        'chains':{key:{'length':len(r['sequence']),'observed_CA':r['observed_count'],'missing':r['missing'],
                  'coverage':r['observed_count']/len(r['sequence']),'contacts_8A_sep4':len(contacts(r))} for key,r in chains.items()},
        'D_62_63_distance_A':float(chains['D']['distances'][61,62]),
        'D_63_66_distance_A':float(chains['D']['distances'][62,65]),'DF_common_CA':87,'DF_rmsd_A':comparison['rmsd_A']}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    payload={'chains':chains,'comparison':comparison,'bfactor_colors':(plt.get_cmap('viridis')(np.linspace(0,1,256))[:,:3]*255).round().astype(int).tolist()}
    (args.output/'lab-data.json').write_text(json.dumps(clean(payload),ensure_ascii=False),encoding='utf8')
    make_figures(chains,comparison,args.output,args.language)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

运行后，`deposited-sequences.fasta` 保存六条完整序列，`residue-map.csv` 保存每个位置与已观察原子的对应关系，`summary.json` 给出覆盖、缺口、距离和对齐结果。FASTA 写出后再读回，逐条核对标识和字母；坐标从字典与结构对象两条路径读取并比较；RMSD 则由变换后的坐标再次直接计算。把这些检查放在数据进入下一步之前，有助于发现序列错位、链选择错误和单位混用，而不是等到最终图形异常时再向前猜测。

### 运行完整示例

将 en 换成 zh 可生成中文图；输入路径相对于脚本定位。

```
python main.py --output results --language en
```

可以用输出表中的五行来检查整个过程：D:63 为 T，有坐标；D:64 为 E，空缺；D:65 为 N，空缺；D:66 为 G，有坐标；D:67 为 A，有坐标。CSV 的空白坐标单元格在分析时应读成缺失值，而不是字符串零。FASTA 中对应的片段仍是 TENGA，说明序列没有随坐标缺失而被删短。若只需要已观察坐标用于后续计算，可以另建筛选后的数组，同时保留原序列位置列；以后将结果放回完整序列时，按位置重新连接即可，不必猜测删除了多少行。

## 沿着一个残基，同时读序列、结构与接触图

实验从 D 链开始。把选中位置移动到 63，可以在序列格子、三维坐标的投影图和接触矩阵中追踪同一个残基；再移动到 64，字母 E 仍在，但坐标、距离和接触邻居显示为空。继续到 66，结构重新出现，对应表会说明它是序列第 66 位。这个小过程比只看一个“缺少 2 个残基”的数字更直观，因为你可以看到缺口怎样同时影响三种表示，而序列位置始终保持一致。

转动视角时，投影图中的两点可能重合或分开，三维距离与接触计数保持不变。视角控制改变观察方向，阈值控制改变分析定义，两个操作回答不同问题。把阈值从 8 Å 改到 6 Å，满足条件的接触减少，矩阵和选中残基的邻居表一起更新；改变最小序列间隔，则能看见局部主链邻近对统计的影响。切换到 F 链再访问 64、65 位，可以比较相同字母在另一个拷贝中保留的坐标，而不是将缺失值误读为缺少这两个氨基酸。

## 残基对应与接触实验

从 D:63 移动到 D:64，再到 D:66，观察相同位置在序列、结构和矩阵中的状态。旋转视角保持真实三维距离不变。

[Figure: 完整沉积序列与坐标覆盖](https://ml-biomat.com/tutorials/python-scientific/s05/#S05-sequence)

蓝格有坐标，橙格缺坐标；黑框是选中位置。

[Figure: 真实三维坐标的正交投影](https://ml-biomat.com/tutorials/python-scientific/s05/#S05-view)

曲线在缺口处断开；橙色连线连接选中残基的当前接触邻居。颜色表示 Cα B 因子。

[Figure: 接触矩阵](https://ml-biomat.com/tutorials/python-scientific/s05/#S05-matrix)

蓝色为满足条件的接触，浅色为其余已知距离，灰色为缺坐标。橙框标记选中位置。

[Figure: 选中位置到全部序列位置的距离](https://ml-biomat.com/tutorials/python-scientific/s05/#S05-profile)

虚线是距离阈值；橙点同时满足距离和序列间隔条件。

扩展到自己的蛋白质时，先确定序列来自实验构建体、数据库参考序列还是某个结构条目的沉积序列，并明确采用哪个模型和哪条链。若要把 UniProt 位点映射到截短构建体，通常还需要序列比对或已有数据库映射，不能把两个系统的位置数字直接相等。当前程序解决的是同一 mmCIF 条目内部、由标准字段给出的对应关系。在这一基础上，突变标记、局部结构检查和后续轨迹分析都可以共享同一张残基映射表，使每一个数值都能回到明确的序列位置。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Biopython Tutorial: Going 3D](https://biopython.org/docs/latest/Tutorial/chapter_pdb.html)

   mmCIF、结构层次、坐标与对齐操作。

   Biopython License Agreement covers software and documentation; some files offer BSD 3-Clause as an alternative.
2. [Biopython Tutorial: Sequence Input/Output](https://biopython.org/docs/latest/Tutorial/chapter_seqio.html)

   SeqRecord 与 FASTA 读写。

   Biopython License Agreement.
3. [PDB 1BRS: barnase–barstar complex](https://www.rcsb.org/structure/1BRS)

   原始公开结构与沉积序列，2.00 Å X 射线晶体模型。

   PDB archive data: CC0 1.0.
4. [Buckle, Schreiber and Fersht (1994)](https://doi.org/10.1021/bi00196a004)

   1BRS 的原始结构研究，Biochemistry 33, 8878–8889。

   American Chemical Society journal article.
5. [wwPDB: label_seq_id and author numbering](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_atom_site.auth_seq_id.html)

   标准序列位置与作者编号的含义。

   wwPDB dictionary reference.
6. [Sanger (1958): The Chemistry of Insulin](https://www.nobelprize.org/prizes/chemistry/1958/sanger/lecture/)

   蛋白质序列测定的历史背景。

   Nobel lecture; historical reference.
7. [Kendrew et al. (1960): Structure of Myoglobin](https://doi.org/10.1038/185422a0)

   肌红蛋白 2 Å 三维结构的原始论文。

   Nature journal article.
8. [RCSB PDB History](https://www.rcsb.org/pages/about-us/history)

   1971 年 PDB 建立与最初 7 个结构。

   RCSB website content: CC BY 4.0.
