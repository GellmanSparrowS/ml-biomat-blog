---
title: "NetworkX 基础：用 Python 理解、构建与分析网络"
date: "2026-06-30"
category: "python-tutorials"
tags: ["NetworkX", "Python", "网络分析", "图论", "网络科学", "数据可视化"]
lang: "zh"
slug: "networkx-fundamentals-zh"
description: "NetworkX 基础：用 Python 理解、构建与分析网络。面向生物与材料科学研究生的实用教程，含完整可运行代码示例与详细原理解析，适合零基础入门与进阶参考。"
---

## 一、为什么需要 NetworkX——从直觉到工具

在理解 NetworkX 之前，先退一步，想想"关系"本身。你的蛋白质组里，一个蛋白质激活另一个蛋白质；一根骨小梁和另一根通过接触点传递应力；一个神经元向下游神经元发放脉冲；一个城市的公路把它和若干相邻城市连通。这些现象在形式上都是一样的：一堆**实体**，以及实体之间的**连接关系**。数学把这种形式抽象为图（Graph），由节点集合 \(V\)（Vertex）和边集合 \(E\)（Edge）构成，记作 \(G = (V, E)\)。

图论在历史上并不年轻，1736 年欧拉解决哥尼斯堡七桥问题时，已经用了等价的思想。但真正让图成为科研日常工具，是因为两件事同时发生了：算力廉价、数据海量。当我们需要分析蛋白质互作网络（PPI）里数千个蛋白、脑连接组里数十万个突触、超材料晶格里成千上万的梁单元时，铅笔和方格纸已经毫无用处。我们需要一个能读入数据、自动计算中心性、找最短路径、识别社区结构并随手画出来的编程库。

NetworkX 就是为此而生的。它是一个纯 Python 的开源库，最初由 Aric Hagberg、Daniel Schult 和 Pieter Swart 于 2002 年开始开发，2004 年在 SciPy 年会上公开亮相，其最初动机之一是分析疾病在社会、生物、基础设施网络中的传播策略。今天的 NetworkX（当前稳定版为 3.6.1）几乎已成为 Python 生态中网络分析的事实标准。它涵盖图的创建与操纵、数十种经典算法、多种图模型生成器和对 Matplotlib、GraphViz 等的可视化接口。

理解 NetworkX 的核心价值，不仅在于它提供了什么函数，更在于它背后的设计哲学：**把图当作可计算的一等公民**。节点可以是任何可哈希的 Python 对象——字符串、整数、元组、甚至另一个图，边可以携带任意属性字典。这意味着你不需要把生物实体先编码成整数再去分析，可以直接用蛋白质名称作为节点，用实验置信度作为边权重，代码读起来和你的科学意图几乎一一对应。这一设计让 NetworkX 在材料科学、结构力学、计算生物学、社会网络分析等截然不同的领域里都能低摩擦地落地。

安装极为简单：

```bash
pip install networkx
# 若需要可视化辅助
pip install matplotlib
```

导入时约定俗成地使用别名：

```python
import networkx as nx
import matplotlib.pyplot as plt
```

---

## 二、图的四种类型——你的问题是哪种图？

拿到一个真实问题，第一步是判断它适合用哪种图来建模。NetworkX 提供了四个核心类，它们的选择直接影响后续所有算法的行为。

`Graph` 是最基础的**无向图**：边没有方向，\((u, v)\) 和 \((v, u)\) 表示同一条边，且两节点之间至多一条边。适用场景：蛋白质互作网络（互作是对称的）、无向骨架网络、朋友关系图。`DiGraph` 是**有向图**（有向图，Directed Graph）：边有方向，\((u, v)\) 表示从 u 指向 v 的单向连接，与 \((v, u)\) 不同。适用场景：基因调控网络（A 激活 B 不等于 B 激活 A）、网页超链接图、有向应力传播路径。`MultiGraph` 是允许两节点之间存在**多条无向边**的图，适合建模不同类型的关系共存于同一节点对之间的情况，例如两个城市之间既有公路又有铁路。`MultiDiGraph` 则是上述二者的结合——有向且多边。

