# 支持向量机：间隔、核与边界

Source: https://ml-biomat.com/tutorials/machine-learning/m05/
Language: zh-CN

从七个点的几何到手写数字、容忍带与正常区域，理解边界由谁决定。

## 把两个群体分开，为什么还要留出走廊

邮政分拣机看到一张手写数字图片，需要判断它写的是3还是8；质检系统读取一组传感器数值，需要区分合格与异常。把已知样本分开只是第一步：新图片会有笔画偏移，传感器也会有测量误差。如果分界线紧贴某个样本，轻微变化就可能使判断翻转。支持向量机从这里提出一个几何问题：在能分开两类的边界中，能否选择一条离最近样本也比较远的边界？留出的空间叫作间隔。它像道路两侧的缓冲带，使我们关心的不只是车辆此刻有没有越线，还包括它距离危险边缘有多远。

这条思路适合中小规模、特征表达已经比较明确的分类问题，也能扩展为回归和新颖性检测。它不会自动理解一张照片的物体结构：输入若是像素，它就按照像素向量的几何关系工作；输入若是频谱或统计特征，边界表达的也是这些特征之间的关系。选择支持向量机之前，先确定样本是什么、两个样本的距离是否有意义，以及预测时能够取得哪些特征。本章从二维点开始，把边界的每一个部件看清，再用真正的手写数字数据检验这些选择。

1995年，Corinna Cortes与Vladimir Vapnik发表的支持向量网络论文把大间隔分类、非线性特征映射和允许训练错误的优化问题结合起来。允许错误是关键一步：真实数据常常重叠，要求所有训练样本都站在正确一侧，会迫使边界追逐噪声。论文中的几何图把“分开多少点”转化为“用什么代价分开这些点”。今天的软件调用虽然只需要几行，间隔与错误之间的取舍仍然是理解结果的中心。

## 距离从哪里来：分数、法向量与支持向量

先把一个样本写成一列数。例如，第一维是经过标准化的笔画宽度，第二维是笔画倾斜程度。线性分类器给它一个分数：每一维乘上相应权重，再把各项相加并加上偏置。正分数判为一类，负分数判为另一类，零分数形成分界线。在更高维空间，这条线变成超平面，但计算方式没有改变。权重向量垂直于边界，因此它同时决定边界朝向；偏置决定边界在空间中的位置。

$$
f(\mathbf x)=\mathbf w^\top\mathbf x+b,\qquad d=\frac{|f(\mathbf x)|}{\|\mathbf w\|_2},\qquad W=\frac{2}{\|\mathbf w\|_2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4fa2300af121b336bb0d7845.svg) | p维特征向量；本章标准化后无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/76309848742948f71178485f.svg) | p维权重向量，决定边界法向；本章无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 偏置，标量，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 有符号决策分数，无量纲；正负决定二分类类别。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9221822a6402f4d6cb9d08be.svg) | 转置，把列向量变为行向量以进行内积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/91c83adc25418ce23b813590.svg) | 权重的欧氏长度，即各分量平方和的平方根；要求非零。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 到零分数平面的垂直距离，单位为标准化特征空间的长度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | 分数−1与+1两个面的距离，采用支持向量机的单位间隔约定。 |

取w=(2,0)、b=−1、x=(1,3)，分数为1，权重长度为2，垂直距离为0.5，走廊宽度为1。x第二维不参与这一条竖直边界的距离。

分数本身不是几何距离。假设把所有权重和偏置一起乘以10，零分数的位置完全相同，所有分数却都扩大10倍。用权重向量的长度去除分数，才消除了这种任意缩放。支持向量机进一步约定，理想情况下最近的两类样本分别位于分数为−1和1的位置，于是两条平行线之间的宽度就是2除以权重长度。扩大间隔便等价于缩小权重长度，但这个等价关系要和样本约束一起理解：把权重全设为零，并不能完成分类。

哪些样本会真正影响边界？想象用两块平行木板夹住两组钉子，最靠近中间空隙的钉子首先接触木板。它们就是支持向量的直观原型。离边界很远且被正确分类的点，稍微移动通常不会改变最优边界；贴近间隔或进入间隔的点则可能改变结果。图中给支持向量加了外圈，因此读图时可以同时观察分界线的位置、两条间隔线的距离，以及究竟是哪几个样本在约束它。

