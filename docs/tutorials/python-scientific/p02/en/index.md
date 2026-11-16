# Numbers, Units, and Numerical Approximation

Source: https://ml-biomat.com/tutorials/python-scientific/p02/en/
Language: en

Use a thin-film stress calculation to distinguish units, input sensitivity, and floating-point rounding.

## How can one specimen acquire results a million times apart?

A thin strip carries a tensile force of 5 N. Its width is 2 mm and its thickness is 0.10 mm. Dividing the force by its cross-sectional area gives a nominal stress that helps compare tensile loading. The calculation contains only a multiplication and a division, yet a unit mistake can change the result by a factor of one million. Multiplying lengths measured in millimetres produces square millimetres; multiplying lengths measured in metres produces square metres. A program that receives numbers without a consistent interpretation of their units will calculate the wrong quantity just as quickly as the right one, and may print many reassuring decimal places afterwards.

N stands for newtons, a unit of force, and mm stands for millimetres, a unit of length. Imagine pulling two strips of the same material but different cross-sectional sizes. Under the same force, the thinner strip carries that force across a smaller area, giving more force per unit area. Nominal stress normalizes force by the original cross-section. Here the initial section is rectangular, so its area is width multiplied by thickness. Local notches and variations of stress within the section are outside this particular geometric model. The numerical inputs define a teaching example for calculation and scale relationships, rather than a prediction of when a particular film will break.

A second issue may appear in the same analysis: why can `0.1 + 0.2` display as `0.30000000000000004`? A unit mismatch and a tiny finite-representation difference require different responses. More printed digits cannot repair a unit error, and hiding a numerical tail does not change the stored value. We will separate these issues with actual Python computations, then vary thickness to compare how input changes and numerical representation affect the answer. The point is to connect each observed difference to the operation that produced it.

The chapter builds on variables, multiplication, and division from chapter one. New tools include integer and floating-point types, scientific notation, and Python's built-in `math`, `decimal`, and `fractions` modules. The complete example evaluates stress through two consistent unit routes, compares three representations of numbers, and plots thickness sensitivity. Every plotted result follows a defined expression, so a point can be calculated by hand and then located in the numerical summary and figure.

