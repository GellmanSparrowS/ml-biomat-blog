# 拉伸实验：从一条曲线认识材料

Source: https://ml-biomat.com/tutorials/experimental-methods/m01/
Language: zh-CN

从力和标距开始，区分模量、屈服、强度与吸收功，并看清夹具和尺寸怎样进入结果。

## 一根线能承受多大拉力，与它有多难拉长，是两件事

缝合线需要在牵拉时保持连接，包装薄膜需要在搬运中承受拉扯，可穿戴传感器又需要跟随皮肤伸展。对这些材料，只问“结不结实”会把几个不同问题混在一起：开始拉它时有多费力，什么时候出现难以恢复的变形，最大能承受多大力，以及最终能伸长多少。拉伸实验把这些问题放进同一段受控过程：夹住试样两端，逐渐拉开，连续记录力和伸长，再结合试样尺寸绘出应力–应变曲线。曲线的不同位置对应不同物理信息，因此一张图往往比一个“强度”数字更能说明用途。

先比较两根用同一种材料制成的直条。粗条需要更大的力才能产生同样的相对伸长，因为更多横截面积共同承担负载；长条在相同相对伸长下会增加更多绝对长度，因为参与变形的长度更大。如果直接比较力与毫米数，就把材料性质和几何尺寸混在一起。工程应力用力除以原始横截面积，工程应变用标距增加量除以原始标距。归一化让我们能够在合适的试样和加载条件下比较材料响应，同时保留方向、温度、速度和结构的影响。对于纤维、打印件和生物组织，取样方向尤其需要说明。

一个容易记住的对照是弹性带与细玻璃条。弹性带可以伸长很多，初始拉伸可能并不费力；玻璃条在小变形时很难拉长，却可能在较小伸长下断裂。刚度、强度与延展性分别描述不同方面，不能用其中一个替代另外两个。拉伸曲线下的面积还描述试样在规定加载路径中吸收了多少机械功。生物材料设计常需要这些指标一起考虑：柔软的材料便于匹配组织变形，足够的承载和抗破坏能力则支持它完成连接、包覆或支撑任务。

## 从Hooke的弹簧，到标距上的两枚小点

Hooke在1678年公开讨论弹性时，用增加负载、观察伸长的实验说明弹簧的比例关系。他对弹簧和计时装置的兴趣，也把抽象的力学规律与实际器件联系起来。图中的两根弹簧用一倍与两倍负载展示这一思想。现代拉伸机沿用的核心问题仍然直观：施加的力怎样对应形变？改变之处是测量精度、加载控制和对试样几何的处理。弹簧整体的力–位移斜率属于结构刚度，而从应力–应变斜率得到的模量进一步除去了特定几何影响，二者通过长度与面积联系。

![原创历史与测量示意：Hooke负载–伸长思想、哑铃试样标距，以及试样与机架夹具的串联位移。图为原理示意，非标准试样尺寸图。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0eb82637e52bb49dee315450.svg?v=0eb82637e52b)

图 1原创历史与测量示意：Hooke负载–伸长思想、哑铃试样标距，以及试样与机架夹具的串联位移。图为原理示意，非标准试样尺寸图。

力传感器的量程也应与试样匹配。若试样只产生很小的力，却使用为大负载设计的传感器，低载荷区的分辨能力可能不足，恰好影响初始模量。选择合适量程后，还需检查校准、零点和装夹后的预载。零点漂移会让应力轴整体平移，夹具自重或安装方式则可能影响加载前读数。对于易损试样，装夹和施加预载本身就可能造成变化，因此应把这一阶段作为实验的一部分，而不是在正式采集开始时才认为试样有了历史。

试样常做成中间窄、两端宽的哑铃形。宽端便于夹持，窄的平行段让变形集中在适合观察的位置，平滑过渡则减小肩部的应力集中。标距是在平行段上选定的两个测量位置之间的原始距离，它可以短于两夹具之间的距离，也不同于试样总长。图中两枚小点是光学引伸测量的标记；相机跟踪它们的间距，直接得到该段材料的伸长。接触式引伸计也能在规定位置测量距离变化，适合的装置取决于试样刚度、尺寸、伸长范围和表面状况。

拉伸机横梁的位移包含整个加载链的变化。除了试样本身，机架、力传感器、夹具和连接部件也会发生微小变形，夹持处还可能逐渐就位或滑动。把这些部分想成串联的弹簧，可以理解为什么总位移等于各部分位移之和。对于短而硬的试样，材料自身伸长很小，装置变形所占比例就可能很大；直接把横梁位移当作标距伸长，会使曲线显得更平缓。这个现象不是材料突然变软，而是测量距离包含了额外部分，因此需要用局部引伸或适当的系统柔度校正来分开。

