# Joining Tables without Losing Their Meaning

Source: https://ml-biomat.com/tutorials/python-scientific/p13/en/
Language: en

Trace sample identity and statistical weight through concat, merge, and every individual match.

## The information for one observation often lives in several tables

An instrument saves stress values, a sample register records formulations, and another table records preparation batches. Asking which formulation has higher stress requires connecting these pieces of information. Copying columns side by side looks quick, but it assumes that all tables retain exactly the same row order. A repeated measurement or missing row can shift the correspondence for everything that follows. pandas provides joins based on field values, allowing each observation to find its sample metadata. This chapter traces the individual pairings between two small tables and then shows how one repeated match changes a mean without changing any original measurement.

The teaching measurement table has six records. R01 and R02 belong to sample S01 and contain stresses of 12 and 14 kPa. R03 belongs to S02 and contains 18 kPa. R04 and R05 belong to S03 and contain 21 and 23 kPa. R06 belongs to S04 and contains 16 kPa. Names beginning with R identify observations; names beginning with S identify samples. These identifiers answer different questions. A sample may be measured more than once, so its identifier can legitimately repeat in the measurement table. Each observation retains its own record identifier so a result can be traced back to the original row.

The sample metadata table has a different grain: one row describes one sample and its formulation. S01 and S03 use formulation A, while S02 and S05 use B. Two deliberate mismatches help explain the join rules. S04 has a measurement but no formulation entry, and S05 has a metadata entry but no measurement. The grain of a table means what one row represents. Establish it before joining, because an additional result row might represent a valid one-to-many association or another use of the same observation.

Think of the tables as an experimental notebook and a sample register. An observation in the notebook uses its sample identifier to find the corresponding description in the register. Reordering the register should not change that relationship. The same reasoning applies to patients and tests, devices and sensor readings, molecules and properties, or simulation tasks and output files. We will connect the tables, retain unmatched objects, check key uniqueness, and follow the way each output row enters a statistical calculation.

## Understand a key-based join through the relational idea

In 1970, E. F. Codd introduced a relational data model that separated the logical organization of information from its physical storage arrangement. IBM's historical account emphasizes access through relationships among information rather than dependence on exact storage locations. Matching two tables by sample identifier is an immediate application of that idea. The relevant question is which sample an observation belongs to, rather than the row position it happens to occupy. In the diagram, the metadata order is deliberately S03, S01, S05, S02. Equal identities still connect correctly.

