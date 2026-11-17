# 蛋白质吸附：材料接触生物环境的第一步

Source: https://ml-biomat.com/tutorials/experimental-methods/p05/
Language: zh-CN

跟随一次进样和冲洗，理解蛋白质到来、离开、带水与呈现功能的不同证据。

## 细胞遇到的表面，往往已经穿上了蛋白质外衣

一块刚制备好的材料放进含血清的培养液后，细胞接触到的环境很快就会发生变化。溶液中的蛋白质不断来到材料附近，有些暂时停留，有些更牢固地结合，还有些改变姿态，露出原先藏在内部的片段。对于细胞培养基底，我们可能希望表面呈现合适的黏附位点；对于血液接触器件或分析传感器，又可能希望减少无关蛋白质的积累。于是，“这块材料是什么化学组成”之后，还需要继续问：在真正使用的液体中，表面形成了怎样的蛋白质层，它形成多快，冲洗后还剩多少？

吸附与吸收的空间含义不同。吸附主要讨论分子在界面区域的富集，吸收则强调物质进入材料内部；多孔材料或可渗透水凝胶中，两者可能同时发生。蛋白质也不是大小相同的硬球。它们由氨基酸链折叠形成，表面分布着不同电荷与亲疏水区域，在水中具有特定构象。靠近固体后，静电作用、疏水作用、氢键、范德华作用以及水和离子的重新安排共同影响能量。把蛋白质比作带有多种接触面的柔软物体，比把它当作只有一个磁极的小磁铁更接近实验情形；同一种分子换一个姿态，接触面积和向外暴露的功能位点就可能改变。

本章围绕一个可以真正设计的实验展开：先让缓冲液流过表面，建立稳定基线，再引入已知浓度的蛋白质，最后切回不含蛋白质的同种缓冲液。连续记录得到的时间曲线称为传感图。我们将比较光学与声学两类读数，学习怎样从曲线中提取容量、速度和保留量，并解释为什么这些量各有含义。一个最终吸附量相同的表面，可能经历完全不同的形成速度；同样的声学质量，也可能由不同蛋白质量与耦合水量构成。因此，实验的目标应先落实到具体问题，再选择读数和模型。

## 从有限吸附位置，到会改变表面的生物分子

Langmuir在1932年的诺贝尔演讲中回顾了工业真空技术怎样帮助他研究表面：可控的气体、可清洁的灯丝和能够记录微小气体变化的装置，让表面作用从经验现象变成可定量比较的过程。单层吸附模型提供了一个容易理解的起点：表面有有限的位置，每个位置可以空着或被占据，分子持续到来，也持续离开。图中的格子是这一思想的原创示意。它不要求把真实蛋白质表面想象成整齐棋盘，而是先用最少的变量建立“到来、空位和离开”之间的数量关系，再观察实验在哪些地方呈现更丰富的行为。

生物分子使这个故事多了一层内容。Leo Vroman在1962年的研究中比较了蛋白质吸附后亲水与疏水固体的润湿变化，把关注点推进到“吸附后的表面呈现什么性质”。蛋白质层能改变外侧环境，材料原本的界面性质便不再是唯一决定因素。在混合蛋白质溶液中，不同分子的浓度、扩散速度与相互作用又会影响表面组成随时间的变化。早期到达的分子可能被后续分子置换，也可能重排后保留下来。因此，单一纯化蛋白质实验适合拆解具体相互作用，复杂生物液体实验则更接近实际使用环境；两种实验能够形成逐步增加复杂性的研究路线。

![原创概念图：有限位置的到来与离开、蛋白质取向和周围水、剪切振动的石英与耦合层。对应Langmuir表面研究、Vroman 1962年润湿研究与Sauerbrey 1959年频率–质量关系；不按分子或装置比例。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/77494e882c91db8e4a1a0de4.svg?v=77494e882c91)

图 1原创概念图：有限位置的到来与离开、蛋白质取向和周围水、剪切振动的石英与耦合层。对应Langmuir表面研究、Vroman 1962年润湿研究与Sauerbrey 1959年频率–质量关系；不按分子或装置比例。

1959年Sauerbrey建立了石英振动频率变化与薄层附加质量的关系，为后来观察极少量界面物质提供了另一条路线。石英具有压电性质：电场可以引起机械变形，机械变形也能产生电信号。传感器中的薄石英片以很高的频率作剪切振动，附着在表面的物质改变它的振动响应。随后发展出的耗散监测，又把振动停止驱动后衰减得多快纳入记录。历史上的有限位置模型、蛋白质改变表面的认识，以及灵敏的界面传感器，在今天的吸附实验中相遇：一个描述动力学，一个提醒我们关注生物状态，一个提供实时信号。

