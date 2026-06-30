---
title: "Common Classification Models in Machine Learning: From Logistic Regression to Gradient Boosting"
date: "2026-06-30"
category: "machine-learning"
tags: ["machine learning", "classification", "logistic regression", "SVM", "random forest", "XGBoost", "scikit-learn"]
lang: "en"
slug: "ml-classification-models"
description: "A systematic overview of common ML classification models, from logistic regression to gradient boosting, with principles, code, and comparison."
---

## 1. What Is Classification — From Labels to Decision Boundaries

Classification is the most fundamental and widely applied task in supervised machine learning. Its goal is straightforward: given an input sample, determine which predefined category it belongs to. This description may sound deceptively simple, but nearly every scientific or engineering problem that requires a "judgment call" can be framed within this structure. Distinguishing healthy cells from cancerous ones in microscopy images, identifying cracks versus intact regions in X-ray scans, differentiating fatigue fracture from ductile failure in materials testing — all of these are classification problems. Whether a classification model can be built that is accurate, interpretable, and computationally efficient often determines the scientific ceiling of a computational research project.

Formally, a classification problem is defined as follows. We are given a training dataset \(\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N\), where \(\mathbf{x}_i \in \mathbb{R}^d\) is the feature vector of the i-th sample (d-dimensional) and \(y_i \in \{1, 2, \ldots, K\}\) is its class label. The objective is to learn a mapping \(f: \mathbb{R}^d \rightarrow \{1, 2, \ldots, K\}\) that generalizes correctly to new, unseen samples. When \(K=2\), this is **binary classification**; when \(K>2\), it is **multi-class classification**.

The core intuition behind classification is the **decision boundary**. Imagine plotting two categories of points — red and blue — in a two-dimensional feature space. A classifier's fundamental job is to draw a surface that separates them. Different algorithms differ in how they draw this surface: logistic regression draws a straight line, SVMs find the widest possible "separation band," decision trees cut the space with axis-aligned boundaries, and neural networks can produce arbitrarily complex curves. This intuition immediately suggests why no single algorithm dominates all problems — the optimal boundary shape depends on the data's intrinsic distribution and the constraints imposed by the scientific context.

In the Python ecosystem, virtually all mainstream classification algorithms are encapsulated under a unified interface in scikit-learn. Every classifier inherits from the same base class and exposes `.fit()`, `.predict()`, and `.predict_proba()` methods, making it easy to swap models with a single line change. Below is the data preparation template used throughout this article:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load a classic multi-class dataset (150 samples, 4 features, 3 classes)
X, y = load_iris(return_X_y=True)

