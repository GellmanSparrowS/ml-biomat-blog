# Turning Simulation Outputs into Comparable Results

Source: https://ml-biomat.com/tutorials/python-scientific/p30/en/
Language: en

Use an exactly solvable oscillator to align eight trajectories and compare position, energy, accuracy, and update counts.

## When do two trajectories represent a fair comparison?

A simulation often produces hundreds or thousands of rows containing time, position, velocity, and energy. Plotting two curves together is straightforward. The harder questions are whether they describe the same physical interval, whether their differences arise from material parameters or numerical choices, and whether the result settles as the time step decreases. These questions occur in molecular motion, elastic vibration, heat transport, and fluid calculations. This chapter uses a spring oscillator with an exact solution, generates eight output files, and then reads, aligns, and compares them as it would outputs from another simulation package.

The oscillator is a deterministic teaching model: a mass of 1 kg attached to an ideal spring of stiffness 1 N/m, displaced initially by 1 m and released from rest, with no friction or external driving. The positions and velocities are simulated data produced by numerical integration. The model combines repeated motion and energy exchange with an independent analytical solution, allowing physical dynamics and numerical error to be separated. The same comparison structure can later accept tables from a more complex simulator while retaining explicit time coordinates, units, measurement definitions, and checks.

All eight runs share the same initial conditions and final time of 20 s. Only two numerical settings change: forward Euler or velocity Verlet integration, and a step of 0.025, 0.05, 0.1, or 0.2 s. Each CSV stores step index, time, position, and velocity. A smaller step creates more rows, but those rows are denser samples along one computed trajectory. We compare accuracy at 101 common physical times so that different file lengths do not change the weighting of the average error.

## Understanding motion from the direction of the spring force

Choose the equilibrium position as zero and the rightward direction as positive. When the mass is pulled right, the spring pulls left; when the mass moves left of equilibrium, the spring pulls right. This restoring force always points toward equilibrium. For an ideal spring, force is proportional to displacement, so a larger displacement produces a larger restoring force. Newton’s second law connects force to acceleration. Knowing position therefore gives acceleration, from which a numerical method advances position and velocity.

