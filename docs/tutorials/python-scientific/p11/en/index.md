# Reading and Cleaning a Real Data Table

Source: https://ml-biomat.com/tutorials/python-scientific/p11/en/
Language: en

Use Antarctic penguin records to understand rows, columns, units, missing values, and selection that preserves observation identity.

## Ask what a row represents before calculating

A spreadsheet full of measurements can look like a collection of interchangeable numbers. Yet a value of 4.2 might represent mass, length, acidity, or a category code. Before calculating, we need to reconnect the entries to their observations: what was measured, which fields belong together, what units were used, and what an empty entry means. pandas is designed for tables that combine numbers with names, categories, and other labels. This chapter uses real penguin measurements to practise reading, inspecting, selecting, and saving records, keeping each plotted point connected to an observation.

The dataset contains 344 adult penguin records from three species, recorded as Adelie, Chinstrap, and Gentoo. Its fields describe island, two bill dimensions, flipper length, body mass, sex, and study year. The program retains the category spellings in the CSV so that one species does not accidentally become two groups through inconsistent naming. No background in bird classification is required for the table operations: these names initially serve as categories distinguishing the observed animals.

A useful first question is which records describe Adelie penguins from Dream Island with body mass of at least 4000 g. This combines two category conditions with a numerical condition and requires an observed mass. We will translate the sentence into separate conditions, obtain 14 records, and mark them in a scatter plot of flipper length against body mass. The selected set belongs to this particular dataset. Species and island combinations reflect the field sampling arrangement, and the plots reveal which combinations actually have records.

The complete example includes the CSV, so execution reads the supplied file without a network connection. The openly released CC0 data were collected by Kristen Gorman and the Palmer Station Long Term Ecological Research project; palmerpenguins provides the simplified table. All figures and selections in this chapter are computed from those records. We retain the input unchanged, generate stable chapter record labels, and create additional columns and output tables separately. That arrangement makes it possible to trace a plotted marker back to its recorded values.

## Column names preserve a field measurement's structure

The observations span three Antarctic field seasons, labelled 2007, 2008, and 2009 in the table. The original study was published in 2014. Researchers measured adult penguins at island breeding nests, using calipers for bill dimensions, a ruler for flipper length, and scales for body mass. For biologists, these measurements describe different parts of an animal. In a program, they become separate columns. Each observation connects bodily structure to place and time, and the table preserves those connections.

Bill length and bill depth describe different dimensions of the bird's bill. A longer bill need not have a proportionally greater depth, so both fields are retained. The flipper is a modified forelimb, and its length describes another aspect of body size. Body mass is a measurement of the whole animal. A local length and a total mass can belong to the same row, but their numerical appearance does not make adding them meaningful. The suffixes `_mm` and `_g` keep the units close to their variable names throughout the calculation.

The species-by-year counts show that real data are rarely a grid of equally sized groups. Adelie has 50, 50, and 52 records across the three year labels; Chinstrap has 26, 18, and 24; Gentoo has 34, 46, and 44. Each value counts rows actually present in the file. Unequal group sizes matter for later summaries and make retaining species and year useful. Study year identifies a sampling season. Combining multiple years in a table does not by itself establish repeated observations of the same individual; studying individual change would require identifiers that link animals across time.

The history of pandas also concerns the structure of observation tables. Wes McKinney's 2010 paper introduced data structures for records with named fields, mixed types, and observation labels. NumPy already supported efficient numerical arrays; practical tables also required answers to questions such as which field a column represents and which records correspond across results. A DataFrame organizes values together with labels, allowing a program to select body mass by name and retrieve one observation by its record label. The figure connects the field sampling structure with concrete rows in the table.

