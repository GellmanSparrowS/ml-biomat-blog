"""An explicit polymer-solution model, clustering, and learned phase boundaries.

Dependencies: numpy, scipy, scikit-learn, matplotlib. All labels are calculated
from the stated N=20 Flory-Huggins model, not from condensate experiments.
"""
from pathlib import Path
from functools import lru_cache
import os
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import json
import numpy as np
from scipy.optimize import least_squares
from scipy.special import expit, logit
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OUT = Path("phase_outputs")
N = 20
PHI_C = 1 / (1 + np.sqrt(N))
CHI_C = .5 * (1 + 1 / np.sqrt(N))**2
COLORS = ["#b38a57", "#567ca0", "#237c69", "#a75660"]


def free_energy(phi, chi):
    """Dimensionless mixing free energy per lattice site."""
    phi = np.asarray(phi)
    return phi / N * np.log(phi) + (1-phi)*np.log1p(-phi) + chi*phi*(1-phi)


def derivative(phi, chi):
    return (np.log(phi)+1)/N - np.log1p(-phi)-1 + chi*(1-2*phi)


def curvature(phi, chi):
    return 1/(N*phi) + 1/(1-phi) - 2*chi


def spinodal(chi):
    if chi <= CHI_C:
        return None
    return np.sort(np.roots([2*chi*N, N-1-2*chi*N, 1])).astype(float)


@lru_cache(maxsize=512)
def binodal(chi):
    """Lower convex hull supplies a bracket; common tangency refines endpoints."""
    if chi <= CHI_C:
        return None
    p = np.unique(np.r_[np.geomspace(1e-12, .08, 600),
                        np.linspace(.08, 1-1e-9, 3001)])
    f = free_energy(p, chi)
    hull = []
    for i in range(len(p)):
        while len(hull) >= 2:
            a, b = hull[-2:]
            if (f[b]-f[a])*(p[i]-p[b]) < (f[i]-f[b])*(p[b]-p[a]):
                break
            hull.pop()
        hull.append(i)
    a, b = max(zip(hull[:-1], hull[1:]), key=lambda ab: ab[1]-ab[0])
    sa, sb = spinodal(chi)

    def residual(z):
        lo, hi = expit(z)
        slope = (free_energy(hi, chi)-free_energy(lo, chi))/(hi-lo)
        return [derivative(lo, chi)-slope, derivative(hi, chi)-slope]

    fitted = least_squares(residual, logit([p[a], p[b]]),
        bounds=([logit(1e-13), logit(sb)], [logit(sa), logit(1-1e-10)]),
        xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=100)
    lo, hi = expit(fitted.x)
    assert fitted.success and max(abs(np.array(residual(fitted.x)))) < 1e-9
    assert lo < sa < sb < hi
    return [float(lo), float(hi)]


def phase_label(phi, bounds):
    phi = np.asarray(phi)
    if bounds is None:
        return np.zeros_like(np.asarray(phi), dtype=int)
    return ((phi > bounds[0]) & (phi < bounds[1])).astype(int)


def dataset():
    """Whole chi conditions belong to a single split; sampling fixed in advance."""
    rows = []
    for group, chi in enumerate(np.linspace(.55, 1.10, 56)):
        bounds = binodal(chi)
        split = "test" if group % 5 == 2 else ("validation" if group % 5 == 4 else "train")
        for z in np.linspace(-9, 3, 80):
            phi = float(expit(z))
            rows.append(dict(group=group, chi=float(chi), phi=phi, z=float(z),
                split=split, sample="grid", label=int(phase_label(phi, bounds)),
                distance=None if bounds is None else float(min(abs(z-logit(np.array(bounds)))))))
        # Challenge samples stay with held-out conditions. They never train models.
        if split == "test" and bounds is not None:
            for edge in bounds:
                for offset in [.005, .015, .05, .15, .35]:
                    for sign in [-1, 1]:
                        z = float(logit(edge)+sign*offset)
                        phi = float(expit(z))
                        rows.append(dict(group=group, chi=float(chi), phi=phi, z=z,
                            split="boundary", sample="boundary", label=int(phase_label(phi, bounds)),
                            distance=offset))
    return rows


