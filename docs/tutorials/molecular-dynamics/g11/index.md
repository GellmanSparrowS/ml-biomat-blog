# 双螺旋在溶液里怎样运动

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g11/
Language: zh-CN

从碱基配对、水和离子出发，运行周期DNA模型，观察双螺旋中持续发生的局部运动。

## 从遗传分子到可设计的材料

DNA常以一条整齐的双螺旋出现在课本里，像一架永远保持同一形状的旋转楼梯。放进水里以后，这架“楼梯”的台阶会轻微摇摆，扶手会弯曲，附近的水和离子不断换位。遗传信息保存在碱基的排列次序中，而分子的空间形状随环境和热运动持续变化。把这两件事分开，是阅读核酸模拟的起点：相同的字母顺序可以对应许多构象，构象变化又会影响蛋白质怎样接近DNA，以及哪些原子更容易与水或其他分子接触。

这种认识也与材料设计有关。两段具有互补序列的DNA能够形成有选择性的配对，因此可以用作识别单元或可组装结构的连接部分。设计者既关心两段是否能够结合，也关心结合后的连接处怎样弯曲、局部配对怎样起伏。就像搭建模型时，连接件的长度和柔软程度会影响整个形状，分子材料也需要知道连接单元的空间响应。本讲先研究一个结构明确的双螺旋片段，让局部运动与可计算的几何量建立联系，再讨论怎样把这些方法用于更大的问题。

我们将运行一个20碱基对的周期DNA模型。它包含两条各20个核苷酸的骨架、2688个水分子和40个钠离子，在300 K附近观察1 ns的无偏运动。“无偏”在这里有具体意思：没有额外施力去拉开某一对碱基，运动由既定力场、温度和压强条件产生。起始结构已经处在配对状态，轨迹主要展示这个状态附近的局部波动。模型沿轴向跨周期边界连接，适合研究连续双螺旋内部的一个重复单元，其连接方式将在运行前仔细说明。

读完以后，你可以辨认DNA模型中的骨架、碱基、水和反离子，检查周期连接，运行完整输入，并从真实轨迹中提取三种不同的局部测量：两个原子相距多远，供体—氢—受体的方向怎样，两块碱基环平面倾斜多少。随后把这些量画成时间曲线、空间位置图和分布图。每一种图都保留原子选择、时间窗口与单位，这样一张漂亮的分子动画才会成为可以讨论和复算的研究结果。

这里需要的生物学与几何知识都会在使用处展开。你可以把DNA先看成有明确连接顺序的两条分子链，再逐步认识链上的化学结构。也可以把一条轨迹先看成按时间排列的坐标表，再学习如何从坐标得到距离和角度。分子模拟把这两种描述放在同一处：化学定义哪些原子相连、哪些作用需要计算，几何和统计把它们的运动转成容易比较的数量。

### 水溶液中的周期双螺旋

实际1 ns轨迹中的保存帧；碱基、骨架和周期连接按实际模型理解。

官方周期DNA模型，20碱基对、40核苷酸、1261 DNA原子、2688 SPC/E水和40 Na；总9365原子。Parmbsc1参数、300 K、1 bar，倾斜周期盒；20 ps衔接后1 ns无偏轨迹。

[下载参考数据与完整输入（ZIP） 33.27 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dna-reference-data.zip)

## 衍射图为什么改变了对DNA的理解

理解DNA结构并不是先拍到一张清晰的分子照片，再照着照片搭模型。二十世纪五十年代的关键工具之一是X射线衍射：让X射线穿过排列较有规律的DNA纤维，记录散射后留下的图案。Franklin与Gosling在不同含水条件下观察DNA，湿度较高的B形与较低含水条件下的A形呈现不同衍射特征。1952年的著名衍射照片及1953年的结构研究，让分子的周期排列与双螺旋模型联系起来，也把水化条件带进了结构问题本身。

衍射图案可以用波的叠加来理解。两列水波相遇时，某些位置的起伏会增强，另一些位置会抵消；从不同原子散射出的X射线也会发生相干叠加。若原子排列有某种重复间距，散射图中就会出现与这种重复有关的特征。记录到的亮暗关系需要结合数学和化学才能解释，并不是把分子轮廓直接印在底片上。科学家因此要同时满足几类信息：衍射给出的周期关系、分子组成、合理的键长与连接，以及碱基之间可能形成的接触。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s2)

图 1 · 衍射与结构建模的原理图：样品的周期排列影响衍射图案，结构模型还须满足分子化学。图中斑点是讲解用示意。

Watson与Crick在1953年提出双螺旋结构模型，同期发表的Franklin与Gosling、Wilkins及合作者的衍射研究提供了重要结构信息。把这些工作放在一起，更容易理解结构研究的实际过程：实验提供约束，模型把约束组织成空间解释，再由更多实验检验它。我们在分子模拟中也会遇到相似关系。坐标文件给出一个结构起点，力场规定运动规则，轨迹则显示这些规则和条件下出现了哪些变化；三者需要彼此对应。

科学史还有一个直接服务于本讲的提醒：DNA的环境属于结构的一部分。水不仅填满双螺旋周围的空白，还会与暴露的化学基团形成有方向的作用；离子则改变带电骨架周围的静电环境。在实验中改变湿度，与在水溶液模拟中改变盐含量或水模型，是不同的具体操作，但都指向同一个问题：分子的构象怎样依赖周围介质。我们因此把水和离子作为实际运动的粒子加入，而不是只画一条孤立的螺旋。

衍射和轨迹也观察不同层面的结构。衍射信号汇集许多分子及其在测量期间的排列信息，模拟保存帧则给出一个小体系在某些时刻的坐标。比较二者时，需要从轨迹计算与实验相应的平均或散射量。眼前这一讲先练习更直接的局部几何：它们能帮助判断模型中发生了怎样的运动，也为以后构造与实验相匹配的观测量打下基础。

## 沿着一对碱基读懂分子模型

DNA的基本重复单元叫核苷酸，可以分成磷酸、脱氧核糖和碱基三部分。脱氧核糖是一种五碳糖，糖与磷酸交替连接构成链的骨架，碱基从糖上伸出。常见的四种碱基用A、T、G、C表示，分别是腺嘌呤、胸腺嘧啶、鸟嘌呤和胞嘧啶。糖上的碳按带撇号的编号区分，例如1′、3′与5′，使它们与碱基上的编号分开。所谓5′到3′方向，便来自这套化学连接规则，并不是给图上的上下方向随意起名。

