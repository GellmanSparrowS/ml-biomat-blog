# 找到耗时在哪里，再提高效率

Source: https://ml-biomat.com/tutorials/python-scientific/p28/
Language: zh-CN

用同一个邻近对计数问题，比较真实耗时、数组形状和内存，再判断局部提速能改变多少整体工作。

## 让一次科学计算更快，需要先看它在做什么

一个程序处理一百个颗粒位置时几乎立即结束，换成几千个位置后却要等待很久。这样的变化在显微颗粒追踪、分子结构分析和空间邻域计算中很常见：我们想知道哪些对象彼此接近，程序便需要比较许多位置。提高效率的第一步，是把科学问题、计算次数和数据形状连接起来；随后测量时间花在哪里，再选择合适的实现。这样得到的改进不仅能让当前例子更快，也能解释数据规模继续增加时会发生什么。

本章比较同一个任务的三种写法：Python 双循环、NumPy 完整广播，以及按行分块的 NumPy 计算。输入是明确生成的二维教学坐标，分布在边长 10 μm 的正方形内；任务是统计距离严格小于 1 μm 的无序点对。三种方法必须给出同一个整数，再比较耗时和内存。在保存的 800 点计时记录中，三种方法都得到 9106 对，单次中位时间分别约为 130.47、8.90 和 5.47 ms，最后一个结果使用 64 行分块。图中还保留七次实际计时，便于看清这些代表值来自怎样的重复测量。

速度与内存需要一起考虑。完整广播把大量标量操作交给 NumPy，但会创建随点数平方增长的中间数组；分块则一次处理一部分点对，随后复用工作空间。它们仍然比较同一批点对，只是组织计算的方式不同。把这个例子讲清楚后，读者可以更有依据地选择广播、分块或进一步采用空间索引，而不必把“循环少”当作判断程序好坏的唯一标准。

## 先固定计数规则，才能比较不同写法

每个点由两个坐标表示，分别对应水平和竖直方向，单位都是 μm。两个点的坐标差给出一段直角三角形的两条直角边，距离平方由两条边长的平方相加得到。我们只需判断距离是否小于某个半径，因此可以直接比较距离平方与半径平方，省去每一对点的开平方。半径为正时，这两种比较具有相同顺序关系；输入和阈值都应使用同一长度单位。

$$
d_{ij}^2=(x_i-x_j)^2+(y_i-y_j)^2,\qquad d_{ij}^2<r^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | 点 i 与点 j 的欧氏距离，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/5e1d0f9befd63fa0c25bf752.svg) | 两个点的水平、竖直坐标，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | 正的邻域半径，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 点的编号，无量纲；只计 j 大于 i 的点对 |

坐标差是直角三角形的两条直角边，勾股关系给出距离平方。正距离与正半径的大小顺序在平方后保持不变，所以不必逐对开平方。点(0,0)与(1,0)的距离平方为1 μm²，半径1.1 μm的平方为1.21 μm²，因此该对符合严格小于条件；点(1,0)与(0,1)的距离平方为2 μm²，则不符合。

“无序点对”表示点 i 与点 j 只计数一次，交换次序仍是同一对；一个点与自己也不参与统计。双循环用 `j` 从 `i+1` 开始实现这条规则。完整距离矩阵则关于对角线对称，因此保留主对角线上方的三角区域即可。分块时，局部行号要转换成全局点号，再用列号大于行号筛选。三种写法的数组形状不同，计数对象的身份必须一致。

独立检查使用四个可以手算的位置：(0,0)、(1,0)、(0,1)、(3,3)，单位为 μm，半径取 1.1 μm。前面三个点中，原点到另外两个点的距离都为 1 μm，而后两个点之间的距离约为 1.414 μm；远处的点与它们也不满足条件，因此答案是 2 对。程序先验证三种方法都得到 2，再处理较大的生成坐标。这个小算例沿用上一章的原则：在比较运行表现之前，先建立与实现方式无关的科学参照。

## 区分定位耗时与测量速度

