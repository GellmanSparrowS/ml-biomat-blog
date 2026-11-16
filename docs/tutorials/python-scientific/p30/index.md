# 把模拟输出变成可比较的结果

Source: https://ml-biomat.com/tutorials/python-scientific/p30/
Language: zh-CN

以有解析解的振子为参照，对齐八份轨迹，联动比较位置、能量、精度与计算步数。

## 两份轨迹，怎样才算在比较同一个过程

运行一次模拟，往往会得到成百上千行时间、位置、速度和能量。把两条曲线画在一起并不难，真正需要判断的是：它们描述了同一段物理时间吗，差别来自材料参数还是数值方法，降低步长以后结果有没有稳定下来？这些问题出现在分子运动、弹性振动、热传导和流体计算里。本章以一个可以写出精确解的弹簧振子为对象，生成八份模拟输出，再像处理外部软件的结果一样读取、对齐、比较，最后得到有明确依据的精度与工作量判断。

这里的振子是确定性的教学模型：质量为1 kg的物体连接到劲度系数为1 N/m的理想弹簧，初始偏离平衡位置1 m，从静止释放，没有摩擦和外部驱动。位置和速度由程序积分产生，属于模拟数据。选择这个模型，是因为它既有往复运动和能量交换，又有独立的解析解，能把真实动力学与计算误差分开。掌握这套比较方式后，可以把输入换成更复杂软件导出的表格，而继续保留时间、单位、观测定义和检查方法。

八次运行使用相同初始条件和20 s终止时间，只改变两项数值设置：显式Euler或速度Verlet方法，以及0.025、0.05、0.1、0.2 s四种步长。每份CSV记录积分步号、时间、位置和速度。步长较小时文件行数更多，但多出来的行只是同一条计算轨迹上的更密采样。比较精度时，我们会选出共同的101个物理时刻，避免让某一份文件因行数多而在平均误差中获得不同权重。

## 从弹簧的方向感理解运动与解析参照

把平衡位置选为零，向右为正。物体拉到右侧时，弹簧把它往左拉；物体来到左侧时，弹簧又把它往右拉。力总是指向平衡位置，这就是恢复力。理想弹簧的力与偏移量成正比，偏移越大，拉回的力越大。牛顿第二定律把力和加速度连接起来，于是我们可以由当前位置算出加速度，再计算下一时刻的位置和速度。

