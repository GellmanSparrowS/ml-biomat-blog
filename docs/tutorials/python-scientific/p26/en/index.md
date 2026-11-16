# Building a Useful Excel Report from Results

Source: https://ml-biomat.com/tutorials/python-scientific/p26/en/
Language: en

Turn an image measurement into a workbook with formulas, units, parameters, and charts that another reader can use.

## A report should support its next reader's work

After an image-analysis run, Python has produced pixel counts, areas, and diameters. A collaborator receiving those results may want to filter conditions, inspect a calculation, revise spatial calibration, or place the results in a larger table. An Excel workbook supports this exchange because it can contain data, formulas, parameters, and charts together. Designing a usable report means keeping numbers numeric, giving units a consistent location, collecting shared parameters, linking charts to cells, and explaining whether a row represents a specimen or a processing condition.

This chapter builds a workbook from the actual results in [Measuring Structure in Microscopy Images](https://ml-biomat.com/tutorials/python-scientific/s01/en/). The input contains fourteen measurements of the same real cell image: seven thresholds combined with two hole-filling settings. Each row retains threshold, hole treatment, and pixel count. XlsxWriter creates the workbook, and openpyxl reads back its formulas and stored values to check that the file preserves the intended scientific meaning. Three worksheets separate calibration parameters, measurements with a chart, and explanations of the data and calculation rules. The same structure can support materials tests, spectral fits, or simulation results with different input columns and quantities.

The default calibration is 0.107 μm per pixel. At threshold 122 with holes filled, the input count is 11746. The workbook displays an area of 134.480 μm² and an equivalent-circle diameter of 13.085 μm. Three decimal places make the table readable, while the full calculated values remain stored internally. The highlighted row identifies the example followed throughout the chapter; its color carries no statistical claim that this condition is preferable.

![Workbook-value preview generated from threshold measurements of the real image. Each row is a condition applied to one image; values display three decimal places.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e76f716fbdf7bc98cfc4393d.svg?v=e76f716fbdf7)

Figure 1Workbook-value preview generated from threshold measurements of the real image. Each row is a condition applied to one image; values display three decimal places.

## The useful feature of a spreadsheet is a visible dependency

In 1979, VisiCalc, developed by Dan Bricklin and Bob Frankston, brought the electronic spreadsheet to personal computers. A central change was to place dependencies between cells on a screen where people could inspect and edit them. When an input changed, connected results could be recalculated. Editing a paper budget required tracing corrections through its rows and columns; an electronic spreadsheet retained those relationships. A scientific workbook uses the same idea. Revising a microscope's calibration should update the dependent areas and diameters through defined relationships, without asking the reader to guess which numbers contain a scale conversion.

The dependency chain here is short enough to inspect completely. `Parameters!B2` stores pixel side length. In `Measurements`, column C stores pixel count, column D calculates area from the count and calibration, and column E calculates equivalent-circle diameter from area. An exclamation mark separates a worksheet name from a cell address; the letter identifies a column and the number identifies a row. Arrows in the diagram mean that one quantity needs another input. Such a diagram helps a beginner read formulas and exposes values that have been changed manually without a recorded relationship.

![Original cell-dependency diagram connecting a shared parameter, count, area, and diameter. The VisiCalc history explains the value of retaining these relationships.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9ce96cc6a4cdbc8db230ec97.svg?v=9ce96cc6a4cd)

Figure 2Original cell-dependency diagram connecting a shared parameter, count, area, and diameter. The VisiCalc history explains the value of retaining these relationships.

Python and the spreadsheet contribute complementary capabilities. Python reads a batch of records, applies consistent rules, and checks the output. The workbook gives another reader a familiar interface for inspection and adjustment. A program can repeatedly produce the same arrangement without manual column resizing, formula dragging, or chart copying. Encoding those repeated actions makes the report design itself reusable: a new input table can enter the same process and produce a report whose organization remains consistent.

## Define the row before designing the worksheets

Each row in this example describes a processing condition applied to one image. Thresholds 120 and 122 select different boundaries, and the hole switch changes the region definition, while the underlying cell image remains the same. Averaging the fourteen rows and treating them as fourteen independent cells would change the identity of the observations. The Readme worksheet states the row definition directly, and the measurement table retains threshold and hole-treatment columns. These records support a sensitivity analysis. A study involving multiple cells, fields of view, or experimental batches would add the corresponding identifiers.

The parameter sheet collects quantities shared by all results. Pixel spacing appears once, with its unit alongside it and a pale blue background identifying an adjustable input. The measurement sheet preserves the original count and places derived area and diameter in subsequent columns, so reading across a row follows the calculation. The explanation sheet answers practical questions about the image, region definition, and formulas. Separating these roles keeps the main table compact while giving a reader access to the details needed to interpret it.

Units belong in stable, visible locations. The headers `Area / um^2` and `Equivalent diameter / um` identify units while the cells retain numerical values. Writing a combined string such as “134.480 μm²” would require string parsing before subsequent numerical work. Hole treatment is stored as a Boolean value; thresholds and counts are integers; derived quantities retain their floating-point values. Matching types to meanings makes filtering, formula references, and programmatic reading straightforward. A missing or inapplicable quantity should retain an explicit missing state rather than being replaced by zero.

Frozen panes keep headers and condition columns visible during scrolling. A structured table supplies consistent row formatting and filters. Suitable column widths keep units readable. These interface features support concrete actions: select a condition, inspect its input, read the result, and locate it in a figure. Color is reserved for inputs, headers, and the representative row, while numerical columns use consistent display precision and the chart uses the same physical units as the table.

## Write formulas that expose their inputs

Area starts from a geometric relationship: each pixel represents a small square, and the region's area is the number of squares multiplied by the area of one square. Let s denote pixel side length, N the selected pixel count, and A the resulting area. The square of the scale factor comes from applying a length calibration in both spatial directions. Translating this into a spreadsheet gives `=C7*Parameters!$B$2^2`. The equals sign introduces a formula, the asterisk multiplies, `^2` squares a value, C7 supplies the count from this row, and the parameter cell supplies the shared calibration.

$$
A=N s^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | area of the selected projected region, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | number of true pixels in the mask, dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | physical side length of one square pixel, μm per pixel |

Each square pixel has area s², and summing N selected squares gives A. Squaring means multiplying a value by itself. With s=0.107 μm and N=11746, A=11746×0.107×0.107=134.479954 μm². Equal spacing in both directions is assumed; unequal spacings are multiplied separately.

Dollar signs fix the column and row components of a cell address. When a formula is copied in Excel, `C7` shifts relative to its destination, while `$B$2` stays fixed. The next row therefore uses its own count and the same calibration. Relative and absolute references determine whether copied formulas preserve their meaning. Python writes explicit formulas for every row in this example, retaining the absolute parameter address so that later copying within the workbook also follows the intended relationship.

Equivalent-circle diameter asks for a circle with the same area as the measured region. Dividing area by π gives radius squared, taking the square root gives radius, and multiplying by two gives diameter. The spreadsheet expression is `=2*SQRT(D7/PI())`: `SQRT` evaluates the square root, `PI()` supplies π, and D7 contains area. This expression makes diameter visibly depend on area, rather than requiring a reader to reconstruct its relationship to the original count. Formula function names follow the English names required by the file format, independently of the spreadsheet application's interface language.

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | diameter of an equal-area circle, μm; eq denotes equivalent |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | selected region area, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | circle constant, approximately 3.14159, dimensionless |

Circle area is π times radius squared. Divide area by π, take the nonnegative square root to obtain radius, then multiply by two. For A=134.479954 μm², A/π≈42.8063 μm², radius≈6.54265 μm, and diameter≈13.0853 μm. The quantity describes an area scale without requiring a circular object.

Changing calibration changes area quadratically and diameter linearly. The next figure fixes the count at 11746 while varying pixel side length. Its two curve shapes follow the definitions: area involves two spatial directions and diameter is a length. Parameters, formulas, and figures consequently form an explainable calculation chain. Additional quantities such as thickness, volume, or mass can be introduced in the same way: establish their unit relationships before translating them into cell formulas.

![At a fixed count of 11746 pixels, area varies quadratically with spacing and equivalent diameter varies linearly.](https://ml-biomat.com/static/tutorials/python-scientific/figures/4c583e9c32bc5b647425e308.svg?v=4c583e9c32bc)

Figure 3At a fixed count of 11746 pixels, area varies quadratically with spacing and equivalent diameter varies linearly.

## The complete program: formulas, typed values, and a chart

XlsxWriter is suited to generating a new XLSX file from a defined collection of data. The program creates a `Workbook`, adds three worksheets, and writes text, numbers, Boolean values, and formulas using their corresponding methods. Keeping types explicit preserves the intended representation inside the file. A `with` block completes writing and closes the workbook before the readback checks begin. The output directory is a command-line parameter, and the input table is located relative to the example script.

### Generate a scientific workbook and verify it by readback

XlsxWriter writes typed data, formulas, cached results, and a chart. openpyxl separately reads formulas and stored values to check all fourteen rows.

```
"""Create and independently read back a calibrated microscopy workbook.

Input pixel counts are measurements of the CC0 skimage.data.cell image using
the S01 threshold/connected-region pipeline. Rows vary processing parameters
on the same image; they are not independent biological replicates.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import zipfile
import numpy as np
import xlsxwriter
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def create_workbook(rows, output, spacing):
    path = output / "microscopy-report.xlsx"
    with xlsxwriter.Workbook(path) as workbook:
        inputs = workbook.add_worksheet("Parameters")
        data = workbook.add_worksheet("Measurements")
        notes = workbook.add_worksheet("Readme")
        number = workbook.add_format({"num_format": "0.000", "font_color": "#172534"})
        parameter = workbook.add_format({"num_format": "0.000", "bg_color": "#e7f1f6", "border": 1})
        header = workbook.add_format({"bold": True, "font_color": "#205b8c", "text_wrap": True})
        inputs.write_row(0,0,["Parameter", "Value", "Unit"],header)
        inputs.write(1,0,"Square-pixel side length");inputs.write_number(1,1,spacing,parameter);inputs.write(1,2,"um / pixel")
        inputs.data_validation("B2",{"validate":"decimal","criteria":">","value":0,
                                     "input_title":"Calibration", "input_message":"Positive micrometres per pixel",
                                     "error_type":"stop","error_message":"Use a positive pixel spacing."})
        inputs.set_column("A:A",32);inputs.set_column("B:C",19);inputs.freeze_panes(1,0)
        headers=["Threshold","Fill holes","Pixels","Area / um^2","Equivalent diameter / um"]
        for i,row in enumerate(rows,start=1):
            excel=i+1
            data.write_number(i,0,row['threshold']);data.write_boolean(i,1,row['fill_holes'])
            data.write_number(i,2,row['pixels'])
            data.write_formula(i,3,f"=C{excel}*Parameters!$B$2^2",number,row['area_um2'])
            data.write_formula(i,4,f"=2*SQRT(D{excel}/PI())",number,row['diameter_um'])
        data.add_table(0,0,len(rows),4,{"name":"RegionMeasurements","style":"Table Style Medium 2",
                                                  "columns":[{"header":h} for h in headers]})
        data.freeze_panes(1,3);data.set_column("A:C",16);data.set_column("D:E",29)
        chart=workbook.add_chart({"type":"scatter","subtype":"straight_with_markers"})
        # Interleaved filled/unfilled rows are written to separate linked columns.
        inputs.write_row(4,0,["Threshold","Area, holes filled / um^2"],header)
        filled=[(i,r) for i,r in enumerate(rows,start=2) if r['fill_holes']]
        for j,(excel,r) in enumerate(filled,start=5):
            inputs.write_number(j,0,r['threshold'])
            inputs.write_formula(j,1,f"=Measurements!D{excel}",number,r['area_um2'])
        chart.add_series({"name":"Same image; holes filled","categories":["Parameters",5,0,4+len(filled),0],
                          "values":["Parameters",5,1,4+len(filled),1],"line":{"color":"#205b8c"},
                          "marker":{"type":"circle","size":5}})
        chart.set_title({"name":"Threshold sensitivity"});chart.set_x_axis({"name":"Intensity threshold"})
        chart.set_y_axis({"name":"Projected area / um^2"});chart.set_legend({"none":True})
        data.insert_chart("G2",chart,{"x_scale":1.2,"y_scale":1.15})
        messages=["Image: skimage.data.cell; data license CC0; Mueller et al. 2018, doi:10.1364/OE.26.010729.",
                  "Each row is one processing condition on the same image, not a biological replicate.",
                  "Pixels: largest eight-connected region with intensity strictly above threshold.",
                  "Fill holes: fill enclosed background after selecting the largest component.",
                  "Area = pixel count * square-pixel spacing squared; diameter = 2*sqrt(area/pi).",
                  "Formulas include cached values independently calculated in Python.",
                  "Editing Parameters!B2 updates dependent cells when a spreadsheet engine recalculates.",
                  "openpyxl reads formula text or cached results; it does not calculate formulas.",
                  "Original measurement workflow: S01, Measuring Structure in Microscopy Images."]
        notes.set_column("A:A",115)
        for i,message in enumerate(messages):notes.write(i,0,message)
    return path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--language",choices=("zh","en"),default="en")
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';tr=lambda a,b:a if zh else b;spacing=.107
    with (HERE/'data/region-measurements.csv').open(encoding='utf-8',newline='') as f:
        rows=[{'threshold':int(r['threshold']),'fill_holes':bool(int(r['fill_holes'])),'pixels':int(r['pixels'])} for r in csv.DictReader(f)]
    for r in rows:
        r['area_um2']=r['pixels']*spacing**2;r['diameter_um']=2*math.sqrt(r['area_um2']/math.pi)
    path=create_workbook(rows,args.output,spacing)
    formulas=openpyxl.load_workbook(path,data_only=False,read_only=True)
    cached=openpyxl.load_workbook(path,data_only=True,read_only=True)
    for i,r in enumerate(rows,start=2):
        assert formulas['Measurements'][f'D{i}'].value==f'=C{i}*Parameters!$B$2^2'
        assert math.isclose(cached['Measurements'][f'D{i}'].value,r['area_um2'],abs_tol=1e-10)
        assert math.isclose(cached['Measurements'][f'E{i}'].value,r['diameter_um'],abs_tol=1e-10)
    assert formulas['Measurements']['B2'].data_type=='b'
    sheetnames=formulas.sheetnames;formulas.close();cached.close()
    with zipfile.ZipFile(path) as z:assert 'xl/worksheets/sheet2.xml' in z.namelist()
    selected=next(r for r in rows if r['threshold']==122 and r['fill_holes'])
    summary={'rows':len(rows),'spacing_um':spacing,'sheet_names':sheetnames,'formula_count':len(rows)*2+7,
             'readback_rows_checked':len(rows),'selected':selected,'calculation_engine':'Python cached values; Excel-compatible formulas'}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    (args.output/'lab-data.json').write_text(json.dumps({'rows':rows,'spacing_um':spacing}),encoding='utf8')
    plt.rcParams.update({'font.family':available_plot_fonts(),'font.size':12,'svg.fonttype':'none',
                         'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',metadata={'Date':None})
        fig.savefig(args.output/f'{name}-{args.language}.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(12.4,5.1),layout='constrained');ax.axis('off')
    header=[tr('阈值','Threshold'),tr('填孔','Fill holes'),tr('像素数','Pixels'),tr('面积 / μm²','Area / μm²'),tr('直径 / μm','Diameter / μm')]
    show=[r for r in rows if r['fill_holes']]
    table=ax.table(cellText=[[r['threshold'],tr('是','Yes'),r['pixels'],f"{r['area_um2']:.3f}",f"{r['diameter_um']:.3f}"] for r in show],colLabels=header,cellLoc='right',loc='center',colWidths=[.13,.13,.18,.27,.27])
    table.auto_set_font_size(False);table.set_fontsize(13);table.scale(1,2)
    for (r,c),cell in table.get_celld().items():
        cell.set_edgecolor('#dce3e6');cell.set_facecolor('#205b8c' if r==0 else ('#e7f1f6' if r==3 else '#ffffff'))
        if r==0:cell.get_text().set_color('white')
    ax.set_title(tr('同一图像的处理条件表 · 原始计数与可追踪的计算列','Processing conditions for one image · counts and traceable calculations'),loc='left',pad=15)
    save(fig,'workbook-values')
    fig,axs=plt.subplots(1,2,figsize=(12.4,4.5),layout='constrained');ss=np.linspace(.07,.15,200);n=selected['pixels']
    axs[0].plot(ss,n*ss**2,color='#205b8c',lw=2);axs[1].plot(ss,2*np.sqrt(n*ss**2/np.pi),color='#b4482e',lw=2)
    for ax,value in zip(axs,[selected['area_um2'],selected['diameter_um']]):
        ax.axvline(spacing,color='#7e8d95',ls='--');ax.scatter([spacing],[value],color='#172534',zorder=4);ax.set_xlabel(tr('像素边长 / μm','Pixel side length / μm'));ax.grid(alpha=.15)
    axs[0].set(ylabel=tr('面积 / μm²','Area / μm²'),title=tr('A  面积随标定的平方改变','A  Area scales with calibration squared'))
    axs[1].set(ylabel=tr('等效圆直径 / μm','Equivalent-circle diameter / μm'),title=tr('B  长度随标定线性改变','B  Diameter scales linearly with calibration'))
    save(fig,'calibration-dependence')
    fig,ax=plt.subplots(figsize=(12.4,4.9),layout='constrained');ax.set(xlim=(0,12),ylim=(0,5));ax.axis('off')
    boxes=[(0.2,3.3,3.1,1.0,'Parameters!B2',tr('标定：0.107 μm/像素','Calibration: 0.107 μm/pixel')),(0.2,.8,3.1,1.0,'Measurements!C7','11746 pixels'),(4.6,2,3.1,1.2,'Measurements!D7','134.479954 μm²'),(8.7,2,3.1,1.2,'Measurements!E7','13.085305 μm')]
    for x,y,w,h,title,value in boxes:
        ax.add_patch(plt.Rectangle((x,y),w,h,facecolor='#e7f1f6' if title.startswith('Parameters') else '#fff',edgecolor='#8da5b4'))
        ax.text(x+.15,y+h-.30,title,fontsize=11,color='#205b8c');ax.text(x+.15,y+.25,value,fontsize=12)
    for start,end in [((3.3,3.8),(4.6,2.9)),((3.3,1.3),(4.6,2.3)),((7.7,2.6),(8.7,2.6))]:ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'#8da5b4','lw':2})
    ax.text(4.6,1.5,'=C7*Parameters!$B$2^2',fontsize=12,parse_math=False);ax.text(8.7,1.5,'=2*SQRT(D7/PI())',fontsize=12,parse_math=False)
    ax.set_title(tr('从 VisiCalc（1979）到科学工作簿：保留单元格之间的依赖','From VisiCalc (1979) to a scientific workbook: preserve cell dependencies'),loc='left',fontsize=15)
    save(fig,'cell-dependencies')
    print(json.dumps(summary))


if __name__=='__main__':main()
```

The chart's values have explicit cell sources too. Below the parameter block, the program collects the seven hole-filled area values through formulas referencing the corresponding measurement rows. These consecutive cells supply a scatter chart. Its horizontal axis is numerical threshold and its vertical axis is area, so the unequal intervals between 120, 122, and 140 retain their numerical meaning. A categorical chart could place those three thresholds at equal distances. The title “Threshold sensitivity” identifies the question answered by the curve: how processing choices affect this one image.

The calibration cell has data validation requiring a positive number, a rule derived from the physical definition of pixel spacing. Zero or a negative side length cannot describe the present spatial measurement. This interface check helps someone editing the workbook, while the Python checks establish consistency when the workbook is generated. Together, they cover initial generation and later editing. More elaborate reports can validate sample identifiers, date ranges, or allowed categories in the same way, with each rule attached to a particular data meaning.

## Distinguish the formula, the saved value, and recalculation

A spreadsheet file can retain both formula text and a previously calculated result. XlsxWriter writes formulas and lets the author provide that result; it does not run Excel's calculation engine. The example therefore calculates area and diameter independently in Python and supplies those values as formula caches. A reader or preview tool that reads cached results can display the values immediately. A spreadsheet application with a calculation engine can subsequently recalculate dependent cells after a parameter changes. Distinguishing those roles explains both why an automatically generated workbook displays meaningful numbers and which component updates them after editing.

With `data_only=False`, openpyxl reads formula text such as `=C7*Parameters!$B$2^2`. With `data_only=True`, it reads the cached result already present in the file. The latter option does not ask openpyxl to execute a formula. We open the same output in both modes, checking that formulas reference the intended inputs and that caches match independent Python calculations. The read-only workbooks are then closed without saving them again, preserving the formulas and cached representation written by XlsxWriter.

Formatting also has a separate role from calculation. The number format `0.000` displays three decimal places while retaining the underlying value. Rounding a result before writing it would change the input available to later formulas. When 134.479954 is displayed as 134.480, diameter should still use the full area value. This prevents display precision from being propagated as a calculation error. Longer calculation chains benefit from the same practice: retain sufficient numerical precision for subsequent work and choose display precision for the reader's immediate task.

The readback checks cover all fourteen area formulas, all fourteen area caches, all fourteen diameter caches, and the Boolean type of hole treatment. The summary records worksheet names, row count, formula count, and the representative result. These checks establish whether writing and rereading preserved the designed structure. They can remain in place when the report's visual layout changes, allowing presentation to improve while its scientific relationships remain inspectable.

## Inspect calibration, formulas, and results together

The interactive workspace retains the workbook's central relationships. Selecting threshold and hole treatment locates a condition in the table. Changing pixel side length updates the substituted formula, area curve, and equivalent circle together. Pixel counts always come from the completed measurements of the real image. Calibration changes the physical size assigned to each pixel. The circle represents the current equal-area diameter, making the consequences of a spatial scale change easier to see.

### Track area changes from the input cells

[Figure: Area versus threshold and selected condition](https://ml-biomat.com/tutorials/python-scientific/p26/en/#P26-chart)

[Figure: Equal-area circle at the current calibration](https://ml-biomat.com/tutorials/python-scientific/p26/en/#P26-circle)

| Threshold | Pixels | Area / μm² | Equivalent diameter / μm |
| --- | --- | --- | --- |

Keep threshold at 122 and change spacing from 0.107 to 0.120 μm. The count remains 11746, while area becomes 169.1424 μm² and diameter increases. Restore the calibration and change the threshold instead: this time the input count changes. Both actions alter area, but at different points in the workflow. One revises the spatial interpretation; the other changes which image region is selected. Showing parameters alongside results helps a reader identify the cause of a numerical change.

The page uses the displayed mathematical expressions to explain workbook dependencies. The XLSX generated by the example stores corresponding cell formulas and initial results. A useful exercise is to establish an expected value in this workspace and then inspect the same calculation in the workbook. For a report author, this is also a practical verification habit: choose a representative condition that can be calculated independently and compare it to the formulas and values written into the file.

## Develop a stable report template

When adapting the workflow to another experiment, begin with the actions its reader needs to perform. A tensile-test report might require specimen identifiers, cross-sectional areas, forces, and strains; a spectral report might require wavelengths, treatment conditions, and fitted parameters. Separate directly recorded quantities from derived quantities, give shared parameters their own location, and connect each chart to an explicit data range. The organization then follows the research object and its use, while visual styling supports the explanation.

For a large collection, a workbook can contain useful summaries and representative details while complete raw data remain in files suited to programmatic reading. The explanation sheet can identify those files, define fields, and identify the analysis script. Some readers need a concise summary; others need to inspect a particular specimen. Assigning those needs to separate worksheets preserves both readability and traceability.

Save the report program alongside the analysis. Input fields, formulas, formats, and charts are all specified in code, so a new batch can produce a consistently organized workbook and pass through the same readback checks. [Making Analysis Programs Testable and Reusable](https://ml-biomat.com/tutorials/python-scientific/p27/en/) turns representative conditions into automated tests. The resulting report is useful immediately and retains the complete relationship between recorded counts and scientific quantities.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P26.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [XlsxWriter: Tutorial 1](https://xlsxwriter.readthedocs.io/tutorial01.html)

   Open tutorial foundation for workbooks, worksheets, and typed cell writing.

   Software: BSD-2-Clause; original tutorial adaptation.
2. [XlsxWriter: Working with Formulas](https://xlsxwriter.readthedocs.io/working_with_formulas.html)

   Formula text, cached values, recalculation, and English function names.

   Official technical documentation.
3. [openpyxl Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)

   Workbooks, cell types, and loading modes.

   Software: MIT; official documentation reference.
4. [Computer History Museum: Software, Putting PCs to Work](https://www.computerhistory.org/revolution/personal-computers/17/305)

   Historical context for VisiCalc and visible spreadsheets in 1979.

   Historical reference; original dependency diagram.
5. [scikit-image cell image](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)

   Real image and spatial calibration underlying the input measurements.

   Original image CC0; numerical derivative measurements supplied with the example.
