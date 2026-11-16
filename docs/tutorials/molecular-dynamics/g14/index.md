# 聚合物在水中伸展还是蜷缩

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g14/
Language: zh-CN

从羟基端基 PEG 的连接方式出发，生成原子模型，再用两条真实轨迹读懂链的尺寸、构象分布与水化。

## 一条柔软的链，究竟有多大

把一根耳机线平放在桌上，拿尺子量它两端的距离，很容易得到一个数。换一种摆法，这个数就变了，线本身却没有变长或变短。水中的柔性高分子也有这样的区别：组成分子的原子数、沿骨架的长度，与它在某一刻占据的空间，是三个不同的问题。这个区别关系到实际材料的设计。把亲水链连接到颗粒或膜的表面时，人们关心它伸入水中多远、周围容纳多少水、相邻链会在什么位置碰面；如果只知道化学式而不知道链的空间形状，这些问题还缺少关键的一环。

本讲从聚乙二醇开始，英文简称 PEG。它的主链中反复出现两个碳和一个氧，碳上还连接着氢，常见的双羟基端基链可以写成 HO–(CH₂–CH₂–O)ₙ–H。下标 n 表示这段重复结构出现的次数，括号外的 H 与开头的 HO 一起补足两端。这里的氧并非装饰性的化学符号：它改变了电荷分布，也使水能在链周围形成有方向性的相互作用。与此同时，碳骨架允许许多单键附近的转动，因此一条 PEG 不必保持笔直。溶液中的尺寸正是局部化学、整链连接和周围水共同作用的结果。

我们选取 n 为 16 的一条短链，显式放入 6996 个水分子中，在 300 K 和 1 bar 条件下观察它。显式水的意思是水也有自己的坐标和运动，而不是在链的外面附加一个“潮湿”的标签。体系一共包含 21103 个原子位点，其中 PEG 占 115 个。这样的大小适合练习从建模到分析的完整过程，也能让每个选择保持可读：链只有一种长度、两个相同的羟基端基，体系没有盐、表面或第二条链，因而后面读到的尺寸变化可以先围绕这条链与水的关系展开。

从严格的链长分类看，16 个重复单元是一条较短的低聚链；从教学上看，它把长链材料需要的连接方式、构象变化和统计方法都保留下来了。PEG 与 PEO 常用于指称具有相同重复化学结构的聚醚，名称的使用还与分子量和应用习惯有关。本讲用 PEG 指这条具有明确双羟基端基和确切重复数的分子，参数库中的 PEO 则是一个构建片段的名字。把材料名称、化学重复数和软件片段名分别认清，后面增加链长时就不会无意间改变分子身份。

读完这一讲，你可以生成这条链的拓扑和起始坐标，理解两个独立运行分支为何会给出不同的形状历史，并从真实轨迹中量出回转半径、端到端距离以及附近水分子的数目。重点是把这些量连回具体画面：哪一部分原子移动会改变它，什么情况下两个指标会给出不同印象，统计窗口又会怎样影响平均值。耳机线的比喻帮助我们分清“长度”和“展开程度”，分子模型则进一步告诉我们，水中的链一直在受热运动驱动地改变构象，桌面上静止的绳子只是理解几何关系的起点。

## 从连接方式理解柔性：为什么长分子会蜷曲

今天在屏幕上画出长链很容易，但在二十世纪初，橡胶和纤维素这类材料究竟由巨大分子组成，还是由许多小分子聚集而成，曾是一个实质性的化学问题。施陶丁格在 1920 年提出以普通共价键连接大量小单元的长分子观点，后来通过化学转化及物性研究推进了这一认识。橡胶的氢化尤其触及当时一种聚集解释：如果特殊性质主要来自与双键有关的小单元聚集，改变双键后便应出现相应的显著解离；实验观察推动人们重新考虑材料内部的连接。分清“连接成一条”与“靠近成一团”，让高分子结构成为可以检验的化学模型。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s2)

图 1 · 施陶丁格的长分子观点把共价连接与小单元聚集区分开来。上方是两类结构解释的概念图；下方说明同一连接图可以对应不同空间构象。

施陶丁格在 1953 年的诺贝尔演讲中，把天然的蛋白质、核酸、多糖与合成高分子放进同一个大分子化学视野：它们由熟悉的原子和化学键构成，分子的尺度和连接结构却带来了新的问题。这个认识直接对应我们今天的拓扑文件。两颗原子在图上贴近，可能只是在热运动中相遇；只有拓扑中明确列出的连接，才承担相应的键相互作用。链的一端绕到另一端附近，也不会自动变成环。要研究真正的成环反应，需要另行定义化学连接及相应模型。

连接并不意味着僵直。可以把主链想成一串相连的短杆：杆长有偏好的范围，两根杆之间的夹角也受到约束，而围绕某些单键的转动提供了更多形状变化。化学里的二面角用连续四个原子定义，描述前后两个原子平面之间的相对转角。当一个二面角发生变化，它后面的一段链会随之改变方向；许多局部转动组合起来，就能让整体从伸展变成弯曲。真实 PEG 的不同转角具有不同能量，附近原子也有体积，因此并非每一种画得出来的折线都同样容易出现。

还有一个容易被忽略的原因：弯曲构象的组合方式很多。若要让几十段短杆都大致朝同一个方向排列，可选择的方向组合相对少；允许它们向不同方向转弯，则能组成许多整体尺寸相近但细节不同的形状。这种可实现构象数与熵有关。熵在这里可以先理解成宏观描述背后容纳微观安排的丰富程度。链可以在没有外力把它压缩的情况下经常呈现弯曲形态，因为热运动不断探索可到达的安排。某一个弯曲形状仍可能能量较高，出现多少次要同时看相互作用与可实现的构象组合。

