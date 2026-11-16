# 不只认出物体：定位、轮廓与运动

Source: https://ml-biomat.com/tutorials/machine-learning/m13/
Language: zh-CN

检测、分割、视频跟踪、姿态和 OCR，围绕输出结构读懂视觉系统。

## 1. 认出一辆车以后，还要回答哪些问题

在路口看一段视频，“画面里有车”只是第一层信息。要统计车辆数量，需要把每辆车的位置找出来；要估计车辆占据的路面范围，需要勾出轮廓；要判断车辆是否逆行，需要把连续画面中的同一辆车连起来。若任务变成读取车牌，还需要从一片像素中恢复有顺序的字符。图像分类把整张图压成一个类别，而这些任务要求输出保留位置、形状、身份和时间。输出结构变了，标注方式、模型设计和评估方法也要跟着改变。

可以把一帧图像想成一张城市地图。检测框像在地图上圈出建筑的大致范围，分割掩码像精确描出占地边界，关键点像标出门窗等重要位置，跟踪轨迹则记录某个对象怎样移动。框并不包含轮廓的全部信息，掩码也不自动告诉我们哪一个对象与上一帧对应。先决定最终要做什么，才能选择足够而不过度复杂的输出。停车场计数未必需要每个轮胎的精确边界，而测量细长裂缝宽度时，一个矩形框又明显不够。

本章把这些任务放在同一条理解路径上：先计算两个框有多重合，理解检测如何处理重复预测；再训练一个小型 U 形网络，让每个像素得到前景概率；随后把检测结果沿时间关联，观察两条相交轨迹什么时候会换错身份。代码中的图像由圆和矩形合成，生成规则与真值完全明确，便于逐像素检查。大规模检测器、可提示分割和 OCR 的结构会围绕各自的输入输出展开，使你能把这个可运行的小实验接到更完整的视觉系统中。

## 2. 框准不准，不能只看中心有没有落在物体上

一个轴对齐边界框可以用左上角和右下角的四个数字表示。这里规定横坐标向右、纵坐标向下，坐标表示像素边界，宽度就是右边界减左边界，不额外加 1。这个约定看似细小，却会影响面积和重叠计算。把图像缩小一半时，四个坐标也应缩小一半；若先补边再缩放，则需要同时记录平移和比例，才能把网络输出放回原图。很多肉眼看来“框总差一点”的问题，实际出在预处理坐标没有正确还原。

$$
w_\cap=\max(0,\min(x_2,x_2')-\max(x_1,x_1')),\quad h_\cap=\max(0,\min(y_2,y_2')-\max(y_1,y_1')),\qquad \operatorname{IoU}=\frac{w_\cap h_\cap}{(x_2-x_1)(y_2-y_1)+(x_2'-x_1')(y_2'-y_1')-w_\cap h_\cap}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d552cb9f1aa1fec81772895c.svg) | 第一个框的左、上、右、下边界，单位px；右大于左、下大于上。 |
| ![Formula](https://ml-biomat.com/static/agent-math/41d1fa18a670d3fb43df055a.svg) | 第二个框对应边界，单位px；撇号区分两个框，不表示导数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/67de279b9227ab3828a2ac64.svg) | 交集宽度和高度，单位px；不相交方向用0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/edf6d089f5f2b0f0b5fc3470.svg) | 交并比，0至1，无量纲；面积单位px²相消。 |

交集使用更靠内的边界；并集把两面积相加，再减去被重复计算的交集。框(0,0,10,10)与(5,0,15,10)交集宽5、高10，面积50；并集100+100−50=150，因此IoU=1/3。完全重合为1，完全分开为0。这里使用连续像素边界约定，面积不额外加1。

交并比 IoU 用重叠面积除以两个框覆盖的总面积。它同时惩罚偏移、框得过大和框得过小，比“预测中心在真值框里”更能反映定位质量。两个 10×10 的框水平错开 5 个像素，交集是 50，覆盖总面积是 150，IoU 为三分之一。小目标对几像素的偏差尤其敏感：同样偏移 2 个像素，对宽 8 的目标和宽 80 的目标影响很不一样。因此，检查总体指标时还应按目标尺寸查看错误，不能让大目标的好表现遮住小目标的漏检。

检测器常为同一个物体产生多个相近框。非极大值抑制 NMS 先保留置信分数最高的框，再删除与它重叠超过阈值的同类框，重复直到候选处理完。注意顺序：阈值越低，抑制越强；阈值越高，越容易保留重叠框。拥挤场景中两个人本来就会高度重叠，过强抑制可能把真实对象删掉。NMS 的重叠阈值、输出置信阈值和评估时的 IoU 阈值承担三个不同任务，应该分别命名和调节。

### 框的实验：偏移、重复与阈值

灰色区域是两个真实对象；三个彩色框是同一类别的候选。虚线表示候选被过滤。右侧计算经过NMS后，在评价IoU≥0.5时的当前精确率与召回率。

[Figure: 真实对象、候选框与保留结果，附交并比和匹配统计](https://ml-biomat.com/tutorials/machine-learning/m13/#M13-svg)

评价时先按置信度排序，并在指定 IoU 条件下将预测与真值一对一匹配。同一个真值只能被一个预测正确认领，多出的重复框计为假阳性。精确率回答“报出的有多少是真的”，召回率回答“真实对象找到了多少”；不断改变置信阈值，就得到一条精确率—召回率曲线。AP 汇总这条曲线，mAP 再按类别或规定的 IoU 条件求平均。比较论文数字时必须核对采用的是 AP50、AP75，还是从 0.50 到 0.95 多阈值的汇总，因为它们对定位精细程度的要求不同。

$$
\operatorname{Precision}=\frac{TP}{TP+FP},\qquad \operatorname{Recall}=\frac{TP}{TP+FN}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fedfc0b572b83a7991e52748.svg) | 按类别与指定IoU阈值一对一匹配成功的预测数，无量纲计数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/479b502526ba6c1154af06a5.svg) | 没有匹配成功的预测数，包含重复框，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f6b50c71aba1b713f18bdba.svg) | 没有被正确预测匹配的真值对象数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3d052e2baf25a3b565522340.svg) | 精确率和召回率，0至1的无量纲比例；分母为0时采用明示的评估约定。 |

