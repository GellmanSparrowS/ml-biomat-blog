"""Network connectivity and loading response are two separate learning tasks.

Dependencies: NumPy, PyTorch, scikit-learn, Matplotlib.
All samples are generated 2D unstressed axial-spring networks.
Lengths use l0, springs use k0, effective stiffness uses k0.
"""
from pathlib import Path
import os, copy, json
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
OUT = Path("gel_outputs")
torch.set_num_threads(4)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)

def boundary_path(n, edges, bottom, top):
    reached=set(map(int,bottom))
    adjacent=[[] for _ in range(n)]
    for a,b in edges:adjacent[a].append(b);adjacent[b].append(a)
    frontier=list(reached)
    while frontier:
        a=frontier.pop()
        for b in adjacent[a]:
            if b not in reached:reached.add(b);frontier.append(b)
    return bool(reached & set(map(int,top)))


def solve(x,edges,k,bottom,top,loading,delta=.01):
    """Minimize spring extension norm; zero modes are allowed, without a penalty."""
    x=np.array(x,float);edges=np.array(edges,int);k=np.array(k,float)
    rows=[]
    for (a,b),value in zip(edges,k):
        d=x[b]-x[a];direction=d/np.linalg.norm(d)
        row=np.zeros(x.size);row[2*a:2*a+2]=-direction*np.sqrt(value)
        row[2*b:2*b+2]=direction*np.sqrt(value);rows.append(row)
    B=np.array(rows).reshape(-1,x.size)
    fixed=np.sort(np.ravel([[2*i,2*i+1] for i in list(bottom)+list(top)]))
    free=np.setdiff1d(np.arange(x.size),fixed)
    u=np.zeros(x.size)
    for i in top:u[2*i:2*i+2]=delta*np.array(loading)
    if len(free):u[free]=np.linalg.lstsq(B[:,free],-B[:,fixed]@u[fixed],rcond=1e-11)[0]
    ext=B@u;energy=.5*float(ext@ext);force=B.T@ext
    reaction=sum(float(force[2*i:2*i+2]@np.array(loading)) for i in top)
    effective=2*energy/delta**2
    residual=float(max(abs(force[free]),default=0))
    assert residual<1e-8
    assert abs(reaction/delta-effective)<1e-8
    if effective<1e-10:effective=0.
    return dict(stiffness=effective,energy=energy,reaction=reaction,residual=residual,
                displacement=u.reshape(-1,2).tolist(),
                free_zero_modes=int(len(free)-np.linalg.matrix_rank(B[:,free],tol=1e-10)))


def generate():
    rng=np.random.default_rng(1313);side=4
    x=np.array([(i/(side-1),j/(side-1)) for j in range(side) for i in range(side)])
    candidates=[]
    for a in range(len(x)):
        for b in range(a+1,len(x)):
            grid=np.round(abs(x[b]-x[a])*(side-1)).astype(int)
            if max(grid)==1:candidates.append((a,b))
    candidates=np.array(candidates)
    bottom=np.arange(4);top=np.arange(12,16);interior=np.arange(4,12)
    budget=rng.integers(8,39,size=80);seen=set();rows=[]
    for family in ["uniform","bottleneck","horizontal_bias"]:
        for parent,m in enumerate(budget):
            weights=np.ones(len(candidates))
            if family=="bottleneck":
                crossing=(x[candidates[:,0],1]<.5)&(x[candidates[:,1],1]>.5)
                weights[crossing]=.035
            if family=="horizontal_bias":
                weights[abs(x[candidates[:,0],1]-x[candidates[:,1],1])>1e-9]=.08
            while True:
                choice=np.sort(rng.choice(len(candidates),size=int(m),replace=False,p=weights/weights.sum()))
                fingerprint=tuple(map(int,choice))
                if fingerprint not in seen:seen.add(fingerprint);break
            edges=candidates[choice]
            basek=rng.uniform(.7,1.3,size=len(edges))
            group=family+"-"+str(parent).zfill(3)
            split="family_test" if family=="horizontal_bias" else (
                "test" if parent%5==2 else "validation" if parent%5==4 else "train")
            for variant in range(2):
                geom=x.copy()
                if variant:geom[interior]+=rng.uniform(-.025,.025,size=(len(interior),2))
                spring=basek*rng.uniform(.85,1.15,size=len(edges))
                for loading_name,loading in [("shear",[1.,0.]),("extension",[0.,1.])]:
                    physical=solve(geom,edges,spring,bottom,top,loading)
                    rows.append(dict(group=group,family=family,variant=variant,loading_name=loading_name,
                        loading=loading,split=split,x=geom.tolist(),edges=edges.tolist(),k=spring.tolist(),
                        bottom=bottom.tolist(),top=top.tolist(),edge_count=int(m),
                        spanning=boundary_path(len(x),edges,bottom,top),**physical))
    return rows



