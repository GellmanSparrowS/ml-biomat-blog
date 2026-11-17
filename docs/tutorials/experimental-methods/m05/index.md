# 应力松弛：拉住不动后力为什么下降

Source: https://ml-biomat.com/tutorials/experimental-methods/m05/
Language: zh-CN

从固定长度下的力下降，读懂分子重排、加载时间、松弛谱与细胞周围的持续阻力。

## 长度没有变，为什么手里的拉力在变

把一条柔软的弹性带拉长后保持双手不动，最初绷紧的感觉可能逐渐减轻。固定在一个间隙里的密封垫、贴在活动皮肤上的敷料，以及包围细胞的水凝胶，都可能遇到类似问题：外部形状暂时保持不变，内部承担的力却随着时间重新分配。应力松弛实验就是把这种变化变成可测量的时间曲线。它关心材料在达到规定形变后，多久减小抵抗、最后还保留多少抵抗，以及这些变化是否会影响接触压力、固定效果或细胞周围的力学环境。

这与把重物挂在材料上观察它越拉越长的实验不同。挂着固定重物时，保持的是力，增加的是形变，称为蠕变；应力松弛则保持形变，观察力减小。二者都涉及时间，但实验仪器替材料约束了不同的量。可以把前者想成保持拉扯力度，看看材料会走多远；后者则像把门拉到固定位置，看看维持这个位置还需要多大力。明确哪个量由机器控制，哪个量由材料响应，是理解后面曲线和公式的起点。

松弛也不等于样品已经断裂。高分子链段可以改变构象，暂时性的连接可以解开并重新结合，含水网络中的液体也可以迁移。这些过程可能让原先集中的应力逐渐重新分配，而材料仍然连在一起。相反，夹具滑移、温度变化或样品缓慢失水，也能使测得的力改变。实验的任务是把力的变化与真实形变、环境及结构变化联系起来，从而判断是哪一种过程在主导响应。

本章用一条均匀受拉的小变形试样建立计算。应力是拉力除以原始截面积，应变是标距内的长度增加除以原始标距。两者把试样大小的影响从材料响应中分离出来。例如原始长度二十毫米，拉长零点四毫米，应变就是百分之二；截面积十平方毫米、拉力零点零一八牛顿，对应一点八千帕应力。计算中的百分之二写成零点零二，千帕和平方毫米相乘转成牛顿时还需要千分之一的单位换算。

$$
\sigma=\frac{F}{A_0},\qquad\varepsilon=\frac{L-L_0}{L_0},\qquad E_{\mathrm{rel}}(t)=\frac{\sigma(t)}{\varepsilon_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 名义拉应力，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 拉力，N。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | 原始截面积，m²。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 当前标距长度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | 原始标距长度，m。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d392a7d1ae884b61e2eb5f45.svg) | 线性应力松弛模量，Pa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从理想应变阶跃开始计时，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 施加并保持的阶跃应变，无量纲。 |

均匀单轴、小变形；松弛模量定义对应无应力初始状态和理想阶跃，有限加载需使用实际历史。L0=20 mm、L=20.4 mm给出应变0.02；F=0.018 N、A0=10 mm²给出1800 Pa，模量90 kPa。

“小变形”在这里是一种待检查的实验条件，并不是所有软材料都遵循同一个百分比界限。可以在一组较小应变下重复实验，观察应力除以应变后的曲线是否重合；如果曲线随应变大小系统变化，就应把形变幅值也作为材料响应的一部分来研究。本章构造数据直接采用线性模型，使加载历史与时间尺度的作用能够被单独看清；真实实验则需要先完成这种幅值检查，再选择相应的分析模型。

## 从气体里的分子运动，到会慢慢回缩的弹簧

理解松弛有一条很有启发性的历史路径。Maxwell在一八六七年发表的气体动力学研究中，讨论了微观运动怎样联系到宏观应力等量，有限的响应时间也进入了这一思路。后来用于粘弹性分析的Maxwell模型，把能够储存能量的弹性响应和随时间发生的流动放在同一条承载路径上。这个联系说明，材料的状态不仅由“现在拉了多长”决定，还可能与此前怎样拉到这里有关。图中画的是帮助理解这条思路的现代力学类比，并不是历史仪器的复原图。

先看一根弹簧。拉长越多，它的回拉力越大；若长度固定，理想弹簧的力也保持不变。再看一个内部充有黏性液体的活塞装置，常称为阻尼器或黏壶。它抵抗的是运动速度：推得越快，需要的力越大；停止相对运动以后，理想黏壶不靠位置本身维持一个弹性力。把两者首尾相接，就像给一根弹簧接上一段可以缓慢移动的支撑。在总长度固定时，黏壶逐渐伸长，弹簧可以回缩，因此整条支路的拉力逐渐下降。

这个过程为什么会得到指数函数，可以先不做积分。串联元件承担同一应力，总应变等于两部分应变之和；保持总应变时，黏壶增加的那部分必须由弹簧减少的部分补偿。应力越大，黏壶流动越快，弹簧也回缩越快；应力减小后，变化又随之放慢。因此每过相同的一小段时间，减少的量与当时剩下的应力成比例。反复按同一比例减小，就得到指数衰减，而不是每秒都减去相同的固定数值。

$$
\dot\sigma+\frac{\sigma}{\tau}=E\dot\varepsilon,\qquad\tau=\frac{\eta}{E},\qquad\sigma(t)=\sigma(0)e^{-t/\tau}\quad(\dot\varepsilon=0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 单条Maxwell支路应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e6fee55eb022e9924b6563.svg) | 应力对时间的变化率，kPa/s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 该支路弹簧模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 该支路总应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f89ba6efd1616ab8c8ae4551.svg) | 总应变变化率，s⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 黏壶黏性系数，kPa·s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 该支路松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 保持阶段已经过的时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5d675645d5125886ba434eba.svg) | 保持开始时的支路应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底，无量纲。 |

