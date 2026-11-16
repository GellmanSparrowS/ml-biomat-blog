# 从分子字符串到化学结构表

Source: https://ml-biomat.com/tutorials/python-scientific/s04/
Language: zh-CN

用 RDKit 追踪原子、核对质量，并区分字符串、构型与化学身份。

## 一张分子表，先要知道每一行是谁

整理材料配方时，经常会遇到这样的表格：一列是名称，一列是结构字符串，后面跟着分子量、溶解性或实验编号。看起来只是普通的数据清洗，真正困难的地方却藏在结构里。同一种分子可以有不同写法；分子式相同的两种物质也可能具有不同连接方式；连接方式完全相同，空间构型仍可能不同。把字符串直接拿去去重，很容易留下重复记录，或者合并本来需要分别研究的对象。本节用 RDKit 把结构字符串读成分子图，再从图中生成可检查的表格。完成后，你可以逐个查看原子及其邻居，核对分子式和质量，寻找指定官能团，并解释某次去重为什么合并了两条记录。

这里选择两组彼此补充的例子。第一组是两端为羟基的乙二醇系列，从乙二醇、二甘醇一直排到含六个乙二醇单元的分子。每增加一个单元，碳、氢、氧的数量都有明确变化，适合检查程序算出的质量是否合理。第二组包括乳酸的两种指定构型、构型未指定的乳酸、乳酸根，以及苯的两种写法。它们把“字符串不同”“化学组成不同”和“结构信息不同”分开，让去重规则有具体对象。所有性质数值都由这些明确定义的分子图计算；接入实验数据时，还需要把温度、溶剂、浓度和测量方法放在独立列里。

RDKit 中的 `Mol` 可以理解为一本分子的连接名册。名册记录哪些原子存在、谁与谁相连、连接是什么键，以及电荷和立体化学等属性。二维结构图是这份名册的一种排版，SMILES 是它的一种文字写法，CSV 则适合存放从名册提取的标量结果。先建立这个对象关系，后面的函数就有了共同目的：读入图、检查图、描述图，再将结果与原来的记录对应起来。

## 读懂 SMILES：括号、环和省略的氢

从 `CC(O)C(=O)O` 开始读，可以把自己想象成沿着分子连接关系走一遍的人。第一个 `C` 建立一个碳，第二个 `C` 与它相连；括号中的 `O` 表示从当前的第二个碳伸出一条支路，括号结束后回到主路径。接着读到另一个 `C`，`(=O)` 表示它向一个氧形成双键，最后的 `O` 再与这个碳形成单键。六个字母建立六个非氢原子，括号负责指路，等号负责说明键型。图中的原子索引从 0 开始，恰好可以逐项对照读取顺序。

图上没有把所有氢都画出来，分子里却仍然有氢。对于这里常见的中性碳和氧，RDKit 根据元素、已连接的键和价态规则补足氢数。例如第一个碳只与一个碳形成单键，带三个氢；第二个碳已有三个单键，带一个氢；形成羰基的碳已有两个单键和一个双键，不再带氢。两个羟基氧各有一个氢，羰基氧没有氢，加起来得到 C₃H₆O₃。`GetNumHeavyAtoms()` 返回 6，`Chem.AddHs(mol).GetNumAtoms()` 返回 12。前者数非氢原子，后者把氢作为独立节点加入图以后再数全部原子，两者回答的是不同计数问题。

