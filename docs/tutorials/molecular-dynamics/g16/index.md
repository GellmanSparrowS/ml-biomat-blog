# 给膜接上聚合物：从稀疏线团到拥挤外衣

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g16/
Language: zh-CN

比较两种PEG接枝比例，用真实轨迹理解表面密度、质量分布、末端高度与初始构象的影响。

## 给脂质膜穿上一层会运动的外衣

一根聚乙二醇链在水里可以弯曲、回折、伸展；把它的一端接到脂质上，情况会怎样？脂质的两条疏水尾留在膜中，亲水的聚合物链伸向水，像浮在水面的一个小锚牵着柔软的绳子。许多这样的分子共同组成一层可移动的表面覆盖物。研究者关心覆盖物伸出多远、分布是否均匀、附近的水和其他分子能否进入。这些问题与脂质载体表面设计、界面润湿和生物分子的接近过程有关，也把前面学到的单链构象与膜结构连接在了一起。

“接枝”指链的一端通过化学连接固定在另一种分子或表面上。本节的固定对象是一个脂质分子，因此接枝点仍能随脂质在膜上移动、上下起伏；它没有被钉在空间的一个坐标上。可以把这层表面想成一排系在小浮台上的软绳：浮台之间能交换位置，绳子也各自改变形状。若只看某一时刻的最高端点，会把偶然伸得很长的一条绳子当成整个覆盖层的高度。合理的测量需要同时看链的整体质量分布、末端位置和不同链之间的差异。

接枝稀疏时，一条链身边有较多空间，可以向侧面展开并回到接枝点附近；接枝变密时，相邻链可占据的空间发生重叠，链的构象与周围溶剂共同重新安排。常用的“蘑菇”和“刷子”图像由此而来：前者强调较独立的线团，后者强调密集接枝带来的向外伸展。真正的分子刷始终在热运动中，链与链之间也没有整齐的空隙。把它画成一把笔直的牙刷容易记住名称，却会遗漏链的回折、相互穿插和末端高度分布这些决定测量结果的细节。

本节比较两块含有相同数量脂质锚定分子的平面膜：每块膜共200个，分布在两个叶片，每个叶片100个。其中一种膜有5%的脂质连接PEG，另一种有25%。每条PEG都包含50个EO建模重复单元及一个羟基末端，链的长度保持一致，改变的是接枝分子数量。我们在300 K、1 bar下分别记录20 ns粗粒化动力学，读取每个时刻的膜面积、链质量平均高度、末端高度与回转半径，看看“链更多”究竟如何反映在这些不同指标中。

这两条记录也提供了一个很实际的研究练习：较密的体系从更向外伸展的初始链构象开始，较稀的体系采用自由生长的初始构象，因此分析时需要把密度、初始构象和松弛时间一起考虑。我们会沿着实际曲线判断链在观察窗口中如何变化，把统计窗口固定在后10 ns，并保留各条链的轨迹。这样得到的结果可以直接用于选择后续重复模拟的长度和初始构象，也能帮助判断哪一种“高度”最适合回答具体的表面问题。

## 从脂质载体实验到可以构建的分子外衣

把亲水聚合物接到脂质上的思路，与人们希望改变脂质载体在生物环境中的行为紧密相关。1990年，Klibanov及合作者研究了含有PEG连接脂质的脂质体，比较其在血清中的表现和体内循环过程。脂质体是由脂质双层包围起来的小囊泡，内部和外部都可以有水；改变外表面组成，相当于改变这个小囊泡首先与环境接触的部分。这类实验把一个具体问题推到了前面：表面少量化学修饰，为什么可能改变整个载体的行为？

要沿着这个问题继续深入，就需要观察实验平均值背后的分子安排。2011年，Lee与Pastor利用粗粒化PEG模型研究含PEG脂质的组装结构，联系聚合物参数、组成和不同聚集形态。对本节而言，这段历史最有用的启发是尺度的连接：原子尺度的信息帮助定义链段如何相互作用，较大的粗粒化体系则让更多链和脂质能够一起运动。不同年代模型的映射和参数各有定义，使用今天的Martini 3时，需要按当前实际文件核对化学连接与相互作用。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s2)

图 1 · PEG脂质研究中的三个尺度：载体实验、粗粒化组装与可重复的分子构建。图形为相应科学问题的概念示意。

随着研究对象越来越复杂，构建模型本身成为一个科学步骤。先搭出膜，再给指定脂质连接几十个单元的链，既要保持化学顺序，也要减少严重重叠。2022年介绍的Polyply框架把分子连接关系、参数片段和坐标生长结合起来，使这类结构能够按明确规则生成。我们使用其中PEG化脂质膜的构建方法：INSANE先放置脂质，Polyply补充链，随后由动力学让整个体系松弛。三个步骤各有职责，构建时给出的生长方向只决定起点，后面的运动由力场和运行条件决定。

理解链为什么伸展，可以先从“能有多少种摆法”入手。同一条软绳能够以许多弯曲方式占据接枝点附近的空间；一旦邻居变多，部分摆法因拥挤而变得代价较高。链向水的一侧重新分布，可能减轻拥挤，同时也减少了自由回折的选择。溶剂与链段之间的亲和程度又影响哪种分布更合适。这里的竞争涉及构象熵和相互作用能，单纯把接枝链想成相互推开的刚杆，很难解释为何末端仍会回落到接枝点附近。

科学史在这里串起了三个可操作的问题：实验要求我们关心表面功能，分子模型要求我们说明哪些相互作用被保留，构建工具则要求我们明确如何得到起始结构。下面将这三个问题落实到一对可测量的体系中。膜是平面的周期模型，水和离子参与运动，PEG与脂质有固定的共价连接；蛋白吸附、血液成分与整个载体的循环过程属于更大的研究层次，若研究目标走向这些行为，就需要把相应分子、曲率和观测时间接入模型。

## 认清一个接枝分子：珠子、质量和电荷

本节把PEG连接的脂质分子命名为PEL。它由一个POPE脂质片段、50个EO单元和一个OHter末端组成，共63个粗粒化珠子：脂质片段12个，聚合物部分51个。作为背景膜的另一种脂质是POPC。两个名字中的PC与PE对应不同的极性头部，连接聚合物所需的拓扑由具体的连接参数定义。Polyply命令中的序列直接列出这些片段，因此读懂这行序列就能知道生成的是哪一种分子，而不必根据最终图片猜测化学组成。

珠子名称、珠子类型和化学电荷是三个不同字段。PEL的连接珠名称仍叫NH3，但其实际类型是P5，电荷为零；相邻的PO4珠子类型是Q5，电荷为−1个元电荷，因此整个PEL净电荷为−1。名称保留了拓扑中的识别作用，真正参与静电计算的是电荷列。低接枝体系含10个PEL，需要10个正一价钠离子中和；高接枝体系含50个PEL，需要50个钠离子。把这项计数写清楚，有助于在运行前发现误用未连接脂质电荷的情况。

质量也要从当前模型读取。50个EO珠子每个质量为45 u，末端OH珠子质量为36 u，选入链尺寸分析的51个珠子总质量为2286 u。这里的质量是动力学与质量加权测量使用的模型质量；把所有珠子一律当成相同质量，会让末端获得不同权重。后面计算链的质量中心、质量平均高度和回转半径时，都使用这套实际质量。脂质锚定部分另外承担膜中的连接作用，其12个珠子不加入PEG尺寸的求和范围。

