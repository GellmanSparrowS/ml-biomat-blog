"""Learn per-position pairing probabilities from a controlled RNA model.
Install: python -m pip install numpy matplotlib torch
Generated teaching labels: noncrossing AU/CG/GU pairs, minimum enclosed positions 3,
equal dimensionless pair log-weight 1. No experimental RNA labels are used.
All sequence variants in one composition/similarity component stay in one split.
"""
from pathlib import Path
from collections import Counter
import time, json, math, copy
import numpy as np
import torch
from torch import nn

OUT=Path('rna_outputs');OUT.mkdir(exist_ok=True)
torch.set_num_threads(4);torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
BASES='ACGU';ALLOWED={'AU','UA','CG','GC','GU','UG'}

def reference(s,theta=1.):
    n=len(s);z=np.eye(n+1);best=np.zeros((n+1,n+1),int);choice=np.full((n+1,n+1),-1,int)
    valid=np.array([[s[i]+s[j] in ALLOWED and j-i>=4 for j in range(n)] for i in range(n)])
    w=math.exp(theta)
    for length in range(1,n+1):
        for i in range(n-length+1):
            j=i+length;k=np.flatnonzero(valid[i,i:j])+i
            z[i,j]=z[i+1,j]+w*np.dot(z[i+1,k],z[k+1,j])
            best[i,j]=best[i+1,j]
            if len(k):
                scores=1+best[i+1,k]+best[k+1,j];q=int(np.argmax(scores))
                if scores[q]>best[i,j]:best[i,j]=scores[q];choice[i,j]=k[q]
    adj=np.zeros_like(z);adj[0,n]=1.;p=np.zeros((n,n))
    for length in range(n,0,-1):
        for i in range(n-length+1):
            j=i+length;k=np.flatnonzero(valid[i,i:j])+i;a=adj[i,j]
            adj[i+1,j]+=a
            p[i,k]+=a*w*z[i+1,k]*z[k+1,j]/z[0,n]
            adj[i+1,k]+=a*w*z[k+1,j];adj[k+1,j]+=a*w*z[i+1,k]
    p+=p.T;brackets=['.']*n
    def trace(i,j):
        if i>=j:return
        k=choice[i,j]
        if k<0:trace(i+1,j)
        else:brackets[i]='(';brackets[k]=')';trace(i+1,k);trace(k+1,j)
    trace(0,n)
    return {'p':p.sum(1).tolist(),'pair_matrix':p.tolist(),'structure':''.join(brackets),
            'log_Z':math.log(z[0,n]),'max_pairs':int(best[0,n])}

