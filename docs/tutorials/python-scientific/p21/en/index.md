# Describing Change with Integrals and Differential Equations

Source: https://ml-biomat.com/tutorials/python-scientific/p21/en/
Language: en

Use a three-state conversion to understand rates, numerical steps, conservation, and accumulated area.

## When should an intermediate state be observed?

A sample may change from state A to B and then from B to C. A could represent material before conversion, B a temporary intermediate, and C material after a subsequent change. By the end of an experiment, little B may remain. If B is the feature of interest, two useful questions are when it reaches its largest fraction and how long it remains present during the process. These questions concern a curve's peak and its area, bringing differential equations and integration into the same practical problem.

We use a defined teaching model: a fixed total passes through A, B, and C in a one-to-one sequence, with constant volume and conditions, no additional input or output, and no reverse conversion. Each state is described as a fraction of the initial total. Initially A is 1 and both B and C are 0. This setup keeps attention on rates of change. For an actual reaction, the corresponding equations would be built from the species, stoichiometry, volume changes, and measurement definitions.

SciPy's `solve_ivp` computes a trajectory from an initial state and a rule for how that state changes. Its `quad` function accumulates the area beneath a supplied function. We first examine short calculations that can be checked by hand, then run the complete program. A simple model with a known analytic answer makes step size, error, conservation, and integral units concrete rather than leaving them as abstract solver options.

## Rates describe change per minute; the equations record the flows

Suppose the rate at which A becomes B is proportional to the amount of A currently present. More A allows more conversion in the same short interval; as A decreases, its conversion rate also decreases. The first rate constant is 0.8 min⁻¹. When A has a fraction of 0.5, its instantaneous loss rate is 0.4 fraction units per minute. “Instantaneous” matters: this is the direction and speed at that moment, and the speed changes as the state changes.

$$
\frac{da}{dt}=-k_1a,\qquad\frac{db}{dt}=k_1a-k_2b,\qquad\frac{dc}{dt}=k_2b
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/326d9c99fe68c4303977dd55.svg) | Fractions of the initial total in A, B, and C; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/d62ad609310d0b90a08f3cae.svg) | Rate constants for A→B and B→C, respectively 0.8 and 0.3 min⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/cf7a258783fb9a082f6d20a4.svg) | Instantaneous rates of change in the fractions, min⁻¹; d denotes differentiation. |

Each transfer is a current fraction multiplied by a rate constant. For a = 0.5, b = 0.3, and c = 0.2, the rates are −0.4, 0.4 − 0.09 = 0.31, and 0.09 min⁻¹. They sum to zero, so the total stays constant while its composition changes.

The three equations can be read as accounts of incoming and outgoing material. A only loses material, so its rate is negative. B receives material from A and loses material to C, giving an inflow minus an outflow. C receives the second flow. Adding the three rates cancels each transfer against its counterpart, leaving a constant total fraction. The second rate constant is 0.3 min⁻¹. Because removal from B is relatively slow, B accumulates early and later declines as its supply from A becomes smaller.

A derivative can be approached through an average rate. Subtract the fractions at two nearby times and divide by the elapsed time to obtain the average change over that interval. Shrinking the interval leads toward the rate at one time. This resembles the relation between position and velocity: a present position and velocity predict a position a short time later. Here the position is replaced by three fractions, and the velocities are replaced by three coupled rates of transfer.

Normalizing the initial total to 1 amounts to dividing the sample into equal counting units and tracking which state each occupies. The one-to-one conversion preserves their total number. For a chemical reaction with multiple reactants or different stoichiometric coefficients, construct equations for concentrations or amounts and then check the appropriate element or mass balance. Fractions make this example convenient, while the physical process determines what must actually be conserved.

## Advance along the current slope, then calculate it again

In the eighteenth century, Euler organized integration and differential equations into systematic tools for studying change. The first volume of his *Foundations of Integral Calculus* appeared in 1768. A numerical program still addresses the same basic relationship: given a rule for change, recover the quantity that changes with time. The Euler method provides an especially clear geometric construction. Move a short distance along the current slope, then recalculate the slope at the new position.

