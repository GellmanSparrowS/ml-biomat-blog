---
title: "NetworkX Fundamentals: Understanding, Building, and Analyzing Networks with Python"
date: "2026-06-30"
category: "python-tutorials"
tags: ["NetworkX", "Python", "network analysis", "graph theory", "network science", "data visualization"]
lang: "en"
slug: "networkx-fundamentals"
description: "A complete hands-on introduction to NetworkX: from graph theory fundamentals to network construction, analysis metrics, and visualization."
---

## 1. Why NetworkX — From Intuition to Tool

Before understanding NetworkX, take a step back and consider "relationships" themselves. In your proteome, one protein activates another; a bone trabecula transmits stress to another through a contact point; a neuron fires downstream; a city's roads connect it to neighboring cities. All of these phenomena share the same formal structure: a set of **entities** and **connections** between them. Mathematics abstracts this as a graph, \(G = (V, E)\), consisting of a vertex set \(V\) and an edge set \(E\).

Graph theory is not young. Euler solved the Königsberg bridge problem in 1736 using equivalent ideas. What truly made graphs a daily research tool was the simultaneous arrival of cheap computing power and abundant data. When analyzing thousands of proteins in a protein–protein interaction (PPI) network, hundreds of thousands of synapses in a connectome, or tens of thousands of beam elements in a metamaterial lattice, pencil and paper become useless. We need a library that can read data, compute centrality automatically, find shortest paths, detect community structure, and visualize results on demand.

NetworkX was built for exactly this purpose. It is a pure-Python open-source library first developed in 2002 by Aric Hagberg, Daniel Schult, and Pieter Swart, publicly debuted at SciPy 2004, and originally motivated in part by modeling disease propagation strategies across social, biological, and infrastructure networks. Today, NetworkX (current stable version: 3.6.1) has become the de facto standard for network analysis in the Python ecosystem. It covers graph creation and manipulation, dozens of classical algorithms, several graph model generators, and visualization interfaces to Matplotlib and GraphViz.

Understanding NetworkX's core value is not just about which functions it provides, but about its design philosophy: **treating graphs as first-class computational objects**. Nodes can be any hashable Python object—strings, integers, tuples, or even another graph. Edges can carry arbitrary attribute dictionaries. This means you never need to encode biological entities as integers before analysis; you can use protein names directly as nodes and experimental confidence scores as edge weights, so that the code reads almost one-to-one with your scientific intent.

Installation is trivial:

```bash
pip install networkx
pip install matplotlib   # for visualization support
```

The conventional import alias is:

```python
import networkx as nx
import matplotlib.pyplot as plt
```

---

## 2. Four Graph Types — Which Structure Fits Your Problem?

The first step when facing a real problem is deciding which type of graph best models it. NetworkX provides four core classes, and the choice directly affects the behavior of every subsequent algorithm.

`Graph` is the most basic **undirected graph**: edges have no direction, \((u, v)\) and \((v, u)\) represent the same edge, and at most one edge exists between any pair of nodes. Use cases include protein interaction networks (interactions are symmetric), undirected skeletal networks, and friendship graphs. `DiGraph` is a **directed graph**: edges have direction, \((u, v)\) differs from \((v, u)\). Use cases include gene regulatory networks (A activating B does not imply B activating A), hyperlink graphs, and directed stress propagation paths. `MultiGraph` allows **multiple undirected edges** between the same pair of nodes—useful when different types of relationships coexist for the same node pair. `MultiDiGraph` combines directed edges with multiple-edge support.

| Class | Directed | Parallel Edges | Typical Use |
|---|---|---|---|
| `Graph` | No | No | PPI networks, undirected lattices |
| `DiGraph` | Yes | No | Gene regulatory, citation networks |
| `MultiGraph` | No | Yes | Multi-modal transportation |
| `MultiDiGraph` | Yes | Yes | Directed multi-relational networks |

All four classes share nearly identical APIs, so switching between them carries minimal cost. When uncertain, start with `Graph` or `DiGraph` and migrate to multi-edge versions if needed.

---

## 3. Building Graphs — Nodes, Edges, and Attributes

