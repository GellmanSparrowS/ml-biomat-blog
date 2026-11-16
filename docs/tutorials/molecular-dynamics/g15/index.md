# 脂质如何自己排成一层膜

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g15/
Language: zh-CN

把原子细节汇总为化学珠子，观察DSPC的真实自组装，并用叶片面积、密度和取向理解双层结构。

## 一层膜怎样从散开的分子中出现

洗碗时，少量洗涤剂就能让油污更容易分散在水中；细胞则用一层薄薄的脂质膜，把内部环境与外界分开。这两种现象背后都有一类特殊分子：同一个分子的一部分容易接触水，另一部分更适合与油脂一类的环境接触。分子的形状、组成和浓度不同，最终可以形成小团、薄层或包着水的囊泡。理解这种自发组织过程，有助于研究药物载体怎样形成、膜材料怎样保持完整，以及改变脂质组成后结构为什么发生变化。本节从随机放置的脂质开始，观察它们在水珠中聚集，再把形成的膜变成能够逐项测量的研究对象。

这里的脂质叫 DSPC，中文常称二硬脂酰磷脂酰胆碱。先把这个长名字拆开：磷脂酰胆碱描述与水接触的头部，两条硬脂酰尾链各含十八个碳，且没有碳碳双键。头部带有分开的正、负电荷，整分子净电荷为零；尾部主要由碳氢结构组成。两条尾链在水中相互靠近，头部仍能朝向水，于是两排方向相反的脂质可以组成双层。每一排称为一个叶片。把它想成两排伞柄相对、伞面朝外的伞，有助于记住方向；真正的脂质始终在热运动，尾链也比伞柄柔软得多。

“亲水”和“疏水”是对分子与周围环境相互作用的概括。水分子、脂质头部和尾部都参与能量与排列方式的变化。聚集减少了许多尾部与水直接接触的机会，同时改变了水和脂质可以采用的微观排列。我们要考察的是这些贡献共同形成的倾向。粗粒化模型把其中一部分细节汇总进有效相互作用，因此程序无需给每个分子规定一个目的地，也能产生聚集。观察到的结构来自既定模型、温度、组成与初始条件共同作用，模拟盒中也可能出现需要较长时间才能重排的中间形态。

这一例含有 128 个 DSPC 分子和 768 个水珠，总共 2304 个计算粒子。第一阶段在 340 K、目标压力 1 bar 下运行 30 ns，让分散的脂质自行组织；第二阶段把形成的膜转到合适方向，再运行 30 ns，观察膜面积、厚度与尾链取向。340 K 约为 66.85 ℃，是针对这一脂质模型选择的状态条件。后续结果都与这一温度及水化水平联系在一起。两段各保存 301 帧，相邻记录相隔 100 ps；图中的时间指模型实际推进的时间，读图时可以沿着分子位置与统计量相互对照。

我们将依次回答三个问题。首先，怎样在减少原子细节后保留头尾性质与成膜倾向？其次，一张越来越整齐的分子图片，怎样转化成可以复算的结构测量？最后，当两个叶片的分子数恰好不同，面积与厚度该怎样定义？这些问题适合放在同一个例子中学习：建模尺度决定可观察的信息，周期边界决定坐标怎样阅读，分子数和测量方向则决定最后报告的数值。走完这一过程，读者可以根据具体研究目的选择分辨率，并为一个膜体系建立清楚的结构分析流程。

## 从原子到珠子：保留什么，平均什么

上一节的 PEG 模型保留了每个碳、氢和氧，本节换一种看分子的方法。想象查看城市地图：寻找某家店需要街道与门牌，研究跨城交通时则希望先看清城市之间的联系。粗粒化也通过改变分辨率突出某些问题。一个珠子代表一组原子相关的化学片段，其坐标描述这一组的整体位置，原子之间许多快速振动不再逐项出现。这样，模型可以把计算用于更多分子的集体重排。地图的比例尺有明确用途，粗粒化的映射也需要与研究问题相配：这里关心头尾分区与双层组织，使用十二珠脂质模型。

这种思路在脂质模拟中有一条具体的发展线索。2004 年，Marrink、de Vries 和 Mark 发表了面向脂质与表面活性剂的粗粒化模型，把分子的化学片段用少量相互作用类型表示，并展示了脂质自发组成双层的过程。这个问题很有代表性：如果从一开始就摆好膜，容易研究膜怎样波动；若要观察膜怎样形成，就需要给大量分子充分重排的机会。减少细节让后一类问题更容易进入计算范围，也把“怎样保留成膜所需的物理信息”变成参数设计的核心问题。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s2)

图 1 · 脂质粗粒化从片段表示发展到更细的化学类型与尾链参数。2025栏用相同珠数、不同间距示意参数区分；间距未按实际键长比例绘制。

2021 年的 Martini 3 进一步细分了珠子的大小和化学相互作用类型，使同一套框架能够描述更丰富的分子环境。这里的珠子并非按颜色随意指定：不同类型之间的相互作用强弱，需要与化合物在不同环境中的分配等物理信息联系起来。2025 年的脂质参数更新又细化了尾链的映射及成键参数，使只相差两个碳的尾链也能得到区别处理。这段发展说明，粗粒化的改进既涉及减少多少自由度，也涉及怎样让保留下来的自由度表达正确的化学差别。本节采用 Martini 3 的基础非键参数及这一更新中的 DSPC 参数。

十二个珠子分别承担明确角色。NC3 对应带正电的胆碱部分，PO4 对应带负电的磷酸部分；GL1、GL2 描述甘油及连接区域；两条尾链分别用 C1A 到 C4A、C1B 到 C4B 表示。字母 A、B 区分两条尾，数字沿着尾链排列。珠子名称用于识别分子位置，珠子类型则用于查相互作用参数，这两个字段各有用途。一个名为 C1A 的珠子在当前 DSPC 拓扑中使用 C1 类型，读文件时要看清它位于哪一列。连线表示粗粒化片段之间的连接关系，其长度和弹性参数与原子模型中的单根碳碳键不同。

水的表示也一起改变。这里一个 W 珠对应四个水分子的粗粒化描述，768 个水珠对应的名义水分子数是 3072，平均每个脂质对应 24 个水分子。这个计数说明体系的整体水化水平；它并没有把四个可独立追踪的水分子藏在珠子内部。因此，前面原子水模型中的 O—H 方向、氢键角度及单个水分子的转动，在这里需要换成与粗粒化分辨率一致的问题。我们可以计算水珠在膜两侧的分布，研究水相和尾链区域怎样分开。若研究目标是具体氢键寿命，就应回到能表达氢位置与方向的模型。

数珠子，也数它们对应的组成式 1

