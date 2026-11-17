# 旋转与振荡流变：从流动到凝胶网络

Source: https://ml-biomat.com/tutorials/experimental-methods/m08/
Language: zh-CN

把黏度、剪切变稀、壁面滑移和结构恢复分开理解，让流变曲线对应配方、加工与生物材料中的具体问题。

## 从能不能倒出来，问到怎样流动和恢复

蜂蜜、牙膏、蛋白质溶液和水凝胶都可能看起来“黏”，但它们在实验中表现出的原因并不相同。蜂蜜可以持续流动，牙膏在轻微作用下可能保持形状，某些聚合物溶液越搅越容易流动，而可注射凝胶在经过针头以后又需要重新支撑形状。旋转与振荡流变把这些体验拆成可以测量的问题：改变流动速度时阻力怎样变化，施加小幅来回剪切时储能与耗能各有多少，强剪切结束后结构多久恢复？这些问题直接连接配方、加工、递送和材料使用条件。

剪切可以想成把一叠扑克牌的上层向旁边推。每一层相对下一层错开，整体形状改变，而不是所有牌一起平移。液体中的相邻薄层也可以具有不同速度；速度变化除以层间距离，就得到剪切速率。旋转流变仪让样品位于两块板、一个锥与平板，或者两个同轴圆筒之间，通过转动施加运动，同时测量阻碍转动的扭矩。仪器首先看到的是转角、转速与扭矩，剪切应力和剪切速率来自测量几何的换算。

这条测量路线与生物研究早有联系。1923 年，du Noüy 发表了一种关注胶体和生理液体的黏度计，希望用很少的血清等样品，追踪黏度随时间与温度的变化。这个历史问题与今天的蛋白制剂、细胞悬液和生物墨水研究相通：样品量有限，状态会改变，测量要尽量分清材料本身和操作过程的作用。现代仪器增加了精密控制与多种加载程序，但仍然要回答同一个基本问题：我们看到的阻力，来自怎样的流动以及怎样的样品状态？

![平行板、锥板与同轴圆筒的原创原理示意。转动几何决定样品中的剪切分布；同轴圆筒旁的历史线索连接 1923 年针对少量生理液体的黏度研究。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ae0c6b1c786e1cfa38849d2d.svg?v=ae0c6b1c786e)

图 1平行板、锥板与同轴圆筒的原创原理示意。转动几何决定样品中的剪切分布；同轴圆筒旁的历史线索连接 1923 年针对少量生理液体的黏度研究。

## 先选对几何，再相信软件给出的物理量

在最直观的两平板模型中，下板不动，上板以固定速度平移。如果液体牢牢贴着两壁、流动稳定且层间速度均匀变化，上下板速度差除以间隙就是剪切速率。剪切应力表示单位面积上的切向力，黏度表示维持单位剪切速率需要多大应力。黏度单位是 Pa·s，可以理解成应力与一个时间尺度的乘积。它与密度不同：密度说明一定体积有多少质量，黏度说明流动过程中层与层相对运动有多难。

剪切速率单位中的每秒，描述的是相邻层相对变形累积的速度，不是转子每秒转了多少圈。上板速度为 1 mm/s、间隙为 1 mm 时，简单平面模型的剪切速率为 1 s⁻¹；保持上板速度不变，把间隙缩小一半，剪切速率就增加一倍。若液体黏度为 2 Pa·s，对应的剪切应力分别为 2 Pa 与 4 Pa。这个小例子把速度、距离和阻力联系起来，也说明为什么只报告转速、没有测量几何时，读者无法判断样品实际承受了怎样的剪切。

$$
\dot\gamma=\frac{U}{h},\qquad \sigma=\eta\dot\gamma
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | 简单平面流动中的剪切速率，s⁻¹；上方点表示随时间变化的速率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | 上下壁速度差，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 壁间距离，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 剪切应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 牛顿流体黏度，Pa·s。 |

在无滑移、稳定、线性速度分布的平面模型中，U=0.001 m/s、h=0.001 m 给出 1 s⁻¹；η=2 Pa·s 时应力为 2 Pa。旋转几何需要相应的半径与扭矩换算。

真实旋转平行板还有一个几何细节：越靠近外缘，同样转速对应的线速度越大，因此剪切速率随半径变化。软件常报告外缘或规定位置的速率，并根据材料响应与几何假设处理扭矩。锥板利用间隙随半径增加的特点，在小锥角、正确间隙和理想流动条件下，使大部分区域的剪切速率接近一致；同轴圆筒则把液体放在环形空间里，适合许多低黏度或容易流出板间的样品。三种几何并非只是容器形状不同，它们决定了样品怎样受到剪切。