串联元件应力相同、应变相加；保持时弹簧回缩补偿黏壶伸长。η=80 kPa·s、E=40 kPa给出τ=2 s；初始支路应力0.8 kPa经过2 s剩0.294304 kPa。

时间常数把这种快慢压缩成一个有物理含义的量。当经过一个时间常数时，这条支路的应力保留最初的约百分之三十七；经过三个时间常数时，约剩百分之五。这里说的是可松弛支路的应力，而不是整个试样包括长期承载部分在内的总应力。若黏性系数为八十千帕秒，支路弹性模量为四十千帕，时间常数就是两秒。黏性系数增大意味着移动更慢，时间常数随之增大；弹簧更强而黏性相同，则它推动内部重新分配的能力更强，时间常数减小。

![原创历史与模型示意：1867年Maxwell研究中的微观运动与宏观响应问题；现代弹簧–黏壶串联类比及具有长期分支的并联系统。图示不是分子结构，也不是历史仪器复原。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/227a2eb5e39c1561435bb60f.svg?v=227a2eb5e39c)

图 1原创历史与模型示意：1867年Maxwell研究中的微观运动与宏观响应问题；现代弹簧–黏壶串联类比及具有长期分支的并联系统。图示不是分子结构，也不是历史仪器复原。

单独一条Maxwell支路最终会把应力完全释放，而很多交联材料仍能长期承担载荷。为表达这部分响应，可以再并联一根弹簧：各支路经历同样的总应变，它们承担的应力相加。若存在快慢不同的过程，再加入不同时间常数的支路。图里的三条路径分别表示长期承载、较快松弛和较慢松弛。这些元件是描述力学响应的工具，一个拟合出来的黏壶不自动对应一种具体化学键；把时间常数归到某种分子过程，还需要温度、化学结构或独立结构测量提供联系。

## 让一条下降曲线说清楚：下降多少，下降多快

设想仪器能够瞬间把应变从零变成百分之二，之后保持不变。刚开始时，每条Maxwell支路中的弹簧都来得及承载，而黏壶还没有明显移动，所以最初模量等于所有弹性模量之和。保持足够久以后，可松弛支路的贡献逐渐消失，留下长期弹簧的模量。中间的曲线由各个衰减过程叠加。这样，曲线的高度差描述可重新分配的承载份额，横向的时间尺度描述重新分配发生得有多快。

$$
E(t)=E_\infty+\sum_{i=1}^{2}E_i e^{-t/\tau_i},\quad\sigma_{\mathrm{step}}(t)=\varepsilon_0E(t),\quad E_0=E_\infty+E_1+E_2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fff42b0e3f57a0075d95d7d8.svg) | 理想阶跃下的松弛模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | 长期平衡模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Maxwell支路编号1或2，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/25faaa3257b422e0c57c5010.svg) | 第i条支路弹簧模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8f98758746427e2aa1a5880.svg) | 第i条支路松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 阶跃施加后时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1bd58ca256010ed07317aabf.svg) | 阶跃响应应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 保持的阶跃应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | 瞬时模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/de4ed77abe73974794d51c59.svg) | 两条Maxwell支路的弹簧模量，kPa。 |

并联支路承受相同应变，应力相加；参数为恒定温度下的线性模型。E∞=20、E1=40、E2=30 kPa，τ1=2、τ2=40 s，ε0=0.02给出E0=90 kPa、初始应力1.8 kPa、长期0.4 kPa。

本章设定长期模量二十千帕，快支路四十千帕、时间常数两秒，慢支路三十千帕、时间常数四十秒。于是理想瞬时模量为九十千帕，百分之二应变下的初始应力为一点八千帕；充分松弛后的应力是零点四千帕。两秒时，快支路已经明显衰减，慢支路却大多保留。把快过程和慢过程分别画出来，可以看出曲线在开始时变化很快、之后拖着一条长尾的原因，而不必把长尾理解为仪器迟迟没有完成动作。

对数时间轴有助于同时观察两秒和四十秒这样的不同尺度。在线性轴上，开始的一小段变化容易被几百秒的总时长挤到边缘；对数轴则给每一个十倍时间区间相近的宽度。图中包含零时刻的曲线使用近零处线性、稍远处对数的坐标，以保留加载结束这个事件。读图时仍应看清坐标标签：横向相同距离可能代表时间乘以十，而不是增加相同的秒数。拟合程序读取真实时间数值，并不会因为改变了显示坐标就改变物理模型。

实验中常把应力除以初始应力，画成从一开始的归一化曲线，这便于比较衰减快慢，但会隐藏绝对承载能力。一个初始应力十千帕的材料和一个一千帕的材料，都可能在一分钟后保留一半，两者仍承担很不一样的力。应保留原始应力图，并说明归一化分母取理想阶跃起点、实际加载峰值，还是某个指定时间。只改变这个分母，就可能让同一条记录表现出不同的“松弛比例”。

半衰减时间也要先明确对象。如果总应力最终平台高于初始应力的一半，曲线永远不会穿过“总应力减半”的水平线；但可松弛部分仍然可以减半。对于只有一条可松弛支路的模型，减去长期平台后，该支路减半需要约零点六九三个时间常数。存在多个过程时，半衰减时间是它们共同作用的结果。它可以作为一个明确条件下的比较指标，却不能直接替代每条支路的时间常数。

## 仪器拉到目标长度之前，材料已经开始变化

真实仪器没有无限大的速度。达到同样百分之二应变，可能需要一秒，也可能需要二十秒；这段逐渐增加应变的过程称为加载斜坡。对于两秒就明显松弛的支路，二十秒加载期间已经发生了大量重新分配。等机器宣布进入保持阶段时，快支路的应力已经远小于理想瞬时加载的值。若只保存保持阶段，再把第一个力值当成材料的瞬时响应，就会把加载过程中已经消失的那部分信息漏掉。