Once you have chosen a graph type, the next step is loading data into the graph object. NetworkX's add/remove API is highly Pythonic, allowing you to build graphs from many sources: one-by-one additions, batch imports, or conversion from dictionaries and matrices.

The most direct method is building from an empty graph. `G.add_node(n)` adds a single node; `G.add_nodes_from(iterable)` adds many at once. Nodes can carry attribute dictionaries at declaration time, stored in `G.nodes[n]` and accessible at any time.

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

Adding edges is equally direct. `G.add_edge(u, v)` adds an edge (auto-creating u and v if they don't exist); `G.add_edges_from(ebunch)` accepts any iterable of edge tuples. Edges can carry attributes, with `weight` being the most common:

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

At the data structure level, NetworkX implements its adjacency list as a "dict-of-dicts": the outer dictionary maps nodes to their neighbor dictionaries; inner dictionaries map neighboring nodes to edge attribute dictionaries. This structure makes node and neighbor lookup, addition, and deletion all close to O(1)—highly efficient for sparse graphs, which real networks almost always are.

Accessing basic properties:

```python
print(G.number_of_nodes())
print(G.number_of_edges())
print(G.adj["ProteinA"])           # adjacency dict
print(G["ProteinA"]["ProteinB"]["weight"])  # 0.95

# G.nodes and G.edges return live Views, not copies
for neighbor in G.neighbors("ProteinA"):
    print(neighbor)
```

Note that `G.nodes` and `G.edges` return **Views** that synchronize with the underlying data structure in real time. If you need to modify the graph while iterating, convert to a list first (`list(G.edges())`), to avoid runtime errors.

NetworkX also supports conversion from adjacency matrices, edge-list DataFrames, and adjacency dictionaries:

```python
import numpy as np

A = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
H = nx.from_numpy_array(A)

adj_dict = {"a": ["b", "c"], "b": ["a"], "c": ["a"]}
K = nx.from_dict_of_lists(adj_dict)
```

---

## 4. Degree, Path Length, and Clustering — Three Keys to Reading a Network

Once a graph is built, the first questions researchers typically ask are: which nodes are "important"? How far does information need to travel from A to B? Does this system tend to form tight cliques or remain open? These three questions correspond to three foundational network metrics: **degree**, **shortest path**, and **clustering coefficient**. Mastering these three is equivalent to learning the basic grammar for reading any network.

**Degree** is the most intuitive node property: how many edges does a node have? For undirected graphs, `G.degree(node)` returns the neighbor count directly. For directed graphs, in-degree and out-degree carry distinct meanings—in a gene regulatory network, a high-in-degree node is a hub regulated by many genes, while a high-out-degree node is a master regulator controlling many others.

```python
G_directed = nx.DiGraph()
G_directed.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])
print(dict(G_directed.in_degree()))   # {1: 0, 2: 1, 3: 2, 4: 1}
print(dict(G_directed.out_degree()))  # {1: 2, 2: 1, 3: 1, 4: 0}
```

The **degree distribution**—the fraction of nodes with degree k—provides a statistical fingerprint of the network. Random networks follow a Poisson distribution; real PPI, social, and web networks follow a power law, indicating scale-free structure with a few massive hubs.

**Shortest path** describes the "distance" between nodes. Of all possible routes, the shortest path minimizes hop count (unweighted) or total weight (weighted):

```python
G = nx.Graph()
G.add_weighted_edges_from([("A","B",4), ("B","D",2), ("A","C",3), ("C","D",4)])

print(nx.shortest_path(G, "A", "D"))                       # ['A', 'B', 'D']
print(nx.shortest_path(G, "A", "D", weight="weight"))      # ['A', 'B', 'D'] (total weight=6)
print(nx.average_shortest_path_length(G))
```

**Clustering coefficient** answers: how tightly connected are a node's neighbors to each other? If all your friends know each other, your clustering coefficient is 1; if none of them do, it is 0. Mathematically, the local clustering coefficient of node \(i\) is:

$$C(i) = \frac{2e_i}{k_i(k_i-1)}$$

where \(k_i\) is node i's degree and \(e_i\) is the number of edges that actually exist among its neighbors.

```python
G = nx.karate_club_graph()  # Zachary's karate club — classic benchmark

local_cc  = nx.clustering(G)
avg_cc    = nx.average_clustering(G)
trans     = nx.transitivity(G)

print(f"Average clustering: {avg_cc:.4f}")
print(f"Transitivity (global clustering): {trans:.4f}")
```

Together, these three metrics give a coarse portrait of any network. High average degree + low average path length + high clustering typically indicates an efficient, robust small-world network. Extremely heterogeneous degree with very short average paths suggests scale-free structure. These signatures are directly meaningful in biology (functional modularity), materials (load redistribution capacity), and infrastructure (vulnerability to targeted failure).

---

## 5. Centrality — Who Matters Most in a Network?

Centrality is the richest—and most easily misused—family of concepts in network analysis. The central question is: what does "important" mean? Different answers give rise to different metrics, each capturing a distinct facet of importance. Researchers must choose based on domain knowledge rather than defaulting to node degree.

**Degree centrality** is the most direct: \(C_D(i) = k_i / (n-1)\). It quantifies how many direct connections a node has—analogous to follower count in a social network or interaction count in a PPI network. Its weakness is being entirely local: it knows nothing about where those neighbors sit in the global network.

**Betweenness centrality** captures how often a node serves as a bridge in global communication:

$$C_B(i) = \sum_{s \neq i \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}}$$

