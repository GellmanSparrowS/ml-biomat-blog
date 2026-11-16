# MLPs and backpropagation: how a network learns

Source: https://ml-biomat.com/tutorials/machine-learning/m09/en/
Language: en

From a hand-calculable chain to a neural network you can train, evaluate, and save.

## When a straight line cannot separate the data

Imagine recording the positions of two groups of people on a map. One group walks around a lake; the other follows a curved running trail. Given the horizontal and vertical coordinates of a new position, we want to decide which group it belongs to. A straight dividing line may be inadequate when the routes curl around one another like two interlocking crescents. This small problem illustrates a practical use of neural networks: they learn combinations of transformations that can express curved, conditional, and piecewise relationships. Recognizing an object in a photograph or interpreting several machine sensors involves the same need for useful combinations, although the inputs and relationships are much larger.

Our experiment reduces the problem to a picture by generating a synthetic two-moons dataset. Each observation has two dimensionless coordinates and a binary label, so the data, predicted probabilities, and decision boundary can all be inspected together. A linear classifier provides a baseline. We then train a multilayer perceptron, or MLP, with two hidden layers. Its curved boundary comes from an actual execution of the accompanying program. By the end of the chapter, you should be able to explain how one parameter influences the final error, check a gradient independently, and connect training, validation, testing, and model saving into a reproducible procedure.

A useful analogy is a set of connected adjustment knobs. Each knob controls how some input affects the output, but turning one knob also changes what later parts of the system receive. The central question is therefore which knob to turn and how far to turn it. The forward calculation answers what the system currently predicts. A loss function converts the discrepancy from the target into a number. Backpropagation measures the local influence of each parameter on that number. Together, these operations turn the vague instruction to “make the model learn” into a sequence of numerical decisions that we can examine.

## Building a transformation from artificial neurons

An artificial neuron first multiplies its inputs by weights, adds the products, and includes a bias. A weight specifies the direction and strength of one input's contribution; the bias shifts the overall starting point. An activation function then changes the shape of this weighted sum. If every activation is removed, a sequence of matrix multiplications and bias additions can be collapsed into one affine transformation. Writing that calculation as many layers does not create a nonlinear decision boundary. With nonlinear activations, different units can respond to different regions, and later layers can recombine those responses into more complicated relationships.

$$
\mathbf{h}=\phi(\mathbf{W}\mathbf{x}+\mathbf{b})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4fa2300af121b336bb0d7845.svg) | Input column vector, shape d×1; standardized coordinates, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e376aab419a2e38d8eb39d69.svg) | Weight matrix, shape m×d; each row describes one output unit, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/639196a1a30d6f6280e3cf49.svg) | Bias vector, shape m×1, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | Elementwise activation, such as tanh or ReLU. |
| ![Formula](https://ml-biomat.com/static/agent-math/412791ff09271eea93125852.svg) | Activated output vector, shape m×1, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/79008c488d4b7c757e91cbd3.svg) | d counts input features and m output units; dimensionless integers. |

Matrix multiplication applies m different weight sets to the same input. Each weighted sum receives a bias and activation. For d=2, m=1, x=(2,−1), W=(0.5,0.2), and b=0.1, the preactivation is 0.9. ReLU returns 0.9; tanh returns approximately 0.7163.

Consider the inputs 2 and −1, weights 0.5 and 0.2, and bias 0.1. Their weighted sum is 0.5×2 + 0.2×(−1) + 0.1 = 0.9. A ReLU activation passes this positive value through unchanged. If the sum had been −0.9, ReLU would instead produce zero. The tanh activation behaves differently: it maps any real input into the interval between −1 and 1, changes smoothly near zero, and gradually flattens toward the ends. ReLU creates piecewise responses, whereas tanh creates smooth compression. We use tanh here because its smooth derivative makes the later hand calculation and finite-difference check especially easy to follow.

The word “hidden” does not mean that a layer is inaccessible. It means that its values are intermediate quantities rather than labels supplied directly with the training observations. Our input contains two coordinates. The first hidden layer produces 16 numbers; the second produces another 16; the output layer produces one classification score. The first layer contains 2×16 + 16 = 48 parameters, the second 16×16 + 16 = 272, and the output layer 16 + 1 = 17. The total is 337. Counting connections and biases in this way also reveals how increasing width affects storage and arithmetic work.

The name “neuron” borrows biological language, but the object used here is a precisely defined computational rule. No background in neurophysiology is required to understand it. The essential distinction is between data, parameters, and intermediate results. Coordinates come from observations. Weights and biases are updated during training. Activations change when different observations pass through the network. All three may appear as tensors in a program, so their numerical container alone does not tell us their role. Drawing a computation graph makes these roles and dependencies visible, which is useful when debugging a much larger model.

## Follow one short computation from beginning to end

Before training the whole network, keep just one input, one weight, and one nonlinear operation. Set the input to 2, the target to 1, the initial weight to 0.3, and a fixed bias to −0.1. The weighted sum is 0.5. Applying tanh gives approximately 0.4621, which is about −0.5379 below the target. For this short hand calculation, use half the squared error as the loss; its value is approximately 0.1447. The factor of one half cancels the factor of two introduced by differentiation. It changes the scale of the loss but not the prediction that minimizes it.

$$
z=wx+b,\qquad h=\tanh z,\qquad L=\frac12(h-y)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Input x and target y; x=2 and y=1, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8d6a07eeeed288d729c0d812.svg) | Weight w=0.3 and fixed bias b=−0.1, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0df8baa5e5b619840f653237.svg) | Weighted sum z and activation h, dimensionless scalars. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Half-squared error for one observation; dimensionless and nonnegative. |