这里有一个特别有用的研究顺序。先用化学组成和厚度比较明确的平面模型表面建立测量方法，再把相同表面化学引入实际器件或多孔支架。平面传感器便于知道面积和流动条件，多孔结构则具有内部面积、扩散路径和可能的滞留液体。两者得到不同数值时，应先检查分母采用的是投影面积、实际可接近面积还是材料质量。这样，模型表面实验能解释某些相互作用，实际结构实验能检验这些作用在复杂几何中怎样表现，二者的联系建立在明确的测量定义上。

## 光学信号和石英频率分别看见什么

表面等离子体共振，简称SPR，利用金属薄膜附近的光学响应检测界面折射率变化。折射率描述光在介质中的传播性质；当蛋白质在表面富集、替换原先由水占据的部分体积时，局部光学环境改变，仪器读数随之移动。通常先记录响应单位，再通过适当模型或标定解释结合量。相同体系内，响应与表面分子数量的关系能够支持动力学分析；把响应进一步换成绝对质量时，还涉及材料的光学性质与仪器标定。本章构造数据直接采用已经标定的等效面密度，便于比较物理量，不把某个固定响应单位武断地等同于所有材料通用的质量单位。

石英晶体微天平及耗散监测，简称QCM-D，记录共振频率变化与耗散变化。频率下降常与附加负载有关，耗散则反映振动过程中能量损失的变化。薄、刚性、牢固耦合的膜可以使用Sauerbrey关系，把按谐波数归一化的频移换成面密度。谐波可以理解为同一振动系统在不同频率模式下的响应，例如5兆赫基频对应第三、第五等奇数谐波。不同谐波的归一化频移是否接近，以及耗散是否较小，为判断简单刚性模型是否合适提供信息；还要结合膜厚、均匀性和溶液条件一起观察。

$$
\Gamma_Q=-C_Q\frac{\Delta f_n}{n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ea099b4870b360b7240fa408.svg) | Sauerbrey声学面密度变化，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5246fed9d112b38b3d16f46c.svg) | 5 MHz基频石英的质量系数，17.7 ng/(cm²·Hz)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd14ee12476c7cb989d35bb4.svg) | 第n谐波相对于基线的频移，Hz。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 奇数谐波数，无量纲，如5。 |

适用于薄、刚性、牢固耦合的层，并在匹配液体基线下解释。第五谐波−50 Hz对应177 ng/cm²；液体中包括耦合水的负载定义需保留。

对于5兆赫石英，常用系数为每赫兹每平方厘米17.7纳克。若第五谐波频率下降50赫兹，先除以5得到负10赫兹，再乘上带负号的系数，得到177纳克每平方厘米。忘记谐波归一化会产生五倍差异。液体中的声学负载还包括随膜运动的水：水可以与分子直接关联，也可以被困在层内或通过流体运动耦合。于是，声学面密度与光学估计的蛋白质面密度可能不同。举例说，200纳克每平方厘米蛋白质若伴随300纳克每平方厘米耦合水，理想刚性耦合极限下总声学质量为500，而蛋白质本身仍为200。

$$
\Gamma_Q=\Gamma_p+\Gamma_w=\Gamma_p(1+h)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ea099b4870b360b7240fa408.svg) | 理想刚性耦合极限下的总声学面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/84290949f1b09115dbf4d4de.svg) | 蛋白质面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/79041d57b32a3efcee507dc2.svg) | 随膜运动的水面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 水质量与蛋白质质量之比，无量纲。 |

质量加和的教学极限，不是软膜黏弹性反演。Γp=200、h=1.5时Γw=300，总量500 ng/cm²。

软膜还会在振动中变形，因此频率变化包含黏弹性贡献。此时需要利用多个谐波的频率与耗散，结合膜和液体模型估计厚度或力学参数。把所有频移都直接乘上质量系数，会把模型选择藏进一个看似简单的数字。耗散增大也不等于已直接测得某个唯一的蛋白质构象；它提供的是能量损失信息，可以与其他观察共同支持结构解释。比较光学与声学结果时，表面化学、缓冲液、温度、流动与观察时间都应匹配，才能把差异主要联系到两种方法的物理敏感性。

## 把一次进样做成可以解释的时间曲线

流动实验从稳定缓冲液开始。缓冲液控制酸碱度，盐影响带电分子之间的作用；温度同时影响蛋白质状态、液体性质与传感器响应。蛋白质样品最好与流动缓冲液具有匹配的组成，否则切换液体时，体相折射率或黏度密度的变化会造成信号阶跃。这个阶跃可以发生在蛋白质尚未吸附之前，切回缓冲液时又突然消失。气泡则可能产生更突兀的扰动，并改变有效接触面积。准备过程中应按仪器要求处理溶液、避免引入气泡，确认基线在所需时间尺度上稳定，再开始解释进样后的变化。