where \(\sigma_{st}\) is the total number of shortest paths from s to t, and \(\sigma_{st}(i)\) is the fraction passing through i. High-betweenness nodes are "traffic hubs"—removing them forces many information flows to reroute or break down. In structural mechanics, such nodes are analogous to critical members carrying the most force paths; in epidemiology, they are superspreaders bridging communities.

**Closeness centrality** measures how quickly a node can reach all others:

$$C_C(i) = \frac{n-1}{\sum_{j \neq i} d(i,j)}$$

A node with high closeness centrality can "reach" the entire network rapidly—making it ideal for placing sensors, broadcast nodes, or emergency response facilities.

**Eigenvector centrality** introduces a recursive idea: a node's importance depends not just on how many neighbors it has, but on how important those neighbors are. This is the conceptual core of Google's PageRank. Mathematically, it is the principal eigenvector of the adjacency matrix.

```python
G = nx.karate_club_graph()

degree_c    = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness   = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G)

def top_node(d):
    return max(d, key=d.get)

print("Top by Degree:      ", top_node(degree_c))
print("Top by Betweenness: ", top_node(betweenness))
print("Top by Closeness:   ", top_node(closeness))
print("Top by Eigenvector: ", top_node(eigenvector))
```

A practical recommendation: in network analysis papers, always report multiple centrality measures and discuss their correlation (using Pearson or Spearman rank correlation). High agreement across measures signals a strong core-periphery structure; independence across measures indicates that network "importance" is multi-dimensional and cannot be reduced to a single axis.

---

## 6. Shortest-Path Algorithms — From Dijkstra to Floyd

Shortest-path computation is one of the most deeply studied problems in graph theory and one of the most frequently needed operations in practice. NetworkX includes several algorithms; understanding their applicability conditions is essential for choosing the right one.

**Dijkstra's algorithm** is the default choice. It uses a greedy strategy: starting from the source node, at each step it selects the unvisited node with the smallest known distance and relaxes its neighbors. Time complexity is \(O((V + E) \log V)\) with heap optimization—the industry standard for positive-weight sparse graphs. NetworkX's `nx.shortest_path(G, source, target, weight='weight')` defaults to Dijkstra.

**Bellman-Ford** allows negative edge weights but runs in \(O(VE)\)—use it only when negative weights are genuinely present.

**Floyd-Warshall** computes all-pairs shortest paths in \(O(V^3)\), appropriate for small to medium networks (up to a few hundred nodes) when the complete distance matrix is needed.

```python
import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([
    (1, 2, 1.5), (2, 3, 2.0), (1, 3, 5.0),
    (3, 4, 1.0), (2, 4, 4.0)
])

paths  = nx.single_source_dijkstra_path(G, source=1)
lengths = nx.single_source_dijkstra_path_length(G, source=1)
print("Shortest path 1->4:",  paths[4])    # [1, 2, 3, 4]
print("Shortest distance 1->4:", lengths[4]) # 4.5

# Extract the largest connected component before computing average path length
if nx.is_connected(G):
    avg_l = nx.average_shortest_path_length(G, weight="weight")
    print(f"Average shortest path length: {avg_l:.3f}")
else:
    lcc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    avg_l = nx.average_shortest_path_length(lcc, weight="weight")
```

