# Turning Repeated Work into Functions

Source: https://ml-biomat.com/tutorials/python-scientific/p04/en/
Language: en

Trace one mass record through parameters, branches, loops, and returned results.

## Apply one calculation to every specimen

Once six experimental records are organized, we want to calculate liquid uptake for each specimen while retaining the record with a missing weighing. One approach is to copy the same subtraction and division six times and edit each pair of variable names. With sixty specimens, a small change in a checking rule becomes a change in many places. This chapter places the calculation for one specimen inside a function and uses a loop to send records through it. The result is an analysis that retains each record's status, calculated value, and contribution to the running summary.

We continue with six constructed records. Dry and wet masses are 1.20 and 4.80 g for A01, 1.00 and 3.40 g for A02, 0.80 and 2.80 g for A03, 1.20 and 3.60 g for B01, and 0.80 and 2.32 g for B03. B02 has a dry mass of 1.00 g and no wet mass. Container contributions have been removed. Dry material is treated as a fixed mass reference, and the increase is counted as absorbed liquid, including dissolved components where present. The order in which the program processes records is a computational order, not the time course of one absorbing specimen.

Think of a function as a calculation sheet with named input and output fields. The input fields say “dry mass, g” and “wet mass, g”; the sheet specifies checks and arithmetic; the output says “liquid mass per dry mass, g/g.” A different specimen supplies different inputs to the same rules. Preparing the sheet and actually using it are separate actions. Python's distinction between defining a function and calling a function captures exactly that separation.

## Definition, call, and return are different events

The short example below begins with the arithmetic alone. The keyword `def` introduces a function definition, and `uptake_simple` is the name we choose. Inside the parentheses, `dry_g` and `wet_g` are parameters: local names that will receive objects when the function is called. The colon introduces the function body. The indented line belongs to that body, conventionally using four spaces per indentation level. In Python, indentation determines which statements execute together; it is part of the program's meaning.

### Define first, then supply two masses

Prints 3.0 and 2.4, both interpreted as g/g.

```
def uptake_simple(dry_g, wet_g):
    return (wet_g - dry_g) / dry_g

q = uptake_simple(1.2, 4.8)
print(q)
print(uptake_simple(wet_g=3.4, dry_g=1.0))
```

Executing the definition associates a function object with its name without yet substituting specimen masses. Calling `uptake_simple(1.2, 4.8)` supplies 1.2 to the first parameter and 4.8 to the second. These particular supplied objects are the arguments. The body calculates a result, and `return` sends it back to the call site, where assignment stores 3.0 in `q`. Alternatively, `uptake_simple(wet_g=4.8, dry_g=1.2)` identifies parameters explicitly, so their written order can change. Named arguments make the meaning of two similar-looking measurements visible at the call site.

A return value and printed output serve different purposes. A returned number can enter an average, a plot, or a saved record. Printing displays text for a reader. If the function's final line uses `print(...)` without returning the calculated quantity, the screen may still show 3.0, but the value assigned to `q` will be `None`. Arithmetic with that value then fails. The complete example keeps these responsibilities separate: calculation functions return useful objects, and the surrounding program decides when to display or save them.

Parameters are local names for a particular call. The first call can use 1.2 as `dry_g` and the next can use 1.0 without manually clearing the previous call's names. An identically named variable outside the function does not automatically become the input. Passing dependencies through parameters makes them visible. Mutable objects require another distinction: a passed dictionary may also be referenced outside the function, so changing its contents changes that shared object. Our analysis makes a shallow copy of each record before adding results. Because these fields contain numbers, strings, and `None`, this is sufficient for adding top-level fields without modifying the original record.

The suffix `_g` keeps the unit convention visible, but it does not perform conversion. If a dry mass measured in milligrams is passed as 1200 while wet mass in grams is passed as 4.8, Python receives two numbers, not two unit-aware measurements. The reading or validation stage must identify the inconsistency. Converting both masses to milligrams preserves the ratio, but field names and documentation should still describe the actual units. The triple-quoted text at the beginning of a function is its documentation string, available through `help(uptake)`. It records quantities, units, returned objects, and missing-data behavior alongside the calculation.