def encode(rows):
    nodes=[];edge_features=[];counts=[];rich=[]
    for r in rows:
        x=np.array(r['x']);edges=np.array(r['edges']);k=np.array(r['k']);v=np.array(r['loading'])
        a=np.zeros((16,16));ef=np.zeros((16,16,5))
        for (i,j),w in zip(edges,k):
            d=x[j]-x[i];length=np.linalg.norm(d);n=d/length
            a[i,j]=a[j,i]=1
            ef[i,j]=[n[0],n[1],length,w,1]
            ef[j,i]=[-n[0],-n[1],length,w,1]
        degree=a.sum(1);bottom=np.zeros(16);top=np.zeros(16)
        bottom[r['bottom']]=1;top[r['top']]=1
        nodes.append(np.c_[x,bottom,top,np.tile(v,(16,1)),degree/8])
        edge_features.append(ef)
        m=len(edges);mean=float(k.mean())
        counts.append([m/42,mean,*v,(m/42)*v[0],(m/42)*v[1]])
        d=x[edges[:,1]]-x[edges[:,0]];length=np.linalg.norm(d,axis=1);n=d/length[:,None]
        affine=float(np.sum(k*(n@v)**2*d[:,1]**2))
        # Descriptors depend only on input geometry/edges, not equilibrium labels.
        triangles=float(np.trace(a@a@a)/6)
        visited=set();components=0
        for start in range(16):
            if start in visited:continue
            components+=1;queue=[start];visited.add(start)
            while queue:
                i=queue.pop()
                for j in np.flatnonzero(a[i]):
                    if j not in visited:visited.add(j);queue.append(j)
        rich.append(counts[-1]+[degree.std(),degree.min(),degree.max(),float(np.mean(degree<=1)),
                    components,triangles,float(k.std()),float(k.min()),float(k.max()),
                    float(np.sum(k*n[:,0]**2)),float(np.sum(k*n[:,1]**2)),
                    float(np.sum(k*n[:,0]*n[:,1])),affine])
    return np.array(nodes),np.array(edge_features),{"count":np.array(counts),"graph_features":np.array(rich)}


class GraphModel(nn.Module):
    def __init__(self,regression):
        super().__init__();self.regression=regression
        self.input=nn.Linear(7,24)
        self.self_layers=nn.ModuleList([nn.Linear(24,24) for _ in range(3)])
        self.neighbor=nn.ModuleList([nn.Linear(24,24,bias=False) for _ in range(3)])
        self.gates=nn.ModuleList([nn.Linear(4,24) for _ in range(3)])
        self.head=nn.Sequential(nn.Linear(24,24),nn.ReLU(),nn.Linear(24,1))
    def forward(self,n,e):
        h=torch.relu(self.input(n));mask=e[:,:,:,4:5]
        degree=mask.sum(2).clamp(min=1)
        for ws,wn,wg in zip(self.self_layers,self.neighbor,self.gates):
            gate=torch.sigmoid(wg(e[:,:,:,:4]))*mask
            message=(gate*wn(h)[:,None,:,:]).sum(2)/degree
            h=torch.relu(ws(h)+message)
        out=self.head(h.mean(1)).ravel()
        return torch.nn.functional.softplus(out) if self.regression else out


def score(rows,pred,task):
    out={}
    for split in ["train","validation","test","family_test"]:
        ids=np.array([i for i,r in enumerate(rows) if r['split']==split])
        if task=="spanning":
            y=np.array([rows[i]['spanning'] for i in ids])
            out[split]=dict(balanced_accuracy=float(balanced_accuracy_score(y,pred[ids]>=.5)),
                           auroc=float(roc_auc_score(y,pred[ids])))
        else:
            y=np.array([rows[i]['stiffness'] for i in ids]);p=np.expm1(pred[ids])
            out[split]=dict(RMSE=float(np.mean((p-y)**2)**.5),MAE=float(np.mean(abs(p-y))),
                           log1p_RMSE=float(np.mean((pred[ids]-np.log1p(y))**2)**.5))
    return out


