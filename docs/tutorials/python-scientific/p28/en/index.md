# Finding and Improving Performance Bottlenecks

Source: https://ml-biomat.com/tutorials/python-scientific/p28/en/
Language: en

Use one neighbor-pair problem to connect measured time, array shapes, memory, and the effect of a local improvement on the whole task.

## Understand the work before making it faster

A program that finishes almost immediately for a hundred particle positions may require a noticeable wait for thousands. This change is common in microscopy tracking, structural analysis, and spatial-neighborhood calculations: identifying nearby objects requires many position comparisons. Improving performance begins by connecting the scientific question to the number of operations and the shapes of the data. Measure where time is spent, then choose an implementation suited to that work. The resulting improvement can explain both the present example and what happens when the dataset grows.

This chapter compares three implementations of one task: Python nested loops, full NumPy broadcasting, and a NumPy calculation processed in row blocks. The input is explicitly generated two-dimensional teaching data in a square of side 10 μm. The task counts unordered pairs separated by strictly less than 1 μm. All methods must return the same integer before their time and memory use are compared. In the saved record for 800 points, all methods find 9106 pairs. Median single-call times are approximately 130.47, 8.90, and 5.47 ms, with the last result using 64-row blocks. Seven actual timings remain visible alongside their representative values.

Time and memory should be considered together. Full broadcasting passes many scalar operations to NumPy but creates intermediate arrays that grow with the square of the point count. Blocking processes a subset of pairs at a time and reuses working space. These methods compare the same pairs with different organization. Understanding that relationship supports an informed choice among broadcasting, blocking, and later spatial-index methods, rather than treating fewer visible loops as the sole criterion for an implementation.

## Fix the counting definition before comparing implementations

Each point has horizontal and vertical coordinates in μm. Differences between two points form the perpendicular sides of a right triangle, so squared distance is the sum of their squares. Because the task asks whether distance is below a positive radius, comparing squared distance to squared radius preserves the ordering and avoids a square-root operation for every pair. Coordinates and radius must use the same length unit.

$$
d_{ij}^2=(x_i-x_j)^2+(y_i-y_j)^2,\qquad d_{ij}^2<r^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | Euclidean distance between points i and j, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/5e1d0f9befd63fa0c25bf752.svg) | horizontal and vertical coordinates of both points, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | positive neighborhood radius, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | dimensionless point indices; only pairs with j greater than i are counted |

Coordinate differences form the perpendicular sides of a right triangle. Squaring preserves the ordering of nonnegative distances and a positive radius, avoiding a square root for every pair. Points (0,0) and (1,0) have squared distance 1 μm², less than 1.1²=1.21 μm². Points (1,0) and (0,1) have squared distance 2 μm² and do not qualify.

An unordered pair is counted once: exchanging point i and point j leaves the same pair. A point is not paired with itself. Nested loops implement this by beginning j at i+1. A full distance matrix is symmetric about its diagonal, so selecting the upper triangle above that diagonal implements the same rule. With blocks, local row numbers must be translated back into global point indices before retaining columns greater than rows. Array shapes differ, while the identity of the counted objects stays fixed.

An independent check uses four positions that can be inspected by hand: (0,0), (1,0), (0,1), and (3,3), all in μm, with radius 1.1 μm. The origin is one micrometre from each of the next two points. Those two points are approximately 1.414 μm apart, and the distant point creates no qualifying pair. The answer is therefore two. The program verifies that all implementations return two before processing larger generated datasets. As in the preceding chapter, an implementation-independent scientific reference precedes the performance comparison.

## Distinguish locating expensive work from timing implementations

A profiler answers which functions account for elapsed work. The example's `analyze_frame` calculates a coordinate center, counts neighboring pairs, and calculates mean radial distance. `cProfile` records calls and timing, while `pstats` organizes the results by cumulative time. Cumulative time includes called functions; self time describes work inside the function itself. Read the report in terms of scientific operations before investigating individual lines. If most time is spent reading many small files, improving an already quick array addition will have little effect on the overall wait.

For implementation benchmarks, the example uses `timeit.repeat`. Coordinates are generated before timing, and each method receives the same array, radius, and counting definition. Every configuration runs seven times, recording one call per repetition. Profiling adds recording overhead, so profiled timings are kept separate from the benchmark. The distinction resembles using one measurement arrangement to locate stages in a process and another to compare outcomes under matched conditions.

![Measured timings with equal coordinates and counting definitions: medians across point counts and seven individual calls at 800 points.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8573f4176c6b7d1e27cffefb.svg?v=8573f4176c6b)

Figure 1Measured timings with equal coordinates and counting definitions: medians across point counts and seven individual calls at 800 points.

Scheduling, cache state, and current resource use can affect timings. Retaining the full collection makes a representative value easier to interpret. We report the median while also saving the minimum and all seven measurements. The median occupies the middle of the sorted values and is less affected by a few slow runs. The minimum provides a view of execution with less external interruption. A logarithmic time axis displays the range of durations clearly, while the second panel shows every repetition. The graph describes this saved record; rerunning the program produces a new record for the current environment.

