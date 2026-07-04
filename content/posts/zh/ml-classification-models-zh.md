---
title: "常用的机器学习分类模型：从逻辑回归到梯度提升"
date: "2026-06-30"
category: "machine-learning"
tags: ["机器学习", "分类模型", "逻辑回归", "SVM", "随机森林", "XGBoost", "scikit-learn"]
lang: "zh"
slug: "ml-classification-models-zh"
description: "系统梳理常用机器学习分类模型：从逻辑回归、KNN、SVM到决策树、随机森林和梯度提升，含核心原理对比、scikit-learn代码实现和应用场景分析。"
---

## 一、分类问题的本质——从标签到决策边界

分类（Classification）是监督学习中最基础、应用最广泛的任务类型。它的目标简单而明确：给定一个输入样本，判断它属于哪个预定义的类别。这个描述听起来平淡，但几乎所有需要"做判断"的科学和工程问题都可以被归入这个框架。细胞图像中的健康细胞与癌变细胞，X 射线图像中的裂纹与正常区域，材料测试结果中的疲劳断裂与韧性断裂——这些都是分类问题。能否建立一个准确、可解释、计算高效的分类模型，往往决定了一项计算科研工作的价值上限。

从数学框架来说，分类问题的结构如下：我们有一个训练数据集 \(\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N\)，其中 \(\mathbf{x}_i \in \mathbb{R}^d\) 是第 i 个样本的特征向量（d 维），\(y_i \in \{1, 2, \ldots, K\}\) 是对应的类别标签。目标是学习一个映射函数 \(f: \mathbb{R}^d \rightarrow \{1, 2, \ldots, K\}\)，使得对训练集之外的新样本，f 也能给出大体正确的预测。当 \(K=2\) 时称为**二分类**，当 \(K>2\) 时称为**多分类**。

理解分类的核心直觉是**决策边界（Decision Boundary）**。想象在二维特征空间中画了两类点：红点和蓝点。分类器的本质工作是在这片空间里画一条线（或曲面），把它们分开。不同算法本质上是不同的"画线方式"：逻辑回归画一条直线，SVM 找最宽的"隔离带"，决策树用平行于坐标轴的折线切格子，神经网络则可以画任意复杂的曲线。理解这个直觉，就理解了为什么没有哪个算法在所有问题上最优——最好的"画线方式"取决于数据的内在分布和研究问题的具体约束。

在 Python 生态中，几乎所有主流分类算法都以统一接口封装在 scikit-learn 中，其设计极为 Pythonic：所有分类器都继承自相同的基类，具备 `.fit()`、`.predict()`、`.predict_proba()` 方法，可以无缝组合成 Pipeline。以下是本文贯穿始终的数据准备模板：

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load a classic multi-class dataset (150 samples, 4 features, 3 classes)
X, y = load_iris(return_X_y=True)

