# 用积分和微分方程描述变化

Source: https://ml-biomat.com/tutorials/python-scientific/p21/
Language: zh-CN

从三种状态之间的转化，理解变化率、小步推进、守恒和累计面积。

## 一种物质经过中间态，什么时候最适合观察

一份样品在处理过程中，可能先从状态A变成B，再从B变成C。A可以代表尚未转化的部分，B代表暂时出现的中间态，C代表已经完成后续变化的部分。观察终点时，B也许已经很少；若研究目标恰好是B，就需要知道它什么时候最多，以及它在整个过程里持续存在了多久。这两个问题分别对应曲线的峰值与曲线下的面积，也把微分方程和积分联系到同一个具体任务。

本节采用一个明确的教学模型：总量固定，A、B、C按一对一关系依次转化，体积和环境条件保持不变，没有额外流入、流出或逆向转化。用每种状态占初始总量的分数描述组成，初始时A为1，B和C都为0。这样可以把注意力集中在变化率上。应用到真实反应时，再根据物种、化学计量关系、体积变化和测量定义建立相应方程。

SciPy的`solve_ivp`能够从初始状态和变化规则计算随时间演化的轨迹，`quad`则能够累计一段函数曲线下的面积。我们会先用纸笔能够检查的小步计算理解这两种操作，再运行完整程序。已有解析答案的简单模型提供了清楚的参照，让步长、误差、守恒和积分单位都能落到实际数字上。

## 变化率是每分钟改变多少，方程先记录流向

假设A转成B的速率与当前A的数量成正比。A越多，同样时间内能够转化的量越多；A逐渐减少，转化速度也随之降低。本例取速率常数0.8 min⁻¹。若某时刻A占0.5，A减少的瞬时速率就是每分钟0.4个分数单位。这里的“瞬时”很关键：它描述当前这一刻的方向与速度，随着A减少，后面的速度也会变化。

$$
\frac{da}{dt}=-k_1a,\qquad\frac{db}{dt}=k_1a-k_2b,\qquad\frac{dc}{dt}=k_2b
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | 分别为A、B、C占初始总量的分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过的时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d62ad609310d0b90a08f3cae.svg) | A→B与B→C的速率常数，本例分别为0.8和0.3 min⁻¹。 |
| ![Formula](https://ml-biomat.com/static/agent-math/cf7a258783fb9a082f6d20a4.svg) | 各状态分数的瞬时变化率，min⁻¹；d表示微分。 |

每项都是“当前数量×单位时间的转化速率”。若a=0.5、b=0.3、c=0.2，三个变化率为−0.4、0.4−0.09=0.31、0.09 min⁻¹，相加为0。因此总分数的变化率为0，而各状态可以持续交换数量。

三个式子可以按账本来读。A只有支出，所以带负号；B一边接收A的转化，一边向C转出，因此是收入减支出；C只接收B的转化。把三个变化率相加，成对的流入与流出刚好抵消，说明总分数保持不变。第二个速率常数取0.3 min⁻¹，使B向C的转出相对较慢，B在早期能够积累，后期又随着A来源减少而下降。

符号中的导数可以从平均速度理解。用两个临近时刻的分数差除以时间差，得到这小段时间里的平均变化率；把时间间隔逐渐缩短，就走向某一时刻的变化率。它与位置—速度关系相似：知道现在的位置和速度，可以估计很短时间后的新位置。对这里的样品，位置换成三个分数，速度换成三个流向相互关联的变化率。

把初始总量归一为1，相当于把样品分成许多相同的计数单位，记录每个单位目前在哪个状态。这里的一对一转化保证单位总数保持不变。对于有多个反应物、产物数量不同的化学反应，应按化学计量关系选择浓度或物质量方程，再检查元素或质量守恒。分数方便教学，具体实验中的守恒对象则由实际过程决定。

## 从当前斜率向前走：把连续变化变成可计算的小步

十八世纪，Euler将积分和微分方程系统地组织为研究变化的数学工具。他的《积分学基础》第一卷于1768年出版。今天写一段数值程序时，仍然要处理同一个基本关系：已知变化规则，怎样恢复随时间变化的量。欧拉方法给出一种容易画出来的做法——先沿当前斜率走一小步，再在新位置重新计算斜率。

$$
\mathbf y_{n+1}=\mathbf y_n+h\,\mathbf f(t_n,\mathbf y_n)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f9863792b3128c856f71d728.svg) | 第n个计算节点的状态向量，包含a、b、c三个无量纲分数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/794309c181b5d3eef90282ba.svg) | 当前和下一个计算节点的整数编号，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 向前推进的时间步长，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a588fc41a723666b153cc137.svg) | 第n个节点的时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a06debad6e153cb789c38ba5.svg) | 由前述三个方程组成的变化率向量，各分量单位min⁻¹。 |

