# 平滑之后，峰还在吗：SciPy信号处理

Source: https://ml-biomat.com/tutorials/python-scientific/p20/
Language: zh-CN

把采样、局部拟合、峰定位和频率响应连起来，检查平滑对信号形状的影响。

## 曲线变平滑之后，峰还在原来的位置吗

传感器记录一个短暂过程时，曲线上常会同时出现缓慢变化、真正的峰和快速起伏。比如一次样品经过检测器，电压先升高再降低，而电源或机械振动又叠加了周期干扰。你希望知道峰在什么时候出现、最高到多少，往往会先平滑曲线。问题在于，平滑不仅改变起伏，也可能改变峰的高度、宽度和位置。本节用SciPy处理一条组成明确的教学信号，观察每一步处理保留了什么、改变了什么。

我们会建立两个宽度不同的峰，加入两个已知频率的周期干扰，然后比较移动平均与Savitzky–Golay局部多项式平滑。接着使用`find_peaks`定位满足条件的局部峰，再从频率视角理解窗口的作用。全部结果都与原先已知的平滑模型对照，因此能具体区分残留干扰和形状偏差。完整程序会输出原始数组、平滑结果、峰位置和数值摘要。

这里“信号”只是按时间排列的一串测量值。它可以来自光强、电压、位移或其他仪器读数；本节统一用mV表示幅值，用s表示时间。处理函数首先看到的是数组，时间单位需要通过采样间隔显式带入。理解这层关系，才能把“21个点的窗口”解释为实际的时间范围。

## 先看采样间隔，再讨论窗口大小

本例从0到10 s每隔0.02 s取一个值，共501条记录。每秒取50个样本，所以采样频率为50 Hz。相邻数组位置对应固定的时间间隔，这使得按位置移动的滤波窗口也对应固定时间范围。若仪器记录的时间不均匀，需要先检查实际时间戳；直接把连续21个点当成同样宽的时间窗口，会让不同位置接受不同的平滑范围。

21点的中心窗口在当前点左右各取10个点，因此最早到最晚的样本跨度为20×0.02=0.40 s。5点跨度为0.08 s，41点跨度为0.80 s。窗口长度说的是参与计算的样本数，跨度说的是首末样本之间的时间差，两者相差一个采样间隔。把这两个量放在一起，读者就能判断窗口与真实峰宽是否处于相近尺度。

采样还决定可分辨的变化速度。对于以50 Hz均匀采样的信号，25 Hz是Nyquist频率；超过这个界限的连续周期变化会与较低频率的采样序列混淆。可以把它想成摄像机看旋转车轮：每次拍到的位置不足以唯一确定两帧之间实际转过多少圈。我们加入9 Hz与17 Hz干扰，它们都位于25 Hz以内，因此可以在后面的频域图中找到。更快的成分应在采集前通过合适的模拟滤波与采样设计处理。

## 构造一条每个部分都能解释的教学信号

平滑模型由缓慢上升的基线和两个钟形峰组成。基线从0.1 mV开始，以每秒0.02 mV上升；第一个峰中心在3 s，幅值1.2 mV、时间尺度0.25 s，第二个在7 s，幅值0.8 mV、时间尺度0.5 s。这里的峰幅值指高出基线的部分，图上纵坐标则包含基线。第一个峰较窄，所以它对过宽的平滑窗口更敏感。

