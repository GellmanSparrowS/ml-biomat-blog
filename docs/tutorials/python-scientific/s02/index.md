# 把材料连接关系写成图

Source: https://ml-biomat.com/tutorials/python-scientific/s02/
Language: zh-CN

从节点与边到连接、最短路和电流守恒，比较断开与备用连接怎样改变材料网络。

## 材料里的连接，为什么值得单独研究

一层导电纤维薄膜看起来像许多线交织在一起，但真正决定电流能否从一端到另一端的，是哪些交点确实连接、哪些线段形成通路。多孔材料中的流体通道、水凝胶里的交联关系和细胞之间的接触，也会遇到相似问题。几何形状告诉我们它们在哪里，连接关系告诉我们可以从哪里到哪里。NetworkX擅长表示和计算后一类信息，并允许把长度、半径、电导等物理量附着在连接上，使结构描述逐步进入科学计算。

本章构造一个13个节点的二维教学网络，把节点看作理想连接点，把边看作导电线段。坐标单位为微米，线段采用相同的材料电导率与截面积乘积，节点0和11分别接1 V与0 V。我们会比较三种问题：两端是否相通，哪条路线最短，全部通路共同能传递多少电流。随后移除一条边，或者增加一条备用连接，看这些答案怎样同时变化。所有结果由明确构造的网络计算得到，可以逐条检查节点和边的定义。

这三种问题不能由一个指标代替。一个只有极细长通道的网络可以相通，却具有很小电导；两条路线的最短长度相同，也可能因为并联通路数量不同而表现出不同导电能力。把这些问题依次展开，既能理解NetworkX的对象和算法，也能学会为材料选择有物理意义的图属性。后续处理显微图像提取的骨架或分子连接表时，首先要把原始结构转成同样清楚的节点表和边表。

## 从七座桥到图：保留解决问题需要的信息

Euler研究柯尼斯堡七桥问题时，关心的是能否走一条路线，恰好经过每座桥一次。他把陆地的具体轮廓和街道距离放到一边，保留四块陆地之间由哪座桥相连。收录为E53、于1741年发表的论文，将问题推进到每个位置关联多少条连接。今天把位置称为节点，把连接称为边；一个节点连接的边数叫作度数。这样的抽象并没有让问题变空泛，而是保留了决定能否完成行走的结构。

