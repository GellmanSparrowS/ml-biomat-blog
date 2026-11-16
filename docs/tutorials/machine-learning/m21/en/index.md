# Time Series: Forecasting from the Past

Source: https://ml-biomat.com/tutorials/machine-learning/m21/en/
Language: en

From bakery production to equipment monitoring, connect seasonality, deep forecasting, and uncertainty on one timeline.

## 1. Forecast from the time when the decision must be made

A bakery deciding tomorrow's production, an electricity supplier planning next week's capacity, and a laboratory monitoring equipment temperature all face forecasting problems. The useful output depends on more than predicting the next number. How early must the decision be made? Which observations will have arrived by then? Does predicting too little cost more than predicting too much? A forecast of today's sales produced after closing time cannot guide morning production. Before choosing an algorithm, specify the forecast origin, the horizon, and the time when someone will use the result. These choices determine which information belongs in the input.

A time index is therefore part of the measurement, not an optional table label. The previous row means something different in daily data and business-day data. Time zones, daylight-saving changes, delayed reports, and repeated timestamps can alter the apparent spacing of observations. A missing observation must also be distinguished from a measured zero: a shop that was closed, an open shop that sold nothing, and a broken reporting connection describe different events. Interpolation and centered moving averages deserve particular attention because they can use observations from after the prediction time. Reconstruct when values were measured and when they became available before constructing training windows.

This chapter follows one synthetic demand series with an explicit generating rule. It contains slow growth, weekly and annual variation, correlated noise, and a late change in level. We begin with forecasts that repeat today or last week, then compare smoothing, ARIMA, lagged regression, and a small GRU. The experiment preserves an informative result: methods with a suitable seasonal structure outperform this particular GRU configuration, while previously calibrated intervals lose coverage after the level shift. The comparison lets us connect performance to information and assumptions instead of treating model complexity as a ranking of quality.

## 2. Today's value, last week's pattern, and a changing level

The naive forecast carries the latest observation into the future. It establishes how much can be gained beyond simply expecting persistence. A seasonal naive forecast repeats the most recent season. With a strong weekly pattern in daily data, next Monday is compared with last Monday rather than with the preceding Sunday. If the last seven values were 1 through 7, the next seven seasonal naive predictions are again 1 through 7. This inexpensive rule retains an important piece of structure without estimating many parameters. Compare a new model against it at the same forecast origins and horizons; otherwise an apparent improvement may come from an easier evaluation task.