![数珠子，也数它们对应的组成](https://ml-biomat.com/static/agent-math/10d931ff75583216629feae3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Nbead | 计算粒子总数 | 1 |
| NL | DSPC分子数，本例128 | 1 |
| NW | W水珠数，本例768 | 1 |
| Nwater | 映射对应的名义水分子数 | 1 |
| h | 每个脂质对应的名义水分子数 | 1 |
| 12, 4 | 每脂质12珠、每W对应4个水分子 | 1 |
| =, +, ×, / | 相等、相加、相乘、相除；相邻符号表示相乘 | 1 |

怎样理解分别按模型的脂质与水映射计数，再用水分子数除以脂质数得到整体水化水平。

算一个例子12×128+768=2304珠；4×768=3072个名义水分子；3072/128=24个水分子/脂质。

使用条件适用于本例十二珠DSPC和四水映射W；映射水数用于组成统计。

## 让参数文件与分子组成相互对应

准备体系时，先把“四份参数文件分别做什么”理清。基础文件定义珠子类型及非键相互作用；成键参数文件给出脂质连接所需的常数；磷脂酰胆碱文件列出 DSPC 的十二个珠子及连接；溶剂文件定义 W。系统拓扑依次包含这些内容，再写明 DSPC 有 128 个、W 有 768 个。这个顺序像先准备字典和语法，再写出完整句子：分子使用的类型和参数必须已经定义。下载包中的同组文件共同构成本例模型，文件名中的 v2 指脂质参数修订，与 Martini 3 的基础版本编号分别管理。

### DSPC体系拓扑

```
#include "martini_v3.0.0.itp"
#include "martini_v3.0.0_ffbonded_v2.itp"
#include "martini_v3.0.0_phospholipids_PC_v2.itp"
#include "martini_v3.0.0_solvents_v1.itp"

[ system ]
DSPC BILAYER SELF-ASSEMBLY

[ molecules ]
DSPC 128
W    768
```

同组四份ITP先定义模型，molecules段按坐标顺序列出128个DSPC与768个W。

初始单分子坐标与力场参数承担不同任务。坐标给出十二个点开始放在哪里，拓扑决定这些点代表什么、怎样相互作用。本例使用与官方流程一致的十二珠起始几何，并把残基名写为 DSPC；实际运行采用 DSPC 的尾链参数。DPPC 与 DSPC 在这套表示中都能使用十二珠几何起点，但它们的化学尾长及相应参数有区别。由此也能理解，修改坐标文件中的名字只是文件准备的一部分，模型身份最终由拓扑中的类型、连接、键长及角度共同决定。查看初始外形时，应同时核对参数所描述的分子。

随机插入把 128 份单分子放进边长 7.5 nm 的立方盒。插入程序尝试不同位置和方向，并用几何距离避免明显重叠；固定随机种子使这一步有可复查的起点。随后加入最多 768 个水珠。这里的初始盒较大，而水珠数量按脂质数限定，最初可以看到尚未被水均匀填满的区域。能量最小化及压力耦合会继续调整接触与盒体积。这是一种低水化自组装设置，水量本身就会影响聚集形态。比较另一种含水量时，应把它视为新的物理条件，并重新检查结构随时间的发展。

三份 MDP 参数把几何松弛、自组装和膜的后续调整分开。最小化采用最陡下降，最多 10000 步，力阈值为 100 kJ mol⁻¹ nm⁻¹；它消除不利接触，不给这段优化编号赋予动力学时间。两个运动阶段的时间步为 0.02 ps，也就是 20 fs，每段 1500000 步，合计各 30000 ps。粗粒化减少了许多快速原子振动，使这个时间步与所选模型相容；该数值应与整套参数共同使用。把它直接移植到前面的全原子 PEG 或蛋白质模型，会改变数值积分所面对的最快运动尺度。

### 写出三份完整MDP

```
"""Write the three full parameter files used for DSPC assembly and relaxation."""
from pathlib import Path
import argparse

FILES = {
'em.mdp': """integrator = steep
nsteps = 10000
nstxout = 0
nstvout = 0
nstfout = 0
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 20
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
emtol = 100
emstep = 0.01
""",
'assembly.mdp': """integrator = md
dt = 0.02
nsteps = 1500000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 1000
nstxout-compressed = 5000
compressed-x-precision = 100
compressed-x-grps = 
energygrps = System
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 5
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 340
gen-vel = yes
gen-temp = 340
gen-seed = 20261501
pcoupl = c-rescale
pcoupltype = isotropic
tau-p = 4.0
ref-p = 1.0
compressibility = 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261502
""",
'bilayer.mdp': """integrator = md
dt = 0.02
nsteps = 1500000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 1000
nstxout-compressed = 5000
compressed-x-precision = 100
compressed-x-grps = 
energygrps = System
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 5
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 340
gen-vel = no
gen-temp = 340
gen-seed = 20261501
pcoupl = c-rescale
pcoupltype = semiisotropic
tau-p = 4.0
ref-p = 1.0 1.0
compressibility = 3e-4 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261503
continuation = yes
""",
}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("."))
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        (args.out/name).write_text(content, encoding="utf-8", newline="\n")
    print("Wrote em.mdp, assembly.mdp, and bilayer.mdp")
```

运行python write_parameters.py，生成最小化、自组装和后续膜阶段的全部参数。

非键相互作用也随模型一起变化。本例使用反应场静电、相对介电常数 15 和 1.1 nm 截断，反应场外部采用导电极限；范德华项也在 1.1 nm 处理，并按文件设定平移势能。温度由 v-rescale 调节，压力由 C-rescale 调节；本例把全部粒子作为一个温控组。对于更大的膜体系，分别检查膜与水相的温度和整体漂移，有助于判断是否需要按相组织温控与质心运动处理。压力耦合每 5 步更新，时间常数为 4 ps；这一组合满足当前积分设置的要求。完整参数让每项选择都能与实际输入对应。

## 观察自组装：从位置变化找到共同方向

先在含有初始坐标、拓扑和参数的自组装目录运行下面的脚本。程序完成插入、溶剂化、最小化和 30 ns 运动，并导出温度、势能、压力、体积及盒长。每一步都使用上一步实际生成的文件：最小化的末态成为运动的初态，运行参数与拓扑则在 grompp 中合并成 TPR。输出前缀 assembly 把这一阶段的文件放在一起。读者可以从保存的轨迹开始重做分析，也可以按照同样流程生成新的记录；固定输入与种子规定起点，后续浮点运算和并行方式仍可能使逐帧运动细节发生分离。

### 随机插入并运行自组装

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" insert-molecules -ci DSPC-em.gro -box 7.5 7.5 7.5 -nmol 128 -radius 0.21 -try 500 -seed 20261500 -o lipids.gro > insert.log 2>&1
"$gmx" solvate -cp lipids.gro -cs water.gro -o solvated.gro -maxsol 768 -radius 0.21 > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f assembly.mdp -c em.gro -p topol.top -o assembly.tpr > assembly.grompp.log 2>&1
"$gmx" mdrun -deffnm assembly -ntmpi 1 -ntomp 2 -pin off > assembly.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f assembly.edr -o assembly-properties.xvg > energy.log 2>&1
"$gmx" check -f assembly.xtc > trajectory-check.log 2>&1
```

在自组装输入目录执行bash run_assembly.sh；所有输入文件放在同一目录。

实际快照中，蓝绿色点是磷酸头基，金色点是尾珠，浅蓝色点是水珠。每幅图把三维位置投影到 xy 平面，并把粒子映回当前盒内，因此视野的范围随盒长变化。开始时三类粒子分散混合，后来头基逐渐形成两条带状分布，尾部与水分占据不同区域。在 30 ns 图中，尾珠出现在盒的上方和下方；沿周期边界把两边接起来，它们属于同一片膜的内部。两条头基带之间显眼的浅蓝区域则是水层。这个例子很适合练习周期图像阅读：图中间的空隙未必就是膜中央。

### 从散开到分层的四幅快照

0、5、15、30ns的实际xy投影；PO4蓝绿、全部尾珠金色、W浅蓝。所有点映回各自周期盒，GL/NC3未画出。

128个Martini 3 DSPC、768个W珠，340 K、1 bar；先各向同性自组装30 ns，再旋转全部坐标与速度，将膜法向转至z，随后半各向同性采样30 ns。采用脂质PC/bonded v2参数。

[下载参考数据与完整输入（ZIP） 5.97 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dspc-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s4)

0、5、15、30 ns原生坐标的xy投影。蓝绿为PO4、金色为尾珠、浅蓝为W；逐珠映入各自周期盒，未画NC3和GL。

为了测量是否出现共同朝向，我们给每个脂质定义一个方向：从两个末端尾珠的中点，指向它的 PO4 头基，再把向量长度归一为一。归一化只保留方向，使较长的脂质不会因为长度更大就获得更高权重。膜两侧的脂质方向相反，但它们都沿着同一根法线排列。如果简单把这些箭头相加，两侧会互相抵消。更合适的办法是比较方向的平方投影：朝上与朝下对同一轴具有相同的贡献，而横躺的方向贡献较小。

寻找脂质共同排列的轴式 2

![寻找脂质共同排列的轴](https://ml-biomat.com/static/agent-math/bc3925c0d735aae09e536b9a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i, NL | 脂质编号与脂质总数 | 1 |
| a, b | x、y、z坐标分量的编号 | 1 |
| uᵢ,ₐ, uᵢ,ᵦ | 脂质尾端中点指向PO4的单位向量分量 | 1 |
| δₐᵦ | a=b时为1，否则为0 | 1 |
| Qₐᵦ, Q | 取向矩阵的元素及整个三乘三矩阵 | 1 |
| S, λmax(Q) | 矩阵最大特征值，即最强共同轴的取向度 | 1 |
| Σ, 1/NL | 对脂质求和并除以分子数，形成等权平均 | 1 |
| 3/2, 1/2 | 使完美轴向排列为1、各向同性极限为0的常数 | 1 |
| =, −, ×, /, max | 相等、相减、相乘、相除、取最大值 | 1 |

怎样理解用分量乘积保留正反同轴排列的信息。最大特征值对应平方投影最集中的方向。

算一个例子若所有方向为±z，Q对角元为−0.5、−0.5、1，S=1；三维各向同性极限的Q为零矩阵。

使用条件逐帧以完整脂质的头尾方向计算；S描述共同朝向，形态还结合空间分布判断。有限样本的各向同性S会有波动。

公式中的矩阵可以理解为“把三个坐标方向两两组合起来，收集所有脂质的朝向信息”。求它的最大特征值，就是找出使平方投影最集中的那根轴，并记录集中程度 S。刚开始分子朝向较散，有限的 128 个分子仍会产生一定的随机偏向；聚集后 S 明显增加。本次记录在约 9 ns 后进入接近 0.8 的取向区间，30 ns 时为 0.799。对应主轴的绝对分量约为 0.028、0.9995、0.012，说明共同方向几乎沿 y。主轴的正负号描述同一根轴，因此图中画的是三个分量的绝对值。

### 整体朝向与主轴

301帧；尾端中点到PO4的单位方向定义取向矩阵。轴的正负等价，图中画绝对分量。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s4)

301帧的整体取向矩阵最大特征值，以及对应主轴的绝对分量；方向按尾端中点指向PO4定义，主轴正负等价。

取向曲线把肉眼观察变成了可重复的测量，但结构身份还需要空间信息配合。许多细长分子平行排列，也可能形成别的聚集体；两条头基层、尾部连续区域以及水相的位置共同支持这里的双层判断。图像与曲线各自回答一部分问题：快照给出在哪里，取向统计给出排列得多一致。下一步还要允许膜在横向和法向上分别调整尺寸。若只在第一阶段结束后量一次面积，就会把刚形成的结构与它仍在进行的尺寸松弛混在一起。

## 把膜转正，让横向面积能够独立调整

形成膜以后，空间中的三个方向开始承担不同角色。沿膜面移动，主要遇到同一层脂质；穿过膜的方向，则依次经过水、头基、尾链和另一侧头基。初始自组装采用各向同性压力耦合，三个盒长使用同一个缩放因子。对于已经形成的膜，更自然的选择是让膜内两个方向共同缩放，而让法向使用另一组缩放。这叫半各向同性压力耦合。它给横向面积与法向厚度留下不同的调整自由度，适合研究膜在给定温度和压力条件下怎样改变形状。

GROMACS 在这里把 xy 看作膜面、z 看作法向，因此需要先处理本次沿 y 形成的膜。下面的程序对全部粒子作同一个刚体旋转，把坐标变为 x、Lz−z、y，速度相应变为 vx、−vz、vy，盒长交换 y 与 z 的位置。整体平移使坐标仍便于放在盒内，旋转本身保持所有距离和速率。这相当于把装着膜的透明盒转过四分之一圈。原先靠近 y 轴的法线现在靠近 z 轴，分子之间的相对结构保持一致，接下来的压力设置就能对应正确方向。

### 旋转全部坐标与速度

```
"""Rotate the recorded y-normal DSPC bilayer, retaining its velocities.

python rotate_bilayer.py --source assembly/assembly.gro --out bilayer/start.gro
The mapped box is orthorhombic: (x,y,z) becomes (x,Lz-z,y).
"""
from pathlib import Path
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("assembly/assembly.gro"))
    parser.add_argument("--out", type=Path, default=Path("bilayer/start.gro"))
    args = parser.parse_args()
    lines = args.source.read_text().splitlines()
    count = int(lines[1]); atoms = lines[2:2+count]
    box = np.array([float(x) for x in lines[2+count].split()])
    if count != 2304 or len(box) != 3:
        raise ValueError("Expected 2304 beads in the recorded orthorhombic box")
    if any(len(line) < 68 for line in atoms):
        raise ValueError("The source must contain all three velocity components")
    xyz = np.array([[float(line[20+8*k:28+8*k]) for k in range(3)] for line in atoms])
    velocity = np.array([[float(line[44+8*k:52+8*k]) for k in range(3)] for line in atoms])
    transformed = xyz[:, [0, 2, 1]].copy(); transformed[:, 1] = box[2]-transformed[:, 1]
    vnew = velocity[:, [0, 2, 1]].copy(); vnew[:, 1] *= -1
    if not np.allclose(np.sum(vnew*vnew, axis=1), np.sum(velocity*velocity, axis=1)):
        raise ValueError("The rotation changed a bead speed")
    output = ["DSPC bilayer, membrane normal rotated from y to z", lines[1]]
    output += [line[:20]+"".join(f"{v:8.3f}" for v in pos)+"".join(f"{v:8.4f}" for v in vel)
               for line, pos, vel in zip(atoms, transformed, vnew)]
    output += [" ".join(f"{v:10.5f}" for v in box[[0, 2, 1]])]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(output)+"\n", encoding="utf-8", newline="\n")
    print("Rotated 2304 positions and velocities; all bead speeds preserved.")


