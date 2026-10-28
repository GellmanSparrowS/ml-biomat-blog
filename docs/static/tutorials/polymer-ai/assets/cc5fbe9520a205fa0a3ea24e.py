"""Read fiber orientation and predict a controlled frame response from images.

Dependencies: numpy, scipy, torch, scikit-learn, matplotlib, Pillow, requests.
Simulation uses fixed EA=1 and EI=.0005, length unit l0=1, small strain .001.
All crossings are welded and all boundary rotations are fixed.
Real fibronectin image: Arafat et al., PLOS ONE (2025), doi:10.1371/journal.pone.0320006.
The author-provided TIFF is downloaded once and SHA256 checked.
Experimental image analysis is separate from simulated mechanical learning.
"""
from pathlib import Path
import os,copy,json,hashlib
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from scipy.ndimage import gaussian_filter,sobel
import torch
from torch import nn
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from PIL import Image
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
OUT=Path('fiber_outputs')
torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)

def beam(xa,xb,EA=1.,EI=.0005):
    d=xb-xa;L=float(np.linalg.norm(d));c,s=d/L
    local=np.zeros((6,6));local[np.ix_([0,3],[0,3])]=EA/L*np.array([[1,-1],[-1,1]])
    ids=[1,2,4,5]
    local[np.ix_(ids,ids)]=EI/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
    R=np.array([[c,s,0],[-s,c,0],[0,0,1.]])
    T=np.zeros((6,6));T[:3,:3]=R;T[3:,3:]=R
    return T.T@local@T

def stiffness_matrix(x,edges,EA=1.,EI=.0005):
    K=np.zeros((3*len(x),3*len(x)))
    for i,j in edges:
        ids=np.r_[np.arange(3*i,3*i+3),np.arange(3*j,3*j+3)]
        K[np.ix_(ids,ids)]+=beam(x[i],x[j],EA,EI)
    return K

def response(x,edges,boundary,direction,epsilon=.001,EA=1.,EI=.0005):
    x=np.array(x);n=np.array(direction);K=stiffness_matrix(x,edges,EA,EI)
    fixed=np.array([d for i in boundary for d in [3*i,3*i+1,3*i+2]])
    free=np.setdiff1d(np.arange(len(K)),fixed);u=np.zeros(len(K))
    affine=epsilon*np.outer((x-.5)@n,n)
    u.reshape(-1,3)[boundary,:2]=affine[boundary]
    if len(free):u[free]=np.linalg.solve(K[np.ix_(free,free)],-K[np.ix_(free,fixed)]@u[fixed])
    force=K@u;energy=float(.5*u@force)
    residual=float(max(abs(force[free]),default=0));assert residual<1e-7
    return dict(response=2*energy/epsilon**2,energy=energy,displacement=u.reshape(-1,3).tolist(),residual=residual)

def geometry(rng):
    while True:
        count=int(rng.integers(6,11));mean=rng.uniform(0,np.pi);concentration=float(rng.choice([0.,1.,3.,7.]))
        angles=(rng.vonmises(2*mean,concentration,count)/2)%np.pi
        segments=[]
        for a in angles:
            direction=np.array([np.cos(a),np.sin(a)]);normal=np.array([-direction[1],direction[0]])
            point=np.array([.5,.5])+rng.uniform(-.36,.36)*normal
            hits=[]
            for axis in [0,1]:
                if abs(direction[axis])<1e-10:continue
                for side in [0.,1.]:
                    t=(side-point[axis])/direction[axis];q=point+t*direction
                    if -1e-10<=q[1-axis]<=1+1e-10:hits.append((t,q))
            hits.sort(key=lambda z:z[0]);segments.append(np.array([hits[0][1],hits[-1][1]]))
        nodes=[];boundary=[];locations=[[] for _ in segments]
        for i,seg in enumerate(segments):
            for t,point in [(0.,seg[0]),(1.,seg[1])]:
                k=len(nodes);nodes.append(point);boundary.append(k);locations[i].append((t,k))
        for i in range(count):
            for j in range(i+1,count):
                a,b=segments[i];c,d=segments[j];matrix=np.column_stack([b-a,-(d-c)])
                if abs(np.linalg.det(matrix))<1e-9:continue
                t,s=np.linalg.solve(matrix,c-a)
                if 1e-9<t<1-1e-9 and 1e-9<s<1-1e-9:
                    k=len(nodes);nodes.append(a+t*(b-a));locations[i].append((t,k));locations[j].append((s,k))
        x=np.array(nodes);edges=[]
        for loc in locations:
            loc.sort();edges.extend((a[1],b[1]) for a,b in zip(loc[:-1],loc[1:]))
        edges=np.array(edges);length=np.linalg.norm(x[edges[:,1]]-x[edges[:,0]],axis=1)
        if length.min()<.008:continue
        n=(x[edges[:,1]]-x[edges[:,0]])/length[:,None]
        q=np.sum(length[:,None]*np.c_[n[:,0]**2-n[:,1]**2,2*n[:,0]*n[:,1]],axis=0)/length.sum()
        return dict(x=x.tolist(),edges=edges.tolist(),boundary=boundary,segments=np.array(segments).tolist(),
                    fiber_count=count,mean_angle=mean,concentration=concentration,length=float(length.sum()),q=q.tolist())

