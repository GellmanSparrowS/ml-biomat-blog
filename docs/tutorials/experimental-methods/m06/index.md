# 蠕变实验：恒定载荷下缓慢发生的变形

Source: https://ml-biomat.com/tutorials/experimental-methods/m06/
Language: zh-CN

从软垫的缓慢下陷出发，认识柔量、延迟恢复和黏性流动，用完整的加载—卸载记录检验材料模型。

## 一块软材料，为什么越压越扁

把一本厚书放在软垫上，软垫会立刻下陷，过一会儿还可能继续变薄。书没有变重，为什么形状还在改变？类似的问题出现在承重水凝胶、黏合剂接头、聚合物管道和组织支架中：材料刚接触载荷时表现得合适，并不意味着几个小时以后仍保持同样的形状。蠕变实验把这个日常现象变成一个明确的问题：在规定的温度、含水状态和近似恒定的应力下，材料的变形怎样随时间发展？它最有用的地方，是把“有多软”进一步拆成“立即有多软”“随后变化多快”和“卸载以后能恢复多少”。

这里的“恒定”需要说清楚。挂上一枚砝码，通常保持的是力；应力还取决于受力面积。在小变形拉伸实验中，常用初始横截面积把力换成工程应力，此时恒力对应恒定工程应力。若试样明显变细，当前截面上的真实应力会增加，实验就不再等同于恒定真实应力。压缩中的面积变化、鼓肚以及板间摩擦也有类似影响。初学时先把变形控制在经过验证的线性范围，再研究较大的变形，能够把时间效应与几何效应分开理解。

还可以把同一块软垫固定在某个压缩厚度上，观察支撑力慢慢下降。这是应力松弛，控制的是变形，观察的是力；蠕变则控制应力，观察变形。两种实验像对同一个人提出两个不同问题，得到的信息可以互相补充，却不能把一条曲线逐点取倒数就变成另一条。理解仪器究竟控制了什么，是读懂任何黏弹性曲线的第一步。本篇采用拉伸符号说明计算，剪切蠕变只需换成相应的剪切应力、剪切应变和剪切柔量，测量几何仍须保持一致。

![恒力蠕变的测量链与弹簧—阻尼器语言。左图标出力控制、标距和载荷传感器，右图把立即弹性、延迟恢复与流动串联。下方历史线索说明这些响应模型如何进入共同的流变学语言；图为原创概念示意。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2ea9da1ceeb456f915d8ad07.svg?v=2ea9da1ceeb4)

图 1恒力蠕变的测量链与弹簧—阻尼器语言。左图标出力控制、标距和载荷传感器，右图把立即弹性、延迟恢复与流动串联。下方历史线索说明这些响应模型如何进入共同的流变学语言；图为原创概念示意。

## 弹簧、阻尼器与材料中的等待时间

一根理想弹簧受到力就立即伸长，撤去力就回到原位；一个装着黏性液体的活塞则需要时间移动，持续受力时会继续前进。把它们画在一起，是研究时间依赖材料的一种语言。十九世纪建立起来的弹性与黏性力学，为后来 Maxwell、Kelvin 型模型提供了基础；到了 1929 年流变学会成立，橡胶、沥青、油漆和生物材料中的这些现象逐渐有了共同的交流方式。图中的弹簧和阻尼器是对响应规律的示意，不是在声称高分子内部真的装着金属零件。

在实际聚合物里，链段转动、链间接触重新安排、可逆结合点打开又闭合，都可能需要一定时间。水凝胶还多了一条途径：水在网络内部移动，甚至从样品中排出。想象一群人共同拖动一张网，绳子能立刻绷紧，但拥挤的人群调整站位需要更久；如果网里还装着水，水的流动又增加一段等待。这个比喻帮助我们理解不同时间过程的叠加。究竟由哪一种过程控制实验，需要结合样品尺寸、温度、溶剂条件和其他表征判断，单条蠕变曲线首先给出的是宏观时间响应。

最简单的延迟恢复单元，是把弹簧与阻尼器并联，使它们具有相同的伸长。加载刚开始时，阻尼器阻碍快速运动；随着活塞移动，弹簧逐渐承担更多载荷，伸长逼近一个上限。把这个单元与另一个弹簧串联，就能同时表示立即变形和随后发生的可恢复变形；再串联一个能持续滑动的阻尼器，就加入了长时间流动。串联部件承受同一应力，总变形等于各部分变形之和，因此后面的柔量表达式是三种响应相加，而不是凭空拼出的一串项。

