# Representing Material Connectivity as a Graph

Source: https://ml-biomat.com/tutorials/python-scientific/s02/en/
Language: en

Connect nodes and edges to reachability, shortest routes, and current balance; compare edge loss and redundant connections.

## Why study a material’s connections separately?

A conducting fiber film may look like many interwoven lines, but electrical transport depends on which intersections truly connect and which segments form routes between electrodes. Related questions occur in porous flow channels, hydrogel crosslinks, and contacts between cells. Geometry says where these objects are; connectivity says where one can travel from them. NetworkX represents and analyzes the latter information while allowing physical quantities such as length, radius, and conductance to be attached to connections.

This chapter constructs a two-dimensional teaching network with 13 ideal junctions connected by conducting segments. Coordinates are in micrometres, all segments share the same product of material conductivity and cross-sectional area, and nodes 0 and 11 are held at 1 V and 0 V. We ask whether the terminals are connected, which route is shortest, and how much current all available routes carry together. Removing an edge or adding a redundant connection then changes these answers in different ways. Every result comes from the explicitly constructed network, whose nodes and edges can be inspected individually.

No single index replaces all three questions. A network with one long, narrow channel can remain connected while conducting poorly. Networks with the same shortest route may conduct differently because they offer different parallel paths. Developing these questions in sequence introduces NetworkX’s objects and algorithms while showing how to choose physically meaningful graph attributes. Applying the method to a microscopy-derived skeleton or a molecular connectivity table begins with equally explicit node and edge definitions.

## From seven bridges to a graph: preserving the relevant information

Euler’s Königsberg bridge problem asked whether a route could cross every bridge exactly once. The outlines of the land regions and street distances were set aside, while the seven connections between four regions were retained. His paper, catalogued as E53 and published in 1741, reduced the problem to the number of connections incident on each location. Today those locations are vertices or nodes, the connections are edges, and the number of incident edges is a node’s degree. The abstraction preserves the structure that determines whether the walk can be completed.

![Multigraph and degrees of Euler’s seven bridges. The displayed route uses six blue edges and leaves the dashed red edge; four odd-degree vertices provide the general impossibility argument.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e3d80402f417a7af6f947e02.svg?v=e3d80402f417)

Figure 1Multigraph and degrees of Euler’s seven bridges. The displayed route uses six blue edges and leaves the dashed red edge; four odd-degree vertices provide the general impossibility argument.

The illustrated walk A→B→A→C→A→D→B uses six bridges and finishes at B with the C–D bridge remaining. One unsuccessful attempt cannot rule out every other route. The general argument examines intermediate vertices: each arrival must be paired with a departure, so their incident edges must be used in pairs. Only the start and finish can each leave one edge unpaired. A connected graph with an open walk using every edge once therefore has at most two odd-degree vertices; a closed walk requires even degree everywhere. The seven-bridge graph has four odd-degree vertices, preventing such a walk.

This history also affects the data structure. Two distinct bridges connect A and B, and another two connect A and C. A `MultiGraph` preserves multiple edges between the same vertices. In an ordinary `Graph`, adding the same vertex pair again updates an existing edge and would merge those separate bridges. Our material example defines at most one equivalent segment for each junction pair, so it uses an undirected simple `Graph`. If two distinct fibers connect the same junctions in an experiment, retain multiple edges or combine them using an explicitly defined physical equivalence.

The graph-theoretic term “bridge” has a more specific meaning: removing that edge increases the number of connected components. This is distinct from a physical bridge in the historical story. Each physical bridge in the seven-bridge graph has an alternative route, whereas a material segment might be the only connection between two regions. Consequently, `nx.bridges` identifies structurally indispensable connections, rather than searching for a particular shape or object name.

## Describing the material with node and edge tables

Each node-table row stores a stable identifier and coordinates. Node 0 is at (0,0) μm and node 1 at (1,0) μm. Each edge-table row identifies two endpoints and attaches length and conductance. An identifier is an identity, not a distance: the numerical difference between identifiers 0 and 11 says nothing about their separation in micrometres. The code stores coordinates through `graph.add_node` and physical edge attributes through `graph.add_edge`. The graph therefore retains both connectivity and inspectable physical information.