# Stratified split preserves class proportions in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Standardize features: zero mean, unit variance
# Critical for distance-based and gradient-based models
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)   # Use training statistics only
```

注意 `stratify=y` 参数保证训练集和测试集中各类别比例一致，避免因类别不平衡导致的评估偏差。特征标准化对逻辑回归、SVM、k-NN 等基于距离或梯度的模型至关重要，但对决策树和随机森林不影响结果。这些细节将在后续各节中反复涉及。

---

## 二、逻辑回归——概率视角下的线性分类

尽管名字里有"回归"二字，逻辑回归（Logistic Regression）是一个彻头彻尾的分类模型。它是初学者学习的第一个分类器，也是工业界最常用的基线模型之一，原因在于它不仅给出"这属于哪类"的判断，还给出"有多大把握"的概率估计。理解逻辑回归，实际上是理解所有参数化分类模型的共同基础。

先建立直觉。假设要根据一块材料的硬度值（一维特征）判断它是金属还是非金属。直觉上，硬度越高，越可能是金属。"越可能"意味着我们需要一个函数把硬度值（取值范围 \(-\infty\) 到 \(+\infty\)）映射到一个概率（0 到 1 之间）。直接用线性函数 \(y = w_0 + w_1 x\) 不行，因为线性函数值域是整个实数轴。逻辑回归的解决方案是**Sigmoid 函数**（也叫 logistic 函数）：

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

这个函数把任意实数压缩到 (0, 1) 区间内，形状是一条 S 形曲线：z 很大时趋近于 1，z 很小时趋近于 0，z=0 时恰好等于 0.5。逻辑回归把线性函数 \(z = \mathbf{w}^T\mathbf{x} + b\) 的输出喂给 sigmoid，得到样本属于正类的概率：

$$P(y=1|\mathbf{x}) = \sigma(\mathbf{w}^T\mathbf{x} + b) = \frac{1}{1+e^{-(\mathbf{w}^T\mathbf{x}+b)}}$$

决策边界是满足 \(\mathbf{w}^T\mathbf{x} + b = 0\) 的超平面——在二维特征空间里，这就是一条直线。预测概率 > 0.5 时判定为正类，否则为负类。

参数 \(\mathbf{w}\) 和 \(b\) 通过**最大似然估计（MLE）**求得：找一组参数，使得训练数据在当前模型下出现的概率最大。对 N 个样本的对数似然函数（即负交叉熵损失的相反数）为：

$$\mathcal{L}(\mathbf{w}, b) = \sum_{i=1}^N \left[ y_i \log \hat{p}_i + (1-y_i) \log(1-\hat{p}_i) \right]$$

其中 \(\hat{p}_i = \sigma(\mathbf{w}^T\mathbf{x}_i + b)\)。最大化这个函数没有解析解，通常用梯度下降或 L-BFGS 求解。为了防止过拟合，可以在目标函数中加入正则化项：L2 正则化（Ridge，`penalty='l2'`）使权重趋向于小但非零；L1 正则化（Lasso，`penalty='l1'`）倾向于产生稀疏权重（许多权重恰好为零），在特征选择上尤为有用。

对生物和材料研究者特别有价值的一点在于，逻辑回归的系数 \(\mathbf{w}\) 具有直接的可解释性。对特征 \(x_j\)，\(e^{w_j}\) 是该特征增加一个单位时，样本属于正类的**优势比（Odds Ratio）**的变化倍数。这使逻辑回归不仅是预测工具，更是特征重要性的分析工具，这在医疗和材料科学研究中往往比预测精度本身更有价值。

```python
from sklearn.linear_model import LogisticRegression

