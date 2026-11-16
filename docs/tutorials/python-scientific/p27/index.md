# 让分析程序经得起检查与复用

Source: https://ml-biomat.com/tutorials/python-scientific/p27/
Language: zh-CN

用能够手算的几何对象、明确的输入定义和实际执行的测试，让一次面积计算成为可复用的科学工具。

## 下一次改代码时，怎样知道原来的计算仍然成立

一个分析程序往往从解决眼前问题开始：读一张图，找出一个区域，算出面积。后来输入变成几十张图，像素间隔也有不同，函数又被接入报告程序。代码越来越有用，修改它时需要确认的事情也随之增加。自动测试把这些确认保存成可以重复执行的条件：给定什么输入，应当得到什么结果；遇到不符合定义的输入，应当怎样说明问题。它让原先靠记忆、手算和临时打印完成的检查，随着程序一起留下来。

本章把一个二维区域面积函数作为完整例子。函数接收布尔掩膜和两个方向的像素间隔，返回 μm² 单位的面积。我们先设计一个能在纸上算出答案的矩形，再检查空区域、尺度变化、转置、无效标定和错误维度。最终的 pytest 文件包含 13 个实际执行的检查。为了看清每个条件为何有用，还会比较三个有意修改过的实现：漏乘一个尺度、把整张图都算进面积、以及省略输入检查。它们是为理解错误模式而建立的教学对照，各自的表现会出现在诊断矩阵里。

可以把测试理解为给一把量尺准备几块已知尺寸的样品。拿量尺去测未知物体之前，先测一块长度已知的标准块，能检查读数与尺度是否一致。程序也需要这样的参照对象。一个复杂细胞的真实面积难以独立知道，但一个横向四个像素、纵向三个像素的矩形很好计算。先用简单对象建立可靠的计算关系，再把函数用于复杂对象，这种顺序同时服务于科学理解和程序维护。

## 把函数的输入与输出说清楚

测试开始之前，需要决定函数究竟做什么。这里的掩膜是二维布尔数组，每个值只有真或假：真表示像素属于选中区域，假表示背景。输入 `spacing` 含两个长度，顺序为行方向、列方向，单位都是 μm。它们允许不同，因为有些成像或重采样数据在两个方向的采样间隔并不相同。输出是所有选中像素对应的总面积，单位为 μm²。函数接收的已经是区域选择结果，因此分割阈值属于上游处理；面积函数负责把明确的区域换算成物理量。

$$
A=N s_y s_x
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选中区域的二维面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 为真的像素个数，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/8f5fc51f77ebba17af28d557.svg) | 行方向的像素间隔，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/d65997e80acc2ddac324815b.svg) | 列方向的像素间隔，μm |

一个像素对应宽 s_x、高 s_y 的小矩形，其面积是两个边长相乘；N 个选中像素的面积相加得到 A。当前矩形选中 12 个像素，行间距 0.2 μm、列间距 0.3 μm，因此 A=12×0.2×0.3=0.72 μm²。也可以从整体几何独立计算：四列宽 1.2 μm，三行高 0.6 μm，相乘同样为 0.72 μm²。

输入定义也包含边界情形。一个全为假的掩膜表示空区域，其面积自然是零；它与“输入不是二维图像”有不同含义。三维数组需要三个方向的尺度和体积定义，所以误传三维数据时，函数给出维度错误。原始灰度数组也与布尔掩膜不同：直接数其中的非零值，会把背景中许多正常灰度像素一并选中。函数要求布尔类型，使读者在调用前明确完成区域选择。这样的检查把可能改变科学意义的错误拦在入口处。

像素间隔必须是两个有限正数。零不能描述像素的实际边长，负数不能作为当前空间采样间隔，`NaN` 和无穷大也无法进入正常几何面积计算。程序对这些情况给出 `ValueError`，表示数值不符合当前定义；掩膜类型不对则给出 `TypeError`。异常名称与简短消息帮助调用者决定怎样修正输入。之后处理一批图像时，可以把失败图像编号与错误原因一起记录，再回到对应输入检查标定或数组形状。

### 科学函数：由区域与标定计算面积

输入类型、维度、单位与无效标定响应都明确写在函数中。

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

## 先准备一个能独立算答案的对象