在常见的双螺旋配对中，两条链的化学方向相反，A与T配对，G与C配对。可以先把局部结构展开成一架梯子：糖磷酸骨架像两侧的扶手，互补碱基像中间配合的台阶。这幅梯子图能帮助分清连接关系，真实分子还具有扭转、堆叠和沟槽。相邻碱基沿螺旋轴的堆叠，与对向碱基之间的接触共同参与结构稳定；简单地把整个双螺旋理解成由几根氢键吊住的两条链，会漏掉相邻台阶及溶剂环境的作用。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s3)

图 2 · 把双螺旋局部展开成梯子，便于分清骨架连接与碱基配对。箭头文字表示沿图向下阅读时两条骨架的相反化学方向。

本例第一条链的序列为CGCGCGCGCGTGCGCGCGCG，第二条链按其自身方向记录为CGCGCGCGCACGCGCGCGCG。比较互补关系时，第二条要反向读，因为两条骨架反平行。第一条第11位的T与第二条对应的A配对；在整个坐标文件连续编号中，它们记作DT11与DA30。残基名里的D表示脱氧核苷酸，最后一个字母标明碱基种类。分析程序按真实链和残基选择原子，不通过屏幕上看起来相邻就猜测谁与谁配对。

观察一条氢键，还需要分清供体、氢与受体。T的N3与H3共价相连，A的N1是本讲所选接触的受体。供体和受体之间的距离描述它们是否靠近，N3—H3—N1夹角描述氢朝向受体的程度。两项信息结合，比只量两个氮之间的距离更接近氢键的几何特征。这里的“氢键”与骨架上的共价键承担不同角色：原子间非键作用产生可变的接触，固定拓扑中的共价连接则规定了分子骨架。

力场采用随模型提供的amber99bsc1参数实现，水使用SPC/E。这个经典模型显式表示DNA原子及其连接，用键、角、扭转和非键作用描述构象变化；涉及氢的共价键长度采用约束，使2 fs时间步能够用于所选运动。电子、化学反应与质子在分子间转移不作为独立自由度演化。因此，碱基接触可以随着构象而减弱或恢复，DNA骨架仍按输入中的共价键图保持连接。研究化学损伤或酶催化切断骨架时，需要在模型中加入相应的反应描述。

每个周期核苷酸带有骨架磷酸的负电荷，两条链的总电荷约为−40个元电荷。40个Na⁺使周期单元整体电中性；这40个离子是为平衡DNA电荷加入的反离子，体系中没有对应的40个Cl⁻盐离子。反离子仍能在溶液中移动，整体中和也没有消除局部电场。水的取向、离子的停留位置和骨架构象相互作用，后面的近邻计数正是观察这个环境的一种具体方式。

## 周期连接给双螺旋施加了什么条件

模拟中的周期边界可以先想成一张不断重复的墙纸：离开一个单元的图案，在相邻单元中继续。对一盒普通水，这主要规定粒子穿过边界后怎样找到相邻环境。本例还多了一层连接：每条DNA骨架的末端原子，通过共价键与相邻周期像中的起始原子相连。于是，一个单元中的20个碱基对组成连续双螺旋的重复部分，链上没有游离的5′或3′末端。

这种设置让研究问题集中在连续螺旋内部。短游离双链的末端可能出现不同于内部的波动，而本例把这些末端效应从几何中移开。同时，周期长度也参与规定轴向条件：螺旋在一个盒长内连续接回相邻单元，整体伸缩与扭转受到这个重复关系的约束。局部碱基仍能摇摆，骨架仍能变形；这些运动发生在周期连接所允许的构象集合里。为有限寡核苷酸测末端解链，或研究长链的大尺度弯曲，应另建具有相应端点和尺度的体系。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s4)

图 3 · 左：xy面夹角60°，距离计算使用完整盒向量。右：20碱基对单元沿z连续重复，骨架跨边界相连；图外的曲线表示相邻周期像。

这个盒子在xy平面还是倾斜的，两条平面盒边之间的夹角为60°。三个边向量描述周期平移，其中z方向的边与xy平面垂直。以第一帧为例，第一条边约为(4.005,0,0) nm，第二条约为(2.002,3.468,0) nm，第三条约为(0,0,6.540) nm。第二条边的长度约4.005 nm，而它的y方向分量约3.468 nm，两者各有明确含义。读取盒尺寸时分清向量长度与坐标分量，能避免把一个倾斜单元误画成直角盒。

倾斜盒子的体积式 5