# Stratified split preserves class proportions in both subsets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Standardize features: zero mean, unit variance
# Critical for distance-based and gradient-based models
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)   # Apply training statistics only
```

The `stratify=y` argument ensures that class proportions are preserved in both the training and test sets, preventing evaluation bias due to class imbalance. Feature standardization is critical for logistic regression, SVMs, and k-NN, but leaves decision trees and random forests completely unaffected. These details recur throughout subsequent sections.

---

## 2. Logistic Regression — Linear Classification Through a Probabilistic Lens

Despite its name, logistic regression is a classification model through and through. It is the first classifier most practitioners learn and one of the most frequently used baselines in both academic research and industry, precisely because it not only outputs a predicted class but also a calibrated probability estimate. Understanding logistic regression amounts to understanding the probabilistic foundations shared by nearly all parametric classifiers.

Start with the intuition. Suppose you want to classify a material as metal or non-metal based on its hardness score (a one-dimensional feature). Intuitively, higher hardness implies a higher probability of being metal. But "higher probability" needs to be quantified. A linear function \(z = w_0 + w_1 x\) is unsuitable because its range is the entire real line, whereas probabilities must lie in (0, 1). Logistic regression solves this with the **sigmoid function**:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

This function maps any real number into (0, 1), producing an S-shaped curve that approaches 1 for large z, approaches 0 for small z, and equals 0.5 at z = 0. Logistic regression feeds the output of a linear function \(z = \mathbf{w}^T\mathbf{x} + b\) through the sigmoid to estimate the probability of the positive class:

$$P(y=1|\mathbf{x}) = \sigma(\mathbf{w}^T\mathbf{x} + b) = \frac{1}{1+e^{-(\mathbf{w}^T\mathbf{x}+b)}}$$

The decision boundary is the hyperplane \(\mathbf{w}^T\mathbf{x} + b = 0\) — a straight line in two-dimensional feature space. Samples with predicted probability above 0.5 are assigned to the positive class; otherwise the negative class.

Parameters \(\mathbf{w}\) and \(b\) are learned by **maximum likelihood estimation (MLE)**: find the parameter values that maximize the probability of observing the training labels. The log-likelihood for N samples is:

$$\mathcal{L}(\mathbf{w}, b) = \sum_{i=1}^N \left[ y_i \log \hat{p}_i + (1-y_i) \log(1-\hat{p}_i) \right]$$

where \(\hat{p}_i = \sigma(\mathbf{w}^T\mathbf{x}_i + b)\). Maximizing this (equivalently, minimizing the **cross-entropy loss**) has no closed-form solution and is typically solved by gradient descent or L-BFGS. Regularization terms prevent overfitting: L2 (Ridge) shrinks weights toward zero without eliminating them, while L1 (Lasso) promotes sparsity — many weights become exactly zero — which serves as an implicit feature selection mechanism.

A key advantage particularly relevant for biology and materials science researchers: the learned coefficients \(\mathbf{w}\) are directly interpretable. For feature \(x_j\), the exponentiated coefficient \(e^{w_j}\) is the multiplicative change in the **odds ratio** for a one-unit increase in that feature. This makes logistic regression not just a prediction tool but an analytical instrument for identifying which features most strongly discriminate between classes.

```python
from sklearn.linear_model import LogisticRegression

# C is the inverse of regularization strength: smaller C = stronger regularization
model = LogisticRegression(C=1.0, penalty='l2', solver='lbfgs',
                           max_iter=500, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # Shape: (n_samples, n_classes)

print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Identify the most important feature per class (by absolute coefficient magnitude)
import numpy as np
feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
for i, cls in enumerate(['setosa', 'versicolor', 'virginica']):
    top = feature_names[np.argmax(np.abs(model.coef_[i]))]
    print(f"Class '{cls}' most discriminative feature: {top}")
```

Logistic regression's key limitation is that it can only learn **linear** decision boundaries. If two classes are not linearly separable in feature space — for instance, if one class surrounds the other — logistic regression will fail regardless of how well it is tuned. Solutions include polynomial feature engineering (using `PolynomialFeatures`) or switching to a nonlinear model. Even so, in settings with limited data or strong interpretability requirements, logistic regression should always be the starting point.

---

## 3. Support Vector Machines — The Widest Possible Margin

Support vector machines (SVMs) were developed by Cortes, Vapnik, and colleagues in the 1990s. After the introduction of the kernel trick, SVMs briefly held the status of state-of-the-art classifier across many domains. For small datasets and high-dimensional data — such as gene expression profiling — they remain highly competitive. Their design philosophy stems from a provocative question: among the infinitely many hyperplanes that correctly separate two classes, which one is the best?

SVM's answer is: **the one with the widest margin**. More precisely, SVM seeks the hyperplane that maximizes the minimum distance from any training sample to the decision boundary — the "margin." The training points that lie exactly on the margin boundaries are the **support vectors**, so named because they "support" the margin: moving any non-support-vector sample leaves the decision boundary unchanged, while shifting a single support vector changes the boundary. This means the entire model is determined by the hardest, most ambiguous examples.

Formally, for binary classification with labels \(y_i \in \{-1, +1\}\), the hard-margin SVM solves:

$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 \quad \text{s.t.} \quad y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1, \quad \forall i$$

The margin width equals \(2/\|\mathbf{w}\|\), so minimizing \(\|\mathbf{w}\|^2\) is equivalent to maximizing the margin. This formulation requires data to be linearly separable. Real data rarely is, so the **soft-margin** variant introduces slack variables, allowing some samples to violate the margin while penalizing the degree of violation. The hyperparameter C controls the tradeoff: large C penalizes misclassification harshly (tight margin, more prone to overfitting); small C tolerates more violations (wider, more robust margin).

The true power of SVMs lies in the **kernel trick**. For nonlinearly separable data, a mapping \(\phi(\mathbf{x})\) projects inputs into a higher-dimensional (potentially infinite-dimensional) feature space, where a linear boundary is sought. The kernel function \(k(\mathbf{x}_i, \mathbf{x}_j) = \phi(\mathbf{x}_i)^T\phi(\mathbf{x}_j)\) lets us compute inner products in the high-dimensional space without ever constructing \(\phi\) explicitly — avoiding prohibitive computational cost. Common kernels include the linear kernel \(k = \mathbf{x}_i^T\mathbf{x}_j\) (equivalent to no mapping; ideal for high-dimensional sparse data), the polynomial kernel \(k = (\gamma \mathbf{x}_i^T\mathbf{x}_j + r)^d\), the widely used RBF kernel \(k = \exp(-\gamma\|\mathbf{x}_i - \mathbf{x}_j\|^2)\) (which implicitly performs infinite-order polynomial expansion), and the sigmoid kernel.

```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C':     [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.01, 0.1]
}
svm = SVC(kernel='rbf', probability=True, random_state=42)

