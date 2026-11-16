# 沿着时间整理多批数据

Source: https://ml-biomat.com/tutorials/python-scientific/p14/
Language: zh-CN

把启动时刻、经过时间、分箱平均和记录覆盖率放在同一条清楚的分析路径中。

## 两批实验都在升温，怎样放在一起比较

两批样品依次放进加热装置，温度记录都从室温逐渐升高。第一批9点启动，第二批晚了7分钟。如果直接按钟表时间把两条曲线画在一起，第二批会明显向右移动；如果问题是“启动以后哪批升温更快”，就应该比较各自启动后的第5分钟、第10分钟。时间列因此不只是画图用的横坐标，它决定哪些观测能够比较，也决定平均值代表哪一段过程。本篇用两批不等间隔的教学记录，完成时间解析、分批对齐、分箱平均和滚动窗口分析。

批次A在经过0、1、2.5、5、6、9、15、16、19 min时记录温度22、26、35、47、51、58、67、69、71 °C；批次B使用0、2、3、5、8、9、15、17、19 min，对应21、29、35、44、53、55、65、68、70 °C。每一对时间与温度是一条观测，两批合计18条。间隔特意没有设成相等，10到15分钟之间也没有记录，便于看清分箱和窗口如何处理真实存在的空档。代码采用一个固定的示例日历日生成时间戳，所有记录都由这里给出的规则确定。

时间整理常常像给两场不同时间起跑的比赛对表。钟表时间说明谁先出发，经过时间说明谁跑到了比赛的哪个阶段。两种坐标都保留有用信息，只是回答不同问题。对实验而言，启动事件还需要明确：打开加热器、放入样品或开始采样，可能是三个不同的时刻。先约定过程从哪个事件算起，再讨论曲线对齐，才能让“第5分钟”在不同批次之间具有相同含义。

## 把时间看作数据的身份，而不只是第几行

Wes McKinney在2010年介绍pandas的论文中，把不同长度数据的对齐、缺失观测和时间处理列为重要的实际问题。来自不同日期范围的数据，不能因为排在同一行就直接相加；记录缺失时，也需要让空缺在结构中保留下来。早期pandas的设计选择之一，是让数据结构理解时间标签，而不强制所有记录都先变成固定间隔。今天整理不等间隔实验记录时，这个思想仍很直接：保留观测真正发生的时刻，再在需要时明确选择怎样对齐或汇总。

普通数组的第4个元素只说明位置，时间标签还说明该值发生在什么时候。一个带时间索引的序列，可以把某个温度与它的时间戳绑定；筛选一个时间范围、比较相邻时间差或按5分钟汇总，都可以围绕这一标签执行。索引可以理解为贴在每条记录上的检索标签，它不必是从0开始的整数。时间标签使日历规则和时长运算进入数据结构，但它仍需要正确的单位、时区和实验事件定义。

