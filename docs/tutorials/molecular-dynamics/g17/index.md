# 让分子走过少见的构象：伞形采样与自由能

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g17/
Language: zh-CN

沿十残基短肽的端距布置观察窗口，读懂偏置、重叠、构象历史与真实自由能剖面的变化。

## 分子为什么愿意停留在某些形状里

把一条柔软的带子对折，再慢慢拉开，两端距离相同的时候，带子仍可能有许多不同的弯曲方式。短肽也是如此：末端靠近，可以形成紧凑的折叠，也可以只是碰巧回到一起；末端拉远，则可能伴随主链转动、侧链接触改变和周围水的重新排列。研究者希望知道哪些构象更常出现，以及从紧凑状态走向伸展状态时，沿途哪些距离较难被访问。这些问题涉及蛋白折叠、分子识别和受力响应，也是从“看分子怎样动”走向“理解它为何这样分布”的一步。

此前的轨迹让我们测量均值和涨落，但一个分子可能在同一类构象附近停留很久。假如门后有一间很大的房间，而通道很窄，短时间在门外观察的人可能一次也进不去；看不到里面的人流，并不能直接知道房间有多大。分子构象空间中的采样也有类似困难：某些区域容易停留，连接区域访问较少，有限轨迹就难以建立不同区域的相对概率。我们需要一种能把观察机会分配到指定区域、又能在分析时恢复原始统计权重的方法。

本节用一条只有10个氨基酸的短肽chignolin，沿第一个和最后一个残基的Cα原子间距离开展伞形采样。我们先用移动的弹簧偏置生成一组不同端距的构象，再在多个固定弹簧中心附近分别记录运动，最后将这些带偏置的记录组合成一个自由能剖面。每一步都有实际结果可读：拉伸曲线告诉我们初始构象怎样得到，窗口分布告诉我们相邻记录如何衔接，分段比较则告诉我们延长采样应优先关注哪里。

这里的自由能包含相互作用能与构象数量的共同影响。若许多不同的分子摆法都对应某个端距，即使每种摆法的势能不特别低，这个距离也可能经常出现。可以把势能理解为某一具体摆法的能量，而自由能剖面把对应同一端距的许多摆法汇总到一起。对热平衡下定义一致的距离概率密度，两个位置的相对自由能由概率比的对数给出。取对数使相乘的概率比变成相加的能量差，也让很大的概率差异变成容易比较的数值范围。

把出现频率转成相对自由能式 1

![把出现频率转成相对自由能](https://ml-biomat.com/static/agent-math/8d8b418525882e0881b9b260.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| W(ξa), W(ξb) | 坐标位置a、b处的自由能剖面值 | kJ/mol |
| ξa, ξb | 两处端距；a、b是位置标签 | nm |
| p₀(ξ) | 无偏平衡端距的概率密度；下标0表示已去掉采样偏置 | nm⁻¹ |
| R | 摩尔气体常数0.008314462618 | kJ mol⁻¹ K⁻¹ |
| T | 绝对温度，本例298 | K |
| p₀(ξb)/p₀(ξa) | 概率密度之比，单位约掉后才能取对数 | 1 |
| ln | 自然对数，对应底数e | 1 |
| =, −, /, ( ), [ ] | 相等、相减或取负、相除、分组；RT表示相乘 | 1 |

怎样理解平衡概率随自由能按指数衰减，取密度比消去归一化常数，再取对数得到差值。

算一个例子298 K时RT=2.47771 kJ/mol。若b的密度为a的十分之一，Wb−Wa=5.70514 kJ/mol。

使用条件针对指定坐标及一致的概率密度定义；沿距离的构象简并已包含在密度中。

概率密度可以先理解为“每单位距离里出现的机会”。如果某个0.01 nm宽的小格包含全部记录的百分之五，那么对应密度是0.05除以0.01，即5 nm⁻¹。它的数值可以大于1，因为只有乘上格宽后才得到这个小格的概率。比较两个位置时，密度使用相同单位，取比值后单位相消，才适合放进对数。这样从计数走到密度、再走到自由能，每一步都有明确的单位和统计含义。

在298 K，RT约为2.478 kJ/mol，概率密度相差10倍对应约5.705 kJ/mol的相对自由能差。较常出现的位置具有较低的剖面值，零点则可以按比较需要选择。这种联系针对已定义的端距分布，包含了该坐标对应的构象数量。端距剖面与一对孤立原子的相互作用势具有不同的含义；同一个距离可能对应多种内部形状，解释某个低谷时还需要查看其中的分子结构。

## 一条十残基短肽，连接了怎样的科学问题

伞形采样的思想可以追溯到Torrie与Valleau在1977年的工作：有意采用更利于访问目标区域的采样分布，再通过统计权重恢复所需信息。偏置在这里承担的是分配观察机会的角色。到了1992年，Kumar及合作者发展了面向生物分子自由能计算的加权直方图分析方法WHAM，把多个相互重叠的记录联系起来。两项方法相互配合，一项改变模拟访问哪里，另一项解释改变访问方式后得到的数据如何组合。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s2)

图 1 · 1977年的伞形采样、1992年的WHAM与2004年的chignolin把采样方法、统计归并和生物分子问题联系起来。

分子的选择则来自另一个问题：多短的氨基酸序列能够形成有组织的折叠？Honda及合作者在2004年报道了chignolin，序列为GYDPETGTWG，由10个残基构成，实验结构呈β发夹形。发夹图像指主链折返后形成两段相邻的伸展片段，中间通过转弯连接；这一折返形状由主链、侧链和水环境中的相互作用共同维持。这样的小体系保留了折叠、回折和内部接触的复杂性，同时便于我们逐个识别残基和定义端距。

结构条目1UAO来自溶液核磁共振研究，保存了18个提交构象。本例取其中第一个模型作为起点。这18个构象表达结构测定中的模型集合，排列顺序没有时间含义；实际时间演化由接下来的动力学记录给出。图中用十个Cα位置勾出主链走向，首尾之间的虚线定义所选距离。相邻Cα之间还隔着其他主链原子，因此连接线帮助阅读整体形状，实际化学键与角度仍由完整拓扑描述。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s2)

图 2 · 原始模型1的Cα位置经过主成分正交投影。编号为残基号，Cα连线表示主链走向，相邻Cα之间还有其他原子；模型顺序没有时间含义。

用两个Cα原子定义端距式 2