def render(g,rng,variant=0,noise_override=None):
    side=48;yy,xx=np.mgrid[:side,:side];xx=xx/(side-1);yy=1-yy/(side-1)
    points=np.stack([xx,yy],axis=-1);signal=np.zeros((side,side))
    for start,end in np.array(g['segments']):
        d=end-start;t=np.clip(np.sum((points-start)*d,axis=-1)/(d@d),0,1)
        distance=np.linalg.norm(points-(start+t[...,None]*d),axis=-1)
        signal=np.maximum(signal,np.exp(-.5*(distance/.009)**2))
    blur=.35 if variant==0 else .7;noise=.035 if variant==0 else .08
    if noise_override is not None:noise=noise_override
    observed=.08+.8*gaussian_filter(signal,blur)+rng.normal(0,noise,signal.shape)
    return np.clip(observed,0,1).astype(np.float32),signal>.5

def orientation(image):
    smooth=gaussian_filter(image.astype(float),.8)
    gx=sobel(smooth,axis=1)/8;gy=-sobel(smooth,axis=0)/8
    gx=gx[2:-2,2:-2];gy=gy[2:-2,2:-2]
    xx=float(np.sum(gx*gx));yy=float(np.sum(gy*gy));xy=float(np.sum(gx*gy))
    return np.array([yy-xx,-2*xy])/(xx+yy+1e-12)

def generate():
    rng=np.random.default_rng(1414);parents=[];images=[];rows=[]
    for i in range(240):
        g=geometry(rng);g['group']=i;g['split']='test' if i%5==0 else 'validation' if i%5==1 else 'train'
        loads=[response(g['x'],g['edges'],g['boundary'],n) for n in [[1.,0.],[0.,1.]]]
        g['loading_results']=loads;parents.append(g)
        for variant in range(2):
            observed,mask=render(g,rng,variant);image_index=len(images);images.append(observed)
            q=orientation(observed)
            for axis in [0,1]:
                rows.append(dict(group=i,split=g['split'],variant=variant,image_index=image_index,
                    loading=[1.,0.] if axis==0 else [0.,1.],response=loads[axis]['response'],
                    q_true=g['q'],q_image=q.tolist()))
    return parents,np.array(images),rows


def descriptors(g,loading):
    x=np.array(g['x']);edges=np.array(g['edges']);d=x[edges[:,1]]-x[edges[:,0]]
    length=np.linalg.norm(d,axis=1);angle=np.arctan2(d[:,1],d[:,0])-np.arctan2(loading[1],loading[0])
    degree=np.bincount(edges.ravel(),minlength=len(x))
    moments=[float(np.sum(length*f(m*angle))/length.sum()) for m in [2,4] for f in [np.cos,np.sin]]
    affine=np.zeros((len(x),3));n=np.array(loading);affine[:,:2]=np.outer((x-.5)@n,n)
    v=affine.ravel();upper=float(v@stiffness_matrix(x,edges)@v)
    count=[g['length'],g['fiber_count'],g['length']**2]
    rich=count+[len(x),len(edges),float(length.mean()),float(length.std()),float(degree.max()),float(degree.mean()),float(degree.std())]+moments+[upper]
    return count,rich

