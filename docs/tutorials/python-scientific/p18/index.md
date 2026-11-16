# 让图回应问题：Plotly联动科学数据

Source: https://ml-biomat.com/tutorials/python-scientific/p18/
Language: zh-CN

跟随同一条周期加载记录，在时间曲线与应力—应变轨迹间切换，解释相位和耗散。

## 把同一个时刻，放进三幅互相联系的图

捏一下软垫再松手，或者反复拉伸一条柔软的材料，你会发现“拉到哪里”与“拉得多快”都可能影响手上的力。实验仪器把这个过程记录成时间、变形和受力三列数据。分别画出三张图并不难，真正有用的交互，是在一张图中选中某个位置，另外两张图立即指出同一条记录：这个时刻材料拉长了多少，正向哪个方向运动，承受的应力又是多少。本节用Plotly完成这样的联动阅读，并把整个图保存为可以离线打开的HTML。

我们使用一个规则明确的周期加载模型，既能生成完整的科学图，也能用少数关键时刻手算核对。课程将依次解释应变、应力与变化率，再把这些物理量组织成Plotly的数据轨迹、布局和悬浮信息。随后加入点击追踪、参数控制和精确读数，让交互承担实际的比较工作。完整Python程序会生成数值表、图形描述文件和自包含网页；正文中的实验可以直接操作。

Plotly擅长在浏览器中保留图上的数据身份。普通图片保存可见的形状，交互图还保存每条曲线背后的坐标数组与附加字段。鼠标悬停时，程序可以找到当前点对应的时间和数值；点击时，可以用同一个记录编号更新其他视图。这个过程仍然建立在清楚的数据组织上：只有每个点对应的记录明确，联动结果才会保持一致。

## 交互图的早期目标：换一个角度，仍然认得同一个点

1974年，Mary Anne Fisherkeller、Jerome Friedman与John Tukey在PRIM-9报告中介绍了一套交互数据分析系统。它允许研究者查看最多九个变量形成的点集，切换二维投影、旋转视角，并选择部分观测继续分析。当时交互图形的重要价值，是让研究者主动改变观察方式，寻找静态摘要中难以辨认的结构。报告特别区分了两种选择：按当前坐标范围筛选，或者把某些数据点的身份固定下来；视角改变后，这两种选择可能留下不同的点。

![以本节数据重画PRIM-9中保留观测身份、改变投影的思路。记录45在三个坐标组合中均以红点表示；灰点每隔5条记录显示一个，突出同一观测在不同投影中的位置。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0a5d73544e6701d622c2e6dc.svg?v=0a5d73544e67)

图 1以本节数据重画PRIM-9中保留观测身份、改变投影的思路。记录45在三个坐标组合中均以红点表示；灰点每隔5条记录显示一个，突出同一观测在不同投影中的位置。

本节只用三个变量，因此无需旋转到复杂的高维空间。时间—应变、时间—应力和应变—应力已经提供了三种不同的坐标投影。上图中被选中的记录45在三幅图中的位置不同，身份始终相同。它对应0.5 s、约3.536%的应变和约0.9293 kPa的应力。保留记录身份，读者就能从“这一段环线为什么在这里”追溯到“这一时刻输入和响应分别发生了什么”。

今天的浏览器让这类操作更容易分享。我们沿用PRIM-9中把观察角度与数据身份分开的思路，为每条记录保存编号，再按不同坐标组合绘图。参数改变时重新计算整条模型轨迹，选择时刻时只改变当前追踪的位置。这样一来，修改研究条件与查看已有结果具有不同、可辨认的作用。

## 先把拉伸过程写成能够计算的量

应变是长度改变量除以原始长度。如果一条原长100 mm的试样拉长5 mm，应变就是0.05，也可以写成5%。它没有长度单位，因为分子与分母的mm相消。应力则把力除以受力面积，用于比较不同尺寸试样承受的力学作用。本节使用kPa表示应力，正值与负值分别表示围绕平衡位置的两个加载方向，讨论的是理想线性模型中的小幅周期运动。