![倾斜盒子的体积](https://ml-biomat.com/static/agent-math/20e51513b824d8b84ca0c0b9.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| V | 周期单元体积 | nm³ |
| a、b、c | 三个盒边向量的长度 | nm |
| γ | a与b的夹角；c与它们均垂直 | ° |
| sin | 正弦函数，计算平行四边形高度与边长的比例 | 运算符 |
| =、+、−、/、× | 相等、相加、相减、除法、乘法；分数横线也表示除法。 | 运算符 |

怎样理解xy底面是平行四边形，面积等于底边a乘垂直高度b sinγ，再乘轴向高度c。

算一个例子若a=b=4 nm、c=6.5 nm、γ=60°，V=4×4×6.5×0.866025≈90.0666 nm³。把它当直角盒会得到104 nm³。

使用条件适用于本例z边垂直xy平面的几何。分析代码用三盒向量组成矩阵的行列式计算每帧体积。

距离计算也必须使用相同几何。一个原子与周期像中的近邻可能在坐标表里相隔很远，直接相减会把穿过边界的短距离写成接近盒长的距离。正确的方法是在周期平移后寻找最短分离，称为最小镜像距离。本讲调用支持完整倾斜盒的距离函数，逐帧传入当时的盒向量。压强耦合会改变盒子，因此不能把第一帧的尺寸固定用于整个轨迹。

寻找离指定原子最近的周期镜像式 1

![寻找离指定原子最近的周期镜像](https://ml-biomat.com/static/agent-math/0a85b50b17c9129522654a18.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| dᵢⱼ | 原子i与j的最小镜像距离 | nm |
| rᵢ、rⱼ | 两原子的三维位置向量 | nm |
| a、b、c | 定义一个周期盒的三个边向量 | nm |
| n₁、n₂、n₃ | 沿三个盒向量移动的整数次数 | 无量纲 |
| i、j | 原子编号 | 无量纲 |
| min、‖ ‖、∈、ℤ | 取最小值；向量长度；属于；整数集合 | 运算符与集合 |
| =、+、−、/、× | 相等、相加、相减、除法、乘法；分数横线也表示除法。 | 运算符 |

怎样理解周期复制使一个原子有许多等价坐标。逐个考虑相邻平移后取最短分离，得到局部接触实际对应的距离。

算一个例子一维盒长4 nm，两个坐标为0.2和3.8 nm。直接相减是3.6 nm；将后者减去一个盒长，得到−0.2 nm，与前者相距0.4 nm。

使用条件实际盒在xy平面有60°夹角，程序使用完整盒几何；三个坐标分别按直角盒取余会改变这个距离定义。

跨边界骨架还影响轨迹整理。若试图把一条无限延续的周期链全部塞进一个有限、完全展开的分子图像，沿链走一圈会遇到一个盒向量的差别。分析局部接触时，我们直接使用最小镜像距离；拟合单个碱基环时，只把这块小环的原子重建到共同局部坐标中。这样既保持环的几何完整，又保留整条链的周期性质。输入里的`periodic-molecules = yes`正是告诉GROMACS按这种自连接结构处理相互作用。

压强耦合采用半各向同性设置：xy方向共同调整，z方向独立调整，目标压强均为1 bar。这里没有膜，“半各向同性”描述的是盒子的调节方式。DNA沿z连续延伸，因此把轴向周期长度和体积曲线一起保存，有助于理解局部构象处于什么几何条件中。体系平均压强会有较大瞬时起伏，温度、体积和局部距离又可能具有不同变化速度；阅读它们时要分别看清测量量和时间尺度。

## 运行一段有明确起点的DNA轨迹

完整例题由模型准备程序、两个MD参数文件、运行脚本和分析程序组成。先把这些文件放在同一个目录，执行`python prepare_dna.py`取得带有坐标、拓扑、索引和力场的周期模型。已有对应归档时，可用`--archive dna-awh.zip`指定它。程序核对归档内容后生成运行需要的文件，坐标中的原子顺序与速度保持一致；模型包含的具体原子、残基和反离子会在终端中给出。

### 取得完整周期DNA模型

```
"""Prepare the official periodic DNA model in the current directory.

python prepare_dna.py --archive dna-awh.zip
Without --archive, the verified upstream archive is downloaded first.
The molecular data and force-field parameters retain the upstream CC BY 4.0 notice.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.request import Request, urlopen
from zipfile import ZipFile

URL = 'https://gitlab.com/gromacs/online-tutorials/awh-tutorial/-/archive/main/awh-tutorial-main.zip'
SHA256 = '67dedf235b40959e0b58239a18ade6f2f92beac1cd4fb7756b1bad9c05b15e6c'
PREFIX = 'awh-tutorial-main/awh-simple/'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=Path('dna-awh.zip'))
    ap.add_argument('--out', type=Path, default=Path('.'))
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    if not args.archive.exists():
        with urlopen(Request(URL, headers={'User-Agent': 'MD-course'}), timeout=60) as response:
            with args.archive.open('wb') as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
    with args.archive.open('rb') as source:
        digest = hashlib.file_digest(source, 'sha256').hexdigest()
    if digest != SHA256:
        raise ValueError(f'SHA256 mismatch for {args.archive.name}; obtain the matching reference archive.')
    written = {}
    with ZipFile(args.archive) as z:
        for member in z.namelist():
            if not member.startswith(PREFIX) or member.endswith('/'):
                continue
            name = member[len(PREFIX):]
            if name not in ['conf.gro', 'topol.top', 'index.ndx'] and not name.startswith('amber99bsc1.ff/'):
                continue
            destination = (args.out / name).resolve()
            if not destination.is_relative_to(args.out.resolve()):
                raise ValueError('Invalid archive path.')
            data = z.read(member)
            if name == 'conf.gro':
                lines = data.decode().splitlines()
                lines[0] = 'Periodic 20-base-pair DNA in SPC/E water'
                data = ('\n'.join(lines) + '\n').encode()
            elif name == 'topol.top':
                # Remove generated workstation metadata, preserving molecular records.
                lines = data.decode().splitlines()
                metadata = re.compile(r'^\s*;.*(?:/data/|/home/|By user:|On host:|At date:|Executable:|Data prefix:|Working dir:|Command line:|gmx pdb2gmx)')
                data = ('\n'.join(line for line in lines if not metadata.search(line)) + '\n').encode()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            written[name] = hashlib.sha256(data).hexdigest()
        (args.out / 'LICENSE-source.txt').write_bytes(z.read('awh-tutorial-main/LICENSE'))
    lines = (args.out / 'conf.gro').read_text().splitlines()
    if int(lines[1]) != 9365 or not all(len(s) >= 68 for s in lines[2:9367]):
        raise ValueError('Expected 9365 atoms with retained velocities.')
    (args.out / 'model-files.json').write_text(json.dumps(written, indent=2))
    print('Prepared 20 periodic base pairs, 2688 SPC/E waters, and 40 sodium ions.')


if __name__ == '__main__':
    main()
```

准备后在例题目录运行bash run.sh；分析用python analyze_dna.py --run . --out figures --language zh。

这个起点是已经准备好的周期双螺旋状态，不是从一段序列凭空开始折叠，也不是一个带PDB编号的实验结构。坐标文件中的每个原子已有位置和速度，拓扑提供相同顺序下的质量、电荷与连接关系。继续模拟时使用这些状态，能够把注意力放在DNA的局部运动与分析上。若换成自己的序列，就需要重新构建对应的结构和拓扑、处理端点或周期连接，并完成溶剂化与准备；这些操作改变的是模型本身。

第一阶段运行20 ps，时间步为0.002 ps，也就是2 fs，因此需要10000步。温度采用v-rescale调节，目标300 K、耦合时间0.5 ps；压强采用Parrinello–Rahman调节，耦合时间5 ps。这里保留已有速度，`gen-vel = no`使程序不再分配一套新的起始速度。准备段让我们检查这个起点在当前输入下能否连续运行，并保留其末态供后续观测使用。

### 20 ps准备参数

```
title                    = Amber NPT equilibration 
integrator               = md
dt                       = 0.002
nsteps = 10000

nstlog = 1000
nstenergy = 100
nstxout-compressed = 500

; Settings that make sure we run with parameters in harmony with the selected force-field
coulombtype              = pme
rcoulomb                 = 1.0
fourierspacing           = 0.121 ; grid spacing for FFT
;
vdwtype                  = cut-off
vdw-modifier             = potential-shift-verlet
rvdw                     = 1.0
dispCorr                 = enerpres
constraints              = h-bonds

; Pressure coupling is on
pcoupl                   = parrinello-rahman  
pcoupl-type              = semiisotropic  ; isotropic in the x and y direction, but different in the z direction  
tau_p                    = 5.0 
ref_p                    = 1.0 1.0
compressibility          = 4.5e-5 4.5e-5 
nstpcouple               = 10

; Keep system temperature fluctuating physically correct
tcoupl                   = v-rescale 
tc-grps                  = system
tau_t                    = 0.5 
ref_t                    = 300 

gen-vel                  = no
gen-temp                 = 300
gen-seed                 = -1


periodic-molecules       = yes              ; for systems with molecules that couple to themselves through the periodic boundary conditions, this requires a slower PBC algorithm and molecules are not made whole in the output.

ld-seed = 20263111
```

准备后在例题目录运行bash run.sh；分析用python analyze_dna.py --run . --out figures --language zh。

第二阶段从准备段的坐标与检查点接续，运行500000步，覆盖1 ns。检查点携带继续积分和耦合所需的状态，坐标文件则提供相应的结构记录。两个阶段保持同一力场、水模型、非键设置和温压目标。PME处理长程静电，库仑与范德华实空间截断均为1.0 nm，色散修正用于能量与压强。按同一套参数接续，使两阶段之间的差别主要是准备与观测的组织，而不是中途更换相互作用。

### 1 ns无偏观测参数

```
title                    = Amber NPT equilibration 
integrator               = md
dt                       = 0.002
nsteps = 500000

nstlog = 1000
nstenergy = 100
nstxout-compressed = 500

; Settings that make sure we run with parameters in harmony with the selected force-field
coulombtype              = pme
rcoulomb                 = 1.0
fourierspacing           = 0.121 ; grid spacing for FFT
;
vdwtype                  = cut-off
vdw-modifier             = potential-shift-verlet
rvdw                     = 1.0
dispCorr                 = enerpres
constraints              = h-bonds

; Pressure coupling is on
pcoupl                   = parrinello-rahman  
pcoupl-type              = semiisotropic  ; isotropic in the x and y direction, but different in the z direction  
tau_p                    = 5.0 
ref_p                    = 1.0 1.0
compressibility          = 4.5e-5 4.5e-5 
nstpcouple               = 10

; Keep system temperature fluctuating physically correct
tcoupl                   = v-rescale 
tc-grps                  = system
tau_t                    = 0.5 
ref_t                    = 300 

gen-vel                  = no
gen-temp                 = 300
gen-seed                 = -1


periodic-molecules       = yes              ; for systems with molecules that couple to themselves through the periodic boundary conditions, this requires a slower PBC algorithm and molecules are not made whole in the output.

ld-seed = 20263111
continuation = yes
```

准备后在例题目录运行bash run.sh；分析用python analyze_dna.py --run . --out figures --language zh。

### 依次运行并导出热力学记录

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f pilot.mdp -c conf.gro -p topol.top -n index.ndx -o pilot.tpr > pilot.grompp.log 2>&1
"$gmx" mdrun -deffnm pilot -ntmpi 1 -ntomp 2 -pin off > pilot.stdout.log 2>&1
"$gmx" grompp -f md.mdp -c pilot.gro -t pilot.cpt -p topol.top -n index.ndx -o md.tpr > md.grompp.log 2>&1
"$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 2 -pin off > md.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

准备后在例题目录运行bash run.sh；分析用python analyze_dna.py --run . --out figures --language zh。

执行`bash run.sh`后，`grompp`把参数、拓扑、坐标和索引组合成可运行的TPR文件，`mdrun`推进运动。脚本随后从能量文件提取温度、压强、体积及盒参数，保存为可读表格。坐标每1 ps记录一次，所以生产阶段含有0到1000 ps的1001帧；能量记录每0.2 ps一次，含5001个时间点。两种输出密度不同，分析时各自使用自己的时间列。

实际生产轨迹中，后半段温度均值约299.992 K，保存记录的标准差约3.043 K。这个数字说明温度记录的平均与起伏，不把1001帧都变成彼此独立的结构样本。检查运行还应读取原子数、时间是否单调、坐标是否有限，以及跨边界共价连接是否保持合理长度。分析程序核到两条周期闭合键分别连接第1与632号、第633与1261号原子，它们在轨迹中的最小镜像距离约0.148至0.171 nm。

原子编号与程序下标有一个容易复现的小差别。GROMACS索引文件从1开始编号，Python数组从0开始。目标氮原子在索引中是338和936，读取数组时因此使用337和935。完整程序先检查这些位置确实对应DT11的N3与DA30的N1，再开始统计。这个身份检查比看到一条大致合理的距离曲线更早，也更容易定位选错原子的原因。

## 把局部运动拆成距离、方向与倾斜

先看目标碱基对的N3—N1距离。它在这1 ns中的平均值约0.29605 nm，保存帧的标准差约0.01119 nm，最小与最大值约为0.2707和0.3592 nm。平均值提供一个典型尺度，时间曲线则显示短时变化怎样围绕这个尺度发生。一次较大的距离值可以与邻近帧、氢的方向和环平面的运动一起阅读，这比只设一个距离阈值就给整对碱基贴上“打开”标签更有物理内容。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s6)

图 4 · 左图的角在氢原子处定义，接近180°时供体、氢与受体更接近共线。右图的平面夹角使用两法向量；它与左图的氢键角描述不同几何关系。

### 一对碱基的局部运动

N—N距离、氢键方向与环平面夹角来自相同1001帧。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s6)