# C is the inverse of regularization strength (smaller C = stronger regularization)
model = LogisticRegression(C=1.0, penalty='l2', solver='lbfgs',
                           max_iter=500, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # Shape: (n_samples, n_classes)

print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Coefficients: shape (n_classes, n_features) for multi-class (OvR scheme)
import numpy as np
feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
for i, cls in enumerate(['setosa', 'versicolor', 'virginica']):
    top_feat = feature_names[np.argmax(np.abs(model.coef_[i]))]
    print(f"Class '{cls}' most important feature: {top_feat}")
```

逻辑回归的局限性在于它只能学习**线性**决策边界。如果两类数据在特征空间中非线性可分（一类包围另一类），纯粹的逻辑回归就会失效。解决方法是加入多项式特征（用 `PolynomialFeatures` 做特征工程）或改用能处理非线性的模型。即便如此，在数据量有限、可解释性要求高的场景下，优先尝试逻辑回归仍是明智之举。

---

## 三、支持向量机——最宽的"隔离带"

支持向量机（Support Vector Machine, SVM）在 1990 年代由 Vapnik 和 Cortes 等人发展成熟，在核函数技术出现后一度是机器学习领域表现最优的分类器，在小数据集和高维数据（如基因表达谱分类）上至今仍有很强的竞争力。它的设计思想来自一个发人深省的问题：能分开两类点的直线有无数条，哪一条最好？

SVM 的回答是：**最宽的那条**。更准确地说，SVM 寻找使两类样本到决策边界的最小距离（"间隔"，margin）最大化的超平面。那些离决策边界最近的样本点被称为**支持向量（Support Vectors）**——它们"支撑"起了这个最大间隔。一个关键性质是：移动任何非支持向量的点，决策边界完全不变；但稍微移动一个支持向量，边界就会改变。这意味着 SVM 只被最难分类的那些点决定，忽略了大多数"容易"的样本。

数学形式化如下：对二分类问题，标签 \(y_i \in \{-1, +1\}\)，SVM 求解：

$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 \quad \text{s.t.} \quad y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1, \quad \forall i$$

间隔宽度等于 \(2/\|\mathbf{w}\|\)，最小化 \(\|\mathbf{w}\|^2\) 等价于最大化间隔。这是**硬间隔（Hard Margin）SVM**，要求数据线性可分。现实数据几乎总有噪声，因此引入**松弛变量**的软间隔版本，允许部分样本越过间隔边界，但对违规程度施以惩罚，强度由超参数 C 控制：C 越大，对误分类惩罚越严（决策边界更硬，可能过拟合）；C 越小，允许更多违规（更宽松，更鲁棒）。

SVM 真正的威力来自**核技巧（Kernel Trick）**。对于非线性可分的数据，通过映射函数 \(\phi(\mathbf{x})\) 将数据投影到更高维（甚至无限维）的特征空间，在那个空间里寻找线性分界面。核函数 \(k(\mathbf{x}_i, \mathbf{x}_j) = \phi(\mathbf{x}_i)^T\phi(\mathbf{x}_j)\) 让我们不需要显式计算高维映射，只计算原始特征之间的核值，避免了维度爆炸。常用核函数有四种：线性核 \(k = \mathbf{x}_i^T\mathbf{x}_j\)（等价于不做映射，适合高维稀疏数据）；多项式核 \(k = (\gamma \mathbf{x}_i^T\mathbf{x}_j + r)^d\)（捕捉特征交互）；RBF 径向基核 \(k = \exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2)\)（最通用的选择，可实现任意平滑非线性分界）；Sigmoid 核 \(k = \tanh(\gamma \mathbf{x}_i^T\mathbf{x}_j + r)\)（类似神经网络激活）。在不确定时，RBF 核是首选。

```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# SVM with RBF kernel — most versatile choice for non-linear problems
param_grid = {
    'C':     [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.01, 0.1]
}
svm = SVC(kernel='rbf', probability=True, random_state=42)

# 5-fold cross-validation grid search
grid_search = GridSearchCV(svm, param_grid, cv=5,
                           scoring='accuracy', n_jobs=-1, verbose=0)
grid_search.fit(X_train, y_train)

best_svm = grid_search.best_estimator_
print(f"Best params: {grid_search.best_params_}")
print(f"Test accuracy: {accuracy_score(y_test, best_svm.predict(X_test)):.4f}")
```

SVM 的主要局限在于计算复杂度随样本数增加接近 \(O(N^2)\) 到 \(O(N^3)\)，在大数据集（N > 50,000）上速度极慢；超参数 C 和 \(\gamma\) 的选择对结果影响很大，必须交叉验证搜索；输出不是自然概率（`probability=True` 会额外用 Platt scaling 校准，但增加计算量）。对于高维稀疏特征（文本、基因组），配合线性核的 `LinearSVC` 是高效的替代方案，可以处理数十万样本。

---

## 四、决策树——透明可解释的树形判断

决策树（Decision Tree）是机器学习中可解释性最好的分类器之一，其决策逻辑可以直接被人类理解——这在医疗诊断、材料失效分析等高风险领域至关重要。"为什么这个样品被判断为疲劳断裂？"决策树可以用一条清晰的 if-then-else 链回答，而黑盒神经网络做不到。

决策树的直觉极为自然。想象你在做猜物游戏，每次只能问"是/否"类型的问题。好的玩家会优先问能把候选范围切得最均匀的问题——"它是动物吗？"比"它是哺乳动物吗？"信息量更大，因为前者把候选范围分成了更均等的两半。决策树的训练过程就是系统地找这样的问题（特征和阈值）：每次把数据集一分为二，不断重复，直到每个子集都"足够纯"（只含一种类别）或达到预设的停止条件。这种贪心的逐步分裂策略叫做**递归分区（Recursive Partitioning）**。

"足够纯"在数学上通过**不纯度（Impurity）**度量。两种最常用的度量是香农熵和基尼不纯度。节点 t 的**香农熵（Shannon Entropy）**定义为：

$$H(t) = -\sum_{k=1}^K p_k \log_2 p_k$$

其中 \(p_k\) 是节点 t 中属于第 k 类的样本比例。纯节点（只含一种类别）的熵为 0，最不纯节点（各类均等）的熵最大为 \(\log_2 K\)。用特征 A 在阈值处分裂节点 t 获得的**信息增益（Information Gain）**为：

$$\text{IG}(t, A) = H(t) - \left(\frac{|t_L|}{|t|} H(t_L) + \frac{|t_R|}{|t|} H(t_R)\right)$$

即分裂前后的熵之差，差值越大越好。**基尼不纯度（Gini Impurity）**则是：

$$G(t) = 1 - \sum_{k=1}^K p_k^2$$

Gini 计算上比熵稍快（避免对数运算），scikit-learn 的 `DecisionTreeClassifier` 默认使用 Gini。两者在绝大多数情况下结果差别不大。

决策树的一个核心问题是**过拟合**。如果不加限制，它会一直生长到每个叶节点只含一个样本——训练集准确率 100%，但对新数据泛化很差。常见的防止策略有两类：**预剪枝（Pre-pruning）**在训练时设置停止条件，例如最大深度 `max_depth` 和叶节点最少样本数 `min_samples_leaf`；**后剪枝（Post-pruning）**在树完全生长后，再由下至上剪掉对验证集无贡献的分支（scikit-learn 的 `cost_complexity_pruning_path` 实现了基于代价-复杂度的剪枝）。

```python
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

# Limit tree depth to prevent overfitting
tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=5,
                               criterion='gini', random_state=42)