$$
\mathbf y_{n+1}=\mathbf y_n+h\,\mathbf f(t_n,\mathbf y_n)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f9863792b3128c856f71d728.svg) | State vector at node n, containing dimensionless fractions a, b, and c. |
| ![Formula](https://ml-biomat.com/static/agent-math/794309c181b5d3eef90282ba.svg) | Integer labels of the current and next numerical nodes, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Time step, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/a588fc41a723666b153cc137.svg) | Time at node n, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/a06debad6e153cb789c38ba5.svg) | Rate vector defined by the three preceding equations; each component has units min⁻¹. |

Rate multiplied by time gives the approximate change over one step. Initial state (1, 0, 0), step 0.5 min, and rate (−0.8, 0.8, 0) min⁻¹ produce (0.6, 0.4, 0). The total is 1, while conversion of newly formed B within this coarse step enters only through later updates.

Starting from A = 1, B = 0, and C = 0, the current rates are −0.8, 0.8, and 0 min⁻¹. For a 0.5 min step, multiply each rate by 0.5 and add it to the corresponding starting value. The result is A = 0.6, B = 0.4, and C = 0. This holds the initial rates constant for half a minute. In the continuous model, A begins slowing immediately as it decreases, and newly formed B immediately starts converting to C. The discrete calculation updates these effects at the next node.

![Euler steps connect nodes using their current slopes. Refinement approaches the analytic curve. The right panel independently measures maximum absolute error across all three fractions; the reference line is proportional to step size.](https://ml-biomat.com/static/tutorials/python-scientific/figures/55a7342979f7dcd42434114e.svg?v=55a7342979f7)

Figure 1Euler steps connect nodes using their current slopes. Refinement approaches the analytic curve. The right panel independently measures maximum absolute error across all three fractions; the reference line is proportional to step size.

The coarse polygonal curves depart from the analytic curve, whereas shorter steps approach it. The right panel plots maximum absolute error against step size on logarithmic axes. At small steps, the trend roughly follows a line proportional to step size. This comparison is more informative than the smooth appearance of a single plot. A plotting program can smoothly connect a few points; numerical accuracy is assessed through refinement, an independent answer, or a more stringent solution procedure.

## Let the solver choose its steps; specify the initial state and output times

The program expresses the rate rule in `rhs(t, y)`. Its argument `t` is the current time, while `y` contains the fractions in the order A, B, C. The returned derivatives use the same order. This ordering plays the role of table column names: the initial values, plot labels, and checks must follow it consistently. Although the present rate constants do not depend on time, the interface keeps the time argument so that heating, external inputs, or other time-dependent conditions can be represented.

`solve_ivp` receives the interval from 0 to 10 min and the initial state [1, 0, 0]. Its default RK45 method evaluates rates at several positions during a step and adjusts its internal step size using an error estimate. Here `t_eval` requests results at 501 evenly spaced times for plotting and comparison. These saved times do not require the solver to use a fixed internal step of 0.02 min. An output grid and the algorithm's internal steps serve different purposes.

The settings are `rtol=1e-9` and `atol=1e-11`. Relative tolerance scales with the magnitude of a fraction, whereas absolute tolerance supplies a scale even when a fraction is close to zero. They control estimates of local error, so the final trajectory is also checked directly. Comparing all three computed fractions with their analytic values at every saved time gives a maximum absolute difference of approximately 7.21 × 10⁻¹¹ in this run.

![Three fractions and the B integral for the same sequential model. RK45 produces the left trajectories; the analytic B curve defines the shaded area on the right. Time is in minutes and the initial total is normalized to 1.](https://ml-biomat.com/static/tutorials/python-scientific/figures/414bbb94b67f0f074da41f76.svg?v=414bbb94b67f)

Figure 2Three fractions and the B integral for the same sequential model. RK45 produces the left trajectories; the analytic B curve defines the shaded area on the right. Time is in minutes and the initial total is normalized to 1.

The program also uses the rate of B as an event function, locating where it changes from positive to negative. That zero marks the transition from increasing B to decreasing B, giving a peak time of approximately 1.96166 min. Event detection finds a zero on the continuous numerical solution rather than simply choosing the largest of the 501 stored values. In a new application, an event should correspond to a precise condition, such as a concentration crossing a threshold or a net flow reversing direction.

The analytic solution can also be understood from the flow rules. A loses the same proportion over equal time intervals, giving exponential decay. B receives contributions from A at many different times, and each contribution subsequently decays toward C according to how long it has been in B. Adding these contributions gives a difference of two exponentials. C follows by subtracting A and B from the total. The expression used in the program assumes distinct rate constants, a condition satisfied by every selectable rate in this chapter.

$$
a(t)=e^{-k_1t},\qquad b(t)=\frac{k_1}{k_2-k_1}\left(e^{-k_1t}-e^{-k_2t}\right),\qquad c(t)=1-a(t)-b(t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db3924ef96d9ef424c4cfc5d.svg) | Three dimensionless fractions at time t for initial state (1, 0, 0). |
| ![Formula](https://ml-biomat.com/static/agent-math/dec0f7dc61f0e9a546cd9d6d.svg) | t is time in min; both rate constants have units min⁻¹ and must be distinct for this expression. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, approximately 2.71828. Rate multiplied by time in each exponent is dimensionless. |

At t = 0 both exponentials equal 1, giving a = 1, b = 0, c = 0. At t = 2 min with rates 0.8 and 0.3 min⁻¹, the fractions are approximately 0.201897, 0.555064, and 0.243039. Their total is 1. This expression supplies a check independent of time stepping.

## A correct total is one check; each fraction also has a meaning

Conservation is useful because it connects three outputs through one relationship. A mistaken positive sign on the loss from B, or an omitted gain by C, would produce a visible drift in the total. Conservation checks whether transfers balance. An Euler step subtracts material from A and adds the same amount to B, then subtracts another amount from B and adds it to C. It can therefore preserve a total of 1 even when the step is very large.

![A 2 min Euler step produces a negative A fraction while preserving a total of 1. Dashed curves show the analytic model, and solid curves with circles show the coarse numerical result. The lower panel checks the total separately.](https://ml-biomat.com/static/tutorials/python-scientific/figures/dfb20e6198e1b48fceb4acb6.svg?v=dfb20e6198e1)

Figure 3A 2 min Euler step produces a negative A fraction while preserving a total of 1. Dashed curves show the analytic model, and solid curves with circles show the coarse numerical result. The lower panel checks the total separately.

With a 2 min step, the first update gives A = −0.6, B = 1.6, and C = 0. Their sum is still 1, but the fractions have left the range implied by the physical model. The update has maintained the initial transfer rate of 0.8 per minute for two whole minutes, moving 1.6 units when only 1 unit was present. This separates three questions: whether the total is conserved, whether all states remain nonnegative, and whether the trajectory closely approximates the continuous equations.

For A alone, an Euler update multiplies its current fraction by one minus the rate constant times the step size. To preserve a nonnegative A during that update, the product of rate constant and step size must be no greater than 1. Larger steps can introduce alternating signs; when the magnitude of the multiplier exceeds 1, those oscillations grow. This calculation connects step size to the speed of the process, rather than to the desired number of plotted points.

When one process evolves much faster than another, the fastest time scale can restrict an explicit method. This is a common source of stiffness. SciPy provides methods such as Radau and BDF for stiff systems. Examine the time scales, solver status, function evaluation count, and changes under tighter settings when choosing a method. After a change of algorithm, conservation, positivity, and the scientific outputs remain useful complementary checks.

An error comparison also needs a precise set of locations. At each Euler node, the program computes the absolute differences for A, B, and C, then selects the largest component difference. The full-run maximum is the largest of those node values. It describes the worst calculated component discrepancy, which answers a different question from an average error. All components here are dimensionless fractions and can be compared directly. State variables with different units or very different scales require an explicit scaling choice.

## Area accumulates an amount together with its duration

The amount of B at one instant differs from its cumulative presence during the process. If B stays near 0.4 for an interval of 0.5 min, that interval contributes approximately 0.2 min of fraction multiplied by time. Divide the entire process into many such strips and add their contributions to obtain the area beneath the B curve. Because a fraction is dimensionless, the area has units of minutes. With concentration in mmol/L on the vertical axis, the corresponding integral would instead have units of mmol·min/L.

$$
I_B(T)=\int_0^T b(t)\,dt\;\approx\;\sum_{n=0}^{N-1} b(t_n)h,\qquad T=Nh
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a11305f0a6beaa6b17d10d0f.svg) | Integral of the B fraction from 0 to T, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea3059ae9f52fe6b926fbbba.svg) | Fraction in B at time t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | Integration time and final time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/f31d38e9354f49723c5bb666.svg) | dt is an infinitesimal time increment; the integral accumulates the function over time, giving its units multiplied by min. |
| ![Formula](https://ml-biomat.com/static/agent-math/a23a4935fef8a0becb8f51d8.svg) | h is the uniform step (min), N the number of intervals, n an integer from 0 to N−1, and t_n = nh the left-end time (min). |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the areas of N left-end rectangles. |

If two half-minute intervals have approximate B fractions of 0.4 and 0.5, their areas are 0.2 and 0.25 min, totaling 0.45 min. Shorter strips describe the curve more closely. The complete model integrates to 3.068473 min over 0–10 min; the finite sum on the right is specifically a left-rectangle approximation.

Over 0–10 min, the integral for B is approximately 3.068473 min. It describes the average accumulated time spent in B during this observation window per initial unit. The area decreases if fewer units enter B or if they leave it quickly. Such an integral compares the persistence of an intermediate. In a particular experiment, connect the quantity to the actual question, such as intermediate exposure, accumulated release, or reaction contribution, while retaining its physical units.

`quad` takes a callable function that can be evaluated at any requested time. Here it integrates the analytic expression for B. Its second return value estimates numerical integration error, approximately 3.41 × 10⁻¹⁴ min in this calculation. This estimate concerns the integration of the specified function. Experimental uncertainty in the rate constants is assessed through parameter variation or uncertainty propagation. Distinguishing these quantities gives the many reported decimal places their proper meaning.

If only sampled measurements are available, `trapezoid` approximates the region between adjacent points by a trapezoid and adds the areas. Applying it to the 501 analytic samples gives 3.068446 min, slightly different from direct function integration because of finite sampling and the implied interpolation. For uneven sampling, supply the actual time array. Row numbers would otherwise assign an artificial and generally incorrect duration to each interval.

The flow account provides another compact check over an infinitely long observation period. Eventually C receives all initial units, so the accumulated B→C transfer is 1. At every time that transfer rate equals 0.3 min⁻¹ multiplied by the B fraction. The integral of B over infinite time is therefore 1 divided by 0.3 min⁻¹, or approximately 3.333333 min. Stopping at 10 min gives the smaller value 3.068473 min; the difference belongs to the tail of B that remains after the observation window.

## A complete program with a model, an algorithm, and an independent answer

The program keeps three calculation paths visible. `rhs` supplies rates and `solve_ivp` evolves the state. `exact` supplies the analytic solution of the same model for comparison. `euler` explicitly implements simple steps so that their effect can be inspected. The analytic function is specific to this closed-form example, whereas the numerical solver interface also supports more complicated models with additional processes.

### Complete example: sequential conversion, peak events, integrals, and step-size comparison

Running the program creates three figures, fractions.csv, and summary.json. All inputs and analytic comparison functions are included.

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

Start checking the output with its first row: at time zero, both the numerical and analytic fractions should be 1, 0, 0. Then inspect the last row, where little A remains and C is the dominant state. The summary records solver success, maximum analytic difference, total-fraction error, the peak time of B, and its integral. Each entry answers one of the scientific or computational questions developed above.

Peak localization and integration use different mathematical forms of the problem. A peak is found where a rate vanishes, so it is handled by event detection. An area is an accumulation over an interval, so it is handled by quadrature. With experimental samples, first decide what interpolation or local model is justified, then choose the corresponding tool. Specifying the question clearly is often more useful than memorizing additional function names.

## Change the rate and step size, then compare the checks

The experiment links continuous analytic curves and Euler trajectories, the composition at the selected time, and the maximum component error at each numerical node. Changing the first conversion rate changes a physical time scale. Changing the Euler step changes the numerical approximation to the same continuous process. Viewing these controls together makes their different roles visible.

### Process rate and numerical step

[Figure: Continuous and Euler trajectories for three fractions](https://ml-biomat.com/tutorials/python-scientific/p21/en/#P21-trajectory)

[Figure: Current composition comparison](https://ml-biomat.com/tutorials/python-scientific/p21/en/#P21-composition)

[Figure: Maximum fraction error at each node](https://ml-biomat.com/tutorials/python-scientific/p21/en/#P21-error)

Colors identify A, B, and C. Main-panel solid curves are analytic; lines with circles are Euler results. Pale composition bars are analytic and darker bars are Euler interpolations.

Keep the first rate at 0.8 min⁻¹ and increase the step from 0.1 min to 0.5, 1, and 2 min. The total stays near 1 while maximum error increases; the 2 min step also produces negative fractions. Then lower the rate to 0.4 min⁻¹ and inspect the effect of the same step sizes. The selected numerical composition uses straight-line interpolation between Euler nodes. Node errors are always evaluated at the positions actually calculated by the algorithm.

The displayed B integral uses left-end rectangles along the Euler trajectory, so it includes effects from both state approximation and area approximation. An analytic integral provides an independent reference. Moving the observation time only changes the displayed composition. It does not change the maximum error or integral over the full 0–10 min calculation. This separates a location on the trajectory from a property of the complete computation.

## Establish quantities and conditions before choosing solver settings

For a new model, begin with a flow diagram. Identify the quantities to track, the processes that increase or decrease each one, their initial values, and their units. Represent internal transfers in matching pairs, then check what adding the equations should preserve. If the system has inputs or outputs, the total change should match those boundary flows. This step often reveals omissions more effectively than immediate adjustment of solver settings.

Save the key scientific results together with the numerical setup: peak times, accumulated areas, initial states, rate parameters, solver method, and tolerances. Compare important outputs under stricter settings before relating their variation to experimental parameters. Integration and differential-equation solving then form a coherent analysis: use flows to explain change, trajectories to inspect the process, and carefully defined quantities to summarize what happened.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P21.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SciPy: Integration tutorial](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

   Function integration, sampled integration, and independent checks.

   BSD-3-Clause; technical reference
2. [SciPy: solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)

   Initial-value problems, RK45, tolerances, and events.

   BSD-3-Clause; technical reference
3. [SciPy: quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)

   Adaptive quadrature and the numerical error estimate.

   BSD-3-Clause; technical reference
4. [Euler Archive: Foundations of integral calculus, volume 1](https://scholarlycommons.pacific.edu/euler-works/342/)

   Archive record for the 1768 volume; the method illustration is an original calculation.

   Public-domain original; bibliographic reference
