# 从单链走向熔体与溶液

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l08/
Language: zh-CN

把一条链放进许多条链组成的环境，逐步读懂浓度、排斥、内部尺寸与运动。

## 从一根线到一团线，问题发生了什么变化

一根鞋带可以在桌面上随意弯曲；把许多鞋带堆在一起，抽动其中一根就会带动或挤开周围的线。聚合物材料也有这种“自己的动作会碰到别人”的特点。塑料加热后能流动，浓的增稠剂溶液倒起来很慢，柔软的高分子涂层能让接近表面的物体感到阻力，这些现象都需要同时考虑许多条链。单链的回转半径仍然有用，但它周围还有多少链、邻居如何填充空间、整条链移动时受到哪些限制，已经成为同样重要的问题。

先分清两种常见环境。聚合物溶液含有链和溶剂，水溶液里的水会参与水化、传递动量，并改变链段之间相遇的代价。聚合物熔体则主要由聚合物链本身组成，邻近空间大多被别的链段占据。本节的实跑体系是一盒没有显式溶剂的珠簧链：80条链，每条20个珠子，共1600个珠子。它用密集链段之间的排斥和固定连接，帮助我们理解熔体的局部堆积与链运动。前面PEG在水中的原子模型，则提供了“水确实作为分子存在”的对照。

珠子数相同并不意味着两个模型代表同一种物质。这里的一个珠子是承担链段位置和质量的有效单元，没有被指定为某个氧乙烯重复单元，也没有携带氧、碳、氢的详细结构。这样做能把注意力集中在连接、体积排斥和浓度上。若研究目标是PEG的水化壳层或某种离子的配位，就需要恢复相应的化学分辨率；若研究的是链在拥挤环境中如何改变形状，珠簧模型能提供更清楚的机制比较。选择模型的起点，是待测量的物理量及其需要保留的信息。

还可以把“链占据的空间”与“珠子实际排开的体积”分开想。把柔软的线绕成一团，线团包围的范围中仍有空隙，另一根线可以穿入这些空隙；两个线团的空间范围重叠，不等于它们的线段彼此重合。高分子线团也是如此，回转半径描述的是珠子分布的尺度，而非一颗实心球的硬边界。随着链浓度增加，不同链的构象范围能够互相穿插，近距离处的排斥仍阻止珠子直接重叠。这个区别让我们理解：材料可以同时具有较大的单链尺寸和相当高的总体密度。

读完本节，你会完成从链坐标生成、温和消除重叠到读取熔体结构的一整条流程。分析会分三层进行：先检查温度和链尺寸怎样随时间变化，再区分同链近邻与异链近邻，最后把珠子的位移与整条链质心的位移分开。参考结果包含三个独立生成的初始构型，让我们看到同一规则下的实际差异。后续交联章节会在这套熔体上添加永久连接，因此这里也承担一个很实际的任务：建立清楚、可复用、各分支共同使用的起始状态。

## 为什么把原子变成珠子：长链运动提出的历史问题

长链运动有一个很容易被低估的困难：局部的一小段能够迅速弯曲，整条链却可能需要很久才换到新的位置。逐个追踪所有原子，计算会花在大量快速振动上；真正关心的整链重排，反而要等很长的模拟时间才能出现。一个自然的研究策略，是把若干局部自由度合并为较少的有效单元，同时保留相邻单元相连、不同单元难以占据同一位置这两条关键约束。这类粗粒化让科学问题从“每根化学键正在怎样振动”转向“连成长链之后，整体运动怎样改变”。

Kremer与Grest在1990年的珠簧熔体研究中比较了不同链长的运动，把短链较自由的重排与长链受周围链约束的运动放在同一模型框架下考察。历史上的重要进展，是让链长、连接和拥挤程度成为可以逐项改变的变量，再用轨迹检验相应的物理图像。下面的图把局部链段运动、整链移动和周围链形成的几何约束并排画出。图中的“管道”表示邻链约束形成的有效运动区域；真实材料里没有预先放置一根坚硬管子。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s2)

图 1 · Kremer与Grest的珠簧熔体研究把不同链长的运动置于同一可控框架。图示局部运动、整链移动与邻链约束的关系。

这也解释了为什么不能仅凭一张交错的链图就判断已经发生了强缠结。三维曲线投影到纸面上会自然交叉，交叉点未必对应空间接触；短链也能在空间里彼此穿插，却未必出现长链特有的慢松弛规律。本节每条链只有20个珠子，分析重点是局部堆积、有限长度链的尺寸和观察窗口内的位移。研究缠结时，需要把链长延长、记录链对自身取向的记忆如何消失，并用合适的拓扑与松弛分析检验机制。密集、交错、缠结分别描述不同层次的信息。

减少自由度也会改变模型怎样与周围交换动量。在显式水模型中，水分子通过碰撞和相互作用传递运动；这里的Langevin热浴则直接给珠子施加摩擦和随机力，用较简洁的方式维持热运动。两者都能产生温度，却具有不同的动力学细节。判断一种粗粒化方法是否适合研究流动、扩散或黏度，因而要同时看相互作用势和热浴，而不能只检查平均结构是否相似。历史上的简化模型之所以有价值，正在于它把保留的机制写得足够清楚，使每次比较都能对应一个具体的问题。

本节使用约化单位，把珠子直径参数σ、相互作用能量ε和珠子质量m分别作为长度、能量和质量的标尺。设σ=1，并不是说直径等于1nm，而是把所有长度写成σ的倍数。时间也用由这三把标尺组成的τ表示；温度T*=1表示热能尺度与ε相同。要与某个真实聚合物的纳米、秒和帕斯卡比较，需要用实验或更细模型的链尺寸、密度、松弛或扩散数据建立映射。直接给珠子随意指定一个原子名称，会绕过这一步最重要的物理对应。

## 连接与排斥各做一件事：读懂珠簧模型

先想象两颗没有连接的珠子。它们相隔很远时，这个模型不给它们作用力；靠得太近时，排斥会迅速变强，让重叠变得昂贵。我们采用Lennard–Jones势的排斥部分，把曲线在最低点截断，再整体上移，使截断位置的能量和力都接近零。这就是常说的WCA排斥。它保留珠子的有效体积，却没有远距离吸引尾部。因而本节的高密度来自规定的盒子体积，不能把“珠子靠得很密”读成已经计算了某种聚合物的气液共存或真实凝聚能。

