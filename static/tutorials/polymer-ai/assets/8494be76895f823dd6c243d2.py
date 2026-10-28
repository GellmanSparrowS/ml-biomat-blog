"""Real CAID reference labels, similarity-group splits, and protein sequence learning.
Install: numpy matplotlib scikit-learn biopython torch transformers requests.
First run downloads a pinned CC BY 3.0 reference and MIT ESM-2 checkpoint (~31 MB).
Run in an empty working folder; all caches and outputs stay in that folder.
CPU execution; unknown labels are masked, while their amino acids remain context.
"""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import json
import time
import requests
import numpy as np
import torch
from torch import nn
from Bio.Align import PairwiseAligner, substitution_matrices
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers.utils import logging
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss, average_precision_score, f1_score, precision_recall_curve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path.cwd()
OUT=HERE/'protein_outputs';OUT.mkdir(exist_ok=True)
AA='ACDEFGHIKLMNPQRSTVWY'
torch.set_num_threads(4);torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
CAID_COMMIT='7bab7e8880d7f949e480fdb377c5a5c8546ae336'
CAID_SHA='b65848395557c751a818dc38049c89d95534c05fbe6f14651e9f5bfd2bb60469'
MODEL_REVISION='c731040fcd8d73dceaa04b0a8e6329b345b0f5df'
MODEL_FILES={'config.json': 'facb9355e8252149f6f99dff5fd1e32e890c3c655362b261d0c81cd6b5839c85', 'model.safetensors': '24c5fa474c48f3b754b86efe752d5f189d2bcd88190fa2270fc92b2ef3034189', 'special_tokens_map.json': '3aedcd4211c0d43aec4e607ff60a63255f3174ead795e997350f09a5f8cd9ee1', 'tokenizer_config.json': '7e9161ecdb548ec45a41cbc6b24aa4476fdd418461f491c4207baa99419a29ad', 'vocab.txt': '0b82cc0a7c7cf9e567b1e5892d793285b9fbae822c964ca48696f7db44598e03', 'README.md': '462a2f24724e19c6be0efab926315c294a863c9a9770e2c8b3d859b2d81a07de'}

def fetch_checked(url,target,digest):
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==digest:return
    response=requests.get(url,timeout=120);response.raise_for_status()
    assert hashlib.sha256(response.content).hexdigest()==digest, 'Source checksum changed'
    target.write_bytes(response.content)