生物组织和软水凝胶还带来不同的夹持问题。过紧可能在夹口压坏试样，过松可能滑脱；试样脱水会在实验期间改变尺寸与力学响应。应根据材料选择适合的夹具、环境与预处理，并记录水合状态和等待时间。用于比较的试样应具有一致的取样方向和有效截面，边缘缺口、气泡或裁切损伤也应进入样品记录。几何准备并非曲线之外的杂事，它直接决定负载通过哪里传递，以及计算中的面积和长度究竟对应哪一部分材料。

## 把牛顿和毫米，换成可以比较的应力与应变

设一条试样的原始标距为50毫米，横截面积为10平方毫米。在某个时刻，力达到100牛顿，两标记之间增加0.25毫米。工程应力为10牛顿每平方毫米，也就是10兆帕；工程应变为0.005，也可写成百分之零点五。应变没有长度单位，因为分子与分母使用相同单位。百分数与小数代表同一比例，但计算斜率时必须一致：若把0.5直接当作0.005代入，模量会错一百倍。图的横轴可以用百分数方便阅读，程序内部则采用无量纲小数。

$$
\sigma_e=\frac{F}{A_0},\qquad\varepsilon_e=\frac{L-L_0}{L_0}=\frac{\Delta L}{L_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | 工程应力，MPa=N/mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 轴向拉力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 原始横截面积，mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | 工程应变，无量纲；乘100显示为百分数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 当前标距，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | 原始标距，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6ca346d066653af4cd6f62fe.svg) | 标距伸长L−L0，mm。 |

用原始尺寸归一化。F=100 N、A0=10 mm²、ΔL=0.25 mm、L0=50 mm时，σe=10 MPa、εe=0.005=0.5%。

“原始”二字决定了工程量的定义。面积在试样未受力时测量，标距也取加载前的参考值。若采用小预载使试样拉直，需要说明参考长度是在什么状态下确定的。宽度与厚度最好在有效测量区域取得，薄膜厚度测量尤其要避免探头压力把软样品压薄。圆形纤维由直径计算面积时，直径误差会经过平方关系放大。对于不规则组织截面，面积定义应与实际测量方法一起保存；一个录入错误的面积会按相同比例移动整条应力曲线，却不会在原始力信号中留下明显异常。

$$
E=\frac{d\sigma_e}{d\varepsilon_e},\qquad k_s=\frac{EA_0}{L_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 线性小应变区模量，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | 工程应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | 工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/778e841bd8e233461c668db9.svg) | 均匀试样的轴向结构刚度，N/mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 原始截面积，mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | 原始标距，mm。 |

微分表示局部斜率；直线区可由应力增量除应变增量。E=2000 MPa、A0=10 mm²、L0=50 mm得到ks=400 N/mm。

在线性小应变区，模量是应力随应变增加的斜率。本例10兆帕除以0.005，得到2000兆帕，也就是2吉帕。对应的试样结构刚度为每毫米400牛顿：增加0.25毫米需要100牛顿。把试样长度加倍而保持材料和面积不变，结构刚度减半，但模量仍为2吉帕。把面积加倍则结构刚度加倍，模量仍不变。这个对照解释了为什么实验报告中既要保存原始力–位移，也要保存尺寸归一化后的曲线：前者描述具体试样怎样承载，后者支持在明确条件下比较材料响应。

初始曲线不一定天然就是直线。试样弯曲被拉直、夹具逐渐就位、纤维束逐步拉紧，以及材料本身的非线性都能产生低载荷弯曲。应根据观察和材料机制区分这些来源，再选择有物理含义的拟合区间。若材料本身持续非线性，可以报告指定应变处的切线斜率，或两个明确应变之间的割线模量，并把区间写清。把曲线上任意一小段直线都命名为唯一的Young模量，会失去比较基础；明确测量定义后，不同研究者才能重复同一计算。

## 为什么相同试样能被算出两种模量

本章构造了一条已知响应，便于把计算误差与材料变化分开。指定初始模量为2000兆帕，工程应变达到2%时应力为40兆帕，随后以较小斜率增加，到20%时达到50.8兆帕，再进入下降段，40%时结束记录。这样的分段曲线用于识别初始斜率、峰值与积分，并不代表某一种指定商品材料的实测行为。程序把应力乘以10平方毫米面积得到力，给力与局部应变加入小幅噪声，并额外生成包含系统柔度的横梁位移。这样，每一个观测通道都有清楚的生成原因。

