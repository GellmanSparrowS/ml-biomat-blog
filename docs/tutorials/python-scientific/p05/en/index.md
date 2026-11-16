# From One File to a Batch of Records

Source: https://ml-biomat.com/tutorials/python-scientific/p05/en/
Language: en

Read CSV files and a JSON manifest to make cooling records with different time units comparable.

## Let a program take over the recorded observations

A cup of hot water cools after it is placed on a table. Recording its temperature once a minute, and repeating the observation three times, produces three sets of time and temperature values. An instrument normally stores those values in files rather than Python variables. This chapter reads three files, turns text into meaningful numbers, converts time units, retains missing readings, and plots comparable cooling curves. It also produces a combined table and a summary, so that each plotted point remains connected to its run and original record.

The example contains explicitly constructed teaching readings. Ambient temperature is set to 20 °C, all runs begin at 80 °C, and observations extend to 300 s. R01 ends at 30 °C, R02 at 35 °C, and R03 at 40 °C. These labels describe the chosen trajectories rather than experimentally established container or material effects. Each run has six scheduled readings; R02 lacks temperature at two minutes. R01 and R03 store time in seconds, while R02 stores minutes. The raw numbers become comparable only when their units are read alongside them.

This resembles receiving a stack of observation sheets: first identify the sheets, then understand each one's fields and units, and finally transfer records into a common table. Paths locate the sheets, a CSV reader identifies fields, conversion functions create numerical values, and record identifiers preserve the connection to the original observations. Understanding those layers gives file reading a structure that can be adapted when an instrument changes its columns, units, or missing-value conventions.

## A path has a starting point

A file holds content; a directory organizes files and other directories; a path describes how to locate a target. The expression `Path('data') / 'run_01.csv'` represents run_01.csv inside the data directory. For a `Path` object, the slash joins path components instead of dividing numbers. Constructing the path does not read the file. Operations such as `open` and `read_text` access its contents. Separating the location from the operation also avoids manually assembling operating-system-specific path separators.

A relative path needs a starting point. In an interactive session, `Path('data')` is usually interpreted relative to the current working directory, which may differ from the directory containing the script. The complete example uses `Path(__file__).resolve().parent / 'data'` to locate data beside the script. Here `__file__` provides the script location, `resolve()` resolves it to an absolute path, `parent` selects the enclosing directory, and the slash adds data. Moving the complete example folder preserves this relationship even when its overall location changes.

### Inspect the file collection from the example directory

Prints run_01.csv, .csv, and three sorted filenames. This short interactive example starts from the current working directory.

```
from pathlib import Path

folder = Path("data")
path = folder / "run_01.csv"
print(path.name)
print(path.suffix)
print(sorted(p.name for p in folder.glob("run_*.csv")))
```

Inputs remain in data, and generated results go into the output directory supplied at execution. The program reads the original CSV files without writing calculated values back into them. The call `mkdir(parents=True, exist_ok=True)` creates the output directory, including required parents, and accepts an existing directory. Another run replaces same-named outputs there, so use separate names such as `output-a` and `output-b` when comparing analyses. The directory names express the purpose of a run while the example's relative layout remains straightforward.

A filename extension indicates a conventional format but does not guarantee its contents. Renaming an image with a .csv suffix does not create a table, and some CSV exports use semicolons rather than commas. Inspecting the first few lines reveals field names, delimiters, and likely encoding. Explicit checks can then enforce the expected structure. Understanding what is present in the input is the starting point for deciding whether a successful read is also a meaningful read.

A notebook cell usually has no script variable named `__file__`. In that setting, inspect the working directory with `Path.cwd()` and specify data relative to the location you have confirmed. A path problem is easier to solve by identifying one stable starting point than by copying inputs into many directories. For the complete command-line example, the script-relative convention lets code and data move together as one folder. Knowing which starting point is used explains why a read locates the intended file.

## Numbers in a CSV begin as text

A CSV record contains fields separated according to a text convention. The first record often names the fields; our files use `time,temperature,note`. Each later record contains one reading. `csv.DictReader` uses the header as dictionary keys, so `row['temperature']` retrieves the temperature field. At first, `'65.0'` is a string. Calling `float('65.0')` creates the floating-point number 65.0 that can enter arithmetic. A table's numerical appearance does not determine the types stored in a text file.