def image_descriptors(image,loading):
    a=gaussian_filter(image.astype(float),.8);gx=sobel(a,1)[2:-2,2:-2]/8;gy=-sobel(a,0)[2:-2,2:-2]/8
    weight=gx*gx+gy*gy;total=weight.sum()+1e-12
    theta=np.arctan2(gy,gx)+np.pi/2-np.arctan2(loading[1],loading[0])
    moments=[float(np.sum(weight*f(m*theta))/total) for m in [2,4] for f in [np.cos,np.sin]]
    density=float(image.mean());spread=float(image.std())
    return [density,spread,float(weight.mean()),*moments,*[density*v for v in moments],density*density]

class ImageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),
            nn.Conv2d(8,12,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),
            nn.Conv2d(12,16,3,padding=1),nn.ReLU(),nn.AvgPool2d(2))
        self.shared=nn.Sequential(nn.Flatten(),nn.Linear(16*6*6,64),nn.ReLU())
        self.qhead=nn.Linear(64,2)
        self.response=nn.Sequential(nn.Linear(66,32),nn.ReLU(),nn.Linear(32,1))
    def forward(self,image,loading):
        h=self.shared(self.conv(image));q=self.qhead(h)
        q=q/torch.linalg.vector_norm(q,dim=1,keepdim=True).clamp(min=1)
        value=torch.nn.functional.softplus(self.response(torch.cat([h,loading],dim=1)))
        return torch.cat([q,value],dim=1)

def metrics(rows,pred,ids):
    pred=np.asarray(pred,dtype=float)
    y=np.array([rows[i]['response'] for i in ids]);value=np.expm1(pred[ids,2]);q=np.array([rows[i]['q_true'] for i in ids])
    return dict(RMSE=float(np.mean((value-y)**2)**.5),MAE=float(np.mean(abs(value-y))),
                log_RMSE=float(np.mean((pred[ids,2]-np.log1p(y))**2)**.5),q_component_RMSE=float(np.mean((pred[ids,:2]-q)**2)**.5))

def infer(model,images,loads,symmetrized=False):
    predictions=[]
    with torch.no_grad():
        for start in range(0,len(images),64):
            batch=images[start:start+64];v=loads[start:start+64];values=[]
            for k in range(4 if symmetrized else 1):
                sign=(-1)**k
                result=model(torch.rot90(batch,k,[2,3]),sign*v)
                result[:,:2]*=sign;values.append(result)
            predictions.append(torch.stack(values).mean(0).numpy())
    return np.concatenate(predictions)

