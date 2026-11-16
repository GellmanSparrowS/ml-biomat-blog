# 把一个分子写进计算机

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l05/
Language: zh-CN

从一条短PEG认识原子身份、连接、参数与构象，再把分子放进水里。

## 从一条软链开始，认识分子的三种身份

一条细绳可以绕在手指上，也可以拉直放在桌面上。外形变了，连接关系却仍然相同：绳子的中间部分没有因此跑到末端，两个相邻位置也没有自动分开。高分子链有相似的一面。它在水中会弯曲、转动，受到拉力后可能逐渐伸展，而哪些原子通过化学键相连，通常保持不变。要把这样的对象放进计算机，我们既要说明“它是什么”，又要说明“它此刻是什么形状”。本讲就从这两个问题出发，把前面能够自由移动的粒子，组织成一条有明确化学身份的分子。

我们使用一条两端带羟基的短聚乙二醇，英文缩写为PEG。它的重复部分由碳、氢、氧组成，骨架上反复出现碳—碳—氧的连接。许多读者可能在亲水涂层、药物配方或水凝胶材料中见过这个名称。这里选择八个重复单元的短链，是为了让连接、末端和周围水分子的关系都能在一个小体系中看清楚。短链的分子式是C₁₆H₃₄O₉，共有五十九个显式原子；改变链长以后，端基所占比例和可探索的构象都会随之改变，因此这个具体分子始终是我们讨论的对象。

可以用三张互相配合的卡片理解它。第一张是身份卡，记录原子属于哪一类、质量多大、携带多少部分电荷；第二张是连接卡，记录哪些原子成键、哪些三原子组合有键角、哪些四原子组合有扭转作用；第三张是位置卡，记录这些原子当前处在什么地方。身份与连接共同规定一个可计算的模型，位置则是这个模型在某一时刻的构象。把三张卡片混在一起，往往会造成误解：画得很近的两个原子未必有化学键，写着相同元素名称的两个原子也未必采用同一套参数。

本讲沿着一条完整的准备路线学习这些信息。先读一个只有三个原子的水分子模板，弄清楚坐标、类型、电荷和连接怎样配合；再把相同思路用于五十九原子的PEG，检查其连接图和参数；最后将它加入已经准备的水中，清除不合适的重叠并观察体系如何调整。页面中的Python程序会把模板中的真实信息画出来，运行结果则展示加入分子后的实际记录。这样，输入文件里的数字和最终画面之间就有了一条可以追踪的联系。

理解连接关系还会为生物大分子打下基础。蛋白质具有由氨基酸连接形成的骨架，糖链的分支位置会改变整体结构，核酸中的连接方向影响序列和构象。它们的化学细节各不相同，但都需要分清原子身份、连接顺序和空间形状。PEG提供了一个容易观察的起点：骨架规则，末端清楚，链条又足够柔软，能让我们看到同一个连接图怎样对应许多不同的三维构象。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s1)

图 1 · 重复结构式说明组成，连接与位置分别说明分子身份和当前构象。

## 为什么“连在一起”曾经是一个科学问题

今天画一条高分子链时，人们很自然地用化学键把重复单元连起来。在高分子科学早期，这种解释却需要与其他物质结构观念竞争。大分子材料表现出的高黏度、缓慢扩散和特殊溶液行为，究竟来自许多小分子的聚集，还是来自真正很长的共价连接？两种想法都可能画出一个很大的团块，但它们对稀释、化学变化和分子运动的解释不同。外形相似，并不意味着内部连接相同，这正是我们现在读分子模型时需要保留的判断。