![The same initial rectangular section gives 25 MPa through both unit routes. Analytical curves hold force and width fixed to show thickness in the denominator and asymmetric responses to signed shifts.](https://ml-biomat.com/static/tutorials/python-scientific/figures/49fc4eb1864e0cd4bf67537c.svg?v=49fc4eb1864e)

Figure 1The same initial rectangular section gives 25 MPa through both unit routes. Analytical curves hold force and width fixed to show thickness in the denominator and asymmetric responses to signed shifts.

## Carry the units through the area calculation

One metre contains 1000 millimetres, so one millimetre is 0.001 m. Converting both dimensions gives a width of 0.002 m and a thickness of 0.0001 m. Their product is 0.0000002 m². Keeping millimetres gives an area of 2×0.10=0.20 mm² instead. These expressions describe the same section. Area multiplies two lengths, so each factor of one thousandth must be retained when converting to metres. This produces a factor of one millionth for the area. Thinking of a square grid helps: changing the scale in both horizontal and vertical directions changes the area by the product of the two scale factors.

$$
A=bt,\qquad 1\,\mathrm{mm}^2=(10^{-3}\,\mathrm{m})^2=10^{-6}\,\mathrm{m}^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Rectangular cross-sectional area, mm² or m² consistent with its dimensions |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Initial width, mm or m |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Initial thickness, in the same length unit as width |
| ![Formula](https://ml-biomat.com/static/agent-math/caa594000bc5cab4891fd227.svg) | One thousandth, a dimensionless conversion factor |
| ![Formula](https://ml-biomat.com/static/agent-math/9d3c6e8b3220d80e71bb33eb.svg) | Square, multiplication of two equal factors; area contains two length units |

2 mm×0.10 mm=0.20 mm². Converting each dimension gives 0.002 m×0.0001 m=2×10⁻⁷ m². Area conversion includes both length factors.

Newtons divided by square metres give pascals, written Pa. One million pascals equal one megapascal, written MPa, where the prefix M means one million. Dividing 5 N by 0.0000002 m² gives 25000000 Pa, or 25 MPa. There is also a shorter route: 5 N divided by 0.20 mm² gives 25 N/mm², and one N/mm² equals one MPa. Both routes work because their arithmetic and unit labels remain consistent. Writing the numerical result 25 with a Pa label would attach an incorrect physical interpretation to an otherwise valid division.

$$
\sigma=\frac{F}{A}=\frac{F}{bt},\qquad 1\,\mathrm{N/mm^2}=10^6\,\mathrm{Pa}=1\,\mathrm{MPa}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Nominal stress using the initial section; MPa for N and mm, Pa for N and m |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Axial tensile force, N |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Positive initial cross-sectional area, mm² or m² |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Initial width, mm or m |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Initial thickness, in the same unit as width |
| ![Formula](https://ml-biomat.com/static/agent-math/80f0e0ae45cf90c79ea06edc.svg) | Pascal, 1 Pa=1 N/m² |
| ![Formula](https://ml-biomat.com/static/agent-math/dfc02cd70c8bfefa2abfca40.svg) | Megapascal, 1 MPa=10⁶ Pa |

Nominal stress distributes force across the original rectangular section: 5/0.20=25 N/mm²=25 MPa. In square metres, 5/(2×10⁻⁷)=2.5×10⁷ Pa, or 25 MPa.

Python writes one thousandth as `1e-3`, and `2e-7` means 0.0000002. The letter `e` marks scientific notation here; it is neither a variable name nor the mathematical constant associated with exponential functions. Negative exponents represent repeated division by ten, while positive exponents represent repeated multiplication by ten. Scientific notation makes the magnitude visible without requiring us to count a long sequence of zeros. Unit prefixes perform a related reading task, but belong to a different layer: `1e6` is a number, whereas MPa is a unit containing a factor of one million.

### Two consistent unit routes

Both outputs are 25.0 MPa, reached through N/mm² and N/m².

```
force_N = 5.0
width_mm = 2.0
thickness_mm = 0.1
area_mm2 = width_mm * thickness_mm
stress_MPa = force_N / area_mm2
width_m = width_mm * 1e-3
thickness_m = thickness_mm * 1e-3
area_m2 = width_m * thickness_m
stress_Pa = force_N / area_m2
print(stress_MPa, stress_Pa / 1e6)
```

Names such as `width_mm`, `width_m`, and `area_m2` expose the conversion steps directly. One useful arrangement converts all inputs to a chosen internal unit system, performs the calculation, then converts outputs into convenient reporting units. It reduces repeated conversions scattered across expressions. An analysis can also consistently use newtons and millimetres, provided its formulas and labels follow that choice. Keeping both routes here creates an independent numerical check: agreement between different unit routes can reveal a scale mistake that simply rerunning one expression would reproduce.

## How did measurements acquire a shared metre?

A unit does more than decorate a number. Two laboratories can both record a length of “1” and still describe different objects if they lack a shared reference. The history of the metre illustrates how such references develop. The 1889 definition referred to a platinum–iridium prototype. In 1960, the definition changed to a wavelength of krypton-86 radiation; in 1983, it changed again to the distance travelled by light in vacuum during a specified interval. The International Bureau of Weights and Measures connects this history to improving how the unit can be realized in practice, rather than merely changing the wording of an agreement.

The diagram below draws the comparisons behind these approaches. A prototype ties length to a shared physical artifact. An optical approach relates it to repeatable radiation and interference. A light-speed definition connects length to a time standard. Today the numerical value of light speed in vacuum is fixed at 299792458 metres per second. In the diagram, *c* denotes that speed in m/s and Δ*t* a time interval in seconds; their product is a length in metres. An interval of 1/299792458 second therefore corresponds to one metre. The drawing summarizes the length–time relationship in the definition; practical realization uses precision optical and time-measurement techniques.

![Original schematic of length metrology: artifact marks, optical wavelength comparison, and the definition linking light speed in vacuum with time. The drawings explain methods rather than reconstructing instruments to scale.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e433bbb1b22f0ee60d1b5e11.svg?v=e433bbb1b22f)

Figure 2Original schematic of length metrology: artifact marks, optical wavelength comparison, and the definition linking light speed in vacuum with time. The drawings explain methods rather than reconstructing instruments to scale.

This history separates two questions that easily become confused: whether the unit has a common definition, and how precisely a particular measurement realizes it. A shared definition does not give an ordinary ruler infinitely fine resolution. A balance reporting grams likewise does not make every possible printed digit equally informative. A conversion such as the decimal relationship between millimetres and metres is exact, while the measured thickness still depends on the instrument, sampling location, and specimen surface. Computation propagates those input quantities; it does not supply information absent from the measurement.

Shared unit conventions in scientific software solve a related collaboration problem. One file may use millimetres and another metres; explicit conversions allow them to enter the same analysis. Guessing units from the apparent size of a number lets mistakes persist until much later. Put units in clear field names or metadata when saving data, beside axes when plotting, and in descriptions of what a function expects. This makes units part of the transferable calculation, instead of something one person must remember throughout the workflow.

## Stored numbers occupy a finite set of positions

Python's `int` type is useful for counts, such as the number of specimens or repetitions. Ordinary Python integers can grow by using more storage, with practical limits set by memory and computation time. The common type for numbers written with decimal points is `float`. It uses finite storage to represent a broad range of magnitudes efficiently. Its structure resembles scientific notation: one part records significant digits and another records scale. A finite number of significant digits means that many real numbers must be approximated by a nearby representable value.

A familiar decimal example makes the issue easier to see. Writing one third as 0.3, 0.33, or 0.333 gives successively better approximations, but no finite decimal expansion completes the fraction. Binary fractional places instead represent halves, quarters, eighths, and so on. The number 0.625 can be built exactly from one half and one eighth, while decimal 0.1 requires an endlessly continuing binary expansion. Storage must stop somewhere, so the computer retains a nearby finite representation. The resulting difference follows from the representation system and its finite length.

$$
0.625=1\times2^{-1}+0\times2^{-2}+1\times2^{-3}=\frac12+0+\frac18
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7303dcd9121400b1daa141ec.svg) | Dimensionless number to represent |
| ![Formula](https://ml-biomat.com/static/agent-math/3ecfcbd49f702b154e843aff.svg) | Weights of the first three binary fractional places: 1/2, 1/4, and 1/8, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/dc8c18188ba2a40751b5057e.svg) | Binary digits selecting each weight, either zero or one |
| ![Formula](https://ml-biomat.com/static/agent-math/a28115dcd3646ef2947dff18.svg) | Multiply by the digit and add the contributions |

The binary fraction 0.101 selects one half, zero quarters, and one eighth, giving 0.625. Decimal 0.1 requires continuing binary digits and is approximated in finite storage.

The figure first uses a deliberately simplified fixed-fraction grid so that every permitted position can be inspected. Adding fractional bits makes the grid finer and changes which point lies nearest 0.1. This is a teaching model of rounding. Actual floating-point values also contain a scale component, so spacing changes with magnitude. For the common double-precision format used by Python, adjacent representable values near one are separated by approximately 2.22×10⁻¹⁶. The function `math.ulp(1.0)` reports this spacing. It describes the computer representation and has a different meaning from the resolution of a measurement instrument.

![A toy fixed-fraction binary grid displays rounding positions. Below it are actual Python floating-point, decimal, and rational results. The toy model is explicitly distinguished from actual floating-point format.](https://ml-biomat.com/static/tutorials/python-scientific/figures/7d862c887d417fcf33aedbe9.svg?v=7d862c887d41)

Figure 3A toy fixed-fraction binary grid displays rounding positions. Below it are actual Python floating-point, decimal, and rational results. The toy model is explicitly distinguished from actual floating-point format.

In `0.1 + 0.2`, both inputs already involve binary approximation, and the sum must itself fit a representable value. Printing it can expose a numerical tail. Python normally chooses a compact decimal display, so printing `0.1` by itself often still shows just those three characters. This concise display does not make the stored value an exact tenth. Formatting or calling `round` therefore requires a clear question: are we changing text for the reader, calculating another rounded value, or switching to a genuinely different representation of numbers?

## Choose integers, decimals, or fractions for the quantity

Input from a file or text field often starts as text. The string `"0.10"` contains four characters; `float("0.10")` converts it to a number that can participate in multiplication. Similarly, `int("3")` converts integer text, but `int(3.9)` truncates toward zero and gives three rather than rounding to four. Conversion should follow the meaning of the quantity. Converting a fractional length to an integer simply to remove a display tail would change the measured input. Operators also encode different questions: `/` performs ordinary division, whereas `//` performs floor division. Thus 7/2 gives 3.5 and 7//2 gives three. Floor division can describe how many complete groups fit into a count, but would discard the fractional information needed for an area-normalized calculation. A small syntactic difference changes the operation, so trace a hand-computable example whenever introducing a new operator.

A numerical type should follow the meaning of the data and operations. Specimen counts usually use integers; a fractional record count is not meaningful for that task. Continuous dimensions, forces, and numerical solvers commonly use floating-point values because of their speed, range, and compatibility with scientific libraries. When a calculation must follow decimal input rules, as in explicit accounting or exact decimal recipes, `Decimal` offers decimal arithmetic. Adding `Decimal("0.1")` and `Decimal("0.2")` gives decimal 0.3 exactly. The change concerns representation and arithmetic rules, rather than the number of digits printed afterwards.

The quotation marks matter. `Decimal("0.1")` reads a decimal number from text. In contrast, `Decimal(0.1)` receives an already constructed floating-point value and converts that value exactly to decimal form, including its existing binary approximation. Think of copying two different originals: decimal text supplies the number expressed by the text, whereas a floating-point input supplies the number the computer already stored. Changing the receiving type cannot reconstruct information lost earlier in the data path.

`Fraction` stores a rational number as an integer numerator and denominator. For example, `Fraction(1, 3)` represents one third exactly. Fractions are useful for explaining ratios, checking rational expressions, and representing discrete relationships that require exact rational arithmetic. Repeated complicated operations can produce very large numerators and denominators, increasing computation cost. Many other numbers, including most square roots and pi, have no exact representation as a ratio of two integers. Decimal arithmetic also uses a finite precision for general operations: calculating one third in a twelve-digit context still produces a finite expansion. Each representation solves particular problems.

### Representation and summation

Outputs are 0.30000000000000004, 0.3, 3/10, 0.0, and 1.0.

```
from decimal import Decimal
from fractions import Fraction
import math
print(repr(0.1 + 0.2))
print(Decimal("0.1") + Decimal("0.2"))
print(Fraction(1, 10) + Fraction(2, 10))
print((1e16 + 1.0) - 1e16)
print(math.fsum([1e16, 1.0, -1e16]))
```

Even when individual inputs are representable exactly, an operation can lose a small contribution. Evaluate `1e16 + 1.0` first: near that large value, the representable spacing is too coarse to retain the added unit. Subtracting `1e16` afterwards gives zero, although the mathematical sum of the three terms is one. `math.fsum` improves the treatment of rounding during summation and returns 1.0 for this example. Understanding how the small contribution disappears points toward an appropriate algorithm. Printing extra decimal places after the final zero cannot recover it.

## “Close enough” requires a scale

The operator `==` asks whether two values are exactly equal. That is natural for identifiers, integer counts, and clearly defined discrete states. Values produced through different floating-point routes often call for another question: is their difference smaller than an explicit comparison scale? `math.isclose` expresses that question using parameters. Relative tolerance scales with the magnitude of the compared values; absolute tolerance has the same units as those values. Relative tolerance controls proportional agreement, while absolute tolerance supplies a meaningful comparison scale near zero.

$$
|x-y|\leq\max\!\left(r\max(|x|,|y|),a\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Two values of the same quantity expressed in the same unit |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Nonnegative relative tolerance, dimensionless; rel_tol in math.isclose |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Nonnegative absolute tolerance, in the units of x and y; abs_tol |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | Absolute value, the magnitude without its sign |
| ![Formula](https://ml-biomat.com/static/agent-math/8228983b74c5db73c259fc11.svg) | Select the larger argument |
| ![Formula](https://ml-biomat.com/static/agent-math/97a7392d70b366cf7bc75310.svg) | Less than or equal to; satisfying the rule returns True |

For zero and 10⁻⁹ with r=10⁻⁶ and a=0, the threshold is 10⁻¹⁵ and the difference exceeds it. Setting a=2×10⁻⁹ makes the comparison pass. The relative and near-zero absolute scales serve different roles.

Consider 25.000000000 MPa and 25.000000001 MPa, differing by approximately one billionth of a megapascal. A relative tolerance of 10⁻⁹ permits a difference of about 25×10⁻⁹ MPa, so the values are close under that rule. Compare zero with 10⁻⁹ instead: a relative tolerance of 10⁻⁶ permits only 10⁻¹⁵, so the values are not close. An absolute tolerance of 2×10⁻⁹ explicitly allows that near-zero difference. Tolerance specifies what the comparison is meant to resolve. A numerical implementation check may use a small computational threshold, while comparing physical measurements requires a threshold based on the measurement question.

The 2015 design proposal that led to `math.isclose` specifically examined comparisons near zero. It turned a common need, previously implemented separately in different programs, into an interface with stated behavior. This part of computing history can be read alongside the history of measurement units. One establishes a shared numerical comparison rule; the other establishes a shared physical reference. In both cases a clear rule helps people coordinate, while the application still determines the appropriate scale. A default parameter provides a starting configuration, not an interpretation of the experiment.

An absolute tolerance must be converted when the physical quantity changes units. A difference of 2×10⁻⁹ MPa is the same physical difference as 2×10⁻³ Pa. Converting values to pascals while leaving the numerical absolute tolerance unchanged would change the comparison rule. Relative tolerance is dimensionless and therefore more naturally survives a consistent multiplicative unit conversion. A meaningful account of a successful comparison states the quantity, units, threshold, and routes being compared; together they explain what agreement has actually been checked.

## Run the example and separate three different error mechanisms

The full script first calculates nominal stress using two unit routes, then compares floating-point, decimal, and rational values. It generates figures for thickness sensitivity, finite numerical grids, and the history of length standards. Width and thickness refer to the initial cross-section, so the stress plotted throughout is nominal stress. Using a changing area measured during stretching would define a different quantity and require matching changes to the variables, axes, and explanation. A model's meaning follows these definitions, rather than the superficial appearance of a division.

### Complete calculations and three figures

Numerical calculations use the Python standard library; figures require Matplotlib.

```
"""Units, floating-point representation and thickness sensitivity."""
from pathlib import Path
import argparse
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=="zh"
    def tr(a,b): return a if zh else b

    # Defined teaching model; width and thickness are initial dimensions.
    force_N=5.0; width_mm=2.0; thickness_mm=0.1
    width_m=width_mm*1e-3; thickness_m=thickness_mm*1e-3
    area_mm2=width_mm*thickness_mm
    area_m2=width_m*thickness_m
    stress_Pa=force_N/area_m2
    stress_MPa=stress_Pa/1e6
    stress_from_mm=force_N/area_mm2
    assert math.isclose(stress_MPa,stress_from_mm,rel_tol=1e-12)

    decimal_sum=Decimal("0.1")+Decimal("0.2")
    rational_sum=Fraction(1,10)+Fraction(2,10)
    float_sum=0.1+0.2
    cancellation=(1e16+1.0)-1e16
    stable_sum=math.fsum([1e16,1.0,-1e16])
    with localcontext() as ctx:
        ctx.prec=12
        decimal_third=str(Decimal(1)/Decimal(3))
    print(f"Area: {area_mm2:.3f} mm^2 = {area_m2:.3e} m^2")
    print(f"Nominal stress: {stress_MPa:.3f} MPa")
    print("Float addition:",repr(float_sum),"Decimal:",decimal_sum,"Fraction:",rational_sum)
    print("Cancellation:",cancellation,"math.fsum:",stable_sum)
    print("Near zero, relative-only:",math.isclose(0,1e-9,rel_tol=1e-6))
    print("Near zero, absolute tolerance:",math.isclose(0,1e-9,abs_tol=2e-9))

    fonts={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ["Noto Sans CJK SC","Microsoft YaHei","DejaVu Sans"] if f in fonts),"DejaVu Sans")
    plt.rcParams.update({"font.family":[family,"DejaVu Sans"] if zh else ["DejaVu Sans"],"font.size":12,"axes.titlesize":15,"axes.titleweight":"bold","svg.fonttype":"none","figure.facecolor":"#fbfaf6","axes.facecolor":"#fbfaf6","text.color":"#172b36","axes.labelcolor":"#172b36","axes.spines.top":False,"axes.spines.right":False})
    blue,red,ink,green="#28648a","#b85336","#172b36","#467a62"
    def save(fig,name):
        fig.savefig(args.output/f"{name}-{args.language}.svg",bbox_inches="tight")
        fig.savefig(args.output/f"{name}-{args.language}.png",dpi=180,bbox_inches="tight")
        plt.close(fig)

    fig=plt.figure(figsize=(12,7),layout="constrained")
    gs=fig.add_gridspec(2,2,height_ratios=[.9,1.3])
    ax=fig.add_subplot(gs[0,:]);ax.axis("off")
    ax.text(.01,.87,tr("a  同一截面，两套一致的单位", "a  One cross-section, two consistent unit choices"),fontsize=16,weight="bold",transform=ax.transAxes)
    ax.text(.03,.55,"2.00 mm × 0.10 mm = 0.20 mm²",fontsize=19,color=red,transform=ax.transAxes)
    ax.text(.03,.18,"0.002 m × 0.0001 m = 0.0000002 m²",fontsize=19,color=blue,transform=ax.transAxes)
    ax.text(.64,.55,"5 N / 0.20 mm² = 25 MPa",fontsize=17,color=red,transform=ax.transAxes)
    ax.text(.64,.18,"5 N / (2 × 10⁻⁷ m²) = 25 × 10⁶ Pa",fontsize=15,color=blue,transform=ax.transAxes)
    ts=[.04+i*.001 for i in range(201)]
    ax=fig.add_subplot(gs[1,0]);ax.plot(ts,[force_N/(width_mm*t) for t in ts],lw=2.8,color=blue)
    for t in [.08,.1,.12]:
        y=force_N/(width_mm*t);ax.scatter([t],[y],s=55,color=red);ax.annotate(f"{t:.2f} mm → {y:.2f} MPa",(t,y),xytext=(.13,y+5) if t!=.12 else (.145,6),fontsize=11,arrowprops={"arrowstyle":"-","color":ink})
    ax.set(xlabel=tr("初始厚度 / mm","Initial thickness / mm"),ylabel=tr("名义应力 / MPa","Nominal stress / MPa"),title=tr("b  分母越薄，应力越大","b  A thinner denominator gives higher stress"),xlim=(.04,.24),ylim=(0,66));ax.grid(alpha=.15)
    ax=fig.add_subplot(gs[1,1]);errors=[-.4+i*.004 for i in range(201)]
    ax.plot([100*e for e in errors],[100*(1/(1+e)-1) for e in errors],color=red,lw=2.8)
    ax.axhline(0,color=ink,lw=.8);ax.axvline(0,color=ink,lw=.8)
    ax.scatter([-20,20],[25,-100/6],s=60,color=ink)
    ax.set(xlabel=tr("厚度输入相对偏差 / %","Relative thickness-input shift / %"),ylabel=tr("应力结果相对变化 / %","Relative stress change / %"),title=tr("c  相同正负偏差，影响并不对称","c  Equal signed shifts have unequal effects"));ax.grid(alpha=.15)
    save(fig,"units-sensitivity")

    fig=plt.figure(figsize=(12,7),layout="constrained")
    gs=fig.add_gridspec(2,2,height_ratios=[1.2,1])
    ax=fig.add_subplot(gs[0,:]);ax.set_xlim(-.025,.38);ax.set_ylim(-.35,1.7);ax.axis("off")
    ax.set_title(tr("a  玩具数轴：固定小数位，展示有限刻度", "a  A toy fixed-fraction grid makes finite spacing visible"),loc="left")
    for row,bits in enumerate([3,5,8]):
        y=1.3-row*.55;step=2**(-bits);ax.hlines(y,0,.35,color="#bcc7c7",lw=1)
        for k in range(int(.35/step)+1):ax.vlines(k*step,y-.05,y+.05,color=blue,lw=1)
        rounded=round(.1/step)*step;ax.scatter([rounded],[y],s=65,color=red,zorder=3)
        ax.annotate(f"{bits} bits: {rounded:.7f}",(rounded,y),xytext=(.19,y+.07),fontsize=12,arrowprops={"arrowstyle":"-","color":red})
    ax.axvline(.1,ymin=.13,ymax=.9,color=ink,ls="--",lw=1.4);ax.text(.1,-.2,"0.1",ha="center",fontsize=14)
    ax.text(.005,1.57,tr("红点：离0.1最近的格点；这不是实际float格式。","Red: nearest grid point to 0.1; this is not the actual float format."),fontsize=12)
    ax=fig.add_subplot(gs[1,0]); ax.axis("off")
    ax.set_title(tr("b  实际Python浮点加法", "b  Actual Python floating-point addition"),loc="left")
    ax.text(.02,.75,"0.1 + 0.2",fontsize=21,transform=ax.transAxes)
    ax.text(.02,.48,repr(float_sum),fontsize=21,color=blue,transform=ax.transAxes)
    ax.text(.02,.18,tr("显示位数改变文字，不改变已存储的值。","Formatting changes the text, not the stored value."),fontsize=12,transform=ax.transAxes)
    ax=fig.add_subplot(gs[1,1]);ax.axis("off")
    ax.set_title(tr("c  精确记录小数或有理数", "c  Exact decimal input or a rational value"),loc="left")
    ax.text(.02,.76,'Decimal("0.1") + Decimal("0.2")',fontsize=14,transform=ax.transAxes)
    ax.text(.02,.56,str(decimal_sum),fontsize=23,color=red,transform=ax.transAxes)
    ax.text(.02,.30,'Fraction(1, 10) + Fraction(2, 10)',fontsize=14,transform=ax.transAxes)
    ax.text(.02,.10,str(rational_sum),fontsize=23,color=green,transform=ax.transAxes)
    save(fig,"finite-number-lines")

    fig=plt.figure(figsize=(12,6.3),layout="constrained");ax=fig.add_subplot();ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,6.3)
    ax.text(.1,5.9,tr("长度标准怎样变得可以重现？", "How can a length standard become reproducible?"),fontsize=19,weight="bold")
    ax.text(.1,5.35,tr("原创方法示意：原器比较 → 光学计数 → 由光速与时间定义", "Original method schematic: artifact comparison → optical counting → light and time"),fontsize=12)
    ax.add_patch(Rectangle((.3,3.6),3.1,.35,facecolor="#bfc6c5",edgecolor=ink))
    for x in [.55,3.15]:ax.plot([x,x],[3.5,4.08],color=ink,lw=2)
    ax.annotate('',(.55,4.35),(3.15,4.35),arrowprops={"arrowstyle":"<->","color":ink})
    ax.text(1.85,4.55,tr("刻线间的距离","Distance between marks"),ha="center",fontsize=13)
    ax.text(.3,2.9,tr("铂铱原器（1889）", "Platinum–iridium (1889)"),fontsize=13,weight="bold")
    ax.text(.3,2.35,tr("与共同保存的实物比较", "Compare against a\nshared physical reference"),fontsize=13)
    xs=[4.4+i*.006 for i in range(451)];ys=[3.8+.27*math.sin((x-4.4)*2*math.pi/.45) for x in xs]
    ax.plot(xs,ys,color=blue,lw=2);ax.hlines(3.8,4.4,7.1,color="#bac4c6",lw=.7)
    ax.annotate('',(4.4,4.4),(4.85,4.4),arrowprops={"arrowstyle":"<->","color":ink});ax.text(4.625,4.58,tr("波长","Wavelength"),ha="center",fontsize=12)
    ax.text(4.4,2.9,tr("氪86辐射（1960）", "Krypton-86 radiation (1960)"),fontsize=13,weight="bold")
    ax.text(4.4,2.35,tr("通过光学干涉连接长度与波长", "Relate length to wavelength\nusing optical interference"),fontsize=12)
    ax.add_patch(FancyArrowPatch((8.4,3.8),(11.5,3.8),arrowstyle='->',mutation_scale=22,color=red,lw=2))
    ax.plot([8.5,8.5],[3.4,4.2],color=ink);ax.plot([11.35,11.35],[3.4,4.2],color=ink)
    ax.text(9.9,4.4,"c × Δt",ha="center",fontsize=21,color=red)
    ax.text(8.4,2.9,tr("真空中的光与时间（1983）", "Light in vacuum and time (1983)"),fontsize=12,weight="bold")
    ax.text(8.4,2.35,tr("固定光速，使用秒定义长度", "Fix light speed; use the\nsecond to define length"),fontsize=13)
    ax.text(.3,1.25,tr("今天的米：光在真空中经过1/299792458秒所走的距离。", "Today’s metre: the distance light travels in vacuum in 1/299792458 second."),fontsize=14)
    ax.text(.3,.55,tr("共同单位定义与实际测量精度，是两个相连但不同的问题。", "A shared unit definition and practical measurement precision are distinct, connected questions."),fontsize=13)
    save(fig,"length-history")
    summary={"model":"Nominal stress from initial rectangular section; defined teaching inputs","force_N":force_N,"width_mm":width_mm,"thickness_mm":thickness_mm,"area_mm2":area_mm2,"area_m2":area_m2,"stress_MPa":stress_MPa,"float_sum_repr":repr(float_sum),"decimal_sum":str(decimal_sum),"rational_sum":str(rational_sum),"decimal_third_12_digits":decimal_third,"direct_cancellation":cancellation,"fsum_result":stable_sum,"float_spacing_at_one":math.ulp(1.0),"near_zero_relative_only":math.isclose(0,1e-9,rel_tol=1e-6),"near_zero_absolute":math.isclose(0,1e-9,abs_tol=2e-9),"stress_at_thickness_mm":{str(t):force_N/(width_mm*t) for t in [.08,.1,.12]}}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')


if __name__=="__main__": main()
```

The numerical summary should contain an area of 0.20 mm², an area of 2×10⁻⁷ m², and a stress of 25 MPa. The floating-point addition is recorded as `0.30000000000000004`, decimal addition as `0.3`, and the rational result as `3/10`. The latter representations are stored as strings in JSON to retain their explicit form. Converting them to ordinary floating-point values before saving would reintroduce that representation. Matching the two unit routes against the numerical summary provides a direct check that the calculation and presentation follow the same data.

### Run and save results

Outputs include summary.json and scientific figures in SVG and PNG formats.

```
python main.py --output output --language en
python main.py --output output-zh --language zh
```

The thickness plot shows a much larger change than a floating-point tail. Holding force at 5 N and width at 2 mm, changing thickness from 0.10 mm to 0.08 mm increases stress from 25 MPa to 31.25 MPa. Changing it to 0.12 mm reduces stress to approximately 20.83 MPa. A 20% thickness decrease produces a 25% stress increase, while a 20% thickness increase produces a reduction of about 16.67%. The effects are asymmetric because thickness appears in the denominator. This input sensitivity has a very different scale and interpretation from the binary approximation used to store 0.1.

$$
t=t_0(1+\varepsilon),\qquad\frac{\sigma}{\sigma_0}=\frac{1}{1+\varepsilon},\qquad\frac{\sigma-\sigma_0}{\sigma_0}=\frac{1}{1+\varepsilon}-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Changed positive thickness, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a15f4e949d9181049b209fc5.svg) | Reference thickness, 0.10 mm here |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Relative thickness change (t−t₀)/t₀, dimensionless and greater than −1 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Nominal stress after the thickness change, MPa |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Nominal stress at the same force and width with reference thickness, MPa |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | Dimensionless unit ratio |

At fixed force and width, stress is inversely proportional to thickness. For ε=−0.20 the stress ratio is 1/0.8=1.25, a 25% increase; for ε=+0.20 it is 1/1.2≈0.8333, a 16.67% reduction.

These distinctions suggest a useful checking order. Establish the object and formula definition, then examine units and magnitude, then examine how measured inputs affect the answer, and finally inspect numerical representation and algorithms. Each step points to a specific action. An area conversion wrong by a million calls for correcting units; thickness varying across sampling locations calls for understanding measurement and geometry; subtraction that loses a small contribution calls for a better computational arrangement. Treating every discrepancy as a generic precision problem makes those actions harder to identify.

## Link geometry, units, sensitivity, and the comparison rule

The experiment below lets you change force, initial width, and thickness, and display length in either millimetres or metres. Linked views track the cross-section and the stress-versus-thickness relationship, while the calculation panel shows both unit routes. First switch display units: the physical specimen and final MPa result should stay unchanged. Next increase thickness: the area grows and the selected point moves down the stress curve. To make a thin section visible, the geometry view uses separately identified drawing scales for the two directions; dimension labels provide the actual sizes. The drawing locates dimensions, while the values and axes support quantitative comparison.

### One section, two unit routes

Dimension inputs are recorded in millimetres; unit selection changes the graphical display. The reference uses current force and width with 0.10 mm thickness.

[Figure: Rectangular section and dimensions](https://ml-biomat.com/tutorials/python-scientific/p02/en/#P02-geometry)

[Figure: Analytical thickness-stress curve](https://ml-biomat.com/tutorials/python-scientific/p02/en/#P02-curve)

Moving thickness above or below the reference shows both nominal stress and its relative change. The comparison retains a reference thickness of 0.10 mm while using the current force and width, so both points address the thickness question under the same loading conditions. Change the relative and absolute tolerances to see whether the rule classifies the current and reference stresses as close. The plotted points and numerical difference remain visible regardless of that classification, preserving the magnitude of the change instead of replacing it with a pass/fail label.

Check one fresh combination independently: a force of 8 N, width of 4 mm, and thickness of 0.20 mm give an area of 0.80 mm² and a stress of 10 MPa. Converting millimetres to metres should produce the same result. If both dimensions double while force stays fixed, the area becomes four times larger and stress falls to one quarter. Explaining these checks connects units, dimensional multiplication, and proportional reasoning. The next chapter organizes well-defined quantities like these into lists and dictionaries for multiple experimental specimens.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Python — Floating-point arithmetic](https://docs.python.org/3.14/tutorial/floatingpoint.html)

   Representation, binary fractions, and display.

   PSF documentation license
2. [Python — Decimal](https://docs.python.org/3.14/library/decimal.html)

   Input construction and arithmetic context.

   PSF documentation license
3. [Python — Fractions](https://docs.python.org/3.14/library/fractions.html)

   Rational numerators/denominators and conversion from floats.

   PSF documentation license
4. [Python — math](https://docs.python.org/3.14/library/math.html)

   Definitions of fsum, ulp, and isclose.

   PSF documentation license
5. [PEP 485 — Approximate equality](https://peps.python.org/pep-0485/)

   Design of approximate equality and comparisons near zero.

   Public-domain dedication in PEP
6. [BIPM — History of the metre](https://www.bipm.org/en/history-si/metre)

   Historical development from a prototype to optical definitions.
7. [BIPM — SI unit metre](https://www.bipm.org/en/si-base-units/metre)

   Exact relationship between vacuum light speed and the metre.