| 类名 | 有向 | 允许平行边 | 典型应用 |
|---|---|---|---|
| `Graph` | 否 | 否 | 蛋白质互作、无向晶格 |
| `DiGraph` | 是 | 否 | 基因调控、引文网络 |
| `MultiGraph` | 否 | 是 | 多模态交通网络 |
| `MultiDiGraph` | 是 | 是 | 有向多关系网络 |

四个类共享几乎相同的 API，切换代价极低。在不确定的时候，从 `Graph` 或 `DiGraph` 开始，日后如有需要再迁移到多边版本。

---

## 三、构建图——节点、边与属性的核心操作

理解了图的类型之后，下一步是把数据"装入"图对象。NetworkX 的增删节点与边的接口设计非常 Pythonic，允许你从各种来源构建图：逐条添加、批量导入、从字典或矩阵转换。

最直接的方式是从空图开始逐步构建。`G.add_node(n)` 添加一个节点，`G.add_nodes_from(iterable)` 批量添加。节点可以在声明时附带属性字典，这些属性存储在 `G.nodes[n]` 中，随时可读可写。

```python
import networkx as nx

G = nx.Graph()

# Add single nodes with attributes
G.add_node("ProteinA", type="kinase", molecular_weight=52.3)
G.add_node("ProteinB", type="receptor")

# Batch add nodes
proteins = [("ProteinC", {"type": "enzyme"}), ("ProteinD", {"type": "transcription_factor"})]
G.add_nodes_from(proteins)
```

添加边同样直接。`G.add_edge(u, v)` 添加一条边（如果 u 或 v 不存在，会自动创建这两个节点），`G.add_edges_from(ebunch)` 接受任何可迭代的边元组。边也可以携带属性，最常用的是 `weight`：

```python
# Add edges with attributes
G.add_edge("ProteinA", "ProteinB", weight=0.95, interaction_type="phosphorylation")
G.add_edge("ProteinB", "ProteinC", weight=0.72, interaction_type="binding")

# Batch add weighted edges
G.add_weighted_edges_from([
    ("ProteinC", "ProteinD", 0.88),
    ("ProteinA", "ProteinD", 0.61),
])
```

这种设计带来了一个深刻的便利：你的节点和边不仅仅是抽象的 ID，它们可以携带实验测量值、空间坐标、材料参数等任何域特定信息，而图算法仍然可以在同一个对象上直接运行。

在数据结构层面，NetworkX 的邻接表用 "字典套字典"（dict-of-dicts）实现：外层字典以节点为键，值为该节点的邻居字典；内层字典以邻居节点为键，值为边的属性字典。这种结构使得节点和邻居的查找、添加、删除都接近 O(1)，在稀疏图（真实网络几乎都是稀疏的）中效率很高。

访问图的基本属性：

```python
print(G.number_of_nodes())   # Number of nodes
print(G.number_of_edges())   # Number of edges
print(G.nodes())             # NodeView of all nodes
print(G.edges())             # EdgeView of all edges
print(G.adj["ProteinA"])     # Adjacency dict of ProteinA

# Iterate over neighbors
for neighbor in G.neighbors("ProteinA"):
    print(neighbor)

# Access edge attributes
print(G["ProteinA"]["ProteinB"]["weight"])  # 0.95
```

一个容易被忽视的细节：`G.nodes` 和 `G.edges` 返回的是**视图（View）**，它们与底层数据结构实时同步——修改图后无需重新获取，视图会自动反映变化。如果需要在迭代时修改图，则要先转成列表（`list(G.edges())`），否则可能引发运行时错误。

从其他数据结构创建图也很方便。NetworkX 支持从邻接矩阵（NumPy 数组）、边列表（Pandas DataFrame）、邻接字典等直接转换：

