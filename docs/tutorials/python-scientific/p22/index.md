# 从有限样本走向统计判断

Source: https://ml-biomat.com/tutorials/python-scientific/p22/
Language: zh-CN

把原始读数、抽样均值和置信区间放在同一组可追踪数据里。

## 测完十个试样以后，怎样描述还没有测到的那一批

假设一种材料的指标通常在20 kPa附近波动。你从一批试样里测了十个，得到的平均值是18.65 kPa。这个差别值得继续研究，但首先要弄清它来自什么：这批材料的总体水平发生了变化，还是这十个试样恰好偏低？统计方法把“如果重新取一组试样，会发生怎样的变化”纳入判断，帮助我们把眼前的一张数据表与它所代表的总体联系起来。

本节使用一个条件完全明确的教学总体：独立试样的读数服从均值20 kPa、标准差4 kPa的正态分布。正态分布的钟形曲线让靠近20的读数更常见，向两侧越远越少见。程序从这个模型生成200组样本，每组最多50个试样。总体参数在模拟中已知，因此可以直接检查估计方法的表现；分析每一组样本时，仍只用该组数据估计均值和波动。

我们将用SciPy计算标准误、t置信区间和单样本t检验，并把它们放回原始读数上解释。这里的重点是三个对象之间的区别：个别试样怎样分散，样本均值怎样随抽样变化，以及一条区间如何表达对总体均值的估计。把这三个层次分开，统计结果就能与实际研究问题建立清楚的关系。

## 先确定一个样本点究竟代表什么

一个试样测三次，与三个独立试样各测一次，回答的问题并不相同。前者主要显示同一试样上的测量波动，后者还包含试样之间的差异。如果研究目标是这批材料的总体水平，独立试样通常是更直接的抽样单位；若把同一试样的重复读数都当作独立试样，公式里的样本数会被扩大，均值的不确定度也会被算得过小。

本节数据数组有200行、50列。每一行代表一次独立抽样实验，每一列是该实验中一个独立试样的读数。研究每组10个试样的情况时，取每行前10列，并沿列方向求均值。增加到30个试样时，保留原来的10个，再加入后20个。这样，同一行的不同样本量可以对照；不同行之间依然是分别生成的独立抽样。

这种设计还说明了随机种子的用处。固定种子让200组数据能够重现，从而保证正文、图和交互中看到的数字一致。种子固定的是一组模拟记录，统计上的总体仍然是预先规定的正态模型。改变种子会得到另一批样本，也会稍微改变覆盖率与某一组的均值；方法的长期性质需要通过许多可能样本来理解。

真实研究还需要让抽样方式对应目标总体。例如，只从最容易取到的位置挑选试样，可能无法覆盖整批材料的空间差异。更合理的做法是在设计阶段规定抽样位置、批次比例和独立制备单位，再将这些信息保存在数据表中。增加记录行数能够提高计算的数量，却只有增加合适的独立信息，才能改善目标总体的估计。

独立性可以用一把共同偏移的尺来理解。如果某次仪器标定整体偏高，同一条件下测出的许多读数可能一起偏高，把这些读数平均并不会让共同偏移自动抵消。标准误中的平方根缩减依赖独立随机变化；共享批次、同一试样或同一时间段带来的共同影响，需要通过分层设计、校准或适当模型表示。因此，理解误差的来源，比把标准误公式重复套用到更多行数据上更重要。

## 标准差描述试样，标准误描述均值的波动

先看一组便于手算的读数：16、18、20、22、24 kPa。平均值为20 kPa，五个读数与均值的差依次为−4、−2、0、2、4 kPa。把差平方后相加得到40 kPa²，再除以样本数减一，即4，得到样本方差10 kPa²；开平方得到标准差约3.1623 kPa。标准差因此概括的是这五个试样围绕它们共同均值的分散程度。

$$
\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar x)^2}{n-1}},\qquad \mathrm{SEM}=\frac{s}{\sqrt n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | 第i个独立试样的读数，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | i为试样编号，n为独立试样数，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | 样本均值，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 样本标准差，kPa；分母n−1用于估计总体方差。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dd3305e34ff527725a7a82ea.svg) | 独立同分布样本下，样本均值标准误的估计，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ca563c8033303e110f807c.svg) | 求和与非负平方根；平方偏差单位kPa²，开根号后回到kPa。 |

16、18、20、22、24 kPa的均值为20，平方偏差和为40 kPa²。标准差为√(40/4)=√10≈3.162278 kPa，标准误为√10/√5=√2≈1.414214 kPa。前者描述个体分散，后者估计重复抽样均值的变化尺度。