速度乘时间给出这一步的近似变化量，再加到当前状态上。初值(1,0,0)、步长0.5 min和变化率(−0.8,0.8,0) min⁻¹给出下一步(0.6,0.4,0)。三个分数合计1，但这一粗步尚未计入步内新生成B的进一步转化。

从A=1、B=0、C=0出发，当前变化率依次为−0.8、0.8、0 min⁻¹。如果一步取0.5 min，就把这些速度分别乘以0.5，加回原值，得到A=0.6、B=0.4、C=0。这一步把最初的速度保持了半分钟，所以它是一种近似。在真实连续模型里，A一开始减少，速度就随之减慢，而B刚出现就开始向C转化；分步计算到下一点才更新这些影响。

![欧拉方法以当前斜率连接相邻节点，细化步长后接近解析曲线。右图独立计算三个分数相对解析解的最大绝对误差，参考线表示与步长成正比的趋势。](https://ml-biomat.com/static/tutorials/python-scientific/figures/f04647f595c40c336922f754.svg?v=f04647f595c4)

图 1欧拉方法以当前斜率连接相邻节点，细化步长后接近解析曲线。右图独立计算三个分数相对解析解的最大绝对误差，参考线表示与步长成正比的趋势。

图中较粗的折线偏离解析曲线，缩短步长后逐渐靠近。右图把不同步长的最大绝对误差放在双对数坐标下，细步长区间大致沿着与步长成正比的方向变化。这种比较比单看一条光滑曲线更有解释力：绘图可以把少数点连接得很顺，真正的数值精度要通过步长变化、独立答案或更严格的求解设置来判断。

## 让求解器选择小步，自己明确初值和输出时刻

完整程序将变化规则写进`rhs(t, y)`。参数`t`是当前时间，`y`按A、B、C的顺序保存当前三个分数，返回值也按相同顺序给出三个导数。顺序就像表格的列名，一旦约定，后续初值、图例和误差检查都要一致。虽然本例的速率常数不随时间改变，接口仍保留时间参数，便于描述升温、外部输入或其他随时间变化的条件。

`solve_ivp`接收时间范围0到10 min和初值[1, 0, 0]，默认使用RK45方法。它在一个步长内利用多个位置的变化率，并依据误差估计调整内部步长。本例用`t_eval`要求在501个均匀时间点保存结果，便于比较与绘图；这些保存点并不意味着求解器内部始终采用0.02 min的步长。输出网格与算法实际走过的小步承担不同任务。

程序设置相对容差`rtol=1e-9`和绝对容差`atol=1e-11`。相对容差随分数大小缩放，绝对容差在数值接近零时仍提供误差控制尺度。它们约束的是求解器的局部误差估计，最终整条曲线的偏差还要通过结果检查。本例同时计算解析解，得到三种分数在全部保存点上的最大绝对差约7.21×10⁻¹¹，直接说明这次运行的数值吻合程度。

![同一串联模型的三个分数与B积分。左图为RK45数值解，右图用解析B曲线填出面积；时间单位min，总量初始归一为1。](https://ml-biomat.com/static/tutorials/python-scientific/figures/229f29c5e5b658545e3bc67f.svg?v=229f29c5e5b6)

图 2同一串联模型的三个分数与B积分。左图为RK45数值解，右图用解析B曲线填出面积；时间单位min，总量初始归一为1。

程序还把B的变化率设为事件函数，寻找它从正变负的位置。这个零点表示B从增加转为减少，也就是本模型的峰顶时刻，约为1.96166 min。事件定位在连续数值解上寻找零点，比直接挑出501个保存值中的最大值更细。实际使用时需要让事件函数对应清楚的科学条件，例如某个浓度达到阈值，或某种净流量改变方向。

解析解也可以从变化规律读懂：A每经过相同时间都会按相同比例减少，因此具有指数衰减形式。B不断接收不同时间由A转入的部分，而每一批转入的部分又按自己的停留时间向C衰减；把这些贡献相加，会得到两条指数曲线之差。C再由总分数减去A和B获得。程序中的解析表达式采用两个速率常数不同的形式，本节所有可选速率均满足这个条件。

$$
a(t)=e^{-k_1t},\qquad b(t)=\frac{k_1}{k_2-k_1}\left(e^{-k_1t}-e^{-k_2t}\right),\qquad c(t)=1-a(t)-b(t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db3924ef96d9ef424c4cfc5d.svg) | 初值(1,0,0)下，时间t时的三个分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/dec0f7dc61f0e9a546cd9d6d.svg) | t为时间(min)，两个速率常数单位min⁻¹，且本式要求两者不相等。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数函数的底数，约2.71828；指数中的速率常数乘时间为无量纲量。 |

代入t=0，两个指数均为1，因此a=1、b=0、c=0。代入t=2 min、速率0.8和0.3 min⁻¹，可得a≈0.201897、b≈0.555064、c≈0.243039，总和为1。该表达式提供独立于逐步求解的核对答案。

## 总量正确以后，还要看每个分数是否合理

守恒检查很有用，因为它把三个输出通过一个关系联系起来。若代码里把B的转出写成正号，或者忘记C的流入，总量就会出现明显漂移。然而，守恒本身只检验流量账是否对得上。欧拉步同时减去A转出的量、加给B，再把B转出的量加给C，所以即使步长很大，它仍然可能保持总分数为1。

![2 min欧拉步出现负A分数，却仍保持三个分数之和为1。上图虚线为连续解析模型，实线与圆点为粗步结果，下图单独检查总量。](https://ml-biomat.com/static/tutorials/python-scientific/figures/fcf207372151633a1539dfc5.svg?v=fcf207372151)

图 32 min欧拉步出现负A分数，却仍保持三个分数之和为1。上图虚线为连续解析模型，实线与圆点为粗步结果，下图单独检查总量。

把步长改为2 min，第一步就得到A=−0.6、B=1.6、C=0。总和确实还是1，但分数已经超出了这个物理模型的含义。原因是程序把初始每分钟0.8的转出速度保持了两分钟，搬走了1.6份，而起初只有1份。这个例子清楚地区分了三个问题：总量是否守恒，每个状态是否保持非负，以及数值轨迹是否接近连续方程的解。

对A单独的更新式，新的分数是原分数乘以“1减去速率常数乘步长”。要使非负的A在这一步之后仍非负，速率常数与步长的乘积就应不超过1。更大的步长还可能产生正负交替的振荡；当放大因子的绝对值超过1，振荡会增长。这个具体推导说明，选步长需要结合变化的快慢，不能只根据一张图上想显示多少个点决定。

遇到一个过程变化很快、另一个过程变化很慢的模型，显式算法可能被最快的时间尺度限制，这也是刚性问题常见的来源。SciPy提供Radau和BDF等方法处理此类方程。判断时先看时间尺度、求解器状态、函数求值次数和收紧容差后的变化，再选择适合模型的方法；更换算法之后，守恒、非负和关键输出仍然值得一起检查。

误差比较还需要明确“在哪些位置比较”。本节欧拉曲线的误差在每个欧拉节点上计算，每个节点先分别求A、B、C的绝对差，再取其中最大的一个；全程最大误差再从这些节点值中取最大。它回答的是最差的已计算分量偏了多少，和平均误差承担不同作用。由于所有分量都是分数，三者可以直接比较；单位或量级差别很大的状态变量需要先确定合适的缩放方式。

## 曲线下的面积，把数量和持续时间一起累计

B在某一时刻有多少，与B在整个过程里出现了多久，是两个不同的问题。若B分数在一段0.5 min时间内近似为0.4，这一小段的“分数乘时间”就是0.2 min。把整段过程分成很多这样的小条，再把它们相加，就得到B曲线下的面积。由于分数无量纲，面积的单位是min；若纵轴换成浓度mmol/L，面积的单位就会变成mmol·min/L。

$$
I_B(T)=\int_0^T b(t)\,dt\;\approx\;\sum_{n=0}^{N-1} b(t_n)h,\qquad T=Nh
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a11305f0a6beaa6b17d10d0f.svg) | 从0到T的B分数积分，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ea3059ae9f52fe6b926fbbba.svg) | 时间t时B的分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | 积分中的时间与终止时间，min。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f31d38e9354f49723c5bb666.svg) | dt表示极短时间增量；积分号表示连续累计，单位由被积函数乘min确定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a23a4935fef8a0becb8f51d8.svg) | h为均匀步长(min)，N为总步数，n为0至N−1的整数编号，t_n=nh为各小条左端时间(min)。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 将N个左端矩形的面积相加。 |