$$
\Delta L_x=\Delta L_s+C_mF,\qquad E_x=\frac{E}{1+EA_0C_m/L_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c60cc7d4d1bf6d7386dcb6b.svg) | 横梁位移，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2aef3aeea0e2f9ed660eb869.svg) | 试样标距伸长，mm。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b4840a9faca02419281df787.svg) | 串联系统柔度，mm/N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 轴向力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af9e236724ae69e17d4a69bc.svg) | 横梁位移除标距得到的表观模量，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 真实线性模量，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 原始面积，mm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | 原始标距，mm。 |

采用线性串联模型并忽略滑移。E=2000、A0=10、L0=50、Cm=0.001时，分母1.4，Ex=1428.571 MPa；100 N时系统多移动0.1 mm。

系统柔度取每牛顿0.001毫米，意味着100牛顿时装置额外伸长0.1毫米。此时试样实际伸长0.25毫米，横梁总位移却为0.35毫米。若都除以50毫米标距，横梁应变成为0.007，于是10兆帕除以0.007只能得到约1428.57兆帕。程序在0.1%到0.8%的指定区间拟合含噪数据，局部引伸结果约2002.02兆帕，横梁结果约1428.49兆帕。两条曲线来自同一个材料模型，差别完全由位移定义与测量噪声产生。

![构造记录：原始力与两类位移、尺寸归一化、初始区放大和拟合窗口扫描。局部与横梁差异来自规定系统柔度，2%后规定曲线离开初始直线。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/40bf887b277bcd0ecde44973.svg?v=40bf887b277b)

图 2构造记录：原始力与两类位移、尺寸归一化、初始区放大和拟合窗口扫描。局部与横梁差异来自规定系统柔度，2%后规定曲线离开初始直线。

图中的拟合窗口扫描从同一应变下限开始，逐渐扩大上限。窗口完全位于初始直线区时，斜率围绕指定模量小幅变化；跨过2%的转折后，较平缓的后续响应被纳入，拟合斜率逐渐下降。窗口选择因此是一项实验定义，而不是只要让拟合优度更高就能自由调整的显示选项。真实实验应按研究对象与适用方法确定区间，并观察残差和局部形变。若一组材料采用不同区间，模量差异可能同时包含区间效应，需要在比较中明确。

还要注意时间同步。力传感器与相机若使用不同采样频率或存在时间延迟，快速变化区的力与伸长可能被错误配对，产生不真实的曲率或回线。把原始时间戳一并保存，确认采集系统的同步方式，必要时在有依据的条件下重采样。平滑可以降低高频噪声，但过强平滑会移动峰值或掩盖突变；对模量、峰值和断裂点使用的处理应可追踪。数据处理的目标是保留与问题相关的变化，而不是把每一条曲线都变成同样光滑的形状。

## 在曲线上分别找到刚度、屈服、强度与吸收功

初始斜率之后，研究者常关心不可恢复变形何时变得明显。有些材料具有清楚的屈服特征，另一些则平缓过渡。偏移法提供一种约定的读数：画一条与选定弹性斜率平行、沿应变轴移动规定距离的直线，取它与曲线的交点。常见的0.2%偏移量等于0.002无量纲应变，但实际采用的定义应与材料和测试方法一致。本章用这一常见构造演示算法，避免把它当成所有聚合物或软组织都具有的统一屈服定义。

$$
\sigma_{\mathrm{offset}}=E_{\mathrm{fit}}(\varepsilon_e-\varepsilon_0)+b
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f86396c182c082f1d21a5f.svg) | 偏移直线上的应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a4e517b14dbb473355e98a18.svg) | 选定区间拟合斜率，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | 工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 规定偏移，本例0.002=0.2%。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 原始拟合直线截距，MPa。 |

寻找此线与应力–应变曲线的交点。指定无噪声模型中Efit=2000、b=0，交点40.123711 MPa；偏移定义与材料测试方法配套。

指定曲线的0.2%偏移交点约为40.124兆帕，含噪曲线得到约40.097兆帕。这个数值与初始直线在40兆帕处结束是两个不同定义。最大工程应力则是整条曲线的最高点，本例约50.8兆帕；它与断裂前最后一个应力也不同。试样可以在达到最大负载后继续伸长，并在更低工程应力处断开。对于存在颈缩的材料，形变逐渐集中在局部区域，原始面积归一化的整体曲线仍有工程意义，但局部应力和局部伸长需要进一步观察。

![指定教学曲线的0.2%偏移、均匀恒体积阶段真应力转换与拉伸功。积分使用无量纲应变；横轴百分数仅为显示。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bacb0fb3380e517bd0076d81.svg?v=bacb0fb3380e)

