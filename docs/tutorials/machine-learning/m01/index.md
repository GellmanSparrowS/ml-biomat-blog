# 数据、特征与机器学习任务

Source: https://ml-biomat.com/tutorials/machine-learning/m01/
Language: zh-CN

从共享单车的一天出发，确定样本、信息出现的时间与预测目标，再用三条完整规则建立可以比较的起点。

## 先说清明天要做什么

清晨的共享单车站点还很安静，调度员却已经要决定今天怎样安排运输和维护。如果等到所有租借都结束，再把当天的总次数算出来，得到的是一份日报；如果在一天开始前估计当天的需求，得到的才是预测；如果进一步决定车辆如何调度，就进入了决策。三件事使用的数据看起来相近，回答的问题却不同。本章从这个区别出发，把一份真实的自行车租借记录变成可以检查的学习任务。读完以后，你应当能说明一行数据代表什么、答案是什么时候知道的，以及一个简单预测究竟比什么更好。

先把问题写成一句有时间和对象的话：“在每天开始前，根据已经知道的信息，预测这一城市系统当天的租借总次数。”这里有三个容易被忽略的词。“每天”规定一条样本的时间跨度；“已经知道”规定哪些字段可以进入模型；“总次数”规定输出的含义和单位。一次租借算一次，同一辆车可以一天被租借多次，因此租借次数与所需车辆数并不相等。若要直接优化车辆配置，还要增加站点位置、归还流向、车辆周转和运力等信息。把目标先定义清楚，后面的算法才有确定的工作对象。

用菜谱来理解数据表会很自然：每一行是一顿已经做过的饭，原料和烹饪条件是输入，食客评分是结果。不过，在预测新菜的评分时，不能把这道新菜已经收到的评分写进“原料”一栏。机器学习也是一样。程序会认真使用你交给它的每一列，至于这列在现实中能否提前取得，需要由任务设计者判断。许多离线结果漂亮、上线后效果差的项目，问题就在这一层，而不是某个优化器选得不够新。

本章使用 UCI 的 Bike Sharing 日级数据，记录了 Capital Bikeshare 系统在2011年至2012年的731天租借情况。数据由 Hadi Fanaee-T 提供，采用 CC BY 4.0 许可。我们会先做三条很容易解释的预测规则，再查看误差和数据分布。这样安排有一个实际好处：以后换成随机森林、神经网络或其他模型，比较的起点已经摆在桌面上。更复杂的方法应当增加有用的信息，而不仅是增加代码行数。

## 一行记录怎样成为一个样本

打开表格时，先不要急着把所有列转换为数字矩阵。请先指出一个明确的观察单位：本例是一整天的城市租借汇总，不是一次行程，也不是一个骑车的人。把日级表和小时级表混在一起，会让同一个词“样本”指向不同对象；把同一位用户的多次记录当成完全独立的人，也会改变评估含义。样本单位决定了什么叫重复、什么叫新样本，以及模型面对的变化来自人、地点还是时间。数组的第一维很容易得到，第一维的现实含义却需要先想清楚。

特征是预测时提供给模型的描述，目标是希望模型输出的量。本例的星期、节假日标记以及七天前的租借次数都可以在当天开始前获得。当日的总租借次数则要等观察结束后才能知道。训练时，这两部分会同时出现在历史表里：输入告诉模型当时的条件，目标告诉模型后来发生了什么；应用时，只有输入先到，目标在未来才出现。训练与应用的信息顺序虽然不同，输入字段的含义应当保持一致。

数值列也并非都表示连续大小。星期编码里的0和1是类别标签，不能解释成星期一比星期日“多一个单位的工作日程度”；记录序号只是识别行的位置，不是天然有预测意义的物理量。与此相对，租借次数可以相加，温度有测量尺度，日期有明确先后。理解这些区别，会影响怎样编码、画图以及计算距离。将所有列直接当成同一种数字，往往比选择哪一种分类器更早引入问题。