![Euler七桥问题的多重图及度数。所示路线走过六条蓝边，余下一条红虚边；四个奇数度节点给出一般的不可能性理由。](https://ml-biomat.com/static/tutorials/python-scientific/figures/aa63a24b9b6ee9e712641790.svg?v=aa63a24b9b6e)

图 1Euler七桥问题的多重图及度数。所示路线走过六条蓝边，余下一条红虚边；四个奇数度节点给出一般的不可能性理由。

可以沿图中的A→B→A→C→A→D→B走六座桥，此时停在B，还剩C与D之间的一座桥。换一条路线能否成功，不能靠这一条尝试就下结论。Euler式的推理看的是每个中间节点：进入一次就需要离开一次，关联边必须成对使用。只有起点和终点可以各多出一条未配对的边，所以一条使用每条边一次的开放路线最多有两个奇数度节点；闭合路线则要求所有节点的度数为偶数。七桥图有四个奇数度节点，因此整个问题没有这样的路线。

这段历史也直接影响数据结构选择。A与B之间有两座不同的桥，A与C之间也有两座，应该使用允许同一对节点存在多条边的`MultiGraph`；若使用普通`Graph`重复添加同一对节点，第二次添加会更新已有连接，七座桥就会被错误合并。我们的材料例子规定每对连接点最多保留一条等效线段，因此使用无向简单图`Graph`。若实验里两根不同纤维连接同一对节点，可以保留多重边，或者按明确的物理规则合并成一条等效边。

图论中的“桥边”还有一个精确含义：删除它以后，连通分量数会增加。它与七桥故事中的实体桥并不是同一个判断。七桥图的每条实体桥都可以绕路，而材料例子中的某条线段可能恰好是两个区域间唯一的连接。记住这一点，就能在读`nx.bridges`时理解它计算的是结构上的不可替代连接，而不是按照线段形状或名字寻找一座桥。

## 用节点表与边表把材料写清楚

节点表每行保存一个稳定编号及其坐标，例如节点0位于(0,0) μm，节点1位于(1,0) μm。边表每行给出两个端点，随后附上长度和电导。编号只是身份，不是距离：编号0到11的差为11，并不能说明它们相距11 μm。代码把坐标作为节点属性，用`graph.add_node`保存；把长度和电导作为边属性，用`graph.add_edge`保存。一个图因此同时具有连接结构和可查阅的物理信息。

本例线段采用两个端点之间的直线长度。实际弯曲纤维的长度应沿着纤维中心线测量，通常比端点直线距离更长；节点坐标与边的实际路径长度可以分别保存。这里采用直线是模型定义的一部分，使每条长度都能从坐标直接核对。所有线段的电导率与截面积乘积取1 μS·μm，因此长度1 μm的边电导为1 μS，长度1.4 μm的边电导约为0.714286 μS。

$$
\ell_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2},\qquad g_{ij}=\frac{c}{\ell_{ij}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 两个端点的节点编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/5e1d0f9befd63fa0c25bf752.svg) | 端点二维坐标，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/659018cdf6f28f6d2e140c19.svg) | 直线线段长度，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/7ad8fca1bb04c3d5470a60b3.svg) | 线段电导，μS |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | 材料电导率与线段截面积的乘积，本例统一取1 μS·μm |

勾股关系将两个坐标差合成长度。均匀截面的欧姆导体电阻与长度成正比，电导为电阻倒数，因此在c相同时电导与长度成反比。节点0与3相差0和1.4 μm，长度1.4 μm，电导1/1.4≈0.714286 μS。对弯曲线段，应把中心线路径长度代入，且实际c由材料与截面决定。

坐标图和邻接矩阵是同一组连接的两种视图。矩阵的第i行、第j列记录节点i与j是否相连，或记录这条边的权重；本例存边电导。无向网络中i到j与j到i代表同一连接，因此矩阵关于对角线对称；没有自连接，对角线为零。读矩阵时需要保留节点顺序，本例明确使用0到12。若换一种排列，亮格的位置会变化，实际网络却没有改变。