若两段各0.5 min的B分数近似为0.4和0.5，两块矩形的面积为0.2和0.25 min，合计0.45 min。缩短小条可更细地描述曲线。完整模型在0–10 min上的积分为3.068473 min；公式右边的有限和是指定左端矩形规则下的近似。

从0到10 min，本模型B的积分约为3.068473 min。它可以解释为所有初始单位在这一观察窗口中处于B状态的平均累计时间；如果只有少部分进入B，或很快离开B，面积都会减小。这样的量适合比较暂态的持续程度。对于具体实验，应再把该积分与实际研究目标对应起来，例如中间态暴露量、累计释放量或反应贡献，并保留正确的单位。

`quad`接收一个能够在任意指定时间求值的函数，本例把解析B函数交给它积分。返回的第二个数是数值积分误差的估计，本次约3.41×10⁻¹⁴ min。它描述计算方法对给定函数的积分误差；速率常数的实验误差需要通过参数变化或不确定度传播另行评估。明确这两类误差的对象，才能正确使用程序返回的精细数字。

如果手里只有离散测量点，可以用`trapezoid`把相邻两点之间的区域视为梯形，再将各梯形面积相加。本例对501个解析值作梯形积分得到3.068446 min，与直接函数积分略有差别。这一区别来自有限采样和插值形状。时间间隔不均匀时，应把实际时间数组一同传入，而不能把行号当成等间隔时间。

