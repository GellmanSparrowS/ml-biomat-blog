# 完整研究：PEG链长、构象与水化

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g18/
Language: zh-CN

比较三种 PEG 链长与六条真实轨迹，把空间尺寸、水化计数和采样差异放进同一项可重算研究。

## 把链加长，究竟改变了什么

把一根短棉线接成长棉线，线的总长度增加了，但它落在桌面上占据的范围还取决于怎样弯曲。水中的聚乙二醇链也有类似的两把尺子：沿着化学键走完一遍的长度，以及整条链在空间中铺开的尺寸。对于希望在材料表面布置柔软链段、设计分子连接臂或理解水如何靠近聚合物的人，这个区别很实际。多加几个重复单元，会增加可连接的原子、可以转动的键和与水接触的位置；这些变化一起发生，最终的空间尺寸需要从分子的运动中读取。

本讲把这个问题做成一项可以完整重算的小研究：比较含有 8、16 和 32 个 EO 重复单元的双羟基 PEG，每一种长度各有两条生产阶段为 2 ns 的轨迹。EO 在这里指链上反复出现的 –CH₂–CH₂–O– 化学片段，末端的补足方式稍后单独说明。三组使用同一套原子参数、同一种水模型、相同温度和压力设置。我们依次看链的尺寸、尺寸随链长增加的方式，以及水的近邻数；同时保留每条轨迹的区别，让比较既有共同的尺子，又看得见分子运动带来的起伏。

这样的设计也把“条件相同”说得更具体。每个盒子只有一条聚合物链，初始盒长都是 6 nm，装入水后在压力调节下允许体积变化。因此固定的是链的条数和建盒规则，聚合物质量分数会随链长改变；比较固定质量分数的溶液，需要另行调整水量或链条数。末端都保留羟基，没有把链的一端绑在表面，也没有在水中加入盐。读图时可以把研究对象想成自由漂浮的单链水溶液模型。若研究表面刷层，还要加入接枝位置、链间拥挤和表面相互作用，这些条件会重新组织链能够探索的空间。

完成这一讲后，你应该能把“长链更大”拆成可以检查的几个问题：化学上到底多了多少原子，空间尺寸采用哪种平均，较大的水化计数是否只是因为氧位点更多，以及两条轨迹是否对同一趋势给出相近的回答。这里的研究顺序可以直接迁移到肽链长度、连接臂组成或糖链支化程度的比较。迁移时先明确改变的化学变量，再保留其余建模条件，最后选择与问题对应的测量量。一次清楚的比较，往往比给单条漂亮轨迹附上许多形容词更有解释力。

## 先把重复单元、端基和原子数对齐

PEG 的分子式可以写成 HO–(CH₂–CH₂–O)ₙ–H。沿着主链看，每增加一个 EO 片段，就增加两个碳、四个氢和一个氧；整条链还需要补足两端的原子。由此得到碳原子数为 2n，氢原子数为 4n+2，氧原子数为 n+1。原子总数是三项相加后的 7n+3。这个简单计数值得在运行前完成：它同时检查了链长、末端形式和模型是否显式保留氢原子。以 PEG8 为例，16 个碳、34 个氢和 9 个氧合起来是 59 个原子；PEG32 则有 64 个碳、130 个氢和 33 个氧，总计 227 个。

由化学重复数检查原子数式 1

![由化学重复数检查原子数](https://ml-biomat.com/static/agent-math/9e1b62b0cd7c6e085ab93c3f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n | 化学 EO 重复单元数 | 1 |
| N_{C}, N_{H}, N_{O} | 碳、氢、氧原子数 | 1 |
| N_{a} | 链的总原子数 | 1 |
| 2, 4, 1, 7, 3 | 由每个重复片段及两个端基的原子组成得到的整数系数 | 1 |
| =, +, × | 相等、加法；数字与 n 相邻表示相乘 | 1 |

怎样理解将 HO–(CH₂–CH₂–O)ₙ–H 的每一种元素逐项相加，原子总数再对元素计数求和。

算一个例子n=16：碳 32、氢 66、氧 17，总计 115 个原子；软件组装片段为 17 个。

使用条件两端均为羟基、所有氢显式存在的中性直链 PEG；换端基时重新计数。

软件的组装片段与化学重复单元需要分别理解。这里使用 Polyply 的 oplsaaLigParGen 参数库：一个 OHter 片段提供 CH₃O，内部 PEO 片段提供 C₂H₄O，连接定义负责把片段接成完整主链。生成 PEGn 的序列因此是 OHter:1 PEO:(n−1) OHter:1。PEG16 对应 1 个左端片段、15 个内部片段和 1 个右端片段，共 17 个软件残基，却有 16 个化学 EO 重复单元。残基只是组织原子的一种分组方式；本讲的链长横坐标始终是化学上的 n。把软件分组数量误当成 n，会使原子计数、端基比例和归一化全部偏移。

原子数还可以换成更常见的摩尔质量。按碳 12.011、氢 1.008、氧 15.999 g/mol 的原子摩尔质量相加，每增加一个 EO 就增加约 44.053 g/mol，整条双羟基链还带有约 18.015 g/mol 的端部补足量。于是三种链的摩尔质量约为 370.439、722.863 和 1427.711 g/mol。摩尔表示把极大量的相同分子作为一份来计数，摩尔质量则描述这一份的质量。原子计数给出的是一个分子内部的组成，摩尔质量把同样的组成连接到称量实验；这两种尺度之间的联系，有助于把模拟中的 n 与实际选用的分子样品对应起来。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s2)

图 1 · 化学 EO 数为 n，软件片段数为 n+1；两端羟基使氧位点的类型比例随链长改变。

两个末端还使短链和长链在化学组成比例上存在有意思的区别。每条链都有两个羟基氧，其余 n−1 个氧位于内部醚键位置。按氧位点计算，末端比例在 PEG8 中是 2/9，约 22.2%；到 PEG32 则成为 2/33，约 6.1%。羟基氧和内部醚氧周围的原子连接、局部电荷与氢键角色不同，因此每个氧的平均近邻水数可以随 n 改变。这个变化可能同时包含端基比例下降和链构象改变。若要进一步分辨两种原因，可以保留当前轨迹，把末端氧与内部氧分别统计，再比较相同化学类型的局部环境。

完整建模程序先复制一致的力场文件，再为三个 n 写入对应的序列、随机种子和模拟参数。拓扑生成解决“有哪些原子、怎样相互作用”，坐标生成解决“这些原子最初放在哪里”；两步的职责不同。初始构象生成种子分别固定，随后对每种长度完成同一套最小化与平衡准备。两条运动历史共享该长度的最小化构型，却使用各自的初速度和随机温控种子。这样可以观察运动历史的影响，也保留了对共同起点的认识。若要检验初始构象本身的影响，应另外生成几个不同形状，并沿相同流程各自准备。

## 从随机步行到真实链：为何要除以链长的平方根

