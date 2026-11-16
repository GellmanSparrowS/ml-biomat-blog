# 如果改变选择，结果会怎样：因果推断与实验设计

Source: https://ml-biomat.com/tutorials/machine-learning/m08/
Language: zh-CN

从雨天带伞的反直觉比较，理解随机实验、观察调整、自然实验与样本量。

## 同一个人，如果没有领券，会怎样

一家商店发现领券顾客平均花的钱更多，于是准备扩大优惠券投放。这个决定看似顺理成章，却缺了一个比较：这些顾客如果没有领券，原本会花多少？常来店里的顾客更容易收到券，也可能本来就买得多；两组消费差异因此混合了优惠券作用与人群差异。预测模型可以利用领券信息猜测消费，但要决定是否继续发券，需要回答改变发券行为会怎样改变结果。

潜在结果把这个问题写得很直接：对同一个对象，分别设想接受处理与不接受处理时的结果。现实只显示其中一个，另一个是反事实。Neyman在1923年的农业试验研究中，用同一地块种植不同品种时的潜在产量组织比较；1990年的英译文保留了这种问题结构。地块、顾客或设备虽然不同，困难相同：无法让同一对象在同一时刻完整经历两个互斥条件，却希望估计两种条件的差异。

$$
Y_i=T_iY_i(1)+(1-T_i)Y_i(0),\quad \tau_i=Y_i(1)-Y_i(0),\quad \tau=\mathbb E[\tau_i]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e237eb39dd0ac5fddf41116f.svg) | 对象索引与0/1处理指示，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/47c4ee00ae1de0cd2e269513.svg) | 同一对象处理、未处理的潜在结果与实际观察结果，均为结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ed1b2a0aa311d96ecb05967c.svg) | 个体效应、目标总体平均效应与对该总体求期望，效应为结果单位。 |

若两潜在消费为12元和9元，效应为3元；分到处理时观察12元，分到对照时观察9元。等式使用处理一致性，并按设定处理版本解释。

本节使用明确生成的优惠券数据。六项处理前特征均在−2到2之间，其中第一项同时影响领券机会、原本的结果水平及优惠券效果。处理效应随第一特征变化，从接近0到接近2，总体平均效应为1个结果单位。模拟器保留两套潜在结果，估计器只读取每人实际分配条件下的一套。因此既能按实际研究流程计算，又能用模拟中的已知答案检查偏差来自哪里。

因果问题还要说明处理版本、对象范围、结果时间窗和人与人之间是否互相影响。给一张满减券与给一张无门槛券是不同处理，七天消费与当天消费是不同结果。若家庭成员共享券，一人的分配可能改变另一人的结果，需要以家庭为单位设计分配或建立干扰模型。明确这些对象与条件，才能把“平均提高多少”变成一个有确定含义的目标。

## 先把人群为什么不同画出来

下雨会让人更愿意带伞，也会增加淋湿机会，于是带伞与淋湿之间可能出现正相关，尽管伞在相同天气下提供保护。因果图画出雨天指向带伞、雨天指向淋湿，以及带伞指向淋湿三条关系。雨天是处理与结果的共同原因，形成一条后门路径。把相同天气条件下的带伞与未带伞者比较，再按目标人群的天气比例组合，可以去掉这个已知共同原因造成的人群组成差异。

