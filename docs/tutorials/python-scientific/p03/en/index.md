# Organizing Experiments with Lists and Dictionaries

Source: https://ml-biomat.com/tutorials/python-scientific/p03/en/
Language: en

Keep specimen identities, conditions, and values together through sorting, missing data, and copying.

## When specimens multiply, how does each value keep its identity?

Chapter one handled a single gel specimen, so two variables could hold its dry and wet masses. Now imagine six specimens split between water and saline baths, each with an identifier, treatment condition, and temperature. Continuing with names such as `dry_1`, `dry_2`, `wet_1`, and `wet_2` creates a growing collection of manual pairings. A missing weighing or a new ordering by mass can disturb those pairings. This chapter introduces lists and dictionaries as structures that keep specimen identity, conditions, and measurements together while the collection grows.

We use six constructed teaching records. A01, A02, and A03 belong to the water bath; B01, B02, and B03 belong to the saline bath. Every temperature field is 25.0 °C. Dry masses are 1.20, 1.00, 0.80, 1.20, 1.00, and 0.80 g. Wet masses are 4.80, 3.40, 2.80, 3.60, missing, and 2.32 g. Container contributions have already been removed. The dry mass is a fixed reference, and the added mass is counted as absorbed liquid; liquid taken up from the saline bath includes water and dissolved components. The letter prefixes are convenient labels in this example, but the analysis reads the explicit treatment field. Changing an identifier convention should not silently change how a specimen is assigned to a treatment.

Think of each record as a complete label attached to a specimen bag. Its identifier says which specimen it is, its conditions describe what happened to it, and its masses provide quantities for calculation. A list resembles an ordered rack that holds many records. A dictionary resembles the named fields on each label, pairing a field name with its value. Together they support both selecting the second record by position and locating A02 by a stable identifier. Both routes should retrieve the same wet mass of 3.40 g.

We will begin with a simple list of numbers, then build a dictionary, a list of records, and an identifier-based lookup. Missing values, sorting, and copying introduce distinctions that matter in real analysis. The final figures and experiment expose a subtle error: exactly the same numerical values can produce very different uptake results when dry and wet masses lose their original correspondence. Preserving the number of entries and avoiding a software error are useful checks, but the structure must also preserve what each entry means.

![Structure of six teaching records. Positional indexing selects a record, while a field key selects a value. Identifier lookup can find the same specimen after reordering.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8ffbb30a3bf980fbbeb419c5.svg?v=8ffbb30a3bf9)

Figure 1Structure of six teaching records. Positional indexing selects a record, while a field key selects a value. Identifier lookup can find the same specimen after reordering.

## A list gives values ordered positions

A list places values inside square brackets and separates them with commas, as in `dry_masses = [1.2, 1.0, 0.8]`. These three entries correspond to three records in order. The function `len(dry_masses)` returns the length, three, and `dry_masses[0]` retrieves the first value, 1.2. Python positions begin at zero, so indices zero, one, and two refer to the first, second, and third entries. One useful interpretation counts steps from the beginning: reaching the first entry requires zero steps.

A negative index counts from the end: `dry_masses[-1]` retrieves the last value, 0.8. The slice `dry_masses[0:2]` retrieves the entries starting at zero and ending before position two. Excluding the right endpoint lets adjacent ranges, such as `[0:2]` and `[2:3]`, meet without repeating a boundary entry. A slice gives a sequence, while a single index gives one contained object. Predicting the result on paper with positions written above the values is a practical way to learn the distinction.

### Positions, slices, and appending

Results are 3; 1.2 and 0.8; [1.2,1.0]; and finally [1.2,1.0,0.8,1.1].

```
dry_masses = [1.2, 1.0, 0.8]
print(len(dry_masses))
print(dry_masses[0], dry_masses[-1])
print(dry_masses[0:2])
dry_masses.append(1.1)
print(dry_masses)
```

