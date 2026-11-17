# 动态力学分析：用振动读懂黏弹性

Source: https://ml-biomat.com/tutorials/experimental-methods/m07/
Language: zh-CN

让两条波形解释储能、损耗与相位，从夹具和幅值选择走到频率谱、回线能量及时间—温度叠加。

## 同一块橡胶，为什么慢慢按和快速振动时不一样

橡胶鞋底需要支撑体重，也需要在脚落地时耗散一部分机械能；减振垫要隔开机器的振动，同时保持足够的承载能力；柔软的组织支架则面对细胞牵拉和身体运动带来的不同时间尺度。这些用途都在问同一件事：材料受到反复变形时，有多少力用来维持弹性形状，又有多少与内部运动和能量耗散有关？动态力学分析，简称 DMA，通过施加幅度很小、节奏可以调节的振动来回答这个问题。它测量的不是一个脱离条件的“硬度值”，而是一组随频率、温度和状态变化的力学响应。

可以把振动想成反复推拉一扇装有弹簧和缓冲器的门。弹簧的阻力主要取决于门离开原位多远，缓冲器的阻力还取决于移动有多快。门经过中间位置时，离原位的距离很小，速度却可能最大；这让两种作用在一个周期中出现在不同的时刻。DMA 利用这个时间差，把应力分解为与应变同步的部分和与应变相差四分之一周期的部分。储能模量与损耗模量，就是对这两部分大小的描述，后面会从两条实际波形逐步算出它们。

振动实验并不要求样品肉眼可见地晃动。一个标距为 10 mm 的薄膜，应变幅值为 0.2% 时，位移幅值只有 0.020 mm，也就是 20 μm。仪器需要在这样小的位移下同时记录力、位移和它们的时间关系，因此装夹、尺寸测量和相位校准都很重要。相同的材料可以用拉伸、压缩、弯曲或剪切方式测试，得到的模量名称和几何换算也随之改变。本篇以小幅拉伸为主线，先弄清一种明确几何，再把思路迁移到其他夹具。

![从夹具到信号的原创概念图。薄膜拉伸与三点弯曲采用不同几何换算，仪器需要同时记录位移、力和时间关系。图中的弯曲形状用于说明受力方式，不是实测位移场。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5bb715d489b1f9fecb0e4682.svg?v=5bb715d489b1)

图 1从夹具到信号的原创概念图。薄膜拉伸与三点弯曲采用不同几何换算，仪器需要同时记录位移、力和时间关系。图中的弯曲形状用于说明受力方式，不是实测位移场。

## 夹具决定怎样变形，传感器决定看见什么

一台 DMA 通常包含施加周期力或位移的驱动部件、记录响应的传感器、夹具，以及控制温度或其他环境的腔体。薄膜和纤维适合拉伸夹具；较硬的条形材料可以采用三点弯曲或悬臂弯曲；柔软块体可用压缩或剪切夹具。选择的关键是让样品稳定地变形，并使力与位移落在仪器可信的量程内。把一个极软的水凝胶装进为硬塑料弯曲设计的夹具，即使软件给出了数字，也可能主要反映接触和夹持状态。

拉伸中的力除以截面积得到应力，位移除以标距得到应变。弯曲则需要考虑梁的长度、宽度和厚度，因为离中性面越远的材料承受越大的拉伸或压缩。常用梁模型中，弯曲刚度对厚度具有三次方依赖，因此厚度误差会被明显放大。试样略微翘曲、厚度不均或支点间距记录错误，都可能造成模量的系统偏移。测量之前在多个位置记录尺寸，比事后为曲线寻找复杂的分子解释更能直接解决这类问题。

拉伸薄膜常需要小的静态预载，避免周期中样品松弛或屈曲；压缩测试则需要建立稳定接触，同时避免预压已经使孔隙或网络发生大变化。预载和动态幅值是两个不同条件，不能用其中一个代替另一个。对水凝胶或组织，应把含水状态、浸液方式、温度和等待时间一起记录。温度扫描时，样品本身达到目标温度需要时间，炉温传感器的读数与样品内部温度可能短暂不同；升温越快、样品越厚，这个问题越值得关注。

正式扫描前，可以在选定温度和频率下逐渐改变振幅，寻找模量近似不随振幅变化的范围。这一范围称为线性黏弹区。幅度太小时，力或位移可能接近噪声；幅度太大时，网络重排、滑移、接触变化或损伤会改变响应。合适的测试幅度应位于可重复的平台内，并保留足够的信号。平台不是材料永久不变的标签，它可能随温度、频率和含水状态移动，所以条件变化较大时应重新检查。