A common pitfall: `nx.average_shortest_path_length()` raises an exception on disconnected graphs, because distances between disconnected node pairs are infinite. Always check connectivity with `nx.is_connected(G)` first or analyze the largest connected component (LCC).

For structural and materials researchers, shortest paths can be interpreted as **load transmission paths**: in a beam network, force travels from a loading point to a support along the shortest (or lowest-impedance) path. Nodes or edges with high betweenness centrality are precisely those through which the most force paths pass—the critical members whose failure maximally disrupts the overall structural response.

---

## 7. Classic Network Models — Random, Small-World, and Scale-Free

Understanding real networks requires a reference baseline: what does "random" look like, and what deviations from it are meaningful? NetworkX provides built-in generators for three theoretically fundamental models.

The **Erdős–Rényi random graph** (ER model) is the simplest baseline. Given n nodes, each pair connects independently with probability p, producing \(G(n, p)\). Degree distribution follows a Poisson, clustering coefficient equals p, and average path length scales as \(\ln n / \ln \langle k \rangle\). The crucial point: real networks almost universally deviate from ER on all of these metrics—and those deviations carry information about internal structure.

```python
G_er = nx.erdos_renyi_graph(n=100, p=0.05, seed=42)
print(f"ER avg clustering: {nx.average_clustering(G_er):.4f}")
```

The **Watts-Strogatz small-world model** (WS model) was proposed in 1998 in *Nature* after Watts and Strogatz observed that neural networks (*C. elegans*), actor collaboration networks, and the US western power grid all shared high clustering coefficients (like regular lattices) yet short average path lengths (like random graphs). Their model generates a ring lattice where each node connects to its k nearest neighbors, then rewires each edge with probability \(\beta\). At intermediate \(\beta\), the model captures the "small-world" co-occurrence of high clustering and short paths.

```python
G_ws = nx.watts_strogatz_graph(n=100, k=4, p=0.1, seed=42)
print(f"WS avg clustering: {nx.average_clustering(G_ws):.4f}")
print(f"WS avg path length: {nx.average_shortest_path_length(G_ws):.4f}")
```

The **Barabási-Albert scale-free model** (BA model), proposed in 1999 in *Science*, revealed that many real networks—the Web, citation networks, PPI networks—follow a power-law degree distribution \(P(k) \sim k^{-\gamma}\), meaning a handful of massively connected hubs dominate the network. This "scale-free" structure emerges from **preferential attachment**: as the network grows, new nodes attach preferentially to already high-degree nodes, embodying a "rich-get-richer" dynamics.

```python
G_ba = nx.barabasi_albert_graph(n=100, m=2, seed=42)
print(f"BA max degree: {max(dict(G_ba.degree()).values())}")
print(f"BA avg clustering: {nx.average_clustering(G_ba):.4f}")
```

Comparing the three models yields crucial intuitions:

| Property | ER Random | WS Small-World | BA Scale-Free |
|---|---|---|---|
| Degree dist. | Poisson | Near-Poisson | Power law |
| Clustering | Low | High | Medium (decreases with size) |
| Avg path length | Short | Short | Short |
| Robustness | Uniform failure | Uniform failure | Robust to random, fragile to targeted attack |

For structural mechanics researchers: scale-free networks are highly robust against random node removal (most nodes have low degree, so random removal rarely matters) but catastrophically vulnerable to targeted attacks on hub nodes. This maps directly onto certain metamaterial and biological skeleton failure modes—seemingly strong, yet harboring a critical Achilles' heel.

---

## 8. Visualization — Making Graphs Speak

NetworkX is not a professional visualization tool, but its Matplotlib interface is sufficient for rapid exploration. For publication-quality figures, dedicated software such as Gephi, Cytoscape (biological networks), or Graphviz is recommended. For research presentations and draft figures, NetworkX + Matplotlib does the job.