含颗粒或细胞的样品，要特别考虑间隙与最大颗粒或团聚体尺寸的关系。间隙太窄，颗粒可能受挤压、卡住或改变局部流场，测到的阻力就混入几何约束。锥尖附近的狭小空间尤其需要注意。间隙加大以后，样品又可能更难稳定地留在板间，低黏度液体还更容易出现惯性或二次流动。选择几何时，把颗粒尺寸、样品体积、黏度范围、温度变化和预期剪切速率放在一起考虑，比先选一个常用夹具再处理所有异常更省力。

装样本身会剪切材料。挤出、移液、降下上板、修整边缘，都可能使脆弱的网络暂时松动，所以装样后的等待时间应由结构恢复过程决定。平行板需要正确设定零间隙，样品边缘应与有效测量半径相匹配；装得过多或不足会改变扭矩换算。气泡会减少实际接触面积，蒸发会改变浓度，边缘破裂会让一部分样品不再参与均匀剪切。可以同时观察样品边缘、法向力和扭矩信号，把这些变化与曲线异常对应起来。

比较不同配方时，尽量保持相同的装样顺序、预剪切、静置时间和温度历史。预剪切可以建立一致起点，但也可能不可逆地改变网络，因此要根据研究目的决定是否采用。测一个刚混合就开始凝胶化的体系，应记录混合到开始测量之间的时间；测一个经过挤出的材料，则要说明挤出与恢复过程。实验条件中的这些时间不是附带信息，它们决定仪器接触的是哪一种结构状态。

用黏度已知且温度条件明确的参照液体检查测量，可以把几何与仪器问题同复杂材料行为分开。参照液应覆盖合适的扭矩范围，测量温度与参考值温度相匹配；如果参照也出现异常的速率依赖，就先检查量程、惯性、温控和装样。扩大板半径通常能增强扭矩信号，但也会改变边缘条件和所需样品量。校准后的仪器仍需针对实际样品选取合适的几何与程序，这两步分别解决“仪器读得准不准”和“测量方式适不适合”的问题。

## 一条流动曲线，分清变稀、屈服和时间变化

牛顿流体在给定温度和组成下，黏度近似不随剪切速率改变，应力与剪切速率成正比。剪切变稀材料则随着速率增加，表观黏度降低，常与链取向、团聚结构调整或其他内部过程有关。这里“表观”表示按当前应力除以当前剪切速率定义的黏度，并不意味着数据不真实。注意黏度下降时，应力仍可能继续上升：推动材料更快通常仍需要更大的力，只是增加得没有恒黏度参照那么快。

为了看清低速和高速之间的过渡，下面采用 Carreau 型教学模型。它在低速有一个黏度平台，在较高速度逐渐变稀，并在足够高速度下趋近另一个平台。中间的时间参数决定大致从什么速率开始转变，指数控制中间区域的变化程度。这个时间参数是该经验响应模型中的尺度，不应直接当成某一条分子链的唯一松弛时间。模型帮助我们紧凑地描述数据，微观机制还需要分子量、结构和其他实验提供联系。

$$
\eta(\dot\gamma)=\eta_\infty+(\eta_0-\eta_\infty)\left[1+(t_c\dot\gamma)^2\right]^{(n-1)/2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/55ca2da5874834a3d36c10a9.svg) | 给定剪切速率下的模型黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | 剪切速率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | 零速率极限黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b784e2ff514e8c900372c5f3.svg) | 高速率极限黏度，Pa·s；∞表示极限。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2641a2efcec4baa36ea120b6.svg) | 控制转变位置的时间参数，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 中间区响应指数，无量纲；本例 0<n<1。 |

取 η₀=10 Pa·s、η∞=0.1 Pa·s、tc=2 s、n=0.4。零速率极限为 10 Pa·s，1 s⁻¹ 时约为 6.209 Pa·s；中间的 tc×剪切速率必须无量纲。

![同一构造流动数据同时以黏度和应力显示。左图给出含相对噪声的数据与 Carreau 拟合，右图说明剪切变稀时应力仍可增加。牛顿参照黏度为 10 Pa·s。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e02556cefe762c3d6588861a.svg?v=e02556cefe76)

图 2同一构造流动数据同时以黏度和应力显示。左图给出含相对噪声的数据与 Carreau 拟合，右图说明剪切变稀时应力仍可增加。牛顿参照黏度为 10 Pa·s。

若材料需要一定作用才出现明显持续流动，实验中常讨论屈服。静置后首次启动流动的静态屈服，与已经流动的材料维持流动时的动态屈服，可以得到不同数值；等待时间、加载程序和判据都影响结果。不能把任意流动曲线低速端的一段外推截距当作唯一的材料常数。可以结合应力控制蠕变、不同等待时间与稳态流动曲线，明确所报告的屈服对应哪个过程。对于可注射凝胶，这个区别分别关联启动推注的阻力和持续推注的阻力。

