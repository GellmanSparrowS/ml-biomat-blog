# 从散点到模型：拟合与残差

Source: https://ml-biomat.com/tutorials/python-scientific/p19/
Language: zh-CN

从一段应力松弛曲线出发，理解参数、残差和观测时间怎样共同决定拟合结果。

## 从一块被拉住的软材料开始

把一条软橡胶稍微拉长，再保持这个长度，手上感到的拉力常会逐渐减小。材料仍然处于拉伸状态，内部不同部分却在重新调整。实验可以记录维持这个长度所需的力，并除以约定的截面积，得到应力随时间的变化。研究者常想从这条下降曲线读出两个问题：应力下降得有多快，长时间以后还留下多少。拟合把这些问题写成有单位的参数，使不同样品的变化可以比较。本篇将用一组明确构造的教学数据，完成建模、SciPy拟合、残差检查和观测时间分析。

先区分三种对象。观测值是每个时刻记录下来的数字，在图中用点表示；模型是给定时间后能够计算应力的函数，在图中用连续曲线表示；参数决定同一个函数具体长成什么样。例如，两条曲线都可以从高处逐渐接近平台，却分别在几秒与几十秒内完成主要下降。参数把这种差别写成数字。函数接受时间作为输入，返回模型预期的应力；拟合则反过来利用观测记录，寻找使函数与这些记录接近的参数。

这次的时间从0到12 s，每隔0.5 s取一个点，共25条记录。理想曲线从2.8 kPa下降，逐渐接近0.4 kPa的平台，主要时间尺度设为3 s；随后逐点加入一组公开写在代码中的小扰动。kPa是千帕，是应力和压强常用的单位。所有数字都由这些规则确定，读者可以追踪每一条记录。先知道生成规则，再把参数当作未知量重新求出，有助于分开“算法是否正确求解”与“观测能否区分参数”这两个问题。

拟合有点像根据路上的几个路标重画一条路线：路标的位置是数据，允许使用的路线形状是模型，调整路线的几个旋钮就是参数。路标之间怎样连接，取决于路线的结构；把每个路标都精确穿过，未必能保留原本想研究的变化规律。因此，本篇始终把曲线和它留下的偏差一起阅读。准备工作只需要理解数组保存一组数字、函数执行同一种计算，以及横纵坐标的含义；指数函数和最小二乘将在实际问题中逐步解释。

## 让参数分别回答高度、速度和平台

一种简单的松弛模型把应力分成“会衰减的部分”和“保持的平台”。会衰减的部分起初较大，随后按指数规律减少。指数规律可以理解为：每经过同样长的一段时间，剩下的可衰减部分都乘上同一个比例，而不是减去同样多的应力。银行复利也是反复乘比例，只是这里的比例小于1，数量随时间减少。这样得到的曲线开始下降较快，后来逐渐变平，适合描述一个主要时间尺度支配的松弛过程。

$$
s(t)=A\exp(-t/\tau)+b
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | 时刻t的模型应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 保持变形后的时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 初始应力超出长期平台的部分，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | 正的松弛时间，s；希腊字母tau |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | 长期平台应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | 以自然常数e为底的指数函数；输入和输出均无量纲 |

t与τ具有相同单位，所以t/τ无量纲。取A=2.4 kPa、τ=3 s、b=0.4 kPa：t=0时exp(0)=1，应力为2.8 kPa；t=3 s时exp(−1)≈0.367879，应力为2.4×0.367879+0.4≈1.28291 kPa。指数项随时间下降，b保持不变；单一τ对应一个主要松弛时间尺度。

A与b都是应力，所以能相加；时间t除以时间尺度τ，单位相互消去，指数函数接收到的是一个纯数字。这个单位检查很有用：若t用秒、τ却直接填入以分钟表示的数值，程序仍能算出曲线，但曲线对应的时间尺度已经改变。τ越大，同一个t所对应的t/τ越小，指数项下降得越慢。t等于τ时，可衰减的部分还剩最初的约36.8%；这里比较的是超出平台的部分，平台本身不参加这次比例变化。

![指数松弛模型中的三个参数各有可观察的作用：A决定超出平台的初始高度，τ决定下降的时间尺度，b决定长期平台。曲线由A=2.4 kPa、τ=3 s、b=0.4 kPa计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/e6fe6874cd69b7756c11742d.svg?v=e6fe6874cd69)

图 1指数松弛模型中的三个参数各有可观察的作用：A决定超出平台的初始高度，τ决定下降的时间尺度，b决定长期平台。曲线由A=2.4 kPa、τ=3 s、b=0.4 kPa计算。

