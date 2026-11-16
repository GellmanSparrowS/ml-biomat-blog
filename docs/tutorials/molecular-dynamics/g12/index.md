# 糖的立体形状与身边的水

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g12/
Language: zh-CN

用海藻糖的全原子轨迹理解糖苷键转动、圆周统计和水化层，把化学身份、空间构象与材料问题连起来。

## 糖为什么值得单独建立模型

把一小勺糖放进水里，晶粒逐渐消失，液体却仍然能留下甜味。肉眼看到的是溶解，分子尺度上发生的事情更具体：水不断接近糖表面的氧和氢，糖分子原有的邻居被流动的水替换，分子本身也在弯曲、转动。对于材料研究，这些细节有实际用途。含糖涂层怎样接触水，多糖链的哪个部分更容易被水接近，改变连接方式会怎样影响链的形状，都需要从局部化学结构走到空间和时间上的描述。本讲用一个海藻糖分子作为起点，把“长什么样”和“周围有多少水”变成可以计算、画图和复查的问题。

海藻糖由两个葡萄糖单元相连，属于双糖。它足够小，能够在图上认出每个重要原子；同时又包含糖链研究中的关键结构：有立体方向的糖环、连接两个糖环的糖苷键，以及分布在表面的多个氧。这里的“糖”不是甜味的同义词，而是一类有具体化学结构的分子。许多糖单元连接后形成多糖，链上的连接位置、空间方向和分支都会影响整体构象。先把一个双糖的连接和运动读清楚，后面处理更长的糖链时，就有了可以重复使用的观察单位。

本例采用全原子描述，海藻糖的12个碳、22个氢和11个氧都在模型中，水也逐个放入周期盒。计算首先根据相互作用求出原子受到的力，再推进位置与速度；保存下来的坐标组成轨迹，像一组间隔相同的分子照片。轨迹中的糖苷连接保留既定化学身份，允许的主要变化包括键角振动、单键扭转和水分子的重新排列。若问题涉及糖苷键水解，需要能够描述化学反应的模型；这一讲关注完整海藻糖在液态水中的局部构象与几何水化环境。

读完后，你应当能完成三件相互关联的工作：确认双糖的两个单元究竟怎样连接；运行包含1360个水分子的海藻糖体系；从1 ns轨迹中提取两个糖苷二面角和近邻水数，并说明统计中的单位、阈值与时间范围。下面的结构播放器显示真实保存坐标。观察时先找连接两环的氧桥，再看两环如何围绕它小幅摆动；水的显示可以按阅读需要开关。这样，后面的角度曲线和计数曲线就有了明确的空间对象。

### 水中的海藻糖

真实1 ns轨迹中的保存坐标；两糖环和糖苷桥随时间运动。

公开GLYCAM06j海藻糖全原子模型，经ParmEd 4.3.1转换并逐项核对；45个糖原子、1360个TIP3P水，300 K、1 bar，1 ns生产轨迹共1001帧。

[下载参考数据与完整输入（ZIP） 14.25 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-glycan-reference-data.zip)

这里的1 ns等于1000 ps，也就是十亿分之一秒。虽然日常经验会把它看成很短的一瞬间，分子在这段时间里已经经历许多碰撞与局部转动。分析使用每1 ps保存的一帧，共1001帧，其中包括生产阶段的起点。它们组成一段有明确长度的观测记录。讨论更慢的构象切换时，可以增加独立初态和更长的观测窗口；讨论当前这段记录时，先把已经出现的角度分布、水分子身份和局部差异读准确。

## 从费歇尔的糖到分子的立体身份

十九世纪的糖化学遇到过一个根本问题：有些物质具有相同的元素组成，性质和化学行为却不同。若把分子只看成一张“碳、氢、氧各有多少”的清单，这种差别很难解释。埃米尔·费歇尔把糖的化学转化、合成关系与空间排列联系起来，为糖建立了可比较的立体结构关系；糖和嘌呤的合成研究使他获得1902年诺贝尔化学奖。他在诺贝尔演讲中讨论了不对称碳与糖的异构形式，并展示用平面投影表达立体关系的方法。分子组成回答有哪些原子，立体化学进一步回答这些原子怎样围绕彼此排列。[费歇尔诺贝尔演讲](https://www.nobelprize.org/uploads/2018/06/fischer-lecture-2.pdf)与[诺贝尔奖官方科学史](https://www.nobelprize.org/prizes/chemistry/1902/speedread/)记录了这条思路。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s2)

图 1 · 费歇尔投影用约定明确的平面图记录立体关系。甘油醛的两个镜像结构具有同样的组成，帮助理解为什么糖的身份需要空间信息。

可以用左右手帮助理解手性。两只手都有相同数量的手指，手指之间的连接顺序也相同，但把左手平移、转动，仍不能让它完全套入一副为右手设计的手套。分子中，当一个碳连接四个不同的基团时，也可能出现这种镜像而不能重合的关系。这里的基团可以先理解为沿某条键继续连接的一组原子；判断“四个不同”，要沿连接继续看，而不是只比较紧挨着碳的四个原子的元素。这个类比解释的是空间关系，真正的分子还会热运动，周围的水和相互作用对象也会改变它偏好的姿态。

费歇尔投影是一种有约定的平面记法：交叉点代表相应的碳，水平连接朝向观察者，竖直连接背向观察者。图中的D-甘油醛和L-甘油醛用最简单的一个手性中心展示这一约定。D、L属于构型命名，不能直接读成分子转动的方向或模拟中的正负二面角；把一张投影图任意翻转，也可能改变它所表达的身份。对于初学者，最有用的习惯是把“纸面画法”与“空间约定”一起阅读。只记住字母而忽略它表达的空间关系，到了糖苷连接和模型构建时容易选错分子。

还要分清两个发音相近的词：构型与构象。构型描述这类相对稳定的立体身份，例如一个糖的异头碳处是α还是β；构象描述同一化学身份下通过键的转动和环的变形得到的不同姿态。你可以把一副右手手套的手指弯曲，但它依然是右手手套。对应到本例，两个糖环绕糖苷连接摆动，会改变构象；模拟从一开始就采用α,α-海藻糖的连接与立体构型。后面的角度直方图讨论的是同一个海藻糖模型采到哪些姿态。

这段科学史直接影响建模方法。一个糖的名称、分子式和原子坐标分别提供不同层次的信息：名称应确定糖种与连接，分子式适合检查组成，坐标给出某个起始构象，拓扑则明确每个原子与谁成键以及采用什么参数。它们要指向同一个化学对象。模型检查因此从身份开始，而不是从一张看起来像糖的六边形开始。现代轨迹能给出成千上万幅空间快照，但辨认每幅快照中“还是不是同一个化学对象”的问题，仍然沿着立体化学建立的思路展开。

## 把两个糖环连接成海藻糖

葡萄糖常以环状形式出现在这样的水溶液模型中。一个葡萄吡喃糖环有六个环成员，其中五个是碳、一个是氧；第六个碳位于环外。碳原子的C1、C2等编号沿化学结构定义，所以“六个碳的糖”与“六个成员的环”是两种计数。环内的氧通常记为O5，因为它来自与C5有关的羟基氧。理解这些编号后，读拓扑中的O5—C1连接就容易了：它是糖环的一部分，并不是第五个单体或第五个水分子。

异头碳是形成环时产生关键立体差异的那个碳；在葡萄糖中，它是C1。α与β描述该处取代基相对于规定参照基团的立体关系，在常用的D-葡萄吡喃糖画法中，可以借助取代基与环外羟甲基的相对方向辨认。海藻糖把两个葡萄糖的C1通过一个氧连接，两个异头位置都采用α构型，因此写作α,α-(1↔1)连接。两个数字都为1，明确告诉我们桥连的是两端的异头碳。换成1→4连接时，化学对象和可用的转动环境都会改变，不能只把图上的连线挪一个位置而继续沿用同一份拓扑。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s3)