计算有限加载的响应，可以把斜坡想成连续增加的一小步一小步形变。较早施加的小步已经松弛较久，刚施加的小步还保留较多应力；把它们在当前时刻的贡献相加，就得到整个响应。这也是线性叠加的含义。对于恒定应变速率，求和可以写成积分并得到下面的表达式。公式中的两个时间要分清：加载时间从开始拉伸计时，保持时间从达到目标应变计时。把二者混成同一个零点，会改变对峰值和早期衰减的解释。

$$
\varepsilon(t)=\varepsilon_0\min(t/t_r,1),\quad\sigma(t)=E_\infty\varepsilon(t)+\sum_{i=1}^{2}\sigma_i(t),\qquad\sigma_i(t)=\begin{cases}E_i\varepsilon_0\frac{\tau_i}{t_r}(1-e^{-t/\tau_i})&0\leq t\leq t_r\\ E_i\varepsilon_0\frac{\tau_i}{t_r}(1-e^{-t_r/\tau_i})e^{-(t-t_r)/\tau_i}&t\geq t_r\end{cases}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 当前工程应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 最终目标应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 从加载开始计时，s，t≥0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ce7b3f4467a12e80e6af8d40.svg) | 恒速加载斜坡持续时间，s，正值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a05d6e83f4c2e8f52c235d7.svg) | 取括号内较小的数，达到目标后不再增加应变。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | 总名义应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | 长期弹簧模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 支路编号1或2。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d11eec53e2e8f271603794c.svg) | 第i条Maxwell支路应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/25faaa3257b422e0c57c5010.svg) | 第i条支路弹簧模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8f98758746427e2aa1a5880.svg) | 第i条支路松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底。 |

从无应力状态恒速加载，再保持最终应变；积分每个小应变增量的后续衰减。沿用20/40/30 kPa与2/40 s参数，ε0=0.02；tr=1 s峰值1.622113 kPa，tr=20 s峰值0.952160 kPa。第二行时间t−tr才是保持时间。

代入本章参数，一秒加载的峰值约为一点六二二千帕，二十秒加载的峰值约为零点九五二千帕，尽管两次实验最终都停在百分之二应变。对二十秒加载，快支路到保持开始时只剩约四千帕的表观模量贡献，而它在模型中的原始弹性模量是四十千帕。慢支路的表观贡献约为二十三点六一千帕。长期分支仍为二十千帕，因此直接用峰值除以应变，只得到约四十七点六一千帕，而不是九十千帕。

![同样2%目标应变，两种加载时长产生不同峰值。中图的时间都从加载开始计算；底图则从20 s斜坡结束计时，分解长期、快与慢支路的承载。数值均为指定模型计算。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d630b492bdaef7affadc820c.svg?v=d630b492bdae)

图 2同样2%目标应变，两种加载时长产生不同峰值。中图的时间都从加载开始计算；底图则从20 s斜坡结束计时，分解长期、快与慢支路的承载。数值均为指定模型计算。

这个结果还有一个容易误判的细节：在这里的线性模型和准确的恒速斜坡下，进入保持阶段以后，每条支路仍然按原来的时间常数衰减。斜坡改变了保持起点的幅值，并没有把两秒自动变成另一个物理时间常数。因此，用两个指数拟合理想的保持曲线，可能仍然得到接近正确的两个时间常数，却低估支路模量。若快过程已经衰减到噪声以下，或者实际加载存在过冲，时间常数的识别也会变得困难。应分别考虑幅值被削弱和信息难以识别这两件事。

实验上应同步保存力、局部应变和时间，而不仅保留机器设定值。快速加载可能带来惯性振荡，过慢加载则会隐藏快速过程；选择加载速度是在仪器动态能力与材料时间尺度之间寻找可解释的范围。先用已知弹性响应的参照样品检查加载形状，再用不同加载时长重复目标材料，可以帮助区分仪器变化和材料变化。若实际应变曲线并非直线斜坡，可以直接把记录下来的历史作为模型输入，逐时间步计算各支路，而不必强行把它压成一条理想直线。

## 让力的变化有明确含义

对于拉伸松弛，最直接的仪器配置包括驱动夹具、力传感器，以及测量试样中部形变的装置。固定横梁位置不一定等于固定试样标距长度：机器和夹具也会变形，夹持区还可能滑动。材料的力下降时，机器自身的弹性变形会相应恢复，实际试样长度可能继续变化。用标记点或引伸计记录局部应变，可以检查保持阶段是否真的保持了所讨论的量。若保持的是压头位移，解释则还要结合压缩接触、摩擦和样品几何。

试样的初始状态也属于加载历史。预拉伸、反复预处理、在液体里浸泡多久，以及从上一次实验恢复了多久，都会影响开始时是否接近无应力状态。本章模型从静置无应力状态起算，实验若有明显预载，就应将预载及其保持时间记录下来。预载有助于去除夹持松弛，却也可能让快过程在正式测量前已经发生。与其把每次试验开头手动移到同一高度，不如说明零点、预载和等待过程怎样定义。

温度和水分尤其值得同步关注。软材料放置几百秒后可能逐渐失水，温度尚未稳定的传感器也可能出现基线漂移。这些变化常落在“慢松弛”所在的同一时间范围。可以记录环境温度、采用合适的液体池或湿度控制，并在相同时间尺度下观察空载或稳定参照的基线。若长尾的量级与基线漂移相近，改善环境与力分辨率会比增加指数项更有帮助。液体池中还应考虑浮力、表面接触及装夹引入的附加力。

采样安排应围绕时间尺度，而不只是追求很长的数据表。要识别两秒过程，就要在加载附近留下足够密集的时间点；要识别四十秒过程和长期平台，就要把保持阶段延伸到相应范围。本章把早期密集记录与后期较稀疏记录结合。拟合时若把每个点赋予相同权重，采样特别密集的区段会拥有更大影响，因此采样规则与权重应一起考虑。噪声随时间变化或各次实验精度不同时，可以根据明确的测量不确定度安排权重。