$$
F=-kx,\qquad a=\frac{F}{m},\qquad \omega=\sqrt{\frac{k}{m}},\qquad x_{\rm exact}(t)=A\cos(\omega t),\qquad v_{\rm exact}(t)=-A\omega\sin(\omega t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | 弹簧恢复力，N |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 劲度系数，N/m，本例1 N/m |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 相对平衡位置的位移，m |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | 加速度，m/s² |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 质量，kg，本例1 kg |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad/s；弧度无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 初始位移幅值，m，本例1 m |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 物理时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/38691bf7f7eb638d9ad5ea26.svg) | 解析位置和速度，分别为m和m/s；初速度为0 |
| ![Formula](https://ml-biomat.com/static/agent-math/93fd67f8da8bc15f77fd04df.svg) | 余弦与正弦，输入角度采用弧度，函数值无量纲 |

负号使力与位移反向。力除以质量得到加速度；余弦的二阶时间导数带来−ω²因子，取ω²=k/m就满足运动关系。本例t=1 s时ωt=1 rad，位置cos(1)≈0.540302 m，速度−sin(1)≈−0.841471 m/s。弹簧力约−0.540302 N，加速度约−0.540302 m/s²。解析表达对应理想弹簧、无摩擦和无驱动条件。

余弦和正弦可以看成圆周运动在两条坐标轴上的投影。圆周角度匀速增加时，一个投影从最大值开始减小，另一个投影先从零开始变化；这正好描述从静止释放的振子的位置和速度。角频率ω决定这种往复有多快，周期是转过一整圈所需的时间。本例ω=1 rad/s，一个周期约为6.283 s，因此20 s覆盖了略多于三次往复。代码中的三角函数使用弧度，不能把角度值直接当作输入。

解析参照的作用是给出任意物理时刻的位置和速度，而不是把某个很小步长的计算先当作绝对正确。比如t=0时位置1 m、速度0；约四分之一个周期后位置经过零点，速度向左达到最大幅值。程序可以在共同时间网格上直接计算这些数值，并与每份输出的对应行相减。这样得到的偏差有明确对象：指定数值积分结果与同一个理想振子的精确运动之间的差别。

## 同样的力，怎样走出两种数值轨迹

显式Euler方法使用当前时刻的信息推进一小步：用当前速度估计位置增量，用当前加速度估计速度增量。它像在弯曲道路上沿当前方向走一小段直线，下一步再重新判断方向。这个规则容易理解，也适合检查程序中的更新顺序。位置和速度都应由同一旧时刻的数值计算；如果先覆盖位置，再用新位置更新速度，就已经变成另一种算法，不能仍沿用显式Euler的名称和预期结果。

$$
x_{n+1}=x_n+h v_n,\qquad v_{n+1}=v_n+h a_n,\qquad a_n=-\frac{kx_n}{m}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 积分步编号，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | 时间步长，s，正数 |
| ![Formula](https://ml-biomat.com/static/agent-math/8db5b3541f45a9fecfa6bd7d.svg) | 当前与下一步位移，m |
| ![Formula](https://ml-biomat.com/static/agent-math/7767393d1a751e86f1bb995c.svg) | 当前与下一步速度，m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/35c129770db807490a096310.svg) | 当前位移处的加速度，m/s² |
| ![Formula](https://ml-biomat.com/static/agent-math/7850be60bb48378ac7367cc8.svg) | 劲度系数N/m、质量kg |

把一个短时间段内的速度与加速度暂视为当前值，时间乘变化率得到相应增量。本例x₀=1 m、v₀=0、a₀=−1 m/s²、h=0.1 s，得到x₁=1 m、v₁=−0.1 m/s。两个更新都使用旧状态，顺序覆盖旧值会改变算法。

对没有摩擦的振子，显式Euler会逐步增加数值能量。这个现象能够从一步计算直接看出来：本例第一步0.1 s后位置仍为1 m，速度变成−0.1 m/s，弹簧势能尚未减少，动能却增加了。将一般一步的位置和速度代入能量式，可以发现每步能量都乘以一个因子：1加上“角频率与步长乘积”的平方。步长0.1 s和角频率1 rad/s对应每步乘1.01，200步后能量约为初值的7.316倍。它解释了曲线振幅为何不断变大，而不必把这误认为材料出现了自发激励。

速度Verlet把一次更新分成对称的三个动作：先用旧位置处的加速度更新半步速度，用这份半步速度更新整步位置，再用新位置处的加速度完成另半步速度。Swope及合作者1982年研究分子团簇计算时讨论的速度形式，使位置与速度能够在相同时刻保存。今天LAMMPS的普通时间积分也采用这一类更新。这里把分子体系简化成一个振子，可以直接看到算法在一个时间步内做了什么。

$$
v_{n+1/2}=v_n+\frac{h}{2}a_n,\qquad x_{n+1}=x_n+h v_{n+1/2},\qquad v_{n+1}=v_{n+1/2}+\frac{h}{2}a_{n+1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e11d2c669fc940d6bc996598.svg) | 步编号无量纲，步长h单位s |
| ![Formula](https://ml-biomat.com/static/agent-math/cd3c6f6a10ac62197d9843a2.svg) | 当前、中间半步与下一整步速度，m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/8db5b3541f45a9fecfa6bd7d.svg) | 当前与下一步位移，m |
| ![Formula](https://ml-biomat.com/static/agent-math/b230218f9e8d2fff4e3df1d8.svg) | 旧位置与新位置处按−kx/m计算的加速度，m/s² |

两次半步速度更新分别使用位置更新前后的加速度，形成对称顺序。本例h=0.1 s，先得半步速度−0.05 m/s，再得位置0.995 m；新加速度为−0.995 m/s²，最后速度为−0.05−0.05×0.995=−0.09975 m/s。

![相空间中的完整轨迹和速度Verlet首步的三个实际更新。位置与速度是不同的状态坐标；右下数值由首步直接计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/77fd11ea5a280fc129a2afc5.svg?v=77fd11ea5a28)

图 1相空间中的完整轨迹和速度Verlet首步的三个实际更新。位置与速度是不同的状态坐标；右下数值由首步直接计算。

右上图用位置作横轴、速度作纵轴，将首步的三个动作画成两段竖直移动和一段水平移动。竖直移动表示位置暂时保持不变、速度发生变化；水平移动表示使用半步速度更新位置。它是一幅状态空间图，不是物体在二维房间里走过的路线。左侧则显示完整20 s轨迹：解析解是闭合轨道，Euler轨迹逐渐向外扩展，速度Verlet轨迹保持在附近。两种图共同说明了更新顺序与长期表现之间的联系。

## 比较物理时间，而不是文件里的行号

假如直接比较两份文件的第101行，步长0.025 s的运行只到2.5 s，步长0.2 s的运行已经到20 s。即使两种计算都完全准确，同一行的结果也通常不同，因为物体处于不同运动阶段。时间对齐要先明确比较窗口和目标时刻。本例统一选择0到20 s，每隔0.2 s取一个点，连同初始时刻共101点；四个步长都能整除0.2 s，所以每个目标时刻都存在对应的积分输出。

代码使用`pandas.merge_asof`按最近时间匹配，要求两个时间列已经递增，并设置1×10⁻⁹ s的匹配容差。这个容差用来容纳浮点表示和CSV往返带来的极小时间差，远小于最小步长0.025 s。程序同时保留目标`time_s`与实际`matched_time_s`，再检查所有目标都匹配成功。本次最大的差约为3.55×10⁻¹⁵ s，量级与浮点舍入一致；不存在用一个邻近但物理上不同的时刻替代目标点的情况。

若两份真实模拟输出的采样间隔没有共同节点，便要明确采用怎样的时间插值，并把插值误差与积分误差一起考虑。线性插值适合足够平滑、采样足够密的段落；发生碰撞、相变或载荷突跳时，跨越事件的直线可能抹去重要变化。也可以选择每份输出都能支持的较稀共同网格，或者直接比较时间区间内的统计量。具体方案由研究问题决定，不能只因为表格函数恰好能合并成功就默认合理。

![相同0.1 s步长、20 s物理窗口下的位置、共同时间误差和能量；局部图放大Verlet的小幅能量波动。](https://ml-biomat.com/static/tutorials/python-scientific/figures/bb1639b96677deb05ff72935.svg?v=bb1639b96677)

图 2相同0.1 s步长、20 s物理窗口下的位置、共同时间误差和能量；局部图放大Verlet的小幅能量波动。

上图比较同一步长0.1 s的两种积分，第二行在相同101个时刻显示位置误差，第三行比较能量相对初值的变化。第三行的局部图专门放大速度Verlet的能量误差，使小幅周期性变化能够被看清。把大幅漂移和小幅波动同时放进一条宽纵轴时，后者容易被视觉压平；局部放大保留了整体差别，也让读者读到较小误差的真实幅度。

## 完整程序：先产生输出，再从输出计算结果

这个项目的完整入口如下。运行以后，`trajectories`保存八份原始模拟表，名称包含方法和步长；每份`-aligned.csv`保存共同时间网格上的匹配值、解析位置和误差；`comparison.csv`汇总每次运行的步数、位置误差和能量偏差。文件名帮助识别运行，列名里的单位则帮助理解数值。它们共同保证比较时不会把“这个运行是什么”和“这一列怎么算”留给读者猜测。

### 运行完整比较

使用zh生成中文图。

```
python main.py --output results --language en
```

### 生成、读回并比较八份模拟输出

所有动力学、能量、时间对齐与绘图均包含在此文件。

```
"""Generate, read, align, and compare harmonic-oscillator simulation outputs."""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import NullLocator

MASS = 1.0             # kg
SPRING = 1.0           # N/m
INITIAL_POSITION = 1.0 # m
FINAL_TIME = 20.0      # s
STEPS = [.025, .05, .1, .2]



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def simulate(method, dt):
    count = round(FINAL_TIME / dt)
    if not np.isclose(count * dt, FINAL_TIME):
        raise ValueError('Final time must be an integer number of steps')
    x, v = np.empty(count+1), np.empty(count+1)
    x[0], v[0] = INITIAL_POSITION, 0.0
    for i in range(count):
        acceleration = -SPRING * x[i] / MASS
        if method == 'euler':
            x[i+1] = x[i] + dt*v[i]
            v[i+1] = v[i] + dt*acceleration
        elif method == 'verlet':
            half_velocity = v[i] + .5*dt*acceleration
            x[i+1] = x[i] + dt*half_velocity
            next_acceleration = -SPRING*x[i+1]/MASS
            v[i+1] = half_velocity + .5*dt*next_acceleration
        else:
            raise ValueError('Unknown integrator')
    return pd.DataFrame({'step': np.arange(count+1),
                         'time_s': np.arange(count+1)*dt,
                         'position_m': x, 'velocity_m_s': v})


def read_and_compare(path, common):
    frame = pd.read_csv(path)
    if frame.time_s.duplicated().any() or not frame.time_s.is_monotonic_increasing:
        raise ValueError('Times must be unique and increasing')
    if not np.isfinite(frame.to_numpy()).all():
        raise ValueError('All values must be finite')
    frame['energy_J'] = .5*MASS*frame.velocity_m_s**2 + .5*SPRING*frame.position_m**2
    frame['relative_energy_error'] = frame.energy_J / (.5*SPRING*INITIAL_POSITION**2) - 1
    # Retain both time columns so the alignment can be inspected explicitly.
    aligned = pd.merge_asof(common, frame.rename(columns={'time_s':'matched_time_s'}),
                            left_on='time_s', right_on='matched_time_s',
                            direction='nearest', tolerance=1e-9)
    if aligned.matched_time_s.isna().any():
        raise ValueError('A requested physical time has no matching sample')
    omega = np.sqrt(SPRING/MASS)
    aligned['exact_position_m'] = INITIAL_POSITION*np.cos(omega*aligned.time_s)
    aligned['position_error_m'] = aligned.position_m-aligned.exact_position_m
    return frame, aligned


def figures(runs, summary, output, language):
    zh = language == 'zh'; tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':available_plot_fonts(),'font.size':13,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'axes.unicode_minus':False,'svg.fonttype':'none'})
    colors={'verlet':'#205b8c','euler':'#bd5535'}
    names={'verlet':'Velocity Verlet','euler':tr('显式Euler','Forward Euler')}
    def save(fig,name):
        for ext in ['svg','png']:
            fig.savefig(output/f'{name}-{language}.{ext}',dpi=160,bbox_inches='tight',facecolor='#faf9f5')
        plt.close(fig)
    fig=plt.figure(figsize=(12.5,10),layout='constrained')
    grid=fig.add_gridspec(3,2)
    axes=[fig.add_subplot(grid[0,:]),fig.add_subplot(grid[1,:]),fig.add_subplot(grid[2,0])]
    exact_time=np.linspace(0,FINAL_TIME,1001)
    axes[0].plot(exact_time,np.cos(exact_time),color='#73828b',lw=3,alpha=.6,label=tr('解析解','Exact'))
    for method in ['euler','verlet']:
        r=next(r for r in runs if r['method']==method and r['dt']==.1)
        axes[0].plot(r['time'],r['position'],color=colors[method],lw=1.7,label=names[method])
        axes[1].plot(r['common_time'],r['common_error'],color=colors[method],lw=2)
        axes[2].plot(r['time'],np.array(r['energy'])/.5,color=colors[method],lw=2)
    axes[0].set(ylabel=tr('位置 / m','Position / m'),title=tr('步长均为0.1 s；比较相同20 s物理过程','Both steps are 0.1 s; compare the same 20 s physical interval'));axes[0].legend(ncol=3,fontsize=12)
    axes[1].set(ylabel=tr('位置误差 / m','Position error / m'),title=tr('误差在101个共同物理时刻计算','Errors evaluated at 101 shared physical times'))
    axes[2].axhline(1,color='#73828b',ls='--');axes[2].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('能量 / 初始能量','Energy / initial energy'),yscale='log')
    inset=fig.add_subplot(grid[2,1])
    vr=next(r for r in runs if r['method']=='verlet' and r['dt']==.1)
    inset.plot(vr['time'],(np.array(vr['energy'])/.5-1)*100,color=colors['verlet'],lw=1.7)
    inset.set_title(tr('Verlet相对能量误差 / %','Verlet relative energy error / %'),fontsize=13)
    inset.set(xlabel=tr('时间 / s','Time / s'));inset.set_xticks([0,10,20]);inset.set_yticks([-.25,0])
    axes[0].tick_params(labelbottom=False);axes[1].tick_params(labelbottom=False)
    save(fig,'trajectory-comparison')
    fig,axes=plt.subplots(1,2,figsize=(13,6),layout='constrained')
    for method in ['euler','verlet']:
        r=[s for s in summary['runs'] if s['method']==method]
        axes[0].loglog([s['dt'] for s in r],[s['rms_position_error_m'] for s in r],'o-',color=colors[method],lw=2,label=names[method])
        axes[1].loglog([s['steps'] for s in r],[s['rms_position_error_m'] for s in r],'o-',color=colors[method],lw=2,label=names[method])
    r=[s for s in summary['runs'] if s['method']=='verlet'];factor=r[0]['rms_position_error_m']/.025**2
    axes[0].loglog(STEPS,factor*np.array(STEPS)**2,ls=':',color='#73828b',label=tr('二阶斜率参考','Second-order slope guide'))
    axes[0].set(xlabel=tr('时间步长 / s','Time step / s'),ylabel=tr('位置均方根误差 / m','RMS position error / m'),title=tr('同一时间网格上的精度','Accuracy on one shared time grid'))
    axes[1].set(xlabel=tr('20 s内的积分步数','Integration steps over 20 s'),ylabel=tr('位置均方根误差 / m','RMS position error / m'),title=tr('精度与工作量；步数不是实测耗时','Accuracy and work; steps are not measured runtime'))
    for ax in axes:ax.legend(fontsize=11);ax.grid(alpha=.2,which='both')
    axes[0].set_xticks(STEPS,[str(s) for s in STEPS]);axes[0].xaxis.set_minor_locator(NullLocator())
    axes[1].set_xticks([100,200,400,800],['100','200','400','800']);axes[1].xaxis.set_minor_locator(NullLocator())
    save(fig,'step-convergence')
    fig=plt.figure(figsize=(13,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,1])
    phase=fig.add_subplot(gs[:,0]);detail=fig.add_subplot(gs[0,1]);note=fig.add_subplot(gs[1,1]);note.axis('off')
    phase.plot(np.cos(exact_time),-np.sin(exact_time),color='#73828b',lw=3,label=tr('解析轨道','Exact orbit'))
    for method in ['euler','verlet']:
        r=next(r for r in runs if r['method']==method and r['dt']==.1)
        phase.plot(r['position'],r['velocity'],color=colors[method],lw=1.6,label=names[method])
    phase.set(xlabel=tr('位置 / m','Position / m'),ylabel=tr('速度 / (m/s)','Velocity / (m/s)'),title=tr('同一运动的相空间表示','The same motion in phase space'));phase.set_aspect('equal');phase.legend(loc='upper left',fontsize=11)
    pts=np.array([[1,0],[1,-.05],[.995,-.05],[.995,-.09975]])
    for i in range(3):
        detail.annotate('',xy=pts[i+1],xytext=pts[i],arrowprops={'arrowstyle':'->','color':colors['verlet'],'lw':2.5})
    detail.plot(pts[:,0],pts[:,1],'o',color=colors['verlet'])
    detail.text(1.0003,-.025,tr('半步速度','Half velocity step'),fontsize=12)
    detail.text(.9975,-.043,tr('整步位置','Full position step'),fontsize=12,ha='center')
    detail.text(.9947,-.078,tr('半步速度','Half velocity step'),fontsize=12,ha='right')
    detail.set(xlim=(.990,1.005),ylim=(-.115,.015),xlabel=tr('位置 / m','Position / m'),ylabel=tr('速度 / (m/s)','Velocity / (m/s)'),title=tr('首步：0 → 0.1 s','First step: 0 → 0.1 s'));detail.ticklabel_format(axis='x',style='plain',useOffset=False)
    note.text(0,.94,'Swope et al., 1982',fontsize=19,weight='bold',transform=note.transAxes)
    note.text(0,.69,tr('速度形式的Verlet积分\n半步 → 整步 → 半步','Velocity form of Verlet integration\nHalf step → full step → half step'),fontsize=15,linespacing=1.7,transform=note.transAxes)
    note.text(0,.34,'x₁ = 0.995 m\nv₁ = −0.09975 m/s\nE₁ = 0.49998753125 J',fontsize=15,linespacing=1.7,color=colors['verlet'],transform=note.transAxes)
    save(fig,'phase-and-verlet')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('results'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    raw=args.output/'trajectories';raw.mkdir(exist_ok=True)
    common=pd.DataFrame({'time_s':np.arange(101)*.2})
    records=[];runs=[]
    for method in ['euler','verlet']:
        for dt in STEPS:
            name=f'{method}-{dt:g}';path=raw/f'{name}.csv'
            simulate(method,dt).to_csv(path,index=False)
            frame,aligned=read_and_compare(path,common)
            aligned.to_csv(args.output/f'{name}-aligned.csv',index=False)
            records.append({'method':method,'dt':dt,'steps':len(frame)-1,
                            'common_samples':len(aligned),
                            'rms_position_error_m':float(np.sqrt(np.mean(aligned.position_error_m**2))),
                            'max_relative_energy_error':float(frame.relative_energy_error.abs().max()),
                            'final_energy_J':float(frame.energy_J.iloc[-1]),
                            'max_time_mismatch_s':float((aligned.time_s-aligned.matched_time_s).abs().max())})
            runs.append({'method':method,'dt':dt,'time':frame.time_s.tolist(),
                         'position':frame.position_m.tolist(),'velocity':frame.velocity_m_s.tolist(),
                         'energy':frame.energy_J.tolist(),'common_time':aligned.time_s.tolist(),
                         'common_error':aligned.position_error_m.tolist()})
    first=simulate('verlet',.1).iloc[1]
    assert np.allclose([first.position_m,first.velocity_m_s],[.995,-.09975],atol=1e-14,rtol=0)
    euler=next(r for r in records if r['method']=='euler' and r['dt']==.1)
    analytic_euler_energy=.5*(1+.1**2)**200
    assert abs(euler['final_energy_J']-analytic_euler_energy)<1e-12
    summary={'model':'deterministic harmonic oscillator teaching simulation',
             'mass_kg':MASS,'spring_N_m':SPRING,'initial_energy_J':.5,
             'final_time_s':FINAL_TIME,'common_samples':len(common),
             'first_verlet_x_m':float(first.position_m),'first_verlet_v_m_s':float(first.velocity_m_s),
             'euler_h01_analytic_final_energy_J':analytic_euler_energy,'runs':records}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    (args.output/'lab-data.json').write_text(json.dumps({'runs':runs,'summary':summary}),encoding='utf8')
    pd.DataFrame(records).to_csv(args.output/'comparison.csv',index=False)
    figures(runs,summary,args.output,args.language)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
```

`simulate`负责动力学更新，用整数步号乘步长产生时间，避免在循环里反复累加时间造成额外漂移。它将位置和速度写成CSV，`read_and_compare`随后重新读取这些文件，并检查时间有序、没有重复、数值有限。这个读回步骤让分析真正经过数据接口；以后替换成其他软件的输出时，主要修改读取和列名映射，能量计算、共同时间比较和绘图可以继续沿用。

代码在一开始用当前加速度更新Euler的两个变量，或者分三步更新Verlet；两者的旧状态都由索引明确保留。最末的断言检查速度Verlet首步位置0.995 m和速度−0.09975 m/s，也检查Euler最终能量是否等于一步增长关系连续应用200次的结果。前者是可以手算的局部检查，后者覆盖整个积分过程。再把全部输出与解析位置比较，便能分别检查更新细节和长期累计误差。

## 能量、轨迹误差和工作量各自回答什么

理想弹簧振子的能量由动能和弹性势能组成。物体经过平衡位置时速度大、弹簧形变小，动能占主要部分；到达最远位置时速度接近零、形变最大，势能占主要部分。两者来回交换，总和应保持0.5 J。对这个封闭、无摩擦的模型，能量变化因此是一项很有解释力的数值诊断。带热浴、阻尼或外部驱动的模型则有相应能量交换，分析时要将这些物理输入和输出一起纳入账本。

$$
E=\frac12 m v^2+\frac12 k x^2,\qquad \delta_E=\frac{E-E_0}{E_0}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f4b96d945f47e589ed760ae0.svg) | 当前与初始机械能，J |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 质量，kg |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | 速度，m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | 劲度系数，N/m |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | 位移，m |
| ![Formula](https://ml-biomat.com/static/agent-math/ba6eaac03ca3b5b78c70ae6d.svg) | 相对能量误差，无量纲；乘100得到百分数 |

动能是质量乘速度平方的一半；线性弹簧从0拉到x所做功为平均力kx/2乘距离x，得到势能kx²/2。本例初始能量0.5 J。Verlet首步x=0.995 m、v=−0.09975 m/s，对应动能0.00497503125 J、势能0.4950125 J，总和0.49998753125 J，相对误差−0.0000249375，即−0.00249375%。

能量接近恒定仍不足以说明运动阶段完全准确。想象两个节拍器的摆幅相同，一个周期稍短，经过很多次往复后它们就会错开。积分轨迹也可能出现这种相位偏差。因此本例同时统计共同物理时刻上的位置均方根误差：把各时刻位置差平方、取平均、再开平方，得到与位置相同的米单位。平方会让偏离大的时刻贡献更多，开平方则把量纲从平方米恢复到米。

$$
\mathrm{RMSE}_x=\sqrt{\frac1M\sum_{j=1}^{M}\left[x_{\rm num}(t_j)-x_{\rm exact}(t_j)\right]^2}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/17f0ca443d34a5ce2ca2b438.svg) | 位置均方根误差，m |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 共同采样时刻个数，本例101，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 共同采样时刻编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/f16686b4a72a5e1ab569f6d6.svg) | 第j个共同物理时刻，s |
| ![Formula](https://ml-biomat.com/static/agent-math/6fe6f6e5934f0e34a0f210b4.svg) | 同一时刻的数值和解析位置，m |

先对相同时刻的位置相减，再平方平均并开方。两点教学算例误差为0.01 m与−0.02 m时，平方平均为(0.0001+0.0004)/2=0.00025 m²，开方约0.015811 m。本章Verlet步长0.1 s在101个共同时间点的结果约0.00334304 m。共同时间网格相同，才能让各设置的平均衡量同一窗口。

步长0.1 s时，Euler的位置均方根误差约为0.63599 m，速度Verlet约为0.0033430 m。将Verlet步长减半到0.05 s，误差约为0.00083488 m，再减半到0.025 s时约为0.00020867 m，两次都接近缩小为四分之一。这是固定终止时间下二阶收敛的可见表现。图中的二阶参考线只说明误差随步长平方变化的斜率，位置由最小步长结果确定，并未额外拟合一条“更漂亮”的数据曲线。

![八次实际积分在101个共同物理时刻的误差，与步长和更新步数的关系。虚线为二阶斜率参照。](https://ml-biomat.com/static/tutorials/python-scientific/figures/c6eaec883c06c9e18ad5a80b.svg?v=c6eaec883c06)

图 3八次实际积分在101个共同物理时刻的误差，与步长和更新步数的关系。虚线为二阶斜率参照。

更小步长也意味着更多更新：20 s里，0.2 s需要100步，0.025 s需要800步。图的右侧用步数表示工作量，与左侧的精度联系起来。步数不是实测秒数，因为不同算法的每步操作、库实现和硬件都会改变耗时；需要性能结论时，再按[耗时与内存分析](https://ml-biomat.com/tutorials/python-scientific/p28/)的方法进行真实计时。这里可以直接做出的判断是，在当前振子、时间窗口和误差定义下，每一种设置需要多少更新、获得多大的位置误差。

## 同步观察位置、相空间和能量

下面的实验把一个时刻的状态同时放在三种视图里。顶部显示物体相对平衡位置的位置；位置—时间曲线用竖线标出当前时刻，相空间图则标出同一时刻的位置和速度，能量条显示动能与势能的分配。切换方法与步长以后，时间滑块仍然选择共同的0.2 s时刻，因此你能够追踪同一个物理时刻在不同数值设置下的差别。

### 在同一时刻比较运动状态

[Figure: 当前位移与解析参照](https://ml-biomat.com/tutorials/python-scientific/p30/#P30-position)

[Figure: 位置时间曲线](https://ml-biomat.com/tutorials/python-scientific/p30/#P30-timeplot)

[Figure: 位置速度相空间](https://ml-biomat.com/tutorials/python-scientific/p30/#P30-phase)

[Figure: 动能势能与初始能量参照](https://ml-biomat.com/tutorials/python-scientific/p30/#P30-energy)

先保持Verlet和0.1 s，在约1.6 s附近观察物体经过平衡位置：位置接近零，速度幅值接近最大，能量条主要由动能组成。移到约3.2 s附近，物体接近另一端的最远位置，速度变小，势能重新占主导。然后在20 s切到Euler，观察位置和速度怎样同时离开解析参照，能量总量怎样增加。每一个变化都来自完整Python例子输出的轨迹，浏览器只读取已保存的状态并同步显示各个视图。

再比较Verlet的0.2 s与0.025 s，注意能量和相位分别怎样改进。对于这个角频率为1 rad/s的谐振子，速度Verlet的线性稳定条件要求步长与角频率的乘积小于2，所选步长都在此范围内；稳定意味着轨迹不会因这种线性更新无界放大，精度则要继续由误差曲线判断。一个步长可以稳定但仍不够准确，这也是收敛比较需要多种步长的原因。

## 把比较方法带到更大的模拟项目

处理真实研究输出时，可以先建立运行清单，记录物理模型、初始条件、边界条件、数值方法、步长、总时长和输出间隔。相同物理问题的步长比较应保持这些物理条件一致；如果研究的是材料参数变化，就先用收敛检查确定数值误差足够小，再把参数作为主要差别。这样，一张比较图中的每条曲线都对应一个明确问题，读者能理解为何两次运行值得放在一起。

有解析解时，可以像本例一样计算共同时间上的轨迹误差；没有解析解时，可以逐步细化时间或空间分辨率，比较守恒量、关键统计量以及不同数值方案之间的一致性。分子体系还需要处理周期边界、整体平移旋转和时间相关性，[轨迹分析专题](https://ml-biomat.com/tutorials/python-scientific/s06/)会把这些步骤接到实际分子数据上。高维场数据则适合用[有名字的多维数组](https://ml-biomat.com/tutorials/python-scientific/s03/)记录时间、空间坐标和物理量，避免在许多无名数组之间丢失含义。

本例最终形成八份轨迹、八份时间对齐表和一张比较表，从原始位置速度到能量、误差与工作量都能逐项追踪。结果表明，在所选20 s谐振子问题上，速度Verlet随步长减半呈现接近四倍的位置精度改进，同时维持小幅有界的能量误差。更大的模拟项目也可以沿着这条思路组织：先使输出具有清楚含义，再让比较发生在相同物理条件和相同测量定义之下。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P30.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pandas merge_asof](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html)

   按时间距离匹配、排序及显式容差。

   pandas BSD-3-Clause; official documentation.
2. [LAMMPS fix nve](https://docs.lammps.org/fix_nve.html)

   速度形式的Verlet时间积分。

   Official technical reference.
3. [LAMMPS: How a timestep works](https://docs.lammps.org/Developer_flow.html)

   位置、半步速度和力更新之间的顺序。

   Official technical reference.
4. [Swope et al. (1982), A computer simulation method for the calculation of equilibrium constants for the formation of physical clusters of molecules](https://doi.org/10.1063/1.442716)

   速度Verlet与分子团簇模拟的历史联系。

   Scientific historical citation; diagrams and teaching simulations are original.
