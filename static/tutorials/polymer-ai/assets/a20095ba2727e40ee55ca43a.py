"""Chain size and extrapolation. Run with Python, NumPy and Matplotlib.

N is the number of freely jointed segments; there are N+1 equal beads.
All conformations are independent equilibrium samples, not a time trajectory.
Length unit: nm. Learning targets are Monte Carlo RMS end distances.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("chain_size_outputs")
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 14,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelsize": 14, "axes.titlesize": 15, "legend.fontsize": 11.5,
    "svg.hashsalt": "L05-chain-size", "savefig.facecolor": "#fffdf8"})
COLORS = ["#8a7865", "#cf6b45", "#237a68", "#293d65"]
TRAIN_N = [8, 12, 16, 32, 40, 64, 80, 112, 128]
TEST_N = [24, 48, 96]
LONG_N = [192, 256, 384, 512]
B_VALUES = np.array([0.5, 0.75, 1.0, 1.5, 2.0])
SAMPLE_COUNT = 6000


def chains(rng, n, count):
    """Isotropic 3D unit steps from normalized independent normal vectors."""
    steps = rng.normal(size=(count, n, 3))
    steps /= np.linalg.norm(steps, axis=2, keepdims=True)
    points = np.concatenate([np.zeros((count, 1, 3)),
                             np.cumsum(steps, axis=1)], axis=1)
    center = points.mean(axis=1, keepdims=True)
    r2 = np.sum(points[:, -1] ** 2, axis=1)
    rg2 = np.mean(np.sum((points-center)**2, axis=2), axis=1)
    return points, r2, rg2


def sample_data():
    rng = np.random.default_rng(505)
    rows, diagnostics, distributions = [], [], {}
    example = None
    for n in sorted(TRAIN_N + TEST_N + LONG_N):
        r2_parts, rg2_parts = [], []
        for batch in range(SAMPLE_COUNT // 250):
            points, r2, rg2 = chains(rng, n, 250)
            r2_parts.append(r2); rg2_parts.append(rg2)
            if n == 64 and batch == 0:
                example = points[:3].copy()
        r2, rg2 = np.concatenate(r2_parts), np.concatenate(rg2_parts)
        exact_rg2 = n * (n+2) / (6*(n+1))
        se_r2 = r2.std(ddof=1)/np.sqrt(SAMPLE_COUNT)
        se_rg2 = rg2.std(ddof=1)/np.sqrt(SAMPLE_COUNT)
        diagnostics.append({"N": n, "mean_R2": float(r2.mean()),
            "mean_Rg2": float(rg2.mean()), "se_R2": float(se_r2),
            "se_Rg2": float(se_rg2), "exact_Rg2": exact_rg2,
            "z_R2": float((r2.mean()-n)/se_r2),
            "z_Rg2": float((rg2.mean()-exact_rg2)/se_rg2)})
        split = "train" if n in TRAIN_N else "in_range" if n in TEST_N else "longer"
        for b in B_VALUES:
            # Scaling the SAME samples is intentional; the full N group stays together.
            rows.append({"N": n, "b_nm": float(b), "split": split,
                "rms_R_nm": float(np.sqrt(r2.mean())*b),
                "rms_Rg_nm": float(np.sqrt(rg2.mean())*b),
                "rms_R_se_nm": float(se_r2/(2*np.sqrt(r2.mean()))*b),
                "exact_R_nm": float(np.sqrt(n)*b)})
        if n == 64:
            distributions = {"R": np.sqrt(r2).tolist(), "Rg": np.sqrt(rg2).tolist()}
    return rows, diagnostics, example, distributions


def loss_and_grad(parameters, x, y):
    w1, c1, w2, c2 = parameters
    z = x @ w1 + c1
    h = np.maximum(z, 0.0)
    error = h @ w2 + c2 - y
    d_out = 2.0 * error / len(y)
    d_hidden = (d_out @ w2.T) * (z > 0)
    grads = [x.T @ d_hidden, d_hidden.sum(axis=0),
             h.T @ d_out, d_out.sum(axis=0)]
    return float(np.mean(error**2)), grads


def network(parameters, x):
    w1, c1, w2, c2 = parameters
    return (np.maximum(x @ w1 + c1, 0) @ w2 + c2).ravel()


def train_network(x, y, seed, steps=6000):
    rng = np.random.default_rng(seed)
    parameters = [rng.normal(0, 0.5, (2, 32)), np.zeros(32),
                  rng.normal(0, 0.15, (32, 1)), np.zeros(1)]
    # Full-batch gradient descent with Adam's first/second moment estimates.
    first, second = [np.zeros_like(p) for p in parameters], [np.zeros_like(p) for p in parameters]
    history = []
    for t in range(1, steps+1):
        loss, gradients = loss_and_grad(parameters, x, y[:, None])
        for j, gradient in enumerate(gradients):
            first[j] = .9*first[j] + .1*gradient
            second[j] = .999*second[j] + .001*gradient**2
            m = first[j]/(1-.9**t); v = second[j]/(1-.999**t)
            parameters[j] -= .003*m/(np.sqrt(v)+1e-8)
        if t == 1 or t % 50 == 0:
            history.append([t, loss])
    return parameters, np.array(history)


def scientific_checks(diag, example):
    p = example[0]
    center = p.mean(axis=0)
    geometric = np.mean(np.sum((p-center)**2, axis=1))
    pair = np.sum((p[:, None]-p[None, :])**2)/(2*len(p)**2)
    q, _ = np.linalg.qr(np.random.default_rng(7).normal(size=(3, 3)))
    q[:, 0] *= np.linalg.det(q)
    moved = p @ q + [20, -5, 11]
    moved_rg2 = np.mean(np.sum((moved-moved.mean(axis=0))**2, axis=1))
    assert abs(geometric-pair) < 1e-10
    assert abs(moved_rg2-geometric) < 1e-10
    step_error = np.max(np.abs(np.linalg.norm(np.diff(example, axis=1), axis=2)-1))
    assert step_error < 1e-12
    zmax = max(abs(d[k]) for d in diag for k in ("z_R2", "z_Rg2"))
    assert zmax < 5, "Compare sampling uncertainty before trusting the simulator."
    # An independent central-difference check of actual learning derivatives.
    r = np.random.default_rng(9)
    pars = [r.normal(size=(2, 4)), r.normal(size=4),
            r.normal(size=(4, 1)), r.normal(size=1)]
    x, y = r.normal(size=(7, 2)), r.normal(size=(7, 1))
    _, gradients = loss_and_grad(pars, x, y)
    gradient_error = 0.0
    for j, par in enumerate(pars):
        for ix in np.ndindex(par.shape):
            old = par[ix]; eps = 1e-6
            par[ix] = old+eps; plus = loss_and_grad(pars, x, y)[0]
            par[ix] = old-eps; minus = loss_and_grad(pars, x, y)[0]
            par[ix] = old
            gradient_error = max(gradient_error, abs((plus-minus)/(2*eps)-gradients[j][ix]))
    assert gradient_error < 1e-7
    return {"pair_identity_error": float(abs(geometric-pair)),
        "rotation_translation_error": float(abs(moved_rg2-geometric)),
        "segment_length_error": float(step_error), "maximum_sampling_z": zmax,
        "gradient_max_error": gradient_error}


def main():
    rows, diagnostics, example, distributions = sample_data()
    x = np.array([[r["N"], r["b_nm"]] for r in rows])
    y = np.array([r["rms_R_nm"] for r in rows])
    exact = np.array([r["exact_R_nm"] for r in rows])
    split = np.array([r["split"] for r in rows])
    train = split == "train"
    # Statistics of the test groups never enter the scaling or the optimization.
    mu, sd = x[train].mean(axis=0), x[train].std(axis=0)
    yscale = y[train].mean()
    scaled = (x-mu)/sd
    linear_weights = np.linalg.lstsq(np.c_[np.ones(train.sum()), scaled[train]], y[train], rcond=None)[0]
    # b and R are numerical ratios to 1 nm, making all logarithms dimensionless.
    log_weights = np.linalg.lstsq(np.c_[np.ones(train.sum()), np.log(x[train])], np.log(y[train]), rcond=None)[0]
    models, histories = [], []
    for seed in [11, 23, 37]:
        model, history = train_network(scaled[train], y[train]/yscale, seed)
        models.append(model); histories.append(history)

    def predictions(values):
        s = (values-mu)/sd
        nn = np.stack([network(model, s)*yscale for model in models])
        return {"linear": np.c_[np.ones(len(values)), s] @ linear_weights,
            "mlp": nn.mean(axis=0),
            "scaling": np.exp(np.c_[np.ones(len(values)), np.log(values)] @ log_weights),
            "analytic": values[:, 1]*np.sqrt(values[:, 0])}, nn

    pred, all_nn = predictions(x)
    metrics = {}
    for name in ["in_range", "longer"]:
        mask = split == name
        metrics[name] = {key: {"relative_mae_percent": float(np.mean(np.abs(p[mask]-exact[mask])/exact[mask])*100),
            "mae_nm": float(np.mean(np.abs(p[mask]-exact[mask])))} for key, p in pred.items()}
        metrics[name]["mlp_individual_relative_percent"] = [float(np.mean(np.abs(p[mask]-exact[mask])/exact[mask])*100) for p in all_nn]
    checks = scientific_checks(diagnostics, example)
    assert not (set(TRAIN_N) & set(TEST_N + LONG_N))
    results = {"definition": "3D freely jointed chain, N segments, N+1 equal beads, b in nm",
        "samples_per_N": SAMPLE_COUNT, "train_N": TRAIN_N, "test_N": TEST_N, "longer_N": LONG_N,
        "learning_target": "Monte Carlo RMS R; metrics use exact RMS R",
        "units": {"N": "segment count", "b": "nm", "R": "nm"},
        "scaling_fit": {"intercept": float(log_weights[0]), "exponent_N": float(log_weights[1]), "exponent_b": float(log_weights[2])},
        "standardization": {"x_mean": mu.tolist(), "x_std": sd.tolist(), "y_scale": float(yscale)},
        "linear_weights": linear_weights.tolist(), "log_weights": log_weights.tolist(),
        "mlp_weights": [[p.tolist() for p in m] for m in models], "mlp_seeds": [11, 23, 37],
        "training_steps": 6000, "hidden_units": 32, "metrics": metrics, "checks": checks,
        "monte_carlo": diagnostics}
    for i, row in enumerate(rows):
        row["predictions_nm"] = {key: float(v[i]) for key, v in pred.items()}
    (OUT/"samples.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (OUT/"results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    def panel(ax, key):
        if key == "conformations":
            for k, p in enumerate(example):
                centered = p-p.mean(axis=0)
                centered[:, 0] += 16*k
                ax.plot(centered[:, 0], centered[:, 1], color=COLORS[k], lw=1.5)
                ax.scatter([16*k], [0], marker="+", s=100, color="#202e39", zorder=4)
            ax.set(xlabel="x / nm (offset for display)", ylabel="y / nm", title="A  Three conformations, N = 64")
            ax.set_aspect("equal", adjustable="datalim")
            ax.text(.03, .96, "3D chains projected onto x-y; + = center", transform=ax.transAxes, va="top", fontsize=10)
        elif key == "distributions":
            for name, c in [("R", COLORS[1]), ("Rg", COLORS[2])]:
                ax.hist(distributions[name], bins=45, density=True, histtype="step", lw=2, color=c, label=name)
            ax.axvline(8, color=COLORS[1], ls="--", lw=1.3, label="R RMS = 8 nm")
            ax.set(xlabel="Size / nm", ylabel="Probability density / nm$^{-1}$", title="B  Size fluctuates: 6,000 chains")
            ax.legend(frameon=False)
        elif key == "finite_size":
            ns = np.arange(1, 129)
            ax.plot(ns, (ns+2)/(ns+1), c=COLORS[2], label="Exact finite-N ratio")
            ax.axhline(1, c=COLORS[0], ls="--", label="Long-chain approximation")
            ax.set(xscale="log", xlabel="N / segments", ylabel=r"$\langle R_g^2\rangle\, /\, (Nb^2/6)$", title="C  The short-chain correction")
            ax.scatter([d["N"] for d in diagnostics if d["N"] <=128], [d["mean_Rg2"]/(d["N"]/6) for d in diagnostics if d["N"] <=128], color=COLORS[1], s=22, label="Monte Carlo")
            ax.legend(frameon=False)
        elif key == "training":
            for h, seed, c in zip(histories, [11, 23, 37], COLORS):
                ax.plot(h[:, 0], h[:, 1], color=c, label=f"Seed {seed}")
            ax.set(yscale="log", xlabel="Optimization step", ylabel="Training MSE (scaled output)", title="D  Training all network weights")
            ax.legend(frameon=False)
        elif key == "extrapolation":
            ns = np.linspace(8, 512, 400); vals = np.c_[ns, np.ones(len(ns))]
            pp, pn = predictions(vals)
            ax.axvspan(128, 512, color="#f0e5d3", alpha=.7)
            labels = ["Linear", "MLP ensemble", "Log-scaling fit", "Analytic"]
            for (key2, v), label, c in zip(pp.items(), labels, COLORS):
                ax.plot(ns, v, color=c, lw=2, ls="--" if key2=="analytic" else "-", label=label)
            ax.fill_between(ns, pn.min(axis=0), pn.max(axis=0), color=COLORS[1], alpha=.15)
            ix = train & (x[:, 1] == 1)
            ax.scatter(x[ix, 0], y[ix], c="#242e37", s=18, zorder=5)
            ax.set(xlabel="N / segments", ylabel="RMS end distance / nm", title="E  New chain lengths, b = 1 nm", ylim=(0, None))
            ax.legend(frameon=False, ncol=2, loc="upper left")
        else:
            names = ["linear", "mlp", "scaling", "analytic"]
            for j, group in enumerate(["in_range", "longer"]):
                v = [metrics[group][name]["relative_mae_percent"] for name in names]
                ax.bar(np.arange(4)+(j-.5)*.36, v, width=.36, color=[COLORS[2], COLORS[1]][j], label=["Held-out N, inside range", "Longer chains"][j])
            ax.set_xticks(range(4), ["Linear", "MLP", "Scaling", "Analytic"])
            ax.set(ylabel="Mean absolute relative error / %", title="F  Test errors against exact size")
            ax.legend(frameon=False)
        ax.grid(alpha=.16)

    keys = ["conformations", "distributions", "finite_size", "training", "extrapolation", "errors"]
    for key in keys:
        fig, ax = plt.subplots(figsize=(6.4, 4.8), layout="constrained", facecolor="#fffdf8")
        panel(ax, key)
        fig.savefig(OUT/(key+".svg"), metadata={"Date": None})
        plt.close(fig)
    fig, axes = plt.subplots(3, 2, figsize=(16, 16), layout="constrained", facecolor="#fffdf8")
    for ax, key in zip(axes.flat, keys): panel(ax, key)
    fig.savefig(OUT/"chain_size_diagnostics.svg", metadata={"Date": None})
    fig.savefig(OUT/"chain_size_diagnostics.png", dpi=160, metadata={"Software": "Matplotlib"})
    plt.close(fig)
    print(f"Independent conformations: {len(diagnostics)*SAMPLE_COUNT:,}; training rows: {train.sum()}")
    print(f"Learned powers: N = {log_weights[1]:.4f}, b = {log_weights[2]:.4f}")
    for group in ["in_range", "longer"]:
        print(group+": relative MAE (%)", {key: round(metrics[group][key]["relative_mae_percent"], 3) for key in pred})
    print("Maximum sampling z:", round(checks["maximum_sampling_z"], 3))
    print("Backpropagation gradient check:", f'{checks["gradient_max_error"]:.2e}')
    print("Saved six panels, full samples, fitted weights and reproducible checks.")


if __name__ == "__main__":
    main()