不同材料可能需要多个延迟单元，因为松动的链段、缠结和结合点具有不同时间尺度。增加单元之前，应先问实验记录能否区分它们。如果一场实验只持续一分钟，就很难分别辨认两个都需要数小时才能显现的过程；如果仪器加载用了五秒，也难以从这段记录确定十分之一秒的响应。模型的复杂程度应由时间窗口和数据质量支持。先学会解释一个延迟单元，再理解一组延迟时间，会比直接面对几十个拟合参数更清楚。

## 从力和长度出发，得到可以比较的柔量

蠕变仪或具有力控制能力的力学试验机，主要记录载荷、位移和时间。试样初始长度决定同样一毫米伸长对应多大变形，初始横截面积决定同样一牛顿力分摊到多大区域，所以比较材料以前必须先做几何归一化。一个初始长度为 20 mm、横截面积为 10 mm² 的试样，受到 0.005 N 拉力时，工程应力是 500 Pa；若它伸长 0.40 mm，工程应变就是 0.020，也就是 2%。这里 10 mm² 要换算成 0.000010 m²，面积单位中的平方很容易在手算时漏掉。

$$
\sigma_0=\frac{F}{A_0},\qquad \varepsilon(t)=\frac{L(t)-L_0}{L_0},\qquad J(t)=\frac{\varepsilon(t)}{\sigma_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 恒定工程应力，单位 Pa；下标 0 表示施加的应力水平。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 拉力，单位 N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 初始横截面积，单位 m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 时间 t 的工程应变，无量纲；乘 100 后以百分数显示。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4310de27232c5927c847a9aa.svg) | 时间 t 的标距长度，单位 m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | 初始标距长度，单位 m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从加载开始计算的时间，单位 s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78711ccf7196ae9599387d2a.svg) | 线性范围内的蠕变柔量，单位 Pa⁻¹。 |

力除以面积得到单位面积承受的力；伸长除以初始长度得到相对伸长。0.005 N / 0.000010 m² = 500 Pa；0.40 mm / 20 mm = 0.020；因此柔量为 0.020 / 500 = 0.000040 Pa⁻¹。

柔量的名字可以理解为“单位应力能引起多少变形”。同样 500 Pa 的载荷下，一个试样在 60 秒时的应变是 0.02，另一个是 0.04，它们此时的柔量分别为 0.000040 Pa⁻¹ 和 0.000080 Pa⁻¹，后者更容易变形。柔量具有应力倒数的单位，却不应在一般黏弹性过程中被当作松弛模量的逐点倒数。两种测量施加的历史不同；只有纯弹性等特定情形，简单倒数关系才直接成立。

阅读图轴时，还要分清百分数与百分点。应变从 1% 增加到 2%，是增加了 1 个百分点，同时也是相对原值增加 100%。残差图使用百分点，是为了直接表示预测曲线与观测点之间的纵向距离；柔量计算则始终使用 0.01、0.02 这样的无量纲应变。把这两个写法在数据表、公式和图注中保持一致，可以避免把本来只有百分之一的变形误输入成一整倍的伸长。这种量纲检查在柔软样品的小变形测量中尤其有用。

判断线性范围的方法很直观：在同样的环境和等待时间下，用几个不同的小应力分别测量，把各条应变曲线除以各自应力。如果得到的柔量曲线在实验波动内重合，说明这一范围内“载荷加倍，变形加倍”的假设可用。若曲线随应力系统性改变，可能出现非线性结构调整，也可能是夹具滑动、接触条件变化或损伤。应力越大信号越清楚，但也越可能改变材料本身；选择载荷就是在分辨率与实验目标之间做有依据的权衡。

试样制备同样进入计算。水凝胶要说明平衡液、温度、浸泡时间和测量时是否浸液，因为表面失水会让长时间曲线混入浓缩效应；薄膜要记录裁切方向和厚度分布，因为取向与厚度误差会改变应力换算。几何尺寸宜在多个位置测量。夹具之间的移动还可能包含机器框架的弹性变形，所以有条件时优先记录试样标距内的位移。用刚性参照样品评估系统柔量，可以判断一开始的快速位移有多少来自仪器本身。

