# Making Analysis Programs Testable and Reusable

Source: https://ml-biomat.com/tutorials/python-scientific/p27/en/
Language: en

Use hand-checkable geometry, explicit input definitions, and executed tests to make an area calculation reusable.

## How can the original calculation remain valid after an edit?

An analysis program often starts with one immediate task: read an image, select a region, and calculate its area. Later, it processes dozens of images with different pixel spacings and supplies values to a report. As the program becomes more useful, more behavior needs to remain consistent when it changes. Automated tests retain that behavior as repeatable conditions: a defined input should produce a particular result, and an input outside the function's definition should receive a clear response. Checks that once depended on memory, hand calculations, and temporary print statements can then remain with the program.

This chapter develops a complete example around two-dimensional region area. The function takes a Boolean mask and two pixel spacings and returns area in μm². We begin with a rectangle whose answer is calculable on paper, then check an empty region, changes of scale, transposition, invalid calibration, and incorrect dimensions. The pytest file contains thirteen executed checks. Three deliberately changed implementations provide teaching comparisons: one omits a scale factor, one counts the entire array, and one omits input validation. Their different behavior appears in a diagnostic matrix, making the purpose of each condition visible.

Think of preparing known-size objects to check a ruler. Before measuring an unfamiliar specimen, a reference block helps establish that the ruler's scale and reading agree. A program benefits from reference objects too. A complex cell's exact area may be difficult to know independently, while a rectangle four pixels wide and three pixels high is straightforward. Establishing the calculation with simple geometry before applying it to complex objects supports both scientific understanding and program maintenance.

## Define the inputs and outputs

Before writing tests, decide what the function means. The mask is a two-dimensional Boolean array: true pixels belong to the selected region and false pixels are background. `spacing` contains two lengths in row-column order, both in μm. They may differ because imaging and resampling can have unequal intervals along the two axes. The output is the total physical area of selected pixels in μm². The mask already expresses a region selection, so thresholding belongs upstream; the area function converts an explicitly selected region into a physical quantity.