性能分析器回答“时间主要花在哪些函数里”。示例中的 `analyze_frame` 先计算坐标中心，再统计近邻点对，最后计算平均径向距离。`cProfile` 记录这些函数的调用和时间，`pstats` 按累计时间整理结果。累计时间包含函数调用的其他函数，自身时间则只计算该函数内部的工作。阅读报告时，先看科学流程中哪个步骤占据主要部分，再决定深入哪一段代码。若大部分时间在读取大量小文件，优化一个很快的数组加法就不会明显改变等待时间。

比较几段实现的实际速度时，示例改用 `timeit.repeat`。输入坐标在计时前生成，三个方法都使用相同数组、半径和计数定义；每个配置分别执行七次，每次记录一次调用的耗时。性能分析会带来额外记录开销，因此不把开启分析器时的时间直接用作基准计时。这个区分与实验测量类似：一种仪器帮助定位过程中的环节，另一种测量安排用于比较统一条件下的结果。

![相同坐标与计数定义下的实际时间：左侧比较不同点数的中位数，右侧显示800点时七次独立计时。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0806220025aff3b22fe947c1.svg?v=0806220025af)

图 1相同坐标与计数定义下的实际时间：左侧比较不同点数的中位数，右侧显示800点时七次独立计时。

计时结果会受系统调度、缓存和当前资源使用影响，所以保留整组记录比只报最快一次更容易理解。这里用中位数描述典型单次时间，同时保存最小值和七次原始时间。中位数位于排序后的中间位置，少量较慢的运行对它影响较小；最小值则帮助观察外部干扰较少时的执行水平。图中用对数时间轴同时展示毫秒量级的差异，并在右侧直接画出每一次计时。它描述这份记录中的运行表现，读者重新执行程序时会获得自己环境中的新记录。

任务规模也应进入比较。点数从 100 增加到 800 时，需要考察的无序点对增长得更快，因为每个点都要与其他许多点比较。对不同规模重复同一测量，能够看出某种写法何时开始受内存分配或工作块大小影响。一个在小数组上很简洁的做法，扩大后可能产生很大的临时数据；反过来，分块在小任务中引入的循环开销，也可能抵消它节省内存带来的好处。

## 广播把循环移到哪里，产生了什么数组

坐标数组的形状是 `(N, 2)`。表达式 `points[:, None, :]` 在中间增加一个长度为 1 的轴，得到 `(N, 1, 2)`；`points[None, :, :]` 得到 `(1, N, 2)`。相减时，NumPy 根据广播规则对齐两个点编号轴，结果形状变成 `(N, N, 2)`。前两个轴表示点对，最后一个轴保存水平和竖直坐标差。这个形状与科学对象一一对应，也直接告诉我们需要保存多少个浮点数。

`np.einsum('ijk,ijk->ij', delta, delta)` 将同一坐标差与自身相乘，并沿最后一个坐标轴求和。这里 i、j 表示两个点的编号，k 表示坐标方向；结果只保留 i 和 j，因此形成 `(N, N)` 的距离平方矩阵。也可以用逐元素平方后求和表达同样的数学关系，不过那样可能额外产生一个平方数组。理解每个轴代表什么，比背住一个简短函数名更有用：看到输出形状时，就能判断是否沿正确的方向求和。

广播常常提高这类计算的速度，因为许多重复操作进入 NumPy 的底层数组循环，减少了 Python 逐个元素解释语句的开销。它并没有让两两比较的工作量消失。坐标差数组仍然需要容纳点对的信息，之后还要形成距离和布尔筛选。因此，评价广播写法时应同时问两个问题：底层执行是否减少了解释开销，中间数组是否适合当前数据规模。前一个问题对应计时，后一个问题对应下一节的内存分析。

## 分块：在保留计算定义的同时控制工作空间

