# Figures That Respond: Linked Scientific Data with Plotly

Source: https://ml-biomat.com/tutorials/python-scientific/p18/en/
Language: en

Follow one cyclic-loading record through time views and a stress–strain trajectory, connecting phase and dissipation.

## Follow one instant through three connected figures

Squeeze a cushion or repeatedly stretch a soft strip and the force you feel can depend on both how far and how quickly it moves. An instrument records that process as time, deformation, and force. Drawing separate plots is straightforward. A useful interaction goes further: select one position in a plot, and the other views identify the same record, showing its deformation, motion direction, and stress together. This chapter uses Plotly to build that connected reading experience and save a complete figure as an HTML file that works offline.

A fully specified cyclic-loading model supplies scientific curves and several key instants that can be checked by hand. We will explain strain, stress, and rate of change before arranging them as Plotly traces, layout properties, and hover fields. Point tracking and parameter controls then let readers inspect records and compare conditions. The complete Python program produces a numerical table, a figure-description file, and a self-contained interactive webpage. The experiment embedded in this chapter is directly usable.

Plotly retains the data identity behind graphical elements in a browser. A static image stores visible shapes; an interactive figure also retains coordinate arrays and additional fields. Hovering can retrieve the time and quantities associated with a point, and clicking can use one record identifier to update several views. This capability depends on clear data organization: each graphical position needs an unambiguous relationship to a record.

## Early interactive graphics: change the view and retain the point

In their 1974 PRIM-9 report, Mary Anne Fisherkeller, Jerome Friedman, and John Tukey described an interactive system for exploring point sets with up to nine variables. Users could change two-dimensional projections, rotate their view, and isolate observations for further examination. The scientific value came from actively changing the view to find structures that static summaries could conceal. The report distinguished filtering by the current coordinate region from retaining the identities of selected points: after a rotation, these operations can preserve different observations.

