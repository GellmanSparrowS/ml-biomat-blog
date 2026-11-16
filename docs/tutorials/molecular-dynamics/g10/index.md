# 蛋白质与小分子怎样相遇

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g10/
Language: zh-CN

从实验结合结构建立蛋白质—配体模型，读懂口袋中的位移、接触与方向。

## 从一个已经结合的口袋，理解分子识别

一块海绵能吸进许多种液体，生物体内的蛋白质却常常需要辨认外形很接近的分子。味觉受体要响应特定化学物质，运输蛋白要抓住可以携带的对象，酶也要让合适的底物靠近参与反应的基团。材料研究会遇到相似的问题：把一种小分子接到生物材料表面，究竟会吸引哪些蛋白质；在药物载体中改变一个羟基的位置，又会怎样改变它周围的相互作用。要把这些问题讲清，既需要知道两个分子能否靠近，也需要看它们靠近以后怎样调整方向、形状和周围的水。

本讲从一个已经结合的蛋白质—小分子结构出发。蛋白质是经过改造的 T4 溶菌酶，小分子是 2-丙基苯酚，结构记录中的名字是 JZ4。我们将把这对分子放进盐水，建立彼此兼容的力场，观察配体在口袋内的位移，并计算哪些蛋白残基经常与它接触。“配体”指与研究对象结合的分子，在这里就是那枚小分子；“口袋”则是蛋白质表面或内部能容纳它的空间。这样的计算适合检查一个结合姿态在所选模型中的局部运动，寻找值得进一步比较的原子与残基。

可以把实验结构想成一张手掌握着物体的照片。照片告诉我们手指和物体的位置，却没有告诉我们手是怎样伸过去的、握住之前尝试过多少姿势，也没有记录松手需要多久。本讲的起点正是这张“已经握住”的照片，随后的一纳秒轨迹记录附近的活动。研究分子从溶液进入口袋的路线，需要覆盖扩散、入口开合和结合事件；研究结合强弱，则需要比较结合态与溶液态的统计权重。这些问题会决定另外的采样设计，不能由一段口袋内运动自动替代。

蛋白质识别的历史中，形状匹配一直是重要线索。早期的钥匙与锁类比突出一种直观事实：分子的大小、形状和化学基团位置会影响它能否接近特定位置。科什兰在 1958 年提出的诱导契合思想进一步强调，配体的接近可以伴随蛋白质构象调整，使有关基团形成合适的空间关系。这里“构象”就是在不改变化学连接的情况下，分子通过转动、弯曲等方式形成的不同形状。科学问题由此从“轮廓是否吻合”扩展到“两个有柔性的对象怎样共同改变”。

[Figure: 识别的历史：从形状到共同调整](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s1)

图 1 · 柔性识别的概念对照。诱导契合把相互作用与构象调整联系起来；本例从已结合姿态观察局部运动。

柔性并不意味着蛋白质每次都要发生巨大的开合。一个侧链转过一点角度，可能足以改变氢原子所指的方向；附近的水进出，也会改变局部相互作用。科什兰后来讨论的一个问题正是：多小的构象变化足以影响功能。阅读模拟时，我们因此既看整条蛋白质的变化，也看口袋中几个原子的相对位置。用整条蛋白质的平均偏移描述一个羟基的方向变化，就像用整只手掌的移动描述指尖是否碰到一个按钮，观察尺度并不相同。

这也解释了为什么本讲选用一个有实验结合结构的小体系。3HTB 中的 L99A 和 M102Q 表示相应位置的氨基酸替换：99 位由亮氨酸变成丙氨酸，102 位由甲硫氨酸变成谷氨酰胺。这些变化为研究口袋空间和局部极性提供了清楚对象。我们沿用结构中解析出的蛋白质与配体身份，重点学习把化学信息变成计算模型，以及如何从轨迹回答局部、可测量的问题。固定连接的经典模型描述原子运动和相互作用；化学反应、质子转移与电子重新分布需要相应的反应模型或量子方法。

## 把结构里的每一种身份认清

打开 3HTB，首先要辨认哪些原子属于蛋白质，哪些属于目标配体，哪些来自结晶环境。这份结构由 X 射线衍射得到，分辨率为 1.81 Å。Å 读作埃，10 Å 等于 1 nm，因此这里对应 0.181 nm 的结构分辨尺度。分辨率描述实验结构信息的空间细节，与每个原子的精确定位误差并不是同一数值。结构文件还给出占据率、替代位置等信息，它们决定我们怎样选择一套可以同时计算的坐标。

蛋白质的登记序列有 164 个残基，实际解析出的连续坐标覆盖 A 链 1—163 位，末端 Leu164 没有坐标。本例保留这段已解析的链，在 Met1 设置带正电的氨基端，在 Asn163 设置带负电的羧基端。这样就得到一个具体的 163 残基模型。末端的电荷位置属于模型定义；若研究问题直接涉及该末端，应建立包含缺失残基的结构并检验补建构象。本例关注内部口袋，同时把末端处理明确保留在模型说明中。

十个残基具有 A、B 等替代位置。对同一残基，我们选择平均占据率较高的一组，平局时选择 A；这份结构中十处最终均选 A。这里必须以残基为单位保持选择一致。若在一个侧链上把某个原子选成 A、另一个原子选成 B，可能拼出实验中并未作为一组给出的几何形状。选定后，蛋白质保留 1300 个重原子。“重原子”在这类分析中指氢以外的原子，这个称呼方便把实验通常较清楚的碳、氮、氧等与后来补入的氢区分开。

JZ4 的化学式是 C₉H₁₂O，共有 22 个原子，其中 10 个是重原子。它包含一个六元芳香碳环、一段丙基和一个羟基。单靠坐标中的原子名称，我们还需要补上化学连接与键级：哪些碳相连，哪些连接属于芳香环，氧是否连着氢。本例使用化学组分字典给出的键图，再把实验中的结合坐标配给相同名字的原子。这样，分子的化学身份与它在口袋中的位置来自各自合适的信息，而不是依靠空间上“看起来很近”去猜所有键。

[Figure: 3HTB：已解析的蛋白与结合口袋](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s2)

图 2 · 依据3HTB实际坐标绘制的蛋白概览与局部口袋，保留所选A构象。右图仅显示JZ4及Gln102的相关重原子，投影压缩了第三维。

羟基中的氧名为 OAB，补氢后的羟基氢名为 H12。名字只是索引，真正的化学连接还要在拓扑的键表中确认。蛋白质 102 位的谷氨酰胺则同时有侧链氧 OE1 和氮 NE2；这两个原子虽然属于同一残基，却有不同的化学角色。后面我们将分别记录 OAB 到 OE1、NE2 的距离，并专门检查 OAB—H12 指向 OE1 的几何关系。若把整个残基压成一个点，就会丢失这种方向与原子身份的信息。

蛋白质中 His31 的加氢位置也要固定。组氨酸的环上有两个氮，可以形成不同的中性互变异构体。本例选择 ND1 带氢的 HID 形式，依据之一是该氮与 Asp70 的 OD2 在起始结构中相距约 2.582 Å，有利于考虑这一方向的供氢几何。它是根据局部环境作出的质子化模型选择，轨迹中不会自行变成另一种形式。其余结晶添加物，包括磷酸根、β-巯基乙醇以及 220 个结晶水氧，随环境重建一起移除；随后用明确的水模型和盐浓度重新建立溶液。

下面两段程序把这些选择落实为文件。第一段下载两个公开结构记录并检查内容指纹，第二段按残基选择替代构象、提取蛋白质与结合配体、写出带键级的小分子文件。运行后，`protein.pdb` 保存选定蛋白质，`ligand-heavy.sdf` 同时保存配体坐标与化学连接，`ligand-bound.pdb` 保存结合姿态的重原子位置。结构检查结果还包括相邻残基间的肽键距离，帮助发现断链或不一致的原子选择。

### 下载并核对公开结构