图中的初始应力是A+b，因此直接把第一个观测值当成A，会把平台也算入振幅。类似地，在12 s看到的应力虽然已接近平台，仍含有少量尚未衰减的部分；把最后一个点直接当成b，会把这个剩余量和该点的扰动一起带进去。初始点和末端点适合提供参数的起始估计，完整拟合则会利用全部记录调整它们。在本例中，A=2.4 kPa、b=0.4 kPa共同给出2.8 kPa的初始模型值，二者各自承担明确含义。

模型与实验条件也连在一起。这里把温度、外部变形和材料状态视为观测期间保持稳定，并用一个τ描述主要变化。若材料有两个相隔很远的松弛过程，曲线可能先快后慢，需要进一步描述两个过程；若温度持续改变，拟合出来的τ会混入温度变化的影响。判断这些情况要看记录的实验条件与残差形状。参数有物理名称以后，选模型、设计观测时间和解释拟合数字才有共同的依据。

## 用残差把“贴近数据”变成可计算的要求

给定一套参数，就能在每个观测时刻算出一个模型值。用观测减去模型得到残差：正值表示观测点位于曲线上方，负值表示位于下方。保留正负很重要，因为连续一段时间的正残差会提示曲线在那一段系统地偏低。为了比较两套参数，还需要把25个残差合成一个目标量。最小二乘采用残差平方和，使正负偏差不会互相抵消，并让较大的偏离付出更大的代价。

$$
r_i=y_i-s(t_i),\qquad Q=\sum_{i=1}^{n}r_i^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 记录序号，从1到n；无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 参与拟合的记录数；无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | 第i次记录的时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i次记录的观测应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/ff229aed753b3375e39a6524.svg) | 模型在同一时间的应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 观测减模型所得的残差，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 所有残差平方之和，也写SSE，kPa² |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 按序号把后面的各项相加 |

残差为正表示该点在曲线上方。若三个残差为0.03、−0.02、0.01 kPa，它们的代数和为0.02 kPa，而平方和为0.0009+0.0004+0.0001=0.0014 kPa²。平方避免正负抵消，并使较大偏离获得更高代价。相同单位、相近误差尺度的记录可采用这里的等权和；比较两个模型时须使用同一批记录。

平方和中的“最小”描述的是一项明确任务：在选定模型和允许参数范围内，寻找平方和较小的参数组合。它并没有要求曲线穿过每个点。若每个观测都带有小扰动，一条概括共同趋势的曲线通常会从点群中间穿过。把参数调得过于灵活，甚至为每个点单独安排一个参数，确实可能让平方和继续变小，但参数就失去了对共同过程的概括。这里三个参数共同解释25个观测，残差继续保留未被模型解释的部分。

等权平方和还表达了一个选择：相同大小的应力偏差具有相同代价。它适合各记录误差尺度接近的情况。若某些记录来自精度较高的测量，另一些记录的标准差较大，可以先将残差除以各自的误差标准差，再平方相加。这样，一次偏离相当于多少个“常见误差大小”就成为比较依据。标准差描述测量误差的典型尺度，与纵坐标读数本身不同；把读数直接当作标准差会给数据引入另一套未经说明的权重。

$$
Q_w=\sum_{i=1}^{n}\left(\frac{r_i}{\sigma_i}\right)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/387edda104c523c662ff5727.svg) | 按测量标准差加权的残差平方和，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | 记录序号及记录总数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | 第i条记录的残差，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/1d11eec53e2e8f271603794c.svg) | 第i条观测误差的已知或外部估计标准差，kPa |

0.04 kPa的残差对应0.02 kPa标准差时，比值为2，对Qw贡献4；相同残差对应0.08 kPa标准差时，比值为0.5，贡献0.25。这样比较的是偏离相对于该记录测量精度的大小。此式按各记录误差不相关组织；有相关误差时需要完整协方差矩阵。本篇明确给定的扰动用于教学，没有另行指定仪器标准差，所以实跑采用等权拟合。

本篇采用等权拟合，因为教学扰动是逐项给定的数组，没有另行设定仪器的标准差。对真实实验，可以通过校准或重复测量获得误差尺度，再考虑权重。如果时间相邻的误差有关联，例如仪器缓慢漂移，同样方向的几个残差就携带重复信息；此时完整的误差协方差能够描述这种关联。先画按时间排列的残差，往往比立即增加优化选项更有帮助，因为它会把漂移、遗漏的平台和孤立异常点表现为不同的结构。

