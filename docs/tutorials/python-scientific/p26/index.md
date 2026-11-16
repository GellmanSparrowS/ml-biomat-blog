# 把实验结果做成可用的 Excel 报告

Source: https://ml-biomat.com/tutorials/python-scientific/p26/
Language: zh-CN

用带公式、单位、参数与图表的工作簿，把一次图像测量交到下一位读者手中。

## 一份报告要让下一位读者接得住

完成一轮图像测量后，Python 已经给出每个区域的像素数、面积和直径。把这些数字发给合作者时，对方往往还会继续做事：按条件筛选，检查某一行的计算，修改空间标定，或者把结果放进自己的汇总表。Excel 工作簿适合承担这种交流，因为它同时容纳表格、公式、参数和图。不过，一份表格能打开，与一份报告能继续使用，中间还隔着许多设计选择。数字应保留为可计算的数字，单位应有固定位置，参数应集中存放，图应连接到对应单元格，读者还应知道每一行究竟代表一个样本还是一次处理条件。

本章将 [显微图像测量](https://ml-biomat.com/tutorials/python-scientific/s01/) 中的实际结果制作成工作簿。输入包含同一幅真实细胞图在七个阈值、两种填孔设置下的 14 行测量，每行保存阈值、填孔状态与像素数。我们用 XlsxWriter 生成工作簿，再用 openpyxl 重新读取公式与保存的数值，核对表格是否保留了原先的科学含义。最终得到三个工作表：一个集中保存标定参数，一个呈现测量及图表，一个解释数据对象和计算规则。这个结构也适合材料测试、光谱拟合或模拟分析，只需换成对应的输入列和物理量。

默认标定为每像素 0.107 μm。阈值 122、填孔开启时的输入计数是 11746，工作簿显示面积 134.480 μm²、等效圆直径 13.085 μm。显示到小数点后三位让表格更容易阅读，内部保存的数值仍为完整计算结果。下面先看成品中的数值组织，再逐步理解为什么要这样安排。蓝色强调行用于帮助读者找到贯穿本章的算例，不承担“这一行更优”或“这一条件应被采用”的统计判断。

![从真实图像的阈值测量生成的工作簿数值预览；每行对应同一图像的一种处理条件，数值显示到三位小数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/9ffe2cb0af99d35607b41beb.svg?v=9ffe2cb0af99)

图 1从真实图像的阈值测量生成的工作簿数值预览；每行对应同一图像的一种处理条件，数值显示到三位小数。

## 电子表格的价值，在于看得见的计算关系

1979 年，Dan Bricklin 与 Bob Frankston 开发的 VisiCalc 将电子表格带到个人电脑上。它的重要变化是把格子之间的计算关系放到了可以直接查看、修改的屏幕里：某个输入变化后，与之相连的结果能够重新计算。过去手工改一张预算表，常常要沿着许多行列逐个修改；电子表格则把这种依赖保存下来。科学工作簿同样受益于这一点。显微镜标定发生修正时，面积和直径应沿着已定义的关系更新，而不需要读者猜测哪些数字曾经乘过一个尺度。

本章的依赖关系很短，却完整地展示了这个思想。`Parameters!B2` 保存像素边长；`Measurements` 中 C 列保存像素数，D 列由像素数和标定计算面积，E 列由面积计算等效圆直径。感叹号连接工作表名称和单元格地址，字母表示列，数字表示行。图中的箭头表达“这个数值需要那个输入”。一张依赖图不仅能帮助初学者读公式，也能揭示报告是否混入了来历不明的手工修改。

![原创单元格依赖图：共享参数、原始计数、面积和直径之间的引用。VisiCalc 的历史说明电子表格为何适合保存这种依赖。](https://ml-biomat.com/static/tutorials/python-scientific/figures/1f19448fec192dd1dd7dd3a9.svg?v=1f19448fec19)

图 2原创单元格依赖图：共享参数、原始计数、面积和直径之间的引用。VisiCalc 的历史说明电子表格为何适合保存这种依赖。

Python 与电子表格在这里形成互补。Python 负责读取整批记录、统一计算规则和检查输出，工作簿则给读者一个熟悉的查看与调整界面。对同一批数据，程序可以稳定地生成同样布局，避免每次导出后重复调整列宽、拖动公式和复制图表。把需要重复执行的部分写进程序，也使工作簿的设计本身成为可复用的研究工具。随后改变输入表，依然能够生成结构一致的报告。

## 先确定每一行是什么，再设计三个工作表

本例每一行描述同一图像的一组处理条件。阈值 120 和阈值 122 对应不同的边界选择，填孔开关对应不同的区域定义；它们共享同一个细胞图像。因此，将这 14 行求平均，并把行数当成 14 个独立细胞，会改变数据原本的含义。工作簿在说明页中直接交代行的身份，条件表也保留阈值和填孔列。研究者可以据此查看处理敏感性，之后再为多个细胞、视野或实验批次增加相应的身份列。

参数表把所有结果共同依赖的量集中存放。像素边长只出现一次，单位写在相邻列中，单元格采用浅蓝色背景，提示这是可以调整的输入。条件表保留原始计数，并将面积和直径放在后面的计算列，读者顺着一行就能看到从输入走向结果的顺序。说明页则回答三个实际问题：图像是什么，区域怎样定义，公式怎样计算。这样的分工让正文表保持紧凑，又为需要追问细节的人保留了入口。

表头中的单位应固定且清楚。本例把 `Area / um^2` 和 `Equivalent diameter / um` 写进列标题，单元格只保存数值。若把“134.480 μm²”连同单位一起写成文本，排序和进一步计算就需要先拆分字符串。填孔列使用真正的布尔值，阈值和像素数使用整数，面积和直径保存浮点结果。数据类型与对象含义对应后，筛选、公式引用和其他程序读取都更直接。对于“无此指标”的情况，应保留明确的空值或状态，而不是用 0 代替。

冻结窗格使读者滚动时仍能看见表头和条件列；结构化表格提供一致的行格式与筛选按钮；适当列宽避免单位被截断。它们都是围绕使用动作设计的界面功能。颜色集中用于输入、表头和当前关注行，数字列按同一精度显示，图中的坐标和表格中的单位相互对应。这样读者可以连续完成“筛选一组条件—检查输入—阅读计算结果—在图中定位”的动作。

## 写下公式，同时解释公式怎样依赖输入

面积的计算从最简单的几何关系开始：一个像素对应一个小方格，区域面积等于方格数量乘以每个方格的面积。设像素边长为 s，选中像素数为 N，得到的面积记为 A。这里的平方来源于两个空间方向各乘一次长度标定；它不是一种为了配合软件而添加的写法。将这条关系翻译成电子表格，就得到 `=C7*Parameters!$B$2^2`。等号表示公式，星号表示乘法，`^2` 表示平方，C7 指向本行计数，参数表的 B2 指向全表共用的标定。

$$
A=N s^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选中投影区域的面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 掩膜中为真的像素个数，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 正方形像素边长对应的实际距离，μm/像素 |

每个像素占据边长为 s 的小方格，面积为 s²；N 个选中方格的面积相加得到 A。平方表示一个数乘以自身。本例 s=0.107 μm，N=11746，因此 A=11746×0.107×0.107=134.479954 μm²。公式采用两个方向间隔相同的像素；若两个方向标定不同，应分别相乘。

美元符号固定单元格地址中的列与行。在 Excel 中复制公式时，`C7` 会随目标行移动，而 `$B$2` 保持不变。于是下一行能够自动使用自己的像素数，同时继续引用同一个标定。这个相对引用与绝对引用的区别，决定了批量公式是否正确。示例由 Python 为每一行写出明确公式，并保留绝对参数地址；读者随后在工作簿里复制公式时，也能得到符合预期的依赖关系。

等效圆直径来自“找一个与当前区域面积相同的圆”。圆面积除以圆周率后得到半径的平方，开平方得到半径，再乘二得到直径。在工作簿里，它写成 `=2*SQRT(D7/PI())`，其中 `SQRT` 是平方根，`PI()` 返回圆周率，D7 是已经计算的面积。这样的写法让直径显式依赖面积，读者无需再次追踪最初的像素计数。公式中的函数名使用文件格式要求的英文名称，工作表界面的显示语言可以另外设置。

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | 与区域等面积的圆的直径，μm；eq 表示等效 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选中区域面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约 3.14159，无量纲 |

圆面积等于圆周率乘半径的平方，因此面积除以圆周率再开平方得到半径，乘 2 得到直径。根号取非负平方根。本例 A=134.479954 μm²，A/π≈42.8063 μm²，平方根约 6.54265 μm，直径约 13.0853 μm。等效圆直径描述面积尺度，并不要求对象真的是圆。

改变标定时，面积按尺度的平方变化，直径按尺度线性变化。下图固定像素数为 11746，只改变像素边长，展示两种依赖。曲线的不同形状是物理定义带来的结果：面积承担两个长度方向，直径承担一个长度方向。工作簿中的参数、公式与图因而形成一条可以讲清楚的计算链。以后加入厚度、体积或质量等量时，也可以先写清单位关系，再翻译成单元格公式。

![固定选中像素数 11746，面积随像素边长的平方变化，等效直径随边长线性变化。](https://ml-biomat.com/static/tutorials/python-scientific/figures/abe5773b367bdd7754577c9c.svg?v=abe5773b367b)

图 3固定选中像素数 11746，面积随像素边长的平方变化，等效直径随边长线性变化。

## 完整程序：生成带公式和图表的工作簿

XlsxWriter 适合从一组确定的数据生成新的 XLSX 文件。程序通过 `Workbook` 建立工作簿，添加三个工作表，再依次写入文本、数字、布尔值和公式。不同类型使用对应的写入函数，使输入在文件中保持应有的类型。`with` 语句在代码块结束时完成保存与关闭，确保工作簿内部的各部分写入完毕之后，后面的读取检查才开始执行。输出目录由运行参数指定，输入表则相对于示例文件定位。

### 生成科学工作簿并读回检查

XlsxWriter 写入类型明确的数据、公式、缓存结果与图表；openpyxl 分别读取公式和保存值，检查全部 14 行。

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

绘图数据也有明确的单元格来源。程序在参数表下方整理填孔开启的七组面积，使用公式引用测量表的对应行，再将这些连续单元格交给散点图。横轴是真正的数值阈值，纵轴是面积，因此相邻阈值的间距在图上具有实际含义。选择数值散点图能够避免把阈值 120、122 和 140 当作三个等距类别。图题写“阈值敏感性”，说明曲线反映的是同一图像的处理选择。

这份程序还为标定单元格加入数据验证，要求输入正数。这个规则来自空间尺度的定义：零或负的像素边长无法表达当前测量。界面验证帮助读者在编辑时发现输入问题，Python 中的计算检查则保障程序生成时的数值一致。两层检查作用于不同入口，彼此配合。对于更复杂的报告，可以进一步验证样本编号、日期范围和类别，但每一条规则都应与实际数据对象对应。

## 公式、保存的结果和重新计算，分别发生在哪里

电子表格文件可以同时保存公式文本与上次计算的结果。XlsxWriter 负责写出公式，并允许我们提供这个结果；它本身不运行 Excel 的公式计算引擎。示例因此先用 Python 根据同一物理关系计算面积与直径，再把数值作为公式的缓存结果写入。这样，读取缓存的程序和预览界面能够直接显示合理数值，能够计算公式的电子表格软件则可以在参数变化后重新计算。清楚区分这两种职责，才能准确解释一个自动生成的工作簿为什么能显示数字，以及修改参数后由谁负责更新它们。

openpyxl 的 `data_only=False` 模式读出公式文本，例如 `=C7*Parameters!$B$2^2`；`data_only=True` 模式读出文件中已保存的缓存值。后一个选项并没有要求 openpyxl 执行公式。本章用这两种模式打开同一个输出文件，分别检查公式指向正确的输入，以及缓存值与 Python 的独立计算相符。随后关闭只读工作簿，不再用读取工具重新保存它，从而保持原先写入的公式与缓存结构。

格式化同样要与计算分开。数字格式 `0.000` 决定显示三位小数，不会把内部数据改成三位小数。反过来，先对结果做取整再写入，会真的改变后续公式的输入。面积 134.479954 显示为 134.480 时，计算等效直径仍应使用完整面积，才能避免把展示精度传播成计算误差。在较长的计算链中，这种区分尤其有用：保存足够精度供后续计算，显示适合当前读者的精度。

最终检查覆盖 14 行的面积公式、面积缓存和直径缓存，并确认填孔列仍然是布尔类型。摘要记录工作表名称、行数、公式数量与代表行的实际结果。它们回答的是文件经过写出与重新读取之后是否保留了所设计的结构。日后修改报告布局时，只要保留同样的科学检查，就能更有把握地调整视觉样式，而不误改计算含义。

## 在一个视图里观察标定、公式和结果

下面的交互保留了工作簿的核心关系。选择阈值与填孔状态后，表格定位到相应条件；调整像素边长后，公式代入、面积曲线和等效圆会同步更新。像素计数始终来自已经完成的真实图像测量，改变标定只改变像素所代表的实际尺寸。圆形视图使用当前面积对应的等效圆，帮助直观看出同一计数在不同空间标定下怎样变化。

### 从输入单元格追踪面积变化

[Figure: 阈值面积曲线与选中条件](https://ml-biomat.com/tutorials/python-scientific/p26/#P26-chart)

[Figure: 按当前标定换算的等效圆](https://ml-biomat.com/tutorials/python-scientific/p26/#P26-circle)

| 阈值 | 像素数 | 面积 / μm² | 等效直径 / μm |
| --- | --- | --- | --- |

先保持阈值 122，把像素边长从 0.107 调为 0.120 μm。计数仍是 11746，面积变为 169.1424 μm²，等效直径随之增加。再恢复标定，只改阈值，你会看到输入计数本身发生变化。两种操作都能改变最终面积，却来自不同环节：前者改变尺度解释，后者改变图像中被选中的区域。把参数与结果放在一起，能够帮助读者追踪变化的原因，而不是只看到表格里的数字在跳动。

页面中的计算使用明确展示的算式，帮助理解工作簿依赖；运行示例生成的 XLSX 则保存对应的实际单元格公式和初始结果。课堂上可以先用交互确认某个条件的预期数值，再打开工作簿查看相同单元格的引用方式。对报告作者来说，这也是一种有用的检查习惯：先建立容易手算的代表条件，再核对文件中的公式和数值。

## 从一次导出走向稳定的报告模板

把这个流程用于自己的实验时，先列出读者需要完成的动作，再决定工作表结构。例如拉伸测试报告可能需要试样编号、截面积、载荷与应变；光谱报告可能需要波长、处理条件和拟合参数。把可以直接保存的原始量与需要公式计算的派生量分开，给共有参数保留单独位置，并让每张图连接到一段明确数据区域。这样，工作簿的布局由研究对象和使用动作驱动，增加装饰也不会替代必要解释。

当记录很多时，电子表格可以保存便于交流的汇总与代表性明细，完整原始数据则保留在适合程序读取的文件中。说明页列出对应数据文件名、字段定义和分析入口，让合作者能够沿着结果继续查找。某些读者只需要一页清楚的摘要，另一些读者要检查某个样本；将这些需求分配到不同工作表，可以同时保留可读性和追溯能力。

报告程序值得与分析程序一起保存。输入字段、公式、格式和图表都写在代码中，新一批数据进入后即可生成结构一致的工作簿，再执行相同的读回检查。后续 [程序检查与复用](https://ml-biomat.com/tutorials/python-scientific/p27/) 将把这些代表性条件进一步写成自动测试。最终交到读者手中的表格既能直接使用，也保留了从原始计数到科学结果的完整关系。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P26.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [XlsxWriter: Tutorial 1](https://xlsxwriter.readthedocs.io/tutorial01.html)

   新建工作簿、工作表及逐类型写入的开源教程基础。

   Software: BSD-2-Clause; original tutorial adaptation.
2. [XlsxWriter: Working with Formulas](https://xlsxwriter.readthedocs.io/working_with_formulas.html)

   公式文本、缓存值、重算与英文函数名的实际行为。

   Official technical documentation.
3. [openpyxl Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)

   工作簿、单元格类型与读取模式。

   Software: MIT; official documentation reference.
4. [Computer History Museum: Software, Putting PCs to Work](https://www.computerhistory.org/revolution/personal-computers/17/305)

   1979 年 VisiCalc 与可见电子表格的历史背景。

   Historical reference; original dependency diagram.
5. [scikit-image cell image](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)

   输入测量对应的真实图像与空间标定。

   Original image CC0; numerical derivative measurements supplied with the example.