参考通道的作用，是记录与目标表面结合无关但同时出现的贡献。SPR结合实验中，它可以采用缺少活性配体、但其他处理相近的表面；材料吸附研究中，则需要根据比较对象设计具有明确含义的对照。参考并不是随便选一块不会吸附的表面：若两通道对溶液变化、非特异吸附或温度的响应不同，简单相减后仍会留下差异。额外的空白缓冲液进样能够帮助识别共同的进样与漂移特征。对照设计的重点，是让被减去的信号对应一个真正想排除的物理贡献。

![构造数据：A为样品与参考，B为五浓度校正曲线及共享拟合，C为残差，D比较蛋白质质量与规定水/蛋白质量比1.5的刚性耦合极限。竖线为开始进样与180 s切换冲洗。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f1eacbfe0a16e2632c42463a.svg?v=f1eacbfe0a16)

图 2构造数据：A为样品与参考，B为五浓度校正曲线及共享拟合，C为残差，D比较蛋白质质量与规定水/蛋白质量比1.5的刚性耦合极限。竖线为开始进样与180 s切换冲洗。

图中的构造数据把这一问题展开。样品通道包含蛋白质面密度、进样时的体相阶跃、缓慢漂移和噪声；参考通道包含相同阶跃与漂移以及自己的噪声。相减后，再用进样前的平均值调整零点，得到可供拟合的曲线。减去参考不会消除所有随机噪声，因为两通道的噪声并不相同；它主要消除共同的系统贡献。程序同时保存相减前后的数据，因此可以回头判断某个尖峰来自样品、参考还是两者的差。直接只保存一条平滑后的曲线，会失去这种区分能力。

进样持续180秒，随后冲洗到600秒。在关联阶段，分子到来和离开同时发生；在理想冲洗阶段，近表面游离浓度迅速降低，曲线主要反映离开过程。如果解离的分子未及时被带走，又在附近重新结合，观察到的下降就会变慢。增加流速、降低表面结合位点密度或改变流道条件，可以检查传质和再结合的影响。高流速也必须与样品稳定性及仪器允许范围配合。研究者应把流量作为实验变量记录，而不是把软件拟合的速度常数自动当作与装置条件无关的分子属性。

## 从空位与占位，推导一条最简单的吸附曲线

把表面总容量记为一个固定上限，当前已有的蛋白质占据其中一部分。到来速率应与溶液浓度有关，因为附近分子越多，接触机会通常越多；也应与剩余空位有关，因为位置逐渐被占满。离开速率则与当前占据量有关，表面没有分子时就没有可离开的分子。将到来项减去离开项，便得到一阶单位置模型。它假设位置性质相同、每个位置独立、表面浓度等于已知体相浓度，且没有额外的构象转换或多层生长。模型之所以适合入门，是每个项都能对应一个清楚的分子事件。

$$
\frac{d\Gamma}{dt}=k_{\mathrm{on}}c(\Gamma_{\max}-\Gamma)-k_{\mathrm{off}}\Gamma,\quad K_D=\frac{k_{\mathrm{off}}}{k_{\mathrm{on}}},\quad\Gamma_{\mathrm{eq}}=\Gamma_{\max}\frac{c}{c+K_D}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | 当前吸附蛋白质面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 近表面游离蛋白质浓度，μmol/L；示例取已知体相浓度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/96b11419ef9b145692736b96.svg) | 单位置模型容量，300 ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | 结合速率常数，(μmol/L)⁻¹s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 离开速率常数，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a443778a30c5870335c56f4d.svg) | 平衡解离常数，μmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff8de87dac4fb31350383329.svg) | 给定浓度的平衡面密度，ng/cm²。 |

等价独立位置、无额外状态转变且传质足够快的模型。kon=0.02、koff=0.002得到KD=0.1 μmol/L；c=KD时容量占据一半，即150 ng/cm²。

达到平衡时，到来与离开的速率相同，曲线平均不再上升，但分子仍然交换。平衡覆盖分数随浓度增加而增大，在浓度等于解离常数时达到二分之一。示例规定结合速率常数为0.02每微摩尔每升每秒，离开速率常数为0.002每秒，两者之比为0.1微摩尔每升。容量是300纳克每平方厘米，因此在0.1微摩尔每升充分平衡后应有150纳克每平方厘米。这里的“充分平衡”是时间条件；180秒结束进样时，实际只达到约76.99，直接把这个终点当作平衡值会改变浓度曲线的解释。