Include workload size in the comparison. Increasing the point count from 100 to 800 increases the number of unordered pairs much more rapidly because every point is compared with many others. Repeating the same measurement across sizes reveals when allocation or block size begins to affect the result. A concise small-array expression may create substantial temporary data at larger sizes. Conversely, loop overhead introduced by blocking may outweigh its memory benefit on a small task.

## Follow broadcasting through the array shapes

The coordinate array has shape `(N, 2)`. `points[:, None, :]` adds a length-one middle axis, producing `(N, 1, 2)`; `points[None, :, :]` produces `(1, N, 2)`. Subtraction broadcasts across the two point-index axes and returns `(N, N, 2)`. Its first two axes identify a pair and its last axis contains horizontal and vertical differences. The shape corresponds directly to the scientific object and immediately tells us how many floating-point values must be stored.

`np.einsum('ijk,ijk->ij', delta, delta)` multiplies each coordinate difference by itself and sums over the last coordinate axis. Here i and j identify points and k identifies coordinate direction. Retaining i and j gives an `(N, N)` squared-distance matrix. Elementwise squaring followed by summation expresses the same mathematics, although it can create an additional temporary squared array. Understanding the axes makes it possible to inspect a result's shape and determine whether reduction occurred over the intended dimension.

Broadcasting often improves this calculation because repeated operations move into NumPy's lower-level array loops, reducing the overhead of interpreting Python statements for each element. Pairwise work still exists. The difference array stores information for point pairs, followed by distance and Boolean-selection arrays. Two questions therefore belong in an assessment: does lower-level execution reduce interpreter overhead, and do intermediate arrays fit the intended scale? Timing addresses the first, while memory analysis addresses the second.

## Control working space with blocks

Full broadcasting retains coordinate differences and squared distances. Each pair needs two floating-point differences and one squared distance. With eight bytes per float64 value, the two named arrays use twenty-four bytes per pair and grow quadratically with N. This calculation describes particular arrays. Boolean selections, indices, and other objects add to the measured peak. Placing a storage formula next to an actual memory measurement shows which part of the allocation is explained by array shapes.

$$
M_{\mathrm{full}}=24N^2\ \mathrm{bytes},\qquad M_{\mathrm{block}}=24BN\ \mathrm{bytes}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38162b15af75aabe566b89b0.svg) | combined storage of the named difference and squared-distance floating-point arrays, bytes |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | number of points, dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | row count of a full working block, no larger than N, dimensionless count |

A pair stores two coordinate differences and one squared distance: three float64 values at eight bytes each, giving 24 bytes. N=800 uses 15360000 bytes, approximately 14.648 MiB after division by 1048576. B=64 uses 1228800 bytes, approximately 1.172 MiB. A partial final block uses its actual row count. Boolean arrays, indices, and runtime allocations contribute separately to the traced peak.

![Shape-based storage for the two named floating-point arrays and independent tracemalloc peaks. One MiB is 1048576 bytes; peaks also include other traced allocations.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ebd9dd256f20ba6db476e799.svg?v=ebd9dd256f20)

Figure 2Shape-based storage for the two named floating-point arrays and independent tracemalloc peaks. One MiB is 1048576 bytes; peaks also include other traced allocations.

Blocking divides the first point-index axis into groups of B rows. Comparing one group with all N points creates differences of shape `(B, N, 2)` and squared distances of shape `(B, N)`. After counting qualifying pairs, the program releases those arrays and processes the next block. When B is smaller than N, named floating-point storage grows with B times N rather than allocating N times N at once. For N=800 and B=64, those arrays total 1228800 bytes, compared with 15360000 bytes for the full calculation. Global indices still remove duplicate pairs, so the final count remains 9106.

The example separately runs each calculation under `tracemalloc`, labeling its result as a traced peak allocation. This quantity has a different definition from a process's total resident memory. Memory tracking runs separately from the seven timing repetitions so its overhead does not enter the benchmark. Different block sizes produce different working-array sizes. Small blocks require more loop iterations, while large blocks create more temporary storage. Combining measurements with a memory budget helps identify a useful range for the intended workload.

## Amdahl's question: what does a local tenfold improvement change?

In 1967, Gene Amdahl discussed large-scale computing capabilities by considering accelerated and unchanged portions of a program together. The reasoning remains useful for scientific scripts. An analysis can include reading, cleaning, fitting, and plotting in addition to neighbor counting. Improving one function leaves other work to be completed. Measuring their relative contributions helps identify which change will have the largest effect on the complete task.

Let a fraction p of the original runtime be work that becomes s times faster. The remaining fraction keeps its original duration. Adding the unchanged time to the shortened target time gives the new total; dividing the old total by that value gives overall speedup. This model describes a fixed workload and assumes the modification does not alter the cost of other stages. The following time budget is an explicitly illustrative calculation, identified separately from the actual benchmark measurements.