def main():
    OUT.mkdir(exist_ok=True)
    rows=generate()
    node,edge,features=encode(rows)
    train=np.array([i for i,r in enumerate(rows) if r['split']=='train'])
    valid=np.array([i for i,r in enumerate(rows) if r['split']=='validation'])
    results={"models":{},"split_counts":{s:sum(r['split']==s for r in rows) for s in ["train","validation","test","family_test"]}}
    for task in ["spanning","response"]:
        # A graph path is invariant to loading, positive spring constants and geometry.
        # Keep only boundary identities, degrees and adjacency for that task.
        task_node=node.copy();task_edge=edge.copy();task_features=features
        if task=="spanning":
            task_node[:,:,[0,1,4,5]]=0
            task_edge[:,:,:,:4]=0
            task_features={"count":features["count"][:,[0]],
                           "graph_features":features["graph_features"][:,[0,6,7,8,9,10,11]]}
        nt=torch.tensor(task_node,dtype=torch.float32);et=torch.tensor(task_edge,dtype=torch.float32)
        y=np.array([float(r['spanning']) if task=="spanning" else np.log1p(r['stiffness']) for r in rows])
        results['models'][task]={}
        for name,X in task_features.items():
            scaler=StandardScaler().fit(X[train]);Z=scaler.transform(X);best=None;history=[]
            for lam in [.01,.1,1.,10.,100.]:
                model=(LogisticRegression(C=1/lam,max_iter=3000,tol=1e-9) if task=="spanning" else Ridge(alpha=lam)).fit(Z[train],y[train])
                p=model.predict_proba(Z[valid])[:,1] if task=="spanning" else np.maximum(0,model.predict(Z[valid]))
                loss=-balanced_accuracy_score(y[valid],p>=.5) if task=="spanning" else np.mean((p-y[valid])**2)
                history.append({"lambda":lam,"validation_loss":float(loss)})
                if best is None or loss<best[0]:best=(loss,model,lam)
            model=best[1]
            p=model.predict_proba(Z)[:,1] if task=="spanning" else np.maximum(0,model.predict(Z))
            results['models'][task][name]=dict(predictions=p.tolist(),scores=score(rows,p,task),lambda_=best[2],
                validation_candidates=history,scaler_mean=scaler.mean_.tolist(),scaler_scale=scaler.scale_.tolist(),
                coef=np.asarray(model.coef_).tolist(),intercept=np.asarray(model.intercept_).tolist())
        seeds=[];predictions=[]
        target=torch.tensor(y,dtype=torch.float32)
        lossfn=nn.BCEWithLogitsLoss() if task=="spanning" else nn.MSELoss()
        for seed in [13,23,33]:
            torch.manual_seed(seed);model=GraphModel(task=="response")
            optimizer=torch.optim.Adam(model.parameters(),lr=.003)
            rng=np.random.default_rng(1315);bestloss=float('inf');wait=0;history=[]
            for epoch in range(1,121):
                model.train()
                order=rng.permutation(train)
                for start in range(0,len(order),64):
                    ids=order[start:start+64];optimizer.zero_grad()
                    loss=lossfn(model(nt[ids],et[ids]),target[ids]);loss.backward();optimizer.step()
                model.eval()
                with torch.no_grad():
                    tl=float(lossfn(model(nt[train],et[train]),target[train]))
                    vl=float(lossfn(model(nt[valid],et[valid]),target[valid]))
                history.append(dict(epoch=epoch,train=tl,validation=vl))
                if vl<bestloss-1e-7:
                    bestloss=vl;bestepoch=epoch;weights=copy.deepcopy(model.state_dict());wait=0
                else:wait+=1
                if wait>=20:break
            model.load_state_dict(weights);model.eval()
            with torch.no_grad():
                p=model(nt,et)
                if task=="spanning":p=torch.sigmoid(p)
            p=p.numpy().astype(float);predictions.append(p)
            seeds.append(dict(seed=seed,best_epoch=bestepoch,history=history,scores=score(rows,p,task),
                parameters=sum(t.numel() for t in model.parameters()),
                state_dict={k:v.numpy().tolist() for k,v in weights.items()}))
            print(task,seed,"best epoch",bestepoch,"validation loss",bestloss,flush=True)
        p=np.mean(predictions,axis=0)
        results['models'][task]['message_passing']=dict(predictions=p.tolist(),scores=score(rows,p,task),seeds=seeds)
        for name,model in results['models'][task].items():
            key="balanced_accuracy" if task=="spanning" else "RMSE"
            print(task,name,key,"test %.6f; new family %.6f" %
                  (model['scores']['test'][key],model['scores']['family_test'][key]),flush=True)
    results["scope"]="Generated, unstressed 2D axial-spring networks; loading response in k0 units"
    results["generator_seed"]=1313
    results["split_parent_counts"]={s:len({r["group"] for r in rows if r["split"]==s}) for s in results["split_counts"]}
    results["topology_task_inputs"]="Boundary identities, degree and adjacency only; independent of geometry/k/loading."
    results["response_ensemble"]="Average log1p stiffness outputs, then expm1."
    results["selected_pair"]=["uniform-007","bottleneck-007"]
    for i,r in enumerate(rows):
        r["predictions"]={task:{name:float(m["predictions"][i]) for name,m in models.items()}
                          for task,models in results["models"].items()}
    make_plots(rows,results)
    (OUT/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT/"samples.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")