仪器本身也有惯性、柔量和时间延迟。空夹具或参照材料的校准用于识别这些贡献，特别是在高频或样品很软时。若真实相位差很小，传感器之间的一点时间偏差就可能显著影响损耗模量。观察原始波形能帮助发现削顶、漂移和高次谐波：它们分别提示量程、基线或非线性问题。把原始信号与软件导出的模量一起保存，后续就能追溯某个异常点是怎样产生的，而不必只面对一个无法解释的最终数值。

可以在上机前估算信号大小。若截面积为 1 mm²，后面例子的应力幅值约为 14422 Pa，对应力幅值约为 0.0144 N；标距为 10 mm、应变幅值为 0.2% 时，对应位移幅值为 20 μm。拿这两个值与所用传感器的分辨率和量程比较，就能判断当前几何是否合适。增加截面积会增加力信号，增加标距会增加同样应变对应的位移，但也会改变装夹稳定性与温度均匀性，因此应结合实际夹具选择尺寸，而不是只追求更大的信号。

## 从两条正弦波读出储能与损耗

先用一个圆周运动理解正弦波。想象圆周上的一个点匀速转动，把它在竖直方向的位置记录下来，就得到上下往复的正弦曲线。一次完整转动对应一个周期，频率表示每秒完成多少周期，单位是 Hz；角频率表示每秒转过多少弧度，单位是 rad/s。一圈是 2π 弧度，所以两种频率之间要乘上 2π。程序中的三角函数使用弧度，不能把以度为单位的角度直接代入。

$$
\varepsilon(t)=\varepsilon_0\sin(\omega t),\qquad \omega=2\pi f,\qquad P=\frac{1}{f}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 时间 t 的工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 应变幅值，无量纲；0.2% 对应 0.002。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 频率，Hz，也就是每秒周期数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 一个完整周期的时长，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约 3.14159，无量纲。 |

正弦函数描述周期往复。角频率为 10 rad/s 时，频率为 10/(2π)≈1.592 Hz，周期约 0.6283 s。应变幅值为 0.002、初始标距 10 mm 时，位移幅值为 0.020 mm。

当应变按正弦规律变化时，线性黏弹材料在稳态下的应力也以同样频率变化，但峰值出现的时间不同。在这里选用的写法中，应力比应变提前一个相位角，等价地说，应变落后于应力。相位角是用一个周期作为尺子衡量的时间差：若应力峰值比应变峰值早四分之一周期，相位差就是 90°。两个信号同相时，响应类似理想弹簧；相差四分之一周期时，响应类似理想黏性元件。真实材料通常处于两者之间。

把提前相位的应力展开，就会得到一个与应变同步的正弦项，以及一个与应变变化速度同步的余弦项。正弦与余弦像两把方向互相垂直的尺子，可以分别测出两部分系数。第一部分除以应变幅值得到储能模量，第二部分除以应变幅值得到损耗模量。名称中一个撇和两个撇只是区分这两个量，不表示求导，也不代表第一次和第二次实验。这个分解是波形几何带来的结果，而不是软件任意设置的两个指标。

$$
\sigma(t)=\varepsilon_0\!\left[E^{\prime}\sin(\omega t)+E^{\prime\prime}\cos(\omega t)\right],\quad E^{\prime}=\frac{\sigma_0}{\varepsilon_0}\cos\delta,\quad E^{\prime\prime}=\frac{\sigma_0}{\varepsilon_0}\sin\delta,\quad \tan\delta=\frac{E^{\prime\prime}}{E^{\prime}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | 周期应力，Pa；在稳态小幅线性响应中使用。 |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 总应力幅值，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 应变幅值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | 拉伸储能模量，Pa；一个撇用于命名。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc2062badd373b0f0dcf4479.svg) | 拉伸损耗模量，Pa；两个撇用于命名。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 应力超前应变的相位角；三角函数使用 rad。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7cfe4f0d59119c3e45744c16.svg) | 损耗因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |

相位提前的正弦可以分解成同步正弦项和四分之一周期错开的余弦项。E′=6 MPa、E″=4 MPa 时，tanδ=2/3，δ≈33.69°；应变幅值为 0.002 时，总应力幅值约 14422 Pa。

例如储能模量为 6 MPa、损耗模量为 4 MPa、应变幅值为 0.002 时，应力中的同步分量幅值是 12000 Pa，余弦分量幅值是 8000 Pa。总应力幅值由两部分的平方和开方得到，约为 14422 Pa；它们在周期中并不同时达到最大，因此不能简单相加得到 20000 Pa。损耗因子为 4/6，约 0.667，相位角约为 33.69°。这组数字贯穿后面的波形、椭圆回线和能量计算，让每一种图都能与同一个实验对应。

