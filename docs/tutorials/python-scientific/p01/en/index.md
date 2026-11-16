# A First Program That Answers a Question

Source: https://ml-biomat.com/tutorials/python-scientific/p01/en/
Language: en

Start with three weighings to understand variables, execution order, and two different ratios.

## How much water has a swollen gel actually retained?

Place a small piece of dry gel in water, leave it for a while, remove easily draining surface water, and weigh it again. The specimen will often be heavier. Variations of this familiar process occur in absorbent materials, dressings, soft contact materials, and many laboratory specimens. Comparing the increase in grams is a useful beginning, but a larger starting specimen can usually retain more water simply because there is more material. To compare specimens meaningfully, we need to turn the weighings into a clearly defined result, such as grams of retained water per gram of dry material. This chapter builds a first Python program around that question and connects every calculation to its physical meaning.

We will use deliberately constructed teaching readings: an empty container weighs 0.40 g, the container with the dry specimen weighs 1.60 g, and the container with the wet specimen weighs 5.20 g. The symbol g means grams, and all three readings use that unit. Simple numbers make it possible to check the program with pencil and paper; these values do not describe the performance of a particular product. The same container appears in both specimen weighings, so its mass must be removed from each total. If containers change, each container needs its own recorded mass. A calculation is useful only when the numbers being combined refer to the intended objects.

Imagine unpacking two parcels. The balance measures a container together with its contents, whereas the question concerns the contents. Removing the container contribution gives the dry mass in one case and the wet mass in the other. Their difference is the increase in mass, which we call retained water in this water-uptake example. An actual experiment would specify soaking time, surface-water handling, and the initial dry state. If material also dissolves, the mass change includes that loss as well. Defining the physical process first gives the variables, equations, and figures a common interpretation.

By the end of the chapter, you will be able to save and run a short program, follow how assignment statements produce its results, distinguish numerical values from displayed text, and compare two ratios with different denominators. The complete example also generates three figures and a numerical summary. On a first reading, begin with the weighing calculation near the top of the script, then examine how its results are plotted and saved. The central task remains the same throughout: explain three weighings clearly enough that both a person and a program can follow the reasoning.

