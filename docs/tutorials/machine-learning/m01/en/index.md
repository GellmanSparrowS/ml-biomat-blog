# Problems, data and learning tasks

Source: https://ml-biomat.com/tutorials/machine-learning/m01/en/
Language: en

Follow a day of bicycle rentals to define observations, information timing and a target, then build three inspectable forecasting baselines.

## Begin with tomorrow's decision

A bicycle station may look quiet before the morning rush, but an operator already has to plan transport and maintenance. Counting all rentals after the day has ended produces a report. Estimating those rentals before the day begins produces a forecast. Deciding how to move bicycles in response is a further decision problem. These activities may use similar-looking tables, yet they answer different questions. This chapter follows that distinction from a real rental dataset to an experiment that can be inspected. By the end, you should be able to explain what one row represents, when its answer becomes available, and which simple alternative a prediction model is expected to improve upon.

Write the task as a sentence with an object and a time: “Before each day begins, use information already available to predict the total number of rentals in this citywide system that day.” Three parts matter. “Each day” defines the duration of one observation. “Already available” determines which fields can enter the model. “Total number of rentals” defines the output and its units. A rental is an event, and the same bicycle can be rented several times in one day. Rental counts therefore differ from fleet size. Turning demand forecasts into vehicle allocations requires station locations, return flows, bicycle turnover and transport capacity as well. A precise target gives the algorithm a definite job.

A useful analogy is a recipe notebook. Each row describes a meal you have cooked, the ingredients and cooking conditions are inputs, and the diners' rating is an outcome. When predicting the rating of a new meal, you cannot put the rating it later receives into the ingredient list. A learning program will use the columns you provide quite faithfully; the task designer must determine whether those columns exist at the moment the prediction is needed. Many projects that look excellent in an offline experiment encounter trouble at this earlier stage. Choosing a newer optimizer does not repair an input that contains information from the future.

Our example uses the daily Bike Sharing data from UCI: 731 days of observations from the Capital Bikeshare system in 2011 and 2012. Hadi Fanaee-T provided the dataset, which is released under CC BY 4.0. We will construct three simple forecasting rules and then examine their errors alongside the observations. This establishes a concrete starting point for later random forests, neural networks or other models. Additional complexity should contribute useful information or a better way of using it. The basic comparison must remain visible, so that improvements refer to the same target, the same forecast timing and the same evaluation period.

## What makes one row an observation?

Before converting the entire table into a numerical matrix, identify its observational unit. Here one row is a complete day of citywide rental activity. It is neither one journey nor one rider. Mixing daily and hourly tables changes what an observation means. Treating several records from one person as if they came from different independent people changes the interpretation of evaluation as well. The unit tells us what counts as a duplicate, what counts as a new example, and whether differences arise across people, locations or time. Software can readily report the first dimension of an array. Explaining what that dimension represents in the world takes a separate modeling decision.

A feature describes something supplied to the prediction rule, whereas the target is the quantity the rule should produce. Weekday, holiday status and the rental count seven days earlier can be available before the new day starts. The new day's total rentals become known only after observation has finished. Historical training tables contain both: the input records the circumstances and the target records what subsequently happened. At application time, the input arrives first and the target arrives later. Although training and application encounter the answer at different times, the input fields must retain the same meaning. Otherwise a model trained for one information setting is quietly being used in another.

A numerical column does not necessarily describe a continuous magnitude. The weekday codes 0 and 1 identify categories; their difference is not a physical measure of how much “more weekday” one day is than another. A record number identifies a row and is not automatically a useful measurement. Rental counts, in contrast, can be added, temperatures have a measurement scale, and dates have a temporal order. These distinctions affect encoding, plotting and distance calculations. Treating all columns as interchangeable numbers can introduce a modeling error before a classifier is ever selected. The table below records the meanings we will use throughout the chapter.

| Field | Meaning in this chapter | Units and use |
| --- | --- | --- |
| dteday | Date of the daily observation; also a key for sorting and duplicate checks | Calendar date |
| weekday | Weekday category, with 0 indicating Sunday | Category code, not a continuous distance |
| workingday | A day that is neither a weekend nor a holiday | 0 or 1 |
| temp | The normalized temperature supplied in the dataset | Unitless; used for exploration, not treated as a known future measurement |
| cnt | Total rentals completed during the day | Rentals/day; prediction target |
| casual, registered | Completed rentals for the two user categories | Rentals/day; their sum equals cnt |