def make_plots(rows,results):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
        "axes.spines.top":False,"axes.spines.right":False,"svg.hashsalt":"L13-gels",
        "text.color":"#29433a","axes.labelcolor":"#29433a","axes.titlepad":14,
        "figure.facecolor":"#fffdf8","savefig.facecolor":"#fffdf8"})
    colors=["#ae8656","#5c7f9f","#257a68"]
    names=["count","graph_features","message_passing"]
    labels=["Connection count","Graph features","Message passing"]

    def graph(ax,r,amplification=0):
        x=np.array(r["x"]);edges=np.array(r["edges"]);u=np.array(r["displacement"])
        ax.add_collection(LineCollection(x[edges],colors="#c2c9be",linewidths=1.2))
        moved=x+amplification*u
        if amplification:
            ax.add_collection(LineCollection(moved[edges],colors="#568f78",linewidths=1.5))
            ax.quiver(x[:,0],x[:,1],amplification*u[:,0],amplification*u[:,1],
                      angles="xy",scale_units="xy",scale=1,width=.004,color="#a97248")
        nodecolors=["#62848b" if i in r["bottom"] else ("#ac8053" if i in r["top"] else "#376d59") for i in range(len(x))]
        ax.scatter(moved[:,0],moved[:,1],s=20,c=nodecolors,zorder=4)
        ax.set_aspect("equal");ax.set_xlim(-.12,1.27);ax.set_ylim(-.12,1.15);ax.axis("off")

    def draw(ax,key):
        if key=="fixture":
            ax.axis("off");ax.set_title("A  A spanning square can have zero linear shear stiffness")
            x=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
            for j,edges in enumerate([[(0,1),(0,2),(1,3),(2,3)],[(0,1),(0,2),(1,3),(2,3),(0,3)]]):
                solved=solve(x,edges,np.ones(len(edges)),[0,1],[2,3],[1.,0.])
                r=dict(x=x.tolist(),edges=edges,bottom=[0,1],top=[2,3],**solved)
                sub=ax.inset_axes([.02+.5*j,.19,.46,.69]);graph(sub,r,20)
                sub.set_title(["Square","Add one diagonal"][j],fontsize=11)
                ax.text(.25+.5*j,.11,"Spanning: yes\nEffective stiffness / k0 = "+str(round(solved["stiffness"],2)),
                        ha="center",va="top",transform=ax.transAxes,fontsize=10)
            ax.text(.5,.01,"Displacement drawn 20 times larger; small-strain axial springs",ha="center",transform=ax.transAxes,fontsize=8)
        elif key=="fractions":
            rr=[r for r in rows if r["variant"]==0 and r["loading_name"]=="shear"]
            intervals=[8,14,20,26,32,39];centers=[];a=[];b=[];counts=[]
            for lo,hi in zip(intervals[:-1],intervals[1:]):
                selected=[r for r in rr if lo<=r["edge_count"]<hi]
                centers.append((lo+hi-1)/2);counts.append(len(selected))
                a.append(np.mean([r["spanning"] for r in selected]))
                b.append(np.mean([r["stiffness"]>1e-8 for r in selected]))
            ax.plot(centers,a,"o-",color=colors[1],label="Bottom-to-top path")
            ax.plot(centers,b,"s-",color=colors[2],label="Positive linear shear response")
            for cx,n in zip(centers,counts):ax.text(cx,.025,"n="+str(n),ha="center",fontsize=8)
            ax.set(xlabel="Number of edges / binned",ylabel="Fraction of generated parent networks",
                   title="B  Connections and shear response emerge differently",ylim=(0,1.06))
            ax.legend(fontsize=8,loc="upper left");ax.grid(alpha=.12)
        elif key=="displacement":
            ax.axis("off");ax.set_title("C  The same 32 edges can leave a mechanical bottleneck")
            for j,group in enumerate(results["selected_pair"]):
                r=next(r for r in rows if r["group"]==group and r["variant"]==0 and r["loading_name"]=="shear")
                sub=ax.inset_axes([.02+.5*j,.19,.46,.69]);graph(sub,r,14)
                sub.set_title(group,fontsize=11)
                ax.text(.25+.5*j,.11,"Spanning: "+str(r["spanning"])+"\nStiffness / k0 = %.4f"%r["stiffness"],
                        ha="center",va="top",transform=ax.transAxes,fontsize=10)
            ax.text(.5,.01,"Gray: reference; green: relaxed displacements amplified 14 times",ha="center",transform=ax.transAxes,fontsize=8)
        elif key=="parity":
            model=results["models"]["response"]["message_passing"]
            maximum=max(r["stiffness"] for r in rows if r["split"] in ["test","family_test"])
            for split,color,mark in [("test",colors[1],"o"),("family_test",colors[2],"^")]:
                ids=[i for i,r in enumerate(rows) if r["split"]==split]
                target=np.array([rows[i]["stiffness"] for i in ids]);pred=np.expm1(np.array(model["predictions"])[ids])
                ax.scatter(target,pred,s=20,alpha=.5,c=color,marker=mark,
                           label="New parents" if split=="test" else "New topology family",edgecolors="none")
            ax.plot([0,maximum],[0,maximum],":",color="#948f7b")
            ax.set(xlabel="Direct mechanical solution / k0",ylabel="Graph model prediction / k0",
                   title="D  Predict response on held-out networks")
            ax.legend(fontsize=8);ax.grid(alpha=.12)
        elif key=="classification":
            for j,split in enumerate(["test","family_test"]):
                vals=[results["models"]["spanning"][name]["scores"][split]["balanced_accuracy"] for name in names]
                ax.barh(np.arange(3)+(.17 if j else -.17),vals,height=.3,
                        color=["#9ebdaa","#567e9e"][j],label=["New parents","New family"][j])
            ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,1.03)
            ax.axvline(.5,color="#9a907c",ls=":")
            ax.set(xlabel="Balanced accuracy",title="E  Learn spanning from topology alone")
            ax.legend(fontsize=8,loc="lower right");ax.grid(axis="x",alpha=.12)
        elif key=="regression":
            ax.axis("off");ax.set_title("F  Response errors in physical stiffness units")
            for j,metric in enumerate(["RMSE","MAE"]):
                sub=ax.inset_axes([.28,.56-.49*j,.68,.34])
                for i,split in enumerate(["test","family_test"]):
                    vals=[results["models"]["response"][name]["scores"][split][metric] for name in names]
                    sub.barh(np.arange(3)+(.16 if i else -.16),vals,height=.28,
                             color=["#9ebdaa","#567e9e"][i],label=["New parents","New family"][i])
                sub.set_yticks(range(3),labels,fontsize=8);sub.invert_yaxis()
                sub.set_xlabel(metric+" / k0",fontsize=9);sub.tick_params(labelsize=8)
                sub.grid(axis="x",alpha=.12)
                if j==0:sub.legend(fontsize=8,loc="upper center",bbox_to_anchor=(.5,1.3),ncol=2)

    keys=["fixture","fractions","displacement","parity","classification","regression"]
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.4,5.2),layout="constrained");draw(ax,key)
        fig.savefig(OUT/(key+".svg"),metadata={"Date":None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(14.8,15.6),layout="constrained")
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(OUT/"network_learning.svg",metadata={"Date":None})
    fig.savefig(OUT/"network_learning.png",dpi=180);plt.close(fig)


if __name__ == "__main__":
    main()