![The relational idea illustrated with the example tables: one row is an observation on the left and a sample on the right. Arrows connect equal sample keys. Metadata are deliberately reordered; S04 has measurements only and S05 has metadata only.](https://ml-biomat.com/static/tutorials/python-scientific/figures/b90c530829490e2071f3f938.svg?v=b90c53082949)

Figure 1The relational idea illustrated with the example tables: one row is an observation on the left and a sample on the right. Arrows connect equal sample keys. Metadata are deliberately reordered; S04 has measurements only and S05 has metadata only.

A field used for matching is called a key. Here the key is the `sample` column, whose values such as S01 and S02 are identifiers. They contain digits but are not measured quantities to average: adding S01 to S02 has no scientific interpretation. Keeping identifiers as strings preserves leading zeros and avoids automatic conversion to another representation. Because a key distinguishes identity, spaces, letter case, and character encoding can affect equality. Normalize keys according to the registration convention while retaining fields that allow the original records to be checked.

A key also has a scope. If every batch restarts sample numbering at S01, the sample identifier alone cannot identify a specimen across all batches. Use `batch` and `sample` together as a composite key, analogous to using a batch name plus a sample name to find an object. Similarly, row 10 in one file need not be the same observation as row 10 in another. Row position describes a current arrangement, while a record identifier describes identity. Sorting, filtering, or rebuilding the index should preserve identity fields.

In pandas, a `DataFrame` is a table with row labels and column names. A join can use explicit columns or an index. Keeping identity in visible columns and declaring `on="sample"` makes early work easy to inspect. If corresponding key columns have different names, use `left_on` and `right_on`. Their values must still refer to the same kind of identity. Equal column names do not guarantee equal meanings, and equal meanings do not require identical column names.

## Include scope when sample names repeat across batches

Consider a separate miniature example. Sample S01 in batch B01 has a stress of 10 kPa, while S01 in batch B02 has a stress of 30 kPa. The register assigns formulation A to B01/S01 and formulation B to B02/S01. Joining on S01 alone gives each observation two same-named metadata matches, producing four combinations. These include a B01 measurement paired with B02 metadata. Each individual file may be well organized; the ambiguity arises when the scope of the identifier is discarded during joining. Using batch and sample together preserves the distinction between the two experimental objects.

The argument `on=["batch", "sample"]` requires both fields to match. The 10 kPa observation for B01/S01 is assigned A, and the 30 kPa observation for B02/S01 is assigned B, giving two rows again. The full script contains this small example and saves its correctly joined result as `composite-key.csv`. Reorder the register and inspect the result: matching field values preserves sample identity. A composite key can also include a test stage, location, or measurement round, but each additional field should have an identifiable role in distinguishing the objects being connected.

The key and the scientific grain determine each other. If a specimen is measured before and after treatment, its sample identifier links fixed sample attributes, while sample plus stage distinguishes the two observation conditions. If two instruments measure the same specimen, instrument identity may belong to observation identity without belonging to sample identity. Decide whether the intended object is a sample, one measurement, or a treatment stage before selecting the fields. Too few fields can mix distinct objects; unnecessary fields with inconsistent meanings can separate records that refer to the same object.

Inspect compound-key duplication with `duplicated(["batch", "sample"], keep=False)`. This marks all rows belonging to repeated combinations, allowing them to be reviewed together. The option `keep=False` includes the first occurrence, so the comparison retains both the original and later occurrences. Whether repetition is appropriate still follows table grain. A sample register commonly requires unique combinations, whereas a measurement table can legitimately contain several observations for one specimen. Once identity is defined, a duplicate check becomes a meaningful part of experimental data organization.

## Adding observations and adding attributes are different operations

`concat` is useful for placing observation tables with the same structure one after another. Suppose a second collection contains R07 and R08 with the same record, sample, and stress columns. Put the two tables into a list and pass it to `pd.concat` to obtain eight observations. The option `ignore_index=True` creates new row labels beginning at zero, avoiding repeated index labels when both input tables start at zero. The original `record` column still carries measurement identity. Rebuilding row labels and renaming experimental records are different operations.

Vertical concatenation aligns fields by column name, not merely by column position. If one table uses `stress_kPa` and the other uses `stress_MPa`, direct concatenation creates two columns with missing entries where each field is absent. This exposes the need to reconcile units and field definitions. If both columns are called `stress` but use different units, the software places their values into the same column, making the unit mismatch harder to see. Columns intended to combine therefore need matching meanings and units before concatenation.

`merge` addresses another task: adding an object's attributes to observations already recorded for that object. Here each observation needs the formulation of its sample. Both S01 observations should acquire formulation A while remaining separate observations. Placing the two tables side by side with `concat` primarily aligns row labels; it does not infer sample identity. Adding new measurements and enriching existing measurements may both enlarge a table, but they depend on different correspondence rules.

For many small files, read each file into a table, add a meaningful batch field, collect the tables in a list, and concatenate them together. This preserves the experimental grouping of each record and avoids repeatedly creating growing intermediate tables. Then check that record identifiers are unique and that columns and data types match expectations before joining metadata. More files do not change the underlying questions: what does each row represent, how is it identified, and how does it relate to a row in the other table?

## Decide where unmatched objects should remain

With the measurement table on the left and the metadata table on the right, `how` determines which keys enter the result. An `inner` join keeps matching records from both sides. Here that retains S01, S02, and S03, giving five observations. A `left` join retains every left-table observation and adds right-table attributes where available. It produces six rows, with a missing formulation for S04. An `outer` join retains keys from either side, adding S05 with formulation B but no observation identifier or stress. It produces seven rows.

The rule follows the scientific task. To organize all measurements that have already occurred, a left join retains S04 and makes its missing registration an identifiable item to complete. To compare measurements whose formulations are known, inspect matching first and then explicitly select that population. An outer join is useful for reconciling a register with a measurement log: it reveals both “measured but not registered” and “registered but not measured.” No rule has a universal priority. Each specifies which objects the current analysis intends to retain.

### Declare the join and its relationship check together

The complete script below creates measurements and specimens in make_tables. m:1 allows many observations on the left to match one sample on the right; indicator retains match status.

```
joined = measurements.merge(
    specimens, on="sample", how="left",
    validate="m:1", indicator=True,
)
missing = joined.loc[joined["_merge"].eq("left_only")]
print(joined)
print(missing[["record", "sample"]])
```

`indicator=True` creates a `_merge` column containing match status. The value `both` means a corresponding key was found on both sides; `left_only` means a left-side record has no match; `right_only` identifies right-side information without a match. These values can produce a table of records needing additional information, saved separately from statistical results. A missing formulation is different from a formulation whose code is zero, and a missing stress is different from a measured stress of 0 kPa. Filling an absent observation with zero changes the meaning of the record and affects means and plots.

![Three join rules applied to the same data. Unique keys produce 5, 6, and 7 rows for inner, left, and outer joins; duplicating S03 metadata produces 7, 8, and 9. Colors identify matched, left-only, and right-only rows.](https://ml-biomat.com/static/tutorials/python-scientific/figures/27fb4f684fa892d688de2eab.svg?v=27fb4f684fa8)

Figure 2Three join rules applied to the same data. Unique keys produce 5, 6, and 7 rows for inner, left, and outer joins; duplicating S03 metadata produces 7, 8, and 9. Colors identify matched, left-only, and right-only rows.

Declare join keys explicitly. If `on` is omitted, pandas may use common column names together as matching conditions, so adding another shared column later can change the result. For non-key fields present on both sides, such as a column named `temperature`, suffixes can preserve each field's role while their agreement is checked. Two temperature fields do not determine which value should take precedence. If one describes preparation temperature and the other test temperature, clear names are the appropriate way to retain both meanings.

## How a repeated key turns two observations into four output rows

The sample key can repeat in the measurement table because a specimen can be measured several times. In contrast, the metadata table is intended to contain one formulation record for each sample. This is a many-to-one relationship, expressed as `validate="m:1"`. The m permits multiple rows on that side, and the 1 requires unique keys on the other. Validation reports an error when the relationship is violated, locating the identity ambiguity in the joining step. It translates the understanding that the right-hand table is a unique register into an executable condition.

Consider accidentally copying the S03 metadata row. R04 now matches the first S03 entry and the second. R05 has the same two possibilities, so two observations generate four result rows. Equal-key matching forms every combination of left and right records carrying the key. Each output row satisfies the equality rule, but there have still been only two measurements. An increased row count should therefore prompt a trace through record identifiers and pairings before additional rows are interpreted as additional data.

$$
N_k=m_k n_k
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | A particular key, such as sample S03; identifier, no units |
| ![Formula](https://ml-biomat.com/static/agent-math/db7985d73352cce0c498191f.svg) | Number of left-table rows with key k; dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/e80174098629760a1d5dacc9.svg) | Number of right-table rows with key k; dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/ad7b34e7b5b399c686f1e5e8.svg) | Number of matched output rows for this key; dimensionless integer |

Every left record with the key pairs with every right record with that key. S03 has 2 measurement rows and 1 metadata row, giving 2×1=2 matches. Duplicating its metadata gives 2×2=4 matches. This expression counts matched rows; unmatched rows retained by left or outer joins are counted separately.

Many-to-many relationships can also be intentional. Suppose one table lists several components in each sample and another lists several measurements of that sample. Joining by sample can associate every measurement with every component. A result row then represents a measurement–component combination rather than one measurement. Subsequent statistics must follow that new grain. A measurement-level mean belongs at the unique-record level; component associations require a clear account of how each observation contributes to different component groups.

When duplicates appear, immediately dropping duplicate rows can conceal the question that needs answering. Two metadata entries might be identical, contain spelling differences, or refer to different preparation batches or versions. Inspect all fields associated with a repeated key before deciding whether to combine equivalent records, add a composite key, or select a version by an explicit rule. Removing a row becomes meaningful once its identity relationship is understood. Validation makes the relationship visible so it can be resolved before statistics are calculated.

## Changes in row count enter the mean

Formulation A originally contains R01, R02, R04, and R05, with stresses 12, 14, 21, and 23 kPa. Their mean is 17.5 kPa. After S03 metadata is repeated, the values 21 and 23 each appear twice. Averaging every merged output row now gives 19 kPa. No original stress value was edited, yet the mean changed because the join changed how often individual observations entered the calculation. In effect, the S03 measurements acquired greater statistical weight.

$$
\bar y_w=\frac{\sum_{i=1}^{n}w_i y_i}{\sum_{i=1}^{n}w_i}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Original measurement index; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of original measurements; dimensionless, 4 here |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Stress recorded in observation i, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | Number of appearances of original record i in the merged output; dimensionless nonnegative integer |
| ![Formula](https://ml-biomat.com/static/agent-math/a1a67b1c7514ecc0a21130b6.svg) | Mean stress across merged result rows, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the terms across all original observations |

Formulation A contains 12, 14, 21, and 23 kPa. One appearance each gives 70/4=17.5 kPa. Repeated matching changes the multiplicities to 1, 1, 2, and 2, giving (12+14+42+46)/6=19 kPa. Joining creates no new measurement but changes how often observations enter the mean. The denominator is positive when at least one record is retained.

![Formulation A has four original stress records. Duplicate S03 metadata makes R04 and R05 each appear twice, changing the mean across result rows from 17.5 to 19 kPa. Horizontal lines mark means on the left; zero-based bars show them on the right. Original measurements remain unchanged.](https://ml-biomat.com/static/tutorials/python-scientific/figures/5774200516be1ba062949820.svg?v=5774200516be)

Figure 3Formulation A has four original stress records. Duplicate S03 metadata makes R04 and R05 each appear twice, changing the mean across result rows from 17.5 to 19 kPa. Horizontal lines mark means on the left; zero-based bars show them on the right. Original measurements remain unchanged.

The value 17.5 kPa already has a specific statistical identity: it is the mean of four observations in group A. If samples have different numbers of measurements, averaging all rows gives greater influence to samples measured more often. Averaging within each sample first and then averaging across samples gives each sample one contribution. Those procedures can answer different questions. An accidental repeated match introduces neither a new measurement nor an intentionally designed sample weight, so it should be identified before analysis.

Read row count together with unique observation count after a join. Unique count tells how many distinct measurements were retained; row count tells how many combinations the join expanded. A left join that grows from six to eight rows while retaining six unique observation identifiers signals repeated appearances. Applying `value_counts` to key fields helps locate the responsible identities. Counting by record identifier shows exactly which observations obtained multiple matches. Retaining both levels of counts makes the resulting statistical calculation easier to trace.

Unmatched records also define the analyzed population. An inner join excluding S04 yields five matched observations rather than all six original measurements. If absent registration is associated with a particular batch or an experimental outcome, the retained data composition changes as well. Counting match rates, identifying missing registrations, and completing traceable metadata are part of defining the research dataset. Once those relationships are resolved, a reported mean refers to a clear set of observations.

## Follow every pairing through linked views

The experiment below shows correspondence between inputs, the complete merged table, and the resulting statistical changes. Every line in the match diagram represents one successful pair. The selected observation receives thicker links and highlighted output rows. Switching among `inner`, `left`, and `outer` does not change equal-key pairings; it changes whether unmatched objects enter the output. Original input records remain visible, allowing an excluded record to be distinguished from a record absent from the input.

## Trace an observation through a join

Choose a join rule or duplicate the S03 metadata record. The match diagram, complete output table, and statistical views update together. Track R04 or R05 to see how one observation generates two result rows when the right key is repeated.

[Figure: Correspondence links between observations and sample metadata](https://ml-biomat.com/tutorials/python-scientific/p13/en/#P13-links)

| Record | Sample | Stress / kPa | Formulation | Match status |
| --- | --- | --- | --- | --- |

[Figure: Output row counts and mean for formulation A](https://ml-biomat.com/tutorials/python-scientific/p13/en/#P13-summary-plot)

Select R04, keep a left join, and enable duplicate S03 metadata. R04 now has two bold links and two result rows; R05 changes in the same way. The input still contains six observations, while the output has eight rows and the group-A mean changes from 17.5 to 19 kPa. Switch to an outer join to add S05 metadata. It contributes no stress observation, so the group-A mean remains 19 kPa. The views distinguish two different reasons for additional rows: retaining metadata for an unmeasured sample and repeating an existing measurement through multiple matches.

The experiment also displays the `m:1` relationship check. When duplication is enabled, S03 has two right-table entries and native pandas reports a nonunique key under this requirement. The page expands those pairings so their origin can be inspected. In an analysis pipeline, resolve the relationship before producing the joined table used for statistics. Reset restores unique metadata keys, a left join, and R04 as the traced record.

## Save results that remain inspectable

The complete example builds the two teaching tables directly. It uses `concat` to append two observations and, separately, to create a deliberately repeated S03 metadata row. It then applies three join rules to unique-key and duplicate-key inputs, saves six CSV results, and records matched rows, unmatched rows on each side, unique observations, and the group-A mean. The intended many-to-one join enables `validate`. Another call checks that duplicated right keys produce `MergeError`. One part of the script computes results while the other checks the declared data relationship.

### Complete example: joining, checking, counting, and statistical weight

Calls pandas concat, merge, and groupby directly, saving each join result as CSV and generating three figures. A MergeError check detects the deliberately duplicated metadata key.

```
"""Join defined teaching tables and inspect record identity and statistical weight."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch,Rectangle

BLUE,RED,INK,GRAY='#28658c','#b64a35','#202e39','#71808b'


def make_tables():
    measurements=pd.DataFrame({'record':['R01','R02','R03','R04','R05','R06'],
        'sample':['S01','S01','S02','S03','S03','S04'],
        'stress_kPa':[12.,14.,18.,21.,23.,16.]})
    specimens=pd.DataFrame({'sample':['S03','S01','S05','S02'],
                            'formulation':['A','A','B','B']})
    return measurements,specimens


def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    def tr(a,b):return a if language=='zh' else b
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'font.size':11,
        'axes.labelsize':12,'axes.titlesize':13,'axes.titleweight':'bold','axes.spines.top':False,
        'axes.spines.right':False,'text.color':INK,'svg.fonttype':'none','svg.hashsalt':'P13'})
    measurements,specimens=make_tables()
    duplicated=pd.concat([specimens,specimens.loc[specimens['sample'].eq('S03')]],ignore_index=True)
    measurements.to_csv(output/'measurements.csv',index=False)
    specimens.to_csv(output/'specimens.csv',index=False)
    duplicated.to_csv(output/'specimens-duplicate.csv',index=False)
    summary={'data_kind':'explicitly defined teaching tables','cases':{}}
    results={}
    for duplicate,metadata in [(False,specimens),(True,duplicated)]:
        for how in ['inner','left','outer']:
            name=f'{how}-'+('duplicate' if duplicate else 'unique')
            result=measurements.merge(metadata,on='sample',how=how,indicator=True,sort=True)
            result.to_csv(output/f'{name}.csv',index=False)
            counts=result['_merge'].value_counts().to_dict()
            group=result.groupby('formulation')['stress_kPa'].agg(['count','mean'])
            summary['cases'][name]={'rows':len(result),'unique_observations':int(result['record'].nunique()),
                'matched':int(counts.get('both',0)),'left_only':int(counts.get('left_only',0)),
                'right_only':int(counts.get('right_only',0)),
                'A_count':int(group.loc['A','count']),'A_mean_kPa':float(group.loc['A','mean'])}
            results[name]=result
    validated=measurements.merge(specimens,on='sample',how='left',validate='m:1',indicator=True)
    try:
        measurements.merge(duplicated,on='sample',how='left',validate='m:1')
    except pd.errors.MergeError:
        summary['duplicate_contract_rejected']=True
    else:
        raise AssertionError('A duplicated right key must fail m:1 validation')
    extra=pd.DataFrame({'record':['R07','R08'],'sample':['S02','S03'],'stress_kPa':[20.,22.]})
    appended=pd.concat([measurements,extra],ignore_index=True)
    assert appended['record'].is_unique
    appended.to_csv(output/'appended-measurements.csv',index=False)
    summary['appended_rows']=len(appended)
    batch_measurements=pd.DataFrame({'batch':['B01','B02'],'sample':['S01','S01'],
                                      'stress_kPa':[10.,30.]})
    batch_metadata=pd.DataFrame({'batch':['B02','B01'],'sample':['S01','S01'],
                                'formulation':['B','A']})
    composite=batch_measurements.merge(batch_metadata,on=['batch','sample'],validate='m:1')
    ambiguous=batch_measurements.merge(batch_metadata,on='sample')
    composite.to_csv(output/'composite-key.csv',index=False)
    summary['composite_key_rows']=len(composite)
    summary['sample_only_rows']=len(ambiguous)
    assert composite['formulation'].tolist()==['A','B']
    assert len(validated)==6
    assert summary['cases']['left-duplicate']['rows']==8
    assert summary['cases']['left-unique']['A_mean_kPa']==17.5
    assert summary['cases']['left-duplicate']['A_mean_kPa']==19.
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',metadata={'Date':None})
        fig.savefig(output/f'{name}-{language}.png',dpi=180)
        plt.close(fig)
    fig=plt.figure(figsize=(12,6.5));ax=fig.add_axes([.03,.1,.94,.75]);ax.set_axis_off();ax.set(xlim=(0,1),ylim=(0,1))
    fig.text(.06,.94,tr('记录靠身份对应，不依赖当前行号','Records match by identity, independently of row order'),fontsize=16,weight='bold')
    ax.text(.04,1,tr('测量表：一行一次测量','Measurements: one row per observation'),fontsize=12,weight='bold')
    ax.text(.65,1,tr('样品表：一行一个样品','Metadata: one row per sample'),fontsize=12,weight='bold')
    colors={'S01':BLUE,'S02':'#886a29','S03':RED,'S04':GRAY,'S05':GRAY}
    for i,row in measurements.iterrows():
        y=.86-i*.135
        ax.add_patch(Rectangle((.035,y-.045),.39,.09,fc='#f2f6f8',ec='none'))
        ax.text(.055,y,f"{row['record']}   {row['sample']}   {row['stress_kPa']:.0f} kPa",va='center',fontsize=12,color=colors[row['sample']])
        for j,target in specimens.iterrows():
            if row['sample']==target['sample']:
                ax.add_patch(FancyArrowPatch((.44,y),(.64,.82-j*.20),arrowstyle='->',mutation_scale=11,color=colors[row['sample']],alpha=.65))
    for j,row in specimens.iterrows():
        y=.82-j*.2
        ax.add_patch(Rectangle((.65,y-.055),.30,.11,fc='#f2f6f8',ec='none'))
        ax.text(.67,y,f"{row['sample']}   →   {row['formulation']}",va='center',fontsize=12,color=colors[row['sample']])
    fig.text(.06,.035,tr('关系数据思想：用字段值表达对应关系；物理存放次序可以改变。','Relational idea: field values specify correspondence while storage order can change.'),fontsize=11,color=GRAY)
    save(fig,'identity')
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),layout='constrained',sharey=True)
    for ax,suffix,title in zip(axes,['unique','duplicate'],[tr('样品键唯一','Unique sample keys'),tr('S03在样品表出现两次','S03 appears twice in metadata')]):
        bottom=np.zeros(3)
        for field,color,label in [('matched',BLUE,tr('成功对应','Matched')),('left_only',RED,tr('只有测量','Measurement only')),('right_only',GRAY,tr('只有样品信息','Metadata only'))]:
            values=np.array([summary['cases'][f'{how}-{suffix}'][field] for how in ['inner','left','outer']])
            ax.bar(np.arange(3),values,bottom=bottom,color=color,width=.55,label=label)
            for x,y,b in zip(np.arange(3),values,bottom):
                if y:ax.text(x,b+y/2,str(y),ha='center',va='center',color='white',weight='bold')
            bottom+=values
        ax.set(xticks=np.arange(3),xticklabels=['inner','left','outer'],ylim=(0,11),title=title)
        ax.legend(frameon=False,loc='upper left',fontsize=10)
    axes[0].set_ylabel(tr('合并结果行数','Rows in the merged result'))
    save(fig,'join-counts')
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.3,1]},layout='constrained')
    left=results['left-unique'];dup=results['left-duplicate'];labels=['R01','R02','R04','R05']
    values=np.array([12,14,21,23])
    counts=[int(dup['record'].eq(label).sum()) for label in labels]
    for i,(record,value,count) in enumerate(zip(labels,values,counts)):
        axes[0].scatter([0],[value],s=55,color=BLUE)
        axes[0].scatter([.9+ .14*j for j in range(count)],[value]*count,s=55,color=RED)
        axes[0].annotate(record,(0,value),xytext=(-28,3),textcoords='offset points',ha='right',fontsize=10)
    axes[0].hlines([17.5,19],[-.15,.75],[.15,1.2],colors=[BLUE,RED],lw=3)
    axes[0].set(xticks=[0,1],xticklabels=[tr('键唯一','Unique keys'),tr('S03重复','Duplicate S03')],
                xlim=(-.45,1.35),ylim=(9,25),ylabel=tr('配方A的应力记录 / kPa','Stress records in formulation A / kPa'),
                title=tr('同一条记录被重复计入','The same observation enters twice'))
    axes[1].bar([0,1],[17.5,19],color=[BLUE,RED],width=.55)
    axes[1].set(xticks=[0,1],xticklabels=[tr('4条结果行','4 result rows'),tr('6条结果行','6 result rows')],
                ylim=(0,24),ylabel=tr('按结果行计算的均值 / kPa','Mean across result rows / kPa'),
                title=tr('重复匹配改变了统计权重','Repeated matches change statistical weight'))
    for i,v in enumerate([17.5,19]):axes[1].text(i,v+.6,f'{v:g}',ha='center',fontsize=13)
    save(fig,'weights')
    summary['versions']={'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

Executed output gives 5, 6, and 7 rows for unique-key inner, left, and outer joins. Duplicating S03 changes these counts to 7, 8, and 9. The unmatched objects remain S04 and S05; the two additional matched rows come from one extra pairing for each S03 observation. Group A expands from four result rows to six, and its mean changes from 17.5 to 19 kPa. Named fields in `summary.json` allow these quantities to be compared directly with the figures and CSV files.

For your own files, retain the same reasoning sequence: establish row meaning and keys, standardize identifier representation and relevant units, inspect missing identities, declare the join relationship, perform the validated join, and examine match states and counts. pandas treats missing join keys differently from some database systems: null keys on both sides can match each other. When sample identity is unknown, treating every empty key as one sample can generate extra combinations. Separate missing-key records before joining so an absent identifier does not stand in for a shared identity.

After joining, every field should have a clear object, meaning, and unit. As the dataset grows, batch and time can also become part of identity. The next chapter organizes multiple experimental batches in time, separates calendar time from elapsed experiment time, and examines how time bins change summary curves. The principle developed here continues to apply: establish objects and correspondence first, then use table operations to answer the scientific question.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P13.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pandas: How to combine data from multiple tables](https://pandas.pydata.org/docs/getting_started/intro_tutorials/08_combine_dataframes.html)

   Official introductory route through concatenation and key-based joins.

   pandas BSD-3; original case and figures
2. [pandas: Merge, join, concatenate and compare](https://pandas.pydata.org/docs/user_guide/merging.html)

   Match cardinality, validate, indicator, and overlapping column names.

   pandas BSD-3 documentation
3. [IBM: The relational database](https://www.ibm.com/history/relational-database)

   Computing-history context for Codd’s 1970 relational model.

   Historical facts paraphrased; no source image or text reproduced