含水凝胶还可能同时出现网络粘弹性和液体迁移。改变试样尺寸、排液边界与加载方式，可以帮助比较二者：与内部结构重排相关的材料时间尺度，和由排液距离决定的扩散时间尺度，可能呈现不同的尺寸依赖。不能只凭一条指数曲线的形状就给它命名为某一种分子反应。若厚度变化明显改变松弛速度，应进一步检查孔弹性或传质模型；若温度与化学结构变化影响更突出，则可以围绕链段运动或可逆连接继续设计实验。

## 拟合应当回答什么，曲线又能提供多少信息

下面的计算构造一秒和二十秒两种加载记录，并加入已知幅度的小噪声。两次实验共享同一组材料参数，拟合时同时使用加载阶段与保持阶段。这样，快速加载保留下来的快过程信息，可以补充慢加载中被削弱的幅值；较长保持阶段则帮助确定慢过程和长期平台。程序并不是给两条曲线分别找最漂亮的线，而是在检查一套参数能否解释两种已知的输入历史。结果还保留了每个点的观测值、拟合值和差值。

残差图把“观测减去拟合”的差值按时间展示出来。如果差值在零附近随机分布，其量级接近测量噪声，模型在这组记录中已经解释了主要时间趋势；如果加载结束附近出现连续同号的偏差，或者长尾一直向同一方向弯曲，就应检查时间零点、实际应变历史、基线或遗漏过程。一个很小的总误差会把这些局部结构平均掉。保留残差图，能够让读者看到哪里符合得好、哪里需要更具体的解释。

![构造数据的有限加载联合拟合、残差、支路幅值和时间窗口比较。c图的保持段阶跃拟合低估原始支路模量；d图的两个模型初始模量相同，但长期平台不同。点为构造观测，线为相应模型。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/91748c1acb2727f5997d5223.svg?v=91748c1acb27)

图 3构造数据的有限加载联合拟合、残差、支路幅值和时间窗口比较。c图的保持段阶跃拟合低估原始支路模量；d图的两个模型初始模量相同，但长期平台不同。点为构造观测，线为相应模型。

图中的表观模量比较特意采用同一段二十秒加载后的保持记录。正确模型知道应变用了二十秒才达到目标；另一种处理把保持开始当成瞬时阶跃。后者得到的支路幅值接近有限加载后的剩余贡献，而不是原始弹性模量。把两种结果并排显示，就能看出数据处理假设怎样改变参数含义。这里无需把一切偏差都归为“拟合失败”：一个数值拟合可以非常贴合曲线，同时回答了与研究者原先想问的不同问题。

长期平台还有时间窗口的问题。图中另一组参数具有相同初始模量和相近的早期变化，却在长时间后趋向不同平台。只观察前五秒，很难区分这种差别；把保持延长到几百秒，差异才逐渐展开。若研究真正关心几小时后还能保持多少接触压力，几秒钟的数据就需要补上更长时间的观察。增加支路数并不能凭空创造未测量的长期信息，反而可能让多个参数互相补偿。实验时长与目标用途应一起确定。

独立试样之间的差异也应与单条曲线的噪声区分。一个试样采集一千个时间点，并不等于测了一个千样本的材料群体。可以先分别拟合多个试样，检查初始模量、平台和时间尺度的分布，再报告批次差异；需要评估参数不确定度时，也应围绕独立试样或合理的相关噪声结构重采样。时间点之间存在相关性时，逐点随机打乱会破坏原始记录的结构，得到过于乐观的精度印象。

## 同一种材料，换一种控制方式会得到另一条时间曲线

为了比较松弛和蠕变，先把模型简化成长期弹簧二十千帕，并联一条四十千帕、松弛时间两秒的Maxwell支路。做松弛实验时，总应变保持不变，应力从全部支路承载逐渐过渡到长期弹簧承载。做蠕变实验时，总应力保持不变，快支路逐渐释放的承载必须转移给长期弹簧，因此总应变会继续增加。两种实验改变的不只是纵坐标名称，内部应力重新分配所受到的约束也改变了。

$$
J(t)=\frac{\varepsilon(t)}{\sigma_0}=\frac{1}{E_\infty}\left(1-\frac{E_1}{E_0}e^{-t/\tau_c}\right),\qquad E_0=E_\infty+E_1,\quad\tau_c=\tau\frac{E_0}{E_\infty}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | 单支路标准线性固体的蠕变柔量，kPa⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 理想应力阶跃后时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 当前应变，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | 施加并保持的应力，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | 长期弹簧模量，kPa，正值。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4527c7825889bcd00202ef22.svg) | 唯一Maxwell支路的弹簧模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | 此单支路模型的瞬时模量，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Maxwell支路松弛时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ba485d6196375f39459ba480.svg) | 固定应力实验中的蠕变迟滞时间，s。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底。 |

这是独立的单支路例子，不是前面双支路的直接代换。总应力恒定时，释放的支路载荷转移给平衡弹簧。E∞=20、E1=40 kPa，τ=2 s给出τc=6 s，J(2)=0.0261156 kPa⁻¹，而1/E(2)=0.0288058 kPa⁻¹。

这个单支路模型的蠕变特征时间为六秒，而松弛时间为两秒。二者的比值等于初始模量与长期模量之比，也就是三。两秒时，蠕变柔量约为零点零二六一二千帕的倒数；把同一时刻的松弛模量直接取倒数，得到约零点零二八八一，两者不同。在刚开始和足够久以后，两种实验分别回到相应的弹性极限，倒数关系才重新成立。中间时刻的差别，来自整个历史的参与，而不是简单的单位换算错误。