$$
\hat y_{T+h\mid T}=y_T\quad\text{(naive)},\qquad \hat y_{T+h\mid T}=y_{T+h-m}\quad\text{(seasonal, }1\le h\le m\text{)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | Observed demand at step t, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Integer index of the last available observation; the next forecast origin is T+1. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Positive integer forecast horizon; the seasonal expression here covers one season. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Number of steps in a season, such as m=7 for weekly seasonality in daily data. |
| ![Formula](https://ml-biomat.com/static/agent-math/90cfee39269e6a786b411a86.svg) | Forecast for T+h using information through T, in demand units. |

Naive forecasting carries the last observation forward. Seasonal naive forecasting moves each target back one complete season, retrieving the matching seasonal position. If the latest week is 1,2,3,4,5,6,7, the naive forecast repeats 7 while the seasonal forecast repeats the week. For longer horizons, cycle through the most recent observed season rather than indexing unobserved future values. The vertical bar identifies the information cutoff; it is not division.

Exponential smoothing compresses history into states that are updated as observations arrive. Simple exponential smoothing maintains a level: the new observation receives one fraction of the weight, and the previous level receives the remainder. Expanding the recursion shows that older observations receive geometrically decreasing weights. Starting at a level of 100, observing 120, and choosing a smoothing coefficient of 0.2 gives an updated level of 104. The estimate responds to the change without interpreting every fluctuation as a permanent new baseline. A larger coefficient responds faster but also passes more measurement noise into the state. Holt's extension adds a changing trend, and the Holt–Winters family adds seasonal states.

$$
\begin{aligned}\ell_t&=\alpha(y_t-s_{t-m})+(1-\alpha)(\ell_{t-1}+b_{t-1}),\\ b_t&=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1},\\ s_t&=\gamma(y_t-\ell_t)+(1-\gamma)s_{t-m},\\ \hat y_{t+h\mid t}&=\ell_t+h b_t+s_{t+h-m},\quad 1\le h\le m.\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | Observation at step t, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/a6fe2f82fa2e4afba3c32986.svg) | Updated local level, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d82478c4058da6c98fa79581.svg) | Trend increment per time step, in demand units per step. |
| ![Formula](https://ml-biomat.com/static/agent-math/f0ee2fe79451c957263c10d2.svg) | Additive effect for the current seasonal position, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f49874ef6bc310341e9a984.svg) | Dimensionless smoothing weights for level, trend, and seasonality, each between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/1605fb5ff388cf936c72524e.svg) | Current integer index, seasonal period, and horizon in steps; one step is one day and m=7 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/508f70b1421da086232be5bb.svg) | Forecast future observation, in demand units. |

The first line removes the seasonal effect before blending the observation with the previous level plus trend. The second smooths the change in level. The third assigns the residual after the updated level to seasonality. This is the component recursion used in the script. With previous level 100, trend 2, old seasonal effect 5, observation 110, and weights 0.2,0.1,0.3, the updated level is 102.6, trend 2.06, and seasonal effect 5.72. If the next seasonal position has effect 4, the one-step forecast is 108.66. Multiplying trend per step by the horizon gives a quantity with the same units as the level.

These recursions also reflect the practical setting in which forecasting developed. Inventory and production planning required repeated updates across many demand records, often with limited computing resources. Compressing history into a few states made it possible to revise forecasts as each observation arrived. Holt's trend extension and Winters' seasonal extension broadened the patterns this approach could handle. Later state-space formulations connected component rules with probability models, supporting questions about how uncertainty propagates into the future. This development follows a persistent scientific question: which parts of the observed history must be retained to support the next decision?

Additive seasonality describes an absolute difference, such as 20 extra units every weekend. Multiplicative seasonality describes a proportion, such as a 20% weekend increase. These produce different forecasts as the overall level grows. ETS models express error, trend, and seasonality within a state-space framework; the labels identify these components and support both structural comparisons and predictive distributions. Our code implements a fixed-coefficient additive Holt–Winters component recursion, tracking a level, a trend, and seven seasonal positions. It does not search over the entire ETS family. Each update remains visible, so the reader can trace exactly how today's observation changes tomorrow's state.

Trend and seasonality are useful descriptions, but not mandatory ingredients of every series. A short curved segment may look like a long-term trend, while holidays can move within the calendar. When decomposition is used for exploration, record the smoothing window and boundary behavior. When decomposed components become forecasting inputs, estimate them using only information available at the corresponding origin. The generating components of synthetic data can be plotted directly because they are known by construction. Components extracted from measured data are estimates; one decomposition is not automatically a unique account of the physical causes behind a curve.

## 3. ARIMA and state-space models connect successive observations

ARIMA starts with dependence across time. Does a deviation today contain information about tomorrow's deviation? The autoregressive part uses past values, the moving-average part uses past forecast innovations, and integration refers to differencing followed by accumulation back to the original scale. “Moving average” here means a weighted combination of innovations, not an ordinary average of the last few measurements. Ordinary differencing compares neighboring observations; seasonal differencing compares matching seasonal positions. Differencing can remove certain changing levels, but excessive differencing can introduce unnecessary noise structure. Inspect the series, fitted residuals, and forecasts rather than assuming that more differencing is always helpful.

$$
d_t=y_t-y_{t-1},\qquad d_t=c+\phi d_{t-1}+\varepsilon_t,\qquad \hat y_{T+h\mid T}=y_T+\sum_{j=1}^{h}\hat d_{T+j\mid T}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | Observed demand at step t, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea3b128d75d4d2dd987ffaf5.svg) | Difference between adjacent observations, in demand units for a fixed one-step interval. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Constant in the differenced regression, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | Dimensionless coefficient of the preceding difference. |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c56edde4f1d59f195d1ee.svg) | Zero-mean forecast innovation, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/766c1b88c51440c474b41780.svg) | Last observation index, forecast horizon, and summed future-step index; integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/be0c2f50f513b340b58e1769.svg) | Predicted differences and accumulated demand forecast, both in demand units. |

The orders in ARIMA(1,1,0) specify one autoregressive lag, one difference, and no moving-average innovation term. Future innovations have conditional mean zero, so predicted differences are recursively generated and added to the latest observation. With last value 10, last difference 2, c=0.5, and phi=0.5, the next differences are 1.5 and 1.25; forecasts are 11.5 and 12.75. The script estimates the constant and coefficient by conditional least squares rather than fitting a full likelihood or searching seasonal orders.

The script implements an inspectable ARIMA(1,1,0). It takes first differences, regresses each difference on a constant and its predecessor, predicts future differences recursively, and accumulates them from the latest observed value. If the input increases by exactly one each day, the forecast should continue increasing by one; the script checks that case. This model has no seasonal terms, explaining its weakness against seasonal naive forecasting on our strongly weekly series. Seasonal ARIMA adds seasonal autoregression, differencing, and moving-average structure. Information criteria, residual autocorrelation, and out-of-sample multi-step backtests answer related but distinct questions when choosing those orders.

