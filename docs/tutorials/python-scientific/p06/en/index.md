# Running and Understanding Your Python Environment

Source: https://ml-biomat.com/tutorials/python-scientific/p06/en/
Language: en

Connect interpreters, modules, and environments to a density calculation with explicit units.

## Understand what runs on your own computer

After learning to write functions, read files, and produce figures, a new set of problems often appears before calculation starts. A plotting library seems installed, but the program cannot find it. A script runs in a terminal but fails in an editor. A notebook displays an old result after a function has changed. This chapter follows one chain: which Python interpreter executes the code, where it finds modules, which versions it uses, and how an exception points back to a concrete input. The complete example imports a local density function, records its runtime, and draws an actual captured call path.

The scientific object is deliberately small: a constructed rectangular specimen of mass 0.20 g, length 10 mm, width 8 mm, and thickness 2 mm. With consistent units, its volume is 0.16 cm³ and its density is 1.25 g/cm³. Setting thickness to zero exposes an explicit input check. Omitting conversion from millimeters to centimeters exposes a different problem: arithmetic can complete while the reported scientific number is wrong. Environment, program logic, and measurement definition each receive a suitable check.

An interpreter resembles the device that actually carries out a calculation; libraries provide additional capabilities; a script describes the procedure; data supply its inputs. Opening an editor does not identify which interpreter it will use. Several Python installations can coexist on one computer, each with different visible packages. Establishing the execution entry point explains the connection between installation and import without repeatedly reinstalling unrelated tools.

## Identify the process executing the code

