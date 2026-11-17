# Fatigue testing: How repeated loads accumulate damage

Source: https://ml-biomat.com/tutorials/experimental-methods/m04/en/
Language: en

Interpret cyclic loads, life scatter, runouts and crack growth as a measurable history of repeated use.

## Why repeated use can break something that survived the first load

Bend a paper clip slightly and it may remain usable. Bend the same region back and forth repeatedly and it eventually breaks. Shoe soles, cartilage replacements, flexible conductors and implanted devices also experience repeated loads. A monotonic tensile test shows how a specimen responds as load rises toward a single failure. A fatigue test asks whether function survives many repetitions even when each repetition remains below the single-load failure condition. Fatigue refers to evolving material structure rather than the human experience of tiredness. The practical question is whether accumulated changes affect stiffness, dimensions, crack size or another property needed for the object to work.

Cyclic failure can begin at a small surface defect or involve pores, interfaces, local plasticity and polymer-network damage. Some stages produce little visible change while a crack grows gradually. A conspicuous final break occurs only after the remaining section can no longer carry the load. Two complementary experimental routes follow. One starts with an initially intact specimen and counts cycles to a defined failure state. The other starts with a measurable crack and records how much it grows during successive groups of cycles. The first supports a life comparison; the second investigates the evolution of an existing defect. Their outputs describe different parts of the history and require different axes and definitions.

Railway-axle failures helped drive the development of fatigue testing in the nineteenth century. Wöhler published systematic investigations between 1858 and 1870 connecting repeated stress with the number of cycles sustained. Rotating bending makes the underlying idea accessible: the external bending load can keep a fixed direction while a surface point travels alternately through tensile and compressive regions as the shaft rotates. That material point experiences a stress cycle. The original schematic below links rotation to the waveform seen by the point. It explains why fatigue analysis follows the material's local loading history rather than merely checking whether the external force changes direction.

![Original rotating-bending schematic: a rotating material point alternates tension and compression under a fixed-direction bending load. Right-hand stresses are illustrative, not Wöhler’s historical data.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e1d64c20469f1cc1eae5c68c.svg?v=e1d64c20469f)

Figure 1Original rotating-bending schematic: a rotating material point alternates tension and compression under a fixed-direction bending load. Right-hand stresses are illustrative, not Wöhler’s historical data.

## Define the maximum, minimum and timing of a cycle

Consider a sinusoidal stress history. The midpoint between maximum and minimum is mean stress; half their difference is stress amplitude; their full difference is stress range. Range and amplitude differ by a factor of two and should not be exchanged when using a fitted fatigue relation. A cycle from 10 to 100 MPa and back has mean stress 55 MPa, amplitude 45 MPa and range 90 MPa. The minimum divided by the maximum is 0.1. This ratio, conventionally R, quickly indicates whether the cycle remains in tension and how much load persists at the lowest point. Together, these quantities describe the cycle more clearly than its maximum alone.

$$
\sigma_m=\frac{\sigma_{\max}+\sigma_{\min}}{2},\quad\sigma_a=\frac{\sigma_{\max}-\sigma_{\min}}{2},\quad\Delta\sigma=2\sigma_a,\quad R=\frac{\sigma_{\min}}{\sigma_{\max}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5269b242adb1189076e77772.svg) | Mean stress, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/1e1d1d71588c211f946d0524.svg) | Stress amplitude, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/b70db1f8af3fa7ce2b6c46bd.svg) | Maximum stress in a cycle, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/36459aa93561f626acf00ff1.svg) | Minimum stress in a cycle, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2073bb3222b4607f026726c2.svg) | Stress range, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Stress ratio, dimensionless, with nonzero maximum. |

Cycling from 10 to 100 MPa gives mean 55, amplitude 45 and range 90 MPa, with R=0.1. Changing minimum at fixed maximum changes both amplitude and mean.

Identical maximum stress does not imply identical cycling. Raise the minimum from 10 to 50 MPa while keeping the maximum at 100 MPa: amplitude falls from 45 to 25 MPa and mean stress rises from 55 to 75 MPa. Crack opening, closure and cyclic plasticity can change with these quantities. Record stress ratio, control mode and waveform together when comparing fatigue curves. Fully reversed loading has R equal to minus one, zero-to-tension loading has R equal to zero, and tension–tension loading commonly has positive R. For compression tests, first establish the sign convention; similar-looking ratios can otherwise conceal different physical histories.

Frequency gives the number of complete cycles per second. At 5 Hz, a million cycles take about 55.6 hours. Increasing frequency shortens clock time, but it may also change the material process. Energy dissipated in each polymer cycle can become heat, and rapid cycling can raise specimen temperature when cooling is insufficient. A hydrated network may have less time to drain or recover, while reactions in a corrosive medium depend on elapsed time as well as cycle count. During accelerated testing, monitor temperature, waveform tracking and material response to establish whether the same process remains dominant. Frequency is therefore an experimental variable, not simply a convenient speed setting.