所选DT11—DA30接触的距离、D—H—A角与局部碱基平面角，采用倾斜盒的最小映像几何。

第二条曲线量N3—H3—N1夹角。角的顶点在H3上，两条边分别从H3指向供体N3和受体N1，接近180°表示三个原子接近共线。实际平均角约165.92°，标准差约7.29°。同一对氮相距差不多时，氢仍可能偏向别处，所以距离与方向要配套观察。分析中每一帧的距离与角度一起保存，散点图上的一个点便同时保留了这两项信息。

将供受体距离不超过0.35 nm、供体—氢—受体角不小于150°作为本讲的几何判据，1001帧中有974帧同时满足，得到97.3027%的接触占比。这个比例对应一个指定原子接触在指定轨迹中的几何定义。A—T配对还包括其他接触，碱基张开又涉及堆叠、溶剂暴露及更大范围的构象变化，所以接触占比和整对碱基打开的概率是不同观测量。把定义写清楚后，可以按研究问题增加其他接触或溶剂量，而不必让一个数字承担所有含义。

按明确几何判据计算接触占比式 2

![按明确几何判据计算接触占比](https://ml-biomat.com/static/agent-math/89e25a33e369aa65f080c794.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| f | 满足两项条件的保存帧比例 | 无量纲 |
| M、k | 保存帧总数及帧编号 | 无量纲 |
| dₖ、dc | 第k帧供受体距离及阈值 | nm |
| θₖ、θc | 供体—氢—受体角及最小角阈值 | ° |
| 1[ ]、∑、≤、≥、and | 条件全满足记1，否则记0；求和；不大于；不小于；同时满足 | 运算符 |
| =、+、−、/、× | 相等、相加、相减、除法、乘法；分数横线也表示除法。 | 运算符 |

怎样理解逐帧检查同一对原子的距离和方向，计数后除以总帧数，便把“经常形成这样的几何”变成一个可复算比例。

算一个例子取dc=0.35 nm、θc=150°，本例974/1001=0.973027，即97.3027%。距离0.30 nm、夹角165°的一帧满足；同距离而夹角135°的一帧不满足。

使用条件这里统计DT11:N3—H3与DA30:N1这一接触的几何占比。帧间具有时间关联，测量对象是指定原子组与给定轨迹。

### 局部接触的分布

两半段使用相同箱边界，右图保留距离与角度的配对信息。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s6)