![Species-by-year count matrix, four measurement fields, and six example rows including NA.](https://ml-biomat.com/static/tutorials/python-scientific/figures/37efe782341119acfe4433da.svg?v=37efe7823411)

Figure 1Study-year labels are 2007, 2008, and 2009. The count matrix preserves actual species totals; measurement names connect to columns, and the first six records show generated PG identifiers.

## A DataFrame is a table; a Series is a labelled column

`pd.read_csv` reads a CSV into a DataFrame, which can initially be understood as a table with row and column labels. The original `shape` is (344, 8), meaning 344 rows and eight columns. `head(6)` displays the first six rows so we can inspect field names, separators, and the positions of numerical values. `shape` is an existing attribute and takes no parentheses, while `head` performs a selection and is called with parentheses. An ellipsis in a displayed table indicates shortened display rather than removed observations.

`table['body_mass_g']` returns a Series: one column retaining its row labels. In contrast, `table[['body_mass_g']]` returns a one-column DataFrame. The inner brackets create a list of column names, while the outer brackets perform the selection. This distinction matters when a later function expects one-dimensional or two-dimensional input. Selecting several fields means putting their names in the same list. Choosing species, island, and body mass produces a narrower table while preserving the relationship among measurements from each record.

We label the first CSV record PG001, the second PG002, and so on through PG344. These generated labels identify positions in this particular input file for tracing and teaching; they are separate from the animal identifiers used in the original research. The program uses `set_index` to make them index labels and also retains a `record_id` column for export. An index acts like a catalogue label that helps locate a row. It does not require that row to remain at one numerical display position.

`table.loc['PG001']` retrieves the record carrying that label, while `table.iloc[0]` retrieves the first row in the current ordering. Immediately after reading the file, both point to the same observation. After sorting by descending body mass, `iloc[0]` refers to PG170, with mass 6300 g, whereas `loc['PG001']` still retrieves the record with mass 3750 g. The difference separates the current first row from the original first observation. Filtering similarly retains labels: gaps in the selected numbering simply mean that intervening records were not selected.

Label and position slices also use different endpoint conventions. `iloc[0:3]` selects positions 0, 1, and 2, excluding position 3 as in ordinary Python slicing. With this chapter’s ordered, unique label index, `loc['PG001':'PG003']` includes both endpoint labels and also returns the first three records. Decide whether the request refers to three positions or an interval of labels before choosing the expression. Sorting changes positions and order while each label should remain attached to its record.

## Keep numerical types, categories, and units distinct

A CSV is text, so reading it requires an interpretation of each column. Species, island, and sex are read as strings. Bill length and depth use nullable `Float64`, while flipper length, body mass, and year use nullable `Int64`. The uppercase I and F belong to pandas' nullable type names. They allow a column to contain numerical values together with `<NA>`, representing a missing entry. An integer-recorded mass column can therefore retain two missing measurements without disguising them as a large negative sentinel number.

A storage type and a scientific meaning are related but distinct. Years are stored as integers, yet they usually serve as selection or grouping labels here; adding them to bill length would have no useful interpretation. Species names are strings, and their alphabetical order does not measure biological distance. `dtypes` describes the representation used for storage and operations, while the field definitions explain what the values mean. Declaring types during reading also exposes text that does not fit an expected numerical field, directing attention back to the input record.

The original body-mass column uses grams. For plotting, we create an additional kilogram column by dividing the whole Series by 1000. pandas converts observed values and leaves missing entries missing. PG001 changes from 3750 g to 3.75 kg, representing the same animal and the same measured mass. Keeping the original gram column and naming the new one `body_mass_kg` lets the selection use a 4000 g threshold while the plot uses kilograms. Both units remain visible in their column names.

$$
m_{\mathrm{kg}}=\frac{m_{\mathrm g}}{1000}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dc51519473042eca7790d43a.svg) | Numerical value of body mass expressed in g |
| ![Formula](https://ml-biomat.com/static/agent-math/d795b0597896cbce0a258e78.svg) | Numerical value of the same body mass expressed in kg |
| ![Formula](https://ml-biomat.com/static/agent-math/11e3e740ee2e42f3954f5b75.svg) | Numerical conversion factor because 1 kg contains 1000 g |

This converts the numerical representation of one physical quantity. PG001 has 3750 g, which becomes 3.75 kg after division by 1000. Retain the gram column and create a kilogram column; missing values remain missing.

When assigning a Series as a new column, pandas aligns it by index labels. A sorted Series assigned to another table is matched through its labels rather than simply pasted according to its current display order. This is useful for labelled calculations and depends on retaining appropriate, meaningful identifiers. Explicit conversion to a NumPy array removes labels, after which operations normally follow positions. Decide whether the intended relationship is by observation identity or by numerical position before making that conversion.

Category spellings and spaces deserve inspection as well. `Adelie` and `Adelie`, with a trailing space, compare as different strings. If an input contains such differences, identify which spellings refer to one category before standardizing them. Two animals may also happen to have identical measured masses and lengths. Equality of a few numerical fields alone does not establish duplicate entry; removing a duplicate requires fields or records that identify the observation itself.

## A missing entry changes which questions a row can answer

The original token `NA` indicates that a field has no available value. Using `isna()`, the program finds two missing masses, two missing entries in each length field, and eleven missing sex entries. PG004 and PG272 lack all four body measurements and sex, while retaining species, island, and year. Another nine records have body measurements but no sex entry. A missingness matrix shows whether several absent fields occur in the same observation, information that separate column totals cannot provide.

![Missing counts by field and a record-by-field missingness matrix.](https://ml-biomat.com/static/tutorials/python-scientific/figures/bc7014f8c0c45d04252b9be9.svg?v=bc7014f8c0c4)

Figure 2Each body measurement has two missing values; sex has eleven. The matrix shows all eleven incomplete records: PG004 and PG272 lack five fields, while nine others lack sex only.

A missing mass differs from a mass of zero. The first describes an unavailable weighing; the second asserts a measured mass of 0 g. Filling the two missing values with zero still allows a mean to be calculated, but it changes the question. The observed masses average approximately 4201.754 g, whereas the incorrectly zero-filled column averages approximately 4177.326 g. The total measured mass stays the same, while the denominator increases from 342 to 344. The animals have not become lighter. Successful execution therefore needs to be accompanied by an understanding of whether the operations preserve the observations' meaning.

$$
f_{\mathrm{observed}}=\frac{N-M}{N},\qquad P_{\mathrm{observed}}=100f_{\mathrm{observed}}\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Total rows in the current record set, here 344; dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Missing entries for the field being checked, 2 for mass; dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/11f64c3bfb2e86718a2ef65d.svg) | Fraction with an observed value in that field; dimensionless, from 0 to 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/a763e1e215ae6ae5172f959a.svg) | The same fraction expressed as a percentage; % means per hundred |
| ![Formula](https://ml-biomat.com/static/agent-math/8c0d9d65f3495da5c81dd0e3.svg) | Factor converting a fraction to its percentage value |

Subtract missing entries from total records, then divide by the total. Mass coverage is 342/344≈0.994186, or 99.4186%; sex coverage is 333/344≈96.8023%. Specify the field and record set before interpreting the fraction. For an empty set N=0, report no records rather than computing the ratio.

The fields required by a question determine which rows are usable. A flipper-length-versus-mass scatter plot needs both of those measurements, giving 342 usable records in this dataset. A comparison by sex also needs a sex entry; requiring all eight original fields to be complete leaves 333 records. An animal with measured mass but missing sex can still contribute to a mass distribution. The program creates selections for the needed fields instead of deleting every incomplete record at the start. Each analysis can then report its actual number of usable observations.

Use `isna()` or `notna()` to detect missing entries. Equality to a missing-value symbol does not provide the same test. Comparing a nullable unknown mass with a threshold can also give an unknown result. The mass condition in this chapter therefore uses `fillna(False)`, specifying that a record with unknown mass does not satisfy “at least 4000 g.” This fills the Boolean selection result, not the mass measurement. When no mass threshold is set, the interactive selection can retain incomplete records while separately reporting how many have coordinates for the scatter plot.

## Turn one question into three conditions

Separate the request into Dream Island, Adelie species, and mass of at least 4000 g. `table['species'].eq('Adelie')` checks species for each record, `table['island'].eq('Dream')` checks island, and `table['body_mass_g'].ge(4000)` checks mass. Each expression returns Boolean values aligned to the original index. Combining them with `&` requires every condition to hold; `|` expresses an alternative. When writing direct comparisons, parentheses around each condition make the grouping explicit.

Python's `and` normally combines two individual truth values and cannot directly replace `&` between entire condition columns. Some rows satisfy a condition while others do not, so one Boolean cannot describe the whole column. The mask retains these row-by-row decisions. `table.loc[mask]` then selects rows where the mask is True. A list of column names after the comma can narrow the output fields. Selection operates on complete records, keeping species, island, and measurements paired within their original rows.

The resulting 14 records begin with PG036, PG040, PG044, and PG046, whose masses are 4150, 4650, 4400, and 4600 g. Rings in the figure locate the selected records within the full scatter. All lie on or above the 4 kg reference line, but other points above the line are excluded because they do not satisfy both category conditions. Showing the selection against its full observational background reveals what each condition contributes rather than presenting only the final reduced table.

![Species-coloured length–mass scatter, selected-record rings, mass histogram, and identifiers.](https://ml-biomat.com/static/tutorials/python-scientific/figures/18f2781b32798a3e21944245.svg?v=18f2781b3279)

Figure 3All 342 records with flipper length and mass provide context; rings identify 14 records satisfying Adelie, Dream, and at least 4000 g. Histogram and identifiers show the same selection.

When adding or changing columns in a selected result, the program first creates an explicit result table with `.copy()`. To assign into a region of an existing table, use a single `.loc[row_condition, column_name]` operation. This makes the target of the change clear and fits pandas 3 assignment semantics. Export uses `index=False` because `record_id` is already retained as an ordinary column; exporting the index as well would duplicate that information. Writing missing entries as `NA` allows a later read to restore the same convention.

The scatter and histogram offer different views. A scatter point pairs length and mass from one record; two records with identical measurements can overlap, so the number of visible markers may be smaller than the record count. The histogram divides mass into 250 g intervals and counts records within them. Both views come from the same identified rows. One preserves the relationship between two variables, while the other summarizes the distribution of one. Read axis units, interval widths, and counts together so that a bar height is not mistaken for a mass value.

## The complete example, from input table to traceable selection

The download includes `main.py`, the unchanged `penguins.csv`, and a data-license notice. No network connection is needed during execution. The program locates the CSV beside its own file, so the terminal's current directory does not determine where it looks for data. `load_table` declares types, creates record labels, and converts kilograms; `select_records` applies the conditions; the main function saves result tables, numerical summaries, and three figures. All functions are included below so that each operation can be followed directly.

### Run the real-table example

Use --language zh for Chinese figures. Keep the supplied penguins.csv beside main.py.

```
python main.py --output output --language en
```

### Complete reading, inspection, selection, and plotting program

Preserve the input, declare column types, label records, add kilograms, and export the same selection as CSV and figures.

```
"""Read, inspect, select, and plot real CC0 Palmer penguin measurements."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap

SPECIES = ['Adelie', 'Chinstrap', 'Gentoo']
COLORS = {'Adelie': '#2e6e91', 'Chinstrap': '#b7553d', 'Gentoo': '#37806a'}
MEASUREMENTS = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
DTYPES = {'species':'string','island':'string','bill_length_mm':'Float64',
          'bill_depth_mm':'Float64','flipper_length_mm':'Int64',
          'body_mass_g':'Int64','sex':'string','year':'Int64'}


def load_table(path):
    raw = pd.read_csv(path, dtype=DTYPES, na_values=['NA'])
    table = raw.copy()
    table.insert(0, 'record_id', [f'PG{i+1:03d}' for i in range(len(table))])
    table = table.set_index('record_id', drop=False)
    table.index.name = 'record_key'
    table['body_mass_kg'] = table['body_mass_g'] / 1000
    return raw, table


def select_records(table, species='all', island='all', minimum_g=0, complete=False):
    mask = pd.Series(True, index=table.index)
    if species != 'all':
        mask &= table['species'].eq(species)
    if island != 'all':
        mask &= table['island'].eq(island)
    if minimum_g > 0:
        mask &= table['body_mass_g'].ge(minimum_g).fillna(False)
    if complete:
        mask &= table[list(DTYPES)].notna().all(axis=1)
    return table.loc[mask].copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('output'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    input_path = Path(__file__).with_name('penguins.csv')
    raw, table = load_table(input_path)
    missing = raw.isna().sum()
    complete_measurements = table.dropna(subset=MEASUREMENTS)
    complete_all = table.dropna(subset=list(DTYPES))
    selected = select_records(table, 'Adelie', 'Dream', 4000)
    mass_mean = float(table['body_mass_g'].mean())
    wrong_zero_mean = float(table['body_mass_g'].fillna(0).mean())
    ordered = table.sort_values('body_mass_g', ascending=False, kind='stable', na_position='last')
    with input_path.open(encoding='utf8', newline='') as file:
        independent = list(csv.DictReader(file))
    valid_mass = [int(r['body_mass_g']) for r in independent if r['body_mass_g'] != 'NA']
    selected_ids = [f'PG{i+1:03d}' for i,r in enumerate(independent)
                    if r['species']=='Adelie' and r['island']=='Dream'
                    and r['body_mass_g']!='NA' and int(r['body_mass_g'])>=4000]
    assert selected.index.tolist() == selected_ids
    assert len(raw)==344 and len(complete_measurements)==342 and len(complete_all)==333
    assert missing['body_mass_g']==2 and missing['sex']==11 and len(selected)==14
    assert math.isclose(mass_mean, math.fsum(valid_mass)/len(valid_mass))
    assert float(table.loc['PG001','body_mass_kg']) == 3.75
    assert pd.isna(table.loc['PG004','body_mass_g'])
    table.to_csv(args.output/'penguins_with_ids.csv', index=False, na_rep='NA')
    selected.to_csv(args.output/'selected_records.csv', index=False, na_rep='NA')
    records = json.loads(table.to_json(orient='records'))
    (args.output/'lab-records.json').write_text(json.dumps(records,ensure_ascii=False),encoding='utf8')
    zh=args.language=='zh'; tr=lambda z,e:z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family':family if zh else ['DejaVu Sans','Arial'],
                         'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold',
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none',
                         'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=170,bbox_inches='tight')
        plt.close(fig)

    fig=plt.figure(figsize=(12.6,8.3),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,.95])
    counts=pd.crosstab(raw['species'],raw['year']).reindex(SPECIES)
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(counts.to_numpy(),cmap='Blues',vmin=0,vmax=60,aspect='auto')
    for i in range(3):
        for j in range(3):ax.text(j,i,str(counts.iloc[i,j]),ha='center',va='center',fontsize=19,color='white' if counts.iloc[i,j]>35 else '#172b36')
    ax.set(xticks=[0,1,2],xticklabels=counts.columns,yticks=[0,1,2],yticklabels=SPECIES,
           xlabel=tr('研究年份标签','Study-year label'),title=tr('a  三次野外季节留下的记录数','a  Records from three field seasons'))
    fig.colorbar(im,ax=ax,pad=.02).set_label(tr('记录数','Records'))
    ax=fig.add_subplot(gs[0,1]);ax.axis('off')
    ax.text(0,.98,tr('测量对象 → 量与单位 → 数据列','Observation → quantity and unit → column'),fontsize=15,weight='bold',va='top')
    descriptions=[('bill_length_mm',tr('喙长：沿喙的长度 / mm','Bill length / mm')),('bill_depth_mm',tr('喙深：喙的上下尺寸 / mm','Bill depth / mm')),('flipper_length_mm',tr('鳍状肢长度 / mm','Flipper length / mm')),('body_mass_g',tr('身体质量 / g','Body mass / g'))]
    for k,(field,label) in enumerate(descriptions):
        y=.77-k*.20;ax.text(0,y,label,fontsize=13);ax.text(0,y-.08,field,fontsize=12,color='#2e6e91')
    ax=fig.add_subplot(gs[1,:]);ax.axis('off')
    rows=[]
    for _,r in table.iloc[:6].iterrows():
        rows.append([r['record_id'],r['species'],r['island'],str(r['year']), 'NA' if pd.isna(r['body_mass_g']) else str(r['body_mass_g']), 'NA' if pd.isna(r['sex']) else r['sex']])
    tab=ax.table(cellText=rows,colLabels=['record_id','species','island','year','body_mass_g','sex'],cellLoc='center',bbox=[0,.08,1,.78]);tab.auto_set_font_size(False);tab.set_fontsize(12)
    for (i,j),cell in tab.get_celld().items():cell.set_edgecolor('#d1dddd');cell.set_facecolor('#e4eeec' if i==0 else '#fbfaf6');cell.set_text_props(color='#b7553d' if i==4 and j in [4,5] else '#172b36')
    ax.text(0,.98,tr('b  每行是一条观测；PG编号保留CSV中的记录位置','b  One observation per row; generated PG labels preserve CSV record positions'),fontsize=14,weight='bold')
    save(fig,'field-records-history')

    fig=plt.figure(figsize=(12.6,7.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);fields=MEASUREMENTS+['sex'];labels=[tr('喙长','Bill length'),tr('喙深','Bill depth'),tr('鳍状肢长','Flipper length'),tr('质量','Body mass'),tr('性别','Sex')];values=[int(missing[c]) for c in fields]
    ax.barh(labels,values,color=['#2e6e91']*4+['#b7553d']);ax.invert_yaxis();ax.set(xlim=(0,13),xticks=range(0,13,2),xlabel=tr('缺失记录数（总数344）','Missing records (344 total)'),title=tr('a  每一列缺了多少','a  Missingness by column'));ax.grid(axis='x',alpha=.15)
    for i,v in enumerate(values):ax.text(v+.2,i,f'{v} / 344',va='center')
    ax=fig.add_subplot(gs[0,1]);incomplete=table.loc[table[fields].isna().any(axis=1),fields];matrix=incomplete.isna().to_numpy(dtype=int)
    ax.imshow(matrix,cmap=ListedColormap(['#e3ecea','#b7553d']),vmin=0,vmax=1,aspect='auto')
    for i in range(len(incomplete)):
        for j in range(5):ax.text(j,i,'NA' if matrix[i,j] else '✓',ha='center',va='center',color='white' if matrix[i,j] else '#286b5a',fontsize=12)
    ax.set(xticks=range(5),xticklabels=labels,yticks=range(len(incomplete)),yticklabels=incomplete.index,title=tr('b  缺失是否落在同一条记录','b  Which fields are missing together'))
    ax.tick_params(axis='x',labelsize=10);fig.suptitle(tr('保留观测身份，才能理解一个空格','A missing entry makes sense within its observation'),fontsize=17,weight='bold')
    save(fig,'missing-records')

    fig=plt.figure(figsize=(12.6,7.7),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.45,1],height_ratios=[1,1])
    ax=fig.add_subplot(gs[:,0])
    for species in SPECIES:
        sub=table.loc[table['species'].eq(species)].dropna(subset=['flipper_length_mm','body_mass_kg'])
        ax.scatter(sub['flipper_length_mm'].to_numpy(dtype=float),sub['body_mass_kg'].to_numpy(dtype=float),s=30,alpha=.65,color=COLORS[species],label=species)
    ax.scatter(selected['flipper_length_mm'].to_numpy(dtype=float),selected['body_mass_kg'].to_numpy(dtype=float),s=100,facecolors='none',edgecolors='#172b36',lw=1.5,label=tr('筛出的14条记录','14 selected records'))
    ax.axhline(4,color='#172b36',ls=':',lw=1);ax.set(xlabel=tr('鳍状肢长度 / mm','Flipper length / mm'),ylabel=tr('身体质量 / kg','Body mass / kg'),xlim=(170,235),ylim=(2.5,6.6),title=tr('a  同一行的两次测量组成一个点','a  Two measurements from one row form a point'));ax.legend(loc='upper left',fontsize=11);ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[0,1]);bins=np.arange(2500,6501,250)
    ax.hist(table['body_mass_g'].dropna().to_numpy(dtype=float),bins=bins,histtype='step',lw=2,color='#9aa9ac',label=tr('全部有效质量','All observed masses'))
    ax.hist(selected['body_mass_g'].to_numpy(dtype=float),bins=bins,color='#2e6e91',alpha=.75,label=tr('筛选结果','Selected'))
    ax.set(xlabel=tr('身体质量 / g','Body mass / g'),ylabel=tr('记录数','Records'),title=tr('b  阈值之外，还限定物种和岛屿','b  Species and island also determine selection'));ax.legend(fontsize=10);ax.grid(axis='y',alpha=.12)
    ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.text(0,.95,'Adelie  ∩  Dream  ∩  mass ≥ 4000 g',fontsize=13,weight='bold');ax.text(0,.74,tr('344条记录 → 14条满足全部条件','344 records → 14 meet every condition'),fontsize=13)
    ax.text(0,.54,tr('原始位置编号保留，例如：','Original-position labels remain, for example:'),fontsize=12)
    for i,(_,r) in enumerate(selected.head(4).iterrows()):ax.text(0,.37-i*.1,f"{r['record_id']}    {r['flipper_length_mm']} mm    {r['body_mass_g']} g",fontsize=12)
    save(fig,'linked-selection')
    summary={'dataset':'Palmer penguins, CC0','input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
             'raw_shape':list(raw.shape),'dtypes':{k:str(v) for k,v in raw.dtypes.items()},'missing_counts':{k:int(v) for k,v in missing.items()},
             'measurement_complete_rows':len(complete_measurements),'all_complete_rows':len(complete_all),
             'selected_count':len(selected),'selected_ids':selected_ids,'mass_observed_count':len(valid_mass),
             'mean_mass_g':mass_mean,'zero_filled_mean_mass_g':wrong_zero_mean,
             'first_record_mass_kg':float(table.loc['PG001','body_mass_kg']),
             'heaviest_record':ordered.iloc[0]['record_id'],'heaviest_mass_g':int(ordered.iloc[0]['body_mass_g']),
             'missing_record_ids':incomplete.index.tolist(),'year_counts':json.loads(counts.to_json(orient='index'))}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
```

After execution, `penguins_with_ids.csv` retains all 344 records with generated labels and the kilogram column. `selected_records.csv` contains the 14 selected records. `summary.json` records the original shape, column types, missing counts, usable record counts, and selected identifiers. The program also uses Python's standard CSV reader to count qualifying records independently and scalar arithmetic to check the mean observed mass. Agreement between two implementations using the same input helps verify conditions and indexing.

`dropna(subset=...)` explicitly identifies the fields needed for a selection. `notna().all(axis=1)` asks whether every listed field in one row has a value, combining several within-row Boolean entries into one decision per observation. The missingness figure uses a related operation: `isna().any(axis=1)` locates rows containing at least one missing entry. The words “all” and “any” retain their everyday meanings once we identify the row over which they operate.

The scatter plot takes flipper length and body mass from the same selected table before passing them to the plotting function. Dropping missing values separately from two columns and pairing what remains by position could combine measurements from different observations. In this particular dataset, the two fields happen to be absent in the same two rows. Selecting complete rows still establishes a pairing rule that remains correct when the data change. A plotted point needs to retain the observation it represents before we can interpret the relationship between its coordinates.

Reading a file and saving a result are also distinct stages. The code adds units and identifiers to a working table while preserving the supplied CSV. A later change to the threshold regenerates the selected table from the same starting records. This makes comparisons between selections easier to understand: a difference in output reflects the stated condition change, rather than a sequence of manual edits whose earlier effects are no longer visible.

The historical sampling figure uses `pd.crosstab` to form its count matrix. One category defines rows, another defines columns, and each cell counts records sharing both categories. Adelie with the year label 2007 gives 50 matching rows; it does not average the years or body measurements. This converts classification information into an inspectable table and prepares for grouping experimental records in the next chapter. The fact that a column is numerically stored does not by itself make its mean a useful answer.

## Move between the plot, conditions, and individual records

The interactive experiment contains the same 344 records as Python. Species and island can be selected independently, a mass threshold can be raised from “unrestricted,” and an optional condition requires all eight original fields to be complete. The page reports the selected record count, the number with both scatter coordinates, and missingness among selected records. Choosing a record updates its details and the highlighted point together. If the selected observation lacks a plotting measurement, its details retain NA and explain why it has no scatter point.

### Select from 344 records while retaining row identity

Grey points retain all records with plot coordinates; colours show the selection and an orange ring marks the inspected record.

[Figure: Scatter and missingness linked to record selection](https://ml-biomat.com/tutorials/python-scientific/p11/en/#P11-chart)

Begin with all records and select PG004. Species and year remain readable while lengths and mass are absent. Enable complete records: PG004 leaves the selection and the count becomes 333. Disable that condition, then choose Adelie, Dream, and 4000 g. The result contains 14 records, matching Python. Finally choose Gentoo with Torgersen Island. The set is empty because the file contains no records with that combination. Axes and background points remain visible, separating an empty result from a display problem.

With the table understood, cleaning becomes a matter of preserving measurement meaning: types correspond to their fields, conditions express a specific question, missing entries retain their interpretation, and points remain traceable to records. The next chapter moves from category summaries to material formulations and repeated readings. We will examine how multiple readings of one specimen contribute to a group average and whose measurements that average describes.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P11.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pandas: Read and write tabular data](https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html)

   Reading, inspecting types, and exporting

   BSD-3-Clause; original teaching code
2. [pandas: Select a subset of a DataFrame](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html)

   Column selection, Boolean conditions, and labels

   BSD-3-Clause
3. [pandas: Working with missing data](https://pandas.pydata.org/pandas-docs/version/3.0/user_guide/missing_data.html)

   Missing values, nullable types, and comparisons

   BSD-3-Clause
4. [Palmer penguins data](https://allisonhorst.github.io/palmerpenguins/)

   Public measurements, field definitions, and data license

   CC0 data; no artwork reproduced
5. [Gorman, Williams & Fraser (2014)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081)

   Field observations and measurement methods

   CC BY article; factual context
6. [McKinney (2010): Data Structures for Statistical Computing in Python](https://doi.org/10.25080/Majora-92bf1922-00a)

   Design history of labelled tables

   CC BY4.0 proceedings article
