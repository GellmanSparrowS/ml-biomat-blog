# Graph neural networks: learning through relationships

Source: https://ml-biomat.com/tutorials/machine-learning/m22/en/
Language: en

From local messages to GCN, GraphSAGE, GAT, and geometric equivariance: inspect how information travels along edges.

## 1. What disappears when we remove the connections?

It is raining in the evening, and you want to know whether the next bus will arrive crowded. The number of people currently at your stop matters, but so do passengers entering upstream stops and a disruption on a nearby subway line. Treating each stop as a separate row of numbers can discard the fact that people move along routes. Graph neural networks address problems in which information about an object is useful partly because of its relationships with other objects. Stops, documents, accounts, and mechanical parts can become nodes; routes, citations, transactions, and contacts can become edges. Deciding what an edge means is an earlier and more consequential choice than selecting a network architecture.

A graph here is a representation of relationships, rather than a statistical chart. Moving two drawn nodes farther apart does not change an abstract graph if their attributes and connections remain the same. There is also no natural left-to-right order: assigning different numbers to bus stops should preserve their individual congestion predictions. A graph model therefore receives both a feature array and relational structure. Its output might be a category for every node, a score for a possible connection, or a property of the whole graph. These tasks can share an information-processing mechanism, while requiring different labels, training losses, and evaluation splits.

We begin by passing a single column of numbers between a few nodes, then build and run a complete graph convolutional network, or GCN. Our synthetic network contains two communities with more connections within each community than between them. Individual observations are deliberately noisy, making the contribution of relational information measurable. We then ask what should change when neighbors deserve unequal attention, new nodes continually arrive, or objects have spatial coordinates. GCN, GraphSAGE, GAT, and geometric equivariant networks each respond to a concrete version of these questions.

## 2. Turning relationships into a computable matrix

Suppose three stops, A, B, and C, form a chain. A and C have no direct connection. An adjacency matrix is a table that records whether the node named by a row can receive a message from the node named by a column. The entry at row A, column B is one; the entry at row A, column C is zero. An undirected connection works both ways, producing a symmetric matrix. A one-way bus route needs its direction preserved. Node features belong in another matrix, X: each row describes a stop, and each column describes an observation, such as standardized passenger count, waiting time, or rainfall. Edges can carry attributes too, including travel duration.