水会进一步改变这种平衡。PEG 的氧与水相互作用，链内部相隔较远的片段也会彼此接近；某次弯曲可能让一部分位点更靠近水，另一次弯曲又可能让局部空间变得拥挤。我们用溶剂质量讨论溶剂如何影响链的统计尺寸，判断时需要同一化学模型下的链长、温度和充分采样等条件。看到一帧伸展的 PEG，可以描述这一帧的形状；讨论水对整类长链的膨胀作用，则要把许多构象和不同长度的结果联系起来。本讲先建立这些测量工具，后面再把链长作为研究变量。

## 把重复单元和端基写对，再生成分子

Polyply 将建模分成两个相互配合的工作：先根据片段及连接规则生成拓扑，再为空间中的原子安排起始坐标。前一步回答“谁与谁连接、相互作用采用什么参数”，后一步回答“这些原子先放在哪里”。这种区分很有用：如果端基选错，再漂亮的三维构象也属于另一种分子；如果拓扑正确而起始坐标中有过近接触，则可以通过合适的构建和松弛步骤改善几何。本例使用固定版本中的 oplsaaLigParGen 参数库，保留库内已有的 PEO、OHter 及它们之间的连接定义。

这里最值得仔细看的命令是 OHter:1 PEO:15 OHter:1。中间一个 PEO 片段包含两个碳、一个氧和四个氢，也就是 C₂H₄O；每个 OHter 片段包含一个碳、一个氧和三个氢，也就是 CH₃O。两端的片段合在一起，比一个 C₂H₄O 重复单元多出 H₂O。因此，15 个内部片段加两端，并不是化学重复数 15 的双羟基 PEG，而是重复数 16 的 C₃₂H₆₆O₁₇。软件中的残基总数为 17，化学重复数为 16，原子总数为 115；这三个数字分别回答不同问题。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s3)

图 2 · OHter 不是一个只有氧和氢的符号端帽，它还包含一个碳。两端片段与15个内部PEO片段组合，得到化学重复数为16的双羟基PEG。

先核对原子数与摩尔质量式 1