Substitute in graph order: z=0.3×2−0.1=0.5, h≈0.462117, and L≈0.144659. Squaring makes either sign of error incur a nonnegative cost; the factor one half simplifies its derivative.

![A one-observation computation graph. Blue arrows follow values from input to loss; orange arrows show backward order. Values come from the specified scalar example.](https://ml-biomat.com/static/tutorials/machine-learning/figures/8c55c272dc50b7a875142f15.svg?v=8c55c272dc50)

Figure 1A one-observation computation graph. Blue arrows follow values from input to loss; orange arrows show backward order. Values come from the specified scalar example.

Read each box in the diagram as a small worksheet. It receives its inputs, performs one operation, and passes a result to the next worksheet. The weighted-sum operation does not need to know the final target. The tanh operation does not need to know how large the loss will be. Only the last node compares prediction with target. A computation graph records these dependencies. If an intermediate value feeds several branches, the framework can identify every path that depends on it. Residual connections, shared parameters, and recurrent networks create more elaborate graphs, but the same dependency-based reasoning still applies.

This connects to a difficulty faced by early multilayer networks: once an output error is known, how should an internal connection be adjusted? The 1986 work by Rumelhart, Hinton, and Williams helped bring widespread attention to learning internal representations through error backpropagation. The key idea is not that each internal node must understand the entire task. Instead, the influence of a final error can be propagated through local rates of change along known computational dependencies. Our short chain is a version of that credit-assignment problem small enough to calculate with a handheld calculator. It also separates the mathematical mechanism from claims about the scale of a modern system.

## Backpropagation carries rates of change

A derivative can initially be understood as a local amplification factor. If an input increases slightly, how much does the next quantity change? In our chain, changing the weight first changes the weighted sum, then the tanh output, and finally the loss. Multiplying those three local rates gives the rate at which the loss changes with the weight. The input is 2, so a small weight change is doubled at the weighted-sum node. The slope of tanh near 0.5 is approximately 0.7864, which reduces the change. The prediction is below its target, making the derivative of loss with respect to prediction negative.

$$
\frac{\partial L}{\partial w}=(h-y)(1-h^2)x,\qquad w_{\mathrm{new}}=w-\eta\frac{\partial L}{\partial w}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/74cc380f215a14d626b16938.svg) | Local rate of loss change with the weight; dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/896a3446dd4c698f708be84d.svg) | tanh output h, target y, and input x, as above. |
| ![Formula](https://ml-biomat.com/static/agent-math/e8027609d6efc5e71c2c8166.svg) | Scalar weights before and after the update, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Positive learning rate, 0.1 here; dimensionless for this example. |

The three factors are derivatives of the loss, tanh, and weighted sum: −0.537883×0.786448×2≈−0.846033. One update gives 0.3−0.1×(−0.846033)≈0.384603. Multiplication follows the chain rule; subtracting the gradient gives a locally downhill direction.

The product is approximately −0.8460. Its sign says that increasing the weight a little will reduce the loss near the current point. With a learning rate of 0.1, one gradient-descent update moves the weight from 0.3 to approximately 0.3846. The learning rate controls how far we choose to travel in a direction suggested by the local slope. It is not a distance automatically certified by the derivative. A derivative describes the neighborhood of the current parameter value; a very large step may cross a low-loss region and increase the loss again. Correct direction and suitable step length therefore require separate attention.

When a computation graph branches, a shared variable may influence the loss through several paths. The contributions from those paths must be added before propagating further backward. Backpropagation performs these multiplications and additions in reverse dependency order, reusing intermediate results instead of recomputing every complete path. For a scalar loss with many parameters, this reverse-mode approach is particularly efficient. Obtaining all parameter gradients generally requires work of the same order as the forward calculation. By contrast, independently perturbing each parameter would require a large number of repeated forward evaluations. This computational difference matters long before the network becomes enormous.

PyTorch's automatic-differentiation system records tensor operations and applies their derivative rules. It implements the chain rule at the operation level rather than estimating derivatives through tiny parameter perturbations. A leaf tensor whose gradient is required must participate in gradient tracking; trainable parameters in neural-network modules are already organized for that role. After `backward()`, each parameter's `.grad` contains its accumulated gradient. The optimizer then uses those gradients to update parameters. Automation removes a great deal of repetitive arithmetic, while a small analytic example and an independent numerical check preserve our ability to understand what the system is doing.

## Align samples, tensors, predictions, and losses

A tensor is a numerical array with a shape. One observation with two coordinates can be represented by a vector of length 2. A batch of 64 observations becomes a tensor with shape 64×2. The final network layer produces one score per observation, giving an output of shape 64×1. We reshape the target labels to 64×1 as well. This prevents certain elementwise expressions from silently broadcasting into an unintended 64×64 array. Naming the sample axis, feature axis, and output axis is a practical habit: shape errors can produce plausible-looking numbers, so a successful program execution by itself does not establish a correct calculation.

A sigmoid transforms a classification score into a number between zero and one, interpreted as a predicted probability. The two-moons classifier is trained with binary cross entropy rather than the squared-error loss used in our short hand calculation. Assigning high probability to the observed class gives a small loss. Assigning high confidence to the wrong class gives a much larger loss. Thus, this objective considers both whether the prediction points toward the right class and how confident it is. In the implementation, the untransformed score goes directly into `BCEWithLogitsLoss`, which combines the sigmoid and logarithmic calculations in a numerically stable form.

$$
p_i=\sigma(s_i),\qquad \mathcal{L}=-\frac1B\sum_{i=1}^{B}\big[y_i\log p_i+(1-y_i)\log(1-p_i)\big]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39a5e1fd0c0f25384d2357d0.svg) | Sample index i and batch size B, dimensionless integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | The network logit for observation i, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Sigmoid function mapping scores into the interval from zero to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/043e1e9a3c94510bfcdeec48.svg) | Predicted probability p_i of class 1 and binary label y_i, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/656d8346ef3238a285037c0c.svg) | Natural logarithm and mean cross entropy; measured in nats, with no physical dimension. |