if __name__ == "__main__":
    main()
```

python rotate_bilayer.py --source assembly/assembly.gro --out bilayer/start.gro。

第二阶段使用旋转后的坐标和速度，设置 gen-vel=no，避免重新抽取一组初速度。温度和压力耦合器则从新阶段重新初始化；这一操作改变的是后续调节条件。准备一个单独的膜目录，放入 start.gro、bilayer.mdp、同组拓扑及 ITP 文件，再运行后续脚本。它仍使用 340 K、20 fs 步长与 30 ns 时长，只把压力耦合改为半各向同性，平面与法向的目标压力都设为 1 bar。两段时间轴分别从各自阶段的零时刻开始，读图时应区分自组装的 30 ns 与后续的 30 ns。

### 运行半各向同性后续阶段

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f bilayer.mdp -c start.gro -p topol.top -o bilayer.tpr > bilayer.grompp.log 2>&1
"$gmx" mdrun -deffnm bilayer -ntmpi 1 -ntomp 2 -pin off > bilayer.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f bilayer.edr -o bilayer-properties.xvg > energy.log 2>&1
"$gmx" check -f bilayer.xtc > trajectory-check.log 2>&1
```

在膜目录中放入start.gro、bilayer.mdp、topol.top与四份ITP，然后执行bash run_bilayer.sh。