def main():
    OUT.mkdir(exist_ok=True)
    parents,images,rows=generate();bygroup={g['group']:g for g in parents}
    ids={s:np.array([i for i,r in enumerate(rows) if r['split']==s]) for s in ['train','validation','test']}
    arrays=[descriptors(bygroup[r['group']],r['loading']) for r in rows]
    features={'counts':np.array([a[0] for a in arrays]),'geometry_graph':np.array([a[1] for a in arrays])}
    features['image_features']=np.array([image_descriptors(images[r['image_index']],r['loading']) for r in rows])
    target=np.array([[*r['q_true'],np.log1p(r['response'])] for r in rows])
    observed=np.array([r['q_image'] for r in rows]);result={'baselines':{},'cnn':{},'split_counts':{k:len(v) for k,v in ids.items()}}
    for name,X in features.items():
        scale=StandardScaler().fit(X[ids['train']]);Z=scale.transform(X);best=None;candidates=[]
        for alpha in [.01,.1,1.,10.,100.]:
            model=Ridge(alpha=alpha).fit(Z[ids['train']],target[ids['train'],2])
            pred=np.maximum(0,model.predict(Z));loss=float(np.mean((pred[ids['validation']]-target[ids['validation'],2])**2))
            candidates.append(dict(alpha=alpha,validation_loss=loss))
            if best is None or loss<best[0]:best=(loss,model,alpha,pred)
        p=np.c_[observed,best[3]]
        result['baselines'][name]=dict(predictions=p.tolist(),scores={s:metrics(rows,p,j) for s,j in ids.items()},
            alpha=best[2],scaler_mean=scale.mean_.tolist(),scaler_scale=scale.scale_.tolist(),
            coef=best[1].coef_.tolist(),intercept=float(best[1].intercept_),validation_candidates=candidates)
    # Direct affine trial energy is an upper bound and uses only input geometry.
    p=np.c_[observed,np.log1p(features['geometry_graph'][:,-1])]
    result['baselines']['affine_upper_bound']=dict(predictions=p.tolist(),scores={s:metrics(rows,p,j) for s,j in ids.items()})
    t=torch.tensor(target,dtype=torch.float32)
    im=torch.tensor(images[[r['image_index'] for r in rows],None],dtype=torch.float32)
    loading=torch.tensor([[r['loading'][0]**2-r['loading'][1]**2,2*r['loading'][0]*r['loading'][1]] for r in rows])
    def lossfn(p,y):return torch.mean((p[:,:2]-y[:,:2])**2)+torch.mean((p[:,2]-y[:,2])**2)
    saved=[];raws=[];sym=[]
    noisy=[]
    for i,image in enumerate(images):
        g=parents[i//2];image2,_=render(g,np.random.default_rng(4141+i),variant=1,noise_override=.16);noisy.append(image2)
    noisy=torch.tensor(np.array(noisy)[[r['image_index'] for r in rows],None],dtype=torch.float32)
    noisy_preds=[];rotated=[]
    for seed in [14,24,34]:
        torch.manual_seed(seed);model=ImageModel();optimizer=torch.optim.Adam(model.parameters(),lr=.001)
        rng=np.random.default_rng(1415);bestloss=float('inf');wait=0;history=[]
        for epoch in range(1,81):
            model.train();order=rng.permutation(ids['train'])
            for start in range(0,len(order),64):
                ix=order[start:start+64];k=int(rng.integers(0,4));sgn=(-1)**k
                batch=torch.rot90(im[ix],k,[2,3]);truth=t[ix].clone();truth[:,:2]*=sgn
                optimizer.zero_grad();loss=lossfn(model(batch,sgn*loading[ix]),truth);loss.backward();optimizer.step()
            model.eval()
            with torch.no_grad():
                vl=float(lossfn(model(im[ids['validation']],loading[ids['validation']]),t[ids['validation']]))
                tl=float(lossfn(model(im[ids['train']],loading[ids['train']]),t[ids['train']]))
            history.append(dict(epoch=epoch,train=tl,validation=vl))
            if vl<bestloss-1e-7:bestloss=vl;bestepoch=epoch;weights=copy.deepcopy(model.state_dict());wait=0
            else:wait+=1
            if wait>=12:break
        model.load_state_dict(weights);model.eval()
        raw=infer(model,im,loading);s=infer(model,im,loading,True)
        rot=infer(model,torch.rot90(im,1,[2,3]),-loading);rot[:,:2]*=-1
        raws.append(raw);sym.append(s);rotated.append(rot);noisy_preds.append(infer(model,noisy,loading,True))
        saved.append(dict(seed=seed,best_epoch=bestepoch,history=history,parameters=sum(p.numel() for p in model.parameters()),
                          state_dict={k:v.numpy().tolist() for k,v in weights.items()}))
        print('seed',seed,'best epoch',bestepoch,'validation loss',bestloss,flush=True)
    avg=np.mean(raws,axis=0);sy=np.mean(sym,axis=0);noise=np.mean(noisy_preds,axis=0);rot=np.mean(rotated,axis=0)
    result['cnn']=dict(seeds=saved,raw_predictions=avg.tolist(),symmetrized_predictions=sy.tolist(),
        noisy_predictions=noise.tolist(),rotated_back_predictions=rot.tolist(),
        scores_raw={s:metrics(rows,avg,j) for s,j in ids.items()},
        scores_symmetrized={s:metrics(rows,sy,j) for s,j in ids.items()},
        scores_noisy_test=metrics(rows,noise,ids['test']),
        rotation_raw_q_RMSE=float(np.mean((rot[ids['test'],:2]-avg[ids['test'],:2])**2)**.5),
        rotation_raw_response_MAE=float(np.mean(abs(np.expm1(rot[ids['test'],2])-np.expm1(avg[ids['test'],2])))))
    result['orientation_baseline_test_RMSE']=float(np.mean((observed[ids['test']]-target[ids['test'],:2])**2)**.5)
    result['scope']='Generated 2D Euler-Bernoulli frames; prescribed affine boundary strain; C=2U/epsilon^2 in EA*l0 units.'
    result['parents']=parents
    result['generator_seed']=1414
    result['experimental_image']=experimental_analysis()
    make_plots(parents,images,rows,result,OUT)
    for i,row in enumerate(rows):
        row['cnn_prediction']=result['cnn']['symmetrized_predictions'][i]
        row['baseline_predictions']={name:m['predictions'][i] for name,m in result['baselines'].items()}
    (OUT/'samples.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    np.save(OUT/'images.npy',images)
    print(json.dumps({'baselines':{k:v['scores']['test'] for k,v in result['baselines'].items()},
          'raw':result['cnn']['scores_raw']['test'],'symmetrized':result['cnn']['scores_symmetrized']['test'],
          'noise':result['cnn']['scores_noisy_test'],'orientation_baseline':result['orientation_baseline_test_RMSE']},indent=2))


def make_plots(parents,images,rows,r,out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
        'text.color':'#29433a','axes.labelcolor':'#29433a','svg.hashsalt':'L14-fibers','axes.titlepad':15,
        'figure.facecolor':'#fffdf8','savefig.facecolor':'#fffdf8'})
    out.mkdir(exist_ok=True);test=np.array([i for i,x in enumerate(rows) if x['split']=='test'])
    row=rows[test[0]];g=parents[row['group']];x=np.array(g['x']);edges=np.array(g['edges'])
    cnn=np.array(r['cnn']['symmetrized_predictions']);base=np.array(r['baselines']['image_features']['predictions'])
    names=['counts','image_features','cnn','geometry_graph','affine_upper_bound']
    labels=['Fiber / length counts','Measured image features','Image CNN + four rotations','Known geometry / graph','Affine physical upper bound']
    def draw(ax,key):
        if key=='observation':
            ax.axis('off');ax.set_title('A  Known geometry and an imperfect image')
            left=ax.inset_axes([.02,.12,.45,.77]);right=ax.inset_axes([.53,.12,.45,.77])
            left.add_collection(LineCollection(x[edges],colors='#43816b',linewidths=1.7));left.scatter(x[:,0],x[:,1],s=7,c='#ae8053')
            left.set(xlim=(0,1),ylim=(0,1),aspect='equal',title='Explicit welded crossings');left.axis('off')
            right.imshow(images[row['image_index']],cmap='gray',vmin=0,vmax=1,extent=(0,1,0,1));right.set_title('48 x 48 observed pixels');right.axis('off')
            ax.text(.5,.02,'First held-out parent; two imaging variants stay in the same group',ha='center',transform=ax.transAxes,fontsize=8)
        elif key=='orientation':
            ax.axis('off');ax.set_title('B  Direction is an axis, without an arrowhead')
            polar=ax.inset_axes([.02,.16,.43,.7],projection='polar');vec=ax.inset_axes([.58,.18,.38,.64])
            d=x[edges[:,1]]-x[edges[:,0]];length=np.linalg.norm(d,axis=1);theta=np.arctan2(d[:,1],d[:,0])%np.pi
            bins=np.linspace(0,np.pi,19);hist,_=np.histogram(theta,bins=bins,weights=length);hist/=hist.sum();centers=(bins[:-1]+bins[1:])/2
            polar.bar(np.r_[centers,centers+np.pi],np.tile(hist,2),width=np.pi/18*.9,color='#8eb19c')
            polar.set_yticks([]);polar.tick_params(labelsize=8);polar.set_title('Length-weighted directions',fontsize=9)
            for q,c,label in [(g['q'],'#ae8053','Geometry'),(row['q_image'],'#6589a2','Structure tensor'),(cnn[test[0],:2],'#267b69','Image CNN')]:
                vec.quiver(0,0,q[0],q[1],angles='xy',scale_units='xy',scale=1,color=c,width=.012,label=label)
            circle=np.linspace(0,2*np.pi,100);vec.plot(np.cos(circle),np.sin(circle),':',c='#c8c8bd')
            vec.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),aspect='equal',xlabel='q_x')
            vec.text(.03,.97,'q_y',ha='left',va='top',transform=vec.transAxes,fontsize=9)
            vec.legend(fontsize=7,loc='upper center',bbox_to_anchor=(.5,-.17));vec.grid(alpha=.15)
        elif key=='deformation':
            ax.set_title('C  Internal nodes translate and rotate')
            ax.add_collection(LineCollection(x[edges],colors='#c9cec3',linewidths=1))
            u=np.array(g['loading_results'][0]['displacement']);curves=[];amp=80
            for a,b in edges:
                d=x[b]-x[a];L=np.linalg.norm(d);t=d/L;normal=np.array([-t[1],t[0]])
                s=np.linspace(0,1,15);axial=(1-s)*(u[a,:2]@t)+s*(u[b,:2]@t)
                bend=(1-3*s*s+2*s**3)*(u[a,:2]@normal)+L*(s-2*s*s+s**3)*u[a,2]+(3*s*s-2*s**3)*(u[b,:2]@normal)+L*(-s*s+s**3)*u[b,2]
                curves.append(x[a]+s[:,None]*d+amp*(axial[:,None]*t+bend[:,None]*normal))
            ax.add_collection(LineCollection(curves,colors='#397d67',linewidths=1.6))
            boundary=g['boundary'];moved=x+amp*u[:,:2];ax.scatter(moved[boundary,0],moved[boundary,1],s=18,c='#ae8053',label='Prescribed boundary nodes')
            ax.set(xlim=(-.1,1.1),ylim=(-.1,1.1),aspect='equal',xlabel='x / l0',ylabel='y / l0')
            ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.13));ax.text(.5,.98,'x-directed affine boundary strain; displacements x 80',ha='center',va='top',transform=ax.transAxes,fontsize=8)
        elif key=='prediction':
            truth=np.array([rows[i]['response'] for i in test])
            ax.scatter(truth,np.expm1(base[test,2]),s=19,c='#c29a6e',alpha=.55,label='Measured image features')
            ax.scatter(truth,np.expm1(cnn[test,2]),s=19,c='#397e69',alpha=.55,label='Image CNN + four rotations')
            limit=max(truth.max(),np.expm1(cnn[test,2]).max());ax.plot([0,limit],[0,limit],':',color='#8c8f7b')
            ax.set(xlabel='Independent beam solution / (EA l0)',ylabel='Prediction / (EA l0)',title='D  Response on 48 unseen parent networks')
            ax.legend(fontsize=8);ax.grid(alpha=.12)
        elif key=='scores':
            vals=[r['cnn']['scores_symmetrized']['test']['RMSE'] if n=='cnn' else r['baselines'][n]['scores']['test']['RMSE'] for n in names]
            ax.barh(range(5),vals,color=['#bcc3b2','#b89b77','#448c73','#6b91aa','#91b0a0']);ax.set_yticks(range(5),labels,fontsize=8);ax.invert_yaxis()
            for i,v in enumerate(vals):ax.text(v+.025,i,f'{v:.3f}',va='center',fontsize=9)
            ax.set(xlim=(0,max(vals)*1.17),xlabel='Response RMSE / (EA l0)',title='E  Compare models with their input information')
            ax.grid(axis='x',alpha=.12)
        elif key=='checks':
            ax.axis('off');ax.set_title('F  Noise and a joint 90-degree rotation')
            left=ax.inset_axes([.13,.18,.38,.66]);right=ax.inset_axes([.67,.18,.29,.66])
            vals=[r['orientation_baseline_test_RMSE'],r['cnn']['scores_symmetrized']['test']['q_component_RMSE'],r['cnn']['scores_noisy_test']['q_component_RMSE']]
            left.bar(range(3),vals,color=['#6b91aa','#448c73','#bc986b']);left.set_xticks(range(3),['Tensor','CNN','CNN\nmore noise'],fontsize=8)
            left.set_ylabel('q-component RMSE');left.grid(axis='y',alpha=.12)
            right.bar([0,1],[r['cnn']['rotation_raw_response_MAE'],0],color=['#9aaea0','#397e69'])
            right.set_xticks([0,1],['Raw','Four-rotation\naverage'],fontsize=8);right.set_ylabel('Prediction change / (EA l0)')
            right.text(1,0,'0 by symmetry',ha='center',va='bottom',rotation=90,fontsize=8)
            ax.text(.5,.02,'Orientation uses q = <cos(2theta), sin(2theta)>; response rotation moves loading too.',ha='center',transform=ax.transAxes,fontsize=8)
    keys=['observation','orientation','deformation','prediction','scores','checks']
    for key in keys:
        fig,ax=plt.subplots(figsize=(7.8,5.4),layout='constrained');draw(ax,key)
        fig.savefig(out/(key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(15.6,16.2),layout='constrained')
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(out/'fiber_learning.png',dpi=160);fig.savefig(out/'fiber_learning.svg',metadata={'Date':None});plt.close(fig)


def tensor(image,roi=None):
    smooth=gaussian_filter(image.astype(float),1.)
    gx=sobel(smooth,axis=1)/8;gy=-sobel(smooth,axis=0)/8
    xx=gaussian_filter(gx*gx,3);yy=gaussian_filter(gy*gy,3);xy=gaussian_filter(gx*gy,3)
    energy=xx+yy;difference=np.sqrt((xx-yy)**2+4*xy*xy)
    coherency=difference/(energy+1e-15)
    theta=(.5*np.arctan2(-2*xy,yy-xx))%np.pi
    valid=np.zeros_like(image,dtype=bool);valid[10:-10,10:-10]=True
    if roi is not None:valid&=roi
    threshold=np.percentile(energy[valid],60)
    valid&=(energy>=threshold)&(coherency>=.2)
    q=np.array([np.sum(energy[valid]*np.cos(2*theta[valid])),np.sum(energy[valid]*np.sin(2*theta[valid]))])/np.sum(energy[valid])
    return dict(theta=theta,coherency=coherency,energy=energy,valid=valid,q=q,threshold=threshold)

def experimental_analysis():
    path=OUT/'Fluorescent_Fibronectin.tif'
    url='https://raw.githubusercontent.com/youssefarafat/Trace_Ridges/ab919e66a0f65b10b6aeb51d7510aedc8e0200dc/Fluorescent_Fibronectin.tif'
    if not path.exists():
        response=requests.get(url,timeout=40);response.raise_for_status();path.write_bytes(response.content)
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='d9107c136570141d3fe55c9ad8ef4dbf71ffb27e9abbe2bda2efed65be2bc18a'
    img=Image.open(path);raw=np.array(img)
    assert raw.ndim==3 and raw.shape[2]==3,raw.shape
    original=(raw.astype(float)@np.array([.299,.587,.114]))/np.iinfo(raw.dtype).max
    roi=np.ones(original.shape,dtype=bool);roi[-70:,-230:]=False
    data=tensor(original,roi);rotated=tensor(np.rot90(original),np.rot90(roi))
    error=float(np.max(abs(data['q']+rotated['q'])))
    assert error<1e-12
    e=data['energy'];coh=data['coherency'];theta=data['theta'];v=data['valid']
    # Independently recover the local director as the smaller-eigenvalue eigenvector.
    smooth=gaussian_filter(original,1);gx=sobel(smooth,1)/8;gy=-sobel(smooth,0)/8
    xx=gaussian_filter(gx*gx,3);yy=gaussian_filter(gy*gy,3);xy=gaussian_filter(gx*gy,3)
    points=np.argwhere(v)[::401];maxerr=0
    for row,col in points:
        _,vec=np.linalg.eigh([[xx[row,col],xy[row,col]],[xy[row,col],yy[row,col]]])
        n=vec[:,0];q=np.array([n[0]**2-n[1]**2,2*n[0]*n[1]])
        target=np.array([np.cos(2*theta[row,col]),np.sin(2*theta[row,col])])
        maxerr=max(maxerr,float(np.max(abs(q-target))))
    assert maxerr<1e-12
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'L14-fibronectin','font.size':10,'figure.facecolor':'#fffdf8','savefig.facecolor':'#fffdf8'})
    def draw(ax,key):
        if key=='source':
            ax.imshow(original,cmap='gray');ax.set_title('A  Author-provided fibronectin image');ax.axis('off')
        elif key=='directions':
            show=np.where(v,theta*180/np.pi,np.nan)
            im=ax.imshow(show,cmap='twilight',vmin=0,vmax=180)
            ax.figure.colorbar(im,ax=ax,label='Local direction / degrees',shrink=.7)
            ax.set_title('B  Selected local fiber directions');ax.axis('off')
        elif key=='overlay':
            ax.imshow(original,cmap='gray',alpha=.65)
            sy,sx=np.mgrid[20:raw.shape[0]-20:32,20:raw.shape[1]-20:32];ok=v[sy,sx];angle=theta[sy,sx]
            xxp=sx[ok];yyp=sy[ok];tt=angle[ok]
            ax.quiver(xxp,yyp,np.cos(tt),-np.sin(tt),angles='xy',scale_units='xy',scale=.06,color='#d9b46d',width=.003,headwidth=0,headlength=0,headaxislength=0,pivot='mid')
            ax.set_title('C  Local directions over the observation');ax.axis('off')
        else:
            bins=np.linspace(0,np.pi,37);hist,_=np.histogram(theta[v],bins=bins,weights=e[v]);hist/=hist.sum()
            ax.bar((bins[:-1]+bins[1:])*90/np.pi,hist,width=4.5,color='#488b76')
            ax.set(xlabel='Unoriented direction / degrees',ylabel='Gradient-energy weighted fraction',title='D  Image orientation distribution')
    keys=['source','directions','overlay','distribution']
    for key in keys:
        fig,ax=plt.subplots(figsize=(6,5.5),layout='constrained');draw(ax,key)
        fig.savefig(OUT/('experimental_'+key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(10,9),layout='constrained')
    for ax,key in zip(axes.flat,keys):draw(ax,key)
    fig.savefig(OUT/'experimental_orientation.png',dpi=150);fig.savefig(OUT/'experimental_orientation.svg',metadata={'Date':None});plt.close(fig)
    report=dict(source='https://raw.githubusercontent.com/youssefarafat/Trace_Ridges/ab919e66a0f65b10b6aeb51d7510aedc8e0200dc/Fluorescent_Fibronectin.tif',
        commit='ab919e66a0f65b10b6aeb51d7510aedc8e0200dc',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        authors='Youssef Arafat, Cristina Cuesta-Apausa, Esther Castellano, Constantino Carlos Reyes-Aldasoro',
        paper='https://doi.org/10.1371/journal.pone.0320006',year=2025,
        image_credit='Author-provided fluorescent fibronectin image from the original study; analysis reproduced with attribution.',
        article_license='CC BY',
        shape=list(raw.shape),dtype=str(raw.dtype),frames=getattr(img,'n_frames',1),
        grayscale_conversion='RGB luminance .299R+.587G+.114B, divided by255; source unchanged',
        excluded_annotation_rectangle_xy=[raw.shape[1]-230,raw.shape[0]-70,raw.shape[1],raw.shape[0]],
        roi_rotation='The exclusion mask is rotated together with the image.',
        gray_range=[int(raw.min()),int(raw.max())],q=data['q'].tolist(),selected_fraction=float(v.mean()),
        gradient_smoothing_pixels=1,tensor_smoothing_pixels=3,coherency_minimum=.2,energy_percentile=60,
        joint_image_rotation_q_max_error=error,independent_eigenvector_max_error=maxerr,independent_points=len(points),
        scope='Experimental image direction statistics and rotation consistency; synthetic frame mechanics is a separate controlled task.',passed=True)
    return report


if __name__=='__main__':main()