![同样的七个点，C从0.1变为10：模型实测间隔宽度分别约4.00与0.566。实线是零分数边界，虚线是±1分数线，外圈标出支持向量。](https://ml-biomat.com/static/tutorials/machine-learning/figures/fe748665e613880d09546738.svg?v=fe748665e613)

图 1同样的七个点，C从0.1变为10：模型实测间隔宽度分别约4.00与0.566。实线是零分数边界，虚线是±1分数线，外圈标出支持向量。

这幅图使用同一组七个点，只改变错误惩罚系数。一个与周围类别不同的点会把边界往另一个方向拉。较小惩罚下，模型接受它落入间隔甚至被分错，保留较宽的走廊；较大惩罚下，边界明显转动，走廊收窄。图上的宽度来自实际拟合权重，而非为说明概念手工挑选的线。宽间隔不等于测试表现一定更好，它提供的是一种控制边界复杂度的方法，具体取舍仍由独立于拟合的数据来比较。

## 给错误标价，而不是追着每一个点跑

硬间隔要求每个训练点都在正确的间隔线外。这在两类明显分离时很直观，但一个错误标签就可能使问题没有可行解。软间隔为每个点安排一个松弛量：它记录这个点距离“站到正确间隔线外”还差多少。松弛量为零表示要求已经满足；处于零和一之间表示类别判断仍正确，但缓冲不足；大于一则表示点已经越过分类边界。这样，几何位置可以转换成连续的惩罚，优化器能够比较不同边界的总得失。

$$
\min_{\mathbf w,b,\boldsymbol\xi}\ \frac12\|\mathbf w\|_2^2+C\sum_{i=1}^{n}\xi_i,\qquad y_i f(\mathbf x_i)\ge 1-\xi_i,\quad\xi_i\ge0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | 训练样本数与样本索引，计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a3cbcc3d75664bd27e243f85.svg) | 沿用前式权重、偏置、分数与第i个特征向量；本章无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i个二分类标签，取−1或+1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/09714133b942eafde68b756d.svg) | 第i个松弛量及其向量，非负，无量纲；固定边界下最小值为max(0,1−y_if)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | 每单位松弛的惩罚系数，正数；取决于特征尺度和求和约定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/87e2d6f0b155ef8920bda496.svg) | 选择使总目标最小的参数；把所有训练点的松弛相加。 |

若w=(1,0)、b=0，正类点x=(0.4,1)的分数为0.4，最小松弛为0.6。只考虑这一个点，C=2时目标为0.5+2×0.6=1.7。分数为−0.2的正类点需要松弛1.2，已被分错。

参数C控制每一个单位的间隔违反有多昂贵。C较大，优化器更愿意增加权重长度来减少训练违反；C较小，较平缓的边界获得更多优先权。C的具体数值依赖特征尺度、样本数量以及目标函数采用求和还是平均，不能把别人的C=1当成跨数据集通用的强度。如果某个特征以米记录，另一个以毫米记录，同样的物理变化会在数值上相差一千倍。标准化把每一列减去训练均值并除以训练标准差，使惩罚不再主要由单位选择决定；均值和标准差必须在各个训练折内估计。

下面的互动让你直接调整一条边界的方向、偏置和权重长度。它计算每个点的有符号间隔、铰链损失以及目标函数两部分。这里的边界由滑块指定，读者扮演优化器：先试着减少误分类，再看看权重惩罚付出了多少。把C调大不会自动移动边界，因为C改变的是你正在比较的价格；观察目标值后继续移动边界，才能体会最优解为什么随C改变。颜色表示类别，外圈表示当前点违反了单位间隔，数值读数给出可核对的结果。

## 亲手比较边界的代价

横纵坐标均为无量纲特征；边界由滑块直接指定。虚线为单位间隔，环圈标出违反点。

