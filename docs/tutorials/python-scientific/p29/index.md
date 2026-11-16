# 从材料实验表格走到可复查的结论

Source: https://ml-biomat.com/tutorials/python-scientific/p29/
Language: zh-CN

用真实吸附数据连接表格、参数、残差和下一轮测量，比较模型形状与压力覆盖的影响。

## 一张吸附曲线，怎样变成可复查的材料结论

空气净化材料为什么能把气体留在表面？材料表面附近的分子会不断到来、停留，也会离开；在一定温度和压力下，最终能够留住多少，关系到吸附剂的用量、表面性质和工作条件。实验通常先给出一张表：每次设定一个压力，记录相应的吸附量。接下来才是分析问题：体积随压力怎样变化，哪一种曲线能描述这些观测，曲线上的参数又能帮助我们判断什么？本章把这些步骤连起来，完成一个包含原始表格、参数估计、残差、区间和范围比较的分析项目。

我们使用NIST统计参考数据集Misra1a中的14个真实观测值。这组数据来自1978年的牙科单分子层吸附研究，自变量是压力，响应变量是体积。原记录列出了数值，但没有给出压力和体积对应的具体物理单位，因此图中统一沿用“原记录压力单位”和“原记录体积单位”。这样做仍然能够重现曲线拟合和比较参数；将结果换算成帕或毫升，需要先取得实验记录中的单位定义。一次完整分析从这类看似不起眼的信息开始，因为单位决定了参数怎样与其他实验相比较。