```python
import numpy as np

# From adjacency matrix
A = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
H = nx.from_numpy_array(A)

# From adjacency dict
adj_dict = {"a": ["b", "c"], "b": ["a"], "c": ["a"]}
K = nx.from_dict_of_lists(adj_dict)
```

---

## 四、度、路径与聚类——读懂一张图的三把钥匙

一旦图构建好，研究者面对的第一批问题通常是：哪些节点"重要"？信息需要走多远才能从 A 到 B？这个系统倾向于形成小团体还是保持开放？这三个问题分别对应网络分析的三个最基础的量：**度（Degree）**、**最短路径（Shortest Path）**和**聚类系数（Clustering Coefficient）**。理解这三者，等于掌握了阅读任何网络的最基本语法。

**度**是节点最直觉的属性：一个节点连了几条边。对无向图，`G.degree(node)` 直接返回邻居数量。对有向图，入度（in-degree）和出度（out-degree）分别代表指向该节点的边数和从该节点出发的边数，语义差异显著——在基因调控网络里，高入度节点是被许多基因调控的枢纽，高出度节点是广泛调控其他基因的主控因子。

```python
G_directed = nx.DiGraph()
G_directed.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])

print(dict(G_directed.in_degree()))   # {1: 0, 2: 1, 3: 2, 4: 1}
print(dict(G_directed.out_degree()))  # {1: 2, 2: 1, 3: 1, 4: 0}
```

度分布（degree distribution）则是从统计视角描述整个网络：网络中具有度 k 的节点占多大比例。随机网络的度分布接近泊松分布，而真实的蛋白质互作网络、社会网络、万维网的度分布遵循幂律，这称为**无标度性（Scale-free）**——少数枢纽节点（Hub）的度比多数节点高出几个数量级。

**最短路径**描述节点间的"距离"。两个节点之间可能有很多条路可走，最短路径是其中经过边数（无权图）或总权重（加权图）最小的那条。NetworkX 提供了多种最短路径算法：

```python
G = nx.Graph()
G.add_weighted_edges_from([("A","B",4), ("B","D",2), ("A","C",3), ("C","D",4)])

# Shortest path (unweighted, by hop count)
print(nx.shortest_path(G, "A", "D"))             # ['A', 'B', 'D']

# Shortest path (weighted, Dijkstra by default)
print(nx.shortest_path(G, "A", "D", weight="weight"))  # ['A', 'B', 'D'] (weight=6)

# All-pairs shortest path length
lengths = dict(nx.all_pairs_shortest_path_length(G))

# Average path length (only for connected graph)
print(nx.average_shortest_path_length(G))
```

**聚类系数**回答的问题是：一个节点的邻居们，自己彼此之间连接得有多紧密？如果你的朋友圈里，你的所有朋友互相都认识，聚类系数就是 1；如果你的朋友们完全不认识彼此，聚类系数就是 0。数学上，节点 \(i\) 的局部聚类系数定义为：

$$C(i) = \frac{e_i}{\binom{k_i}{2}} = \frac{2e_i}{k_i(k_i-1)}$$

其中 \(k_i\) 是节点 i 的度，\(e_i\) 是其邻居之间实际存在的边数，\(\binom{k_i}{2}\) 是邻居之间可能存在的最大边数。直觉上，这个公式计算的是"我的朋友中，有多大比例的朋友对彼此相识"。全局聚类系数（也叫传递性，transitivity）则计算整个网络中封闭三角形的比例。

```python
G = nx.karate_club_graph()  # Classic benchmark: Zachary's karate club

# Local clustering coefficients (dict of node -> coefficient)
local_cc = nx.clustering(G)

# Average clustering coefficient
avg_cc = nx.average_clustering(G)
print(f"Average clustering coefficient: {avg_cc:.4f}")

# Global clustering (transitivity)
transitivity = nx.transitivity(G)
print(f"Transitivity: {transitivity:.4f}")
```