## Reusable routines addressed repeated scientific work

The idea of reusable calculations predates Python. The Cambridge Computer Laboratory's institutional history records work on closed subroutines and a subroutine library for EDSAC in 1948–49, including Wheeler's contributions. By 1950, library development included Gill's Runge–Kutta program and Wheeler's floating-point routine. Wilkes, Wheeler, and Gill published their programming book in 1951. For our purposes, the useful connection is the organization of a repeated calculation into a callable unit that receives data and returns control to the surrounding computation.

Suppose a scientific calculation needs the same type of mathematical operation at several places. Writing the instructions again at every place creates repeated maintenance. Jumping to a shared routine instead requires a convention for supplying inputs and a way to return to the appropriate point. Those conventions make reuse possible. Python manages the lower-level details, while arguments and `return` provide a readable interface. The illustration uses this chapter's uptake calculation to explain the relationship; it is a conceptual diagram rather than a reconstruction of EDSAC instructions.

![The historical problem of reusable subroutines explains modern functions. Two calls supply their own masses to one definition and return to their call sites. Original conceptual illustration.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e99109c93e2e748342d03769.svg?v=e99109c93e2e)

Figure 1The historical problem of reusable subroutines explains modern functions. Two calls supply their own masses to one definition and return to their call sites. Original conceptual illustration.

In scientific code, reuse also improves explanation. A call such as `uptake(dry_g=1.2, wet_g=4.8)` tells the reader what is being calculated, while the function body provides the definition and checking rules. That benefit weakens if one enormous function reads files, converts units, filters records, computes every statistic, and draws every figure. A useful division gives the single-specimen function responsibility for the quantity, the batch function responsibility for records and status, and plotting responsibility for presentation. Clearly defined values connect the layers.

## Check the calculation's conditions at its entrance

Dry mass is the denominator of the uptake ratio. The complete function first requires a finite, positive dry mass and then asks whether a wet mass has been supplied. Finite excludes positive or negative infinity and the numerical marker `NaN`, meaning “not a number.” The standard-library function `math.isfinite` performs this check. `None` means that this record has no wet measurement. A non-finite numeric value and an absent field value have different meanings even though neither supplies a usable mass for this calculation.

