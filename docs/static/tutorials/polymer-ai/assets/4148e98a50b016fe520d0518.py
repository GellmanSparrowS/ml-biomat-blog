"""Glycan connectivity and a learned kernel: reproduce the real CMA1 array example.
Install: python -m pip install numpy scipy matplotlib openpyxl requests
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

OUT=Path('glycan_outputs');OUT.mkdir(exist_ok=True)
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
    print(name,'dimensions',x.shape[1],'lambda',reg,'val',round(value,3),'test',metrics(prediction,te),flush=True)
results={'data_source_doi':'10.3762/bjoc.20.31','source_sheet':'imperial','source_sha256':'403d65ebe15cef6d05a92fa0a231fb81ea681fcdd2184a65b526ce3bf40e391a',
 'selection':'Explicit parsed glycan tree with one occurrence among the structurally eligible source rows; no response-based selection',
 'rows':len(rows),'composition_groups':len(families),'split_seed':1010,
 'split':{s:{'indices':ids.tolist(),'rows':len(ids),'groups':len({rows[i]['composition_group'] for i in ids}),
             'positive_reported_RFU':sum(rows[i]['RFU']>0 for i in ids)} for s,ids in groups.items()},
 'transform':'natural_log(1+RFU/1RFU)','models':models,'test_metrics':{k:metrics(p,te) for k,p in predictions.items()}}
samples={'rows':[r|{'log_RFU':float(y[i]),'predictions':{k:float(v[i]) for k,v in predictions.items()}} for i,r in enumerate(rows)],
         'exclusions':parsed['excluded'],'repeated_tree_rows_excluded':len(parsed['accepted'])-len(rows)}

# Keep source identifiers and molecular fields in the downloadable learning table.
for row in samples['rows']:
    row.pop('original_notation',None);row.pop('Zscore',None)
samples.update(source_doi='10.3762/bjoc.20.31',license='CC BY 4.0')
pair=[]
for name in ['H-Tri-T2-AO','Lex-Tri-AO']:
    matches=[r for r in source_rows if r['original_notation']==name]
    assert len(matches)==1
    r=matches[0];pair.append({'name':name,'glycan':r['glycan'],'RFU':r['RFU'],
                             'graph':parse(r['glycan'])})
results['illustrative_isomers']=pair
results['source_rows']=len(source_rows)
results['structurally_parsed_rows']=len(accepted)
results['zero_reported_RFU']=sum(r['RFU']==0 for r in rows)
results['presentation_covariate']='explicit AO marker vs other; fixed feature amplitude 0.25'
results['isomer_scope']='Source measurements for illustration, not a two-sample model evaluation; Lex tree occurs repeatedly and is outside the learning cohort.'
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2),encoding='utf-8')
print({s:v['rows'] for s,v in results['split'].items()},'positive RFU',sum(y>0))
print('Mean baseline:',results['test_metrics']['train_mean'])

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
    'axes.spines.right':False,'axes.labelcolor':'#273b36','text.color':'#273b36',
    'svg.hashsalt':'ai4s-L10','savefig.facecolor':'#fffdf8'})
names=['train_mean','composition','untyped_graph','typed_graph']
labels=['Training mean','Composition','Graph: no bond type','Graph: typed bonds']
colors=['#a39372','#5c7899','#c17150','#267b69']
toy=[parse(f'Gal({link})GlcNAc') for link in ['a1-3','b1-3','a1-4','b1-4']]
d=[descriptors(g,2,True) for g in toy]
similarity=np.array([[sum(v*b.get(k,0) for k,v in a.items())/
    np.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values())) for b in d] for a in d])

def panel(ax,key):
    if key=='data':
        splits=list(groups);n=np.array([len(groups[s]) for s in splits])
        pos=np.array([sum(rows[i]['RFU']>0 for i in groups[s]) for s in splits]);zero=n-pos
        ax.bar(range(3),zero,color='#d4dcd2',label='Reported RFU = 0',width=.58)
        ax.bar(range(3),pos,bottom=zero,color=colors[-1],label='Reported RFU > 0',width=.58)
        for j in range(3):
            ax.text(j,zero[j]/2,str(zero[j]),ha='center',va='center')
            ax.text(j,n[j]+7 if pos[j]<15 else zero[j]+pos[j]/2,str(pos[j]),
                    ha='center',va='center',color=colors[-1] if pos[j]<15 else 'white')
        ax.set_xticks(range(3),[f'{s.title()}\n{results["split"][s]["groups"]} groups' for s in splits])
        ax.set(ylabel='Number of glycan probes',ylim=(0,320),title='A  Split whole composition groups')
        ax.legend(frameon=False,fontsize=9)
    elif key=='prediction':
        p=predictions['typed_graph'][te];observed=y[te];positive=observed>0
        ax.scatter(observed[~positive],p[~positive],c='#a4b7ad',alpha=.5,s=32,label='Reported zero')
        ax.scatter(observed[positive],p[positive],c='#c17150',edgecolors='white',s=65,label='Reported positive')
        ax.plot([0,11],[0,11],c='#a9afa5',ls='--',label='Equal prediction and observation')
        ax.axhline(y[tr].mean(),c=colors[0],ls=':',label='Training-mean baseline')
        ax.set(xlabel='Observed ln(1 + RFU / 1 RFU)',ylabel='Predicted transformed response',
               title='B  Typed graph: all 64 test probes',xlim=(-.4,11),ylim=(min(-.5,p.min()-.4),11))
        ax.legend(frameon=False,fontsize=8,loc='upper left')
    elif key=='metrics':
        for j,(k,c) in enumerate(zip(names,colors)):
            rmse=results['test_metrics'][k]['RMSE_log'];mae=results['test_metrics'][k]['MAE_log']
            ax.plot([mae,rmse],[j,j],c=c,lw=3,alpha=.5)
            ax.scatter([mae],[j],c=c,s=65,marker='o');ax.scatter([rmse],[j],c=c,s=65,marker='D')
            ax.text(mae-.05,j-.17,f'{mae:.2f}',ha='right',fontsize=9)
            ax.text(rmse+.05,j+.20,f'{rmse:.2f}',ha='left',fontsize=9)
        ax.set_yticks(range(4),labels);ax.invert_yaxis()
        ax.set(xlim=(1.2,3.4),ylim=(3.7,-.7),xlabel='Error on transformed response / lower is better',
               title='C  Typical error and large errors weigh differently')
        ax.scatter([],[],c='#273b36',marker='o',label='MAE');ax.scatter([],[],c='#273b36',marker='D',label='RMSE')
        ax.legend(frameon=False,fontsize=9,loc='lower right')
    elif key=='validation':
        for k,c,label in zip(names[1:],colors[1:],labels[1:]):
            model=models[k]
            for depth in sorted({r['depth'] for r in model['choices']}):
                selected=[r for r in model['choices'] if r['depth']==depth]
                ax.plot([r['regularization'] for r in selected],
                        [r['validation_group_RMSE'] for r in selected],
                        c=c,ls='-' if depth==model['depth'] else ':',
                        label=f'{label}, depth {depth}')
            r=next(r for r in model['choices'] if r['depth']==model['depth'] and r['regularization']==model['selected_regularization'])
            ax.scatter([r['regularization']],[r['validation_group_RMSE']],c=c,s=65,zorder=4)
        ax.set(xscale='log',xlabel='Regularization strength',ylabel='Equal-group validation RMSE',
               title='D  Validation selects depth and regularization')
        ax.legend(frameon=False,fontsize=8)
    elif key=='isomers':
        vals=[r['RFU'] for r in pair]
        ax.bar([0,1],vals,color=[colors[-1],colors[2]],width=.5)
        for j,v in enumerate(vals):ax.text(j,v+100,f'{v:,} RFU',ha='center')
        ax.set_xticks([0,1],['H-Tri-T2-AO\nFuc to Gal: alpha 1-2','Lex-Tri-AO\nFuc to GlcNAc: alpha 1-3'])
        ax.set(ylabel='Published CMA1 array response / RFU',ylim=(0,5200),
               title='E  Same composition, different connectivity')
        ax.text(.02,.97,'Source illustration: two AO-labelled probes\nBoth contain one Fuc, one Gal and one GlcNAc',
                va='top',transform=ax.transAxes,fontsize=9)
    else:
        im=ax.imshow(similarity,cmap='YlGnBu',vmin=0,vmax=1)
        ticks=['alpha 1-3','beta 1-3','alpha 1-4','beta 1-4']
        ax.set_xticks(range(4),ticks);ax.set_yticks(range(4),ticks)
        for i in range(4):
            for j in range(4):ax.text(j,i,f'{similarity[i,j]:.2f}',ha='center',va='center',
                                     color='white' if i==j else '#273b36')
        ax.set(title='F  A representation can retain bond identity',xlabel='Gal(link)GlcNAc / defined structural examples')
        ax.text(.5,-.22,'Composition and untyped-graph similarities are all 1.00.\nShown: typed, depth-2 motif cosine; no assay covariate.',
                ha='center',transform=ax.transAxes,fontsize=8)
        ax.grid(False)
        return
    ax.grid(alpha=.14)

keys=['data','prediction','metrics','validation','isomers','similarity']
for key in keys:
    fig,ax=plt.subplots(figsize=(7.7,5.6),layout='constrained',facecolor='#fffdf8');panel(ax,key)
    fig.savefig(OUT/(key+'.svg'),metadata={'Date':None});plt.close(fig)
fig,axes=plt.subplots(3,2,figsize=(16,18),layout='constrained',facecolor='#fffdf8')
for ax,key in zip(axes.flat,keys):panel(ax,key)
fig.savefig(OUT/'glycan_learning.svg',metadata={'Date':None})
fig.savefig(OUT/'glycan_learning.png',dpi=160,metadata={'Software':'Matplotlib'});plt.close(fig)
print('Saved six panels, all cohort rows, predictions, selected models and exclusions.')