真实有5个对象，预测6个框，其中4个一对一匹配正确，则TP=4、FP=2、FN=1，精确率4/6≈0.667，召回率4/5=0.8。提高置信阈值可能同时减少假阳性和真阳性，因此要沿不同阈值观察变化。AP需要整条排序曲线及指定插值规则，不能把某一个阈值的精确率直接叫AP。

## 3. 先提出候选，直接预测，还是一次给出一个集合

两阶段检测把“哪里值得看”和“那里是什么”分开处理。以 Faster R-CNN 一类系统为例，共享骨干网络先计算特征图，区域提议网络给出可能包含物体的区域，再从这些区域提取对齐后的特征，完成分类和位置修正。它像先在整张地图上圈出候选区域，再仔细检查每一处。共享特征避免为每个候选重新处理整张原图，区域特征则允许后续分支聚焦对象。若继续给每个候选输出掩码，就能走向实例分割。

单阶段检测把类别和位置预测直接铺在一个或多个特征图上。Redmon 等人在 2015 年发布的 YOLO 工作，将检测整理为整图到类别与边界框的联合预测；SSD 则明确利用多个尺度的特征图处理不同大小的对象。高分辨率特征图保留细节，适合小目标；较低分辨率特征图的单个位置能观察更大范围。锚框方法从预设的尺度与长宽比出发学习偏移，中心点或其他无锚框方法则从位置或距离表达对象边界。它们共同面对正负样本不平衡和不同尺度目标的分配问题。

![D2L 的 SSD 多尺度结构原图](https://ml-biomat.com/static/tutorials/machine-learning/figures/a0891e7ebb443d0779b0d0d8.svg?v=a0891e7ebb44)

图 1D2L 的 SSD 多尺度结构原图。沿逐级缩小的特征图观察类别与位置预测如何处理不同大小的对象。Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola，Dive into Deep Learning，Fig. 14.7.1，https://d2l.ai/chapter_computer-vision/ssd.html，CC BY-SA 4.0；原图未改动。

不必先记住所有检测器缩写，可以先核对输出张量。一个 20×20 的特征图，每个位置设 3 个锚框、2 个对象类别，再加背景类，需要 20×20×3×3 个分类分数，以及 20×20×3×4 个位置参数。网络输出大量候选后，还需要把参数解码成原图坐标并处理重复。这个算例说明为什么检测头常使用卷积：空间位置不同，但预测同类局部信息的规则可以共享。具体网络还会采用不同的背景定义、目标分配和损失形式，维度应与实现逐一对齐。

Carion 等人在 2020 年提出的 DETR 把检测看成集合预测。它使用一组可学习的对象查询，直接输出固定数量的候选槽位，未对应物体的槽位学习“无对象”。训练时，二分图匹配为真值与预测寻找一对一分配，再同时优化类别与位置。假设有两个真值和三个输出槽位，匹配选择最合适的两个槽位负责这两个对象，第三个学习空类别。由集合损失鼓励唯一预测，是其去掉常规锚框生成与 NMS 流程的关键。具体速度、训练收敛和小目标表现仍取决于实现、尺度与训练配置。

## 4. 把一个类别扩展到每个像素

语义分割给每个像素分配类别，例如道路、车辆或天空；两辆车相互接触时，车辆像素仍属于同一语义类别。实例分割进一步区分“第一辆车”和“第二辆车”，所以不仅要知道类别，还要知道对象归属。全景分割把可数对象的实例与道路、天空这类连续背景区域统一成覆盖画面的表示。若你想数有多少个相互接触的圆，把二元前景掩码连通域的数量当作对象数量就会出错：两圆接触后属于一个连通区域，但仍然是两个对象。

分割的困难在于同时需要语义背景和准确位置。缩小特征图有利于扩大观察范围，却会丢掉边界细节；只在很小的窗口里判断，又可能分不清对象和相似纹理。Ronneberger、Fischer 与 Brox 在 2015 年的 U-Net 中，用收缩路径获取背景信息，用扩张路径恢复空间分辨率，并把对应尺度的高分辨率特征连接到解码端。这条跳跃连接像给正在绘制大轮廓的人递回最初的细节草图。它不是简单把小图放大，而是让解码器学习怎样结合上下文与精确位置。

$$
p_i=\frac{1}{1+e^{-z_i}},\qquad \mathcal L=-\frac1N\sum_{i=1}^{N}\big[y_i\log p_i+(1-y_i)\log(1-p_i)\big]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | 当前批次的像素总数与像素索引；无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/29337fa51cf400a673c72b86.svg) | 像素i的前景logit与sigmoid概率，无量纲；网络输出形状B×1×H×W。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6efa4604c774374baf410795.svg) | 批次图像数、像素高度和像素宽度；代码为B×1×48×48。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d904ffb3258f0e94299beb6e.svg) | 0或1的真实前景标记、平均二元交叉熵、自然对数；损失单位为nat/像素。 |