剪切变稀描述对速率的依赖，触变则涉及结构随时间改变并具有恢复性。把剪切速率固定以后，黏度是否继续变化，是区分二者的一个直接问题。升速与降速曲线围成的回线可能来自时间依赖，但也可能混入温度变化、蒸发或尚未达到稳态的响应。改变每个点的保持时间、比较相反扫描方向，并查看固定速率下的时间记录，可以逐步辨认原因。每个低速点往往需要更长观察，频点很多却停留很短，可能得到一条细密但含义模糊的曲线。

图中的教学数据覆盖六个数量级的剪切速率，因此绘图使用对数坐标。横轴相邻等距位置表示相同倍数的变化，而不是相同的速率差；这样低速平台与高速转变都能看清。拟合在对数黏度上进行，对应构造数据中近似恒定的相对误差。若真实仪器的主要误差是固定扭矩噪声，低应力处的相对误差会更大，就需要根据实际误差结构改变权重。拟合坐标与误差模型应一起解释。

拟合出的两个平台也需要与测量范围对应。若所有数据都位于中间变稀区，许多不同的低速平台和时间参数可能组合出近似相同的曲线；这时延伸到未测速率的预测会对参数选择很敏感。可以增加足够低速、持续时间足够长的测量，或使用独立信息约束参数。图中的构造例子特意包含较宽范围，便于读者看见转变两侧。拿真实数据练习时，应同时显示数据覆盖区间和拟合曲线，让读者知道哪些部分来自观察，哪些部分来自模型延伸。

零剪切黏度指剪切速率趋近零时的极限，而不是把一个静止样品的零应力直接除以零速率。图上可以通过足够低速的平台支持这个极限，也可以使用与实验相容的模型估计；两种做法都需要观察时间足够长，能够区分稳态与缓慢变化。对数坐标本身不包含零，因此曲线最左边的点仍然对应一个有限速率。理解这一点，就能把软件输出的极限参数与仪器实际测到的点区分开来。

## 材料真的变稀了，还是在壁面上滑动

想象用手掌推动一块果冻。如果手掌牢牢贴住果冻，果冻内部会变形；如果表面有一层水，手掌可能滑过去，果冻本体移动得少。流变仪也会遇到这样的情况：板的运动一部分消耗在界面滑动上，剩余部分才用于体相剪切。若仍用板速度除以间隙计算全部剪切速率，就会高估内部真正的变形速率，进而低估黏度。这个问题在凝胶、悬浮液、乳液等体系中尤其值得检查。

下面用一个明确的模型说明间隙诊断。假设体相是黏度恒定的牛顿流体，两侧界面具有相同滑移长度。滑移长度是把流体内部直线速度分布向壁外延长，到速度达到壁面值时对应的几何长度；它将界面滑动与内部速度梯度联系起来。两壁都滑动时，上板总位移要分配给内部剪切和两个界面，因此有效的速度变化距离包含实际间隙再加两倍滑移长度。这个简单关系能给出清楚的预测：同一种流体，在更窄间隙下可能显示更低的表观黏度。

$$
\dot\gamma_{\mathrm{bulk}}=\frac{U}{h+2b},\qquad \eta_{\mathrm{app}}=\eta\frac{h}{h+2b},\qquad v_s=b\dot\gamma_{\mathrm{bulk}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/67700e02cb2f499190a144e7.svg) | 流体内部真实剪切速率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | 两壁速度差，m/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 实际间隙，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 两壁各自相同的滑移长度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/78a927dab1b242ae576337ff.svg) | 用壁速度除以间隙定义速率后得到的表观黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 牛顿体相黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/45519a4b53cded8c1e2b5bac.svg) | 每一壁面的滑移速度大小，m/s。 |

假设两壁相同 Navier 滑移、牛顿体相和稳定平面流动。η=2 Pa·s、h=1 mm、b=0.2 mm 时，表观黏度为 2×1/(1+0.4)=1.428571 Pa·s；同一式中长度单位保持一致。

![两壁 Navier 滑移的平面牛顿模型。左图速度分布在壁面留下速度差，右图显示真实黏度固定为 2 Pa·s 时的表观间隙依赖。曲线由明确模型计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/203c5aabb4694ea5ac897e89.svg?v=203c5aabb469)

图 3两壁 Navier 滑移的平面牛顿模型。左图速度分布在壁面留下速度差，右图显示真实黏度固定为 2 Pa·s 时的表观间隙依赖。曲线由明确模型计算。

例如真实黏度为 2 Pa·s，间隙为 1 mm，两壁滑移长度各为 0.2 mm，则表观黏度约为 1.429 Pa·s。把间隙增大到 2 mm，表观黏度提高到约 1.667 Pa·s，材料本体的黏度其实没有改变。这个间隙依赖可以作为诊断线索，但真实样品也可能因为间隙改变而出现不同的结构、温度或颗粒约束，所以需要结合表面粗糙度和时间历史比较。粗糙板、齿形板或叶片转子能够帮助减少某些滑移，同时也要考虑它们对局部流动的影响。

