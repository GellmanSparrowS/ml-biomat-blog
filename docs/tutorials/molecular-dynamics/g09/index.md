# 一条曲线有多可靠：重复、相关与误差

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g09/
Language: zh-CN

用三条泛素轨迹区分真实涨落、时间相关与平均值的不确定性，让下一次计算补充需要的信息。

## 多算几千帧，为什么还要问结果有多可靠

如果想知道一座城市夏天通常有多热，连续一小时每秒记录一次气温，会得到3600个数字；每天同一时间测量一次，持续一个月，则只有约30个数字。前一组记录很多，却主要描述那一个小时的天气。后一组记录较少，覆盖的天气变化可能更丰富。分子模拟也有类似的问题：轨迹文件可以保存成千上万幅构象，但这些构象沿着连续的运动产生，相邻两幅往往保留了相似的结构。读懂一条曲线，需要同时知道它记录了多少次、持续了多久，以及在这段时间里经历过哪些变化。

这个问题会直接影响研究决策。假设两种溶液中的蛋白质平均回转半径相差0.003 nm，我们希望知道这是否与溶液条件有关。如果同一种条件的不同轨迹之间也常有这么大的差异，就应该先增加重复和观察时间，再比较条件。又例如，某个药物结合口袋在一条轨迹里保持张开，而另一条轨迹里较早闭合，研究重点便从挑选一幅好看的快照，转向开闭状态出现的频率与转换时间。统计分析在这里帮助我们安排下一次计算，让计算资源用于区分真正关心的物理差异。

本节继续观察水中的泛素。它有76个氨基酸残基，采用AMBER99SB-ILDN蛋白参数、TIP3P水和同一份加盐体系，在300 K、1 bar下运动。我们从共同的最小化坐标出发，准备三组不同初始速度和随机热浴种子的轨迹，每组都经历100 ps NVT、200 ps NPT准备，再记录1 ns无位置限制的生产过程。蛋白、水和离子的相互作用保持相同，因此这三组记录能够回答：在这个共同起点和给定模型下，重新开始一次随机运动，会得到多大的短时间差异？

我们会先画出三条原始曲线和累计平均，再用时间相关、分块平均和副本间比较拆开这些差异。RMSD描述相对共同参考结构的偏离，回转半径描述蛋白质量在质心周围的分布，两者需要分别检查。读完之后，你可以说明一张误差图究竟把什么当作重复，判断增加输出频率与延长轨迹有什么区别，并给后续采样提出具体安排。这里的“误差”主要指有限采样造成的不确定性；积分步长、力场选择和实验条件对应的问题，仍然分别通过数值检验与模型比较处理。

先保留一个有用的直觉：分子的热运动本身会涨落，而我们对平均值的认识也会因记录有限而不精确。这两件事可以同时发生，却不是同一个数。一条柔软的蛋白环区即使被充分观察，也可能持续大幅运动；积累更多合适的样本，改进的是对这种运动分布的认识，而不会把真实的柔软性从分子里抹掉。接下来所有公式都围绕这个区别展开：哪些数描述分子在动，哪些数描述我们对平均状态知道多少。

## 连续运动留下记忆：分块思想从哪里来

分子运动方程让当前坐标和速度参与下一步计算，因此一条轨迹天然带有时间上的联系。一个环区刚向外摆动，下一帧通常还在附近；整个蛋白正在缓慢转变局部构象，连续许多帧都可能处于相似状态。这里说的“记忆”是统计意义上的：知道当前读数，能够帮助预测过一小段时间后的读数。它并不要求分子主动保存信息，也不要求所有物理量具有同样长的记忆。速度、局部键角、整体尺寸和构象状态，可以在不同时间尺度上变化。

随着分子动力学和蒙特卡洛计算积累越来越长的记录，研究者发现，对相关数据直接使用独立测量的误差公式，会把重复的信息算得过多。Flyvbjerg与Petersen在1989年研究了相关数据平均值的误差估计，用逐步合并相邻数据的分块思想处理这个问题。其历史意义在于，误差分析开始把数据的生成方式带回计算：同一串数字，保持相邻顺序与打乱顺序，可能具有相同的均值和宽度，却有不同的时间联系。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s2)

图 1 · 相邻观测合并的历史概念图。示意数值使用无量纲单位，B₂和B₄分别表示每块2个和4个读数的平均。

可以用一条缓慢起伏的水面记录理解图中的做法。很近的两个时刻常常位于同一个波峰，把它们平均后，就得到一小段时间的代表值；再把相邻小段合并，代表的时间范围逐渐增长。若一块已经覆盖了大部分相关运动，不同块之间剩下的联系会减弱。我们就能够从块与块的差异估计平均值的采样尺度。合并过程没有改变底层物理模型，它改变的是统计单位：从单帧读数，转为一段连续时间内的平均读数。

分块还揭示了一个取舍。块很短时，块数很多，但相邻块仍可能跟着同一个慢变化一起升降；块很长时，这种联系减弱，却只剩少数块可供比较。一条1000 ps的记录，每100 ps分一块有10块，每200 ps分一块只有5块。只选择一个自己喜欢的块长，很容易错过这个变化。更有信息的做法，是画出估计值怎样随块长改变，同时检查原始时间曲线，让分块结果与实际运动相互解释。

现代分子模拟的统计实践把这条思路与多副本比较结合起来。沿同一轨迹分块，询问的是这段运动内部的时间组织；从同一建模方案重新生成随机轨迹，则观察重新开始后会出现哪些差异。两者服务于同一研究问题，却覆盖不同层次。对于从一个实验结构起步的蛋白，几个不同速度的副本仍然共享这个结构及周围溶剂的初始安排。把共同条件说清楚，就能准确理解重复结果，并进一步决定是否需要从更多构象或重新构建的溶剂环境出发。

## 把重复设计好，再开始比较