![同一构造实验的应变与应力波形。应变幅值为 0.2%，角频率为 10 rad/s；应力波形包含固定种子的测量噪声与 120 Pa 基线偏移，拟合同时估计正弦、余弦与常数项。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d19e1e94b9f692d073a00991.svg?v=d19e1e94b9f6)

图 2同一构造实验的应变与应力波形。应变幅值为 0.2%，角频率为 10 rad/s；应力波形包含固定种子的测量噪声与 120 Pa 基线偏移，拟合同时估计正弦、余弦与常数项。

谈论某个模量时，需要保留测量方式。拉伸或适当条件下的压缩、弯曲通常报告 E′、E″，剪切报告 G′、G″。它们具有相同的应力单位，却描述不同的变形方式。只有在适用的连续介质假设和已知泊松比关系下，才能把拉伸模量与剪切模量换算。对强各向异性纤维、复杂多孔结构或非均匀组织，直接把一种几何的模量数值当成另一种几何的结果，会丢掉样品如何承受载荷的重要信息。

## 把时间轴折起来，看见一圈损失的能量

波形图把应变和应力分别画在时间轴上；还可以把同一时刻的应变作为横坐标、应力作为纵坐标，沿时间顺序连起来。纯弹性材料沿一条直线往返，加载时输入的能量在卸载时返回。黏弹材料通常形成一个椭圆，加载与卸载走不同的路线，围住的面积对应每周期、单位体积耗散的机械能。这个图常称为应力—应变 Lissajous 图，它把“两个信号错开了多少”转化成一个可以看见的面积。

面积为什么具有能量的含义？力乘移动距离是做功，而应力乘应变，相当于把这份功再除以试样体积。沿着一个周期把许多小段的应力与应变变化相乘并相加，就得到回线积分。这里应变应使用 0.002 这样的无量纲数，而不是图上写出的 0.2；若直接对百分数坐标积分，就会多出一百倍。应力单位为 Pa，所以每周期耗散能密度的单位也可写成 Pa，等价于 J/m³。

$$
W_{\mathrm{diss}}=\oint\sigma\,\mathrm{d}\varepsilon=\pi E^{\prime\prime}\varepsilon_0^2,\qquad W_{\mathrm{ref}}=\frac12 E^{\prime}\varepsilon_0^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/338bcad567736ca2de614709.svg) | 每周期耗散能密度，J/m³。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f028f6920f65d3c579388781.svg) | 沿一个完整应力—应变周期积分。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 瞬时应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/69d9e6d74063f2d3721f88c4.svg) | 工程应变的微小变化，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc2062badd373b0f0dcf4479.svg) | 损耗模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | 储能模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 应变幅值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ccced5783ddc69fc9d8592.svg) | 由储能模量定义的常用弹性能量尺度，J/m³。 |

公式用于小幅稳态正弦的线性响应。应力乘应变具有单位体积能量的量纲。E″=4000000 Pa、ε₀=0.002 时，耗散为 π×4000000×0.002²≈50.27 J/m³；E′=6000000 Pa 时，储能尺度为 12 J/m³。

对于前面的例子，损耗模量为 4000000 Pa，应变幅值为 0.002，每周期耗散能密度约为 50.27 J/m³。若在相同线性范围内把应变幅值增加一倍，模量不变，但耗散能增大到四倍，因为一周期中力和位移幅值都增加了。储能模量给出的常用弹性能量尺度为 12 J/m³；损耗因子比较的是模量之比，它并不等于“输入能量中损失了百分之多少”。把 0.667 直接写成损失 66.7% 的能量，会混淆不同的定义。

![左图的理论应力—应变回线围住每周期约 50.27 J/m³ 的耗散能密度，计算面积时应变必须使用无量纲数。右图将含噪声拟合残差按周期内相位排列；阴影为设定噪声标准差的两倍范围。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4958b14daee743e3d7a7c6d6.svg?v=4958b14daee7)

图 3左图的理论应力—应变回线围住每周期约 50.27 J/m³ 的耗散能密度，计算面积时应变必须使用无量纲数。右图将含噪声拟合残差按周期内相位排列；阴影为设定噪声标准差的两倍范围。

回线还能提供形状诊断。小幅稳态正弦加载下，线性响应产生椭圆；如果回线出现明显尖角、扁平边或不同周期不重合，应检查非线性、接触滑移、基线漂移和材料随时间改变的可能性。频率升高后，系统惯性也可能改变相位，所以要结合仪器校准判断。回线面积大，可以说明在当前幅值与频率下每周期耗散较多；选择减振材料时，还应同时考虑刚度、工作温度、变形幅度和允许的发热，不能只按一个损耗因子排序。

