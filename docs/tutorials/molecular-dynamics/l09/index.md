# 把长链连成网络

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l09/
Language: zh-CN

用真实的珠簧网络，把连接数、连通结构、周期贯穿与准备松弛逐步分清。

## 把链连起来，为什么材料会改变

一碗煮熟的面条可以被筷子挑开，一张渔网却会把一处的拉力传给远处。两者都有细长的组成部分，差别在于这些部分是否被连接起来。高分子材料也有类似的问题：一些链彼此靠近、摩擦、穿插，另一些链之间还有稳定的交联点。橡胶的回弹、许多水凝胶的整体形状以及黏合层的承载能力，都与链之间怎样连接有关。想理解这些现象，首先要把“链很多”和“链形成网络”区分开。密集的链可以相互阻碍运动，而一条永久连接还会持续限制两个位置的相对距离，给材料增加一种持续存在的约束。

本讲从上一讲的珠簧熔体出发，把八十条短链中的一些近邻珠子连接起来，再检查整个体系发生了什么变化。这里的珠子是粗粒化的结构单元，弹簧表示连接的能量代价。一个珠子可以代表一小段真实分子，具体对应关系要由材料参数化确定。当前模型使用统一的珠子质量、长度和能量尺度，重点研究几何与连接带来的作用。这样的设置适合练习网络构建、识别孤立团簇以及检查连接后的结构调整；当研究对象是含水凝胶时，水与网络之间的相互作用、溶胀程度和离子条件需要在后续材料模型中明确加入。

可以先把链想成由小环串成的绳子。沿绳方向的小环连接已经存在，我们再用扣子把不同绳子上的小环连接起来。扣子装在端部，可能只是把两条绳子接成长一些的绳子；装在内部，则会让局部出现分叉。两个原来分开的团簇之间加一个扣子，会减少团簇数；同一团簇内部再加一个扣子，则会形成额外的闭合路线。这几个动作在总连接数上都只增加一，却改变了不同的结构特征。后面看到交联密度时，就应继续问：它数的是连接、参与连接的位点，还是能够传递载荷的网络链段？

读完本讲，你将能从LAMMPS的数据文件中恢复珠子与键组成的图，计算连通团簇、最大团簇比例和独立闭合路线数，并理解周期边界为什么需要另一项检查。你还会运行同一熔体的三种连接方案，比较加边前后的键长、温度和势能。整个过程遵循一个顺序：先确定要保留的分子关系，再让这些关系进入势能与运动方程，最后检查产生的结构。下一讲将拉伸这些已经准备好的体系。把构建与加载分开，可以清楚地看见材料响应来自哪些连接，也能看见准备阶段留下的局部应力如何影响后续结果。

## 凝胶问题怎样变成连接问题

在研究逐步聚合时，一个很自然的问题是：许多较小的分子不断连接，为什么有时会突然出现一个难以分开的整体？如果每个分子都只有两个可连接的位置，连接容易延伸成线；如果部分分子能连接三个或更多邻居，分叉就会不断出现。分叉又把原本独立的部分带进同一个大分子中。单看一条新生成的化学键，很难看出这种整体变化；把所有连接放在一起，才能讨论最大分子的大小以及不同大小分子的分布。这正是凝胶理论需要跨过的尺度：从一次局部反应，走到整个体系的连接结构。

弗洛里在1941年研究三维聚合物的分子尺寸分布与凝胶化；斯托克迈尔随后在1943年从统计方法出发研究支化链的尺寸分布和凝胶形成。他们关心的是，连接概率与分叉如何改变整个分子群体。科学史中值得带到这里的，是这种问题的组织方式：先规定可发生的连接，再推导许多连接累积后的结构。图中把这一思路画成逐渐长大的团簇。形成大团簇以后，体系里仍然可以同时存在小团簇。观察到一个巨大的连通部分，并不要求每一条原始链都已被接入，这一点会直接出现在本讲的实际数据里。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s2)

图 1 · 凝胶理论把局部成键与整个分子群体的尺寸分布联系起来。团簇图示意这种思路，右侧保留一个小团簇，说明大团簇形成时仍可有未接入的部分。

将这个思路用于计算时，可以把一个结构写成“点”和“边”。每颗珠子是一个点，每条永久键是一条边；从一个点沿着边走到另一个点，就表示两者属于同一个连通团簇。这里的“走”是数学上的查找，不需要珠子真的沿着链运动。它像查看地铁线路图：两座车站有没有换乘路线，与列车此刻开到哪里是两个问题。同样，连接图记录谁和谁有键，坐标记录这些珠子当时放在哪里。链可以弯曲、翻转、穿过周期边界，只要没有增删键，连接图中的连通关系就保持不变。

历史理论中的连接概率常常与化学反应程度相联系，本讲的连接则由一个明确的几何规则指定：先在准备好的熔体里寻找足够近、原链编号不同的珠子，再从候选列表中选边。这个规则保存了空间邻近性，因此很适合讨论现有链如何连成一个网络；它给出的结构也会受到熔体构象、选择顺序和位点占用限制的影响。要研究某一种真实交联反应，需要另外给出反应位点、反应条件以及成键规则与实验反应程度之间的对应。我们在这里先把几何、图结构和弹簧能量三者接通，建立后续材料模型可以复用的分析方法。

## 同一个熔体，怎样得到三种可比较的连接方案

三个方案都从同一个准备后的熔体快照开始：体系有一千六百颗等质量珠子，分成八十条原链，每条二十颗珠子，约化数密度为0.85。每条开放的线性链原本有十九条键，因此加边前共有一千五百二十条键。我们分别加入零、八十和一百六十条跨原链连接。这里“原链”这个名称很重要：一旦连接完成，多条原链可以属于同一个大分子，文件里的分子编号却仍用于标识它们起初属于哪条链。保留这个编号，便于比较加边前后的链尺寸；判断最终分子是否连通，则需要沿所有键重新查找。

数清珠子和键式 1

