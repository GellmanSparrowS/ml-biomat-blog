# Organizing Time and Multiple Data Batches

Source: https://ml-biomat.com/tutorials/python-scientific/p14/en/
Language: en

Connect start times, elapsed time, bin averages, and observation coverage in one clear analysis.

## How can two heating experiments be compared in time?

Two batches enter a heating apparatus at different times, and both temperature records rise gradually from room temperature. The first batch starts at nine o'clock; the second starts seven minutes later. Plotting their records against clock time shifts the second curve to the right. To ask which batch heats faster after starting, compare their fifth or tenth elapsed minute instead. A time column therefore does more than supply a horizontal plotting coordinate: it determines which observations can be compared and what interval a mean describes. This chapter uses two irregularly sampled teaching records to develop time parsing, batch alignment, bin averages, and rolling windows.

Batch A is observed at elapsed times 0, 1, 2.5, 5, 6, 9, 15, 16, and 19 min, with temperatures 22, 26, 35, 47, 51, 58, 67, 69, and 71 °C. Batch B uses times 0, 2, 3, 5, 8, 9, 15, 17, and 19 min, with temperatures 21, 29, 35, 44, 53, 55, 65, 68, and 70 °C. Each time–temperature pair is one observation, giving 18 records in total. Unequal intervals and the gap between 10 and 15 min make the behavior of bins and windows visible. The code uses a fixed example calendar day to create timestamps; all records follow these stated values.

Organizing time resembles comparing two races that start at different clock times. Clock time tells who started first, while elapsed time identifies the stage reached after each start. Both coordinates preserve useful information and answer different questions. An experiment also needs a defined starting event: turning on a heater, inserting a sample, and starting acquisition may occur at different moments. Decide which event starts the process clock before aligning curves, so “the fifth minute” has the same meaning across batches.

## Treat time as part of observation identity

In his 2010 paper introducing pandas, Wes McKinney discusses practical problems involving differently sized datasets, missing observations, and date handling. Series covering different date ranges should not be added merely because their values occupy the same row positions. Missing observations also need to remain represented in the structure. One design choice was to make the structures aware of time labels without forcing every record onto a fixed frequency first. The same idea applies directly to irregular experimental records: retain when observations actually occurred, then explicitly choose an alignment or aggregation when it is needed.

The fourth element of an ordinary array identifies a position; a time label also identifies when its value occurred. A time-indexed series binds a temperature to a timestamp. Selecting an interval, inspecting time differences, or grouping by five-minute periods can then operate on those labels. An index is a retrieval label attached to each record, and it need not be an integer beginning at zero. Time labels bring calendar rules and duration operations into the data structure, alongside the continuing need for correct units, time zones, and experimental event definitions.