施陶丁格在1920年的《论聚合》中提出长链共价结构的观点，将高分子问题与化学连接联系起来。对本讲而言，这个历史转变最有用的启发，是把“一个分子”理解成有明确连接的对象，而不是屏幕上碰巧靠在一起的一群球。图中的两种组织方式因此可以具有相近的外形，却有不同的运动条件：小分子聚集体里的成员可以彼此离开，固定连接的链则需要通过键长、键角和扭转共同调整形状。[Staudinger，1920](https://doi.org/10.1002/cber.19200530627)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s2)

图 2 · 高分子结构观念的概念对照：相似外形可以对应不同连接关系。

在当前分子动力学模型中，连接卡不会在每一步重新猜测。程序根据已经指定的键表计算相关能量，让相连原子围绕适合的距离运动，也让相邻键能够弯曲、扭转。两个原子偶然接近时，非键作用可以改变它们的受力，却不会自动把它们加入键表。于是，“链在水里伸展”是这个模型可以直接提出的问题，“单体怎样聚合成长链”则需要进一步定义成键过程以及相应的反应模型。研究对象中的动词不同，输入必须提供的信息也会改变。

再看“元素”和“原子类型”的区别。元素说明原子核的化学身份，例如碳或氧；原子类型则把它在特定力场中的局部环境与参数联系起来。PEG中间的醚氧连接两个碳，末端的羟基氧连接一个碳和一个氢，它们都是氧，却处在不同环境中。这个例子的标签分别采用OE和OAlc，因此参数表能给它们不同的电荷环境与非键作用。水氧又使用OW。标签帮助人追踪模型中的分类，真正的数值仍由质量、电荷和相互作用定义共同给出。

原子编号承担另一项任务。编号像一本通讯录里的唯一索引，用来指出“究竟是哪一个原子”；类型像职业分类，可以由许多人共享。分子编号又像家庭编号，用来把属于同一个分子的原子组织起来。这三者不能互相替代。许多氢原子可以共享同一类型，却必须具有各自的原子编号；一个分子也可以包含多种类型。后来读取轨迹时，按原子编号找到同一个对象，按类型选择一类对象，按分子编号重组一整个对象，便成为三个目的清楚的操作。

因此，建模时最先整理的并不是一幅漂亮图片，而是一组可以相互核对的关系。分子式回答有哪些元素和多少原子，连接图回答它们怎样组成分子，参数回答这些连接和接近会产生怎样的能量变化，坐标回答当前几何。每一层都能帮助发现另一层里的问题。例如，总原子数符合分子式，却可能仍有一个氢连到了错误的氧上；键表完全正确，也可能配上一组过于拥挤的起始坐标。后面的检查会逐层展开，而不只依靠一个总数。

## 从三个原子读懂一份分子模板

先打开本例的water.mol。它在开头列出三个原子、两条键和一个角，然后分别给出Coords、Types、Charges、Bonds和Angles区块。Coords中的第一列是模板内部编号，后面三列是位置；Types为这些编号赋予原子类型；Charges写出电荷；Bonds和Angles通过相同编号建立连接。文件没有要求我们按肉眼距离猜测哪两点属于一个水分子，而是把这种关系明确保存下来。程序随后可以复制这个模板，为每个副本分配系统中的身份。

### 完整柔性水分子模板

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

3 atoms
2 bonds
1 angles

Coords

1 0 0 0 # H2O O
2 1.012 0 0	# H2O H
3 -0.4 0.929 0 # H2O H

Types

1 OW
2 HW
3 HW

Charges

1 -0.82 # H2O O (SPC/Fw)
2 0.41 # H2O H (SPC/Fw)
3 0.41 # H2O H (SPC/Fw)

Bonds

1 OW-HW 1 2
2 OW-HW 1 3

Angles

1 HW-OW-HW 2 1 3
```

编号连接位置、类型、电荷与几何项。

这个模板让氧位于原点，一个氢在氧的一侧，另一个氢沿不同方向放置。编号一为OW，编号二和三为HW；两条键分别连接一与二、一与三。角记录的顺序是二、一、三，中间的一就是角的顶点。用手握住两根铅笔，让它们的一端相遇，铅笔之间的张角就对应这个三原子角。改变张角时，两个氢之间的距离也会变化，即使两条氧—氢键的长度暂时不变。这说明键长与键角描述了不同的几何自由度。

Charges中，氧为−0.82，两个氢分别为+0.41，单位采用元电荷e。把同一分子的电荷逐项相加得到零，说明这个模型水分子整体电中性；但不同位置仍保留正负电荷，因此它可以随取向与其他分子相互作用。一个体系的电荷核对也按同样方式进行。加入带电末端、离子或不同质子化状态时，局部变化会反映在总电荷中。总和是一个简单而有用的检查，同时还要确认电荷是否分配给了正确的原子。

逐原子相加得到分子总电荷式 1

![逐原子相加得到分子总电荷](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Q | 分子或指定原子组的总电荷 | e |
| qᵢ | 第i个原子的部分电荷 | e |
| N, i | 原子总数与求和编号 | 1 |
| Σ, = | Σ将编号一至N的电荷相加；等号定义总和 | 1 |

怎样理解电荷是可逐项相加的量；正负号同时保留，局部正负分离可以与整体中性共存。

算一个例子SPC/Fw水的电荷为−0.82、+0.41、+0.41，单位为e，因此Q=0。PEG模板中59个电荷之和在浮点舍入精度内为零。

使用条件部分电荷属于指定模型；电中性检查与电荷在空间中的分布各有用途。

PEG模板把相同组织方式扩展到五十九个原子。它具有五十八条键、一百零四个角和一百一十六个二面角记录。对于一张连通、没有环的原子连接图，边数比顶点数少一；因此五十九个原子与五十八条键是一个值得核对的关系。这里说的“没有环”是连接图的性质，和链在空间中弯成一个近似圆圈不同。弯曲的线可以看起来像圈，只要末端没有成键，连接图仍是一棵树。我们的程序会真正遍历键表，检查连通性，而不把这一数量关系单独当作充分条件。

### 完整PEG分子模板

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PEG molecule

59 atoms
58 bonds
104 angles
116 dihedrals

Coords

1 -3.0661409 -3.1122069 -1.2331413
2 -3.0905955 -3.1901295 -0.3069935
3 -1.7871211 -3.4628029 0.1677571
4 -1.7892607 -3.9757321 1.1640826
5 -1.4364998 -2.4400568 0.4558979
6 -0.9585523 -4.2486658 -0.9052389
7 -1.5905948 -5.0815649 -1.3120303
8 -0.0526673 -4.7456765 -0.4700128
9 -0.63208 -3.3539891 -2.0115812
10 0.2145577 -4.0010762 -2.9207664
11 -0.3729619 -4.5629487 -3.6922491
12 1.0240761 -4.5117416 -2.3388433
13 0.9711505 -2.8357534 -3.5251923
14 0.3408715 -1.9581318 -3.822669
15 1.6180273 -3.1186311 -4.3940263
16 1.8975644 -2.4613039 -2.5075514
17 3.0585685 -1.8075132 -3.006783
18 2.8443427 -0.8083913 -3.4607034
19 3.6249113 -2.4323449 -3.7466593
20 3.992363 -1.7272376 -1.8733916
21 4.9511518 -1.186389 -2.07637
22 4.254519 -2.795933 -1.6625937
23 3.423965 -1.0901105 -0.7496133
24 3.8947239 -1.659389 0.516987
25 3.9258208 -0.8841055 1.3251652
26 4.9554296 -2.0063238 0.4150401
27 3.0359709 -2.8971462 1.0103722
28 3.8185678 -3.6568248 1.2752906
29 2.4917984 -3.195833 0.0744643
30 2.0725911 -2.848428 2.0760021
31 1.638817 -1.4838974 2.5253139
32 2.5752075 -1.0062795 2.9080422
33 0.9012089 -1.6500344 3.3573053
34 0.8815328 -0.5306711 1.5538689
35 0.5519052 -1.1815579 0.7041188
36 1.6224746 0.2331944 1.1997508
37 -0.2989756 -0.0199954 2.1694908
38 -0.3033598 1.4095408 2.1280825
39 0.0521263 1.761717 1.1273303
40 0.4747811 1.7876458 2.8392599
41 -1.6030958 1.9523106 2.4553161
42 -1.5646386 2.9988577 2.8519616
43 -1.9732467 1.2583804 3.2576206
44 -2.5225735 1.8953969 1.3081864
45 -3.3669469 3.0741107 1.0973018
46 -3.0220368 3.8450892 1.8318384
47 -4.4858675 3.0095129 1.1439484
48 -3.0599689 3.6382723 -0.3005937
49 -3.982976 3.5193791 -0.9249329
50 -2.1988642 3.09917 -0.7700861
51 -2.7010767 5.025878 -0.199455
52 -1.3877664 5.5169363 -0.1698399
53 -0.8882234 5.1431508 -1.0995853
54 -0.935725 4.957068 0.6896982
55 -1.3304483 7.055419 0.0381237
56 -2.0611646 7.6166778 -0.601446
57 -0.3436857 7.3639388 -0.3955144
58 -1.5631742 7.5380082 1.3714558
59 -2.4256234 7.9039402 1.5299768

Types

1 H 
2 OAlc 
3 CPos 
4 HC 
5 HC 
6 C 
7 HC 
8 HC 
9 OE 
10 C 
11 HC 
12 HC 
13 C 
14 HC 
15 HC 
16 OE 
17 C 
18 HC 
19 HC 
20 C 
21 HC 
22 HC 
23 OE 
24 C 
25 HC 
26 HC 
27 C 
28 HC 
29 HC 
30 OE 
31 C 
32 HC 
33 HC 
34 C 
35 HC 
36 HC 
37 OE 
38 C 
39 HC 
40 HC 
41 C 
42 HC 
43 HC 
44 OE 
45 C 
46 HC 
47 HC 
48 C 
49 HC 
50 HC 
51 OE 
52 C 
53 HC 
54 HC 
55 CPos 
56 HC 
57 HC 
58 OAlc 
59 H 

Charges

1 0.211 
2 -0.328 
3 -0.019 
4 0.093 
5 0.093 
6 -0.063 
7 0.079 
8 0.079 
9 -0.295 
10 -0.021 
11 0.084 
12 0.084 
13 -0.023 
14 0.083 
15 0.083
16 -0.283 
17 -0.023 
18 0.083 
19 0.083 
20 -0.023 
21 0.083
22 0.083 
23 -0.283 
24 -0.023 
25 0.082 
26 0.082 
27 -0.023 
28 0.082 
29 0.082 
30 -0.283 
31 -0.023 
32 0.082 
33 0.082 
34 -0.023 
35 0.082 
36 0.082 
37 -0.283 
38 -0.023 
39 0.082 
40 0.083
41 -0.023 
42 0.083 
43 0.083 
44 -0.283 
45 -0.023 
46 0.083 
47 0.083
48 -0.021 
49 0.084 
50 0.084 
51 -0.295 
52 -0.063 
53 0.079 
54 0.079 
55 -0.019 
56 0.093 
57 0.093 
58 -0.328 
59 0.211 

Bonds

1 g18 13 16 
2 g18 16 17 
3 g18 20 23 
4 g18 23 24 
5 g18 27 30 
6 g18 30 31 
7 g18 34 37 
8 g18 37 38 
9 g18 41 44 
10 g18 44 45 
11 g18 48 51 
12 g18 51 52 
13 g18 6 9 
14 g18 9 10 
15 g26 17 20 
16 g26 24 27 
17 g26 31 34 
18 g26 38 41 
19 g27 10 13 
20 g27 3 6 
21 g27 45 48 
22 g27 52 55 
23 g4 10 11 
24 g4 10 12 
25 g4 13 14 
26 g4 13 15 
27 g4 17 18 
28 g4 17 19 
29 g4 20 21 
30 g4 20 22 
31 g4 24 25 
32 g4 24 26 
33 g4 27 28 
34 g4 27 29 
35 g4 3 4 
36 g4 3 5 
37 g4 31 32 
38 g4 31 33 
39 g4 34 35 
40 g4 34 36 
41 g4 38 39 
42 g4 38 40 
43 g4 41 42 
44 g4 41 43 
45 g4 45 46 
46 g4 45 47 
47 g4 48 49 
48 g4 48 50 
49 g4 52 53 
50 g4 52 54 
51 g4 55 56 
52 g4 55 57 
53 g4 6 7 
54 g4 6 8 
55 g56 2 3 
56 g56 55 58 
57 g71 1 2 
58 g71 58 59 

Angles

1 g102 14 13 16 
2 g102 15 13 16 
3 g102 2 3 4 
4 g102 2 3 5 
5 g102 21 20 23 
6 g102 22 20 23 
7 g102 23 24 25 
8 g102 23 24 26 
9 g102 30 31 32 
10 g102 30 31 33 
11 g102 35 34 37 
12 g102 36 34 37 
13 g102 37 38 39 
14 g102 37 38 40 
15 g102 4 3 5 
16 g102 4 3 6 
17 g102 44 45 46 
18 g102 44 45 47 
19 g102 5 3 6 
20 g102 52 55 56 
21 g102 52 55 57 
22 g102 56 55 57 
23 g102 56 55 58 
24 g102 57 55 58 
25 g12 1 2 3 
26 g12 13 16 17 
27 g12 20 23 24 
28 g12 27 30 31 
29 g12 34 37 38 
30 g12 41 44 45 
31 g12 48 51 52 
32 g12 55 58 59 
33 g12 6 9 10 
34 g13 10 13 16 
35 g13 16 17 20 
36 g13 17 20 23 
37 g13 23 24 27 
38 g13 3 6 9 
39 g13 30 31 34 
40 g13 31 34 37 
41 g13 37 38 41 
42 g13 38 41 44 
43 g13 44 45 48 
44 g13 45 48 51 
45 g13 51 52 55 
46 g13 9 10 13 
47 g14 11 10 12 
48 g14 14 13 15 
49 g14 18 17 19 
50 g14 21 20 22 
51 g14 25 24 26 
52 g14 28 27 29 
53 g14 32 31 33 
54 g14 35 34 36 
55 g14 39 38 40 
56 g14 42 41 43 
57 g14 46 45 47 
58 g14 49 48 50 
59 g14 51 52 53 
60 g14 51 52 54 
61 g14 53 52 54 
62 g14 7 6 8 
63 g14 7 6 9 
64 g14 8 6 9 
65 g15 2 3 6 
66 g15 3 6 7 
67 g15 3 6 8 
68 g15 52 55 58 
69 g15 53 52 55 
70 g15 54 52 55 
71 g51 10 13 14 
72 g51 10 13 15 
73 g51 11 10 13 
74 g51 12 10 13 
75 g51 16 17 18 
76 g51 16 17 19 
77 g51 17 20 21 
78 g51 17 20 22 
79 g51 18 17 20 
80 g51 19 17 20 
81 g51 24 27 28 
82 g51 24 27 29 
83 g51 25 24 27 
84 g51 26 24 27 
85 g51 28 27 30 
86 g51 29 27 30 
87 g51 31 34 35 
88 g51 31 34 36 
89 g51 32 31 34 
90 g51 33 31 34 
91 g51 38 41 42 
92 g51 38 41 43 
93 g51 39 38 41 
94 g51 40 38 41 
95 g51 42 41 44 
96 g51 43 41 44 
97 g51 45 48 49 
98 g51 45 48 50 
99 g51 46 45 48 
100 g51 47 45 48 
101 g56 49 48 51 
102 g56 50 48 51 
103 g56 9 10 11 
104 g56 9 10 12 

Dihedrals

1 g23 1 2 3 6 
2 g23 10 13 16 17 
3 g23 13 16 17 20 
4 g23 17 20 23 24 
5 g23 20 23 24 27 
6 g23 27 30 31 34 
7 g23 3 6 9 10 
8 g23 31 34 37 38 
9 g23 34 37 38 41 
10 g23 38 41 44 45 
11 g23 41 44 45 48 
12 g23 45 48 51 52 
13 g23 48 51 52 55 
14 g23 52 55 58 59 
15 g23 6 9 10 13 
16 g34 2 3 6 9 
17 g34 51 52 55 58 
18 g46 16 17 20 23 
19 g46 30 31 34 37 
20 g46 37 38 41 44 
21 g46 44 45 48 51 
22 g46 9 10 13 16 
23 glj14 1 2 3 4 
24 glj14 1 2 3 5 
25 glj14 11 10 13 14 
26 glj14 11 10 13 15 
27 glj14 11 10 13 16 
28 glj14 12 10 13 14 
29 glj14 12 10 13 15 
30 glj14 12 10 13 16 
31 glj14 13 16 17 18 
32 glj14 13 16 17 19 
33 glj14 14 13 16 17 
34 glj14 15 13 16 17 
35 glj14 16 17 20 21 
36 glj14 16 17 20 22 
37 glj14 18 17 20 21 
38 glj14 18 17 20 22 
39 glj14 18 17 20 23 
40 glj14 19 17 20 21 
41 glj14 19 17 20 22 
42 glj14 19 17 20 23 
43 glj14 2 3 6 7 
44 glj14 2 3 6 8 
45 glj14 20 23 24 25 
46 glj14 20 23 24 26 
47 glj14 21 20 23 24 
48 glj14 22 20 23 24 
49 glj14 23 24 27 28 
50 glj14 23 24 27 29 
51 glj14 25 24 27 28 
52 glj14 25 24 27 29 
53 glj14 26 24 27 28 
54 glj14 26 24 27 29 
55 glj14 27 30 31 32 
56 glj14 27 30 31 33 
57 glj14 28 27 30 31 
58 glj14 29 27 30 31 
59 glj14 30 31 34 35 
60 glj14 30 31 34 36 
61 glj14 32 31 34 35 
62 glj14 32 31 34 36 
63 glj14 32 31 34 37 
64 glj14 33 31 34 35 
65 glj14 33 31 34 36 
66 glj14 33 31 34 37 
67 glj14 34 37 38 39 
68 glj14 34 37 38 40 
69 glj14 35 34 37 38 
70 glj14 36 34 37 38 
71 glj14 37 38 41 42 
72 glj14 37 38 41 43 
73 glj14 39 38 41 42 
74 glj14 39 38 41 43 
75 glj14 39 38 41 44 
76 glj14 4 3 6 7 
77 glj14 4 3 6 8 
78 glj14 4 3 6 9 
79 glj14 40 38 41 42 
80 glj14 40 38 41 43 
81 glj14 40 38 41 44 
82 glj14 41 44 45 46 
83 glj14 41 44 45 47 
84 glj14 42 41 44 45 
85 glj14 43 41 44 45 
86 glj14 44 45 48 49 
87 glj14 44 45 48 50 
88 glj14 46 45 48 49 
89 glj14 46 45 48 50 
90 glj14 46 45 48 51 
91 glj14 47 45 48 49 
92 glj14 47 45 48 50 
93 glj14 47 45 48 51 
94 glj14 48 51 52 53 
95 glj14 48 51 52 54 
96 glj14 49 48 51 52 
97 glj14 5 3 6 7 
98 glj14 5 3 6 8 
99 glj14 5 3 6 9 
100 glj14 50 48 51 52 
101 glj14 51 52 55 56 
102 glj14 51 52 55 57 
103 glj14 53 52 55 56 
104 glj14 53 52 55 57 
105 glj14 53 52 55 58 
106 glj14 54 52 55 56 
107 glj14 54 52 55 57 
108 glj14 54 52 55 58 
109 glj14 56 55 58 59 
110 glj14 57 55 58 59 
111 glj14 6 9 10 11 
112 glj14 6 9 10 12 
113 glj14 7 6 9 10 
114 glj14 8 6 9 10 
115 glj14 9 10 13 14 
116 glj14 9 10 13 15 
```

所有原子、键、角和二面角均直接列出，类型对应parameters.inc。

连通无环分子的连接计数式 2

![连通无环分子的连接计数](https://ml-biomat.com/static/agent-math/06af21f58d192d5a49dedea3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Nbond | 连接图中的边数，即不同原子对之间的键数 | 1 |
| Natom | 连接图中的顶点数，即显式原子数 | 1 |
| −, 1, = | 减去一；一是无量纲常数；等号给出树图计数关系 | 1 |

怎样理解从一个原子开始，每添一个新原子并用一条键接到已有连通部分，就增加一个顶点和一条边；没有环时始终少一条边。

算一个例子水有3个原子和2条键；本例PEG有59个原子和58条键。两者还须由连接遍历确认只有一个连通分量。

使用条件适用于连通无环的连接图。环状分子、多个分子和交联网络使用相应图关系；空间中弯成圆弧不等于产生连接环。

角和二面角的数目也不只取决于主链有多长。显式氢原子形成的分支会带来许多不同的三原子路径和四原子路径；力场还规定哪些路径采用哪种参数。在四个顺次相连的原子中，前三个定义一个平面，后三个定义另一个平面，两个平面的相对转动给出二面角。沿中间那条键转动，可以显著改变末端方向，同时使邻近键长保持接近原值。高分子链能够变化出许多形状，正与这类局部转动不断组合有关。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s3)

图 3 · 键长、键角与二面角的几何示意。半透明三角形表示两个三原子平面，共享加深显示的2–3键；φ描述这两个平面之间的转角。

分子模板和完整体系的数据文件用途不同。模板描述一个可以被放置或复制的分子，完整数据文件还要描述当前盒子、系统中的原子编号、分子编号和全部连接。采用atom_style full时，常见Atoms记录依次包含原子编号、分子编号、类型、电荷和三个坐标；可选的映像标记帮助追踪周期位置。阅读时先看文件区块和所用atom_style，再解释每一列。这样就不会把模板的局部编号直接当成整个水溶液里的永久编号，也不会在复制分子后让不同对象发生编号冲突。

## 键、角和扭转，分别为哪一种变化计费

连接图只告诉我们哪些原子相连，还没有说明它们相连后怎样运动。最简单的理解，是为不同几何变化分别建立能量规则。键长偏离适合距离时产生代价，键角偏离适合角度时产生代价，绕键转动则会经过不同的能量位置。把这些贡献与非键作用相加，程序就能求出当前构象的总势能和受力。这里的“分别”是一种模型组织方法：同一次原子移动可能同时改变多条键、多个角和许多非键距离，因此最终的力仍是各项贡献合起来的结果。

LAMMPS的harmonic键势围绕一个平衡距离形成抛物线。把两原子距离与平衡距离相减，得到伸长或压缩量；平方后，两种方向都带来正的能量代价；再乘一个系数，规定相同形变需要多少能量。它与弹簧的直觉很接近。不过，软件对系数的定义必须看清楚：这一命令已经把常见弹簧公式中的二分之一吸收进K，所以不能抄入另一个定义下的刚度后又保留原数值。单位相同不意味着数值约定也相同。

LAMMPS谐和键的能量与恢复力式 3

![LAMMPS谐和键的能量与恢复力](https://ml-biomat.com/static/agent-math/d55282782159f711c94f7c1c.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Ub | 单条谐和键的能量 | kcal mol⁻¹ |
| Kb | LAMMPS键势系数，已包含常见定义的二分之一 | kcal mol⁻¹ Å⁻² |
| r, r₀ | 当前键长与平衡键长 | Å |
| Fr | 沿增大键长方向定义的径向力 | kcal mol⁻¹ Å⁻¹ |
| ², −, =, ×, 2 | 平方使压缩与伸长都有能量代价；负号使力朝能量下降方向；等号定义；相邻项相乘；2来自平方项斜率 | 1 |

怎样理解距离差平方乘系数得到能量；其距离斜率为2Kb(r−r0)，取负号得到径向恢复力。

算一个例子本例水键Kb=529.581，r0=1.012Å。若r=1.032Å，偏离0.020Å，Ub=0.2118324kcal/mol，Fr=−21.18324kcal/(mol Å)，方向使键缩短。

使用条件这是本例固定连接的谐和键项。作用在原子上的总力还包含其他项；该抛物线在本模型中保持连接。

利用这条曲线，还能判断恢复力为什么指向平衡位置。键被拉长时，继续增大距离会增加能量，因此力趋向缩短距离；键被压短时，力的方向相反。对抛物线求斜率会出现二倍的K，再加上沿能量下降方向的负号，便得到径向恢复力。没有学过求导也可以从相邻位置的能量差理解：把距离多增加一点，比较能量增加多少，再除以这段距离，就是局部斜率的近似。第三讲的力与能量关系，现在具体落到了一条化学键上。

角势也采用平方形式，但角度单位增加了一层转换。参数文件中的平衡角用度输入，程序内部在计算角偏离时使用弧度。弧度可以借助圆弧理解：圆心角对应的弧长除以半径，就给出这个角的弧度数；转半圈是π弧度，也就是一百八十度。因此，偏离五度时，应先得到约0.08727弧度，再代入这条能量式。直接把五代进去会把平方项放大三千多倍，这并非一个可以忽略的书写差别。

先换弧度，再计算角偏离的能量式 4

![先换弧度，再计算角偏离的能量](https://ml-biomat.com/static/agent-math/376f11665921ded0ea330039.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Δθdeg | 当前角减去平衡角，以度表示 | ° |
| Δθrad | 同一角偏离的弧度数 | rad |
| Kθ | 角势系数 | kcal mol⁻¹ rad⁻² |
| Uθ | 这个角势项的能量 | kcal mol⁻¹ |
| π, 180, /, ², =, × | π弧度对应180度；先相除并相乘换算，再平方；等号定义；相邻因子相乘 | 1 |

怎样理解角度的不同表示对应同一个几何。系数按弧度平方定义，因此代入前要统一角偏离的单位。

算一个例子水角Kθ=37.95，平衡角113.24°。当前角118.24°时，偏离5°=0.0872665rad，能量约0.28901kcal/mol。

使用条件本式对应LAMMPS harmonic角势；输入平衡角用度，内部计算用弧度。

二面角命令的名称也需要结合公式理解。这里的dihedral_style harmonic采用周期余弦表达式，和前面的键长、键角抛物线不是同一种形状。转动一整圈后，几何回到相同方向，能量也应重复；余弦函数正适合表达这种周期性。参数n控制一圈内重复的次数，d控制势峰和势谷的位置，K控制起伏大小。本例有些二面角项具有三重周期，因而允许多个不同的局部优选角。完整构象分布还取决于其他能量项与水环境，不能把某一个单项的最低点直接当成整条链唯一的姿态。

周期扭转势怎样给出多个优选角式 5

![周期扭转势怎样给出多个优选角](https://ml-biomat.com/static/agent-math/a44eeef478426e584c2c40d3.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| Uφ | 一个二面角项的能量 | kcal mol⁻¹ |
| Kφ | 控制周期起伏的能量系数 | kcal mol⁻¹ |
| φ | 由四个顺次连接原子定义的二面角 | rad |
| n | 整数周期数 | 1 |
| d | 取+1或−1，选择余弦项的符号 | 1 |
| cos, 1, +, [ ], =, × | 余弦随转角周期重复；1为常数；加号与括号组合项；等号定义；相邻因子相乘 | 1 |

怎样理解转过一圈后几何重复，余弦也重复；n改变一圈内重复的次数，Kφ与d决定起伏尺度和位置。

算一个例子PEG的g23项Kφ=0.3011、d=1、n=3。φ=0°时U=0.6022kcal/mol，φ=60°时U=0，因为cos180°=−1；φ=120°时又回到0.6022。

使用条件这是单个周期项。程序余弦函数使用弧度；完整构象能量还叠加其他键合与非键贡献。

解析参数练习：选择一个几何项，查看指定参数的能量响应。

[Figure: 解析键合势能与当前几何](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s4)

三个解析势能项分别采用本例参数；曲线高度按当前项调整，纵轴保留能量单位。

交互中分别改变键长、键角和扭转角，可以看到三种坐标变化怎样进入各自的能量式。曲线使用本例参数中的一个具体项，帮助理解参数含义。把这一观察带回PEG：拉长链条时，许多二面角可以重新组合，整条链的两端便拉得更远，而局部键长仍只在较小范围内变化。因此，链的整体伸长不等于把每一条共价键都等比例拉长。第七讲会沿着真实轨迹把这两种尺度分开，查看端到端距离、回转半径和局部转动怎样共同变化。

## 一套参数，需要连同它的单位和配对规则一起读

本例的parameters.inc集中列出类型标签、质量以及各类相互作用系数。标签映射把一至八分别关联到PEG和水的原子环境；质量按类型给出，电荷则保存在分子模板的逐原子记录中。这个分工解释了为什么一个质量表还不能完整定义水，也解释了为什么复制pair_coeff不能替代Charges。读参数时，应沿着“模板里的标签—参数表里的同名条目—指定的势函数形式”往返核对，确认每个数字究竟进入了哪条公式。

### 完整参数与类型标签

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

labelmap atom 1 OE 2 C 3 HC 4 H 5 CPos 6 OAlc 7 OW 8 HW
labelmap bond 1 g4 2 g18 3 g26 4 g27 5 g56 6 g71 7 OW-HW
labelmap angle 1 g12 2 g13 3 g14 4 g15 5 g51 6 g56 7 g102 8 HW-OW-HW
labelmap dihedral 1 g23 2 g34 3 g46 4 glj14

mass OE 15.9994 # PEG O (GROMOS 54A7)
mass C 12.011 # PEG C (GROMOS 54A7)
mass HC 1.008 # PEG H (GROMOS 54A7)
mass H 1.008 # PEG H (GROMOS 54A7)
mass CPos 12.011 # PEG C (GROMOS 54A7)
mass OAlc 15.9994 # PEG O (GROMOS 54A7)
mass OW 15.9994 # H2O O (SPC/Fw)
mass HW 1.008 # H2O H (SPC/Fw)

pair_coeff OE OE 0.2526 2.8492
pair_coeff C C 0.0663 3.5812
pair_coeff HC HC 0.0283 2.3734
pair_coeff H H 0.0 0.0
pair_coeff CPos CPos 0.2450 2.8114
pair_coeff OAlc OAlc 0.1195 3.1000
pair_coeff OW OW 0.155 3.165
pair_coeff HW HW 0.0 0.0

bond_coeff g4 1109.2926 1.12
bond_coeff g18 399.7916 1.43
bond_coeff g26 299.8440 1.52
bond_coeff g27 400.0343 1.53
bond_coeff g56 310.7075 1.41
bond_coeff g71 179.2543 0.971
bond_coeff OW-HW 529.581 1.012

angle_coeff g12 47.6940 109.5
angle_coeff g13 55.1271 109.5
angle_coeff g14 47.6350 109.6
angle_coeff g15 55.1139 111.0
angle_coeff g51 54.9931 110.3
angle_coeff g56 180.4602 109.0
angle_coeff g102 30.1731 110.0
angle_coeff HW-OW-HW 37.95 113.24

dihedral_coeff g23 0.3011 1 3
dihedral_coeff g34 1.4149 1 3
dihedral_coeff g46 0.2390 -1 3
dihedral_coeff glj14 0.0 1 1
```

参数按本例势函数与real单位解释。

units real规定长度用埃，时间用飞秒，能量用千卡每摩尔，温度用开尔文，压强用大气压。于是，一飞秒的时间步写作1.0，三百开尔文写作300，压强1对应一大气压。此前约化LJ模型里的温度1则采用另一套尺度，两者不能只凭数值直接比较。把一条键的系数读成“千卡每摩尔每平方埃”，就能检查它乘以距离偏离的平方后是否回到能量单位。单位检查是把公式和文件连接起来的一种很实用的推理方法。

把分子模型的力换成皮牛顿式 6

![把分子模型的力换成皮牛顿](https://ml-biomat.com/static/agent-math/80ada808bc3f7ad515f86d61.svg)

| 符号 | 含义 | 单位 |
| --- | --- | --- |
| kcal, mol, Å | 千卡、摩尔与埃；本例的能量和长度单位 | 单位 |
| NA | 阿伏伽德罗常数6.02214076×10²³ | mol⁻¹ |
| N, pN | 牛顿与皮牛顿；1pN=10⁻¹²N | 力单位 |
| 4184, 10⁻¹⁰ | 每千卡对应4184焦耳，每埃对应10⁻¹⁰米 | J/kcal; m/Å |
| =, ≈, /, × | 等号是单位转换；约等号表示末位舍入；依次相除；乘号合并分母 | 1 |

怎样理解先把每摩尔能量除以阿伏伽德罗常数换成单个相互作用的能量，再以米为单位除以长度，得到牛顿。

算一个例子1kcal/(mol Å)约为69.477pN，10kcal/(mol Å)约为694.77pN。换算只改变表达单位，不改变施加的物理力。

使用条件用于units real中的力；能量记录的每摩尔约定需要与原子级表达一致换算。

水采用SPC/Fw，是保留键长与键角变化的柔性三位点模型。Wu、Tepper和Voth在2006年的研究把水分子几何参数与液体的扩散、介电等性质联系起来，说明分子内部的一点改变也可能进入许多分子的集体行为。本例中的氧电荷为−0.82e，平衡氧—氢距离为1.012埃，平衡角为113.24度，均应按这一具体参数组合理解。柔性水的平衡参数也不等于每一帧测量值，热运动与周围分子的作用会使内部几何发生分布。[Wu、Tepper与Voth，2006](https://doi.org/10.1063/1.2136877)

PEG使用公开例题提供的GROMOS54A7衍生参数，与SPC/Fw水组成这里明确的教学模型。我们保留这组具体组合来学习拓扑、溶剂准备和外力响应。若研究问题转向某种溶剂条件下的定量链尺寸或力谱，就需要把PEG—水交叉作用与目标条件下的水化、密度、链尺寸或力—伸长数据联系起来检验。检验对象是这组完整相互作用，而不是仅看参数所属家族的名称。这样的提问也能指导模型改进：先确定哪个观测量需要更好描述，再追踪影响它的相互作用。

普通非键粒子对之外，还需要处理沿键相连的近邻。一个原子与直接相连的伙伴称为1—2关系，隔两条键到达的伙伴称为1—3，隔三条键到达的称为1—4。这些数字描述连接图距离，不是空间中相距一、二、三埃。由于键、角和扭转已经承担部分内部能量，力场会对这些近邻的非键项规定排除或缩放。本例将LJ的三个权重设为0、0、0.5，静电权重设为0、0、1，并保留angle yes的规则。它们与连接表一起定义模型，不能在改写拓扑时遗漏。

angle yes又让1—3排除与显式角、二面角记录之间建立特定对应，所以检查程序应同时读连接图和实际列出的角，而不是只数两步路径便推断全部计算。对教学读者，最重要的习惯是把这些条目视为一套相互配合的约定：局部几何势、特殊近邻权重、LJ混合方式和电荷一起决定相互作用。更换水模型或搬运一份分子参数时，这些约定都要重新核对。只调整一个看起来像“强度”的数字，可能同时改变模型原先希望保持的内部平衡。

## 把分子放进水里，需要给它真正腾出空间

准备从一个长方体盒子开始，三个边长分别是六十、三十、三十埃，也就是六、三、三纳米。程序预先为八种原子类型、七种键类型、八种角类型和四种二面角类型留出位置。这里的“种”表示参数分类的数量，不是体系中已经存在的原子或键的总数。好比图书馆先建立分类目录，再把具体书籍放进去；随后复制七百个水分子时，许多原子共享水的两种类型，许多键也共享同一种氧—氢参数。

molecule命令读取模板，create_atoms再根据模板创建实际分子。create_atoms开头的零是类型偏移量，表示保留模板已经指定的类型对应关系；它不要求系统原子编号永远等于模板中的一、二、三。随机插入时，两个种子分别参与位置与分子取向的选择，overlap和maxtry控制接触检查与尝试次数。最终创建了多少原子，应读实际输出，因为有限次尝试可能没有放入全部请求的分子。这个数量会影响后面的质量和密度，值得在运行起点就明确下来。

### 建立并准备七百个水分子

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units real
atom_style full
bond_style harmonic
angle_style harmonic
dihedral_style harmonic
pair_style lj/cut/coul/long 10
kspace_style ewald 1e-5
special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes

region box block -30 30 -15 15 -15 15
  create_box 8 box &
  bond/types 7 &
  angle/types 8 &
  dihedral/types 4 &
  extra/bond/per/atom 3 &
  extra/angle/per/atom 6 &
  extra/dihedral/per/atom 10 &
  extra/special/per/atom 14

include parameters.inc

molecule h2omol water.mol
create_atoms 0 random 700 87910 NULL mol h2omol 454756 overlap 1.0 maxtry 50

group H2O type OW HW
minimize 1.0e-4 1.0e-6 100 1000
reset_timestep 0

fix mynpt all npt temp 300 300 100 iso 1 1 1000


thermo 500
thermo_style custom step temp etotal vol density


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho file water-thermo.dat format " %.15g"
dump trajectory all custom 250 water.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id

timestep 1.0
run 15000

write_restart water.restart
# write_data water.data # uncomment to write a .data file as well
write_data water.data
```

运行lmp -in water.lmp，保留实际创建数量与数值记录。

刚生成的水经过一次几何最小化，再进行十五皮秒的各向同性NPT准备。初始长方体的形状比例保持，三个方向一起缩放以调整体积；温度目标为三百开尔文，压强目标为一大气压。水阶段的输入使用Ewald处理长程静电，后面加入PEG后改用PPPM，误差控制均按输入中的设定。两种方法都在处理周期电荷的长程部分，切换的是数值求和方案，不能据此把水解释成另一种化学组成。实际温度与密度曲线会告诉我们这个准备窗口里发生了什么。

接着在盒子中间放入一个PEG模板。原有水分子并不知道那里将出现一条链，因此有些水会与新加入的原子距离过近。删除重叠时，mol yes要求以完整分子为单位移除水：只删掉靠得太近的一个氢，会把水的原子、键和电荷关系破坏。我们的检查因此再次核对剩余分子数、总原子数和连接。删除距离是一项构建选择，它要为后续几何和动力学提供可用起点，实际删掉多少水则由这一次位置排列决定。

### 插入PEG并删除重叠整水

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart water.restart

molecule pegmol peg.mol
create_atoms 0 single 0 0 0 mol pegmol 454756

group PEG type C CPos H HC OAlc OE

delete_atoms overlap 2.0 H2O PEG mol yes


fix mynpt all npt temp 300 300 100 x 1 1 1000
fix myrct PEG recenter 0 0 0 shift all
timestep 1.0

thermo 500

# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file merge-thermo.dat format " %.15g"
dump trajectory all custom 250 merge.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 merge-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 10000

write_restart merge.restart
# write_data merge.data # uncomment to write a .data file as well
write_data merge.data
```

water.lmp结束后运行lmp -in merge.lmp，读取同目录检查点。

加入链后的十皮秒准备只让盒子x方向响应压强控制，y、z方向保持。它与前一阶段三个方向一起缩放的条件不同，正文和图轴也会按这个区别解释体积变化。原输入还把PEG的质心移回原点，同时平移所有原子，以便在同一个画面中央观察链。这个坐标平移保持内部距离、键角和链尺寸；相应轨迹适合分析构象，而实验室坐标下的整体平移扩散应使用保留该运动的另一套记录。坐标处理服务于具体观测量，不能因为画面居中了，就忘记它改变了什么表示。

分阶段准备的意义，是把不同原因造成的变化拆开。先让水建立适合的平均体积，再加入链并清理局部接触，随后观察混合体系的温度、体积和构象。若链在加入后立即伸展，先问是不是与初始重叠、局部空穴或坐标处理有关，再沿时间观察它是否继续探索不同形状。这样的阅读顺序，会让后面的拉伸比较更清楚：我们希望区分分子原本的构象变化与外力增加以后出现的响应，而不是把全部变化都归给最后加入的一条命令。

## 让连接表、结构图和运行记录互相核对

下面的完整程序把模板变成可以阅读的结构描述。它先按区块读取原子坐标、类型、电荷和键，再检查被引用的原子是否存在、编号是否重复、数量是否符合文件头。接着建立连接图，从一个原子沿键走到其他原子，确认整个PEG属于同一个连通对象。它还分别统计元素组成、原子类型、度数以及总电荷，将这些数值与我们描述的短链对应。这里的度数是一个原子连接了多少个伙伴，能够帮助识别末端氢、骨架氧和不同碳环境。

### 完整Python：模板、参数曲线与准备记录

```
#!/usr/bin/env python3
"""Inspect the supplied PEG/water templates and plot actual preparation records.

python inspect_molecule.py --input . --run . --output figures --language en
Requires NumPy and Matplotlib. --input holds peg.mol and water.mol; --run holds
water-thermo.dat, merge-thermo.dat, and merge.data from the preparation commands.
"""
from pathlib import Path
from collections import Counter, deque
import argparse
import json
import re
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


ELEMENT = {'OE': 'O', 'OAlc': 'O', 'OW': 'O', 'C': 'C', 'CPos': 'C',
           'HC': 'H', 'H': 'H', 'HW': 'H'}


def molecule(path):
    counts, sections = {}, {}
    current = None
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'(\d+) (atoms|bonds|angles|dihedrals)', line)
        if match:
            counts[match[2]] = int(match[1])
        elif line in ('Coords', 'Types', 'Charges', 'Bonds', 'Angles', 'Dihedrals'):
            current = line
            sections[current] = []
        elif current:
            sections[current].append(line.split())
    for key in ('Coords', 'Types', 'Charges', 'Bonds', 'Angles'):
        if key not in sections:
            raise ValueError(f'{path.name}: missing {key}.')
    ids = [int(row[0]) for row in sections['Coords']]
    if len(ids) != counts['atoms'] or len(set(ids)) != len(ids):
        raise ValueError('Atom count or unique IDs do not agree.')
    coords = {int(row[0]): np.array(row[1:], dtype=float) for row in sections['Coords']}
    types = {int(row[0]): row[1] for row in sections['Types']}
    charges = {int(row[0]): float(row[1]) for row in sections['Charges']}
    if set(coords) != set(types) or set(coords) != set(charges):
        raise ValueError('Position, type, and charge IDs disagree.')
    if any(value.shape != (3,) or not np.all(np.isfinite(value)) for value in coords.values()):
        raise ValueError('Each atom requires three finite coordinates.')
    graph = {atom: set() for atom in ids}
    connections = {}
    for section, noun, width in [('Bonds', 'bonds', 2), ('Angles', 'angles', 3), ('Dihedrals', 'dihedrals', 4)]:
        records = sections.get(section, [])
        if len(records) != counts.get(noun, 0):
            raise ValueError(f'{section} count differs from the header.')
        if len({int(row[0]) for row in records}) != len(records):
            raise ValueError(f'Duplicate IDs in {section}.')
        connections[section] = []
        for row in records:
            atoms = [int(x) for x in row[2:]]
            if len(atoms) != width or len(set(atoms)) != width or not set(atoms).issubset(coords):
                raise ValueError(f'Invalid reference in {section}.')
            connections[section].append((row[1], atoms))
            if section == 'Bonds':
                first, second = atoms
                if second in graph[first]:
                    raise ValueError('Repeated physical bond.')
                graph[first].add(second)
                graph[second].add(first)
    for section in ('Angles', 'Dihedrals'):
        for _, atoms in connections[section]:
            if any(v not in graph[u] for u, v in zip(atoms, atoms[1:])):
                raise ValueError(f'{section} does not follow bonded atoms.')
    unseen = set(ids)
    components = []
    while unseen:
        start = next(iter(unseen))
        queue, seen = deque([start]), {start}
        while queue:
            for neighbour in graph[queue.popleft()]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        components.append(len(seen))
        unseen -= seen
    summary = {'counts': counts, 'type_counts': dict(Counter(types.values())),
               'element_counts': dict(Counter(ELEMENT[t] for t in types.values())),
               'total_charge_e': float(sum(charges.values())), 'component_sizes': components,
               'cycle_rank': counts['bonds'] - counts['atoms'] + len(components),
               'degree_counts': dict(Counter(len(x) for x in graph.values()))}
    return coords, types, connections, summary


def thermo(path, columns):
    values = np.loadtxt(path, comments='#', ndmin=2)
    if values.shape[1] != columns or not np.all(np.isfinite(values)):
        raise ValueError(f'Expected {columns} finite columns in {path.name}.')
    if len(values) < 2 or np.any(np.diff(values[:, 1]) <= 0):
        raise ValueError('Recorded times must increase strictly.')
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('.'))
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    coords, types, links, peg = molecule(args.input / 'peg.mol')
    _, _, _, water = molecule(args.input / 'water.mol')
    if peg['element_counts'] != {'H': 34, 'O': 9, 'C': 16}:
        raise ValueError('PEG composition differs from C16H34O9.')
    if peg['component_sizes'] != [59] or peg['cycle_rank'] != 0:
        raise ValueError('Expected a single acyclic PEG connection graph.')
    if abs(peg['total_charge_e']) > 1e-8 or abs(water['total_charge_e']) > 1e-8:
        raise ValueError('A template is not electrically neutral.')
    water_record = thermo(args.run / 'water-thermo.dat', 9)
    merge_record = thermo(args.run / 'merge-thermo.dat', 10)
    data = (args.run / 'merge.data').read_text(encoding='utf-8')
    match = re.search(r'^\s*(\d+) atoms\s*$', data, re.M)
    if not match:
        raise ValueError('Missing prepared-system atom count.')
    final_atoms = int(match[1])
    if (final_atoms - 59) % 3:
        raise ValueError('Prepared count cannot contain PEG and complete three-site waters.')
    retained_water = (final_atoms - 59) // 3
    summary = {'PEG': peg, 'water': water, 'prepared_atoms': final_atoms,
               'retained_water_molecules': retained_water,
               'removed_water_molecules': 700 - retained_water,
               'preparation_final_time_ps': float(merge_record[-1, 1] / 1000),
               'preparation_final_density_g_cm3': float(merge_record[-1, 8])}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'molecule_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'template_bonds.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['bond_type', 'atom1', 'atom2', 'template_length_A'])
        for kind, (i, j) in links['Bonds']:
            writer.writerow([kind, i, j, float(np.linalg.norm(coords[i] - coords[j]))])
    zh = args.language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else 'DejaVu Sans',
        'font.size': 14, 'svg.fonttype': 'path', 'axes.spines.top': False, 'axes.spines.right': False,
        'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2', 'savefig.facecolor': '#f8f7f2'})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), constrained_layout=True)
    colors = {'H': '#94a7aa', 'C': '#254953', 'O': '#bd6541'}
    for _, (i, j) in links['Bonds']:
        pair = np.array([coords[i], coords[j]])
        axes[0].plot(pair[:, 0], pair[:, 1], color='#8d9b98', lw=1.4, zorder=1)
    for element in ('H', 'C', 'O'):
        positions = np.array([coords[i] for i in coords if ELEMENT[types[i]] == element])
        axes[0].scatter(positions[:, 0], positions[:, 1], s=35 if element == 'H' else 95,
                        color=colors[element], label=element, zorder=2)
    axes[0].set(xlabel='x / Å', ylabel='y / Å', aspect='equal',
                title=tr('模板坐标与真实键表：xy投影', 'Template coordinates and listed bonds\nxy projection'))
    axes[0].legend(frameon=False, ncol=3, loc='upper right')
    labels = list(peg['type_counts'])
    bars = axes[1].bar(labels, [peg['type_counts'][x] for x in labels], color='#167d84', width=.65)
    axes[1].bar_label(bars, padding=4)
    axes[1].set(ylabel=tr('原子数', 'Atom count'), ylim=(0, max(peg['type_counts'].values())*1.2),
                title=tr('同一个元素可以分成不同原子类型', 'One element can have\nseveral atom types'))
    fig.savefig(args.output/'template-inspection.svg');fig.savefig(args.output/'template-inspection.png', dpi=180);plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.9), constrained_layout=True)
    distance = np.linspace(.90, 1.12, 200)
    axes[0].plot(distance, 529.581*(distance-1.012)**2, color='#167d84')
    axes[0].set(xlabel='r / Å', ylabel='U / kcal mol⁻¹', title=tr('SPC/Fw氧—氢键项', 'SPC/Fw O–H bond term'))
    angle = np.linspace(95, 130, 200)
    axes[1].plot(angle, 37.95*np.deg2rad(angle-113.24)**2, color='#bd6541')
    axes[1].set(xlabel='θ / °', ylabel='U / kcal mol⁻¹', title=tr('SPC/Fw角项', 'SPC/Fw angle term'))
    phi = np.linspace(-180, 180, 361)
    axes[2].plot(phi, .3011*(1+np.cos(3*np.deg2rad(phi))), color='#466eaa')
    axes[2].set(xlabel='φ / °', ylabel='U / kcal mol⁻¹', title=tr('PEG g23扭转项', 'PEG g23 torsional term'))
    fig.savefig(args.output/'parameter-curves.svg');fig.savefig(args.output/'parameter-curves.png', dpi=180);plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    fields = [(2, tr('温度 / K', 'Temperature / K')), (8, tr('密度 / g cm⁻³', 'Density / g cm⁻³')),
              (7, tr('体积 / Å³', 'Volume / Å³'))]
    for ax, (column, label) in zip(axes, fields):
        ax.plot(water_record[:,1]/1000, water_record[:,column], color='#167d84', label=tr('纯水：各向同性NPT', 'Water: isotropic NPT'))
        ax.plot(merge_record[:,1]/1000, merge_record[:,column], color='#bd6541', label=tr('加入PEG：x方向NPT', 'Inserted PEG: x-only NPT'))
        ax.axvline(15, color='#687b80', ls=':', lw=1)
        ax.set_ylabel(label);ax.grid(axis='y',alpha=.2)
    axes[0].axhline(300,color='#687b80',ls='--',lw=1)
    axes[0].legend(frameon=False,fontsize=12,loc='best')
    axes[-1].set_xlabel(tr('从建水阶段起算的物理时间 / ps', 'Physical time from the water stage / ps'))
    fig.savefig(args.output/'preparation-records.svg');fig.savefig(args.output/'preparation-records.png', dpi=180);plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