图 3指定教学曲线的0.2%偏移、均匀恒体积阶段真应力转换与拉伸功。积分使用无量纲应变；横轴百分数仅为显示。

$$
\sigma_t=\sigma_e(1+\varepsilon_e),\qquad\varepsilon_t=\ln(1+\varepsilon_e)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/87de164e10556b3dda44460d.svg) | 当前面积上的真应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | 原始面积上的工程应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c56edde4f1d59f195d1ee.svg) | 沿均匀拉伸方向的对数真应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | 工程应变，无量纲。 |

应力换算要求均匀单轴变形且体积近似守恒。εe=0.2、σe=50.8 MPa时，σt=60.96 MPa、εt=0.182322；颈缩后需局部几何。

在均匀单轴变形且体积近似守恒的阶段，试样伸长时横截面积缩小，因此真应力高于工程应力。20%工程应变对应长度变为原来的1.2倍；若面积相应变为原来的1/1.2，50.8兆帕工程应力对应60.96兆帕真应力，真应变为约0.18232。颈缩后各处伸长不再相同，不能继续用一个全局伸长比自动推算颈部面积。图中的转换限定在指定的均匀阶段，后续区域留给局部尺寸或全场测量，而不是把同一公式机械延伸到断裂。

$$
W_V=\int_0^{\varepsilon_f}\sigma_e\,d\varepsilon_e
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/104ddb2cc44384e56d1f9bb2.svg) | 单位原始体积的拉伸功，MJ/m³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8ebdb3fc88042909ea28a74.svg) | 本次路径终点工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | 工程应力，MPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | 工程应变，无量纲。 |

由功F dL除以原始体积A0L0得到。指定曲线终点0.4，三段梯形面积0.4+8.172+8.56=17.132 MJ/m³；这与裂纹扩展的单位新生面积能量不同。

积分与功的关系可以从一小步伸长看出来。在很短的一步里，力近似不变，外界做功等于力乘伸长。把力写成工程应力乘原始面积，再把伸长写成原始标距乘应变增量，原始面积与原始标距的乘积正好是参考体积。因此，对整条曲线逐段累加后，除以参考体积就得到应力–应变面积。这个推导要求力与伸长对应同一试样受力段；若用包含装置变形的横梁位移积分，就同时计入了加载系统中储存或消耗的功，不能仍把全部面积归给材料。

曲线下面积可以通过小梯形逐段相加，得到单位原始体积的拉伸功。应力单位为兆帕、应变无量纲时，数值对应兆焦每立方米。示例三个线性段分别贡献0.4、8.172和8.56，总计17.132兆焦每立方米。这个量描述规定试样和加载路径的整体吸收功；含裂纹试样的裂纹扩展阻力则需要断裂实验和不同的面积归一化。二者都与抗破坏有关，却使用不同对象与分母。区分它们，能够避免把一条光滑试样曲线的积分直接当作裂纹韧性。

## 让不同试样之间的比较真正可用

聚合物与生物组织的响应常随加载速度变化。慢拉时链段、液体或组织结构有更多时间调整，快拉时这些过程可能来不及完成；温度和水分也会改变调整速度。即使横梁速度相同，标距不同也会产生不同的名义应变速率。例如每分钟5毫米作用于50毫米标距，在理想均匀伸长下对应每分钟0.1的工程应变变化率；标距减半时，这个比例加倍。比较材料时，应说明控制的是横梁速度、局部应变速率还是其他加载程序，并保持环境与预处理一致。

试样方向与微结构同样影响曲线。沿纤维方向拉伸，负载更多由纤维承担；横向拉伸时，界面和基体可能更重要。打印材料还具有层间结合、孔隙与路径方向，生物组织具有纤维取向和层级结构。报告“材料模量”时，方向与制备状态属于结果定义的一部分。若目标是了解器件实际承载，可以按器件方向测试；若目标是建立材料模型，则可能需要多个方向、多个速度或不同加载方式。一个方向的拉伸试验提供一条明确的信息，并与后续压缩、循环或松弛实验形成互补。

![系统柔度与录入面积的独立敏感性，以及七个独立构造试样的模量。右图线为均值，带为均值±样本标准差，不是均值置信区间。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/05d8e95e96f34d2ca7c37c9a.svg?v=05d8e95e96f3)

图 4系统柔度与录入面积的独立敏感性，以及七个独立构造试样的模量。右图线为均值，带为均值±样本标准差，不是均值置信区间。