这三个量合在一起，已经能给出任何网络的粗略画像。高平均度 + 低平均路径 + 高聚类系数，通常意味着一个高效、鲁棒的小世界网络；低平均度 + 低聚类系数 + 中等平均路径，可能是树状层级网络；极少数节点度极高且平均路径极短，往往暗示无标度结构。

---

## 五、中心性——谁在网络中"最重要"？

中心性（Centrality）是网络分析中最丰富、也最容易被误用的一组概念。核心问题是：什么叫做"重要"？不同的答案孕育了不同的中心性指标，它们彼此互补，有时结论截然不同。研究者需要结合领域知识选择合适的指标，而不是盲目套用"节点度越高越重要"这种朴素直觉。

**度中心性（Degree Centrality）**最直接：归一化的节点度，即 \(C_D(i) = \frac{k_i}{n-1}\)，其中 n 是节点总数。它量化的是节点拥有多少直接连接，在社交网络里对应"粉丝数"，在蛋白质网络里对应"互作数目"。度中心性的缺点是完全局部化——它只看直接邻居，不知道这些邻居在全局网络中处于什么位置。

**介数中心性（Betweenness Centrality）**着眼于节点在全局通信中扮演的桥梁角色。节点 i 的介数中心性定义为所有节点对之间的最短路径中，经过节点 i 的那部分比例：

$$C_B(i) = \sum_{s \neq i \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}}$$

其中 \(\sigma_{st}\) 是 s 到 t 的最短路径总数，\(\sigma_{st}(i)\) 是其中经过 i 的数量。直觉上，介数中心性高的节点是"交通枢纽"——切掉它，大量信息流就会被迫绕路甚至中断。在结构力学中，这样的节点类比于承受大量传力路径的关键构件；在流行病学中，这样的个体是疾病跨社区传播的超级传播者。

**接近中心性（Closeness Centrality）**量化节点"距离所有其他节点有多近"：

$$C_C(i) = \frac{n-1}{\sum_{j \neq i} d(i,j)}$$

其中 \(d(i,j)\) 是 i 和 j 之间的最短路径长度。接近中心性高的节点可以快速"接触到"全网。如果你要在网络中找一个放置传感器或广播节点的位置，接近中心性高的节点通常是理想候选。

**特征向量中心性（Eigenvector Centrality）**引入了一个递归思想：一个节点的重要性不只由邻居数量决定，还由邻居的重要性决定。这正是 Google PageRank 的核心思想。数学上，节点 i 的特征向量中心性满足：

$$C_E(i) = \frac{1}{\lambda} \sum_{j \in \mathcal{N}(i)} C_E(j)$$

这等价于求邻接矩阵的主特征向量。重要的邻居赋予你更高的中心性，哪怕你的直接连接数并不多。

```python
import networkx as nx

G = nx.karate_club_graph()

degree_c    = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness   = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G)

# Find the most central node by each measure
def top_node(centrality_dict):
    return max(centrality_dict, key=centrality_dict.get)

print("Top by Degree:      ", top_node(degree_c))
print("Top by Betweenness: ", top_node(betweenness))
print("Top by Closeness:   ", top_node(closeness))
print("Top by Eigenvector: ", top_node(eigenvector))
```

在 Zachary 空手道俱乐部这个经典数据集上，不同中心性指标给出的"最重要节点"往往相同（节点 0 和节点 33，即俱乐部教练和管理员），但在复杂的生物或材料网络中，四种指标可能给出四个不同的节点——它们分别在各自的语义框架里"最重要"。

一个实用建议：在撰写网络分析论文时，不要只报告一种中心性，而应同时报告几种，并讨论它们之间的相关性（可用 Pearson/Spearman 相关系数）。如果四种中心性高度一致，说明网络有明显的核心-外围结构；如果它们相互独立，说明网络的"重要性"是多维度的，不可化约。