给平面与法向相同目标压力，相当于选择没有外加平面—法向压力差的条件。有限体系里的瞬时压力仍会波动，两个叶片也可能有不同的内部应力。尤其本例自组装后，一侧有 66 个脂质，另一侧有 62 个；调节盒面积不会自动把两个叶片变成一样多。脂质从一侧翻到另一侧，需要头部穿过不利的膜内环境，属于另一种重排过程。这里保存的后续帧中叶片身份保持不变，因此面积分析将沿用这组实际成员数，同时把它作为体系状态的一部分保留。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s5)

图 2 · 头部朝外、尾部朝内的双层侧视示意。标注66/62为本例实际叶片计数；圆点按概念示意抽样绘制。面积是垂直于z观察时的投影面积。

半各向同性记录仍有起伏，这些起伏包含膜和盒形状随时间的调整。我们统一取第二阶段 15–30 ns 的 151 帧作为本节的结构统计窗口，并同时展示整段曲线，让读者看到窗口前后发生了什么。这个选择使各测量共享同一批记录；窗口长度、帧间隔和两叶片组成也都可以明确复查。若以后要比较不同温度、含水量或脂质类型，应对每个体系检查尺寸调整所需时间，再用一致定义比较相应阶段的分布与平均值。

## 一片膜，两种每脂质面积

从正上方看一片平面膜，盒的 x 长度乘以 y 长度就是它的投影面积。想象两层书架在同一块地面上投下影子：两层各自覆盖相同地面面积，但每层放的书数可以不同。膜的两个叶片也是这样，因此平均每个脂质分到的投影面积，要分别除以该叶片的分子数。把 128 除以二得到 64，是在假定两侧恰好对半分；本次结构的实际计数是 66 和 62。共同的面积分子配上两个真实的分母，才能描述这片膜的两侧。

每个叶片使用自己的分子数式 3