断裂伸长还与标距如何覆盖局部变形有关。假设一条试样在很短的颈部额外伸长2毫米，其他部分变化较少；用20毫米标距平均，这部分贡献10%应变，用50毫米标距平均则贡献4%。两种数字可以来自同一处局部伸长。比较延展性时，标距、试样形状与断后拼接测量方式需要一致。全场成像可以进一步显示变形是否集中，但从全场图提取平均量时，选取区域仍然是计算定义的一部分，不能在不同试样中随意改变。

图中的面积敏感性显示，真实面积10平方毫米若被录成11，全部应力和模量会乘上10/11，2000兆帕变为约1818.18。系统柔度与面积误差因此有不同的来源，却可能同时把模量向下移动。重复测量能反映随机波动，但每次使用同一错误面积不会在重复散点中暴露。另一面板给出七个独立构造试样的模量，均值约2013.82兆帕，样本标准差约75.74兆帕；色带表示均值上下一个样本标准差，用来展示试样间离散，而非均值的置信区间。

断裂位置也值得与曲线一起记录。若多数试样都在夹口或肩部破坏，可能是夹持或过渡几何主导了结果；若断裂发生在标距内，局部缺陷和材料结构更值得继续观察。断后照片、标记轨迹和样品尺寸能够把异常曲线与具体情况联系起来。对一条突然掉力的记录，先检查是否真正断裂、是否滑脱、是否触发了停止条件，再决定它属于哪类结果。保留这些事实，有助于把统计中的离群点变成可解释的实验事件。

## 交互实验：只改测量方法，材料会不会“变软”

下面的模型材料始终具有2000兆帕模量，真实面积10平方毫米、标距50毫米。你可以改变录入面积、系统柔度，并在局部引伸与横梁位移之间切换。先使用正确面积和局部引伸，曲线斜率应保持2000；随后增加系统柔度，局部曲线不变，而横梁曲线逐渐变平。再把输入面积改成11平方毫米，两种方式得到的应力都会降低。交互将几何归一化和位移来源分开，因此每次变化都可以用前面的公式手算核对。

## 交互：材料与测量定义

真实材料固定为E=2000 MPa、A=10 mm²、L=50 mm。