The machine controls force, displacement or local strain, with the remaining quantities recorded as responses. Under force control, softening can cause deformation to increase. Under displacement control, the same softening can lower the peak force. Either trend can contain damage or recoverable rearrangement, so examine residual deformation and recovery as well. A hysteresis loop shows that loading and unloading follow different paths; its area is mechanical energy lost during a cycle. It can indicate dissipation and possible heating. It does not directly measure the fraction of total fatigue life consumed by that cycle. Connecting a loop to life requires an additional model and appropriate experimental evidence.

![Left: cycles with the same 100 MPa maximum but different R. Right: a separately constructed hysteresis loop illustrates per-cycle dissipation; it is not the constitutive model of the S–N or Paris datasets.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9f7e4fbb7d92a443e9bb95f5.svg?v=9f7e4fbb7d92)

Figure 2Left: cycles with the same 100 MPa maximum but different R. Right: a separately constructed hysteresis loop illustrates per-cycle dissipation; it is not the constitutive model of the S–N or Paris datasets.

## An arrow on a life curve is an experimental observation

A stress–life or S–N curve comes from independent specimens tested at several stress levels. Record the cycles required to reach a predefined failure condition and plot stress against that count. A logarithmic cycle axis is useful because lives can span thousands to millions of cycles. Equal distances on that axis represent equal ratios rather than equal added counts, so apparently nearby points can have substantially different lives. Define failure before testing: complete separation, a specified stiffness reduction, a particular crack length or unacceptable device output produces a different life measure. The criterion should match the scientific comparison or the function that matters in use.