$$
m_i=\sum_{j=1}^{N}A_{ij}x_j,\qquad \mathbf m=A\mathbf x
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of nodes, a dimensionless integer; this example uses one scalar feature per node. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Receiving and sending node indices, from 1 to N. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | N-by-N adjacency matrix; entry Aij is one when j sends to i, zero otherwise, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3e1f8a0b406959ab68838255.svg) | Scalar signal at node j and the N-component column vector; dimensionless standardized observations here. |
| ![Formula](https://ml-biomat.com/static/agent-math/63d7401d5988a965f904b548.svg) | Neighbor-signal sum and N-component result, in the same units as x. |

Each adjacency entry acts as a switch before summation, so matrix multiplication gathers precisely the permitted messages. On a three-node chain without self-loops, input (1,3,5) becomes (3,6,3). Adding self-loops makes the middle-node sum 1+3+5=9. Dividing by its three contributors gives mean 3. Summation and averaging are distinct operations; the next normalization specifies a particular weighting rule.

Matrix multiplication now has a physical interpretation: follow existing connections and add the numbers arriving from neighbors. If A, B, and C carry signals 1, 3, and 5, B receives a neighbor sum of 6. Including its own value makes the average of the three messages equal to 3. Imagine a small neighborhood meeting. The graph determines who is invited; the aggregation rule determines how their contributions are combined. Nothing has been learned yet. We have transported and combined observations. A neural network subsequently learns how these combined observations should be transformed into features useful for prediction.

This distinction helps explain the development of graph convolution. Graph signal processing studies how signals vary over irregular relational structures. Similar values at connected nodes represent relatively smooth variation along those relationships. In their ICLR 2017 GCN work, Kipf and Welling organized a local approximation to spectral graph convolution into a compact propagation rule for semi-supervised classification. Features and connectivity participate together. The original Distill illustration below shows neighboring information converging on a node. Follow the messages and their destination before memorizing the names of the boxes: the route of information is the central idea.

![Distill architecture diagram showing neighborhood pooling and node updates.](https://ml-biomat.com/static/tutorials/machine-learning/figures/959cd188a1cbd110dea60bdb.png?v=959cd188a1cb)

Figure 1Original architecture illustration: neighboring representations are pooled before updating node representations. Figure: Sanchez-Lengeling, Reif, Pearce, and Wiltschko, A Gentle Introduction to Graph Neural Networks, Distill (2021), https://distill.pub/2021/gnn-intro/, CC BY 4.0; unmodified.

Constructing a graph is already a modeling assumption. Distance-based edges suggest local interaction, citation edges record intellectual relationships, and transaction edges identify shared participants. None of these automatically means that connected nodes have the same class. An unusual account may interact mainly with ordinary accounts; adjacent transport stops can have very different passenger counts. Compare a graph model with a feature-only baseline, and inspect edge meaning, direction, and time. A relationship discovered after the prediction date belongs to the future of that prediction. Including it in a historical training graph changes the information available to the model.

## 3. GCN: gathering messages without letting degree dominate

A raw sum grows with the number of neighbors. A node connected to a hundred others can receive a much larger value than a node connected to two, even when every incoming observation is ordinary. GCN adds self-connections and weights each connection using the degrees of both its endpoints. The resulting symmetric normalization accounts for the receiving and sending nodes. It is different from dividing only by the receiver's neighborhood size. The two rules agree on a regular graph with equal degrees, but differ when some nodes are much more connected than others. This normalization gives subsequent transformations a more controlled numerical scale.

$$
\widetilde A=A+I_N,\quad \widetilde D_{ii}=\sum_j\widetilde A_{ij},\quad \widehat A=\widetilde D^{-1/2}\widetilde A\widetilde D^{-1/2},\qquad H^{(\ell+1)}=\operatorname{ReLU}(\widehat A H^{(\ell)}W^{(\ell)})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e40cf74018a825ff1b5a7b89.svg) | N-by-N undirected adjacency and identity matrices, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4fd6c496d6d7712a47e3912f.svg) | Adjacency with self-loops and its diagonal degree matrix, both N-by-N; degree counts contributors including self. |
| ![Formula](https://ml-biomat.com/static/agent-math/c47342559dd71b1b19dfe153.svg) | Symmetrically normalized propagation matrix, N-by-N; a present edge has weight 1/√(di dj), dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/fa29d7dba7af8c5436716754.svg) | Layer-ℓ representations of shape N-by-Fℓ and weights Fℓ-by-Fℓ₊₁; dimensionless hidden representations and weights, with H⁽⁰⁾=X. |
| ![Formula](https://ml-biomat.com/static/agent-math/90d899d413b08675e0bedf96.svg) | Layer index, channel count at that layer, and elementwise max(0,z); the code omits ReLU at the classification output. |

Left multiplication mixes nodes; right multiplication mixes feature channels. The shapes are (N×N)(N×Fℓ)(Fℓ×Fℓ₊₁). A three-node chain with self-loops has degrees 2, 3, 2. For input (1,3,5), the middle output before a learned transform is 1/√6+3/3+5/√6≈3.449, compared with the simple neighborhood mean 3. The difference comes from sender-degree normalization. When every degree is d, each present-edge coefficient reduces to 1/d.

The propagation matrix answers where information comes from; the learned weight matrix answers how feature channels are combined. If every node has six input numbers and the layer produces sixteen numbers, the input shape is number-of-nodes by six and the weight shape is six by sixteen. The output is number-of-nodes by sixteen. The same weights apply at every node, so the model does not learn an unrelated rule for each bus stop. ReLU replaces negative values with zero and introduces nonlinearity. Applying a second layer brings information from two-hop neighborhoods. Increasing depth enlarges the region that can influence a node, but a larger receptive field does not by itself guarantee more distinguishable representations.

During training, the network produces class scores for every node, while the supervised loss uses only nodes with training labels. The labels are not copied along edges as answers at each layer. Features and hidden representations are propagated. Labels influence shared weights through the loss gradient, and those weights influence predictions throughout the graph. In our experiment, all node features and the full graph are available during training, but only twenty node labels update the parameters. This is transductive node classification. A deployment problem involving next year's new nodes requires a split that reflects those new objects and the relationships available at their prediction times.

### Neighborhood lab: graph, matrix, and signal

Each step updates all nodes simultaneously from the previous state, including self-loops. Changing a parameter recomputes from the initial signal; the step button advances propagation once.

[Figure: Graph and current values at left, propagation matrix at right, node-signal bars below](https://ml-biomat.com/tutorials/machine-learning/m22/en/#M22-svg)

In the interaction, choose the mean rule, set the first node's signal to six, and advance one propagation step. Its change reaches adjacent nodes; another step carries the effect farther. Turning on the additional edge changes both the invitation list and its size. Switching to a sum reveals how highly connected positions can accumulate larger values. The interaction isolates aggregation with no trained parameters. It makes information movement inspectable, while the full Python example places graph propagation inside a trainable two-layer network.

## 4. GraphSAGE and GAT: welcoming new nodes and weighting opinions

A growing network acquires new stations, documents, and accounts. Memorizing a separate vector for every fixed node provides no immediate recipe for processing a new one. In GraphSAGE, published in 2017, Hamilton, Ying, and Leskovec emphasized a reusable neighborhood aggregation function and sampling to control computation. In a mean-aggregation version, the model averages sampled neighbor features, concatenates that result with the node's own representation, and applies a shared learned transformation and activation. It learns a way to process local observations. A new node with compatible features and available neighbors can therefore enter the same computational procedure.

$$
\overline h_i=\frac{1}{|S(i)|}\sum_{j\in S(i)}h_j,\qquad h_i'=\sigma\!\left(W[h_i\Vert\overline h_i]+b\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5681a4914647757834ffe88.svg) | Center node, neighbor index, sampled neighbor set, and its size; a nonempty set is assumed, with an explicit zero-neighbor convention for isolated nodes. |
| ![Formula](https://ml-biomat.com/static/agent-math/a2215da064eaf2b3b48181bd.svg) | F-component node column vectors and their F-component neighbor mean, dimensionless hidden features. |
| ![Formula](https://ml-biomat.com/static/agent-math/8cf39fd79bbe48a27c6ceb26.svg) | Concatenation producing 2F components; W has shape F′-by-2F and b has F′ components, trainable dimensionless parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/59ac27727155f13a2ca7aad9.svg) | Elementwise activation and updated F′-component vector; this is the core mean-GraphSAGE transform, with optional representation normalization in full variants. |

Self information and neighbor information occupy separate coordinates, allowing different learned effects. With self feature 2 and neighbor features 1 and 5, the neighbor mean is 3. Concatenation gives (2,3). Choosing W=(2,−1), bias zero, and ReLU produces max(0,4−3)=1. Including self in the neighbor mean would define a different aggregation rule; naming the set explicitly prevents that ambiguity.

Sampling changes the amount of neighborhood expansion. With roughly fifty neighbors per node, a two-hop expansion can involve about 2,500 branches. Sampling ten at each level reduces this rough count to a hundred. Repeated nodes can make the actual counts smaller, but the growth pattern explains the computational pressure. Sampling also introduces variation between batches and may omit an important rare relation. Report the sampling sizes and randomization together with evaluation results. Inductive performance comes from a shared computation paired with an evaluation on genuinely unseen objects or graphs; the architecture name alone does not establish the evaluation setting.

Neighbors may also deserve unequal attention. The GAT work by Veličković and colleagues, presented at ICLR 2018, brings attention into local graph neighborhoods. A learned function scores the compatibility of a center node and a neighboring node. Softmax converts the scores into nonnegative weights summing to one within that neighborhood. Consider scores zero and the natural logarithm of three. Exponentiation gives one and three, so the normalized weights are one quarter and three quarters. For scalar messages two and six, the weighted result is five. Attention coefficients vary with features and the receiving node, whereas basic GCN normalization is determined by connectivity and degree.

$$
\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_{k\in\mathcal N_i}\exp(e_{ik})},\qquad h_i'=\sigma\!\left(\sum_{j\in\mathcal N_i}\alpha_{ij}Wh_j\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d151193ddab5d9bfb3903d6d.svg) | Center node, neighbor and summation indices, and the allowed neighborhood, possibly including self; an edge mask defines this set. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff454cbb1c2c014f5d6a966e.svg) | Learned compatibility score and softmax weight, dimensionless; scores depend on transformed features of i and j. |
| ![Formula](https://ml-biomat.com/static/agent-math/eaaae4da4516a6e235e27303.svg) | F-component input, F′-by-F weights, F′-component output, and activation; this is a single head with dimensionless hidden quantities. |

Exponentiation makes scores positive, and division by their sum normalizes the weights. Subtracting the largest local score before exponentiation preserves the result and improves stability. Scores 0 and ln3 yield weights 0.25 and 0.75. Transformed messages 2 and 6 then give 0.25×2+0.75×6=5 before activation. Adding or removing a neighbor changes the denominator, so other weights are renormalized too.

Multiple attention heads can form different weighted combinations and then concatenate or average their outputs. The heads may learn different preferences, or partly redundant ones; their behavior is determined by optimization. A large attention coefficient describes emphasis inside a particular computation. Studying an edge's effect on a final prediction requires additional comparisons, such as removing the edge or replacing its features. GCN provides a compact structural baseline, GraphSAGE supports sampled local computation and new-node processing, and GAT learns local weighting. Compare them with consistent data splits, computational budgets, and task metrics rather than treating their publication dates as a performance ranking.

## 5. Where the label lives determines the experiment

Node classification asks which category an object belongs to, so each labeled training node contributes a classification loss. Link prediction asks whether a relationship should connect two objects. One common approach obtains two node representations and scores their pairing with a dot product or a small network. Representations (1, 0) and (2, 1) have dot product two; applying a sigmoid gives approximately 0.881. Its probabilistic interpretation depends on the training objective, candidate sampling, and calibration. In link prediction, a held-out test edge must also be removed from the message-passing input when the task is to infer that unobserved connection.

$$
z_{ij}=h_i^{\mathsf T}h_j,\qquad p_{ij}=\frac{1}{1+\exp(-z_{ij})}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Indices of the node pair being scored. |
| ![Formula](https://ml-biomat.com/static/agent-math/2a3e18970f6df1c85ae1bb61.svg) | Dimensionless F-component embeddings in the same space; this example uses a symmetric dot-product score. |
| ![Formula](https://ml-biomat.com/static/agent-math/ffd0fc75ca5b5a2073a0cec7.svg) | Pair logit, sigmoid output between zero and one, and transpose notation; all quantities dimensionless. |

The dot product sums coordinatewise products. Inputs (1,0) and (2,1) give z=2 and p≈0.8808. Swapping the pair leaves the score unchanged, making this decoder symmetric. Directed or typed relations require a suitable relation-specific or order-sensitive scoring rule. Negative sampling affects score interpretation, and evaluation should use the intended candidate population.

An absent record is not always a true negative. Two people may have no interaction because they never had an opportunity to meet; a knowledge-base relation may be missing because nobody has recorded it. Negative sampling starts by defining a candidate set, then choosing unobserved pairs under a stated labeling convention. Recommendation additionally needs evaluation in a realistic candidate pool. Finding an appropriate item among a million candidates differs sharply from distinguishing one positive pair from one random negative. In a temporal network, training should use features and events available before the prediction cutoff, with later events reserved for evaluation.

Graph classification assigns a label to an entire graph, such as a connected arrangement of mechanical parts. Node counts vary but the output length must remain fixed, which motivates a readout operation. A sum retains information about system size, a mean emphasizes a typical node representation, and a maximum captures the presence of a strong feature. Scalar node representations two and four have sum six and mean three. Duplicating both nodes leaves the mean at three but doubles the sum to twelve. The target determines which behavior is appropriate. Concatenating nodes in arbitrary numerical order does not provide an order-independent graph representation.

Heterogeneous graphs retain node and relation types. Authors, papers, and venues are different entities; writing and publication are different relationships. Relation-specific transformations can process their messages separately before aggregation at a receiving node. Knowledge graphs express facts as subject–relation–object triples, with direction and relation type entering the score. Dynamic graphs additionally record time and may use temporal windows, recurrent state, or event-time encodings. Each extension preserves information that changes what a message means. Treating all edge types and dates as interchangeable is a modeling decision with direct consequences for the task.

## 6. A complete experiment: recovering communities from noisy observations

The code generates 120 nodes in two communities of sixty. The probability of an edge is 0.18 within a community and 0.015 between communities; the fixed generated graph contains 648 undirected edges. Every node has six standard-normal noise features. The first two receive a class-dependent shift of minus or plus 0.25, leaving the individual feature distributions strongly overlapping. From each class, ten nodes supply training labels, ten supply validation labels, and forty supply test labels. Display coordinates are generated solely for the drawing and never enter the classifier. In particular, the visible left-right arrangement is not a hidden predictive feature supplied to the network.

![Community graph beside a scatterplot of the first two node features.](https://ml-biomat.com/static/tutorials/machine-learning/figures/feab869fa67e6571a3c7c27f.svg?v=feab869fa67e)

Figure 2Two views of the synthetic data. Left: 120 nodes and 648 edges; colors show generated classes and rings identify 20 training labels. Drawing coordinates never enter the model. Right: the first two input features overlap strongly.

GCN and MLP both use bias-free layers with dimensions 6→16→2, ReLU, and dropout probability 0.2. Their trainable parameter counts match. GCN adds graph aggregation before each linear layer, whereas MLP processes each node's own features. Both train for 150 epochs. The checkpoint with the smallest validation cross-entropy is restored before test accuracy is computed. Five initialization seeds repeat this process with the same graph and label split, so their scatter describes variation from training initialization. Estimating variability across new graphs or different labeled subsets requires additional graph-generation and split seeds.

### Complete Python: GCN comparison, propagation plots, and symmetry checks

Uses NumPy, PyTorch, and Matplotlib. Run main.py --output output --language en, or select zh. The fixed graph and split support five runs of equally parameterized GCN and MLP models; validation loss selects checkpoints. The script writes data, summary.json, and three figure groups.

```
"""A transductive graph experiment with reproducible ablations and symmetries."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


def dataset():
    rng = np.random.default_rng(2026)
    labels = np.repeat(np.arange(2), 60)
    p = np.where(labels[:, None] == labels[None, :], .18, .015)
    upper = np.triu(rng.random((120, 120)) < p, 1)
    adjacency = (upper | upper.T).astype(np.float32)
    features = rng.normal(0, 1, (120, 6)).astype(np.float32)
    features[:, :2] += (2 * labels[:, None] - 1) * .25
    train, valid, test = [], [], []
    for c in range(2):
        order = rng.permutation(np.where(labels == c)[0])
        train.extend(order[:10]); valid.extend(order[10:20]); test.extend(order[20:])
    a = adjacency + np.eye(120, dtype=np.float32)
    inv = 1 / np.sqrt(a.sum(1))
    normalized = inv[:, None] * a * inv[None, :]
    return adjacency, normalized, features, labels, train, valid, test


class NodeModel(nn.Module):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.first = nn.Linear(6, 16, bias=False)
        self.last = nn.Linear(16, 2, bias=False)

    def forward(self, x, a):
        hidden = torch.relu(self.first(a @ x if self.graph else x))
        hidden = nn.functional.dropout(hidden, .2, self.training)
        return self.last(a @ hidden if self.graph else hidden)


def fit(kind, seed, a, x, y, train, valid, test):
    torch.manual_seed(seed)
    model = NodeModel(kind == 'GCN')
    optimizer = torch.optim.Adam(model.parameters(), lr=.02, weight_decay=5e-4)
    trace, best_loss, best = [], float('inf'), None
    for epoch in range(150):
        model.train(); optimizer.zero_grad()
        logits = model(x, a)
        loss = nn.functional.cross_entropy(logits[train], y[train])
        loss.backward(); optimizer.step()
        model.eval()
        with torch.no_grad():
            logits = model(x, a)
            val = nn.functional.cross_entropy(logits[valid], y[valid]).item()
            trace.append([loss.item(), val])
            if val < best_loss:
                best_loss, best = val, copy.deepcopy(model.state_dict())
    model.load_state_dict(best); model.eval()
    with torch.no_grad():
        logits = model(x, a)
        accuracy = (logits[test].argmax(1) == y[test]).float().mean().item()
    return model, np.asarray(trace), accuracy, logits.detach().numpy()


def vectors(points):
    difference = points[None, :, :] - points[:, None, :]
    weights = np.exp(-np.square(difference).sum(-1))
    return (weights[:, :, None] * difference).sum(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': 'Microsoft YaHei' if zh else 'Arial',
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none'})
    def label(ch, en): return ch if zh else en
    def save(fig, name):
        fig.savefig(args.output / f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output / f'{name}-{args.language}.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
    adjacency, normalized, features, labels, train, valid, test = dataset()
    a, x, y = torch.tensor(normalized), torch.tensor(features), torch.tensor(labels)
    results, traces, scores, models = {}, {}, {}, {}
    for kind in ['MLP', 'GCN']:
        traces[kind], scores[kind] = [], []
        for seed in range(5):
            model, trace, score, logits = fit(kind, seed, a, x, y, train, valid, test)
            traces[kind].append(trace); scores[kind].append(score)
            if seed == 0: models[kind] = (model, logits)
        results[kind] = {'test_accuracy': scores[kind], 'mean_accuracy': float(np.mean(scores[kind]))}
    permutation = torch.tensor(np.random.default_rng(17).permutation(120))
    with torch.no_grad():
        shifted = models['GCN'][0](x[permutation], a[permutation][:, permutation])
        original = models['GCN'][0](x, a)[permutation]
        permutation_error = float((shifted-original).abs().max())
    points = np.array([[0., 0.], [1., .1], [.2, .8], [1.2, 1.]])
    theta = .7
    rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotation_error = float(np.max(np.abs(vectors(points @ rotation.T) - vectors(points) @ rotation.T)))
    assert permutation_error < 2e-6
    assert rotation_error < 1e-12
    results.update({'nodes': 120, 'edges': int(adjacency.sum()/2), 'split_sizes': [20, 20, 80],
                    'permutation_max_error': permutation_error, 'rotation_max_error': rotation_error})
    (args.output/'summary.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    np.savez(args.output/'data.npz', adjacency=adjacency, features=features, labels=labels,
             train=train, valid=valid, test=test, GCN_trace=np.array(traces['GCN']),
             MLP_trace=np.array(traces['MLP']), GCN_scores=scores['GCN'], MLP_scores=scores['MLP'])

    colors = np.array(['#176b91', '#bb554d'])[labels]
    rng = np.random.default_rng(71)
    xy = rng.normal(0, .32, (120, 2)); xy[:, 0] += (labels*2-1)*.8
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={'width_ratios':[1.25, 1]})
    for i, j in zip(*np.where(np.triu(adjacency, 1))):
        axs[0].plot(xy[[i,j],0], xy[[i,j],1], color='#b4c0c9', lw=.45, alpha=.35, zorder=0)
    axs[0].scatter(*xy.T, c=colors, s=24)
    axs[0].scatter(*xy[train].T, facecolors='none', edgecolors='black', s=85, linewidths=1.2)
    axs[0].set(title=label('关系图：黑圈为20个训练标签', 'Graph: rings mark 20 training labels'), aspect='equal')
    axs[0].axis('off')
    axs[1].scatter(features[:,0], features[:,1], c=colors, s=28, alpha=.7)
    axs[1].set(xlabel=label('节点特征1（无量纲）','Node feature 1 (dimensionless)'),
               ylabel=label('节点特征2（无量纲）','Node feature 2 (dimensionless)'),
               title=label('仅看特征，两个类别重叠','Features alone overlap'))
    fig.tight_layout(); save(fig, 'data')

    fig = plt.figure(figsize=(12, 7)); gs=fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax = fig.add_subplot(gs[:,0])
    for kind, c in [('MLP','#bb554d'), ('GCN','#176b91')]:
        values = np.asarray(traces[kind])[:,:,1]
        ax.plot(np.arange(1,151), np.mean(values,0), color=c, label=kind)
        ax.fill_between(np.arange(1,151), *np.quantile(values,[.25,.75],axis=0), color=c, alpha=.15)
    ax.set(xlabel=label('训练轮数','Epoch'), ylabel=label('验证交叉熵','Validation cross-entropy'),
           title=label('5次初始化：均值与四分位带','5 initializations: mean and interquartile band'))
    ax.legend()
    ax=fig.add_subplot(gs[0,1])
    for k, kind in enumerate(['MLP','GCN']):
        vals=scores[kind];ax.scatter(k+np.linspace(-.12,.12,5),vals,c=['#bb554d','#176b91'][k],s=50)
        ax.hlines(np.mean(vals),k-.25,k+.25,color=['#bb554d','#176b91'][k])
    ax.set(xticks=[0,1],xticklabels=['MLP','GCN'],ylim=(0,1.05),ylabel=label('测试准确率','Test accuracy'))
    ax=fig.add_subplot(gs[1,1]); logits=models['GCN'][1]
    pred=logits.argmax(1); confusion=np.zeros((2,2),int)
    for t in test: confusion[labels[t],pred[t]]+=1
    ax.imshow(confusion,cmap='Blues',vmin=0,vmax=40)
    for i in range(2):
        for j in range(2): ax.text(j,i,str(confusion[i,j]),ha='center',va='center',color='white' if confusion[i,j]>20 else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xlabel=label('预测类别','Predicted class'),
           ylabel=label('真实类别','True class'),title=label('GCN种子0：80个测试节点','GCN seed 0: 80 test nodes'))
    fig.tight_layout();save(fig,'results')

    n=36; ring=np.eye(n)
    for i in range(n): ring[i,(i-1)%n]=ring[i,(i+1)%n]=1
    ring/=3; signal=np.zeros(n); signal[:6]=1
    sequence=[signal.copy()]
    for _ in range(60): sequence.append(ring@sequence[-1])
    sequence=np.array(sequence)
    fig,axs=plt.subplots(1,3,figsize=(13,4),gridspec_kw={'width_ratios':[1.3,1,.9]})
    im=axs[0].imshow(sequence,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    axs[0].set(xlabel=label('环上节点编号','Node on a ring'),ylabel=label('平均传播次数','Averaging steps'),title=label('扩散信息，也磨平差别','Information spreads; contrast fades'))
    fig.colorbar(im,ax=axs[0],label=label('节点信号（无量纲）','Node signal (dimensionless)'))
    axs[1].semilogy(np.var(sequence,axis=1),color='#176b91')
    axs[1].set(xlabel=label('传播次数','Propagation steps'),ylabel=label('节点间方差','Variance across nodes'))
    v=vectors(points); rotated=points@rotation.T; vr=vectors(rotated)
    axs[2].quiver(*points.T,*v.T,color='#176b91',angles='xy',scale_units='xy',scale=1,label=label('原坐标','Original'))
    axs[2].quiver(*rotated.T,*vr.T,color='#bb554d',angles='xy',scale_units='xy',scale=1,label=label('旋转0.7 rad','Rotated 0.7 rad'))
    axs[2].scatter(*points.T,color='#176b91',s=12);axs[2].scatter(*rotated.T,color='#bb554d',s=12)
    axs[2].set(xlim=(-.7,1.6),ylim=(-.2,1.8),aspect='equal',xlabel='x',ylabel='y',title=label('向量随几何旋转','Vectors rotate with geometry'))
    axs[2].legend(fontsize=8)
    fig.tight_layout();save(fig,'structure')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
```

The actual GCN test accuracies are 0.9875, 0.9750, 0.9750, 0.9750, and 0.9750, with mean 0.9775. The MLP mean is 0.4950. This contrast matches the data-generating mechanism: dense within-community connectivity provides information beyond noisy measurements at one node. Validation-loss curves show the checkpoint-selection behavior, individual dots preserve all five results, and the confusion matrix shows how the eighty test nodes are classified for seed zero. These scores describe this synthetic graph with strong homophily. Raising the cross-community connection probability, or making different-class nodes preferentially adjacent, changes the information gathered by the same propagation rule.

![Validation-loss traces, test-accuracy dots, and a test confusion matrix.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9190834f9ce8c3eafae5da33.svg?v=9190834f9ce8)

Figure 3Executed results. Left: mean validation cross-entropy and interquartile band over five initializations. Upper right: test accuracy at each run's validation-selected checkpoint, with mean lines. Lower right: seed-zero GCN confusion matrix on 80 test nodes. Graph and label split are fixed.

The script also performs two structural checks. It permutes node numbers, applying the same permutation to feature rows and to both axes of the adjacency matrix, then compares correspondingly reordered predictions. The maximum absolute difference is approximately 9.54×10⁻⁷, at floating-point precision for these operations. A separate distance-weighted vector-message operator is evaluated before and after a spatial rotation; its equivariance error is about 2.22×10⁻¹⁶. The first test checks node permutation behavior of the trained GCN. The second checks the independently constructed geometric operator. Neither substitutes for predictive accuracy: structural consistency and task performance answer different questions.

## 7. Change the indexing or coordinate system, preserve the object

Renumbering nodes resembles replacing the index labels on a bookshelf. Node predictions should follow the same reordering, a property called permutation equivariance. A whole-graph scalar should remain unchanged, which is permutation invariance. Sum and mean ignore the order in which neighbor messages arrive, while shared transformations do not depend on node names. Together, these choices support the desired structural behavior. Randomly renumbering a graph is a useful implementation test; designing the computation to have the property provides a stronger foundation. Feeding arbitrary node indices into the model as continuous measurements can reintroduce an irrelevant ordering.

$$
f(PX,PAP^{\mathsf T})=P f(X,A)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/08b9af13817a89a808fad482.svg) | N-by-F feature matrix and N-by-N adjacency matrix. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d12beb7c65071b9de7ea3da.svg) | N-by-N permutation matrix and transpose, with exactly one one per row and column; dimensionless reindexing operators. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Graph model returning N-by-C node scores, where C is the class count and scores are dimensionless. |

Reordering feature rows and both adjacency axes changes indexing alone. Recomputing on the left should match reordering the original output on the right. Outputs (2,5,7) become (5,2,7) after swapping the first two nodes. A sum readout yields 14 under either numbering, giving graph-level invariance. Floating-point summation order may produce a small numerical discrepancy.

Spatial geometry introduces another family of transformations. Rotating a molecule or mechanical structure should preserve scalar properties such as mass, while vector properties such as force should rotate with it. An ordinary GCN processes general features. Supplying x, y, and z coordinates does not automatically make it rotationally equivariant. A simple construction uses distance to determine message strength and displacement to determine message direction. Rotation preserves the distance and rotates the displacement, so their weighted sum rotates correctly. The next equation makes this argument executable. Positions are first expressed relative to a shared reference length, making the exponential's argument dimensionless.

$$
v_i=\sum_j\exp\!\left(-\|r_j-r_i\|^2\right)(r_j-r_i),\qquad v_i(Rr)=R\,v_i(r)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f69e9a731c172316bf6e0e05.svg) | Node indices and position vectors normalized by a reference length, hence dimensionless; the code uses 2D, with the same construction valid in 3D. |
| ![Formula](https://ml-biomat.com/static/agent-math/247c126e566140ca1dceb95f.svg) | Euclidean distance and aggregated vector, both in normalized coordinate units; the self term is zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/2d823743d6fb81798bf85e6a.svg) | Rotation matrix with RᵀR=I and determinant one, the full collection of positions, and its rotation; vᵢ(Rr) means recomputing from rotated positions. |

Rotation preserves distance, leaving each exponential weight unchanged. Displacements become R(rj−ri), and the common matrix can be taken outside the sum. For points (0,0) and (1,0), the first message is (e⁻¹,0)≈(0.3679,0). After a 90-degree counterclockwise rotation it becomes (0,0.3679). The script tests this explicitly designed vector operator separately from the trained classifier.

Geiger and Smidt's 2022 e3nn work places scalars, vectors, and more general geometric tensors within a framework of learnable equivariant operations. Three-dimensional models can combine spherical harmonics, tensor products, and distance-dependent networks while maintaining prescribed transformation rules. Our small vector operator isolates the part that is easiest to calculate by hand: what should happen when a coordinate system rotates. Tasks that distinguish mirror structures require explicit attention to reflection behavior as well as rotations. Distance-threshold graph construction should use consistent thresholds and numerical tolerances across transformed inputs, since a changed edge set can disturb the expected symmetry.

## 8. Let information travel without erasing useful distinctions

Imagine a circular water channel containing dye in one short segment. At each step, a location mixes its contents with those of its immediate neighbors. The signal spreads, while local contrast decreases. Our heatmap performs the corresponding calculation on thirty-six ring nodes with pure averaging. Horizontal position identifies the node, vertical position counts propagation steps, and color shows signal strength. A neighboring variance curve quantifies how differences between nodes shrink. This illustrates one mechanism behind oversmoothing. Trained networks also contain learned transformations, nonlinearities, residual paths, and normalization, so layer-by-layer measurements of an actual model complement this isolated propagation experiment.

![Node-by-step propagation heatmap, variance curve, and vectors before and after rotation.](https://ml-biomat.com/static/tutorials/machine-learning/figures/edf2c52e93d952617eddfe68.svg?v=edf2c52e93d9)

Figure 4Left and center: pure averaging on a 36-node ring, initially one on six nodes and zero elsewhere; signal spreads and across-node variance decreases. Right: a separate distance-weighted vector operator rotates with its geometry by 0.7 rad. These structural calculations are distinct from classification metrics.

Expressive power raises a different question. Suppose all initial node features are identical and every node has two neighbors. At each layer, a basic local message-passing network receives the same multiset of neighbor representations at every node. A six-node cycle and two disconnected three-node cycles can therefore produce identical node representations. With six nodes in each graph, sum or mean readouts may also coincide. The example identifies information that this local computation cannot distinguish. Structural positional features, higher-order relationships, and task-relevant subgraph features add information unavailable to the original aggregation rule.

Oversquashing concerns many distant messages being compressed through a small number of connections into fixed-width vectors. More layers expand reach while potentially increasing pressure on those channels. Rewiring, residual paths, global attention, and hierarchical readout modify different bottlenecks, with corresponding computational and modeling costs. A practical investigation starts by defining relations and the prediction time, builds an MLP and a shallow GCN, examines the split and the errors, and then changes the model in response to a specific failure pattern. Each added mechanism should have a clear reason to exist.

You can extend the example into a small controlled study by varying only the between-community edge probability while preserving features, label allocation, and optimization settings. Generate several graphs at each value, recording mean degree, the fraction of same-class edges, and test accuracy alongside the GCN–MLP difference. Random edge deletion and selective removal of cross-community edges provide another useful comparison. They separate the amount of connectivity from the information carried by particular connections. Such an experiment explains when a relational representation helps, rather than turning architecture names into a universal ranking.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M22.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [A Gentle Introduction to Graph Neural Networks](https://distill.pub/2021/gnn-intro/)

   Relational representations, message-passing visualization, and the original figure used here.

   Original diagrams and text CC BY 4.0; selected original GCN image unmodified.
2. [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)

   GCN propagation, semi-supervised node classification, and spectral motivation.
3. [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216)

   GraphSAGE aggregation and neighborhood sampling.
4. [Graph Attention Networks](https://arxiv.org/abs/1710.10903)

   Feature-dependent attention within graph neighborhoods.
5. [e3nn: Euclidean Neural Networks](https://arxiv.org/abs/2207.09453)

   Geometric tensors and Euclidean equivariant networks.