![Mass accounting for three constructed weighings. The gray container contributes 0.40 g to every total; the composition diagram excludes it before comparing dry material and retained water.](https://ml-biomat.com/static/tutorials/python-scientific/figures/8d493975c13de6a158f4581e.svg?v=8d493975c13d)

Figure 1Mass accounting for three constructed weighings. The gray container contributes 0.40 g to every total; the composition diagram excludes it before comparing dry material and retained water.

## A program is a calculation that can be executed again

A calculator can immediately evaluate `1.60 − 0.40`. When another set of readings arrives tomorrow, however, someone must remember the entire sequence: subtract the container, calculate the increase, and divide by the dry mass. Individual calculator results do not necessarily preserve that sequence. A program records it as text that can be saved and executed again. Python is a programming language: it defines how that text represents numbers, calculations, and actions. A Python interpreter is the software that reads and executes the statements. The distinction resembles the difference between a system of musical notation and an instrument that plays from a score, although a program assigns precise computational meanings to its instructions.

There are two common ways to use the interpreter. An interactive session accepts a statement and shows its result immediately, which is useful for trying an expression. A script contains a saved sequence of statements that can be executed from the beginning. A file whose name ends in `.py`, such as `main.py`, is normally a Python script. An editor changes the contents of that file, a terminal accepts the command that launches it, and the interpreter executes the Python code. Keeping these three roles separate helps make an unfamiliar computing environment easier to understand. [Chapter six](https://ml-biomat.com/tutorials/python-scientific/p06/en/) explains installation and environment checks in detail; here we focus on what a working program does.

The short example below contains the calculation itself. Text following `#` is a comment for the reader and does not participate in arithmetic. The operators `-` and `/` mean subtraction and division, while `print(...)` displays the content inside its parentheses. Examples shown in an interactive interpreter sometimes include a prompt before each input line; the code blocks here contain code that can be saved directly, without those prompts. Python expressions use ordinary programming punctuation, including parentheses and a decimal point. Explanations belong in comments or quoted strings, where they remain clearly separate from arithmetic.

### Three inputs, two ratios

Sequential execution gives 1.200 g, 3.600 g, 3.000 g/g, and 75.0%.

```
# Constructed balance readings, all in grams.
tare_g = 0.4
dry_total_g = 1.6
wet_total_g = 5.2
dry_g = dry_total_g - tare_g
wet_g = wet_total_g - tare_g
water_g = wet_g - dry_g
uptake_g_per_g = water_g / dry_g
water_fraction = water_g / wet_g
print(f"Dry mass: {dry_g:.3f} g")
print(f"Retained water: {water_g:.3f} g")
print(f"Dry-basis uptake: {uptake_g_per_g:.3f} g/g")
print(f"Water fraction: {water_fraction:.1%}")
```

Read the code from top to bottom: first establish the three readings, then obtain the dry and wet masses, next calculate water mass, and finally form the ratio. This order expands a dependency relationship. Water mass depends on the dry and wet values, which depend on the balance readings. Executing the ratio line before the names above it have values leaves the interpreter without a numerator or denominator. Running a saved script from its beginning recreates this chain from the same starting point. The result can therefore be reproduced and its intermediate steps inspected, rather than accepted as an isolated number.

## Names reveal what the numbers mean and when they change

Read `tare_g = 0.4` as “associate the name `tare_g` with the value 0.4.” Tare refers to the empty container contribution, and the suffix `_g` reminds the reader that the unit is grams. A variable is a name used to refer to a value. Assignment does not establish a permanently recalculated spreadsheet formula. Python first evaluates the expression on the right of `=`, then assigns its result to the name on the left. When `dry_g = dry_total_g - tare_g` executes, it reads the two input values available at that moment, performs the subtraction, and associates the resulting number with `dry_g`.

A small change makes this behavior visible. Calculate the dry mass, then change only `dry_total_g` to 1.8. The existing value of `dry_g` still holds the earlier result. Execute the subtraction again and it becomes approximately 1.4 g. Assignment saves the result of the current execution; it does not promise to update whenever another name changes. This matters in notebooks, where code is divided into cells that can be run in different orders. A new input can coexist with an old calculated value. When edited readings and an unchanged figure appear together, follow the dependencies and rerun the calculations instead of assuming that visible cell order records execution order.

Names also determine how easily another person can check a program. Calling the dry mass `a` and the wet mass `b` still allows arithmetic, but requires a separate key to their meanings. Names such as `dry_g`, `wet_g`, and `water_g` carry the object and its unit into the calculation. Python is case-sensitive: `dry_g` and `Dry_g` are different names. Underscores join words without introducing spaces into a name. A unit suffix is a human convention, however; the interpreter does not automatically convert milligrams to grams because a name ends in `_g`. The inputs and calculations must establish compatible units explicitly.

Numbers and text have different roles. The value `0.4` can participate in subtraction, while `"0.4 g"` is a string of characters suitable for display. Strings can contain words, spaces, and unit labels, but that does not make them numerical masses. Calculating with numbers first and adding explanatory text at the output stage keeps these roles clear. The following diagram separates measurements, expressions, and displayed output. It also connects this readable expression style to Python's origins as a language designed to work with existing tools, a useful theme for the scientific libraries introduced later.

![The upper panel follows inputs, an expression, and output. The lower panel connects Python’s early design context to readable code that accesses existing tools. Original historical-method schematic.](https://ml-biomat.com/static/tutorials/python-scientific/figures/acd2cf928dc3c09596eb2f5f.svg?v=acd2cf928dc3)

Figure 2The upper panel follows inputs, an expression, and output. The lower panel connects Python’s early design context to readable code that accesses existing tools. Original historical-method schematic.

## Balance the mass account before choosing a ratio

Removing the container contribution is a simple subtraction, but it defines the starting point for every ratio that follows. A 0.40 g container and 1.20 g of dry material reproduce the first total reading of 1.60 g. Adding 3.60 g of retained water reproduces the second total reading of 5.20 g. The first figure gives these contributions consistent colors, so that the same material can be followed across different weighings. The colors perform an explanatory job: they identify what has been removed and what remains after each subtraction.

$$
m_d=M_d-m_c,\qquad m_w=M_w-m_c,\qquad m_a=m_w-m_d
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | Net dry-material mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/9161e0473b88657dd837c6df.svg) | Container plus dry-specimen reading, g |
| ![Formula](https://ml-biomat.com/static/agent-math/da91b33ee64dd3e861a37f01.svg) | Empty-container mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | Net wet-specimen mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | Container plus wet-specimen reading, g |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | Retained-water mass in this uptake example, g |
| ![Formula](https://ml-biomat.com/static/agent-math/1526ecedf7893f4ee28503c0.svg) | Subtract a known contribution from a total |

Remove the same container contribution from both totals: 1.60−0.40=1.20 g; 5.20−0.40=4.80 g; 4.80−1.20=3.60 g. The last difference is assigned to water under the stated unchanged-dry-material assumption.

Once water mass is known, we must decide what comparison is useful. Dividing by dry mass describes water uptake relative to the amount of starting material. Imagine resizing every specimen so that it started with exactly one gram of dry material, while scaling its retained water by the same factor. The quotient describes the corresponding amount of water. Here, 3 g/g means three grams of retained water for each gram of dry material. The ratio can exceed one because the water arrives from outside the specimen. Expressing this dry-basis ratio as a percentage gives 300%, so its denominator must remain visible in the description.

$$
q=\frac{m_a}{m_d}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Dry-basis water uptake; g/g, dimensionless after mass units cancel |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | Retained-water mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | Positive dry-material mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/88a00dfa266c2fd007f2ab5e.svg) | Divide the numerator by the denominator; denominator must be nonzero |

3.60 g divided by 1.20 g gives 3.00 g/g: three grams of water per gram of dry material. Its percentage expression is 300%, still on a dry-material basis.

A different question asks how much of the wet specimen's current mass is water. That calculation divides water mass by wet mass. The same 3.60 g of water makes up three quarters of the 4.80 g wet specimen, giving a water mass fraction of 75%. Both results describe the same physical object. The apparent difference between 300% and 75% comes from the reference quantity, just as “percentage increase” and “percentage of the current total” answer different everyday questions. Writing the numerator and denominator explicitly preserves that distinction all the way into a figure caption or report.

$$
w=\frac{m_a}{m_w}=\frac{q}{1+q}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | Water mass fraction of the wet specimen, dimensionless; percentage display is 100w% |
| ![Formula](https://ml-biomat.com/static/agent-math/c2d8ca155f55a24d4711b346.svg) | Retained-water mass, g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | Net combined mass of dry material and water, g |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Water-to-dry-material mass ratio, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | Unit ratio obtained by dividing dry mass by itself, dimensionless |

The wet specimen contains dry material plus water. Dividing both numerator and denominator by dry mass gives q/(1+q). Here 3.60/4.80=3/(1+3)=0.75, displayed as 75%.

The curves below show what the denominator does across a wider range. With dry mass fixed at 1.20 g, increasing water mass makes the water-to-dry-material ratio rise along a straight line. The water fraction of the wet specimen instead approaches 100%, because adding water increases both its numerator and its denominator. The first quantity compares uptake relative to the starting material; the second describes the composition of the present wet specimen. A program can provide both, while the surrounding text and axis labels identify which question each result answers.

![With dry mass fixed at 1.20 g, increasing water mass gives a linear dry-basis ratio and a curved wet-basis fraction.](https://ml-biomat.com/static/tutorials/python-scientific/figures/7eb02a694c2814267b269c83.svg?v=7eb02a694c28)

Figure 3With dry mass fixed at 1.20 g, increasing water mass gives a linear dry-basis ratio and a curved wet-basis fraction.

## A readable language that could reach other tools

Python grew from a practical problem: how could people express work clearly while still accessing capabilities already available on a computer? In the official Python FAQ, Guido van Rossum describes experience implementing the ABC language and working on the Amoeba distributed operating system. ABC offered ideas for readable language design, while system work required access to existing interfaces and ways to handle errors during execution. Python brought these concerns together. Development began in late 1989, followed by a public release in 1991. That background helps explain how the same language can express a short calculation and later connect files, numerical computation, and graphics.

The useful historical lesson is the division between expressing a method and providing the tools that execute it. Dry mass equals a total reading minus a container contribution: this is a scientific relationship a person can understand. Expressing it in Python allows the interpreter to repeat the operation. When a graph is needed, a specialized plotting library supplies the machinery for axes, lines, and output files. This resembles a laboratory specimen moving between a balance, a microscope, and analysis software. Each tool performs a distinct task, and the information exchanged between them must retain a consistent meaning.

A library is a collection of existing functionality that another program can use. The complete example uses Matplotlib to make figures, so the program does not need to position every screen pixel itself. Python's built-in `json` module stores numerical results in structured text. An `import` statement makes these capabilities available to the script. The scientific calculation remains ordinary subtraction and division; the plotting library receives the resulting numbers and displays them. This separation also helps locate problems. An incorrect ratio calls for examining the data and arithmetic, whereas a correct ratio with a clipped label calls for examining the figure layout.

The same arrangement lets a first program grow gradually. A list can hold several specimens, a function can express one reusable calculation, and arrays or tables can organize larger batches. Each step introduces an expression tool that solves a new problem, while the mass account remains valid. Learning a library therefore involves more than memorizing function names. It means understanding what objects represent the data, what operations act on those objects, and how the operations correspond to a scientific question. The small weighing example provides a stable reference while those tools become more capable.

## Read the output and check what a plausible number means

The short program gives a dry mass of about 1.20 g, retained water of about 3.60 g, and dry-basis uptake of about 3.00 g/g. Displaying some intermediate values without formatting may reveal a tail such as `1.2000000000000002`. It arises from representing decimal fractions with a finite binary representation, rather than from additional balance precision. The next chapter explains the mechanism. For now, distinguish the stored numerical value from the number of decimal places chosen for display. The full example prints masses to three decimal places and percentages to one; formatting changes the appearance of the result, not the measurement process.

The expression `f"{dry_g:.3f} g"` creates a formatted string. The initial `f` asks Python to insert expression values at the braces, `dry_g` identifies the value, and `.3f` requests three digits after the decimal point. The final `g` is ordinary unit text. Percentage formatting, such as `.1%`, multiplies a fraction by 100 for display and adds a percent sign, so an internal value of 0.75 appears as 75.0%. Checking whether the stored value is a fraction or an already scaled percentage prevents a second multiplication that would turn 75 into a misleading 7500% display.

Useful checks begin with relationships that can be explained by hand. Dry specimen plus container should reproduce the dry total. Wet specimen plus container should reproduce the wet total. Dry material plus retained water should reproduce the wet mass. Setting the wet total equal to the dry total should give zero retained water and zero for both uptake ratios. Doubling every weighing should double the absolute masses while leaving both ratios unchanged. These checks examine mass accounting, a zero-change case, and a scale transformation. Together they explain why the calculation behaves as it should across several inputs.

The physical relationships also define valid inputs. The dry total must exceed the container mass so that the dry mass is positive and can serve as a denominator. In this pure water-uptake example, wet mass should be at least dry mass. If a record violates these conditions, inspect the recorded weighings, units, and experimental process. Replacing a negative value with zero would change the record and conceal the reason for the discrepancy. A useful program message identifies the relationship requiring attention. The interactive experiment makes those relationships visible beside the inputs so that an invalid state produces an interpretable explanation.

## Run the complete example: calculate, plot, and save

The complete script below includes both the scientific calculation and the code that produces all three figures. Its opening weighings and arithmetic match the short example. The following sections configure fonts and colors, construct the plots, and save the results as `summary.json`. Each JSON key names a field, such as `water_g`, whose value can be read into another analysis. That is more useful for further computation than recovering a number from an image. SVG preserves vector lines and text for enlargement, while PNG stores a pixel image that is convenient in many general-purpose applications.

### Complete calculation and figure script

Requires Matplotlib; the calculation uses built-in Python numbers. All outputs are written to the chosen results folder.

```
"""Mass accounting for a gel: a complete, deterministic teaching example."""
from pathlib import Path
import argparse
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en

    # Readings are constructed teaching data, all in grams.
    tare_g = 0.4
    dry_total_g = 1.6
    wet_total_g = 5.2
    dry_g = dry_total_g - tare_g
    wet_g = wet_total_g - tare_g
    water_g = wet_g - dry_g
    uptake_g_per_g = water_g / dry_g
    water_fraction = water_g / wet_g
    print(f"Dry material: {dry_g:.3f} g")
    print(f"Retained water: {water_g:.3f} g")
    print(f"Water per dry material: {uptake_g_per_g:.3f} g/g")
    print(f"Water fraction of wet specimen: {water_fraction:.1%}")

    available = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ["Noto Sans CJK SC", "Microsoft YaHei", "DejaVu Sans"] if f in available), "DejaVu Sans")
    plt.rcParams.update({"font.family": family, "font.size": 12, "axes.titlesize": 15,
                         "axes.titleweight": "bold", "svg.fonttype": "none",
                         "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6",
                         "text.color": "#172b36", "axes.labelcolor": "#172b36",
                         "axes.spines.top": False, "axes.spines.right": False})
    ink, dry_color, water_color, tare_color = "#172b36", "#b85336", "#28648a", "#bfc6c5"
    def save(fig, name):
        fig.savefig(args.output / f"{name}-{args.language}.svg", bbox_inches="tight")
        fig.savefig(args.output / f"{name}-{args.language}.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig = plt.figure(figsize=(12, 6.5), layout="constrained")
    grids = fig.add_gridspec(1, 2, width_ratios=[1.3, 1])
    ax = fig.add_subplot(grids[0])
    labels = [tr("空容器", "Container"), tr("干样 + 容器", "Dry + container"), tr("湿样 + 容器", "Wet + container")]
    ax.barh(labels, [tare_g]*3, color=tare_color, label=tr("容器", "Container"), height=.52)
    ax.barh(labels, [0,dry_g,dry_g], left=[tare_g]*3, color=dry_color, label=tr("干材料", "Dry material"), height=.52)
    ax.barh(labels, [0,0,water_g], left=[tare_g,tare_g,dry_total_g], color=water_color, label=tr("留存水", "Retained water"), height=.52)
    for i, value in enumerate([tare_g,dry_total_g,wet_total_g]):
        ax.text(value+.07, i, f"{value:.2f} g", va="center")
    ax.set(xlim=(0,6.3), xlabel=tr("天平总读数 / g", "Total balance reading / g"), title=tr("a  把每次称量拆开", "a  Account for each weighing"))
    ax.invert_yaxis(); ax.legend(loc="upper right", frameon=False)
    ax.grid(axis="x", alpha=.16); ax.set_axisbelow(True)
    ax = fig.add_subplot(grids[1]); ax.axis("off")
    ax.set_title(tr("b  同一份湿样中的质量", "b  Mass inside the wet specimen"), loc="left")
    ax.add_patch(Rectangle((.08,.28),.84,.42,facecolor=water_color,transform=ax.transAxes))
    ax.add_patch(Rectangle((.08,.28),.84*(1-water_fraction),.42,facecolor=dry_color,transform=ax.transAxes))
    ax.text(.08+.42*(1-water_fraction),.49,f"{dry_g:.2f} g",color="white",ha="center",va="center",transform=ax.transAxes,fontsize=15)
    ax.text(.08+.84*(1-water_fraction)+.42*water_fraction,.49,f"{water_g:.2f} g",color="white",ha="center",va="center",transform=ax.transAxes,fontsize=18)
    ax.text(.08,.80,tr(f"总湿质量 {wet_g:.2f} g，不含容器", f"Wet mass {wet_g:.2f} g, container removed"),transform=ax.transAxes)
    ax.text(.08,.15,tr(f"干材料 {1-water_fraction:.0%}  |  水 {water_fraction:.0%}", f"Dry material {1-water_fraction:.0%}  |  water {water_fraction:.0%}"),transform=ax.transAxes,fontsize=14)
    fig.suptitle(tr("构造称量数据：相减保留了什么？", "Constructed weighings: what remains after subtraction?"),fontsize=17)
    save(fig,"mass-accounting")

    fig, axes = plt.subplots(1,2,figsize=(12,5),layout="constrained")
    water_values = [i*.03 for i in range(201)]
    axes[0].plot(water_values,[v/dry_g for v in water_values],color=dry_color,lw=2.8)
    axes[0].scatter([water_g],[uptake_g_per_g],s=85,color=ink,zorder=3)
    axes[0].annotate(f"{water_g:.2f} / {dry_g:.2f} = {uptake_g_per_g:.2f}",(water_g,uptake_g_per_g),xytext=(1,4),arrowprops={"arrowstyle":"-","color":ink})
    axes[0].set(ylabel=tr("水 / 干材料（g/g）", "Water / dry material (g/g)"),title=tr("a  干质量作分母：直线", "a  Dry mass denominator: a line"))
    axes[1].plot(water_values,[100*v/(dry_g+v) for v in water_values],color=water_color,lw=2.8)
    axes[1].scatter([water_g],[100*water_fraction],s=85,color=ink,zorder=3)
    axes[1].axhline(100,color="#899496",ls="--",lw=1)
    axes[1].annotate(f"{water_g:.2f} / {wet_g:.2f} = {water_fraction:.0%}",(water_g,100*water_fraction),xytext=(1,30),arrowprops={"arrowstyle":"-","color":ink})
    axes[1].set(ylabel=tr("水 / 湿样（%）", "Water / wet specimen (%)"),ylim=(0,108),title=tr("b  湿质量作分母：逐渐接近100%", "b  Wet mass denominator: approaches 100%"))
    for ax in axes:
        ax.set(xlabel=tr("留存水质量 / g", "Retained water mass / g"),xlim=(0,6)); ax.grid(alpha=.16)
    fig.suptitle(tr(f"固定干质量 {dry_g:.2f} g：两种比例回答两个问题", f"Dry mass fixed at {dry_g:.2f} g: two ratios answer two questions"),fontsize=16)
    save(fig,"denominators")

    fig = plt.figure(figsize=(12,7),layout="constrained")
    ax = fig.add_subplot(); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7)
    ax.text(0,6.65,tr("a  一段表达式如何连接测量与报告", "a  Expressions connect measurements to reports"),fontsize=17,weight="bold")
    boxes=[(.1,4.3,3.2,1.35,f"dry_total_g = {dry_total_g}\ntare_g = {tare_g}",tare_color),
           (4.2,4.3,3.2,1.35,"dry_g = (\n dry_total_g - tare_g\n)",dry_color),
           (8.3,4.3,3.4,1.35,f"print(dry_g)\n{dry_g!r}",water_color)]
    for x,y,w,h,label,color in boxes:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=color,alpha=.13,edgecolor=color,lw=1.2))
        ax.text(x+.15,y+h/2,label,va="center",fontsize=13)
    for x in [3.35,7.45]: ax.add_patch(FancyArrowPatch((x,4.98),(x+.75,4.98),arrowstyle="->",mutation_scale=17,color=ink))
    ax.text(.1,3.72,tr("每次赋值读取当时的数值；修改输入后，需要重新执行后续计算。", "Each assignment reads current values. Changed inputs require recalculating dependent values."),fontsize=12)
    ax.text(0,2.95,tr("b  Python的起点：可读的语言，能连接已有工具", "b  Python's origins: readable language, access to existing tools"),fontsize=17,weight="bold")
    ax.text(.1,2.15,"ABC",fontsize=21,color=dry_color,weight="bold")
    ax.text(.1,1.55,tr("表达与组织容易阅读", "Readable expressions\nand program structure"),fontsize=13)
    ax.text(4.6,2.15,"Python",fontsize=25,color=ink,weight="bold")
    ax.text(4.6,1.55,tr("1989年开始开发\n1991年公开发布", "Development began in 1989\nPublic release in 1991"),fontsize=13)
    ax.text(8.5,2.15,"Amoeba",fontsize=21,color=water_color,weight="bold")
    ax.text(8.5,1.55,tr("访问操作系统的实际需求", "Practical access to\noperating-system services"),fontsize=13)
    ax.add_patch(FancyArrowPatch((2.6,2.2),(4.3,2.2),arrowstyle="->",mutation_scale=17,color=dry_color))
    ax.add_patch(FancyArrowPatch((8.2,2.2),(6.9,2.2),arrowstyle="->",mutation_scale=17,color=water_color))
    ax.text(.1,.45,tr("今天：少量清楚的Python语句，连接数据文件、数值库与绘图工具。", "Today: a few readable Python statements connect files, numerical libraries and plotting tools."),fontsize=13)
    save(fig,"program-history")
    summary={"dataset":"Constructed mass measurements in grams", "tare_g":tare_g,"dry_total_g":dry_total_g,"wet_total_g":wet_total_g,
             "dry_g":dry_g,"wet_g":wet_g,"water_g":water_g,"uptake_g_per_g":uptake_g_per_g,"water_fraction":water_fraction}
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")


if __name__ == "__main__":
    main()
```

Save the script as `main.py` and run the command below from its folder. The word `python` selects the interpreter, `main.py` identifies the script, `--output output` chooses a results folder named `output`, and `--language en` selects English figure text. A folder organizes files, and the relative path `output` begins at the current working location rather than at a fixed directory on a particular computer. Change `en` to `zh` for Chinese figure text. Installation and environment checks for the plotting dependency are developed together in chapter six.

### Run the script

Run from the script folder; the two commands generate English and Chinese figures.

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

The line `def main():` places the workflow inside a function, with indentation marking the statements belonging to it. The entry-point check at the end calls that function when the file runs directly. At this stage, treat the structure as a container around the calculation; [chapter four](https://ml-biomat.com/tutorials/python-scientific/p04/en/) explains how to write functions step by step. When reading a larger script, find the inputs, main calculation, and outputs before studying every layout instruction. The scientific calculation here contains only a few named quantities. The remaining code presents the same results in useful, inspectable forms.

After execution, check the numerical summary before examining the figures. Confirm the three readings, dry mass, water mass, and both ratios. The first figure should let you reconstruct the contributions to each total; the second explains how changing a denominator changes a curve; the third connects program dependencies with the language's design background. Editing an input and rerunning should produce a coherent new set of outputs. Keeping both the script and numerical results preserves the relationship that generated a figure and makes the next modification understandable.

## Change a reading and follow the complete response

The experiment below links balance readings, a mass decomposition, both normalization curves, and the step-by-step calculation. First hold the container and dry totals fixed while increasing the wet total. The blue retained-water contribution grows, the dry-basis result moves along a straight line, and the wet-basis fraction follows a curved response. Next add 0.20 g to all three readings. This represents the same increase in container mass in each weighing, so both net specimen masses and both ratios should remain unchanged. The transformation makes the purpose of tare subtraction directly visible.

### Weighings, composition, and denominators

Enter the three weighings and follow the mass account and both ratios. Dashed curves retain the original dry mass so that changes in water and dry material can be distinguished.

[Figure: Mass contributions to the weighings](https://ml-biomat.com/tutorials/python-scientific/p01/en/#P01-mass)

[Figure: Dry-basis and wet-basis ratio curves](https://ml-biomat.com/tutorials/python-scientific/p01/en/#P01-curves)

For a different comparison, multiply all three readings by two and observe which displays change. The mass bars show absolute quantities in grams; the ratios describe composition or uptake relative to the amount of material. Identical ratios can describe specimens of different sizes, and identical water masses can give different normalized uptake. Consistent variables, units, and graphical labels preserve these distinctions. Following how all views respond to an input change is a way to test the structure of the calculation, beyond obtaining one expected answer.

Finish with a small independent calculation. Set the dry total to 2.40 g, the wet total to 6.40 g, and the container to 0.40 g. Before running the program, calculate a dry mass of 2.00 g, a water mass of 4.00 g, a dry-basis uptake of 2.00 g/g, and a wet-specimen water fraction of approximately 66.7%. Explain each denominator in a complete sentence. The next chapter continues from this foundation, examining units, numerical representations, and finite precision so that every number in a program remains connected to an interpretable quantity.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Software Carpentry — Variables and Assignment](https://swcarpentry.github.io/python-novice-gapminder/02-variables.html)

   Adapts the teaching method of tracing variables and execution order, with an original weighing case and linked figures. Copyright The Carpentries; CC BY 4.0.

   CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; adapted instructional structure, original prose/code/figures.
2. [Python 3.14 Tutorial — An Informal Introduction](https://docs.python.org/3.14/tutorial/introduction.html)

   Language reference for arithmetic, assignment, strings, and print.

   Python Software Foundation documentation license; https://docs.python.org/3.14/license.html
3. [Python 3.14 — Using the Interpreter](https://docs.python.org/3.14/tutorial/interpreter.html)

   Interactive execution and script execution.

   PSF documentation license.
4. [Python FAQ — Why was Python created?](https://docs.python.org/3/faq/general.html#why-was-python-created-in-the-first-place)

   Guido van Rossum’s account of ABC, Amoeba, and Python’s origins.

   PSF documentation license; original historical diagram.
