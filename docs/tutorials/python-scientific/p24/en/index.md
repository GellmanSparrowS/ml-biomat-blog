# Connecting Symbolic Mathematics to Numerical Computation

Source: https://ml-biomat.com/tutorials/python-scientific/p24/en/
Language: en

Derive force and stiffness from elastic energy with SymPy, then use exact algebra to understand numerical error.

## Begin with an elastic element in your hand

Opening a clip, compressing a spring, or stretching a flexible connector gives a familiar sensation: resistance changes as the object moves. Suppose an expression describes the energy stored in that element. Can it also tell us the force required to hold a displacement, and how much extra force a small additional movement will require? These are questions about energy, force, and stiffness. They provide a connected way to learn symbolic computation: derive relationships while retaining letters, then supply parameters and displacement values to obtain corresponding curves.

We will use a deliberately simple elastic energy model throughout. Loading is slow, work supplied by the applied force is stored in the element, and unloading follows the same relation in reverse. This describes reversible elastic response. A measured loop, a dependence on loading speed, or permanent deformation calls for additional variables describing dissipation or internal state. Understanding this small model makes the connection between a physical assumption and a formula's purpose concrete.

SymPy stores and transforms the expressions, NumPy evaluates arrays of displacement values, and Matplotlib displays the physical quantities. We will also estimate force by subtracting two nearby energy values and dividing by their separation. Comparing that estimate with a symbolic derivative reveals why making a numerical step extremely small can eventually make a calculation worse.

## Put energy, displacement, and units together

Think of stored energy as mechanical work gradually deposited in an element. A larger displacement generally stores more, while each equal increment of displacement can require a different amount of work. A quadratic term describes a simple elastic energy. Adding a quartic term allows resistance to rise more rapidly at larger displacements. Two coefficients control their contributions. These are chosen inputs to a teaching model; the plotted values are evaluations of that model.

$$
U(x)=\frac{kx^2}{2}+\frac{\alpha x^4}{4},\qquad k>0,\quad \alpha\geq0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9469b6261e047457191334c2.svg) | Elastic energy at displacement x, mJ; U(0) = 0. |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Displacement from the undeformed position, mm; its sign indicates direction. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Quadratic energy coefficient and tangent stiffness at the origin, N/mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Quartic energy coefficient, N/mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/96d66c13fb959b10fd625f8f.svg) | Dimensionless denominator constants; superscripts 2 and 4 denote second and fourth powers. |

For k = 2 N/mm, α = 0.5 N/mm³, and x = 1 mm, U = 2 × 1² / 2 + 0.5 × 1⁴ / 4 = 1.125 N·mm = 1.125 mJ. Both terms have energy units. Setting α to zero retains quadratic energy; positive α adds a contribution that grows faster at larger displacement.

Powers apply to units as well as numerical values. Squared displacement has units of square millimeters. Multiplying by newtons per millimeter produces newton millimeters. The quartic coefficient needs units of newtons per cubic millimeter so that its contribution has the same energy units. Checking that addition combines like quantities can reveal an incorrect exponent or coefficient. Throughout this example, displacement is entered in millimeters and energy is reported in millijoules: one newton millimeter equals one millijoule.

With a quadratic coefficient of 2 N/mm and a quartic coefficient of 0.5 N/mm³, a displacement of 1 mm stores 1 mJ in the quadratic contribution and 0.125 mJ in the quartic contribution. At 2 mm, these become 4 mJ and 2 mJ, giving 6 mJ altogether. Doubling displacement multiplies the quadratic contribution by four and the quartic contribution by sixteen. These numbers already explain why the higher power becomes more prominent farther from the origin.

The energy at zero displacement is chosen as zero. Adding the same constant everywhere changes this reference but leaves energy differences and forces unchanged. Changing displacement units is different: converting from millimeters to meters requires converting both coefficients as well. Relabeling the horizontal axis alone would change the physical interpretation of every calculated point.

Symmetry can be checked before inserting numbers. Both energy terms contain even powers, so equal displacements in opposite directions store equal energy. Holding forces consequently have equal magnitudes and opposite signs, while tangent stiffness is the same on both sides. This is a concrete assumption encoded by the formula. An element with different tensile and compressive responses requires an energy model that captures that distinction.