The core function is `nx.draw_networkx()`. Layout algorithms determine where nodes are placed, and choice of layout strongly affects readability:

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

layouts = {
    "Spring Layout\n(force-directed)": nx.spring_layout(G, seed=42),
    "Circular Layout":                 nx.circular_layout(G),
    "Kamada-Kawai Layout":             nx.kamada_kawai_layout(G),
}

betweenness = nx.betweenness_centrality(G)
node_colors = [betweenness[n] for n in G.nodes()]

for ax, (title, pos) in zip(axes, layouts.items()):
    nx.draw_networkx(
        G, pos=pos, ax=ax,
        node_color=node_colors, cmap=plt.cm.viridis,
        node_size=200, with_labels=True, font_size=7,
        edge_color="gray", alpha=0.85
    )
    ax.set_title(title)
    ax.axis("off")

plt.suptitle("Karate Club — Node color = Betweenness Centrality", y=1.02)
plt.tight_layout()
plt.show()
```

Practical tips: encode centrality in node color, degree in node size, and edge weight in transparency or width—this conveys rich information in a single figure without clutter. For large graphs (> 500 nodes), direct drawing typically produces an uninterpretable hairball. In that case, aggregate to community level, display only the topological skeleton, or export to Gephi via `nx.write_gexf(G, "graph.gexf")`.

---

## 9. Community Detection and Graph Generators — Advanced Tools

When a network grows too large to comprehend visually, **community detection** becomes the primary tool for revealing structure. A community is a set of nodes with dense internal connections and sparse external ones—analogous to protein complexes (functional modules), crystal grains in materials (clusters of aligned atoms), or interest groups in social networks.

NetworkX includes the Louvain algorithm (available as `nx.community.louvain_communities()` from version 3.x onward), the most widely used community detection method, based on greedy modularity optimization:

```python
G = nx.karate_club_graph()

communities = nx.community.louvain_communities(G, seed=42)
print(f"Number of communities: {len(communities)}")

node_community = {}
for idx, community in enumerate(communities):
    for node in community:
        node_community[node] = idx

colors = [node_community[n] for n in G.nodes()]
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(G, pos=pos, node_color=colors, cmap=plt.cm.tab10,
                 node_size=300, with_labels=True)
plt.title("Louvain Communities — Karate Club")
plt.axis("off")
plt.show()