A state-space model separates an evolving hidden state from its noisy observation. For a temperature sensor, the physical temperature changes over time while measurement error affects the reported number. The prediction step propagates an estimated state and its uncertainty. The update step then uses the discrepancy between a new observation and its prediction to revise that estimate. A filtering estimate at a given time uses current and past observations; a smoothing estimate can use later observations to reinterpret the past. Substituting smoothed historical states for filtered ones in a forecasting evaluation can leak future information.

$$
\begin{aligned}\mu_t^-&=\mu_{t-1},& P_t^-&=P_{t-1}+q,\\ K_t&=\frac{P_t^-}{P_t^-+r},&\mu_t&=\mu_t^-+K_t(y_t-\mu_t^-),\\ P_t&=(1-K_t)P_t^-.\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9d131aa3749f8c85574efde6.svg) | Hidden-level estimate before and after the observation update, in observation units; superscript minus identifies prediction. |
| ![Formula](https://ml-biomat.com/static/agent-math/bff399a88510a283acdfc6d4.svg) | Current observation, in observation units. |
| ![Formula](https://ml-biomat.com/static/agent-math/b59daee6fd36fad95fe4813a.svg) | State-error variance before and after the update, in squared observation units. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4d4462a83beb571480a8e07.svg) | Per-step process-noise variance and measurement-noise variance, in squared observation units. |
| ![Formula](https://ml-biomat.com/static/agent-math/b4090df4ac7ee2164e33cf0b.svg) | Dimensionless Kalman gain between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Discrete time-step index. |

This scalar linear-Gaussian example assumes a random-walk hidden level measured directly with noise. Prediction keeps the mean but adds process variance. Updating weights the observation according to the relative uncertainties. With predicted level 10, predicted variance 4, measurement variance 9, and observation 13, the gain is 4/13. The updated level is approximately 10.923 and its variance is 36/13, approximately 2.769. A more precise measurement has smaller r and receives more weight. This worked mechanism is separate from the six-model benchmark.

This view also provides a natural treatment of missing measurements. State prediction can continue while the observation update is skipped, allowing uncertainty to evolve. Several sensors can observe a shared state through different measurement equations, and trend or seasonal components can be included in the state vector. State-space models and neural networks are compatible: a transition or observation function can itself be learned. The substantive choices are what should evolve, which variation comes from the process, which comes from measurement, and whether those distinctions match the forecasting decision.

## 4. A backtest should replay decisions that were possible then

Randomly shuffling a series before splitting it can place later patterns into the training set for earlier test dates. Rolling-origin evaluation instead advances through the calendar. At each origin, the forecaster sees only preceding information, predicts the next several steps, and is scored when the relevant outcomes become available. An expanding window retains the whole observed past; a sliding window keeps only a recent segment. The first uses more data, while the second may adapt more quickly when the mechanism changes. Preprocessing, feature selection, and parameter estimation must obey the same information boundary as the forecasting model.

Predicting one day ahead and predicting a full week are different tasks. A recursive strategy learns a next-step model and feeds its predictions back as inputs for subsequent steps. It reuses one rule but allows earlier errors to affect later predictions. A direct strategy predicts each horizon separately or produces a vector of future values. It avoids treating its own previous forecast as an observed fact, but must learn the relationships needed at every requested horizon. Our Ridge model forecasts recursively; the GRU outputs seven values together. Reporting errors by horizon makes these design choices visible instead of hiding everything inside one average.

The availability of external variables matters just as much as the availability of the target. Calendar positions, scheduled promotions, and preannounced prices may be known at the origin. Next week's measured temperature and future failure reports usually are not. If weather forecasts are used, preserve the forecast version issued at the time rather than replacing it with weather observed afterward. When an input must itself be predicted, evaluate its errors as part of the full system. Our regression uses past demand, known calendar cycles, and time position. It receives neither future demand nor the future random disturbances used to generate the series.

Four chronological segments have separate jobs. Day indices 0–499 train the models; 500–599 select the GRU checkpoint; 600–699 calibrate prediction intervals; and the segment beginning at 700 evaluates them. A seven-day forecast is issued every seven days, producing 28 origins and 196 test predictions. The final four observations do not form another complete forecast window and are excluded. Ridge and GRU weights remain fixed during testing, while their input histories advance. Smoothing states and ARIMA parameters are updated using the history available at each origin. These are explicit deployment protocols; a comparison of different retraining schedules would be another experiment.

![Top: 900 generated daily observations and four chronological segments; the dashed line marks the level change at day 820. Bottom: local observations after subtracting the known generating trend, compared with the known seasonal component. These components are not supplied to the forecasters.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ba8743eb57fdbfd0e8edc5f7.svg?v=ba8743eb57fd)

Figure 1Top: 900 generated daily observations and four chronological segments; the dashed line marks the level change at day 820. Bottom: local observations after subtracting the known generating trend, compared with the known seasonal component. These components are not supplied to the forecasters.

## 5. Deep forecasting learns reusable temporal representations

Neural forecasting maps a history into an internal representation and uses it to predict future values. A GRU accumulates information through gated states, temporal convolutions examine patterns within local windows, and a Transformer exchanges information across positions through attention. Dividing a long series into patches reduces the number of positions while retaining information within each segment. These models still require a representation of order, calendar position, or sampling intervals. Inputs commonly have the shape batch × history length × variables; outputs have shape batch × forecast horizon × targets. Naming these dimensions describes a working system more precisely than simply saying that it uses a Transformer.

Our small GRU receives 28 daily observations of one variable, maintains a hidden state of dimension 16, and maps its final hidden state to seven outputs through a linear layer. Normalization uses the mean and standard deviation of the training segment only, with the same constants applied afterward. Repeated training windows expose recurring shapes, but growth beyond the training segment and the late level shift require extrapolation or adaptation. Its larger test error suggests concrete follow-up experiments: preserve local level more explicitly, provide calendar information, compare local normalization, or update the model on a defined schedule. Adding layers does not address all of these issues at once.

Time-series foundation models seek transferable structure across many different series. The 2024 Chronos paper represents scaled and quantized values as tokens and learns their distribution with language-model-style training. The original TimesFM work uses a patched decoder attention architecture pretrained on a large time-series corpus. Both aim to help a new forecasting problem benefit from patterns learned elsewhere. Choosing a released model still requires checking its supported frequencies, context and forecast lengths, treatment of multiple variables, and handling of external covariates. The relationship between its training corpus and the intended evaluation dataset is also part of a credible comparison.

Training across multiple series raises the question of what should be shared. Shops in a chain may share a weekend pattern but differ greatly in scale. Devices may share dynamics while their sensors differ in units or noise. A global model can use object identifiers, static attributes, and normalization to learn common structure while retaining differences between objects. Evaluation can include the future of familiar objects and, when relevant, entirely new objects. Those two tests distinguish forecasting within a known setting from transferring to a new one; pooling all observations into a random split would obscure that distinction.

## 6. Describe a range of futures, then check it

A point forecast compresses the possible future into one value. A bakery ordering from an estimated mean has not yet expressed the different costs of unsold bread and unmet demand. Quantile forecasts provide another useful description: a 0.9 quantile aims to place about 90% of outcomes below the predicted value. Such a target can support decisions that place greater cost on underprediction. Quantile loss assigns different weights to errors on the two sides of the prediction. When several quantiles form an interval, their ordering should be checked so that a lower quantile does not exceed a higher one.

$$
e=y-q_\tau,\qquad L_\tau(y,q_\tau)=\begin{cases}\tau e,&e\ge0,\\(\tau-1)e,&e<0.\end{cases}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Observed outcome, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/c744d28123c834669893c23a.svg) | Predicted tau quantile, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Dimensionless quantile level between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Outcome minus prediction; positive means underprediction, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/827f570a764047d02167b369.svg) | Quantile or pinball loss, in demand units. |

At tau=0.9, each unit of underprediction costs 0.9 while each unit of overprediction costs 0.1, moving the optimum above the median. A prediction of 10 incurs loss 1.8 when the outcome is 12 and loss 0.2 when it is 8. Absolute errors match but decision weights differ. For a continuous outcome distribution, expected loss is minimized where the probability weights on the two sides balance, giving the tau quantile. A normal distribution for future outcomes is not required.

Interval evaluation must consider both coverage and width. An extremely wide interval can cover almost every observation while offering little help in making a precise decision. A narrow interval that repeatedly misses the outcome fails in a different way. Useful summaries include the fraction of outcomes inside the interval, average width, and interval scores that penalize misses as well as excessive width. Break these summaries down by horizon, object group, and operating condition. Overall coverage near 90% does not establish the same coverage for long horizons or unusual states. Temporal dependence and changing mechanisms can alter how well calibration errors represent future errors.

$$
\mathrm{coverage}=\frac1n\sum_{i=1}^n\mathbf1\{L_i\le y_i\le U_i\},\qquad \mathrm{width}=\frac1n\sum_{i=1}^n(U_i-L_i)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | Number of evaluated predictions and their integer index. |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Observed demand associated with prediction i, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/8a3f22d38c60047b8702b4f2.svg) | Lower and upper interval endpoints, in demand units. |
| ![Formula](https://ml-biomat.com/static/agent-math/2ac1b98030d2dc2b2acb75cd.svg) | Indicator equal to one when its condition holds and zero otherwise. |
| ![Formula](https://ml-biomat.com/static/agent-math/e7e43dea1f17851acba633c1.svg) | Dimensionless covered fraction between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4121a5409ac039446013e23.svg) | Mean interval width, in demand units. |

Test each outcome against its endpoints and average the resulting zeros and ones. Covering three of four outcomes gives coverage 0.75. Intervals [8,12] and [0,20] both cover an outcome of 10, but widths 4 and 20 provide different precision. The script uses a fixed half-width of about 2.993, so every interval is about 5.986 units wide. Comparing coverage before and after the shift therefore holds the interval width fixed.

The script collects Ridge's absolute errors on a separate calibration segment and chooses a rank-adjusted approximately 90% quantile as a fixed half-width. The resulting interval extends about 2.993 demand units on each side of the forecast. This is an explicit residual-calibration construction; time-series errors are not assumed automatically exchangeable. Its measured test coverage is 0.6429, comprising 0.9167 before the shift and 0.2105 afterward. The fixed width does not respond to the new level bias, and the time plot shows where the missed observations accumulate. Recalibrating an interval, updating a state, and retraining a predictor are distinct actions that should be recorded separately.

## 7. Run six forecasters on the same calendar

The generated series starts from a baseline of 40 and adds 0.018 per day. Weekly and annual oscillations have amplitudes 5 and 3. Noise equals 0.6 times the preceding noise plus a new disturbance with standard deviation 1.5. From day index 820 onward, the level increases by another 6. All values use the same demand unit, and each step represents one day. Known components are retained for explanatory plots, but forecasting functions see only the total observations available at their origins and the prescribed calendar features. They are not handed the true trend, noise process, or future change point.

### Six forecasters with chronological interval calibration

Generate 900 daily observations, train and select chronologically, calibrate intervals, and save measured test errors, horizon errors, and coverage around the shift. Uses NumPy, PyTorch, scikit-learn, and Matplotlib with two CPU threads.

```
"""Chronological forecasts, rolling horizons, and held-out interval calibration."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
HORIZON=7


def seasonal_naive(history, horizon=7, period=7):
    return np.asarray([history[-period+(h%period)] for h in range(horizon)])


def generate():
    rng=np.random.default_rng(21);t=np.arange(900);noise=np.zeros(900)
    for i in range(1,900):noise[i]=.6*noise[i-1]+rng.normal(0,1.5)
    trend=40+.018*t;season=5*np.sin(2*np.pi*t/7)+3*np.sin(2*np.pi*t/365)
    shift=6*(t>=820)
    return trend+season+noise+shift,trend,season,noise


def features(history,t):
    return np.r_[history[-28:],t/900,np.sin(2*np.pi*t/7),np.cos(2*np.pi*t/7),
                 np.sin(2*np.pi*t/365),np.cos(2*np.pi*t/365)]


def holt_winters(history,horizon=7):
    alpha,beta,gamma=.25,.03,.2;m=7
    level=np.mean(history[:m]);trend=(np.mean(history[m:2*m])-level)/m
    season=history[:m]-level
    for t in range(m,len(history)):
        old_level=level;slot=t%m;old_season=season[slot]
        level=alpha*(history[t]-old_season)+(1-alpha)*(level+trend)
        trend=beta*(level-old_level)+(1-beta)*trend
        season[slot]=gamma*(history[t]-level)+(1-gamma)*old_season
    return np.array([level+h*trend+season[(len(history)+h-1)%m] for h in range(1,horizon+1)])


def arima110(history,horizon=7):
    differenced=np.diff(history)
    # Conditional least squares for an AR(1) model of first differences.
    design=np.column_stack([np.ones(len(differenced)-1),differenced[:-1]])
    constant,phi=np.linalg.lstsq(design,differenced[1:],rcond=None)[0]
    value=history[-1];delta=differenced[-1];out=[]
    for _ in range(horizon):
        delta=constant+phi*delta;value+=delta;out.append(value)
    return np.asarray(out)


class DirectGRU(nn.Module):
    def __init__(self):
        super().__init__();self.recurrent=nn.GRU(1,16,batch_first=True);self.output=nn.Linear(16,7)
    def forward(self,x):
        _,hidden=self.recurrent(x);return self.output(hidden[-1])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def text(ch,en):return ch if zh else en
    plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'Arial','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    y,trend,season,noise=generate();torch.manual_seed(21)
    train_end,selection_end,calibration_end=500,600,700
    train_ids=np.arange(28,train_end)
    xx=np.array([features(y[:i],i) for i in train_ids]);yy=y[train_ids]
    scaler=StandardScaler().fit(xx);ridge=Ridge(alpha=10).fit(scaler.transform(xx),yy)
    mean,std=y[:train_end].mean(),y[:train_end].std()
    def windows(origins):
        a=np.array([(y[o-28:o]-mean)/std for o in origins],dtype=np.float32)[:,:,None]
        b=np.array([(y[o:o+7]-mean)/std for o in origins],dtype=np.float32)
        return torch.tensor(a),torch.tensor(b)
    train_origins=np.arange(28,train_end-6);select_origins=np.arange(train_end,selection_end-6,7)
    tx,ty=windows(train_origins);vx,vy=windows(select_origins)
    model=DirectGRU();optimizer=torch.optim.Adam(model.parameters(),lr=.005)
    trace=[];best=float('inf')
    for epoch in range(45):
        model.train();losses=[]
        for ids in torch.randperm(len(tx)).split(64):
            optimizer.zero_grad();loss=nn.functional.mse_loss(model(tx[ids]),ty[ids]);loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad():val=nn.functional.mse_loss(model(vx),vy).item()
        trace.append([float(np.mean(losses)),val])
        if val<best:best=val;checkpoint=copy.deepcopy(model.state_dict())
    model.load_state_dict(checkpoint);model.eval()
    methods=['Naive','Seasonal naive','Holt-Winters','ARIMA(1,1,0)','Ridge','GRU']
    def forecast(origin,method):
        history=y[:origin].copy()
        if method=='Naive':return np.full(7,history[-1])
        if method=='Seasonal naive':return seasonal_naive(history)
        if method=='Holt-Winters':return holt_winters(history)
        if method=='ARIMA(1,1,0)':return arima110(history)
        if method=='Ridge':
            out=[]
            for t in range(origin,origin+7):
                prediction=float(ridge.predict(scaler.transform(features(history,t)[None]))[0]);out.append(prediction);history=np.r_[history,prediction]
            return np.array(out)
        with torch.no_grad():return model(torch.tensor(((history[-28:]-mean)/std).astype(np.float32))[None,:,None]).numpy()[0]*std+mean
    calibration_origins=np.arange(selection_end,calibration_end-6,7)
    test_origins=np.arange(calibration_end,len(y)-6,7)
    target=np.array([y[o:o+7] for o in test_origins]);predictions={m:np.array([forecast(o,m) for o in test_origins]) for m in methods}
    calibration_error=np.abs(np.array([forecast(o,'Ridge')-y[o:o+7] for o in calibration_origins])).ravel()
    rank=min(len(calibration_error),int(np.ceil((len(calibration_error)+1)*.9)))
    radius=float(np.sort(calibration_error)[rank-1])
    lower=predictions['Ridge']-radius;upper=predictions['Ridge']+radius
    covered=(target>=lower)&(target<=upper)
    times=test_origins[:,None]+np.arange(7)[None]
    before=times<820;after=~before
    summary={'test_origins':len(test_origins),'forecast_horizon':7,'test_forecasts':target.size,
             'mae':{m:float(np.mean(np.abs(predictions[m]-target))) for m in methods},
             'mae_by_horizon':{m:np.mean(np.abs(predictions[m]-target),axis=0).tolist() for m in methods},
             'ridge_interval_radius':radius,'coverage':float(covered.mean()),
             'coverage_before_shift':float(covered[before].mean()),'coverage_after_shift':float(covered[after].mean()),
             'gru_selected_epoch':int(np.argmin(np.array(trace)[:,1])+1),
             'latest_training_target':int(train_origins[-1]+6),'first_selection_origin':int(select_origins[0]),
             'latest_calibration_target':int(calibration_origins[-1]+6),'first_test_origin':int(test_origins[0]),
             'seasonal_hand_forecast':seasonal_naive(np.tile(np.arange(1,8),3)).tolist(),
             'arima_constant_increment_forecast':arima110(np.arange(30,dtype=float)).tolist()}
    assert summary['latest_training_target']<summary['first_selection_origin']
    assert summary['latest_calibration_target']<summary['first_test_origin']
    assert np.allclose(arima110(np.arange(30,dtype=float)),np.arange(30,37))
    assert np.array_equal(forecast(700,'Seasonal naive'),y[693:700])
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(args.output/'data.npz',series=y,trend=trend,season=season,noise=noise,
             train_trace=trace,test_origins=test_origins,targets=target,interval_lower=lower,
             interval_upper=upper,calibration_errors=calibration_error,**{m.replace(' ','_'):p for m,p in predictions.items()})
    colors=['#8c9196','#b38b31','#328679','#8d64a6','#176b91','#bd554c']
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,1,height_ratios=[2,1]);ax=fig.add_subplot(gs[0])
    ax.plot(y,color='#476170',lw=.8)
    for a,b,c,l in [(0,500,'#d9e9ef',text('训练','Train')),(500,600,'#f6e9ca',text('模型选择','Selection')),(600,700,'#e3dfed',text('区间校准','Calibration')),(700,900,'#e0eadc',text('测试','Test'))]:
        ax.axvspan(a,b,color=c,alpha=.5);ax.text((a+b)/2,75,l,ha='center')
    ax.axvline(820,color='#bd554c',ls='--');ax.set(xlabel=text('日索引','Day index'),ylabel=text('需求 / 量单位','Demand / quantity units'),ylim=(25,80))
    ax=fig.add_subplot(gs[1]);start=80;ax.plot(np.arange(start,start+56),y[start:start+56]-trend[start:start+56],color='#176b91',label=text('去已知趋势的观测','Observation minus known trend'))
    ax.plot(np.arange(start,start+56),season[start:start+56],color='#bd554c',label=text('生成的季节分量','Generated seasonal component'))
    ax.set(xlabel=text('日索引','Day index'),ylabel=text('偏离 / 量单位','Deviation / quantity units'));ax.legend(ncol=2,fontsize=9)
    fig.tight_layout();save(fig,'timeline')
    fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,2,width_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,0]);ax.plot(times.ravel(),target.ravel(),color='#333',lw=1,label=text('真实观测','Observed'))
    ax.plot(times.ravel(),predictions['Ridge'].ravel(),color='#176b91',lw=1,label='Ridge')
    ax.fill_between(times.ravel(),lower.ravel(),upper.ravel(),color='#176b91',alpha=.15,label=text('校准区间','Calibrated interval'))
    ax.axvline(820,color='#bd554c',ls='--');ax.set(xlabel=text('日索引','Day index'),ylabel=text('需求','Demand'));ax.legend(ncol=3,fontsize=8)
    ax=fig.add_subplot(gs[1,0]);errors=np.abs(predictions['Ridge']-target)
    im=ax.imshow(errors.T,aspect='auto',origin='lower',cmap='magma',extent=[test_origins[0]-3.5,test_origins[-1]+3.5,.5,7.5])
    ax.set(xlabel=text('滚动预测起点（日）','Rolling origin (day)'),ylabel=text('预测步长（日）','Horizon (days)'),yticks=range(1,8));fig.colorbar(im,ax=ax,label=text('绝对误差','Absolute error'))
    ax=fig.add_subplot(gs[:,1]);
    method_labels={'Naive':text('朴素','Naive'),'Seasonal naive':text('季节朴素','Seasonal naive')}
    for m,c in zip(methods,colors):ax.plot(range(1,8),summary['mae_by_horizon'][m],'o-',label=method_labels.get(m,m),color=c,ms=4)
    ax.set(xlabel=text('预测步长（日）','Horizon (days)'),ylabel=text('MAE / 量单位','MAE / quantity units'),xticks=range(1,8));ax.legend(fontsize=9)
    fig.tight_layout();save(fig,'backtest')
    fig,axs=plt.subplots(1,3,figsize=(12,3.8),gridspec_kw={'width_ratios':[1.2,1,1]})
    trace=np.array(trace);axs[0].plot(range(1,46),trace[:,0],label=text('训练','Train'),color='#176b91');axs[0].plot(range(1,46),trace[:,1],label=text('选择窗口','Selection window'),color='#bd554c')
    axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('标准化均方误差','Standardized MSE'),title='GRU');axs[0].legend()
    axs[1].hist(calibration_error,bins=15,color='#176b91',alpha=.8);axs[1].axvline(radius,color='#bd554c',ls='--')
    axs[1].set(xlabel=text('校准绝对残差','Calibration absolute residual'),ylabel=text('预测数','Forecast count'),title=text(f'区间半宽 {radius:.2f}',f'Interval radius {radius:.2f}'))
    vals=[summary['coverage_before_shift'],summary['coverage_after_shift']]
    axs[2].bar([0,1],vals,color=['#176b91','#bd554c']);axs[2].axhline(.9,color='#888',ls='--')
    axs[2].set(xticks=[0,1],xticklabels=[text('变化前','Before shift'),text('变化后','After shift')],ylim=(0,1),ylabel=text('区间覆盖率','Interval coverage'))
    fig.tight_layout();save(fig,'uncertainty')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

Across the 196 test predictions, mean absolute errors are 4.9229 for naive, 1.9687 for seasonal naive, 1.8597 for additive fixed-coefficient Holt–Winters, 4.7632 for nonseasonal ARIMA(1,1,0), 2.6424 for Ridge, and 5.8398 for GRU. The error unit is the demand unit. Holt–Winters has the lowest error in this experiment, while the strong weekly pattern makes seasonal naive a competitive baseline. The simplified ARIMA has no seasonal component, and the GRU's fixed training and input design do not adapt well to the later level. These results describe the stated configurations and identify productive changes for another controlled comparison.

![Twenty-eight test origins each predict seven days. Ridge forecasts, observations, and fixed calibrated intervals appear above the origin-by-horizon error map; the right panel compares MAE by horizon for six methods. Weekly origin spacing links each horizon to a fixed weekly phase.](https://ml-biomat.com/static/tutorials/machine-learning/figures/723b2a97bc6c60c8c9d9421f.svg?v=723b2a97bc6c)

Figure 2Twenty-eight test origins each predict seven days. Ridge forecasts, observations, and fixed calibrated intervals appear above the origin-by-horizon error map; the right panel compares MAE by horizon for six methods. Weekly origin spacing links each horizon to a fixed weekly phase.

Read the forecast origin and horizon before interpreting the colors. The upper-left panel connects successive seven-day forecasts and shows the calibrated interval. The lower-left heatmap separates absolute errors by origin and horizon. The right panel aggregates errors for days one through seven ahead. Since origins advance exactly one week, a given horizon always falls at the same position in the weekly cycle. The resulting curve can vary with seasonal phase rather than increasing monotonically with lead time. Advancing origins daily would mix more weekly phases into each horizon and answer a somewhat different evaluation question.

![GRU training and selection error, 98 calibration residuals and their selected radius, and observed coverage before and after the level change. The 90% line is the target; bar heights are measured test coverage.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e4427a2e0539867373ec1b65.svg?v=e4427a2e0539)

Figure 3GRU training and selection error, 98 calibration residuals and their selected radius, and observed coverage before and after the level change. The 90% line is the target; bar heights are measured test coverage.

The numerical checks have recognizable meanings. Feeding the sequence 0 through 29 into ARIMA(1,1,0) should extend it to 30 through 36. Feeding three repetitions of 1 through 7 into seasonal naive should produce another 1 through 7. The latest training target has index 499 and the first checkpoint-selection origin is 500; the latest calibration target is 697 and the first test origin is 700. These boundary checks accompany the measured errors so that the information available to a forecast can be traced to actual windows. The interactive exercise below lets the same seasonal rule encounter a level shift as the origin moves forward.

## Move the forecast origin across a change

This hand-checkable series combines level 20, weekly offsets [0,2,4,3,1,−1,−2], a linear trend, and a level change at day 42. Forecasts read only observations before the origin. Hide the future, issue a forecast, then reveal outcomes to see how seasonal naive adapts one week after a change.

[Figure: Forecast origin, history window, predictions, and optional future observations](https://ml-biomat.com/tutorials/machine-learning/m21/en/#M21-svg)

## 8. Neighbors influence the series, and the mechanism can change

Many series have spatial structure as well as temporal structure. Congestion on an upstream road affects downstream traffic, nearby weather stations share atmospheric processes, and multiple machines can experience the same power fluctuation. A first model can use lagged neighboring observations as external features. A graph network can then aggregate spatial relationships while a temporal model describes their evolution. Reporting delays still apply: a station's observation is usable only after it has actually arrived. Forecasts across shops, regions, and national totals may also need reconciliation so that component predictions add to their aggregate or obey a relevant conservation constraint.

An anomaly and a change point ask different questions. A single sensor spike may be a transient error; a persistent rise in the mean may indicate a changed operating regime. Anomaly detection can compare a new observation with a forecast interval constructed from the past. Change-point detection asks whether the mean, variance, or dynamic parameters have shifted persistently. Online cumulative residuals, comparisons between recent windows, and offline segmentation have different detection delays and assumptions. A detected change may call for a sensor check, a shorter training window, a state update, or model retraining, depending on whether the measuring system or the observed process changed.

A useful forecasting project ultimately produces a replayable forecast archive. Each record identifies when the forecast was issued, the model version, the latest available observation, the target timestamps, the interval-calibration rule, and when outcomes were added. Relating errors to horizon, seasonal position, and changing conditions helps determine whether to keep using a model or modify it. The central problem is not merely to fit a line through an existing curve. It is to make each computation about the future from the information that a real decision maker could have possessed at that time.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M21.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Forecasting: Principles and Practice — forecasting tools](https://otexts.com/fpp3/toolbox.html)

   Open textbook explanations of naive forecasts and rolling-origin evaluation.
2. [Forecasting: Principles and Practice — exponential smoothing](https://otexts.com/fpp3/exponential-smoothing.html)

   Smoothing, trends, seasonality, and state-space forms.
3. [Forecasting: Principles and Practice — ARIMA](https://otexts.com/fpp3/arima.html)

   Differencing, innovations, and seasonal ARIMA.
4. [Chronos: Learning the Language of Time Series](https://arxiv.org/abs/2403.07815)

   Original work on scaling, quantization, and probabilistic forecasting.
5. [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688)

   Original TimesFM patched-decoder design.