![独立单支路标准线性固体：E∞=20、E1=40 kPa、τ=2 s。固定应力下的蠕变柔量与松弛模量的逐点倒数在中间时刻不同，蠕变迟滞时间为6 s。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c2be50ad2248af6430746f3a.svg?v=c2be50ad2248)

图 4独立单支路标准线性固体：E∞=20、E1=40 kPa、τ=2 s。固定应力下的蠕变柔量与松弛模量的逐点倒数在中间时刻不同，蠕变迟滞时间为6 s。

因此，若实验室已经有应力松弛数据，想预测固定载荷下的长期变形，需要先用相应模型或历史关系转换，再与蠕变实验比较。直接把整条模量曲线逐点倒过来，会得到错误的中间响应。对于多支路材料，转换涉及多个耦合过程，通常适合用数值方法完成。重要的是先明确输入历史，随后计算响应，而不是把同一时刻的两个量当成静态弹簧那样互相除一下。

这也解释了为何两种实验值得配合使用。某个模型若能同时解释固定应变下的力下降和固定力下的形变增加，其参数含义会更明确；如果两种实验只能用互不相容的参数解释，就应检查样品状态、形变范围、几何和控制质量。实际使用条件若包含持续载荷与位移约束的交替，则还需要把完整历史接入模型。材料没有在切换仪器模式时忘记先前经历过的加载。

## 从一条松弛曲线走向材料与细胞的时间问题

应力松弛在生物材料研究中引出的一个问题是：细胞周围两种材料初始一样硬，细胞随后感受到的阻力也一样吗？细胞会通过黏附连接向周围网络施力，而连接后的网络可以持续抵抗，也可以逐渐重排。Chaudhuri等人在二〇一六年发表的海藻酸盐水凝胶研究，把松弛速度与初始模量、黏附配体密度等变量分别考虑，研究三维培养中的细胞行为。这个历史进展让“软硬”从单个初始数值扩展为随时间变化的环境特征。

这里的黏附配体，可以理解为细胞能够抓住的分子连接点。若材料更快地重新安排承载路径，细胞施力后周围阻力的持续方式就会改变；这种改变可能与细胞铺展和局部基质重塑有关。图中用同样初始模量、不同松弛时间的构造曲线说明这一比较，并用原创网络示意解释问题，不把曲线当成细胞实验结果。具体细胞类型、培养维度、配体呈递和降解条件，仍然是设计实际比较时需要匹配的变量。

