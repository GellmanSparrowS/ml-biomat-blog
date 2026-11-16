# 生命中的三类长链：蛋白质、糖链与核酸

Source: https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/
Language: zh-CN

[下载代码合集 ↓](https://ml-biomat.com/static/tutorials/polymer-ai/polymer-ai-notebooks.zip)

认识生命中的长链

杨云浩 · 复旦大学 · 高分子与生物大分子教程

棉线、鸡蛋和米饭，看上去很难归到同一类东西里。棉线可以纺成衣服，鸡蛋加热后会凝固，米饭能提供能量。把视线缩小到分子层面，会发现它们都与长链有关；但“有一条长链”还远远不够，我们还要知道链上装着什么、怎样接起来、哪些部分会与周围接触。本节从这三件事出发，认识生命中的蛋白质、糖链和核酸，并用一次AI实验检查：把分子写成数据时，怎样保留真正有用的信息。

[《高分子构象统计：采样、分布与独立样本》](https://ml-biomat.com/tutorials/polymer-ai/02-conformations-and-statistics/)把同一条链的许多构象放在一起，讨论怎样描述变化。这一次，我们暂时停住运动，把注意力放在分子本身的身份上。同一条链弯成不同形状，通常仍有相同的化学连接；若交换两个单元、增加一处分支或改变连接的立体方向，对象本身就可能变了。后面研究折叠、凝胶和分子设计时，会反复遇到这两层变化：一层是“同一个对象怎样活动”，另一层是“我们造出了怎样的新对象”。先分清它们，才能为AI选对输入和预测目标。

## 01蛋白质：共同的骨架，不同的侧链

可以先把一条蛋白质链想成一串带有不同挂件的连接件。连接件本身可以首尾相接，挂件则使不同位置具有不同的接触偏好。这个比喻里，连接件对应氨基酸的共同骨架，挂件对应侧链。常见的蛋白质氨基酸有20种，有的侧链容易与水接触，有的更愿意躲在水较少的地方，有的在一定条件下带电，有的体积较大、会影响相邻部分怎样摆放。这里的“愿意”描述的是许多分子运动之后的统计倾向；分子没有意图，接触方式改变了体系的能量和可实现的状态。

在通常的蛋白质主链中，一个氨基酸的羧基部分与下一个的氨基部分形成肽键，许多这样的连接构成多肽。连入链以后保留下来的氨基酸部分称为“残基”，因此数据库里的“第25号残基”就是链上第25个氨基酸单元。残基这个名字容易让人联想到废料，其实它强调的是成键后分子组成发生了变化。阅读序列、画粗粒化模型或分析蛋白质结构时，这个词会频繁出现。一个残基节点可以代表许多原子；它与“一个原子节点”是两种观察尺度，选择哪一种取决于研究问题。

这条骨架还有方向。蛋白质序列通常从N端写向C端，相当于先约定沿链读字母的起点和终点；N与C分别来自氨基端和羧基端的命名。A、G、K分别可以表示丙氨酸、甘氨酸和赖氨酸，字母让冗长的化学名称变成便于存储的序列。不过，符号的意义由所用字母表决定：核酸序列中的A指腺嘌呤。本节后面的学习实验另用A、B表示两种抽象单元，用它们检查排列顺序的作用。保存序列时连同字母表一起保存，程序才能知道自己读到的是哪类分子、哪种表示。

顺序为什么重要？想象一条链上有几处容易接触水的侧链，还有几处倾向于彼此靠近的侧链。如果把后者集中到同一段，形成的局部环境会与把它们均匀分散在整条链上不同。链的弯曲和接触把序列中相隔很远的残基带到一起，于是原本的一维排列参与组织三维结构。这样的过程要同时考虑周围的水、温度和其他分子。我们以后会用自由能和构象分布进一步解释，此处先抓住一件可以直接检查的事：数出每种残基有多少个，还没有告诉我们这些残基位于哪里。

20世纪50年代，Frederick Sanger及合作者研究胰岛素的工作，把这种“位于哪里”的问题变成了可以回答的化学问题。分析长链时，他们需要综合较短片段的信息，确定各个残基的排列，并进一步弄清二硫键的连接。序列可以由实验建立，这使蛋白质从一种含氮的复杂物质，变成可以逐位置描述的具体分子。今天向程序输入一行字母看似简单，这行字母背后却可能对应一整套分离、测量和推断。[[1]](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#ref-sanger)

![Frederick Sanger的1958年肖像](https://ml-biomat.com/static/tutorials/polymer-ai/assets/1d40517e51e300f5fcbf647c.jpg?v=1d40517e51e3)

1958 · 把序列确定为可描述的化学结构

Frederick Sanger

由片段确定排列，再补上链内与链间的连接。今天输入计算机的字母序列，承接着这些实验建立的分子身份。

**图1** Sanger的历史肖像。照片：Nobel Foundation，1958，摄影者未署名；[Wikimedia Commons，PD-Sweden / PD-1996](https://commons.wikimedia.org/wiki/File:Frederick_Sanger.jpg)。

二硫键也提醒我们，写出一行序列以后，连接信息有时还没写完。两处半胱氨酸侧链可以通过二硫键连接，位置可能在同一条主链上，也可能位于不同链上。若把主链画成绳子，这相当于给绳子的某些位置加了扣子。扣子改变哪些运动容易发生，也可能把几条链联系起来。序列文件可以告诉我们哪里有半胱氨酸；要知道实际成了哪些扣子，还需要相应的结构或实验信息。图表示便于把这些额外连接单独记录下来，避免把一行文字误当成全部结构。

蛋白质承担的作用也不止一种。酶通过具体的空间环境帮助反应发生；胶原构成细胞外基质的重要纤维；肌动蛋白则参与细胞内部骨架的组织。它们都由氨基酸残基组成，研究时关心的量却各不相同：酶可能关注反应活性，胶原纤维可能关注承载与形变，肌动蛋白网络可能关注连接如何随时间改变。把它们一概称作“功能好的蛋白质”无法形成明确的预测任务。AI需要知道输出究竟是活性、结合、尺寸、柔性还是某种力学响应，以及这个量是在什么条件下测得的。

再回到煮鸡蛋这件事。加热能改变蛋白质原先维持的接触关系，暴露新的接触位置，并促进许多分子形成聚集结构，宏观上便出现凝固。这个过程同时涉及单条链的状态和许多链之间的组织。把鸡蛋从生到熟简单画成“一条卷曲链变成直线”会遗漏关键环节；分子不必全部拉直，样品也并非由一条链构成。以后讲相分离、网络与凝胶时，我们会把这两层联系起来：先认识单分子，再看大量分子如何共同改变材料。

## 02糖链：单元相同，接法也能大不相同

“糖”在日常语言里常常让人想到甜味，在分子语言里却覆盖了许多不同的对象。单糖是构建糖链的基本单元；多个单糖通过糖苷键连接，就形成不同长度和连接方式的糖链，较长的通常称为多糖。棉花的重要成分纤维素是多糖，淀粉也是，细胞表面的一些短糖链还会参与分子识别。名称里都有糖，并不意味着它们都甜、都易溶于水或都能被同一种酶处理。认识糖链，最有用的起点是把“有哪些糖”与“这些糖怎么接”分开记。

以葡萄糖组成的链为例，淀粉中的直链淀粉主要采用α(1→4)连接，纤维素采用β(1→4)连接。括号中的1与4是参与连接的碳位置编号，箭头说明连接从哪一端指向哪一端；α与β进一步区分异头碳处的构型，也就是特定位置的立体排列。初学时不必立即记住完整的环状结构，可以把编号看作积木上的接口编号，把α、β看作接口的立体朝向。两个积木即使型号相同，用不同的接口方向接起来，后续可摆出的形状也会变化。这个比喻帮助我们记住必须保存哪些信息，真实的几何仍由原子的成键和相互作用决定。

这一区别会沿链积累。局部连接限制了相邻单元之间可以怎样转动，许多局部限制共同影响整条链的构象、链与链怎样接近，以及能否形成有序区域。因此，从葡萄糖单元到棉纤维的强度，中间需要经过连接、构象、分子间组织和纤维尺度的结构，不能跳过这些层次。若一个数据库只写“葡萄糖聚合物”，模型便失去了区分这两类连接的重要依据；再增加许多相同写法的记录，也无法恢复已经被删去的信息。

[Figure: 两条连接图的节点相同，边分别标记α一至四和β一至四](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#linkage-figure)

**图2** 连接图把化学信息保存在边的属性中。这里用相同的平面布点突出“属性不同”，线的朝向不表示真实的糖环构型或链构象。

糖链还有一种很自然的变化：分支。一个单糖具有多个可能参与连接的位置，当其中不止一处被用于连接其他糖单元，结构就可能长出分叉。淀粉中的支链淀粉除了α(1→4)主链连接，还含有α(1→6)分支连接。画在纸上时，分叉像树枝；存进计算机时，却需要明确哪个节点从哪个位置接出了哪条边。一条没有分支的序列可以从头到尾读下来，分支结构则要额外规定何处离开主干、何处返回，否则同一串字母可能对应不止一种连接方式。

“连成一条线”与“长出分支”也不是糖链结构的全部。糖单元的种类、某些位置的修饰、键的立体信息，都可能改变它与其他分子的接触。细胞表面的糖链像一片伸向周围的分子环境，蛋白质可能识别其中某些局部排列；识别所需的局部结构不一定能够用总含糖量概括。描述一次结合实验时，糖链结构、识别它的蛋白质、测量条件与观测信号需要一起记录。后面学习糖链AI时，会把这些信息分成输入与目标，并说明为什么荧光强度和结合常数是不同的量。

多糖也把生物功能与日常材料联系起来。纤维素能够构成纤维，某些多糖在水中形成黏稠溶液，还有一些能在适当条件下构成凝胶。它们表现不同，与链长、连接、带电基团、分子间接触以及制备条件共同有关。想知道一种多糖是否适合做含水材料，就需要把“是什么结构”与“在什么环境中使用”一起描述。[《高分子的环境响应：水合、温度与电荷》](https://ml-biomat.com/tutorials/polymer-ai/04-chain-environments/)将专门讨论水、电荷与温度；这一节先把结构身份写清楚，使后面的环境变量有一个确定的作用对象。

20世纪20年代开始，Hermann Staudinger围绕长链大分子的研究，推动了对天然与合成高分子连接方式的认识。他在1953年的诺贝尔演讲中讨论了纤维素等对象。对今天的读者而言，这段历史与糖链的联系很直接：要解释一根纤维，我们必须知道它内部是哪些单元通过化学键连成长链，再研究许多长链如何组织。这个先确定分子、再解释材料的顺序，也适用于训练数据的整理。[[2]](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#ref-staudinger)

![Hermann Staudinger的历史肖像](https://ml-biomat.com/static/tutorials/polymer-ai/assets/ed30f776c0eb2d17203db726.jpg?v=ed30f776c0eb)

1920年代 → 1953 · 从共价长链理解高分子

Hermann Staudinger

先确定单元怎样连接为分子，再研究许多分子如何组成纤维和其他材料。糖链让分子结构与宏观材料之间的联系变得具体。

**图3** Staudinger的历史肖像。照片：Nobel Foundation，《Les Prix Nobel en 1953》（1954）；[Wikimedia Commons，PD-Sweden](https://commons.wikimedia.org/wiki/File:Hermann_Staudinger.jpg)。

描述糖链时，本节使用的圆点和连线是为了突出连接关系。真正的结构图还会区分单糖种类，并标明连接位置和构型；糖生物学中有相应的符号规范，可以把复杂结构画得较为紧凑。规范的意义在于让读图者与程序共享同一套约定。类似地图上蓝色线条代表河流，符号只有在图例明确时才可靠。以后读取糖链数据，应把采用的表示格式也作为数据说明的一部分，尤其要检查简写里有没有省略本次预测需要的连接信息。

## 03核酸：沿骨架读序列，跨序列看配对

DNA和RNA由核苷酸连接而成。每个核苷酸可以拆成碱基、糖和磷酸相关部分来理解；糖与磷酸参与构成骨架，不同的碱基把位置之间的差别带到序列里。DNA常用A、T、G、C表示四种碱基，RNA通常使用A、U、G、C。这里的A代表腺嘌呤相关的序列位置，与前面蛋白质字母表中的A不同。文件类型、分子种类和字母表必须一起保存，否则看起来合法的一串字符，也可能被程序按错误的化学对象解释。

核酸序列常沿5′端到3′端书写。撇号是糖上碳原子编号的习惯，帮助它与碱基上的编号区分；对刚开始阅读的人，最先需要把它当作序列方向的明确约定。一条序列换个方向读，位置次序就变了，而另一条与它配对的链还涉及互补关系。以一小段DNA为例，5′-AAGC-3′对应的互补片段可写为3′-TTCG-5′；若也把第二条链按5′到3′记录，便成为5′-GCTT-3′。先逐位配对，再反向书写这两步，解释了为什么程序里会出现“反向互补”操作。

双链中的骨架连接和两条链之间的配对承担不同的作用。骨架把同一条链上的核苷酸连续连接起来，配对则把合适位置的碱基联系起来，并与碱基堆积、溶液条件等共同参与稳定结构。若画成图，骨架边与配对边应该有不同的类型。把它们全部画成没有说明的同一种连线，会掩盖“沿链移动一个位置”和“跳到配对位置”这两种关系的差别。这个区分以后会直接进入RNA结构图和图神经网络的边特征。

1953年的DNA结构研究让这种跨链关系变得清晰。Watson与Crick提出的双螺旋模型，与同一期发表的Wilkins等人、Franklin与Gosling的实验研究共同构成了这段历史的重要材料。模型需要同时容纳骨架几何、碱基关系和实验线索。我们现在画出的梯子图只是帮助阅读连接层次的简图；从梯子到真实螺旋，还要加入空间排布及其证据。科学史在这里提供了一种研究顺序：先确认图里每条线表达的关系，再讨论它能解释哪些观测。[[3]](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#ref-dna)

[Figure: 两条反向平行DNA链，绿色实线为骨架，棕色虚线为配对](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#nucleic-figure)

**图4** DNA局部连接的概念图。绿色实线表示沿链的骨架关系，棕色虚线表示互补配对；图未展开原子结构，也未画成真实螺旋。

RNA让“序列与结构不是同一份信息”更加直观。一条RNA可以在同一链内的不同位置之间形成配对，出现茎环等结构；序列较远的两个位置，空间上可能靠得很近。就像一根有标记的绳子，沿绳子量距离与把它折起来后量两点的空间距离，会得到两种不同的结果。要预测哪个位置与哪个位置配对，输入是一维的字母序列，输出却涉及成对的位置关系。第十一节会从小规模的配对算法出发，讨论怎样让学习模型参与这个任务。

同一类分子也会因研究目标不同而采用不同表示。若要统计DNA中G与C的总比例，数一数字母已经足够；若要寻找特定排列，就必须保留顺序；若要研究RNA的茎环，需进一步关心配对；若要估计与另一分子的空间接触，又需要结构或构象信息。这些表示不是一条简单的优劣排行榜。保存得越详细，处理成本通常也越高，而某些信息还要通过实验或计算获得。合适的表示应保留影响当前问题的差异，同时清楚说明观察尺度和信息来源。

还可以用这三类分子理解材料中的复合结构：一种蛋白质可以带有糖链，核酸可以与蛋白质共同组装，细胞外的多糖与蛋白质也会一起构成含水环境。我们把它们分开介绍，是为了先学会几种基本连接语言；真正研究生物材料时，经常要把这些语言放在同一个对象里。相应地，AI输入可以同时包含序列、糖链图、组成比例和环境条件，只要每项输入都能对应到一个可说明的物理或生物量。

## 04把分子写成数据，先问会丢掉什么

现在来做一个小实验。给你六个A单元和六个B单元，可以把它们排成AAAAAABBBBBB，也可以排成ABABABABABAB。两条链都有12个单元，组成各占一半。若把数据表写成“总长度12，A比例0.5，B比例0.5”，它们对应的两行便完全一样。模型收到相同的输入，只能给出相同的确定性预测；如果标签却要求它区分“集中排列”与“交替排列”，矛盾就出在输入已经删掉了顺序。这个例子帮助我们在训练之前判断，一张表究竟有没有保留任务所需的信息。

把数量转成可比较的比例

fA = nA / N；fB = nB / N

式子里的N是总单元数，n_{A}、n_{B}分别是A、B的个数，f表示它们所占的比例。6除以12得到0.5，意思是每两个单元平均有一个属于A。这些比例都是无量纲的，因为分子和分母数的是同一种对象。在只有A、B两类单元时，两项比例相加等于1；如果将来还有第三类，就要把第三类一起列入。组成比例解决了不同长度之间怎样比较的问题，同时也明确放弃了位置信息。计算本身很简单，重要的是知道这一步保留了什么。

要让程序看见一点顺序，可以数一数相邻两个单元何时不同。12个单元排成未闭环的线性链，一共有11对相邻单元；AAAAAABBBBBB只有A与B交界的那一对不同，所以比例是1/11，约0.091。ABABABABABAB的11对邻居都不同，比例就是1。这个量描述“类型切换得有多频繁”，并不需要知道每个字母的具体化学性质。用这样的小量开始，有助于把特征与可观察的结构差异联系起来。

线性、未闭环序列；每对相邻单元只数一次

c = 相邻单元不同的连接数 / (N − 1)

s_{i}表示第i个位置的单元类型，s_{i+1}表示下一个位置；粗体的1是一个判断开关：括号里的“不同”成立时取1，否则取0。求和符号Σ让我们从第1对邻居一直检查到第N−1对，把这些0和1相加。最后除以N−1，得到0到1之间的比例c。若链首尾闭合，邻居对的数目和最后一对的处理都要相应改变。公式中的分母来自图里实际数过的对象，而不是看到“平均”就习惯性地写N。

移动单元：组成留下，邻居改变

[Figure: 十二个单元的排列，可使用下方按钮改变顺序](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#sequence-svg)

A的比例 不同邻居对 变化比例

**图5** 两个类型各六个的连接示意。动画每次交换两个位置，单元总数与组成始终保持不变；用暂停按钮停在任一排列，便可逐对核对变化比例。

对于分支结构，可以给节点编号，再写一张“谁与谁直接相连”的表。这张表就是邻接矩阵A：第i行、第j列的A_{ij}在节点i、j相连时取1，否则取0。在本节的无向图里，i连j也意味着j连i，所以表格沿对角线对称；节点不与自己相连，对角线取0。把第i行的1数出来，就是这个节点的邻居数，称为度数d_{i}。一条普通线性链的两个端点各有一个邻居，中间点各有两个；树状分支可以出现三个或更多邻居。

无向、无自环的连接图；每个邻居贡献一个1

di = Ai1 + Ai2 + … + AiN

这里的j从1数到N，意思是依次检查所有可能的邻居。例如某一行是0、1、0、1、1，把它们加起来得到3，这个节点就连着三个其他节点。给同一张图重新编号，会把矩阵的行列一起重新排列，但每个实际节点有几个邻居不会因此改变。一个针对整张图的性质预测，也应当保持这种“换编号不换物理对象”的一致性。下面的程序会主动重编号并核对特征，为第十八节训练GNN时检查置换不变性做准备。

1965年，Margaret Dayhoff及合作者编纂的《Atlas of Protein Sequence and Structure》把已知序列汇集成可比较的材料。把不同来源的记录放到共同格式里，能够提出单看一条序列时不容易问的问题：哪些位置相似，哪些片段可能有关，怎样系统地比较。今天训练模型前整理字母表、对象编号和来源，延续了这种把生物材料变成可计算对象的工作。数据表示不是计算结束后的排版，它会直接影响接下来能比较什么。[[4]](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#ref-dayhoff)

1965 · Dayhoff及合作者的序列汇编

[Figure: 三条示例序列按相同位置对齐，第三个位置用不同颜色突出](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#history-dayhoff)

**图6** 从序列收集到按位置比较的现代概念图。字母与颜色由本节为说明方法而绘制，未复刻原始图谱中的分子记录。原始汇编见文献[4]。

2017年，Gilmer等人的消息传递神经网络框架，把一组分子图学习方法写成共同的形式：节点结合邻居及连接的信息更新自身表示，再汇总成整个分子的输出。沿用本节的语言，就是让程序学会怎样从局部连接中提取有用的量，而不必总由人手工挑出“度数”这一项。信息传播一次，节点能汇入一跳邻居的情况；传播多次，可以纳入更远的图上关系。具体网络的表达能力取决于节点、边、更新函数和汇总方式，仍须用对应任务来检验。[[5]](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#ref-mpnn)

2017 · 消息传递神经网络框架

[Figure: 同一目标节点在零、一、两轮邻居汇入后，信息来源逐渐扩展](https://ml-biomat.com/tutorials/polymer-ai/03-biological-polymers/#history-message)

**图7** 绿色节点表示橙色圈中目标节点可接收信息的范围。图为消息传递范围的概念示意；每轮怎样计算、汇总什么特征，需要由具体模型定义。对应框架见文献[5]。

目前的度数特征已经能区分本节设计的线性树与带三叉点的树，但它描述不了所有图的差别。两张图可以有相同的度数分布，却采用不同的整体连接；同一张无类型连接图，也可能对应不同的糖苷键构型。因此，我们将循着实际问题逐步补充表示：先验证组成遗漏了顺序，再让边带上类型，最后训练会利用邻居信息的模型。每一步都有对应的结构差异和检验对象，模型的复杂度才有明确的用途。

## 05训练一个模型，观察信息怎样进入预测

下面的例子安排了两个彼此独立的分类任务。序列任务区分“相邻变化少”与“相邻变化多”，图任务区分线性树与有分支的树。数据由程序生成，标签分别来自切换比例和连接规则。这样做的用处是把问题控制得很清楚：我们事先知道该看哪里，可以检查模型有没有得到必要的输入。蛋白质活性、糖链识别和RNA折叠需要各自的生物观测作为标签；本次实验先检验表示和训练这两个环节。

程序生成320组配对对象，每组两个例子拥有相同的单元数，两个标签各出现一次。序列中A、B总数相等：一类相邻变化比例不超过0.4，另一类不低于0.6，中间区间留空；所有完整序列都经过查重。图中两类例子具有相同的点数和边数，通过改变一处连接产生分支。80组完整留作测试，其余240组训练，因此训练侧480个例子、测试侧160个例子。组号只负责划分，不作为模型特征；同一组的两个例子始终留在同一侧。

每个任务比较两种表示，并采用相同的学习方法。序列先看长度和组成，再加入相邻变化比例；图先看点数和边数，再加入度数至少为3的节点比例及端点比例。为了把训练过程看清楚，我们使用逻辑回归：它给每个输入特征一个权重，乘起来再相加，把得到的分数映射到0与1之间。这个映射叫sigmoid，输出p表示模型赋给类别1的概率。序列任务中类别1为“变化多”，图任务中类别1为“有分支”。

逻辑回归：从特征得到类别1的概率

z = w0 + Σ(j=1…D) wj xj；p = 1 / [1 + exp(−z)]

x_{j}是第j项输入特征，D是特征的总数，w_{j}是训练要调整的权重，w_{0}是与输入无关的偏置。程序先用训练集的均值和标准差把各列转为可比较的尺度，因此这里进入加权和的x是标准化后的值。exp表示以自然常数e为底的指数函数，exp(0)=1，所以当分数z=0时，p=1/(1+1)=0.5；当z约为2.20时，p约为0.9。分数越大，概率越接近1。需要输出类别时，程序把p不小于0.5的情况判为1，其余判为0。

有了预测，还要给程序一个可以逐步改进的目标。设真实类别y只取0或1：y=1时，希望模型把p推高；y=0时，希望它把1−p推高。可以把p与1−p想成分给两个答案的概率份额，正确答案分得越多，这次预测就越好。训练需要把“越好”写成“代价越小”，于是取正确类别概率的负对数：概率等于1时代价为0，概率很小时代价变大。把两个类别合在一个式子里，就得到**二元交叉熵**。它在这里衡量模型给正确类别分配了多少概率；这个定义明确以后，便能用数值比较两次预测，再决定参数往哪边调整。

每个训练例子的代价；再对训练样本取平均

ℓ(p,y) = −y ln(p) − (1 − y) ln(1 − p)

ln是自然对数，符号ℓ表示一个例子的损失。当y=1时，第二项乘上0消失，剩下−ln(p)：预测p=0.9时损失约0.105，预测p=0.1时约2.303。两次如果只看最后的类别，会得到一次对、一次错；损失进一步区分模型对正确答案给了多少概率。训练时，对480个训练例子的损失取平均，再调整权重。测试集留在训练过程之外，直到模型训练完才用来评价新对象。

权重怎样调整也可以顺着这个定义理解。对某项特征，如果模型经常把正类的概率估得偏小，而该特征在这些例子中为正，增加它的权重便会推高分数，使这些预测向正确方向移动。把所有训练例子的这种倾向加起来，得到平均损失对权重的导数，也就是梯度。逻辑回归与交叉熵组合后，导数可以化成一个简洁的式子：对每个例子，用概率与标签之差乘以该项特征，再求平均。

这里可以把导数理解为“把一个权重稍微调大一点，代价会怎样变化”。变化沿着权重、分数、概率、损失逐层传递：分数随该权重变化的快慢是相应特征值，sigmoid的变化率是p(1−p)，损失对概率的变化率则是−y/p+(1−y)/(1−p)。将后两项相乘，分母中的p和1−p分别约掉，留下p−y；再乘特征值，就得到下面每个例子的贡献。这个逐层相乘的规则，就是复合函数求导的链式法则。更深的神经网络会经过更多层，反向传播仍沿这些连接计算参数怎样影响损失。

训练集大小为M；偏置使用恒为1的一列特征

wj ← wj − η × [Σ(k=1…M) (pk − yk) xkj] / M

箭头表示用右边的新值替换原权重。M是训练例子数，k用来逐个编号，x_{kj}是第k个例子的第j项特征，η是学习率，控制每次沿梯度反方向走多远。本例取η=0.15，重复更新800次。例如某个例子y=1、p=0.2、某项标准化特征为1，它对这一项导数的贡献为−0.8；减去负数会增加权重，使下一次相应分数上升。程序中的矩阵乘法一次完成全部例子的相乘和求和，数学含义仍是这项逐例计算。偏置可以看成额外加入了一列恒为1的特征，因此也能用同一个更新式。

完整代码如下。安装NumPy与Matplotlib后可直接运行，结果保存在当前目录下的`representation_outputs`。`samples.json`保存每个序列、图的边、标签、特征和划分；`results.json`保存模型参数、预测概率、训练损失与检查结果。绘图部分直接读取同一次计算中的数组，所以页面上的图、数值和下载文件可以相互对应。先顺着`main`阅读样本怎样生成，再回看`fit_predict`，就能把数据、标准化、训练和预测接起来。

完整Python例子 · NumPy + Matplotlib[下载代码](https://ml-biomat.com/static/tutorials/polymer-ai/assets/108c92748b0907be8c4e0a7a.py)

```python
"""组成、顺序与连接：两个受控的表示学习实验。

运行：python example.py；依赖：numpy、matplotlib。
标签来自下文明确的结构规则，数据由程序生成。
输出含完整样本、划分、模型参数、数值及六幅结果图。
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SEED = 20261022
rng = np.random.default_rng(SEED)
OUT = Path('representation_outputs')
OUT.mkdir(exist_ok=True)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'DejaVu Sans'],
    'font.size': 14, 'axes.titlesize': 13, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.edgecolor': '#a7b9b2',
    'axes.labelcolor': '#24423c', 'text.color': '#24423c',
    'xtick.color': '#536c63', 'ytick.color': '#536c63',
    'figure.facecolor': '#fcfaf5', 'axes.facecolor': '#fcfaf5',
    'svg.fonttype': 'path', 'svg.hashsalt': str(SEED),
})
GREEN, GOLD = '#14786b', '#bc7041'


def switch_fraction(sequence):
    a = np.asarray(sequence)
    return float(np.mean(a[1:] != a[:-1]))


def draw_sequence(n, label, used):
    # 两类都有一半 A、一半 B。只选择变化少/变化多的序列。
    while True:
        a = rng.permutation(np.repeat([0, 1], n // 2))
        c = switch_fraction(a)
        key = tuple(a.tolist())
        if key not in used and (c <= .4 if label == 0 else c >= .6):
            used.add(key)
            return a


def make_graph(n, branched):
    edges = [(i, i + 1) for i in range(n - 1)]
    if branched:
        # 把末端的一个点改接到内部：仍是连通树，出现三叉点。
        edges.pop()
        edges.append((int(rng.integers(1, n - 3)), n - 1))
    # 随机重编号，避免让编号成为提示标签的捷径。
    perm = rng.permutation(n)
    a = np.zeros((n, n), dtype=int)
    for i, j in edges:
        a[perm[i], perm[j]] = a[perm[j], perm[i]] = 1
    return a


def features(a):
    degree = a.sum(axis=1)
    return [len(a), int(a.sum() // 2), float(np.mean(degree >= 3)),
            float(np.mean(degree == 1))]


def sigmoid(z):
    # z 经标准化训练后在有限范围，截断兼顾数值安全。
    return 1 / (1 + np.exp(-np.clip(z, -40, 40)))


def fit_predict(x, y, train, test):
    x = np.asarray(x, dtype=float)
    # 标准化只从训练侧估计；常数列取尺度 1，避免除以零。
    mean, scale = x[train].mean(axis=0), x[train].std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    z = np.column_stack([np.ones(len(x)), (x - mean) / scale])
    weight = np.zeros(z.shape[1])
    history = []
    for _ in range(800):
        p = sigmoid(z[train] @ weight)
        history.append(float(np.mean(np.logaddexp(0, z[train] @ weight)
                                     - y[train] * (z[train] @ weight))))
        gradient = z[train].T @ (p - y[train]) / train.sum()
        weight -= .15 * gradient
    probability = sigmoid(z[test] @ weight)
    prediction = (probability >= .5).astype(int)
    return {'accuracy': float(np.mean(prediction == y[test])),
            'probabilities': probability.tolist(), 'loss': history,
            'mean': mean.tolist(), 'scale': scale.tolist(),
            'weight_with_bias': weight.tolist()}


def main():
    sequences, graphs, groups, labels, used = [], [], [], [], set()
    for group in range(320):
        n = int(rng.integers(8, 21)) * 2
        for label in (0, 1):
            sequences.append(draw_sequence(n, label, used))
            graphs.append(make_graph(n, bool(label)))
            groups.append(group)
            labels.append(label)
    groups, y = np.asarray(groups), np.asarray(labels)
    test_groups = rng.choice(320, 80, replace=False)
    test = np.isin(groups, test_groups)
    train = ~test
    count = np.array([[len(a), np.mean(a == 0)] for a in sequences])
    order = np.column_stack([count, [switch_fraction(a) for a in sequences]])
    graph = np.array([features(a) for a in graphs])
    x = {'sequence_count': count, 'sequence_order': order,
         'graph_count': graph[:, :2], 'graph_degree': graph}
    scores = {name: fit_predict(value, y, train, test) for name, value in x.items()}
    # 结构规则也作直接计算参照；它与学习模型回答的是同一标签问题。
    rule_sequence = (order[test, -1] >= .5).astype(int)
    rule_graph = (graph[test, 2] > 0).astype(int)
    permutation_error = 0.0
    for a in graphs:
        perm = rng.permutation(len(a))
        permutation_error = max(permutation_error, float(np.max(np.abs(
            np.asarray(features(a)) - features(a[perm][:, perm])))))
    checks = {
        'train_test_group_overlap': len(set(groups[train]) & set(groups[test])),
        'unique_sequences': len(used) == len(sequences),
        'each_pair_same_counts': bool(np.all(count[::2] == count[1::2])),
        'each_pair_same_node_edge_counts': bool(np.all(graph[::2, :2] == graph[1::2, :2])),
        'relabel_feature_max_error': permutation_error,
        'sequence_rule_accuracy': float(np.mean(rule_sequence == y[test])),
        'graph_rule_accuracy': float(np.mean(rule_graph == y[test])),
    }
    assert checks['train_test_group_overlap'] == 0
    assert checks['unique_sequences'] and checks['each_pair_same_counts']
    assert checks['each_pair_same_node_edge_counts'] and permutation_error == 0
    assert scores['sequence_count']['accuracy'] == .5
    assert scores['graph_count']['accuracy'] == .5
    result = {'seed': SEED, 'source': 'program_generated_structural_examples',
              'n_groups': 320, 'n_train': int(train.sum()), 'n_test': int(test.sum()),
              'scores': scores, 'checks': checks}
    samples = []
    for i, (seq, a) in enumerate(zip(sequences, graphs)):
        samples.append({'group': int(groups[i]), 'split': 'test' if test[i] else 'train',
                        'label': int(y[i]), 'sequence': ''.join('AB'[v] for v in seq),
                        'edges': np.argwhere(np.triu(a, 1)).tolist(),
                        'sequence_features': order[i].tolist(),
                        'graph_features': graph[i].tolist()})
    (OUT / 'samples.json').write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    def panel_count(ax):
        # 同一组成上两类点重叠：环表示标签 0，实点表示标签 1。
        ax.scatter(count[test & (y == 0), 0], count[test & (y == 0), 1],
                   s=90, facecolors='none', edgecolors=GREEN, label='相邻变化少')
        ax.scatter(count[test & (y == 1), 0], count[test & (y == 1), 1],
                   s=13, c=GOLD, label='相邻变化多')
        ax.set(xlabel='单元数 N', ylabel='A 的比例', ylim=(.42, .58),
               title='A  组成相同，两类点完全重合')
        ax.legend(frameon=False, loc='upper left', fontsize=11)

    def panel_order(ax):
        for label, color, name in [(0, GREEN, '变化少'), (1, GOLD, '变化多')]:
            mask = test & (y == label)
            ax.scatter(order[mask, 0], order[mask, 2], c=color, s=19, alpha=.6, label=name)
        ax.axhspan(.4, .6, color='#dde5df', alpha=.7)
        ax.text(28, .5, '未采样的中间区间', ha='center', fontsize=11)
        ax.set(xlabel='单元数 N', ylabel='相邻变化比例 c', ylim=(0, 1),
               title='B  保留邻居关系后，两类可以分开')

    def panel_loss(ax):
        for key, color, name in [('sequence_count', '#8d9e97', '组成特征'),
                                  ('sequence_order', GREEN, '顺序特征'),
                                  ('graph_degree', GOLD, '连接特征')]:
            ax.plot(scores[key]['loss'], color=color, lw=2,
                    ls='--' if key == 'graph_degree' else '-', label=name)
        ax.set(xlabel='参数更新次数', ylabel='训练集平均交叉熵',
               title='C  相同训练方法，输入信息不同')
        ax.legend(frameon=False, fontsize=11)

    def panel_accuracy(ax):
        names = list(scores)
        values = [100 * scores[k]['accuracy'] for k in names]
        bars = ax.barh(np.arange(4), values, color=['#a6b8ae', GREEN, '#a6b8ae', GOLD], height=.6)
        ax.set_yticks(range(4), ['序列：组成', '序列：组成＋顺序', '图：点数＋边数', '图：加入节点度数'])
        ax.set(xlim=(0, 117), xlabel='独立留出 80 组的准确率 / %',
               title='D  两个任务中的表示对照')
        ax.invert_yaxis()
        for b, value in zip(bars, values):
            ax.text(value + 2, b.get_y() + b.get_height() / 2, f'{value:.1f}', va='center')

    def panel_degree(ax):
        for label, color, shift, name in [(0, GREEN, -.16, '线性树'), (1, GOLD, .16, '分支树')]:
            hist = np.mean([np.bincount(a.sum(axis=1), minlength=4)[1:4] / len(a)
                            for a, v, keep in zip(graphs, y, test) if v == label and keep], axis=0)
            ax.bar(np.arange(1, 4) + shift, hist, width=.3, color=color, label=name)
        ax.set(xticks=[1, 2, 3], xlabel='每个节点直接连接的邻居数', ylabel='测试图内比例的平均值',
               title='E  分支改变了局部连接分布')
        ax.legend(frameon=False, fontsize=11)

    def panel_probability(ax):
        p = np.array(scores['sequence_order']['probabilities'])
        for label, color, name in [(0, GREEN, '变化少'), (1, GOLD, '变化多')]:
            ax.hist(p[y[test] == label], bins=np.linspace(0, 1, 21), alpha=.8, color=color, label=name)
        ax.axvline(.5, ls='--', color='#73867c', lw=1)
        ax.set(xlabel='模型给“变化多”的概率', ylabel='测试序列数',
               title='F  概率是输出，阈值才给类别')
        ax.legend(frameon=False, fontsize=11, loc='upper center')

    panels = [('counts', panel_count), ('order', panel_order), ('loss', panel_loss),
              ('accuracy', panel_accuracy), ('degree', panel_degree), ('probability', panel_probability)]
    for name, draw in panels:
        fig, ax = plt.subplots(figsize=(6.6, 4.6), layout='constrained')
        draw(ax)
        fig.savefig(OUT / f'{name}.svg', metadata={'Date': None})
        plt.close(fig)
    fig, axes = plt.subplots(3, 2, figsize=(14, 13), layout='constrained')
    for (_, draw), ax in zip(panels, axes.ravel()):
        draw(ax)
    fig.savefig(OUT / 'representation_diagnostics.svg', metadata={'Date': None})
    fig.savefig(OUT / 'representation_diagnostics.png', dpi=180)
    plt.close(fig)
    for name, score in scores.items():
        print(f'{name}: 测试准确率 {100 * score["accuracy"]:.1f}%')
    print(f'训练/测试样本：{train.sum()}/{test.sum()}；共有组数：{checks["train_test_group_overlap"]}')
    print(f'节点重新编号后，特征最大变化：{permutation_error:.1f}')
    print('结果与完整样本已保存至 representation_outputs')


if __name__ == '__main__':
    main()
```

本次实际运行输出

```
sequence_count: 测试准确率 50.0%
sequence_order: 测试准确率 100.0%
graph_count: 测试准确率 50.0%
graph_degree: 测试准确率 100.0%
训练/测试样本：480/160；共有组数：0
节点重新编号后，特征最大变化：0.0
结果与完整样本已保存至 representation_outputs
```

一次运行 · 六幅结果图

![A · 相同组成的配对样本在输入坐标上重合。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/884fe3b0042eaf71fbcc8a10.svg)

A · 相同组成的配对样本在输入坐标上重合。

![B · 相邻变化比例补上了与本次标签有关的顺序信息。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/a1fe2e7d5f12c58749d70573.svg)

B · 相邻变化比例补上了与本次标签有关的顺序信息。

![C · 每次更新都使用训练集；组成信息对应的损失保持不变。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/4a9848060311c5edd6accf0b.svg)

C · 每次更新都使用训练集；组成信息对应的损失保持不变。

![D · 两个任务各比较两种输入，完整留出80组作测试。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/0e220dbc261b69834b82338d.svg)

D · 两个任务各比较两种输入，完整留出80组作测试。

![E · 节点的局部邻居数量区分本次线性树和分支树。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/772876553f171b71c398e094.svg)

E · 节点的局部邻居数量区分本次线性树和分支树。

![F · 保留测试概率，观察阈值分类之前的输出。](https://ml-biomat.com/static/tutorials/polymer-ai/assets/51b4a9d20a801d16e5962d70.svg)

F · 保留测试概率，观察阈值分类之前的输出。

**图8** 程序生成的640个例子按320组组织，每组两个标签各一例；两个任务分别训练，使用相同的组划分。序列采样取相邻变化比例不超过0.4或不低于0.6的两个区间。

[矢量组图SVG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/a1b99d64c38d5478ec1afa3a.svg)[高清组图PNG](https://ml-biomat.com/static/tutorials/polymer-ai/assets/d3a557b85f12ebc8cdbe6176.png)[完整样本JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/bb1bf516aeaaf4a70fccd3a2.json)[模型与结果JSON](https://ml-biomat.com/static/tutorials/polymer-ai/assets/622b1a209d0d9cd012d38fb9.json)

图A中，两个标签在组成坐标上重叠；图B加入相邻变化比例后，它们沿纵轴分开。图C显示训练过程：组成特征的损失停在约0.693，也就是对平衡两类始终给出0.5概率时的交叉熵；加入顺序或连接信息后，训练损失随更新下降。这里对照的是同一种学习方法看到不同输入时的表现。配对设计确保长度本身不会替模型提示标签，训练集也包含等量的两类对象。

这次固定种子的运行中，组成表示和点数加边数表示的测试准确率都为50.0%，加入顺序和局部连接特征后都为100.0%。直接按已知结构规则分类也得到100%。把规则计算列在旁边，可以看清学习的作用：逻辑回归从样本中学到了一个能区分本次结构标签的边界，而标签原本就有明确的生成规则。用于生物研究时，我们会保留这样的简单对照，再把输出换成实验定义的活性、识别或材料响应，判断学习方法在那个问题中增加了什么。

图E把图任务中的差别画得更具体：线性树只有端点和二邻居节点；接出分支后，出现三邻居节点，端点比例也相应变化。程序还把每张图的节点重新编号，再算一次特征，最大变化为0.0。这说明本次图特征确实依赖连接，而不依赖编号顺序。图F则保留概率输出，提醒我们准确率只是一个汇总量；对以后没有人为留出间隔的真实任务，还需检查概率与实际发生频率是否相符，并按独立分子或实验批次评价。

可以从两处改动继续探索。先把序列任务的中间区间补回来，再比较训练损失和测试概率怎样变化；接着保留节点度数分布，尝试画出两张连接不同的图，检查当前特征能否辨认。第一处让分类边界附近的例子出现，第二处让局部统计相同而整体关系不同。两种改动都在追问同一个具体问题：当前输入中的哪些差别，足以支撑我们想预测的量？

认识蛋白质、糖链和核酸以后，我们已有了几种记录分子的办法：组成表记录有哪些单元，序列记录沿链的次序，带类型的图记录哪些位置怎样连接。接下来还要把这些对象放回环境中。同一条链进入不同的水溶液，改变温度、酸碱度或盐含量，可能表现出不同的接触与构象。第四节将从这些熟悉的实验操作出发，解释环境变量为什么也必须进入科学模型和AI的数据表。

## 资料与延伸阅读

1. Frederick Sanger，1958，[The Chemistry of Insulin](https://www.nobelprize.org/uploads/2018/06/sanger-lecture.pdf)。关于胰岛素序列及连接分析的诺贝尔演讲。
2. Hermann Staudinger，1953，[Macromolecular Chemistry](https://www.nobelprize.org/uploads/2018/06/staudinger-lecture.pdf)。天然与合成高分子的连接观念。
3. 1953年DNA结构论文：[Watson与Crick](https://doi.org/10.1038/171737a0)；[Wilkins、Stokes与Wilson](https://doi.org/10.1038/171738a0)；[Franklin与Gosling](https://doi.org/10.1038/171740a0)。
4. Dayhoff、Eck、Chang与Sochard，1965，[Atlas of Protein Sequence and Structure](https://ntrs.nasa.gov/citations/19660014530)，NASA档案中的原始汇编。
5. Gilmer等，2017，[Neural Message Passing for Quantum Chemistry](https://proceedings.mlr.press/v70/gilmer17a.html)，PMLR 70:1263–1272。

图中简化连接采用本节绘制的概念示意，符号含义以各图说明为准。Python样本、标签和六幅统计结果由页面中的代码生成。