运行脚本开头的命令；--language zh或en控制图中文字，输入与记录保存在同一例题目录。

结构图直接使用模板中的真实坐标，并用键表连接相应原子。为了看清骨架，图中可以把氢画得较小，但计算和计数仍包含它们。另一幅图比较不同原子类型的数量，让“六种PEG类型”与“五十九个PEG原子”的区别变得可见。图中的某个氧与另一处氢在投影上重叠，可能只是三维结构沿视线方向重叠；检查真实距离时，程序仍使用三个坐标分量。因此，图像负责帮助我们定位，数量和几何计算负责把判断说准确。

### PEG模板的实际结构与参数响应

结构与计数来自peg.mol；参数曲线由本例解析式计算。它们分别展示起始模板和单项能量规则。

LAMMPS 30 Sep 2026 Update 1；Gravelle等人的PEG/SPC-Fw开源例，300 K，real单位。保持原分阶段准备与恒力拉伸流程，增加可逐项核对的观测记录。

[下载参考数据与完整输入（ZIP） 4.47 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-peg-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s7)

peg.mol的59个原子与58条共价键的实际xy投影，以及按原子类型分类的计数。原子类型区分不同局部化学环境，同一种元素可以有多个类型。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s7)

按本例参数计算的解析能量项：SPC/Fw的氧—氢键、H—O—H键角与PEG的g23扭转。角度在势能计算中换成弧度；这里分别观察单项规则。