![Retaining observation identity while changing projections, following a distinction in PRIM-9. Record 45 is red in all three coordinate combinations; gray points show every fifth record to clarify its position.](https://ml-biomat.com/static/tutorials/python-scientific/figures/5155ca9ec384f191b8be5ce1.svg?v=5155ca9ec384)

Figure 1Retaining observation identity while changing projections, following a distinction in PRIM-9. Record 45 is red in all three coordinate combinations; gray points show every fifth record to clarify its position.

Our example has only three variables, so time–strain, time–stress, and strain–stress already provide three informative coordinate projections. Record 45 occupies different positions in the three panels while retaining its identity. It corresponds to 0.5 s, approximately 3.536% strain, and approximately 0.9293 kPa stress. Keeping that identity lets a reader move from asking why part of the loop occupies a particular position to examining what the imposed deformation and response were doing at that instant.

A browser makes this kind of inspection easy to share. Following the distinction between viewpoint and point identity, we give every record an identifier and draw different coordinate combinations. Changing a physical parameter recalculates the complete model trajectory; selecting an instant changes the position being tracked. These controls give condition changes and inspection of existing results distinct, visible roles.

## Turn the stretching motion into computable quantities

Strain is the change in length divided by the original length. A specimen initially 100 mm long that lengthens by 5 mm has strain 0.05, also written 5%. It is dimensionless because the millimeters cancel. Stress divides force by loaded area, allowing comparison between differently sized specimens. We express stress in kPa. Positive and negative values represent opposite loading directions around an equilibrium position in an ideal linear model of small cyclic motion.

The imposed strain moves smoothly back and forth: it starts at zero, reaches a positive maximum, passes through zero to a negative maximum, and returns to its starting position. A sine function describes this periodic motion. A frequency of 0.25 Hz means one quarter of a cycle per second, giving a period of 4 s. A strain amplitude of 0.05 gives maximum extension and contraction of 5%. Angular frequency converts elapsed time into the radians required to describe one full cycle in a trigonometric function.

$$
\varepsilon(t)=\varepsilon_0\sin(\omega t),\qquad \dot\varepsilon(t)=\varepsilon_0\omega\cos(\omega t),\qquad \omega=2\pi f,\quad T=1/f
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Strain at time t, length change divided by initial length; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Strain amplitude, 0.05 or 5% here; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, s |
| ![Formula](https://ml-biomat.com/static/agent-math/08df7049c9da9e9ff155cb79.svg) | Rate of strain change; the dot denotes a time derivative, s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad·s⁻¹; radians are dimensionless in dimensional analysis |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Cycle frequency, Hz=s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Period duration, s |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant approximately 3.141593; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/5bc8e1a5d4bcca693b9f9dcf.svg) | Sine and cosine with radian arguments; dimensionless outputs |

At f=0.25 Hz, T=4 s and ω=π/2 rad·s⁻¹. At t=0, sin0=0 and cos0=1 give strain 0 and strain rate 0.05×π/2≈0.078540 s⁻¹. At t=1 s the angle is π/2, giving strain 0.05 and zero rate. Sine changes fastest at zero crossings and has zero slope at extrema; cosine describes that rate.

Strain rate measures how much strain changes per second. It can be understood from a change in strain divided by the short time interval over which that change occurs. A sine curve moves fastest when it crosses zero, then momentarily stops and reverses at its maximum and minimum. A cosine describes that rate: at time zero, strain is zero but strain rate is approximately 0.07854 s⁻¹; at 1 s, strain reaches 0.05 and strain rate is zero. The derivative symbol records this local speed of change. Our model provides its exact expression, so adjacent samples are not needed to estimate it.

The interactive control uses cycle positions from 0 to 360 degrees, making a quarter-cycle easy to recognize as 90 degrees. Sine and cosine in the calculation use radians, with a complete cycle corresponding to 2π. Multiplying degrees by π/180 performs the conversion. Elapsed time depends on both cycle position and frequency, so doubling frequency reaches the same 90-degree position in half the time.

## Add elastic and viscous contributions

A linear spring produces stress proportional to strain, while an ideal viscous element produces stress proportional to strain rate. Connecting them in parallel gives both the same deformation and adds their stresses, producing the Kelvin–Voigt model. Imagine moving a handle that feels both a restoring spring force and a viscous resistance. Greater displacement increases the spring contribution, while faster movement increases the viscous contribution. Separate coefficients E and η make the effects of these two mechanisms inspectable.

$$
\sigma(t)=E\varepsilon(t)+\eta\dot\varepsilon(t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | Total stress at time t, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Elastic modulus, 20 kPa here |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Strain; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Viscosity parameter, kPa·s |
| ![Formula](https://ml-biomat.com/static/agent-math/08df7049c9da9e9ff155cb79.svg) | Strain rate, s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, s |

Parallel elements share strain and add their stresses. E times strain has units kPa, as does η times strain rate. With η=4 kPa·s at t=0, total stress is 20×0+4×0.078540≈0.314159 kPa. At t=1 s it is 20×0.05+4×0=1 kPa. E and η are treated as constants within the modeled amplitude and frequency range.

Here E = 20 kPa and η = 4 kPa·s. At time zero, strain and the elastic contribution are zero, while the viscous contribution is approximately 0.31416 kPa. A quarter-cycle later, strain reaches 0.05, producing 1 kPa of elastic stress, while the zero strain rate makes the viscous contribution vanish. The stress maximum therefore occurs at a different position from the strain maximum. For this strain-controlled model, stress leads strain by approximately 17.44 degrees. Linked views let readers track that timing relationship directly.

![Three projections of the same Kelvin–Voigt teaching model. Matching colors mark cycle positions 0, 90, 180, and 270 degrees; lines sample the analytic functions. E = 20 kPa, η = 4 kPa·s, f = 0.25 Hz, and strain amplitude is 5%.](https://ml-biomat.com/static/tutorials/python-scientific/figures/791cad76ce84ccac1a2193af.svg?v=791cad76ce84)

Figure 2Three projections of the same Kelvin–Voigt teaching model. Matching colors mark cycle positions 0, 90, 180, and 270 degrees; lines sample the analytic functions. E = 20 kPa, η = 4 kPa·s, f = 0.25 Hz, and strain amplitude is 5%.

Putting strain horizontally and stress vertically produces a closed trajectory over one cycle. Loading and unloading pass through the same strain at different velocities or motion directions, so their viscous stresses differ and the paths separate. Setting η to zero leaves only the elastic term, collapsing the loop to a straight line traversed in both directions. The loop arises from the specified rate-dependent response of the model.

Applying the model to a real material requires considering loading amplitude, time scale, and measured behavior. The linear model keeps E and η constant throughout the calculation and adds the two stress contributions. It offers a clear description of the principal relationships in a small-amplitude response. Amplitude-dependent stiffness, yielding, or several relaxation scales call for corresponding mechanisms in the model. The interactive figure exposes the relationships already present in this model and supplies explicit coordinates and units for later comparison with measurements.

## Why the loop area is related to dissipation

Mechanical work accumulates force along displacement. Dividing force by area and displacement by the original length gives an integral of stress with respect to strain, representing work per unit volume. At the end of a complete cycle, an ideal spring returns to its original deformation and stored elastic energy. The viscous branch dissipates the mechanical work supplied to it. In the stress–strain diagram, net work over the cycle corresponds to the enclosed trajectory area, with the time-ordered direction retained in the integral.

$$
W=\oint\sigma\,d\varepsilon=\int_0^T\eta\dot\varepsilon^{\,2}\,dt=\pi\eta\omega\varepsilon_0^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | Dissipated work per unit volume per cycle, kPa; 1 kPa=1000 J/m³ |
| ![Formula](https://ml-biomat.com/static/agent-math/f028f6920f65d3c579388781.svg) | Integral around a complete closed loading cycle in time order |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Model stress, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/0d7e4b3c87f0601fe79d5d06.svg) | Small strain increment; dimensionless, with sign retaining motion direction |
| ![Formula](https://ml-biomat.com/static/agent-math/c3042adc312baf37455fff0f.svg) | Accumulate from time 0 to the end of the period T |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Period duration, s |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Viscosity parameter, kPa·s |
| ![Formula](https://ml-biomat.com/static/agent-math/f89ba6efd1616ab8c8ae4551.svg) | Strain rate, s⁻¹ |
| ![Formula](https://ml-biomat.com/static/agent-math/df5e63c0caad262849a85d73.svg) | Small time interval, s |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad·s⁻¹, treating radians as dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Strain amplitude 0.05; dimensionless |

The elastic term Eε stores and returns energy over a closed cycle, giving zero net integral. Multiplying the viscous term by dε=ε̇dt gives ηε̇²dt. Substitution of the cosine strain rate uses the cycle-average of cos², one half, yielding πηωε₀². For η=4, ω=π/2, and ε₀=0.05, W≈0.0493480 kPa=49.3480 J/m³. Pa=N/m² can also be written N·m/m³, identifying energy per volume.

The code uses `np.trapezoid(stress, strain)` to add the mean stress between adjacent records multiplied by the strain increment. Strain first increases and then decreases, so record order matters. Sorting the horizontal coordinates before integrating would destroy the loading path. The calculation uses dimensionless strain 0.05, while the displayed axis uses 5% for readability. Integrating directly against the percentage value 5 would increase the result by a factor of one hundred. Distinguishing displayed units from calculation variables becomes especially important for areas and slopes.

![Left: change η at a fixed frequency of 0.25 Hz and strain amplitude of 5%. Right: analytic dissipated energy per cycle versus frequency at the same amplitude. Displayed strain is percent; integration uses dimensionless strain.](https://ml-biomat.com/static/tutorials/python-scientific/figures/dd398ffc6372ca4cb30ea36e.svg?v=dd398ffc6372)

Figure 3Left: change η at a fixed frequency of 0.25 Hz and strain amplitude of 5%. Right: analytic dissipated energy per cycle versus frequency at the same amplitude. Displayed strain is percent; integration uses dimensionless strain.

The exact dissipated energy density per cycle is approximately 49.3480 J/m³. Trapezoids connecting 361 points give approximately 49.3455 J/m³, a relative difference of about 0.00508%. This difference comes from representing a smooth curve with finite samples. At fixed strain amplitude, doubling viscosity or frequency doubles the model’s dissipated energy per cycle. The figure connects the evolving loop shape to the frequency dependence, making area changes interpretable in terms of physical parameters.

## How Plotly stores a traceable scientific figure

A Plotly Figure contains data traces and layout properties. Traces retain coordinates, line and marker styles, and additional data. Layout properties define axis titles, panel positions, ranges, and overall dimensions. `go.Scatter` can display points or connect coordinates in array order with `mode='lines'`. Its name identifies a general two-dimensional trace, so it also suits the smooth model trajectory here. We use three line traces for the three projections and three marker traces for the current selection.

`customdata` stores additional fields for every plotted position. Its columns here are record identifier, time, percentage strain, and stress. A panel that uses strain as its horizontal coordinate can still reveal time in a hover label. `hovertemplate` selects these fields and formats their presentation: decimal precision, unit labels, and an explicit record name. It acts like a row label in an experimental table, turning an approximate visual position into an identifiable record.

Data and layout can be serialized as JSON, a general text format for dictionaries, lists, and values. `write_json` saves a figure description that can be loaded later or rendered in a webpage. `write_html` combines the description with browser code to create an openable page. With `include_plotlyjs=True`, the required browser library is embedded in the file. The larger file then works without an internet connection. Running this chapter’s Python program produces that self-contained HTML export.

A click event supplies the fields associated with the selected point. The event handler updates the three highlight-marker traces while retaining the original trajectories. A short JavaScript block enters the exported page through `post_script` and handles browser clicks. Python supplies the physical calculation and complete arrays. This division connects numerical calculation, figure description, and user interaction while giving each a definite responsibility.

The update also depends on a small indexing convention worth reading carefully. Trace indices 0, 1, and 2 contain the full paths, while indices 3, 4, and 5 contain the corresponding highlights. The click handler passes three one-element coordinate arrays to those marker traces. A record has one time, one strain, and one stress, but each panel uses a different pair. Keeping the mapping explicit makes it possible to inspect the handler without treating interaction as a hidden feature of the plotting library.

## A complete program: calculate, export, and link clicks

The program samples a cycle at one-degree intervals, producing 361 records with the first and last positions coincident. The `cycle` function returns arrays for time, strain, strain rate, and stress, and every figure derives from those arrays. `make_subplots` arranges a large upper trajectory and two lower time views, with quantity names and units assigned to each axis. The layout supports both inspection of the overall loop and verification of its phase relationship.

NumPy arrays are converted to ordinary lists before being passed to Plotly. Each row of `customdata` retains the same ordering as its coordinate point. Record 45 is highlighted initially; clicking a record on any curve updates all three markers. Matplotlib additionally generates the static figures used in the chapter, making the same results convenient for ordinary documents. Both plotting systems use the same analytic data, and the CSV and JSON outputs preserve their numerical content beyond the visible figure.

### Complete Python: cyclic loading, three Plotly views, and linked offline export

NumPy generates analytic data, Plotly retains coordinates and record identity, and an embedded click handler links the offline export. Matplotlib produces static views of the same values.

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

After running, `cycle.csv` contains 361 model records, `figure.json` contains six Plotly traces, and `interactive.html` opens directly for click-based tracking. `summary.json` reports a 4 s period, approximately 0.314159 kPa stress at zero phase, 1 kPa at 90 degrees, and the analytic and polygon-integrated work values. The η = 0 limiting calculation returns net work close to numerical zero, helping check strain ordering and the sign of integration.

The stored numerical values retain more digits than the hover text displays. Formatting a label to four decimal places improves reading while leaving the original array available for calculations. If you later export selected records to another analysis, use those underlying values rather than copying rounded labels. This distinction lets the interface remain readable without discarding information from the computational result.

## Separate condition changes from record tracking

Keep the default parameters and move the cycle-position slider from zero to 90 degrees. Strain increases to its maximum while the stress marker advances along the loop; the corresponding positions appear in both time panels. You can also click a curve to select a record or adjust the slider with the keyboard. Selecting an instant retains the model curves and updates the tracked positions and readout.

### Track the response through one cycle

Click any curve or adjust cycle position with the keyboard to track one record across all views. Parameter changes recalculate the complete trajectory; E stays at 20 kPa and strain amplitude stays at 5%.

Set η to zero. The main trajectory contracts to a line and the energy dissipated per cycle becomes zero. Restore η = 4 kPa·s and increase frequency from 0.25 to 0.5 Hz. The period shortens to 2 s while strain amplitude stays at 5%; viscous stress grows and the loop area increases. Changing a model condition therefore recalculates all complete curves and summary quantities. Fixed strain and stress ranges keep those condition comparisons visually direct.

Hover labels retrieve a record, axis zoom examines a local shape, and parameter controls recalculate the model. The reset button restores default parameters and display ranges. For measured data, a specimen, frequency, or temperature selector can replace the model controls while record identifiers and timestamps retain the route from a graphical point to one original row.

## Make interaction a checkable reading path

Begin an interactive design with one concrete action: after selecting a point, what should a reader learn alongside it? Here the answer includes time, deformation, response, and motion direction, so three projections and a current-value readout serve the task. Multiple specimens may call for a condition list and consistent colors. A long process may need a selected time window whose position remains visible in an overview. Each new control should support an identifiable observation or comparison.

Very large point sets can slow browser drawing and hover queries. A structured sample, an extrema-preserving reduction, or staged loading can make an overview usable. Quantitative summaries should continue to use the stated data range, and readers need to know whether displayed points are original observations or a reduced overview. This example has only 361 regular model points, making complete display practical. For irregular observations, keep record index separate from actual time so array positions are not mistaken for equally spaced measurements.

Point selection and coordinate zoom have different effects. Selection retains a record identity that appears at the corresponding position in other coordinate systems. Zoom changes the visible coordinate range of a panel. One panel may show a detail while another keeps the overview, with both preserving the selected record. Rectangular filtering introduces a third operation: it selects a set of records according to current coordinate conditions. A statistical display using that selection should update its sample count and identify the range contributing to its calculation.

For shared data, retaining units in column names, axes, and numerical explanations helps preserve meaning. The CSV column `strain` stores a dimensionless fraction; the percentage displayed in the figure comes from multiplying by one hundred. `strain_rate_per_s` identifies the time unit of the rate, and `stress_kPa` identifies the stress unit. Converting to Pa would require both stress values and the viscosity parameter to change consistently. The figure JSON restores the graphical interface, while the physical-quantity CSV supports further numerical work. Their different purposes make both useful.

Check a familiar value in every view: under default conditions, 0 s corresponds to zero strain and 0.314159 kPa stress, while 1 s corresponds to 5% strain and 1 kPa stress. Then compare the integrated cycle area with its analytic value. These point-level and whole-cycle checks connect graphical detail with the complete scientific interpretation. Interaction becomes a way to ask questions, follow records, and compare conditions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P18.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Plotly: creating and updating figures](https://plotly.com/python/creating-and-updating-figures/)

   Trace and layout objects

   Plotly.py MIT
2. [Plotly: hover text and formatting](https://plotly.com/python/hover-text-and-formatting/)

   Additional fields and unit-aware labels

   Plotly.py MIT
3. [Plotly: interactive HTML export](https://plotly.com/python/interactive-html-export/)

   Offline HTML with embedded runtime

   Plotly.py MIT
4. [Plotly.js: event handlers](https://plotly.com/javascript/plotlyjs-events/)

   Click events and point data

   Plotly.js MIT
5. [Fisherkeller, Friedman & Tukey (1974), PRIM-9](https://www.slac.stanford.edu/pubs/slacpubs/1250/slac-pub-1408.pdf)

   Interactive projections, coordinate masking, and observation identity

   Historical reference; original figures here
6. [NEML2: viscoelasticity](https://applied-material-modeling.github.io/neml2/dev/content/modules/solid_mechanics/viscoelasticity.html)

   Stress addition for parallel elastic and viscous elements