```
"""Download the public 3HTB structure and JZ4 chemical dictionary record."""
from pathlib import Path
from urllib.request import urlopen
import hashlib

destination = Path("source")
destination.mkdir(exist_ok=True)
files = [
    ("3HTB.pdb", "https://files.rcsb.org/download/3HTB.pdb",
     "69c7b4776c588526160c587e14a36289f5f74b265cb0736fcbed47c4335adfa7"),
    ("JZ4.cif", "https://files.rcsb.org/ligands/download/JZ4.cif",
     "adea84e7352ad38e5210cb555e62b100d692323739f709cfb4901fc7d6620e82"),
]
for filename, url, expected in files:
    data = urlopen(url, timeout=60).read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f"Public record has changed: {filename}, SHA256={actual}")
    (destination / filename).write_bytes(data)
    print(filename, len(data), "bytes", actual)
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 选择蛋白构象并建立配体键图

```
from pathlib import Path
import collections,json,shlex,hashlib,math
import argparse
parser=argparse.ArgumentParser(description='Prepare the resolved 3HTB protein and the CCD-defined bound ligand.')
parser.add_argument('--source',type=Path,default=Path('source'))
parser.add_argument('--out',type=Path,default=Path('prepared'))
args=parser.parse_args();src=args.source;out=args.out
out.mkdir(parents=True,exist_ok=True)
lines=(src/'3HTB.pdb').read_text().splitlines();groups=collections.defaultdict(list)
for l in lines:
    if l.startswith('ATOM  ') and l[21]=='A':groups[(int(l[22:26]),l[26],l[17:20])].append(l)
selected=[];alts=[]
for resid,rows in sorted(groups.items()):
    options=sorted(set(l[16] for l in rows if l[16]!=' '))
    if options:
        means={k:sum(float(l[54:60]) for l in rows if l[16]==k)/sum(l[16]==k for l in rows) for k in options}
        chosen=sorted(options,key=lambda k:(-means[k],k))[0]
        alts.append(dict(residue=resid,mean_occupancy=means,chosen=chosen))
    else:chosen=' '
    keep=[l for l in rows if l[16] in (' ',chosen)]
    assert len({l[12:16] for l in keep})==len(keep)
    selected.extend(l[:16]+' '+l[17:] for l in keep)
assert len(groups)==163 and sorted(set(int(l[22:26]) for l in selected))==list(range(1,164))
def xyz(l):return tuple(float(l[i:i+8]) for i in [30,38,46])
def dist(a,b):return math.dist(xyz(a),xyz(b))
peptide=[]
for i in range(1,163):
    a=next(l for l in selected if int(l[22:26])==i and l[12:16].strip()=='C')
    b=next(l for l in selected if int(l[22:26])==i+1 and l[12:16].strip()=='N')
    peptide.append(dist(a,b))
assert max(peptide)<1.6
(out/'protein.pdb').write_text('TITLE     3HTB chain A resolved residues 1-163\n'+'\n'.join(selected)+'\nTER\nEND\n',newline='\n')
lig=[l for l in lines if l.startswith('HETATM') and l[17:20]=='JZ4'];assert len(lig)==10
(out/'ligand-bound.pdb').write_text('TITLE     3HTB JZ4 bound heavy-atom coordinates\n'+'\n'.join(lig)+'\nEND\n',newline='\n')
cif=(src/'JZ4.cif').read_text().splitlines();bonds=[];inside=False
for l in cif:
    if l.startswith('_chem_comp_bond.'):inside=True;continue
    if inside and l.strip()=='#':break
    if inside and l.startswith('JZ4 '):
        x=shlex.split(l);bonds.append((x[1],x[2],x[3]))
names=[l[12:16].strip() for l in lig];heavy=[(a,b,o) for a,b,o in bonds if a in names and b in names]
assert len(heavy)==10
s=['JZ4 bound coordinates','3HTB / RCSB CCD bond orders','',f'{len(lig):3d}{len(heavy):3d}  0  0  0  0            999 V2000']
for l in lig:
    x,y,z=xyz(l);s.append(f'{x:10.4f}{y:10.4f}{z:10.4f} {l[76:78].strip():<3s} 0  0  0  0  0  0  0  0  0  0  0  0')
for a,b,o in heavy:s.append(f'{names.index(a)+1:3d}{names.index(b)+1:3d}{dict(SING=1,DOUB=2,TRIP=3)[o]:3d}  0  0  0  0')
s+=['M  END','$$$$'];(out/'ligand-heavy.sdf').write_text('\n'.join(s)+'\n',newline='\n')
hist=[l for l in selected if l[17:20]=='HIS' and l[12:16].strip() in ['ND1','NE2']]
neighbors=[]
for h in hist:
    neighbors.append(dict(atom=h[12:16].strip(),resid=int(h[22:26]),neighbors=[dict(resname=l[17:20],resid=int(l[22:26]),atom=l[12:16].strip(),distance_A=dist(h,l)) for l in selected if l[22:26]!=h[22:26] and l[76:78].strip() in ['O','N','S'] and dist(h,l)<4]))