## 把模型交给SciPy，也保留对计算的理解

科学计算软件的一项重要变化，是把成熟的数值方法接到统一的数据与函数接口上。SciPy开发者在2020年的综述中回顾：项目从早期版本发展到2017年发布1.0，逐步汇集了优化、积分、信号处理等算法。今天可以用一个NumPy数组保存时间，用一个Python函数表达模型，再由SciPy调整参数。研究者因此能把精力放在实验问题和结果检验上，同时保留可重复执行的计算步骤。下图用本节的25个观测展示这条连接：先让三个候选时间尺度生成曲线，再逐点计算残差，最后比较残差平方和。固定时间尺度时，A与b由线性最小二乘重新求解；星号表示本节有边界curve_fit得到的结果。

![SciPy计算方法图解：本节25个教学观测、固定τ=2、3、5 s时重新求得的A与b、逐点残差以及残差平方和。右下曲线在每个τ处重新求解两个线性系数；星号为有边界curve_fit的结果。SciPy的发展把这些数组与函数操作接到可复用的数值算法上。](https://ml-biomat.com/static/tutorials/python-scientific/figures/2c0a02666dca6a638d9f76c0.svg?v=2c0a02666dca)

图 2SciPy计算方法图解：本节25个教学观测、固定τ=2、3、5 s时重新求得的A与b、逐点残差以及残差平方和。右下曲线在每个τ处重新求解两个线性系数；星号为有边界curve_fit的结果。SciPy的发展把这些数组与函数操作接到可复用的数值算法上。

`curve_fit`首先需要模型函数。函数的第一个参数是自变量，这里为时间；后面的参数依次为振幅、时间尺度和平台。它还需要长度相同、顺序对应的时间与应力数组。若时间数组经过排序，应力数组必须采用同一顺序。`p0=[2., 2., .3]`给出搜索起点，单位依次为kPa、s、kPa；这组数值告诉算法从什么形状开始尝试，并不把最终结果固定在那里。`bounds`给出参数允许范围，本例把振幅与平台约束为非负，把τ保持为正。

数值搜索可以想成在一张误差地形图上寻找低处：每个位置是一组参数，高度是残差平方和。算法试探附近怎样移动能够降低目标，再更新参数继续计算。起点离合适区域太远，参数之间差距悬殊，或者许多参数组合都产生近似相同的曲线，都会让搜索更困难。使用合理单位、数量级相近的参数和基于曲线的初值，有助于把问题写得清楚。遇到收敛信息时，应把它与得到的参数、边界位置和残差一起检查，而不是只看函数是否返回了一个数组。

返回的`popt`按模型函数中的顺序保存拟合参数，`pcov`保存基于局部线性近似的参数协方差估计。对角元素开平方，可得到相应的局部参数标准差；不同参数的单位也随之保留。这里的“局部”表示把最优点附近的曲面近似为较简单的形状。如果数据只能确定某两个参数的组合，参数之间会强烈关联，单独读几个标准差就容易遗漏这种关系。后面的剖面图将直接改变一个参数并重新优化其他参数，把这件事画出来。

## 运行完整例子，再读曲线留下的偏差

下面的程序在一个文件中完成数据生成、两种模型的拟合、参数剖面、四幅图和数值摘要。`relaxation`表达物理模型；`profile`在固定τ时求解另外两个系数；`main`组织输入和输出。图像与数据统一写入指定的输出目录，CSV保留每个时间、应力和教学扰动。运行时可通过`--language zh`或`--language en`选择图中文字。代码中的绘图后端用于直接保存文件，因此完整运行结束后应打开生成的图和摘要检查结果。

### 完整示例：曲线、残差、剖面与独立数值检查

主程序直接使用NumPy、SciPy与Matplotlib。固定扰动数组、模型、原生拟合、独立剖面与四幅图都在同一文件中；输出包含CSV和数值摘要。

```
"""Fit an explicitly defined relaxation dataset and inspect residuals and profiles."""
from pathlib import Path
import argparse
import json
import numpy as np
import scipy
from scipy.optimize import curve_fit, minimize_scalar
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BLUE, RED, INK, GRAY = "#28658c", "#b64a35", "#202e39", "#71808b"


def relaxation(t, amplitude, tau, baseline):
    return amplitude * np.exp(-np.asarray(t) / tau) + baseline


def profile(t, observed, tau):
    """Solve the two linear coefficients at a fixed positive time scale."""
    design = np.column_stack((np.exp(-t / tau), np.ones_like(t)))
    amplitude, baseline = np.linalg.lstsq(design, observed, rcond=None)[0]
    residual = observed - design @ np.array([amplitude, baseline])
    return float(residual @ residual), float(amplitude), float(baseline)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    zh = language == "zh"
    def tr(a, b): return a if zh else b
    plt.rcParams.update({"font.family": [name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],
        "font.size": 11, "axes.labelsize": 12, "axes.titlesize": 13,
        "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "text.color": INK, "svg.fonttype": "none",
        "svg.hashsalt": "P19", "savefig.facecolor": "white"})
    t = np.arange(25, dtype=float) / 2
    noise = np.array([.04,-.03,.02,-.05,.01,.03,-.02,.04,-.01,-.03,
                     .02,-.04,.03,0,-.02,.01,.03,-.01,-.03,.02,-.01,.03,-.02,.01,-.02])
    truth = np.array([2.4, 3., .4])
    y = relaxation(t, *truth) + noise
    popt, pcov = curve_fit(relaxation, t, y, p0=[2., 2., .3],
        bounds=([0., .1, 0.], [10., 20., 3.]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    def zero_baseline(time, amplitude, tau): return relaxation(time, amplitude, tau, 0.)
    pzero, _ = curve_fit(zero_baseline, t, y, p0=[2., 3.],
        bounds=([0., .1], [10., 20.]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    residual = y - relaxation(t, *popt)
    residual_zero = y - zero_baseline(t, *pzero)
    tau_grid = np.linspace(1., 7., 301)
    profiles = {}
    for end in (3., 6., 12.):
        use = t <= end
        solution = minimize_scalar(lambda tau: profile(t[use], y[use], tau)[0],
                                   bounds=(1., 7.), method="bounded",
                                   options={"xatol": 1e-12})
        loss, amp, base = profile(t[use], y[use], solution.x)
        profiles[str(int(end))] = {"n": int(use.sum()), "tau_s": float(solution.x),
            "amplitude_kPa": amp, "baseline_kPa": base, "sse_kPa2": loss,
            "curve": [profile(t[use], y[use], q)[0] for q in tau_grid]}
    clean, _ = curve_fit(relaxation, t, relaxation(t, *truth), p0=[2., 2., .3],
                        bounds=([0., .1, 0.], [10., 20., 3.]),
                        xtol=1e-12, ftol=1e-12, gtol=1e-12)
    assert np.max(np.abs(clean-truth)) < 1e-8
    assert abs(profiles["12"]["tau_s"] - popt[1]) < 1e-5
    assert residual @ residual < residual_zero @ residual_zero
    dense = np.linspace(0, 12, 400)
    def save(fig, name):
        fig.savefig(output / f"{name}-{language}.svg", metadata={"Date": None})
        fig.savefig(output / f"{name}-{language}.png", dpi=180)
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(11.5, 5.5), layout="constrained")
    ax.plot(dense, relaxation(dense, *truth), color=BLUE, lw=2.5)
    ax.axhline(.4, color=GRAY, ls="--", lw=1)
    ax.vlines(3, 0, relaxation(3, *truth), color=RED, ls="--")
    ax.scatter([0,3], relaxation(np.array([0,3]), *truth), color=RED, zorder=4)
    ax.annotate("A + b = 2.8 kPa", (0,2.8), xytext=(1.3,2.65),
                arrowprops={"arrowstyle":"->", "color":GRAY})
    ax.annotate(tr("t = τ：超出平台的部分剩下约36.8%", "t = τ: 36.8% of the initial excess remains"),
                (3,relaxation(3,*truth)), xytext=(4.4,1.75),
                arrowprops={"arrowstyle":"->", "color":RED}, color=RED)
    ax.text(8,.23,"b = 0.4 kPa",color=GRAY)
    ax.set(xlim=(-.2,12),ylim=(0,3.1),xlabel=tr("时间 / s","Time / s"),
           ylabel=tr("应力 / kPa","Stress / kPa"),
           title=tr("参数把曲线拆成高度、时间尺度和平台", "Parameters separate amplitude, time scale, and plateau"))
    save(fig,"parameters")
    fig, axes = plt.subplots(2,2,figsize=(12.3,8.2),sharex=True,sharey="row",
                             gridspec_kw={"height_ratios":[2.1,1]},layout="constrained")
    for j,(parameters,errors,title) in enumerate([(popt,residual,tr("带平台的指数模型","Exponential with a plateau")),
         (np.r_[pzero,0.],residual_zero,tr("强制平台为零","Plateau fixed to zero"))]):
        axes[0,j].scatter(t,y,s=27,color=INK,label=tr("教学数据","Teaching data"),zorder=3)
        axes[0,j].plot(dense,relaxation(dense,*parameters),color=BLUE if j==0 else RED,lw=2,
                       label=tr("拟合曲线","Fitted curve"))
        axes[0,j].set_title(title,loc="left")
        axes[0,j].legend(frameon=False,fontsize=10)
        axes[0,j].set_ylim(0,3.05)
        axes[1,j].axhline(0,color=GRAY,lw=1)
        axes[1,j].vlines(t,0,errors,color=BLUE if j==0 else RED,lw=1.5)
        axes[1,j].scatter(t,errors,color=BLUE if j==0 else RED,s=20)
        axes[1,j].set(xlabel=tr("时间 / s","Time / s"),ylim=(-.3,.3))
        axes[1,j].text(.96,.94,f"SSE = {errors @ errors:.5f} kPa²",transform=axes[1,j].transAxes,
                        va="top",ha="right",bbox={"fc":"white","ec":"none","alpha":.9},fontsize=10)
    axes[0,0].set_ylabel(tr("应力 / kPa","Stress / kPa"))
    axes[1,0].set_ylabel(tr("观测 − 拟合 / kPa","Observed − fitted / kPa"))
    save(fig,"residuals")
    fig, axes = plt.subplots(1,2,figsize=(12.3,5.7),layout="constrained")
    colors=[RED,GRAY,BLUE]
    for end,color in zip((3,6,12),colors):
        p=profiles[str(end)]
        axes[0].plot(tau_grid,np.asarray(p["curve"])-p["sse_kPa2"],color=color,lw=2,
                     label=f"0–{end} s; n={p['n']}")
        axes[0].scatter([p["tau_s"]],[0],color=color,s=35,zorder=4)
    axes[0].set(xlabel=tr("固定的时间尺度 τ / s","Fixed time scale τ / s"),
        ylabel=tr("相对最小值增加的SSE / kPa²","SSE above its minimum / kPa²"),ylim=(-.015,.6),
        title=tr("观测窗口决定谷底有多清楚","The observation window shapes the valley"))
    axes[0].legend(frameon=False)
    axes[1].scatter(t,y,color=INK,s=25,zorder=4)
    for tau,color in zip((2.,3.,5.),(RED,BLUE,GRAY)):
        _,amplitude,baseline=profile(t[t<=3],y[t<=3],tau)
        axes[1].plot(dense,relaxation(dense,amplitude,tau,baseline),color=color,lw=2,label=f"τ = {tau:g} s")
    axes[1].axvspan(0,3,color="#eaf1f5",zorder=0)
    axes[1].set(xlabel=tr("时间 / s","Time / s"),ylabel=tr("应力 / kPa","Stress / kPa"),
                title=tr("只用前3秒拟合，向后外推","Fit the first 3 seconds, then extrapolate"),ylim=(-.6,3.1))
    axes[1].legend(frameon=False)
    save(fig,"profiles")
    fig,axes=plt.subplot_mosaic([['curves','curves'],['residuals','objective']],
                                figsize=(12.3,9),layout='constrained')
    axes['curves'].scatter(t,y,color=INK,s=24,zorder=5,label=tr('25个教学观测值','25 teaching observations'))
    candidate_sse=[]
    for tau,color in zip((2.,3.,5.),(RED,BLUE,GRAY)):
        loss,amp,base=profile(t,y,tau);candidate_sse.append(loss)
        axes['curves'].plot(dense,relaxation(dense,amp,tau,base),color=color,lw=2,
                            label=f'τ={tau:g} s; A={amp:.3f} kPa; b={base:.3f} kPa')
        axes['residuals'].plot(t,y-relaxation(t,amp,tau,base),'o-',color=color,ms=3,
                               lw=1.3,label=f'τ={tau:g} s')
    axes['curves'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / kPa','Stress / kPa'),
                       title=tr('A  函数接口：每个候选τ都生成一条完整曲线','A  Function interface: each candidate τ generates a complete curve'))
    axes['curves'].legend(frameon=False,fontsize=10,ncols=2)
    axes['residuals'].axhline(0,color=INK,lw=1)
    axes['residuals'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('观测 − 模型 / kPa','Observed − model / kPa'),
                          title=tr('B  数组相减：逐点计算残差','B  Array subtraction: pointwise residuals'))
    axes['residuals'].legend(frameon=False)
    axes['objective'].plot(tau_grid,profiles['12']['curve'],color=INK,lw=1.7)
    axes['objective'].scatter([2,3,5],candidate_sse,c=[RED,BLUE,GRAY],s=55,zorder=5)
    axes['objective'].scatter([popt[1]],[residual@residual],marker='*',color='#d19a24',s=150,zorder=6,
                              label=tr('有边界curve_fit结果','Bounded curve_fit result'))
    axes['objective'].set(xlabel=tr('固定的τ / s','Fixed τ / s'),ylabel='SSE / kPa²',
                          title=tr('C  数值搜索：定位平方和的低处','C  Numerical search: locate a lower sum of squares'))
    axes['objective'].legend(frameon=False,fontsize=10)
    for a in axes.values():a.grid(alpha=.14)
    fig.suptitle(tr('SciPy：数组、模型函数与数值求解在同一问题中相接',
                     'SciPy: arrays, model functions, and numerical solvers meet'),fontsize=16)
    save(fig,"history")
    np.savetxt(output/"relaxation.csv",np.c_[t,y,noise],delimiter=",",comments="",
               header="time_s,stress_kPa,teaching_perturbation_kPa",fmt="%.12g")
    summary={"data_kind":"defined teaching model plus explicit perturbations", "n":len(t),
        "truth":{"amplitude_kPa":2.4,"tau_s":3.,"baseline_kPa":.4},
        "fit":{"amplitude_kPa":float(popt[0]),"tau_s":float(popt[1]),"baseline_kPa":float(popt[2]),
               "sse_kPa2":float(residual@residual),"residual_sd_kPa":float(np.sqrt(residual@residual/(len(t)-3))),
               "local_parameter_std":np.sqrt(np.diag(pcov)).tolist()},
        "zero_baseline":{"amplitude_kPa":float(pzero[0]),"tau_s":float(pzero[1]),
                         "sse_kPa2":float(residual_zero@residual_zero)},
        "profiles":{k:{q:v for q,v in p.items() if q!="curve"} for k,p in profiles.items()},
        "noise_free_max_abs_error":float(np.max(np.abs(clean-truth))),
        "profile_native_tau_difference_s":float(abs(profiles["12"]["tau_s"]-popt[1])),
        "versions":{"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__}}
    (output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    (output/"profile-data.json").write_text(json.dumps({"tau_s":tau_grid.tolist(),"profiles":profiles}),encoding="utf-8")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args()
    main(args.output,args.language)
```

实际计算得到A≈2.40810 kPa、τ≈2.97543 s、b≈0.40224 kPa，残差平方和约为0.01679233 kPa²。它们与生成参数2.4 kPa、3 s、0.4 kPa接近，但没有完全相同，因为拟合面对的是加入了扰动的25个观测。程序还单独去掉扰动，使用相同算法恢复生成参数；这时最大绝对偏差约为4.4×10⁻¹⁶，处于浮点运算舍入的尺度。这两次计算回答不同问题：前者展示扰动下的参数估计，后者检查模型和拟合调用在已知答案上的一致性。

![同一组25个教学记录分别拟合带平台和零平台模型。上排给出曲线，下排使用相同残差轴；零平台模型的早、中、晚段残差呈有组织的偏移。每条竖线保留对应记录的时间。](https://ml-biomat.com/static/tutorials/python-scientific/figures/9a5c160935f6097ce7a85466.svg?v=9a5c160935f6)

图 3同一组25个教学记录分别拟合带平台和零平台模型。上排给出曲线，下排使用相同残差轴；零平台模型的早、中、晚段残差呈有组织的偏移。每条竖线保留对应记录的时间。

强制平台为零以后，算法得到τ≈4.97216 s，平方和增加到0.37693015 kPa²。为了兼顾后段仍然较高的观测，曲线整体下降得更慢，于是中段偏高、后段又偏低。下排残差清楚保留了这种结构：先出现正值，中间连续为负，后面再次转为正。它说明零平台模型难以同时描述这组记录的早、中、晚三个阶段。带平台模型的残差则围绕零上下变化，幅度也小得多；两排共享坐标范围，使这种差别可以直接比较。

残差还可以浓缩成一个与应力同单位的尺度。先把平方和除以观测数减去参数数，再开平方，便得到常用的残差标准差估计。它比平方和更容易与某个单独观测的波动比较，但仍需配合残差图，因为一个数值无法表达连续偏正或偏负的形状。在本例中，25个观测拟合3个参数，对应22个残差自由度，得到约0.02763 kPa。残差尺度描述记录围绕曲线的波动，参数标准差描述拟合参数的局部不确定程度，两者回答的问题不同。

$$
s_r=\sqrt{\frac{Q}{n-p}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/516137c2821586f22d9e1cae.svg) | 残差标准差的估计量，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | 残差平方和，kPa² |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 观测数，无量纲；这里25 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 拟合参数数，无量纲；这里3 |

拟合用掉p个参数方向，所以残差尺度按n−p调整。25条记录、3个参数、Q=0.0167923269 kPa²，得到sqrt(0.0167923269/22)=0.02762766 kPa。它在误差独立、均值模型适当、方差相同的统计解释下估计记录的误差尺度；非线性模型中这是常用局部近似。它与参数标准差是不同的量。

## 为什么延长观测时间有时比增加点数更有用

设想仪器只记录到3 s。早期曲线下降明显，却还没充分接近平台；这时较低的平台配上较慢的衰减，或较高的平台配上较快的衰减，都可能穿过相近的点群。参数之间能够互相补偿，叫作可辨识性不足：数据对某个参数的区分能力较弱。这是观测内容与模型之间的关系。即使把同一小段时间采得更密，也主要增加早期的信息；把记录延长到接近平台，则会增加一种原先缺少的形状信息。

剖面计算可以把补偿关系逐步展开。先固定一个τ，比如3 s，此时每个观测时间对应的指数值都已确定。把这些指数值看作一个新变量z，模型就成为关于z的直线，振幅是斜率，平台是截距。用最小二乘求出这条直线，就得到了当前τ下最合适的A和b。然后把τ改成3.1 s，再重新拟合一次A和b；如此重复，便能画出“每个τ能达到的最小平方和”。这一条曲线就是τ的目标函数剖面。

$$
z_i=\exp(-t_i/\tau),\quad A=\frac{\sum_i(z_i-\bar z)(y_i-\bar y)}{\sum_i(z_i-\bar z)^2},\quad b=\bar y-A\bar z
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | 固定τ后第i个指数值，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/1cedf803e310ed61a4074c0b.svg) | 记录时间与固定时间尺度，s |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 观测应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/0c0542cabaa03a20baa1420d.svg) | 全部z值的算术平均，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b95acd43e540455890524d58.svg) | 全部观测应力的算术平均，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/95c6ae2cac80faa066eac4ee.svg) | 当前固定τ下的最小二乘振幅与平台，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/5ca220bf09b42c86c851749f.svg) | 对当前选用的全部记录求和 |