For label 1, the individual loss reduces to −log(p). Probability 0.8 gives approximately 0.2231, while 0.2 gives 1.6094. A confident wrong prediction is more costly. Averaging over B samples provides a comparable batch-loss scale.

`TensorDataset` pairs each input with the target at the same index. `DataLoader` sends these pairs to the network in batches and can reshuffle their order for each epoch. Our batch size is 64. Because 600 is not divisible by 64, the final batch is smaller. For each batch, the program clears previous gradients, evaluates the forward calculation, backpropagates the loss, and updates the parameters. PyTorch normally accumulates new gradients into the existing gradient buffers, so `zero_grad` explicitly controls when a fresh accumulation begins. Deliberately accumulating across batches is also possible, but the loss scaling and update schedule must then be chosen consistently.

Two other controls serve different purposes. `model.eval()` changes the behavior of layers such as Dropout and BatchNorm, whereas `torch.no_grad()` prevents subsequent operations from building a gradient-tracking graph. Our tanh network contains neither of those special layers, but the code still uses training and evaluation modes explicitly. This keeps the procedure correct when a later experiment changes the architecture. Inputs, labels, and model parameters must also reside on compatible devices. Everything in this chapter runs on a CPU, allowing us to establish the computational logic before introducing parallel execution and acceleration.