For a first installation, obtain the interpreter from the [official Python website](https://www.python.org/downloads/). These examples were checked with Python 3.14; choose a maintenance release in that series when reconstructing the environment. On Windows, follow the [official installation guide](https://docs.python.org/3.14/using/windows.html) to install the Python install manager and select a 3.14 runtime. On macOS, use the official installer and complete the installation and certificate steps in the [macOS guide](https://docs.python.org/3.14/using/mac.html). On Linux, follow the distribution instructions for Python, pip, and venv support. Open a new terminal after installation and run the version checks below. Python and pip version output confirms that both entry points are available. On macOS and Linux the command usually begins with `python3`. If the reported version differs from the intended one, select the corresponding interpreter, such as `py -3.14` on Windows, before creating the project environment.

### Check the interpreter and installer first

Run in the system terminal; on macOS and Linux usually replace python with python3. The reported version and location identify the selected entry point.

```
python --version
python -m pip --version
```

When a terminal receives `python main.py`, it first locates a program named python and then gives main.py to that interpreter. The interpreter executes Python; the editor primarily edits files. A notebook uses a kernel process to execute cells. A terminal, editor, and notebook may select the same interpreter or different environments. When one location works and another does not, comparing their execution entry points is a concrete first step.

### Inspect the active Python interpreter

Run in the execution context being diagnosed and compare the actual interpreter.

```
import sys
print(sys.executable)
print(sys.version)
```

The value `sys.executable` identifies the current interpreter location, while `sys.version` describes the Python version. Inspect these in the terminal process, editor runner, and notebook to see whether they select the same installation. The complete example's shareable outputs retain the executable's filename, version, and environment status. For local diagnosis, inspecting the full location helps identify the installation. Location answers which interpreter is running; version describes the language implementation and interfaces available there.

In `python -m pip`, the option `-m` asks this Python to run a module named pip. Installation is thereby tied to the specified interpreter. A standalone `pip` command may instead be an entry point belonging to another installation. Similarly, `python -m venv` uses the environment-creation module supplied by the selected Python. Read these commands as three parts: select an interpreter, select a module, and supply that module's arguments. Their structure becomes more useful than memorizing an undivided command.

If installation succeeded but an editor cannot import the package, inspect its selected interpreter. For a notebook, inspect its current kernel. After choosing a different kernel, rerun the required cells to establish variables and imports in the new process. An already running process does not automatically replace every in-memory object when a file on disk changes. Installation, interpreter selection, and a fresh execution are separate actions that must connect to the same workflow.

Terminal commands and Python statements belong to different layers. An installation command is interpreted by the operating-system shell; a statement such as `import sys` is interpreted by Python. Placing an installation command directly in an ordinary .py file therefore produces a syntax problem before installation can begin. The prompt helps identify the current layer: interactive Python commonly displays `>>>` while waiting for a statement, whereas a shell waits for a command that launches a program. Copy the command itself, excluding any illustrative prompt. This distinction also explains why notebook commands beginning with special symbols may not transfer unchanged into a script.

## Virtual environments organize project dependencies

Two projects may need different versions of the same library: one uses an older interface while another needs a newer one. Sharing one installation can make upgrades affect work already in progress. A virtual environment provides its own package installation location while using a base Python installation. It is not a complete virtual machine, and it does not automatically copy experimental data or correct units. It organizes which interpreter and packages a project sees.

PEP 405, proposed in 2011 for Python 3.3, brought this mechanism into Python. The proposal discussed difficulties faced by existing environment tools when coordinating with interpreter startup and provided support within the standard library. An environment keeps its configuration and package directory while sharing the base standard library. The figure shows two projects connected to their separate package locations and then to the common base. The file `pyvenv.cfg` records the environment's relationship to that base installation.

![PEP 405 environment structure: projects have separate package locations and share a base standard library. Arrows indicate dependencies.](https://ml-biomat.com/static/tutorials/python-scientific/figures/2478737a2f4058085ee5f64b.svg?v=2478737a2f40)

Figure 1PEP 405 environment structure: projects have separate package locations and share a base standard library. Arrows indicate dependencies.

The next examples give direct interpreter commands for Windows PowerShell and for macOS or Linux terminals. Create `.venv` in the example project, then use its interpreter to install the included dependency requirements and run the analysis. Every command explicitly selects the environment without depending on whether the terminal has activated it. Activation is another convenient route: it changes the terminal's command search order so that the shorter name `python` selects the environment. Both methods can select the same interpreter.

### Windows PowerShell: use the project environment

Run inside the downloaded example directory; each command selects the environment interpreter.

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --output output --language en
```

### macOS and Linux: use the project environment

The same workflow uses the interpreter entry point for these platforms.

```
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py --output output --language en
```

A requirements file names distribution packages and constrains their versions. The command `python -m pip freeze` reports installed package versions and can record a successful environment. A dedicated project environment usually yields a more understandable record than a global installation containing unrelated work. The environment directory itself is normally recreated on another machine because it can contain configuration tied to the local interpreter location. Code, data, dependency information, and execution instructions together allow someone else to reconstruct the workflow.

Think of isolated environments as two drawers. Project A stores its tools in drawer A and project B stores its tools in drawer B; the selected interpreter determines which drawer is opened. Installing a plotting library into B does not make it automatically visible to A. The shared base in the diagram represents common infrastructure beneath those separate package locations. Packages can also require particular versions of other packages. An installer checks these requirements and reports conflicts. Read which packages impose incompatible conditions, then adjust the relevant project requirements. Repeating the same installation command leaves those conditions unchanged.

## A module gives calculation rules a clear location

The preceding chapters separated work into functions. This chapter places the density function in `calibration.py` and uses it from `main.py` through `from calibration import density`. A .py file can serve as a module containing related definitions. Import connects those definitions to another program. With `import calibration`, the call is `calibration.density(...)`; importing density directly allows the shorter function name. The module-qualified form keeps the function's origin visible, while direct import suits a few clearly named functions used frequently.

A library is a general term for reusable functionality. Modules and packages describe how Python organizes importable objects; a package may contain modules and subpackages. The distribution name used by an installer is not always the same as the name imported in code, so consult a library's official installation and import instructions together. Here `math` belongs to the standard library, `matplotlib` is separately installed, and `calibration` is a local module beside the script. All enter through import, but they become available in different ways.

A dot accesses an attribute of an object. The expression `math.isfinite` selects a function from a module, and parentheses call it. The expression `Path('data').parent` accesses the parent-path attribute without calling it. The expression `path.open()` calls a method associated with the path object. Asking what the object is, what the attribute provides, and whether it should be called makes unfamiliar interfaces easier to read. NumPy arrays and pandas tables later use the same relationship between objects and operations.

Import search order can expose an unexpected local file. Naming a script `matplotlib.py`, `csv.py`, or another module name may shadow the library you intended to import. Inspecting a module's `__file__` identifies which file was actually loaded. Rename the local script to describe its task and start a fresh process before importing again. This checks the imported object's identity, much as inspecting the interpreter location checks the execution entry point.

Import also executes statements at a module’s outer level. Place reusable definitions in the module, place the complete task in a main function, and use the entry-point guard to control when that task runs. Otherwise, a program that only wants to borrow a density function may unexpectedly start file operations or plotting. Imported modules are normally cached within the current process, so a second import generally does not execute the whole file again. This helps preserve consistent objects and explains why changing a module may require a fresh process. For a small beginner project, clear file responsibilities and a fresh execution are easy to inspect.

## Begin with a result that can be calculated by hand

Mass density expresses mass per unit volume. For this regular rectangular specimen, volume is length times width times thickness. Length times width gives a base area, and extending that area through the thickness gives the volume. The three lengths must use consistent units. Converting 10, 8, and 2 mm gives 1.0, 0.8, and 0.2 cm. Their product is 0.16 cm³, and 0.20 g divided by this volume gives 1.25 g/cm³.

$$
V=LWH,\qquad \rho=\frac{m}{V}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Rectangular volume, cm³ |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Length, cm |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | Width, cm |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Thickness, cm |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/5903a3ca133db5ae3585d59d.svg) | Mass density, g/cm³ |

The base area LW extended through H gives the volume. With finite positive inputs and lengths in cm, 1.0×0.8×0.2=0.16 cm³; 0.20 g/0.16 cm³=1.25 g/cm³.

Each length acquires a factor of 0.1 when converted from millimeters to centimeters. A volume contains three length factors, giving a combined factor of 0.001. The function converts each length before multiplying, keeping that physical relationship visible in the code. Multiplying the raw numbers 10, 8, and 2 gives 160 mm³. Interpreting this as 160 cm³ enlarges the volume by one thousand and reduces the reported density by the same factor. The computer still performs valid numerical multiplication and division; the error is in the assigned unit meaning.

$$
(1\,\mathrm{mm})^3=(0.1\,\mathrm{cm})^3=0.001\,\mathrm{cm}^3
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/35a3d51ce955f3ec1cc867b0.svg) | Millimeter and centimeter, units of length; 1 mm=0.1 cm |
| ![Formula](https://ml-biomat.com/static/agent-math/6cb44f25e489afb06ec62d2e.svg) | The exponent 3 represents multiplication of three length factors, producing a volume unit |

Volume has three length dimensions, so its conversion factor is 0.1×0.1×0.1=0.001. Thus 160 mm³=0.160 cm³; using 160 cm³ instead enlarges volume by 1000 and divides density for the same mass by 1000.

![Common-scale views of a constructed rectangular specimen and the density–thickness relation at mass 0.20 g, length 10 mm, and width 8 mm.](https://ml-biomat.com/static/tutorials/python-scientific/figures/927810206025f836ce41a372.svg?v=927810206025)

Figure 2Common-scale views of a constructed rectangular specimen and the density–thickness relation at mass 0.20 g, length 10 mm, and width 8 mm.

The left panel shows top and side views at a common spatial scale. The side view is shifted down on the page to expose thickness; that layout gap is not part of the specimen. The right panel fixes mass, length, and width while changing thickness. Increasing thickness from two to four millimeters doubles volume and gives 0.625 g/cm³; reducing it to one millimeter gives 2.5 g/cm³. These are relationships among supplied quantities. Cutting a thicker piece from the same uniform material also increases mass, rather than changing the material's intrinsic density simply through thickness.

This distinction suggests another physically meaningful check. With length and width unchanged, doubling both thickness and mass should preserve density. Doubling mass alone at unchanged dimensions should double it. A relationship check identifies which inputs should vary together, helping both function validation and experiment design. The rectangular-volume model applies to the defined regular specimen. An irregular object needs a volume measurement or reconstruction appropriate to its geometry before the same mass-per-volume definition is applied.

The numerical density also depends on the object being measured. For a porous specimen, using its external envelope volume gives a bulk average that includes the effect of pores. Studying the solid constituent requires a volume definition appropriate to that constituent. The same mass divided by different volumes answers different scientific questions. Here the regular rectangular specimen uses its outer dimensions to define volume, with those dimensions understood to represent the geometry being compared. Keep that convention with the input fields. A more powerful array library can accelerate the arithmetic later, but it does not choose the physical object for us.

## Follow an exception back to its smallest input

Setting thickness to zero raises `ValueError` with a message requiring finite positive thickness. The complete program catches this actual exception and draws the extracted call stack. The main function calls analyze_specimen, which calls density in the calibration module, where the input check stops the operation. The final exception line identifies type and message; the preceding frames show how execution reached that point. Read the final cause first, then follow relevant call sites back to the original argument.

![The upper panel records an actual zero-thickness exception. The lower panel compares correct and omitted cubic-unit conversion; equal distances on the logarithmic axis represent equal ratios.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8219044933f1462992e06ce9.svg?v=8219044933f1)

Figure 3The upper panel records an actual zero-thickness exception. The lower panel compares correct and omitted cubic-unit conversion; equal distances on the logarithmic axis represent equal ratios.

Different error types point toward different layers. `ModuleNotFoundError` prompts an interpreter, installation, or module-location check. `NameError` directs attention to whether a name exists in the relevant scope. `TypeError` indicates an operation received an unsuitable kind of object. `ValueError` describes a value that is inappropriate even when its general type can be used. `SyntaxError` occurs before normal execution and calls for examining punctuation or code structure. Recognizing the type helps select a concrete next check.

Once the relevant input is known, reduce the problem to one call. The expression `density(.2, 10, 8, 0)` reproduces the zero-thickness check without regenerating every figure. Printing a value and its `type` distinguishes numerical zero from the string `'0'`. An editor breakpoint can pause just before the call and expose local variables. Both approaches ask what the operation actually received. The suitable method depends on the size of the program and the state that needs examination.

After a correction, retain a small expectation: normal inputs give 1.25 g/cm³, centimeter inputs for the same specimen give the same density, and zero thickness triggers its check. Later edits can rerun these understood cases. Then examine the unit error that raises no exception: 0.00125 is incorrectly labeled as g/cm³ and is one thousand times too small. Input checks establish whether the function accepts its inputs according to the declared rules; hand calculations, units, and relationships establish what scientific quantity those rules calculate.

Keep the relevant error message intact while diagnosing it. Missing matplotlib and missing calibration can both appear as module-location failures, but their remedies differ. The former may require installing a third-party library into the active environment; the latter calls for checking that the two example files still sit together. Deleting the failing line or swallowing every exception in a broad handler removes this distinction. An understood exception can be converted into a clear result state. An unexplained exception should retain its call information while a smaller input reproduces it, so each correction addresses an identified cause.

## Two complete files and an inspectable run

Start with the calculation module. It receives mass, three dimensions, and a length unit, then returns a dictionary containing volume and density. Returning the intermediate volume helps locate a discrepancy in either dimensional conversion or mass normalization. Explicit `raise ValueError` statements make input rules part of the function, and the documentation string states units and returned objects. The entire calculation module appears below, so its core arithmetic can be read on the page.

### calibration.py: density with explicit units

Keep beside main.py as an importable local module.

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

The main script imports this function, calculates the default specimen and its equivalent centimeter representation, and deliberately calls the zero-thickness case to inspect its exception. It then reads actual Python and Matplotlib versions, creates three figures, and saves results. Filenames, line numbers, and statements in the call-path diagram come from the captured exception rather than a prewritten imitation. The `if __name__ == '__main__'` guard separates direct execution from import. Using the calculation module elsewhere does not automatically generate this chapter's figures.

### main.py: complete calculation, figures, and runtime record

Both the normal calculation and deliberately triggered exception produce inspectable output.

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

The numerical summary contains volume 0.16 cm³, density 1.25 g/cm³, the incorrect-unit demonstration value 0.00125, and their factor of one thousand. It also retains the captured ValueError and runtime versions. Versions identify the tool combination, while code-file digests help identify changes in the source. When repeating a run, compare physical quantities before examining version and file differences. Fonts and image-file bytes may differ between computers even when the same numerical calculation is reproduced.

A notebook's state needs deliberate attention. Running later cells first or editing an earlier variable can leave displayed results from different stages of an exploration. Before retaining a complete analysis, restart the kernel and run all cells in order. This checks whether the document depends on an old variable that is no longer established by its visible code. A script's sequential entry point makes such dependencies easier to expose; a notebook supports incremental exploration. Both can import the same calculation module and therefore use the same scientific definition.

The runtime record is descriptive rather than a universal installation recipe. It reports the versions used by that execution. A requirements file describes what should be installed for another run, and the package manager resolves dependencies available for that Python and platform. Retain both the intended requirements and the observed runtime when an analysis needs to be reconstructed. A small numerical check then confirms that the recreated environment actually performs the expected calculation.

## Select an execution route, then inspect the calculation

The experiment has two layers. Select an interpreter entry point and an installation target to see whether the plotting package is visible to that entry point. This is a teaching model of import relationships and installs nothing on the computer. Then change specimen thickness, mass, and unit handling while observing geometry, the density curve, and the result state. Doubling mass and thickness together checks constant density. Zero thickness triggers validation. Omitting millimeter conversion still permits arithmetic but produces the one-thousand-fold unit discrepancy.

### Experiment: connect the execution route, units, and geometry

A and B are model environments. The installation target determines which can find the plotting package. The curve shows the correct density relation for the current mass; the red point shows the reported value.

[Figure: Environment and import route](https://ml-biomat.com/tutorials/python-scientific/p06/en/#P06-route)

[Figure: Specimen geometry and density curve](https://ml-biomat.com/tutorials/python-scientific/p06/en/#P06-plot)

The environment diagram answers which tool installation executes the code. The call path identifies the operation that encountered a problem. The dimensional and relationship plots connect results to measurement definitions. Joining these lines of reasoning gives a directed approach to execution problems. Variables, records, functions, files, and environments now form the basic working pieces. The next chapter organizes repeated numerical observations into arrays so one calculation can act along an explicitly defined dimension.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Python Tutorial — Virtual Environments and Packages](https://docs.python.org/3.14/tutorial/venv.html)

   Environment and installation workflow

   PSF License
2. [Python Packaging User Guide — Installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

   Interpreter-bound installation; factual technical reference

   CC BY-SA 3.0 documentation; no adapted prose reproduced
3. [Python Tutorial — Modules](https://docs.python.org/3.14/tutorial/modules.html)

   Modules, import, and execution guards

   PSF License
4. [Software Carpentry — Errors and Exceptions](https://swcarpentry.github.io/python-novice-inflammation/09-errors.html)

   Traceback-led diagnosis; an original density case replaces the lesson data

   CC BY 4.0 lessons; MIT code
5. [PEP 405 — Python Virtual Environments](https://peps.python.org/pep-0405/)

   2011 proposal, Python 3.3, and shared standard-library design

   Public domain
6. [Python — Downloads and platform installation](https://www.python.org/downloads/)

   Interpreter downloads and platform installation entry points.

   Python Software Foundation website; factual installation reference.
