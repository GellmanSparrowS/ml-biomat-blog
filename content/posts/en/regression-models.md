---
title: "Common Regression Models in Machine Learning"
date: "2026-07-03"
category: "machine-learning"
tags: ["regression","machine-learning","scikit-learn","gradient-boosting"]
lang: "en"
slug: "regression-models-ml"
description: "A systematic guide to linear regression, Ridge, Lasso, SVR, trees and boosting."
---


## 1. The Nature of Regression — From Numerical Prediction to Function Approximation

The most fundamental distinction between regression and classification lies in the nature of the output: classification predicts discrete category labels, whereas regression predicts continuous numerical values. This difference, while seemingly minor, profoundly shapes model design choices, loss function selection, and the interpretation of evaluation metrics. In biology, materials science, and structural mechanics, regression problems are essentially ubiquitous: predicting elastic modulus from material composition and processing parameters, estimating binding free energy from protein sequence features, inferring full-field stress distributions from a subset of finite-element outputs, or predicting residual fatigue life from sensor time-series data. Whether an accurate and generalizable regression model can be built largely determines the practical credibility of data-driven science — the aspiration to let computation substitute for experimentation.

Formally, a regression problem is defined as follows. Given a training dataset \(\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N\), where \(\mathbf{x}_i \in \mathbb{R}^d\) is the d-dimensional feature vector of the i-th sample and \(y_i \in \mathbb{R}\) is the corresponding continuous target value, the objective is to learn a function \(f: \mathbb{R}^d \rightarrow \mathbb{R}\) such that \(f(\mathbf{x})\) provides accurate numerical predictions for new, unseen samples. The specific form of \(f\) is determined by the chosen model — it may be a simple linear function, a polynomial, a piecewise constant function (decision tree), or a highly nonlinear ensemble model.

The central intuition behind regression is **function approximation**. Behind any real-world dataset lies some unknown true function \(f^*(\mathbf{x})\), but we can only observe noise-corrupted samples of it: \(y_i = f^*(\mathbf{x}_i) + \epsilon_i\), where \(\epsilon_i\) is zero-mean random noise. The regression model's task is to estimate \(f^*\) from a finite collection of noisy observations. Different regression algorithms are, fundamentally, different estimation strategies: they impose different prior assumptions on \(f^*\) (linear, piecewise-linear, smooth...), make different distributional assumptions about the noise (Gaussian, Laplacian...), and use different optimization methods to find the best fit.

A distinctive challenge in regression is the **balance between underfitting and overfitting**, which is more visually tangible here than in classification. Underfitting means the model is too simple to capture the patterns in the data (fitting a straight line through an obviously nonlinear scatter plot); overfitting means the model is so complex that it perfectly memorizes the training noise, failing catastrophically on new data. Plotting training error and validation error as a function of model complexity — the learning curve — is the standard diagnostic for both pathologies, and fluency with this diagnostic is a basic skill in data science practice.

The following data preparation and evaluation template is used throughout this article:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

np.random.seed(42)

# Synthetic regression dataset: cubic trend + Gaussian noise
N = 300
X_raw = np.linspace(-3, 3, N).reshape(-1, 1)
y_raw = (0.5 * X_raw.ravel()**3
         - X_raw.ravel()**2
         + 2 * X_raw.ravel()
         + np.random.randn(N) * 1.5)

X_train, X_test, y_train, y_test = train_test_split(
    X_raw, y_raw, test_size=0.2, random_state=42
)

# Standardize: critical for regularized and kernel-based models
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)   # Apply training statistics only