![数清珠子和键](https://ml-biomat.com/static/agent-math/34c0761ccdd5cccad86e3378.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| N | 珠子总数 | 1 |
| M | 原始开放线性链的条数 | 1 |
| n | 每条原链的珠子数 | 1 |
| B | 全部永久键的数目 | 1 |
| Bₓ | 新增跨原链键的数目 | 1 |
| 1 | 从点数减去一得到开放链边数 | 1 |
| =, +, − | 相等、相加、相减；相邻符号表示相乘 | 1 |

怎样理解一条含n个点的开放链需要n−1条连接；M条链相加，再加入Bₓ条新边。

算一个例子M=80、n=20时N=1600；Bₓ=80时，B=80×19+80=1600。

使用条件所有原链等长、开放，且构建过程中只增加指定的跨链键。

候选边的两个端点必须属于不同的原链，最近周期距离不超过1.15σ，其中σ是珠子的长度单位。最近周期距离会把穿过盒子边界的近邻也考虑进去：位于盒子左右两侧的珠子可能在周期空间中紧挨着。然后把候选边用固定随机种子打乱，按顺序挑选，同时要求每颗珠子最多参与一条新增边。这样做限制了局部连接度，避免少数珠子变成过多连接汇聚的中心。规则允许内部珠子从两条原键增加到三条键，也允许末端珠子从一条键增加到两条键，二者对网络的作用稍后再分别分析。

为了让八十条与一百六十条连接之间的比较更清楚，两组使用同一个排序后的候选列表。前八十条就是较稀连接方案，前一百六十条构成较密连接方案，因此较稀方案的每一条新键都会保留在较密方案中。两组并不是各自重新抽取一套完全不同的边。对于每个初始熔体，我们都保存所选珠子的编号及它们刚连接时的距离。这样，看到结果差异时，可以回到具体连接检查，而不是只保留一个“交联百分比”。另外两组独立准备的熔体重复相同流程，用于观察初始构象与连接选择带来的差别。

这种同起点、嵌套连接的安排，也帮助我们理解比较实验中的控制变量。对于同一个初始熔体，三种方案的珠子坐标、速度、盒子大小和温度设置一致，改变的是新增边的集合。连接加入以后，力自然改变，之后的轨迹也会逐渐分开。比较时要寻找的是同样条件下结构与响应的统计差别，而不是要求某颗珠子在各个方案里保持相同路径。三个独立初始熔体则提供另一层比较：同一种连接规则作用于不同构象时，结果变化有多大。把这两层比较分清，可以避免把某一组偶然特别致密的连接结构当成规则本身的必然结果。

所谓参与比例，也必须说明分母是什么。本例每条新增边占用两个不同珠子，而且每颗珠子最多被新增连接使用一次，所以八十条边占用一百六十颗珠子，占全部珠子的百分之十；一百六十条边占用百分之二十。这个比例描述的是本模型里被选作连接端点的珠子。真实材料的化学转化率通常以某类反应基团为分母，还可能涉及未成键的副反应或多官能基团。把两者建立对应时，需要先定义每颗珠子携带多少个反应位点。只要把分子、位点和边这三个计数层次写清，百分数就能保留明确的物理含义。

占用位点比例和平均连接度式 2

![占用位点比例和平均连接度](https://ml-biomat.com/static/agent-math/3c99deb197ed01c1f4e0c097.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| p | 参与新增边的珠子比例 | 1 |
| Bₓ | 新增边数 | 1 |
| N | 珠子总数 | 1 |
| d̄ | 每颗珠子的平均成键数 | 1 |
| B | 总边数，含原链和新增连接 | 1 |
| 2 | 每条边有两个端点 | 1 |
| =, / | 相等、相除；横线表示除法，相邻符号表示乘法 | 1 |

怎样理解把边的两个端点分别计数；每颗珠子最多参与一条新增边，所以新增端点数也等于被占用的珠子数。总连接度则把每条键计两次。

算一个例子Bₓ=80、N=1600时，p=160/1600=0.10。总键数B=1600时，平均连接度d̄=3200/1600=2。

使用条件p采用本模型的单次占用规则；平均连接度公式适用于这里的无向成键图。

## 把新增连接写进LAMMPS，邻居关系也要跟着改变

在LAMMPS数据文件的Bonds部分，一行记录一条键：先写这条键的编号，再写键类型，最后写两个端点的原子编号。编号用于查找和追踪，键类型用于选择能量参数。本例把原链的键记为类型一，把新增连接记为类型二；两种类型使用相同的FENE参数，因此类型差别只帮助我们区分它们的形成方式。FENE弹簧越接近最大伸长，阻止进一步拉长的力就越大。这里最大伸长为1.5σ，它是势能函数的定义边界。若希望研究化学断键或可逆结合，需要选择包含这些过程的连接模型及相应参数。

新增键不仅增加一项弹簧能量，也改变了哪些珠子属于直接相连的邻居。当前设置中的FENE键本身已经包含珠子之间的短程排斥，因此special_bonds fene将直接成键珠子的普通非键相互作用权重设为零，隔着两条或三条键的珠对权重保留为一。这样，直接成键珠子的排斥由键势计算一次，普通近邻的排斥由非键势计算一次。连接后的数据文件需要重新读入，使LAMMPS依据新拓扑建立这套关系。对于其他力场，隔两条和隔三条键的相互作用可能有不同缩放，修改连接时应一起核对对应的规则。

这里采用先生成完整拓扑、再读入运行的方式。几何生成程序准备熔体，建立候选边和选择列表，写出三份network.data，并为每一份生成完整的运行输入。它把初始构型的随机种子、连接列表和结果目录一起保存，便于重新产生同一比较。每个方案随后依次运行固定体积松弛、保持体积的单轴拉伸和固定形变保持三个阶段，本讲分析第一阶段；后两个阶段用于下一讲。把整个流程放在一个程序里，可以保证后面的力学比较接续同一份网络状态，同时每个阶段仍然有独立保存的数据和重启文件。

### 完整构建与运行程序

```
"""Prepare, connect, relax and stretch a FENE bead-spring network.

python run_network.py --beads 1600 --replica 1 --out-dir network-runs
The LAMMPS executable is selected by --lmp or the LAMMPS environment variable.
Each independent preparation is followed by zero, one or two links per
original chain in total. The linked cases share nested selected-edge lists.
The output retains the exact selected endpoints, inputs and simulation logs.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,re,math
import numpy as np
import os,shutil
p=argparse.ArgumentParser();p.add_argument('--beads',type=int,default=1600);p.add_argument('--replica',type=int,default=1);p.add_argument('--out-dir',type=Path,default=Path('network-runs'));p.add_argument('--lmp',default=os.environ.get('LAMMPS','lmp'));a=p.parse_args()
N=a.beads;M=N//20;assert N%20==0
base=a.out_dir.resolve();d=base/f'n{N}-rep{a.replica}'
if d.exists():raise SystemExit('Choose a new output directory for this configuration.')
d.mkdir(parents=True)
seed=20263000+a.replica;generator=np.random.default_rng(seed);L=(N/.85)**(1/3);coords=[];bonds=[]
# Pack open chains while retaining the seeded sequence of random draws.
for chain in range(M):
 current=generator.uniform(0,L,3)
 for local in range(20):
  for attempt in range(100000):
   candidate=generator.uniform(0,L,3) if local==0 else current+.97*(v:=generator.normal(size=3))/np.linalg.norm(v)
   if coords:
    dr=np.array(coords)-candidate;dr-=L*np.round(dr/L)
    if np.min(np.sum(dr*dr,axis=1))<.65**2:continue
   break
  else:raise RuntimeError('Chain packing did not find a valid location')
  coords.append(candidate.copy());current=candidate
  if local:bonds.append((len(coords)-1,len(coords)))
lines=['Generated FENE chain starting configuration','',f'{N} atoms',f'{len(bonds)} bonds','','1 atom types','2 bond types','',f'0 {L:.15g} xlo xhi',f'0 {L:.15g} ylo yhi',f'0 {L:.15g} zlo zhi','','Masses','','1 1.0','','Atoms # bond','']
for i,xyz in enumerate(coords):
 image=np.floor(xyz/L).astype(int);wrapped=xyz-L*image;lines.append(f'{i+1} {i//20+1} 1 '+' '.join(f'{x:.15g}' for x in wrapped)+' '+' '.join(str(x) for x in image))
lines+=['','Bonds','']+[f'{j+1} 1 {i} {k}' for j,(i,k) in enumerate(bonds)]
(d/'initial.data').write_text('\n'.join(lines)+'\n')
# Shared reduced-unit, neighbour and special-pair definitions.
header='''units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
'''
# Instantaneous records: time, T, U/N, K/N, E/N, pressure, box and longest bond.
record='''compute cTemp all temp
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
'''
# Soft separation, FENE switch, minimization and 100 tau melt preparation.
prepare=header+f'''read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 {seed+100} mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+200} zero yes
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
fix bath all langevin 1.0 1.0 1.0 {seed+300} zero yes
'''+record+'''run 20000
write_restart melt.restart
write_data melt.data
'''
(d/'prepare.lmp').write_text(prepare,encoding='utf-8',newline='\n')
found=shutil.which(a.lmp);assert found, f'LAMMPS executable not found: {a.lmp}';binary=Path(found).resolve();logs=[]
def run(where,script):
 cmd=[str(binary),'-in',script,'-log','simulation.log']
 r=dict(command=cmd,directory=where.relative_to(base).as_posix(),input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});t=time.perf_counter()
 with (where/'stdout.log').open('wb') as f:q=subprocess.run(cmd,cwd=where,env={**os.environ,'OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 r.update(exit_code=q.returncode,wall_seconds=time.perf_counter()-t,output_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});logs.append(r)
 (d/'progress.json').write_text(json.dumps(logs,indent=2));print(json.dumps({'directory':str(where),'exit_code':q.returncode,'wall_seconds':r['wall_seconds']}),flush=True)
 if q.returncode:raise SystemExit(q.returncode)
run(d,'prepare.lmp')
data=(d/'melt.data').read_text();atompart=re.search(r'\nAtoms[^\n]*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',data,re.S)[1]
atoms=np.array([[float(x) for x in line.split()] for line in atompart.splitlines() if line.strip()]);atoms=atoms[np.argsort(atoms[:,0])];xyz=atoms[:,3:6];mol=atoms[:,1].astype(int)
# Candidate edges connect nearby beads with different original chain IDs.
candidate=[]
for i in range(N-1):
 dr=xyz[i+1:]-xyz[i];dr-=L*np.round(dr/L);r2=np.sum(dr*dr,1)
 for j in np.flatnonzero((r2<=1.15**2)&(mol[i+1:]!=mol[i])):candidate.append((i,int(i+1+j),float(np.sqrt(r2[j]))))
# Greedy matching uses each bead once; prefixes of one list give nested cases.
edgegen=np.random.default_rng(seed+400);edgegen.shuffle(candidate);edges=[];used=set()
for i,j,dist in candidate:
 if i not in used and j not in used:edges.append((i+1,j+1,dist));used.update((i,j))
target=M*2
if len(edges)<target:raise RuntimeError(f'Only {len(edges)} available edges for {target} target')
# Each branch: 100 tau relaxation, 100 tau extension, 100 tau fixed strain.
choices=[0,M,2*M]
for nc in choices:
 sub=d/f'links-{nc}';sub.mkdir();selected=edges[:nc];text=data
 text=re.sub(r'^\d+ bonds$',f'{len(bonds)+nc} bonds',text,flags=re.M)
 match=re.search(r'\nBonds\s*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',text,re.S)
 original=match[1].strip();addition='\n'.join(f'{len(bonds)+j+1} 2 {i} {k}' for j,(i,k,_) in enumerate(selected))
 text=text[:match.start(1)]+original+'\n'+addition+'\n'+text[match.end(1):]
 (sub/'network.data').write_text(text)
 (sub/'selected-crosslinks.json').write_text(json.dumps(dict(seed=seed+400,candidates=len(candidate),selected=selected,definition='Different original chain IDs, minimum-image distance<=1.15, at most one added edge per bead; common ordered candidate list gives nested link sets.'),indent=2))
 protocol=header+f'''bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+500} zero yes
'''+record+'''run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
'''
 (sub/'network.lmp').write_text(protocol,encoding='utf-8',newline='\n');run(sub,'network.lmp')
receipt=dict(case='lammps-network',N=N,chains=M,replica=a.replica,seed=seed,rho=.85,chain_length=20,links=choices,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),source='Official LAMMPS30Sep2026Update1 bench/in.chain interaction model; independently generated coordinates and explicitly added crosslink/deformation protocols',runs=logs,exit_code=0)
(d/'receipt.json').write_text(json.dumps(receipt,indent=2));print('Network comparison complete',flush=True)
```

生成三个嵌套连接方案，保留每条新增边，并连续运行准备、拉伸和保持阶段。默认单个重复1600珠子；--replica改变独立准备编号。

### 第一组80条新边的完整LAMMPS输入

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
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
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
```

该输入由完整构建程序写出，在含相应network.data的目录执行。本讲使用前100τ，之后的拉伸与保持记录用于下一讲。

运行时，在包含这两个Python文件和运行脚本的目录中执行run.sh。脚本依次准备三个独立熔体，每个熔体产生三种连接方案，最后统一生成本讲的图和数值表。示例采用约化单位：长度按σ，能量按ε，时间按τ记录，温度目标是T*=1。把结果换成纳米、皮秒或实际温度，需要先为这些尺度指定物理对应。程序中的目录名记录珠子数和重复编号，分析程序则核对原链数、连接数及文件内容。若只想先练习生成与运行，可把单次生成命令中的珠子数改为六百四十；本讲所列统计与图像均对应一千六百珠子的三组结果。

### 运行三组构型并生成双语分析图

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python analyze_network.py network-runs --out network-analysis/en --language en
python analyze_network.py network-runs --out network-analysis/zh --language zh
```

在包含run_network.py、analyze_network.py和run.sh的目录运行；LAMMPS由--lmp或LAMMPS环境变量选择。

## 大团簇、闭合路线与悬垂部分

判断连通性可以从任意一颗尚未访问的珠子开始，找到它所有成键的邻居，再找到这些邻居的邻居，直到没有新的珠子可加入。这一轮找到的全部珠子就是一个连通团簇。随后换一颗尚未访问的珠子，重复同样的查找，直到覆盖整个体系。这种方法称为图遍历，实际程序用一个待处理列表完成。加边前，每条原链各自连通，所以有八十个团簇，每个二十颗珠子。加边之后，团簇可能合并，但珠子的空间位置仍在热运动中变化。因此，先由键表判断归属，再由坐标研究形状，是一个清楚的分析顺序。

最大团簇占比式 3

![最大团簇占比](https://ml-biomat.com/static/agent-math/4ebb9e2b58f74ffad9f5fb1b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Pₘₐₓ | 属于最大连通团簇的珠子比例 | 1 |
| Nₘₐₓ | 最大连通团簇中的珠子数 | 1 |
| N | 体系珠子总数 | 1 |
| max | 在所有连通团簇中取最大的下标标记 | 1 |
| =, / | 相等；横线表示相除 | 1 |

怎样理解用所关心部分的珠子数除以总体珠子数，得到从体系随机选一颗珠子时落在最大团簇中的比例。

算一个例子第一组80条新增边：Nₘₐₓ=63×20=1260，Pₘₐₓ=1260/1600=0.7875。

使用条件本例珠子等质量，所以珠子比例也等于质量比例；不同质量时，质量比例需要改为质量求和。

第一组构型加入八十条边后，有十三个团簇，最大团簇包含六十三条原链，也就是一千二百六十颗珠子，占体系的0.7875。加入一百六十条边后，只剩两个团簇，最大团簇包含七十九条原链，占0.9875。连接数翻倍，并没有把所有链都接入同一个团簇。第二、第三组构型在八十条边时分别有十三和十八个团簇，最大团簇都包含六十二条原链。这些差别来自原有空间构象与具体连接列表。把三个结果并列画出，比只显示一张看起来很密的网络图片更能说明连接规则实际产生了怎样的结构。

### 三组真实网络的连通性

点表示各构型的实际键表统计；连线帮助比较新增边数。最大团簇比例、团簇数和独立闭合路线数分别回答不同问题。

LAMMPS 30 Sep 2026 Update 1；官方珠簧相互作用模型，1600个珠子、80条20珠链，ρ*=0.85、T*=1，三个初始构型；FENE/WCA正式动力学时间步0.005τ。

[下载参考数据与完整输入（ZIP） 2.33 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-connectivity-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s5)

三个初始熔体分别增加0、80、160条永久连接，得到九个拓扑。图中的最大组分比例、独立回路数和周期绕行秩由实际键表与初态坐标计算，并与100τ松弛后结构核对；连接数与网络结构在图中分开衡量。

再看一条边究竟做了什么。如果它连接两个原来独立的团簇，团簇数会减一，同时总边数加一；如果两个端点原本已有一条路径连通，新边就会增加一条独立闭合路线。独立的意思是，这条闭合路线增加了先前路线组合中没有的闭环关系。图论用“总边数减总点数再加团簇数”来计算这个数。加边前，每条链是一棵没有闭合路线的树；第一组八十条新边中，六十七条用于合并八十个团簇为十三个，其余十三条提供独立闭合路线。这个计数也能用来检查程序是否遗漏了某些连接。

独立闭合路线的计数式 4

![独立闭合路线的计数](https://ml-biomat.com/static/agent-math/13f6200a36cd44df7485535b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| μ | 独立闭合路线数，也称图的循环秩 | 1 |
| B | 总边数；同一对原链间的多条边分别计数 | 1 |
| N | 珠子图中的点数 | 1 |
| C | 连通团簇数 | 1 |
| =, −, + | 相等、相减、相加 | 1 |

怎样理解C个互不相连的树总共需要N−C条边；比这个数多出的每条边增加一个独立闭合路线。

算一个例子第一组80条新增边后，B=1600、N=1600、C=13，所以μ=13。160条新增边时，μ=1680−1600+2=82。

使用条件这是有限无向图的拓扑计数；周期绕行方向另由闭合位移检查。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s5)

图 2 · 相同的一条新增边，在两个团簇之间会合并团簇，在同一个团簇内部会增加独立闭合路线。

局部连接度也可以用手算检查。未加边时，八十条链共有一百六十颗末端珠子，它们各有一条键；其余一千四百四十颗内部珠子各有两条键。第一组八十条新增边占用了二十一颗末端珠子和一百三十九颗内部珠子，因此最后有一百三十九颗一连接珠子、一千三百二十二颗二连接珠子和一百三十九颗三连接珠子。三类计数加起来仍是一千六百，连接度加总则等于总键数的两倍，因为每条键都有两个端点。这个小练习说明，平均连接度等于二的体系既可能是很多线性链，也可能包含分叉与悬垂端，需要继续检查完整分布。

把每条原链收缩成图上的一个点，可以更直观地查看新增连接。图中八十个点沿圆周摆放，圆周位置用于清楚排列编号；线条来自实际选择的跨链连接。同一对原链之间可以有多条连接，它们在计算时各自保留。这样的图强调谁与谁相连，而分子轨迹强调真实空间中的构象。另外还要留意悬垂部分：一个末端伸出的链段可能随着热运动摆动，却没有像跨越两个网络接点的链段那样约束两处相对运动。最终承担弹性响应的结构，需要结合接点、悬垂支路、闭合路线以及加载方向一起判断。

### 把第一组的80条原链收缩成图节点

圆周上的节点位置按原链编号排列，线条对应实际新增连接；青色为最大团簇，橙色为其余部分。零连接时各链同样大，图中均为橙色。同一对原链的多条边在图上重合，在计算中分别保留。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s5)

每个节点代表原来的整条20珠链，节点沿圆周按链编号排列；节点间的边来自实际新增跨链连接。圆上的位置用于清楚显示连接关系，三维几何位置另保存在模拟坐标中。

[Figure: 八条原链的连接图](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s5)

每个点表示一条原链；边表示新增连接。图上位置用于排列编号，颜色区分连通团簇。

八条原链的连接图练习：比较相同边数、不同连接顺序得到的团簇与闭合路线。

## 穿过周期边界，和贯穿周期网络有什么不同

周期盒子相当于把一个小盒子沿三个方向重复铺开。一个珠子走出右边，就从左边对应的位置继续出现。对于一条有限的链，可以顺着键把跨边界的珠子移回相邻镜像，让整条链在同一个展开空间中保持连续。连接更多以后，情况会变得有趣：沿某条闭合的键路线走一圈，可能回到起始珠子的另一个周期镜像。它们在主盒子里有同一个编号，在展开的无限空间里却相隔一个或多个盒长。这样的闭合路线表明，网络通过周期复制延伸到了相邻盒子，而不是只在盒子内部形成一个有限团簇。

仅仅看见一条键穿过边界，还不足以分辨这两种情况。一条很短的链也可能恰好横跨盒子的左右边界，把它整体平移就能显示成普通的有限链。更可靠的办法是沿闭合路线累计每段键的最近周期位移。如果这条路线只在有限空间中绕回原点，累计位移为零；如果累计位移等于一个盒长乘某个非零整数向量，就出现了周期绕行。整数向量的三个分量分别记录沿三个方向净跨越了多少个盒长。程序利用这项检查，区分普通的闭合小环与能联系不同周期镜像的路线。

沿闭合路线累计周期位移式 5

![沿闭合路线累计周期位移](https://ml-biomat.com/static/agent-math/87916823504495865d28552b.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| 𝒞 | 一条有指定行走方向的闭合成键路线 | 1 |
| k | 路线上的一段键 | 1 |
| Δrₖ | 沿行走方向的最近周期键位移向量 | σ |
| Σ, ∈ | 把所列路线上的各段相加；属于该集合 | 1 |
| Lₓ, Lᵧ, L𝓏 | 正交盒子的三个边长 | σ |
| w, wₓ, wᵧ, w𝓏 | 周期绕行整数向量及三个分量 | 1 |
| ℤ³ | 由三个整数组成的向量集合 | 1 |
| =, (, ), , | 相等；括号和逗号按x、y、z排列向量分量，相邻符号相乘 | 1 |

怎样理解主盒子的同一珠子编号在展开空间中可以有不同镜像。闭合路线的总位移只能是各方向盒长的整数倍。

算一个例子若盒长都是10σ，闭合路线累计位移为(10σ,0,0)，则w=(1,0,0)，表示沿x方向绕行一个周期。累计为零时w=(0,0,0)。

使用条件用于正交周期盒子；每段键取短于半盒长的最近镜像。本例键长远小于该上限。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s6)

图 3 · 左侧是一条跨越边界的有限链；右侧的闭合编号路线在展开空间中通向起始点的相邻镜像，沿x方向绕行一次。

如果所有非零绕行向量都沿同一个方向，它们提供的是一种独立的周期延伸；如果还存在无法由这个方向组合出来的第二、第三个方向，周期延伸的独立方向数就会增加。这里用向量组的秩来数这种独立性：秩一、二、三分别表示一、二、三个独立方向。它强调方向是否相互独立，而不是一条路线看起来有多长。举例说，绕行向量为(1,0,0)和(2,0,0)，仍然只有一个独立方向；再加入(0,1,0)才得到第二个。分析程序会保存原始整数向量，使这个判断可以回到具体闭合路线检查。

本例六个带连接的体系，在刚连接和松弛一百τ后，最大团簇的绕行秩都是三；未加边的体系则由八十条有限原链组成。这个结果告诉我们，带连接方案已经在周期拓扑上建立了三个独立方向的延伸。它与最大团簇占比一起描述网络形态，但弹性模量还取决于链段构象、温度、松弛和受力方式。另一个实际问题是，贯穿周期空间的网络通常无法给每颗珠子选定一组镜像，让所有闭合路线同时成为有限盒外的闭合曲线。因此，整张网络的展开尺寸需要谨慎定义，而保留原链编号仍可让我们测量各条有限原链的尺寸变化。

还可以把盒子大小看成一个需要控制的尺度。小盒子通过周期复制，使同一段局部结构反复出现；改变盒子大小或链数，可能改变绕行路线出现的概率。若研究目标是寻找凝胶形成的临界条件，就需要在多个体系尺寸和多个连接比例下重复构建，统计大团簇与周期绕行随条件的变化。当前的三种连接数提供了具体网络之间的对照，适合学习结构分析与后续加载。把有限体系中的观察组织成尺寸系列，才进一步接近宏观材料中“何时形成贯通网络”的问题，也能区分边界重复与体相连接产生的影响。

## 连接完成以后，为什么还要让网络松一口气

候选距离限制保证新键不会一开始就接近FENE的最大伸长，但它没有保证每条新键都处在偏好的长度附近。熔体中原本相邻的两颗珠子，只需满足非键排斥与周围堆积；一旦加上弹簧，它们还要承担弹性拉力。第一组构型八十条新增键的初始平均长度为1.0791σ，松弛一百τ后变为0.9665σ。原链键在连接前的平均长度约为0.9651σ，这个比较能说明新增连接如何从几何邻近转向受到弹簧约束的距离分布。缩短某一条键还会牵动周围链段，因此整个网络需要通过许多珠子的共同运动重新分配局部应力。

### 新增键从几何邻近走向弹簧约束

左图分别汇总三组80或160条新增键，虚线为刚连接，实线为100τ后；右图保留六个带连接体系各自的最大键长时间记录。FENE的最大伸长参数为1.5σ。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s7)

新增连接在初态与100τ松弛后采用相同身份配对比较。距离由周期最短位移计算，单位为σ；原来的主链键与后来增加的连接分别统计，最大允许伸长R₀=1.5σ由所用FENE模型给定。

加边的瞬间，珠子位置和速度可以保持原样，势能却会改变，因为描述体系的能量函数已经增加了连接项。在本模型中，新成键珠对的排斥原来由非键WCA势承担，成键后由FENE键内相同的排斥项承担，两者恰好对应。因此，在同一组坐标上，新旧势能的差只剩新增键的FENE弹性部分。第一组八十条边给出的势能增量为每颗珠子1.24037ε，直接按保存的新键长度逐条计算得到相同结果。这是一个很有用的核对：它同时检查键确实加入、参数使用正确以及短程排斥没有重复计算。

同一坐标上新增连接的势能代价式 6

![同一坐标上新增连接的势能代价](https://ml-biomat.com/static/agent-math/e54c6ec00f905aa9880a1fd1.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ΔU | 加入指定连接后总势能的增量 | ε |
| N | 珠子总数 | 1 |
| K | FENE弹性系数，本例30ε/σ² | ε/σ² |
| R₀ | 最大伸长参数，本例1.5σ | σ |
| Bₓ, j | 新增键总数和其中一条键的编号 | 1 |
| rⱼ | 第j条新增键刚连接时的最近周期长度 | σ |
| Σ | 将j从1到Bₓ的所有项相加 | 1 |
| ln | 自然对数；本式括号内数量为正且无量纲 | 1 |
| ² | 平方，即该数量与自身相乘 | 1 |
| Δ, =, −, / | 变化量标记、相等、负号或相减、相除；相邻量相乘 | 1 |
| 1, 2, [, ], (, ) | 常数一和二；括号限定运算顺序 | 1 |

怎样理解新键内的WCA排斥替代了同一珠对原来的非键WCA排斥，两者抵消；剩余差值是FENE弹性项。求总和后除以N得到每颗珠子的增量。

算一个例子一条r=1σ的新键，弹性增量=−(30×1.5²/2)ln(1−1/1.5²)=19.8378ε。若N=1600，它贡献0.0123986ε/珠子；实际80条键用各自长度求和，得到1.24037191ε/珠子。

使用条件比较完全相同的坐标，使用相同WCA参数和special_bonds fene；每条键满足0<rⱼ<R₀。这里计算连接操作造成的势能改变。

开始积分以后，较长的新键缩短，势能可以转化为珠子的运动能量，热浴再与体系交换能量，使温度围绕T*=1波动。本例继续采用Langevin热浴，阻尼时间为一τ，时间步为0.005τ。在温度图旁同时画出势能调整，可以把这几个过程联系起来：热浴控制的是运动统计，结构松弛则体现在键长、链段形状和能量随时间的变化。势能曲线按每个分支自身的起点作差，便于查看各自的调整过程。三种拓扑具有不同数量的能量项，比较其绝对势能时，应同时说明连接数和能量定义。

### 同一起点三种拓扑的温度与势能调整

第一组构型的真实0–100τ记录。温度虚线为T*=1；势能按各分支自己的起点作差，单位为每颗珠子的ε。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/#zh-s7)

九个体系0–100τ的固定体积松弛记录。温度使用模型约化单位，势能按1600个珠子归一化；不同初始连接带来的能量变化保留在各条曲线中，随后才能在同一准备流程下比较结构与受力。

检查最大键长，可以及时发现局部是否出现接近定义边界的高伸长。再检查团簇数、闭合路线和绕行秩，就能确认松弛过程中连接关系与预期一致。这里使用永久键，在一百τ内的结构变化主要来自珠子位置重新安排。若温度已经稳定，而某些链段形状或应力仍缓慢变化，延长准备时间就会回答它们是否继续调整。对于后续拉伸，我们保留松弛终点的数据文件和重启文件，以同一状态开始加载。这样，初始网络怎样建立、已经松弛多久、加载之前有哪些残余结构，都能在后续比较中保持明确。

固定体积的准备还保留了一个清楚的材料条件：网络没有通过改变整体体积来消除新增连接造成的应力。对于真实水凝胶，网络常会吸水或失水，尺寸由弹性约束与溶剂作用共同决定；对于被模具或基底约束的材料，固定体积或固定部分尺寸可能更接近实际准备过程。选择哪一种方式，应与后续要解释的实验条件相连。当前流程把盒子保持在原来的密度，允许珠子在盒内重新安排，因此接下来得到的是这个固定密度网络在规定热浴和加载条件下的响应。读者也可以据此设计体积可调的对照，研究制备约束怎样改变初始应力。

## 从连接统计走向可解释的材料比较

完整分析程序把前面的检查串在一起。它读取九个方案的初始网络与松弛后网络，按珠子编号恢复所有键，检查新边端点、距离限制和嵌套关系，再计算连通团簇、闭合路线及周期绕行。随后读取温度与势能记录，提取零到一百τ的准备阶段，绘制同一套定义下的比较图。所有数字同时写入JSON和CSV，便于继续分析。图上将三组初始构型分开显示，新键长度分布则把三组同连接数的键集中起来，比较连接瞬间与松弛终点。统计对象与合并方式需要随着图一起阅读，才能看清每条曲线回答什么问题。

### 完整连接图、周期绕行与松弛分析

```
"""Measure the actual fixed-topology networks and their initial relaxation.

python analyze_network.py network-runs --out network-analysis --language en
Requires NumPy and Matplotlib. The input directory contains n1600-rep1/2/3.
Each replica contains links-0/80/160 with network.data, relaxed.data,
selected-crosslinks.json and thermo.dat. 
"""
from pathlib import Path
import argparse
import csv
import json
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.collections import LineCollection


def read_data(path):
    """Read the orthogonal atom_style bond files used in this example."""
    text = path.read_text(encoding="utf-8")
    sections, section = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z ]*", line):
            section = line
            sections[section] = []
        elif section:
            sections[section].append(line.split())
    atoms = np.asarray(sections["Atoms"], float)
    atoms = atoms[np.argsort(atoms[:, 0])]
    assert np.array_equal(atoms[:, 0], np.arange(1, len(atoms) + 1))
    bonds = np.asarray(sections["Bonds"], int)
    bounds = []
    for direction in "xyz":
        found = re.search(rf"^([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+{direction}lo {direction}hi", text, re.M)
        bounds.append([float(found[1]), float(found[2])])
    bounds = np.asarray(bounds)
    return {"xyz": atoms[:, 3:6], "mol": atoms[:, 1].astype(int),
            "box": bounds[:, 1]-bounds[:, 0], "bonds": bonds}


def bond_geometry(data):
    ends = data["bonds"][:, 2:4] - 1
    delta = data["xyz"][ends[:, 1]] - data["xyz"][ends[:, 0]]
    shift = -np.rint(delta / data["box"]).astype(int)
    minimum_image = delta + shift * data["box"]
    return ends, shift, np.linalg.norm(minimum_image, axis=1)


def connectivity(data):
    """Graph components, cycle counts and independent periodic directions.

    Integer image offsets are propagated along a spanning tree. A cycle that
    closes at a different periodic image leaves a nonzero integer vector.
    The rank of these vectors counts independent periodic winding directions.
    """
    n = len(data["xyz"])
    ends, shifts, lengths = bond_geometry(data)
    graph = [[] for _ in range(n)]
    for edge_id, ((i, j), shift) in enumerate(zip(ends, shifts)):
        graph[i].append((j, shift, edge_id))
        graph[j].append((i, -shift, edge_id))
    labels = np.full(n, -1, int)
    offsets = np.zeros((n, 3), int)
    components = []
    for root in range(n):
        if labels[root] >= 0:
            continue
        label = len(components)
        labels[root] = label
        stack, vertices, edge_ids, closures = [root], [], set(), []
        while stack:
            i = stack.pop()
            vertices.append(i)
            for j, shift, edge_id in graph[i]:
                edge_ids.add(edge_id)
                trial = offsets[i] + shift
                if labels[j] < 0:
                    labels[j] = label
                    offsets[j] = trial
                    stack.append(j)
                else:
                    assert labels[j] == label
                    closure = trial - offsets[j]
                    if np.any(closure):
                        closures.append(closure.tolist())
        unique_closures = np.unique(closures, axis=0) if closures else np.empty((0, 3), int)
        rank = int(np.linalg.matrix_rank(unique_closures.astype(float), tol=1e-10)) if len(unique_closures) else 0
        components.append({"beads": len(vertices), "edges": len(edge_ids),
                           "original_chains": len(np.unique(data["mol"][vertices])),
                           "independent_cycles": len(edge_ids)-len(vertices)+1,
                           "winding_rank": rank,
                           "integer_closure_vectors": unique_closures.tolist()})
    largest_id = int(np.argmax([c["beads"] for c in components]))
    largest = components[largest_id]
    degree = np.array([len(x) for x in graph])
    return {"components": components, "component_count": len(components),
            "largest": largest, "largest_id": largest_id, "labels": labels,
            "total_cycles": len(ends)-n+len(components), "degree": degree,
            "lengths": lengths, "ends": ends}


def numeric_rows(path):
    return np.loadtxt(path, comments="#")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("network-analysis"))
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        base = args.directory / f"n1600-rep{replica}"
        previous_edges = set()
        for count in (0, 80, 160):
            folder = base / f"links-{count}"
            before = read_data(folder / "network.data")
            after = read_data(folder / "relaxed.data")
            graph = connectivity(before)
            later = connectivity(after)
            n = len(before["xyz"])
            assert n == 1600 and len(np.unique(before["mol"])) == 80
            selected = json.loads((folder / "selected-crosslinks.json").read_text(encoding="utf-8"))["selected"]
            chosen = {tuple(sorted((int(x[0]), int(x[1])))) for x in selected}
            assert len(chosen) == count and previous_edges <= chosen
            previous_edges = chosen
            added = before["bonds"][:, 1] == 2
            endpoints = graph["ends"][added]
            assert len(endpoints) == count
            assert len(np.unique(endpoints)) == 2*count
            assert np.all(before["mol"][endpoints[:, 0]] != before["mol"][endpoints[:, 1]])
            assert np.all(graph["lengths"][added] <= 1.15 + 1e-10)
            assert graph["component_count"] == later["component_count"]
            assert graph["largest"]["winding_rank"] == later["largest"]["winding_rank"]
            # Equal masses make the largest bead fraction a mass fraction too.
            largest_fraction = graph["largest"]["beads"] / n
            t = numeric_rows(folder / "thermo.dat")
            t = t[(t[:, 1] >= 0) & (t[:, 1] <= 100)]
            assert len(t) == 201
            elastic_added = float(np.sum(-.5*30*1.5**2*np.log1p(-(graph["lengths"][added]/1.5)**2)))
            if count == 0:
                reference_energy = t[0, 3]
            observed_change = float(t[0, 3]-reference_energy)
            assert abs(observed_change-elastic_added/n) < 1e-9
            assert np.max(graph["degree"]) <= 3
            old_lengths = graph["lengths"][~added]
            new_lengths = graph["lengths"][added]
            relaxed_new = later["lengths"][after["bonds"][:, 1] == 2]
            rec = {"replica": replica, "added_links": count,
                   "beads": n, "total_bonds": len(before["bonds"]),
                   "component_count": graph["component_count"],
                   "largest_component_beads": graph["largest"]["beads"],
                   "largest_component_chains": graph["largest"]["original_chains"],
                   "largest_mass_fraction": largest_fraction,
                   "total_independent_cycles": graph["total_cycles"],
                   "largest_winding_rank": graph["largest"]["winding_rank"],
                   "modified_bead_fraction": 2*count/n,
                   "mean_degree": float(graph["degree"].mean()),
                   "degree_counts": {str(k): int(np.sum(graph["degree"] == k)) for k in (1, 2, 3)},
                   "initial_U_change_per_bead": observed_change,
                   "sum_added_FENE_elastic_per_bead": elastic_added/n,
                   "original_bond_initial_mean": float(old_lengths.mean()),
                   "added_bond_initial_mean": float(new_lengths.mean()) if count else None,
                   "added_bond_after_100tau_mean": float(relaxed_new.mean()) if count else None,
                   "max_bond_before": float(graph["lengths"].max()),
                   "max_bond_after_100tau": float(later["lengths"].max()),
                   "late_50_100tau_temperature_mean": float(t[t[:, 1] >= 50, 2].mean()),
                   "components": graph["components"]}
            records.append(rec)
            raw[(replica, count)] = (before, after, graph, later, t)
    summary = {"case": "fixed FENE networks", "records": records,
               "topology": "All edges retained, including parallel connections between original chains.",
               "winding": "Rank of integer closure vectors; connectivity is distinct from mechanical response.",
               "time_scope": "Topology at insertion; before/after100tau fixed-volume relaxation. All statistics are finite-window descriptors."}
    (args.out / "network_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    table = [{k: v for k, v in rec.items() if k not in ("components", "degree_counts")} for rec in records]
    with (args.out / "network_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    colors = ["#187e89", "#ca713f", "#7663a0"]
    def save(fig, name):
        fig.savefig(args.out / f"{name}.svg")
        fig.savefig(args.out / f"{name}.png", dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for replica, color in enumerate(colors, 1):
        rr = [x for x in records if x["replica"] == replica]
        for ax, key in zip(axes, ["largest_mass_fraction", "component_count", "total_independent_cycles"]):
            ax.plot([x["added_links"] for x in rr], [x[key] for x in rr], "o-", color=color,
                    label=tr(f"构型 {replica}", f"Configuration {replica}"), alpha=.8)
    axes[0].set_ylabel(tr("最大连通分量质量分数", "Largest-component mass fraction"))
    axes[0].set_ylim(0, 1.05)
    axes[1].set_ylabel(tr("连通分量数", "Connected components"))
    axes[2].set_ylabel(tr("独立环数 E − V + C", "Independent cycles E − V + C"))
    for ax in axes:
        ax.set_xlabel(tr("新增连接数", "Added connections")); ax.set_xticks([0, 80, 160]); ax.grid(alpha=.2)
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同一熔体逐步加边：哪些链已经连在一起", "Adding edges to each melt: which chains are connected"), fontsize=19)
    save(fig, "network-connectivity")
    # A chain-level circular graph is a connectivity drawing, not a spatial projection.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    theta = np.linspace(0, 2*np.pi, 80, endpoint=False)
    positions = np.column_stack([np.cos(theta), np.sin(theta)])
    for ax, count in zip(axes, (0, 80, 160)):
        data, _, graph, _, _ = raw[(1, count)]
        selected = data["bonds"][:, 1] == 2
        chain_ends = data["mol"][graph["ends"][selected]]-1
        segments = positions[chain_ends]
        if len(segments):
            ax.add_collection(LineCollection(segments, colors="#6c9c99", linewidths=.7, alpha=.5))
        chain_labels = graph["labels"][np.arange(80)*20]
        in_largest = chain_labels == graph["largest_id"]
        # At zero links all components are tied; use the same color for all chains.
        node_colors = np.where(in_largest, "#177d88", "#d59564") if count else ["#d59564"]*80
        ax.scatter(positions[:, 0], positions[:, 1], c=node_colors, s=26, zorder=3)
        rr = next(x for x in records if x["replica"] == 1 and x["added_links"] == count)
        ax.set_title(tr(f"{count} 条新增边", f"{count} added edges"))
        ax.text(0, -1.3, tr(f"最大分量：{rr['largest_component_chains']}/80 条链", f"Largest component: {rr['largest_component_chains']}/80 chains"), ha="center", fontsize=12)
        ax.set_aspect("equal"); ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.46, 1.15); ax.axis("off")
    fig.suptitle(tr("构型 1 的连接图：每个圆点代表一条原始链", "Configuration 1 connectivity: one node per original chain"), fontsize=18)
    save(fig, "network-chain-graph")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), constrained_layout=True)
    bins = np.linspace(.85, 1.20, 36)
    for count, color in zip((80, 160), colors[:2]):
        for stage, linestyle in [(0, "--"), (1, "-")]:
            vals = []
            for replica in (1, 2, 3):
                before, after, graph, later, t = raw[(replica, count)]
                dat, gg = (before, graph) if stage == 0 else (after, later)
                vals.extend(gg["lengths"][dat["bonds"][:, 1] == 2])
            axes[0].hist(vals, bins=bins, density=True, histtype="step", lw=2, color=color, linestyle=linestyle,
                         label=f"{count}: " + (tr("刚加边", "Just connected") if stage == 0 else tr("100τ 后", "After 100τ")))
    for replica, color in enumerate(colors, 1):
        for count, linestyle in [(80, "--"), (160, "-")]:
            t = raw[(replica, count)][4]
            axes[1].plot(t[:, 1], t[:, 12], color=color, ls=linestyle, lw=1.1, alpha=.7,
                         label=tr(f"构型{replica} · {count}边", f"Config. {replica} · {count} links"))
    axes[0].set(xlabel=tr("新增键长 / σ", "Added-bond length / σ"), ylabel=tr("概率密度 / σ⁻¹", "Probability density / σ⁻¹"))
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("全体系最大键长 / σ", "Largest bond length / σ"))
    for ax in axes:
        ax.legend(frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2); ax.grid(alpha=.2)
    fig.suptitle(tr("连接后的局部几何松弛", "Local geometrical relaxation after adding connections"), fontsize=19)
    save(fig, "network-bond-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.4), sharex=True, constrained_layout=True)
    for count, color in zip((0, 80, 160), colors):
        t = raw[(1, count)][4]
        axes[0].plot(t[:, 1], t[:, 2], color=color, lw=1.1, label=tr(f"{count} 条新增边", f"{count} added edges"))
        axes[1].plot(t[:, 1], t[:, 3]-t[0, 3], color=color, lw=1.3)
    axes[0].axhline(1, color="#6d7779", ls="--", lw=1)
    axes[0].set_ylabel(tr("温度 T*", "Temperature T*")); axes[0].legend(frameon=False, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=3, fontsize=11)
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("相对各分支起点的 Δ(U/N) / ε", "Δ(U/N) from each branch's start / ε"))
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle(tr("构型 1：固定连接后的温度与势能调整", "Configuration 1: temperature and energy after fixing the connections"), fontsize=18)
    save(fig, "network-preparation")
    print(json.dumps(table, indent=2))


if __name__ == "__main__":
    main()
```

分析network-runs下的三个n1600-rep目录，每个含links-0、links-80、links-160。输出四组图以及逐条件JSON和CSV。

回到开头的材料问题，连接数增加确实改变了这些体系的结构：最大团簇通常纳入更多原链，独立闭合路线增加，局部连接度的分布也发生变化。第一组八十条新增边之后，平均每颗珠子的连接度正好为二，但体系里同时存在一条键、两条键和三条键的珠子。平均值把它们混在一起，无法说明分叉分布在什么位置。类似地，最大团簇占比接近一也会同时容纳悬垂链段、小环与跨越周期空间的路线。描述网络时，把几个互补指标放在同一张结构图景里，通常比寻找一个包办所有现象的交联密度更有解释力。

把这种方法移到生物材料时，可以先明确真正想研究的连接是什么。化学交联的水凝胶可把稳定共价连接作为永久边，再单独描述溶剂；物理凝胶中的可逆结合则需要让结合概率或寿命进入模型；蛋白质构成的网络还可能具有方向性、特定结合位点和可变构象。每一种选择都会改变哪些运动被保留、哪些连接能够变化，以及怎样把模拟时间对应到实验。当前的等质量珠簧体系提供了一个清楚的起点：先确定拓扑与空间约束，再逐步加入材料所需的分子细节，使新增复杂性对应一个具体问题。

准备开展下一步比较时，可以给每个体系保留一张简明的结构记录：原链数与链长、新增边列表、最大团簇比例、独立闭合路线数、周期绕行方向以及松弛终点。比较材料力学时，再把加载速度、温度、体积变化和应力定义补上。这样，遇到某组网络拉伸时反而表现较软，就能查看它的连接位置和初始构象，而不必立即把差异归结为程序错误。下一讲将沿这个顺序对同一批网络施加形变：从实际盒长算伸长比，从压力张量得到拉伸应力，再观察固定形变以后应力如何随链段调整而变化。

## 延伸阅读与开放资料

- [LAMMPS 30 September 2026 Update 1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE珠簧相互作用、约化单位和Langevin积分组合。

  沿用L08教学熔体：1600珠子、80条20珠链、密度0.85；WCA精确截断、时间步0.005τ、热浴阻尼1τ。新增永久连接选择、三组构型、松弛与拉伸流程及完整图分析。
- [bond_style fene; special_bonds; read_data](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation; cited for definitions

  FENE能量项、直接成键排斥与数据拓扑定义。

  公式解释、算例与图解独立编写。
- [special_bonds command](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation; cited for command semantics

  fene权重0、1、1及键表对特殊邻居的定义。

  围绕新增连接解释相互作用计数。
- [read_data command](https://docs.lammps.org/read_data.html) · LAMMPS developers · Official documentation; cited for command semantics

  Bonds数据格式和周期贯穿体系的镜像关系。

  原创闭合路线图与周期绕行分析。
- [Molecular Size Distribution in Three Dimensional Polymers. I. Gelation (1941)](https://doi.org/10.1021/ja01856a061) · Paul J. Flory · Research article citation; no original text or image reproduced

  凝胶化与分子尺寸分布的科学史。

  用原创团簇图解释研究问题。
- [Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers (1943)](https://doi.org/10.1063/1.1723803) · Walter H. Stockmayer · Research article citation; no original text or image reproduced

  支化连接与凝胶形成的统计思路。

  历史叙述结合公开学术传记核对。
- [Walter Hugo Stockmayer: A Biographical Memoir (2017)](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf) · Jeffrey Kovac and Marshall Fixman · National Academy of Sciences memoir; citation and paraphrase, no image reproduced

  核对1941—1943年凝胶研究的背景与联系。

  历史信息用于本讲原创概念解释。