图 2 · α,α-海藻糖的连接关系。两个环各有一个环内氧原子O5；桥氧O1在拓扑中归属1GA，并连接两个异头碳C1。图中六边形表示连接顺序。

本例拓扑把两个糖残基命名为1GA和0GA。这里的“残基”是文件中用于组织原子的化学单元，并不表示分子已经断成两个独立部分。桥氧O1归属于1GA，跨残基的实际键为1GA:O1—0GA:C1；1GA的C1也与这个O1成键。因此，完整桥连顺序是C1—O1—C1。把桥氧归到哪一侧是一种数据组织方式，不能据此把对称连接解释成一边多一个额外的游离氧。GLYCAM命名把糖种、环形式、构型和占据的连接位置编码进残基名，具体连接仍要和键表一起核对。[GLYCAM官方命名说明](https://glycam.org/docs/forcefield/glycam-naming-2/)解释了这些编码承担的信息。

检查分子式是一项直观的核对。两个游离葡萄糖各有C₆H₁₂O₆的组成，以缩合关系表示连接时，总组成减去一个H₂O，得到海藻糖的C₁₂H₂₂O₁₁。这里是在清点组成，当前模拟从已经连接好的分子开始。12+22+11给出45个原子，模型包含46条共价键；键数比简单开链的“原子数减一”更多，是因为两个糖环各自有闭合连接。由这些数字可以交叉检查是否漏了一个氢、重复放了桥氧，或者在格式转换时丢失了环闭合键。

两个糖环之间并不是一根完全自由的转轴。转动会改变原子之间的相对距离，影响局部排斥、电荷相互作用以及与水的接触，因此不同角度的能量并不相同。描述桥的常见方法是选两个二面角，本例固定φ为1GA:O5—C1—O1—0GA:C1，ψ为1GA:C1—O1—0GA:C1—O5。先写出带残基身份的四原子顺序，再去读角度，可以避免把两个不同的“O5”混在一起。这个习惯会在支化糖链中尤其有用：相同原子名可能出现许多次，残基与连接共同确定测量位置。

## 参数怎样完整地进入GROMACS

坐标只告诉程序原子在哪里，参数还要告诉程序它们怎样相互作用。糖环内的共价键有偏好的长度，三个连续原子形成的键角有偏好的范围，四原子转动有相应的扭转能；距离较远、没有直接成键的原子还会通过电荷和Lennard–Jones相互作用彼此影响。力场把这些规则和数值组织成一套模型。本例采用公开海藻糖的GLYCAM06j全原子参数，数据来自Brandner等人的双糖研究配套资料。该研究还讨论粗粒化参数，本讲使用其中的全原子海藻糖输入来练习构象和水化分析。[公开数据与脚本](https://zenodo.org/records/14291060)和[研究论文](https://doi.org/10.1021/acs.jcim.4c01874)给出了对应的科学对象。

原参数采用Amber文件格式，例题通过ParmEd 4.3.1转换为GROMACS格式。可以把这个过程比作把同一张地图从米换成另一种标注体系：纸面格式和部分数值单位发生变化，地标之间的关系应当保持。真正需要检查的是转换前后的电荷、质量、键图、平衡键长、力常数、二面角项及非键参数是否一致。下面的程序读取两个原始文件，核对其校验值，执行转换，再把结果重新读回进行比较。它还检查原来的46条键、83个键角和160项二面角参数，避免“文件能打开”掩盖模型内容的变化。

### 转换与逐项核对糖参数

```
"""Convert the supplied GLYCAM trehalose parameters and audit the conversion.

Run: python prepare_glycan.py --source . --out prepared
The source directory contains the two Amber files and tip3p.itp.
Dependencies: ParmEd 4.3.1 and NumPy. No parameter fitting is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import numpy as np
import parmed as pmd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('prepared'))
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    names = ['glycan_1GA_0GA_nowat.parm7', 'glycan_1GA_0GA_nowat.rst7']
    expected = ['e879a354e9e935cf73142d587dfe691c476ef88cc49846c7dd6aa9dd3b41b401',
                '2c9525820dae93b400b241554e9a301c1b4624e8a91ccc8bc3a826fa10f0b9d3']
    for name, checksum in zip(names, expected):
        if hashlib.sha256((args.source / name).read_bytes()).hexdigest() != checksum:
            raise ValueError('Source checksum differs: ' + name)
    if pmd.__version__ != '4.3.1':
        raise ValueError('Use ParmEd 4.3.1 for this conversion.')
    original = pmd.load_file(str(args.source / names[0]), xyz=str(args.source / names[1]))
    original.save(str(args.out / 'converted.top'), overwrite=True)
    original.save(str(args.out / 'glycan.gro'), overwrite=True, precision=6)
    converted = pmd.load_file(str(args.out / 'converted.top'), xyz=str(args.out / 'glycan.gro'))
    atom_ids = lambda term: tuple(getattr(term, 'atom' + str(i)).idx
                                  for i in range(1, 5) if hasattr(term, 'atom' + str(i)))
    if len(original.atoms) != 45 or len(converted.atoms) != 45:
        raise ValueError('Expected 45 sugar atoms.')
    comparisons = {}
    for attr, tolerance in [('charge', 1e-7), ('mass', 1e-6), ('sigma', 1e-6), ('epsilon', 1e-8)]:
        error = max(abs(getattr(a, attr) - getattr(b, attr))
                    for a, b in zip(original.atoms, converted.atoms))
        comparisons[attr + '_max_abs_difference'] = float(error)
        if error > tolerance:
            raise ValueError('Converted atomic parameter differs: ' + attr)
    fields = [('bonds', [('k', 1e-4), ('req', 1e-7)]),
              ('angles', [('k', 1e-4), ('theteq', 1e-6)]),
              ('dihedrals', [('phi_k', 1e-6), ('per', 0), ('phase', 1e-6)])]
    for collection, parameters in fields:
        left, right = getattr(original, collection), getattr(converted, collection)
        if len(left) != len(right) or [atom_ids(x) for x in left] != [atom_ids(x) for x in right]:
            raise ValueError('Converted connectivity differs: ' + collection)
        for attribute, tolerance in parameters:
            error = max(abs(getattr(a.type, attribute) - getattr(b.type, attribute))
                        for a, b in zip(left, right))
            comparisons[collection + '_' + attribute + '_max_abs_difference'] = float(error)
            if error > tolerance:
                raise ValueError('Converted bonded parameter differs: ' + attribute)
    pairs = {tuple(sorted((d.atom1.idx, d.atom4.idx))) for d in original.dihedrals
             if not d.improper and not d.ignore_end}
    actual_pairs = {tuple(sorted((p.atom1.idx, p.atom2.idx))) for p in converted.adjusts}
    scales = {(d.type.scee, d.type.scnb) for d in original.dihedrals}
    if pairs != actual_pairs or len(pairs) != 126 or scales != {(1.0, 1.0)}:
        raise ValueError('The original unscaled 1-4 interactions must be retained.')
    if (converted.defaults.fudgeLJ, converted.defaults.fudgeQQ) != (1.0, 1.0):
        raise ValueError('GROMACS 1-4 factors must both be one.')
    coordinate_error = float(np.max(np.abs(original.coordinates - converted.coordinates)))
    if coordinate_error > 6e-6:
        raise ValueError('Coordinate conversion exceeds the six-decimal GRO precision.')
    text = (args.out / 'converted.top').read_text()
    text = text[text.index('[ defaults ]'):]
    text = text.replace('[ moleculetype ]',
                        'OW 8 16.000 0.000 A 3.15061e-01 6.36386e-01\n'
                        'HW 1 1.008 0.000 A 0.0 0.0\n\n[ moleculetype ]', 1)
    text = text.replace('[ system ]', '#include "tip3p.itp"\n\n[ system ]')
    text = text.replace('Generic title', 'Trehalose in TIP3P water')
    text = ('; GLYCAM06j public trehalose topology, converted with ParmEd4.3.1.\n'
            '; Original 1-4 electrostatic and LJ factors = 1.\n' + text)
    (args.out / 'topol.top').write_text(text, encoding='utf-8', newline='\n')
    gro = (args.out / 'glycan.gro').read_text().splitlines()
    gro[0] = 'Trehalose, GLYCAM06j'
    (args.out / 'glycan.gro').write_text('\n'.join(gro) + '\n', newline='\n')
    shutil.copyfile(args.source / 'tip3p.itp', args.out / 'tip3p.itp')
    # These stage inputs are supplied with the example and retain the stated protocol.
    for name in ['em.mdp', 'nvt.mdp', 'npt.mdp', 'md.mdp', 'run.sh']:
        shutil.copyfile(args.source / name, args.out / name)
    report = {'parmed_version': pmd.__version__, 'atoms': 45, 'bonds': len(original.bonds),
              'angles': len(original.angles), 'dihedral_terms': len(original.dihedrals),
              'one_four_pairs': len(pairs), 'fudgeLJ': 1, 'fudgeQQ': 1,
              'net_charge_e': float(sum(a.charge for a in original.atoms)),
              'coordinate_max_abs_difference_A': coordinate_error,
              'parameter_comparisons_in_ParmEd_units': comparisons}
    (args.out / 'conversion-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
```

在例题目录运行python prepare_glycan.py --source . --out prepared，随后进入prepared目录运行。需要ParmEd 4.3.1。

一个值得单独理解的细节叫1–4相互作用。沿一条四原子路径A—B—C—D，A与D之间隔着三条共价键，它们既受到链上键角与扭转项的影响，也可能保留特定的非键相互作用。不同力场对这些作用是否缩放有不同约定。本例GLYCAM参数使用不缩放的电荷与Lennard–Jones 1–4作用，转换后两个缩放因子都为1，实际需要的1–4原子对有126对。把另一个蛋白力场常见的缩放值直接套上来，会改变糖的角度能量，即使原子名称、坐标和分子式看上去完全相同。

水采用TIP3P，氧带−0.834 e电荷，两个氢各带+0.417 e，三者相加为零；e表示一个基本电荷的大小。中性的水分子仍然有电荷分离，所以能够以不同方向靠近糖上不同的极性位点。水的Lennard–Jones参数放在氧上，氢的该项为零。下面的水拓扑规定O—H长度为0.09572 nm，并用氢—氢距离配合确定水的弯曲形状。生产阶段用SETTLE保持水几何，糖中涉及氢的共价键用LINCS约束；它们限制的是快速的共价键振动，糖与水之间的接近和分离仍然发生。

### 水分子的电荷和几何

```
[ moleculetype ]
; molname	nrexcl
SOL		2

[ atoms ]
; id  at type     res nr  res name  at name  cg nr  charge    mass
  1   OW          1       SOL       OW       1      -0.834    16.00000
  2   HW          1       SOL       HW1      1       0.417     1.00800
  3   HW          1       SOL       HW2      1       0.417     1.00800

#ifndef FLEXIBLE

[ settles ]
; OW	funct	doh	dhh
1       1       0.09572 0.15139

[ exclusions ]
1	2	3
2	1	3
3	1	2

#else

[ bonds ]
; i     j       funct   length  force_constant
1       2       1       0.09572 502416.0   0.09572        502416.0 
1       3       1       0.09572 502416.0   0.09572        502416.0 
        

[ angles ]
; i     j       k       funct   angle   force_constant
2       1       3       1       104.52  628.02      104.52  628.02  

#endif
```

TIP3P水与糖的原始GLYCAM参数分别定义，非键组合规则保持一致。

参数准备完成后，目录中有糖坐标、包含完整糖参数的topol.top、水拓扑和四个阶段的设置。原始糖参数与新选择的TIP3P水共同定义本例的溶液模型。盒内只有一个海藻糖，净电荷为零，因此没有为电中和额外加入离子。这个选择适合观察一个糖分子周围的局部水环境；若要研究高浓度糖溶液、盐对糖链的影响或糖—蛋白接触，就需要明确增加对应分子和离子，并用新体系重新比较相互作用与采样。模型内容的增加，应当由所问的问题来决定。

## 让糖和水一起运动

运行从一个边长3.5 nm的立方盒开始。糖放到盒中，水填入剩余空间，重叠过近的水被建模程序排除，最后保留1360个水分子，总原子数为45+3×1360=4125。命令中的spc216.gro提供初始水坐标排列；水的电荷、相互作用和约束由已经包含的TIP3P拓扑决定。区分“放在哪里”的坐标模板与“怎样相互作用”的参数模型，有助于读懂这条看似包含另一个水模型名称的命令。后续能量最小化和动力学准备会调整初始排列。

最小化像是在正式活动前松开几处挤在一起的接触。程序沿降低势能的方向调整坐标，直到达到力的阈值或预设步数。它没有给分子定义通常意义上的运动时间，所以不能把第几次最小化更新当成经过多少皮秒。这里采用最陡下降，最多10000次更新，目标最大力250 kJ mol⁻¹ nm⁻¹，并在这个阶段允许水几何柔性变化。随后20 ps的NVT准备把体系带到300 K附近；N、V、T分别表示粒子数、体积和温度，温度是热浴目标，瞬时测量值会随热运动波动。

### 先消除紧密接触

```
integrator = steep
define = -DFLEXIBLE
nsteps = 10000
emtol = 250
emstep = 0.001
constraints = none
nstenergy = 10
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
```

最陡下降最小化允许水几何柔性调整，目标最大力250 kJ mol⁻¹ nm⁻¹。

### 20 ps定容准备

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 10000
ld-seed = 20263201
continuation = no
gen-vel = yes
gen-temp = 300
gen-seed = 20263200
pcoupl = no
```

随机动力学目标300 K，2 fs步长，重新生成初速度。

接下来的100 ps NPT阶段保持粒子数，允许体积响应压力耦合。这里P表示压力，目标为1 bar；各向同性C-rescale使三个盒方向按同一比例调整，适合这个均匀溶液盒。压力是大量微观动量传递与相互作用共同形成的量，小盒子里的瞬时压力波动可以很大，读取它时应观察时间平均和体积行为。生产阶段继续采用相同的温压目标，记录1 ns。准备和生产是人为划分的用途：前者整理初始环境，后者保存用于当前问题分析的连续观测。

### 100 ps定压准备

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 50000
ld-seed = 20263202
continuation = yes
gen-vel = no
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5
ref-p = 1
compressibility = 4.5e-5
```

延续已有状态，以各向同性C-rescale调节体积至1 bar目标。

### 1 ns观测参数

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 500000
ld-seed = 20263203
continuation = yes
gen-vel = no
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5
ref-p = 1
compressibility = 4.5e-5
```

每1 ps保存坐标；随机动力学、压力耦合和约束设置与正文对应。

动力学采用GROMACS的sd积分器。它通过摩擦和随机作用与300 K热浴交换能量，摩擦对应的时间参数为1 ps；长程静电用PME处理，短程非键截断设为1.1 nm。步长2 fs等于0.002 ps，所以20 ps、100 ps和1000 ps分别需要10000、50000和500000步。约束减少快速键振动对步长的要求，但积分仍然需要逐步检验稳定性。脚本在各阶段延续已有坐标与速度，只在首次NVT开始时生成初速度；后续阶段有各自明确的随机种子。随机热浴的摩擦影响动力学，当前分析据此聚焦构象分布和几何邻居。

### 从糖分子建盒到生产轨迹

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" editconf -f glycan.gro -o boxed.gro -box 3.5 3.5 3.5 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr > npt.grompp.log 2>&1
"$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 2 -pin off > npt.stdout.log 2>&1
"$gmx" grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr > md.grompp.log 2>&1
"$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 2 -pin off > md.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

在新准备目录运行bash run.sh。GMX环境变量可指定GROMACS入口，默认gmx。

实际使用时，在例题目录执行参数准备程序，进入新生成的prepared目录，再运行bash run.sh。运行会依次产生阶段日志、能量文件、坐标和检查点；最终的md.tpr保存本阶段的拓扑与运行设置，md.xtc保存压缩坐标。分析程序读取这两个文件来同时取得原子身份、质量、键和随时间变化的位置。MDAnalysis默认把坐标转换成Å，1 nm等于10 Å，所以分析中0.35 nm要与3.5 Å比较。把单位换算放在读取数据的地方明确处理，能够避免图看起来合理而距离阈值实际上差了十倍。

## 沿着圆周理解糖苷键的转动

二面角需要四个有顺序的原子。A、B、C定义一个平面，B、C、D定义另一个平面，两平面共享B—C这根轴；沿规定方向看过去，两个平面的相对转动给出带正负号的角度。它与三个原子定义的键角不同：键角描述折得有多弯，二面角描述围绕一根轴转到了哪里。想象两页纸沿同一条装订边相连，纸页的开合可以帮助理解两平面之间的转动；分子中的原子会同时振动，所以实际测量仍由每帧四个原子的坐标完成。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s6)

图 3 · 二面角由有顺序的四个原子定义。两平面共享中间的B—C轴；φ与ψ的原子次序固定后，同一角度定义可以用于每一帧。

对本例而言，φ使用第17、2、1、24号原子，ψ使用第2、1、24、39号原子。这些是从1开始的原子编号，Python数组从0开始，程序因此使用减1后的下标，并进一步核对每个位置的残基名与原子名。计算函数使用当帧的周期盒，避免跨边界的坐标把相邻原子拉成远距离连接。真实记录中，φ约在40.43°到104.43°之间变化，ψ约在46.27°到100.26°之间变化；在这个保存窗口内，两者围绕同一个局部角度区域波动。

### 两个糖苷二面角的时间记录

1001帧，间隔1 ps；虚线标记各自的圆均值。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s6)

同一糖苷桥两侧φ与ψ的实际1 ns记录。角度由明确列出的四原子顺序计算，周期边界使用原生盒矢量处理。

角度是绕一圈回到原处的量，平均方法也应当尊重这个特点。179°与−179°之间只隔2°，但把两个带符号数字直接相加再除以2，得到的是0°。原因在于−180°与180°是同一位置，数字轴上的断点并不是分子运动中的障碍。圆周平均先把每个角度画成单位圆上的箭头，将水平和竖直分量分别相加，再从合箭头读回方向。下面的公式把这幅图写成运算；其中atan2同时读取两个分量，因此知道合箭头处在哪个象限。

用方向求平均角度式 1

![用方向求平均角度](https://ml-biomat.com/static/agent-math/a472d03ea64242a4a66ce242.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| θⱼ | 第j帧记录的二面角 | 三角函数中用rad；输出可换成° |
| θ̄ | 平均方向对应的角度 | rad或°，注明输出约定 |
| j、M | 帧编号；参与统计的帧数 | 无量纲 |
| sin、cos | 把圆周方向分成竖直和水平分量 | 输出无量纲 |
| ∑、j=1、= | 从第1帧累加到第M帧；等号表示定义的相等关系 | 运算符 |
| atan2(y,x) | 根据竖直分量y和水平分量x确定所在象限与角度 | 输出rad |

怎样理解每个角度先变成一根单位长度的箭头，合并所有箭头后再读方向。把正弦、余弦的和都除以M不改变方向，因此这里直接用两个和。

算一个例子179°与−179°的正弦相互抵消，余弦和约为−1.99970，合箭头指向180°。普通算术平均给0°，相差半圈。实际轨迹的φ圆均值为71.88655°。

使用条件用于等权角度记录。合箭头长度为零时平均方向没有定义；极小的长度意味着单一平均方向概括不了分布。

把两根箭头放到圆周上，再比较两种平均方法。

圆周统计的几何练习。两根方向箭头由滑块指定，红色箭头是它们的向量平均。

平均方向之外，还要问角度散得有多开。若所有箭头几乎平行，它们的平均长度接近1；若指向四面八方，箭头互相抵消，平均长度就变短。把这个长度记为R，可以进一步定义圆标准差。实际φ和ψ的圆均值分别为71.88655°与71.85063°，圆标准差分别为9.05662°与8.73675°。它们描述当前1001帧中的典型方向与离散程度。两个均值接近，和海藻糖两端相似的化学环境相容；要比较微小差别，还需要看时间分块与独立重复。

平均方向有多集中式 2

![平均方向有多集中](https://ml-biomat.com/static/agent-math/392c31afca4b8f1a74abafe5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| C、S | 所有cos θⱼ、sin θⱼ各自的算术平均 | 无量纲 |
| R | 平均单位箭头的长度，范围0到1 | 无量纲 |
| s_{circ} | 圆标准差，弧度结果乘180/π可换为度 | rad |
| π | 圆周率，约3.14159；半周为π rad，等于180° | 无量纲 |
| 180/π | 弧度转为度的换算系数，约57.2958；斜线表示相除 | °/rad |
| √、²、+ | 正平方根；平方；相加 | 运算符 |
| ln、−、2、= | 自然对数；负号；定义中的常数2；等号 | 运算符与无量纲常数 |

怎样理解长度接近1说明方向接近，方向分散会使箭头相互抵消。这一定义把长度换成角度尺度；在很窄、近似正态的角度簇中，它接近普通角度标准差。

算一个例子本例φ的R=0.987585，−2ln R约为0.02499，开平方约0.15807 rad，再乘180/π得到9.05662°。

使用条件要求0<R≤1；R=0的角分布需要直接报告分布。圆标准差描述所记录角度的离散程度，均值的统计误差还需要时间相关和独立重复分析。

### 构象簇的二维分布

二维格宽5°×5°，一维格宽5°；颜色和高度均为保存帧计数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s6)

1001帧的双二面角联合分布与角度统计；同一帧的φ、ψ成对保留，圆统计通过方向向量平均处理角度周期性。

二维图把每帧的φ与ψ作为同一个点保留下来，横轴和纵轴分别对应两个角度，颜色显示每个5°×5°格里落入多少帧。两条一维直方图只保留各自的计数，因此二维图还可以显示两个转动是否倾向于一起变化。这里把观察到的局部簇画在0°到150°范围内，让其宽度和形状容易辨认。对更长轨迹，如果角度越过±180°边界，应先选择一致的周期显示方式。构象有两个相隔很远的簇时，先描述两个簇的占据和转换，再选择能够表达它们的统计量，比只报告一个落在中间的平均角度更有信息。

## 糖周围的水应该怎样数

“一个糖周围有多少水”需要先指定“周围”的含义。本讲定义一个几何壳层：只要某个水的氧距离任意一个糖氧小于0.35 nm，就把这个水计入；距离采用周期最小镜像。同一个水可以同时靠近两个糖氧，但对整个糖的水化数只贡献一次。这个规则便于复现，也直接对应空间接近程度。氢键是更具体的相互作用分类，需要进一步检查供体、受体和氢的方向；水在壳层里待了多久，又需要跟踪同一个水分子的身份随时间变化。距离计数为这些更细的分析提供起点。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s7)

图 4 · 一个水氧可以同时进入两个糖氧的距离阈值。逐位点计数适合比较局部环境；按水身份取并集适合回答整个糖周围共有多少去重后的水分子。

把重叠的水化区域合并后计数式 3

![把重叠的水化区域合并后计数](https://ml-biomat.com/static/agent-math/106c1bcd0ad06f0ebb159a9c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N_{water}(t;r_{c}) | 时刻t、阈值r_c下的独立近邻水分子数 | 无量纲计数 |
| t、r_{c} | 保存帧的时间；距离阈值 | ps；nm |
| w、N_{W} | 水分子编号；盒内水分子总数1360 | 无量纲 |
| o、𝒪 | 糖氧编号；糖分子11个氧构成的集合 | 编号与集合 |
| d_{ow}(t) | 糖氧o到水氧w的周期最小镜像距离 | nm |
| 𝟙[·] | 条件满足取1，否则取0的指示函数 | 无量纲 |
| min、∈、∑、<、= | 取最小值；属于集合；求和；严格小于；等号 | 运算符 |

怎样理解先对一个水寻找最近的糖氧，再决定它是否进入壳层，因此同一个水同时靠近两个糖氧也只贡献1。最后对全部水相加得到区域并集内的水数。

算一个例子若水A同时靠近两个糖氧、水B只靠近其中一个氧，逐位点合计为3，去重后的水分子数为2。本例r_c=0.35 nm时，1001帧的平均去重水分子数为23.18282。

使用条件这是氧—氧距离定义的几何壳层。若研究氢键，应增加供体、受体及方向判据；若研究水交换，应继续跟踪水分子身份与时间。

实现时，程序先计算11个糖氧与1360个水氧之间的距离矩阵。可以把它想成一张表：每行是一个糖氧，每列是一个水氧，格子里写两者的距离。沿一列取最小值，就找到了这个水离糖上哪个氧最近；将该值与3.5 Å比较，便得到这个水是否在壳层里的答案。最后把所有列的“是”相加，得到当帧去重水分子数。这种顺序把“先确定水的身份，再决定是否计数”写得很直接，也避免用几个重叠球的体积相加来代替真实粒子计数。

### 距离阈值怎样影响水化计数

左图使用0.35 nm，右图逐一改变阈值；阴影表示逐帧标准差。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s7)

以糖氧—水氧最近距离识别几何水化壳，比较逐帧不同水分子数及改变壳半径的结果。同一水接近多个糖氧时只计一次。

实际1001帧得到平均去重水分子数23.18282，逐帧标准差2.33283，保存帧中的最小值与最大值分别为15和30。平均数可以带小数，因为它概括许多个整数计数；一帧里仍然只有整数个水。右图把阈值从0.25 nm逐渐增加到0.50 nm，每一帧进入邻域的水数都会保持不减，曲线因此向上增长。选择0.35 nm是在定义本次比较的观察尺度，改变尺度后应该一并报告新的定义。阴影反映同一阈值下计数随帧的波动，不把它当作平均值的置信区间。

平均水数与逐帧波动式 4

![平均水数与逐帧波动](https://ml-biomat.com/static/agent-math/7589de5d9a934c77aeb1bad2.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Nⱼ、⟨N⟩ | 第j帧的去重水分子数；全部帧的平均值 | 无量纲计数 |
| s_{N} | 采用分母M的逐帧标准差 | 无量纲计数 |
| j、M | 帧编号；等时间间隔记录的帧数 | 无量纲 |
| ∑、1/M、−、²、√、= | 求和；除以帧数；差值；平方；正平方根；等号 | 运算符 |

怎样理解平均数给出记录期间的典型占据水平；把每帧偏离均值的距离平方再平均，消去正负抵消，最后开平方恢复计数尺度。

算一个例子三个示意帧有21、23、25个水，均值为23，标准差为√(8/3)=1.633。实际1001帧得到23.18282和2.33283。

使用条件这里概括已保存帧的分布，故分母用M。相邻帧相关时，均值的误差需要分块或独立重复计算，不能直接把M当独立样本数。

逐氧位点的统计回答另一个问题：水更容易出现在糖的哪个位置？本例桥氧1GA:O1周围平均约0.660个水，两个环内氧原子O5周围分别约1.419和1.421个水，两个O6位点周围分别约3.454和3.430个水。桥附近的几何遮挡、各氧的电荷环境及邻近基团共同影响这些数值，所以可以把差别读成该模型中局部接近机会的差别。要单独归因于电荷或空间遮挡，需要改变一个因素并保持其他条件一致，或按相同构象进一步比较。每根柱的误差线给出该位点的逐帧标准差。

### 各个糖氧身边的水

以同一0.35 nm阈值逐位点统计；误差线为逐帧标准差，同一水可出现在不同位点计数中。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/#zh-s7)

11个糖氧位点各自在0.35 nm内的近邻水数，误差定义见图。位点之间可能共享同一水，位点计数之和与水分子并集分别解释。

把全部11个氧的平均位点计数相加，得到29.23377，比整个糖的23.18282更大，差值来自同时靠近多个位点的水。两种算法都保留了有用的信息：去重水分子数适合描述整个分子的邻域，逐位点计数适合定位接触位置。代码同时导出两者，便于直接检查“各位点之和不小于并集计数”这个关系。下面的完整分析还输出角度、阈值敏感性、逐氧计数和四个250 ps分块；其中每块采用左开右闭的时间区间，包含250帧，以避免把边界帧重复计入相邻两块。

### 完整角度与水化分析

```
"""Analyze trehalose torsions and geometrical hydration from TPR + XTC.

Run: python analyze_glycan.py --run . --out figures --language en
Dependencies: MDAnalysis 2.11, NumPy 2.5, Matplotlib 3.11.
MDAnalysis returns coordinates in angstroms and time in picoseconds.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_dihedrals, distance_array, calc_bonds
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def circular_stats(degrees):
    z = np.exp(1j * np.deg2rad(degrees)).mean()
    length = float(abs(z))
    return {'mean_deg': float(np.rad2deg(np.angle(z))),
            'resultant_length': length,
            'circular_sd_deg': float(np.rad2deg(np.sqrt(-2 * np.log(length))))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    chinese = [f for f in ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
                           'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family': chinese if args.language == 'zh' else ['DejaVu Sans'],
                         'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2',
                         'svg.fonttype': 'path'})
    u = mda.Universe(str(args.run / 'md.tpr'), str(args.run / 'md.xtc'))
    sugar = u.atoms[:45]
    if [(r.resname, len(r.atoms)) for r in sugar.residues] != [('1GA', 23), ('0GA', 22)]:
        raise ValueError('Expected the supplied 45-atom trehalose topology.')
    composition = {e: sum(a.name.startswith(e) for a in sugar) for e in ['C', 'H', 'O']}
    if composition != {'C': 12, 'H': 22, 'O': 11} or abs(sugar.charges.sum()) > 1e-5:
        raise ValueError('Expected neutral C12H22O11.')
    torsions = np.array([[16, 1, 0, 23], [1, 0, 23, 38]])
    expected = [[('1GA', 'O5'), ('1GA', 'C1'), ('1GA', 'O1'), ('0GA', 'C1')],
                [('1GA', 'C1'), ('1GA', 'O1'), ('0GA', 'C1'), ('0GA', 'O5')]]
    for ids, identities in zip(torsions, expected):
        if [(a.resname, a.name) for a in u.atoms[ids]] != identities:
            raise ValueError('Dihedral atom identities differ from the supplied model.')
    oxygen = sugar.select_atoms('name O*')
    water = u.select_atoms('resname SOL and name OW')
    bonds = np.array([b.indices for b in sugar.bonds if np.all(b.indices < 45)])
    if len(bonds) != 46 or not any(set(b) == {0, 23} for b in bonds):
        raise ValueError('Expected both sugar rings and the inter-residue O1-C1 bond.')
    if len(water) != 1360 or len(u.atoms) != 4125:
        raise ValueError('Expected the supplied 1360-water system.')
    radii_nm = np.arange(25, 51, dtype=float) / 100
    selected_radius = int(np.flatnonzero(np.isclose(radii_nm, .35))[0])
    rows = []; threshold_counts = []; site_counts = []; max_bond = 0.
    for ts in u.trajectory:
        if not np.isfinite(ts.positions).all():
            raise ValueError('Non-finite coordinate.')
        angles = [np.rad2deg(calc_dihedrals(*u.atoms[ids].positions, box=ts.dimensions))
                  for ids in torsions]
        distances = distance_array(oxygen.positions, water.positions, box=ts.dimensions)
        # The minimum over sugar oxygens counts each water once at each radius.
        closest = distances.min(axis=0)
        counts = (closest[:, None] < 10 * radii_nm[None, :]).sum(axis=0)
        sites = (distances < 3.5).sum(axis=1)
        rows.append([ts.time, *angles, counts[selected_radius], sites.sum(), ts.volume / 1000])
        threshold_counts.append(counts); site_counts.append(sites)
        max_bond = max(max_bond, float(calc_bonds(u.atoms[bonds[:, 0]].positions,
                       u.atoms[bonds[:, 1]].positions, box=ts.dimensions).max() / 10))
    a = np.asarray(rows); thresholds = np.asarray(threshold_counts); sites = np.asarray(site_counts)
    if len(a) != 1001 or not np.allclose(a[:, 0], np.arange(1001)) or max_bond > .20:
        raise ValueError('Unexpected frame times or sugar bond geometry.')
    if not np.all(np.diff(thresholds, axis=1) >= 0) or not np.all(a[:, 4] >= a[:, 3]):
        raise ValueError('Hydration union and per-site counts are inconsistent.')
    block_results = []
    for lo in range(0, 1000, 250):
        keep = (a[:, 0] > lo) & (a[:, 0] <= lo + 250)
        block_results.append({'time_ps': [lo, lo + 250], 'endpoint_rule': '(start, end]',
                              'frames': int(keep.sum()),
                              'phi': circular_stats(a[keep, 1]), 'psi': circular_stats(a[keep, 2]),
                              'unique_water_mean': float(a[keep, 3].mean())})
    summary = {'frames': len(a), 'time_ps': [float(a[0, 0]), float(a[-1, 0])],
               'atom_count': len(u.atoms), 'sugar_atoms': 45, 'water_count': len(water),
               'formula': 'C12H22O11', 'sugar_mass_u': float(sugar.masses.sum()),
               'sugar_charge_e': float(sugar.charges.sum()), 'sugar_bonds': len(bonds),
               'max_sugar_bond_nm': max_bond, 'torsion_indices_one_based': (torsions + 1).tolist(),
               'phi': circular_stats(a[:, 1]), 'psi': circular_stats(a[:, 2]),
               'angle_min_max_deg': [[float(a[:, i].min()), float(a[:, i].max())] for i in [1, 2]],
               'hydration_radius_nm': .35, 'unique_water_mean': float(a[:, 3].mean()),
               'unique_water_frame_sd': float(a[:, 3].std()),
               'unique_water_min_max': [int(a[:, 3].min()), int(a[:, 3].max())],
               'per_site_count_sum_mean': float(a[:, 4].mean()),
               'oxygen_labels': [f'{o.resname}:{o.name}' for o in oxygen],
               'oxygen_mean_counts': sites.mean(axis=0).tolist(),
               'blocks': block_results,
               'definition': 'All 1001 equally spaced saved frames. A water is in the geometrical '
                             'shell when its oxygen is strictly closer than 0.35 nm to any sugar '
                             'oxygen under periodic minimum-image geometry. Unique water counts '
                             'use the union of sites; per-site counts may repeat a water. '
                             'Frame standard deviations describe fluctuations, not mean uncertainty.'}
    (args.out / 'glycan_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out / 'glycan_timeseries.csv', a, delimiter=',', comments='',
               header='time_ps,phi_deg,psi_deg,unique_waters_035nm,sum_site_counts,volume_nm3')
    np.savetxt(args.out / 'glycan_thresholds.csv', np.column_stack([radii_nm, thresholds.mean(0),
               thresholds.std(0)]), delimiter=',', comments='', header='radius_nm,mean_unique_water,frame_sd')
    np.savetxt(args.out / 'glycan_sites.csv', np.column_stack([sites.mean(0), sites.std(0)]),
               delimiter=',', comments='', header='mean_count,frame_sd; rows: ' + ','.join(summary['oxygen_labels']))

    def save(fig, name):
        fig.savefig(args.out / (name + '.svg'), bbox_inches='tight')
        fig.savefig(args.out / (name + '.png'), dpi=160, bbox_inches='tight')
        plt.close(fig)

    blue, red, gold = '#176d83', '#b44e3f', '#b28a35'
    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6.3), sharex=True, layout='constrained')
    for i, (symbol, color) in enumerate([('φ', blue), ('ψ', red)]):
        ax[i].plot(a[:, 0], a[:, i + 1], lw=.8, color=color, alpha=.7,
                   label=tr('每 1 ps 保存的角度', 'Angles saved every 1 ps'))
        mean = summary['phi' if i == 0 else 'psi']['mean_deg']
        ax[i].axhline(mean, color='#292f34', ls='--', lw=1.5,
                      label=tr(f'全程圆均值 {mean:.2f}°', f'Circular mean {mean:.2f}°'))
        ax[i].set_ylabel(symbol + tr(' / 度', ' / degrees'))
        ax[i].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
        ax[i].grid(axis='y', alpha=.15)
    ax[-1].set_xlabel(tr('生产阶段时间 / ps', 'Production time / ps'))
    save(fig, 'glycan-torsions')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
    edges = np.arange(0, 151, 5)
    hist = ax[0].hist2d(a[:, 1], a[:, 2], bins=[edges, edges], cmap='YlGnBu', cmin=1)
    fig.colorbar(hist[3], ax=ax[0], label=tr('每个 5° × 5° 格的帧数', 'Frames per 5° × 5° bin'))
    ax[0].set(xlabel='φ / ' + tr('度', 'degrees'), ylabel='ψ / ' + tr('度', 'degrees'),
              xlim=(0, 150), ylim=(0, 150))
    ax[1].hist(a[:, 1], bins=edges, histtype='step', lw=2, color=blue, label='φ')
    ax[1].hist(a[:, 2], bins=edges, histtype='step', lw=2, color=red, label='ψ')
    ax[1].set(xlabel=tr('二面角 / 度', 'Dihedral / degrees'), ylabel=tr('每个 5° 格的帧数', 'Frames per 5° bin'),
              xlim=(0, 150))
    ax[1].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
    save(fig, 'glycan-angle-map')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
    ax[0].plot(a[:, 0], a[:, 3], color=blue, lw=.8, label=tr('0.35 nm 内的去重后的水分子', 'Unique waters within 0.35 nm'))
    ax[0].axhline(a[:, 3].mean(), color=red, ls='--', lw=1.6,
                  label=tr(f'均值 {a[:, 3].mean():.2f}', f'Mean {a[:, 3].mean():.2f}'))
    ax[0].set(xlabel=tr('生产阶段时间 / ps', 'Production time / ps'), ylabel=tr('水分子数', 'Water molecules'))
    mean = thresholds.mean(0); sd = thresholds.std(0)
    ax[1].plot(radii_nm, mean, color=blue, lw=2, label=tr('平均去重后的水分子数', 'Mean unique-water count'))
    ax[1].fill_between(radii_nm, mean - sd, mean + sd, color=blue, alpha=.17,
                        label=tr('逐帧标准差', 'Frame standard deviation'))
    ax[1].axvline(.35, color=red, ls='--', lw=1)
    ax[1].set(xlabel=tr('距离阈值 / nm', 'Distance threshold / nm'), ylabel=tr('水分子数', 'Water molecules'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), fontsize=10, frameon=False)
        axis.grid(axis='y', alpha=.15)
    save(fig, 'glycan-hydration')

    fig, ax = plt.subplots(figsize=(11.5, 4.8), layout='constrained')
    colors = [blue if o.resname == '1GA' else gold for o in oxygen]
    ax.bar(np.arange(len(oxygen)), sites.mean(0), color=colors, width=.68)
    # Intervals here describe fluctuations at a site, not statistical confidence.
    ax.errorbar(np.arange(len(oxygen)), sites.mean(0), yerr=sites.std(0), fmt='none',
                 color='#333333', capsize=4, lw=1.2)
    ax.set_xticks(np.arange(len(oxygen)), summary['oxygen_labels'], rotation=30, ha='right')
    ax.set_ylabel(tr('0.35 nm 内的平均水数', 'Mean waters within 0.35 nm'))
    ax.plot([], [], color=blue, lw=8, label='1GA')
    ax.plot([], [], color=gold, lw=8, label='0GA')
    ax.plot([], [], color='#333333', lw=1.2, label=tr('误差线：逐帧标准差', 'Error bars: frame standard deviation'))
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, frameon=False)
    ax.grid(axis='y', alpha=.15)
    save(fig, 'glycan-sites')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

运行python analyze_glycan.py --run prepared --out figures --language zh。分析只读取md.tpr与md.xtc。

## 从一个双糖走向糖链材料

一段轨迹提供两种尺度的信息。快速起伏告诉我们分子在当前环境中怎样活动，较长时间块之间的差别则帮助检查这些活动是否围绕相似的统计状态。把本例分成四个250 ps区间，φ圆均值依次约为71.14°、71.46°、71.57°和73.43°；去重水分子数均值分别为23.192、23.104、23.328和23.116。角度的最后一块稍向较大值移动，水数的四块均值相近。下一轮若研究角度的精细分布，可以延长观测并设置独立初速度重复，比较这些块与重复之间的差异，而不把每一张相邻照片都当作一次全新的独立实验。

从双糖扩展到多糖时，首先增加的是连接问题。每增加一个糖单元，就要确认糖种、α或β构型、连接的碳位与是否分支；每个连接又带来局部转动自由度。一个由许多相似单元组成的链，也可能因连接位置不同而在空间上更伸展、弯曲或形成螺旋倾向。建立更长模型时，可以沿用本讲的检查顺序：核对残基和跨残基键，检查组成、电荷与参数，再选择能够描述链整体形状的量。局部φ、ψ与整体回转半径分别观察不同尺度，二者配合才能把某段连接的偏好与整条链的形状联系起来。

如果研究糖与蛋白质的结合，当前的位点水化图可以帮助提出一个明确问题：结合位点占据糖表面某个区域时，原来接近该区域的水会怎样变化？建立复合物后，可以同时测糖—蛋白接触、糖的角度分布和同一批糖氧周围的水数，并在结合与分离的结构条件下比较。氢键分析应给出供体、受体与方向标准，水交换分析应明确连续停留还是允许短暂离开的定义。这样，结构图中一条虚线、曲线里一次计数增加和某个水的停留时间，各自都有清楚的测量对象。

对于含糖材料，研究问题还可以落在浓度、链间联系和界面环境上。提高糖浓度会同时改变可用水的数量、糖之间的接近机会和溶液的整体性质；把糖接到表面，会限制其可达构象；引入更长的糖链，则增加相互遮挡和多点接触。设计比较时，可以先固定力场、水模型、温度、压力和统计阈值，再明确改变其中一个结构因素，记录每个条件下实际的糖数、水数、体积和观察时间。若跨体系比较水化，还应同时报告每个分子、每个糖单元或每个氧位点的计数口径，让数字与材料组成相匹配。

本讲得到的直接认识来自相互连接的三层证据：拓扑确定α,α-海藻糖的化学身份，角度轨迹显示糖苷桥附近的局部构象簇，氧位点与去重水分子数把分子的空间形状接到周围溶剂。读者可以从改动距离阈值和时间分块开始练习，再把同样的原子身份检查、参数核对和统计定义带到新的糖链。一个可解释的糖模拟，最终应让每条曲线都能回到图中的具体原子和真实空间关系，并让每次模型扩展都对应一个新的材料问题。

## 延伸阅读与开放资料

- [Systematic Approach to Parametrization of Disaccharides for the Martini 3 Coarse-Grained Force Field: data and scripts](https://zenodo.org/records/14291060) · Brandner et al. · CC BY 4.0

  公开海藻糖GLYCAM06j全原子参数与初始坐标。

  保留糖参数，经ParmEd转换；新建TIP3P水盒，并使用本讲的短时准备和1 ns观测流程。
- [Systematic Approach to Parametrization of Disaccharides for the Martini 3 Coarse-Grained Force Field](https://doi.org/10.1021/acs.jcim.4c01874) · Brandner et al. · Research article; cited for scientific context

  双糖构象与全原子参考模型的研究背景。

  本讲分析公开全原子海藻糖模型，讲解角度和水化测量。
- [GLYCAM naming convention](https://glycam.org/docs/forcefield/glycam-naming-2/) · GLYCAM developers · Official documentation; cited

  糖类型、环形式、构型与连接位置的命名原则。

  结合本例两残基与实际成键解释。
- [Syntheses in the purine and sugar group](https://www.nobelprize.org/uploads/2018/06/fischer-lecture-2.pdf) · Emil Fischer, Nobel Lecture, 1902 · Historical lecture; cited, figures drawn independently

  糖立体结构问题与费歇尔投影的科学史。

  用甘油醛镜像投影重新绘制原理图。
- [Bringing chemistry to biology](https://www.nobelprize.org/prizes/chemistry/1902/speedread/) · Nobel Prize Outreach · Official historical account; cited

  费歇尔糖研究与1902年诺贝尔化学奖的背景。

  将历史问题与分子模型中的构型、构象联系。
- [MDAnalysis distance and dihedral functions](https://docs.mdanalysis.org/stable/documentation_pages/lib/distances.html) · MDAnalysis developers · Official documentation; cited; MDAnalysis LGPL-3.0

  周期最小镜像距离与有符号二面角计算。

  编写本例完整分析程序，固定原子身份与统计窗口。
- [ParmEd](https://github.com/ParmEd/ParmEd) · ParmEd developers · LGPL-2.1-or-later

  Amber与GROMACS参数格式转换，使用4.3.1。

  增加电荷、质量、连接、势参数与1–4相互作用逐项检查。
