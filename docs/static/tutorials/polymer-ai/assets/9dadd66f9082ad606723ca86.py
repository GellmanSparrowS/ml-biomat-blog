"""Environment-conditioned learning from exactly enumerated 3D lattice chains.
Run with Python, NumPy and Matplotlib. All distances use lattice step b = 1.
The generated observations are independent samples from the model, not lab data.
"""
from pathlib import Path
from collections import defaultdict
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("solvent_outputs")
OUT.mkdir(exist_ok=True)
DIRS = ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1))
NS = np.arange(3, 11)
TRAIN_U = [0, .25, .5, .75, 1]
VALID_U = [.125, .375, .625, .875]
NEW_U = [1.25, 1.5, 1.75, 2]
ADAPT_N = [4, 6, 8]
OBSERVATIONS = 10000
COLORS = ["#247968", "#c46c46", "#596d99", "#b3945d"]
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
    "axes.spines.top":False, "axes.spines.right":False,
    "axes.labelcolor":"#273b36", "text.color":"#273b36",
    "svg.hashsalt":"ai4s-L07", "savefig.facecolor":"#fffdf8"})


def enumerate_chains():
    # A histogram preserves multiplicity: distinct walks can share both m and Rg2.
    tables = [defaultdict(int) for _ in range(11)]
    occupied = {(0,0,0), (1,0,0)}
    points = [(0,0,0), (1,0,0)]
    representatives = {}

    def visit(n, position, contacts, sx, sy, sz, squared_sum):
        beads = n+1
        numerator = beads*squared_sum-sx*sx-sy*sy-sz*sz
        tables[n][(contacts, numerator)] += 1
        if n == 10:
            if contacts not in representatives:
                representatives[contacts] = [list(p) for p in points]
            return
        for dx, dy, dz in DIRS:
            new = (position[0]+dx, position[1]+dy, position[2]+dz)
            if new in occupied:
                continue
            # The previous bead is always adjacent; its chemical bond is excluded.
            added = sum((new[0]+a,new[1]+b,new[2]+c) in occupied
                        for a,b,c in DIRS)-1
            occupied.add(new); points.append(new)
            visit(n+1, new, contacts+added, sx+new[0], sy+new[1], sz+new[2],
                  squared_sum+sum(v*v for v in new))
            points.pop(); occupied.remove(new)

    visit(1, (1,0,0), 0, 1,0,0,1)
    histograms = {}
    for n in range(1,11):
        histograms[n] = np.array([[m, a, count] for (m,a),count
                                  in sorted(tables[n].items())], dtype=float)
    return histograms, representatives


def distribution(histograms, n, u):
    table = histograms[int(n)]
    contacts, numerator, counts = table.T
    log_weight = np.log(counts)+u*contacts
    weight = np.exp(log_weight-log_weight.max())
    weight /= weight.sum()
    rg2 = numerator/(n+1)**2
    return contacts, rg2, weight


def exact_response(histograms, n, u):
    m, rg2, probability = distribution(histograms, n, u)
    return float(np.sqrt(probability@rg2)), float(probability@m)


def ideal_size(n):
    n = np.asarray(n)
    return np.sqrt(n*(n+2)/(6*(n+1)))


def observation(histograms, n, u, rng):
    _, rg2, probability = distribution(histograms, n, u)
    counts = rng.multinomial(OBSERVATIONS, probability)
    observed = np.sqrt(counts@rg2/OBSERVATIONS)
    mean = probability@rg2
    variance = probability@((rg2-mean)**2)
    # Delta-method standard error of sqrt(mean Rg2), valid for a large sample.
    se = np.sqrt(variance/OBSERVATIONS)/(2*np.sqrt(mean))
    return float(observed), float(se)


def kernel(a, b, lengths):
    difference = (np.asarray(a)[:,None,:]-np.asarray(b)[None,:,:])/lengths
    return np.exp(-.5*np.sum(difference*difference, axis=2))


def fit_kernel(x, y, lengths, regularization, mean=1.):
    matrix = kernel(x, x, lengths)+regularization*np.eye(len(x))
    weights = np.linalg.solve(matrix, y-mean)
    return {"x":x.tolist(), "weights":weights.tolist(), "lengths":list(lengths),
            "regularization":regularization, "mean":mean}