标准误再把标准差除以样本数的平方根。本例约为1.4142 kPa，它描述在独立、同分布抽样条件下，样本均值波动尺度的估计。不同试样的偏高与偏低在平均时会部分抵消，所以均值通常比单个读数稳定。样本数增加四倍时，在总体波动近似相同的情况下，标准误大约减半；这也说明提高均值精度往往需要相当多的独立试样。

![同一个正态教学总体：左侧保留第一组10个独立读数，右侧统计200组各自的均值，分箱宽0.5 kPa。红线指出左侧样本在右图中的位置。](https://ml-biomat.com/static/tutorials/python-scientific/figures/04127732b0190577b18646a2.svg?v=04127732b019)

图 1同一个正态教学总体：左侧保留第一组10个独立读数，右侧统计200组各自的均值，分箱宽0.5 kPa。红线指出左侧样本在右图中的位置。

左图显示某一组十个原始读数，右图则显示200组各自算出的均值。两幅图纵轴承担不同任务：左图数值仍是kPa，右图纵轴数的是有多少组均值落进某一区间。把左图的一组压缩成一个均值，它就在右图中贡献一个位置。这种“每组变一个点”的转换，正是理解抽样分布的入口。

程序使用`stats.sem`计算标准误，它默认采用样本方差所需的`ddof=1`。NumPy的`std`默认是`ddof=0`，因此需要显式设置，才能与这里的手算一致。参数并非形式上的细节：它决定平方偏差和除以什么数，也对应你是描述眼前全部数值，还是用有限样本估计总体的波动。

样本标准差每次也会变化。某一组恰好包含较多接近均值的试样，就会得到较小的标准差和标准误；另一组包含更分散的读数，估计的波动就大一些。模拟里虽然总体标准差固定为4 kPa，各组算出的样本标准差仍然不必等于4。区间宽度因此既受样本数影响，也受这一次实际抽到了什么影响，不能只凭n就确定每条区间的精确长度。

## Student的小样本问题：连波动大小也是估出来的

1908年，以Student为署名发表的《均值的可能误差》讨论了一个关键困难：样本很少时，均值有抽样波动，用来衡量这种波动的标准差本身也不稳定。文章开头就把问题放在那些难以大量重复的化学、生物和农业实验中。这个背景与今天的小批量材料实验仍然相通——有限样本需要同时告诉我们中心在哪里，以及判断中心的尺度有多可靠。

若总体标准差已经精确知道，可以用它直接缩放均值的偏离；实际研究常常用样本标准差替代。替代后，分母也跟着样本变化，标准化统计量的两侧尾部会更厚。t分布把这一额外变化纳入参考分布。它由自由度控制，本节单样本均值问题的自由度为样本数减一。样本越多，对波动的估计越稳定，t分布逐渐接近标准正态分布。

![Student的小样本问题通过概率密度与临界倍数展示。左图标准化正态与t分布的面积均为1，红色尾部对应自由度4的双侧5%；右图用SciPy分位数计算95%区间倍数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/efbbc41fd0537baf9df32764.svg?v=efbbc41fd053)

图 2Student的小样本问题通过概率密度与临界倍数展示。左图标准化正态与t分布的面积均为1，红色尾部对应自由度4的双侧5%；右图用SciPy分位数计算95%区间倍数。

图中的概率密度曲线用面积表达概率，曲线在某一点的高度本身并不是该点出现的概率。红色t分布对应自由度4，即五个独立试样，尾部比虚线正态分布更厚。为容纳中间95%的面积，t分布需要延伸到约±2.776，而标准正态分布约为±1.960。两者乘以相同标准误，前者就得到更宽的区间。

自由度减一可以从偏差的约束理解：样本均值确定后，所有“读数减均值”的差必然相加为零。知道其中四个差，第五个就被决定了，因此五个偏差只有四个可以独立变化。这个约束解释了为何方差估计要扣除一个自由度：确定样本中心后，剩余偏差能够独立变化的数目减少了一个。

## 置信区间是一套重复使用的估计规则

均值给出一个中心估计，置信区间则把这个估计的精度一同呈现。对独立正态样本、总体方差未知的情形，用样本均值向两侧各延伸“t临界倍数乘标准误”，就得到相应的t区间。样本分散越大，标准误越大，区间越宽；独立样本增多通常使标准误减小，临界倍数也向正态值靠近。

$$
\mathrm{CI}_{1-\alpha}=\left[\bar x-q_{1-\alpha/2,n-1}\frac{s}{\sqrt n},\;\bar x+q_{1-\alpha/2,n-1}\frac{s}{\sqrt n}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ef3c902b8343b9c13d7ced08.svg) | 置信水平为1−α的总体均值区间，两个端点单位kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 两端合计的参考概率，无量纲；95%区间取0.05。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a8d6097212e39d5151b95ed9.svg) | 自由度n−1的t分布在累积概率1−α/2处的分位数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/91dad9a192a1a10a4a3490bc.svg) | 样本均值和标准差单位kPa，n为无量纲的独立试样数。 |