![The same teaching temperature records in two time coordinates. Left: B starts 7 minutes after A. Right: subtracting each batch’s own start aligns process stage. Connecting segments trace neighboring records without adding observations between them. This is one explicit alignment supported by labeled temporal data.](https://ml-biomat.com/static/tutorials/python-scientific/figures/fe0608f4a920390dbcd9f892.svg?v=fe0608f4a920)

Figure 1The same teaching temperature records in two time coordinates. Left: B starts 7 minutes after A. Right: subtracting each batch’s own start aligns process stage. Connecting segments trace neighboring records without adding observations between them. This is one explicit alignment supported by labeled temporal data.

The left panel uses clock time and preserves the fact that B started seven minutes later. The right subtracts each batch's start time to align process age. Both panels use exactly the same 18 temperatures. The comparison separates a change in the coordinate used for comparison from a change in observations. Here temperature is unchanged and no observations are added inside gaps. Connecting segments trace record order; whether temperature varied linearly between adjacent observations requires an additional process assumption.

An alignment should follow an interpretable experimental event. Sliding curves until their peaks coincide can remove a real onset delay or response-time difference along with the visual offset. After alignment by a defined start, retain calendar timestamps as well, because they can reveal environmental changes that occurred at the same actual time. Keeping calendar and elapsed time together preserves more of the experimental meaning than retaining a newly numbered horizontal axis alone.

## Convert date text into time that can be calculated

A time field in a CSV often begins as text, perhaps containing a date, hour, and minute. Text can be displayed but does not automatically support a meaningful calculation of minutes between observations. `pd.to_datetime` parses it into a temporal value. When the format is known, provide `format` to assign the year, month, and day to specified positions. A string such as “01/02” can mean January 2 or February 1 under different conventions. Date format belongs to the data definition and should be established when reading the file.

A timestamp describes an instant, while a duration describes the separation between instants. pandas supports date-time and duration types for these roles. Subtracting timestamps gives a duration; adding a duration to a timestamp gives another instant. This is the distinction between “Monday at nine o'clock” and “five minutes later.” The example creates batch starts as explicit UTC timestamps and adds the stated elapsed minutes to obtain observation times, so the elapsed-time calculation can also be checked in reverse.

A time zone connects a clock reading to an actual instant. Text with a specified UTC offset can be standardized using `utc=True`. If input text has no time-zone information, that option interprets it as UTC; it does not infer where the instrument was located. For local clock readings with a known time zone, establish that zone before converting to a shared basis. `tz_localize` gives previously unzoned readings their time context, whereas `tz_convert` changes the clock representation of instants that already have a zone. These operations solve different problems.

Parsing failures should remain traceable to source records. With `errors="coerce"`, unrecognized text becomes `NaT`, the missing temporal value. A missing-value mask can then isolate those rows for format correction or completion. Simply dropping them can change the record's time coverage. After parsing, inspect earliest and latest times, within-batch order, and duplicate timestamps. Repetition might represent several sensors or repeated imports; the appropriate treatment follows observation identity.

## Construct elapsed time inside each batch

Elapsed time begins at the start of the relevant batch. Since A and B have different start times, each subtraction must use its own start rather than the earliest timestamp in the combined table. Otherwise B's first record would appear at seven elapsed minutes when B has just started. The full script retains `batch`, `timestamp`, and `start` on each row before computing the difference. Together those fields explain the process stage associated with each temperature.

$$
\Delta t_i=T_i-T_{0,b}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Observation index within the batch; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Batch identifier, such as A or B; no units |
| ![Formula](https://ml-biomat.com/static/agent-math/d337cf254934852ef394972a.svg) | Observation timestamp in a common time zone and time unit |
| ![Formula](https://ml-biomat.com/static/agent-math/5e26e8726da71c7cc497d4b0.svg) | Start timestamp of batch b on the same time basis |
| ![Formula](https://ml-biomat.com/static/agent-math/f9b2449534eeccba7530b307.svg) | Elapsed time since this batch started, expressed in min here |

Batch B starts at 09:07, so its 09:12 observation has elapsed time 5 min. Batch A starts at 09:00, making 09:05 the same process age. The program subtracts timestamps to obtain a duration, converts it to seconds with total_seconds(), and divides by 60 to obtain minutes. Both timestamps must refer to actual instants on a common time basis.

`.dt.total_seconds()` converts the complete duration into seconds, including contributions spanning hours or days. Division by 60 then gives minutes. This is different from extracting the minute field of a clock, which restarts at zero every hour. A process continuing from 09:58 to 10:03 lasts five minutes; subtracting the displayed minute fields, 3 minus 58, produces an incorrect negative number. Dedicated temporal types allow the relevant carry and calendar rules to participate in the calculation.

Sort by batch and time before neighboring differences, rolling windows, or nearest-time lookup. Within-batch order describes process order. If the last A record and the first B record are treated as one sequence, a rolling mean can mix temperatures from two specimens. The result may look smooth while its scientific object has changed. Grouping therefore defines a boundary for temporal operations. Process each batch separately and concatenate the results, or use an explicitly grouped window interface; the essential requirement is that a window stays inside the intended experiment.

Aligning elapsed time does not require sampling at identical moments. A has a record at 2.5 min and B at 3 min; preserve both as observed. A common grid can later be constructed through binning, interpolation, or model prediction, each with a different meaning. Binning aggregates observations in an interval. Interpolation constructs intermediate values from neighboring observations. Model prediction describes the process through a chosen function. We begin with binning because every summary can be traced directly to the observations assigned to its interval.

## Which observations belong to a five-minute average?

Binning divides a time axis into intervals and summarizes the observations assigned to each. A width of 5 min and reference of zero give intervals [0,5), [5,10), [10,15), and [15,20). The square bracket includes the left endpoint, while the round bracket excludes the right endpoint. An observation at exactly 5 min therefore enters the second bin without also being counted in the first. This endpoint convention assigns each record unambiguously.

$$
k_i=\left\lfloor\frac{t_i-a}{h}\right\rfloor,\qquad a+k_i h\le t_i<a+(k_i+1)h
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | Elapsed time of observation i, min |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Offset of the bin reference, min |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Positive bin width, min |
| ![Formula](https://ml-biomat.com/static/agent-math/e8755a0f9e8b8e36aada3a9f.svg) | Integer index of the assigned bin; may be negative, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/9441613214b6ab5fddf9ec85.svg) | Floor: the largest integer not greater than the enclosed value |

With h=5 min and a=0, t=5 min gives k=1 and enters [5,10). The left endpoint is included, while the right belongs to the next bin. At offset a=2 min, t=0 gives (0−2)/5=−0.4; flooring gives −1 and bin [−3,2). A negative left boundary follows from the bin coordinate system while original observations still begin at 0 min.

pandas `resample` connects time grouping to a subsequent aggregation. The option `closed="left"` declares left-inclusive membership, while `label="left"` labels each output row with the left boundary. Label position and membership are separate choices: moving a label to the right boundary does not automatically reassign boundary observations. The example also specifies a reference and offset, giving batches the same elapsed-time boundaries instead of independently starting bins at an incidental first sampling time.

A bin mean uses the observations that actually enter that bin. A's first bin contains times 0, 1, and 2.5 min with temperatures 22, 26, and 35 °C. Its second contains times 5, 6, and 9 min with temperatures 47, 51, and 58 °C. Summing temperatures and dividing by record count gives approximately 27.6667 and 52 °C. Keeping `mean` beside `count` retains both the numerical summary and the number of observations supporting it.

$$
\bar y_k=\frac{1}{n_k}\sum_{i\in I_k}y_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Time-bin index; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/db1af26db044259d897bbc6c.svg) | Set of indices of observations in bin k with nonmissing temperatures; no units |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Observation index in that set; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | Count of nonmissing temperature records in the bin; positive dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Recorded temperature for observation i, °C |
| ![Formula](https://ml-biomat.com/static/agent-math/c752241b25f7282c420ab050.svg) | Arithmetic mean of observed temperatures in the bin, °C |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the temperature records belonging to the bin |

Batch A contributes 22, 26, and 35 °C to [0,5), giving 83/3≈27.6667 °C from 3 records. The [10,15) bin has zero records, so the denominator is undefined and its mean remains missing. Each observation has equal weight here; under irregular sampling this differs from an average weighted by duration.

Under irregular sampling, this arithmetic mean gives each observation equal weight. A more densely sampled stage contributes more readings to the mean. Estimating mean temperature over elapsed time requires an additional account of how long each value represents or an integration rule for changes between observations. Preserve the meaning of the observation average before introducing that different quantity. Similarly, temperature readings often suit averaging, whereas some counts accumulated over intervals may suit summation. The definition of the measured quantity determines the aggregation operation.

## Retain gaps alongside the mean curve

Batch A has no records in [10,15) min. Its count is zero and its mean remains missing. The observation at 15 min belongs to the next interval under the declared endpoint convention. A missing mean differs fundamentally from 0 °C: one says that no observations support the calculation, while the other is a specific temperature. Filling the missing mean with zero would create a sudden cooling event followed by reheating. The figure breaks the mean curve at the empty bin and displays a count of zero below it, making the gap readable.

![Five- and ten-minute bins for batch A. Each mean is placed at its bin center, with record counts below. The empty \[10,15) interval breaks the five-minute mean curve. A ten-minute bin groups that empty interval together with later observed times.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e45da6b99951334b13d1d237.svg?v=e45da6b99951)

Figure 2Five- and ten-minute bins for batch A. Each mean is placed at its bin center, with record counts below. The empty [10,15) interval breaks the five-minute mean curve. A ten-minute bin groups that empty interval together with later observed times.

Changing to ten-minute bins gives six records in [0,10) and three in [10,20), so both bins have means. The original [10,15) gap remains, but a wider bin now contains it together with later observed times. A more continuous-looking line between two means does not imply that missing observations have appeared. Compare original time locations and counts as well as the means when changing bin width. Wider bins can stabilize a summary while reducing how precisely it locates changes in time.

Forward filling is an explicit imputation rule: continue using the latest observation at subsequent times. This can describe a state held until its next update, such as an instrument setting. Applied to a continuously changing sample temperature, it assumes that the temperature stayed constant over that interval. Linear interpolation adopts a different assumption, placing intermediate values on straight segments between observations. Before filling, define what analysis the constructed values will support and distinguish them from observed values. This example keeps the original gap visible so the available coverage can be understood first.

Record count is also different from independent sample count. Many readings from one sensor describe a minute more finely without creating additional specimens; neighboring readings may be correlated. Retaining a bin's count first explains how many records enter its summary. Estimating uncertainty in a group difference requires the actual independent units, such as separate samples or experimental batches. This follows the previous chapter's distinction between original observations and rows produced by table operations.

## The last three records may span much longer than five minutes

A rolling window moves with the current record rather than dividing time into fixed bins. A mean of the last three records selects the current record and the preceding two. A mean over the last five minutes selects records by their actual timestamps. With regular sampling and corresponding settings the two can be close; unequal intervals and gaps can make their process coverage substantially different.

![Two rolling averages of the same irregular records. At 15 min, the last three records occur at 6, 9, and 15 min, while the trailing five-minute interval (10,15\] contains the record at 15 min alone. Lines trace calculated results without filling the original observation gap.](https://ml-biomat.com/static/tutorials/python-scientific/figures/b0f6ce246e5e1b9e597c0df7.svg?v=b0f6ce246e5e)

Figure 3Two rolling averages of the same irregular records. At 15 min, the last three records occur at 6, 9, and 15 min, while the trailing five-minute interval (10,15] contains the record at 15 min alone. Lines trace calculated results without filling the original observation gap.

At 15 min, the last three records occur at 6, 9, and 15 min, with temperatures 51, 58, and 67 °C. Their mean is approximately 58.6667 °C, and they span nine minutes. A five-minute trailing window that includes the current time but excludes the left boundary is (10,15]. It contains the single 67 °C observation at 15 min, so its mean is 67 °C. Both values follow their stated rules accurately; the difference lies in whether window length means a number of records or a duration.

In code, `rolling(3)` means three records and `rolling("5min")` means a five-minute span. Time-based windows need a temporal index in chronological order. `min_periods` sets the minimum number of nonmissing records required for an output. The example explicitly uses one, allowing calculation at the beginning when only one observation is available and making partial-window behavior visible. An analysis can choose a larger minimum according to its task, while retaining information about actual window coverage.

Rolling averages make local variation smoother, but successive windows reuse many of the same observations. Their output points are therefore dependent. Wider windows average over more short-term variation and can delay the apparent response of a trend. A window ending at the current time supports calculations from data already available; a centered window also uses future observations relative to that time and suits retrospective smoothing. Decide whether the operation supports sequential interpretation or a completed-record review before explaining the position of its output curve.

## Move bin boundaries and follow the changing summaries

The experiment below separates binning into three linked views. Original records remain in the upper plot, with background bands marking intervals. The lower plots show bin means and record counts. Selecting a bin highlights its records and summaries in red, and the page lists the time and temperature of every member. Width determines the duration summarized; offset determines where the boundaries begin. Both affect the assignment of observations near a boundary.

## Move time bins and trace observations into their means

Changing bin width or reference offset updates observations, bin means, and counts together. Select an interval to highlight its records in red. Horizontal mean segments summarize whole bins; empty bins remain blank.

[Figure: Original temperature records and time-bin membership](https://ml-biomat.com/tutorials/python-scientific/p14/en/#P14-records)

[Figure: Mean observed temperature in each bin](https://ml-biomat.com/tutorials/python-scientific/p14/en/#P14-means)

[Figure: Actual observation counts in each bin](https://ml-biomat.com/tutorials/python-scientific/p14/en/#P14-counts)

Keep batch A and five-minute width, then select [10,15) to see the original observations, mean, and count consistently show an empty bin. Change the offset from zero to two minutes. The first interval becomes [−3,2), containing the 22 and 26 °C records at zero and one minute, with mean 24 °C. The observations still begin at zero; the negative left boundary results from shifting the bin grid relative to that start. Now choose ten-minute width and inspect how the summaries compress temporal detail while the original points stay in place.

Different bin definitions summarize the same records differently. Choose a rule from the process time scale, sampling coverage, and scientific question, then preserve width, reference, and endpoint convention in the calculation. Choosing boundaries solely to maximize an apparent group difference makes that difference depend on presentation. Retaining original observations alongside reasonable alternative scales helps distinguish persistent features from changes mainly caused by moving a bin boundary.

## Make the complete time calculation reproducible

The full script separates data creation, aggregation, and the main calculation. `teaching_data` specifies times and temperatures for both batches and parses timestamps with UTC information. `aggregate` places elapsed times on a shared example time reference, then uses `resample` to obtain means and counts. `main` evaluates bin widths and offsets within each batch before comparing the two rolling windows. The common reference makes bin boundaries consistent while original clock timestamps remain in the output table.

### Complete example: parsing, batch alignment, resampling, and rolling windows

Runs pandas time types, resample, and rolling directly. Both batches have explicitly listed times and temperatures; outputs retain original records, bin tables, rolling results, and numerical summaries.

```
"""Align two irregular teaching time series and inspect aggregation and coverage."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

BLUE,RED,INK,GRAY='#28658c','#b64a35','#202e39','#71808b'
EPOCH=pd.Timestamp('2000-01-01T00:00:00Z')


def teaching_data():
    definitions={'A':([0,1,2.5,5,6,9,15,16,19],[22,26,35,47,51,58,67,69,71],'2000-01-01T09:00:00Z'),
                 'B':([0,2,3,5,8,9,15,17,19],[21,29,35,44,53,55,65,68,70],'2000-01-01T09:07:00Z')}
    frames=[]
    for batch,(elapsed,temperature,start) in definitions.items():
        stamp=pd.Timestamp(start)+pd.to_timedelta(elapsed,unit='min')
        frames.append(pd.DataFrame({'batch':batch,'timestamp':stamp.astype(str),'start':start,
                                    'temperature_C':temperature}))
    frame=pd.concat(frames,ignore_index=True)
    frame['timestamp']=pd.to_datetime(frame['timestamp'],utc=True)
    frame['start']=pd.to_datetime(frame['start'],utc=True)
    frame['elapsed_min']=(frame['timestamp']-frame['start']).dt.total_seconds()/60
    return frame.sort_values(['batch','timestamp']).reset_index(drop=True)


def aggregate(frame,width,offset=0):
    relative_index=EPOCH+pd.to_timedelta(frame['elapsed_min'],unit='min')
    signal=pd.Series(frame['temperature_C'].to_numpy(dtype=float),index=relative_index)
    grouped=signal.resample(f'{width}min',origin=EPOCH,offset=pd.Timedelta(minutes=offset),
                            closed='left',label='left').agg(['mean','count'])
    grouped['left_min']=(grouped.index-EPOCH).total_seconds()/60
    grouped['right_min']=grouped['left_min']+width
    return grouped.reset_index(drop=True)


def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    def tr(a,b):return a if language=='zh' else b
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'font.size':11,
        'axes.labelsize':12,'axes.titlesize':13,'axes.titleweight':'bold','axes.spines.top':False,
        'axes.spines.right':False,'text.color':INK,'svg.fonttype':'none','svg.hashsalt':'P14'})
    data=teaching_data();data.to_csv(output/'thermal-records.csv',index=False)
    cases={}
    for batch,frame in data.groupby('batch',sort=True):
        for width,offset in [(5,0),(5,2),(10,0),(2,0)]:
            result=aggregate(frame,width,offset)
            result.to_csv(output/f'bins-{batch}-{width}-{offset}.csv',index=False)
            records=[{'left_min':float(r.left_min),'right_min':float(r.right_min),
                      'mean_C':None if pd.isna(r.mean) else float(r.mean),'count':int(r.count)}
                     for r in result.itertuples(index=False)]
            cases[f'{batch}-{width}-{offset}']={'bins':records,'empty_bins':sum(r['count']==0 for r in records),
                'total_observations':sum(r['count'] for r in records)}
    a=data.loc[data['batch'].eq('A')].copy()
    a['row_window_mean']=a['temperature_C'].rolling(3,min_periods=1).mean()
    time_signal=pd.Series(a['temperature_C'].to_numpy(dtype=float),index=pd.to_timedelta(a['elapsed_min'],unit='min'))
    a['time_window_mean']=time_signal.rolling('5min',min_periods=1,closed='right').mean().to_numpy()
    a.to_csv(output/'rolling-A.csv',index=False)
    at15=a.loc[a['elapsed_min'].eq(15)].iloc[0]
    assert abs(cases['A-5-0']['bins'][0]['mean_C']-83/3)<1e-12
    assert cases['A-5-0']['bins'][2]['count']==0
    assert cases['A-5-0']['bins'][2]['mean_C'] is None
    assert at15['row_window_mean']==(51+58+67)/3
    assert at15['time_window_mean']==67
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',metadata={'Date':None})
        fig.savefig(output/f'{name}-{language}.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.6),layout='constrained',sharey=True)
    origin=pd.Timestamp('2000-01-01T09:00:00Z')
    for batch,frame in data.groupby('batch'):
        color=BLUE if batch=='A' else RED
        clock=(frame['timestamp']-origin).dt.total_seconds()/60
        axes[0].plot(clock,frame['temperature_C'],'o-',color=color,ms=5,lw=1.3,label=tr('批次','Batch ')+batch)
        axes[1].plot(frame['elapsed_min'],frame['temperature_C'],'o-',color=color,ms=5,lw=1.3,label=tr('批次','Batch ')+batch)
    axes[0].xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'09:{int(v):02}'))
    axes[0].set(xticks=np.arange(0,31,5),xlabel=tr('钟表时间 / UTC','Clock time / UTC'),
                title=tr('钟表时间保留启动先后','Clock time retains start order'))
    axes[1].set(xlabel=tr('从各自启动起经过的时间 / min','Elapsed time from each start / min'),
                title=tr('经过时间对齐过程阶段','Elapsed time aligns process stage'))
    axes[0].set_ylabel(tr('温度 / °C','Temperature / °C'))
    for ax in axes:ax.legend(frameon=False);ax.set_ylim(15,78)
    save(fig,'alignment')
    fig,axes=plt.subplots(2,2,figsize=(12.4,8),sharex='col',gridspec_kw={'height_ratios':[2,1]},layout='constrained')
    for j,width in enumerate([5,10]):
        binned=aggregate(a,width)
        centers=(binned['left_min']+binned['right_min'])/2
        axes[0,j].scatter(a['elapsed_min'],a['temperature_C'],s=35,color=GRAY,label=tr('原始记录','Original records'),clip_on=False)
        axes[0,j].plot(centers,binned['mean'],'o-',color=BLUE,lw=2,label=tr('箱内观测均值','Mean of observations in bin'))
        axes[0,j].set(ylim=(15,78),title=tr(f'{width}分钟分箱',f'{width}-minute bins'))
        axes[0,j].legend(frameon=False,fontsize=9)
        axes[1,j].bar(centers,binned['count'],width=width*.8,color=BLUE)
        axes[1,j].set(xlim=(0,20),ylim=(0,7),xticks=np.arange(0,21,5),xlabel=tr('经过时间 / min','Elapsed time / min'))
        for x,count in zip(centers,binned['count']):axes[1,j].text(x,count+.15,str(count),ha='center',color=RED if count==0 else INK)
        for ax in axes[:,j]:
            for edge in binned['left_min']:ax.axvline(edge,color='#dce3e8',lw=.7,zorder=0)
    axes[0,0].set_ylabel(tr('温度 / °C','Temperature / °C'));axes[1,0].set_ylabel(tr('记录数','Observation count'))
    save(fig,'coverage')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.7),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
    axes[0].scatter(a['elapsed_min'],a['temperature_C'],s=30,color=INK,label=tr('原始记录','Original records'),zorder=4)
    axes[0].plot(a['elapsed_min'],a['row_window_mean'],'o-',color=RED,label=tr('最近3条记录','Last 3 records'))
    axes[0].plot(a['elapsed_min'],a['time_window_mean'],'s-',color=BLUE,label=tr('最近5分钟','Trailing 5 minutes'))
    axes[0].set(xlabel=tr('经过时间 / min','Elapsed time / min'),ylabel=tr('温度 / °C','Temperature / °C'),
                title=tr('窗口长度可以按行，也可以按时间','Window length can mean rows or elapsed time'))
    axes[0].legend(frameon=False,fontsize=10)
    axes[1].set_axis_off()
    axes[1].text(.03,.94,tr('在15分钟这一刻','At elapsed time 15 min'),fontsize=14,weight='bold')
    lines=[tr('最近3条记录：6、9、15 min','Last 3 records: 6, 9, 15 min'),
           tr('温度：51、58、67 °C','Temperatures: 51, 58, 67 °C'),
           tr('均值 = 58.67 °C','Mean = 58.67 °C'),'',
           tr('最近5分钟：(10, 15] min','Trailing 5 min: (10, 15] min'),
           tr('区间内有1条记录：67 °C','One observation in the interval: 67 °C'),
           tr('均值 = 67.00 °C','Mean = 67.00 °C')]
    for i,line in enumerate(lines):axes[1].text(.03,.79-i*.105,line,fontsize=11,color=RED if i<3 else BLUE)
    save(fig,'windows')
    summary={'data_kind':'explicit teaching timestamps and temperatures','n_records':len(data),
        'start_delay_B_min':7,'cases':cases,'at_15_min':{'row_window_mean_C':float(at15['row_window_mean']),
        'time_window_mean_C':float(at15['time_window_mean'])},'versions':{'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();main(args.output,args.language)
```

After execution, `thermal-records.csv` retains the 18 original teaching records, their start timestamps, and elapsed times. Each bin table includes left and right boundaries, mean, and count. The file `rolling-A.csv` places both rolling results beside their original timestamps. The numerical summary gives four bins for A with a five-minute width and zero offset, with counts 3, 3, 0, and 3. At 15 min, the two rolling means are approximately 58.6667 and 67 °C. These results can be checked directly from the records listed in the chapter.

For your own records, establish correct parsing, a shared time basis, and a clear starting event before sorting within batches and calculating elapsed time. Then choose individual observations, fixed bins, or rolling windows according to the question. Retain observation identity, interval rules, and counts with each derived result. A scientific figure can then show a temperature trajectory while also explaining how each plotted summary came from the experiment. The next chapter follows these meanings into coordinates, graphical objects, and saved scientific figures.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P14.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pandas: Time series / date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html)

   Timestamps, durations, time zones, bin endpoints, and labels.

   pandas BSD-3 documentation; original case and figures
2. [pandas: Windowing operations](https://pandas.pydata.org/docs/user_guide/window.html)

   Rolling windows defined by row count or elapsed duration.

   pandas BSD-3 documentation
3. [McKinney (2010), Data Structures for Statistical Computing in Python](https://github.com/scipy-conference/scipy_proceedings_2010/blob/master/papers/mckinney/pandas_scipy.rst)

   The original author discusses alignment, missing observations, and temporal structures without forced fixed frequency.

   Historical facts and design ideas paraphrased; original diagrams, no source code or image reproduced