![每个叶片使用自己的分子数](https://ml-biomat.com/static/agent-math/e8854a3a726d249227fd94d3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Lx, Ly | 膜面内正交盒边长 | nm |
| A | 膜的投影面积 | nm² |
| N+, N− | 正z、负z叶片的固定成员数66与62 | 1 |
| a+, a− | 两个叶片各自的平均每脂质投影面积 | nm² |
| +, − | 下标用于区分叶片朝向 | 1 |
| =, +, ×, / | 相等、相加、相乘、相除；相邻符号表示相乘 | 1 |

怎样理解两个叶片共享盒的投影面积，按各自分子数分配得到不同的平均面积。

算一个例子A=38.4734 nm²时，a+=38.4734/66≈0.58293 nm²，a−=38.4734/62≈0.62054 nm²。

使用条件用于平面膜的投影面积；局部分子面积与曲面真实面积需要另外定义。

后 15 ns 的平均投影面积为 38.473 nm²。除以 66，得到朝向正 z 一侧的 0.583 nm²；除以 62，得到另一侧的 0.621 nm²。两条面积曲线同步升降，因为它们共享每一帧的盒面积，差别来自固定分母。相应的逐帧标准差约为 0.022 和 0.024 nm²，反映这一段记录中的波动。这里的“每脂质面积”是叶片总面积的平均分配量，单个分子并没有被划进一个边界固定的小方格。若要研究局部拥挤程度，需要进一步定义每个分子周围的面积划分方法。

### 叶片面积、磷酸面间距与整体取向

两叶片固定66/62成员；浅色标出15–30ns的151帧统计窗口。

128个Martini 3 DSPC、768个W珠，340 K、1 bar；先各向同性自组装30 ns，再旋转全部坐标与速度，将膜法向转至z，随后半各向同性采样30 ns。采用脂质PC/bonded v2参数。

[下载参考数据与完整输入（ZIP） 5.97 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dspc-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s6)

旋转后的30 ns采样：按66/62固定成员分别计算的每脂质投影面积、两PO4面的距离和整体取向。15–30 ns包含151个保存时刻。

膜厚度同样需要先说明尺子放在哪里。本节使用两侧 PO4 珠平均位置的间距。程序先根据尾链末端找到膜内部的周期中面，再把两侧头基坐标放到这个中面的两边，最后分别平均并相减。这个步骤解决了前面快照中的周期接缝问题：头基层之间沿盒内直线较短的间隔可能是水层，直接选择那个间隔会量错对象。通过尾部定位膜内部，再沿已知法向量两侧头基，测量才能跟随同一片膜，而不会在它跨越盒边时忽然改变含义。

在膜内部两侧量头基平面式 4

![在膜内部两侧量头基平面](https://ml-biomat.com/static/agent-math/d32f0d6867dbb3521dbef182.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dPP | 两叶片PO4平均平面间距 | nm |
| zᵢ, zⱼ | 以周期尾端中面为零点展开后的PO4法向坐标 | nm |
| i, j | 两个叶片中的脂质编号 | 1 |
| N+, N− | 两个叶片的成员数66和62 | 1 |
| Σ, ∈, +, − | 按指定叶片求和、属于；求和下标+和−标叶片，中央−为相减 | 1 |
| =, / | 相等与相除；求和除以成员数形成平均 | 1 |

怎样理解分别求两侧平均坐标，再取两者之差。先以尾端中面处理周期坐标，保证距离穿过膜内部。

算一个例子两侧平均坐标若为+2.1和−2.2 nm，则dPP=2.1−(−2.2)=4.3 nm。

使用条件本例近似平面膜、固定叶片成员、法向z；它是PO4平面间距。

本次统计得到的平均磷酸面间距为 4.321 nm，逐帧标准差为 0.122 nm。在曲线上，面积较大的区段常伴随较小的头基间距，这与脂质在横向展开时尾链区域变薄的几何直觉相符；分子的倾斜、尾链弯曲和水化也同时参与变化。若将这两个量用于定量关系，就需要分析它们的联合分布与时间相关性。单凭两条曲线外形相似，不能把膜的全部变形简化成某一种固定体积机制；本节把它们作为相互联系、定义清楚的两个结构测量。

“厚度”在实验和模拟中可能指不同位置之间的距离，例如头基密度峰间距、疏水核心厚度或由散射模型拟合得到的结构尺度。与实验比较时，应先问实验方法对哪些物质敏感，再构造相匹配的模拟观测量。这里的 PO4 珠平均平面很适合跟踪同一模型随条件的变化，接下来的珠数密度剖面则把它扩展为整张空间分布图。这样，两个平均位置之外的信息也能保留下来，包括头基层的宽度、尾部区域与水相的过渡，以及膜的整体平移怎样被消除。

## 用密度和取向读懂膜的内部

密度剖面的做法类似把一条长走廊切成等宽的小段，再数每一段里有多少人。沿膜法向，把空间分成宽 0.1 nm 的薄片；每片的体积是当前膜面积乘以片厚，粒子数除以这个体积就得到珠数密度。我们分别统计 PO4、全部尾珠和 W，并在每一帧按尾端中面居中，再平均后 15 ns 的结果。这样得到的横坐标始终以膜内部为零点，整体漂移不会把两侧头基峰涂抹开。体积随压力调节变化，因此每帧使用自己的面积归一化。

数目除以薄片体积，再对帧平均式 5

![数目除以薄片体积，再对帧平均](https://ml-biomat.com/static/agent-math/9e894015e70b4cb954e7f164.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| k, f, F | 薄片编号、帧编号与统计帧数151 | 1 |
| nₖ, f | 帧f的第k片中选定种类的珠数 | 1 |
| Af | 该帧膜面投影面积 | nm² |
| Δz | 薄片宽度，本例0.1 | nm |
| AfΔz | 该帧该薄片的体积 | nm³ |
| ρ̄ₖ | 平均珠数密度 | nm⁻³ |
| Σ, 1/F, =, /, × | 逐帧求和、帧平均、相等、相除、相乘 | 1 |

怎样理解每帧先除以真实薄片体积，再平均，保留压力调节下的面积变化。

算一个例子面积40 nm²、片厚0.1 nm、片内有8珠时，密度为8/(40×0.1)=2 nm⁻³。

使用条件分别数PO4、全部尾珠或W；坐标先居中。对z积分得到平均的珠数/面积，W按珠计数。

剖面中央以尾珠为主，两侧出现 PO4 的峰，水珠主要分布在更外侧；这种层次与双层结构的化学组成一致。三条曲线的高度同时受到空间聚集程度与所数珠子总数影响。每个脂质有一个 PO4，却有八个尾珠，因此尾珠曲线覆盖的总面积自然更大。沿 z 对珠数密度积分，得到的是每单位投影面积上的珠子数，程序用这个关系检查计数与归一化。W 曲线使用水珠数；换算名义水分子数密度时还要乘以四，而讨论电子密度或质量密度时则应使用各自对应的权重。

### 膜内的珠数密度与尾链取向

后15ns，以周期尾端中面居中。密度单位nm⁻³，P₂误差棒为逐帧分子平均值的样本标准差。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s7)

后15 ns相对于周期尾端中面的珠数密度，以及六种尾链相邻珠连接的P₂。误差棒为逐帧分子平均值的样本标准差；连接取向与整体分子轴的特征值分别定义。

尾链取向提供另一种内部结构信息。取相邻两个尾珠的连线，计算它与 z 法线的夹角，再将这个角变成 P₂。沿法线正向或反向的键都得到 1，完全平行于膜面的键得到 −0.5。对于三维各向同性分布，平方余弦的平均值是三分之一，P₂ 的平均值于是为零。这里先计算每一根键的平方余弦，再对分子和记录求平均。把所有角度先平均后再取余弦平方，会得到不同的量，特别是两个叶片的方向相反时，这种差别会非常明显。

先求每根键的平方投影，再平均式 6

![先求每根键的平方投影，再平均](https://ml-biomat.com/static/agent-math/fd8cee8e4e7ddfbb77f3af22.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| P₂ | 相对于膜法线的二阶取向参数 | 1 |
| θ | 粗粒化尾链键向量与+z法线夹角 | ° |
| b, bz | 连接相邻尾珠的向量及其z分量 | nm |
| ‖b‖ | 该向量的长度 | nm |
| cos θ, cos² θ | 长度比形成的余弦及其平方 | 1 |
| ⟨·⟩ | 先逐根计算，再在指定分子与帧上平均 | 1 |
| 3, 1, 2 | 设定取向刻度的无量纲常数 | 1 |
| =, −, /, ², ‖·‖ | 相等、相减、相除、平方、取向量长度 | 1 |

怎样理解平方让正反方向贡献相同；三维各向同性时平均平方余弦为1/3，减去1并除2使该极限为0。

算一个例子0°与180°都给1；90°给−0.5。两根0°和180°方向的平均P₂为1，虽然它们的平均角是90°。

使用条件本节对六种尾链连接分别计算，以z为膜法线；先平均角度会改变测量定义。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s7)

图 3 · 0°与180°同样沿膜法线，P₂都为1；90°位于膜面内，P₂为−0.5。三维各向同性时平均P₂为0。

本例两条尾链靠近连接区的 C1—C2 键，P₂ 平均值分别约为 0.571 和 0.597；末端 C3—C4 键则约为 0.432 和 0.430。末端较低的取向表明它们对法线的平方投影更分散，与尾链末端拥有较多弯折自由度的图像相呼应。图上的误差棒是每帧对 128 个分子平均后，151 个帧均值之间的标准差。它描述记录中的波动，时间相关性还会影响平均值的不确定度。这里的局部尾链 P₂ 与前面整个脂质方向的 S 使用了不同向量，比较时应分别保留各自定义。

四根等权方向的几何算例：比较先计算后平均与先平均角度。

[Figure: 四个方向与膜法线的夹角](https://ml-biomat.com/tutorials/molecular-dynamics/g15/#zh-s7)

虚线为膜面、竖线为法线。每根向量等权；0°和180°同轴，平方投影相同。

交互把四根等权方向放在同一个平面中，方便看清平均次序。选择“同角度”时四根方向相同；选择“上下对称”时，一半为 θ，另一半为 180°−θ。把角度调到零，上下对称的四根箭头有两根向上、两根向下，P₂ 仍为 1；把角度调到 90°，它们都躺在膜面内，P₂ 变为 −0.5。这是角度定义的几何算例。真实轨迹中的方向分布在三维空间，程序对全部选中向量逐一计算，因此同样的运算规则能够自然用于两个叶片与不同尾链位置。

## 把自组装记录变成可继续研究的模型

完整分析程序只需要两段记录的 TPR 和 XTC。它先核对 128 个十二珠 DSPC、768 个 W 及分子内的珠子顺序，再沿拓扑连接逐步恢复跨越周期边界的分子。对所有连接检查闭合关系，可以避免一根被盒边切开的尾链被误认为异常伸长。恢复后的分子坐标用于方向和键角，水珠密度则使用适合周期盒的居中坐标。程序把轨迹时间、结构量和图像一起保存，所有面积、厚度及取向结果都可以追溯到相同的记录与统计窗口。

### 完整的自组装与膜结构分析

```
"""Read DSPC assembly and bilayer trajectories and measure their organization.

python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer \
    --out analysis --language en
The two directories contain assembly.tpr/xtc and bilayer.tpr/xtc respectively.
Dependencies: MDAnalysis, NumPy, Matplotlib. MDAnalysis lengths are angstrom.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def plans(group):
    index = {int(x): i for i, x in enumerate(group.indices)}
    edges = np.array([[index[int(a)], index[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, k, sign))
    if len(seen) != 12:
        raise ValueError("Each DSPC molecule must have a connected 12-bead graph")
    return edges, plan


def reconstruct(raw, box, edges, plan):
    # Apply one identical molecular topology to all 128 lipids in this frame.
    delta = raw[:, edges[:, 1]]-raw[:, edges[:, 0]]
    delta = minimize_vectors(delta.reshape(-1, 3), box).reshape(delta.shape)
    xyz = np.empty_like(raw, dtype=float); xyz[:, 0] = raw[:, 0]
    for a, b, k, sign in plan:
        xyz[:, b] = xyz[:, a]+sign*delta[:, k]
    actual = xyz[:, edges[:, 1]]-xyz[:, edges[:, 0]]
    if np.max(np.linalg.norm(actual-delta, axis=-1)) > .005:
        raise ValueError("Periodic bond-cycle closure failed")
    longest = float(np.linalg.norm(actual, axis=-1).max()/10)
    if longest > .8:
        raise ValueError("A coarse-grained bonded distance exceeds 0.8 nm")
    return xyz/10, longest


def statistics(a):
    return {"mean": float(np.mean(a)), "sd": float(np.std(a, ddof=1))}


def save(fig, path):
    fig.savefig(path.with_suffix(".svg"))
    fig.savefig(path.with_suffix(".png"), dpi=150)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--assembly", type=Path, default=Path("records/assembly"))
    p.add_argument("--bilayer", type=Path, default=Path("records/bilayer"))
    p.add_argument("--out", type=Path, default=Path("analysis"))
    p.add_argument("--language", choices=["zh", "en"], default="en")
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    available = {f.name for f in font_manager.fontManager.ttflist}
    families = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [n for n in families if n in available],
                         "font.size": 14, "axes.labelsize": 15,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    expected_names = ["NC3", "PO4", "GL1", "GL2", "C1A", "C2A", "C3A", "C4A",
                      "C1B", "C2B", "C3B", "C4B"]
    tail_pairs = [(4, 5), (5, 6), (6, 7), (8, 9), (9, 10), (10, 11)]
    arrays = {}; snapshots = []; maximum_bond = 0.; initial_side = None
    density_edges = np.linspace(-4, 4, 81)
    density = np.zeros((3, 80)); expected_integral = np.zeros(3)
    order = []; leaflet_changes = 0; late_frames = 0
    for name, folder in [("assembly", args.assembly), ("bilayer", args.bilayer)]:
        u = mda.Universe(str(folder/f"{name}.tpr"), str(folder/f"{name}.xtc"))
        lipids = u.select_atoms("resname DSPC")
        water = u.select_atoms("resname W")
        if len(u.atoms) != 2304 or len(lipids) != 1536 or len(water) != 768:
            raise ValueError("Expected 128 DSPC molecules and 768 W beads")
        if list(lipids.names) != expected_names*128 or abs(sum(lipids.charges)) > 1e-5:
            raise ValueError("DSPC bead ordering or charge differs from this model")
        edges, plan = plans(lipids[:12]); rows = []
        for frame in u.trajectory:
            if not np.allclose(frame.dimensions[3:], 90):
                raise ValueError("This analysis uses the recorded orthorhombic boxes")
            box = frame.dimensions[:3].astype(float)/10
            xyz, longest = reconstruct(lipids.positions.astype(float).reshape(128, 12, 3), frame.dimensions, edges, plan)
            maximum_bond = max(maximum_bond, longest)
            head = xyz[:, 1]; tail = xyz[:, [7, 11]]
            direction = head-tail.mean(axis=1)
            direction /= np.linalg.norm(direction, axis=1)[:, None]
            q = 1.5*direction.T@direction/128-.5*np.eye(3)
            eig, axes = np.linalg.eigh(q); axis = axes[:, -1]
            row = [float(frame.time), float(eig[-1]), *np.abs(axis)]
            if name == "assembly" and frame.frame in [0, 50, 150, 300]:
                snapshots.append({"time_ps": float(frame.time), "box_nm": box.tolist(),
                                  "lipid_coordinates_nm": (xyz % box).tolist(),
                                  "water_coordinates_nm": (water.positions/10 % box).tolist()})
            if name == "bilayer":
                side = direction[:, 2] > 0
                if initial_side is None:
                    initial_side = side.copy()
                    if [int(side.sum()), int((~side).sum())] != [66, 62]:
                        raise ValueError("Expected the recorded 66/62 leaflet membership")
                leaflet_changes += int(np.sum(side != initial_side))
                # A circular mean locates the tail midplane across the periodic seam.
                phase = np.mean(np.exp(2j*np.pi*tail[:, :, 2]/box[2]))
                if abs(phase) < .1:
                    raise ValueError("Tail positions do not define one clear midplane")
                center = np.angle(phase)*box[2]/(2*np.pi)
                hz = head[:, 2]-center; hz -= box[2]*np.round(hz/box[2])
                area = box[0]*box[1]
                thickness = hz[initial_side].mean()-hz[~initial_side].mean()
                row += [float(area), float(area/66), float(area/62), float(thickness)]
                if frame.time >= 15000:
                    late_frames += 1
                    groups = [xyz[:, 1, 2], xyz[:, 4:, 2].ravel(), water.positions[:, 2]/10]
                    for k, z in enumerate(groups):
                        centered = z-center; centered -= box[2]*np.round(centered/box[2])
                        counts, _ = np.histogram(centered, bins=density_edges)
                        if counts.sum() != len(z):
                            raise ValueError("Density interval does not cover all selected beads")
                        density[k] += counts/(area*np.diff(density_edges))
                        expected_integral[k] += len(z)/area
                    bond = np.stack([xyz[:, b]-xyz[:, a] for a, b in tail_pairs], axis=1)
                    cos2 = bond[:, :, 2]**2/np.sum(bond*bond, axis=-1)
                    order.append((1.5*cos2-.5).mean(axis=0))
            rows.append(row)
        values = np.asarray(rows)
        if len(values) != 301 or not np.allclose(values[:, 0], np.arange(301)*100):
            raise ValueError("Expected 301 saved frames spanning 0–30000 ps")
        arrays[name] = values
        fields = ["time_ps", "nematic_eigenvalue", "axis_abs_x", "axis_abs_y", "axis_abs_z"]
        if name == "bilayer":
            fields += ["area_nm2", "area_positive_nm2", "area_negative_nm2", "phosphate_separation_nm"]
        with (args.out/f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(fields); writer.writerows(values)
    density /= late_frames; expected_integral /= late_frames
    actual_integral = np.sum(density*np.diff(density_edges), axis=1)
    if not np.allclose(actual_integral, expected_integral, rtol=1e-12):
        raise ValueError("Density integral check failed")
    order = np.asarray(order); late = arrays["bilayer"][150:]
    summary = {"model": "128 DSPC, Martini 3 regular v3.0.0 + PC/bonded v2; 768 W; 340 K",
               "frames_per_stage": 301, "bilayer_late_frames": late_frames,
               "bilayer_window_ps": [15000, 30000], "leaflet_counts": [66, 62],
               "leaflet_orientation_changes": leaflet_changes, "maximum_bond_nm": maximum_bond,
               "assembly_final_nematic_eigenvalue": arrays["assembly"][-1, 1],
               "assembly_final_axis_absolute": arrays["assembly"][-1, 2:5].tolist(),
               "bilayer_last15ns": {n: statistics(late[:, j]) for n, j in [
                   ("nematic_eigenvalue", 1), ("area_nm2", 5), ("area_positive_nm2", 6),
                   ("area_negative_nm2", 7), ("phosphate_separation_nm", 8)]},
               "tail_bond_labels": [f"{expected_names[a]}–{expected_names[b]}" for a, b in tail_pairs],
               "tail_bond_P2_mean": order.mean(axis=0).tolist(),
               "tail_bond_P2_frame_sd": order.std(axis=0, ddof=1).tolist(),
               "density_integral_per_nm2": actual_integral.tolist(),
               "density_expected_mean_count_over_area_per_nm2": expected_integral.tolist(),
               "sd_definition": "Sample standard deviation across saved frames, ddof=1"}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    np.savetxt(args.out/"density.csv", np.column_stack(((density_edges[:-1]+density_edges[1:])/2, density.T)),
               delimiter=",", header="z_nm,PO4_per_nm3,tail_beads_per_nm3,W_per_nm3", comments="")
    fig, axs = plt.subplots(2, 2, figsize=(12, 10), constrained_layout=True)
    for ax, frame in zip(axs.ravel(), snapshots):
        xyz = np.asarray(frame["lipid_coordinates_nm"]); w = np.asarray(frame["water_coordinates_nm"])
        ax.scatter(w[:, 0], w[:, 1], s=7, c="#aabfce", alpha=.35)
        ax.scatter(xyz[:, 4:, 0], xyz[:, 4:, 1], s=8, c="#d2974f", alpha=.45)
        ax.scatter(xyz[:, 1, 0], xyz[:, 1, 1], s=27, c="#147d92", edgecolors="none")
        ax.set(xlabel="x / nm", ylabel="y / nm", xlim=(0, frame["box_nm"][0]),
               ylim=(0, frame["box_nm"][1]), aspect="equal", title=f'{frame["time_ps"]/1000:g} ns')
    fig.suptitle("自组装轨迹：磷酸头基、尾珠与水珠的 xy 投影" if zh else
                 "Assembly trajectory: xy projections of phosphate heads, tails, and water", fontsize=16)
    save(fig, args.out/"assembly-structure")
    a = arrays["assembly"]
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    axs[0].plot(a[:, 0]/1000, a[:, 1], c="#147d92", lw=1.8)
    axs[0].set_ylabel("最大取向特征值 S" if zh else "Largest alignment\neigenvalue S")
    for j, color in enumerate(["#c66b43", "#147d92", "#7566a8"]):
        axs[1].plot(a[:, 0]/1000, a[:, j+2], label=f"|n{'xyz'[j]}|", color=color, lw=1.4)
    axs[1].set_ylabel("主轴单位向量的绝对分量" if zh else "Principal-axis components\n(absolute values)")
    axs[1].set_xlabel("自组装阶段时间 / ns" if zh else "Assembly-stage time / ns")
    axs[1].legend(ncol=3); axs[0].set_title("共同朝向随聚集逐渐出现" if zh else "A common orientation develops during aggregation")
    for ax in axs: ax.grid(alpha=.15)
    save(fig, args.out/"assembly-order")
    b = arrays["bilayer"]
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    for j, color, label in [(6, "#147d92", "+z: 66"), (7, "#c66b43", "−z: 62")]:
        axs[0].plot(b[:, 0]/1000, b[:, j], c=color, lw=1.5, label=label)
    axs[0].set_ylabel("每脂质投影面积 / nm²" if zh else "Projected area per lipid\n/ nm²"); axs[0].legend(ncol=2)
    axs[1].plot(b[:, 0]/1000, b[:, 8], c="#7566a8", lw=1.5)
    axs[1].set_ylabel("磷酸面间距 / nm" if zh else "Phosphate-plane\nseparation / nm")
    axs[2].plot(b[:, 0]/1000, b[:, 1], c="#147d92", lw=1.5)
    axs[2].set_ylabel("最大取向特征值 S" if zh else "Largest alignment\neigenvalue S")
    axs[2].set_xlabel("半各向同性阶段时间 / ns" if zh else "Semiisotropic-stage time / ns")
    axs[0].set_title("同一片膜，两种叶片分母" if zh else "One membrane area, two leaflet populations")
    for ax in axs: ax.axvspan(15, 30, color="#e8d5ac", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"bilayer-geometry")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    centers = (density_edges[:-1]+density_edges[1:])/2
    labels = ["磷酸珠 PO4", "全部尾珠", "水珠 W"] if zh else ["Phosphate beads PO4", "All tail beads", "Water beads W"]
    for values, label, color in zip(density, labels, ["#147d92", "#c59148", "#7896b0"]):
        axs[0].plot(centers, values, label=label, c=color, lw=2)
    axs[0].set(xlabel="距尾端中面的 z / nm" if zh else "z from terminal-tail midplane / nm",
               ylabel="珠数密度 / nm⁻³" if zh else "Bead number density / nm⁻³")
    axs[0].legend(ncol=3, loc="lower center", bbox_to_anchor=(.5, 1.01), fontsize=12)
    positions = np.arange(6)
    axs[1].errorbar(positions, order.mean(axis=0), yerr=order.std(axis=0, ddof=1), fmt="o", c="#147d92", capsize=5)
    axs[1].set_xticks(positions, summary["tail_bond_labels"], rotation=15)
    axs[1].set_ylim(-.5, 1); axs[1].set_ylabel("尾链键取向 P₂" if zh else "Tail-bond orientation P₂")
    axs[1].set_title("误差棒为逐帧均值的标准差" if zh else "Bars show the standard deviation of frame means")
    for ax in axs: ax.grid(alpha=.15)
    save(fig, args.out/"bilayer-profile-order")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

读取两段原生TPR/XTC，恢复分子连接并输出双语图及数值记录。

运行时，将自组装的 assembly.tpr、assembly.xtc 放入 records/assembly，将后续的 bilayer.tpr、bilayer.xtc 放入 records/bilayer，然后执行页面中的分析命令。程序输出四组图：自组装快照、共同方向随时间的变化、膜几何量随时间的变化，以及密度与局部取向。中英文模式只切换标签，计算定义保持一致。两阶段的 602 帧全部经过连接检查；密度积分也与逐帧珠数除以面积的平均相符。读者修改统计窗口或片厚时，这些对应关系仍能帮助检查新结果是否符合计数与单位。

### 生成两种语言的分析图

```
python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer --out analysis-zh --language zh
python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer --out analysis-en --language en
```

records中分别放置assembly.tpr/xtc和bilayer.tpr/xtc；两次运行共享同一组数值。

从这一次记录可以具体读出：128 个脂质形成了一片近似平面双层；两侧分别保留 66 与 62 个分子；在后续 15–30 ns 窗口，平均面积为 38.473 nm²，磷酸面间距为 4.321 nm，整个脂质方向的 S 约为 0.836。水相、头基和尾部的分区也在珠数密度中清楚出现。这组结果把自组装的形态、分子数和内部排列联系起来。它为后续在膜上接入聚合物链、改变头基组成或研究膜表面拥挤提供了可检查的起点。

粗粒化模型的时间尺度需要和它保留的自由度一起理解。去掉快速内部运动后，摩擦、能量起伏和某些重排路径都会改变，不同过程受到的影响也可能不同。本节报告的每段 30 ns 是积分时间；若研究真实扩散或成膜速率，需要针对所测过程，与合适的实验或更细分辨率模型建立联系。结构比较同样要配对条件：温度、含水量、脂质参数版本、叶片数和压力设置共同定义了这片膜。明确这些量，才能让一次材料改动对应一个清楚的问题。

下一次研究可以从一个小而具体的比较开始。例如保持脂质种类与温度不变，增加水量，观察面积、密度剖面和尾链取向怎样变化；或者预先构建人数相等的两个叶片，考察不对称性对几何量的影响。两种设计改变的物理条件不同，应分别组织重复与统计。接下来关于接枝聚合物的例子，会在已经明确的膜表面增加柔软链，并把“每个脂质占多大面积”进一步变成“每单位膜面积接了多少条链”。本节建立的分辨率、叶片计数和法向坐标，将继续决定那些新测量的含义。

## 延伸阅读与开放资料

- [Lipid bilayers – Part I: Self-assembly](https://cgmartini.nl/docs/tutorials/Martini3/LipidsI/index.html) · Luís Borges-Araújo; Manuel N. Melo; Martini Force Field Developers Team · MIT (website source and documentation)

  DSPC随机自组装、转动膜法线、半各向同性续段与结构分析的流程和输入。

  固定随机种子与记录间隔；压力更新改为5步；采用真实66/62叶片数；补充周期居中、完整双语分析及逐符号解释。
- [Martini force fields and Martini 3 Lipid Parameters](https://github.com/Martini-Force-Field-Initiative/M3-Lipid-Parameters) · Martini Force Field Initiative; Kasper B. Pedersen and contributors · Apache-2.0

  2025脂质成键v2与PC v2中的DSPC，配合Martini3基础v3.0.0及溶剂v1。

  保留力场数值参数；系统组成及运行设置按本节输入。
- [Martini Force Fields](https://github.com/Martini-Force-Field-Initiative/martini-forcefields) · Martini Force Field Initiative · Apache-2.0

  Martini3基础珠子相互作用与W溶剂参数。

  数值参数保持不变。
- [Coarse Grained Model for Semiquantitative Lipid Simulations (2004)](https://doi.org/10.1021/jp036508g) · Siewert J. Marrink; Alex H. de Vries; Alan E. Mark · Copyright American Chemical Society; cited historical facts

  脂质粗粒化及自组装模型的科学史。

  独立绘制概念图，按科学问题叙述历史。
- [Martini 3: A General Purpose Force Field for Coarse-Grained Molecular Dynamics (2021)](https://doi.org/10.1038/s41592-021-01098-3) · Paulo C. T. Souza and colleagues · Article cited; author manuscript publicly accessible

  Martini3分辨率、珠子类型与有效相互作用的背景。

  以本节模型解释概念。
- [The Martini 3 Lipidome: Expanded and Refined Parameters Improve Lipid Phase Behavior (2025)](https://doi.org/10.1021/acscentsci.5c00755) · Kasper B. Pedersen and colleagues · CC BY 4.0

  尾链映射及参数修订的物理含义。

  独立撰写解释与概念图。