耗散还可以换成单位时间的能量输入。每周期耗散 50.27 J/m³、每秒振动约 1.592 次时，平均耗散功率密度约为 80 W/m³。这个计算只需要把每周期能量乘以每秒周期数，适用于稳态重复振动。它还不是样品温升，因为温度同时取决于热容量、导热以及周围环境带走热量的速度。持续振动时若样品自己升温，材料模量又可能随之改变，形成力学与热过程的相互影响。将测试温度稳定下来，能让不同频率的比较更接近同一材料状态。

## 换一种振动节奏，分子运动来不来得及

慢慢拉动材料时，许多内部运动有时间完成；快速反复拉动时，它们可能还没有调整好，载荷方向就已经改变。把外部振动的角频率乘以内在松弛时间，得到一个没有单位的数。这个数很小，表示内部过程相对快，能够跟上外部变化；这个数很大，表示过程相对慢，在每一周期中近似被冻结。用同一套材料参数扫过一系列频率，就像从不同时间窗口观察材料，能够把单次测试中混在一起的过程逐渐分开。

下面的教学模型由一个平衡弹簧与一个 Maxwell 支路并联组成。平衡弹簧始终提供低频刚度，Maxwell 支路中的弹簧和黏性元件在不同频率下分担响应。低频时，支路中的黏性运动有时间释放应力；高频时，支路更像额外的弹簧，因此储能模量从较低平台升向较高平台。损耗模量在中间频率附近出现峰值，因为这时外部节奏与内部调整时间相当。这是理解频率谱的一个清楚起点，真实聚合物往往包含多个这样的时间过程。

$$
E^{\prime}(\omega)=E_{\mathrm{eq}}+E_1\frac{(\omega\tau)^2}{1+(\omega\tau)^2},\qquad E^{\prime\prime}(\omega)=E_1\frac{\omega\tau}{1+(\omega\tau)^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6bcebecca57a8b130798178.svg) | 角频率 ω 下的储能模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e627d8d9ef684b3751f55a4f.svg) | 角频率 ω 下的损耗模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d8d43630c801e4462b1455e5.svg) | 平衡弹簧的模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4527c7825889bcd00202ef22.svg) | Maxwell 支路弹簧的模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 该 Maxwell 支路的松弛时间，s；此处不是蠕变延迟时间。 |

平衡弹簧与 Maxwell 支路并联，承担的应力相加。取 Eeq=2 MPa、E₁=8 MPa、τ=0.1 s、ω=10 rad/s，ωτ=1，得到 E′=6 MPa 和 E″=4 MPa。低频储能平台为 2 MPa，高频趋近 10 MPa。

取平衡模量 2 MPa、支路模量 8 MPa、松弛时间 0.1 s，当角频率为 10 rad/s 时，频率约为 1.592 Hz，无量纲乘积正好等于 1。这时支路对储能和损耗各贡献 4 MPa，加上平衡弹簧后得到 6 MPa 与 4 MPa，恰好是前面波形的数字。由此也能看出，损耗峰、两个模量相等的位置以及损耗因子峰，不一定是同一个频率。平衡弹簧改变了分母和平台，不能把所有峰都机械地解释成同一个松弛时间。

## 交互实验：频率、幅值与材料时钟

观察应力—应变回线。改变频率或松弛时间会改变模量；在线性模型内改变幅值，会改变能量而保持模量。