对完整无限时长的过程，还可以从账本得到一个简洁检验：C最后接收全部初始单位，累计的B→C转移为1。因为该流量在每一刻等于0.3 min⁻¹乘B分数，B在无限时间上的积分就是1除以0.3 min⁻¹，即约3.333333 min。本节只积分到10 min，所以得到较小的3.068473 min；剩余差值对应10 min之后B仍会持续存在的尾部。

## 完整程序：把模型、数值算法与核对答案放在一起

下面的程序保留了三条清楚的计算路径。`rhs`提供变化率，`solve_ivp`据此推进状态；`exact`给出同一模型的解析解，用来比较数值输出；`euler`显式执行简单小步，展示步长为何影响结果。解析函数只用于这个有闭式答案的案例，数值求解的接口则可以继续用于更复杂的模型。

### 完整示例：串联转化、峰顶事件、积分与步长比较

运行后生成三幅图、fractions.csv和summary.json。所有输入与解析核对函数包含在程序内。

```
"""Follow a conserved three-state conversion with integration and an ODE solver."""
from pathlib import Path
import argparse,json
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad,trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

COLORS=['#28658c','#c26835','#477f67']
K1,K2=.8,.3


def exact(t,k1=K1,k2=K2):
    t=np.asarray(t);a=np.exp(-k1*t)
    b=k1/(k2-k1)*(np.exp(-k1*t)-np.exp(-k2*t))
    return np.array([a,b,1-a-b])


def rhs(t,y,k1=K1,k2=K2):
    a,b,c=y
    return np.array([-k1*a,k1*a-k2*b,k2*b])


def euler(h,k1=K1,k2=K2):
    t=np.linspace(0,10,round(10/h)+1);y=np.zeros((3,len(t)));y[:,0]=[1,0,0]
    for i in range(len(t)-1):y[:,i+1]=y[:,i]+h*rhs(t[i],y[:,i],k1,k2)
    return t,y


def b_integral(end,k1=K1,k2=K2):
    return k1/(k2-k1)*((1-np.exp(-k1*end))/k1-(1-np.exp(-k2*end))/k2)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    available={f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family':[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in available],'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    t=np.linspace(0,10,501)
    def peak_b(t,y):return K1*y[0]-K2*y[1]
    peak_b.direction=-1
    solution=solve_ivp(rhs,(0,10),[1.,0.,0.],t_eval=t,rtol=1e-9,atol=1e-11,events=peak_b)
    if not solution.success:raise RuntimeError(solution.message)
    reference=exact(t);area,area_error=quad(lambda time:float(exact(time)[1]),0,10,epsabs=1e-11)
    comparisons={}
    for h in [.1,.5,1.,2.]:
        te,ye=euler(h);comparisons[str(h)]={'max_error':float(np.max(np.abs(ye-exact(te)))),'min_fraction':float(ye.min()),'sum_error':float(np.max(np.abs(ye.sum(axis=0)-1))),
            'first_step':ye[:,1].tolist(),'final':ye[:,-1].tolist(),'left_integral_B_min':float(h*ye[1,:-1].sum())}
    np.savetxt(args.output/'fractions.csv',np.column_stack([t,solution.y.T,reference.T]),delimiter=',',comments='',header='time_min,A_numeric,B_numeric,C_numeric,A_exact,B_exact,C_exact')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained',gridspec_kw={'width_ratios':[1.5,1]})
    for i,name in enumerate('ABC'):ax[0].plot(t,solution.y[i],color=COLORS[i],lw=2.3,label=name)
    ax[0].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('状态分数，无量纲','State fraction, dimensionless'),title=tr('A → B → C：中间态先升后降','A → B → C: an intermediate rises and falls'),xlim=(0,10),ylim=(0,1));ax[0].legend(frameon=False);ax[0].grid()
    ax[1].fill_between(t,0,reference[1],color=COLORS[1],alpha=.2);ax[1].plot(t,reference[1],color=COLORS[1],lw=2)
    ax[1].text(.96,.92,tr(f'0–10 min的面积\n{area:.6f} min',f'Area over 0–10 min\n{area:.6f} min'),ha='right',va='top',transform=ax[1].transAxes)
    ax[1].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('B的分数，无量纲','Fraction in B, dimensionless'),title=tr('面积累计“数量 × 持续时间”','Area accumulates fraction × time'),xlim=(0,10),ylim=(0,.65));ax[1].grid();save(fig,'conversion')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for h,color in zip([1.,.5,.1],['#b64a35','#8f8990',COLORS[0]]):
        te,ye=euler(h);ax[0].plot(te,ye[0],'.-',color=color,lw=1.4,label=f'h = {h:g} min')
    ax[0].plot(t,reference[0],'--',color='#20313e',lw=1.8,label=tr('解析曲线','Analytic curve'))
    ax[0].set(xlim=(0,3),ylim=(0,1.02),xlabel=tr('时间 / min','Time / min'),ylabel=tr('A的分数，无量纲','Fraction in A, dimensionless'),title=tr('欧拉步：沿当前斜率向前走','Euler steps: advance along the current slope'));ax[0].legend(frameon=False,fontsize=10);ax[0].grid()
    hvals=np.array([.025,.05,.1,.2,.5,1.]);errors=[]
    for h in hvals:
        te,ye=euler(h);errors.append(np.max(np.abs(ye-exact(te))))
    ax[1].loglog(hvals,errors,'o-',color=COLORS[1],label=tr('三种分数的最大绝对误差','Maximum absolute error across A, B, C'))
    ax[1].loglog(hvals,errors[0]*hvals/hvals[0],':',color='#71808b',label=tr('与步长成正比的参考线','Reference proportional to step size'))
    ax[1].set(xlabel=tr('步长 h / min','Step size h / min'),ylabel=tr('最大绝对误差，无量纲','Maximum absolute error, dimensionless'),title=tr('缩短步长，检验逐步逼近','Reduce the step and inspect convergence'));ax[1].legend(frameon=False,fontsize=9);ax[1].grid(which='both');save(fig,'history')
    fig,ax=plt.subplots(2,1,figsize=(12,7.5),layout='constrained',gridspec_kw={'height_ratios':[1.5,1]})
    te,ye=euler(2.)
    for i,name in enumerate('ABC'):
        ax[0].plot(t,reference[i],color=COLORS[i],alpha=.5,ls='--');ax[0].plot(te,ye[i],'o-',color=COLORS[i],label=name)
    ax[0].axhline(0,color='#20313e',lw=1);ax[0].set(ylabel=tr('状态分数，无量纲','State fraction, dimensionless'),title=tr('h = 2 min：总量保持，个别分数却变成负值','h = 2 min: total is conserved while a fraction becomes negative'));ax[0].legend(frameon=False,ncol=3);ax[0].grid()
    ax[1].plot(te,ye.sum(axis=0),'o-',color='#20313e');ax[1].set(ylim=(.95,1.05),xlabel=tr('时间 / min','Time / min'),ylabel=tr('A + B + C，无量纲','A + B + C, dimensionless'),title=tr('守恒、非负与准确性是三项不同检查','Conservation, positivity, and accuracy are separate checks'));ax[1].grid();save(fig,'checks')
    summary={'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'rates_per_min':[K1,K2],
        'solver_success':bool(solution.success),'solver_max_error':float(np.max(np.abs(solution.y-reference))),
        'solver_sum_error':float(np.max(np.abs(solution.y.sum(axis=0)-1))),
        'B_peak_time_min':float(solution.t_events[0][0]),'B_peak_time_exact_min':float(np.log(K1/K2)/(K1-K2)),
        'integral_B_min':area,'integral_B_exact_min':float(b_integral(10)),'quad_error_estimate_min':area_error,
        'trapezoid_B_min':float(trapezoid(reference[1],x=t)),'euler':comparisons}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

读完代码后，可以先检查输出文件中的第一行：时间为0，三种数值分数和解析分数都应是1、0、0。再检查最后一行，确认A已经很少、C占主要部分。摘要同时记录求解器是否成功、与解析解的最大差、总量偏差、B的峰顶时刻和积分值。每项记录对应前文的一个科学或计算问题，而不是把所有返回值都堆进表格。

程序中的峰顶定位和积分各自使用适合的问题形式。峰顶是变化率的零点，所以交给事件检测；面积是函数在区间上的累计，所以交给积分。若以后只拿到实验采样数据，可以先明确要保留怎样的插值或局部模型，再选相应工具。把问题形式说清楚，通常比记住更多函数名更能帮助选择算法。

## 联动实验：改变速度和步长，观察三项检查怎样分开

实验同时显示三种状态的连续解析曲线与欧拉折线、当前时刻的组成，以及各数值节点相对于解析解的最大误差。改变第一步转化速率，会改变整个过程的物理时间尺度；改变欧拉步长，则改变对同一连续过程的数值近似。把这两个控制放在一起，能够看到模型参数与算法参数各自改变了什么。

### 过程速度与计算步长

[Figure: 三个分数的连续解和欧拉近似](https://ml-biomat.com/tutorials/python-scientific/p21/#P21-trajectory)

[Figure: 当前组成比较](https://ml-biomat.com/tutorials/python-scientific/p21/#P21-composition)

[Figure: 各节点的最大分数误差](https://ml-biomat.com/tutorials/python-scientific/p21/#P21-error)

颜色依次对应A、B、C。主图实线为解析解，带圆点折线为欧拉结果；组成图浅色柱为解析值，深色柱为欧拉插值。

先保持0.8 min⁻¹的转化速率，将步长从0.1 min改到0.5 min、1 min和2 min。总量仍接近1，但最大误差逐渐变大，2 min时出现负分数。再把速率降到0.4 min⁻¹，观察同样步长怎样对应不同的转化比例。当前时刻的数值分数通过欧拉节点间的直线插值得到，节点误差则始终在算法实际计算的位置上比较。

读数中的B积分采用欧拉左端矩形累计，因而同时受状态近似和面积近似影响；解析积分提供独立参照。移动观察时刻只改变组成图的截面，整段0到10 min的最大误差与积分不会随观察位置改变。这样可以把“曲线的哪个位置”与“整次计算有多准确”分开阅读。

## 把变化问题交给计算机前，先把量和条件放稳

准备自己的模型时，可以从一张流向图开始：哪些量需要随时间保存，哪些过程增加它们，哪些过程减少它们，初始值和单位分别是什么。先让每条流向在方程中成对出现，再检查相加后应该保持什么。若系统存在输入输出，总量变化也应与这些边界流量对应。这个步骤往往比立即调节求解器参数更能发现模型中的遗漏。

运行之后，把关键科学量与数值设置一起保存，例如峰顶时间、累计面积、初值、速率参数、求解方法和容差。选取几组更严格的设置比较关键量是否稳定，再把主要变化与实验参数联系起来。数值积分和微分方程求解由此成为一条完整的研究链：从流向解释变化，从曲线读取过程，再把过程浓缩成有单位、有含义的结果。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P21.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SciPy: Integration tutorial](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

   函数积分、采样积分和结果核对。

   BSD-3-Clause; technical reference
2. [SciPy: solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)

   初值问题、RK45、容差和事件定位。

   BSD-3-Clause; technical reference
3. [SciPy: quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)

   自适应积分与误差估计的含义。

   BSD-3-Clause; technical reference
4. [Euler Archive: Foundations of integral calculus, volume 1](https://scholarlycommons.pacific.edu/euler-works/342/)

   1768年原著的档案记录；方法图为本节原创计算。

   Public-domain original; bibliographic reference