The expression `with path.open(...)` creates a controlled period of file access. The indented block reads from the stream, and leaving the block closes it, including when an exception occurs. The encoding `utf-8-sig` reads ordinary UTF-8 and accepts the initial byte-order marker added by some exporters. Setting `newline=''` lets the CSV module manage newline conventions without a second layer rewriting them. Encoding asks which characters the bytes represent; delimiting asks how those characters form fields. These are separate parts of reading.

![Raw R02 text, unit metadata, and typed records. Missing temperature becomes None; original minutes and normalized seconds are both retained.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a5f9ba3f1758d152fc2f4b61.svg?v=a5f9ba3f1758)

Figure 1Raw R02 text, unit metadata, and typed records. Missing temperature becomes None; original minutes and normalized seconds are both retained.

The first note in run_01.csv is `"start, open vessel"`, which contains a comma inside the text. CSV quoting preserves the whole note as one field. A manual `line.split(',')` would split it into two items and disturb the column correspondence. Quoted CSV fields can also contain newlines, so one logical CSV record need not occupy one physical text line. The example records a `source_record` number counted from the first data record, excluding the header, rather than claiming that this is always a physical line number.

An empty temperature field needs its own interpretation. The reader applies `strip()` to remove surrounding whitespace. An empty result becomes `None`; otherwise, `float` converts the text. This normalization concerns the numerical field, while note text is retained as written. Filling the absent reading with 0 °C would invent a measurement far below ambient temperature and create a sharp dip in the curve. Missing information and an observed numerical zero are distinct statements about the experiment.

The complete reader expects the field names and order defined for this example. Extra or missing fields, non-finite values, and negative times produce messages identifying the file and record. This suits a collection of exports with an agreed structure. To connect another instrument, first map its fields to the quantities used here, then adjust the reader. A similarly named column may describe a different channel or quantity. Field meaning, units, and the observational unit together determine which calculation can use it.

Decimal punctuation and delimiters can both depend on export settings. A file may use decimal commas and semicolon-separated fields, writing a temperature as `65,0`. Our example explicitly expects decimal points. Reading the alternative convention requires both a chosen CSV delimiter and a numerical conversion rule. Replacing every comma in the entire file could also alter punctuation inside notes. Apply conversions to fields that have already been parsed so the scope of a change matches the meaning of the field.

## Meaning must travel with numbers

Astronomy encountered a related problem early: how could an image from one observatory be interpreted by a different computer system? NASA's FITS history describes cross-system file exchange in 1979, followed by the basic format description published by Wells, Greisen, and Harten in 1981. FITS combines descriptive text headers with numerical data, allowing receiving software to interpret the organization and contents of an array. The connection to our example is that interpretation rules must travel with the values. Opening a file completes only the first part of exchanging a scientific observation.