$$
\mathbb E[Y\mid\operatorname{do}(T=t)]=\sum_x\mathbb E[Y\mid T=t,X=x]P(X=x)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3ba0d89b068fe27c0c672309.svg) | 结果、处理变量及设定的处理值；结果有其测量单位，处理为类别。 |
| ![Formula](https://ml-biomat.com/static/agent-math/93ff10e0b86ffafa9dd3c1c4.svg) | 足以阻断后门路径的处理前变量、其类别与目标总体比例；比例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8bf285eaef0939b34185f166.svg) | 条件均值、对类别求和与主动设置处理；求和公式用于离散X。 |

在图的调整条件、共同支持与一致性下，用目标人群比例组合分层均值。带伞后的雨天/晴天淋湿概率0.4/0.01与比例0.3/0.7给0.127；不带伞给0.3×0.9+0.7×0.02=0.284。

## 观察带伞者，还是为同一群人设置带伞

调整雨天比例、选择与保护机制。观察模式比较自行选择的人群；干预模式保留同一天气组成，切断雨天到带伞的入箭头。

[Figure: 因果图与两群体淋湿概率](https://ml-biomat.com/tutorials/machine-learning/m08/#M08-plot)

交互里的全部概率都是公开显示的教学设定。默认雨天比例30%，雨天带伞概率90%、晴天10%；同在雨天，带伞后淋湿概率从0.9降至0.4。直接观察带伞人群时，雨天在其中占比很高，淋湿率约0.320；未带伞者约0.060。若把带伞行为统一设置到同一目标人群，两种条件下淋湿率则为0.127和0.284，差为−0.157。观察与干预改变的不是同一件事，图中的人群组成和入箭头会随操作一起更新。

调整变量需要依据关系，不能把所有可见列都塞进模型。处理前的共同原因通常需要调整；处理后的中介位于作用路径上，调整它会改变所估计的效应。碰撞点则同时受到两端变量影响，例如技术能力和推荐关系都影响是否进入面试；只看进入面试的人，两个原本独立的因素可能产生关联。筛选样本、控制中介和处理混杂分别对应不同图结构，测量得更多也要知道每个变量处在什么位置。

![DoWhy公开例图，显示处理与结果及其他因果变量。](https://ml-biomat.com/static/tutorials/machine-learning/figures/d16bf35d97928117c6aae74d.png?v=d16bf35d9792)

图 1DoWhy原始因果图示例：逐条读取共同原因、工具、处理与结果的连接。图由PyWhy/DoWhy项目提供，MIT许可，未改编；英文节点保留原貌。

DoWhy的公开例图把共同原因、工具变量、处理和结果放在同一张图里，适合练习逐条解释箭头。图先承载关于机制的假设，再据此判断目标能否由现有数据识别，随后才选择估计方法。若一项共同原因没有被记录，可以设计新的测量或寻找另一种分配机制；换一个更强的回归器，无法自动补出那条缺失的信息关系。

## 随机分配怎样建立可比较的对照

随机实验让分配机制在设计上独立于处理前的潜在结果。足够重复的随机分配下，两组的人群差异平均抵消，组均值差便可以估计目标平均效应。某一次有限实验仍可能出现年龄、需求或基础表现不平衡，因此要保留分配记录、检查实施过程并计算不确定性。分层随机化可以在重要类别内分别分配，整群随机化则把家庭、班级或门店作为单位，后续标准误也要对应这个分配单位。

$$
\widehat\tau=\overline Y_1-\overline Y_0,\qquad \widehat{\operatorname{SE}}=\sqrt{s_1^2/n_1+s_0^2/n_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a62f35d39c75449fe5e10640.svg) | 估计效应与g组样本均值，g=0或1，结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ed135ab2bddd4999f47e8a94.svg) | 组内样本方差与独立对象数，分别为结果单位平方和计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e06a2e9c61e7893c25a5dab9.svg) | 独立两组均值差的估计标准误，结果单位。 |

随机独立组的均值方差相加。两组均值5和3、样本方差4和9、人数各100，效应2，标准误√0.13≈0.361。整群设计按分配单位另算方差。

公开研究可以把计数与效应尺度连接起来。1989年Physicians’ Health Study终报记录，随机分配阿司匹林组11037名男性医师中出现139例心肌梗死，安慰剂组11034人中出现239例。按这些汇总计数计算的原始事件比例约为每千人12.59和21.66，差约每千人−9.07，原始比例比约0.581。本节计算展示这项历史试验中两个随机分配组的原始比例；论文另有调整分析与随访信息，使用的统计量不同。

实际领用、坚持使用与最初分配也应分别记录。按随机分配比较得到的是意向处理效应，包含试验中实际出现的不依从情况；只挑出认真执行的人重新比较，会重新引入自选择。对于优惠券，分配、打开通知、领取和消费也组成一条过程链。先选择政策真正能够控制的动作，再说明评价是按分配者、领取者还是执行者进行，能避免把一个实验结果不知不觉换成人群不同的另一个问题。

## 匹配与加权，怎样重组观察数据

无法随机分配时，可以在已记录的处理前变量上寻找可比较对象。匹配为每位处理者寻找特征相近的对照，本例对前三项相关特征标准化后做最近邻匹配，允许一个对照被重复使用。最终平均的是处理者与其匹配对照的差，因此目标是已处理人群的平均效应ATT。若处理更容易分配给本来收益较高的人，ATT与全体人群ATE就不同；名称相似不意味着应把两者放在同一条真值线上比较。

倾向得分描述在处理前特征已知时，接受处理的概率。反概率加权让原本不容易接受处理却实际接受的人具有较大权重，也让不容易留在对照组却实际未接受的人具有较大权重，构造更可比较的加权人群。它需要目标人群各特征区域都有接受与不接受处理的可能，也需要已记录变量足以处理共同原因。某区域如果几乎只有处理者，巨大的权重会放大少数记录；可以缩小目标人群或补充对照，而不是让计算结果掩盖信息缺口。

$$
e_i=P(T_i=1\mid X_i),\qquad\widehat\tau_{\rm IPW}=\frac1n\sum_{i=1}^n\left[\frac{T_iY_i}{e_i}-\frac{(1-T_i)Y_i}{1-e_i}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/abc3f76f8225d9caf149a4a3.svg) | 对象索引、总人数、0/1处理、观察结果与处理前特征；结果带测量单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e6d27b68a3f1be1ab997a076.svg) | 给定特征的处理概率，0到1之间，无量纲；计算时用估计概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/30f485c2b5f41881b79cd1a9.svg) | 反概率加权的平均效应与对对象求和，效应为结果单位。 |

处理人群的出现概率e与权重1/e抵消，使其代表目标人群。四人中两处理结果4、6，两对照2、4，所有e=0.5时，(8+12−4−8)/4=2。识别需要一致性、条件可交换性与正值性。