| 字段 | 本章中的意义 | 单位与使用方式 |
| --- | --- | --- |
| dteday | 一天的日期，也是排序与查重依据 | 日历日期，用于时间顺序 |
| weekday | 星期类别，0表示星期日 | 类别编码，不作连续距离解释 |
| workingday | 是否为非周末且非节假日的工作日 | 0或1 |
| temp | 数据集提供的归一化温度 | 无量纲；用于观察，不作为提前已知的实测天气 |
| cnt | 一天内全部租借次数 | 次/日，预测目标 |
| casual、registered | 两类用户当天完成的租借次数 | 次/日，两者相加等于cnt |

这个小表就是数据字典的雏形。一个实用的数据字典还应记录字段在什么时候生成、缺失值怎样表示、来源系统如何定义，以及转换前后发生过什么变化。例如“温度归一化到某个区间”与“温度单位是摄氏度”不是同一件事，不能因为纵轴想写得亲切，就擅自把归一化值标成摄氏度。本章保留原数据的无量纲温度；以后需要物理单位时，再根据对应版本的数据说明完成变换。

## 把信息出现的时间画出来

判断一个特征能否使用，最直接的办法是沿时间线摆放它。星期和节假日来自日历，提前就能知道；七天前的租借次数来自已结束的一天，也已经知道；全天实测天气和当天注册用户的租借总数，则在一天结束以后才完整。历史文件把它们并排存放，只是为了便于整理，不表示这些信息在预测时同时可用。下图用“作出预测”这条竖线把可用信息与未来结果分开，读图时先看时间位置，再看字段名称。