加载前还需要建立一个可重复的起点。试样刚放进夹具时可能存在松弛、接触不完全或装夹产生的预应变，仪器显示的零位并不自动等于材料的无载状态。可以采用经过记录的微小预载建立接触，再等待位移变化减缓，并把这个预载及等待时间写进实验条件。随后施加目标载荷时，同时保存力和位移通道；在力曲线上确认上升时间、超调与稳定程度，才能判断应变曲线最初的弯折是材料响应还是控制器追赶目标值造成的。如果预载已经引起明显蠕变，应把这段载荷历史纳入分析。

## 一条曲线中的立即变形、延迟变形和流动

下面用一个包含三种贡献的线性模型贯通实验。第一项是加载瞬间出现的柔量，第二项随时间逐渐增长并逼近上限，第三项以固定斜率持续增加。指数函数可以把它理解成“尚未完成调整的那部分”：每经过同样一段时间，剩余部分按固定比例减少，所以开始变化快，后来逐渐放慢。参数 τ 称为延迟时间；时间达到 τ 时，延迟部分完成约 63.2%，达到三倍 τ 时完成约 95.0%。它表示一个时间尺度，既不是所有变化结束的时刻，也不是材料必然发生损伤的时间。

$$
J(t)=J_0+J_1\!\left(1-e^{-t/\tau}\right)+\frac{t}{\eta_0},\qquad \varepsilon(t)=\sigma_0J(t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/78711ccf7196ae9599387d2a.svg) | 加载阶跃后的蠕变柔量，Pa⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a994f358d07ca2f1e8d481af.svg) | 立即柔量，Pa⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/56837856c14a72566e349ad4.svg) | 延迟恢复单元最终增加的柔量，Pa⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 加载后的时间，s；此式取 t≥0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 延迟时间，s；等于该并联单元的黏度除以弹性模量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | 串联流动阻尼器的终端黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数函数的底，约 2.71828，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 恒定工程应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 工程应变，无量纲。 |

串联元件受相同应力，变形相加；指数中的 t/τ 必须无量纲。取 J₀=0.000020 Pa⁻¹、J₁=0.000040 Pa⁻¹、τ=40 s、η₀=20000000 Pa·s，在 500 Pa 应力和 180 s 保持时间下，卸载前应变约 0.034278，即 3.428%。

教学例子取立即柔量 0.000020 Pa⁻¹、延迟柔量 0.000040 Pa⁻¹、延迟时间 40 s、终端黏度 20000000 Pa·s。在 500 Pa 的应力下，加载瞬间的应变为 1.00%；保持 180 s，到卸载前应变约为 3.428%。这时，立即部分贡献 1.00 个百分点，延迟部分贡献约 1.978 个百分点，流动贡献 0.450 个百分点。把总量拆开以后，就能看出同样一条上升曲线里，既有能够恢复的变形，也有模型中会留下的永久变形。

末段曲线还在上升，并不自动说明发生了稳定流动。如果延迟时间远大于观察时间，指数项在眼前的小窗口里也近似直线，容易与黏性流动混淆。延长保持时间、增加卸载恢复段，或改变温度和样品尺寸，都能提供额外信息。反过来，末段近似水平也只是说明在当前时间窗口内增长较慢；长期服役预测需要与目标时间相匹配的实验依据。这里把“长期”落实为明确时间范围，比给材料贴一个笼统的耐久标签更有帮助。

![同一组参数生成的组成图与完整蠕变—恢复曲线。面积图中的三部分相加为卸载前总应变；180 s 卸载后先立即回弹，再逐渐接近 0.450% 的模型残余。数据为教学构造，采用 500 Pa 工程应力。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/206ddb9b2eb0f789b7fef2fc.svg?v=206ddb9b2eb0)

图 2同一组参数生成的组成图与完整蠕变—恢复曲线。面积图中的三部分相加为卸载前总应变；180 s 卸载后先立即回弹，再逐渐接近 0.450% 的模型残余。数据为教学构造，采用 500 Pa 工程应力。

拟合时采用正参数，是为了让弹性贡献、黏度和时间尺度保持物理意义。程序实际拟合参数的对数，再转换回原单位，能减少不同数量级给数值优化带来的困难。最小二乘会寻找让预测值与观测值之差整体较小的参数，但一组漂亮的重合曲线并不告诉我们每个参数都被可靠确定。若两个参数可以互相补偿，拟合曲线几乎不变，它们各自的估计仍可能波动很大；因此还要查看残差、误差尺度以及更换拟合时间窗口后参数的变化。