$$
\Gamma(t)=\begin{cases}\Gamma_{\mathrm{eq}}[1-e^{-(k_{\mathrm{on}}c+k_{\mathrm{off}})t}],&0\le t\le t_i,\\\Gamma(t_i)e^{-k_{\mathrm{off}}(t-t_i)},&t>t_i,\end{cases}\qquad t_{1/2}=\frac{\ln2}{k_{\mathrm{off}}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b07e3ee7455065c1715113d8.svg) | 时刻t的蛋白质面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff8de87dac4fb31350383329.svg) | 进样浓度对应的平衡面密度，ng/cm²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 以进样开始为零点的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | 进样结束与冲洗开始时间，180 s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | 结合速率常数，(μmol/L)⁻¹s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 进样阶段浓度，μmol/L。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | 离开速率常数，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | 从冲洗起点计的剩余量减半时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底，无量纲。 |

初始表面为空、进样浓度恒定，冲洗使游离浓度近似为零。默认条件下180 s为76.9872 ng/cm²，600 s为33.2362 ng/cm²，半衰时间346.574 s。

在冲洗阶段，若近表面游离浓度可以近似取零，剩余量按指数下降。离开常数为0.002每秒时，约346.57秒后剩余一半。注意计时起点是冲洗开始，而不是进样开始；在本例中，600秒对应已经冲洗420秒，剩余约33.24纳克每平方厘米。把两组速率同时放大三倍，会保留相同的平衡解离常数，却让到达平衡和冲洗下降都更快。这说明亲和程度与速度不同：最终偏好相同的两种相互作用，可以具有完全不同的时间节奏。

![A为平衡覆盖率，B把两种速率共同改变而保持KD=0.1 μM，C将冲洗段按起点归一化。亲和程度、形成速度和保留比例在不同面板中分开。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4e6b8595a404cf4e7d3b233d.svg?v=4e6b8595a404)

图 3A为平衡覆盖率，B把两种速率共同改变而保持KD=0.1 μM，C将冲洗段按起点归一化。亲和程度、形成速度和保留比例在不同面板中分开。

为了同时估计结合速度、离开速度与容量，程序把五个浓度的全部时间点放在一起拟合，让它们共享三个参数。含噪数据得到结合常数约0.02005、离开常数约0.001998每秒、容量约299.61纳克每平方厘米，解离常数约0.09964微摩尔每升。不同浓度帮助分开容量与结合速度的影响，冲洗段帮助确定离开速度。拟合残差沿时间展开后，若在进样切换处或某个阶段持续同向偏离，就提示简单模型遗漏了过程；增加参数之前，先检查缓冲液匹配、传质、表面异质性和蛋白质聚集等具体原因。

## 真实薄层的厚度，怎样与水和模型联系起来

下面重绘Kobayashi等人在2018年发表的公开数据。研究中的氧化聚苯乙烯表面吸附牛血清白蛋白BSA或纤连蛋白FN，QCM-D信号经Voigt模型估计膜厚。20摄氏度时，两者厚度均值分别为4.5与13.8纳米；37摄氏度时分别为4.2与10.3纳米。误差棒表示三次实验的标准差。图保留论文给出的汇总量，没有把均值和标准差展开成虚构的个体观测。读图时应把“模型厚度”“具体表面”和“温度”连在一起，避免将其中一个数值当作蛋白质在所有条件下固定的分子直径。

![公开实验汇总数据重绘：Kobayashi等，Int. J. Mol. Sci. 19, 1516 (2018)，表2，doi:10.3390/ijms19051516，CC BY 4.0。氧化聚苯乙烯表面上BSA与FN的QCM-D/Voigt模型厚度；误差棒为三次实验的标准差，点为均值，未构造个体数据。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/25af5d196f5891a25776799d.svg?v=25af5d196f58)

图 4公开实验汇总数据重绘：Kobayashi等，Int. J. Mol. Sci. 19, 1516 (2018)，表2，doi:10.3390/ijms19051516，CC BY 4.0。氧化聚苯乙烯表面上BSA与FN的QCM-D/Voigt模型厚度；误差棒为三次实验的标准差，点为均值，未构造个体数据。

若没有实时界面传感器，也可以测量接触材料前后溶液中的蛋白质浓度，再用溶液体积计算减少的总量。这种耗减法需要同时处理容器壁吸附、蒸发和取样损失。假设100微升溶液最初含20微克蛋白质，接触面积为1平方厘米的材料后少了0.2微克，对应200纳克每平方厘米；但浓度变化只有初始量的百分之一，配液和浓度测定精度就变得十分关键。设置同样容器与等待时间、但不放入材料的空白，能够估计容器造成的损失；表面吸附量较小、溶液体积较大时，直接观察界面通常更有利于分辨这类微小变化。