同一套构建流程还指定了一个重要的交叉相互作用：PEG珠子的SN3r类型与磷酸基Q5类型之间，Lennard–Jones参数ε取3.0 kJ/mol，长度参数σ保持0.43 nm。ε控制势阱深度，也影响相应距离上的力；降低ε会减弱该对珠子的吸引井深。这里沿用PEG化膜模型规定的数值，并保留其余参数。本节使用脂质v1文件及与之配套的连接规则，上一节DSPC所用的2025脂质v2属于另一组参数组合，文件替换需要重新检查连接与相互作用的一致性。

PEG与磷酸基的一对非键相互作用式 1

![PEG与磷酸基的一对非键相互作用](https://ml-biomat.com/static/agent-math/f54c3700fad433a3ffb76d13.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| U(r) | 距离r处未平移的LJ势能 | kJ/mol |
| r, rₘᵢₙ | 珠子间距离；势阱最低处距离 | nm |
| ε | 该对类型的势阱深度，取3.0 | kJ/mol |
| σLJ | LJ长度参数，取0.43；与接枝密度不同 | nm |
| σLJ/r | 距离的无量纲比 | 1 |
| 4, 2, 6, 12, 1/6 | 常数、幂指数；上标表示乘方 | 1 |
| =, −, /, ( ), [ ] | 相等、相减、相除、先计算括号内容；相邻量相乘 | 1 |

怎样理解短程正项快速上升，较远处的负项产生吸引井；ε改变井深，σLJ定义距离尺度。

算一个例子σLJ=0.43 nm时，最低处r约0.48266 nm，未平移势能为−3.0 kJ/mol。运行输入另在截断处作势能平移。

使用条件此式解释指定类型对的LJ项；完整模型还含静电及成键项，运行采用1.1 nm截断。

下面的程序定位这唯一一行交叉参数，核对长度和原始能量值，再写入规定的ε。若文件已经包含3.0，它会保持现有内容；若读到意外的参数，则报告具体差异，方便检查下载文件的版本。这种小程序把“调整某个相互作用”变成了可检查的具体操作。运行前在基础准备页完成Polyply与INSANE的建模工具安装，再把本节提供的四个Martini参数文件放在工作目录中，后续拓扑生成与动力学就会使用同一组定义。

### 设置PEG与磷酸基交叉参数

```
"""Apply the PEG–phosphate interaction specified by the Polyply tutorial.

The Q5–SN3r Lennard-Jones epsilon becomes 3.0 kJ/mol; sigma stays 0.43 nm.
Running this on an already corrected file leaves its bytes unchanged.
"""
from pathlib import Path
import argparse
import math

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, default=Path("martini_v3.0.0.itp"))
    args = parser.parse_args(); lines = args.file.read_text().splitlines()
    matches = []
    for index, line in enumerate(lines):
        fields = line.split(";")[0].split()
        if len(fields) == 5 and set(fields[:2]) == {"Q5", "SN3r"}:
            matches.append((index, fields))
    if len(matches) != 1:
        raise ValueError("Expected exactly one Q5–SN3r pair entry")
    index, fields = matches[0]
    if not math.isclose(float(fields[3]), .43, abs_tol=1e-10):
        raise ValueError("Unexpected pair sigma")
    old = float(fields[4])
    if math.isclose(old, 3.0, abs_tol=1e-10):
        print("Q5–SN3r already uses epsilon 3.0 kJ/mol and sigma 0.43 nm")
    elif math.isclose(old, 4.175, abs_tol=1e-10):
        lines[index] = " ".join([*fields[:4], "3.0"])+" ; PEG-phosphate correction prescribed by original Polyply tutorial"
        args.file.write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
        print("Q5–SN3r epsilon: 4.175 -> 3.0 kJ/mol; sigma retained at 0.43 nm")
    else:
        raise ValueError("Pair parameters differ from both defined input states")
```

核对唯一类型对与原参数，应用规定的ε值。

运行时还会同时出现成键参数和非键参数。前者规定PEG内部相邻珠子如何连接、键角如何改变以及连接脂质时采用哪种局部几何；后者规定没有直接化学连接的珠子怎样相互吸引或排斥。链能够保持连续，主要依靠拓扑中的成键项，而它愿意靠近水、磷酸基还是其他链段，又取决于相应的非键项。改变某一对非键参数不会自动重新生成链的连接关系，因此检查时要分别确认“接对了”和“相互作用选对了”这两层问题。

## 把链接到正确的脂质上

构建从一块8 nm×8 nm的膜开始。INSANE按输入的相对组成放置POPC和POPE，实际得到每个叶片100个脂质；低比例每叶片有95个POPC和5个POPE，高比例则是75个与25个。随后POPE会成为PEL的锚定部分，Polyply从它的连接珠向外补齐PEG。坐标文件中的分子排列与拓扑的分子排列必须一致，因为GROMACS按顺序把坐标赋给拓扑中的原子。数目正确但顺序错位，也会把本该属于PEG的参数分配给别的坐标。

下面的程序逐个读取脂质，保存真实排列，按连续出现的分子种类写出拓扑计数。它还利用头部坐标判断每个锚位于哪一叶片，为高接枝构建指定向水侧生长的方向。每条生长约束都指向正确的系统分子编号，因此即使POPC和PEL交替排列，也能找到对应链。当前盒子是正交盒，九数形式中六个非对角项都为零，程序将其写成等价的三个边长，便于坐标生成工具读取；膜的位置和盒子大小在这个表示转换中保持一致。

### 按坐标顺序建立分子拓扑

```
from pathlib import Path
from itertools import groupby
from collections import Counter
import json
lines=Path('bilayer.gro').read_text().splitlines();n=int(lines[1]);atoms=lines[2:2+n]
box=[float(v) for v in lines[-1].split()]
if len(box)==9:
    assert all(abs(v)<1e-12 for v in box[3:]),'This construction uses an orthorhombic box'
    lines[-1]=' '.join(f'{v:10.5f}' for v in box[:3]);Path('bilayer.gro').write_text('\n'.join(lines)+'\n')
groups=[list(v) for _,v in groupby(atoms,key=lambda l:l[:10])]
assert all(len(g)==12 for g in groups)
phosphates=[float(l[36:44]) for l in atoms if l[10:15].strip()=='PO4'];mid=sum(phosphates)/len(phosphates)
species=[];report=[];build=[]
for i,g in enumerate(groups):
    name=g[0][5:10].strip();assert name in ['POPC','POPE'];species.append('PEL' if name=='POPE' else name)
    head=next(l for l in g if l[10:15].strip() in ['NC3','NH3']);z=float(head[36:44]);side=1 if z>mid else -1
    report.append(dict(index=i,original=name,molecule=species[-1],head_z_nm=z,leaflet=side))
    if name=='POPE':build.append(f'[ molecule ]\nPEL {i} {i+1}\n[ rw_restriction ]\nEO 0 100 0 0 {side} 90\n')
top=''.join(f'#include "{s}"\n' for s in ['martini_v3.0.0.itp','martini_v3.0.0_ions_v1.itp','martini_v3.0.0_solvents_v1.itp','martini_v3.0.0_phospholipids_v1.itp','PEL.itp'])
top+='[ system ]\nPEGylated membrane\n[ molecules ]\n'
top+=''.join(f'{name} {len(list(g))}\n' for name,g in groupby(species))
Path('system.top').write_text(top);Path('growth.bld').write_text('\n'.join(build))
Path('bilayer-audit.json').write_text(json.dumps(dict(lipids=len(groups),molecules=dict(Counter(species)),midplane_nm=mid,leaflet_counts={str(side):dict(Counter(r['molecule'] for r in report if r['leaflet']==side)) for side in [-1,1]},molecule_order=report),indent=2))
```

逐分子核对组成、叶片与高比例生长范围。

低接枝比例使用自由随机生长，高比例使用朝外半空间中的随机生长，以减少初始链之间严重穿插和堆叠。可以把这一步理解为给一团软线选择合理的起始摆法：摆法会影响最初的松弛过程，却不会在后续动力学中持续命令链朝某个方向移动。高接枝盒子在法向取33 nm，低接枝取20 nm，为初始链和水层留出空间。两步建模都使用各自同一个盒高，使膜中面与后续水层定位保持一致。

随机种子使一次构建中的抽样序列明确。下面的短程序在调用Polyply前设置Python和NumPy的随机状态；完整构建脚本分别使用固定的INSANE种子和链生长种子，并将参数生成、膜生成、分子顺序检查和链生长串起来。种子解决的是同一实现中的随机选择，软件版本、参数库和输入结构也共同决定生成过程。阅读脚本时可以沿着文件流追踪：脂质参数先生成PEL拓扑，脂质坐标随后补成带链坐标，最后写出动力学所需的运行设置。

### 固定坐标生长随机状态

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

设置Python与NumPy种子后调用Polyply。

### 从脂质片段生成完整带链膜

```
#!/usr/bin/env bash
set -euo pipefail
fraction=${1:-5}
case "$fraction" in
  5) height=20; other=95; growth=() ;;
  25) height=33; other=75; growth=(-b growth.bld) ;;
  *) echo "Choose 5 or 25 percent PEL" >&2; exit 2 ;;
esac
export INSANE_SEED=$((20261600 + fraction))
python patch_interaction.py
polyply gen_params -f martini_v3.0.0_phospholipids_v1.itp -lib martini3 -o PEL.itp -name PEL -seq POPE:1 EO:50 OHter:1 > topology-generation.log 2>&1
insane -l "POPC:$other" -l "POPE:$fraction" -o bilayer.gro -dz "$height" -x 8 -y 8 -pbc rectangular > insane.log 2>&1
python build_topology.py
python seeded_polyply.py "$((20261650 + fraction))" gen_coords -p system.top -o polymer-bilayer.gro -res EO OHter -c bilayer.gro -name PEGylated -box 8 8 "$height" -split POPE:HEAD-NH3:TAIL-PO4,GL1,GL2,C1A,D2A,C3A,C4A,C1B,C2B,C3B,C4B "${growth[@]}" > coordinate-generation.log 2>&1
python write_parameters.py --fraction "$fraction"
```

传入5或25，分别构建低比例与高比例；先完成基础准备页的建模工具安装。

构建命令中的split选项尤其值得读一次。它将连接珠与脂质其余部分分开标识，让新链能够从正确的连接位置开始生成，同时保留已有脂质的空间结构。它没有切断最终拓扑中的化学连接。类似地，res选项告诉程序哪些残基需要补坐标，已经放置好的脂质仍作为建模参照。将这些选项与生成文件中的63个珠子逐一对应，就能看清一条看似很长的命令如何分别处理“已有部分”“新添部分”和“二者的接点”。

本节参考包同时包含已经构建好的两组带链膜，可以从它们直接进入溶剂化步骤。若从头重建，请在两个分别存放公共脚本和参数的目录中运行构建脚本，参数分别传入5与25；若从提供的结构继续，则将对应fraction目录中的带链坐标、系统拓扑和叶片审计文件复制到各自工作目录。两条路径使用相同的化学模型。比较轨迹时保留所选择的初始结构，尤其要记录高比例的朝外生长条件，因为后面的高度曲线会清楚显示这一条件留下的松弛过程。

## 让水、离子、链和膜一起松弛

把水盒叠加到带链膜周围时，几何填充工具可能在疏水尾部核心留下少量水珠。这个区域最初应由脂质尾占据，因此我们以初始膜中面为中心，去掉法向距离小于1.5 nm的水珠，再按保留数量更新拓扑。程序只改变水的初始放置，脂质与PEG的坐标保持原样。这个1.5 nm是本例构建的核心排水半厚度，与随后从轨迹测得的聚合物高度属于不同定义；它也没有作为生产阶段的外加排斥墙存在。

### 清理初始膜核心的水珠

```
from pathlib import Path
import json
lines=Path('water-added.gro').read_text().splitlines();n=int(lines[1]);atoms=lines[2:2+n];box=[float(x) for x in lines[-1].split()]
mid=json.loads(Path('bilayer-audit.json').read_text())['midplane_nm']
kept=[];removed=0;water=0
for l in atoms:
    iswater=l[5:10].strip()=='W'
    dz=float(l[36:44])-mid;dz-=box[2]*round(dz/box[2])
    if iswater and abs(dz)<1.5:removed+=1;continue
    if iswater:water+=1
    kept.append(l[:15]+f'{(len(kept)+1)%100000:5d}'+l[20:])
Path('solvated.gro').write_text('PEGylated membrane with tail core excluded from water placement\n'+f'{len(kept):5d}\n'+'\n'.join(kept)+'\n'+lines[-1]+'\n')
Path('topol.top').write_text(Path('system.top').read_text()+f'W {water}\n')
Path('solvation-audit.json').write_text(json.dumps(dict(water_beads_before=water+removed,water_beads_after=water,removed_tail_core_beads=removed,excluded_half_thickness_nm=1.5,midplane_nm=mid),indent=2))
```

按初始中面排除1.5 nm半厚度内的W珠，并更新数量。

完成排水和电荷中和后，5%体系包含10575个珠子：190个POPC、10个PEL、7655个水珠和10个钠离子；25%体系包含16198个珠子：150个POPC、50个PEL、11198个水珠和50个钠离子。水珠采用当前Martini水模型，一颗W珠汇总多个水分子的行为。两体系水层高度不同，水珠数量也随之不同。我们把比较对象放在每条链和每叶片面积上，计算时逐项归一化，从而使单纯的链数量或总盒体积不会直接放大所画出的高度分布。

初始链段之间可能存在较近接触，因此先最小化，再逐渐增大动力学步长。本例依次运行20 ps的2 fs步长准备、100 ps的5 fs步长松弛、2 ns的20 fs步长准备，最后记录20 ns。能量最小化寻找附近较低势能的构型，动力学准备让速度、溶剂和链构象一起调整。步长增大依赖本例粗粒化势的时间尺度和实际运行稳定性；把同样数值直接用于含原子级快速振动的体系，会改变数值积分的适用条件。

所有动力学阶段采用300 K温控和1 bar半各向同性压力耦合，横向两个方向共同调整，法向可以分别响应。静电采用介电常数15的反应场处理，实空间截断为1.1 nm，邻居表范围1.35 nm；这组条件应与Martini参数一起阅读。每个阶段的完整设置由下面的程序写出，温压耦合状态通过检查点连续传入下一阶段。生产段保存201个结构帧，时间从0到20 ns、间隔0.1 ns，足够观察这次记录中的慢变化和链间差异。

### 写出每个动力学阶段的完整设置

```
"""Write full MDP inputs for the 5 or 25 percent PEL membrane."""
from pathlib import Path
import argparse

EM = """integrator = steep
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
"""

BASE = """integrator = md
dt = 0.02
nsteps = 1000000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 500
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
ref-t = 300
gen-vel = no
gen-temp = 300
gen-seed = 20261625
pcoupl = c-rescale
pcoupltype = semiisotropic
tau-p = 4.0
ref-p = 1 1
compressibility = 3e-4 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261658
continuation = yes
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fraction", type=int, choices=[5, 25], required=True)
    parser.add_argument("--out", type=Path, default=Path("."))
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    values = dict(line.split(" = ", 1) for line in BASE.splitlines())
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    stages = [("preflight", ".002", 10000), ("relax", ".005", 20000),
              ("equil", ".02", 100000), ("md", ".02", 1000000)]
    for index, (stage, dt, steps) in enumerate(stages):
        parameters = dict(values)
        parameters.update(dt=str(float(dt)), nsteps=str(steps))
        parameters["gen-vel"] = "yes" if index == 0 else "no"
        parameters["gen-seed"] = str(20261620+args.fraction)
        parameters["ld-seed"] = str(20261650+args.fraction+index)
        parameters["continuation"] = "no" if index == 0 else "yes"
        content = "".join(f"{key} = {value}\n" for key, value in parameters.items())
        (args.out/f"{stage}.mdp").write_text(content, encoding="utf-8", newline="\n")
    print("Wrote em, preflight, relax, equil, and md parameter files")
```

--fraction 5或25写出与对应实际运行一致的五份MDP。

### 溶剂化、中和、松弛与记录

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python=${PYTHON:-python3}
"$gmx" solvate -cp polymer-bilayer.gro -cs water.gro -radius 0.21 -o water-added.gro > solvate.log 2>&1
"$python" clean_water.py
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'W\n' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -neutral -seed 20261601 > genion.log 2>&1
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f preflight.mdp -c em.gro -p topol.top -o preflight.tpr > preflight.grompp.log 2>&1
"$gmx" mdrun -deffnm preflight -ntmpi 1 -ntomp 2 -pin off > preflight.stdout.log 2>&1
prev=preflight
for stage in relax equil md; do
  "$gmx" grompp -f "$stage.mdp" -c "$prev.gro" -t "$prev.cpt" -p topol.top -o "$stage.tpr" > "$stage.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "$stage" -ntmpi 1 -ntomp 2 -pin off > "$stage.stdout.log" 2>&1
  prev=$stage
done
printf 'Temperature\nPotential\nPressure\nVolume\nDensity\nBox-X\nBox-Y\nBox-Z\n0\n' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

从带链膜坐标与系统拓扑开始，逐阶段传递检查点。

### 从提供的带链膜启动一次完整计算

```
#!/usr/bin/env bash
set -euo pipefail
fraction=${1:-5}
case "$fraction" in 5|25) ;; *) echo "Choose 5 or 25" >&2; exit 2 ;; esac
mkdir -p "work/$fraction"
cp martini_v3.0.0.itp martini_v3.0.0_ions_v1.itp \
   martini_v3.0.0_solvents_v1.itp martini_v3.0.0_phospholipids_v1.itp \
   PEL.itp water.gro clean_water.py write_parameters.py run.sh "work/$fraction/"
cp "fraction-$fraction/polymer-bilayer.gro" \
   "fraction-$fraction/system.top" "fraction-$fraction/bilayer-audit.json" "work/$fraction/"
cd "work/$fraction"
python3 write_parameters.py --fraction "$fraction"
bash run.sh
```

在参考包examples目录中运行bash start.sh 5或bash start.sh 25，各自复制输入到work子目录后运行。

脚本把每一阶段的输出作为下一阶段的输入：坐标文件保存当时的位置，检查点还携带速度与需要延续的运行状态，新的MDP文件则定义接下来如何推进。生产时间重新从零计起，表示图中0 ns之前已经完成准备阶段。读到图中的20 ns时，应该把它理解为记录段的长度。保存间隔与积分步长也相差很大：积分每20 fs更新一次，而图片分析每100 ps读取一帧，前者决定数值推进，后者决定能够回看哪些运动细节。

观察生产段的起点，可以预先知道后面应留意什么：低比例体系的PEG质量平均高度约0.96 nm，末端平均高度约1.50 nm；高比例对应约3.58 nm与6.20 nm。两组起点相差明显，高比例中不少链仍很伸展。后面的轨迹将显示低比例链逐渐向外展开，而高比例链部分回缩。把这两条演化放在一起读，比只比较最后两个数更能说明初始构象的作用，也为后续采用多种起始摆法和独立重复提供直接依据。

## 接枝比例相同，表面拥挤程度也可能不同

配方中的5%或25%表示脂质锚定分子中有多少比例携带PEG。真正描述表面上链有多密的量，则是一个叶片中的接枝链数除以该叶片占据的膜投影面积。两片叶片面向相反的水层，因此算上侧的链密度时，用上侧的链数和膜横向面积；把两侧链数全部除以一次面积，会使结果多出一倍。压力耦合又会让面积随时间变化，所以同一组固定链数也有随时间变化的接枝密度。

组成比例与每叶片接枝密度式 2

![组成比例与每叶片接枝密度](https://ml-biomat.com/static/agent-math/1b44044187c226f60392eb3c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| f | 携带PEG的脂质分子比例 | 1 |
| NPEL, NPOPC | 所计表面或整个体系中的两类分子数，范围一致 | 1 |
| N g | 一个叶片中的接枝链数，5或25 | 1 |
| t | 观察时刻 | ns |
| Lₓ, Lᵧ | 正交膜盒的两个横向边长 | nm |
| A | 一片叶片的横向投影面积 | nm² |
| Γ | 每叶片每面积的接枝链数 | nm⁻² |
| =, +, /, ( ) | 相等、相加、相除；括号标明时刻；相邻边长相乘 | 1 |

怎样理解比例计数没有长度信息；每面积链数把配方与实际膜几何连接起来。

算一个例子每叶片5条链、100个脂质时f=0.05。面积65 nm²时，Γ=5/65=0.076923 nm⁻²。

使用条件平面正交盒中的投影密度；两叶片分别计数。报告均值时先逐帧计算Γ。

在后10 ns，低比例膜的平均投影面积约65.358 nm²，每叶片有5条链，逐帧计算后得到平均接枝密度0.07651 nm⁻²；高比例膜面积约68.738 nm²，每叶片25条链，平均密度0.36374 nm⁻²。高比例的链数增加5倍，实际密度增加约4.75倍，因为膜面积也不同。对逐帧密度求平均，与把链数除以平均面积在数学上略有差别；这里报告前一种定义，使每个时刻的几何条件都参与同样的计算。

### 膜面积与接枝密度

两体系逐帧投影面积与每叶片接枝密度；淡色背景标后10 ns。

Martini 3脂质v1与Polyply PEG50模型；每片膜200个脂质，PEL比例5%或25%，每叶片分别5或25条PEG链。300 K、1 bar，各采样20 ns；保留不同水盒、Na⁺数量及构建起点。Q5–SN3r采用原教程规定的ε=3.0 kJ/mol。

[下载参考数据与完整输入（ZIP） 21.26 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-pegmembrane-comparison-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s6)

两体系各201帧的膜投影面积与每叶片接枝密度，淡色背景标出后10 ns的101帧；面密度用每叶片实际接枝数除以该帧膜面积。

面积倒数还能给出一个容易理解的长度尺度：先求每条链平均可分到的面积，再取平方根，得到特征间距。按上述密度估算，低比例约3.62 nm，高比例约1.66 nm。这个长度类似把不规则分布的接枝点均匀分到方格后得到的格距，实际最近邻距离还取决于位置分布和脂质的横向运动。它的用途是把“每平方纳米多少条链”转成可与链尺寸比较的尺度，让密度从抽象的数字变成空间上的问题。

从表面密度估算间距与重叠尺度式 3

![从表面密度估算间距与重叠尺度](https://ml-biomat.com/static/agent-math/fa011b4207454444bd4093ca.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| d | 平均每链面积的平方根，特征间距 | nm |
| Γ | 每叶片接枝密度 | nm⁻² |
| R₀ | 独立给定的参考线团足迹半径 | nm |
| π | 圆周率，约3.14159 | 1 |
| R₀², πR₀² | 半径平方；圆形参考足迹面积 | nm² |
| χ | 圆形参考足迹面积与每链面积之比 | 1 |
| −1/2, ², = | 负二分之一次幂表示倒数开方；平方与相等；相邻量相乘 | 1 |

怎样理解每链面积是1/Γ，取平方根得到长度；乘以参考足迹面积得到无量纲重叠指标。

算一个例子Γ=0.25 nm⁻²、R₀=1 nm时，d=2 nm，χ=π/4≈0.7854。

使用条件均匀分配面积与圆形足迹的几何估计；实际最近邻距离和构象转变需分子轨迹。

[Figure: 参考圆形足迹与每链面积](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s6)

均匀接枝位置与圆形线团足迹的几何算例；显示相邻九个面积单元，输入链数用于计算整个叶片的密度。

交互图用一个指定的参考线团半径，在平面上画出相应的圆形足迹，再与接枝点平均分配的面积比较。圆形足迹面积与每链面积之比越大，说明参考线团之间越容易发生空间重叠。参考半径是这个几何算例的输入，应由单独的稀溶液或稀接枝测量来确定；后面测得的密接枝链回转半径已经受到环境影响，不能不加区分地拿来定义自由线团。圆相互重叠表示几何尺度的交叠，分子仍然是有回折、有水穿入的柔性链。

密度的解释也要回到膜的可移动性。在固体表面，接枝位点可能固定在材料结构中；在这里，携带PEG的脂质可以在叶片内移动，邻居关系会随时间改变。高比例体系除了平均密度较高，还可能有局部密度涨落，PEG与头部之间的相互作用又会影响这些局部安排。若研究重点变成聚集或均匀覆盖，可以继续对接枝点做二维距离与空间分布分析，并同时观察膜面积，这样就能把平均拥挤程度与局部组织区分开来。

## 一条链有不止一种高度

测量链向外伸出多远，首先要为每条链选一个随它一起移动的零点。本节用该PEL的NH3连接珠作为零点，取膜法向的坐标差；上叶片向上为正，下叶片向下为正。这样两侧伸向水的链都具有正的向外高度，膜整体平移也不会改变结果。坐标求差前，程序沿拓扑中的每条键恢复完整分子，并检查所有键长，避免跨周期边界的同一条链被读成两个相距一个盒高的片段。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s7)

图 2 · 两叶片分别取朝向水的方向为正，每条链都相对自身NH3连接珠测量。示意链形与膜厚用于解释坐标定义。

相对连接珠的向外高度式 4

![相对连接珠的向外高度](https://ml-biomat.com/static/agent-math/8538bee70d1ed2fd988fd96c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| c, i, 0, 51 | 链序号、PEG珠子序号；0为NH3连接珠，51为OH末端 | 1 |
| s c | 上叶片+1，下叶片−1，令向水侧为正 | 1 |
| zci, zc0 | 完整分子表示中PEG珠子和连接珠的法向坐标 | nm |
| hci, Hc, Hc,end | 单珠高度、链质量平均高度、末端高度 | nm |
| mi, M | 珠子质量；51个PEG珠子的总质量2286 | u |
| mi hci | 质量与高度的乘积 | u nm |
| Σ, =, −, /, ( ) | 对51个PEG珠子求和、相等、相减、相除、括号；相邻量相乘 | 1 |

怎样理解减去各自连接点消除整体平移，叶片符号统一外侧方向，质量权重描述聚合物质量的位置。

算一个例子下叶片连接珠z=10 nm、末端z=7 nm，s=−1，末端向外高度为3 nm。

使用条件先按键图恢复完整PEL；仅51个PEG珠子进入质量平均，连接珠用作零点。

把51个PEG珠子的高度按质量加权，得到一条链的质量平均高度；只取末端OH珠子的高度，得到末端高度；再围绕PEG自己的三维质量中心计算回转半径，得到链整体铺开的尺度。这三种测量回答不同问题。若链沿膜面摊开，回转半径可以较大，质量平均高度却较小；若只有末端的一小段伸得很高，末端高度的变化会比整条链的质量平均高度更明显。一个单独的“链高”名称不足以说明测量过程，必须把选入珠子、参考点和平均方式写清楚。

PEG自身的三维回转半径式 5

![PEG自身的三维回转半径](https://ml-biomat.com/static/agent-math/ef2f5f340c0fad7378b4f475.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| c, i, 51 | 链编号、PEG珠子编号、所选珠子总数 | 1 |
| rci, rc,cm | PEG珠子位置向量与PEG质量中心 | nm |
| mi, M | 当前珠子质量与所选PEG总质量 | u |
| Rg,c | 此链PEG部分的回转半径 | nm |
| ‖rci−rc,cm‖² | 到质量中心的距离平方 | nm² |
| mi‖rci−rc,cm‖² | 质量乘距离平方 | u nm² |
| Σ, √, =, −, /, 1 | 求和、平方根、相等、向量相减、相除、常数1；相邻量相乘 | 1 |

怎样理解质量中心随整条PEG移动，距离平方平均描述所有方向上的展开程度。

算一个例子几何算例中两个等质量点相距2 nm，中心在中间，每点距中心1 nm，因此Rg=1 nm。

使用条件本例仅PEG的51珠，使用原生质量与完整分子坐标；逐链先开方，再平均Rg。

### 三种链尺寸的真实演化

每帧先逐链测量，再对该体系全部链平均。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s7)

以各链NH3接枝点为高度零点，分别观察质量平均高度、末端高度与PEG回转半径；方向按各自叶片的外法线统一。

在后10 ns，低比例体系的PEG质量平均高度为1.717 nm，高比例为3.031 nm；末端平均高度分别为2.356 nm与4.630 nm；PEG回转半径分别为1.782 nm与2.082 nm。高比例链的质量和末端都分布在更远的外侧，而回转半径的增加幅度较小。这很合理：把一团链重新沿法向分配，并不要求它的全部三维尺寸按同样比例增大。曲线还显示高比例链在记录早期明显回缩，后段仍有变化，比较时应保留这段20 ns观察范围。

平均值旁边还藏着另一层结构：同一时刻，不同链的末端高度差别很大。对每帧的所有链计算末端高度总体标准差，再在后10 ns平均，低比例为约1.739 nm，高比例为约2.156 nm。这里的标准差描述一帧内链与链的分散程度，使用全部链数量作为分母；时间曲线本身的波动则是逐帧链均值的变化，分析表对这些帧值采用样本标准差。高比例体系有更多链参与平均，平均曲线较平稳，同时仍保留很宽的单链分布，这两件事可以同时发生。

### 每条链的末端高度

链号从零开始，使用同一颜色尺度显示两体系全部201帧。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s7)

全部20 ns内每条链的末端向外高度，两个体系采用共同色标；纵轴为实际链编号。同一体系中的链和保存帧共享环境，两种条件则保留各自起始构象、盒高与溶剂组成。

热图把每条链沿时间的末端高度放在单独一行，行号是从零开始的固定链序号。连续的亮带表示某条链在一段时间内保持较高末端，暗带表示它更多停留在接枝点附近；两种颜色之间的过渡显示回折与展开。横向逐行阅读可以看到单链记忆，纵向阅读可以比较同一时刻的链间差异。出现少量负高度时，含义是末端位于它自己的连接珠内侧；是否真正穿过膜，需要结合完整膜几何和整条链的位置另行判断。

## 把分布、完整代码和研究问题连起来

为了看清聚合物覆盖层占据哪些高度，可以把法向分成等宽的小格，统计每个格子中的PEG质量。每条链先除以自身的总质量，所有链再按相同权重平均，最后除以高度格宽。得到的曲线纵轴单位为nm⁻¹，曲线下面积为1，因此两组不同链数的结果可以直接比较形状。若把它乘以实际接枝密度和每链质量，就能进一步构造单位面积上的质量分布；本节先使用归一化概率密度，专门观察每条链的质量如何沿法向分配。

按每条链归一化的高度概率密度式 6

![按每条链归一化的高度概率密度](https://ml-biomat.com/static/agent-math/e3165ee4f76890f8f053f0fb.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| p k | 第k个高度格的质量加权概率密度 | nm⁻¹ |
| k, f, c, i | 高度格、帧、链、PEG珠子索引 | 1 |
| F, Nc, 51 | 帧数101、链数10或50、每链PEG珠子数 | 1 |
| Δh, hfci | 格宽0.25与该珠子向外高度 | nm |
| mi/M | 该珠子占其PEG链总质量的比例 | 1 |
| Bk | 第k格的高度区间 | 区间单位nm |
| 𝕀 | 条件成立取1，否则取0 | 1 |
| Σ, =, /, Δ, ∈, 1 | 求和、相等、相除、区间宽度记号、属于区间、常数1；相邻量相乘 | 1 |

怎样理解每条链质量权重总和为1，再平均所有链与帧并除以格宽，得到可跨链数比较的分布。

算一个例子若宽0.25 nm的一格包含总归一化权重0.10，该格密度为0.10/0.25=0.40 nm⁻¹。

使用条件后10 ns的101帧，格子覆盖全部选定样本；末端分布对每链末端等权计数。

### 质量与末端高度分布

后10 ns的101帧，质量分布每链归一化；末端分布每条链等权。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s8)

后10 ns的两种高度分布：上图按每条PEG链的模型质量归一化，统计各珠相对接枝点的高度；下图统计每条链的末端高度。两体系各用共同分格，密度积分均为1。

低比例的质量分布较集中在靠近接枝点的区域，高比例在更远的高度仍有明显权重，反映向水侧展开的覆盖层。末端高度分布则更宽，因为一个末端的位置可以随局部回折快速改变，它也不代表整条链的质量都移到了那里。图中两种分布均按后10 ns的101帧统计，高度格包含该窗口中的全部样本。概率密度较高表示落入单位高度范围的权重较多，曲线的峰值本身可以因格宽改变，因此比较时两组使用统一的格子和归一化方式。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/#zh-s8)

图 3 · 三个珠子的质量归一化算例：45、45、36 u各进入一个1 nm高度格。实际PEG含51珠，分析还平均全部链与帧。

下面的完整分析程序读取拓扑中的质量、分子边界和键图，逐帧还原每个PEL，核对两叶片的链数、分子电荷与最大键长，再计算所有指标。它把链级记录、逐帧平均值和汇总表分别输出，便于从一幅总体曲线追查到具体链。内部坐标由MDAnalysis按Å读取，输出时显式换算为nm；时间由ps换算为ns。链号、统计窗口和单位都与图中标注一致，修改选取范围时也能沿着相同程序重新生成结果。

### 完整的双体系链级分析

```
"""Measure PEG50 chains on two recorded lipid membranes.

python analyze_brush.py --low records/5 --high records/25 --out analysis --language en
Each record directory contains md.tpr and md.xtc. Dependencies: MDAnalysis,
NumPy, Matplotlib. Lengths read by MDAnalysis are in angstrom.
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


def connection_plan(group):
    local = {int(v): i for i, v in enumerate(group.indices)}
    edges = np.array([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, k, sign))
    if len(seen) != len(group):
        raise ValueError("A PEL molecule must have one connected bond graph")
    return edges, plan


def reconstruct(raw, box, edges, plan):
    delta = minimize_vectors(raw[edges[:, 1]]-raw[edges[:, 0]], box)
    whole = np.empty_like(raw, dtype=float); whole[0] = raw[0]
    for a, b, k, sign in plan:
        whole[b] = whole[a]+sign*delta[k]
    observed = whole[edges[:, 1]]-whole[edges[:, 0]]
    if np.max(np.linalg.norm(observed-delta, axis=1)) > .005:
        raise ValueError("A reconstructed bond cycle does not close")
    longest = float(np.linalg.norm(observed, axis=1).max()/10)
    if longest > .7:
        raise ValueError("A coarse-grained PEL bond exceeds 0.7 nm")
    return whole/10, longest


def stats(a):
    return {"mean": float(np.mean(a)), "sd": float(np.std(a, ddof=1)),
            "minimum": float(np.min(a)), "maximum": float(np.max(a))}


def save(fig, path):
    fig.savefig(path.with_suffix(".svg")); fig.savefig(path.with_suffix(".png"), dpi=150)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--low", type=Path, default=Path("records/5"))
    p.add_argument("--high", type=Path, default=Path("records/25"))
    p.add_argument("--out", type=Path, default=Path("analysis"))
    p.add_argument("--language", choices=["zh", "en"], default="en")
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    present = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [f for f in fonts if f in present],
                         "font.size": 14, "axes.labelsize": 15,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    summaries = []; all_arrays = []; all_chains = []; all_heights = []; snapshots = []
    for fraction, folder, count, waters, atoms in [(5, args.low, 10, 7655, 10575),
                                                 (25, args.high, 50, 11198, 16198)]:
        u = mda.Universe(str(folder/"md.tpr"), str(folder/"md.xtc"))
        pel = u.select_atoms("moltype PEL")
        chains = [pel[pel.molnums == number] for number in np.unique(pel.molnums)]
        if len(chains) != count or len(u.atoms) != atoms or len(u.select_atoms("moltype W")) != waters:
            raise ValueError("Composition differs from the selected recorded model")
        if len(u.select_atoms("moltype NA")) != count or abs(sum(u.atoms.charges)) > 1e-5:
            raise ValueError("Counterion count or total charge differs from the model")
        for chain in chains:
            if len(chain) != 63 or list(chain.names[:2]) != ["NH3", "PO4"]:
                raise ValueError("Expected a 63-bead PEL with NH3 and PO4 first")
            if list(chain.resnames[12:]) != ["EO"]*50+["OHter"]:
                raise ValueError("Expected 50 EO beads followed by one OHter bead")
            if abs(sum(chain.charges)+1) > 1e-5 or not np.allclose(chain.masses[12:], [45]*50+[36]):
                raise ValueError("PEL charge or PEG bead masses differ from the model")
        plans = [connection_plan(c) for c in chains]
        records = []; individual = []; height_frames = []; initial_sides = None
        changes = 0; max_bond = 0.; final_shapes = []
        for frame in u.trajectory:
            if not np.allclose(frame.dimensions[3:], 90):
                raise ValueError("The recorded box must be orthorhombic")
            area = float(frame.dimensions[0])*float(frame.dimensions[1])/100
            rows = []; heights = []; sides = []; shapes = []
            for index, (chain, (edges, plan)) in enumerate(zip(chains, plans)):
                xyz, longest = reconstruct(chain.positions.astype(float), frame.dimensions, edges, plan)
                max_bond = max(max_bond, longest)
                side = 1 if xyz[1, 2] > xyz[[7, 11], 2].mean() else -1
                sides.append(side)
                anchor = xyz[0]; peg = xyz[12:]; mass = chain.masses[12:]
                height = side*(peg[:, 2]-anchor[2]); center = np.average(peg, axis=0, weights=mass)
                mean_height = float(np.average(height, weights=mass))
                rg = float(np.sqrt(np.average(np.sum((peg-center)**2, axis=1), weights=mass)))
                rows.append([float(height[-1]), mean_height, rg]); heights.append(height)
                individual.append([float(frame.time), index, side, float(height[-1]), mean_height, rg])
                shapes.append((xyz-anchor)*[1, 1, side])
            if initial_sides is None:
                initial_sides = np.asarray(sides)
                if [sum(initial_sides > 0), sum(initial_sides < 0)] != [count//2, count//2]:
                    raise ValueError("Unexpected graft count per leaflet")
            changes += int(np.sum(np.asarray(sides) != initial_sides))
            rows = np.asarray(rows)
            records.append([float(frame.time), area, (count//2)/area, *rows.mean(axis=0),
                            float(np.std(rows[:, 0], ddof=0))])
            height_frames.append(heights); final_shapes = shapes
        values = np.asarray(records); individuals = np.asarray(individual)
        heights = np.asarray(height_frames)
        if len(values) != 201 or not np.allclose(values[:, 0], np.arange(201)*100):
            raise ValueError("Expected 201 frames from 0 to 20000 ps")
        late = values[:, 0] >= 10000
        labels = ["area_nm2", "graft_density_per_leaflet_nm-2", "tip_height_nm",
                  "mass_mean_height_nm", "PEG_Rg_nm", "within_frame_tip_sd_nm"]
        summary = {"PEL_fraction_percent": fraction, "grafts_per_leaflet": count//2,
                   "total_beads": atoms, "water_beads": waters, "NA": count,
                   "frames": 201, "late_frames": int(late.sum()), "PEG_beads_per_chain": 51,
                   "PEG_model_mass_u": float(sum(chains[0].masses[12:])),
                   "maximum_bond_nm": max_bond, "leaflet_membership_changes": changes,
                   "initial": dict(zip(labels, values[0, 1:].tolist())),
                   "last10ns": {name: stats(values[late, i+1]) for i, name in enumerate(labels)}}
        summaries.append(summary); all_arrays.append(values); all_chains.append(individuals)
        all_heights.append(heights[late])
        with (args.out/f"fraction-{fraction}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(["time_ps", *labels]); writer.writerows(values)
        with (args.out/f"chains-{fraction}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(["time_ps", "chain_index", "leaflet_side", "tip_height_nm", "mass_mean_height_nm", "PEG_Rg_nm"]); writer.writerows(individuals)
        last = individuals[individuals[:, 0] == 20000]
        selected = np.argsort(last[:, 3])[[0, len(last)//2, -1]]
        for index in selected:
            snapshots.append({"fraction_percent": fraction, "chain_index": int(index),
                              "selection": "minimum, median-index, or maximum terminal height at 20 ns",
                              "tip_height_nm": last[index, 3], "mass_mean_height_nm": last[index, 4],
                              "coordinates_relative_to_graft_nm": final_shapes[index].tolist(),
                              "names": chains[index].names.tolist(), "bonds": plans[index][0].tolist()})
    # Normalize each chain by its model mass, then average chains and frames.
    pooled = np.concatenate([v.ravel() for v in all_heights])
    bins = np.arange(np.floor(pooled.min()/.25)*.25-.25, np.ceil(pooled.max()/.25)*.25+.5, .25)
    mass = np.array([45]*50+[36], dtype=float); mass /= mass.sum()
    densities = []
    for heights in all_heights:
        weights = np.broadcast_to(mass, heights.shape).ravel()/np.prod(heights.shape[:2])
        density, _ = np.histogram(heights.ravel(), bins=bins, weights=weights)
        density /= np.diff(bins)
        if not np.isclose(np.sum(density*np.diff(bins)), 1, atol=1e-12):
            raise ValueError("Height probability density must integrate to one")
        densities.append(density)
    summary = {"window_ps": [10000, 20000], "models": summaries,
               "height_reference": "Signed outward displacement from the NH3-named attachment bead",
               "height_distribution": "PEG bead model-mass probability density; normalized per chain, then averaged across chains and saved frames",
               "time_sd": "Sample SD of frame means, ddof=1; chains within a frame are not independent replicates",
               "height_probability_integrals": [float(np.sum(v*np.diff(bins))) for v in densities]}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    np.savetxt(args.out/"height-probability.csv", np.column_stack(((bins[:-1]+bins[1:])/2, *densities)),
               delimiter=",", header="height_nm,fraction5_per_nm,fraction25_per_nm", comments="")
    colors = ["#147d92", "#c66b43"]; labels = ["5% PEL", "25% PEL"]
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for values, color, label in zip(all_arrays, colors, labels):
        axs[0].plot(values[:, 0]/1000, values[:, 1], c=color, label=label)
        axs[1].plot(values[:, 0]/1000, values[:, 2], c=color, label=label)
    axs[0].set_ylabel("膜面投影面积 / nm²" if zh else "Projected area / nm²")
    axs[1].set_ylabel("每叶片接枝密度 / nm⁻²" if zh else "Graft density per leaflet\n/ nm⁻²")
    axs[1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axs[0].legend(ncol=2); axs[0].set_title("接枝数与实际面积共同决定面密度" if zh else "Graft count and actual area jointly define surface density")
    for ax in axs: ax.axvspan(10, 20, color="#e8d5ac", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"graft-geometry")
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    names = ["PEG质量平均高度 / nm", "末端平均高度 / nm", "PEG平均回转半径 / nm"] if zh else ["Mean PEG mass height\n/ nm", "Mean terminal height\n/ nm", "Mean PEG radius of gyration\n/ nm"]
    for values, color, label in zip(all_arrays, colors, labels):
        for ax, column in zip(axs, [4, 3, 5]):ax.plot(values[:, 0]/1000, values[:, column], c=color, label=label)
    for ax, name in zip(axs, names):ax.set_ylabel(name);ax.axvspan(10, 20, color="#e8d5ac", alpha=.2);ax.grid(alpha=.15)
    axs[0].legend(ncol=2);axs[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axs[0].set_title("高度、末端与整体尺寸的不同变化" if zh else "Height, terminal position, and overall size evolve differently")
    save(fig, args.out/"brush-height")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    centers = (bins[:-1]+bins[1:])/2
    tips = [v[v[:, 0] >= 10000, 3] for v in all_chains]
    tip_bins = np.linspace(min(v.min() for v in tips)-.1, max(v.max() for v in tips)+.1, 35)
    for density, tip, color, label in zip(densities, tips, colors, labels):
        axs[0].plot(centers, density, color=color, lw=2.2, label=label)
        axs[1].hist(tip, bins=tip_bins, density=True, histtype="step", color=color, lw=2.2, label=label)
    axs[0].set(xlabel="距接枝点向外高度 / nm" if zh else "Outward height from the attachment bead / nm",
               ylabel="质量加权概率密度 / nm⁻¹" if zh else "Mass-weighted probability\ndensity / nm⁻¹")
    axs[1].set(xlabel="末端高度 / nm" if zh else "Terminal height / nm",
               ylabel="概率密度 / nm⁻¹" if zh else "Probability density / nm⁻¹")
    axs[0].legend(ncol=2); axs[0].set_title("后10ns：逐链归一化后的高度分布" if zh else "Final 10 ns: height distributions normalized per chain")
    for ax in axs:ax.axvline(0, c="#999999", lw=1);ax.grid(alpha=.15)
    save(fig, args.out/"brush-distribution")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    vmin = min(v[:, 3].min() for v in all_chains); vmax = max(v[:, 3].max() for v in all_chains)
    for ax, chain_values, label in zip(axs, all_chains, labels):
        n = len(np.unique(chain_values[:, 1]));matrix = chain_values[:, 3].reshape(201, n).T
        im = ax.imshow(matrix, origin="lower", aspect="auto", extent=[0, 20, -.5, n-.5],
                       vmin=vmin, vmax=vmax, cmap="viridis", interpolation="nearest")
        ax.set_title(label);ax.set_ylabel("链编号" if zh else "Chain index");ax.set_xlabel("时间 / ns" if zh else "Time / ns")
    fig.colorbar(im, ax=axs, label="末端向外高度 / nm" if zh else "Outward terminal height / nm", shrink=.85)
    save(fig, args.out/"brush-chains")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

读取两组TPR/XTC，用显式键图遍历、质量权重和统一统计窗口生成结果。

### 从参考记录生成双语图和数据表

```
#!/usr/bin/env bash
set -euo pipefail
python analyze_brush.py --low records/5 --high records/25 --out results-zh --language zh
python analyze_brush.py --low records/5 --high records/25 --out results-en --language en
```

每组records目录包含md.tpr与md.xtc；输出目录分别保存中英文图。

运行分析时，两组目录各自提供md.tpr和md.xtc即可；前者让程序知道珠子属于哪条分子、质量是多少、哪些珠子有键相连，后者提供逐帧位置与盒子。输出目录中的CSV保留未经文字取舍的逐帧数值，汇总JSON保存窗口和平均定义，图像则适合并排观察。要比较一个新的接枝比例，先检查分子组成和链长度，再调整脚本中对应的组成断言与输入目录。这样修改的是明确的比较对象，几何计算和统计定义仍有可追踪的连续性。

要继续研究接枝密度的影响，一个有用的下一步是在每个比例下准备数个独立构型，其中既有较紧凑也有较伸展的链，再比较各重复的高度分布是否逐渐接近。若目标是蛋白靠近表面的过程，则需要加入具有合适参数的蛋白，明确其初始位置、取向和接近坐标，同时记录水与聚合物的重排。若目标是弯曲载体，还要将平面膜扩展为曲率明确的几何结构。每一次扩展都对应一个新的物理对象和测量量，而已有的接枝密度与高度定义可以继续沿用。

读完这一节，面对“表面接了更多PEG”这样的描述，就可以进一步问出三个具体问题：每片表面实际有多少条链、每条链的质量主要分布在哪里、不同链和不同时间之间差别有多大。本例给出了两种配方在各自20 ns记录中的答案，也展示了初始构象如何留在演化曲线中。把分子身份、空间参考点和统计平均连起来，才能从一张看上去蓬松的分子图片，走向能够比较、能够复算、也能够继续设计实验的界面结构描述。

## 延伸阅读与开放资料

- [PEGylated Lipid Bilayers](https://polyply.github.io/polyply_1.0/tutorials/pegylated-lipid-bilayers/) · Fabian Grünewald and Polyply contributors · Apache-2.0

  PEG50–POPE连接、5%与25%构建、方向生长及PEG–磷酸基参数规定。

  读取实际分子顺序；统一低比例初始盒高20 nm；固定种子并补充分阶段动力学和完整分析。
- [Polyply: a Python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald and colleagues · CC BY 4.0 (paper); Apache-2.0 (software)

  分子连接、参数片段与坐标生成的原理及历史。

  固定软件源码commit 38d4d5424e1ef35c86e7cb8532fbd86ecf997221。
- [Martini Force Fields](https://github.com/Martini-Force-Field-Initiative/martini-forcefields) · Martini Force Field Initiative · Apache-2.0

  Martini 3 v3.0.0基础与脂质、离子、溶剂v1参数。

  按Polyply规定将Q5–SN3r的ε从4.175改为3.0 kJ/mol，σ保持0.43 nm。
- [INSANE](https://github.com/Tsjerk/Insane) · Tsjerk A. Wassenaar and contributors · GPL-2.0 (software)

  初始POPC/POPE膜的坐标生成。

  使用固定种子、组成与盒尺寸；生成坐标按实际分子顺序接入拓扑。
- [Amphipathic polyethyleneglycols effectively prolong the circulation time of liposomes (1990)](https://doi.org/10.1016/0014-5793%2890%2981016-H) · Alexander L. Klibanov; Kazuo Maruyama; Vladimir P. Torchilin; Leaf Huang · Copyright publisher; historical facts cited

  PEG连接脂质的载体实验背景。

  按研究问题讲述，独立绘制概念图。
- [Coarse-grained model for PEGylated lipids: effect of PEGylation on the size and shape of self-assembled structures (2011)](https://doi.org/10.1021/jp2020148) · Hwankyu Lee; Richard W. Pastor · Author manuscript publicly readable; cited historical facts

  PEG脂质粗粒化与聚集形态的历史。

  讨论尺度与科学问题；本节参数为明确的Martini 3组合。
