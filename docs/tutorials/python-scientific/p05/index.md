# 从一个文件到一批实验记录

Source: https://ml-biomat.com/tutorials/python-scientific/p05/
Language: zh-CN

读取CSV和JSON清单，把不同时间单位的冷却记录接成可比较的数据。

## 让程序接过仪器留下的记录

一杯热水放在桌上会逐渐冷却。如果每分钟记录一次温度，做三次这样的观察，我们会得到三组时间与温度。仪器通常把它们保存成文件，而不是直接放进Python变量。本章要完成的事情，是从一个文件夹读取三份记录，把文本转成有含义的数字，统一时间单位，保留缺失读数，再画出可以比较的冷却曲线。处理完以后，还会生成一张合并表和一份摘要，使“这个图里的点来自哪一次观察、哪一条记录”始终有答案。

本例使用三组明确构造的教学读数，环境温度设为20 °C，起点都为80 °C，观察到300 s。R01最后降到30 °C，R02到35 °C，R03到40 °C；这些名称描述所选数值轨迹，不表示经过实验检验的容器或材料效果。每组安排六次读数，R02在2 min时缺少温度。更值得留意的是，R01和R03的时间字段按秒写入，R02按分钟写入。原始文件中看似相同的数字，只有连同单位一起读取，才能放到同一横轴上比较。

这种工作很像接手一摞实验记录纸：先确认找到了哪些纸，知道每张纸的栏位和单位，再逐行抄入统一的表格。Python中的路径定位纸放在哪里，CSV解析器辨认每行的字段，转换函数把文字变成数字，记录中的编号和位置让新表还能指回原来的纸。理解这些层次后，文件读取就不会只剩下一句需要背诵的命令；当列数、单位或缺失格式发生变化时，也知道应该在哪一层处理。

## 文件在哪里，取决于路径从哪里出发

文件是保存内容的对象，文件夹把文件和其他文件夹组织在一起，路径则描述怎样找到目标。`Path('data') / 'run_01.csv'`表示data文件夹中的run_01.csv。这里的斜杠由`Path`对象解释为拼接路径，不是在做除法，也不立即读取文件。只有调用`open`、`read_text`这类操作时，程序才会接触文件内容。这种表示方式把“目标位置”与“准备对它做什么”分开，也减少了手动拼接不同系统分隔符的麻烦。

相对路径需要一个出发点。在交互窗口里写`Path('data')`，通常相对于当前工作目录；这个目录可以与程序文件所在位置不同。完整例子使用`Path(__file__).resolve().parent / 'data'`，从当前脚本的位置找到旁边的data目录。`__file__`提供脚本位置，`resolve()`得到解析后的绝对路径，`parent`取它的父目录，最后再接上data。这样，读者把整个示例文件夹移动到另一个位置，只要脚本与data的相对关系保持不变，就仍能找到输入。

### 在示例目录中查看文件集合

输出run_01.csv、.csv和三个已排序的文件名；这段交互示例以当前工作目录为起点。

```
from pathlib import Path

folder = Path("data")
path = folder / "run_01.csv"
print(path.name)
print(path.suffix)
print(sorted(p.name for p in folder.glob("run_*.csv")))
```

示例的输入放在data中，输出放进运行参数指定的output中。程序只读取输入，不把结果写回原始CSV。`mkdir(parents=True, exist_ok=True)`负责创建输出目录：需要时一并创建上层目录，目录已经存在时继续使用。再次运行会覆盖这个输出目录里的同名结果，所以需要比较两次分析时，可以分别使用`output-a`和`output-b`。目录名称由工作目的决定，代码中的相对布局则保持简单、清楚。

文件后缀帮助人和软件识别常见格式，却不保证内部内容一定符合格式。把一张图片改名为.csv不会使它变成表格；同样，一个CSV文件也可能采用分号而不是逗号分隔。读取之前可以先打开前几行，观察字段名称、分隔符和编码。程序中的明确检查会进一步核对约定，但理解输入长什么样，仍是判断读取结果是否合理的起点。

在笔记本环境里，代码单元通常没有`__file__`这个脚本变量，这时可以先用`Path.cwd()`查看当前工作目录，再相对于已经确认的位置指定data。路径问题不需要通过到处复制输入文件来解决；确认一个稳定的出发点，就能解释每次读取为什么找到同一个目标。终端里执行完整示例时，则保留脚本相对位置的写法，让代码和数据作为一个文件夹一起移动。