把柔性分子当成一串能够转向的线段，是高分子统计理论中一个很有用的简化。先想象一个人在空旷地面上走路，每一步长度相同，却不断改变方向。走过的路程逐步累加，起点到终点的直线距离却会受到前后方向抵消的影响。聚合物的理想随机链模型也利用了这种几何关系，只是线段在三维空间中取向。这里比较的是许多可能构象中的端到端距离，而不是一个人在时间中的行走速度。把这个模型当作尺寸增长的参照，有助于理解为什么链长增加一倍，空间尺寸通常不需要增加一倍。

理想独立随机线段的尺寸式 2

![理想独立随机线段的尺寸](https://ml-biomat.com/static/agent-math/bd5b2eb5ec6fe72ef03b5229.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| R_{rms} | 构象群中端到端距离的均方根 | nm |
| b | 统计线段的固定长度 | nm |
| N | 独立、各向同性取向的线段数 | 1 |
| L | 所有线段长度相加的轮廓长度 | nm |
| √, /, ×, = | 非负平方根、除法、相乘和相等；Nb 表示乘积 | 1 |
| 1 | 常数1；分式1/√N表示√N的倒数 | 1 |

怎样理解总向量平方展开后，独立各向同性线段的交叉项平均为零，留下 N 个 b²；开平方后得到长度。

算一个例子b=0.5 nm、N=16 时，R_rms=2 nm，L=8 nm，两者之比为 0.25。

使用条件理想独立线段的统计关系；N 与化学 EO 数 n 分开定义，单帧构象可偏离均方根。

公式中平方根的来源可以直接从向量相加理解。总端到端向量是所有步向量之和，把它与自身相乘，会出现每一步自身长度的平方，以及不同步之间的交叉项。在独立、各向同性取向的理想条件下，交叉项的正负贡献在充分平均后抵消；留下的 N 项各为 b²，所以距离平方的平均为 Nb²，再开平方得到 b√N。“充分平均”在这里承担了关键作用，一条恰好伸直的构象当然可以达到 Nb。这个推理解释的是构象群的统计尺寸，直观图中因此要画出多种转向方式，才能看清平均如何进入问题。

真实链还要为自己的原子留出空间。Flory 在 1949 年讨论真实聚合物链时，把远隔链段之间的空间排斥纳入尺寸问题，推动了从随机线段到溶液中真实链的理解。后来对链构象、溶液性质与实验尺寸的联系，使高分子统计能够同时讨论局部化学结构和大尺度形状。这个历史转变带来的具体问题是：远处的链段靠近时会怎样，溶剂又如何改变这些接触的代价？在分子模拟中，原子间排斥、吸引和水的重新排列共同回答这些问题；理想随机链则提供一个结构清楚的比较起点。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s3)

图 2 · 独立随机线段提供平方根参照；真实链的非局部接触及周围溶剂改变构象权重。

把理想模型用于 PEG 时还需要看清尺度。式中的 N 是能够近似独立取向的统计线段数，b 是这类线段的长度；它们不会自动等于 EO 数和某一根化学键的长度。PEG 的键角、二面角和相邻片段的关联决定了多长一段链才适合被合并成一个统计线段。本讲把实际尺寸除以 √n，是为了检查它相对于化学链长平方根的增长方式。当局部结构与有效线段比例在一系列足够长的链中保持近似稳定，这种参照才更接近统计链的尺度描述。8 到 32 个 EO 的比较仍然保留明显端基与有限链长特征，我们会把实际点逐一展示出来。

下面的交互把尺寸写成一条简单幂律，固定 n=8 时的尺寸为 0.5 nm，只改变增长指数和要比较的 n。指数为 0.5 时，除以 √n 后得到水平线；指数高于 0.5，归一化曲线就上升。把显示切换成除以 n，还可以看出“空间尺寸增长”与“每个重复单元贡献同样直线长度”是两个不同问题。交互中的曲线按解析表达式计算，实际 PEG 轨迹的测量值随后单独展示。试着先预测链长从 8 增至 32 时尺寸应增加几倍，再拖动滑块检查自己的判断。

幂律参照与归一化式 3