$$
A=N s_y s_x
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | two-dimensional selected area, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | number of true pixels, dimensionless count |
| ![Formula](https://ml-biomat.com/static/agent-math/8f5fc51f77ebba17af28d557.svg) | row-direction pixel spacing, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/d65997e80acc2ddac324815b.svg) | column-direction pixel spacing, μm |

One pixel is a rectangle with width s_x and height s_y. Multiplying those lengths gives its area; summing N selected pixels gives A. Twelve pixels with row spacing 0.2 μm and column spacing 0.3 μm give A=12×0.2×0.3=0.72 μm². Independent whole-object geometry gives width 1.2 μm and height 0.6 μm, whose product is also 0.72 μm².

The definition includes edge cases. An all-false mask describes an empty region whose area is zero. This differs from receiving an array that is not a two-dimensional image. A three-dimensional object requires three spacings and a volume definition, so the function reports a dimension error for a volume. A raw intensity array also differs from a Boolean mask: counting all its nonzero values could include many ordinary background pixels. Requiring Boolean membership asks the caller to make the region selection explicit before measurement. These checks address inputs that would otherwise change the scientific meaning.

Both spacings must be finite and strictly positive. Zero and negative values do not describe the pixel side lengths used here, and NaN or infinity cannot participate in an ordinary finite area calculation. The function raises `ValueError` for such values and `TypeError` for an incorrect mask type. The exception name and short message help the caller identify what to repair. In batch processing, an image identifier and error description can be recorded together, allowing calibration or array shape to be examined for that particular input.

### Scientific function: area from a region and calibration

The function explicitly defines types, dimensions, units, and invalid-calibration behavior.

```
"""A small scientific function with an explicit input and unit contract."""
import numpy as np


def mask_area(mask, spacing):
    """Return selected 2D area in um^2 for (row, column) spacing in um.

    A Boolean mask defines membership. Empty selections have area zero.
    Both physical spacings must be finite and strictly positive.
    """
    mask = np.asarray(mask)
    if mask.ndim != 2:
        raise ValueError("mask must have exactly two spatial dimensions")
    if mask.dtype != np.bool_:
        raise TypeError("mask must contain Boolean membership values")
    scale = np.asarray(spacing, dtype=float)
    if scale.shape != (2,) or not np.all(np.isfinite(scale)) or np.any(scale <= 0):
        raise ValueError("spacing must contain two finite positive lengths")
    return float(np.count_nonzero(mask) * scale[0] * scale[1])
```

## Prepare an object with an independent answer

The test rectangle sits inside an eight-row, ten-column background. Rows 2 through 4 and columns 1 through 4 are true. Python slices exclude their stopping index, so `mask[2:5, 1:5]` selects three rows and four columns: twelve pixels. With row spacing 0.2 μm and column spacing 0.3 μm, the rectangle is 0.6 μm high and 1.2 μm wide. Its geometric area is 0.72 μm². This expected value comes from width times height, independently of how the function counts pixels internally.

![Independent expectations from explicit geometry: twelve selected pixels within an eighty-pixel grid, with unequal directional spacings.](https://ml-biomat.com/static/tutorials/python-scientific/figures/4f3aaa4542ec64eab53d51af.svg?v=4f3aaa4542ec)

Figure 1Independent expectations from explicit geometry: twelve selected pixels within an eighty-pixel grid, with unequal directional spacings.

Keeping background around the rectangle makes the test more informative. If every input pixel were true, counting selected pixels and counting all array elements would agree, allowing an incorrect implementation to pass. The present array has eighty pixels but only twelve selected ones. Those two operations therefore have clearly different results. A test input is useful because of the behaviors it distinguishes, rather than simply because it contains many values. A small, targeted input can locate a problem more directly than a complicated image whose answer is unknown.

A calculated result may appear as `0.7200000000000001` because of floating-point representation. pytest's `approx` compares floating-point results within a tolerance, expressing agreement with the geometric expectation at a specified numerical precision. Counts can be compared exactly; floating-point multiplication and longer numerical methods need an appropriate tolerance. A tolerance wide enough to accept values such as 2.4 or 4.8 would hide scale or counting errors. Its size should therefore follow the numerical calculation and scientific definition.

The tests explicitly set relative tolerance `rel=1e-12` and absolute tolerance `abs=1e-12`. The relative allowance scales with the expected value at one part in a trillion; the absolute allowance has a scale of 10 to the power −12 μm². The comparison uses the larger allowance. For an expectation of 0.72 μm², the relative term is 0.72 times 10 to the power −12, so the absolute allowance determines the threshold. This accommodates rounding from the few double-precision multiplications here while remaining far smaller than a missing-scale error. A later approximate solver or numerical integral would need a tolerance chosen for that algorithm's accuracy.

## Retain a check as a repeatable object

The history of testing frameworks has produced useful divisions of responsibility. Python's standard `unittest` was inspired by JUnit and separates input preparation, individual cases, collections of cases, and their execution. Its documentation also links Kent Beck's early paper on Smalltalk testing patterns. The organization fits scientific code: prepare a reusable geometric object, express distinct properties as individual cases, and let an execution tool run and report them together. pytest provides concise function and assertion syntax within this tradition, making automated checks accessible to small analysis projects.

![The same rectangle connects independent geometry, an actual pytest failure excerpt, and the passing correct-function suite. The executed report reveals how omitting column spacing changes 0.72 to 2.4.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9b252a3754443b6dc16f3b7a.svg?v=9b252a375444)

Figure 2The same rectangle connects independent geometry, an actual pytest failure excerpt, and the passing correct-function suite. The executed report reveals how omitting column spacing changes 0.72 to 2.4.

Here, a fixture prepares the rectangle with background. Each test requesting it receives the same defined input. Functions whose names begin with `test_` state checks, and `assert` expresses the expected relationship. pytest discovers those functions, runs them, and identifies a failed assertion. A fixture avoids copying the array-construction code into several tests. The geometric object's definition remains in one place, making it easier to confirm that different checks refer to the intended input.

Parametrization lists several inputs for the same type of check. Zero spacing, negative spacing, nonfinite spacing, and an incorrect number of spacing values all violate the calibration definition. `pytest.mark.parametrize` runs one check function separately for each set of arguments. `pytest.raises(ValueError)` states that a call should reject the input explicitly. Raising the expected exception is the correct outcome in those cases. Successful testing therefore includes both a correct value for valid input and an appropriate response to invalid input.

### Checks of independent geometry, input boundaries, and invariants

Thirteen executed pytest checks use geometry and object definitions as expectations.

```
"""Expected values come from geometry and input definitions."""
import numpy as np
import pytest
from measurement import mask_area


@pytest.fixture
def rectangle():
    mask = np.zeros((8, 10), dtype=bool)
    mask[2:5, 1:5] = True
    return mask


def test_rectangle_geometry(rectangle):
    # Four columns × 0.3 um = 1.2 um; three rows × 0.2 um = 0.6 um.
    assert mask_area(rectangle, (.2, .3)) == pytest.approx(.72, rel=1e-12, abs=1e-12)


def test_empty_region():
    assert mask_area(np.zeros((4, 7), dtype=bool), (.2, .3)) == 0


def test_doubling_both_lengths_quadruples_area(rectangle):
    assert mask_area(rectangle, (.4, .6)) == pytest.approx(2.88, rel=1e-12, abs=1e-12)


def test_transpose_with_swapped_spacing(rectangle):
    assert mask_area(rectangle.T, (.3, .2)) == pytest.approx(.72, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("spacing", [(0, .3), (-.2, .3), (.2, float('nan')),
                                    (.2, float('inf')), (.2,), (.2, .3, .4)])
def test_reject_invalid_calibration(rectangle, spacing):
    with pytest.raises(ValueError):
        mask_area(rectangle, spacing)


@pytest.mark.parametrize("mask", [np.ones(5,dtype=bool), np.ones((2,3,4),dtype=bool)])
def test_reject_wrong_dimension(mask):
    with pytest.raises(ValueError):
        mask_area(mask, (.2, .3))


def test_reject_numeric_intensities():
    with pytest.raises(TypeError):
        mask_area(np.array([[0, 120], [80, 255]]), (.2, .3))
```

## Add geometric relationships to individual examples

A known rectangle provides one numerical reference. Geometric relationships check behavior under transformations. Doubling both pixel spacings doubles each pixel's width and height, so area must become four times larger: 0.72 becomes 2.88 μm². An implementation using only one spacing responds to only one length change, exposing its missing spatial factor. Expressing this relationship in a test makes the physical definition directly visible to someone modifying the code.

Transposing the array exchanges rows and columns. Swapping the associated spacings at the same time describes the same region in a different axis order, so area remains 0.72 μm². This check becomes particularly helpful when direction-dependent properties are added later, because an axis mistake can still produce plausible numbers. An empty-region check confirms that background does not contribute area. Dimension and type checks distinguish a two-dimensional region from a volume or an unsegmented intensity image. Together, they turn the function's intended use into executable conditions.

Three questions guide the selection of tests: is there an independently calculable answer, is there a relationship that should survive an input change, and is there an incorrect input that would change the object's meaning? These provide numerical references, relational references, and input constraints. Other scientific functions offer similar opportunities. A line fit can use points on a known line; an integral can use a function with known area; a coordinate transformation can preserve distances under rigid translation. Connecting tests to the scientific meaning clarifies which changes deserve attention during later revisions.

## Inspect what a collection of tests detects

The following matrix comes from executing eight diagnostic conditions. Columns represent the correct implementation and three deliberate changes; rows represent inputs. PASS and FAIL indicate whether an implementation meets the expectation for that row. The unit-square case allows all four implementations to pass because it has no background, both spacings are one, and the input is valid. Introducing a rectangle with background and unequal, nonunit spacings reveals the missing-factor and whole-array errors. Invalid calibration and incorrect array types then distinguish the omitted-validation implementation.

![Diagnostic matrix from eight executed conditions. PASS means the row expectation is met, including numerical outputs for valid inputs and expected exceptions for invalid ones.](https://ml-biomat.com/static/tutorials/python-scientific/figures/63013fb524ca30125cb40a8b.svg?v=63013fb524ca)

Figure 3Diagnostic matrix from eight executed conditions. PASS means the row expectation is met, including numerical outputs for valid inputs and expected exceptions for invalid ones.

Interpret the matrix through inputs and expectations rather than counting green cells alone. The missing-factor implementation passes six conditions because it retains validation and happens to handle zero area and the unit square. The nonunit rectangle and doubled-spacing case reveal its geometric error. The implementation without validation calculates valid inputs correctly but continues accepting invalid spacings, a volume, and raw intensities. Different mistakes leave different patterns of failure, which the matrix brings together for inspection.

The interactive workspace lets you choose which conditions are active and observe which implementations that collection distinguishes. Begin with the unit square, add the rectangle, and then add negative calibration. Selecting a case or changing the implementation updates its input description, independent expectation, and observed result. The values come from actual Python execution of the implementations. Choosing among those recorded outcomes helps explain the composition of a test collection without turning a test count into a general reliability score.

To read an actual failure, first locate `test_missing_column_spacing`, then inspect `Obtained` and `Expected`. The observed value is 2.4000000000000004 and the expectation is 0.72±1.0e-12, with the same twelve-pixel rectangle as input. Returning to geometry, twelve times row spacing 0.2 gives exactly 2.4: column spacing 0.3 has been omitted. Restoring that factor gives 0.72, which can be checked with the independent suite. The file `failure_demo.py` retains this teaching failure and is invoked separately by the main program. Its expected exit status is one; the correct-function suite exits with zero.

### An explicitly selected teaching failure

The intentionally omitted column spacing produces the actual 2.4-versus-0.72 failure.

```
"""One intentional failure, selected explicitly for reading a failure report."""
import numpy as np
import pytest
from main import changed_area


def test_missing_column_spacing():
    mask = np.zeros((8, 10), dtype=bool)
    mask[2:5, 1:5] = True
    observed = changed_area(mask, (.2, .3), mode="one_scale")
    assert observed == pytest.approx(.72, rel=1e-12, abs=1e-12)
```

### Which conditions distinguish each change?

[Figure: Selected input array and calibration](https://ml-biomat.com/tutorials/python-scientific/p27/en/#P27-input)

#### Selected comparison

```

```

[Figure: Executed diagnostic matrix of cases and implementations](https://ml-biomat.com/tutorials/python-scientific/p27/en/#P27-matrix)

## Run the checks and generate the diagnostic results

The core example has three files, plus a teaching file for inspecting a failure. `measurement.py` holds the scientific function for other programs to import. `test_measurement.py` holds independent checks. `main.py` executes the checks and generates figures and the diagnostic matrix. All complete files are shown on this page and run together from one directory. The main program invokes pytest using the current Python interpreter, checks its return status, and saves the actual test output. After the correct-function suite succeeds, it separately executes the missing-scale example and checks that the intended discrepancy is reported.

Open a terminal in the example directory. The first command runs the complete program and creates figures and summaries; the second runs the thirteen tests of the correct function; the third explicitly selects the teaching failure. `--output` chooses the result directory and `--language` chooses figure language. Naming the test file keeps the two collections separate.

### Full run, correct-function checks, and the failure example

The third command displays the intentional teaching failure and exits with status one.

```
python main.py --output results --language en
python -m pytest test_measurement.py -q
python -m pytest failure_demo.py -q
```

### Execute tests and generate the diagnostic matrix

Save actual test output, compare three teaching mutations, and draw geometry, matrix, and structure figures.

```
"""Run scientific tests and compare deliberately changed implementations."""
from pathlib import Path
import argparse
import json
import math
import os
import re
import subprocess
import sys
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
from measurement import mask_area

HERE=Path(__file__).resolve().parent



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def changed_area(mask,spacing,mode):
    """Teaching mutations: each intentionally changes one scientific rule."""
    if mode=='correct':return mask_area(mask,spacing)
    if mode=='no_validation':return float(np.count_nonzero(mask)*spacing[0]*spacing[1])
    mask_area(mask,spacing)  # These two mutations retain the input checks.
    if mode=='one_scale':return float(np.count_nonzero(mask)*spacing[0])
    if mode=='whole_grid':return float(mask.size*spacing[0]*spacing[1])
    raise ValueError(mode)


def cases():
    rectangle=np.zeros((8,10),bool);rectangle[2:5,1:5]=True
    return [
        ('unit_square',np.ones((2,2),bool),(1.,1.),4.),
        ('rectangle',rectangle,(.2,.3),.72),
        ('empty',np.zeros((8,10),bool),(.2,.3),0.),
        ('doubled',rectangle,(.4,.6),2.88),
        ('negative',rectangle,(-.2,.3),'ValueError'),
        ('nonfinite',rectangle,(.2,float('nan')),'ValueError'),
        ('volume',np.ones((2,3,4),bool),(.2,.3),'ValueError'),
        ('intensity',np.array([[0,120],[80,255]]),(.2,.3),'TypeError')]


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--language',choices=['zh','en'],default='en');args=ap.parse_args()
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh';tr=lambda a,b:a if zh else b
    environment=os.environ.copy();environment['PYTHONDONTWRITEBYTECODE']='1'
    environment['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
    command=[sys.executable,'-m','pytest',str(HERE/'test_measurement.py'),'-q','--rootdir',str(HERE),'-p','no:cacheprovider']
    completed=subprocess.run(command,cwd=HERE,text=True,capture_output=True,env=environment)
    (out/'pytest-output.txt').write_text(completed.stdout+completed.stderr,encoding='utf8')
    if completed.returncode:raise RuntimeError('Scientific tests failed; see pytest-output.txt')
    negative=subprocess.run([sys.executable,'-m','pytest','failure_demo.py','-q','--tb=short','-p','no:cacheprovider'],cwd=HERE,text=True,capture_output=True,env=environment)
    if negative.returncode!=1:raise RuntimeError('The deliberate missing-scale example must fail its assertion')
    (out/'failure-example.txt').write_text(negative.stdout+negative.stderr,encoding='utf8')
    modes=['correct','one_scale','whole_grid','no_validation'];records=[]
    for name,mask,spacing,expected in cases():
        for mode in modes:
            try:
                value=changed_area(mask,spacing,mode)
                observed=value if math.isfinite(value) else 'NaN'
            except (ValueError,TypeError) as error:observed=type(error).__name__
            passed=(observed==expected if isinstance(expected,str) else isinstance(observed,(int,float)) and math.isclose(observed,expected,rel_tol=1e-12,abs_tol=1e-12))
            records.append({'case':name,'mode':mode,'expected':expected,'observed':observed,'passed':bool(passed)})
    passes={m:sum(r['passed'] for r in records if r['mode']==m) for m in modes}
    passed_count=int(re.search(r'(\d+) passed',completed.stdout).group(1))
    summary={'pytest_exit_code':completed.returncode,'pytest_passed':passed_count,'deliberate_failure_exit':negative.returncode,'cases':8,'modes':4,'pass_counts':passes,
             'rectangle_area_um2':mask_area(cases()[1][1],(.2,.3)),'mutation_results':records}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    inputs={name:{'shape':list(mask.shape),'dtype':str(mask.dtype),'mask':mask.tolist(),
                  'spacing':[v if math.isfinite(v) else 'NaN' for v in spacing]}
            for name,mask,spacing,expected in cases()}
    (out/'lab-data.json').write_text(json.dumps({'records':records,'modes':modes,'cases':[c[0] for c in cases()],'inputs':inputs}),encoding='utf8')
    plt.rcParams.update({'font.family':available_plot_fonts(),'font.size':12,'svg.fonttype':'none','figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        fig.savefig(out/f'{name}-{args.language}.svg',metadata={'Date':None});fig.savefig(out/f'{name}-{args.language}.png',dpi=150);plt.close(fig)
    mask=cases()[1][1];fig,ax=plt.subplots(figsize=(9,5.3),layout='constrained')
    ax.imshow(mask,cmap=ListedColormap(['#f0f2f3','#205b8c']),extent=(0,3,1.6,0),interpolation='nearest')
    ax.vlines(np.arange(0,3.01,.3),0,1.6,color='white',lw=1.2)
    ax.hlines(np.arange(0,1.61,.2),0,3,color='white',lw=1.2)
    ax.set(xlabel=tr('水平位置 / μm','Horizontal position / μm'),ylabel=tr('垂直位置 / μm','Vertical position / μm'))
    ax.text(1.8,.65,tr('选中 4 列 × 3 行\n宽 1.2 μm，高 0.6 μm\n独立几何面积 = 0.72 μm²','4 columns × 3 rows selected\nWidth 1.2 μm, height 0.6 μm\nGeometric area = 0.72 μm²'),fontsize=12,linespacing=1.8)
    ax.set_title(tr('一个能在纸上独立算出答案的测试对象','A test object with an independently calculable answer'),loc='left')
    save(fig,'known-geometry')
    grid=np.array([[int(next(r['passed'] for r in records if r['case']==case[0] and r['mode']==m)) for m in modes] for case in cases()])
    fig,ax=plt.subplots(figsize=(12.4,6.4),layout='constrained');ax.imshow(grid,cmap=ListedColormap(['#f1d7cb','#deebe6']),vmin=0,vmax=1,aspect='auto')
    names=tr(['单位方格','有背景的矩形','空区域','双向尺度加倍','负标定','非有限标定','误传三维数组','误传灰度数组'],['Unit square','Rectangle with background','Empty region','Both lengths doubled','Negative calibration','Nonfinite calibration','3D input','Intensity input'])
    ax.set_xticks(range(4),tr(['正确实现','漏乘一个尺度','误数整个网格','省略输入检查'],['Correct','One scale missing','Whole grid counted','No input validation']))
    ax.set_yticks(range(8),names)
    for y in range(8):
        for x in range(4):ax.text(x,y,'PASS' if grid[y,x] else 'FAIL',ha='center',va='center',color='#205b55' if grid[y,x] else '#9b3e21',fontsize=13)
    ax.set_title(tr('测试诊断矩阵：不同科学条件发现不同错误','Diagnostic test matrix: different conditions detect different errors'),loc='left',pad=18)
    save(fig,'test-matrix')
    fig=plt.figure(figsize=(13.2,7.3));gs=fig.add_gridspec(2,2,width_ratios=[1,1.6],height_ratios=[1.3,1],left=.06,right=.97,bottom=.15,top=.88,hspace=.23,wspace=.18)
    geom=fig.add_subplot(gs[0,0]);geom.imshow(mask,cmap=ListedColormap(['#edf1f3','#205b8c']),extent=(0,3,1.6,0),interpolation='nearest')
    geom.vlines(np.arange(0,3.01,.3),0,1.6,color='white',lw=1);geom.hlines(np.arange(0,1.61,.2),0,3,color='white',lw=1)
    geom.set(xlabel=tr('横坐标 / μm','Horizontal position / μm'),ylabel=tr('纵坐标 / μm','Vertical position / μm'))
    geom.set_title(tr('A  同一个 12 像素矩形','A  The same 12-pixel rectangle'),loc='left',fontsize=14)
    calculation=fig.add_subplot(gs[1,0]);calculation.axis('off')
    calculation.text(0,.97,tr('独立几何期望','Independent geometry'),fontsize=14,color='#205b8c',va='top')
    calculation.text(0,.73,'(4 × 0.3) × (3 × 0.2)\n= 0.72 μm²',fontsize=17,va='top',linespacing=1.6)
    calculation.text(0,.16,tr('漏乘列间隔：12 × 0.2 = 2.4\n恢复列间隔：2.4 × 0.3 = 0.72','Missing column spacing: 12 × 0.2 = 2.4\nRestore it: 2.4 × 0.3 = 0.72'),fontsize=12,va='top',linespacing=1.6)
    failure=fig.add_subplot(gs[0,1]);failure.axis('off');failure.set_title(tr('B  pytest 的实际失败片段','B  Actual pytest failure excerpt'),loc='left',fontsize=14,color='#9b3e21')
    excerpt=[line for line in negative.stdout.splitlines() if line.startswith('E ') or 'failure_demo.py:' in line]
    # Keep actual diagnostic text; wrap long lines for display.
    visible=[]
    for line in excerpt[:7]:visible.extend(textwrap.wrap(line,width=64,replace_whitespace=False,drop_whitespace=False) or [''])
    failure.text(0,.94,'\n'.join(visible),va='top',family='DejaVu Sans Mono',fontsize=12,linespacing=1.45,
                 bbox={'facecolor':'#f5e8e1','edgecolor':'#d7b5a5','pad':12})
    success=fig.add_subplot(gs[1,1]);success.axis('off');success.set_title(tr('C  正确函数通过独立测试集','C  Correct function passes the independent suite'),loc='left',fontsize=14,color='#205b55')
    success.text(0,.85,'assert area == pytest.approx(\n    0.72, rel=1e-12, abs=1e-12\n)',va='top',family='DejaVu Sans Mono',fontsize=12.5,linespacing=1.5)
    actual_pass=next(line for line in completed.stdout.splitlines() if re.search(r'\d+ passed',line))
    success.text(0,.15,actual_pass,fontsize=14,color='#205b55',bbox={'facecolor':'#e1eee7','edgecolor':'none','pad':9})
    fig.suptitle(tr('把一次真实失败读回面积定义','Read an actual failure back into the area definition'),x=.06,ha='left',fontsize=18)
    fig.text(.06,.035,tr('测试传统：Python unittest 受 JUnit 启发；可重复输入、独立期望与执行报告保留在一起。','Testing tradition: Python unittest was inspired by JUnit; retain repeatable inputs, independent expectations, and execution reports.'),fontsize=12)
    save(fig,'test-structure')
    print(json.dumps({k:v for k,v in summary.items() if k!='mutation_results'}))


if __name__=='__main__':main()
```

The example run passes thirteen tests, and the correct implementation passes all eight diagnostic conditions. The three teaching variants pass six, five, and four conditions respectively. These counts describe the explicitly listed inputs. `summary.json` also retains each case's expected value, observed value, and comparison result, allowing changes to the test objects to be inspected later. The figures and records derive from the same execution, so each matrix cell can be traced to a particular comparison.

Separating the main program from the scientific function has another practical benefit: an analysis script can import `mask_area` without automatically starting plotting or testing. The `if __name__ == '__main__'` block starts the program when this file is run directly. This organization suits small scientific projects: core calculations remain callable, checks remain repeatable, and the main script organizes presentation and file writing. Later performance changes can be checked against the same scientific definitions before their timings are compared.

## Let the tests develop with the research question

Moving from two-dimensional images to volumes calls for a volume function with three spacings and a stated volume unit, followed by tests using a rectangular solid, an empty volume, and scale transformations. The original area function continues to serve its original definition. When a scientific question changes, the interface, explanation, and tests should change together. A caller benefits from knowing whether the function measures area or volume, with the corresponding inputs made explicit.

During maintenance, a discovered error can become a small reproducible test input. If an axis-order change produces an incorrect result, retain the smallest array and spacings that reproduce that situation. Once corrected, preserve the expected behavior in a test so that future restructuring checks it automatically. The important objects are the triggering relationship and its intended meaning. A compact geometric array and calibration parameters can travel with the test as an independent example.

Useful checks make code easier to change. Array operations can be reorganized, functions separated, and execution accelerated while known geometry and input constraints confirm that the scientific meaning remains consistent. The next chapter compares the time and memory costs of different calculations, beginning with agreement of their results. Testing connects a research definition to its implementation and gives later optimization a stable reference.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P27.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pytest: Get Started](https://docs.pytest.org/en/stable/getting-started.html)

   Open introductory tutorial for discovery, assertions, and expected exceptions.

   pytest code and documentation: MIT.
2. [pytest: Parametrizing fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)

   Parameterized execution for related input conditions.

   MIT.
3. [Python unittest](https://docs.python.org/3/library/unittest.html)

   JUnit historical connection and the roles of fixtures, cases, suites, and runners.

   Python documentation: PSF terms; historical and technical reference.
4. [pytest.approx](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx)

   Tolerance-based floating-point comparison.

   MIT.