---

## 六、最短路径算法——从 Dijkstra 到 Floyd

最短路径是图论中被研究最深的问题之一，也是实际应用中出现频率最高的计算任务。NetworkX 内置了多种算法，理解它们的适用条件，才能选对工具避免计算浪费。

**Dijkstra 算法**是最短路径的默认首选。它基于贪心策略：从源节点出发，每步选择当前已知距离最小的未访问节点，更新其邻居的距离。时间复杂度为 \(O((V + E) \log V)\)（使用堆优化），是正权重稀疏图的工业级标准。NetworkX 中 `nx.shortest_path(G, source, target, weight='weight')` 默认就调用 Dijkstra。

**Bellman-Ford 算法**允许负权重边，但时间复杂度为 \(O(VE)\)，仅在确有负权重时使用。NetworkX 提供 `nx.bellman_ford_path()`。

**Floyd-Warshall 算法**一次性计算所有节点对之间的最短路径，时间复杂度为 \(O(V^3)\)，适合节点数较少（几百以内）且需要全对距离矩阵的场景。

```python
import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([
    (1, 2, 1.5), (2, 3, 2.0), (1, 3, 5.0),
    (3, 4, 1.0), (2, 4, 4.0)
])

# Single-source shortest paths
paths = nx.single_source_dijkstra_path(G, source=1)
lengths = nx.single_source_dijkstra_path_length(G, source=1)
print("Shortest path 1->4:", paths[4])       # [1, 2, 3, 4]
print("Shortest distance 1->4:", lengths[4]) # 4.5

# All-pairs shortest path (returns a dict-of-dicts)
all_lengths = dict(nx.all_pairs_dijkstra_path_length(G))

# Check connectivity first before computing average path length
if nx.is_connected(G):
    avg_l = nx.average_shortest_path_length(G, weight="weight")
    print(f"Average shortest path length: {avg_l:.3f}")
```

一个常见陷阱：`nx.average_shortest_path_length()` 在图不连通时会抛出异常，因为不连通的节点对之间的距离是无穷大，平均值无意义。实践中应先用 `nx.is_connected(G)`（无向图）或 `nx.is_strongly_connected(G)`（有向图）检查连通性，或者提取最大连通分量（Largest Connected Component，LCC）后再分析：

```python
# Extract the largest connected component
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()
print("LCC size:", G_lcc.number_of_nodes())
```

网络直径（Diameter）是所有最短路径中最长的那个，可以理解为网络的"最坏情况距离"：

```python
diameter = nx.diameter(G_lcc)
print(f"Network diameter: {diameter}")
```

对于材料/结构力学背景的研究者，可以把最短路径理解为**传力路径**：在一个杆件网络中，从加载点到支撑点，力沿最短（或最低阻抗）路径传递。介数中心性高的节点或边，正是最多传力路径经过的"关键构件"，这类构件的失效将对整个结构的响应产生最大影响。

---

## 七、经典网络模型——随机图、小世界与无标度

理解真实网络，需要一把参考尺：什么叫"随机"，什么叫"不随机"？NetworkX 内置了几个理论上极重要的网络生成器，理解它们，就理解了现代网络科学的基础语言。

**Erdős–Rényi 随机图（ER 模型）**是最简单的参考基准。给定 n 个节点，每对节点以概率 p 独立地连接一条边，记作 \(G(n, p)\)。这是对"纯随机关系"的数学化。ER 图的度分布遵循泊松分布，聚类系数等于 p，平均路径长度约为 \(\ln n / \ln \langle k \rangle\)。关键在于，真实网络几乎在所有这些量上都显著偏离 ER 图——这种偏离本身就是信息，说明真实网络有非随机的内在结构。