我们让应变像钟摆投影一样平滑地往返：从零开始增加，到达正的最大值，再经过零到达负的最大值，最后回到起点。正弦函数恰好描述这种周期变化。频率0.25 Hz表示每秒完成0.25个周期，也就是4 s完成一个周期；应变振幅0.05表示最大伸长与缩短的比例为5%。为了在三角函数中表示一个完整周期，需要用角频率把时间转换成弧度。

$$
\varepsilon(t)=\varepsilon_0\sin(\omega t),\qquad \dot\varepsilon(t)=\varepsilon_0\omega\cos(\omega t),\qquad \omega=2\pi f,\quad T=1/f
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 时刻t的应变，长度变化/初始长度，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 应变振幅，本节0.05，即5%，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/08df7049c9da9e9ff155cb79.svg) | 应变对时间的变化率，上方圆点表示时间导数，s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad·s⁻¹；弧度在量纲运算中为无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | 周期频率，Hz=s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 一个周期所需时间，s |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率约3.141593，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/5bc8e1a5d4bcca693b9f9dcf.svg) | 以弧度为输入的正弦、余弦函数，输出无量纲 |

f=0.25 Hz时，T=4 s、ω=π/2 rad·s⁻¹。t=0时sin0=0、cos0=1，应变0、应变率0.05×π/2≈0.078540 s⁻¹；t=1 s时角度π/2，应变0.05、应变率0。正弦在过零处变化最快、极值处斜率为零，余弦正好描述这一变化率。

应变率描述应变每秒改变多少，它可以从相邻时刻的应变变化除以时间间隔来理解。正弦曲线过零时移动最快，到达最高或最低位置时瞬间停下并转向。余弦函数表达了这个变化率：时间零点的应变为零，应变率却达到约0.07854 s⁻¹；在1 s时应变达到0.05，而应变率为零。导数符号把“局部变化有多快”写成一个可供计算的量，本例使用解析表达式，所以无需通过相邻点近似求导。

交互控件以0至360度表示周期位置，便于把四分之一周期理解为90度。代码计算正弦、余弦时使用弧度，一个完整周期对应2π。把角度乘以π/180就能完成换算。时间仍由周期位置与当前频率共同决定，因此把频率加倍后，同样的90度位置会在原来一半的时间到达。

## 把弹性响应与黏性响应相加

线性弹簧的应力随应变增大，理想黏性阻尼元件的应力则随应变率增大。把这两个元件并联，它们经历相同的变形，总应力由两个分支相加，得到Kelvin–Voigt模型。可以把它想成推动一个同时受到弹簧拉回与黏性阻力作用的把手：离开平衡位置越远，弹簧作用越大；运动越快，黏性作用越大。模型将这两种作用分别写入E与η，便于观察它们怎样改变曲线。