这里会用到pandas整理表格、NumPy表达数组运算、SciPy估计参数和不确定性、Matplotlib呈现结果。它们各自处理同一条证据链的一段：表中的一行变成一个点，所有点共同确定一条曲线，每个点到曲线的差又变成残差。你可以沿着这条链检查任何一个数字，而不必一次记住所有函数。已有的[表格读取](https://ml-biomat.com/tutorials/python-scientific/p11/)和[拟合与残差](https://ml-biomat.com/tutorials/python-scientific/p19/)知识会在具体任务里重新出现。

## 先看清一行数据究竟记录了什么

下载材料中的`Misra1a.dat`是一个普通文本文件，前半段介绍变量、模型和参考结果，后半段才是数字表。它的第一列是体积，第二列是压力；如果直接凭习惯把第一列当作横坐标，程序仍可能画出一条平滑曲线，但研究问题已经被悄悄调换了。代码先找到明确的数字表标题，再以空白字符为分隔符读取，并赋予`volume`和`pressure`这两个列名。列名在这里承担科学含义，让后面的计算不依赖“第零列大概是什么”的记忆。

第一行的含义是：压力为77.6时，记录的体积为10.07；最后一行则是压力760.0对应体积81.78。14行代表14个压力条件下的观测，不是14次相同条件的重复实验。我们检查行数是否为14、数值是否有限且为正、压力是否有重复，再按压力排序。排序让折线沿着压力逐渐增加的方向连接，也让“取前六个观测”具有明确意义：取低压力端的六个点，而非文件里恰巧排在前面的任意六条记录。

数值检查通过以后，还应读一遍散点图。压力大约增加到原来的9.8倍，体积增加到约8.1倍，说明增长已开始变缓；不过最高压力处的曲线仍然明显向上。日常可以把它想成一个逐渐坐满的座位区：最初有很多空位，新增来客容易找到位置，后来空位变少，新增人数的增幅下降。这个比喻帮助理解有限容量，但实际吸附还涉及分子与表面的相互作用、温度以及吸附和脱附的动态平衡。哪些细节可以简化，需要由接下来选用的模型说明。

![真实压力—体积观测、指数拟合与近似均值区间；共享压力轴的残差图显示细小而有结构的偏离。](https://ml-biomat.com/static/tutorials/python-scientific/figures/743925b2e797bb2e0aabf621.svg?v=743925b2e797)

图 1真实压力—体积观测、指数拟合与近似均值区间；共享压力轴的残差图显示细小而有结构的偏离。

图的上半部分把数据和拟合曲线放在一起，下半部分沿用相同压力轴，把细小差别放大成残差。上图中许多差别小于圆点直径，看起来几乎完全贴合；下图却能看出低压力端多为正、中间多为负、最高压力端重新为正。上下两幅图回答不同的问题：一幅说明总体变化，另一幅检查这种变化是否被所选函数系统地偏离。

## 从表面位点到函数：两种“逐渐饱和”并不相同

Langmuir在1918年讨论气体在玻璃、云母和铂表面的吸附时，把表面上的有限位置与分子层联系起来。今天最常见的简化模型把这些位置看成等价位点，每个位点最多容纳一个分子，并令吸附和脱附在稳态时达到平衡。若已占位点比例为θ，空位比例就是1−θ；气体越多、空位越多，吸附就越容易发生，而脱附对应已经占据的位点。在温度固定、位点近似等价且忽略邻近吸附分子相互影响的条件下，这种平衡得到下面的关系。

$$
\theta=\frac{KP}{1+KP},\qquad V=A\theta=\frac{AKP}{1+KP}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | 已占据位点比例，0到1，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 压力，原记录压力单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Langmuir平衡参数，原记录压力单位的倒数 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 该模型的饱和体积，原记录体积单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 模型预测的吸附体积，原记录体积单位 |

吸附速率与压力及空位比例的乘积成正比，脱附速率与已占比例成正比。平衡时令两者相等，把吸附与脱附比例系数之比写成K，整理得到θ。乘以全部位点占据时的体积A，就得到V。教学算例取A=100体积单位、K=0.002压力单位⁻¹、P=500压力单位，KP=1，θ=1/2，V=50体积单位。温度固定、位点等价且一位点至多一分子是该简化的条件。

这条曲线具有清楚的两个尺度：A决定最终的平台高度，K决定压力增加时接近平台的快慢。让KP等于1，就得到一半容量；因此1/K是模型中的半饱和压力。下面的位点图画了九个位点和五个被占据的位置，只用于解释比例与空位，它没有把14个实验数据换成九个微观观测。由表面构想走到宏观函数时，应该保留两者的尺度区别：位点是微观图景，曲线是大量分子共同产生的体积响应。

![有限表面位点的示意与两种函数的实际拟合。灰色区域是观测压力覆盖；区域之外显示数学外推。](https://ml-biomat.com/static/tutorials/python-scientific/figures/bac3340ca971b2b5b2c65c82.svg?v=bac3340ca971)

图 2有限表面位点的示意与两种函数的实际拟合。灰色区域是观测压力覆盖；区域之外显示数学外推。

NIST为Misra1a指定的数值参考模型采用另一种函数：指数型的饱和曲线。它也从零开始，逐渐接近一个平台，但中间弯曲的方式与Langmuir曲线不同。参考值的用途是让我们核对“同一个数学问题是否被正确求解”。选择哪个数学问题来描述材料，还要检查残差和模型对应的物理条件。因此程序先重现指定的指数模型，再把Langmuir模型放到同一批观测上比较。

$$
\widehat V(P)=A\left(1-e^{-kP}\right)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8a576b30f1fc1047cbfe6275.svg) | 在压力P处预测的平均体积，原记录体积单位；帽号表示预测 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 指数模型的渐近容量，原记录体积单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 指数模型的压力尺度参数，原记录压力单位的倒数 |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 压力，原记录压力单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 自然指数函数的底数，约2.71828，无量纲 |

kP无量纲，因此可以作为指数。P为0时括号为0；压力逐渐增大时指数项趋近0，预测趋近A。这给出从零接近平台的一种函数形状。教学算例A=100体积单位、k=0.002压力单位⁻¹、P=500压力单位时，kP=1，预测100×(1−e⁻¹)≈63.2121体积单位。它与相同示例参数下Langmuir函数的50不同。

这里的k乘的是压力，所以k具有压力单位的倒数。把同样的指数外形用于时间变化时，系数才可能具有每秒的单位；函数看起来相似，并不会自动让两个参数具有相同的物理意义。代码用`-np.expm1(-k * pressure)`计算一减指数的部分，`expm1`专门计算指数减一，在乘积很小时能减少两个接近的数相减造成的精度损失。这个细节把数学表达式和计算机实际执行的算术接了起来。

## 让全部观测共同决定参数

试着手工移动一条曲线，会发现提高A可以让预测整体变高，而降低k又可以把较低压力处的预测拉下来。因此两个参数能互相补偿，凭眼睛选择并不容易。最小二乘法为这种选择规定一个明确的目标：在每一个实测压力处计算预测体积，把实测减去预测得到残差，再把所有残差的平方相加。平方既避免正负差互相抵消，也让较大的偏离获得更大的代价。

$$
r_i=V_i-\widehat V(P_i),\qquad \mathrm{RSS}=\sum_{i=1}^{n}r_i^2,\qquad s=\sqrt{\frac{\mathrm{RSS}}{n-2}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | 观测编号与观测个数，无量纲计数；本例n=14 |
| ![Formula](https://ml-biomat.com/static/agent-math/538402917df2dc5b1bae4c8e.svg) | 第i次观测的压力与体积，分别沿用原记录压力单位和体积单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/1bb2f4fa5d74eb43925bfa72.svg) | 同一压力处的预测体积，原记录体积单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 实测减预测的残差，原记录体积单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/b50b0236980ee4169c09fda4.svg) | 全部残差的平方和，原记录体积单位的平方 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 拟合残差标准差，原记录体积单位；分母扣除两个估计参数 |
| ![Formula](https://ml-biomat.com/static/agent-math/df10424aca79108f20c06f2f.svg) | 从第1个到第n个观测逐项相加的求和记号；每项均为残差平方 |

平方使正负偏离不会抵消。首个点的残差10.07−9.98626636≈0.08373364体积单位，对RSS的贡献约为0.00701132体积单位²。14项加和为0.12455138894；除以14−2=12再开平方，得到s≈0.10187876体积单位。相同权重对应体积误差采用相近尺度，压力在拟合中视作给定。

本例没有逐点测量标准差，采用相同权重；这对应把体积方向的误差看成相近尺度，并在拟合中把压力当作给定值。若自己的压力测量误差也很明显，就需要把两条轴的测量过程一起建模；若不同观测有可靠的标准差，则可通过`sigma`指定权重。权重应该来自测量含义，而不是为了把某几个不合意的点压下去。本例的残差标准差由RSS除以12再开平方得到，12来自14个观测减去两个估计参数。

`curve_fit`需要接收“给定压力和参数时计算体积”的函数、压力数组、体积数组以及初始参数。我们取A=250、k=0.0005作为初值，要求两个参数为正，并用`x_scale`告诉求解器两类参数的典型数量级。A约为几百，k约为万分之几，直接按相同数值步长移动两者会产生很不均衡的影响。尺度设置使搜索更符合参数的实际幅度，改变的是寻找解的方式，目标函数仍然是原来的残差平方和。

代码还提供了Jacobian，即每个预测值对每个参数的小幅变化有多敏感。你可以把它理解为求解器旁边的一张方向表：A增加一点会怎样，k增加一点又会怎样。指数模型对A的导数是一减指数，对k的导数则是A乘压力再乘指数；这正对应代码中的两列。无需先掌握整套优化理论也能使用程序，但知道这两列来自模型的变化规律，有助于检查参数单位、符号以及数组形状。

## 运行完整项目，并追踪一个数值的来路

把示例目录中的`main.py`与`data/Misra1a.dat`保持相对位置，运行下面的命令，就会生成结果表、数值摘要和三组图。输出目录由`--output`选择，语言由`--language`选择。程序读取一次原始观测，对两种模型分别使用6到14个点拟合，共得到18组状态；最后将同一批状态写入交互数据。这样，页面中的参数比较和下载后的运行使用同一组定义。

### 运行项目

将en换为zh生成中文图。

```
python main.py --output results --language en
```

### 完整吸附分析：数据、两种拟合、区间与图

读取随例提供的14个观测，复现数值参考并计算18组范围比较。

```
"""Analyze the observed NIST Misra1a adsorption data and fitting range."""
from pathlib import Path
from io import StringIO
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def exponential(pressure, capacity, scale):
    return -capacity * np.expm1(-scale * pressure)


def langmuir(pressure, capacity, scale):
    return capacity * scale * pressure / (1 + scale * pressure)


def jacobian(pressure, capacity, scale, model):
    if model == 'exponential':
        return np.column_stack((-np.expm1(-scale * pressure),
                                capacity * pressure * np.exp(-scale * pressure)))
    denominator = 1 + scale * pressure
    return np.column_stack((scale * pressure / denominator,
                            capacity * pressure / denominator**2))


def load_data(path):
    raw = path.read_bytes()
    text = raw.decode('ascii')
    # The first Data heading describes variables; the second starts the numbers.
    numeric = text.split('Data:   y               x', 1)[1]
    frame = pd.read_csv(StringIO(numeric), sep=r'\s+', names=['volume', 'pressure'])
    if len(frame) != 14 or not np.isfinite(frame.to_numpy()).all():
        raise ValueError('Expected 14 finite observations')
    if frame.pressure.duplicated().any() or (frame <= 0).any().any():
        raise ValueError('Expected positive values and unique pressures')
    return frame.sort_values('pressure').reset_index(drop=True), hashlib.sha256(raw).hexdigest()


def fit(frame, count, model, grid):
    pressure = frame.pressure.to_numpy(dtype=float)
    volume = frame.volume.to_numpy(dtype=float)
    function = exponential if model == 'exponential' else langmuir
    parameters, covariance = curve_fit(
        function, pressure[:count], volume[:count], p0=[250, .0005],
        jac=lambda x, a, k: jacobian(x, a, k, model), bounds=(0, np.inf),
        x_scale=[250, .0005], ftol=1e-13, xtol=1e-13, gtol=1e-13,
        max_nfev=10000)
    residuals = volume - function(pressure, *parameters)
    rss = float(residuals[:count] @ residuals[:count])
    gradient = jacobian(grid, *parameters, model)
    variance = np.einsum('ij,jk,ik->i', gradient, covariance, gradient)
    half_width = t.ppf(.975, count - 2) * np.sqrt(np.maximum(0, variance))
    standard_error = np.sqrt(np.diag(covariance))
    return {'model': model, 'count': count, 'max_pressure': float(pressure[count-1]),
            'capacity': float(parameters[0]), 'scale': float(parameters[1]),
            'standard_errors': standard_error.tolist(),
            'correlation': float(covariance[0, 1] / np.prod(standard_error)),
            'rss': rss, 'residual_sd': float(np.sqrt(rss / (count-2))),
            'residuals': residuals.tolist(), 'prediction': function(grid, *parameters).tolist(),
            'mean_ci_half_width': half_width.tolist()}


def figures(frame, states, grid, output, language):
    zh = language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': available_plot_fonts(),
                         'font.size': 13, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'axes.unicode_minus': False})
    blue, orange, green = '#205b8c', '#bd5535', '#2b7c73'
    p, v = frame.pressure.to_numpy(), frame.volume.to_numpy()
    full = next(s for s in states if s['count'] == 14 and s['model'] == 'exponential')
    other = next(s for s in states if s['count'] == 14 and s['model'] == 'langmuir')
    xlabel = tr('压力 / 原记录压力单位', 'Pressure / recorded pressure unit')
    ylabel = tr('体积 / 原记录体积单位', 'Volume / recorded volume unit')

    def save(fig, name):
        for suffix in ['svg', 'png']:
            fig.savefig(output / f'{name}-{language}.{suffix}', dpi=160,
                        facecolor='#faf9f5', bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                             gridspec_kw={'height_ratios': [2.2, 1]}, layout='constrained')
    selected = grid <= 800
    prediction, half = np.array(full['prediction']), np.array(full['mean_ci_half_width'])
    axes[0].fill_between(grid[selected], (prediction-half)[selected],
                         (prediction+half)[selected], color=blue, alpha=.2,
                         label=tr('均值曲线的近似95%区间', 'Approximate 95% interval for the mean curve'))
    axes[0].plot(grid[selected], prediction[selected], color=blue, lw=2.5,
                 label=tr('指数模型拟合', 'Exponential model fit'))
    axes[0].scatter(p, v, s=56, facecolor='#faf9f5', edgecolor=orange,
                    linewidth=2, zorder=3, label=tr('14个观测值', '14 observed values'))
    axes[0].set(ylabel=ylabel, title=tr('观测与曲线：体积增加逐渐放缓',
                                      'Observations and curve: volume increases more slowly'))
    axes[0].legend(loc='upper left', fontsize=12)
    axes[1].axhline(0, color='#667782', lw=1)
    axes[1].stem(p, full['residuals'], linefmt=blue, markerfmt='o', basefmt=' ')
    axes[1].set(xlabel=xlabel, ylabel=tr('残差 / 体积单位', 'Residual / volume unit'),
                title=f"RSS = {full['rss']:.8f};  " + tr('自由度 = 12', 'degrees of freedom = 12'))
    save(fig, 'fit-and-residuals')

    fig = plt.figure(figsize=(13, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1])
    ax = fig.add_subplot(gs[:, 0]); top = fig.add_subplot(gs[0, 1]); bottom = fig.add_subplot(gs[1, 1])
    capacities = np.linspace(210, 270, 180)
    scales = np.linspace(.000475, .00064, 180)
    aa, kk = np.meshgrid(capacities, scales)
    rss = np.sum((v[:, None, None] - exponential(p[:, None, None], aa, kk))**2, axis=0)
    filled = ax.contourf(aa, kk*1000, np.log10(rss/full['rss']),
                         levels=np.linspace(0, 4, 17), cmap='cividis', extend='max')
    ax.plot(full['capacity'], full['scale']*1000, '*', color=orange, ms=16)
    ax.set(xlabel=tr('容量参数 A / 体积单位', 'Capacity parameter A / volume unit'),
           ylabel=tr('尺度参数 k / 10⁻³ 压力单位⁻¹', 'Scale parameter k / 10⁻³ pressure unit⁻¹'),
           title=tr('同一批数据形成狭长的参数谷', 'A narrow parameter valley for the same data'))
    fig.colorbar(filled, ax=ax, label='log₁₀(RSS / RSSmin)', shrink=.7)
    subset = [s for s in states if s['model'] == 'exponential']
    for axis, key, index, factor, label in [(top, 'capacity', 0, 1, 'A'),
                                            (bottom, 'scale', 1, 1000, 'k × 1000')]:
        axis.errorbar([s['max_pressure'] for s in subset],
                       [s[key]*factor for s in subset],
                       yerr=[s['standard_errors'][index]*factor for s in subset],
                       color=blue, marker='o', capsize=3)
        axis.axhline(full[key]*factor, color=orange, ls='--')
        axis.set(ylabel=(tr('A / 体积单位','A / volume unit') if key=='capacity'
                         else tr('k / 10⁻³ 压力单位⁻¹','k / 10⁻³ pressure unit⁻¹')))
    top.set_title(tr('逐步纳入高压力观测\n误差棒为1 SE',
                     'Include higher-pressure observations\nBars show 1 SE'), fontsize=13)
    bottom.set_xlabel(tr('拟合范围的最大压力 / 原单位',
                         'Maximum fitted pressure / recorded unit'))
    save(fig, 'parameter-coverage')

    fig = plt.figure(figsize=(13, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[.85, 1.35], width_ratios=[1, 1])
    surface = fig.add_subplot(gs[0, 0]); explanation = fig.add_subplot(gs[0, 1])
    curve = fig.add_subplot(gs[1, :])
    for axis in [surface, explanation]:
        axis.set(xlim=(0, 10), ylim=(0, 4)); axis.axis('off')
    surface.add_patch(Rectangle((.4, .5), 9, .65, facecolor='#ccd5d8'))
    occupied = {0, 2, 3, 6, 8}
    for i in range(9):
        surface.add_patch(Rectangle((.6+i, 1.15), .65, .12, color=blue))
        if i in occupied:
            surface.add_patch(Circle((.925+i, 1.65), .32, facecolor=orange))
    surface.annotate('', xy=(1.925, 1.5), xytext=(1.925, 3.3),
                     arrowprops={'arrowstyle': '->', 'lw': 2, 'color': blue})
    surface.annotate('', xy=(6.925, 3.3), xytext=(6.925, 2.1),
                     arrowprops={'arrowstyle': '->', 'lw': 2, 'color': orange})
    surface.text(.4, 3.75, tr('有限位点：空位吸附，已占位点脱附',
                             'Finite sites: adsorption and desorption'), fontsize=14)
    surface.text(.4, .05, tr('位点占据示意：5个占据，4个空位',
                            'Site occupancy: five occupied, four vacant'), fontsize=12)
    explanation.text(.2, 3.5, 'Langmuir, 1918', fontsize=19, weight='bold')
    explanation.text(.2, 2.55, tr('单层、等价位点、动态平衡',
                                 'Monolayer, equivalent sites, dynamic balance'), fontsize=14)
    explanation.text(.2, 1.55, r'$V=A K P/(1+K P)$', fontsize=21, color=green)
    explanation.text(.2, .3, tr('指数曲线采用另一种函数形状；分别检验',
                               'The exponential curve has a different shape'), fontsize=13)
    curve.axvspan(0, p.max(), color='#d8e2e7', alpha=.7,
                   label=tr('观测覆盖范围', 'Observed pressure coverage'))
    curve.plot(grid, full['prediction'], color=blue, lw=2.5,
                label=tr('指数模型', 'Exponential') + f"; RSS={full['rss']:.3f}")
    curve.plot(grid, other['prediction'], color=green, lw=2.5, ls='--',
                label=f"Langmuir; RSS={other['rss']:.3f}")
    curve.scatter(p, v, color=orange, s=25, zorder=3)
    curve.set(xlabel=xlabel, ylabel=ylabel, xlim=(0, grid.max()),
                title=tr('越过观测区间，模型形状的差别逐渐放大',
                         'Model shapes diverge beyond the observations'))
    curve.legend(loc='lower right', fontsize=12)
    save(fig, 'surface-and-extrapolation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    frame, checksum = load_data(Path(__file__).resolve().parent / 'data' / 'Misra1a.dat')
    grid = np.linspace(0, 4000, 401)
    states = [fit(frame, count, model, grid) for model in ['exponential', 'langmuir']
              for count in range(6, 15)]
    full = next(s for s in states if s['model'] == 'exponential' and s['count'] == 14)
    assert np.allclose([full['capacity'], full['scale']],
                       [238.94212918, .00055015643181], rtol=2e-8, atol=0)
    assert abs(full['rss'] - .12455138894) < 1e-10
    frame['fitted_volume'] = exponential(frame.pressure.to_numpy(), full['capacity'], full['scale'])
    frame['residual'] = frame.volume - frame.fitted_volume
    frame.to_csv(args.output / 'observations-and-fit.csv', index=False)
    data = {'pressure': frame.pressure.tolist(), 'volume': frame.volume.tolist(),
            'grid': grid.tolist(), 'states': states}
    (args.output / 'lab-data.json').write_text(json.dumps(data), encoding='utf8')
    summary = {'observations': len(frame), 'data_sha256': checksum,
               'units': {'pressure': 'recorded pressure unit, SI identity unspecified',
                         'volume': 'recorded volume unit, SI identity unspecified'},
               'exponential': {k: v for k, v in full.items()
                               if k not in ['prediction', 'mean_ci_half_width', 'residuals']},
               'langmuir_rss': states[-1]['rss'],
               'first_residual': float(frame.residual.iloc[0]),
               'observed_fraction_of_capacity': float(frame.volume.max()/full['capacity']),
               'states': len(states)}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    figures(frame, states, grid, args.output, args.language)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

阅读程序时，可以先顺着`main`看数据如何流动，再回到各个函数。`load_data`返回有列名的表和文件校验值；`fit`接收所用点数和模型名称，返回参数、残差、区间与预测；`figures`只把已经算好的量组织成图。最后生成的`observations-and-fit.csv`保留原有压力、体积，再添加拟合体积和残差。原观测与派生结果在同一行相邻，方便逐行检查，也保留了重新采用其他模型的起点。

例如第一行的预测体积约为9.986266，观测为10.07，残差就是0.083734。把14个残差分别平方再相加，得到0.12455138894，与NIST对指数模型的参考值一致；A约为238.942129，k约为0.0005501564。程序把这些比较写成断言，重新运行时会自动检查。这里校验的是文件读取、模型定义和数值求解能否连成同一个问题，尤其能发现把两列读反、漏掉负号或使用错误模型函数的情况。

## 好看的曲线之后，还要读残差与参数关系

指数模型的参数标准误差分别约为2.7070和0.0000072669。它们描述在当前模型及误差假设下，参数估计对观测扰动的敏感程度。程序根据拟合点附近的线性近似计算协方差，再把它传播到各个压力处的预测值，乘以相应自由度的t分布系数，得到图中的近似95%均值曲线区间。这个区间回答的是“平均响应曲线的位置有多不确定”；如果要预测下一次单独测量的体积，还要加入该次测量本身的随机变化，因此预测区间通常更宽。

两项标准误差不能分别讲完整个故事。本例两个参数的相关系数约为−0.9988：沿着一条狭长的组合方向，A变大、k变小，曲线仍能贴近现有观测。下图把一片参数平面上的RSS逐点算出来，颜色较深处表示较小残差。横轴是A，纵轴是k，每个位置是一整条候选曲线，而不是一个实验点。狭长的深色谷正好解释了参数为何紧密相关，也说明报告参数时最好同时保留协方差或共同的拟合记录。

![左侧逐点计算参数平面的RSS；右侧每次增加一个较高压力观测后重新拟合，误差棒为参数的一个标准误差。](https://ml-biomat.com/static/tutorials/python-scientific/figures/d79c364ad992fb88144362dd.svg?v=d79c364ad992)

图 3左侧逐点计算参数平面的RSS；右侧每次增加一个较高压力观测后重新拟合，误差棒为参数的一个标准误差。

残差图还提出了一个与求解精度不同的问题。指数模型的残差有连续成组的正负变化；对同一14个点拟合Langmuir模型，RSS约为0.0564193，比指数模型的0.1245514更小。两者都有两个参数，在当前相同权重和数据范围下，Langmuir形状更贴近这些体积观测。进一步判断其位点图景，需要结合温度、平衡条件和材料表面信息；拟合记录提供的直接证据，是具体模型在这些观测上的偏离有多大、偏离怎样随压力变化。

这种分工也解释了为什么“重现参考参数”和“寻找合适材料模型”可以同时成立。前者使用固定问题核对计算，后者比较问题的设定是否抓住实验变化。科学分析需要两种能力：把给定问题算对，并且愿意根据残差重新审视原先选用的函数。一个收敛提示只能说明求解器停止了，逐点残差和数据覆盖范围才让我们读懂它找到的曲线。

## 逐步扩大压力范围，观察容量估计怎样变化

把前六个低压力观测单独拟合，再逐步加入更高压力点，是一种直观的数据覆盖实验。它保持观测本身不变，只改变哪些点参与确定参数。左侧曲线始终显示全部14个点，参与拟合的点着色，未参与的点保留为灰色；右侧残差则让你看到模型如何预测这些稍后才加入的观测。改变显示范围到4000，还能比较观测区间以外两种函数逐渐分开的形状。

### 看见数据覆盖怎样约束曲线

[Figure: 曲线、均值区间及已用和未用观测](https://ml-biomat.com/tutorials/python-scientific/p29/#P29-curve)

[Figure: 全部14点的残差](https://ml-biomat.com/tutorials/python-scientific/p29/#P29-residual)

[Figure: 容量随拟合覆盖范围变化](https://ml-biomat.com/tutorials/python-scientific/p29/#P29-path)

橙点参与拟合；灰点保留作范围比较。纵轴体积与横轴压力均沿用原记录单位。

先选指数模型和六个点，观察A的估计；再增加到十四个点，同时看参数轨迹和灰色残差的变化。低压力曲线接近直线，主要确定的是初始斜率，即A与k的乘积。较高压力点引入更多弯曲信息，才帮助区分“较高容量但增长较慢”和“较低容量但增长较快”。这与用一小段山路推测整座山的形状相似：局部坡度容易比较，远处的平台高度需要更长的路线才能约束。

即使使用全部观测，最大的体积81.78也只约为指数模型容量参数的34.2%，观测尚处于明显增长的区间。下一轮实验若围绕容量设计，可以在材料和设备允许的条件下增加高压力覆盖，检查是否逐渐出现平台，并在关键压力处安排重复测量以估计体积误差。页面里的4000只是计算函数的延伸横坐标，实验计划中的压力上限应由材料稳定性、装置范围和研究目标共同确定。交互的价值在于看清还缺少哪一段曲线信息，再决定需要补哪一类测量。

18组状态由下载示例中的SciPy实际拟合得到，页面按当前点数和模型读取相应结果。每次调整都同步更新曲线、残差、参数轨迹和所用数据范围，右侧灰点始终对应已有但未纳入拟合的观测。这里按压力扩展数据覆盖，并没有随机划分训练集与测试集；读者观察的是参数和外推对覆盖范围的敏感性，可以把具体状态记录下来后在Python中逐项复现。

## 把项目整理成别人能够接着使用的结果

一份可用的材料分析结果，应当让人同时找到研究对象、数据范围、数学定义和关键数值。本例可以这样概括：对Misra1a的14个压力—体积观测采用等权最小二乘，指定指数模型得到A=238.9421、k=0.0005501564，RSS=0.12455139；在同一观测范围内，Langmuir模型RSS=0.05641930。参数沿用原记录单位，最大观测体积约为指数模型容量的34.2%。这几句话把对象、计算与含义放在一起，读者也能据此找到对应表格和图。

保存时，原始数据保留原样，结果表保存逐点预测与残差，摘要保存参数及其定义，图保留坐标、单位和区间含义。以后增加新的压力条件，可以追加新的原始记录并重新运行，而不是手动把曲线拖到新点附近。若新的测量提供逐点标准差，就把它接入加权拟合；若温度变化成为主要研究变量，就在表格中增加温度列，按等温条件组织数据，再比较温度怎样影响参数。每一步扩展都能落到一个清楚的数据字段或模型条件上。

这个项目把Python课程里的多个工具放进了一次真实研究分析：pandas让观测含义保持清楚，NumPy把函数落实为数组计算，SciPy寻找参数并描述局部不确定性，Matplotlib把整体趋势与细小偏离同时呈现。最值得保留的习惯，是从一个可解释的观测出发，逐步连接模型、数值和下一轮测量。读者因此能够接着分析，而不只是得到一张漂亮的拟合图。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P29.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NIST StRD: Misra1a](https://www.itl.nist.gov/div898/strd/nls/data/misra1a.shtml)

   14个真实吸附观测及指定指数模型的认证数值。

   NIST Standard Reference Database 140; free SRD with NIST SRD terms and source attribution.
2. [NIST SRD copyright and licensing](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)

   标准参考数据的版权与使用条款。

   NIST official SRD terms; SRD is a distinct category under 15 USC 290e.
3. [SciPy curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   参数尺度、Jacobian、协方差与非线性拟合的官方用法。

   SciPy BSD-3-Clause; original chapter implementation.
4. [Langmuir (1918), The Adsorption of Gases on Plane Surfaces of Glass, Mica and Platinum](https://pubs.acs.org/jacsat/article/40/9/1361/430014/THE-ADSORPTION-OF-GASES-ON-PLANE-SURFACES-OF-GLASS)

   表面位点与单层吸附的历史背景。

   Scientific historical citation; original explanatory diagram.
5. [NIST StRD background](https://www.nist.gov/itl/sed/statistical-reference-datasets/strd-background-information)

   参考数据用于检查统计计算准确性的目的。

   Official NIST information.