$$
q=\frac{m_w-m_d}{m_d},\qquad m_d>0,\quad m_w\ge m_d
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Liquid uptake per dry mass, g/g and dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | Net wet mass, g; absence produces None |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | Net dry mass, g; finite and positive |
| ![Formula](https://ml-biomat.com/static/agent-math/16df88788b1d832b83b1bd9b.svg) | Subtract to obtain retained liquid mass, then divide by dry mass |
| ![Formula](https://ml-biomat.com/static/agent-math/604114aa9f8783cbc02b7d55.svg) | Greater than, and greater than or equal to; input conditions for this mass account |

With fixed dry material, A01 retains 4.80−1.20=3.60 g of liquid, giving 3.60/1.20=3.00 g/g. Doubling both masses gives (9.60−2.40)/2.40=3.00 g/g again.

An `if` statement evaluates a condition and runs its indented statements when the condition is true. The comparison `dry_g <= 0` asks whether dry mass is zero or negative. The operator `not` reverses truth, and `or` combines conditions so that either can trigger the branch. Checking dry mass before testing whether wet mass is missing means that zero dry mass is reported even when no wet mass exists. This ordering is an explicit part of the record-handling rule, applied consistently to every specimen.

When wet mass is `None`, `return None` ends the call immediately; subsequent subtraction is never reached. When a supplied wet mass is smaller than dry mass, the function raises `ValueError` with a specific message. Our mass account assumes retained dry material, so a negative increase prompts examination of identity, weighing, and material loss. A dissolving or degrading specimen needs an account that includes solid loss as well as incoming liquid. Taking an absolute value would conceal this change of meaning rather than define the appropriate calculation.

The complete example places the specimen calculation inside `try` and handles its expected `ValueError` with `except ValueError`. The result retains the identifier, status, and reason, allowing other independent records to be processed. Missing measurements and invalid mass accounting remain separate states, named `missing` and `invalid`. A misspelled field can produce `KeyError`, which this handler does not suppress. It continues to identify a structural problem in the program or input. Handling an anticipated measurement condition is different from turning every possible programming failure into an empty result.

## One iteration handles one current record

Read `for record in records:` as “take each record in turn and refer to the current one as record.” The first iteration uses A01, the next A02, and the process continues until the list is exhausted. Each iteration copies the current record, calls the function, adds result fields, and appends the new record to a result list. The statement `results = []` occurs once before the loop. Putting it inside the loop would create a fresh list every time, discarding previously accumulated results. Indentation often explains a surprising final output more quickly than examining the output alone.

The example uses `enumerate(records, start=1)` to obtain both a step number and the record itself. Human-readable steps start at one; list positions still start at zero. These conventions serve different purposes and do not conflict. When a calculation needs records directly, iterating over records avoids unnecessary positional lookups. `range(6)`, by contrast, provides the six integers zero through five and is useful when integer steps are genuinely needed. Its stop value is excluded. Choosing a loop begins with identifying whether the current operation needs an object, a position, or both.

![Stepwise execution for six constructed records. The missing fifth weighing remains a record but adds no valid value. The horizontal axis is a computation step, and values come from the complete script.](https://ml-biomat.com/static/tutorials/python-scientific/figures/7b062320506272579c622787.svg?v=7b0623205062)

Figure 2Stepwise execution for six constructed records. The missing fifth weighing remains a record but adds no valid value. The horizontal axis is a computation step, and values come from the complete script.

The fifth record, B02, returns `None`. It remains in the results, so the processed-record count increases from four to five. The valid-value count stays at four, and the running mean stays at 2.475 g/g. After B03, five valid values sum to 11.8 g/g and have a mean of 2.36 g/g. The horizontal axis is the number of records processed, not elapsed experimental time. Pooling the two treatment groups here makes the execution state easy to follow. A scientific comparison of treatments would retain the separate group summaries developed in the preceding chapter.

$$
\bar q_k=\frac{1}{n_k}\sum_{i\in V_k}q_i\quad(n_k>0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Number of records processed, not experimental time; dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/ec1501006f8037f1c7ffd945.svg) | Set of specimen indices with valid numerical results among the first k records |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Specimen index in the set, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | Number of available values in V_k, dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | Liquid uptake for specimen i, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/f5666e2316365712884fc0f6.svg) | Running equal-specimen mean over available values, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/99c8b956831093e4e1e9a7c9.svg) | Add the values; include only indices in the valid set |

At step four, (3.0+2.4+2.5+2.0)/4=2.475 g/g. Missing B02 changes neither set nor count at step five. Adding 1.9 at step six gives 11.8/5=2.36 g/g. When n_k is zero, the mean is None.

After every iteration, two useful statements should remain true: the result-list length equals the number of processed records, and the available-value list contains exactly the numerical results encountered so far. Such a relationship is called a loop invariant. Although the current input changes, the relationship should hold at each step. If the fifth iteration suddenly has five valid values, inspect the missing-data branch. If the final result list contains one record, inspect where the list is initialized. An execution trace connects a local operation with the accumulating state.

The position of `return` matters just as much. Placing `return results` inside the loop ends the function after its first iteration, so the remaining five records are never processed. After the loop, it means “return the collection once every record has been handled.” Two other control statements operate at a different level: `continue` skips the rest of the current iteration, and `break` ends the current loop. Neither necessarily ends the whole function. This example needs every record to enter both results and trace, so the explicit sequential structure makes that requirement visible. Choose control flow by identifying which level of work should finish.

## Check answers and relationships

Start with a small example that can be calculated independently: dry mass 1.20 g and wet mass 4.80 g should return 3.00 g/g. Next examine boundaries. Equal dry and wet masses should return numerical zero, while an absent wet mass should return `None`. Zero contributes to the valid count and mean; absence does not. Then test invalid inputs, such as zero dry mass and a wet mass below dry mass. These should enter the explicit checking branch instead of producing an uptake value.

A stronger check examines a relationship between several inputs. Multiplying both masses by two multiplies the mass difference and denominator by two, leaving their ratio unchanged. Thus 1.20 and 4.80 g should give the same uptake as 2.40 and 9.60 g. The left panel evaluates a grid of dry and wet masses using the same function. Color represents output, and white contours connect combinations with equal uptake. The right panel follows common scaling of both masses and produces a horizontal line. An incorrect normalization denominator becomes easier to detect when both numerical examples and structural relationships are examined.

Read the color map through a point that is easy to calculate. Dry mass 1.00 g and wet mass 4.00 g give a difference of 3.00 g and therefore lie on the contour labeled 3. The pair 0.80 and 3.20 g lies on the same contour. Holding dry mass at 1.00 g and reducing wet mass to 3.00 g instead gives uptake 2. The colors encode the function's output; they do not encode measurement probability or the number of observed specimens. Each cell corresponds to defined inputs, while the blank region retains combinations outside this particular mass account.

![The same uptake function applied to dry–wet mass combinations. Contours join equal outputs; blank space marks wet mass below dry mass. Scaling both masses together leaves the ratio unchanged.](https://ml-biomat.com/static/tutorials/python-scientific/figures/165fbf50f4835c5a72adc065.svg?v=165fbf50f483)

Figure 3The same uptake function applied to dry–wet mass combinations. Contours join equal outputs; blank space marks wet mass below dry mass. Scaling both masses together leaves the ratio unchanged.

The complete script records several expectations with `assert`. A failed condition produces an assertion error and directs attention to the implementation. Floating-point ratios use `math.isclose` so that last-place rounding does not masquerade as a changed formula. Zero, `None`, and the structure of a returned dictionary can be compared according to their own meanings. Input validation remains explicit `if` and `raise` code: Python can remove assertions in optimized execution, so assertions serve development checks while the function itself enforces its input rules.

The empty case deserves a deliberate answer. Calling `summarize([])` returns a valid count of zero and a mean of `None`. No observations are available to define an average. Returning zero would instead suggest that a zero mean had been measured. The summary function therefore returns a dictionary containing both count and mean. Downstream display can distinguish no result from a result that happens to be zero. A useful interface retains the smallest amount of context needed to interpret its number.

## Connect the functions into a complete analysis

The program below defines `uptake`, `summarize`, and `analyze`, then uses `main` to arrange input, checks, figures, and output files. The call `results, trace = analyze(records)` receives two returned objects through unpacking. The first contains specimen results; the second contains the execution trace. Their separation allows the same results to support a report while the trace explains how they accumulated, without reconstructing state from printed messages.

### Complete functions, batch analysis, and figures

Calculations use the Python standard library; Matplotlib generates the figures.

```
"""Trace reusable calculations over a small set of teaching specimens."""
from pathlib import Path
import argparse
import json
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def uptake(dry_g, wet_g):
    """Return retained-liquid mass per dry mass, or None if wet mass is absent.

    Masses are net specimen masses in grams. This example assumes no loss
    of dry material. Invalid mass accounting raises ValueError.
    """
    if not math.isfinite(dry_g) or dry_g <= 0:
        raise ValueError("dry_g must be finite and positive")
    if wet_g is None:
        return None
    if not math.isfinite(wet_g) or wet_g < dry_g:
        raise ValueError("wet_g must be finite and at least dry_g")
    return (wet_g - dry_g) / dry_g


def summarize(values):
    """Return the count and equally weighted mean of available values."""
    valid = [value for value in values if value is not None]
    return {"valid_count": len(valid),
            "mean": math.fsum(valid) / len(valid) if valid else None}


def analyze(records):
    """Return new result records and an execution trace, preserving inputs."""
    results, trace, available = [], [], []
    for step, record in enumerate(records, start=1):
        item = record.copy()
        try:
            value = uptake(record["dry_g"], record["wet_g"])
            status = "missing" if value is None else "valid"
            reason = "wet mass absent" if value is None else "calculated"
        except ValueError as error:
            value, status, reason = None, "invalid", str(error)
        item.update(uptake_g_per_g=value, status=status, reason=reason)
        results.append(item)
        if value is not None:
            available.append(value)
        trace.append({"step": step, "id": record["id"], "status": status,
                      "returned": value, "valid_count": len(available),
                      "sum": math.fsum(available),
                      "mean": summarize(available)["mean"]})
    return results, trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(a, b): return a if zh else b
    records = [
        {"id":"A01", "dry_g":1.2, "wet_g":4.8},
        {"id":"A02", "dry_g":1.0, "wet_g":3.4},
        {"id":"A03", "dry_g":0.8, "wet_g":2.8},
        {"id":"B01", "dry_g":1.2, "wet_g":3.6},
        {"id":"B02", "dry_g":1.0, "wet_g":None},
        {"id":"B03", "dry_g":0.8, "wet_g":2.32},
    ]
    results, trace = analyze(records)
    assert math.isclose(uptake(1.2, 4.8), 3.0)
    assert math.isclose(uptake(2.4, 9.6), uptake(1.2, 4.8))
    assert uptake(1.0, 1.0) == 0.0
    assert uptake(1.0, None) is None
    assert summarize([]) == {"valid_count": 0, "mean": None}
    invalid_examples = []
    for dry, wet in [(0.0, 1.0), (1.0, 0.5), (float("nan"), 2.0)]:
        try:
            uptake(dry, wet)
        except ValueError as error:
            invalid_examples.append({"reason": str(error)})
        else:
            raise AssertionError("An invalid input was accepted")
    assert "status" not in records[0]
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ["Noto Sans CJK SC", "Microsoft YaHei", "DejaVu Sans"] if f in fonts), "DejaVu Sans")
    plt.rcParams.update({"font.family":[family,"DejaVu Sans"] if zh else ["DejaVu Sans","Arial"],"font.size":12,"axes.titlesize":15,"axes.titleweight":"bold","svg.fonttype":"none","figure.facecolor":"#fbfaf6","axes.facecolor":"#fbfaf6","text.color":"#172b36","axes.labelcolor":"#172b36","axes.spines.top":False,"axes.spines.right":False})
    ink, blue, red, green = "#172b36", "#28648a", "#b85336", "#467a62"
    def save(fig, name):
        fig.savefig(args.output/f"{name}-{args.language}.svg", bbox_inches="tight")
        fig.savefig(args.output/f"{name}-{args.language}.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig = plt.figure(figsize=(12,8), layout="constrained")
    gs = fig.add_gridspec(2,1,height_ratios=[1.4,1])
    ax = fig.add_subplot(gs[0]);ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.15,6.6,tr("a  每次循环保留输入、分支与返回值","a  Each iteration retains inputs, branch, and return"),fontsize=17,weight="bold")
    headers=[tr("步骤","Step"),"ID",tr("干 / 湿质量 (g)","Dry / wet mass (g)"),tr("分支","Branch"),tr("返回 (g/g)","Return (g/g)"),tr("有效计数","Valid count")]
    xs=[.2,1.2,2.5,6.2,8.4,10.5]
    for x,h in zip(xs,headers):ax.text(x,5.8,h,fontsize=12,weight="bold")
    for i,(r,t) in enumerate(zip(records,trace)):
        y=5.1-i*.75;color=red if t["status"]=="missing" else blue
        ax.add_patch(Rectangle((.1,y-.2),11.7,.65,color=color,alpha=.065))
        wet="None" if r['wet_g'] is None else f"{r['wet_g']:.2f}"
        vals=[str(i+1),r['id'],f"{r['dry_g']:.2f} / {wet}",tr("缺失","Missing") if t['status']=='missing' else tr("计算","Calculate"),'None' if t['returned'] is None else f"{t['returned']:.2f}",str(t['valid_count'])]
        for x,v in zip(xs,vals):ax.text(x,y,v,color=color,fontsize=13)
    ax = fig.add_subplot(gs[1]);steps=[t['step'] for t in trace]
    ax.plot(steps,[t['mean'] for t in trace],color=blue,marker='o',lw=2,label=tr('累计样品均值','Running specimen mean'))
    ax.axvspan(4.7,5.3,color=red,alpha=.1)
    ax.annotate(tr('第5条缺失：计数与均值保持','Record 5 missing: count and mean unchanged'),(5,trace[4]['mean']),xytext=(3.0,3.15),arrowprops={'arrowstyle':'->','color':red},fontsize=12,color=red)
    ax.set(xticks=steps,xlabel=tr('已处理记录数','Records processed'),ylabel=tr('累计均值 / g·g⁻¹','Running mean / g·g⁻¹'),ylim=(2.2,3.35),title=tr('b  跟踪计算顺序；不是随时间的吸液曲线','b  A computational trace, not an uptake time curve'));ax.grid(alpha=.15)
    save(fig,'execution-trace')

    fig=plt.figure(figsize=(12,6.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.2,1])
    ax=fig.add_subplot(gs[0]);dry_values=[.5+i*.025 for i in range(61)];wet_values=[.5+i*.05 for i in range(111)]
    field=[[uptake(d,w) if w>=d else math.nan for d in dry_values] for w in wet_values]
    mesh=ax.pcolormesh(dry_values,wet_values,field,shading='auto',cmap='cividis',vmin=0,vmax=11)
    contours=ax.contour(dry_values,wet_values,field,levels=[0.5,1,2,3,5,8],colors='white',linewidths=.8)
    ax.clabel(contours,fmt='%g',fontsize=11);ax.plot([.5,2],[.5,2],color=red,lw=2)
    ax.text(1.1,.75,tr('检查质量账本','Check mass accounting'),color=red,fontsize=11,rotation=25)
    ax.scatter([1.2, .8],[4.8,3.2],s=80,facecolors='none',edgecolors='white',linewidths=2)
    ax.set(xlabel=tr('干质量 / g','Dry mass / g'),ylabel=tr('湿质量 / g','Wet mass / g'),title=tr('a  函数的输入平面与输出','a  An input plane and its output'))
    fig.colorbar(mesh,ax=ax,label=tr('吸液量 / g·g⁻¹','Uptake / g·g⁻¹'),shrink=.8)
    ax=fig.add_subplot(gs[1]);scales=[.5+i*.05 for i in range(31)]
    ax.plot(scales,[uptake(1.2*k,4.8*k) for k in scales],color=blue,lw=2)
    ax.scatter([.5,1,2],[3,3,3],s=65,color=blue)
    ax.set(xlabel=tr('同时缩放两种质量的倍数','Factor applied to both masses'),ylabel=tr('吸液量 / g·g⁻¹','Uptake / g·g⁻¹'),ylim=(0,4),title=tr('b  比一个答案更强的关系检查','b  Check a relationship, not one answer'))
    ax.text(.55,.65,tr('干、湿质量同时加倍\n相减结果与分母都加倍\n比值保持 3 g/g','Double both masses:\nthe difference and denominator\nboth double; the ratio stays 3 g/g'),fontsize=13)
    ax.grid(alpha=.15);save(fig,'function-domain')

    fig=plt.figure(figsize=(12,7),layout='constrained');ax=fig.add_subplot();ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.2,6.65,tr('复用的关键：带着输入进入，带着结果返回','Reuse: enter with inputs, return with a result'),fontsize=19,weight='bold')
    ax.text(.2,6.05,tr('EDSAC：1948–49年的子程序研究 → 今天的函数调用示意','EDSAC subroutine work, 1948–49 → a modern function-call illustration'),fontsize=13)
    for i,(label,inputs,result) in enumerate([('A01','1.20 g, 4.80 g','3.00 g/g'),('A02','1.00 g, 3.40 g','2.40 g/g')]):
        y=4.9-i*2.5
        ax.add_patch(Rectangle((.3,y-.6),3.1,1.2,facecolor=blue,alpha=.1));ax.text(.5,y+.15,f'{label} → uptake(...)',fontsize=16);ax.text(.5,y-.3,inputs,fontsize=14)
        ax.add_patch(FancyArrowPatch((3.6,y+.25),(7.2,3.55),arrowstyle='->',connectionstyle=f'arc3,rad={-.2 if i==0 else .2}',mutation_scale=18,color=blue,lw=2))
        ax.add_patch(FancyArrowPatch((7.2,3.15),(3.6,y-.25),arrowstyle='->',connectionstyle=f'arc3,rad={.25 if i==0 else -.25}',mutation_scale=18,color=red,lw=2))
        ax.text(4.0,y+.3,tr('传入参数','Pass arguments'),fontsize=12,color=blue,bbox={'facecolor':'#fbfaf6','edgecolor':'none','pad':1.5})
        ax.text(4.0,y-.5,tr('返回','Return')+' '+result,fontsize=13,color=red,bbox={'facecolor':'#fbfaf6','edgecolor':'none','pad':1.5})
    ax.add_patch(Rectangle((7.4,2.35),4.2,2.3,facecolor=green,alpha=.1,edgecolor=green))
    ax.text(7.7,4.18,'def uptake(dry_g, wet_g):',fontsize=14,weight='bold')
    ax.text(7.7,3.6,tr('检查输入与缺失','Check inputs and missing data'),fontsize=14)
    ax.text(7.7,3.05,'return (wet_g - dry_g) / dry_g',fontsize=13)
    ax.text(.3,.45,tr('同一份定义；两次调用具有各自的局部参数。图为原理示意，并非EDSAC指令。','One definition; two calls with separate local parameters. Conceptual diagram, not EDSAC instructions.'),fontsize=12)
    save(fig,'subroutine-history')
    summary={'dataset':'Constructed six-specimen uptake records','record_count':len(records),**summarize([r['uptake_g_per_g'] for r in results]),'sum':math.fsum(r['uptake_g_per_g'] for r in results if r['uptake_g_per_g'] is not None),'missing_ids':[r['id'] for r in results if r['status']=='missing'],'invalid_examples':invalid_examples,'empty_summary':summarize([]),'scaling_check':uptake(2.4,9.6),'trace':trace}
    for name,data in [('summary',summary),('results',results),('records',records)]:
        (args.output/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    print(json.dumps({k:summary[k] for k in ['record_count','valid_count','sum','mean','missing_ids']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
```

Read the program once by following data: records enter `analyze`; masses enter `uptake`; available values enter `summarize`; results and traces enter plotting. The later style and save settings present already calculated quantities. At the bottom, `if __name__ == '__main__':` calls `main()` when the file runs directly. Importing a function from the file later does not automatically produce the full set of plots. This organization becomes useful when the next chapter separates stored records from the code that processes them.

The expression `[value for value in values if value is not None]` in the summary function is a list comprehension. It can be expanded into an empty list followed by a loop that checks each value and appends those that are not `None`. It shortens a simple filtering operation without changing the missing-data rule. Read from `for` to the condition and then to the expression placed in the new list. More elaborate branches remain clearer as an ordinary loop. The aim is to trace each output to its inputs, rather than minimize the number of written lines.

### Save outputs in either language

The output directory contains three figures, input records, results, and a summary.

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

The saved summary reports six records, five valid values, a total near 11.8, and a mean of 2.36, with B02 listed as missing. Long decimal representations in JSON reflect floating-point arithmetic; figures display two to four decimal places for reading. The three figures show execution, the input plane, and call–return relationships. The files `records.json`, `results.json`, and `summary.json` preserve inputs, individual statuses, and aggregate results with the trace. Display precision and retained numerical data remain separate choices.

Default arguments offer a convenient interface when an option has a stable usual meaning. For example, `enumerate` has a default start value, and we explicitly set it to one. When designing a function, make units and essential scientific rules clear even if optional settings have defaults. Avoid using a mutable list as a default object that the function repeatedly appends to: that same default object is shared across calls. A common alternative defaults to `None` and creates a fresh list inside the function. The relationship between names and objects links this issue to the copying behavior from the preceding chapter.

Function size can be judged by how clearly its purpose can be stated. Our uptake function answers one specimen-level question; the summary function answers how many values exist and what their equal-weight mean is; the analysis function connects records with those operations. A reader can test each idea with small input before following the full workflow. This organization also makes a later change local. If a new experiment needs a different mass model, its specimen calculation can be revised while keeping the visible record and summary structure under review.

When practicing, run the definition and one call before adding the loop. If a later edit causes trouble, reduce the problem in the reverse direction: move from the full batch to the affected specimen and then to its two masses. Keeping those inputs gives a repeatable calculation. This resembles retaining the conditions of an experimental observation. Once a problem is represented by a small call with known inputs, it becomes easier to determine whether a change fixes that particular behavior and preserves the relationships checked elsewhere.

## Predict what the next record changes

The experiment below begins before any record has been processed. “Next record” advances the table, current branch, and running curve together. “Process all” displays the completed result. With the default inputs, predict whether B02 will change the valid count and mean, then examine the fifth step. Next supply B02 with a wet mass of 2.80 g and restart. It now contributes a numerical value. Each input change starts the trace again so that every displayed step belongs to the currently selected data.

### Execution desk: how does one record enter the summary?

Advance through the original records, then edit one specimen. Input changes restart the trace. “Restart trace” retains edits; “Restore data” restores all six original records.

[Figure: Current function branch and running mean](https://ml-biomat.com/tutorials/python-scientific/p04/en/#P04-plot)

The highlighted box marks where the current call ends; green marks passed checks. Blue points follow valid returns, red points add no value, and gray positions are unprocessed. Every available specimen has equal weight in the mean.

| Step | ID | Dry mass | Wet mass | Status | Return | Valid count | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- |

Set A01's wet mass equal to its dry mass and observe how numerical zero enters the valid count. Then reduce its wet mass below dry mass and inspect the retained invalid status and reason. Gray positions mark unprocessed records, while the branch labels distinguish missing measurements from inputs requiring examination. Blue points show running means already produced. Finally return to the function definition and explain which `return` ended a particular call or which check raised its exception. Following a concrete input through an execution path turns function syntax into a calculation you can reason about.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Software Carpentry — Writing Functions](https://swcarpentry.github.io/python-novice-gapminder/16-writing-functions.html)

   Adapts the definition–call–return teaching progression using an original specimen calculation. Copyright The Carpentries.

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; original case, prose, code and figures.
2. [Python 3.14 — More Control Flow Tools](https://docs.python.org/3.14/tutorial/controlflow.html)

   Language reference for conditions, loops, parameters, local names, and defaults.

   PSF documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Errors and Exceptions](https://docs.python.org/3.14/tutorial/errors.html)

   Raising and handling specified exceptions.

   PSF documentation license
4. [University of Cambridge — A Brief Informal History of the Computer Laboratory](https://www.cl.cam.ac.uk/events/EDSAC99/history.html)

   Historical facts on EDSAC subroutines, scientific routines, and the 1951 programming book.

   Historical factual reference; copyright University of Cambridge. Original diagram; no reproduced source illustration.