荧光标记提供另一种路线：在蛋白质上连接可发光的基团，用光强比较表面分布。它可以揭示吸附是否集中在某些区域，但标记比例、光漂白、环境对发光效率的影响，以及标记是否改变分子相互作用，都进入定量过程。把标记蛋白质与未标记蛋白质混合，并保持总浓度和标记比例一致，有助于建立清楚的比较。选用哪种方法，取决于最需要的观察是空间分布、实时动力学还是总量，而不同信号之间的互补正是实验设计的价值。

一个吸附层的厚度与它的分子长度不是同一件事。蛋白质可能平躺、倾斜或伸展，层中还可能含有水；表面覆盖不足时，均匀层模型会用某个平均响应描述并不完全连续的分布。因此，比较厚度时也需要问面密度是否相同、层是否连续，以及所采用的密度或光学参数是否一致。图中两个蛋白质的差异为理解这些问题提供了真实尺度：几纳米与十几纳米都属于常见光学显微镜无法直接分辨的薄层，却能通过合适的界面敏感方法建立定量描述。

对于细胞黏附，蛋白质总量只是研究链条的一部分。细胞受体识别的是可接近的分子片段；同样质量的层，如果关键片段被遮挡或构象改变，生物功能就可能不同。可以把总量测量与识别特定位点的抗体实验、酶活性、适当光谱或细胞响应结合。对抗污材料，则应在与使用场景相关的蛋白质混合物、温度和接触时间下比较保留量，而不只比较某一种纯化蛋白质的短时结果。每增加一种观察，都应说明它补充的是数量、组成、结构还是功能，避免几种实验重复回答同一个问题。

实验结束后的冲洗也定义了“剩余吸附量”。温和缓冲液冲洗保留的是该流动条件下仍留在表面的组分，改变盐、酸碱度或加入竞争分子后得到的保留量则对应另一种条件。干燥后称量或成像又可能改变含水层的结构，因此湿态与干态结果需要明确区分。若研究的是可再生传感器，应进一步比较多次吸附—冲洗循环后的基线与容量，确认材料是否逐轮积累残留或失去活性。这样的记录把一次漂亮的时间曲线推进到实际使用中的稳定表现。

## 交互实验：同样的亲和程度，可以有不同速度

交互图采用相同的单位置模型，允许改变浓度、结合速度与离开速度，容量固定为300纳克每平方厘米。先保持两种速度不变，只提高浓度：关联阶段上升更快，平衡占据也增加。再同时把两种速度乘以相同倍数，观察解离常数保持不变，但曲线更快达到目标并更快下降。最后只减小离开速度，比较冲洗后的保留分数。图中同时显示180秒的进样终点与600秒的保留量，帮助分清平衡容量、有限时间形成量以及经过规定冲洗后的剩余量。

## 交互：吸附与冲洗

实线为有限时间吸附量，虚线为进样浓度下的平衡目标；180 s开始冲洗。