[Figure: 初始应力应变曲线](https://ml-biomat.com/tutorials/experimental-methods/m01/#M01-plot)

若希望把实验进一步用于设计，可以先给出允许变形，再由模量、长度和面积估计所需负载。例如同一线性模型下，允许50毫米标距伸长0.1毫米，就对应0.2%应变、4兆帕应力和40牛顿力。若器件使用要求只涉及这一小变形范围，初始刚度很有帮助；若实际动作会拉到20%甚至更大，就需要使用相应区间的完整曲线。把设计工作点标在实验曲线上，能够看出所用参数来自哪一段，也能判断还需要补测多大变形、什么速度或多少次重复加载。

观察点控制实际材料应变，图中同时给出该点力、局部伸长和横梁位移。默认0.5%实际应变时，100牛顿负载使试样伸长0.25毫米，系统柔度额外贡献0.1毫米。若只看到横梁0.35毫米而没有局部测量，就无法单凭这一读数知道两部分各占多少。将系统柔度设为零，两种位移重合；将录入面积恢复真实值，应力归一化也恢复。这些边界情况是检查计算是否合理的简单方法，也帮助理解为什么测试准备和传感器选择能直接影响材料参数。

## 完整处理：从原始通道到可以复算的材料指标

完整程序保存施加应变、测得力、局部伸长、横梁位移和两种应变定义，随后拟合初始斜率、搜索偏移交点、寻找最大工程应力并积分拉伸功。真应力转换只在规定的均匀阶段输出，后续表格保留为空值，提示需要不同的局部信息。代码还扫描拟合窗口，计算面积与系统柔度敏感性，并展示独立构造试样的离散。每一步都有对应图像，既能看到最终数字，也能看清数字对输入定义的依赖。

### 完整Python：拉伸曲线与测量敏感性

保留原始力和两种位移，提取模量、偏移交点、峰值与功，再检查窗口和几何。

```
"""Tensile-test analysis with constructed force and local-extension observations.
Run: python main.py --output results --language en
The piecewise engineering curve is a teaching specification, not measured data.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def stress(strain,E=2000.):
    e=np.asarray(strain);ey=40/E;peak=40+60*(.2-ey)
    return np.where(e<=ey,E*e,np.where(e<=.2,40+60*(e-ey),peak-80*(e-.2)))

def apparent_modulus(area_entered=10.,compliance=.001,method='crosshead'):
    return 2000*10/area_entered/(1+400*compliance if method=='crosshead' else 1)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1901);eps=np.unique(np.r_[np.linspace(0,.03,301),np.linspace(.03,.4,371)]);sig=stress(eps);A=10.;L=50.;C=.001
    force=sig*A+rng.normal(0,.3,len(eps));local=eps+rng.normal(0,.00002,len(eps));cross=(L*eps+C*force)/L
    mask=(eps>=.001)&(eps<=.008);E,b=np.polyfit(local[mask],force[mask]/A,1);Ex,bx=np.polyfit(cross[mask],force[mask]/A,1)
    # Use monotonically ordered imposed strain to interpolate a noisy measured curve.
    fy=lambda x:np.interp(x,eps,force/A)-(E*(x-.002)+b)
    offset=brentq(fy,.02,.03);offset_sig=np.interp(offset,eps,force/A)
    offset_exact=brentq(lambda x:float(stress(x))-2000*(x-.002),.02,.03)
    energy=float(np.trapezoid(sig,eps));peak_idx=int(np.argmax(force));valid=eps<=.2
    true_sig=np.where(valid,sig*(1+eps),np.nan);true_eps=np.where(valid,np.log1p(eps),np.nan)
    ends=np.linspace(.002,.035,60);slopes=[np.polyfit(local[(eps>=.001)&(eps<=en)],force[(eps>=.001)&(eps<=en)]/A,1)[0] for en in ends]
    reps=2000+rng.normal(0,80,7)
    summary={'fit_local_modulus_MPa':float(E),'fit_crosshead_modulus_MPa':float(Ex),'analytic_crosshead_modulus_MPa':apparent_modulus(),
      'offset_yield_MPa':float(offset_sig),'offset_strain':float(offset),'noiseless_offset_yield_MPa':float(stress(offset_exact)),
      'specified_peak_MPa':50.8,'observed_peak_MPa':float(force[peak_idx]/A),'observed_peak_strain':float(eps[peak_idx]),
      'specified_work_MJ_m3':energy,'work_hand_integral_MJ_m3':17.132,'true_stress_at_20pct_MPa':60.96,'true_strain_at_20pct':float(np.log(1.2)),
      'area_11mm2_modulus_MPa':apparent_modulus(11,0,'local'),'replicate_mean_MPa':float(reps.mean()),'replicate_sd_MPa':float(reps.std(ddof=1)),'data_kind':'Constructed teaching observations and specified piecewise engineering response'}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(o/'data.csv',np.column_stack([eps,force,local*L,cross*L,force/A,local,cross,true_sig,true_eps]),delimiter=',',header='imposed_strain,force_N,local_extension_mm,crosshead_extension_mm,engineering_stress_MPa,local_strain,crosshead_strain,uniform_true_stress_MPa,uniform_true_strain',comments='')
    np.savetxt(o/'fit_windows.csv',np.column_stack([ends,slopes]),delimiter=',',header='upper_strain,fit_modulus_MPa',comments='')
    np.savetxt(o/'replicates.csv',reps,delimiter=',',header='constructed_modulus_MPa',comments='')
    fig,axs=plt.subplots(1,3,figsize=(14.5,5));
    for ax in axs:ax.set_xlim(0,10);ax.set_ylim(0,10);ax.axis('off')
    ax=axs[0];ax.plot([.8,9.2],[8.8,8.8],lw=4,color='#6b808d')
    for x,le,n in [(3,3,1),(7,5,2)]:
        yy=np.linspace(8.8,8.8-le,180);xx=x+.4*np.sin(np.linspace(0,12*np.pi,180));ax.plot(xx,yy,color=blue);ax.plot([x,x],[8.8-le,8.2-le],color=blue);ax.add_patch(Rectangle((x-.65,7.2-le),1.3,1,facecolor=orange));ax.text(x,6.6-le,f'{n}F',ha='center')
    ax.text(5,9.5,tr('Hooke，1678：负载与伸长','Hooke, 1678: load and extension'),ha='center',fontsize=10);ax.text(5,.3,tr('弹簧长度变化体现结构刚度','Extension reveals structural stiffness'),ha='center',fontsize=9)
    ax=axs[1];pts=[(2,1),(8,1),(8,2.5),(6.2,3.5),(6.2,6.5),(8,7.5),(8,9),(2,9),(2,7.5),(3.8,6.5),(3.8,3.5),(2,2.5)];ax.add_patch(Polygon(pts,facecolor='#cce2e8',edgecolor=blue,lw=2));ax.add_patch(Rectangle((1.5,.4),7,1.1,color='#8f9fa8'));ax.add_patch(Rectangle((1.5,8.5),7,1.1,color='#8f9fa8'))
    ax.scatter([5,5],[4,6],s=45,color=orange);ax.annotate('',xy=(7,6),xytext=(7,4),arrowprops={'arrowstyle':'<->'});ax.text(7.3,5,'L₀',va='center');ax.text(5,.1,tr('标距内直接跟踪材料伸长','Track local extension inside the gauge'),ha='center',fontsize=9)
    ax=axs[2];ax.add_patch(Rectangle((1.5,7),7,1.2,facecolor='#cce2e8',edgecolor=blue));ax.text(5,7.6,tr('试样','Specimen'),ha='center',va='center');ax.add_patch(Rectangle((1.5,3.4),7,1.2,facecolor='#f1d5be',edgecolor=orange));ax.text(5,4,tr('机架与夹具','Frame and grips'),ha='center',va='center');ax.plot([5,5],[4.6,7],color='#6b808d');ax.annotate('',xy=(5,1),xytext=(5,3.4),arrowprops={'arrowstyle':'->','lw':2});ax.text(5,9.4,tr('串联位移：各部分相加','Series displacement: contributions add'),ha='center',fontsize=10);ax.text(5,.3,tr('横梁移动量包含两者变形','Crosshead travel includes both'),ha='center',fontsize=9);save(fig,'geometry')
    fig,axs=plt.subplots(2,2,figsize=(12,9));aa,bb,cc,dd=axs.ravel();aa.plot(local*L,force,color=blue,label=tr('标距伸长','Gauge extension'));aa.plot(cross*L,force,color=orange,label=tr('横梁位移','Crosshead travel'));aa.set_xlabel(tr('位移 / mm','Displacement / mm'));aa.set_ylabel(tr('力 / N','Force / N'));aa.legend(fontsize=9);aa.set_title(tr('A  原始力与两种位移','A  Force and two displacement channels'),loc='left')
    bb.plot(local*100,force/A,color=blue);bb.scatter(eps[peak_idx]*100,force[peak_idx]/A,color=orange,zorder=3);bb.set_xlabel(tr('工程应变 / %','Engineering strain / %'));bb.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));bb.set_title(tr('B  从尺寸归一化到曲线','B  Normalise by specimen dimensions'),loc='left')
    small=eps<=.012;cc.scatter(local[small]*100,force[small]/A,s=8,color=blue,label=tr('标距','Gauge'));cc.plot(cross[small]*100,force[small]/A,color=orange,label=tr('横梁','Crosshead'));cc.plot(local[mask]*100,E*local[mask]+b,color=green,lw=2,label=tr('标距拟合','Gauge fit'));cc.set_xlabel(tr('应变 / %','Strain / %'));cc.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));cc.legend(fontsize=8);cc.set_title(tr('C  小应变处的柔度差异','C  Compliance matters at small strain'),loc='left')
    dd.plot(ends*100,slopes,color=blue);dd.axhline(2000,color=green,ls='--');dd.axvline(2,color=orange,ls=':');dd.set_xlabel(tr('拟合上限应变 / %','Upper fit strain / %'));dd.set_ylabel(tr('拟合斜率 / MPa','Fitted slope / MPa'));dd.set_title(tr('D  拟合窗口跨入非线性区','D  A fit window enters nonlinearity'),loc='left');fig.tight_layout();save(fig,'analysis')
    fig,axs=plt.subplots(1,3,figsize=(14.5,4.7));aa,bb,cc=axs
    aa.plot(eps*100,sig,color=blue);x=np.linspace(.002,.04,100);aa.plot(x*100,2000*(x-.002),color=orange,ls='--');aa.scatter(offset_exact*100,float(stress(offset_exact)),color=green,zorder=5);aa.set_xlim(0,4);aa.set_ylim(0,65);aa.set_xlabel(tr('工程应变 / %','Engineering strain / %'));aa.set_ylabel(tr('应力 / MPa','Stress / MPa'));aa.set_title(tr('A  0.2%偏移交点','A  Intersection at 0.2% offset'),loc='left')
    bb.plot(eps[valid]*100,sig[valid],color=blue,label=tr('工程应力','Engineering stress'));bb.plot(eps[valid]*100,true_sig[valid],color=orange,label=tr('真应力','True stress'));bb.set_xlabel(tr('工程应变 / %','Engineering strain / %'));bb.set_ylabel(tr('应力 / MPa','Stress / MPa'));bb.legend(fontsize=9);bb.set_title(tr('B  均匀、恒体积阶段','B  Uniform constant-volume interval'),loc='left')
    cc.fill_between(eps*100,0,sig,color='#cce2e8');cc.plot(eps*100,sig,color=blue);cc.text(.05,.85,'17.132 MJ/m³',transform=cc.transAxes);cc.set_xlabel(tr('工程应变 / %','Engineering strain / %'));cc.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));cc.set_title(tr('C  体积归一化的拉伸功','C  Tensile work per initial volume'),loc='left');fig.tight_layout();save(fig,'properties')
    fig,axs=plt.subplots(1,3,figsize=(14,4.8));cm=np.linspace(0,.003,100);axs[0].plot(cm,2000/(1+400*cm),color=orange);axs[0].axhline(2000,color=green,ls='--');axs[0].set_xlabel(tr('系统柔度 / mm/N','System compliance / mm/N'));axs[0].set_ylabel(tr('表观模量 / MPa','Apparent modulus / MPa'));axs[0].set_title(tr('A  横梁法中的系统柔度','A  Compliance in crosshead analysis'),loc='left');area=np.linspace(8,12,100);axs[1].plot(area,2000*10/area,color=blue);axs[1].axvline(10,color=green,ls='--');axs[1].set_xlabel(tr('输入面积 / mm²','Entered area / mm²'));axs[1].set_ylabel(tr('表观模量 / MPa','Apparent modulus / MPa'));axs[1].set_title(tr('B  几何分母影响全部应力','B  Area scales every stress value'),loc='left');axs[2].scatter(np.arange(1,8),reps,color=blue,s=35);axs[2].axhline(reps.mean(),color=green);axs[2].axhspan(reps.mean()-reps.std(ddof=1),reps.mean()+reps.std(ddof=1),color=green,alpha=.12);axs[2].set_xlabel(tr('构造试样编号','Constructed specimen number'));axs[2].set_ylabel(tr('模量 / MPa','Modulus / MPa'));axs[2].set_title(tr('C  独立试样：均值±样本标准差','C  Specimens: mean ± sample SD'),loc='left',fontsize=10);fig.tight_layout();save(fig,'sensitivity')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

处理原始表格时，应同时检查缺测值与采集状态。光学标记丢失后，有的软件可能输出空值，有的可能重复上一帧，还有的可能写入零；它们的含义与真实应变归零完全不同。先根据状态字段或图像识别无效测量，再决定是否在允许范围内插值，并保留被排除的位置。断裂附近的信号本来就可能不连续，跨越断裂点插值会制造一段并不存在的承载过程。让每个处理动作对应已知的采集现象，能够保持曲线与实验事件的一致。

把程序用于实际记录时，应先接入真实尺寸、时间和信号通道，再按适用的材料测试方法选择区间与结果定义。保留原始数据后，可以在新的尺寸测量或同步信息出现时重新计算，而不必重新猜测曲线从哪里来。拉伸实验最终交付的应是一个有条件的材料描述：在什么方向、环境、速度和测量定义下，试样怎样变形、承载并失效。这样的记录能够支持材料比较，也为下一步研究压缩承载、裂纹扩展和长期力学行为提供可靠起点。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Hooke — Potentia Restitutiva, or Spring (historical text)](https://doi.org/10.1190/1.9781560801931.ch3a)

   原文的负载与螺旋弹簧伸长实验。

   Historical text excerpt consulted through publisher index; no image reused.
2. [MacTutor — Robert Hooke](https://mathshistory.st-andrews.ac.uk/Biographies/Hooke/)

   1678年公开弹性关系及计时装置背景。

   Historical reference; no image reused.
3. [Instron — Tensile testing](https://www.instron.com/en/resources/test-types/tensile-test/)

   装夹、引伸、模量和强度的测量。
4. [Instron — Extensometers](https://www.instron.com/en/products/testing-accessories/extensometers/)

   标距与系统柔度、接触和非接触测量。
5. [Instron — Offset yield strength](https://www.instron.com/en/resources/glossary/offset-yield-strength/)

   偏移量、交点与弹性极限的区别。
6. [DoITPoMS — True and nominal stresses and strains](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.3:_True_and_Nominal_Stresses_and_Strains)

   面积与长度的不同应力应变定义。

   CC BY-NC-SA source consulted; no text or figures adapted.
7. [DoITPoMS — Tensile testing, necking and failure](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.6:_Tensile_Testing_-_Necking_and_Failure)

   均匀变形、颈缩和局部测量。

   CC BY-NC-SA source consulted; no text or figures adapted.
8. [Lord and Morrell — Elastic modulus measurement (2010)](https://doi.org/10.1088/0026-1394/47/2/s05)

   原始研究摘要中的应变、对中、分析与不确定度问题。

   Publisher abstract consulted; no figures reused.
