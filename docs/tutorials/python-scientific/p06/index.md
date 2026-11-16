# 让程序在自己的电脑上稳定运行

Source: https://ml-biomat.com/tutorials/python-scientific/p06/
Language: zh-CN

从解释器、模块和环境到一次有单位的密度计算，学会沿着实际执行路径定位问题。

## 同一段程序，怎样在自己的电脑上跑清楚？

已经能够写函数、读取文件和生成图表以后，新的问题往往出现在计算开始之前：明明安装了绘图库，程序却说找不到；终端能运行，编辑器却报错；改过函数以后，笔记本仍然显示旧结果。本章把这些现象放回同一条工作链：由哪个Python解释器运行代码，它到哪里寻找模块，使用哪些版本，以及异常如何把我们带回具体输入。最终例子会调用一个独立模块计算矩形样品的密度，保存运行信息，并把实际捕获的调用路径画出来。

计算对象很小：一块构造的矩形试样，质量0.20 g，长10 mm、宽8 mm、厚2 mm。统一长度单位后，它的体积是0.16 cm³，密度是1.25 g/cm³。我们还会把厚度改成零，观察明确的输入检查；再故意漏掉毫米到厘米的换算，观察为什么没有异常也可能出现错误的科学数值。这个例子把运行环境、程序逻辑和物理定义分开检查，让每个问题都有相应的定位办法。

可以把解释器看成实际执行计算的设备，第三方库是装在设备上的功能部件，脚本是这次实验的操作流程，数据是输入材料。打开某个编辑器并不自动说明正在使用哪台“设备”。同一台电脑上可以有多个Python，它们各自能找到的库也可能不同。明确运行入口，才能解释安装操作与后续导入之间的关系，而不必在遇到问题时反复重新安装所有东西。

## 先确认是谁在执行代码