参数图则从本例的键长和角度系数出发，逐点评估能量表达式。它们描述一个单项如何响应几何变化，可以与输入中的数值直接对应。模板中的起始键长可以落在平衡值附近，也可能偏离一些；受到其他相互作用以后，实际几何还会调整。我们因此把“参数规定的平衡距离”“模板中测得的初始距离”和“轨迹中随时间变化的距离”分别说明。它们都是长度，却来自不同层次，混在一起就容易把一个坐标快照当成力场参数。

实际准备结果另外读取水阶段和加入链之后的数值记录。这里观察温度、密度和体积怎样随物理时间变化，并用不同面板保留阶段的条件。只有水时的原子总数、加入PEG后的原子总数和删除整水后的数量，可以与最终data文件逐项核对。轨迹播放器则让我们检查链是否完整、是否处在水环境中，以及周期表示是否切断了画面中的分子。数据表和动画各自回答不同问题，放在一起才能把数量、几何和运动联系起来。

### 水与插链阶段的实际准备记录

初始700水，删除30个完整重叠水后保留670水与59个PEG原子。0–15ps各向同性NPT，15–25ps仅x方向NPT。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/#zh-s7)

原输入的实际准备记录。0–15 ps为700个水分子的各向同性NPT；插入PEG并删除30个重叠水后，15–25 ps以670个水与59个PEG原子运行x方向NPT。两段体积变化对应不同的盒子控制条件。

