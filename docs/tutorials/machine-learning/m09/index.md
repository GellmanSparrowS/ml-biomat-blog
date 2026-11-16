# MLP与反向传播：看清网络怎样学习

Source: https://ml-biomat.com/tutorials/machine-learning/m09/
Language: zh-CN

从一条可以手算的计算链，走到真正训练、评价和保存的神经网络。

## 一条直线分不开的时候

假设地图上记录了两群人的活动位置：一群沿湖岸散步，另一群沿弯曲的步道跑步。仅凭横、纵坐标判断一个新位置属于哪一群，一条直线往往不够，因为两条路线可能像两个月牙互相环抱。这个小问题说明了神经网络的一项实际用途：当输入与目标之间存在弯曲、组合或分段的关系时，用一组可以学习的变换把关系表达出来。识别照片中的物体、根据多个传感器读数判断设备状态，都包含类似的困难；输入更多了，所需的组合也更复杂了。

本章用人工生成的双月牙数据把这种困难缩到一张图上。每个样本只有两个无量纲坐标和一个二元标签，因此可以同时看见数据、预测概率与分类边界。我们先让线性分类器完成任务，再训练一个有两层隐藏层的多层感知机，简称 MLP。图中的弯曲边界来自代码实际训练的结果。读完后，你应能解释一个参数如何影响最终误差，亲手核对一次梯度，并把训练、验证、测试和保存模型串成可以重复执行的工作流程。

把学习想成调节一组旋钮很有帮助：每个旋钮控制一种输入影响输出的方式，但旋钮之间相互连接，转动一个，后面的变化会逐级传下去。真正要解决的问题是怎样知道转哪一个、转多少。神经网络的前向计算回答“现在会预测什么”，损失函数把预测差异变成一个数，反向传播计算每个旋钮对这个数的局部影响。三者接起来，训练就从含混的“让模型变聪明”变成一系列可以检查的数值操作。

## 神经元怎样组成可学习的变换

一个人工神经元首先把输入按不同权重相加，再加一个偏置。权重决定某项输入的影响方向和强度，偏置调整整体起点。随后，激活函数改变这个和的形状。若去掉所有非线性激活，多层矩阵乘法仍可以合并成一次矩阵乘法；虽然参数写了很多层，表达出的边界依然是线性的。插入非线性以后，不同神经元可以响应不同区域，再由下一层重新组合，弯曲的关系便有了表达空间。