参数单位也能帮助检查模型。柔量若用 kPa⁻¹ 表示，数值会是用 Pa⁻¹ 表示时的一千倍；例如 0.000040 Pa⁻¹ 等于 0.040 kPa⁻¹，因为相同应变除以更小数值的应力，得到的柔量数值更大。终端黏度则是应力乘时间，Pa·s 与 Pa/s 描述的不是同一个量。把全部输入先转换到一套单位，再只在绘图时选择便于阅读的刻度，能避免拟合程序顺利运行、参数却相差千倍的情况。检查表达式中每一项能否相加，也是理解公式含义的一种有效方法。

## 卸下载荷，观察材料留下了什么

恢复段像一次追问：刚才增长的变形，有多少只是暂时的？在线性叠加的条件下，在某时刻卸去原有载荷，相当于在那里又施加一个大小相同、方向相反的应力阶跃。前一次加载仍有自己的历史，后一次负阶跃开始抵消它，所以恢复响应由两个不同起点的柔量相减得到。这个思路不需要先学复杂微积分，只要记住“每次载荷变化都有自己的时钟”；若实验中有多个加载台阶，就逐个计算，再把贡献相加。

$$
\varepsilon(t)=\sigma_0\!\left[J(t)-J(t-t_h)\right]\quad(t\geq t_h),\qquad \varepsilon_{\mathrm{res},\infty}=\frac{\sigma_0t_h}{\eta_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 卸载后的工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 卸载前恒定工程应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | 上一式定义的蠕变柔量函数，Pa⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从最初加载算起的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/87a9fd0f547cfac0b56c2382.svg) | 保持时间，也是卸载时刻，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | 终端黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6b812d82bdc604fb38d896f1.svg) | 模型中充分恢复后的残余应变，无量纲；∞表示时间趋于无限长。 |

卸载相当于增加一个负应力阶跃，在线性叠加条件下减去它的响应。500 Pa 保持 180 s、终端黏度为 20000000 Pa·s 时，长期残余为 500×180/20000000=0.0045，即 0.450%。在卸载瞬间立即弹性部分回退，延迟部分随后继续恢复。

在本例 180 s 卸载时，立即弹性变形先回退 1.00 个百分点，随后延迟部分逐渐恢复。足够长时间后，模型留下的应变为 0.450%，来自串联流动阻尼器在保持期间积累的位移。若把保持时间增加一倍而参数不变，这部分残余也增加一倍。相反，如果模型没有流动项，延迟恢复最终会回到零。实际测量中的“残余应变”总是在某个恢复时刻读出，报告 240 s 恢复后的值与报告拟合外推的无限长时间极限，是两个不同但都可以明确表达的量。

对含水材料，恢复缓慢还可能来自水的重新进入。把厚度增加一倍，如果恢复时间大约增加到四倍，就值得检验是否存在以距离平方为尺度的扩散或孔弹性过程；这个比例是寻找机制的线索，要与排水边界和材料结构一起分析。夹具滑移会留下另一种残余，通常可通过标记点相对移动、重复加载或不同夹持条件识别。观察恢复段的价值正在这里：它让相同外观的加载曲线拥有了更多可以区分的后续行为。

“没有完全恢复”也要与“结构受损”分开理解。某些材料在正常使用时就允许链段滑动或结合点重新形成，因此形成稳定的新形状；另一些样品则可能出现裂纹、界面脱黏或网络断裂。它们都能留下残余变形，但后续承载能力不同。可以在恢复后再次施加同样的小载荷，比较第二次的立即柔量和整条响应，并结合显微观察或质量变化判断发生了什么。这样的复测把残余形状与结构变化联系起来，比只用一个末端读数给材料判定“好”或“坏”更具体。

## 交互实验：改变加载历史，看恢复如何变化

拖动三个滑块，观察峰值、卸载回弹和长期残余。参数对应本篇线性教学模型；纵轴为应变百分数。