![原创概念图：两种指定模型具有相同初始模量与长期模量，慢模型的两个时间常数均放大5倍。细胞与接点示意解释持续牵拉和网络重排，不是细胞实验图或形态预测。](https://ml-biomat.com/static/tutorials/experimental-methods/figures/245b04532110939b2cf72073.svg?v=245b04532110)

图 5原创概念图：两种指定模型具有相同初始模量与长期模量，慢模型的两个时间常数均放大5倍。细胞与接点示意解释持续牵拉和网络重排，不是细胞实验图或形态预测。

同样的思路也适用于密封与柔性器件。密封垫装入后几何被固定，工程上关心的是规定温度与时间后是否还保留足够接触压力；柔性支撑与组织相接触时，则可能希望减小持续压迫，同时保持必要的结构支撑。这里没有一个统一的“松弛越快越好”。先把需要维持的功能写成时间与力的要求，再选择初始模量、平台和时间尺度，材料设计才会从一条好看的下降曲线走向具体用途。

### 完整Python：有限加载、共同参数拟合与蠕变比较

两条独立构造记录共享一套模型参数；保存原始量、拟合值、残差和单支路蠕变结果。

```
"""Stress relaxation with measured finite ramps and a generalized Maxwell model.
All numerical records are constructed teaching data, with fixed random seed.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

PARAM=np.array([20.,40.,30.,2.,40.])  # kPa,kPa,kPa,s,s
EPS=.02
def response(t,ramp,q=PARAM,eps=EPS):
    """Uniaxial stress in kPa from initially unstressed material, t in seconds."""
    t=np.asarray(t,dtype=float);Ein,E1,E2,tau1,tau2=q
    u=np.minimum(np.maximum(t,0),ramp);hold=np.maximum(t-ramp,0)
    strain=eps*u/ramp;stress=Ein*strain
    for modulus,tau in [(E1,tau1),(E2,tau2)]:
        stress=stress+modulus*eps*tau/ramp*(-np.expm1(-u/tau))*np.exp(-hold/tau)
    return stress
def step(t,q=PARAM):
    Ein,E1,E2,tau1,tau2=q;t=np.asarray(t)
    return Ein+E1*np.exp(-t/tau1)+E2*np.exp(-t/tau2)
def apparent(q,ramp):
    Ein,E1,E2,t1,t2=q
    return np.array([Ein,E1*t1/ramp*(-np.expm1(-ramp/t1)),E2*t2/ramp*(-np.expm1(-ramp/t2)),t1,t2])

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92';K='#18344a'
    def save(f,n):
        f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1905);records=[]
    for ramp in [1.,20.]:
        t=np.unique(np.r_[np.linspace(0,ramp,51),ramp+np.geomspace(.05,400,180)])
        true=response(t,ramp);obs=true+rng.normal(0,.003,len(t));records.append((ramp,t,true,obs))
    def residual(q):return np.concatenate([response(t,r,q)-y for r,t,truth,y in records])
    fit=least_squares(residual,[18,35,33,3,35],bounds=([.1,.1,.1,.1,10],[100,200,200,10,200]),xtol=1e-13,ftol=1e-13,gtol=1e-13);assert fit.success
    q=fit.x
    r,t,true,y=records[1];mask=t>=r;h=t[mask]-r
    naive=least_squares(lambda v:EPS*step(h,v)-y[mask],[20,4,24,2,40],bounds=([.1,.01,.01,.1,10],[100,200,200,10,200]),xtol=1e-13,ftol=1e-13,gtol=1e-13);assert naive.success
    tt=np.linspace(0,20,401)
    sol=solve_ivp(lambda time,s:np.array([40.,30.])*EPS/20-s/np.array([2.,40.]),[0,20],[0,0],t_eval=tt,rtol=1e-11,atol=1e-13)
    ode=20*EPS*tt/20+sol.y.sum(axis=0);ode_error=float(np.max(np.abs(ode-response(tt,20))))
    # F1: original conceptual history and a matched mechanical network.
    f,ax=plt.subplots(1,3,figsize=(14,5),layout='constrained')
    for aa in ax:aa.set(xlim=(0,10),ylim=(0,10));aa.axis('off')
    ax[0].set_title(tr('a  1867：响应需要时间','a  1867: response takes time'))
    ax[0].add_patch(Rectangle((1,3),8,4,fill=False,ec=B,lw=2))
    for x,y,dx,dy in [(2,4,.8,.4),(4,5,-.7,.8),(6,4.3,.6,-.5),(8,6,-.8,-.4),(3,6,.6,.4),(7,5.8,-.7,-.8)]:
        ax[0].add_patch(Circle((x,y),.19,color=G));ax[0].annotate('',(x+dx,y+dy),(x,y),arrowprops={'arrowstyle':'->','color':G})
    ax[0].text(5,2,tr('Maxwell的气体动力学问题','Maxwell’s gas-dynamics question'),ha='center',fontsize=11)
    ax[0].text(5,1.2,tr('分子运动与宏观应力的联系','Molecular motion and macroscopic stress'),ha='center',fontsize=10)
    def spring(aa,x0,x1,y,color=B):
        x=np.linspace(x0+.18,x1-.18,13);ys=y+np.r_[0,np.tile([.35,-.35],5),.35,0]
        aa.plot([x0,x0+.18],[y,y],color=color,lw=2);aa.plot(x,ys,color=color,lw=2);aa.plot([x1-.18,x1],[y,y],color=color,lw=2)
    def dash(aa,x0,x1,y):
        aa.plot([x0,x0+.3],[y,y],color=G,lw=2)
        aa.plot([x1-.3,x0+.3,x0+.3,x1-.3],[y+.4,y+.4,y-.4,y-.4],color=G,lw=2)
        aa.plot([x1-.8,x1-.8],[y-.3,y+.3],color=G,lw=2);aa.plot([x1-.8,x1],[y,y],color=G,lw=2)
    ax[1].set_title(tr('b  串联：形变可以重新分配','b  Series: deformation can redistribute'))
    spring(ax[1],1,4,5);dash(ax[1],4,8.5,5)
    ax[1].text(2.5,6.2,'E',ha='center');ax[1].text(6.2,6.2,'η',ha='center')
    ax[1].text(5,3.5,tr('总伸长固定，弹簧逐渐回缩','Fixed total extension; spring recoils'),ha='center',fontsize=10)
    ax[1].text(5,2.5,'τ = η / E',ha='center',fontsize=15)
    ax[2].set_title(tr('c  并联：不同时间尺度分担载荷','c  Parallel: several load-bearing timescales'))
    ax[2].plot([1,1],[2.5,7.5],color=K,lw=2);ax[2].plot([9,9],[2.5,7.5],color=K,lw=2)
    spring(ax[2],1,9,7.5);spring(ax[2],1,4,5);dash(ax[2],4,9,5);spring(ax[2],1,4,2.5);dash(ax[2],4,9,2.5)
    ax[2].text(5,8.4,'E∞ = 20 kPa',ha='center');ax[2].text(5,5.9,'E₁ = 40 kPa, τ₁ = 2 s',ha='center',fontsize=10);ax[2].text(5,3.4,'E₂ = 30 kPa, τ₂ = 40 s',ha='center',fontsize=10)
    ax[2].text(5,.9,tr('现代力学类比；不是分子结构图','Modern mechanical analogy, not molecular structure'),ha='center',fontsize=9)
    save(f,'history')
    # F2: measured input and resulting load are inseparable.
    f,ax=plt.subplots(3,1,figsize=(11,10),layout='constrained');ts=np.linspace(0,100,1501)
    for ramp,c in [(1,B),(20,O)]:
        lab=tr('加载','Ramp')+f' {ramp:g} s';ax[0].plot(ts,100*EPS*np.minimum(ts/ramp,1),color=c,label=lab)
        ax[1].plot(ts,response(ts,ramp),color=c,label=lab)
    ax[0].set(xlabel=tr('从加载开始的时间 / s','Time from ramp start / s'),ylabel=tr('应变 / %','Strain / %'),xlim=(0,30));ax[0].legend()
    ax[1].plot(ts,EPS*step(ts),'--',color=G,label=tr('理想瞬时阶跃','Ideal instantaneous step'));ax[1].axhline(.4,color='#81939e',ls=':');ax[1].set(xlabel=tr('从加载开始的时间 / s','Time from ramp start / s'),ylabel=tr('应力 / kPa','Stress / kPa'));ax[1].legend()
    hold=np.linspace(0,120,600);app=apparent(PARAM,20)
    ax[2].stackplot(hold,np.full_like(hold,.4),EPS*app[1]*np.exp(-hold/2),EPS*app[2]*np.exp(-hold/40),colors=[G,B,O],alpha=.8,labels=[tr('长期分支','Equilibrium'),tr('快分支','Fast arm'),tr('慢分支','Slow arm')]);ax[2].set(xlabel=tr('20 s加载结束后的保持时间 / s','Hold time after the 20 s ramp / s'),ylabel=tr('应力分担 / kPa','Stress contributions / kPa'));ax[2].legend(loc='upper right',ncol=3)
    for aa,title in zip(ax,[tr('a  两次实验达到相同2%应变','a  Both experiments reach 2% strain'),tr('b  加载期间已经发生松弛','b  Relaxation starts during loading'),tr('c  保持阶段的不同承载路径','c  Load-bearing paths during the hold')]):aa.set_title(title,loc='left')
    save(f,'ramp')
    # F3: fitted results, residuals, and an exact explanation of apparent amplitudes.
    f,ax=plt.subplots(2,2,figsize=(13,9),layout='constrained')
    for r,t,true,y in records:
        c=B if r==1 else O;h=t-r;sel=h>=0;ax[0,0].scatter(h[sel],y[sel],s=9,color=c,alpha=.45);ax[0,0].plot(h[sel],response(t[sel],r,q),color=c,label=f'{r:g} s '+tr('加载','ramp'));ax[0,1].scatter(h[sel],(y-response(t,r,q))[sel]*1000,s=8,color=c,alpha=.55)
    ax[0,0].set_xscale('symlog',linthresh=.1);ax[0,1].set_xscale('symlog',linthresh=.1)
    ax[0,0].set(xlabel=tr('保持时间 / s','Hold time / s'),ylabel=tr('应力 / kPa','Stress / kPa'));ax[0,0].legend();ax[0,1].axhline(0,color=K,lw=1);ax[0,1].set(xlabel=tr('保持时间 / s','Hold time / s'),ylabel=tr('观测−拟合 / Pa','Observed − fitted / Pa'))
    ix=np.arange(3);ax[1,0].bar(ix-.24,PARAM[:3],.24,color=G,label=tr('指定模型','Specified'));ax[1,0].bar(ix,q[:3],.24,color=B,label=tr('有限加载联合拟合','Joint finite-ramp fit'));ax[1,0].bar(ix+.24,naive.x[:3],.24,color=O,label=tr('20 s保持段当作阶跃','20 s hold treated as a step'));ax[1,0].set(xticks=ix,xticklabels=['E∞','E₁','E₂'],ylabel=tr('分支模量 / kPa','Arm modulus / kPa'));ax[1,0].legend(fontsize=8.7)
    window=np.linspace(0,300,601);alt=np.array([5,40,45,2,60]);ax[1,1].plot(window,step(window),color=B,label='E∞=20, E₂=30, τ₂=40');ax[1,1].plot(window,step(window,alt),'--',color=P,label='E∞=5, E₂=45, τ₂=60');ax[1,1].axvspan(0,5,color=O,alpha=.2,label=tr('只观察前5 s','Only the first 5 s'));ax[1,1].set(xlabel=tr('理想阶跃后的时间 / s','Time after ideal step / s'),ylabel=tr('松弛模量 / kPa','Relaxation modulus / kPa'));ax[1,1].legend(fontsize=8.7)
    for aa,title in zip(ax.flat,[tr('a  两条输入历史共同识别模型','a  Joint fit to two input histories'),tr('b  残差保留时间结构供检查','b  Residuals reveal time structure'),tr('c  忽略加载会低估分支幅值','c  Ignoring the ramp suppresses amplitudes'),tr('d  短窗口看不清长期平台','d  A short window misses the plateau')]):aa.set_title(title,loc='left')
    save(f,'fit')
    # F4: an independent one-arm solid compares two controlled experiments.
    time=np.linspace(0,25,501);Er=20+40*np.exp(-time/2);J=(1-2/3*np.exp(-time/6))/20
    f,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained');ax[0].plot(time,Er,color=B);ax[0].axhline(20,color=G,ls=':');ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('松弛模量 / kPa','Relaxation modulus / kPa'),title=tr('a  保持应变：应力逐渐减小','a  Fixed strain: stress decreases'))
    ax[1].plot(time,J,color=G,label=tr('蠕变柔量 J(t)','Creep compliance J(t)'));ax[1].plot(time,1/Er,'--',color=O,label='1 / E(t)');ax[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('柔量 / kPa⁻¹','Compliance / kPa⁻¹'),title=tr('b  保持应力：时间尺度也改变','b  Fixed stress: the timescale changes'));ax[1].legend();save(f,'creep')
    # F5: original conceptual link to time-dependent cell environments, no cell measurements.
    f,ax=plt.subplots(1,3,figsize=(14,4.6),layout='constrained');bt=np.geomspace(.05,300,400)
    for factor,c,lab in [(1,B,tr('较快','Faster')),(5,P,tr('较慢','Slower'))]:
        bq=PARAM.copy();bq[3:]*=factor;ax[0].semilogx(bt,step(bt,bq)/90,color=c,label=lab)
    ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('归一化模量 E(t)/E(0)','Normalized modulus E(t)/E(0)'),title=tr('a  相同初始模量，不同持续阻力','a  Same initial modulus, different persistence'));ax[0].legend()
    for aa,title,col in [(ax[1],tr('b  细胞通过黏附点牵拉网络','b  A cell pulls through adhesions'),B),(ax[2],tr('c  接点重排改变周围的应力','c  Junction rearrangement changes stress'),P)]:
        aa.set(xlim=(-3,3),ylim=(-3,3),aspect='equal');aa.axis('off');aa.set_title(title,fontsize=11)
        theta=np.linspace(0,2*np.pi,60);aa.fill(.9*np.cos(theta),.55*np.sin(theta),color='#e4b6a3');aa.add_patch(Circle((0,0),.24,color='#9a6d91'))
        for ang in np.linspace(0,2*np.pi,9)[:-1]:
            x,y=2.5*np.cos(ang),2.5*np.sin(ang);cx,cy=.9*np.cos(ang),.55*np.sin(ang);mx,my=(x+cx)/2,(y+cy)/2
            if aa is ax[2]:mx+=.18*np.sin(3*ang);my+=.16*np.cos(2*ang)
            aa.plot([cx,mx,x],[cy,my,y],color=col,lw=1.8);aa.add_patch(Circle((mx,my),.09,fc=O));aa.annotate('',(cx*.82,cy*.82),(cx*1.6,cy*1.6),arrowprops={'arrowstyle':'->','color':K})
        aa.text(0,-2.9,tr('机制示意，非显微观测','Mechanistic sketch, not microscopy'),ha='center',fontsize=9)
    save(f,'biology')
    arr=np.concatenate([np.c_[np.full(len(t),r),t,EPS*np.minimum(t/r,1),true,y,response(t,r,q),y*.01] for r,t,true,y in records])
    np.savetxt(o/'data.csv',arr,delimiter=',',header='ramp_s,time_s,strain,true_stress_kPa,observed_stress_kPa,fitted_stress_kPa,observed_force_N',comments='')
    np.savetxt(o/'parameters.csv',np.c_[PARAM,q,naive.x],delimiter=',',header='specified,finite_ramp_fit,hold_as_step_fit',comments='')
    np.savetxt(o/'creep.csv',np.c_[time,Er,J,1/Er],delimiter=',',header='time_s,relaxation_kPa,creep_compliance_per_kPa,inverse_relaxation_per_kPa',comments='')
    app20=apparent(PARAM,20);out={'specified_E0_kPa':90.,'specified_Einf_kPa':20.,'step_initial_stress_kPa':1.8,'equilibrium_stress_kPa':.4,'ramp1_peak_kPa':float(response(1,1)),'ramp20_peak_kPa':float(response(20,20)),'ramp20_apparent_E1_kPa':float(app20[1]),'ramp20_apparent_E2_kPa':float(app20[2]),'ramp20_apparent_E0_kPa':float(app20[:3].sum()),'fit_Einf_kPa':float(q[0]),'fit_E1_kPa':float(q[1]),'fit_E2_kPa':float(q[2]),'fit_tau1_s':float(q[3]),'fit_tau2_s':float(q[4]),'naive_E0_kPa':float(naive.x[:3].sum()),'naive_tau1_s':float(naive.x[3]),'naive_tau2_s':float(naive.x[4]),'residual_rms_Pa':float(np.sqrt(np.mean(residual(q)**2))*1000),'ode_max_error_kPa':ode_error,'one_arm_retardation_s':6.,'one_arm_J_at2_per_kPa':float((1-2/3*np.exp(-2/6))/20),'one_arm_inverseE_at2_per_kPa':float(1/(20+40*np.exp(-1))),'force_at_equilibrium_N':.004}
    (o/'summary.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))
if __name__=='__main__':main()
```

完整程序从设定的两条加载历史生成数据，保存应变、应力和力的对应表，完成共同参数拟合，并输出上面的图。另一段独立的微分方程计算检查有限加载的解析表达式。替换成实测数据时，应保留加载前后连续的时间、实际局部应变和力，核对截面积及单位，再决定是否使用恒速斜坡公式。若应变历史变化较复杂，可以沿用支路微分方程，把每一个时刻的应变变化作为输入，而不是删掉加载段以后重新定义一个方便的零点。

交互实验把加载时长、快支路时间常数和观察时刻放在一起。先固定材料参数，把加载从一秒调到二十秒，观察峰值怎样变化；再固定加载时长，只改变快支路时间常数，观察同一台仪器能否保留这个过程的幅值。图中同时给出已完成加载的应变比例和当前应力，避免把“仍在拉伸”和“已经保持”混成同一状态。最后把观察时刻移向长时间，查看所有曲线如何趋向相同的长期承载水平。

## 交互：在加载期间发生了多少松弛

固定E∞=20、E₁=40、E₂=30 kPa，τ₂=40 s，目标应变2%。时间从开始加载计。改变加载时长和快过程，比较应变、应力与峰值。

[Figure: 应变和应力随时间变化](https://ml-biomat.com/tutorials/experimental-methods/m05/#M05-plot)

准备一项应力松弛研究时，可以沿着这条主线安排实验：先确定实际需要保持的形变与使用时间，测清真实加载历史，再检查幅值范围、环境和独立试样差异；用原始应力、归一化曲线和残差共同解释结果。若快过程看不清，改进加载与早期采样；若平台不明确，延长保持并控制漂移；若想把时间尺度对应到分子或液体迁移，增加温度、尺寸或结构的对照。每一步都围绕一个可观察的量展开，松弛曲线便能成为研究材料如何随时间承担任务的入口。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Royal Society — Maxwell’s other equations](https://royalsociety.org/blog/2015/09/maxwells-other-equations/)

   Maxwell1867年气体动力学与有限响应时间的历史联系。
2. [Roylance — Engineering Viscoelasticity](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/d173f95347f59d59dd9b7387ab4303e7_MIT3_11F99_visco.pdf)

   串并联力学模型、蠕变转换、恒速加载与历史叠加。

   MIT OpenCourseWare; reference only,
3. [Bower — Small-Strain Viscoelastic Materials](https://solidmechanics.org/Text/Chapter3_6/Chapter3_6.php)

   载荷历史、温度与松弛/蠕变定义。

   Public textbook reference; no figures reproduced.
4. [TA Instruments RH111 — Linear Viscoelastic Region in Creep and Stress Relaxation](https://www.tainstruments.com/applications-notes/determining-the-linear-viscoelastic-region-in-creep-and-stress-relaxation-tests/)

   用归一化曲线检查瞬态实验的线性幅值范围。

   Instrument application note; reference only.
5. [Chaudhuri et al. — Hydrogels with tunable stress relaxation regulate stem cell fate and activity](https://backoffice.biblio.ugent.be/download/8692536/8692544)

   2016年三维海藻酸盐细胞培养研究中分别设计初始模量与松弛。

   Public author manuscript; technical reference, no figures/data reproduced.
6. [Righi and Balbi — Foundations of viscoelasticity and application to soft tissues mechanics](https://arxiv.org/abs/2108.08078)

   从线性模型延伸到软组织非线性与有限斜坡的进阶阅读。

   Open preprint; reference only, no figures reproduced.