# 5-fold cross-validated grid search
grid_search = GridSearchCV(svm, param_grid, cv=5,
                           scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_svm = grid_search.best_estimator_
print(f"Best params: {grid_search.best_params_}")
print(f"Test accuracy: {accuracy_score(y_test, best_svm.predict(X_test)):.4f}")
```

SVMs have notable limitations: training complexity approaches \(O(N^2)\) to \(O(N^3)\), making them impractical for datasets larger than ~50,000 samples; hyperparameter selection (C and \(\gamma\)) strongly influences performance and requires cross-validated search; and the output is not a natural probability (the `probability=True` flag applies Platt scaling post-hoc, at additional computational cost). For high-dimensional sparse inputs such as text or genomics data, `LinearSVC` with a linear kernel is a far more scalable alternative.

---

## 4. Decision Trees — Transparent, Rule-Based Classification

Decision trees are among the most interpretable classifiers in machine learning. Their decision logic can be understood directly by human experts — a crucial property in high-stakes domains such as medical diagnosis and structural failure analysis. When asked "why was this sample classified as fatigue fracture?", a decision tree can answer with a clear if-then-else chain; a black-box neural network cannot.

The intuition behind decision trees is entirely natural. Imagine playing a guessing game where you can only ask yes/no questions. A skilled player prioritizes questions that divide the remaining possibilities into roughly equal halves — "Is it an animal?" is more informative than "Is it a mammal?" because the former more evenly splits the candidate space. Decision tree training does exactly this systematically: at each node, find the feature and threshold that most effectively splits the current data subset, then repeat recursively until each subset is "pure" (contains only one class) or a stopping criterion is met. This greedy recursive splitting strategy is known as **recursive partitioning**.

"Purity" is quantified by an **impurity measure**. Two standard choices are Shannon entropy and Gini impurity. The **Shannon entropy** at node t is:

$$H(t) = -\sum_{k=1}^K p_k \log_2 p_k$$

where \(p_k\) is the fraction of samples at node t belonging to class k. A pure node has entropy 0; a maximally mixed node has entropy \(\log_2 K\). The **information gain** from splitting node t on feature A is:

$$\text{IG}(t, A) = H(t) - \left(\frac{|t_L|}{|t|} H(t_L) + \frac{|t_R|}{|t|} H(t_R)\right)$$

Larger information gain means a more useful split. The **Gini impurity** is:

$$G(t) = 1 - \sum_{k=1}^K p_k^2$$

Gini is computationally slightly cheaper (no logarithm) and is the default criterion in scikit-learn's `DecisionTreeClassifier`. The two measures typically yield very similar results in practice.

A critical issue with decision trees is **overfitting**. Without constraints, a tree will grow until every leaf node contains a single sample — achieving 100% training accuracy but failing to generalize. Standard remedies include **pre-pruning** (setting `max_depth`, `min_samples_leaf` before growth) and **post-pruning** (growing a full tree and then removing branches that do not improve performance on a held-out set).

```python
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=5,
                               criterion='gini', random_state=42)
tree.fit(X_train, y_train)

print(f"Depth: {tree.get_depth()}, Leaves: {tree.get_n_leaves()}")
print(f"Test accuracy: {accuracy_score(y_test, tree.predict(X_test)):.4f}")