有意义的重复先要保持测量对象一致。三份轨迹的RMSD都使用228个主链N、Cα、C原子，按质量加权完成整体平移与旋转拟合，再相对同一份最小化参考结构计算偏离。回转半径则使用全部1231个蛋白原子的质量和完整坐标。若每个副本各自选自己的生产第一帧作为参考，RMSD就会分别回答“离我自己的起点有多远”，三条曲线之间还混入参考结构的差异。共同参考使它们面对同一把尺子，原子选择与单位也始终相同。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s3)

图 2 · 共同起点下的随机副本设计。每条分支内部延续状态，最终用共同参考和原子选择比较。

三条分支从相同的em.gro坐标开始，在NVT入口生成各自的初始速度。gen-seed控制这一步的随机抽样，ld-seed控制相应阶段所用的随机过程。本例将第一组初始速度种子设为20261121，其余两组依次加1；NVT、NPT和生产阶段的ld-seed分别采用各自的一组整数。种子是重现随机数序列的入口编号，数值大小不表示温度高低、运动强弱或结果质量。温度由目标条件与实际动力学决定，种子的作用是在同一规则下选择另一组随机实现。

初始速度只在NVT开始时重新生成。NPT读取前一阶段保存的坐标和检查点，生产阶段再延续NPT的速度与状态；后两段的gen-vel保持no。这样，每个副本内部是一段连续准备与运动的过程，三个副本之间则从一开始就采用不同的随机实现。100 ps与200 ps的准备过程保留蛋白重原子位置限制，生产阶段解除该限制。解释生产中的尺寸变化时，需要把这次解除限制视为准备方案的一部分，并检查结构是否还在继续调整。

下面的运行入口把三个副本放入新建目录。准备文件夹中应放入前面得到的em.gro、topol.top和posre.itp；拓扑所引用的AMBER99SB-ILDN力场由同一套GROMACS安装提供。脚本为每个副本建立共同参考、依次运行三段，再输出RMSD和回转半径。它保留每个副本自己的文件，便于把一条曲线追溯到对应的输入条件。运行前，先把三个基准MDP文件与两个脚本放在同一例题目录，随后执行bash run_replicas.sh。

### 运行三个副本并导出相同观测量

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python make_replicas.py --prepared prepared --output new-replicas
for replica in 1 2 3; do
  (
    cd "new-replicas/replica-${replica}"
    "$gmx" grompp -f md.mdp -c em.gro -p topol.top -o reference.tpr
    "$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
    "$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off
    "$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr
    "$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off
    "$gmx" grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
    "$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off
    printf 'Protein\nSystem\n' | "$gmx" trjconv -s md.tpr -f md.xtc -o md-whole.xtc -pbc mol -center
    printf 'Backbone\nBackbone\n' | "$gmx" rms -s reference.tpr -f md-whole.xtc -o rmsd.xvg -fit rot+trans
    "$gmx" gyrate -s md.tpr -f md-whole.xtc -o gyrate.xvg -sel 'group "Protein"'
  )
done
python analyze_replicas.py --records new-replicas --out analysis --language en
```

在例题目录运行bash run_replicas.sh，prepared包含共同最小化坐标、拓扑与位置限制文件。

生成器用参数名称寻找种子设置，只替换明确对应的那一行。三个基准输入中的第一副本参数与参考计算一致，其余副本只在规定的种子位置变化。新目录采用创建而不覆盖的方式，因此已经完成的一组计算仍可保留。共同坐标、共同拓扑和不同种子这三件事，通过文件操作对应到明确的实验设计：每条分支面对相同的势能模型，同时拥有自己的热运动历史。

### 生成各副本的输入与固定种子

```
"""Create three independent random realizations from one prepared structure.

python make_replicas.py --prepared prepared --output new-replicas

The prepared folder contains em.gro, topol.top and posre.itp from the protein
preparation. Baseline nvt.mdp, npt.mdp and md.mdp sit beside this script.
"""
from pathlib import Path
import argparse
import re
import shutil


def replace_setting(text, key, value):
    pattern = rf"(?m)^{re.escape(key)}\s*=.*$"
    result, count = re.subn(pattern, f"{key} = {value}", text)
    if count != 1:
        raise ValueError(f"Expected exactly one {key} setting")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, default=Path("prepared"))
    parser.add_argument("--output", type=Path, default=Path("new-replicas"))
    args = parser.parse_args()
    templates = {stage: Path(f"{stage}.mdp").read_text(encoding="utf-8")
                 for stage in ("nvt", "npt", "md")}
    for name in ("em.gro", "topol.top", "posre.itp"):
        if not (args.prepared/name).is_file():
            raise FileNotFoundError(f"Prepared input missing: {name}")
    args.output.mkdir(exist_ok=False)
    for number in (1, 2, 3):
        folder = args.output/f"replica-{number}"
        folder.mkdir()
        for name in ("em.gro", "topol.top", "posre.itp"):
            shutil.copyfile(args.prepared/name, folder/name)
        for stage, offset in [("nvt", 20261200), ("npt", 20261300), ("md", 20261400)]:
            text = replace_setting(templates[stage], "ld-seed", offset+number)
            if stage == "nvt":
                text = replace_setting(text, "gen-seed", 20261120+number)
            (folder/f"{stage}.mdp").write_text(text, encoding="utf-8", newline="\n")
    print("Prepared three seed-specific folders with the same coordinates and topology.")


if __name__ == "__main__":
    main()
```

按参数名称替换gen-seed和ld-seed，其他模型参数保持一致。

### NVT基准输入：生成初始速度

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
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
define = -DPOSRES
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261121
ld-seed = 20261201
```

100 ps、300 K、蛋白重原子位置限制；由生成器写入各副本种子。