第一次使用时，先从[Python官方网站](https://www.python.org/downloads/)取得解释器。这套示例在Python 3.14下运行核对，可选择该系列的维护版本建立环境。Windows用户可以按[官方Windows安装说明](https://docs.python.org/3.14/using/windows.html)安装Python安装管理器，再选择3.14运行时；macOS用户可使用官方网站提供的安装包，按[macOS说明](https://docs.python.org/3.14/using/mac.html)完成安装与证书设置；Linux用户按所用发行版的说明安装Python、pip与venv支持。安装完成后重新打开终端，先执行下面的版本检查。能看到Python版本和pip信息，才说明这两个入口已经可用；macOS和Linux通常把命令开头换成`python3`。若显示的版本与计划使用的不同，先选择对应解释器，例如Windows上的`py -3.14`，再用该入口创建项目环境。

### 先检查解释器与安装工具

在系统终端执行；macOS与Linux通常用python3替换命令开头的python。输出中的版本与位置用于确认当前入口。

```
python --version
python -m pip --version
```

在终端输入`python main.py`，终端先寻找名为python的可执行程序，再把main.py交给它。解释器负责读取Python代码并执行，编辑器主要负责编辑文件；笔记本还通过一个内核进程执行单元格。终端、编辑器和笔记本可以被配置成同一个解释器，也可以各自指向不同环境。出现“这里能用、那里不能用”时，先检查运行入口，比猜测库是否损坏更直接。

### 在当前Python中查看运行入口

在需要诊断的运行窗口执行，比较实际解释器。

```
import sys
print(sys.executable)
print(sys.version)
```

`sys.executable`给出当前解释器的位置，`sys.version`描述Python版本。可以在终端启动的解释器、编辑器运行窗口和笔记本单元格中分别查看，判断它们是否指向同一套安装。这里的完整示例只在可分享的结果中保存解释器文件名、版本和环境状态，读者自己定位问题时则可以在本机查看完整位置。位置解决“是谁在运行”，版本解决“这一套语言与库接口是什么”，两项信息相互补充。

`python -m pip`中的`-m`表示让这个Python运行名为pip的模块。它把安装操作与当前明确指定的解释器绑定起来；单独输入`pip`时，终端找到的命令入口可能属于另一套Python。相同道理，`python -m venv`调用的是当前解释器提供的环境创建模块。理解这个结构以后，一长串命令可以拆成“指定解释器—运行哪个模块—给它什么参数”，每一部分的职责都能说明白。

如果安装已经成功而编辑器仍无法导入，检查编辑器选择的解释器；如果问题出现在笔记本，检查当前内核。切换内核后重新执行所需单元格，才能在新进程里建立变量和导入。已经启动的进程不会因为磁盘上的文件改变，就自动替换内存中的全部对象。安装、选择入口与重启执行过程是不同动作，只有把它们接到同一条链上，新环境里的代码才真正参与计算。

终端里输入的命令和Python语句也属于不同层次。带有安装参数的命令应交给操作系统终端，`import sys`这样的语句交给Python解释器；把安装命令直接放进普通.py文件，会先遇到语法问题。屏幕上的提示符能够帮助识别当前所在位置：交互式Python常用`>>>`等待语句，终端则等待启动程序的命令。教程中展示的提示符用于说明上下文，复制时只复制命令本身。理解这个区别，还能解释为什么笔记本里某些以特殊符号开头的命令不能原样移入脚本。

## 虚拟环境解决的是依赖如何相处

两个项目可能需要同一个库的不同版本：一个项目使用旧接口，另一个需要新接口。如果只保留一套共同安装，升级时就容易影响正在使用的项目。虚拟环境为项目提供自己的包安装位置，同时使用创建它的基础Python。它不是一台独立虚拟机，也不会自动复制实验数据或修正单位；它组织的是解释器与包的可见范围，使项目依赖能够分别管理。

2011年提出的PEP 405把这种机制纳入Python，目标版本为Python 3.3。提案讨论了当时已有虚拟环境工具需要配合解释器启动行为的困难，并给出标准库层面的支持：环境保存自己的配置和包目录，基础标准库仍可共享。图中两个项目分别连接自己的包位置，再连接共同基础，这正是“分开安装项目依赖”和“复用基础Python”能够同时成立的原因。环境目录里的`pyvenv.cfg`记录了与基础安装的联系。

![PEP 405的环境结构：两个项目分别寻找自己的第三方包，同时共享基础Python的标准库。箭头表示依赖关系。](https://ml-biomat.com/static/tutorials/python-scientific/figures/a9b702a7f6f19c241bac2f18.svg?v=a9b702a7f6f1)

图 1PEP 405的环境结构：两个项目分别寻找自己的第三方包，同时共享基础Python的标准库。箭头表示依赖关系。

下面分别给出Windows PowerShell与macOS、Linux终端的运行入口。先在示例项目目录创建`.venv`，再直接使用其中的解释器安装下载包附带的依赖清单并运行程序。这种写法每次都明确选择入口，不依赖终端是否已经激活环境。激活环境同样可用，它主要改变当前终端查找命令的顺序，让较短的`python`指向所选环境；直接指定解释器与激活后运行，是到达同一目标的两种方式。

### Windows PowerShell：使用项目环境

在下载示例目录运行；每行明确指定环境解释器。

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --output output --language zh
```

### macOS与Linux：使用项目环境

相同流程使用平台对应的解释器入口。

```
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py --output output --language zh
```

依赖清单中的包名告诉安装工具需要哪些分发包，版本约束描述要采用的版本范围或具体版本。`python -m pip freeze`可以列出当前安装状态，适合记录一次成功运行所用的版本；专门项目环境中的清单通常比混合许多无关工作的全局环境更容易理解。环境文件夹一般在目标电脑重新创建，因为其中可能保存与本机解释器位置有关的配置。代码、数据、依赖清单和运行说明一起传递，才能使别人按同一约定重建工作流程。

环境隔离可以用两个抽屉来理解：项目A把自己需要的工具放在A抽屉，项目B把工具放在B抽屉，取用者按所选入口打开对应抽屉。把绘图库装进B，并不会让A自动看见它。图里的共享基础则像两边都使用的同一套基础设施。依赖之间还可能存在版本要求，安装工具会检查这些要求并给出结果；若发生冲突，先读清楚是哪两个包提出了互不相容的条件，再决定调整哪个项目的清单。单纯重复同一条安装命令不会改变这些条件。

## 模块让计算规则有一个清楚的家

上一章已经把复杂工作拆成函数。本章再把密度函数放进`calibration.py`，让`main.py`通过`from calibration import density`使用它。一个.py文件可以作为模块，保存相关定义；导入把这些定义连接到当前程序中。若写`import calibration`，调用时使用`calibration.density(...)`；若只导入density，就直接用函数名。前者让函数来自哪个模块更显眼，后者适合名称清楚且使用频繁的少量函数。

库是对一组可复用功能的通常称呼，模块和包则描述Python组织导入对象的方式。一个包可以包含多个模块和子包；安装工具处理的分发包名称，与代码中导入的名称并不总是相同。例如学习某个库时，应以它的官方安装和导入说明为准。这里的`math`属于标准库，`matplotlib`需要安装，`calibration`是示例旁边的本地模块。三者都通过import进入程序，获得它们的方式却不同。

点号表示访问对象的某个属性。`math.isfinite`是模块里提供的函数，后面加括号才调用；`Path('data').parent`是路径对象的父目录属性，通常不加括号；`path.open()`是与路径对象关联的方法，需要调用才能打开文件。把“对象是什么”“点号后取到什么”“是否准备调用”依次分清，许多陌生接口都能从结构上读懂。后面的NumPy数组和pandas表格，也会沿用这种对象与操作的关系。

导入时的查找顺序还会带来一个实际问题：把自己的脚本命名为`matplotlib.py`、`csv.py`或其他正在使用的模块名，可能使本地文件遮住预期的库。若导入对象与预期不同，可以查看模块的`__file__`定位实际载入了哪一个文件。改用能表达任务的名字后，重新启动进程再导入。这个步骤是在核对对象身份，和前面查看解释器位置一样，能把一个模糊的“导入出错”缩小到具体文件。

导入还会执行模块最外层的语句，因此适合把可复用定义放在模块中，把完整任务放进main函数，并用入口条件控制何时执行。否则，一个原本只想借用密度函数的程序，也可能意外启动文件读写或绘图。模块通常会缓存在当前进程中，第二次import一般不会从头重跑整个文件；这有助于保持对象一致，也说明修改模块后为什么需要重新启动运行。对初学阶段的小项目，清楚的文件职责与重新运行顺序，比复杂的自动重载更容易检查。

## 先用尺寸与单位检查一个能够手算的结果

质量密度表示单位体积里有多少质量。对本例规则矩形试样，体积由长、宽、厚相乘得到：可以把底面看成长乘宽得到的面积，再让它沿厚度方向延伸。三种长度都需要使用相同单位。10 mm等于1.0 cm，8 mm等于0.8 cm，2 mm等于0.2 cm，所以体积为1.0×0.8×0.2=0.16 cm³。0.20 g除以0.16 cm³，得到1.25 g/cm³。

$$
V=LWH,\qquad \rho=\frac{m}{V}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | 长方体体积，cm³ |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 长度，cm |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | 宽度，cm |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | 厚度，cm |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | 质量，g |
| ![Formula](https://ml-biomat.com/static/agent-math/5903a3ca133db5ae3585d59d.svg) | 质量密度，g/cm³ |

底面积LW沿厚度H延伸得到体积。长度统一为cm且各量为有限正数时，1.0×0.8×0.2=0.16 cm³；0.20 g÷0.16 cm³=1.25 g/cm³。

长度从毫米换成厘米时，每一条都乘0.1；体积包含三条长度，整体换算因子因此是0.001。本章函数先分别转换三种长度，再相乘，能在代码里保留这个物理关系。如果直接用10×8×2得到160，这个数的单位是mm³；把它当成160 cm³，就会把体积放大1000倍，使密度数值缩小1000倍。程序仍然完成了普通乘除，错误发生在数值与单位的对应上。

$$
(1\,\mathrm{mm})^3=(0.1\,\mathrm{cm})^3=0.001\,\mathrm{cm}^3
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/35a3d51ce955f3ec1cc867b0.svg) | 毫米与厘米，长度单位；1 mm=0.1 cm |
| ![Formula](https://ml-biomat.com/static/agent-math/6cb44f25e489afb06ec62d2e.svg) | 指数3表示三个长度因子相乘，产生体积单位 |

体积有三个长度方向，因此换算因子是0.1×0.1×0.1=0.001。160 mm³=0.160 cm³；误用160 cm³会将体积放大1000倍，并使同一质量的密度缩小1000倍。

![构造矩形试样的同尺度尺寸图，以及固定质量0.20 g、长10 mm、宽8 mm时的密度—厚度关系。](https://ml-biomat.com/static/tutorials/python-scientific/figures/fcced9fe87945e4a53cea464.svg?v=fcced9fe8794)

图 2构造矩形试样的同尺度尺寸图，以及固定质量0.20 g、长10 mm、宽8 mm时的密度—厚度关系。

图左用同尺度的上视图和侧视图表示三种尺寸，侧视图在页面中向下分开放置，便于辨认厚度；这个排版间距不属于试样几何。右图固定质量、长和宽，改变厚度。厚度从2增到4 mm，体积加倍，密度变成0.625 g/cm³；减到1 mm，体积减半，密度变成2.5 g/cm³。这里是在比较输入条件下的计算关系，不表示同一材料只通过改变试样厚度就改变了内在密度。若从同一种均匀材料切取不同厚度，质量也会相应变化。

这个区别还能形成一个更贴近实验的检查：同种材料的长、宽保持不变，厚度和质量同时加倍，密度应保持不变。只把质量加倍而尺寸不变，密度才加倍。关系检查告诉我们哪些输入应一起变化，既帮助核对函数，也帮助设计实验记录。矩形体积模型适合这里定义的规则试样；不规则形状需要用与其几何相匹配的体积测量或重建方法，然后再用质量除以体积。

密度数值还依赖实际测量对象。多孔试样若以外轮廓体积作分母，得到的是包含孔隙影响的体积平均密度；若研究实体材料本身，就需要对应的实体体积定义。同样的质量除以不同体积，回答的研究问题不同。本章规则长方体采用外形尺寸定义体积，默认尺寸已经代表所比较的几何量。这个约定应该与输入字段一起保留，后面即使换成更强的数组库，计算对象也不会因接口改变而自动改变。

## 沿着异常回到最小的出错输入

把厚度设为0 mm，函数会发出`ValueError`，说明厚度必须为有限正数。完整程序实际捕获这次异常，提取调用栈并画成图：main调用analyze_specimen，后者调用calibration模块中的density，最终在输入检查处停止。异常最后一行说明问题类型和消息，前面的调用记录说明怎样到达这里。读回溯时可以先看最后的原因，再沿相关调用位置向上找到最初传入的厚度。

![上图来自实际捕获的零厚度异常。下图比较正确单位与漏掉立方换算的结果；对数横轴用等距表示相同倍数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/0e313025ba97f27fe9749533.svg?v=0e313025ba97)

图 3上图来自实际捕获的零厚度异常。下图比较正确单位与漏掉立方换算的结果；对数横轴用等距表示相同倍数。

不同错误把我们带向不同层次。`ModuleNotFoundError`通常需要核对当前解释器与安装或模块位置；`NameError`要求查看当前作用域里是否定义过这个名字；`TypeError`提示操作收到的对象类型不合适；`ValueError`表示类型可能适用，但具体数值不满足操作要求。`SyntaxError`则发生在代码尚未正常执行时，需要检查括号、引号、冒号等语法。先辨认类型，能够选择下一步检查，而不是把所有错误都归结为环境问题。

找出相关输入后，把问题缩成一次函数调用。例如`density(.2, 10, 8, 0)`足以复现零厚度检查，不需要重新执行所有绘图。用`print`查看值与`type`，可以确认传入的是数值0还是字符串`'0'`；在编辑器中设置断点，则可以暂停到调用前查看局部变量。两种方法都在回答“这一行执行时实际拿到了什么”，选择取决于程序复杂程度和当下最需要观察的信息。

修复后保留一个很小的预期检查：本例正常输入应得到1.25 g/cm³，厘米表示同一试样也应得到相同结果，零厚度应进入明确检查。这样，后续改动可以重新验证已经理解的行为。再看图中没有触发异常的单位错误：0.00125被错误地标成g/cm³，数值比正确结果小1000倍。异常检查说明程序是否按约定接受输入，手算、单位和关系检查则帮助确认它算的是正确的科学量。

检查时还要保留完整的相关错误消息。例如，缺少matplotlib与缺少calibration都会表现为找不到模块，但前者可能需要在当前环境安装第三方库，后者则要检查示例的两个文件是否仍放在一起。删除报错行、用一个笼统的except把所有异常吞掉，都会失去这种区别。明确知道怎样处理的异常可以转换成清楚的结果状态；还不知道原因的异常应保留调用信息，用最小输入重新观察。这样，每次修复都对应一个具体原因。

## 两份完整代码，以及一次可复查的运行

先看计算模块。函数明确接收质量、三种长度和长度单位，返回同时包含体积与密度的字典。中间量体积也返回给调用者，使后续能够检查错误发生在体积换算还是质量归一化。输入检查使用`raise ValueError`，因此规则属于函数本身；文档字符串说明单位与返回对象。下面就是随示例提供的全部计算模块，不需要再打开另一个文件才能读到核心算式。

### calibration.py：单位明确的密度函数

保留在main.py旁，作为可导入的本地模块。

```
"""Mass density of a rectangular specimen with explicit length units."""
import math


def density(mass_g, length, width, thickness, length_unit='mm'):
    """Return density in g/cm^3 and volume in cm^3.

    All three lengths share length_unit, either mm or cm.
    Mass and lengths must be finite and strictly positive.
    """
    factors_to_cm={'mm':0.1,'cm':1.0}
    if length_unit not in factors_to_cm:
        raise ValueError('length_unit must be mm or cm')
    for name,value in [('mass_g',mass_g),('length',length),('width',width),('thickness',thickness)]:
        if not math.isfinite(value) or value<=0:
            raise ValueError(f'{name} must be finite and positive')
    factor=factors_to_cm[length_unit]
    volume_cm3=(length*factor)*(width*factor)*(thickness*factor)
    return {'density_g_per_cm3':mass_g/volume_cm3,'volume_cm3':volume_cm3}
```

主程序导入这个函数，计算默认试样和厘米表示的同一试样，再故意调用一次零厚度情况以观察异常。之后读取真实的Python与Matplotlib版本，生成三幅图，并保存结果。调用栈图中的文件名、行号和语句来自这次实际异常，不是事先编写的假报错。`if __name__ == '__main__'`把直接运行入口与导入行为分开；在另一个程序中导入计算模块时，不会连带运行本章的整套绘图。

### main.py：完整运行、图形与运行记录

正常计算与故意触发的异常都产生可检查的输出。

```
"""Run a local module, inspect its runtime, and diagnose a specimen calculation."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import sys
import traceback
import textwrap
from calibration import density
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon


def analyze_specimen(thickness):
    return density(mass_g=.2,length=10,width=8,thickness=thickness,length_unit='mm')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('output'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    baseline=analyze_specimen(2)
    converted=density(.2,1,.8,.2,length_unit='cm')
    assert math.isclose(baseline['density_g_per_cm3'],1.25)
    assert math.isclose(baseline['volume_cm3'],.16)
    assert math.isclose(converted['density_g_per_cm3'],baseline['density_g_per_cm3'])
    assert math.isclose(density(.4,10,8,2)['density_g_per_cm3'],2.5)
    try:
        analyze_specimen(0)
    except ValueError as error:
        failure={'type':type(error).__name__,'message':str(error),'frames':[{'file':Path(frame.filename).name,'function':frame.name,'line':frame.lineno,'statement':frame.line} for frame in traceback.extract_tb(error.__traceback__)]}
    else:
        raise AssertionError('Zero thickness should trigger its input check')
    runtime={'python':platform.python_version(),'implementation':platform.python_implementation(),'executable_name':Path(sys.executable).name,'virtual_environment':sys.prefix!=sys.base_prefix,'matplotlib':importlib.metadata.version('matplotlib')}
    thicknesses=[.5+i*.025 for i in range(141)]
    densities=[analyze_specimen(h)['density_g_per_cm3'] for h in thicknesses]
    unchecked_density=.2/(10*8*2)
    zh=args.language=='zh'
    def tr(z,e):return z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist};family=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':15,'axes.titleweight':'bold','svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36','axes.labelcolor':'#172b36','axes.spines.top':False,'axes.spines.right':False})
    blue,red,green,ink='#28648a','#b85336','#467a62','#172b36'
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg',bbox_inches='tight');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12,7.8),layout='constrained');ax=fig.add_subplot();ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,8)
    ax.text(.2,7.55,tr('PEP 405：把项目依赖分开，同时复用基础Python','PEP 405: separate project packages, reuse a base Python'),fontsize=18,weight='bold')
    ax.text(.2,6.95,tr('2011年提出；随Python 3.3加入标准库。下图表示结构，不指定示意项目的实际版本。','Proposed in 2011; included with Python 3.3. Diagram shows structure, not measured project versions.'),fontsize=12)
    for i,label in enumerate([tr('项目 A','Project A'),tr('项目 B','Project B')]):
        x=.3+i*6;ax.add_patch(Rectangle((x,2.9),5.1,3.3,facecolor=blue if i==0 else green,alpha=.08));ax.text(x+.2,5.72,label,fontsize=19,weight='bold')
        ax.text(x+.2,5.03,tr('环境自己的解释器入口','Environment interpreter entry'),fontsize=14)
        ax.text(x+.2,4.3,'python -m pip',fontsize=17,color=blue if i==0 else green)
        ax.text(x+.2,3.6,tr('本环境的 site-packages','This environment’s site-packages'),fontsize=14)
        ax.add_patch(FancyArrowPatch((x+2.55,2.85),(6,1.75),arrowstyle='->',mutation_scale=20,lw=2,color=blue if i==0 else green))
    ax.add_patch(Rectangle((2.5,.65),7,1.1,facecolor='#d9dfd9'));ax.text(6,1.15,tr('基础Python与共享的标准库','Base Python and shared standard library'),ha='center',fontsize=17)
    ax.text(.3,.1,tr('环境改变导入位置；数据文件、分析脚本和科学单位仍需明确。','An environment changes import locations; data, scripts, and scientific units remain explicit.'),fontsize=12)
    save(fig,'environment-history')

    fig=plt.figure(figsize=(12,7.3),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1,1.25])
    ax=fig.add_subplot(gs[0]);ax.set_aspect('equal');ax.set_xlim(-1,12);ax.set_ylim(-2,12)
    ax.add_patch(Rectangle((0,3),10,8,facecolor=blue,alpha=.16,edgecolor=blue,lw=2));ax.add_patch(Rectangle((0,0),10,2,facecolor=green,alpha=.18,edgecolor=green,lw=2))
    ax.text(5,7,tr('上视图：10 × 8 mm','Top view: 10 × 8 mm'),ha='center',fontsize=14);ax.text(5,1,tr('侧视图：厚度2 mm','Side view: thickness 2 mm'),ha='center',va='center',fontsize=13)
    ax.set(xlabel=tr('长度坐标 / mm','Length coordinate / mm'),ylabel=tr('示意平面坐标 / mm','Diagram coordinate / mm'),title=tr('a  定义体积所需的三种长度','a  Three lengths define the volume'));ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[1]);ax.plot(thicknesses,densities,color=blue,lw=2.5)
    for h in [1,2,4]:
        value=analyze_specimen(h)['density_g_per_cm3'];ax.scatter(h,value,color=red,s=65);ax.annotate(f'{h:g} mm → {value:g} g/cm³',(h,value),xytext=(h-.25 if h<4 else 2.9,value+.35),fontsize=12,bbox={'facecolor':'#fbfaf6','edgecolor':'none','alpha':.9,'pad':2})
    ax.set(xlabel=tr('厚度 / mm','Thickness / mm'),ylabel=tr('质量密度 / g·cm⁻³','Mass density / g·cm⁻³'),title=tr('b  同一质量下，厚度决定体积','b  Thickness changes volume at fixed mass'),ylim=(0,5.5),xlim=(.4,4.7));ax.grid(alpha=.15)
    ax.text(1.3,4.5,tr('质量0.20 g；长10 mm；宽8 mm','Mass 0.20 g; length 10 mm; width 8 mm'),fontsize=11)
    save(fig,'density-sensitivity')

    fig=plt.figure(figsize=(12,9),layout='constrained');gs=fig.add_gridspec(2,1,height_ratios=[1.65,1]);ax=fig.add_subplot(gs[0]);ax.axis('off');ax.set_xlim(0,12);ax.set_ylim(0,5.5)
    ax.text(.1,5.2,tr('a  实际捕获的调用路径：厚度0 mm','a  Captured call path: thickness 0 mm'),fontsize=17,weight='bold')
    for i,frame in enumerate(failure['frames']):
        y=4.55-i*1.25;ax.text(.2,y,f"{frame['file']}:{frame['line']}  |  {frame['function']}",fontsize=13,color=blue);ax.text(.45,y-.35,textwrap.fill(frame['statement'],width=88),fontsize=10.5,va='top')
    ax.text(.2,.35,f"{failure['type']}: {failure['message']}",fontsize=16,color=red)
    ax=fig.add_subplot(gs[1]);labels=[tr('统一成cm后计算','Convert to cm before calculating'),tr('mm³数值误标成cm³','Mislabel numerical mm³ as cm³')];values=[baseline['density_g_per_cm3'],unchecked_density]
    ax.scatter(values,[1,0],s=100,color=[blue,red]);ax.plot(values,[1,0],color='#aab5b2',ls='--');ax.set_xscale('log');ax.set(yticks=[1,0],yticklabels=labels,xlabel=tr('被报告的密度数值 / g·cm⁻³','Reported density value / g·cm⁻³'),xlim=(.0005,5),ylim=(-.5,1.5),title=tr('b  没有异常的计算，也要核对单位','b  Check units even when arithmetic completes'));ax.grid(axis='x',alpha=.15)
    for value,y in zip(values,[1,0]):ax.annotate(f'{value:g}',(value,y),xytext=(8,12),textcoords='offset points',fontsize=14)
    ax.text(.015,.5,tr('相差1000倍','A factor of 1000'),fontsize=15,color=red)
    save(fig,'diagnostic-evidence')
    summary={'dataset':'Constructed rectangular specimen','inputs':{'mass_g':.2,'length_mm':10,'width_mm':8,'thickness_mm':2},'baseline':baseline,'same_specimen_in_cm':converted,'incorrect_density_if_mm3_labeled_cm3':unchecked_density,'unit_error_factor':baseline['density_g_per_cm3']/unchecked_density,'runtime':runtime,'captured_failure':failure,'source_sha256':{n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ['main.py','calibration.py']}}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    (args.output/'runtime.json').write_text(json.dumps(runtime,indent=2),encoding='utf8')
    print(json.dumps({'baseline':baseline,'runtime':runtime,'failure_type':failure['type'],'unit_error_factor':summary['unit_error_factor']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
```

运行后的数值摘要包含体积0.16 cm³、密度1.25 g/cm³、错误单位演示值0.00125及1000倍差异，还包含捕获的ValueError和运行版本。版本记录说明这次计算使用了怎样的工具组合，代码文件摘要则帮助检查代码是否改变。重新运行时可以先比较物理数值，再查看版本和文件变化；不同电脑的字体与图形输出字节可能不同，即使计算相同，也应把数值复现与图像文件完全相同分开判断。

笔记本中的状态需要特别留意：先运行后面的单元格、再修改前面的变量，屏幕上可能混合不同阶段的结果。准备保存一次完整分析时，重启内核并按顺序执行全部单元格，能检验程序是否依赖某个未写进文档的旧变量。脚本从入口顺序执行，便于暴露这类依赖；笔记本适合逐步探索，两者可以围绕同一个计算模块配合使用。把核心规则放在模块中，也使图文探索与完整运行采用相同算式。

运行记录描述这次实际用到的版本，依赖清单描述重建环境时希望安装的工具，两者承担不同职责。安装工具还需要结合Python版本与操作系统选择可用分发文件。保存成功运行的依赖约定和实际版本，再用一个手算可核对的小例子检验重建结果，可以把“安装完成”接到“目标计算成功”上。这里选择密度算例，就是因为输入简单、单位关系明确，能够先检查整条运行链，再接入更大的实验数据。

## 选择运行入口，再检查计算含义

实验分为两层。先选择解释器入口与安装目标，观察绘图库是否对当前入口可见；这部分是解释导入关系的教学模型，不会在电脑上安装任何软件。接着改变试样厚度、质量和单位处理，观察几何、密度曲线与结果状态。让质量和厚度同时加倍，可以验证同一密度的关系；把厚度改为零，会进入输入检查；故意省略毫米换算时，程序仍能乘除，但单位比较会显示1000倍差异。

### 实验：入口、单位与几何一起核对

A、B是示意环境；选择的安装目标决定哪个环境能找到绘图库。曲线表示当前质量的正确密度关系，红点表示实际报告值。

[Figure: 环境与导入关系](https://ml-biomat.com/tutorials/python-scientific/p06/#P06-route)

[Figure: 试样几何和密度曲线](https://ml-biomat.com/tutorials/python-scientific/p06/#P06-plot)

环境图回答“代码在哪一套工具里执行”，调用栈回答“哪一次操作遇到问题”，单位与关系图回答“结果是否符合测量定义”。把这三条线分别看清，再接成完整流程，就能有方向地处理运行问题。基础部分到这里已经具备变量、记录、函数、文件和环境这几块积木；下一章把成批的数值组织成数组，让相同计算沿着明确的维度一次作用于许多观测。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P06.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Python Tutorial — Virtual Environments and Packages](https://docs.python.org/3.14/tutorial/venv.html)

   环境与包安装入口

   PSF License
2. [Python Packaging User Guide — Installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

   解释器绑定的安装方式，技术事实参考

   CC BY-SA 3.0 documentation; no adapted prose reproduced
3. [Python Tutorial — Modules](https://docs.python.org/3.14/tutorial/modules.html)

   模块、导入与入口条件

   PSF License
4. [Software Carpentry — Errors and Exceptions](https://swcarpentry.github.io/python-novice-inflammation/09-errors.html)

   沿回溯定位输入的教学方法，采用原创密度案例

   CC BY 4.0 lessons; MIT code
5. [PEP 405 — Python Virtual Environments](https://peps.python.org/pep-0405/)

   2011年提案、Python3.3与共享标准库机制

   Public domain
6. [Python — Downloads and platform installation](https://www.python.org/downloads/)

   解释器获取与平台安装入口。

   Python Software Foundation website; factual installation reference.
