# 分子怎样自己聚成一团

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l13/
Language: zh-CN

运行二维两亲分子模型，从头尾相互作用走到真实聚集轨迹，再用周期距离与图的连通性测量团簇。

## 从洗涤剂到会聚集的分子

清水接触一层油污时，水和油往往各占一边；加入适合的表面活性剂后，分子可以同时接触两种环境，帮助重新组织界面。理解这一现象，首先要认识同一个分子内部的差别：一部分更容易与水相处，另一部分更偏好非极性环境。这样的分子称为两亲分子。在合适条件下，许多两亲分子能够通过各自的运动形成聚集体，把较少接触水的部分集中起来，把较容易接触水的部分留在外侧。这类组织方式与洗涤、分散、乳化以及软材料中的微观结构都有联系。

“自组装”描述分子在相互作用和热运动共同作用下形成较大组织的过程。没有一个控制器给每个分子指定最终座位，结构来自局部碰撞、接近、分离和重新排列的累积。可以用一群拿着不同材质雨伞的人作粗略类比：每个人都在移动，但不同表面对周围环境的适应程度，会影响他们怎样挤在一起。分子还受到温度、浓度和几何连接的约束，因此仅说“相似相溶”还不够。本讲把这些因素缩成一套明确的头尾珠模型，实际观看聚集过程，并从坐标计算聚集体的大小。

案例来自LAMMPS随软件提供的二维micelle示例。一个两亲分子由一个头珠和两个尾珠构成，另有单独的溶剂珠；总共150个两亲分子、750个溶剂珠，在xy平面内运动。模型保留头尾对溶剂的不同偏好、尾部之间的联系、分子的连接和热运动，适合研究分选、聚集及几何统计。珠子代表有效相互作用中心，本例没有把它们标定为某种具体洗涤剂的原子团，也没有给它们电荷。要研究某种实际表面活性剂的盐响应或化学细节，可以进一步建立相应的化学映射与电荷模型。

### 真实的二维组装过程

从软准备后的t=0开始，继续到505τ；每帧按固定粒子与分子身份显示。

官方二维micelle模型：750个溶剂珠与150条三珠两亲分子，共1200珠。软势准备后，保留原LJ参数、速度缩放温控及平面约束，T*=0.45、步长0.005τ，生产段0–505τ。

[下载参考数据与完整输入（ZIP） 4.93 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-micelle-reference-data.zip)

播放器中的每一帧都来自实际LAMMPS计算。先注意尾珠是否逐渐集中、头珠是否更常出现在聚集体外侧，再看跨越盒边界的团是否在另一边接续。接下来的分析会把这些观察拆成三个可复算的问题：体系中有多少个连通团簇，最大的团簇含多少个分子，以及头尾珠周围各有多少溶剂近邻。三个问题分别描述整体组织、较大的聚集体和局部环境，配合起来比单看一张“像胶束”的图更有信息。

这里使用约化单位。距离的共同标尺记为σ，能量标尺记为ε，所有珠子的质量数值为1，运动时间用这套标尺确定的τ表示。约化温度0.45表示热能尺度相对于ε的大小。这样可以先研究相互作用之间的关系，随后再为选定化学体系建立长度、能量与时间的对应。本例观察到505τ，因此图上保留τ作为单位；将它换成纳秒，需要额外的物理标定。读完这一讲，你应能从模型定义一路走到真实轨迹、团簇算法和结构解释，并知道每一步统计实际上在数什么。

## 肥皂溶液为何推动了胶束研究

肥皂溶液曾给早期胶体化学提出一个很具体的问题：它既表现出电解质的某些性质，又形成比普通小分子更大的组织单元，溶液里究竟有哪些东西在移动？McBain与Salmon在1920年关于肥皂溶液的研究中讨论了胶体电解质，把带电聚集体及其携带的溶剂纳入溶液结构解释。McBain随后关于胶体的论述，也关注普通分子与胶体粒子之间的尺度关系。研究者需要把电学、溶液性质和聚集结构放在同一框架里理解。[1920年的原始论文](https://doi.org/10.1021/ja01448a010)与[1921年的论述](https://www.nature.com/articles/107046a0)保留了这条思考线索。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s2)

图 1 · 肥皂溶液推动了对带电聚集体及其水化的讨论。装置与聚集体为原理示意，强调从可测性质推断溶液中的组织单元。

这个历史问题有助于理解“一个粒子”在不同测量中的含义。在化学式中，一个表面活性剂分子有自己的组成；在溶液中，几十个这样的分子可以暂时形成一个共同移动的聚集体；在光散射或其他结构测量中，人们又可能把这个聚集体当作一个较大的对象。分子没有因为聚集而自动变成新的共价大分子，它们仍可通过非共价接触维持组织。因而，“分子有多少个”和“聚集体有多少个”属于不同层次的计数。稍后同一帧中会同时出现150个分子与12个连通分量，这正是层次不同带来的自然结果。

现代的头尾图像为这种组织提供了直观描述。在水环境中，亲水端倾向于与周围溶剂接触，疏水部分的聚集减少了它们直接暴露给水的机会；具体结构由分子形状、相互作用、温度和组成共同决定。真实水中，溶剂结构和熵也参与疏水效应。本例的溶剂是简单珠子，通过选定的成对相互作用表达有效偏好，适合观察由这种偏好产生的分选趋势。历史中的带电肥皂与这里的不带电模型提供两个层次：前者展示需要解释的现象，后者让少数机制在可控制的条件下显现。

胶束与其他聚集形态也应当在空间上区分。一个通常所说的三维胶束可以具有内部和外表面，双层膜则有两侧亲水界面与中间疏水区；二维模型中的团只有平面内的内外关系。把二维圆团直接看成一个三维球形胶束，会混入额外的体积、曲率和堆积假设。本讲使用“二维聚集体”描述实际结构，使用“胶束模型”说明它所抽取的头尾分选问题。若需要球形聚集数、膜厚或三维曲率，应建立三维体系，并重新选择合适的形貌测量。

这种从测量反推结构的思路仍然适用。一张轨迹图能显示分子是否聚到一起，数值统计则要求进一步说明何谓“在一起”。如果两个小团只是短暂擦过，某个距离阈值可能会把它们算成一团；如果一个大团跨越周期边界，直接按画面两边分开又会把它拆成两团。历史上的聚集概念因此在计算中变成了定义与测量的问题：先明确观察尺度，再检查结论对这个尺度是否稳定。后面的交互会让你在不改变原始坐标的情况下体验这一点。

## 一个头和两个尾珠保留了什么

模型有四种粒子类型。类型1是溶剂，共750个；类型2是头珠，共150个；类型3和4分别是中间尾珠与末端尾珠，各150个。每个两亲分子的连接顺序是2—3—4，所以150个分子共有450个珠子和300条键。头珠与两个尾珠拥有同一个分子编号，溶剂珠则单独处理。粒子编号负责在轨迹中追踪具体珠子，分子编号负责把三个珠子识别为同一个对象；类型编号决定采用哪组相互作用参数。这三个编号各有用途，不能在分析时彼此替代。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s3)