List arithmetic also differs from numerical arithmetic. Adding two lists joins them end to end: `[1.2, 1.0] + [0.8]` produces three entries. Multiplying a list by two repeats its sequence, so `[1.2, 1.0] * 2` produces four entries instead of doubling each mass. Changing every number requires applying a calculation to the individual entries; loops and NumPy arrays will provide appropriate tools. Whenever an unfamiliar object uses a familiar operator, inspect what that operator means for the object rather than assuming it performs the numerical operation suggested by its symbol.

Lists can change. Calling `dry_masses.append(1.1)` adds one value at the end. The object appears to the left of the dot, the operation name to the right, and the input inside parentheses. This method changes the existing list and returns `None`, so assigning its return value back to the list name would lose that name's reference to the list. Assigning `dry_masses[1] = 1.05` replaces the second entry without changing the length. Deleting an entry shifts later entries forward. A position therefore describes the current arrangement and does not automatically provide a permanent specimen identity.

A list can contain different types, but possible storage is not always clear organization. Interleaving identifiers, masses, and temperatures in one long list forces every operation to remember what each position means. Lists are natural for a sequence of comparable observations, such as temperature readings in time order. Different fields of one specimen benefit from named relationships. A dictionary makes those field meanings visible in the retrieval expression instead of relying on a hidden positional convention.

## A dictionary keeps a field name attached to its value

A dictionary uses braces and contains entries formed from a key, a colon, and a value. A key is the name used for lookup, such as `"dry_g"`; its value might be 1.2. The expression `sample["dry_g"]` retrieves dry mass from the specimen record. Quotation marks identify the field name as a string, and the brackets specify the key being requested. One dictionary can contain strings, numbers, and a missing-value marker because its fields describe different aspects of the same specimen. Unit suffixes preserve the conventions established in the previous chapter.

### Read and update by field name

The first lookup gives A01 and 4.8; the absent note gives None; the updated wet_g is 4.9.

```
sample = {"id": "A01", "bath": "water", "dry_g": 1.2, "wet_g": 4.8}
print(sample["id"], sample["wet_g"])
print(sample.get("note"))
sample["wet_g"] = 4.9
print(sample["wet_g"])
```

Keys are unique within a dictionary. Assigning a value to an existing key updates its association rather than creating a second field with the same key. This is useful, but requires care when specimen identifiers become keys. If two records are assigned to the outer key A01, the later association replaces the earlier one. Check identifier uniqueness before constructing the lookup. The expression `set(ids)` creates a collection of distinct identifiers; comparing its length with the original identifier list reveals duplicates. Here the set checks uniqueness, while the list remains responsible for record order.

Python dictionaries preserve insertion order, so fields normally display in the order in which they were added. Retrieval by key nevertheless follows the association, rather than a displayed row position. `sample["wet_g"]` still retrieves wet mass if the order of fields changes. Lists and dictionaries both use square brackets for lookup, but ask different questions: a list index identifies a position, while a dictionary key identifies an association. Distinguishing those questions clarifies whether an operation must preserve a sequence or preserve a named relationship.

Direct bracket lookup is useful for required fields because a missing key produces a `KeyError`, revealing a spelling or structural problem. The expression `sample.get("note")` suits a genuinely optional note, returning `None` when the key is absent unless another default is supplied. Giving a required wet-mass field a default of zero would let computation continue while turning an absent weighing into a real zero reading. Define required fields first, then specify how missing contents are represented, and only then decide which records can enter a particular calculation.

## Move whole records so sorting preserves the experiment

Before building records, define what one record represents. Here it contains one dry–wet weighing pair for one specimen, so specimen ID is unique. If the same specimen is weighed at ten, twenty, and thirty minutes, there are multiple observations. Each observation could receive a separate identifier while retaining specimen ID and time as fields, or the specimen record could contain an organized time series. A repeated specimen ID is therefore not automatically an entry error: permitted repetition follows the unit of the record. Define that unit first so the uniqueness check tests the intended object.