这次构建先放入700个完整水分子。插入PEG后，重叠规则移除了30个整水，因此最终有670个水分子与59个PEG原子，总计2069个原子。到25ps准备末态，质量密度为0.94018g/cm³。随后固定体积的构象观察沿用这一具体起点；评估目标条件下的平衡密度，需要继续观察其体积和密度分布。这个数量关系与阶段条件，也让我们能够准确说明第七讲的链尺寸来自哪一种水环境。

### 水中的短PEG链

插链后的15–25ps实际准备轨迹。PEG与全部溶剂共同平移以保持链居中，适合观察内部构象。

读完图后，可以自己做一项简短推理：如果把某个PEG原子的类型标签改成水氧，原子总数与连接图可能完全不变，但质量和相互作用可能改变；如果只改它的原子编号，同时正确更新所有引用，化学模型反而可以保持相同。这个对比揭示了检查工作的层次。字节或编号相同是一种文件关系，化学身份、几何和参数一致则是物理关系。读懂模型，需要知道每个字段怎样进入计算，而不是只看文件是否成功打开。

## 从一份模板走向一个有明确条件的研究对象

现在，这条PEG已经具有几种相互补充的描述：分子式给出组成，连接图给出身份，参数给出受力规则，坐标给出构象，水环境与运行设置给出观察条件。任何后续比较都应从这里说明改变了哪一项。例如，增加重复单元会改变分子大小和连接表；改变末端基团会改变局部化学环境和电荷；调整温度会改变热运动条件；增加外力则改变链受到的驱动。把这些操作分开，结果之间的差异才容易追踪到具体原因。