def prepare_reference():
    fetch_checked(f'https://raw.githubusercontent.com/BioComputingUP/CAID/{CAID_COMMIT}/demo-data/references/disorder_pdb.fasta',
                  HERE/'caid_disorder_pdb.fasta',CAID_SHA)
    lines=(HERE/'caid_disorder_pdb.fasta').read_text().splitlines();records=[];excluded=[]
    for i in range(0,len(lines),3):
        identifier=lines[i][1:];sequence=lines[i+1];labels=lines[i+2]
        assert len(sequence)==len(labels) and set(labels)<=set('01-')
        reason=[]
        if not 64<=len(sequence)<=768:reason.append('length_outside_64_768')
        if not set(sequence)<=set('ACDEFGHIKLMNPQRSTVWY'):reason.append('noncanonical_residue')
        if sum(v in '01' for v in labels)<32:reason.append('fewer_than_32_evaluable_residues')
        row={'id':identifier,'sequence':sequence,'labels':labels,'length':len(sequence)}
        if reason:excluded.append({'id':identifier,'reasons':reason})
        else:records.append(row)
    records.sort(key=lambda r:r['id'])
    aligner=PairwiseAligner();aligner.mode='local';aligner.substitution_matrix=substitution_matrices.load('BLOSUM62')
    aligner.open_gap_score=-10.;aligner.extend_gap_score=-.5
    parent=list(range(len(records)))
    def root(i):
        while i!=parent[i]:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        a,b=root(i),root(j)
        if a!=b:parent[max(a,b)]=min(a,b)
    pairs=[];edges=[];start=time.perf_counter();skipped=0
    for i,a in enumerate(records):
        for j in range(i+1,len(records)):
            b=records[j]
            # Paired-residue coverage >=70% of BOTH sequences is impossible otherwise.
            if min(a['length'],b['length'])/max(a['length'],b['length'])<.7:
                skipped+=1;continue
            alignment=aligner.align(a['sequence'],b['sequence'])[0]
            matched=0;paired=0
            for (a0,a1),(b0,b1) in zip(*alignment.aligned):
                matched+=sum(x==y for x,y in zip(a['sequence'][a0:a1],b['sequence'][b0:b1]))
                paired+=int(a1-a0)
            columns=int(np.max(np.diff(alignment.coordinates,axis=1),axis=0).sum())
            identity=matched/columns;ca=paired/a['length'];cb=paired/b['length']
            pair={'a':a['id'],'b':b['id'],'identity':identity,'coverage_a':ca,'coverage_b':cb}
            pairs.append(pair)
            if identity>=.3 and ca>=.7 and cb>=.7:
                union(i,j);edges.append(pair)
        if i%40==0:print('Aligned index',i,'/',len(records),'elapsed',round(time.perf_counter()-start,1),flush=True)
    groups={}
    for i,row in enumerate(records):groups.setdefault(root(i),[]).append(row)
    ordered=sorted(groups);shuffled=np.random.default_rng(909).permutation(ordered)
    train_end=int(.6*len(shuffled));valid_end=int(.8*len(shuffled))
    for i,g in enumerate(shuffled):
        split='train' if i<train_end else 'validation' if i<valid_end else 'test'
        name=min(r['id'] for r in groups[g])
        for row in groups[g]:row['cluster']=name;row['split']=split
    mapping={r['id']:r for r in records}
    assert all(mapping[e['a']]['split']==mapping[e['b']]['split'] for e in edges)
    stats={}
    for split in ['train','validation','test']:
        subset=[r for r in records if r['split']==split];counts=Counter(''.join(r['labels'] for r in subset))
        stats[split]={'proteins':len(subset),'clusters':len({r['cluster'] for r in subset}),
                      'residues':sum(r['length'] for r in subset),'label_counts':dict(counts)}
        assert counts['0']>0 and counts['1']>0
    output={'source_sha256':hashlib.sha256((HERE/'caid_disorder_pdb.fasta').read_bytes()).hexdigest(),
        'selection':'64<=length<=768; canonical20aminoacids; >=32 evaluated residues; no score-based selection',
        'clustering':'Connected components; local BLOSUM62 alignment open-10 extend-.5; identity>=.30; paired-residue coverage>=.70 of each sequence',
        'split':'seed909 shuffled connected components, first60%train,next20%validation,last20%test',
        'records':records,'excluded':excluded,'similarity_edges':edges,'all_length_compatible_pair_metrics':pairs,
        'length_incompatible_pairs_skipped':skipped,'cluster_count':len(groups),
        'max_cluster_size':max(map(len,groups.values())),'statistics':stats,'elapsed_seconds':time.perf_counter()-start}
    (HERE/'grouped_reference.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    return output

def prepare_embeddings(reference):
    model_folder=HERE/'esm2_model';model_folder.mkdir(exist_ok=True)
    folder=HERE/'embeddings';folder.mkdir(exist_ok=True)
    for filename,digest in MODEL_FILES.items():
        fetch_checked(f'https://huggingface.co/facebook/esm2_t6_8M_UR50D/resolve/{MODEL_REVISION}/{filename}',
                      model_folder/filename,digest)
    records=sorted(reference['records'],key=lambda r:(r['length'],r['id']))
    logging.set_verbosity_error();logging.disable_progress_bar()
    tokenizer=AutoTokenizer.from_pretrained(model_folder,local_files_only=True)
    model=AutoModelForMaskedLM.from_pretrained(model_folder,local_files_only=True,use_safetensors=True)
    model.eval();model.requires_grad_(False)
    assert model.config.hidden_size==320 and model.config.num_hidden_layers==6
    entries=[]
    with torch.inference_mode():
        for start in range(0,len(records),4):
            batch=records[start:start+4]
            inputs=tokenizer([r['sequence'] for r in batch],padding=True,return_tensors='pt')
            assert np.array_equal(inputs['attention_mask'].sum(dim=1).numpy(),[r['length']+2 for r in batch])
            hidden=model.esm(**inputs).last_hidden_state.cpu().numpy()
            for j,row in enumerate(batch):
                features=hidden[j,1:row['length']+1].copy()
                assert features.shape==(row['length'],320) and np.isfinite(features).all()
                target=folder/(row['id']+'.npy');np.save(target,features,allow_pickle=False)
                entries.append({'id':row['id'],'sequence_sha256':hashlib.sha256(row['sequence'].encode()).hexdigest(),
                                'feature_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (HERE/'feature_checksums.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
    print('Frozen ESM-2 embeddings:',len(records),'proteins, 320 features per residue',flush=True)

def encode(sequence):
    return np.eye(20,dtype=np.float32)[[AA.index(a) for a in sequence]]

def windows(onehot,radius=10):
    prefix=np.vstack([np.zeros((1,20)),np.cumsum(onehot,axis=0)])
    left=np.maximum(0,np.arange(len(onehot))-radius)
    right=np.minimum(len(onehot),np.arange(len(onehot))+radius+1)
    return (prefix[right]-prefix[left])/(right-left)[:,None]

class LocalCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.network=nn.Sequential(nn.Conv1d(20,24,21,padding=10),nn.Tanh(),nn.Conv1d(24,1,1))
    def forward(self,x):return self.network(x).squeeze(1)

def batch_tensor(rows,indices):
    width=max(rows[i]['length'] for i in indices)
    x=np.zeros((len(indices),20,width),dtype=np.float32)
    y=np.zeros((len(indices),width),dtype=np.float32)
    mask=np.zeros((len(indices),width),dtype=bool)
    for j,i in enumerate(indices):
        row=rows[i];length=row['length'];x[j,:,:length]=row['onehot'].T
        y[j,:length]=np.maximum(0,row['y']);mask[j,:length]=row['y']>=0
    return torch.from_numpy(x),torch.from_numpy(y),torch.from_numpy(mask)

def predict_cnn(model,rows,indices):
    model.eval();pred={}
    with torch.inference_mode():
        for start in range(0,len(indices),16):
            ids=indices[start:start+16];x,_,_=batch_tensor(rows,ids)
            p=torch.sigmoid(model(x)).numpy()
            for j,i in enumerate(ids):pred[i]=p[j,:rows[i]['length']].astype(float)
    return pred

def concat_known(rows,indices,pred=None):
    yy=np.concatenate([rows[i]['y'][rows[i]['y']>=0] for i in indices])
    if pred is None:return yy
    pp=np.concatenate([pred[i][rows[i]['y']>=0] for i in indices])
    return yy,pp

def metrics(rows,indices,pred,threshold):
    y,p=concat_known(rows,indices,pred)
    per={rows[i]['id']:float(log_loss(rows[i]['y'][rows[i]['y']>=0],
         pred[i][rows[i]['y']>=0],labels=[0,1])) for i in indices}
    return {'residue_BCE':float(log_loss(y,p,labels=[0,1])),
        'average_precision':float(average_precision_score(y,p)),
        'F1':float(f1_score(y,p>=threshold)), 'threshold':float(threshold),
        'protein_macro_BCE':float(np.mean(list(per.values()))),'protein_losses':per}

def main():
    started=time.perf_counter()
    reference=prepare_reference()
    prepare_embeddings(reference)
    rows=reference['records'];groups={s:[i for i,r in enumerate(rows) if r['split']==s]
                                     for s in ['train','validation','test']}
    for row in rows:
        row['onehot']=encode(row['sequence'])
        row['y']=np.array([-1 if x=='-' else int(x) for x in row['labels']])
    tr,va,te=[groups[s] for s in ['train','validation','test']]
    ytrain=concat_known(rows,tr);yvalid=concat_known(rows,va)
    predictions={};heads={};histories=[];cnn_runs=[]
    for name in ['composition','window21','ESM2_frozen']:
        features=[]
        for row in rows:
            if name=='composition':f=np.repeat(row['onehot'].mean(axis=0)[None,:],row['length'],axis=0)
            elif name=='window21':f=windows(row['onehot'])
            else:f=np.load(HERE/'embeddings'/(row['id']+'.npy'),allow_pickle=False)
            # Use float64 for the convex classifier so the solver tolerance is meaningful.
            features.append(np.asarray(f,dtype=np.float64))
        xtrain=np.concatenate([features[i][rows[i]['y']>=0] for i in tr])
        xvalid=np.concatenate([features[i][rows[i]['y']>=0] for i in va])
        scaler=StandardScaler().fit(xtrain)
        xtrain=scaler.transform(xtrain);xvalid=scaler.transform(xvalid)
        choices=[];best=None
        for c in [.001,.01,.1,1.,10.]:
            head=LogisticRegression(C=c,max_iter=2000,tol=1e-7,solver='lbfgs').fit(xtrain,ytrain)
            assert int(head.n_iter_.max())<2000
            loss=float(log_loss(yvalid,head.predict_proba(xvalid)[:,1],labels=[0,1]))
            choices.append({'C':c,'validation_BCE':loss})
            if best is None or loss<best[0]:best=(loss,c,head)
        loss,c,head=best
        predictions[name]={i:head.predict_proba(scaler.transform(f))[:,1] for i,f in enumerate(features)}
        heads[name]={'selected_C':c,'choices':choices,'mean':scaler.mean_.tolist(),
                     'scale':scaler.scale_.tolist(),'coef':head.coef_[0].tolist(),
                     'intercept':float(head.intercept_[0])}
        print(name,'selected C',c,'validation BCE',round(loss,5),flush=True)

    for seed in [9,19,29]:
        torch.manual_seed(seed);rng=np.random.default_rng(seed)
        model=LocalCNN();initial={k:v.detach().clone() for k,v in model.state_dict().items()}
        optimizer=torch.optim.Adam(model.parameters(),lr=.003,weight_decay=.0001)
        best_loss=float('inf');best_state=None;best_epoch=0;history=[]
        for epoch in range(1,61):
            model.train();total_loss=0.;total_known=0
            order=rng.permutation(tr).tolist()
            for start in range(0,len(order),16):
                ids=order[start:start+16];x,y,mask=batch_tensor(rows,ids)
                optimizer.zero_grad(set_to_none=True)
                loss=nn.functional.binary_cross_entropy_with_logits(model(x)[mask],y[mask])
                loss.backward();optimizer.step()
                total_loss+=float(loss.detach())*int(mask.sum());total_known+=int(mask.sum())
            vp=predict_cnn(model,rows,va);yy,pp=concat_known(rows,va,vp)
            value=float(log_loss(yy,pp,labels=[0,1]))
            history.append({'epoch':epoch,'online_train_BCE':total_loss/total_known,'validation_BCE':value})
            if value<best_loss:
                best_loss=value;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
            if epoch-best_epoch>=12:break
        model.load_state_dict(best_state)
        delta=float(sum(torch.sum((best_state[k]-initial[k])**2) for k in initial).sqrt())
        assert delta>0
        pred=predict_cnn(model,rows,list(range(len(rows))));cnn_runs.append(pred)
        histories.append({'seed':seed,'best_epoch':best_epoch,'best_validation_BCE':best_loss,
            'weight_change_l2':delta,'history':history,
            'state_dict':{k:v.detach().numpy().tolist() for k,v in best_state.items()}})
        print('CNN',seed,'best epoch',best_epoch,'val BCE',round(best_loss,5),'weight change',round(delta,3),flush=True)
    predictions['CNN21']={i:np.mean([r[i] for r in cnn_runs],axis=0) for i in range(len(rows))}
    results={'data':reference['statistics'],'data_url':f'https://raw.githubusercontent.com/BioComputingUP/CAID/{CAID_COMMIT}/demo-data/references/disorder_pdb.fasta',
        'reference_license':'CC BY 3.0','model_id':'facebook/esm2_t6_8M_UR50D','model_revision':MODEL_REVISION,
        'model_weight_sha256':MODEL_FILES['model.safetensors'],'pretraining':'frozen pretrained sequence model; supervised labels only from training components',
        'runtime':{'torch':torch.__version__,'numpy':np.__version__},'sequence_groups':reference['cluster_count'],
        'source_sha256':reference['source_sha256'],'heads':heads,'cnn_runs':histories,
        'CNN_description':'20 one-hot channels -> Conv1d(20,24,kernel21,padding10) -> tanh -> Conv1d(24,1,1); average of three validation-selected seeds',
        'threshold_rule':'maximize validation residue F1 over .05,.06,...,.95; first threshold wins ties',
        'test_metrics':{},'validation_metrics':{},'bootstrap':{}}
    rng=np.random.default_rng(1909)
    clusters=sorted({rows[i]['cluster'] for i in te})
    draws=rng.integers(0,len(clusters),size=(1000,len(clusters)))
    for name,pred in predictions.items():
        yy,pp=concat_known(rows,va,pred)
        candidates=np.arange(5,96)/100
        threshold=float(candidates[np.argmax([f1_score(yy,pp>=t) for t in candidates])])
        results['test_metrics'][name]=metrics(rows,te,pred,threshold)
        results['validation_metrics'][name]=metrics(rows,va,pred,threshold)
        losses=results['test_metrics'][name]['protein_losses']
        # Resample whole similarity components, keeping all proteins of each selected component.
        sums=np.array([sum(losses[rows[i]['id']] for i in te if rows[i]['cluster']==c) for c in clusters])
        counts=np.array([sum(rows[i]['cluster']==c for i in te) for c in clusters])
        bootstrap=sums[draws].sum(axis=1)/counts[draws].sum(axis=1)
        results['bootstrap'][name]={'protein_macro_BCE_95_percentile':np.quantile(bootstrap,[.025,.975]).tolist(),
                                  'replicates':1000,'unit':'whole sequence-similarity component'}
    # Example selection uses labels and length, never a prediction error.
    eligible=[i for i in te if rows[i]['labels'].count('0')>=50 and rows[i]['labels'].count('1')>=50 and '-' in rows[i]['labels']]
    example=min(eligible,key=lambda i:(abs(rows[i]['length']-400),rows[i]['id']))
    results['example_id']=rows[example]['id']
    results['example_selection']='test proteins with >=50 ordered and >=50 disordered labels plus unknowns; length nearest400, ID tie-break'
    results['seed_test_AP']=[float(average_precision_score(*concat_known(rows,te,p))) for p in cnn_runs]
    results['test_disorder_fraction']=float(np.mean(concat_known(rows,te)))
    samples={'source':'CAID pinned repository demo-data/references/disorder_pdb.fasta',
        'license':'CC BY 3.0','records':[{k:v for k,v in row.items() if k not in ['onehot','y']}|{
            'predictions':{name:pred[i].tolist() for name,pred in predictions.items()}}
            for i,row in enumerate(rows)],'similarity_edges':reference['similarity_edges']}
    (OUT/'samples.json').write_text(json.dumps(samples,separators=(',',':')),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    for name,m in results['test_metrics'].items():
        print(name,'test AP',round(m['average_precision'],4),'F1',round(m['F1'],4),
              'residue BCE',round(m['residue_BCE'],4),'protein macro BCE',round(m['protein_macro_BCE'],4),flush=True)
    render_plots(results,samples)
    print('Example:',results['example_id'],'; six panels, all sequences and scores saved.',flush=True)

def render_plots(results,samples):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
        'axes.spines.right':False,'axes.labelcolor':'#273b36','text.color':'#273b36',
        'svg.hashsalt':'ai4s-L09','savefig.facecolor':'#fffdf8'})
    names=['composition','window21','CNN21','ESM2_frozen']
    colors=['#a39372','#5c7899','#c17150','#267b69']
    labels=['Whole-protein composition','21-residue composition','21-residue CNN (3 seeds)','Frozen ESM-2 + linear head']
    test=[r for r in samples['records'] if r['split']=='test']
    example=next(r for r in test if r['id']==results['example_id'])
    yy=np.array([int(v) for r in test for v in r['labels'] if v!='-'])
    pp={k:np.array([p for r in test for p,v in zip(r['predictions'][k],r['labels']) if v!='-']) for k in names}
    def panel(ax,key):
        if key=='sequence':
            x=np.arange(1,example['length']+1)
            for k,c,label in zip(names,colors,labels):ax.plot(x,example['predictions'][k],color=c,lw=1.3,label=label)
            colors_label={'0':'#5c7899','1':'#c17150','-':'#d9d9d3'}
            rgba=np.array([matplotlib.colors.to_rgba(colors_label[v]) for v in example['labels']])[None,:,:]
            ax.imshow(rgba,extent=(.5,example['length']+.5,-.15,-.04),aspect='auto')
            ax.set(xlim=(.5,example['length']+.5),ylim=(-.17,1.04),xlabel='Residue position / 1-based',ylabel='Disorder score',
                   title='')
            ax.set_title('A  '+example['id']+': scores along one test protein',pad=52)
            ax.legend(frameon=False,fontsize=8,loc='lower left',bbox_to_anchor=(0,1.01),ncol=2)
            ax.text(.02,-.20,'Reference strip: blue = order; orange = disorder; gray = excluded',transform=ax.transAxes,fontsize=8)
        elif key=='ranking':
            for k,c,label in zip(names,colors,labels):
                precision,recall,_=precision_recall_curve(yy,pp[k])
                ap=results['test_metrics'][k]['average_precision']
                ax.plot(recall,precision,c=c,label=f'{label}: AP {ap:.3f}')
            ax.axhline(yy.mean(),c='#b7b8ab',ls='--',label=f'Positive fraction: {yy.mean():.3f}')
            ax.set(xlim=(0,1),ylim=(0,1.03),xlabel='Recall of annotated disorder',ylabel='Precision among selected residues',title='B  Ranking known labels on 49 test proteins')
            ax.legend(frameon=False,fontsize=8,loc='lower left')
        elif key=='protein_errors':
            for j,(k,c) in enumerate(zip(names,colors)):
                values=np.array(list(results['test_metrics'][k]['protein_losses'].values()))
                jitter=np.linspace(-.15,.15,len(values))
                ax.scatter(np.full(len(values),j)+jitter,values,s=13,c=c,alpha=.35)
                mean=results['test_metrics'][k]['protein_macro_BCE']
                low,high=results['bootstrap'][k]['protein_macro_BCE_95_percentile']
                ax.plot([j,j],[low,high],c='#253e35',lw=2.5)
                ax.scatter([j],[mean],c=c,s=85,edgecolors='white',zorder=4)
            ax.set_xticks(range(4),['Global\ncomposition','Local\ncomposition','Local CNN','Frozen ESM-2'])
            ax.set(ylabel='Mean binary cross-entropy per protein',title='C  Each dot is one held-out protein')
            ax.text(.02,.98,'Large dots: equal-protein means\nBars: 95% component-bootstrap intervals',va='top',transform=ax.transAxes,fontsize=9)
        elif key=='learning':
            for run,c in zip(results['cnn_runs'],colors[1:]):
                history=run['history'];xx=[h['epoch'] for h in history]
                ax.plot(xx,[h['validation_BCE'] for h in history],c=c,label=f'Validation, seed {run["seed"]}')
                ax.plot(xx,[h['online_train_BCE'] for h in history],c=c,ls=':',alpha=.6)
                ax.scatter([run['best_epoch']],[run['best_validation_BCE']],c=c,s=45,zorder=3)
            ax.set(xlabel='Training epoch',ylabel='Binary cross-entropy',title='D  Select checkpoints using validation proteins')
            ax.text(.02,.02,'Dotted: online training loss; dots: selected checkpoints',transform=ax.transAxes,fontsize=8)
            ax.legend(frameon=False,fontsize=8)
        elif key=='data':
            splits=['train','validation','test'];bottom=np.zeros(3)
            for lab,c,label in [('0','#5c7899','Order (0)'),('1','#c17150','Disorder (1)'),('-','#d9d9d3','Excluded (-)')]:
                count=np.array([results['data'][s]['label_counts'][lab] for s in splits])/1000
                ax.bar(range(3),count,bottom=bottom,color=c,label=label,width=.58)
                for j,v in enumerate(count):ax.text(j,bottom[j]+v/2,f'{v:.1f}k',ha='center',va='center',fontsize=10)
                bottom+=count
            ax.set_xticks(range(3),[f'{s.title()}\n{results["data"][s]["proteins"]} proteins' for s in splits])
            ax.set(ylabel='Number of residues / thousand',title='E  Three labels, with whole-component splitting')
            ax.legend(frameon=False,fontsize=9)
        else:
            ax.plot([0,1],[0,1],c='#b8b9ab',ls='--',label='Equal score and observed fraction')
            edges=np.linspace(0,1,11)
            for k,c,label in zip(names,colors,labels):
                xx=[];observed=[];counts=[]
                bins=np.clip(np.digitize(pp[k],edges)-1,0,9)
                for b in range(10):
                    use=bins==b
                    if use.sum()>=30:xx.append(pp[k][use].mean());observed.append(yy[use].mean());counts.append(use.sum())
                ax.plot(xx,observed,c=c,lw=1,label=label)
                ax.scatter(xx,observed,c=c,s=12+np.array(counts)/60,alpha=.6)
            ax.set(xlim=(0,1),ylim=(0,1),xlabel='Mean predicted score in a bin',ylabel='Observed annotated-disorder fraction',title='F  Does a score behave like a probability?')
            ax.legend(frameon=False,fontsize=8,loc='upper left')
        ax.grid(alpha=.14)
    keys=['sequence','ranking','protein_errors','learning','data','calibration']
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.4,5.4),layout='constrained',facecolor='#fffdf8');panel(ax,key)
        fig.savefig(OUT/(key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(16,18),layout='constrained',facecolor='#fffdf8')
    for ax,key in zip(axes.flat,keys):panel(ax,key)
    fig.savefig(OUT/'protein_learning.svg',metadata={'Date':None})
    fig.savefig(OUT/'protein_learning.png',dpi=160,metadata={'Software':'Matplotlib'});plt.close(fig)

if __name__=='__main__':main()