只保留短距离排斥式 1

![只保留短距离排斥](https://ml-biomat.com/static/agent-math/c26582e3fc3c240160a5435b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U_{WCA} | 普通珠对的WCA势能 | ε |
| r | 两珠中心距离 | σ |
| ε | 能量标尺，本例约化值1 | 能量 |
| σ | 长度标尺，本例约化值1 | 长度 |
| 2^(1/6)σ | 截断位置，约1.122462σ | σ |
| 12, 6, 1/6 | 幂指数；1/6表示六次方根 | 1 |
| =, +, −, / | 等于、加、减、相除；相邻量相乘 | 1 |
| <, ≥, { } | 小于、大于等于；按距离选择一行 | 1 |

怎样理解原LJ最低点处能量为−ε，加上ε后恰好归零；最低点的斜率也是零，所以这一截断同时保留能量与力的连续性。

算一个例子取ε=σ=1、r=1，方括号为1−1=0，U=1；当r=2^(1/6)时，U=0，继续增加距离仍为0。

使用条件本节的非键势是纯排斥WCA；直接相连珠子的同类排斥包含在键势中。

再考虑沿链相邻的两颗珠子。它们既不能挤到一起，也不能无限分开，所以键势需要同时处理短距离排斥和大距离拉回。LAMMPS的FENE键在非线性弹性项之外，已经包含同样的短程WCA排斥。非线性项中的R₀是允许伸展的上限尺度，和“平衡键长”不是一个概念。取K=30、R₀=1.5、ε=σ=1时，两项竞争形成的最低点接近0.96σ，参考坐标生成时使用0.97σ作为初始相邻间距。把R₀直接当成所有键该有的长度，会把体系放到势能陡增的危险区域。

FENE弹性与短程排斥共同决定键长式 2

![FENE弹性与短程排斥共同决定键长](https://ml-biomat.com/static/agent-math/91873c7546e438279238523f.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U_{bond} | 完整键势能 | ε |
| K | 非线性弹性强度，本例30 | ε/σ² |
| R₀ | 最大伸展尺度，本例1.5；不是平衡键长 | σ |
| r | 相邻珠子距离 | σ |
| U_{WCA} | 前式定义的短程排斥 | ε |
| ln | 自然对数，括号内必须是正的无量纲数 | 1 |
| ² | 某个量与自身相乘 | 1 |
| =, −, +, /, 1/2 | 等于、负号或相减、加、相除和二分之一；并列量相乘 | 1 |
| < | 小于；规定可用距离范围 | 1 |

怎样理解靠近R₀时对数的自变量接近0，负对数迅速增加，形成很强的拉回作用；短距离处WCA又阻止两珠塌到一起。两种趋势竞争产生有限的最佳间距。

算一个例子K=30、R₀=1.5、r=1时，弹性项为19.83780ε，WCA为1ε，完整键能为20.83780ε；其最低点约在0.961σ。

使用条件固定连接的珠簧键，参数与LAMMPS bond_style fene一致。接近R₀需要充分小的积分步长；化学断键需另行建模。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s3)

图 2 · 各曲线按解析势函数逐点评估。完整键势包含一份WCA排斥，普通非键项对直接相连珠对的权重设为0。

相邻珠子的排斥既然已经算在键势里，就要避免在普通珠对势里再算一次。输入中的special_bonds fene把直接相连的1–2珠对的普通非键相互作用权重设为0，而相隔两根键的1–3珠对、相隔三根键的1–4珠对保留完整权重。这里的1–2、1–3和1–4描述沿连接图相隔几步，不是珠子类型编号。链内相隔较远的珠子和不同链的珠子也按普通WCA势相互作用。这样一张连接表就能影响哪些邻居进入哪一项能量，而无需再给每组连续珠子写角度或二面角势。

解析珠对与键势：读取给定距离处的能量和沿距离增大方向的力。

[Figure: 解析势能曲线](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s3)

沿距离方向的力由势能的负斜率给出；正值排开，负值拉近。练习固定ε=σ=1、R₀=1.5σ，逐点计算解析函数。

FENE这个名称里的“有限伸展”也有明确的计算含义。随着距离接近R₀，势能和拉回力迅速增大，合理的时间步会让轨迹在这一区域之前被强烈拉回。它不是检测到某个长度就自动断开的化学键，当前连接表在整个计算过程中保持不变。如果出现异常长键，应检查初始重叠、时间步、加力速度和温控过程，让数值积分能够解析剧烈的力变化。研究真正的键断裂，则需要能够改变连接或描述反应的模型，并重新定义相应参数与能量过程。

上面的交互练习可以分别查看普通珠对、FENE弹性项与完整键势。先把距离放在σ附近，观察排斥和拉回怎样相互竞争；再逐步接近1.5σ，看看键势为什么越来越陡。改变K会改变拉回的强弱，也会改变两项平衡的位置。这个操作是在解析函数上读取能量和力，便于把输入参数与曲线联系起来。真正的熔体还会让许多邻居同时施力，温度使距离不断波动，因此轨迹里的键长形成一条分布，而不是全部停在单独一根键的最低点。

## 怎样把80条链放进同一个盒子

盒子大小先由珠子数和数密度决定。数密度回答“单位体积里有多少个珠子”，与按克和立方厘米计算的质量密度相关，却需要分开命名。本例1600个珠子的约化数密度是0.85，因此立方盒子的边长约12.347σ。每条链的中心位置可以遍布盒子，相邻珠子则沿随机方向走一步。周期边界允许一条链跨过盒子的左右两侧；坐标文件会同时保存盒内位置与跨越次数，使连接关系和后续尺寸计算保持连续。

从数密度算盒长式 3

![从数密度算盒长](https://ml-biomat.com/static/agent-math/d03f1fad6700a0503ff8092c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ρ | 珠子数密度 | σ⁻³ |
| N | 盒内总珠子数，本例1600 | 1 |
| L | 立方盒边长 | σ |
| ³, 1/3 | 三次方给体积；三次方根由体积恢复长度 | 1 |
| =, / | 等于、相除 | 1 |

怎样理解立方盒体积为边长的三次方，珠子数除以体积就是数密度；把等式换个顺序便可反求盒长。

算一个例子1600÷0.85=1882.35294σ³，取三次方根得到L=12.34715838σ；单位质量珠子的质量密度数值也为0.85，但单位是m/σ³。

使用条件正交立方周期盒；此处σ是模型长度标尺。

随机放置不会自动生成合理的液体结构。假设把很多细线直接撒进一个小盒子，某些线段可能挤得过近；计算中同样会出现很大的初始排斥。生成器先要求新珠子与已放入的珠子至少相隔0.65σ，并以0.97σ的步长连接同一条链。这能排除最严重的坐标重合，却仍允许比正常WCA接触更近的间距。接受一个位置之前，要用最近周期镜像的距离检查周围珠子，否则盒子两侧看似相隔很远的珠子，实际上可能在周期拼接后靠在一起。

### 生成初始的80条链

```
"""Generate 80 chains of 20 beads at reduced number density 0.85.

The default seed reproduces the first reference configuration. A bead is a
coarse-grained segment with mass 1, not a specified chemical repeat unit.
"""
from pathlib import Path
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=20263001)
    parser.add_argument('--output', type=Path, default=Path('initial.data'))
    args = parser.parse_args()
    count, chain_length, density = 1600, 20, 0.85
    length = (count/density)**(1/3)
    rng = np.random.default_rng(args.seed)
    coordinates, bonds = [], []
    for chain in range(count//chain_length):
        current = rng.uniform(0, length, 3)
        for local in range(chain_length):
            for attempt in range(100000):
                if local == 0:
                    candidate = rng.uniform(0, length, 3)
                else:
                    direction = rng.normal(size=3)
                    candidate = current + 0.97*direction/np.linalg.norm(direction)
                if coordinates:
                    delta = np.array(coordinates)-candidate
                    delta -= length*np.round(delta/length)
                    if np.min(np.sum(delta*delta, axis=1)) < 0.65**2:
                        continue
                break
            else:
                raise RuntimeError('No acceptable next bead; change the packing protocol.')
            coordinates.append(candidate.copy())
            current = candidate
            if local:
                bonds.append((len(coordinates)-1, len(coordinates)))
    lines = ['Generated FENE chain starting configuration', '',
             f'{count} atoms', f'{len(bonds)} bonds', '',
             '1 atom types', '2 bond types', '',
             f'0 {length:.15g} xlo xhi', f'0 {length:.15g} ylo yhi',
             f'0 {length:.15g} zlo zhi', '', 'Masses', '', '1 1.0', '',
             'Atoms # bond', '']
    for i, position in enumerate(coordinates):
        image = np.floor(position/length).astype(int)
        wrapped = position-length*image
        lines.append(f'{i+1} {i//chain_length+1} 1 ' +
                     ' '.join(f'{v:.15g}' for v in wrapped) + ' ' +
                     ' '.join(str(v) for v in image))
    lines += ['', 'Bonds', '']
    lines += [f'{j+1} 1 {left} {right}' for j, (left, right) in enumerate(bonds)]
    args.output.write_text('\n'.join(lines)+'\n', encoding='utf8', newline='\n')
    print(f'{count} beads, {len(bonds)} bonds, box length {length:.8f} sigma')


if __name__ == '__main__':
    main()
```

用最近周期距离检查新珠子，并保存分子编号、连接与镜像。

接下来要给这些链一个温和整理空间的机会。准备阶段暂时使用有限高度的soft排斥，逐渐增加排斥强度，同时用谐和键把相邻珠子的间距维持在0.97σ附近。这个阶段持续40τ，以较小的0.002τ步长推进。随后切换到完整的WCA与FENE相互作用，做能量最小化，再以0.005τ步长记录100τ的热运动。三段各有任务：缓慢排开近邻、修整切换后的局部几何、观察正式模型下的运动。势函数在中途改变，所以不能把整个准备流程连成一段定哈密顿量的平衡轨迹。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s4)

图 3 · 准备阶段按任务使用不同势函数。100τ记录从完整FENE/WCA模型启用后的最小化状态开始。

### 从soft整理到FENE熔体记录

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 20263101 mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263201 zero yes
variable softA equal ramp(0,100)
fix soften all adapt 1 pair soft a * * v_softA
timestep 0.002
thermo 1000
thermo_style custom step temp pe ke etotal
run 20000
unfix soften
unfix dyn
unfix bath
write_data after-soft.data
pair_style lj/cut 1.122462048309373
pair_modify shift yes
pair_coeff * * 1 1 1.122462048309373
bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0
min_style cg
min_modify dmax 0.01
minimize 1e-8 0.01 10000 100000
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263301 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 20000
write_restart melt.restart
write_data melt.data
```

完整准备输入：40τ的温和整理、相互作用切换、最小化与100τ记录。

### 运行三个独立初始构型

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=1
mkdir melt-runs
for replica in 1 2 3; do
  folder="melt-runs/n1600-rep${replica}"
  mkdir "$folder"
  python make_melt.py --seed "$((20263000 + replica))" --output "$folder/initial.data"
  python - "$replica" "$folder" <<'PY'
from pathlib import Path
import sys
replica = int(sys.argv[1])
destination = Path(sys.argv[2])
text = Path('prepare.lmp').read_text(encoding='utf8')
for offset in [100, 200, 300]:
    text = text.replace(str(20263001 + offset), str(20263000 + replica + offset))
(destination/'prepare.lmp').write_text(text, encoding='utf8', newline='\n')
PY
  ( cd "$folder"; "$lmp" -in prepare.lmp -log simulation.log > stdout.log 2>&1 )
done
python analyze_melt.py melt-runs --output figures --language en
```

在包含初始生成器、准备输入和分析程序的目录运行。几何种子与三个速度/热浴种子按构型编号改变，其他条件相同；输出保存在新建的melt-runs目录。

生成文件中的分子编号也值得停下来理解。一个珠子的编号用于确认“始终是这一个珠子”，分子编号则用于说明它属于哪条原始链。原子类型在此全部相同，表示珠子采用同一套质量和非键参数；键类型另行指定连接所用的参数。文件预留了两种键类型，本节实际只使用第一种，后续交联使用第二种以便区分连接身份。这些整数都不是空间坐标，也不直接决定颜色或化学元素。把身份、分组和相互作用类别分开，后面读取网络数据时就不会把画面中的颜色变化误认成新物质。

运行后会得到melt.data和melt.restart，它们把当前状态保存下来，分别便于阅读结构和继续同版本计算。thermo.dat记录温度、每珠能量、压力分量和盒长；chain-rg.dat把80条链各自的回转半径保留下来；trajectory.lammpstrj保存位置、速度与周期镜像。不要只看一个总平均就丢掉逐链记录：若某几条链仍明显偏伸展，它们可能被平均值掩盖。后续的交联、拉伸和重复比较都从这些共同定义的记录出发，观察到差异时才能追溯到具体操作。

## 温度稳定以后，还要看链是否记得初始形状

开始看结果时，先把横轴的起点认清。这里的0τ位于soft整理、相互作用切换和最小化之后，曲线记录的是完整FENE/WCA模型下随后100τ的运动。最小化主要改变位置，并不会自动把速度分布调整到新的平衡状态；刚开始的一小段时间里，势能和动能仍会交换，热浴也会补充或带走能量。因此温度先出现过渡，再围绕目标值波动，是一个可以从准备步骤理解的现象。把过渡段与后面的观察窗口标出来，比只报告整段平均温度更容易看清过程。

### 温度与逐链尺寸的实际变化

三组1600珠熔体记录；横轴从正式FENE/WCA最小化后的0τ开始，浅色区域为50–100τ分析窗口。

LAMMPS 30 Sep 2026 Update 1；官方珠簧相互作用模型，1600个珠子、80条20珠链，ρ*=0.85、T*=1，三个初始构型；FENE/WCA正式动力学时间步0.005τ。

[下载参考数据与完整输入（ZIP） 5.92 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-melt-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s5)

三组初始构型各自经过40τ软排斥整理和FENE/WCA最小化，再从0τ开始记录100τ的正式珠簧动力学。图中分别保留各组温度与80条链的平均回转半径；浅色背景标出50–100τ统计窗口。

温度只反映速度平方的统计，链的整体形状则需要许多珠子协同改变。两者的调整速度可以相差很大。实际图中同时画出了80条链平均回转半径随时间的变化，并保留三个独立初始构型的曲线。若温度已经在1附近波动，而平均尺寸仍在缓慢变化，就应继续观察尺寸，而不是用温度曲线代替构象检查。即使平均尺寸看起来平稳，也可以进一步比较前后时间段的分布、较长链段的内部距离和链的取向相关性；它们从不同尺度询问体系还保留多少初始记忆。

为了让每个统计都有确定的范围，后面的结构和位移分析使用50–100τ这一段。轨迹每2.5τ保存一次，所以这个窗口包含21帧；每一帧又有80条链。它们提供了1680个链构象记录，但同一条链相邻时刻的形状通常相关，邻链之间也共享相互作用环境。1680因此是记录数，不是独立重复实验数。三个初始构型的结果分开绘制，便于区分同一盒内部的构象宽度与重新准备一盒材料后的差异。这个区别会在后面设计交联比较时继续发挥作用。

分布图中的纵轴是概率密度，不能直接读成某一个精确尺寸出现的概率。例如横轴按0.1σ分箱，某一箱的柱高为2σ⁻¹，那么这一箱的面积是0.2，对应约20%的构象记录。改变分箱宽度会改变柱子的高度与细节，所以比较三组构型时使用同一套箱边界。平均尺寸相同也不保证分布相同：一组总在3σ附近，另一组在2σ与4σ之间切换，它们平均值相近，却反映不同的构象自由度。读图时先看整体宽度，再观察是否存在可重复的峰或尾部变化。

第一组构型在这个窗口内的平均回转半径约为2.151σ，均方根回转半径约为2.184σ，而均方根末端距离约为5.262σ。这三个数没有矛盾：回转半径统计所有珠子相对于链中心的分布，末端距离只选择两端；“先平方再平均再开方”又比“直接平均长度”更重视较大的构象。查看分布图时，会看到同一条20珠链能够有许多尺寸，单个平均数无法画出它们全部的形状。比较不同模型或链长时，应把尺寸定义与取平均的次序一起写出来。

## 珠子的邻居是谁：把链内结构与链间堆积分开

一张熔体快照里，珠子都挤在一起，很难判断最近的邻居来自哪里。可以把观察方式换成“站在一颗珠子上，数不同距离处有多少珠子”。距离落在某个薄球壳里的珠对越多，说明那里越容易出现邻居。为了让不同距离能够公平比较，要除以球壳体积：半径较大的球壳本来就容得下更多点。再与相同珠子数和体积下均匀分布的期望值比较，就得到径向分布函数g(r)。它把拥挤的三维快照转化为可比较的距离统计。

用球壳体积归一化珠对计数式 4

![用球壳体积归一化珠对计数](https://ml-biomat.com/static/agent-math/d97e947f56a13d96efd6989d.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| g(r) | 壳内平均径向分布 | 1 |
| r | 球壳中心半径 | σ |
| V | 盒子体积 | σ³ |
| C(r) | J帧中落入该壳的无序珠对总数，每对每帧只数一次 | 1 |
| J | 参与统计的帧数，本例每个构型21 | 1 |
| N | 每帧珠子数，本例1600 | 1 |
| N(N−1)/2 | 不同无序珠对的总数 | 1 |
| ΔV | 薄球壳的精确体积 | σ³ |
| r₊, r₋ | 球壳外半径与内半径 | σ |
| π | 圆周率，约3.14159 | 1 |
| ³ | 三次方 | 1 |
| =, /, −, 2, 4/3 | 等于、除、减；2把无序计数与总珠对数匹配，4/3来自球体体积；并列量相乘 | 1 |

怎样理解均匀分布时，一对珠子落入球壳的机会由壳体积占盒体积的比例给出；实测计数除以这个期望便得到相对结构。

算一个例子若N=100、J=10、V=1000σ³、ΔV=1σ³，则均匀参照期望49.5个无序珠对；实测99个给g=2。

使用条件均匀体相、球壳外半径小于最短盒边的一半。本例用几何距离统计全部珠对，再按连接身份拆分；各组共享总珠对分母。

这里进一步把珠对分成三组：直接用一根键相连的珠对、同一条链上其余的珠对、来自不同链的珠对。三组都使用相同的总珠对归一化，所以三条曲线相加恰好得到总g(r)。直接成键的珠对会在正常键长附近贡献窄峰；其他珠对则反映链内折返或周围链的堆积。分析坐标时，我们主动把直接成键的几何距离也统计进去。这与计算普通非键力时排除1–2珠对是两件事：一个决定怎样计数结构，一个决定能量分项如何避免重复。

### 同链与异链的空间结构

珠对曲线平均三组构型的50–100τ记录，各组身份贡献相加为总g(r)；内部距离分别保留三组。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s6)

左图把总珠对分布分解为直接成键、同链其他珠对和不同链珠对；三项使用同一个总珠对归一化，逐点相加得到总g(r)。右图按沿链键数比较内部均方距离，虚线为独立等长步的参照值。

从空间距离回到连接关系，还可以沿链数“相隔几根键”。选择珠子i与i+s，求它们空间距离的平方，再对所有允许的起点、所有链和所有选定帧取平均，就得到内部距离S(s)。当s=1时，它就是平均键长平方；当s=19时，20珠链只剩两端这一对，得到平均末端距离平方。中间的s值让我们逐步放大观察尺度。这样即使两个体系具有相似的总回转半径，也能检查它们在短链段与长链段上的展开方式是否相同。

沿链相隔s根键时的平均平方距离式 5

![沿链相隔s根键时的平均平方距离](https://ml-biomat.com/static/agent-math/ade091bf31e82f669343332a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| S(s) | 内部距离的平方平均 | σ² |
| s | 沿链的键间隔，1至19 | 1 |
| J, j | 帧数与帧编号 | 1 |
| M, a | 链数与链编号，本例M=80 | 1 |
| n | 每链珠子数，本例20 | 1 |
| i | 沿链的起点编号 | 1 |
| rₐ,ᵢ⁽ʲ⁾ | 第j帧、第a条链第i珠的连续解包位置向量 | σ |
| Σ | 把所列帧、链和起点的结果逐一相加 | 1 |
| \| \|² | 向量三个分量的平方之和 | σ² |
| =, +, −, / | 等于、加、减、除；并列量相乘 | 1 |

怎样理解相隔s根键时，每条n珠链有n−s个合法珠对，乘以链数和帧数就是平均的分母。

算一个例子四珠链位于(0,0)、(1,0)、(1,1)、(2,1)，s=2时两对距离平方都是2，所以S(2)=2；s=3时只剩两端，S(3)=5。

使用条件固定顺序、相同珠子数的线性链；先依据镜像展开整条链。此统计均匀计数珠对，不给不同构象额外权重。

径向分布中的峰也要结合它的定义理解。g(r)大于1说明相对于均匀参照，该距离更容易找到另一颗珠子；它不表示那里一定有吸引力。直接相连的珠子受到键约束，即使普通非键势完全是排斥的，也会在某个键长附近频繁出现。反过来，某个距离上的g(r)接近零，可能来自体积排斥或连接几何。结构分布汇集了所有相互作用和可达构象的共同结果，不能把每个峰简单当成一项独立势能。先区分珠对身份，再结合具体模型，才容易把图上的结构与机制连起来。

如果每一步的方向完全独立、步长统计相同，许多随机方向的交叉项平均后会抵消，S(s)就随s成正比。图中把S(s)除以sS(1)，用水平的1作为这一简单参照。本例的实际曲线高于1，说明链段方向及排斥形成的空间相关，使有限链段的展开超过了独立步图像。第一组构型在s=19处的S约为27.690σ²，而19S(1)约为17.699σ²。这个比较说明模型里的珠子不能逐个当成互不相关的随机步；它并没有要求每个珠子都对应一个统计独立的Kuhn链段。

## 一颗珠子动得快，为什么整条链仍移动得慢

观察一条链时，可以同时看到两种运动：珠子围绕链中心重新排列，链中心本身也在改变位置。前一种运动会让局部结构变化，却不一定把整条链运到远处。想象一群人手拉手站成一串，每个人都能移动脚步或转身，而整串人的中心位置取决于所有人的共同变化。这个类比帮助区分局部运动与整体平移，但模拟中的珠子没有主动意图，它们由相互作用、惯性和热浴共同推动。把两种位移分别计算出来，才能知道一条轨迹中的“活跃”主要发生在哪个尺度。

### 相同链长的不同构象尺寸

每组统计21帧中的80条链；柱面积归一到1，记录之间存在时间与链间相关。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s7)

50–100τ内每组21个保存时刻、每帧80条链的尺寸分布。每条直方图的面积归一为1，三组构型分开绘制；同一链的相邻时刻与同一盒中的邻链均具有相关性。

平均平方位移先选一个时间间隔，再把相隔这段时间的两个位置相减，求向量长度的平方，最后平均。平方让相反方向的移动都计入运动量，避免左移与右移相互抵消。珠子的平均平方位移对所有珠子求平均，链质心的平均平方位移则先求每条链的中心，再对链求平均。我们的程序还去掉了整个盒子的共同平移，避免所有珠子一起漂移时产生一个与内部输运无关的贡献。周期镜像用于把位置解包，使越过盒子边缘的珠子继续沿原来的路径计量。

去掉整体漂移后测量平均平方位移式 6

![去掉整体漂移后测量平均平方位移](https://ml-biomat.com/static/agent-math/56f33b9ed71e4007019c4f13.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| MSD | 平均平方位移 | σ² |
| Δt | 两帧之间的时间间隔 | τ |
| t | 位移的起始时间 | τ |
| rᵢ | 第i珠的解包位置向量；分析链中心时换成该链中心 | σ |
| R_{box} | 同一帧全体等质量珠子的平均位置 | σ |
| r̃ᵢ | 减去盒子整体位置后的坐标 | σ |
| ⟨ ⟩ᵢ,ₜ | 对所有测量对象与可用时间起点取平均 | 1 |
| \| \|² | 位移向量分量的平方相加 | σ² |
| =, +, − | 等于、相加、相减 | 1 |

怎样理解去掉共同平移后，平方使各个方向的位移都按运动量累计；再平均得到给定时间间隔上的尺度。

算一个例子两颗珠子在同一时间间隔的去漂移位移为(1,0,0)σ和(−1,0,0)σ，平均位移为0，MSD却是(1+1)/2=1σ²。

使用条件本例50–100τ窗口，等质量、固定盒子，最大间隔25τ；重叠时间起点之间具有相关性。

### 珠子位移与链质心位移

解包坐标去掉整体平移，50–100τ内采用全部可用起点，最大间隔25τ；每条线保留一组构型。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/#zh-s7)

先用周期映像编号重建连续坐标，再移除盒内全部珠子的整体平移。珠子与链质心的均方位移使用50–100τ内所有可用起点，最大时间间隔25τ；这些短间隔记录描述本段轨迹上的局部与整链运动。

在50–100τ窗口内，对每个允许的起点都计算同样的时间间隔，可以提高有限记录的利用率。时间间隔越大，可用的起点越少，因此这里最多画到25τ。第一组构型在25τ间隔下，珠子的平均平方位移约2.569σ²，而链质心约0.568σ²。珠子通过内部弯曲和转动移动了更多距离，整链中心仍然走得较少。不同颜色保留不同初始构型的结果，实线和虚线分别对应珠子与链中心。

多个时间起点让我们能更稳定地描述这段轨迹，却不会凭空增加独立材料样本。以25τ间隔为例，50τ与75τ、52.5τ与77.5τ等位移共享相邻的运动过程；它们不是完全无关的实验。这也是为什么图中保留三个独立初始构型，而没有只画一条光滑平均线和极窄的误差带。若需要估计统计不确定性，可以按足够长的连续时间块分别计算，并比较不同初始构型的结果。误差的计算单位要与独立性的来源相对应：粒子、链、时间块和独立体系承担不同的角色。

从位移曲线提取扩散系数，还需要找到足够长时间下接近线性的区间，并检查拟合范围、相关性和重复差异。短时惯性、内部松弛及周围链的约束都可能让曲线弯曲。这里先保留实际位移随时间间隔变化的形状，不强行把整段拟合为一条直线。若后续目标是与某种材料的扩散实验比较，可延长无变形条件下的记录，再建立约化时间与实际时间的映射。Langevin阻尼也属于动力学模型的一部分；改变它可能改变运动速度，即使静态尺寸看起来相近。

## 让模型回答材料问题：熔体、溶液与下一步比较

完整分析程序把上述测量连接起来：先按原子编号排序，读取周期镜像并恢复连续坐标，再按每20个珠子的分子编号分组。回转半径会与LAMMPS保存的逐链数值逐项核对；珠对统计在最近周期镜像下计算，沿链内部距离和位移则使用解包坐标。这种区别很实用：数周围最近的邻居时要看周期环境，量一条完整链或累计行走距离时要保留它的连续形状。用同一种坐标处理替代所有任务，很容易让某个结果在盒子边缘出现人为跳变。

### 完整的结构与位移分析

```
"""Read chain packing, internal dimensions and motion from FENE melt records.

python analyze_melt.py records --output figures --language en
records may contain one prepare.lmp run, or n1600-rep1/2/3 subdirectories.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_trajectory(file):
    frames, steps, lengths = [], [], []
    with file.open(encoding='utf8') as stream:
        while stream.readline():
            step = int(stream.readline())
            assert stream.readline().startswith('ITEM: NUMBER')
            count = int(stream.readline())
            assert stream.readline().startswith('ITEM: BOX BOUNDS pp pp pp')
            box = np.array([list(map(float, stream.readline().split())) for _ in range(3)])
            fields = stream.readline().split()[2:]
            rows = np.array([list(map(float, stream.readline().split())) for _ in range(count)])
            rows = rows[np.argsort(rows[:, fields.index('id')])]
            assert np.array_equal(rows[:, 0], np.arange(1, count+1))
            assert np.array_equal(rows[:, fields.index('mol')], np.arange(count)//20+1)
            length = box[:, 1]-box[:, 0]
            position = rows[:, [fields.index(q) for q in ['x', 'y', 'z']]]
            images = rows[:, [fields.index(q) for q in ['ix', 'iy', 'iz']]]
            frames.append(position+images*length)
            steps.append(step)
            lengths.append(length)
    return np.array(steps), np.array(frames), np.array(lengths)


def native_rg(file):
    records = {}
    lines = [s for s in file.read_text().splitlines() if s and not s.startswith('#')]
    i = 0
    while i < len(lines):
        step, count = map(int, lines[i].split())
        records[step] = np.array([float(s.split()[1]) for s in lines[i+1:i+count+1]])
        i += count+1
    return records


def inspect(folder):
    steps, positions, lengths = read_trajectory(folder/'trajectory.lammpstrj')
    assert np.allclose(lengths, lengths[0])
    n = positions.shape[1]
    chain_count = n//20
    time = steps*0.005
    chains = positions.reshape(len(steps), chain_count, 20, 3)
    centers = chains.mean(axis=2)
    rg = np.sqrt(np.mean(np.sum((chains-centers[:, :, None])**2, axis=-1), axis=-1))
    end = chains[:, :, -1]-chains[:, :, 0]
    re = np.linalg.norm(end, axis=-1)
    native = native_rg(folder/'chain-rg.dat')
    error = max(np.max(np.abs(native[int(s)]-v)) for s, v in zip(steps, rg))
    if error > 0.0001:
        raise ValueError('Gyration reconstruction differs from the native record.')
    late = time >= 50
    internal = np.array([np.mean(np.sum((chains[late, :, s:]-chains[late, :, :-s])**2,
                                       axis=-1)) for s in range(1, 20)])
    # Geometrical pair distributions include directly bonded neighbors. Divide
    # unordered pair counts by N(N-1)/2 times shell-volume / box-volume.
    left, right = np.triu_indices(n, k=1)
    same = left//20 == right//20
    bonded = same & (right-left == 1)
    edges = np.linspace(0, 6, 121)
    counts = np.zeros((3, len(edges)-1))
    for frame in positions[late]:
        delta = frame[right]-frame[left]
        delta -= lengths[0]*np.round(delta/lengths[0])
        distance = np.linalg.norm(delta, axis=1)
        for row, selection in enumerate([bonded, same & ~bonded, ~same]):
            counts[row] += np.histogram(distance[selection], edges)[0]
    shell = 4*np.pi*(edges[1:]**3-edges[:-1]**3)/3
    pair_g = counts * (2*np.prod(lengths[0])) / (late.sum()*n*(n-1)*shell)
    # Remove whole-box translation before bead and molecular COM displacement.
    pos = positions[late]
    pos = pos-pos.mean(axis=1, keepdims=True)
    com = pos.reshape(len(pos), chain_count, 20, 3).mean(axis=2)
    maxlag = (len(pos)-1)//2
    msd = np.array([[np.mean(np.sum((pos[lag:]-pos[:-lag])**2, axis=-1)),
                     np.mean(np.sum((com[lag:]-com[:-lag])**2, axis=-1))]
                    for lag in range(1, maxlag+1)])
    thermo = np.loadtxt(folder/'thermo.dat')
    summary = dict(beads=n, chains=chain_count, beads_per_chain=20,
                   box_length_sigma=lengths[0].tolist(),
                   density=float(n/np.prod(lengths[0])), frames=len(steps),
                   late_window_tau=[50, 100], late_frames=int(late.sum()),
                   mean_rg_sigma=float(rg[late].mean()),
                   rms_rg_sigma=float(np.sqrt(np.mean(rg[late]**2))),
                   rms_re_sigma=float(np.sqrt(np.mean(re[late]**2))),
                   mean_bond_square_sigma2=float(internal[0]),
                   mean_re2_over_mean_rg2=float(np.mean(re[late]**2)/np.mean(rg[late]**2)),
                   native_rg_max_error_sigma=float(error),
                   late_mean_T=float(thermo[thermo[:, 1] >= 50, 2].mean()),
                   late_max_bond_sigma=float(thermo[thermo[:, 1] >= 50, -1].max()),
                   internal_distance_sigma2=internal.tolist(),
                   lag_tau=(np.arange(1, maxlag+1)*2.5).tolist(),
                   bead_msd_sigma2=msd[:, 0].tolist(), com_msd_sigma2=msd[:, 1].tolist())
    return dict(time=time, rg=rg, re=re, late=late, internal=internal,
                pair_r=(edges[1:]+edges[:-1])/2, pair_g=pair_g, msd=msd,
                thermo=thermo, summary=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    folders = [args.records] if (args.records/'trajectory.lammpstrj').exists() else sorted(args.records.glob('n1600-rep[123]'))
    if not folders:
        raise ValueError('No melt preparation records found.')
    results = [inspect(folder) for folder in folders]
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    def tr(a, b): return a if zh else b
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in installed],
                         'font.size': 13, 'axes.titlesize': 15,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6'})
    colors = ['#167d84', '#c16b3d', '#466eaa']
    def save(fig, name):
        fig.savefig(args.output/f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png', bbox_inches='tight', dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), layout='constrained')
    for i, record in enumerate(results):
        thermo = record['thermo']
        label = tr(f'初始构型 {i+1}', f'Initial configuration {i+1}')
        axes[0].plot(thermo[:, 1], thermo[:, 2], color=colors[i], lw=1, label=label)
        axes[1].plot(record['time'], record['rg'].mean(axis=1), color=colors[i], label=label)
    axes[0].axhline(1, color='#536168', ls='--', lw=1)
    axes[0].set(ylabel='T*', title=tr('模型切换后的 100τ：温度与链尺寸分别检查',
                                     '100τ after changing the model: temperature and chain size'))
    axes[1].set(ylabel=tr('80 条链的平均 Rg / σ', 'Mean Rg of 80 chains / σ'),
                xlabel=tr('时间 / τ', 'Time / τ'))
    for ax in axes:
        ax.axvspan(50, 100, color='#167d84', alpha=.06)
        ax.legend(frameon=False, fontsize=11)
    save(fig, 'melt-preparation')
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout='constrained')
    labels = [tr('直接相连', 'Directly bonded'), tr('同链其余珠对', 'Other same-chain pairs'),
              tr('不同链珠对', 'Different-chain pairs')]
    mean_g = np.mean([r['pair_g'] for r in results], axis=0)
    for j, label in enumerate(labels):
        axes[0].plot(results[0]['pair_r'], mean_g[j], label=label, color=colors[j])
    axes[0].plot(results[0]['pair_r'], mean_g.sum(axis=0), color='#163840', ls='--', label=tr('总和', 'Sum'))
    axes[0].set(xlim=(.7, 3.2), xlabel='r / σ', ylabel=tr('对 g(r) 的贡献', 'Contribution to g(r)'),
                title=tr('近邻既来自自身链，也来自周围链', 'Neighbors within and between chains'))
    axes[0].legend(frameon=False, fontsize=11)
    rg_edges = np.linspace(0, np.ceil(max(r['rg'].max() for r in results)*2)/2, 31)
    re_edges = np.linspace(0, np.ceil(max(r['re'].max() for r in results)*2)/2, 31)
    for i, r in enumerate(results):
        axes[1].plot(np.arange(1, 20), r['internal']/(np.arange(1, 20)*r['internal'][0]),
                     color=colors[i], label=tr(f'构型 {i+1}', f'Configuration {i+1}'))
    axes[1].axhline(1, ls='--', color='#536168', label=tr('独立等长步的参照', 'Independent-step reference'))
    axes[1].set(xlabel=tr('沿链相隔的键数 s', 'Separation along chain, s bonds'),
                ylabel='S(s) / [s S(1)]', xticks=[1, 5, 10, 15, 19],
                title=tr('内部距离：逐段查看链怎样展开', 'Internal distances across chain scales'))
    axes[1].legend(frameon=False, fontsize=11)
    save(fig, 'melt-structure')
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), layout='constrained')
    for i, r in enumerate(results):
        label = tr(f'构型 {i+1}', f'Configuration {i+1}')
        axes[0].hist(r['rg'][r['late']].ravel(), bins=rg_edges,
                     density=True, histtype='step', lw=2, color=colors[i], label=label)
        axes[1].hist(r['re'][r['late']].ravel(), bins=re_edges,
                     density=True, histtype='step', lw=2, color=colors[i], label=label)
    for ax, name in zip(axes, ['Rg', 'Re']):
        ax.set(xlabel=f'{name} / σ', ylabel=tr('概率密度 / σ⁻¹', 'Probability density / σ⁻¹'))
        ax.legend(frameon=False, fontsize=11)
    axes[0].set_title(tr('50–100τ：回转半径的分布', '50–100τ: distribution of gyration radii'))
    axes[1].set_title(tr('50–100τ：末端距离的分布', '50–100τ: distribution of end distances'))
    save(fig, 'melt-dimensions')
    fig, ax = plt.subplots(figsize=(11, 5), layout='constrained')
    for i, r in enumerate(results):
        lag = np.arange(1, len(r['msd'])+1)*2.5
        label = tr(f'构型 {i+1}', f'Configuration {i+1}')
        ax.plot(lag, r['msd'][:, 0], color=colors[i], label=label+' '+tr('珠子', 'beads'))
        ax.plot(lag, r['msd'][:, 1], '--', color=colors[i], label=label+' '+tr('链质心', 'chain COM'))
    ax.set(xlabel=tr('时间间隔 Δt / τ', 'Lag time Δt / τ'),
           ylabel=tr('平均平方位移 / σ²', 'Mean squared displacement / σ²'),
           title=tr('50–100τ 窗口内的位移：珠子与整链', 'Displacement within 50–100τ: beads and whole chains'))
    ax.legend(frameon=False, ncols=2, fontsize=11)
    save(fig, 'melt-motion')
    summary = {'replica_count': len(results), 'replicas': [r['summary'] for r in results],
               'pair_normalization': '2 V times unordered pair counts / [frames N(N-1) shell volume]; all three pair classes share this denominator and add to total g(r).',
               'msd_definition': 'Unwrapped positions, whole-box translation removed; average over chains/beads and every available time origin in 50–100 tau, maximum lag25tau.'}
    (args.output/'melt_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    np.savetxt(args.output/'pair_structure.csv', np.c_[results[0]['pair_r'], mean_g.T], delimiter=',',
               header='r_sigma,bonded_contribution,same_chain_other_contribution,different_chain_contribution', comments='')
    print(json.dumps([r['summary'] for r in results], indent=2))


if __name__ == '__main__':
    main()
```

给定单个运行目录可分析一组构型；给定包含n1600-rep1、n1600-rep2和n1600-rep3的目录会保留三组曲线。--language zh生成中文图。

现在再看“从熔体走向溶液”应怎样实施。若要显式加入水，必须为链与水分别建立相容的相互作用、质量和连接模型，并处理它们之间的交叉参数；前面的PEG/SPC/Fw例子演示了这一类流程。若采用隐式溶剂，则把溶剂的部分作用放入有效链段势、摩擦和随机力中，再用目标条件下的链尺寸、渗透或动力学数据校准。单纯把本例盒子放大，会得到更稀疏的珠簧链体系。它改变了珠子浓度，却没有自动生成真实水的氢键、离子屏蔽或流体动量传递机制。

做材料比较时，一次先改变一个能说清楚的因素。例如保持总珠子数和数密度相同，改变每条链的长度，就必须相应调整链的条数；如果固定链数而增加链长，又保持盒子不变，密度也同时增加，结果会混合两个效应。比较溶剂品质时，固定温度并不够，还要明确调整了哪一类链段间或链段与溶剂间作用。比较不同初始构型时，则保持相同的制备程序和观测窗口，让差异主要反映结构与采样。表面上只是修改输入中的一行，物理上改变的对象可能远不止一个。

一个适合继续深入的小研究，是保持每链20珠和相互作用不变，比较几种数密度下的内部距离与链间近邻。为每个密度重新建立盒子、使用同样的整理流程，再增加观察时间直到关注的结构量变化可控。这样可以研究拥挤本身的影响。另一个问题是相同密度下不同链长的运动，这就需要让记录时间随慢松弛增加，而不是给所有链长机械使用同样步数。研究问题越具体，越容易决定哪一张图应该保持不变、哪一个量需要重新测量，以及下一次计算最应该花在哪里。

本节建立的共同起点是一种密集、无显式溶剂、固定链连接的模型材料。它已经能够回答近邻来自哪条链、短链段如何展开、局部运动与整体平移如何分开这些问题。接下来添加交联时，我们保留同一批珠子、同一个初始盒子和同一套链段相互作用，只改变永久连接的数量及其位置。这样就能把问题推进为：哪些链被连成共同网络，连接如何改变松弛，以及拉伸后的力学响应怎样与网络结构对应。每一步都从清楚定义的上一层出发，复杂材料问题便能逐渐拆成可计算、可检查的关系。

## 延伸阅读与开放资料

- [FENE bead–spring benchmark: bench/in.chain (30 Sep 2026 Update 1)](https://github.com/lammps/lammps/blob/develop/bench/in.chain) · LAMMPS developers · LAMMPS source repository: GPL-2.0. This lesson uses the interaction model with independently generated coordinates and preparation/analysis scripts.

  FENE珠簧熔体的开源输入基础；固定采用30 Sep 2026 Update 1官方归档中的bench/in.chain。

  1600珠，80条链、每链20珠，ρ*=0.85；精确WCA截断、soft整理、时间步从0.012τ降至0.005τ，Langevin阻尼时间从10τ改为1τ；三组初始构型与结构分析。
- [LAMMPS 30 Sep 2026 Update 1 source archive](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · LAMMPS source software: GPL-2.0.

  本讲采用的固定发行源码包；其中bench/in.chain定义原始珠簧基准。

  输入适配与具体参数变化列于珠簧基准条目。
- [Dynamics of entangled linear polymer melts: A molecular-dynamics simulation](https://doi.org/10.1063/1.458541) · Kurt Kremer and Gary S. Grest · Research citation; publisher copyright. Figures in this lesson are original conceptual illustrations.

  珠簧模型、链长与运动约束之间的历史联系。

  重组为局部运动、整链运动与邻链约束的教学图。
- [bond_style fene — LAMMPS documentation](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  完整FENE键势、参数和特殊珠对设置。

  补充符号、算例、图解与实际输入对应。
- [special_bonds — LAMMPS documentation](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  1–2、1–3和1–4相互作用权重。

  补充符号、算例、图解与实际输入对应。
- [pair_style soft — LAMMPS documentation](https://docs.lammps.org/pair_soft.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  通过可调软排斥准备近邻结构。

  补充符号、算例、图解与实际输入对应。