对基础读者，一个很有价值的练习是沿着water.mol中的一个氢走一遍完整路径：找到它的编号与类型，读出电荷，找到与氧相连的键，再到parameters.inc中找到对应的键参数，最后把某个给定距离代入公式计算能量。随后用相同方法检查一个PEG醚氧。这个练习只需要加减乘除和对文件关系的理解，却已经涵盖了复杂大分子模型的重要部分：每项物理作用，都应能从一组明确的信息追溯出来。

准备新材料时，还可以把目标写成一个能够测量的问题。想研究表面修饰后的水化，就要确定表面的化学连接与电荷，并统计水在相应区域的分布；想比较两种链的柔顺性，就要保持比较条件一致，观察足够多的内部转动与整体尺寸；想研究交联后的弹性，则需要进一步定义哪些链段之间形成了连接。模型不再是一份孤立参数表，而是研究问题在原子、连接和环境三个层次上的具体表达。

下一讲会把注意力放到水与离子的相互作用。我们已经知道电荷属于哪个原子、连接怎样限定分子、参数怎样进入能量式，接下来就可以理解为什么同样是水，不同位点安排和几何约束会带来不同模型，以及离子和界面怎样改变局部环境。第七讲再回到这条PEG，沿轨迹追踪它的形状与受力响应。分子身份先明确，运动中的每一个变化才有可以解释的对象。