y=1时只留下−log p，y=0时只留下−log(1−p)，因此给真值更高概率会降低损失。一个前景像素预测0.8，损失−ln0.8≈0.2231；一个背景像素也预测前景概率0.8，损失−ln0.2≈1.6094。代码用binary_cross_entropy_with_logits直接处理z，避免先算极端概率再取对数造成数值问题；绘图时才计算sigmoid。

我们的二元分割网络输出每个像素属于前景的 logit，训练时使用数值稳定的二元交叉熵；展示时再经 sigmoid 转成概率，并以 0.5 划分前景。前景面积通常小于背景面积，只报像素准确率容易产生错觉：若背景占 95%，全部预测成背景就已有 95% 准确率，却一个对象也没有找到。前景 IoU 与 Dice 直接比较预测区域和真实区域的重叠，边界误差或按对象统计则补充它们忽略的细节。不同图像先各自计算再平均，与把所有像素合并后计算是两种不同权重方式。

$$
\operatorname{IoU}_{\rm mask}=\frac{|P\cap G|}{|P|+|G|-|P\cap G|},\qquad \operatorname{Dice}=\frac{2|P\cap G|}{|P|+|G|}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/939924d4ef9cfd6c8974e1c1.svg) | 二值预测前景像素集合与真实前景像素集合；P由概率阈值形成。 |
| ![Formula](https://ml-biomat.com/static/agent-math/614e03b6a4b537e0c9c4b390.svg) | 各集合及交集的像素数，单位pixel count。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aa08102b6650df285e8ee2b7.svg) | 区域IoU与Dice重叠系数，0至1，无量纲；本实验每张图都有真实前景。 |

预测有8个前景像素，真值有10个，其中6个重合，则并集8+10−6=12，IoU=6/12=0.5，Dice=12/18≈0.667。两者都关注前景但刻度不同，不能直接比较数值大小来决定哪个模型更好。本章先对每张图计算，再对40张图求算术平均，因此每张图权重相同；空前景图的约定需另行明确。

可提示分割把人希望分出的对象也作为输入。2023 年的 SAM 将图像编码、点或框等提示编码，以及掩码解码结合起来；同一张图可以先缓存图像表示，再根据不同提示快速生成候选掩码。一个正点说“这一带属于我要的对象”，一个负点说“这里不要纳入”，框则限定大致区域。对象可能存在多层含义：点在车轮上，用户可能想要车轮，也可能想要整辆车，因此多个候选和交互修正有实际作用。提示描述的是选择意图，并不替代类别定义或标注规范。

2024 年的 SAM 2 把可提示分割扩展到视频，并使用流式记忆保留跨帧信息。对于某一帧漏掉的部位，补充提示可以影响后续的对象传播。实际工作中需要确定标的是可见部分还是推断出的完整对象，遮挡出现时是否继续维持身份，以及多对象接触时怎样区分。通用分割模型提供了有用的对象先验；细线、透明物体、低对比度边界和特殊成像条件，则值得用相应样本单独检查和补充训练。评价应与最终测量目标一起设计。

## 5. 从一张图到一段视频：位移、身份和动作

光流描述像素的表观位移：某个位置在下一帧移动到了哪里。它可能由对象运动引起，也可能由相机运动引起，所以光流箭头并不等同于对象在真实三维空间中的速度。经典推导先假定短时间内同一表面点的亮度近似不变，把下一帧亮度做一阶展开，得到空间梯度、时间梯度和位移速度之间的关系。一条直边只能约束垂直于边的运动，沿边滑动可能几乎不改变局部图像，这就是为什么单个像素的信息不足以唯一求出两个运动分量。

$$
I_x u+I_y v+I_t=0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/338ef8468bcc4575db37ec2d.svg) | 位置(x,y)、时间t的图像亮度；这里亮度已归一化为无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e6b967262bd6322703a3df2.svg) | 对横、纵坐标及时间的偏导数；单位分别为亮度/px、亮度/px、亮度/frame。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8d978f4f1831d626cb3d5ca1.svg) | 每帧的水平和垂直位移速度，px/frame；若时间采用秒，则相应改为px/s。 |