[Figure: 分类边界与间隔](https://ml-biomat.com/tutorials/machine-learning/m05/#M05-plot)

类别不平衡时还可以给不同类别设置不同惩罚。例如漏检缺陷的代价较高，可让缺陷样本的违反承担更高权重。权重改变学习目标，分类阈值改变已有分数的决策规则，两者作用的位置不同。确定权重或阈值后，应同时查看召回率、误报率与业务成本，而不是只看总体准确率。支持向量机的原始决策分数也不是概率；需要概率时，应在训练侧另设校准步骤，并检查可靠性曲线。

## 弯曲的边界，怎样由两两相似性得到

二维直线分不开内圈与外圈时，问题未必是优化做得不够好，而可能是表达方式太简单。如果给每个点增加“到原点距离的平方”这一维，环形结构就可能在新的空间中被一个平面分开。核方法把这种想法推进了一步：不必总是显式列出新空间的所有坐标，只要能计算两个样本在新空间中的内积，就能完成支持向量机所需的许多计算。核函数接收两个输入，返回这个内积所对应的数值。

$$
K_{\rm lin}(\mathbf x,\mathbf z)=\mathbf x^\top\mathbf z,\quad K_{\rm poly}=(\gamma\mathbf x^\top\mathbf z+r)^q,\quad K_{\rm RBF}=e^{-\gamma\|\mathbf x-\mathbf z\|_2^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4d10fa08c540fadb62d6163.svg) | 线性、多项式和径向基核的相似值；本章标准化输入下无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/af71bc998a10ca33d6d1ea71.svg) | 两个同维特征向量，标准化尺度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | 正的尺度参数；RBF中具有特征距离平方倒数的单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a3862e85bcfb892a6e44bb39.svg) | 多项式偏移及正整数次数；常用有效条件为gamma>0、r≥0。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数的底数，约2.71828。 |

取x=(1,0)、z=(0,1)，内积为0，平方距离为2。gamma=0.5时RBF相似度为exp(−1)≈0.3679；若两点重合，相似度为1。取r=1、q=2，多项式核为1。

线性核保留原有特征的内积。多项式核引入特征乘积，因而能够表达交互关系；次数升高也会让边界更加灵活。径向基函数核，也叫RBF核，以两点的平方距离决定相似性：距离为零时相似性为一，距离增大时逐渐衰减。它的参数gamma控制影响范围。gamma很小时，一个点的影响分布得很宽；gamma很大时，影响集中在很小的邻域，边界容易围绕单个训练点形成细小岛屿。因此C和gamma要共同选择，一个控制违反代价，一个控制几何影响尺度。

并不是任何看起来合理的相似度都能直接代入标准支持向量机。对于任意有限样本集合，核矩阵应满足半正定条件：任意实数加权组合所得到的二次型不为负。这个条件保证它能够对应某个内积空间，并使通常的凸优化解释成立。实际学习时可以先掌握库中已经定义好的核，再研究领域核的构造。把相关系数、编辑距离或神经网络输出随意叫作“核”，不会自动得到这些性质。

对偶问题的计算变量从特征权重换成每个训练点的系数。可以把这些系数理解为约束对最优目标施加的“价格”：违反样本条件会引入相应代价，消去原始权重后，特征只通过两两内积出现，因此可以把内积替换成核。下面的等式约束来自偏置项；系数上限来自软间隔的线性惩罚。原始问题是关于权重的凸最小化，对偶是带盒约束的凹最大化，两者在这里描述同一个最优分类器的两种求解方式。

$$
\max_{\boldsymbol\alpha}\sum_{i=1}^n\alpha_i-\frac12\sum_{i=1}^n\sum_{j=1}^n\alpha_i\alpha_j y_i y_j K(\mathbf x_i,\mathbf x_j),\quad 0\le\alpha_i\le C,\quad\sum_i\alpha_i y_i=0
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a70831c35436479ca201ac33.svg) | n维对偶变量及第i个系数，无量纲；包含可为零的非支持点系数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a6505df9c7be061c1a794c47.svg) | 训练样本数与两次求和中的样本索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e39d2f647a056424e7dd5ef3.svg) | 标签、特征、有效半正定核和统一惩罚，含义与单位沿用前式。 |

线性核下取两个一维点x₁=−1、x₂=1，标签分别−1、+1。令两个系数均为a，等式约束自动满足，目标变成2a−2a²；若C≥0.5，最大值在a=0.5，恢复权重w=Σαyx=1。