## Why the slope of energy gives force

Consider a short loading interval over which the applied force is nearly constant. Work is force multiplied by displacement increment. Dividing the increase in energy by that increment therefore gives the average force over the interval. On an energy graph, this ratio is the slope of a line joining two points. As the points approach one another, the average approaches the force at a particular position and the line approaches a tangent. A derivative describes this local rate of change.

$$
F(x)=\frac{\mathrm dU}{\mathrm dx}=kx+\alpha x^3,\qquad K(x)=\frac{\mathrm dF}{\mathrm dx}=k+3\alpha x^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f42ff2aa801298d0b0e10a.svg) | Applied force holding a displacement during slow loading, N; the restoring force is −F. |
| ![Formula](https://ml-biomat.com/static/agent-math/c18cc14db4443d05e8ca8d27.svg) | Tangent stiffness at the current position, N/mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/d2936881a9db32d00d3ef560.svg) | U is stored energy, mJ; x is displacement, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/c716d1023aa9003462dc1854.svg) | k is the quadratic coefficient, N/mm; α the quartic coefficient, N/mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/d7307287aa169cbb98be8758.svg) | Derivative with respect to displacement: local change per unit displacement. |
| ![Formula](https://ml-biomat.com/static/agent-math/6cb44f25e489afb06ec62d2e.svg) | Dimensionless coefficient obtained by differentiating x³ to give 3x². |

For a power, bring the exponent forward and reduce it by one: x² becomes 2x and x⁴ becomes 4x³, canceling the energy denominators. With k = 2, α = 0.5, and x = 1 in the defined units, F = 2 + 0.5 = 2.5 N and K = 2 + 3 × 0.5 = 3.5 N/mm. The first derivative connects energy slope to force, and the next connects force slope to stiffness.

Positive force here means the external force needed to hold a positive displacement. The element's restoring force points in the opposite direction, toward lower energy, and has the opposite sign. Identifying which object exerts the force resolves the apparent sign difference between familiar energy formulas. Differentiating once more gives tangent stiffness: the local rate at which required force rises with displacement.

At 1 mm, holding force is 2.5 N and tangent stiffness is 3.5 N/mm. An additional displacement of 0.01 mm therefore increases force by approximately 0.035 N. The complete expression gives 0.0351505 N, differing by about 0.0001505 N. The local slope is useful for small increments. Over a longer interval, stiffness changes along the path, so evaluate the full force at both endpoints and subtract.

![Energy, applied force, and tangent stiffness from one model. Colors compare α = 0, 0.5, and 2 N/mm³, with k = 2 N/mm throughout. Blue markers track three corresponding values at x = 1 mm. Curves are model evaluations.](https://ml-biomat.com/static/tutorials/python-scientific/figures/22fa82ae00c17ce447225822.svg?v=22fa82ae00c1)

Figure 1Energy, applied force, and tangent stiffness from one model. Colors compare α = 0, 0.5, and 2 N/mm³, with k = 2 N/mm throughout. Blue markers track three corresponding values at x = 1 mm. Curves are model evaluations.

The three panels use identical parameters to show energy, applied force, and stiffness. With the quartic term set to zero, the gray force curve is linear and stiffness is constant. The blue and orange models retain the quartic term, so stiffness increases with displacement. A high energy value and a steep energy slope have different meanings and units. Reading the axis labels and the derivative linking each pair of panels keeps those meanings distinct.

## Keep the letters meaningful and the fractions exact

The statement `x = sp.Symbol('x', real=True)` creates a symbol representing a real number; it does not yet choose a displacement. The coefficient `k` is positive and `alpha` is nonnegative. Including zero lets us compare models with and without the quartic contribution. These assumptions guide algebraic operations. For example, the square root of a squared real displacement is its absolute value. At −2 mm the result is 2 mm, which explains why retaining the absolute value matters.

The program constructs coefficients with `sp.Rational(1, 2)` and `sp.Rational(1, 4)`. Both fractions happen to have exact binary floating-point representations, but rational objects keep the derivation in exact arithmetic. The benefit becomes especially visible with one third. Ordinary division between Python integers is evaluated before its result enters a symbolic expression. A Rational object instead retains a numerator and denominator. Conversion to a decimal can wait until a numerical result is needed.

Substituting values returns a new expression while preserving the general one. This resembles keeping both an unfilled calculation sheet and a version containing one element's parameters. Supplying the two coefficients leaves displacement as a free symbol; supplying displacement as well produces a definite energy. Inspecting `free_symbols` helps locate a parameter that has not yet been assigned. The separation also makes it easy to evaluate the same general model for several parameter sets.

These symbolic objects carry algebraic relationships, while this example manages units through explicit definitions and consistent numerical conventions. Naming a symbol displacement does not automatically attach millimeters to it. When extending the model, list the input and output units, then check each added term and derivative. A successful program execution then corresponds to an understandable physical calculation.

## How a formula becomes something a computer can transform

A picture of a formula can be displayed, but taking its derivative requires an operational representation. In their 2017 paper describing SymPy, Meurer and colleagues explained expression trees: operations form nodes, symbols and constants form leaves, and algebraic transformations consume and construct these structures. Implementing the system as a Python library connects symbolic work to the surrounding scientific ecosystem. The authors' openly available paper sources explain the architecture behind this connection.

![Original model illustration: thirteen nodes read recursively from the actual SymPy expression show how sums, products, powers, and rational numbers form energy. The expression and its derivative appear below. The 2017 paper discusses this architecture; the spring model is constructed for this chapter.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ce6234471836d23e588a0d28.svg?v=ce6234471836)

Figure 2Original model illustration: thirteen nodes read recursively from the actual SymPy expression show how sums, products, powers, and rational numbers form energy. The expression and its derivative appear below. The 2017 paper discusses this architecture; the spring model is constructed for this chapter.

The top Add node combines two terms. Each Mul branch multiplies a rational coefficient, a parameter, and a displacement power. A Pow node connects the displacement to its exponent. The illustration is generated from the actual energy expression, so each branch corresponds to its `func` and `args` structure. Symbols and fractions have no further children in this algebraic representation. Following a branch from top to bottom provides a practical reading of how the formula is stored.

This also explains a distinction between mathematical equality and matching structure. A polynomial written as a product can have a different tree from its expanded sum. Python assignment gives an object a name; `sp.Eq` constructs an equation; `==` compares the structure of SymPy expressions. To check the polynomial identities used here, expand or simplify the difference and see whether it becomes zero. Substituting several numerical values is also useful for finding mistakes in a proposed identity.

For the spring, the same stored expression produces both force and stiffness, and integrating force reconstructs energy. Changing the energy model therefore regenerates related quantities from a common mathematical definition. This organization helps keep coefficients and powers consistent across calculations. The tree illustration exposes the representation that makes those operations possible.

## Turn a derived expression into a numerical curve

Letters are useful during a derivation, while plotting needs numerical values. The call `lambdify((x, k, alpha), U, modules='numpy')` constructs a callable numerical function. The ordered tuple specifies the argument order. Passing a displacement array and the two coefficients returns the corresponding energy values. Force and stiffness are converted in the same way. This is a deliberate transition from a completed symbolic expression to array-based evaluation.

The displacement array contains 401 equally spaced positions from 0 to 2 mm, separated by 0.005 mm. The exported model table keeps displacement, energy, force, and stiffness in the same row. At 1 mm, a reader can inspect 1.125 mJ, 2.5 N, and 3.5 N/mm together. Increasing the number of plotted points gives a finer display of the same model; it does not add a new physical parameter or create extra measurements.

The model can also answer an inverse question: which displacement requires a force of 3 N? The program subtracts 3 from the force expression and passes the result to `nsolve`, starting at 1 mm. The solution is approximately 1.134728 mm. Substituting it back checks the force balance. Because tangent stiffness is positive throughout this model, force increases strictly with displacement, giving one real equilibrium displacement for each prescribed force. That uniqueness follows from the model's slope.

$$
W_{0\to b}=\int_0^b F(s)\,\mathrm ds=U(b)-U(0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa1aa9ce37fea73c98f0d1b.svg) | Work supplied while slowly loading from displacement 0 to b, mJ. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Final loading displacement, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Integration variable for displacement, mm; it varies from 0 to b. |
| ![Formula](https://ml-biomat.com/static/agent-math/553badbaf2c0b915d0d4369a.svg) | Applied force at displacement s, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/eafdac3dd6a477b3670861c5.svg) | The integral accumulates work over small displacement increments; ds has units of mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/fdd3a5a8d8d6ca2f49a8ba46.svg) | Stored energies at the final and initial positions, mJ. |

For b = 2 mm, k = 2 N/mm, and α = 0.5 N/mm³, integration gives k b² / 2 + α b⁴ / 4 = 4 + 2 = 6 mJ. Initial energy is zero, so work equals final stored energy. The symbol s distinguishes the varying integration coordinate from the fixed endpoint b.

Integration adds the work of all the small loading increments. Loading from 0 to 2 mm stores 6 mJ, equal to the final energy minus the initial energy. Multiplying the final force of 8 N by the entire displacement would give 16 mJ. That calculation assumes 8 N was applied throughout, although the force actually rose from zero. The relevant work is the area under the complete force curve, giving a direct mechanical interpretation of the symbolic integral.

An initial guess and a model parameter play different roles. The guess specifies where a numerical search begins; changing it should still lead to the unique equilibrium in this example when the search converges. Changing a stiffness coefficient changes the element and shifts equilibrium. More complicated energy functions can have multiple equilibria. Their interpretation then involves the allowed domain and the behavior of energy near each solution. Reading the force curve before interpreting the returned position connects the solver to the physical picture.

## Why the smallest difference step is not always the best

A function that returns energy values is enough to estimate force numerically. Evaluate the function on both sides of the target position and divide the energy difference by their separation. This centered difference uses information symmetrically. With half-spacing h, the full separation is 2h; omitting that factor of two doubles the estimated force. For the quartic energy used here, SymPy can expand the complete difference between this estimate and the derivative.

$$
D_hU(x)=\frac{U(x+h)-U(x-h)}{2h},\qquad D_hU(x)-F(x)=\alpha xh^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/732aa542b12ff5c3ed36159d.svg) | Centered-difference estimate of force with half-spacing h, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/a83c7a267ed0d7a6190ac2db.svg) | Stored energies on either side of the center, mJ. |
| ![Formula](https://ml-biomat.com/static/agent-math/8c42b0b36a7b3ec0bebfa150.svg) | x is central displacement and h a positive half-spacing, both mm; the points are 2h apart. |
| ![Formula](https://ml-biomat.com/static/agent-math/d7f42ff2aa801298d0b0e10a.svg) | Applied force obtained from the symbolic derivative, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Quartic energy coefficient, N/mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/f5f3224583db57b9cfe323c8.svg) | The denominator factor 2 converts half-spacing to full spacing; superscript 2 denotes squaring. |

Substitute x+h and x−h into energy and expand. Subtraction cancels terms with even powers of h; division by 2h leaves kx + αx³ + αxh². The first two terms are F, leaving the exact-arithmetic truncation error. For α = 0.5 N/mm³, x = 1 mm, and h = 0.1 mm, it is 0.005 N and the difference estimate is 2.505 N. Floating-point evaluation adds rounding effects.

At 1 mm with a half-spacing of 0.1 mm, the exact-arithmetic estimate is 2.505 N, exceeding the derivative by 0.005 N. Halving the spacing to 0.05 mm reduces this error to 0.00125 N, a factor of four. The squared step in the error expression explains the phrase second-order accuracy with a directly calculable example. When the quartic coefficient is zero, the centered difference of the quadratic energy gives the exact derivative in exact arithmetic.

![At left, compare the tangent at x = 1 mm with a secant using half-spacing 0.2 mm. At right, evaluate 170 steps for the same model. Orange is the exact-arithmetic error αxh²; blue is absolute error from actual NumPy evaluation. Horizontal axes represent position and step size, respectively.](https://ml-biomat.com/static/tutorials/python-scientific/figures/2c2e3527960f342948be0a26.svg?v=2c2e3527960f)

Figure 3At left, compare the tangent at x = 1 mm with a secant using half-spacing 0.2 mm. At right, evaluate 170 steps for the same model. Orange is the exact-arithmetic error αxh²; blue is absolute error from actual NumPy evaluation. Horizontal axes represent position and step size, respectively.

Floating-point arithmetic adds a competing effect. Very close positions have very close energy values. Subtraction leaves a small difference, so rounding errors in the original values can become a substantial fraction of that difference. Dividing by a still smaller separation magnifies the effect. The error plot initially follows the predicted square-law decrease, then fluctuates and rises as the step becomes extremely small. Details depend on operation order and floating-point implementation; the competition between the two error mechanisms is the useful pattern.

A symbolic derivative supplies a clear reference in this example. The difference calculation shows what happens when only evaluations of the energy function are used. Studying both on a tractable problem provides a method for examining more complicated functions. When a derivative can be generated from the model, use that mathematical structure. When differences are needed, compare several step sizes and look for a stable region.

The vertical error axis uses newtons and reports the absolute difference from the derivative. Scaling up the forces can also scale up absolute error. Comparisons across models may therefore benefit from normalization by a clearly defined reference force. Dividing by the local force becomes problematic near zero force, so selecting a reference scale is part of defining the numerical question. Absolute error here connects directly to the worked value of 0.005 N.

## A complete program from derivation to figures

The program creates symbols with assumptions, constructs energy using exact fractions, and derives force, stiffness, and the centered-difference error. It then substitutes a common parameter set, records key values in a numerical summary, and generates model and error tables. The three figures show connected physical quantities, the actual expression tree, and competing numerical errors. Every plotted model value, tree node, and error point comes from the calculation.

### Complete example: from energy expression to numerical error

Generate model and error CSV tables, a numerical summary, and three figures. SymPy performs derivation and solving; NumPy evaluates arrays.

```
"""Derive a spring model symbolically, then evaluate it with NumPy."""
from pathlib import Path
import argparse
import json
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def expression_tree(ax, expression):
    """Draw the actual func/args structure; each leaf receives one position."""
    nodes, edges = [], []
    next_leaf = [0]

    def visit(expr, depth=0):
        index = len(nodes)
        nodes.append(None)
        children = [visit(child, depth + 1) for child in expr.args]
        if children:
            horizontal = np.mean([nodes[child][0] for child in children])
        else:
            horizontal = next_leaf[0]
            next_leaf[0] += 1
        label = expr.func.__name__ if children else str(expr)
        nodes[index] = (horizontal, -depth, label, bool(children))
        edges.extend((index, child) for child in children)
        return index

    visit(expression)
    for parent, child in edges:
        a, b = nodes[parent], nodes[child]
        ax.plot([a[0], b[0]], [a[1], b[1]], color='#b7c6cd', lw=1.7, zorder=0)
    for x, y, label, branch in nodes:
        ax.text(x, y, label, ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round,pad=.48', facecolor='#eaf2f5' if branch else '#fbf1e9',
                          edgecolor='#28658c' if branch else '#b36837', lw=1.3))
    ax.set(xlim=(-.65, next_leaf[0] - .35), ylim=(-3.65, .65))
    ax.axis('off')
    return len(nodes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ['Noto Sans CJK SC', 'Noto Sans SC',
        'Microsoft YaHei', 'SimHei', 'DejaVu Sans'] if f in available],
        'font.size': 12, 'svg.fonttype': 'none', 'axes.spines.top': False,
        'axes.spines.right': False, 'grid.alpha': .16})

    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=160)
        plt.close(fig)

    # Numerical values use mm, N, and N*mm (= mJ) consistently.
    x = sp.Symbol('x', real=True)
    k = sp.Symbol('k', positive=True)
    alpha = sp.Symbol('alpha', nonnegative=True)
    h = sp.Symbol('h', positive=True)
    U = sp.Rational(1, 2) * k * x**2 + sp.Rational(1, 4) * alpha * x**4
    F = sp.diff(U, x)
    K = sp.diff(F, x)
    reconstructed = sp.integrate(F, x)
    assert sp.simplify(reconstructed - U) == 0
    centered = (U.subs(x, x + h) - U.subs(x, x - h)) / (2 * h)
    truncation = sp.expand(centered - F)
    assert sp.simplify(truncation - alpha * x * h**2) == 0
    values = {k: sp.Integer(2), alpha: sp.Rational(1, 2)}
    exact_one = [expr.subs(values).subs(x, 1) for expr in (U, F, K)]
    work = sp.integrate(F.subs(values), (x, 0, 2))
    equilibrium = sp.nsolve(F.subs(values) - 3, x, 1, prec=40)
    equilibrium_residual = abs((F.subs(values) - 3).subs(x, equilibrium))
    u_num = sp.lambdify((x, k, alpha), U, modules='numpy')
    f_num = sp.lambdify((x, k, alpha), F, modules='numpy')
    stiffness_num = sp.lambdify((x, k, alpha), K, modules='numpy')
    grid = np.linspace(0, 2, 401)
    energy = u_num(grid, 2., .5)
    force = f_num(grid, 2., .5)
    stiffness = stiffness_num(grid, 2., .5)
    np.savetxt(args.output / 'model.csv', np.column_stack([grid, energy, force, stiffness]),
               delimiter=',', header='displacement_mm,energy_mJ,force_N,stiffness_N_per_mm', comments='')

    fig, axes = plt.subplots(1, 3, figsize=(13.4, 5.2), layout='constrained')
    for a, color in zip([0., .5, 2.], ['#82939b', '#28658c', '#c26835']):
        for ax, fn in zip(axes, [u_num, f_num, stiffness_num]):
            output = np.broadcast_to(fn(grid, 2., a), grid.shape)
            ax.plot(grid, output, color=color, lw=2.3, label=f'α = {a:g} N/mm³')
    for ax, value, title, ylabel in zip(axes, [1.125, 2.5, 3.5],
        [tr('A  储存了多少能量', 'A  Stored energy'), tr('B  维持位移的外力', 'B  Holding force'),
         tr('C  当前有多难再拉长', 'C  Tangent stiffness')],
        [tr('储能 U / mJ', 'Energy U / mJ'), tr('外力 F / N', 'Applied force F / N'),
         tr('切线刚度 K / (N/mm)', 'Tangent stiffness K / (N/mm)')]):
        ax.scatter([1], [value], s=58, color='#28658c', edgecolor='white', zorder=5)
        ax.annotate(f'{value:g}', (1, value), xytext=(6, 10), textcoords='offset points', color='#28658c',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=.85, pad=.5))
        ax.set(title=title, xlabel=tr('位移 x / mm', 'Displacement x / mm'), ylabel=ylabel, xlim=(0, 2))
        ax.set_xticks([0, .5, 1, 1.5, 2]); ax.grid(True)
    axes[0].legend(loc='upper left', fontsize=11)
    fig.suptitle(tr('同一个储能函数的三个读法；k = 2 N/mm',
                       'Three readings of one energy function; k = 2 N/mm'), fontsize=16)
    save(fig, 'mechanics')

    fig = plt.figure(figsize=(12, 6.8), layout='constrained')
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])
    ax = fig.add_subplot(gs[0]); node_count = expression_tree(ax, U)
    ax.set_title(tr('SymPy的2017年论文：表达式树架构',
                       'Expression-tree architecture in the 2017 SymPy paper'), fontsize=16, pad=14)
    ax = fig.add_subplot(gs[1]); ax.axis('off')
    ax.text(.02, .73, '$U=' + sp.latex(U) + '$', fontsize=19, transform=ax.transAxes)
    ax.text(.55, .73, '$F=' + sp.latex(F) + '$', fontsize=19, transform=ax.transAxes)
    ax.text(.02, .05, tr('Add：相加     Mul：相乘     Pow：乘方；叶子保留符号和精确分数。',
        'Add: sum     Mul: product     Pow: power; leaves retain symbols and exact fractions.'),
        fontsize=12, transform=ax.transAxes)
    save(fig, 'history')

    steps = np.logspace(-14, -1, 170)
    differences = (u_num(1 + steps, 2., .5) - u_num(1 - steps, 2., .5)) / (2 * steps)
    errors = abs(differences - 2.5)
    exact_error = .5 * steps**2
    np.savetxt(args.output / 'difference-error.csv', np.column_stack([steps, differences, errors, exact_error]),
        delimiter=',', header='step_mm,centered_force_N,absolute_error_N,exact_arithmetic_error_N', comments='')
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6), layout='constrained', gridspec_kw={'width_ratios': [1, 1.22]})
    local = np.linspace(.65, 1.35, 200); hh = .2
    secant = float((u_num(1 + hh, 2., .5) - u_num(1 - hh, 2., .5)) / (2 * hh))
    intercept = float((u_num(1 + hh, 2., .5) + u_num(1 - hh, 2., .5)) / 2)
    axes[0].plot(local, u_num(local, 2., .5), color='#28658c', lw=2.5, label=tr('能量曲线', 'Energy'))
    axes[0].plot(local, 1.125 + 2.5 * (local - 1), color='#2b8a74', ls='--', label=tr('中心切线', 'Center tangent'))
    axes[0].plot(local, intercept + secant * (local - 1), color='#c26835', ls=':', lw=2.4, label=tr('两点割线', 'Two-point secant'))
    axes[0].scatter([.8, 1.2], u_num(np.array([.8, 1.2]), 2., .5), color='#c26835', zorder=5)
    axes[0].set(title=tr('A  先看斜率的几何意义', 'A  Read slope geometrically'),
        xlabel=tr('位移 / mm', 'Displacement / mm'), ylabel=tr('储能 / mJ', 'Stored energy / mJ'))
    axes[0].legend(loc='upper left', fontsize=11); axes[0].grid(True)
    positive = errors > 0
    axes[1].loglog(steps[positive], errors[positive], color='#28658c', lw=1.2, marker='.', ms=3,
                  label=tr('NumPy浮点计算', 'NumPy floating-point calculation'))
    axes[1].loglog(steps, exact_error, color='#c26835', lw=2.2, ls='--',
                  label=tr('精确算术：αxh²', 'Exact arithmetic: αxh²'))
    axes[1].set(title=tr('B  步长与力的绝对误差', 'B  Step size and absolute force error'),
        xlabel=tr('半间距 h / mm', 'Half-spacing h / mm'), ylabel=tr('绝对误差 / N', 'Absolute error / N'),
        ylim=(1e-17, .1))
    axes[1].legend(loc='upper center', fontsize=11); axes[1].grid(True, which='major')
    fig.suptitle(tr('x = 1 mm，k = 2 N/mm，α = 0.5 N/mm³；左图 h = 0.2 mm',
                       'x = 1 mm, k = 2 N/mm, α = 0.5 N/mm³; left panel h = 0.2 mm'), fontsize=14)
    save(fig, 'difference')
    summary = {'sympy_version': sp.__version__, 'energy_expression': str(U), 'force_expression': str(F),
        'stiffness_expression': str(K), 'truncation_expression': str(truncation),
        'energy_at_1_mJ': float(exact_one[0]), 'force_at_1_N': float(exact_one[1]),
        'stiffness_at_1_N_per_mm': float(exact_one[2]), 'work_0_to_2_mJ': float(work),
        'equilibrium_3N_mm': float(equilibrium), 'equilibrium_residual_N': float(equilibrium_residual),
        'centered_h01_N': float(centered.subs(values).subs({x: 1, h: sp.Rational(1, 10)})),
        'exact_h01_error_N': .005, 'expression_tree_nodes': node_count,
        'sqrt_real_x_squared': str(sp.sqrt(x**2)), 'zero_float_errors': int((errors == 0).sum()),
        'minimum_positive_float_error_N': float(errors[positive].min()),
        'maximum_float_error_N': float(errors.max())}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

Start inspecting the output with the three results at 1 mm, followed by the work from 0 to 2 mm. The field `equilibrium_3N_mm` records the inverse solution and `truncation_expression` records the exact difference identity. The error table retains each step, estimated force, absolute numerical error, and exact-arithmetic error, allowing a plotted point to be traced to its values. A logarithmic vertical axis accepts positive values; any exactly zero numerical errors are counted and omitted from that curve. The count was zero in the displayed run.

For a first modification, set the quartic coefficient to zero and check that force becomes linear and stiffness constant. Restore it, then consider adding a new energy contribution and examine how its derivative and units change. Altering one component at a time makes the relationship between formulas and figures easy to follow. Choosing an energy term for a particular material requires matching the physical response that the model is meant to describe.

## Explore energy, force, and calculation error together

Keep the default position of 1 mm and quartic coefficient of 0.5 N/mm³, and locate the energy of 1.125 mJ and force of 2.5 N. The upper panel shows the energy curve, the tangent at the current position, and the two evaluation points. The lower-left panel follows force at that position. The lower-right panel displays errors across step sizes and highlights the selected step. All views update together, separating a change in the physical model from a change in numerical resolution.

### Read local slope and numerical error from energy

[Figure: Energy curve, tangent, and evaluation points](https://ml-biomat.com/tutorials/python-scientific/p24/en/#P24-energy-view)

[Figure: Force at the same position](https://ml-biomat.com/tutorials/python-scientific/p24/en/#P24-force-view)

[Figure: Exact-arithmetic and floating-point difference errors](https://ml-biomat.com/tutorials/python-scientific/p24/en/#P24-error-view)

k = 2 N/mm throughout. Blue denotes the model or actual difference error, green dashed line the energy tangent, and orange the evaluation points or exact-arithmetic error. The logarithmic error panel plots positive errors; zero values remain in the readout.

Set the quartic coefficient to zero. Energy remains curved, while force becomes a straight line. The exact-arithmetic difference error is now zero, as the readout reports; the error panel displays floating-point effects. Restore the quartic term and reduce the step from 0.1 mm. Watch for the point at which numerical error stops following the theoretical decrease. Tiny separations become visually indistinguishable in the energy panel, while the logarithmic error view makes their numerical consequences visible.

Finally, move the observation toward larger displacement. For the same quartic coefficient, the energy tangent steepens, holding force rises, and the coefficient of the difference error changes with position. Energy, derivatives, arrays, and errors now belong to one connected investigation: define the physical quantities and assumptions, derive their relationships, and use numerical values and figures to examine those relationships.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P24.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SymPy: Basic Operations](https://docs.sympy.org/latest/tutorials/intro-tutorial/basic_operations.html)

   Substitution and immutable expressions.

   BSD-3-Clause; technical reference
2. [SymPy: Calculus](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html)

   Derivative and integration interfaces.

   BSD-3-Clause; technical reference
3. [SymPy: Lambdify](https://docs.sympy.org/latest/modules/utilities/lambdify.html)

   Connecting expressions to NumPy with ordered arguments.

   BSD-3-Clause; technical reference
4. [SymPy: Gotchas and assumptions](https://docs.sympy.org/latest/tutorials/intro-tutorial/gotchas.html)

   Exact fractions, symbols, and equality.

   BSD-3-Clause; technical reference
5. [SymPy: Assumptions](https://docs.sympy.org/latest/guides/assumptions.html)

   Conditions for real and positive symbols and absolute values.

   BSD-3-Clause; technical reference
6. [SymPy: Expression Manipulation](https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html)

   Expression trees, func, and args.

   BSD-3-Clause; technical reference
7. [SymPy: Numerical solving](https://docs.sympy.org/latest/guides/solving/solve-numerically.html)

   nsolve and initial values for root finding.

   BSD-3-Clause; technical reference
8. [Meurer et al. (2017): SymPy, symbolic computing in Python](https://github.com/sympy/sympy-paper)

   Original authors’ paper and architecture explanation, DOI:10.7717/peerj-cs.103.

   Published article CC-BY-4.0; historical reference; figures here original