```python
# Erdos-Renyi random graph: n nodes, edge probability p
G_er = nx.erdos_renyi_graph(n=100, p=0.05, seed=42)
print(f"ER: nodes={G_er.number_of_nodes()}, edges={G_er.number_of_edges()}")
print(f"ER avg clustering: {nx.average_clustering(G_er):.4f}")
```

**Watts-Strogatz 小世界模型（WS 模型）**由 Duncan Watts 和 Steven Strogatz 于 1998 年在 *Nature* 上提出。他们观察到神经元网络（*C. elegans*）、电影演员合作网络、美国西部电网都有两个共同特性：聚类系数高（像规则格子）但平均路径很短（像随机图）。这两个特性的共存就叫**小世界效应**。WS 模型的生成方式是：先创建一个规则环状格子（每个节点和最近的 k 个邻居相连），然后以概率 \(\beta\) 随机重连每条边。当 \(\beta = 0\) 时是纯粹规则格子，\(\beta = 1\) 时趋近随机图；在中间某个 \(\beta\) 值处，模型就捕捉到了高聚类 + 短路径的小世界特征。

```python
# Watts-Strogatz small-world graph
# n=100 nodes, k=4 nearest neighbors, rewiring probability beta=0.1
G_ws = nx.watts_strogatz_graph(n=100, k=4, p=0.1, seed=42)
print(f"WS avg clustering: {nx.average_clustering(G_ws):.4f}")
print(f"WS avg path length: {nx.average_shortest_path_length(G_ws):.4f}")
```

**Barabási-Albert 无标度模型（BA 模型）**于 1999 年由 Albert-László Barabási 和 Réka Albert 在 *Science* 上提出，揭示了另一类普遍现象：许多真实网络（万维网、引文网络、蛋白质互作网络）的度分布不是泊松分布，而是幂律分布 \(P(k) \sim k^{-\gamma}\)，即少数节点（Hub）的连接数比大多数节点高出数个数量级。这种网络被称为**无标度网络（Scale-free network）**，因为幂律分布没有特征尺度。BA 模型的生成机制是**优先连接（Preferential Attachment）**：网络从小到大增长，每个新加入的节点更倾向于连接那些度数本就很高的节点——"强者愈强，富者愈富"。

```python
# Barabasi-Albert scale-free graph
# n=100 nodes, each new node connects to m=2 existing nodes
G_ba = nx.barabasi_albert_graph(n=100, m=2, seed=42)

import collections
degree_sequence = sorted([d for n, d in G_ba.degree()], reverse=True)
degree_count = collections.Counter(degree_sequence)

print(f"BA avg clustering: {nx.average_clustering(G_ba):.4f}")
print(f"Max degree in BA graph: {max(degree_sequence)}")
```

比较这三个模型，得到的直觉非常重要：

| 属性 | ER 随机图 | WS 小世界 | BA 无标度 |
|---|---|---|---|
| 度分布 | 泊松分布 | 近泊松 | 幂律 |
| 聚类系数 | 低 | 高 | 中（随规模下降） |
| 平均路径 | 短 | 短 | 短 |
| 鲁棒性 | 均匀失效 | 均匀失效 | 随机失效鲁棒，靶向攻击脆弱 |

对结构力学研究者：无标度网络对"随机去除节点"高度鲁棒（因为绝大多数节点度数很低，随机去掉不影响连通性），但对"靶向攻击枢纽节点"极度脆弱。这与某些超材料或生物骨架的失效模式高度对应——看似坚固，却有致命弱点。

---

## 八、可视化——让图说话

NetworkX 不是专业可视化工具，但它内置了对 Matplotlib 的接口，足以在探索阶段快速看懂网络结构。真正的出版级可视化通常需要 Gephi、Cytoscape（生物网络）或 Graphviz 等专用软件，但 NetworkX + Matplotlib 完全可以胜任科研汇报和论文草图。

核心函数是 `nx.draw()` 和更精细的 `nx.draw_networkx()`。节点的布局（Layout）是可视化效果的关键，NetworkX 提供了多种布局算法：