[Figure: 应力应变回线](https://ml-biomat.com/tutorials/experimental-methods/m07/#M07-plot)

交互图同时显示一个周期内的应力—应变回线和计算出的模量。先改变频率，观察回线的斜率与张开程度；再只改变应变幅值，观察线性模型中的模量保持不变，而回线面积随幅值平方变化。最后改变松弛时间，比较同一个外部频率在不同材料时间尺度下的含义。图中参数属于明确的教学模型，单位和计算方式与正文一致。把三个控制量分开操作，能够避免把振动更快、变形更大和材料更慢混成同一种变化。

频率扫描还需要考虑测试时长。测一个很低的频率，单个周期就可能持续很久，通常还要经历若干周期才达到稳态；在这段时间里样品可能失水、老化、继续固化或发生结构恢复。若从低频扫到高频与反方向扫描得到不同结果，应检查材料是否随实验时间改变。选择频点时，可以先采用对数间隔覆盖宽范围，再在转变附近加密，既看见整体趋势，也把时间花在真正需要分辨的区域。

## 温度改变分子的时钟，也连接了科学史

加热通常让链段运动更快，因此同样的振动频率在较高温度下，可能相当于较低温度下更慢的观察。二十世纪的高分子研究把这种现象发展为时间—温度叠加：不同温度下的频率谱，如果形状相容，可以沿横轴平移到同一参考温度。Williams、Landel 和 Ferry 在 1955 年发表的关系式，为许多玻璃形成体系中温度与松弛速度的联系提供了常用表达。这个历史节点的意义在于，让实验者用可测的短时间窗口去连接更宽的动力学范围。

$$
\log_{10}a_T=-\frac{C_1(T-T_r)}{C_2+(T-T_r)},\qquad \tau(T)=a_T\tau(T_r),\qquad f_r=a_Tf
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93f58a7269ddba173c110888.svg) | 相对参考温度的水平平移因子，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以 10 为底的对数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 样品温度，此处用 °C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1240a9baf3662030a4316b2e.svg) | 参考温度，此处用 °C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d959d9fd17553ff38c0ee430.svg) | WLF 参数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c52ac7e99d50739d28c6ed2.svg) | WLF 参数，与温差具有相同单位，此处为 °C。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e17a6485dc3092a405bf22d.svg) | 温度 T 下的松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9c19e2c0b19966180a0b5b02.svg) | 参考温度下的松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 测量频率，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ace823c9792eb2dad5fee165.svg) | 移到参考温度的等效频率，Hz。 |

这组式子采用松弛时间比定义 aT，要求相关谱形可由一致的时间平移描述。教学取 C₁=8、C₂=80 °C、Tr=20 °C；T=40 °C 时 log₁₀aT=−1.6，aT≈0.0251，0.1 s 的参考松弛时间变为约 0.00251 s。

这里选用参考温度 20 °C、两个教学参数分别为 8 和 80 °C；温度升到 40 °C 时，平移因子的常用对数为 −1.6，因此平移因子约为 0.0251。若参考松弛时间为 0.1 s，相应的高温松弛时间就是约 0.00251 s。图中据此生成的频率谱，在乘以一致的横向平移因子以后重合。这是一组满足假设的计算例子，参数不是适用于所有聚合物的通用常数。实际使用时，参考温度、参数和所覆盖温度范围应一起给出。

![频率谱、相位和时间—温度叠加由同一标准线性固体模型生成。下排用 1955 年 WLF 关系的教学参数展示温度怎样改变分子时钟，再按相同定义平移频率形成主曲线；曲线为构造模型数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7e362b7ca4962b1ef51f451f.svg?v=7e362b7ca496)

图 4频率谱、相位和时间—温度叠加由同一标准线性固体模型生成。下排用 1955 年 WLF 关系的教学参数展示温度怎样改变分子时钟，再按相同定义平移频率形成主曲线；曲线为构造模型数据。

有些体系不能通过一组平移因子同时对齐所有过程。结晶、相分离、网络继续反应，或水分改变，都会让谱形发生变化；多种松弛过程对温度的敏感程度不同，也会造成形状不相容。此时保留各温度曲线的差异，往往比强行拼出一条平滑主曲线更能揭示材料变化。可以比较重叠频率范围，检查储能与损耗是否同时对齐，再结合 DSC、质量变化或结构表征寻找原因。平移不是绘图技巧，而是一个关于材料时间尺度如何变化的物理假设。

DMA 也常用来识别玻璃化转变附近的力学变化。随着链段运动变得更活跃，储能模量常出现下降，损耗模量和损耗因子可能出现峰；但储能下降的起始位置、损耗模量峰和损耗因子峰采用不同定义，给出的温度通常不同。频率、升温速率、样品热历史和含水量也会影响读数。因此比较两个样品时，要使用同一种判据和匹配条件。把一个峰温与 DSC 中热容变化的转变温度放在一起讨论，可以获得互补信息，同时保留两种测量各自观察的过程。

对于含水或含溶剂的材料，温度扫描还伴随一个容易忽略的问题：样品组成可能在变化。水分逸出会使某些网络变硬，也可能改变相分离或内部摩擦；一次扫描后的材料因此不一定等于最初的材料。可以比较升温与降温、第一次与第二次扫描，并在相应条件下检查质量或含水量，辨认哪些变化可逆、哪些来自样品重新组织。组织样品还需要留意热变性等生物结构变化。这样得到的温度响应既保留力学信息，也能与样品的化学和生物状态联系起来。

## 从完整波形计算模量，再判断结果怎样使用