[Figure: 蠕变与恢复曲线](https://ml-biomat.com/tutorials/experimental-methods/m06/#M06-plot)

交互实验把应力、保持时间和延迟时间分开调整。先固定材料参数把应力加倍，观察峰值与残余应变是否一起加倍；再固定应力延长保持时间，观察延迟部分如何趋近饱和，而流动残余继续积累。最后改变延迟时间，比较恢复曲线的快慢。图中只演示所列线性模型，应力范围内的线性是否适用于某种真实样品，要由前面介绍的多载荷实验判断。这样，交互结果对应的是一个可以计算、可以检验的假设。

## 从原始记录拟合参数，也保留诊断信息

完整示例先构造已知参数的蠕变—恢复数据，再加入固定随机种子的测量噪声，目的是让读者能够逐项核对计算。数据文件保留时间、应力、理论应变和含噪声应变，曲线中的点因此有明确来源。拟合只使用加载段，恢复段作为随后预测：如果一个模型需要看完所有数据才能描出所有曲线，读者很难分清它是在记住已有形状，还是抓住了能够延伸到新加载历史的关系。这里的分段设计给了这个区别一个具体例子。

程序同时画出拟合曲线和残差。残差就是观测应变减去预测应变；如果它们围绕零无规则波动，说明模型在当前噪声水平下描述了主要形状。若残差在早期连续为正、随后连续为负，可能遗漏了第二个时间过程，也可能把有限加载斜坡当作瞬间阶跃。记录仪器实际达到目标力的时间，可以把这两类原因分开。对于加载速度较慢的设备，可把实际应力历史分成许多小台阶，用同样的叠加原理计算响应，而不是删除早期数据后假装加载是瞬间完成的。

![加载段用于拟合，恢复段由拟合参数预测。下图残差是观测值减预测值，阴影为设定噪声标准差的两倍范围，单位为应变百分点。所有观测点由给定模型加固定随机噪声构造。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b12cdd1f36f8bde26505d914.svg?v=b12cdd1f36f8)

图 3加载段用于拟合，恢复段由拟合参数预测。下图残差是观测值减预测值，阴影为设定噪声标准差的两倍范围，单位为应变百分点。所有观测点由给定模型加固定随机噪声构造。

拟合参数的不确定性与输入误差不是一回事。程序的局部参数标准误来自曲线拟合附近的灵敏度和设定噪声，它描述这个模型、这个时间窗口下的统计波动；若样品厚度整体量错 10%，应力与柔量都会受到系统影响，单靠增加采样点不会消除。重复测试不同试样可以观察材料与制备差异，重复分析同一条曲线则主要检查计算稳定性。把这两种重复放在不同层次处理，能避免把大量时间点误当作大量独立样品。

采样节奏会改变我们看到的细节。加载和卸载附近变化最快，宜保留足够密的原始记录；稳定保持的后段可以在展示时适度抽稀，同时保留完整数据。若仪器内部平滑了信号，相邻点的误差往往相关，不能简单按独立白噪声估计置信区间。示例中的噪声是明确构造的独立噪声，因此局部标准误具有相应的教学含义；真实实验可通过空载记录、稳定段或重复试样评估更合适的误差结构。平滑曲线可以帮助观看，原始点和处理规则仍是判断时间响应的依据。

### 完整示例：从蠕变记录预测恢复

程序使用统一的 SI 单位，导出含噪声构造数据、拟合参数、数值检查量和四张图。仅用加载段拟合，在恢复段检查预测。

```
"""Creep and recovery: a reproducible constructed experiment in SI units."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.optimize import curve_fit


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def compliance(t, j0, j1, tau, eta):
    t = np.asarray(t, dtype=float)
    return j0 + j1 * (-np.expm1(-t / tau)) + t / eta


def response(t, stress, hold, pars):
    """Right-continuous response: a negative stress step begins at hold."""
    t = np.asarray(t, dtype=float)
    result = stress * compliance(t, *pars)
    unload = t >= hold
    result[unload] -= stress * compliance(t[unload] - hold, *pars)
    return result


def fit_loading(t, strain, stress, noise):
    def model(times, *log_parameters):
        return stress * compliance(times, *np.exp(log_parameters))
    logs, covariance = curve_fit(
        model, t, strain, p0=np.log([2e-5, 4e-5, 40, 2e7]),
        sigma=np.full(t.size, noise), absolute_sigma=True,
        bounds=(np.log([1e-7, 1e-7, 0.5, 1e5]),
                np.log([1e-2, 1e-2, 2e4, 1e11])), maxfev=20000)
    parameters = np.exp(logs)
    standard_error = parameters * np.sqrt(np.diag(covariance))
    return parameters, standard_error


def setup(language):
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    cjk = next((n for n in ['Microsoft YaHei', 'Noto Sans CJK SC', 'SimHei'] if n in names), 'DejaVu Sans')
    plt.rcParams.update({'font.family': cjk if language == 'zh' else 'DejaVu Sans',
        'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': '#213342', 'text.color': '#213342',
        'axes.prop_cycle': plt.cycler(color=['#176c83', '#d4813d', '#7d5ea4', '#3c8a6a']),
        'svg.fonttype': 'none', 'figure.facecolor': '#faf9f5',
        'axes.facecolor': '#faf9f5', 'savefig.facecolor': '#faf9f5',
        'axes.unicode_minus': False})
    return lambda zh, en: zh if language == 'zh' else _label(en)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    tr = setup(language)
    seed, stress, hold, noise = 604, 500., 180., 0.0001
    parameters = np.array([2e-5, 4e-5, 40., 2e7])
    times = np.r_[np.linspace(0, hold, 121, endpoint=False), np.linspace(hold, 420, 121)]
    truth = response(times, stress, hold, parameters)
    observed = truth + np.random.default_rng(seed).normal(0, noise, times.size)
    loading = times < hold
    fitted, errors = fit_loading(times[loading], observed[loading], stress, noise)
    predicted = response(times, stress, hold, fitted)
    residual = observed - predicted
    np.savetxt(output / 'data.csv', np.c_[times, np.where(loading, stress, 0), truth, observed],
        delimiter=',', header='time_s,stress_Pa,theoretical_strain,observed_strain', comments='')
    peak = float(stress * compliance(hold, *parameters))
    summary = {'data_kind': 'constructed teaching experiment', 'seed': seed,
        'instantaneous_strain': float(stress*parameters[0]),
        'peak_strain_before_unload': peak,
        'permanent_strain': float(stress*hold/parameters[3]),
        'retardation_fraction_at_tau': float(1-np.exp(-1)),
        'fitted': dict(zip(['j0_Pa_inverse','j1_Pa_inverse','tau_s','eta_Pa_s'], map(float,fitted))),
        'local_standard_errors': dict(zip(['j0_Pa_inverse','j1_Pa_inverse','tau_s','eta_Pa_s'], map(float,errors))),
        'recovery_rmse_strain': float(np.sqrt(np.mean(residual[~loading]**2)))}
    (output/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf8')

    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        plt.close(fig)

    # Original conceptual drawing: history and mechanical response share symbols.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained', gridspec_kw={'width_ratios':[1.05,1.25]})
    a, b = axes
    for ax in axes: ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a.set_title(tr('A  从恒力到长度变化','A  Constant force, changing length'),loc='left',fontweight='bold')
    a.add_patch(Rectangle((2,8),4,.45,color='#7b8990'))
    a.add_patch(Rectangle((3.25,3.5),1.5,4.5,facecolor='#b9d7d9',edgecolor='#176c83',lw=2))
    a.add_patch(Rectangle((2.5,2.8),3,.6,color='#7b8990'))
    a.add_patch(FancyArrowPatch((4,2.7),(4,.7),arrowstyle='-|>',mutation_scale=19,lw=2,color='#d4813d'))
    a.annotate(tr('固定端','Fixed grip'),(6.1,8.2),fontsize=11)
    a.annotate(tr('试样标距','Gauge length'),(5.2,5.8),fontsize=11)
    a.annotate(tr('载荷传感器','Load cell'),(5.8,3.0),fontsize=11)
    a.text(4,.3,tr('控制力，记录伸长与时间','Control force; record extension and time'),ha='center',fontsize=10)
    b.set_title(tr('B  三种响应的机械语言','B  A mechanical language for three responses'),loc='left',fontweight='bold')
    def spring(x1,x2,y,color):
        xs=np.linspace(x1,x2,17);ys=np.full(17,y);ys[1:-1]=y+np.tile([.35,-.35],8)[:15]
        b.plot(xs,ys,color=color,lw=2)
    def dashpot(x1,x2,y,color):
        b.plot([x1,x1+.6],[y,y],color=color,lw=2)
        b.plot([x1+.6,x1+.6,x2-.5,x2-.5],[y+.4,y-.4,y-.4,y+.4],color=color,lw=2)
        b.plot([x1+1,x1+1],[y-.3,y+.3],color=color,lw=2)
        b.plot([x1+1,x2],[y,y],color=color,lw=2)
    spring(.3,2.3,6.8,'#176c83'); b.text(1.3,8,tr('立即弹性','Immediate elasticity'),ha='center')
    b.plot([2.3,3,3],[6.8,6.8,7.8],color='#213342'); b.plot([3,3],[6.8,5.8],color='#213342')
    spring(3,5.3,7.8,'#7d5ea4');dashpot(3,5.3,5.8,'#7d5ea4')
    b.plot([5.3,5.3,6],[7.8,6.8,6.8],color='#213342');b.plot([5.3,5.3],[5.8,6.8],color='#213342')
    dashpot(6,8.5,6.8,'#d4813d')
    b.text(4.2,9.1,tr('延迟恢复','Delayed recovery'),ha='center');b.text(7.3,8,tr('持续流动','Ongoing flow'),ha='center')
    b.text(.4,3.6,tr('十九世纪：弹性与黏性模型','19th century: elastic and viscous models'),fontsize=11)
    b.annotate('',(8.7,2.7),(.4,2.7),arrowprops={'arrowstyle':'->','color':'#7b8990'})
    b.text(.4,1.7,tr('1929：流变学会成立','1929: Society of Rheology founded'),fontsize=11)
    b.text(.4,.45,tr('原创概念示意；串联单元的变形相加','Original conceptual diagram; series deformations add'),fontsize=9,color='#62747d')
    save(fig,'mechanism')

    fig, axs = plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    t=np.linspace(0,hold,301)
    components=[np.full_like(t,stress*parameters[0]*100),stress*parameters[1]*(-np.expm1(-t/parameters[2]))*100,stress*t/parameters[3]*100]
    labels=[tr('立即弹性','Immediate elastic'),tr('延迟恢复部分','Delayed recoverable'),tr('黏性流动','Viscous flow')]
    axs[0].stackplot(t,*components,labels=labels,alpha=.7)
    axs[0].set(xlabel=tr('加载时间 / s','Loading time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('A  卸载前的三部分贡献','A  Three contributions before unloading'))
    axs[0].legend(frameon=False,fontsize=9,loc='upper left')
    axs[1].plot(times,truth*100,lw=2.5);axs[1].axvline(hold,color='#777',ls=':',lw=1)
    axs[1].axhline(summary['permanent_strain']*100,color='#d4813d',ls='--',label=tr('长期残余 0.450%','Long-time residual 0.450%'))
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('B  蠕变与卸载恢复','B  Creep and recovery'))
    axs[1].legend(frameon=False,fontsize=9); save(fig,'components')

    fig,axs=plt.subplots(2,1,figsize=(11,6.3),layout='constrained',sharex=True,gridspec_kw={'height_ratios':[2,1]})
    axs[0].scatter(times[::3],observed[::3]*100,s=13,color='#899b9e',label=tr('构造观测值','Constructed observations'))
    axs[0].plot(times[loading],predicted[loading]*100,color='#176c83',lw=2,label=tr('加载段拟合','Fit to loading'))
    axs[0].plot(times[~loading],predicted[~loading]*100,color='#d4813d',lw=2,label=tr('恢复段预测','Predicted recovery'))
    axs[0].set(ylabel=tr('应变 / %','Strain / %'),title=tr('A  用加载段预测恢复段','A  Predict recovery from the loading fit'))
    axs[0].legend(frameon=False,ncols=3,fontsize=9)
    axs[1].axhspan(-noise*200,noise*200,color='#176c83',alpha=.1,label=tr('±2 倍设定噪声标准差','±2 prescribed noise standard deviations'))
    axs[1].axhline(0,color='#738087',lw=1);axs[1].scatter(times,residual*100,s=10,color='#176c83')
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('残差 / 百分点','Residual / percentage points'))
    axs[1].legend(frameon=False,fontsize=9); save(fig,'diagnostics')

    fig,axs=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    for st in [250,500,750]:
        axs[0].plot(t,st*compliance(t,*parameters)*100,lw=2,label=f'{st} Pa')
    axs[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('A  线性模型中的载荷比例','A  Stress proportionality in the linear model'));axs[0].legend(frameon=False)
    for tau,col in [(20,'#176c83'),(40,'#d4813d'),(80,'#7d5ea4')]:
        p=parameters.copy();p[2]=tau;axs[1].plot(times,response(times,stress,hold,p)*100,lw=2,color=col,label=f'τ = {tau} s')
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('B  改变时间尺度，残余极限相同','B  Different retardation times, same residual limit'));axs[1].legend(frameon=False)
    save(fig,'design')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

运行后先打开数据表，确认时间单位是秒、应力单位是帕、应变是无量纲数值；绘图时乘以 100 才显示百分数。接着检查 summary.json 中的立即应变、卸载前应变和长期残余是否与手算一致，再查看拟合得到的时间尺度是否接近构造值。最后改变噪声、缩短保持段或移除恢复段，比较参数的稳定性。完成这一轮以后，把构造数据换成仪器导出的真实记录就有了清楚的接口：保留时间和载荷历史，统一单位，再选择与测量几何一致的模型。

## 让实验回答真正关心的使用问题

如果目标是组织支架在轻微持续载荷下保持孔隙结构，首先关心的可能是几小时内的变形以及卸载后的恢复；如果目标是压敏胶在接头中抵抗滑动，就要关注保持时间内的位移积累和应力依赖；如果目标是软材料长期密封，还应把温度循环、环境介质和重复加载接进实验设计。相同的蠕变仪可以服务于这些问题，但“测试到多少秒”“选多大载荷”“记录哪一个形状指标”应由用途决定。曲线的横轴和纵轴因此也是实验问题的具体表达。

温度常常显著改变分子运动速度。时间—温度叠加尝试把不同温度的曲线沿时间轴平移，拼成更宽的观察窗口；前提是主要过程随着温度按相容的方式改变，而材料没有在测试中结晶、相分离、失水或发生其他结构转变。应先观察不同曲线形状是否相容，再讨论平移因子。将高温短时数据直接称作常温多年寿命，会跳过中间的物理检验。更完整的做法，是在重叠时间范围核对预测，再逐步扩大可用范围。

还可以从使用要求反推一个可检查的判据。假设某个接头在给定载荷保持 180 s 后，允许的工程应变为 4%，本例模型预测的 3.428% 满足这个特定形变要求；若卸载充分恢复后允许的残余只有 0.2%，预测的 0.450% 就提示需要提高终端黏度、缩短持续受力时间或调整结构。这里两个判据考察的是不同性能，优化一个并不保证另一个同步改善。明确判据后，实验结果自然变成设计选择的依据，而不是在许多曲线中寻找一个看起来最平缓的样品。

![改变载荷与改变时间尺度具有不同后果。左图在同一线性模型中应力与应变成比例；右图只改变延迟时间，恢复速度改变，但相同应力、保持时间和终端黏度给出同一长期残余。教学模型曲线。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ee2eb899787e282ae36f3fc1.svg?v=ee2eb899787e)

图 4改变载荷与改变时间尺度具有不同后果。左图在同一线性模型中应力与应变成比例；右图只改变延迟时间，恢复速度改变，但相同应力、保持时间和终端黏度给出同一长期残余。教学模型曲线。

最后整理结果时，保留样品几何、环境、加载上升时间、保持与恢复时长、应力水平以及独立样品数，曲线旁给出清楚的单位和误差定义。报告某时刻的柔量、峰值应变、规定恢复时间后的残余，以及有明确依据的模型参数，读者就能把材料表现与使用条件对应起来。下一篇的动态力学分析会换一种提问方式：让材料反复受到小幅振动，用应力与应变的相位差辨认储能和耗能。两种方法都在研究材料怎样分配时间，只是使用了不同的加载语言。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [David Roylance — Linear Viscoelasticity](https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Mechanics_of_Materials_%28Roylance%29/05:_General_Stress_Analysis/5.04:_Linear_Viscoelasticity)

   弹性、黏性单元和加载历史的基础阅读。
2. [RepTate — Creep Theories](https://reptate.readthedocs.io/manual/Applications/Creep/Theory/theory.html)

   延迟模态、立即柔量和终端黏度的模型定义。
3. [RepTate — Tutorial Creep Application](https://reptate.readthedocs.io/manual/Applications/Creep/Tutorial/tutorialGUICreep.html)

   继续练习蠕变数据导入、视图和拟合。
4. [Society of Rheology — History](https://www.societyofrheology.org/history)

   流变学会成立与学科交流历史。

   Historical reference; original illustration.
5. [SciPy — curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   最小二乘、参数边界与协方差解释。
6. [RepTate — TTS Theories](https://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html)

   时间—温度叠加与平移因子的延伸阅读。