```python
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

G = nx.karate_club_graph()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Layout options
layouts = {
    "Spring Layout\n(force-directed)": nx.spring_layout(G, seed=42),
    "Circular Layout":                 nx.circular_layout(G),
    "Kamada-Kawai Layout":             nx.kamada_kawai_layout(G),
}

# Use betweenness centrality to color nodes
betweenness = nx.betweenness_centrality(G)
node_colors = [betweenness[n] for n in G.nodes()]

for ax, (title, pos) in zip(axes, layouts.items()):
    nx.draw_networkx(
        G, pos=pos, ax=ax,
        node_color=node_colors,
        cmap=plt.cm.viridis,
        node_size=200,
        with_labels=True,
        font_size=7,
        edge_color="gray",
        alpha=0.85
    )
    ax.set_title(title)
    ax.axis("off")

plt.suptitle("Zachary's Karate Club — Node color = Betweenness Centrality", y=1.02)
plt.tight_layout()
plt.savefig("karate_club_layouts.png", dpi=150, bbox_inches="tight")
plt.show()
```

几个实用技巧：用节点颜色编码中心性或社区标签，用节点大小编码度数，用边的透明度和宽度编码权重，可以在一张图里传递大量信息而不显得凌乱。如果图太大（节点数 > 500），直接 draw 通常一片混乱，这时应该先聚合社区、只显示拓扑骨架，或改用 Gephi 导入 `nx.write_gexf(G, "graph.gexf")` 生成的文件来做专业可视化。

---

## 九、社区检测与图生成器——进阶工具

当一个网络大到难以直观理解时，**社区检测（Community Detection）**成为揭示结构的核心手段。社区是指内部连接稠密、外部连接稀疏的节点集合——类比于蛋白质复合物（功能模块）、材料中的晶粒（相同晶向的原子群）、社交网络中的兴趣圈子。

NetworkX 内置了 Louvain 算法（3.x 版本后通过 `nx.community.louvain_communities()` 直接调用），这是目前最常用的社区检测算法之一，基于贪心模块度优化，速度快且效果好：

```python
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

G = nx.karate_club_graph()

# Louvain community detection
communities = nx.community.louvain_communities(G, seed=42)
print(f"Number of communities found: {len(communities)}")

# Assign community labels to nodes for coloring
node_community = {}
for idx, community in enumerate(communities):
    for node in community:
        node_community[node] = idx

colors = [node_community[n] for n in G.nodes()]
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx(
    G, pos=pos,
    node_color=colors,
    cmap=plt.cm.tab10,
    node_size=300,
    with_labels=True
)
plt.title("Louvain Community Detection on Karate Club")
plt.axis("off")
plt.show()
```

模块度（Modularity）是评估社区质量的标准指标，值域 \([-1, 1]\)，越接近 1 表示社区划分越清晰：

```python
modularity = nx.community.modularity(G, communities)
print(f"Modularity: {modularity:.4f}")
```

Girvan-Newman 算法则从反向思路出发：反复移除介数中心性最高的边，直到图分裂成若干连通分量，适合层次化的社区分析，但计算量更大。

NetworkX 还内置了大量**图生成器**，方便快速生成标准拓扑进行对照实验：

```python
# Some useful graph generators for structural/biological research
G_lattice  = nx.grid_2d_graph(5, 5)           # 2D square lattice
G_hex      = nx.hexagonal_lattice_graph(3, 3)  # Hexagonal lattice (common in 2D materials)
G_tree     = nx.balanced_tree(r=3, h=3)        # Balanced ternary tree
G_complete = nx.complete_graph(10)              # Every node connects to all others
G_star     = nx.star_graph(10)                 # Hub-and-spoke

# These are particularly relevant for structural engineers and materials scientists
print(nx.info(G_hex))
```