## Train a real model and inspect unseen observations

The complete program below generates 1,000 two-moons observations with noise level 0.23 and declared random seeds. It first sets aside 200 test observations. The remaining data are divided into 600 training observations and 200 validation observations. Standardization statistics are fitted on the training inputs alone; the same mean and scale are then applied to validation and test inputs. This sequence makes the question being evaluated clear: how well does the fitted procedure predict new observations? Preprocessing should be learned from the training information available to that procedure, rather than quietly using the held-out sample to prepare its inputs.

The program trains for 180 epochs, records training and validation cross entropy, and retains the parameter state with the lowest validation loss. Test labels do not participate in choosing that state. The principal test metrics are computed after model selection. Logistic regression is fitted as a baseline using exactly the same training observations and standardized coordinates. Sharing the split helps relate differences to the models and training settings. Run `python main.py --output results --language en` to reproduce the English figures. Selecting `zh` changes plot labels to Chinese while retaining the same data, parameters, and numerical experiment.

### Complete experiment: from splitting data to reloading a model

Requires NumPy, Matplotlib, scikit-learn, and PyTorch. The seeded synthetic experiment trains a 337-parameter MLP; its output directory contains three figures, weights, data, and numerical summaries.

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

![Linear classifier and MLP on one fixed split. Maps overlay only the 200 test observations; background color shows class-1 probability. The lower panels show 180 epochs of training/validation loss and the selected model’s test confusion matrix. The dashed line marks epoch 52.](https://ml-biomat.com/static/tutorials/machine-learning/figures/a52dcf3c8296038cb9ec810c.svg?v=a52dcf3c8296)

Figure 2Linear classifier and MLP on one fixed split. Maps overlay only the 200 test observations; background color shows class-1 probability. The lower panels show 180 epochs of training/validation loss and the selected model’s test confusion matrix. The dashed line marks epoch 52.

In this execution of the fixed configuration, the linear classifier correctly classified 175 of the 200 test observations, giving 87.5% accuracy. The 337-parameter MLP correctly classified 189, giving 94.5%. The lowest validation loss occurred at epoch 52, and the selected MLP's test cross entropy was approximately 0.1313. Begin reading the figure with the two decision maps. The linear classifier maintains one straight dividing direction, whereas the MLP changes direction around the crescents. Then examine the learning curves and confusion matrix. These panels explain where the improvement occurs and how the selected parameter state was obtained.

The confusion matrix uses rows for true classes and columns for predicted classes. Class 0 contains 98 correct predictions and 2 errors; class 1 contains 91 correct predictions and 9 errors. Return to the scatterplots to examine the difficult observations. Some occupy regions where noise causes the classes to overlap. Increasing network width changes the detail that the boundary can express, but does not automatically remove ambiguity in the measured inputs. This experiment therefore teaches a joint reading of data geometry, probability, and error distribution. In a practical task, that same reading should begin with whether the available measurements and labels support the question being asked.

## Check the derivative as well as the learning curve

A decreasing training loss is useful evidence, but it does not independently verify every implementation detail. Our short computation can be checked three ways: derive its gradient analytically, obtain the result from automatic differentiation, and compare two losses evaluated after small positive and negative weight perturbations. The final method, a central finite difference, does not rely on the backward rules used inside autograd. It is therefore useful when testing custom operations. A large perturbation measures an average slope over a broad neighborhood. An extremely small perturbation subtracts nearly equal floating-point values, which can lose meaningful digits.

$$
g_{\mathrm{FD}}(w;\varepsilon)=\frac{L(w+\varepsilon)-L(w-\varepsilon)}{2\varepsilon}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/040ee07b10011f083afb82ca.svg) | Central finite-difference gradient approximation, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | Scalar weight being checked; all other inputs and parameters are fixed. |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Positive perturbation, with the same units as w; 0.0001 in the worked check. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Exactly the same half-squared loss function used above. |

The two perturbed weights are 2ε apart, so divide the loss difference by 2ε. At w=0.3 and ε=0.0001 the evaluated slope is −0.846033503, about 1.88×10⁻⁸ from the analytic derivative.