## 交互实验：有多少运动进入了流体内部

体相黏度固定为 2 Pa·s。改变间隙、滑移长度和上壁速度，观察流体速度分布及仪器按无滑移假设读出的黏度。

[Figure: 流体速度分布](https://ml-biomat.com/tutorials/experimental-methods/m08/#M08-plot)

交互图把上壁运动拆成流体内部的速度分布与两端滑移。先把滑移长度设为零，确认表观黏度与间隙无关；再逐渐增加滑移长度，观察两壁处出现速度差；最后改变间隙，比较读出的黏度和内部剪切速率。这里采用平面、均匀、稳定的牛顿流体模型，目的是把诊断逻辑看清。换成非牛顿材料或复杂旋转几何时，应使用相应的流场关系，仍然保留“板的运动是否全部传进了样品”这个检查问题。

## 轻轻来回剪切，观察网络怎样形成

旋转流变仪除了连续转动，还可以以很小角度来回摆动。材料在这种小幅振荡下，表现出与应变同步和相差四分之一周期的两部分应力，分别对应剪切储能模量与剪切损耗模量。它们与 DMA 中的相位分解相同，只是变形方式换成了剪切。振幅扫描先帮助找到线性区域，频率扫描描述不同时间尺度的响应，时间扫描则观察凝胶形成、结构恢复或老化。把扫描类型与问题对应起来，能避免一个固定频率的读数承担过多解释。

$$
\gamma(t)=\gamma_0\sin(\omega t),\qquad \sigma(t)=\gamma_0\!\left[G^{\prime}\sin(\omega t)+G^{\prime\prime}\cos(\omega t)\right],\qquad \tan\delta=\frac{G^{\prime\prime}}{G^{\prime}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/29b9e33d3a0db087be052d2e.svg) | 剪切应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/97e4157d29a2b15aac854b6c.svg) | 剪切应变幅值，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | 剪切应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85160d4b7cf0a0fe234b2a1a.svg) | 剪切储能模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d513ad606518673291bd21cf.svg) | 剪切损耗模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 应力超前应变的相位角，rad。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7cfe4f0d59119c3e45744c16.svg) | 损耗因子，无量纲。 |

这些式子用于稳态小幅线性剪切。G′=100 Pa、G″=50 Pa、应变幅值为 0.01 时，两部分应力幅值分别为 1 Pa 和 0.5 Pa，损耗因子为 0.5。

对正在凝胶化的体系，人们常画出储能模量和损耗模量随时间的变化，并把交点作为一个方便的过程指标。这个交点的含义依赖测量频率。更有物理内容的临界凝胶判据，需要比较多个频率下的响应：在合适的临界状态，两种模量具有相同的频率幂律，损耗因子因而近似不随频率改变。Winter 与 Chambon 在二十世纪八十年代的交联聚合物研究，使这种频率结构成为辨认凝胶点的重要思路。科学问题从“哪条线在上面”推进到了“整个时间尺度范围怎样组织”。

$$
G^{\prime}=Q\omega^n\cos\!\left(\frac{n\pi}{2}\right),\qquad G^{\prime\prime}=Q\omega^n\sin\!\left(\frac{n\pi}{2}\right),\qquad \tan\delta=\tan\!\left(\frac{n\pi}{2}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/85160d4b7cf0a0fe234b2a1a.svg) | 临界幂律模型的储能模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d513ad606518673291bd21cf.svg) | 临界幂律模型的损耗模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 此频率模型的正系数，单位 Pa·sⁿ。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 临界幂律指数，无量纲，0<n<1；与前面 Carreau 指数是不同模型的独立参数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | 相位角，rad。 |

两种模量具有相同的频率因子，取比值时它被约去，因此损耗因子与频率无关。n=0.4 时 tanδ≈0.7265；n=0.5 时为 1，此时两种模量重合。

![三个临界幂律模型展示 Winter–Chambon 判据背后的频率结构。每一模型的储能与损耗具有相同指数，比例与频率无关；只有指数为 0.5 时两条曲线重合。构造谱用于比较判据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6770accbcc57d46cf0ea399b.svg?v=6770accbcc57)

图 4三个临界幂律模型展示 Winter–Chambon 判据背后的频率结构。每一模型的储能与损耗具有相同指数，比例与频率无关；只有指数为 0.5 时两条曲线重合。构造谱用于比较判据。