![按本章日初预测任务绘制的信息可用时间示意。绿色为预测前可知字段，红色为当日结束后才完整的字段。位置表达工作流程中的先后，不是对各列相关性的评分。](https://ml-biomat.com/static/tutorials/machine-learning/figures/2d7f379efe6ee31de8e5ea50.svg?v=2d7f379efe6e)

图 1按本章日初预测任务绘制的信息可用时间示意。绿色为预测前可知字段，红色为当日结束后才完整的字段。位置表达工作流程中的先后，不是对各列相关性的评分。

尤其值得检查的是 `casual` 与 `registered`。它们相加恰好得到 `cnt`，因此把两列作为特征，程序无需学习天气或出行规律，就能通过加法还原答案。这样的计算在核对日终报表时非常有用，在日初预测时却用到了未来。目标泄漏不是某种神秘的软件故障，而是答案或者答案的近亲，沿数据处理流程提前进入了输入。寻找泄漏时，问“这列与答案相关吗”还不够，还要问“在真正作决定的那一刻，这列已经生成了吗”。

同样的时间问题也会出现在更隐蔽的转换里。假如先用两年的所有数据计算平均租借次数，再假装站在第一年末预测第二年，未来的信息已经进入那个平均值。填补缺失值、标准化、筛选特征和选择阈值都有类似风险。正确的顺序是先确定训练窗口，再在这个窗口内估计所需的统计量，最后把确定下来的规则应用到后面的日期。这个原则可以从一个平均数开始理解，不必等到复杂模型出现才讨论。

我们还要区分“一次预测未来183天”与“连续183天，每天预测下一天”。本章采用第二种工作方式：每到新的一天，就可以使用此前已经观察到的真实租借次数，所以测试窗口中的第八天可以使用测试窗口第一天的记录作为上周同日值。这样做符合逐日预测的信息顺序。如果任务改成在七月初一次性预测半年，就不能继续取用半年中后来才出现的实际记录；需要递推预测或为不同预测跨度设计模型。

## 先分清没有记录、重复记录和真实变化

数据检查应当围绕对象的含义展开。本例对日期排序后有731个不同日期，没有缺失单元格，并且每一天都满足总次数等于两类用户次数之和。前两个检查回答记录是否完整、主键是否重复，第三个检查回答字段之间是否一致。它们检查的是不同问题，即使都通过，也还需要读图观察数据覆盖了哪些环境。数据质量不是一个可以统一打满分的开关，而是一组与任务相对应的具体关系。

如果某天缺少记录，不应立即把租借次数填成0。0表示确实观察到没有租借；缺失可能表示传感器停机、数据未同步或者统计口径发生变化。把缺失当0，会让模型学到一个实际上没有发生的需求骤降。对输入特征的缺失，可以在训练数据中估计填补规则，并额外保留“是否缺失”的标记；对预测目标缺失，则通常需要先找回记录，或者明确哪些日期可以参与训练和评估。不同字段缺失，处理方式也应当不同。

重复记录也需要结合样本单位判断。一天被导出两次，是同一日级样本的重复；同一天出现很多小时级记录，则可能完全合理。直接按整行去重会漏掉“相同日期但部分字段有更新”的情况，也可能删掉本来应当存在的相同行程属性。因此我们把日期作为日级表的唯一键，再检查计数是否一致。若两个版本记录冲突，解决方法应来自来源系统或版本规则，而不是随手保留让模型得分更高的那个版本。

采样范围决定了模型究竟学到了谁的规律。这里只包含一个系统的两个年份，覆盖了该系统当时的运营方式、用户构成和城市环境。如果换到另一座城市，气候、通勤和收费制度都可能变化；即使仍在同一系统，运营规模增长也可能改变需求水平。后面会看到，第二年的总体租借量与第一年明显不同。这样一来，简单把所有样本随机打乱，虽然容易让训练和测试拥有相似分布，却不一定模拟了“用过去预测未来”的真实工作。

## 让每一幅图回答一个具体问题

图像最有用的时候，是我们带着一个问题去看它。时间曲线回答“需求是否随季节与年份改变”；温度散点图回答“相近温度下的需求是否仍然分散”；按星期分组的柱图回答“星期结构在两个年份之间是否保持相似”。把三个视角放在同一张图版中，读者就能追问：一个模型如果只知道星期，是否遗漏了系统规模增长？如果只知道温度，又是否遗漏了降雨、节假日和用户组成？这些问题会指引特征设计，远比堆积几十张没有解释的相关性热图有效。

![731个真实日级观测的三个视角。上图按时间显示租借次数，虚线为训练/测试分界；左下按年份着色，温度保留数据集的归一化尺度；右下比较星期均值。数据：H. Fanaee-T，UCI Bike Sharing，CC BY 4.0；本图由随章代码计算。](https://ml-biomat.com/static/tutorials/machine-learning/figures/9f0a3f7350a42d137186867f.svg?v=9f0a3f7350a4)

图 2731个真实日级观测的三个视角。上图按时间显示租借次数，虚线为训练/测试分界；左下按年份着色，温度保留数据集的归一化尺度；右下比较星期均值。数据：H. Fanaee-T，UCI Bike Sharing，CC BY 4.0；本图由随章代码计算。

散点图里同样温度对应的租借次数有明显差别，这说明温度并没有唯一决定需求。颜色把年份区分开以后，还能看到两个时间段的整体位置变化。这样的观察提示我们继续比较不同群体和时期，但它本身不告诉我们“升温会让租借增加多少”。温度、季节、白昼长度和出行活动可能同时变化。描述模式、预测结果与改变一个因素造成的因果效应，是三种不同的任务；后面的因果章节会专门说明怎样为第三种任务设计对照。

画图时还要注意平均值隐藏了什么。星期均值会把许多个星期一压成一个数，其中可能同时包含晴天、雨天和特殊活动日。一个柱子很平稳，不代表每天都平稳。需要评估运作风险时，应当同时查看个体观测或误差分布。我们先把原始点保留下来，再用均值概括，这样读者既能看到规律，也能看到围绕规律的变化范围。对于类别特征则应明确类别含义，不把任意编码画成有连续物理距离的坐标。

## 从经验改进规则，究竟在学什么

1959年，Arthur Samuel 在关于西洋跳棋的论文中研究程序如何通过经验改善下棋表现。棋局数量太多，逐个手写“在这个局面走这一步”并不现实；可以计算局面的特征，用评价规则选择行动，再利用后续经验调整判断。把这个问题放回今天的预测任务，就能看到一个共同结构：先规定要完成的任务，再把可观察的对象变成表示，最后用经验改进一条可以重复执行的规则。这里的“经验”必须经过测量和记录，程序并不会自动知道哪一列才是我们关心的结果。

![从历史问题到当前任务的原创机制示意：棋局特征帮助评价行动，日历与历史计数帮助预测需求；后续结果使规则有机会被检验和改进。左图是教学棋盘，不复原某一局历史对弈。](https://ml-biomat.com/static/tutorials/machine-learning/figures/56eedef3b8635becc226505d.svg?v=56eedef3b863)

图 3从历史问题到当前任务的原创机制示意：棋局特征帮助评价行动，日历与历史计数帮助预测需求；后续结果使规则有机会被检验和改进。左图是教学棋盘，不复原某一局历史对弈。

有历史输入和对应结果时，我们可以做监督学习。自行车需求预测的输出是一个数量，属于回归；如果把问题改成“明天是否超过某个需求阈值”，输出变成类别，属于分类。两种任务可以来自同一张表，但损失函数、指标和行动含义会改变。如果手头只有对象描述，希望按相似性寻找群组或压缩表示，就进入无监督学习。群组不是自动产生的真理，它依赖所选特征、距离和建模假设，需要结合任务检查是否有用。

强化学习还增加了行动与后续环境的联系。调度车辆会改变站点可用性，进而影响未来能够完成的租借；一个行动今天有成本，明天可能有收益。这时不仅要预测，还要学习怎样行动，使一段时间内的回报更好。本章的三条需求基线没有主动改变环境，因此是预测实验，并不是强化学习实验。任务名称应由数据与反馈的结构决定，而不能只看应用发生在交通、医疗还是游戏中。

无论哪种学习方式，都需要一个可比较的起点。对于回归，“始终预测历史平均值”就是一种基线；对于分类，“始终预测训练集中最常见的类别”也是一种基线。基线把我们在使用复杂方法之前已经知道的规律显式写出来。如果一个新模型没有超过合适的基线，我们就可以检查输入是否真的带来新信息、优化是否有效、评估是否符合用途，而不必仅凭算法名字判断它应该更强。

## 三条完整规则与一次真正的预测实验

第一条规则把训练窗口中的每日租借次数求平均，以后每天都预测同一个数。平均的做法是先把总量加起来，再按天数平分：它保留整体水平，舍弃日期之间的变化。第二条规则分别为七种星期计算平均值，因此保留一部分每周结构。第三条规则直接使用七天前的实际次数，既保留星期位置，也能部分追随近期需求水平。三条规则的复杂度都很低，但它们保留的信息并不相同，这正是比较它们的理由。

$$
\widehat y_{\mathrm{mean}}=\frac{1}{n}\sum_{i=1}^{n}y_i
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b27050485e352807978721bc.svg) | 训练均值给出的预测，单位为租借次数/日；帽子表示估计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | 训练窗口内的天数，计数，无量纲；本例为548。 |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | 训练日的索引，从1到n，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | 第i个训练日的实际租借次数，以日级观察表示，单位为租借次数/日。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 把后面的量按所有训练日相加。 |

若三个训练日分别观察到300、450、600次租借，总和1350除以3得到450次/日。新的一天尚未观察到时，这条规则仍预测450。平均值由训练日计算；它是一个简单水平基线，计算平均绝对误差并不要求它是该指标下的最优常数。

程序按照日期把前548天作为固定训练窗口，把后183天作为逐日测试窗口，分界点是2012年7月2日。这个时间点只是本例明确选定的评估设计；换一个预测季节，误差可能变化。我们用平均绝对误差衡量预测与观测相差多少次租借。先逐日求差，取绝对值以免正负抵消，再对所有测试日取平均。这个指标与原始目标单位相同，便于直接理解预测误差的大小。

$$
\operatorname{MAE}=\frac{1}{m}\sum_{j=1}^{m}|y_j-\widehat y_j|
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fbefa31f23bf03bf2a6369fb.svg) | 平均绝对误差，单位为租借次数/日。 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 测试日数量，计数，无量纲；本例为183。 |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | 测试日索引，与训练索引分别定义。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6a43238afaec89629eda11aa.svg) | 第j个测试日的实际租借次数，租借次数/日。 |
| ![Formula](https://ml-biomat.com/static/agent-math/50766b3825474216cf588eaf.svg) | 在第j个测试日开始前给出的预测，租借次数/日。 |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | 绝对值，把差的正负去掉，保留大小。 |

若两天的观测为500和700，预测为600和650，差分别为−100和50；绝对值为100和50，平均后得到75次/日。直接平均有符号误差会得到−25，掩盖了两天分别发生的偏差。

下面的完整脚本读取随代码提供的 `data/day.csv`，检查日期唯一性和计数关系，计算三个基线，并保存预测表、数值摘要和本章三幅结果图。运行时用 `--language zh` 或 `--language en`切换图中文字。数据读取、训练统计量、测试预测和绘图集中在同一份脚本中，因此每一条曲线都能追溯到相同的输入与计算。没有额外下载步骤，解压代码和数据后就能重现。

### 完整例子：日级数据检查、三条基线与结果图

依赖NumPy、pandas、Matplotlib。代码包含data/day.csv与原数据说明；运行python main.py --output results --language zh。summary.json保存数值，predictions.csv保留逐日预测，SVG保存图像。

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

![后183天逐日向前预测的观测、预测和平均绝对误差。前两条规则只在前548天估计；上周同日使用预测前七天已知的实际记录。误差单位为租借次数/日；数据：H. Fanaee-T，UCI Bike Sharing，CC BY 4.0。](https://ml-biomat.com/static/tutorials/machine-learning/figures/97f2d61ff32f4f0b38c5495a.svg?v=97f2d61ff32f)

图 4后183天逐日向前预测的观测、预测和平均绝对误差。前两条规则只在前548天估计；上周同日使用预测前七天已知的实际记录。误差单位为租借次数/日；数据：H. Fanaee-T，UCI Bike Sharing，CC BY 4.0。

在这次183天的测试中，训练均值的平均绝对误差为2455.4次/日，星期均值为2453.2次/日，上周同日为1128.5次/日。前两个数很接近，说明仅仅知道星期，并没有解决这段测试期与较早训练期之间的水平差异；使用近期观测则帮助规则追随变化。时间曲线同时说明，上周同日并不会预知当周突然发生的需求变化。我们因此得到两个具体的后续问题：怎样加入预测时可获得的天气预报，以及怎样在保留近期变化的同时减少单日噪声。

## 把预测误差接到行动成本

同样相差100次，低估需求和高估需求可能带来不同后果。低估会让一部分潜在租借无法得到服务，高估则可能造成多余的服务能力闲置。为了把这个想法算清楚，下面建立一个教学用的容量决策：把每天可完成的租借次数当成服务能力，规定每缺少一次能力的代价是3个成本单位，每闲置一次能力的代价是1个成本单位。这里的服务能力是一天的总处理次数，尚未转换为车辆数量；车辆可以重复使用，转换需要额外的运营模型。

$$
L(q,d)=c_{\mathrm{s}}\max(d-q,0)+c_{\mathrm{i}}\max(q-d,0)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 一天的总损失，单位为教学成本单位。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | 一天可提供的租借服务次数，即容量；单位为次。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | 当天实际需求，单位为次。 |
| ![Formula](https://ml-biomat.com/static/agent-math/64010aae2cb5ed6f6d23139c.svg) | 每次短缺的成本，本例默认3成本单位/次。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5b9a50f370aa466c577ad30d.svg) | 每次闲置容量的成本，本例为1成本单位/次。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5d7480bbc1584257fff25e60.svg) | 取a与0中较大的值；只计入正的短缺或闲置数量。 |

容量500次、需求620次时，短缺120次，损失为3×120=360；容量仍为500次、需求350次时，闲置150次，损失为1×150=150。每一天最多只有一项为正，所以短缺与闲置不会同时收费。

这个损失像一个左右坡度不同的山谷。容量小于需求时，往左少准备一步会增加更多成本；容量大于需求时，往右多准备一步仍有成本，但增长较缓。只追求平均绝对误差的预测，与按这个成本选择容量，可能给出不同答案。先预测，再按成本作决定，是理解许多应用的有用分工；把两步混在一起，会让人误以为某个统计指标提高一点，就自动等于运营结果改善了同样程度。

交互使用八个明确列出的教学需求值，故意把数据规模缩小到可以手算。改变容量和缺供成本，观察同一批需求在曲线与账本中怎样产生总成本。点击某一天，会同时突出它的需求、当日短缺或闲置以及当日损失。你可以先在纸上算一遍，再看页面给出的数值；这种可核对的小例子，为后面理解不同损失函数建立了直觉。

## 需求与容量的成本账本

八个教学需求值为300、420、500、620、350、560、710、480次。容量从200到800次，闲置成本固定为1；缺供成本由你设定。成本曲线对同一批八天求和，因此能直接检查当前容量离低成本区域还有多远。

[Figure: 每日需求与容量](https://ml-biomat.com/tutorials/machine-learning/m01/#M01-demand)

[Figure: 容量与总成本](https://ml-biomat.com/tutorials/machine-learning/m01/#M01-loss)

## 带着一份清楚的任务说明进入模型

一个可复现的小项目可以由几样具体东西组成：原始数据及说明、数据字典、能运行的脚本、逐样本预测表，以及解释结果的图。只保存一个最终得分，会丢掉检查误差发生在哪里的机会；只保存图片，会丢掉重算和改参数的机会；只保存模型文件，又会让后来的使用者难以知道输入究竟是什么。把这些材料联系起来，比在文件夹里堆很多不同名字的模型更有助于持续改进。

现在可以把同样的思路带到新的领域。预测房屋能耗时，明确输出是一小时耗电量还是整月账单；识别图像时，明确样本是一张图片还是同一个对象的一组照片；预测用户流失时，明确哪些行为在作出预测之前已经发生。先写出“对谁、在什么时候、用哪些已知信息、预测什么、用于什么决定”，再设计采样、特征和评估。这样一份任务说明，能让数学、代码和业务讨论使用相同的对象。

试着做一个小练习：假如目标改成“预测下一周七天的总租借次数”，需要把目标重新聚合为周总量，规定在星期几发出预测，并检查每个输入在该时刻是否可得。上周同日的规则可以逐日相加，但评估误差的单位和样本数也要跟着改变。能解释这些变化，就说明你已经掌握了这一章最关键的能力：从现实问题出发，组织出一个可以计算、可以比较、也可以追问的数据任务。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Bike Sharing — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)

   Hadi Fanaee-T提供的原始数据、字段定义和引用信息。

   Dataset: CC BY 4.0; DOI 10.24432/C5W894.
2. [INRIA: First look at our dataset](https://inria.github.io/scikit-learn-mooc/python_scripts/01_tabular_data_exploration.html)

   继续练习特征类型、联合分布与手写决策规则。

   CC BY 4.0
3. [Samuel (1959), Some Studies in Machine Learning Using the Game of Checkers](https://www.cs.virginia.edu/~evans/greatworks/samuel1959.pdf)

   阅读从棋局表示、评价规则到经验改进的原始研究。
4. [Dive into Deep Learning: Introduction](https://d2l.ai/chapter_introduction/index.html)

   比较监督、无监督和强化学习的问题结构。

   CC BY-SA 4.0