modularity = nx.community.modularity(G, communities)
print(f"Modularity: {modularity:.4f}")
```

Modularity quantifies the quality of the community partition, ranging from \(-1\) to \(1\); values closer to 1 indicate cleaner, more distinct communities.

NetworkX also provides an extensive suite of **graph generators** for rapid benchmarking:

```python
G_lattice  = nx.grid_2d_graph(5, 5)           # 2D square lattice
G_hex      = nx.hexagonal_lattice_graph(3, 3)  # Hexagonal lattice (2D materials)
G_tree     = nx.balanced_tree(r=3, h=3)        # Balanced ternary tree
G_complete = nx.complete_graph(10)             # Fully connected
G_star     = nx.star_graph(10)                 # Hub-and-spoke
```

For materials and structural mechanics researchers, hexagonal (`hexagonal_lattice_graph`) and triangular (`triangular_lattice_graph`) lattices are excellent starting points for parameterizing metamaterial topologies as NetworkX graphs, then computing connectivity, centrality distributions, and robustness curves (largest connected component size as a function of random removal vs. targeted attack fraction).

---

## 10. Performance Considerations and Further Resources

NetworkX prioritizes flexibility and readability over raw speed. Its pure-Python dict-of-dicts architecture is a bottleneck for graphs exceeding one million nodes or requiring real-time computation. Common alternatives include **igraph** (C core, Python interface, significantly faster for most metrics), **graph-tool** (C++/OpenMP, for very large graphs), and **cuGraph** (NVIDIA RAPIDS, GPU-accelerated, for billion-scale graphs). A 2025 benchmarking study published in *Social Network Analysis and Mining* confirmed that igraph and graph-tool outperform NetworkX substantially on computationally intensive tasks such as community detection and betweenness centrality, though NetworkX's seamless integration with NumPy, SciPy, and Pandas remains its core competitive advantage for research workflows.

Recommended resources for graduate students seeking to go deeper—most have no comprehensive Chinese-language equivalents, which is why direct engagement with the English materials is strongly recommended:

- **Official Documentation & Tutorial**: https://networkx.org/documentation/stable/tutorial.html — authoritative and up-to-date
- **GitHub Repository**: https://github.com/networkx/networkx — source code, issues, and example notebooks; reading the source is itself an excellent way to learn graph algorithms
- **Memgraph's NetworkX Guide**: https://memgraph.github.io/networkx-guide/ — well-structured with extensive practical code examples
- **PHYS 7332 Network Science Course Materials**: https://asmithh.github.io/network-science-data-book/ — graduate-level, combining theory and NetworkX practice
- **DataCamp NetworkX Tutorial**: https://www.datacamp.com/tutorial/networkx-python-graph-tutorial — problem-driven (Chinese Postman Problem), fully runnable code

NetworkX is a tool, but the thinking it enables—modeling systems as nodes and relationships, describing function and fragility in topological language—is the skill worth cultivating. Whether your research concerns protein folding, impact-resistant metamaterials, brain connectomes, or urban road networks, the ability to fluently translate between graph language and domain language is one of the most valuable cross-disciplinary competencies a modern computational researcher can develop.

---

## References

1. Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. *Proceedings of the 7th Python in Science Conference (SciPy 2008)*, 11–16.

2. Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature*, 393(6684), 440–442. https://doi.org/10.1038/30918

3. Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509–512. https://doi.org/10.1126/science.286.5439.509

4. Albert, R., & Barabási, A. L. (2002). Statistical mechanics of complex networks. *Reviews of Modern Physics*, 74(1), 47–97. https://doi.org/10.1103/RevModPhys.74.47

5. Nair, A., Rajput, P., & Rahman, M. (2025). A comparative evaluation of social network analysis tools: performance and community engagement perspectives. *Social Network Analysis and Mining*, 15, Article 40. https://doi.org/10.1007/s13278-025-01409-y

6. Verma, T., & others (2021). Searching for small-world and scale-free behaviour in long-term historical data of a real-world power grid. *Scientific Reports*, 11, 6879. https://doi.org/10.1038/s41598-021-86103-7

7. Humphries, M. D., & Gurney, K. (2011). Methods for generating complex networks with selected structural properties for simulations: A review and tutorial for neuroscientists. *Frontiers in Computational Neuroscience*, 5, 10. https://doi.org/10.3389/fncom.2011.00010

8. NetworkX Developers. (2024). NetworkX 3.x Documentation. https://networkx.org/documentation/stable/
```