tree.fit(X_train, y_train)

print(f"Tree depth: {tree.get_depth()}, Leaves: {tree.get_n_leaves()}")
print(f"Test accuracy: {accuracy_score(y_test, tree.predict(X_test)):.4f}")

# Human-readable text representation
feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
print(export_text(tree, feature_names=feature_names))

# Visual representation (ideal for papers/reports)
fig, ax = plt.subplots(figsize=(16, 8))
plot_tree(tree, feature_names=feature_names,
          class_names=['setosa', 'versicolor', 'virginica'],
          filled=True, rounded=True, impurity=True, ax=ax)
plt.tight_layout()
plt.show()

# Feature importances: total Gini impurity reduction contributed by each feature
print("Feature importances:", dict(zip(feature_names, tree.feature_importances_)))
```

决策树的另一个优良特性是自带**特征重要性（Feature Importance）**：通过统计每个特征在所有分裂点上贡献的不纯度降低量，可以为特征打分。这在材料科学中非常实用：哪些力学参数最能区分失效模式？哪些基因特征最能预测细胞命运？决策树的重要性评分是理解数据的第一把钥匙，但需注意它对高基数（取值种类很多）特征有轻微偏好，这是一个已知的系统性偏差。

---

## 五、随机森林与集成学习——群体智慧

单棵决策树直觉清晰但容易过拟合。随机森林（Random Forest）通过集成大量决策树来解决这个问题，体现了一个简单而深刻的思想：**多个弱学习器联合，往往胜过一个强学习器**。理解随机森林，需要先理解机器学习中一对核心矛盾——偏差与方差。

**偏差-方差权衡（Bias-Variance Tradeoff）**是理解任何学习算法的基础框架。一个学习器的期望误差可以分解为三部分：**偏差**（模型假设与真实规律之间的系统性偏差，反映模型的表达能力）、**方差**（模型对训练数据随机波动的敏感程度，反映模型的稳定性）和不可约误差（数据本身的噪声）。决策树的典型问题是高方差：同样的问题，换一批训练样本，树的结构可能面目全非。集成方法的思路是：既然单个模型方差大，就训练多个模型然后综合它们的预测——多个高方差模型的平均，方差会大幅降低，而偏差基本不变。这就是**Bagging（Bootstrap Aggregating）**的本质。

**随机森林**在 Bagging 之上再加一层随机化，以保证各棵树尽量独立、预测误差尽量不相关：

**第一层——Bootstrap 抽样**：对训练集做有放回抽样，得到 T 个大小相同但内容不同的子集，各自训练一棵完整的决策树。由于有放回抽样，每次约有 63.2% 的原始样本被选中；其余约 36.8% 未被选中的样本称为 **OOB（Out-of-Bag）样本**，可以在不另设验证集的情况下直接估计泛化误差。

**第二层——特征随机化**：在每个节点做分裂时，不从全部 d 个特征中选最优，而是随机抽取 \(m \approx \sqrt{d}\) 个特征（分类），只在这个子集中寻找最优分裂点。这进一步削弱了各树之间的相关性，使平均后的方差降低更多。

预测时，T 棵树各自给出一个预测类别，用多数投票（分类）或均值（回归）作为最终结果。

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,      # Number of trees; more is generally better up to a point
    max_depth=None,        # Grow full trees (depth controlled by min_samples)
    min_samples_leaf=2,    # Minimum samples required at a leaf node
    max_features='sqrt',   # Random feature subset per split: sqrt(d)
    oob_score=True,        # Estimate generalization with OOB samples
    n_jobs=-1,             # Parallelize across all available CPU cores
    random_state=42
)
rf.fit(X_train, y_train)

print(f"OOB generalization estimate: {rf.oob_score_:.4f}")
print(f"Test accuracy:               {accuracy_score(y_test, rf.predict(X_test)):.4f}")

# Aggregated feature importances across all trees (mean Gini decrease)
feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
importances = dict(zip(feature_names, rf.feature_importances_))
print("Feature importances:", importances)
```