![同一3000人样本的倾向重叠、六项特征平衡与ATE估计。虚线为生成总体ATE=1，AIPW横线为影响分数近似95%区间。](https://ml-biomat.com/static/tutorials/machine-learning/figures/bb2c0c0f02bf4ee47f3928d0.svg?v=bb2c0c0f02bf)

图 2同一3000人样本的倾向重叠、六项特征平衡与ATE估计。虚线为生成总体ATE=1，AIPW横线为影响分数近似95%区间。

3000条合成数据中，1490人被分配券、1510人未被分配。直接组均值差约2.249，普通IPW约0.979，按两组总权重分别归一化的Hájek估计约0.924。真实总体ATE为1。第一特征的绝对标准化均值差从约0.687降到0.0065，图中同时显示两组倾向分布与其他特征的平衡变化。这些检查针对已测量变量；共同原因是否完整，还要依靠数据生成知识、研究设计和后面的敏感性分析。

最近邻匹配得到ATT约1.226，而模拟中已处理样本的真实平均效应约1.204。它比全体ATE高，符合较高第一特征者更容易领券且更受益的设定。匹配后的样本数不等于独立对照数量，重复匹配会让同一对照影响多个差值，计算标准误时要处理这种依赖。本节保留匹配索引，供读者查看哪些对照被反复使用，而不把普通独立样本均值公式机械套到匹配差上。

## 预测模型怎样帮助估计因果效应

机器学习可以预测领券机会，也可以分别预测领券与未领券时的结果。因果估计将这些预测组织成特定的校正公式。AIPW先用两套结果模型给每人预测处理差异，再按照倾向得分加权实际结果与相应预测的残差。它因此结合了结果回归与加权两条信息。所谓双重稳健描述的是在适当条件下，其中一类辅助模型正确时仍能得到一致估计；有限样本中，两类模型误差和极端权重仍会影响精度。

$$
\widehat\tau_{\rm AIPW}=\frac1n\sum_i\left[\widehat m_1(X_i)-\widehat m_0(X_i)+\frac{T_i(Y_i-\widehat m_1(X_i))}{\widehat e_i}-\frac{(1-T_i)(Y_i-\widehat m_0(X_i))}{1-\widehat e_i}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/82967c0626fb473fc2c047fb.svg) | 对象索引、样本数、特征、0/1处理与观察结果。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2d470acda069ebd1f6d52cd3.svg) | 折外估计的t组条件结果均值与处理概率；前者为结果单位，后者无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4b2f5c53de0b7adc153583bf.svg) | 增广IPW平均效应与对全部对象求和；结果单位。 |

先预测差，再用观测残差校正。某处理者m1=5、m0=3、e=0.5、Y=6，其分数为2+(6−5)/0.5=4；平均所有分数得到估计。双重稳健是适当条件下的模型一致性性质。

交叉拟合让每条记录使用没有见过该记录结果的辅助模型预测。代码把数据分为五折，在其余四折训练倾向模型和结果模型，再预测留出的一折，最后拼回所有折外预测。由此得到AIPW约0.945，基于影响分数的近似95%区间约0.858到1.033。它在这次样本中没有比普通IPW更接近1；稳健性性质不是每次实验必然得到最小误差的保证。比较时应关注重复抽样表现及对辅助模型变化的敏感程度。

双重机器学习DML利用另一种正交化组织。先预测结果与处理各自在给定特征下的平均水平，把二者减去这些预测，再利用剩余处理变化解释剩余结果变化。代码将条件效应设为第一特征的线性函数，实际拟合得到截距约0.937、斜率约0.531，生成真值分别为1和0.5。总体第一特征均值为零，所以截距对应本例总体平均效应；如果目标人群的特征分布改变，平均效应也要重新对该人群求平均。

$$
\widetilde Y_i=Y_i-\widehat m(X_i),\quad \widetilde T_i=T_i-\widehat e(X_i),\quad\widehat{\boldsymbol\theta}=\arg\min_{\theta_0,\theta_1}\sum_i[\widetilde Y_i-\widetilde T_i(\theta_0+\theta_1X_{i0})]^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3caa0fc11feacec3e9107dc0.svg) | 对象索引、六维特征向量及第一个特征，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9cd0ac3ebae962df3781b107.svg) | 结果、处理、两者的折外条件均值与残差；Y相关量为结果单位，T相关量无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d5760dc4f1c7b29e4955d631.svg) | 条件效应的截距、斜率、二参数估计、取最小值参数与对象求和；此处特征无量纲，所以参数为结果单位。 |

条件均值先去掉可预测的背景。若残差T=0.4、X0=1且θ=(1,0.5)，残差结果预测为0.4×1.5=0.6。固定线性效应形式时，代码用两列残差设计矩阵最小二乘。

![左：真实与DML估计的条件效应。右：全体ATE与已处理人群ATT及各自目标；两根柱回答不同人群的问题。](https://ml-biomat.com/static/tutorials/machine-learning/figures/7e106c09143337ae0879403c.svg?v=7e106c091433)

图 3左：真实与DML估计的条件效应。右：全体ATE与已处理人群ATT及各自目标；两根柱回答不同人群的问题。

效应异质性研究的是哪些人因处理而改变得更多，不等同于哪些人的结果本来更高。一个原本消费很高、发券后几乎不变的顾客，与原本消费一般但对券反应很大的顾客，可能需要不同策略。估计条件平均效应也不意味着知道每个人的精确反事实，分组或个体预测需要相应的独立评价。先把估计人群、效应函数形式和验证方式说清，机器学习预测才有明确的因果用途。

## 工具变量借助另一种分配机会

假设是否参加培训受到个人积极性影响，积极性也影响后续表现，而且没有完整测量。研究者随机发送一封鼓励参加的通知，通知会改变参加概率，便可能作为工具变量。关键关系包括：通知确实影响参加，通知与潜在混杂独立，而且通知只能通过参加培训影响结果。若通知本身激励了学习，即使没有参加培训也改善表现，排除限制便不成立。工具变量的价值来自这组机制条件，不来自它与处理相关这一条统计事实。

$$
\widehat\tau_{\rm IV}=\frac{\overline Y_{Z=1}-\overline Y_{Z=0}}{\overline T_{Z=1}-\overline T_{Z=0}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b317ec89cfcc2f4f9f025e45.svg) | 二值工具、实际处理与结果；Z/T无量纲，Y为结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/92ff81cb81b642357084631d.svg) | 按工具组求得的结果均值与处理比例，z为0或1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e02ece28c9c8e3120f322e0f.svg) | Wald比值效应估计，为结果单位；分母为第一阶段差异。 |