![同一13节点教学网络的几何图与电导邻接矩阵。节点0为1 V，11为0 V；节点颜色为电势，边宽为电流幅值。](https://ml-biomat.com/static/tutorials/python-scientific/figures/c86d065cfe2b3119f31f2663.svg?v=c86d065cfe2b)

图 2同一13节点教学网络的几何图与电导邻接矩阵。节点0为1 V，11为0 V；节点颜色为电势，边宽为电流幅值。 所有网络图使用相同电流线宽尺度：0–0.4 μA对应1–6点线宽。

图中的线宽表示计算得到的电流幅值，节点颜色表示电势，位置则保留微米坐标。节点5通向节点12的悬挂支路很容易看到：它属于整个连通网络，但末端没有接到另一个电压边界，在稳态时没有持续电流。边5–12的线宽较细，两个端点电势相同；邻接矩阵仍保留这条边，因为“存在连接”和“当前条件下有电流”是不同的数据含义。

## 先问是否相通，再问哪条路最短

`nx.connected_components`把可以相互到达的节点分成集合。原网络只有一个集合，包含13个节点；去掉2–6以后分成两个集合，分别含7个和6个节点。节点0与11落在不同集合中，`nx.has_path`返回假，这时“最短路径长度”应记录为空值，而不是零。零长度意味着起点已经在终点，无路径则意味着根本无法到达，两者在汇总表和后续平均中必须保持区别。

路径问题还要明确“短”指什么。没有权重时，最短路径通常指经过的边最少；以`length_um`为权重时，比较的是沿途长度相加。NetworkX允许在调用时明确指定这项属性。本例所有长度为正，适合使用最短路径算法；每一步经过的节点列表与加和后的长度一起保存，读者既能读到一个数，也能在结构图上追踪它经过了哪些边。

$$
L(\mathcal P)=\sum_{(i,j)\in\mathcal P}\ell_{ij}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/15e02dd85393a0816f232b0e.svg) | 由连续相邻边构成的一条源到汇路径，无单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/e17a5d4458b8339cc8b3a6f3.svg) | 该路径总长度，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/659018cdf6f28f6d2e140c19.svg) | 路径上节点i到j这一段的长度，μm |
| ![Formula](https://ml-biomat.com/static/agent-math/bd09c4dd97c45db77a3fdd7f.svg) | 沿路径把每条边长度加一次的求和记号 |

沿路线走过的总长度是各段长度之和。路径0→1→2→6→10→11中，四段为1 μm，斜段6–10长√(1²+1.4²)≈1.720465 μm，总长5.720465 μm。加权最短路径在所有可行路径中选择这个和最小的路径；没有可行路径时长度为空值。

原网络从0到11的一条最短路线是0→1→2→6→10→11，长度约为5.720465 μm。其中四段各长1 μm，6–10是一条水平、竖直差分别为1与1.4 μm的斜边，长约1.720465 μm。程序直接由边表把这五段加起来。最短路线并不意味着所有电流都集中走这一条路：只要其他通路也有电导，电流就会按整个网络的电势差分配，这需要下一步的守恒计算。

检查度数还能快速发现建图问题。每条无向边有两个端点，因此所有节点的度数相加应该等于边数的两倍。本例18条边对应总度数36，代码把这件事写成断言。如果一份原本应当简单的表重复记录同一条边，普通图可能把它合并，边数就与原表行数不同；这时应回到表格判断是重复记录还是两条真实通路，而不是仅凭图能画出来就忽略差别。

## 让电流守恒，把连接图变成可求解的物理模型

在电阻网络里，一条边上的电流等于该边电导乘两端电势差。电势可以类比水位，电导可以类比通道在单位水位差下的通流能力，但这里计算的量仍然是电压和电流。节点0被固定在1 V，节点11固定在0 V，其余节点的电势需要求解。稳态时，中间节点不持续积累电荷，因此流出的电流总和为零；从一边流入的电流必须从其他边流出。

$$
I_{ij}=g_{ij}(V_i-V_j),\qquad \sum_{j\in\mathcal N(i)}I_{ij}=0,\qquad G=\frac{I_{\rm source}}{V_{\rm source}-V_{\rm sink}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3aad26c22f336550c6187e70.svg) | 按节点i流向j记正的边电流，μA |
| ![Formula](https://ml-biomat.com/static/agent-math/7ad8fca1bb04c3d5470a60b3.svg) | 该边电导，μS |
| ![Formula](https://ml-biomat.com/static/agent-math/527ff599b45245d7294c413d.svg) | 节点电势，V |
| ![Formula](https://ml-biomat.com/static/agent-math/ea20a3fb6af0124421780ca7.svg) | 与内部节点i直接相连的邻居集合，无单位 |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对所有邻边按流出方向相加；只在内部节点令总和为零 |
| ![Formula](https://ml-biomat.com/static/agent-math/a50cb44584a6811e306c7faa.svg) | 从固定源端流入网络的总电流，μA |
| ![Formula](https://ml-biomat.com/static/agent-math/fe06f954ddff36872452979f.svg) | 源端与汇端固定电势，本例1 V与0 V |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | 两个指定端点之间的等效电导，μS |

电导乘电势差得到电流，μS乘V为μA；内部节点稳态不积累电荷，故流出电流总和为零。例如一条1 μS边两端为0.8 V与0.6 V，正向电流为0.2 μA。原网络在1 V差下流入0.276577085 μA，除以1 V得到G≈0.276577085 μS。该模型采用线性欧姆边、理想连接点和固定直流电势。

把每个中间节点的守恒式写在一起，会形成一个线性方程组。NetworkX的`laplacian_matrix`按照图的连接和边电导构造矩阵：对角线是该节点所有相连边的电导之和，非对角线是对应边电导的负值。代码把固定电势节点对应的项移到右边，对其余节点用`np.linalg.solve`求解。这个矩阵的正负结构来自电流差，不是为了使用矩阵而人为安排的格式。

原网络的端到端电导约为0.276577 μS。在1 V边界差下，源端流出约0.276577 μA，汇端流入同样大小的电流；所有内部节点的电流不平衡小于10⁻¹² μA。这个检查直接对应守恒条件，能够发现矩阵索引、边方向或符号的错误。电流的正负号依赖我们给边选择的记账方向，交换端点会改变符号，但不会改变实际电流大小或网络总电导。

连通分量也帮助处理求解条件。一个分量同时接到1 V与0 V边界时，需要求解内部电势；只接到一个固定边界时，稳态电势处处相同，没有内部持续电流；完全悬浮的分量没有给定绝对电势，记录为空值即可。删除5–12后，独立节点12就是最后一种情况，图中用空心点标识。分别处理这些情况，可以避免对没有电势基准的矩阵强行求逆，也保留了每个结果的物理含义。

## 运行完整例子，比较每一种单边移除

下面的程序包含网络构造、连接分析、加权路径、稳态电势求解和绘图。它先分析原网络以及逐条移除18条边的结果，再增加5–9这条备用边，分析19条边对应的单边移除。两组分别有19和20个状态，共39个。每个状态都保存连通分量、桥边、最短路线、节点电势、边电流和总电导，因此图表和交互可以沿着同一组数据相互检查。

### 运行完整网络例子

使用zh生成中文图。

```
python main.py --output results --language en
```

### 网络结构、稳态电流与39种连接状态

实际使用NetworkX建图、连通分量、桥边、路径和Laplacian；NumPy求解电势。

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

`build_graph`每次创建一个新图，避免一次移除意外影响后续对照；`analyze`只对当前副本执行一次移除，再计算结构与物理量。读代码时尤其留意两个权重名：最短路径使用`length_um`，电势矩阵使用`conductance_uS`。如果把电导当作路径代价，算法会偏好电导数值小的边，所回答的问题就发生变化。属性名和单位写清楚，可以防止这种“函数调用正确、科学问题错误”的混淆。

运行后，`nodes.csv`和`edges.csv`给出构造规则落实成的两张表，`removal-comparison.csv`按状态汇总结构与电导，`summary.json`保留几组重点结果。程序还独立检查原图的两条桥边是否为2–6和5–12、删除2–6是否切断两端、删除5–12是否保持总电导不变。最后一条检查用到了悬挂支路在稳态没有电流的物理推理，能够补充纯粹的节点和边计数。

## 同样少一条边，影响为何差这么多

删除2–6和删除5–12都会让连通分量数从1变成2，所以它们都被识别为桥边。但前者切断源端与汇端，电导降到零；后者只把悬挂末端变成一个独立节点，原来的导电通路保持，电导仍约0.276577 μS。最大连通分量分别包含7个与12个节点。这个对照说明，结构指标需要与研究任务结合：关心整个网络完整性时，两条边都重要；关心0到11的稳态导电时，它们的作用很不一样。

![A到D比较原网络、断开主连接、移除悬挂末端、增加备用边后断开主连接。空心节点没有指定绝对电势；下方分别比较电导与最大连通分量。](https://ml-biomat.com/static/tutorials/python-scientific/figures/a32126a2d5d0e1bdeaa3be46.svg?v=a32126a2d5d0)

图 3A到D比较原网络、断开主连接、移除悬挂末端、增加备用边后断开主连接。空心节点没有指定绝对电势；下方分别比较电导与最大连通分量。 所有网络图使用相同电流线宽尺度：0–0.4 μA对应1–6点线宽。

增加5–9后，原有2–6不再是两个主要区域间的唯一通路。完整网络的电导提高到约0.368931 μS；此时再删除2–6，电流可以经5–9绕行，网络仍连通，电导约0.276577 μS。这个教学网络具有对应的几何和边权关系，因此备用通路单独承担连接时恰好恢复到原电导。更一般的材料里，备用路线的长度、截面和接触电阻不同，保留下来的电导也会不同。

### 连接、路径与电流一起变化

[Figure: 固定几何网络、电势、电流和最短路](https://ml-biomat.com/tutorials/python-scientific/s02/#S02-network)

[Figure: 同一状态的电导邻接矩阵](https://ml-biomat.com/tutorials/python-scientific/s02/#S02-matrix)

[Figure: 每条边分别移除后的电导](https://ml-biomat.com/tutorials/python-scientific/s02/#S02-compare)

紫色虚线是一条最短路线；红色虚线是被移除的边。空心节点的绝对电势未指定。

先关闭备用连接，分别选择移除2–6、5–12和1–4，比较节点分组、最短路线和电导。再打开备用连接，保持移除2–6，观察电势颜色和边电流怎样重新分配。邻接矩阵同步删去对应的两个对称格子，单边移除比较图则突出当前选择。你也可以从比较图寻找一种“图仍然连通，但电导明显降低”的移除，回到网络结构中判断它影响了哪几条可并行工作的通路。

这组交互采用实际NetworkX与线性求解器预先算出的39种状态，页面选择已有状态进行同步展示。所有边电流都满足同一组边界条件；节点的几何坐标在比较中保持不变，避免布局算法移动节点造成视觉上的结构差异。记录备用边状态和被移除边的编号，就能在完整Python例子里复现同一组数值。

## 从教学图走向显微结构与材料问题

用显微结构建图时，首先确定节点代表什么。可以把纤维交叉点作为节点、两交叉点之间的纤维作为边，也可以把颗粒作为节点、真实接触作为边。两种定义会产生不同尺度的网络。二维投影里两条线相交，并不自动说明三维中存在连接；接触判定应结合层面、分辨率和材料机制。节点与边的定义越清楚，后续连通分量和路径的科学解释就越稳定。

物理权重则取决于研究对象。导电问题需要材料电导率、截面和接触电阻；流动问题需要通道形状及相应流阻规律；力学问题还需要线段方向、拉伸与弯曲刚度以及边界载荷。连通性分析可以定位孤立区域和关键连接，具体传输或承载能力要接上相应物理方程。本章的电阻网络提供了一种完整衔接方式：先描述连接，再为边赋予有单位的物理关系，最后在节点上施加守恒。

NetworkX让这些步骤保持可读：节点表和边表决定对象，图算法回答结构问题，矩阵与数值库计算物理响应，图形把两者放到同一套编号上。移除边的例子也提醒我们，最有用的指标往往来自一个具体任务，而不是把能调用的中心性、聚类系数和路径函数全部算一遍。围绕“能否相通、如何绕行、能传多少”组织分析，能够把复杂材料的连接关系逐步变成可检查的结论。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S02.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [NetworkX tutorial](https://networkx.org/documentation/stable/tutorial.html)

   图对象、属性、遍历与分析的开放教程基础。

   NetworkX BSD-3-Clause; original chapter text and implementation.
2. [NetworkX bridges](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bridges.bridges.html)

   删除边后连通分量增加的桥边定义。

   NetworkX BSD-3-Clause.
3. [NetworkX weighted shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html)

   明确指定边权的最短路径。

   NetworkX BSD-3-Clause.
4. [Euler Archive E53: Solutio problematis ad geometriam situs pertinentis](https://scholarlycommons.pacific.edu/euler-works/53/)

   七桥问题原论文档案、度数论证与1741年出版记录。

   Historical citation; newly drawn explanatory graph.