def generate():
    rng=np.random.default_rng(1111);rows=[]
    for length_class,number,lengths in [('short',240,[24,32,40]),('long',48,[56,64])]:
        for family in range(number):
            n=int(rng.choice(lengths));freq=rng.dirichlet(np.full(4,2.));stay=float(rng.choice([0.,.3,.6]))
            s=[str(rng.choice(list(BASES),p=freq))]
            for i in range(1,n):s.append(s[-1] if rng.random()<stay else str(rng.choice(list(BASES),p=freq)))
            # Composition-preserving sibling: change order while keeping every count.
            sibling=list(rng.permutation(s))
            for variant,letters in enumerate([s,sibling]):
                rows.append({'id':f'{length_class}-{family:03d}-{variant}','origin_group':f'{length_class}-{family:03d}',
                    'sequence':''.join(letters),'length':n,'length_class':length_class})
    # Merge generator siblings, exact compositions and high positional identity.
    parent=list(range(len(rows)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        a,b=root(i),root(j)
        if a!=b:parent[max(a,b)]=min(a,b)
    groups={}
    for i,row in enumerate(rows):
        for key in [('origin',row['origin_group']),('composition',tuple(row['sequence'].count(a) for a in BASES))]:
            if key in groups:union(i,groups[key])
            else:groups[key]=i
    for n in sorted({r['length'] for r in rows}):
        ids=[i for i,r in enumerate(rows) if r['length']==n]
        matrix=np.array([list(rows[i]['sequence']) for i in ids])
        for j,i in enumerate(ids):
            same=np.mean(matrix[j+1:]==matrix[j],axis=1)
            for k in np.flatnonzero(same>=.8):union(i,ids[j+1+int(k)])
    components=sorted({root(i) for i,row in enumerate(rows) if row['length_class']=='short'})
    shuffled=np.random.default_rng(1112).permutation(components)
    split={int(c):('train' if j<int(.6*len(shuffled)) else 'validation' if j<int(.8*len(shuffled)) else 'test')
           for j,c in enumerate(shuffled)}
    for i,row in enumerate(rows):
        row['group']=root(i);row['split']='long_test' if row['length_class']=='long' else split[root(i)]
        row.update(reference(row['sequence']))
    return rows

def features(rows):
    nmax=max(r['length'] for r in rows);x=np.zeros((len(rows),nmax,12),np.float32)
    target=np.zeros((len(rows),nmax),np.float32);mask=np.zeros_like(target)
    for q,r in enumerate(rows):
        s=r['sequence'];n=len(s);one=np.eye(4)[[BASES.index(a) for a in s]]
        x[q,:n,:4]=one;x[q,:n,4:8]=one.mean(0);pos=np.arange(n)
        x[q,:n,8]=pos/max(1,n-1);x[q,:n,9]=1/(pos+1);x[q,:n,10]=1/(n-pos);x[q,:n,11]=n/40
        target[q,:n]=r['p'];mask[q,:n]=1
    return tuple(torch.from_numpy(v) for v in [x,target,mask])

class Learner(nn.Module):
    def __init__(self,kind):
        super().__init__();self.kind=kind
        self.embed=nn.Linear(12,32)
        if kind=='attention':
            block=nn.TransformerEncoderLayer(32,4,64,dropout=0.,batch_first=True,activation='gelu')
            self.context=nn.TransformerEncoder(block,2,enable_nested_tensor=False)
        else:self.context=nn.Sequential(nn.Linear(32,64),nn.GELU(),nn.Linear(64,32))
        self.head=nn.Linear(32,1)
    def forward(self,x,mask):
        h=torch.tanh(self.embed(x))
        if self.kind=='attention':h=self.context(h,src_key_padding_mask=~mask.bool())
        else:h=self.context(h)
        return self.head(h).squeeze(-1).sigmoid()


def fit(rows):
    x,y,mask=features(rows)
    groups={s:np.array([i for i,r in enumerate(rows) if r['split']==s])
            for s in ['train','validation','test','long_test']}
    tr,va=groups['train'],groups['validation']
    def mse(p,target,active):
        return (((p-target)**2*active).sum(1)/active.sum(1)).mean()
    base=float((y[tr].sum(1)/mask[tr].sum(1)).mean())
    predictions={'training_mean':np.full(y.shape,base)};runs={};weights={}
    for kind in ['position_composition','attention']:
        run_predictions=[];runs[kind]=[];weights[kind]=[]
        for seed in [11,21,31]:
            torch.manual_seed(seed);model=Learner(kind)
            optimizer=torch.optim.Adam(model.parameters(),lr=.003)
            order=np.random.default_rng(1113);best=1e9;stale=0;history=[];saved=None
            for epoch in range(1,81):
                model.train();permutation=order.permutation(tr)
                for start in range(0,len(tr),64):
                    ids=permutation[start:start+64];optimizer.zero_grad()
                    p=model(x[ids],mask[ids]);loss=mse(p,y[ids],mask[ids])
                    loss.backward();optimizer.step()
                model.eval()
                with torch.no_grad():
                    v=float(mse(model(x[va],mask[va]),y[va],mask[va]))
                    train=float(mse(model(x[tr],mask[tr]),y[tr],mask[tr]))
                history.append({'epoch':epoch,'training_MSE':train,'validation_MSE':v})
                if v<best-1e-8:
                    best=v;saved=copy.deepcopy(model.state_dict());stale=0;best_epoch=epoch
                else:stale+=1
                if stale>=12:break
            model.load_state_dict(saved);model.eval()
            with torch.no_grad():run_predictions.append(model(x,mask).numpy())
            runs[kind].append({'history':history,'best_epoch':best_epoch,
                'best_validation_MSE':best,'parameters':sum(p.numel() for p in model.parameters()),'seed':seed})
            weights[kind].append({k:v.tolist() for k,v in saved.items()})
            print(kind,'seed',seed,'selected epoch',best_epoch,'validation MSE',round(best,6),flush=True)
        predictions[kind]=np.mean(run_predictions,axis=0)
        for k,run in enumerate(runs[kind]):
            run['split_RMSE']={s:float(np.sqrt(np.mean([
                np.mean((run_predictions[k][i,:rows[i]['length']]-np.array(rows[i]['p']))**2)
                for i in ids]))) for s,ids in groups.items()}
    metrics={}
    for name,p in predictions.items():
        metrics[name]={}
        for split,ids in groups.items():
            errors=np.array([np.mean((p[i,:rows[i]['length']]-np.array(rows[i]['p']))**2) for i in ids])
            metrics[name][split]={'sequence_equal_RMSE':float(np.sqrt(errors.mean())),
                                  'sequence_errors':errors.tolist()}
    # Choose the first held-out 32-base sequence by ID, before looking at errors.
    example=min((i for i in groups['test'] if rows[i]['length']==32),key=lambda i:rows[i]['id'])
    for i,r in enumerate(rows):
        r['predictions']={k:p[i,:r['length']].tolist() for k,p in predictions.items()}
    results={'scope':'controlled noncrossing RNA ensemble; generated labels, no experimental labels',
        'theta':1.,'minimum_enclosed_positions':3,'allowed_pairs':sorted(ALLOWED),
        'seeds':[11,21,31],'generator_seed':1111,'split_seed':1112,
        'split_rule':'Generator siblings, equal A/C/G/U counts, or >=80% same-position identity at equal length are joined before group split; 56/64 bases reserved for long_test.',
        'metrics':metrics,'runs':runs,'weights':weights,'example_id':rows[example]['id'],
        'example_pair_matrix':rows[example]['pair_matrix'],
        'split':{s:{'rows':len(ids),'groups':len({rows[i]['group'] for i in ids}),
                    'lengths':sorted({rows[i]['length'] for i in ids})} for s,ids in groups.items()}}
    for name,m in metrics.items():
        print(name,{s:round(v['sequence_equal_RMSE'],5) for s,v in m.items()},flush=True)
    samples={'rows':[{k:v for k,v in r.items() if k!='pair_matrix'} for r in rows],
             'label_scope':results['scope']}
    (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    (OUT/'samples.json').write_text(json.dumps(samples,separators=(',',':')),encoding='utf-8')
    plots(results,samples)
    print('Example:',results['example_id'],'; six panels and all targets/predictions saved.')

def plots(results,samples):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
        'axes.spines.right':False,'axes.labelcolor':'#273b36','text.color':'#273b36',
        'svg.hashsalt':'ai4s-L11','savefig.facecolor':'#fffdf8'})
    rows=samples['rows'];names=['training_mean','position_composition','attention']
    labels=['Training mean','Base + composition + position','Sequence attention']
    colors=['#a39372','#5c7899','#267b69']
    example=next(r for r in rows if r['id']==results['example_id'])
    def panel(ax,key):
        if key=='sequence':
            xx=np.arange(1,example['length']+1)
            ax.plot(xx,example['p'],color='#202f29',lw=2,label='Exact rule-model target')
            for k,c,label in zip(names,colors,labels):
                ax.plot(xx,example['predictions'][k],color=c,lw=1.4,label=label)
            ax.set(xlabel='Position / 1-based',ylabel='Probability of being paired',
                   xlim=(1,example['length']),ylim=(-.02,1.02))
            ax.set_title('A  '+example['id']+': predict a marginal probability',pad=52)
            ax.legend(frameon=False,fontsize=8,loc='lower left',bbox_to_anchor=(0,1.01),ncol=2)
        elif key=='pairs':
            matrix=np.array(results['example_pair_matrix'])
            im=ax.imshow(matrix,origin='lower',cmap='YlGnBu',vmin=0,vmax=float(matrix.max()),
                         extent=(.5,len(matrix)+.5,.5,len(matrix)+.5))
            ax.figure.colorbar(im,ax=ax,label='Rule-model pairing probability',shrink=.8)
            ax.set(xlabel='Partner position j',ylabel='Position i',
                   title='B  Exact partner probabilities for the same sequence')
            ax.grid(False);return
        elif key=='length':
            lengths=[24,32,40,56,64]
            for k,c,label in zip(names,colors,labels):
                vals=[]
                for n in lengths:
                    selected=[r for r in rows if r['length']==n and r['split'] in ['test','long_test']]
                    vals.append(np.sqrt(np.mean([np.mean((np.array(r['predictions'][k])-r['p'])**2) for r in selected])))
                ax.plot(lengths,vals,'o-',c=c,label=label)
            ax.axvspan(48,68,color='#eadbc7',alpha=.45)
            ax.text(60,.265,'Lengths not used\nin training',ha='center',fontsize=9)
            ax.set(xlabel='Sequence length / bases',ylabel='Equal-sequence RMSE',
                   xlim=(21,68),ylim=(0,.31),xticks=lengths,title='C  Held-out sequences and held-out lengths')
            ax.legend(frameon=False,fontsize=8,loc='upper left')
        elif key=='learning':
            for run,c in zip(results['runs']['attention'],['#267b69','#587fa0','#c17a53']):
                h=run['history'];xx=[v['epoch'] for v in h]
                ax.plot(xx,[v['validation_MSE'] for v in h],c=c,label=f'Validation, seed {run["seed"]}')
                ax.plot(xx,[v['training_MSE'] for v in h],c=c,ls=':',alpha=.7)
                ax.scatter([run['best_epoch']],[run['best_validation_MSE']],c=c,s=40)
            ax.set(xlabel='Epoch',ylabel='Equal-sequence mean squared error',
                   title='D  Three actual attention-model training runs')
            ax.legend(frameon=False,fontsize=8);ax.text(.02,.03,'Dotted: training; dots: saved checkpoints',transform=ax.transAxes,fontsize=8)
        elif key=='data':
            splits=['train','validation','test','long_test'];counts=np.zeros(6)
            for split,c in zip(splits,['#267b69','#9bbca8','#5c7899','#c9a47b']):
                values=np.array([sum(r['length']==n and r['split']==split for r in rows) for n in [24,32,40,48,56,64]])
                ax.bar(range(6),values,bottom=counts,color=c,label=split,width=.65);counts+=values
            ax.set_xticks(range(6),[24,32,40,48,56,64])
            ax.set(xlabel='Sequence length / bases',ylabel='Number of sequences',ylim=(0,220),
                   title='E  Whole components stay in one split')
            ax.legend(frameon=False,fontsize=9)
        else:
            pairs=[]
            for origin in sorted({r['origin_group'] for r in rows if r['split']=='test'}):
                siblings=sorted([r for r in rows if r['origin_group']==origin],key=lambda r:r['id'])
                if len(siblings)==2:pairs.append(siblings)
            actual=np.array([np.mean(b['p'])-np.mean(a['p']) for a,b in pairs])
            extent=max(.02,float(np.max(abs(actual))))*1.2
            lo=-extent;hi=extent;ax.plot([lo,hi],[lo,hi],c='#b2b5a7',ls='--')
            for k,c,label in zip(names[1:],colors[1:],labels[1:]):
                predicted=[np.mean(b['predictions'][k])-np.mean(a['predictions'][k]) for a,b in pairs]
                ax.scatter(actual,predicted,c=c,s=30,alpha=.65,label=label)
            ax.set(xlim=(lo,hi),ylim=(lo,hi),xlabel='Rule target change in mean paired fraction',
                   ylabel='Predicted change after shuffling',title='F  Keep composition; rearrange the sequence')
            ax.legend(frameon=False,fontsize=8,loc='upper left')
        ax.grid(alpha=.14)
    keys=['sequence','pairs','length','learning','data','shuffle']
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.7,5.6),layout='constrained',facecolor='#fffdf8');panel(ax,key)
        fig.savefig(OUT/(key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(16,18),layout='constrained',facecolor='#fffdf8')
    for ax,key in zip(axes.flat,keys):panel(ax,key)
    fig.savefig(OUT/'rna_learning.svg',metadata={'Date':None})
    fig.savefig(OUT/'rna_learning.png',dpi=160,metadata={'Software':'Matplotlib'});plt.close(fig)

def main():
    rows=generate()
    print('Generated',len(rows),'sequences; rule-model targets and whole-component splits.')
    fit(rows)

if __name__=='__main__':main()