$$
f(\mathbf x)=\sum_{i\in S}\alpha_i y_i K(\mathbf x_i,\mathbf x)+b,\qquad 0<\alpha_i\le C
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8a1afc03b89f0210dd0f13b5.svg) | 非零系数的支持向量索引集合，以及其中的索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/c1688c6743f4779a68a29b34.svg) | 优化得到的非零对偶系数，无量纲；统一C的软间隔二分类形式。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1a7ca3fd714cc9789220d8f1.svg) | 分别为支持向量标签、核、训练向量、新向量、偏置、惩罚参数与预测分数，定义沿用前式。 |

两个支持向量的系数均为0.5、标签分别为+1和−1；与新点的核值分别0.8和0.2，偏置为0时，分数为0.5×0.8−0.5×0.2=0.3，判为正类。完整对偶还要求各alpha_i y_i之和为零，本例满足。

对偶表达式解释了预测为什么只需要支持向量：系数为零的训练点在求和中消失，留下非零系数、类别符号和与新样本的核值共同决定分数。这也揭示了资源成本。若有n个训练样本，完整核矩阵包含n乘n个数；样本数扩大十倍，矩阵元素会扩大一百倍。精确求解的时间还受核、数据和优化过程影响。因此面对大量稀疏文本，线性求解器往往更合适；面对中等样本、明显非线性而特征数适中的问题，RBF核值得进入比较。

## 让手写数字检验几何直觉

本章使用scikit-learn随包提供的手写数字数据，共1797张8乘8灰度图片。每张图片展开成64维向量，像素值从0到16，目标是0到9的数字类别。为了让每一类都进入训练和测试，我们按类别分层抽取1347张用于训练，450张用于测试，随机种子固定为17。图片像素展开会丢失显式的二维邻接结构，但它提供了一个清楚、可复现的起点；后续卷积网络章节会进一步利用这种邻接结构。

参数搜索只在1347张训练图片内进行。每组C和gamma使用相同的三个分层折，标准化放进Pipeline，因此验证折不会参与均值和方差的估计。图中的热图展示16组设置的平均验证准确率，而不是从测试集挑出来的最漂亮组合。本次搜索选择C=100、gamma=0.001，平均验证准确率约98.07%。确定参数后重新拟合全部训练图片，再对450张测试图片做一次评估。这个顺序把“选择方法”和“估计选定方法的表现”分开，避免测试结果反过来操纵参数。

![左：只用训练样本进行三折验证的16组参数；右：选定RBF模型在450张独立测试图片上的混淆矩阵。左图用颜色和格内数字表示验证准确率；右图用颜色表示各真实类别与预测类别的样本数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/7f162791271c2aa293f4f03b.svg?v=7f162791271c)

图 2左：只用训练样本进行三折验证的16组参数；右：选定RBF模型在450张独立测试图片上的混淆矩阵。左图用颜色和格内数字表示验证准确率；右图用颜色表示各真实类别与预测类别的样本数。

测试中，RBF支持向量机答对446张，准确率99.11%；线性支持向量机答对444张，为98.67%；逻辑回归为97.11%；采用150个Nyström特征再接LinearSVC的近似方案为96.22%。这些数字描述本章固定拆分下的结果。四张与六张错误之间的差距很小，若要比较算法在新样本上的稳定优势，应重复拆分或使用合适的配对评估。这里更值得观察的是：线性方法已经很强，非线性带来有限改善，而计算近似改变了精度与资源的取舍。