![从同一个乳酸分子追踪 SMILES 分支、原子索引、氢数与规范表示；1988 年的线性结构表示思想落实为可核对的连接名册。](https://ml-biomat.com/static/tutorials/python-scientific/figures/015faf0aafdb7ddbe3f60562.svg?v=015faf0aafdb)

图 1从同一个乳酸分子追踪 SMILES 分支、原子索引、氢数与规范表示；1988 年的线性结构表示思想落实为可核对的连接名册。

David Weininger 在 1988 年发表的 SMILES 论文，把分子连接关系编码为便于计算机处理的一行文字。它解决的一个实际问题，是让结构能像其他数据一样被存储、传送和搜索。上图把今天的一次读取操作与这个思想联系起来：换一个起点走遍乳酸，可以写出 `OC(=O)C(O)C`，连接关系仍然相同。规范化算法为同一套已保留的图属性选择一致的输出顺序，所以这两种写法在本例中得到相同规范 SMILES。原子索引却依赖当前对象的建立顺序；合并两个来源的数据时，需要做原子映射，不能仅凭“原子 3”认定它们在化学上对应。

环的写法也遵循连接关系。苯的 `c1ccccc1` 中，小写 `c` 表示芳香碳，两次出现的数字 1 要求把对应位置连接起来，数字本身不代表新原子。输入 `C1=CC=CC=C1` 则先明确单双键，RDKit 在化学检查过程中识别其芳香性，最终也输出 `c1ccccc1`。芳香性是作用在分子图上的规则，不由图片画成圆圈还是交替双线决定。处理复杂稠环、金属配合物或特殊价态时，应进一步查看相应的芳香性和价态模型；本节用常见有机分子把基本操作讲清楚。

连接名册还可以写成矩阵：行和列都按同一组原子索引排列，有键的位置填 1，没有键的位置填 0。乳酸的第 1 行，在第 0、2、3 列为 1，正好对应那个碳的三个重原子邻居。因为同一条普通共价键同时连接两端，矩阵关于对角线对称；没有原子与自身成键时，对角线为 0。把这一行相加得到的是重原子邻居数 3，氢仍在原子属性里，因此不能把这个数当作碳的全部价态。若需要区分单、双键，可以使用包含键级的矩阵或直接读取键对象。页面先展示 0/1 连接矩阵，便于把每个着色格子与分子图中的一条边对应。

## 从输入记录到可追踪的结构表

`Chem.MolFromSmiles()` 不只是把字符切开。它会建立原子和键，并进行价态、芳香性等化学检查。示例特意加入 `C(C)(C)(C)(C)C`：中间那个未标电荷的碳被连上五个单键，违反这里的中性碳价态规则，返回值是 `None`。如果紧接着调用分子量函数，错误会出现在远离原始输入的位置。更清楚的做法，是在读取后立即检查结果，将原始编号、原始字符串和未通过的原因保留在同一行。于是 13 行输入形成 12 行有效结构和 1 行明确待修的结构，不会因为跳过一行而悄悄改变样本数。

一个有用的结构表至少保留三种信息：来源记录的标识、原始表示，以及程序建立的规范表示。标识用于关联实验记录，原始表示用于回看输入，规范表示用于按指定规则比较结构。它们承担的任务不同，所以规范化以后仍保留原始字符串。本例的 CSV 还列出分子式、平均摩尔质量、单同位素质量、原子数、形式电荷和几种结构描述符。列名直接带上单位，例如 `mass_g_mol` 与 `tpsa_A2`，这样在 pandas 中合并数据或绘图时，列名仍提醒我们数值是什么。

CSV 善于存表格，SDF 则能保存原子、键、二维坐标和分子属性。代码把有效分子同时写入 SDF，然后重新读取，将读回的规范异构 SMILES 与写出前逐项比较。这相当于把包裹拆开再点一遍内容：文件存在只能说明写出了某些字节，结构往返一致才说明本例关心的连接和指定构型保留下来了。这里使用二维坐标作为结构展示；坐标由排版算法生成，键在图上画得长一点或短一点，不应当拿来测量真实键长。需要分子构象和能量时，要另行建立三维结构及相应计算模型。

还要区分“能被程序读入”和“正是自己要研究的物质”。一个写错连接位置的 SMILES 可能完全满足价态规则，程序会顺利建立另一个分子。对于刚接入的数据，最好把几条代表性记录画出来，并与预期的官能团、端基和电荷逐一比较。这里的质量检查能够发现漏掉某种原子的错误，却无法区分分子式相同的结构异构体；官能团匹配进一步检查局部连接，立体信息则补上空间构型。这几层检查相互补充，每层都有清楚的问题，阅读结果时也就能定位某次不一致发生在哪里。

## 先用能手算的质量，检查自动生成的描述符

一个描述符，就是把分子图的某个方面压缩成一个数。最容易检查的是平均摩尔质量：按分子式数清每种元素的原子，再乘以相应原子量并相加。本节使用 RDKit 的平均原子量约定，碳、氢、氧分别取 12.011、1.008、15.999，对应计算得到的摩尔质量单位为 g/mol。以乙二醇 C₂H₆O₂ 为例，两个碳贡献 24.022，六个氢贡献 6.048，两个氧贡献 31.998，合计 62.068 g/mol。代码对全部六个系列分子做同样的独立计数核对，而不是把库输出再次抄写为预期值。

$$
M=\sum_e N_e A_e,\qquad M(n)=(44.053n+18.015)\ \mathrm{g\,mol^{-1}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | 指定分子的平均摩尔质量，g/mol |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | 元素种类的索引，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/2244f89c20614334f7d67053.svg) | 一个分子中元素 e 的原子数，无量纲整数 |
| ![Formula](https://ml-biomat.com/static/agent-math/db201892debabce52fc649b2.svg) | 元素 e 按平均原子量换算的摩尔质量贡献，g/mol |
| ![Formula](https://ml-biomat.com/static/agent-math/acf5fc4aba87dc0808b830d5.svg) | 对分子中各元素的贡献求和 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | HO–(CH₂CH₂O)ₙ–H 中的重复单元数，本例为 1–6，无量纲 |

每个重复单元含 C₂H₄O，贡献 2×12.011+4×1.008+15.999=44.053 g/mol；端基余量 H₂O 贡献 18.015 g/mol。n=3 时为 C₆H₁₄O₄，质量 3×44.053+18.015=150.174 g/mol，与 RDKit 输出逐项核对。这是确定分子的原子计数，不包含链长分布平均。

系列分子的端基需要一起数。结构写成 HO–(CH₂CH₂O)ₙ–H 时，重复部分贡献 n 份 C₂H₄O，两个端部合起来额外贡献 H₂O，所以整个分子式为 C₂ₙH₄ₙ₊₂Oₙ₊₁。式中的 H₂O 是原子计数得到的端基余量，并不表示溶液里还混入了一分子水，也不指明某条合成路线。每增加一个单元，摩尔质量增加 44.053 g/mol；n 从 1 到 6，质量从 62.068 增到 282.333 g/mol。这个六点序列的每一点对应一个确定分子。商业聚乙二醇样品通常包含不同链长的分布，讨论它的数均、重均分子量时，需要把各链长的数量或质量分数也纳入计算。

`ExactMolWt` 的含义要与 `MolWt` 分开。前者通常使用指定同位素或各元素最常见同位素的精确质量，返回单同位素质量，以 Da 表示；后者使用平均原子量。乙二醇在这里得到 62.036779432 Da 与 62.068 g/mol，这个数值差异来自定义。质谱中的峰还涉及具体离子、加合物和电荷数，不能把某个中性分子的质量直接当成所有谱峰的位置。结构表同时保留这两列，是为了让后续计算有明确起点。

![六个端基确定的分子，各描述符保留自己的坐标与单位。橙色加号是按分子式计算的质量；末端供体数保持不变，受体数随内部醚氧增加。](https://ml-biomat.com/static/tutorials/python-scientific/figures/c53abf0f25b837aa2be9df60.svg?v=c53abf0f25b8)

图 2六个端基确定的分子，各描述符保留自己的坐标与单位。橙色加号是按分子式计算的质量；末端供体数保持不变，受体数随内部醚氧增加。

另外几列描述符让我们看见同一系列的不同变化。氢键供体 HBD 统计能以合适氢参与氢键的位点；这个系列一直有两个末端羟基，因此供体数维持 2。氢键受体 HBA 依照化学规则识别可以接受氢键的原子环境，随着中间醚氧增多，从 2 增到 7。这里数的是位点，不是分子在水中某一时刻实际形成的氢键数。拓扑极性表面积 TPSA 由原子环境片段贡献加和得到，单位是 Å²；它随系列增长，从 40.46 增至 86.61 Å²。它是一种结构描述符，不需要先生成三维构象，也不等于把某个三维分子外壳的面积直接量出来。

## 相同质量，还要继续看构型、电荷和分组规则

乳酸的中间碳连接四种不同的基团，可以形成互为镜像的空间构型。手套是常用的类比：左、右手套的组成和连接安排相似，却无法只靠平移和旋转完全重合。SMILES 中的 `@` 与 `@@` 用局部邻居顺序描述这种区别；它们并不是可以脱离字符串上下文直接翻译成 R 或 S 的符号。本例由 RDKit 分配 CIP 构型，`C[C@H](O)C(=O)O` 得到 S，另一个得到 R。图中楔形键说明空间朝向，普通二维折线承担其余连接关系。

![乳酸构型、质子化状态与苯的两种写法，展示不同层次的结构信息。表中数字是在相应比较规则下得到的不同键数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/747aa170dc7a43f0dfb505cf.svg?v=747aa170dc7a)

图 3乳酸构型、质子化状态与苯的两种写法，展示不同层次的结构信息。表中数字是在相应比较规则下得到的不同键数。

两种指定构型的乳酸具有相同分子式、相同摩尔质量，本节选用的 HBD、HBA、TPSA 和片段 logP 也相同。因此，拿这几列数值当作结构身份证，会把它们合并。保留立体信息的规范 SMILES 则将两者分开；构型未指定的第三条乳酸记录还应单独保留，因为“没有填写构型”表示信息状态，并不自动表示等量的两种构型混合物。若研究问题确实只比较连接骨架，可以显式选择 `isomericSmiles=False`，并在结果表中保留这项选择。这个选项也会省略同位素标记；本例没有指定同位素，所以数量变化全部来自立体信息。若要保留同位素而只忽略构型，应先复制分子，调用 `Chem.RemoveStereochemistry()`，再以保留异构信息的方式输出。本例 12 条有效记录按异构 SMILES 有 11 个键，忽略立体信息后有 9 个键；数量变化来自两种苯写法合并，以及三条乳酸记录在第二种规则下合并。

乳酸变成乳酸根时，还发生了组成和电荷变化。酸性羟基失去一个质子，C₃H₆O₃ 变成 C₃H₅O₃⁻，形式电荷从 0 变成 −1，平均摩尔质量少了约 1.008 g/mol。HBD 从 2 变成 1，HBA 从 2 变成 3，原因是羧酸与羧酸根采用不同的原子环境规则。形式电荷是图中按电子归属约定记录的整数，不是计算得到的每个原子的实际部分电荷。处理不同 pH 条件下的实验时，要把结构的质子化状态与实验条件对应；单纯进行规范化不会自动替你选择溶液中的主要形态，也不会自动把盐、互变异构体或全部质子化状态视为同一记录。

片段模型 logP 也需要这样读。其物理背景是某个中性溶质在辛醇和水两相平衡时的浓度比，取十为底的对数。RDKit 的 `MolLogP` 根据原子片段规则估算这个量，而图上显示的是计算结果。乙二醇系列从约 −1.029 变到 −0.946，提示在这套片段模型下数值变化很小；用一个宽度只有 0.1 的纵轴看，仍会出现明显上升的线，因此读趋势时也要读坐标范围。对带电乳酸根，程序同样能给出片段值，研究 pH 相关的两相分配时则要进一步处理各形态比例与分配系数，使用与实验定义一致的 logD 等量。

$$
P=\frac{c_{\mathrm{oct}}}{c_{\mathrm{water}}},\qquad \log P=\log_{10}P
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 中性溶质在平衡两相间的分配系数，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/183d49ffc49fec8f7907e9d8.svg) | 辛醇相中该中性溶质的浓度，例如 mol/L |
| ![Formula](https://ml-biomat.com/static/agent-math/cd4e6f8a69162522cc831012.svg) | 水相中同一中性溶质的浓度，使用与分子相同的单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | 以 10 为底的对数运算 |

分子和分母采用相同浓度单位，所以比值无量纲。若两相浓度分别为 0.01 与 0.1 mol/L，则 P=0.1，logP=−1。RDKit 给乙二醇的片段模型值为 −1.029，对应 10^(−1.029)≈0.0935；这是由结构模型估算的分配量，图中各点均采用相同计算定义。

## 完整程序：保留记录，再逐层生成结果

程序的 `inputs()` 用简短规则构造六个乙二醇系列分子，随后加入身份比较组。`process()` 是每条记录经过的主要步骤：解析字符串，检查是否成功，生成二维坐标和立体化学标签，遍历原子，匹配子结构，计算描述符。每个原子都生成一个字典，保留索引、元素、氢数、电荷、相邻原子和已分配的 R/S 标签。把这些小字典放进列表，可以在原子表中逐行查看；把整分子描述符放在外层字典，则可以直接写成 CSV。这种层次与数据本身的层次一致：一张分子表含多个分子，一个分子又含多个原子。

查找官能团使用 SMARTS。它与 SMILES 长得相似，但承担的是匹配规则。`[OX2H]` 在这里寻找连接数为 2、带一个氢的氧；`[OD2]([#6])[#6]` 寻找与两个碳连接的二配位氧，捕捉系列中的醚氧环境。匹配返回的是原子索引元组，可以直接用于高亮图中的相应部分。一次羧基匹配含三个原子，因而“匹配数”和“高亮原子数”应分别统计。只需羟基规则就能解释为什么链变长后末端数仍为 2；再切换醚基规则，就能追踪新增单元带来的内部连接。

### 完整结构解析、表格与科学绘图程序

在同一脚本中读取分子图、保留无效记录、匹配官能团、生成描述符，并核对分子式质量及 SDF 往返结果。

```
"""Build molecular identity tables and figures with RDKit.

Run: python main.py --output results --language en
All molecular inputs are defined below; no network service is required.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from rdkit import Chem, RDLogger, rdBase
from rdkit.Chem import Descriptors, Lipinski, rdDepictor, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D


BLUE, ORANGE, GREEN, INK = "#235b89", "#bf5635", "#177d72", "#192b3a"
PATTERNS = {
    "hydroxyl": "[OX2H]",
    "ether": "[OD2]([#6])[#6]",
    "carboxyl": "[CX3](=[OX1])[OX2H1,O-]",
    "aromatic": "a",
}



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def inputs():
    rows = [{"id": f"EG{n}", "smiles": "O" + "CCO" * n, "n": n,
             "zh": f"乙二醇系列 n={n}", "en": f"Glycol series n={n}"}
            for n in range(1, 7)]
    rows.extend([
        {"id": "LA1", "smiles": "C[C@H](O)C(=O)O", "zh": "乳酸：指定构型 1", "en": "Lactic acid: stereo 1"},
        {"id": "LA2", "smiles": "C[C@@H](O)C(=O)O", "zh": "乳酸：指定构型 2", "en": "Lactic acid: stereo 2"},
        {"id": "LA?", "smiles": "CC(O)C(=O)O", "zh": "乳酸：构型未指定", "en": "Lactic acid: unspecified"},
        {"id": "LAC", "smiles": "CC(O)C(=O)[O-]", "zh": "乳酸根：构型未指定", "en": "Lactate: unspecified"},
        {"id": "BZ1", "smiles": "c1ccccc1", "zh": "苯：芳香写法", "en": "Benzene: aromatic input"},
        {"id": "BZ2", "smiles": "C1=CC=CC=C1", "zh": "苯：单双键写法", "en": "Benzene: Kekule input"},
        {"id": "BAD", "smiles": "C(C)(C)(C)(C)C", "zh": "五键中性碳测试", "en": "Neutral five-bond carbon test"},
    ])
    return rows


def depiction(mol, highlight=()):
    drawer = rdMolDraw2D.MolDraw2DSVG(640, 360)
    opt = drawer.drawOptions()
    opt.addAtomIndices = True
    opt.baseFontSize = 0.85
    opt.minFontSize = 20
    opt.maxFontSize = 28
    opt.padding = 0.13
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, highlightAtoms=list(highlight),
                                     highlightAtomColors={i: (0.99, 0.78, 0.36) for i in highlight})
    positions = [[drawer.GetDrawCoords(i).x, drawer.GetDrawCoords(i).y]
                 for i in range(mol.GetNumAtoms())]
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    svg = svg[svg.find("<svg"):]
    return svg, positions


def process(row):
    # Keep a rejected row visible in the output table instead of silently dropping it.
    with rdBase.BlockLogs():
        mol = Chem.MolFromSmiles(row["smiles"])
    if mol is None:
        return {**row, "valid": False, "reason": "invalid neutral carbon valence"}, None
    rdDepictor.Compute2DCoords(mol)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    atoms = [{"index": a.GetIdx(), "element": a.GetSymbol(),
              "hydrogens": a.GetTotalNumHs(), "charge": a.GetFormalCharge(),
              "aromatic": a.GetIsAromatic(),
              "neighbors": [x.GetIdx() for x in a.GetNeighbors()],
              "cip": a.GetProp("_CIPCode") if a.HasProp("_CIPCode") else None}
             for a in mol.GetAtoms()]
    hits = {name: [list(match) for match in mol.GetSubstructMatches(Chem.MolFromSmarts(pattern))]
            for name, pattern in PATTERNS.items()}
    drawings = {}
    for pattern in ["none", *PATTERNS]:
        indices = sorted({i for match in hits.get(pattern, []) for i in match})
        drawings[pattern], xy = depiction(mol, indices)
    canonical = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
    plain = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=False)
    restored = Chem.MolFromSmiles(canonical)
    assert restored is not None
    assert Chem.MolToSmiles(restored, isomericSmiles=True) == canonical
    result = {**row, "valid": True, "canonical": canonical, "without_stereo": plain,
              "formula": rdMolDescriptors.CalcMolFormula(mol),
              "mass_g_mol": Descriptors.MolWt(mol),
              "monoisotopic_mass_Da": Descriptors.ExactMolWt(mol),
              "heavy_atoms": mol.GetNumHeavyAtoms(),
              "total_atoms_with_H": Chem.AddHs(mol).GetNumAtoms(),
              "formal_charge": Chem.GetFormalCharge(mol),
              "hbd": Lipinski.NumHDonors(mol), "hba": Lipinski.NumHAcceptors(mol),
              "tpsa_A2": rdMolDescriptors.CalcTPSA(mol),
              "logP_model": Descriptors.MolLogP(mol),
              "atoms": atoms, "bonds": Chem.GetAdjacencyMatrix(mol).tolist(),
              "matches": hits, "drawings": drawings, "xy": xy}
    return result, mol


def molecule_image(ax, mol, highlighted=()):
    drawer = rdMolDraw2D.MolDraw2DCairo(800, 380)
    opt = drawer.drawOptions()
    opt.addAtomIndices = True
    opt.minFontSize = 20
    opt.maxFontSize = 29
    opt.padding = 0.12
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, highlightAtoms=list(highlighted),
                                     highlightAtomColors={i: (.99, .78, .36) for i in highlighted})
    drawer.FinishDrawing()
    ax.imshow(plt.imread(io.BytesIO(drawer.GetDrawingText()), format="png"))
    ax.axis("off")


def figures(records, mols, out, language):
    zh = language == "zh"
    tr = lambda cn, en: cn if zh else en
    plt.rcParams.update({"font.family": available_plot_fonts() if zh else ["DejaVu Sans"],
        "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 14,
        "figure.facecolor": "#faf9f6", "axes.spines.top": False,
        "axes.spines.right": False, "svg.fonttype": "path"})
    byid = {r["id"]: r for r in records}
    def save(fig, name):
        for ext in ("svg", "png"):
            fig.savefig(out / f"{name}-{language}.{ext}", dpi=165, bbox_inches="tight")
        plt.close(fig)

    # F1: the same numbered molecular graph explains the branch tokens and atom table.
    fig = plt.figure(figsize=(13, 8.2), layout="constrained")
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], width_ratios=[1.15, 1])
    ax = fig.add_subplot(gs[0, 0])
    molecule_image(ax, mols["LA?"], [2, 3, 4, 5])
    ax.set_title(tr("同一张图：6 个重原子，6 个隐含氢", "One graph: 6 heavy atoms and 6 implicit H"))
    ax = fig.add_subplot(gs[0, 1]); ax.axis("off")
    ax.text(0, .95, "CC(O)C(=O)O", fontsize=23, family="monospace", color=BLUE, va="top")
    lines = [tr("0–1–3–5：主路径", "0–1–3–5: main traversal"),
             tr("(O)：在原子 1 处分支到原子 2", "(O): branch from atom 1 to atom 2"),
             tr("(=O)：原子 3 与原子 4 形成双键", "(=O): double bond from atom 3 to atom 4"),
             tr("括号控制连接；不增加原子", "Parentheses control connectivity"),
             tr("H 由价态补足，保存在原子属性中", "Hydrogens follow the atom valences")]
    for k, line in enumerate(lines): ax.text(0, .70-k*.125, line, fontsize=14, color=INK)
    ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
    r = byid["LA?"]
    table = ax.table(cellText=[[a["index"], a["element"], a["hydrogens"],
                               ", ".join(map(str, a["neighbors"]))] for a in r["atoms"]],
                     colLabels=[tr("索引", "Index"), tr("元素", "Element"), "H", tr("邻接原子", "Neighbors")],
                     loc="center", cellLoc="center", bbox=[0, .06, 1, .9])
    table.auto_set_font_size(False); table.set_fontsize(14)
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor("#d6e1e5")
        if i == 0: cell.set_facecolor("#dce9ee")
    ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
    ax.text(0, .92, tr("1988：SMILES 把分子图写进一行文字", "1988: SMILES encodes a graph in one line"),
            fontsize=15, weight="bold", va="top")
    ax.text(0, .72, "CC(O)C(=O)O\nOC(=O)C(O)C", family="monospace", fontsize=20, color=BLUE, linespacing=1.6, va="top")
    ax.annotate("", xy=(.45, .32), xytext=(.45, .43), arrowprops={"arrowstyle": "->", "color": INK})
    ax.text(0, .25, tr("RDKit 规范表示：CC(O)C(=O)O", "RDKit canonical form: CC(O)C(=O)O"), fontsize=14)
    ax.text(0, .10, tr("不同遍历顺序 → 相同连接关系", "Different traversals → the same connectivity"), fontsize=14)
    save(fig, "graph-and-string")

    # F2: values have separate axes and retain their scientific units.
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
    series = [r for r in records if r.get("n")]
    n = np.array([r["n"] for r in series])
    mass = np.array([r["mass_g_mol"] for r in series])
    axes[0, 0].plot(n, mass, "o-", color=BLUE, lw=2.5)
    axes[0, 0].plot(n, 44.053*n+18.015, "+", color=ORANGE, ms=15, mew=2,
                    label=tr("按分子式加和", "Formula sum"))
    axes[0, 0].set_ylabel(tr("摩尔质量 / g mol⁻¹", "Molar mass / g mol⁻¹")); axes[0, 0].legend()
    for i in (0, 5): axes[0, 0].annotate(f"{mass[i]:.3f}", (n[i], mass[i]), xytext=(4, 8), textcoords="offset points")
    axes[0, 1].plot(n, [r["tpsa_A2"] for r in series], "o-", color=GREEN, lw=2.5)
    axes[0, 1].set_ylabel(tr("拓扑极性表面积 / Å²", "Topological polar surface area / Å²"))
    axes[1, 0].plot(n, [r["hba"] for r in series], "o-", lw=2.5, color=BLUE, label=tr("受体位点 HBA", "Acceptor sites HBA"))
    axes[1, 0].plot(n, [r["hbd"] for r in series], "s-", lw=2.5, color=ORANGE, label=tr("供体位点 HBD", "Donor sites HBD"))
    axes[1, 0].set_ylabel(tr("位点数", "Site count")); axes[1, 0].legend()
    axes[1, 1].plot(n, [r["logP_model"] for r in series], "o-", lw=2.5, color=ORANGE)
    axes[1, 1].set_ylabel(tr("片段模型 logP / 无量纲", "Fragment-model logP / dimensionless"))
    for ax in axes.flat:
        ax.set_xlabel(tr("链中乙二醇单元数 n", "Number of ethylene-glycol units n"))
        ax.set_xticks(n); ax.grid(alpha=.18)
    fig.suptitle(tr("明确端基的六个分子：HO–(CH₂CH₂O)ₙ–H", "Six molecules with defined end groups: HO–(CH₂CH₂O)ₙ–H"), fontsize=18)
    save(fig, "oligomer-descriptors")

    # F3: molecular identity depends on which structural attributes are retained.
    fig = plt.figure(figsize=(13, 8.2), layout="constrained")
    gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, .65])
    ids = ["LA1", "LA2", "LA?", "LAC", "BZ1", "BZ2"]
    for k, ident in enumerate(ids):
        ax = fig.add_subplot(gs[k//3, k%3]); r = byid[ident]
        molecule_image(ax, mols[ident])
        stereo = ",".join(a["cip"] for a in r["atoms"] if a["cip"])
        ax.set_title(r[language]+(f" ({stereo})" if stereo else ""), fontsize=14)
        ax.text(.5, -.02, f"{r['formula']}  |  {r['mass_g_mol']:.3f} g mol⁻¹\n{r['canonical']}",
                transform=ax.transAxes, ha="center", va="top", fontsize=12.5)
    ax = fig.add_subplot(gs[2, :]); ax.axis("off")
    cols = [tr("去重时保留的属性", "Attributes retained in the key"), tr("三种乳酸记录", "Three lactic-acid records"), tr("两种苯写法", "Two benzene inputs")]
    cells = [[tr("连接关系、键型、形式电荷、指定构型", "Connectivity, bond type, charge, specified stereo"), "3", "1"],
             [tr("连接关系、键型、形式电荷", "Connectivity, bond type, charge"), "1", "1"]]
    tab = ax.table(cellText=cells, colLabels=cols, cellLoc="center", bbox=[0, .03, 1, .65], colWidths=[.55, .25, .20])
    tab.auto_set_font_size(False); tab.set_fontsize(13)
    for (i, j), cell in tab.get_celld().items():
        cell.set_edgecolor("#d6e1e5")
        if i == 0: cell.set_facecolor("#dce9ee")
    save(fig, "identity-and-stereo")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    records, molecules = [], {}
    for row in inputs():
        result, mol = process(row); records.append(result)
        if mol is not None: molecules[row["id"]] = mol
    valid = [r for r in records if r["valid"]]
    columns = ["id", "smiles", "valid", "canonical", "without_stereo", "formula", "mass_g_mol",
               "monoisotopic_mass_Da", "heavy_atoms", "total_atoms_with_H", "formal_charge",
               "hbd", "hba", "tpsa_A2", "logP_model", "reason"]
    with (args.output / "structures.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    writer = Chem.SDWriter(str(args.output / "structures.sdf"))
    for r in valid:
        mol = molecules[r["id"]]; mol.SetProp("_Name", r["id"])
        mol.SetProp("input_smiles", r["smiles"]); writer.write(mol)
    writer.close()
    roundtrip = [m for m in Chem.SDMolSupplier(str(args.output / "structures.sdf")) if m is not None]
    assert len(roundtrip) == len(valid)
    assert [Chem.MolToSmiles(m, isomericSmiles=True) for m in roundtrip] == [r["canonical"] for r in valid]
    series = [r for r in valid if r.get("n")]
    mass_error = max(abs(r["mass_g_mol"]-(44.053*r["n"]+18.015)) for r in series)
    assert mass_error < 1e-10
    summary = {"rdkit_version": rdBase.rdkitVersion, "input_rows": len(records), "valid_rows": len(valid),
               "unique_isomeric": len({r["canonical"] for r in valid}),
               "unique_without_stereo": len({r["without_stereo"] for r in valid}),
               "formula_mass_max_error_g_mol": mass_error,
               "rows": [{k: v for k, v in r.items() if k not in ("drawings", "xy", "atoms", "bonds", "matches")} for r in records]}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.output / "lab-data.json").write_text(json.dumps({"records": records, "patterns": PATTERNS}, ensure_ascii=False), encoding="utf-8")
    figures(valid, molecules, args.output, args.language)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

在保存脚本的目录中运行下面的命令，结果目录会得到 `structures.csv`、`structures.sdf`、数值摘要和三幅图。CSV 保留那条无效输入及原因，SDF 则只写入 12 个成功建立的分子。读回检查核对 SDF 中的分子数和每个分子的规范异构 SMILES，独立质量检查核对六个系列分子的手算公式。代码生成的交互数据还包含原子坐标、索引和匹配结果，所以页面中的图、表和描述符来自同一次计算。更换输入时，应保留相同检查层次，再增加能够覆盖新化学类型的具体例子。

### 运行完整示例

中文图将 en 改为 zh；全部生成文件写入 results。

```
python main.py --output results --language en
```

阅读代码时，可以先沿一条记录走完流程，再看循环怎样推广到整张表。例如 EG3 输入为 `OCCOCCOCCO`，解析得到 10 个重原子；加上隐含氢后共 24 个原子，公式为 C₆H₁₄O₄。四个氧中两个位于末端、两个位于内部，因此羟基匹配为 2，醚氧环境匹配也为 2。由图提取的 HBD 为 2、HBA 为 4，质量为 150.174 g/mol。每一个结果都能回到这条结构上解释，之后再看 n=1 到 6 的变化，就能分清哪些是数量增长带来的必然变化，哪些依赖描述符所采用的化学规则。

## 把结构、原子表和去重结果放在一起检查

在实验中选中一个分子，左侧显示带原子编号的结构，右侧显示这个分子的原子表与邻接关系。移动原子索引，会同时标出结构中的位置、它的邻居以及表中对应行。原子索引只是当前结构对象内的地址；它使你能够追查某个属性究竟来自哪一个原子。切换官能团规则，可以把化学名称与真实匹配联系起来：先在 EG1 中找两个羟基，再换成 EG6，末端羟基数仍然是两个，内部醚氧匹配数则增加到五个。

下方描述符图让所有有效分子共用一套坐标。选择某一条乳酸记录时，三个中性乳酸条目落在相同的位置，可以通过图旁的记录表确认重叠的身份。打开或关闭“保留立体信息”，分组表随之更新；分子自身的结构图和质量不变，因为这个开关改变的是比较键，而不是发生了化学反应。再选中乳酸根，电荷、氢数和描述符同时变化，能看到另一个层次的区别。此时再回到两种苯输入，便可以用同一套检查解释：它们原文不同，但经过同一芳香性规则解析后属于相同的分子图。

## 结构身份实验台

选择分子和官能团，再移动原子索引；结构、连接矩阵、属性和分组表同步更新。分组开关改变比较规则，保留原始分子图。

黄色：模式匹配；蓝圈：选中原子；蓝虚圈：相邻原子。坐标用于二维排版。

[Figure: 分子连接矩阵](https://ml-biomat.com/tutorials/python-scientific/s04/#S04-matrix)

每行、每列对应同一组原子索引；蓝格表示存在一条键，白格表示没有键。矩阵不区分单键与双键。

[Figure: 分子质量与描述符对照](https://ml-biomat.com/tutorials/python-scientific/s04/#S04-scatter)

共用坐标保留数值尺度；同位置记录的编号并列显示。

将这种方法接到自己的结构表时，可以先挑一个容易手算的分子，逐项确认氢、电荷、分子式与单位，再检查重复记录是怎样分组的。若表格含多个片段，例如分子和对离子用点号连接，应为是否保留盐形式建立明确规则；若同时存在不同同位素或未指定构型，也应保留对应字段。RDKit 把这些操作组织成可以重复运行的计算，而决定比较对象的仍是具体研究问题。结构身份清楚以后，再与实验批次、性质和误差列连接，后面的统计分析才有稳定的基础。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S04.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [RDKit: Getting Started in Python](https://www.rdkit.org/docs/GettingStartedInPython.html)

   分子读写、原子操作、子结构匹配、描述符与官方开放教程。

   Greg Landrum documentation: CC BY-SA 4.0; RDKit software: BSD 3-Clause.
2. [The RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html)

   芳香性、SMILES 支持、立体化学与化学检查的具体规则。

   RDKit documentation; consult the page license and project license for reuse.
3. [Weininger (1988), SMILES: methodology and encoding rules](https://doi.org/10.1021/ci00057a005)

   SMILES 历史背景与原始方法论文，JCICS 28(1), 31–36。

   American Chemical Society journal article.