图中三个教学临界谱采用不同幂律指数。指数为 0.5 时，两种模量重合；指数为 0.4 时，储能模量一直更大；指数为 0.7 时，损耗模量一直更大，但三种情况的损耗因子都与频率无关。这说明“储能等于损耗”是特定指数下的情况，不是所有凝胶形成的普遍定义。实际材料需要在可测频率范围、线性幅值和近似稳定状态下检验幂律。若反应进行得太快，一次顺序频率扫描可能把时间演化误当成频率依赖，应相应调整采集策略。

对于含细胞生物墨水，较大的小幅储能模量可以帮助理解静置时形状支撑，但通过针头时的剪切通常远超小幅线性条件。需要把稳态流动、启动响应和剪切后恢复接起来，才能讨论加工与成形；细胞受力还受针头几何、流量和局部流场影响。材料的一个模量不能单独给出细胞存活率。把流变测量作为确定力学环境的一部分，再与细胞实验对应，能让两类证据在各自清楚的尺度上连接起来。

比例指标与绝对大小也应一起阅读。两个样品的损耗因子都为 0.5，一个的储能模量是 100 Pa，另一个是 10000 Pa，它们具有相同的模量比例，却需要相差一百倍的应力才能达到同样的小幅剪切应变。把曲线全部归一化有助于比较形状，但会隐藏这类承载差异。描述配方时，保留实际模量与相对比例，能够同时说明“抵抗变形有多强”和“响应中两种成分怎样分配”。同样的原则也适用于恢复比例与原始黏度的共同报告。

## 强剪切之后，恢复速度怎样变成可用信息

三阶段实验先用温和的剪切或小幅振荡记录初始状态，再施加强剪切模拟处理，最后回到与第一阶段相同的温和条件观察恢复。前后测量条件相同很重要，否则读数改变可能只是因为剪切速率不同。强剪切阶段应与研究用途相联系：它可能模拟涂布、混合或挤出的一部分条件，但不等于自动复现了整个加工流场。记录恢复到指定比例所需的时间，或者在规定时刻比较恢复程度，都比笼统写“具有自恢复能力”更具体。

为了理解曲线形状，示例引入一个介于零与一之间的结构变量，表示模型中的相对结构完整程度。静置或温和剪切允许结构逐渐重建，强剪切加快其破坏；两种作用同时存在，最终状态由它们的竞争决定。这个变量是教学模型的内部量，并非从仪器直接测得的交联比例。程序把它线性映射到黏度，展示一个有限恢复时间如何使第三阶段曲线逐渐上升。真实材料可以具有多个恢复过程，因此应先观察数据再选择模型复杂度。