对材料和结构力学研究者，六边形格子（`hexagonal_lattice_graph`）、三角格子（`triangular_lattice_graph`）和完全图（`complete_graph`）是建立初步对照基准的极好工具，可以直接将超材料点阵的拓扑参数化为 NetworkX 图，随后计算其连通性、中心性分布、抗毁性（比较随机节点去除和靶向攻击两种情景下的最大连通分量大小变化）。

---

## 十、性能考量与进阶资源

NetworkX 的设计优先考虑灵活性和可读性，代价是在大规模图上的性能。它基于纯 Python 的字典结构，对于超过百万节点或需要实时处理的场景，应考虑替代方案。常见的替代或补充库包括：**igraph**（C 语言核心，Python 接口，速度远快于 NetworkX）、**graph-tool**（C++核心，OpenMP 并行，适合超大图）、**cuGraph**（基于 NVIDIA RAPIDS，GPU 加速，面向亿级节点）。一项 2025 年发表于 *Social Network Analysis and Mining* 的对比研究指出，在社区检测和介数中心性等计算密集型任务上，igraph 和 graph-tool 的性能显著优于 NetworkX，但 NetworkX 的生态整合（与 NumPy/SciPy/Pandas 的无缝对接）和易学性仍是其核心竞争力。

对于希望深入学习的研究生，以下资源是目前最好的英文材料（大多数没有系统的中文版，这也是推荐直接阅读英文的原因）：

- **官方文档与教程**：https://networkx.org/documentation/stable/tutorial.html — 权威且更新及时，涵盖从入门到高级算法的所有内容
- **GitHub 仓库**：https://github.com/networkx/networkx — 源码、issue、examples notebook 都在这里，阅读源码本身是学习图算法的绝佳方式
- **Memgraph 的 NetworkX 指南**：https://memgraph.github.io/networkx-guide/ — 结构清晰，有大量实用代码示例
- **PHYS 7332 Network Science 课程材料**：https://asmithh.github.io/network-science-data-book/ — 大学研究生级别，理论与 NetworkX 实践并重
- **DataCamp NetworkX 教程**：https://www.datacamp.com/tutorial/networkx-python-graph-tutorial — 面向实际问题（中国邮递员问题），代码完整可运行

NetworkX 是一个工具，但工具背后的思维方式——把系统建模为节点和关系，用拓扑语言描述功能与脆弱性——才是真正值得训练的能力。无论你研究的是蛋白质折叠、抗冲击超材料、脑连接组还是城市路网，能熟练地在图的语言和领域语言之间自由切换，是现代计算科学研究者最有价值的跨学科技能之一。

---

## 参考文献

1. Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. *Proceedings of the 7th Python in Science Conference (SciPy 2008)*, 11–16.

2. Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature*, 393(6684), 440–442. https://doi.org/10.1038/30918

3. Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509–512. https://doi.org/10.1126/science.286.5439.509

4. Albert, R., & Barabási, A. L. (2002). Statistical mechanics of complex networks. *Reviews of Modern Physics*, 74(1), 47–97. https://doi.org/10.1103/RevModPhys.74.47

5. Nair, A., Rajput, P., & Rahman, M. (2025). A comparative evaluation of social network analysis tools: performance and community engagement perspectives. *Social Network Analysis and Mining*, 15, Article 40. https://doi.org/10.1007/s13278-025-01409-y

6. Verma, T., & others (2021). Searching for small-world and scale-free behaviour in long-term historical data of a real-world power grid. *Scientific Reports*, 11, 6879. https://doi.org/10.1038/s41598-021-86103-7

7. Humphries, M. D., & Gurney, K. (2011). Methods for generating complex networks with selected structural properties for simulations: A review and tutorial for neuroscientists. *Frontiers in Computational Neuroscience*, 5, 10. https://doi.org/10.3389/fncom.2011.00010

8. NetworkX Developers. (2024). NetworkX 3.x Documentation. https://networkx.org/documentation/stable/