def predict(model, x):
    return model["mean"]+kernel(x, model["x"], model["lengths"])@model["weights"]


def select_model(x, y, train, validation, condition):
    choices = []
    for ln in [.25, .5, 1.]:
        for lu in ([.25, .5, 1., 2.] if condition else [None]):
            lengths = [ln, lu] if condition else [ln]
            for reg in [1e-5, 1e-4, 1e-3]:
                model = fit_kernel(x[train], y[train], lengths, reg)
                loss = float(np.mean((predict(model,x[validation])-y[validation])**2))
                choices.append((loss, model))
    loss, model = min(choices, key=lambda item:item[0])
    model["validation_mse"] = loss
    return model


def main():
    histograms, representatives = enumerate_chains()
    full_counts = [int(6*histograms[n][:,2].sum()) for n in range(1,11)]
    assert full_counts == [6,30,150,726,3534,16926,81390,387966,1853886,8809878]
    rng = np.random.default_rng(707)
    rows = []
    for split, conditions in [("train",TRAIN_U),("validation",VALID_U),("new",NEW_U)]:
        for u in conditions:
            for n in NS:
                observed, se = observation(histograms, int(n), u, rng)
                exact, contacts = exact_response(histograms, int(n), u)
                role = "adapt" if split=="new" and u==1.5 and n in ADAPT_N else split
                rows.append({"N":int(n),"u":u,"split":role,"observed_Rg":observed,
                    "standard_error_Rg":se,"exact_Rg":exact,"exact_contacts":contacts})
    x = np.array([[r["N"]/10,r["u"]] for r in rows])
    ns = np.array([r["N"] for r in rows])
    scale = ideal_size(ns)
    y = np.array([r["observed_Rg"] for r in rows])/scale
    exact = np.array([r["exact_Rg"] for r in rows])
    role = np.array([r["split"] for r in rows])
    train, val, adapt, test = [role==name for name in ["train","validation","adapt","new"]]
    baseline = select_model(x[:,:1],y,train,val,False)
    conditioned = select_model(x,y,train,val,True)
    # A residual learner uses just three newly observed labels; test labels stay hidden.
    correction = fit_kernel(x[adapt], y[adapt]-predict(conditioned,x[adapt]),
        conditioned["lengths"],conditioned["regularization"],mean=0.)
    estimates = {"N_only":predict(baseline,x[:,:1])*scale,
        "conditioned":predict(conditioned,x)*scale,
        "updated":(predict(conditioned,x)+predict(correction,x))*scale}
    assert all(np.all(v>0) for v in estimates.values())
    metrics = {}
    for group, mask in [("validation_selected",val),("new_conditions",test),
                        ("u_1p5_unmeasured_N",test & (x[:,1]==1.5))]:
        metrics[group] = {key:float(100*np.mean(abs(p[mask]-exact[mask])/exact[mask]))
                          for key,p in estimates.items()}
    for i,row in enumerate(rows):
        row["predictions"] = {key:float(p[i]) for key,p in estimates.items()}
    # Independent repeated equilibrium samples quantify sampling scatter for one point.
    replicate_rng = np.random.default_rng(1707)
    repeat = np.array([observation(histograms,10,1.5,replicate_rng)[0] for _ in range(100)])
    reference = exact_response(histograms,10,1.5)[0]
    declared_se = observation(histograms,10,1.5,np.random.default_rng(2707))[1]
    derivative_checks = []
    for n in [4,7,10]:
        for u in [0,.5,1,1.5,2]:
            m, rg2, p = distribution(histograms,n,u)
            variance_m = p@((m-p@m)**2)
            covariance = p@((rg2-p@rg2)*(m-p@m))
            eps = 1e-5
            plus = exact_response(histograms,n,u+eps)
            minus = exact_response(histograms,n,u-eps)
            derivative_checks.extend([abs((plus[1]-minus[1])/(2*eps)-variance_m),
                abs((plus[0]**2-minus[0]**2)/(2*eps)-covariance)])
    # Every saved illustrative path satisfies the constraints and contact count.
    for m,path in representatives.items():
        points = np.array(path)
        assert len(set(map(tuple,path))) == len(path)
        assert np.all(np.sum(abs(np.diff(points,axis=0)),axis=1)==1)
        counted = sum(np.sum(abs(points[i]-points[j]))==1
                      for i in range(len(points)) for j in range(i+2,len(points)))
        assert counted == m
    z = [(r["observed_Rg"]-r["exact_Rg"])/r["standard_error_Rg"] for r in rows]
    check = {"enumerated_counts_all_orientations":full_counts,
        "first_direction_fixed_N10":full_counts[-1]//6,
        "response_derivative_max_error":float(max(derivative_checks)),
        "max_sampling_abs_z":float(np.max(np.abs(z))),
        "replicate_standard_error_ratio":float(repeat.std(ddof=1)/declared_se),
        "replicate_mean_z":float((repeat.mean()-reference)/(declared_se/10)),
        "train_rows":int(train.sum()),"validation_rows":int(val.sum()),
        "adapt_rows":int(adapt.sum()),"test_rows":int(test.sum())}
    assert check["response_derivative_max_error"] < 1e-7
    assert set(TRAIN_U).isdisjoint(VALID_U+NEW_U)
    assert not np.any(adapt & test)
    results = {"model":"3D cubic lattice; N segments, N+1 equal beads; no repeated site; E=-epsilon*m",
        "units":"b=1 lattice step; u=epsilon/(kBT); Rg is sqrt(mean Rg2)",
        "observation_source":"10000 independent equilibrium draws per (N,u) from exact joint histogram",
        "train_u":TRAIN_U,"validation_u":VALID_U,"new_u":NEW_U,
        "adaptation":{"u":1.5,"N":ADAPT_N,"method":"three-label residual kernel regression"},
        "models":{"N_only":baseline,"conditioned":conditioned,"correction":correction},
        "metrics_relative_mae_percent":metrics,"checks":check,
        "N10_u0_Rg":exact_response(histograms,10,0)[0],
        "N10_u2_Rg":exact_response(histograms,10,2)[0],
        "N10_u0_contacts":exact_response(histograms,10,0)[1],
        "N10_u2_contacts":exact_response(histograms,10,2)[1],
        "replicate_observations":repeat.tolist()}
    sample_output = {"rows":rows,"histograms":{str(n):h.astype(int).tolist() for n,h in histograms.items()},
        "histogram_columns":["contacts","Rg2_numerator","multiplicity_first_step_fixed"],
        "representative_paths":representatives,
        "representatives_note":"First enumerated path for each contact count, illustrative, not an equilibrium sample."}
    (OUT/"samples.json").write_text(json.dumps(sample_output,indent=2),encoding="utf-8")
    (OUT/"results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")

    def panel(ax, name):
        if name == "populations":
            for u,c in zip([0,1,2],COLORS):
                m,_,p = distribution(histograms,10,u)
                prob = np.bincount(m.astype(int),weights=p,minlength=8)
                ax.plot(np.arange(8),prob,"o-",color=c,label=f"u = {u}")
            ax.set(xlabel="Nonbonded contacts m",ylabel="Probability",title="A  Multiplicity and attraction, N = 10")
            ax.legend(frameon=False)
        elif name == "response":
            us = np.linspace(0,2,81)
            for n,c in zip([4,6,8,10],COLORS):
                ax.plot(us,[exact_response(histograms,n,u)[0] for u in us],c=c,label=f"N = {n}")
            ax.axvline(1,c="#8b9590",ls="--",lw=1)
            ax.set(xlabel="Attraction / thermal energy, u",ylabel="RMS radius of gyration / b",title="B  Exact finite-chain response")
            ax.legend(frameon=False,ncol=2)
        elif name == "conditional":
            us = np.linspace(0,2,121); xx = np.c_[np.ones(len(us)),us]
            truth = [exact_response(histograms,10,u)[0] for u in us]
            ax.axvspan(1,2,color="#eee2cd",alpha=.55,label="New conditions")
            ax.plot(us,truth,c=COLORS[0],lw=2.5,label="Exact enumeration")
            ax.plot(us,predict(baseline,xx[:,:1])*ideal_size(10),c=COLORS[2],ls=":",label="N only")
            ax.plot(us,predict(conditioned,xx)*ideal_size(10),c=COLORS[1],ls="--",label="N and u")
            mask = train & (ns==10)
            ax.scatter(x[mask,1],y[mask]*scale[mask],s=25,c="#273b36",zorder=5)
            ax.set(xlabel="u",ylabel="RMS radius of gyration / b",title="C  Same chain, different conditions")
            ax.legend(frameon=False,fontsize=9)
        elif name == "adaptation":
            xx = np.c_[NS/10,np.full(len(NS),1.5)]; scales = ideal_size(NS)
            ax.plot(NS,[exact_response(histograms,int(n),1.5)[0] for n in NS],"o-",c=COLORS[0],label="Exact enumeration")
            ax.plot(NS,predict(conditioned,xx)*scales,"--",c=COLORS[1],label="Before new labels")
            ax.plot(NS,(predict(conditioned,xx)+predict(correction,xx))*scales,"-.",c=COLORS[2],label="After 3 new labels")
            ax.scatter(ns[adapt],y[adapt]*scale[adapt],marker="*",s=150,c=COLORS[3],edgecolor="#806235",zorder=5,label="New observations")
            ax.set(xlabel="N / segments",ylabel="RMS radius of gyration / b",title="D  Updating at u = 1.5")
            ax.legend(frameon=False,fontsize=9)
        elif name == "errors":
            groups = ["new_conditions","u_1p5_unmeasured_N"]
            for i,group in enumerate(groups):
                vals = [metrics[group][key] for key in ["N_only","conditioned","updated"]]
                bars = ax.bar(np.arange(3)+(i-.5)*.36,vals,width=.36,color=COLORS[i],label=["All 29 held-out points","5 unmeasured N at u = 1.5"][i])
                ax.bar_label(bars,fmt="%.2f",padding=3,fontsize=9)
            ax.set_xticks(range(3),["N only","N and u","+ 3 labels"])
            ax.set(ylabel="Mean absolute relative error / %",title="E  Errors on unobserved targets")
            ax.margins(y=.22); ax.legend(frameon=False,fontsize=9)
        else:
            ax.hist((repeat-reference)/declared_se,bins=np.linspace(-4,4,19),color=COLORS[0],alpha=.75,edgecolor="white")
            ax.axvline(0,c=COLORS[1],lw=2,label="Exact equilibrium mean")
            ax.set(xlabel="(Sample RMS Rg - exact RMS Rg) / SE",ylabel="Repeated observations / count",title="F  100 independent observations, N = 10")
            ax.text(.04,.92,"u = 1.5; 10,000 draws each",transform=ax.transAxes,fontsize=10)
            ax.legend(frameon=False,fontsize=9)
        ax.grid(alpha=.15)

    keys = ["populations","response","conditional","adaptation","errors","sampling"]
    for name in keys:
        fig,ax = plt.subplots(figsize=(6.5,4.8),layout="constrained",facecolor="#fffdf8")
        panel(ax,name); fig.savefig(OUT/(name+".svg"),metadata={"Date":None}); plt.close(fig)
    fig,axes = plt.subplots(3,2,figsize=(16,16),layout="constrained",facecolor="#fffdf8")
    for ax,name in zip(axes.flat,keys): panel(ax,name)
    fig.savefig(OUT/"solvent_diagnostics.svg",metadata={"Date":None})
    fig.savefig(OUT/"solvent_diagnostics.png",dpi=160,metadata={"Software":"Matplotlib"}); plt.close(fig)
    print("Exact 3D walks (N=10, first direction fixed):",full_counts[-1]//6)
    print("Train / validation / new labels / untouched test:",train.sum(),val.sum(),adapt.sum(),test.sum())
    print("Selected conditional lengths, regularization:",conditioned["lengths"],conditioned["regularization"])
    for group in ["new_conditions","u_1p5_unmeasured_N"]:
        print(group,"relative MAE (%):",{k:round(v,3) for k,v in metrics[group].items()})
    print("Response derivative check:",f'{max(derivative_checks):.2e}')
    print("Independent replicate scatter / predicted SE:",round(check["replicate_standard_error_ratio"],3))
    print("Saved six figures, equilibrium histograms, observations and learned weights.")


if __name__ == "__main__":
    main()