$$
\frac{\mathrm{d}q}{\mathrm{d}t}=\frac{1-q}{t_r}-k|\dot\gamma|q,\qquad \eta(t)=\eta_{\min}+(\eta_{\max}-\eta_{\min})q(t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 教学模型中的相对结构完整程度，无量纲，0≤q≤1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b6e2c601f1fac12ffd56a65e.svg) | 结构变量的变化速率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce7b3f4467a12e80e6af8d40.svg) | 结构重建时间参数，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 剪切破坏系数，此写法下无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | 剪切速率，s⁻¹；绝对值表示只取大小。 |
| ![Formula](https://ml-biomat.com/static/agent-math/149f9d508f1c76e4c344a227.svg) | 该结构模型对应的黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/60fc16ed766ca41bd115bfae.svg) | 结构变量为零时的黏度，Pa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a98e02d685fd171c3442f4f7.svg) | 结构变量为一时的黏度，Pa·s。 |

第一项重建结构，第二项在剪切下破坏结构。取 tr=60 s、k=0.01，100 s⁻¹ 下的平衡 q 约为 0.01639；0.1 s⁻¹ 下约为 0.9434。程序在每一恒定速率区间使用这一方程的解析解。

![独立的结构动力学教学模型：0.1 s⁻¹、100 s⁻¹、0.1 s⁻¹ 三个阶段分别对应温和测量、强剪切与恢复。曲线描述模型结构变量映射的黏度，不是前面 Carreau 流体的时间响应。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d4d301f048f04ccab4a6dae9.svg?v=d4d301f048f0)

图 5独立的结构动力学教学模型：0.1 s⁻¹、100 s⁻¹、0.1 s⁻¹ 三个阶段分别对应温和测量、强剪切与恢复。曲线描述模型结构变量映射的黏度，不是前面 Carreau 流体的时间响应。

本例低剪切为 0.1 s⁻¹，高剪切为 100 s⁻¹，高剪切持续 30 s，随后观察 150 s 的低剪切恢复。恢复曲线没有立刻回到初始值，并不需要用“恢复失败”概括；它直接说明在这段时间内，模型中的重建仍在进行，而且温和剪切也保留了少量破坏作用。若改成完全静置，平衡结构状态和恢复过程都会变化。报告恢复比例时，应说明分母是初始稳定值、第一次瞬时值还是其他参照，避免相同百分数对应不同定义。

恢复段的上升还应与蒸发增浓、温度下降和继续发生的化学交联区分。溶剂罩、稳定温控和相同时间长度的未受强剪切对照，有助于把这些因素分开。如果材料在处理后永久改变，后续曲线描述的是新的状态；如果它随着休息逐渐接近原状态，才有进一步讨论可逆结构恢复的基础。重复三阶段测试还能检查材料是否在多次加工中积累改变，这对重复涂布、打印与循环使用很有实际价值。

## 让代码保留测量定义，让结论对应实验用途

完整程序包含几个相互独立、用途明确的构造例子。Carreau 流动数据用于练习拟合和比较应力与黏度；恒黏度滑移模型用于理解间隙诊断；结构动力学用于解释三阶段恢复；临界凝胶谱用于比较不同幂律指数。它们不是一份材料记录的四种处理结果，各自的参数和假设在代码中单独列出。这样的安排让每一种图回答一个清楚的问题，也避免为了展示许多现象而给一个模型赋予它没有的物理含义。

### 完整示例：流动、滑移、恢复与临界谱

四个独立构造模型分别回答拟合、间隙诊断、时间恢复和凝胶判据问题；每个模型的参数与输出均明确保留。

```
"""Rotational rheometry: constructed flow, slip, recovery and critical-gel examples."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,FancyArrowPatch


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def carreau(rate,eta0=10.,eta_inf=.1,time_scale=2.,exponent=.4):
    return eta_inf+(eta0-eta_inf)*(1+(time_scale*np.asarray(rate))**2)**((exponent-1)/2)


def apparent_viscosity(gap_mm,slip_mm=.2,eta=2.):
    return eta*np.asarray(gap_mm)/(np.asarray(gap_mm)+2*slip_mm)


def structure_segment(t,initial,rate,recovery_time=60.,breakdown=.01):
    speed=1/recovery_time+breakdown*rate
    equilibrium=(1/recovery_time)/speed
    return equilibrium+(initial-equilibrium)*np.exp(-speed*np.asarray(t))


def main(output,language):
    from matplotlib import font_manager
    output.mkdir(parents=True,exist_ok=True)
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((x for x in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if x in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rate=np.geomspace(.001,1000,181);true_eta=carreau(rate)
    observed_eta=true_eta*np.exp(np.random.default_rng(808).normal(0,.025,rate.size))
    def model(lograte,*p):return np.log(carreau(np.exp(lograte),np.exp(p[0]),np.exp(p[1]),np.exp(p[2]),p[3]))
    fit,cov=curve_fit(model,np.log(rate),np.log(observed_eta),p0=[np.log(10),np.log(.1),np.log(2),.4],bounds=([np.log(1),np.log(.001),np.log(.01),.05],[np.log(100),np.log(1),np.log(100),.95]))
    fit_values=[*np.exp(fit[:3]),fit[3]];predicted=carreau(rate,*fit_values)
    t1=np.linspace(0,60,121,endpoint=False);l1=structure_segment(t1,1,.1)
    start2=float(structure_segment(60,1,.1));t2=np.linspace(60,90,61,endpoint=False);l2=structure_segment(t2-60,start2,100)
    start3=float(structure_segment(30,start2,100));t3=np.linspace(90,240,301);l3=structure_segment(t3-90,start3,.1)
    times=np.r_[t1,t2,t3];structure=np.r_[l1,l2,l3];rates=np.r_[np.full(t1.size,.1),np.full(t2.size,100),np.full(t3.size,.1)];eta_time=.1+9.9*structure
    summary={'data_kind':'independent constructed teaching models','carreau_zero_rate_eta_Pa_s':float(carreau(0)),'carreau_eta_at_1_Pa_s':float(carreau(1)),
     'apparent_eta_1mm_Pa_s':float(apparent_viscosity(1)),'slip_fraction_1mm':.2/1.4,'critical_gel_tan_delta_n04':float(np.tan(.4*np.pi/2)),
     'structure_at_90s':start3,'structure_at_240s':float(l3[-1]),'fitted':dict(zip(['eta0_Pa_s','eta_inf_Pa_s','time_scale_s','exponent'],map(float,fit_values)))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(output/'flow.csv',np.c_[rate,true_eta,observed_eta,predicted,rate*observed_eta],delimiter=',',comments='',header='shear_rate_s_inverse,true_eta_Pa_s,observed_eta_Pa_s,fitted_eta_Pa_s,observed_stress_Pa')
    np.savetxt(output/'recovery.csv',np.c_[times,rates,structure,eta_time],delimiter=',',comments='',header='time_s,shear_rate_s_inverse,structure_fraction,viscosity_Pa_s')

    fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a,b,c=axes
    a.set_title(tr('A  平行板','A  Parallel plates'),loc='left',fontweight='bold')
    for y in [3,6]:a.add_patch(Rectangle((1,y),8,.6,facecolor='#85969e'))
    a.add_patch(Rectangle((1,3.6),8,2.4,facecolor='#c0ddda',alpha=.85));a.add_patch(FancyArrowPatch((2,7.5),(8,7.5),arrowstyle='-|>',mutation_scale=16,color='#cc803f',lw=2))
    a.text(5,1.6,tr('间隙可调；剪切速率随半径变化','Adjustable gap; shear rate varies with radius'),ha='center',fontsize=9)
    b.set_title(tr('B  锥板','B  Cone and plate'),loc='left',fontweight='bold')
    b.add_patch(Rectangle((1,3),8,.6,facecolor='#85969e'));b.add_patch(Polygon([[1,4.8],[5,4],[9,4.8]],facecolor='#85969e'))
    b.add_patch(Polygon([[1,3.6],[9,3.6],[9,4.8],[5,4],[1,4.8]],facecolor='#c0ddda',alpha=.8));b.text(5,1.6,tr('小锥角；理想条件下剪切近均匀','Small cone angle; nearly uniform ideal shear'),ha='center',fontsize=9)
    c.set_title(tr('C  同轴圆筒与生物流体','C  Concentric cylinders and biofluids'),loc='left',fontweight='bold')
    c.add_patch(Rectangle((1.5,2.8),7,4.8,facecolor='#c0ddda',edgecolor='#85969e',lw=3));c.add_patch(Rectangle((3.4,4),3.2,4.2,facecolor='#85969e'));c.plot([5,5],[8.2,9],color='#85969e',lw=5)
    c.text(5,1.3,tr('1923：du Noüy 关注血清等小体积样品','1923: du Noüy studied small-volume biofluids'),ha='center',fontsize=9)
    fig.suptitle(tr('现代测量几何与生物流体黏度研究的联系','Modern measurement geometries and their connection to biofluid viscosity'),fontsize=10,y=-.01)
    save(fig,'geometry')

    fig,axs=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    axs[0].loglog(rate,observed_eta,'o',ms=3,alpha=.5,label=tr('构造观测','Constructed observations'));axs[0].loglog(rate,predicted,lw=2,label=tr('Carreau 拟合','Carreau fit'))
    axs[0].set(xlabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),ylabel=tr('黏度 / Pa·s','Viscosity / Pa·s'),title=tr('A  降低的黏度与两个平台','A  Falling viscosity and two plateaus'));axs[0].legend(frameon=False,fontsize=9)
    axs[1].loglog(rate,rate*true_eta,lw=2,label=tr('同一材料的应力','Stress for the same material'));axs[1].loglog(rate,rate*10,ls='--',lw=1.5,label=tr('10 Pa·s 牛顿参照','Newtonian reference, 10 Pa·s'))
    axs[1].set(xlabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),ylabel=tr('剪切应力 / Pa','Shear stress / Pa'),title=tr('B  黏度下降时，应力仍可上升','B  Stress can rise while viscosity falls'));axs[1].legend(frameon=False,fontsize=9)
    for ax in axs:ax.grid(alpha=.13)
    save(fig,'flow')

    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    y=np.linspace(0,1,101);b=.2;h=1.;vel=(b+y*h)/(h+2*b)
    axs[0].plot(y,y,'--',label=tr('无滑移','No slip'),color='#9aabb0');axs[0].plot(vel,y,lw=3,label=tr('两壁滑移','Slip at both walls'))
    axs[0].plot([0,vel[0]],[0,0],color='#cc803f',lw=4);axs[0].plot([vel[-1],1],[1,1],color='#cc803f',lw=4)
    axs[0].set(xlabel=tr('流体速度 / 上壁速度','Fluid velocity / top-wall velocity'),ylabel=tr('高度 / 间隙','Height / gap'),title=tr('A  运动分给了界面与体相','A  Motion is shared by interfaces and bulk'));axs[0].legend(frameon=False,fontsize=9)
    gaps=np.linspace(.2,2,201)
    for slip in [0,.1,.2,.4]:axs[1].plot(gaps,apparent_viscosity(gaps,slip),lw=2,label=f'b={slip} mm')
    axs[1].set(xlabel=tr('间隙 / mm','Gap / mm'),ylabel=tr('表观黏度 / Pa·s','Apparent viscosity / Pa·s'),title=tr('B  真实黏度相同，间隙依赖不同','B  Same bulk viscosity, different gap dependence'));axs[1].legend(frameon=False,fontsize=9)
    save(fig,'slip')

    fig,axs=plt.subplots(2,1,figsize=(11,6.4),sharex=True,layout='constrained',gridspec_kw={'height_ratios':[1,2]})
    axs[0].step(times,rates,where='post',color='#cc803f',lw=2);axs[0].set_yscale('log');axs[0].set(ylabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),title=tr('A  低剪切—高剪切—低剪切','A  Low shear – high shear – low shear'))
    axs[1].plot(times,eta_time,lw=2.5);axs[1].axvspan(60,90,color='#cc803f',alpha=.1)
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('模型黏度 / Pa·s','Model viscosity / Pa·s'),title=tr('B  恢复有自己的时间尺度','B  Recovery has its own timescale'))
    save(fig,'recovery')

    fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout='constrained');w=np.geomspace(.1,100,150)
    for ax,n in zip(axes,[.4,.5,.7]):
        gp=100*w**n*np.cos(n*np.pi/2);gpp=100*w**n*np.sin(n*np.pi/2)
        ax.loglog(w,gp,lw=2,label='G′');ax.loglog(w,gpp,'--',lw=2,label='G″');ax.set(xlabel=tr('角频率 / rad·s⁻¹','Angular frequency / rad·s⁻¹'),ylabel=tr('模量 / Pa','Modulus / Pa'),title=f'n={n}; tan δ={np.tan(n*np.pi/2):.3f}');ax.legend(frameon=False,fontsize=9)
    fig.suptitle(tr('临界凝胶的频率判据：同一幂律，不要求处处 G′=G″','Critical-gel frequency criterion: a common power law, not universal G′=G″'),fontsize=13)
    save(fig,'gel')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

运行后，先核对零速率平台为 10 Pa·s，再检查 1 mm 间隙下的滑移表观黏度约为 1.429 Pa·s，以及指数 0.4 的临界损耗因子约为 0.727。随后改变构造数据噪声，比较拟合参数稳定性；改变间隙和滑移长度，观察几何诊断；改变恢复时间参数，检查第三阶段的快慢。输出的 flow.csv 与 recovery.csv 保留单位清楚的数值，summary.json 保存可以逐项复核的检查量。把真实仪器数据接进来时，应先确认列名、单位、几何定义和加载历史，再替换对应的那一个例子。

最终报告应围绕研究用途选择指标。配方是否适合泵送，需要规定速率与温度下的流动阻力；是否能在放置后保持形状，需要相应时间尺度下的弹性、屈服或蠕变信息；处理后能否继续使用，需要恢复及重复处理数据。附上几何、间隙、表面状态、装样与等待时间、温控、扫描程序和独立样品数，曲线就能成为别人可以理解和比较的证据。仪器名称告诉读者用了什么工具，测量定义与物理解释才告诉读者这条曲线回答了什么。

独立样品之间的差异值得保留在图中。来自同一次装样的几十个频点，说明这一个样品在不同条件下的响应；来自多次独立制备和装样的曲线，才能进一步反映配方与操作的重复性。可以在主图显示各次测量的细线，再给出规定条件下的汇总值，并说明误差条表示标准差、标准误还是其他范围。对于随时间演化的体系，还要采用一致的时间起点。这样，读者能分辨曲线细节、重复性和真正的配方差异，而不会把密集采样误读为大量独立实验。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [TA Instruments — Core Rheometry: Yield Stress, Time-dependency, and Rheometry Tips](https://www.tainstruments.com/applications-notes/core-rheometry-yield-stress-time-dependency-and-rheometry-tips-rh146/)

   流动、触变与壁面滑移的实验设计。
2. [TA Instruments — Yield Stress and Time-Dependency: Practical Rheology](https://www.tainstruments.com/applications-notes/yield-stress-time-dependency-practical-rheology-rh151/)

   区分真实壁滑与时间依赖引起的表观差异。
3. [Anton Paar — Avoid Measurement Errors in Rheometry](https://wiki.anton-paar.com/ie-en/avoid-measurement-errors-in-rheometry/)

   几何、装样、量程、蒸发与边缘观察。
4. [P. Lecomte du Noüy (1923) — A New Viscometer](https://pmc.ncbi.nlm.nih.gov/articles/PMC2140572/)

   少量血清等生理液体的黏度测量历史。
5. [Winter and Chambon (1986) — Analysis of Linear Viscoelasticity of a Crosslinking Polymer at the Gel Point](https://doi.org/10.1122/1.549853)

   临界凝胶频率判据的原始研究。
6. [Yucel et al. — Direct Observation of Early-Time Hydrogelation in β-Hairpin Peptide Self-Assembly](https://pmc.ncbi.nlm.nih.gov/articles/PMC2630258/)

   生物大分子自组装体系中的频率依赖与凝胶判据。
7. [RepTate — LVE Theories](https://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html)

   线性黏弹谱与 Carreau–Yasuda 型模型的延伸阅读。
8. [SciPy — curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   拟合边界、误差权重与参数解释。