若鼓励让结果提高0.6、处理率提高0.3，则比值为2。在独立性、排除、相关性及适当效应/单调性条件下赋予因果解释；较小分母会放大随机差异。

代码随机生成鼓励变量，同时让未观测积极性影响实际参加与结果。真实处理效应设为2。较强鼓励使参加率增加约0.284，Wald比值估计约2.340；较弱鼓励只改变约0.0238，估计变成约6.047。同一次有限样本里，随机鼓励两组仍有约0.0965的非处理结果差异，这项波动除以更小的第一阶段差异后被放大。因此，第一阶段强度是实质检查，弱工具问题也需要专门的不确定性方法。

处理效应在人群间不同时，二值工具在独立性、排除限制、相关性与单调性等条件下通常识别服从者的局部平均处理效应LATE。服从者指因鼓励而从不参加变为参加的人，不能直接从每人的单次记录完整识别。若鼓励让某些人更愿意参加、另一些人反而更不愿意参加，单调性假设就需要重新讨论。解释一个工具变量结果时，应把这类人群含义与数值一起交代。

## 利用时间变化或阈值附近的对照

某地区开始实施政策时，可以比较政策前后的变化，再减去未实施地区同期变化，这就是双重差分。它允许两地原本水平不同，关键条件是：如果没有政策，两地结果会有平行的变化趋势。代码给处理组设定较高初始水平，两组共同每期增长0.8，政策效应为3，计算得到双重差分约2.998。把两地水平直接相比，初始差异仍在；比较变化再相减，才消去稳定的组间差异。

$$
\widehat\tau_{\rm DiD}=(\overline Y_{1,\rm post}-\overline Y_{1,\rm pre})-(\overline Y_{0,\rm post}-\overline Y_{0,\rm pre})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2424bfc0d9d3e719fec7ec75.svg) | 组g=1处理或0对照、时期s=政策前pre或后post的结果均值；结果单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2bdddcb4db2b6c0ec4f34ca8.svg) | 两组变化之差的效应估计；结果单位。 |

处理组从10到15、对照从6到8，变化5−2=3。在无政策平行趋势等条件下消去共同变化与固定组差。代码前后各两期均值相隔两时间单位，额外每期0.7趋势产生1.4偏差。