[Figure: 吸附时间曲线](https://ml-biomat.com/tutorials/experimental-methods/p05/#P05-plot)

默认浓度正好等于0.1微摩尔每升解离常数，因此虚线平衡目标为150纳克每平方厘米；实际曲线在180秒时仍低于它。把浓度提高到0.4微摩尔每升，平衡目标变为240，同时到达目标的特征速度也增加。这个变化来自模型中“浓度乘空位”的到来项。冲洗开始后，浓度输入被切为零，下降比例由离开常数控制。将不同浓度曲线各自除以冲洗起点值，在模型成立时，它们应落到相同的归一化下降曲线上；实验中若明显分开，就有理由检查再结合、异质位点或状态变化。

## 完整分析：保留原始通道，再检验模型

完整程序从五组已知浓度生成关联与冲洗曲线，加入共同的体相阶跃、漂移和独立噪声，完成参考相减与基线校正后进行共享参数拟合。拟合在参数的对数空间中进行，所以结合速度、离开速度和容量保持正值；这是一种数值参数化方法，并未改变物理方程。程序还计算无噪声数据的恢复结果，检查优化能否回到规定参数，并用手算可得的半占据、半衰时间和第五谐波质量换算作独立核对。原始通道、参考通道、校正曲线、预测值和真实教学曲线都保存到表格中。

### 完整Python：参考相减与多浓度动力学

生成可核对的构造曲线，执行正参数共享拟合，同时重绘有明确许可的公开汇总数据。

```
"""Protein adsorption: reversible kinetics, referencing and hydrated mass.
Constructed observations are distinct from the bundled published summary table.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse,Circle

def coverage(time,concentration,kon=.02,koff=.002,capacity=300.,injection=180.):
    t=np.asarray(time,dtype=float);rate=kon*concentration+koff
    eq=capacity*kon*concentration/rate
    end=eq*(-np.expm1(-rate*injection))
    return np.where(t<0,0,np.where(t<=injection,eq*(-np.expm1(-rate*np.maximum(t,0))),end*np.exp(-koff*np.maximum(t-injection,0))))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True)
    tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1805);time=np.arange(-60,602,2.);conc=np.array([.025,.05,.1,.2,.4]);truth=np.array([coverage(time,c) for c in conc]);bulk=np.array([25*(c/.1)*((time>=0)&(time<180)) for c in conc]);drift=.008*(time+60)
    reference=bulk+drift+rng.normal(0,.8,truth.shape);raw=truth+bulk+drift+rng.normal(0,1.2,truth.shape)
    corrected=raw-reference;corrected-=corrected[:,time<0].mean(axis=1,keepdims=True)
    def residual(logp):
        k1,k2,cap=np.exp(logp);return (np.array([coverage(time,c,k1,k2,cap) for c in conc])-corrected).ravel()
    fit=least_squares(residual,np.log([.015,.003,280.]));kon,koff,cap=np.exp(fit.x);pred=np.array([coverage(time,c,kon,koff,cap) for c in conc])
    noiseless=least_squares(lambda x:(np.array([coverage(time,c,*np.exp(x)) for c in conc])-truth).ravel(),np.log([.015,.003,280.]))
    base=coverage(time,.1);hydration=1.5;acoustic=base*(1+hydration);df5=-5*acoustic/17.7
    summary={'fit_kon_uM_inv_s_inv':float(kon),'fit_koff_s_inv':float(koff),'fit_capacity_ng_cm2':float(cap),'fit_KD_uM':float(koff/kon),'fit_rmse_ng_cm2':float(np.sqrt(np.mean((pred-corrected)**2))),
    'specified_KD_uM':.1,'equilibrium_at_KD_ng_cm2':150.,'mass_at_180s_ng_cm2':float(coverage(180,.1)),'mass_at_600s_ng_cm2':float(coverage(600,.1)),
    'rinse_half_life_s':float(np.log(2)/.002),'sauerbrey_5th_minus50Hz_ng_cm2':177.,'hydrated_mass_for_200_ng_cm2':500.,
    'noiseless_fit_kon':float(np.exp(noiseless.x[0])),'noiseless_fit_koff':float(np.exp(noiseless.x[1])),'noiseless_fit_capacity':float(np.exp(noiseless.x[2])),'data_kind':'Constructed kinetics; published table summarized separately'}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    rows=np.vstack([np.column_stack([np.full(len(time),c),time,raw[i],reference[i],corrected[i],pred[i],truth[i]]) for i,c in enumerate(conc)])
    np.savetxt(o/'data.csv',rows,delimiter=',',header='concentration_uM,time_s,raw_equivalent_ng_cm2,reference_equivalent_ng_cm2,corrected_ng_cm2,fit_ng_cm2,specified_ng_cm2',comments='')
    np.savetxt(o/'acoustic.csv',np.column_stack([time,base,acoustic,df5]),delimiter=',',header='time_s,protein_ng_cm2,rigid_limit_coupled_ng_cm2,delta_f5_Hz',comments='')
    tab=list(csv.DictReader((Path(__file__).parent/'data/kobayashi2018-table2.csv').open(encoding='utf8')))
    fig,axs=plt.subplots(1,3,figsize=(14.5,4.5))
    for ax in axs:ax.set_xlim(0,10);ax.set_ylim(0,6);ax.axis('off')
    ax=axs[0];ax.add_patch(Rectangle((.4,1),9.2,.6,facecolor='#a7b8c0'))
    for j in range(8):
        ax.add_patch(Rectangle((.7+j*1.1,1.6),.85,.45,facecolor='white',edgecolor=blue))
        if j in [0,2,3,6]:ax.add_patch(Circle((1.1+j*1.1,2.45),.4,color=green))
    ax.annotate('',xy=(5.6,2.3),xytext=(5.6,4.1),arrowprops={'arrowstyle':'<->','color':orange,'lw':2});ax.text(5,5,tr('Langmuir：有限位置与动态平衡','Langmuir: finite sites and exchange'),ha='center',fontsize=10);ax.text(5,.25,tr('位置可空出，也可被占据','Sites can be empty or occupied'),ha='center',fontsize=10)
    ax=axs[1];ax.add_patch(Rectangle((.5,1),9,.6,facecolor='#a7b8c0'));ax.add_patch(Ellipse((3,2.3),3,.9,angle=10,facecolor=green));ax.add_patch(Ellipse((7,2.7),1.4,2.1,facecolor=orange))
    for x,y in [(2,2.8),(3,3),(4,2.7),(6.3,3.6),(7,3.9),(7.7,3.5)]:ax.add_patch(Circle((x,y),.17,color='#82c5df'))
    ax.text(5,5,tr('Vroman，1962：吸附改变润湿','Vroman, 1962: adsorption alters wetting'),ha='center',fontsize=9);ax.text(5,.25,tr('取向、暴露基团与周围水','Orientation, exposed groups and water'),ha='center',fontsize=9)
    ax=axs[2];ax.add_patch(Rectangle((1,1.4),8,.6,facecolor='#b6cbd1'));ax.add_patch(Rectangle((1,2),8,.15,color=orange));
    for x in [2,4,6,8]:ax.add_patch(Ellipse((x,2.5),1.1,.6,facecolor=green))
    ax.annotate('',xy=(8,1),xytext=(2,1),arrowprops={'arrowstyle':'<->','color':blue,'lw':2});ax.text(5,5,tr('Sauerbrey，1959：频率与附加质量','Sauerbrey, 1959: frequency and added mass'),ha='center',fontsize=9);ax.text(5,.25,tr('石英作剪切振动，膜随其运动','Quartz shears; coupled film moves with it'),ha='center',fontsize=9);save(fig,'history')
    fig,axs=plt.subplots(2,2,figsize=(12,8.7));aa,bb,cc,dd=axs.ravel();i=2
    aa.plot(time,raw[i],color=blue,label=tr('样品通道','Sample channel'));aa.plot(time,reference[i],color=orange,label=tr('参考通道','Reference channel'));aa.legend(fontsize=9);aa.set_title(tr('A  体相阶跃与漂移叠加','A  Bulk step and drift are superposed'),loc='left');aa.set_ylabel(tr('等效面密度 / ng/cm²','Equivalent areal mass / ng/cm²'))
    for j,c in enumerate(conc):bb.scatter(time[::5],corrected[j,::5],s=9,alpha=.55);bb.plot(time,pred[j],label=f'{c:g} μM')
    bb.legend(fontsize=8,ncol=2);bb.set_title(tr('B  多浓度共享动力学参数','B  Concentrations share kinetic parameters'),loc='left');bb.set_ylabel(tr('蛋白质面密度 / ng/cm²','Protein areal mass / ng/cm²'))
    for j in range(5):cc.plot(time,corrected[j]-pred[j],lw=.7,alpha=.65)
    cc.axhline(0,color='#a1abb2');cc.set_title(tr('C  保留全部拟合残差','C  Retain all fit residuals'),loc='left');cc.set_ylabel(tr('残差 / ng/cm²','Residual / ng/cm²'))
    dd.plot(time,base,color=green,label=tr('蛋白质质量','Protein mass'));dd.plot(time,acoustic,color=blue,label=tr('刚性极限耦合质量','Rigid-limit coupled mass'));dd.legend(fontsize=9);dd.set_title(tr('D  耦合水改变声学质量定义','D  Coupled water changes acoustic mass'),loc='left');dd.set_ylabel(tr('面密度 / ng/cm²','Areal mass / ng/cm²'))
    for ax in axs.ravel():ax.axvline(0,color='#b3bec4',ls=':');ax.axvline(180,color='#b3bec4',ls=':');ax.set_xlabel(tr('时间 / s','Time / s'))
    fig.tight_layout();save(fig,'sensorgrams')
    fig,axs=plt.subplots(1,3,figsize=(14,4.5));cc=np.logspace(-3,1,200);axs[0].semilogx(cc,cc/(cc+.1),color=blue);axs[0].axvline(.1,color=orange,ls='--');axs[0].axhline(.5,color='#a1abb2',ls=':');axs[0].set_xlabel(tr('浓度 / μmol/L','Concentration / μmol/L'));axs[0].set_ylabel(tr('平衡覆盖分数','Equilibrium occupied fraction'));axs[0].set_title(tr('A  半占据对应KD','A  Half occupancy at KD'),loc='left')
    for k,col in [(.001,blue),(.002,orange),(.006,green)]:axs[1].plot(time,coverage(time,.1,k*10,k)/300,color=col,label=f'koff={k:g} s⁻¹')
    axs[1].set_xlabel(tr('时间 / s','Time / s'));axs[1].set_ylabel(tr('占据分数','Occupied fraction'));axs[1].set_title(tr('B  相同KD，不同速度','B  Same KD, different rates'),loc='left');axs[1].legend(fontsize=8)
    rinse=np.linspace(0,600,200)
    for k,col in [(.001,blue),(.002,orange),(.006,green)]:axs[2].plot(rinse,np.exp(-k*rinse),color=col)
    axs[2].set_xlabel(tr('冲洗经过时间 / s','Elapsed rinse time / s'));axs[2].set_ylabel(tr('相对冲洗开始的保留分数','Fraction retained from start of rinse'));axs[2].set_title(tr('C  冲洗读取离开速度','C  Rinse reads the departure rate'),loc='left');fig.tight_layout();save(fig,'kinetics')
    fig,axs=plt.subplots(1,2,figsize=(11.8,4.8))
    for ax,protein in zip(axs,['BSA','FN']):
        rr=[r for r in tab if r['protein']==protein];x=np.array([float(r['temperature_C']) for r in rr]);y=np.array([float(r['thickness_mean_nm']) for r in rr]);err=np.array([float(r['thickness_sd_nm']) for r in rr]);ax.errorbar(x,y,yerr=err,fmt='o',ms=9,capsize=5,color=green if protein=='BSA' else blue);ax.set_xticks([20,37]);ax.set_xlim(15,42);ax.set_ylim(0,16);ax.set_xlabel(tr('温度 / °C','Temperature / °C'));ax.set_ylabel(tr('Voigt模型厚度 / nm','Voigt-model thickness / nm'));ax.set_title(protein+' · '+tr('氧化聚苯乙烯','Oxidized polystyrene'),loc='left');ax.text(.04,.08,tr('均值±标准差；n=3','Mean ± SD; n=3'),transform=ax.transAxes,fontsize=10)
    fig.suptitle(tr('Kobayashi等，2018，表2数据重绘 · CC BY 4.0','Kobayashi et al., 2018, Table 2 redrawn · CC BY 4.0'),fontsize=12);fig.tight_layout();save(fig,'published')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

阅读输出时，可以从最容易解释的量开始。先检查进样前的零点，再看切换时是否留下阶跃；随后比较不同浓度的上升与同一冲洗条件下的下降，最后再阅读三个拟合参数。声学示例单独标为刚性耦合极限，展示蛋白质与水的质量定义；真实论文表格则单独保存其模型、表面、温度、样本数和开放许可。这样，构造数据提供可核对的推理练习，公开实验数据提供实际研究尺度。研究新的材料时，也可以沿着这个顺序，把“表面有东西”逐步变成关于形成速度、保留量、组成与功能的清楚证据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Irving Langmuir — Surface Chemistry, Nobel lecture (1932)](https://www.nobelprize.org/uploads/2018/06/langmuir-lecture.pdf)

   真空、灯丝、表面实验与单层思想的历史原文。

   Historical facts paraphrased; no lecture figures reproduced.
2. [Leo Vroman — Effect of Adsorbed Proteins on the Wettability of Hydrophilic and Hydrophobic Solids (1962)](https://www.nature.com/articles/196476a0)

   蛋白质吸附改变外侧润湿性质的历史研究。
3. [NPTEL — Langmuir adsorption assumptions](https://archive.nptel.ac.in/content/storage2/courses/103104045/lecture25/25_6.htm)

   等价独立位置与单层模型。
4. [Biolin Scientific — QCM-D measurement](https://www.biolinscientific.com/measurements/qcm-d)

   压电、谐波、频率与耗散。
5. [Biolin Scientific — The QCM-D principle](https://www.biolinscientific.com/faq/the-qcm-d-principle)

   光学与声学质量及耦合水的区别。
6. [Biolin Scientific — Sauerbrey equation](https://www.biolinscientific.com/blog/what-is-the-sauerbrey-equation)

   1959年关系、17.7系数与刚性层条件。
7. [Cytiva — Kinetics and affinity measurements with Biacore systems](https://cdn.cytivalifesciences.com/api/public/content/digi-33041-pdf)

   参考表面、传质、浓度系列和动力学设计。
8. [Harvard CMI — Surface plasmon resonance](https://cmi.hms.harvard.edu/surface-plasmon-resonance)

   折射率、配体、分析物与响应单位。
9. [Kobayashi et al. — Temperature and serum protein adsorption (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5983614/)

   表2的真实QCM-D/Voigt厚度汇总，保留表面、温度与n。

   CC BY 4.0; numeric table transcribed and bilingual chart redrawn; attribution and licence included.