def evaluate(name, y_true, y_pred):
    """Compact multi-metric regression report."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)
    print(f"{name:35s} | RMSE={rmse:.3f}  MAE={mae:.3f}  R²={r2:.4f}")
```

---

## 2. Linear Regression — The Most Concise Baseline

Linear regression is both the starting point for all regression models and one of the most widely used statistical tools in scientific research. Its assumption is extremely simple: the target value is a linear combination of input features plus random noise. This assumption provides a good approximation in many scientific contexts — Young's modulus versus composition in materials science, dose-response relationships in biology, and the stress-strain relationship during the linear-elastic phase in structural mechanics. Understanding linear regression is not only a prerequisite for learning more complex models; the derivation itself reveals the most fundamental concepts of supervised learning: the loss function, least-squares estimation, and their geometric interpretation.

Start with the intuition. Suppose you have stiffness measurements for a set of springs (cross-sectional area x, stiffness y), and you want to find the line \(\hat{y} = w_1 x + w_0\) that best "passes through" the scatter of points. "Best" needs to be quantified. The most natural idea is to minimize the total vertical distance from each point to the line. However, summing signed distances allows positive and negative errors to cancel, so instead we sum the squared distances — this is the **Ordinary Least Squares (OLS)** criterion. Generalizing to d-dimensional features, with design matrix \(\mathbf{X} \in \mathbb{R}^{N \times (d+1)}\) (each row is a sample's feature vector, with a leading column of ones for the intercept), target vector \(\mathbf{y} \in \mathbb{R}^N\), and parameter vector \(\mathbf{w} \in \mathbb{R}^{d+1}\), the loss is:

$$\mathcal{L}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2 = (\mathbf{y} - \mathbf{X}\mathbf{w})^T(\mathbf{y} - \mathbf{X}\mathbf{w})$$

Setting the gradient with respect to \(\mathbf{w}\) to zero yields the **Normal Equation**:

$$\mathbf{X}^T\mathbf{X}\mathbf{w} = \mathbf{X}^T\mathbf{y}$$

When \(\mathbf{X}^T\mathbf{X}\) is invertible, the closed-form solution is:

$$\hat{\mathbf{w}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

This is a closed-form solution requiring no iteration, with computational complexity \(O(Nd^2 + d^3)\). When d is large (e.g., \(d > 10^4\)), matrix inversion becomes prohibitively slow and stochastic gradient descent (SGD) is preferred.

Linear regression has several key statistical assumptions under which the OLS estimator is the Best Linear Unbiased Estimator (BLUE, per the Gauss-Markov theorem): the error terms have zero mean \(\mathbb{E}[\epsilon_i]=0\); they are homoscedastic, meaning \(\text{Var}(\epsilon_i) = \sigma^2\) is constant; they are uncorrelated; and they are independent of the features. These assumptions can be systematically checked through residual diagnostics: a scatter plot of residuals against fitted values should be structureless (any visible curvature indicates missing nonlinearity); a Q-Q plot checks normality; a scale-location plot checks homoscedasticity.

The coefficient \(\hat{w}_j\) has a direct interpretation: holding all other features constant, a one-unit increase in feature j is associated with an average change of \(\hat{w}_j\) in the target. This marginal effect interpretation is widely used in biostatistics and materials genomics. One important caveat is multicollinearity: when two features are highly correlated, their coefficient estimates become highly unstable (large variance), making individual coefficients difficult to interpret and requiring regularization.

```python
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(X_train_sc, y_train)

y_pred_lr = lr.predict(X_test_sc)
evaluate("Linear Regression", y_test, y_pred_lr)
print(f"Coefficients : {lr.coef_}")
print(f"Intercept    : {lr.intercept_:.4f}")

# Residual diagnostics
residuals = y_test - y_pred_lr
plt.figure(figsize=(8, 4))
plt.scatter(y_pred_lr, residuals, alpha=0.6, edgecolors='k', linewidths=0.4)
plt.axhline(0, color='red', linewidth=1.2, linestyle='--')
plt.xlabel("Predicted values")
plt.ylabel("Residuals  (Actual − Predicted)")
plt.title("Residual Plot — Linear Regression")
plt.tight_layout()
plt.show()
```

---

## 3. Ridge and Lasso — The Art of Regularization

When the number of features approaches or exceeds the sample count (\(d \approx N\) or \(d > N\)), or when features are highly correlated, ordinary linear regression encounters a severe numerical problem: \(\mathbf{X}^T\mathbf{X}\) becomes nearly singular, coefficient estimate variances explode, and predictions become wildly unstable. This is the classic recipe for overfitting. Regularization addresses this by adding a penalty term on coefficient magnitude to the loss function, forcing the model to "not be too greedy" — accepting a slight increase in bias in exchange for a substantial reduction in variance. From a Bayesian perspective, regularization is equivalent to imposing a prior distribution on the parameters: L2 regularization corresponds to a Gaussian prior, and L1 regularization corresponds to a Laplacian prior. Understanding these two forms of regularization is equivalent to understanding the bias-variance tradeoff in the context of linear models.

**Ridge Regression (L2 regularization)** adds the squared L2 norm of the coefficients to the loss:

$$\mathcal{L}_{\text{Ridge}}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2 + \lambda \|\mathbf{w}\|^2$$

The hyperparameter \(\lambda \geq 0\) controls regularization strength: \(\lambda = 0\) reduces to ordinary linear regression; \(\lambda \rightarrow \infty\) drives all coefficients toward zero. Ridge retains a closed-form solution:

$$\hat{\mathbf{w}}_{\text{Ridge}} = (\mathbf{X}^T\mathbf{X} + \lambda\mathbf{I})^{-1}\mathbf{X}^T\mathbf{y}$$

Adding \(\lambda\mathbf{I}\) makes the matrix strictly positive definite, resolving the singularity problem entirely — this is the origin of the name "ridge," as \(\lambda\mathbf{I}\) adds a "ridge" to the diagonal. Geometrically, Ridge confines the coefficients to an L2 ball (a sphere), shrinking all coefficients toward zero but never exactly to zero: all features are retained, but their contributions are uniformly dampened.

**Lasso (Least Absolute Shrinkage and Selection Operator, L1 regularization)** replaces the penalty with the L1 norm:

$$\mathcal{L}_{\text{Lasso}}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2 + \lambda \|\mathbf{w}\|_1 = \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2 + \lambda \sum_{j=1}^d |w_j|$$

The L1 constraint region is a diamond (a cross-polytope in higher dimensions), with corners lying exactly on the coordinate axes. Because the loss function's minimum tends to land on these corners — where some coordinates are exactly zero — Lasso performs implicit **feature selection**: unimportant feature coefficients are pushed to precisely zero rather than just made small. This sparsity property is extremely valuable for high-dimensional data (genomics, metabolomics, where d can reach tens of thousands), as the data effectively tells you which features genuinely matter. Lasso has no closed-form solution (the L1 norm is non-differentiable at the origin) and is typically solved by coordinate descent.

**Elastic Net** combines both penalties:

$$\mathcal{L}_{\text{EN}}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2 + \lambda_1 \|\mathbf{w}\|_1 + \lambda_2 \|\mathbf{w}\|^2$$

Elastic Net inherits sparsity from Lasso and numerical stability from Ridge. When features are strongly correlated in groups, Lasso tends to arbitrarily select just one feature from the group, while Elastic Net tends to keep or discard entire groups together — a more physically interpretable behavior when multiple descriptors collectively encode the same underlying physical mechanism.

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet, RidgeCV
import numpy as np

# Ridge: L2 — numerically stable, retains all features
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_sc, y_train)
evaluate("Ridge (alpha=1.0)", y_test, ridge.predict(X_test_sc))

# Lasso: L1 — sparse feature selection
lasso = Lasso(alpha=0.1, max_iter=10000)
lasso.fit(X_train_sc, y_train)
evaluate("Lasso (alpha=0.1)", y_test, lasso.predict(X_test_sc))
n_nonzero = np.sum(lasso.coef_ != 0)
print(f"  Lasso non-zero coefficients: {n_nonzero} / {len(lasso.coef_)}")

# Elastic Net: L1 + L2 hybrid
en = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000)
en.fit(X_train_sc, y_train)
evaluate("Elastic Net", y_test, en.predict(X_test_sc))

# Cross-validated alpha selection — mandatory in practice
alphas = np.logspace(-4, 3, 100)
ridge_cv = RidgeCV(alphas=alphas, cv=5, scoring='neg_mean_squared_error')
ridge_cv.fit(X_train_sc, y_train)
print(f"\nRidgeCV best alpha: {ridge_cv.alpha_:.5f}")
evaluate("Ridge (CV-tuned alpha)", y_test, ridge_cv.predict(X_test_sc))
```

Selecting \(\lambda\) (called `alpha` in scikit-learn) through cross-validation is not optional — it is the critical step that determines whether regularization helps or hurts. The regularization path plot, which shows how each feature's coefficient evolves as \(\lambda\) decreases from large to small, is a standard diagnostic tool for understanding the relative importance and correlation structure of features.

---

## 4. Polynomial Regression and Feature Engineering — Breaking the Linear Constraint

The assumption that target values are linear functions of features is too restrictive for many real-world problems. The stress-strain relationship enters a nonlinear regime at plasticity onset; enzyme-catalyzed reactions follow Michaelis-Menten kinetics; material fatigue life follows a power-law relationship with stress amplitude. These are all fundamentally nonlinear. Polynomial regression is the simplest way to introduce nonlinearity: generate polynomial combinations of the original features and feed them into an ordinary linear regression. This seemingly simple idea reveals a deep general principle: **feature engineering** — transforming and combining raw features to enhance the model's expressive power — is often more effective than switching to a more complex model, and is particularly impactful when sample sizes are limited.

For a single feature \(x\), the polynomial feature vector is \((1, x, x^2, \ldots, x^p)\), and the regression model becomes:

$$\hat{y} = w_0 + w_1 x + w_2 x^2 + \ldots + w_p x^p$$

This model is still **linear in its parameters** \(\mathbf{w}\), so all tools developed for linear regression — the normal equation, regularization, cross-validation — remain directly applicable. But with respect to the original input \(x\), the model is nonlinear and can fit curves. For d-dimensional features, `PolynomialFeatures` generates all terms up to the specified degree, including cross-terms like \(x_i x_j\), \(x_i^2 x_j\). With d features, degree-2 expansion generates \(\binom{d+2}{2}\) features and degree-3 generates \(\binom{d+3}{3}\) — the explosive growth in feature count makes regularization not just advisable but essential. In practice, polynomial regression is almost always paired with Ridge or Lasso.

The polynomial degree p is the critical hyperparameter. Too small yields underfitting; too large yields overfitting — high-degree polynomials oscillate violently between data points (the Runge phenomenon), especially near the boundaries of the input range. Comparing training and cross-validated error across different values of p identifies the bias-variance optimal degree, illustrating the universal methodology of hyperparameter tuning.

Feature engineering extends far beyond polynomials. In materials science, if elastic modulus is known to follow a power-law relationship with density, manually constructing \(\log(\rho)\) or \(1/d^2\) (inverse grain size) as features may be far more effective than a generic polynomial expansion. In biomechanics, if knee joint moment relates to angle sinusoidally, using \(\sin(\theta)\) and \(\cos(\theta)\) as features is more data-efficient and more interpretable than any polynomial. Injecting domain knowledge into feature design is the highest-leverage strategy for improving model performance under data-scarce conditions.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

# Systematically compare polynomial degrees
print(f"{'Degree':>7} | {'Test R²':>8} | {'CV RMSE':>10}")
print("-" * 35)
for degree in [1, 2, 3, 4, 5, 7]:
    pipe = Pipeline([
        ('poly',   PolynomialFeatures(degree=degree, include_bias=False)),
        ('scaler', StandardScaler()),
        ('ridge',  Ridge(alpha=1.0))
    ])
    pipe.fit(X_train, y_train)
    test_r2 = r2_score(y_test, pipe.predict(X_test))
    cv_mse  = cross_val_score(pipe, X_train, y_train,
                              cv=5, scoring='neg_mean_squared_error')
    cv_rmse = np.sqrt(-cv_mse.mean())
    print(f"{degree:>7d} | {test_r2:>8.4f} | {cv_rmse:>8.3f} ± {cv_mse.std():.3f}")

# Best pipeline: polynomial features + Ridge regularization
best_pipe = Pipeline([
    ('poly',   PolynomialFeatures(degree=3, include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge',  Ridge(alpha=0.5))
])
best_pipe.fit(X_train, y_train)
evaluate("Poly(3) + Ridge", y_test, best_pipe.predict(X_test))
```

Using a `Pipeline` to encapsulate the entire preprocessing-modeling chain has two critical benefits. First, it prevents **data leakage**: standardization parameters and polynomial features are estimated only on the training fold, with the validation fold exposed only to `transform` — the pipeline's `fit_transform` mechanism enforces this automatically. Second, it enables correct cross-validation: when `cross_val_score` is applied to an entire pipeline, all preprocessing steps are independently re-estimated in each fold, ensuring that no validation-set information leaks into training. Any preprocessing step should be included inside the pipeline — this is a non-negotiable standard in production-quality code.

---

## 5. Support Vector Regression — The ε-Insensitive Tube

Support Vector Regression (SVR) transfers the margin-maximization philosophy of SVMs to regression tasks, but with a fundamentally different objective: rather than finding the hyperplane that maximally separates classes, SVR seeks the widest possible **tube** (ε-tube) that encloses as many training points as possible, penalizing only those that fall outside it. This design introduces a concept absent from ordinary regression: the **ε-insensitive loss**.

The intuition is as follows. Suppose you are fitting a curve through scattered points and you believe the data contains a certain level of measurement noise. For predictions that deviate from the true value by less than ε, you consider the fit "good enough" and apply no penalty. Only when the deviation exceeds ε does the loss begin to accumulate, and it does so linearly — not quadratically as in least squares. This is like drawing a tolerance band of width \(2\varepsilon\) around the regression curve: training points inside the band are structurally irrelevant (analogous to non-support-vectors in classification); only the points outside the band — the "hard" examples — determine the model parameters.

Formally:

$$\min_{\mathbf{w}, b, \xi, \xi^*} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^N (\xi_i + \xi_i^*)$$

$$\text{s.t.} \quad y_i - (\mathbf{w}^T\mathbf{x}_i + b) \leq \varepsilon + \xi_i, \quad (\mathbf{w}^T\mathbf{x}_i + b) - y_i \leq \varepsilon + \xi_i^*, \quad \xi_i, \xi_i^* \geq 0$$

Slack variables \(\xi_i\) and \(\xi_i^*\) quantify the degree of violation above and below the tube, respectively; C controls the penalty for exceeding the tube. Identical to classification SVMs, the kernel trick applies directly: mapping inputs to a high-dimensional space via an RBF kernel and fitting a linear function there is equivalent to fitting a nonlinear function in the original space, without ever constructing the high-dimensional mapping explicitly.

SVR has three key hyperparameters: C (regularization strength), ε (tube half-width — larger ε means a smoother function with more points "inside"), and γ (RBF kernel bandwidth). This three-dimensional search space makes tuning more expensive than for most other models. SVR's key advantage is **robustness to outliers**: the ε-insensitive loss grows only linearly beyond the tube boundary, in stark contrast to least-squares' quadratic penalty, which can be dominated by even a handful of extreme observations. When data contains occasional anomalous measurements (sensor faults, experimental errors), SVR is often substantially more stable than ordinary least squares.

```python
from sklearn.svm import SVR, LinearSVR
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C':       [0.1, 1, 10, 100],
    'epsilon': [0.01, 0.1, 0.5, 1.0],
    'gamma':   ['scale', 'auto', 0.01, 0.1]
}
gs_svr = GridSearchCV(
    SVR(kernel='rbf'), param_grid,
    cv=5, scoring='neg_mean_squared_error', n_jobs=-1
)
gs_svr.fit(X_train_sc, y_train)

print(f"Best SVR params: {gs_svr.best_params_}")
evaluate("SVR (RBF, grid-tuned)", y_test, gs_svr.predict(X_test_sc))

# LinearSVR: scales to large N
lin_svr = LinearSVR(C=1.0, epsilon=0.1, max_iter=10000)
lin_svr.fit(X_train_sc, y_train)
evaluate("Linear SVR", y_test, lin_svr.predict(X_test_sc))
```

SVR's primary limitation mirrors that of classification SVMs: training complexity approaches \(O(N^2)\) to \(O(N^3)\), making it impractical for datasets larger than roughly 50,000 samples. When data are abundant, gradient boosting models (discussed next) are a far more scalable alternative.

---

## 6. Decision Tree and Random Forest Regression — Piecewise Approximation to Ensemble Averaging

Decision trees are not limited to classification — they perform regression just as naturally. A Decision Tree Regressor recursively partitions the feature space into rectangular regions, assigning each leaf node the mean target value of all training samples within that region. The model is therefore a **piecewise constant function** approximator: finer partitioning (deeper tree) produces a more staircase-like function that fits training data more closely, but generalizes less well to new inputs. The overfitting behavior of decision tree regression is particularly transparent: an unconstrained deep tree achieves R² = 1 on the training set but may achieve R² < 0 on the test set.

The splitting criterion minimizes a weighted sum of **mean squared error (MSE)** across child nodes:

$$\min_{j,\,\tau} \left[\frac{|t_L|}{|t|} \text{MSE}(t_L) + \frac{|t_R|}{|t|} \text{MSE}(t_R)\right]$$

where \(\text{MSE}(t) = \frac{1}{|t|}\sum_{i \in t}(y_i - \bar{y}_t)^2\) and \(\bar{y}_t\) is the mean target value at node t. The search is performed over all features j and all candidate thresholds τ.

**Random Forest Regression** resolves the high variance of individual trees using the same Bagging + feature randomization strategy as in classification, but aggregation switches from majority voting to **mean averaging**: the final prediction is the average of all T trees' individual predictions. When individual tree errors are approximately uncorrelated, averaging reduces the variance by approximately a factor of T, while leaving the bias nearly unchanged. Random forest regression also enables a practically valuable form of **predictive uncertainty quantification**: by collecting all T individual tree predictions for a given test point, one can compute a mean ± standard deviation, attaching an uncertainty estimate to each prediction. In materials property prediction, "elastic modulus = 210 GPa ± 5 GPa" is far more informative than a bare point estimate — it directly guides experimental prioritization and engineering safety margins.

A fundamental limitation of random forest regression must be stated clearly: **poor extrapolation**. Because every prediction is a weighted average of training set target values, the model "plateaus" for inputs outside the training set's range, returning approximately the boundary value rather than extrapolating the true trend. This is not a tunable limitation — it is structural. When predicting material properties outside the observed composition or processing space, or structural responses at loads exceeding the training range, tree-based models will give confidently wrong answers. In such contexts, one should revert to parametric models (linear, polynomial) or consider physics-informed neural networks with appropriate inductive biases.

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

# Decision tree: depth controls the bias-variance tradeoff
print(f"{'max_depth':>12} | {'Train R²':>9} | {'Test R²':>8}")
for depth in [2, 4, 6, 10, None]:
    dt = DecisionTreeRegressor(max_depth=depth, min_samples_leaf=5, random_state=42)
    dt.fit(X_train, y_train)
    tr2 = r2_score(y_train, dt.predict(X_train))
    te2 = r2_score(y_test,  dt.predict(X_test))
    print(f"{str(depth):>12s} | {tr2:>9.4f} | {te2:>8.4f}")

# Random forest regression
rf_reg = RandomForestRegressor(
    n_estimators=300,
    min_samples_leaf=3,
    max_features=1.0,       # Use 'sqrt' for high-dimensional data
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
rf_reg.fit(X_train, y_train)
evaluate("Random Forest Regressor", y_test, rf_reg.predict(X_test))
print(f"OOB R²: {rf_reg.oob_score_:.4f}")

# Predictive uncertainty via distribution across trees
tree_preds = np.array([t.predict(X_test) for t in rf_reg.estimators_])
pred_mean  = tree_preds.mean(axis=0)
pred_std   = tree_preds.std(axis=0)
print(f"Mean predictive uncertainty (std): {pred_std.mean():.4f}")
```

---

## 7. Gradient Boosting Regression — XGBoost and LightGBM

Gradient boosting regression is currently among the strongest algorithms for structured-data regression tasks and is the predominant winning solution in data science competitions involving tabular data. The core idea is: **sequentially accumulate a series of weak learners (shallow decision trees), each one fitting the residuals of all previous trees, gradually approximating the target function**. Unlike random forests — which train trees in parallel and average their outputs — gradient boosting trains trees serially, with each new tree specifically targeting whatever the current ensemble is getting wrong. This is equivalent to performing gradient descent in function space, hence the name.

The simplest case provides the clearest intuition. For MSE loss, the first tree \(T_1\) fits the raw targets \(\mathbf{y}\), producing \(\hat{F}_1(\mathbf{x})\); the residuals \(r_1 = \mathbf{y} - \hat{F}_1\) are computed; the second tree \(T_2\) fits those residuals; the updated ensemble prediction is \(\hat{F}_2 = \hat{F}_1 + \eta T_2\), where \(\eta\) is the learning rate (shrinkage). The m-th tree fits the residuals of all preceding trees:

$$\hat{F}_m(\mathbf{x}) = \hat{F}_{m-1}(\mathbf{x}) + \eta \cdot T_m(\mathbf{x})$$

For any differentiable loss function \(\mathcal{L}(y, \hat{y})\), "residuals" generalize to the **negative gradient (pseudo-residuals)** of the loss with respect to the current prediction:

$$r_{im} = -\left[\frac{\partial \mathcal{L}(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)}\right]_{F=\hat{F}_{m-1}}$$

This generalization allows gradient boosting to accommodate different loss functions: MSE corresponds to ordinary residuals; MAE corresponds to the sign of the residual (making the model robust to outliers); quantile loss enables **quantile regression** — directly predicting prediction intervals (e.g., the 10th and 90th percentile) rather than point estimates — a feature of direct relevance to reliability analysis in structural engineering.

**XGBoost** improves upon vanilla gradient boosting by incorporating second-order gradient information (Taylor expansion to second order, exploiting the curvature of the loss landscape for faster convergence), tree structure regularization (penalizing the number of leaf nodes and the magnitude of leaf weights), column subsampling (per-tree feature randomization analogous to random forests), and a parallelized node-splitting algorithm. **LightGBM** further introduces histogram binning (discretizing continuous features into histograms, dramatically reducing the complexity of finding optimal splits and reducing memory consumption several-fold) and Gradient-based One-Side Sampling (GOSS, retaining samples with large gradients while subsampling those with small gradients). LightGBM is typically several times faster than XGBoost on large datasets and is the most commonly deployed gradient boosting implementation in industry today.

```python
from sklearn.ensemble import GradientBoostingRegressor

gb_reg = GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.8,
    min_samples_leaf=5,
    validation_fraction=0.1,
    n_iter_no_change=30,    # Early stopping
    random_state=42
)
gb_reg.fit(X_train, y_train)
evaluate("Gradient Boosting (sklearn)", y_test, gb_reg.predict(X_test))
print(f"Trees used (early stopping): {gb_reg.n_estimators_}")

# XGBoost
try:
    import xgboost as xgb
    xgb_reg = xgb.XGBRegressor(
        n_estimators=500, learning_rate=0.05, max_depth=4,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        early_stopping_rounds=30, eval_metric='rmse',
        random_state=42, verbosity=0
    )
    xgb_reg.fit(X_train, y_train,
                eval_set=[(X_test, y_test)], verbose=False)
    evaluate("XGBoost", y_test, xgb_reg.predict(X_test))
except ImportError:
    print("XGBoost not installed — run: pip install xgboost")

# LightGBM
try:
    import lightgbm as lgb
    lgb_reg = lgb.LGBMRegressor(
        n_estimators=500, learning_rate=0.05, num_leaves=31,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        random_state=42, verbose=-1
    )
    lgb_reg.fit(X_train, y_train,
                eval_set=[(X_test, y_test)],
                callbacks=[lgb.early_stopping(30, verbose=False)])
    evaluate("LightGBM", y_test, lgb_reg.predict(X_test))
except ImportError:
    print("LightGBM not installed — run: pip install lightgbm")

# Quantile regression: predict 10th and 90th percentile for uncertainty bounds
try:
    import xgboost as xgb
    q10 = xgb.XGBRegressor(objective='reg:quantileerror', quantile_alpha=0.10,
                            n_estimators=300, learning_rate=0.05, verbosity=0)
    q90 = xgb.XGBRegressor(objective='reg:quantileerror', quantile_alpha=0.90,
                            n_estimators=300, learning_rate=0.05, verbosity=0)
    q10.fit(X_train, y_train); q90.fit(X_train, y_train)
    coverage = np.mean((y_test >= q10.predict(X_test)) &
                       (y_test <= q90.predict(X_test)))
    print(f"80% prediction interval empirical coverage: {coverage:.3f} (ideal ≈ 0.80)")
except Exception:
    pass
```

Key gradient boosting tuning principles: smaller `learning_rate` paired with more trees consistently yields better generalization (0.01–0.1 is the standard range); `max_depth` of 3–6 is typical for regression; `subsample` and `colsample_bytree` introduce stochasticity that acts similarly to dropout; `early_stopping_rounds` is the most effective single guard against overfitting and should always be enabled in practice.

---

## 8. Regression Evaluation Metrics — Choosing Between MSE, MAE, and R²

After training a regression model, how do we accurately characterize its performance? Regression evaluation is subtler than classification: different error metrics embed different implicit assumptions about what constitutes "good prediction," and choosing the wrong metric can lead to seriously misleading conclusions. Reporting multiple metrics simultaneously, supported by diagnostic plots, is responsible scientific practice.

**Mean Squared Error (MSE)** is the classical regression loss:

$$\text{MSE} = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2$$

Root Mean Squared Error (RMSE) is its square root, which shares the target variable's units and is more interpretable as a typical error magnitude. Because MSE applies a quadratic penalty to large errors, it is highly sensitive to outliers — a sample with error 10 contributes 100 times as much MSE as one with error 1. In materials property prediction, if most samples have errors within 1 MPa but two or three extreme cases (near phase-transition boundaries, for instance) carry errors of 20 MPa, the reported RMSE will be dominated by those few points and will not accurately represent model performance on the bulk of the data.

**Mean Absolute Error (MAE)**:

$$\text{MAE} = \frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i|$$

MAE penalizes all errors linearly, making it far less sensitive to outliers than MSE. When unavoidable anomalous measurements exist in the dataset, MAE better represents model performance on the "typical" samples. Theoretically, minimizing MAE is equivalent to predicting the conditional median rather than the conditional mean — useful when the target distribution is skewed.

**Coefficient of Determination (\(R^2\))**:

$$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2} = 1 - \frac{\text{SS}_\text{res}}{\text{SS}_\text{tot}}$$

\(R^2\) measures the fraction of total variance in the target that the model explains. \(R^2 = 1\) is perfect prediction; \(R^2 = 0\) means the model is no better than always predicting the mean (the zero-skill baseline); \(R^2 < 0\) is a strong alarm signal — the model is worse than the trivial baseline. The greatest practical advantage of \(R^2\) is that it is **dimensionless**: it can be compared across datasets with different target units, whereas MSE and MAE are unit-dependent and cannot be meaningfully compared across tasks with different physical quantities. One important caveat: \(R^2\) on the training set increases monotonically with model complexity and must never be used for model selection — only its value on a held-out test set or via cross-validation is meaningful.

**Mean Absolute Percentage Error (MAPE)** provides a relative error perspective:

$$\text{MAPE} = \frac{100\%}{N}\sum_{i=1}^N \left|\frac{y_i - \hat{y}_i}{y_i}\right|$$

It is intuitive for communication (e.g., "predictions are within 5% on average") but diverges when target values approach zero.

```python
def comprehensive_eval(name, y_true, y_pred):
    """Compute and display all standard regression metrics."""
    mse  = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)
    mask = y_true != 0
    mape = np.mean(np.abs((y_true[mask]-y_pred[mask]) / y_true[mask])) * 100

    print(f"\n{'='*52}")
    print(f" {name}")
    print(f"{'='*52}")
    print(f"  MSE   = {mse:>10.4f}")
    print(f"  RMSE  = {rmse:>10.4f}")
    print(f"  MAE   = {mae:>10.4f}")
    print(f"  R²    = {r2:>10.4f}")
    print(f"  MAPE  = {mape:>9.2f}%")

def regression_diagnostics(y_true, y_pred, title=""):
    """Standard two-panel diagnostic plot."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Predicted vs. actual (ideal: points on y = x line)
    axes[0].scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidths=0.3, s=25)
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    axes[0].plot(lims, lims, 'r--', lw=1.5, label='Perfect prediction')
    axes[0].set_xlabel("Actual values")
    axes[0].set_ylabel("Predicted values")
    axes[0].set_title(f"Predicted vs Actual — {title}")
    axes[0].legend()

    # Residual distribution (should be symmetric around 0)
    residuals = y_true - y_pred
    axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    axes[1].axvline(0, color='red', lw=1.5, linestyle='--')
    axes[1].set_xlabel("Residual  (Actual − Predicted)")
    axes[1].set_ylabel("Count")
    axes[1].set_title(f"Residual Distribution — {title}")

    plt.tight_layout()
    plt.show()