固定τ后，模型成为关于z的直线Az+b。A取z与y共同变化的量除以z自身变化的量，b把直线移到平均点。以z=[1,0.5,0]、y=[2.8,1.6,0.4] kPa为代数算例，平均值为0.5与1.6，分子为1.2 kPa，分母为0.5，因此A=2.4 kPa、b=0.4 kPa。这里z=0是指数衰减的极限，用来简化手算；实际有限时间的z均大于0。计算要求z不是全部相同。

代码用`np.linalg.lstsq`解固定τ时的两列设计矩阵，浏览器实验则使用上式的平均值和求和计算。两种写法求解同一个线性问题，提供相互核对的途径。最后再用一维最小化寻找剖面的谷底，完整数据得到τ≈2.975432546 s，与原生`curve_fit`的差约为1.4×10⁻⁹ s。这里独立的是求解路线：一次同时调整三个参数，另一次先解析地消去两个线性参数，再搜索剩下的时间尺度。

![左图固定τ、重新拟合A和b后计算SSE，各条曲线减去自身最小值，以比较谷底形状。右图只用0–3 s记录分别拟合三个固定τ；阴影外的曲线是外推。这里的剖面拟合允许b自由取值，因此某些外推平台为负。](https://ml-biomat.com/static/tutorials/python-scientific/figures/bd5777310c66388e175fd121.svg?v=bd5777310c66)

图 4左图固定τ、重新拟合A和b后计算SSE，各条曲线减去自身最小值，以比较谷底形状。右图只用0–3 s记录分别拟合三个固定τ；阴影外的曲线是外推。这里的剖面拟合允许b自由取值，因此某些外推平台为负。

左图中，0–3 s数据的谷底较平，许多τ都能达到相近的平方和；0–12 s的谷底明显更窄。每条曲线减去了自己的最小值，所以图中比较的是偏离各自最佳τ的代价，而不是不同样本数的总误差大小。右图只用前3 s拟合，三条曲线在阴影区域接近，向后延伸后却逐渐分开。剖面计算让b自由变化以展示参数补偿，因而某些τ对应负的平台；若研究条件要求非负平台，需把同样的约束也加到剖面求解中，再解释受约束后的谷底。

## 同时观察曲线、残差和误差地形

下面的实验把τ作为可以主动改变的参数，每次变化都重新计算最合适的A和b。主图显示当前曲线与25条记录；用于拟合的时间范围以阴影标出，范围外记录用空心点表示。残差图显示当前纳入记录的残差；剖面图显示相同数据窗口下的整个τ剖面，并用红点标出当前选择。这样可以同时回答三个问题：曲线在哪里改变、哪些记录偏离、整体目标量怎样变化。剖面图纵轴使用当前窗口的平方和，选择不同窗口时会按数据范围更新刻度。

## 改变时间尺度，观察参数怎样互相补偿

每次固定τ后，重新拟合A与b。三幅图使用同一组教学数据；实心点参与拟合，空心点用于观察外推。A与b在这里自由求解，平台可取负值。观察窗口改变时，残差和SSE纵轴会随数据重新定标，请同时读刻度。

[Figure: 拟合曲线、纳入范围与外推记录](https://ml-biomat.com/tutorials/python-scientific/p19/#P19-curve)

[Figure: 纳入记录的有符号残差](https://ml-biomat.com/tutorials/python-scientific/p19/#P19-residual)

[Figure: 不同固定时间尺度下的最小残差平方和](https://ml-biomat.com/tutorials/python-scientific/p19/#P19-profile)

先保留12 s窗口，把τ从3 s改到5 s。注意振幅和平台也在变化：它们在尽量补偿新的时间尺度，而残差图展示补偿以后仍留下的结构。再保持τ=5 s，把观测窗口缩短到3 s。早段点和曲线会显得更接近，剖面谷底也更平；后段空心点则清楚展示外推与完整记录之间的差别。空心点始终保留在页面上，使“暂不纳入拟合”与“记录不存在”能够区分。点击重置可返回τ=3 s、窗口12 s，重新比较同一基准。

这个实验不会把每次滑块位置都称为最优值。红点表示当前固定的τ，A与b是在这个条件下重新拟合的系数；只有剖面谷底附近才对应这条时间尺度搜索中的最佳区域。这个区分也适用于实际研究：锁定某个文献参数以后求得的其他系数，是条件拟合；把所有参数都放开，是另一种拟合问题。报告参数时写清哪些量固定、哪些量自由，其他人才能正确重现同一条曲线。

## 让拟合结果回到实验问题

一份可理解的拟合结果应同时保留数据范围、模型、参数单位和残差。本例可以完整表述为：在0–12 s的25个教学观测上，用带平台的单指数模型进行等权最小二乘拟合，得到τ约2.975 s、平台约0.402 kPa；残差尺度约0.0276 kPa。读者由此知道数字属于什么模型、来自哪段时间，也能在图中检查模型是否遗漏了有组织的变化。单独列出一个很长的小数，反而丢掉了这些决定含义的信息。

当残差出现明显结构时，可以把它转成下一步具体工作。若随时间缓慢偏移，检查仪器基线和环境条件；若早期偏离集中，核对加载过程是否已完成、时间零点是否一致；若曲线先快后慢而单一τ难以兼顾，比较是否需要多个可解释的松弛过程，并增加覆盖相应时间范围的记录。若几个参数互相补偿，延长观测窗口或独立测量平台，往往比单纯增加迭代次数更能解决问题。

相同的思路也可用于反应浓度、药物释放的局部阶段、冷却曲线或仪器响应，但需要为每个问题重新明确模型和参数含义。例如冷却问题中的平台可能对应环境温度，振幅对应初始温差，时间尺度取决于传热条件。换一个应用时，单位、边界条件、观测误差和机制都应随问题调整。Python函数负责把这些选择准确写进计算；SciPy负责求解选定的数值问题；图形与残差帮助把求解结果重新接回可观察的科学过程。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P19.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   模型函数、参数边界、sigma与局部协方差。

   SciPy BSD-3 documentation; original teaching dataset and explanations
2. [SciPy: Optimization tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)

   最小二乘问题与数值优化接口。

   SciPy BSD-3 documentation
3. [NIST/SEMATECH: Least Squares](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm)

   平方和、线性系数解与残差尺度的数学参考。
4. [Virtanen et al. (2020), SciPy 1.0](https://arxiv.org/abs/1907.10121)

   由开发者撰写的SciPy计算史与方法综述。

   CC BY 4.0; facts paraphrased, original diagram