**梯度提升（Gradient Boosting）**是集成学习的另一条主线，与随机森林的"并行训练"截然不同，它采用**串行**策略：每棵新树专门拟合前面所有树的残差（当前模型预测错误的方向），逐步纠正前任的错误，相当于在函数空间中做梯度下降。这让梯度提升通常比随机森林偏差更低，在 Kaggle 等结构化数据竞赛中几乎是标配。现代实现如 XGBoost、LightGBM 和 CatBoost，通过直方图加速、叶节点最优分裂等工程优化，在大数据集上速度极快。

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,  # Shrinkage: smaller lr + more trees often better
    max_depth=3,         # Shallow trees ("stumps") are typical for boosting
    subsample=0.8,       # Stochastic gradient boosting: use 80% of data per tree
    random_state=42
)
gb.fit(X_train, y_train)
print(f"Gradient Boosting Test accuracy: {accuracy_score(y_test, gb.predict(X_test)):.4f}")
```

对研究者的实用建议：随机森林是"开箱即用"最可靠的分类器之一。它对特征缩放不敏感，能处理混合类型特征，对少量缺失值有一定鲁棒性，且通过 OOB 误差可估计泛化性能，省去了另设验证集的麻烦。在不知道用什么模型的时候，随机森林是最安全的起点。在需要更高精度时，再考虑 LightGBM 等梯度提升系列。

---

## 六、k 近邻——最懒惰的学习者

k 近邻（k-Nearest Neighbors, k-NN）是机器学习中最直觉化的算法，也是"懒惰学习（Lazy Learning）"的典型代表。它的思想来自一个日常经验：**看一个人的邻居，就能猜出这个人的性质**。在特征空间中，k-NN 找到离测试样本最近的 k 个训练样本，用这 k 个邻居的多数类标签作为预测结果。没有任何显式的参数拟合过程，"学习"就是把训练数据原封不动地记忆下来。

这种"懒惰"既是优点也是缺点。优点在于无需训练、数据可以随时增量加入；缺点在于每次预测都需要计算与所有训练样本的距离，时间复杂度是 \(O(Nd)\)，对大数据集极慢（可以用 KD-Tree 或 Ball-Tree 加速到 \(O(\log N)\)，但高维下性能下降明显）。

距离度量的选择对 k-NN 的性能影响巨大。最常用的是**欧氏距离（L2）**：

$$d(\mathbf{x}, \mathbf{x}') = \sqrt{\sum_{j=1}^d (x_j - x_j')^2}$$

和**曼哈顿距离（L1）**：

$$d(\mathbf{x}, \mathbf{x}') = \sum_{j=1}^d |x_j - x_j'|$$

欧氏距离对大尺度特征更敏感，曼哈顿距离在高维空间中往往更稳定（对离群点的鲁棒性更好）。**特征标准化对 k-NN 至关重要**——如果一个特征范围是 1—100，另一个是 \(10^6 - 10^9\)，欧氏距离会被后者完全主导，前者的信息被淹没。

k 的选择决定了模型复杂度：k=1 时，模型极度局部，高方差（倾向过拟合）；k=N 时，总是预测训练集的多数类，高偏差（欠拟合）。通常通过交叉验证找到最优 k。

k-NN 还有一个更深层的理论障碍：**维度灾难（Curse of Dimensionality）**。在高维空间中，随着维度 d 增大，所有点之间的距离趋于相等——"近邻"的概念失去意义。可以直觉上理解为：在 100 维空间里，一个点和它最近邻的距离与它和最远点的距离之比趋近于 1，"近"和"远"的区别消失。这意味着 k-NN 在原始高维特征空间（如原始像素或原始基因表达向量）中性能很差，通常需要先做 PCA 或 UMAP 降维，再在低维嵌入空间中使用 k-NN。

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Find optimal k via cross-validation
k_range = range(1, 31)
cv_scores = [
    cross_val_score(
        KNeighborsClassifier(n_neighbors=k, metric='euclidean'),
        X_train, y_train, cv=5, scoring='accuracy'
    ).mean()
    for k in k_range
]

optimal_k = list(k_range)[np.argmax(cv_scores)]
print(f"Optimal k: {optimal_k}, CV accuracy: {max(cv_scores):.4f}")

# Train with optimal k; distance-weighted voting often improves performance
knn = KNeighborsClassifier(n_neighbors=optimal_k, weights='distance',
                           algorithm='auto', metric='euclidean')
knn.fit(X_train, y_train)
print(f"Test accuracy: {accuracy_score(y_test, knn.predict(X_test)):.4f}")
```

