# Is the Peak Still There? Signal Processing with SciPy

Source: https://ml-biomat.com/tutorials/python-scientific/p20/en/
Language: en

Connect sampling, local fitting, peak detection, and frequency response to inspect how smoothing changes a signal.

## After smoothing, is the peak still in the same place?

A sensor recording a transient process can show a slow baseline, genuine peaks, and rapid fluctuations together. A sample passing a detector may produce a voltage that rises and falls, while electrical or mechanical disturbance adds periodic interference. To identify when the peak occurs and how high it is, you may first smooth the curve. Smoothing also changes peak height, width, and sometimes position. This chapter uses SciPy with a fully specified teaching signal to examine what each processing step preserves and changes.

We create two peaks of different widths, add interference at two known frequencies, and compare a moving mean with Savitzky–Golay local polynomial smoothing. Then `find_peaks` locates maxima that satisfy explicit conditions, and a frequency view explains the effect of the window. Comparing every output with the known smooth model separates residual interference from shape distortion. The complete program exports original arrays, smoothed values, peak locations, and numerical summaries.

A signal is simply a sequence of values ordered in time. It may describe light intensity, voltage, displacement, or another instrument reading. Here amplitude is measured in mV and time in seconds. Processing routines receive arrays, while physical time enters through the sampling interval. Understanding that connection turns a “21-point window” into an interpretable time range.

## Read the sampling interval before choosing a window

Our example samples from 0 to 10 s at intervals of 0.02 s, producing 501 records. Fifty samples per second correspond to a sampling frequency of 50 Hz. Adjacent array positions represent a fixed time increment, so a filter moving by sample index also spans a fixed duration. For irregular instrument timestamps, inspect those actual times first. Treating every consecutive set of twenty-one records as the same temporal window would otherwise apply different smoothing durations at different positions.

A centered 21-point window takes ten neighbors on each side. Its earliest and latest samples are separated by 20×0.02 = 0.40 s. A five-point window spans 0.08 s and a forty-one-point window spans 0.80 s. Window length counts participating observations, whereas temporal span measures the separation between the first and last. Displaying both makes it possible to compare the processing window with the physical width of a peak.

Sampling also constrains the rates of variation that can be distinguished. With uniform 50 Hz sampling, 25 Hz is the Nyquist frequency. Faster continuous oscillations can produce the same sampled sequence as lower frequencies. A camera observing a rotating wheel provides an analogy: the observed positions alone may not reveal how many full turns occurred between frames. Our added components at 9 and 17 Hz lie below 25 Hz and appear in the later frequency plot. Faster components call for appropriate analog filtering and sampling design before acquisition.

## Build a signal whose components can be explained

The smooth model combines a rising baseline with two bell-shaped peaks. The baseline begins at 0.1 mV and rises at 0.02 mV per second. The first peak is centered at 3 s, with amplitude 1.2 mV and time scale 0.25 s; the second is centered at 7 s, with amplitude 0.8 mV and time scale 0.5 s. Peak amplitude here means the height above the baseline, while the plotted vertical value includes that baseline. The narrower first peak is more sensitive to a wide smoothing window.