从亮度近似守恒I(x,y,t)≈I(x+uΔt,y+vΔt,t+Δt)出发，一阶展开并除以Δt，得到本式。若Ix=2、Iy=0、It=−6，方程给u=3 px/frame，而v仍未确定。需要邻域内更多独立梯度约束，才能求两个分量；大位移与亮度变化会增加一阶近似和守恒假设的误差。

Lucas–Kanade 一类方法在小邻域内假定运动相近，用多个像素的梯度方程一起估计位移；图像金字塔把较大位移先放到较低分辨率上处理。低纹理区域、反光或遮挡会削弱这些假设。现代学习式方法可以学习特征匹配与更新规则，但仍需要区分图像证据充分的位置与遮挡后没有直接对应的位置。光流适合像素级运动分析；多对象跟踪则把检测到的对象连成带身份的轨迹，通常结合位置预测、外观相似性和一对一匹配。

只把当前检测框接到上一帧最近的框，在两个人交叉走过时可能交换身份。简单的恒速度预测先用前两帧估计移动方向，再预测下一帧位置，匹配时比较预测位置与新检测。代码中的两个对象在第 9 与第 10 帧之间交错，逐帧检测都存在；最近位置关联发生 2 次身份切换，而恒速度关联为 0。这个受控例子拆开了检测错误与关联错误。遇到急转弯或长时间遮挡，恒速度也需要外观信息、轨迹寿命和重新识别等机制补充。

ByteTrack 的 2021 年预印本关注另一个常见现象：被遮挡的真实对象往往得到较低检测分数，直接丢掉它们会打断轨迹。它先关联较高分检测，再利用剩余轨迹与较低分检测进行第二轮关联，让运动一致的低分观测有机会延续已有身份。检测精确率、身份保持和轨迹完整性因此不能由一个框指标代替。IDF1、HOTA 等指标从身份或关联角度补充评价；逐帧回放则帮助定位身份究竟从哪一刻开始出错。

视频理解又把输出推进到事件层面。“打开门”和“关上门”可能包含近似的单帧画面，先后顺序决定动作类别。三维卷积在空间与时间窗口内共同提取模式，逐帧编码后接循环模型可以积累历史，时空 Transformer 则通过注意力建立跨位置和跨帧关系。片段分类给一段视频一个标签；时序动作定位还要输出动作的起止时间；逐帧动作分割则把连续长视频切成有语义的阶段。标注开始与结束的规则、视频帧率和允许使用未来帧的范围，都要与使用场景一致。

## 6. 有结构的对象：关节连成姿态，字符组成文字

姿态估计用少量关键点表达身体或物体的结构，例如肩、肘、腕。自顶向下的方法先检测每个人，再在个人区域内预测关键点；自底向上的方法先在全图寻找关节，再把属于同一个人的关节组合起来。前者把难度分解为定位人和定位关节，漏掉人框也会漏掉整个人；后者需要在拥挤场景中解决关节归属。关键点可以直接回归坐标，也可以预测一张热图，让每个像素表示某个关节出现的可能程度。热图保留空间上的多解线索，峰值位置再转换回原图坐标。

假设原图中的人物框是 200×400 像素，缩放到 100×200 输入后，模型在热图中给出的腕部位置还需要乘回尺度并加上框的左上角偏移。若热图又比输入缩小 4 倍，这一级比例也要恢复。评价关键点时，误差应相对对象尺度解释：手腕偏差 5 像素对远处小人和近处大人意义不同，PCK 或 OKS 等指标因此采用尺度相关的容差。不可见关节还需要可见性标记，区分“未标注”“遮挡但有推定位置”和“确实可见”，避免把不同信息状态混作同一真值。

OCR 的目标是把图像中的文字恢复成有顺序的字符。完整系统通常先检测文字区域，再矫正方向或透视，随后识别字符序列，最后恢复阅读顺序。PP-OCR 在 2020 年展示了轻量文字检测、方向分类与识别的组合。这里的检测框可能是倾斜四边形，弯曲文字甚至需要更细的边界；裁切错一小段字头，就可能让后续识别器再强也读不回来。把“找到了文字”与“读对了文字”分开评估，有助于定位整个系统的误差来源。