`weights='distance'` 让近邻的投票权重与距离成反比，越近的邻居影响越大，通常比等权重投票效果更好，尤其是在类别边界附近。

---

## 七、朴素贝叶斯——概率推断的极简哲学

朴素贝叶斯（Naive Bayes）是基于贝叶斯定理的概率分类器，以计算极简、训练极快著称，在文本分类（垃圾邮件检测）和生物序列分析中有悠久应用历史。理解它需要先理解贝叶斯定理的核心逻辑：如何在观测到数据后**系统性地更新我们的信念**。

**贝叶斯定理**形式如下：

$$P(y|\mathbf{x}) = \frac{P(\mathbf{x}|y) \cdot P(y)}{P(\mathbf{x})}$$

其中 \(P(y)\) 是**先验概率**（看到样本前，各类别出现的概率），\(P(\mathbf{x}|y)\) 是**似然**（已知类别 y，特征向量 \(\mathbf{x}\) 出现的概率），\(P(y|\mathbf{x})\) 是我们真正想要的**后验概率**（给定特征，属于类别 y 的概率），\(P(\mathbf{x})\) 是归一化常数（与类别无关，分类时可以直接忽略）。

分类时，选择使后验概率最大的类别（MAP 决策规则）：

$$\hat{y} = \arg\max_y P(\mathbf{x}|y) \cdot P(y)$$

核心难题在于 \(P(\mathbf{x}|y) = P(x_1, x_2, \ldots, x_d | y)\) 是 d 维联合分布，在高维时几乎不可能从有限数据中直接估计。**朴素贝叶斯的"朴素假设"**在此登场：假设给定类别标签 y 时，各特征之间**条件独立**：

$$P(\mathbf{x}|y) = \prod_{j=1}^d P(x_j|y)$$

这个假设在现实中几乎从来不成立（特征之间总有相关性），但实践中往往给出出人意料的好结果。原因在于：即使假设错误，它也以一种一致的方式错误，不同类别的预测误差方向相似，最终的排名（哪类后验概率最高）可能仍然正确。这是机器学习中"错误的模型，有用的预测"的经典案例。

在这个假设下，只需估计每个特征在每个类别下的一维分布。对连续特征，通常假设高斯分布（高斯朴素贝叶斯）：

$$P(x_j|y=k) = \frac{1}{\sqrt{2\pi\sigma_{kj}^2}} \exp\left(-\frac{(x_j - \mu_{kj})^2}{2\sigma_{kj}^2}\right)$$

只需从训练数据中估计每类每特征的均值 \(\mu_{kj}\) 和方差 \(\sigma_{kj}^2\)，计算量极小，且是完全解析解，不需要任何迭代优化。