![先核对原子数与摩尔质量](https://ml-biomat.com/static/agent-math/8cc9941aa31fd73c5d5fabf6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n | 化学式中的 C₂H₄O 重复数 | 1 |
| Nₐₜₒₘ | 整条双羟基链的原子总数 | 1 |
| 7, 3 | 每重复单元有7原子，两端总补足3原子 | 1 |
| M | 整条分子的摩尔质量 | g mol⁻¹ |
| Mᴇᴏ | C₂H₄O 的摩尔质量，44.053 | g mol⁻¹ |
| Mₑₙd | H₂O 端基总补足量的摩尔质量，18.015 | g mol⁻¹ |
| =, +, × | 等号、相加和相邻符号的相乘；运算本身无单位 | 1 |

怎样理解化学式 C₂ₙH₄ₙ₊₂Oₙ₊₁ 的三类原子数相加得到7n+3；各元素质量按数量相加得到摩尔质量。

算一个例子n=16：原子数为7×16+3=115；M=16×44.053+18.015=722.863 g/mol。两个OHter加15个PEO片段的元素计数正好一致。

使用条件适用于本例两个羟基端基的中性线型PEG；端基改变后重新数元素。

式中的摩尔质量可以从元素计数直接检查。一个 C₂H₄O 单元约为 44.053 g/mol，双端基相对于重复单元的总补足量为 18.015 g/mol，所以 n 为 16 时得到约 722.863 g/mol。摩尔质量说的是一摩尔这种分子的质量；轨迹分析中的原子质量则以 u 表示，用于计算单个分子的质量中心。两者的数值关系来自摩尔与原子质量单位的定义，计算回转半径时只需在分子内部使用一致的原子质量。115 个原子并不意味着 115 个相同重量的珠子，氢、碳和氧的贡献应按各自质量加权。

下面的两个拓扑文件分别服务于无水坐标构建和水溶液模拟。polymer.top 只列一条 PEG，方便 Polyply 生成链的起始构象；topol.top 还引入 SPC/E 水参数，随后由溶剂化步骤填入水分子数量。PEG.itp 会由参数生成命令写出，其中列出原子类型、局部电荷、键、角和二面角。它使用 OPLS-AA 体系的原子参数和库内保留的 LigParGen 电荷；本例采用的水是 SPC/E。参数库、连接规则及水模型一起定义实际模型，不能只保留“PEG”这个名称而随意替换其中一项。

### 无水链的系统拓扑

```
#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
[ system ]
Hydroxyl-ended PEG
[ molecules ]
PEG 1
```

只包含一条PEG，供Polyply生成起始坐标。

### 水溶液的系统拓扑

```
#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
Hydroxyl-ended PEG in SPC/E water
[ molecules ]
PEG 1
```

溶剂化命令把实际水分子数加入molecules段。

运行构建前，先完成[准备页的分子建模环境](https://ml-biomat.com/tutorials/molecular-dynamics/s00/#zh-modeling)安装，其中包含固定版本的 Polyply 与配套依赖。这里使用固定源码提交 38d4d5424e1ef35c86e7cb8532fbd86ecf997221，而不是随安装时间变化的最新分支。辅助脚本同时设定 Python 与 NumPy 的随机种子，再调用 Polyply 的坐标生成入口；种子决定这次起始摆放的随机序列。准备好下面两个文件后，在包含拓扑与 oplsaa.ff 参数目录的例题目录中运行 bash generate.sh，便会得到 PEG.itp 和 PEG.gro。坐标种子让起始模型可追踪，模拟过程中探索哪些构象仍由后续力场和动力学决定。

### 固定坐标构建的随机种子

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

同时初始化Python和NumPy随机数，再调用已安装的Polyply入口。

### 生成PEG16拓扑与起始坐标

```
#!/usr/bin/env bash
set -euo pipefail
polyply gen_params -lib oplsaaLigParGen -o PEG.itp -name PEG -seq OHter:1 PEO:15 OHter:1 > topology-generation.log 2>&1
python seeded_polyply.py 20261416 gen_coords -p polymer.top -o PEG.gro -name PEG -box 6 6 6 > coordinate-generation.log 2>&1
```

在已准备的Polyply环境及oplsaa.ff目录旁运行bash generate.sh。

## 让同一条链经历两段独立的运动

起始坐标生成后，链被置于边长 6 nm 的立方盒中央，再填入水。这个盒子的初始体积为 216 nm³，周期边界让它在三个方向上与相邻映像衔接。盒子需要同时容纳链与周围的水层；只看某一帧的回转半径较小，还不足以决定盒子大小，因为端部的伸展以及整链相对于映像的位置也会变化。后续分析要先恢复完整链，再检查构象的空间跨度与实际映像间距。本例两条记录经逐帧检查，PEG 与非零周期映像的最小原子间距分别约为 3.139 和 3.313 nm，都大于 1.0 nm 的短程截断距离。这个检查针对直接短程接触，长程静电仍按周期体系求解。

能量最小化先松弛构建时的局部接触。本例在这一准备阶段使用柔性水几何及无键约束的最陡下降法，随后所有动力学阶段恢复刚性 SPC/E 水，并约束涉及氢的共价键。约束抑制快速的键长振动，使 2 fs 时间步能够用于这套设置；链仍可通过未冻结的键角、二面角和整体运动改变构象。位置限制则是另一回事：它把指定原子拉向某个参考位置。本例的 PEG 动力学没有位置限制，因此不会把链固定在 Polyply 生成的轮廓上。将这两种“限制”分清，读输入文件时就能知道具体保留了哪些自由度。

共同的最小化末态随后分成两个运行分支。每个分支先进行 100 ps 的定体积控温，再进行 200 ps 的控温控压准备，最后记录 2 ns 的生产轨迹。两条链的化学结构、力场、水分子数和目标温压相同，初始速度及温控器随机种子分别设置。它们从同一个经过最小化的几何出发，经过各自准备阶段后，生产阶段的第一帧便可以具有不同形状。这种安排把不同运动历史带来的差异显露出来；若研究更慢的构象转变，还可以从彼此差异较大的初始构象建立更多独立分支。

参数文件中，v-rescale 将温度控制在 300 K 附近，C-rescale 以各向同性方式调节体积，使平均压力围绕 1 bar 采样；各向同性表示盒子三个方向按同一比例缩放，适合这个没有预设界面方向的溶液。PME 处理周期体系中的长程静电，1.0 nm 是实空间静电和范德华相互作用的短程设置。范德华能量采用势能平移，并包含相应的长程色散修正。理解这些设置的共同作用，比把某个截断值当成所有聚合物的固定答案更有帮助：改变溶剂、分辨率或参数体系时，需要重新检查整套设置的适配关系。

### 写出全部MDP参数

```
"""Write the complete PEG16 simulation settings for two velocity histories.
Run: python write_parameters.py [--out INPUT_DIRECTORY]
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
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    for replica in [1, 2]:
        replacements = {"20263161": str(20263160+replica),
                        "20264161": str(20264160+replica),
                        "20265161": str(20265160+replica),
                        "20266161": str(20266160+replica)}
        for stage, template in [("nvt", NVT), ("npt", NPT), ("md", MD)]:
            content = template
            for old, new in replacements.items():
                content = content.replace(old, new)
            (args.out/f"{stage}-{replica}.mdp").write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
```

运行python write_parameters.py；包含完整最小化、NVT、NPT与生产参数，两个副本使用分别指定的随机种子。

参数生成脚本写出最小化和两个分支所需的全部 MDP 文件，两个分支只在指定的随机种子上区分。生产阶段每 2500 步保存一次坐标，2 fs 乘以 2500 等于 5 ps；2 ns 因而留下从 0 到 2000 ps 的 401 帧，首尾都计入。运行脚本依次完成建盒、溶剂化、最小化和两个分支，所有输入均使用相对路径。在例题目录执行 python write_parameters.py，再执行 bash run.sh，即可沿相同流程计算；已有参考记录也可以直接用于后面的分析。重新运行时应使用新的例题目录，让每段输出保持清楚的对应关系。

### 执行建盒、溶剂化与两条运行分支

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

在新的例题目录运行bash run.sh。每阶段的GRO与CPT衔接到下一阶段。

## 回转半径与端到端距离：同一条链的两把尺子

要测量链的空间尺寸，先把跨过周期边界的部分接回同一个完整分子。假如一段共价键两端分别位于盒子的左边和右边，直接相减会得到接近盒长的距离，而实际相邻原子只隔着一小段键长。分析程序沿拓扑中的键逐一恢复相邻位移，再检查所有键是否保持合理长度。这个顺序比先画图再猜哪一段被切开更可靠，也让后面的质量中心和平方距离拥有明确的几何含义。本例两条轨迹共 802 帧中，恢复后的最长共价键约为 0.1653 nm。

回转半径 Rg 衡量全部原子相对于质量中心的分散程度。先想象把每个原子的位置乘以它的质量，再把这些贡献相加、除以总质量，便得到质量中心；重的原子对这个中心影响更大。随后测量每个原子离中心多远，把距离平方、按质量平均，最后开平方。平方使不同方向的距离不会互相抵消，也让远处原子对整体尺寸更敏感。这个量叫“半径”，但分子无需是球形：一条细长的链、一条弯曲的链，都可以计算 Rg。

全部原子共同定义回转半径式 2

![全部原子共同定义回转半径](https://ml-biomat.com/static/agent-math/f0ddad2cd53c7894acade735.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i, Nₐ | 原子编号与选中原子总数，本例为115 | 1 |
| mᵢ | 原子i的质量 | u |
| Mₐ | 选中原子的总质量，与摩尔质量M区别使用 | u |
| rᵢ, r꜀ₘ | 完整链中原子位置向量、质量中心向量 | nm |
| Rg | 质量加权回转半径 | nm |
| Σ | 对选中原子求和，运算本身无单位 | 1 |
| ‖rᵢ − r꜀ₘ‖² | 位移长度的平方 | nm² |
| mᵢ‖rᵢ − r꜀ₘ‖² | 每个原子的质量乘平方距离 | u nm² |
| =, −, /, √, × | 相等、向量相减、相除、平方根及相邻量相乘；根号使nm²回到nm | 运算本身无单位 |

怎样理解先找到质量中心，再平均各原子的平方距离。质量在分子与分母中抵消，最终保留长度单位。

算一个例子两个等质量节点位于x=−1和+1 nm，y=z=0：质量中心为0，Rg=√[(1²+1²)/2]=1 nm。

使用条件使用同一完整分子的全部原子和真实质量。先按化学键恢复周期边界，不把跨盒坐标当作分子伸长。

端到端距离 Re 则只关注两个指定端点，本例选择左右两个羟基氧。它很直观，也很容易受到端部位置影响：一条链形成较宽的 U 形时，两端可能靠近，但中部仍分布在较大的空间；另一个构象的两端分开较远，内部却可以更紧凑。沿骨架逐段相加得到的轮廓长度，又是第三个量。端到端距离是从起点到终点的直线捷径，轮廓长度是沿实际路径走过的路程，所以前者不大于后者。比较时必须固定端点与骨架定义，否则测量对象已经改变。

端距走直线，轮廓长度沿骨架走式 3

![端距走直线，轮廓长度沿骨架走](https://ml-biomat.com/static/agent-math/030abfabaea5214015e8d7a5.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Re | 两个指定端氧的直线距离 | nm |
| rᴏ,ʀ, rᴏ,ʟ | 右端与左端羟基氧的完整坐标向量 | nm |
| L꜀ | 连接同一对端点的骨架路径总长度 | nm |
| j, Nᵦ | 路径段编号与段数 | 1 |
| ℓⱼ | 第j段的长度 | nm |
| Σ, =, −, ‖·‖, ≤ | 逐段求和、相等、向量相减、向量长度、不大于；运算本身无单位 | 1 |

怎样理解直线是同一对端点之间的最短路程。弯折会改变直线距离，逐段相加仍保留路径长度。

算一个例子三段各1 nm的折线路径长度为3 nm。交互中转角90°时端点位移为(2,1,0) nm，Re=√5≈2.236 nm，小于3 nm。

使用条件端点必须与路径一致。这里测量末端氧；改变为末端碳会得到另一种端距定义。

[Figure: 四个等质量节点的几何尺寸](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s5)

四个等质量节点的平面几何链：三个连接长度固定，通过转动中间线段比较轮廓长度、端距和回转半径。

几何交互中的四个等质量节点通过三段等长连接组成一条折线。调节中间方向时，总轮廓长度保持不变，端距与回转半径却同时改变，而且变化幅度不同。节点间距选择为 1 nm、转角为 90° 时，端距约为 2.236 nm，回转半径约为 0.866 nm；转角回到 0°，它们分别变为 3.000 和 1.118 nm。这里用可控的平面几何帮助理解测量定义。真实 PEG 有 115 个质量不同的原子及三维相互作用，下面的曲线则逐帧使用实际原子质量和完整坐标计算。

### 回转半径和端氧距离的实际变化

两条2ns生产记录，各401帧；浅色背景标出1000–2000ps统计窗口。

化学聚合度16的双羟基PEG，115原子；Polyply固定版本的OPLS-AA/LigParGen参数、SPC/E水。初始6 nm立方盒，300 K、1 bar；共同最小化起点的两条速度/热浴历史各2 ns。

[下载参考数据与完整输入（ZIP） 59.40 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-peg16-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s5)

按化学键逐步恢复整链并核验每一根键，显示两条轨迹的质量加权回转半径与端氧距离。

两条轨迹都表现出持续的收缩与伸展，变化并不总在相同时间发生。整个 2 ns 内，副本 1 的平均 Rg 约为 0.7738 nm，副本 2 为 0.7638 nm，看起来很接近；平均端氧距离却分别约为 1.8845 和 2.1859 nm。这个组合提醒我们，整体原子分散程度接近，并不要求两个端点的统计位置也接近。读图时可以沿着某一段时间同时查看上下两条曲线，找出 Rg 变化较小而端距明显变化的区间，再回到相应构象理解是哪一部分链改变了位置。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s5)

图 3 · 从每个副本全部401帧中分别选择Rg最小和最大的真实构象。显示主链碳、氧及其真实化学键，两个端氧加圈；氢和水参加原模拟。各构象采用各自的主轴平面投影与同一比例尺，图中直线投影距离可能短于三维距离。

## 把许多形状放在一起，平均值才有含义

单独挑选最伸展或最蜷曲的一帧，可以帮助认识链的形状范围；若想知道某种尺寸出现得多不多，需要看整段记录。我们把生产阶段后 1 ns，即 1000 至 2000 ps 之间的 201 帧，用作一个明确的比较窗口。选用同样长度的窗口，可以让两条轨迹的分布在相同统计定义下比较。这个时间选择属于分析方案：它把后段构象单独拿出来观察，并没有给链的所有运动设置一个统一的“完成平衡”时刻。对很慢的形状变化，窗口之间的差别本身就是需要继续研究的信息。

直方图把尺寸轴分成连续的小区间，数一数每个区间中落入多少帧。若只画帧数，增加记录长度就会让所有柱子整体变高；若画概率密度，则先除以总帧数，再除以区间宽度。这样，某一根柱子的高度乘以它的宽度，就等于落入这个区间的帧数比例。横坐标以 nm 为单位时，概率密度的单位为 nm⁻¹。高度超过 1 完全正常，只要所有区间的面积相加为 1；它不是“概率超过百分之百”，而是每单位长度容纳的概率比较集中。

用面积表示概率式 4

![用面积表示概率](https://ml-biomat.com/static/agent-math/484a99912c114acffc6e9f7f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| k | 直方图区间编号 | 1 |
| pₖ | 第k个区间的概率密度 | nm⁻¹ |
| cₖ | 落入该区间的帧数 | 1 |
| F | 纳入统计的总帧数，本例后1ns为201 | 1 |
| Δxₖ | 尺寸区间的宽度 | nm |
| pₖΔxₖ | 该区间的帧数比例，即经验概率 | 1 |
| Σ, =, /, ×, 1 | 对所有区间求和、相等、相除、相乘及归一化常数1；运算本身无单位 | 1 |

怎样理解先用帧数除以总数得到概率，再除以宽度得到密度。所有帧都进入某一区间时，各区间面积相加为1。

算一个例子100帧中20帧落入宽0.05 nm的区间，密度为20/(100×0.05)=4 nm⁻¹，区间概率为4×0.05=0.20。

使用条件两副本使用共同区间边界且覆盖全部所选值；相邻帧的相关性另行用于不确定度分析。

### 后1ns的尺寸分布

每条201帧，使用共同区间边界并覆盖所选数据；阶梯高度乘宽度得到区间概率。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s6)

后1 ns每条201帧的实际构象分布，采用相同分格和概率密度归一化。

后 1 ns 中，两个副本的平均 Rg 分别为 0.7833 和 0.7570 nm，样本标准差分别约为 0.0668 和 0.0560 nm。平均端距分别为 1.9055 和 2.0590 nm，标准差约为 0.3724 和 0.3262 nm。标准差在这里描述这一窗口内形状的起伏幅度，数值较大表示轨迹访问的尺寸更分散。平均值描述分布的位置，两者一起才让“这条链有多大”具备基本的统计含义。图中两个副本的分布有明显重叠，也保留了各自访问不同构象区域的差异。

相邻两帧相隔 5 ps，并不意味着链已经忘记前一帧的形状。某一段链刚刚转动，后续位置通常仍与刚才有关，所以 201 帧包含的独立信息少于 201 次完全独立抽样。计算标准误时，需要考虑这种时间相关，或者使用足够长的分块与更多独立运行。这里先保留每条轨迹的平均值、标准差和完整曲线，避免把重复分支混成一条更长曲线后掩盖它们的差别。两条分支都源于共同的最小化结构，这一点也有助于理解重复所覆盖的是怎样的初始条件范围。

你还可以用同一分析程序改变窗口，比较 0–1 ns 与 1–2 ns；也可以把直方图区间数从 25 改为 12 或 40。前一项改变的是纳入统计的运动片段，后一项改变的是展示分辨率。若细分区间后出现许多尖峰，要先查看每格的帧数，而不是马上为每个尖峰命名一种新的构象状态。某个峰是否对应明确的内部转角组合，需要进一步把尺寸、二面角和时间连续性联系起来。尺寸分布提供了寻找这种关系的入口，原始轨迹保留了追问局部结构的材料。

## 水化不是在链外面套一个固定的壳

“PEG 周围有多少水”听起来像一个可以直接数出的简单问题，实际计算前还需要定义“周围”。本例选用几何标准：只要某个水分子的氧距任意一个 PEG 氧小于 0.35 nm，就把这个水分子列入近邻集合。17 个 PEG 氧分别位于两个羟基端和 15 个内部醚位点，水的氧作为水分子位置的代表。这个定义适合把局部水环境与链的空间结构联系起来，而且可以用每一帧坐标直接重复计算；距离阈值改变时，得到的是另一层空间范围的近邻统计。

这里有两个容易混淆的数。一个水分子可能同时靠近两个甚至更多 PEG 氧，如果按“氧—水氧接触对”逐个计数，它会贡献多次；如果问附近有多少个不同的水分子，则应在最后合并重复身份。想象两家相邻商店分别统计门口的人流，同一个人站在两家门前的交叠区域，会进入两份店门口名单，但整条街上的人数只应记一次。分子分析中的身份合并与此类似，差别在于距离需要考虑三维空间和周期边界。

一次数水分子，一次数接触对式 5

![一次数水分子，一次数接触对](https://ml-biomat.com/static/agent-math/ba060b9dffcbf6fe0bc9863b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| t | 记录时刻 | ps |
| Nw(t) | 满足条件的不同水分子数 | 1 |
| C(t) | 满足条件的聚合物氧—水氧接触对数 | 1 |
| j, Nᴡ | 水分子编号与体系中的水分子总数6996 | 1 |
| i, 𝒪 | PEG氧的编号及其集合，本例17个 | 1 |
| dᵢⱼ(t) | 考虑周期边界的两个氧之间的最短距离 | nm |
| r꜀ | 几何近邻距离阈值，本例0.35 | nm |
| 𝟙[·] | 条件满足记1，否则记0 | 1 |
| Σ, min, ∈, <, = | 求和、取最小值、属于集合、小于及相等；这些运算本身无单位 | 1 |

怎样理解对每个水分子先取它到全部PEG氧的最小距离，就能把多位点共享的水只数一次。双重求和则保留每一个满足阈值的接触对。

算一个例子水A距两个PEG氧分别0.30与0.32 nm，水B为0.34与0.50 nm：0.35 nm阈值下，不同水数为2，接触对数为3。

使用条件这是几何近邻定义。氢键分析另加供受体、氢位置和角度；驻留分析另外跟踪同一水分子的身份。

程序先计算 PEG 氧与所有水氧之间的周期距离矩阵，每一行对应一个 PEG 氧，每一列对应一个水分子。对一列判断“是否至少有一个距离满足阈值”，再把满足条件的列数相加，就得到不同近邻水的数目；直接把矩阵中满足条件的元素数相加，则得到接触对数。这两种写法测量的对象不同，均有用途。前者适合讨论链周围的水分子数量，后者保留同一水分子同时接近多个位点的信息。它们的差值表示按位点计数带来的重复贡献，并不是另一批额外的水。

### 不同水分子数与重复的位点贡献

水氧距任意PEG氧小于0.35nm；上图数不同水分子，下图为接触对数减去不同水数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/#zh-s7)

以聚合物氧—水氧距离小于0.35 nm识别近邻；分别计数不同水分子和原子接触对。

后 1 ns 中，两个副本的不同近邻水数平均为 20.219 和 19.443，样本标准差约为 1.950 和 2.206。按接触对计数时，平均值则为 38.826 和 37.478，明显更大。这些数字正好说明空间交叠的作用：链包含 17 个氧，附近水分子也会靠近相邻的氧位点，分别数每个位点再相加，就会重复计入部分水。每一帧的水分子数仍然是整数，带小数的平均值来自许多帧的统计。例如连续两帧分别数到 20 和 21 个水，平均数便是 20.5。

这个近邻集合随时间更新，并非固定黏在链上的同一批水。要讨论水停留多久，需要沿时间跟踪水分子的身份，并说明短暂离开后返回如何处理；要讨论氢键，还需要氢原子、供体和受体定义，以及方向角条件。0.35 nm 的氧间距离在这里用于空间近邻，不承担完整的氢键判据。链构象改变可能影响近邻数量，近邻数量也可能在相似 Rg 下起伏，因为局部朝向和空间暴露程度仍在变化。把整链尺寸与局部水化并列观察，能让“亲水的柔性链”变成两个可以分别测量、再寻找联系的问题。

## 从完整分析程序走向下一次比较

下面的 Python 程序直接读取两个副本的 md.tpr 和 md.xtc。TPR 提供原子名、质量、电荷与连接关系，XTC 提供各时刻的坐标；两者共同确定我们测量的是哪条分子。程序先核对原子数、元素计数、电荷和水分子数，再沿键恢复完整链，随后计算尺寸和近邻水。MDAnalysis 读入坐标时默认使用 Å，代码在计算链的尺寸时除以 10 转为 nm，在近邻水判断中则使用等价的 3.5 Å。这样的单位转换放在具体计算位置，便于把代码与公式逐项对照。

### 完整的尺寸与水化分析

```
"""Measure PEG shape and geometric hydration in two recorded trajectories.

python analyze_peg.py --records records --out analysis --language en
Each records/replica-1 and replica-2 contains md.tpr and md.xtc.
Dependencies: MDAnalysis, NumPy, Matplotlib. Native coordinates are in angstrom.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors, distance_array
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def bond_plan(group):
    local = {int(index): k for k, index in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for edge, (a, b) in enumerate(edges):
        graph[a].append((b, edge, 1)); graph[b].append((a, edge, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, edge, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, edge, sign))
    if len(seen) != len(group):
        raise ValueError("The polymer must have one connected bond graph")
    return edges, plan


def whole_chain(raw, box, edges, plan):
    vectors = minimize_vectors(raw[edges[:, 1]]-raw[edges[:, 0]], box)
    whole = np.empty_like(raw, dtype=float); whole[0] = raw[0]
    for parent, child, edge, sign in plan:
        whole[child] = whole[parent]+sign*vectors[edge]
    actual = whole[edges[:, 1]]-whole[edges[:, 0]]
    if np.max(np.linalg.norm(actual-vectors, axis=1)) > .005:
        raise ValueError("A reconstructed bond cycle is inconsistent")
    longest = float(np.linalg.norm(actual, axis=1).max()/10)
    if longest > .25:
        raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
    return whole/10, longest


def statistics(values):
    return {"mean": float(np.mean(values)), "sd": float(np.std(values, ddof=1)),
            "minimum": float(np.min(values)), "maximum": float(np.max(values))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    available = {f.name for f in font_manager.fontManager.ttflist}
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [n for n in candidates if n in available],
                         "font.size": 14, "axes.labelsize": 15, "axes.titlesize": 16,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    arrays = []; summaries = []; snapshots = []; maximum_bond = 0.
    for rep in [1, 2]:
        folder = args.records/f"replica-{rep}"
        u = mda.Universe(str(folder/"md.tpr"), str(folder/"md.xtc"))
        polymer = u.select_atoms("resname OHter PEO")
        oxygen = polymer.select_atoms("name O*")
        water = u.select_atoms("resname SOL and name OW")
        terminal = np.flatnonzero(polymer.names == "OA1")
        if len(polymer) != 115 or len(oxygen) != 17 or len(water) != 6996 or len(terminal) != 2:
            raise ValueError("Expected one hydroxyl-ended PEG16 and 6996 SPC/E waters")
        counts = {element: int(sum(n.startswith(element) for n in polymer.names)) for element in ["C", "H", "O"]}
        if counts != {"C": 32, "H": 66, "O": 17} or abs(sum(polymer.charges)) > 1e-5:
            raise ValueError("Polymer formula or charge differs from the defined model")
        edges, plan = bond_plan(polymer)
        rows = []; shapes = []
        for frame in u.trajectory:
            pos, longest = whole_chain(polymer.positions.astype(float), frame.dimensions, edges, plan)
            maximum_bond = max(maximum_bond, longest)
            center = np.average(pos, axis=0, weights=polymer.masses)
            centered = pos-center
            rg = np.sqrt(np.average(np.sum(centered**2, axis=1), weights=polymer.masses))
            end = np.linalg.norm(pos[terminal[1]]-pos[terminal[0]])
            # A water contributes once to unique hydration, even near several polymer O atoms.
            near = distance_array(oxygen.positions, water.positions, box=frame.dimensions) < 3.5
            unique = int(np.any(near, axis=0).sum())
            pairs = int(near.sum())
            rows.append([float(frame.time), float(rg), float(end), unique, pairs])
            shapes.append(centered)
        values = np.asarray(rows); arrays.append(values)
        if values.shape != (401, 5) or not np.allclose(values[:, 0], np.arange(401)*5):
            raise ValueError("Expected 401 saved frames from 0 to 2000 ps")
        late = values[:, 0] >= 1000
        names = ["Rg_nm", "Re_nm", "unique_waters", "oxygen_water_pairs"]
        summaries.append({"replica": rep, "frames": len(values), "late_frames": int(late.sum()),
                          "all": {n: statistics(values[:, k+1]) for k, n in enumerate(names)},
                          "last_1ns": {n: statistics(values[late, k+1]) for k, n in enumerate(names)}})
        with (args.out/f"replica-{rep}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle); writer.writerow(["time_ps", *names]); writer.writerows(values)
        for label, index in [("minimum-Rg", int(np.argmin(values[:, 1]))), ("maximum-Rg", int(np.argmax(values[:, 1])))]:
            snapshots.append({"replica": rep, "selection": label, "time_ps": values[index, 0],
                              "Rg_nm": values[index, 1], "Re_nm": values[index, 2],
                              "coordinates_nm": shapes[index].tolist(), "names": polymer.names.tolist(),
                              "bonds": edges.tolist(), "terminal_indices": terminal.tolist()})
    summary = {"model": "HO-(CH2-CH2-O)16-H; OPLS-AA/LigParGen; SPC/E; 300 K; 1 bar",
               "window_ps": [1000, 2000], "sd_definition": "sample SD, ddof=1; not uncertainty of the mean",
               "hydration_cutoff_nm": .35, "maximum_bond_nm": maximum_bond, "replicas": summaries}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    colors = ["#147d92", "#c46b3c"]
    labels = ["副本 1", "副本 2"] if zh else ["Replica 1", "Replica 2"]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for k, (ax, ylabel) in enumerate(zip(axes, ["回转半径 Rg / nm", "端氧间距 Re / nm"] if zh else ["Radius of gyration Rg / nm", "Terminal-O distance Re / nm"])):
        for i, values in enumerate(arrays):
            ax.plot(values[:, 0]/1000, values[:, k+1], color=colors[i], lw=1.2, label=labels[i])
        ax.axvspan(1, 2, color="#e7d8b4", alpha=.2); ax.set_ylabel(ylabel); ax.grid(alpha=.15)
    axes[0].legend(ncol=2); axes[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axes[0].set_title("相同链长，两条构象历史" if zh else "One chain length, two conformational histories")
    save(fig, args.out/"peg-shape")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8), constrained_layout=True)
    pooled = np.concatenate([v[v[:, 0] >= 1000] for v in arrays])
    bins = [np.linspace(pooled[:, k].min()-.01, pooled[:, k].max()+.01, 26) for k in [1, 2]]
    for k, ax in enumerate(axes):
        for i, values in enumerate(arrays):
            v = values[values[:, 0] >= 1000, k+1]
            ax.hist(v, bins=bins[k], density=True, histtype="step", linewidth=2.3, color=colors[i], label=labels[i])
        ax.set_xlabel(["Rg / nm", "Re / nm"][k]); ax.set_ylabel("概率密度 / nm⁻¹" if zh else "Probability density / nm⁻¹"); ax.grid(alpha=.15)
    axes[0].legend(); fig.suptitle("后 1 ns 的构象分布：每条 201 帧" if zh else "Conformational distributions over the final 1 ns: 201 frames each")
    save(fig, args.out/"peg-distributions")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for i, values in enumerate(arrays):
        axes[0].plot(values[:, 0]/1000, values[:, 3], color=colors[i], lw=1.2, label=labels[i])
        axes[1].plot(values[:, 0]/1000, values[:, 4]-values[:, 3], color=colors[i], lw=1.2, label=labels[i])
    axes[0].set_ylabel("不同近邻水分子数" if zh else "Unique nearby water molecules")
    axes[1].set_ylabel("接触对数 − 不同水分子数" if zh else "Contact pairs − unique waters")
    axes[0].set_title("氧—水氧距离小于 0.35 nm 的几何近邻" if zh else "Geometric neighbors: polymer O–water O distance < 0.35 nm")
    axes[0].legend(ncol=2); axes[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    for ax in axes: ax.axvspan(1, 2, color="#e7d8b4", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"peg-hydration")
    print(json.dumps(summary, indent=2))


def save(fig, path):
    fig.savefig(path.with_suffix(".svg")); fig.savefig(path.with_suffix(".png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
```

读取两条真实轨迹，按化学键恢复链并核对所有键，输出逐帧数据、分布和水化图。

把两条参考记录分别放在 records/replica-1 与 records/replica-2 中，执行 python analyze_peg.py --records records --out analysis --language zh，就会得到三组图、两份逐帧 CSV 和统计摘要。选择 en 会使用相同数据与计算，只改变图中的语言。CSV 的一行对应一帧，列中依次保留时间、回转半径、端氧距离、不同近邻水数和接触对数，因此可以从某一个图上感兴趣的点回到明确的时刻。程序还保存每个副本中 Rg 最大和最小的真实构象，便于将分布两端与原子画面联系起来。

将来增加链长时，一个很有用的出发点是最简单的自由连接链。设想一条链由 N 段等长、方向彼此独立的线段组成，每段长度为 b。端到端向量是这些小向量相加的结果；平方后既有每段自身的长度平方，也有不同段之间的交叉项。对大量方向各向同性的构象取平均，交叉项相互抵消，便得到下面的关系。它说明随机折线的典型端距随段数的平方根增加，而沿路程相加的轮廓长度随段数本身增加。两种“长度”因此具有不同的增长方式。

自由连接链的典型端距式 6

![自由连接链的典型端距](https://ml-biomat.com/static/agent-math/9ef8a802f33a136168b4ab44.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N | 方向独立的统计线段数 | 1 |
| b | 每段的固定长度 | nm |
| Re² | 端到端距离的平方 | nm² |
| ⟨Re²⟩ | 构象集合中的平均平方端距 | nm² |
| Re,rms | 均方根端距，与平均端距区别使用 | nm |
| L꜀ | 轮廓长度 | nm |
| ⟨·⟩, =, √, ×, ² | 构象平均、相等、平方根、相乘和平方运算；平方把长度单位变为nm² | 运算本身无单位 |

怎样理解端向量由N个段向量相加；独立且各向同性的方向使不同段的点积平均为零，剩下N份b²。

算一个例子N=16、b=0.5 nm的理想链有平均平方端距4 nm²，均方根端距2 nm，轮廓长度8 nm。这里N是模型线段数。

使用条件自由连接、等长、独立各向同性方向的理想模型。PEG化学重复数不直接等于统计段数；本例原子模拟保留角度、转动势和溶剂。

PEG 的化学键角、二面角、原子体积和溶剂相互作用会让相邻方向相关，因此应用这个理想关系时，必须先说明怎样把实际分子转换成统计线段。化学重复数 n 为 16，不会自动等于理想模型中的独立线段数 N；从原子轨迹获得统计段长，需要更多构象与长度信息。这个区分很重要，因为它让简单模型发挥解释作用，同时把需要从真实分子中测出的量留在正确位置。以后比较 PEG8、PEG16 与 PEG32 时，我们会继续固定端基、力场、水模型和测量定义，再观察尺寸如何变化。

本讲的轨迹已经显示，同一条短链可以在相近的平均回转半径下经历不同的端距历史，几何近邻水的数量也在持续起伏。下一次研究可以据此提出明确的问题：增加链长后，尺寸分布是否向更大的范围移动；每条链周围的水是否增加；若按氧位点数归一化，水化变化又如何。对于端基修饰或表面连接，还需要把端基化学和空间约束写进新模型。沿着“分子身份—运动条件—测量定义—统计比较”的顺序推进，才容易看清一项材料变化究竟改变了哪个分子过程。

## 延伸阅读与开放资料

- [Polyply Quick Start and oplsaaLigParGen library](https://github.com/marrink-lab/polyply_1.0/tree/38d4d5424e1ef35c86e7cb8532fbd86ecf997221) · Polyply developers; Marrink group · Apache-2.0

  拓扑生成、坐标构建流程以及PEO、OHter原子参数和连接定义。

  把通用构建流程用于双羟基PEG16水溶液；固定起始种子，增加两条GROMACS2026.4运行历史、元素计数与完整分析。
- [Polyply; a python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald, Riccardo Alessandri, Peter C. Kroon, Luca Monticelli, Paulo C. T. Souza, Siewert J. Marrink · CC BY 4.0

  连接图参数化与坐标构建相分离的方法背景。

  用本例PEG说明两个阶段，图解与分析重新绘制。
- [LigParGen web server: an automatic OPLS-AA parameter generator for organic ligands](https://doi.org/10.1093/nar/gkx312) · Leela S. Dodda, Israel Cabeza de Vaca, Julian Tirado-Rives, William L. Jorgensen · Bibliographic reference; no article text or figures reproduced

  固定参数库所引的LigParGen参数背景。

  保留库内参数，不通过网页重新生成电荷。
- [Macromolecular Chemistry — Nobel Lecture, 1953](https://www.makro.uni-freiburg.de/dateien_neu/document-pdf-word-excel-usw/geschichte/vorlesung_hs) · Hermann Staudinger · Publicly readable lecture; no open reuse license assumed

  大分子共价连接及天然、合成材料之间的历史联系。

  简述历史观点；使用独立绘制的连接示意图。
- [Hermann Staudinger and the Foundation of Polymer Science](https://www.acs.org/education/whatischemistry/landmarks/staudingerpolymerscience.html) · American Chemical Society, National Historic Chemical Landmarks · Publicly readable history; no site text or image reproduced

  1920年长链观点和橡胶氢化所检验的问题。

  简述事实并连接到本讲的拓扑与构象概念。
