"""L18: train message-passing models on published CMA1 glycan-array records.
Install: python -m pip install numpy scipy matplotlib openpyxl requests torch
Data: Lundstrøm et al. (2024), doi:10.3762/bjoc.20.31, CC BY 4.0.
The 403-row cohort is selected by structure and presentation occurrence, not RFU.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import io
import requests
import openpyxl
import numpy as np
from scipy.stats import spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path('graph_outputs');OUT.mkdir(exist_ok=True)
URL='https://www.beilstein-journals.org/bjoc/content/supplementary/1860-5397-20-31-S1.xlsx'
SHA='403d65ebe15cef6d05a92fa0a231fb81ea681fcdd2184a65b526ce3bf40e391a'
cache=OUT/'cma1_arrays.xlsx'
if not cache.exists():
    response=requests.get(URL,timeout=60);response.raise_for_status()
    cache.write_bytes(response.content)
raw=cache.read_bytes()
assert hashlib.sha256(raw).hexdigest()==SHA,'Source file differs from the published example'
book=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
values=list(book['imperial'].values);headers=values[0]
source_rows=[dict(zip(headers,row)) for row in values[1:]]
book.close()

BASES=['GlcNAc','GalNAc','Neu5Ac','Neu5Gc','GlcNS','GlcN','GlcA','IdoA','GalA','ManA','GulA','ManNAc','Glc','Gal','Man','Fuc','Xyl','Ara','Rha','Fru']
MONOMER=re.compile('(?:'+'|'.join(sorted(BASES,key=len,reverse=True))+r')(?:[1-9][SP])*$')

def parse(sequence):
    # Exact token coverage: no silent stripping of placeholders or unknown linkages.
    tokens=re.findall(r'\[|\]|\([ab][12]-[1-9]\)|[A-Za-z0-9]+',sequence)
    if ''.join(tokens)!=sequence:raise ValueError('unsupported_or_incomplete_notation')
    nodes=[];edges=[];pos=len(tokens)-1
    def chain(parent=None,branch=False):
        nonlocal pos
        current=parent;first=None
        while pos>=0 and tokens[pos]!='[':
            token=tokens[pos]
            if token==']':
                if current is None:raise ValueError('branch_without_parent')
                pos-=1;chain(current,True)
                if pos<0 or tokens[pos]!='[':raise ValueError('unbalanced_branch')
                pos-=1;continue
            if token.startswith('('):
                if current is None:raise ValueError('dangling_link')
                link=token[1:-1];pos-=1
                if pos<0 or not MONOMER.fullmatch(tokens[pos]):raise ValueError('unknown_residue')
                node=len(nodes);nodes.append(tokens[pos]);edges.append({'child':node,'parent':current,'link':link})
                current=node;pos-=1
            else:
                if current is not None or not MONOMER.fullmatch(token):raise ValueError('unknown_residue_or_missing_link')
                current=len(nodes);nodes.append(token);pos-=1
            if first is None:first=current
        return first
    root=chain()
    if pos!=-1 or not nodes or len(edges)!=len(nodes)-1:raise ValueError('not_a_complete_tree')
    children={i:[] for i in range(len(nodes))}
    for e in edges:children[e['parent']].append((e['link'],e['child']))
    for values in children.values():
        acceptor=[link.split('-')[1] for link,_ in values]
        if len(acceptor)!=len(set(acceptor)):raise ValueError('duplicate_acceptor_site')
    def canonical(i):return nodes[i]+'{'+','.join(link+':'+canonical(c) for link,c in sorted(children[i],key=lambda q:(q[0],canonical(q[1]))))+'}'
    return {'nodes':nodes,'edges':edges,'root':root,'canonical':canonical(root)}


accepted=[];excluded=[]
for index,row in enumerate(source_rows):
    try: accepted.append(row|{'row':index+2,'graph':parse(row['glycan'])})
    except ValueError as error:
        excluded.append({'row':index+2,'reason':str(error),'glycan':row['glycan']})
parsed={'accepted':accepted,'excluded':excluded}
assert len(source_rows)==866 and len(accepted)==649
counts=Counter(r['graph']['canonical'] for r in parsed['accepted'])
rows=[r for r in parsed['accepted'] if counts[r['graph']['canonical']]==1]
rows.sort(key=lambda r:r['graph']['canonical'])
families=sorted({json.dumps(sorted(Counter(r['graph']['nodes']).items())) for r in rows})
order=np.random.default_rng(1010).permutation(len(families))
partition={families[int(j)]:('train' if i<int(.6*len(order)) else 'validation' if i<int(.8*len(order)) else 'test') for i,j in enumerate(order)}
for r in rows:
    r['composition_group']=json.dumps(sorted(Counter(r['graph']['nodes']).items()))
    r['split']=partition[r['composition_group']]
    r['AO_label']=int(bool(re.search(r'[-.]AO(?:\b|\*)',r['original_notation'])))
    r['id']=f"ICL-{r['row']:04d}"
groups={s:np.array([i for i,r in enumerate(rows) if r['split']==s]) for s in ['train','validation','test']}
y=np.log1p([r['RFU'] for r in rows]);tr,va,te=[groups[s] for s in groups]

def descriptors(graph,depth,typed=True):
    labels=list(graph['nodes']);out=Counter('0:'+x for x in labels)
    adjacency=[[] for _ in labels]
    for edge in graph['edges']:
        i,j=edge['child'],edge['parent'];link=edge['link'] if typed else '*'
        adjacency[i].append(('to-parent:'+link,j));adjacency[j].append(('to-child:'+link,i))
    for level in range(1,depth+1):
        labels=[json.dumps([labels[i],sorted((edge,labels[j]) for edge,j in neighbors)],separators=(',',':'))
                for i,neighbors in enumerate(adjacency)]
        out.update(str(level)+':'+label for label in labels)
    return dict(out)

def matrix(dicts):
    # Feature vocabulary from training structures only; unseen motifs contribute zero.
    vocabulary=sorted({k for i in tr for k in dicts[i]});index={k:j for j,k in enumerate(vocabulary)}
    x=np.zeros((len(dicts),len(vocabulary)),dtype=float)
    for i,d in enumerate(dicts):
        for key,value in d.items():
            if key in index:x[i,index[key]]=value
    # Include unseen motif counts in the norm: they are orthogonal features,
    # not a reason to inflate the similarity of the remaining known motifs.
    norm=np.array([np.sqrt(sum(v*v for v in d.values())) for d in dicts])[:,None]
    x=np.divide(x,norm,out=np.zeros_like(x),where=norm>0)
    # Observed AO notation is an assay-presentation covariate, shared by every learned model.
    presentation=np.array([[int(r['AO_label']==0),r['AO_label']] for r in rows],float)
    return np.hstack([x,.25*presentation]),vocabulary

def metrics(pred,indices):
    loss=(pred[indices]-y[indices])**2
    unique=sorted({rows[i]['composition_group'] for i in indices})
    per=[float(np.mean([loss[j] for j,i in enumerate(indices) if rows[i]['composition_group']==f])) for f in unique]
    return {'RMSE_log':float(np.sqrt(loss.mean())),'MAE_log':float(np.mean(abs(pred[indices]-y[indices]))),
            'R2_log':float(1-loss.sum()/np.sum((y[indices]-y[indices].mean())**2)),
            'group_equal_RMSE_log':float(np.sqrt(np.mean(per))),
            'spearman':float(spearmanr(pred[indices],y[indices]).statistic) if np.std(pred[indices])>1e-12 else None}

predictions={'train_mean':np.full(len(rows),y[tr].mean())};models={}
for name,depths,typed in [('composition',[0],True),('untyped_graph',[1,2],False),('typed_graph',[1,2],True)]:
    mean=float(y[tr].mean());choices=[];best=None
    for depth in depths:
        dictionaries=[descriptors(r['graph'],depth,typed) for r in rows];x,vocabulary=matrix(dictionaries)
        kernel=x@x.T
        for reg in [1e-4,1e-3,.01,.1,1.,10.]:
            alpha=np.linalg.solve(kernel[np.ix_(tr,tr)]+reg*np.eye(len(tr)),y[tr]-mean)
            prediction=mean+kernel[:,tr]@alpha
            value=metrics(prediction,va)['group_equal_RMSE_log']
            choices.append({'depth':depth,'regularization':reg,'validation_group_RMSE':value})
            if best is None or value<best[0]:best=(value,reg,alpha,prediction,depth,x,vocabulary)
    value,reg,alpha,prediction,depth,x,vocabulary=best;predictions[name]=prediction
    models[name]={'depth':depth,'typed_edges':typed,'vocabulary':vocabulary,'alpha':alpha.tolist(),
        'train_mean':mean,'selected_regularization':reg,'choices':choices,'features':x.tolist()}
    print('baseline',name,'lambda',reg,'validation',round(value,3),flush=True)
results={'data_source_doi':'10.3762/bjoc.20.31','source_sheet':'imperial','source_sha256':'403d65ebe15cef6d05a92fa0a231fb81ea681fcdd2184a65b526ce3bf40e391a',
 'selection':'Explicit parsed glycan tree with one occurrence among the structurally eligible source rows; no response-based selection',
 'rows':len(rows),'composition_groups':len(families),'split_seed':1010,
 'split':{s:{'indices':ids.tolist(),'rows':len(ids),'groups':len({rows[i]['composition_group'] for i in ids}),
             'positive_reported_RFU':sum(rows[i]['RFU']>0 for i in ids)} for s,ids in groups.items()},
 'transform':'natural_log(1+RFU/1RFU)','models':models,'test_metrics':{k:metrics(p,te) for k,p in predictions.items()}}


# Learn messages on the same glycan records and split used above.
import copy
import torch
from torch import nn
torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
vocabulary=['<UNK>']+sorted({token for i in tr for token in rows[i]['graph']['nodes']})
node_index={v:i for i,v in enumerate(vocabulary)}
target_mean=float(y[tr].mean());target_scale=float(y[tr].std())
def pack(graphs,ao):
    types=[];send=[];receive=[];edge_features=[];membership=[];offset=0
    for k,g in enumerate(graphs):
        types.extend(node_index.get(t,0) for t in g['nodes']);membership.extend([k]*len(g['nodes']))
        for e in g['edges']:
            link=e['link'];anomer=0 if link[0]=='a' else 1;donor=int(link[1])-1;acceptor=int(link[3:])-1
            for direction,(a,b) in enumerate([(e['child'],e['parent']),(e['parent'],e['child'])]):
                f=np.zeros(15);f[anomer]=1;f[2+donor]=1;f[4+acceptor]=1;f[13+direction]=1
                send.append(offset+a);receive.append(offset+b);edge_features.append(f)
        offset+=len(g['nodes'])
    return dict(x=torch.eye(len(vocabulary))[types],sender=torch.tensor(send,dtype=torch.long),
        receiver=torch.tensor(receive,dtype=torch.long),edge=torch.tensor(np.array(edge_features).reshape(-1,15),dtype=torch.float32),
        group=torch.tensor(membership,dtype=torch.long),size=torch.tensor([len(g['nodes']) for g in graphs],dtype=torch.float32),
        ao=.25*torch.tensor([[1-a,a] for a in ao],dtype=torch.float32))
graphs=[r['graph'] for r in rows];ao=[r['AO_label'] for r in rows]
packed={s:pack([graphs[i] for i in ids],[ao[i] for i in ids]) for s,ids in groups.items()};all_graphs=pack(graphs,ao)
class GraphModel(nn.Module):
    def __init__(self,mode):
        super().__init__();self.mode=mode;self.embed=nn.Linear(len(vocabulary),32)
        self.sender=nn.ModuleList([nn.Linear(32,32,bias=False) for _ in range(3)])
        self.edge=nn.ModuleList([nn.Linear(15,32) for _ in range(3)])
        self.self_update=nn.ModuleList([nn.Linear(32,32) for _ in range(3)])
        self.aggregate=nn.ModuleList([nn.Linear(32,32,bias=False) for _ in range(3)])
        self.readout=nn.Sequential(nn.Linear(66,32),nn.Tanh(),nn.Linear(32,1))
    def forward(self,data):
        h=torch.tanh(self.embed(data['x']));e=data['edge']
        if self.mode=='untyped':e=torch.cat([torch.zeros_like(e[:,:13]),e[:,13:]],dim=1)
        for k in range(3):
            if self.mode=='bag':h=torch.tanh(self.self_update[k](h))
            else:
                message=torch.tanh(self.sender[k](h[data['sender']])+self.edge[k](e))
                total=torch.zeros_like(h).index_add(0,data['receiver'],message)
                h=torch.tanh(self.self_update[k](h)+self.aggregate[k](total))
        pooled=torch.zeros((len(data['size']),32),dtype=h.dtype).index_add(0,data['group'],h)
        out=torch.cat([pooled/data['size'][:,None],pooled,data['ao']],dim=1)
        return self.readout(out).squeeze(-1)
gnn_models={};gnn_curves={};seed_metrics={};gnn_predictions={}
validation_groups=sorted({rows[i]['composition_group'] for i in va})
vgroup=[np.array([j for j,i in enumerate(va) if rows[i]['composition_group']==g]) for g in validation_groups]
train_target=torch.tensor((y[tr]-target_mean)/target_scale,dtype=torch.float32)
for mode in ['bag','untyped','typed']:
    saved=[];histories=[];outputs=[];individual=[]
    for seed in [18,28,38]:
        torch.manual_seed(seed);model=GraphModel(mode);opt=torch.optim.Adam(model.parameters(),lr=.003,weight_decay=1e-4)
        best=float('inf');best_epoch=0;best_state=None;history=[]
        for epoch in range(1,241):
            model.train();opt.zero_grad();loss=((model(packed['train'])-train_target)**2).mean();loss.backward();opt.step()
            if epoch%5==0:
                model.eval()
                with torch.no_grad():vp=model(packed['validation']).numpy()*target_scale+target_mean
                vl=float(np.sqrt(np.mean([np.mean((vp[g]-y[va][g])**2) for g in vgroup])))
                history.append([epoch,float(loss.detach()),vl])
                if vl<best:best=vl;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
        model.load_state_dict(best_state);model.eval()
        with torch.no_grad():prediction=model(all_graphs).numpy()*target_scale+target_mean
        active=sum(p.numel() for name,p in model.named_parameters() if mode!='bag' or not name.startswith(('sender.','edge.','aggregate.')))
        if mode=='untyped':active-=3*32*13  # Zero chemical-edge columns never affect a prediction.
        saved.append(dict(seed=seed,epoch=best_epoch,validation_group_RMSE=best,allocated_parameters=sum(p.numel() for p in model.parameters()),active_parameters=active,
            weights={k:v.tolist() for k,v in best_state.items()}))
        histories.append(history);outputs.append(prediction);individual.append(metrics(prediction,te))
        print('GNN',mode,'seed',seed,'epoch',best_epoch,'validation_group_RMSE',round(best,4),flush=True)
    gnn_models[mode]=saved;gnn_curves[mode]=histories;seed_metrics[mode]=individual;gnn_predictions[mode]=outputs
    predictions['gnn_'+mode]=np.mean(outputs,axis=0)
def graph_predict(mode,graphs,ao):
    data=pack(graphs,ao);out=[]
    for item in gnn_models[mode]:
        model=GraphModel(mode);model.load_state_dict({k:torch.tensor(v) for k,v in item['weights'].items()});model.eval()
        with torch.no_grad():out.append(model(data).numpy()*target_scale+target_mean)
    return np.mean(out,axis=0)
toy_names=['Gal(a1-3)GlcNAc','Gal(b1-3)GlcNAc','Gal(a1-4)GlcNAc','Gal(b1-4)GlcNAc']
toy_graphs=[parse(s) for s in toy_names]
toy_predictions={mode:graph_predict(mode,toy_graphs,[0]*4).tolist() for mode in gnn_models}
assert np.ptp(toy_predictions['bag'])<1e-6 and np.ptp(toy_predictions['untyped'])<1e-6
def geometry(x):
    x=np.array(x,float);d=np.linalg.norm(x[:,None]-x[None,:],axis=-1)
    return dict(points=x.tolist(),distances=d.tolist(),Rg=float(np.sqrt(np.mean(np.sum((x-x.mean(0))**2,axis=1)))),
        signed_volume=float(np.linalg.det((x[1:]-x[0]).T)/6) if len(x)==4 else None)
straight=geometry([[0,0,0],[1,0,0],[2,0,0]]);bent=geometry([[0,0,0],[1,0,0],[1,1,0]])
x=np.array([[0,0,0],[1,0,0],[.2,1.1,0],[.1,.3,.8]])
theta=.7;rotation=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
spatial={name:geometry(v) for name,v in dict(original=x,rotated_translated=x@rotation.T+[3,-2,.4],reflected=x*[-1,1,1]).items()}
results.update(gnn=dict(vocabulary=vocabulary,target_mean=target_mean,target_scale=target_scale,models=gnn_models,
    training_curves=gnn_curves,seed_test_metrics=seed_metrics,unknown_nodes={s:sum(t not in node_index for i in ids for t in graphs[i]['nodes']) for s,ids in groups.items()},
    toy_names=toy_names,toy_predictions=toy_predictions),geometry=dict(straight=straight,bent=bent,rigid=spatial),
    test_metrics={k:metrics(p,te) for k,p in predictions.items()},validation_metrics={k:metrics(p,va) for k,p in predictions.items()})
samples={'rows':[dict(id=r['id'],source_row=r['row'],glycan=r['glycan'],graph=r['graph'],RFU=r['RFU'],
    log_RFU=float(y[i]),AO_label=r['AO_label'],composition_group=r['composition_group'],split=r['split'],
    predictions={k:float(v[i]) for k,v in predictions.items()}) for i,r in enumerate(rows)],'source_doi':'10.3762/bjoc.20.31','license':'CC BY 4.0'}
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
np.savez_compressed(OUT/'predictions.npz',target=y,**predictions,**{'seeds_'+k:np.array(v) for k,v in gnn_predictions.items()})
for name,p in predictions.items():print(name,metrics(p,te),flush=True)


# Computed diagnostics and figures; no additional model selection.
conditional={}
for name,p in predictions.items():
    conditional[name]={}
    for positive in [False,True]:
        ids=np.array([i for i in te if (rows[i]['RFU']>0)==positive]);err=p[ids]-y[ids]
        conditional[name]['positive' if positive else 'reported_zero']=dict(n=len(ids),MAE_log=float(np.mean(abs(err))),RMSE_log=float(np.sqrt(np.mean(err**2))))
results['conditional_test_metrics']=conditional
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
    'axes.labelcolor':'#30453f','text.color':'#243d35','axes.edgecolor':'#bac7c0','xtick.color':'#53675e',
    'ytick.color':'#53675e','svg.hashsalt':'L18-messages','figure.facecolor':'#fffef9','axes.facecolor':'#fffef9'})
names=['train_mean','composition','untyped_graph','typed_graph','gnn_bag','gnn_untyped','gnn_typed']
labels=['Training mean','Composition ridge','Untyped graph kernel','Typed graph kernel','Node-only neural model','GNN: no chemical edge type','GNN: typed edges']
colors=['#a39780','#7d94a1','#9dabb4','#387e94','#bfa777','#bb8153','#267b69']
def style(ax,title,x='',y=''):
    ax.set_title(title,loc='left',fontweight='bold',pad=15);ax.set_xlabel(x);ax.set_ylabel(y);ax.grid(axis='y',color='#e9ede5',lw=.7);ax.set_axisbelow(True)
def panel(i,fig,spec):
    if i==5:
        grid=spec.subgridspec(1,2,wspace=.35);axes=[fig.add_subplot(grid[0,j]) for j in range(2)]
        for j,(name,g) in enumerate([('Straight chain',results['geometry']['straight']),('Bent chain',results['geometry']['bent'])]):
            ax=axes[j];xy=np.array(g['points'])[:,:2];center=xy.mean(0)
            ax.plot(*xy.T,color='#93a894',lw=3,zorder=1);ax.scatter(*xy.T,s=150,c=['#b78351','#287b63','#387e94'],edgecolor='white',zorder=3)
            ax.scatter(*center,marker='+',s=100,color='#4d5e51',zorder=4)
            for k,p in enumerate(xy):ax.text(p[0],p[1]+.17,str(k+1),ha='center',fontsize=10)
            for p in xy:ax.plot([center[0],p[0]],[center[1],p[1]],color='#b6b9a8',ls=':',lw=1)
            ax.set(xlim=(-.25,2.25),ylim=(-.45,1.55),xlabel=f'x (nm)\n{name} · Rg = {g["Rg"]:.3f} nm',ylabel='y (nm)',aspect='equal')
            ax.set_title(('F  Same graph, different geometry' if j==0 else 'Same two bond lengths'),loc='left',fontsize=11,fontweight='bold',pad=18)
        return
    ax=fig.add_subplot(spec)
    if i==0:
        xx=np.arange(4)
        for mode,label,c in [('bag','Node-only',colors[4]),('untyped','No chemical edge type',colors[5]),('typed','Typed-edge GNN',colors[6])]:
            ax.plot(xx,results['gnn']['toy_predictions'][mode],'o-',label=label,color=c,lw=2,ms=6)
        ax.set_xticks(xx,['α1–3','β1–3','α1–4','β1–4']);ax.set_ylim(-.5,9.5)
        style(ax,'A  What changes when a linkage changes?','Gal(linkage)GlcNAc','Predicted ln(1 + RFU / 1 RFU)')
        ax.legend(frameon=False,fontsize=9,loc='upper left');ax.text(.03,.04,'Three-seed means · AO flag = 0\nModel sensitivity probe; no measured labels shown',transform=ax.transAxes,fontsize=9)
    elif i==1:
        for mode,label,c in [('bag','Node-only',colors[4]),('untyped','GNN: no chemical edge type',colors[5]),('typed','GNN: typed edges',colors[6])]:
            curves=np.array(results['gnn']['training_curves'][mode]);epochs=curves[0,:,0];values=curves[:,:,2]
            ax.fill_between(epochs,values.min(0),values.max(0),color=c,alpha=.13)
            ax.plot(epochs,values.mean(0),color=c,lw=2,label=label)
            for m in results['gnn']['models'][mode]:ax.scatter(m['epoch'],m['validation_group_RMSE'],color=c,s=25,zorder=3)
        style(ax,'B  Select checkpoints on validation groups','Training epoch','Equal-group validation RMSE (log response)')
        ax.legend(frameon=False,fontsize=8,loc='upper right');ax.text(.03,.05,'Line: mean of three seeds\nBand: seed range · dots: selected checkpoints',transform=ax.transAxes,fontsize=9)
    elif i==2:
        for j,(name,c) in enumerate(zip(names,colors)):
            mae=results['test_metrics'][name]['MAE_log'];rmse=results['test_metrics'][name]['RMSE_log']
            ax.plot([mae,rmse],[j,j],color=c,lw=3,alpha=.5);ax.scatter(mae,j,color=c,s=60,marker='o');ax.scatter(rmse,j,color=c,s=60,marker='D')
            ax.text(mae-.07,j,f'{mae:.2f}',ha='right',va='center',fontsize=9);ax.text(rmse+.07,j,f'{rmse:.2f}',ha='left',va='center',fontsize=9)
        ax.set_yticks(range(7),labels,fontsize=9);ax.invert_yaxis();ax.set_xlim(.9,3.7)
        style(ax,'C  Compare the same 64 test probes','Error in log response')
        ax.scatter([],[],c='#526658',marker='o',label='MAE');ax.scatter([],[],c='#526658',marker='D',label='RMSE');ax.legend(frameon=False,loc='lower right',ncol=2,fontsize=9)
    elif i==3:
        p=predictions['gnn_typed'][te];positive=y[te]>0
        ax.scatter(y[te][~positive],p[~positive],s=38,c='#9eafa1',alpha=.7,label='Reported zero (57)')
        ax.scatter(y[te][positive],p[positive],s=68,c='#b78351',edgecolor='white',label='Reported positive (7)')
        ax.plot([0,11],[0,11],c='#a5b5a6',ls='--');ax.axhline(target_mean,c='#9f947b',ls=':',lw=1)
        ax.set(xlim=(-.4,11),ylim=(min(-.5,p.min()-.3),max(11,p.max()+.3)))
        style(ax,'D  Typed GNN: inspect each prediction','Observed ln(1 + RFU / 1 RFU)','Predicted log response');ax.legend(frameon=False,loc='upper left',fontsize=9)
    else:
        selected=['train_mean','typed_graph','gnn_bag','gnn_untyped','gnn_typed'];xx=np.arange(5)
        zero=[conditional[k]['reported_zero']['RMSE_log'] for k in selected];pos=[conditional[k]['positive']['RMSE_log'] for k in selected]
        ax.bar(xx-.18,zero,.33,color='#93ac9b',label='Reported zero: 57 probes');ax.bar(xx+.18,pos,.33,color='#ba8559',label='Reported positive: 7 probes')
        ax.set_xticks(xx,['Mean','Typed\nkernel','Node-only','Untyped\nGNN','Typed\nGNN']);ax.set_ylim(0,8.5)
        style(ax,'E  Locate the errors by observed response','','RMSE in log response');ax.legend(frameon=False,loc='upper left',fontsize=9)
keys=['linkage','training','metrics','prediction','subgroups','geometry']
for i,key in enumerate(keys):
    fig=plt.figure(figsize=(8.6,5.3),layout='constrained');panel(i,fig,fig.add_gridspec(1,1)[0]);fig.savefig(OUT/f'{key}.svg',metadata={'Date':None});plt.close(fig)
fig=plt.figure(figsize=(18,16.2),layout='constrained');grid=fig.add_gridspec(3,2,hspace=.12,wspace=.1)
for i in range(6):panel(i,fig,grid[i//2,i%2])
fig.savefig(OUT/'graph_learning.svg',metadata={'Date':None});fig.savefig(OUT/'graph_learning.png',dpi=160,metadata={'Software':'L18 reproducible example'});plt.close(fig)
print('Source: 403 CMA1 probes, 265 composition groups; same L10 split 258/81/64')
print('Nine trained networks: three representations x three seeds; each budget 240 epochs')
print('Unknown residues in validation/test:',results['gnn']['unknown_nodes'])
print('Geometry example: identical two bonds, Rg',round(straight['Rg'],6),'vs',round(bent['Rg'],6),'nm')
print('Full observations, learned weights, predictions and six figures: graph_outputs/')