![用两个Cα原子定义端距](https://ml-biomat.com/static/agent-math/f428f40e44da901dc2e5d976.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ξ | 端距，一个非负长度 | nm |
| r₁, r₁₀ | Gly1与Gly10的Cα位置向量；下标为残基号 | nm |
| Δr; Δx, Δy, Δz | 最小镜像位移及其三个正交分量 | nm |
| ‖Δr‖ | 位移向量的模 | nm |
| √ | 开平方运算，本式把nm²转为nm | 1 |
| (Δx)², (Δy)², (Δz)² | 三个分量的平方；上标2为自乘 | nm² |
| min.image | 在周期映像间取定义明确的最近位移 | 1 |
| =, +, −, ( ) | 相等、相加、相减和分组 | 1 |

怎样理解三个正交方向满足勾股关系。周期边界先修正位移，再计算长度。每组只有一个原子，组质心就是该原子。

算一个例子最小镜像位移为(0.3, 0.4, 0) nm时，端距为0.5 nm。

使用条件检查实际盒尺寸，确保所采距离与最近映像定义相容；这个标量保留端距信息。

选择反应坐标，也是在选择压缩信息的方法。一幅完整构象包含数万原子的坐标，端距却只留下一个数。同一端距下的形状如果能在观察时间内充分交换，沿端距归并数据就能较好地描述这一维度的统计；如果某种侧链排布长时间保留，端距已经反复涨落，内部结构却仍在缓慢变化。因此，每个窗口除了保存距离和偏置力，也保存结构轨迹，便于把曲线上的某一段重新对应到分子的实际形状。

水也参与决定不同距离的相对概率。短肽伸展时，原先彼此接触的部分可能开始与水接触，附近水分子的取向和排列随之改变。因而这里汇总的是整个含水体系在指定端距下能够采取的构象，而不只是短肽内部的势能。若只把两幅构象的肽内能量相减，会遗漏溶剂重排和构象数量的影响。把水显式放进模型，再在统计中围绕短肽端距汇总，正是将这些环境效应纳入自由能描述的一种方式。

模型采用CHARMM36m蛋白参数及该参数包中的CHARMM TIP3P水。N端带正电，C端带负电，Asp3和Glu5侧链各带一个负电荷，整条肽净电荷为−2，因此加入两个钠离子中和。最终体系含138个肽原子、9276个水分子和两个钠离子，共27968个原子。原结构中的氢由pdb2gmx按当前力场重新生成，使名称与端基定义一致。水模型中的氢位点还带有CHARMM定义的Lennard–Jones参数，选择水时应连同具体参数文件一起确认。

初始周期盒为6.6 nm的立方体，为接近3 nm的端距留出空间。端距按三维最小镜像距离定义，因此使用过程中需要关注实际盒长与端距的关系，使所选两端的最近周期映像保持明确。我们用Gly1和Gly10各一个Cα作为两组，每组只含一个原子，所以组的质量中心就是该原子的位置。这个选择测量主链首尾的伸展程度；若要区分两个端距相近但折叠方式不同的构象，还可以进一步加入主链氢键、侧链接触或转角等结构量。

## 虚拟弹簧怎样改变分子的访问机会

伞形窗口可以想成一个轻轻扶住某个距离范围的弹簧。分子的真实相互作用仍然存在，我们额外增加一项随端距偏离中心而升高的能量：偏离越远，回复力越大。弹簧中心指定希望多观察的区域，弹簧常数决定限制有多紧。偏置作用于两个选定原子定义的距离；GROMACS根据这项距离能量，将回复力分配给两端原子，其余原子再通过原本的相互作用响应。

偏置能量、恢复力与移动中心式 3

![偏置能量、恢复力与移动中心](https://ml-biomat.com/static/agent-math/137bedfae3ecbb0efbaf3777.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i | 窗口编号 | 1 |
| Uᵢ | 该窗口的谐和偏置能量 | kJ/mol |
| ξ, ξᵢ, ξᵢ(0) | 实际端距、当前中心、初始中心 | nm |
| kᵢ | 弹簧常数；固定窗1000，移动阶段2000 | kJ mol⁻¹ nm⁻² |
| Fᵢ | 沿增大端距方向定义的偏置力；为负时使端距缩小 | kJ mol⁻¹ nm⁻¹ |
| v, t | 中心移动速度与经过时间 | nm/ps; ps |
| (ξ−ξᵢ)² | 位移的平方 | nm² |
| 1/2, ² | 数值系数；平方指数 | 1 |
| =, −, +, ( ) | 相等、取负或相减、相加、分组；相邻量相乘 | 1 |

怎样理解力随位移从零线性增加，克服回复力所做的功是力的大小—位移图上的三角形面积，因此能量有1/2系数。力是能量对端距导数的负值，指向中心。

算一个例子固定窗k=1000、ξ−ξi=0.05 nm时，U=1.25 kJ/mol，F=−50 kJ mol⁻¹ nm⁻¹。移动阶段v=0.005 nm/ps，100 ps后中心增加0.5 nm。

使用条件固定窗v=0仍有恢复力。移动偏置改变构象访问过程，窗口统计再用于平衡重加权。

本节固定窗口的弹簧常数为1000 kJ mol⁻¹ nm⁻²。端距偏离中心0.05 nm时，偏置能为1.25 kJ/mol，回复力大小为50 kJ mol⁻¹ nm⁻¹；距离偏差加倍，力加倍，能量则变为四倍。力的正负表示它沿距离增大的方向还是减小的方向作用。例如端距小于中心时，偏置倾向于把两端分开；端距大于中心时，它倾向于将两端拉近。读取输出力时，必须把符号约定与所定义的坐标一起看。

移动弹簧和固定弹簧使用同一种能量形式，区别在中心是否随时间变化。生成初始构象时，中心从起始端距出发，每皮秒增加0.005 nm，弹簧常数为2000；这个外部驱动使短肽逐渐伸展。正式窗口中，中心固定为0.5、0.6等指定值，移动速率设为零，弹簧常数改为1000。速率为零意味着中心不再移动，回复力仍随瞬时端距变化。即使固定窗口的平均端距偏离中心，也可能是分子自身的构象偏好在与弹簧共同作用。

弹簧应多紧，可以先做一个温度尺度上的估算。若原有自由能在很小的距离范围内近似平坦，只剩谐和偏置控制距离分布，那么分布宽度约为RT除以弹簧常数后再开方。在298 K与本例弹簧常数下，宽度约0.0498 nm。这个估算帮助理解为什么过强的弹簧会使窗口太窄、相邻记录难以重叠；实际短肽还有内部自由能变化，其分布可以偏移、变宽或出现不对称，需要从运行记录中检查。

弹簧的热宽度参照式 4

![弹簧的热宽度参照](https://ml-biomat.com/static/agent-math/251c05489e28f289a6b3d3a7.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| ξ, ξᵢ | 当前端距与弹簧中心 | nm |
| σξ | 谐和偏置下端距分布的标准差参照 | nm |
| R, T | 摩尔气体常数与绝对温度 | kJ mol⁻¹ K⁻¹; K |
| k | 弹簧常数 | kJ mol⁻¹ nm⁻² |
| RT/k | 热能与刚度之比，量纲为长度平方 | nm² |
| √, ≃, / | 开平方、近似相等、相除；RT表示乘积 | 1 |

怎样理解局部原自由能近似平坦时，指数权重exp[−k(ξ−ξi)²/(2RT)]与高斯分布的指数形式对应。

算一个例子298 K、k=1000时σξ约0.04978 nm；刚度增加四倍，参照宽度减半。

使用条件分子的真实自由能坡度和曲率会改变均值与宽度；实际覆盖由轨迹直方图给出。

力的单位也可以和熟悉的机械实验联系起来。1 kJ mol⁻¹ nm⁻¹约等于1.66054 pN，因此50 kJ mol⁻¹ nm⁻¹对应约83.0 pN。这个换算把每摩尔能量单位还原到单个分子上的力，便于与分子尺度的受力问题比较。偏置力在模拟中通过能量函数施加，实际端距仍受分子内部和水环境的共同影响。移动弹簧下的力随拉伸速度与构象历史变化，若要研究接近可逆的受力响应，就需要围绕速度、松弛和重复性另行设计记录。

[Figure: 谐和偏置能量与热宽度参照](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s3)

左图为谐和偏置能量，右图为局部原自由能平坦时的峰值归一化概率参照。黑点表示当前位移，宽度按输入温度与刚度计算。

交互图展示谐和偏置的能量、回复力和这个局部平坦条件下的参考宽度。把距离偏差设为零，能量和回复力都归零；把偏差改成相反数，能量不变，力的方向反转；增大弹簧常数，则同样偏差对应更强的力，同时参考宽度缩小。理解这几个关系后，选择窗口间隔就有了物理依据。它还说明了一个常见现象：窗口中心按相同间隔排列，真正采样到的距离分布却可能并不均匀，因为分子本身的自由能地形也参与决定访问概率。

## 从初始结构生成二十六个观察窗口

先把短肽放入水中，让整个体系在目标条件下准备。本例使用100 ps受限NVT和100 ps受限NPT，温度298 K、压力1 bar，随后去掉位置限制进入500 ps的移动弹簧阶段。含氢共价键采用约束，积分步长2 fs；静电采用PME，Lennard–Jones力在1.0至1.2 nm之间切换。完整设置写在下面的生成程序中，读者可以逐行找到控制温度、压力、输出间隔和弹簧参数的字段，而不需要在几份分散的配置说明之间来回查找。

### 下载并核对指定参数包

```
"""Download the specified official CHARMM GROMACS parameter archive."""
from pathlib import Path
import argparse,hashlib,tarfile,urllib.request

URL='https://mackerell.umaryland.edu/download.php?filename=CHARMM_ff_params_files%2Fcharmm36-jul2022.ff.tgz'
SHA256='9f31db8502852bc8fcf36497c27db14f1b6509b33701e7cafc2187840b7d2f09'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('.'))
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    archive=args.out/'charmm36-jul2022.ff.tgz'
    if not archive.exists():
        request=urllib.request.Request(URL,headers={'User-Agent':'MD-course-parameter-download'})
        with urllib.request.urlopen(request,timeout=120) as response:
            archive.write_bytes(response.read())
    actual=hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual!=SHA256:raise ValueError('The archive differs from the specified parameter release')
    with tarfile.open(archive) as handle:
        handle.extractall(args.out,filter='data')
    if not (args.out/'charmm36-jul2022.ff/forcefield.itp').is_file():
        raise ValueError('Expected GROMACS force-field directory missing')
    print('Official CHARMM July 2022 GROMACS parameter archive verified and extracted')
```

直接访问参数维护者的下载地址，核对归档哈希后解压。

### 按身份建立两个端点组

```
from pathlib import Path
s=Path('ions.gro').read_text().splitlines();n=int(s[1]);groups={}
for i,line in enumerate(s[2:2+n],1):
    resid=int(line[:5]);resname=line[5:10].strip();name=line[10:15].strip()
    if resid in (1,10) and name=='CA':
        assert resname=='GLY'
        groups[f'Gly{resid}_CA']=i
assert groups=={'Gly1_CA':5,'Gly10_CA':133}
all_atoms='\n'.join(' '.join(str(i) for i in range(start,min(start+15,n+1))) for start in range(1,n+1,15))
Path('index.ndx').write_text('[ System ]\n'+all_atoms+'\n'+''.join(f'[ {k} ]\n{v}\n' for k,v in groups.items()))
```

核对Gly1、Gly10及其Cα原子，再写入组编号。

### 完整生成准备、牵引和采样参数

```
"""Write complete inputs for chignolin pulling, 26 umbrellas, and two bridge trials."""
from pathlib import Path
import argparse

BASE = {
'ions.mdp': """integrator = steep
emtol = 1000.0
emstep = 0.01
nsteps = 50000
nstlist = 1
cutoff-scheme = Verlet
coulombtype = cutoff
rcoulomb = 1.2
rvdw = 1.2
pbc = xyz
""",
'em.mdp': """integrator = steep
emtol = 250
emstep = 0.001
nsteps = 10000
nstlist = 1
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
vdw-modifier = force-switch
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
pbc = xyz
define = -DFLEXIBLE
constraints = none
""",
'nvt.mdp': """define = -DPOSRES
integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = no
pbc = xyz
gen-vel = yes
gen-temp = 298
gen-seed = 20261700
nstfout = 0
nstxout-compressed = 500
ld-seed = 20261701
""",
'npt.mdp': """define = -DPOSRES
integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
refcoord-scaling = com
pbc = xyz
gen-vel = no
nstfout = 0
nstxout-compressed = 500
ld-seed = 20261702
""",
'pull.mdp': """integrator = md
nsteps = 250000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = yes
pull-coord1-rate = 0.005
pull-coord1-k = 2000
nstfout = 0
ld-seed = 20261703
pull-nstxout = 500
pull-nstfout = 500
""",
}


UMBRELLA = """integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.5
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20261900
pull-nstxout = 50
pull-nstfout = 50
"""

EQUILIBRATION = """integrator = md
nsteps = 10000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = yes
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.5
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20261850
pull-nstxout = 50
pull-nstfout = 50
gen-temp = 298
gen-seed = 20261800
"""

BRIDGE_EQ = """integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 2500
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = yes
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.65
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20267101
pull-nstxout = 50
pull-nstfout = 50
gen-temp = 298
gen-seed = 20267301
"""

BRIDGE_US = """integrator = md
nsteps = 250000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 2500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.65
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20267201
pull-nstxout = 50
pull-nstfout = 50
"""

def replace_values(template, updates):
    rows=[]
    for line in template.splitlines():
        if '=' in line:
            key=line.split('=',1)[0].strip()
            if key in updates:line=f'{key} = {updates[key]}'
        rows.append(line)
    return '\n'.join(rows)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=Path('.'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for name,content in BASE.items():(a.out/name).write_text(content,encoding='utf8',newline='\n')
    for i in range(26):
        center=round(.5+.1*i,1)
        us=replace_values(UMBRELLA,{'pull-coord1-init':center,'ld-seed':20261900+i})
        eq=replace_values(EQUILIBRATION,{'pull-coord1-init':center,'gen-seed':20261800+i,'ld-seed':20261850+i})
        (a.out/f'us{i}.mdp').write_text(us,encoding='utf8',newline='\n');(a.out/f'eq{i}.mdp').write_text(eq,encoding='utf8',newline='\n')
    for letter,delta in [('a',0),('b',1)]:
        d=a.out/f'bridge-{letter}';d.mkdir(exist_ok=True)
        eq=replace_values(BRIDGE_EQ,{'gen-seed':20267301+delta,'ld-seed':20267101+delta})
        us=replace_values(BRIDGE_US,{'ld-seed':20267201+delta})
        (d/'eq.mdp').write_text(eq,encoding='utf8',newline='\n');(d/'us.mdp').write_text(us,encoding='utf8',newline='\n')

if __name__=='__main__':main()
```

在同一处列出61份MDP的完整模板和逐窗随机种子。

### 从结构到双语图的完整运行入口

```
#!/usr/bin/env bash
set -euo pipefail
py=${PYTHON:-python3}
root=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$root/work/original"
for name in chignolin.pdb build_index.py select_windows.py run.sh; do
  cp "$root/$name" "$root/work/original/$name"
done
(cd "$root/work/original" && "$py" "$root/fetch_forcefield.py")
"$py" "$root/write_parameters.py" --out "$root/work/original"
(cd "$root/work/original" && bash run.sh)
"$py" "$root/prepare_bridges.py" --original "$root/work/original" --out "$root/work"
for letter in a b; do
  (cd "$root/work/bridge-$letter" && bash run.sh)
done
"$py" "$root/run_wham.py" --original "$root/work/original" --bridge-a "$root/work/bridge-a" --bridge-b "$root/work/bridge-b" --out "$root/work/wham"
for language in zh en; do
  "$py" "$root/analyze_umbrella.py" --original "$root/work/original" --bridge-a "$root/work/bridge-a" --bridge-b "$root/work/bridge-b" --wham "$root/work/wham" --out "$root/work/results-$language" --language "$language"
done
```

在配置好的GROMACS与分析环境中执行bash start.sh；脚本依次运行26窗和两个桥接试验，再进行六组WHAM与双语分析。

参数准备程序生成共同准备、移动弹簧、26组窗口准备和记录，以及两组后续桥接窗的完整MDP。固定窗口使用pull-coord1-start=no，表示弹簧中心由init字段直接指定；移动弹簧则使用起始距离作为初始中心。窗口坐标可能来自端距0.598 nm的一帧，而我们仍把中心明确设为0.600 nm。坐标值和弹簧中心属于不同对象，分开定义才能让各窗口的目标位置保持清楚，也让WHAM从TPR中读到正确的偏置信息。

### 运行原始26窗流程

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
py=${PYTHON:-python3}
"$gmx" pdb2gmx -f chignolin.pdb -o processed.gro -p topol.top -ff charmm36-jul2022 -water tip3p -ignh > pdb2gmx.log 2>&1
"$gmx" editconf -f processed.gro -o boxed.gro -box 6.6 6.6 6.6 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro > solvate.log 2>&1
"$gmx" grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'SOL\n' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname SOD -nname CLA -neutral -seed 20261700 > genion.log 2>&1
"$py" build_index.py
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr > npt.grompp.log 2>&1
"$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 2 -pin off > npt.stdout.log 2>&1
"$gmx" grompp -f pull.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o pull.tpr > pull.grompp.log 2>&1
"$gmx" mdrun -deffnm pull -ntmpi 1 -ntomp 2 -pin off > pull.stdout.log 2>&1
"$py" select_windows.py
for i in $(seq 0 25); do
  win=$(printf '%02d' "$i")
  "$gmx" grompp -f "eq$i.mdp" -c "window-$win.gro" -p topol.top -n index.ndx -o "eq$i.tpr" > "eq$i.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "eq$i" -ntmpi 1 -ntomp 2 -pin off > "eq$i.stdout.log" 2>&1
  "$gmx" grompp -f "us$i.mdp" -c "eq$i.gro" -t "eq$i.cpt" -p topol.top -n index.ndx -o "us$i.tpr" > "us$i.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "us$i" -ntmpi 1 -ntomp 2 -pin off > "us$i.stdout.log" 2>&1
done
for i in $(seq 0 25); do printf 'us%s.tpr\n' "$i"; done > tpr-files.dat
for i in $(seq 0 25); do printf 'us%s_pullf.xvg\n' "$i"; done > pullf-files.dat
"$gmx" wham -it tpr-files.dat -if pullf-files.dat -o pmf.xvg -hist histograms.xvg -temp 298 -b 0 -bins 150 > wham.log 2>&1
```

按最小化、NVT、NPT、牵引、选帧与各窗准备/记录依次运行。

移动偏置下的端距曲线总体向上，但在每个时刻都有热涨落，也会落后于移动的中心。沿着这条记录，我们为每个目标中心寻找实际端距最接近的保存帧，再提取完整体系坐标。这个过程相当于从一段连续伸展录像中挑出一组候选起点，端距相近只是挑选条件，后续窗口还要进行自己的准备。拉伸图中的点显示了所选择的帧，虚线显示中心的运动，二者之间的差异直接体现有限刚度的弹簧与分子响应。

### 牵引记录与起始帧

500 ps牵引的实际端距、移动中心与选出的26帧。

Chignolin十残基肽、CHARMM36 July 2022及TIP3P水；298 K、1 bar、2 fs步长。原26个中心0.5–3.0 nm、间隔0.1 nm的窗口各生产100 ps；两个0.65 nm桥接窗分别从0.60与0.70 nm窗末态开始，各生产500 ps。固定窗弹簧常数1000 kJ mol⁻¹ nm⁻²。

[下载参考数据与完整输入（ZIP） 19.37 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-chignolin-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s4)

实际牵引阶段的端距、以0.005 nm/ps移动的偏置中心，以及为26个固定窗口选取的真实起始帧。牵引产生构象序列，固定中心下的记录用于后续统计。

### 从实际牵引记录选择起始帧

```
from pathlib import Path
import json,os,subprocess
import numpy as np
rows=np.loadtxt([s for s in Path('pull_pullx.xvg').read_text().splitlines() if s and s[0] not in '#@'])
assert rows.shape[1]==2 and np.isfinite(rows).all()
gmx=os.environ.get('GMX','gmx');report=[]
for i in range(26):
    center=.5+.1*i;j=int(np.argmin(abs(rows[:,1]-center)));t=float(rows[j,0]);actual=float(rows[j,1])
    assert abs(actual-center)<.08,(center,actual)
    with open(f'window-{i:02d}-extract.log','w') as log:
        subprocess.run([gmx,'trjconv','-s','pull.tpr','-f','pull.xtc','-dump',str(t),'-o',f'window-{i:02d}.gro'],input='System\n',text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
    report.append(dict(index=i,center_nm=center,selected_time_ps=t,saved_distance_nm=actual))
Path('window-selection.json').write_text(json.dumps(report,indent=2))
```

查找各中心最近的已保存端距，并抽取相应完整坐标。

每个固定窗口从选出的构象重新生成速度，先在自身偏置下准备20 ps，再记录100 ps。26个中心覆盖0.5至3.0 nm，间隔0.1 nm。坐标和偏置力每0.1 ps输出一次，因此每个窗口有1001条距离与力记录。结构轨迹的保存间隔另为1 ps，选择初始窗口时使用的移动偏置记录也与其保存帧时间对应。将积分步长、结构保存间隔和标量输出间隔分别说明，才能知道一列时间序列中的每一行究竟来自哪一次记录。

执行脚本把拓扑、索引和MDP组合为TPR，再运行各个阶段。索引文件中的两组原子身份是Gly1的Cα与Gly10的Cα，实际原子序号为5和133；这些编号来自当前拓扑，程序按残基与原子名查找后写出。下载的力场档会先核对固定版本的散列值，既有准备文件与本例相匹配。对于窗口统计，1001行数据中的相邻记录通常相关，记录行数说明保存了多少次观察，独立统计信息还需要结合时间相关和重复模拟判断。

## 相邻窗口是否真的看到了共同的区域

窗口中心排成一列，并不自动意味着数据已经连成一条通路。我们把每个窗口的端距分成相同的0.01 nm小格，统计每格所占的记录比例，再并排查看分布。图中每一行对应一个弹簧中心，亮的地方表示实际端距经常落在那里，虚线则是“实际端距等于中心”的位置。许多记录偏在虚线一侧，说明分子自身的构象偏好使平均端距与输入中心不同。分析时应以这些实际分布判断衔接，而不是只看输入文件里的中心列表。

### 原始窗口与桥接区域

共同0.01 nm区间；各分布按自身记录数归一化。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s5)

左图为26个原窗的实测端距分布，每窗单独归一；虚线为设定中心，圆点为实际平均端距。右图放大0.60、0.70 nm原窗及两个0.65 nm桥接窗，使用共同0.01 nm箱宽。

本例中心0.6 nm的窗口平均端距约0.5181 nm，中心0.7 nm的窗口约0.6509 nm，两者之间的分布衔接较弱。用每个格子中两组概率的较小者相加，可以量化它们共有多少统计覆盖：完全相同的两个分布得1，没有共同格子得0。对这对窗口，重叠系数为0.04296。这个数直接说明按当前格宽观察到的共同区域较少，帮助我们把新增计算集中到一个具体位置，而不是平均延长所有窗口。

量化两个窗口共享的覆盖式 5

![量化两个窗口共享的覆盖](https://ml-biomat.com/static/agent-math/0e466cca6e003d8ce6aede08.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i, j, b | 两个窗口编号与共同区间编号 | 1 |
| Hᵢb, nᵢ | 窗口i在区间b的计数及其总计数 | count |
| Pᵢb, Pⱼb | 两个窗口落入同一区间的概率 | 1 |
| Oᵢⱼ | 重叠系数，介于0和1之间 | 1 |
| Σb, min | 对全部区间求和；逐区间取两概率较小值 | 1 |
| =, /, ( ), , | 相等、相除、分组；逗号分隔函数参数 | 1 |

怎样理解逐区间较小的概率是两份分布共同拥有的部分，加总后得到共享概率。

算一个例子两区间概率分别为(0.7,0.3)与(0.2,0.8)，重叠为0.2+0.3=0.5。

使用条件本例所有分布用共同0.01 nm区间且覆盖全部观测；此量描述端距投影上的重叠。

重叠系数依赖所用的格子，也依赖实际采样长度，因此比较时应统一分箱并保存定义。格子过细会让短记录显得零碎，过粗则可能把本来分开的区域并到一起。本节0.01 nm的格宽小于弹簧给出的约0.05 nm参考宽度，便于看清这对窗口的细部。它给出的是投影到端距上的覆盖程度；即使两条记录拥有相近端距，内部转角或侧链接触也可能停留在不同状态，还需要结合构象或不同起点的记录继续检查。

原26个窗口的结果提供了一个很有价值的诊断例子：相同的弹簧常数和中心间隔，在某些区域工作得比较顺畅，在另一些区域则需要更密的观察。原因可能与局部自由能斜率、构象转换和慢变量有关。处理方式可以是增加一个中间中心、改变限制强度，或者延长相关区域的采样。本节选择最直接的一项：在0.65 nm增加窗口，并分别从两侧已有构象开始，使我们同时观察“补上距离空隙”和“起始构象是否仍有影响”这两个问题。

后面的WHAM会按照各窗口的偏置重新加权，重叠区为不同窗口之间的相对归一化提供联系。可以把它想成两张拍摄同一景物的照片，共同出现的部分帮助确定它们如何拼接；如果只在边缘看见很少的共同内容，拼接就容易受到局部噪声影响。这里的照片类比只说明统计衔接，真正组合时要用已知弹簧能量修正不同位置被偏爱的程度。原始计数、偏置定义和共同区域三者一起决定了分析的基础。

## 同一个中心，从两种构象开始

桥接窗A取原0.6 nm窗口的末态，桥接窗B取原0.7 nm窗口的末态，两者的弹簧中心都设为0.65 nm，弹簧常数都为1000。每组重新生成速度，在该偏置下准备100 ps，再记录500 ps。这样既增加了中间区域的观察，也保留了两种起始构象的身份。准备脚本把原体系的拓扑、索引和对应末态复制到独立目录，写出各自的种子与运行设置；后续计算可以分别进行，分析时再按清楚的标签组合。

### 生成两种起点的桥接试验

```
"""Prepare the two 0.65 nm windows from the 0.6 and 0.7 nm final states."""
from pathlib import Path
import argparse,shutil
from write_parameters import BRIDGE_EQ,BRIDGE_US,replace_values

RUN='''#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f eq.mdp -c start.gro -p topol.top -n index.ndx -o eq.tpr > eq.grompp.log 2>&1
"$gmx" mdrun -deffnm eq -ntmpi 1 -ntomp 2 -pin off > eq.stdout.log 2>&1
"$gmx" grompp -f us.mdp -c eq.gro -t eq.cpt -p topol.top -n index.ndx -o us.tpr > us.grompp.log 2>&1
"$gmx" mdrun -deffnm us -ntmpi 1 -ntomp 2 -pin off > us.stdout.log 2>&1
'''

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('original'))
    parser.add_argument('--out',type=Path,default=Path('.'))
    args=parser.parse_args()
    for letter,index,delta in [('a',1,0),('b',2,1)]:
        folder=args.out/f'bridge-{letter}';folder.mkdir(parents=True,exist_ok=True)
        for name in ['topol.top','posre.itp','index.ndx']:
            shutil.copy2(args.original/name,folder/name)
        shutil.copytree(args.original/'charmm36-jul2022.ff',folder/'charmm36-jul2022.ff',dirs_exist_ok=True)
        shutil.copy2(args.original/f'us{index}.gro',folder/'start.gro')
        eq=replace_values(BRIDGE_EQ,{'gen-seed':20267301+delta,'ld-seed':20267101+delta})
        us=replace_values(BRIDGE_US,{'ld-seed':20267201+delta})
        (folder/'eq.mdp').write_text(eq,encoding='utf8',newline='\n')
        (folder/'us.mdp').write_text(us,encoding='utf8',newline='\n')
        (folder/'run.sh').write_text(RUN,encoding='utf8',newline='\n')
    print('Run bash run.sh separately inside bridge-a and bridge-b')
```

分别从0.6和0.7 nm窗末态建立0.65 nm偏置试验。

两条桥接记录各有5001个距离样本。A的平均端距约0.55005 nm，B约0.58478 nm，虽然中心完全相同，平均位置仍有差别。时间曲线进一步显示，B在部分时段访问较大的端距，随后又回到较小值附近；A也有波动，但各时段占据区域的比例不同。弹簧没有强迫两组记录变成相同的轨迹，它只是提供同一个距离偏置。不同初态和有限记录长度留下的差异，需要从这些实际访问历史中理解。

### 相同偏置下的两种历史

每条桥接轨迹500 ps，分段均值按各自250 ps边界计算。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s6)

两个共同中心0.65 nm的桥接窗各500 ps实际记录，起始构象来自不同方向。下图分别比较各窗前250 ps和后250 ps的平均端距，保留起始历史及时间变化的信息。

把每条桥接记录在250 ps处分成两段，A前后平均端距分别为0.56049与0.53961 nm；B分别为0.58331与0.58624 nm。A在这段记录中向较小端距变化，B两个半段均值接近，但曲线内部仍有持续的高低区域。单独比较两个半段均值有助于发现明显变化，完整时间曲线则保留停留与跃迁的信息。对于涉及不同内部构象的慢变化，端距均值接近也需要结合其他结构量，才能判断两段是否采样了相近的构象集合。

新增记录确实改善了端距上的衔接。将A与B的归一化分布等权组合后，它与原0.6 nm窗口的重叠为0.56125，与0.7 nm窗口的重叠为0.36203；A和B之间的重叠为0.76025。相比原两窗之间0.04296的数值，中间区域获得了更充分的共同覆盖。同时，两种历史的均值和时间分布还存在差异。把这两方面同时保留下来，可以清楚说明新增计算解决了哪一个采样问题，以及下一轮观察还应关注什么。

桥接窗的500 ps比原窗口的100 ps更长，因此在实际WHAM输入中提供了更多记录。这里各窗口沿用相同0.1 ps的标量保存间隔，组合程序使用原生记录计数，没有额外启用自相关权重修正。统计解释要与这一操作一致：更多保存点可以改善直方图分辨率，其独立信息量仍取决于相关时间。下一轮若需要报告可靠的不确定度，应比较多个准备历史和更长的记录，并检查端距以外的结构变化，避免把一串相关的观察当成许多独立实验。

## 去掉偏置后，怎样把窗口拼成自由能剖面

带弹簧的窗口偏爱中心附近的距离，因此各窗原始直方图不能直接相加当成自然分布。WHAM利用已知偏置，把某个距离在每个窗口中被促进或抑制的程度纳入权重，同时求出窗口之间的归一化关系。直观地说，某个格子在偏置很不利的条件下仍经常出现，会提供不同于“偏置本来就鼓励到这里”的信息。多个重叠窗口共同约束这种比较，使我们能够恢复同一坐标上的相对概率。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s7)

图 3 · 计数和偏置已知，共同概率与每窗归一化相互依赖。矩阵与曲线为这一统计关系的概念示意。

WHAM共同求解概率与窗口归一化式 6

![WHAM共同求解概率与窗口归一化](https://ml-biomat.com/static/agent-math/9f7b43ced8f3d517d7607f72.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| i, b | 窗口编号与共同区间编号 | 1 |
| p_{b} | 无偏分布在区间b的概率质量；除以区间宽度后为密度 | 1 |
| Hᵢb, nᵢ | 窗口i在区间b的原始计数与总观测数 | count |
| wᵢb | 窗口i在区间b的已知偏置能量 | kJ/mol |
| fᵢ | 窗口归一化自由能偏移，由右侧方程自洽求得 | kJ/mol |
| R, T | 摩尔气体常数；共同绝对温度 | kJ mol⁻¹ K⁻¹; K |
| (fᵢ−wᵢb)/(RT), −fᵢ/(RT), −wᵢb/(RT) | 能量除以热能，得到无量纲指数 | 1 |
| exp | 自然指数函数，以e为底 | 1 |
| Σi, Σb | 对窗口或区间求和 | 1 |
| =, −, /, [ ], ( ), 1 | 相等、相减或取负、相除、分组；1为归一化概率总和，邻接表示乘积 | 1 |

怎样理解各窗口的已知偏置改变不同区间的访问机会；共同概率与每窗归一化互相依赖，迭代使所有窗口满足同一统计描述。

算一个例子一个零偏置窗口在两个区间计数2和3时，p=(0.4,0.6)，归一化f=0。多个谐和窗口则需求解位置相关权重。

使用条件此式对应共同温度、共同区间和原始计数权重；当前原生分析未加自相关修正。方程收敛与构象采样充分程度分别检查。

先考虑一个容易算清的极限情形：只有一个窗口，两个区间的偏置能量都为零，计数分别为2和3。那么恢复的概率就是0.4和0.6，归一化不需要按距离额外补偿。换成谐和偏置后，不同距离承受的偏置能量不同，每个区间需要不同权重；再加入多个窗口，还要让它们校正后的结果共同描述一份概率分布。这个计数例子把公式中的未知量与日常的频率统计联系起来。

直方图的每个格子只保存端距计数，它把同一窗口内的时间顺序压缩掉了。因此WHAM分析之前保留时间曲线十分有用：两段记录可以得到相似的总体计数，却由不同的长时间停留过程组成。分段比较和不同起点的桥接记录，让我们重新看到被直方图压缩掉的历史信息。后续若加入统计误差估计，也应让重采样单位与这些时间相关相适应，例如以足够长的片段或独立模拟为单位，而不是直接把每个保存点都当成独立抽样。

公式中的未知量相互依赖：格子的无偏概率需要窗口归一化常数，归一化常数又依赖当前的概率估计。程序从一组初值开始反复更新，直到相邻两次迭代变化小于设定阈值。这里设置阈值为10⁻⁷，它约束的是数值求解的停止条件。轨迹是否已经充分访问相关构象，则由采样历史、窗口重叠和独立记录决定。程序顺利停止，说明这组输入直方图对应的方程已经求解到指定精度；我们继续用时间分段比较评估输入统计本身的变化。

下面的脚本生成六组匹配列表：原26窗、分别加入A或B、同时加入两桥的28窗，以及28窗各自的前半段和后半段。每行TPR都与同一窗口的偏置力文件对应，WHAM从TPR读取中心与弹簧常数，再由力记录还原相应距离信息。所有分析统一使用298 K、0.35至3.2 nm的150格网格。分半时，原窗口按50 ps分开，桥接窗按250 ps分开，各自依据本身的记录长度，保留这一统计定义才能正确比较。

### 组合完整与分段原生WHAM输入

```
"""Recompute six native WHAM profiles with matching grids and window lists."""
from pathlib import Path
import argparse,os,subprocess
import numpy as np


def read_xvg(path):
    return np.loadtxt([s for s in Path(path).read_text().splitlines() if s.strip() and not s.lstrip().startswith(('#','@'))])


def relative(path,folder):
    return os.path.relpath(path.resolve(),folder.resolve()).replace('\\','/')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('records/original'))
    parser.add_argument('--bridge-a',type=Path,default=Path('records/bridge-a'))
    parser.add_argument('--bridge-b',type=Path,default=Path('records/bridge-b'))
    parser.add_argument('--out',type=Path,default=Path('wham-recomputed'))
    parser.add_argument('--gmx',default=os.environ.get('GMX','gmx'))
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    datasets=[(f'original-{i:02d}',args.original/f'us{i}.tpr',args.original/f'us{i}_pullf.xvg',100) for i in range(26)]
    datasets += [(f'bridge-{letter}',folder/'us.tpr',folder/'us_pullf.xvg',500) for letter,folder in [('a',args.bridge_a),('b',args.bridge_b)]]
    configurations=[('original26',datasets[:26],None),('bridge-a27',datasets[:27],None),
                    ('bridge-b27',datasets[:26]+[datasets[27]],None),('both28',datasets,None),
                    ('both28-first-half',datasets,0),('both28-second-half',datasets,1)]
    for name,selected,half in configurations:
        folder=args.out/name;folder.mkdir(parents=True,exist_ok=True)
        tpr_lines=[];force_lines=[]
        for label,tpr,force,duration in selected:
            if not tpr.is_file() or not force.is_file():raise FileNotFoundError(label)
            tpr_lines.append(relative(tpr,folder))
            if half is not None:
                data=read_xvg(force)
                mask=data[:,0]<duration/2 if half==0 else data[:,0]>=duration/2
                selected_force=folder/(label+'-pullf.xvg')
                np.savetxt(selected_force,data[mask],fmt='%.8g')
            else:selected_force=force
            force_lines.append(relative(selected_force,folder))
        (folder/'tpr-files.dat').write_text('\n'.join(tpr_lines)+'\n',encoding='utf8',newline='\n')
        (folder/'pullf-files.dat').write_text('\n'.join(force_lines)+'\n',encoding='utf8',newline='\n')
        command=[args.gmx,'wham','-it','tpr-files.dat','-if','pullf-files.dat','-o','pmf.xvg','-hist','histograms.xvg',
                 '-b','0','-temp','298','-bins','150','-min','0.35','-max','3.2','-tol','1e-7']
        if not args.prepare_only:
            with (folder/'wham.log').open('wb') as log:
                subprocess.run(command,cwd=folder,stdout=log,stderr=subprocess.STDOUT,check=True)
        print(name,'inputs prepared' if args.prepare_only else 'native WHAM completed')
```

逐行配对TPR与力文件，生成六组统一网格的原生分析。

自由能零点可以整体平移。为了比较六条曲线，我们把0.8至1.0 nm范围内各格的平均剖面值设为零，再观察其他区间相对于这一共同参照的位置。图中左侧放大桥接区域，可以看出两种桥接历史对短端距部分的影响；右侧比较同样28个窗口的完整记录与前后半段。两组半段在较宽距离范围内仍有差别，说明记录长度和内部构象访问对剖面具有实际影响。这个比较给出了后续延长采样的具体依据。

### 相对剖面与分段差异

六组原生WHAM；0.8–1.0 nm区间平均置零，无观测区间保留空白。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/#zh-s7)

原生GROMACS WHAM结果采用相同150格网格，并把0.8≤r<1.0 nm区间均值平移到零。左图比较加入不同桥接窗后的局部剖面，右图比较完整28窗及各窗前后半段。原生直方图无样本的格点不连线；阴影标出两个固定比较区间。

固定网格还包含一些没有样本的边缘格。原生输出文件在这些格子可能写入有限的占位数值，因此分析程序同时读取直方图，只在所有窗口合计计数大于零的格子上绘制剖面，空格保留为断段。这样图线表达的是有记录支撑的区间。接近最大端距的少数样本还会带来陡峭且敏感的尾部形状，读图时应结合计数分布。增加横坐标范围本身不会增加采样，真正扩大可解释区间，需要让模拟在新增区域积累足够的构象记录。

## 让一条曲线变成可以判断的研究结果

完整分析程序从28个实际距离记录和偏置力记录出发，核对时间点、样本数以及力与距离偏差的关系，再计算每窗均值、分段均值、直方图重叠和六条原生WHAM曲线。对于每个固定窗口，力记录应等于弹簧常数乘距离偏差再取负号；文本输出的有限小数位会留下很小的舍入差。把这项关系一起检查，可以发现窗口中心、文件配对或符号约定的错误，使后面图像中的每个数都能追溯到明确的输入记录。

### 完整分析重叠、历史和自由能变化

```
"""Analyze recorded chignolin windows and native GROMACS WHAM profiles."""
from pathlib import Path
import argparse,json,csv,logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)


def xvg(path):
    lines=Path(path).read_text(encoding='utf-8').splitlines()
    data=np.loadtxt([line for line in lines if line.strip() and not line.lstrip().startswith(('#','@'))])
    if data.ndim!=2 or data.shape[1]<2 or not np.isfinite(data).all():
        raise ValueError(f'Expected finite two-column XVG: {Path(path).name}')
    return data


def save(fig,path):
    fig.savefig(path.with_suffix('.svg'))
    fig.savefig(path.with_suffix('.png'),dpi=150)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('records/original'))
    parser.add_argument('--bridge-a',type=Path,default=Path('records/bridge-a'))
    parser.add_argument('--bridge-b',type=Path,default=Path('records/bridge-b'))
    parser.add_argument('--wham',type=Path,default=Path('records/wham'))
    parser.add_argument('--out',type=Path,default=Path('analysis'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh'
    fonts=['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans'] if zh else ['DejaVu Sans']
    plt.rcParams.update({'font.family':fonts,'font.size':14,'axes.titlesize':16,'axes.labelsize':15,'svg.fonttype':'path','axes.unicode_minus':False})
    datasets=[(f'original-{i:02d}',args.original/f'us{i}_pullx.xvg',args.original/f'us{i}_pullf.xvg',100,.5+.1*i) for i in range(26)]
    datasets += [(f'bridge-{letter}',folder/'us_pullx.xvg',folder/'us_pullf.xvg',500,.65) for letter,folder in [('a',args.bridge_a),('b',args.bridge_b)]]
    edges=np.arange(.3,3.3001,.01);mids=(edges[1:]+edges[:-1])/2;hist=[];raw=[];rows=[]
    for name,path,forcepath,duration,center in datasets:
        data=xvg(path);force=xvg(forcepath)
        if len(data)!=duration*10+1 or data[0,0]!=0 or data[-1,0]!=duration or not np.all(np.diff(data[:,0])>0):
            raise ValueError(f'Unexpected times or sample count: {name}')
        if force.shape!=data.shape or not np.array_equal(force[:,0],data[:,0]):
            raise ValueError('Coordinate and force records must share time points')
        values=data[:,1];counts=np.histogram(values,edges)[0]
        if counts.sum()!=len(values):raise ValueError('Histogram range excludes recorded samples')
        probabilities=counts/counts.sum();hist.append(probabilities);raw.append(data)
        # GROMACS scalar pull force is -k times displacement from the fixed center.
        residual=float(np.max(np.abs(force[:,1]+1000*(values-center))))
        if residual>.02:raise ValueError('Force/coordinate/spring relation differs from the recorded bias')
        rows.append({'name':name,'center_nm':center,'samples':len(values),'duration_ps':duration,
                     'mean_nm':float(values.mean()),'population_sd_nm':float(values.std()),
                     'first_half_mean_nm':float(values[data[:,0]<duration/2].mean()),
                     'second_half_mean_nm':float(values[data[:,0]>=duration/2].mean()),
                     'max_force_rounding_residual_kJ_mol_nm':residual})
    hist=np.asarray(hist);combined=(hist[26]+hist[27])/2
    overlap=lambda a,b:float(np.minimum(a,b).sum())
    overlaps={'old_0.6_vs_0.7':overlap(hist[1],hist[2]),'bridge_a_vs_b':overlap(hist[26],hist[27]),
              '0.6_vs_combined_bridge':overlap(hist[1],combined),'combined_bridge_vs_0.7':overlap(combined,hist[2])}
    configurations=['original26','bridge-a27','bridge-b27','both28','both28-first-half','both28-second-half']
    profiles={};profile_rows=[]
    for name in configurations:
        arr=xvg(args.wham/name/'pmf.xvg')
        if len(arr)!=150:raise ValueError('Expected 150 native WHAM bins')
        if profiles and not np.array_equal(arr[:,0],next(iter(profiles.values()))[:,0]):raise ValueError('WHAM grids differ')
        native_hist=xvg(args.wham/name/'histograms.xvg')
        if not np.array_equal(native_hist[:,0],arr[:,0]):raise ValueError('Native histogram and PMF grids differ')
        sampled=native_hist[:,1:].sum(axis=1)>0
        ref=(arr[:,0]>=.8)&(arr[:,0]<1.);target=(arr[:,0]>=2.4)&(arr[:,0]<2.6)
        if not sampled[ref|target].all():raise ValueError('Comparison interval contains unsampled bins')
        offset=float(arr[ref,1].mean());arr[:,1]-=offset;profiles[name]=arr
        profile_rows.append({'name':name,'reference_offset_kJ_mol':offset,'band_difference_kJ_mol':float(arr[target,1].mean()),
                             'sampled_bins':int(sampled.sum()),'unsampled_bins':int((~sampled).sum()),
                             'sampled_range_nm':[float(arr[sampled,0].min()),float(arr[sampled,0].max())]})
        # Native WHAM writes finite placeholders in empty bins; omit these from
        # interpreted profiles while retaining the unmodified native XVG inputs.
        arr[~sampled,1]=np.nan
        np.savetxt(args.out/(name+'-aligned.csv'),arr,delimiter=',',header='distance_nm,relative_profile_kJ_mol',comments='')
    pull=xvg(args.original/'pull_pullx.xvg');selected=[]
    for center in np.linspace(.5,3.,26):
        j=int(np.argmin(np.abs(pull[:,1]-center)))
        selected.append({'center_nm':float(center),'time_ps':float(pull[j,0]),'distance_nm':float(pull[j,1])})
    summary={'temperature_K':298,'spring_kJ_mol_nm2':1000,'histogram_bin_width_nm':.01,
             'windows':rows,'overlap_coefficients':overlaps,'native_profiles':profile_rows,
             'pulling_selected_frames':selected,
             'definitions':{'window_sd':'Population dispersion of all recorded coordinates; not standard error',
                            'half':'Time < duration/2 and time >= duration/2 for each window separately',
                            'profile_alignment':'Mean of bins with 0.8 <= distance < 1.0 nm set to zero',
                            'band_comparison':'Mean profile over 2.4 <= distance < 2.6 nm after alignment; a fixed band comparison',
                            'overlap':'Sum of minimum normalized bin probabilities on common 0.01 nm bins',
                            'empty_profile_bins':'Masked using zero total native histogram counts; original XVG remains unchanged'}}
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    with (args.out/'window-statistics.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    teal='#117f92';orange='#c56b3b';purple='#70629b';gray='#7f898e'
    fig,ax=plt.subplots(figsize=(11,5),constrained_layout=True)
    ax.plot(pull[:,0],pull[:,1],color=teal,label='记录端距' if zh else 'Recorded end distance')
    ax.plot(pull[:,0],pull[0,1]+.005*pull[:,0],ls='--',color=gray,label='移动弹簧中心' if zh else 'Moving spring center')
    ax.scatter([r['time_ps'] for r in selected],[r['distance_nm'] for r in selected],s=28,color=orange,zorder=4,label='26个窗口的初始帧' if zh else 'Initial frames for 26 windows')
    ax.set(xlabel='拉伸时间 / ps' if zh else 'Pulling time / ps',ylabel='端距 / nm' if zh else 'End distance / nm',title='移动偏置生成一组起始构象' if zh else 'A moving bias generates starting conformations')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.34),ncol=1,fontsize=12);ax.set_title(ax.get_title(),pad=88);ax.grid(alpha=.15);save(fig,args.out/'pulling-selection')
    fig,axs=plt.subplots(1,2,figsize=(13,6),constrained_layout=True)
    im=axs[0].imshow(hist[:26]/.01,origin='lower',aspect='auto',extent=[edges[0],edges[-1],.45,3.05],cmap='magma',interpolation='nearest')
    axs[0].plot([.5,3],[.5,3],'w--',lw=1.2,label='中心位置' if zh else 'Bias centers')
    axs[0].plot([r['mean_nm'] for r in rows[:26]],[r['center_nm'] for r in rows[:26]],'o',ms=3,color='#71d6e1',label='实际平均端距' if zh else 'Recorded mean distances')
    axs[0].set(xlabel='实际端距 / nm' if zh else 'Recorded distance / nm',ylabel='弹簧中心 / nm' if zh else 'Bias center / nm',title='26个原始窗口' if zh else 'The original 26 windows')
    legend=axs[0].legend(fontsize=11,loc='upper center',bbox_to_anchor=(.5,1.18));legend.legend_handles[0].set_color('#555555');axs[0].set_title(axs[0].get_title(),pad=75);fig.colorbar(im,ax=axs[0],label='概率密度 / nm⁻¹' if zh else 'Probability density / nm⁻¹',shrink=.8)
    for i,color,label in [(1,teal,'0.60 nm'),(2,orange,'0.70 nm'),(26,purple,'0.65 nm A'),(27,gray,'0.65 nm B')]:axs[1].plot(mids,hist[i]/.01,color=color,label=label)
    axs[1].set(xlim=(.4,.85),xlabel='实际端距 / nm' if zh else 'Recorded distance / nm',ylabel='概率密度 / nm⁻¹' if zh else 'Probability density / nm⁻¹',title='薄弱连接处与新增桥接窗' if zh else 'A weak connection and the bridge windows')
    axs[1].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.2),ncol=2);axs[1].set_title(axs[1].get_title(),pad=75);axs[1].grid(alpha=.15);save(fig,args.out/'window-overlap')
    fig,axs=plt.subplots(2,1,figsize=(11,8),constrained_layout=True)
    for index,color,label in [(26,teal,'A：从0.60 nm窗起步' if zh else 'A: start from the 0.60 nm window'),(27,orange,'B：从0.70 nm窗起步' if zh else 'B: start from the 0.70 nm window')]:
        a=raw[index];axs[0].plot(a[:,0],a[:,1],color=color,alpha=.65,lw=.7,label=label)
        for x0,x1,key in [(0,250,'first_half_mean_nm'),(250,500,'second_half_mean_nm')]:axs[1].plot([x0,x1],[rows[index][key]]*2,color=color,lw=3)
        axs[1].scatter([125,375],[rows[index]['first_half_mean_nm'],rows[index]['second_half_mean_nm']],color=color,s=40)
    axs[0].axhline(.65,color=gray,ls='--',label='共同偏置中心0.65 nm' if zh else 'Shared bias center 0.65 nm')
    axs[0].legend(loc='upper center',bbox_to_anchor=(.5,1.31),ncol=1,fontsize=12)
    axs[0].set(ylabel='瞬时端距 / nm' if zh else 'Instantaneous distance / nm')
    axs[1].set(ylabel='各半段平均端距 / nm' if zh else 'Mean distance\nin each half / nm')
    for ax in axs:ax.set_xlabel('桥接窗记录时间 / ps' if zh else 'Bridge production time / ps');ax.axvline(250,color='#bbb',ls=':');ax.grid(alpha=.15)
    save(fig,args.out/'bridge-history')
    fig,axs=plt.subplots(1,2,figsize=(13,6),constrained_layout=True)
    for name,color,label in [('original26',gray,'原26窗' if zh else 'Original 26'),('bridge-a27',teal,'加桥A' if zh else 'Add A'),('bridge-b27',orange,'加桥B' if zh else 'Add B'),('both28',purple,'加两桥' if zh else 'Add both')]:
        arr=profiles[name];axs[0].plot(arr[:,0],arr[:,1],color=color,label=label)
    for name,color,label in [('both28',purple,'完整记录' if zh else 'Complete records'),('both28-first-half',teal,'各窗前半段' if zh else 'First half of each window'),('both28-second-half',orange,'各窗后半段' if zh else 'Second half of each window')]:
        arr=profiles[name];axs[1].plot(arr[:,0],arr[:,1],color=color,label=label)
    for ax in axs:
        ax.axvspan(.8,1,color=teal,alpha=.10);ax.axvspan(2.4,2.6,color=orange,alpha=.12);ax.axhline(0,color='#bbb',lw=1)
        ax.set(xlabel='端距 / nm' if zh else 'End distance / nm',ylabel='相对自由能剖面 / kJ mol⁻¹' if zh else 'Relative free-energy profile / kJ mol⁻¹');ax.grid(alpha=.15)
    axs[0].set_xlim(.4,1.05)
    local=np.concatenate([a[(a[:,0]>=.4)&(a[:,0]<=1.05),1] for a in list(profiles.values())[:4]])
    axs[0].set_ylim(float(np.nanmin(local))-2,float(np.nanmax(local))+3)
    axs[0].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.29),ncol=2)
    axs[1].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.29),ncol=1)
    axs[0].set_title('桥接区域的相对剖面' if zh else 'Relative profiles in the bridge region',pad=100)
    axs[1].set_title('相同28窗的分段比较' if zh else 'Time-segment comparison of the same 28 windows',pad=100)
    save(fig,args.out/'wham-profiles')
    print(json.dumps({'overlap':overlaps,'profiles':profile_rows,'bridges':rows[-2:]},indent=2))