# Print human-readable rule set
feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
print(export_text(tree, feature_names=feature_names))

# Visualize the tree structure
fig, ax = plt.subplots(figsize=(16, 8))
plot_tree(tree, feature_names=feature_names,
          class_names=['setosa', 'versicolor', 'virginica'],
          filled=True, rounded=True, impurity=True, ax=ax)
plt.tight_layout()
plt.show()

# Feature importances: aggregated Gini impurity reduction per feature
print("Feature importances:", dict(zip(feature_names, tree.feature_importances_)))
```

Decision trees naturally produce **feature importance scores** by tallying the total impurity reduction each feature contributes across all splits. In materials science, this immediately answers questions such as: which mechanical parameters best discriminate between failure modes? In genomics: which gene-expression features best predict cell fate? These scores are a useful starting point for feature understanding, though they exhibit a known bias toward high-cardinality features.

---

## 5. Random Forests and Ensemble Learning — The Wisdom of Crowds

A single decision tree is intuitive but prone to overfitting. Random forests address this by combining many trees, embodying a simple yet profound principle: **an ensemble of weak learners consistently outperforms a single strong learner**. Understanding random forests requires first grasping one of machine learning's central conceptual tensions: the bias-variance tradeoff.

The **bias-variance tradeoff** states that a learner's expected generalization error can be decomposed into bias (systematic deviation of the model's assumptions from the true pattern), variance (sensitivity of the model to random fluctuations in training data), and irreducible noise. Decision trees suffer from high variance: on the same problem, different training samples yield structurally different trees. Ensemble methods exploit a key statistical fact: averaging predictions from multiple high-variance, uncorrelated models dramatically reduces variance while leaving bias approximately unchanged. This is the core insight behind **Bagging (Bootstrap Aggregating)**.

Random forests add two layers of randomization to maximize the independence (and thus decorrelation) of individual trees:

The first layer is **bootstrap sampling**: each of the T trees is trained on a random sample drawn with replacement from the training set. Approximately 63.2% of samples appear in each bootstrap sample; the remaining ~36.8% — the **out-of-bag (OOB) samples** — can be used to estimate generalization error without requiring a separate validation set.

The second layer is **feature randomization**: at each split node, rather than searching all d features for the optimal split, the algorithm randomly selects \(m \approx \sqrt{d}\) features and considers only those. This further decorrelates individual trees, amplifying the variance-reduction benefit of averaging.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,      # Number of trees
    min_samples_leaf=2,    # Minimum samples at a leaf node
    max_features='sqrt',   # Feature subset size per split: sqrt(d)
    oob_score=True,        # Estimate generalization with OOB samples
    n_jobs=-1,             # Parallelize across all CPU cores
    random_state=42
)
rf.fit(X_train, y_train)

print(f"OOB generalization estimate: {rf.oob_score_:.4f}")
print(f"Test accuracy:               {accuracy_score(y_test, rf.predict(X_test)):.4f}")

feature_names = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid']
print("Feature importances:", dict(zip(feature_names, rf.feature_importances_)))
```