五点示例取n=5、α=0.05，临界倍数q≈2.776445。用它乘标准误√2 kPa，半宽为3.926486 kPa；从均值20 kPa向两侧延伸，得到[16.073514,23.926486] kPa。左右各留2.5%的参考概率，所以分位数使用0.975。

对16、18、20、22、24 kPa这组数据，95%区间的半宽为2.776445乘1.414214，约3.926486 kPa，所以区间约为16.073514到23.926486 kPa。这里区间估计的对象是总体均值。若要预测下一个试样的读数，还要包含试样本身的波动，因此需要预测区间等另一类计算；样本均值的区间会随着样本数增加而变窄，个别试样的分散却仍然存在。

95%应放在整套抽样与构造规则上理解：在条件相同的重复实验中，每次重新抽样、重新算区间，长期大约95%的区间会覆盖固定的总体均值。当前算出的区间是这条规则的一次结果。图中总体均值始终用20 kPa的竖线表示，变化的是每次样本给出的区间中心和宽度；这种画法把规则的频率含义直接展示出来。

![左图显示前40组的95% t区间与固定总体均值20 kPa，红色区间未覆盖该值。右图覆盖率使用全部200组，分母相同；样本量之间共享各行的前部读数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0476f2546cb8ce0bb99c4254.svg?v=0476f2546cb8)

图 3左图显示前40组的95% t区间与固定总体均值20 kPa，红色区间未覆盖该值。右图覆盖率使用全部200组，分母相同；样本量之间共享各行的前部读数。

本次固定记录里，每组10个试样时，200条95%区间有188条覆盖20 kPa，实际比例为94%。理论置信水平与有限模拟得到的比例可以略有不同，就像掷硬币200次不一定恰好出现100次正面。把置信水平提高到99%会扩大每条区间，也会提高覆盖的数量。提高覆盖要求和保持区间精细之间的取舍，应结合研究要回答的问题安排。

本次200组中，每组5个试样的95%区间平均宽度约9.0435 kPa，50个试样时约2.2634 kPa。宽度缩小来自两方面：标准误随样本增加而减小，小样本所需的较大t临界倍数也随之下降。这些平均宽度汇总的是指定总体和这200次抽样下的结果，能帮助比较设计的精度；规划真实实验时，可以将预期的试样波动和目标区间宽度放进同样的计算框架。

## 把均值与一个具体参考值比较

有时问题已经带着一个明确的参考值，例如工艺设定的20 kPa。单样本t检验先建立总体均值等于该参考值的零假设，再看当前均值偏离了多少个标准误。差值除以标准误后变成无量纲统计量，不同单位的数据便能用相同的t参考分布比较。偏离越大，意味着在这套零假设与抽样条件下越少见。