本篇程序从已知储能与损耗模量生成应变和应力波形，再加入固定种子的应力噪声。计算时不直接读取模型参数，而是用正弦项、余弦项和常数项对含噪声应力做最小二乘分解。常数项吸收基线偏移，另外两个系数除以应变幅值后分别得到模量。程序同时输出逐点数据、拟合参数、相位角、回线积分和理论能量，读者可以从原始波形一路核对到最终数值。所有示例数据均为明确构造的教学记录。

选择完整周期参与计算很有帮助，因为理想正弦与余弦在完整周期上的交叉贡献相互抵消。实际仪器记录若没有对齐周期，仍可使用相同的最小二乘思想，但必须保留正确的时间与频率，并检查漂移和瞬态是否混入。每个频率刚开始施加时，材料可能还没有达到周期稳态，这时前几个周期与后面的周期不同。比较连续周期的幅值和相位是否稳定，是判断可分析区间的具体方法；仅凭波形看起来平滑，并不能替代这一检查。

### 完整示例：从波形分解到回线能量

用正弦、余弦和常数项拟合含噪声应力，独立计算每周期能量，再生成频谱与温度平移图。所有数据为教学构造并随程序导出。

```
"""DMA from complete waveforms: original constructed data and SI-unit analysis."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def moduli(omega, tau=0.1, equilibrium=2e6, branch=8e6):
    x=np.asarray(omega)*tau
    return equilibrium+branch*x*x/(1+x*x), branch*x/(1+x*x)


def shift_factor(temperature, reference=20., c1=8., c2=80.):
    difference=np.asarray(temperature)-reference
    return 10.**(-c1*difference/(c2+difference))


def main(output, language):
    from matplotlib import font_manager
    output.mkdir(parents=True,exist_ok=True)
    fonts={f.name for f in font_manager.fontManager.ttflist}
    cjk=next((n for n in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if n in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':cjk if language=='zh' else 'DejaVu Sans','font.size':11,
      'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,
      'axes.prop_cycle':plt.cycler(color=['#186e83','#cc7d3d','#8160a1','#3e876d']),
      'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5'})
    tr=lambda zh,en:zh if language=='zh' else _label(en)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    omega,amplitude=10.,.002;storage,loss=moduli(omega)
    time=np.linspace(0,8*np.pi/omega,1600,endpoint=False)
    strain=amplitude*np.sin(omega*time)
    true_stress=amplitude*(storage*np.sin(omega*time)+loss*np.cos(omega*time))
    noise_sd=100.;offset=120.
    observed=true_stress+offset+np.random.default_rng(707).normal(0,noise_sd,time.size)
    design=np.c_[np.sin(omega*time),np.cos(omega*time),np.ones(time.size)]
    coefficients=np.linalg.lstsq(design,observed,rcond=None)[0]
    fit_storage,fit_loss=coefficients[:2]/amplitude
    predicted=design@coefficients;residual=observed-predicted
    phase=np.linspace(0,2*np.pi,2001)
    loop_strain=amplitude*np.sin(phase)
    loop_stress=amplitude*(storage*np.sin(phase)+loss*np.cos(phase))
    energy=float(np.pi*loss*amplitude**2)
    integrated=float(np.trapezoid(loop_stress,loop_strain))
    summary={'data_kind':'constructed teaching experiment','seed':707,
      'storage_Pa':float(storage),'loss_Pa':float(loss),'tan_delta':float(loss/storage),
      'phase_degrees':float(np.degrees(np.arctan2(loss,storage))),
      'energy_per_cycle_J_m3':energy,'integrated_energy_J_m3':integrated,
      'power_density_W_m3':energy*omega/(2*np.pi),'shift_at_40C':float(shift_factor(40)),
      'fitted_storage_Pa':float(fit_storage),'fitted_loss_Pa':float(fit_loss),
      'fitted_offset_Pa':float(coefficients[2]),'residual_sd_Pa':float(np.std(residual,ddof=3))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(output/'waveforms.csv',np.c_[time,strain,true_stress,observed,predicted,residual],delimiter=',',comments='',header='time_s,strain,true_stress_Pa,observed_stress_Pa,fitted_stress_Pa,residual_Pa')
    frequencies=np.geomspace(.01,100,241);w=2*np.pi*frequencies;sp,lp=moduli(w)
    np.savetxt(output/'spectrum.csv',np.c_[frequencies,sp,lp,lp/sp],delimiter=',',comments='',header='frequency_Hz,storage_Pa,loss_Pa,tan_delta')

    fig,axes=plt.subplots(1,3,figsize=(12,4.4),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a,b,c=axes
    a.set_title(tr('A  薄膜拉伸','A  Film tension'),loc='left',fontweight='bold')
    for y in [1.5,7.6]:a.add_patch(Rectangle((2.5,y),5,.8,facecolor='#8b9aa1'))
    a.add_patch(Rectangle((4,2.3),2,5.3,facecolor='#badbd9',edgecolor='#186e83',lw=2))
    a.add_patch(FancyArrowPatch((8,2.2),(8,7.8),arrowstyle='<->',mutation_scale=14,color='#cc7d3d',lw=2))
    a.text(8.5,5,tr('标距','Gauge'),rotation=90,ha='center');a.text(5,.35,tr('力 ÷ 面积 → 应力','Force ÷ area → stress'),ha='center',fontsize=10)
    b.set_title(tr('B  三点弯曲','B  Three-point bending'),loc='left',fontweight='bold')
    xs=np.linspace(1,9,101);ys=5-.8*np.sin(np.pi*(xs-1)/8)
    b.plot(xs,ys,color='#186e83',lw=8)
    for x in [1,9]:b.add_patch(Polygon([[x-.6,3.7],[x+.6,3.7],[x,4.8]],facecolor='#8b9aa1'))
    b.add_patch(FancyArrowPatch((5,8),(5,4.5),arrowstyle='-|>',mutation_scale=18,color='#cc7d3d',lw=2))
    b.text(5,2.6,tr('跨度、厚度决定换算','Span and thickness enter conversion'),ha='center',fontsize=10)
    b.text(5,.35,tr('图为变形与夹持概念示意','Conceptual deformation and fixture'),ha='center',fontsize=9)
    c.set_title(tr('C  同时记录两个信号','C  Record two signals together'),loc='left',fontweight='bold')
    for y,text,color in [(7,tr('位移 → 应变','Displacement → strain'),'#186e83'),(4.8,tr('力 → 应力','Force → stress'),'#cc7d3d'),(2.6,tr('时间差 → 相位','Time difference → phase'),'#8160a1')]:
        c.add_patch(Rectangle((.4,y-.4),9,1.3,facecolor='white',edgecolor=color,lw=1.5));c.text(4.9,y+.25,text,ha='center',va='center',fontsize=11)
    c.text(5,.35,tr('环境：温度、湿度、浸液','Environment: temperature, humidity, liquid'),ha='center',fontsize=9)
    save(fig,'measurement')

    fig,axs=plt.subplots(2,1,figsize=(11,6),sharex=True,layout='constrained')
    mask=time<2*2*np.pi/omega
    axs[0].plot(time[mask],strain[mask]*100,color='#186e83',lw=2.3)
    axs[0].set(ylabel=tr('应变 / %','Strain / %'),title=tr('A  受控应变：幅值 0.2%','A  Controlled strain: amplitude 0.2%'))
    axs[1].scatter(time[mask][::4],observed[mask][::4]/1000,s=9,color='#a9b5b7',label=tr('含噪声信号','Noisy signal'))
    axs[1].plot(time[mask],predicted[mask]/1000,color='#cc7d3d',lw=2,label=tr('正弦与余弦分解拟合','Sine–cosine fit'))
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('B  应力提前：相位约 33.69°','B  Stress leads: phase approximately 33.69°'))
    for ax in axs:ax.axhline(0,color='#b5c0c3',lw=.8);ax.grid(axis='x',alpha=.15)
    axs[1].legend(frameon=False,fontsize=9,ncols=2);save(fig,'waveforms')

    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    axs[0].fill(loop_strain*100,loop_stress/1000,color='#186e83',alpha=.16)
    axs[0].plot(loop_strain*100,loop_stress/1000,color='#186e83',lw=2)
    axs[0].plot(loop_strain*100,storage*loop_strain/1000,color='#cc7d3d',ls='--',label=tr('储能分量','Storage contribution'))
    axs[0].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('A  回线面积：50.27 J/m³ / 周期','A  Loop area: 50.27 J/m³ per cycle'));axs[0].legend(frameon=False,fontsize=9)
    axs[1].scatter((omega*time)%(2*np.pi),residual,s=7,alpha=.45,color='#8160a1')
    axs[1].axhline(0,color='#818e94',lw=1);axs[1].axhspan(-200,200,color='#8160a1',alpha=.08)
    axs[1].set(xlabel=tr('周期内相位 / rad','Phase within cycle / rad'),ylabel=tr('残差 / Pa','Residual / Pa'),title=tr('B  残差保留了周期结构吗','B  Does residual structure follow the cycle?'))
    save(fig,'energy')

    fig,axs=plt.subplots(2,2,figsize=(12,8.2),layout='constrained')
    axs[0,0].loglog(frequencies,sp/1e6,label="E′",lw=2);axs[0,0].loglog(frequencies,lp/1e6,label="E″",lw=2)
    axs[0,0].axvline(omega/(2*np.pi),color='#8d999e',ls=':',lw=1)
    axs[0,0].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('模量 / MPa','Modulus / MPa'),title=tr('A  单一松弛过程与平衡弹簧','A  One relaxation process and equilibrium spring'));axs[0,0].legend(frameon=False)
    axs[0,1].semilogx(frequencies,np.degrees(np.arctan2(lp,sp)),color='#8160a1',lw=2)
    axs[0,1].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('相位角 / °','Phase angle / °'),title=tr('B  相位随观察节奏变化','B  Phase depends on the observation pace'))
    for temp,color in [(0,'#186e83'),(20,'#cc7d3d'),(40,'#3e876d')]:
        at=shift_factor(temp);_,loss_t=moduli(w,tau=.1*at)
        axs[1,0].loglog(frequencies,loss_t/1e6,label=f'{temp} °C',color=color,lw=2)
        axs[1,1].loglog(frequencies*at,loss_t/1e6,color=color,lw=2,ls=['-',':','--'][temp//20],label=f'{temp} °C')
    axs[1,0].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('损耗模量 / MPa','Loss modulus / MPa'),title=tr('C  1955 WLF 关系：温度改变时钟','C  The 1955 WLF relation: changing the clock'));axs[1,0].legend(frameon=False,fontsize=9)
    axs[1,1].set(xlabel=tr('平移后频率 aT·f / Hz','Shifted frequency aT·f / Hz'),ylabel=tr('损耗模量 / MPa','Loss modulus / MPa'),title=tr('D  一致平移后形成主曲线','D  Consistent shifts produce a master curve'));axs[1,1].legend(frameon=False,fontsize=9)
    for ax in axs.flat:ax.grid(alpha=.13,which='major')
    save(fig,'spectrum')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en')
    a=p.parse_args();main(a.output,a.language)
```