def evaluate(y, pred):
    return dict(accuracy=float(accuracy_score(y, pred)),
                balanced_accuracy=float(balanced_accuracy_score(y, pred)),
                confusion=confusion_matrix(y, pred, labels=[0, 1]).tolist(), count=len(y))


def main():
    OUT.mkdir(exist_ok=True)
    rows = dataset()
    X = np.array([[r["z"], r["chi"]] for r in rows])
    y = np.array([r["label"] for r in rows])
    masks = {s: np.array([r["split"] == s for r in rows])
             for s in ["train", "validation", "test", "boundary"]}
    train, val = masks["train"], masks["validation"]
    scaler = StandardScaler().fit(X[train])
    Z = scaler.transform(X)
    # Clustering receives no labels. Cluster numbers have no phase identity.
    km = KMeans(n_clusters=2, n_init=20, random_state=1212).fit(Z[train])
    clusters = km.predict(Z)
    mapping = [int(np.mean(y[train & (clusters == k)]) >= .5) for k in range(2)]
    candidates = []
    models = {}
    for C in [.1, 1., 10.]:
        model = LogisticRegression(C=C, solver="lbfgs", max_iter=2000, tol=1e-9).fit(Z[train], y[train])
        score = balanced_accuracy_score(y[val], model.predict(Z[val]))
        candidates.append(dict(model="linear", C=C, validation=float(score)))
        if "linear" not in models or score > models["linear"][0]:
            models["linear"] = (score, model, dict(C=C))
    for C in [.1, 1., 10.]:
        for gamma in [.1, 1., 10.]:
            model = SVC(C=C, gamma=gamma, kernel="rbf", tol=1e-7).fit(Z[train], y[train])
            score = balanced_accuracy_score(y[val], model.predict(Z[val]))
            candidates.append(dict(model="rbf", C=C, gamma=gamma, validation=float(score)))
            if "rbf" not in models or score > models["rbf"][0]:
                models["rbf"] = (score, model, dict(C=C, gamma=gamma))
    preds = {
        "curvature": (curvature(expit(X[:, 0]), X[:, 1]) < 0).astype(int),
        "cluster_mapped": np.array(mapping)[clusters],
        "linear": models["linear"][1].predict(Z),
        "rbf": models["rbf"][1].predict(Z)}
    scores = {name: {s: evaluate(y[m], pred[m]) for s, m in masks.items()}
              for name, pred in preds.items()}
    for i, r in enumerate(rows):
        r["cluster"] = int(clusters[i])
        r["predictions"] = {k: int(v[i]) for k, v in preds.items()}
    svm = models["rbf"][1]
    linear = models["linear"][1]
    result = dict(scope="Equilibrium binary incompressible N=20 polymer solution; constant chi; generated labels",
        N=N, critical=dict(phi=float(PHI_C), chi=float(CHI_C)), scores=scores,
        counts={s: int(m.sum()) for s, m in masks.items()},
        groups={s: sorted({rows[i]["group"] for i in np.flatnonzero(m)}) for s, m in masks.items()},
        selected={k: v[2] for k, v in models.items()}, candidates=candidates,
        scaler=dict(mean=scaler.mean_.tolist(), scale=scaler.scale_.tolist()),
        cluster=dict(centers=km.cluster_centers_.tolist(), phase_mapping_from_train=mapping),
        linear=dict(coef=linear.coef_.tolist(), intercept=linear.intercept_.tolist()),
        rbf=dict(support_vectors=svm.support_vectors_.tolist(), dual=svm.dual_coef_.tolist(),
                 intercept=svm.intercept_.tolist(), gamma=float(svm._gamma)),
        example=dict(chi=.90, phi=.20, binodal=binodal(.90)))
    lo, hi = result["example"]["binodal"]
    result["example"]["dense_volume_fraction"] = (.20-lo)/(hi-lo)
    result["example"]["free_energy_drop"] = float(free_energy(.20, .9) -
        ((hi-.20)*free_energy(lo, .9)+(.20-lo)*free_energy(hi, .9))/(hi-lo))
    # Independently useful coordinates for an offline equilibrium-condition viewer.
    result["interaction_table"] = [{"chi":float(c), "binodal":binodal(c)} for c in np.linspace(.55,1.10,111)]
    make_plots(rows, X, Z, y, masks, models, km, scaler, preds, result)
    (OUT/"results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT/"samples.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("N = 20; critical phi = %.6f, chi = %.6f" % (PHI_C, CHI_C))
    print("Samples:", result["counts"])
    print("Selected on validation:", result["selected"])
    for name in preds:
        print("%-15s balanced accuracy: test %.4f, boundary %.4f" %
              (name, scores[name]["test"]["balanced_accuracy"], scores[name]["boundary"]["balanced_accuracy"]))
    print("chi=0.90: dilute %.6f, dense %.6f, dense volume fraction %.6f" %
          (lo, hi, result["example"]["dense_volume_fraction"]))


def make_plots(rows, X, Z, y, masks, models, km, scaler, preds, result):
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10,
        "axes.spines.top":False, "axes.spines.right":False, "axes.labelcolor":"#2a4139",
        "text.color":"#2a4139", "svg.hashsalt":"L12-phase", "figure.facecolor":"#fffdf8",
        "axes.titlepad":13, "savefig.facecolor":"#fffdf8"})
    zs = np.linspace(-9,3,181); cs = np.linspace(.55,1.10,111)
    zz, cc = np.meshgrid(zs,cs); pp = expit(zz)
    GX = np.c_[zz.ravel(),cc.ravel()]; GZ = scaler.transform(GX)
    gr = models["rbf"][1].predict(GZ).reshape(zz.shape)
    gc = km.predict(GZ).reshape(zz.shape)
    bounds = [binodal(c) for c in cs]
    cmap = ListedColormap(["#e4eee7","#70b7a2"])

    def phase_axes(ax):
        ax.set_xscale("log");ax.set_xlim(expit(-9),expit(3));ax.set_ylim(.55,1.10)
        ax.set_xlabel("Polymer volume fraction");ax.set_ylabel("Interaction parameter chi")
        ax.set_xticks([.0002,.002,.02,.2,.8], labels=["0.0002","0.002","0.02","0.2","0.8"])

    def boundaries(ax, spin=False):
        use=np.array([[c,*b] for c,b in zip(cs,bounds) if b is not None])
        for j in [1,2]:ax.plot(use[:,j],use[:,0],color="#283b35",lw=1.5,label="Coexistence" if j==1 else None)
        if spin:
            ss=np.array([[c,*spinodal(c)] for c in cs if c>CHI_C])
            for j in [1,2]:ax.plot(ss[:,j],ss[:,0],color="#ab7046",ls="--",lw=1.4,label="Spinodal" if j==1 else None)
        ax.plot(PHI_C,CHI_C,"o",color="#ab7046",ms=4)

    def draw(ax, key):
        if key=="energy":
            p=np.linspace(.00001,.65,501);chi=.9;lo,hi=binodal(chi)
            m=(free_energy(hi,chi)-free_energy(lo,chi))/(hi-lo)
            # Subtract the tangent to magnify the meaningful free-energy difference.
            tangent=free_energy(lo,chi)+m*(p-lo)
            ax.plot(p,free_energy(p,chi)-tangent,color=COLORS[2],lw=2,label="Uniform state minus tangent")
            ax.hlines(0,lo,hi,color="#ac7852",lw=3,label="Two-phase free energy")
            ax.scatter([lo,hi],[0,0],color="#ac7852",zorder=5)
            ax.axvline(.20,color="#aaa18c",ls=":")
            ax.set(xlabel="Polymer volume fraction",ylabel="Free energy per site / kBT\nrelative to common tangent",
                   title="A  Why two compositions can lower free energy",ylim=(-.0006,.009))
            ax.legend(fontsize=8)
        elif key=="phase":
            truth=np.array([phase_label(expit(zs),b) for b in bounds])
            ax.contourf(pp,cc,truth,levels=[-.5,.5,1.5],cmap=cmap,antialiased=False)
            boundaries(ax,True);phase_axes(ax);ax.legend(fontsize=8,loc="lower left")
            ax.set_title("B  One phase, coexistence, and local instability")
            ax.text(.002,1.04,"Two phases",fontsize=10);ax.text(.002,.61,"One phase",fontsize=10)
        elif key=="clusters":
            ax.contourf(pp,cc,gc,levels=[-.5,.5,1.5],cmap=ListedColormap(["#d5e2ee","#dfceba"]),antialiased=False)
            boundaries(ax);phase_axes(ax);ax.set_title("C  Two clusters of inputs are not two phases")
            centers=scaler.inverse_transform(km.cluster_centers_)
            ax.scatter(expit(centers[:,0]),centers[:,1],marker="X",s=65,color="#495b69",edgecolor="white")
        elif key=="learned":
            ax.contourf(pp,cc,gr,levels=[-.5,.5,1.5],cmap=cmap,antialiased=False)
            boundaries(ax);phase_axes(ax);ax.set_title("D  Learned boundary and held-out errors")
            m=masks["test"] & (preds["rbf"]!=y)
            ax.scatter(expit(X[m,0]),X[m,1],s=20,marker="x",color="#b04c56",label="Wrong grid test")
            ax.legend(fontsize=8,loc="lower left")
        elif key=="scores":
            names=["curvature","cluster_mapped","linear","rbf"]
            labels=["Local curvature","Mapped clusters","Linear classifier","RBF classifier"]
            for j,s in enumerate(["test","boundary"]):
                ax.barh(np.arange(4)+(.17 if j else -.17),
                    [result["scores"][k][s]["balanced_accuracy"] for k in names],
                    height=.3,color=["#9bbcac","#477c9f"][j],label=["Held-out grid","Near boundary"][j])
            ax.axvline(.5,color="#9b9589",ls=":",label="Chance reference")
            ax.set_yticks(range(4),labels);ax.set_xlim(0,1.03);ax.invert_yaxis()
            ax.set(xlabel="Balanced accuracy",title="E  Evaluate both classes and both test sets")
            ax.legend(fontsize=8,loc="upper center",bbox_to_anchor=(.5,1.01),ncol=3)
            ax.set_title("E  Evaluate both classes and both test sets",pad=34)
        elif key=="boundary":
            for name,color in zip(["curvature","linear","rbf"],[COLORS[0],COLORS[1],COLORS[2]]):
                offsets=[.005,.015,.05,.15,.35];rates=[]
                for d in offsets:
                    m=masks["boundary"] & np.array([r["distance"]==d for r in rows])
                    rates.append(balanced_accuracy_score(y[m],preds[name][m]))
                ax.plot(offsets,rates,"o-",color=color,label=name.replace("rbf","RBF").replace("curvature","Local curvature"))
            ax.set_xscale("log");ax.set_ylim(0,1.04);ax.axhline(.5,color="#aaa18c",ls=":")
            ax.set(xlabel="Distance from coexistence boundary in logit(phi)",
                   ylabel="Balanced accuracy",title="F  Moving toward a boundary makes the test harder")
            ax.legend(fontsize=8)
        ax.grid(alpha=.12)

    keys=["energy","phase","clusters","learned","scores","boundary"]
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.4,5.2),layout="constrained");draw(ax,key)
        fig.savefig(OUT/(key+".svg"),metadata={"Date":None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(14.8,15.6),layout="constrained")
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(OUT/"phase_learning.svg",metadata={"Date":None})
    fig.savefig(OUT/"phase_learning.png",dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