$$
y_{\mathrm{clean}}(t)=b_0+b_1t+\sum_{j=1}^{2}A_j\exp\!\left[-\frac{(t-\mu_j)^2}{2w_j^2}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f54c83f4dc801bfa41bd22ff.svg) | Interference-free teaching-model voltage at time t, mV |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, s |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | Baseline intercept, 0.1 mV |
| ![Formula](https://ml-biomat.com/static/agent-math/86ef2a91a3da50f97dc73bcd.svg) | Baseline slope, 0.02 mV/s |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Peak index, 1 or 2; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/cb2c27f1e1ca2cb88caf17da.svg) | Peak amplitude above baseline, 1.2 and 0.8 mV |
| ![Formula](https://ml-biomat.com/static/agent-math/7d98312b42264644b238b90b.svg) | Peak center time, 3 and 7 s |
| ![Formula](https://ml-biomat.com/static/agent-math/f6264b954f8fef8d9872def7.svg) | Peak time scale, 0.25 and 0.5 s |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | Natural exponential; its argument is a dimensionless ratio of squared times |
| ![Formula](https://ml-biomat.com/static/agent-math/52d4c787eb9b2a9aa747a1d4.svg) | Add the voltage contributions of both peaks |

At t=μ_j a peak’s exponent is zero and its contribution equals A_j. Increasing distance from the center makes the exponent more negative and the contribution smaller. At t=3 s, the baseline is 0.16 mV, the first peak contributes 1.2 mV, and the second contributes about 0.8 exp(−32) mV, giving approximately 1.36 mV. The time scale w describes peak width, not the standard deviation of a voltage measurement.

We add a 9 Hz sine component of amplitude 0.12 mV and a 17 Hz cosine component of amplitude 0.035 mV. These are explicitly defined periodic disturbances rather than random noise collected from an instrument. The construction gives identical data on every run and an identifiable origin for both higher-frequency components. Real measurements can combine random noise, baseline drift, and periodic disturbances, which can be investigated using instrument knowledge and repeated records.

At 3 s the smooth model is approximately 1.36 mV: the baseline contributes 0.16 mV and the first peak contributes 1.2 mV, while the second peak contributes a negligible amount. Added interference gives an observed value of approximately 1.395 mV at that instant. Neighboring high and low samples reflect both the genuine peak shape and the periodic terms. Selecting the maximum of the raw array would combine those effects in the reported peak height.

## From averaging neighbors to preserving local curvature

The simplest smoother adds a point and its neighbors and divides by their number. It pools nearby values to estimate the center, attenuating some rapid variations while also pulling a curved peak toward its lower neighbors. In 1964, Abraham Savitzky and Marcel Golay described smoothing and differentiation through local least-squares polynomials. For equally spaced observations and a fixed window, the local fit becomes a reusable set of weights. The calculation remains simple while preserving polynomial shape within the window.

![Original method diagram: five quadratic samples give a 2 mV center under a moving mean and 0 mV under a quadratic local fit. The coefficients show how local fitting becomes repeated weighting in the Savitzky–Golay method.](https://ml-biomat.com/static/tutorials/python-scientific/figures/63e6dbc49c375e566d99f6b7.svg?v=63e6dbc49c37)

Figure 1Original method diagram: five quadratic samples give a 2 mV center under a moving mean and 0 mV under a quadratic local fit. The coefficients show how local fitting becomes repeated weighting in the Savitzky–Golay method.

The five values 4, 1, 0, 1, and 4 occur at relative positions −2, −1, 0, 1, and 2 and lie exactly on a quadratic curve. Their moving mean is two, lifting the center from zero. Fitting a quadratic through them and evaluating it at the center returns zero. The distinction comes from the local model: an average retains one horizontal level, while a quadratic fit permits curvature. Near a peak, that curvature can be part of the feature we want to preserve.

$$
\widetilde y_i=\sum_{k=-m}^{m}c_k y_{i+k},\qquad N=2m+1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8985c98a921e74cb3aa7e8e1.svg) | Smoothed output at position i, mV |
| ![Formula](https://ml-biomat.com/static/agent-math/45b1400cf31b096a28adc5db.svg) | Input value k samples from the center, mV; values outside the record follow the boundary rule |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Current output sample index; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Integer sample offset from the center; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Number of samples on each side of the center; nonnegative integer |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Total window sample count; odd and dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/7b0456e549b6eae9fe9ab8b6.svg) | Fixed coefficient at offset k; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the products of input values and weights across the window |

For five points, m=2 and N=5. Moving-mean weights are all 1/5, giving 2 mV from inputs 4, 1, 0, 1, and 4 mV. Quadratic Savitzky–Golay weights [−3,12,17,12,−3]/35 give 0 mV, retaining the quadratic’s center. Coefficients summing to one preserve a constant signal.

The five-point quadratic smoother has weights −3, 12, 17, 12, and −3, all divided by 35. Negative endpoint weights correct the average’s curvature bias. Their sum remains one, preserving a constant input. Substituting 4, 1, 0, 1, and 4 gives a numerator of −12+12+0+12−12 = 0. Negative weights also allow an output beyond the local input range, particularly near abrupt changes or boundaries, so its interpretation depends on local signal shape.

SciPy’s `savgol_filter` specifies this fit through window length and polynomial degree. We keep degree two fixed and investigate temporal range. The window must contain enough observations to determine the polynomial coefficients, and an odd centered window places the current sample in the middle. A higher degree retains more complicated local variation and can retain more rapid fluctuation as well. The characteristic time scale of the feature guides that choice.

Imagine moving a short ruler along the record. A moving mean compresses everything under the ruler into one horizontal level, whereas a local quadratic allows the short segment to bend. At each position, neighboring observations determine the segment and the algorithm reads its center. Equal sample spacing, a fixed window, and a fixed polynomial degree give the least-squares equations the same geometry everywhere inside the record. The corresponding weights can therefore be calculated once and reused. This is why a method described as repeated local fitting can be implemented efficiently as repeated weighted sums.

## What information does a window need at a boundary?

Inside a record, a centered window has neighbors on both sides. At the first sample, earlier observations are absent, so the calculation needs a boundary rule. We use `mode='mirror'`, reflecting interior values beyond an endpoint without repeating the endpoint itself. If a sequence begins a, b, c, the positions extending to its left correspond successively to b and c. This convention preserves output length and specifies how the first and last values are calculated.

Reflection introduces a local shape assumption. If the real signal still has a slope at an endpoint, its reflected continuation can differ from its physical continuation. Edge results should therefore be read together with the boundary rule. SciPy provides other modes, including local polynomial extrapolation. Using the same mirror rule for both smoothers here keeps the comparison focused on their weights. In an experiment, recording an extra margin around the region of interest can move the analysis away from endpoints and reduce dependence on boundary treatment.

A symmetric window uses values from both earlier and later times, making it suitable for completed records. A real-time controller does not yet have future observations and needs a causal filter or a delay before producing a centered estimate. These workflows have different timing and boundary interpretations. After choosing a useful offline smoother, connect its information requirements to the eventual application.

## Locate peaks with explicit criteria after smoothing

The figure applies a 21-point quadratic Savitzky–Golay filter. Rapid oscillations diminish while both slower peaks remain visible. The lower panel subtracts the known model from the processed result. Five points retain considerable periodic interference; forty-one points produce a more distinct shape bias near the narrow peak. Twenty-one points give a smaller overall error for these specified peak widths, interference frequencies, and sampling interval.

![Top: input with defined interference, known model, and 21-point quadratic Savitzky–Golay output. Red points meet a 0.3 mV prominence and 100-sample separation. Below: errors relative to the model at different window lengths; sampling interval 0.02 s, mirrored boundaries.](https://ml-biomat.com/static/tutorials/python-scientific/figures/1f6dd886740bd48e106af81a.svg?v=1f6dd886740b)

Figure 2Top: input with defined interference, known model, and 21-point quadratic Savitzky–Golay output. Red points meet a 0.3 mV prominence and 100-sample separation. Below: errors relative to the model at different window lengths; sampling interval 0.02 s, mirrored boundaries.

`find_peaks` first identifies local values higher than their neighbors and then applies the requested conditions. `distance=100` is measured in samples, corresponding to 2 s here, and requires retained peaks to be separated by at least that amount. `prominence=0.3` requires a peak to rise at least 0.3 mV relative to its surrounding contour level. Prominence is found from appropriate bases on either side and differs from absolute vertical height. A rising baseline can increase a peak’s height without increasing its prominence by the same amount.

The retained locations are 3.00 and 7.02 s, with values approximately 1.35605 and 1.04352 mV. The second selected sample lies slightly away from the specified 7 s peak center. The rising baseline and residual interference both influence the maximum of the combined curve. Returned peak positions are indices on the sampling grid; multiplying by 0.02 s converts them into time. Finer localization can use an explicitly chosen local peak model or finer acquisition sampling.

$$
\mathrm{RMSE}=\sqrt{\frac1n\sum_{i=1}^{n}(\widetilde y_i-y_{\mathrm{clean},i})^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ffa6620282ab195b6f2fd00.svg) | Root-mean-square error relative to the known teaching model, mV |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of compared samples, 501; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Sample index; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/8985c98a921e74cb3aa7e8e1.svg) | Smoothed sample value, mV |
| ![Formula](https://ml-biomat.com/static/agent-math/a9aa8eda074ad6c3a6f6c7a6.svg) | Interference-free model value at the same time, mV |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum over all compared positions |
| ![Formula](https://ml-biomat.com/static/agent-math/9bcc38017e1856dc949d86bd.svg) | Square root, restoring units of mV |

Squaring prevents signed errors from cancelling; averaging and taking a square root restores the original units. Errors of 0.03 and −0.04 mV give √[(0.0009+0.0016)/2]≈0.035355 mV. The 21-point quadratic filter gives about 0.005705 mV over all 501 samples, combining boundary treatment, residual interference, and shape change.

We can calculate root-mean-square error here because the teaching model without interference is known. The 21-point output gives approximately 0.005705 mV, compared with 0.075340 mV for five points and 0.012498 mV for forty-one. Measured signals generally lack a complete known reference. Independent repeats, calibration signals, established features, or held-out observations can then help evaluate processing. A before–after difference alone contains both removed interference and altered signal shape, so its meaning follows the scientific objective.

A landscape analogy helps distinguish prominence from absolute height. A summit has an elevation above sea level, but its rise above a surrounding valley describes a different feature. For a signal peak, the algorithm identifies bases on both sides and uses the higher base as its reference level. A prominence threshold therefore expresses how strongly an event must stand out locally. A distance threshold expresses how far apart retained events must lie in time. These conditions constrain different aspects of the result, and each deserves a value connected to the process being studied.

## Read a window as a selector of variation rates

A time plot shows when the signal changes. A frequency plot describes components that repeat at different rates: 9 Hz means nine oscillations per second and 17 Hz means seventeen. Both have known origins in this example. The program computes a power spectral density with `periodogram` and explicitly supplies the 50 Hz sampling frequency. Units of mV²/Hz describe squared-amplitude contribution per frequency interval. A Hann window and linear detrending help manage the finite record boundaries and slow baseline.

![Left: one-sided power spectral density using 50 Hz sampling, a Hann window, and linear detrending. Right: sinusoidal amplitude gain calculated directly from filter coefficients, with 9 Hz marked. Gain describes the filter; spectral density describes the finite records.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a51378ffcbd433a4ef486a49.svg?v=a51378ffcbd4)

Figure 3Left: one-sided power spectral density using 50 Hz sampling, a Hann window, and linear detrending. Right: sinusoidal amplitude gain calculated directly from filter coefficients, with 9 Hz marked. Gain describes the filter; spectral density describes the finite records.

A finite-duration record spreads a frequency component across neighboring frequency positions, and the window alters the distribution of peak width and magnitude. These choices therefore belong in its interpretation. The 501-point record has a frequency spacing of approximately 50/501 = 0.0998 Hz, so 9 and 17 Hz do not fall exactly on frequency-grid locations. Local spectral peaks still identify nearby periodic components. We use the density display to compare frequency content before and after smoothing, rather than as an exact estimator of one sinusoid’s amplitude.

The companion panel calculates amplitude gain directly from the smoothing weights. Gain one retains a sinusoid’s amplitude; gain 0.1 reduces it to about one tenth. At 9 Hz, the 21-point window has gain approximately 0.04464, while the 41-point window gives approximately 0.06804. A wider window therefore does not attenuate every frequency more strongly: finite filter responses contain ripples. Considering both target shape and disturbance frequency makes parameter selection more concrete than judging smoothness by appearance.

Amplitude gain and power spectral density describe related quantities at different levels. A filter that multiplies a sinusoidal amplitude by a factor multiplies its power by the square of that factor. The gain panel describes the filter itself and can be calculated without applying it to this particular signal. The spectral panel describes the finite input and output records with the stated spectral-estimation settings. Reading them together separates an algorithm’s response from the frequency content of the data supplied to it.

## A complete program and a linked experiment

The `data` function explicitly generates the smooth model and periodic disturbance. The main loop evaluates two methods at four window lengths and stores each result’s error, value at 3 s, gain at 9 Hz, and peak information. `savgol_coeffs` supplies reusable window weights, `savgol_filter` applies local calculations to the full sequence, and `find_peaks` extracts maxima satisfying the stated conditions. Keeping the stages distinct makes the effect of a parameter change easier to locate.

### Complete Python: signal, smoothing, peaks, and frequency response

Generate an explicit signal, apply native SciPy filters and peak detection, retain numerical errors and arrays, and produce three scientific figures.

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

The experiment displays the complete processed signal, current window weights, and frequency response together. Select a moving mean or quadratic local fit and change its length to see different results from the same 501 records. The value at 3 s and RMSE come from the processed curve. Moving the focus changes which input neighborhood is inspected while leaving the filter result unchanged. The experiment calculates quadratic least-squares weights through a closed-form expression independently checked against the Python SciPy output.

### Link window, weights, and output

Gray is the input with defined interference, black dashed is the known smooth model, and blue is the processed output. Red neighborhood points identify mirrored boundary inputs; sampling interval is 0.02 s.

[Figure: Full signal and current window](https://ml-biomat.com/tutorials/python-scientific/p20/en/#P20-signal)

[Figure: Local weights and input samples](https://ml-biomat.com/tutorials/python-scientific/p20/en/#P20-weights)

[Figure: Frequency response magnitude](https://ml-biomat.com/tutorials/python-scientific/p20/en/#P20-gain)

Start with a five-point quadratic fit and observe the remaining interference. Change to twenty-one points and inspect the 9 Hz gain and narrow-peak shape. At forty-one points, examine the reduced peak near 3 s. Switching to a moving mean makes every weight equal, changing both frequency response and shape bias. Move the focus to the beginning or end to examine the reflected samples that supply the centered window at a boundary.

One useful way to read the program is to follow index 150, which represents 3 s. A 21-point window takes ten neighbors on either side, spanning 2.80 to 3.20 s. The reported 1.35605 mV is the weighted sum of those 21 observed values; the known smooth model at 3 s is approximately 1.36 mV. Moving the focus displays the same kind of calculation at another position. Changing the window or method actually recomputes the trace. Keeping the viewing position separate from the processing parameters makes the interaction easier to interpret and makes individual numerical results traceable.

## Describe processing parameters as reproducible conditions

For measured signals, preserve original times and values, then record the sampling interval, smoothing method, window length, polynomial degree, and boundary mode. Peak results should also preserve detection criteria, minimum separation, prominence, and amplitude units. This lets another reader distinguish a feature in the observations from a result selected under particular processing settings. Comparing several specimens usually calls for consistent physical time scales, which can require different point counts when sampling rates differ.

A rate-of-change analysis also needs the time unit in the differentiation step. Savitzky–Golay supports polynomial derivatives; for a first derivative, supply the actual interval, such as `delta=0.02` here. The result then has units mV/s. Direct differences between neighbors emphasize rapid fluctuations, while a local fit can stabilize a rate estimate over a chosen time range. That same range also combines its internal details, so the relevant process speed still guides the window choice.

A useful processing chain keeps the relationships among observations, assumptions, parameters, and results visible. Time views check location and shape, coefficient views explain the local operation, and frequency views identify retained or attenuated rates of variation. Together they turn a smoother-looking curve into specific conclusions about weakened disturbance, preserved peak shape, and the questions the processed result can answer.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P20.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SciPy: signal processing tutorial](https://docs.scipy.org/doc/scipy/tutorial/signal.html)

   Convolution, filters, and sampled signals

   SciPy BSD-3-Clause; original teaching data and figures
2. [SciPy: Savitzky–Golay filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

   Local polynomials and boundary modes

   SciPy BSD-3-Clause; original teaching data and figures
3. [SciPy: Savitzky–Golay coefficients](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_coeffs.html)

   Weights for a fixed window

   SciPy BSD-3-Clause; original teaching data and figures
4. [SciPy: find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)

   Local maxima, prominence, and separation

   SciPy BSD-3-Clause; original teaching data and figures
5. [SciPy: periodogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html)

   Spectral density, sampling rate, and windows

   SciPy BSD-3-Clause; original teaching data and figures
6. [Savitzky & Golay (1964), Smoothing and Differentiation of Data by Simplified Least Squares Procedures](https://doi.org/10.1021/ac60214a047)

   Original paper on local least-squares smoothing

   Historical and technical reference; no reproduced passage or figure