运行后，先核对无噪声的模量为 6 MPa 和 4 MPa，损耗因子为三分之二，相位约为 33.69°，理论每周期耗散能密度约为 50.27 J/m³。数值积分应接近这个能量值，差异主要来自离散步长。再比较含噪声拟合与构造值，并查看残差是否有明显周期结构。若残差保留两倍或三倍频率的波动，可以进一步检查非线性响应或信号失真。一个有物理含义的数值检查，比只确认程序成功画出一条曲线更能帮助发现问题。

材料选择时，把储能模量、损耗模量和损耗因子放回使用条件。较大的损耗因子可能来自损耗增加，也可能来自储能模量下降；前者与后者对承载能力的意义不同。对于组织支架，还要结合细胞实际施力的时间尺度、培养状态与测量几何；对于减振垫，要结合受力方式、工作频率和温升。报告中保留夹具、尺寸、预载、动态幅值、频率、温度程序、环境以及独立试样数，读者就能把一组频谱理解为有明确条件的材料证据。

把本篇与蠕变实验放在一起看，时间域和频率域就有了联系：前者观察恒定载荷下变形怎样积累，后者观察周期载荷下响应怎样错开。它们都能研究黏弹性，但实验时间窗口、控制变量和分析条件不同。下一篇旋转与振荡流变会把相同的相位概念带到液体、浆料和凝胶中，并进一步处理剪切速率、屈服、壁面滑移和几何选择。掌握了原始信号到物理量的这条路径，换一种仪器也能知道应该追问什么。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M07.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [TA Instruments — DMA Basic Theory and Applications](https://www.tainstruments.com/wp-content/uploads/2020_DMA_Online_Training_Part_1.pdf)

   仪器信号、相位、夹具与线性幅值范围。
2. [TA Instruments — Introduction to DMA of Polymer Solids](https://www.tainstruments.com/applications-notes/introduction-to-dynamic-mechanical-analysis-and-its-application-to-testing-of-polymer-solids/)

   储能与损耗定义及玻璃化转变判据。
3. [RepTate — LVE Theories](https://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html)

   Maxwell 模态的频率响应。
4. [RepTate — TTS Theories](https://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html)

   平移因子定义、参考温度及谱形比较。
5. [Williams, Landel and Ferry (1955) — Temperature Dependence of Relaxation Mechanisms](https://doi.org/10.1021/ja01619a008)

   WLF 关系的原始文献与历史节点。
6. [NumPy — numpy.linalg.lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)

   正弦—余弦分解所用最小二乘接口。