$$
\mathbf{h}=\phi(\mathbf{W}\mathbf{x}+\mathbf{b})
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4fa2300af121b336bb0d7845.svg) | 输入列向量，形状d×1；本例为标准化坐标，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e376aab419a2e38d8eb39d69.svg) | 权重矩阵，形状m×d；每行对应一个输出神经元，本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/639196a1a30d6f6280e3cf49.svg) | 偏置列向量，形状m×1；本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | 逐元素激活函数，例如tanh或ReLU。 |
| ![Formula](https://ml-biomat.com/static/agent-math/412791ff09271eea93125852.svg) | 激活后的输出向量，形状m×1，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/79008c488d4b7c757e91cbd3.svg) | d为输入特征数，m为输出神经元数，均为无量纲整数。 |

矩阵乘法把同一输入送给m组权重，每组计算一次加权和，再逐项加偏置与激活。取d=2、m=1，x=(2,−1)，W=(0.5,0.2)，b=0.1，激活前结果为0.9；ReLU输出0.9，tanh输出约0.7163。

例如两个输入是 2 和 −1，权重是 0.5 和 0.2，偏置是 0.1，加权结果就是 0.5×2＋0.2×(−1)＋0.1＝0.9。若采用 ReLU，正数原样通过，输出仍是 0.9；若结果为 −0.9，ReLU 输出为零。tanh 则把任意实数压到 −1 到 1 之间，在零附近平滑变化，在两端逐渐变平。ReLU 的分段响应与 tanh 的平滑压缩对应不同的计算行为。本章选 tanh，让后面的手算和有限差分更容易看清。

“隐藏层”中的隐藏，只表示这些量没有直接作为数据标签给出，并不表示它们无法观察。输入层接收两个坐标，第一层产生 16 个中间数，第二层再产生 16 个中间数，输出层给出一个分类分数。第一层有 2×16＋16＝48 个参数，第二层有 16×16＋16＝272 个，输出层有 16＋1＝17 个，共 337 个。这个数来自连接与偏置的逐项计数；它也提醒我们，网络增加宽度时，计算和存储代价会怎样增长。

神经元的名字借用了生物学语言，但这里的对象是一条明确的计算规则。理解本章不需要先掌握神经生理学。真正需要分清的是数据、参数和中间结果：坐标来自样本，权重和偏置由训练更新，中间激活随着样本而变化。三个对象在代码中都可能表现为张量，却承担不同角色。把它们画成计算图，比把整层看成一个神秘的黑盒更便于定位错误。

## 沿着一条短计算链走一遍

在训练整个网络之前，先只保留一个输入、一个权重和一次非线性。输入设为 2，目标设为 1，权重从 0.3 开始，偏置固定为 −0.1。加权和是 0.5，经过 tanh 得到约 0.4621，与目标相差约 −0.5379。为了让这条手算链足够短，暂用平方误差的一半作为损失，结果约为 0.1447。前面的“一半”会在求导时抵消平方产生的系数 2，不改变哪个预测使损失最小。

$$
z=wx+b,\qquad h=\tanh z,\qquad L=\frac12(h-y)^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | x为输入，y为目标；本例x=2、y=1，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/8d6a07eeeed288d729c0d812.svg) | 权重w=0.3、固定偏置b=−0.1，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/0df8baa5e5b619840f653237.svg) | 加权和z和激活h，均为无量纲标量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 单个样本的半平方损失，无量纲，非负。 |

按箭头顺序代入：z=0.3×2−0.1=0.5，h≈0.462117，L≈0.144659。平方使正负误差都产生非负代价；这里的一半便于后面求导。

![单样本的计算图。蓝色箭头沿输入到损失方向传值，橙色箭头表示反向传播顺序；数值来自本章明确指定的标量例子。](https://ml-biomat.com/static/tutorials/machine-learning/figures/f165d89316c7bf02db9086cc.svg?v=f165d89316c7)

图 1单样本的计算图。蓝色箭头沿输入到损失方向传值，橙色箭头表示反向传播顺序；数值来自本章明确指定的标量例子。

读这张图时，可以把每个方框理解成一张小工作单：只知道自己的输入，执行一种运算，再把结果交给后面。加权求和不需要知道最终目标是什么，tanh 也不需要知道损失有多大。最后一个节点才把预测与目标进行比较。计算图记录这种依赖关系，因此一个中间数被多个分支使用时，框架能够知道哪些路径都受它影响。残差连接、共享参数和循环网络会让图更复杂，但这套依赖关系仍然适用。

这与早期多层网络遇到的困难相连：给出一个最终错误以后，如何判断内部每个连接应承担多少调整？Rumelhart、Hinton 与 Williams 在 1986 年的工作展示了用误差反向传播学习内部表示的效果，使多层网络训练的这条路线受到广泛关注。它的重要之处并不是要求每个节点理解任务，而是把整体误差拆成沿计算关系传递的局部变化率。图里的短链正是这个问题的一个可以手算的版本。

## 反向传播是在传递变化率

导数可以先理解成“附近的放大倍数”。若输入稍微增加，下一步的输出增加多少？短链中，权重增加一点，会先改变加权和，再改变 tanh 输出，最后改变损失。这三个局部变化率相乘，就得到损失对权重的变化率。因为输入为 2，权重的一点变化会被加权和放大为两倍；因为 tanh 在 0.5 附近的斜率约为 0.7864，这个变化又被缩小；最后，当前预测低于目标，使损失对预测的导数为负。

$$
\frac{\partial L}{\partial w}=(h-y)(1-h^2)x,\qquad w_{\mathrm{new}}=w-\eta\frac{\partial L}{\partial w}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/74cc380f215a14d626b16938.svg) | 损失对权重的局部变化率；本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/896a3446dd4c698f708be84d.svg) | h为tanh输出，y为目标，x为输入，定义同前式。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e8027609d6efc5e71c2c8166.svg) | 更新前与更新后的标量权重，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | 正学习率，本例取0.1；对本例的无量纲参数也无量纲。 |