Putting the six specimen dictionaries inside a list creates `records`. The expression `records[1]` selects the second dictionary, and a following `["wet_g"]` selects its wet-mass field. The lookup proceeds from specimen to quantity. We can also build `by_id`, a dictionary mapping every identifier to its full record, and retrieve the same value with `by_id["A02"]["wet_g"]`. The list supports processing in the current order, while the mapping supports finding a named specimen. These structures can reference the same records without creating independent copies of the experimental data.

Sort records as complete objects. After ordering the collection by dry mass, A01 may occupy a different list position, but its identifier, water-bath condition, dry mass, and wet mass remain in the same dictionary. The complete example uses `sorted` to create a newly ordered list while preserving the original list order. Its key specifies the field used for comparison, here dry mass. Records with equal dry masses retain their previous relative order. Sorting changes presentation and traversal, while the relationships inside each record stay intact.

Now consider sorting only the wet-mass column. The original water-bath pairs are 1.20 with 4.80, 1.00 with 3.40, and 0.80 with 2.80 g, giving uptake values of 3.00, 2.40, and 2.50 g/g. Sorting wet masses alone associates 2.80 g with A01's dry mass of 1.20 g and 4.80 g with A03's dry mass of 0.80 g. The resulting values become approximately 1.33, 2.40, and 5.00 g/g. The wet-mass total has not changed, and every value still resembles a plausible weighing, but the specimen relationships have been broken.

![Associations among the first three water-bath records. Correct associations retain identifiers; sorting wet masses independently changes pairing and uptake. The historical data-independence question is connected to stable identity in this example.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9fc94a997dace3763fe0e777.svg?v=9fc94a997dac)

Figure 2Associations among the first three water-bath records. Correct associations retain identifiers; sorting wet masses independently changes pairing and uptake. The historical data-independence question is connected to stable identity in this example.

This concern connects to a major development in data management. E. F. Codd's 1970 relational-model paper examined how users could work with data without depending closely on its internal storage arrangement. Our small example makes identifier-to-measurement relationships explicit so that rearrangement does not change which specimen owns a value. Ordinary Python dictionaries supply keyed lookup and lists organize traversal. Larger tables, relational queries, and persistent data management introduce additional tools later. The principle established here is to distinguish stable identity from a temporary position.

## An absent weighing and a zero reading have different meanings

B02's wet mass is `None`, indicating that this weighing did not supply a numerical value. Zero has a different meaning: 0 g is a numerical record, potentially calling for an examination of the object or weighing process. `None` means that no mass is available to substitute into the formula. Replacing the absent wet mass with zero would produce an uptake of −1 g/g, effectively claiming that the entire dry specimen mass disappeared. A casual data-cleaning substitution would thereby become a strong physical statement unsupported by a weighing.

Our rule retains B02's complete record and also records its uptake as `None`. Only calculations requiring a numerical wet mass skip that result. The collection still contains six records, while five uptake values are available: three in the water group and two in the saline group. The figure retains B02's position and marks it as not weighed, so the location of the missing observation remains visible. Its identifier, dry mass, and treatment are still useful information even when one particular calculation cannot use the record.