## 延伸阅读与开放资料

- [Polymer in water; A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial3/polymer-in-water.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY4.0

  PEG/SPC-Fw分子模板、参数与水准备/插链流程。

  保留原模型与准备阶段，增加数值记录、双语解释、模板检查与图表。
- [Über Polymerisation](https://doi.org/10.1002/cber.19200530627) · Hermann Staudinger · Scientific citation; no reproduced figure

  长链共价结构的科学史。

  绘制连接观念示意图。
- [Flexible simple point-charge water model with improved liquid-state properties](https://doi.org/10.1063/1.2136877) · Yujie Wu; Harald L. Tepper; Gregory A. Voth · Scientific citation; no reproduced figure

  SPC/Fw模型与几何参数的物理作用。

  结合所用模板解释。
- [Definition and testing of the GROMOS force-field versions 54A7 and 54B7](https://doi.org/10.1007/s00249-011-0700-9) · Nathan Schmid and colleagues · Scientific citation; no reproduced figure

  PEG参数的力场家族背景。

  与本例具体教学参数组合区分。
- [LAMMPS: molecule](https://docs.lammps.org/molecule.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
- [LAMMPS: atom_style](https://docs.lammps.org/atom_style.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
- [LAMMPS: bond_harmonic](https://docs.lammps.org/bond_harmonic.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
- [LAMMPS: angle_harmonic](https://docs.lammps.org/angle_harmonic.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
- [LAMMPS: dihedral_harmonic](https://docs.lammps.org/dihedral_harmonic.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
- [LAMMPS: special_bonds](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Technical reference

  核对输入字段、势函数与相互作用约定。

  独立解释、算例和图示。