```

Beyond numerical metrics, two diagnostic plots should always accompany regression model evaluation in a research report. The **predicted versus actual scatter plot** reveals whether errors are randomly distributed or whether there is a systematic bias structure (points that consistently fall on one side of the y = x diagonal, which indicates model misspecification). The **residual distribution histogram** should be centered at zero and roughly symmetric; right- or left-skewness indicates systematic bias; heteroscedastic spread (residuals whose variance grows with the predicted value) signals the need for target variable transformation (e.g., log-transform) or weighted regression.

---

## 9. A Practical Model-Selection Guide

As in classification, no regression algorithm is universally optimal. Different algorithms exhibit different adaptations to dataset size, feature structure, noise distribution, extrapolation requirements, and interpretability constraints. A principled selection strategy is more important than chasing the highest numerical benchmark.

**Dataset size** is the primary constraint. When N < 200, ordinary linear regression, Ridge, and Lasso are the most reliable choices: their low effective parameter count prevents overfitting, and their interpretable coefficients provide scientifically actionable insights. For intermediate sample sizes (200 < N < 10,000), SVR (RBF), random forests, and scikit-learn's gradient boosting are strong candidates. For large datasets (N > 10,000), LightGBM and XGBoost offer decisive speed advantages and typically achieve the highest accuracy; SVMs become computationally impractical at this scale.

**Interpretability** is often a non-negotiable hard requirement rather than a soft preference in materials science and biomechanics research, where the model output must be connected to a physical mechanism or reported to domain experts. Linear regression (including Ridge and Lasso) provides direct marginal effect estimates via coefficients; decision trees produce explicit if-then rule chains; random forests and gradient boosting offer feature importance scores and SHAP values that connect predictions to individual feature contributions. SHAP (SHapley Additive exPlanations) deserves special mention: it provides a theoretically grounded, model-agnostic method for attributing each prediction to each feature, and is increasingly expected in high-impact research publications that use machine learning.

**Extrapolation capability** is a dimension that receives insufficient attention in machine learning courses but is critical in science and engineering applications. Linear models extrapolate predictably along their linear trend. Polynomial models fit nonlinearity well within the training range but produce violently unstable extrapolations outside it. Tree-based models (random forests, gradient boosting) produce piecewise-constant predictions that plateau at the training boundary, giving confidently wrong but numerically flat answers for out-of-distribution inputs. When extrapolation is a core research requirement — predicting properties at conditions never observed in the training set — Gaussian process regression or physics-constrained neural networks with explicit uncertainty propagation are more appropriate choices.

**Noise and outlier sensitivity** should match the chosen loss function: for clean data, MSE-based models (standard least squares, gradient boosting with default MSE loss) perform best. For data with occasional severe outliers, MAE-based objectives, SVR (ε-insensitive loss), or Huber regression (`HuberRegressor`, which transitions smoothly from MSE near zero residuals to MAE for large residuals) are more robust.

| Model | Data Size | Nonlinearity | Extrapolation | Interpretability | Outlier Robustness | Needs Scaling |
|---|---|---|---|---|---|---|
| Linear Regression | Small–Large | Poor | Good (linear) | Highest | Poor | Yes |
| Ridge / Lasso | Small–Large | Poor | Good | High | Poor | Yes |
| Poly + Ridge | Small–Med | Medium | Poor (oscillates) | Medium | Poor | Yes |
| SVR (RBF) | Small–Med | Good | Medium | Low | Good | Yes |
| Decision Tree | Med–Large | Good | Poor (plateau) | High | Medium | No |
| Random Forest | Med–Large | Good | Poor (plateau) | Medium | Medium | No |
| Gradient Boosting | Med–Large | Best | Poor (plateau) | Medium | Adjustable | No |

**Practical workflow recommendation**: on a new regression problem, always begin with a simple baseline — linear regression or Ridge — to obtain an interpretable characterization of feature importance and to establish the floor on model complexity needed. Then inspect the residual plot: if clear nonlinear patterns are visible, introduce polynomial features or physically motivated transformations before switching to a black-box model. If sample size permits and nonlinearity is substantial, progress to random forest. Finally, with adequate data, compare random forest against gradient boosting via cross-validation and select the model with superior generalization. Throughout this process, SHAP value analysis is the bridge between predictive performance and scientific interpretation — treat it as a mandatory component of the workflow rather than an optional add-on.

---

## References

1. Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451

2. Tibshirani, R. (1996). Regression shrinkage and selection via the Lasso. *Journal of the Royal Statistical Society: Series B*, 58(1), 267–288. https://doi.org/10.1111/j.2517-6161.1996.tb02080.x

3. Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55–67. https://doi.org/10.1080/00401706.1970.10488634

4. Drucker, H., Burges, C. J. C., Kaufman, L., Smola, A., & Vapnik, V. (1997). Support vector regression machines. *Advances in Neural Information Processing Systems*, 9, 155–161.

5. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324

6. Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

7. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785

8. Ke, G., Meng, Q., Finley, T., et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30, 3146–3154.