audit=dict(pdb='3HTB',pdb_sha256=hashlib.sha256((src/'3HTB.pdb').read_bytes()).hexdigest(),ccd_sha256=hashlib.sha256((src/'JZ4.cif').read_bytes()).hexdigest(),model='T4 lysozyme L99A/M102Q, resolved residues 1-163 + JZ4',missing_terminal='Unresolved Leu164 is omitted; Asn163 is assigned a deprotonated C terminus; Met1 protonated N terminus',protein_atoms=len(selected),protein_residues=163,altlocs=alts,peptide_CN_range_A=[min(peptide),max(peptide)],ligand_names=names,ligand_heavy_bonds=heavy,removed_heterogens=dict(collections.Counter(l[17:20] for l in lines if l.startswith('HETATM') and l[17:20]!='JZ4')),histidine_neighbors=neighbors)
(out/'structure-audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

## 一套相互作用规则怎样容纳蛋白质和配体

上一讲的蛋白质由常见氨基酸组成，力场已经提供相应的残基模板。加入 2-丙基苯酚以后，程序还需要知道这个新分子中每种键、角、扭转和非键相互作用怎样计算。可以把蛋白质模板想成一套标准零件说明书，小分子则需要根据它的化学连接重新选取适合的零件类型。把配体的坐标直接拼到蛋白质坐标后面，只增加了位置，没有增加这些相互作用规则，因此还没有得到一个完整的计算体系。

本例采用 AMBER99SB-ILDN 描述蛋白质，用 GAFF 描述有机小分子，并用 SPC/E 描述水。GAFF 是通用 AMBER 力场，它按元素及局部化学环境区分原子类型，例如芳香碳、脂肪碳和羟基氧。同是碳，环中的碳与饱和丙基中的碳拥有不同的邻接环境，相关参数也会不同。参数化程序读取连接和键级后，给原子分配类型，并组合已有的键长、键角、扭转和非键参数。研究特殊官能团或新的化学环境时，需要进一步检查参数覆盖与构象能量。

部分电荷是另一块必要信息。一个整体中性的分子内部，电子分布仍然可以不均匀，氧附近通常偏负，某些氢附近偏正。固定电荷力场把这种分布近似成附着在原子位置上的点电荷，随原子运动，却不在每个时间步重新求电子密度。AM1-BCC 先利用半经验量子计算得到电荷，再施加按键环境定义的修正。这里保留的是这种方法产生的分数电荷，而小分子的形式总电荷指定为零。两者分别描述整体电荷状态与内部电荷分配。

部分电荷组成分子总电荷式 1

![部分电荷组成分子总电荷](https://ml-biomat.com/static/agent-math/63f4713fea9a8569f03a999e.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Q | 整枚分子的总电荷 | C |
| e | 元电荷大小，1.602176634×10⁻¹⁹ C | C |
| qᵢ | 第 i 个原子以 e 为单位的部分电荷数值 | 1 |
| i, N | 原子编号与原子总数；JZ4 的 N=22 | 1 |
| Σᵢ₌₁ᴺ | 依次加入全部原子的电荷数值 | 1 |
| =, eΣqᵢ | 等号表示相等；e 与求和结果相乘 | 等号无单位；乘积为 C |

怎样理解电荷可相加，部分电荷总和必须与指定的分子电荷状态一致。qᵢ 是用元电荷作尺度的数值，乘 e 后得到库仑。

算一个例子三个示意位点的 q 分别为0.4、−0.2、−0.2，总和为0，故 Q=0 C。JZ4 则需要将全部22项相加；单独把 OAB 与 H12 相加约为−0.081099e，剩余原子补足全分子的零净电荷。

使用条件固定电荷模型中的电荷分配；电子分布不随每帧重新求解。

实际参数中，OAB 的电荷约为 −0.498099e，H12 约为 +0.417000e。两者相加不是零，因为羟基与碳环的电荷分配要放进整枚分子一起求和。把 22 个原子电荷全部相加，才得到中性 JZ4 的总电荷。这里 e 是一个元电荷的大小，负号表示相对于正电荷的方向；它不是说氧已经变成一个独立、带整单位负电的离子。这样的区分也能帮助理解为什么一个中性分子仍会与水、蛋白质中的极性基团发生明显的静电相互作用。

力场兼容性涉及的不只是单位。两套参数需要采用相同的非键组合约定，并正确处理相隔三个化学键的原子对，通常称为 1–4 相互作用。在本例的 AMBER 约定中，这些成对项具有专门的缩放规则；对应参数转换到 GROMACS 后仍须保持同一含义。把一套力场的电荷、另一套力场的范德华参数和第三套力场的缩放系数任意拼起来，会改变模型整体的平衡。选择同一参数家族的蛋白质与小分子描述，给了我们明确的兼容起点，随后仍要核查实际输出的拓扑。

ACPYPE 在这里承担调用 AmberTools 并生成 GROMACS 文件的工作。运行参数中的 `-a gaff` 明确选择 GAFF，`-c bcc` 选择 AM1-BCC，`-n 0` 指定净电荷。GAFF 与 GAFF2 是不同参数版本，文件名相似并不意味着参数可以不加区分地替换。这里固定使用的程序版本为 ACPYPE 2026.10.15，配套 AmberTools 26。若希望改变电荷方法或力场版本，应让新的模型完整经历准备和分析流程，使比较对应清楚的科学改变。

参数化时还有一个容易忽略的坐标问题：为计算电荷或整理小分子而处理的自由配体，未必保持原来的结合位置。本例以实验重原子坐标为基准添加氢，完成参数化后按原子名字恢复这组结合坐标，再让整个复合物一起松弛。新增氢则保留生成的位置，经过共同最小化处理局部接触。这样，初始问题保持为“这个实验结合姿态附近怎样运动”，而不是把一个在别处优化过的配体随意摆回口袋。

## 把化学身份、坐标顺序和拓扑接在一起

准备好建模环境后，可以按下面的顺序生成小分子参数。环境安装的完整步骤在[准备计算环境的分子建模部分](https://ml-biomat.com/tutorials/molecular-dynamics/s00/#zh-modeling)。本节的命令从当前练习目录运行，输出集中在 `prepared` 和 `run` 两个子目录。把公共结构文件与计算输出放在不同目录，有助于保留原始坐标，也能让我们清楚地比较加氢、参数化和重新溶剂化分别改变了什么。

### 从公开结构到分析图

```
# Run from an exercise directory directly inside the course workspace.
course_workspace=$(cd .. && pwd)
export PATH="$course_workspace/runtime/modeling/bin:$PATH"
python fetch_structure.py
python prepare_structure.py --source source --out prepared
bash parameterize_ligand.sh prepared
python export_model.py --prepared prepared --out run
(cd run && bash run_complex.sh)
# Use the separately prepared analysis environment.
"$course_workspace/runtime/analysis/bin/python" analyze_complex.py --records run --out analysis --language en
```

本例目录放在准备页工作目录下一层，并先执行准备页的环境激活命令。建模和分析分别使用runtime/modeling与runtime/analysis。参考数据目录可直接作为--records参数读取。

### 加氢、保持原子身份并生成GAFF参数

```
#!/usr/bin/env bash
set -euo pipefail
cd "${1:-prepared}"
obabel ligand-heavy.sdf -O ligand.mol2 -h > obabel.log 2>&1
python - <<'PY'
from pathlib import Path
import json
from openbabel import openbabel as ob
c=ob.OBConversion();c.SetInFormat('mol2');m=ob.OBMol();c.ReadFile(m,'ligand.mol2')
assert m.NumAtoms()==22 and m.GetFormula()=='C9H12O',(m.NumAtoms(),m.GetFormula())
original=json.loads(Path('structure-audit.json').read_text())['ligand_names']
lines=Path('ligand.mol2').read_text().splitlines();section=''
for i,line in enumerate(lines):
    if line.startswith('@<TRIPOS>'):section=line;continue
    if section=='@<TRIPOS>ATOM' and line.strip():
        v=line.split();idx=int(v[0]);v[1]=original[idx-1] if idx<=10 else 'H'+str(idx-10);v[6]='1';v[7]='JZ4';lines[i]=' '.join(v)
Path('ligand.mol2').write_text('\n'.join(lines)+'\n')
PY
acpype -i ligand.mol2 -b JZ4 -c bcc -n 0 -a gaff -o gmx > acpype.log 2>&1
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

小分子文件中的原子名字在这个过程中有实际作用。结构字典用 OAB 指代羟基氧，轨迹分析也要沿用这个名字找到同一位置；如果格式转换把它改成一个通用的 O1，后续选择就可能指向错误对象。因此程序在加氢后恢复十个重原子的原名，并给新增氢赋予稳定的编号。它还检查化学式和原子数：9 个碳、12 个氢和 1 个氧共同组成 22 个原子。这样的核对比单看屏幕上的分子形状更容易发现缺氢、重复原子或错误电荷状态。

接着要把蛋白质与配体放进同一份 GROMACS 坐标。`pdb2gmx` 为选定蛋白质补氢并建立拓扑，得到 2614 个蛋白质原子；配体占随后 22 个位置。`[ molecules ]` 中的分子排列必须与这份坐标一致，因为程序依照拓扑规定的顺序把参数分配给坐标行。这个关系很像剧场座位表：姓名、票号和座位需要一一对应，人数相同只是第一步，顺序错了仍然会把身份放到错误位置。

[Figure: 坐标顺序与分子身份一一对应](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s4)

图 3 · 同一配体同时具有局部拓扑编号与全体系坐标位置。分子数量、原子总数和排列顺序共同决定参数与坐标的对应。

包含关系同样重要。`forcefield.itp` 先定义整个参数体系的基本约定，小分子的原子类型要在使用这些类型的分子定义之前出现。JZ4 的文件同时包含原子类型和分子拓扑，因此插入到力场入口之后。位置限制文件则属于某个特定分子，里面的编号从该分子的第一个原子开始计数。配体只有 22 个原子，它的限制编号应使用这 22 个局部编号，而不是直接填入整个体系中从 2615 开始的全局坐标行号。

导出程序将配体参数、结合坐标、重原子位置限制和运行输入整理到 `run`。其中 `JZ4.itp` 是完整分子拓扑，`posre_JZ4.itp` 列出准备阶段受限的配体重原子。下面的合并程序还会检查 His31 是否具有 HD1、是否缺少 HE2，以确认实际建立的是选定的 HID 形式。这种核查直接面对生成后的原子身份，能够把前面讨论的化学选择与最终运行对象连接起来。

### 导出小分子参数与结合坐标

```
from pathlib import Path
import argparse,shutil
import numpy as np
parser=argparse.ArgumentParser(description="Export GAFF parameters and retain the bound ligand pose.")
parser.add_argument("--prepared",type=Path,default=Path("prepared"))
parser.add_argument("--out",type=Path,default=Path("run"))
args=parser.parse_args();prep=args.prepared;out=args.out;params=prep/"JZ4.acpype"
out.mkdir(parents=True,exist_ok=True)
shutil.copy2(prep/'protein.pdb',out/'protein.pdb')
itp=(params/'JZ4_GMX.itp').read_text();itp=itp[itp.index('[ atomtypes ]'):]
itp+='\n#ifdef POSRES\n#include "posre_JZ4.itp"\n#endif\n';(out/'JZ4.itp').write_text('; JZ4 GAFF / AM1-BCC; ACPYPE2026.10.15, AmberTools26.\n'+itp,newline='\n')
pos=(params/'posre_JZ4.itp').read_text();(out/'posre_JZ4.itp').write_text(pos[pos.index('[ position_restraints ]'):],newline='\n')
gro=(params/'JZ4_GMX.gro').read_text().splitlines();gro[0]='JZ4 bound conformation with added hydrogen atoms'
bound={l[12:16].strip():np.array([float(l[i:i+8])/10 for i in [30,38,46]]) for l in (prep/'ligand-bound.pdb').read_text().splitlines() if l.startswith('HETATM')}
errors=[]
for j,l in enumerate(gro[2:-1],2):
    name=l[10:15].strip()
    if name in bound:
        pos=np.array([float(l[i:i+8]) for i in [20,28,36]]);errors.append(float(np.linalg.norm(pos-bound[name])))
        gro[j]=l[:20]+''.join(f'{v:8.3f}' for v in bound[name])
assert max(errors)<.001,errors
(out/'JZ4.gro').write_text('\n'.join(gro)+'\n',newline='\n')
template=Path(__file__).resolve().parent
for name in ['ions.mdp','em.mdp','nvt.mdp','npt.mdp','md.mdp','merge_complex.py','run_complex.sh']:
    (out/name).write_text((template/name).read_text(),encoding='utf8',newline='\n')
print('Exported 22-atom ligand; maximum input-coordinate rounding:',max(errors),'nm')
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 合并坐标与拓扑

```
from pathlib import Path
import re,json
protein=Path('processed.gro').read_text().splitlines();ligand=Path('JZ4.gro').read_text().splitlines()
n=int(protein[1]);m=int(ligand[1]);assert m==22
atoms=protein[2:2+n]
for j,line in enumerate(ligand[2:2+m],1):atoms.append(f'{164:5d}'+line[5:15]+f'{n+j:5d}'+line[20:])
Path('complex.gro').write_text('3HTB resolved protein + bound JZ4\n'+str(n+m)+'\n'+'\n'.join(atoms)+'\n'+protein[-1]+'\n')
top=Path('topol.top').read_text();anchor='#include "amber99sb-ildn.ff/forcefield.itp"';assert anchor in top
top=top.replace(anchor,anchor+'\n#include "JZ4.itp"');top+='JZ4 1\n';Path('topol.top').write_text(top)
hist=[line[10:15].strip() for line in protein[2:2+n] if int(line[:5])==31]
assert 'HD1' in hist and 'HE2' not in hist
Path('prepared-model.json').write_text(json.dumps(dict(protein_atoms=n,ligand_atoms=m,protein_residues=163,His31='HID, HD1 present and HE2 absent'),indent=2))
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

原子数也给出一个清楚的总账。最终体系共有 33382 个原子，来自 2614 个蛋白质原子、22 个配体原子、10226 个三点水分子、31 个钠离子和 37 个氯离子。蛋白质净电荷为 +6e，配体为零，因此氯离子比钠离子多六个，既有成对加入的盐，也有抵消蛋白电荷的额外阴离子。这里的水是 SPC/E；虽然同样由三个相互作用位点组成，它与前面蛋白质练习中的 TIP3P 具有不同参数，分析时要连同蛋白质和配体力场一起记录。

## 让口袋和溶液共同调整，再解除位置限制

刚拼好的结构包含实验坐标、模型生成的氢和新放入的水。不同部分的几何来源不同，局部可能存在过近的接触，首先需要最小化。最陡下降方法沿降低势能的方向修改坐标，目标是降低过大的力；它的迭代步没有通常轨迹中的物理时间含义。本例使用柔性水进行这一几何准备，然后在所有分子动力学阶段恢复刚性 SPC/E，并约束含氢化学键。这些约束去掉部分最快振动，使 2 fs 的时间步适合所选积分方案。

准备阶段给蛋白质和配体的重原子加位置限制，水、离子及未被限制的自由度仍可运动。它像在调整物体周围的填充材料时，先用有弹性的支架保留主要形状：支架允许少量偏移，却对较大位移施加回复力。限制系数为 1000 kJ·mol⁻¹·nm⁻²。这里每一个单位都很有意义，因为位移平方带有 nm²，乘上该系数以后才得到能量单位；它既不是一个温度，也不是一个已经作用在原子上的固定力。

一个受限原子的弹性位置能式 2

![一个受限原子的弹性位置能](https://ml-biomat.com/static/agent-math/68225b0a803b586ee4346521.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Upos | 该原子的位置限制势能 | kJ mol⁻¹ |
| kpos | 各方向相同的限制系数，本例1000 | kJ mol⁻¹ nm⁻² |
| α, {x,y,z} | 三个笛卡尔方向的索引与集合 | 1 |
| rα, rα,0 | 当前坐标与限制参考坐标的相应分量 | nm |
| rα−rα,0 | 该方向上的位移 | nm |
| (rα−rα,0)² | 位移分量自乘 | nm² |
| Σ, ½, =, − | 三方向求和、二分之一、等号与减法 | 运算与常数无单位 |

怎样理解小位移的回复力与位移成正比，对位移积分后得到二次能量。三个正交方向的贡献相加，总位移长度的平方等于三个正交分量的平方和。

算一个例子若只有 x 方向偏移0.02 nm，能量为0.5×1000×0.02²=0.20 kJ/mol；同一方向偏移0.04 nm 时能量为0.80 kJ/mol。位移翻倍，二次能量变为四倍。

使用条件本例准备阶段对蛋白质和配体重原子使用该形式；生产阶段关闭位置限制。

100 ps 的 NVT 阶段在固定体积下把体系与 300 K 热环境耦合，随后 200 ps 的 NPT 阶段允许盒子在 1 bar 目标压力下调整体积。温度采用随机速度重标定，整个体系属于同一温控组；压力采用各向同性 C-rescale。准备阶段保留重原子位置限制，且 NPT 使用 `refcoord-scaling = com`。这些设置服务于保形和溶液体积准备。后面的 1 ns 生产阶段移除位置限制，保持相同温度、压力、非键规则和 2 fs 时间步，记录自由运动中的局部相互作用。

下面完整展示各阶段的输入。`ions.mdp` 产生离子替换所需的结构与拓扑描述，并不承担生产采样；其中采用短程静电设置，随后真实动力学输入采用 PME 处理长程静电。`em.mdp` 中的力阈值单位是 kJ·mol⁻¹·nm⁻¹，`emstep` 是以 nm 表示的最小化步长。把这些量与动力学中的 `dt` 区分开，可以避免将“多少次坐标改进”误读成“经过多少时间”。

### 离子替换的预处理输入

```
integrator = steep
nsteps = 0
cutoff-scheme = Verlet
nstlist = 20
coulombtype = Cut-off
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 最小化输入

```
integrator = steep
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
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 100 ps NVT输入

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
gen-seed = 20261000
ld-seed = 20261001
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 200 ps NPT输入

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
ld-seed = 20261002
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

### 1 ns无位置限制生产输入

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
ld-seed = 20261003
```

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

运行脚本依次建立蛋白质参数、合并配体、生成距分子边缘 1.0 nm 的十二面体周期盒、加入水与离子，再执行各阶段计算。每次 `grompp` 都把当前坐标、拓扑和阶段参数组合成新的运行文件；相邻动力学阶段还读取检查点，以传递速度等状态。初始速度在 NVT 阶段生成一次，后续继续运动。生产输入中的 `nsteps = 500000` 与 0.002 ps 时间步相乘，得到 1000 ps，即 1 ns；每 500 步保存一次压缩坐标，因此相邻记录相隔 1 ps。

### 构建盐水体系并执行模拟

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
py=${PYTHON:-python3}
printf '0
' | "$gmx" pdb2gmx -f protein.pdb -o processed.gro -p topol.top -i posre.itp -ff amber99sb-ildn -water spce -his > pdb2gmx.log 2>&1
"$py" merge_complex.py
"$gmx" editconf -f complex.gro -o boxed.gro -c -d 1.0 -bt dodecahedron > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'SOL
' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -conc 0.15 -neutral -seed 20261000 > genion.log 2>&1
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr > npt.grompp.log 2>&1
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

文件名与上文运行顺序对应；所有输入和输出均采用相对路径。

计算结束后，先核对日志中的约束与能量表现，再进入几何分析。这里的 1001 帧包括生产起点和 1000 ps 终点，每帧都会参与本节的平均与接触比例。这个选择与上一讲为分块而使用的右端点不包含窗口不同，两种做法各自对应明确的统计任务。温控和压控定义的是环境条件，分子是否充分访问了相关构象仍要从轨迹和重复设计判断。对于口袋内某个侧链，时间尺度可能明显长于本节记录，后续比较需要针对它增加采样。

## 让每一个“接触”都有明确的测量方法

观察复合物动画时，蛋白质与配体会一起平移、转动，也可能穿过周期边界。若直接用屏幕坐标计算配体位移，就会把整个复合物的漂移混进局部运动。本例先按化学键恢复完整蛋白质和配体，再把配体放到蛋白质附近的相应周期像，最后用蛋白质的 163 个 Cα 对齐最小化末态。Cα 是每个氨基酸主链上的中心碳，沿序列选取它们可以得到覆盖整条蛋白质的一组参照点。所有配体坐标使用同一个蛋白质对齐变换。

在蛋白参照系中测量配体位移式 3

![在蛋白参照系中测量配体位移](https://ml-biomat.com/static/agent-math/2c11fb2bac301c7c62531559.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| RMSDL\|P(t) | 用蛋白质对齐变换计算的配体 RMSD | nm |
| t | 生产阶段时间 | ps |
| NL, i | 配体重原子数与其编号；本例 NL=10 | 1 |
| rᵢ(t), rᵢ,0 | 配体当前与最小化参考位置的行向量 | nm |
| cP(t), cP,0 | 当前与参考蛋白 Cα 的等权几何中心 | nm |
| RP(t) | 使居中蛋白 Cα 最佳重合的正旋转矩阵 | 1 |
| (rᵢ−cP)RP+cP,0−rᵢ,0 | 经蛋白变换后与参考配体位置之差 | nm |
| ‖·‖² | 位移向量长度的平方 | nm² |
| Σ, /NL, √, =, +, − | 逐原子求和、除以原子数、平方根、等号、加法和减法 | 运算本身无单位；平方根将 nm² 变回 nm |

怎样理解先消除蛋白质整体平移与转动，再对配体到固定参考的位移平方取平均。平方保证不同方向的偏移不会相互抵消，最后开平方恢复长度单位。

算一个例子若两个示意配体原子经蛋白对齐后分别离参考0.05和0.10 nm，RMSD=√[(0.05²+0.10²)/2]=0.07906 nm。本例实际使用十个重原子且不再单独对齐配体。

使用条件蛋白质163个 Cα 参与等权刚体拟合；已按键恢复分子并选择邻近周期像；保持同名原子的固定对应。

这里没有再单独对齐配体。这个选择保留了它在口袋中的整体移动和转动，同时也包含自身构象改变。假如把配体再次旋转到最佳重合，计算就会转向它自身形状的变化，口袋内转向的一部分信息会被消去。两个指标都可以有用途，关键是让拟合对象与测量问题一致。本例使用等权重的十个配体重原子，单位为 nm；蛋白质 Cα 的 RMSD 单独计算，帮助辨认整体参照结构改变的幅度。

残基接触采用另一种定义。对某个蛋白残基，先计算它所有重原子到配体所有重原子的距离，再取其中最小值。只要这一个最小距离小于阈值，就记该残基在这一帧接触配体。同一残基即使有多个原子靠近，也只计一次。这个规则回答“口袋中哪些残基靠得近”，不把面积较大的残基简单重复计成许多接触。距离使用周期盒中的最近像，因而一个分子被保存到盒子另一侧不会凭空失去接触。

一个残基到配体的最近距离式 4

![一个残基到配体的最近距离](https://ml-biomat.com/static/agent-math/f1fceff237614bbedd0d3bd3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| da(t) | 残基 a 到配体的最小重原子距离 | nm |
| a, L | 所选蛋白残基与配体的重原子集合 | 1 |
| i, j | 两个原子集合中的索引 | 1 |
| rᵢ(t), rⱼ(t) | 原子的三维位置列向量 | nm |
| H(t) | 三列为周期盒基向量的矩阵 | nm |
| n, ℤ³ | 三个整数组成的周期像索引与其集合 | 1 |
| Hn | 选定周期像的平移向量 | nm |
| min, ∈, ‖·‖, =, +, − | 取最小值、属于、向量长度、等号、加法和减法 | 运算无单位；向量长度为 nm |
| t | 生产时间 | ps |

怎样理解接触由最靠近的一对重原子决定。周期像枚举使跨边界的邻居与盒内邻居遵循同一距离定义。实际程序使用支持三斜盒的最近像距离算法。

算一个例子若某残基的最小候选距离为0.32、0.46、0.58 nm，da=0.32 nm。以0.40 nm为阈值时该残基计一次接触，即使其中不止一个原子靠近配体。

使用条件重原子几何邻近；按残基计数，保留所选距离阈值。

在 1001 帧中把接触指示值相加，再除以帧数，就得到本段记录中的接触比例。例如某残基有 801 帧满足条件，比例约为 0.8002，也就是约 80.0%。它描述按给定几何标准观察到接触的时间份额。相邻帧彼此相关，因此这 1001 次记录并不等于 1001 次独立抽样；若要给比例加统计不确定性，需要使用分块或重复轨迹。我们还同时计算 0.35、0.40、0.45 nm 三种阈值，观察结论对几何边界有多敏感。

接触比例是逐帧指示值的平均式 5

![接触比例是逐帧指示值的平均](https://ml-biomat.com/static/agent-math/acbd78151b8aa8de8af21630.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Ia,m | 残基 a 在第 m 帧的接触指示值，取0或1 | 1 |
| da(tm), rc | 当前最近距离与指定接触阈值 | nm |
| tm | 第 m 帧对应的生产时间 | ps |
| a, m, M | 残基编号、帧编号与帧总数；本例 M=1001 | 1 |
| pa | 该残基在选定记录中的接触比例 | 1 |
| Σ, /M, 0, 1, <, ≥, = | 相加后除以总帧数；二元值、小于、大于等于及等号 | 1 |

怎样理解每帧按同一条件记为0或1，求和就是满足条件的帧数，再除以全部帧数。等间隔记录使它对应所选窗口的时间份额。

算一个例子M=1001，满足条件的帧数为801，则 pa=801/1001=0.80020，约80.0%。这是一段记录中的比例，相关性和独立重复决定其统计不确定性。

使用条件本讲包含0—1000 ps的全部1001帧；阈值分别取0.35、0.40、0.45 nm。

氢键需要进一步认识原子角色和方向。在 OAB—H12···OE1 这组关系中，OAB 是与氢相连的供体重原子，H12 是相应氢，谷氨酰胺的 OE1 是受体氧。本节采用一个明确的几何判据：供体到受体距离小于 0.35 nm，且供体—氢—受体的夹角至少为 150°。角的顶点在氢原子，接近 180° 表示三者接近直线。阈值是一种分析约定，允许我们稳定地逐帧分类；具体氢键强度还取决于化学环境和模型中的相互作用。

在氢原子处定义供体—氢—受体角式 6

![在氢原子处定义供体—氢—受体角](https://ml-biomat.com/static/agent-math/c8818eda8feede41f009c61a.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| θ | D—H—A夹角，顶点在H | 公式反余弦为 rad；输出转换为 ° |
| D, H, A | 供体重原子、其成键氢与受体重原子 | 1 |
| rD, rH, rA | 三个原子的位置 | nm |
| rD−rH, rA−rH | 从氢出发的两条向量，使用邻近周期像 | nm |
| · | 向量点积 | 这里的结果为 nm² |
| ‖rD−rH‖ ‖rA−rH‖ | 两条向量长度相乘 | nm² |
| arccos, /, =, − | 反余弦由余弦值恢复角度；除法、等号和减法 | 比值无量纲；运算本身无单位 |

怎样理解点积等于两向量长度乘积再乘夹角余弦，因此除去长度后得到只由方向决定的余弦。反余弦恢复夹角，并把数值舍入造成的余弦越界裁回−1至1。

算一个例子D=(0,0,0)、H=(0.10,0,0)、A=(0.30,0,0) nm。两向量为(−0.10,0,0)与(0.20,0,0)，点积−0.02 nm²，长度乘积0.02 nm²，故余弦−1、θ=180°，同时D—A距离0.30 nm满足本例距离条件。

使用条件OAB—H12···OE1这一选定供体受体组合；几何分类要求D—A<0.35 nm且θ≥150°。

下面的交互把这件事拆成距离与方向两个可调整因素。保持供体与受体相距较近，转动 O—H 方向，几何判据仍可能从满足变成不满足。它解释了为什么一条 O···O 距离曲线还不够完整，也说明同一残基中的氮不能因为位置近就被自动当作受体。程序中我们通过键表确认 H12 确实与 OAB 相连，再计算角度；这一顺序把化学身份放在几何筛选之前。

固定 O—H 长度0.10 nm，供体D为O、氢为H、受体A为O。距离与方向共同决定所选几何判据。

[Figure: D–H–A geometry](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s6)

一个固定O—H键的解析几何算例。供体与受体的距离不变时，转动供氢方向仍会改变D—H—A夹角。

## 把轨迹中的局部变化画出来

分析程序直接读取运行拓扑、压缩轨迹和最小化末态。拓扑提供质量、键和残基身份，轨迹提供逐帧坐标，最小化末态提供共同的比较参照。MDAnalysis 默认把距离读成 Å，因此程序在输出 nm 前显式除以 10。距离、角度、接触和 RMSD 在同一个逐帧循环里计算，保证不同图中的时间点一致。保存的 CSV 列出每一帧的数值，另一个文件保存全部残基的最小距离，便于更换阈值而保持坐标记录不变。

### 分析配体运动、方向与残基接触

```
"""Measure local protein–ligand motion and contacts from the 3HTB trajectory.

python analyze_complex.py --records records --out analysis --language en
Required files: md.tpr, md.xtc, em.gro. Dependencies: MDAnalysis, numpy,
matplotlib. MDAnalysis uses angstrom internally; all plotted distances are nm.
All 1001 equally spaced frames from 0 to 1000 ps enter the reported averages.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import distance_array, minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


class BondReconstruction:
    """Restore one connected molecule by traversing its explicit topology bonds."""
    def __init__(self, group):
        self.group = group
        local = {int(index): i for i, index in enumerate(group.indices)}
        self.edges = np.array([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
        neighbours = [[] for _ in group]
        for edge, (a, b) in enumerate(self.edges):
            neighbours[a].append((b, edge, 1))
            neighbours[b].append((a, edge, -1))
        visited = {0}
        queue = [0]
        self.plan = []
        for parent in queue:
            for child, edge, sign in neighbours[parent]:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
                    self.plan.append((parent, child, edge, sign))
        if len(visited) != len(group):
            raise ValueError("Selected molecule is not a single connected bond graph")

    def restore(self, box):
        raw = self.group.positions.astype(float)
        a, b = self.edges.T
        vectors = minimize_vectors(raw[b] - raw[a], box)
        whole = np.empty_like(raw)
        whole[0] = raw[0]
        for parent, child, edge, sign in self.plan:
            whole[child] = whole[parent] + sign * vectors[edge]
        errors = np.linalg.norm((whole[b] - whole[a]) - vectors, axis=1)
        if np.max(errors) > 0.005:
            raise ValueError("Bond-cycle reconstruction disagreement exceeds 0.005 angstrom")
        longest_nm = float(np.linalg.norm(whole[b] - whole[a], axis=1).max() / 10)
        if longest_nm > 0.25:
            raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
        self.group.positions = whole
        return longest_nm


def fit_rotation(moving, reference):
    left, _, right = np.linalg.svd(moving.T @ reference)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(left @ right)
    return left @ correction @ right


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == "zh" else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [x for x in candidates if x in available]
                         if args.language == "zh" else ["DejaVu Sans"],
                         "font.size": 13, "axes.titlesize": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#faf8f2", "axes.facecolor": "#faf8f2"})
    universe = mda.Universe(str(args.records / "md.tpr"), str(args.records / "md.xtc"))
    reference = mda.Universe(str(args.records / "md.tpr"), str(args.records / "em.gro"))
    protein = universe.select_atoms("protein")
    ca = protein.select_atoms("name CA")
    heavy = protein.select_atoms("not name H*")
    ligand = universe.select_atoms("resname JZ4")
    ligand_heavy = ligand.select_atoms("not name H*")
    ref_protein = reference.select_atoms("protein")
    ref_ligand = reference.select_atoms("resname JZ4")
    assert len(ca) == 163 and len(ligand_heavy) == 10
    assert len(ligand) == 22 and len(protein) == 2614
    BondReconstruction(ref_protein).restore(reference.dimensions)
    BondReconstruction(ref_ligand).restore(reference.dimensions)
    protein_reconstruction = BondReconstruction(protein)
    ligand_reconstruction = BondReconstruction(ligand)
    ref_ca = ref_protein.select_atoms("name CA").positions.astype(float)
    ref_center = ref_ca.mean(axis=0)
    ref_ca -= ref_center
    ref_ligand_positions = ref_ligand.positions.astype(float)
    offset = ref_ligand_positions.mean(axis=0) - ref_center
    ref_ligand_positions += minimize_vectors(offset[None, :], reference.dimensions)[0] - offset
    ref_ligand_heavy = ref_ligand_positions[~np.char.startswith(ref_ligand.names.astype(str), "H")] - ref_center
    donor = ligand.select_atoms("name OAB")[0]
    hydrogen = ligand.select_atoms("name H12")[0]
    assert hydrogen.index in donor.bonded_atoms.indices
    acceptor = protein.select_atoms("resid 102 and name OE1")[0]
    amide_n = protein.select_atoms("resid 102 and name NE2")[0]
    residue_numbers = protein.residues.resids
    residue_names = protein.residues.resnames
    row_for_resindex = {r.ix: j for j, r in enumerate(protein.residues)}
    atom_to_residue = np.array([row_for_resindex[a.resindex] for a in heavy])
    records, contact_distances = [], []
    maximum_bond_nm = 0.
    for ts in universe.trajectory:
        maximum_bond_nm = max(maximum_bond_nm, protein_reconstruction.restore(ts.dimensions),
                             ligand_reconstruction.restore(ts.dimensions))
        current_ca = ca.positions.astype(float)
        center = current_ca.mean(axis=0)
        current_ca -= center
        rotation = fit_rotation(current_ca, ref_ca)
        ca_rmsd = np.sqrt(np.mean(np.sum((current_ca @ rotation - ref_ca)**2, axis=1))) / 10
        lig_xyz = ligand_heavy.positions.astype(float)
        offset = ligand.positions.mean(axis=0) - center
        lig_xyz += minimize_vectors(offset[None, :], ts.dimensions)[0] - offset
        lig_rmsd = np.sqrt(np.mean(np.sum(((lig_xyz - center) @ rotation - ref_ligand_heavy)**2, axis=1))) / 10
        pair_distances = distance_array(heavy.positions, ligand_heavy.positions, box=ts.dimensions) / 10
        atom_nearest = pair_distances.min(axis=1)
        res_nearest = np.full(len(residue_numbers), np.inf)
        np.minimum.at(res_nearest, atom_to_residue, atom_nearest)
        contact_distances.append(res_nearest)
        target_distances = distance_array(donor.position[None, :],
                                         np.array([acceptor.position, amide_n.position]),
                                         box=ts.dimensions)[0] / 10
        hd = minimize_vectors((donor.position-hydrogen.position)[None, :], ts.dimensions)[0]
        ha = minimize_vectors((acceptor.position-hydrogen.position)[None, :], ts.dimensions)[0]
        cosine = np.dot(hd, ha) / np.linalg.norm(hd) / np.linalg.norm(ha)
        angle = np.degrees(np.arccos(np.clip(cosine, -1, 1)))
        hbond = target_distances[0] < .35 and angle >= 150
        records.append([ts.time, ca_rmsd, lig_rmsd, *target_distances, angle,
                        int(hbond), np.sum(res_nearest < .4)])
    values = np.array(records)
    distances = np.array(contact_distances)
    assert values.shape == (1001, 8) and np.all(np.isfinite(values))
    assert np.allclose(values[:, 0], np.arange(1001))
    fractions = np.array([(distances < cutoff).mean(axis=0) for cutoff in [.35, .4, .45]])
    ranked = np.argsort(-fractions[1], kind="stable")[:14]
    summary = {"frames": len(values), "time_ps": [0, 1000], "right_endpoint_included": True,
               "maximum_reconstructed_covalent_bond_nm": maximum_bond_nm,
               "CA_rmsd_mean_nm": float(values[:, 1].mean()),
               "ligand_protein_aligned_rmsd_mean_nm": float(values[:, 2].mean()),
               "ligand_protein_aligned_rmsd_range_nm": [float(values[:, 2].min()), float(values[:, 2].max())],
               "OAB_OE1_mean_nm": float(values[:, 3].mean()),
               "OAB_NE2_mean_nm": float(values[:, 4].mean()),
               "OAB_H12_OE1_angle_mean_deg": float(values[:, 5].mean()),
               "OAB_OE1_distance_fraction_below_035": float((values[:, 3] < .35).mean()),
               "OAB_H12_OE1_geometry_fraction": float(values[:, 6].mean()),
               "contact_residue_mean_at_040_nm": float(values[:, 7].mean()),
               "top_contact_residues": [{"resid": int(residue_numbers[i]), "resname": str(residue_names[i]),
                                         "fractions_035_040_045": fractions[:, i].tolist()} for i in ranked],
               "geometry_rule": "OAB donor–OE1 acceptor distance <0.35 nm and OAB–H12–OE1 angle >=150 degrees",
               "contact_rule": "A residue contacts if any of its heavy atoms is within the selected cutoff of any ligand heavy atom; nearest periodic images; one count per residue per frame"}
    (args.out / "complex_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(args.out / "complex_observations.csv", values, delimiter=",", header=
               "time_ps,CA_RMSD_nm,ligand_RMSD_nm,OAB_OE1_nm,OAB_NE2_nm,DHA_angle_deg,geometry_contact,residue_contacts", comments="")
    np.savez_compressed(args.out / "residue_contacts.npz", time_ps=values[:, 0],
                        nearest_nm=distances, resids=residue_numbers, resnames=residue_names)
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    t = values[:, 0]
    axes[0, 0].plot(t, values[:, 1], color="#167d84", label=tr("蛋白质 Cα", "Protein Cα"))
    axes[0, 0].plot(t, values[:, 2], color="#bd7045", label=tr("配体重原子", "Ligand heavy atoms"))
    axes[0, 0].set(title=tr("共同蛋白参照系中的运动", "Motion in the common protein frame"), ylabel="RMSD / nm")
    axes[0, 0].legend()
    axes[0, 1].plot(t, values[:, 3], color="#167d84", label="OAB–Gln102 OE1")
    axes[0, 1].plot(t, values[:, 4], color="#4d6fb0", label="OAB–Gln102 NE2")
    axes[0, 1].axhline(.35, color="#6c7271", lw=1, ls="--", label=tr("几何距离阈值", "Geometric distance cutoff"))
    axes[0, 1].set(title=tr("同一残基上的两种原子", "Two atoms in the same residue"), ylabel=tr("距离 / nm", "Distance / nm"))
    axes[0, 1].legend(fontsize=11)
    axes[1, 0].plot(t, values[:, 5], color="#bd7045", lw=.8)
    axes[1, 0].axhline(150, color="#6c7271", ls="--", lw=1)
    axes[1, 0].scatter(t[values[:, 6] == 1], values[values[:, 6] == 1, 5], s=3, color="#167d84",
                       label=tr("距离与角度同时满足", "Both distance and angle pass"))
    axes[1, 0].set(title="OAB–H12–OE1", ylabel=tr("D–H–A 夹角 / °", "D–H–A angle / °"), ylim=(0, 185))
    axes[1, 0].legend(fontsize=11, loc="lower right")
    axes[1, 1].step(t, values[:, 7], where="mid", color="#4d6fb0", lw=.9)
    axes[1, 1].set(title=tr("0.40 nm 内的不同蛋白残基", "Distinct residues within 0.40 nm"),
                   ylabel=tr("接触残基数", "Contacting residue count"))
    for ax in axes.flat:
        ax.set(xlabel=tr("生产时间 / ps", "Production time / ps"), xlim=(0, 1000))
        ax.grid(alpha=.13)
    for suffix in ["svg", "png"]:
        fig.savefig(args.out / f"complex_motion.{suffix}", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [1.4, 1]}, constrained_layout=True)
    labels = [f"{residue_names[i]} {residue_numbers[i]}" for i in ranked]
    axes[0].imshow((distances[:, ranked] < .4).T, origin="upper", interpolation="nearest", aspect="auto",
                   extent=(-.5, 1000.5, len(ranked)-.5, -.5), cmap=matplotlib.colors.ListedColormap(["#ece8dd", "#167d84"]), vmin=0, vmax=1)
    axes[0].set(yticks=np.arange(len(ranked)), yticklabels=labels, xlabel=tr("生产时间 / ps", "Production time / ps"),
                title=tr("逐帧接触：青色为有接触", "Framewise contacts: teal indicates contact"))
    for j, (cutoff, color) in enumerate(zip([.35, .4, .45], ["#bd7045", "#167d84", "#4d6fb0"])):
        axes[1].plot(fractions[j, ranked], np.arange(len(ranked)), "o-", ms=5, lw=.8, color=color, label=f"{cutoff:.2f} nm")
    axes[1].set(yticks=np.arange(len(ranked)), yticklabels=labels, ylim=(len(ranked)-.5, -.5), xlim=(-.03, 1.03),
                xlabel=tr("1001 帧中的接触比例", "Contact fraction among 1001 frames"),
                title=tr("改变距离阈值后的同一批记录", "The same frames at three cutoffs"))
    axes[1].legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=3, fontsize=11)
    axes[1].set_title(tr("改变距离阈值后的同一批记录", "The same frames at three cutoffs"), pad=48)
    axes[1].grid(alpha=.15)
    for suffix in ["svg", "png"]:
        fig.savefig(args.out / f"complex_contacts.{suffix}", dpi=180)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

读取md.tpr、md.xtc、em.gro；核对OAB—H12的实际成键关系；所有1001帧参与平均。脚本同时保存CSV、残基距离数组和两组双语可选图。

第一组图把整体参照与局部观察放在一起。蛋白质 Cα 相对共同最小化末态的平均 RMSD 为 0.08791 nm，蛋白参照系中配体重原子的平均 RMSD 为 0.10900 nm，范围约为 0.02807—0.20775 nm。前者描述整条蛋白质的 Cα 坐标偏离参照的幅度，后者保留配体相对口袋的运动。两个选择包含的原子不同，因此曲线高低要结合各自定义阅读。一个局部基团的转向可能明显改变相互作用几何，却只给整条蛋白的 RMSD 带来很小贡献。

### 蛋白参照系中的配体与局部几何

1001帧、0—1000 ps。蛋白Cα等权对齐共同最小化参考，配体保持该变换；两距离、D—H—A角与残基接触数同步显示。

GROMACS 2026.4；3HTB链A解析残基1–163与中性JZ4；AMBER99SB-ILDN/SPC/E、GAFF与AM1-BCC。体系共33382个原子，包含2614个蛋白质原子、22个配体原子、10226个水、31个Na⁺与37个Cl⁻；300 K、1 bar，无限制生产1000 ps，保存1001帧。

[下载参考数据与完整输入（ZIP） 118.20 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-complex-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s7)

蛋白Cα按等权刚体拟合对齐最小化参考，配体采用同一变换。各面板在相同1001帧上比较Cα与配体重原子RMSD、OAB到Gln102两原子的距离、OAB—H12—OE1夹角和0.40 nm内接触的残基数；分子先按键图恢复完整坐标并检查键长。

OAB 到 Gln102 的 OE1 平均距离为 0.34331 nm，到 NE2 平均距离为 0.51023 nm。把两条曲线并列，可以看见同一残基的不同原子具有不同空间关系。OAB···OE1 在约 68.13% 的帧中小于 0.35 nm；加入至少 150° 的 OAB—H12—OE1 角度要求后，同时满足的比例为约 16.78%。这里的差别来自同一批原子坐标中的方向信息。角度面板标出两项条件同时通过的时刻，使“接近一个残基”“靠近一个特定受体”和“满足指定氢键几何”成为三个能够逐层检查的观察。

在 0.40 nm 阈值下，每帧接触配体的不同蛋白残基平均为 9.3926 个。这里的小数来自对时间求平均：某一帧可以有九个或十个接触残基，许多帧合在一起便会得到非整数均值。接触总数变化时，还要看具体身份。总数相同的两帧可能由不同残基围住配体；一个原有接触消失、另一个新接触形成，计数也可能保持不变。因此第二组图以残基为行、时间为列展示接触记录，并把各残基的时间比例放在旁边。

### 口袋接触的身份、时间与阈值

按0.40 nm接触比例排序的前14个残基。左图逐帧显示接触，右图在同1001帧上比较0.35、0.40、0.45 nm阈值；比例是观察窗口中的时间份额。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g10/#zh-s7)

残基按0.40 nm定义下的接触时间比例排序，保留前14个。时间图记录各帧的接触身份；右图以相同轨迹比较0.35、0.40与0.45 nm三种距离阈值，显示测量定义对观察比例的影响。

热图中连续的有色区域意味着相应残基在这段时间经常满足距离条件，断续的色带则显示接触进出。旁边三个阈值的曲线使用同一批轨迹；阈值放宽以后，接触比例按定义只能增加或保持。若某残基在 0.35 nm 很少接触、在 0.45 nm 却经常接触，说明许多距离位于这一区间，值得回到距离分布和局部结构中查看。若三种阈值下都经常接触，它提供的是对距离边界较稳定的局部邻近信息。

这些图也帮助选择下一步的科学问题。可以挑选一种化学修饰，比较同一个羟基在相同参照系、相同温盐条件下的方向分布；也可以改变口袋中某个残基，观察邻近接触怎样重新分配。开始比较之前，应固定拟合原子、距离定义、阈值和时间窗口，并为各模型设置独立随机重复。这样，新模型与原模型之间的差异才有清楚的测量含义，结果图也能直接连接到具体的化学改变。

## 从局部运动走向结合问题的研究设计

蛋白质与小分子的研究常把三个层次放在一起讨论：结合后的姿态、进入与离开的过程、结合态相对于溶液态的自由能。本讲已经建立了第一个层次的完整工作流：确定结构与化学身份，准备兼容参数，建立溶液，在解除位置限制后测量局部运动。这套流程还能帮助发现准备上的具体问题，例如错误原子名使分析选择为空、质子化状态改变受体或供体身份、配体坐标与拓扑顺序不一致。它为进一步研究提供一个可以复查的物理起点。

要研究结合与解离过程，观察窗口需覆盖事件及其前后的环境变化。配体停在口袋里的一纳秒记录，可以给出这段局部停留的结构；若要估计解离速率，就需要足够的解离事件、明确定义的状态以及相应的动力学采样。一次进入或离开也只是事件的一次实现，重复和状态统计仍然重要。这样的任务选择，决定我们应延长普通模拟、增加多条起始状态，还是采用专门的稀有事件方法。

结合自由能则比较不同状态的统计权重。直观地说，配体进入口袋时，可能获得有利的蛋白相互作用，同时失去一部分与水的相互作用和在溶液中可选择的位置、方向与构象。只计算一帧中蛋白质和配体之间的吸引能，会漏掉这些共同改变。可靠的自由能方案需要定义结合与溶液参考态，处理约束和标准态，并检查相关自由度是否被采样。后面的自由能章节将从反应坐标和偏置采样开始，逐步建立这种状态比较的语言。

在材料研究中，相同思路也能帮助理解表面功能基团与蛋白的接触。若把小分子接到一条聚合物链上，它的可达位置会受到连接点和链构象限制；若把许多相同基团排列在表面，空间密度又会影响蛋白接近和水的排布。这时可以保留本讲的原子身份、接触和方向分析，同时把模型扩展为明确的链或界面。测量对象随着研究问题改变，基本原则仍然相同：先让化学模型对应真实要研究的体系，再让每条曲线对应一个明确的观察。

一次有内容的比较可以从很小的改变开始。例如保持蛋白质模型、温度和盐条件一致，只改变配体上的一个官能团，并分别建立完整参数；先比较配体在口袋中的位置与取向，再看哪些残基接触被保持、替换或重新定向。每个模型安排独立随机重复，用相同时间窗口分析，并检查快变量与慢变量的采样差别。若要连接到实验亲和力，再加入状态间自由能计算或适合的实验量。这样，模型改动、轨迹观察和实验问题之间便形成一条清楚的推理关系。

读完这一讲，再看一个“配体在口袋里动”的动画，画面中的每个元素都会有更具体的含义。蛋白质的整体漂移可以被参照系处理掉，配体的转动可以转化为几何测量，一个颜色变化的接触格子对应指定原子集合与距离条件。我们由此能把直观的相遇和贴合，写成可运行的模型、可重复的分析和有明确用途的下一次计算。

## 延伸阅读与开放资料

- [Protein Ligand Complex MD Setup tutorial using BioExcel Building Blocks](https://github.com/bioexcel/biobb_wf_protein-complex_md_setup) · BioExcel Building Blocks contributors · Apache-2.0

  3HTB/JZ4案例、AMBER99SB-ILDN/SPC/E/GAFF模型及分开参数化、合并、溶剂化、平衡、生产的流程。

  改为明确命令与独立脚本，固定结构选择和HID31，保留结合重原子坐标，更新GROMACS2026.4及采样时长，补局部几何与接触分析。
- [3HTB: 2-propylphenol in complex with T4 lysozyme L99A/M102Q](https://doi.org/10.2210/pdb3HTB/pdb) · S. E. Boyce, D. L. Mobley, G. J. Rocklin, A. P. Graves, K. A. Dill, B. K. Shoichet · CC0-1.0 — PDB archive data

  实验起始坐标及JZ4结合姿态；结构图使用实际选定坐标。

  保留链A解析残基1—163与JZ4，统一选择替代位置A，重建氢、溶剂和离子；末端及His31状态在正文明确。
- [JZ4 chemical component: 2-propylphenol](https://www.rcsb.org/ligand/JZ4) · wwPDB Chemical Component Dictionary · CC0-1.0 — PDB archive data

  分子身份、化学式、原子名称与键级。

  将化学连接与3HTB中的结合坐标组合，生成加氢与参数化输入。
- [Predicting ligand binding affinity with alchemical free energy methods in a polar model binding site](https://doi.org/10.1016/j.jmb.2009.09.049) · Boyce et al. (2009) · Scientific citation; no reused text or figures

  3HTB模型口袋的实验研究背景。

  本讲采用局部无偏轨迹；原论文提供结合自由能研究背景。
- [Application of a Theory of Enzyme Specificity to Protein Synthesis](https://doi.org/10.1073/pnas.44.2.98) · D. E. Koshland Jr. (1958) · Scientific citation; original conceptual illustration

  诱导契合与蛋白柔性识别的历史背景。

  重写概念解释并绘制示意图；图中轮廓为概念模型。
- [Conformational changes: How small is big enough?](https://laskerfoundation.org/wp-content/uploads/2021/01/1998_koshland.pdf) · D. E. Koshland Jr. (1998) · Scientific citation; no reused text or figures

  原作者对局部构象变化与功能关系的回顾。

  以局部测量尺度解释相关科学问题。
- [General AMBER Force Field](https://ambermd.org/antechamber/gaff.html) · Amber developers; Wang et al. · Scientific/software attribution; generated molecular parameters

  GAFF原子类型、参数家族兼容性与AM1-BCC方法背景。

  显式固定GAFF及零净电荷，使用ACPYPE生成本例小分子参数。
- [ACPYPE — AnteChamber PYthon Parser interfacE](https://github.com/alanwilter/acpype) · ACPYPE contributors · GPL-3.0 for ACPYPE software

  调用AmberTools并生成GROMACS拓扑，版本2026.10.15。

  课程提供调用脚本，生成后按原子身份保持结合坐标。