![Left: absolute gradient error across finite-difference step sizes. Right: the three local chain-rule factors. The error decreases and later rises in float64 arithmetic, revealing truncation and floating-point effects.](https://ml-biomat.com/static/tutorials/machine-learning/figures/12ffa6ad0fcfcc73c9b067d6.svg?v=12ffa6ad0fcf)

Figure 3Left: absolute gradient error across finite-difference step sizes. Right: the three local chain-rule factors. The error decreases and later rises in float64 arithmetic, revealing truncation and floating-point effects.

The error curve is not monotonically decreasing as the perturbation shrinks. Truncation error dominates at larger steps, while floating-point cancellation becomes visible at sufficiently small steps. With 64-bit floating-point arithmetic and a perturbation of 0.0001, the finite-difference gradient is approximately −0.846033503. Both the analytic calculation and autograd give approximately −0.846033485, an absolute difference of about 1.88×10⁻⁸. This check uses a smooth tanh chain. If an analogous check straddles the corner of a ReLU function, the left and right slopes differ; the derivative convention and test position must be considered before interpreting the discrepancy.

For a whole training pipeline, use a similarly concrete order of inspection. Check tensor shapes, label ranges, and finite numerical values. Then see whether the model can fit a deliberately small subset. Finally, compare training and validation curves. When training loss continues downward while validation loss rises, the fitted model is becoming more specific to the training observations. Retaining the best validation epoch responds directly to that behavior. When both losses remain high, examine the information in the inputs, model capacity, learning rate, and update sequence. These observations turn a broad statement about poor performance into a set of testable computational questions.

## Turn one weight yourself

The input is fixed at 2, bias at −0.1, and target at 1. Moving the weight explores the complete loss curve. Select a learning rate and take one update to see how the negative-gradient direction changes prediction and loss. At weight 0.05, the tanh input is exactly zero and the gradient is easily calculated as −2.

[Figure: Loss against weight with local tangent](https://ml-biomat.com/tutorials/machine-learning/m09/en/#M09-lab)

| Quantity | Current value |
| --- | --- |
| w | 0.300000 |

## Turn one experiment into a reusable predictor

A reusable predictor contains more than a sequence of weights. The mean and scale used to standardize its input, the mapping from score to probability, and the threshold used to select a class all belong to the prediction procedure. Our program stores the weights together with the standardization parameters. It then reconstructs the architecture and loads the saved state. Starting from raw test coordinates, it reapplies the mean and scale read from the file and computes new scores. Their maximum difference from the original predictions is zero. This check answers a specific question: whether the saved file preserves this model's numerical behavior. It is stronger than checking that a file with an appropriate name exists.

Fixed random seeds establish starting points for data generation, splitting, initialization, and batch order. Recording software versions, architecture, and training settings describes the computational conditions under which the outputs were produced. The example keeps these values in its summary and saves test inputs, probabilities, and training history in a separate data file. Changing hardware, libraries, or underlying implementations may change floating-point operation order, so comparative studies should still use a clearly shared data definition and evaluation procedure. Repeating noisy experiments with several seeds can then show how stable an observed comparison is across random realizations.

A neural network can now be understood as a collection of concrete objects: parameterized transformations carry inputs forward, a loss measures discrepancy from the target, the chain rule supplies local adjustment directions, an optimizer updates parameters, and held-out data answer distinct evaluation questions. The next chapter develops learning rates, momentum, AdamW, initialization, and regularization, explaining why the same architecture can produce very different learning curves. When convolution, recurrence, or attention appears later, the same questions remain productive: what information flow does this operation change, why should that change help a particular task, and where can its effect be seen in a calculation or experiment?

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M09.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning — Forward Propagation, Backward Propagation, and Computational Graphs](https://d2l.ai/chapter_multilayer-perceptrons/backprop.html)

   A systematic treatment of forward and backward computation graphs.

   CC BY-SA 4.0
2. [PyTorch — Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

   Official explanation of gradient tracking, backward, and disabling recording.

   BSD-3-Clause (tutorial repository)
3. [PyTorch — Datasets & DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)

   Data interfaces for examples, batches, and iteration.

   BSD-3-Clause (tutorial repository)
4. [Rumelhart, Hinton & Williams (1986), Learning representations by back-propagating errors](https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf)

   Historical reading on learning internal representations in multilayer networks.