三项分别来自损失、tanh和加权和的导数：−0.537883×0.786448×2≈−0.846033。于是一次更新为0.3−0.1×(−0.846033)≈0.384603。各项相乘是链式法则，减去梯度让小步朝损失下降的方向移动。

乘积约为 −0.8460。负号意味着在当前位置把权重增大一点，损失会减小。若学习率取 0.1，一次更新把权重从 0.3 改为约 0.3846。学习率控制我们愿意沿局部方向走多远；它不是模型自动得出的真实距离。导数只描述当前位置附近的变化，步子过大可能跨过低谷，甚至让损失升高。因此，方向正确与步长合适是两件需要分别检查的事。

在一张有分支的计算图里，共享变量可能通过多条路径影响损失。这时要把各条路径的贡献相加，再继续向前传递，而不是任意选择其中一条。反向传播按依赖关系的逆序完成这些乘法与加法，复用已经得到的中间结果。对于一个标量损失和大量参数，这种反向模式很有效率：计算所有参数的梯度通常只需与前向计算同数量级的工作，而逐参数尝试微小扰动则要重复运行许多次。

PyTorch 的自动微分系统负责记录张量运算并应用这些局部求导规则。它执行的是运算级的链式法则，不是用一小步一小步扰动参数来猜导数。只有需要计算梯度的叶张量才要启用 `requires_grad`；神经网络模块中的可训练参数已经按这个角色组织好。调用 `backward()` 后，参数的 `.grad` 保存本轮梯度，优化器再根据梯度更新参数。自动化减少了机械劳动，手算和数值核对仍然让结果保持可理解。

## 把样本、张量和损失对齐

张量是带形状的数值数组。一个双坐标样本可以写成长度为 2 的向量；把 64 个样本排在一起，输入张量的形状就是 64×2。网络的最后一层对每个样本输出一个分数，所以输出形状是 64×1。标签也整理成 64×1，能避免某些逐元素运算因广播而悄悄变成 64×64。写代码时把样本轴、特征轴和输出轴说清楚，常常比先增加网络层数更能解决问题。

分类分数经过 sigmoid 可以转换为 0 到 1 之间的预测概率。训练双月牙分类器时，采用二元交叉熵而不是前面手算用的平方误差：对真实类别分配较高概率，损失较小；很自信地给错类别，损失会显著增大。它同时利用了标签是否正确和模型有多确信的信息。实现中直接把未经过 sigmoid 的分数交给 `BCEWithLogitsLoss`，由该函数以数值更稳定的方式合并 sigmoid 和对数运算。