![左：强弱工具对处理率的改变；中：平行与差异趋势下的四期组均值；右：阈值带宽0.4内的1624点与局部线性断点拟合。](https://ml-biomat.com/static/tutorials/machine-learning/figures/0381e800ec0da705feffa32f.svg?v=0381e800ec0d)

图 4左：强弱工具对处理率的改变；中：平行与差异趋势下的四期组均值；右：阈值带宽0.4内的1624点与局部线性断点拟合。

若处理组即使没有政策，也会每期额外增长0.7，同样计算得到约4.398，额外趋势被算进政策效应。处理前多个时期、预定安慰剂日期和制度背景可以帮助评估平行趋势是否合理。处理前曲线看起来平行，也不强制政策后的未处理趋势继续平行。多批次、错峰实施政策时，传统双向固定效应还可能混合不同群组和时间的效应，应明确每批次的对照与估计目标。

断点设计利用另一种局部对照：当评分达到阈值便获得资格，刚低于与刚高于阈值的对象可能十分接近，处理机会却突然变化。若未处理和已处理的潜在结果随评分在阈值附近连续，而且对象不能精确操纵自己跨过阈值，就能把结果的局部跳跃解释为阈值处的处理效应。代码生成一个真实跳跃1.5的例子，用阈值两侧的局部直线拟合；带宽0.4时使用1624点，估计跳跃约1.427。

把带宽改为0.2和0.8，结果约1.423和1.490。较小范围更贴近局部比较却样本较少，较大范围信息更多却更依赖函数形状。实际研究要检查评分密度、处理前变量是否也在阈值跳跃，以及是否有其他政策共用同一阈值。若资格只让接受处理的概率跳升，而非从0变成1，可采用模糊断点的比值思路。无论哪种形式，首先识别的是阈值附近人群的效应，扩展到远处需要额外结构。

## 把假设变化转成可检查的情景

处理前变量平衡、估计器复杂、样本量大，都不能替代关于共同原因的识别条件。敏感性分析把问题具体化：如果存在一个未测量因素，它同时影响分配与结果，需要多强才会明显改变估计？代码另外生成一个已知但暂时不提供给估计器的因素U，逐步增加它对结果的作用。真实处理效应固定为1，遗漏U时估计从约1.001升到3.392；把U纳入调整后，各情景估计约1.025。

![左：遗漏因素作用增强时，调整与遗漏它的回归效应；右：1989年终报的两随机组原始事件比例，柱顶保留事件数/分配人数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e57ccf601a0491b731b5f603.svg?v=e57ccf601a04)

图 5左：遗漏因素作用增强时，调整与遗漏它的回归效应；右：1989年终报的两随机组原始事件比例，柱顶保留事件数/分配人数。

这幅图中的U是模拟器公开生成的，用来说明机制，不是从现实资料中恢复的神秘变量。真实研究可以根据已有测量、外部资料或专家范围设定敏感性参数，并报告哪些范围会改变决策。安慰剂结果、处理前结果、虚假政策日期和负对照也能寻找与因果故事不相符的模式。例如政策出现前已经有“效果”，就要检查趋势、提前反应或时间对齐，而不是只换一个显著性阈值。

DoWhy把工作组织为建模、识别、估计和反驳检查。反驳检查通过某一项，表示该项扰动或已测试含义没有暴露相应问题；它能帮助排查，却不会凭数据自动确认所有未测量关系。更有用的记录方式是把每项检查连到一个假设与一个后续动作：补测哪类变量、扩大哪一段共同支持、检查哪一时期的趋势，或重新设计分配。这样，资料缺口会对应具体研究步骤。

## 开始实验前，先决定要看见多大的变化

如果当前转化率约10%，希望识别提高到12%的效果，差异是2个百分点，而不是2%的相对提升。样本量计算需要目标差异、基线比例、允许的一类错误率和所需功效。功效描述真实存在指定大小效果时，预先规定的检验能够检出的概率。本例采用独立对象、两组等量、双侧5%检验与80%功效的正态近似，得到每组约3841人。效果越小，需要的样本通常越多，图中用对数纵轴显示这一增长。

$$
n\approx\frac{[z_{1-\alpha/2}\sqrt{2\bar p(1-\bar p)}+z_{1-\beta}\sqrt{p_0(1-p_0)+p_1(1-p_1)}]^2}{(p_1-p_0)^2},\quad\bar p=(p_0+p_1)/2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6368178ee6d1c0d30add9a37.svg) | 每组独立对象数、对照与处理比例及二者平均；人数为计数，比例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1eb80413bb0a95188b8354e3.svg) | 双侧一类错误率、二类错误率与功效，均为概率。 |
| ![Formula](https://ml-biomat.com/static/agent-math/86b5d956b90b25e300aeff00.svg) | 标准正态分布q分位数，无量纲。 |

这是等组独立二项比例的正态近似设计。p0=0.10、p1=0.12、α=0.05、功效0.8，代入z≈1.960与0.842，向上取整3841人/组；整群或重复测量另用相应设计方差。

![左：基线10%、双侧5%检验、80%功效下的等组样本量，纵轴为对数；右：14天招募与额外7天结局观察窗。](https://ml-biomat.com/static/tutorials/machine-learning/figures/561429b8dc90fa95c0f076e7.svg?v=561429b8dc90)

图 6左：基线10%、双侧5%检验、80%功效下的等组样本量，纵轴为对数；右：14天招募与额外7天结局观察窗。

若每天有1000名新的合格对象，两组合计约7682人，纯数量需要8天。但转化可能随星期变化，方案将招募期预定为覆盖两周的14天；若结果定义为分配后七天内转化，最后一批对象还需等待七天，完整结果到第21天形成。样本数应按独立分配对象计，而不是把同一用户的反复访问当成新样本。整群分配、流失、重复观察和多指标选择，都需要相应调整计算与分析计划。

每天查看效果，看到一次显著便立即停止，会改变原先固定样本检验的错误率。需要提前选择固定样本方案，或使用有相应边界的序贯方法，并记录停止规则。把主要结果、分析人群、分配单位、处理版本、观察窗和最小有意义效应一并确定，实验才有明确终点。历史随机试验中的数据监测也属于设计的一部分，不能用随手重复检验替代正式的监测程序。

## 让每个估计值都对应一个可复述的问题

完整代码将优惠券的潜在结果、观察结果、折外预测、匹配索引和各设计结果保存在同一输出中。可以先固定生成机制比较估计器，再只改变一个识别条件，观察误差怎样出现。读数时始终同时问：这是哪个人群、哪种处理、哪个结果时间窗的效应；对照来自随机分配、已测量共同原因、工具、趋势还是阈值。一个数有了这些坐标，才可以用于下一步研究与决策。

### 完整实验：观察调整、DML、工具变量、DiD、RD与功效

运行python main.py --output results --language zh。数据由固定种子生成，另含公开终报的四个汇总计数。输出五组图、完整数组与summary.json；五折预测与匹配索引保留。

```
"""Causal designs with known synthetic effects and one public aggregate experiment."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.special import expit
from scipy.stats import norm
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def ols(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];r=y-X@b;s2=r@r/(len(y)-X.shape[1]);cov=s2*np.linalg.inv(X.T@X);return b,np.sqrt(np.diag(cov))

def crossfit(X,T,Y,seed=8):
 e=np.zeros(len(T));m0=np.zeros(len(T));m1=np.zeros(len(T));m=np.zeros(len(T));fold=np.zeros(len(T),int)
 for k,(train,test) in enumerate(StratifiedKFold(5,shuffle=True,random_state=seed).split(X,T)):
  prop=LogisticRegression(C=10,max_iter=1000).fit(X[train],T[train]);e[test]=prop.predict_proba(X[test])[:,1];fold[test]=k
  for group,dest in [(0,m0),(1,m1)]:
   ind=train[T[train]==group];model=HistGradientBoostingRegressor(max_iter=120,max_leaf_nodes=9,l2_regularization=2,random_state=seed).fit(X[ind],Y[ind]);dest[test]=model.predict(X[test])
  model=HistGradientBoostingRegressor(max_iter=120,max_leaf_nodes=9,l2_regularization=2,random_state=seed).fit(X[train],Y[train]);m[test]=model.predict(X[test])
 return e,m0,m1,m,fold

def n_per_arm(p0,p1,alpha=.05,power=.8):
 p=(p0+p1)/2;return float(((norm.ppf(1-alpha/2)*np.sqrt(2*p*(1-p))+norm.ppf(power)*np.sqrt(p0*(1-p0)+p1*(1-p1)))/(p1-p0))**2)

def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';L=lambda z,e:z if zh else e;rng=np.random.default_rng(8)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 n=3000;X=rng.uniform(-2,2,(n,6));true_e=expit(.6*X[:,0]-.4*X[:,1]);T=rng.binomial(1,true_e);tau=1+.5*X[:,0];noise=rng.normal(0,1,n);Y0=2+1.5*X[:,0]+X[:,1]**2+np.sin(X[:,2])+noise;Y1=Y0+tau;Y=np.where(T,Y1,Y0)
 e,m0,m1,m,fold=crossfit(X,T,Y);e=np.clip(e,.001,.999);phi=m1-m0+T*(Y-m1)/e-(1-T)*(Y-m0)/(1-e);aipw=float(phi.mean());aipw_se=float(phi.std(ddof=1)/np.sqrt(n));ipw=float(np.mean(T*Y/e-(1-T)*Y/(1-e)));hajek=float(np.sum(T*Y/e)/np.sum(T/e)-np.sum((1-T)*Y/(1-e))/np.sum((1-T)/(1-e)));naive=float(Y[T==1].mean()-Y[T==0].mean())
 residual_T=T-e;residual_Y=Y-m;design=np.c_[residual_T,residual_T*X[:,0]];dml=np.linalg.lstsq(design,residual_Y,rcond=None)[0];dml_ate=float(dml[0]);cate=dml[0]+dml[1]*X[:,0]
 # Nearest-neighbor matching with replacement estimates ATT for treated records.
 scaled=StandardScaler().fit_transform(X[:,:3]);treated=np.flatnonzero(T==1);controls=np.flatnonzero(T==0);nearest=NearestNeighbors(n_neighbors=1).fit(scaled[controls]).kneighbors(scaled[treated],return_distance=False)[:,0];matched=controls[nearest];att=float(np.mean(Y[treated]-Y[matched]));true_att=float(tau[treated].mean())
 def smd(weights):
  mean1=np.average(X[T==1],axis=0,weights=weights[T==1]);mean0=np.average(X[T==0],axis=0,weights=weights[T==0]);return (mean1-mean0)/np.sqrt((X[T==1].var(0,ddof=1)+X[T==0].var(0,ddof=1))/2)
 w=np.where(T==1,1/e,1/(1-e));before=smd(np.ones(n));after=smd(w)
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].hist(e[T==0],bins=25,alpha=.5,density=True,label=L('未分配券','No coupon'),color='#237b94');axs[0].hist(e[T==1],bins=25,alpha=.5,density=True,label=L('分配券','Coupon'),color='#d87430');axs[0].set(xlabel=L('折外倾向概率','Out-of-fold propensity'),ylabel=L('密度','Density'),title=L('两组的共同支持','Overlap between groups'));axs[0].legend(fontsize=9)
 axs[1].plot(abs(before),range(6),'o-',label=L('调整前','Before'));axs[1].plot(abs(after),range(6),'s-',label=L('IPW调整后','After IPW'));axs[1].axvline(.1,color='#aab7bf',ls=':');axs[1].set(yticks=range(6),yticklabels=[f'x{j}' for j in range(6)],xlabel=L('绝对标准化均值差','Absolute standardized mean difference'),title=L('观测变量的平衡','Balance of observed covariates'));axs[1].legend(fontsize=9)
 names=['Naive','IPW','Hajek','AIPW','DML'];vals=[naive,ipw,hajek,aipw,dml_ate];axs[2].barh(names,vals,color=['#aab7bf']+['#237b94']*4);axs[2].axvline(1,color='#d87430',ls='--',label=L('生成总体ATE=1','Generating population ATE=1'));axs[2].errorbar(aipw,3,xerr=1.96*aipw_se,fmt='none',color='#263744',capsize=4);axs[2].set(xlabel=L('结果单位的平均处理效应','Average treatment effect in outcome units'));axs[2].legend(fontsize=8);save(fig,'adjustment')
 fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');xx=np.linspace(-2,2,100);axs[0].plot(xx,1+.5*xx,color='#d87430',label=L('生成效应','Generating effect'));axs[0].plot(xx,dml[0]+dml[1]*xx,'--',color='#237b94',label=L('折外残差DML','Cross-fitted residual DML'));axs[0].set(xlabel='x0',ylabel=L('条件平均处理效应','Conditional average treatment effect'));axs[0].legend();axs[1].bar(['ATE','ATT'],[aipw,att],color=['#237b94','#609b6d']);axs[1].scatter([0,1],[1,true_att],marker='_',s=500,color='#d87430',linewidth=3,label=L('对应真实目标','Corresponding true target'));axs[1].set(ylabel=L('结果单位','Outcome units'),title=L('人群变了，目标也变了','A different population changes the target'));axs[1].legend(fontsize=9);save(fig,'heterogeneity')
 # Three distinct identification designs, each with an explicit known mechanism.
 N=4000;U=rng.normal(size=N);Z=rng.binomial(1,.5,N);eps=rng.normal(size=N);outcome_noise=rng.normal(size=N);iv={}
 for strength in [1.,.05]:
  treatment=(strength*Z+.8*U+eps>0).astype(int);outcome=2*treatment+U+outcome_noise;first=float(treatment[Z==1].mean()-treatment[Z==0].mean());reduced=float(outcome[Z==1].mean()-outcome[Z==0].mean());iv[str(strength)]={'first_stage':first,'reduced_form':reduced,'wald_effect':reduced/first}
 G=np.repeat([0,1],400);time=np.arange(-2,2);panel_noise=rng.normal(0,.5,(800,4));did={};panel={}
 for trend in [0.,.7]:
  yy=10+2*G[:,None]+.8*time[None,:]+3*G[:,None]*(time>=0)[None,:]+trend*G[:,None]*time[None,:]+panel_noise;means=np.array([yy[G==g].mean(0) for g in [0,1]]);effect=float((means[1,2:].mean()-means[1,:2].mean())-(means[0,2:].mean()-means[0,:2].mean()));did[str(trend)]=effect;panel[str(trend)]=means
 running=rng.uniform(-1,1,N);D=(running>=0).astype(int);outcome=1+2*running+1.5*D+rng.normal(0,.4,N);rd={}
 for bandwidth in [.2,.4,.8]:
  use=abs(running)<=bandwidth;rdX=np.c_[np.ones(use.sum()),running[use],D[use],running[use]*D[use]];b,se=ols(rdX,outcome[use]);rd[str(bandwidth)]={'n':int(use.sum()),'jump':float(b[2]),'se':float(se[2])}
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained');axs[0].bar([0,1],[iv['1.0']['first_stage'],iv['0.05']['first_stage']],color=['#237b94','#d87430']);axs[0].set(xticks=[0,1],xticklabels=[L('强鼓励','Strong encouragement'),L('弱鼓励','Weak encouragement')],ylabel=L('第一阶段处理率差','First-stage treatment-rate difference'));axs[0].set_title(L('工具变量先改变处理','Instrument first changes treatment'))
 for tr,style in [('0.0','-'),('0.7','--')]:
  for g,c in [(0,'#83949e'),(1,'#237b94')]:axs[1].plot(time,panel[tr][g],style+'o',color=c,label=(L('对照','Control') if g==0 else L('处理','Treated'))+f' trend={tr}')
 axs[1].axvline(-.5,color='#d87430',ls=':');axs[1].set(xlabel=L('时期','Period'),ylabel=L('平均结果','Mean outcome'),title=L('DiD与平行趋势','DiD and parallel trends'));axs[1].legend(fontsize=7)
 use=abs(running)<=.4;axs[2].scatter(running[use],outcome[use],s=5,c=np.where(D[use],'#d87430','#237b94'),alpha=.25);b,_=ols(np.c_[np.ones(use.sum()),running[use],D[use],running[use]*D[use]],outcome[use]);
 for side,interval in [(0,[-.4,0]),(1,[0,.4])]:
  rx=np.linspace(*interval,100);axs[2].plot(rx,b[0]+b[1]*rx+b[2]*side+b[3]*rx*side,color='#263744')
 axs[2].set(xlabel=L('运行变量距阈值','Running variable relative to cutoff'),ylabel=L('结果','Outcome'),title=L('RD：阈值附近的跳跃','RD: a jump near the cutoff'));save(fig,'designs')
 # Sensitivity demonstration: a generated omitted U is known to the simulator.
 Xs=rng.normal(size=3000);Us=rng.normal(size=3000);Ts=(.8*Xs+Us+rng.normal(size=3000)>0).astype(int);sn=rng.normal(size=3000);sens=[]
 for gamma in [0,.5,1,1.5,2]:
  ys=Ts+2*Xs+gamma*Us+sn;omit,_=ols(np.c_[np.ones(3000),Ts,Xs],ys);full,_=ols(np.c_[np.ones(3000),Ts,Xs,Us],ys);sens.append({'hidden_effect':gamma,'omitted_U':float(omit[1]),'included_U':float(full[1])})
 # Public aggregate facts from the 1989 FINAL PHS report; crude summaries, not its adjusted analysis.
 count1,n1,count0,n0=139,11037,239,11034;p1=count1/n1;p0=count0/n0;rdiff=p1-p0;se=np.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0);rr=p1/p0
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot([v['hidden_effect'] for v in sens],[v['omitted_U'] for v in sens],'o-',label=L('遗漏U','U omitted'),color='#d87430');axs[0].plot([v['hidden_effect'] for v in sens],[v['included_U'] for v in sens],'s-',label=L('调整U','U adjusted'),color='#237b94');axs[0].axhline(1,color='#83949e',ls=':');axs[0].set(xlabel=L('隐藏U对结果的生成系数','Generating outcome coefficient of hidden U'),ylabel=L('处理效应估计','Treatment-effect estimate'),title=L('敏感性情景：改变未测量机制','Sensitivity scenarios: change the omitted mechanism'));axs[0].legend(fontsize=9)
 axs[1].bar([0,1],[1000*p0,1000*p1],color=['#83949e','#237b94']);axs[1].set(xticks=[0,1],xticklabels=[L('安慰剂组','Placebo group'),L('随机分配阿司匹林组','Assigned aspirin group')],ylabel=L('每千名分配者的事件数','Events per 1,000 assigned participants'),title=L('1989报告：原始事件比例','1989 report: crude event fractions'));axs[1].text(0,1000*p0+.4,f'{count0}/{n0}',ha='center');axs[1].text(1,1000*p1+.4,f'{count1}/{n1}',ha='center');axs[1].set_ylim(0,26);save(fig,'sensitivity_trial')
 differences=np.linspace(.005,.05,100);sizes=np.array([n_per_arm(.1,.1+d) for d in differences]);required=int(np.ceil(n_per_arm(.1,.12)));days=int(np.ceil(2*required/1000));recruitment=max(14,int(np.ceil(days/7)*7));fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot(100*differences,sizes,color='#237b94');axs[0].scatter([2],[required],c='#d87430');axs[0].set(yscale='log',xlabel=L('绝对提升（百分点）','Absolute increase (percentage points)'),ylabel=L('每组所需人数','Required participants per arm'),title=L('基线10%，双侧5%，功效80%','Baseline 10%, two-sided 5%, power 80%'));axs[1].broken_barh([(0,recruitment)],(15,8),facecolors='#237b94');axs[1].broken_barh([(recruitment,7)],(15,8),facecolors='#d87430');axs[1].set(xlim=(0,recruitment+8),ylim=(5,32),yticks=[],xlabel=L('天数','Days'),title=L('招募覆盖两周，再等待7天结局','Recruit over two weeks, then mature 7-day outcomes'));axs[1].text(recruitment/2,19,L('招募','Recruit'),ha='center',va='center',color='white');axs[1].text(recruitment+3.5,19,L('结局成熟','Maturation'),ha='center',va='center',color='white',fontsize=9);save(fig,'power_duration')
 summary={'n':n,'treated_n':int(T.sum()),'controls_n':int((1-T).sum()),'true_population_ate':1,'true_sample_ate':float(tau.mean()),'naive_difference':naive,'ipw_ate':ipw,'hajek_ate':hajek,'aipw_ate':aipw,'aipw_se':aipw_se,'aipw_ci95':[aipw-1.96*aipw_se,aipw+1.96*aipw_se],'dml_intercept':float(dml[0]),'dml_slope':float(dml[1]),'matching_att':att,'true_sample_att':true_att,'propensity_min':float(e.min()),'propensity_max':float(e.max()),'absolute_smd_before':abs(before).tolist(),'absolute_smd_after':abs(after).tolist(),'iv':iv,'did':did,'rd':rd,'sensitivity':sens,'trial':{'treated_events':count1,'treated_n':n1,'control_events':count0,'control_n':n0,'total_n':n1+n0,'crude_risk_difference':rdiff,'crude_risk_ratio':rr,'binomial_difference_ci95':[rdiff-1.96*se,rdiff+1.96*se]},'power_per_arm':required,'raw_recruitment_days':days,'planned_recruitment_days':recruitment,'outcome_window_days':7,'planned_complete_day':recruitment+7}
 summary.update({'crossfit_fold_counts':np.bincount(fold).tolist(),'potential_effect_identity_error':float(np.max(abs(Y1-Y0-tau))),'did_trend_bias':did['0.7']-did['0.0']})
 np.savez_compressed(out/'experiment_data.npz',X=X,treatment=T,outcome=Y,potential_y0=Y0,potential_y1=Y1,true_effect=tau,propensity=e,crossfit_fold=fold,aipw_scores=phi,matched_control_indices=matched,rd_running=running,rd_outcome=outcome);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

从新的实际问题出发，可以依次完成四件事：确定潜在结果与目标人群，画出分配和结果的机制，选择能够识别该目标的设计，再用与设计相符的估计、区间及敏感性检查形成结果。机器学习主要帮助处理复杂预测关系，研究设计决定这些预测关系能否支持所问的干预。两者各自做好自己的工作，才能把相关性分析推进成清楚的因果论证。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M08.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Neyman (1923; English translation 1990), On the Application of Probability Theory to Agricultural Experiments](https://ics.uci.edu/~sternh/courses/265/neyman_statsci1990.pdf)

   潜在结果与随机农业试验的历史结构。

   Primary reference; no article figure reproduced
2. [DoWhy — User guide](https://www.pywhy.org/dowhy/main/user_guide/)

   图、识别、估计与反驳检查。

   MIT project; original graph attributed
3. [DoWhy repository](https://github.com/py-why/dowhy)

   原始因果图与逐文件MIT许可。

   MIT
4. [EconML — Double Machine Learning](https://econml.azurewebsites.net/spec/estimation/dml.html)

   残差化、交叉拟合和异质效应。
5. [Causal Inference for the Brave and True — Regression Discontinuity](https://matheusfacure.github.io/python-causality-handbook/16-Regression-Discontinuity-Design.html)

   阈值附近局部比较与带宽。

   Open tutorial; linked reference
6. [Final report on the aspirin component of the ongoing Physicians’ Health Study (1989)](https://www.urmc.rochester.edu/MediaLibraries/URMCMedia/neurology/documents/PHS.pdf)

   表1的139/11037与239/11034；本文由汇总计数重算原始比例。

   Primary paper; aggregate numerical facts, no figure or prose reproduced