![同一组教学温度记录在两种时间坐标下的比较。左图保留B比A晚7分钟启动的事实；右图分别减去各批次启动时刻，对齐过程阶段。连线用于追踪相邻记录，并未增加区间内部的观测。这是带标签时间数据所支持的一种显式对齐。](https://ml-biomat.com/static/tutorials/python-scientific/figures/dc761cd99608544fc94d7e40.svg?v=dc761cd99608)

图 1同一组教学温度记录在两种时间坐标下的比较。左图保留B比A晚7分钟启动的事实；右图分别减去各批次启动时刻，对齐过程阶段。连线用于追踪相邻记录，并未增加区间内部的观测。这是带标签时间数据所支持的一种显式对齐。

图中左侧的两条曲线采用钟表时间，保留了B晚启动7分钟的信息；右侧分别减去各批次的启动时刻，使过程阶段对齐。两边使用完全相同的18个温度值。这个对照体现了数据整理中的一个重要选择：改变的是比较坐标，还是观测本身。本例只改变时间基准，没有修改温度，也没有在空档中制造新观测。连线帮助追踪相邻记录之间的顺序，区间内部是否近似线性，需要额外的过程假设。

对齐依据应来自可解释的实验事件。如果为了让两条曲线看起来相似，任意移动它们直到峰值重合，原本真实存在的启动延迟或响应时间差也可能被消去。按明确启动事件对齐后，可以继续保留日历时间列，以便检查同一时刻环境是否发生变化。日历时间与经过时间共同保存，比只留下一个重新编号的横轴更有利于理解多批实验。

## 从写着日期的文本，得到能计算的时间

CSV中的时间通常最初是一段文本，例如一个包含日期、小时和分钟的字符串。文本可以显示给人看，却不自动具备“相差几分钟”的计算意义。`pd.to_datetime`把文本解析成pandas能处理的时间值。格式清楚时可以显式给出`format`，让年份、月份、日期分别对应固定位置。像“01/02”这样的写法在不同习惯下可能指1月2日或2月1日；日期格式属于数据定义，应在读取时确定。

时间戳描述一个时刻，时间间隔描述两个时刻相隔多久。pandas分别提供相关的日期时间类型与时间间隔类型。两个时间戳相减得到时间间隔，时间戳加上时间间隔得到另一个时刻。这种区别与“星期一上午9点”和“过了5分钟”的区别相同。本例先按明确的UTC时间建立各批次启动时刻，再加上逐项给定的分钟数，得到每条记录的时间戳，因此经过时间可以反向检查。

时区说明钟表读数如何对应实际时刻。带有UTC偏移的时间文本可通过`utc=True`统一到UTC；如果输入没有时区信息，这个参数会把它解释为UTC，而不会自动猜测仪器所在地。对于明确记录当地钟表时间的文件，应先按已知时区建立对应关系，再转换到共同基准。`tz_localize`给原本没有时区的钟表读数指定时间语境，`tz_convert`则把已有时区的时刻换成另一种钟表表示。二者解决的问题不同。

解析失败也应能定位到原始记录。使用`errors="coerce"`时，无法解释的文本会变成`NaT`，表示缺失的时间值；随后可以通过缺失标记筛出这些行，核对日期格式或补全字段。若直接删除它们，曲线中的记录覆盖范围可能随之改变。完成解析后，检查最早与最晚时刻、同批次时间是否单调、是否有重复时间戳，再进入分箱。重复时间可能来自多个传感器，也可能是重复导入，处理方式取决于观测身份。

## 在每个批次内部建立经过时间

经过时间从本批次启动时刻算起。因为A与B的启动时刻不同，减法必须使用各自的起点，而不能把整个数据表最早的时间当成所有批次的起点。否则B的第一条记录会显示为经过7分钟，实际上它刚刚启动。完整脚本让每行保留`batch`、`timestamp`和`start`，然后逐行计算时间差；这些字段共同说明温度属于哪个过程阶段。

$$
\Delta t_i=T_i-T_{0,b}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 当前批次的观测序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 批次标识符，例如A或B，无单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/d337cf254934852ef394972a.svg) | 该观测的时间戳，使用一致的时区和时间单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e26e8726da71c7cc497d4b0.svg) | 批次b的启动时间戳，采用与T相同的时间基准 |
| ![Formula](https://ml-biomat.com/static/agent-math/f9b2449534eeccba7530b307.svg) | 相对于本批次启动时刻的经过时间，本篇以min表示 |

批次B在09:07启动，09:12的记录对应经过时间5 min。批次A在09:00启动，09:05也对应5 min。程序先把时间戳相减得到时间间隔，再通过total_seconds()转换为秒并除以60，得到分钟。相减前两时间戳必须指向同一时间基准下的实际时刻。

`.dt.total_seconds()`把时间间隔转换成完整秒数，包括跨小时或跨天的部分；再除以60得到分钟。这个顺序比提取钟表的“分钟”字段更可靠，因为钟表分钟会在每小时重新从0开始。假如一个过程从09:58持续到10:03，完整间隔是5分钟；单独用分钟字段3减58则会得到错误的负值。把日期时间当作专门的类型处理，能够让进位和跨日规则参与计算。

在做相邻差分、滚动窗口或查找最近时刻之前，应按批次和时间排序。各批次内部的先后顺序才是过程顺序。若把A的末条记录与B的首条记录接成同一序列，再做滚动平均，窗口可能同时包含两个样品的温度；结果看起来平滑，却已经改变了分析对象。因此，分组是时间运算的边界。可以先逐批处理后再拼接，也可以使用明确按批次分组的窗口接口，关键是避免窗口跨越独立实验。

经过时间对齐也不要求每批都恰好在同一时刻采样。A在2.5 min有记录，B在3 min有记录，这两个时间应该先如实保留。需要共同网格时，可以选择分箱、插值或模型预测，但它们各自引入不同含义。分箱把一个区间里的观测汇总；插值依据相邻观测构造中间值；模型预测通过函数描述过程。本篇先学习分箱，因为它能把每个摘要明确追溯到包含的原始记录。

## 一个5分钟平均值，究竟包含哪几条记录

分箱是沿时间轴划出一段段区间，再把每个区间内的记录汇总。把箱宽设为5 min、起点设为0，可以得到[0,5)、[5,10)、[10,15)、[15,20)等区间。左边的方括号表示包含左端点，右边的圆括号表示不包含右端点。因此，恰好5 min的观测进入第二箱，不会同时在第一箱再计入一次。这种端点规则保证每条记录有明确归属。

$$
k_i=\left\lfloor\frac{t_i-a}{h}\right\rfloor,\qquad a+k_i h\le t_i<a+(k_i+1)h
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | 第i条记录的经过时间，min |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 分箱基准偏移量，min |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 正的箱宽，min |
| ![Formula](https://ml-biomat.com/static/agent-math/e8755a0f9e8b8e36aada3a9f.svg) | 记录所属箱的整数编号，可以为负，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/9441613214b6ab5fddf9ec85.svg) | 向下取整，取不大于内部数值的最大整数 |

箱宽h=5 min、偏移a=0时，t=5 min得到k=1，进入[5,10)箱；左端点包含，右端点留给下一箱。偏移改为a=2 min，t=0时(0−2)/5=−0.4，向下取整为−1，对应[−3,2)箱。负的箱左端点是分箱坐标的结果，原始观测仍从0 min开始。

pandas的`resample`把时间分组与后续汇总连接起来。`closed="left"`指定左闭右开的成员规则，`label="left"`指定结果行使用箱左端点作为标签。标签的位置与成员规则是两件事：将标签改到右端点，并不会自动把边界上的观测重新分组。本例还明确指定基准和偏移，使所有批次都按相同的经过时间边界处理，而不是分别从某个偶然的首条采样时刻向后划箱。

箱内平均值使用实际进入该箱的观测。A的第一箱有0、1、2.5 min三条记录，温度为22、26、35 °C；第二箱有5、6、9 min的47、51、58 °C。把温度相加后除以记录数，就分别得到约27.6667和52 °C。输出同时保留`mean`与`count`，使一个摘要既有数值，也有它所依据的记录数量。

$$
\bar y_k=\frac{1}{n_k}\sum_{i\in I_k}y_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 一个时间箱的编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/db1af26db044259d897bbc6c.svg) | 第k箱中温度非缺失的观测序号集合，无单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 集合中的观测序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | 该箱内非缺失温度记录数，无量纲正整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i条温度记录，°C |
| ![Formula](https://ml-biomat.com/static/agent-math/c752241b25f7282c420ab050.svg) | 该箱内观测温度的算术平均，°C |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 把属于该箱的温度记录相加 |

批次A的[0,5)箱包含22、26、35 °C，因此平均值为83/3≈27.6667 °C，记录数3。[10,15)箱的记录数为0，分母不成立，均值保存为缺失。这里每条记录各占一份权重；不等间隔采样时，它与按持续时间加权的时间平均不同。

不等间隔采样时，这个均值给每条观测相同权重。如果某一阶段采样更密，它就会在观测均值中贡献更多次。要估计一段时间内的平均温度，需要进一步说明每个值代表多长时间，或为相邻点之间的变化选择积分规则。这里先保留观测均值的含义，避免把它与时间平均混在一起。类似地，温度读数通常适合求均值，而某些按区间累计的计数可能适合求和；汇总函数应由测量量的定义决定。

## 让空档与平均曲线一起留下来

A在[10,15) min内没有记录。这个箱的计数为0，平均值保存为缺失；15 min本身按照左闭右开规则属于下一箱。缺失均值与0 °C差别很大：前者说明没有观测可供计算，后者是一种具体温度。将缺失填成零会制造一次突然降温，再制造随后的升温。图中让均值曲线在空箱处断开，并在下方明确画出记录数0，使空档成为可以直接阅读的信息。

![批次A的5分钟与10分钟分箱。每个均值点放在对应区间中心，下排保留记录数；5分钟分箱中的\[10,15)为空，均值曲线在这里断开。10分钟箱把这段空缺与后段有观测的时间放在同一箱中。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0e818130a13507831ed5202c.svg?v=0e818130a135)

图 2批次A的5分钟与10分钟分箱。每个均值点放在对应区间中心，下排保留记录数；5分钟分箱中的[10,15)为空，均值曲线在这里断开。10分钟箱把这段空缺与后段有观测的时间放在同一箱中。

箱宽改为10 min以后，[0,10)包含六条记录，[10,20)包含三条记录，两个箱都有平均值。原本[10,15)的空档仍然存在，只是与后半段有记录的时间一起被装入较宽的箱。两个平均值之间的连线看起来更完整，并不意味着仪器补采了空档。比较不同分箱宽度时，观察均值变化之外，也应查看各箱的计数和原始时间分布。宽箱改善了摘要的稳定程度，同时降低了时间定位的细致程度。

向前填充是一种明确的补值规则：把最近一次观测继续用于后续时间点。它适合描述某些一直保持到下一次更新的状态，例如设备设定值；用于持续变化的样品温度时，则相当于假设温度在这段时间保持不变。线性插值又采用另一种假设，认为相邻观测之间按直线变化。选择补值之前，应说明补出的值承担什么分析用途，并用标记把它与实际观测区分开。本例保留原始空档，让读者先看到数据本身的覆盖情况。

记录数也不等于独立样品数。一个传感器在某分钟连续读了很多次，能够更细地描述这段时间，却没有增加样品个数；相邻读数还可能彼此相关。把分箱计数保留下来，首先是说明摘要由多少条记录构成。若要估计组间差异的不确定性，还需要回到独立实验批次、样品或其他实际重复单位。这与上一篇区分原始测量数和连接结果行数的思路相通。

## 最近三条记录，不一定等于最近五分钟

滚动窗口与固定分箱的区别，是窗口会跟着当前记录移动。计算“最近3条记录的平均值”，每前进一步就选取当前和此前两条记录；计算“最近5分钟的平均值”，则按真实时间跨度寻找落入区间的记录。在等间隔采样且参数相应匹配时，两者可能接近；不等间隔或有空档时，它们覆盖的过程范围会明显不同。

![同一组不等间隔记录的两种滚动平均。在15 min处，最近3条记录覆盖6、9、15 min，而最近5分钟窗口(10,15\]内只有15 min的记录。两条曲线的连线帮助追踪结果，未对原始缺口补值。](https://ml-biomat.com/static/tutorials/python-scientific/figures/4540e27822a526b56a934ba1.svg?v=4540e27822a5)

图 3同一组不等间隔记录的两种滚动平均。在15 min处，最近3条记录覆盖6、9、15 min，而最近5分钟窗口(10,15]内只有15 min的记录。两条曲线的连线帮助追踪结果，未对原始缺口补值。

以15 min这一刻为例，最近三条记录发生在6、9、15 min，对应51、58、67 °C，均值约58.6667 °C。它实际回看了9分钟。若使用最近5分钟并包含当前时刻、排除恰好10 min的左端点，窗口是(10,15]，其中只有15 min的67 °C一条记录，均值为67 °C。两个结果都能由各自规则准确得到，差别来自窗口究竟按“条数”还是按“时长”定义。

代码中的`rolling(3)`表示三条记录，`rolling("5min")`表示五分钟跨度。时间窗口需要时间类型的索引，并要求时间按顺序排列。`min_periods`规定窗口至少有多少条非缺失记录才输出结果；本例明确设为1，使开始阶段已有一条记录时就能计算，并让计数不足三条时的行为保持可读。正式分析可以根据任务设置更多最低记录数，再同时保存窗口覆盖情况。

滚动平均会让局部波动更平缓，但它也把相邻窗口大量重叠的记录重复用于多个输出点，所以输出点之间相互依赖。窗口越宽，短时变化越容易被平均，趋势响应也可能延后。把窗口放在当前时刻之前，适合逐时读取已有数据；把窗口居中，则会利用当前时刻之后的记录，适合回看完整过程时平滑展示。选择规则时先说明它服务于实时判断还是事后整理，再解释曲线的时间位置。

## 移动箱的边界，看平均值怎样跟着改变

下面的实验把每次分箱拆成三个同步视图。上方保留原始观测，背景带表示时间箱；下方分别显示箱内观测均值与记录数。选中某个箱后，其中的观测和对应摘要会标为红色，页面同时列出每条记录的时间与温度。箱宽决定汇总多长的时间，偏移决定从哪里开始划分；两者都会影响边界附近的观测归属。

## 移动时间箱，追踪记录与平均值

修改箱宽或起点偏移，原始记录、分箱均值和记录数同步更新。选择一个区间后，红色标记显示它包含的全部记录。均值图中的横线表示整个时间箱的摘要；空箱保留空白。

[Figure: 原始温度记录及其时间箱归属](https://ml-biomat.com/tutorials/python-scientific/p14/#P14-records)

[Figure: 各时间箱的观测平均温度](https://ml-biomat.com/tutorials/python-scientific/p14/#P14-means)

[Figure: 各时间箱的实际记录数](https://ml-biomat.com/tutorials/python-scientific/p14/#P14-counts)

先保持A批次和5 min箱宽，选择[10,15)区间，确认原始记录、均值和计数共同表达“空箱”。然后把偏移从0改为2 min，第一箱变成[−3,2)，其中包含0和1 min的22、26 °C，均值为24 °C。原始记录仍从0开始，负的左端点只是分箱网格相对观测起点移动后的结果。再把箱宽改成10 min，比较两幅摘要图怎样压缩时间细节，同时观察上方原始点没有移动。

不同分箱方案得到不同摘要，是规则对同一组数据的不同整理。应根据过程变化的时间尺度、采样覆盖和分析问题选择规则，再把箱宽、基准与端点写进计算。若只挑选使两组差别看起来最大的边界，结论就会依赖展示方式。保留原始记录与几种合理尺度的对照，可以帮助确定哪些变化持续存在，哪些主要来自分箱边界的移动。

## 把完整时间处理过程写成可重复运行的程序

下面的完整脚本分成数据建立、分箱函数和主计算三部分。`teaching_data`给出两批时间与温度，并解析成带UTC信息的时间戳；`aggregate`把经过时间放到共同的示例时间基准上，调用`resample`计算均值与计数；`main`按批次运行不同箱宽和偏移，随后比较两种滚动窗口。共同基准用于让分箱边界一致，原始钟表时间仍保存在输出表里。

### 完整例子：时间解析、分批对齐、分箱与窗口

直接运行pandas时间类型与resample、rolling。两个批次的时间和温度都明确列出；输出保留原始记录、每种分箱表、滚动结果和数值摘要。

```
"""Align two irregular teaching time series and inspect aggregation and coverage."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

BLUE,RED,INK,GRAY='#28658c','#b64a35','#202e39','#71808b'
EPOCH=pd.Timestamp('2000-01-01T00:00:00Z')


def teaching_data():
    definitions={'A':([0,1,2.5,5,6,9,15,16,19],[22,26,35,47,51,58,67,69,71],'2000-01-01T09:00:00Z'),
                 'B':([0,2,3,5,8,9,15,17,19],[21,29,35,44,53,55,65,68,70],'2000-01-01T09:07:00Z')}
    frames=[]
    for batch,(elapsed,temperature,start) in definitions.items():
        stamp=pd.Timestamp(start)+pd.to_timedelta(elapsed,unit='min')
        frames.append(pd.DataFrame({'batch':batch,'timestamp':stamp.astype(str),'start':start,
                                    'temperature_C':temperature}))
    frame=pd.concat(frames,ignore_index=True)
    frame['timestamp']=pd.to_datetime(frame['timestamp'],utc=True)
    frame['start']=pd.to_datetime(frame['start'],utc=True)
    frame['elapsed_min']=(frame['timestamp']-frame['start']).dt.total_seconds()/60
    return frame.sort_values(['batch','timestamp']).reset_index(drop=True)


def aggregate(frame,width,offset=0):
    relative_index=EPOCH+pd.to_timedelta(frame['elapsed_min'],unit='min')
    signal=pd.Series(frame['temperature_C'].to_numpy(dtype=float),index=relative_index)
    grouped=signal.resample(f'{width}min',origin=EPOCH,offset=pd.Timedelta(minutes=offset),
                            closed='left',label='left').agg(['mean','count'])
    grouped['left_min']=(grouped.index-EPOCH).total_seconds()/60
    grouped['right_min']=grouped['left_min']+width
    return grouped.reset_index(drop=True)


def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    def tr(a,b):return a if language=='zh' else b
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'font.size':11,
        'axes.labelsize':12,'axes.titlesize':13,'axes.titleweight':'bold','axes.spines.top':False,
        'axes.spines.right':False,'text.color':INK,'svg.fonttype':'none','svg.hashsalt':'P14'})
    data=teaching_data();data.to_csv(output/'thermal-records.csv',index=False)
    cases={}
    for batch,frame in data.groupby('batch',sort=True):
        for width,offset in [(5,0),(5,2),(10,0),(2,0)]:
            result=aggregate(frame,width,offset)
            result.to_csv(output/f'bins-{batch}-{width}-{offset}.csv',index=False)
            records=[{'left_min':float(r.left_min),'right_min':float(r.right_min),
                      'mean_C':None if pd.isna(r.mean) else float(r.mean),'count':int(r.count)}
                     for r in result.itertuples(index=False)]
            cases[f'{batch}-{width}-{offset}']={'bins':records,'empty_bins':sum(r['count']==0 for r in records),
                'total_observations':sum(r['count'] for r in records)}
    a=data.loc[data['batch'].eq('A')].copy()
    a['row_window_mean']=a['temperature_C'].rolling(3,min_periods=1).mean()
    time_signal=pd.Series(a['temperature_C'].to_numpy(dtype=float),index=pd.to_timedelta(a['elapsed_min'],unit='min'))
    a['time_window_mean']=time_signal.rolling('5min',min_periods=1,closed='right').mean().to_numpy()
    a.to_csv(output/'rolling-A.csv',index=False)
    at15=a.loc[a['elapsed_min'].eq(15)].iloc[0]
    assert abs(cases['A-5-0']['bins'][0]['mean_C']-83/3)<1e-12
    assert cases['A-5-0']['bins'][2]['count']==0
    assert cases['A-5-0']['bins'][2]['mean_C'] is None
    assert at15['row_window_mean']==(51+58+67)/3
    assert at15['time_window_mean']==67
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',metadata={'Date':None})
        fig.savefig(output/f'{name}-{language}.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.6),layout='constrained',sharey=True)
    origin=pd.Timestamp('2000-01-01T09:00:00Z')
    for batch,frame in data.groupby('batch'):
        color=BLUE if batch=='A' else RED
        clock=(frame['timestamp']-origin).dt.total_seconds()/60
        axes[0].plot(clock,frame['temperature_C'],'o-',color=color,ms=5,lw=1.3,label=tr('批次','Batch ')+batch)
        axes[1].plot(frame['elapsed_min'],frame['temperature_C'],'o-',color=color,ms=5,lw=1.3,label=tr('批次','Batch ')+batch)
    axes[0].xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'09:{int(v):02}'))
    axes[0].set(xticks=np.arange(0,31,5),xlabel=tr('钟表时间 / UTC','Clock time / UTC'),
                title=tr('钟表时间保留启动先后','Clock time retains start order'))
    axes[1].set(xlabel=tr('从各自启动起经过的时间 / min','Elapsed time from each start / min'),
                title=tr('经过时间对齐过程阶段','Elapsed time aligns process stage'))
    axes[0].set_ylabel(tr('温度 / °C','Temperature / °C'))
    for ax in axes:ax.legend(frameon=False);ax.set_ylim(15,78)
    save(fig,'alignment')
    fig,axes=plt.subplots(2,2,figsize=(12.4,8),sharex='col',gridspec_kw={'height_ratios':[2,1]},layout='constrained')
    for j,width in enumerate([5,10]):
        binned=aggregate(a,width)
        centers=(binned['left_min']+binned['right_min'])/2
        axes[0,j].scatter(a['elapsed_min'],a['temperature_C'],s=35,color=GRAY,label=tr('原始记录','Original records'),clip_on=False)
        axes[0,j].plot(centers,binned['mean'],'o-',color=BLUE,lw=2,label=tr('箱内观测均值','Mean of observations in bin'))
        axes[0,j].set(ylim=(15,78),title=tr(f'{width}分钟分箱',f'{width}-minute bins'))
        axes[0,j].legend(frameon=False,fontsize=9)
        axes[1,j].bar(centers,binned['count'],width=width*.8,color=BLUE)
        axes[1,j].set(xlim=(0,20),ylim=(0,7),xticks=np.arange(0,21,5),xlabel=tr('经过时间 / min','Elapsed time / min'))
        for x,count in zip(centers,binned['count']):axes[1,j].text(x,count+.15,str(count),ha='center',color=RED if count==0 else INK)
        for ax in axes[:,j]:
            for edge in binned['left_min']:ax.axvline(edge,color='#dce3e8',lw=.7,zorder=0)
    axes[0,0].set_ylabel(tr('温度 / °C','Temperature / °C'));axes[1,0].set_ylabel(tr('记录数','Observation count'))
    save(fig,'coverage')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.7),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
    axes[0].scatter(a['elapsed_min'],a['temperature_C'],s=30,color=INK,label=tr('原始记录','Original records'),zorder=4)
    axes[0].plot(a['elapsed_min'],a['row_window_mean'],'o-',color=RED,label=tr('最近3条记录','Last 3 records'))
    axes[0].plot(a['elapsed_min'],a['time_window_mean'],'s-',color=BLUE,label=tr('最近5分钟','Trailing 5 minutes'))
    axes[0].set(xlabel=tr('经过时间 / min','Elapsed time / min'),ylabel=tr('温度 / °C','Temperature / °C'),
                title=tr('窗口长度可以按行，也可以按时间','Window length can mean rows or elapsed time'))
    axes[0].legend(frameon=False,fontsize=10)
    axes[1].set_axis_off()
    axes[1].text(.03,.94,tr('在15分钟这一刻','At elapsed time 15 min'),fontsize=14,weight='bold')
    lines=[tr('最近3条记录：6、9、15 min','Last 3 records: 6, 9, 15 min'),
           tr('温度：51、58、67 °C','Temperatures: 51, 58, 67 °C'),
           tr('均值 = 58.67 °C','Mean = 58.67 °C'),'',
           tr('最近5分钟：(10, 15] min','Trailing 5 min: (10, 15] min'),
           tr('区间内有1条记录：67 °C','One observation in the interval: 67 °C'),
           tr('均值 = 67.00 °C','Mean = 67.00 °C')]
    for i,line in enumerate(lines):axes[1].text(.03,.79-i*.105,line,fontsize=11,color=RED if i<3 else BLUE)
    save(fig,'windows')
    summary={'data_kind':'explicit teaching timestamps and temperatures','n_records':len(data),
        'start_delay_B_min':7,'cases':cases,'at_15_min':{'row_window_mean_C':float(at15['row_window_mean']),
        'time_window_mean_C':float(at15['time_window_mean'])},'versions':{'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();main(args.output,args.language)
```

运行以后，`thermal-records.csv`保留18条原始教学记录及启动时刻、经过时间。各个`bins`表保存箱的左右边界、均值和计数；`rolling-A.csv`把两种窗口结果放回对应的原始时间。数值摘要中，A的5 min分箱有四个箱，计数依次为3、3、0、3；15 min处的两种滚动均值分别约为58.6667和67 °C。这些值可以直接由本篇列出的记录手算核对。

处理自己的时间记录时，先检查时间文本能否正确解析，时区是否一致，启动事件是否定义清楚，再按批次排序并计算经过时间。随后决定需要逐条记录、固定时间箱还是滚动窗口；每种结果都保留原始观测身份、区间规则和记录数。这样，后面的科学图不仅能展示一条温度曲线，还能说明每个点怎样由实验记录得到。下一篇将继续讨论这些信息如何进入坐标、图层和可保存的科学图形。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P14.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pandas: Time series / date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html)

   时间戳、时间间隔、时区以及分箱端点与标签。

   pandas BSD-3 documentation; original case and figures
2. [pandas: Windowing operations](https://pandas.pydata.org/docs/user_guide/window.html)

   按行数与按时间间隔定义滚动窗口。

   pandas BSD-3 documentation
3. [McKinney (2010), Data Structures for Statistical Computing in Python](https://github.com/scipy-conference/scipy_proceedings_2010/blob/master/papers/mckinney/pandas_scipy.rst)

   原作者讨论数据对齐、缺失观测与不强制等间隔的时间结构。

   Historical facts and design ideas paraphrased; original diagrams, no source code or image reproduced