$$
S=\frac{1}{(1-p)+p/s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | overall speedup, original total time divided by new total time, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | fraction of original runtime spent in the target part, between zero and one |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | speedup of the target part, at least one here, dimensionless |

Normalize original total time to one. Unchanged work still needs 1−p, and target work falls from p to p/s. Their sum is the new total, so dividing one by it gives S. With p=0.8 and s=10, the new fraction is 0.2+0.08=0.28 and S≈3.571. An illustrative 100-second task becomes 20+8=28 seconds. Workload and the cost of other stages remain fixed.

![Original illustration of Amdahl time decomposition. The 100-to-28-second budget is a teaching calculation, identified separately from measured benchmark timings.](https://ml-biomat.com/static/tutorials/python-scientific/figures/642fc54d086a81c979b98f6c.svg?v=642fc54d086a)

Figure 3Original illustration of Amdahl time decomposition. The 100-to-28-second budget is a teaching calculation, identified separately from measured benchmark timings.

For example, a hundred-second workflow might contain eighty seconds of target computation and twenty seconds of other work. Making the target ten times faster reduces it to eight seconds, giving a twenty-eight-second total and an overall speedup of approximately 3.57. Improving that eight-second portion further still leaves the twenty-second remainder. Performance work therefore returns repeatedly to the complete workflow: once one calculation is fast enough, reading or output may become the next useful target. The historical architectural question retains the same clear time relationship inside a Python analysis.

## Keep timing records, memory measurements, and numerical checks

The complete program generates teaching coordinates with a fixed random seed, performs the independent four-point check, and compares nested loops, full broadcasting, and four block sizes at 100, 200, 400, and 800 points. Each configuration first checks count agreement, then saves seven timings and a separately measured memory peak. Inputs, scientific calculations, and measurement arrangements are visible in one file. Outputs include `benchmark.json`, `profile.txt`, `summary.json`, and three scientific figures. The benchmark retains individual repetitions for later distribution plots or inspection of unusual runs.

### Compare equal computations using timing, memory, and an overall time budget

Run seven timing repetitions and independent memory tracking; an explicitly supplied prior record can generate another-language figures.

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

The default run performs a new benchmark. `--timing-input` accepts an explicitly identified previous record when another-language figure is needed for the same measurements; that mode still rechecks pair counts. The Chinese and English figures on this page use one benchmark record, preserving the comparison across languages. Python and NumPy versions accompany method names, input sizes, units, and measurement definitions so that later results can be compared on a consistent basis.

Inspect the outputs in order: confirm the four-point answer of two, confirm agreement across methods for each size, then read time and memory. The 800-point count is 9106. The full method's two named floating-point arrays occupy 15360000 bytes, while 64-row blocks use 1228800 bytes. Retaining quantities derivable from definitions and shapes alongside timings separates algorithmic meaning, storage scale, and observed execution behavior. Each contributes a different part of the performance explanation.

## See the blocks inside the pair matrix

The interactive workspace connects point count, block size, the current block, and measured timing records. Changing the number of points updates positions, pair count, and method comparisons. Changing block size updates the highlighted matrix rows, named-buffer size, and corresponding timing distribution. Both matrix axes are point indices; the upper triangle represents unordered pairs counted once. Move the current block to inspect how a matrix is covered progressively while the counting definition stays fixed.

### Divide pairwise work into visible row blocks

[Figure: Coordinates and points in the current row block](https://ml-biomat.com/tutorials/python-scientific/p28/en/#P28-points)

[Figure: Upper-triangular pair matrix and working row band](https://ml-biomat.com/tutorials/python-scientific/p28/en/#P28-matrix)

[Figure: Seven actual timings for six configurations at the selected point count](https://ml-biomat.com/tutorials/python-scientific/p28/en/#P28-timing)

At 800 points, compare blocks of 16, 64, and 128 rows. Storage changes with block size, while timings need not follow the same proportion. Switch to 100 points and examine the difference between full broadcasting and blocking. The intended workload size belongs in an implementation decision. If data grow much further, enumerating all pairs may itself become the main cost. Grid partitions, neighbor lists, or tree structures can concentrate work on potentially nearby points; changing the search strategy calls for new applicability conditions and independent checks.

A practical improvement follows the evidence developed here: define the objects being counted, preserve independent tests, measure the full workflow, select an expensive component, and compare implementations that retain the same result. Record both time and memory, then reuse the definitions when inputs or computing environments change. Performance becomes an explainable property of a scientific program, connected to its actual workload.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P28.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Python timeit](https://docs.python.org/3.14/library/timeit.html)

   Official foundation for repeated timing, setup, and interpretation.

   Python documentation: PSF terms.
2. [The Python Profilers](https://docs.python.org/3.14/library/profile.html)

   cProfile and pstats call counts, self time, and cumulative time.

   Python documentation: PSF terms.
3. [NumPy Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)

   Broadcasting-axis rules and memory implications.

   NumPy: BSD-3-Clause; official documentation.
4. [Python tracemalloc](https://docs.python.org/3.14/library/tracemalloc.html)

   Definitions of traced allocations and peaks.

   Python documentation: PSF terms.
5. [Gene M. Amdahl (1967), Validity of the single processor approach to achieving large scale computing capabilities](https://doi.org/10.1145/1465482.1465560)

   Historical question of accelerated and unchanged portions of fixed work; the diagrams and numerical budget are original.

   Scientific historical citation.