**Gradient boosting** represents an alternative ensemble philosophy. Rather than training trees in parallel and averaging, it trains trees **sequentially**: each new tree is fit specifically to the residuals of all previous trees, gradually correcting accumulated errors. This corresponds to performing gradient descent in function space. Gradient boosting typically achieves lower bias than random forests, and modern implementations — XGBoost, LightGBM, CatBoost — exploit histogram-based splits and sparsity awareness to scale to very large datasets.

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,  # Shrinkage: smaller rate + more trees is often better
    max_depth=3,         # Shallow "stumps" are conventional for boosting
    subsample=0.8,       # Stochastic gradient boosting
    random_state=42
)
gb.fit(X_train, y_train)
print(f"Gradient Boosting Test accuracy: {accuracy_score(y_test, gb.predict(X_test)):.4f}")
```

Practical recommendation: random forests are the most reliably "out-of-the-box" classifier available. They are insensitive to feature scaling, handle mixed feature types, tolerate modest missing data, and estimate generalization performance via OOB error — eliminating the need for a separate validation set. When uncertain which model to use, start with random forests. If further accuracy is needed, move to LightGBM or XGBoost.

---

## 6. k-Nearest Neighbors — The Laziest Learner

k-Nearest Neighbors (k-NN) is the most intuitively transparent algorithm in machine learning and the canonical example of **lazy learning**. Its premise reflects an everyday heuristic: **you can infer someone's characteristics by looking at who they are close to**. In feature space, k-NN locates the k training samples nearest to a test point and assigns the majority class label among those neighbors. There is no training phase at all — the algorithm simply memorizes the entire training set and defers all computation to prediction time.

This "laziness" is both an advantage and a liability. On the positive side, new data can be added without any retraining. On the negative side, every prediction requires computing the distance to all N training points: O(Nd) complexity, which becomes prohibitive for large datasets. Tree-based data structures (KD-Tree, Ball-Tree) can accelerate this to approximately \(O(\log N)\), though their benefit degrades in high dimensions.

The choice of distance metric profoundly affects k-NN's behavior. The most common options are the **Euclidean (L2) distance**:

$$d(\mathbf{x}, \mathbf{x}') = \sqrt{\sum_{j=1}^d (x_j - x_j')^2}$$

and the **Manhattan (L1) distance**:

$$d(\mathbf{x}, \mathbf{x}') = \sum_{j=1}^d |x_j - x_j'|$$

Euclidean distance is more sensitive to large-scale features; Manhattan distance is often more stable in high dimensions due to its reduced sensitivity to outliers. **Feature standardization is mandatory for k-NN**: if one feature ranges over millimeters (1–100) and another over pascals (\(10^6 - 10^9\)), Euclidean distance is entirely dominated by the latter.

The choice of k governs model complexity: k=1 is maximally local and highly prone to overfitting; k=N always predicts the majority class and underfits. Optimal k is typically found via cross-validation.

A deeper theoretical concern is the **curse of dimensionality**. As dimensionality d grows, all pairwise distances tend to equalize — the contrast between "near" and "far" erodes. Intuitively, in 100-dimensional space, the ratio of the nearest-neighbor distance to the farthest-neighbor distance approaches 1, rendering the neighborhood concept meaningless. This implies that k-NN performs poorly in raw high-dimensional feature spaces (raw pixels, gene expression vectors) and generally requires prior dimensionality reduction (PCA, UMAP) before use.

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Find optimal k by cross-validation
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

# Distance-weighted voting: closer neighbors contribute more
knn = KNeighborsClassifier(n_neighbors=optimal_k, weights='distance',
                           algorithm='auto', metric='euclidean')
knn.fit(X_train, y_train)
print(f"Test accuracy: {accuracy_score(y_test, knn.predict(X_test)):.4f}")
```

Setting `weights='distance'` makes each neighbor's vote inversely proportional to its distance from the test point, typically improving performance near class boundaries compared to uniform weighting.

---

## 7. Naive Bayes — The Minimalist Philosophy of Probabilistic Inference

Naive Bayes is a family of probabilistic classifiers grounded in Bayes' theorem. Celebrated for its extreme simplicity and training speed, it has a long history in text classification (spam detection) and biological sequence analysis. Understanding it requires first grasping the conceptual core of Bayes' theorem: how to **systematically update beliefs in light of observed evidence**.

**Bayes' theorem** states:

$$P(y|\mathbf{x}) = \frac{P(\mathbf{x}|y) \cdot P(y)}{P(\mathbf{x})}$$

Here \(P(y)\) is the **prior** (the probability of each class before observing the sample), \(P(\mathbf{x}|y)\) is the **likelihood** (the probability of observing feature vector \(\mathbf{x}\) given class y), \(P(y|\mathbf{x})\) is the **posterior** — what we actually want: the probability of class y given the observed features — and \(P(\mathbf{x})\) is a normalizing constant that is identical across all classes and can be safely ignored during classification.

The classification decision follows the MAP (maximum a posteriori) rule:

$$\hat{y} = \arg\max_y P(\mathbf{x}|y) \cdot P(y)$$

The central challenge is that \(P(\mathbf{x}|y) = P(x_1, x_2, \ldots, x_d | y)\) is a d-dimensional joint distribution, which is essentially impossible to estimate from finite data when d is large. The **naive assumption** resolves this: given the class label y, all features are assumed to be **conditionally independent**:

$$P(\mathbf{x}|y) = \prod_{j=1}^d P(x_j|y)$$

This assumption almost never holds in reality — features are correlated. Yet in practice the model often performs surprisingly well. The reason: even if the assumption is wrong, it is wrong in a consistent direction across all classes. The relative ordering of posterior probabilities — and thus the final classification — can remain correct even when the absolute probability values are distorted.

Under this assumption, only univariate distributions \(P(x_j|y)\) need to be estimated — one per feature per class. For continuous features, Gaussian Naive Bayes assumes:

$$P(x_j|y=k) = \frac{1}{\sqrt{2\pi\sigma_{kj}^2}} \exp\left(-\frac{(x_j - \mu_{kj})^2}{2\sigma_{kj}^2}\right)$$

Training requires only estimating the per-class per-feature mean \(\mu_{kj}\) and variance \(\sigma_{kj}^2\) from the data — a closed-form operation requiring zero iterative optimization.

```python
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)

print(f"Test accuracy: {accuracy_score(y_test, gnb.predict(X_test)):.4f}")

# Inspect learned parameters
print("Class priors P(y):", gnb.class_prior_)
# theta_: per-class per-feature means, shape (n_classes, n_features)
print("Feature means per class:\n", gnb.theta_)
```

Naive Bayes' strengths are training speed (\(O(Nd)\)), well-calibrated probabilistic outputs, graceful handling of missing features (simply skip the missing term in the product), and stability on small datasets. Specialized variants exist for different data types: `MultinomialNB` for word-count features (the standard in text classification), `BernoulliNB` for binary presence/absence features (e.g., whether a gene is expressed or not). Its main weakness is that strong feature correlations degrade performance — when the naive independence assumption is severely violated, SVMs and random forests will typically outperform it.

---

## 8. Evaluation Metrics — Accuracy Is Just the Beginning

Once a classifier is trained, how should its performance be measured? Many beginners default to **accuracy** — the fraction of correctly classified samples. But accuracy is a dangerous oversimplification, especially under class imbalance. If 99% of a medical dataset consists of healthy subjects, a classifier that always predicts "healthy" achieves 99% accuracy while being completely useless for disease detection. Choosing the right evaluation metric is, fundamentally, an act of encoding what it means to be wrong in the specific context of your problem.

The foundation of all evaluation metrics is the **confusion matrix**. For binary classification:

| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actually Positive** | TP (True Positive) | FN (False Negative — missed) |
| **Actually Negative** | FP (False Positive — false alarm) | TN (True Negative) |

From these four counts, a coherent family of metrics emerges:

**Precision** measures the fraction of predicted positives that are genuinely positive:

$$\text{Precision} = \frac{TP}{TP+FP}$$

It answers: "Of all my reported positives, how many are real?" Precision matters most when false positives are costly — a cancer misdiagnosis leading to unnecessary surgery, or a material classified as defective triggering an expensive replacement.

**Recall** (also called Sensitivity or True Positive Rate) measures the fraction of actual positives that were detected:

$$\text{Recall} = \frac{TP}{TP+FN}$$

It answers: "Did I find all the real positives?" Recall matters most when false negatives are costly — a missed structural crack that leads to catastrophic failure, or a disease missed by a diagnostic screen.

**F1 score** is the harmonic mean of precision and recall, providing a single balanced metric:

$$F_1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**ROC curve and AUC** are obtained by varying the classification threshold (default 0.5) and plotting True Positive Rate (Recall) against False Positive Rate (\(FP/(FP+TN)\)). The AUC (Area Under the Curve) ranges from 0.5 (random guessing) to 1.0 (perfect classification) and is invariant to class imbalance — making it one of the most reliable summary statistics for binary classification.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    classification_report, roc_auc_score,
    RocCurveDisplay
)
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

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
y_prob_bc  = clf.predict_proba(X_te)[:, 1]

# Confusion matrix
ConfusionMatrixDisplay(
    confusion_matrix(y_te, y_pred_bc),
    display_labels=['Malignant', 'Benign']
).plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# Full multi-metric report
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