```python
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)

print(f"Test accuracy: {accuracy_score(y_test, gnb.predict(X_test)):.4f}")

# Inspect learned parameters
print("Class priors P(y):", gnb.class_prior_)
# theta_: per-class per-feature means, shape (n_classes, n_features)
print("Per-class feature means:\n", gnb.theta_)
```

朴素贝叶斯的优势是：训练速度极快（\(O(Nd)\)），输出是校准良好的概率，对小数据集稳定，缺失特征可优雅跳过。针对不同数据类型有变体：`MultinomialNB` 适合词频等计数特征（文本分类的标准选择），`BernoulliNB` 适合二值特征（基因是否表达）。主要缺点是条件独立假设的违背会损害性能，对强相关特征数据集，表现往往不如 SVM 或随机森林。

---

## 八、评估指标——准确率只是起点

训练好一个分类器之后，用什么指标评估它的好坏？很多初学者默认用**准确率（Accuracy）**：正确分类的样本占总样本的比例。但准确率在类别不平衡时是一个危险的简化——如果一个疾病数据集中 99% 是健康样本，一个永远预测"健康"的分类器准确率高达 99%，但它对疾病检测毫无用处。理解评估指标，本质上是理解"在我的问题里，什么叫做犯了错误，这个错误有多严重"。

理解评估指标的基础是**混淆矩阵（Confusion Matrix）**。对二分类问题，混淆矩阵有四个格子：

| | 预测正类 | 预测负类 |
|---|---|---|
| **实际正类** | TP（真正例） | FN（假负例，漏报） |
| **实际负类** | FP（假正例，误报） | TN（真负例） |

从这四个数字派生出一系列关键指标：

**精确率（Precision）**衡量"我报告的阳性中，有多少是真阳性"：

$$\text{Precision} = \frac{TP}{TP+FP}$$

在假阳性代价高的场景（癌症误诊导致不必要手术，材料误判导致过度维修），精确率更重要。

**召回率（Recall，也叫灵敏度/Sensitivity）**衡量"我把所有真阳性都找出来了吗"：

$$\text{Recall} = \frac{TP}{TP+FN}$$

在漏报代价高的场景（结构缺陷漏检导致灾难性失效，疾病漏诊延误治疗），召回率更重要。精确率和召回率之间天然存在权衡：降低分类阈值会提高召回率但降低精确率，反之亦然。

**F1 分数**是两者的调和均值，在类别不平衡时比准确率更有参考价值：

$$F_1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**ROC 曲线与 AUC** 通过改变分类阈值，绘制假阳性率（FPR = FP/(FP+TN)）对真阳性率（TPR = Recall）的曲线。AUC（曲线下面积）取值 [0, 1]，0.5 表示随机猜测，1.0 表示完美分类。AUC 不受类别不平衡影响，是二分类综合评估的标准指标之一。

```python
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    classification_report, roc_auc_score,
    RocCurveDisplay
)
import matplotlib.pyplot as plt

# Use breast cancer dataset for binary classification demo
X_bc, y_bc = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(
    X_bc, y_bc, test_size=0.2, random_state=42, stratify=y_bc
)
sc = StandardScaler()
X_tr = sc.fit_transform(X_tr)
X_te = sc.transform(X_te)

clf = LogisticRegression(max_iter=1000, C=1.0)
clf.fit(X_tr, y_tr)
y_pred_bc = clf.predict(X_te)
y_prob_bc  = clf.predict_proba(X_te)[:, 1]  # Probability of positive class

# Confusion matrix visualization
ConfusionMatrixDisplay(
    confusion_matrix(y_te, y_pred_bc),
    display_labels=['Malignant', 'Benign']
).plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# Full classification report
print(classification_report(y_te, y_pred_bc,
                            target_names=['Malignant', 'Benign']))

# AUC-ROC
auc = roc_auc_score(y_te, y_prob_bc)
print(f"AUC-ROC: {auc:.4f}")
RocCurveDisplay.from_predictions(y_te, y_prob_bc,
                                  name="Logistic Regression").plot()
plt.title(f"ROC Curve (AUC = {auc:.3f})")
plt.show()
```