---
Learn more:
1. [Tutorial — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/tutorial.html)
2. [Complex Network Series: Part 4 — Network Analysis with NetworkX | by Ebrahim Mousavi | Medium](https://medium.com/@ebimsv/complex-network-series-part-4-network-analysis-with-networkx-8b009bdae040)
3. [Small World and Scale-Free Networks](https://dshizuka.github.io/networkanalysis/example1_smallworld.html)
4. [NetworkX for Python — A Practical Guide to Graphs, Visualization, and Traversals | by Sneha Jain | Medium](https://medium.com/@jainsnehasj6/networkx-for-python-a-practical-guide-to-graphs-visualization-and-traversals-35106cfee2ea)
5. [An introduction to Graph Analysis and NetworkX | by Luigi Sciarretta | Data Reply IT | DataTech | Medium](https://medium.com/data-reply-it-datatech/an-introduction-to-graph-analysis-and-networkx-b76e4a387c6c)
6. [NetworkX - Wikipedia](https://en.wikipedia.org/wiki/NetworkX)
7. [Scale-Free Networks - Think Complexity, 2nd Edition \[Book\]](https://www.oreilly.com/library/view/think-complexity-2nd/9781492040194/ch04.html)
8. [Introduction — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/reference/introduction.html)
9. [Exploring Network Structure, Dynamics, and Function ...](https://aric.hagberg.org/papers/hagberg-2008-exploring.pdf)
10. [Clustering — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/reference/algorithms/clustering.html)
11. [The modeling of scale-free networks - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378437103011257)
12. [networkx · PyPI](https://pypi.org/project/networkx/)
13. [Graph Data Science With Python/NetworkX | Toptal®](https://www.toptal.com/developers/data-science/graph-data-science-python-networkx)
14. [Clustering, Connectivity and other Graph properties using Python Networkx](https://www.tutorialspoint.com/article/clustering-connectivity-and-other-graph-properties-using-python-networkx)
15. [Searching for small-world and scale-free behaviour in long-term historical data of a real-world power grid | Scientific Reports](https://www.nature.com/articles/s41598-021-86103-7)
16. [Reference — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/reference/index.html)
17. [NetworkX: A Comprehensive Guide to Mastering Network Analysis with Python | by Tushar Aggarwal | Medium](https://medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0)
18. [Network Analysis with NetworkX](https://python-fiddle.com/tutorials/networkx)
19. [Network Model with Scale‐Free, High Clustering Coefficients, and Small‐World Properties - Yan - 2023 - Journal of Applied Mathematics - Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1155/2023/5533260)
20. [Python NetworkX for Graph Optimization Tutorial | DataCamp](https://www.datacamp.com/tutorial/networkx-python-graph-tutorial)
21. [Working with spatial networks using NetworkX | D-Lab](https://dlab.berkeley.edu/news/working-spatial-networks-using-networkx)
22. [Class 3: Introduction to Networkx 2 — Graph Properties & Algorithms — PHYS 7332 (Network Science Data)](https://asmithh.github.io/network-science-data-book/class_03_networkx2.html)
23. [Watts–Strogatz model - Wikipedia](https://en.wikipedia.org/wiki/Watts%E2%80%93Strogatz_model)
24. [GitHub - networkx/networkx: Network Analysis in Python · GitHub](https://github.com/networkx/networkx)
25. [NetworkX Resources – Deep Learning Garden](https://deeplearning.lipingyang.org/networkx-resources/)
26. [NetworkX: Network Analysis with Python](https://www.cl.cam.ac.uk/teaching/1314/L109/tutorial.pdf)
27. [Networks: Structure and Dynamics Erzs´ebet Ravasz Regan](https://regan.med.harvard.edu/Teaching/CVBR/Ravasz_Networks.pdf)
28. [NetworkX Package - Python Graph Library - AskPython](https://www.askpython.com/python-modules/networkx-package)
29. [Graph Theory and NetworkX - Part 1: Loading and Visualization - Tales of One Thousand and One Data](https://walkenho.github.io/graph-theory-and-networkX-part1/)
30. [Graph Algorithms - - Maël Fabien](https://maelfabien.github.io/machinelearning/graph_3/)
31. [(PDF) Scale-Free Networks: A Decade and Beyond](https://www.researchgate.net/publication/26692135_Scale-Free_Networks_A_Decade_and_Beyond)
32. [NetworkX basics | Memgraph's Guide for NetworkX library](https://memgraph.github.io/networkx-guide/basics/)
33. [(PDF) Exploring Network Structure, Dynamics, and Function Using NetworkX](https://www.researchgate.net/publication/236407765_Exploring_Network_Structure_Dynamics_and_Function_Using_NetworkX)
34. [Python | Clustering, Connectivity and other Graph properties using Networkx - GeeksforGeeks](https://www.geeksforgeeks.org/python-clustering-connectivity-and-other-graph-properties-using-networkx/)
35. [(a) WS small world (Watts and Strogatz, 1998) and (b) BA scale free... | Download Scientific Diagram](https://www.researchgate.net/figure/a-WS-small-world-Watts-and-Strogatz-1998-and-b-BA-scale-free-Barabasi-and-Albert_fig2_282395671)
36. [Graph types — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/reference/classes/index.html)
37. [NetworkX Graph Visualization | Tom Sawyer Software](https://blog.tomsawyer.com/networkx-graph-visualization)
38. [A comparative evaluation of social network analysis tools: performance and community engagement perspectives | Social Network Analysis and Mining | Springer Nature Link](https://link.springer.com/article/10.1007/s13278-025-01409-y)
39. [Methods for Generating Complex Networks with Selected Structural Properties for Simulations: A Review and Tutorial for Neuroscientists - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3059456/)