### NPT基准输入：延续状态并调整体积

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
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
define = -DPOSRES
refcoord-scaling = com
nsteps = 100000
ld-seed = 20261301
```

200 ps、300 K、1 bar，保留位置限制并延续速度。

### 生产基准输入：解除位置限制

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 500
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
nsteps = 500000
ld-seed = 20261401
```

1 ns无位置限制NPT；每1 ps保存一帧，继承前一阶段状态。

复现也有不同层次。同一种算法在不同并行执行方式下，浮点求和的次序可能不同，微小舍入会逐渐改变具体轨迹。本组参考计算使用同一GROMACS 2026.4版本和同一物理参数，包含CPU与加速执行得到的随机副本；比较的是共同测量定义下的统计与结构行为。若问题专门针对执行方式，就另外固定同一输入、种子和计算环境做数值对照。本节首先固定科学模型，把不同副本的实际变化完整保留下来。

## 平均值、涨落宽度和累计曲线分别说明什么

先把一个物理量写成按时间排列的读数。可以选择RMSD，也可以选择回转半径，每一个读数的单位都是nm。算术平均把所有读数相加，再除以读数个数，相当于让每个等间隔保存的时刻占有相同权重。样本标准差则先减去平均值、把差平方、相加后除以N−1，再开平方。平方让偏高与偏低都贡献宽度，开平方把单位恢复成nm。N−1反映平均值已经由这组数据估计；存在时间相关时，使用这个分母仍不能自动解决有效样本数的问题。

平均值与样本标准差式 1

![平均值与样本标准差](https://ml-biomat.com/static/agent-math/60e186597ec69212c30c8b8e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| xⱼ, x̄ | 第j个读数与所选读数的平均值；上横线表示平均 | nm |
| sₓ | 该记录的样本标准差，描述读数围绕均值的散布 | nm |
| N, j | 读数总数与编号；本节N=1000 | 1 |
| (xⱼ−x̄)² | 一个读数偏离均值的平方 | nm² |
| N−1 | 估计样本方差使用的分母；时间相关另行检查 | 1 |
| Σ, /, −, +, = | 按指定编号求和、除法、减法、加法与定义等号；相邻量相乘 | 运算符无单位 |
| √ | 非负平方根，把nm²恢复为nm | 运算符无单位 |

怎样理解等间隔读数获得相同权重；偏差平方避免正负抵消，开方恢复原量的尺度。

算一个例子1.18、1.20、1.22 nm的平均为1.20 nm；s=√[(0.0004+0+0.0004)/2]=0.020 nm。

使用条件描述固定窗口内的数值与宽度。相关帧的s/√N需要独立性检验后才能解释为均值标准误差。

举一个可以手算的例子：三次长度读数是1.18、1.20、1.22 nm，平均值为1.20 nm。三项偏差平方分别为0.0004、0和0.0004 nm²，除以2再开方，样本标准差为0.02 nm。这个数说明三次读数相对中心的散布尺度。如果把同一个顺序重复抄写十次，数据表变长了，物理观察却没有增加。平均值的可靠程度因此还需要知道这些数字之间怎样关联，而不只看计算器里的N变成了多大。

本节原始时间图展示0到1000 ps的1001个保存时刻。为了把同一段记录恰好分成完整的等长块，统计采用0≤t<1000 ps，即0至999 ps这1000个时刻，1000 ps终点仍显示在原始曲线中。前500个读数属于0≤t<500 ps，后500个属于500≤t<1000 ps。这个约定使100 ps一块恰好得到10块。它与上一节包含终点的1001帧描述有一个读数的差别，所以本节会直接报告自己的窗口与均值，避免把边界不同的结果当作计算冲突。

### 同一把尺子下的三条轨迹

逐帧曲线展示0–1000 ps，累计与分块统计使用0≤t<1000 ps；RMSD共同参考，Rg全蛋白质量加权。

GROMACS2026.4；PDB 1UBQ链A、76个残基；AMBER99SB-ILDN与TIP3P。保留602个实验重原子，加入629个氢原子；His68选中性NE2质子化状态，采用带电游离末端。

[下载参考数据与完整输入（ZIP） 0.36 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-replicate-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s4)

三个随机副本共享蛋白化学模型与最小化参考结构，各自具有独立的初始速度和随机耦合过程。逐帧图显示0–1000 ps，累计均值使用0≤t<1000 ps的1000条等间隔记录；每条曲线保留各副本的运动历史。

在这1000个读数中，三个副本的平均RMSD分别约为0.14377、0.12485和0.19556 nm；平均回转半径分别约为1.19152、1.18785和1.18476 nm。RMSD的差异表明三段运动相对共同参考具有不同的偏离程度，而回转半径更接近，说明总体质量分布的尺寸变化小得多。这两种观察可以同时成立：一个环区的转向或局部构象变化，能够改变相对参考的偏离，却未必大幅改变整体紧凑程度。进一步定位差异时，再回到残基波动、接触和实际构象。

累计平均曲线在每个时刻使用从生产起点到当前的全部读数。它越到后面通常越平滑，因为单个新读数只占越来越小的权重。把一个已有平均值与一个新值合并时，旧数据总数越大，新值越难把整体平均拉远。这个算术效果本身就能让曲线看起来逐渐安定。因此，我们还要观察三条累计平均是否接近、原始曲线是否经历相似范围，以及前后窗口的均值是否一致。平滑度帮助阅读，多个尺度上的比较才帮助判断采样。

原始曲线中的宽度也有直接的物理含义。副本1的RMSD样本标准差约0.04167 nm，而回转半径标准差约0.00603 nm，说明这两个观测量的时间波动尺度不同。数值的大小与各自定义有关，不能把它们直接排成蛋白“稳定性”的等级。RMSD测量相对一个固定结构的偏离，回转半径测量围绕自身质心的展开程度；它们都把复杂构象压缩为一个标量。把标量与结构图配合，才能把变化联系到具体分子运动。

## 相隔多久，两次观察才带来不同的信息

现在把时间曲线想象成两张相同的透明纸。第一张保持不动，第二张沿时间轴平移若干格，再比较重叠区域里的读数。如果一张在平均值上方时，另一张也经常在上方，两者具有正相关；如果一个偏高时另一个常常偏低，则可能出现负相关。比较之前先减去各自这段记录的平均值，使讨论集中在涨落，而不让一个很大的常量背景占据结果。对同一条曲线不同时间位置的比较，称为自相关。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s5)