![幂律参照与归一化](https://ml-biomat.com/static/agent-math/c1eaf8c2ee492e14fd83637b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| D(n), D₀ | n 对应的尺寸及参照尺寸，交互中 D₀=0.5 nm | nm |
| n, n₀ | 化学重复数与参照重复数，n₀=8 | 1 |
| ν | 所选增长指数 | 1 |
| α | 归一化指数；0 为原尺寸，0.5 为除以 √n，1 为除以 n | 1 |
| Q_α(n) | 归一化后的尺寸量 | nm |
| ( ), /, ^, =, × | 括号先算、除法、上标幂运算、相等和相乘 | 1 |

怎样理解先用无量纲链长比确定尺寸放大倍数，再除以选定的链长幂，显示相对于该参照的剩余变化。

算一个例子n=32、ν=0.5：D=0.5×√(32/8)=1 nm；Q₀.₅=1/√32≈0.1768 nm，与 n=8 时相同。

使用条件交互使用指定指数的解析参照。实际轨迹的尺寸与局部斜率由独立分析计算。

解析幂律：D(8)=0.5 nm；改变指数，再比较归一化。

[Figure: 解析尺寸与链长关系](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s3)

解析幂律比较。圆点跟随所选 n；所有曲线在 n=8 的原始尺寸均为 0.5 nm。

## 六条轨迹怎样放在同一把尺子下

模型准备从三个明确的化学序列出发。使用固定版本的 Polyply 参数库生成 PEG 拓扑与初始坐标，随后在 6 nm 的立方盒中居中并加入水。三个最终体系分别包含 7012、6996 和 6970 个水分子，差别来自聚合物排开的空间以及建盒时的重叠处理。水采用 SPC/E；聚合物采用库中 OPLS-AA/LigParGen 参数，保留原库的原子电荷、成键项和非键相互作用。用同一参数家族比较链长，有助于把差别追溯到化学组成和构象；若改用另一组聚合物—水参数，则应重新比较局部构象和水化的响应。

每种长度先做能量最小化，让最初较拥挤的接触得到调整；随后两条运动历史分别经历 100 ps 的定体积温度准备、200 ps 的恒压准备，再各记录 2 ns 恒压生产轨迹。目标温度为 300 K，目标压力为 1 bar，时间步为 2 fs。含氢共价键采用约束，水在动力学阶段保持模型规定的几何；最小化阶段使用可柔性处理水的设置。约束的作用是把最快的一部分键振动从积分问题中分离出来，2 fs 的步长仍需与这一选择配套。温度调节使用速度重标定的随机方案，压力采用各向同性 C-rescale，三个方向的盒长一起按相同比例变化。

### 建立三个化学长度的输入目录

```
"""Prepare three fresh PEG model directories from the pinned Polyply library.

python prepare_study.py --forcefield oplsaa.ff --out length-runs
Install the pinned Polyply version using the preparation page before running
the generated construction commands. GROMACS 2026.4 supplies oplsaa.ff.
"""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

POLYMER = '''#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
[ system ]
Hydroxyl-ended PEG
[ molecules ]
PEG 1
'''
SOLUTION = '''#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
Hydroxyl-ended PEG in SPC/E water
[ molecules ]
PEG 1
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--forcefield', type=Path, default=Path('oplsaa.ff'))
    parser.add_argument('--out', type=Path, default=Path('length-runs'))
    args = parser.parse_args()
    if not (args.forcefield/'forcefield.itp').is_file() or not (args.forcefield/'spce.itp').is_file():
        raise ValueError('Supply the complete GROMACS oplsaa.ff directory')
    targets=[args.out/f'PEG{n}' for n in (8,16,32)]
    if any(p.exists() for p in targets):
        raise ValueError('Choose a fresh output directory for the three models')
    here=Path(__file__).resolve().parent
    for n,target in zip((8,16,32),targets):
        target.mkdir(parents=True)
        shutil.copytree(args.forcefield,target/'oplsaa.ff')
        for name in ('seeded_polyply.py','run_one.sh'):
            shutil.copyfile(here/name,target/name)
        (target/'polymer.top').write_text(POLYMER,encoding='utf-8',newline='\n')
        (target/'topol.top').write_text(SOLUTION,encoding='utf-8',newline='\n')
        generate=f'''#!/usr/bin/env bash
set -euo pipefail
polyply gen_params -lib oplsaaLigParGen -o PEG.itp -name PEG -seq OHter:1 PEO:{n-1} OHter:1 > topology-generation.log 2>&1
python seeded_polyply.py {20261400+n} gen_coords -p polymer.top -o PEG.gro -name PEG -box 6 6 6 > coordinate-generation.log 2>&1
'''
        (target/'generate.sh').write_text(generate,encoding='utf-8',newline='\n')
        subprocess.run([sys.executable,str(here/'write_parameters.py'),'--n',str(n),'--out',str(target)],check=True)
        print(f'Prepared PEG{n}: {7*n+3} atoms, {n+1} oxygen sites')


if __name__=='__main__':main()
```

复制共同力场，写入三个序列及起始种子，再调用参数生成器。

### 写入完整模拟参数

```
"""Write the complete PEG length-study simulation settings for two velocity histories.
Run: python write_parameters.py --n 8|16|32 [--out INPUT_DIRECTORY]
"""
from pathlib import Path
import argparse

EM = """integrator = steep
define = -DFLEXIBLE
constraints = none
emtol = 500
emstep = 0.001
nsteps = 50000
nstenergy = 20
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
"""

NVT = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20263161
ld-seed = 20264161
"""

NPT = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
nsteps = 100000
ld-seed = 20265161
"""

MD = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
nstenergy = 1000
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
nsteps = 1000000
ld-seed = 20266161
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("."))
    parser.add_argument("--n", type=int, choices=[8, 16, 32], required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    for replica in [1, 2]:
        replacements = {"20263161": str(20263000+10*args.n+replica),
                        "20264161": str(20264000+10*args.n+replica),
                        "20265161": str(20265000+10*args.n+replica),
                        "20266161": str(20266000+10*args.n+replica)}
        for stage, template in [("nvt", NVT), ("npt", NPT), ("md", MD)]:
            content = template
            for old, new in replacements.items():
                content = content.replace(old, new)
            (args.out/f"{stage}-{replica}.mdp").write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
```

最小化及两条历史各阶段的参数完整保留；n 决定各自随机种子。

### 固定坐标构建的随机状态

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

为 Polyply 使用的 Python 与 NumPy 随机数设置同一给定种子。

记录坐标之后，第一件事是把跨过周期边界的链重新拼成连续分子。可以把周期盒想成一张左右、上下、前后边缘彼此相接的地图：原子坐标从一侧跳到另一侧时，化学键仍然连接着。分析程序从一个末端氧出发，沿共价键逐个访问相邻原子，把每条键放回最短周期位移对应的位置，直到整条链恢复连续。接着检查所有键，而不只检查遍历时碰到的那部分键。这样，后面的回转半径和端到端距离才描述同一条完整分子。长度单位也在此统一：MDAnalysis 读入的坐标以 Å 表示，除以 10 后才以 nm 作图。

连续分子还可以用来检查它离自己的周期映像有多远。程序把整条链平移到周围 26 个相邻盒位置，计算本体原子到这些映像原子的最近距离。六条轨迹中最小值约为 2.082 nm，出现在 PEG32 的第一条历史；它大于本例 1.0 nm 的短程非键截断。这个结果说明，保存帧中的链与自身映像保持了明确的短程几何间隔。长程静电仍通过周期体系的 PME 处理，尺寸涨落和溶剂响应也可能随盒大小变化；研究盒尺寸效应时，应在更大的水盒中保持同一链模型，比较相同定义的尺寸与相关时间。

实际生产轨迹每隔 5 ps 保存一帧，每条从 0 到 2000 ps 共 401 帧。主比较选取 1000 到 2000 ps，包含两端，共 201 帧；同时把完整时间曲线画出来，让前后变化保持可见。选择后一段是一个明确的测量窗口，不能替代对慢变化的观察。相邻帧来自连续运动，彼此有时间关联。稍后使用的 500 ps 分块，是为了看到平均值如何随时间段改变，而不是把每一帧都当成一次全新的独立实验。

## 三种长度、两把空间尺子

用眼睛看分子时，最容易注意到两个末端是否远离；用回转半径测量时，则要关心整条链的质量怎样分布。质心相当于把原子看成一组带质量的小物体后找到的平衡位置，较重原子对它的贡献更大。回转半径先计算每个原子到质心的距离平方，乘以该原子的质量，再除以总质量并开平方。端到端距离更直接：取两个末端氧之间的空间直线距离。前者综合全链，后者聚焦末端，这使两者对局部折返和整体弯曲的响应不同。

质量分布与两个末端式 4

![质量分布与两个末端](https://ml-biomat.com/static/agent-math/fce8efd11f65b25d8badbf12.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N_{a}, i | 链原子总数及逐原子编号 | 1 |
| mᵢ, M | 原子质量及整条链总质量 | u |
| rᵢ, r_{cm} | 完整链中原子的位置向量及质心位置 | nm |
| r_{A}, r_{B} | 两个末端氧的位置向量；A、B 标识末端 | nm |
| R_{g}, R_{e} | 质量加权回转半径及端到端距离 | nm |
| Σ, =, /, −, √ | 求和、相等、除法、向量相减和非负平方根 | 1 |
| \|rᵢ−r_{cm}\|² | 向量长度的平方，即三坐标分量平方之和 | nm² |
| mᵢ\|rᵢ−r_{cm}\|² | 质量与距离平方相乘 | u nm² |
| \|r_{B}−r_{A}\| | 两末端位移向量的长度 | nm |
| 1, 2 | 原子编号从 1 开始；上标 2 表示平方 | 1 |

怎样理解质心以质量作权重；距离平方避免正负方向抵消。先恢复周期边界下的完整分子，再测量内部几何。

算一个例子两个等质量点分别位于 x=−1 和 +1 nm，其他坐标为零：质心为零，R_g=1 nm，若它们为端点则 R_e=2 nm。

使用条件R_g 包含所有 PEG 原子，质量取自各自 TPR；R_e 使用同一完整分子的两端氧。

想象一条链卷成弯曲的马蹄形：两个末端可以靠得很近，链中间的大部分原子仍分布在较大的范围里。这时端到端距离显著变小，回转半径却可能保持较大。另一个容易混淆的量是轮廓长度，它沿主链逐根共价键累加，在本例的两端氧之间一共经过 3n 根主链键。实际记录的平均轮廓长度随 PEG8、PEG16、PEG32 约为 3.50、7.01 和 14.02 nm，接近随 n 成比例；它们的空间尺寸则小得多。这说明增长的化学路径大量用于改变方向，而不是全部投影到一条直线上。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s5)

图 3 · 六条轨迹各取 1–2 ns 内最接近回转半径中位数的一帧，按共价键恢复完整链，以统一比例投影；尺寸统计使用完整三维坐标。

图中的构象取自各条轨迹在 1–2 ns 窗口内接近回转半径中位数的一帧，按同一长度比例展示。原子间相对位置来自完整分子的实际坐标，整体转动只是为了看清形状，水暂时隐藏。中位数选择回答的是“这一段轨迹中尺寸居中的一个形状长什么样”，它仍然只是构象群中的一员。一个平均回转半径通常对应许多不同弯曲方式，所以接下来必须读完整时间曲线，尤其要观察大幅起伏是否持续很久，以及两条历史在哪些时间段接近或分开。

### 六条轨迹的尺寸变化

阴影表示 1–2 ns 主统计窗口；每条完整记录 401 帧。

化学EO聚合度8、16、32的双羟基PEG，固定Polyply OPLS-AA/LigParGen版本、SPC/E水、300 K、1 bar。每种链长各两条2 ns速度与热浴历史，同一链长共用最小化起点；不同链长分别构建。

[下载参考数据与完整输入（ZIP） 178.13 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-peg-lengths-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s5)

六条实际2 ns轨迹，每条401帧；阴影标出1–2 ns的201帧主分析窗口。质量回转半径和端氧距离均在逐键恢复整链并核查全部键后计算。

PEG8 的两条曲线在后一半多次进入相近的尺寸区间，时间平均回转半径分别约为 0.485 和 0.473 nm。PEG16 对应约 0.783 和 0.757 nm，PEG32 则为 1.288 和 1.154 nm。长链两条历史之间的分离更明显，尤其在 1.0–1.5 ns 附近。这与更长链拥有更多内部形状、整体重排需要一定时间的图景相符。判断这一解释需要继续看更长记录和更多起始形状；当前曲线首先给出了下一轮采样应重点关注的位置，而不是把每条线压缩成一个没有时间背景的数字。

计算时还要区分“距离的平均”与“距离平方平均之后开平方”。例如两帧回转半径分别是 0.4 和 0.6 nm，普通平均为 0.5 nm，均方根则约为 0.510 nm，因为平方运算给较大尺寸更多权重。理论随机链关系通常写成距离平方的平均，因此本讲跨链长主图使用均方根，并在数据表同时保留普通平均、标准差和完整时间序列。对同一条轨迹选用不同统计量不会改变它的坐标，却会改变你正在回答的测量问题。

普通平均与均方根式 5

![普通平均与均方根](https://ml-biomat.com/static/agent-math/cbf32dbc2d5f556c9fb0c55d.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| D_{k} | 第 k 个保存帧的 R_g 或 R_e | nm |
| m, k | 选定窗口帧数及帧编号 | 1 |
| D̄, D_{rms} | 普通平均和均方根 | nm |
| D_{k}² | 单帧尺寸的平方 | nm² |
| Σ, /, √, = | 求和、除法、非负平方根和相等 | 1 |
| 1, 2 | 1/m 表示每帧等权；上标 2 表示与自身相乘 | 1 |

怎样理解先平方再平均会给大尺寸更多权重；最后开平方让结果回到长度单位。

算一个例子两帧 D=0.4、0.6 nm：普通平均 0.5 nm，均方根 √[(0.16+0.36)/2]≈0.510 nm。

使用条件每条轨迹主窗口 1000≤t≤2000 ps，共 201 帧；等时间间隔帧使用等权，时间关联影响统计精度。

## 增长趋势怎样读，斜率又怎样算

先逐条历史计算均方根，再把两条历史等权汇总，可得到 PEG8、PEG16、PEG32 的回转半径均方根约为 0.481、0.773 和 1.227 nm。这里的汇总是先平均距离平方，再开平方；由于两条历史选取的帧数相同，也等于把两个窗口的平方值合在一起求平均。主图仍把两条历史分别画成圆点和方点，以保留它们的差别。随 n 增大，链的空间尺寸清楚增加；接下来要问的是，这种增长相对于一个明确参照是快还是慢。

### 原始尺寸与链长归一化

每个点对应一条历史；虚线为以 PEG8 等权均方根为锚的 √n 参照。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s6)

原始尺寸与按化学EO数归一化的尺寸，每点对应一条历史。虚线以PEG8的等权均方根为锚按√n延伸，用作参考关系。

图中的虚线以 PEG8 的汇总值为起点，随后按 √n 增长。它让“增长快慢”有了可读的标尺：从 8 到 32，n 增加四倍，平方根参照只把尺寸增加两倍，从约 0.481 增到 0.962 nm。PEG32 两条历史的实际回转半径均方根约为 1.290 和 1.159 nm，都位于这条参照之上。相应地，除以 √n 后，PEG8 的两点约为 0.172 和 0.168 nm，PEG32 约为 0.228 和 0.205 nm。归一化图把主要的链长增长先拿来做比较，再显示剩余的变化，便于观察局部构象、端基和采样共同留下的影响。

端到端距离给出了更有层次的结果。三种长度等权汇总后的均方根约为 1.085、2.014 和 2.810 nm，但 PEG32 两条历史分别约为 3.333 和 2.163 nm，相差明显。后一条的端到端尺寸除以 √n 后，恰好接近 PEG8 的数值；同一条长链的回转半径归一化值仍较高。把两把尺子一起读，就会发现“链整体较大”与“末端相隔较远”之间并没有一一对应关系。对连接臂能跨越多大间距的问题，端点距离及其分布尤其有用；对链的总体空间展开程度，回转半径更直接。

相邻两种链长的局部增长斜率式 6

![相邻两种链长的局部增长斜率](https://ml-biomat.com/static/agent-math/f970df85819488f454b4ee20.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n₁, n₂ | 两个化学重复数，n₂>n₁>0 | 1 |
| D(n₁), D(n₂) | 相同定义和采样窗口下的尺寸统计量 | nm |
| ν₁₂ | 这两个链长之间的对数增长比 | 1 |
| ln, /, [ ], = | 自然对数、除法、分组和相等；对数的输入均为无量纲比值 | 1 |
| 1, 2 | 标识两个比较条件的下标 | 1 |

怎样理解若尺寸正好按 n 的某个幂变化，对两个尺寸比取对数便能解出该幂；用于实测点时得到对应区间的局部斜率。

算一个例子回转半径均方根 D(8)=0.481104 nm、D(16)=0.772702 nm，ν₁₂≈ln(0.772702/0.481104)/ln2≈0.684。

使用条件本例是有限链长、有限时间窗口的描述；渐近尺度关系需要更长链范围与稳定采样。

如果希望把相邻两种长度的变化写成一个数字，可以计算对数比值。回转半径均方根从 PEG8 到 PEG16 给出约 0.684，从 PEG16 到 PEG32 给出约 0.667；端到端距离的两个对应值却约为 0.893 和 0.480。它们是这两个有限链长区间、这套力场和这段采样窗口的局部增长斜率。长链理论中的渐近指数还要求进入适当的长度范围，并对采样、有限尺寸和端基效应有稳定认识。当前最值得保留的事实，是两种测量量对有限长度比较给出了不同敏感性，这能直接指导后续要增加什么数据。

继续做研究时，可以在已有长度之间补几个 n，并把最长链的记录延长，观察相邻区间斜率是否稳定。同时保留每条历史，不要只画合并后的三个点。若较长记录让 PEG32 的两个端点距离分布逐渐接近，原先的分离便能与慢构象采样联系起来；若两者仍明显不同，就需要更多起始构象与时间尺度检查。实验比较还要对齐测量定义：散射、扩散和末端标记距离各自对分子形状的加权方式不同，模拟中选用的原子质量加权回转半径，需要与目标实验的对比方式一起说明。

## 水变多了，还是每个位置更容易接近水

一条 PEG 链周围的水分子不断更换。要把这种流动的近邻关系变成可比较的数据，先给出一个几何规则：当水氧与任一聚合物氧的周期最短距离小于 0.35 nm，就把该水分子记为近邻水。这是一个氧—氧距离定义；它容易计算，也方便在不同链长之间保持一致。若要进一步统计氢键，还应补充供体、受体和角度条件。若要讨论水在某处停留多久，则需要追踪同一水分子的身份随时间怎样变化。清楚区分这些问题，才能让一个计数承担合适的物理含义。

同一个水分子有时会同时靠近两个或更多聚合物氧。若关心周围共有多少个不同水分子，它只能计一次；若关心所有氧—水近邻接触共有多少对，每一个满足阈值的氧—水组合都应该计入。可以把聚合物氧想成几盏照向周围的灯，水分子是被照到的点。几束光的并集给出不同水分子的数量，而逐束统计后相加会把重叠区域中的点重复计算。两种计数都合理，它们分别回答“有多少个水”与“有多少次位点接触”，所以分析程序同时保存这两列。

不同水分子与接触对式 7

![不同水分子与接触对](https://ml-biomat.com/static/agent-math/43eca583cd3b469fd2c9509a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N_{w}, w | 水分子总数及水编号 | 1 |
| N_{O}, j | 聚合物氧数及氧编号，N_O=n+1 | 1 |
| d_{wj} | 水 w 的氧到聚合物氧 j 的周期最短距离 | nm |
| r_{c} | 近邻截断，主图采用 0.35 nm | nm |
| U, C | 不同近邻水数及氧—水接触对数 | 1 |
| u, c | 上述两项分别除以氧位点数后的值 | 每氧位点 |
| Σ, min, 1[ ], < | 求和、取最小值、条件成立记 1 否则记 0、严格小于 | 1 |
| /, =, 1 | 除法、相等以及编号起点或指示函数的计数单位 | 1 |

怎样理解不同水计数对每个水先问是否至少接近一个氧；接触对计数则逐个氧—水组合累加。除以氧数后可以比较不同链长。

算一个例子2 个氧附近共有 3 个不同水，其中 1 个同时靠近两个氧，则 U=3、C=4、u=1.5、c=2。

使用条件距离使用每帧周期盒；该计数按氧—氧几何近邻定义，氢键分析另需角度与供受体规则。

### 总水化计数与每氧位点计数

1–2 ns 平均；氧—氧阈值 0.35 nm。不同水并集与接触对分别计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s7)

1–2 ns的水化计数：聚合物氧—水氧阈值0.35 nm，分别计算不同水分子的并集与接触对，再与每氧位点计数对照。

在 1–2 ns 的窗口内，PEG8 两条历史的不同近邻水平均数约为 11.80 和 11.62，PEG16 约为 20.22 和 19.44，PEG32 约为 33.79 和 33.29。链越长，拥有更多氧位点，周围不同水分子的总数随之增加。可是把它除以各链的氧数后，PEG8 得到约 1.311 和 1.291 个水/氧，PEG32 则约为 1.024 和 1.009 个水/氧。总量上升而每位点分配量下降并不矛盾：长链提供了更多位置，但不同位置的近邻区域可能重叠，末端与内部位点的比例也同时改变。

接触对数除以氧数后，PEG8 约为 2.357 和 2.346，PEG32 约为 2.176 和 2.162。这一量允许同一水为多个位点贡献，因此比“不同近邻水数/氧数”更接近逐位点平均近邻计数。二者之间的差距还提示了共享近邻的重要性。解释这些变化时，可以进一步把链的氧按末端、内部以及离端点的化学距离分组，再观察链卷曲程度是否与近邻重叠一起变化。这样从总量到位点再到构象的推进，把一个抽象的“水化增强或减弱”拆成了能够逐步测量的局部过程。

距离阈值同样属于测量定义。把 0.35 nm 改成 0.30 nm，会更多保留距离较近的水；改成 0.40 nm，则把外侧一圈近邻纳入。完整程序对这三个阈值都保存计数，便于检查趋势对边界选择的敏感性。一个水分子在阈值附近轻微运动就可能使瞬时计数改变，因此稳定的解释应结合时间平均和近邻距离分布。这里的几何计数可以帮助观察链—水接触，但溶解自由能还涉及能量、熵和参照状态；要回答溶解热力学问题，应另设相应的自由能计算。

## 把比较写成可重算的研究流程

研究的最后一步，是把化学定义、运行条件与分析选择串成可以重复执行的流程。下面的单体系脚本完成建盒、加水、最小化和两条历史的准备与生产；总脚本依次为三个链长调用它，再生成两种语言的图。运行前把准备页中同版本的 GROMACS、Polyply 和分析环境准备好，并把完整 oplsaa.ff 目录放在例题旁。生成器要求新的输出目录，已有结果可以保留用于对照。读者也可以直接使用本页附带的参考轨迹，先运行分析程序，再根据自己的计算资源重跑分子动力学阶段。

### 完成一种长度的原生模拟

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" editconf -f PEG.gro -o boxed.gro -box 6 6 6 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
for rep in 1 2; do
  mkdir "replica-$rep"
  cp em.gro topol.top PEG.itp "replica-$rep/"
  cp -r oplsaa.ff "replica-$rep/"
  for stage in nvt npt md; do cp "$stage-$rep.mdp" "replica-$rep/$stage.mdp"; done
  (
    cd "replica-$rep"
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
  )
done
```

同一最小化构型分别生成两条运动历史；温度、压力与能量记录同时保留。

### 运行三个长度并生成双语图

```
#!/usr/bin/env bash
set -euo pipefail
python prepare_study.py --forcefield oplsaa.ff --out length-runs
for n in 8 16 32; do
  (
    cd "length-runs/PEG$n"
    bash generate.sh
    bash run_one.sh
  )
done
python analyze_lengths.py --peg8 length-runs/PEG8 --peg16 length-runs/PEG16 --peg32 length-runs/PEG32 --out length-study/en --language en
python analyze_lengths.py --peg8 length-runs/PEG8 --peg16 length-runs/PEG16 --peg32 length-runs/PEG32 --out length-study/zh --language zh
```

在例题目录启动；新体系写入 length-runs，分析输出按语言分别保存。

分析程序先读取各条轨迹自己的 TPR，以取得真实原子质量、共价连接和水分子数量，然后才读取坐标。对每一帧，它先重建整条 PEG，检查所有键的几何一致性，再计算尺寸、轮廓长度、近邻水和周期映像距离。输出的逐帧 CSV 可以在表格软件中直接打开；汇总 JSON 保留主窗口统计、归一化量和分块结果，SVG 图保留清楚的坐标轴与单位。这样的输出组合使一个图上的数值可以回到对应时间窗口，再回到相应构象，而不必依靠人工抄录重新建立联系。

### 从原生拓扑与轨迹生成完整比较

```
"""Compare hydroxyl-ended PEG8, PEG16 and PEG32 under common conditions.

python analyze_lengths.py --peg8 PEG8 --peg16 PEG16 --peg32 PEG32 --out length-study --language en
Each PEG directory contains replica-1 and replica-2, each with md.tpr and md.xtc.
Dependencies: MDAnalysis, NumPy, SciPy and Matplotlib.
"""
from pathlib import Path
from itertools import product
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors, distance_array
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def bond_plan(group, terminal):
    local = {int(index): k for k, index in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for edge, (a, b) in enumerate(edges):
        graph[a].append((b, edge, 1)); graph[b].append((a, edge, -1))
    queue, seen, plan = [int(terminal[0])], {int(terminal[0])}, []
    parents = {int(terminal[0]): None}
    for a in queue:
        for b, edge, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, edge, sign));parents[b] = a
    if len(seen) != len(group):
        raise ValueError('Polymer bond graph is not connected')
    route = [int(terminal[1])]
    while parents[route[-1]] is not None:
        route.append(parents[route[-1]])
    return edges, plan, np.array(route[::-1])


def reconstruct(raw, box, edges, plan, anchor):
    vectors = minimize_vectors(raw[edges[:,1]]-raw[edges[:,0]], box)
    whole = np.empty_like(raw, dtype=float);whole[anchor] = raw[anchor]
    for parent, child, edge, sign in plan:
        whole[child] = whole[parent]+sign*vectors[edge]
    actual = whole[edges[:,1]]-whole[edges[:,0]]
    if np.max(np.linalg.norm(actual-vectors, axis=1)) > .005:
        raise ValueError('Reconstructed bond cycle is inconsistent')
    longest = float(np.linalg.norm(actual, axis=1).max()/10)
    if longest > .25:
        raise ValueError('Reconstructed covalent bond exceeds 0.25 nm')
    return whole/10, longest


def stats(v):
    return {'mean':float(np.mean(v)), 'sample_sd':float(np.std(v,ddof=1)),
            'rms':float(np.sqrt(np.mean(v*v))), 'minimum':float(np.min(v)), 'maximum':float(np.max(v))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in (8,16,32):parser.add_argument(f'--peg{n}',type=Path,default=Path(f'PEG{n}'))
    parser.add_argument('--out',type=Path,default=Path('length-study'))
    parser.add_argument('--language',choices=['en','zh'],default='en')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    arrays={};summaries=[];snapshots=[];blocks=[]
    translations=np.array([v for v in product((-1,0,1),repeat=3) if v!=(0,0,0)])
    expected_waters={8:7012,16:6996,32:6970}
    for n in (8,16,32):
        for rep in (1,2):
            folder=getattr(args,f'peg{n}')/f'replica-{rep}'
            u=mda.Universe(str(folder/'md.tpr'),str(folder/'md.xtc'))
            polymer=u.select_atoms('resname OHter PEO');oxygen=polymer.select_atoms('name O*')
            water=u.select_atoms('resname SOL and name OW');terminal=np.flatnonzero(polymer.names=='OA1')
            counts={el:int(sum(str(name).startswith(el) for name in polymer.names))for el in ('C','H','O')}
            if counts!={'C':2*n,'H':4*n+2,'O':n+1} or len(polymer)!=7*n+3 or len(terminal)!=2 or len(water)!=expected_waters[n]:
                raise ValueError(f'PEG{n} composition differs from the specified model')
            if abs(sum(polymer.charges))>1e-5:raise ValueError('Polymer charge is not neutral')
            edges,plan,route=bond_plan(polymer,terminal)
            assert len(route)==3*n+1 and len(edges)==len(polymer)-1
            masses=polymer.masses;totalmass=float(masses.sum());rows=[];coordinates=[];maxbond=0.
            for frame in u.trajectory:
                whole,bondmax=reconstruct(polymer.positions.astype(float),frame.dimensions,edges,plan,int(terminal[0]))
                maxbond=max(maxbond,bondmax);center=np.average(whole,axis=0,weights=masses);pos=whole-center
                rg=float(np.sqrt(np.average(np.sum(pos*pos,axis=1),weights=masses)))
                re=float(np.linalg.norm(whole[terminal[1]]-whole[terminal[0]]))
                contour=float(np.linalg.norm(np.diff(whole[route],axis=0),axis=1).sum())
                assert re<=contour+1e-8
                distances=distance_array(oxygen.positions,water.positions,box=frame.dimensions)/10
                hydration=[]
                for cutoff in (.30,.35,.40):
                    near=distances<cutoff;hydration += [int(np.any(near,axis=0).sum()),int(near.sum())]
                # Explicit translated copies, with no minimum-image operation on their separation.
                if not np.allclose(frame.dimensions[3:],90,atol=.001):raise ValueError('Image check expects the orthogonal simulation cells')
                boxnm=frame.dimensions[:3]/10
                if np.any(np.ptp(pos,axis=0)>=boxnm):raise ValueError('Extend the periodic-image search for this chain span')
                translated=(pos[None,:,:]+translations[:,None,:]*boxnm).reshape(-1,3)
                image_min=float(cKDTree(pos).query(translated,k=1)[0].min())
                volume=float(np.prod(boxnm))
                rows.append([float(frame.time),rg,re,contour,*hydration,image_min,volume]);coordinates.append(pos)
            values=np.array(rows);arrays[(n,rep)]=values
            assert values.shape==(401,12) and np.allclose(values[:,0],np.arange(401)*5)
            late=values[:,0]>=1000
            row={'EO_degree':n,'replica':rep,'polymer_atoms':len(polymer),'oxygen_sites':len(oxygen),
                 'water_molecules':len(water),'mass_u':totalmass,'backbone_bonds':len(route)-1,
                 'frames':401,'main_window_frames':int(late.sum()),'maximum_bond_nm':maxbond,
                 'minimum_image_distance_nm':float(values[:,10].min()),
                 'main_window':{name:stats(values[late,col])for name,col in [('Rg_nm',1),('Re_nm',2),('contour_nm',3),('unique_waters',6),('contact_pairs',7),('volume_nm3',11)]},
                 'cutoff_sensitivity':{str(c):{'unique_mean':float(values[late,4+2*j].mean()),'pairs_mean':float(values[late,5+2*j].mean())}for j,c in enumerate((.30,.35,.40))}}
            row['RMS_Rg_over_sqrt_n_nm']=row['main_window']['Rg_nm']['rms']/np.sqrt(n)
            row['RMS_Re_over_sqrt_n_nm']=row['main_window']['Re_nm']['rms']/np.sqrt(n)
            row['unique_per_oxygen']=row['main_window']['unique_waters']['mean']/(n+1)
            row['pairs_per_oxygen']=row['main_window']['contact_pairs']['mean']/(n+1)
            row['unique_per_EO']=row['main_window']['unique_waters']['mean']/n
            summaries.append(row)
            for q in range(4):
                mask=(values[:,0]>q*500)&(values[:,0]<=(q+1)*500);assert mask.sum()==100
                blocks.append({'EO_degree':n,'replica':rep,'start_ps':q*500,'end_ps':(q+1)*500,
                               'frames':100,'Rg_mean_nm':float(values[mask,1].mean()),'Re_mean_nm':float(values[mask,2].mean()),
                               'unique_mean':float(values[mask,6].mean())})
            pick=np.flatnonzero(late)[np.argmin(abs(values[late,1]-np.median(values[late,1])))]
            snapshots.append({'EO_degree':n,'replica':rep,'time_ps':values[pick,0],'Rg_nm':values[pick,1],
                              'Re_nm':values[pick,2],'coordinates_nm':coordinates[pick].tolist(),
                              'names':polymer.names.tolist(),'masses':masses.tolist(),'bonds':edges.tolist(),'terminal_indices':terminal.tolist()})
            with (args.out/f'PEG{n}-replica-{rep}.csv').open('w',newline='',encoding='utf-8')as stream:
                writer=csv.writer(stream);writer.writerow(['time_ps','Rg_nm','Re_nm','contour_nm','unique_030','pairs_030','unique_035','pairs_035','unique_040','pairs_040','image_min_nm','volume_nm3']);writer.writerows(values)
    pooled={}
    for n in (8,16,32):
        v=np.concatenate([arrays[(n,r)][arrays[(n,r)][:,0]>=1000]for r in (1,2)])
        pooled[n]={'rms_Rg_nm':float(np.sqrt(np.mean(v[:,1]**2))),'rms_Re_nm':float(np.sqrt(np.mean(v[:,2]**2)))}
    slopes=[]
    for lo,hi in [(8,16),(16,32)]:
        slopes.append({'n_low':lo,'n_high':hi,'Rg_log_ratio':float(np.log(pooled[hi]['rms_Rg_nm']/pooled[lo]['rms_Rg_nm'])/np.log(hi/lo)),
                       'Re_log_ratio':float(np.log(pooled[hi]['rms_Re_nm']/pooled[lo]['rms_Re_nm'])/np.log(hi/lo))})
    summary={'model':'Hydroxyl-ended PEG; pinned Polyply oplsaaLigParGen; SPC/E; 300K/1bar',
             'main_window_ps':[1000,2000],'time_block_definition':'(0,500],(500,1000],(1000,1500],(1500,2000]ps,100frames each',
             'replicate_design':'Two velocity and thermostat histories share one minimized geometry per length; different lengths are separate molecular models',
             'image_check':'26 nearest nonzero orthogonal translations of reconstructed full chain, separate from periodic PME effects',
             'records':summaries,'pooled_equal_frame_RMS':pooled,'adjacent_length_log_ratios':slopes,'chronological_blocks':blocks}
    (args.out/'length_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (args.out/'length_snapshots.json').write_text(json.dumps(snapshots),encoding='utf-8')
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={f.name for f in font_manager.fontManager.ttflist};fonts=['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans']
    plt.rcParams.update({'font.family':[f for f in fonts if f in available]if zh else['DejaVu Sans'],
                         'font.size':14,'svg.fonttype':'path','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,
                         'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    colors=['#167d84','#c16b3d'];markers=['o','s']
    def save(fig,name):
        fig.savefig(args.out/f'{name}-{args.language}.svg');fig.savefig(args.out/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(3,1,figsize=(12,9.6),sharex=True,constrained_layout=True)
    for n,ax in zip((8,16,32),axes):
        for r in (1,2):
            v=arrays[(n,r)];ax.plot(v[:,0]/1000,v[:,1],color=colors[r-1],lw=1.2,label=tr(f'轨迹{r}',f'History {r}'))
        ax.axvspan(1,2,color='#e9d9ba',alpha=.35);ax.set(ylabel=f'PEG{n}: Rg / nm');ax.grid(alpha=.15)
    axes[0].legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    axes[-1].set_xlabel(tr('生产阶段时间 / ns','Production time / ns'));save(fig,'length-conformations')
    fig,axes=plt.subplots(2,2,figsize=(13,9),constrained_layout=True)
    ns=np.array([8,16,32]);grid=np.linspace(8,32,100)
    for j,(name,label)in enumerate([('Rg_nm','Rg'),('Re_nm','Re')]):
        for rep in (1,2):
            vals=[r['main_window'][name]['rms']for r in summaries if r['replica']==rep]
            axes[0,j].scatter(ns,vals,c=colors[rep-1],marker=markers[rep-1],s=65,label=tr(f'轨迹{rep}',f'History {rep}'))
            axes[1,j].scatter(ns,np.array(vals)/np.sqrt(ns),c=colors[rep-1],marker=markers[rep-1],s=65)
        anchor=pooled[8]['rms_'+label+'_nm']
        axes[0,j].plot(grid,anchor*np.sqrt(grid/8),c='#647b80',ls='--',label=tr('以PEG8为锚的√n参考','√n guide anchored at PEG8'))
        axes[0,j].set_ylabel(tr(f'{label} 均方根 / nm',f'RMS {label} / nm'))
        axes[1,j].set_ylabel(tr(f'{label} 均方根 / √n / nm',f'RMS {label} / √n / nm'))
        for ax in axes[:,j]:ax.set(xticks=ns,xlabel=tr('化学EO重复数 n','Chemical EO repeat count n'));ax.grid(alpha=.15)
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False,fontsize=12)
    save(fig,'length-normalization')
    fig,axes=plt.subplots(1,3,figsize=(15,5.8),constrained_layout=True);fig.get_layout_engine().set(wspace=.12)
    for rep in (1,2):
        rr=[r for r in summaries if r['replica']==rep]
        axes[0].scatter(ns,[r['main_window']['unique_waters']['mean']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65,label=tr(f'轨迹{rep}',f'History {rep}'))
        axes[1].scatter(ns,[r['unique_per_oxygen']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65)
        axes[2].scatter(ns,[r['pairs_per_oxygen']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65)
    for ax,label in zip(axes,[tr('不同近邻水分子数','Unique nearby waters'),tr('不同水分子数 / 氧位点','Unique waters / oxygen site'),tr('接触对数 / 氧位点','Contact pairs / oxygen site')]):
        ax.set(xticks=ns,xlabel=tr('EO重复数 n','EO repeat count n'),ylabel=label);ax.grid(alpha=.15)
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=2,frameon=False)
    fig.supxlabel(tr('1–2 ns均值；聚合物氧—水氧距离 < 0.35 nm','Means over 1–2 ns; polymer O–water O distance < 0.35 nm'),fontsize=12)
    save(fig,'length-hydration')
    fig,axes=plt.subplots(1,3,figsize=(14,5.8),constrained_layout=True);fig.get_layout_engine().set(wspace=.1)
    for n,ax in zip((8,16,32),axes):
        for rep in (1,2):
            rr=[r for r in blocks if r['EO_degree']==n and r['replica']==rep]
            ax.plot([.25,.75,1.25,1.75],[r['Rg_mean_nm']for r in rr],marker=markers[rep-1],c=colors[rep-1],lw=1.5,label=tr(f'轨迹{rep}',f'History {rep}'))
        ax.set(title=f'PEG{n}',xlabel=tr('区间中点 / ns','Block midpoint / ns'),ylabel=tr('块平均 Rg / nm','Block mean Rg / nm'),xticks=[.25,.75,1.25,1.75]);ax.grid(alpha=.15)
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=2,frameon=False)
    fig.supxlabel(tr('四个连续0.5 ns时间块；每块100帧','Four consecutive 0.5 ns blocks; 100 saved frames per block'),fontsize=12)
    save(fig,'length-sampling')
    print(json.dumps({'runs':len(summaries),'pooled_RMS':pooled,'log_ratios':slopes},indent=2))


if __name__=='__main__':main()
```

读取六组 TPR/XTC，逐键恢复分子，计算尺寸、水化、映像距离和时间块，输出 CSV、JSON 与 SVG。

最后再看一遍时间，而不只看链长。把每条 2 ns 轨迹分为四个连续 0.5 ns 区间，每段使用 100 个保存帧，画出回转半径的区间平均。PEG32 第一条历史在第三段明显较大，第二条历史则在第四段上升；两者经历尺寸变化的时间并不一致。PEG8 的两条历史在后两段接近一些。这幅图把前面看到的曲线变化压缩成容易比较的时间块，却保留了时间顺序。四个块共享连续运动历史，块之间也可能相关，因此这里读的是区间敏感性，而不是四次独立重复给出的误差条。

读到两条轨迹时，还应保留“重复”的层次。每个 n 的两条历史从共同的最小化坐标出发，初速度与随机温控历史不同，它们展示了这一准备方案下的运动差异。不同 n 之间并没有逐原子匹配的共同构型，所以图中相同颜色只是表示第几条历史，不是可以跨链长逐点相减的配对实验。若以后要估计某一长度的总体平均和不确定性，可以先增加独立起始形状，再结合轨迹相关时间选择有效分块，并把不同准备之间的变化与单条轨迹内部的波动分别报告。这样的层次有助于把新增计算花在尚未覆盖的变化上。

### 连续时间块的敏感性

四段 (0,500]、(500,1000]、(1000,1500]、(1500,2000] ps，各 100 帧。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/#zh-s8)

四个左开右闭连续500 ps窗口，每窗100帧。保留六条历史各自的时间变化，用于检查尺寸比较对选取时间段的敏感性。

六条轨迹合起来已经给出一组具体结果：按本例参数与 1–2 ns 窗口，较长 PEG 的整体尺寸增大，不同近邻水总数增加，而每氧归一化的两种水化计数下降；PEG32 的端点距离对运动历史更敏感。这些结果之间有可以继续追问的联系。若要解释每氧水化的下降，先分开末端和内部氧；若要判断尺寸增长关系，先增加时间与构象覆盖，并扩展链长范围；若研究表面连接臂，就把末端接枝和表面距离纳入模型。下一步的选择来自已经测到的差异，因此每新增一个体系都对应一个清楚的问题。

把研究结果写给别人看时，可以沿着同样的顺序组织叙述：先交代所比较的三条化学链及共同水环境，再用时间曲线展示它们怎样运动，随后解释尺寸归一化和位点归一化各自改变了什么问题，最后指出哪一项差异最值得继续检验。图中的原子、曲线中的坐标和段落中的数字应来自同一套定义。这也是整门课程最终希望形成的能力：从一个材料问题出发，把分子模型、真实轨迹和有物理意义的测量连接起来，让别人既能读懂你的判断，也能沿着代码和记录重新得到它。

## 延伸阅读与开放资料

- [Polyply Quick Start and oplsaaLigParGen library](https://github.com/marrink-lab/polyply_1.0/tree/38d4d5424e1ef35c86e7cb8532fbd86ecf997221) · Polyply developers; Marrink group · Apache-2.0

  拓扑生成、坐标构建流程以及PEO、OHter原子参数和连接定义。

  以同一固定参数库比较双羟基 PEG8、PEG16、PEG32，各两条原生 GROMACS 历史；增加链长归一化、周期映像和逐位点水化计数。
- [Polyply; a python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald, Riccardo Alessandri, Peter C. Kroon, Luca Monticelli, Paulo C. T. Souza, Siewert J. Marrink · CC BY 4.0

  连接图参数化与坐标构建相分离的方法背景。

  用本例PEG说明两个阶段，图解与分析重新绘制。
- [LigParGen web server: an automatic OPLS-AA parameter generator for organic ligands](https://doi.org/10.1093/nar/gkx312) · Leela S. Dodda, Israel Cabeza de Vaca, Julian Tirado-Rives, William L. Jorgensen · Bibliographic reference; no article text or figures reproduced

  固定参数库所引的LigParGen参数背景。

  保留库内参数，不通过网页重新生成电荷。
- [Paul John Flory — Biographical Memoir](https://www.nasonline.org/wp-content/uploads/2024/06/flory-paul.pdf) · William S. Johnson, Walter H. Stockmayer, Henry Taube · Publicly readable scholarly memoir; no open reuse license assumed

  1949 年真实链空间排斥问题及构象统计的发展。

  简述研究问题，配独立绘制的概念图。