## CSV中的数字，最初只是文字

CSV把一条记录写成一组分隔的字段，第一行常用来写字段名。本例固定为`time,temperature,note`，后面每行是一次读数。`csv.DictReader`用第一行作为键，把后续记录读成字典，因此可以用`row['temperature']`取温度字段。刚读进来的`'65.0'`是字符串，`float('65.0')`才得到可参与算术的浮点数65.0。表格看起来像数字，并不意味着文本文件已经替程序决定了数字类型。

读取时用`with path.open(...)`建立一个临时的文件访问范围。缩进块里可以从文件读取，离开块时文件会关闭，即使中途发生异常也会完成关闭。这里写`encoding='utf-8-sig'`，既能读取普通UTF-8文本，也能处理某些软件在UTF-8开头加入的字节顺序标记。`newline=''`让CSV模块按其规则处理换行，避免文本层与CSV层同时改写换行符。编码解决“这些字节表示什么字符”，分隔符解决“这些字符怎样分成字段”，它们是两件事。

![R02文件的原始文本、清单中的单位和转换后的记录。空温度保存为None，原始分钟值与统一秒数同时保留。](https://ml-biomat.com/static/tutorials/python-scientific/figures/aabc966271befd88737c7590.svg?v=aabc966271be)

图 1R02文件的原始文本、清单中的单位和转换后的记录。空温度保存为None，原始分钟值与统一秒数同时保留。

注意run_01.csv的第一条注释是`"start, open vessel"`，文字内部也有一个逗号。CSV用双引号把整个注释包成一个字段，读取后得到包含逗号的完整字符串。直接使用`line.split(',')`会把它拆成两项，导致字段错位。类似地，带引号的CSV字段还可以包含换行，因此“一条CSV记录”不总等于“文件里的一条物理文本行”。程序保存的是`source_record`，从第一条数据记录开始计数，字段名本身不计入。

空温度字段需要单独处理。程序先用`strip()`去掉字段两端空白，如果剩下空字符串，就保存为`None`；否则再用`float`转换。这项约定只应用于数值字段，注释中的文字空格仍按原样保留。把空值自动填成0 °C，会凭空增加一个远低于环境温度的读数，在冷却曲线上制造尖锐凹口。缺少一次测量描述的是信息缺失，数值零则描述一次具体的温度，两者不能互换。

在完整代码中，字段名和顺序需要与本例约定一致，额外字段、缺失字段、非有限数字或负时间会指出具体文件和记录位置。这样的检查适合格式已经确定的一组仪器输出。若接入另一台仪器，先明确其字段与这里字段的对应关系，再调整读取函数；不要把一个名称相近的列悄悄当成温度。列的含义、单位和记录粒度共同决定它能进入哪一个计算。

小数点和分隔符也可能受导出设置影响。有些文件用逗号写小数、分号隔开字段，温度会写成`65,0`；本例约定用点表示小数，因而不会自动接受这种写法。接入这类文件时，需要同时设置CSV分隔符并明确数值转换规则，而不是对整份文件全局替换逗号，因为注释里的标点也可能被改掉。每次转换尽量针对已经解析好的字段，修改范围才与字段含义一致。

## 数字能交换，含义也要一起交换

天文学曾经很早面对这种问题：一个观测站获得的图像，怎样让另一套计算机正确读取？NASA的FITS历史说明，1979年已经进行跨系统文件交换，Wells、Greisen和Harten在1981年发表了基本格式的描述。FITS把描述数据组织方式的文本头与数值数据放在一起，让接收方能够理解数组怎样排列、包含什么内容。这里值得带走的思想，是数据的解释规则需要与数据一起传递；文件能够被打开，只完成了交换工作的第一步。

![FITS交换问题的原创图解。4×4计数为构造示意，右侧给出尺寸、方向与尺度说明；对应到本章，时间数值与单位必须共同解释。](https://ml-biomat.com/static/tutorials/python-scientific/figures/95f57e860535a2e141b62637.svg?v=95f57e860535)

图 2FITS交换问题的原创图解。4×4计数为构造示意，右侧给出尺寸、方向与尺度说明；对应到本章，时间数值与单位必须共同解释。

图中的十六个数字是为解释格式构造的示意计数，不是实际天文图像。仅看它们，读者不知道横纵方向、尺寸和坐标尺度；加上描述信息，才知道如何给数值定位。本例不需要学习FITS的二进制组织，而是把类似的信息放进一个小型JSON清单：每个CSV对应哪个run_id，时间用秒还是分钟，温度单位是什么，环境温度设为多少。JSON适合表达这种带名称、列表和嵌套关系的结构，CSV适合保存反复出现的同类观测行。

图中的像素就是数组里一个小格，角秒是角度单位，一角秒为一度的三千六百分之一。若约定相邻格中心相隔0.4角秒，两个格距对应0.8角秒；索引之差相同，换用另一坐标尺度后，物理角度距离便会不同。方向和尺度在图中都是为说明问题设置的条件，并不是所有天文图像统一采用的规则。它们说明为什么“数字排列相同”仍需要配上测量解释，正如本章的时间列需要配上秒或分钟。

`json.loads`把一段JSON文字读成Python对象。清单外层变成字典，`runs`又对应一个字典，里面每个文件名关联自己的说明。JSON中的字符串使用双引号，缺失标记写`null`，布尔值写`true`和`false`；读入Python后分别对应`None`、`True`和`False`。两种表示之间存在明确对应，不能把JSON文件当作任意Python代码执行，也不需要执行它才能读取其中的信息。

$$
t_{\mathrm{s}}=t_{\mathrm{min}}\times 60\,\mathrm{s/min}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd4a0a48d39daabe7bc7d1ae.svg) | 换算为秒的同一时间量，单位s |
| ![Formula](https://ml-biomat.com/static/agent-math/aacbc6362eba3545a7672631.svg) | 原始时间量，单位min |
| ![Formula](https://ml-biomat.com/static/agent-math/255625cb0300aa6fc822fba6.svg) | 一分钟对应60秒的换算因子 |
| ![Formula](https://ml-biomat.com/static/agent-math/66d58377d47e96b8baecdfbc.svg) | 乘法；分钟单位与换算因子的分母相消 |

R02的末点为5 min，乘60 s/min得到300 s。程序保存的time_raw为5.0，time_unit为min，time_s为300.0；同一次观察以不同单位表示。

R02的5 min乘以60 s/min后成为300 s，才能与其他两组的末点对齐。完整程序用`{'s': 1.0, 'min': 60.0}`查找换算因子，再为每条记录同时保存原始时间、原始单位和统一后的`time_s`。保留原字段有一个直接好处：当曲线横轴看起来不对时，可以从300 s追回5 min，检查换算是否符合约定。单位换算改变数值表示，不改变这一次观测真正发生的时刻。

## 从读一个文件，走到有顺序的一批文件

`data_dir.glob('run_*.csv')`查找名称以run_开头、以.csv结尾的文件，星号允许中间出现零个或多个字符。程序再用`sorted`得到确定的文件顺序，随后在循环里对每个路径调用同一个`read_run`函数。这个顺序让输出在重复运行时便于比较，却不是实验时间的证明；真正的时间来自记录字段。文件名若写成run_1、run_2、run_10，按文字排序时run_10可能排在run_2前面，固定宽度编号或明确的实验索引能避免把文件排列误当成科学顺序。

清单还承担检查文件集合的作用。程序比较实际找到的文件名与清单列出的文件名，两边相同才继续。若少放了一份CSV，或者输出结果误混进输入目录，就能在汇总前发现。合并时使用`observations.extend(rows)`，把一个文件的多条记录依次加入总列表；若用`append(rows)`，加入的会是整个列表对象，总列表就变成“列表的列表”。两种结构都合法，后续循环读取的对象层次却不同，选择取决于是否想保留文件层级。

每条合并记录保留`run_id`、`source_file`和`source_record`。因此，合并不是把三组数字揉成一条看不出身份的长曲线。画图前仍按run_id区分三次独立观察，时间排序也只在各次观察内部进行。程序还检查同一run内是否出现重复时间，因为重复时间可能表示重复测量、重复导出或不同通道，需要明确规则才能处理。遇到这种情况，先把记录身份定义补充完整，比直接删除其中一条更能保留实验含义。

十八条观测行也不等于十八次独立冷却实验。同一次run里的六个时刻属于同一个对象随时间的变化，不能把它们当成六个平行样品去增加实验次数。合并表采用一行一次读数，run_id保存更高一层的实验归属；将来计算重复实验间的差异时，仍可按这个字段区分对象。记录粒度先定义清楚，文件越多时，统计含义反而越容易保持稳定。

输入文件的SHA-256摘要把文件字节映射成一串固定长度的十六进制字符。相同内容会得到相同摘要，修改一个数值通常就会改变它，因而适合检查两次分析是否使用同一份文件。换行或编码变化也会改变摘要，即使表格数值看起来一样；它检验的是文件内容的字节一致性。它没有替代单位、列名和测量定义的检查，所以本例同时保存结构化字段与输入摘要，两者分别回答“内容有没有变”和“内容该怎样解释”。

## 把结果放到同一时间尺度上读

三条曲线的横轴统一为秒，纵轴为摄氏温度。R02在120 s处没有读数，完整程序把该位置交给绘图时设成`NaN`，使折线在缺失处断开；原始记录中的缺失仍保存为`None`。曲线下方的采样位置条直接标出每次安排的读数，红色叉号对应缺失。这样，读者既看得到测到的变化，也看得到数据在哪一处没有提供温度，不会把一条跨过空白的直线误读成连续观测。

![三组构造冷却读数，统一时间轴为秒。R02缺失中间温度，折线断开且采样条标叉；右侧速率由相同300 s窗口的首末点计算。](https://ml-biomat.com/static/tutorials/python-scientific/figures/d06f65344100d00f9002182f.svg?v=d06f65344100)

图 3三组构造冷却读数，统一时间轴为秒。R02缺失中间温度，折线断开且采样条标叉；右侧速率由相同300 s窗口的首末点计算。

为了给出一个容易手算的比较量，我们用首末有效点计算平均温度变化率。R01从80降到30 °C，温度变化为−50 °C，历时300 s，所以平均速率约为−0.1667 °C/s。负号表示温度降低；若只想比较下降快慢，可以比较它们的绝对值，同时保留图上的方向。平均速率把整个窗口压缩成一个数，不等于每一时刻的瞬时速率。R01前一分钟下降19 °C，最后一分钟只下降3 °C，原始曲线仍保留着这种变化。

$$
\bar r=\frac{\Delta T}{\Delta t}=\frac{T_b-T_a}{t_b-t_a},\qquad t_b>t_a
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/034efae3b5f390a37ee38957.svg) | 首末有效点之间的平均温度变化率，°C/s |
| ![Formula](https://ml-biomat.com/static/agent-math/13f62c4a10f34a0609cd9de4.svg) | 首个和末个有效点的温度，°C |
| ![Formula](https://ml-biomat.com/static/agent-math/f213d0ac00827bc8c49482fb.svg) | 这两个点对应的时间，统一为s |
| ![Formula](https://ml-biomat.com/static/agent-math/1aeb1d02edb16548e34a25c6.svg) | 末温减初温，°C；负值表示降温 |
| ![Formula](https://ml-biomat.com/static/agent-math/ec5cb06e66e7cce442514c70.svg) | 末时刻减初时刻，s，需大于零 |
| ![Formula](https://ml-biomat.com/static/agent-math/c795c6799d8e90e39a1931b0.svg) | Δ表示两个端点的差；上横线表示整个窗口的平均值 |

R02：(35−80)/(300−0)=−45/300=−0.15 °C/s。若把分钟误当秒，则错误地算成−45/5=−9 °C/s，数值大小扩大60倍。温差用°C或K有相同数值；这里始终使用摄氏温度字段。

本例R02缺失的是中间点，首末点仍为0与300 s，因此平均速率可以由保留的端点算出−0.15 °C/s。如果缺的是最后一个点，最后有效时刻会退到240 s，统计窗口随之改变；输出中的起止时间就必须与速率一起查看。少于两个有效温度时，无法形成两个不同时间的端点，函数返回缺失速率。跨组比较时，先核对时间窗口是否相同，再讨论速率大小，才知道数字回答的是不是同一个问题。

平均温度和平均变化率也需要分清。R01六个读数相加为291 °C，按读数等权平均得到48.5 °C，回答的是这六个观测值处于怎样的温度水平；−0.1667 °C/s回答的是整个窗口平均每秒变化多少。两者的单位已经提示它们在描述不同对象。六个时间点之间只有五段间隔，因此观察从0到300 s，并不是六段一分钟。先在图上数点、数间隔，再写分母，是检查时间计算很直接的方法。

若把R02的分钟数直接当成秒，首末时间会变成0与5 s，同一个−45 °C变化除以5，就得到−9 °C/s，恰好是正确值的60倍。图线看上去依然光滑，程序也可以顺利完成除法；错误来自量的解释，而不是算式写错。这个例子说明，读取文件时的单位信息会一直影响到最终图形和结论。把转换规则放在输入边界，并在输出列名写明统一单位，能使后续每一步都使用同一种时间尺度。

## 完整程序：读取、转换、合并，再保存

下载示例中，`main.py`旁边的data目录包含三份CSV、一份JSON清单和数据说明。计算使用Python标准库中的`pathlib`、`csv`、`json`、`math`与`hashlib`，图由Matplotlib生成。可以先阅读`read_run`，跟踪一条R02记录从字符串进入统一秒数，再看主循环怎样把三份结果连起来。这里把三组读数都保存在列表中，便于初学者检查每条记录；数据规模很大时，可以逐块处理，避免把全部文件一次装进内存。

### 完整批量读取与绘图

data目录随示例下载，包含原始CSV和单位清单。

```
"""Read three cooling CSV files with explicit per-file time units."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def read_run(path, specification):
    """Return typed observations in seconds and degrees Celsius."""
    factors = {'s': 1.0, 'min': 60.0}
    factor = factors[specification['time_unit']]
    rows = []
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['time', 'temperature', 'note']:
            raise ValueError(f'{path.name}: expected time,temperature,note')
        for record_index, row in enumerate(reader, start=1):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path.name}, record {record_index}: field count differs')
            try:
                time_raw = float(row['time'])
                temperature_text = row['temperature'].strip()
                temperature = float(temperature_text) if temperature_text else None
            except ValueError as error:
                raise ValueError(f'{path.name}, record {record_index}: invalid numeric field; {error}') from error
            if not math.isfinite(time_raw) or time_raw < 0:
                raise ValueError(f'{path.name}, record {record_index}: invalid time')
            if temperature is not None and not math.isfinite(temperature):
                raise ValueError(f'{path.name}, record {record_index}: invalid temperature')
            rows.append({'run_id': specification['run_id'], 'source_file': path.name,
                         'source_record': record_index, 'time_raw': time_raw,
                         'time_unit': specification['time_unit'], 'time_s': time_raw * factor,
                         'temperature_C': temperature, 'note': row['note']})
    rows.sort(key=lambda row: row['time_s'])
    times = [row['time_s'] for row in rows]
    if len(set(times)) != len(times):
        raise ValueError(f'{path.name}: repeated times need an explicit replicate rule')
    return rows


def summarize_run(rows):
    valid = [row for row in rows if row['temperature_C'] is not None]
    if len(valid) < 2:
        return {'record_count':len(rows), 'valid_count':len(valid), 'mean_rate_C_per_s':None}
    first, last = valid[0], valid[-1]
    duration = last['time_s'] - first['time_s']
    change = last['temperature_C'] - first['temperature_C']
    return {'record_count':len(rows), 'valid_count':len(valid),
            'start_time_s':first['time_s'], 'end_time_s':last['time_s'],
            'temperature_change_C':change, 'duration_s':duration,
            'mean_rate_C_per_s':change / duration}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    data_dir=Path(__file__).resolve().parent/'data'
    manifest=json.loads((data_dir/'manifest.json').read_text(encoding='utf-8'))
    if manifest['temperature_unit']!='degC':
        raise ValueError('This example expects temperatures in degrees Celsius')
    paths=sorted(data_dir.glob('run_*.csv'))
    if {path.name for path in paths}!=set(manifest['runs']):
        raise ValueError('Discovered files and manifest entries differ')
    observations=[];runs={};hashes={'manifest.json':hashlib.sha256((data_dir/'manifest.json').read_bytes()).hexdigest()}
    for path in paths:
        spec=manifest['runs'][path.name]
        rows=read_run(path,spec)
        observations.extend(rows)
        runs[spec['run_id']]={'specification':spec,'rows':rows,'summary':summarize_run(rows)}
        hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    columns=['run_id','source_file','source_record','time_raw','time_unit','time_s','temperature_C','note']
    with (args.output/'combined.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns);writer.writeheader();writer.writerows(observations)
    with (args.output/'combined.csv').open(encoding='utf-8',newline='') as stream:
        reread=list(csv.DictReader(stream))
    assert len(reread)==18
    assert reread[0]['note']=='start, open vessel'
    assert sum(row['temperature_C']=='' for row in reread)==1
    assert math.isclose(runs['R02']['summary']['mean_rate_C_per_s'],-.15)
    zh=args.language=='zh'
    def tr(z,e):return z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ['Noto Sans CJK SC','Microsoft YaHei','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':15,'axes.titleweight':'bold','svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36','axes.labelcolor':'#172b36','axes.spines.top':False,'axes.spines.right':False})
    blue,red,green='#28648a','#b85336','#467a62';colors=[blue,red,green]
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,.9])
    ax=fig.add_subplot(gs[0,0]);ax.axis('off');ax.set_title(tr('a  CSV保存文本字段','a  CSV stores text fields'),loc='left')
    text='run_02.csv\n'+(data_dir/'run_02.csv').read_text(encoding='utf-8').strip()
    ax.text(.02,.93,text,va='top',fontsize=14,linespacing=1.55,transform=ax.transAxes)
    ax=fig.add_subplot(gs[0,1]);ax.axis('off');ax.set_title(tr('b  清单补上测量含义','b  A manifest supplies meaning'),loc='left')
    for i,(k,v) in enumerate([('run_id','R02'),('time_unit','min'),('temperature_unit','degC'),('ambient_temperature_C','20.0')]):
        y=.84-i*.18;ax.text(.02,y,k,fontsize=13,transform=ax.transAxes);ax.text(.88,y,v,color=red,ha='right',fontsize=15,transform=ax.transAxes)
    ax.text(.02,.07,tr('空字段 → None\n时间字段 × 60 → 秒','Empty field → None\nTime field × 60 → seconds'),fontsize=15,color=blue,transform=ax.transAxes)
    ax=fig.add_subplot(gs[1,:]);ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,4)
    ax.text(.1,3.65,tr('c  转换后的记录保留身份与原始数值','c  Typed records retain identity and original values'),fontsize=16,weight='bold')
    xs=[.15,1.4,3.4,5.6,7.6,9.4];heads=['run_id','source_record','time_raw','time_unit','time_s','temperature_C']
    for x,h in zip(xs,heads):ax.text(x,2.9,h,fontsize=12,weight='bold')
    for j,r in enumerate(runs['R02']['rows'][1:4]):
        y=2.2-j*.7;ax.add_patch(Rectangle((.1,y-.14),11.5,.55,color=red if r['temperature_C'] is None else blue,alpha=.07))
        values=[r['run_id'],r['source_record'],r['time_raw'],r['time_unit'],r['time_s'],'None' if r['temperature_C'] is None else r['temperature_C']]
        for x,value in zip(xs,values):ax.text(x,y,str(value),fontsize=13)
    save(fig,'file-to-record')

    fig=plt.figure(figsize=(12,7.8),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.4,1],height_ratios=[1,.26])
    ax=fig.add_subplot(gs[0,0])
    for (rid,run),col in zip(runs.items(),colors):
        rr=run['rows'];ax.plot([r['time_s'] for r in rr],[r['temperature_C'] if r['temperature_C'] is not None else math.nan for r in rr],'-o',color=col,label=rid,lw=2,ms=6)
    ax.axhline(manifest['ambient_temperature_C'],color='#76837c',ls='--',lw=1,label=tr('环境20°C','Ambient 20°C'))
    ax.set(xlabel=tr('统一时间 / s','Common time / s'),ylabel=tr('温度 / °C','Temperature / °C'),title=tr('a  三次独立冷却记录','a  Three independent cooling records'),ylim=(16,85),xlim=(-10,310),xticks=[0,60,120,180,240,300]);ax.legend(frameon=False,ncols=2);ax.grid(alpha=.15)
    ax=fig.add_subplot(gs[1,0]);ax.set_xlim(-10,310);ax.set_ylim(-.6,2.6)
    for i,(rid,run) in enumerate(runs.items()):
        for r in run['rows']:ax.scatter(r['time_s'],i,marker='x' if r['temperature_C'] is None else 's',color=red if r['temperature_C'] is None else '#a4b6b5',s=65)
    ax.set(yticks=[0,1,2],yticklabels=list(runs),xticks=[0,60,120,180,240,300],xlabel=tr('采样位置 / s；×为缺失','Sampling positions / s; × marks missing'));ax.invert_yaxis();ax.spines[['left','bottom']].set_visible(False)
    ax=fig.add_subplot(gs[:,1]);rates=[r['summary']['mean_rate_C_per_s'] for r in runs.values()]
    ax.barh(list(runs),rates,color=colors,height=.5);ax.axvline(0,color='#172b36',lw=1)
    for i,v in enumerate(rates):ax.text(v-.008,i,f'{v:.4f}',ha='right',va='center',fontsize=13)
    ax.set(xlim=(-.25,.01),xlabel=tr('首末有效点平均速率 / °C·s⁻¹','Endpoint mean rate / °C·s⁻¹'),title=tr('b  相同300 s窗口比较','b  Compare the same 300 s window'));ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
    save(fig,'cooling-results')

    fig=plt.figure(figsize=(12,7.3),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1,1.2],height_ratios=[1,.5])
    pixels=[[0,0,1,0],[0,2,8,1],[1,4,6,0],[0,1,0,0]]
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(pixels,cmap='cividis',vmin=0,vmax=8,origin='lower')
    for i,row in enumerate(pixels):
        for j,v in enumerate(row):ax.text(j,i,str(v),ha='center',va='center',fontsize=15,color='white' if v<4 else '#172b36')
    ax.set(xticks=range(4),yticks=range(4),xlabel=tr('列索引','Column index'),ylabel=tr('行索引','Row index'),title=tr('a  数组本身：16个数值','a  An array: sixteen values'))
    ax=fig.add_subplot(gs[0,1]);ax.axis('off');ax.set_title(tr('b  描述信息让接收者读懂数组','b  Description makes the array interpretable'),loc='left')
    items=[(tr('尺寸','Dimensions'),'4 × 4'),(tr('数值含义','Value meaning'),tr('示意计数','Illustrative counts')),(tr('方向','Orientation'),tr('原点在左下','Origin at lower left')),(tr('坐标尺度','Coordinate scale'),tr('每像素0.4角秒','0.4 arcsec per pixel'))]
    for i,(k,v) in enumerate(items):
        y=.85-i*.22;ax.text(.01,y,k,fontsize=14,transform=ax.transAxes,color=blue);ax.text(.43,y,v,fontsize=14,transform=ax.transAxes)
    ax=fig.add_subplot(gs[1,:]);ax.axis('off');ax.text(.01,.79,tr('FITS：把数据的组织方式与数值一起交换','FITS: exchange the organization of data together with its values'),fontsize=18,weight='bold',transform=ax.transAxes)
    ax.text(.01,.46,tr('1979 年跨系统交换 → 1981 年发表基本定义','Cross-system exchange in 1979 → basic definition published in 1981'),fontsize=14,transform=ax.transAxes)
    ax.text(.01,.1,tr('本章中的同类问题：CSV的时间值 + JSON中的单位 → 可比较的冷却曲线','The corresponding issue here: CSV time values + JSON units → comparable cooling curves'),fontsize=14,color=red,transform=ax.transAxes)
    save(fig,'metadata-history')
    r02_valid=[r for r in runs['R02']['rows'] if r['temperature_C'] is not None]
    incorrect_rate=(r02_valid[-1]['temperature_C']-r02_valid[0]['temperature_C'])/(r02_valid[-1]['time_raw']-r02_valid[0]['time_raw'])
    summary={'dataset':manifest['description'],'file_count':len(paths),'record_count':len(observations),'valid_count':sum(r['temperature_C'] is not None for r in observations),'input_sha256':hashes,'runs':{rid:run['summary'] for rid,run in runs.items()},'unit_error_R02_rate_if_minutes_read_as_seconds':incorrect_rate,'roundtrip_record_count':len(reread),'quoted_note_roundtrip':reread[0]['note']}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    (args.output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['file_count','record_count','valid_count','runs']},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
```

`csv.DictWriter`按明确的列名顺序写出合并表，`writeheader`写字段名，`writerows`写全部记录。Python的`None`在这个CSV输出中成为空字段；CSV本身没有独立的缺失类型，重新读取时仍需按约定解释为空值。JSON摘要则把`None`写为`null`，保留结构化的缺失含义。程序用`allow_nan=False`保存摘要，让意外出现的非有限浮点数直接被指出，避免把不规范的数值标记悄悄写入交换文件。

### 运行与输出

生成combined.csv、summary.json、manifest.json和三幅图。

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

这份程序实际得到3个文件、18条记录和17个有效温度。三个端点平均速率依次为−0.166666…、−0.15和−0.133333… °C/s；合并CSV再次读取后仍有18条记录，注释中的逗号仍位于同一个字段，缺失温度仍保留为空字段。这次“写出再读回”的检查，验证了输出结构能够按相同约定恢复。图像适合快速比较，合并表适合继续分析，摘要适合记录关键数值；它们来自同一批已转换记录。

保存时也在保存读取过程中获得的含义。`time_s`明确统一单位，`time_raw`和`time_unit`保留原来的表示；run_id区分都从零时刻开始的三次观察，记录号又把每一点定位到对应文件内部。后续程序可以直接使用统一后的列，需要检查细节时仍能沿原始字段回看。这样的表格不仅适合当前绘图，也为下一步换用数组和数据表工具留下了清楚的接口。

如果程序提示某个文件未找到，先核对脚本旁的数据目录及文件名；如果字段检查报错，就查看表头和实际分隔符；如果浮点转换失败，就定位提示的记录，检查那里是否出现了带单位的文字、其他缺失标记或小数逗号。把问题沿着“路径—文本—字段—类型—单位—计算”的顺序缩小，通常能找到明确的修改位置。保留原始文件，再在读取步骤调整规则，能让修正被完整重复执行。

## 交互检查：一分钟究竟被放在横轴哪里？

下方实验选择一组记录后，会同时显示原始字段、统一时间、温度曲线与端点速率。先选择R02，确认原始时间5对应300 s；再打开“忽略分钟换算”，观察曲线横向压缩与速率增大。恢复正确单位后，分别保留缺失、补入一个中间读数或把最后读数设为缺失。你会看到中间点改变曲线形状，但首末点不变时端点平均速率保持原值；末点缺失则会同时改变计算窗口与速率。

### 从文件字段到曲线与速率

选择记录，改变单位解释或缺失处理，同时观察曲线、端点窗口和平均速率。表中“统一时间”表示当前规则给出的秒数。

[Figure: 时间单位与缺失处理联动的冷却曲线和速率比较](https://ml-biomat.com/tutorials/python-scientific/p05/#P05-plot)

浅灰细线是另外两次观察。灰色虚线按正确单位放置当前读数，蓝线采用当前选择；两者重合时蓝线盖住灰线。红色点线只连接端点，用来解释平均速率。

| 记录号 | 原始时间 | 原单位 | 统一时间 | 温度 | 计算角色 |
| --- | --- | --- | --- | --- | --- |

这几种变化把读取规则与科学解释连在了一起。一个文件保存了哪些字符，是输入层的问题；这些字符代表几秒、几度以及哪次观察，是数据定义的问题；用哪些有效点计算平均变化率，是分析的问题。最后画出的曲线汇集了这些选择。下一次面对仪器导出的新格式，可以沿着同样的顺序逐层接入，让每一次转换都有明确对象，最终结果也能追溯到原来的记录。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P05.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Software Carpentry — Looping Over Data Sets](https://swcarpentry.github.io/python-novice-gapminder/14-looping-data-sets.html)

   沿用发现文件集合后统一循环处理的教学顺序，改为原创冷却记录与标准库读取。Copyright The Carpentries。

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; original prose, code and figures.
2. [Python 3.14 — csv](https://docs.python.org/3.14/library/csv.html)

   字段解析、引号、换行与字典式读写。

   PSF documentation license
3. [Python 3.14 — pathlib](https://docs.python.org/3.14/library/pathlib.html)

   相对路径、文件发现与文件访问。

   PSF documentation license
4. [Python 3.14 — json](https://docs.python.org/3.14/library/json.html)

   结构化清单与结果交换。

   PSF documentation license
5. [NASA FITS — The First Agreement](https://fits.gsfc.nasa.gov/users_guide/users_guide/node9.html)

   跨系统交换与基本定义发表的历史事实。

   NASA institutional historical reference; original diagram, no reused image.
6. [NASA Science Data Portal — FITS](https://science.data.nasa.gov/fits)

   文本头描述数值数据的科学文件思想。

   NASA factual technical reference