测试矩形放在一张 8 行、10 列的空白掩膜里，其中第 2 到第 4 行、第 1 到第 4 列设为真。Python 切片的终点不包含在结果中，所以 `mask[2:5, 1:5]` 选中三行、四列，共 12 个像素。行间距取 0.2 μm，列间距取 0.3 μm，于是矩形高 0.6 μm、宽 1.2 μm，几何面积为 0.72 μm²。这个期望值从长乘宽得到，独立于函数内部怎样数像素。

![用明确几何定义建立独立期望：12 个选中像素处在 80 个像素的网格中，两个方向间隔不同。](https://ml-biomat.com/static/tutorials/python-scientific/figures/19fd269a421abd409c96f874.svg?v=19fd269a421a)

图 1用明确几何定义建立独立期望：12 个选中像素处在 80 个像素的网格中，两个方向间隔不同。

把背景保留在测试图中很有用。如果测试输入恰好全部为真，那么数选中像素与数整个数组元素会得到相同结果，一个错误实现也可能通过。当前矩形周围有背景，数组总共 80 个像素，而选中区域只有 12 个。两种计数在这里明显分开。测试数据的价值因此来自它能区分哪些行为，而不只是它包含多少个数。一个小而有针对性的输入，往往比一张复杂但答案未知的图更能定位问题。

数值结果可能显示为 `0.7200000000000001`，这是浮点表示带来的细小差异。pytest 的 `approx` 用容差比较浮点结果，表达“在约定精度内等于几何期望”。容差应与计算的数值性质相配：计数可以精确比较，经过浮点乘法或较长数值算法的结果则需要相应容差。把一个明显错误的 2.4 或 4.8 放进很宽的容差范围，会掩盖单位或计数错误，因此容差也应服务于科学定义。

这份测试显式设置相对容差 `rel=1e-12` 和绝对容差 `abs=1e-12`。前者允许误差随期望值的大小按万亿分之一缩放，后者给出 10 的负十二次方 μm² 的绝对尺度，比较时采用两者中较大的允许差异。对期望值 0.72 μm²，相对项为 0.72×10 的负十二次方，绝对项更大，因此最终允许差异为 10 的负十二次方 μm²。这个尺度足以容纳本例几次双精度乘法的舍入差异，又远小于漏乘尺度产生的差异。若函数以后加入近似求解或数值积分，应根据相应算法的精度重新选择容差。

## 测试框架怎样把一次检查变成长期保留的能力

测试框架的历史积累，形成了几种很实用的分工。Python 标准库的 `unittest` 受 JUnit 启发，将输入准备、单个检查、检查集合和执行器分别组织起来；它的官方文档也保留了 Kent Beck 关于 Smalltalk 测试模式的早期论文入口。这套思路适合科学代码：准备一个重复使用的几何对象，将不同性质写成独立用例，再由程序统一执行和报告。pytest 在这种自动测试工作方式上提供了简洁的函数与断言写法，使小型分析项目也能方便地保留检查。

![同一个矩形的几何期望、真实 pytest 失败片段和正确函数通过记录。报告文字来自示例实际运行，指出漏乘列间距如何把0.72变成2.4。](https://ml-biomat.com/static/tutorials/python-scientific/figures/7930b97a136dd362cb0c8312.svg?v=7930b97a136d)

图 2同一个矩形的几何期望、真实 pytest 失败片段和正确函数通过记录。报告文字来自示例实际运行，指出漏乘列间距如何把0.72变成2.4。

在本例中，`fixture` 准备那张带背景的矩形掩膜，每次需要它的测试都获得同样定义的输入。以 `test_` 开头的函数表示检查条件，`assert` 写出期望关系。执行 pytest 后，它发现这些函数，逐个运行，并将失败定位到具体断言。为矩形创建一个 fixture，能够避免在多个测试里重复复制数组构造代码；几何对象的定义集中在一处，读者也更容易核对每个检查使用的是同一个输入。

参数化把一类检查的多个输入列出来。零标定、负标定、非有限标定和尺度数量不正确，都属于标定输入违反定义的情况。`pytest.mark.parametrize` 让同一个检查函数分别接收这些参数，每种情况独立报告。`pytest.raises(ValueError)` 则表示这次调用应当明确拒绝输入。这里抛出预期异常就是正确行为，因此测试成功包含两类结果：有效输入得到正确面积，以及无效输入得到明确说明。

### 独立几何、输入边界与规律检查

13 项 pytest 检查实际运行，期望值来自几何和对象定义。

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

## 用几何规律补充单个算例

已知矩形给出一个数值参照，几何规律则检查函数在一组变化下是否保持合理关系。两个方向的像素间隔同时加倍时，每个像素的宽和高都加倍，面积应变为原来的四倍。本例从 0.72 变成 2.88 μm²。若函数只乘了一个方向的尺度，它会表现为面积只随一个长度变化，这个检查便能暴露少掉的空间方向。把单位关系写成测试，也让代码修改者直接看见物理定义要求什么。

转置数组时，行和列交换；同时交换两个方向的像素间隔，表示同一个区域采用另一种轴顺序。总面积应保持 0.72 μm²。这个检查在今后加入方向相关属性时尤其有用，因为轴顺序错误常常仍能产生看似合理的数值。空区域检查则确认背景不会自动贡献面积。维度和类型检查进一步区分二维区域、三维对象与未分割的灰度图，它们共同把函数的用途写成可以执行的条件。

选择测试时可以围绕三个问题展开：有没有能够独立计算的答案，有没有输入变化后应遵守的规律，有没有会改变对象定义的错误输入。它们对应数值参照、关系参照和入口约束。实际项目中的其他函数也能找到类似条件：线性拟合可以用完全落在已知直线上的点，数值积分可以用面积已知的函数，坐标变换可以检查刚体平移后的距离。测试对象越贴近要维护的科学含义，后来修改代码时越容易判断哪些变化需要重新审视。

## 看清一组测试究竟发现了什么

下面的矩阵来自实际执行的八类诊断条件。列分别对应正确实现和三种有意改变过的实现，行对应具体输入，单元格中的 PASS 或 FAIL 表示该实现是否符合这一行的预期。第一行的单位方格恰好让四种实现都通过：它没有背景、尺度都为 1、输入也有效。接下来增加带背景的非等间距矩形，漏乘尺度和数完整数组两种错误便显现出来；再加入无效标定与错误数组类型，省略输入检查的问题也能被区分。

![八类条件实际运行得到的诊断矩阵。每个 PASS 表示满足该行预期，包括有效输入的数值与无效输入的预期异常。](https://ml-biomat.com/static/tutorials/python-scientific/figures/9a1f42d910af94c4153af11d.svg?v=9a1f42d910af)

图 3八类条件实际运行得到的诊断矩阵。每个 PASS 表示满足该行预期，包括有效输入的数值与无效输入的预期异常。

矩阵中的失败信息应沿着输入与期望来解释，而不是只数有多少个绿色格子。漏乘尺度的实现通过了六类条件，是因为它仍保留输入检查，也恰好能处理零面积与单位方格；真正揭示其几何错误的是非单位尺度的矩形和双向尺度加倍条件。省略验证的实现则能够算对有效输入，但会继续接受无效标定、三维数组和灰度数组。不同错误留下不同的失败形状，矩阵把这些区别集中呈现出来。

交互中可以选择启用哪些条件，观察哪些改动会被当前测试集合发现。先只保留单位方格，再加入矩形，最后加入负标定，诊断能力会随之变化。点击某个用例或切换实现后，输入说明、独立期望和实际结果同时更新。这里的数据来自 Python 对各实现的真实执行；页面通过选择已有结果帮助理解检查组合，而不把测试数量直接换成一个泛化的可靠性分数。

阅读一次真实失败时，可以先找函数名 `test_missing_column_spacing`，再看报告中的 `Obtained` 和 `Expected`。本例观察值为 2.4000000000000004，期望是 0.72±1.0e-12；输入仍是那块 12 像素矩形。回到几何关系，12 乘行间距 0.2 恰好得到 2.4，说明列间距 0.3 漏掉了。补回这一乘法得到 0.72，再运行独立测试集即可核对修正。`failure_demo.py` 专门保留这个教学失败，由主程序单独调用；其返回状态为 1，正确函数的测试集返回状态为 0。

### 单独执行的教学失败

故意漏掉列间距，真实运行后给出2.4与0.72的差异。

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

### 哪些条件能发现哪一种改动

[Figure: 当前测试数组与标定](https://ml-biomat.com/tutorials/python-scientific/p27/#P27-input)

#### 当前比较

```

```

[Figure: 用例与实现的实际诊断矩阵](https://ml-biomat.com/tutorials/python-scientific/p27/#P27-matrix)

## 完整运行：执行检查，生成诊断结果

核心示例由三个文件组成，另附一个用于阅读失败报告的教学文件。`measurement.py` 保存供其他程序调用的科学函数，`test_measurement.py` 保存独立检查，`main.py` 执行检查并生成教学图与诊断矩阵。完整代码都在本页展示，下载后放在同一目录即可运行。主程序调用当前 Python 解释器执行 pytest，检查返回状态，并将实际测试输出写入结果目录。正确函数的检查成功后，再单独运行故意漏乘尺度的示例，并确认它确实报告预期差异。

在示例目录打开终端，第一条命令执行完整程序并生成图与摘要；第二条只执行正确函数的 13 项测试；第三条单独执行教学失败，用来练习阅读报告。`--output` 指定结果目录，`--language` 决定图中的文字。pytest 命令明确给出文件名，因此两组用途不同的检查各自执行。

### 完整运行、正确函数检查与失败示例

第三条命令用于观察预期的教学失败，返回状态1。

```
python main.py --output results --language en
python -m pytest test_measurement.py -q
python -m pytest failure_demo.py -q
```

### 执行测试并生成诊断矩阵

保存实际测试输出，比较三个教学变体，并绘制几何、矩阵和结构图。

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

本次示例执行得到 13 项测试通过，正确实现通过八类诊断条件。三个教学变体分别通过六类、五类和四类条件，这些计数描述当前明确列出的输入集合。`summary.json` 还保存每个用例的期望值、观察值和是否符合预期，便于将来修改测试对象后重新核对。运行输出与图都由同一次执行产生，因此矩阵里的颜色可以追溯到一条具体比较，而不只是手工填写的示意。

主程序与科学函数分开，还有一个直接好处：别的分析脚本可以导入 `mask_area`，不会因为导入而自动运行绘图或测试。`if __name__ == '__main__'` 把直接执行的入口保留在主程序末尾。这样的文件组织适合规模不大的科研项目：核心计算保持可调用，检查保持可重复，展示与文件输出集中在入口程序中。后续提高效率时，可以先运行同一组科学测试，确认新实现仍然遵守原先的定义。

## 让测试随着研究问题一起发展

当输入从二维图像变成三维体数据时，需要建立新的体积函数，说明三个方向的间隔和体积单位，再为长方体、空体积及尺度变化写出对应检查。原来的二维函数仍然服务于原来的定义。研究问题改变时，函数接口、说明和测试应一起改变，这比让一个函数默默接受更多形状更容易维护。对使用者而言，明确知道调用的是面积还是体积，比让所有输入都返回某个数字更有价值。

维护现有程序时，可以把每次发现的具体错误转成一个小型可重复输入。例如一张图由于轴顺序变化得到错误面积，就保留能重现这一情况的最小数组与尺度；修正之后，把正确行为写入测试。这样，下一次重构时该条件会自动重新检查。保留的重点是触发关系和预期意义；几何数组和标定参数可以组成独立的小数据包，随测试一起传递。

好的检查让代码更容易改变。你可以调整数组操作、拆分函数或提高运行效率，同时用已知几何对象和输入约束确认科学含义保持一致。下一章会比较不同计算方式的耗时与内存，首先要做的就是确认它们得到相同结果。测试由此成为连接研究定义、程序实现和后续优化的一段稳定关系。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P27.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [pytest: Get Started](https://docs.pytest.org/en/stable/getting-started.html)

   测试发现、断言与预期异常的开源基础教程。

   pytest code and documentation: MIT.
2. [pytest: Parametrizing fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)

   同类输入的参数化执行。

   MIT.
3. [Python unittest](https://docs.python.org/3/library/unittest.html)

   JUnit 历史联系，以及 fixture、case、suite、runner 的分工。

   Python documentation: PSF terms; historical and technical reference.
4. [pytest.approx](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx)

   浮点数容差比较。

   MIT.