字符序列的长度通常事先未知，也没有逐字符边界。采用 CTC 的识别器沿图像宽度输出一串字符或空白分数，再把连续重复和空白折叠成文字。以一个简化路径 A、A、空白、B、B 为例，先合并连续重复再去掉空白，得到 AB；A、空白、A 则保留为 AA。训练会汇总多条能够产生相同目标文本的对齐路径，因而不要求手工给每个字符切块。基于注意力的解码器则逐步生成字符，并根据视觉特征选择关注位置；语言习惯可以帮助辨认，也可能把罕见编号改成更常见的词。

$$
\operatorname{CER}=\frac{S+D+I}{N}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/13068cfa28766b99858d616e.svg) | 把真值转成识别文本所需的最少编辑中，替换、删除、插入的次数；均为字符计数，I此处不是图像亮度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 非空真值文本的字符数；处理空格、大小写等规范应在计算前固定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d3283f595665abbe12efce0d.svg) | 字符错误率，无量纲；插入很多时可超过1。 |

以真值到识别结果的编辑方向计数，真值2074变成204需删除7，所以D=1，CER=1/4；变成2074A需插入A，I=1，同样为1/4。总编辑距离与方向无关，但插入删除的命名随方向互换，评估实现需固定方向。全串准确率则只统计完整一致的字符串，适合编号任务。

字符错误率 CER 用替换、删除和插入的编辑次数除以真值字符数。真值“2074”识别为“204”，删除一个字符，CER 为 1/4；若读成“2074A”，插入一个字符，CER 也是 1/4。对快递编号或实验样本编号，整串完全正确率往往更贴近实际用途，因为一个字符错就可能指向另一个对象。自然文档还需要检查多栏顺序、表格单元和标点，评估前应明确大小写、空格和全半角如何处理。视觉识别的输出最终要进入具体流程，合适的指标来自那个流程会怎样使用结果。

## 7. 完整实验：让掩码、误差与轨迹一起出现

下面的完整脚本生成 160 张训练图、40 张验证图和 40 张测试图，各自使用独立随机种子。每张 48×48 的灰度图包含一到三个圆或矩形，背景带有轻微亮度梯度，再加入标准差为 0.14 的高斯噪声。前景真值是所有形状的并集；重叠形状在本实验里属于同一语义前景。网络只有一次下采样与上采样，在高分辨率路径和低分辨率路径之间保留跳跃连接，因此可直接看清 U 形结构的计算过程。

### 完整 Python：像素分割与身份关联

依赖NumPy、SciPy、PyTorch、Matplotlib。运行 main.py --output output --language zh，可改为en生成英文图。脚本训练小型U形网络、保存每张测试图的概率与重叠指标，再独立计算NMS与两种关联轨迹，所有输出写入指定目录。