图 3 · 有限记录的配对示意：间隔3格时，10个读数产生7对。灰色格不参与该方向的这次配对。格内数字表示记录序号。

本例相邻记录间隔1 ps，把第二张纸平移k格，就是比较相隔k ps的两个时刻。每对偏差相乘，同号时给正值，异号时给负值；把能够配成对的结果平均，再除以零间隔时的平均偏差平方，就得到无量纲的自相关读数。零间隔把每个偏差与自身相乘，所以归一化后的C(0)=1。随着间隔增大，若原先的关联逐渐消失，曲线会接近零；一小段负值也可能来自回摆、有限记录或缓慢变化，需要结合原始曲线判断。

按实际配对数计算的中心化自相关式 2

![按实际配对数计算的中心化自相关](https://ml-biomat.com/static/agent-math/9547f4c544bc1594deabd703.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dⱼ, dⱼ₊ₖ | 相隔k个记录的两个读数，各自减去同一窗口均值 | nm |
| xⱼ, x̄ | 第j个原读数与窗口平均值 | nm |
| v | 零间隔均方偏差，使用N作分母 | nm² |
| dⱼdⱼ₊ₖ | 两个偏差的乘积，同号为正、异号为负 | nm² |
| C(k) | 间隔k处的归一化自相关；C(0)=1 | 1 |
| N, j, k, N−k | 读数数目、起点编号、间隔格数和可用配对数；本例一格1 ps | 1 |
| Σ, /, −, +, = | 按指定编号求和、除法、减法、加法与定义等号；相邻量相乘 | 运算符无单位 |
| ² | 一个偏差与自身相乘，结果单位为nm² | 指数无单位 |

怎样理解比较同一序列相隔一定时间的偏差，按可用配对求平均，再除以自身均方偏差消去量纲。

算一个例子中心化序列−1、−1、1、1 nm有v=1 nm²；k=1时乘积和为1 nm²、配对数3，因此C(1)=1/3。

使用条件等间隔、非零方差的有限记录估计。解释为平衡记忆时间时，还需相应时段具有稳定的统计性质。

用四个已经减去平均值的读数−1、−1、1、1理解这个计算，零间隔的平均平方是1。相隔一格有三对，乘积为1、−1、1，平均后得到1/3，自相关就是1/3。若把相同四个数排成−1、1、−1、1，均值与散布都保持不变，相隔一格的乘积却全部为−1。顺序因此包含均值和直方图之外的信息。这也解释了为什么在分析之前随机打乱时间序列，会改变与相关性有关的误差判断。

自相关的归一化还涉及一个容易遗漏的细节：间隔为k格时，只有N−k对数据。程序用这个实际配对数求平均，再用全窗口的零间隔均方偏差归一化。较大的间隔使用较少的配对，结果会更不稳定；用同一段有限数据估计均值，也会影响相关函数的尾部。因此我们把图画到200 ps，并把它当作这段记录的时间结构诊断，结合前后窗口与副本比较一起读。不同软件的有限样本归一化约定可能略有差别，复算时应先对齐公式和配对规则。

还有一个更基础的条件：把一个自相关曲线解释为平衡状态的记忆时间，通常要求平均状态和涨落性质在所分析时段内保持一致。如果蛋白在这1 ns内仍持续离开初始结构，慢趋势也会让相隔较远的读数呈现联系。直接把这条相关曲线积分，可能把准备过程与平衡涨落混在一起。本节先展示这种慢联系，并在下一部分检查分块结果；需要平衡相关时间时，再为所关心的构象量建立更长、更稳定的观察窗口。

输出间隔应该与待观察的变化相配合。若每100 ps保存一帧，却想研究几皮秒的快速联系，记录会跳过需要比较的细节；若每0.1 ps保存一次，观察的总时长仍只有100 ps，就增加了同一段运动的时间分辨率。两种选择分别影响快速过程的可见程度与文件大小。延长轨迹则可能接触新的构象变化，是另一种投入。先估计研究问题的时间尺度，再选择保存频率与运行时长，能够同时照顾可读的曲线和有用的采样。

## 把相邻时刻合成一块，看看误差怎样改变

分块平均把前面的直觉变成一个可以执行的计算。先选每块包含b个相邻读数，把它们平均为一个块均值；整段记录恰好分成M块。本节的块彼此不重叠，每个原始读数只进入一块，所有块长度相同。接着计算这些块均值之间的样本标准差，再除以块数的平方根，得到按这些块估计的均值标准误差。最后这一步使用了块均值近似独立的统计条件，所以我们会改变b来检查结果，而不是把切块本身当作独立性的证明。

等长分块与块均值标准误差式 3

![等长分块与块均值标准误差](https://ml-biomat.com/static/agent-math/82ec1a03ff4bd1513f3eb70c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Bₘ | 第m个连续时间块的平均值 | nm |
| b, M, N, m, j | 每块读数数目、块数、总读数数目、块编号与读数编号 | 1 |
| xⱼ, x̄ | 原读数与全部等长块对应的总平均 | nm |
| SE_{b} | 按块均值近似独立计算的总平均标准误差 | nm |
| (Bₘ−x̄)² | 块均值相对总平均的偏差平方 | nm² |
| (m−1)b+1, mb | 第m块的第一个与最后一个读数编号 | 1 |
| Σ, /, −, +, = | 按指定编号求和、除法、减法、加法与定义等号；相邻量相乘 | 运算符无单位 |
| √ | 非负平方根，将方差单位恢复为长度 | 运算符无单位 |

怎样理解先把相邻读数平均为一个时间块，再把块间样本方差除以块数；独立性通过块长和采样检查。

算一个例子四块均值1.18、1.20、1.22、1.20 nm，偏差平方和0.0008 nm²；SE=√[0.0008/(4×3)]=0.008165 nm。

使用条件完整、等长、不重叠块；M至少为2。块长增加后仍需足够块数，图上的估计随块长变化是采样诊断。

假设四个足够独立的块均值是1.18、1.20、1.22、1.20 nm。总体平均为1.20 nm，块均值的样本标准差约0.01633 nm，除以√4得到0.008165 nm的标准误差。标准差描述四个块均值之间的散布，标准误差描述用这四块平均来估计共同中心的采样尺度。若这些块仍跟着同一个缓慢趋势一起变化，独立性的条件就需要重新检查。一个公式能够算出数值，与这个数值适合回答当前问题，是相互衔接的两步。

### 相关时间结构与块长敏感性

相邻记录1 ps；1000个读数。每块从1到200个记录，分别计算各副本；200 ps时仅5块。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s6)

左列用各副本的窗口平均值中心化后计算自相关；右列把同一段记录分成等长、不重叠的块，再从块均值计算标准误差。每块从1 ps增至200 ps时，块数从1000降至5；曲线是否形成稳定区域，是选择统计尺度时要观察的信息。

实际图给出了从1 ps到200 ps的多种块长。副本1的RMSD若逐帧按独立数据处理，标准误差约0.00132 nm；100 ps一块时增至约0.01237 nm，200 ps一块时约0.01747 nm。增长的趋势说明短块把许多相近时刻当成了过多的独立信息。在已经检查的块长范围内，这条曲线还没有形成清楚的平台，而且最长块只剩5个。因此，下一步应延长有关构象的观察，并保留独立副本，继续判断慢变化，而不是从现有图中挑一个数作为最终平衡误差。

回转半径的情况更细致。副本1在100 ps和200 ps块长下的读数都约为0.00104 nm，看上去已经相近；副本2却从约0.00198 nm继续升到0.00262 nm，副本3也在增加。把三条曲线放在一起，可以看见一个副本上的局部平台未必适用于整个准备方案。回转半径本身变化较小，也可能被局部快速波动包围的缓慢偏移影响。检查同一物理量在不同副本上的一致性，比只看一条平滑曲线更容易发现这种情况。

块越长、误差估计越大并不是必须遵守的数学定律。有限块数带来的随机变化可以让某个点下降，负相关过程也可能表现不同。我们关心的是有物理依据的一段稳定范围：块长已经足够覆盖主要联系，仍保留足够多的块，并且不同观察窗口或副本给出相容的结果。若曲线在最后两个点偶然相交，就回到各块均值，看看是不是少数块控制了估计。分块图的作用，是让这些条件能够被看见和检查。

本节采用固定块长直接划分1000个记录，没有强制数据长度必须是2的整数次幂。这样可以比较1、2、5、10、20、25、50、100和200 ps，所有读数都被保留。1989年的逐级合并方法与这种等长分块共享处理相关性的思想，但具体切分与误差估计细节可以不同。GROMACS的gmx analyze也提供分块分析，并可进一步拟合相关时间模型；这里把直接计算写成完整Python，使每一步使用的帧数、分母和块长都能够在公式与结果之间逐项对应。

## 三条轨迹之间的差异，怎样进入结论

副本比较先把每条轨迹压缩为一个定义相同的平均值，再观察这几个平均值之间的差异。这个顺序与把所有帧直接拼在一起不同：前者明确把“一次独立随机实现”当作统计单位，后者若忘记帧之间的相关性，很容易得到过窄的误差。对于长度相同、同一窗口的三个副本，先分别平均再等权平均，与把所有数值等权求总平均得到相同的中心；差别主要出现在我们怎样描述这个中心的不确定性。

以一条随机副本为重复单位式 4

![以一条随机副本为重复单位](https://ml-biomat.com/static/agent-math/bad2ee064032fe065635554e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Aᵣ | 第r个副本在相同窗口内的平均观测量 | nm |
| Ā | 各副本均值的等权平均 | nm |
| Q, r | 副本数与编号；本例Q=3 | 1 |
| s_{rep} | 副本均值之间的样本标准差 | nm |
| SE_{rep} | 以随机副本为独立单位估计的均值标准误差 | nm |
| (Aᵣ−Ā)² | 一个副本均值偏离总平均的平方 | nm² |
| Σ, /, −, +, = | 按指定编号求和、除法、减法、加法与定义等号；相邻量相乘 | 运算符无单位 |
| √, rep | 非负平方根；rep下标标记副本间统计 | 运算符与标签无单位 |

怎样理解先让每条等长分支提供一个平均值，再以分支间变化衡量重新开始后的差异。

算一个例子本例Rg均值约1.191521、1.187855、1.184757 nm；总平均1.188044 nm，s_rep=0.003386 nm，SE_rep=0.001955 nm。

使用条件描述共同准备坐标与规定短时间协议下的独立随机实现；共享起点和模型假设保留为共同条件。

三个回转半径均值的总平均约为1.18804 nm，副本均值之间的样本标准差约为0.00339 nm。如果将这三条具有独立随机数的、相同长度的分支作为重复单位，均值标准误差为0.00339除以√3，约0.00195 nm。这个数的对象是从同一份准备坐标出发、按照当前短时间协议得到的平均值。各分支共享的初始构象、力场选择及未探索的其他构象区域，仍然是共同条件。扩大这些条件的覆盖，需要新的起始状态和更长的结构采样。

### 前后窗口与副本之间的平均值

三角形分别表示前、后500个读数的均值，圆点为1000个读数的全段均值；连线帮助辨认同一副本。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s7)

三角形分别表示0≤t<500 ps与500≤t<1000 ps的均值，圆点表示完整1000条记录的均值，线段连接前后两个窗口。它们呈现时间窗口与独立随机历史带来的差别；图中标记表示窗口平均值。

窗口比较把副本差异与各自的时间变化联系起来。副本1的RMSD在前500 ps平均约0.11445 nm，后500 ps约0.17309 nm；副本2相应为0.11135和0.13834 nm；副本3为0.17679和0.21434 nm。三条分支在后段都具有较高的平均偏离，说明共同参考附近的早期调整仍影响整段统计。与此相比，副本2的回转半径从前段约1.19242 nm降到后段约1.18329 nm，显示它的总体尺寸也经历了变化。原始轨迹、窗口均值和分块诊断在这里指向了可以进一步观察的具体过程。

这些结果可以组织成一个明确的后续计算方案。先延长现有三条分支，保持模型与测量定义，观察RMSD、回转半径和局部结构量在后续窗口中的变化；再选择相隔足够远、结构上有区别的构象准备新的重复，用来检验共同起点的影响。若研究目标是某个结合口袋，就增加口袋相关的距离或接触指标，让采样判断针对功能问题。一个整体尺寸读数即使已经平稳，局部开闭也可能具有自己的慢时间尺度。

不确定性的范围也要与科学问题匹配。改变随机种子主要调查热运动与有限时间采样；改变力场或质子化状态调查模型假设；改变积分时间步调查数值近似。三种比较的横轴不同，得到的差异也应分别说明。研究报告可以先写在给定模型与条件下测到了什么，再说明副本间的变化和所选时间窗口，最后把模型比较放在对应的实验设计里。这样，读者能沿着具体条件理解结论，并知道下一次计算会增加哪一类信息。

对生物大分子而言，真实环境还包括溶液组成、温度、相互作用伙伴以及可能发生的化学过程。当前固定连接的经典模型描述给定化学身份下的构象运动，反应、质子转移或键断裂需要相应的扩展模型。把统计误差估计得更精细，会改进对当前模型平均行为的认识；与实验功能建立联系时，继续检查实验观测量与模拟定义是否对应。采样设计与模型设计共同决定一条曲线最终能回答多大的问题。

## 让保存频率、运行时长和重复各有任务

最后用一个可控制的相关模型，把保存频率的影响单独拿出来。设某个长度读数围绕固定平均值波动，标准差为0.01 nm，两个时刻的相关性随时间间隔按指数衰减。相关时间τc表示这条指数曲线降到起始值约37%所需的时间。这里的模型只描述读数的统计联系，帮助我们计算同样长的观察时间里，更密的记录会带来多少新增信息。它的平均状态和相关规律预先给定，因此可以直接算出均值方差。

固定观察时长下的指数相关模型式 5

![固定观察时长下的指数相关模型](https://ml-biomat.com/static/agent-math/0e3191cbd6d77715042820ff.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| C(k) | 指数模型中相隔k格的相关系数 | 1 |
| δt, τc | 保存间隔与指数相关时间；τc>0时使用所示指数式 | ps |
| N, k | 记录数与间隔格数；本交互Nδt=500 ps | 1 |
| e | 自然指数函数的底数，约2.71828 | 1 |
| g_{N} | 相关性造成的均值方差倍率 | 1 |
| N_{eff} | 对均值方差具有等效贡献的独立记录数，可为非整数 | 1 |
| σₓ, SE | 单个读数的标准差与模型下均值的标准误差 | nm |
| 1−k/N, 2 | 有限记录的配对权重与两个时间方向的贡献 | 1 |
| Σ, /, −, +, = | 按指定编号求和、除法、减法、加法与定义等号；相邻量相乘 | 运算符无单位 |
| √, −kδt/τc | 非负平方根；指数中的比值为无量纲时间间隔 | 运算符与指数无单位 |

怎样理解平均值方差累积所有观察对的协方差；同一间隔有N−k对，两个时间方向给系数2。

算一个例子τc=20 ps、δt=1 ps、N=500、σₓ=0.01 nm时，gN=38.40867，N_eff=13.01790，SE=0.00277159 nm。

使用条件恒定平均、恒定方差、已知指数相关的解析统计模型。τc=0选项采用独立极限C(k>0)=0；真实轨迹需检验其相关规律。

公式中每个间隔的贡献前面有1−k/N，是因为相隔k格的配对只有N−k组。把正、负两个时间方向的等价贡献合在一起，得到前面的系数2；零间隔的自身方差则形成开头的1。所有间隔贡献合并为gN后，均值方差等于单个读数方差乘gN/N。用N/gN定义等效独立记录数，只是在“对平均值方差有同样贡献”的意义下换一把计数尺子，它可以不是整数，也不会为实际轨迹增加新的构象。

观察窗口0≤t<500 ps；单个读数标准差σₓ=0.01 nm。调整保存间隔与相关时间，比较原始记录数和等效独立数。

[Figure: 指数相关与有效信息曲线](https://ml-biomat.com/tutorials/molecular-dynamics/g09/#zh-s8)

固定500 ps观察窗口与0.01 nm单帧标准差的解析指数相关模型。保存间隔改变记录数，相关时间控制相邻信息的相似程度。

交互固定观察范围为0≤t<500 ps，你可以改变相关时间和保存间隔。相关时间取20 ps时，将保存间隔从1 ps缩短为0.5 ps，记录数从500增到1000，等效独立数却只发生很小变化，因为新增时刻与原有时刻高度相关。把相关时间设为0，交互采用各次独立的极限，等效独立数才等于记录数。这个对照也说明，独立极限与一条缓慢构象轨迹属于不同的统计条件。真实数据的相关规律需要从足够的观察中估计，不能直接套用交互里的指数假设。

下面的完整分析程序读取三份RMSD和回转半径记录，检查时间是否都以1 ps等间隔覆盖0到1000 ps，再执行本节的窗口、相关和分块计算。它会输出三组图和一个结构化摘要：逐帧及累计曲线、自相关及块长曲线、前后窗口与全段均值。图中文字可以用--language zh切换，数值和筛选条件保持相同。你可以先用配套的参考记录重算，再把同样格式的新轨迹放入三个副本目录，比较延长观察后哪些图发生了变化。

### 完整Python：窗口、相关与分块

```
"""Compare three protein trajectories at fixed measurement definitions.

python analyze_replicas.py --records records --out analysis --language en

Each records/replica-1, replica-2 and replica-3 contains rmsd.xvg and gyrate.xvg.
Dependencies: numpy, matplotlib. Time is ps and both observables are nm.
The plots display 0--1000 ps. Statistics use 0 <= t < 1000 ps: exactly 1000
equally spaced observations, divided into complete, disjoint blocks.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_xvg(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith(("#", "@")):
            rows.append([float(value) for value in text.split()])
    data = np.asarray(rows, dtype=float)
    if data.ndim != 2 or not np.all(np.isfinite(data)):
        raise ValueError(f"Expected finite two-dimensional data in {path.name}")
    return data


def autocorrelation(values, max_lag=200):
    """Pair-count covariance estimate, centered on this record's mean."""
    centered = values - values.mean()
    variance = np.mean(centered**2)
    if variance <= 0:
        raise ValueError("A constant record has no normalized fluctuation ACF")
    return np.array([np.dot(centered[:len(values)-lag], centered[lag:]) /
                     ((len(values)-lag)*variance)
                     for lag in range(max_lag+1)])


def block_estimates(values, block_sizes):
    rows = []
    for size in block_sizes:
        if len(values) % size:
            raise ValueError("Use complete equal-sized blocks for this exercise")
        means = values.reshape(-1, size).mean(axis=1)
        if len(means) < 2:
            raise ValueError("At least two block means are required")
        # This is an estimate based on treating block means as independent.
        # Plot its dependence on size before making that statistical assumption.
        sem = means.std(ddof=1) / np.sqrt(len(means))
        rows.append({"block_records": int(size), "blocks": int(len(means)),
                     "sem_nm": float(sem), "means_nm": means.tolist()})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(cn, en): return cn if zh else en
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in fonts if f in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16, "svg.fonttype": "path",
                         "figure.facecolor": "#faf8f3", "axes.facecolor": "#faf8f3",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.unicode_minus": False})
    colors = ["#167d84", "#be7045", "#4c6dab"]
    names = ["RMSD", "Rg"]
    block_sizes = [1, 2, 5, 10, 20, 25, 50, 100, 200]
    series, summaries, correlations = [], [], []
    reference_time = None
    for number in (1, 2, 3):
        folder = args.records / f"replica-{number}"
        rmsd = read_xvg(folder / "rmsd.xvg")
        gyrate = read_xvg(folder / "gyrate.xvg")
        time = rmsd[:, 0]
        if not (np.array_equal(time, gyrate[:, 0]) and
                np.allclose(time, np.arange(1001), rtol=0, atol=1e-9)):
            raise ValueError("Both measurements must have the same 0--1000 ps grid")
        if reference_time is None:
            reference_time = time.copy()
        if not np.array_equal(time, reference_time):
            raise ValueError("Replica time grids differ")
        values = np.column_stack([rmsd[:, 1], gyrate[:, 1]])
        series.append(values)
        selected = values[:-1]
        record = {"replica": number, "samples": len(selected), "observables": {}}
        acfs = []
        for column, name in enumerate(names):
            data = selected[:, column]
            acfs.append(autocorrelation(data))
            record["observables"][name] = {
                "mean_nm": float(data.mean()), "frame_sd_nm": float(data.std(ddof=1)),
                "independent_frame_sem_nm": float(data.std(ddof=1)/np.sqrt(len(data))),
                "first_half_mean_nm": float(data[:500].mean()),
                "second_half_mean_nm": float(data[500:].mean()),
                "blocks": block_estimates(data, block_sizes)}
        correlations.append(np.array(acfs))
        summaries.append(record)
    series = np.array(series)
    summary = {"window_ps": [0, 1000], "right_endpoint_in_statistics": False,
               "record_interval_ps": 1, "replica_count": 3, "replicas": summaries,
               "replica_mean_summary": {},
               "interpretation": "Finite-window estimates conditional on a common prepared coordinate state. Block-size curves and ACF are sampling diagnostics; block independence is assessed, not imposed by dividing data."}
    for column, name in enumerate(names):
        means = series[:, :-1, column].mean(axis=1)
        summary["replica_mean_summary"][name] = {
            "grand_mean_nm": float(means.mean()), "between_replica_sd_nm": float(means.std(ddof=1)),
            "conditional_sem_nm": float(means.std(ddof=1)/np.sqrt(3))}
    (args.out / "replica_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(args.out / "replica_series.csv", np.column_stack([time, *[x for x in series]]),
               delimiter=",", header="time_ps,r1_RMSD_nm,r1_Rg_nm,r2_RMSD_nm,r2_Rg_nm,r3_RMSD_nm,r3_Rg_nm", comments="")

    def save(fig, basename):
        for extension in ("svg", "png"):
            fig.savefig(args.out / f"{basename}.{extension}", dpi=170, bbox_inches="tight")
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            label = tr(f"副本 {number+1}", f"Replica {number+1}")
            axes[column, 0].plot(time, series[number, :, column], color=color, lw=.8, alpha=.85, label=label)
            running = np.cumsum(series[number, :-1, column])/np.arange(1, 1001)
            axes[column, 1].plot(time[:-1], running, color=color, lw=1.8, label=label)
        axes[column, 0].set(title=tr("逐帧记录", "Frame-by-frame record"), ylabel=f"{name} / nm")
        axes[column, 1].set(title=tr("从生产起点累计的平均", "Mean accumulated from production start"), ylabel=f"{name} / nm")
        for ax in axes[column]:
            ax.set_xlabel(tr("生产时间 / ps", "Production time / ps"))
            ax.set_xlim(0, 1000)
            ax.grid(alpha=.15)
            ax.legend(frameon=False, fontsize=12)
    save(fig, "replica_traces")

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            label = tr(f"副本 {number+1}", f"Replica {number+1}")
            axes[column, 0].plot(np.arange(201), correlations[number][column], color=color, label=label)
            errors = [item["sem_nm"] for item in summaries[number]["observables"][name]["blocks"]]
            axes[column, 1].plot(block_sizes, errors, "o-", color=color, ms=5, label=label)
        axes[column, 0].axhline(0, color="#879896", lw=.8)
        axes[column, 0].set(xlabel=tr("时间间隔 / ps", "Lag / ps"), ylabel="C(k)",
                            title=tr(f"{name} 的中心化自相关", f"Centered autocorrelation of {name}"), xlim=(0, 200))
        axes[column, 1].set(xscale="log", xlabel=tr("每块长度 / ps", "Block duration / ps"),
                            ylabel=tr("按块均值计算的标准误差 / nm", "Block-based standard error / nm"),
                            title=tr(f"{name}：每块 1 至 200 个记录", f"{name}: 1 to 200 records per block"))
        for ax in axes[column]:
            ax.grid(alpha=.15)
            ax.legend(frameon=False, fontsize=12)
    fig.suptitle(tr("0≤t<1000 ps；200 ps一块时仅有5块", "0≤t<1000 ps; a 200 ps block leaves only five blocks"), fontsize=17)
    save(fig, "replica_correlation")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            record = summaries[number]["observables"][name]
            x = number+1
            axes[column].plot([x-.18, x+.18], [record["first_half_mean_nm"], record["second_half_mean_nm"]], color=color, alpha=.7)
            axes[column].scatter(x-.18, record["first_half_mean_nm"], color=color, marker="<", s=90)
            axes[column].scatter(x+.18, record["second_half_mean_nm"], color=color, marker=">", s=90)
            axes[column].scatter(x, record["mean_nm"], color=color, edgecolor="white", s=130, zorder=3)
        axes[column].set(xlim=(.5, 3.5), xticks=[1, 2, 3], xlabel=tr("独立随机副本", "Random realization"),
                         ylabel=f"{name} / nm", title=tr("前段、全段与后段的均值", "First half, full window,\nand second half"))
        axes[column].grid(axis="y", alpha=.15)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color="#445e61", marker=marker, linestyle="None", markersize=9, label=label)
               for marker, label in [("<", "0≤t<500 ps"), ("o", "0≤t<1000 ps"), (">", "500≤t<1000 ps")]]
    fig.legend(handles=handles, loc="outside lower center", ncols=3, frameon=False)
    save(fig, "replica_windows")
    print(json.dumps(summary["replica_mean_summary"], indent=2))


if __name__ == "__main__":
    main()
```

读取三个副本目录下的rmsd.xvg与gyrate.xvg；--language zh或en选择图中文字。

安排下一次模拟时，可以把三个投入分别考虑。增加输出频率用于解析更快的变化；延长每条轨迹用于观察较慢的调整和状态转换；增加独立重复用于比较重新开始后的差异。若已经保存了足够密的轨迹，却发现分块曲线持续上升，优先延长相关结构过程的观察更有针对性。若不同起始构象落在不同区域，就把采样方案扩展到这些区域，并围绕研究指标检查它们之间的交换。预算由希望补充的信息决定，文件越大并不自动意味着问题回答得越完整。

接下来的蛋白与配体、核酸、糖和膜体系都会用到这套判断方式。观察对象从整体尺寸换成一个接触、糖苷扭转角或膜厚时，平均的定义、相关时间和合适的重复单位也会随之改变。保持对象与单位清楚，保留原始时间顺序，用多个窗口和分支观察变化，就能把“看见一条曲线”推进为“知道这条曲线记录了什么”。在这个基础上，新的分子模型和更复杂的采样方法才有明确的比较尺度。

## 延伸阅读与开放资料

- [Molecular dynamics simulation of a small protein using GROMACS](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · GROMACS tutorial contributors · CC BY 4.0

  蛋白质水溶液的准备、生产与RMSD/Rg分析流程。

  使用共同1UBQ模型的三个随机副本，补充等窗口比较、相关性与分块分析。
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  蛋白质水中模拟与结构分析主线、RMSD解释。

  泛素替代原示例蛋白，固定共同参考与测量选择，增加完整统计教学和实际副本比较。
- [gmx analyze — GROMACS 2026.4 documentation](https://manual.gromacs.org/2026.4/onlinehelp/gmx-analyze.html) · GROMACS developers · Official technical reference; command conventions cited

  等间隔记录、自相关和分块误差的定义。

  用独立编写的Python逐项计算显示的公式，展示块长依赖。
- [Error estimates on averages of correlated data](https://doi.org/10.1063/1.457480) · H. Flyvbjerg and H. G. Petersen · Historical research citation; publisher copyright

  1989年相关数据平均误差与分块思想的历史背景。

  以自绘相邻平均图解释统计单位变化。
- [Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations [Article v1.0]](https://doi.org/10.33011/livecoms.1.1.5067) · Alan Grossfield, Paul N. Patrone, Daniel R. Roe, Andrew J. Schultz, Daniel W. Siderius and Daniel M. Zuckerman · Publicly accessible methodological article cited; no article text, code or illustration reproduced

  采样诊断、均值不确定性与共同起点下副本的统计范围。

  结合实际短轨迹，以连续教学文字和新图解说明后续采样设计。