$$
t_{\mathrm{obs}}=\frac{\bar x-\mu_0}{s/\sqrt n}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fec9b3a28810ab0be441f7e3.svg) | 当前样本的t统计量，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | 当前样本均值，kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca57ac9e96d5d1c8997d7034.svg) | 零假设中规定的总体均值，本例20 kPa。 |
| ![Formula](https://ml-biomat.com/static/agent-math/913e236aa6d008dc21044e37.svg) | s为样本标准差(kPa)，n为独立试样数；s/√n是标准误(kPa)。 |

第一组10个试样给出(18.653641−20)/0.994789≈−1.353412。负号表示均值低于参考值，绝对值表示偏离了多少个标准误。以自由度9的t分布计算两端同样或更极端的面积，得到双侧p≈0.208936。

程序第一组10个试样的均值约18.653641 kPa，标准误约0.994789 kPa，因此t约为−1.353412。双侧检验将参考分布中两端至少同样远的区域都计入，得到p约0.208936。这个面积回答的是：假设总体均值为20 kPa，重复抽样中出现至少这么大的标准化偏离有多常见。它衡量当前数据与所设参考模型的关系，实际差值仍应保留kPa单位一起报告。

同一组数据的95%置信区间约为16.403271到20.904010 kPa，包含20。对于这里使用的同一双侧t方法，区间是否包含参考值与5%水平检验的判断对应。区间还进一步显示与数据相容的均值范围，因此读结果时可以同时看中心差值、区间宽度与p值。若研究关心是否足够接近目标，应先规定有实际意义的容许差值，再采用相应的等效性分析设计。

检验方向和比较对象应在分析前由问题确定。双侧问题关心向任意方向的偏离，单侧问题关心事先指定的方向。看到样本偏高后再选择“只看偏高”，会改变原先的抽样判据。多次比较、反复查看结果后决定是否停止采样，也会改变整体错误概率；这些都属于实验和分析设计的一部分，需要与单次计算共同安排。

p值的两端面积还可以联系到区间规则来理解。一个固定参考值越远离样本均值，标准化后的绝对偏离越大，对应尾部面积越小。若先设定某个错误概率水平，再找出所有不会被该双侧检验排除的参考均值，就会得到相应的置信区间。两种工具因此来自同一套参考分布，但一个突出“这个值如何”，另一个突出“哪些值与当前数据相容”。

## 完整程序：每个区间都能追到它自己的样本

完整程序先生成固定的200×50数据数组，再分别取5、10、30和50个试样进行计算。`stats.ttest_1samp(..., axis=1)`让每一行作为一个独立实验，返回200个统计量；它的`confidence_interval`方法构造相应区间。程序还用t临界值与标准误直接重算区间，核对两条计算路径是否一致。

### 完整示例：从固定样本到t区间与覆盖率

运行生成全部样本、数值摘要与三幅科学图。区间同时使用SciPy结果与显式分位数公式核对。

```
"""Study sample means, Student intervals, and repeated-sampling coverage."""
from pathlib import Path
import argparse,json
import numpy as np
import scipy
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
SEED=20261114
MU,SIGMA=20.,4.
BLUE,RED,INK='#28658c','#b64a35','#20313e'


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={f.name for f in font_manager.fontManager.ttflist};plt.rcParams.update({'font.family':[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in available],'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    bank=np.random.default_rng(SEED).normal(MU,SIGMA,size=(200,50));cases={};critical={}
    for n in [5,10,30,50]:
        samples=bank[:,:n];test=stats.ttest_1samp(samples,MU,axis=1)
        for confidence in [.9,.95,.99]:
            interval=test.confidence_interval(confidence_level=confidence);means=samples.mean(axis=1);sem=stats.sem(samples,axis=1);q=float(stats.t.ppf((1+confidence)/2,n-1));critical[f'{n}_{confidence}']=q
            assert np.allclose(interval.low,means-q*sem)
            cases[f'{n}_{confidence}']={'coverage_count':int(np.sum((interval.low<=MU)&(MU<=interval.high))),
                'mean_interval_width_kPa':float(np.mean(interval.high-interval.low)),
                'selected_mean_kPa':float(means[0]),'selected_sem_kPa':float(sem[0]),'selected_low_kPa':float(interval.low[0]),'selected_high_kPa':float(interval.high[0]),
                'selected_t':float(test.statistic[0]),'selected_p':float(test.pvalue[0])}
    hand=np.array([16,18,20,22,24.]);hand_sem=float(stats.sem(hand));hand_q=float(stats.t.ppf(.975,4));hand_test=stats.ttest_1samp(hand,20.)
    np.savetxt(args.output/'samples.csv',bank,delimiter=',',header=','.join(f'specimen_{i+1}' for i in range(50)),comments='')
    bank_data={'samples':bank.tolist(),'critical':critical,'population_mean_kPa':MU,'population_sd_kPa':SIGMA,'seed':SEED}
    (args.output/'sample-bank.json').write_text(json.dumps(bank_data),encoding='utf-8')
    n=10;sample=bank[0,:n];means=bank[:,:n].mean(axis=1);test=stats.ttest_1samp(bank[:,:n],MU,axis=1);ci=test.confidence_interval();covers=(ci.low<=MU)&(MU<=ci.high)
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    ax[0].scatter(np.arange(1,n+1),sample,color=BLUE,s=55);ax[0].axhline(sample.mean(),color=BLUE,label=tr('该组样本均值','This sample mean'));ax[0].axhline(MU,color=INK,ls='--',label=tr('规定总体均值20 kPa','Defined population mean 20 kPa'))
    ax[0].set(xlabel=tr('独立试样编号','Independent specimen index'),ylabel=tr('教学读数 / kPa','Teaching reading / kPa'),title=tr('一组10个试样，保留每个读数','One group of ten specimens, all readings visible'),xticks=[1,3,5,7,10]);ax[0].legend(frameon=False,fontsize=10);ax[0].grid()
    ax[1].hist(means,bins=np.arange(15,25.5,.5),color='#b6d0df',edgecolor='white');ax[1].axvline(MU,color=INK,ls='--');ax[1].axvline(sample.mean(),color=RED,label=tr('左图这一组的均值','Mean of the group shown at left'))
    ax[1].set(xlabel=tr('每组的样本均值 / kPa','Sample mean of each group / kPa'),ylabel=tr('组数','Number of groups'),title=tr('200组独立抽样，形成均值分布','200 independent groups form a mean distribution'));ax[1].legend(frameon=False,fontsize=10);save(fig,'sampling')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained');x=np.linspace(-5,5,1001)
    ax[0].plot(x,stats.norm.pdf(x),color=INK,ls='--',label=tr('标准正态','Standard normal'))
    for df,color in [(4,RED),(49,BLUE)]:ax[0].plot(x,stats.t.pdf(x,df),color=color,label=f't, df = {df}')
    mask=np.abs(x)>=hand_q;ax[0].fill_between(x,0,stats.t.pdf(x,4),where=mask,color=RED,alpha=.2);ax[0].set(xlabel=tr('标准化统计量，无量纲','Standardized statistic, dimensionless'),ylabel=tr('概率密度','Probability density'),title=tr('Student（1908）：小样本还要估计波动','Student (1908): small samples also estimate spread'));ax[0].legend(frameon=False,fontsize=10)
    ns=np.arange(3,61);qs=stats.t.ppf(.975,ns-1);ax[1].plot(ns,qs,color=RED,lw=2);ax[1].axhline(stats.norm.ppf(.975),color=INK,ls='--');ax[1].scatter([5,50],stats.t.ppf(.975,np.array([4,49])),color=RED)
    ax[1].annotate('n = 5: 2.776',(5,hand_q),xytext=(11,3.2),arrowprops={'arrowstyle':'-','color':RED});ax[1].set(xlabel=tr('每组独立试样数 n','Independent specimens per group, n'),ylabel=tr('95%区间的临界倍数','Critical multiplier for a 95% interval'),title=tr('样本增多，临界倍数逐渐靠近1.96','With more observations, the multiplier approaches 1.96'));ax[1].grid();save(fig,'history')
    fig,ax=plt.subplots(1,2,figsize=(12,8.4),layout='constrained',gridspec_kw={'width_ratios':[1.5,1]})
    for i in range(40):ax[0].plot([ci.low[i],ci.high[i]],[i+1,i+1],color=BLUE if covers[i] else RED,lw=1.8);ax[0].scatter(means[i],i+1,color=BLUE if covers[i] else RED,s=14)
    ax[0].axvline(MU,color=INK,ls='--');ax[0].invert_yaxis();ax[0].set(xlabel=tr('均值与95%置信区间 / kPa','Mean and 95% confidence interval / kPa'),ylabel=tr('独立抽样组编号','Independent sample-group index'),title=tr('展示前40组：区间随样本变化','First 40 groups: intervals vary across samples'))
    counts=[cases[f'{n}_0.95']['coverage_count'] for n in [5,10,30,50]]
    ax[1].bar([0,1,2,3],np.array(counts)/2,color=BLUE,width=.55);ax[1].axhline(95,color=RED,ls='--',label=tr('设定置信水平95%','Nominal confidence 95%'))
    for i,count in enumerate(counts):ax[1].text(i,max(97,count/2+2),f'{count}/200',ha='center',fontsize=11)
    ax[1].set(xticks=[0,1,2,3],xticklabels=[5,10,30,50],ylim=(0,105),xlabel=tr('每组试样数 n','Specimens per group, n'),ylabel=tr('覆盖20 kPa的比例 / %','Intervals covering 20 kPa / %'),title=tr('全部200组的实际覆盖率','Observed coverage over all 200 groups'));ax[1].legend(frameon=False,fontsize=9);save(fig,'coverage')
    summary={'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'seed':SEED,'groups':200,'cases':cases,
        'hand_mean_kPa':float(hand.mean()),'hand_sd_kPa':float(hand.std(ddof=1)),'hand_sem_kPa':hand_sem,'hand_critical95':hand_q,'hand_halfwidth95_kPa':hand_q*hand_sem,'hand_t':float(hand_test.statistic),'hand_p':float(hand_test.pvalue)}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

`samples.csv`保留全部读数，`sample-bank.json`保存同一数据与交互需要的临界值，`summary.json`记录不同样本量和置信水平的覆盖数量、平均区间宽度以及第一组的具体结果。图中的“覆盖”通过比较区间端点与已知20 kPa得到，没有把点的位置靠近参考线当成覆盖。因为模拟总体在这里已知，这项检验能够直接进行。

阅读输出时先从手算五点示例检查均值20、标准差√10、标准误√2，再核对第一组模拟样本。数组方向尤其值得检查：沿行求值是在一个实验内部汇总试样，沿列求值则是在不同实验中汇总同一编号位置。两种运算都会返回数字，只有与抽样单位一致的方向才回答本节的问题。

## 联动查看一个样本、它的均值和它的区间

下面的实验保留与Python完全相同的200组读数。选择每组的试样数量与置信水平，再移动组编号，可以同时看到当前组的全部点、它在200组均值分布中的位置，以及它所在的一页40条区间。当前组用较粗线标出，未覆盖20 kPa的区间用红色显示。读数中的覆盖比例始终使用全部200组，图中40条只是为了让每条都能清楚阅读。

### 200次抽样中的一个具体样本

[Figure: 40条可追踪的样本均值区间](https://ml-biomat.com/tutorials/python-scientific/p22/#P22-intervals)

[Figure: 当前样本的全部读数](https://ml-biomat.com/tutorials/python-scientific/p22/#P22-sample)

[Figure: 全部200个样本均值的分布](https://ml-biomat.com/tutorials/python-scientific/p22/#P22-means)

虚线为规定总体均值20 kPa，红色区间未覆盖它。上图每页40组；所有读数中的覆盖数量均以全部200组计算。

先固定某一个组编号，把试样数从5增加到50，观察新加入的读数怎样共同改变均值和区间。更大样本通常提高精度，但某一个具体样本的均值不必在每一步都朝20靠近。然后固定样本量，只把95%改为99%，原始读数和均值都保持不变，只有临界倍数与区间宽度变化。两次操作分别改变数据量与估计规则，可以逐项比较其影响。

再找一条红色区间，查看对应样本是否整体偏向20的一侧，或者样本波动估计较小。区间没有覆盖真值，是重复抽样中可以出现的结果。查看这类样本能够帮助理解方法的频率性质，同时也提醒我们在真实分析中保存完整读数和抽样信息，让估计范围背后的数据结构保持可见。

本节选择正态总体，是为了让小样本t方法的条件与验证完全对应。实际数据的分布可以先通过全部点、直方图和分位数图查看，并结合测量机制理解。只有五个点时，很难仅凭外形判断尾部或偏斜；这时已有的工艺知识、更多独立样本和针对研究问题的稳健分析都能提供帮助。模拟适合把这些条件逐一改变，观察估计规则会怎样响应。

## 把统计结果写回研究问题

报告一个均值时，把独立试样数、测量单位、离散程度和区间定义一起交代清楚。例如可以写某组10个独立试样的平均读数为18.654 kPa，95% t置信区间为16.403至20.904 kPa，并说明这些数值来自教学正态抽样模型。真实研究则填入实际样品范围、抽样设计与处理条件，让读者知道这个均值代表哪一类对象。

选方法之前先看数据的形成方式。配对前后测量可以分析每一对的差，多个制备批次需要保留批次结构，强烈偏斜或少量极端读数需要结合分布形状选择合适的估计方法。统计工具之所以有用，是因为它把抽样、估计和判断连接起来；一个清楚的结果既有数值，也让人看得懂这些数值如何从独立信息中产生。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P22.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SciPy: ttest_1samp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html)

   单样本检验、独立观测与置信区间接口。

   BSD-3-Clause; technical reference
2. [SciPy: Student t distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)

   自由度、分位数和概率密度。

   BSD-3-Clause; technical reference
3. [SciPy: sem](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sem.html)

   标准误与自由度修正。

   BSD-3-Clause; technical reference
4. [Student (1908), The Probable Error of a Mean](https://en.wikisource.org/wiki/The_Probable_Error_of_a_Mean)

   原论文关于小样本均值与波动估计的讨论；图为原创计算。

   Public-domain original; historical reference
