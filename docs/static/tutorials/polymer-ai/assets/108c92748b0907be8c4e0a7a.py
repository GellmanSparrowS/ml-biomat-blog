"""组成、顺序与连接：两个受控的表示学习实验。

运行：python example.py；依赖：numpy、matplotlib。
标签来自下文明确的结构规则，数据由程序生成。
输出含完整样本、划分、模型参数、数值及六幅结果图。
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SEED = 20261022
rng = np.random.default_rng(SEED)
OUT = Path('representation_outputs')
OUT.mkdir(exist_ok=True)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'DejaVu Sans'],
    'font.size': 14, 'axes.titlesize': 13, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.edgecolor': '#a7b9b2',
    'axes.labelcolor': '#24423c', 'text.color': '#24423c',
    'xtick.color': '#536c63', 'ytick.color': '#536c63',
    'figure.facecolor': '#fcfaf5', 'axes.facecolor': '#fcfaf5',
    'svg.fonttype': 'path', 'svg.hashsalt': str(SEED),
})
GREEN, GOLD = '#14786b', '#bc7041'


def switch_fraction(sequence):
    a = np.asarray(sequence)
    return float(np.mean(a[1:] != a[:-1]))


def draw_sequence(n, label, used):
    # 两类都有一半 A、一半 B。只选择变化少/变化多的序列。
    while True:
        a = rng.permutation(np.repeat([0, 1], n // 2))
        c = switch_fraction(a)
        key = tuple(a.tolist())
        if key not in used and (c <= .4 if label == 0 else c >= .6):
            used.add(key)
            return a


def make_graph(n, branched):
    edges = [(i, i + 1) for i in range(n - 1)]
    if branched:
        # 把末端的一个点改接到内部：仍是连通树，出现三叉点。
        edges.pop()
        edges.append((int(rng.integers(1, n - 3)), n - 1))
    # 随机重编号，避免让编号成为提示标签的捷径。
    perm = rng.permutation(n)
    a = np.zeros((n, n), dtype=int)
    for i, j in edges:
        a[perm[i], perm[j]] = a[perm[j], perm[i]] = 1
    return a


def features(a):
    degree = a.sum(axis=1)
    return [len(a), int(a.sum() // 2), float(np.mean(degree >= 3)),
            float(np.mean(degree == 1))]


def sigmoid(z):
    # z 经标准化训练后在有限范围，截断兼顾数值安全。
    return 1 / (1 + np.exp(-np.clip(z, -40, 40)))


def fit_predict(x, y, train, test):
    x = np.asarray(x, dtype=float)
    # 标准化只从训练侧估计；常数列取尺度 1，避免除以零。
    mean, scale = x[train].mean(axis=0), x[train].std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    z = np.column_stack([np.ones(len(x)), (x - mean) / scale])
    weight = np.zeros(z.shape[1])
    history = []
    for _ in range(800):
        p = sigmoid(z[train] @ weight)
        history.append(float(np.mean(np.logaddexp(0, z[train] @ weight)
                                     - y[train] * (z[train] @ weight))))
        gradient = z[train].T @ (p - y[train]) / train.sum()
        weight -= .15 * gradient
    probability = sigmoid(z[test] @ weight)
    prediction = (probability >= .5).astype(int)
    return {'accuracy': float(np.mean(prediction == y[test])),
            'probabilities': probability.tolist(), 'loss': history,
            'mean': mean.tolist(), 'scale': scale.tolist(),
            'weight_with_bias': weight.tolist()}


def main():
    sequences, graphs, groups, labels, used = [], [], [], [], set()
    for group in range(320):
        n = int(rng.integers(8, 21)) * 2
        for label in (0, 1):
            sequences.append(draw_sequence(n, label, used))
            graphs.append(make_graph(n, bool(label)))
            groups.append(group)
            labels.append(label)
    groups, y = np.asarray(groups), np.asarray(labels)
    test_groups = rng.choice(320, 80, replace=False)
    test = np.isin(groups, test_groups)
    train = ~test
    count = np.array([[len(a), np.mean(a == 0)] for a in sequences])
    order = np.column_stack([count, [switch_fraction(a) for a in sequences]])
    graph = np.array([features(a) for a in graphs])
    x = {'sequence_count': count, 'sequence_order': order,
         'graph_count': graph[:, :2], 'graph_degree': graph}
    scores = {name: fit_predict(value, y, train, test) for name, value in x.items()}
    # 结构规则也作直接计算参照；它与学习模型回答的是同一标签问题。
    rule_sequence = (order[test, -1] >= .5).astype(int)
    rule_graph = (graph[test, 2] > 0).astype(int)
    permutation_error = 0.0
    for a in graphs:
        perm = rng.permutation(len(a))
        permutation_error = max(permutation_error, float(np.max(np.abs(
            np.asarray(features(a)) - features(a[perm][:, perm])))))
    checks = {
        'train_test_group_overlap': len(set(groups[train]) & set(groups[test])),
        'unique_sequences': len(used) == len(sequences),
        'each_pair_same_counts': bool(np.all(count[::2] == count[1::2])),
        'each_pair_same_node_edge_counts': bool(np.all(graph[::2, :2] == graph[1::2, :2])),
        'relabel_feature_max_error': permutation_error,
        'sequence_rule_accuracy': float(np.mean(rule_sequence == y[test])),
        'graph_rule_accuracy': float(np.mean(rule_graph == y[test])),
    }
    assert checks['train_test_group_overlap'] == 0
    assert checks['unique_sequences'] and checks['each_pair_same_counts']
    assert checks['each_pair_same_node_edge_counts'] and permutation_error == 0
    assert scores['sequence_count']['accuracy'] == .5
    assert scores['graph_count']['accuracy'] == .5
    result = {'seed': SEED, 'source': 'program_generated_structural_examples',
              'n_groups': 320, 'n_train': int(train.sum()), 'n_test': int(test.sum()),
              'scores': scores, 'checks': checks}
    samples = []
    for i, (seq, a) in enumerate(zip(sequences, graphs)):
        samples.append({'group': int(groups[i]), 'split': 'test' if test[i] else 'train',
                        'label': int(y[i]), 'sequence': ''.join('AB'[v] for v in seq),
                        'edges': np.argwhere(np.triu(a, 1)).tolist(),
                        'sequence_features': order[i].tolist(),
                        'graph_features': graph[i].tolist()})
    (OUT / 'samples.json').write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    def panel_count(ax):
        # 同一组成上两类点重叠：环表示标签 0，实点表示标签 1。
        ax.scatter(count[test & (y == 0), 0], count[test & (y == 0), 1],
                   s=90, facecolors='none', edgecolors=GREEN, label='相邻变化少')
        ax.scatter(count[test & (y == 1), 0], count[test & (y == 1), 1],
                   s=13, c=GOLD, label='相邻变化多')
        ax.set(xlabel='单元数 N', ylabel='A 的比例', ylim=(.42, .58),
               title='A  组成相同，两类点完全重合')
        ax.legend(frameon=False, loc='upper left', fontsize=11)

    def panel_order(ax):
        for label, color, name in [(0, GREEN, '变化少'), (1, GOLD, '变化多')]:
            mask = test & (y == label)
            ax.scatter(order[mask, 0], order[mask, 2], c=color, s=19, alpha=.6, label=name)
        ax.axhspan(.4, .6, color='#dde5df', alpha=.7)
        ax.text(28, .5, '未采样的中间区间', ha='center', fontsize=11)
        ax.set(xlabel='单元数 N', ylabel='相邻变化比例 c', ylim=(0, 1),
               title='B  保留邻居关系后，两类可以分开')

    def panel_loss(ax):
        for key, color, name in [('sequence_count', '#8d9e97', '组成特征'),
                                  ('sequence_order', GREEN, '顺序特征'),
                                  ('graph_degree', GOLD, '连接特征')]:
            ax.plot(scores[key]['loss'], color=color, lw=2,
                    ls='--' if key == 'graph_degree' else '-', label=name)
        ax.set(xlabel='参数更新次数', ylabel='训练集平均交叉熵',
               title='C  相同训练方法，输入信息不同')
        ax.legend(frameon=False, fontsize=11)

    def panel_accuracy(ax):
        names = list(scores)
        values = [100 * scores[k]['accuracy'] for k in names]
        bars = ax.barh(np.arange(4), values, color=['#a6b8ae', GREEN, '#a6b8ae', GOLD], height=.6)
        ax.set_yticks(range(4), ['序列：组成', '序列：组成＋顺序', '图：点数＋边数', '图：加入节点度数'])
        ax.set(xlim=(0, 117), xlabel='独立留出 80 组的准确率 / %',
               title='D  两个任务中的表示对照')
        ax.invert_yaxis()
        for b, value in zip(bars, values):
            ax.text(value + 2, b.get_y() + b.get_height() / 2, f'{value:.1f}', va='center')

    def panel_degree(ax):
        for label, color, shift, name in [(0, GREEN, -.16, '线性树'), (1, GOLD, .16, '分支树')]:
            hist = np.mean([np.bincount(a.sum(axis=1), minlength=4)[1:4] / len(a)
                            for a, v, keep in zip(graphs, y, test) if v == label and keep], axis=0)
            ax.bar(np.arange(1, 4) + shift, hist, width=.3, color=color, label=name)
        ax.set(xticks=[1, 2, 3], xlabel='每个节点直接连接的邻居数', ylabel='测试图内比例的平均值',
               title='E  分支改变了局部连接分布')
        ax.legend(frameon=False, fontsize=11)

    def panel_probability(ax):
        p = np.array(scores['sequence_order']['probabilities'])
        for label, color, name in [(0, GREEN, '变化少'), (1, GOLD, '变化多')]:
            ax.hist(p[y[test] == label], bins=np.linspace(0, 1, 21), alpha=.8, color=color, label=name)
        ax.axvline(.5, ls='--', color='#73867c', lw=1)
        ax.set(xlabel='模型给“变化多”的概率', ylabel='测试序列数',
               title='F  概率是输出，阈值才给类别')
        ax.legend(frameon=False, fontsize=11, loc='upper center')

    panels = [('counts', panel_count), ('order', panel_order), ('loss', panel_loss),
              ('accuracy', panel_accuracy), ('degree', panel_degree), ('probability', panel_probability)]
    for name, draw in panels:
        fig, ax = plt.subplots(figsize=(6.6, 4.6), layout='constrained')
        draw(ax)
        fig.savefig(OUT / f'{name}.svg', metadata={'Date': None})
        plt.close(fig)
    fig, axes = plt.subplots(3, 2, figsize=(14, 13), layout='constrained')
    for (_, draw), ax in zip(panels, axes.ravel()):
        draw(ax)
    fig.savefig(OUT / 'representation_diagnostics.svg', metadata={'Date': None})
    fig.savefig(OUT / 'representation_diagnostics.png', dpi=180)
    plt.close(fig)
    for name, score in scores.items():
        print(f'{name}: 测试准确率 {100 * score["accuracy"]:.1f}%')
    print(f'训练/测试样本：{train.sum()}/{test.sum()}；共有组数：{checks["train_test_group_overlap"]}')
    print(f'节点重新编号后，特征最大变化：{permutation_error:.1f}')
    print('结果与完整样本已保存至 representation_outputs')


if __name__ == '__main__':
    main()