For multi-class problems, precision, recall, and F1 must be aggregated: **macro-averaging** treats all classes equally (more sensitive to minority classes), while **weighted averaging** weights each class by its sample count (biased toward majority classes). Always choose the aggregation scheme that reflects your actual scientific priorities.

Finally, **K-fold cross-validation** is the gold standard for estimating generalization performance. The dataset is partitioned into K folds; in each iteration one fold serves as the validation set while the rest form the training set, cycling K times and averaging the result. This is far more reliable than a single train-test split, particularly when data are limited — a condition that is endemic in experimental biology and materials science.

---

## 9. A Practical Model-Selection Guide — No Free Lunch

No classifier is optimal for every problem. This is formalized by the **No Free Lunch Theorem**: when averaged over all possible datasets, every algorithm has identical expected performance. In practice, model selection requires reasoning across several dimensions simultaneously — not defaulting to whichever algorithm won last year's Kaggle competition.

**Dataset size** is the first constraint. When N < 500, logistic regression, Naive Bayes, and SVMs with strong inductive biases are more reliable than data-hungry models. When N > 100,000, gradient boosting (XGBoost, LightGBM) and deep learning can realize their full potential, while SVMs become computationally impractical due to their \(O(N^2)\) to \(O(N^3)\) training complexity.

**Interpretability requirements** are the second constraint and are often non-negotiable in clinical, regulatory, and safety-critical engineering contexts. When you must explain a decision to a physician, structural engineer, or regulatory body, decision trees and logistic regression are the natural choices: the former produces explicit if-then rule chains; the latter provides signed, magnitude-ordered feature coefficients. Random forests and gradient boosting offer partial interpretability through feature importance scores; neural networks are essentially opaque without additional explainability tools (SHAP, LIME).

**Feature dimensionality** is the third constraint. For low-dimensional features (d < 20), k-NN, Naive Bayes, and decision trees work well. For moderate dimensionality (20 < d < 1000), SVM with RBF kernel and random forests are the workhorses. For high-dimensional sparse inputs (text, genomics, d > 1000), linear SVM (`LinearSVC`), L1-regularized logistic regression, and Multinomial Naive Bayes are preferred for their computational efficiency and implicit sparsity handling.

**Class imbalance** is pervasive in real-world scientific data and must be addressed independently of model choice. Nearly all scikit-learn classifiers support `class_weight='balanced'`, which automatically adjusts loss contributions inversely proportional to class frequency. Alternatively, SMOTE oversampling of the minority class at the data level can be effective.

| Model | Train Speed | Predict Speed | Interpretability | Needs Scaling | Small Data | High-Dim Sparse |
|---|---|---|---|---|---|---|
| Logistic Regression | Fast | Fast | High | Yes | ✓ | ✓ (L1) |
| SVM (RBF) | Medium–Slow | Medium | Low | Yes | ✓ | ✗ |
| Decision Tree | Fast | Fast | Highest | No | Medium | ✗ |
| Random Forest | Medium | Medium | Medium | No | Medium | Medium |
| Gradient Boosting | Slow | Medium | Medium | No | ✗ | Medium |
| k-NN | None (lazy) | Slow | Medium | Yes | ✓ | ✗ |
| Naive Bayes | Very Fast | Very Fast | Medium | No | ✓ | ✓ |

**Practical recommendation**: always begin with a simple baseline — logistic regression or random forest — to understand the intrinsic difficulty of the data and identify the most informative features. A carefully tuned random forest will satisfy the accuracy requirements of most structured scientific datasets while remaining far more interpretable than a neural network. Reserve deep learning for situations where data are abundant (N > 10,000), computational infrastructure is available, and classical methods have been rigorously shown to be insufficient.

---

## References

1. Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

2. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324

3. Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297. https://doi.org/10.1007/BF00994018

4. Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451

5. Cover, T. M., & Hart, P. E. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21–27. https://doi.org/10.1109/TIT.1967.1053964

6. Zhang, H. (2004). The optimality of naive Bayes. *Proceedings of the 17th International FLAIRS Conference*. American Association for Artificial Intelligence.

7. Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters*, 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010

8. Wolpert, D. H. (1996). The lack of a priori distinctions between learning algorithms. *Neural Computation*, 8(7), 1341–1390. https://doi.org/10.1162/neco.1996.8.7.1341