完整广播同时保存坐标差和距离平方。两个方向的坐标差需要两个浮点数，每对点的距离平方再需要一个；本例使用 64 位浮点数，每个占 8 字节。因此这两个命名数组合计每对点占 24 字节，随 N 的平方增长。这个计算描述特定数组的存储量；程序还会创建布尔筛选、索引和其他对象，所以实际追踪到的峰值会更高。把公式估计与实际测量并排放置，可以看清数组形状解释了哪一部分内存。

$$
M_{\mathrm{full}}=24N^2\ \mathrm{bytes},\qquad M_{\mathrm{block}}=24BN\ \mathrm{bytes}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38162b15af75aabe566b89b0.svg) | 坐标差和距离平方这两个命名浮点数组的合计存储量，字节 |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 点数，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | 当前完整块的行数，假设不大于 N，无量纲计数 |

每对点保存两个坐标差和一个距离平方，共3个float64数，每个8字节，因此系数为3×8=24。N=800时，完整数组占24×800×800=15360000字节，除以1048576约为14.648 MiB；B=64时占1228800字节，约1.172 MiB。末块不足B行时按实际行数计算。布尔数组、索引与运行时分配另外计入追踪峰值。

![两个命名浮点数组的形状预测与独立tracemalloc峰值测量。MiB等于1048576字节；峰值还包含其他可追踪分配。](https://ml-biomat.com/static/tutorials/python-scientific/figures/5a39844b1ce29f33f31487a9.svg?v=5a39844b1ce2)

图 2两个命名浮点数组的形状预测与独立tracemalloc峰值测量。MiB等于1048576字节；峰值还包含其他可追踪分配。

分块把第一个点编号轴切成 B 行一组。当前块与全部 N 个点比较，得到 `(B, N, 2)` 的坐标差和 `(B, N)` 的距离平方；完成计数后释放这两个工作数组，再处理下一组。只要 B 小于 N，命名浮点数组的大小就随 B×N 增长，而不是一次保存 N×N。对于 N=800、B=64，两个数组合计 1228800 字节，完整广播则为 15360000 字节。每一块仍用全局编号去掉重复点对，因此最终计数保持 9106。

示例用 `tracemalloc` 另外执行一次计算，记录其能够追踪的峰值分配，并把结果标为“tracemalloc 峰值”。这与整个进程占用的物理内存有不同定义。内存追踪和速度计时分开进行，避免追踪开销混入七次基准记录。图中不同块大小对应不同的工作数组规模；块过小会增加循环次数，块过大则增加临时内存。选择块大小时，结合实际计时和内存预算寻找合适范围，比假定某个固定数字总是最快更实用。

## Amdahl 的问题：局部快十倍，整体会怎样

1967 年，Gene Amdahl 讨论大规模计算能力时，将程序中能够加速和保持不变的部分放在一起考虑。这个思路至今仍适合日常科研程序。一次完整分析除了邻居计数，还可能包含读取、清洗、拟合和写图；即使把其中一个函数大幅提速，其他部分仍然需要原先的时间。先测量各部分所占比例，才能估计哪项修改最值得做。

把原始总时间设为一个整体，其中比例 p 的工作获得 s 倍局部加速，其余部分时间保持不变。加速后的总时间由未改变部分与缩短后的目标部分相加得到，再用原时间除以新时间，就得到整体加速倍数。这个模型用于固定工作量，并假定修改没有改变其他环节的成本。下面的数值时间预算是明确的教学算例，与前面的实际计时记录分别标识。

$$
S=\frac{1}{(1-p)+p/s}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | 完整任务原时间除以新时间得到的整体加速倍数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | 原时间中目标部分所占比例，0到1，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 目标部分获得的局部加速倍数，本例不小于1，无量纲 |

把原总时间归一化为1，未改变部分仍需1−p，目标部分从p缩短到p/s，两者相加是新总时间。原时间1除以新时间即为S。p=0.8、s=10时，新时间比例为0.2+0.08=0.28，S≈3.571。对应100 s的教学流程，其中80 s缩短到8 s，另外20 s保持不变，得到28 s。模型采用固定工作量，其他部分成本保持不变。

![Amdahl时间分解的原创图：局部加速比例改变整体收益。右侧100 s到28 s为教学时间预算，与实际基准计时分别标识。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0ee927988b26069d88df74a6.svg?v=0ee927988b26)

图 3Amdahl时间分解的原创图：局部加速比例改变整体收益。右侧100 s到28 s为教学时间预算，与实际基准计时分别标识。

例如原流程用时 100 s，其中 80 s 属于目标计算，20 s 属于其他工作。目标计算加快十倍后变成 8 s，总时间为 28 s，整体加速约为 3.57 倍。继续让这 8 s 更短，仍会留下那 20 s。这个结果解释了为什么优化需要反复回到完整流程观察：当主要计算已经足够快，读取或输出可能成为下一项值得处理的工作。历史上的计算机体系结构问题，在一份 Python 分析脚本中仍然具有同样清楚的时间关系。

## 完整程序：保留计时记录、内存结果与数值检查

下面的程序生成固定随机种子的教学坐标，执行独立四点检查，再对 100、200、400 和 800 个点比较双循环、完整广播以及四种分块大小。每种配置都先检查计数一致，再保存七次时间和独立测量的峰值内存。科学任务的输入、计算和测量安排都在同一文件中，运行后得到 `benchmark.json`、`profile.txt`、`summary.json` 和三组科学图。计时文件保留每一次记录，便于进一步画分布或检查异常运行。

### 比较一致计算的耗时、内存与整体时间预算

默认进行七次重复计时，独立追踪内存；可用明确的已有记录生成另一种语言的图。

```
"""Compare equal neighbor-pair calculations using measured time and memory.

Coordinates are generated teaching data in a 10 um square. Timing samples are
local measurements; memory formulas describe named buffers rather than RSS.
"""
from pathlib import Path
import argparse
import cProfile
import io
import json
import platform
import pstats
import timeit
import tracemalloc
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def pair_count_loop(points, radius):
    count=0;limit=radius*radius
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            dx=points[i,0]-points[j,0];dy=points[i,1]-points[j,1]
            if dx*dx+dy*dy < limit:count+=1
    return count


def pair_count_full(points,radius):
    delta=points[:,None,:]-points[None,:,:]
    squared=np.einsum('ijk,ijk->ij',delta,delta)
    return int(np.count_nonzero(np.triu(squared < radius*radius,k=1)))


def pair_count_blocked(points,radius,block=64):
    count=0;n=len(points);columns=np.arange(n)[None,:]
    for start in range(0,n,block):
        stop=min(start+block,n)
        delta=points[start:stop,None,:]-points[None,:,:]
        squared=np.einsum('ijk,ijk->ij',delta,delta)
        rows=np.arange(start,stop)[:,None]
        count+=int(np.count_nonzero((squared < radius*radius)&(columns>rows)))
        del delta,squared
    return count


def measured_peak(function):
    tracemalloc.start()
    result=function()
    _,peak=tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result,int(peak)


def analyze_frame(points,radius):
    """A small scientific workload for function-level profiling."""
    center=points.mean(axis=0)
    centered=points-center
    pairs=pair_count_loop(centered,radius)
    radial=np.sqrt(np.einsum('ij,ij->i',centered,centered))
    return {'center':center.tolist(),'pairs':pairs,'mean_radius_um':float(radial.mean())}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--language',choices=['zh','en'],default='en')
    ap.add_argument('--timing-input',type=Path,help='Reuse an explicitly saved benchmark for an alternative-language figure')
    args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh';tr=lambda a,b:a if zh else b
    sizes=[100,200,400,800];blocks=[16,32,64,128];radius=1.0
    points=np.random.default_rng(2819).uniform(0,10,size=(max(sizes),2))
    hand=np.array([[0.,0.],[1.,0.],[0.,1.],[3.,3.]])
    assert pair_count_loop(hand,1.1)==pair_count_full(hand,1.1)==pair_count_blocked(hand,1.1,2)==2
    if args.timing_input:
        benchmark=json.loads(args.timing_input.read_text(encoding='utf8'))
        assert benchmark['seed']==2819 and benchmark['sizes']==sizes
        records=benchmark['records']
    else:
        records=[]
        for n in sizes:
            x=points[:n];reference=pair_count_loop(x,radius)
            methods=[('loop',0,lambda x=x:pair_count_loop(x,radius)),('full',n,lambda x=x:pair_count_full(x,radius))]
            methods += [('blocked',b,lambda x=x,b=b:pair_count_blocked(x,radius,b)) for b in blocks]
            for method,block,fn in methods:
                assert fn()==reference
                samples=timeit.repeat(fn,number=1,repeat=7)
                result,peak=measured_peak(fn)
                assert result==reference
                records.append({'n':n,'method':method,'block':block,'pairs':result,'seconds':samples,
                                'median_seconds':float(np.median(samples)),'minimum_seconds':min(samples),
                                'traced_peak_bytes':peak,'named_float_buffers_bytes':0 if method=='loop' else 24*n*min(block,n)})
        benchmark={'seed':2819,'sizes':sizes,'radius_um':radius,'python':platform.python_version(),
                   'numpy':np.__version__,'timing_definition':'seven independent timeit runs, one call per run',
                   'memory_definition':'separate tracemalloc peak; named buffers are float64 delta and squared distances',
                   'records':records}
    # Every run still independently checks the saved reference computations.
    for n in sizes:
        expected=next(r['pairs'] for r in records if r['n']==n)
        assert pair_count_full(points[:n],radius)==pair_count_blocked(points[:n],radius,64)==expected
    (out/'benchmark.json').write_text(json.dumps(benchmark,indent=2),encoding='utf8')
    profile=cProfile.Profile();profile_result=profile.runcall(analyze_frame,points[:400],radius)
    assert profile_result['pairs']==next(r['pairs'] for r in records if r['n']==400)
    stream=io.StringIO();pstats.Stats(profile,stream=stream).strip_dirs().sort_stats('cumulative').print_stats(8)
    (out/'profile.txt').write_text(stream.getvalue(),encoding='utf8')
    largest=[r for r in records if r['n']==800]
    summary={'hand_checked_pairs':2,'sizes':sizes,'pair_counts':{str(n):next(r['pairs'] for r in records if r['n']==n) for n in sizes},
             'all_methods_agree':True,'repeats':7,'largest_full_named_buffers_bytes':24*800*800,
             'largest_block64_named_buffers_bytes':24*800*64,'amdahl_p08_s10':1/(.2+.8/10)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    (out/'lab-data.json').write_text(json.dumps({'points':points.tolist(),'radius':radius,'records':records}),encoding='utf8')
    plt.rcParams.update({'font.family':available_plot_fonts(),'font.size':12,'svg.fonttype':'none','figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','axes.spines.top':False,'axes.spines.right':False})
    colors={'loop':'#b4482e','full':'#205b8c','blocked':'#2b7c73'}
    def save(fig,name):
        fig.savefig(out/f'{name}-{args.language}.svg',metadata={'Date':None});fig.savefig(out/f'{name}-{args.language}.png',dpi=150);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(12.4,5.3),layout='constrained',gridspec_kw={'width_ratios':[1.1,1]})
    for method in ['loop','full','blocked']:
        selected=[r for r in records if r['method']==method and (method!='blocked' or r['block']==64)]
        label=tr({'loop':'Python 双循环','full':'完整广播','blocked':'64 行分块'}[method],{'loop':'Python loops','full':'Full broadcast','blocked':'64-row blocks'}[method])
        axs[0].plot([r['n'] for r in selected],[r['median_seconds']*1000 for r in selected],'-o',color=colors[method],label=label)
        r=next(r for r in selected if r['n']==800);i=['loop','full','blocked'].index(method)
        axs[1].scatter(np.full(7,i)+np.linspace(-.1,.1,7),np.array(r['seconds'])*1000,color=colors[method],s=35)
        axs[1].hlines(r['median_seconds']*1000,i-.24,i+.24,color=colors[method],lw=3)
    axs[0].set(xscale='log',yscale='log',xlabel=tr('点数 N','Point count N'),ylabel=tr('单次中位时间 / ms','Median time per call / ms'))
    axs[0].set_xticks(sizes,[str(n) for n in sizes]);axs[0].xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axs[0].legend(frameon=False,fontsize=11);axs[0].set_title(tr('A  相同输入与计数定义','A  Equal inputs and counting definitions'),loc='left')
    axs[1].set_yscale('log');axs[1].set_xticks(range(3),tr(['双循环','完整广播','64 行分块'],['Loops','Full','Block 64']))
    axs[1].set_ylabel(tr('单次时间 / ms（7 次）','Time per call / ms (7 runs)'));axs[1].set_title(tr('B  N = 800 的实际重复测量','B  Actual repeated timings at N = 800'),loc='left')
    for ax in axs:ax.grid(axis='y',alpha=.2)
    save(fig,'measured-timings')
    fig,axs=plt.subplots(1,2,figsize=(12.4,5.2),layout='constrained');nn=np.array(sizes)
    axs[0].plot(nn,24*nn**2/2**20,'-o',color=colors['full'],label=tr('完整浮点数组','Full floating-point buffers'))
    axs[0].plot(nn,24*nn*64/2**20,'-o',color=colors['blocked'],label=tr('64 行浮点分块','64-row floating-point buffers'))
    axs[0].set(xlabel=tr('点数 N','Point count N'),ylabel=tr('命名浮点数组大小 / MiB','Named floating-point buffers / MiB'));axs[0].legend(frameon=False,fontsize=10)
    rows=[r for r in largest if r['method']=='full' or (r['method']=='blocked' and r['block'] in [16,64,128])]
    x=np.arange(len(rows));axs[1].bar(x-.17,[r['named_float_buffers_bytes']/2**20 for r in rows],width=.34,color='#a5bfce',label=tr('两个命名数组','Two named arrays'))
    axs[1].bar(x+.17,[r['traced_peak_bytes']/2**20 for r in rows],width=.34,color='#205b8c',label=tr('tracemalloc 峰值','tracemalloc peak'))
    axs[1].set_xticks(x,[('Full' if r['method']=='full' else f"B={r['block']}") for r in rows]);axs[1].set_ylabel(tr('追踪/计算内存 / MiB','Traced/calculated memory / MiB'));axs[1].legend(frameon=False,fontsize=10)
    axs[0].set_title(tr('A  保存形状决定增长规律','A  Stored shapes determine growth'),loc='left');axs[1].set_title(tr('B  N = 800：数组与实际峰值','B  N = 800: arrays and measured peaks'),loc='left')
    save(fig,'memory-growth')
    fig,axs=plt.subplots(1,2,figsize=(12.4,5.2),layout='constrained');accelerations=np.linspace(1,50,250)
    for p,color in [(.5,'#205b8c'),(.8,'#b4482e'),(.95,'#2b7c73')]:
        axs[0].plot(accelerations,1/((1-p)+p/accelerations),color=color,label=f'p = {p}')
    axs[0].set(xlabel=tr('目标部分的加速倍数 s','Speedup s of the selected part'),ylabel=tr('整体加速倍数 S','Overall speedup S'));axs[0].legend(frameon=False)
    axs[0].set_title(tr('A  Amdahl（1967）的时间分解思想','A  Amdahl (1967): decompose elapsed time'),loc='left',fontsize=13)
    axs[1].barh([1,0],[20,20],color='#9db5c3',label=tr('保持不变的部分','Unchanged work'))
    axs[1].barh([1,0],[80,8],left=[20,20],color='#b4482e',label=tr('加速的部分','Accelerated work'))
    axs[1].set_yticks([1,0],tr(['原流程','局部加速 10 倍'],['Original','Local 10× speedup']))
    axs[1].set_xlabel(tr('教学时间预算 / s','Illustrative time budget / s'));axs[1].legend(frameon=False,loc='lower right',fontsize=10)
    axs[1].text(29,0,'100 / 28 ≈ 3.57',va='center',fontsize=13);axs[1].set_title(tr('B  80% 工作加速后的整体变化','B  Accelerating 80% of the original work'),loc='left',fontsize=13)
    save(fig,'amdahl-budget')
    print(json.dumps(summary))


if __name__=='__main__':main()
```

默认运行会进行新的计时。`--timing-input` 可以读取明确指定的一份既有计时记录，以便为同一批测量生成另一种语言的图；这个模式仍会重新核对计数结果。页面中的中英图使用同一份基准记录，因此比较关系一致。Python 与 NumPy 版本同方法、数组规模、单位和测量定义一起保存，为后来比较不同运行记录提供一致的依据。

查看输出时，先确认四点例子的答案为 2，三个方法在各个规模下计数相同，再读时间与内存。800 点的计数为 9106，完整广播的两个命名浮点数组为 15360000 字节，64 行分块对应 1228800 字节。将这些可以由定义和形状核对的量与实际运行时间一起保存，能区分算法语义、内存规模和机器上的执行表现。三者互相联系，但各自回答不同问题。

## 在点对矩阵中看见分块，再选择下一步改进

交互把点数、块大小、当前处理块和实际计时记录放在同一工作区。改变点数后，二维位置图、点对计数和方法比较同步更新；改变块大小后，矩阵中当前处理的行带、命名数组大小与对应的计时分布一起变化。矩阵的横轴和纵轴都是点编号，主对角线上方对应只计一次的无序点对。移动当前块可以观察一个完整矩阵怎样被逐段覆盖，而科学计数定义始终保持不变。

### 把点对工作分成可见的行带

[Figure: 二维坐标与当前块的点](https://ml-biomat.com/tutorials/python-scientific/p28/#P28-points)

[Figure: 点对上三角矩阵与工作行带](https://ml-biomat.com/tutorials/python-scientific/p28/#P28-matrix)

[Figure: 同点数下六种配置的七次实际计时](https://ml-biomat.com/tutorials/python-scientific/p28/#P28-timing)

可以先在 800 点时比较 16、64 和 128 行分块，查看内存随工作块改变，计时却未必按同一比例变化。再切到 100 点，观察完整广播和分块之间的差距。这些结果提醒我们用目标任务规模来评估实现。若数据继续增大，两两枚举本身可能成为主要成本，此时可以研究网格划分、邻居表或树结构，让计算集中到可能接近的点；那属于改变搜索策略，需要重新设计适用条件与独立检查。

实际项目中的改进顺序可以沿着本章的证据展开：明确计算对象，保存能独立核对的测试，测量完整流程，选择占时较多的部分，再比较保持结果一致的实现。运行时间和内存都记录下来，后续换数据或改环境时继续沿用同样定义。这样，效率改进成为科学程序可解释的一部分，而不是一组脱离输入规模的速度数字。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P28.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Python timeit](https://docs.python.org/3.14/library/timeit.html)

   重复计时、输入准备与计时解释的官方基础。

   Python documentation: PSF terms.
2. [The Python Profilers](https://docs.python.org/3.14/library/profile.html)

   cProfile与pstats的调用次数、自身时间及累计时间。

   Python documentation: PSF terms.
3. [NumPy Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)

   广播轴规则及中间数组的内存影响。

   NumPy: BSD-3-Clause; official documentation.
4. [Python tracemalloc](https://docs.python.org/3.14/library/tracemalloc.html)

   追踪内存分配与峰值的定义。

   Python documentation: PSF terms.
5. [Gene M. Amdahl (1967), Validity of the single processor approach to achieving large scale computing capabilities](https://doi.org/10.1145/1465482.1465560)

   固定任务中加速部分与其余部分的历史问题；图和时间算例为本章原创。

   Scientific historical citation.