$$
p_i=\sigma(s_i),\qquad \mathcal{L}=-\frac1B\sum_{i=1}^{B}\big[y_i\log p_i+(1-y_i)\log(1-p_i)\big]
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39a5e1fd0c0f25384d2357d0.svg) | i为批内样本索引，B为该批样本数，均为无量纲整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | 网络对第i个样本给出的未归一化分数logit，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | sigmoid函数，将分数映射到0到1之间。 |
| ![Formula](https://ml-biomat.com/static/agent-math/043e1e9a3c94510bfcdeec48.svg) | p_i为类别1的预测概率，y_i为0或1标签，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/656d8346ef3238a285037c0c.svg) | log取自然对数；平均交叉熵L以nats计，无物理量纲。 |

当标签为1，单样本损失只保留−log(p)。预测概率0.8对应约0.2231，而0.2对应约1.6094；错误且自信的预测代价更高。对B个样本求平均，使损失尺度便于在不同批次间比较。

`TensorDataset` 把输入和标签按同一索引配对，`DataLoader` 将样本分批送入模型，并在每轮训练重新排列顺序。这里使用 64 个样本组成一个小批量；600 个训练样本不能整除 64，因此最后一批稍小。训练代码每次依次执行清梯度、前向计算、反向传播和更新。PyTorch 默认把新梯度累加到已有梯度上，清梯度这一步由 `zero_grad` 明确完成；有意跨批累积时则需要同时处理损失缩放和更新频率。

另两个容易混淆的开关是 `model.eval()` 与 `torch.no_grad()`。前者改变 Dropout、BatchNorm 等层的运行方式，后者停止为后续运算记录梯度。本章的 tanh 网络没有这两种层，仍然把训练和评价模式写完整，使代码在换成更复杂的模型后保持正确。标签、预测和输入还必须位于兼容的设备上；本实验全部在 CPU 运行，先把计算逻辑看清，再讨论并行与加速。

## 实际训练：看边界，也看未见样本

下面的完整程序生成 1000 个双月牙样本，噪声强度设为 0.23，并固定随机种子。先留出 200 个测试样本，再把其余数据分为 600 个训练样本和 200 个验证样本。标准化的均值与尺度只从训练集计算；验证集和测试集使用同一组变换参数。这样，“模型在新样本上表现怎样”这个问题才不会被预处理阶段提前看见测试分布的细节所混淆。

程序运行 180 轮，每轮记录训练和验证交叉熵，保留验证损失最低时的参数。这个选择过程不使用测试标签；最后才在测试集计算一次主要指标。作为对照，逻辑回归使用同样的训练样本与标准化坐标。两种模型共享数据划分，因此可以把差异联系到表达方式和训练设置。运行命令可写为 `python main.py --output results --language zh`；将语言改为 `en` 会输出英文图，模型与数据保持一致。

### 完整实验：从数据划分到模型重载

依赖NumPy、Matplotlib、scikit-learn、PyTorch。固定种子生成合成数据，训练337参数MLP；结果目录包含三幅图、权重、数据和数值摘要。

```
"""Train a small MLP, check one derivative, and reproduce the chapter figures.

Dependencies: numpy, matplotlib, scikit-learn, torch.
Run: python main.py --output results --language en
The two-moons data are synthetic and generated by the declared seed.
"""
from pathlib import Path
import argparse, copy, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss, confusion_matrix


def experiment(output, language):
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(2)
    torch.manual_seed(19)
    np.random.seed(19)
    torch.use_deterministic_algorithms(True)
    zh = language == 'zh'
    label = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'DejaVu Sans'],
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'savefig.bbox': 'tight'})
    blue, amber, teal = '#0072B2', '#D58500', '#008675'

    # Hold out test data before fitting preprocessing or choosing an epoch.
    X, y = make_moons(n_samples=1000, noise=0.23, random_state=19)
    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=20)
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_dev, y_dev, test_size=0.25, stratify=y_dev, random_state=21)
    scaler = StandardScaler().fit(X_train)
    train = torch.tensor(scaler.transform(X_train), dtype=torch.float32)
    valid = torch.tensor(scaler.transform(X_valid), dtype=torch.float32)
    test = torch.tensor(scaler.transform(X_test), dtype=torch.float32)
    targets = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)
    valid_targets = torch.tensor(y_valid, dtype=torch.float32).reshape(-1, 1)
    loader = DataLoader(TensorDataset(train, targets), batch_size=64,
                        shuffle=True, generator=torch.Generator().manual_seed(22))
    model = nn.Sequential(nn.Linear(2, 16), nn.Tanh(), nn.Linear(16, 16),
                          nn.Tanh(), nn.Linear(16, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCEWithLogitsLoss()
    history, best_loss, best_state, best_epoch = [], float('inf'), None, 0
    for epoch in range(1, 181):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            train_loss = criterion(model(train), targets).item()
            valid_loss = criterion(model(valid), valid_targets).item()
        history.append([epoch, train_loss, valid_loss])
        if valid_loss < best_loss:
            best_loss, best_epoch = valid_loss, epoch
            best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        probability = torch.sigmoid(model(test)).numpy().ravel()
    baseline = LogisticRegression().fit(train.numpy(), y_train)
    baseline_probability = baseline.predict_proba(test.numpy())[:, 1]

    # Save the weights together with the preprocessing needed at inference.
    checkpoint = {'state_dict': model.state_dict(), 'mean': scaler.mean_.tolist(),
                  'scale': scaler.scale_.tolist(), 'best_epoch': best_epoch}
    torch.save(checkpoint, output / 'mlp.pt')
    restored = nn.Sequential(nn.Linear(2, 16), nn.Tanh(), nn.Linear(16, 16),
                             nn.Tanh(), nn.Linear(16, 1))
    loaded = torch.load(output / 'mlp.pt', weights_only=True)
    restored.load_state_dict(loaded['state_dict'])
    # Reconstruct preprocessing from the saved artifact and the raw test inputs.
    restored_test = torch.tensor((X_test - np.asarray(loaded['mean'])) /
                                 np.asarray(loaded['scale']), dtype=torch.float32)
    restored.eval()
    with torch.no_grad():
        reload_error = torch.max(torch.abs(restored(restored_test) - model(test))).item()

    # An independent scalar calculation makes autograd inspectable.
    x, target, b, w0 = 2.0, 1.0, -0.1, 0.3
    w = torch.tensor(w0, dtype=torch.float64, requires_grad=True)
    h = torch.tanh(w * x + b)
    scalar_loss = 0.5 * (h - target) ** 2
    scalar_loss.backward()
    autograd = w.grad.item()
    h0 = float(np.tanh(w0 * x + b))
    analytic = (h0 - target) * (1 - h0 ** 2) * x
    def objective(value):
        return 0.5 * (np.tanh(value * x + b) - target) ** 2
    epsilons = np.logspace(-1, -10, 10)
    numeric = np.array([(objective(w0 + e) - objective(w0 - e)) / (2 * e)
                        for e in epsilons])
    assert abs(autograd - analytic) < 1e-12
    assert abs(numeric[3] - analytic) < 1e-6
    assert reload_error == 0.0

    history = np.asarray(history)
    xmin, xmax = X[:, 0].min() - .2, X[:, 0].max() + .2
    ymin, ymax = X[:, 1].min() - .2, X[:, 1].max() + .2
    xx, yy = np.meshgrid(np.linspace(xmin, xmax, 180), np.linspace(ymin, ymax, 140))
    grid = scaler.transform(np.column_stack([xx.ravel(), yy.ravel()]))
    with torch.no_grad():
        surface = torch.sigmoid(model(torch.tensor(grid, dtype=torch.float32))).numpy().reshape(xx.shape)
    linear_surface = baseline.predict_proba(grid)[:, 1].reshape(xx.shape)
    fig = plt.figure(figsize=(12.0, 7.4), layout='constrained')
    gs = fig.add_gridspec(2, 4, height_ratios=[1.2, 1])
    for i, (name, values) in enumerate([(label('线性分类器', 'Linear classifier'), linear_surface),
                                        (label('多层感知机', 'Multilayer perceptron'), surface)]):
        ax = fig.add_subplot(gs[0, 2*i:2*i+2])
        img = ax.contourf(xx, yy, values, levels=np.linspace(0, 1, 11), cmap='RdBu_r', alpha=.72)
        ax.contour(xx, yy, values, levels=[.5], colors=['#253b45'], linewidths=1.4)
        for cls, color in [(0, blue), (1, amber)]:
            mask = y_test == cls
            ax.scatter(X_test[mask, 0], X_test[mask, 1], c=color, s=17, edgecolor='white', linewidth=.35,
                       label=label(f'测试类别 {cls}', f'Test class {cls}'))
        ax.set(title=name, xlabel=label('特征 1（无量纲）', 'Feature 1 (dimensionless)'),
               ylabel=label('特征 2（无量纲）', 'Feature 2 (dimensionless)'))
        ax.set_aspect('equal'); ax.legend(fontsize=9, loc='lower left')
    ax = fig.add_subplot(gs[1, :3])
    ax.plot(history[:, 0], history[:, 1], color=blue, label=label('训练', 'Train'))
    ax.plot(history[:, 0], history[:, 2], color=amber, label=label('验证', 'Validation'))
    ax.axvline(best_epoch, color=teal, ls='--', lw=1)
    ax.set(xlabel=label('训练轮数', 'Epoch'), ylabel=label('平均交叉熵', 'Mean cross entropy'))
    ax.legend(fontsize=9)
    ax = fig.add_subplot(gs[1, 3])
    cm = confusion_matrix(y_test, probability >= .5)
    ax.imshow(cm, cmap='Blues', vmin=0)
    for i in range(2):
        for j in range(2):ax.text(j, i, str(cm[i, j]), ha='center', va='center', color='white' if cm[i,j]>65 else '#142e38', fontsize=15)
    ax.set(xticks=[0, 1], yticks=[0, 1], xlabel=label('预测类别', 'Predicted class'),
           ylabel=label('真实类别', 'True class'))
    fig.colorbar(img, ax=fig.axes[:2], shrink=.6, label=label('类别 1 的预测概率', 'Predicted probability of class 1'))
    fig.savefig(output / f'learning-{language}.svg');plt.close(fig)

    fig, ax = plt.subplots(figsize=(11.7, 4.2));ax.set(xlim=(0, 11), ylim=(0, 3));ax.axis('off')
    nodes=[(1, 'x = 2', label('输入', 'Input')), (3.3, 'z = wx + b\n= 0.5000', label('加权求和', 'Affine map')),
           (6, f'h = tanh(z)\n= {h0:.4f}', label('非线性变换', 'Nonlinearity')),
           (9, f'L = (h − y)² / 2\n= {float(scalar_loss.detach()):.4f}', label('比较目标 y = 1', 'Compare with target y = 1'))]
    for pos,text,subtitle in nodes:
        ax.text(pos,1.8,text,ha='center',va='center',fontsize=13,bbox={'boxstyle':'round,pad=.65','facecolor':'#edf5f8','edgecolor':'none'})
        ax.text(pos,.75,subtitle,ha='center',va='center',fontsize=11)
    for a,bx in [(1.65,2.4),(4.3,5),(7,7.9)]:
        ax.annotate('',xy=(bx,1.8),xytext=(a,1.8),arrowprops={'arrowstyle':'->','color':blue,'lw':2})
        ax.annotate('',xy=(a,2.65),xytext=(bx,2.65),arrowprops={'arrowstyle':'->','color':amber,'lw':2})
    ax.text(5.4,2.92,label('反向：把每一步的变化率乘起来','Backward: multiply local rates of change'),ha='center',color=amber)
    ax.text(5.4,.15,label(f'w = 0.3，b = −0.1；梯度 dL/dw = {analytic:.6f}',f'w = 0.3, b = −0.1; gradient dL/dw = {analytic:.6f}'),ha='center')
    fig.savefig(output / f'graph-{language}.svg');plt.close(fig)

    fig, axes = plt.subplots(1,2,figsize=(11,4.2),layout='constrained',gridspec_kw={'width_ratios':[1.4,1]})
    axes[0].loglog(epsilons,np.maximum(np.abs(numeric-analytic),1e-17),'o-',color=blue)
    axes[0].set(xlabel=label('有限差分步长 ε（无量纲）','Finite-difference step ε (dimensionless)'),
                ylabel=label('梯度绝对误差','Absolute gradient error'))
    factors=[h0-target,1-h0*h0,x]
    axes[1].barh([0,1,2],factors,color=[amber,teal,blue])
    axes[1].set(yticks=[0,1,2],yticklabels=['∂L/∂h','∂h/∂z','∂z/∂w'],xlabel=label('局部导数（无量纲）','Local derivative (dimensionless)'))
    axes[1].axvline(0,color='#65747d',lw=.8)
    for i,v in enumerate(factors):axes[1].text(v+(0.04 if v>=0 else -.04),i,f'{v:.4f}',ha='left' if v>=0 else 'right',va='center')
    axes[1].set_xlim(-1.1,2.5)
    fig.savefig(output / f'gradient-{language}.svg');plt.close(fig)
    summary={'seed':19,'sizes':{'train':600,'validation':200,'test':200},
             'epochs':180,'best_epoch':best_epoch,'parameter_count':sum(p.numel() for p in model.parameters()),
             'mlp_test_accuracy':accuracy_score(y_test,probability>=.5),
             'linear_test_accuracy':accuracy_score(y_test,baseline_probability>=.5),
             'mlp_test_log_loss':log_loss(y_test,probability),'validation_log_loss':best_loss,
             'gradient_analytic':analytic,'gradient_autograd':autograd,
             'gradient_finite_difference_eps_1e4':float(numeric[3]),'reload_max_error':reload_error,
             'versions':{'torch':torch.__version__,'numpy':np.__version__},'confusion_matrix':cm.tolist()}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',X_train=X_train,y_train=y_train,X_valid=X_valid,y_valid=y_valid,
             X_test=X_test,y_test=y_test,probability=probability,history=history)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('results'))
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    experiment(args.output,args.language)
```

![同一固定划分上的线性分类器与MLP。边界图只叠加200个测试样本，颜色背景为类别1概率；下方为180轮训练/验证损失及所选模型的测试混淆矩阵，虚线标记第52轮。](https://ml-biomat.com/static/tutorials/machine-learning/figures/236ec5e95d58b170b9d2bb19.svg?v=236ec5e95d58)

图 2同一固定划分上的线性分类器与MLP。边界图只叠加200个测试样本，颜色背景为类别1概率；下方为180轮训练/验证损失及所选模型的测试混淆矩阵，虚线标记第52轮。

这次固定配置的运行中，线性分类器在 200 个测试样本上正确分类 175 个，准确率为 87.5%；337 参数的 MLP 正确分类 189 个，准确率为 94.5%。验证损失最低出现在第 52 轮，测试交叉熵约为 0.1313。先沿着左侧两幅图看边界：线性模型的分界方向一致，MLP 可以绕着弯月改变方向。随后再看下方的学习曲线和混淆矩阵，判断改进来自哪些样本，而不是只记住一个百分数。

混淆矩阵按真实类别分行、预测类别分列：第一类有 98 个判对、2 个判错，第二类有 91 个判对、9 个判错。那些错误的位置值得回到散点图中查看，有的落在噪声造成的交叠区域。增加网络宽度能够改变边界的细致程度，却不会自动消除输入中本来就含糊的信息。这个例子教我们同时考察数据形状、概率与错误分布；把同样的工作流程移到真实任务时，也应先确定标签和测量是否足够支持所问的问题。

## 怎样知道梯度和训练确实算对了

训练损失下降是一条有用线索，却不能单独说明每项实现都正确。短计算链可以独立核验：用公式求一次导数，用自动微分求一次，再让权重分别增加和减少一个很小的量，观察两次损失的差。最后一种中央差分没有使用反向传播内部的规则，因此适合检查自定义运算。扰动太大时，它测的是一段较宽区间的平均斜率；扰动太小时，两个几乎相等的浮点数相减会损失有效数字。

$$
g_{\mathrm{FD}}(w;\varepsilon)=\frac{L(w+\varepsilon)-L(w-\varepsilon)}{2\varepsilon}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/040ee07b10011f083afb82ca.svg) | 中央有限差分近似梯度，本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | 被检查的标量权重，其余输入与参数保持固定。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | 正扰动步长，与w单位相同；本例取0.0001。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | 与前面完全相同的半平方损失函数。 |

上下两次扰动之间相距2ε，因此用损失差除以2ε估计斜率。对w=0.3、ε=0.0001，两次实际计算给出梯度−0.846033503；与解析值绝对差约1.88×10⁻⁸。

![左图比较不同有限差分步长的梯度绝对误差；右图展开链式法则的三个局部因子。64位运算下误差先降后升，能看到截断与浮点舍入的共同影响。](https://ml-biomat.com/static/tutorials/machine-learning/figures/da9d58051ba2dcc88631b3f9.svg?v=da9d58051ba2)

图 3左图比较不同有限差分步长的梯度绝对误差；右图展开链式法则的三个局部因子。64位运算下误差先降后升，能看到截断与浮点舍入的共同影响。

图中不同扰动尺度的误差并非单调下降，这正是截断误差与舍入误差共同作用的结果。采用 64 位浮点数、扰动为 0.0001 时，有限差分得到约 −0.846033503，解析导数和自动微分均为约 −0.846033485，绝对差约 1.88×10⁻⁸。这个检查针对的是光滑的 tanh 计算链；若把测试点放在 ReLU 的折点附近，左右斜率不同，便需要先说清采用的导数约定与检查位置。

对整个训练过程，值得建立一套可操作的观察顺序。首先检查形状、标签范围和有限数值，再确认一个很小的数据子集能被模型拟合，然后观察训练与验证曲线是否同步变化。若训练损失继续降低而验证损失上升，模型正在更贴近训练样本的细节；验证集保存最佳轮次就是对这一现象的直接处理。若两条曲线都很高，则应回到模型容量、输入信息、学习率和优化步骤逐项定位。对照图让这些原因比一句“模型效果不好”更具体。

## 亲手转动一个权重

输入固定为2，偏置为−0.1，目标为1。拖动权重可以沿完整损失曲线移动；再选择学习率并执行一步更新，观察负梯度方向如何改变预测与损失。把权重设为0.05时，tanh输入恰为零，梯度可以直接手算成−2。

[Figure: 损失随权重变化与局部切线](https://ml-biomat.com/tutorials/machine-learning/m09/#M09-lab)

| 量 | 当前值 |
| --- | --- |
| w | 0.300000 |

## 让一次实验成为可以复用的模型

训练结束后真正需要保存的，不止是一串权重。输入曾按什么均值和尺度标准化、输出分数怎样变成概率、使用什么阈值做分类，都属于预测过程的一部分。程序把权重与标准化参数一起存入文件，并重新建立同样的网络结构加载它们。重载时从原始测试坐标出发，用文件里的均值和尺度重新标准化，再计算分数；它与原预测的最大差为零。这个检查直接回答“文件中是否保留了这次模型的行为”，比仅确认某个文件存在更有意义。

固定随机种子使数据划分、参数初始化和批次顺序有明确起点；记录库版本、模型结构与训练设置，则让别人知道是在什么计算条件下得到结果。本例同时记录这些信息，并把测试输入、预测概率和训练历史保存在数据文件中。换硬件、换底层实现或换库版本时，浮点运算顺序可能改变，因此比较实验时仍应围绕相同的数据定义和评价流程组织证据。对噪声较强的研究任务，多个随机种子的重复实验还可以说明结论是否稳定。

到这里，一个神经网络已经可以拆成具体对象：输入经过带参数的变换，损失衡量目标差异，链式法则给出局部调整方向，优化器完成更新，验证与测试回答不同的评价问题。下一章会把学习率、动量、AdamW、初始化和正则化展开，解释为什么同一结构会因为训练方法不同而出现很不一样的学习曲线。再往后看到卷积、循环或注意力层时，可以继续追问同一件事：它改变了哪一种信息传递方式，又怎样在实验里看出这种改变。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M09.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Dive into Deep Learning — Forward Propagation, Backward Propagation, and Computational Graphs](https://d2l.ai/chapter_multilayer-perceptrons/backprop.html)

   沿计算图理解前向与反向的系统教材。

   CC BY-SA 4.0
2. [PyTorch — Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

   梯度记录、backward和关闭梯度的官方说明。

   BSD-3-Clause (tutorial repository)
3. [PyTorch — Datasets & DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)

   样本封装、小批量与迭代的数据接口。

   BSD-3-Clause (tutorial repository)
4. [Rumelhart, Hinton & Williams (1986), Learning representations by back-propagating errors](https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf)

   多层网络学习内部表示的方法史阅读。