![Original illustration of the FITS interchange problem. The 4×4 counts are constructed; descriptions supply dimensions, orientation, and scale. The analogous issue here is interpreting time values together with units.](https://ml-biomat.com/static/tutorials/python-scientific/figures/7e7f876c45ca1d9b955122b0.svg?v=7e7f876c45ca)

Figure 2Original illustration of the FITS interchange problem. The 4×4 counts are constructed; descriptions supply dimensions, orientation, and scale. The analogous issue here is interpreting time values together with units.

The sixteen numbers in the illustration are constructed counts for explaining a format, not an observed astronomical image. Alone, they do not specify direction, dimensions, or coordinate scale. Descriptive information supplies that context. Our example uses a small JSON manifest rather than implementing FITS: it states the run identifier for each CSV, the time unit, the temperature unit, and the chosen ambient temperature. JSON expresses named values and nested relationships conveniently; CSV expresses repeated rows of similarly structured observations.

A pixel is one cell in this illustrative array. An arcsecond is an angular unit equal to one three-thousand-six-hundredth of a degree. With the stated scale of 0.4 arcsecond between neighboring pixel centers, two cell spacings correspond to 0.8 arcsecond. The same index difference would represent another angular separation under a different scale. The displayed orientation and scale are chosen explanatory conditions, not universal rules for astronomical images. They show why an unchanged arrangement of numbers still needs measurement context, just as a time column needs seconds or minutes.

The function `json.loads` turns JSON text into Python objects. The outer manifest becomes a dictionary, and its `runs` field contains another dictionary associating each filename with its specification. JSON strings use double quotes, its missing marker is `null`, and its Boolean values are `true` and `false`. Reading converts these to Python's `None`, `True`, and `False`. These are defined representations of data. A JSON file does not need to be executed as Python code to recover the information it contains.

$$
t_{\mathrm{s}}=t_{\mathrm{min}}\times 60\,\mathrm{s/min}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd4a0a48d39daabe7bc7d1ae.svg) | The same time expressed in seconds, unit s |
| ![Formula](https://ml-biomat.com/static/agent-math/aacbc6362eba3545a7672631.svg) | Original time quantity, unit min |
| ![Formula](https://ml-biomat.com/static/agent-math/255625cb0300aa6fc822fba6.svg) | Conversion factor: sixty seconds per minute |
| ![Formula](https://ml-biomat.com/static/agent-math/66d58377d47e96b8baecdfbc.svg) | Multiplication; minutes cancel the denominator unit of the conversion factor |

R02 ends at 5 min; multiplying by 60 s/min gives 300 s. The stored fields are time_raw=5.0, time_unit=min, and time_s=300.0, different representations of the same observation time.

Multiplying R02's five minutes by 60 seconds per minute places its endpoint at 300 s, aligned with the other runs. The program looks up conversion factors in `{'s': 1.0, 'min': 60.0}`, retaining raw time, original unit, and converted `time_s` together. If the horizontal axis later appears suspicious, the converted value can be traced from 300 s back to five minutes. Unit conversion changes the numerical representation while preserving the observation's actual time.

## Process a defined collection of files

The expression `data_dir.glob('run_*.csv')` finds names beginning with run_ and ending with .csv. The asterisk matches zero or more intervening characters. Applying `sorted` produces a deterministic file order, after which the same `read_run` function processes every path. This makes repeated outputs easier to compare; it does not establish experimental chronology. Filenames such as run_1, run_2, and run_10 can sort with run_10 before run_2. Fixed-width identifiers or an explicit experimental index help distinguish textual ordering from scientific ordering.

The manifest also defines the intended collection. The script compares discovered filenames with manifest entries before proceeding. A missing input or an unintended file in the input directory is then detected before aggregation. During combination, `observations.extend(rows)` adds individual records from one run to the combined list. Using `append(rows)` instead would add the list itself, creating a list of lists. Both structures are valid, but the next loop would receive different kinds of objects. Choose according to whether the file-level nesting should remain part of the representation.

Every combined record retains `run_id`, `source_file`, and `source_record`. Combining files therefore preserves the identity of the three independent observations. Plotting separates runs by identifier, and time sorting occurs within each run. Repeated times within a run trigger an explicit check because they might represent replicate measurements, repeated exports, or separate channels. A meaningful response begins by defining those record identities, rather than silently deleting one of them.

Eighteen rows are not eighteen independent cooling experiments. Six times within one run describe the evolution of the same object, so treating them as six parallel specimens would misstate the experimental replication. One row here represents one reading, while run_id preserves the higher-level experimental grouping. Later comparisons among repeated experiments can still distinguish the objects through that identifier. Defining record granularity before combining files helps preserve the statistical meaning as the collection grows.

A SHA-256 digest maps a file's bytes to a fixed-length hexadecimal string. Identical content produces the same digest, while changing a value will ordinarily change it. The digest can therefore identify whether two analyses used the same file contents. Changes in encoding or newline conventions also change the bytes even if the displayed values look identical. This is a check of byte identity. Field names, units, and measurement definitions require their own interpretation, so the example retains both structured metadata and input digests.

## Read all results on a common time scale

The three curves use seconds on the horizontal axis and degrees Celsius on the vertical axis. R02 has no temperature at 120 s. For plotting, the example supplies `NaN` at that position so the line breaks there; the stored observation still uses `None` for absence. A sampling strip beneath the curves marks every scheduled reading, with a red cross at the absent one. Readers can therefore see both the observed change and the position where no temperature was provided.

![Three constructed cooling trajectories on a common time axis. Missing R02 temperature breaks its line and is marked in the sampling strip. Rates use endpoints over the same 300 s window.](https://ml-biomat.com/static/tutorials/python-scientific/figures/2991c6472881361273c2d9a0.svg?v=2991c6472881)

Figure 3Three constructed cooling trajectories on a common time axis. Missing R02 temperature breaks its line and is marked in the sampling strip. Rates use endpoints over the same 300 s window.

We compare the runs with a quantity that is easy to calculate independently: the mean temperature-change rate between the first and last valid readings. R01 changes from 80 to 30 °C, a difference of −50 °C over 300 s, giving approximately −0.1667 °C/s. The negative sign expresses decreasing temperature. Comparing magnitudes describes the size of the decrease while the plotted sign retains direction. An endpoint average compresses a window into one number; it is not the instantaneous rate at every time. R01 loses 19 °C during its first minute and only 3 °C during the last.

$$
\bar r=\frac{\Delta T}{\Delta t}=\frac{T_b-T_a}{t_b-t_a},\qquad t_b>t_a
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/034efae3b5f390a37ee38957.svg) | Mean temperature-change rate between available endpoints, °C/s |
| ![Formula](https://ml-biomat.com/static/agent-math/13f62c4a10f34a0609cd9de4.svg) | Temperatures at the first and last valid endpoints, °C |
| ![Formula](https://ml-biomat.com/static/agent-math/f213d0ac00827bc8c49482fb.svg) | Times corresponding to those endpoints, in s |
| ![Formula](https://ml-biomat.com/static/agent-math/1aeb1d02edb16548e34a25c6.svg) | Final minus initial temperature, °C; negative for cooling |
| ![Formula](https://ml-biomat.com/static/agent-math/ec5cb06e66e7cce442514c70.svg) | Elapsed endpoint time, s, strictly positive |
| ![Formula](https://ml-biomat.com/static/agent-math/c795c6799d8e90e39a1931b0.svg) | Delta denotes an endpoint difference; the bar denotes an interval average |

R02 gives (35−80)/(300−0)=−45/300=−0.15 °C/s. Misreading minutes as seconds gives −45/5=−9 °C/s, sixty times the magnitude. Temperature differences have equal numerical values in °C and K; these fields consistently use Celsius.

R02's absent point is internal, so its endpoints remain at zero and 300 s and give −0.15 °C/s. If the final reading were missing, the last valid time would move back to 240 s, changing the calculation window. Start and end times should therefore accompany the rate. With fewer than two valid temperatures, there are no two available endpoints to define a rate, so the function returns a missing value. Before comparing runs, check whether their numbers describe the same time interval.

A mean temperature answers a different question from a mean rate. R01's six temperatures sum to 291 °C, giving an equal-reading average of 48.5 °C. That describes the level of the six observations. The endpoint rate of approximately −0.1667 °C/s describes change per second over the interval. Their units make the distinction visible before any scientific interpretation is added. Also count intervals carefully: six time points contain five gaps, so observations from zero through 300 s cover five one-minute intervals, not six. Counting points and gaps on the graph provides a direct check of the time denominator. Keeping the level of the readings, their change, and the elapsed duration separate helps prevent an otherwise plausible calculation from answering the wrong question.

Reading R02's minutes as seconds would put its endpoints at zero and five seconds. The same −45 °C divided by five gives −9 °C/s, exactly sixty times the correct magnitude. The resulting curve can still look smooth, and division can complete successfully. The changed answer comes from interpreting the quantities incorrectly. Unit information at the reading stage influences the final graph and scientific comparison. Converting at the input boundary and putting units in normalized field names keeps later operations on one time scale.

## Read, convert, combine, and save

The downloadable example places three CSV files, a JSON manifest, and a data description in the data directory beside `main.py`. Computation uses the standard-library modules `pathlib`, `csv`, `json`, `math`, and `hashlib`; Matplotlib draws the figures. Start with `read_run` and follow one R02 record from text to seconds, then examine how the outer loop combines files. The example keeps all rows in lists for inspection. Larger datasets can be processed in chunks when storing the whole collection in memory becomes unnecessary or impractical.

### Complete batch reader and figures

The downloaded example includes the data directory with CSV inputs and unit manifest.

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

The `csv.DictWriter` uses an explicit output column order. Its `writeheader` method writes field names, and `writerows` writes the observations. In this CSV output, Python's `None` becomes an empty field. CSV has no separate missing-value type, so a later reader must apply the same convention. JSON instead writes `None` as `null`, retaining a structured marker. The summary is saved with `allow_nan=False`, causing unexpected non-finite floats to be reported instead of placing nonstandard numerical tokens in an exchange file.

### Run and save outputs

Creates combined.csv, summary.json, manifest.json, and three figures.

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

The actual run reads three files, eighteen records, and seventeen available temperatures. Endpoint rates are −0.166666…, −0.15, and −0.133333… °C/s. Reading the combined CSV back yields eighteen records, retains the comma inside the original note field, and preserves one empty temperature field. This write-and-read check confirms that the output structure can be recovered under the stated conventions. Figures support comparison, the combined table supports further analysis, and the summary retains selected numerical results. All are generated from the same converted records.

If a file cannot be found, inspect its name and the data directory beside the script. If the field check fails, inspect the header and delimiter. If float conversion fails, locate the identified record and check for text with attached units, a different missing marker, or a decimal comma. Following the sequence “path, text, fields, types, units, calculation” narrows the problem to a concrete operation. Keeping the input and changing the reader makes the correction repeatable.

Writing results is also an opportunity to preserve the meaning gained during reading. A column named `time_s` states the normalized unit, while `time_raw` and `time_unit` retain the original representation. The identifier distinguishes three observations that each begin at time zero. The record number identifies the row within its original file. A later reader can use the normalized columns immediately and still reconstruct the earlier choices when a detail needs examination.

## Where does one minute land on the axis?

The experiment displays raw fields, normalized times, curves, and endpoint rate together. Select R02 and confirm that raw time five corresponds to 300 s. Then enable “Ignore minute conversion” and observe the compressed horizontal scale and increased rate magnitude. Restore the unit interpretation and compare retaining the missing point, supplying an intermediate reading, and removing the final reading. An internal value changes the curve but leaves the endpoint rate unchanged when endpoints remain fixed. Removing the endpoint changes both the interval and its rate.

### From file fields to curves and rates

Select a run and change its unit interpretation or missing-data treatment. Curves, endpoint intervals, and rates update together. Normalized time means the seconds assigned by the current rule.

[Figure: Linked cooling curves and endpoint rates under unit and missing-data choices](https://ml-biomat.com/tutorials/python-scientific/p05/en/#P05-plot)

Pale thin curves represent the other two runs. The gray dashed curve places current readings with correct units; blue uses the selected interpretation. Blue covers gray where they coincide. The red dotted line joins endpoints to explain the interval average.

| Record | Raw time | Original unit | Normalized time | Temperature | Role |
| --- | --- | --- | --- | --- | --- |

These variations connect reading rules with scientific meaning. Which characters a file contains is an input question. Which seconds, degrees, and run those characters represent is a data-definition question. Which available endpoints enter a rate is an analysis question. The plotted curve carries all of those choices forward. When connecting a new instrument export, follow the same layers so that every conversion has a defined object and every reported result remains traceable to its observations.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Software Carpentry — Looping Over Data Sets](https://swcarpentry.github.io/python-novice-gapminder/14-looping-data-sets.html)

   Adapts discovery followed by repeated processing, using original cooling records and standard-library readers. Copyright The Carpentries.

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; original prose, code and figures.
2. [Python 3.14 — csv](https://docs.python.org/3.14/library/csv.html)

   Fields, quoting, newlines, and dictionary-based reading and writing.

   PSF documentation license
3. [Python 3.14 — pathlib](https://docs.python.org/3.14/library/pathlib.html)

   Relative paths, file discovery, and file access.

   PSF documentation license
4. [Python 3.14 — json](https://docs.python.org/3.14/library/json.html)

   Structured manifests and result exchange.

   PSF documentation license
5. [NASA FITS — The First Agreement](https://fits.gsfc.nasa.gov/users_guide/users_guide/node9.html)

   Historical facts on cross-system interchange and the basic definition.

   NASA institutional historical reference; original diagram, no reused image.
6. [NASA Science Data Portal — FITS](https://science.data.nasa.gov/fits)

   Scientific-file organization with text headers describing numerical data.

   NASA factual technical reference