Segments in this model have the straight-line distance between their endpoints. A curved fiber’s actual length should instead be measured along its centerline and will generally exceed endpoint separation. Junction coordinates and physical path length can be stored separately. Straight segments are part of this example’s definition, allowing every length to be checked from coordinates. Conductivity times cross-sectional area is set to 1 μS·μm for every edge, giving conductance 1 μS for a 1 μm segment and approximately 0.714286 μS for a 1.4 μm segment.

$$
\ell_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2},\qquad g_{ij}=\frac{c}{\ell_{ij}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | dimensionless endpoint node identifiers |
| ![Formula](https://ml-biomat.com/static/agent-math/5e1d0f9befd63fa0c25bf752.svg) | two-dimensional endpoint coordinates, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/659018cdf6f28f6d2e140c19.svg) | straight segment length, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/7ad8fca1bb04c3d5470a60b3.svg) | segment conductance, μS |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | material conductivity times segment cross-sectional area, uniformly 1 μS·μm here |

The Pythagorean relation combines coordinate differences into length. Resistance of a uniform ohmic segment is proportional to length; conductance is its reciprocal, giving inverse-length scaling for fixed c. Nodes 0 and 3 differ by 0 and 1.4 μm, so length is 1.4 μm and conductance 1/1.4≈0.714286 μS. A curved segment uses its centerline path length, with c determined by material and cross-section.

A coordinate drawing and an adjacency matrix show the same connections in two ways. Matrix entry i,j records whether nodes i and j connect, or stores the weight of that connection; here it stores edge conductance. In an undirected network, i–j and j–i represent the same connection, so the matrix is symmetric. With no self-connections, its diagonal is zero. The node order must be retained when reading the matrix; this example explicitly uses 0 through 12. Reordering nodes moves bright entries without changing the physical network.

![Geometry and conductance adjacency of the same 13-node teaching network. Node 0 is at 1 V and node 11 at 0 V; color encodes potential and line width current magnitude.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ee7d26f0d70d655d2c80905f.svg?v=ee7d26f0d70d)

Figure 2Geometry and conductance adjacency of the same 13-node teaching network. Node 0 is at 1 V and node 11 at 0 V; color encodes potential and line width current magnitude. Every network uses the same current-to-width scale: 0–0.4 μA maps to 1–6 points.

Line thickness represents computed current magnitude, node color represents potential, and position retains micrometre coordinates. The branch from node 5 to node 12 is particularly informative. It belongs to the connected network but ends without another voltage boundary, so it carries no sustained current at steady state. Its line is thin and both endpoints have the same potential. The adjacency matrix still includes the edge because an existing connection and current under a particular boundary condition have different meanings.

## Ask whether a route exists before asking which is shortest

`nx.connected_components` groups mutually reachable nodes into sets. The original network has one set containing all 13 nodes. Removing 2–6 creates sets of seven and six nodes. Terminals 0 and 11 lie in different sets, so `nx.has_path` is false. The shortest route length is then recorded as missing rather than zero. A zero length means the starting point is already at the destination; no path means the destination cannot be reached. Summary tables and subsequent averages must preserve that distinction.

A shortest-path question must also specify what “short” measures. Without weights, it usually means the fewest edges. With `length_um` as the weight, it means the smallest sum of segment lengths. NetworkX lets the caller name that attribute explicitly. All lengths here are positive and support weighted shortest-path calculation. We save both the sequence of visited nodes and the total length, allowing the numerical result to be followed through the corresponding structure.

$$
L(\mathcal P)=\sum_{(i,j)\in\mathcal P}\ell_{ij}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/15e02dd85393a0816f232b0e.svg) | a source-to-sink path formed from consecutive adjacent edges, no units |
| ![Formula](https://ml-biomat.com/static/agent-math/e17a5d4458b8339cc8b3a6f3.svg) | total length of the path, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/659018cdf6f28f6d2e140c19.svg) | length of the path segment from node i to j, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/bd09c4dd97c45db77a3fdd7f.svg) | sum each edge length once along the path |

Travel length is the sum of segment lengths. Along 0→1→2→6→10→11, four segments are 1 μm and diagonal 6–10 is √(1²+1.4²)≈1.720465 μm, giving 5.720465 μm. The weighted shortest path minimizes this sum among available routes. When no route exists, length is missing.

One shortest route in the original graph is 0→1→2→6→10→11, with total length approximately 5.720465 μm. Four segments each have length 1 μm. The diagonal 6–10 has horizontal and vertical differences of 1 and 1.4 μm and length approximately 1.720465 μm. The program sums these five edge attributes directly. This shortest route does not carry all the current by itself: other conducting paths also contribute according to the potential differences throughout the network. Determining that distribution requires conservation equations.

Degree counting provides another quick construction check. Every undirected edge has two endpoints, so the sum of all node degrees equals twice the edge count. Eighteen edges here give total degree 36, which the program asserts. If an edge table accidentally repeats a connection, a simple graph may merge its rows and have fewer edges than the table. Return to the records to decide whether they are duplicates or genuinely distinct routes. A successful drawing alone cannot resolve that scientific distinction.

## Using current conservation to make a physical graph model

Current through a resistive edge equals its conductance times the potential difference between its endpoints. Potential can be compared with water level and conductance with the amount a channel passes per unit level difference, although the quantities calculated here remain voltage and electrical current. Node 0 is fixed at 1 V and node 11 at 0 V; the remaining potentials are unknown. At steady state, an internal junction does not continually accumulate charge, so its outgoing currents sum to zero. Whatever enters through some edges must leave through others.

$$
I_{ij}=g_{ij}(V_i-V_j),\qquad \sum_{j\in\mathcal N(i)}I_{ij}=0,\qquad G=\frac{I_{\rm source}}{V_{\rm source}-V_{\rm sink}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3aad26c22f336550c6187e70.svg) | edge current counted positive from i toward j, μA |
| ![Formula](https://ml-biomat.com/static/agent-math/7ad8fca1bb04c3d5470a60b3.svg) | edge conductance, μS |
| ![Formula](https://ml-biomat.com/static/agent-math/527ff599b45245d7294c413d.svg) | node potentials, V |
| ![Formula](https://ml-biomat.com/static/agent-math/ea20a3fb6af0124421780ca7.svg) | set of nodes directly adjacent to internal node i, no units |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | sum outward currents over adjacent edges; zero balance applies at internal nodes |
| ![Formula](https://ml-biomat.com/static/agent-math/a50cb44584a6811e306c7faa.svg) | total current entering the network from the fixed source, μA |
| ![Formula](https://ml-biomat.com/static/agent-math/fe06f954ddff36872452979f.svg) | fixed source and sink potentials, 1 V and 0 V here |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | effective conductance between the specified terminals, μS |

Conductance times potential difference gives current: μS times V is μA. Internal nodes accumulate no charge at steady state, so outward currents sum to zero. A 1 μS edge at 0.8 and 0.6 V carries 0.2 μA in the stated direction. The original network admits 0.276577085 μA under 1 V, giving G≈0.276577085 μS. The model assumes linear ohmic edges, ideal junctions, and fixed DC potentials.

Writing this balance at every internal node produces a linear system. NetworkX’s `laplacian_matrix` builds its coefficients from connectivity and edge conductance. A diagonal entry is the sum of incident conductances; an off-diagonal entry is the negative of the corresponding edge conductance. The code moves terms involving fixed-potential nodes to the right-hand side and solves for remaining potentials with `np.linalg.solve`. The signs and structure come directly from potential differences in the current law.

The original network’s end-to-end conductance is approximately 0.276577 μS. Under a 1 V boundary difference, approximately 0.276577 μA leaves the source and enters the sink. Internal current imbalance is below 10⁻¹² μA at every other node. This check directly tests conservation and can expose indexing, orientation, or sign errors. Current signs depend on the chosen bookkeeping direction for an edge: swapping its endpoints reverses the sign, while current magnitude and total network conductance remain unchanged.

Connected components also identify how a potential problem should be solved. A component connected to both voltage boundaries requires internal potentials to be calculated. A component connected to a single fixed boundary has uniform steady potential and no sustained internal current. A completely floating component has no prescribed absolute potential, so that value is recorded as missing. After removing 5–12, isolated node 12 falls into the last case and is drawn as an open marker. Treating these cases separately avoids solving a matrix without a potential reference and keeps the physical meaning of each result explicit.

## Running the example and comparing every single-edge removal

The complete program includes network construction, connectivity analysis, weighted paths, steady potentials, and plotting. It analyzes the original network and each of its 18 single-edge removals, then adds the redundant edge 5–9 and analyzes removals of the resulting 19 edges. Including the unchanged network in each group gives 19 plus 20, or 39 states. Every state retains components, bridges, a shortest route, node potentials, edge currents, and effective conductance, keeping the figures and interaction connected to one dataset.

### Run the complete network example

Use zh for Chinese figures.

```
python main.py --output results --language en
```

### Network structure, steady current, and 39 connectivity states

Use NetworkX graphs, components, bridges, paths, and the Laplacian; NumPy solves potentials.

```
"""Analyze a constructed material network using NetworkX and resistor balance."""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch

COORDINATES = {0:(0,0),1:(1,0),2:(2,0),3:(0,1.4),4:(1,1.4),5:(2,1.4),
               6:(3,0),7:(4,0),8:(5,0),9:(3,1.4),10:(4,1.4),11:(5,1.4),12:(2,2.7)}
BASE_EDGES = [(0,1),(1,2),(3,4),(4,5),(0,3),(1,4),(2,5),(1,5),
              (6,7),(7,8),(9,10),(10,11),(6,9),(7,10),(8,11),(6,10),
              (2,6),(5,12)]
BYPASS=(5,9)
SOURCE, SINK = 0,11



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def edge_id(u,v):
    return f'{min(u,v)}-{max(u,v)}'


def build_graph(bypass=False):
    graph=nx.Graph()
    for node,(x,y) in COORDINATES.items():
        graph.add_node(node,x_um=x,y_um=y)
    for u,v in BASE_EDGES+([BYPASS] if bypass else []):
        length=float(np.linalg.norm(np.array(COORDINATES[u])-COORDINATES[v]))
        graph.add_edge(u,v,length_um=length,conductance_uS=1/length,id=edge_id(u,v))
    return graph


def solve_potentials(graph):
    potentials={node:None for node in graph}
    for component in nx.connected_components(graph):
        boundary={node:value for node,value in [(SOURCE,1.0),(SINK,0.0)] if node in component}
        if not boundary:
            continue  # An isolated floating component has no prescribed absolute potential.
        if len(boundary)==1:
            potentials.update({node:next(iter(boundary.values())) for node in component})
            continue
        nodes=sorted(component);indices={node:i for i,node in enumerate(nodes)}
        matrix=nx.laplacian_matrix(graph.subgraph(component),nodelist=nodes,
                                   weight='conductance_uS').toarray()
        free=[indices[node] for node in nodes if node not in boundary]
        fixed=[indices[node] for node in boundary]
        values=np.array(list(boundary.values()))
        rhs=-matrix[np.ix_(free,fixed)]@values
        solution=np.linalg.solve(matrix[np.ix_(free,free)],rhs)
        potentials.update(boundary)
        potentials.update({nodes[index]:float(value) for index,value in zip(free,solution)})
    currents={};balance={node:0.0 for node in graph}
    for u,v,attr in graph.edges(data=True):
        current=0.0 if potentials[u] is None else attr['conductance_uS']*(potentials[u]-potentials[v])
        currents[edge_id(u,v)]=float(current if u<v else -current)
        balance[u]+=current;balance[v]-=current
    residual=max(abs(value) for node,value in balance.items() if node not in [SOURCE,SINK])
    return potentials,currents,float(balance[SOURCE]),float(balance[SINK]),float(residual)


def analyze(bypass,removed='none'):
    graph=build_graph(bypass)
    if removed!='none':
        u,v=map(int,removed.split('-'));graph.remove_edge(u,v)
    components=sorted([sorted(c) for c in nx.connected_components(graph)],key=lambda c:(-len(c),c))
    potential,current,source_current,sink_current,residual=solve_potentials(graph)
    connected=nx.has_path(graph,SOURCE,SINK)
    route=nx.shortest_path(graph,SOURCE,SINK,weight='length_um') if connected else []
    route_length=sum(graph.edges[u,v]['length_um'] for u,v in zip(route,route[1:])) if route else None
    degree=dict(graph.degree())
    assert sum(degree.values())==2*graph.number_of_edges()
    assert residual<1e-12 and abs(source_current+sink_current)<1e-12
    return {'bypass':bypass,'removed':removed,'nodes':graph.number_of_nodes(),'edges':graph.number_of_edges(),
            'components':components,'component_count':len(components),'largest_component':len(components[0]),
            'bridges':sorted(edge_id(u,v) for u,v in nx.bridges(graph)),
            'degree':degree,'route':route,'route_length_um':route_length,
            'potential_V':potential,'current_uA':current,'effective_conductance_uS':source_current,
            'sink_current_uA':sink_current,'max_internal_current_imbalance_uA':residual,
            'adjacency_uS':nx.to_numpy_array(graph,nodelist=sorted(graph),weight='conductance_uS').tolist()}


def draw_network(ax,state,language):
    graph=build_graph(state['bypass']);pos=COORDINATES
    if state['removed']!='none':
        u,v=map(int,state['removed'].split('-'))
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],color='#b64d34',ls='--',lw=2)
        graph.remove_edge(u,v)
    max_current=0.4  # microampere: shared line-width scale across every state
    for u,v in graph.edges:
        value=abs(state['current_uA'][edge_id(u,v)])
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],
                 color='#205b8c' if value>1e-12 else '#a9b4b9',lw=1+5*value/max_current,zorder=1)
    values=[state['potential_V'][n] if state['potential_V'][n] is not None else .5 for n in graph]
    scatter=ax.scatter([pos[n][0] for n in graph],[pos[n][1] for n in graph],c=values,cmap='viridis',
                        vmin=0,vmax=1,s=340,edgecolor='#172534',linewidth=1,zorder=3)
    floating=[n for n in graph if state['potential_V'][n] is None]
    if floating:
        ax.scatter([pos[n][0] for n in floating],[pos[n][1] for n in floating],
                    s=340,facecolor='#faf9f5',edgecolor='#82949e',linewidth=1.5,zorder=4)
    for n in graph:
        ax.text(pos[n][0],pos[n][1]+.20,str(n),ha='center',va='bottom',fontsize=13)
    ax.set(xlim=(-.45,5.45),ylim=(-.5,3.2),xlabel='x / μm',ylabel='y / μm')
    ax.set_aspect('equal');ax.grid(alpha=.15)
    return scatter


def figures(states,output,language):
    zh=language=='zh';tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':available_plot_fonts() if zh else ['DejaVu Sans'],'font.size':13,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'axes.unicode_minus':False,'svg.fonttype':'none'})
    find=lambda bypass,removed:next(s for s in states if s['bypass']==bypass and s['removed']==removed)
    base=find(False,'none')
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(output/f'{name}-{language}.{ext}',dpi=160,bbox_inches='tight',facecolor='#faf9f5')
        plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,6),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
    scatter=draw_network(axes[0],base,language)
    axes[0].set_title(tr('几何位置、节点电势与边电流','Geometry, node potential, and edge current'))
    fig.colorbar(scatter,ax=axes[0],label=tr('电势 / V','Potential / V'),shrink=.65)
    im=axes[1].imshow(base['adjacency_uS'],cmap='Blues',vmin=0,vmax=1)
    axes[1].set(xticks=range(13),yticks=range(13),xlabel=tr('节点编号','Node index'),ylabel=tr('节点编号','Node index'),title=tr('同一网络的加权邻接矩阵','Weighted adjacency of the same network'))
    axes[1].tick_params(labelsize=12.5);fig.colorbar(im,ax=axes[1],label=tr('边电导 / μS','Edge conductance / μS'),shrink=.65)
    save(fig,'network-and-matrix')
    scenarios=[find(False,'none'),find(False,'2-6'),find(False,'5-12'),find(True,'2-6')]
    titles=[tr('原网络','Original'),tr('移除2–6','Remove 2–6'),tr('移除5–12','Remove 5–12'),tr('增加5–9后移除2–6','Add 5–9, then remove 2–6')]
    fig=plt.figure(figsize=(13,10),layout='constrained');gs=fig.add_gridspec(3,2,height_ratios=[1.2,1.2,.85])
    for j,state in enumerate(scenarios):
        ax=fig.add_subplot(gs[j//2,j%2]);draw_network(ax,state,language)
        ax.set_title('ABCD'[j]+'  '+titles[j]+f"\nG = {state['effective_conductance_uS']:.4f} μS",fontsize=14)
    ax=fig.add_subplot(gs[2,0]);other=fig.add_subplot(gs[2,1])
    colors=['#205b8c','#b64d34','#82949e','#2b7c73']
    ax.bar(range(4),[s['effective_conductance_uS'] for s in scenarios],color=colors)
    other.bar(range(4),[s['largest_component'] for s in scenarios],color=colors)
    for axis in [ax,other]:axis.set_xticks(range(4),['A','B','C','D'])
    ax.set_ylabel(tr('端到端电导 / μS','End-to-end conductance / μS'));other.set(ylabel=tr('最大连通分量节点数','Nodes in largest component'),ylim=(0,14))
    for j,state in enumerate(scenarios):
        ax.text(j,state['effective_conductance_uS']+.008,f"{state['effective_conductance_uS']:.3f}",ha='center',fontsize=12)
        other.text(j,state['largest_component']+.3,str(state['largest_component']),ha='center',fontsize=12)
    save(fig,'removal-and-redundancy')
    fig=plt.figure(figsize=(13,7.5),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.7,1])
    ax=fig.add_subplot(gs[:,0]);degree_ax=fig.add_subplot(gs[0,1]);text_ax=fig.add_subplot(gs[1,1]);text_ax.axis('off')
    positions={'A':(0,0),'B':(-1.7,1.6),'C':(-1.7,-1.6),'D':(1.8,0)}
    edges=[('A','B',.18),('A','B',-.18),('A','C',.18),('A','C',-.18),('A','D',0),('B','D',-.18),('C','D',.18)]
    historic=nx.MultiGraph();historic.add_edges_from((u,v) for u,v,_ in edges)
    for j,(u,v,rad) in enumerate(edges):
        ax.add_patch(FancyArrowPatch(positions[u],positions[v],connectionstyle=f'arc3,rad={rad}',arrowstyle='-',
                     color='#b64d34' if j==6 else '#205b8c',linewidth=3,linestyle='--' if j==6 else '-',shrinkA=25,shrinkB=25))
    for node,(x,y) in positions.items():
        ax.scatter(x,y,s=1500,color='#e3ebee',edgecolor='#172534',zorder=3)
        ax.text(x,y,node,ha='center',va='center',fontsize=19)
        ax.text(x,y-.40,tr('度数 ','degree ')+str(historic.degree[node]),ha='center',fontsize=13,
                bbox=dict(facecolor='#faf9f5',edgecolor='none',pad=1.5),zorder=5)
    ax.set(xlim=(-2.5,2.6),ylim=(-2.4,2.5));ax.set_aspect('equal');ax.axis('off')
    ax.set_title(tr('Euler七桥问题：保留四块陆地与七条连接','Euler’s seven bridges: four regions, seven links'),fontsize=14)
    degree_ax.barh(list(historic),[historic.degree[n] for n in historic],color='#205b8c');degree_ax.set(xlabel=tr('关联桥的条数','Number of incident bridges'),xticks=range(6),title=tr('四个节点的度数都为奇数','All four vertices have odd degree'))
    text_ax.text(0,.95,'Euler · E53 · 1741',fontsize=20,weight='bold',transform=text_ax.transAxes)
    text_ax.text(0,.64,'A → B → A → C → A → D → B',fontsize=15,color='#205b8c',transform=text_ax.transAxes)
    text_ax.text(0,.34,tr('已走六座桥；停在B，余下C–D\n经过中间节点，进入与离开必须成对。','Six bridges used; at B, C–D remains.\nAt an intermediate vertex, arrivals pair with departures.'),fontsize=14,linespacing=1.8,transform=text_ax.transAxes)
    save(fig,'euler-bridge-parity')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('results'))
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    states=[]
    for bypass in [False,True]:
        graph=build_graph(bypass)
        for removed in ['none']+sorted(edge_id(u,v) for u,v in graph.edges):states.append(analyze(bypass,removed))
    base=states[0];bridge=next(s for s in states if not s['bypass'] and s['removed']=='2-6');leaf=next(s for s in states if not s['bypass'] and s['removed']=='5-12')
    assert base['nodes']==13 and base['edges']==18 and base['bridges']==['2-6','5-12']
    assert bridge['largest_component']==7 and bridge['component_count']==2 and abs(bridge['effective_conductance_uS'])<1e-12
    assert leaf['largest_component']==12 and abs(leaf['effective_conductance_uS']-base['effective_conductance_uS'])<1e-12
    assert abs(base['current_uA']['5-12'])<1e-12
    graph=build_graph(True)
    nodes=[{'id':n,**graph.nodes[n]} for n in graph]
    edges=[{'u':u,'v':v,**attr,'bypass':edge_id(u,v)==edge_id(*BYPASS)} for u,v,attr in graph.edges(data=True)]
    pd.DataFrame(nodes).to_csv(args.output/'nodes.csv',index=False);pd.DataFrame(edges).to_csv(args.output/'edges.csv',index=False)
    pd.DataFrame([{k:s[k] for k in ['bypass','removed','edges','component_count','largest_component','route_length_um','effective_conductance_uS']} for s in states]).to_csv(args.output/'removal-comparison.csv',index=False)
    (args.output/'lab-data.json').write_text(json.dumps({'nodes':nodes,'edges':edges,'states':states}),encoding='utf8')
    summary={'data_identity':'constructed 13-node resistor-network teaching model','states':len(states),'baseline':base,'bridge_removed':bridge,'leaf_removed':leaf}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    figures(states,args.output,args.language)
    print(json.dumps({'nodes':base['nodes'],'edges':base['edges'],'states':len(states),'conductance_uS':base['effective_conductance_uS'],'route':base['route'],'route_length_um':base['route_length_um'],'bridges':base['bridges'],'imbalance_uA':base['max_internal_current_imbalance_uA']}))


if __name__=='__main__':main()
```

`build_graph` creates a fresh graph for each case so that one removal cannot accidentally carry into later comparisons. `analyze` removes at most one edge from that fresh instance and computes structural and physical quantities. Notice the two weight names: shortest paths use `length_um`, while potential equations use `conductance_uS`. If conductance were supplied as a path cost, a shortest-path algorithm would prefer numerically smaller conductances and answer a different question. Explicit attribute names and units help prevent a correct function call from quietly addressing the wrong scientific problem.

After execution, `nodes.csv` and `edges.csv` expose the constructed geometry and attributes as tables. `removal-comparison.csv` summarizes each state, while `summary.json` retains selected detailed cases. The program checks independently that the original bridges are 2–6 and 5–12, that deleting 2–6 disconnects the terminals, and that deleting 5–12 leaves effective conductance unchanged. The last check uses the physical reasoning that a dangling branch carries zero steady current, complementing node and edge counts.

## Why can removing one edge have very different effects?

Removing 2–6 and removing 5–12 both increase the component count from one to two, so both edges qualify as bridges. The first separates source and sink and reduces conductance to zero. The second isolates a dangling endpoint while retaining the conducting paths, leaving conductance approximately 0.276577 μS. Their largest components contain seven and twelve nodes respectively. A structural index gains meaning from the task: both edges matter for keeping every node connected, while their roles in steady transport between nodes 0 and 11 differ substantially.

![Cases A–D compare the original network, main-connection loss, dangling-end removal, and main-connection loss with redundancy. Open nodes have no prescribed absolute potential; lower panels compare conductance and largest component.](https://ml-biomat.com/static/tutorials/python-scientific/figures/87f6921bbcc06e08acecab8d.svg?v=87f6921bbcc0)

Figure 3Cases A–D compare the original network, main-connection loss, dangling-end removal, and main-connection loss with redundancy. Open nodes have no prescribed absolute potential; lower panels compare conductance and largest component. Every network uses the same current-to-width scale: 0–0.4 μA maps to 1–6 points.

Adding 5–9 gives the two main regions another route, so 2–6 is no longer their unique connection. Conductance of the intact network increases to approximately 0.368931 μS. If 2–6 is then removed, current can pass through 5–9; the network stays connected and conductance is approximately 0.276577 μS. The corresponding geometry and edge weights in this teaching network make the remaining alternative reproduce the original value. In a general material, alternative paths have different lengths, cross-sections, and contact resistances, and the retained conductance changes accordingly.

### Connectivity, paths, and current change together

[Figure: Fixed geometry, potentials, currents, and shortest route](https://ml-biomat.com/tutorials/python-scientific/s02/en/#S02-network)

[Figure: Conductance adjacency for the same state](https://ml-biomat.com/tutorials/python-scientific/s02/en/#S02-matrix)

[Figure: Conductance after removing each edge separately](https://ml-biomat.com/tutorials/python-scientific/s02/en/#S02-compare)

Purple dashes show a shortest route; red dashes show the removed edge. Open nodes have no prescribed absolute potential.

With the redundant connection disabled, compare removal of 2–6, 5–12, and 1–4. Follow the node grouping, shortest route, and effective conductance together. Then enable the redundant edge while retaining removal of 2–6, and observe the redistribution of potentials and currents. The adjacency matrix removes the corresponding pair of symmetric entries, while the single-edge comparison highlights the current choice. You can also find a removal that retains connectivity while appreciably lowering conductance, then return to the network to inspect which parallel routes it affects.

The interaction selects among 39 states actually computed with NetworkX and the linear solver. All currents use the same voltage boundaries. Geometric coordinates remain fixed during comparisons, preventing an automatic layout from moving nodes and creating an apparent structural difference. Recording the redundant-edge setting and removed-edge identifier is sufficient to reproduce the same numerical state in the Python example.

## Moving from a teaching graph to microscopy and materials

When building a graph from microscopy, decide first what a node represents. Fiber junctions can become nodes and fiber segments between them become edges. Alternatively, particles can become nodes and physical contacts become edges. These choices describe different structural scales. Two crossing lines in a projection do not automatically establish a three-dimensional connection; contact identification should account for depth, resolution, and the material mechanism. Clear node and edge definitions support consistent interpretation of components and paths.

Physical weights depend on the question. Electrical transport requires conductivity, cross-sectional area, and contact resistance. Flow requires channel geometry and its flow-resistance relation. Mechanical response additionally requires segment directions, stretching and bending stiffnesses, and loading conditions. Connectivity analysis locates isolated regions and critical connections, while quantitative transport or load-bearing behavior requires its corresponding physical equations. This resistor network demonstrates one complete connection: describe the graph, assign a dimensional edge law, and impose conservation at nodes.

NetworkX keeps these steps readable. Node and edge tables define the object, graph algorithms answer structural questions, numerical matrices calculate response, and figures relate both to one set of identifiers. Edge removal also shows why useful metrics usually follow a specific task, rather than a list of every centrality, clustering, or path function available. Organizing the analysis around reachability, alternative routes, and transport capacity turns a complex material’s connections into conclusions that can be checked.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NetworkX tutorial](https://networkx.org/documentation/stable/tutorial.html)

   Open tutorial foundation for graph objects, attributes, traversal, and analysis.

   NetworkX BSD-3-Clause; original chapter text and implementation.
2. [NetworkX bridges](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bridges.bridges.html)

   Bridge definition based on increased component count after removal.

   NetworkX BSD-3-Clause.
3. [NetworkX weighted shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html)

   Shortest paths with an explicitly specified edge weight.

   NetworkX BSD-3-Clause.
4. [Euler Archive E53: Solutio problematis ad geometriam situs pertinentis](https://scholarlycommons.pacific.edu/euler-works/53/)

   Primary-paper archive, degree argument, and 1741 publication record.

   Historical citation; newly drawn explanatory graph.