This table is the beginning of a data dictionary. A practical dictionary also records when a field is generated, how missing values are represented, how the source system defines it and which transformations have been applied. “Temperature normalized to a numerical range” and “temperature measured in degrees Celsius” are different statements. A readable axis label should not silently turn a normalized quantity into a physical measurement. We retain the supplied unitless temperature in this chapter. If a later analysis requires physical units, the transformation should be taken from the documentation for the relevant data version and checked against its scale.

## Draw the moment when information becomes available

The simplest test of a candidate feature is to place it on a timeline. Weekday and holiday status come from the calendar. The count seven days earlier comes from a day that has already ended. Full-day observed weather and the day's completed rentals by registered users become complete after the day ends. A historical file stores these columns side by side for convenient organization; it does not imply that they were all available simultaneously. In the diagram, the vertical line marks the forecast issue time. Read the time position of a field before considering how strongly it might be associated with demand.

![Information availability for a forecast issued before the day starts. Green fields are available in advance; red fields become complete after the day ends. Position represents workflow timing, not a correlation score.](https://ml-biomat.com/static/tutorials/machine-learning/figures/981d57c0f96f1c67633b1c18.svg?v=981d57c0f96f)

Figure 1Information availability for a forecast issued before the day starts. Green fields are available in advance; red fields become complete after the day ends. Position represents workflow timing, not a correlation score.

The columns `casual` and `registered` deserve particular attention. Their sum is exactly `cnt`. A program given both can recover the answer by addition without learning any relationship involving weather or travel patterns. That calculation is useful for checking an end-of-day report. In a forecast issued at the beginning of the day, it uses the future outcome. Target leakage is often this concrete: the answer, or a close relative of the answer, enters the input too early. When checking a feature, asking whether it correlates with the answer is insufficient. Ask whether its value has actually been generated when the real decision must be made.

Information can also travel backward through an apparently harmless transformation. If we compute an average rental count over both years and then pretend to stand at the end of the first year, the future has already contributed to that average. Imputation, standardization, feature selection and threshold selection can create similar problems. The correct order is to define the training window, estimate the required quantities within that window, and apply the resulting rules to later observations. A mean is enough to demonstrate the principle. It does not depend on the complexity of a neural network or on a particular software implementation.

We must also distinguish one forecast for the next 183 days from a sequence of 183 one-day-ahead forecasts. This chapter uses the latter setting. As each new day begins, previous days' actual rental counts have become available. The eighth test day can therefore use the first test day's observed count as its same-weekday value from the previous week. That follows the intended information order. If the task instead required predicting an entire half-year from a single July forecast origin, those later observed values would be unavailable. We would need recursive predictions or models designed for explicit forecast horizons.

## Separate missing records, duplicates and real change

Data checks should reflect the meaning of the observations. After sorting, this dataset contains 731 distinct dates, no missing cells, and a total count equal to the sum of the two user-category counts on every day. These checks answer different questions: whether the records are complete, whether the daily key is duplicated, and whether related fields reconcile. Even after all three checks succeed, plots are needed to investigate which environments the data cover. Data quality is better understood as a set of specific relationships tied to a task than as a single switch that labels a file good or bad.

If a day's record is absent, replacing its rental count with zero changes the meaning of the observation. Zero says that the day was observed and no rentals occurred. Absence may instead indicate a sensor outage, a synchronization delay or a change in reporting conventions. Treating absence as zero can teach a model a demand collapse that never happened. Missing input values may be handled with an imputation rule estimated on training data, sometimes together with an indicator of missingness. A missing target usually calls for recovering the record or specifying which dates can enter training and evaluation. The same replacement rule need not be appropriate for every column.

Duplicates also depend on the observational unit. Exporting a daily record twice creates a duplicate daily example, while many hourly records on the same date can be perfectly valid. Removing identical full rows will miss two versions of the same date whose fields differ after an update. It may also delete separate observations that happen to share the same attributes. We therefore check the date as the daily table's unique key and then inspect count consistency. When versions conflict, a source-system or versioning rule should determine the resolution. The preferred record should not be selected because it happens to produce a better evaluation score.

The sampling frame tells us whose behavior the model can learn. These observations cover one system over two years, with its operating practices, user population and urban setting. Another city may have different weather, commuting patterns or prices. Even the same system may grow, changing the level of demand. The plots will show a substantial difference between the two years. Randomly shuffling all observations can make training and testing look distributionally similar, but that does not necessarily reproduce the job of using earlier data to predict later demand. The split should be chosen to represent the intended use rather than simply to make the table convenient.

## Give each figure a question

A plot becomes useful when it answers a question we can articulate. The time series asks whether demand changes with season and year. The temperature scatter asks how much demand varies among days with similar temperature. The weekday bars ask whether weekly patterns look similar across the two years. Placing these views together allows a reader to investigate what a proposed model might miss. A weekday-only rule may overlook growth in system activity. A temperature-only rule may overlook rainfall, holidays or changing user composition. These observations guide feature design more effectively than a long collection of unexplained correlations.

![Three views of 731 daily observations. The dashed line separates training and testing; scatter colors identify the year and temperature retains the dataset normalization; bars compare weekday means. Data: H. Fanaee-T, UCI Bike Sharing, CC BY 4.0. Calculated by the accompanying code.](https://ml-biomat.com/static/tutorials/machine-learning/figures/8ac46d85d9af62e8d0ec15d4.svg?v=8ac46d85d9af)

Figure 2Three views of 731 daily observations. The dashed line separates training and testing; scatter colors identify the year and temperature retains the dataset normalization; bars compare weekday means. Data: H. Fanaee-T, UCI Bike Sharing, CC BY 4.0. Calculated by the accompanying code.

Days with similar normalized temperature can have markedly different rental counts. Temperature therefore does not determine a unique outcome in these observations. Distinguishing the two years by color also reveals a shift in the location of the point cloud. This motivates further comparisons across periods and groups, but it does not directly quantify the effect of increasing temperature. Temperature, season, daylight and travel activity can move together. Describing a pattern, predicting an outcome and estimating the effect of intervening on a variable are different tasks. The causal-inference chapter develops the comparisons and assumptions needed for the intervention question.

Averages conceal variation that can matter for a decision. A weekday mean compresses many Mondays into one number, including sunny days, rainy days and special events. A stable-looking bar does not mean that each day is stable. For operational risk, inspect individual observations or an error distribution as well. We preserve the points and then use averages as summaries, so that readers can see both a pattern and its variability. Category axes should identify their categories explicitly. Arbitrary codes should not acquire the appearance of physical distances merely because a plotting function accepts them as numbers.

## What does improving a rule from experience mean?

In his 1959 paper on checkers, Arthur Samuel investigated how a program could improve its play through experience. The number of possible positions makes an exhaustive list of handwritten instructions impractical. A program can instead represent a position with features, evaluate possible choices and use later experience to improve its judgments. The same broad structure appears in a modern forecasting task: define the job, represent observable objects and improve a repeatable rule using recorded experience. The experience must be measured and organized. A program does not automatically infer which column expresses the outcome a researcher or operator actually cares about.

![An original mechanism illustration connecting an historical learning problem to forecasting: position features inform an action evaluation; calendar and past counts inform demand forecasts; later outcomes enable improvement. The board is a teaching illustration, not a reconstruction of an historical game.](https://ml-biomat.com/static/tutorials/machine-learning/figures/a6dc1d7feea939920426f728.svg?v=a6dc1d7feea9)

Figure 3An original mechanism illustration connecting an historical learning problem to forecasting: position features inform an action evaluation; calendar and past counts inform demand forecasts; later outcomes enable improvement. The board is a teaching illustration, not a reconstruction of an historical game.

When historical inputs come with corresponding outcomes, supervised learning becomes possible. Forecasting rental counts is regression because the output is a quantity. Changing the question to “Will tomorrow exceed a chosen demand threshold?” makes it classification because the output is a category. Both questions can be built from the same table, but the loss, evaluation metric and decision meaning change. If we have descriptions without outcome labels and want to discover similar groups or compact representations, we enter unsupervised learning. The resulting groups depend on the selected features, distance measure and assumptions. Their usefulness needs to be checked against the purpose of the analysis.

Reinforcement learning adds the relationship between an action and the environment's later state. Moving bicycles changes station availability, which can affect which rentals are completed later. An action can incur a cost now and produce a benefit tomorrow. The task then involves learning how to act to improve return across a sequence, rather than forecasting outcomes alone. Our three demand baselines do not intervene in the environment; they form a prediction experiment. Whether an application concerns transport, health or games does not determine the learning setting. The available data, action structure and feedback determine it.

Every setting needs a useful starting comparison. For regression, always predicting a historical average is one baseline. For classification, always predicting the most frequent training class is another. Such rules make explicit the regularity already available before a complex model is introduced. If a new model does not improve upon an appropriate baseline, we can investigate whether the inputs add information, whether fitting worked, and whether the evaluation matches the intended job. An algorithm's name is not evidence that it must outperform an established alternative. A well-defined baseline keeps that comparison concrete and reproducible.

## Three complete rules and a forecasting experiment

The first rule averages the rental counts in the training window and predicts that same value on every later day. Adding the counts and dividing by the number of days retains the overall level while discarding day-to-day variation. The second rule computes a separate mean for each of the seven weekdays and retains some weekly structure. The third uses the actual count seven days earlier, retaining both weekday position and a more recent level of activity. The rules are all simple, yet they preserve different information. This makes their comparison scientifically useful even before we introduce a fitted regression or classification algorithm.

$$
\widehat y_{\mathrm{mean}}=\frac{1}{n}\sum_{i=1}^{n}y_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b27050485e352807978721bc.svg) | Prediction from the training mean, in rentals/day; the hat denotes an estimate. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of training days, a unitless count; 548 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Training-day index from 1 to n, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Observed rentals for training day i, expressed as rentals/day. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the following quantity over the training days. |

For training counts of 300, 450 and 600, divide the total 1350 by three to obtain 450 rentals/day. The rule predicts 450 before observing the new day. This is a simple level baseline estimated on training data; evaluating it with MAE does not assert that the mean is the MAE-optimal constant.

The script assigns the first 548 days to a fixed training window and the remaining 183 days to sequential one-day-ahead evaluation. The first test date is July 2, 2012. This cutoff is a specified experimental choice; a different forecast season can produce different errors. We evaluate how many rentals the predictions miss by using mean absolute error. For each day, subtract the prediction from the observation, take the absolute value so that positive and negative errors do not cancel, and average across the test dates. The result has the same units as the original target, making the magnitude easy to interpret.

$$
\operatorname{MAE}=\frac{1}{m}\sum_{j=1}^{m}|y_j-\widehat y_j|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fbefa31f23bf03bf2a6369fb.svg) | Mean absolute error, in rentals/day. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Number of test days, unitless; 183 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Index over test days, defined separately from the training index. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a43238afaec89629eda11aa.svg) | Observed rentals on test day j, in rentals/day. |
| ![Formula](https://ml-biomat.com/static/agent-math/50766b3825474216cf588eaf.svg) | Prediction issued before test day j, in rentals/day. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | Absolute value, retaining the magnitude of a difference. |

With observations of 500 and 700 and predictions of 600 and 650, the signed differences are −100 and 50. Their absolute values average to 75 rentals/day. Averaging signed differences would give −25 and cancel part of the discrepancies.

The complete script below reads the bundled `data/day.csv`, checks unique dates and the count identity, computes all three baselines, and saves a prediction table, numerical summary and the three result figures. The `--language zh` and `--language en` options select the figure labels. Reading, estimation, evaluation and plotting use the same script, allowing each displayed curve to be traced to the same inputs and calculations. No additional download is required after extracting the code-and-data bundle. The file also preserves the data citation so that the observations remain identifiable when the example is reused.

### Complete example: daily data checks, three baselines and result figures

Requires NumPy, pandas and Matplotlib. The bundle includes data/day.csv and its original documentation. Run python main.py --output results --language en. summary.json stores metrics, predictions.csv retains daily forecasts, and SVG files contain the figures.

```
"""Daily bicycle demand: an auditable data table and three forecasting baselines.

Run: python main.py --output results --language en
Data: H. Fanaee-T, Bike Sharing, UCI, doi:10.24432/C5W894, CC BY 4.0.
The bundled day.csv has 731 observations of daily rental counts, not fleet size.
"""
from pathlib import Path
import argparse
import json
import hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results')
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'DejaVu Sans'],
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'figure.facecolor': 'white', 'axes.titlepad': 12})
    source = Path(__file__).resolve().parent / 'data' / 'day.csv'
    df = pd.read_csv(source, parse_dates=['dteday']).sort_values('dteday')
    assert len(df) == 731 and df['dteday'].is_unique
    assert (df['cnt'] == df['casual'] + df['registered']).all()
    assert not df.isna().any().any()
    # The first 548 days fit two fixed baselines. Every later day is a new forecast.
    cut = 548
    train, test = df.iloc[:cut].copy(), df.iloc[cut:].copy()
    global_mean = float(train['cnt'].mean())
    weekday_means = train.groupby('weekday')['cnt'].mean()
    predictions = pd.DataFrame({'date': test['dteday'], 'observed': test['cnt'],
                                'mean': global_mean,
                                'weekday': test['weekday'].map(weekday_means),
                                'last_week': df['cnt'].shift(7).iloc[cut:]})
    names = {'mean': '训练均值' if zh else 'Training mean',
             'weekday': '星期均值' if zh else 'Weekday mean',
             'last_week': '上周同日' if zh else 'Same day last week'}
    colors = {'mean': '#6f8191', 'weekday': '#ca8446', 'last_week': '#167b82'}
    mae = {k: float(np.mean(np.abs(predictions[k] - predictions.observed))) for k in names}
    medae = {k: float(np.median(np.abs(predictions[k] - predictions.observed))) for k in names}
    summary = {'n_days': len(df), 'train_days': len(train), 'test_days': len(test),
               'split_date': str(test['dteday'].iloc[0].date()), 'missing_cells': 0,
               'unique_dates': int(df.dteday.nunique()), 'identity_max_error': 0,
               'global_mean': global_mean, 'mae_rentals_per_day': mae,
               'median_absolute_error': medae,
               'data_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    predictions.to_csv(out / 'predictions.csv', index=False)
    df[['dteday', 'weekday', 'workingday', 'temp', 'casual', 'registered', 'cnt']].to_csv(out / 'observations.csv', index=False)

    # A linked overview: the same daily records in time and in feature space.
    fig = plt.figure(figsize=(11.5, 7.0), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1])
    ax = fig.add_subplot(gs[0, :])
    ax.plot(df.dteday, df.cnt, color='#183845', lw=1.05)
    ax.axvline(test.dteday.iloc[0], color='#a95238', ls='--', lw=1.5,
               label='预测起点' if zh else 'First forecast date')
    ax.set(ylabel='租借次数 / 日' if zh else 'Rentals / day',
           title='每个点都对应一整天的城市租借记录' if zh else 'Each observation represents one day of citywide rentals')
    ax.legend(frameon=False)
    ax = fig.add_subplot(gs[1, 0])
    for year, color in [(0, '#788b98'), (1, '#167b82')]:
        sub = df[df.yr == year]
        ax.scatter(sub.temp, sub.cnt, s=13, alpha=.6, color=color, label=str(2011 + year))
    ax.set(xlabel='归一化温度（无量纲）' if zh else 'Normalized temperature (unitless)',
           ylabel='租借次数 / 日' if zh else 'Rentals / day')
    ax.legend(frameon=False, ncols=2)
    ax = fig.add_subplot(gs[1, 1])
    for year, offset, color in [(0, -.18, '#788b98'), (1, .18, '#167b82')]:
        means = df[df.yr == year].groupby('weekday')['cnt'].mean()
        ax.bar(np.arange(7) + offset, means.reindex(range(7)), width=.34, color=color)
    ax.set(xticks=range(7), xlabel='星期编码（0=星期日）' if zh else 'Weekday code (0 = Sunday)',
           ylabel='平均租借次数 / 日' if zh else 'Mean rentals / day')
    fig.savefig(out / f'observations-{args.language}.svg')
    plt.close(fig)

    fig, axs = plt.subplots(2, 1, figsize=(11.5, 7.4), height_ratios=[1.8, 1], layout='constrained')
    ax = axs[0]
    ax.plot(test.dteday, test.cnt, lw=1.8, color='#183845', label='观测' if zh else 'Observed')
    for k in names:
        ax.plot(test.dteday, predictions[k], lw=1.1, alpha=.85, label=names[k], color=colors[k])
    ax.set(ylabel='租借次数 / 日' if zh else 'Rentals / day',
           title='固定训练窗口；随后183天逐日向前预测' if zh else 'Fixed training window; 183 subsequent one-day-ahead forecasts')
    ax.legend(frameon=False, ncols=2)
    ax = axs[1]
    for i, k in enumerate(names):
        ax.barh(i, mae[k], color=colors[k], height=.48)
        ax.text(mae[k] + 35, i, f'{mae[k]:.1f}', va='center')
    ax.set(yticks=range(3), yticklabels=list(names.values()),
           xlabel='平均绝对误差（租借次数 / 日）' if zh else 'Mean absolute error (rentals / day)',
           xlim=(0, max(mae.values()) * 1.2))
    fig.savefig(out / f'baselines-{args.language}.svg')
    plt.close(fig)

    # Availability is a causal ordering in the workflow, not a correlation score.
    labels = ['星期/节假日', '前7日次数', '全天实测天气', '当日注册租借', '当日临时租借', '当日总次数'] if zh else ['Weekday / holiday', 'Count seven days ago', 'Full-day observed weather', 'Today: registered rentals', 'Today: casual rentals', 'Today: total rentals']
    fig, ax = plt.subplots(figsize=(11.5, 4.5), layout='constrained')
    for i, (label, available) in enumerate(zip(labels, [True, True, False, False, False, False])):
        y = 5-i
        ax.text(-.08, y, label, ha='right', va='center', fontsize=11)
        ax.plot([0, 1], [y, y], color='#d4dfe3', lw=8, solid_capstyle='round')
        x = 0 if available else 1
        ax.scatter([x], [y], s=135, color='#167b82' if available else '#b65b44', zorder=3)
    ax.axvline(.12, color='#183845', lw=1, ls='--')
    ax.text(.12, 5.65, '作出预测' if zh else 'Forecast issued', ha='center', fontsize=11)
    ax.set(xticks=[0,1], xticklabels=['一天开始前','当天结束后'] if zh else ['Before the day starts','After the day ends'],
           xlim=(-.65,1.2), ylim=(-.7,6.0), yticks=[])
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.savefig(out / f'availability-{args.language}.svg')
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
```

![Observed counts, forecasts and MAE over 183 sequential one-day-ahead forecasts. The first two rules are estimated on the first 548 days; the weekly lag uses observations already available seven days earlier. Error units are rentals/day. Data: H. Fanaee-T, UCI Bike Sharing, CC BY 4.0.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c72980235bf7cd9ff1b4a1ff.svg?v=c72980235bf7)

Figure 4Observed counts, forecasts and MAE over 183 sequential one-day-ahead forecasts. The first two rules are estimated on the first 548 days; the weekly lag uses observations already available seven days earlier. Error units are rentals/day. Data: H. Fanaee-T, UCI Bike Sharing, CC BY 4.0.

Across these 183 test days, mean absolute error is 2455.4 rentals/day for the training mean, 2453.2 for the weekday mean and 1128.5 for the same-day-last-week rule. The first two results are close: weekday information alone does not resolve the level difference between this test period and the earlier training window. Recent observations help the third rule follow changing activity. The time-series panel also makes clear that last week's count does not anticipate a sudden change this week. Two concrete extensions follow: incorporate weather forecasts available at issue time, and combine adaptation to recent activity with resistance to single-day noise.

## Connect prediction errors to the cost of action

Two errors of 100 rentals can have different consequences. Underestimating demand may leave potential rentals unserved, whereas overestimating can leave service capacity unused. To make this distinction calculable, consider a teaching model in which capacity is the number of rentals that can be served during a day. Assign a cost of three units for each unit of unmet demand and one unit for each unused capacity unit. This is total daily service capacity, not a count of bicycles. Since bicycles can be reused, translating capacity into a fleet requires a further operational model. Keeping that distinction explicit preserves the meaning of the calculation.

$$
L(q,d)=c_{\mathrm{s}}\max(d-q,0)+c_{\mathrm{i}}\max(q-d,0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Total daily loss, in illustrative cost units. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Available daily rental-service capacity, in rental events. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Demand for that day, in rental events. |
| ![Formula](https://ml-biomat.com/static/agent-math/64010aae2cb5ed6f6d23139c.svg) | Cost per unmet rental, initially 3 cost units/rental. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b9a50f370aa466c577ad30d.svg) | Cost per unused capacity unit, fixed at 1 cost unit/rental. |
| ![Formula](https://ml-biomat.com/static/agent-math/5d7480bbc1584257fff25e60.svg) | The larger of a and zero, counting only positive shortage or unused capacity. |

Capacity 500 with demand 620 creates a shortage of 120 and a loss of 3×120=360. Capacity 500 with demand 350 leaves 150 unused units and costs 150. At most one term is positive for any day, so shortage and unused capacity are never charged simultaneously.

The loss is like a valley with different slopes on its two sides. When capacity is below demand, preparing one unit less increases cost rapidly. When capacity is above demand, preparing one unit more still costs something, but the increase is slower. A forecast chosen for mean absolute error and a capacity decision chosen for this asymmetric loss need not coincide. Separating prediction from the subsequent cost-based decision is useful in many applications. It helps explain why an improvement in a statistical score does not automatically translate into an equally sized improvement in operations, and why stakeholders must specify the consequences of different errors.

The interactive exercise uses eight explicitly listed teaching demand values, small enough to check by hand. Change capacity and the shortage cost to observe how the same demands generate a total cost in both a plot and an account. Selecting one day highlights its demand, its shortage or unused capacity, and its loss. Calculate a case on paper before comparing it with the page. This small, inspectable example builds an intuition for loss functions: the mathematical expression is a precise account of which discrepancies matter, in which direction and by how much.

## A capacity-and-demand account

The eight teaching demands are 300, 420, 500, 620, 350, 560, 710 and 480 rentals. Capacity ranges from 200 to 800; unused capacity costs one unit per rental, and you choose the shortage cost. The curve sums costs over these same eight days.

[Figure: Daily demand and capacity](https://ml-biomat.com/tutorials/machine-learning/m01/en/#M01-demand)

[Figure: Total cost against capacity](https://ml-biomat.com/tutorials/machine-learning/m01/en/#M01-loss)

## Carry a clear task definition into modeling

A reproducible project can start with a few concrete objects: original data and documentation, a data dictionary, an executable script, per-observation predictions, and figures that explain the results. Saving only a final score removes the opportunity to inspect where errors occur. Saving only pictures removes the ability to recalculate them under different parameters. Saving only a fitted model makes it difficult for a later reader to reconstruct the intended input. Connecting these objects gives subsequent improvements a stable basis. The goal is a traceable relationship between a question, observations, computation and interpretation, rather than a folder full of differently named model files.

The same reasoning transfers to other domains. For household energy use, distinguish an hourly consumption forecast from a monthly bill. For image recognition, decide whether the observation is one photograph or a set of photographs of the same object. For customer attrition, determine which activities happened before the prediction was issued. Write down who or what is being predicted, at which time, from which known information, and for which decision. Sampling, features and evaluation can then be designed around that statement. Mathematics, programming and application discussions become easier when they all refer to the same object and time boundary.

As an exercise, change the target to the total rentals over the next seven days. The target now needs a weekly aggregation, the forecast must be issued at a specified time, and each input must be checked against that time. The same-day-last-week rule can be summed across seven dates, but the evaluation unit, target units and number of examples change too. Explaining these changes demonstrates the main skill developed here: organizing a real question into a task whose data can be computed with, whose alternatives can be compared and whose conclusions can be questioned in concrete terms.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Bike Sharing — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)

   Original observations, variable definitions and citation supplied by Hadi Fanaee-T.

   Dataset: CC BY 4.0; DOI 10.24432/C5W894.
2. [INRIA: First look at our dataset](https://inria.github.io/scikit-learn-mooc/python_scripts/01_tabular_data_exploration.html)

   Further practice with feature types, joint distributions and hand-written decision rules.

   CC BY 4.0
3. [Samuel (1959), Some Studies in Machine Learning Using the Game of Checkers](https://www.cs.virginia.edu/~evans/greatworks/samuel1959.pdf)

   The original study of representations, evaluation rules and learning from experience in checkers.
4. [Dive into Deep Learning: Introduction](https://d2l.ai/chapter_introduction/index.html)

   Compare the problem structures of supervised, unsupervised and reinforcement learning.

   CC BY-SA 4.0
