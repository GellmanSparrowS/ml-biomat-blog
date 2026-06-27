---
title: "Machine Learning for Fiber Mechanics: From Data Preparation to Model Deployment"
date: "2026-06-26"
category: "machine-learning"
tags: ["machine-learning", "random-forest", "XGBoost", "fiber-materials", "mechanics"]
lang: "en"
slug: "ml-predict-fiber-mechanics"
description: "Step-by-step guide to predicting fiber biomaterial mechanical properties with ML: data cleaning, feature engineering, model selection, and uncertainty quantification."
---

## The Problem

Fiber biomaterial mechanics (Young's modulus, ultimate strength, toughness) depend on many factors: fiber diameter, orientation, crosslink density, water content, strain rate. Traditional regression handles linear relationships poorly, and fiber networks exhibit highly nonlinear behavior.

The special challenge in materials ML: **data is scarce**. You might have only 30-50 experimental samples.

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import cross_val_score
```

## Data Preparation

```python
data = pd.DataFrame({
    "fiber_diameter_nm": [45, 52, 48, 55, 50],
    "orientation_std_deg": [12, 22, 8, 18, 15],
    "crosslink_density_pct": [2.5, 1.8, 3.2, 2.0, 4.1],
    "youngs_modulus_GPa": [2.8, 1.9, 3.5, 2.3, 4.0],
})
```

## Model Selection for Small Data

| Model | Small-data advantage | Watch out for |
|------|---------------------|--------------|
| Random Forest | Insensitive to hyperparams, feature importance | Keep max_depth small |
| Gradient Boosting | High accuracy, handles nonlinearity | Easy to overfit, low lr needed |
| Gaussian Process | Built-in uncertainty, perfect for n<100 | O(n^3), avoid n>1000 |

```python
models = {
    "RF": RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42),
    "GB": GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42),
}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error")
    print(f"{name}: MAE = {-scores.mean():.3f} +/- {scores.std():.3f}")
```

## Uncertainty Quantification

```python
def predict_with_uncertainty(model, X, n_iter=100):
    predictions = np.zeros((n_iter, len(X)))
    for i in range(n_iter):
        idx = np.random.choice(len(X_train), len(X_train))
        model.fit(X_train[idx], y_train[idx])
        predictions[i] = model.predict(X)
    return np.mean(predictions, axis=0), np.std(predictions, axis=0)
```

## Advanced Directions

- **GNN**: model fiber networks as graphs
- **Transfer learning**: pretrain on simulations, fine-tune on experiments
- **Active learning**: let the model suggest the next experiment
- **PINNs**: inject constitutive equations as NN constraints

## Key Takeaways

1. Small data is not a blocker -- Bayesian methods and GPs are designed for it
2. Feature engineering matters more than model choice
3. Always report uncertainty -- reviewers will ask
4. Open-source your code and data for reproducibility

- Yang Y., Bai R., Gao W. et al. (2024). *Advanced Science*, 2413293.

## References
- Yang Y., Bai R., Gao W. et al. (2024). Optimizing biomimetic 3D fibrous networks via DRL. *Advanced Science*, 2413293.
- Ramprasad, R. et al. (2017). Machine learning in materials informatics. *npj Computational Materials*, 3, 54.


## Practical Considerations for ML in Materials

The curse of dimensionality hits materials ML particularly hard. Each experimental condition adds a dimension, and with limited data, models quickly overfit. Dimensionality reduction via principal component analysis or feature selection based on physical insight is essential before training.

Uncertainty quantification distinguishes good ML practice from wishful thinking. Bootstrapping provides a simple, non-parametric way to estimate prediction intervals. Train 100 models on bootstrapped samples of your data, and the distribution of predictions at each point gives a confidence interval. This approach requires no distributional assumptions and works with any model type.

Domain adaptation addresses the simulation-to-experiment gap. Models trained on abundant simulation data often fail on experimental measurements due to systematic differences. Domain adaptation techniques from transfer learning can align the feature distributions, allowing models trained on simulations to generalize to experimental data with minimal fine-tuning.

## References
- Butler, K.T. et al. (2018). Machine learning for molecular and materials science. *Nature*, 559, 547-555.