$$
F=-kx,\qquad a=\frac{F}{m},\qquad \omega=\sqrt{\frac{k}{m}},\qquad x_{\rm exact}(t)=A\cos(\omega t),\qquad v_{\rm exact}(t)=-A\omega\sin(\omega t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | spring restoring force, N |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | spring stiffness, N/m; 1 N/m here |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | displacement from equilibrium, m |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | acceleration, m/s² |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | mass, kg; 1 kg here |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | angular frequency, rad/s; radians are dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | initial displacement amplitude, m; 1 m here |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | physical time, s |
| ![Formula](https://ml-biomat.com/static/agent-math/38691bf7f7eb638d9ad5ea26.svg) | analytical position and velocity, m and m/s respectively; initial velocity is zero |
| ![Formula](https://ml-biomat.com/static/agent-math/93fd67f8da8bc15f77fd04df.svg) | cosine and sine; arguments are in radians, function values dimensionless |

The minus sign directs force opposite displacement. Force divided by mass gives acceleration. A second time derivative of cosine supplies −ω²; choosing ω²=k/m satisfies the motion relation. At t=1 s here, position is cos(1)≈0.540302 m, velocity −sin(1)≈−0.841471 m/s, force approximately −0.540302 N, and acceleration approximately −0.540302 m/s². The solution assumes an ideal spring without friction or driving.

Cosine and sine can be understood as projections of motion around a circle. As the angle increases steadily, one projection decreases from its maximum while the other begins changing from zero. These functions describe the position and velocity of an oscillator released from rest. Angular frequency ω controls the pace, and the period is the time required for a full cycle. Here ω=1 rad/s, giving a period of approximately 6.283 s; the 20 s interval contains slightly more than three cycles. NumPy’s trigonometric functions take radians, so numerical angles in degrees require conversion first.

The analytical reference supplies position and velocity at any physical time. We therefore do not need to declare one very-small-step calculation exact. At time zero, position is 1 m and velocity is zero. After about a quarter period, the mass passes through equilibrium with its greatest leftward speed. The program evaluates the analytical position directly at the common time grid and subtracts it from corresponding simulation values. Each error then has a precise definition: the discrepancy between a specified numerical integrator and the exact motion of this same ideal oscillator.

## How the same force produces different numerical trajectories

Forward Euler advances using information from the current time. Current velocity estimates the position increment, and current acceleration estimates the velocity increment. It resembles taking a short straight step along a curved road using the present direction, then reassessing the direction at the next step. The rule is easy to understand and useful for checking update order. Both new variables must use values from the same old state. Overwriting position first and then using that new position in the velocity update defines another algorithm, with different expected behavior.

$$
x_{n+1}=x_n+h v_n,\qquad v_{n+1}=v_n+h a_n,\qquad a_n=-\frac{kx_n}{m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | dimensionless integer integration-step index |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | positive time step, s |
| ![Formula](https://ml-biomat.com/static/agent-math/8db5b3541f45a9fecfa6bd7d.svg) | current and next displacement, m |
| ![Formula](https://ml-biomat.com/static/agent-math/7767393d1a751e86f1bb995c.svg) | current and next velocity, m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/35c129770db807490a096310.svg) | acceleration at the current position, m/s² |
| ![Formula](https://ml-biomat.com/static/agent-math/7850be60bb48378ac7367cc8.svg) | spring stiffness in N/m and mass in kg |

Approximate velocity and acceleration over a short interval by their current values. Multiplying a rate by elapsed time gives its increment. With x₀=1 m, v₀=0, a₀=−1 m/s², and h=0.1 s, x₁=1 m and v₁=−0.1 m/s. Both updates use the old state; overwriting it changes the algorithm.

For this frictionless oscillator, forward Euler gradually increases numerical energy. The first 0.1 s step shows why: position stays at 1 m while velocity becomes −0.1 m/s. Spring energy has not decreased, yet kinetic energy has appeared. Substituting a general Euler step into the energy expression shows that each step multiplies energy by one plus the square of angular frequency times step size. Here that factor is 1.01. After 200 steps, energy is approximately 7.316 times its initial value. This predicts the growing amplitude without interpreting it as a material that spontaneously excites itself.

Velocity Verlet instead divides an update symmetrically. It advances velocity by half a step using acceleration at the old position, advances position by a full step using that intermediate velocity, and completes the remaining half velocity step using acceleration at the new position. The velocity formulation discussed by Swope and colleagues in their 1982 molecular-cluster study allows position and velocity to be stored at the same time. Ordinary time integration in LAMMPS also uses this form of update. Reducing a molecular system to one oscillator makes the individual operations directly visible.

$$
v_{n+1/2}=v_n+\frac{h}{2}a_n,\qquad x_{n+1}=x_n+h v_{n+1/2},\qquad v_{n+1}=v_{n+1/2}+\frac{h}{2}a_{n+1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e11d2c669fc940d6bc996598.svg) | dimensionless step index and step h in s |
| ![Formula](https://ml-biomat.com/static/agent-math/cd3c6f6a10ac62197d9843a2.svg) | current, intermediate half-step, and next full-step velocities, m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/8db5b3541f45a9fecfa6bd7d.svg) | current and next displacement, m |
| ![Formula](https://ml-biomat.com/static/agent-math/b230218f9e8d2fff4e3df1d8.svg) | accelerations −kx/m at old and new positions, m/s² |

The two half velocity updates use accelerations before and after the position change, forming a symmetric sequence. With h=0.1 s, the half velocity is −0.05 m/s and the new position is 0.995 m. The new acceleration is −0.995 m/s², giving final velocity −0.05−0.05×0.995=−0.09975 m/s.

![Complete phase-space trajectories and the three actual operations in the first velocity-Verlet step. Position and velocity are different state coordinates; the lower-right values follow directly from that step.](https://ml-biomat.com/static/tutorials/python-scientific/figures/c63104b97cfb67db0997a6e6.svg?v=c63104b97cfb)

Figure 1Complete phase-space trajectories and the three actual operations in the first velocity-Verlet step. Position and velocity are different state coordinates; the lower-right values follow directly from that step.

The upper-right view plots position horizontally and velocity vertically. Its first step consists of two vertical movements and one horizontal movement. A vertical segment changes velocity while holding position fixed; the horizontal segment updates position using the intermediate velocity. This is a state-space diagram, rather than the physical path of an object through a two-dimensional room. The left view shows complete trajectories over 20 s: the exact solution follows a closed orbit, Euler spirals outward, and velocity Verlet remains nearby. Together the views connect the update sequence with its accumulated behavior.

## Comparing physical time instead of row number

Consider comparing row 101 of two files. With a 0.025 s step, the run has reached 2.5 s; with a 0.2 s step, it has reached 20 s. Even perfectly accurate results would usually differ because they describe different phases of motion. Time alignment must therefore start by defining a comparison interval and target times. Here the targets extend from zero to 20 s in 0.2 s increments, including the initial instant for 101 samples. Each chosen integration step divides 0.2 s, so every target time has a corresponding recorded state in every run.

The program uses `pandas.merge_asof` to match the nearest time after ensuring increasing time columns. A tolerance of 1×10⁻⁹ s accommodates tiny floating-point and CSV round-trip differences and is far smaller than the shortest step of 0.025 s. Both requested `time_s` and actual `matched_time_s` are retained, and every target must find a match. The largest mismatch is approximately 3.55×10⁻¹⁵ s, consistent with rounding. The comparison is consequently between the intended common nodes, rather than between physically different neighboring instants.

Real simulation outputs may not share exact sampling nodes. In that case, specify an interpolation method and consider its error alongside integration error. Linear interpolation can suit smooth, sufficiently sampled intervals. Across a collision, phase change, or sudden loading event, a straight segment can erase important behavior. Other options include a coarser common grid supported by all outputs or comparison of statistics over common time windows. The research question determines the appropriate choice; a successful table join alone does not establish a meaningful physical comparison.

![Position, common-time error, and energy for the same 0.1 s step and 20 s interval; the lower right panel enlarges the small Verlet energy variation.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ad9c551e91d4d2df29f12233.svg?v=ad9c551e91d4)

Figure 2Position, common-time error, and energy for the same 0.1 s step and 20 s interval; the lower right panel enlarges the small Verlet energy variation.

The figure compares the two methods at a common step of 0.1 s. Its second panel evaluates position error at the same 101 times, and its third compares energy relative to the initial value. The lower right panel enlarges the small velocity-Verlet energy error, revealing its oscillation. A single broad vertical range would compress this small variation into an apparently flat line. The enlarged view preserves the large difference between methods while also showing the magnitude of the smaller error.

## The complete program: write outputs, then analyze the outputs

The full entry point appears below. Running it creates eight original simulation tables in `trajectories`, with method and step in each filename. Each `-aligned.csv` stores matched values at the common times, analytical positions, and errors. `comparison.csv` collects the step count, position error, and energy discrepancy for each run. Filenames identify a run, while units in column names explain its values. These conventions keep both the identity of an output and the meaning of its calculations visible.

### Run the complete comparison

Use zh for Chinese figures.

```
python main.py --output results --language en
```

### Generate, reread, and compare eight simulation outputs

Dynamics, energy evaluation, time alignment, and plotting are all included.

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

`simulate` implements the dynamical updates. It constructs time from integer step indices multiplied by the step, avoiding additional drift from repeatedly accumulating time inside the loop. It writes positions and velocities to CSV; `read_and_compare` then reads those files back and checks increasing unique times and finite values. Reading back makes the analysis pass through a real data interface. When replacing these files with another simulator’s outputs, the reader and column mapping are the main pieces to adapt; energy evaluation, common-time comparison, and plotting can retain their roles.

The integrator explicitly preserves old states through array indices. Euler updates both quantities from the old state, while Verlet performs its three ordered operations. Assertions check the hand-calculable first Verlet step, position 0.995 m and velocity −0.09975 m/s, and compare Euler’s final energy with the independently derived per-step growth factor applied 200 times. The first check targets a local update, and the second covers the complete integration interval. Comparison with the analytical positions then exposes accumulated trajectory error.

## What energy, trajectory error, and work each tell us

The ideal oscillator’s energy combines kinetic and spring potential energy. Near equilibrium, the mass moves quickly while spring deformation is small, so kinetic energy dominates. Near maximum displacement, speed approaches zero and deformation is greatest, so potential energy dominates. Energy transfers between these forms while their sum remains 0.5 J. For this closed, frictionless model, energy change is therefore a useful numerical diagnostic. Models with a heat bath, damping, or external driving require their corresponding energy transfers to be included in the accounting.

$$
E=\frac12 m v^2+\frac12 k x^2,\qquad \delta_E=\frac{E-E_0}{E_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f4b96d945f47e589ed760ae0.svg) | current and initial mechanical energy, J |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | mass, kg |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | velocity, m/s |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | spring stiffness, N/m |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | displacement, m |
| ![Formula](https://ml-biomat.com/static/agent-math/ba6eaac03ca3b5b78c70ae6d.svg) | relative energy error, dimensionless; multiply by 100 for percent |

Kinetic energy is half mass times squared velocity. Stretching a linear spring from zero to x requires average force kx/2 times distance x, giving kx²/2. Initial energy here is 0.5 J. After the first Verlet step, x=0.995 m and v=−0.09975 m/s give kinetic energy 0.00497503125 J, potential energy 0.4950125 J, total 0.49998753125 J, and relative error −0.0000249375, or −0.00249375%.

Nearly constant energy does not guarantee an accurate phase of motion. Two metronomes may keep equal amplitudes while one has a slightly shorter period; after many cycles their positions differ substantially. A numerical trajectory can accumulate a similar phase error. We therefore also calculate root-mean-square position error at shared physical times: square position differences, average them, and take the square root. Larger discrepancies contribute more, and the square root restores metres after the squaring operation produced square metres.

$$
\mathrm{RMSE}_x=\sqrt{\frac1M\sum_{j=1}^{M}\left[x_{\rm num}(t_j)-x_{\rm exact}(t_j)\right]^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/17f0ca443d34a5ce2ca2b438.svg) | root-mean-square position error, m |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | number of common sampling times, 101 here, dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | dimensionless common-sample index |
| ![Formula](https://ml-biomat.com/static/agent-math/f16686b4a72a5e1ab569f6d6.svg) | common physical time j, s |
| ![Formula](https://ml-biomat.com/static/agent-math/6fe6f6e5934f0e34a0f210b4.svg) | numerical and analytical positions at the same time, m |

Subtract positions at matching times, square the differences, average, and take a square root. In a two-point illustration with errors 0.01 m and −0.02 m, the mean square is (0.0001+0.0004)/2=0.00025 m² and RMSE≈0.015811 m. Verlet at 0.1 s gives approximately 0.00334304 m over this chapter’s 101 common times. Sharing the grid keeps the averages tied to the same interval.

At a 0.1 s step, the Euler RMS position error is approximately 0.63599 m, compared with 0.0033430 m for velocity Verlet. Halving the Verlet step to 0.05 s gives approximately 0.00083488 m; halving it again to 0.025 s gives approximately 0.00020867 m. Each halving reduces error by close to a factor of four, displaying second-order convergence over this fixed interval. The second-order guide in the figure shows a slope proportional to step squared and is anchored at the smallest-step result; it is not another fitted data series.

![Errors from eight actual integrations at 101 shared physical times, related to step size and update count. The dotted line is a second-order slope guide.](https://ml-biomat.com/static/tutorials/python-scientific/figures/317c630c9d98ecddea1b1cde.svg?v=317c630c9d98)

Figure 3Errors from eight actual integrations at 101 shared physical times, related to step size and update count. The dotted line is a second-order slope guide.

A smaller step also requires more updates. Over 20 s, a 0.2 s step requires 100 updates, while a 0.025 s step requires 800. The right panel connects this work count with accuracy. Step count is distinct from measured runtime: operation counts per step, implementation, and hardware affect elapsed time. A performance claim would require measurements using the methods in [timing and memory analysis](https://ml-biomat.com/tutorials/python-scientific/p28/en/). Here the direct comparison concerns the number of updates and position accuracy obtained for a particular oscillator, interval, and error definition.

## Following position, phase space, and energy together

The experiment below presents one instant in several synchronized views. A position diagram shows displacement from equilibrium. A vertical line marks the same instant on the position–time curve, a point marks position and velocity in phase space, and an energy bar separates kinetic and potential contributions. Changing the method or step preserves the selected common 0.2 s observation time. You can therefore track the same physical instant across different numerical choices.

### Compare states at one physical instant

[Figure: Current displacement and exact reference](https://ml-biomat.com/tutorials/python-scientific/p30/en/#P30-position)

[Figure: Position versus time](https://ml-biomat.com/tutorials/python-scientific/p30/en/#P30-timeplot)

[Figure: Position–velocity phase space](https://ml-biomat.com/tutorials/python-scientific/p30/en/#P30-phase)

[Figure: Kinetic and potential energy with the initial-energy reference](https://ml-biomat.com/tutorials/python-scientific/p30/en/#P30-energy)

Begin with Verlet at 0.1 s and move to approximately 1.6 s. The mass is passing near equilibrium, position is near zero, speed is near its maximum, and kinetic energy occupies most of the bar. Near 3.2 s the mass approaches the opposite extreme, its speed decreases, and potential energy again dominates. At 20 s, switch to Euler and observe how position and velocity depart together from the analytical reference while total energy increases. Each state comes from the complete Python trajectory output; the page reads saved values and synchronizes the views.

Next compare Verlet steps of 0.2 and 0.025 s, watching energy and phase improve in different ways. For this harmonic oscillator, linear stability of velocity Verlet requires the product of angular frequency and step size to be less than two; all selected steps meet that condition. Stability means that this linear update does not produce unbounded amplification. Accuracy still needs to be assessed from the error curves. A stable step can remain too coarse for a desired measurement, which is why the convergence comparison uses several steps.

## Carrying the comparison into a larger simulation project

For research outputs, begin with a run inventory recording physical model, initial conditions, boundary conditions, numerical method, step, total time, and output interval. A step-size comparison for one physical problem keeps physical conditions fixed. If the question concerns a material parameter, first establish sufficiently small numerical error through convergence checks, then make that parameter the primary difference. Each curve in a comparison can then be connected to a precise question, and a reader can understand why the runs belong together.

With an analytical solution, compare trajectories at common times as done here. Without one, refine temporal or spatial resolution and examine conserved quantities, key statistics, and agreement between numerical approaches. Molecular systems additionally require periodic-boundary handling, translation and rotation alignment, and temporal correlation; [the trajectory analysis topic](https://ml-biomat.com/tutorials/python-scientific/s06/en/) connects those operations to molecular data. Field outputs benefit from [labeled multidimensional arrays](https://ml-biomat.com/tutorials/python-scientific/s03/en/) that retain time, spatial coordinates, and physical quantities without relying on unnamed array axes.

The completed example contains eight trajectories, eight alignment tables, and one comparison table. Position and velocity can be followed into energy, error, and work counts. Over the specified 20 s oscillator interval, velocity Verlet improves position accuracy by close to a factor of four when the step is halved, while maintaining a small bounded energy error. Larger projects can preserve this structure: make outputs interpretable first, then compare them under shared physical conditions and explicit measurement definitions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P30.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pandas merge_asof](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html)

   Matching by time distance, sorting, and explicit tolerance.

   pandas BSD-3-Clause; official documentation.
2. [LAMMPS fix nve](https://docs.lammps.org/fix_nve.html)

   Velocity form of Verlet time integration.

   Official technical reference.
3. [LAMMPS: How a timestep works](https://docs.lammps.org/Developer_flow.html)

   Ordering of position, half velocity, and force updates.

   Official technical reference.
4. [Swope et al. (1982), A computer simulation method for the calculation of equilibrium constants for the formation of physical clusters of molecules](https://doi.org/10.1063/1.442716)

   Historical connection between velocity Verlet and molecular-cluster simulation.

   Scientific historical citation; diagrams and teaching simulations are original.