```
"""Pixel segmentation, component boxes, NMS, and temporal association."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

torch.set_num_threads(2)


def make_images(n, seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[:48, :48]
    images, masks = [], []
    for _ in range(n):
        mask = np.zeros((48,48), bool)
        for obj in range(rng.integers(1,4)):
            x,y=rng.integers(9,39,2); size=rng.integers(4,9)
            if obj%2: shape=(abs(xx-x)<size)&(abs(yy-y)<size)
            else: shape=(xx-x)**2+(yy-y)**2<size**2
            mask |= shape
        background=.15+.08*xx/48
        image=np.clip(background+mask*rng.uniform(.35,.65)+rng.normal(0,.14,(48,48)),0,1)
        images.append(image);masks.append(mask)
    return np.array(images,dtype=np.float32)[:,None], np.array(masks,dtype=np.float32)[:,None]


class SmallUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.high=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.Conv2d(8,8,3,padding=1),nn.ReLU())
        self.low=nn.Sequential(nn.MaxPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),nn.Conv2d(16,16,3,padding=1),nn.ReLU())
        self.output=nn.Sequential(nn.Conv2d(24,8,3,padding=1),nn.ReLU(),nn.Conv2d(8,1,1))

    def forward(self,x):
        high=self.high(x);low=self.low(high)
        up=nn.functional.interpolate(low,size=high.shape[-2:],mode='bilinear',align_corners=False)
        return self.output(torch.cat([high,up],dim=1))


def iou(box1,box2):
    x1,y1=np.maximum(box1[:2],box2[:2]);x2,y2=np.minimum(box1[2:],box2[2:])
    intersection=max(0,x2-x1)*max(0,y2-y1)
    area1=np.prod(np.array(box1[2:])-box1[:2]);area2=np.prod(np.array(box2[2:])-box2[:2])
    return intersection/(area1+area2-intersection)


def nms(boxes,scores,threshold):
    order=np.argsort(-np.asarray(scores));keep=[]
    while len(order):
        selected=int(order[0]);keep.append(selected)
        order=np.array([i for i in order[1:] if iou(boxes[selected],boxes[i])<=threshold],dtype=int)
    return keep


def box_components(mask):
    labels,n=ndimage.label(mask)
    boxes=[]
    for i in range(1,n+1):
        y,x=np.where(labels==i)
        if len(x)>=12:boxes.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
    return boxes


def track(use_velocity):
    frames=np.arange(21)
    truth=np.stack([np.column_stack([8+2*frames,24+0*frames]),np.column_stack([46-2*frames,25+0*frames])],axis=1)
    rng=np.random.default_rng(9);observed=truth+rng.normal(0,.12,truth.shape)
    previous=observed[0].copy();velocity=np.zeros((2,2));history=[previous.copy()];identities=[np.array([0,1])]
    for obs in observed[1:]:
        predicted=previous+velocity if use_velocity else previous
        cost=np.square(predicted[:,None,:]-obs[None,:,:]).sum(2)
        _,col=linear_sum_assignment(cost)
        current=obs[col];velocity=current-previous;previous=current
        history.append(current.copy());identities.append(col)
    identities=np.array(identities)
    switches=int(np.sum(identities[1:]!=identities[:-1]))
    return truth,np.array(history),switches


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def text(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    torch.manual_seed(12)
    xt,yt=map(torch.tensor,make_images(160,100));xv,yv=map(torch.tensor,make_images(40,200))
    test_x,test_y=make_images(40,300);model=SmallUNet();optimizer=torch.optim.Adam(model.parameters(),lr=.003)
    best=float('inf');history=[]
    for epoch in range(25):
        model.train();losses=[]
        for indices in torch.randperm(160).split(20):
            optimizer.zero_grad();loss=nn.functional.binary_cross_entropy_with_logits(model(xt[indices]),yt[indices])
            loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad(): val=nn.functional.binary_cross_entropy_with_logits(model(xv),yv).item()
        history.append([float(np.mean(losses)),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    with torch.no_grad():probability=torch.sigmoid(model(torch.tensor(test_x))).numpy()[:,0]
    truth=test_y[:,0].astype(bool);predicted=probability>=.5;baseline=test_x[:,0]>=.45
    def overlap(pred):
        inter=(pred&truth).sum((1,2));union=(pred|truth).sum((1,2))
        return inter/union,2*inter/(pred.sum((1,2))+truth.sum((1,2)))
    score,dice=overlap(predicted);base_score,_=overlap(baseline)
    boxes=[[5,5,25,25],[7,6,27,26],[30,10,44,25]];scores=[.9,.8,.7]
    assert abs(iou([0,0,10,10],[5,0,15,10])-1/3)<1e-12
    assert nms(boxes,scores,.5)==[0,2]
    trajectories={}
    for method in ['position','velocity']:
        true_track,estimated,switches=track(method=='velocity')
        trajectories[method]=(estimated,switches)
    summary={'test_images':40,'mean_foreground_iou':float(score.mean()),'mean_dice':float(dice.mean()),
             'intensity_baseline_iou':float(base_score.mean()),'selected_epoch':int(np.argmin(np.array(history)[:,1])+1),
             'nms_kept':nms(boxes,scores,.5),'position_identity_switches':trajectories['position'][1],
             'velocity_identity_switches':trajectories['velocity'][1]}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',test_images=test_x,test_masks=test_y,probability=probability,
             history=history,iou=score,dice=dice,baseline_iou=base_score,true_track=true_track,
             position_track=trajectories['position'][0],velocity_track=trajectories['velocity'][0])
    selected=[0,1,int(np.argmin(score))];fig,axs=plt.subplots(3,4,figsize=(12,8))
    titles=[text('带噪输入','Noisy input'),text('真实前景','Ground-truth foreground'),text('预测概率','Predicted probability'),text('错误与连通域框','Errors and component boxes')]
    for row,index in enumerate(selected):
        axs[row,0].imshow(test_x[index,0],cmap='gray',vmin=0,vmax=1)
        axs[row,1].imshow(truth[index],cmap='gray',vmin=0,vmax=1)
        im=axs[row,2].imshow(probability[index],cmap='viridis',vmin=0,vmax=1)
        rgb=np.stack([truth[index]*.2]*3,axis=-1);rgb[predicted[index]&~truth[index]]=[.8,.3,.2];rgb[~predicted[index]&truth[index]]=[.1,.6,.8]
        axs[row,3].imshow(rgb)
        for x1,y1,x2,y2 in box_components(predicted[index]):axs[row,3].add_patch(Rectangle((x1-.5,y1-.5),x2-x1,y2-y1,fill=False,edgecolor='#e8bd52',lw=1))
        axs[row,0].set_ylabel(f'#{index} | IoU={score[index]:.3f}')
        for col in range(4):
            axs[row,col].set_xticks([]);axs[row,col].set_yticks([])
            if row==0:axs[row,col].set_title(titles[col])
    fig.tight_layout(rect=(0,.075,1,1))
    color_axis=fig.add_axes([.535,.035,.17,.012])
    fig.colorbar(im,cax=color_axis,orientation='horizontal',ticks=[0,.5,1],label=text('前景概率','Foreground probability'))
    save(fig,'segmentation')
    fig,axs=plt.subplots(1,3,figsize=(12,3.7),gridspec_kw={'width_ratios':[1.1,1,.9]})
    history=np.array(history)
    axs[0].plot(np.arange(1,26),history[:,0],label=text('训练','Training'),color='#176b91')
    axs[0].plot(np.arange(1,26),history[:,1],label=text('验证','Validation'),color='#bb554d')
    axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('像素二元交叉熵','Pixel binary cross-entropy'));axs[0].legend()
    axs[1].scatter(base_score,score,c='#176b91',s=24);axs[1].plot([0,1],[0,1],'--',c='#999')
    axs[1].set(xlim=(0,1),ylim=(0,1),xlabel=text('强度阈值基线IoU','Intensity-threshold IoU'),ylabel=text('小型U形网络IoU','Small U-shaped network IoU'),aspect='equal')
    for i,b in enumerate(boxes):
        axs[2].add_patch(Rectangle((b[0],b[1]),b[2]-b[0],b[3]-b[1],fill=False,lw=2,ls='--' if i==1 else '-',edgecolor=['#176b91','#bb554d','#8f711b'][i]))
        axs[2].text(b[0],b[3]+3 if i==1 else b[1]-1,f'{i}: {scores[i]}',fontsize=9)
    axs[2].set(xlim=(0,48),ylim=(35,0),aspect='equal',xlabel=text('横坐标 / px','Horizontal / px'),ylabel=text('纵坐标 / px','Vertical / px'),title=text('NMS保留0、2','NMS retains 0 and 2'))
    fig.tight_layout();save(fig,'metrics')
    fig,axs=plt.subplots(2,2,figsize=(12,4.2),gridspec_kw={'height_ratios':[1,.35]})
    for j,method in enumerate(['position','velocity']):
        estimated,switches=trajectories[method]
        for k,c in enumerate(['#176b91','#bb554d']):
            axs[0,j].plot(np.arange(21),true_track[:,k,0],'--',color='#adb6bc',lw=3)
            axs[0,j].plot(np.arange(21),estimated[:,k,0],color=c,label=f'ID {k+1}')
        method_name={'position':'位置关联','velocity':'速度预测关联'}[method]
        axs[0,j].set(xlabel=text('帧编号','Frame'),ylabel=text('横坐标 / px','Horizontal / px'),xticks=np.arange(0,21,5),title=text(f'{method_name}：身份切换{switches}次',f'{method}: {switches} identity switches'));axs[0,j].legend()
        axs[1,j].axis('off')
        for a,t in enumerate([0,7,10,13,20]):
            inset=axs[1,j].inset_axes([a*.2,0,.18,.9]);inset.set(xlim=(0,58),ylim=(34,16),aspect='equal')
            for k,c in enumerate(['#176b91','#bb554d']):
                px,py=estimated[t,k];inset.add_patch(Rectangle((px-3,py-3),6,6,fill=False,edgecolor=c,lw=2));inset.text(px,py-5,str(k+1),color=c,ha='center')
            inset.set_title(f't={t}',fontsize=9);inset.set_xticks([]);inset.set_yticks([])
    fig.tight_layout();save(fig,'tracking')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

训练共 25 轮，每批 20 张图，用验证二元交叉熵选择检查点。实际选择的是第 25 轮；在 40 张测试图上，逐图平均的前景 IoU 为 0.9082，Dice 为 0.9499。直接把灰度大于 0.45 的像素当作前景，平均 IoU 为 0.6363。这个基线说明空间上下文怎样帮助过滤噪声。下图展示测试图 0、1，以及测试集中 IoU 最低的图；最后一列红色表示假阳性，蓝色表示漏掉的前景，黄色框来自预测掩码的连通区域。

![测试图像0、1与最低IoU样本的真实输出](https://ml-biomat.com/static/tutorials/machine-learning/figures/ef8f917bed1a7bb680ea251d.svg?v=ef8f917bed1a)

图 2测试图像0、1与最低IoU样本的真实输出。输入与概率范围为0至1，掩码为二值；末列红色是假阳性，蓝色是漏检，黄色是至少12像素预测连通域的框。图像均48×48 px，各行编号与IoU在左侧。

连通域框是从分割结果计算得到的几何框，每个区域至少包含 12 个像素；脚本没有训练独立目标检测头，也没有给这些框学习检测置信度。这个处理适合展示掩码怎样转为粗位置输出，尤其能看到接触对象为什么会合成一个区域。指标图保留每一张测试图的基线与网络 IoU 对照，虚线表示两种方法得分相同。右侧 NMS 示例使用三个明确给定的框和分数，独立于分割训练，方便把框去重的运算逐项核对。

![左：训练与验证二元交叉熵；中：40张测试图的逐图IoU，虚线表示与强度阈值基线相同；右：独立给定候选的NMS，阈值0.5，虚线框1被框0抑制，保留框0与2](https://ml-biomat.com/static/tutorials/machine-learning/figures/00d6cd32a43cce560d5de4e2.svg?v=00d6cd32a43c)

图 3左：训练与验证二元交叉熵；中：40张测试图的逐图IoU，虚线表示与强度阈值基线相同；右：独立给定候选的NMS，阈值0.5，虚线框1被框0抑制，保留框0与2。

最后一组图显示完整的 21 帧合成轨迹。虚线是两个对象的真实横坐标，彩色曲线按估计身份连接观测；下方选取五帧展示身份框。位置关联在交叉之后把两条路径接错，恒速度关联则保持对应。脚本中的检测中心直接由真值加小幅噪声得到，所以这里比较的是关联规则本身，不包含图像检测器的漏检。若要研究遮挡，可以接着删除若干帧的一部分检测，再增加轨迹预测保留和重新匹配；每增加一个环节，都能用同样的回放检查它修复了哪一种错误。

![两种关联规则处理同一21帧观测](https://ml-biomat.com/static/tutorials/machine-learning/figures/51c7a3f702bcc6fbd09e99e4.svg?v=51c7a3f702bc)

图 4两种关联规则处理同一21帧观测。上：横坐标随帧变化，灰虚线是真值，颜色为估计身份；下：五个选定帧的身份框。仅比较位置出现2次身份切换，恒速度预测为0；中心观测来自真值加标准差0.12 px噪声。

## 8. 从一幅漂亮结果到可用的视觉测量

一个可用的视觉项目从标注约定开始。框是包住可见部分还是完整对象，掩码是否包含透明区域，关键点遮挡时怎么标，动作从接触物体开始还是从身体启动开始，这些决定会进入训练目标。先让两个人独立标注一小组代表性样本，比较分歧发生在哪里，再把规则写清楚，通常比盲目增加样本更有帮助。对象、场景和视频片段应作为划分单位；同一段视频的相邻帧随机分到训练和测试，会让相似背景与近乎重复的姿态同时出现在两边。

图像分辨率、速度和精度之间的关系也需要实测。缩小输入会节省计算，却可能让细小文字只剩几列像素；分块处理保留分辨率，又需要处理重叠区合并和跨块对象。报告速度时应说明是否包含解码图像、预处理、网络推理、NMS 和结果传输，批量吞吐与单帧延迟也应区分。对视频交互，用户感受到的是输入出现到结果可用的时间；对离线大批量分析，总处理量与稳定性可能更重要。

最后，把错误变成可以逐项检查的对象。检测看小目标漏检与重复框，分割看薄结构和接触边界，跟踪看遮挡后的身份，姿态看被挡住的关节，OCR 看相似字符和阅读顺序。选择一些正常场景，也选择暗光、模糊和密集重叠等条件，将可视化与对应指标放在一起。一个数告诉你整体变化，一张具体图告诉你变化发生在哪里。输出越丰富，越需要让读者看见每一种结构是否都对上了真实问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M13.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Single Shot Multibox Detection](https://d2l.ai/chapter_computer-vision/ssd.html)

   多尺度检测教程、完整实现及已许可原图。

   Original diagram CC BY-SA 4.0.
2. [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

   上下文与定位结合的网络结构。
3. [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640)

   整图联合预测类别与位置。
4. [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)

   对象查询、一对一集合匹配与检测。
5. [Segment Anything](https://arxiv.org/abs/2304.02643)

   提示、图像表示与掩码解码。
6. [SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714)

   视频可提示分割和流式记忆。
7. [ByteTrack: Multi-Object Tracking by Associating Every Detection Box](https://arxiv.org/abs/2110.06864)

   低分检测参与身份关联。
8. [PP-OCR: A Practical Ultra Lightweight OCR System](https://arxiv.org/abs/2009.09941)

   文字检测、方向与序列识别组合。
9. [OpenCV Optical Flow Tutorial](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)

   光流假设、梯度约束和Lucas–Kanade。
10. [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)

    共享特征与区域提议的两阶段检测。
11. [Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)

    未对齐序列的路径折叠与训练目标。
12. [MMPose Overview](https://mmpose.readthedocs.io/en/latest/overview.html)

    关键点、热图、编码解码和姿态工具入口。