$$
N_{50}=N_{\mathrm{ref}}\left(\frac{\sigma_a}{\sigma_{\mathrm{ref}}}\right)^{-b},\qquad\log_{10}N\sim\mathcal N\!\left(\log_{10}N_{50},s^2\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8e84b28fc356c74bc8262265.svg) | Median cycles to failure at the specified amplitude, cycles. |
| ![Formula](https://ml-biomat.com/static/agent-math/0d389c9b3256376faa184ef9.svg) | Median life at reference amplitude, 10⁶ cycles here. |
| ![Formula](https://ml-biomat.com/static/agent-math/1e1d1d71588c211f946d0524.svg) | Stress amplitude, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/1a95f2b7007feac96d8dcf4f.svg) | Reference amplitude, 100 MPa here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Stress–life power exponent, five here, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Individual failure cycle count, cycles; its numerical count enters the logarithm. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Standard deviation of log10 life, 0.16 here, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0e378265ddb70b5dadd36830.svg) | Normal-distribution notation with mean and variance. |

Teaching power law and lognormal scatter at fixed load ratio, waveform and environment. At 125 MPa, N50=327680 cycles; survival to a million-cycle stop contributes N>10⁶ information.

The teaching relation assigns a median life of one million cycles at stress amplitude 100 MPa, with life decreasing according to the fifth power of increasing stress. At 125 MPa the median is 327680 cycles; at 150 MPa it is approximately 131687 cycles. Median means that half the life distribution lies below the value and half above it, not that every specimen must break there. The program adds scatter in logarithmic life to construct 24 independent specimens, then stops every test at one million cycles. Some lower-stress specimens remain intact at that limit. These surviving observations reproduce the statistical situation encountered when finite laboratory time prevents waiting for every specimen to fail.

A surviving observation is a runout, or right-censored life. It says that life exceeds the cycles already completed, not that failure occurred exactly at the stopping count. The graph uses a rightward arrow to preserve that direction. Treating every arrow as failure at one million cycles shortens the inferred long lives. Deleting the arrows instead retains a preferentially short-lived subset. Both operations change the meaning of the observations. The exported table therefore stores observed cycles together with a failure indicator. A reader or analysis program can distinguish an observed break from survival up to a test limit without guessing from the numerical count.

The example uses maximum likelihood to combine failures and runouts. For a failed specimen, the model evaluates how plausible failure near its observed life is. For a runout, it evaluates the probability of surviving beyond the limit. Assuming approximately normal logarithmic life, the program estimates curve position, stress exponent and scatter using both kinds of evidence. The shaded region spans the fitted 10th to 90th percentiles of specimen life. It describes variation among specimens, not a confidence interval for the estimated median curve. These two uncertainties answer different questions: how widely lives vary and how precisely the underlying curve has been estimated from the available tests.

![Twenty-four constructed independent specimens with a 10⁶-cycle stop. Right arrows are runouts; the band is fitted life-distribution 10–90% quantiles, not parameter confidence bounds. Right shows the survival tail at 100 MPa.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/06f86726c43dfd5c19be6a88.svg?v=06f86726c43d)

Figure 3Twenty-four constructed independent specimens with a 10⁶-cycle stop. Right arrows are runouts; the band is fitted life-distribution 10–90% quantiles, not parameter confidence bounds. Right shows the survival tail at 100 MPa.

## Track how far a crack moves instead of waiting for separation

Total life can include crack formation and subsequent growth. Once a crack is observable, growth can be studied separately. Measure its length, apply a block of cycles, then divide the length increment by the cycle increment. This gives an average advance per cycle. It may be much smaller than a displacement resolvable in one image, because many cycles accumulate a measurable total motion. A very short measurement window is dominated by localisation error; a very long window can average across a changing driving force. Select the window using both image resolution and growth speed, and retain its cycle boundaries so that the reported rate has a clear experimental meaning.

$$
\frac{da}{dN}=C(\Delta K)^m,\qquad\Delta K=Y\Delta\sigma\sqrt{\pi a},\qquad N_p=\int_{a_0}^{a_f}\frac{da}{C[Y\Delta\sigma\sqrt{\pi a}]^m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Centre-crack half-length in this example, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Accumulated cycles, cycles. |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Paris coefficient; for m=3 its units are m/cycle/(MPa·√m)³, set to 10⁻¹⁰. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Paris growth exponent, three here, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1b568e0bb351fe2c942a6f22.svg) | Mode-I stress-intensity range, MPa·√m. |
| ![Formula](https://ml-biomat.com/static/agent-math/ab4817775494786b06f0b9ce.svg) | Geometry factor, one for the wide-plate example. |
| ![Formula](https://ml-biomat.com/static/agent-math/2073bb3222b4607f026726c2.svg) | Remote stress range, 60 MPa here. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi. |
| ![Formula](https://ml-biomat.com/static/agent-math/5a9c1aa4dbcfe2c2217b3e46.svg) | Propagation cycles from initial to prescribed terminal size, cycles. |
| ![Formula](https://ml-biomat.com/static/agent-math/6301e767c6538ae4707f3d93.svg) | Initial half-length, 0.001 m here. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa14f1964a62cdb086a276be.svg) | Prescribed terminal half-length, 0.006 m here. |

Teaching long-crack linear elastic Paris regime under fixed conditions, excluding threshold and instability regimes. The integral adds each length increment divided by its local growth rate. Numerical integration is checked independently against the m=3 analytical result.

Paris and Erdogan's 1963 study examined crack-growth laws and the range of evidence used to assess them. The familiar Paris relation connects growth per cycle with stress-intensity range. In an intermediate regime of many linear elastic long-crack datasets, a log–log plot is approximately straight: its slope gives an exponent and its position a coefficient. The coefficient's units depend on the exponent and the units used for stress intensity and length. Moving a coefficient calibrated with millimetres into a program using metres without conversion changes the prediction. Near-threshold growth, short cracks and the approach to rapid instability require descriptions appropriate to those regimes rather than unlimited extrapolation of the same middle-region line.

The example prescribes exponent three and coefficient 10⁻¹⁰ m per cycle per cubed MPa·√m. Stress range is 60 MPa and the geometry factor is one. A centre crack starts with half-length 1 mm and is followed to a specified 6 mm endpoint. Growth accelerates because the stress-intensity range increases with crack length even though the external stress range stays fixed. The program evaluates an analytical integral and independently solves the differential equation to check agreement. The endpoint is a chosen length for comparing propagation histories. It is not a final failure size automatically calculated from fracture toughness, and the result describes this propagation interval rather than total specimen life.

Starting with a larger defect changes the cycles required to reach the same endpoint. Increasing initial half-length from 1 to 2 mm removes an early portion that would have grown slowly, not merely one millimetre of travel. This connects defect detection with propagation modelling: the smallest reliably identified crack helps determine where a measured or inferred history begins. In a real component, geometry factors commonly vary with crack size relative to the component, while load ratio, residual stress and closure can affect growth. Pair these conditions with those used to determine the growth relation. A curve fitted for one crack geometry and environment becomes useful when its application preserves those relevant conditions.

![Constructed Paris-regime data, initial-crack effects, Miner fractions and propagation-life sensitivity. Six millimetres is a prescribed comparison endpoint, not an instability size derived from toughness.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/67eaa8c40855f0a2bb9cb3eb.svg?v=67eaa8c40855)

Figure 4Constructed Paris-regime data, initial-crack effects, Miner fractions and propagation-life sensitivity. Six millimetres is a prescribed comparison endpoint, not an instability size derived from toughness.

## Can cycles of different sizes simply be added?

Service loading rarely has a single amplitude. Walking, running and occasional jumps impose different loads on a shoe sole; a flexible device may experience frequent small bends and a few large folds. A simple accumulation model divides cycles applied at each level by the reference life at that level, then adds the fractions. This is the familiar Miner approach. It converts different load blocks into a common bookkeeping measure for an initial comparison. The resulting damage value is a model indicator, not a directly observed fraction of broken molecular bonds or lost cross-sectional area. Its usefulness comes from a clear relation to a chosen constant-amplitude life curve.

$$
D=\sum_i\frac{n_i}{N_i}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Miner linear accumulation indicator, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Load-level or block index. |
| ![Formula](https://ml-biomat.com/static/agent-math/4ac70a528e41a9bd73952b00.svg) | Applied cycles at level i, cycles. |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | Reference constant-amplitude life at the same level, cycles. |

Consistent reference-life definitions and conditions; linear addition contains no sequence effect. 100000/327680 + 200000/1000000 = 0.5051758. D=1 is a nominal model endpoint, not a universal measured broken-bond fraction.

Using the specified teaching curve, one hundred thousand cycles at 125 MPa contribute about 0.3052, while two hundred thousand cycles at 100 MPa contribute 0.2. The sum is about 0.5052. Exchanging the order of those blocks leaves the linear-model result unchanged. Materials can retain sequence effects through plastic zones, residual stresses, network softening or changes in crack closure. This difference suggests a direct experiment: apply the same counts and amplitudes in opposite orders and compare the response. The experiment tests whether the selected accumulation rule captures the relevant history, rather than interpreting its arithmetic as a measurement of physical damage.

Irregular loading also requires a counting rule. Large excursions may contain smaller loops, so merely counting zero crossings can miss meaningful repeated ranges. Rainflow counting is a family of methods that decomposes a complex history into cycle ranges and means. It addresses counting; a suitable material-fatigue relation is still needed afterward. Preserve the original time sequence because a histogram removes order and dwell times. Those details can matter for recovery, sustained-load effects and environmental reactions. Keeping them makes it possible to ask a different question later without reconstructing the original loading from an incomplete summary.

For polymers and hydrated materials, keep clock time alongside cycle count. Three hundred thousand cycles at 5 Hz take approximately 16.67 hours. At another frequency, heating, drainage or recovery may differ even when count is identical. During a long pause, material state can continue changing without any additional cycles. Divide the record into loading blocks, holds and recovery intervals, and synchronise temperature with peak and valley measurements. This preserves the history needed for interpretation. A single average frequency may be convenient for a table but cannot describe all the physical differences between two such experiments.

## Read “no detectable growth” in an actual hydrogel study

The following actual research image comes from Lin and colleagues' anti-fatigue-fracture PVA hydrogel study. Original cycle labels, energy label and scale bars are retained. At the displayed loading condition, the images compare the notch after 10 and 30000 cycles. The large view has a 5 mm scale bar and the close views have 1 mm bars. This makes repeated-load crack observation concrete and illustrates why resistance to one tear and resistance to cyclic crack advance are measured separately. The photograph is reproduced under the source's CC BY 4.0 license, with its identity preserved rather than presented as data generated by the accompanying teaching program.

![Lin et al., Anti-fatigue-fracture hydrogels, arXiv:1812.06403v1 (2018), cropped Fig. 3H, CC BY 4.0. Swollen PVA after 90-min dry annealing, original G=1000 J/m², comparing N=10 and 30000; original 5 mm and 1 mm scale bars and labels retained.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/72ddc34bf7e318892b127dce.svg?v=72ddc34bf7e3)

Figure 5Lin et al., Anti-fatigue-fracture hydrogels, arXiv:1812.06403v1 (2018), cropped Fig. 3H, CC BY 4.0. Swollen PVA after 90-min dry annealing, original G=1000 J/m², comparing N=10 and 30000; original 5 mm and 1 mm scale bars and labels retained.

Interpreting an absence of detectable motion requires both a length resolution and a cycle window. As an arithmetic example, suppose reliable localisation resolves 20 μm and no displacement is resolved over one thousand cycles. That window corresponds to an average-growth resolution of about 20 nm per cycle. Growth per cycle can be smaller than a pixel because the observation accumulates motion over many cycles. Better localisation or a longer window can improve sensitivity, provided loading remains stable. A finite observation with no resolved growth therefore has a defined spatial and temporal scale. Retaining those scales makes comparisons between instruments and test durations meaningful.

Cycling can first change the stress–stretch response of an unnotched gel as its network approaches a more stable cyclic state. A driving-force calculation for a notched specimen should be paired with the relevant material state. Using the first cycle's energy to represent a much later state can miss softening or rearrangement. Save representative loops, image the crack periodically and track peak force, residual extension and temperature. Their combined histories help distinguish global softening, crack advance and instrumental drift. They also show whether a nominally constant imposed deformation produces a constant mechanical driving condition throughout the test.

Hydration control affects crack observation itself. Drying at the edge of a thin gel can change dimensions and local stress, and a long fatigue test provides much more time for evaporation than a brief tensile test. Maintain immersion or humidity, temperature and medium, and check whether markers or contrast treatments alter the surface. For transparent specimens, suitable illumination, texture or local markings can improve visibility. Apply the same treatment across comparison groups. The resulting image sequence is then connected to a controlled material state rather than to a gradually changing mixture of mechanical loading and environmental exposure.

## Calculate life and crack growth from complete records

The program keeps constructed numerical records separate from the published photograph. With a fixed random seed, it creates 24 stress–life specimens, explicitly distinguishes failures from runouts and compares a censored-data fit with a fit using failures alone. A separate constructed dataset provides Paris-regime growth rates for estimating coefficient and exponent. Propagation from a known initial crack to the defined endpoint is then solved independently. Life quantiles, growth-rate plots and linear damage fractions all come from these calculations. Exported tables allow the reader to redraw them directly rather than attempting to recover numerical values from a picture.

When substituting experimental files, check cycle-counter continuity and whether restarting a machine resets the counter. A second file from one specimen should not accidentally become a new independent specimen. Failure indicators must match the predefined criterion; an unexpected stop, grip slip and specimen fracture are distinct events. Cycles completed before an interruption remain part of the loading history. Whether and how the test resumes depends on the interruption and material state. Recording these events at acquisition is more reliable than trying to infer them later from a smooth fitted curve or an isolated final cycle count.

### Complete Python: censored lives, Paris growth and load blocks

Numerical records are constructed; the actual paper image is bundled with its separate license notice.

```
"""Fatigue teaching: censored stress-life data and a separate Paris growth model.
The bundled photograph is actual CC BY 4.0 research; see data/NOTICE.txt.
All numerical records generated here are constructed, not that paper's data.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Arc

def life(stress):return 1e6*(np.asarray(stress)/100.)**-5
def growth_life(a0=.001,af=.006,ds=60.,C=1e-10):
    return 2*(a0**-.5-af**-.5)/(C*(ds*np.sqrt(np.pi))**3)
def growth(n,a0=.001,ds=60.,C=1e-10,af=.006):
    ne=np.minimum(np.asarray(n),growth_life(a0,af,ds,C));return (a0**-.5-.5*C*(ds*np.sqrt(np.pi))**3*ne)**-2

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1904);S=np.repeat([80.,90.,105.,125.,150.,180.],4);true_log=np.log10(life(S))+rng.normal(0,.16,len(S));stop=1e6;Ntrue=10**true_log;failed=Ntrue<=stop;Nobs=np.minimum(Ntrue,stop);x=np.log10(S/100);y=np.log10(Nobs)
    def objective(q):
        mu=q[0]-q[1]*x;sd=np.exp(q[2]);z=(y-mu)/sd
        return -np.sum(np.where(failed,norm.logpdf(z)-np.log(sd),norm.logsf(z)))
    fit=minimize(objective,[6,5,np.log(.16)],method='L-BFGS-B',bounds=[(4,8),(1,10),(np.log(.03),np.log(.7))]);assert fit.success,fit.message
    intercept,m,logsd=fit.x;sd=float(np.exp(logsd));ols=np.polyfit(x[failed],y[failed],1)
    DK=np.geomspace(3.5,12,36);rate=1e-10*DK**3*10**rng.normal(0,.08,len(DK));mp,cp=np.polyfit(np.log10(DK),np.log10(rate),1);Cfit=10**cp
    nend=growth_life();nn=np.linspace(0,nend,401);aa=growth(nn);ode=solve_ivp(lambda n,v:[1e-10*(60*np.sqrt(np.pi*v[0]))**3],(0,nend),[.001],rtol=1e-10,atol=1e-13,dense_output=True);ode_error=float(np.max(abs(ode.sol(nn)[0]-aa)))
    blocks=np.array([100000.,200000.]);levels=np.array([125.,100.]);damage=blocks/life(levels)
    summary={'specimens':len(S),'failures':int(failed.sum()),'runouts':int((~failed).sum()),'fit_intercept_log10N':float(intercept),'fit_stress_exponent':float(m),'fit_log10_scatter':sd,'failures_only_intercept':float(ols[1]),'fit_median_life_at100':float(10**intercept),'specified_median_life_at125':float(life(125)),'specified_damage_sum':float(damage.sum()),'hours_300000cycles_at5Hz':300000/5/3600,'paris_fit_C':float(Cfit),'paris_fit_m':float(mp),'growth_cycles_1to6mm':float(nend),'growth_cycles_2to6mm':float(growth_life(.002)),'ode_max_error_m':ode_error,'growth_at_start_m_cycle':float(1e-10*(60*np.sqrt(np.pi*.001))**3),'stress_amplitude_100_10_MPa':45.,'mean_stress_100_10_MPa':55.,'stress_ratio_100_10':.1}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[S,Nobs,failed.astype(int)],delimiter=',',header='stress_amplitude_MPa,observed_cycles,failure_observed_1',comments='');np.savetxt(o/'growth.csv',np.c_[nn,aa*1000,60*np.sqrt(np.pi*aa),1e-10*(60*np.sqrt(np.pi*aa))**3],delimiter=',',header='cycles,crack_half_length_mm,delta_K_MPa_sqrt_m,da_dN_m_cycle',comments='');np.savetxt(o/'paris.csv',np.c_[DK,rate],delimiter=',',header='delta_K_MPa_sqrt_m,growth_rate_m_cycle',comments='');np.savetxt(o/'blocks.csv',np.c_[levels,blocks,life(levels),damage],delimiter=',',header='stress_amplitude_MPa,applied_cycles,median_constant_amplitude_life,miner_fraction',comments='')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));ax[0].set(xlim=(0,10),ylim=(0,7));ax[0].axis('off');ax[0].add_patch(Rectangle((1,3),8,.55,facecolor='#c5d6df',edgecolor=B));
    for xx in [2,8]:ax[0].add_patch(Rectangle((xx-.3,2.6),.6,1.4,facecolor='#6e8593'))
    ax[0].annotate('',(5,3.7),(5,5.7),arrowprops={'arrowstyle':'->','color':O,'lw':2});ax[0].text(5,6,tr('固定方向弯曲载荷','Bending load in a fixed direction'),ha='center');ax[0].add_patch(Arc((5,3.3),2,2,theta1=30,theta2=320,color=G,lw=2));ax[0].annotate('',(5.9,3.8),(5.8,4.1),arrowprops={'arrowstyle':'->','color':G});ax[0].scatter([4],[3.5],s=55,color=O);ax[0].text(5,1.3,tr('表面一点随转动交替受拉、受压','One surface point alternates tension and compression'),ha='center',fontsize=10);ax[0].text(5,.4,tr('Wöhler：1858–1870年的系统试验','Wöhler: systematic tests, 1858–1870'),ha='center',fontsize=10);ax[0].set_title(tr('a  旋转弯曲的历史问题','a  The historical rotating-bending question'),fontsize=12)
    theta=np.linspace(0,2*np.pi,250);ax[1].plot(theta/(2*np.pi),100*np.cos(theta),color=B);ax[1].axhline(0,color='#8a9ca7',ls='--');ax[1].set(xlabel=tr('一圈中的转数','Fraction of one revolution'),ylabel=tr('归一示例应力 / MPa','Illustrative stress / MPa'),title=tr('b  外力不换向，材料点仍经历循环','b  A rotating point still sees a stress cycle'));f.tight_layout();save(f,'history')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));t=np.linspace(0,2,501)
    for r,c in [(.1,B),(.5,O)]:mean=100*(1+r)/2;amp=100*(1-r)/2;ax[0].plot(t,mean+amp*np.sin(2*np.pi*t),color=c,label=f'R={r}')
    ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / MPa','Stress / MPa'),title=tr('a  相同最大应力，不同循环','a  Same maximum stress, different cycles'));ax[0].legend()
    eps=.03*np.sin(theta);sig=3*np.sin(theta)+.8*np.cos(theta);ax[1].plot(eps*100,sig,color=G);ax[1].fill(eps*100,sig,color=G,alpha=.18);ax[1].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('b  示意滞后环：每圈消耗能量','b  Illustrative hysteresis: energy lost per cycle'));ax[1].text(0,0,tr('面积有能量含义','Area has an energy meaning'),ha='center',fontsize=10);f.tight_layout();save(f,'waveform')
    f,ax=plt.subplots(1,2,figsize=(12,4.9));ss=np.linspace(75,185,180);mu=intercept-m*np.log10(ss/100);med=10**mu;lo=10**(mu+norm.ppf(.1)*sd);hi=10**(mu+norm.ppf(.9)*sd);ax[0].fill_betweenx(ss,lo,hi,color=B,alpha=.15,label=tr('拟合寿命分布10–90%分位','Fitted life distribution 10–90% quantiles'));ax[0].plot(med,ss,color=B,label=tr('包含未失效试样','Includes runouts'));ax[0].plot(10**np.polyval(ols,np.log10(ss/100)),ss,color=O,ls='--',label=tr('仅拟合失效点','Fit failures only'));ax[0].scatter(Nobs[failed],S[failed],color='#163b51',s=25)
    for nx,sy in zip(Nobs[~failed],S[~failed]):ax[0].annotate('',(nx*1.7,sy),(nx,sy),arrowprops={'arrowstyle':'->','color':G});ax[0].scatter([nx],[sy],facecolors='none',edgecolors=G,s=30)
    ax[0].set(xscale='log',xlabel=tr('观测循环数 / cycles','Observed cycles'),ylabel=tr('应力幅 / MPa','Stress amplitude / MPa'),title=tr('a  箭头表示达到停机上限仍未失效','a  Arrows mark survival to the test limit'));ax[0].legend(fontsize=8,loc='lower left')
    yy=np.linspace(4.7,7,500);pdf=norm.pdf(yy,intercept,sd);ax[1].plot(yy,pdf,color=B);ax[1].fill_between(yy,0,pdf,where=yy>=6,color=G,alpha=.3,label=tr('寿命超过10⁶的概率','Probability of life above 10⁶'));ax[1].axvline(6,color=O,ls='--');ax[1].set(xlabel='log₁₀(N)',ylabel=tr('对数寿命概率密度','Density of log life'),title=tr('b  100 MPa下的分布与删失','b  Distribution and censoring at 100 MPa'));ax[1].legend(fontsize=9);f.tight_layout();save(f,'life')
    f,ax=plt.subplots(2,2,figsize=(12,8));ax[0,0].loglog(DK,rate,'o',color=B,ms=4,label=tr('构造增长数据','Constructed growth data'));ax[0,0].loglog(DK,Cfit*DK**mp,color=O,label=f'm={mp:.3f}');ax[0,0].set(xlabel='ΔK / MPa √m',ylabel='da/dN / m cycle⁻¹',title=tr('a  Paris中段关系','a  Paris-regime relation'));ax[0,0].legend(fontsize=9)
    for start,c in [(.001,B),(.002,O)]:ns=np.linspace(0,growth_life(start),300);ax[0,1].plot(ns,growth(ns,start)*1000,color=c,label=f'a₀={start*1000:g} mm')
    ax[0,1].set(xlabel=tr('循环数','Cycles'),ylabel=tr('裂纹半长 / mm','Crack half-length / mm'),title=tr('b  从已知裂纹到规定6 mm终点','b  Known crack to a specified 6 mm endpoint'));ax[0,1].legend()
    ax[1,0].bar([0,1],damage,color=[B,O]);ax[1,0].set(xticks=[0,1],xticklabels=['125 MPa\n100,000 cycles','100 MPa\n200,000 cycles'],ylabel=tr('线性损伤份额','Linear damage fraction'),title=tr('c  Miner相加，不包含先后次序','c  Miner addition omits sequence effects'));ax[1,0].text(.5,.28,f'D={damage.sum():.4f}',ha='center')
    aa0=np.linspace(.0005,.0025,150);ax[1,1].plot(aa0*1000,[growth_life(q) for q in aa0],color=P);ax[1,1].set(xlabel=tr('初始裂纹半长 / mm','Initial crack half-length / mm'),ylabel=tr('到6 mm的循环数','Cycles to 6 mm'),title=tr('d  初始缺陷改变传播寿命','d  Initial defect changes propagation life'));f.tight_layout();save(f,'growth')
    img=plt.imread(Path(__file__).resolve().parent/'data/lin2018-fig3h.png');f,ax=plt.subplots(figsize=(12,5.3));ax.imshow(img);ax.axis('off');ax.set_title(tr('真实研究图：PVA凝胶在循环载荷下的缺口观测','Actual research figure: a PVA-gel notch under repeated loading'),loc='left',pad=18,fontsize=14);f.text(.5,.03,tr('Lin等，arXiv:1812.06403v1，图3H裁切，CC BY 4.0；保留原始标注与比例尺。','Lin et al., arXiv:1812.06403v1, cropped Fig. 3H, CC BY 4.0; original labels and scale bars retained.'),ha='center',fontsize=10);f.tight_layout(rect=[0,.06,1,1]);save(f,'published')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

Begin reading the output by counting specimens before interpreting coefficients. Of the twenty-four constructed specimens, fifteen reach the failure criterion and nine remain operational at the stopping limit of one million cycles. Including those nine survival records gives a fitted median life of about 1.09 million cycles at a stress amplitude of 100 MPa. Fitting the failures alone gives approximately 0.92 million cycles at the same amplitude. The difference comes from how the same observations enter the calculation. It does not describe a change of material. A median divides the modeled life distribution in half: half of the population lies above it and half below it. It is therefore different from a minimum guaranteed life and from an observation that every specimen actually survived for 1.09 million cycles.

Check the propagation calculation separately from the specimen life fit. Starting with a crack half-length of 1 mm requires approximately 311,000 cycles to reach the prescribed 6 mm endpoint. Starting at 2 mm requires about 157,000 cycles. The stress range, growth coefficient and final length are unchanged; only the initial flaw differs. The program evaluates this trajectory using both a closed-form integral and a numerical differential-equation solver. Their close agreement checks the implementation of this specified model, particularly the length units and integration direction. Selecting the interval over which the growth law represents an actual experiment still depends on measured crack growth and specimen geometry.

If a measured trajectory accelerates earlier than the model, use synchronized observations to investigate the change. A growing crack can appreciably reduce the remaining section, while the geometry correction to the driving force can change with crack length. Temperature rise, liquid uptake and contact between crack faces may also alter the response. Marking these events at their corresponding cycle counts makes their timing visible. The resulting evidence can guide the next experiment: increase the imaging rate near acceleration, record temperature beside the specimen, or replace the wide-plate approximation with a geometry calibration appropriate to the actual coupon. This connects a mismatch in the graph to a specific measurement that can resolve it.

The interactive experiment fixes the Paris coefficient, exponent and six-millimetre endpoint while varying initial crack half-length, stress range and elapsed cycles. Increasing stress range steepens growth earlier; increasing the initial flaw reduces cycles to the endpoint. The calculation stops at that defined length and reports both current size and the propagation interval's cycle count. Crack initiation, the threshold regime and rapid final instability are not folded into this result. Its starting condition and stopping rule remain visible, making it possible to identify exactly which experimental inputs control the prediction and which additional stages would require their own measurements.

## Interactive: initial crack and propagation cycles

Fixed C=10⁻¹⁰, m=3 and Y=1 using MPa, m and cycles. Calculation stops at half-length 6 mm.

[Figure: Crack half-length versus cycles](https://ml-biomat.com/tutorials/experimental-methods/m04/en/#M04-plot)

## Turn durability into a complete research question

Start with the function that must be retained and a corresponding failure criterion. A scaffold may need stiffness and crack control, a flexible electrode electrical continuity, and a dressing intact edges and adhesion. Synchronising mechanical cycles with functional measurements can reveal degradation before visible separation. Choose load range, mean level, frequency, waveform and environment accordingly, then decide between an intact-specimen life test and an existing-crack growth study. The resulting cycle count has a practical meaning. It becomes possible to compare materials under a shared use condition instead of creating a durability ranking detached from what each specimen was asked to do.

Statistical comparison needs independent specimens and informative stress levels. If all specimens fail quickly, the data describe high-load behaviour but say little about long lives. If all reach the stopping limit, they establish survival during that observation but provide limited information about the stress–life slope. Use initial results to select further levels, retain runouts and distinguish batches from individual specimens. This helps use long machine runs effectively. Fracture-surface observations, temperature histories and representative loops also reveal whether different stress levels activate different mechanisms, which may explain a curve that cannot be represented adequately by one straight segment on logarithmic axes.

Present the loading definition, failure definition, independent specimen count, stopping limit and runouts together with the fitted range. For crack-growth models, also identify geometry, length units, calibration interval and propagation endpoint. Results then lead to specific follow-up questions. A gel with high single-tear energy but continuing cyclic growth invites study of how dissipation evolves with reuse. Large life scatter motivates examination of initial defects and processing batches. Fatigue testing is valuable because it makes repeated-use history observable, linking small changes over many cycles to the eventual loss of a material or device function.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Deutsche Biographie — August Wöhler](https://www.deutsche-biographie.de/sfz26909.html?language=en)

   Verify railway-axle investigations and the 1858–1870 publication timeline.

   Biographical reference; original diagram here.
2. [Instron — Dynamic fatigue testing](https://instron.com/en/resources/test-types/dynamic-test/)

   Dynamic frames, force and strain measurement, and waveform control.

   Official technical reference; no images reused.
3. [NIST — Censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm)

   Meaning of survival at stopping and right-censored observations.

   Official statistical handbook; original example here.
4. [NIST — Maximum likelihood with censored reliability data](https://www.itl.nist.gov/div898/handbook/apr/section4/apr413.htm)

   Failure indicators, survival probability and life-distribution estimation.

   Official statistical reference; no example data reused.
5. [JCSS — Fatigue models for metallic structures](https://www.jcss-lc.org/publications/jcsspmc/JCSS-3-12-Fatigue.pdf)

   S–N, Miner accumulation and long-crack growth models.
6. [Paris and Erdogan — A critical analysis of crack propagation laws (1963)](https://doi.org/10.1115/1.3656900)

   Primary abstract on assessing growth laws over a broad data range.

   Publisher indexed abstract consulted; no figures reused.
7. [Lin et al. — Anti-fatigue-fracture hydrogels](https://arxiv.org/abs/1812.06403v1)

   Actual PVA-notch photographs, hydration, cyclic observations and detection scales.

   CC BY 4.0, confirmed by arXiv license link. Fig. 3H cropped; attribution and change notice in data/NOTICE.txt.