if __name__=='__main__':main()
```

从原始XVG计算统计量、核对偏置力，并以实际直方图屏蔽空区间。

### 重现中英文结果图

```
#!/usr/bin/env bash
set -euo pipefail
python analyze_umbrella.py --out results-zh --language zh
python analyze_umbrella.py --out results-en --language en
```

使用数据包的records目录运行同一分析定义。

以两桥都加入的完整记录为例，2.4至2.6 nm区间的平均剖面值，比0.8至1.0 nm参照区间高20.7188 kJ/mol；对每窗前半段和后半段分别求解，得到23.4533与17.6447 kJ/mol。这里比较的是两个预先指定距离区间内的平均曲线高度，方便量化分段变化。要把研究问题改成“折叠与未折叠的自由能差”，需要先根据结构定义两个状态，再对各状态覆盖的概率进行积分，最后取概率比的对数；这与两个区间的曲线均值是不同的统计操作。

同样，端距上的低谷或高处需要结合分子结构解释。短端距可以由不同转角和侧链接触共同形成，某一距离格内也可能同时包含数种内部构象。一个有用的扩展是同时记录主链氢键或关键侧链接触，在相近端距下比较它们的分布，并从不同初态检查这些内部结构是否发生交换。若交换比端距涨落慢，增加第二个观察坐标或设计额外采样，会比单纯增加距离保存频率更直接地改善对构象空间的认识。

这套流程还提供了规划计算量的方法。先用短记录看哪些区域连得上、哪些窗口偏离中心较多，再把资源集中到有明确问题的位置；增加数据后，重新比较窗口历史与自由能剖面，而不是只检查输出文件是否生成。完整运行与分析脚本可以用于下一轮更长或更多初态的研究，分箱、温度、弹簧定义和参考区间则保持一致，便于知道结果变化来自新增采样，还是来自测量定义的改变。

从最初的移动弹簧，到固定窗口、桥接记录与WHAM，每一步都回答一个不同的问题：怎样得到起始构象，怎样在某个区域停留观察，怎样联系相邻记录，以及怎样恢复原有的相对概率。本例的实际轨迹展示了局部重叠可以改善，也展示了时间历史仍会改变剖面。把这些具体变化读清楚，自由能图就成为一份能够指导下一次计算的研究结果；分子的运动、统计权重和科学问题之间，也由此建立了可检查的联系。

## 延伸阅读与开放资料

- [GROMACS tutorials: chignolin umbrella sampling](https://github.com/Lemkul-Lab/gmx_tutorials_jpcb/tree/main/inputs/03_chignolin) · Justin A. Lemkul / Lemkul Lab · MIT

  原始结构、端距坐标、26窗流程与输入设置。

  保留科学问题；采用6.6 nm立方盒、缩短教学记录，增加双起点桥接和分段分析，更新完整脚本。
- [Introductory Tutorials for Simulating Protein Dynamics with GROMACS](https://doi.org/10.1021/acs.jpcb.4c04901) · Justin A. Lemkul · CC BY 4.0

  原教程第3练习的科学设计与研究目标。

  重新组织解释、符号表、历史图、交互和本次实算结果；短窗侧重观察采样行为。
- [CHARMM July 2022 GROMACS force-field archive](https://mackerell.umaryland.edu/charmm_ff.shtml) · MacKerell laboratory and CHARMM parameter contributors · Publicly downloadable parameter archive; separate open license not stated in the archived package

  CHARMM36m蛋白与CHARMM TIP3P参数。

  通过原维护者链接下载并核对哈希；完整参数包保留其原始条款和文献说明。
- [1UAO: ten-residue peptide chignolin](https://www.rcsb.org/structure/1UAO) · S. Honda, K. Yamasaki, Y. Sawada, H. Morii · wwPDB data: CC0

  实验结构身份、序列与NMR构象集合。

  模型1的Cα坐标重绘为正交投影。
- [Nonphysical sampling distributions in Monte Carlo free-energy estimation: Umbrella sampling](https://doi.org/10.1016/0021-9991%2877%2990121-8) · G. M. Torrie and J. P. Valleau · Citation; no source text or figures reproduced

  伞形采样的历史与统计思想。

  用短肽问题重述偏置分配观察机会的含义。
- [The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method](https://doi.org/10.1002/jcc.540130812) · S. Kumar, D. Bouzida, R. H. Swendsen, P. A. Kollman, J. M. Rosenberg · Citation; no source text or figures reproduced

  WHAM历史与自洽归一化方程。

  按离散区间概率重写公式解释与零偏置算例。
- [GROMACS 2026.4: gmx wham](https://manual.gromacs.org/2026.4/onlinehelp/gmx-wham.html) · GROMACS development team · Official documentation; linked for command definitions

  原生命令、直方图、相关性与输入配对要求。

  固定共同网格并加入空区间检查与分段比较。