$$
q_i=\frac{m_{w,i}-m_{d,i}}{m_{d,i}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Index corresponding to a specimen identity, dimensionless; all quantities refer to the same specimen |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | Dry-basis liquid uptake of specimen i, g/g and dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/58390e8adf97ce97c3d618a2.svg) | Net wet mass of specimen i, g; an absent value leaves q uncomputed |
| ![Formula](https://ml-biomat.com/static/agent-math/5bb3742873949f3a3604d91d.svg) | Positive net dry mass of specimen i, g |
| ![Formula](https://ml-biomat.com/static/agent-math/1526ecedf7893f4ee28503c0.svg) | Subtract dry from wet mass to obtain retained-liquid mass in this example |

A02 gives (3.40−1.00)/1.00=2.40 g/g; B03 gives (2.32−0.80)/0.80=1.90 g/g. Identity keeps each pair within a specimen. B02 lacks wet mass and retains None as its result.

The formula first calculates retained liquid for each specimen, then divides by that specimen's own dry mass. A02 gives (3.40−1.00)/1.00=2.40 g/g, and B03 gives (2.32−0.80)/0.80=1.90 g/g. The code checks missingness with `is None`. A broad condition such as `if not value` would also treat numerical zero and an empty string as false, mixing situations that have different meanings. Checking the intended missing marker keeps the rule connected to the record. Later pandas chapters develop richer missing-data representations from this basic distinction.

Before calculating, the script also verifies that dry mass is positive and that wet mass is not below dry mass in this pure uptake example. Those conditions follow from the mass interpretation and the formula's denominator. Missing-data handling says that a quantity was not provided; range validation asks whether a provided value satisfies the current calculation's conditions. Keeping original fields and adding a separate result field makes both operations visible and preserves the measurements needed to recalculate under a revised analysis rule.

## Keep individual specimens and valid counts beside a summary

Once the records are organized, comparing group means is a natural next question. Plotting every specimen first reveals within-group variation and missing positions. The water group contains 3.00, 2.40, and 2.50 g/g; the saline group contains the two available values 2.00 and 1.90 g/g. Each plotted point retains its specimen identity, while color indicates the group. Mean lines summarize those points and valid counts identify how many values entered the calculation. The summary is easier to interpret because its contributing records remain visible.

$$
\bar q_G=\frac{1}{n_G}\sum_{i\in G_{\mathrm{valid}}}q_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Selected treatment group, such as water or saline; a label |
| ![Formula](https://ml-biomat.com/static/agent-math/a91f85a3669211aaa75489f7.svg) | Set of specimens in the group with valid uptake values |
| ![Formula](https://ml-biomat.com/static/agent-math/cf52d0d51f7a704e935d0e7c.svg) | Number of valid specimens, a positive dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/a2d98e5d8f94ef37d7537f81.svg) | Uptake of specimen i, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/af6a93670140117cb6d2d5f5.svg) | Group mean giving each valid specimen equal weight, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/99c8b956831093e4e1e9a7c9.svg) | The sum adds the individual terms; membership selects valid specimen indices |

Water gives (3.00+2.40+2.50)/3=2.6333… g/g; saline gives (2.00+1.90)/2=1.95 g/g. If no valid results exist, retain a missing mean rather than divide by zero.

We give every available specimen equal weight. The water-group mean is (3.00+2.40+2.50)/3≈2.6333 g/g, and the saline-group mean is (2.00+1.90)/2=1.95 g/g. The denominator counts available results, not the planned number of specimens. Dividing the saline sum by three would implicitly add a zero result and lower its mean to 1.30 g/g. Displaying both the denominator and valid count allows direct recalculation and makes the missing-value rule visible in the summary itself.

![Individual specimens and the missing position appear on the left; valid counts and equally weighted specimen means appear on the right. Constructed data, calculated by the script.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a6437a272aab13c9766ab9b0.svg?v=a6437a272aab)

Figure 3Individual specimens and the missing position appear on the left; valid counts and equally weighted specimen means appear on the right. Constructed data, calculated by the script.

Growing collections also need consistent field contents. The strings `"water"`, `"Water"`, and `"water "` differ, with the last containing a trailing space. Grouping by their literal text would create separate conditions. A defined input rule can normalize agreed capitalization and surrounding spaces while retaining conditions that truly differ. A temperature of twenty-five and an absent temperature field also remain distinct. Applying cleaning rules together at the input boundary makes their effect easier to inspect than repairing records separately inside each summary calculation.

A mean of specimen-level ratios differs from adding masses first and calculating a ratio for the entire batch. The latter weights specimens according to their dry mass and asks how much water the combined starting material retained. The equal-specimen mean used here practices calculating each record before grouping the results. [Chapter twelve](https://ml-biomat.com/tutorials/python-scientific/p12/en/) develops weighting and grouped summaries in greater depth. Naming the object being averaged prevents a familiar mean symbol from hiding a change in the unit of comparison.

These teaching records demonstrate structures and calculation rules. Differences between the displayed groups show what follows from the specified inputs. Comparing treatments in a research experiment requires a corresponding design, independent specimens, and measurement descriptions. A data structure should make room for that information, such as batch, time, and treatment concentration. Beginning with clear specimen identities and adding the fields the experiment requires gives later statistical analysis a traceable connection to experimental objects.

## Complete code: from original records to inspectable results

The script below defines all six records near the beginning and requires no network data. It checks identifier uniqueness, constructs a lookup by identifier, calculates uptake record by record, and saves both original and processed records. The statement `for record in records` selects each record in turn, and the indented statements act on that current record. An `if` statement chooses a branch according to a condition. The next chapter develops loops and functions in detail. For now, read this structure as applying one rule to every record while following how inputs remain attached to results.

### Complete record analysis and figures

Records and calculations use built-in Python structures; figures use Matplotlib.

```
"""Keep specimen identity attached to values while organizing records."""
from pathlib import Path
import argparse
import json
import math
import copy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    # Net specimen masses in grams; constructed teaching records.
    records=[
        {"id":"A01","bath":"water","dry_g":1.2,"wet_g":4.8,"temperature_C":25.0},
        {"id":"A02","bath":"water","dry_g":1.0,"wet_g":3.4,"temperature_C":25.0},
        {"id":"A03","bath":"water","dry_g":0.8,"wet_g":2.8,"temperature_C":25.0},
        {"id":"B01","bath":"saline","dry_g":1.2,"wet_g":3.6,"temperature_C":25.0},
        {"id":"B02","bath":"saline","dry_g":1.0,"wet_g":None,"temperature_C":25.0},
        {"id":"B03","bath":"saline","dry_g":0.8,"wet_g":2.32,"temperature_C":25.0},
    ]
    ids=[record['id'] for record in records]
    if len(set(ids))!=len(ids):raise ValueError("Specimen identifiers must be unique.")
    by_id={record['id']:record for record in records}
    processed=[]
    for record in records:
        if record['dry_g']<=0:raise ValueError("Dry mass must be positive.")
        item=record.copy()
        if record['wet_g'] is None:
            item['uptake_g_per_g']=None
        else:
            if record['wet_g']<record['dry_g']:raise ValueError("Check uptake mass accounting.")
            item['uptake_g_per_g']=(record['wet_g']-record['dry_g'])/record['dry_g']
        processed.append(item)
    groups={}
    for bath in ['water','saline']:
        all_rows=[r for r in processed if r['bath']==bath]
        values=[r['uptake_g_per_g'] for r in all_rows if r['uptake_g_per_g'] is not None]
        groups[bath]={'record_count':len(all_rows),'valid_count':len(values),'mean_uptake':math.fsum(values)/len(values) if values else None}
    ordered=sorted(records,key=lambda row:row['dry_g'])
    ordered_lookup={record['id']:record for record in ordered}
    assert ordered_lookup['A01']==by_id['A01']
    # Assignment shares an object; deepcopy provides independent nested records.
    alias=records
    independent=copy.deepcopy(records)
    independent[0]['dry_g']=9.0
    assert records[0]['dry_g']==1.2 and alias is records

    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ['Noto Sans CJK SC','Microsoft YaHei','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans'],'font.size':12,'axes.titlesize':15,'axes.titleweight':'bold','svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36','axes.labelcolor':'#172b36','axes.spines.top':False,'axes.spines.right':False})
    ink,blue,red,green='#172b36','#28648a','#b85336','#467a62'
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12,7),layout='constrained');ax=fig.add_subplot();ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,7)
    ax.text(.1,6.6,tr('a  列表保留记录顺序，字典保留字段名称','a  A list orders records; dictionaries name their fields'),fontsize=17,weight='bold')
    cols=[.2,1.4,3.3,5.1,7.1,9.3]; widths=[1,1.7,1.6,1.7,1.9,2.4]
    headers=[tr('位置','Position'),'id','bath','dry_g','wet_g','temperature_C']
    for x,label in zip(cols,headers):ax.text(x,5.95,label,fontsize=13,weight='bold')
    for i,r in enumerate(records):
        y=5.05-i*.62
        vals=[str(i),r['id'],r['bath'],f"{r['dry_g']:.2f}",'None' if r['wet_g'] is None else f"{r['wet_g']:.2f}",f"{r['temperature_C']:.1f}"]
        for j,(x,w,val) in enumerate(zip(cols,widths,vals)):
            ax.add_patch(Rectangle((x-.05,y-.13),w,.5,facecolor=red if i==1 else blue,alpha=.13 if i==1 else .045,edgecolor='#cad2d0',lw=.6))
            ax.text(x+.05,y+.03,val,fontsize=13,color=red if val=='None' else ink)
    ax.text(.2,.85,'records[1]["wet_g"] → 3.40 g',fontsize=19,color=red)
    ax.text(6.0,.85,'by_id["A02"]["wet_g"] → 3.40 g',fontsize=17,color=blue)
    ax.text(.2,.2,tr('None表示缺少该次称量；0.00表示称量值为零。两者参与计算的规则不同。','None marks an absent weighing; 0.00 is a numerical reading. They require different calculations.'),fontsize=12)
    save(fig,'record-anatomy')

    fig=plt.figure(figsize=(12,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.1,1.2])
    for panel,wrong in enumerate([False,True]):
        ax=fig.add_subplot(gs[0,panel]);ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
        ax.set_title(tr('a  排序整条记录：身份保持','a  Sort whole records: preserve identity') if not wrong else tr('b  单独排序一列：配对改变','b  Sort one column alone: change pairing'),loc='left')
        order=[2,1,0] if not wrong else [0,1,2]
        left=['A01 | 1.20 g','A02 | 1.00 g','A03 | 0.80 g']; right=['A03 | 2.80 g','A02 | 3.40 g','A01 | 4.80 g']
        for i in range(3):
            y=.78-i*.28;ax.text(.02,y,left[i],fontsize=13);ax.text(.67,y,right[i],fontsize=13)
            dest=2-i if not wrong else i
            ax.add_patch(FancyArrowPatch((.36,y+.02),(.65,.78-dest*.28+.02),arrowstyle='->',mutation_scale=16,color=[blue,green,red][i],lw=1.7))
        ax.text(.02,.96,tr('干质量及身份','Dry mass + identity'),fontsize=11);ax.text(.67,.96,tr('湿质量及身份','Wet mass + identity'),fontsize=11)
    ax=fig.add_subplot(gs[1,0]);correct=[3,2.4,2.5];wrong=[(2.8-1.2)/1.2,(3.4-1)/1,(4.8-.8)/.8]
    for i,(c,w) in enumerate(zip(correct,wrong)):
        ax.plot([c,w],[i,i],color='#acb8b8',lw=2);ax.scatter([c],[i],color=blue,s=80,zorder=3);ax.scatter([w],[i],color=red,s=70,marker='x',zorder=3)
    ax.set(yticks=[0,1,2],yticklabels=['A01','A02','A03'],xlabel=tr('按干质量归一化的吸液量 / g·g⁻¹','Dry-basis liquid uptake / g·g⁻¹'),title=tr('c  相同数字，错误关联改变结果','c  The same numbers give different results'))
    ax.grid(axis='x',alpha=.15);ax.scatter([],[],color=blue,s=60,label=tr('正确配对','Correct pairing'));ax.scatter([],[],color=red,s=60,marker='x',label=tr('错配','Mismatched'));ax.legend(frameon=False)
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.set_title(tr('d  从存储位置转向数据含义','d  Separate position from meaning'),loc='left')
    ax.text(.02,.78,'E. F. Codd · 1970',fontsize=20,color=ink,transform=ax.transAxes)
    ax.text(.02,.54,tr('关系数据模型关注：\n改变存储安排时，数据关系保持清楚。','Relational data modeling asks how\nmeaning can survive changes\nin storage arrangement.'),fontsize=15,transform=ax.transAxes)
    ax.text(.02,.15,tr('本例中的做法：\n把样品ID、条件与测量值放在同一记录中。','In this example:\nkeep specimen ID, conditions,\nand measurements in one record.'),fontsize=14,transform=ax.transAxes)
    save(fig,'identity-history')

    fig=plt.figure(figsize=(12,6),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.4,1])
    ax=fig.add_subplot(gs[0]);
    for i,r in enumerate(processed):
        color=blue if r['bath']=='water' else red;q=r['uptake_g_per_g']
        if q is None:ax.text(.08,i,tr('未称量','Not weighed'),va='center',color='#6b7779',fontsize=12)
        else:ax.hlines(i,0,q,color=color,alpha=.4,lw=2);ax.scatter([q],[i],s=80,color=color);ax.text(q+.08,i,f'{q:.2f}',va='center',fontsize=12)
    ax.set(yticks=range(6),yticklabels=ids,xlim=(0,3.7),xlabel=tr('吸液量 / g·g⁻¹','Liquid uptake / g·g⁻¹'),title=tr('a  每个点保留样品身份','a  Keep each specimen visible'));ax.set_ylim(-.5,len(processed)-.5);ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
    ax=fig.add_subplot(gs[1]);
    for i,bath in enumerate(['water','saline']):
        vals=[r['uptake_g_per_g'] for r in processed if r['bath']==bath and r['uptake_g_per_g'] is not None];col=blue if i==0 else red
        ax.scatter([i+(.1*(j-(len(vals)-1)/2)) for j in range(len(vals))],vals,color=col,s=70,alpha=.8)
        avg=groups[bath]['mean_uptake'];ax.text(i,3.3,tr(f"有效 {len(vals)} / 3",f"{len(vals)} of 3 valid"),ha='center',fontsize=14)
        if avg is not None:
            ax.hlines(avg,i-.25,i+.25,color=ink,lw=3)
            label=tr(f'均值 {avg:.4f}',f'Mean {avg:.4f}')
        else:
            label=tr('无有效称量','No valid weighing')
        ax.text(i,.4,label,ha='center',fontsize=13,color=col)
    ax.set(xticks=[0,1],xticklabels=[tr('水浴','Water'),tr('盐水浴','Saline')],ylabel=tr('吸液量 / g·g⁻¹','Liquid uptake / g·g⁻¹'),ylim=(0,3.6),xlim=(-.55,1.55),title=tr('b  汇总同时说明有效计数','b  Summaries retain valid counts'));ax.grid(axis='y',alpha=.15)
    save(fig,'specimen-results')
    summary={'dataset':'Constructed six-record liquid-uptake example','record_count':len(records),'valid_count':sum(r['uptake_g_per_g'] is not None for r in processed),'missing_ids':[r['id'] for r in processed if r['uptake_g_per_g'] is None],'groups':groups,'uptake_by_id':{r['id']:r['uptake_g_per_g'] for r in processed},'lookup_A01_after_sort':ordered_lookup['A01'],'independent_copy_original_dry_g':records[0]['dry_g'],'wrong_pairing_A_uptake':wrong}
    for name,data in [('records.json',records),('processed.json',processed),('summary.json',summary)]:
        (args.output/name).write_text(json.dumps(data,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

The code also demonstrates a subtle copying issue. The assignment `alias = records` makes two names refer to the same list, so changing an inner dictionary is visible through either name. Copying only the outer list can still leave the dictionaries shared. `copy.deepcopy(records)` creates independent nested records in this example, allowing a change to the copy without altering the originals. The script performs a definite change and then checks that A01's original dry mass remains 1.20 g. Understanding names, containers, and contained objects prevents an exploratory edit from changing the data already being analyzed.

For calculation, the example calls `record.copy()` to copy one dictionary before adding `uptake_g_per_g`. Its original fields contain only strings, numbers, and `None`, so a shallow copy is enough to keep the added field separate from the original dictionary. A nested mutable field, such as a list of time-series measurements, would require another look at the sharing relationship. The useful question is which object layer will be changed and which objects should continue serving as shared original records.

### Run and retain three output levels

Generates original records, specimen results, a summary, and three scientific figures.

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

After execution, inspect `summary.json` for six total records, five available uptake values, and the missing identifier B02. Then check uptake by identifier. The file `records.json` contains original fields, while `processed.json` includes computed results. JSON writes Python's `None` marker as `null`. Each file serves a clear role: inspect the input, trace an individual specimen through calculation, or compare summaries quickly. Preserving these levels makes an entry or pairing error easier to locate than retaining only the two final means.

## Reorder a record, edit a weighing, and follow its identity

The experiment below lets you select a specimen, edit dry and wet masses, mark a wet mass as missing, and sort records by identifier, dry mass, or wet mass. The table and result plot update together, and highlighting follows the selected identifier. Select A01 before changing the ordering: its position may change, but its wet mass and uptake should remain attached to A01. A comparison mode deliberately sorts the three water-bath wet masses separately, showing how an incorrect association changes calculated results while the same input numbers remain present.

### Move records, preserve identity

Select a specimen before sorting or editing. Table position and graphical highlighting follow the same identifier. The purple mismatching comparison retains the input values.

| Position | ID | Bath | dry_g | wet_g | Uptake / g·g⁻¹ |
| --- | --- | --- | --- | --- | --- |

[Figure: Paired masses and uptake by specimen](https://ml-biomat.com/tutorials/python-scientific/p03/en/#P03-plot)

Next select B02, remove the missing marker, and enter a wet mass of 2.80 g. Its dry mass is 1.00 g, so the added uptake is 1.80 g/g. The saline valid count rises from two to three, and its mean changes from 1.95 to 1.90 g/g. This change follows a newly available observation, rather than a reordering. Mark the value missing again: the specimen record remains, its numerical point disappears, and the summary denominator returns to two. Observing position changes, numerical edits, and observation availability separately makes data organization an interpretable sequence of operations.

Finish by explaining the responsibility of each structure: a list preserves an order of records, a dictionary preserves field associations, an identifier index supports stable lookup, and a missing marker preserves the fact that a value is absent. Together they allow a small program to handle more specimens without multiplying the amount of manual pairing. The next chapter turns the repeated calculation into functions so that one scientific rule can be called, checked, and reused clearly.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Software Carpentry — Lists](https://swcarpentry.github.io/python-novice-gapminder/11-lists.html)

   Adapts the progression from individual indexing to collection changes, using an original specimen-record case. Copyright The Carpentries.

   CC BY4.0, https://creativecommons.org/licenses/by/4.0/; original prose, code and figures.
2. [Python 3.14 — Data Structures](https://docs.python.org/3.14/tutorial/datastructures.html)

   Language reference for lists, dictionaries, sorting, and shallow copying.

   PSF documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Built-in Types](https://docs.python.org/3.14/library/stdtypes.html#dict)

   Mapping lookup, insertion order, and operations relevant to missing markers.

   PSF documentation license
4. [E. F. Codd — A Relational Model of Data for Large Shared Data Banks (1970)](https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks)

   Historical motivation for separating data meaning from internal storage arrangement.

   Historical factual reference to IBM publication record; no reproduced article text or figure.