$$
y_{\mathrm{clean}}(t)=b_0+b_1t+\sum_{j=1}^{2}A_j\exp\!\left[-\frac{(t-\mu_j)^2}{2w_j^2}\right]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f54c83f4dc801bfa41bd22ff.svg) | 无干扰教学模型在时刻t的电压，mV |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | 基线截距0.1 mV |
| ![Formula](https://ml-biomat.com/static/agent-math/86ef2a91a3da50f97dc73bcd.svg) | 基线斜率0.02 mV/s |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 两个峰的序号1或2，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/cb2c27f1e1ca2cb88caf17da.svg) | 高出基线的峰幅值，依次1.2与0.8 mV |
| ![Formula](https://ml-biomat.com/static/agent-math/7d98312b42264644b238b90b.svg) | 峰中心时间，依次3与7 s |
| ![Formula](https://ml-biomat.com/static/agent-math/f6264b954f8fef8d9872def7.svg) | 峰时间尺度，依次0.25与0.5 s |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | 自然指数函数，自变量由时间平方之比构成，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/52d4c787eb9b2a9aa747a1d4.svg) | 将两个峰的电压贡献相加 |

每个峰在t=μ_j处指数为0，所以贡献为A_j；离中心越远，负指数绝对值越大，贡献越小。t=3 s时，基线0.1+0.02×3=0.16 mV，第一个峰为1.2 mV，第二个峰约为0.8 exp(−32) mV，总值约1.36 mV。w描述时间方向的宽度，不是电压测量的标准差。

在平滑模型上，我们再加入幅值0.12 mV、频率9 Hz的正弦项，以及幅值0.035 mV、频率17 Hz的余弦项。这些是规定好的周期干扰，而非从某个仪器采集的随机噪声。这样的设计让每次运行得到相同数据，也让频域中的两个高频成分有明确来历。真实实验中可能同时存在随机噪声、基线漂移和其他周期扰动，需要结合仪器与重复记录逐项判断。

在3 s处，平滑模型约为1.36 mV：基线0.16 mV加上第一个峰1.2 mV，第二个峰在这里的贡献极小。叠加干扰后，这个时刻的记录约为1.395 mV。附近更高或更低的样本既受真实峰形影响，也受周期项影响。只选原始数组中的最大值，会把这两种作用一起带入峰高判断。

## 从平均附近数值，到保留局部曲率

最直接的平滑方式是把当前点及其邻居相加，再除以点数。它利用相邻值共同估计中心位置，能减弱某些快速变化，但也会把弯曲峰顶向周围较低的值拉近。1964年，Abraham Savitzky与Marcel Golay介绍了以局部最小二乘多项式完成平滑和求导的方法。对于等间隔采样与固定窗口，局部拟合可以改写成一组重复使用的权重，使计算保持简单，同时更好地保留局部多项式形状。

![原创方法图解：五个二次曲线样本经移动平均得到中心值2 mV，经二次局部拟合得到0 mV。右图显示两种方法的固定权重，说明Savitzky与Golay将局部拟合化为重复加权的思想。](https://ml-biomat.com/static/tutorials/python-scientific/figures/be79f77ed9b0e3602198d895.svg?v=be79f77ed9b0)

图 1原创方法图解：五个二次曲线样本经移动平均得到中心值2 mV，经二次局部拟合得到0 mV。右图显示两种方法的固定权重，说明Savitzky与Golay将局部拟合化为重复加权的思想。

看图中的五个值4、1、0、1、4，它们位于相对位置−2、−1、0、1、2，恰好构成一段二次曲线。移动平均输出2，把中心从0抬高了；用二次多项式拟合这五个点，再取中心位置的值，会得到0。差别来自模型假设：平均值在窗口内只保留一个水平高度，二次拟合允许局部弯曲。对于峰顶这样的区域，曲率正是需要保留的信息。

$$
\widetilde y_i=\sum_{k=-m}^{m}c_k y_{i+k},\qquad N=2m+1
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8985c98a921e74cb3aa7e8e1.svg) | 第i个位置的平滑输出，mV |
| ![Formula](https://ml-biomat.com/static/agent-math/45b1400cf31b096a28adc5db.svg) | 相对中心偏移k个样本的输入值，mV；边界外按指定规则延伸 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 当前输出的样本序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 相对中心的整数样本偏移，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 中心左右各取的样本数，非负整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 窗口内总样本数，奇数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/7b0456e549b6eae9fe9ab8b6.svg) | 偏移k处的固定权重，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对窗口内各输入与权重的乘积求和 |

五点窗口m=2、N=5。移动平均的五个权重均为1/5，输入4、1、0、1、4 mV时输出2 mV。二次Savitzky–Golay权重为[−3,12,17,12,−3]/35，同一输入得到0 mV，保持这段二次曲线的中心值。权重总和为1保证常数信号保持原值。

五点二次平滑的权重按位置依次为−3、12、17、12、−3，再统一除以35。两端出现负权重，使中心输出可以修正曲率带来的平均偏差；权重总和仍然为1，所以常数输入保持不变。把4、1、0、1、4代入，分子为−12+12+0+12−12=0。负权重也意味着输出可能超过局部样本的最大或最小值，尤其在突变与边界附近，需要从函数形状理解这种结果。

SciPy的`savgol_filter`用窗口长度与多项式阶数指定这种局部拟合。本节固定二次多项式，把注意力放在时间范围上。窗口需要容纳足够多的点来确定系数；中心对称的奇数窗口使当前样本处于正中。提高阶数能保留更复杂的局部变化，也会保留更多快速起伏，因此要结合目标特征的时间尺度选择。

可以把整个过程想成沿记录移动的一把短尺：普通平均把尺子覆盖的数值压成同一个水平高度，局部二次拟合则允许尺子在这一小段弯曲。每到一个新位置，都用相邻样本重新决定这段曲线，再读取中心。采样间隔相等、窗口和阶数固定时，最小二乘方程的几何结构也固定，因此可以预先求出一组权重，沿着整条记录重复使用。这正是局部拟合能够高效执行的原因。

## 窗口走到边界时，计算需要什么信息

中心窗口在记录内部可以同时取左右邻居，走到第一个样本时却没有更早的数据。软件必须用某种边界规则补足计算。本例采用`mode='mirror'`：把边界内的数据向外镜像，且镜像时不重复最靠近边界的端点。若原始序列开头为a、b、c，向左延伸的位置依次对应b、c。这个规则保持数组长度，也为开头与结尾的输出提供了明确计算方式。

镜像相当于给边界附近增加了一个形状假设。若真实信号在端点仍有斜率，反射出的变化方向与真实延续可能不同，因此边缘结果需要与边界规则一起读。SciPy还支持局部多项式外推等模式，适合不同情况。本节让移动平均与Savitzky–Golay都使用相同镜像规则，使比较主要反映权重差异。研究中可以保留一段额外采样范围，再把关心的分析区域放在内部，减少结果对端点处理的依赖。

这种对称窗口同时使用过去与未来的值，适合已经完整记录的数据分析。在线控制设备在当前时刻还没有未来记录，就需要因果滤波或等待足够数据后再输出。两种工作方式的时间延迟与边界含义不同。为离线信号选择一个看起来很平滑的参数之后，应再核对它是否适合实际使用场景。

## 平滑之后再定位峰，仍要保留明确的判据

下面用21点二次Savitzky–Golay处理信号。原始快速起伏明显减弱，两个较慢的峰仍然可辨。下排画出平滑结果减去已知模型后的差值：5点窗口保留较多周期干扰，41点窗口在较窄峰附近引入更明显的形状偏差。21点在这组明确规定的数据上得到较小的整体误差，这个比较依赖当前峰宽、干扰频率和采样间隔。

![上图比较规定干扰输入、已知模型与21点二次Savitzky–Golay输出，红点是突出度至少0.3 mV、间隔至少100点的峰。下图比较不同窗口相对已知模型的误差，采样间隔0.02 s，边界采用镜像。](https://ml-biomat.com/static/tutorials/python-scientific/figures/6a7dcf87eb526340d55ed6f4.svg?v=6a7dcf87eb52)

图 2上图比较规定干扰输入、已知模型与21点二次Savitzky–Golay输出，红点是突出度至少0.3 mV、间隔至少100点的峰。下图比较不同窗口相对已知模型的误差，采样间隔0.02 s，边界采用镜像。

`find_peaks`先寻找高于相邻值的局部最大位置，再按给定条件筛选。`distance=100`的单位是样本点，在本例对应2 s；它让保留的峰至少相隔这么远。`prominence=0.3`表示要求峰相对于周围背景的突出程度至少为0.3 mV。突出度通过向两侧寻找相应基底确定，与峰在纵轴上的绝对高度不同。较高的基线会抬升峰值，但不一定产生同样大的突出度。

本例保留的峰位于3.00 s与7.02 s，峰值约为1.35605与1.04352 mV。第二个峰的采样位置与规定的7 s中心略有不同，基线上升和残留干扰都会影响总曲线局部最大值的位置。数组返回的峰位置本来就是采样网格上的索引，乘以0.02 s才能成为时间。需要更细的定位时，可以在明确的局部模型下拟合峰顶，或者提高实际采样分辨率。

$$
\mathrm{RMSE}=\sqrt{\frac1n\sum_{i=1}^{n}(\widetilde y_i-y_{\mathrm{clean},i})^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ffa6620282ab195b6f2fd00.svg) | 与已知教学模型比较的均方根误差，mV |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 参与比较的总样本数501，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 样本序号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/8985c98a921e74cb3aa7e8e1.svg) | 平滑后的样本值，mV |
| ![Formula](https://ml-biomat.com/static/agent-math/a9aa8eda074ad6c3a6f6c7a6.svg) | 相同时刻无干扰模型的值，mV |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对全部比较位置求和 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bcc38017e1856dc949d86bd.svg) | 平方根，使结果回到mV单位 |

先将每个处理误差平方，使正负偏差不抵消，再平均和开方。若两点误差分别为0.03与−0.04 mV，RMSE=√[(0.0009+0.0016)/2]≈0.035355 mV。本节21点二次滤波对全部501点得到约0.005705 mV，包含边界处理、残留干扰与形状变化的共同影响。

这里可以计算均方根误差，是因为教学信号的无干扰模型已知。21点结果约为0.005705 mV，5点约为0.075340 mV，41点约为0.012498 mV。真实测量的平滑曲线通常没有这样的完整真值，可以通过独立重复、标定信号、已知特征或保留数据评价处理效果。仅看处理前后差值，会同时包含被去掉的干扰与被改变的真实形状，解释时需要结合研究目标。

突出度可以用两座处在不同山坡上的山峰来理解。山顶的海拔对应峰的绝对高度，而从附近可比较的谷地爬到山顶的高度更接近突出度。对信号而言，算法需要先确定两侧的基底，再取较高的基底作为参考水平。因此，选择突出度时应想到希望识别多明显的局部事件；选择最小距离时，则应想到两个独立事件至少隔多久。它们分别约束形状和时间，不能只用一个“峰值很高”的条件替代。

## 从频率看窗口：它保留哪些变化速度

时间图告诉我们信号何时变化，频率图则描述不同重复速度的成分。9 Hz表示每秒振动9次，17 Hz表示每秒17次；这两个成分在本例中都有已知来源。程序用`periodogram`计算功率谱密度，并明确给出50 Hz采样频率。纵轴单位mV²/Hz说明它描述每单位频率范围中的平方幅值贡献。采用Hann窗和线性去趋势，主要帮助处理有限记录的边界与缓慢基线。

![左图采用50 Hz采样频率、Hann窗与线性去趋势计算单边功率谱密度；右图由各窗口权重直接计算正弦幅值增益，虚线标出9 Hz。增益图描述滤波器，谱密度图描述本节有限时长数据。](https://ml-biomat.com/static/tutorials/python-scientific/figures/84d39982d93b80d9671a7c1d.svg?v=84d39982d93b)

图 3左图采用50 Hz采样频率、Hann窗与线性去趋势计算单边功率谱密度；右图由各窗口权重直接计算正弦幅值增益，虚线标出9 Hz。增益图描述滤波器，谱密度图描述本节有限时长数据。

有限时长的记录会把一个频率成分分散到相邻频率位置，窗函数又会改变峰宽和幅值分配，所以频域图需要与所用方法一起解释。501点记录的频率网格间隔约为50/501≈0.0998 Hz，9和17 Hz未必恰好落在网格点上。图中的局部峰仍然指出附近的周期成分。这里使用谱密度而非单个正弦的精确振幅估计，重点是比较平滑前后的频率分布。

右图直接由平滑权重计算不同频率的幅值增益。增益为1表示该频率的正弦幅值保持不变，0.1表示输出幅值约为输入的十分之一。21点窗口在9 Hz处的增益约为0.04464，而41点约为0.06804。更宽的窗口并没有在每一个频率都产生更强衰减，因为这些有限长度滤波器的频率响应带有起伏。选择参数时同时查看目标峰形与干扰频率，能比单纯追求更平滑的外观更清楚地判断效果。

幅值增益和功率谱纵轴还隔着一次平方。若某个正弦分量的幅值减为原来的0.1，它的平均平方幅值就减为0.01。右图采用幅值增益，便于直接理解输入和输出的振幅比例；左图采用功率谱密度，反映平方量在频率上的分配。在记录内部、远离边界时，固定权重对正弦成分的这种关系尤其清楚；有限记录中的窗函数和端点处理还会影响具体谱线外观。

## 完整程序与联动实验：从权重追到最终曲线

程序中的`data`函数明确生成平滑模型与周期干扰。主循环分别计算两种方法、四个窗口长度，将每种结果的误差、3 s读数、9 Hz增益和峰信息写入JSON。`savgol_coeffs`返回固定窗口对应的权重；`savgol_filter`把这些局部计算应用到整条序列；`find_peaks`再从结果中提取满足条件的峰。三个函数处理的是不同阶段，分别保留其输入与输出，有助于定位参数变化产生的影响。

### 完整Python：信号、平滑、峰与频率响应

显式信号生成后由SciPy实际滤波和定位峰，保留各方法的误差与完整数据，并生成三组科学图。

```
"""Inspect smoothing, peak finding, and frequency response on a defined teaching signal."""
from pathlib import Path
import argparse,json
import numpy as np
import scipy
from scipy import signal,ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

DT=.02
BLUE,RED,INK,GRAY='#28658c','#b64a35','#20313e','#71808b'


def data():
    t=np.arange(501)*DT
    clean=.1+.02*t+1.2*np.exp(-.5*((t-3)/.25)**2)+.8*np.exp(-.5*((t-7)/.5)**2)
    interference=.12*np.sin(2*np.pi*9*t)+.035*np.cos(2*np.pi*17*t)
    return t,clean,clean+interference


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    available={font.name for font in font_manager.fontManager.ttflist}
    font_names=[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in available]
    plt.rcParams.update({'font.family':font_names,
        'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    t,clean,observed=data();results={}
    for method in ['savgol','mean']:
        for window in [5,11,21,41]:
            coefficients=signal.savgol_coeffs(window,2) if method=='savgol' else np.ones(window)/window
            smoothed=signal.savgol_filter(observed,window,2,mode='mirror') if method=='savgol' else ndimage.uniform_filter1d(observed,window,mode='mirror')
            peaks,properties=signal.find_peaks(smoothed,prominence=.3,distance=100)
            # A centered symmetric filter has a real frequency response.
            offsets=np.arange(window)-window//2
            gain9=float(abs(np.sum(coefficients*np.cos(2*np.pi*9*DT*offsets))))
            results[f'{method}_{window}']={'rmse_mV':float(np.sqrt(np.mean((smoothed-clean)**2))),
                'value_at3s_mV':float(smoothed[150]),'gain9':gain9,
                'peak_times_s':t[peaks].tolist(),'peak_values_mV':smoothed[peaks].tolist(),
                'prominences_mV':properties['prominences'].tolist(),'coefficient_sum':float(coefficients.sum())}
    smooth=signal.savgol_filter(observed,21,2,mode='mirror');peaks,properties=signal.find_peaks(smooth,prominence=.3,distance=100)
    np.savetxt(args.output/'signal.csv',np.column_stack([t,clean,observed,smooth]),delimiter=',',comments='',
        header='time_s,clean_model_mV,with_interference_mV,savgol21_mV')
    fig,axes=plt.subplots(2,1,figsize=(12,8),layout='constrained',gridspec_kw={'height_ratios':[1.4,1]})
    axes[0].plot(t,observed,color='#bdc9d0',lw=1,label=tr('含规定干扰','Defined interference added'))
    axes[0].plot(t,clean,color=INK,lw=1.5,ls='--',label=tr('已知平滑模型','Known smooth model'))
    axes[0].plot(t,smooth,color=BLUE,lw=2,label=tr('Savitzky–Golay：21点，二次','Savitzky–Golay: 21 points, degree 2'))
    axes[0].scatter(t[peaks],smooth[peaks],color=RED,zorder=5)
    for i in peaks:axes[0].annotate(f'{t[i]:.2f} s',(t[i],smooth[i]),xytext=(8,13),textcoords='offset points',color=RED)
    axes[0].set(ylabel=tr('信号 / mV','Signal / mV'),title=tr('A  平滑与局部峰定位','A  Smoothing and local peak locations'));axes[0].legend(frameon=False,fontsize=10)
    for window,color in zip([5,21,41],[GRAY,BLUE,RED]):
        y=signal.savgol_filter(observed,window,2,mode='mirror');axes[1].plot(t,y-clean,color=color,label=tr(f'{window}点',f'{window} points'))
    axes[1].axhline(0,color=INK,lw=.8);axes[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('平滑结果 − 已知模型 / mV','Smoothed − known model / mV'),title=tr('B  误差同时包含残留干扰与峰形改变','B  Error includes residual interference and shape change'))
    for a in axes:a.grid();a.set_xlim(0,10)
    axes[1].legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3);axes[1].set_title(tr('B  误差同时包含残留干扰与峰形改变','B  Error includes residual interference and shape change'),pad=38);save(fig,'smoothing')
    fig,axes=plt.subplots(1,2,figsize=(12,5.6),layout='constrained')
    k=np.arange(-2,3,dtype=float);values=k*k;dense=np.linspace(-2,2,200)
    axes[0].plot(dense,dense*dense,color=BLUE,lw=2,label=tr('局部二次曲线','Local quadratic'))
    axes[0].scatter(k,values,color=INK,zorder=4,label=tr('五个样本值','Five sampled values'))
    axes[0].axhline(values.mean(),color=RED,ls='--',label=tr('移动平均的中心输出 = 2','Moving-mean center output = 2'))
    axes[0].scatter([0],[0],s=80,facecolors='white',edgecolors=BLUE,zorder=5,label=tr('二次拟合的中心输出 = 0','Quadratic-fit center output = 0'))
    axes[0].set(xlabel=tr('相对样本位置 k','Relative sample offset k'),ylabel=tr('教学数值 / mV','Teaching value / mV'),title=tr('保留局部曲率','Preserve local curvature'));axes[0].legend(frameon=False,fontsize=9)
    coefficients=signal.savgol_coeffs(5,2)
    axes[1].bar(k-.14,np.ones(5)/5,width=.28,color=RED,label=tr('移动平均','Moving mean'))
    axes[1].bar(k+.14,coefficients,width=.28,color=BLUE,label='Savitzky–Golay')
    axes[1].axhline(0,color=INK,lw=1);axes[1].set(xlabel=tr('相对样本位置 k','Relative sample offset k'),ylabel=tr('权重，无量纲','Weight, dimensionless'),xticks=k,title=tr('固定权重实现局部最小二乘','Fixed weights implement local least squares'));axes[1].legend(frameon=False,fontsize=10)
    fig.suptitle(tr('Savitzky与Golay（1964）：把局部拟合变成重复加权','Savitzky and Golay (1964): local fitting as repeated weighting'),fontsize=15)
    save(fig,'history')
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for y,color,label in [(observed,GRAY,tr('含干扰','With interference')),(smooth,BLUE,'SG21')]:
        freq,psd=signal.periodogram(y,fs=1/DT,window='hann',detrend='linear',scaling='density')
        axes[0].semilogy(freq,psd,color=color,lw=1.5,label=label)
    axes[0].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel='PSD / mV²·Hz⁻¹',xlim=(0,25),ylim=(1e-12,1),title=tr('频域：9 Hz与17 Hz干扰','Frequency view: 9 Hz and 17 Hz interference'));axes[0].legend(frameon=False)
    freq=np.linspace(0,25,501)
    for window,color in zip([5,21,41],[GRAY,BLUE,RED]):
        c=signal.savgol_coeffs(window,2);k=np.arange(window)-window//2;gain=np.abs(np.cos(2*np.pi*freq[:,None]*DT*k[None,:])@c)
        axes[1].plot(freq,gain,color=color,label=tr(f'{window}点',f'{window} points'))
    axes[1].axvline(9,color=INK,ls=':',lw=1);axes[1].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('幅值增益，无量纲','Amplitude gain, dimensionless'),title=tr('窗口决定保留哪些变化速度','The window selects rates of variation'),xlim=(0,25));axes[1].legend(frameon=False)
    for a in axes:a.grid()
    save(fig,'frequency')
    summary={'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},
        'sampling_interval_s':DT,'sampling_frequency_Hz':1/DT,'n':len(t),'cases':results,
        'sg5_coefficients':coefficients.tolist(),'quadratic_sg_center':float(coefficients@values),
        'quadratic_mean_center':float(values.mean())}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

下面的实验同步显示整条结果、当前窗口的权重和频率响应。选择移动平均或二次局部拟合，再改变窗口长度，能看到相同501条记录怎样产生不同结果。图中的3 s读数与RMSE由同一条处理后曲线计算；移动焦点只是查看窗口覆盖哪些原始样本，不会改变整条滤波结果。实验用局部最小二乘的闭式权重独立计算，并与Python的SciPy输出核对。

### 窗口、权重与结果联动

灰线为含规定周期干扰的输入，黑色虚线为已知平滑模型，蓝线为处理结果。窗口图的红点表示由边界镜像得到的输入；采样间隔固定0.02 s。

[Figure: 完整信号和当前窗口](https://ml-biomat.com/tutorials/python-scientific/p20/#P20-signal)

[Figure: 局部权重和输入样本](https://ml-biomat.com/tutorials/python-scientific/p20/#P20-weights)

[Figure: 频率响应幅值](https://ml-biomat.com/tutorials/python-scientific/p20/#P20-gain)

先选择5点二次拟合，观察较多干扰仍在；再改成21点，查看9 Hz增益与窄峰形状；最后改成41点，注意3 s附近峰顶被压低。切换为移动平均后，同样窗口对应的权重全部相等，频率响应和峰形偏差也随之改变。把焦点移到开头或结尾，还可以看到镜像规则如何为中心窗口提供样本。

读程序时可以先追踪一个位置，例如第150号样本对应3 s。21点窗口使用它前后各10个位置，时间从2.80到3.20 s。Python输出的1.35605 mV是这些21个观测值按固定权重相乘后相加的结果，已知平滑模型在3 s约为1.36 mV。改变焦点只是把这笔局部计算移到别处展示，改变窗口或方法才会重新计算整条曲线。把“查看哪里”和“怎样计算”分清，交互操作才真正帮助理解算法。

## 把处理参数写成能够复现的分析条件

使用真实信号时，首先保存原始时间和值，再记录采样间隔、平滑方法、窗口长度、多项式阶数与边界模式。描述峰时同时保存定位规则、最小间距、突出度以及峰值单位。这样，另一位读者才能判断某个峰是数据本身的特征，还是特定处理参数下的结果。若需要比较多个样品，处理条件通常应在共同的物理时间尺度上统一，而不只是机械使用相同点数。

对变化率的研究，还需要把时间单位带入求导。Savitzky–Golay支持局部多项式导数，使用一阶导数时应设置实际采样间隔，例如本例的`delta=0.02`。得到的单位是mV/s。直接对相邻样本做差会突出快速起伏，局部拟合可以在一定时间范围内稳定变化率估计；相应地，它也会把这个范围内的细节整合到一起。窗口选择仍然要围绕你希望识别的过程速度。

一条好的处理链让原始记录、模型假设、参数与结果之间的关系保持可见。时间图负责检查位置和形状，权重图解释局部计算，频率图说明哪些变化被保留或衰减。三种视角共同帮助我们从“曲线更顺了”走向具体判断：哪一种干扰被削弱，目标峰保留得如何，以及当前结果适合回答什么问题。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P20.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SciPy: signal processing tutorial](https://docs.scipy.org/doc/scipy/tutorial/signal.html)

   卷积、滤波与采样信号

   SciPy BSD-3-Clause; original teaching data and figures
2. [SciPy: Savitzky–Golay filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

   局部多项式与边界模式

   SciPy BSD-3-Clause; original teaching data and figures
3. [SciPy: Savitzky–Golay coefficients](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_coeffs.html)

   固定窗口的加权系数

   SciPy BSD-3-Clause; original teaching data and figures
4. [SciPy: find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)

   局部最大值、突出度和最小间隔

   SciPy BSD-3-Clause; original teaching data and figures
5. [SciPy: periodogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html)

   谱密度、采样率与窗函数

   SciPy BSD-3-Clause; original teaching data and figures
6. [Savitzky & Golay (1964), Smoothing and Differentiation of Data by Simplified Least Squares Procedures](https://doi.org/10.1021/ac60214a047)

   局部拟合平滑方法的原始论文

   Historical and technical reference; no reproduced passage or figure