最后，**K 折交叉验证（K-Fold Cross-Validation）**是评估泛化性能的金标准。将数据分成 K 个子集，依次以其中一个作为验证集，其余为训练集，重复 K 次，取平均性能。这比单次分割更可靠，尤其在数据量有限时（这在生物和材料科学实验数据中极为常见）。`StratifiedKFold` 保证每折内类别比例一致，是不平衡数据的必备选项。

---

## 九、模型选择指南——没有免费的午餐

没有哪个分类器在所有问题上最优——这是机器学习中"没有免费的午餐定理（No Free Lunch Theorem）"的通俗表达：对所有可能的问题平均，任何两个算法的期望性能相同。实际科研中，选择分类器应综合考虑以下维度，而非照单全收某个"最好的"模型。

**数据量**是第一个约束。数据量极少（N < 500）时，逻辑回归、朴素贝叶斯和 SVM 往往比参数量大的模型稳定，因为它们的归纳偏置（inductive bias）更强，不容易在少量数据上过拟合；数据量大（N > 100,000）时，梯度提升（XGBoost、LightGBM）和深度学习的潜力才能充分发挥，SVM 因为 \(O(N^2)\) 的训练代价变得不切实际。

**可解释性**是第二个约束，在医疗、监管和工程安全领域往往是硬性要求。需要向临床医生或工程师解释决策逻辑时，决策树和逻辑回归是优先选择。逻辑回归的系数直接量化每个特征的贡献方向和强度；决策树可以打印出完整的 if-then 规则链。随机森林和梯度提升通过特征重要性分数提供部分解释性，但远不如前两者直接。神经网络则基本是黑盒，需要额外的可解释 AI（XAI）工具（如 SHAP、LIME）来事后解释。

**特征维度**是第三个约束。低维特征（d < 20）：k-NN、朴素贝叶斯和决策树都能有效工作；中等维度（20 < d < 1000）：SVM（RBF 核）和随机森林是主力；高维稀疏（文本、基因组，d > 1000）：线性 SVM（`LinearSVC`）、逻辑回归（L1 正则）和朴素贝叶斯是首选，因为它们的计算复杂度与非零特征数线性相关。

**类别不平衡**几乎在真实科研数据中普遍存在，需要在任何模型中单独处理：调整类权重（几乎所有 sklearn 分类器都支持 `class_weight='balanced'`），或在数据层面用 SMOTE 过采样少数类。

| 模型 | 训练速度 | 预测速度 | 可解释性 | 特征缩放 | 小数据 | 高维稀疏 |
|---|---|---|---|---|---|---|
| 逻辑回归 | 快 | 快 | 高 | 需要 | ✓ | ✓（L1） |
| SVM（RBF） | 中~慢 | 中 | 低 | 需要 | ✓ | ✗ |
| 决策树 | 快 | 快 | 最高 | 不需要 | 中 | ✗ |
| 随机森林 | 中 | 中 | 中 | 不需要 | 中 | 中 |
| 梯度提升 | 慢 | 中 | 中 | 不需要 | ✗ | 中 |
| k-NN | 无（懒惰） | 慢 | 中 | 需要 | ✓ | ✗ |
| 朴素贝叶斯 | 极快 | 极快 | 中 | 不需要 | ✓ | ✓ |

实践建议：在一个新问题上，永远先建立一个简单基线（逻辑回归或随机森林），了解数据的基础难度和特征的相对重要性，再根据结果决定是否需要更复杂的模型。一个精心调参的随机森林，往往能在大多数结构化科研数据问题上给出令人满意的结果，且解释性远优于神经网络。对"是否要上神经网络"这个问题，答案通常是：除非你有充足的数据（N > 10,000）、充分的计算资源，且经典方法已经确实无法满足需求，否则先把经典分类器做好。

---
## 参考文献

1. Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

2. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324

3. Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297. https://doi.org/10.1007/BF00994018

4. Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451

5. Cover, T. M., & Hart, P. E. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21–27. https://doi.org/10.1109/TIT.1967.1053964

6. Zhang, H. (2004). The optimality of naive Bayes. *Proceedings of the 17th International FLAIRS Conference*. American Association for Artificial Intelligence.

7. Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters*, 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010

8. Wolpert, D. H. (1996). The lack of a priori distinctions between learning algorithms. *Neural Computation*, 8(7), 1341–1390. https://doi.org/10.1162/neco.1996.8.7.1341