![手写数字的实际误判样本（不足六张时补入正确样本）与四种具体配置的测试准确率。图片为scikit-learn随包digits数据；所有指标由本章脚本计算。](https://ml-biomat.com/static/tutorials/machine-learning/figures/e8adca72f6919b44c215d91d.svg?v=e8adca72f691)

图 3手写数字的实际误判样本（不足六张时补入正确样本）与四种具体配置的测试准确率。图片为scikit-learn随包digits数据；所有指标由本章脚本计算。

混淆矩阵把每种真实数字分到各个预测类别的数量摆在一起，错误图片则让我们看到抽象计数背后的具体笔画。一个真实数字被错判，可能来自写法接近、像素分辨率有限，也可能来自模型没有利用空间结构。观察错误后可以提出下一步实验，例如保留二维结构、增加平移扰动或调整特征，但不能一边根据这450张图片改方案，一边继续把它们称为完全独立的最终测试。把它们转为开发材料时，另留新的评估集合即可。

十分类的SVC并不是只画一条超平面。库中的训练策略采用两两类别比较，十个类别对应45个二分类器，再合并判断。用于讲解的二维间隔图仍然有效，不过它解释的是这些二分类问题的基本部件。下面的完整代码同时保留数据拆分索引、验证结果、模型指标和绘图过程。修改参数网格后，可先观察热图如何变化，再检查错误类型是否改变，而不只是追逐最后一位小数。

### 完整实验：间隔、数字识别、回归与新颖性检测

需要NumPy、Matplotlib、scikit-learn；数据由随包digits与固定种子生成器提供。运行python main.py --output results --language zh，得到五幅SVG、summary.json和experiment_data.npz。

```
"""SVM margins, digit recognition, support-vector regression and novelty detection.
Run: python main.py --output results --language en
The digits data are bundled with scikit-learn (UCI optical handwritten digits).
"""
from pathlib import Path
import argparse,json,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC,SVR,LinearSVC,OneClassSVM
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='results');p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';rng=np.random.default_rng(17)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):fig.savefig(out/f'{name}-{a.language}.svg',bbox_inches='tight');plt.close(fig)
    X=np.array([[-2,-1],[-2,1],[-1,0],[1,0],[2,-1],[2,1],[-.8,.3]])
    y=np.array([-1,-1,-1,1,1,1,1])
    gx,gy=np.meshgrid(np.linspace(-3,3,180),np.linspace(-2,2,150));grid=np.c_[gx.ravel(),gy.ravel()]
    fig,axs=plt.subplots(1,2,figsize=(11.4,4.5),layout='constrained');margins=[]
    for ax,C in zip(axs,[.1,10.]):
        model=SVC(kernel='linear',C=C).fit(X,y);z=model.decision_function(grid).reshape(gx.shape)
        ax.contourf(gx,gy,z,levels=[-100,0,100],colors=['#d7e9ed','#f5e2cb'])
        ax.contour(gx,gy,z,levels=[-1,0,1],colors='#183845',linestyles=['--','-','--'])
        ax.scatter(X[:,0],X[:,1],c=np.where(y<0,'#167b82','#ca8446'),s=65,edgecolors='white')
        ax.scatter(model.support_vectors_[:,0],model.support_vectors_[:,1],s=165,facecolors='none',edgecolors='#183845',lw=1.4)
        norm=np.linalg.norm(model.coef_);margins.append({'C':C,'w':model.coef_[0].tolist(),'b':float(model.intercept_[0]),'width':float(2/norm),'support_indices':model.support_.tolist()})
        ax.set(title=f'C = {C:g}; '+('间隔宽度 ' if zh else 'margin width ')+f'{2/norm:.2f}',xlabel='x₁',ylabel='x₂',xlim=(-3,3),ylim=(-2,2),aspect='equal')
    save(fig,'margins')
    digits=load_digits();train_idx,test_idx=train_test_split(np.arange(len(digits.target)),test_size=.25,stratify=digits.target,random_state=17)
    Xt,Xs=digits.data[train_idx],digits.data[test_idx];yt,ys=digits.target[train_idx],digits.target[test_idx]
    grid_search=GridSearchCV(make_pipeline(StandardScaler(),SVC(kernel='rbf')),{'svc__C':[.1,1,10,100],'svc__gamma':[.001,.01,.1,1]},cv=StratifiedKFold(3,shuffle=True,random_state=17),n_jobs=1)
    grid_search.fit(Xt,yt)
    models={'Linear SVM':make_pipeline(StandardScaler(),SVC(kernel='linear',C=1)),
            'RBF SVM':grid_search.best_estimator_,
            'Logistic regression':make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=2000)),
            'Nystroem + LinearSVC':make_pipeline(StandardScaler(),Nystroem(gamma=.01,n_components=150,random_state=17),LinearSVC(C=1,dual=False,max_iter=5000))}
    scores={};predictions={}
    for name,model in models.items():
        start=time.perf_counter()
        if name!='RBF SVM':model.fit(Xt,yt)
        pred=model.predict(Xs);predictions[name]=pred
        scores[name]={'test_accuracy':float(accuracy_score(ys,pred)),'prediction_seconds':None,'support_vectors':int(model[-1].support_.size) if hasattr(model[-1],'support_') else None}
        t=time.perf_counter();model.predict(Xs);scores[name]['prediction_seconds']=time.perf_counter()-t
    cv=np.array(grid_search.cv_results_['mean_test_score']).reshape(4,4)
    fig,axs=plt.subplots(1,2,figsize=(11.5,4.8),gridspec_kw={'width_ratios':[1,1.2]},layout='constrained')
    im=axs[0].imshow(cv,vmin=.1,vmax=1,cmap='YlGnBu',aspect='auto');fig.colorbar(im,ax=axs[0],label='CV accuracy')
    axs[0].set(xticks=range(4),xticklabels=['.001','.01','.1','1'],yticks=range(4),yticklabels=['.1','1','10','100'],xlabel='γ',ylabel='C',title='训练集内3折验证' if zh else '3-fold validation inside training data')
    for i in range(4):
        for j in range(4):axs[0].text(j,i,f'{cv[i,j]:.3f}',ha='center',va='center',color='white' if cv[i,j]>.7 else '#183845',fontsize=10)
    cm=confusion_matrix(ys,predictions['RBF SVM']);im=axs[1].imshow(cm,cmap='Blues');fig.colorbar(im,ax=axs[1],label='样本数' if zh else 'Count')
    axs[1].set(xlabel='预测数字' if zh else 'Predicted digit',ylabel='真实数字' if zh else 'True digit',xticks=range(10),yticks=range(10),title='独立测试集：RBF SVM' if zh else 'Held-out test set: RBF SVM')
    save(fig,'validation')
    fig=plt.figure(figsize=(11.4,6.1),layout='constrained');gs=fig.add_gridspec(2,6,height_ratios=[1,1.5]);err=np.flatnonzero(ys!=predictions['RBF SVM']);show=np.r_[err[:6],np.flatnonzero(ys==predictions['RBF SVM'])[:6-len(err[:6])]]
    for j,idx in enumerate(show):
        ax=fig.add_subplot(gs[0,j]);ax.imshow(Xs[idx].reshape(8,8),cmap='gray_r',vmin=0,vmax=16);ax.set_title(f'{ys[idx]} → {predictions["RBF SVM"][idx]}',fontsize=11);ax.axis('off')
    ax=fig.add_subplot(gs[1,:]);names=list(scores);vals=[scores[n]['test_accuracy'] for n in names];ax.barh(names,vals,color=['#6f8191','#167b82','#ca8446','#8b7557']);ax.set(xlim=(0,1.08),xlabel='测试准确率' if zh else 'Test accuracy')
    for i,v in enumerate(vals):ax.text(v+.01,i,f'{v:.3f}',va='center')
    save(fig,'digits')
    x=np.sort(rng.uniform(0,6,80));target=np.sin(x)+rng.normal(0,.12,80);xx=np.linspace(0,6,300)
    fig,axs=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained');svr=[]
    for ax,eps in zip(axs,[.05,.25]):
        model=SVR(C=10,gamma=.5,epsilon=eps).fit(x[:,None],target);fit=model.predict(xx[:,None])
        ax.fill_between(xx,fit-eps,fit+eps,color='#cfe5e6',label='ε '+('容忍带' if zh else 'tube'));ax.plot(xx,fit,color='#167b82',lw=2);ax.plot(xx,np.sin(xx),'--',color='#6f8191',label='生成函数' if zh else 'Generating function');ax.scatter(x,target,s=20,color='#183845');ax.scatter(x[model.support_],target[model.support_],s=70,facecolors='none',edgecolors='#ca8446');ax.set(xlabel='x',ylabel='y',title=f'ε={eps}; '+('支持向量 ' if zh else 'support vectors ')+str(len(model.support_)));ax.legend(frameon=False,fontsize=9)
        svr.append({'epsilon':eps,'n_support':len(model.support_)})
    save(fig,'svr')
    normal=rng.normal(0,.6,(160,2));new=rng.normal(0,.6,(40,2));outliers=rng.uniform(-3,3,(40,2));novel=make_pipeline(StandardScaler(),OneClassSVM(nu=.1,gamma=.5)).fit(normal)
    xx2,yy2=np.meshgrid(np.linspace(-3,3,140),np.linspace(-3,3,140));zz=novel.decision_function(np.c_[xx2.ravel(),yy2.ravel()]).reshape(xx2.shape)
    fig,ax=plt.subplots(figsize=(7.6,5.8),layout='constrained');ax.contourf(xx2,yy2,zz,levels=[zz.min(),0,zz.max()],colors=['#f7e6d7','#d6e9eb']);ax.contour(xx2,yy2,zz,levels=[0],colors='#183845');ax.scatter(normal[:,0],normal[:,1],s=12,color='#167b82',alpha=.6,label='正常训练样本' if zh else 'Normal training samples');ax.scatter(new[:,0],new[:,1],s=38,facecolors='none',edgecolors='#183845',label='新正常样本' if zh else 'New normal samples');ax.scatter(outliers[:,0],outliers[:,1],s=30,marker='x',color='#b45d3b',label='广域测试样本' if zh else 'Broad-range test samples');ax.set(xlabel='x₁',ylabel='x₂',aspect='equal',title='One-Class SVM');ax.legend(frameon=False,fontsize=9)
    save(fig,'novelty')
    summary={'digits_samples':len(digits.target),'train_samples':len(yt),'test_samples':len(ys),'best_params':grid_search.best_params_,'best_cv_accuracy':float(grid_search.best_score_),'models':scores,'margin_models':margins,'svr':svr,'one_class_normal_acceptance':float((novel.predict(new)==1).mean()),'one_class_broad_rejection':float((novel.predict(outliers)==-1).mean())}
    np.savez_compressed(out/'experiment_data.npz',tiny_X=X,tiny_y=y,train_idx=train_idx,test_idx=test_idx,test_y=ys,rbf_prediction=predictions['RBF SVM'],cv_scores=cv,svr_x=x,svr_y=target)
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

## 从分界线到一条有容忍宽度的预测曲线

如果目标不再是数字类别，而是设备温度或某个连续响应，支持向量回归把“间隔”改造成预测曲线两侧的一条容忍带。普通平方误差会处罚每一次偏离，即使偏离比测量分辨率还小；epsilon不敏感损失允许误差在一条规定宽度内不受惩罚，越过容忍带后才按超出部分增长。这个设计让“多小的偏差值得追逐”成为明确的参数，而不是让模型无差别地贴近所有观测。

$$
\ell_\epsilon(y,f)=\max\bigl(0,|y-f|-\epsilon\bigr)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db4e42af6785df82e7296e31.svg) | epsilon不敏感损失，单位与回归目标相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2eea885ee51e19ae4e16f003.svg) | 观测响应与预测响应，单位相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | 非负容忍半宽，单位与响应相同。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ab88af114f90ff87651b701.svg) | 绝对误差，以及取0和超出容忍值中较大者。 |

epsilon=0.2时，误差0.15对应损失0；误差0.6对应损失0.4。若响应单位是摄氏度，epsilon和损失也以摄氏度表示。

![相同合成观测与相同C、gamma，改变epsilon容忍宽度。背景带为训练损失的容忍范围，外圈为支持向量；虚线是真实生成关系。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f029b68da2bfe1e856e149c7.svg?v=f029b68da2bf)

图 4相同合成观测与相同C、gamma，改变epsilon容忍宽度。背景带为训练损失的容忍范围，外圈为支持向量；虚线是真实生成关系。

图中数据由一条正弦关系加上标准差0.12的独立高斯噪声生成，横坐标和响应均采用无量纲教学尺度。我们保持C=10和gamma=0.5，只把epsilon从0.05改为0.25。实际拟合中，支持向量数从47个降为6个；更宽的容忍带允许更多样本不参与决定曲线。宽带是否合适，要结合目标的测量精度与预测用途判断。如果需要分辨很小的变化，过宽容忍带会抹去有意义的信号；如果观测本身很嘈杂，追逐微小波动则会增加不必要的复杂度。

回归中的epsilon与目标具有相同单位，而C和核参数仍受特征和目标缩放的影响。例如把温度从摄氏度改成毫摄氏度，epsilon也要同步调整，才能保持同一个容忍标准。SVR的输出是条件关系的一种估计，容忍带不是置信区间，也不是未来观测覆盖区间；它来自训练损失的定义。若需要“下一次观测落在哪个范围”的答案，可在独立校准数据上构造预测区间，或接着学习概率回归与保形预测。

## 只有正常样本时，学习它们占据的区域

某些系统拥有大量正常运行记录，却几乎没有故障实例。One-Class SVM处理的是这样的新颖性检测问题：从正常训练分布中估计一个区域，再判断新观测是否明显偏离。它并不需要先编造各种故障标签。核函数仍然决定空间中的相似关系，而参数nu控制边界所保留的支持向量和训练外点比例。在通常的理论条件下，nu为训练错误比例提供上界、为支持向量比例提供下界；有限样本及数值求解会带来近似，因此读结果时仍应直接统计实际落在边界外的训练点。

![160个正常训练点定义核边界，另外两组各40个点用于观察接纳与拒绝。宽区域生成器与正常分布存在空间重叠。](https://ml-biomat.com/static/tutorials/machine-learning/figures/115ff8c7451b829979e010fd.svg?v=115ff8c7451b)

图 5160个正常训练点定义核边界，另外两组各40个点用于观察接纳与拒绝。宽区域生成器与正常分布存在空间重叠。

本例从二维标准差0.6的高斯分布生成160个正常训练点，再生成40个同分布新点以及40个覆盖更宽区域的均匀点。拟合采用nu=0.1、gamma=0.5和训练侧标准化。同分布新点的接纳率为90%，宽区域样本的拒绝率为80%。宽区域样本中也有点落在正常区域，因此“来自宽分布”不等于“每一个都应被拒绝”。这幅图要展示的是边界与分布支持范围的关系，而不是把生成器标签包装成真实故障诊断成绩。

异常检测、离群点检测与新颖性检测经常被混用。离群点检测通常面对已经混有异常的训练数据，需要发现其中的可疑点；新颖性检测先在相对干净的正常数据上学习，再检查未来样本。选择训练协议时应先确定属于哪一种。若设备的正常工作模式会季节性迁移，一个固定边界可能把新工况当成异常；这时应按工况分层、重新校准阈值或更新正常参考数据。算法边界必须与实际监测流程一起设计。

## 把精确核、近似核与线性方法放进同一张工作台

核近似的目标是用有限长度的显式特征近似原本隐式的特征空间，再交给线性算法。Nyström方法从训练样本中选出一组代表点，利用它们与其他样本的核关系构造低秩近似；随机傅里叶特征则针对某些平移不变核，通过随机频率把相似性近似为有限向量的内积。前者依赖代表点的选择，后者依赖随机特征数量与核的适用条件。两者都把特征数量变成可控制的资源旋钮，适合研究精度、内存和预测速度之间的关系。

本例的Nyström方案使用150个特征，并采用与精确RBF最优设置不同的固定gamma=0.01，因此其96.22%的准确率说明的是这一个具体配置。要比较近似方法的最佳可达表现，应给它独立的训练侧参数搜索，并控制总预算；不能把一个固定近似配置与充分调优的精确核直接当成公平的算法排名。类似地，LinearSVC与SVC(kernel='linear')虽然都产生线性边界，却使用不同求解器、默认损失和多分类策略，比较时应记录具体实现。

完成本章后，可以用一个三步实验巩固选择能力：先只改变标准化方式，观察验证热图和支持向量数量；再固定预处理，增加Nyström特征数并测量多次预测的中位耗时；最后对误分类样本按数字类别和笔画形态分组。每一步只改变一个主要因素，把准确率、计算资源和错误结构并排记录。这样得到的结论既能说明某个模型是否合适，也能说明它为什么合适，以及下一步应改数据表达、参数还是算法家族。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Cortes & Vapnik (1995), Support-vector networks](https://homepages.math.uic.edu/~lreyzin/papers/cortes95.pdf)

   间隔、软约束与核分类的原始论证。
2. [scikit-learn — Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)

   SVC、SVR、OneClassSVM的实现与参数解释。

   BSD-3-Clause documentation/code; dataset terms separate.
3. [scikit-learn — SVM Margins Example](https://scikit-learn.org/stable/auto_examples/svm/plot_svm_margin.html)

   对照观察C与间隔的几何关系。

   BSD-3-Clause
4. [scikit-learn — Kernel Approximation](https://scikit-learn.org/stable/modules/kernel_approximation.html)

   Nyström与随机傅里叶特征的适用条件。

   BSD-3-Clause
5. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   随包手写数字的形状、数值与原始数据链接。

   Dataset from UCI Optical Recognition of Handwritten Digits; see linked dataset terms.