图 2 · 模型保留头尾差异、两个尾段的尺寸参数和分子连接。珠子是有效相互作用中心，颜色与粒子类型对应；画出的圆是识别符号。

两个连接采用谐键，平衡长度为0.75σ，LAMMPS参数中的系数为50 ε/σ²。谐键可以想成在自然长度附近拉伸或压缩的弹簧，偏离越大，能量代价增长越快。每个分子只有两个这样的连接，没有额外键角或二面角势，因此可以在平面内弯曲。尾珠与头珠之间的非键排斥仍会影响过度折叠，周围分子也会限制它能采取的姿态。分子虽短，已经具有“头在哪里、尾朝向哪里”的内部结构，和没有连接的单一粒子流体不同。

两条键把三个珠子连成一个分子式 2

![两条键把三个珠子连成一个分子](https://ml-biomat.com/static/agent-math/b9f78e87a55b157cf86cc200.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U_{b} | 一条谐键的势能 | 基准ε |
| K_{b} | LAMMPS谐键系数，已包含常见写法中的1/2因子 | ε/σ² |
| r、r₀ | 当前键长；平衡键长0.75σ | σ |
| −、²、= | 键长偏差；平方；等号；系数与平方项相乘 | 运算符 |

怎样理解偏离平衡长度会提高能量，方向相反但大小相同的偏差得到相同能量代价。每个两亲分子保留两条这样的连接。

算一个例子K_b=50 ε/σ²，r₀=0.75σ。若r=0.85σ，U_b=50×0.10²=0.5ε；r=0.65σ时相同。

使用条件本例没有键角或二面角势。special_bonds fene指定非键排除权重，并没有把这里的harmonic键变成FENE键。

输入中的special_bonds fene容易让初学者误读。这里的fene是一个非键排除设置的名称，给出沿键图相隔一条、两条和三条键的成对作用权重0、1、1；它没有改变前面bond_style harmonic所定义的键势。因此，直接相连的头—中尾和中尾—末尾不再另算普通LJ作用，隔着中尾的头—末尾保留相应非键作用。读输入文件时，键势和非键排除属于两项不同的设置。这样分别理解，才能判断一条链的柔顺性与近邻排斥究竟由哪些项控制。

盒的x、y边长都是35.85686σ。1200个珠子除以盒面积，得到实际珠子面数密度约0.933333 σ⁻²；150个两亲分子对应面数密度约0.116667 σ⁻²。原始构建说明中还出现0.7这个数，它描述900个初始格点相对于面积的密度：其中150个格点变成头珠，随后再为这些头加入300个尾珠。增加尾珠之后，珠子总密度自然提高。这里用的是二维面积密度，z方向狭窄的盒厚是二维文件的几何设置，不应拿来构造一个三维液体质量密度。

运行前的检查程序直接读取公开的data.micelle。它核对文件校验值、四种类型的数量、每个分子的三珠组成以及两条键是否确实构成2—3—4链，并检查所有z坐标为零。通过这些检查后，后续算法可以把一个分子看成稳定的节点，不必在每帧重新猜测谁和谁属于同一条链。例题包保留原始数据文件；实际模拟从这些坐标出发，先用温和排斥整理局部接触，再切换到正式相互作用。

### 先核对分子与连接

```
"""Inspect the supplied micelle data before running LAMMPS.

python check_micelle.py --data data.micelle
Uses only the Python standard library.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path('data.micelle'))
    args = parser.parse_args()
    expected = '35d33cbc97b1862bc46dd18ee52fec5f6dd879436cf12fbc6d0bb6ba9a803c8c'
    actual = hashlib.sha256(args.data.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError('The data.micelle checksum differs from the supplied example.')
    atoms = {}; bonds = []; box = []; section = None
    for raw in args.data.read_text().splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if fields[-1] in ['xhi', 'yhi', 'zhi']:
            box.append([float(fields[0]), float(fields[1])])
        elif line in ['Masses', 'Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Velocities']:
            section = line
        elif section == 'Atoms' and fields[0].isdigit():
            aid, mol, typ = map(int, fields[:3])
            if aid in atoms:
                raise ValueError('Duplicate atom identifier.')
            atoms[aid] = (mol, typ, tuple(map(float, fields[3:6])))
        elif section == 'Bonds' and fields[0].isdigit():
            bonds.append(tuple(map(int, fields)))
    counts = Counter(a[1] for a in atoms.values())
    molecules = defaultdict(list)
    for aid, (mol, typ, xyz) in atoms.items():
        if xyz[2] != 0:
            raise ValueError('Every particle must start in the xy plane.')
        if typ != 1:
            molecules[mol].append(aid)
    if counts != {1: 750, 2: 150, 3: 150, 4: 150} or len(molecules) != 150 or len(bonds) != 300:
        raise ValueError('Unexpected particle or bond counts.')
    for mol, ids in molecules.items():
        if sorted(atoms[i][1] for i in ids) != [2, 3, 4]:
            raise ValueError('Each molecule needs a head and two distinct tail types.')
        local = [b for b in bonds if b[2] in ids or b[3] in ids]
        pairs = {tuple(sorted([atoms[b[2]][1], atoms[b[3]][1]])) for b in local}
        if len(local) != 2 or pairs != {(2, 3), (3, 4)}:
            raise ValueError('The two bonds must form a head-middle-tail chain.')
        if any(atoms[b[2]][0] != mol or atoms[b[3]][0] != mol for b in local):
            raise ValueError('A bond crosses molecular identities.')
    area = (box[0][1] - box[0][0]) * (box[1][1] - box[1][0])
    print(json.dumps({'data_sha256': actual, 'particles': len(atoms), 'types': dict(counts),
                      'amphiphiles': len(molecules), 'bonds': len(bonds),
                      'bead_areal_density': len(atoms) / area,
                      'amphiphile_areal_density': len(molecules) / area,
                      'dimensions': 2}, indent=2))


if __name__ == '__main__':
    main()
```

在例题目录运行python check_micelle.py --data data.micelle，检查原始数据、150条三珠链和二维面积密度。

## 从温和排斥走到正式相互作用

刚构建好的珠子排列可能含有很近的接触。若一开始就施加距离很短时迅速发散的LJ排斥，局部大力会给积分带来困难。原示例先采用有限的soft势，将其强度参数在1000步中从1逐渐提高到20，让近邻逐步分开；谐键在此期间维持各分子的连接。这个阶段的任务是准备几何结构，所用的非键势与正式观测阶段不同。完成后移除控制soft强度的设置，再切换到lj/cut，保留同一套粒子身份和已经整理过的坐标。

Lennard–Jones势有两个竞争项：非常近时的排斥增长快一些，稍远时的吸引占优势。不同类型对各有自己的σᵢⱼ，因此势能过零位置和最低点会移动；截断r_c,ij则规定计算保留到多远。本例所有类型对的能量参数数值都为1，但尺寸与截断不同。溶剂—溶剂、头—头和溶剂—头的σᵢⱼ为1，截断2.5σ，保留较长的吸引区。尾珠之间也保留较长作用，3—3、4—4、3—4的尺寸参数分别为0.75、0.50、0.67，均使用2.5σ的绝对截断。

读懂不同珠子之间的LJ相互作用式 1

![读懂不同珠子之间的LJ相互作用](https://ml-biomat.com/static/agent-math/1063501ec3d59262028abc37.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Uᵢⱼ(r) | 类型i、j的两珠在距离r处的非键势能 | 能量，以基准ε表示 |
| i、j | 粒子类型编号1到4 | 无量纲 |
| r、σᵢⱼ、r_{c,ij} | 中心距离；该对势能过零的距离尺度；该对截断距离 | 长度，以基准σ表示 |
| εᵢⱼ | 该对势阱的深度参数，本例各对为1个基准ε | 能量 |
| 4、12、6 | LJ形式中的常数；12次幂与6次幂 | 无量纲 |
| /、−、[ ]、=、< | 相除；两项之差；分组；等号；严格小于；相邻因子相乘 | 运算符 |

怎样理解近距离12次幂项增长更快，产生排斥；较远处6次幂项带来吸引。截断距离决定实际保留曲线的哪一段。

算一个例子σᵢⱼ=1、εᵢⱼ=1时，r=1处两项相消，U=0；r=2^(1/6)≈1.122462处U=−1。若σᵢⱼ=0.88，最低点移到约0.987767。

使用条件适用于非键作用及special_bonds保留的对。本例使用未平移的lj/cut，截断外势能设为零；能量曲线的截断跳变与力的吸引/排斥方向要分别理解。

溶剂—尾珠采用σᵢⱼ=1、截断1.12246σ，接近这组LJ势的最低点，因此保留的力主要是近距离排斥。头—中尾与头—末尾也采用1.12246σ截断，但尺寸参数分别为0.88和0.75。它们的最低点分别约为0.987767σ和0.841847σ，所以最低点到截断之间仍有吸引力区间。这里需要把“同一个绝对截断”与“同一段势函数”分开：势阱位置随尺寸参数改变，单看截断数值或一行简短注释无法确定作用方向。图中把三个实际区间并排画出，便于直接比较。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s4)

图 3 · σ在图中表示共同基准长度。各类型对的σᵢⱼ分别为1、0.88和0.75个基准σ，因此相同的绝对截断会保留不同的力区间；图只画0.5σ以上。

正式阶段仍使用原示例的速度缩放温控：每100步检查一次温度，目标为0.45，允许窗口为0.02，超出窗口时按1.0比例修正到目标。位置和速度的积分由fix nve完成，temp/rescale负责温度调整，enforce2d把z方向速度与力保持为零。fix nve这个名称只说明使用的积分更新方式，整个运行还受到温控操作。这里保留原示例的机制演示协议，用它观察聚集与分选；若研究精确的平衡涨落或动力学输运，应选择与相应统计系综和时间尺度相匹配的热浴协议并重新比较。

### 完整二维组装输入

```
# 2d micelle simulation

dimension	2

neighbor	0.3 bin
neigh_modify	delay 5

atom_style	bond

# Soft potential push-off

read_data	data.micelle
special_bonds	fene

pair_style	soft 1.12246
pair_coeff	* * 0.0 1.12246

bond_style 	harmonic
bond_coeff	1 50.0 0.75

velocity	all create 0.45 2349852

variable	prefactor equal ramp(1.0,20.0)

fix		1 all nve
fix		2 all temp/rescale 100 0.45 0.45 0.02 1.0
fix		3 all adapt 1 pair soft a * * v_prefactor
fix		4 all enforce2d

thermo		50

# Whole-system energies; LJ reduced units, a two-dimensional model.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
thermo_style custom step time c_cTemp c_cPE c_cKE etotal
thermo_modify norm no
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E file soft-thermo.dat format " %.15g"
dump trajectory all custom 250 soft.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
run 1000
unfix record
undump trajectory
write_data after-soft.data pair ij

unfix		3

# Main run

pair_style	lj/cut 2.5

# solvent/head - full-size and long-range

pair_coeff	1 1 1.0 1.0 2.5
pair_coeff	2 2 1.0 1.0 2.5
pair_coeff	1 2 1.0 1.0 2.5

# tail/tail - size-averaged and long-range

pair_coeff	3 3 1.0 0.75 2.5
pair_coeff	4 4 1.0 0.50 2.5
pair_coeff	3 4 1.0 0.67 2.5

# solvent/tail - full-size and repulsive

pair_coeff	1 3 1.0 1.0 1.12246
pair_coeff	1 4 1.0 1.0 1.12246

# head/tail - smaller sigma and short absolute cutoff;
# the interval between the pair-specific minimum and cutoff is attractive

pair_coeff	2 3 1.0 0.88 1.12246
pair_coeff	2 4 1.0 0.75 1.12246

thermo		50

#dump		1 all atom 2000 dump.micelle

#dump		2 all image 2000 image.*.jpg type type zoom 1.6
#dump_modify	2 pad 5 adiam 1 0.5 adiam 2 1.5 adiam 3 1.0 adiam 4 0.75

#dump		3 all movie 2000 movie.mpg type type zoom 1.6
#dump_modify	3 pad 5 adiam 1 0.5 adiam 2 1.5 adiam 3 1.0 adiam 4 0.75

reset_timestep 0
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E file micelle-thermo.dat format " %.15g"
dump trajectory all custom 500 micelle.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
run 1000
write_restart original-example.restart
write_data original-example.data pair ij
# Extend observation with the same Hamiltonian, integrator and thermostat.
run 100000
write_restart micelle.restart
write_data micelle.data pair ij
```

保留官方参数、原始准备与1000步主段，并继续100000步；输出全体系能量和带分子身份的真实坐标。

完整输入先运行1000步soft准备，再把主阶段步号设为零。LJ阶段首先运行原示例的1000步，然后在相同相互作用、温度设置和积分器下继续100000步。步长为0.005τ，所以原主段到5τ，完整主段到505τ；soft阶段此前也经历5τ，但不计入这条主阶段时间轴。每500步保存一次轨迹，相当于2.5τ一帧，包含起点后共有203帧。运行脚本把日志写到文件，避免关键参数与数值提示在终端里滚过后难以查找。

### 运行模型并保留日志

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=2
"$lmp" -in in.micelle -log micelle.log > micelle.stdout.log 2>&1
```

运行bash run.sh，默认调用lmp。需要MOLECULE包及soft、lj/cut、adapt、temp/rescale和enforce2d命令。

## 读懂真实的温度和结构变化

判断轨迹之前，可以先检查一个与自由度有关的数值关系。二维点粒子每个只有x、y两个速度分量，温度计算默认扣除整体平移的两个自由度，因此1200珠体系使用2398个平动自由度。在温度0.45时，全体系动能应为539.55ε，而每珠动能约0.449625ε。完整输出记录的是全体系势能、动能和总能量；绘图时才除以1200。把这个顺序说清楚，可以避免把已经归一化的输出再除一次粒子数，或者误用三维自由度来解释二维温度。

二维温度与总动能的对应式 3

![二维温度与总动能的对应](https://ml-biomat.com/static/agent-math/8b93bd1a92f84d0ea8bb2e48.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| K | 整个体系的平移动能 | ε |
| N | 粒子总数1200，包括溶剂、头和尾珠 | 无量纲 |
| k_{B}、T | 玻尔兹曼常数；温度，LJ单位中k_B数值取1 | k_B T具有能量单位 |
| 2N−2 | 每珠两个运动方向，扣除两个整体平移自由度 | 无量纲自由度计数 |
| 2、−、/、= | 每个二次自由度贡献k_B T/2；相减；相除；等号；相邻因子相乘 | 常数与运算符 |

怎样理解温度计算把动能分配到实际参与统计的自由度。二维点粒子每个有x和y两个速度分量，默认计算再扣除整体平移。

算一个例子T*=0.45时，K=1199×0.45=539.55ε，每粒子为0.449625ε。把三维的3N−3套入此模型会多算一个运动方向。

使用条件用于本例无刚性约束的二维点珠与默认温度自由度。这里的恒温方式是周期速度缩放，数值关系用于检查记录定义。

### 温度控制与势能变化

温度以LJ单位给出，能量按全部1200珠归一；控制温度的速度缩放持续存在。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s5)

原生记录的温度以及每珠势能、动能，使用LJ约化单位。温度缩放始终作用于主模拟，势能下降与温度涨落需要结合这一条件阅读。

实际记录的平均温度约为0.451128，随时间在设定值附近起伏。势能在主阶段早期下降较快，之后变化逐渐缓慢，反映粒子排列和相互作用邻居在持续调整。动能则受温控维持在相近尺度。这条能量曲线记录热浴参与下的结构演变，所用截断势也保留了截断处的能量跳变。对应的检查包括温度、全体系能量加和、粒子身份和几何结构是否与定义一致。本例逐行核对了势能加动能等于总能量，并核对二维动能—温度关系。

四张实际坐标图保留了不同阶段的结构。t=0表示soft准备刚结束，尾珠尚未形成后期的大团；t=5τ对应原始示例主段的终点，已经出现一些近邻组合；到100τ和505τ时，尾珠富集区域更明显，较多头珠位于这些区域周围。溶剂仍填充剩余的平面空间。图中颜色代表粒子类型，不能直接据颜色连成的一片来决定一个团簇的成员：具体分组还需要后面定义的周期距离和分子身份。

### 从分散结构到更大的聚集体

实际0、5、100和505τ坐标，平面周期盒中的溶剂、头与两种尾珠分别着色。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s5)

0、5、100、505τ的实际平面坐标；灰色为溶剂、青色为头珠、金色和红色为两种尾珠。周期盒边缘可把同一聚集体分开显示，团簇计算使用周期距离。

周期盒的边界需要特别留意。盒左边和右边相接，上边和下边也相接，所以一个团可能在平面图上被边界切成两块。这个显示切口没有把真实近邻分开。分析两珠距离时，程序比较它们通过盒内或相邻周期像靠近的方式，取最短的平面距离。比如边长约35.86σ的盒中，x=0.2σ与x=35.6σ的两珠在x方向实际只相隔约0.46σ，而不是35.4σ。把图上的距离直接代入团簇判断，会漏掉跨边界的接触。

另一项有用的观察是时间尺度的分离。短程排斥能够很快整理过近的接触，几个分子形成小团也可能较早发生；已经形成的团再碰到一起、交换成员或改变内部排列，则需要更长的运动。温度曲线进入稳定范围，并不自动意味着团簇大小分布也已经稳定。这里把原5τ主段与延长后的结构同时展示，就是为了让读者看到“局部运动已受控”与“较大尺度组织还在变化”可以同时成立。后面的团簇曲线会进一步量化这种变化。

## 怎样从坐标认出一个团簇

数团簇之前，先决定图上的一个节点代表什么。本例以完整两亲分子为节点，共150个；溶剂不进入团簇节点列表。两个分子之间，只要任意一对尾珠的周期最小镜像距离不超过阈值，就连一条边。头珠仍随所属分子保留，但不负责这条尾部接触规则。这样得到的图只表达某一帧中的几何接近关系；真实的共价键始终是分子内部的两条谐键，分析图上的边并没有在模拟中生成新化学键。

用尾珠距离建立分子间的连接式 4

![用尾珠距离建立分子间的连接](https://ml-biomat.com/static/agent-math/f762e2d0bdfc39929fbdd0fd.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| A、B | 两个不同的两亲分子 | 分子身份 |
| 𝒯_A、𝒯_B | 两分子各自的两个尾珠集合 | 集合 |
| i、j | 分别属于A与B的尾珠编号 | 无量纲 |
| dᵢⱼ^PBC | 两个尾珠在xy周期平面内的最小镜像距离 | σ |
| d_{AB}、r_* | 两分子最近的尾珠距离；分析连接阈值 | σ |
| min、∈、≤、∼、if、= | 取最小值；属于；小于等于；在图中相邻；条件成立时；等号 | 运算符 |

怎样理解两个分子只要有一对尾珠足够近就在图上连边，再沿边寻找全部可达分子。阈值改变的是对同一坐标的分组规则。

算一个例子若A–B最近尾距1.1σ、B–C为1.0σ、A–C为2.1σ，取r_*=1.2σ时三者仍属于同一连通团簇，因为A可以经B到C。

使用条件所有150个分子都作为图节点，孤立分子也计为大小1的团簇。这一几何定义需要与组装形貌和阈值敏感性一起解释。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s6)

图 4 · 图中的节点是完整两亲分子，实线表示最近尾珠距离满足阈值。A与C可通过B连接，所以属于同一连通分量；D保留为大小1的分量。

连通团簇的含义是可以沿边走到一起。A接近B、B接近C时，即使A与C本身相隔较远，三者仍属于同一团簇。这与把所有成员都要求成“两两足够近”不同，后者会把一个较长的聚集体切碎。实现时，程序从150个独立分子出发，找到满足距离条件的尾珠对，把对应分子的集合合并；最后统计每个连通分量有多少个分子。每一帧所有分量的大小相加都应为150，这个守恒关系是分析中很实用的检查。

阈值1.2σ下，主阶段起点有100个连通分量，其中最大含4个分子；到原5τ主段结束时，有72个分量，最大含6个分子；100τ时有35个分量，最大含10个分子；505τ末帧有12个分量，最大含36个分子。这些分量包括大小为1的孤立分子。初始分量数没有等于150，是因为soft准备后已经有尾珠接触满足1.2σ规则。明确时间起点与判据后，这种初始接近关系就不会被误解释为正式阶段之前已经形成了相同形貌的大胶束。

### 三个阈值下的聚集统计

连通分量包括大小1的单分子；每条曲线分析相同203帧。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s6)

同一203帧在0.9、1.2、1.5σ尾珠接触阈值下的连通团簇数及最大团簇分子数。每个分子作为一个节点，大小1的分子也计入；曲线展示聚集随时间和定义的变化。

把阈值改为0.9σ，末帧得到15个分量、最大23个分子；改为1.5σ，则得到12个分量、最大36个分子。较严格的距离规则会切断较松的桥接，较宽的规则可能把相邻部分连起来。下面的交互直接使用0、5、100和505τ的真实坐标，拖动滑块后重新计算连通性，所有粒子位置保持不变。颜色表示当前分量，因此同一个颜色出现在盒两边时，往往提示周期连接。它把“模型产生的坐标”与“分析施加的分类规则”放在同一个画面里。

同一真实保存帧，改变尾珠距离阈值后重新计算团簇。

四个实际保存帧的几何重分类。溶剂珠隐藏，全部150个两亲分子的450个珠子保持原坐标；颜色随当前阈值计算的连通分量更新。

阈值敏感性有助于选择后续分析方式。若几个相近阈值给出相同的大团，可以继续检查其内部头尾分布和形状；若最大团大小频繁在两个数之间切换，则可以查看是否由一两条短暂接触把两团连接起来。进一步研究寿命时，可以要求接触持续一段时间，或跟踪成员集合随时间的重叠，但每增加一种规则都应重新说明它测量的对象。当前交互使用即时几何连通性，让最基本的定义保持清楚，再为更复杂的时间分析留出明确入口。

## 平均胶束大小为何不止一种

假设某一帧只有两个团，分别含2个和8个分子。如果随机选一个团，两团被选中的机会相同，平均大小为5；如果随机选一个分子，它有八成机会来自较大的团，所处团的平均大小就变成6.8。两种结果都叫平均大小，却回答不同问题。前者强调聚集体个数，后者强调分子实际分布在哪里。材料研究中，按对象个数、质量或散射权重统计也会带来类似差别，因此报告平均聚集数时应当把权重写在名称或定义中。

按团簇或按分子选择观察对象式 5

![按团簇或按分子选择观察对象](https://ml-biomat.com/static/agent-math/214afd67e71cd11cdbf80cf6.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| n、c_{n} | 团簇包含的分子数；该大小的团簇有多少个 | 无量纲计数 |
| n̄_cluster | 每个团簇等权的平均大小 | 分子数 |
| n̄_molecule | 随机选择一个分子时，其所在团簇的平均大小 | 分子数 |
| ∑ₙ、n²、/、= | 对全部大小求和；平方；相除；等号；相邻量相乘 | 运算符 |

怎样理解团簇等权时每团计一次；分子等权时，大小n的团里有n个可被选中的分子，因此再多一个n权重。

算一个例子两个团分别含2和8个分子，按团平均为(2+8)/2=5；按分子平均为(2²+8²)/10=6.8。实际末帧r_*=1.2σ时，两者分别为12.5与21.25333。

使用条件本例包括大小1的分子。若另设最小聚集数，应重新说明筛选对象和两个归一化分母。

实际末帧在1.2σ阈值下的团簇大小为36、23、23、22、11、10、7、6、5、3、3、1，相加正好150。每团等权的均值为150/12=12.5；每个分子等权时，分子数平方之和为3188，再除以150，得到21.25333。较大的团容纳更多分子，因此第二个数更大。图中还分别给出两种归一化分布：一种问某个大小占全部团簇的比例，另一种问有多少分子生活在这个大小的团里。两组柱的高度分别加起来为1。

这两组柱来自505τ的一帧，因此它们准确回答“此时分子怎样分配”。要描述一段时间里的典型分布，可以在选定时间窗内逐帧计算，并将相邻时间块分别比较。这里还有一个容易忽略的权重选择：先让每帧的团簇分布归一化再取平均，意味着每个时刻等权；把所有帧中的团簇直接合并再归一化，则会让团簇较多的时刻贡献更多。两种计算都能执行，但应根据研究问题选定。保存间隔2.5τ也只是记录频率，同一个团可能连续存在许多帧，所以203帧不等于203次独立组装实验。若关心末期状态是否可重复，可以从不同初始速度和排列开始运行，再比较相同时间窗的分布。

### 团簇大小与头尾接触的差别

左图为末帧1.2σ阈值下两种加权分布；右图为1.5σ内逐珠平均溶剂近邻数。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/#zh-s7)

左侧为505τ、1.2σ阈值下的团簇大小分布，分别按团簇和分子等权；右侧为头、中间尾珠、末端尾珠在1.5σ内的平均溶剂近邻数。两种分布回答不同的抽样问题。

同一幅图的右侧把结构描述接到局部环境。对每一帧，程序以1.5σ为半径，分别数每个头珠、中间尾珠和末端尾珠附近的溶剂珠，再对同类珠子平均。到505τ末帧，三者分别约为2.14667、0.52667和0.23333。头珠周围保留较多溶剂近邻，尾珠尤其是末端尾珠的溶剂接触明显减少，与坐标图中的尾部富集和头部外露相互呼应。这里的水化图像由简单溶剂珠表达，数值是几何邻居计数；若用真实水模型研究氢键，需要重新加入分子方向与供受体定义。

比较这三个数时，还应记住头尾的尺寸参数不同。用同一个几何半径有利于统一测量范围，但不同珠子周围可以容纳多少溶剂，也受到排斥范围和邻居分布的影响。因此，这里用它们共同说明实际模型中溶剂接近方式的变化；若要把差别拆成尺寸效应和化学亲和效应，可以设置尺寸相同而相互作用不同的对照，或者测量各类型的径向分布并选择对应的接触壳层。把测量定义和模型参数一起保留，后续的机制比较才有稳定的参照。

完整程序同时读取热力学记录与轨迹。它核对203帧的粒子身份、分子组成、固定盒和零z坐标，再计算三个团簇阈值、两种大小分布及溶剂近邻数。程序导出的CSV便于重新绘图，JSON保留定义和汇总，四张坐标图使用同一批真实帧。先运行默认分析，再尝试改变距离阈值或显示时间，可以把每次变化追溯到具体定义；只要不改原始轨迹，这些都是对同一个模拟结果的不同观察方式。

### 完整团簇、分布和溶剂接近分析

```
"""Analyze the official two-dimensional micelle model.

python analyze_micelle.py --run . --out figures --language en
Requires NumPy, SciPy, and Matplotlib.
All distances and times remain in the model's LJ reduced units.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    with path.open() as stream:
        while line := stream.readline():
            if line.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a timestep header.')
            step = int(stream.readline())
            if stream.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Expected an atom-count header.')
            count = int(stream.readline())
            if stream.readline().split() != ['ITEM:', 'BOX', 'BOUNDS', 'pp', 'pp', 'pp']:
                raise ValueError('Expected an orthogonal periodic cell.')
            box = np.array([list(map(float, stream.readline().split())) for _ in range(3)])
            names = stream.readline().split()[2:]
            values = np.array([list(map(float, stream.readline().split())) for _ in range(count)])
            if values.shape != (count, len(names)) or not np.isfinite(values).all():
                raise ValueError('Incomplete or non-finite atom records.')
            order = np.argsort(values[:, names.index('id')]); values = values[order]
            yield step, box, {name: values[:, i] for i, name in enumerate(names)}


def components(xy, mol, cutoff, lengths):
    ids = np.unique(mol); parent = {int(m): int(m) for m in ids}
    def find(m):
        while parent[m] != m:
            parent[m] = parent[parent[m]]; m = parent[m]
        return m
    for i, j in sorted(cKDTree(xy, boxsize=lengths).query_pairs(cutoff)):
        a, b = find(int(mol[i])), find(int(mol[j]))
        if a != b:
            parent[max(a, b)] = min(a, b)
    groups = {}
    for m in ids:
        groups.setdefault(find(int(m)), []).append(int(m))
    return sorted(groups.values(), key=lambda g: (-len(g), g[0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    names = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Source Han Sans SC', 'Noto Sans CJK SC',
                         'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in names]
    plt.rcParams.update({'font.family': fonts if args.language == 'zh' else ['DejaVu Sans'],
        'font.size': 12, 'svg.fonttype': 'path', 'axes.spines.top': False,
        'axes.spines.right': False, 'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2'})
    records = []; snapshots = {}; identities = None; maximum_z = 0.; final_groups = None
    thresholds = [.9, 1.2, 1.5]
    for step, box, data in frames(args.run / 'micelle.lammpstrj'):
        ids = data['id'].astype(int); typ = data['type'].astype(int); mol = data['mol'].astype(int)
        identity = np.column_stack([ids, typ, mol])
        if identities is None:
            identities = identity.copy(); initial_box = box.copy()
        if not np.array_equal(identity, identities) or not np.array_equal(box, initial_box):
            raise ValueError('Particle identity or the fixed cell changed.')
        if dict(zip(*np.unique(typ, return_counts=True))) != {1: 750, 2: 150, 3: 150, 4: 150}:
            raise ValueError('Expected 750 solvent beads and 150 three-bead amphiphiles.')
        for m in np.unique(mol[typ == 2]):
            if sorted(typ[mol == m].tolist()) != [2, 3, 4]:
                raise ValueError('Each amphiphile must contain types 2, 3, and 4.')
        xy = np.column_stack([data['x'], data['y']]) - box[:2, 0]
        lengths = box[:2, 1] - box[:2, 0]; xy %= lengths
        maximum_z = max(maximum_z, float(abs(data['z']).max()))
        tail = typ >= 3; row = [step, step * .005]
        for cutoff in thresholds:
            groups = components(xy[tail], mol[tail], cutoff, lengths)
            sizes = np.array([len(g) for g in groups])
            if sizes.sum() != 150:
                raise ValueError('Cluster membership must conserve all 150 amphiphiles.')
            row.extend([len(groups), int(sizes.max()), int((sizes == 1).sum()),
                        float(np.sum(sizes * sizes) / 150)])
            if cutoff == 1.2:
                final_groups = groups
        # Contacts count solvent beads using one common geometrical radius.
        distance = xy[typ == 1, None, :] - xy[None, typ >= 2, :]
        distance -= lengths * np.rint(distance / lengths)
        close = (np.sum(distance * distance, axis=2) <= 1.5 ** 2).sum(axis=0)
        amph_type = typ[typ >= 2]
        row.extend([float(close[amph_type == t].mean()) for t in [2, 3, 4]])
        records.append(row)
        if step in [0, 1000, 20000, 101000]:
            snapshots[str(step)] = {'time_tau': step * .005, 'xy': xy.tolist(),
                                    'types': typ.tolist(), 'mol': mol.tolist(),
                                    'lengths': lengths.tolist()}
    a = np.asarray(records); thermo = np.loadtxt(args.run / 'micelle-thermo.dat')
    if len(a) != 203 or not np.allclose(a[:, 0], np.arange(0, 101001, 500)) or maximum_z > 1e-10:
        raise ValueError('Expected 203 planar frames spanning 0 to 505 tau.')
    if thermo.shape[1] != 6 or not np.isfinite(thermo).all():
        raise ValueError('Expected six finite thermodynamic columns.')
    kinetic_error = float(abs(thermo[:, 4] - 1199 * thermo[:, 2]).max())
    total_error = float(abs(thermo[:, 3] + thermo[:, 4] - thermo[:, 5]).max())
    if kinetic_error > 1e-8 or total_error > 1e-8:
        raise ValueError('Whole-system energy normalization or 2D temperature is inconsistent.')
    sizes = np.array([len(g) for g in final_groups]); n = np.arange(1, 151)
    multiplicity = np.bincount(sizes, minlength=151)[1:]
    number_fraction = multiplicity / len(sizes); molecule_fraction = n * multiplicity / 150
    summary = {'frames': len(a), 'time_tau': [float(a[0, 1]), float(a[-1, 1])],
        'particle_types': {'solvent': 750, 'heads': 150, 'middle_tails': 150, 'end_tails': 150},
        'molecules': 150, 'dimensions': 2, 'cell_lengths_sigma': lengths.tolist(),
        'bead_areal_density': float(1200 / np.prod(lengths)),
        'amphiphile_areal_density': float(150 / np.prod(lengths)),
        'maximum_abs_z': maximum_z, 'mean_temperature_reduced': float(thermo[:, 2].mean()),
        'kinetic_identity_max_error': kinetic_error, 'energy_sum_max_error': total_error,
        'thresholds_sigma': thresholds,
        'initial_clusters': [int(a[0, 2 + 4*i]) for i in range(3)],
        'initial_largest': [int(a[0, 3 + 4*i]) for i in range(3)],
        'final_clusters': [int(a[-1, 2 + 4*i]) for i in range(3)],
        'final_largest': [int(a[-1, 3 + 4*i]) for i in range(3)],
        'final_singletons': [int(a[-1, 4 + 4*i]) for i in range(3)],
        'final_molecule_weighted_size': [float(a[-1, 5 + 4*i]) for i in range(3)],
        'final_sizes_at_1p2': sizes.tolist(),
        'final_number_mean_at_1p2': float(sizes.mean()),
        'final_molecule_mean_at_1p2': float(np.sum(sizes * sizes) / 150),
        'mean_solvent_contacts_at_1p5': a[:, -3:].mean(axis=0).tolist(),
        'final_solvent_contacts_at_1p5': a[-1, -3:].tolist(),
        'definition': 'Graph nodes are whole amphiphiles. An edge joins two different molecules '
                      'if any pair of their tail beads is within the stated periodic xy cutoff. '
                      'Connected components include isolated molecules. Time zero follows the soft '
                      'preparation; the original LJ interval ends at 5 tau and the extension ends at '
                      '505 tau. Contact counts measure solvent-bead proximity, not hydrogen bonds.'}
    (args.out / 'micelle_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    (args.out / 'micelle_snapshots.json').write_text(json.dumps(snapshots, separators=(',', ':')), encoding='utf-8')
    header = 'step,time_tau,' + ','.join(f'{v}_r{r}' for r in thresholds for v in
        ['clusters', 'largest', 'singletons', 'molecule_weighted_size']) + ',solvent_contacts_head,solvent_contacts_middle_tail,solvent_contacts_end_tail'
    np.savetxt(args.out / 'micelle_clusters.csv', a, delimiter=',', comments='', header=header)
    np.savetxt(args.out / 'micelle_size_distribution.csv', np.column_stack([n, multiplicity,
               number_fraction, molecule_fraction]), delimiter=',', comments='',
               header='size,multiplicity,cluster_number_fraction,molecule_fraction')

    def save(fig, name):
        fig.savefig(args.out / (name + '.svg'), bbox_inches='tight')
        fig.savefig(args.out / (name + '.png'), dpi=160, bbox_inches='tight'); plt.close(fig)
    colors = ['#976c25', '#176d83', '#b44e3f']
    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6), sharex=True, layout='constrained')
    ax[0].plot(thermo[:, 1], thermo[:, 2], color=colors[1], lw=.8, label=tr('保存的温度', 'Recorded temperature'))
    ax[0].axhline(.45, color=colors[2], ls='--', label=tr('目标 0.45', 'Target 0.45'))
    ax[0].set_ylabel('T*')
    ax[1].plot(thermo[:, 1], thermo[:, 3] / 1200, color=colors[1], label='U/N')
    ax[1].plot(thermo[:, 1], thermo[:, 4] / 1200, color=colors[0], label='K/N')
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'), ylabel=tr('能量 / (Nε)', 'Energy / (Nε)'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
        axis.grid(alpha=.15, axis='y')
    save(fig, 'micelle-thermo')

    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6.5), sharex=True, layout='constrained')
    for i, cutoff in enumerate(thresholds):
        for j in range(2):
            ax[j].step(a[:, 1], a[:, 2 + 4*i + j], where='post', color=colors[i], lw=1.5,
                       label=f'r = {cutoff:.1f} σ')
    ax[0].set_ylabel(tr('连通团簇数（含单分子）', 'Clusters\n(including single molecules)'))
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'),
              ylabel=tr('最大团簇的分子数', 'Largest cluster\n(molecules)'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, frameon=False)
        axis.grid(alpha=.15, axis='y')
    save(fig, 'micelle-clusters')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4), layout='constrained')
    occupied = multiplicity > 0
    ax[0].bar(n[occupied]-.2, number_fraction[occupied], width=.4, color=colors[1],
               label=tr('按团簇等权', 'Equal weight per cluster'))
    ax[0].bar(n[occupied]+.2, molecule_fraction[occupied], width=.4, color=colors[0],
               label=tr('按分子等权', 'Equal weight per molecule'))
    ax[0].set(xlabel=tr('团簇中的分子数 n', 'Molecules per cluster n'), ylabel=tr('比例', 'Fraction'))
    ax[0].legend(loc='lower left', bbox_to_anchor=(0, 1.01), fontsize=10, frameon=False)
    for i, label in enumerate([tr('头', 'Head'), tr('中间尾珠', 'Middle tail'), tr('末端尾珠', 'End tail')]):
        ax[1].plot(a[:, 1], a[:, -3+i], color=colors[i], label=label, lw=1)
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'),
               ylabel=tr('每珠平均溶剂近邻数（1.5σ）', 'Solvent neighbours / bead\n(within 1.5σ)'))
    ax[1].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, fontsize=9, frameon=False)
    save(fig, 'micelle-size-environment')

    fig, ax = plt.subplots(1, 4, figsize=(14, 4.1), layout='constrained')
    for axis, snap in zip(ax, snapshots.values()):
        xy = np.array(snap['xy']); types = np.array(snap['types']); mol = np.array(snap['mol'])
        for t, color, size, label in [(1,'#b7c4bf',4,tr('溶剂','Solvent')),(2,'#176d83',14,tr('头','Head')),
                                      (3,'#b28a35',10,tr('中间尾珠','Middle tail')),(4,'#b44e3f',7,tr('末端尾珠','End tail'))]:
            axis.scatter(xy[types == t,0],xy[types == t,1],s=size,color=color,label=label,linewidths=0)
        axis.set(xlim=(0,lengths[0]),ylim=(0,lengths[1]),xlabel='x / σ',title=f"t = {snap['time_tau']:g} τ")
        axis.set_aspect('equal')
    ax[0].set_ylabel('y / σ')
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=4,frameon=False,markerscale=2)
    save(fig, 'micelle-snapshots')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

运行python analyze_micelle.py --run . --out figures --language zh；只需要micelle-thermo.dat与micelle.lammpstrj。

## 让自组装模拟回答材料问题

这一例最直接显示的是头尾偏好与分子连接怎样共同推动平面内的分选。尾部聚到一起时，其周围的溶剂接触减少；头部仍与外侧环境相接；许多小的连通分量逐渐转为较少、较大的分量。热运动又不断改变接触，使分量数和最大分量大小在过程中起伏。这样的轨迹适合提出关于结构形成、几何接触和成员重排的问题。若要测量材料的真实扩散系数或组装速率，则应先给珠子建立物理时间标尺，并采用适合动力学测量的温控方式。

临界胶束浓度是另一个常见研究目标，它需要浓度方向上的信息。一个固定组成的盒子展示的是该条件下的聚集过程；要寻找浓度变化中的转折，可以设计多个组成，在每个组成下比较游离分子比例、聚集大小分布和时间稳定性，并设置独立初态。二维模型对应的是面浓度，真实三维溶液通常用体积浓度或物质的量浓度。将两者联系起来，需要明确模型映射和空间维度。这样，浓度扫描得到的转折才与所研究的材料体系有一致含义。

改变分子形状也是有用的研究方向。例如增加尾段数量、改变头部尺寸、加入第二条尾链或提高弯曲刚度，都会改变一个分子在聚集体中占据空间的方式。设计这些比较时，应保持共同的能量与长度标尺，明确改变哪些键、类型对参数和组成，并检查新初态是否存在紧密接触。当前三珠模型没有额外角势；若加入角势来表达刚性，应给出其平衡角、强度和作用的三原子顺序，再观察局部排列如何传递到整体形貌。

当一个聚集体变得接近盒子的尺度，周期环境也会参与结果。更大的盒子可以容纳更多分子与更多独立聚集体，但同时增加采样时间和计算工作量。一个可操作的比较是保持面浓度与分子参数不变，增大面积并相应增加分子数，查看团簇分布和局部溶剂接触是否保留相似特征；再用独立初态比较聚集体合并过程。观察时间同样要跟随研究目标延长。温度达到目标、势能变化变缓和团簇分布稳定分别描述不同层次，需要对应各自的曲线来判断。

这条学习路线最终把一段自组装动画变成可解释的研究记录：原始数据规定150个三珠分子，相互作用规定头尾对环境的偏好，轨迹展示真实的位置变化，连通图把几何接近转换为团簇，两种加权分布则说明分子与聚集体各自怎样分配。你可以从复算末帧的12个分量开始，继续检查0.9σ与1.5σ规则下的差别，再选择一个与材料问题对应的参数比较。每次扩展都保留对象身份、空间维度、单位和统计定义，聚集图像就能逐步转化为有清楚依据的结构认识。

## 延伸阅读与开放资料

- [LAMMPS examples/micelle, 30Sep2026 update1](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0-or-later

  二维头尾分子、原始坐标、相互作用与准备流程。

  增加全体系数值输出与轨迹，并在原1000步主段后延长100000步；分析和图解重新编写。
- [Colloidal electrolytes: Soap solutions and their constitution](https://doi.org/10.1021/ja01448a010) · James W. McBain and C. S. Salmon, 1920 · Historical research article; cited

  从肥皂溶液讨论带电聚集体的科学史。

  重绘测量与结构推断关系的原理图。
- [Colloids and Colloidal Electrolytes](https://www.nature.com/articles/107046a0) · J. W. McBain, 1921 · Historical research article; cited

  分子与胶体聚集体之间的尺度问题。

  将历史问题接到现代粗粒化模型的描述层次。
- [LAMMPS lj/cut pair style](https://docs.lammps.org/pair_lj.html) · LAMMPS developers · Official documentation; cited

  LJ势、类型对参数与绝对截断距离。

  明确比较实际头尾参数的势阱位置与保留区间。
- [LAMMPS two-dimensional simulations](https://docs.lammps.org/Howto_2d.html) · LAMMPS developers · Official documentation; cited

  xy运动、二维盒与enforce2d。

  结合实际二维自由度检查动能记录。
- [LAMMPS temp/rescale](https://docs.lammps.org/fix_temp_rescale.html) · LAMMPS developers · Official documentation; cited

  温度窗口、缩放频率与独立积分器的分工。

  以本例100步、0.02窗口和1.0比例解释实际温控。
- [LAMMPS harmonic bonds and special_bonds](https://docs.lammps.org/bond_harmonic.html) · LAMMPS developers · Official documentation; cited

  谐键参数约定；非键排除与键势分开理解。

  用两条三珠分子连接与0.1σ伸长算例说明。