$$
\sigma(t)=E\varepsilon(t)+\eta\dot\varepsilon(t)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | 时刻t的总应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | 弹性模量，本节20 kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | 应变，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 黏度参数，kPa·s |
| ![Formula](https://ml-biomat.com/static/agent-math/08df7049c9da9e9ff155cb79.svg) | 应变率，s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 经过时间，s |

并联元件具有相同应变，总应力为两个分支之和。E乘应变得到kPa，η乘应变率也得到kPa，因而可以相加。η=4 kPa·s、t=0时，总应力=20×0+4×0.078540≈0.314159 kPa；t=1 s时为20×0.05+4×0=1 kPa。模型在当前幅度和频率范围内将E与η视为常数。

本节取E=20 kPa、η=4 kPa·s。时间零点的应变为零，弹性贡献为零，黏性贡献却约为0.31416 kPa。四分之一周期后，应变达到0.05，弹性贡献为1 kPa，而应变率变成零，黏性贡献也为零。因此，应力的最大位置不会恰好与应变最大位置重合。对这个规定应变的模型，应力相对于应变提前约17.44度。联动图能让这种时间关系直接被追踪。

![同一Kelvin–Voigt教学模型的三个投影。颜色一致的标记对应0、90、180、270度四个周期位置；线为解析函数采样，E=20 kPa、η=4 kPa·s、f=0.25 Hz、应变振幅5%。](https://ml-biomat.com/static/tutorials/python-scientific/figures/5e580ffb46416932f7104837.svg?v=5e580ffb4641)

图 2同一Kelvin–Voigt教学模型的三个投影。颜色一致的标记对应0、90、180、270度四个周期位置；线为解析函数采样，E=20 kPa、η=4 kPa·s、f=0.25 Hz、应变振幅5%。

如果横轴放应变、纵轴放应力，整个周期会形成一个闭合环。沿着加载和卸载两段经过同一个应变时，运动方向或速度不同，黏性应力不同，所以两段不重合。η=0时只剩弹性项，环会收缩成一条来回经过的直线。这里的环形来自模型的速度相关响应，图形并没有额外给曲线加入视觉弯曲。

实际材料是否适合这个模型，需要结合加载幅度、时间尺度与实验现象判断。线性模型假设E与η在本次计算中保持常数，应力由两项相加，适合练习小幅响应中的主要关系。若实验出现幅度相关刚度、屈服或多种时间尺度，就需要在模型与数据结构中加入相应机制。交互图首先帮助我们看清当前模型已经包含的关系，并为比较真实曲线提供清楚的坐标与单位。

## 环线围住的面积为什么与耗散有关

力学中的功等于力沿位移的积累。把力除以面积、位移除以原长后，可以写成应力对应变的积分，结果是单位体积所做的功。一个完整周期结束时，理想弹簧恢复到原来的变形状态，储存的弹性能量也回到原值；黏性分支则把输入的机械功耗散掉。在应力—应变图中，这一周期净输入的功对应闭合轨迹所围面积，并保留沿时间前进的积分方向。

$$
W=\oint\sigma\,d\varepsilon=\int_0^T\eta\dot\varepsilon^{\,2}\,dt=\pi\eta\omega\varepsilon_0^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | 每周期单位体积耗散功，kPa；1 kPa=1000 J/m³ |
| ![Formula](https://ml-biomat.com/static/agent-math/f028f6920f65d3c579388781.svg) | 沿完整闭合加载周期，按时间顺序积分 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | 模型应力，kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/0d7e4b3c87f0601fe79d5d06.svg) | 微小应变增量，无量纲，正负保留运动方向 |
| ![Formula](https://ml-biomat.com/static/agent-math/c3042adc312baf37455fff0f.svg) | 从时间0到周期末T累加 |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 周期时长，s |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 黏度参数，kPa·s |
| ![Formula](https://ml-biomat.com/static/agent-math/f89ba6efd1616ab8c8ae4551.svg) | 应变率，s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/df5e63c0caad262849a85d73.svg) | 微小时间间隔，s |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | 角频率，rad·s⁻¹，弧度按无量纲处理 |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | 应变振幅0.05，无量纲 |

弹性项Eε在闭合周期中先储能后返还，净积分为0；黏性项乘以dε=ε̇dt得到ηε̇²dt。把余弦应变率代入后，cos²在一个周期内的平均值为1/2，得到πηωε₀²。η=4、ω=π/2、ε₀=0.05时，W≈0.0493480 kPa=49.3480 J/m³。Pa=N/m²，乘无量纲应变后可写作N·m/m³，说明它是能量密度。

代码用`np.trapezoid(stress, strain)`沿记录顺序累加，把相邻点间的应力平均值乘以应变改变量。这里应变会先增加再减少，所以顺序必须保留；把横坐标排序后再积分，会破坏加载路径。计算时使用无量纲应变0.05，而图上为了易读显示5%。若直接把百分数坐标5代入积分，数值会被放大100倍。显示单位与计算变量之间的区别，在面积或斜率计算中尤其重要。

![左图保持频率0.25 Hz与应变振幅5%，改变η观察环线；右图展示相同振幅下每周期耗散随频率的解析关系。应变轴以百分数显示，能量积分使用无量纲应变。](https://ml-biomat.com/static/tutorials/python-scientific/figures/42a894e1967c3b4ea475826e.svg?v=42a894e1967c)

图 3左图保持频率0.25 Hz与应变振幅5%，改变η观察环线；右图展示相同振幅下每周期耗散随频率的解析关系。应变轴以百分数显示，能量积分使用无量纲应变。

本例每周期的解析耗散能密度约为49.3480 J/m³。361个点连接成的小梯形给出约49.3455 J/m³，相对差约0.00508%。这个小差异来自有限采样对曲线的近似。把黏度加倍或频率加倍，在保持应变振幅不变的条件下，模型的每周期耗散也会加倍。图中同时展示环线形状与频率关系，使面积变化能够与物理参数联系起来。

## Plotly怎样保存一个可追踪的科学图

Plotly的Figure可以分成数据轨迹与布局两部分。轨迹保存横纵坐标、线型、点型和附加数据，布局保存轴标题、面板位置、显示范围与整体尺寸。`go.Scatter`既可以画散点，也可以在`mode='lines'`时按数组顺序连接曲线。这个名字描述的是通用二维坐标轨迹，不要求数据必须来自统计散点实验。本例用三条线轨迹保存三个投影，再用三条点轨迹标出当前选择。

`customdata`为每个图上位置保留附加字段。本例依次存入记录编号、时间、百分数应变和应力，即使一幅图的横轴只使用应变，悬停提示仍能显示该点的时间。`hovertemplate`负责取出字段并格式化：保留几位小数、写出单位、给记录编号加上明确名称。它像实验表上的行标签，让图形从“看起来靠近这里”变成“准确指向这一行记录”。

数据与布局可以序列化成JSON，也就是一种保存字典、列表与数值的通用文本格式。`write_json`保留图形描述，方便以后重新读取或交给网页渲染；`write_html`再把描述与浏览器运行代码组合成可打开的页面。选择`include_plotlyjs=True`时，所需的Plotly浏览器库会嵌入网页，文件较大，却能在没有网络时使用。本节的主程序在运行后生成这份自包含HTML。

点击事件提供当前点的字段，程序据此更新三条高亮点轨迹。我们只替换高亮点的位置，原始三条曲线继续保留。代码里的短JavaScript片段通过`post_script`加入导出网页，负责浏览器中的点击响应；模型计算与完整数组仍由Python产生。这样的分工把物理计算、图形描述和用户操作连接起来，同时让每一部分都有明确职责。

这里还保留了一个可以直接查看的轨迹编号约定：0、1、2号轨迹保存完整曲线，3、4、5号轨迹保存对应高亮点。点击处理把三组只含一个坐标的数组交给这三条点轨迹。同一条记录只有一个时间、一个应变和一个应力，但每个面板取用不同的坐标组合。明确写出这个映射，就能沿着代码检查联动操作。

## 完整程序：计算、导出与点击联动

下面的程序以1度为步长生成一个周期，共361条记录，首末记录对应同一个周期位置。`cycle`函数返回时间、应变、应变率和应力四个数组，随后所有图都从这四个数组产生。代码使用`make_subplots`安排上方大环线与下方两条时间曲线，并对每个坐标轴分别设置量名和单位。这样既能比较总体形状，也能在时间轴上核对相位关系。

程序将NumPy数组转换成普通列表后交给Plotly，`customdata`的每一行与对应坐标点保持同一顺序。初始高亮选择记录45，点击任一曲线上的记录会更新三幅图中的标记。代码最后另外用Matplotlib生成正文中的静态组图，便于导入普通文档；两种图使用相同的解析数据。输出的CSV与JSON也让图上的数值可以在图形之外继续使用。

### 完整Python：周期加载、Plotly三视图和离线联动导出

NumPy生成解析数据，Plotly保存坐标和记录身份，内嵌点击处理让导出的HTML保留联动；Matplotlib生成同源静态图。

```
"""Create a linked-ready Plotly figure for an analytic cyclic viscoelastic response."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

E,AMPLITUDE,FREQUENCY=20.,.05,.25
BLUE,RED,INK='#28658c','#b64a35','#20313e'


def cycle(eta=4.,frequency=FREQUENCY,n=361):
    time=np.linspace(0,1/frequency,n);omega=2*np.pi*frequency
    strain=AMPLITUDE*np.sin(omega*time)
    rate=AMPLITUDE*omega*np.cos(omega*time)
    stress=E*strain+eta*rate
    return time,strain,rate,stress


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'font.size':12,
        'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    time,strain,rate,stress=cycle();eta=4.;omega=2*np.pi*FREQUENCY
    np.savetxt(args.output/'cycle.csv',np.column_stack([time,strain,rate,stress]),delimiter=',',
        header='time_s,strain,strain_rate_per_s,stress_kPa',comments='')
    custom=np.column_stack([np.arange(len(time)),time,strain*100,stress]).tolist()
    plot=make_subplots(rows=2,cols=2,specs=[[{'colspan':2},None],[{},{}]],
        subplot_titles=[tr('应力—应变轨迹','Stress–strain trajectory'),tr('应变随时间变化','Strain over time'),tr('应力随时间变化','Stress over time')],vertical_spacing=.17)
    hover=tr('记录 %{customdata[0]}<br>t=%{customdata[1]:.3f} s<br>应变=%{customdata[2]:.3f}%<br>应力=%{customdata[3]:.4f} kPa<extra></extra>',
             'Record %{customdata[0]}<br>t=%{customdata[1]:.3f} s<br>strain=%{customdata[2]:.3f}%<br>stress=%{customdata[3]:.4f} kPa<extra></extra>')
    for row,col,x,y,color in [(1,1,strain*100,stress,BLUE),(2,1,time,strain*100,BLUE),(2,2,time,stress,RED)]:
        plot.add_trace(go.Scatter(x=x.tolist(),y=y.tolist(),mode='lines',line={'color':color,'width':3},
                        customdata=custom,hovertemplate=hover,showlegend=False),row=row,col=col)
    for row,col,x,y in [(1,1,strain*100,stress),(2,1,time,strain*100),(2,2,time,stress)]:
        plot.add_trace(go.Scatter(x=[float(x[45])],y=[float(y[45])],mode='markers',
            marker={'color':RED,'size':12},customdata=[custom[45]],hovertemplate=hover,
            showlegend=False),row=row,col=col)
    plot.update_xaxes(title_text=tr('应变 / %','Strain / %'),row=1,col=1)
    plot.update_yaxes(title_text=tr('应力 / kPa','Stress / kPa'),row=1,col=1)
    for col in [1,2]:plot.update_xaxes(title_text=tr('时间 / s','Time / s'),row=2,col=col)
    plot.update_yaxes(title_text=tr('应变 / %','Strain / %'),row=2,col=1)
    plot.update_yaxes(title_text=tr('应力 / kPa','Stress / kPa'),row=2,col=2)
    plot.update_layout(template='plotly_white',height=850,font={'size':15},margin={'l':70,'r':30,'t':70,'b':60},
        title=tr('周期加载：同一记录的三种坐标','Cyclic loading: three coordinate views of each record'))
    plot.write_json(args.output/'figure.json')
    linked_click="""
    const graph=document.getElementById('{plot_id}');
    graph.on('plotly_click',event=>{
      const record=event.points[0].customdata;
      if(!record)return;
      Plotly.restyle(graph,{x:[[record[2]],[record[1]],[record[1]]],
        y:[[record[3]],[record[2]],[record[3]]],
        customdata:[[record],[record],[record]]},[3,4,5]);
    });
    """
    plot.write_html(args.output/'interactive.html',include_plotlyjs=True,full_html=True,
                    post_script=linked_click,config={'displaylogo':False,'responsive':True})
    fig,axes=plt.subplot_mosaic([['loop','loop'],['strain','stress']],figsize=(12,9),layout='constrained')
    points=[0,90,180,270]
    axes['loop'].plot(strain*100,stress,color=BLUE,lw=2.5)
    axes['loop'].fill(strain*100,stress,color=BLUE,alpha=.08)
    axes['strain'].plot(time,strain*100,color=BLUE,lw=2);axes['stress'].plot(time,stress,color=RED,lw=2)
    for i in points:
        color=plt.colormaps['viridis'](i/360)
        for key,x,y in [('loop',strain[i]*100,stress[i]),('strain',time[i],strain[i]*100),('stress',time[i],stress[i])]:
            axes[key].scatter([x],[y],color=color,s=45,zorder=5)
            axes[key].annotate(f'{i}°',(x,y),xytext=(8,8),textcoords='offset points',fontsize=10)
    axes['loop'].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('A  闭合轨迹与四个周期位置','A  Closed trajectory and four cycle positions'))
    axes['strain'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('B  输入的形变','B  Imposed deformation'))
    axes['stress'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('C  模型的应力响应','C  Model stress response'))
    for ax in axes.values():ax.grid();ax.margins(.12)
    save(fig,'linked')
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    viscosity_colors=dict(zip([0,2,4,8],plt.colormaps['viridis'](np.linspace(.15,.85,4))))
    for visc,color in viscosity_colors.items():
        tt,eps,rr,sig=cycle(visc);axes[0].plot(eps*100,sig,color=color,lw=2,label=f'η={visc:g} kPa·s')
    axes[0].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('黏性项让加载与卸载分开','Viscosity separates loading and unloading'));axes[0].legend(frameon=False,fontsize=10)
    freq=np.linspace(.05,.5,100)
    for visc in [2,4,8]:
        color=viscosity_colors[visc]
        axes[1].plot(freq,1000*np.pi*visc*2*np.pi*freq*AMPLITUDE**2,color=color,label=f'η={visc:g} kPa·s')
    axes[1].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('每周期耗散能密度 / J·m⁻³','Dissipated energy per cycle / J·m⁻³'),title=tr('相同振幅下，速度改变耗散','At fixed amplitude, speed changes dissipation'));axes[1].legend(frameon=False,fontsize=10)
    for ax in axes:ax.grid()
    save(fig,'dissipation')
    fig,axes=plt.subplots(1,3,figsize=(13,4.6),layout='constrained')
    selected=45
    for ax,x,y,xlabel,ylabel in [(axes[0],time,strain*100,tr('时间 / s','Time / s'),tr('应变 / %','Strain / %')),
          (axes[1],time,stress,tr('时间 / s','Time / s'),tr('应力 / kPa','Stress / kPa')),
          (axes[2],strain*100,stress,tr('应变 / %','Strain / %'),tr('应力 / kPa','Stress / kPa'))]:
        ax.scatter(x[::5],y[::5],s=10,color='#c4cdd3');ax.scatter([x[selected]],[y[selected]],s=65,color=RED,zorder=5)
        ax.set(xlabel=xlabel,ylabel=ylabel);ax.grid();ax.annotate(tr('记录 45','record 45'),(x[selected],y[selected]),xytext=(0,-30),textcoords='offset points',ha='center',color=RED)
    fig.suptitle(tr('PRIM-9（1974）的交互思想：换坐标，保留同一个数据点','PRIM-9 (1974): change coordinates while retaining point identity'),fontsize=14)
    save(fig,'history')
    exact=np.pi*eta*omega*AMPLITUDE**2
    polygon=float(np.trapezoid(stress,strain));zero=cycle(0)
    summary={'versions':{'numpy':np.__version__,'matplotlib':matplotlib.__version__,'plotly':plotly.__version__},
             'n':len(time),'period_s':1/FREQUENCY,'E_kPa':E,'eta_kPa_s':eta,'strain_amplitude':AMPLITUDE,
             'stress_at_phase0_kPa':float(stress[0]),'stress_at_phase90_kPa':float(stress[90]),
             'loop_work_exact_kPa':float(exact),'loop_work_polygon_kPa':polygon,
             'loop_work_exact_J_m3':float(exact*1000),'relative_quadrature_error':float(abs(polygon-exact)/exact),
             'zero_viscosity_work_kPa':float(np.trapezoid(zero[3],zero[1])),
             'phase_lead_deg':float(np.degrees(np.arctan(eta*omega/E))),
             'plotly_traces':len(plot.data)}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

运行后，`cycle.csv`包含361条模型记录，`figure.json`包含六条Plotly轨迹，`interactive.html`可以直接打开并点击查看同一记录的三个位置。`summary.json`给出周期4 s、零相位应力约0.314159 kPa、90度应力1 kPa，以及解析和数值积分的耗散值。η=0的极限检查得到接近数值零的净功，能帮助确认应变顺序与积分符号一致。

底层数组保留的有效数字比悬浮提示显示的更多。把读数格式化到几位小数有助于阅读，原始数值仍然保留给后续计算。若需要把所选记录导入另一项分析，应使用底层数组值，而不是复制已经取舍过的小数标签。显示精度与计算精度分开处理，可以兼顾易读性与数值信息。

## 直接操作：参数变化与记录追踪分开观察

先保持默认参数，用周期位置滑块从0移动到90度。观察应变从零增加到最大值，应力标记同时在环线上前进；同一个位置也出现在两幅时间图中。你还可以点击任一曲线选择记录，或用键盘调整滑块。每次改变当前记录，模型曲线保留，只有追踪位置与读数更新。

### 沿着一个周期追踪材料响应

点击任一曲线或用键盘调整周期位置，三图同步追踪同一记录。参数改变时重新计算完整轨迹；E固定20 kPa，应变振幅固定5%。

把η改成0后，主图收缩为直线，每周期耗散变成零。再恢复η=4 kPa·s，并把频率从0.25 Hz改成0.5 Hz：周期缩短为2 s，应变振幅保持5%，黏性应力增大，环面积也随之增加。这个操作改变的是研究条件，因此三条完整曲线和所有汇总量一起重新计算。为便于不同条件直接比较，应变和应力显示范围保持固定。

悬浮提示用于读取某一记录，坐标缩放用于检查局部形状，参数控件用于重新计算模型，三者各自承担不同任务。重置按钮恢复默认参数与显示范围。如果你把同样的方式用到实测数据中，可以把参数控件换成试样、频率或温度条件选择器，同时保留记录编号与测量时间，让每个图上位置都能回到原始表中的一行。

## 把交互做成一条可核对的阅读路径

设计交互图时，可以从一个具体动作开始：读者点击一个点之后，希望同时知道什么。本例需要知道时间、形变、响应和运动方向，因此三个投影与当前读数足够完成任务。若研究多批样品，可以再加入条件列表与一致的颜色；若研究长时间过程，可以加入选定时间窗，并在总览上保留该窗口的位置。新的控制项应当对应一个新的观察或比较问题。

点数很多时，浏览器的绘制与悬浮查询会变慢，可以对总览采用有规则的抽样、保留峰值的降采样或分层读取。精确统计仍应基于规定的数据范围，并让读者知道显示的是原始点还是简化总览。本节只有361个规则模型点，完整保留它们即可。对不规则采样，记录编号还应与真实时间分开保存，避免把数组位置误当成等间隔时间。

还需要区分图上的选点与坐标缩放。选点保留一个记录身份，它会在别的坐标系里出现相应位置；缩放只改变当前面板可见的坐标范围。如果读者在一个面板放大了局部，另一个面板仍显示整体，两者各有用处，但所选记录应继续保持一致。研究中常见的矩形范围筛选则是第三种操作：它按当前坐标条件选出一组记录，需要同时更新样本数以及参与统计的范围。

共享数据时，把单位留在列名、图轴与数值解释里，也有助于保持同一含义。这里CSV中的`strain`保存无量纲比例，图上的应变百分数通过乘100得到；`strain_rate_per_s`明确变化率的时间单位，`stress_kPa`明确应力单位。若后续改为Pa，应力数值与黏度参数都要同步换算。保存图形的JSON适合恢复界面，保存物理量的CSV适合继续计算，两个文件因用途不同而互相补充。

最后检查一个熟悉的数值是否能在每个视图中找到：默认条件下0 s对应零应变与0.314159 kPa应力，1 s对应5%应变与1 kPa应力。再检查整个周期的面积是否与解析值接近。单点与整体的两种核对连接了图的局部细节与完整科学含义。交互由此成为读者提出问题、追踪记录和比较条件的工具。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P18.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Plotly: creating and updating figures](https://plotly.com/python/creating-and-updating-figures/)

   轨迹与布局对象

   Plotly.py MIT
2. [Plotly: hover text and formatting](https://plotly.com/python/hover-text-and-formatting/)

   附加字段与带单位的提示

   Plotly.py MIT
3. [Plotly: interactive HTML export](https://plotly.com/python/interactive-html-export/)

   内嵌运行库的离线HTML导出

   Plotly.py MIT
4. [Plotly.js: event handlers](https://plotly.com/javascript/plotlyjs-events/)

   点击事件与点数据

   Plotly.js MIT
5. [Fisherkeller, Friedman & Tukey (1974), PRIM-9](https://www.slac.stanford.edu/pubs/slacpubs/1250/slac-pub-1408.pdf)

   交互投影、坐标筛选与观测身份

   Historical reference; original figures here
6. [NEML2: viscoelasticity](https://applied-material-modeling.github.io/neml2/dev/content/modules/solid_mechanics/viscoelasticity.html)

   并联弹性与黏性元件的应力相加