同一1001帧的距离与方向联合分布；几何判据定义该特定接触。

接触出现得多，与单次接触保持得久，是两个不同的问题。假设两段记录都有九成帧满足判据，其中一段可能频繁短暂偏离，另一段可能只有一次较长偏离。它们的占比相同，时间组织却不同。研究接触寿命时，需要保留连续的满足与不满足区间，还要明确1 ps保存间隔之内的短过程怎样处理；当前占比则直接回答保存时刻中有多少满足所选几何。

第三条曲线关注两块碱基环平面的相对倾斜。把一个六元环中的原子近似拟合成平面，再找一条与平面垂直的单位向量，这条向量叫法向量。两条法向量的点积给出它们夹角的余弦。由于同一个平面可以选择朝上或朝下的法向量，先取点积绝对值，便能消除这个任意的正负方向。本例得到的平面夹角平均约11.32°，说明两块环也在持续发生相对倾斜。

比较两个碱基环平面的倾斜式 3

![比较两个碱基环平面的倾斜](https://ml-biomat.com/static/agent-math/a397f68bcc9f396532fcba61.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| β | 两无方向平面的较小夹角，范围0至90° | ° |
| n̂₁、n̂₂ | 与各环拟合平面垂直、长度为1的向量 | 无量纲 |
| ·、\| \|、arccos | 点积；绝对值；余弦的反函数，最后转成度 | 运算符 |
| 1、2 | 两块碱基环平面的编号 | 无量纲 |
| =、+、−、/、× | 相等、相加、相减、除法、乘法；分数横线也表示除法。 | 运算符 |

怎样理解平面的法向量可以指向两个相反方向，物理平面相同。取点积的绝对值消除这个符号任意性，再由余弦反求夹角。

算一个例子两个单位法向量取(0,0,1)与(0.6,0,0.8)，点积0.8，因此β≈36.87°。把第二个向量反向，绝对值仍为0.8，平面夹角不变。

使用条件程序分别拟合原索引中的两个六元环。这是环平面夹角；DNA局部扭转、张开或螺旋参数需各自的坐标定义。

这个平面角值得与DNA专用的螺旋参数区分。它只比较两块环平面的朝向，范围为0至90°，不会说明某个碱基向大沟还是小沟转出，也不等同于相邻碱基对之间的扭转角。若研究需要完整的张开、剪切、伸展和扭转分解，可以进一步引入有明确局部坐标系的核酸结构分析。先使用定义简单、可以手算的几何量，有助于读者理解更专门的参数究竟新增了哪些方向信息。

下面的交互仍使用实际的1001帧，只改变分类条件。把距离阈值收紧，或把最小角提高，绿色区域中的点会减少；将条件放宽则会增加。坐标和轨迹没有变化，变化的是你用来描述接触的尺子。进行不同体系的比较时，沿用同一判据才能让占比具有共同含义；研究判据敏感性时，则应像这里一样，把改变的阈值与结果同时展示。

用同一组1001帧，比较接触判据的选择。

基于实际1001帧的静态交互。调节阈值重新分类同一批观测，方向键可控制滑块。

最后用GROMACS自身的距离工具独立读取同一对原子。这里显式关闭整分子重建，同时开启周期距离处理，适应跨边界连续的骨架。输出与Python的最小镜像距离在保存精度内一致。两个工具采用同一原子定义和同一盒几何，是这次比较成立的基础；若一个工具测原子距离，另一个测整块碱基的质心距离，数值不同便首先来自测量定义。

### 用GROMACS独立读取同一距离

```
gmx distance -s md.tpr -f md.xtc -select "atomnr 338 plus atomnr 936" -normpbc -pbc -oall target-distance.xvg
```

关闭整条分子重建，保留周期最小镜像距离；适用于本例跨边界自连接骨架。

## 把时间轨迹读成分布和环境变化

时间曲线保留变化先后，直方图则把问题改成“哪些距离出现得较多”。将距离轴切成一段段小区间，数每段中落入多少帧，再按总帧数与区间宽度归一化，就得到概率密度。密度的单位是nm⁻¹；某个柱子的高度可以大于1，因为真正的区间概率由高度乘宽度得到。这个单位检查能帮助分清直方图纵轴究竟画的是次数、比例还是密度。

从距离直方图读出概率式 4

![从距离直方图读出概率](https://ml-biomat.com/static/agent-math/0c697a54b2064d3c9e2b3da0.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| pj | 第j个距离箱的概率密度 | nm⁻¹ |
| Nj | 落入第j个箱的保存帧数 | 无量纲 |
| M | 参与这一幅直方图的总帧数 | 无量纲 |
| Δd | 距离箱宽度 | nm |
| Pj | 落入该箱的帧比例 | 无量纲 |
| j、Δ | 距离箱编号；区间宽度 | 无量纲；运算符 |
| =、+、−、/、× | 相等、相加、相减、除法、乘法；分数横线也表示除法。 | 运算符 |

怎样理解先把计数除以总样本数得到一段距离内的比例，再除以箱宽得到单位距离上的密度。柱高乘柱宽恢复该区间的概率。

算一个例子500帧中50帧落在宽0.01 nm的箱内，密度为50/(500×0.01)=10 nm⁻¹，区间比例为10×0.01=0.10。密度数值大于1与概率不超过1相容。

使用条件两半段采用相同箱边界，各自按500或501帧归一化。比较的是已观测到的局部距离分布。

本例分别统计0≤t<500 ps与500≤t≤1000 ps，两段含500和501帧。它们使用同一组距离箱边界，均值分别约0.29484与0.29725 nm。两幅分布的主要区域相近，同时保留尾部与形状的差异。相邻半段从同一条轨迹延续而来，所以这里观察的是时间窗口敏感性。独立重复需要另建速度和随机历史，并在相同模型条件下分别运行，才能回答重复之间的变化有多大。

还可以把同一测量扩展到20个配对位置。程序沿第一条链排序，与第二条反向序列逐对对应，为每对选择中心的N1或N3原子，生成一幅位置—时间图。横轴仍是时间，纵轴是配对位置，颜色是最小镜像距离。这样既能找到目标A—T对，也能看到周围G—C配对的局部波动。颜色上限截在整体记录的99.5%分位处，使主要波动更容易辨认，超出的点用色条顶端颜色表示，原始距离仍完整保存在CSV中。

### 沿双螺旋观察20个配对位置

颜色表示中心N—N最小镜像距离；色条上三角表示超出显示上限的值，原数据完整保留。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s7)

20对碱基的中心N—N最小映像距离逐帧绘制；色条上三角标出超过显示上限的值。

DNA周围的离子环境也在变化。我们把每个Na⁺到全部磷酸非桥氧O1P、O2P的最短距离算出来，小于或等于0.35 nm便计作一个近邻离子。同一个Na⁺即使同时靠近两个氧，也只计一次。实际1001帧的近邻数平均约3.216，标准差约1.825，范围0到9。这里的近邻是一个空间定义，40个反离子仍始终留在周期体系中；近邻数下降，表示更多离子处于所选近邻区域之外。

这个计数不会把离子固定在某个位点，也没有把靠近等同于形成新的共价键。若研究特定离子的停留时间，还需保留离子身份，跟踪它进入、离开及再次返回的时间，并说明短暂越过阈值怎样处理。若研究盐浓度效应，则要给体系加入成对的阳离子与阴离子，在电中和之外定义额外盐含量。当前40个Na⁺首先服务于带负电DNA的反离子环境，这一点决定了怎样与其他盐条件比较。

### 轴向重复与近邻离子

Na⁺按距任一磷酸非桥氧≤0.35 nm计数，每个离子每帧最多计一次。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/#zh-s7)

原生盒矢量确定轴向周期与盒体积；Na⁺在任一磷酸非桥氧0.35 nm内每帧只计一次。

最后把轴向周期长度与离子曲线并列。实际轴向重复长度平均约6.579 nm，盒体积平均约90.379 nm³，二者会随温压耦合和体系运动变化。轴长除以20可以给出每个重复配对位置所分摊的平均轴向尺度，但单个碱基台阶的升高还需局部几何分析。不同量放在同一时间轴上方便寻找值得追踪的同步变化；判断因果关系仍要通过受控改变条件、重复计算和相应的机制测量来组织证据。

### 完整Python：配对、方向、离子与盒几何

```
"""Analyze the periodic duplex with full triclinic minimum-image geometry.

Run: python analyze_dna.py --run . --out figures --language en
Dependencies: MDAnalysis 2.11, NumPy 2.5, Matplotlib 3.11.
Atom numbers in the index file are one-based; Python indices are zero-based.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_bonds, calc_angles, distance_array, minimize_vectors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def index_groups(path):
    groups = {}; current = None
    for raw in path.read_text().splitlines():
        line = raw.split(';', 1)[0].strip()
        if line.startswith('['):
            current = line.strip('[] ').strip(); groups[current] = []
        elif line and current:
            groups[current].extend(int(x) - 1 for x in line.split())
    return {k: np.array(v, dtype=int) for k, v in groups.items()}


def one_atom(residue, name):
    atoms = residue.atoms.select_atoms('name ' + name)
    if len(atoms) != 1:
        raise ValueError(f'Expected one {name} in residue {residue.resid}')
    return atoms[0].index


def ring_normal(points, box):
    # Each ring is smaller than the cell. Reconstruct this local object only.
    local = minimize_vectors(points - points[0], box)
    _, _, vh = np.linalg.svd(local - local.mean(axis=0))
    return vh[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, default=Path('.'))
    ap.add_argument('--out', type=Path, default=Path('figures'))
    ap.add_argument('--language', choices=['zh', 'en'], default='en')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in available]
    plt.rcParams.update({'font.family': fonts if args.language == 'zh' else ['DejaVu Sans'],
                         'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2',
                         'svg.fonttype': 'path'})
    u = mda.Universe(str(args.run / 'md.tpr'), str(args.run / 'md.xtc'))
    groups = index_groups(args.run / 'index.ndx')
    target = np.concatenate([groups['base_N1orN3'], groups['partner_N1orN3']])
    identities = [(a.resname, int(a.resid), a.name, int(a.index)) for a in u.atoms[target]]
    if identities != [('DT', 11, 'N3', 337), ('DA', 30, 'N1', 935)]:
        raise ValueError('Target must be the supplied thymine N3 and adenine N1.')
    dna = u.select_atoms('nucleic'); segments = dna.segments
    if len(segments) != 2 or [len(s.residues) for s in segments] != [20, 20]:
        raise ValueError('Expected two 20-residue periodic strands.')
    pair_residues = list(zip(segments[0].residues, segments[1].residues[::-1]))
    pairs = np.array([[one_atom(a, 'N1' if a.resname in ['DA', 'DG'] else 'N3'),
                       one_atom(b, 'N1' if b.resname in ['DA', 'DG'] else 'N3')]
                      for a, b in pair_residues])
    hydrogen = one_atom(u.atoms[target[0]].residue, 'H3')
    phosphorus_oxygen = dna.select_atoms('name O1P O2P')
    ions = u.select_atoms('resname NA')
    closure = []
    for strand in segments:
        first = one_atom(strand.residues[0], 'P')
        last = one_atom(strand.residues[-1], "O3'")
        if not any(set(b.indices) == {first, last} for b in strand.atoms.bonds):
            raise ValueError('Missing cross-boundary covalent closure.')
        closure.append([first, last])
    closure = np.array(closure)
    times = []; distances = []; angles = []; tilt = []; cells = []; counts = []; bonds = []
    for ts in u.trajectory:
        if not np.isfinite(ts.positions).all():
            raise ValueError('Non-finite trajectory coordinate.')
        box = ts.dimensions
        if not np.allclose(box[3:5], 90, atol=.01) or not np.isclose(box[5], 60, atol=.01):
            raise ValueError('This reference model uses a 60-degree cell in xy.')
        times.append(float(ts.time))
        distances.append(calc_bonds(u.atoms[pairs[:, 0]].positions,
                                    u.atoms[pairs[:, 1]].positions, box=box) / 10)
        angles.append(float(np.degrees(calc_angles(u.atoms[target[0]].position,
                      u.atoms[hydrogen].position, u.atoms[target[1]].position, box=box))))
        n1 = ring_normal(u.atoms[groups['base_6ring']].positions, box)
        n2 = ring_normal(u.atoms[groups['partner_6ring']].positions, box)
        tilt.append(float(np.degrees(np.arccos(np.clip(abs(np.dot(n1, n2)), 0, 1)))))
        cells.append(ts.triclinic_dimensions.copy() / 10)
        d = distance_array(ions.positions, phosphorus_oxygen.positions, box=box) / 10
        counts.append(int(np.sum(np.min(d, axis=1) <= .35)))
        bonds.append(calc_bonds(u.atoms[closure[:, 0]].positions,
                               u.atoms[closure[:, 1]].positions, box=box) / 10)
    t = np.array(times); d = np.array(distances); theta = np.array(angles)
    beta = np.array(tilt); h = np.array(cells); nc = np.array(counts); bc = np.array(bonds)
    if np.any(np.diff(t) <= 0) or bc.max() > .2:
        raise ValueError('Invalid time order or closure-bond geometry.')
    target_column = int(np.where(np.all(pairs == target, axis=1))[0][0])
    dt = d[:, target_column]
    hb = (dt <= .35) & (theta >= 150)
    halves = [t < 500, t >= 500]
    volume = np.linalg.det(h)
    summary = {
        'atoms': len(u.atoms), 'dna_atoms': len(dna), 'nucleotides': len(dna.residues),
        'base_pairs': len(pairs), 'waters': len(u.select_atoms('resname SOL').residues),
        'sodium_ions': len(ions), 'frames': len(t), 'time_ps': [float(t[0]), float(t[-1])],
        'target_one_based_atom_numbers': (target + 1).tolist(),
        'target_residues': ['DT11:N3', 'DA30:N1'],
        'target_distance_nm': {'mean': float(dt.mean()), 'sd': float(dt.std()),
                               'min': float(dt.min()), 'max': float(dt.max())},
        'target_angle_deg': {'mean': float(theta.mean()), 'sd': float(theta.std())},
        'ring_plane_tilt_deg': {'mean': float(beta.mean()), 'sd': float(beta.std())},
        'central_hbond_geometry_fraction': float(hb.mean()),
        'criterion': 'T:N3-to-A:N1 <=0.35nm and T:N3-H3-A:N1 angle>=150deg',
        'halves': [{'time_ps': [0, 500] if j == 0 else [500, 1000],
                    'frame_count': int(mask.sum()), 'distance_mean_nm': float(dt[mask].mean()),
                    'hbond_geometry_fraction': float(hb[mask].mean())}
                   for j, mask in enumerate(halves)],
        'na_within_035nm_phosphate_oxygen': {'mean': float(nc.mean()), 'sd': float(nc.std()),
                                            'min': int(nc.min()), 'max': int(nc.max())},
        'closure_bonds_one_based': (closure + 1).tolist(),
        'closure_bond_range_nm': [float(bc.min()), float(bc.max())],
        'cell_first_nm': h[0].tolist(), 'volume_mean_nm3': float(volume.mean()),
        'axial_repeat_mean_nm': float(h[:, 2, 2].mean()),
        'mean_central_distance_by_pair_nm': d.mean(axis=0).tolist(),
        'sequence_strand_A': ''.join(r.resname[-1] for r in segments[0].residues),
        'sequence_strand_B': ''.join(r.resname[-1] for r in segments[1].residues),
        'definitions': 'Full triclinic minimum images; ring-plane angle ignores normal sign. '
                       'Hydrogen-bond fraction is one stated geometric contact, not opening probability. '
                       'Neighbour counts count each sodium once. Adjacent frames are correlated.'}
    (args.out / 'dna_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out / 'dna_timeseries.csv', np.column_stack([t, dt, theta, beta, hb, h[:, 2, 2], volume, nc, bc]),
               delimiter=',', header='time_ps,target_distance_nm,DHA_angle_deg,plane_tilt_deg,hbond_geometry,axial_repeat_nm,volume_nm3,Na_near_phosphate,closure_A_nm,closure_B_nm', comments='')
    np.savetxt(args.out / 'dna_pair_distances.csv', np.column_stack([t, d]), delimiter=',',
               header='time_ps,' + ','.join('pair_' + str(i + 1) + '_nm' for i in range(20)), comments='')
    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(args.out / f'{name}.{ext}', dpi=170, bbox_inches='tight')
        plt.close(fig)
    colors = ['#147d85', '#c46938', '#4c78b5']
    fig, ax = plt.subplots(3, 1, figsize=(11, 9), sharex=True, layout='constrained')
    for axis, values, label, col in zip(ax, [dt, theta, beta],
                [tr('N3—N1距离 / nm', 'N3–N1 distance / nm'),
                 tr('N3—H3—N1角 / °', 'N3–H3–N1 angle / °'),
                 tr('两碱基环平面夹角 / °', 'Angle between base-ring planes / °')], colors):
        axis.plot(t, values, lw=.75, color=col); axis.set_ylabel(label)
    ax[0].set_title(tr('同一A—T碱基对的三种局部测量', 'Three local measurements of the same A–T pair'))
    ax[-1].set_xlabel(tr('时间 / ps', 'Time / ps')); save(fig, 'dna-local-motion')
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), layout='constrained')
    edges = np.linspace(dt.min() - .0001, dt.max() + .0001, 30)
    for i, mask in enumerate(halves):
        ax[0].hist(dt[mask], bins=edges, density=True, histtype='step', lw=2, color=colors[i],
                   label=['0 ≤ t < 500 ps', '500 ≤ t ≤ 1000 ps'][i])
    ax[0].legend(fontsize=10,loc='upper center',bbox_to_anchor=(.5,-.19),ncol=2); ax[0].set(xlabel=tr('N3—N1距离 / nm', 'N3–N1 distance / nm'),
             ylabel=tr('概率密度 / nm⁻¹', 'Probability density / nm⁻¹'),
             title=tr('相邻半段采用同一组距离箱', 'Common bins for adjacent half-trajectories'))
    ax[1].scatter(dt, theta, s=8, alpha=.4, color=colors[0]); ax[1].axhline(150, ls='--', c=colors[1])
    ax[1].set(xlabel=tr('N3—N1距离 / nm', 'N3–N1 distance / nm'), ylabel=tr('供体—氢—受体角 / °', 'Donor–H–acceptor angle / °'),
             title=tr('距离与方向共同描述接触', 'Distance and direction describe a contact'))
    save(fig, 'dna-contact-distribution')
    fig, ax = plt.subplots(figsize=(11, 6), layout='constrained')
    im = ax.pcolormesh(t, np.arange(1, 21), d.T, shading='nearest', cmap='viridis',
                      vmin=float(d.min()), vmax=float(np.quantile(d, .995)))
    ax.set_yticks(np.arange(1, 21)); ax.set(xlabel=tr('时间 / ps', 'Time / ps'),
                   ylabel=tr('第一条链的配对位置', 'Pair position on strand A'),
                   title=tr('20对碱基的中心N—N距离', 'Central N–N distances across 20 base pairs'))
    fig.colorbar(im, ax=ax, label=tr('最小镜像距离 / nm', 'Minimum-image distance / nm'), extend='max')
    save(fig, 'dna-pair-map')
    fig, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True, layout='constrained')
    ax[0].plot(t, h[:, 2, 2], color=colors[0], lw=1); ax[0].set_ylabel(tr('轴向周期长度 / nm', 'Axial repeat / nm'))
    ax[1].plot(t, volume, color=colors[1], lw=1); ax[1].set_ylabel(tr('盒体积 / nm³', 'Cell volume / nm³'))
    ax[2].plot(t, nc, color=colors[2], lw=.8); ax[2].set_ylabel(tr('磷酸氧近邻Na⁺数', 'Na⁺ near phosphate O')); ax[2].set_ylim(0, max(10,int(nc.max())+1))
    ax[2].set_xlabel(tr('时间 / ps', 'Time / ps')); ax[0].set_title(tr('轴向约束与离子环境随轨迹一同记录', 'Axial geometry and ionic environment along the trajectory'))
    save(fig, 'dna-cell-ions')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

准备后在例题目录运行bash run.sh；分析用python analyze_dna.py --run . --out figures --language zh。

## 让模型选择对应生物学问题

完成这次分析后，可以把研究目标写得更具体：在连续、周期连接的双螺旋内部，某一A—T对的局部几何怎样在水和反离子环境中波动？这个问题与现有坐标、连接方式及1 ns时间窗口匹配。若目标改为短DNA识别单元的末端稳定性，就应改用有限双链，并明确末端化学状态。若目标是DNA材料连接件的弯曲，需要足够长度和合适的连接结构，让待观察的空间变形能够在模型中发生。

讨论碱基打开的自由能时，还要让采样覆盖关闭与打开之间的变化。可以选择与打开有关的坐标，采用增强采样方法促进往返，再检查不同区域的覆盖、时间块与独立重复。当前无偏轨迹让我们熟悉关闭状态附近的几何变化，也帮助选择有物理含义的测量坐标。把两项工作衔接起来，研究路径便清楚了：先认识坐标和局部运动，再设计跨越不同构象区域的采样，最后计算与研究问题对应的分布或自由能。

生物学中的识别还涉及序列与环境共同作用。某个局部距离相近，并不意味着两个不同序列对蛋白质提供完全相同的接触面；沟槽形状、电荷分布、邻近碱基和溶剂暴露都可能参与。可以先固定温度、水模型、离子条件与边界，改变一个序列位置，再对同一套局部几何和环境量进行比较。这样的设计把差异与具体改变联系起来，也让后续增加蛋白质或配体时有一个清楚的结构参照。

对初学者，一个适合在现有数据上完成的练习，是同时改变氢键角阈值和距离阈值，记录目标接触占比，再比较两半段是否给出相同变化趋势。另一个练习是选取目标附近的G—C对，先查明供体氢和受体的化学身份，再复用分析方法。两个练习分别强调测量定义与原子选择：前者改变分类规则，后者改变被测对象，所需要检查的信息也不同。

课本中的双螺旋因此可以读成一个持续运动的分子结构。化学连接维持骨架，碱基接触和堆叠组织局部构象，水与反离子提供周围环境，周期几何规定这一次计算允许的整体变化。距离、方向、平面夹角和时间分布把这些运动拆成可理解的部分。以后研究糖链、蛋白质识别或核酸材料时，同样可以先问清对象与连接，再选择适合它的局部量、空间尺度和采样方式。

## 延伸阅读与开放资料

- [Calculating PMFs with AWH in GROMACS](https://tutorials.gromacs.org/docs/awh-tutorial.html) · Viveca Lindahl; reviewed and updated by Alessandra Villa and Christian Blau · CC BY 4.0

  原周期DNA模型、无偏MD设置、目标碱基原子索引。

  保留模型，采用20 ps准备及1 ns无偏轨迹；扩展基础解释、局部几何与离子分析。
- [Sequence dependency of canonical base pair opening in the DNA double helix](https://doi.org/10.1371/journal.pcbi.1005463) · Viveca Lindahl, Alessandra Villa, Berk Hess · CC BY

  parmbsc1参数实现与碱基局部接触的研究背景。
- [The story behind Photograph 51](https://www.kcl.ac.uk/the-story-behind-photograph-51) · Brian Sutton, King’s College London

  Franklin、Gosling的衍射与水化历史；本讲历史图为原创原理示意。
- [GROMACS periodic-molecules and pressure coupling](https://manual.gromacs.org/documentation/2026.4/user-guide/mdp-options.html#mdp-periodic-molecules)
- [gmx distance](https://manual.gromacs.org/documentation/current/onlinehelp/gmx-distance.html)
- [MDAnalysis distance functions](https://docs.mdanalysis.org/stable/documentation_pages/lib/distances.html)
